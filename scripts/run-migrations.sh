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
  "supabase/migrations/20261011200000_streak_moi_bai.sql|Chuỗi ngày tính mọi bài đạt điểm tối thiểu (không chỉ bài thuộc nguồn RP)|ngoài giờ học sinh làm bài"
  "supabase/migrations/20261011230000_phu_dao_don_muc_chi_vi_cau_kho.sql|Đóng ~174 mục phụ đạo chỉ mở vì câu Khó (có sao lưu)|lúc nào cũng được"
  "supabase/migrations/20261012120000_kiem_tra_dau_vao.sql|Kiểm tra đầu vào cho em vào lớp trễ: bảng entry_diagnostics + 4 hàm diagnostic_*|lúc nào cũng được"
  "supabase/migrations/20261013100000_lop_avcn_anh_van_chuyen_nganh.sql|Lớp Anh văn chuyên ngành Cơ khí (avcn): môn + lớp + chương + 10 bài, chỉ Chapter 8 công bố (chỉ chèn dữ liệu)|lúc nào cũng được"
  "supabase/migrations/20261013180000_avcn_de_luyen_tap_mo_cho_moi_nguoi.sql|Gỡ gắn lớp avcn khỏi đề 914 (RLS chặn HS vì lớp vào tự do không có user_classes), có sao lưu|lúc nào cũng được"
  "supabase/migrations/20261013200000_mon_va_lop_avcn_cttc.sql|Môn và 2 lớp học phần Anh văn chuyên ngành CTTC (CĐN CGKL 23A, CĐ CK 23A)|lúc nào cũng được"
  "supabase/migrations/20261013230000_tien_trinh_day_va_moi_chan_doan.sql|Tiến trình bài dạy theo khoá (tick đã dạy + ghi chú, thầy/trợ giảng dùng chung) + RPC thầy mời em làm kiểm tra đầu vào|lúc nào cũng được"
  "supabase/migrations/20261013233000_tien_trinh_day_ds_khoa.sql|Hàm teaching_courses: danh sách khoá + lịch tuần mà thầy/trợ giảng được ghi tiến trình dạy|lúc nào cũng được"
  "supabase/migrations/20261014100000_phu_dao_dang_ky_theo_chu_de.sql|Đăng ký phụ đạo chọn 1–3 chủ đề có đủ câu bài kiểm tra, chốt 6 giờ trước, báo trợ giảng + thầy qua chuông|lúc nào cũng được"
  "supabase/migrations/20261014110000_phu_dao_diem_danh_noi_phieu.sql|Phụ đạo: điểm danh có mặt/vắng, phiếu + bài kiểm tra cuối buổi nối với buổi lịch (slot_id), RPC bảng theo dõi cho thầy|lúc nào cũng được (chạy sau 20261014100000)"
  "supabase/migrations/20261014120000_staff_sua_sdt_hoc_sinh.sql|Hàm staff_set_student_phones: thầy/TA sửa SĐT học sinh + phụ huynh trong hồ sơ|lúc nào cũng được"
  "supabase/migrations/20261014140000_chan_doan_ban_do_xuat_phat.sql|Kiểm tra đầu vào có độ chắc (3 mức) → 4 nhóm vững/chưa vững/hiểu sai/chưa biết; phụ huynh chỉ thấy bản cắt; hàm diagnostic_maps cho trợ giảng|chỉ thay hàm, chạy lúc nào cũng được"
  "supabase/migrations/20261014150000_hsg9_cd17_thien_van.sql|Khoá HSG Vật lí: thêm CĐ17 Thiên văn (ẩn), đổi CĐ14 còn gương phẳng + bóng (chỉ chèn/đổi tên)|lúc nào cũng được"
  "supabase/migrations/20261014170000_teacher_lesson_notes.sql|Bảng teacher_lesson_notes: ghi chú giáo viên lúc dạy (RLS chỉ người viết, is_staff), chỉ thêm bảng mới|lúc nào cũng được"
  "supabase/migrations/20261014150000_giao_em_cho_tro_giang.sql|Nút Giao trợ giảng: bảng ta_student_handoffs + 4 hàm ta_handoff_* + trigger tự gán mục phụ đạo mới cho trợ giảng phụ trách|chạy lúc nào cũng được (chỉ thêm bảng + hàm)"
  "supabase/migrations/20261015200000_rank_ho_so_thanh_tuu_mua.sql|Hồ sơ thành tựu mùa: thêm cột vào rank_season_results + hàm rank_snapshot_season, rank_close_season chụp đầy đủ (chỉ thêm cột/thay hàm)|lúc nào cũng được"
  "supabase/migrations/20261015180000_phu_huynh_tu_noi_con.sql|Phụ huynh tự nối với con bằng tên + ngày sinh + SĐT: bảng parent_link_attempts, parent_link_requests + 4 RPC (claim_parent_by_child_info, request_parent_link_review, review_parent_link_request, search_students_for_link)|lúc nào cũng được (chỉ thêm bảng + hàm)"
  "supabase/migrations/20261015233000_ngay_sinh_tu_dang_ky.sql|Chép ngày sinh HS khai ở /dang-ky (metadata) sang profiles.birth_date (năm 1990–2015, có sao lưu) + handle_new_user tự chép cho tài khoản mới|lúc nào cũng được (chỉ ghi cột đang NULL + thay hàm)"
  "supabase/migrations/20261015234500_staff_sua_ngay_sinh.sql|Hàm staff_set_student_birth: thầy/TA sửa ngày sinh HS (ghi profiles + metadata) ở thẻ Liên lạc gia đình|lúc nào cũng được (chỉ thêm hàm)"
  "supabase/migrations/20261016120000_ta_phong_van_phu_dao.sql|Bảng ta_interviews + hàm ta_interview_save/list: trợ giảng ghi phỏng vấn HS về kênh tự thoát phụ đạo (trang /tro-giang/phong-van)|lúc nào cũng được (chỉ thêm bảng/hàm)"
  "supabase/migrations/20261016150000_ta_diem_thay_mac_dinh_day.sql|Điểm Thầy quan sát mặc định 10 (hàm ta_monthly_policy), không còn chặn chốt tháng vì thiếu điểm này|lúc nào cũng được, chỉ đổi 1 hàm|chạy lại bản trong 20261003150000_phu_dao_kiem_tra_cuoi_buoi.sql"
  "supabase/migrations/20261016170000_ta_he_so_phu_dao_1_1_1_2.sql|Hệ số phụ đạo trợ giảng 1,1 (1–2 em) / 1,2 (3–4 em) để chi phí tăng tối đa ~10% (hàm ta_monthly_policy)|lúc nào cũng được, chỉ đổi 1 hàm|chạy lại bản trong 20261016150000_ta_diem_thay_mac_dinh_day.sql"
  "supabase/migrations/20261016130000_hsg9_dot3_muc_noi_dung.sql|Khoá HSG Vật lí: tạo mục Lý thuyết + Bài tập mẫu (rỗng) cho CĐ15 Âm (150), CĐ16 (164), CĐ12 (153), bài vẫn ẩn|lúc nào cũng được (chỉ chèn)"
  "supabase/migrations/20261017120000_rate_limit_hardening.sql|Giới hạn tần suất: bảng rate_hits + rl_allow, chặn dò resolve_login_email/quiz_join, vá search_path hàm definer|lúc nào cũng được, nhưng nên ngoài giờ HS làm bài"
  "supabase/migrations/20261017150000_reset_code_manh_hon.sql|Mã đặt lại mật khẩu RS + 10 hex (trước 6), CHECK hạn tối đa 7 ngày cho bản ghi mới|lúc nào cũng được"
)
# ĐÃ CHẠY 17/10/2026: 20261017180000_ta_giao_btvn_rieng
# ĐÃ CHẠY 15/10/2026 19:14: 20261015120000_vinh_danh_hoa_diem_xoay_vong
# ĐÃ CHẠY 14/10/2026 17:41: 20261014160000_course_mastery_radar
# ĐÃ CHẠY 13/10/2026 (00:44): 20261013150000_chapter_mastery_radar
# ĐÃ CHẠY 12/10/2026 (09:51): 20261012100000_hsg9_dot2_muc_noi_dung
# ĐÃ CHẠY 11/10/2026 (17:20): 20261011220000_phu_dao_bo_cau_kho
# ĐÃ CHẠY 11/10/2026 (16:49): 20261011210000_live_study_summary
# ĐÃ CHẠY 11/10/2026 (13:57): 20261011190000_mistake_review_mix_ok
# ĐÃ CHẠY 11/10/2026 (13:56): 20261011170000_rank_lop10_bat_nguon, 20261011170000_ta_reminders
# ĐÃ CHẠY 11/10/2026 (08:50): 20261011150000_student_mistakes_spaced_review, 20261011160000_rank_bat_nguon_thuong_chenh_lech
# ĐÃ CHẠY 11/10/2026: 20261011180000_ta_doc_ket_qua_lam_bai (dán tay vào SQL Editor), 20261010500000_notify_rp_thuong, 20261010600000_lop_hsg_vat_ly_9_duyet_tay, 20261010700000_ta_doc_thanh_vien_lop,
#   20261011100000_exam_ta_preview, 20261010800000_an_cau_cat_cut_hien_thi, 20261010150000_ta_sua_buoi_7_ngay_va_doi_anh,
#   20261011120000_question_bank_lint_flags, 20261011130000_bank_set_question_figure_service, 20261011140000_bank_replace_question_imgs
# ĐÃ CHẠY 10/10/2026 (13:11): 20261009180000_an_cau_de_hong_audit, 20261009100000_notify_exam_assigned, 20261006150000_quiz_live; 20261010200000_hsg9_dot1_muc_noi_dung bỏ qua vì DB đã có đủ mục + nội dung bài 154/155/160/162
# ĐÃ CHẠY 10/10/2026: 20261010400000_rank_chan_thuong_qua_cao, 20261010410000_rank_thu_hoi_rp_vuot (thu hồi 4.350 RP/79 dòng), 20261010420000_rank_ly_thuyet_muc_cong,
#   20261010300000_hsg_cham_nhanh (đã có bảng + 1 bài Pre-test; chạy lại báo policy tồn tại), 20261010100000_khoa_hsg9_vat_ly_khung
# ĐÃ CHẠY 8/10/2026 23:27: 20261008120000_rank_streak_week_theory_review
# ĐÃ CHẠY 5–6/10/2026 (đối chiếu log scripts/logs/, dọn khỏi FILES 7/10): 20261005140000_weakest_topics, 20261005100000_bank_grade_lop10,
#   20261005160000_push_subscriptions, 20261006120000_question_bank_dedup, 20261006120000_thpt_fee_ledger, 20261006180000_similar_bank_questions
# ĐÃ CHẠY 7/10/2026: 20261007070000_rls_backup_tables, 20261007120000_tu_vao_lop_thpt
# ĐÃ CHẠY 4/10/2026 22:58: 20261004120000_phu_dao_hang_cho, 20261004130000_phu_dao_xem_lai_ly_thuyet, 20261004230000_thpt_course_pairs
# ĐÃ CHẠY 4/10/2026: 20261004100000_bank_grade_thi_thu_tn
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
