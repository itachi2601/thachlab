-- ============================================================
-- Phụ đạo theo chủ đề: "em nào hổng phần nào · đã được dạy phần nào"
-- ============================================================
-- Chạy SAU:
--   docs/supabase-migration-exam-analytics.sql      (question_topics, exam_question_results)
--   docs/supabase-migration-question-topics-seed.sql (danh mục chủ đề)
--   docs/supabase-migration-ta-policy-oct2026.sql   (phiếu buổi trợ giảng)
-- Idempotent — chạy lại được.
--
-- Vòng đời một "mục cần phụ đạo" = (một em × một chủ đề × lý thuyết|bài tập):
--   open      HS sai ≥ 50% số câu của chủ đề đó trong 2 bài gần nhất (tối thiểu 3 câu)
--   assigned  trợ giảng nhận
--   tutored   đã có buổi phụ đạo ghi nhận dạy chủ đề này
--   cleared   bài sau làm đúng ≥ 75% chủ đề đó -> tự đóng, có bằng chứng
--   dismissed bỏ qua (thầy/trợ giảng thấy không cần)
-- ============================================================


-- ---------- 0. Trợ giảng cũng là người dạy em đó ----------
-- teaches_student() trước đây chỉ tính admin + class_instructors (role 'instructor'),
-- nên trợ giảng không đọc được cảnh báo lẫn kết quả từng câu — trong khi phụ đạo mới
-- chính là việc của họ. Trợ giảng gắn với lớp qua ta_assistant_classes (trang Nhân sự).
-- Bản mở rộng này nằm ở đây chứ không sửa file exam-analytics để khỏi lệch hai nơi;
-- chạy lại file exam-analytics sau này thì chạy lại file này để lấy lại định nghĩa rộng.
create or replace function public.assists_class(p_class bigint)
returns boolean
language sql security definer stable set search_path = public
as $$
  select exists (
    select 1
    from public.ta_assistant_classes tac
    join public.ta_assistants a on a.id = tac.assistant_id
    where tac.class_id = p_class and a.user_id = auth.uid() and a.active
  );
$$;

create or replace function public.teaches_student(p_student uuid)
returns boolean
language sql security definer stable set search_path = public
as $$
  select public.is_admin() or exists (
    select 1
    from public.user_classes uc
    join public.class_instructors ci on ci.class_id = uc.class_id
    where uc.user_id = p_student and ci.instructor_id = auth.uid()
  ) or exists (
    select 1
    from public.user_classes uc
    join public.ta_assistant_classes tac on tac.class_id = uc.class_id
    join public.ta_assistants a on a.id = tac.assistant_id
    where uc.user_id = p_student and a.user_id = auth.uid() and a.active
  );
$$;


-- ---------- 1. Mục cần phụ đạo ----------
create table if not exists public.tutoring_needs (
  id bigint generated always as identity primary key,
  student_id uuid not null references public.profiles (id) on delete cascade,
  class_id bigint references public.classes (id) on delete set null,
  topic_id bigint not null references public.question_topics (id) on delete cascade,
  form text not null default '' check (form in ('ly_thuyet', 'bai_tap', '')),
  wrong int not null default 0,
  total int not null default 0,
  pct int not null default 0,                 -- % sai trong cửa sổ xét
  source text not null default 'auto' check (source in ('auto', 'manual')),
  status text not null default 'open'
    check (status in ('open', 'assigned', 'tutored', 'cleared', 'dismissed')),
  assigned_to uuid references public.profiles (id) on delete set null,
  note text not null default '',
  first_seen_at timestamptz not null default now(),
  last_seen_at timestamptz not null default now(),
  tutored_at timestamptz,
  cleared_at timestamptz,
  updated_at timestamptz not null default now(),
  unique (student_id, topic_id, form)
);
create index if not exists tutoring_needs_class_idx
  on public.tutoring_needs (class_id, status, pct desc);
create index if not exists tutoring_needs_student_idx
  on public.tutoring_needs (student_id, status);

