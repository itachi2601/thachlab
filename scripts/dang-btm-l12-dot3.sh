#!/usr/bin/env bash
# Đăng Bài tập mẫu L12 đợt 3 (17,18,19,125,126,127). Bài 17,18,19 chưa có mục bai_tap_mau → tạo mục (khuôn mục 224) trước.
# Bài 125,126,127 đã có mục; dạng cũ của chúng đã nằm trong tu_luan của file nên KHÔNG dùng --giu-cu. Dừng khi lỗi.
set -e
cd /Users/MAC/Projects/thachlab
for id in 17 18 19; do npx tsx scripts/tao-muc-bai-tap-mau.mts --lesson $id --mau 224; done
for id in 17 18 19 125 126 127; do npx tsx scripts/publish-bai-tap-mau.mts --lesson $id --dry-run; done
read -p "Dry-run ổn? Enter để đăng thật, Ctrl+C để dừng " _
for id in 17 18 19 125 126 127; do npx tsx scripts/publish-bai-tap-mau.mts --lesson $id --yes; done
echo "Xong. Bài tập mẫu đọc từ DB lúc chạy nên không cần deploy."
