# RLS_REPORT — auth.uid() → (select auth.uid()) (Agent E, nhánh `perf/rpc-gv`, 25/9/2026)

Nguồn: `pg_policies` + `pg_get_functiondef` đọc trực tiếp từ project (`supabase db query --linked`, chỉ SELECT). Sinh bằng script, không viết tay. **85 policy** trên **53 bảng** và **18 hàm helper** (`stable security definer language sql`), tổng **124 chỗ** `auth.uid()` trần được bọc thành `(select auth.uid())`.

Kiểm chứng máy: với mỗi policy/hàm, `undo(new) == old` (gỡ `(select …)` ra thì bằng đúng chuỗi cũ) — script assert, nên **điều kiện logic không đổi**, tên/roles/cmd/permissive giữ nguyên. Migration: `supabase/migrations/20260925140000_perf_rls.sql`; rollback: `perf/rollback/20260925140000_perf_rls.down.sql` (định nghĩa cũ). Đã chạy thử cả hai trên pglite với schema stub (xem cuối).

## 1. Hàm helper

| Hàm | Số chỗ | Trước (đoạn quanh `auth.uid()`) | Sau |
|---|---:|---|---|
| `assists_class` | 1 | `…d = p_class and a.user_id = auth.uid() and a…` | `…d = p_class and a.user_id = (select auth.uid()) and a…` |
| `can_manage_class` | 1 | `…lass_id and instructor_id = auth.uid() ); …` | `…lass_id and instructor_id = (select auth.uid()) ); …` |
| `can_manage_course` | 1 | `…urse_id and instructor_id = auth.uid() ); …` | `…urse_id and instructor_id = (select auth.uid()) ); …` |
| `get_periodic_rank` | 1 | `…public.get_periodic_rank_of(auth.uid(), p_cl…` | `…public.get_periodic_rank_of((select auth.uid()), p_cl…` |
| `is_admin` | 1 | `…lic.profiles where id = auth.uid() and r…` | `…lic.profiles where id = (select auth.uid()) and r…` |
| `is_course_member` | 1 | `…_course_id and student_id = auth.uid() and s…` | `…_course_id and student_id = (select auth.uid()) and s…` |
| `is_homeroom_classmate` | 1 | `…ofile_id and m.student_id = auth.uid() ); …` | `…ofile_id and m.student_id = (select auth.uid()) ); …` |
| `is_homeroom_monitor` | 1 | `…_course_id and student_id = auth.uid() ); …` | `…_course_id and student_id = (select auth.uid()) ); …` |
| `is_parent_of` | 1 | `…links where parent_id = auth.uid() and s…` | `…links where parent_id = (select auth.uid()) and s…` |
| `manages_class` | 1 | `…lass and ci.instructor_id = auth.uid() ); …` | `…lass and ci.instructor_id = (select auth.uid()) ); …` |
| `rank_is_staff` | 1 | `…profiles p where p.id = auth.uid() and p…` | `…profiles p where p.id = (select auth.uid()) and p…` |
| `rank_my_status` | 1 | `…elect public.rank_status_of(auth.uid()); $fu…` | `…elect public.rank_status_of((select auth.uid())); $fu…` |
| `rank_my_titles` | 1 | `…elect public.rank_titles_of(auth.uid()); $fu…` | `…elect public.rank_titles_of((select auth.uid())); $fu…` |
| `student_outcome_gaps` | 1 | `…) as s(id) where s.id = auth.uid() or pu…` | `…) as s(id) where s.id = (select auth.uid()) or pu…` |
| `ta_current_assistant_id` | 1 | `…_assistants where user_id = auth.uid(); $fun…` | `…_assistants where user_id = (select auth.uid()); $fun…` |
| `teaches_student` | 2 | `…dent and ci.instructor_id = auth.uid() ) o…`<br>`…= p_student and a.user_id = auth.uid() and a…` | `…dent and ci.instructor_id = (select auth.uid()) ) o…`<br>`…= p_student and a.user_id = (select auth.uid()) and a…` |
| `thpt_has_registration` | 2 | `…d and (r.student_id = auth.uid() …`<br>`… or r.registered_by = auth.uid() …` | `…d and (r.student_id = (select auth.uid()) …`<br>`… or r.registered_by = (select auth.uid()) …` |
| `unread_notification_count` | 1 | `…tifications where user_id = auth.uid() and r…` | `…tifications where user_id = (select auth.uid()) and r…` |

