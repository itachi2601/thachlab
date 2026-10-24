# Sơ đồ dữ liệu Supabase (schema public) — sinh tự động 2026-10-24

Sinh bằng `node scripts/gen-database-doc.mjs` (chỉ đọc `pg_class`/`pg_attribute`). **Không sửa
tay** — chạy lại sau khi migration mới đã chạy trên production. Danh sách hàm/RPC ở
`docs/DATABASE-RPC.md` (tách riêng vì dài, chỉ mở khi cần tên hàm hoặc chữ ký tham số).

Ký hiệu: `ten:kieu` · `*` khoá chính · `>bang` khoá ngoại · `(~n)` số dòng ước lượng của planner
(−1 = chưa ANALYZE). ts = timestamptz, int8 = bigint, num = numeric.

Xương sống THPT: `classes` → `chapters` → `lessons` → `lesson_items` (lý thuyết / luyện tập /
kiểm tra / BTVN) → `exams` ↔ `exam_attempts` (bài làm) ↔ `exam_question_results` (từng câu).
Tài khoản: `profiles` (role, track THPT/CTTC, admin_area); ghi danh lớp: `user_classes`.
Xương sống CTTC: `course_offerings` → `course_enrollments`, điểm danh `attendance_sessions`.

## Tài khoản · lớp · khoá học — 32 bảng

- **academic_subjects** (~3): code:text*, label:text, icon:text, sort_order:int, active:bool
- **class_announcements** (~1): id:int8*, class_id:int8>classes, kind:text, body:text, created_by:uuid>profiles, created_at:ts, exam_id:int8>exams
- **class_assessments** (~2): id:int8*, created_at:ts, class_id:int8>classes, exam_id:int8>exams, lesson_id:int8>lessons, kind:text, term:text, sequence:int, weight:numeric(4,2), published_at:ts, due_at:ts
- **class_homework_checks** (~-1): id:int8*, announcement_id:int8>class_announcements, student_id:uuid>profiles, percent:int, checked_by:uuid>profiles, checked_at:ts
- **class_instructors** (~1): class_id:int8*>classes, instructor_id:uuid*>profiles, assigned_by:uuid>profiles, assigned_at:ts
- **class_review_homework** (~-1): id:int8*, class_id:int8>classes, source_exam_id:int8>exams, exam_id:int8>exams, title:text, wrong_count:int, bank_count:int, created_by:uuid>profiles, created_at:ts
- **classes** (~4): id:int8*, created_at:ts, name:text, slug:text, color:text, icon:text, sort_order:int, active:bool, requires_approval:bool
- **course_enrollments** (~170): course_id:int8*>course_offerings, student_id:uuid*>profiles, enrolled_at:ts, status:text, approved_at:ts, approved_by:uuid>profiles
- **course_grade_overrides** (~11): course_id:int8*>course_offerings, student_id:uuid*>profiles, grade_key:text*, score:numeric(4,2), updated_by:uuid>profiles, updated_at:ts
- **course_instructors** (~2): course_id:int8*>course_offerings, instructor_id:uuid*>profiles, assigned_by:uuid>profiles, assigned_at:ts
- **course_offerings** (~3): id:int8*, subject_id:int8>subjects, created_by:uuid>profiles, created_at:ts, name:text, class_label:text, school_year:text, join_code:text, enrollment_mode:text, starts_at:date, ends_at:date, status:text, open_lesson_ids:text[]
- **parent_link_attempts** (~-1): id:int8*, user_id:uuid>profiles, success:bool, created_at:ts
- **parent_link_requests** (~-1): id:int8*, parent_id:uuid>profiles, child_name:text, child_birth:date, parent_phone:text, note:text, matched_student_id:uuid>profiles, status:text, reviewed_by:uuid>profiles, reviewed_at:ts, created_at:ts
- **parent_links** (~137): id:uuid*, code:text, student_id:uuid>profiles, parent_id:uuid>profiles, label:text, created_by:uuid>profiles, created_at:ts, claimed_at:ts
- **password_reset_codes** (~27): id:uuid*, code:text, student_id:uuid>profiles, method:text, created_by:uuid>profiles, created_at:ts, expires_at:ts, used_at:ts
- **profiles** (~523): id:uuid*>users, created_at:ts, full_name:text, class_name:text, role:text, student_code:text, admin_area:text, birth_date:date, track:text, display_title_code:text>rank_titles, display_title_level:text, avatar_url:text, honor_visibility:text, is_test:bool
- **staff_invites** (~7): id:uuid*, email:text, full_name:text, role:text, admin_area:text, class_id:int8>classes, course_id:int8>course_offerings, tier:text, invited_by:uuid>profiles, invited_at:ts, claimed_at:ts, claimed_user_id:uuid>users, code:text
- **staff_week_plans** (~-1): user_id:uuid*>profiles, week_start:date*, events:jsonb, warnings:jsonb, updated_at:ts
- **thpt_attendance_records** (~-1): session_id:int8*>thpt_attendance_sessions, student_id:uuid*>profiles, status:text, note:text, marked_by:uuid>profiles, marked_at:ts
- **thpt_attendance_sessions** (~-1): id:int8*, class_id:int8>classes, created_by:uuid>profiles, created_at:ts, title:text, session_date:date, starts_at:ts, note:text
- **thpt_course_schedules** (~8): id:int8*, course_id:int8>thpt_courses, weekday:smallint, start_time:time without time zone, end_time:time without time zone, location:text
- **thpt_courses** (~8): id:int8*, class_id:int8>classes, name:text, description:text, school_year:text, starts_at:date, ends_at:date, capacity:int, fee_note:text, is_public:bool, status:text, created_by:uuid>profiles, created_at:ts, current_topic_id:int8>question_topics, pair_key:text, pair_slot:text, referral_discount_pct:int
- **thpt_fee_charges** (~-1): id:int8*, plan_id:int8>thpt_fee_plans, student_id:uuid>profiles, period:date, amount_vnd:int, waived:bool, created_at:ts
- **thpt_fee_payments** (~-1): id:int8*, charge_id:int8>thpt_fee_charges, amount_vnd:int, method:text, paid_on:date, note:text, recorded_by:uuid>profiles, created_at:ts
- **thpt_fee_plans** (~-1): id:int8*, class_id:int8>classes, billing_key:text, label:text, amount_vnd:int, due_day:smallint, active:bool, created_by:uuid>profiles, created_at:ts
- **thpt_fee_settings** (~-1): id:bool*, staff_visible:bool, family_visible:bool, updated_at:ts
- **thpt_registration_requests** (~-1): id:int8*, created_at:ts, updated_at:ts, user_id:uuid>profiles, requested_class_id:int8>classes, full_name:text, username:text, email:text, phone:text, parent_phone:text, birth_date:date, gender:text, student_code:text, status:text, reviewed_by:uuid>profiles, reviewed_at:ts
- **thpt_registrations** (~2): id:int8*, course_id:int8>thpt_courses, student_id:uuid>profiles, registered_by:uuid>profiles, child_name:text, contact:text, note:text, status:text, joined_late:bool, payment_status:text, payment_note:text, created_at:ts, reviewed_by:uuid>profiles, reviewed_at:ts, known_topic_ids:bigint[], catchup_topic_ids:bigint[], catchup_done_topic_ids:bigint[]
- **thpt_teaching_notes** (~-1): id:int8*, class_id:int8>classes, topic_id:int8>question_topics, course_id:int8>thpt_courses, school_year:text, body:text, author_id:uuid>profiles, created_at:ts
- **thpt_teaching_progress** (~-1): course_id:int8*>thpt_courses, topic_id:int8*>question_topics, taught_on:date, week_start:date, taught_by:uuid>profiles, updated_at:ts
- **user_classes** (~323): user_id:uuid*>profiles, class_id:int8*>classes, status:text, requested_at:ts, reviewed_by:uuid>profiles, reviewed_at:ts
- **user_classes_backup_20261007** (~-1): user_id:uuid, class_id:int8, status:text, requested_at:ts, reviewed_by:uuid, reviewed_at:ts

