#!/usr/bin/env bash
# Đẩy CHỈ nội dung lý thuyết của một bài (không đụng đề, bài tập mẫu, tiêu đề, tiến độ học).
#   bash scripts/cap-nhat-ly-thuyet.sh <theory.html | bundle.json> <lesson_id> [--yes] [--chi-video] [--cho-phep-khac]
# Chạy trên Mac: pull main → xem thử (dry-run, tự sao lưu) → hỏi xác nhận → ghi → nhắc deploy.
#
# --chi-video: dùng khi BỒI DẶP video vào bài ĐÃ ĐĂNG — chỉ ghi nếu phần NGOÀI khối video giống hệt
#   bản đang có trong DB (chặn ghi đè mất bản sửa trực tiếp trên web). Chủ ý ghi đè: --cho-phep-khac.
#
# QUY TẮC (thầy chốt 4/10/2026): đăng bài lý thuyết CHỈ ghi mục Lý thuyết của đúng bài đó, không làm
# ảnh hưởng phần còn lại của bài (Luyện tập, Kiểm tra, Bài tập mẫu…) hay bài khác. Script không tin
# vào việc người chạy nhớ quy tắc: `update-ly-thuyet-from-bundle.mts` lọc đúng mục kind='ly_thuyet',
# in phạm vi ở bước dry-run, ràng buộc UPDATE bằng cả id lẫn kind, rồi chụp lesson_items TRƯỚC/SAU và
# tự báo lỗi (exit 1) nếu có bất kỳ cột/mục nào khác đổi. Đừng thay bằng upload-lesson.mts (script đó
# ghi cả đề Luyện tập).
set -euo pipefail
cd "$(dirname "$0")/.."
SRC="${1:-}"; LESSON="${2:-}"
[[ -f "$SRC" && -n "$LESSON" ]] || { echo "Dùng: bash scripts/cap-nhat-ly-thuyet.sh <theory.html|bundle.json> <lesson_id> [--yes] [--chi-video] [--cho-phep-khac]"; exit 1; }
shift 2 || true

YES=""
EXTRA=""
for a in "$@"; do
  case "$a" in
    --yes) YES="--yes" ;;
    --chi-video|--cho-phep-khac|--with-title) EXTRA="$EXTRA $a" ;;
    *) echo "✗ cờ không nhận: $a"; exit 1 ;;
  esac
done

if [[ "$SRC" == *.html ]]; then python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_theory.py "$SRC"; fi
echo "── Xem thử (chưa ghi) ──"
# shellcheck disable=SC2086
npx tsx scripts/update-ly-thuyet-from-bundle.mts "$SRC" --lesson "$LESSON" --dry-run $EXTRA
if [[ "$YES" != "--yes" ]]; then read -r -p "Ghi đè Lý thuyết bài $LESSON? [y/N] " a; [[ "$a" == "y" || "$a" == "Y" ]] || { echo "Dừng."; exit 0; }; fi
# shellcheck disable=SC2086
npx tsx scripts/update-ly-thuyet-from-bundle.mts "$SRC" --lesson "$LESSON" $EXTRA
echo "Hoàn tác nếu hỏng: npx tsx scripts/khoi-phuc-ly-thuyet.mts <file sao lưu in ở trên>"
echo "Nếu CSS .tl-* vừa đổi thì mới cần: bash scripts/deploy.sh"