create or replace function public.touch_tutoring_need()
returns trigger language plpgsql as $$
begin new.updated_at := now(); return new; end; $$;
drop trigger if exists trg_touch_tutoring_need on public.tutoring_needs;
create trigger trg_touch_tutoring_need before update on public.tutoring_needs
  for each row execute function public.touch_tutoring_need();

alter table public.tutoring_needs enable row level security;

-- Học sinh thấy thẳng phần mình còn hổng (khác cảnh báo student_alerts: cái đó ẩn
-- tới khi trợ giảng xử lý, còn đây là việc học của chính em).
drop policy if exists "student reads own needs" on public.tutoring_needs;
create policy "student reads own needs" on public.tutoring_needs
  for select to authenticated
  using (student_id = auth.uid() or public.teaches_student(student_id));

drop policy if exists "staff update needs" on public.tutoring_needs;
create policy "staff update needs" on public.tutoring_needs
  for update to authenticated
  using (public.teaches_student(student_id)) with check (public.teaches_student(student_id));

-- Thầy/trợ giảng thêm tay một mục cần phụ đạo (source = 'manual').
drop policy if exists "staff insert needs" on public.tutoring_needs;
create policy "staff insert needs" on public.tutoring_needs
  for insert to authenticated
  with check (public.teaches_student(student_id));

drop policy if exists "admin manages needs" on public.tutoring_needs;
create policy "admin manages needs" on public.tutoring_needs
  for all to authenticated using (public.is_admin()) with check (public.is_admin());


-- ---------- 2. Buổi phụ đạo đã dạy chủ đề nào cho em nào ----------
alter table public.ta_sessions
  add column if not exists class_id bigint references public.classes (id) on delete set null,
  add column if not exists phudao_student_ids uuid[] not null default '{}';

create table if not exists public.tutoring_session_topics (
  id bigint generated always as identity primary key,
  session_id uuid not null references public.ta_sessions (id) on delete cascade,
  student_id uuid not null references public.profiles (id) on delete cascade,
  topic_id bigint not null references public.question_topics (id) on delete cascade,
  need_id bigint references public.tutoring_needs (id) on delete set null,
  note text not null default '',
  created_at timestamptz not null default now(),
  unique (session_id, student_id, topic_id)
);
create index if not exists tst_student_idx on public.tutoring_session_topics (student_id, created_at desc);

alter table public.tutoring_session_topics enable row level security;

drop policy if exists "read tutoring coverage" on public.tutoring_session_topics;
create policy "read tutoring coverage" on public.tutoring_session_topics
  for select to authenticated
  using (student_id = auth.uid() or public.teaches_student(student_id));

-- Trợ giảng chỉ ghi được vào buổi của chính mình.
drop policy if exists "assistant writes own coverage" on public.tutoring_session_topics;
create policy "assistant writes own coverage" on public.tutoring_session_topics
  for all to authenticated
  using (exists (
    select 1 from public.ta_sessions s
    join public.ta_assistants a on a.id = s.assistant_id
    where s.id = session_id and a.user_id = auth.uid()
  ) or public.is_admin())
  with check (exists (
    select 1 from public.ta_sessions s
    join public.ta_assistants a on a.id = s.assistant_id
    where s.id = session_id and a.user_id = auth.uid()
  ) or public.is_admin());

-- Ghi nhận dạy xong -> mục tương ứng chuyển sang "đã phụ đạo".
create or replace function public.trg_tutoring_covered()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  update public.tutoring_needs n
    set status = case when n.status in ('open', 'assigned') then 'tutored' else n.status end,
        tutored_at = coalesce(n.tutored_at, now())
  where n.student_id = new.student_id and n.topic_id = new.topic_id
    and n.status in ('open', 'assigned');
  return new;
end; $$;
drop trigger if exists trg_tutoring_covered on public.tutoring_session_topics;
create trigger trg_tutoring_covered after insert on public.tutoring_session_topics
  for each row execute function public.trg_tutoring_covered();


