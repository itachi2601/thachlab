#!/usr/bin/env bash
# Lô 10 — 5 bài KHTN 9 (đã đăng 18/11 18h42, chưa có video): ghi lại CHỈ mục ly_thuyet
# (video lô 10 + hộp exp đã sửa lộ đáp án) — đề luyện tập không đổi, giữ nguyên.
#   bash scripts/video-thi-nghiem/dang-lo10-l9.sh          # xem thử, không ghi
#   bash scripts/video-thi-nghiem/dang-lo10-l9.sh --yes    # ghi thật (chỉ sau 22h)
set -u
[[ "${1:-}" == "--yes" ]] && YES=1
cd "$(dirname "$0")/../.."
for p in "l9-cam-ung-dien-tu 92" "l9-tac-dung-dong-dien-xoay-chieu 93" "l9-vong-nang-luong-hoa-thach 94" "l9-nang-luong-tai-tao 95" "l9-mo-dau-dung-cu-thuyet-trinh 128"; do
  set -- $p
  echo "════ $1 (bài $2)"
  if [[ "${YES:-}" == "1" ]]; then
    bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --chi-video --cho-phep-khac --yes || { echo "✗ dừng ở bài $2"; exit 1; }
  else
    echo N | bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --chi-video --cho-phep-khac
  fi
done
