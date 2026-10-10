#!/usr/bin/env bash
# Đăng Bài tập mẫu 6 bài L12 đợt 1 (2,3,4,6,7,8). Dừng khi lỗi. Bài tập mẫu đọc từ DB lúc chạy nên không cần deploy.
set -e
cd /Users/MAC/Projects/thachlab
for id in 2 3 4 6 7 8; do npx tsx scripts/publish-bai-tap-mau.mts --lesson $id --dry-run; done
read -p "Dry-run ổn? Enter để đăng thật, Ctrl+C để dừng " _
for id in 2 3 4 6 7 8; do npx tsx scripts/publish-bai-tap-mau.mts --lesson $id --yes; done
echo "Xong."
