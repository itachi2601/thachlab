#!/usr/bin/env bash
# Dry-run dang lo 11 (6 bai L11) - chi doc, khong ghi. Log: scripts/logs/dry-lo11-l11.log
cd "$(dirname "$0")/../.."
mkdir -p scripts/logs
for p in "l11-song-dung 32" "l11-song-ngang-song-doc 28" "l11-giao-thoa-song 31" "l11-bai-tap-song 33" "l11-thuc-hanh-do-toc-do-am 34" "l11-dien-truong-deu 37"; do
  set -- $p
  echo "==== $1 (bai $2)"
  echo N | bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --chi-video --cho-phep-khac 2>&1
done 2>&1 | tee scripts/logs/dry-lo11-l11.log
