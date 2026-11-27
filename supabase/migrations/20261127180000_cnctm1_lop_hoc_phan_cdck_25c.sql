-- Lớp học phần "Công nghệ chế tạo máy 1" cho lớp CĐ CK 25C (27/11/2026).
-- Bối cảnh: lớp học phần `CĐ CK 25C - Công nghệ chế tạo máy 1` (id 12, mã CNCTM-25C) đã tạo từ 26/11
-- nhưng chưa có SV; ô chọn môn trong dashboard thiếu mã 'cnctm' nên lớp không hiện trong tab của môn.
-- SV đang vào lớp nội dung `cnctm` bằng link đăng ký (user_classes active) nhưng KHÔNG tự có dòng
-- course_enrollments → bảng điểm/điểm danh trống, profiles.track bị trigger user_classes đặt 'thpt'.
-- Migration này (chỉ dữ liệu + 1 trigger, idempotent):
--   1. Trigger sau khi một SV vào lớp đang hoạt động: nếu slug lớp trùng mã môn VÀ môn đó chỉ có ĐÚNG
--      MỘT lớp học phần đang hoạt động thì ghi danh luôn vào lớp học phần đó (mơ hồ = bỏ qua, để thầy
--      chọn tay). Nhờ vậy SV vào lớp sau này cũng có mặt trong bảng điểm.
--   2. Backfill các SV đang học lớp 'cnctm' (CĐ CK 25C) và 'gcpt' (CĐ CK 25B) vào lớp học phần tương ứng.
-- Rollback ở cuối file.

begin;

-- 1. Trigger đồng bộ: user_classes (active) → course_enrollments khi môn chỉ có 1 lớp học phần.
create or replace function public.sync_class_to_course_enrollment()
returns trigger
language plpgsql
security definer
set search_path to 'public'
as $$
declare
  v_slug text;
  v_course bigint;
  v_count int;
begin
  if new.status <> 'active' then
    return new;
  end if;

  select c.slug into v_slug from public.classes c where c.id = new.class_id;
  if v_slug is null then
    return new;
  end if;

  select count(*), min(co.id) into v_count, v_course
  from public.course_offerings co
  join public.subjects s on s.id = co.subject_id
  where s.code = v_slug and co.status = 'active';

  -- 0 lớp học phần → môn chưa mở lớp; >1 → nhiều khoá (vd AVCN 24A / CGKL 25A), không đoán.
  if v_count <> 1 then
    return new;
  end if;

  insert into public.course_enrollments (course_id, student_id, status, approved_at)
  values (v_course, new.user_id, 'active', now())
  on conflict (course_id, student_id) do update
    set status = 'active',
        approved_at = coalesce(course_enrollments.approved_at, now());

  return new;
end;
$$;

revoke all on function public.sync_class_to_course_enrollment() from public, anon, authenticated;

drop trigger if exists trg_sync_class_to_course on public.user_classes;
create trigger trg_sync_class_to_course
after insert or update of status on public.user_classes
for each row execute function public.sync_class_to_course_enrollment();

-- 2. Backfill SV đang học lớp nội dung 'cnctm' / 'gcpt' vào lớp học phần đang hoạt động của môn đó.
insert into public.course_enrollments (course_id, student_id, status, approved_at)
select co.id, uc.user_id, 'active', now()
from public.course_offerings co
join public.subjects s on s.id = co.subject_id
join public.classes c on c.slug = s.code
join public.user_classes uc on uc.class_id = c.id and uc.status = 'active'
join public.profiles p on p.id = uc.user_id and p.role = 'student'
where s.code in ('cnctm', 'gcpt')
  and co.status = 'active'
  and (select count(*) from public.course_offerings x where x.subject_id = s.id and x.status = 'active') = 1
on conflict (course_id, student_id) do update
  set status = 'active',
      approved_at = coalesce(course_enrollments.approved_at, now());

commit;

-- Kiểm lại: mỗi lớp học phần có bao nhiêu SV active + track của SV
select co.id, co.name, co.class_label, s.code, co.join_code,
       (select count(*) from public.course_enrollments e
         where e.course_id = co.id and e.status = 'active') as active_students
from public.course_offerings co
join public.subjects s on s.id = co.subject_id
where s.code in ('cnctm', 'gcpt')
order by co.id;

-- ROLLBACK (chạy tay khi cần):
-- begin;
-- drop trigger if exists trg_sync_class_to_course on public.user_classes;
-- drop function if exists public.sync_class_to_course_enrollment();
-- -- Dòng course_enrollments giữ nguyên (là ghi danh thật); muốn xoá sạch của lớp CNCTM 25C:
-- -- delete from public.course_enrollments where course_id = (select id from public.course_offerings where join_code = 'CNCTM-25C');
-- commit;
