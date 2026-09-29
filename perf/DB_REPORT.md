# DB_REPORT — index & RLS (Agent B, nhánh `perf/db-index`, 25/9/2026)

Nguồn sự thật: catalog thật của project qua `supabase db query --linked` (chỉ SELECT): `pg_indexes` (227 index), `pg_policies` (260 policy), `pg_constraint` (204 khoá ngoại), `pg_stat_user_tables`, `information_schema.columns`. PostgreSQL **17.6** (chưa có btree skip-scan → index kép chỉ dùng được khi lọc từ cột đầu). Code quét bằng script trên `services/ lib/ components/ app/ features/` (981 lời gọi `.from/.eq/.in/.order/...`, 60 `.rpc`).

Sản phẩm: `supabase/migrations/20260925120000_perf_indexes.sql` — **7 index**, idempotent, đã chạy thử trên pglite (schema stub) 2 lần + chạy block rollback → sạch.

## 0. Kích thước & mức "nóng" (pg_stat_user_tables)

| Bảng | n_live_tup | size | seq_scan | idx_scan | Ghi chú |
|---|---:|---:|---:|---:|---|
| question_bank | 10 841 | 27 MB | 76 | 293 147 | bảng lớn nhất, ngân hàng câu hỏi |
| exam_question_results | 7 207 | 1.8 MB | 22 | 18 436 | tăng nhanh nhất (≈ 40 dòng / lần nộp bài) |
| practice_question_results | 434 | 192 kB | 25 | 1 | |
| attendance_records | 411 | 216 kB | 42 | 27 579 | |
| cnc_learning_records | 395 | 168 kB | 2 024 | 7 224 | |
| profiles | 349 | 176 kB | 685 | **2 848 862** | ≈ toàn bộ là `is_admin()` gọi trong policy (xem §3) |
| lesson_items | 262 | 792 kB | 21 533 | 467 264 | ~3 KB/dòng (HTML) |
| question_topics | 238 | 176 kB | **296 862** | 53 873 | seq scan do hash-join với eqr trong RPC rank/tutoring — bảng 10 trang, planner chọn đúng, không phải thiếu index |
| exam_results | 228 | 312 kB | 54 | 31 715 | |
| user_classes | 193 | 104 kB | 292 | 11 177 | |
| exams | 175 | 5.3 MB | 20 652 | 38 317 | JSON câu hỏi TOAST; seq scan từ `.in("id", …)` nhiều id |
| exam_classes | 172 | 56 kB | 35 632 | 27 948 | 172 dòng — seq scan là tối ưu |
| tutoring_needs | 149 | 144 kB | 43 | 912 | |
| lesson_progress | 128 | 24 kB | 4 | 6 048 | |
| course_enrollments | 112 | 88 kB | 16 412 | 11 447 | seq scan từ policy `e.course_id = e.course_id` (§3.4) |
| exam_attempts | 83 | 144 kB | 27 | 6 782 | |
| chapter_classes | 22 | 56 kB | 71 091 | 27 677 | 22 dòng — seq scan là tối ưu |

Kết luận chung: **DB rất nhỏ** (mọi bảng < 11k dòng). Lợi ích của index ở đây chủ yếu là (a) tránh Sort + đọc heap trên `question_bank`, (b) tránh đọc HTML 3 KB/dòng ở `lesson_items`, (c) lookup gọn trong trigger/RPC chạy sau mỗi lần nộp bài. Chi phí RLS (§3) lớn hơn chi phí thiếu index nhiều lần.

## 1. Cột bị lọc / sắp xếp theo bảng (từ code)

Ký hiệu: `=`/`in`/`↓` = eq / in / order. **Đậm** = chưa có index phù hợp. Bảng danh mục nhỏ (classes, chapters, lessons, subjects, rank_tiers/titles/sources, machines, ta_*, cnc_lessons…) lọc chủ yếu theo PK hoặc không lọc — bỏ qua.

