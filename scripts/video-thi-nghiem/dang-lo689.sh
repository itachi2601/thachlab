#!/bin/bash
# Dang ly thuyet --chi-video 16 bai lo 6 (L9), lo 8, lo 9 (L10) - 18/11/2026, thay duyet "Duyet, giu hop".
# Cho 22:05 va cho lo 5 xong (XONG-DANG trong /tmp/dang-lo5.log) roi moi ghi.
cd "$(dirname "$0")/../.."
while [ "$(date +%H%M)" -lt 2205 ]; do sleep 60; done
while ! grep -q XONG-DANG /tmp/dang-lo5.log 2>/dev/null; do sleep 30; done
dang() { echo "===== $1 lesson $2"; bash scripts/cap-nhat-ly-thuyet.sh "$1" "$2" --chi-video --yes 2>&1 | grep -v "ghép nhiều ý" | grep -vi imageio; }
for p in l9-doan-mach-noi-tiep-song-song:90 l9-dien-tro-dinh-luat-ohm:89 l9-co-nang:130 l9-dong-nang-the-nang:129 \
  l10-luc-can-luc-nang:64 l10-moment-luc:66 l10-thuc-hanh-tong-hop-luc:67 l10-bien-dang-vat-ran:78 l10-khoi-luong-rieng-ap-suat:79 \
  l10-nang-luong-cong-co-hoc:68 l10-dong-nang-the-nang:70 l10-co-nang-bao-toan:71 l10-hieu-suat:72 l10-bao-toan-dong-luong:74 l10-thuc-hanh-dong-luong:75; do
  dang "content/lesson-samples/${p%%:*}/bundle.json" "${p##*:}"
done
dang content/hsg9/cd15-am-thanh/theory.html 150
echo XONG-DANG-689
