# AGENTS.md — entry point for any AI agent working in this repository

Read this first. It is a **router**, not a manual: it tells you what this repo is and where the real instructions live. Detailed procedure lives in skills, which load on demand.

**Read-status per agent — verified by cold-session test 2026-08-31, not self-reported:**

All three were asked, in a fresh session with this repo as the working directory and no tools allowed, for two facts that exist **only** in this file (that `16_Legal_and_Regulations/` is Belarus-only, and the merge-to-main rule).

| Agent | Receives this file automatically? | Evidence |
| :--- | :--- | :--- |
| **Antigravity** | **Yes** | Answered both, plus listed all four skills and knew the deprecated one. Discovery walks up from cwd; no `GEMINI.md` needed. |
| **Codex** | **Yes** | Answered both exactly. ⚠️ Note it had earlier *reported* it does not receive this file — **its self-report was wrong**; trust the test. |
| **Claude Code** | **Yes, via the `@AGENTS.md` import in `CLAUDE.md`** | ⚠️ **Failed this test on first run** and was the only agent that did. `CLAUDE.md` held a markdown *link*, which is inert prose — Claude loaded the stub, read "see AGENTS.md", and never opened it. Replaced with an `@`-import and **retested in a fresh session the same day: passes.** This is why the stub must stay an import. |

> [!WARNING]
> **None of these agents can be trusted about its own context loading.** Codex gave three mutually inconsistent accounts of whether it reads this file; Claude Code asserted it was readable via the stub when it was not. **Ask an agent what it knows, never how it knows it** — the answers are evidence, the introspection isn't.

---

## What this repository actually is

**A personal renovation knowledge base and planning vault** for one specific apartment renovation, built from ~813 extraction notes taken mostly from Russian-language YouTube practitioner sources, routed into ~243 wiki pages.

> [!IMPORTANT]
> **`README.md` describes the original project, not the current one.** This repo began as a Node/TypeScript/Playwright/SQLite marketplace price scraper (`src/`, `package.json`, `data/`). That code still exists and still runs, but it is now a *minor component*. If you read only the README you will work on the wrong thing.

The renovation vault is the primary work. The scraper feeds appliance pricing into it.

## Layout

| Path | What it holds |
| :--- | :--- |
| `_Sources/` | ~813 extraction notes, one per source. **Raw evidence — never edit to fit a conclusion.** |
| `_Knowledge/store/` | Intermediate store: `Durable_Facts`, `Rules_Heuristics`, `Numeric_Data`, `Source_Index`, `Change_Log`, `Cross_Source_Comparison_Tables` |
| `00_Master/` | Project-level docs. **Start with `project_decisions.md`** — decisions taken about this apartment, and the open items. Also the deliverable roadmap, `processed_sources.csv`, `exchange_rates_reference.md`, `wiki_page_format.md` |
| `01_`–`17_` | Room and topic wiki folders. Each has a compact guide page plus `analysis/` detail pages |
| `_Archive/processed_sources/` | Archived transcripts. **Frozen — hashed for provenance; never edit, not even to fix a BOM** |
| `_Inbox/planning/` | Channel triage plans, backlogs, work-in-progress notes |
| `src/`, `data/`, `dist/` | The legacy price scraper (Node/TS/Playwright/SQLite) |
| `tools/` | Python tooling — see below |
| `.agents/skills/` | Project-specific skills. **See the discovery note below — this differs per agent** |

## Skills

> [!WARNING]
> **Skill discovery is asymmetric across agents. Verified 2026-08-31.**
> - **Antigravity** auto-discovers `.agents/skills/**/SKILL.md` and mounts them.
> - **Codex** does **not** discover them. If you are Codex, read the relevant `SKILL.md` file explicitly before starting work.
> - **Claude Code** does not treat them as Skill-tool-invocable either; read the file.
>
> Do not assume a skill is loaded because it exists.

| Skill | Use it for |
| :--- | :--- |
| `.agents/skills/renovation-knowledge-intake/SKILL.md` | **The main pipeline.** Ingesting any new source into the vault: extraction notes, the store, wiki routing, USD normalisation, dedup, archiving. Read this before processing any source |
| `.agents/skills/apartment-layout-modelling/SKILL.md` | Layout case datasets, frames → case JSON → rules JSONL → prose |
| `.agents/skills/residential-bim-geometry-rules/SKILL.md` | Geometry conventions for the model |
| `.agents/skills/homestyler-cad-to-revit/SKILL.md` | CAD/Revit interchange |

