# Barry Content Agent — Project Overview

## What this is
Complete, deployable content engine for Rent a Recruiter. Built on Isabella pipeline infrastructure + Mixpost + n8n.

## Structure
```
barry-content-agent/
├── docker-compose.yml          # Mixpost + n8n + supporting services
├── .env.example                # All required secrets
├── workflows/
│   ├── blog-to-social.json     # n8n: blog post → 3 platform drafts → Mixpost
│   ├── trend-discovery.json    # n8n: Apify scrape → trend score → queue
│   ├── competitor-monitor.json # n8n: weekly competitor scrape → report
│   └── approval-bot.json       # n8n: Slack approval → publish
├── templates/
│   ├── linkedin-10.json        # 10 LinkedIn post templates
│   ├── instagram-10.json       # 10 IG post templates
│   ├── facebook-10.json        # 10 FB post templates
│   └── tiktok-10.json          # 10 TikTok templates
├── config/
│   ├── mixpost.yaml            # Mixpost platform config
│   ├── hashtags.yaml           # Recruitment hashtags + competitor profiles
│   └── isabella-retarget.yaml  # Isabella recruitment retarget
├── scripts/
│   ├── setup.sh                # One-command setup
│   ├── ai-citation-tracker.py  # Monthly AI citation check
│   └── analytics-dashboard.py  # Pull data from all platforms
├── docs/
│   ├── SETUP.md                # Full setup guide
│   ├── RUNBOOK.md              # Daily/weekly/monthly ops
│   ├── APPROVAL.md             # How Slack approval works
│   └── HANDOVER.md             # If Barry's team takes over
└── README.md
```

## What ships tonight
- [x] Docker Compose (Mixpost + n8n)
- [x] Blog-to-social n8n workflow
- [x] Trend discovery n8n workflow (Isabella retargeted)
- [x] Competitor monitor n8n workflow
- [x] Slack approval bot n8n workflow
- [x] 40 content templates (10 per platform)
- [x] Recruitment hashtag + profile config
- [x] AI citation tracker script
- [x] Analytics dashboard script
- [x] One-command setup script
- [x] Full documentation
- [x] Handover guide

## Deploy
```bash
cd barry-content-agent
cp .env.example .env
# fill in secrets
./scripts/setup.sh
```

## Status: BUILT ✅
