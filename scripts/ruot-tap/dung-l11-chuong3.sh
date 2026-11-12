#!/usr/bin/env bash
# Dựng cả quyển ruột tập VL11 Chương 3 Điện trường (bài 16–21, lesson 35–40, 72 trang, đánh số liền mạch)
# → scripts/ruot-tap/out/ruot-tap-vl11-chuong3.pdf
# Mỗi bài: scripts/ruot-tap/l11-bai<N>.mjs (khung.mjs với lop:11, baiDau:16, tuongTu → bố cục bài 14) + hinh-l11-bai<N>.mjs.
# Bài nào chưa có file thì bỏ qua (các phiên song song gộp dần vào main).
set -euo pipefail
cd "$(dirname "$0")/../.."
co=()
for n in 16 17 18 19 20 21; do
  f=scripts/ruot-tap/l11-bai$n.mjs
  if [ ! -f "$f" ]; then echo "· bài $n: chưa có $f — bỏ qua"; continue; fi
  node "$f" | grep -E "dư -[2-9]|dư -[0-9][0-9]|katexErr=[1-9]|→" || true
  co+=("scripts/ruot-tap/out/ruot-tap-vl11-bai$n.pdf")
done
[ ${#co[@]} -ge 2 ] || { echo "cần ≥ 2 bài để ghép quyển"; exit 0; }
pdfunite "${co[@]}" scripts/ruot-tap/out/ruot-tap-vl11-chuong3.pdf
pdfinfo scripts/ruot-tap/out/ruot-tap-vl11-chuong3.pdf | grep Pages
pdffonts scripts/ruot-tap/out/ruot-tap-vl11-chuong3.pdf | grep -iE "helvetica|lucida|hiragino|arial" && echo "! CẢNH BÁO: còn font hệ thống" || true
