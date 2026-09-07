# Barry Content Agent — Deployment Status

**Deployed:** 2026-09-07  
**Deployed by:** Hermes Agent (automated)  
**Coolify project:** Barry Content Agent (uuid: `q56xwzjla0zvi1s09az8ioiv`)  
**Coolify service:** barry-content-agent (uuid: `u1024ohhkhkodkmebqloubev`)

## What's Live

### Mixpost (Social Media Scheduler)
- **URL:** http://mixpost.5.161.96.208.sslip.io/mixpost
- **Login URL:** http://mixpost.5.161.96.208.sslip.io/mixpost/login
- **Status:** Running, login page reachable (HTTP 200), dashboard accessible with credentials
- **Admin email:** barry@rentarecruiter.com
- **Admin password:** stored in macOS keychain (see Credentials below)
- **Version:** Mixpost Lite 2.6.0.0
- **Backend:** MySQL 8.0 + Redis (both running in the same Coolify service stack)

### n8n (Workflow Automation)
- **URL:** http://n8n.5.161.96.208.sslip.io
- **Health endpoint:** http://n8n.5.161.96.208.sslip.io/healthz → `{"status":"ok"}` (HTTP 200)
- **Login URL:** http://n8n.5.161.96.208.sslip.io (setup complete, owner account created)
- **Owner email:** barry@rentarecruiter.com
- **Owner password:** stored in macOS keychain (see Credentials below)
- **API key:** stored in macOS keychain (see Credentials below)
- **Version:** n8n 2.37.10

### n8n Workflows (4 imported, ALL INACTIVE)
| Workflow | n8n ID | Status |
|---|---|---|
| Blog-to-Social | `aB292jCfJsOdUuNp` | Inactive ✅ |
| Trend-Discovery | `GoGAXJL6eNFAmirX` | Inactive ✅ |
| Competitor-Monitor | `mAeAIS9BJuDxLdv8` | Inactive ✅ |
| Slack-Approval-Bot | `5dqKhUdCUy3vW7zb` | Inactive ✅ |

## Credentials (macOS Keychain)

All credentials stored via `security add-generic-password` in the login keychain.

| Keychain service name | Account | Purpose |
|---|---|---|
| `barry-mixpost-admin-login` | `barry@rentarecruiter.com` | Mixpost admin login (email + password) |
| `barry-mixpost-admin-password` | `hermes` | Mixpost admin password (generated) |
| `barry-mixpost-db-password` | `hermes` | Mixpost MySQL database password |
| `barry-mysql-root-password` | `hermes` | MySQL root password |
| `barry-mixpost-app-key` | `hermes` | Mixpost Laravel APP_KEY |
| `barry-n8n-password` | `hermes` | n8n owner password |
| `barry-n8n-api-key` | `hermes` | n8n public API key |
| `barry-n8n-encryption-key` | `hermes` | n8n encryption key |

**To retrieve any credential:**
```bash
security find-generic-password -a hermes -s <service-name> -w
# or for mixpost admin login:
security find-generic-password -a barry@rentarecruiter.com -s barry-mixpost-admin-login -w
```

## Health Check Proof

| Check | URL | Result |
|---|---|---|
| n8n healthz | http://n8n.5.161.96.208.sslip.io/healthz | HTTP 200, `{"status":"ok"}` |
| n8n login page | http://n8n.5.161.96.208.sslip.io/ | HTTP 200, title: "n8n.io - Workflow Automation" |
| n8n API (authenticated) | http://n8n.5.161.96.208.sslip.io/api/v1/workflows | HTTP 200, 4 workflows returned |
| Mixpost login page | http://mixpost.5.161.96.208.sslip.io/mixpost/login | HTTP 200, title: "Mixpost Auth - RAR Content Engine" |
| Mixpost dashboard (authenticated) | http://mixpost.5.161.96.208.sslip.io/mixpost | HTTP 200 (after login with barry@rentarecruiter.com) |

## What's Pending (and who owns each item)

