#!/usr/bin/env python3
"""
Engagement Data Collector — Pulls engagement data from all platforms.

Usage:
    python scripts/engagement-collector.py --month 2026-09
    python scripts/engagement-collector.py --month 2026-09 --output engagement.json

Collects:
- Post-level metrics (likes, comments, shares, saves, clicks)
- Follower growth
- Top performing posts
- Worst performing posts

In production, this uses official platform APIs:
- Instagram Graph API
- Facebook Graph API
- LinkedIn API
- TikTok Research API
- X API v2
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def collect_instagram_data(ig_user_id: str, access_token: str) -> list:
    """Collect Instagram media insights."""
    import requests
    
    url = f"https://graph.facebook.com/v21.0/{ig_user_id}/media"
    params = {
        "fields": "id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count",
        "access_token": access_token,
        "limit": 50,
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"❌ Instagram API error: {response.status_code}")
        return []
    
    data = response.json().get("data", [])
    
    posts = []
    for item in data:
        posts.append({
            "platform": "instagram",
            "post_id": item.get("id"),
            "title": item.get("caption", "")[:100],
            "content_type": item.get("media_type", "unknown").lower(),
            "posted_at": item.get("timestamp"),
            "posted_hour": datetime.fromisoformat(item.get("timestamp", "2026-01-01T00:00:00+00:00")).hour if item.get("timestamp") else 0,
            "likes": item.get("like_count", 0),
            "comments": item.get("comments_count", 0),
            "shares": 0,
            "saves": 0,
            "clicks": 0,
            "followers": 0,
            "url": item.get("permalink", ""),
        })
    
    return posts


def collect_facebook_data(page_id: str, access_token: str) -> list:
    """Collect Facebook page post insights."""
    import requests
    
    url = f"https://graph.facebook.com/v21.0/{page_id}/posts"
    params = {
        "fields": "id,message,created_time,likes.summary(true),comments.summary(true),shares",
        "access_token": access_token,
        "limit": 50,
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"❌ Facebook API error: {response.status_code}")
        return []
    
    data = response.json().get("data", [])
    
    posts = []
    for item in data:
        posts.append({
            "platform": "facebook",
            "post_id": item.get("id"),
            "title": item.get("message", "")[:100],
            "content_type": "post",
            "posted_at": item.get("created_time"),
            "posted_hour": datetime.fromisoformat(item.get("created_time", "2026-01-01T00:00:00+00:00")).hour if item.get("created_time") else 0,
            "likes": item.get("likes", {}).get("summary", {}).get("total_count", 0),
            "comments": item.get("comments", {}).get("summary", {}).get("total_count", 0),
            "shares": item.get("shares", {}).get("count", 0),
            "saves": 0,
            "clicks": 0,
            "followers": 0,
        })
    
    return posts


def collect_linkedIn_data(organization_id: str, access_token: str) -> list:
    """Collect LinkedIn post insights."""
    # LinkedIn API requires specific permissions for organization content
    # This is a simplified version
    print("⚠️  LinkedIn API requires specific permissions. Skipping for now.")
    return []


def collect_tiktok_data(user_id: str, access_token: str) -> list:
    """Collect TikTok video insights."""
    # TikTok Research API requires approved app
    print("⚠️  TikTok Research API requires approved app. Skipping for now.")
    return []


def main():
    parser = argparse.ArgumentParser(description="Engagement Data Collector")
    parser.add_argument("--month", default=datetime.now().strftime("%Y-%m"), help="Month to collect data for")
    parser.add_argument("--output", help="Output file (default: engagement-{month}.json)")
    args = parser.parse_args()
    
    print(f"📊 Collecting engagement data for {args.month}...")
    
    # In production, these would come from environment variables or a config file
    ig_user_id = os.environ.get("IG_USER_ID")
    ig_token = os.environ.get("IG_ACCESS_TOKEN")
    fb_page_id = os.environ.get("FB_PAGE_ID")
    fb_token = os.environ.get("FB_ACCESS_TOKEN")
    
    all_posts = []
    
    if ig_user_id and ig_token:
        print("   📸 Collecting Instagram data...")
        ig_posts = collect_instagram_data(ig_user_id, ig_token)
        all_posts.extend(ig_posts)
        print(f"      Found {len(ig_posts)} posts")
    
    if fb_page_id and fb_token:
        print("   📘 Collecting Facebook data...")
        fb_posts = collect_facebook_data(fb_page_id, fb_token)
        all_posts.extend(fb_posts)
        print(f"      Found {len(fb_posts)} posts")
    
    if not all_posts:
        print("⚠️  No data collected. Set IG_USER_ID/IG_ACCESS_TOKEN or FB_PAGE_ID/FB_ACCESS_TOKEN.")
        print("   For now, create engagement-{month}.json manually with this structure:")
        print(json.dumps([{
            "platform": "instagram",
            "post_id": "123",
            "title": "Example post",
            "content_type": "reel",
            "posted_at": "2026-09-01T12:00:00+00:00",
            "posted_hour": 12,
            "likes": 100,
            "comments": 20,
            "shares": 10,
            "saves": 5,
            "clicks": 50,
            "followers": 2000,
            "topic": "hiring"
        }], indent=2))
        sys.exit(0)
    
    # Save data
    output_file = args.output or f"engagement-{args.month}.json"
    Path(output_file).write_text(json.dumps(all_posts, indent=2))
    print(f"\n✅ Saved {len(all_posts)} posts to {output_file}")
    print(f"\nNext steps:")
    print(f"  1. Run self-improving-loop.py to analyze performance")
    print(f"  2. Run monthly-report.py to generate report")


if __name__ == "__main__":
    main()
