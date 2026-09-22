-- ============================================================
-- Vào lớp trễ: phụ đạo bù bài trước khi vào lớp chính thức
--
-- Em đăng ký sau khai giảng (thpt_registrations.joined_late) thì:
--   1. Giáo viên đánh dấu lớp "đang dạy tới bài" (thpt_courses.current_topic_id — chủ đề
--      tầng bài trong question_topics). Mọi bài có sort_order <= bài đó là phần lớp đã học.
--   2. Lúc đăng ký, em / phụ huynh tick các bài đã học ở nơi khác (known_topic_ids).
--      Phần còn lại thành catchup_topic_ids, xếp bài GẦN NHẤT lên đầu rồi lùi dần về trước —
--      buổi đầu bù đúng phần lớp vừa học để em theo kịp ngay, các buổi sau vá dần phía sau.
--      Chưa học ở đâu hết -> không tick gì -> bù toàn bộ, vẫn theo thứ tự gần nhất trước.
--   3. Giáo viên duyệt -> user_classes active (em vào khối, đọc được bài, đăng ký được ca
--      phụ đạo) nhưng trạng thái ghi danh là 'catchup' cho tới khi bù xong.
--   4. Em / phụ huynh đăng ký ca trong lịch tuần của trợ giảng khối (tutoring_slots) —
--      ca nào có topic trùng bài cần bù kế tiếp được gợi ý lên đầu.
--   5. Trợ giảng ghi buổi phụ đạo (tutoring_session_topics) -> trigger gạch bài đó khỏi
--      catchup_topic_ids; hết danh sách -> 'active'. Giáo viên cũng bấm "Xong bù bài" được.
--
-- Chạy SAU: supabase-migration-khoa-hoc-thpt.sql, supabase-migration-tutoring-slots.sql,
--           supabase-migration-topic-outcomes.sql
-- Idempotent — chạy lại được. Chạy trong Supabase → SQL Editor.
-- ============================================================

-- ---------- 1. Cột ----------
alter table public.thpt_courses
  add column if not exists current_topic_id bigint references public.question_topics (id) on delete set null;

alter table public.thpt_registrations
  add column if not exists known_topic_ids bigint[] not null default '{}',
  add column if not exists catchup_topic_ids bigint[] not null default '{}',
  add column if not exists catchup_done_topic_ids bigint[] not null default '{}';

-- ---------- 2. Khối lớp -> grade của question_topics ----------
-- classes.name: '10' | '11' | '12' | 'KHTN 9' -> question_topics.grade: '10' | '11' | '12' | '9'
create or replace function public.thpt_course_grade(p_course_id bigint)
returns text
language sql stable security definer set search_path = public
as $$
  select (regexp_match(cl.name, '\d+'))[1]
  from public.thpt_courses c
  join public.classes cl on cl.id = c.class_id
  where c.id = p_course_id;
$$;
grant execute on function public.thpt_course_grade(bigint) to anon, authenticated;

-- ---------- 3. Lớp đã học tới đâu — bài gần nhất trước ----------
-- Trả về rỗng khi giáo viên chưa đặt current_topic_id (không đoán).
create or replace function public.thpt_taught_topics(p_course_id bigint)
returns table (id bigint, name text, chapter_id bigint, chapter_title text, sort_order int)
language sql stable security definer set search_path = public
as $$
  with cur as (
    select t.sort_order as cur_sort, c.id as course_id
    from public.thpt_courses c
    join public.question_topics t on t.id = c.current_topic_id
    where c.id = p_course_id
  )
  select t.id, t.name, t.chapter_id, ch.title, t.sort_order
  from cur
  join public.question_topics t
    on t.grade = public.thpt_course_grade(cur.course_id)
   and t.parent_id is null
   and t.sort_order <= cur.cur_sort
  left join public.chapters ch on ch.id = t.chapter_id
  order by t.sort_order desc, t.name;
$$;
grant execute on function public.thpt_taught_topics(bigint) to anon, authenticated;

