#!/usr/bin/env python3
"""
Predictive Content Calculator — Scores content ideas BEFORE posting using platform algorithms.

Usage:
    python scripts/predictive-content-calculator.py --content "5 hiring myths" --platform linkedin
    python scripts/predictive-content-calculator.py --content "salary transparency" --all
    python scripts/predictive-content-calculator.py --batch ideas.json

Scores content ideas based on:
- Platform algorithm weights (dwell time, engagement rate, etc.)
- Content type multipliers (Reels > Static, etc.)
- Virality triggers (contrarian, data-driven, etc.)
- Timing windows (peak vs off-peak)
- Industry calendar relevance
- Penalty avoidance

Output: Score 0-100 + recommendations to improve.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def load_config():
    """Load all config files."""
    config = {}
    config_files = [
        "config/platform-algorithms.json",
        "config/industry-calendar.json",
        "config/strategy.json",
    ]
    for f in config_files:
        if Path(f).exists():
            key = Path(f).stem.replace("-", "_")
            config[key] = json.loads(Path(f).read_text())
    return config


def score_content_type(platform: str, content_type: str, algorithms: dict) -> dict:
    """Score a content type for a platform based on algorithm weights."""
    plat = algorithms.get("platforms", {}).get(platform, {})
    if not plat:
        return {"score": 50, "notes": "Unknown platform"}
    
    formats = plat.get("optimal_formats", {})
    content_key = None
    
    # Match content type to format key
    for key in formats:
        if content_type.lower() in key or key in content_type.lower():
            content_key = key
            break
    
    if not content_key:
        # Default score if format not recognized
        return {"score": 40, "notes": f"Format '{content_type}' not optimal for {platform}"}
    
    format_data = formats[content_key]
    multiplier = format_data.get("engagement_multiplier", 1.0)
    
    # Convert multiplier to score (1.0 = 50, 3.0 = 100)
    score = min(100, max(0, int((multiplier / 3.0) * 100)))
    
    return {
        "score": score,
        "multiplier": multiplier,
        "notes": format_data.get("notes", ""),
    }


def score_timing(platform: str, hour: int, day: str, algorithms: dict) -> dict:
    """Score a posting time based on platform peak windows."""
    plat = algorithms.get("platforms", {}).get(platform, {})
    if not plat:
        return {"score": 50, "notes": "Unknown platform"}
    
    windows = plat.get("posting_windows", {})
    
    # Check if current time matches a peak window
    best_score = 30  # Base score for off-peak
    best_notes = "Off-peak time"
    
    for day_key, times in windows.items():
        if day.lower() in day_key.lower():
            for time_key, time_data in times.items():
                if time_key in ["peak", "secondary", "tertiary"]:
                    # Parse hour from time string like "08:00-09:00"
                    time_str = time_data if isinstance(time_data, str) else time_data.get("peak", "")
                    if "-" in time_str:
                        start_h = int(time_str.split("-")[0].split(":")[0])
                        end_h = int(time_str.split("-")[1].split(":")[0])
                        if start_h <= hour < end_h:
                            if time_key == "peak":
                                best_score = 100
                                best_notes = f"Peak time for {platform}"
                            elif time_key == "secondary":
                                best_score = 80
                                best_notes = f"Secondary peak for {platform}"
                            elif time_key == "tertiary":
                                best_score = 60
                                best_notes = f"Tertiary peak for {platform}"
    
    return {"score": best_score, "notes": best_notes}


def score_virality_triggers(platform: str, content_meta: dict, algorithms: dict) -> dict:
    """Score based on virality triggers present in content."""
    plat = algorithms.get("platforms", {}).get(platform, {})
    if not plat:
        return {"score": 50, "notes": "Unknown platform"}
    
    triggers = plat.get("virality_triggers", {})
    if not triggers:
        return {"score": 50, "notes": "No triggers defined"}
    
    # Count matching triggers
    matched = []
    total_multiplier = 1.0
    
    content_tags = [t.lower() for t in content_meta.get("tags", [])]
    content_title = content_meta.get("title", "").lower()
    
    for trigger_name, trigger_data in triggers.items():
        # Check if trigger keywords match
        trigger_words = trigger_name.replace("_", " ").split()
        if any(word in content_title or word in content_tags for word in trigger_words):
            matched.append(trigger_name)
            total_multiplier *= trigger_data.get("multiplier", 1.0)
    
    # Cap multiplier
    total_multiplier = min(total_multiplier, 5.0)
    score = min(100, int((total_multiplier / 5.0) * 100))
    
    return {
        "score": score,
        "matched_triggers": matched,
        "multiplier": total_multiplier,
        "notes": f"Matched {len(matched)} virality triggers" if matched else "No virality triggers detected",
    }


def score_industry_relevance(content_meta: dict, calendar: dict) -> dict:
    """Score based on current industry calendar relevance."""
    now = datetime.now()
    current_month = now.strftime("%B").lower()
    current_quarter = f"q{(now.month - 1) // 3 + 1}"
    
    cycles = calendar.get("hiring_cycles", {})
    cycle = cycles.get(current_quarter, {})
    
    if not cycle:
        return {"score": 50, "notes": "No cycle data"}
    
    # Check if content matches current cycle themes
    themes = [t.lower() for t in cycle.get("content_themes", [])]
    content_title = content_meta.get("title", "").lower()
    content_tags = [t.lower() for t in content_meta.get("tags", [])]
    
    matches = 0
    for theme in themes:
        theme_words = theme.split()
        if any(word in content_title or word in content_tags for word in theme_words):
            matches += 1
    
    # Check trending topics
    trending = calendar.get("trending_topics_2026", {})
    seasonal = trending.get("seasonal", {}).get(current_month, [])
    
    seasonal_matches = 0
    for topic in seasonal:
        topic_words = topic.lower().split()
        if any(word in content_title or word in content_tags for word in topic_words):
            seasonal_matches += 1
    
    score = 50 + (matches * 10) + (seasonal_matches * 15)
    score = min(100, score)
    
    return {
        "score": score,
        "cycle_match": matches,
        "seasonal_match": seasonal_matches,
        "cycle_name": cycle.get("name", "Unknown"),
        "notes": f"Matches {matches} cycle themes, {seasonal_matches} seasonal topics",
    }


def score_penalty_risk(platform: str, content_meta: dict, algorithms: dict) -> dict:
    """Check for penalty risks in content."""
    plat = algorithms.get("platforms", {}).get(platform, {})
    if not plat:
        return {"risk": "unknown", "notes": "Unknown platform"}
    
    penalties = plat.get("penalties", {})
    if not penalties:
        return {"risk": "low", "notes": "No penalties detected"}
    
    risks = []
    content_title = content_meta.get("title", "").lower()
    
    # Check for common penalty triggers
    if platform == "linkedin":
        if "http" in content_title or "www." in content_title:
            risks.append("external link in post")
        if content_meta.get("hashtags", 0) > 5:
            risks.append("too many hashtags")
    
    elif platform == "instagram":
        if content_meta.get("hashtags", 0) > 10:
            risks.append("hashtag stuffing")
        if content_meta.get("watermark", False):
            risks.append("watermark from other app")
    
    elif platform == "tiktok":
        if content_meta.get("duration", 0) > 60 and content_meta.get("retention", 100) < 50:
            risks.append("long video with poor retention")
        if content_meta.get("watermark", False):
            risks.append("watermark from other app")
    
    risk_level = "low" if len(risks) == 0 else "medium" if len(risks) == 1 else "high"
    
    return {
        "risk": risk_level,
        "detected_risks": risks,
        "notes": f"{len(risks)} penalty risks detected" if risks else "No penalty risks",
    }


def calculate_score(platform: str, content_meta: dict, config: dict) -> dict:
    """Calculate overall score for a content idea."""
    algorithms = config.get("platform_algorithms", {})
    calendar = config.get("industry_calendar", {})
    
    # Score each dimension
    content_type_score = score_content_type(platform, content_meta.get("format", "text"), algorithms)
    
    timing_score = score_timing(
        platform,
        content_meta.get("hour", 12),
        content_meta.get("day", "tuesday"),
        algorithms
    )
    
    virality_score = score_virality_triggers(platform, content_meta, algorithms)
    industry_score = score_industry_relevance(content_meta, calendar)
    penalty_score = score_penalty_risk(platform, content_meta, algorithms)
    
    # Weighted total
    # Content type: 30%, Timing: 20%, Virality: 25%, Industry: 15%, Penalty avoidance: 10%
    penalty_penalty = 0 if penalty_score["risk"] == "low" else 20 if penalty_score["risk"] == "medium" else 40
    
    total = int(
        content_type_score["score"] * 0.30 +
        timing_score["score"] * 0.20 +
        virality_score["score"] * 0.25 +
        industry_score["score"] * 0.15 +
        (100 - penalty_penalty) * 0.10
    )
    
    return {
        "total_score": total,
        "breakdown": {
            "content_type": content_type_score,
            "timing": timing_score,
            "virality": virality_score,
            "industry_relevance": industry_score,
            "penalty_risk": penalty_score,
        },
        "recommendations": generate_recommendations(
            content_type_score, timing_score, virality_score, industry_score, penalty_score
        ),
    }


def generate_recommendations(content_type, timing, virality, industry, penalty):
    """Generate actionable recommendations."""
    recs = []
    
    if content_type["score"] < 60:
        recs.append(f"💡 {content_type['notes']}")
    
    if timing["score"] < 60:
        recs.append(f"⏰ {timing['notes']}. Consider posting during peak hours.")
    
    if virality["score"] < 60:
        recs.append(f"🔥 {virality['notes']}. Add a contrarian take or personal story.")
    
    if industry["score"] < 60:
        recs.append(f"📅 {industry['notes']}. Align with current hiring cycle.")
    
    if penalty["risk"] != "low":
        recs.append(f"⚠️ {penalty['notes']}. Fix before posting.")
    
    if not recs:
        recs.append("✅ Strong content! Ready to post.")
    
    return recs


def main():
    parser = argparse.ArgumentParser(description="Predictive Content Calculator")
    parser.add_argument("--content", help="Content title/idea to score")
    parser.add_argument("--platform", help="Platform (linkedin, instagram, tiktok, facebook, twitter)")
    parser.add_argument("--all", action="store_true", help="Score for all platforms")
    parser.add_argument("--format", default="text", help="Content format (reel, carousel, video, text)")
    parser.add_argument("--hour", type=int, default=12, help="Posting hour (0-23)")
    parser.add_argument("--day", default="tuesday", help="Day of week")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--batch", help="JSON file with multiple ideas")
    args = parser.parse_args()
    
    config = load_config()
    
    if args.batch:
        # Batch mode
        ideas = json.loads(Path(args.batch).read_text())
        results = []
        for idea in ideas:
            result = calculate_score(idea["platform"], idea, config)
            result["idea"] = idea.get("title", "Unknown")
            result["platform"] = idea["platform"]
            results.append(result)
        results.sort(key=lambda x: x["total_score"], reverse=True)
        print(json.dumps(results, indent=2))
        return
    
    if not args.content:
        print("❌ Provide --content or --batch")
        sys.exit(1)
    
    content_meta = {
        "title": args.content,
        "format": args.format,
        "hour": args.hour,
        "day": args.day,
        "tags": args.tags.split(",") if args.tags else [],
    }
    
    if args.all:
        platforms = ["linkedin", "instagram", "tiktok", "facebook", "twitter"]
        results = []
        for platform in platforms:
            result = calculate_score(platform, content_meta, config)
            result["platform"] = platform
            results.append(result)
        results.sort(key=lambda x: x["total_score"], reverse=True)
        
        print(f"\n📊 Content Score: '{args.content}'")
        print(f"   Format: {args.format} | Time: {args.day} {args.hour}:00")
        print(f"   Tags: {', '.join(content_meta['tags'])}\n")
        
        for r in results:
            emoji = "🟢" if r["total_score"] >= 70 else "🟡" if r["total_score"] >= 50 else "🔴"
            print(f"{emoji} {r['platform'].upper()}: {r['total_score']}/100")
            for rec in r["recommendations"]:
                print(f"   {rec}")
            print()
    else:
        if not args.platform:
            print("❌ Provide --platform or use --all")
            sys.exit(1)
        
        result = calculate_score(args.platform, content_meta, config)
        
        print(f"\n📊 Content Score: '{args.content}' → {args.platform.upper()}")
        print(f"   Format: {args.format} | Time: {args.day} {args.hour}:00")
        print(f"   Tags: {', '.join(content_meta['tags'])}\n")
        print(f"   TOTAL SCORE: {result['total_score']}/100\n")
        
        print("   Breakdown:")
        for key, val in result["breakdown"].items():
            print(f"   - {key}: {val.get('score', val.get('risk', 'N/A'))}")
        
        print("\n   Recommendations:")
        for rec in result["recommendations"]:
            print(f"   {rec}")


if __name__ == "__main__":
    main()
