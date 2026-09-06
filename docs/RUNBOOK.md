# Runbook — Barry Content Agent

## Daily (5 minutes)

### Check Slack (#content-approval)
- Review any pending posts
- Click ✅ Approve, ✏️ Edit, or ❌ Reject
- If no action in 24hrs, auto-approves (configurable)

### Check Mixpost calendar
- Verify today's posts are scheduled
- Look for any failed publishes

## Weekly (30 minutes, Monday morning)

### Review competitor report
- n8n auto-posts to Slack every Monday
- Read the 3-bullet analysis
- Identify 1-2 content opportunities for the week

### Review trend discovery
- Check what's trending in recruitment
- Approve or adapt trend-based posts in Mixpost queue

### Content mix check
Ensure the week's content is balanced:
- LinkedIn: founder voice (not just company updates)
- Instagram: mix of Reels, carousels, static
- TikTok: short, punchy, trend-aligned
- Facebook: link backs to blog + social proof

## Monthly (1 hour, first week)

### AI citation check
```bash
python scripts/ai-citation-tracker.py --month 2026-09 --output report.md
```
This generates a report on whether RAR is cited by ChatGPT/Gemini/Perplexity.
Share with Barry — it's the "are we winning AI search?" scorecard.

### Analytics review
Pull metrics from each platform:
- Follower growth
- Engagement rate
- Top performing post
- Worst performing post
- Traffic to website from social

### Self-improvement loop
- Kill bottom 20% of content types
- Double down on top 20%
- Update templates if needed

### Send monthly report to Barry
Template:
```
📊 MONTHLY CONTENT REPORT — [Month]

📈 Followers
- LinkedIn: +X% (now Y)
- Instagram: +X% (now Y)
- TikTok: +X% (now Y)

🏆 Top Post
- [Platform]: [Post description]
- Engagement: X likes, Y comments, Z shares

📉 Needs Improvement
- [Content type] underperformed — adjusting strategy

🤖 AI Citations
- RAR cited X times across AI engines
- Top keyword: "[keyword]"

📅 Next Month
- Focus: [theme]
- Goal: [target]
```

## Quarterly (2 hours)

### Full content audit
- What worked, what didn't
- Competitor landscape changes
- Platform algorithm shifts
- Template refresh
- Hashtag refresh

### Strategy adjustment
- Content mix rebalancing
- New platform evaluation (YouTube? Pinterest?)
- Pricing review (still competitive?)

## Who does what

### Agent (automated)
- Blog repurpose → social drafts
- Trend discovery every 6hrs
- Competitor monitoring Monday
- Scheduling and publishing (after approval)

### Barry / Julieanne
- Approve posts in Slack (5 min/day)
- Provide feedback (what feels right, what doesn't)
- Share wins, news, conference clips

### James / Agent team
- Monthly report
- Quarterly audit
- Strategy adjustment
- Technical maintenance

## Escalation

| Issue | Who | Action |
|---|---|---|
| Post failed to publish | Agent | Check Mixpost logs, retry |
| Negative comments on post | Barry/Julieanne | Respond or flag |
| Competitor launches new content | Agent | Alert + adapt trend strategy |
| Platform API changes | James | Update workflow + templates |
| Barry unhappy with content | James | Adjust prompts + templates |
