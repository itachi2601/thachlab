#!/usr/bin/env bash
# Chạy lần lượt các migration đang chờ lên Supabase production.
# Chạy trên máy Mac (cần supabase CLI đã `supabase link`), KHÔNG chạy trong sandbox.
#
#   bash scripts/run-migrations.sh            # hỏi xác nhận trước từng file
#   bash scripts/run-migrations.sh --yes      # chạy thẳng, không hỏi
#   bash scripts/run-migrations.sh --only 4   # chỉ chạy file thứ 4
#   bash scripts/run-migrations.sh --list     # chỉ xem danh sách, không chạy
#
# Mỗi file ghi log ra scripts/logs/. Dừng ngay khi một file lỗi.
# Quy tắc cho agent: xem AGENTS.md mục "Migration Supabase".
set -euo pipefail
cd "$(dirname "$0")/.."

# "<đường dẫn>|<mô tả ngắn>|<ghi chú thời điểm chạy>"
FILES=(
  # Trống — không có migration nào đang chờ (cập nhật 26/9/2026 17:28).
  # Thêm dòng mới theo mẫu: "<đường dẫn>|<mô tả ngắn>|<thời điểm nên chạy>"
)
# ĐÃ CHẠY 26/9/2026, không đưa vào danh sách nữa:
#   20260925120000_perf_indexes.sql
#   20260925130000_perf_rpc_gv.sql
#   20260925140000_perf_rls.sql
#   20260925150000_difficulty_source.sql
#   20260925160000_mastery.sql
#   20260926100000_rank_paragon.sql
#   20260926110000_rank_exclude_staff.sql
#   20260926120000_lesson_item_draft_publish.sql
#   20260926130000_exam_violation_alert.sql

AUTO=0; ONLY=""; LIST=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --yes|-y) AUTO=1; shift ;;
    --only) ONLY="$2"; shift 2 ;;
    --list|-l) LIST=1; shift ;;
    *) echo "Tham so khong hieu: $1"; exit 2 ;;
  esac
done

if [[ $LIST -eq 1 ]]; then
  printf '%s\n' "Cac migration dang cho:"
  for i in "${!FILES[@]}"; do
    IFS='|' read -r f desc when <<< "${FILES[$i]}"
    printf '  %d. %-52s %s  [%s]\n' "$((i+1))" "$(basename "$f")" "$desc" "$when"
  done
  exit 0
fi

command -v supabase >/dev/null || { echo "Chua cai supabase CLI"; exit 1; }
[[ -f supabase/.temp/project-ref ]] || { echo "Chua 'supabase link' project"; exit 1; }
echo "Project: $(cat supabase/.temp/project-ref)"
echo "Tong: ${#FILES[@]} file."
[[ ${#FILES[@]} -eq 0 ]] && { echo "Khong co migration nao dang cho."; exit 0; }

mkdir -p scripts/logs
STAMP=$(date +%Y%m%d-%H%M%S)

for i in "${!FILES[@]}"; do
  n=$((i+1))
  IFS='|' read -r f desc when <<< "${FILES[$i]}"
  [[ -n "$ONLY" && "$ONLY" != "$n" ]] && continue
  [[ -f "$f" ]] || { echo "Thieu file: $f"; exit 1; }

  echo
  echo "=== [$n/${#FILES[@]}] $(basename "$f") ==="
  echo "    $desc"
  echo "    Thoi diem: $when"


  if [[ $AUTO -eq 0 ]]; then
    read -r -p "    Chay file nay? [y/N] " ans
    [[ "$ans" =~ ^[yY]$ ]] || { echo "    Bo qua."; continue; }
  fi

  log="scripts/logs/${STAMP}-$(basename "$f" .sql).log"
  if supabase db query --linked -f "$f" 2>&1 | tee "$log"; then
    echo "    OK -> $log"
  else
    echo "    LOI o file $n. Da dung. Xem $log"
    down="perf/rollback/$(basename "$f" .sql).down.sql"
    [[ -f "$down" ]] && echo "    Rollback: supabase db query --linked -f $down"
    exit 1
  fi
done

echo
echo "Xong. Kiem tra lai:"
echo "  npx tsx scripts/perf-compare-rpc.mts    # doi chieu RPC vs duong cu"
echo "Backfill muc do (GHI THAT, khong co dry-run) — thu nho truoc:"
echo "  npx tsx scripts/backfill-question-bank-difficulty.mts 20"
