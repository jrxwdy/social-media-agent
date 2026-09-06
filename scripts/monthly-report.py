#!/usr/bin/env python3
"""
Monthly Report Generator — Auto-generates the report for Barry.

Usage:
    python scripts/monthly-report.py --month 2026-09
    python scripts/monthly-report.py --month 2026-09 --output report.md

Pulls data from:
- Mixpost API (posts published, scheduled)
- Platform APIs (follower growth, engagement)
- AI citation tracker (citations this month)
- Self-improving loop (performance analysis)
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def load_data(month: str) -> dict:
    """Load all data sources for the month."""
    data = {
        "month": month,
        "generated_at": datetime.now().isoformat(),
        "posts": [],
        "followers": {},
        "engagement": {},
        "citations": {},
        "analysis": {},
    }
    
    # Load engagement data
    engagement_file = f"engagement-{month}.json"
    if Path(engagement_file).exists():
        data["posts"] = json.loads(Path(engagement_file).read_text())
    
    # Load follower data
    follower_file = f"followers-{month}.json"
    if Path(follower_file).exists():
        data["followers"] = json.loads(Path(follower_file).read_text())
    
    # Load AI citation data
    citation_file = f"citations-{month}.json"
    if Path(citation_file).exists():
        data["citations"] = json.loads(Path(citation_file).read_text())
    
    # Load self-improving analysis
    analysis_file = f"analysis-{month}.json"
    if Path(analysis_file).exists():
        data["analysis"] = json.loads(Path(analysis_file).read_text())
    
    return data


def generate_report(data: dict) -> str:
    """Generate the monthly report."""
    month = data["month"]
    posts = data.get("posts", [])
    followers = data.get("followers", {})
    citations = data.get("citations", {})
    analysis = data.get("analysis", {})
    
    # Calculate metrics
    total_posts = len(posts)
    total_likes = sum(p.get("likes", 0) for p in posts)
    total_comments = sum(p.get("comments", 0) for p in posts)
    total_shares = sum(p.get("shares", 0) for p in posts)
    
    # Platform breakdown
    platform_posts = {}
    for p in posts:
        platform = p.get("platform", "unknown")
        platform_posts[platform] = platform_posts.get(platform, 0) + 1
    
    # Top performer
    top_post = None
    if posts:
        scored = sorted(posts, key=lambda x: x.get("likes", 0) + x.get("comments", 0) * 3, reverse=True)
        top_post = scored[0]
    
    # Follower growth
    follower_growth = {}
    for platform, counts in followers.items():
        if len(counts) >= 2:
            growth = counts[-1] - counts[0]
            pct = (growth / counts[0] * 100) if counts[0] > 0 else 0
            follower_growth[platform] = {"absolute": growth, "percent": round(pct, 1)}
    
    # AI citations
    total_citations = sum(1 for c in citations if c.get("cited", False))
    citation_rate = (total_citations / len(citations) * 100) if citations else 0
    
    # Build report
    report = f"""# 📊 Monthly Content Report — {month}

## Overview

| Metric | Value |
|---|---|
| Total posts published | {total_posts} |
| Total likes | {total_likes:,} |
| Total comments | {total_comments:,} |
| Total shares | {total_shares:,} |
| Avg engagement per post | {round((total_likes + total_comments + total_shares) / total_posts) if total_posts else 0} |

## Follower Growth

| Platform | Growth | % |
|---|---|---|"""
    
    for platform, growth in sorted(follower_growth.items(), key=lambda x: -x[1]["absolute"]):
        report += f"\n| {platform} | +{growth['absolute']:,} | +{growth['percent']}% |"
    
    report += f"\n\n## Platform Breakdown\n\n| Platform | Posts |\n|---|---|"
    
    for platform, count in sorted(platform_posts.items(), key=lambda x: -x[1]):
        report += f"\n| {platform} | {count} |"
    
    report += f"\n\n## 🏆 Top Performer\n\n"
    if top_post:
        report += f"**{top_post.get('title', 'Untitled')}**\n"
        report += f"- Platform: {top_post.get('platform', 'unknown')}\n"
        report += f"- Engagement: {top_post.get('likes', 0)} likes, {top_post.get('comments', 0)} comments\n"
        report += f"- Posted: {top_post.get('posted_at', 'unknown')}\n"
    
    report += f"\n## 🤖 AI Citations\n\n| Metric | Value |\n|---|---|\n"
    report += f"| Keywords monitored | {len(citations)} |\n"
    report += f"| RAR cited | {total_citations} |\n"
    report += f"| Citation rate | {citation_rate:.0f}% |\n"
    
    report += f"\n## 📈 Self-Improving Insights\n\n"
    if analysis.get("recommendations"):
        for rec in analysis["recommendations"]:
            report += f"- {rec}\n"
    else:
        report += "No insights yet — need more data.\n"
    
    report += f"\n## 📅 Next Month\n\n"
    if analysis.get("focus_topics"):
        report += f"**Focus topics:** {', '.join(analysis['focus_topics'])}\n\n"
    if analysis.get("content_type_avg"):
        best_type = max(analysis["content_type_avg"], key=analysis["content_type_avg"].get)
        report += f"**Double down on:** {best_type}\n\n"
    
    report += f"---\n*Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"
    
    return report


def main():
    parser = argparse.ArgumentParser(description="Monthly Report Generator")
    parser.add_argument("--month", default=datetime.now().strftime("%Y-%m"), help="Month to report on")
    parser.add_argument("--output", help="Output file (default: stdout)")
    args = parser.parse_args()
    
    print(f"📊 Generating monthly report for {args.month}...")
    
    data = load_data(args.month)
    report = generate_report(data)
    
    if args.output:
        Path(args.output).write_text(report)
        print(f"📄 Report saved: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
