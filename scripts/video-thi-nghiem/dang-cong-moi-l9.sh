#!/usr/bin/env bash
# Việc 4 "Cổng mới — L9" (27/11/2026): ghi 36 clip L9 bản mới lên DB (16 bài KHTN 9 + cd15 HSG âm thanh), chỉ mục ly_thuyet,
# tự sao lưu. Chạy SAU khi thầy duyệt và đã chạy `python3 scripts/video-thi-nghiem/doi-cong-moi-l9.py --apply` (đổi kho + bài + khung).
#   bash scripts/video-thi-nghiem/dang-cong-moi-l9.sh          # xem thử (dry-run) cả 17 bài
#   bash scripts/video-thi-nghiem/dang-cong-moi-l9.sh --yes    # ghi thật ngay (không hẹn giờ)
# Chỉ đổi URL clip + data-khung trong khối video → không cần --cho-phep-khac, trừ bài 150 (xem dưới); bài nào khác dry-run báo khác ngoài khối video thì dừng, hỏi thầy).
cd "$(dirname "$0")/../.."
YES="${1:-}"
for p in "lesson-samples/l9-dien-tro-dinh-luat-ohm/bundle.json 89" "lesson-samples/l9-doan-mach-noi-tiep-song-song/bundle.json 90" \
         "lesson-samples/l9-nang-luong-dong-dien-cong-suat/bundle.json 91" "lesson-samples/l9-dong-nang-the-nang/bundle.json 129" \
         "lesson-samples/l9-cam-ung-dien-tu/bundle.json 92" "lesson-samples/l9-tac-dung-dong-dien-xoay-chieu/bundle.json 93" \
         "lesson-samples/l9-vong-nang-luong-hoa-thach/bundle.json 94" "lesson-samples/l9-co-nang/bundle.json 130" \
         "lesson-samples/l9-cong-cong-suat/bundle.json 131" "lesson-samples/l9-mo-dau-dung-cu-thuyet-trinh/bundle.json 128" \
         "hsg9/cd15-am-thanh/theory.html 150" "lesson-samples/l9-nang-luong-tai-tao/bundle.json 95" \
         "lesson-samples/l9-kinh-lup-bai-tap-thau-kinh/bundle.json 88" "lesson-samples/l9-lang-kinh-tan-sac/bundle.json 85" \
         "lesson-samples/l9-phan-xa-toan-phan/bundle.json 84" "lesson-samples/l9-thau-kinh/bundle.json 86" \
         "lesson-samples/l9-thuc-hanh-tieu-cu/bundle.json 87"; do
  set -- $p
  # Bài 150 (HSG cd15): repo đã có dòng "Đọc ~16 phút · học kỹ … ~29 phút" (P2, commit 70bd8505a 26/11) mà DB chưa có → khác ngoài khối video đúng câu đó.
  KHAC=""; [ "$2" = "150" ] && KHAC="--cho-phep-khac"
  echo "===== bai $2 ($1) $(date '+%H:%M:%S')"
  if [ "$YES" = "--yes" ]; then
    bash scripts/cap-nhat-ly-thuyet.sh "content/$1" "$2" --chi-video $KHAC --yes || echo "LOI bai $2"
  else
    echo n | bash scripts/cap-nhat-ly-thuyet.sh "content/$1" "$2" --chi-video $KHAC
  fi
done
echo "XONG $(date '+%H:%M:%S')"
