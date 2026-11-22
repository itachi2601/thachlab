#!/usr/bin/env bash
# Gói A dụng cụ đo + sửa sai số bài 3 (22/11/2026): tải clip tn-l10-sai-so-02 bản mới, deploy code, đăng lý thuyết 4 bài.
# CHỈ chạy sau 22h (ghi DB + Storage). Chạy trong checkout chính trên Mac:
#   bash scripts/video-thi-nghiem/dang-goi-a.sh            # xem thử: kiểm clip, in việc sẽ làm, không ghi gì
#   bash scripts/video-thi-nghiem/dang-goi-a.sh --yes      # ghi thật
# Thứ tự bắt buộc: clip lên Storage trước (bài 48 trỏ tới tn-l10-sai-so-02-<ngày UTC>.mp4), deploy code (MoPhongPortals
# có 4 khoá mới) rồi mới đăng bài; đăng trước deploy thì hộp mô phỏng hiện trống tới khi hosting kéo bản mới.
set -u
cd "$(dirname "$0")/../.."
YES="${1:-}"
MP4="${MP4:-/Users/MAC/Projects/thachlab/.claude/worktrees/goi-a-dung-cu-do-438e16/scripts/video-thi-nghiem/ra/tn-l10-sai-so-02.mp4}"
NGAY=$(date -u +%Y%m%d)
URL="https://jgvbdbpvjdntdgzthumv.supabase.co/storage/v1/object/public/lesson-clips/clip/tn-l10-sai-so-02-$NGAY.mp4"

[ -f "$MP4" ] || { echo "Thiếu clip $MP4"; exit 1; }
grep -q "tn-l10-sai-so-02-$NGAY.mp4" content/lesson-samples/l10-thuc-hanh-sai-so/bundle.json \
  || { echo "bundle.json bài 48 không trỏ tới -$NGAY.mp4 (ngày UTC khác 22/11?) → báo lại, đừng đăng"; exit 1; }

if [ "$YES" != "--yes" ]; then
  npx tsx scripts/tai-clip-len-storage.mts "$MP4" --tn tn-l10-sai-so-02 --toi-da 55 \
    --nhan "Một thước kẻ, hai vật đo: sai số so nhau thế nào?" --nhin-vao "Sai số dụng cụ do đâu mà có?"
  echo "Xem thử xong. Sẽ: tải clip → $URL · deploy · đăng lý thuyết bài 48, 47, 51, 45. Chạy lại với --yes sau 22h."
  exit 0
fi

h=$(date +%H); if [ "$h" -lt 22 ] && [ "$h" -ge 6 ]; then echo "Mới $h giờ: chỉ chạy sau 22h hoặc trước 6h."; exit 1; fi

echo "== 1. Tải clip $(date '+%H:%M:%S')"
npx tsx scripts/tai-clip-len-storage.mts "$MP4" --tn tn-l10-sai-so-02 --toi-da 55 \
  --nhan "Một thước kẻ, hai vật đo: sai số so nhau thế nào?" --nhin-vao "Sai số dụng cụ do đâu mà có?" --apply || exit 1
curl -sfI "$URL" >/dev/null || { echo "Clip chưa mở được: $URL"; exit 1; }
git add content/thi-nghiem/tn-l10-sai-so-02.json && git commit -q -m "Kho TN sai-so-02: video bản $NGAY (ΔA = 1 ĐCNN)" -- content/thi-nghiem/tn-l10-sai-so-02.json && git push -q origin main

echo "== 2. Deploy $(date '+%H:%M:%S')"
bash scripts/deploy.sh || exit 1
echo "Chờ 10 phút cho hosting kéo bản mới…"; sleep 600

echo "== 3. Đăng lý thuyết $(date '+%H:%M:%S')"
for p in "l10-thuc-hanh-sai-so 48" "l10-an-toan-phong-thuc-hanh 47" "l10-thuc-hanh-do-toc-do 51" "l11-thuc-hanh-do-sdd-pin 45"; do
  set -- $p
  echo "===== bài $2 ($1)"
  bash scripts/cap-nhat-ly-thuyet.sh "content/lesson-samples/$1/bundle.json" "$2" --yes || echo "LỖI bài $2"
done
echo "XONG $(date '+%H:%M:%S') · kiểm: curl -sI $URL"