-- ---------- 3. Buộc phiếu phụ đạo gắn với tài khoản học sinh thật ----------
-- Từ 01/10/2026 em được phụ đạo phải có tài khoản trên web (thầy chốt) — có vậy mới
-- nối được với chủ đề em đang hổng. phudao_students (tên) vẫn giữ để bảng lương và
-- phiếu theo dõi từng em chạy y như cũ; phudao_student_ids khớp theo đúng thứ tự.
create or replace function public.ta_session_student_link_guard()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  if new.session_type <> 'phudao' or new.work_date < date '2026-10-01' then
    return new;
  end if;
  if cardinality(new.phudao_student_ids) <> cardinality(new.phudao_students) then
    raise exception 'Mỗi em được phụ đạo phải chọn từ danh sách lớp (em chưa có tài khoản thì đăng ký trước)';
  end if;
  if cardinality(new.phudao_student_ids)
     <> (select count(distinct x) from unnest(new.phudao_student_ids) x) then
    raise exception 'Một em chỉ ghi một lần trong buổi';
  end if;
  return new;
end; $$;
drop trigger if exists ta_session_student_link_guard on public.ta_sessions;
create trigger ta_session_student_link_guard before insert or update on public.ta_sessions
  for each row execute function public.ta_session_student_link_guard();


-- ---------- 4. Sinh / đóng mục cần phụ đạo từ kết quả làm bài ----------
-- Cửa sổ xét: 2 đề gần nhất em đã nộp (lấy lượt nộp mới nhất của mỗi đề).
create or replace function public.refresh_tutoring_needs(p_student uuid)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  v_class bigint;
  v_window int := 2;        -- xét 2 bài gần nhất
  v_min_q int := 3;         -- cần ít nhất 3 câu cùng chủ đề mới dám kết luận
  v_need_pct numeric := 50; -- sai từ 50% -> cần phụ đạo
  v_clear_pct numeric := 25;-- sai ≤ 25% (đúng ≥ 75%) -> coi như đã khắc phục
begin
  select uc.class_id into v_class
  from public.user_classes uc
  where uc.user_id = p_student and uc.status = 'active'
  order by uc.class_id desc
  limit 1;

  -- (a) mở / cập nhật mục còn hổng
  with recent as (
    select er.exam_id
    from public.exam_results er
    where er.student_id = p_student
    group by er.exam_id
    order by max(er.created_at) desc
    limit v_window
  ),
  last_try as (
    select distinct on (er.exam_id) er.id
    from public.exam_results er
    join recent r on r.exam_id = er.exam_id
    where er.student_id = p_student
    order by er.exam_id, er.created_at desc
  ),
  agg as (
    select q.topic_id,
           coalesce(nullif(q.form, ''), '') as form,
           (count(*))::int as total,
           (count(*) filter (where not q.is_correct))::int as wrong
    from public.exam_question_results q
    join last_try t on t.id = q.exam_result_id
    where q.student_id = p_student and q.topic_id is not null
    group by q.topic_id, coalesce(nullif(q.form, ''), '')
  )
  insert into public.tutoring_needs
    (student_id, class_id, topic_id, form, wrong, total, pct, source, status)
  select p_student, v_class, a.topic_id, a.form, a.wrong, a.total,
         round(a.wrong * 100.0 / a.total)::int, 'auto', 'open'
  from agg a
  where a.total >= v_min_q and a.wrong * 100.0 / a.total >= v_need_pct
  on conflict (student_id, topic_id, form) do update set
    wrong = excluded.wrong,
    total = excluded.total,
    pct = excluded.pct,
    class_id = coalesce(excluded.class_id, tutoring_needs.class_id),
    last_seen_at = now(),
    -- đã đóng mà hổng lại -> mở lại như vấn đề mới
    status = case when tutoring_needs.status in ('cleared', 'dismissed')
                  then 'open' else tutoring_needs.status end,
    cleared_at = case when tutoring_needs.status in ('cleared', 'dismissed')
                  then null else tutoring_needs.cleared_at end,
    note = case when tutoring_needs.status in ('cleared', 'dismissed')
                  then '' else tutoring_needs.note end;

  -- (b) làm đúng lại -> đóng mục, ghi rõ nhờ phụ đạo hay tự khắc phục
  with recent as (
    select er.exam_id
    from public.exam_results er
    where er.student_id = p_student
    group by er.exam_id
    order by max(er.created_at) desc
    limit v_window
  ),
  last_try as (
    select distinct on (er.exam_id) er.id
    from public.exam_results er
    join recent r on r.exam_id = er.exam_id
    where er.student_id = p_student
    order by er.exam_id, er.created_at desc
  ),
  agg as (
    select q.topic_id,
           coalesce(nullif(q.form, ''), '') as form,
           (count(*))::int as total,
           (count(*) filter (where not q.is_correct))::int as wrong
    from public.exam_question_results q
    join last_try t on t.id = q.exam_result_id
    where q.student_id = p_student and q.topic_id is not null
    group by q.topic_id, coalesce(nullif(q.form, ''), '')
  )
  update public.tutoring_needs n
  set status = 'cleared',
      cleared_at = now(),
      last_seen_at = now(),
      wrong = a.wrong,
      total = a.total,
      pct = round(a.wrong * 100.0 / a.total)::int,
      note = case when n.note <> '' then n.note
                  when n.tutored_at is not null then 'đã phụ đạo, bài sau làm đúng lại'
                  else 'tự khắc phục, không cần phụ đạo' end
  from agg a
  where n.student_id = p_student
    and n.topic_id = a.topic_id
    and n.form = a.form
    and n.status in ('open', 'assigned', 'tutored')
    and a.total >= 2
    and a.wrong * 100.0 / a.total <= v_clear_pct;
