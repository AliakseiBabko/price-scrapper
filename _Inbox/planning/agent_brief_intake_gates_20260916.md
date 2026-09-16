# Agent brief — two intake gates: Routing verification, and `covers_also` archiving

**Created 2026-09-16 at the owner's request.** He asked for proposals to improve the source-intake skill; two were chosen and **delegated to Antigravity**, with Claude Code verifying the result afterwards.

**This file is the brief, not the work.** **§1 is the paste-ready prompt.** §2 is how the work will be judged — Antigravity should read it too, because it is the acceptance test. §3 records what was verified in the repo on 2026-09-16, so the prompt's context can be trusted rather than re-derived.

**Scope: two changes only.** Three further proposals (a probe-before-fetch preflight, unambiguous fetcher exit codes, a no-`%`-format rule) were deliberately **not** delegated in this round and are recorded in §4 so they are not lost.

---

## §1 — The prompt

> **You are working in `price-scrapper`. Read `AGENTS.md` first; it is the router, and its standing rules bind this task. Read `00_Master/Validator_Design_Discipline.md` before writing either checker — it is not optional here, because both deliverables are gates and its failure classes are exactly the ones this task can fall into.**
>
> **Build two things. Both are intake-pipeline gates. Neither may reimplement an existing tool — extend what is there.**
>
> ---
>
> ### Task 1 — Gate the Routing section in `tools/verify_batch.py`
>
> **The defect it exists to catch.** Every source note under `_Sources/` ends with a `## Routing` section naming the wiki pages its findings went to. **Nothing has ever checked those claims.** On 2026-09-16 an audit of 133 notes written 2026-09-14..16 found **two sources cited nowhere in the wiki at all** (`1UGUjGmZPNA`, `SwOVFr5YRP8` — since fixed by hand) and **~24 notes whose Routing names a page that does not cite them.**
>
> **It also catches a second, worse failure mode that has occurred twice this week:** a routing script dies partway through (a text anchor no longer matches), the failing step is fixed and re-run, and **items earlier in the same script are silently never applied.** The CSV's `target_docs` column is audited and passes; the Routing prose is not, so the loss is invisible.
>
> **What to build.** Add a check to `tools/verify_batch.py` — it already takes `--base <ref>`, computes changed files, and accumulates problems; follow that structure and reporting style exactly.
>
> For each **changed** file matching `_Sources/YT_*.md`:
> 1. Read its frontmatter `video_id:`.
> 2. Extract the `## Routing` section (from that heading to the next `## ` or end of file).
> 3. Find every wiki link `[[target|label]]` or `[[target]]` in it. **Normalise path separators** — `glob` returns backslashes on Windows and the links use forward slashes; a naive comparison produces ~45 false positives, which is how the first hand-run audit misread the situation.
> 4. **Skip** links whose target resolves under `_Sources/`, `_Inbox/`, `_Archive/`, or ends `.txt`.
> 5. For every remaining link that resolves to a real `.md`, **that page must contain the literal string `YT_<video_id>_`.** If it does not, report a problem naming the note, the page, and the video id.
>
> **The contract this establishes, and you must enforce it rather than soften it: every wiki link inside a `## Routing` section is a CLAIM that the named page carries this source's content.** Cross-references, "see also" and "compare" links belong in the note's body, not in Routing.
>
> **Therefore also normalise the existing notes this flags.** Run the check across all of `_Sources/`, and for each note where a Routing link is a cross-reference rather than a claim, **move that link out of the Routing section** into the body or a `## See also` line. **Do not** add spurious citations to wiki pages to make the check pass — that would be fabricating provenance. If a Routing entry names a page whose content genuinely moved (the Moscow benchmark material moved to `11_Budget_and_Planning/analysis/Moscow_Per_Square_Metre_Benchmarks.md` in a page split; two notes still point at `Budget_Tiers_Cheap_Optimal_Premium.md`), **correct the Routing text to name where it actually is.**
>
> ---
>
> ### Task 2 — Archive `covers_also` transcripts in `tools/youtube/archive_transcripts.py`
>
> **The defect it exists to catch.** The repo groups several videos under one source note via a frontmatter `covers_also:` list, with their transcripts recorded as `transcript_file_pt2:`, `transcript_file_pt3:` and so on. **`archive_transcripts.py` matches transcripts to notes by `video_id`, so a `covers_also` transcript matches no note and is skipped** — it must currently be moved and renamed **by hand**, and its `_pt*` path typed into the note by hand.
>
> **Scale, measured today: 33 grouped notes carrying 50 `transcript_file_pt*` paths.** Every one is a chance to mistype a hash. In the 2026-09-14..16 batches alone the author hand-corrected guessed hashes at least six times, and shipped one note whose `_pt*` paths were pure placeholders.
>
> **What to build.** Extend `tools/youtube/archive_transcripts.py`:
> 1. After its existing per-note pass, build a map of `covers_also` ids → owning note, by reading each note's frontmatter.
> 2. For each remaining inbox transcript whose `.meta.json` `video_id` appears in that map, move it and its sidecar to `_Archive/processed_sources/` using the **same naming rule the tool already uses** — `<inbox date prefix>_<owning note's slug>_<hash8>` — **disambiguated per part**, e.g. `..._pt2_<hash8>.txt`.
> 3. **Write the resulting relative path into the owning note's `transcript_file_ptN:` line**, creating the line if absent, by the same whole-line regex rewrite the tool already uses for `transcript_file:`. Read that function's comment before changing anything near it: a previous version used substring replacement and silently produced a corrupted nested path.
> 4. **Order `ptN` by the order the ids appear in `covers_also:`**, so the numbering is stable and reproducible rather than filesystem-order.
> 5. Be **idempotent**: running twice must not move an already-archived file, renumber anything, or rewrite a correct line.
> 6. **Never modify an archived transcript's bytes.** `AGENTS.md` freezes them; only the `.meta.json` sidecar may gain additive provenance fields, and this task needs none.
>
> ---
>
> ### Required for both, per standing rule 10
>
> **`00_Master/Validator_Design_Discipline.md` states that a gate nobody has watched fail is not a gate.** So for each task, add a **self-test that seeds real defects and asserts each is rejected**, following the existing pattern in `scripts/verify_batch_selftest.py` (a `CASES` table of labelled fixtures, each with its expected verdict) and `scripts/dxf_closure_selftest.py`.
>
> **Minimum seeds — the checker must reject every one, and you must have watched it do so:**
>
> *Routing gate:* a note whose Routing names a page that does not cite it; a note whose Routing names a page that does (must PASS); a link written with backslashes (must still resolve, not false-positive); a link to a `_Sources/` note (must be ignored); a Routing section that is absent entirely (must not crash); a note whose `video_id` is missing (must report, not crash).
>
> *`covers_also` archiving:* a grouped note whose `pt2` transcript sits in the inbox (must be moved and the line written); the same run repeated (must be a no-op); a `covers_also` id with no transcript present (must be reported, not silently skipped); a note whose `transcript_file_pt2:` line is absent (must be created); two `covers_also` ids (must number pt2, pt3 in `covers_also` order).
>
> **Also run `scripts/verify_batch_selftest.py` after touching `verify_batch.py`** — `AGENTS.md` says it exists to guard that tool against over-suppression, and a new check must not weaken the existing ones.
>
> ### Practical notes
>
> - **Python is `.venv\Scripts\python.exe`.** `.venv-ifc314` is a separate IFC/Blender runtime — not for this task.
> - **Do not put Cyrillic or mixed quotes in a bash heredoc**; this repo's own notes record that failing repeatedly. Write a script to a file and run it.
> - **Do not use `%`-style string formatting on any text extracted from the vault.** `"10% of"`, `"+60%"` and `"30% dearer"` all parse as format specifiers and have broken three scripts this week. Use concatenation.
> - **Branch, commit, merge `--no-ff` to main, delete the branch local and remote** — standing rule 12.
> - Run `tools/verify_batch.py --base HEAD` and `tools/check_page_sizes.py` before committing.
> - **Do not change any wiki content to make a gate pass.** If the gate finds a real gap, report it; the owner decides. The single exception is Task 1's explicit instruction to correct Routing text that names the wrong page after a split.

