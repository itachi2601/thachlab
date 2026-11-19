#!/usr/bin/env bash
# Dựng cả quyển ruột tập VL10 Chương 5 Động lượng (bài 28–30, lesson 73–75, 36 trang, đánh số liền mạch)
# → scripts/ruot-tap/out/ruot-tap-vl10-chuong5.pdf
# Mỗi bài: scripts/ruot-tap/l10-bai<N>.mjs (khung.mjs với lop:10, baiDau:28, tuongTu → bố cục bài 14) + hinh-l10-bai<N>.mjs.
# Bài nào chưa có file thì bỏ qua (các phiên song song gộp dần vào main).
set -euo pipefail
cd "$(dirname "$0")/../.."
co=()
for n in 28 29 30; do
  f=scripts/ruot-tap/l10-bai$n.mjs
  if [ ! -f "$f" ]; then echo "· bài $n: chưa có $f — bỏ qua"; continue; fi
  node "$f" | grep -E "dư -[2-9]|dư -[0-9][0-9]|katexErr=[1-9]|→" || true
  co+=("scripts/ruot-tap/out/ruot-tap-vl10-bai$n.pdf")
done
[ ${#co[@]} -ge 2 ] || { echo "cần ≥ 2 bài để ghép quyển"; exit 0; }
pdfunite "${co[@]}" scripts/ruot-tap/out/ruot-tap-vl10-chuong5.pdf
pdfinfo scripts/ruot-tap/out/ruot-tap-vl10-chuong5.pdf | grep Pages
pdffonts scripts/ruot-tap/out/ruot-tap-vl10-chuong5.pdf | grep -iE "helvetica|lucida|hiragino|arial" && echo "! CẢNH BÁO: còn font hệ thống" || true
