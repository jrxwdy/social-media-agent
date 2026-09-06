#!/usr/bin/env python3
"""
Optimal Time Slacker — Uses platform algorithms + industry calendar to find best posting times.

Usage:
    python scripts/optimal-time-slammer.py --platform linkedin
    python scripts/optimal-time-slammer.py --all --next-days 7
    python scripts/optimal-time-slammer.py --month-september --output calendar.csv

Finds the optimal posting times by cross-referencing:
- Platform peak windows
- Industry hiring cycles
- Events calendar (conferences, expos)
- Competitor posting times (avoid their peak to stand out)
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path


def load_config():
    """Load config files."""
    config = {}
    for f in ["config/platform-algorithms.json", "config/industry-calendar.json"]:
        if Path(f).exists():
            key = Path(f).stem.replace("-", "_")
            config[key] = json.loads(Path(f).read_text())
    return config


def get_optimal_times(platform: str, days_ahead: int = 7) -> list:
    """Get optimal posting times for the next N days."""
    config = load_config()
    algorithms = config.get("platform_algorithms", {})
    calendar = config.get("industry_calendar", {})
    
    plat = algorithms.get("platforms", {}).get(platform, {})
    if not plat:
        return []
    
    windows = plat.get("posting_windows", {})
    events = calendar.get("recruitment_events_2026", {})
    
    results = []
    now = datetime.now()
    
    for day_offset in range(days_ahead):
        date = now + timedelta(days=day_offset)
        day_name = date.strftime("%A").lower()
        month_name = date.strftime("%B").lower()
        hour = date.hour
        
        # Find matching windows
        matching_windows = []
        for day_key, times in windows.items():
            if day_name in day_key.lower():
                for time_key, time_data in times.items():
                    if time_key in ["peak", "secondary", "tertiary"]:
                        time_str = time_data if isinstance(time_data, str) else time_data.get("peak", "")
                        matching_windows.append({
                            "time": time_str,
                            "priority": time_key,
                            "score": 100 if time_key == "peak" else 80 if time_key == "secondary" else 60,
                        })
        
        # Check for events on this day
        month_events = events.get(month_name, [])
        day_events = []
        for event in month_events:
            # Simple date matching (in production, parse actual dates)
            day_events.append(event)
        
        # Check for seasonal relevance
        trending = calendar.get("trending_topics_2026", {})
        seasonal = trending.get("seasonal", {}).get(month_name, [])
        
        if matching_windows:
            results.append({
                "date": date.strftime("%Y-%m-%d"),
                "day": day_name,
                "windows": matching_windows,
                "events": day_events,
                "seasonal_topics": seasonal,
            })
    
    return results


def generate_posting_calendar(days_ahead: int = 30) -> list:
    """Generate a full posting calendar across all platforms."""
    platforms = ["linkedin", "instagram", "tiktok", "facebook", "twitter"]
    calendar = []
    
    for platform in platforms:
        times = get_optimal_times(platform, days_ahead)
        for t in times:
            t["platform"] = platform
            calendar.append(t)
    
    # Sort by date
    calendar.sort(key=lambda x: x["date"])
    return calendar


def main():
    parser = argparse.ArgumentParser(description="Optimal Time Finder")
    parser.add_argument("--platform", help="Specific platform")
    parser.add_argument("--all", action="store_true", help="All platforms")
    parser.add_argument("--next-days", type=int, default=7, help="Days to look ahead")
    parser.add_argument("--output", help="Output CSV file")
    args = parser.parse_args()
    
    config = load_config()
    
    if args.all:
        calendar = generate_posting_calendar(args.next_days)
        print(f"\n📅 Posting Calendar — Next {args.next_days} Days\n")
        
        current_date = ""
        for entry in calendar:
            if entry["date"] != current_date:
                current_date = entry["date"]
                print(f"\n{current_date} ({entry['day']})")
                if entry.get("events"):
                    for event in entry["events"]:
                        print(f"  🎪 {event['name']} — {event['location']}")
            
            for window in entry["windows"]:
                emoji = "🔴" if window["priority"] == "peak" else "🟡" if window["priority"] == "secondary" else "🟢"
                print(f"  {emoji} {entry['platform']:12s} {window['time']:15s} ({window['priority']})")
        
        if args.output:
            import csv
            with open(args.output, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["date", "day", "platform", "time", "priority", "score"])
                for entry in calendar:
                    for window in entry["windows"]:
                        writer.writerow([
                            entry["date"],
                            entry["day"],
                            entry["platform"],
                            window["time"],
                            window["priority"],
                            window["score"],
                        ])
            print(f"\n📄 Calendar saved: {args.output}")
    
    elif args.platform:
        times = get_optimal_times(args.platform, args.next_days)
        print(f"\n📅 {args.platform.upper()} — Next {args.next_days} Days\n")
        
        for t in times:
            print(f"\n{t['date']} ({t['day']})")
            if t.get("events"):
                for event in t["events"]:
                    print(f"  🎪 {event['name']}")
            for window in t["windows"]:
                emoji = "🔴" if window["priority"] == "peak" else "🟡" if window["priority"] == "secondary" else "🟢"
                print(f"  {emoji} {window['time']:15s} ({window['priority']})")
    
    else:
        print("❌ Provide --platform or --all")


if __name__ == "__main__":
    main()