---

## §2 — How this will be verified

**Claude Code will check the following, and will not take a self-report for any of them.**

| # | Check | Method |
| :--- | :--- | :--- |
| 1 | **The Routing gate actually fails on a real defect** | Seed a note whose Routing names a page that does not cite it; run `verify_batch.py --base HEAD`; require non-zero exit and the note named. **A gate that only passes is not evidence.** |
| 2 | **It does not false-positive** | Run across the whole of `_Sources/` (1,145 notes) and review every hit. **Backslash-vs-forward-slash normalisation is the specific trap** — the first hand-run audit produced ~45 hits of which ~24 were this bug and 2 were real. |
| 3 | **No fabricated provenance** | `git diff` every wiki page touched. A page gaining a `[source: …]` link for content it does not actually carry is a worse defect than the one being fixed, and fails this brief. |
| 4 | **`covers_also` archiving works end-to-end** | Take a grouped note, put its `pt` transcript back in `_Inbox/transcripts/`, run the tool, and require: file moved, name matching the existing convention, `transcript_file_pt2:` rewritten, path resolving on disk. |
| 5 | **Idempotency** | Run it twice. The second run must move nothing and rewrite nothing. `git status` clean after the second. |
| 6 | **Archived bytes unchanged** | `sha256` every file under `_Archive/processed_sources/` before and after. Any changed hash on a `.txt` fails the brief outright. |
| 7 | **Both self-tests exist and have been watched failing** | Run each; then break the checker deliberately and require the self-test to fail. A self-test that cannot fail is the failure class `Validator_Design_Discipline.md` names first. |
| 8 | **`verify_batch_selftest.py` still passes** | Directly, per `AGENTS.md`. |
| 9 | **The 50 existing `pt` paths still resolve** | Re-run the transcript-path audit across all notes: zero missing. |
| 10 | **Gates green** | `verify_batch.py`, `check_page_sizes.py`, `check_wall_junctions.py`, `check_dxf_closure.py` — the last two because they must be untouched by this work, and confirming that is cheap. |

