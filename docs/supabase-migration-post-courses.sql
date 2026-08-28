-- ============================================================
-- Migration: Bài đăng gắn với khóa học CTTC (course_offerings)
-- Chạy SAU supabase-schema.sql + supabase-migration-classes.sql
-- + supabase-migration-course-enrollments.sql + supabase-migration-academic-subjects.sql
-- (idempotent, chạy lại được)
-- ============================================================

-- ---------- Loại nội dung ----------
alter table public.posts
  add column if not exists content_type text not null default 'thong_bao';

alter table public.posts drop constraint if exists posts_content_type_check;
alter table public.posts add constraint posts_content_type_check
  check (content_type in ('thong_bao', 'tai_lieu', 'video'));

-- ---------- Gán bài đăng theo khóa học (many-to-many) ----------
create table if not exists public.post_courses (
  post_id bigint not null references public.posts (id) on delete cascade,
  course_id bigint not null references public.course_offerings (id) on delete cascade,
  primary key (post_id, course_id)
);

alter table public.post_courses enable row level security;

drop policy if exists "read post courses" on public.post_courses;
create policy "read post courses" on public.post_courses for select using (true);
drop policy if exists "admin manages post courses" on public.post_courses;
create policy "admin manages post courses" on public.post_courses
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- ---------- Tạo/sửa bài đăng nguyên khối (atomic) ----------
-- Tạo bài + gán lớp/khóa trong 1 transaction — nếu bước gán lỗi thì toàn bộ
-- rollback, tránh tình trạng bài "mồ côi" bị coi là public toàn trường.
create or replace function public.create_post_with_targets(
  p_title text,
  p_body text,
  p_video_url text,
  p_content_type text,
  p_subject_code text,
  p_class_ids bigint[],
  p_course_ids bigint[]
) returns bigint
language plpgsql security definer set search_path = public
as $$
declare
  v_post_id bigint;
begin
  if not public.is_admin() then
    raise exception 'not authorized';
  end if;

  insert into public.posts (title, body, video_url, content_type, subject_code)
  values (coalesce(p_title, ''), coalesce(p_body, ''), coalesce(p_video_url, ''), coalesce(p_content_type, 'thong_bao'), coalesce(p_subject_code, 'vat-ly'))
  returning id into v_post_id;

  if p_class_ids is not null and array_length(p_class_ids, 1) > 0 then
    insert into public.post_classes (post_id, class_id)
    select v_post_id, class_id from unnest(p_class_ids) as class_id;
  end if;

  if p_course_ids is not null and array_length(p_course_ids, 1) > 0 then
    insert into public.post_courses (post_id, course_id)
    select v_post_id, course_id from unnest(p_course_ids) as course_id;
  end if;

  return v_post_id;
end;
$$;

create or replace function public.update_post_with_targets(
  p_post_id bigint,
  p_title text,
  p_body text,
  p_video_url text,
  p_content_type text,
  p_subject_code text,
  p_class_ids bigint[],
  p_course_ids bigint[]
) returns void
language plpgsql security definer set search_path = public
as $$
begin
  if not public.is_admin() then
    raise exception 'not authorized';
  end if;

  update public.posts set
    title = coalesce(p_title, ''),
    body = coalesce(p_body, ''),
    video_url = coalesce(p_video_url, ''),
    content_type = coalesce(p_content_type, 'thong_bao'),
    subject_code = coalesce(p_subject_code, 'vat-ly')
  where id = p_post_id;

  delete from public.post_classes where post_id = p_post_id;
  if p_class_ids is not null and array_length(p_class_ids, 1) > 0 then
    insert into public.post_classes (post_id, class_id)
    select p_post_id, class_id from unnest(p_class_ids) as class_id;
  end if;

  delete from public.post_courses where post_id = p_post_id;
  if p_course_ids is not null and array_length(p_course_ids, 1) > 0 then
    insert into public.post_courses (post_id, course_id)
    select p_post_id, course_id from unnest(p_course_ids) as course_id;
  end if;
end;
$$;

grant execute on function public.create_post_with_targets(text, text, text, text, text, bigint[], bigint[]) to authenticated;
grant execute on function public.update_post_with_targets(bigint, text, text, text, text, text, bigint[], bigint[]) to authenticated;