end;
$$;

-- Chạy sau khi kết quả từng câu đã ghi xong (ExamRunner chèn exam_question_results
-- SAU exam_results, nên không móc vào trigger của exam_results được).
create or replace function public.trg_eqr_tutoring_needs()
returns trigger language plpgsql security definer set search_path = public
as $$
declare r record;
begin
  for r in select distinct student_id from new_rows loop
    perform public.refresh_tutoring_needs(r.student_id);
  end loop;
  return null;
end; $$;

drop trigger if exists trg_eqr_tutoring_needs on public.exam_question_results;
create trigger trg_eqr_tutoring_needs
  after insert on public.exam_question_results
  referencing new table as new_rows
  for each statement execute function public.trg_eqr_tutoring_needs();


-- ---------- 5. Dựng lại cho cả lớp ----------
-- Dùng sau khi mới gắn nhãn chủ đề cho các đề cũ: bấm "Dựng lại" ở tab Phụ đạo.
create or replace function public.refresh_class_tutoring_needs(p_class bigint)
returns int
language plpgsql security definer set search_path = public
as $$
declare v_count int := 0; r record;
begin
  if not (public.manages_class(p_class) or public.assists_class(p_class)) then
    raise exception 'không có quyền với lớp này';
  end if;
  for r in
    select uc.user_id from public.user_classes uc
    where uc.class_id = p_class and uc.status = 'active'
  loop
    perform public.refresh_tutoring_needs(r.user_id);
    v_count := v_count + 1;
  end loop;
  return v_count;
end;
$$;

grant execute on function public.refresh_class_tutoring_needs(bigint) to authenticated;
grant execute on function public.assists_class(bigint) to authenticated;


-- ---------- 6. Trợ giảng đọc được danh sách lớp mình phụ trách ----------
-- Phiếu phụ đạo nay chọn em từ danh sách lớp chứ không gõ tên, nên trợ giảng phải
-- đọc được roster. Chỉ SELECT, chỉ đúng lớp được phân công (ta_assistant_classes).
drop policy if exists "assistants read class rosters" on public.user_classes;
create policy "assistants read class rosters" on public.user_classes
  for select to authenticated
  using (public.assists_class(class_id));

drop policy if exists "assistants read student profiles" on public.profiles;
create policy "assistants read student profiles" on public.profiles
  for select to authenticated
  using (exists (
    select 1 from public.user_classes uc
    where uc.user_id = profiles.id and public.assists_class(uc.class_id)
  ));
