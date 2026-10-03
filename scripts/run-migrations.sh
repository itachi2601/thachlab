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
)
# ĐÃ CHẠY 3/10/2026 22:57: 20261003130000_parent_attendance_announcements, 20261003140000_rank_theory_rp, 20261003150000_phu_dao_kiem_tra_cuoi_buoi
# ĐÃ CHẠY 3/10/2026 13:30: 20261003100000_rank_gate_adaptive, 20261003110000_rank_rp_first_attempt, 20261003120000_distractor_notes
# ĐÃ CHẠY (kiểm trên production 3/10/2026 13:20 — hàm tồn tại, log scripts/logs/ không lỗi): 20260930160000_rank_title_distinct_questions (nhiều lần, idempotent),
#   20260930170000_question_bank_hash_ignore_image_ts + 20260930180000_bank_similarity_per_topic (1/10, file đã bị xoá khỏi đĩa),
#   20261001100000_resolve_login_email, 20261002100000_ta_all_classes, 20261002110000_staff_student_account (2/10 23:54).
# ĐÃ CHẠY 30/9/2026 (17:15): 20260930160000_exit_quiz_bank_children.sql
# ĐÃ CHẠY 30/9/2026 (16:07): 20260930110000_rank_board_by_tier.sql, 20260930120000_rank_gd1b_spacing_progress.sql,
#   20260930130000_rank_streak_freeze.sql, 20260930140000_rank_class_goal.sql, 20260930150000_rank_teacher_reports.sql (thứ tự 1 → 5)
# ĐÃ CHẠY 30/9/2026: 20260930100000_tutoring_exit_cooldown.sql
# ĐÃ CHẠY 29/9/2026 (17:43): 20260929130000_rank_weekly_goal_adaptive.sql
# ĐÃ CHẠY 29/9/2026 (14:04): 20260929100000_rank_restore_daily_streak.sql, 20260929110000_rank_progress_week.sql,
#   20260929120000_rank_honor_progress.sql (file 3 từng bị rollback rồi chạy lại; thứ tự 1 → 2 → 3)
# ĐÃ CHẠY 28/9/2026 (23:47): 20260928190000_rank_tier_names_lien_quan.sql
# ĐÃ CHẠY 28/9/2026 (11:39):
#   20260928170000_question_results_retention.sql (pg_cron đã bật, job question-results-rollup 0 20 1 * *)
# ĐÃ CHẠY 28/9/2026 (10:55):
#   20260928150000_drop_question_bank_backup.sql
# ĐÃ CHẠY 28/9/2026 (13:46): 20260928180000_rank_public_honor_v2.sql
# ĐÃ CHẠY 28/9/2026 (11:39): 20260928160000_rank_public_honor.sql
# ĐÃ CHẠY 28/9/2026 (10:42):
#   20260928100000_rank_specialist_difficulty.sql
#   20260928130000_rank_title_code_in_class_rpcs.sql
# ĐÃ CHẠY 26–27/9/2026, không đưa vào danh sách nữa:
#   20260925120000_perf_indexes.sql
#   20260925130000_perf_rpc_gv.sql
#   20260925140000_perf_rls.sql
#   20260925150000_difficulty_source.sql
#   20260925160000_mastery.sql
#   20260926100000_rank_paragon.sql
#   20260926110000_rank_exclude_staff.sql
#   20260926120000_lesson_item_draft_publish.sql
#   20260926130000_exam_violation_alert.sql
#   20260926140000_fix_rls_tautology.sql
#   20260926150000_fix_question_bank_similarity_timeout.sql
#   20260927100000_class_announcement_exam.sql
#   20260927110000_bug_report_question_link.sql
#   20260927120000_lesson_item_summary.sql
#   20260927130000_homework_check.sql
#   20260927140000_class_review_homework.sql
#   20260927150000_exam_class_access.sql (chạy trực tiếp bằng đường dẫn tuyệt đối,
#     không qua script này vì worktree không có supabase link)

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
