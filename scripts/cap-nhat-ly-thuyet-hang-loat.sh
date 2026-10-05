#!/usr/bin/env bash
# Đăng lý thuyết NHIỀU bài trong một lượt (mỗi bài vẫn chỉ ghi đúng mục Lý thuyết của bài đó),
# rồi nhắc deploy MỘT lần — thay vì chạy cap-nhat-ly-thuyet.sh rồi deploy từng bài.
#
#   bash scripts/cap-nhat-ly-thuyet-hang-loat.sh <slug>:<lesson_id> [<slug>:<lesson_id> ...] [--yes]
# Ví dụ:
#   bash scripts/cap-nhat-ly-thuyet-hang-loat.sh l11-giao-thoa-song:31 l11-song-dung:32 --yes
#
# Chạy TRÊN MAC (Supabase bị chặn ở sandbox). Mặc định từng bài vẫn hỏi xác nhận;
# thêm --yes để chạy thẳng. Dừng ngay khi một bài lỗi. Sao lưu nằm trong scripts/logs/.
set -euo pipefail
cd "$(dirname "$0")/.."

YES=""
PAIRS=()
for a in "$@"; do
  if [[ "$a" == "--yes" ]]; then YES="--yes"; else PAIRS+=("$a"); fi
done
[[ ${#PAIRS[@]} -gt 0 ]] || { echo "Dùng: bash scripts/cap-nhat-ly-thuyet-hang-loat.sh <slug>:<lesson_id> [...] [--yes]"; exit 1; }

LOGDIR="scripts/logs"
mkdir -p "$LOGDIR"
STAMP="$(date +%Y%m%d-%H%M%S)"
SUMMARY="$LOGDIR/dang-ly-thuyet-hang-loat-$STAMP.log"
: > "$SUMMARY"

for pair in "${PAIRS[@]}"; do
  SLUG="${pair%%:*}"; LESSON="${pair##*:}"
  if [[ "$SLUG" == "$pair" || -z "$LESSON" ]]; then
    echo "✗ '$pair' sai dạng — cần <slug>:<lesson_id>"; exit 1
  fi
  THEORY="content/lesson-samples/$SLUG/theory.html"
  if [[ ! -f "$THEORY" ]]; then echo "✗ Không thấy $THEORY"; exit 1; fi
  if [[ ! "$LESSON" =~ ^[0-9]+$ ]]; then echo "✗ lesson_id '$LESSON' phải là số"; exit 1; fi

  echo "════ Bài $SLUG → lesson $LESSON ════"
  bash scripts/cap-nhat-ly-thuyet.sh "$THEORY" "$LESSON" $YES
  echo "$SLUG:$LESSON ok $(date +%H:%M:%S)" >> "$SUMMARY"
done

echo
echo "── Xong ${#PAIRS[@]} bài (nhật ký: $SUMMARY) ──"
echo "Giờ deploy MỘT lần từ worktree sạch:"
echo "  git -C .claude/worktrees/deploy-tree checkout --detach origin/main && (cd .claude/worktrees/deploy-tree && bash scripts/deploy.sh)"
