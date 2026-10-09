#!/usr/bin/env bash
# Ghi nội dung HSG KHTN 9 đợt 1 (CĐ13=162, CĐ10=155, CĐ11=154, CĐ00=160): lý thuyết + bài tập mẫu.
# Chạy SAU migration 20261010200000. Mỗi bước tự sao lưu ra scripts/logs/ và dừng khi lỗi.
#   bash scripts/dang-hsg9-dot1.sh [--yes]
set -euo pipefail
cd "$(dirname "$0")/.."
Y="${1:-}"
for pair in "cd13-chuyen-dong-va-do-thi:162" "cd10-luc:155" "cd11-co-hoc-chat-luu:154" "cd00-ky-nang-nen:160"; do
  d="${pair%%:*}"; id="${pair##*:}"
  echo "══ CĐ $d (bài $id) ══"
  bash scripts/cap-nhat-ly-thuyet.sh "content/hsg9/$d/theory.html" "$id" $Y
  npx tsx scripts/publish-bai-tap-mau.mts --lesson "$id" $Y
done
echo "Xong. Xem trên web sau khi chạy: bash scripts/deploy.sh (nội dung bài tập mẫu là file tĩnh)."