-- ---------- 4. Chốt danh sách bù ----------
-- Gọi ngay sau thpt_register (em / phụ huynh), hoặc giáo viên sửa lại. p_known: bài đã học
-- nơi khác. Trả về danh sách bài cần bù theo thứ tự.
create or replace function public.thpt_set_catchup(p_registration_id bigint, p_known_topic_ids bigint[] default '{}')
returns bigint[]
language plpgsql security definer set search_path = public
as $$
declare
  r public.thpt_registrations%rowtype;
  c public.thpt_courses%rowtype;
  v_catchup bigint[];
  v_known bigint[];
begin
  if auth.uid() is null then raise exception 'Bạn cần đăng nhập.'; end if;
  select * into r from public.thpt_registrations where id = p_registration_id;
  if r.id is null then raise exception 'Không tìm thấy đăng ký.'; end if;
  select * into c from public.thpt_courses where id = r.course_id;

  if not (
    r.student_id = auth.uid()
    or r.registered_by = auth.uid()
    or (r.student_id is not null and public.is_parent_of(r.student_id))
    or public.manages_class(c.class_id)
  ) then
    raise exception 'Bạn không sửa được đăng ký này.';
  end if;

  -- Chỉ giữ những bài thật sự nằm trong phần lớp đã học.
  select coalesce(array_agg(t.id order by t.sort_order desc), '{}')
  into v_known
  from public.thpt_taught_topics(c.id) t
  where t.id = any (coalesce(p_known_topic_ids, '{}'::bigint[]));

  select coalesce(array_agg(t.id order by t.sort_order desc), '{}')
  into v_catchup
  from public.thpt_taught_topics(c.id) t
  where not (t.id = any (v_known))
    and not (t.id = any (r.catchup_done_topic_ids));

  update public.thpt_registrations
  set known_topic_ids = v_known,
      catchup_topic_ids = v_catchup,
      -- Đang bù mà danh sách trống (đã học hết ở nơi khác / giáo viên bỏ hết) -> vào lớp luôn.
      status = case when status = 'catchup' and cardinality(v_catchup) = 0 then 'active' else status end
  where id = p_registration_id;

  return v_catchup;
end;
$$;
revoke all on function public.thpt_set_catchup(bigint, bigint[]) from public, anon;
grant execute on function public.thpt_set_catchup(bigint, bigint[]) to authenticated;

-- ---------- 5. Duyệt: vào trễ còn bài phải bù -> 'catchup' ----------
-- Thay bản ở supabase-migration-khoa-hoc-thpt.sql. p_status = 'active':
--   · đang pending, joined_late, còn catchup_topic_ids -> 'catchup' (user_classes vẫn active)
--   · đang catchup -> 'active' (giáo viên chốt "xong bù bài")
create or replace function public.thpt_review_registration(p_id bigint, p_status text)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  r public.thpt_registrations%rowtype;
  c public.thpt_courses%rowtype;
  v_new text := p_status;
begin
  if p_status not in ('active', 'rejected', 'left', 'pending') then
    raise exception 'Trạng thái không hợp lệ: %', p_status;
  end if;
  select * into r from public.thpt_registrations where id = p_id;
  if r.id is null then raise exception 'Không tìm thấy đăng ký.'; end if;
  select * into c from public.thpt_courses where id = r.course_id;
  if not public.manages_class(c.class_id) then
    raise exception 'Bạn không phụ trách khối lớp này.';
  end if;
  if p_status = 'active' and r.student_id is null then
    raise exception 'Con chưa có tài khoản — gắn tài khoản trước rồi mới duyệt được.';
  end if;

  if p_status = 'active' and r.status <> 'catchup' and r.joined_late and cardinality(r.catchup_topic_ids) > 0 then
    v_new := 'catchup';
  end if;

  update public.thpt_registrations
  set status = v_new, reviewed_by = auth.uid(), reviewed_at = now()
  where id = p_id;

  if r.student_id is not null then
    if v_new in ('active', 'catchup') then
      insert into public.user_classes (user_id, class_id, status, reviewed_by, reviewed_at)
      values (r.student_id, c.class_id, 'active', auth.uid(), now())
      on conflict (user_id, class_id) do update
        set status = 'active', reviewed_by = excluded.reviewed_by, reviewed_at = excluded.reviewed_at;
    elsif p_status = 'rejected' then
      update public.user_classes
      set status = 'rejected', reviewed_by = auth.uid(), reviewed_at = now()
      where user_id = r.student_id and class_id = c.class_id and status = 'pending';
    end if;
  end if;
