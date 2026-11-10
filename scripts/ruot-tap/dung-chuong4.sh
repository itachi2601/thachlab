#!/usr/bin/env bash
# Dựng cả quyển ruột tập Chương 4 (bài 14–18, 60 trang, đánh số liền mạch) → scripts/ruot-tap/out/ruot-tap-vl12-chuong4.pdf
# BOOK_PAGE_START=61 bash scripts/ruot-tap/dung-chuong4.sh  → quyển nối tiếp chương liền kề (chỉ áp cho bài 15–18; bài 14 giữ số 1–12).
set -euo pipefail
cd "$(dirname "$0")/../.."
for n in 14 15 16 17 18; do node scripts/ruot-tap/bai$n.mjs | grep -E "dư -|katexErr=[1-9]|→" || true; done
pdfunite scripts/ruot-tap/out/ruot-tap-vl12-bai{14,15,16,17,18}.pdf scripts/ruot-tap/out/ruot-tap-vl12-chuong4.pdf
pdfinfo scripts/ruot-tap/out/ruot-tap-vl12-chuong4.pdf | grep Pages
