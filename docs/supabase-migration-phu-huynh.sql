-- ============================================================
-- Phụ huynh xem kết quả học tập của con
--
-- Mô hình giống lời mời giảng viên (supabase-migration-staff-invites.sql):
--   giáo viên phụ trách lớp (hoặc admin) tạo MÃ cho một học sinh, gửi link
--     https://thachlab.id.vn/loi-moi?ma=PHxxxxxx
--   qua Zalo cho phụ huynh. Phụ huynh mở link:
--     - chưa có tài khoản -> đăng ký ngay tại đó, mã đi kèm raw_user_meta_data.invite_code,
--       trigger zz_claim_parent_link nối tài khoản với con;
--     - đã có tài khoản  -> bấm "Nhận", gọi claim_parent_link() cho chính mình.
--
-- Mã phụ huynh luôn bắt đầu bằng "PH" + 6 ký tự hex, còn mã mời nhân sự là 8 ký tự hex
-- thuần — nên trang /loi-moi phân biệt được hai loại mã chỉ bằng tiền tố, và
-- apply_staff_invite / apply_parent_link không bao giờ nhận nhầm mã của nhau.
--
-- Phụ huynh CHỈ ĐỌC: mọi policy mới đều là SELECT, không có INSERT/UPDATE nào dùng
-- is_parent_of(). Không đụng vào teaches_student() vì hàm đó đang gác cả quyền chấm
-- bài, sửa cảnh báo, thêm mục phụ đạo.
--
-- Chạy SAU: supabase-migration-vai-tro-tro-giang.sql, supabase-migration-student-rank.sql,
--           supabase-migration-topic-outcomes.sql, supabase-migration-tutoring-needs.sql.
-- Idempotent — chạy lại được. Chạy trong Supabase → SQL Editor.
-- ============================================================

-- ---------- 1. Vai trò mới ----------
alter table public.profiles drop constraint if exists profiles_role_check;
alter table public.profiles add constraint profiles_role_check
  check (role in ('student', 'admin', 'instructor', 'tro_giang', 'parent'));

-- "update own profile" (supabase-schema.sql) chỉ cho with check role = 'student' —
-- phụ huynh sửa họ tên của mình sẽ bị chặn. Thêm một policy song song, vẫn không cho
-- tự đổi vai trò.
drop policy if exists "parent updates own profile" on public.profiles;
create policy "parent updates own profile" on public.profiles
  for update to authenticated
  using (id = auth.uid() and role = 'parent')
  with check (id = auth.uid() and role = 'parent');

-- ---------- 2. Liên kết phụ huynh ↔ học sinh ----------
-- Một dòng vừa là "mã mời" (parent_id null, claimed_at null) vừa là "liên kết" sau khi
-- phụ huynh nhận. Không tách hai bảng để khỏi đồng bộ.
create table if not exists public.parent_links (
  id uuid primary key default gen_random_uuid(),
  code text not null unique
    default 'PH' || upper(substr(replace(gen_random_uuid()::text, '-', ''), 1, 6)),
  student_id uuid not null references public.profiles (id) on delete cascade,
  parent_id uuid references public.profiles (id) on delete cascade,
  -- Ghi nhớ mời ai ("Mẹ Lan", "Bố") — chỉ để giáo viên nhìn, không bắt buộc.
  label text not null default '',
  created_by uuid references public.profiles (id) on delete set null,
  created_at timestamptz not null default now(),
  claimed_at timestamptz
);

create index if not exists parent_links_student_idx on public.parent_links (student_id);
create index if not exists parent_links_parent_idx on public.parent_links (parent_id)
  where parent_id is not null;
-- Một phụ huynh chỉ nối với một học sinh một lần.
create unique index if not exists parent_links_pair_idx
  on public.parent_links (student_id, parent_id) where parent_id is not null;

alter table public.parent_links enable row level security;

-- Giáo viên được phân công lớp của em (teaches_student đã gồm admin) tạo/xem/huỷ mã.
drop policy if exists "staff manage parent links" on public.parent_links;
create policy "staff manage parent links" on public.parent_links
  for all to authenticated
  using (public.teaches_student(student_id))
  with check (public.teaches_student(student_id));

