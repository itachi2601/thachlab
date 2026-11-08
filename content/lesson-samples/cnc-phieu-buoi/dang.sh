#!/usr/bin/env bash
# Ghi 12 phiếu buổi vào cnc_lessons (flip-1 đã có → --replace, tự sao lưu; flip-2…12 thêm mới, sort_order nối tiếp).
#   bash content/lesson-samples/cnc-phieu-buoi/dang.sh --dry-run   rồi   bash content/lesson-samples/cnc-phieu-buoi/dang.sh
# Sửa lại phiếu đã có (từ 8/11/2026 cả 12 đã có): thêm --replace, vd. dang.sh --replace --dry-run
# Hoàn tác flip-2…12: delete from cnc_lessons where id in ('flip-2',…,'flip-12'); flip-1: ghi lại từ scripts/logs/cnc-flip-1-row-backup-*.json.
set -euo pipefail
cd "$(dirname "$0")/../../.."
node content/lesson-samples/cnc-phieu-buoi/build.mjs
for n in $(seq 1 12); do
  extra=""; [ "$n" = 1 ] && extra="--replace"
  npx tsx scripts/them-bai-cnc.mts content/lesson-samples/cnc-phieu-buoi/out/flip-$n.html --meta content/lesson-samples/cnc-phieu-buoi/out/flip-$n.meta.json $extra "$@" | grep -v "^Hiện có"
done
