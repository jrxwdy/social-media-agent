#!/usr/bin/env python3
"""
Self-Improving Loop — Reads engagement data, scores posts, updates strategy.

Usage:
    python scripts/self-improving-loop.py
    python scripts/self-improving-loop.py --month 2026-09
    python scripts/self-improving-loop.py --auto-apply

This is the "brain" of the content engine. It:
1. Pulls engagement data from all platforms
2. Scores every post
3. Identifies top/bottom performers
4. Generates recommendations
5. Can auto-update templates and strategy
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# Platform APIs (simplified — in production, use official APIs)
PLATFORM_APIS = {
    "instagram": "https://graph.facebook.com/v21.0/{ig_user_id}/media",
    "facebook": "https://graph.facebook.com/v21.0/{page_id}/posts",
    "linkedin": "https://api.linkedin.com/v2/posts",
    "tiktok": "https://open.tiktokapis.com/v2/video/list/",
}


def load_engagement_data(month: str) -> list:
    """
    Load engagement data for the month.
    In production, this pulls from platform APIs.
    For now, reads from a JSON file that n8n populates.
    """
    data_file = f"engagement-{month}.json"
    if Path(data_file).exists():
        return json.loads(Path(data_file).read_text())
    
    # Demo data for testing
    print(f"⚠️  No engagement data found for {month}. Run n8n workflow to populate.")
    print(f"   Expected file: {data_file}")
    return []


def score_post(post: dict) -> dict:
    """
    Score a single post based on engagement relative to followers.
    
    Scoring:
    - Like rate: likes / followers (weight: 1x)
    - Comment rate: comments / followers (weight: 3x)
    - Share rate: shares / followers (weight: 5x)
    - Save rate: saves / followers (weight: 4x)
    - Click rate: clicks / followers (weight: 2x)
    """
    followers = post.get("followers", 1000)
    if followers == 0:
        followers = 1000
    
    likes = post.get("likes", 0)
    comments = post.get("comments", 0)
    shares = post.get("shares", 0)
    saves = post.get("saves", 0)
    clicks = post.get("clicks", 0)
    
    like_rate = likes / followers
    comment_rate = comments / followers
    share_rate = shares / followers
    save_rate = saves / followers
    click_rate = clicks / followers
    
    # Weighted score
    score = (
        like_rate * 1.0 +
        comment_rate * 3.0 +
        share_rate * 5.0 +
        save_rate * 4.0 +
        click_rate * 2.0
    ) * 100
    
    return {
        **post,
        "score": round(score, 2),
        "like_rate": round(like_rate * 100, 2),
        "comment_rate": round(comment_rate * 100, 2),
        "share_rate": round(share_rate * 100, 2),
        "save_rate": round(save_rate * 100, 2),
        "click_rate": round(click_rate * 100, 2),
    }


def analyze_performance(posts: list) -> dict:
    """Analyze overall performance and generate insights."""
    if not posts:
        return {"error": "No posts to analyze"}
    
    # Score all posts
    scored = [score_post(p) for p in posts]
    
    # Sort by score
    scored.sort(key=lambda x: x["score"], reverse=True)
    
    # Top and bottom performers
    top_20 = scored[:max(1, len(scored) // 5)]
    bottom_20 = scored[-(max(1, len(scored) // 5)):]
    
    # Platform breakdown
    platform_scores = defaultdict(list)
    for p in scored:
        platform_scores[p.get("platform", "unknown")].append(p["score"])
    
    platform_avg = {}
    for platform, scores in platform_scores.items():
        platform_avg[platform] = round(sum(scores) / len(scores), 2)
    
    # Content type breakdown
    type_scores = defaultdict(list)
    for p in scored:
        type_scores[p.get("content_type", "unknown")].append(p["score"])
    
    type_avg = {}
    for ctype, scores in type_scores.items():
        type_avg[ctype] = round(sum(scores) / len(scores), 2)
    
    # Posting time breakdown
    time_scores = defaultdict(list)
    for p in scored:
        hour = p.get("posted_hour", 12)
        bucket = f"{hour:02d}:00"
        time_scores[bucket].append(p["score"])
    
    time_avg = {}
    for time, scores in time_scores.items():
        if len(scores) >= 2:  # Need at least 2 posts to be meaningful
            time_avg[time] = round(sum(scores) / len(scores), 2)
    
    # Topic breakdown
    topic_scores = defaultdict(list)
    for p in scored:
        topic = p.get("topic", "general")
        topic_scores[topic].append(p["score"])
    
    topic_avg = {}
    for topic, scores in topic_scores.items():
        if len(scores) >= 2:
            topic_avg[topic] = round(sum(scores) / len(scores), 2)
    
    # Generate recommendations
    recommendations = []
    
    # Best platform
    if platform_avg:
        best_platform = max(platform_avg, key=platform_avg.get)
        worst_platform = min(platform_avg, key=platform_avg.get)
        recommendations.append(f"Double down on {best_platform} (avg score: {platform_avg[best_platform]})")
        if platform_avg[best_platform] > platform_avg[worst_platform] * 1.5:
            recommendations.append(f"Reduce {worst_platform} frequency (avg score: {platform_avg[worst_platform]})")
    
    # Best content type
    if type_avg:
        best_type = max(type_avg, key=type_avg.get)
        worst_type = min(type_avg, key=type_avg.get)
        recommendations.append(f"More {best_type} content (avg score: {type_avg[best_type]})")
        if type_avg[best_type] > type_avg[worst_type] * 1.5:
            recommendations.append(f"Kill or reduce {worst_type} (avg score: {type_avg[worst_type]})")
    
    # Best posting times
    if time_avg:
        best_times = sorted(time_avg.items(), key=lambda x: -x[1])[:3]
        recommendations.append(f"Best posting times: {', '.join(t[0] for t in best_times)}")
    
    # Best topics
    if topic_avg:
        best_topics = sorted(topic_avg.items(), key=lambda x: -x[1])[:3]
        recommendations.append(f"Top topics: {', '.join(t[0] for t in best_topics)}")
    
    # Bottom performer patterns
    if bottom_20:
        bottom_types = defaultdict(int)
        for p in bottom_20:
            bottom_types[p.get("content_type", "unknown")] += 1
        worst_performing_type = max(bottom_types, key=bottom_types.get)
        recommendations.append(f"Review {worst_performing_type} format — overrepresented in bottom performers")
    
    return {
        "total_posts": len(scored),
        "avg_score": round(sum(p["score"] for p in scored) / len(scored), 2),
        "top_performer": scored[0] if scored else None,
        "bottom_performer": scored[-1] if scored else None,
        "platform_avg": platform_avg,
        "content_type_avg": type_avg,
        "time_avg": time_avg,
        "topic_avg": topic_avg,
        "top_20": top_20,
        "bottom_20": bottom_20,
        "recommendations": recommendations,
    }


def auto_apply_strategy(analysis: dict) -> dict:
    """
    Auto-update strategy based on analysis.
    Returns the updated strategy.
    """
    strategy = {
        "updated_at": datetime.now().isoformat(),
        "content_mix": {},
        "posting_times": {},
        "focus_topics": [],
        "kill_topics": [],
    }
    
    # Update content mix based on performance
    type_avg = analysis.get("content_type_avg", {})
    if type_avg:
        total_score = sum(type_avg.values())
        for ctype, avg in type_avg.items():
            # Higher score = higher percentage
            pct = max(10, min(50, int((avg / total_score) * 100)))
            strategy["content_mix"][ctype] = f"{pct}%"
    
    # Update posting times
    time_avg = analysis.get("time_avg", {})
    if time_avg:
        best_times = sorted(time_avg.items(), key=lambda x: -x[1])[:3]
        for time, score in best_times:
            strategy["posting_times"][time] = "high"
    
    # Update topics
    topic_avg = analysis.get("topic_avg", {})
    if topic_avg:
        sorted_topics = sorted(topic_avg.items(), key=lambda x: -x[1])
        strategy["focus_topics"] = [t[0] for t in sorted_topics[:3]]
        strategy["kill_topics"] = [t[0] for t in sorted_topics[-2:]] if len(sorted_topics) > 3 else []
    
    return strategy


def generate_report(analysis: dict, month: str) -> str:
    """Generate markdown report."""
    report = f"""# Self-Improving Loop Report — {month}