drop policy if exists "parent reads own links" on public.parent_links;
create policy "parent reads own links" on public.parent_links
  for select to authenticated
  using (parent_id = auth.uid());

-- ---------- 3. is_parent_of — dùng trong mọi policy đọc bên dưới ----------
create or replace function public.is_parent_of(p_student uuid)
returns boolean
language sql security definer stable set search_path = public
as $$
  select exists (
    select 1 from public.parent_links
    where parent_id = auth.uid() and student_id = p_student and claimed_at is not null
  );
$$;

grant execute on function public.is_parent_of(uuid) to authenticated;

-- ---------- 4. Áp dụng mã (dùng chung cho trigger đăng ký và tự nhận) ----------
-- Trả về id liên kết; null nếu mã không có / đã dùng.
create or replace function public.apply_parent_link(p_user_id uuid, p_code text)
returns uuid
language plpgsql
security definer
set search_path = public
as $$
declare
  v_code text := upper(trim(coalesce(p_code, '')));
  lnk public.parent_links%rowtype;
  v_existing uuid;
begin
  if v_code = '' then
    return null;
  end if;

  select * into lnk from public.parent_links
  where upper(code) = v_code and claimed_at is null;

  if lnk.id is null then
    return null;
  end if;

  if lnk.student_id = p_user_id then
    raise exception 'Mã này dành cho phụ huynh — em không tự nhận mã của chính mình được.';
  end if;

  if exists (select 1 from public.profiles where id = p_user_id and role = 'admin') then
    raise exception 'Tài khoản quản trị không cần mã phụ huynh — gửi mã này cho đúng phụ huynh.';
  end if;

  -- Đã nối với em này từ mã trước: bỏ mã thừa, trả về liên kết đang có.
  select id into v_existing from public.parent_links
  where student_id = lnk.student_id and parent_id = p_user_id and claimed_at is not null;
  if v_existing is not null then
    delete from public.parent_links where id = lnk.id;
    return v_existing;
  end if;

  update public.parent_links
  set parent_id = p_user_id, claimed_at = now()
  where id = lnk.id;

  -- Tài khoản mới tinh (chưa vào lớp nào, chưa ghi danh khoá nào) -> vai trò phụ huynh.
  -- Giảng viên / trợ giảng / học sinh đang học vẫn giữ vai trò cũ; is_parent_of() vẫn
  -- cho họ xem kết quả của con.
  update public.profiles p
  set role = 'parent'
  where p.id = p_user_id
    and p.role = 'student'
    and not exists (select 1 from public.user_classes uc where uc.user_id = p_user_id)
    and not exists (select 1 from public.course_enrollments ce where ce.student_id = p_user_id);

  return lnk.id;
end;
$$;

revoke all on function public.apply_parent_link(uuid, text) from public, authenticated, anon;
grant execute on function public.apply_parent_link(uuid, text) to service_role;

-- ---------- 4b. Người đã có tài khoản tự nhận mã ----------
-- Luôn áp cho chính người đang đăng nhập. Trả về tên + lớp của con để trang báo đúng.
create or replace function public.claim_parent_link(p_code text)
returns table (student_name text, class_name text)
language plpgsql
security definer
set search_path = public
as $$
declare
  v_user uuid := auth.uid();
  v_code text := upper(trim(coalesce(p_code, '')));
  lnk public.parent_links%rowtype;
  v_link_id uuid;
begin
  if v_user is null then
    raise exception 'Bạn cần đăng nhập trước khi nhận mã.';
  end if;

  select * into lnk from public.parent_links where upper(code) = v_code;

  if lnk.id is null then
    raise exception 'Không có mã phụ huynh nào là %. Nhờ giáo viên gửi lại link mới.', v_code;
  end if;

  if lnk.claimed_at is not null then
    if lnk.parent_id = v_user then
      -- Chính chủ bấm lại: đã nối rồi, coi như xong.
      return query
      select p.full_name, p.class_name from public.profiles p where p.id = lnk.student_id;
      return;
    end if;
    raise exception 'Mã % đã được một tài khoản khác nhận lúc %. Nhờ giáo viên tạo mã mới.',
      v_code,
      to_char(lnk.claimed_at at time zone 'Asia/Ho_Chi_Minh', 'HH24:MI "ngày" DD/MM/YYYY');
  end if;

  v_link_id := public.apply_parent_link(v_user, p_code);
  if v_link_id is null then
    raise exception 'Không nhận được mã này — nhờ giáo viên tạo lại.';
  end if;

  return query
  select p.full_name, p.class_name from public.profiles p where p.id = lnk.student_id;
