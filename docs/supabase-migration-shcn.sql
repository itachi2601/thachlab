-- Module SHCN (sinh hoạt chủ nhiệm) cho lớp chủ nhiệm CTTC.
--
-- Ba việc tách bạch nhau:
--   1. Điểm danh HÀNG NGÀY do lớp trưởng / lớp phó nhập (homeroom_daily_attendance) —
--      độc lập với tiết SHCN và với attendance_sessions của GVCN (mỗi buổi 1 dòng tổng hợp,
--      không phải 1 dòng / sinh viên: lớp trưởng chỉ báo sĩ số + danh sách vắng).
--   2. Nội dung sinh hoạt TUẦN (homeroom_weekly_sessions) — chép lại phần đã lược của biên bản
--      tuần (tuan-XX.json) để sinh viên xem lại trên web. KHÔNG thay thế quy trình nộp biên bản
--      .docx lên portal.caothang.edu.vn.
--   3. Ai được nhập điểm danh hàng ngày (homeroom_monitors).
--
-- Khác với bản mô tả gốc của spec, để khớp schema đang chạy:
--   * "lop_id TEXT" → course_id bigint → course_offerings: 1 lớp chủ nhiệm = 1 khóa dưới môn
--     'gddd-ptnn' (xem supabase-migration-cttc-homeroom.sql). Năm học lấy từ course_offerings.
--   * Role "lop_truong" KHÔNG thêm vào profiles.role: lớp trưởng vẫn là sinh viên (role
--     'student', vẫn học/làm bài như bạn cùng lớp), quyền nhập điểm danh cấp qua bảng
--     homeroom_monitors theo từng lớp — giống cách course_instructors cấp quyền cho giảng viên.
--     Nhờ vậy 1 lớp có thể có cả lớp trưởng lẫn lớp phó mà không đụng tới hệ thống role.
--   * Site xuất tĩnh, không có API route: mọi ràng buộc "chỉ sửa được ngày hôm nay", "chỉ lớp
--     của mình" nằm ở RLS bên dưới, không nằm ở tầng ứng dụng.
--
-- Chạy sau supabase-migration-cttc-homeroom.sql. Idempotent.

-- ---------- Ngày hiện tại theo giờ Việt Nam ----------
-- current_date của Postgres tính theo UTC: từ 00:00 đến 07:00 giờ VN sẽ vẫn là "hôm qua",
-- lớp trưởng điểm danh đầu giờ sáng sẽ bị RLS chặn. Mọi chỗ khóa theo ngày dùng hàm này.
create or replace function public.vn_today()
returns date language sql stable set search_path = public
as $$ select (now() at time zone 'Asia/Ho_Chi_Minh')::date $$;

-- ---------- Lớp trưởng / lớp phó ----------
create table if not exists public.homeroom_monitors (
  course_id bigint not null references public.course_offerings(id) on delete cascade,
  student_id uuid not null references public.profiles(id) on delete cascade,
  role text not null default 'lop_truong' check (role in ('lop_truong', 'lop_pho')),
  assigned_by uuid references public.profiles(id) on delete set null,
  assigned_at timestamptz not null default now(),
  primary key (course_id, student_id)
);
create index if not exists homeroom_monitors_student_idx
  on public.homeroom_monitors(student_id, course_id);

-- true nếu người đang đăng nhập là lớp trưởng/lớp phó của đúng lớp này.
create or replace function public.is_homeroom_monitor(p_course_id bigint)
returns boolean language sql security definer stable set search_path = public
as $$
  select exists (
    select 1 from public.homeroom_monitors
    where course_id = p_course_id and student_id = auth.uid()
  );
$$;

-- true nếu người đang đăng nhập đang học lớp này (dùng cho quyền xem).
create or replace function public.is_course_member(p_course_id bigint)
returns boolean language sql security definer stable set search_path = public
as $$
  select exists (
    select 1 from public.course_enrollments
    where course_id = p_course_id and student_id = auth.uid() and status = 'active'
  );
$$;

alter table public.homeroom_monitors enable row level security;

drop policy if exists "teachers manage homeroom monitors" on public.homeroom_monitors;
create policy "teachers manage homeroom monitors" on public.homeroom_monitors
  for all to authenticated
  using (public.can_manage_course(course_id))
  with check (public.can_manage_course(course_id));

drop policy if exists "class members read homeroom monitors" on public.homeroom_monitors;
create policy "class members read homeroom monitors" on public.homeroom_monitors
  for select to authenticated using (student_id = auth.uid() or public.is_course_member(course_id));

-- ---------- Điểm danh hàng ngày ----------
create table if not exists public.homeroom_daily_attendance (
  id bigint generated always as identity primary key,
  course_id bigint not null references public.course_offerings(id) on delete cascade,
  attendance_date date not null,
  headcount int not null check (headcount >= 0),
  present_count int not null check (present_count >= 0),
  -- [{student_id, full_name, reason}] — student_id có thể null nếu sinh viên chưa có tài khoản.
  absentees jsonb not null default '[]'::jsonb
    check (jsonb_typeof(absentees) = 'array'),
  submitted_by uuid references public.profiles(id) on delete set null,
  submitted_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (course_id, attendance_date),
  check (present_count <= headcount)
);
create index if not exists homeroom_daily_attendance_course_date_idx
  on public.homeroom_daily_attendance(course_id, attendance_date desc);

