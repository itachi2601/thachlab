-- ============================================================================
-- Vá bảo mật sau rà soát 11/11/2026 — BƯỚC 1/2: thêm hàm mới + đóng 2 lỗ không còn ai dùng.
-- Chạy TRƯỚC khi deploy client (client mới gọi 3 hàm dưới đây). Lúc nào cũng được: chỉ thêm hàm, xoá 1 hàm cũ, xoá 2 policy.
-- Bước 2 (20261111200000_va_bao_mat_buoc_2_thu_quyen.sql) chạy SAU khi deploy, sau 22h.
--
--  1. notify_user_staff: thay cho việc client gọi thẳng notify_user (hàm đó không kiểm quyền → HS gửi được thông báo
--     giả kèm link tuỳ ý cho bất kỳ ai). Bản mới: chỉ admin/GV/trợ giảng, href phải là đường dẫn trong site.
--  2. get_cnc_quiz_banks: đường đọc câu hỏi quiz CNC (exams.cnc_key) để bước 2 thu được quyền đọc exams.questions
--     — đây là "RPC riêng cho CNC" mà P0 #1 chặng 3 đang chờ. Giữ nguyên phạm vi đang đọc được: đề đã published
--     (admin đọc mọi đề), phải đăng nhập.
--  3. cnc_milling_quiz_save: ghi bài kiểm tra vận hành phay theo participant_key (khoá bí mật nằm ở máy người làm)
--     thay cho upsert thẳng vào bảng (policy UPDATE using(true) cho anon → ai cũng sửa được bài của người khác).
--  4. Xoá rank_fix_quiz_submit(bigint, int): bản cũ nhận "số câu đúng" từ máy, còn mở cho anon. Client đã dùng bản
--     (bigint, jsonb) chấm server từ 24/10 (20261024150000 ghi "bản p_correct int bỏ ở chặng 3").
--  5. cnc_milling_checklist_attempts: bảng không còn mã nào dùng; xoá 2 policy cho anon INSERT/UPDATE mọi dòng.
--  6. get_student_learning_history (quyền người gọi) đang đọc thẳng exams.questions để biết đề có câu tự luận → đổi sang
--     hàm phụ exam_has_essay, kết quả y như cũ; không đổi thì bước 2 làm trang hồ sơ học sinh lỗi.
--
-- Rollback: perf/rollback/20261111190000_va_bao_mat_buoc_1_ham_moi.down.sql
-- ============================================================================
begin;

-- ---------- 1. Thông báo do giáo viên/trợ giảng gửi ----------
create or replace function public.notify_user_staff(p_user uuid, p_kind text, p_title text, p_body text default '', p_href text default '')
returns void
language plpgsql security definer set search_path = public
as $$
begin
  if not public.is_staff() then
    raise exception 'Chỉ giáo viên/trợ giảng gửi được thông báo.' using errcode = '42501';
  end if;
  if p_user is null or coalesce(btrim(p_title), '') = '' or coalesce(btrim(p_kind), '') = '' then
    raise exception 'Thiếu người nhận, loại hoặc tiêu đề.' using errcode = '22023';
  end if;
  -- Link chỉ được trỏ trong site: bắt đầu bằng một dấu "/" (không "//", không "http:", không "javascript:").
  if coalesce(p_href, '') <> '' and p_href !~ '^/[^/\\]' and p_href <> '/' then
    raise exception 'Link thông báo phải là đường dẫn trong site.' using errcode = '22023';
  end if;
  insert into public.notifications (user_id, kind, title, body, href)
  values (p_user, left(p_kind, 60), left(p_title, 200), left(coalesce(p_body, ''), 2000), coalesce(p_href, ''));
end;
$$;
revoke all on function public.notify_user_staff(uuid, text, text, text, text) from public, anon;
grant execute on function public.notify_user_staff(uuid, text, text, text, text) to authenticated;

-- ---------- 2. Câu hỏi quiz CNC ----------
create or replace function public.get_cnc_quiz_banks(p_keys text[])
returns table (cnc_key text, questions jsonb)
language sql stable security definer set search_path = public
as $$
  select e.cnc_key, e.questions
  from public.exams e
  where (select auth.uid()) is not null
    and e.cnc_key = any (p_keys)
    and (e.published or public.is_admin());
$$;
revoke all on function public.get_cnc_quiz_banks(text[]) from public, anon;
grant execute on function public.get_cnc_quiz_banks(text[]) to authenticated;

