#!/usr/bin/env bash
# Ghi nội dung HSG KHTN 9 đợt 2 — mảng Điện (CĐ03=159, CĐ04=157, CĐ05=165): lý thuyết + bài tập mẫu.
# Bài 157/159/165 đã có trong DB (migration 20261010100000). Mỗi bước tự sao lưu ra scripts/logs/.
#   bash scripts/dang-hsg9-dot2.sh [--yes]
set -euo pipefail
cd "$(dirname "$0")/.."
Y="${1:-}"
for pair in "cd03-dien-tro-dinh-luat-ohm:159" "cd04-mach-noi-tiep-song-song:157" "cd05-cong-suat-dien-joule-lenz:165"; do
  d="${pair%%:*}"; id="${pair##*:}"
  echo "══ CĐ $d (bài $id) ══"
  bash scripts/cap-nhat-ly-thuyet.sh "content/hsg9/$d/theory.html" "$id" $Y
  npx tsx scripts/publish-bai-tap-mau.mts --lesson "$id" $Y
done
echo "Xong. Deploy để bài tập mẫu (file tĩnh) lên web: bash scripts/deploy.sh"
