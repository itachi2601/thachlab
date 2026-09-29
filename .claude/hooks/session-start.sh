#!/bin/bash
# SessionStart hook — CHỈ chạy trên Claude Code cloud (CLAUDE_CODE_REMOTE=true).
# Việc 1: cài npm để lint/tsc chạy được. Việc 2: in tình hình đồng bộ cloud↔Mac để phiên
# không làm trên nền cũ. Hook lỗi không được chặn phiên → luôn exit 0 ở phần báo cáo.
set -uo pipefail

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0
cd "${CLAUDE_PROJECT_DIR:-.}"

# --- 1. Phụ thuộc ---------------------------------------------------------
if [ -f package.json ]; then
  npm install --no-audit --no-fund --loglevel=error >/dev/null 2>&1 \
    || echo "⚠ npm install lỗi — chạy tay: npm install"
fi

# --- 2. Tình hình đồng bộ ------------------------------------------------
git fetch origin --prune --quiet 2>/dev/null || { echo "⚠ git fetch lỗi — số liệu dưới đây có thể cũ"; }

base="origin/main"
git rev-parse --verify --quiet "$base" >/dev/null || exit 0
cur="$(git rev-parse --abbrev-ref HEAD)"

echo "=== ĐỒNG BỘ CLOUD ↔ MAC ($(date +%F)) ==="
echo "Nhánh hiện tại: $cur"
behind=$(git rev-list --count "HEAD..$base" 2>/dev/null || echo "?")
ahead=$(git rev-list --count "$base..HEAD" 2>/dev/null || echo "?")
echo "So với origin/main: hơn $ahead commit, thiếu $behind commit"
[ "$behind" != "0" ] && [ "$behind" != "?" ] && echo "  → main có việc mới (thường từ Mac). Merge trước khi làm: git merge origin/main"

# Nhánh claude/* hoạt động 7 ngày gần đây mà còn commit chưa vào main. Nhánh cũ bị bỏ qua vì PR
# squash-merge khiến số commit luôn "chưa vào main" dù việc đã xong.
others=""
since=$(date -d '7 days ago' +%s 2>/dev/null || echo 0)
for b in $(git for-each-ref --format='%(refname:short)' 'refs/remotes/origin/claude/*'); do
  [ "$b" = "origin/$cur" ] && continue
  [ "$(git log -1 --format=%ct "$b")" -lt "$since" ] && continue
  n=$(git rev-list --count "$base..$b" 2>/dev/null || echo 0)
  [ "$n" -gt 0 ] && others="$others\n  - ${b#origin/}: $n commit chưa vào main (nếu đã squash-merge qua PR thì bỏ qua)"
done
[ -n "$others" ] && printf "Nhánh cloud gần đây khác chưa thấy trong main:%b\n" "$others"

# Migration nằm ở nhánh này/nhánh khác nhưng chưa vào main = chưa thể chạy trên production
pend=$(git diff --name-only "$base"...HEAD -- supabase/migrations 2>/dev/null)
[ -n "$pend" ] && printf "Migration mới ở nhánh này (chưa vào main):\n%s\n" "$(echo "$pend" | sed 's/^/  - /')"

echo "Mục ĐANG CHỜ trong docs/STATE.md:"
sed -n '/^## Migration — ĐANG CHỜ/,/^## /p' docs/STATE.md | sed '1d;$d' | head -12 | sed 's/^/  /'

echo "Nhắc: cloud KHÔNG chạy được migration/đăng đề/backfill (Supabase bị chặn) — viết file + lệnh rồi dừng."
echo "Memory dự án: docs/memory/MEMORY.md. Cuối phiên: /ban-giao."
exit 0
