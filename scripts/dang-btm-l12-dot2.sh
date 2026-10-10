#!/usr/bin/env bash
# Đăng Bài tập mẫu L12 đợt 2 (9,11,13,14,15,16). Bài 9,15,16 chưa có mục bai_tap_mau → tạo mục (khuôn mục 224) trước.
# Bài 11,13,14 đã có dạng cũ: chúng đã nằm trong tu_luan của file nên KHÔNG dùng --giu-cu. Dừng khi lỗi.
set -e
cd /Users/MAC/Projects/thachlab
for id in 9 15 16; do npx tsx scripts/tao-muc-bai-tap-mau.mts --lesson $id --mau 224; done
for id in 9 11 13 14 15 16; do npx tsx scripts/publish-bai-tap-mau.mts --lesson $id --dry-run; done
read -p "Dry-run ổn? Enter để đăng thật, Ctrl+C để dừng " _
for id in 9 11 13 14 15 16; do npx tsx scripts/publish-bai-tap-mau.mts --lesson $id --yes; done
echo "Xong. Bài tập mẫu đọc từ DB lúc chạy nên không cần deploy."
