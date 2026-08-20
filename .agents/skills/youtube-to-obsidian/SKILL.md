---
name: youtube-to-obsidian
description: "DEPRECATED 2026-08-04 - see .agents/skills/renovation-knowledge-intake/SKILL.md instead. Extracts a YouTube transcript and integrates its knowledge into the Obsidian Wikipedia (price-scrapper)."
---

> [!WARNING]
> **Deprecated 2026-08-04.** Use [[.agents/skills/renovation-knowledge-intake/SKILL.md|renovation-knowledge-intake]] instead, which delegates fetching to the shared `youtube-transcript-fetch` skill and synthesis to `tiered-knowledge-base` - the pipeline actually used for every playlist batch processed in this repo since 2026-07-31 (electrical/lighting playlist, general renovation-tips playlist). This file is kept for reference and is not actively maintained; its documented CSV schema/status vocabulary has been superseded by the canonical copy in `renovation-knowledge-intake/SKILL.md` (which additionally documents `duplicate_skipped` and the pre-fetch duplicate-check requirement, missing here).
>
> `scripts/get_youtube_transcript.py` itself is **not** removed or altered by this deprecation - it remains available as a manual/legacy fallback (e.g. for a single one-off video, or if the shared skills aren't available in a given environment) as long as something still references it. If nothing does after a future audit, it can be removed along with this file.

# YouTube to Obsidian Knowledge Ingestion (deprecated - see notice above)

**Purpose**: Automate the process of extracting text from a YouTube video and updating the Obsidian knowledge base (`price-scrapper`).

## Workflow Steps

1. **Extract Transcript**:
   When the user provides a YouTube link, navigate to `c:\Users\User\Documents\price-scrapper\` and run the Python script to extract the transcript text:
   ```bash
   .venv\Scripts\python.exe scripts\get_youtube_transcript.py "<youtube_link>" "<slug_name>"
   ```
   *Note: Use a short slug of the title for `<slug_name>`. The script will extract the transcript, hash it, and save it in `_Inbox/transcripts/YYYYMMDD_<slug_name>_<hash8>.txt`. If the script detects that the generated hash already exists in `00_Master/processed_sources.csv`, it will abort execution to prevent processing a duplicate source. If this happens, inform the user that the source has already been processed.*

2. **Analyze and Summarize**:
   Read the transcript. Summarize the key points related to the renovation project (e.g., floors, ceilings, walls, budgeting, tips, warnings).

3. **Year-Aware Price Conversion & Regional Policy**:
   - Preserve original currencies (e.g., RUB, USD, BYN) as the source currency to maintain context.
   - Convert historical prices ONLY using the annual average exchange rate for the `source_year`, never current spot rates.
   - Source year priority: (1) Explicit year mentioned in title/content (e.g. "2025"); (2) Verified YouTube publish date year; (3) `unknown` if neither is reliable (do not present converted values as directly comparable).
   - Local Minsk/Belarus pricing is primary. Russian/RUB prices must be labeled as secondary "currency-normalized reference", not Minsk-equivalent pricing.

4. **Update Obsidian Vault**:
   Based on the topics covered in the video, classify the content by scope (e.g., Master Planning, Room-Specific) and update or create markdown files in the relevant folders inside `c:\Users\User\Documents\price-scrapper\`:
   - `00_Master/`: For overall concepts, general rules, and master plans.
   - `11_Budget_and_Planning/`: For project budgeting rules, how to plan steps, estimation techniques.
   - Specific rooms (`07_Bathroom/`, `08_WC/`, `09_Laundry_Room/`, `03_Kitchen/`, etc.): For room-specific materials or advice.

5. **Log Processing**:
   Add a new row to `00_Master\processed_sources.csv` to track this source.
   - **Schema**: `run_id,date,source_type,source_url,source_title,source_hash,source_year,region,pricing_priority,conversion_basis,topic_tags,scope,target_docs,status,notes`
   - **Status**: see the canonical, up-to-date vocabulary in `renovation-knowledge-intake/SKILL.md`'s "CSV schema and status vocabulary" section (this file's own copy is stale as of the 2026-08-04 deprecation above - it's missing `duplicate_skipped`, now a real status in this CSV).

6. **Archive Transcript**:
   Move the transcript file from `_Inbox\transcripts\` to `_Archive\processed_sources\`.

7. **Report to User**:
   Provide the user with a quick summary of the video and links to the Obsidian files that were updated or created. Mention how the concepts could map to the 3D Homestyler plan (e.g. suggesting an ID tag).
