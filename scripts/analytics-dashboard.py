#!/usr/bin/env python3
"""
Analytics Dashboard — Generates an HTML dashboard of all metrics.

Usage:
    python scripts/analytics-dashboard.py --month 2026-09
    python scripts/analytics-dashboard.py --output dashboard.html

Generates a self-contained HTML dashboard with:
- Follower growth charts
- Engagement by platform
- Top performing posts
- Content mix breakdown
- AI citation tracking
- Self-improving recommendations
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


def load_all_data(month: str) -> dict:
    """Load all data sources."""
    data = {"month": month, "posts": [], "followers": {}, "citations": {}, "analysis": {}}
    
    for key, file_prefix in [("posts", "engagement"), ("followers", "followers"), ("citations", "citations"), ("analysis", "analysis")]:
        f = f"{file_prefix}-{month}.json"
        if Path(f).exists():
            data[key] = json.loads(Path(f).read_text())
    return data


def generate_html(data: dict) -> str:
    """Generate self-contained HTML dashboard."""
    posts = data.get("posts", [])
    followers = data.get("followers", {})
    citations = data.get("citations", [])
    analysis = data.get("analysis", {})
    
    total_posts = len(posts)
    total_likes = sum(p.get("likes", 0) for p in posts)
    total_comments = sum(p.get("comments", 0) for p in posts)
    total_shares = sum(p.get("shares", 0) for p in posts)
    total_citations = sum(1 for c in citations if c.get("cited"))
    
    platform_counts = {}
    for p in posts:
        plat = p.get("platform", "unknown")
        platform_counts[plat] = platform_counts.get(plat, 0) + 1
    
    top_posts = sorted(posts, key=lambda x: x.get("likes", 0) + x.get("comments", 0) * 3, reverse=True)[:5]
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAR Content Dashboard — {data['month']}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f1117; color: #e1e4e8; padding: 2rem; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; max-width: 1400px; margin: 0 auto; }}
.card {{ background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 1.5rem; }}
.card h3 {{ color: #8b949e; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }}
.card .value {{ font-size: 2rem; font-weight: 700; color: #58a6ff; }}
.card .sub {{ color: #8b949e; font-size: 0.85rem; margin-top: 0.25rem; }}
h1 {{ text-align: center; margin-bottom: 2rem; color: #f0f6fc; }}
.platform-bar {{ display: flex; align-items: center; gap: 0.5rem; margin: 0.5rem 0; }}
.platform-name {{ width: 100px; font-size: 0.85rem; color: #8b949e; }}
.bar {{ height: 24px; background: #238636; border-radius: 4px; min-width: 4px; transition: width 0.3s; }}
.bar-label {{ font-size: 0.8rem; color: #8b949e; }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{ padding: 0.75rem; text-align: left; border-bottom: 1px solid #30363d; font-size: 0.9rem; }}
th {{ color: #8b949e; font-weight: 600; }}
.recommendation {{ background: #0d419d; border-left: 3px solid #58a6ff; padding: 1rem; margin: 0.5rem 0; border-radius: 0 8px 8px 0; font-size: 0.9rem; }}
</style>
</head>
<body>
<h1>📊 Rent a Recruiter — Content Dashboard</h1>
<p style="text-align:center;color:#8b949e;margin-bottom:2rem;">{data['month']} · Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>

<div class="grid">
  <div class="card">
    <h3>Total Posts</h3>
    <div class="value">{total_posts}</div>
    <div class="sub">Across all platforms</div>
  </div>
  <div class="card">
    <h3>Total Likes</h3>
    <div class="value">{total_likes:,}</div>
    <div class="sub">{(total_likes/total_posts if total_posts else 0):.0f} avg/post</div>
  </div>
  <div class="card">
    <h3>Total Comments</h3>
    <div class="value">{total_comments:,}</div>
    <div class="sub">{(total_comments/total_posts if total_posts else 0):.1f} avg/post</div>
  </div>
  <div class="card">
    <h3>Total Shares</h3>
    <div class="value">{total_shares:,}</div>
    <div class="sub">Viral coefficient: {(total_shares/max(total_likes,1)*100):.1f}%</div>
  </div>
  <div class="card">
    <h3>AI Citations</h3>
    <div class="value">{total_citations}</div>
    <div class="sub">RAR cited by AI engines</div>
  </div>
</div>

<div class="grid" style="margin-top:1.5rem;">
  <div class="card">
    <h3>Platform Breakdown</h3>
    {"".join(f'<div class="platform-bar"><span class="platform-name">{p}</span><div class="bar" style="width:{max(20,c/max(max(platform_counts.values()),1)*200)}px"></div><span class="bar-label">{c}</span></div>' for p, c in sorted(platform_counts.items(), key=lambda x: -x[1]))}
  </div>
  <div class="card">
    <h3>Top 5 Posts</h3>
    <table>
      <tr><th>Platform</th><th>Post</th><th>Score</th></tr>
      {"".join(f'<tr><td>{p.get("platform","?")}</td><td>{p.get("title","")[:40]}...</td><td>{p.get("likes",0)+p.get("comments",0)*3}</td></tr>' for p in top_posts)}
    </table>
  </div>
</div>

<div class="card" style="margin-top:1.5rem;">
  <h3>🧠 Self-Improving Recommendations</h3>
  {"".join(f'<div class="recommendation">{r}</div>' for r in analysis.get("recommendations", ["No recommendations yet — need more data."]))}
</div>

</body>
</html>"""
    return html


def main():
    parser = argparse.ArgumentParser(description="Analytics Dashboard Generator")
    parser.add_argument("--month", default=datetime.now().strftime("%Y-%m"), help="Month to report on")
    parser.add_argument("--output", help="Output HTML file")
    args = parser.parse_args()
    
    data = load_all_data(args.month)
    html = generate_html(data)
    
    output = args.output or f"dashboard-{args.month}.html"
    Path(output).write_text(html)
    print(f"📊 Dashboard saved: {output}")


if __name__ == "__main__":
    main()
