-- ============================================================
-- ThachLab LMS — schema Supabase
-- Chạy toàn bộ file này trong Supabase Dashboard → SQL Editor
-- ============================================================

-- ---------- Hồ sơ người dùng ----------
create table if not exists public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  created_at timestamptz not null default now(),
  full_name text not null,
  class_name text not null default '',
  role text not null default 'student' check (role in ('student', 'admin'))
);

-- Tự tạo hồ sơ khi có tài khoản mới (tên/lớp lấy từ metadata lúc đăng ký)
create or replace function public.handle_new_user()
returns trigger
language plpgsql security definer set search_path = public
as $$
begin
  insert into public.profiles (id, full_name, class_name)
  values (
    new.id,
    coalesce(new.raw_user_meta_data ->> 'full_name', ''),
    coalesce(new.raw_user_meta_data ->> 'class_name', '')
  );
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- Hàm kiểm tra admin (security definer để tránh đệ quy RLS)
create or replace function public.is_admin()
returns boolean
language sql security definer stable set search_path = public
as $$
  select exists (
    select 1 from public.profiles
    where id = auth.uid() and role = 'admin'
  );
$$;

alter table public.profiles enable row level security;

create policy "read own profile" on public.profiles
  for select to authenticated using (id = auth.uid() or public.is_admin());
create policy "update own profile" on public.profiles
  for update to authenticated using (id = auth.uid())
  with check (id = auth.uid() and role = 'student'); -- không tự thăng quyền

-- ---------- Bài đăng (video, bài giảng) ----------
create table if not exists public.posts (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  title text not null,
  body text not null default '',
  video_url text not null default '',
  published boolean not null default true
);

alter table public.posts enable row level security;
create policy "anyone reads published posts" on public.posts
  for select using (published or public.is_admin());
create policy "admin manages posts" on public.posts
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- ---------- Đề kiểm tra ----------
-- questions (jsonb) là mảng câu hỏi, mỗi câu một trong 3 dạng:
--  { "type":"multiple_choice", "question":html, "options":[html×4], "answer":0-3, "explanation":html }
--  { "type":"true_false", "question":html, "statements":[{"text":html,"answer":bool}×4], "explanation":html }
--  { "type":"short_answer", "question":html, "answer":"1,25", "explanation":html }
create table if not exists public.exams (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  title text not null,
  duration_minutes int not null default 45,
  published boolean not null default false,
  questions jsonb not null default '[]',
  question_count int generated always as (jsonb_array_length(questions)) stored
);

alter table public.exams enable row level security;
create policy "students read published exams" on public.exams
  for select to authenticated using (published or public.is_admin());
create policy "admin manages exams" on public.exams
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

-- ---------- Kết quả bài làm ----------
create table if not exists public.exam_results (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  student_id uuid not null references public.profiles (id) on delete cascade,
  exam_id bigint not null references public.exams (id) on delete cascade,
  score numeric(4, 2) not null,
  detail jsonb not null default '{}', -- đáp án đã chọn, số câu đúng từng phần
  duration_seconds int not null default 0
);

create index if not exists exam_results_exam_idx on public.exam_results (exam_id, created_at desc);
create index if not exists exam_results_student_idx on public.exam_results (student_id, created_at desc);

alter table public.exam_results enable row level security;
create policy "student inserts own result" on public.exam_results
  for insert to authenticated with check (student_id = auth.uid());
create policy "student reads own results" on public.exam_results
  for select to authenticated using (student_id = auth.uid() or public.is_admin());

-- ---------- Tin nhắn ----------
-- Gửi cho 1 học sinh (recipient_id) hoặc cả lớp (class_name), hoặc tất cả (both null)
create table if not exists public.messages (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  sender_id uuid not null references public.profiles (id),
  recipient_id uuid references public.profiles (id) on delete cascade,
  class_name text,
  subject text not null default '',
  body text not null
);

create index if not exists messages_recipient_idx on public.messages (recipient_id, created_at desc);

alter table public.messages enable row level security;
create policy "admin sends messages" on public.messages
  for insert to authenticated with check (public.is_admin() and sender_id = auth.uid());
create policy "read own messages" on public.messages
  for select to authenticated using (
    public.is_admin()
    or recipient_id = auth.uid()
    or (recipient_id is null and (
      class_name is null
      or class_name = (select class_name from public.profiles where id = auth.uid())
    ))
  );

-- ============================================================
-- SAU KHI ĐĂNG KÝ TÀI KHOẢN CỦA THẦY trên web, chạy lệnh này
-- để cấp quyền admin (thay email cho đúng):
--
--   update public.profiles set role = 'admin'
--   where id = (select id from auth.users where email = 'itachi2601@gmail.com');
-- ============================================================