## Học liệu THPT: chương · bài · mục — 8 bảng

- **chapter_classes** (~22): chapter_id:int8*>chapters, class_id:int8*>classes
- **chapters** (~22): id:int8*, created_at:ts, title:text, sort_order:int, subject_code:text>academic_subjects
- **lesson_items** (~414): id:int8*, created_at:ts, lesson_id:int8>lessons, kind:text, title:text, subtitle:text, body_html:text, video_url:text, pdf_url:text, sort_order:int, exam_ids:bigint[], questions:jsonb, due_at:ts, quiz_min_correct:int, practice_pass_score:numeric(4,2), required:bool, published_at:ts, draft_payload:jsonb, draft_saved_at:ts, summary_html:text
- **lesson_progress** (~830): user_id:uuid*>profiles, item_id:int8*>lesson_items, done_at:ts, course_id:int8>course_offerings
- **lesson_read_depth** (~414): student_id:uuid*>profiles, item_id:int8*>lesson_items, read_date:date*, lesson_id:int8>lessons, h3_max:smallint, h3_total:smallint, quiz_done:smallint, quiz_total:smallint, sends:int, first_at:ts, last_at:ts
- **lesson_read_depth_rollups** (~-1): student_id:uuid*>profiles, item_id:int8*>lesson_items, lesson_id:int8>lessons, days_read:int, h3_max:smallint, h3_total:smallint, quiz_done:smallint, quiz_total:smallint, first_at:ts, last_at:ts, updated_at:ts
- **lessons** (~155): id:int8*, created_at:ts, chapter_id:int8>chapters, title:text, sort_order:int, published:bool, lesson_kind:text, description:text, is_preview:bool
- **subjects** (~4): id:int8*, code:text, name:text, area:text, active:bool, is_practicum:bool

