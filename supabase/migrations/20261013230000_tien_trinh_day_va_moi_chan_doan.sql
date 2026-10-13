-- ============================================================================
-- 13/10/2026 — (1) Tiến trình bài dạy theo khoá (tick "đã dạy" theo tuần + ghi chú cải tiến năm sau),
--              dùng chung cho thầy và trợ giảng; (2) thầy mời em đã có trong lớp làm kiểm tra đầu vào.
-- Thêm: 2 bảng thpt_teaching_progress / thpt_teaching_notes (RLS bật, không ai đọc/ghi trực tiếp),
--       hàm can_edit_teaching, teaching_get, teaching_set, teaching_note_add, teaching_note_delete,
--       thpt_invite_entry_diagnostic.
-- Tick đã dạy ĐỒNG BỘ mốc thpt_courses.current_topic_id ("lớp đang dạy tới bài") để phần bù bài của em vào trễ
-- luôn khớp tiến trình thật. Không đụng dữ liệu cũ.
-- Cách chạy: bash scripts/run-migrations.sh --yes --only N (lúc nào cũng chạy được).
-- Rollback: cuối file.
-- ============================================================================

begin;

create table if not exists public.thpt_teaching_progress (
  course_id bigint not null references public.thpt_courses (id) on delete cascade,
  topic_id bigint not null references public.question_topics (id) on delete cascade,
  taught_on date not null,
  week_start date not null,
  taught_by uuid references public.profiles (id) on delete set null,
  updated_at timestamptz not null default now(),
  primary key (course_id, topic_id)
);
alter table public.thpt_teaching_progress enable row level security;
revoke all on public.thpt_teaching_progress from anon, authenticated;

create table if not exists public.thpt_teaching_notes (
  id bigint generated always as identity primary key,
  class_id bigint not null references public.classes (id) on delete cascade,
  topic_id bigint not null references public.question_topics (id) on delete cascade,
  course_id bigint references public.thpt_courses (id) on delete set null,
  school_year text not null default '',
  body text not null check (length(trim(body)) between 1 and 1000),
  author_id uuid references public.profiles (id) on delete set null,
  created_at timestamptz not null default now()
);
create index if not exists thpt_teaching_notes_class_topic on public.thpt_teaching_notes (class_id, topic_id);
alter table public.thpt_teaching_notes enable row level security;
revoke all on public.thpt_teaching_notes from anon, authenticated;

-- Thầy phụ trách khối, admin, hoặc trợ giảng đang hoạt động được phân công khối đó.
create or replace function public.can_edit_teaching(p_class bigint)
returns boolean
language sql stable security definer set search_path = public
as $$
  select auth.uid() is not null and (
    public.manages_class(p_class)
    or exists (
      select 1 from public.ta_assistant_classes tac
      join public.ta_assistants a on a.id = tac.assistant_id
      where tac.class_id = p_class and a.user_id = auth.uid() and a.active
    )
  );
$$;
revoke all on function public.can_edit_teaching(bigint) from public, anon;
grant execute on function public.can_edit_teaching(bigint) to authenticated;

-- Đọc: tiến trình của khoá + ghi chú của CẢ khối qua các năm học (để năm sau thấy ghi chú năm trước).
create or replace function public.teaching_get(p_course bigint)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare c public.thpt_courses%rowtype;
begin
  select * into c from public.thpt_courses where id = p_course;
  if c.id is null then raise exception 'Không tìm thấy khoá học.'; end if;
  if not public.can_edit_teaching(c.class_id) then
    raise exception 'Bạn không phụ trách khối lớp này.' using errcode = '42501';
  end if;
  return jsonb_build_object(
    'currentTopicId', c.current_topic_id,
    'progress', coalesce((
      select jsonb_agg(jsonb_build_object(
        'topicId', p.topic_id, 'taughtOn', p.taught_on, 'weekStart', p.week_start,
        'by', (select full_name from public.profiles where id = p.taught_by)
      )) from public.thpt_teaching_progress p where p.course_id = p_course
    ), '[]'::jsonb),
    'notes', coalesce((
      select jsonb_agg(jsonb_build_object(
        'id', n.id, 'topicId', n.topic_id, 'body', n.body, 'schoolYear', n.school_year,
        'courseId', n.course_id, 'createdAt', n.created_at, 'mine', n.author_id = auth.uid(),
        'author', (select full_name from public.profiles where id = n.author_id)
      ) order by n.created_at desc)
      from public.thpt_teaching_notes n where n.class_id = c.class_id
    ), '[]'::jsonb)
  );