### 1. Social Account Connections (Owner: Barry/Julieanne)
- IG, FB, TikTok, LinkedIn, X accounts need OAuth connection in Mixpost
- Requires app review for each platform (IG Professional + FB Page, TikTok Business, etc.)
- Mixpost → Settings → Social Accounts → Connect each platform
- **Cannot be automated** — requires Barry's sign-off and platform app reviews

### 2. LLM API Key (Owner: James)
- Workflows reference `$env.ANTHROPIC_API_KEY` and `$env.APIFY_API_TOKEN`
- DeepSeek key was mentioned as alternative; `DeepSeek_API_KEY` exists as a GitHub secret on TwinToneAI repos but was not reachable from this deployment context
- **Action needed:** Add `ANTHROPIC_API_KEY` (or DeepSeek equivalent) and `APIFY_API_TOKEN` as environment variables in the Coolify service, then redeploy
- Until this is done, workflows that call the LLM will fail at the "Generate Posts" / "Analyze Trends" / "Analyze Competitor" nodes

### 3. Barry's Approval to Activate (Owner: Barry)
- All 4 workflows are imported but INACTIVE — they will not run until activated
- Barry must review and approve the workflow designs before activation
- **Action:** Barry reviews workflows in n8n UI → gives go-ahead → James activates

### 4. Domain DNS (Owner: James)
- Currently using `*.5.161.96.208.sslip.io` wildcard (works for testing)
- Production should use `content.rentarecruiter.com` (Mixpost) and `n8n.content.rentarecruiter.com` (n8n)
- **Action:** Add A records pointing `content.rentarecruiter.com` and `n8n.content.rentarecruiter.com` to `5.161.96.208`, then update the Coolify service domains

### 5. Slack Webhook (Owner: James)
- `SLACK_WEBHOOK_URL` and `SLACK_CHANNEL_ID` need to be set for the approval bot and competitor monitor workflows
- **Action:** Create Slack app webhook for #content-approval channel, add as env var in Coolify

## Next 3 Steps for James

1. **Add API keys to Coolify service env vars:** Go to Coolify → Barry Content Agent → Environment Variables → add `ANTHROPIC_API_KEY` (or DeepSeek key), `APIFY_API_TOKEN`, `SLACK_WEBHOOK_URL`, `SLACK_CHANNEL_ID`, `MIXPOST_URL=http://mixpost.5.161.96.208.sslip.io`, `MIXPOST_API_TOKEN` (generate from Mixpost settings), `RAR_BLOG_RSS=https://rentarecruiter.com/feed/`, `COMPETITOR_IG_HANDLE=competitor1,competitor2,competitor3`. Then redeploy the service.

2. **Set up production domains:** Add DNS A records for `content.rentarecruiter.com` → `5.161.96.208` and `n8n.content.rentarecruiter.com` → `5.161.96.208`. Update the Coolify service's Traefik labels to use the production domains. Update `APP_URL` and `WEBHOOK_URL` env vars accordingly.

3. **Get Barry's approval + connect social accounts:** Walk Barry through the Mixpost UI (http://mixpost.5.161.96.208.sslip.io/mixpost) to connect IG/FB/TikTok/LinkedIn accounts. Then review the 4 n8n workflows together. Once approved, activate workflows in n8n (toggle Active on each).

## Infrastructure Details

- **Coolify instance:** http://5.161.96.208:8000 (TwinTone Coolify on Hetzner)
- **Server:** Hetzner CCX23 (5.161.96.208), Ashburn
- **Docker Compose stack:** 4 containers (mixpost, mixpost-db, redis, n8n) deployed as a single Coolify service
- **Network:** Coolify-managed Traefik reverse proxy with auto-assigned network
- **SSL:** Not configured yet (using HTTP with sslip.io wildcard for testing)

## Notes

- The `inovector/mixpost:latest` (Lite/free) image was used. The original project referenced Mixpost Pro ($299 one-time license). To upgrade, replace the image with `inovector/mixpost-pro-team:latest` and add the `LICENSE_KEY` env var.
- n8n was configured with `N8N_SECURE_COOKIE=false` to allow HTTP access. For production with HTTPS, set it back to `true`.
- The `N8N_BASIC_AUTH_*` env vars are set but n8n 2.x uses its own user management system. The basic auth vars are legacy and may not be needed.