alter table public.homeroom_daily_attendance enable row level security;

drop policy if exists "teachers manage homeroom daily attendance" on public.homeroom_daily_attendance;
create policy "teachers manage homeroom daily attendance" on public.homeroom_daily_attendance
  for all to authenticated
  using (public.can_manage_course(course_id))
  with check (public.can_manage_course(course_id));

-- Lớp trưởng: chỉ lớp mình, chỉ ngày hôm nay (không sửa lùi ngày cũ, không nhập trước ngày mai).
drop policy if exists "monitors insert today attendance" on public.homeroom_daily_attendance;
create policy "monitors insert today attendance" on public.homeroom_daily_attendance
  for insert to authenticated
  with check (public.is_homeroom_monitor(course_id) and attendance_date = public.vn_today());

drop policy if exists "monitors update today attendance" on public.homeroom_daily_attendance;
create policy "monitors update today attendance" on public.homeroom_daily_attendance
  for update to authenticated
  using (public.is_homeroom_monitor(course_id) and attendance_date = public.vn_today())
  with check (public.is_homeroom_monitor(course_id) and attendance_date = public.vn_today());

-- Cả lớp xem được điểm danh của lớp mình (minh bạch, và để lớp trưởng nạp lại bản ghi cũ).
drop policy if exists "class members read homeroom daily attendance" on public.homeroom_daily_attendance;
create policy "class members read homeroom daily attendance" on public.homeroom_daily_attendance
  for select to authenticated using (public.is_course_member(course_id));

-- ---------- Nội dung sinh hoạt tuần ----------
create table if not exists public.homeroom_weekly_sessions (
  id bigint generated always as identity primary key,
  course_id bigint not null references public.course_offerings(id) on delete cascade,
  week_no int not null check (week_no between 1 and 53),
  met_on date,
  -- [{tieu_de, ghi_chu}] — đã lược theo lớp, tối đa 5 mục như biên bản nộp portal.
  announcements jsonb not null default '[]'::jsonb
    check (jsonb_typeof(announcements) = 'array' and jsonb_array_length(announcements) <= 5),
  -- Tên chủ đề GDĐĐ&PTNN, vd 'Chủ đề 2: Kỹ năng sống'.
  ethics_topic text not null default '',
  -- [text] — CHỈ các trọng tâm đã dạy buổi đó, không phải cả chủ đề.
  ethics_taught jsonb not null default '[]'::jsonb
    check (jsonb_typeof(ethics_taught) = 'array'),
  headcount int check (headcount >= 0),
  present_count int check (present_count >= 0),
  created_by uuid references public.profiles(id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (course_id, week_no)
);
create index if not exists homeroom_weekly_sessions_course_idx
  on public.homeroom_weekly_sessions(course_id, week_no desc);

alter table public.homeroom_weekly_sessions enable row level security;

drop policy if exists "teachers manage homeroom weekly sessions" on public.homeroom_weekly_sessions;
create policy "teachers manage homeroom weekly sessions" on public.homeroom_weekly_sessions
  for all to authenticated
  using (public.can_manage_course(course_id))
  with check (public.can_manage_course(course_id));

drop policy if exists "class members read homeroom weekly sessions" on public.homeroom_weekly_sessions;
create policy "class members read homeroom weekly sessions" on public.homeroom_weekly_sessions
  for select to authenticated using (public.is_course_member(course_id));

-- ---------- Lớp trưởng thấy danh sách lớp để tick vắng ----------
-- Sinh viên thường chỉ đọc được dòng course_enrollments của chính mình và profile của chính
-- mình; lớp trưởng cần cả danh sách lớp. Hai policy dưới mở đúng phạm vi đó, và phần kiểm tra
-- "có phải lớp trưởng không" nằm trong hàm security definer để không bị chính RLS của
-- course_enrollments chặn (khác với các policy instructors vốn chạy dưới quyền giảng viên).

drop policy if exists "monitors read class enrollments" on public.course_enrollments;
create policy "monitors read class enrollments" on public.course_enrollments
  for select to authenticated using (public.is_homeroom_monitor(course_id));

create or replace function public.is_homeroom_classmate(p_profile_id uuid)
returns boolean language sql security definer stable set search_path = public
as $$
  select exists (
    select 1 from public.course_enrollments e
    join public.homeroom_monitors m on m.course_id = e.course_id
    where e.student_id = p_profile_id and m.student_id = auth.uid()
  );
$$;

drop policy if exists "monitors read classmate profiles" on public.profiles;
create policy "monitors read classmate profiles" on public.profiles
  for select to authenticated using (public.is_homeroom_classmate(profiles.id));