end;
$$;
revoke all on function public.teaching_get(bigint) from public, anon;
grant execute on function public.teaching_get(bigint) to authenticated;

-- Tick / bỏ tick "đã dạy" một bài (chủ đề tầng bài). Tuần = thứ Hai của ngày dạy.
create or replace function public.teaching_set(p_course bigint, p_topic bigint, p_taught boolean, p_on date default current_date)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  c public.thpt_courses%rowtype;
  t public.question_topics%rowtype;
  v_cur_sort int;
  v_max bigint;
begin
  select * into c from public.thpt_courses where id = p_course;
  if c.id is null then raise exception 'Không tìm thấy khoá học.'; end if;
  if not public.can_edit_teaching(c.class_id) then
    raise exception 'Bạn không phụ trách khối lớp này.' using errcode = '42501';
  end if;
  select * into t from public.question_topics where id = p_topic;
  if t.id is null or t.parent_id is not null or t.grade is distinct from public.thpt_course_grade(p_course) then
    raise exception 'Bài này không thuộc chương trình của khoá.';
  end if;

  if p_taught then
    insert into public.thpt_teaching_progress (course_id, topic_id, taught_on, week_start, taught_by)
    values (p_course, p_topic, coalesce(p_on, current_date), date_trunc('week', coalesce(p_on, current_date))::date, auth.uid())
    on conflict (course_id, topic_id) do update
      set taught_on = excluded.taught_on, week_start = excluded.week_start, taught_by = excluded.taught_by, updated_at = now();
    select sort_order into v_cur_sort from public.question_topics where id = c.current_topic_id;
    if c.current_topic_id is null or t.sort_order >= coalesce(v_cur_sort, -1) then
      update public.thpt_courses set current_topic_id = p_topic where id = p_course;
    end if;
  else
    delete from public.thpt_teaching_progress where course_id = p_course and topic_id = p_topic;
    if c.current_topic_id = p_topic then
      select p.topic_id into v_max
      from public.thpt_teaching_progress p join public.question_topics q on q.id = p.topic_id
      where p.course_id = p_course order by q.sort_order desc limit 1;
      update public.thpt_courses set current_topic_id = v_max where id = p_course;
    end if;
  end if;
end;
$$;
revoke all on function public.teaching_set(bigint, bigint, boolean, date) from public, anon;
grant execute on function public.teaching_set(bigint, bigint, boolean, date) to authenticated;

create or replace function public.teaching_note_add(p_course bigint, p_topic bigint, p_body text)
returns bigint
language plpgsql security definer set search_path = public
as $$
declare c public.thpt_courses%rowtype; v_id bigint;
begin
  select * into c from public.thpt_courses where id = p_course;
  if c.id is null then raise exception 'Không tìm thấy khoá học.'; end if;
  if not public.can_edit_teaching(c.class_id) then
    raise exception 'Bạn không phụ trách khối lớp này.' using errcode = '42501';
  end if;
  if not exists (select 1 from public.question_topics q where q.id = p_topic and q.parent_id is null) then
    raise exception 'Bài không hợp lệ.';
  end if;
  insert into public.thpt_teaching_notes (class_id, topic_id, course_id, school_year, body, author_id)
  values (c.class_id, p_topic, p_course, coalesce(c.school_year, ''), trim(p_body), auth.uid())
  returning id into v_id;
  return v_id;
end;
$$;
revoke all on function public.teaching_note_add(bigint, bigint, text) from public, anon;
grant execute on function public.teaching_note_add(bigint, bigint, text) to authenticated;