## Đề · câu hỏi · bài làm — 25 bảng

- **bug_reports** (~144): id:int8*, created_at:ts, updated_at:ts, user_id:uuid>profiles, reporter_name:text, reporter_email:text, page_url:text, category:text, description:text, screenshot_path:text, status:text, admin_note:text, exam_id:int8>exams, question_index:int
- **exam_attempts** (~1987): id:int8*, client_token:uuid, student_id:uuid>profiles, exam_id:int8>exams, item_id:int8>lesson_items, started_at:ts, submitted_at:ts, exam_result_id:int8>exam_results, responses:jsonb, seconds_left:int, saved_at:ts
- **exam_classes** (~877): exam_id:int8*>exams, class_id:int8*>classes
- **exam_question_results** (~42355): exam_result_id:int8*>exam_results, question_index:int*, student_id:uuid>profiles, exam_id:int8>exams, topic_id:int8>question_topics, topic_name:text, form:text, qtype:text, earned:numeric(4,2), max:numeric(4,2), is_correct:bool, estimated:bool, created_at:ts, manual_earned:numeric(4,2), manual_max:numeric(4,2), graded_by:uuid>profiles, graded_at:ts, difficulty:text
- **exam_results** (~1876): id:int8*, created_at:ts, student_id:uuid>profiles, exam_id:int8>exams, score:numeric(4,2), detail:jsonb, duration_seconds:int, course_id:int8>course_offerings, violation_count:int, violations:jsonb, client_token:uuid, results_rolled_up_at:ts
- **exam_ta_previews** (~-1): exam_id:int8*>exams, class_id:int8*>classes, sent_by:uuid>users, sent_at:ts
- **exams** (~1018): id:int8*, created_at:ts, title:text, duration_minutes:int, published:bool, questions:jsonb, question_count:int, topic:text, difficulty:text, type_counts:jsonb, subject_code:text>academic_subjects, cnc_key:text, pass_score:numeric(4,2)
- **practice_question_results** (~9466): session_id:int8*>practice_sessions, question_index:int*, student_id:uuid>profiles, exam_id:int8>exams, source_index:int, topic_id:int8>question_topics, topic_name:text, form:text, qtype:text, earned:numeric(4,2), max:numeric(4,2), is_correct:bool, created_at:ts, difficulty:text, bank_id:int8
- **practice_sessions** (~620): id:int8*, created_at:ts, student_id:uuid>profiles, lesson_id:int8>lessons, item_id:int8>lesson_items, question_count:int, correct_count:int, score:numeric(5,2), duration_seconds:int, timed_out:bool, client_token:uuid, results_rolled_up_at:ts
- **question_bank** (~29159): id:int8*, created_at:ts, updated_at:ts, subject_code:text, grade:text, topic_id:int8>question_topics, topic_name:text, form:text, qtype:text, difficulty:text, question:jsonb, content_hash:text, source_exam_id:int8>exams, source_index:int, archived:bool, note:text, figure_not_needed:bool, ai_figure:jsonb, difficulty_source:text, lint_flags:text[]
- **question_bank_audit_de_hong_20261009** (~599): id:int8, archived:bool, note:text
- **question_bank_backup_20260930** (~12984): id:int8, created_at:ts, updated_at:ts, subject_code:text, grade:text, topic_id:int8, topic_name:text, form:text, qtype:text, difficulty:text, question:jsonb, content_hash:text, source_exam_id:int8, source_index:int, archived:bool, note:text, figure_not_needed:bool, ai_figure:jsonb, difficulty_source:text
- **question_bank_cat_cut_20261010** (~181): id:int8, archived:bool, note:text
- **question_bank_dedup_backup_20261006** (~3299): id:int8, created_at:ts, updated_at:ts, subject_code:text, grade:text, topic_id:int8, topic_name:text, form:text, qtype:text, difficulty:text, question:jsonb, content_hash:text, source_exam_id:int8, source_index:int, archived:bool, note:text, figure_not_needed:bool, ai_figure:jsonb, difficulty_source:text
- **question_bank_dedup_backup_20261006b** (~278): id:int8, created_at:ts, updated_at:ts, subject_code:text, grade:text, topic_id:int8, topic_name:text, form:text, qtype:text, difficulty:text, question:jsonb, content_hash:text, source_exam_id:int8, source_index:int, archived:bool, note:text, figure_not_needed:bool, ai_figure:jsonb, difficulty_source:text
- **question_bank_dedup_backup_20261006c** (~578): id:int8, created_at:ts, updated_at:ts, subject_code:text, grade:text, topic_id:int8, topic_name:text, form:text, qtype:text, difficulty:text, question:jsonb, content_hash:text, source_exam_id:int8, source_index:int, archived:bool, note:text, figure_not_needed:bool, ai_figure:jsonb, difficulty_source:text
- **question_bank_grade_fix_20261004** (~5899): id:int8*
- **question_bank_grade_fix_20261005** (~6262): id:int8*
- **question_dang** (~1573): question_id:int8*>question_bank, lesson_id:int8*>lessons, dang_label:text, source:text, unsure:bool, created_at:ts
- **question_result_rollups** (~-1): id:int8*, student_id:uuid>profiles, source:text, topic_id:int8>question_topics, topic_name:text, form:text, qtype:text, difficulty:text, attempted:int, correct:int, earned:num, max:num, first_at:ts, last_at:ts, updated_at:ts
- **question_topics** (~254): id:int8*, created_at:ts, subject_code:text, grade:text, chapter_id:int8>chapters, lesson_id:int8>lessons, name:text, sort_order:int, parent_id:int8>question_topics
- **rubric_exam_attempts** (~63): id:int8*, course_id:int8>course_offerings, student_id:uuid>profiles, machine:text, role:text, grader_id:uuid>profiles, item_levels:jsonb, zero_tolerance_confirmed:jsonb, ky_thuat_score:num, thanh_phan_score:num, total_score:num, xep_loai:text, notes:text, created_at:ts, updated_at:ts
- **tutoring_exit_attempts** (~2): id:int8*, tutoring_need_id:int8>tutoring_needs, student_id:uuid>profiles, topic_id:int8, form:text, question_ids:bigint[], total:int, correct:int, pct:int, passed:bool, created_at:ts, window_id:uuid>tutoring_exit_windows
- **tutoring_exit_attempts_backup_20260930** (~-1): id:int8, question_ids:bigint[]
- **tutoring_exit_windows** (~-1): id:uuid*, assistant_id:uuid>ta_assistants, class_id:int8, student_ids:uuid[], topic_ids:bigint[], opened_at:ts, closes_at:ts, created_at:ts, slot_id:int8>tutoring_slots