Shared cross-project skills live in `../ai-skills/skills/` and are linked into `~/.claude/skills/` and `~/.codex/skills/`. `youtube-transcript-fetch` is the one you will most often need.

## Tools — run these, don't reimplement them

| Tool | Purpose |
| :--- | :--- |
| `tools/verify_batch.py --base <ref>` | **Run before every commit that touches vault content.** Mojibake, BOM, retired patterns, citation-ID drift, USD rounding and rate checks |
| `scripts/verify_batch_selftest.py` | Guards the above against over-suppression. Run after changing it |
| `tools/check_page_sizes.py` | **Enforces the 300-line hard page ceiling — exits non-zero on a breach.** Also warns below it, and flags FRAGMENTED pages, which means merge instead |
| `tools/split_page.py analyse\|apply\|merge` | Does the split or the merge. Moves sections by line range byte-for-byte, then asserts content-line and citation-ID parity |
| `tools/build_knowledge_base_index.py` | Rebuilds the numeric-claims index |
| `tools/youtube/preflight_playlist.py` | Dedup a playlist/channel against `processed_video_ids.txt` before fetching |
| `tools/youtube/archive_transcripts.py <inbox>` | Archive transcripts and repoint `transcript_file:` frontmatter |
| `tools/pricing/currency_converter.py` | Historical FX. **Never use a spot rate for a historical figure** |

## Standing rules

These are the ones that cause real damage when broken. Everything else is in the skills.

1. **Original language only.** Never fetch or cite auto-translated English captions for a Russian source. Force `--languages ru`. Preserve Russian terms inline in notes and wiki pages — searchability depends on it.
2. **A price is meaningless without location and year.** Never compare two figures until both are resolved. Confirm dates from `yt-dlp` metadata, not from the title.
3. **Attribute every claim to a named practitioner, as opinion.** Nothing in this vault is a flat fact. Name the person or company inline, per claim — not just in a Source Notes block at the bottom.
4. **`16_Legal_and_Regulations/` is Belarus-only.** A Russian-sourced regulatory claim never goes there, not even hedged. Route it to the relevant technical page with the jurisdiction flagged.
5. **Value-filter before batch processing.** For any playlist or channel, title-skim and spot-check transcripts first. Do not process everything by default.
6. **Route to wiki pages in the same turn as extraction** (intake step 5a). Batching it up for later has caught real errors precisely because it was done late — don't rely on that.
7. **Serialize YouTube fetches**, one at a time with spacing and bounded backoff. A rate-limit can be IP-wide across all channels — pause, don't rotate channels into the same wall.
8. **No wiki page reaches 300 lines, and pages are organised by topic, not by intake date.** `tools/check_page_sizes.py` exits non-zero on a ceiling breach and the exceptions file cannot waive it. **Before adding a heading, look for an existing section the fact belongs under** — pages get to 700 lines by twenty batches each appending a little, not by a decision. **Diagnose by reading the headings**: topic headings mean the page is fine; headings like "… (added 2026-09-01, Round 4)" mean it is FRAGMENTED. Fragmented → `tools/split_page.py merge` (demotes the dated headings to `###`, keeping every attribution). Oversized → `apply`. **Both at once → merge first, then extract.** See `00_Master/wiki_page_format.md`.
9. **Merge to main every time.** After commit and push on a branch: merge `--no-ff` into main, push main, delete the branch locally and remotely. No lingering branches, no PRs.

## Conventions

- Page shape: see `00_Master/wiki_page_format.md`. Compact guide page + `analysis/` detail pages, with Perspectives / Common Ground / Your Priority blocks for genuine source disagreements.
- Pages fail in **two** directions: too long, and **fragmented** (many stub sections from each batch appending its own dated heading). The fix for the second is merging. Look for an existing section before adding a heading.
- USD equivalents are rounded comparability aids: nearest 10 below $1,000, nearest 100 to $99,999, nearest 1,000 above. Never show cents. A figure that is exact by construction is tagged `arithmetic-exact` and keeps its precision.
- Areas: developer plans are clear/net, БТИ are gross. Dimensions nominal ±25 mm.

## Cross-repo

`.agents/ai-management-link.md` explains how this repo connects to the sibling `ai-*` repos — shared skills, telemetry, and the cross-agent plan dialogue in `ai-management`.
