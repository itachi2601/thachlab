#!/bin/bash
# Dang lai ly thuyet 25 bai sau khi sua hop exp lo dap an (18/11/2026, thay duyet "sua cac hop thi nghiem lo dap an").
# DB dang = file truoc commit sua hop (vua dang --chi-video toi nay, "KHONG khac") nen khac biet = dung diff commit sua hop.
cd "$(dirname "$0")/../.."
dang() { echo "===== $1 lesson $2"; bash scripts/cap-nhat-ly-thuyet.sh "$1" "$2" --chi-video --cho-phep-khac --yes 2>&1 | grep -v "ghép nhiều ý" | grep -vi imageio; }
for p in l11-thuc-hanh-do-tan-so-am:29 l11-thuc-hanh-do-toc-do-am:34 l9-lang-kinh-tan-sac:85 l9-thau-kinh:86 l9-thuc-hanh-tieu-cu:87 l9-kinh-lup-bai-tap-thau-kinh:88 \
  l9-doan-mach-noi-tiep-song-song:90 l9-dien-tro-dinh-luat-ohm:89 l9-co-nang:130 \
  l10-luc-can-luc-nang:64 l10-moment-luc:66 l10-thuc-hanh-tong-hop-luc:67 l10-bien-dang-vat-ran:78 l10-khoi-luong-rieng-ap-suat:79 \
  l10-nang-luong-cong-co-hoc:68 l10-dong-nang-the-nang:70 l10-co-nang-bao-toan:71 l10-bao-toan-dong-luong:74 l10-thuc-hanh-dong-luong:75 \
  l10-dinh-luat-1-newton:59 l10-dinh-luat-2-newton:60 l10-dinh-luat-3-newton:61 l10-trong-luc-luc-cang:62 l10-luc-ma-sat:63; do
  dang "content/lesson-samples/${p%%:*}/bundle.json" "${p##*:}"
done
dang content/hsg9/cd15-am-thanh/theory.html 150
echo XONG-SUA-HOP
