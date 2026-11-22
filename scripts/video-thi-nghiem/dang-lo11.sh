#!/usr/bin/env bash
# Lô 11 — 12 bài (6 L11, 5 L9/L10, 1 HSG9): ghi lại CHỈ mục ly_thuyet (video tự dựng + hộp exp đã sửa lộ đáp án).
#   bash scripts/video-thi-nghiem/dang-lo11.sh          # xem thử, không ghi
#   bash scripts/video-thi-nghiem/dang-lo11.sh --yes    # ghi thật (chỉ sau 22h, sau khi thầy duyệt)
set -u
[[ "${1:-}" == "--yes" ]] && YES=1
cd "$(dirname "$0")/../.."
for p in "lesson-samples/l11-song-dung 32" "lesson-samples/l11-song-ngang-song-doc 28" "lesson-samples/l11-giao-thoa-song 31" \
  "lesson-samples/l11-bai-tap-song 33" "lesson-samples/l11-thuc-hanh-do-toc-do-am 34" "lesson-samples/l11-dien-truong-deu 37" \
  "lesson-samples/l9-khuc-xa-anh-sang 83" "lesson-samples/l9-phan-xa-toan-phan 84" "lesson-samples/l9-lang-kinh-tan-sac 85" \
  "lesson-samples/l10-chuyen-dong-nem 57" "lesson-samples/l9-doan-mach-noi-tiep-song-song 90" "hsg9/cd15-am-thanh 150"; do
  set -- $p
  echo "════ $1 (bài $2)"
  if [[ "${YES:-}" == "1" ]]; then
    bash scripts/cap-nhat-ly-thuyet.sh "$(f=content/$1/bundle.json; [[ -f $f ]] || f=content/$1/theory.html; echo $f)" "$2" --chi-video --cho-phep-khac --yes || { echo "✗ dừng ở bài $2"; exit 1; }
  else
    echo N | bash scripts/cap-nhat-ly-thuyet.sh "$(f=content/$1/bundle.json; [[ -f $f ]] || f=content/$1/theory.html; echo $f)" "$2" --chi-video --cho-phep-khac
  fi
done
