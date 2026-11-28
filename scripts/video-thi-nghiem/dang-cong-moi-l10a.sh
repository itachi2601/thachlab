#!/usr/bin/env bash
# Cổng mới L10a mẻ 1 (thầy duyệt 27/11/2026 "Duyệt, sửa cả hộp"): đổi 13 clip L10 (8 bài, lesson 46–53) sang bản dựng lại -20261127
# trên DB (chỉ mục ly_thuyet, tự sao lưu). Trước đó: doi-cong-moi-l10a.py --apply (kho + bài + gắn khung) đã chạy và commit.
#   bash scripts/video-thi-nghiem/dang-cong-moi-l10a.sh          # xem thử (dry-run)
#   bash scripts/video-thi-nghiem/dang-cong-moi-l10a.sh --yes    # ghi thật (không hẹn giờ)
#   ME=2 bash scripts/video-thi-nghiem/dang-cong-moi-l10a.sh [--yes]   # mẻ 2 (thầy duyệt 27/11 "sửa hết"): 7 clip, bài 54, 55, 56, 51;
#     bài 54, 56 kèm sửa hộp exp (sua-hop-l10a-3.json, -4.json) → --cho-phep-khac.
# Bài 50, 51, 53 kèm sửa hộp exp lộ Dự đoán (sua-hop-l10a.json, sua-hop-l10a-2.json) → --cho-phep-khac; khác ngoài khối video
# phải đúng các câu trong hai file đó. Bài khác dry-run báo khác ngoài khối video thì dừng, hỏi thầy.
cd "$(dirname "$0")/../.."
YES="${1:-}"
DS=("l10-lam-quen-voi-vat-li 46" "l10-an-toan-phong-thuc-hanh 47" "l10-thuc-hanh-sai-so 48" "l10-do-dich-chuyen-quang-duong 49" \
         "l10-toc-do-van-toc 50" "l10-thuc-hanh-do-toc-do 51" "l10-do-thi-dich-chuyen-thoi-gian 52" "l10-chuyen-dong-bien-doi-gia-toc 53")
KHAC_BAI="50 51 53"
if [ "${ME:-1}" = "2" ]; then DS=("l10-chuyen-dong-thang-bien-doi-deu 54" "l10-su-roi-tu-do 55" "l10-thuc-hanh-do-g 56" "l10-thuc-hanh-do-toc-do 51"); KHAC_BAI="54 56"; fi
# ME=3: mẻ 3 (thầy duyệt 28/11 "sửa hộp"): 9 clip nhóm C, bài 57–62; 57, 58, 62 có sửa hộp exp
if [ "${ME:-1}" = "3" ]; then DS=("l10-chuyen-dong-nem 57" "l10-tong-hop-phan-tich-luc 58" "l10-dinh-luat-1-newton 59" "l10-dinh-luat-2-newton 60" "l10-dinh-luat-3-newton 61" "l10-trong-luc-luc-cang 62"); KHAC_BAI="57 58 62"; fi
for p in "${DS[@]}"; do
  set -- $p
  KHAC=""; case " $KHAC_BAI " in *" $2 "*) KHAC="--cho-phep-khac" ;; esac
  echo "===== bai $2 ($1) $(date '+%H:%M:%S')"
  if [ "$YES" = "--yes" ]; then
    bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --chi-video $KHAC --yes || echo "LOI bai $2"
  else
    echo n | bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --chi-video $KHAC
  fi
done
echo "XONG $(date '+%H:%M:%S')"