end;
$$;

grant execute on function public.claim_parent_link(text) to authenticated;

-- ---------- 4c. Tự nhận khi phụ huynh đăng ký mới từ /loi-moi?ma=PH... ----------
-- Chạy sau on_auth_user_created (đã có profiles) — tên bắt đầu bằng "zz_" như trigger mời
-- nhân sự. Chỉ xử lý mã tiền tố PH; mã khác để zz_claim_staff_invite lo.
create or replace function public.trg_claim_parent_link()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  v_code text := upper(trim(coalesce(new.raw_user_meta_data ->> 'invite_code', '')));
begin
  if v_code like 'PH%' then
    perform public.apply_parent_link(new.id, v_code);
  end if;
  return new;
end;
$$;

drop trigger if exists zz_claim_parent_link on auth.users;
create trigger zz_claim_parent_link
  after insert on auth.users
  for each row execute function public.trg_claim_parent_link();

-- ---------- 5. Phụ huynh đọc dữ liệu của con — CHỈ SELECT ----------
drop policy if exists "parent reads child profile" on public.profiles;
create policy "parent reads child profile" on public.profiles
  for select to authenticated using (public.is_parent_of(id));

drop policy if exists "parent reads child classes" on public.user_classes;
create policy "parent reads child classes" on public.user_classes
  for select to authenticated using (public.is_parent_of(user_id));

drop policy if exists "parent reads child exam results" on public.exam_results;
create policy "parent reads child exam results" on public.exam_results
  for select to authenticated using (public.is_parent_of(student_id));

drop policy if exists "parent reads child question results" on public.exam_question_results;
create policy "parent reads child question results" on public.exam_question_results
  for select to authenticated using (public.is_parent_of(student_id));

drop policy if exists "parent reads child practice sessions" on public.practice_sessions;
create policy "parent reads child practice sessions" on public.practice_sessions
  for select to authenticated using (public.is_parent_of(student_id));

drop policy if exists "parent reads child practice question results" on public.practice_question_results;
create policy "parent reads child practice question results" on public.practice_question_results
  for select to authenticated using (public.is_parent_of(student_id));

drop policy if exists "parent reads child lesson progress" on public.lesson_progress;
create policy "parent reads child lesson progress" on public.lesson_progress
  for select to authenticated using (public.is_parent_of(user_id));

drop policy if exists "parent reads child tutoring needs" on public.tutoring_needs;
create policy "parent reads child tutoring needs" on public.tutoring_needs
  for select to authenticated using (public.is_parent_of(student_id));

drop policy if exists "parent reads child tutoring coverage" on public.tutoring_session_topics;
create policy "parent reads child tutoring coverage" on public.tutoring_session_topics
  for select to authenticated using (public.is_parent_of(student_id));

-- Cảnh báo: giống học sinh, chỉ thấy khi thầy đã xử lý (status <> 'open').
drop policy if exists "parent reads child visible alerts" on public.student_alerts;
create policy "parent reads child visible alerts" on public.student_alerts
  for select to authenticated
  using (public.is_parent_of(student_id) and status <> 'open');

