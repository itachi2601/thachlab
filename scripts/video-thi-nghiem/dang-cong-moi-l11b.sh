#!/usr/bin/env bash
# Cổng mới — L11b: đổi 25 clip L11 (bài 34–45) + tn-l12-tdhphantu-04 sang bản dựng lại 27/11/2026 trên DB
# (13 bài lý thuyết, chỉ mục ly_thuyet, cap-nhat-ly-thuyet.sh tự sao lưu). Chạy SAU khi thầy duyệt và đã chạy
# doi-ban-l11b.py --apply (kho + bài trỏ bản mới, khung gắn lại).
#   bash scripts/video-thi-nghiem/dang-cong-moi-l11b.sh          # xem thử (dry-run)
#   bash scripts/video-thi-nghiem/dang-cong-moi-l11b.sh --yes    # ghi thật ngay (chạy trong tab terminal, thầy theo dõi)
# Chỉ đổi URL clip + data-khung trong khối video → không cần --cho-phep-khac. Không hẹn giờ trong script.
cd "$(dirname "$0")/../.."
YES="${1:-}"
for p in "l11-thuc-hanh-do-toc-do-am 34" "l11-luc-coulomb 35" "l11-khai-niem-dien-truong 36" "l11-dien-truong-deu 37" \
         "l11-the-nang-dien 38" "l11-dien-the 39" "l11-tu-dien 40" "l11-cuong-do-dong-dien 41" \
         "l11-dien-tro-dinh-luat-ohm 42" "l11-nguon-dien 43" "l11-nang-luong-cong-suat-dien 44" \
         "l11-thuc-hanh-do-sdd-pin 45" "l12-thuyet-dong-hoc-phan-tu 6"; do
  set -- $p
  echo "===== bai $2 ($1) $(date '+%H:%M:%S')"
  if [ "$YES" = "--yes" ]; then
    bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --chi-video --yes || echo "LOI bai $2"
  else
    echo n | bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --chi-video
  fi
done
echo "XONG $(date '+%H:%M:%S')"
