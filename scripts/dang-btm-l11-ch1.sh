#!/usr/bin/env bash
# Đăng Bài tập mẫu 7 bài L11 Chương 1 Dao động (20–26). Dừng khi lỗi.
# Bài 20 đã có mục (ghi đè 1 dạng cũ đã biên tập thành Dạng 1, có sao lưu); 21–26 chưa có mục nên tạo trước.
set -e
cd /Users/MAC/Projects/thachlab
for id in 21 22 23 24 25 26; do npx tsx scripts/tao-muc-bai-tap-mau.mts --lesson $id --mau 158; done
for id in 20 21 22 23 24 25 26; do npx tsx scripts/publish-bai-tap-mau.mts --lesson $id --yes; done
echo "Xong. Bài tập mẫu đọc từ DB lúc chạy nên không cần deploy."
