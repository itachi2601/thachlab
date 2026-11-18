#!/bin/bash
# Dry-run dang ly thuyet --chi-video cho 4 bai lo 9 L10 (18/11/2026). Khong ghi DB.
cd "$(dirname "$0")/../.."
for p in l10-nang-luong-cong-co-hoc:68 l10-dong-nang-the-nang:70 l10-co-nang-bao-toan:71 l10-hieu-suat:72 l10-bao-toan-dong-luong:74 l10-thuc-hanh-dong-luong:75; do
  s=${p%%:*}; id=${p##*:}
  echo "===== $s lesson $id"
  npx tsx scripts/update-ly-thuyet-from-bundle.mts "content/lesson-samples/$s/bundle.json" --lesson "$id" --dry-run --chi-video 2>&1 | grep -vi imageio | tail -25
done
echo XONG-DRY
