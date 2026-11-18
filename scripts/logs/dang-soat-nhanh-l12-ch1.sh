#!/bin/bash
# Hẹn đăng ✓ Soát nhanh L12 Ch.1 (lesson 3, 4, 5) lúc 22:05 18/11/2026 — UI đã deploy 18:46 (deploy 49ecdeb8b).
# publish-bai-tap-mau.mts tự sao lưu `questions` cũ ra scripts/logs/.
cd /Users/MAC/Projects/thachlab/.claude/worktrees/kind-margulis-58c72d || exit 1
target=$(date -j -f '%Y-%m-%d %H:%M:%S' '2026-11-18 22:05:00' +%s)
now=$(date +%s)
[ "$target" -gt "$now" ] && { echo "Chờ tới 22:05 ($(( (target-now)/60 )) phút)…"; sleep $(( target-now )); }
LOG=scripts/logs/dang-soat-nhanh-l12-ch1.log
for i in 3 4 5; do
  echo "== $(date '+%F %T') lesson $i" | tee -a "$LOG"
  npx tsx scripts/publish-bai-tap-mau.mts --lesson "$i" --yes 2>&1 | tail -4 | tee -a "$LOG"
done
echo "== XONG $(date '+%F %T')" | tee -a "$LOG"