Hàm `stable` viết bằng plpgsql (get_exam_rank, rank_class_board, rank_can_view…) và mọi hàm `volatile` (submit_*, thpt_register, ta_*…) **không đổi**: plpgsql không được planner inline nên `auth.uid()` trong đó đã chỉ chạy 1 lần / câu lệnh.

## 2. Policy (theo bảng)

| Bảng | Policy | cmd | Số chỗ | Trước → Sau (mỗi chỗ) |
|---|---|---|---:|---|
| attendance_machine_photos | students read attendance machine photos | SELECT | 1 | `…rse_id) AND (e.student_id = auth.uid()) AND …` → `…rse_id) AND (e.student_id = (select auth.uid())) AND …` |
| attendance_machine_scores | students read attendance machine scores | SELECT | 1 | `…rse_id) AND (e.student_id = auth.uid()) AND …` → `…rse_id) AND (e.student_id = (select auth.uid())) AND …` |
| attendance_records | students read own attendance | SELECT | 1 | `((student_id = auth.uid()) OR i…` → `((student_id = (select auth.uid())) OR i…` |
| attendance_sessions | students read course attendance sessions | SELECT | 1 | `…rse_id) AND (e.student_id = auth.uid()) AND …` → `…rse_id) AND (e.student_id = (select auth.uid())) AND …` |
| bug_reports | anyone reports bug | INSERT | 1 | `…r_id IS NULL) OR (user_id = auth.uid()))` → `…r_id IS NULL) OR (user_id = (select auth.uid())))` |
| bug_reports | read own or admin bug reports | SELECT | 1 | `((user_id = auth.uid()) OR i…` → `((user_id = (select auth.uid())) OR i…` |
| checklist_attempts | students read own or graded checklist attempts | SELECT | 2 | `…is_admin() OR (student_id = auth.uid()) OR (…` → `…is_admin() OR (student_id = (select auth.uid())) OR (…`<br>`…auth.uid()) OR (grader_id = auth.uid()))` → `…(select auth.uid())) OR (grader_id = (select auth.uid())))` |
| checklist_sessions | students read course checklist sessions | SELECT | 1 | `…rse_id) AND (e.student_id = auth.uid()) AND …` → `…rse_id) AND (e.student_id = (select auth.uid())) AND …` |
| class_announcements | staff post announcements | INSERT | 1 | `((created_by = auth.uid()) AND …` → `((created_by = (select auth.uid())) AND …` |
| class_announcements | students read class announcements | SELECT | 1 | `…s uc WHERE ((uc.user_id = auth.uid()) AND …` → `…s uc WHERE ((uc.user_id = (select auth.uid())) AND …` |
| class_instructors | instructors read own class assignments | SELECT | 1 | `((instructor_id = auth.uid()) OR i…` → `((instructor_id = (select auth.uid())) OR i…` |
| cnc_competency_permissions | students read own competency permissions | SELECT | 1 | `((student_id = auth.uid()) OR i…` → `((student_id = (select auth.uid())) OR i…` |
| cnc_drawing_submissions | students read own cnc drawings | SELECT | 1 | `((student_id = auth.uid()) OR i…` → `((student_id = (select auth.uid())) OR i…` |
| cnc_drawing_submissions | students resubmit rejected cnc drawings | UPDATE | 2 | `((student_id = auth.uid()) AND …` → `((student_id = (select auth.uid())) AND …`<br>`((student_id = auth.uid()) AND …` → `((student_id = (select auth.uid())) AND …` |
| cnc_drawing_submissions | students submit own cnc drawings | INSERT | 1 | `((student_id = auth.uid()) AND …` → `((student_id = (select auth.uid())) AND …` |
| cnc_learning_records | students read own cnc learning records | SELECT | 1 | `((student_id = auth.uid()) OR i…` → `((student_id = (select auth.uid())) OR i…` |
| course_enrollments | students read own enrollment | SELECT | 1 | `((student_id = auth.uid()) OR i…` → `((student_id = (select auth.uid())) OR i…` |
| course_grade_overrides | students read own course grade overrides | SELECT | 1 | `((student_id = auth.uid()) OR i…` → `((student_id = (select auth.uid())) OR i…` |
| course_instructors | instructors read own assignments | SELECT | 1 | `((instructor_id = auth.uid()) OR i…` → `((instructor_id = (select auth.uid())) OR i…` |
| course_offerings | students read joined courses | SELECT | 1 | `…ngs.id) AND (e.student_id = auth.uid())))))` → `…ngs.id) AND (e.student_id = (select auth.uid()))))))` |
| equipment_breakdown_reports | students read equipment breakdown reports | SELECT | 1 | `…rse_id) AND (e.student_id = auth.uid()) AND …` → `…rse_id) AND (e.student_id = (select auth.uid())) AND …` |
| exam_attempts | student inserts own attempt | INSERT | 1 | `(student_id = auth.uid())` → `(student_id = (select auth.uid()))` |
| exam_attempts | student reads own attempts | SELECT | 1 | `((student_id = auth.uid()) OR t…` → `((student_id = (select auth.uid())) OR t…` |
| exam_attempts | student updates own open attempt | UPDATE | 2 | `((student_id = auth.uid()) AND …` → `((student_id = (select auth.uid())) AND …`<br>`(student_id = auth.uid())` → `(student_id = (select auth.uid()))` |
| exam_question_results | student inserts own question results | INSERT | 1 | `(student_id = auth.uid())` → `(student_id = (select auth.uid()))` |
| exam_question_results | student reads own question results | SELECT | 1 | `((student_id = auth.uid()) OR t…` → `((student_id = (select auth.uid())) OR t…` |
| exam_results | assigned instructors read student results | SELECT | 1 | `…id) AND (ci.instructor_id = auth.uid()))))` → `…id) AND (ci.instructor_id = (select auth.uid())))))` |
| exam_results | student inserts own result | INSERT | 1 | `(student_id = auth.uid())` → `(student_id = (select auth.uid()))` |
| exam_results | student reads own results | SELECT | 1 | `((student_id = auth.uid()) OR i…` → `((student_id = (select auth.uid())) OR i…` |
| homeroom_monitors | class members read homeroom monitors | SELECT | 1 | `((student_id = auth.uid()) OR i…` → `((student_id = (select auth.uid())) OR i…` |
| homeroom_term_records | students read own homeroom term records | SELECT | 1 | `((student_id = auth.uid()) OR i…` → `((student_id = (select auth.uid())) OR i…` |
| lesson_progress | student manages own progress | ALL | 2 | `((user_id = auth.uid()) OR i…` → `((user_id = (select auth.uid())) OR i…`<br>`(user_id = auth.uid())` → `(user_id = (select auth.uid()))` |
| messages | admin sends messages | INSERT | 1 | `…is_admin() AND (sender_id = auth.uid()))` → `…is_admin() AND (sender_id = (select auth.uid())))` |
| messages | read own messages | SELECT | 2 | `…_admin() OR (recipient_id = auth.uid()) OR (…` → `…_admin() OR (recipient_id = (select auth.uid())) OR (…`<br>`…iles WHERE (profiles.id = auth.uid()))))))` → `…iles WHERE (profiles.id = (select auth.uid())))))))` |
| notifications | delete own notifications | DELETE | 1 | `(user_id = auth.uid())` → `(user_id = (select auth.uid()))` |
| notifications | mark own notifications read | UPDATE | 2 | `(user_id = auth.uid())` → `(user_id = (select auth.uid()))`<br>`(user_id = auth.uid())` → `(user_id = (select auth.uid()))` |
| notifications | read own notifications | SELECT | 1 | `(user_id = auth.uid())` → `(user_id = (select auth.uid()))` |
| parent_links | parent reads own links | SELECT | 1 | `(parent_id = auth.uid())` → `(parent_id = (select auth.uid()))` |
| practice_question_results | student inserts own practice question results | INSERT | 1 | `(student_id = auth.uid())` → `(student_id = (select auth.uid()))` |
| practice_question_results | student reads own practice question results | SELECT | 1 | `((student_id = auth.uid()) OR t…` → `((student_id = (select auth.uid())) OR t…` |
| practice_sessions | student inserts own practice sessions | INSERT | 1 | `(student_id = auth.uid())` → `(student_id = (select auth.uid()))` |
| practice_sessions | student reads own practice sessions | SELECT | 1 | `((student_id = auth.uid()) OR t…` → `((student_id = (select auth.uid())) OR t…` |
| profiles | assigned instructors read student profiles | SELECT | 1 | `…id) AND (ci.instructor_id = auth.uid()))))` → `…id) AND (ci.instructor_id = (select auth.uid())))))` |
| profiles | instructors read enrolled student profiles | SELECT | 1 | `…id) AND (ci.instructor_id = auth.uid()))))` → `…id) AND (ci.instructor_id = (select auth.uid())))))` |
| profiles | parent updates own profile | UPDATE | 2 | `((id = auth.uid()) AND …` → `((id = (select auth.uid())) AND …`<br>`((id = auth.uid()) AND …` → `((id = (select auth.uid())) AND …` |
| profiles | read own profile | SELECT | 1 | `((id = auth.uid()) OR i…` → `((id = (select auth.uid())) OR i…` |
| profiles | update own profile | UPDATE | 2 | `(id = auth.uid())` → `(id = (select auth.uid()))`<br>`((id = auth.uid()) AND …` → `((id = (select auth.uid())) AND …` |
| question_bank | staff manage question bank | ALL | 2 | `…profiles p WHERE ((p.id = auth.uid()) AND …` → `…profiles p WHERE ((p.id = (select auth.uid())) AND …`<br>`…profiles p WHERE ((p.id = auth.uid()) AND …` → `…profiles p WHERE ((p.id = (select auth.uid())) AND …` |
| question_bank | student reads exit-quiz bank questions | SELECT | 1 | `… n WHERE ((n.student_id = auth.uid()) AND …` → `… n WHERE ((n.student_id = (select auth.uid())) AND …` |
| question_topics | staff manage question topics | ALL | 2 | `…profiles p WHERE ((p.id = auth.uid()) AND …` → `…profiles p WHERE ((p.id = (select auth.uid())) AND …`<br>`…profiles p WHERE ((p.id = auth.uid()) AND …` → `…profiles p WHERE ((p.id = (select auth.uid())) AND …` |
| rank_fix_attempts | read own rank_fix_attempts | SELECT | 1 | `((student_id = auth.uid()) OR t…` → `((student_id = (select auth.uid())) OR t…` |
| rank_gate_passes | read own rank_gate_passes | SELECT | 1 | `((student_id = auth.uid()) OR t…` → `((student_id = (select auth.uid())) OR t…` |
| rank_rp_awards | read own rank_rp_awards | SELECT | 1 | `((student_id = auth.uid()) OR t…` → `((student_id = (select auth.uid())) OR t…` |
| rank_rp_ledger | read own rank_rp_ledger | SELECT | 1 | `((student_id = auth.uid()) OR t…` → `((student_id = (select auth.uid())) OR t…` |
| rank_season_results | read own rank_season_results | SELECT | 1 | `((student_id = auth.uid()) OR t…` → `((student_id = (select auth.uid())) OR t…` |
| rank_student_seasons | read own rank_student_seasons | SELECT | 1 | `((student_id = auth.uid()) OR t…` → `((student_id = (select auth.uid())) OR t…` |
| rank_title_awards | read own rank_title_awards | SELECT | 1 | `((student_id = auth.uid()) OR t…` → `((student_id = (select auth.uid())) OR t…` |
| rubric_exam_attempts | students manage own self rubric attempt | INSERT | 1 | `((student_id = auth.uid()) AND …` → `((student_id = (select auth.uid())) AND …` |
| rubric_exam_attempts | students read own rubric exam attempts | SELECT | 1 | `((student_id = auth.uid()) OR i…` → `((student_id = (select auth.uid())) OR i…` |
| rubric_exam_attempts | students update own self rubric attempt | UPDATE | 2 | `((student_id = auth.uid()) AND …` → `((student_id = (select auth.uid())) AND …`<br>`((student_id = auth.uid()) AND …` → `((student_id = (select auth.uid())) AND …` |
| student_alerts | student reads own visible alerts | SELECT | 1 | `(((student_id = auth.uid()) AND …` → `(((student_id = (select auth.uid())) AND …` |
| student_learning_presence | assigned instructors read class learning presence | SELECT | 1 | `…id) AND (ci.instructor_id = auth.uid()))))` → `…id) AND (ci.instructor_id = (select auth.uid())))))` |
| student_learning_presence | students manage own learning presence | ALL | 2 | `(student_id = auth.uid())` → `(student_id = (select auth.uid()))`<br>`(student_id = auth.uid())` → `(student_id = (select auth.uid()))` |
| ta_assistants | ta xem chinh minh | SELECT | 1 | `((user_id = auth.uid()) OR i…` → `((user_id = (select auth.uid())) OR i…` |
| thpt_attendance_records | assigned instructors manage thpt attendance records | ALL | 2 | `…id) AND (ci.instructor_id = auth.uid()))))` → `…id) AND (ci.instructor_id = (select auth.uid())))))`<br>`…id) AND (ci.instructor_id = auth.uid()))))` → `…id) AND (ci.instructor_id = (select auth.uid())))))` |
| thpt_attendance_records | students read own thpt attendance | SELECT | 1 | `((student_id = auth.uid()) OR i…` → `((student_id = (select auth.uid())) OR i…` |
| thpt_attendance_sessions | assigned instructors manage thpt attendance sessions | ALL | 2 | `…id) AND (ci.instructor_id = auth.uid()))))` → `…id) AND (ci.instructor_id = (select auth.uid())))))`<br>`…id) AND (ci.instructor_id = auth.uid()))))` → `…id) AND (ci.instructor_id = (select auth.uid())))))` |
| thpt_attendance_sessions | students read own class thpt attendance sessions | SELECT | 1 | `…class_id) AND (uc.user_id = auth.uid()))))` → `…class_id) AND (uc.user_id = (select auth.uid())))))` |
| thpt_courses | anyone reads public courses | SELECT | 1 | `…tus = 'active'::text)) OR ((auth.uid() IS NO…` → `…tus = 'active'::text)) OR (((select auth.uid()) IS NO…` |
| thpt_registration_requests | staff read assigned thpt registrations | SELECT | 1 | `…id) AND (ci.instructor_id = auth.uid())))))` → `…id) AND (ci.instructor_id = (select auth.uid()))))))` |
| thpt_registration_requests | students read own thpt registration | SELECT | 1 | `(user_id = auth.uid())` → `(user_id = (select auth.uid()))` |
| thpt_registrations | own registrations | SELECT | 2 | `((student_id = auth.uid()) OR (…` → `((student_id = (select auth.uid())) OR (…`<br>`….uid()) OR (registered_by = auth.uid()) OR (…` → `….uid()) OR (registered_by = (select auth.uid())) OR (…` |
| tutoring_exit_attempts | read own exit attempts | SELECT | 1 | `((student_id = auth.uid()) OR t…` → `((student_id = (select auth.uid())) OR t…` |
| tutoring_exit_attempts | student logs own exit attempt | INSERT | 1 | `(student_id = auth.uid())` → `(student_id = (select auth.uid()))` |
| tutoring_needs | student reads own needs | SELECT | 1 | `((student_id = auth.uid()) OR t…` → `((student_id = (select auth.uid())) OR t…` |
| tutoring_registrations | student cancels self | DELETE | 1 | `(student_id = auth.uid())` → `(student_id = (select auth.uid()))` |
| tutoring_registrations | student reads own registration | SELECT | 1 | `(student_id = auth.uid())` → `(student_id = (select auth.uid()))` |
| tutoring_registrations | student registers self | INSERT | 2 | `((student_id = auth.uid()) AND …` → `((student_id = (select auth.uid())) AND …`<br>`…class_id) AND (uc.user_id = auth.uid()) AND …` → `…class_id) AND (uc.user_id = (select auth.uid())) AND …` |
| tutoring_session_topics | assistant writes own coverage | ALL | 2 | `…ession_id) AND (a.user_id = auth.uid())))) O…` → `…ession_id) AND (a.user_id = (select auth.uid()))))) O…`<br>`…ession_id) AND (a.user_id = auth.uid())))) O…` → `…ession_id) AND (a.user_id = (select auth.uid()))))) O…` |
| tutoring_session_topics | read tutoring coverage | SELECT | 1 | `((student_id = auth.uid()) OR t…` → `((student_id = (select auth.uid())) OR t…` |
| tutoring_slots | assistant manages own slots | ALL | 2 | `…istant_id) AND (a.user_id = auth.uid())))) O…` → `…istant_id) AND (a.user_id = (select auth.uid()))))) O…`<br>`…istant_id) AND (a.user_id = auth.uid())))) O…` → `…istant_id) AND (a.user_id = (select auth.uid()))))) O…` |
| tutoring_slots | class reads own slots | SELECT | 1 | `…s uc WHERE ((uc.user_id = auth.uid()) AND …` → `…s uc WHERE ((uc.user_id = (select auth.uid())) AND …` |
| user_classes | read own user classes | SELECT | 1 | `((user_id = auth.uid()) OR i…` → `((user_id = (select auth.uid())) OR i…` |
| user_classes | students request own class | INSERT | 1 | `((user_id = auth.uid()) AND …` → `((user_id = (select auth.uid())) AND …` |
| user_classes | students resubmit rejected class request | UPDATE | 2 | `((user_id = auth.uid()) AND …` → `((user_id = (select auth.uid())) AND …`<br>`((user_id = auth.uid()) AND …` → `((user_id = (select auth.uid())) AND …` |

