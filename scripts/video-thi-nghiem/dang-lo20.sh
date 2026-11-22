#!/usr/bin/env bash
# Việc 4 lô 20: đổi 20 clip L12 sang bản -20261121 trên DB (15 bài lý thuyết, chỉ mục ly_thuyet, tự sao lưu).
#   bash scripts/video-thi-nghiem/dang-lo20.sh                 # xem thử (dry-run)
#   bash scripts/video-thi-nghiem/dang-lo20.sh --yes           # ghi thật ngay
#   bash scripts/video-thi-nghiem/dang-lo20.sh --yes --22h05   # chờ tới 22:05 hôm nay rồi ghi thật (chạy kèm caffeinate)
# 4 bài có sửa chữ ngoài khối video (thầy duyệt 21/11) → --cho-phep-khac:
#   4 noi-nang-dl1 (Nhìn vào), 13 cam-ung-dien-tu (Nhìn vào + dòng Φ âm), 11 luc-tu-cam-ung-tu (Nhìn vào), 5 thuc-hanh-nhiet (từ khoá đầu đo chạm điện trở).
cd "$(dirname "$0")/../.."
YES="${1:-}"
if [ "${2:-}" = "--22h05" ]; then
  now=$(date +%s); target=$(date -j -f "%Y-%m-%d %H:%M:%S" "$(date +%Y-%m-%d) 22:05:00" +%s)
  if [ "$target" -gt "$now" ]; then echo "Chờ $(( (target-now)/60 )) phút tới 22:05…"; sleep $((target-now)); fi
fi
for p in "l12-su-chuyen-the 2" "l12-thang-nhiet-do 3" "l12-noi-nang-dl1 4" "l12-thuc-hanh-nhiet 5" "l12-boyle-charles 7" \
         "l12-phuong-trinh-trang-thai 8" "l12-ap-suat-dong-nang 9" "l12-luc-tu-cam-ung-tu 11" "l12-thuc-hanh-cam-ung-tu 12" \
         "l12-cam-ung-dien-tu 13" "l12-dong-dien-xoay-chieu 14" "l12-hat-nhan-mo-hinh-nguyen-tu 15" "l12-phong-xa 18" \
         "l12-an-toan-phong-xa 19" "l12-may-phat-dien-bien-ap 125"; do
  set -- $p
  EXTRA=""; case "$2" in 4|5|11|13) EXTRA="--cho-phep-khac";; esac
  echo "===== bai $2 ($1) $(date '+%H:%M:%S')"
  if [ "$YES" = "--yes" ]; then
    bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --chi-video $EXTRA --yes || echo "LOI bai $2"
  else
    echo n | bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --chi-video $EXTRA
  fi
done
echo "XONG $(date '+%H:%M:%S')"
