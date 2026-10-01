#!/bin/bash
# SessionStart hook — CHỈ chạy trên Claude Code cloud (CLAUDE_CODE_REMOTE=true).
# Việc 1: cài npm để lint/tsc chạy được. Việc 2: in tình hình đồng bộ cloud↔Mac để phiên
# không làm trên nền cũ. Hook lỗi không được chặn phiên → luôn exit 0 ở phần báo cáo.
set -uo pipefail

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0
cd "${CLAUDE_PROJECT_DIR:-.}"

# --- 1. Phụ thuộc ---------------------------------------------------------
if [ -f package.json ]; then
  # npm ci: cài đúng package-lock.json, không ghi đè lockfile (npm install trên Linux làm bẩn
  # lock do Mac tạo). Bỏ qua nếu node_modules đã có (container đã cache).
  if [ ! -d node_modules ]; then
    if [ -f package-lock.json ]; then cmd="npm ci"; else cmd="npm install"; fi
    $cmd --no-audit --no-fund --loglevel=error >/dev/null 2>&1 \
      || echo "⚠ $cmd lỗi — chạy tay: $cmd"
  fi
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

# Kiểm khả năng ghi DB từ cloud: cần (1) mạng cho phép *.supabase.co, (2) secret SUPABASE_SERVICE_ROLE_KEY.
url="${NEXT_PUBLIC_SUPABASE_URL:-https://jgvbdbpvjdntdgzthumv.supabase.co}"
code=$(curl -s -o /dev/null -m 6 -w '%{http_code}' "$url/rest/v1/" 2>/dev/null || echo 000)
if [ "$code" = "000" ] || [ "$code" = "403" ]; then net=chặn; else net=thông; fi
if [ -n "${SUPABASE_SERVICE_ROLE_KEY:-}" ]; then key=có; else key=thiếu; fi
if [ "$net" = "thông" ] && [ "$key" = "có" ]; then
  echo "Supabase: mạng $net, service key $key → ĐĂNG/SỬA BÀI ĐƯỢC từ cloud (upload-lesson.mts, update-*.mts). Migration vẫn chỉ chạy trên Mac."
else
  echo "Supabase: mạng $net (HTTP $code), service key $key → cloud CHƯA đăng/sửa được; viết file + lệnh rồi dừng. Cách bật: docs/CLOUD-GHI-DB.md"
fi
echo "Memory dự án: docs/memory/MEMORY.md. Cuối phiên: /ban-giao."
exit 0