---

## §3 — Verified repo context, 2026-09-16 (checked, not recalled)

| Fact | Value |
| :--- | :--- |
| Source notes | **1,145** (`_Sources/YT_*.md`) |
| CSV rows | **1,318** — 1,208 archived, 86 skipped, 9 duplicate_skipped, 14 integrated, 1 processed |
| Archived transcripts | **1,156** |
| Ledger ids | **1,342**, all unique |
| **Grouped notes (`covers_also:`)** | **33** |
| **`transcript_file_pt*` paths needing manual archiving today** | **50** |
| `tools/verify_batch.py` | 798 lines; `--base` defaults to `origin/main`; per-file checks returning problem lists |
| `scripts/verify_batch_selftest.py` | 197 lines; `CASES` table of labelled fixtures with expected verdicts |
| `tools/youtube/archive_transcripts.py` | Matches transcript → note by `video_id` from `.meta.json`; derives the archive name as `<date>_<note slug>_<hash8>`; rewrites `transcript_file:` by whole-line regex, with a comment explaining why substring replacement was abandoned |
| Audit result that prompted this | 2 sources cited nowhere; ~24 Routing entries naming a page that does not cite them; ~45 raw hits before path normalisation |

**Both genuine misses were fixed by hand on 2026-09-16** (commit *"Two sources cited nowhere in the wiki"*) — `14_Furniture/analysis/Upholstery_Fabric_Selection.md` gained `[source:]` links and a Source Notes block. **Antigravity should not redo that; it is the worked example of what the gate is for.**

---

## §4 — Proposed and deliberately NOT delegated in this round

Recorded so they survive the conversation. All three are cheap and all three have this week's evidence behind them.

1. **A probe-before-fetch preflight.** Normalise and dedup ids (one request sent the same id twice), reject malformed ones (a 10-character id; a URL with no id at all), and report duration, available caption languages, original language, and a likely-silent flag. **Would have prevented**: forcing `--languages ru` on English sources (standing rule 1 means *original* language, which was misread as "always ru"); fetching four videos with no caption track in any language; and fetching two that turned out to be music with no speech.
2. **Unambiguous exit codes in the fetch script.** `argparse` exits **2** on a usage error, and the script uses **2** for rate-limited — so a malformed id reads as an IP block and stops a whole run. Separate them. **And a companion habit for the skill: capture `$?` before any pipe** — a circuit breaker silently never fired because `$?` was read after `| tail -3`.
3. **Ban `%`-style formatting on extracted text** in the intake skill, alongside the existing heredoc warning.

**A fourth, softer one worth considering later:** make the **coverage grep before triage** a named step in `renovation-knowledge-intake/SKILL.md`. It is what found transformer tables at zero files against wall beds at 28, and it is why one channel triage took 9 of 169 videos instead of 40. It currently happens only when the operator thinks of it.
