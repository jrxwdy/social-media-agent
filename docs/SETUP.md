# Setup Guide — Barry Content Agent

## What you're deploying
- **Mixpost**: Self-hosted social media scheduler. Connects to IG, FB, TikTok, LinkedIn, X. Has built-in MCP server so the agent drives it.
- **n8n**: Workflow automation. Runs the blog-to-social, trend discovery, competitor monitoring, and approval workflows.

## Prerequisites
- Docker + Docker Compose
- A server (Hetzner/Coolify, or run locally)
- Domain (optional but recommended: `content.rentarecruiter.com`)
- API keys:
  - Anthropic (Claude) — for content generation
  - Apify — for trend discovery + competitor monitoring
  - Upload-Post — for multi-platform publishing
  - Slack — for approval workflow

## Quick Start

```bash
cd barry-content-agent
cp .env.example .env
# Edit .env with your keys
./scripts/setup.sh
```

That's it. This deploys Mixpost + n8n, imports workflows, and runs health checks.

## Step-by-step

### 1. Fill in `.env`
Minimum required:
```
ANTHROPIC_API_KEY=sk-ant-your-key
APIFY_API_TOKEN=apify_api_your_token
UPLOAD_POST_API_KEY=your-upload-post-key
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK
```

### 2. Run setup
```bash
./scripts/setup.sh
```

### 3. Open n8n
- URL: http://localhost:5678 (or your domain)
- Login with `N8N_USER` / `N8N_PASSWORD` from .env

### 4. Import workflows
If auto-import failed, manually import these from the `workflows/` folder:
- `blog-to-social.json` — triggers on new blog post, generates 3 platform drafts
- `trend-discovery.json` — every 6hrs, finds trending recruitment content
- `competitor-monitor.json` — weekly competitor report
- `slack-approval-bot.json` — Slack approve/edit/reject

### 5. Open Mixpost
- URL: http://localhost:8080 (or your domain)
- Complete setup wizard
- Connect IG, FB, TikTok, LinkedIn, X accounts

### 6. Test
Create a test post in Mixpost → send to Slack approval → approve → verify it publishes.

## Connecting social accounts

### Instagram
1. Must be an Instagram Professional account
2. Connected to a Facebook Page
3. In Mixpost: Settings → Accounts → Add Instagram → OAuth flow

### Facebook
1. Facebook Page (not personal profile)
2. Admin access required
3. In Mixpost: Settings → Accounts → Add Facebook → OAuth flow

### TikTok
1. TikTok Business account
2. In Mixpost: Settings → Accounts → Add TikTok → OAuth flow

### LinkedIn
1. Personal profile or company page
2. In Mixpost: Settings → Accounts → Add LinkedIn → OAuth flow

## Troubleshooting

| Problem | Fix |
|---|---|
| n8n import fails | Import manually via n8n UI (Workflows → Import) |
| Mixpost won't start | Check `docker logs barry-mixpost` — usually DB connection timeout, just retry |
| Slack not receiving | Verify `SLACK_WEBHOOK_URL` in .env |
| Instagram auth fails | Must be Professional account connected to FB Page |

## Security notes
- All secrets in `.env` — never commit to git
- n8n has basic auth enabled
- Mixpost runs on localhost by default — use a reverse proxy (Caddy/nginx) for HTTPS
- Back up `n8n-data` and `mixpost-storage` volumes regularly

## Support
See `docs/RUNBOOK.md` for daily operations.
See `docs/HANDOVER.md` if Barry's team takes over.
