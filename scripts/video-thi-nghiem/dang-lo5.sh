#!/bin/bash
# Dang ly thuyet --chi-video 6 bai lo 5 (L11 am + L9 quang) - 18/11/2026, thay duyet, giu nguyen hop exp.
# Cho toi 22:05 roi moi ghi (ngoai gio HS lam bai).
cd "$(dirname "$0")/../.."
while [ "$(date +%H%M)" -lt 2205 ]; do sleep 60; done
for p in l11-thuc-hanh-do-tan-so-am:29 l11-thuc-hanh-do-toc-do-am:34 l9-lang-kinh-tan-sac:85 l9-thau-kinh:86 l9-thuc-hanh-tieu-cu:87 l9-kinh-lup-bai-tap-thau-kinh:88; do
  s=${p%%:*}; id=${p##*:}
  echo "===== $s lesson $id"
  bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$s/theory.html" "$id" --chi-video --yes 2>&1 | grep -v "ghép nhiều ý" | grep -vi imageio
done
echo XONG-DANG
