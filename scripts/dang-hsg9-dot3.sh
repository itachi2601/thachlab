#!/usr/bin/env bash
# Ghi nội dung HSG KHTN 9 đợt 3 — mảng Nhiệt – âm: lý thuyết + bài tập mẫu.
# Cần migration 20261016130000 (tạo mục rỗng cho 150, 153, 164). Mỗi bước tự sao lưu ra scripts/logs/.
#   bash scripts/dang-hsg9-dot3.sh [--yes] [cd15-am-thanh:150 …]   (không truyền cặp nào = mọi CĐ đã soạn của đợt)
set -euo pipefail
cd "$(dirname "$0")/.."
Y=""; PAIRS=()
for a in "$@"; do [ "$a" = "--yes" ] && Y="--yes" || PAIRS+=("$a"); done
[ ${#PAIRS[@]} -eq 0 ] && PAIRS=("cd15-am-thanh:150")
for pair in "${PAIRS[@]}"; do
  d="${pair%%:*}"; id="${pair##*:}"
  echo "══ CĐ $d (bài $id) ══"
  bash scripts/cap-nhat-ly-thuyet.sh "content/hsg9/$d/theory.html" "$id" $Y
  npx tsx scripts/publish-bai-tap-mau.mts --lesson "$id" $Y
done
echo "Xong. Deploy để bài tập mẫu (file tĩnh) lên web: bash scripts/deploy.sh"
