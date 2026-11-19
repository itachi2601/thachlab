#!/bin/bash
# Dang ly thuyet --chi-video 5 bai lo 7 (L10 Newton, ma sat) - 18/11/2026, thay duyet "Duyet, giu hop".
# Cho lo 6/8/9 xong (XONG-DANG-689 trong /tmp/dang-lo689.log) roi moi ghi.
cd "$(dirname "$0")/../.."
while [ "$(date +%H%M)" -lt 2205 ]; do sleep 60; done
while ! grep -q XONG-DANG-689 /tmp/dang-lo689.log 2>/dev/null; do sleep 30; done
for p in l10-dinh-luat-1-newton:59 l10-dinh-luat-2-newton:60 l10-dinh-luat-3-newton:61 l10-trong-luc-luc-cang:62 l10-luc-ma-sat:63; do
  echo "===== ${p%%:*} lesson ${p##*:}"
  bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/${p%%:*}/bundle.json" "${p##*:}" --chi-video --yes 2>&1 | grep -v "ghép nhiều ý" | grep -vi imageio
done
echo XONG-DANG-7
