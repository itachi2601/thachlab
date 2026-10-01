---
name: project-thachlab-hosting
description: "ThachLab hosting/domain setup — where it lives and how it's meant to be deployed"
metadata: 
  node_type: memory
  type: project
  originSessionId: aeb6fa12-c91e-4887-bd44-21b55ca287ba
---

ThachLab (Next.js 16 app) is intended to be deployed to the custom domain **Thachlab.id.vn**, purchased by the user. Hosting is a control panel at `https://cda009.secureweb.vn:2222/evo/` — looks like DirectAdmin (port 2222, "evo" skin), Vietnamese provider. Confirmed to support Node.js apps via a Node Selector/Passenger-style feature, so the Next.js server can run directly rather than needing a static export.

**Why:** User wants full site management handed to Claude — bring requirements, Claude implements and (per [[feedback_deploy_autonomy]]) deploys tested changes to production without asking each time.

**Current state (2026-07-06):**
- DNS: thachlab.id.vn → 150.95.109.197 (correct, already pointing at the hosting).
- Hosting is **LiteSpeed shared hosting** (PHP-oriented, DirectAdmin user `hd0dd7f3a7`) — despite the user's earlier guess, treat Node.js server support as unavailable; the chosen deploy path is **Next.js static export** (`output: "export"` in next.config.ts, build produces `out/`, ~1.4MB). Verified the export builds and serves correctly.
- A throwaway WordPress test site currently occupies the domain's public_html — user confirmed it can be replaced, no backup needed.
- SSL: domain still serves the server's default cert (CN=cda009.secureweb.vn); needs a Let's Encrypt cert issued via DirectAdmin SSL section.
- SSH: **externally blocked, permanently** — provider (TenTen.vn / secureweb.vn, support confirmed 2026-07-06) does not allow outside SSH connections for security; only a web-based Terminal inside the DirectAdmin panel. The deploy keypair at `~/.ssh/thachlab_deploy(.pub)` + Authorized Keys entry are therefore useless for direct connection — don't retry SSH ports.
- User pasted their DirectAdmin password in chat once — Claude refused to use it and advised changing it.

**How to apply — automated deploy is LIVE (verified end-to-end 2026-07-06):** run `./scripts/deploy.sh` from the repo root. It builds the static export, writes an `.htaccess` (blocks `/.git`, long-cache for hashed assets), and force-pushes a single-commit `deploy` branch to the public repo `github.com/itachi2601/thachlab`. On the hosting, public_html is a git checkout of that branch and a DirectAdmin Cron Job (every 10 min, at :00/:10/:20...) runs `git fetch origin deploy && git reset --hard origin/deploy`. So: deploy = run the script, site updates within ≤10 minutes — no user action needed per deploy. Verify afterward via `curl -sI https://thachlab.id.vn/ | grep -i last-modified`. Source lives on `main` (push normally). SSL: Let's Encrypt cert issued for the domain, auto-renews.
