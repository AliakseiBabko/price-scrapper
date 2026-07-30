import sys
import json
import os
import hashlib
import csv
import re
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)
    try:
        transcript = transcript_list.find_transcript(['en', 'ru'])
    except Exception:
        # Fallback to generated if manually created doesn't exist
        transcript = transcript_list.find_generated_transcript(['ru', 'en'])
    text = " ".join([entry.text for entry in transcript.fetch()])
    return text

def sanitize_slug(slug):
    # Remove invalid Windows filename characters and limit length
    slug = re.sub(r'[\\/*?:"<>|]', "", slug)
    return slug.strip().replace(" ", "_")[:50]

def is_duplicate(file_hash):
    csv_file = os.path.join("00_Master", "processed_sources.csv")
    if not os.path.exists(csv_file):
        return False
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("source_hash") == file_hash:
                    return True
    except Exception as e:
        print(f"Error: Could not check duplicates in CSV: {e}", file=sys.stderr)
        sys.exit(1)
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_youtube_transcript.py <youtube_url> [slug_name]")
        sys.exit(1)
        
    url = sys.argv[1]
    raw_slug = sys.argv[2] if len(sys.argv) > 2 else "youtube_video"
    slug = sanitize_slug(raw_slug)
    if not slug:
        slug = "youtube_video"
    
    video_id = None
    if "v=" in url:
        video_id = url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[1].split("?")[0]
        
    if not video_id:
        print("Could not extract video ID from URL", file=sys.stderr)
        sys.exit(1)
        
    try:
        text = get_transcript(video_id)
    except Exception as e:
        print(f"Error fetching transcript: {e}", file=sys.stderr)
        sys.exit(1)
        
    if text:
        # Hash the text
        sha256_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        
        if is_duplicate(sha256_hash):
            print(f"Error: Transcript already processed! (Duplicate hash: {sha256_hash})", file=sys.stderr)
            sys.exit(1)
            
        hash8 = sha256_hash[:8]
        
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"{date_str}_{slug}_{hash8}.txt"
        out_dir = os.path.join("00_Inbox", "transcripts")
        os.makedirs(out_dir, exist_ok=True)
        
        file_path = os.path.join(out_dir, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
            
        print(f"Transcript saved to: {file_path}")
        print(f"SHA-256 Hash: {sha256_hash}")
    else:
        print("Transcript was empty.", file=sys.stderr)
        sys.exit(1)
