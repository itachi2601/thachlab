#!/bin/bash
# Dry-run dang ly thuyet --chi-video cho 4 bai lo 4 L11 (16/11/2026). Khong ghi DB.
cd "$(dirname "$0")/../.."
for p in l11-tu-dien:40 l11-dien-tro-dinh-luat-ohm:42 l11-nguon-dien:43 l11-thuc-hanh-do-sdd-pin:45; do
  s=${p%%:*}; id=${p##*:}
  echo "===== $s lesson $id"
  npx tsx scripts/update-ly-thuyet-from-bundle.mts "content/lesson-samples/$s/bundle.json" --lesson "$id" --dry-run --chi-video 2>&1 | grep -vi imageio | tail -25
done
echo XONG-DRY