-- ---------- 3. Ghi bài kiểm tra vận hành phay ----------
create or replace function public.cnc_milling_quiz_save(
  p_course_id bigint,
  p_participant_key uuid,
  p_participant_name text,
  p_class_name text,
  p_answers jsonb,
  p_score integer,
  p_total integer,
  p_status text
)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  v_uid uuid := auth.uid();
  v_owner uuid;
  v_found boolean;
  v_answers jsonb := case when jsonb_typeof(p_answers) = 'object' then p_answers else '{}'::jsonb end;
  v_count int;
begin
  if p_participant_key is null then
    raise exception 'Thiếu mã người làm bài.' using errcode = '22023';
  end if;
  if p_status not in ('in_progress', 'passed', 'failed') then
    raise exception 'Trạng thái không hợp lệ.' using errcode = '22023';
  end if;
  if octet_length(v_answers::text) > 20000 or coalesce(p_total, 0) <= 0 or coalesce(p_total, 0) > 200
     or coalesce(p_score, -1) < 0 or p_score > p_total then
    raise exception 'Bài làm không hợp lệ.' using errcode = '22023';
  end if;
  select count(*) into v_count from jsonb_object_keys(v_answers);

  select true, a.student_id into v_found, v_owner
  from public.cnc_milling_quiz_attempts a where a.participant_key = p_participant_key for update;

  -- Bài đã gắn với một tài khoản thì chỉ tài khoản đó ghi tiếp được.
  if v_found and v_owner is not null and v_owner is distinct from v_uid then
    raise exception 'Bài làm này thuộc tài khoản khác.' using errcode = '42501';
  end if;

  insert into public.cnc_milling_quiz_attempts (
    course_id, student_id, participant_key, participant_name, class_name, answers, answered_count,
    score, total_questions, status, last_activity_at, submitted_at
  ) values (
    p_course_id, v_uid, p_participant_key,
    left(coalesce(nullif(btrim(p_participant_name), ''), 'Học sinh'), 120), left(coalesce(btrim(p_class_name), ''), 60),
    v_answers, v_count, p_score, p_total, p_status, now(),
    case when p_status = 'in_progress' then null else now() end
  )
  on conflict (participant_key) do update set
    course_id = excluded.course_id,
    student_id = coalesce(excluded.student_id, cnc_milling_quiz_attempts.student_id),
    participant_name = excluded.participant_name,
    class_name = excluded.class_name,
    answers = excluded.answers,
    answered_count = excluded.answered_count,
    score = excluded.score,
    total_questions = excluded.total_questions,
    status = excluded.status,
    last_activity_at = excluded.last_activity_at,
    submitted_at = excluded.submitted_at;
end;
$$;
revoke all on function public.cnc_milling_quiz_save(bigint, uuid, text, text, jsonb, integer, integer, text) from public;
grant execute on function public.cnc_milling_quiz_save(bigint, uuid, text, text, jsonb, integer, integer, text) to anon, authenticated;

-- ---------- 4. Bản cũ nhận số câu đúng từ máy ----------
drop function if exists public.rank_fix_quiz_submit(bigint, integer);

-- ---------- 5. Bảng checklist phay không còn dùng: thôi cho anon ghi ----------
drop policy if exists "classroom creates live checklist attempts" on public.cnc_milling_checklist_attempts;
drop policy if exists "classroom updates live checklist attempts" on public.cnc_milling_checklist_attempts;

-- ---------- 6. Lịch sử học tập: thôi đọc thẳng exams.questions ----------
create or replace function public.exam_has_essay(p_exam_id bigint)
returns boolean
language sql stable security definer set search_path = public
as $$
  select coalesce((
    select exists (select 1 from jsonb_array_elements(e.questions) x where x ->> 'type' = 'essay')
    from public.exams e where e.id = p_exam_id and jsonb_typeof(e.questions) = 'array'), false);
$$;
revoke all on function public.exam_has_essay(bigint) from public, anon;
grant execute on function public.exam_has_essay(bigint) to authenticated;

create or replace function public.get_student_learning_history(p_student uuid)
returns table (activity text, at timestamptz, lesson_title text, item_title text, score numeric, correct_count integer,
               question_count integer, detail_correct_count jsonb, has_essay boolean)
language sql stable set search_path = public
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
           public.exam_has_essay(er.exam_id)
    from public.exam_results er
    left join public.exams e on e.id = er.exam_id
    where er.student_id = p_student
    order by er.created_at desc
    limit 100
  );
$$;

commit;