## 3. Ba policy cần thầy quyết (KHÔNG tự sửa điều kiện)

1. `attendance_sessions` — "students read course attendance sessions": `e.course_id = e.course_id` (luôn đúng) thay vì `e.course_id = attendance_sessions.course_id` → sinh viên có 1 enrollment active đọc được buổi điểm danh của **mọi** khoá. Migration này chỉ chép lại y nguyên (đã đổi cú pháp auth.uid()).
2. `equipment_breakdown_reports` — "students read equipment breakdown reports": cùng lỗi `e.course_id = e.course_id`. Cũng chép lại y nguyên.
3. `class_assessments` — "anyone reads class assessments": `using (true)` cho mọi tài khoản đăng nhập. Không có `auth.uid()` nên **không nằm trong migration này**, chỉ ghi nhận (analytics.ts:81 đang đọc toàn bảng không lọc class_id — có thể chủ ý).

Nếu thầy đồng ý sửa (1)(2): đổi `e.course_id = e.course_id` thành `e.course_id = attendance_sessions.course_id` / `= equipment_breakdown_reports.course_id` — nên làm thành hotfix riêng để tách bạch "đổi cú pháp" và "đổi quyền".

## 4. Đề xuất bước sau (CHƯA đưa vào migration — đổi điều kiện = rủi ro)

