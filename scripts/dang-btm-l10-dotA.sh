#!/usr/bin/env bash
# Đăng Bài tập mẫu L10 đợt A (58,60,62,63,66 — Chương 3 Động lực học). Cả 5 bài đã có mục bai_tap_mau; dạng cũ đã nằm trong tu_luan
# của file nên KHÔNG dùng --giu-cu (bản sao lưu 20/13/4/8/15 dạng cũ ghi ở scripts/logs/). Dừng khi lỗi.
set -e
cd /Users/MAC/Projects/thachlab
for id in 58 60 62 63 66; do npx tsx scripts/publish-bai-tap-mau.mts --lesson $id --dry-run; done
read -p "Dry-run ổn? Enter để đăng thật, Ctrl+C để dừng " _
for id in 58 60 62 63 66; do npx tsx scripts/publish-bai-tap-mau.mts --lesson $id --yes; done
echo "Xong. Bài tập mẫu đọc từ DB lúc chạy nên không cần deploy."
