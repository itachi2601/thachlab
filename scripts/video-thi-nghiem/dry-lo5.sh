#!/bin/bash
# Xem thu (dry-run, khong ghi) dang lo 5: chi khoi video co khac DB khong.
cd "$(dirname "$0")/../.."
for p in l11-thuc-hanh-do-tan-so-am:29 l11-thuc-hanh-do-toc-do-am:34 l9-kinh-lup-bai-tap-thau-kinh:88 l9-lang-kinh-tan-sac:85 l9-thau-kinh:86 l9-thuc-hanh-tieu-cu:87; do
  echo "=== ${p%%:*} (lesson ${p##*:})"
  npx tsx scripts/update-ly-thuyet-from-bundle.mts "content/lesson-samples/${p%%:*}/bundle.json" --lesson "${p##*:}" --dry-run --chi-video
done
echo XONG-DRY