| Bảng | Cột lọc / sắp xếp | Nơi gọi | Index sẵn có |
|---|---|---|---|
| exam_question_results | `=student_id` | analytics.ts:110 | eqr_student_exam_idx ✓ |
| | `=exam_id in student_id` | analytics.ts:298, :339 | eqr_exam_correct_idx / eqr_student_exam_idx ✓ |
| | `=exam_result_id` | rank.ts:121 | pkey ✓ |
| | **`=qtype is graded_at null in student_id`** | progress.ts:444 | → idx_eqr_pending_essay |
| | RPC: `student_id` (rank_title_stats, refresh_tutoring_needs, student_outcome_gaps), `exam_result_id` | rank-system.sql, tutoring-needs.sql, phu-huynh.sql | ✓ |
| practice_question_results | chỉ insert (lessons.ts:382); RPC không lọc | | pkey, pqr_student_idx, pqr_topic_idx ✓ |
| exam_attempts | **`=student_id =exam_id is submitted_at null ↓started_at`** | progress.ts:308 (mỗi lần mở đề) | → idx_exam_attempts_student_exam_open |
| | **`in student_id in exam_id is submitted_at null`** | progress.ts:95 | (cùng index trên) |
| | `=client_token` (update) | progress.ts:286, :334 | unique ✓ |
| exam_results | `=student_id ↓created_at` | analytics.ts:77, lessons.ts:274, progress.ts:380 | exam_results_student_idx ✓ |
| | `=student_id` | lessons.ts:183, :236 | ✓ |
| | `in student_id ↓created_at` | class-results.ts:16 | ✓ |
| | **`in student_id in exam_id`** | progress.ts:86 | → idx_exam_results_student_exam_created |
| | `=exam_id in student_id` | analytics.ts:253, :758 | exam_results_exam_idx ✓ (hoặc index mới) |
| | `=client_token` | progress.ts:347 | unique ✓ |
| | `in id` | analytics.ts:153 | pkey ✓ |
| | RPC: **`student_id = ? and exam_id = ?`** (rank_best_pct, evaluate_student_alerts, sweep_missed_assessments, refresh_tutoring_needs — trigger sau mỗi lần nộp) | | → index mới |
| lesson_progress | `=user_id` / `in user_id in item_id` | lessons.ts:197, :235, progress.ts:82, :368 | pkey (user_id, item_id) ✓ |
| lesson_items | `=lesson_id ↓sort_order` | lessons.ts:111 | lesson_items_lesson_idx ✓ |
| | **`in lesson_id` chỉ lấy id, lesson_id, exam_ids** | lessons.ts:209, :234 (trang /lop-hoc, trang chủ HS) | → idx_lesson_items_lesson_cover (index-only) |
| | `in kind ↓sort_order` | rank.ts:318 (admin) | bỏ qua (kind ít giá trị) |
| | `=lesson_id contains exam_ids` | LessonImporter.tsx:431 (admin) | lesson_idx ✓ |
| question_topics | **`in name`** | ExamRunner.tsx:197 (mỗi lần nộp), lessons.ts:363 | → idx_question_topics_name |
| | `in id` | rank.ts:128, :133 | pkey ✓ |
| | `↓grade ↓sort_order ↓name` (toàn bảng) | analytics.ts:574 | question_topics_grade_idx (subject_code, grade, sort_order) — không khớp thứ tự; 238 dòng, bỏ qua |
| | `parent_id` (RPC, trigger topic-outcomes, rank.ts:131 gián tiếp) | | question_topics_parent_idx (parent_id, sort_order) ✓ — **đã có, không cần thêm** |
| | `coalesce(parent_id,id) = ?` (rank_evaluate_titles "Phá Đảo Chuyên Đề") | rank-system.sql:852-860 | expression index — cân nhắc, bỏ (238 dòng, hash join) |
| question_bank | **`=grade =archived [=form =qtype =difficulty] ↓topic_id ↓source_exam_id ↓source_index limit 500`** | question-bank.ts:85-103 | grade_idx (subject_code, grade, archived) KHÔNG dùng được → idx_question_bank_grade_archived_browse |
| | `in topic_id` (+grade, archived) | question-bank.ts:97 | question_bank_topic_idx ✓ |
| | **`=grade '' =archived false` (count)** | question-bank.ts:143 | → index mới |
| | `in id` | question-bank.ts:112, :202 | pkey ✓ |
| | `ilike question->>question` | question-bank.ts:104 | không index được (dùng `%…%`); RPC find_similar dùng gin trgm ✓ |
| | view question_bank_topic_counts: group by grade, topic_id, archived | question-bank.ts:127 | → index mới cho index-only scan |
| tutoring_needs | `in student_id [in status] ↓pct` | tutoring.ts:111 | tutoring_needs_student_idx (student_id, status) ✓ |
| | `=student_id ↓status ↓pct` | tutoring.ts:123 | ✓ |
| | policy question_bank: `student_id = uid and topic_id = ? and status in …` | | unique (student_id, topic_id, form) ✓ |
| tutoring_slots | `=class_id =status ≥work_date ↓work_date ↓start_time` | tutoring.ts:322 | tutoring_slots_class_idx (class_id, work_date, start_time) ✓ |
| | `=assistant_id =class_id` | tutoring.ts:336 | class_idx rồi lọc — 0 dòng, bỏ qua |
| tutoring_registrations / _session_topics / _exit_attempts | slot_id, student_id, need+student | tutoring.ts:394-426, :230 | ✓ đủ |
| rank_rp_ledger | (season_id, student_id, created_at) — rank_class_board, rank_my_status | RPC | rank_rp_ledger_student_idx ✓ |
| rank_title_awards | student_id, (student_id, title_code, level) | RPC | ✓ |
| rank_student_seasons / gate_passes / rp_awards / season_results | (season_id, student_id) | RPC | pkey ✓ |
| rank_fix_attempts | `=exam_result_id` | rank.ts:149 | rank_fix_attempts_result_idx ✓ |
| rank_sources | `=season_id =source_kind =source_id` | rank.ts:189, RPC join | pkey ✓ |
| attendance_records | `=session_id` | course-attendance.ts:90 | pkey ✓ |
| | `=student_id` (+ join sessions.course_id) | course-attendance.ts:126 | attendance_records_student_idx ✓ |
| | **`=machine_code ↓sessions.session_date limit 30`** | course-attendance.ts:27 | → idx_attendance_records_machine_code |
| attendance_sessions | `=course_id ↓starts_at` | course-attendance.ts:37 | course_date_idx ✓ |
| thpt_attendance_sessions / _records | class_id ↓starts_at; session_id | class-attendance.ts:26, :58 | ✓ |
| course_enrollments | `=course_id ↓enrolled_at` | course-enrollments.ts:61 | pkey prefix ✓ |
| | `=student_id in status ↓enrolled_at` (+ !inner course_offerings/subjects) | course-enrollments.ts:84, :96, :114 | student_idx ✓ |
| | `in student_id` / không lọc | classes.ts:255, :293 | ✓ / seq |
| profiles | `=id`, `in id` | AuthProvider.tsx:122, student-profile.ts | pkey ✓ |
| | `in id =track` | classes.ts:248 | pkey + lọc ✓ |
| | `=role [in status] ↓full_name` | classes.ts:281, course-instructors.ts:13, MessagesAdmin.tsx:50 | role 4 giá trị / 349 dòng — seq scan hợp lý, bỏ qua |
| user_classes | `=user_id =status` / `=class_id =status [↓requested_at]` | classes.ts:123, :139, :206, learning-presence.ts:36 | pkey / user_classes_status_idx ✓ |
| exams | `=published in id` | lessons.ts:150-173 | pkey ✓ |
| | `=published ↓created_at` (+ exam_classes) | content.ts:40 | 175 dòng — bỏ qua |
| | `=id` | nhiều nơi | pkey ✓ |
| student_alerts | `in student_id ↓updated_at` / `=student_id` | analytics.ts:421, :433 | (student_id, kind) unique ✓ |
| student_learning_presence | `in student_id ≥last_seen_at ↓last_seen_at` | learning-presence.ts:45 | pkey(student_id) + last_seen_idx ✓ |
| notifications | `↓created_at` (RLS lọc user_id) | notifications.ts:18 | notifications_user_idx ✓ |
| class_announcements | `=class_id [=kind] ↓created_at` | announcements.ts:48, :68 | class_idx ✓ |
| practice_sessions | `=student_id ↓created_at`, `in student_id in item_id`, `=client_token` | progress.ts:103, :352, :374 | student_idx ✓ (item_id lọc sau — 31 dòng, bỏ qua) |
| thpt_courses / _registrations / _schedules | class_id+status, course_id+status, is_public+status | thpt-courses.ts | ✓ (8 dòng) |
| cnc_* / checklist_* / rubric_* / homeroom_* / machine_status_log / equipment_* / bug_reports / parent_links / messages / staff_invites / ta_* | course_id, student_id, session_id, status, machine_code… | services/*.ts, lib/tro-giang | ✓ đã có index từ migration gốc; bảng ≤ 400 dòng |

### Khoá ngoại chưa có index (95/204) — chỉ đáng lưu ý
Đa số là cột audit (`created_by`, `updated_by`, `approved_by`, `reviewed_by`, `marked_by`, `assigned_by`…) trên bảng ≤ 400 dòng: chỉ ảnh hưởng khi **xoá** dòng cha (profiles) → seq scan bảng con để kiểm tra FK. Không thêm. Đáng nhắc:
- `exam_question_results.graded_by → profiles` (7 207 dòng): xoá tài khoản giáo viên sẽ seq scan bảng này một lần — chấp nhận được.
- `question_topics.lesson_id / chapter_id`, `tutoring_needs.topic_id / assigned_to`, `practice_question_results.exam_id`, `exam_attempts.exam_result_id / item_id`, `exam_results.course_id`, `lesson_progress.course_id / item_id`, `exam_classes.class_id`, `chapter_classes.class_id`: **code không lọc riêng cột này** (chỉ lọc kèm cột đầu đã có index, hoặc bảng ≤ 240 dòng) → không thêm.

## 2. Index đề xuất (đã viết trong migration)

| # | Index | Bảng | Kiểu | Vì sao |
|---|---|---|---|---|
| 1 | `idx_question_bank_grade_archived_browse (grade, archived, topic_id, source_exam_id, source_index)` | question_bank (10.8k) | kép 5 cột, khớp WHERE + ORDER BY | bỏ Seq Scan 10k dòng + Sort; LIMIT 500 dừng sớm; view topic_counts index-only. **Lợi nhất.** |
| 2 | `idx_exam_attempts_student_exam_open (student_id, exam_id, started_at desc) where submitted_at is null` | exam_attempts | kép + partial | mở đề nào cũng gọi findOpenExamAttempt; index chỉ chứa bài dở |
| 3 | `idx_exam_results_student_exam_created (student_id, exam_id, created_at desc)` | exam_results | kép | lookup (HS, đề) ở client + 4 RPC/trigger sau mỗi lần nộp bài |
| 4 | `idx_question_topics_name (name)` | question_topics | đơn | `.in("name", …)` mỗi lần nộp bài / lưu luyện tập |
| 5 | `idx_lesson_items_lesson_cover (lesson_id) include (id, exam_ids)` | lesson_items | covering | index-only scan, không đọc HTML 3 KB/dòng ở /lop-hoc |
| 6 | `idx_eqr_pending_essay (student_id) where qtype='essay' and graded_at is null` | exam_question_results | partial | câu tự luận chờ chấm — gần rỗng |
| 7 | `idx_attendance_records_machine_code (machine_code) where machine_code is not null` | attendance_records | partial | trang tình trạng máy |

Đã cân nhắc rồi **bỏ** (tránh index thừa): `exams (created_at) where published` (175 dòng), `profiles (role)` (4 giá trị), `practice_sessions (student_id, item_id)` (31 dòng), `question_topics (coalesce(parent_id,id))` (238 dòng, planner hash-join), `exam_classes.class_id`, `chapter_classes.class_id`, `question_topics(parent_id)` (đã có `question_topics_parent_idx`), `tutoring_needs(topic_id)` (đã có unique (student_id, topic_id, form)).

Index hiện có **có thể thừa** (chỉ gợi ý, chưa động): `question_bank_grade_idx (subject_code, grade, archived)` — code không lọc `subject_code` trên question_bank; sau khi index #1 chạy vài ngày, xem `pg_stat_user_indexes.idx_scan` rồi quyết định drop.

## 3. RLS

### 3.1 Số liệu
- 260 policy trên 95 bảng. `is_admin()` xuất hiện **184 lần**, `auth.uid()` trực tiếp trong thân policy **104 lần / 85 policy** (0 policy dùng dạng `(select auth.uid())`), `rank_is_staff()` 10, `ta_current_assistant_id()` 10, `vn_today()` 3.
- Mọi hàm helper (`is_admin`, `manages_class`, `assists_class`, `teaches_student`, `is_parent_of`, `is_course_member`, `can_manage_course`, `rank_is_staff`, `ta_current_assistant_id`, `thpt_has_registration`) đều đã `stable security definer` **nhưng bên trong vẫn gọi `auth.uid()` trần** và đều là `language sql` → planner inline thành subquery chạy **mỗi dòng**. Bằng chứng: `profiles.idx_scan = 2 848 862` (gấp 8 000 lần số dòng) — đó là `is_admin()` chạy lặp.

### 3.2 Policy gọi `auth.uid()` trực tiếp — 85 policy, 41 bảng (nguồn: pg_policies; file docs tương ứng là `docs/supabase-migration-<module>.sql`)

| Bảng | Số | Policy (cmd) |
|---|---|---|
| user_classes | 3 | read own user classes (S) · students request own class (I) · students resubmit rejected class request (U) |
| tutoring_registrations | 3 | student cancels self (D) · student reads own registration (S) · student registers self (I) |
| rubric_exam_attempts | 3 | students manage own self rubric attempt (I) · students read own (S) · students update own self (U) |
| profiles | 3 (+2 EXISTS) | parent updates own profile (U) · read own profile (S) · update own profile (U) · assigned instructors read student profiles (S) · instructors read enrolled student profiles (S) |
| notifications | 3 | delete own (D) · mark own read (U) · read own (S) |
| exam_attempts | 3 | student inserts own attempt (I) · student reads own attempts (S) · student updates own open attempt (U) |
| cnc_drawing_submissions | 3 | students read own (S) · students resubmit rejected (U) · students submit own (I) |
| exam_results | 3 | assigned instructors read student results (S, EXISTS) · student inserts own result (I) · student reads own results (S) |
| exam_question_results | 2 | student inserts own question results (I) · student reads own question results (S) |
| practice_sessions / practice_question_results | 2+2 | student inserts own … (I) · student reads own … (S) |
| tutoring_exit_attempts | 2 | read own exit attempts (S) · student logs own exit attempt (I) |
| messages | 2 | admin sends messages (I) · read own messages (S — kèm subquery `select class_name from profiles where id = auth.uid()`) |
| bug_reports | 2 | anyone reports bug (I) · read own or admin bug reports (S) |
| attendance_machine_photos / attendance_machine_scores / attendance_sessions / checklist_sessions / course_offerings / equipment_breakdown_reports | 1 mỗi bảng | students read … (S, EXISTS course_enrollments e … e.student_id = auth.uid()) |
| attendance_records · checklist_attempts · class_instructors · cnc_competency_permissions · cnc_learning_records · course_enrollments · course_grade_overrides · course_instructors · homeroom_monitors · homeroom_term_records · lesson_progress · parent_links · ta_assistants · thpt_attendance_records · thpt_registration_requests(2) · thpt_registrations · tutoring_needs · student_alerts · student_learning_presence(2) | 1–2 | "read own …" / "manages own …" dạng `col = auth.uid() [or is_admin()/teaches_student()]` |
| class_announcements | 2 | staff post announcements (I) · students read class announcements (S, EXISTS user_classes) |
| question_bank · question_topics | 1+1 | staff manage … (ALL, EXISTS profiles p where p.id = auth.uid() and role='instructor' and admin_area='thpt') — đây chính là thân của `rank_is_staff()` viết lặp lại |
| question_bank | 1 | student reads exit-quiz bank questions (S, EXISTS tutoring_needs) |
| rank_fix_attempts · rank_gate_passes · rank_rp_awards · rank_rp_ledger · rank_season_results · rank_student_seasons · rank_title_awards | 1 mỗi bảng | read own … (S): `student_id = auth.uid() or teaches_student(student_id) or is_parent_of(student_id)` |
| thpt_attendance_sessions | 2 | assigned instructors manage (ALL, EXISTS class_instructors) · students read own class (S, EXISTS user_classes) |
| thpt_courses | 1 | anyone reads public courses (S) |
| tutoring_slots | 2 | assistant manages own slots (ALL, EXISTS ta_assistants) · class reads own slots (S, EXISTS user_classes) |
| tutoring_session_topics | 2 | assistant writes own coverage (ALL, EXISTS ta_sessions⋈ta_assistants) · read tutoring coverage (S) |

### 3.3 Đề xuất cho Agent E (Pha 2) — CHƯA làm gì ở nhánh này
1. **Đổi `auth.uid()` → `(select auth.uid())`** ở tất cả 85 policy trên và **trong thân 10 hàm helper**. Với hàm SQL `stable`, viết `(select auth.uid())` để planner coi là InitPlan (tính 1 lần/câu lệnh). Ưu tiên theo lưu lượng: profiles, exam_results, exam_question_results, lesson_progress, exam_attempts, notifications, user_classes, tutoring_needs, rank_* (7 bảng), practice_*.
2. **Gom subquery lặp thành hàm helper** (`security definer stable`, thân dùng `(select auth.uid())`):
   - `is_course_member(course_id)` đã có nhưng 6 policy (attendance_machine_photos, attendance_machine_scores, attendance_sessions, checklist_sessions, course_offerings, equipment_breakdown_reports) vẫn viết tay `exists (select 1 from course_enrollments e where … e.student_id = auth.uid() and e.status='active')` → thay bằng hàm.
   - `rank_is_staff()` đã có nhưng policy `staff manage question bank` / `staff manage question topics` viết lại nguyên thân → thay bằng hàm.
   - 4 policy "assigned instructors read …" (exam_results, profiles, student_learning_presence, thpt_attendance_records) lặp `exists (user_classes uc join class_instructors ci …)` = thân `teaches_student()` (thiếu phần trợ giảng) → dùng `teaches_student(student_id)`.
   - `is_class_member(class_id)` mới: 4 policy (class_announcements, thpt_attendance_sessions, tutoring_slots, tutoring_registrations) lặp `exists (select 1 from user_classes uc where uc.user_id = auth.uid() and uc.class_id = … and uc.status='active')`.
   - `is_thpt_instructor()`/`is_staff()` cache: `is_admin()` gọi 184 lần; cân nhắc `current_setting('request.jwt.claims')` để đọc role từ JWT (cần đưa role vào app_metadata) — thay đổi lớn hơn, chỉ gợi ý.
3. **profiles** có 10 policy chồng nhau (7 SELECT được OR lại, 4 trong đó có EXISTS/join; 3 UPDATE) — mỗi lần AuthProvider đọc `profiles where id = uid` đều đánh giá cả 7. Gợi ý gộp thành 1 policy SELECT gọi 1 hàm `can_read_profile(id)`.

### 3.4 Policy có vẻ nới quyền bất thường (chỉ ghi nhận, KHÔNG sửa)
- **`attendance_sessions` — "students read course attendance sessions"** và **`equipment_breakdown_reports` — "students read equipment breakdown reports"**: điều kiện `e.course_id = e.course_id` (so sánh chính nó, luôn đúng) thay vì `e.course_id = attendance_sessions.course_id` → **mọi sinh viên có 1 enrollment active đọc được buổi điểm danh / báo hỏng máy của MỌI khoá**. Cũng là lý do course_enrollments có 16k seq scan. Cần thầy xác nhận sửa (Agent E hoặc hotfix riêng).
- `class_assessments` — "anyone reads class assessments": `true` cho mọi tài khoản đăng nhập (kể cả lớp khác). Có thể chủ ý (analytics.ts:81 đọc toàn bảng không lọc class_id).
- `thpt_course_schedules` — "anyone reads public schedules" (role public): chỉ kiểm tra tồn tại `thpt_courses c where c.id = course_id`; an toàn nhờ RLS của thpt_courses lồng bên trong, nhưng phụ thuộc ngầm.
- `cnc_milling_quiz_attempts` / `cnc_milling_checklist_attempts`: anon INSERT/UPDATE/SELECT (lớp học trực tiếp không đăng nhập) — chủ ý, nhưng anon UPDATE có thể sửa attempt của người khác nếu đoán được id.
- `question_topics`, `lesson_items`, `exam_classes`, `chapter_classes`, `chapters`, `lessons (published)`, `posts (published)`: role public đọc toàn bộ — chủ ý (static export), ghi nhận.

## 4. EXPLAIN mẫu — thầy chạy trước/sau migration (SQL Editor, chỉ đọc)

Thay `<uuid>` bằng id một học sinh thật, `<exam>` bằng id đề. Chạy 2 lần, lấy lần 2 (cache ấm).

```sql
-- (1) Ngân hàng câu hỏi lớp 12, trang đầu — kỳ vọng: Seq Scan + Sort  →  Index Scan using idx_question_bank_grade_archived_browse, không còn "Sort"
explain (analyze, buffers)
select id, topic_id, source_exam_id, source_index from public.question_bank
where grade = '12' and archived = false
order by topic_id asc nulls last, source_exam_id asc, source_index asc limit 500;

-- (2) Bài đang dở của 1 HS trên 1 đề — kỳ vọng: Index Scan using idx_exam_attempts_student_exam_open, rows=1, Buffers shared hit ≤ 4
explain (analyze, buffers)
select client_token, seconds_left from public.exam_attempts
where student_id = '<uuid>' and exam_id = <exam> and submitted_at is null
order by started_at desc limit 1;

-- (3) Điểm tốt nhất của (HS, đề) như rank_best_pct — kỳ vọng: Index Only/Index Scan using idx_exam_results_student_exam_created thay vì exam_results_student_idx + Filter exam_id
explain (analyze, buffers)
select max(score) from public.exam_results where student_id = '<uuid>' and exam_id = <exam>;

-- (4) Đếm mục theo bài cho /lop-hoc — kỳ vọng: "Index Only Scan using idx_lesson_items_lesson_cover", Heap Fetches: 0 (sau khi autovacuum đã chạy)
explain (analyze, buffers)
select id, lesson_id, exam_ids from public.lesson_items
where lesson_id in (select id from public.lessons where chapter_id = 1);

-- (5) Tra chủ đề theo tên lúc nộp bài — kỳ vọng: Bitmap Index Scan on idx_question_topics_name (bảng 238 dòng nên planner có thể vẫn chọn Seq Scan — chấp nhận)
explain (analyze, buffers)
select id, name from public.question_topics where name in ('Định luật Ohm', 'Sóng cơ');
```

Cách đọc: dòng đầu là node gốc; `Seq Scan on X` = đọc cả bảng, `Index Scan using Y` / `Index Only Scan` = đi index (Only = không chạm heap, xem `Heap Fetches`); `Filter:` = điều kiện phải lọc trên từng dòng sau khi đọc (càng ít càng tốt, so `rows` với `Rows Removed by Filter`); `Sort` biến mất nghĩa là index đã cho đúng thứ tự; `Buffers: shared hit=N` = số trang 8 KB đọc — chỉ số ổn định nhất để so trước/sau (thời gian trên Supabase free dao động nhiều). Muốn thấy chi phí RLS thật, chạy cùng truy vấn với `set role authenticated; set request.jwt.claims = '{"sub":"<uuid>","role":"authenticated"}';` trong cùng phiên rồi `reset role;` — sẽ thấy `SubPlan`/`InitPlan` của policy; sau Pha 2 (Agent E) `SubPlan` (mỗi dòng) phải chuyển thành `InitPlan` (một lần).

## 5. Rủi ro & việc còn lại

- **Chi phí ghi**: 7 index; 3 partial gần rỗng; index #1 (question_bank, 5 cột) và #3 (exam_results) tốn thêm ~1 lần ghi index mỗi insert — không đáng kể ở quy mô này. Dung lượng thêm ước < 2 MB tổng.
- **Khoá bảng**: `create index` (không concurrently) khoá ghi bảng trong lúc tạo; với bảng ≤ 11k dòng là < 100 ms. Nên chạy ngoài giờ học sinh làm bài cho chắc.
- **Index-only scan** (#5) chỉ có tác dụng khi visibility map đã được autovacuum cập nhật; sau khi thầy sửa nhiều lesson_items thì vài phút đầu vẫn có Heap Fetches.
- `supabase/migrations/` là thư mục mới; `supabase db push` sẽ **không** biết 99 migration cũ → chỉ chạy tay file này trên Dashboard (hoặc `supabase db query --linked -f`), không push.
- **Cần thầy quyết**: (a) sửa 2 policy tautology `e.course_id = e.course_id` (§3.4) — lỗ hổng đọc chéo khoá; (b) `class_assessments` đọc toàn bộ có chủ ý không; (c) có drop `question_bank_grade_idx` sau khi theo dõi `idx_scan`.
- **Việc còn lại (Pha 2, Agent E)**: §3.3 — `(select auth.uid())` + helper; đo lại bằng mục 4 (đặc biệt `profiles.idx_scan` phải ngừng tăng theo tốc độ hàng nghìn/phút).
