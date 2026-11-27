#!/usr/bin/env bash
# Cổng mới L10a mẻ 1 (thầy duyệt 27/11/2026 "Duyệt, sửa cả hộp"): đổi 13 clip L10 (8 bài, lesson 46–53) sang bản dựng lại -20261127
# trên DB (chỉ mục ly_thuyet, tự sao lưu). Trước đó: doi-cong-moi-l10a.py --apply (kho + bài + gắn khung) đã chạy và commit.
#   bash scripts/video-thi-nghiem/dang-cong-moi-l10a.sh          # xem thử (dry-run)
#   bash scripts/video-thi-nghiem/dang-cong-moi-l10a.sh --yes    # ghi thật (không hẹn giờ)
# Bài 50, 51, 53 kèm sửa hộp exp lộ Dự đoán (sua-hop-l10a.json, sua-hop-l10a-2.json) → --cho-phep-khac; khác ngoài khối video
# phải đúng các câu trong hai file đó. Bài khác dry-run báo khác ngoài khối video thì dừng, hỏi thầy.
cd "$(dirname "$0")/../.."
YES="${1:-}"
for p in "l10-lam-quen-voi-vat-li 46" "l10-an-toan-phong-thuc-hanh 47" "l10-thuc-hanh-sai-so 48" "l10-do-dich-chuyen-quang-duong 49" \
         "l10-toc-do-van-toc 50" "l10-thuc-hanh-do-toc-do 51" "l10-do-thi-dich-chuyen-thoi-gian 52" "l10-chuyen-dong-bien-doi-gia-toc 53"; do
  set -- $p
  KHAC=""; case "$2" in 50|51|53) KHAC="--cho-phep-khac" ;; esac
  echo "===== bai $2 ($1) $(date '+%H:%M:%S')"
  if [ "$YES" = "--yes" ]; then
    bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --chi-video $KHAC --yes || echo "LOI bai $2"
  else
    echo n | bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --chi-video $KHAC
  fi
done
echo "XONG $(date '+%H:%M:%S')"
