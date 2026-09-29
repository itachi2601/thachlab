-- ============================================================================
-- perf(rpc-gv): RPC tổng hợp cho trang giáo viên — Pha 2 tối ưu tốc độ 9/2026
-- ============================================================================
-- Mục đích: thay các chỗ client tải hàng nghìn dòng thô (exam_question_results,
-- exam_results, lesson_progress, practice_sessions kèm exams.questions ~30 KB/đề)
-- về trình duyệt rồi tự tính, bằng hàm SQL gộp sẵn trên server.
--
-- Mọi hàm ở đây đều `security invoker` → RLS của người gọi vẫn áp dụng y như khi
-- client select thẳng bảng (giáo viên chỉ thấy học sinh mình dạy qua
-- teaches_student(), học sinh chỉ thấy chính mình). Không nới quyền.
--
-- Client (services/analytics.ts, services/student-profile.ts, lib/tro-giang/queries.ts)
-- gọi rpc trước; nếu hàm chưa tồn tại (PGRST202 / 42883) hoặc lỗi thì tự fallback
-- về đường cũ, nên chạy hay chưa chạy file này web vẫn hiển thị y hệt.
--
-- Cách chạy: Dashboard → SQL Editor → dán cả file, Run (idempotent: create or replace).
--   hoặc: supabase db query --linked -f supabase/migrations/20260925130000_perf_rpc_gv.sql
-- KHÔNG dùng `supabase db push` (thư mục migrations chưa đồng bộ với 99 file docs/).
-- Sau khi chạy: `npx tsx scripts/perf-compare-rpc.mts` để đối chiếu rpc vs đường cũ.
-- ============================================================================

begin;

-- ---------------------------------------------------------------------------
-- 1. Điểm tốt nhất của từng học sinh trên một đề (tab Phân tích → thẻ tổng quan)
--    thay: services/analytics.ts fetchExamOverview — select mọi lượt làm của lớp
--    trên đề rồi lấy max ở client. Trả ≤ 1 dòng / học sinh.
-- ---------------------------------------------------------------------------
create or replace function public.get_class_exam_best(p_exam bigint, p_students uuid[])
returns table (student_id uuid, score numeric, duration_seconds integer)
language sql
stable
security invoker
set search_path = public
as $$
  select distinct on (r.student_id) r.student_id, r.score, r.duration_seconds
  from public.exam_results r
  where r.exam_id = p_exam
    and r.student_id = any (coalesce(p_students, '{}'::uuid[]))
  order by r.student_id, r.score desc nulls last, r.created_at asc;
$$;

revoke all on function public.get_class_exam_best(bigint, uuid[]) from public;
grant execute on function public.get_class_exam_best(bigint, uuid[]) to authenticated;

-- ---------------------------------------------------------------------------
-- 2. Thống kê sai/đúng theo từng câu của một đề trong lớp (tab Phân tích → "câu sai nhiều nhất")
--    thay: fetchWrongestQuestions — tải ≈ 40 dòng × số lượt làm (lớp 12: ~5.8k dòng
--    cho cả lớp) rồi group ở client. Trả ≤ số câu của đề.
--    is_correct null tính là sai (giống `!r.is_correct` ở client).
-- ---------------------------------------------------------------------------
create or replace function public.get_class_exam_question_stats(p_exam bigint, p_students uuid[])
returns table (question_index integer, topic_name text, form text, qtype text, total integer, wrong integer)
language sql
stable
security invoker
set search_path = public
as $$
  select q.question_index,
         max(q.topic_name) as topic_name,
         max(q.form) as form,
         max(q.qtype) as qtype,
         count(*)::int as total,
         (count(*) filter (where not coalesce(q.is_correct, false)))::int as wrong
  from public.exam_question_results q
  where q.exam_id = p_exam
    and q.student_id = any (coalesce(p_students, '{}'::uuid[]))
  group by q.question_index
  order by q.question_index;
$$;

revoke all on function public.get_class_exam_question_stats(bigint, uuid[]) from public;
grant execute on function public.get_class_exam_question_stats(bigint, uuid[]) to authenticated;

-- ---------------------------------------------------------------------------
-- 3. Ma trận chủ đề × dạng → số câu / số sai của lớp (tab Phân tích → "chủ đề yếu")
--    thay: fetchClassTopicMatrix — cùng bộ dòng thô như (2). p_exam null = mọi đề.
--    Nhóm theo (tên chủ đề đã chuẩn hoá, form) đúng như khoá `${topic}|${form}` ở client;
--    topic_id lấy max() (client lấy topic_id khác null cuối cùng gặp — cùng ý).
-- ---------------------------------------------------------------------------
create or replace function public.get_class_topic_matrix(p_students uuid[], p_exam bigint default null)
returns table (topic_id bigint, topic_name text, form text, total integer, wrong integer)
language sql
stable
security invoker
set search_path = public
as $$
  select max(q.topic_id) as topic_id,
         coalesce(nullif(q.topic_name, ''), 'Chưa gắn chủ đề') as topic_name,
         q.form,
         count(*)::int as total,
         (count(*) filter (where not coalesce(q.is_correct, false)))::int as wrong
  from public.exam_question_results q
  where q.student_id = any (coalesce(p_students, '{}'::uuid[]))
    and (p_exam is null or q.exam_id = p_exam)
  group by coalesce(nullif(q.topic_name, ''), 'Chưa gắn chủ đề'), q.form;
