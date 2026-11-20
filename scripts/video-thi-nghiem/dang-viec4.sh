#!/usr/bin/env bash
# Đổi 3 clip mẫu việc 4 (bản -20261120) trên DB: bài 57 nemngang1, 83 khucxa2, 12 thuchanhtu4.
#   bash scripts/video-thi-nghiem/dang-viec4.sh                 # xem thử (dry-run)
#   bash scripts/video-thi-nghiem/dang-viec4.sh --yes           # ghi thật ngay
#   bash scripts/video-thi-nghiem/dang-viec4.sh --yes --22h05   # chờ tới 22:05 hôm nay rồi ghi thật
# Bài 12 cần --cho-phep-khac: file có thêm việc 5 (clip dời lên trước hộp mô phỏng, hộp thêm
# tl-mo-phong data-mo-phong="can-dong-dien"). Bản web chưa deploy việc 5 thì bỏ qua khoá lạ → hộp tĩnh như cũ.
cd "$(dirname "$0")/../.."
YES="${1:-}"
if [ "${2:-}" = "--22h05" ]; then
  now=$(date +%s); target=$(date -j -f "%Y-%m-%d %H:%M:%S" "$(date +%Y-%m-%d) 22:05:00" +%s)
  if [ "$target" -gt "$now" ]; then echo "Chờ $(( (target-now)/60 )) phút tới 22:05…"; sleep $((target-now)); fi
fi
for p in "l10-chuyen-dong-nem 57" "l9-khuc-xa-anh-sang 83" "l12-thuc-hanh-cam-ung-tu 12"; do
  set -- $p
  EXTRA=""; [ "$2" = "12" ] && EXTRA="--cho-phep-khac"
  echo "===== bai $2 ($1) $(date '+%H:%M:%S')"
  if [ "$YES" = "--yes" ]; then
    bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --chi-video $EXTRA --yes || echo "LOI bai $2"
  else
    echo n | bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --chi-video $EXTRA
  fi
done
echo "XONG $(date '+%H:%M:%S')"
