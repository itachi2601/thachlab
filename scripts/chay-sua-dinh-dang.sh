#!/usr/bin/env bash
# Chạy lần lượt các file apply-NN.sql do sua-dinh-dang-hang-loat.mts sinh ra (00 = sao lưu, cuối = đếm đã đổi).
# Mỗi file một giao dịch (tắt trg_exams_sync_bank trong giao dịch); lỗi ở file nào thì dừng ngay, file trước đã commit vẫn giữ.
# Chỉ chạy sau 22h hoặc trước 6h (Disk IO); thầy cho phép chạy ban ngày thì đặt BAN_NGAY=1. Chạy từ checkout chính (cần supabase link):
#   bash scripts/chay-sua-dinh-dang.sh <đường-dẫn-tuyệt-đối>/scripts/data/quet-dinh-dang/<ts>/sua [từ-số-file]
set -euo pipefail
dir="$1"; from="${2:-0}"
h=$(date +%H)
if [ -z "${BAN_NGAY:-}" ] && (( 10#$h >= 6 && 10#$h < 22 )); then echo "Đang $h giờ — chỉ chạy sau 22h hoặc trước 6h."; exit 1; fi
for f in "$dir"/apply-*.sql; do
  n=$(basename "$f" .sql); n=${n#apply-}
  (( 10#$n < from )) && continue
  h=$(date +%H); if [ -z "${BAN_NGAY:-}" ] && (( 10#$h >= 6 && 10#$h < 22 )); then echo "Đã $h giờ — dừng trước $(basename "$f"). Tối nay chạy tiếp: thêm tham số $((10#$n))"; exit 0; fi
  echo "== $(date +%H:%M:%S) $(basename "$f") ($(wc -c <"$f" | tr -d ' ') byte)"
  supabase db query --linked -f "$f" || { echo "LỖI ở $f — dừng. Chạy tiếp từ file này: thêm tham số $((10#$n))"; exit 1; }
  sleep 3
done
echo "XONG $(date +%H:%M:%S)"
