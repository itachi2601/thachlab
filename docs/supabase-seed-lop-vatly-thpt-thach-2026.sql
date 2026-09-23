-- ============================================================
-- Seed lịch dạy Vật lí THPT của thầy Ngô Diệu Thạch — năm học 2026-2027
--
-- Nguồn: bảng phân công lịch dạy (ảnh chụp thời khoá biểu trung tâm).
-- Chỉ seed các lớp của thầy Thạch; lớp của cô Trần Ái Nhân (10L5, 10L6,
-- 11L7) và các môn/giáo viên khác không nằm trong đợt này.
--
-- 12L1 học 2 buổi/tuần (1 buổi A + 1 buổi B), mỗi buổi có 2 khung giờ để
-- chọn (A4/A5, B7/B8). Hệ thống ghi danh (thpt_courses) mỗi khoá chỉ có
-- một lịch cố định, nên tách thành 4 khoá công khai riêng — phụ huynh/
-- học sinh đăng ký 2 lần: một lần ở nhóm buổi A, một lần ở nhóm buổi B.
--
-- Cần chạy SAU: supabase-migration-khoa-hoc-thpt.sql, và sau khi đã bấm
-- "Tạo/cập nhật 4 lớp khối" ở /quan-tri (mục Hệ lớp) để có sẵn classes
-- '10' / '11' / '12'.
--
-- location để trống — thầy Thạch điền phòng/địa chỉ trung tâm sau, ở
-- Dashboard THPT → tab Ghi danh → "Sửa lịch" (không cần chạy lại script).
--
-- Idempotent — chạy lại không tạo trùng (so theo tên khoá + năm học).
-- Chạy trong Supabase → SQL Editor.
-- ============================================================

do $$
declare
  v_school_year text := '2026-2027';
  v_class10 bigint;
  v_class11 bigint;
  v_class12 bigint;
  v_course_id bigint;
