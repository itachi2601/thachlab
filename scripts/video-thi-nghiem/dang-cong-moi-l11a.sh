#!/usr/bin/env bash
# Cổng mới L11a: đổi 21 clip L11 Dao động + Sóng sang bản -20261127 trên DB (12 bài lý thuyết, chỉ mục ly_thuyet, tự sao lưu).
# Trước đó: python3 scripts/video-thi-nghiem/doi-ban-cong-moi-l11a.py --apply (kho + bài + gắn lại khung), commit.
#   bash scripts/video-thi-nghiem/dang-cong-moi-l11a.sh          # xem thử (dry-run)
#   bash scripts/video-thi-nghiem/dang-cong-moi-l11a.sh --yes    # ghi thật ngay (không hẹn giờ; chạy khi thầy bảo)
# Chỉ đổi URL clip + data-khung trong khối video → không cần --cho-phep-khac.
cd "$(dirname "$0")/../.."
YES="${1:-}"
for p in "l11-dao-dong-dieu-hoa 20" "l11-mo-ta-dao-dong 21" "l11-van-toc-gia-toc 22" "l11-bai-tap-dao-dong 23" \
         "l11-co-nang-dao-dong 24" "l11-tat-dan-cuong-buc 25" "l11-bai-tap-nang-luong-dao-dong 26" \
         "l11-song-ngang-song-doc 28" "l11-thuc-hanh-do-tan-so-am 29" "l11-giao-thoa-song 31" "l11-song-dung 32" \
         "l11-bai-tap-song 33"; do
  set -- $p
  echo "===== bai $2 ($1) $(date '+%H:%M:%S')"
  if [ "$YES" = "--yes" ]; then
    bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --chi-video --yes || echo "LOI bai $2"
  else
    echo n | bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --chi-video
  fi
done
echo "XONG $(date '+%H:%M:%S')"
