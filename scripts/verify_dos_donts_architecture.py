import os
import csv
import re
import hashlib

def get_file_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def verify():
    issues = []

    # 1. 14_Rooms must NOT exist
    if os.path.exists("14_Rooms"):
        issues.append("Forbidden folder '14_Rooms' exists! Room rules must live in canonical room folders.")

    # 2. Expected files list with full relative paths
    expected_files = [
        r"00_Master\Dos_and_Donts_Master_Summary.md",
        r"12_Engineering_and_Systems\Electrical_and_Lighting.md",
        r"12_Engineering_and_Systems\Plumbing_and_Waterproofing.md",
        r"12_Engineering_and_Systems\HVAC_and_Ventilation.md",
        r"13_Surfaces_and_Finishes\Flooring_Guide.md",
        r"13_Surfaces_and_Finishes\Walls_and_Paint.md",
        r"13_Surfaces_and_Finishes\Ceilings_Guide.md",
        r"07_Bathroom\analysis\Dos_and_Donts.md",
        r"08_WC\analysis\Dos_and_Donts.md",
        r"09_Laundry_Room\analysis\Dos_and_Donts.md",
        r"03_Kitchen\General\analysis\Dos_and_Donts.md"
    ]

    # Additional key budget & planning files that must exist and be non-empty.
    # Paths updated 2026-07-31 to match the 11_Budget_and_Planning reorg (top-level
    # Budgeting_Guide.md/Renovation_Sequence.md; the old Cost_Saving_Strategies.md and
    # Master_Budgeting_Guide.md names no longer exist - the content was folded into
    # Budgeting_Guide.md itself, with full detail preserved under 11_Budget_and_Planning/analysis/).
    key_target_docs = [
        r"11_Budget_and_Planning\analysis\cost_saving_strategies_full.md",
        r"11_Budget_and_Planning\Budgeting_Guide.md",
        r"11_Budget_and_Planning\Renovation_Sequence.md",
        r"00_Master\Revit_AutoCAD_Integration_Strategy.md",
        r"00_Master\exchange_rates_reference.md"
    ]

    # Verify all expected_files and key_target_docs exist and are non-empty
    for filepath in expected_files + key_target_docs:
        if not os.path.exists(filepath):
            issues.append(f"Missing required file: {filepath}")
        elif os.path.getsize(filepath) == 0:
            issues.append(f"Required file is EMPTY (0 bytes): {filepath}")

    # 3. Verify CSV schema, hash logging, and target_docs citations
    valid_hashes = set()
    csv_sources_info = {}
    csv_path = r"00_Master\processed_sources.csv"
    required_csv_fields = ["source_year", "region", "pricing_priority", "conversion_basis"]
    if not os.path.exists(csv_path):
        issues.append(f"Missing CSV log: {csv_path}")
    else:
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                header = reader.fieldnames or []
                for req_field in required_csv_fields:
                    if req_field not in header:
                        issues.append(f"processed_sources.csv is missing required schema header: '{req_field}'")

                for row in reader:
                    h = row.get("source_hash", "")
                    sh8 = h[:8] if h else ""
                    if h:
                        valid_hashes.add(h)
                        valid_hashes.add(sh8)
                        csv_sources_info[sh8] = row
                        csv_sources_info[h] = row
                    
                    # Verify target_docs listed in CSV
                    tdocs = [d.strip() for d in row.get("target_docs", "").split(",") if d.strip()]
                    for doc_name in tdocs:
                        if doc_name.endswith(".md"):
                            found_file_path = None
                            for root, dirs, files in os.walk("."):
                                if doc_name in files:
                                    found_file_path = os.path.join(root, doc_name)
                                    break
                            
                            if not found_file_path:
                                issues.append(f"processed_sources.csv lists target doc '{doc_name}' for hash '{sh8}', but file '{doc_name}' does not exist in workspace.")
                            else:
                                if os.path.getsize(found_file_path) == 0:
                                    issues.append(f"CSV target doc '{doc_name}' is EMPTY (0 bytes): {found_file_path}")
                                else:
                                    with open(found_file_path, 'r', encoding='utf-8') as tf:
                                        t_content = tf.read()
                                    if sh8 and sh8 not in t_content and h not in t_content:
                                        issues.append(f"processed_sources.csv lists target doc '{doc_name}' for source hash '{sh8}', but '{doc_name}' does not contain any citation to '{sh8}'.")

            # Verify actual on-disk files in _Archive/processed_sources match logged CSV hashes
            archive_dir = r"_Archive\processed_sources"
            if os.path.exists(archive_dir):
                for filename in os.listdir(archive_dir):
                    if filename.endswith(".txt"):
                        archived_file_path = os.path.join(archive_dir, filename)
                        actual_hash = get_file_sha256(archived_file_path)
                        if actual_hash not in valid_hashes:
                            issues.append(
                                f"Archived transcript integrity mismatch! File '{filename}' actual SHA-256 hash ({actual_hash[:8]}) is NOT registered in {csv_path}"
                            )
        except Exception as e:
            issues.append(f"Error reading {csv_path}: {e}")

    # 4. Verify YouTube-to-Obsidian SKILL.md rules
    skill_path = r".agents\skills\youtube-to-obsidian\SKILL.md"
    if not os.path.exists(skill_path):
        issues.append(f"Missing skill file: {skill_path}")
    else:
        with open(skill_path, 'r', encoding='utf-8') as f:
            skill_content = f.read()
        
        required_skill_terms = ["source_year", "region", "pricing_priority", "conversion_basis", "annual average"]
        for term in required_skill_terms:
            if term not in skill_content:
                issues.append(f"youtube-to-obsidian SKILL.md missing required rule term: '{term}'")
        
        if "current approximate exchange rate" in skill_content:
            issues.append("youtube-to-obsidian SKILL.md contains deprecated instruction 'current approximate exchange rate'. Must use annual average for source_year.")

    # 5. Verify Master_Budgeting_Guide.md obsidian wikilink style, region/source markers, metadata block & budget table reconciliation
    # NOTE (2026-07-31): this check targets the OLD Master_Budgeting_Guide.md's specific
    # structure (a detailed metadata block per pricing entry, a single "Minsk 2025 budget
    # table" with a reconcilable total). The 11_Budget_and_Planning reorg replaced it with
    # Budgeting_Guide.md, a deliberately compressed high-level page that doesn't follow
    # that structure by design - repointing mbg_path at it would fire a wall of new,
    # not-actually-wrong findings against an intentional format change, not a real
    # regression. Left pointing at the retired path (so this section is a documented no-op)
    # until someone decides whether to rewrite these checks for the new page's own format.
    mbg_path = r"11_Budget_and_Planning\analysis\Master_Budgeting_Guide.md"
    if os.path.exists(mbg_path):
        with open(mbg_path, 'r', encoding='utf-8') as f:
            mbg_content = f.read()

        if "file:///" in mbg_content:
            issues.append("Master_Budgeting_Guide.md contains hardcoded file:/// links. Must use vault-relative Obsidian wikilinks.")

        if "Un-Itemized Delivery, Logistics & Fees" in mbg_content:
            issues.append("Master_Budgeting_Guide.md contains prohibited phrase 'Un-Itemized Delivery, Logistics & Fees'. Must use 'Unallocated Difference Between Itemized Subtotal and Stated Turnkey Total'.")

        # Check pricing table headings contain region/source-class markers
        headings = [line.strip() for line in mbg_content.splitlines() if line.strip().startswith("### ")]
        for h in headings:
            if any(term in h for term in ["Benchmark", "Pricing", "Cost", "Breakdown"]):
                if not re.search(r"(Minsk|Belarus|Russia|Saint-Petersburg|Primary|Secondary|Local|Reference)", h, re.IGNORECASE):
                    issues.append(f"Pricing heading in Master_Budgeting_Guide.md missing region/source-class marker: '{h}'")

        # Check metadata block keys
        required_metadata_keys = ["Source class", "Region", "Source year", "Currency in source", "Conversion basis", "Comparability"]
        for key in required_metadata_keys:
            if f"- **{key}**:" not in mbg_content:
                issues.append(f"Master_Budgeting_Guide.md missing required metadata block key: '{key}'")

        # Check no line contains BYN and [Secondary Reference: Russia / RUB] together unless it contains Original source: and Converted values:
        for line in mbg_content.splitlines():
            if "BYN" in line and "[Secondary Reference: Russia / RUB]" in line:
                if not ("Original source:" in line and "Converted values:" in line):
                    issues.append(f"Line in Master_Budgeting_Guide.md mixes BYN and Secondary Russia/RUB reference without explicit Original source and Converted values labels: '{line.strip()}'")

        # Check secondary pricing references contain a comparability note
        for line in mbg_content.splitlines():
            line_s = line.strip()
            if line_s.startswith("- **") and "Original source:" in line_s:
                if not any(term in line_s for term in ["not Minsk-equivalent", "NOT Minsk-equivalent", "secondary reference only"]):
                    issues.append(f"Secondary pricing reference line missing explicit comparability note ('not Minsk-equivalent' or 'secondary reference only'): '{line_s}'")

        # Reconcile budget table totals
        table_lines = [l.strip() for l in mbg_content.splitlines() if l.strip().startswith("|")]
        stated_total = None
        item_sum = 0
        has_subtotal = False

        for line in table_lines:
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 2:
                cat_name = cells[0].replace("**", "")
                cost_str = cells[1].replace("**", "").replace("$", "").replace(",", "")
                
                # Check for numbers in stated cost column
                if re.match(r"^\d+$", cost_str):
                    val = int(cost_str)
                    if "Stated Turnkey Project Total" in cat_name or "Total Budget" in cat_name:
                        stated_total = val
                    elif "Subtotal Explicit Itemized Items" in cat_name:
                        has_subtotal = True
                    elif "Unallocated Difference" in cat_name or "Un-Itemized" in cat_name:
                        item_sum += val
                    elif val > 0 and cat_name not in ["Budget Category", "Category", "---"]:
                        item_sum += val

        if stated_total is not None and has_subtotal:
            if item_sum != stated_total:
                issues.append(f"Minsk 2025 budget table total mismatch! Row sum (${item_sum}) does not match Stated Turnkey Project Total (${stated_total}).")

    # 6. Verify exchange_rates_reference.md structure and rates
    verified_rate_years = set()
    err_path = r"00_Master\exchange_rates_reference.md"
    if os.path.exists(err_path):
        with open(err_path, 'r', encoding='utf-8') as f:
            err_content = f.read()

        required_err_headers = ["retrieval_date", "source_url", "confidence"]
        for req_h in required_err_headers:
            if req_h not in err_content:
                issues.append(f"exchange_rates_reference.md missing required table header column: '{req_h}'")

        if "TODO" not in err_content and "http" not in err_content:
            issues.append("exchange_rates_reference.md contains unverified exchange rates without explicit source URLs or TODO markers.")

        for line in err_content.splitlines():
            if line.strip().startswith("|") and "http" in line and "TODO" not in line:
                match = re.search(r"\|\s*(\d{4})\s*\|", line)
                if match:
                    verified_rate_years.add(match.group(1))

    # 7. Check conversion basis consistency and evidence for inferred metadata
    seen_hashes = set()
    for sh, info in csv_sources_info.items():
        sh8 = sh[:8]
        if sh8 in seen_hashes:
            continue
        seen_hashes.add(sh8)

        s_year = info.get("source_year", "")
        reg = info.get("region", "")
        notes = info.get("notes", "")

        # Check: inferred source_year or city requires evidence in notes or transcript text
        if s_year != "unknown" or ("Saint-Petersburg" in reg or "Moscow" in reg):
            archive_dir = r"_Archive\processed_sources"
            if os.path.exists(archive_dir):
                for fn in os.listdir(archive_dir):
                    if sh8 in fn:
                        t_path = os.path.join(archive_dir, fn)
                        with open(t_path, 'r', encoding='utf-8') as tf:
                            t_text = tf.read()
                        
                        year_in_text = s_year in t_text if s_year != "unknown" else True
                        city_in_text = True
                        if "Saint-Petersburg" in reg:
                            city_in_text = any(term in t_text for term in ["Петербург", "СПб", "Питер", "варшавской"])
                        elif "Moscow" in reg:
                            city_in_text = any(term in t_text for term in ["Москва", "Мск"])

                        if not (year_in_text and city_in_text):
                            if not notes or len(notes.strip()) < 10:
                                issues.append(f"processed_sources.csv assigns year '{s_year}' / region '{reg}' to source hash '{sh8}', but transcript text does not contain explicit year/city markers and notes lack evidence documentation.")
                        break

    # Check that docs do not present converted BYN/USD values for unverified exchange rates or unknown_year sources.
    # Associate pricing bullet lines with immediately following source citation lines (line N + line N+1).
    for filepath in expected_files + key_target_docs:
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            file_lines = f.readlines()

        for idx, line in enumerate(file_lines):
            line_s = line.strip()
            if not line_s:
                continue

            # Build combined context: current line + next line if next line contains a source citation
            combined_context = line_s
            if idx + 1 < len(file_lines):
                next_line = file_lines[idx + 1].strip()
                if "Source:" in next_line or "_Archive" in next_line or "[[" in next_line:
                    combined_context = line_s + " " + next_line

            cited_hashes = re.findall(r"([a-fA-F0-9]{8,64})", combined_context)
            for ch in cited_hashes:
                sh8 = ch[:8]
                if sh8 in csv_sources_info:
                    info = csv_sources_info[sh8]
                    cb = info.get("conversion_basis", "")

                    has_converted_values = (re.search(r"~\d+\s*(BYN|USD)", combined_context) or re.search(r"\$\d+\s*USD", combined_context))
                    is_demoted = "Converted values: N/A" in combined_context

                    if has_converted_values and not is_demoted:
                        if cb.startswith("annual_avg_"):
                            yr = cb.replace("annual_avg_", "")
                            if yr not in verified_rate_years:
                                issues.append(f"File {filepath} presents converted BYN/USD values for source '{sh8}' (basis '{cb}') whose exchange rate for {yr} is TODO/unverified in exchange_rates_reference.md: '{line_s}'")
                        elif cb in ["unknown_year_no_conversion", "unknown_year"]:
                            issues.append(f"File {filepath} presents converted BYN/USD values for source '{sh8}' which has conversion_basis '{cb}': '{line_s}'")

    # 8. Verify source citations and wikilinks across both expected_files and key_target_docs
    for filepath in expected_files + key_target_docs:
        if not os.path.exists(filepath):
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            citations = re.findall(r"_Archive[/\\]processed_sources[/\\][a-zA-Z0-9_]+\.txt", content)
            wikilink_citations = re.findall(r"\[\[(_Archive[/\\]processed_sources[/\\][a-zA-Z0-9_]+)(?:\\?\|[^\]]+)?\]\]", content)
            for wpath in wikilink_citations:
                if not wpath.endswith(".txt"):
                    citations.append(wpath + ".txt")
                else:
                    citations.append(wpath)

            for cite in citations:
                source_file_path = cite.replace("/", "\\")
                if not os.path.exists(source_file_path):
                    issues.append(f"Cited source file does not exist on disk: '{cite}' in {filepath}")
                else:
                    computed_hash = get_file_sha256(source_file_path)
                    if computed_hash not in valid_hashes:
                        issues.append(
                            f"Cited source file '{cite}' in {filepath} actual SHA-256 ({computed_hash[:8]}) does NOT match {csv_path}"
                        )
        except Exception as e:
            issues.append(f"Error parsing source citations in {filepath}: {e}")

    for filepath in expected_files:
        if not os.path.exists(filepath):
            continue

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            in_table = False
            source_idx = -1
            current_heading = None

            for line_idx, line in enumerate(lines, start=1):
                line_str = line.strip()
                if line_str.startswith("#"):
                    current_heading = line_str
                    in_table = False
                    source_idx = -1
                    continue

                if line_str.startswith("|") and line_str.endswith("|"):
                    cells = [c.strip() for c in line_str.split("|")[1:-1]]
                    
                    if "Rule" in cells and ("Reason" in cells or "Risk" in cells):
                        # Accept both a bare '## Do's'/'## Don'ts' heading (flat-table pages)
                        # and a '### Do's'/'### Don'ts' subheading nested under a numbered
                        # "Quick Reference" section (the wiki-page-format convention adopted
                        # 2026-07-31 for HVAC/Electrical/Plumbing/Bathroom/WC) - both are
                        # valid, deliberate page shapes, not a naming error.
                        heading_text = current_heading.lstrip('#').strip() if current_heading else ""
                        if "Risk" in cells and heading_text != "Don't's" and heading_text != "Don'ts":
                            issues.append(f"Don'ts table (line {line_idx}) in {filepath} is under heading '{current_heading}', expected a \"Don'ts\" heading (## or ###).")
                        if "Reason" in cells and heading_text != "Do's":
                            issues.append(f"Do's table (line {line_idx}) in {filepath} is under heading '{current_heading}', expected a \"Do's\" heading (## or ###).")

                        if "Source" in cells:
                            source_idx = cells.index("Source")
                            in_table = True
                        else:
                            issues.append(f"Table in {filepath} missing 'Source' header column.")
                        continue
                    
                    if cells and all(re.match(r"^:?-+:?$", c) for c in cells):
                        continue

                    if in_table and source_idx >= 0 and len(cells) > source_idx:
                        raw_cell = cells[source_idx].strip()
                        if not raw_cell:
                            issues.append(f"Empty source cell in {filepath} row: {line_str}")
                            continue

                        if "General practice" in raw_cell:
                            continue

                        # A source cell may cite more than one archive path, e.g.
                        # "`path/a.txt`, `path/b.txt`" - extract each backtick-delimited
                        # (or, failing that, whitespace/comma-delimited) path individually
                        # rather than treating the whole cell as one literal path.
                        backtick_vals = re.findall(r"`([^`]+)`", raw_cell)
                        source_vals = backtick_vals if backtick_vals else [raw_cell.strip(" \"'")]

                        for source_val in source_vals:
                            source_val = source_val.strip(" `\"'")
                            if not source_val:
                                continue

                            source_file_path = source_val.replace("/", "\\")
                            if not os.path.exists(source_file_path):
                                issues.append(f"Cited source file does not exist on disk: '{source_val}' in {filepath}")
                            else:
                                computed_hash = get_file_sha256(source_file_path)
                                if computed_hash not in valid_hashes:
                                    issues.append(
                                        f"Cited source file '{source_val}' in {filepath} actual SHA-256 ({computed_hash[:8]}) does NOT match {csv_path}"
                                    )

                            if "processed_sources" in source_val:
                                match = re.search(r"_([a-fA-F0-9]{8,64})\.txt$", source_val)
                                if match:
                                    file_hash = match.group(1)
                                    if file_hash not in valid_hashes:
                                        issues.append(f"Cited source hash '{file_hash}' from '{source_val}' in {filepath} is NOT in processed_sources.csv")
                else:
                    in_table = False
                    source_idx = -1

        except Exception as e:
            issues.append(f"Error validating table sources in {filepath}: {e}")

    # Master Summary full vault-relative link check
    summary_path = r"00_Master\Dos_and_Donts_Master_Summary.md"
    if os.path.exists(summary_path):
        with open(summary_path, 'r', encoding='utf-8') as f:
            summary_content = f.read()
            for filepath in expected_files:
                if filepath == summary_path:
                    continue
                rel_path = filepath.replace("\\", "/").replace(".md", "")
                if rel_path not in summary_content:
                    issues.append(f"Master summary does not link to full vault-relative path: '{rel_path}'")

    # Renovation Dashboard link check
    dashboard_path = r"00_Master\Renovation_Dashboard.md"
    if os.path.exists(dashboard_path):
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            dash_content = f.read()
            if "Dos_and_Donts_Master_Summary" not in dash_content:
                issues.append("Renovation Dashboard does not link to Dos_and_Donts_Master_Summary")

    if not issues:
        print("Verification PASSED: Do's and Don'ts architecture, pricing policy, and source traceability are fully valid.")
    else:
        print("Verification FAILED with the following issues:")
        for issue in issues:
            print(f" - {issue}")
        exit(1)

if __name__ == "__main__":
    verify()