- 6 policy `students read …` (attendance_machine_photos, attendance_machine_scores, attendance_sessions, checklist_sessions, course_offerings, equipment_breakdown_reports) viết tay `exists (select 1 from course_enrollments e … e.student_id = auth.uid() and e.status = 'active')` → thay bằng `is_course_member(course_id)` đã có.
- `staff manage question bank` / `staff manage question topics` viết lại nguyên thân `rank_is_staff()` → gọi hàm.
- 4 policy "assigned instructors read …" (exam_results, profiles, student_learning_presence, thpt_attendance_records) lặp `exists (user_classes uc join class_instructors ci …)` = `teaches_student(student_id)` (thiếu phần trợ giảng — cần thầy xác nhận có muốn mở cho trợ giảng không).
- Helper mới `is_class_member(class_id)` cho 4 policy (class_announcements, thpt_attendance_sessions, tutoring_slots, tutoring_registrations) đang lặp `exists (select 1 from user_classes uc where uc.user_id = auth.uid() and uc.class_id = … and uc.status = 'active')`.
- `profiles` có 7 policy SELECT OR nhau; AuthProvider đọc `profiles where id = uid` mỗi lần vào trang → gộp thành 1 policy gọi `can_read_profile(id)`.
- Đo sau khi chạy: `select relname, idx_scan from pg_stat_user_tables where relname = 'profiles'` — idx_scan phải ngừng tăng hàng nghìn/phút; EXPLAIN với `set role authenticated` phải thấy `InitPlan` thay `SubPlan` (DB_REPORT §4).

## 5. Kiểm chứng cú pháp trên pglite

`node perf/rls-pglite-check.mjs` (pglite 0.5.8, schema stub `perf/pglite-stub-schema.sql` sinh từ information_schema.columns + pg_proc thật: 95 bảng rỗng đúng cột, 193 hàm stub, `auth.uid()` giả):

```
✓ stub schema · ✓ migration RLS · ✓ rollback RLS · ✓ migration RLS (lần 2, idempotent)
✓ migration RPC · ✓ rollback RPC · ✓ migration RPC (lần 2)
policy trong pglite: 85, còn auth.uid() trần trong qual: 0
hàm helper stable còn auth.uid() trần (không đứng sau select): 0
```

Thân hàm `language sql` được Postgres kiểm tra lúc tạo (check_function_bodies) nên cột/bảng tham chiếu trong 5 RPC và 18 helper đều đã được xác nhận tồn tại. Chưa chạy trên DB thật (luật: không DDL lên prod) — thầy chạy tay, ngoài giờ học sinh làm bài (drop/create policy khoá bảng vài ms mỗi bảng, 53 bảng, trong 1 transaction).
