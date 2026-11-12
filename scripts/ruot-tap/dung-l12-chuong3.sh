#!/usr/bin/env bash
# Dựng cả quyển ruột tập VL12 Chương 3 Từ trường (bài 9–16, lesson 10–14, 125–127, 96 trang, đánh số liền mạch)
# → scripts/ruot-tap/out/ruot-tap-vl12-chuong3.pdf
# Mỗi bài: scripts/ruot-tap/l12-c3-bai<N>.mjs (khung.mjs với lop:12, baiDau:9, tuongTu → bố cục bài 14) + hinh-l12-c3-bai<N>.mjs.
# Tên file có '-c3-' vì bài 14–16 trùng số với Chương 4 (bai14.mjs…): mỗi bài truyền out …/ruot-tap-vl12-c3-bai<N>.pdf vào dung().
# Bài nào chưa có file thì bỏ qua (các phiên song song gộp dần vào main).
set -euo pipefail
cd "$(dirname "$0")/../.."
co=()
for n in 9 10 11 12 13 14 15 16; do
  f=scripts/ruot-tap/l12-c3-bai$n.mjs
  if [ ! -f "$f" ]; then echo "· bài $n: chưa có $f — bỏ qua"; continue; fi
  node "$f" | grep -E "dư -[2-9]|dư -[0-9][0-9]|katexErr=[1-9]|→" || true
  co+=("scripts/ruot-tap/out/ruot-tap-vl12-c3-bai$n.pdf")
done
[ ${#co[@]} -ge 2 ] || { echo "cần ≥ 2 bài để ghép quyển"; exit 0; }
pdfunite "${co[@]}" scripts/ruot-tap/out/ruot-tap-vl12-chuong3.pdf
pdfinfo scripts/ruot-tap/out/ruot-tap-vl12-chuong3.pdf | grep Pages
pdffonts scripts/ruot-tap/out/ruot-tap-vl12-chuong3.pdf | grep -iE "helvetica|lucida|hiragino|arial" && echo "! CẢNH BÁO: còn font hệ thống" || true