## Summary

| Metric | Value |
|---|---|
| Total posts analyzed | {analysis['total_posts']} |
| Average score | {analysis['avg_score']} |

## Platform Performance

| Platform | Avg Score |
|---|---"""
    
    for platform, avg in sorted(analysis.get("platform_avg", {}).items(), key=lambda x: -x[1]):
        report += f"\n| {platform} | {avg} |"
    
    report += f"\n\n## Content Type Performance\n\n| Type | Avg Score |\n|---|---"
    
    for ctype, avg in sorted(analysis.get("content_type_avg", {}).items(), key=lambda x: -x[1]):
        report += f"\n| {ctype} | {avg} |"
    
    report += f"\n\n## Top Performer\n\n"
    top = analysis.get("top_performer")
    if top:
        report += f"- **{top.get('title', 'Untitled')}** ({top.get('platform', 'unknown')})\n"
        report += f"- Score: {top['score']}\n"
        report += f"- Engagement: {top.get('likes', 0)} likes, {top.get('comments', 0)} comments\n"
    
    report += f"\n## Recommendations\n\n"
    for i, rec in enumerate(analysis.get("recommendations", []), 1):
        report += f"{i}. {rec}\n"
    
    report += f"\n---\n*Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"
    return report


def main():
    parser = argparse.ArgumentParser(description="Self-Improving Loop for Barry Content Agent")
    parser.add_argument("--month", default=datetime.now().strftime("%Y-%m"), help="Month to analyze")
    parser.add_argument("--output", help="Output file (default: stdout)")
    parser.add_argument("--auto-apply", action="store_true", help="Auto-update strategy based on analysis")
    parser.add_argument("--strategy-output", default="config/strategy.json", help="Where to save updated strategy")
    args = parser.parse_args()
    
    print(f"🧠 Self-Improving Loop — {args.month}")
    
    # Load data
    posts = load_engagement_data(args.month)
    if not posts:
        print("❌ No engagement data. Run n8n workflow to populate engagement data first.")
        sys.exit(1)
    
    print(f"   Loaded {len(posts)} posts")
    
    # Analyze
    analysis = analyze_performance(posts)
    
    # Generate report
    report = generate_report(analysis, args.month)
    
    if args.output:
        Path(args.output).write_text(report)
        print(f"📄 Report saved: {args.output}")
    else:
        print(report)
    
    # Auto-apply strategy
    if args.auto_apply:
        strategy = auto_apply_strategy(analysis)
        Path(args.strategy_output).write_text(json.dumps(strategy, indent=2))
        print(f"📊 Strategy updated: {args.strategy_output}")
        print(f"   Focus topics: {', '.join(strategy['focus_topics'])}")
        print(f"   Kill topics: {', '.join(strategy['kill_topics'])}")
    
    # Save analysis data
    data_file = f"analysis-{args.month}.json"
    Path(data_file).write_text(json.dumps(analysis, indent=2))
    print(f"📊 Analysis saved: {data_file}")


if __name__ == "__main__":
    main()