## Rank · huy hiệu — 21 bảng

- **rank_fix_attempts** (~8): id:int8*, student_id:uuid>profiles, season_id:int8>rank_seasons, exam_result_id:int8>exam_results, exam_id:int8>exams, topic_id:int8>question_topics, question_ids:bigint[], total:int, correct:int, pct:int, passed:bool, status:text, created_at:ts, submitted_at:ts, responses:jsonb
- **rank_fix_attempts_backup_20260930** (~-1): id:int8, question_ids:bigint[]
- **rank_gate_attempts** (~39): id:int8*, season_id:int8>rank_seasons, student_id:uuid>profiles, tier_code:text, status:text, question_ids:bigint[], answers:jsonb, pool_ids:bigint[], level_cur:text, correct:int, total:int, hard_correct:int, pct:int, passed:bool, level_end:text, created_at:ts, submitted_at:ts
- **rank_gate_passes** (~232): season_id:int8*>rank_seasons, student_id:uuid*>profiles, tier_code:text*, passed_at:ts, evidence:jsonb
- **rank_rp_awards** (~3682): season_id:int8*>rank_seasons, student_id:uuid*>profiles, source_kind:text*, source_ref:text*, awarded:int, best_value:numeric(6,2), updated_at:ts
- **rank_rp_awards_backup_20261010** (~79): season_id:int8, student_id:uuid, source_kind:text, source_ref:text, awarded:int, best_value:numeric(6,2), updated_at:ts, new_awarded:int, note:text, backed_up_at:ts
- **rank_rp_ledger** (~4116): id:int8*, season_id:int8>rank_seasons, student_id:uuid>profiles, source_kind:text, source_ref:text, amount:int, reason:text, ref_result_id:int8, actor:uuid>profiles, created_at:ts
- **rank_season_results** (~0): season_id:int8*>rank_seasons, student_id:uuid*>profiles, rp:int, tier_code:text, division:int, titles_count:int, closed_at:ts, tier_sort:int, tier_name:text, class_names:text, season_titles:jsonb, weeks_goal_met:int, weekly_rp:jsonb, mastered_topic_ids:bigint[], mastered_count:int, snapshot_at:ts
- **rank_seasons** (~2): id:int8*, created_at:ts, created_by:uuid>profiles, name:text, starts_on:date, ends_on:date, class_ids:bigint[], status:text, config:jsonb, boss_exam_id:int8>exams, boss_pass_score:numeric(4,2), closed_at:ts
- **rank_sources** (~857): season_id:int8*>rank_seasons, source_kind:text*, source_id:int8*, max_rp:int, enabled:bool
- **rank_sources_backup_20261011** (~340): season_id:int8, source_kind:text, source_id:int8, max_rp:int, backed_up_at:ts
- **rank_sources_backup_20261017** (~364): season_id:int8, source_kind:text, source_id:int8, max_rp:int, backed_up_at:ts
- **rank_sources_backup_20261017b** (~-1): season_id:int8, source_kind:text, source_id:int8, max_rp:int, backed_up_at:ts
- **rank_sources_backup_20261020** (~-1): season_id:int8, source_kind:text, source_id:int8, max_rp:int, backed_up_at:ts
- **rank_student_seasons** (~282): season_id:int8*>rank_seasons, student_id:uuid*>profiles, rp:int, tier_code:text, tier_sort:int, division:int, tier_reached_at:ts, joined_at:ts, updated_at:ts
- **rank_tier_floor** (~-1): season_id:int8*>rank_seasons, student_id:uuid*>profiles, tier_code:text, tier_sort:int, reason:text, created_at:ts
- **rank_tiers** (~14): season_id:int8*>rank_seasons, code:text*, sort:int, name:text, min_rp:int, has_divisions:bool, required_title_count:int, required_title_level:text, challenge_exam_id:int8>exams, challenge_pass_score:numeric(4,2), gate_pass_pct:int, gate_min_hard_correct:int, gate_min_level_held:text
- **rank_tiers_backup_20261017** (~-1): season_id:int8, code:text, min_rp:int, backed_up_at:ts
- **rank_title_awards** (~970): id:int8*, student_id:uuid>profiles, title_code:text>rank_titles, level:text, season_id:int8>rank_seasons, evidence:jsonb, awarded_at:ts
- **rank_title_topics** (~71): title_code:text*>rank_titles, topic_id:int8*>question_topics
- **rank_titles** (~45): code:text*, group_code:text, kind:text, name:text, description:text, sort:int, min_questions:int, awaken_accuracy:int, master_accuracy:int, legend_challenge_exam_id:int8>exams, legend_accuracy:int, requires:jsonb, enabled:bool, min_de:int, min_tb:int, min_kho:int