$$;

revoke all on function public.get_class_topic_matrix(uuid[], bigint) from public;
grant execute on function public.get_class_topic_matrix(uuid[], bigint) to authenticated;

-- ---------------------------------------------------------------------------
-- 4. Lịch sử học tập của một học sinh (tab Hồ sơ học sinh)
--    thay: services/progress.ts fetchStudentLearningHistory — 3 truy vấn, mỗi cái
--    limit 100, trong đó exam_results kéo cả exams.questions (JSON ~30 KB/đề) chỉ để
--    biết đề có câu tự luận hay không. Ở đây trả cờ has_essay + các số thô; client
--    ghép chuỗi hiển thị y như cũ.
-- ---------------------------------------------------------------------------
create or replace function public.get_student_learning_history(p_student uuid)
returns table (
  activity text,
  at timestamptz,
  lesson_title text,
  item_title text,
  score numeric,
  correct_count integer,
  question_count integer,
  detail_correct_count jsonb,
  has_essay boolean
)
language sql
stable
security invoker
set search_path = public
as $$
  (
    select 'theory'::text, lp.done_at, l.title, li.title,
           null::numeric, null::integer, null::integer, null::jsonb, null::boolean
    from public.lesson_progress lp
    left join public.lesson_items li on li.id = lp.item_id
    left join public.lessons l on l.id = li.lesson_id
    where lp.user_id = p_student
    order by lp.done_at desc
    limit 100
  )
  union all
  (
    select 'practice'::text, ps.created_at, l.title, null::text,
           ps.score, ps.correct_count, ps.question_count, null::jsonb, null::boolean
    from public.practice_sessions ps
    left join public.lessons l on l.id = ps.lesson_id
    where ps.student_id = p_student
    order by ps.created_at desc
    limit 100
  )
  union all
  (
    select 'exam'::text, er.created_at, e.title, null::text,
           er.score, null::integer, null::integer,
           er.detail -> 'correctCount',
           case when jsonb_typeof(e.questions) = 'array'
                then exists (select 1 from jsonb_array_elements(e.questions) x where x ->> 'type' = 'essay')
                else false end
    from public.exam_results er
    left join public.exams e on e.id = er.exam_id
    where er.student_id = p_student
    order by er.created_at desc
    limit 100
  );
$$;

revoke all on function public.get_student_learning_history(uuid) from public;
grant execute on function public.get_student_learning_history(uuid) to authenticated;

-- ---------------------------------------------------------------------------
-- 5. Điểm tháng của NHIỀU trợ giảng trong 1 lần gọi (trang /tro-giang, bảng quản trị)
--    thay: components/tro-giang/AdminMonthlyTable — 1 rpc ta_monthly_score / trợ giảng.
--    Chỉ là vỏ bọc: gọi lại đúng hàm ta_monthly_score (security definer, tự kiểm tra
--    quyền admin / chính mình cho từng id) → không thêm quyền gì mới.
-- ---------------------------------------------------------------------------
create or replace function public.ta_monthly_scores(p_assistant_ids uuid[], p_month date)
returns table (
  assistant_id uuid, month date, lop_sessions integer, phudao_sessions integer,
  avg_touches numeric, touches_score numeric, ontime_error_notes integer, error_note_rate numeric,
  error_note_score numeric, complete_phudao integer, phudao_complete_rate numeric, phudao_score numeric,
  flag_count integer, focus_score numeric, total_score numeric, bonus_per_hour integer,
  converted_hours numeric, papers_graded integer, base_pay numeric, bonus_pay numeric,
  grading_pay numeric, total_pay numeric
)
language sql
stable
security invoker
set search_path = public
as $$
  select s.*
  from unnest(coalesce(p_assistant_ids, '{}'::uuid[])) with ordinality as a(id, ord)
  cross join lateral public.ta_monthly_score(a.id, p_month) as s
  order by a.ord;
$$;

revoke all on function public.ta_monthly_scores(uuid[], date) from public;
grant execute on function public.ta_monthly_scores(uuid[], date) to authenticated;

commit;

-- ============================================================================
-- ROLLBACK (chạy khi cần gỡ; client tự quay về đường cũ vì rpc trả PGRST202)
-- ============================================================================
-- begin;
-- drop function if exists public.get_class_exam_best(bigint, uuid[]);
-- drop function if exists public.get_class_exam_question_stats(bigint, uuid[]);
-- drop function if exists public.get_class_topic_matrix(uuid[], bigint);
-- drop function if exists public.get_student_learning_history(uuid);
-- drop function if exists public.ta_monthly_scores(uuid[], date);
-- commit;
