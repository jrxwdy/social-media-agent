# Handover Guide — Barry Content Agent

## For: Barry's team (Julieanne or future hire)
## From: James Rowdy / TwinTone

## What you own
- Mixpost instance (self-hosted on your server)
- n8n workflows (blog-to-social, trend discovery, competitor monitor, approval bot)
- All connected social accounts
- All credentials and API keys
- 40 content templates
- AI citation tracker
- This documentation

## What you need to know

### Daily (5 min)
1. Open Slack → #content-approval channel
2. Review pending posts (they'll have ✅ Approve / ✏️ Edit / ❌ Reject buttons)
3. Click approve on anything you're happy with
4. If you don't act within 24 hours, posts auto-approve

### Weekly (30 min, Monday)
1. Check the competitor report in Slack (auto-posted every Monday 9am)
2. Review the trend discovery queue in Mixpost
3. Make sure the week's content mix looks right (not all one type)

### Monthly (1 hour)
1. Run the AI citation tracker:
   ```bash
   cd barry-content-agent
   python scripts/ai-citation-tracker.py --month 2026-09 --output report.md
   ```
2. Review follower growth, engagement, top posts
3. Send Barry the monthly report (template in docs/RUNBOOK.md)

## How to log in

| Service | URL | Credentials |
|---|---|---|
| Mixpost | https://content.rentarecruiter.com | Set during setup |
| n8n | https://n8n.content.rentarecruiter.com | In .env file |
| Slack | Your workspace | #content-approval channel |

## How to add a new team member
1. In Mixpost: Settings → Team → Invite
2. In n8n: Settings → Users → Invite
3. In Slack: Add to #content-approval channel

## How to change content templates
1. Open `templates/` folder
2. Edit the JSON file for the platform (e.g., `linkedin-10.json`)
3. Changes apply to new posts immediately
4. Existing scheduled posts won't change

## How to add a competitor to monitor
1. Open `config/hashtags.yaml`
2. Add under `profiles:` section:
   ```yaml
   - handle: competitor_handle
     platform: instagram
     notes: What they do
   ```
3. Restart n8n: `docker-compose restart n8n`

## How to pause all posting
1. Open n8n → Workflows
2. Toggle off all 4 workflows
3. Posts in Mixpost queue won't publish until you toggle back on

## How to change posting times
1. Open `config/mixpost.yaml`
2. Edit `posting_times` for each platform
3. Restart: `docker-compose restart mixpost`

## Troubleshooting

| Problem | Fix |
|---|---|
| Posts not publishing | Check Mixpost → Calendar → look for red/failed |
| Slack not getting approvals | Check `SLACK_WEBHOOK_URL` in .env, restart n8n |
| n8n workflow errors | Open n8n → Executions → see error details |
| Instagram auth expired | Re-connect in Mixpost → Settings → Accounts |
| Need to stop everything | `docker-compose stop` (pauses all services) |

## Backups
- `n8n-data` volume = all workflows + execution history
- `mixpost-storage` volume = all posts, media, settings
- Back up weekly: `docker-compose exec n8n n8n export:workflow --all`

## When to call James
- Platform API changes break workflows
- Need new features (YouTube, Pinterest, etc.)
- Want to add another client/brand to the same instance
- Major strategy pivot

## When to handle it yourself
- Approving/rejecting posts
- Changing templates
- Adding competitors
- Monthly reports
- Content mix adjustments

## The .env file
This is the keys to the kingdom. It contains:
- API keys (Anthropic, Apify, Upload-Post)
- Database passwords
- Slack webhook
- Social account access

**Keep it safe. Don't commit to git. Don't share.**

## Cost breakdown (what you're paying for)

| Service | Cost | Why |
|---|---|---|
| Mixpost Pro | $299 one-time | Self-hosted scheduler |
| Upload-Post | $24-50/mo | Multi-platform publishing |
| Apify | ~$4/mo | Trend + competitor scraping |
| Server (Hetzner) | ~$10/mo | Docker hosting |
| **Total** | **~$40-65/mo** | **+ James's management fee** |

## The deal
- You own everything
- No lock-in
- Cancel anytime
- Source code: [link to repo]
- Support: [email]

---

**You've got this. The system does 90% of the work. You just steer.**
