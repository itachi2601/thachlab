#!/usr/bin/env bash
# Đăng Bài tập mẫu L10 đợt B (68,69,70,71,72,73,74,76,77,78,79 — Chương 4–7). Bài 68,69,72,78 chưa có mục bai_tap_mau → tạo mục
# (khuôn mục 224) trước. Bài còn lại đã có mục; dạng cũ đã nằm trong tu_luan của file (bản sao lưu: scripts/logs/bai-tap-mau-bai<id>-*.json)
# nên KHÔNG dùng --giu-cu. Bài 76: 2/14 ví dụ cũ cố ý bỏ vì sai số (xem docstring build-hinh-76.py). Dừng khi lỗi.
set -e
cd /Users/MAC/Projects/thachlab
for id in 68 69 72 78; do npx tsx scripts/tao-muc-bai-tap-mau.mts --lesson $id --mau 224; done
for id in 68 69 70 71 72 73 74 76 77 78 79; do npx tsx scripts/publish-bai-tap-mau.mts --lesson $id --dry-run; done
read -p "Dry-run ổn? Enter để đăng thật, Ctrl+C để dừng " _
for id in 68 69 70 71 72 73 74 76 77 78 79; do npx tsx scripts/publish-bai-tap-mau.mts --lesson $id --yes; done
echo "Xong. Bài tập mẫu đọc từ DB lúc chạy nên không cần deploy."