## Phụ đạo · thông báo · bài đăng — 13 bảng

- **messages** (~-1): id:int8*, created_at:ts, sender_id:uuid>profiles, recipient_id:uuid>profiles, class_name:text, subject:text, body:text
- **notifications** (~1375): id:int8*, user_id:uuid>profiles, kind:text, title:text, body:text, href:text, created_at:ts, read_at:ts, pushed_at:ts
- **post_classes** (~-1): post_id:int8*>posts, class_id:int8*>classes
- **post_courses** (~-1): post_id:int8*>posts, course_id:int8*>course_offerings
- **posts** (~1): id:int8*, created_at:ts, title:text, body:text, video_url:text, published:bool, topic:text, content_type:text, subject_code:text>academic_subjects
- **student_alerts** (~370): id:int8*, student_id:uuid>profiles, class_id:int8>classes, kind:text, severity:text, reason:text, assessment_ids:bigint[], status:text, assigned_to:uuid>profiles, handled_by:uuid>profiles, handled_note:text, created_at:ts, updated_at:ts
- **tutoring_needs** (~1079): id:int8*, student_id:uuid>profiles, class_id:int8>classes, topic_id:int8>question_topics, form:text, wrong:int, total:int, pct:int, source:text, status:text, assigned_to:uuid>profiles, note:text, first_seen_at:ts, last_seen_at:ts, tutored_at:ts, cleared_at:ts, updated_at:ts
- **tutoring_needs_backup_20261011** (~174): id:int8*, status:text, cleared_at:ts, note:text
- **tutoring_registrations** (~-1): id:int8*, slot_id:int8>tutoring_slots, student_id:uuid>profiles, created_at:ts, topic_ids:bigint[], attended:bool, attended_at:ts
- **tutoring_session_topics** (~112): id:int8*, session_id:uuid>ta_sessions, student_id:uuid>profiles, topic_id:int8>question_topics, need_id:int8>tutoring_needs, note:text, created_at:ts
- **tutoring_slots** (~-1): id:int8*, assistant_id:uuid>ta_assistants, class_id:int8>classes, work_date:date, start_time:time without time zone, end_time:time without time zone, topic_ids:bigint[], capacity:int, registered_count:int, note:text, status:text, created_at:ts
- **tutoring_theory_reviews** (~118): tutoring_need_id:int8*>tutoring_needs, student_id:uuid>profiles, item_id:int8>lesson_items, started_at:ts, last_ping_at:ts, active_seconds:int, required_seconds:int, sections_total:int, sections_seen:int, quiz_total:int, quiz_answered:int, completed_at:ts
- **tutoring_waitlist** (~-1): id:int8*, slot_id:int8>tutoring_slots, student_id:uuid>profiles, created_at:ts, topic_ids:bigint[]

