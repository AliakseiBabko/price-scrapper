import os
import csv
import re

def verify_pipeline():
    inbox = r"00_Inbox\cad"
    archive = r"90_Archive\homestyler_exports"
    csv_file = r"00_Master\cad_sources.csv"
    
    issues = []

    # 1. Folders exist
    if not os.path.exists(inbox): issues.append(f"Missing folder: {inbox}")
    if not os.path.exists(archive): issues.append(f"Missing folder: {archive}")

    # 2. CSV exists and header matches
    expected_header = ["source_id", "date", "source_type", "source_file", "source_hash", "origin", "units", "status", "revit_model", "target_views", "related_files", "notes"]
    if not os.path.exists(csv_file):
        issues.append(f"Missing CSV file: {csv_file}")
    else:
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                header = reader.fieldnames
                if header != expected_header:
                    issues.append(f"CSV header mismatch. Found: {header}")
                
                # Check rows
                for row in reader:
                    source_file = row.get("source_file", "")
                    if not os.path.exists(source_file):
                        issues.append(f"source_file does not exist: {source_file}")
                    
                    related_files = row.get("related_files", "")
                    if related_files:
                        for rel_file in related_files.split(";"):
                            if not os.path.exists(rel_file):
                                issues.append(f"related_file does not exist: {rel_file}")
                                
                    status = row.get("status", "")
                    valid_statuses = ["inbox", "linked", "imported", "archived", "skipped", "failed"]
                    if status not in valid_statuses:
                        issues.append(f"Invalid status: {status}")
                        
                    source_hash = row.get("source_hash", "")
                    if not re.match(r"^[a-fA-F0-9]{64}$", source_hash):
                        issues.append(f"Invalid source_hash: {source_hash}")
        except Exception as e:
            issues.append(f"Error reading {csv_file}: {e}")

    if not issues:
        print("Verification PASSED: CAD Pipeline is configured correctly.")
    else:
        print("Verification FAILED with the following issues:")
        for issue in issues:
            print(f" - {issue}")

if __name__ == "__main__":
    verify_pipeline()
