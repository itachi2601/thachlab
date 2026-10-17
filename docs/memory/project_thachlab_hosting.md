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

**Deploy từ worktree sạch (11/10/2026):** cây chính thường dở dang nên không chạy `deploy.sh` ở đó. Cách làm: `git worktree add --detach <thư mục trong scratchpad> <commit>`, `cp .env.local` vào, `cp -cR node_modules` (KHÔNG symlink — Turbopack báo "Symlink node_modules is invalid"), rồi chạy `bash <worktree>/scripts/deploy.sh` trong tab terminal (~3 phút), xong `git worktree remove --force`.

**Sự cố 16–17/10/2026 — web đứng ở bản 16/10 23:11:** hosting hết quota ("Disk quota exceeded"); mỗi phút cron `git fetch` tải dở để lại `.git/objects/pack/tmp_pack_*` (55 file, 1,6 GB) → càng đầy. Sửa bằng Terminal DirectAdmin (`/evo/user/terminal`, thư mục `~/domains/thachlab.id.vn/public_html`): xoá `tmp_pack_*`, fetch + reset, rồi `git reflog expire --expire=now --all && git gc --prune=now` → 2,2 GB còn 114 MB. Web không lên bản mới thì kiểm quota trước. Mỗi lần deploy force-push để lại bản cũ trong git hosting → nên gc định kỳ (thêm `&& git gc --auto -q` vào cron khi thầy đồng ý). Cron hiện thiếu `git clean -fdx` mà `scripts/deploy.sh` khuyến nghị.