end;
$$;

-- Duyệt ở hàng chờ user_classes cũ: pending -> catchup nếu còn bài phải bù, ngược lại active.
-- Dòng đang catchup giữ nguyên (chỉ trigger buổi phụ đạo / giáo viên chốt mới đổi).
create or replace function public.trg_sync_thpt_registration()
returns trigger
language plpgsql security definer set search_path = public
as $$
begin
  if new.status = 'active' and (old.status is distinct from 'active') then
    update public.thpt_registrations r
    set status = case when r.joined_late and cardinality(r.catchup_topic_ids) > 0 then 'catchup' else 'active' end,
        reviewed_by = coalesce(new.reviewed_by, r.reviewed_by), reviewed_at = now()
    from public.thpt_courses c
    where c.id = r.course_id and c.class_id = new.class_id
      and r.student_id = new.user_id and r.status = 'pending';
  elsif new.status = 'rejected' and (old.status is distinct from 'rejected') then
    update public.thpt_registrations r
    set status = 'rejected', reviewed_by = coalesce(new.reviewed_by, r.reviewed_by), reviewed_at = now()
    from public.thpt_courses c
    where c.id = r.course_id and c.class_id = new.class_id
      and r.student_id = new.user_id and r.status in ('pending', 'catchup');
  end if;
  return new;
end;
$$;

-- ---------- 6. Buổi phụ đạo ghi xong -> gạch bài đã bù ----------
-- tutoring_session_topics.topic_id có thể là tầng bài hoặc yêu cầu cần đạt -> quy về tầng bài.
create or replace function public.trg_catchup_progress()
returns trigger
language plpgsql security definer set search_path = public
as $$
declare
  v_topic bigint;
begin
  select coalesce(t.parent_id, t.id) into v_topic from public.question_topics t where t.id = new.topic_id;
  if v_topic is null then return new; end if;

  update public.thpt_registrations r
  set catchup_topic_ids = array_remove(r.catchup_topic_ids, v_topic),
      catchup_done_topic_ids = case
        when v_topic = any (r.catchup_done_topic_ids) then r.catchup_done_topic_ids
        else array_append(r.catchup_done_topic_ids, v_topic)
      end
  where r.student_id = new.student_id
    and r.status = 'catchup'
    and v_topic = any (r.catchup_topic_ids);

  update public.thpt_registrations
  set status = 'active', reviewed_at = now()
  where student_id = new.student_id and status = 'catchup' and cardinality(catchup_topic_ids) = 0;

  return new;
end;
$$;

drop trigger if exists trg_catchup_progress on public.tutoring_session_topics;
create trigger trg_catchup_progress
  after insert on public.tutoring_session_topics
  for each row execute function public.trg_catchup_progress();

-- ---------- 7. Phụ huynh xem lịch phụ đạo của khối con và đăng ký ca cho con ----------
drop policy if exists "parent reads child class slots" on public.tutoring_slots;
create policy "parent reads child class slots" on public.tutoring_slots
  for select to authenticated
  using (exists (
    select 1 from public.user_classes uc
    where uc.class_id = tutoring_slots.class_id and uc.status = 'active' and public.is_parent_of(uc.user_id)
  ));

drop policy if exists "parent reads child slot registrations" on public.tutoring_registrations;
create policy "parent reads child slot registrations" on public.tutoring_registrations
  for select to authenticated
  using (public.is_parent_of(student_id));

drop policy if exists "parent registers child" on public.tutoring_registrations;
create policy "parent registers child" on public.tutoring_registrations
  for insert to authenticated
  with check (
    public.is_parent_of(student_id)
    and exists (
      select 1 from public.tutoring_slots s
      join public.user_classes uc on uc.class_id = s.class_id and uc.user_id = student_id and uc.status = 'active'
      where s.id = slot_id
    )
  );

drop policy if exists "parent cancels child" on public.tutoring_registrations;
create policy "parent cancels child" on public.tutoring_registrations
  for delete to authenticated
  using (public.is_parent_of(student_id));
