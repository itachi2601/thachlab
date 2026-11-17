#!/bin/bash
# Dang ly thuyet --chi-video --cho-phep-khac 3 bai lo 4 L11 con lai (42, 43, 45) - 17/11/2026, thay duyet.
cd "$(dirname "$0")/../.."
for p in l11-dien-tro-dinh-luat-ohm:42 l11-nguon-dien:43 l11-thuc-hanh-do-sdd-pin:45; do
  s=${p%%:*}; id=${p##*:}
  echo "===== $s lesson $id"
  bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$s/theory.html" "$id" --chi-video --cho-phep-khac --yes 2>&1 | grep -v "ghép nhiều ý" | grep -vi imageio
done
echo XONG-DANG
