#!/usr/bin/env python3
"""Verify that this repository is readable by any AI agent, not just the one
that happened to write it.

Proposed independently by ANTIGRAVITY and CODEX in the AGENT_KNOWLEDGE_PORTABILITY
review round (2026-08-31). Two different model families inventing the same check
unprompted is the strongest signal that round produced, so it exists.

CODEX's formulation is the one implemented, because it separates three contracts
the original plan had conflated:

  1. INSTRUCTION SCOPE   - AGENTS.md exists, is a router not a manual, and the
                           CLAUDE.md stub points at it.
  2. SKILL DISCOVERY     - every skill AGENTS.md names is actually DISCOVERED by
                           the agent, not merely present on disk.
  3. NO MEMORY LEAKS     - no git-tracked file points into an agent's private,
                           machine-local memory.

Contract 2 cannot be fully automated and this script does not pretend otherwise.
Discovery is a property of each agent's runtime, and the reviews proved the
agents disagree: ANTIGRAVITY auto-discovers `.agents/skills/**/SKILL.md`, CODEX
does not see them at all. A filesystem check would return "pass" for Codex and
be wrong. So contract 2 is split: the file-resolution half is checked here, and
the discovery half is printed as an explicit manual cold-session checklist.

Exit code 0 = all automated contracts pass. 1 = at least one failed.

Usage:
    python tools/verify_agent_readiness.py [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

AGENTS_FILE = "AGENTS.md"
STUB_FILE = "CLAUDE.md"

# Antigravity reported a hard practical limit on router size: AGENTS.md is
# loaded on every turn in every agent, so procedural detail there is an
# unconditional token tax on all three. 150 is the target, 200 the cap.
ROUTER_TARGET_LINES = 150
ROUTER_MAX_LINES = 200

# Two exemptions, both found by running this check against a clean repo on
# 2026-08-31 and watching it flag things that are not defects:
#
#   SELF_PATH  - this file necessarily contains every pattern it searches for.
#                Same self-reference trap as tools/verify_batch.py's SELF_PATH
#                and scripts/verify_batch_selftest.py's fixtures.
#   HISTORICAL - a file may legitimately DESCRIBE the migration away from agent
#                memory. 00_Master/project_decisions.md records that its content
#                was drained out of ~/.claude/projects/.../memory/, which is
#                history, not a live dependency. The defect this check exists to
#                catch is a POINTER - "see <note> in this machine's Claude
#                memory" - because that resolves to nothing for Codex, for
#                Antigravity, or for Claude on another machine. Prose about the
#                past resolves to nothing either, but nobody is meant to follow
#                it. A file declares the exemption explicitly with the marker
#                below, so the check is never silently weakened for a new file.
SELF_PATH = "tools/verify_agent_readiness.py"
HISTORICAL_MARKER = "memory-reference: historical"

# Patterns that indicate a git-tracked file reaching into agent-private memory.
MEMORY_LEAK_PATTERNS = (
    r"claude memory",
    r"machine's Claude",
    r"\.claude/projects",
    r"~/\.gemini/antigravity/(knowledge|brain)",
    r"\.codex/memory",
)

# Require a concrete path with at least one directory segment and no glob
# metacharacter. Without this the pattern also matched prose mentions like
# `.agents/skills/**/SKILL.md` and a bare `SKILL.md`, and reported both as
# unresolvable skills - two false failures on the first run.
SKILL_LINK_RE = re.compile(r"`([A-Za-z0-9_./\-]+/SKILL\.md)`")


def run_git(args: list[str]) -> tuple[int, str]:
    proc = subprocess.run(
        ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8"
    )
    return proc.returncode, proc.stdout


def contract_1_instruction_scope() -> list[dict]:
    findings = []
    agents = REPO_ROOT / AGENTS_FILE
    if not agents.exists():
        findings.append({"contract": 1, "check": "agents_md_exists", "ok": False,
                         "detail": f"{AGENTS_FILE} is missing - agents entering this repo get nothing"})
        return findings
    findings.append({"contract": 1, "check": "agents_md_exists", "ok": True, "detail": AGENTS_FILE})

    lines = agents.read_text(encoding="utf-8").count("\n") + 1
    findings.append({
        "contract": 1, "check": "router_size", "ok": lines <= ROUTER_MAX_LINES,
        "detail": f"{lines} lines (target <={ROUTER_TARGET_LINES}, cap {ROUTER_MAX_LINES})"
                  + ("" if lines <= ROUTER_TARGET_LINES else " - over target; move detail into a skill"),
    })

    stub = REPO_ROOT / STUB_FILE
    if not stub.exists():
        findings.append({"contract": 1, "check": "claude_stub", "ok": False,
                         "detail": f"{STUB_FILE} missing - Claude Code has no entry point"})
    else:
        text = stub.read_text(encoding="utf-8")
        points_at = AGENTS_FILE in text
        findings.append({"contract": 1, "check": "claude_stub", "ok": points_at,
                         "detail": f"{STUB_FILE} -> {AGENTS_FILE}" if points_at
                         else f"{STUB_FILE} exists but does not reference {AGENTS_FILE}"})
    return findings


def contract_2_skill_resolution() -> tuple[list[dict], list[str]]:
    """File-resolution half only. Discovery is per-agent and is returned as a
    manual checklist - see the module docstring."""
    findings = []
    agents = REPO_ROOT / AGENTS_FILE
    if not agents.exists():
        return findings, []

    named = sorted({
        m for m in SKILL_LINK_RE.findall(agents.read_text(encoding="utf-8"))
        if "*" not in m
    })
    if not named:
        findings.append({"contract": 2, "check": "skills_named", "ok": False,
                         "detail": "AGENTS.md names no SKILL.md paths - agents cannot find the procedures"})
        return findings, []

    for rel in named:
        # resolve() follows NTFS junctions, which is exactly the thing that
        # must not be mistaken for discovery
        target = (REPO_ROOT / rel).resolve()
        findings.append({"contract": 2, "check": "skill_resolves", "ok": target.is_file(),
                         "detail": rel if target.is_file() else f"{rel} does NOT resolve to a file"})
    return findings, named


def contract_3_no_memory_leaks() -> list[dict]:
    findings = []
    exempt = {SELF_PATH}
    code, out = run_git(["grep", "-lIF", HISTORICAL_MARKER, "--", "."])
    exempt.update(line.strip() for line in out.splitlines() if line.strip())

    for pattern in MEMORY_LEAK_PATTERNS:
        code, out = run_git(["grep", "-In", "-E", pattern, "--", "."])
        hits = [
            line for line in out.splitlines()
            if line.strip() and line.split(":", 1)[0] not in exempt
        ]
        # git grep exits 1 on no match, which is the passing case here
        findings.append({
            "contract": 3, "check": f"no_leak:{pattern}", "ok": not hits,
            "detail": "clean" if not hits else f"{len(hits)} hit(s): " + "; ".join(hits[:3]),
        })
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    findings = contract_1_instruction_scope()
    resolution, named_skills = contract_2_skill_resolution()
    findings += resolution
    findings += contract_3_no_memory_leaks()

    failed = [f for f in findings if not f["ok"]]

    if args.json:
        print(json.dumps({"findings": findings, "failed": len(failed),
                          "manual_checklist_skills": named_skills}, indent=2, ensure_ascii=False))
        return 1 if failed else 0

    titles = {1: "Instruction scope", 2: "Skill resolution (NOT discovery)", 3: "No memory leaks"}
    for contract in (1, 2, 3):
        print(f"\n{titles[contract]}")
        for f in [x for x in findings if x["contract"] == contract]:
            print(f"  {'PASS' if f['ok'] else 'FAIL'}  {f['check']:<28} {f['detail']}")

    print("\n" + "=" * 72)
    print("MANUAL: cold-session discovery test - this script CANNOT check it")
    print("=" * 72)
    print("Skill discovery differs per agent. Verified 2026-08-31: Antigravity")
    print("auto-discovers .agents/skills/, Codex does not see them at all. A")
    print("filesystem check passes in both cases and is therefore worthless here.")
    print("\nIn a COLD session of each agent, with no prior context, confirm it can:")
    print("  1. state what this repository is (renovation vault, not the scraper);")
    print("  2. name where a new source note goes;")
    print("  3. invoke or read each skill below by name.")
    for rel in named_skills:
        print(f"       - {rel}")
    print("\nAgents to test: Claude Code | Codex | Antigravity")

    print(f"\n{len(failed)} automated check(s) failed." if failed
          else "\nAll automated checks passed.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
