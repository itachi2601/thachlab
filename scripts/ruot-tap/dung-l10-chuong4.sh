#!/usr/bin/env bash
# Dựng cả quyển ruột tập VL10 Chương 4 (bài 23–27, 60 trang, đánh số liền mạch) → scripts/ruot-tap/out/ruot-tap-vl10-chuong4.pdf
# Mỗi bài: scripts/ruot-tap/l10-bai<N>.mjs (khung.mjs với lop:10, baiDau:23, tuongTu → bố cục bài 14).
set -euo pipefail
cd "$(dirname "$0")/../.."
for n in 23 24 25 26 27; do node scripts/ruot-tap/l10-bai$n.mjs | grep -E "dư -[2-9]|dư -[0-9][0-9]|katexErr=[1-9]|→" || true; done
pdfunite scripts/ruot-tap/out/ruot-tap-vl10-bai{23,24,25,26,27}.pdf scripts/ruot-tap/out/ruot-tap-vl10-chuong4.pdf
pdfinfo scripts/ruot-tap/out/ruot-tap-vl10-chuong4.pdf | grep Pages
pdffonts scripts/ruot-tap/out/ruot-tap-vl10-chuong4.pdf | grep -iE "helvetica|lucida|hiragino|arial" && echo "! CẢNH BÁO: còn font hệ thống" || true
