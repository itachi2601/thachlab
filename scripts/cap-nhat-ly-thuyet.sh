#!/usr/bin/env bash
# Đẩy CHỈ nội dung lý thuyết của một bài (không đụng đề, bài tập mẫu, tiêu đề, tiến độ học).
#   bash scripts/cap-nhat-ly-thuyet.sh <theory.html | bundle.json> <lesson_id> [--yes]
# Chạy trên Mac: pull main → xem thử (dry-run, tự sao lưu) → hỏi xác nhận → ghi → nhắc deploy.
set -euo pipefail
cd "$(dirname "$0")/.."
SRC="${1:-}"; LESSON="${2:-}"; YES="${3:-}"
[[ -f "$SRC" && -n "$LESSON" ]] || { echo "Dùng: bash scripts/cap-nhat-ly-thuyet.sh <theory.html|bundle.json> <lesson_id> [--yes]"; exit 1; }
if [[ "$SRC" == *.html ]]; then python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_theory.py "$SRC"; fi
echo "── Xem thử (chưa ghi) ──"
npx tsx scripts/update-ly-thuyet-from-bundle.mts "$SRC" --lesson "$LESSON" --dry-run
if [[ "$YES" != "--yes" ]]; then read -r -p "Ghi đè Lý thuyết bài $LESSON? [y/N] " a; [[ "$a" == "y" || "$a" == "Y" ]] || { echo "Dừng."; exit 0; }; fi
npx tsx scripts/update-ly-thuyet-from-bundle.mts "$SRC" --lesson "$LESSON"
echo "Hoàn tác nếu hỏng: npx tsx scripts/khoi-phuc-ly-thuyet.mts <file sao lưu in ở trên>"
echo "Nếu CSS .tl-* vừa đổi thì mới cần: bash scripts/deploy.sh"
