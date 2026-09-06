#!/usr/bin/env python3
"""
AI Citation Tracker — Monthly check if RAR is cited by AI engines.

Usage:
    python scripts/ai-citation-tracker.py
    python scripts/ai-citation-tracker.py --month 2026-09
    python scripts/ai-citation-tracker.py --output report.md

Queries ChatGPT, Gemini, Perplexity for RAR keywords and checks if
Rent a Recruiter is cited in the response.

Note: AI engines don't have public APIs for this. This script uses
their web interfaces via browser automation or manual input.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Keywords to monitor
KEYWORDS = [
    "rent a recruiter",
    "rent a recruiter Ireland",
    "rent a recruiter Australia",
    "embedded recruitment",
    "embedded recruitment Ireland",
    "recruitment as a service",
    "RaaS recruitment",
    "how to hire in Ireland",
    "how to hire in Australia",
    "best recruitment agency Ireland",
    "best recruitment agency Australia",
    "recruitment agency Dublin",
    "talent acquisition Ireland",
    "employer branding Ireland",
]

# Competitors to check against
COMPETITORS = [
    "Cpl",
    "Sigmar",
    "Hays Ireland",
    "Morgan McKinley",
    "Allen Recruitment",
]


def check_citation_manual(keyword: str) -> dict:
    """
    Manual check — prompts user to paste AI engine response.
    In production, this would use browser automation or a third-party
    service like Peec.ai, Profound, or Ahrefs AI citations.
    """
    print(f"\n{'='*60}")
    print(f"Keyword: {keyword}")
    print(f"{'='*60}")
    print(f"\n1. Ask ChatGPT: '{keyword}'")
    print(f"2. Ask Gemini: '{keyword}'")
    print(f"3. Ask Perplexity: '{keyword}'")
    print(f"\nFor each, check if 'Rent a Recruiter' or 'rentarecruiter.com' is cited.")
    
    cited = input("\nWas RAR cited in ANY engine? (y/n): ").lower().strip() == 'y'
    which = []
    if cited:
        if input("  ChatGPT? (y/n): ").lower() == 'y':
            which.append("ChatGPT")
        if input("  Gemini? (y/n): ").lower() == 'y':
            which.append("Gemini")
        if input("  Perplexity? (y/n): ").lower() == 'y':
            which.append("Perplexity")
    
    competitors_cited = []
    for comp in COMPETITORS:
        if input(f"  Was {comp} cited? (y/n): ").lower() == 'y':
            competitors_cited.append(comp)
    
    return {
        "keyword": keyword,
        "cited": cited,
        "engines": which,
        "competitors_cited": competitors_cited,
    }


def generate_report(results: list, month: str) -> str:
    """Generate markdown report."""
    total = len(results)
    cited_count = sum(1 for r in results if r["cited"])
    citation_rate = (cited_count / total * 100) if total else 0
    
    # Count engine breakdown
    engine_counts = {"ChatGPT": 0, "Gemini": 0, "Perplexity": 0}
    for r in results:
        for eng in r.get("engines", []):
            engine_counts[eng] = engine_counts.get(eng, 0) + 1
    
    # Competitor mentions
    comp_mentions = {}
    for r in results:
        for comp in r.get("competitors_cited", []):
            comp_mentions[comp] = comp_mentions.get(comp, 0) + 1
    
    report = f"""# AI Citation Report — {month}

## Summary

| Metric | Value |
|---|---|
| Keywords monitored | {total} |
| RAR cited | {cited_count} |
| Citation rate | {citation_rate:.0f}% |

## Engine Breakdown

| Engine | Times cited |
|---|---|
| ChatGPT | {engine_counts['ChatGPT']} |
| Gemini | {engine_counts['Gemini']} |
| Perplexity | {engine_counts['Perplexity']} |

## Competitor Citations

| Competitor | Times cited |
|---|---|
"""
    for comp, count in sorted(comp_mentions.items(), key=lambda x: -x[1]):
        report += f"| {comp} | {count} |\n"
    
    report += f"\n## Keyword Details\n\n"
    report += "| Keyword | RAR Cited | Engines | Competitors |\n"
    report += "|---|---|---|---|\n"
    for r in results:
        engines = ", ".join(r.get("engines", [])) or "—"
        comps = ", ".join(r.get("competitors_cited", [])) or "—"
        cited = "✅" if r["cited"] else "❌"
        report += f"| {r['keyword']} | {cited} | {engines} | {comps} |\n"
    
    report += f"\n---\n*Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"
    return report


def main():
    parser = argparse.ArgumentParser(description="AI Citation Tracker for RAR")
    parser.add_argument("--month", default=datetime.now().strftime("%Y-%m"), help="Month to report on")
    parser.add_argument("--output", help="Output file (default: stdout)")
    parser.add_argument("--quick", action="store_true", help="Skip to summary (for demos)")
    args = parser.parse_args()
    
    print(f"🔍 AI Citation Tracker — {args.month}")
    print(f"   Monitoring {len(KEYWORDS)} keywords")
    print(f"   Tracking {len(COMPETITORS)} competitors")
    
    if args.quick:
        # Demo mode — generate sample report
        results = []
        for kw in KEYWORDS:
            results.append({
                "keyword": kw,
                "cited": kw in ["rent a recruiter", "embedded recruitment"],
                "engines": ["ChatGPT"] if kw == "rent a recruiter" else [],
                "competitors_cited": ["Cpl", "Sigmar"] if "Ireland" in kw else [],
            })
    else:
        results = []
        for kw in KEYWORDS:
            results.append(check_citation_manual(kw))
    
    report = generate_report(results, args.month)
    
    if args.output:
        Path(args.output).write_text(report)
        print(f"\n📄 Report saved: {args.output}")
    else:
        print(report)
    
    # Save raw data
    data_file = f"citations-{args.month}.json"
    Path(data_file).write_text(json.dumps(results, indent=2))
    print(f"📊 Raw data saved: {data_file}")


if __name__ == "__main__":
    main()