begin
  select id into v_class10 from public.classes where name = '10';
  select id into v_class11 from public.classes where name = '11';
  select id into v_class12 from public.classes where name = '12';

  if v_class10 is null or v_class11 is null or v_class12 is null then
    raise exception 'Chưa có lớp khối 10/11/12 — vào /quan-tri, mục Hệ lớp, bấm "Tạo/cập nhật 4 lớp khối" trước.';
  end if;

  -- ---------- 10L3 — Thứ 3, 18g00–21g15 ----------
  select id into v_course_id from public.thpt_courses
    where class_id = v_class10 and name = 'Vật lí 10L3' and school_year = v_school_year;
  if v_course_id is null then
    insert into public.thpt_courses (class_id, name, school_year, is_public, status)
    values (v_class10, 'Vật lí 10L3', v_school_year, true, 'active')
    returning id into v_course_id;
    insert into public.thpt_course_schedules (course_id, weekday, start_time, end_time)
    values (v_course_id, 2, '18:00', '21:15');
  end if;

  -- ---------- 10L4 — Chủ nhật, 08g00–11g15 ----------
  select id into v_course_id from public.thpt_courses
    where class_id = v_class10 and name = 'Vật lí 10L4' and school_year = v_school_year;
  if v_course_id is null then
    insert into public.thpt_courses (class_id, name, school_year, is_public, status)
    values (v_class10, 'Vật lí 10L4', v_school_year, true, 'active')
    returning id into v_course_id;
    insert into public.thpt_course_schedules (course_id, weekday, start_time, end_time)
    values (v_course_id, 7, '08:00', '11:15');
  end if;

  -- ---------- 11L4 — Thứ 2, 18g00–21g15 ----------
  select id into v_course_id from public.thpt_courses
    where class_id = v_class11 and name = 'Vật lí 11L4' and school_year = v_school_year;
  if v_course_id is null then
    insert into public.thpt_courses (class_id, name, school_year, is_public, status)
    values (v_class11, 'Vật lí 11L4', v_school_year, true, 'active')
    returning id into v_course_id;
    insert into public.thpt_course_schedules (course_id, weekday, start_time, end_time)
    values (v_course_id, 1, '18:00', '21:15');
  end if;

  -- ---------- 11L5 — Thứ 6, 18g00–21g15 ----------
  select id into v_course_id from public.thpt_courses
    where class_id = v_class11 and name = 'Vật lí 11L5' and school_year = v_school_year;
  if v_course_id is null then
    insert into public.thpt_courses (class_id, name, school_year, is_public, status)
    values (v_class11, 'Vật lí 11L5', v_school_year, true, 'active')
    returning id into v_course_id;
    insert into public.thpt_course_schedules (course_id, weekday, start_time, end_time)
    values (v_course_id, 5, '18:00', '21:15');
  end if;

  -- ---------- 12L1 — buổi A, khung Thứ 4 (12L1A4) — 19g30–21g30 ----------
  select id into v_course_id from public.thpt_courses
    where class_id = v_class12 and name = 'Vật lí 12L1 — buổi A · Thứ 4 (A4)' and school_year = v_school_year;
  if v_course_id is null then
    insert into public.thpt_courses (class_id, name, description, school_year, is_public, status)
    values (
      v_class12, 'Vật lí 12L1 — buổi A · Thứ 4 (A4)',
      'Lớp 12L1 học 2 buổi/tuần: 1 buổi A + 1 buổi B. Đây là buổi A khung Thứ 4 — đăng ký thêm 1 khoá buổi B (12L1B7 hoặc 12L1B8) nữa để đủ lịch tuần.',
      v_school_year, true, 'active'
    )
    returning id into v_course_id;
    insert into public.thpt_course_schedules (course_id, weekday, start_time, end_time)
    values (v_course_id, 3, '19:30', '21:30');
  end if;

  -- ---------- 12L1 — buổi A, khung Thứ 5 (12L1A5) — 19g30–21g30 ----------
  select id into v_course_id from public.thpt_courses
    where class_id = v_class12 and name = 'Vật lí 12L1 — buổi A · Thứ 5 (A5)' and school_year = v_school_year;
  if v_course_id is null then
    insert into public.thpt_courses (class_id, name, description, school_year, is_public, status)
    values (
      v_class12, 'Vật lí 12L1 — buổi A · Thứ 5 (A5)',
      'Lớp 12L1 học 2 buổi/tuần: 1 buổi A + 1 buổi B. Đây là buổi A khung Thứ 5 — đăng ký thêm 1 khoá buổi B (12L1B7 hoặc 12L1B8) nữa để đủ lịch tuần.',
      v_school_year, true, 'active'
    )
    returning id into v_course_id;
    insert into public.thpt_course_schedules (course_id, weekday, start_time, end_time)
    values (v_course_id, 4, '19:30', '21:30');
  end if;

  -- ---------- 12L1 — buổi B, khung Thứ 7 (12L1B7) — 14g00–16g00 ----------
  select id into v_course_id from public.thpt_courses
    where class_id = v_class12 and name = 'Vật lí 12L1 — buổi B · Thứ 7 (B7)' and school_year = v_school_year;
  if v_course_id is null then
    insert into public.thpt_courses (class_id, name, description, school_year, is_public, status)
    values (
      v_class12, 'Vật lí 12L1 — buổi B · Thứ 7 (B7)',
      'Lớp 12L1 học 2 buổi/tuần: 1 buổi A + 1 buổi B. Đây là buổi B khung Thứ 7 — đăng ký thêm 1 khoá buổi A (12L1A4 hoặc 12L1A5) nữa để đủ lịch tuần.',
      v_school_year, true, 'active'
    )
    returning id into v_course_id;
    insert into public.thpt_course_schedules (course_id, weekday, start_time, end_time)
    values (v_course_id, 6, '14:00', '16:00');
  end if;

  -- ---------- 12L1 — buổi B, khung Chủ nhật (12L1B8) — 14g00–16g00 ----------
  select id into v_course_id from public.thpt_courses
    where class_id = v_class12 and name = 'Vật lí 12L1 — buổi B · CN (B8)' and school_year = v_school_year;
  if v_course_id is null then
    insert into public.thpt_courses (class_id, name, description, school_year, is_public, status)
    values (
      v_class12, 'Vật lí 12L1 — buổi B · CN (B8)',
      'Lớp 12L1 học 2 buổi/tuần: 1 buổi A + 1 buổi B. Đây là buổi B khung Chủ nhật — đăng ký thêm 1 khoá buổi A (12L1A4 hoặc 12L1A5) nữa để đủ lịch tuần.',
      v_school_year, true, 'active'
    )
    returning id into v_course_id;
    insert into public.thpt_course_schedules (course_id, weekday, start_time, end_time)
    values (v_course_id, 7, '14:00', '16:00');
  end if;
end $$;
