#!/usr/bin/env python3
"""
Content Idea Generator — Uses brand model + industry calendar + platform algorithms to generate ideas.

Usage:
    python scripts/content-idea-generator.py --count 10
    python scripts/content-idea-generator.py --platform linkedin --count 5
    python scripts/content-idea-generator.py --theme "hiring myths" --count 3
    python scripts/content-idea-generator.py --trending --count 10

Generates content ideas that are:
- On-brand (match Barry's voice and key messages)
- Industry-relevant (aligned with hiring cycles)
- Platform-optimized (right format for each platform)
- Timely (trending topics, events, seasons)
"""

import argparse
import json
import random
from datetime import datetime
from pathlib import Path


def load_config():
    """Load all config files."""
    config = {}
    for f in ["config/brand-model.json", "config/industry-calendar.json", "config/platform-algorithms.json", "config/strategy.json"]:
        if Path(f).exists():
            key = Path(f).stem.replace("-", "_")
            config[key] = json.loads(Path(f).read_text())
    return config


def generate_idea(theme: str, platform: str, config: dict) -> dict:
    """Generate a single content idea."""
    brand = config.get("brand_model", {})
    calendar = config.get("industry_calendar", {})
    algorithms = config.get("platform_algorithms", {})
    
    # Get platform-specific format options
    plat = algorithms.get("platforms", {}).get(platform, {})
    formats = plat.get("optimal_formats", {})
    top_formats = sorted(formats.items(), key=lambda x: x[1].get("engagement_multiplier", 1), reverse=True)[:3]
    
    # Get theme data
    themes = brand.get("content_themes", {})
    theme_data = themes.get(f"theme_{list(themes.keys()).index(theme) + 1}" if theme in [t.get("name","").lower().replace(" ","_") for t in themes.values()] else "theme_1", {})
    
    # Get current cycle
    now = datetime.now()
    quarter = f"q{(now.month - 1) // 3 + 1}"
    cycles = calendar.get("hiring_cycles", {})
    cycle = cycles.get(quarter, {})
    
    # Get trending topics
    trending = calendar.get("trending_topics_2026", {})
    seasonal = trending.get("seasonal", {}).get(now.strftime("%B").lower(), [])
    
    # Build idea
    idea = {
        "title": f"{theme}: {random.choice(themes.get(theme, {}).get('examples', ['New insight']))}" if theme in themes else f"{theme} — fresh take",
        "platform": platform,
        "format": random.choice([f[0] for f in top_formats]) if top_formats else "text",
        "theme": theme,
        "key_message": random.choice(list(brand.get("key_messages", {}).values())),
        "hook_style": random.choice(["contrarian", "data-driven", "question", "personal_story"]),
        "cta": random.choice(["question", "save_share", "link_in_bio", "comment"]),
        "seasonal_relevance": random.choice(seasonal) if seasonal else "evergreen",
        "cycle_alignment": cycle.get("name", "Unknown"),
        "bars_voice": random.choice(brand.get("founder_voice", {}).get("phrases", [])),
    }
    
    return idea


def generate_ideas(count: int, platform: str = None, theme: str = None, trending: bool = False) -> list:
    """Generate multiple content ideas."""
    config = load_config()
    brand = config.get("brand_model", {})
    calendar = config.get("industry_calendar", {})
    
    # Get available themes
    themes = brand.get("content_themes", {})
    theme_names = [t.get("name", "").lower().replace(" ", "_") for t in themes.values()]
    
    # Get trending topics
    trending_topics = calendar.get("trending_topics_2026", {})
    evergreen = trending_topics.get("evergreen", [])
    emerging = trending_topics.get("emerging", [])
    
    platforms = [platform] if platform else ["linkedin", "instagram", "tiktok", "facebook", "twitter"]
    ideas = []
    
    for i in range(count):
        p = random.choice(platforms)
        if theme:
            t = theme
        elif trending:
            t = random.choice(evergreen + emerging)
        else:
            t = random.choice(theme_names)
        
        idea = generate_idea(t, p, config)
        idea["id"] = f"idea-{i+1:03d}"
        ideas.append(idea)
    
    return ideas


def main():
    parser = argparse.ArgumentParser(description="Content Idea Generator")
    parser.add_argument("--count", type=int, default=10, help="Number of ideas to generate")
    parser.add_argument("--platform", help="Specific platform")
    parser.add_argument("--theme", help="Specific theme")
    parser.add_argument("--trending", action="store_true", help="Focus on trending topics")
    parser.add_argument("--output", help="Output JSON file")
    args = parser.parse_args()
    
    ideas = generate_ideas(args.count, args.platform, args.theme, args.trending)
    
    print(f"\n💡 Generated {len(ideas)} Content Ideas\n")
    
    for idea in ideas:
        print(f"  {idea['id']}: {idea['title']}")
        print(f"    Platform: {idea['platform']} | Format: {idea['format']}")
        print(f"    Theme: {idea['theme']} | Hook: {idea['hook_style']}")
        print(f"    Seasonal: {idea['seasonal_relevance']} | Cycle: {idea['cycle_alignment']}")
        print(f"    Voice: \"{idea['bars_voice']}\"")
        print()
    
    if args.output:
        Path(args.output).write_text(json.dumps(ideas, indent=2))
        print(f"📄 Ideas saved: {args.output}")


if __name__ == "__main__":
    main()
