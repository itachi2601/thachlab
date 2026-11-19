#!/usr/bin/env bash
# Dựng cả quyển ruột tập VL11 Chương 4 Dòng điện. Mạch điện (bài 22–26, lesson 41–45, 60 trang, đánh số liền mạch)
# → scripts/ruot-tap/out/ruot-tap-vl11-chuong4.pdf
# Mỗi bài: scripts/ruot-tap/l11-bai<N>.mjs (khung.mjs với lop:11, baiDau:22, tuongTu → bố cục bài 14) + hinh-l11-bai<N>.mjs.
# Bài nào chưa có file thì bỏ qua (các phiên song song gộp dần vào main).
set -euo pipefail
cd "$(dirname "$0")/../.."
co=()
for n in 22 23 24 25 26; do
  f=scripts/ruot-tap/l11-bai$n.mjs
  if [ ! -f "$f" ]; then echo "· bài $n: chưa có $f — bỏ qua"; continue; fi
  node "$f" | grep -E "dư -[2-9]|dư -[0-9][0-9]|katexErr=[1-9]|→" || true
  co+=("scripts/ruot-tap/out/ruot-tap-vl11-bai$n.pdf")
done
[ ${#co[@]} -ge 2 ] || { echo "cần ≥ 2 bài để ghép quyển"; exit 0; }
pdfunite "${co[@]}" scripts/ruot-tap/out/ruot-tap-vl11-chuong4.pdf
pdfinfo scripts/ruot-tap/out/ruot-tap-vl11-chuong4.pdf | grep Pages
pdffonts scripts/ruot-tap/out/ruot-tap-vl11-chuong4.pdf | grep -iE "helvetica|lucida|hiragino|arial" && echo "! CẢNH BÁO: còn font hệ thống" || true