## CTTC: CNC · điểm danh · checklist · máy — 25 bảng

- **attendance_machine_photos** (~-1): id:int8*, session_id:int8>attendance_sessions, machine_code:text, checkpoint:text, storage_path:text, note:text, uploaded_by:uuid>profiles, created_at:ts
- **attendance_machine_scores** (~3): session_id:int8*>attendance_sessions, machine_code:text*, bonus_points:int, note:text, updated_at:ts, sang_loc:bool, sap_xep:bool, sach_se:bool, san_soc:bool, san_sang:bool, equipment_status:text
- **attendance_records** (~472): session_id:int8*>attendance_sessions, student_id:uuid*>profiles, status:text, checked_in_at:ts, note:text, marked_by:uuid>profiles, updated_at:ts, bonus_points:int, machine_code:text, machine_selected_at:ts
- **attendance_session_machines** (~8): session_id:int8*>attendance_sessions, machine_code:text*>machines
- **attendance_sessions** (~14): id:int8*, course_id:int8>course_offerings, created_by:uuid>profiles, created_at:ts, title:text, session_date:date, starts_at:ts, late_after:ts, closes_at:ts, code:text, status:text, note:text, machine_selection_open:bool, machine_edit_override:bool, workshop:text, period:text
- **checklist_attempts** (~-1): id:int8*, session_id:int8>checklist_sessions, course_id:int8>course_offerings, lesson_id:text, student_id:uuid>profiles, grader_id:uuid>profiles, grader_role:text, item_results:jsonb, score:num, total:num, critical_ok:bool, zero_tolerance_ok:bool, passed:bool, created_at:ts, started_at:ts, duration_seconds:int
- **checklist_sessions** (~4): id:int8*, course_id:int8>course_offerings, lesson_id:text, created_by:uuid>profiles, created_at:ts, title:text, starts_at:ts, closes_at:ts, code:text, status:text
- **checklist_work_starts** (~-1): session_id:int8*>checklist_sessions, course_id:int8>course_offerings, lesson_id:text, student_id:uuid*>profiles, grader_id:uuid*>profiles, started_at:ts
- **cnc_competency_permissions** (~176): course_id:int8*>course_offerings, student_id:uuid*>profiles, competency_id:text*, status:text, note:text, approved_by:uuid>profiles, approved_at:ts, updated_at:ts
- **cnc_drawing_submissions** (~33): id:int8*, created_at:ts, updated_at:ts, student_id:uuid>profiles, lesson_id:text, file_name:text, storage_path:text, mime_type:text, size_bytes:int8, status:text, teacher_feedback:text, reviewed_by:uuid>profiles, reviewed_at:ts, course_id:int8>course_offerings
- **cnc_learning_records** (~395): course_id:int8*>course_offerings, student_id:uuid*>profiles, lesson_id:text*, assessment_id:text*, completed:bool, latest_score:int, best_score:int, total_questions:int, attempt_count:int, last_activity_at:ts
- **cnc_lesson_files** (~5): id:int8*, created_at:ts, lesson_id:text, kind:text, title:text, file_name:text, file_url:text, storage_path:text, mime_type:text, size_bytes:int8
- **cnc_lesson_videos** (~9): id:int8*, created_at:ts, lesson_id:text, title:text, youtube_url:text, youtube_id:text, sort_order:int
- **cnc_lessons** (~8): id:text*, title:text, short_title:text, duration_label:text, emphasis:text, body_html:text, resources:jsonb, sort_order:int, created_at:ts
- **cnc_milling_checklist_attempts** (~-1): id:int8*, student_id:uuid>profiles, participant_key:uuid, participant_name:text, class_name:text, checked:jsonb, zero_tolerance:jsonb, score:numeric(4,1), max_score:numeric(4,1), critical_passed:bool, zero_tolerance_passed:bool, status:text, started_at:ts, last_activity_at:ts, passed_at:ts
- **cnc_milling_quiz_attempts** (~18): id:int8*, student_id:uuid>profiles, answers:jsonb, answered_count:int, score:int, total_questions:int, status:text, started_at:ts, last_activity_at:ts, submitted_at:ts, participant_key:uuid, participant_name:text, class_name:text, course_id:int8>course_offerings
- **cnc_quiz_questions** (~110): id:text*, quiz_key:text, question_type:text, question:text, options:jsonb, correct_index:int, keywords:jsonb, min_keyword_matches:int, explanation:text, order_index:int, updated_by:uuid>profiles, updated_at:ts
- **equipment_breakdown_reports** (~-1): id:int8*, course_id:int8>course_offerings, session_id:int8>attendance_sessions, machine_code:text, description:text, broken_photo_path:text, status:text, reported_by:uuid>profiles, resolved_by:uuid>profiles, resolved_at:ts, resolved_note:text, created_at:ts, resolved_photo_path:text, broken_at:ts, assigned_to:uuid>profiles
- **homeroom_daily_attendance** (~-1): id:int8*, course_id:int8>course_offerings, attendance_date:date, headcount:int, present_count:int, absentees:jsonb, submitted_by:uuid>profiles, submitted_at:ts, updated_at:ts
- **homeroom_monitors** (~1): course_id:int8*>course_offerings, student_id:uuid*>profiles, role:text, assigned_by:uuid>profiles, assigned_at:ts
- **homeroom_term_records** (~-1): course_id:int8*>course_offerings, student_id:uuid*>profiles, term:text*, exam_score:numeric(4,2), conduct:text, note:text, updated_by:uuid>profiles, updated_at:ts
- **homeroom_weekly_sessions** (~3): id:int8*, course_id:int8>course_offerings, week_no:int, met_on:date, announcements:jsonb, ethics_topic:text, ethics_taught:jsonb, headcount:int, present_count:int, created_by:uuid>profiles, created_at:ts, updated_at:ts
- **machine_status_log** (~104): id:int8*, machine_code:text>machines, status:text, note:text, created_by:uuid>profiles, updated_by:uuid>profiles, created_at:ts, updated_at:ts
- **machines** (~92): code:text*, label:text, machine_type:text, is_active:bool, created_at:ts, workshop:text, status:text, note:text
- **student_learning_presence** (~1): student_id:uuid*>profiles, lesson_id:int8>lessons, activity_type:text, lesson_opened_at:ts, last_seen_at:ts

