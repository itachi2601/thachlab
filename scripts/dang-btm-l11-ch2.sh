#!/usr/bin/env bash
# Đăng Bài tập mẫu 6 bài L11 Chương 2 (27,28,30,31,32,33). Dừng khi lỗi.
set -e
cd /Users/MAC/Projects/thachlab
npx tsx scripts/tao-muc-bai-tap-mau.mts --lesson 30 --mau 158
npx tsx scripts/tao-muc-bai-tap-mau.mts --lesson 32 --mau 158
for id in 27 28 30 31 32 33; do npx tsx scripts/publish-bai-tap-mau.mts --lesson $id --yes; done
echo "Xong. Bài tập mẫu đọc từ DB lúc chạy nên không cần deploy."
