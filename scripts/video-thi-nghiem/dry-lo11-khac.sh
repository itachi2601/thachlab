#!/usr/bin/env bash
# Dry-run lo 11 (L9/L10/HSG) - chi doc. Log: scripts/logs/dry-lo11-khac.log
cd "$(dirname "$0")/../.."
mkdir -p scripts/logs
for p in "lesson-samples/l9-khuc-xa-anh-sang 83" "lesson-samples/l9-phan-xa-toan-phan 84" "lesson-samples/l9-lang-kinh-tan-sac 85" "lesson-samples/l10-chuyen-dong-nem 57" "lesson-samples/l9-doan-mach-noi-tiep-song-song 90" "hsg9/cd15-am-thanh 150"; do
  set -- $p
  echo "==== $1 (bai $2)"
  echo N | bash scripts/cap-nhat-ly-thuyet.sh "$(f=content/$1/bundle.json; [[ -f $f ]] || f=content/$1/theory.html; echo $f)" "$2" --chi-video --cho-phep-khac 2>&1
done 2>&1 | tee scripts/logs/dry-lo11-khac.log