## Trợ giảng — 15 bảng

- **ta_assistant_classes** (~7): assistant_id:uuid*>ta_assistants, class_id:int8*>classes, assigned_by:uuid>profiles, assigned_at:ts
- **ta_assistants** (~6): id:uuid*, user_id:uuid>users, full_name:text, short_name:text, tier:text, retained_rate:int, bank_name:text, bank_account:text, active:bool, started_at:date, created_at:ts
- **ta_flags** (~-1): id:uuid*, assistant_id:uuid>ta_assistants, flag_date:date, note:text, created_at:ts
- **ta_homework_assignments** (~-1): id:int8*, class_id:int8>classes, student_id:uuid>profiles, exam_id:int8>exams, note:text, due_at:ts, assigned_by:uuid>profiles, created_at:ts
- **ta_interviews** (~-1): id:uuid*, assistant_id:uuid>ta_assistants, code:text, grp:text, answers:jsonb, barrier:text, wish:text, created_at:ts, updated_at:ts
- **ta_leads** (~-1): id:uuid*, student_name:text, source:text, attributed_session_id:uuid>ta_sessions, registered_at:date, created_by:uuid>users, created_at:ts
- **ta_month_reviews** (~-1): assistant_id:uuid*>ta_assistants, month:date*, scores:jsonb, hourly_rate:int, note:text, closed_at:ts, snapshot:jsonb, updated_by:uuid>users, updated_at:ts
- **ta_policy_audit** (~128): id:int8*, assistant_id:uuid, month:date, actor_id:uuid, action:text, before_value:jsonb, after_value:jsonb, created_at:ts
- **ta_rates** (~3): id:uuid*, tier:text, effective_from:date, base_rate:int
- **ta_reminders** (~-1): id:int8*, assistant_id:uuid>ta_assistants, week_start:date, level:smallint, items:jsonb, title:text, body:text, notification_id:int8>notifications, created_at:ts
- **ta_sessions** (~69): id:uuid*, assistant_id:uuid>ta_assistants, work_date:date, session_type:text, class_label:text, start_time:time without time zone, end_time:time without time zone, hours:num, student_touches:int, touch_names:text[], error_note:text, error_note_at:ts, homework_given:text, student_recap_ok:bool, papers_graded:int, video_url:text, video_tier:text, published_at:ts, topic_source_id:uuid>ta_sessions, note:text, status:text, reject_reason:text, created_at:ts, approved_at:ts, phudao_students:text[], policy:jsonb, class_id:int8>classes, phudao_student_ids:uuid[], slot_id:int8>tutoring_slots
- **ta_settings** (~1): id:bool*, course_hours_cap:int, updated_at:ts
- **ta_student_handoffs** (~-1): student_id:uuid*>profiles, assistant_id:uuid>ta_assistants, assigned_by:uuid>profiles, created_at:ts
- **ta_video_rates** (~1): id:uuid*, effective_from:date, price_don_gian:int, price_dung_ky:int, view_threshold_1:int, view_bonus_1:int, view_threshold_2:int, view_bonus_2:int, lead_bonus:int, monthly_budget_cap:int
- **ta_video_stats** (~-1): id:uuid*, session_id:uuid>ta_sessions, checked_at:date, views:int, saves:int, comments:int, created_at:ts

