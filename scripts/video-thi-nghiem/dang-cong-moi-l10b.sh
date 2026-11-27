#!/usr/bin/env bash
# Cổng mới L10b: đổi 38 clip L10 (17 bài, lesson 63–79) sang bản dựng lại 27/11/2026 trên DB (chỉ mục ly_thuyet, tự sao lưu).
#   bash scripts/video-thi-nghiem/dang-cong-moi-l10b.sh          # xem thử (dry-run)
#   bash scripts/video-thi-nghiem/dang-cong-moi-l10b.sh --yes    # ghi thật (chạy khi thầy bảo; không hẹn giờ bằng sleep)
# Trước đó: kho + bài đã đổi URL và gắn lại khung (gan-khung-video.mts) — chỉ khác khối video → không cần --cho-phep-khac.
cd "$(dirname "$0")/../.."
YES="${1:-}"
for p in "l10-luc-ma-sat 63" "l10-luc-can-luc-nang 64" "l10-giai-bai-toan-dong-luc-hoc 65" "l10-moment-luc 66" \
         "l10-thuc-hanh-tong-hop-luc 67" "l10-nang-luong-cong-co-hoc 68" "l10-cong-suat 69" "l10-dong-nang-the-nang 70" \
         "l10-co-nang-bao-toan 71" "l10-hieu-suat 72" "l10-dong-luong 73" "l10-bao-toan-dong-luong 74" \
         "l10-thuc-hanh-dong-luong 75" "l10-chuyen-dong-tron-deu 76" "l10-luc-huong-tam 77" "l10-bien-dang-vat-ran 78" \
         "l10-khoi-luong-rieng-ap-suat 79"; do
  set -- $p
  echo "===== bai $2 ($1) $(date '+%H:%M:%S')"
  if [ "$YES" = "--yes" ]; then
    bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --chi-video --yes || echo "LOI bai $2"
  else
    echo n | bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --chi-video
  fi
done
echo "XONG $(date '+%H:%M:%S')"