-- Xoá ghi chú: người viết hoặc admin.
create or replace function public.teaching_note_delete(p_id bigint)
returns void
language plpgsql security definer set search_path = public
as $$
declare n public.thpt_teaching_notes%rowtype;
begin
  select * into n from public.thpt_teaching_notes where id = p_id;
  if n.id is null then return; end if;
  if not (n.author_id = auth.uid() or public.is_admin()) then
    raise exception 'Chỉ người viết hoặc admin xoá được ghi chú.' using errcode = '42501';
  end if;
  delete from public.thpt_teaching_notes where id = p_id;
end;
$$;
revoke all on function public.teaching_note_delete(bigint) from public, anon;
grant execute on function public.teaching_note_delete(bigint) to authenticated;

-- Thầy mời một em ĐÃ có trong lớp (thêm thẳng, không qua đăng ký) làm kiểm tra đầu vào:
-- tạo/cập nhật đăng ký khoá với joined_late = true, status 'active', danh sách bài = phần lớp đã học (mới nhất trước).
-- Cần đã đặt mốc "lớp đang dạy tới bài". Không đổi học phí (payment_status giữ mặc định).
create or replace function public.thpt_invite_entry_diagnostic(p_course bigint, p_student uuid)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  c public.thpt_courses%rowtype;
  v_catchup bigint[];
  v_id bigint;
begin
  select * into c from public.thpt_courses where id = p_course;
  if c.id is null then raise exception 'Không tìm thấy khoá học.'; end if;
  if not public.manages_class(c.class_id) then
    raise exception 'Bạn không phụ trách khối lớp này.' using errcode = '42501';
  end if;
  if c.current_topic_id is null then
    raise exception 'Chưa đặt mốc “Lớp đang dạy tới bài” cho khoá này nên chưa biết kiểm tra phần nào.';
  end if;
  if not exists (select 1 from public.user_classes where user_id = p_student and class_id = c.class_id and status = 'active') then
    raise exception 'Em này chưa ở trong lớp của khoá.';
  end if;

  select coalesce(array_agg(t.id order by t.sort_order desc), '{}') into v_catchup
  from public.thpt_taught_topics(p_course) t;

  insert into public.thpt_registrations
    (course_id, student_id, registered_by, child_name, note, status, joined_late, catchup_topic_ids, reviewed_by, reviewed_at)
  values
    (p_course, p_student, auth.uid(), '', 'Thầy mời làm kiểm tra đầu vào', 'active', true, v_catchup, auth.uid(), now())
  on conflict (course_id, student_id) where student_id is not null do update
    set joined_late = true,
        status = case when public.thpt_registrations.status in ('rejected', 'left', 'pending') then 'active' else public.thpt_registrations.status end,
        catchup_topic_ids = case when cardinality(public.thpt_registrations.catchup_topic_ids) = 0
                                   and cardinality(public.thpt_registrations.catchup_done_topic_ids) = 0
                                 then excluded.catchup_topic_ids else public.thpt_registrations.catchup_topic_ids end
  returning id into v_id;

  return jsonb_build_object('registrationId', v_id, 'topicCount', cardinality(v_catchup));
end;
$$;
revoke all on function public.thpt_invite_entry_diagnostic(bigint, uuid) from public, anon;
grant execute on function public.thpt_invite_entry_diagnostic(bigint, uuid) to authenticated;

commit;

-- ============================================================================
-- ROLLBACK (dữ liệu tick/ghi chú sẽ mất; nên xuất trước nếu đã dùng)
-- drop function if exists public.thpt_invite_entry_diagnostic(bigint, uuid);
-- drop function if exists public.teaching_note_delete(bigint);
-- drop function if exists public.teaching_note_add(bigint, bigint, text);
-- drop function if exists public.teaching_set(bigint, bigint, boolean, date);
-- drop function if exists public.teaching_get(bigint);
-- drop function if exists public.can_edit_teaching(bigint);
-- drop table if exists public.thpt_teaching_notes;
-- drop table if exists public.thpt_teaching_progress;
-- ============================================================================
