#!/usr/bin/env bash
# Dựng cả quyển ruột tập VL12 Chương 1 Vật lí nhiệt (bài 1–4, lesson 2–5, 48 trang, đánh số liền mạch)
# → scripts/ruot-tap/out/ruot-tap-vl12-chuong1.pdf
# Mỗi bài: scripts/ruot-tap/l12-bai<N>.mjs (khung.mjs với lop:12, baiDau:1, tuongTu → bố cục bài 14) + hinh-l12-bai<N>.mjs.
# Bài nào chưa có file thì bỏ qua (các phiên song song gộp dần vào main).
set -euo pipefail
cd "$(dirname "$0")/../.."
co=()
for n in 1 2 3 4; do
  f=scripts/ruot-tap/l12-bai$n.mjs
  if [ ! -f "$f" ]; then echo "· bài $n: chưa có $f — bỏ qua"; continue; fi
  node "$f" | grep -E "dư -[2-9]|dư -[0-9][0-9]|katexErr=[1-9]|→" || true
  co+=("scripts/ruot-tap/out/ruot-tap-vl12-bai$n.pdf")
done
[ ${#co[@]} -ge 2 ] || { echo "cần ≥ 2 bài để ghép quyển"; exit 0; }
pdfunite "${co[@]}" scripts/ruot-tap/out/ruot-tap-vl12-chuong1.pdf
pdfinfo scripts/ruot-tap/out/ruot-tap-vl12-chuong1.pdf | grep Pages
pdffonts scripts/ruot-tap/out/ruot-tap-vl12-chuong1.pdf | grep -iE "helvetica|lucida|hiragino|arial" && echo "! CẢNH BÁO: còn font hệ thống" || true
