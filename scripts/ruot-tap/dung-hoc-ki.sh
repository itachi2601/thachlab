#!/usr/bin/env bash
# Dựng ruột tập THEO HỌC KÌ — mỗi khối mỗi học kì một quyển, đánh số trang liền mạch cả quyển (thầy yêu cầu 17/11/2026).
#   bash scripts/ruot-tap/dung-hoc-ki.sh            → cả 6 quyển
#   bash scripts/ruot-tap/dung-hoc-ki.sh vl12-hk1   → một quyển
# → scripts/ruot-tap/out/ruot-tap-vl<lớp>-hk<1|2>.pdf
# Chia theo phân phối chương trình (sửa hàm quyen nếu trường chia khác):
#   VL10 HK1 = Ch.1–3 (bài 1–22) · HK2 = Ch.4–7 (bài 23–34)
#   VL11 HK1 = Ch.1–2 (bài 1–15) · HK2 = Ch.3–4 (bài 16–26)
#   VL12 HK1 = Ch.1–2 + Ch.3 bài 9–12 (từ trường, cảm ứng điện từ) · HK2 = Ch.3 bài 13–16 (xoay chiều, sóng điện từ) + Ch.4
# Mỗi mục "script-chương:bỏ:giữ" = chạy dung-<script-chương>.sh với BOOK_PAGE_START sao cho trang đầu bài được giữ
# đứng đúng số trang trong quyển, rồi cắt lấy `giữ` bài (12 trang/bài) sau khi bỏ `bỏ` bài đầu chương (giữ=0 → hết chương).
# Bản theo chương (dung-l*-chuong*.sh chạy riêng) vẫn dựng được, số trang bắt đầu từ 1.
set -euo pipefail
cd "$(dirname "$0")/../.."
OUT=scripts/ruot-tap/out
quyen() { case $1 in   # bash 3.2 trên Mac: không có mảng kết hợp
  vl10-hk1) echo "l10-chuong1:0:0 l10-chuong2:0:0 l10-chuong3:0:0" ;;
  vl10-hk2) echo "l10-chuong4:0:0 l10-chuong5:0:0 l10-chuong6:0:0 l10-chuong7:0:0" ;;
  vl11-hk1) echo "l11-chuong1:0:0 l11-chuong2:0:0" ;;
  vl11-hk2) echo "l11-chuong3:0:0 l11-chuong4:0:0" ;;
  vl12-hk1) echo "l12-chuong1:0:0 l12-chuong2:0:0 l12-chuong3:0:4" ;;
  vl12-hk2) echo "l12-chuong3:4:0 chuong4:0:0" ;;
  *) echo "không có quyển $1" >&2; exit 1 ;;
esac; }
pdf_chuong() { case $1 in chuong4) echo $OUT/ruot-tap-vl12-chuong4.pdf ;; l*) echo $OUT/ruot-tap-v${1%%-*}-${1#*-}.pdf ;; esac; }

dung() {
  local q=$1 tmp; tmp=$(mktemp -d); local cur=1 k=0
  echo "=== $q $(date +%H:%M:%S)"
  for muc in $(quyen "$q"); do
    IFS=: read -r ch bo giu <<<"$muc"
    BOOK_PAGE_START=$((cur - bo * 12)) bash scripts/ruot-tap/dung-$ch.sh >/dev/null
    local f; f=$(pdf_chuong "$ch"); local n; n=$(pdfinfo "$f" | awk '/^Pages/{print $2}')
    local tu=$((bo * 12 + 1)) den=$n
    [ "$giu" -gt 0 ] && den=$((bo * 12 + giu * 12))
    pdfseparate -f $tu -l $den "$f" "$tmp/$(printf %03d $k)-%04d.pdf"
    k=$((k + 1)); cur=$((cur + den - tu + 1))
    echo "  $ch: tr.${tu}–${den} của chương → hết tr.$((cur - 1)) của quyển"
  done
  pdfunite $(ls "$tmp"/*.pdf | sort) $OUT/ruot-tap-$q.pdf
  rm -rf "$tmp"
  pdfinfo $OUT/ruot-tap-$q.pdf | grep Pages
  pdffonts $OUT/ruot-tap-$q.pdf | grep -iE "helvetica|lucida|hiragino|arial|symbols" && echo "! CẢNH BÁO: còn font hệ thống" || true
}

if [ $# -gt 0 ]; then for q in "$@"; do dung "$q"; done
else for q in vl10-hk1 vl10-hk2 vl11-hk1 vl11-hk2 vl12-hk1 vl12-hk2; do dung "$q"; done; fi
echo "=== XONG $(date +%H:%M:%S)"