-- ---------- 6. Hai RPC đang tự kiểm quyền theo auth.uid() ----------
-- 6a. Chi tiết YCCĐ còn sai: thêm nhánh phụ huynh vào bộ lọc đầu vào, phần còn lại giữ nguyên.
drop function if exists public.student_outcome_gaps(uuid[], int);
create or replace function public.student_outcome_gaps(p_students uuid[], p_window int default 2)
returns table (
  student_id uuid,
  parent_topic_id bigint,
  topic_id bigint,
  topic_name text,
  form text,
  total int,
  wrong int
)
language sql stable security definer set search_path = public
as $$
  with students as (
    select s.id
    from unnest(coalesce(p_students, '{}'::uuid[])) as s(id)
    where s.id = auth.uid() or public.teaches_student(s.id) or public.is_parent_of(s.id)
  ),
  recent as (
    select er.student_id, er.exam_id, row_number() over (
             partition by er.student_id order by max(er.created_at) desc
           ) as rn
    from public.exam_results er
    join students s on s.id = er.student_id
    group by er.student_id, er.exam_id
  ),
  last_try as (
    select distinct on (er.student_id, er.exam_id) er.id
    from public.exam_results er
    join recent r on r.student_id = er.student_id and r.exam_id = er.exam_id
    where r.rn <= greatest(p_window, 1)
    order by er.student_id, er.exam_id, er.created_at desc
  )
  select q.student_id,
         coalesce(t.parent_id, q.topic_id) as parent_topic_id,
         q.topic_id,
         coalesce(t.name, q.topic_name) as topic_name,
         coalesce(nullif(q.form, ''), '') as form,
         (count(*))::int as total,
         (count(*) filter (where not q.is_correct))::int as wrong
  from public.exam_question_results q
  join last_try lt on lt.id = q.exam_result_id
  left join public.question_topics t on t.id = q.topic_id
  where q.topic_id is not null
  group by q.student_id, coalesce(t.parent_id, q.topic_id), q.topic_id,
           coalesce(t.name, q.topic_name), coalesce(nullif(q.form, ''), '')
  having count(*) filter (where not q.is_correct) > 0
  order by 1, 2, 7 desc, 6 desc;
$$;

grant execute on function public.student_outcome_gaps(uuid[], int) to authenticated;

-- 6b. Hạng theo bài kiểm tra định kỳ: tách phần tính ra hàm nhận student_id, có kiểm quyền
-- (chính em / giáo viên của em / phụ huynh của em). get_periodic_rank(bigint) cũ giữ
-- nguyên chữ ký, chỉ còn là lớp mỏng gọi hàm mới cho auth.uid().
create or replace function public.get_periodic_rank_of(p_student uuid, p_class_id bigint)
returns table(rnk int, total int, my_avg numeric, class_avg numeric)
language plpgsql security definer stable set search_path = public
as $$
begin
  if p_student is null then
    return;
  end if;
  if not (
    p_student = auth.uid()
    or public.teaches_student(p_student)
    or public.is_parent_of(p_student)
  ) then
    return;
  end if;
  -- chỉ tính hạng cho lớp mà em đang active — không cho dò lớp khác
  if not exists (
    select 1 from public.user_classes
    where user_id = p_student and class_id = p_class_id and status = 'active'
  ) then
    return;
  end if;

  return query
  with classmates as (
    select user_id from public.user_classes
    where class_id = p_class_id and status = 'active'
  ),
  scores as (
    select c.user_id as student_id,
           (select max(er.score) from public.exam_results er
              where er.student_id = c.user_id and er.exam_id = ca.exam_id) as best
    from classmates c
    cross join public.class_assessments ca
    where ca.class_id = p_class_id
  ),
  avgs as (
    select student_id, avg(best) as avg_score
    from scores
    where best is not null
    group by student_id
  ),
  ranked as (
    select student_id, avg_score, rank() over (order by avg_score desc) as rnk
    from avgs
  )
  select r.rnk::int, (select count(*)::int from avgs), r.avg_score,
         (select avg(avg_score) from avgs)
  from ranked r
  where r.student_id = p_student;
end;
$$;

grant execute on function public.get_periodic_rank_of(uuid, bigint) to authenticated;

create or replace function public.get_periodic_rank(p_class_id bigint)
returns table(rnk int, total int, my_avg numeric, class_avg numeric)
language sql security definer stable set search_path = public
as $$
  select * from public.get_periodic_rank_of(auth.uid(), p_class_id);
$$;

grant execute on function public.get_periodic_rank(bigint) to authenticated;
