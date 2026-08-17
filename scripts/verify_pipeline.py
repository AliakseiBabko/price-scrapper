import os
import csv

def verify_pipeline():
    inbox = r"_Inbox\transcripts"
    archive = r"_Archive\processed_sources"
    csv_file = r"00_Master\processed_sources.csv"
    skill_file = r".agents\skills\youtube-to-obsidian\SKILL.md"
    raw_dir = r"11_Budget_and_Planning\raw_transcripts"

    issues = []

    # 1. Folders exist
    if not os.path.exists(inbox): issues.append(f"Missing folder: {inbox}")
    if not os.path.exists(archive): issues.append(f"Missing folder: {archive}")

    # 2. Cleanup happened
    if os.path.exists(raw_dir): issues.append(f"Folder should not exist: {raw_dir}")

    # 3. CSV header
    expected_header = ["run_id", "date", "source_type", "source_url", "source_title", "source_hash", "topic_tags", "scope", "target_docs", "status", "notes"]
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header != expected_header:
                issues.append(f"CSV header mismatch. Found: {header}")
    except Exception as e:
        issues.append(f"Error reading {csv_file}: {e}")

    # 4. Skill mentions important keywords
    try:
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if "_Inbox\\transcripts" not in content and "_Inbox/transcripts" not in content:
                issues.append("SKILL.md does not mention _Inbox/transcripts")
            if "_Archive\\processed_sources" not in content and "_Archive/processed_sources" not in content:
                issues.append("SKILL.md does not mention _Archive/processed_sources")
            if "scope" not in content.lower():
                issues.append("SKILL.md does not mention 'scope'")
    except Exception as e:
        issues.append(f"Error reading {skill_file}: {e}")

    if not issues:
        print("Verification PASSED: Pipeline is configured correctly.")
    else:
        print("Verification FAILED with the following issues:")
        for issue in issues:
            print(f" - {issue}")

if __name__ == "__main__":
    verify_pipeline()
