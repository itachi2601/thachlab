#!/bin/bash
# Dọn worktree phiên Claude để ổ Mac không đầy (sự cố 19/11/2026: còn 2 GB trống, worktree ~240 GB).
# Mỗi worktree là một bản mã nguồn ~0,6 GB + node_modules + .next (~0,6 GB/lần build).
#
#   bash scripts/don-worktree.sh            # xem trước: in việc sẽ làm, không xoá gì
#   bash scripts/don-worktree.sh --yes      # làm thật
#   NGAY=14 bash scripts/don-worktree.sh    # đổi ngưỡng "bỏ không" (mặc định 7 ngày)
#
# Làm 2 việc, chỉ với worktree KHÔNG có file nào sửa trong NGAY ngày qua (bỏ qua node_modules/.next)
# và không có tiến trình nào đang mở trong đó:
#   1. Worktree sạch (git status trống) → `git worktree remove` (không --force). Nhánh và commit vẫn
#      còn trong repo; phiên Claude mở lại sẽ tạo lại worktree.
#   2. Worktree còn thay đổi chưa commit → giữ nguyên mã, chỉ xoá .next (bản build, tạo lại được).
# Không bao giờ đụng checkout chính, worktree đang chạy, hay thay đổi chưa commit.
set -uo pipefail

LAM_THAT=0; [ "${1:-}" = "--yes" ] && LAM_THAT=1
NGAY="${NGAY:-7}"
ROOT="$(git rev-parse --path-format=absolute --git-common-dir 2>/dev/null)"; ROOT="${ROOT%/.git}"
WT="$ROOT/.claude/worktrees"
[ -d "$WT" ] || { echo "Không thấy $WT"; exit 1; }

# Worktree có tiến trình đang mở (dev server, phiên Claude đang chạy lệnh…)
dang_chay="$(lsof -Fn -d cwd 2>/dev/null | sed -n "s#^n$WT/\([^/]*\).*#\1#p" | sort -u)"

truoc=$(df -k "$WT" | awk 'NR==2{print $4}')
go=0; nhe=0; giu=0
for p in "$WT"/*/; do
  p="${p%/}"; w="$(basename "$p")"
  git -C "$p" rev-parse --git-dir >/dev/null 2>&1 || continue
  if echo "$dang_chay" | grep -qx "$w"; then giu=$((giu+1)); continue; fi
  # Có file sửa trong NGAY ngày qua → coi là đang dùng
  moi="$(find "$p" \( -name node_modules -o -name .next -o -name .git \) -prune -o -type f -mtime "-$NGAY" -print -quit 2>/dev/null)"
  if [ -n "$moi" ]; then giu=$((giu+1)); continue; fi

  trang_thai="$(git -C "$p" status --porcelain 2>/dev/null)" || continue   # thư mục vừa mất/lỗi → bỏ qua
  if [ -z "$trang_thai" ]; then
    echo "gỡ worktree sạch: $w ($(git -C "$p" branch --show-current))"
    if [ $LAM_THAT = 1 ]; then git -C "$ROOT" worktree remove "$p" && go=$((go+1)); else go=$((go+1)); fi
  elif [ -d "$p/.next" ] && [ ! -L "$p/.next" ]; then
    echo "giữ mã (còn thay đổi chưa commit), xoá .next: $w"
    if [ $LAM_THAT = 1 ]; then find "$p" -maxdepth 1 -name .next -type d -exec rm -rf {} +; fi
    nhe=$((nhe+1))
  else
    giu=$((giu+1))
  fi
done
[ $LAM_THAT = 1 ] && git -C "$ROOT" worktree prune

sau=$(df -k "$WT" | awk 'NR==2{print $4}')
echo "---"
echo "Gỡ $go worktree sạch · xoá .next ở $nhe worktree còn thay đổi · giữ $giu (đang dùng trong $NGAY ngày hoặc đang chạy)"
if [ $LAM_THAT = 1 ]; then
  echo "Trống: $((truoc/1048576)) GB → $((sau/1048576)) GB"
else
  echo "Đây là XEM TRƯỚC. Làm thật: bash scripts/don-worktree.sh --yes"
fi
