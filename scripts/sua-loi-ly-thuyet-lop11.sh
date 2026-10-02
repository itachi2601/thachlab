#!/usr/bin/env bash
# Đẩy 12 bài lý thuyết lớp 11 đã sửa lỗi nguồn (content/sua-loi-ly-thuyet/<id>.html). Chỉ ghi body_html, tự sao lưu ra scripts/logs/.
#   bash scripts/sua-loi-ly-thuyet-lop11.sh [--dry-run | --yes]
set -euo pipefail
cd "$(dirname "$0")/.."
for id in 24 25 27 30 31 34 35 36 37 38 39 40; do
  f="content/sua-loi-ly-thuyet/$id.html"
  if [[ "${1:-}" == "--dry-run" ]]; then npx tsx scripts/update-ly-thuyet-from-bundle.mts "$f" --lesson "$id" --dry-run
  else bash scripts/cap-nhat-ly-thuyet.sh "$f" "$id" ${1:-}; fi
done
echo "Xong. Hoàn tác từng bài: npx tsx scripts/khoi-phuc-ly-thuyet.mts <file sao lưu>. Rồi: bash scripts/deploy.sh"
