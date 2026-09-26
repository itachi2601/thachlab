#!/usr/bin/env bash
# Chạy lần lượt 5 migration đang chờ lên Supabase production.
# Chạy trên máy Mac (cần supabase CLI đã `supabase link`), KHÔNG chạy trong sandbox.
#
#   bash scripts/run-migrations.sh            # hỏi xác nhận trước từng file
#   bash scripts/run-migrations.sh --yes      # chạy thẳng, không hỏi
#   bash scripts/run-migrations.sh --only 4   # chỉ chạy file thứ 4
#
# Mỗi file ghi log ra scripts/logs/. Dừng ngay khi một file lỗi.
set -euo pipefail
cd "$(dirname "$0")/.."

FILES=(
  "supabase/migrations/20260925120000_perf_indexes.sql"
  "supabase/migrations/20260925130000_perf_rpc_gv.sql"
  "supabase/migrations/20260925140000_perf_rls.sql"
  "supabase/migrations/20260925150000_difficulty_source.sql"
  "supabase/migrations/20260925160000_mastery.sql"
  "supabase/migrations/20260926100000_rank_paragon.sql"
)

AUTO=0; ONLY=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --yes|-y) AUTO=1; shift ;;
    --only) ONLY="$2"; shift 2 ;;
    *) echo "Tham so khong hieu: $1"; exit 2 ;;
  esac
done

command -v supabase >/dev/null || { echo "Chua cai supabase CLI"; exit 1; }
[[ -f supabase/.temp/project-ref ]] || { echo "Chua 'supabase link' project"; exit 1; }
echo "Project: $(cat supabase/.temp/project-ref)"

mkdir -p scripts/logs
STAMP=$(date +%Y%m%d-%H%M%S)

for i in "${!FILES[@]}"; do
  n=$((i+1)); f="${FILES[$i]}"
  [[ -n "$ONLY" && "$ONLY" != "$n" ]] && continue
  [[ -f "$f" ]] || { echo "Thieu file: $f"; exit 1; }

  echo
  echo "=== [$n/${#FILES[@]}] $(basename "$f") ==="
  if [[ $AUTO -eq 0 ]]; then
    read -r -p "Chay file nay? [y/N] " ans
    [[ "$ans" =~ ^[yY]$ ]] || { echo "Bo qua."; continue; }
  fi

  log="scripts/logs/${STAMP}-$(basename "$f" .sql).log"
  if supabase db query --linked -f "$f" 2>&1 | tee "$log"; then
    echo "OK -> $log"
  else
    echo "LOI o file $n. Da dung. Xem $log"
    [[ "$n" == "3" ]] && echo "Rollback: supabase db query --linked -f perf/rollback/20260925140000_perf_rls.down.sql"
    exit 1
  fi
done

echo
echo "Xong. Kiem tra lai:"
echo "  npx tsx scripts/perf-compare-rpc.mts    # doi chieu RPC vs duong cu"
echo "Backfill muc do (GHI THAT, khong co dry-run) — thu nho truoc:"
echo "  npx tsx scripts/backfill-question-bank-difficulty.mts 20"