## Khác — 25 bảng

- **_bak_exam_classes_avcn_20261013** (~-1): exam_id:int8, class_id:int8
- **_bak_profiles_birth_20261015** (~142): id:uuid*, copied_at:ts
- **entry_diagnostics** (~-1): id:int8*, student_id:uuid>profiles, per_topic:jsonb, need_count:int, created_at:ts
- **feature_flags** (~-1): flag:text*, class_id:int8*>classes, enabled:bool, note:text, created_by:uuid>profiles, created_at:ts
- **hsg_grade_sheets** (~-1): id:int8*, test_id:int8>hsg_grade_tests, student_name:text, class_name:text, answers:jsonb, scores:jsonb, total:num, graded_by:uuid>profiles, created_at:ts, updated_at:ts
- **hsg_grade_tests** (~-1): id:int8*, title:text, kind:text, config:jsonb, created_by:uuid>profiles, created_at:ts, archived:bool
- **learning_events** (~-1): id:int8*, student_id:uuid>profiles, lesson_id:int8>lessons, item_id:int8>lesson_items, kind:text, duration_s:int, occurred_at:ts
- **public_stats_cache** (~-1): id:smallint*, computed_at:ts, stats:jsonb
- **push_subscriptions** (~31): id:int8*, student_id:uuid>profiles, endpoint:text, p256dh:text, auth_key:text, remind_hour:smallint, enabled:bool, last_sent_at:ts, created_at:ts
- **quiz_answers** (~-1): room_id:int8>quiz_rooms, player_id:int8*>quiz_players, q_index:int*, choice:int, correct:bool, points:int, answered_at:ts
- **quiz_ch3_l12_bank_backup_20261021** (~158): id:int8, archived:bool, note:text, backed_up_at:ts
- **quiz_ch3_l12_sources_backup_20261021** (~-1): season_id:int8, source_kind:text, source_id:int8, max_rp:int, backed_up_at:ts
- **quiz_players** (~-1): id:int8*, room_id:int8>quiz_rooms, nickname:text, token:uuid, joined_at:ts
- **quiz_rooms** (~-1): id:int8*, created_at:ts, pin:text, set_id:int8>quiz_sets, host_id:uuid>profiles, title:text, questions:jsonb, time_limit_sec:int, status:text, current_index:int, question_started_at:ts
- **quiz_sets** (~-1): id:int8*, created_at:ts, updated_at:ts, owner_id:uuid>profiles, title:text, grade:text, questions:jsonb, banked_at:ts
- **rate_hits** (~44): id:int8*, key:text, hit_at:ts
- **referrals** (~-1): id:int8*, created_at:ts, referrer_user_id:uuid>profiles, referred_request_id:int8>trial_requests, status:text
- **review_sessions** (~5): id:int8*, created_at:ts, class_id:int8>classes, created_by:uuid>profiles, title:text, threshold:int, stages:jsonb, current_stage:int, stage_started_at:ts, extra_seconds:int, status:text
- **student_mistake_review_attempts** (~57): id:int8*, student_id:uuid>profiles, season_id:int8>rank_seasons, mistake_ids:bigint[], answers:jsonb, correct_count:int, total:int, rp_awarded:int, status:text, created_at:ts, submitted_at:ts, ok_items:jsonb
- **student_mistakes** (~6075): id:int8*, student_id:uuid>profiles, exam_id:int8>exams, question_index:int, topic_id:int8>question_topics, form:text, difficulty:text, mistake_count:int, consecutive_correct:int, stage:int, cleared:bool, last_wrong_at:ts, last_reviewed_at:ts, next_review_at:ts, created_at:ts
- **teacher_lesson_notes** (~-1): id:int8*, created_at:ts, updated_at:ts, user_id:uuid>profiles, lesson_id:int8>lessons, item_id:int8>lesson_items, page_key:text, page_heading:text, tag:text, body:text, status:text, resolution:text
- **theory_quiz_keys** (~93): item_id:int8*>lesson_items, enabled:bool, answers:jsonb, challenge:jsonb, est_read_seconds:int, updated_at:ts
- **theory_reviews** (~-1): student_id:uuid*>profiles, item_id:int8*>lesson_items, round:int*, opened_at:ts, submitted_at:ts, correct:int, total:int, awarded:int, result:text
- **theory_sessions** (~631): student_id:uuid*>profiles, item_id:int8*>lesson_items, opened_at:ts, submitted_at:ts, correct:int, total:int, awarded:int, result:text
- **trial_requests** (~-1): id:int8*, created_at:ts, parent_name:text, phone:text, grade:smallint, school:text, preferred_evenings:text[], note:text, source:text, status:text, handled_by:uuid>profiles, handled_at:ts

