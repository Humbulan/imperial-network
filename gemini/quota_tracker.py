#!/usr/bin/env python3
"""
Gemini Quota Tracker for Imperial Network
Tracks usage against free tier limits: 100 images/day, 2 videos/day
"""
import json
import os
import sys
from datetime import datetime, date
from pathlib import Path

QUOTA_FILE = Path.home() / '.imperial_gemini_quota.json'

def load_quota():
    if QUOTA_FILE.exists():
        with open(QUOTA_FILE, 'r') as f:
            data = json.load(f)
            # Reset if new day
            if data.get('date') != str(date.today()):
                return {'date': str(date.today()), 'images': 0, 'videos': 0}
            return data
    return {'date': str(date.today()), 'images': 0, 'videos': 0}

def save_quota(quota):
    with open(QUOTA_FILE, 'w') as f:
        json.dump(quota, f, indent=2)

def check_quota():
    quota = load_quota()
    
    images_left = max(0, 100 - quota['images'])
    videos_left = max(0, 2 - quota['videos'])
    
    status = "GREEN"
    if quota['images'] >= 100 or quota['videos'] >= 2:
        status = "RED"
    elif quota['images'] >= 80 or quota['videos'] >= 1:
        status = "YELLOW"
    
    print("🏛️ IMPERIAL GEMINI QUOTA")
    print("=" * 50)
    print(f"📸 Images: {quota['images']}/100 used today")
    print(f"   Remaining: {images_left}")
    print(f"🎥 Videos: {quota['videos']}/2 used today")
    print(f"   Remaining: {videos_left}")
    print(f"💰 Cost Today: $0.00 (Free Tier)")
    print(f"📈 Status: {status}")
    
    return status

def increment_usage(media_type='images', count=1):
    quota = load_quota()
    quota[media_type] = quota.get(media_type, 0) + count
    save_quota(quota)
    print(f"✅ Recorded {count} {media_type} usage")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--increment':
        increment_usage(sys.argv[2] if len(sys.argv) > 2 else 'images')
    else:
        check_quota()
