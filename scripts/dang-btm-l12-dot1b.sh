#!/usr/bin/env bash
# Bài 2,3,4 đã đăng. Bài 6,7,8 chưa có mục bai_tap_mau: tạo mục (sao khuôn từ mục 224 của bài 3) rồi đăng. Dừng khi lỗi.
set -e
cd /Users/MAC/Projects/thachlab
for id in 6 7 8; do npx tsx scripts/tao-muc-bai-tap-mau.mts --lesson $id --mau 224; done
for id in 6 7 8; do npx tsx scripts/publish-bai-tap-mau.mts --lesson $id --yes; done
echo "Xong. Bài tập mẫu đọc từ DB lúc chạy nên không cần deploy."
