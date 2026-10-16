#!/usr/bin/env bash
# Ghi nội dung HSG KHTN 9 đợt 3 — mảng Nhiệt – âm: lý thuyết + bài tập mẫu.
# Cần migration 20261016130000 (tạo mục rỗng cho 150, 153, 164). Mỗi bước tự sao lưu ra scripts/logs/.
#   bash scripts/dang-hsg9-dot3.sh [--yes] [cd15-am-thanh:150 cd16-truyen-nhiet-no-vi-nhiet:164 cd12-nhiet-hoc:153 …]
# Có content/hsg9/<cd>/luyen-tap/bundle.json thì ghi thêm mục luyen_tap (upload-lesson.mts --target luyen_tap).   (không truyền cặp nào = mọi CĐ đã soạn của đợt)
set -euo pipefail
cd "$(dirname "$0")/.."
Y=""; PAIRS=()
for a in "$@"; do [ "$a" = "--yes" ] && Y="--yes" || PAIRS+=("$a"); done
[ ${#PAIRS[@]} -eq 0 ] && PAIRS=("cd15-am-thanh:150")
for pair in "${PAIRS[@]}"; do
  d="${pair%%:*}"; id="${pair##*:}"
  echo "══ CĐ $d (bài $id) ══"
  bash scripts/cap-nhat-ly-thuyet.sh "content/hsg9/$d/theory.html" "$id" $Y
  npx tsx scripts/publish-bai-tap-mau.mts --lesson "$id" $Y
  lt="content/hsg9/$d/luyen-tap/bundle.json"
  if [ -f "$lt" ]; then
    # upload-lesson không có dry-run: chỉ chạy khi --yes; bundle chỉ có exam nên lý thuyết + bài tập mẫu giữ nguyên
    if [ -n "$Y" ]; then
      SUPABASE_SERVICE_ROLE_KEY="$(grep '^SUPABASE_SERVICE_ROLE_KEY=' .env.local | cut -d= -f2-)" \
        npx tsx scripts/upload-lesson.mts "$lt" --lesson "$id" --target luyen_tap
    else echo "  (luyện tập $lt: chỉ ghi khi chạy với --yes)"; fi
  fi
done
echo "Xong. Deploy để bài tập mẫu (file tĩnh) lên web: bash scripts/deploy.sh"
