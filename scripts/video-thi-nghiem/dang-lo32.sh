#!/usr/bin/env bash
# Việc 4 lô 32: đổi 32 clip L12 sang bản -20261126 trên DB (20 bài lý thuyết, chỉ mục ly_thuyet, tự sao lưu). Thầy duyệt 27/11/2026.
#   bash scripts/video-thi-nghiem/dang-lo32.sh                 # xem thử (dry-run)
#   bash scripts/video-thi-nghiem/dang-lo32.sh --yes           # ghi thật ngay
#   bash scripts/video-thi-nghiem/dang-lo32.sh --yes --22h05   # chờ tới 22:05 hôm nay rồi ghi thật (chạy kèm caffeinate)
# Chỉ đổi URL clip + data-khung trong khối video → không cần --cho-phep-khac.
cd "$(dirname "$0")/../.."
YES="${1:-}"
if [ "${2:-}" = "--22h05" ]; then
  now=$(date +%s); target=$(date -j -f "%Y-%m-%d %H:%M:%S" "$(date +%Y-%m-%d) 22:05:00" +%s)
  if [ "$target" -gt "$now" ]; then echo "Chờ $(( (target-now)/60 )) phút tới 22:05…"; sleep $((target-now)); fi
fi
for p in "l12-su-chuyen-the 2" "l12-thang-nhiet-do 3" "l12-noi-nang-dl1 4" "l12-thuc-hanh-nhiet 5" "l12-thuyet-dong-hoc-phan-tu 6" \
         "l12-boyle-charles 7" "l12-ap-suat-dong-nang 9" "l12-khai-niem-tu-truong 10" "l12-luc-tu-cam-ung-tu 11" \
         "l12-thuc-hanh-cam-ung-tu 12" "l12-cam-ung-dien-tu 13" "l12-dong-dien-xoay-chieu 14" "l12-hat-nhan-mo-hinh-nguyen-tu 15" \
         "l12-nang-luong-lien-ket 16" "l12-phan-hach-nhiet-hach 17" "l12-phong-xa 18" "l12-an-toan-phong-xa 19" \
         "l12-may-phat-dien-bien-ap 125" "l12-ung-dung-cam-ung-dien-tu 126" "l12-dien-tu-truong-song-dien-tu 127"; do
  set -- $p
  echo "===== bai $2 ($1) $(date '+%H:%M:%S')"
  if [ "$YES" = "--yes" ]; then
    bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --chi-video --yes || echo "LOI bai $2"
  else
    echo n | bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --chi-video
  fi
done
echo "XONG $(date '+%H:%M:%S')"
