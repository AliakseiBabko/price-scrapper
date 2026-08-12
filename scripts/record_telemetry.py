"""Thin wrapper: record price-scrapper telemetry into the shared
ai-telemetry database (C:\\Users\\User\\Documents\\ai-telemetry by default).

This script does NOT talk to the database itself and does NOT reimplement
any of ai-telemetry's write/dedup logic - it just resolves which
ai-telemetry `record_*.py` script a given fact table needs, fills in this
project's own defaults (`--project-id=price-scrapper`,
`--source-system=native`) unless the caller already supplied them, and
execs that script with the rest of the arguments passed straight through.
All real validation (redaction, FK checks, the idempotent
project_id/source_system/source_ref dedup) happens inside ai-telemetry
itself, exactly as it does for any other caller of those scripts.

Usage
-----
    python scripts/record_telemetry.py <kind> [--ai-telemetry-path PATH] <rest of the record_<kind>.py args>

`<kind>` is one of: session, task, skill-invocation, validation,
command-run, artifact-touch, feedback-event - see ai-telemetry's own
README ("Recording native telemetry") for each one's full flag list.

Examples
--------
    python scripts/record_telemetry.py session ^
        --runtime-id claude --session-id abc123 --date 2026-08-12

    python scripts/record_telemetry.py task ^
        --task-type scrape_job --date 2026-08-12 --status-normalized ok

    python scripts/record_telemetry.py validation ^
        --check-name pytest --status-normalized pass --date 2026-08-12

`--source-ref` (idempotency key)
---------------------------------
Not supplied by this wrapper - pass `--source-ref <your-stable-id>`
yourself when you already have one (a scrape run id, a task id -
anything you'd recognize on retry). If you omit it, the underlying
ai-telemetry script mints one itself and prints it prominently on
stdout (this wrapper never captures or hides that output) - reuse that
exact printed value via `--source-ref` on any retry instead of leaving
it out again, or a retry will insert a second row instead of being
recognized as a duplicate.

Defaults (override by passing the flag explicitly)
----------------------------------------------------
    --project-id      price-scrapper
    --source-system   native
    --ai-telemetry-path   C:\\Users\\User\\Documents\\ai-telemetry
                          (or $AI_TELEMETRY_PATH if set)
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

DEFAULT_PROJECT_ID = "price-scrapper"
DEFAULT_SOURCE_SYSTEM = "native"
DEFAULT_AI_TELEMETRY_PATH = r"C:\Users\User\Documents\ai-telemetry"

# kind -> ai-telemetry script that actually performs the write.
SCRIPT_MAP = {
    "session": "record_session.py",
    "task": "record_task.py",
    "skill-invocation": "record_skill_invocation.py",
    "validation": "record_validation.py",
    "command-run": "record_command_run.py",
    "artifact-touch": "record_artifact_touch.py",
    "feedback-event": "record_feedback_event.py",
}


def _has_flag(args: list[str], flag: str) -> bool:
    return any(a == flag or a.startswith(flag + "=") for a in args)


def main() -> int:
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        print("kinds: " + ", ".join(sorted(SCRIPT_MAP)))
        return 0 if argv else 2

    kind = argv[0]
    rest = argv[1:]
    if kind not in SCRIPT_MAP:
        print(f"ERROR: unknown kind {kind!r}. Choose one of: {', '.join(sorted(SCRIPT_MAP))}", file=sys.stderr)
        return 2

    # --ai-telemetry-path is this wrapper's own flag, not forwarded -
    # pull it out of the passthrough args if present.
    ai_telemetry_path = os.environ.get("AI_TELEMETRY_PATH", DEFAULT_AI_TELEMETRY_PATH)
    passthrough: list[str] = []
    i = 0
    while i < len(rest):
        arg = rest[i]
        if arg == "--ai-telemetry-path":
            if i + 1 >= len(rest):
                print("ERROR: --ai-telemetry-path requires a value.", file=sys.stderr)
                return 2
            ai_telemetry_path = rest[i + 1]
            i += 2
            continue
        if arg.startswith("--ai-telemetry-path="):
            ai_telemetry_path = arg.split("=", 1)[1]
            i += 1
            continue
        passthrough.append(arg)
        i += 1

    target_script = Path(ai_telemetry_path) / "scripts" / SCRIPT_MAP[kind]
    if not target_script.exists():
        print(f"ERROR: {target_script} not found - check --ai-telemetry-path / $AI_TELEMETRY_PATH.", file=sys.stderr)
        return 1

    # Inject this project's own defaults unless the caller already
    # supplied them explicitly - never override an explicit caller value.
    if not _has_flag(passthrough, "--project-id"):
        passthrough = ["--project-id", DEFAULT_PROJECT_ID] + passthrough
    if not _has_flag(passthrough, "--source-system"):
        passthrough = ["--source-system", DEFAULT_SOURCE_SYSTEM] + passthrough

    cmd = [sys.executable, str(target_script), *passthrough]
    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
