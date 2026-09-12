-- ============================================================
-- Migration: profiles.track — nguồn sự thật duy nhất cho "học sinh thuộc hệ nào"
-- Chạy SAU: supabase-migration-classes.sql, supabase-migration-course-enrollments.sql,
--           supabase-migration-user-classes-approval.sql
-- Idempotent — chạy lại được.
--
-- Trước migration này, hệ của học sinh chỉ suy ra ngầm qua việc có mặt ở user_classes
-- (THPT) hay course_enrollments (CTTC) — không có gì ngăn 1 học sinh dính cả 2 hoặc
-- không dính bảng nào, và mọi nơi cần "danh sách học sinh hệ X" phải tự nhớ join/loại
-- trừ bảng kia (đã phải vá 2 lần trong 1 ngày: fetchUnassignedStudents, rồi
-- fetchCttcStudentIds cho nhãn cảnh báo). Cột track dưới đây thay thế toàn bộ các join đó.
-- ============================================================

alter table public.profiles add column if not exists track text check (track in ('thpt', 'cttc'));
create index if not exists profiles_track_idx on public.profiles (track);

-- Tự động gắn track khi có dòng mới ở user_classes (THPT) hoặc course_enrollments (CTTC).
-- CTTC được ưu tiên khi xung đột: ghi danh CTTC đòi hỏi hành động rõ ràng (nhập mã khóa),
-- đáng tin hơn 1 dòng user_classes (có thể do gán nhầm — đúng tình huống vừa gặp).
create or replace function public.set_profile_track_thpt()
returns trigger
language plpgsql security definer set search_path = public
as $$
begin
  update public.profiles set track = 'thpt'
  where id = new.user_id and track is distinct from 'cttc';
  return new;
end;
$$;

drop trigger if exists trg_set_track_thpt on public.user_classes;
create trigger trg_set_track_thpt
  after insert on public.user_classes
  for each row execute function public.set_profile_track_thpt();

create or replace function public.set_profile_track_cttc()
returns trigger
language plpgsql security definer set search_path = public
as $$
begin
  update public.profiles set track = 'cttc' where id = new.student_id;
  return new;
end;
$$;

drop trigger if exists trg_set_track_cttc on public.course_enrollments;
create trigger trg_set_track_cttc
  after insert on public.course_enrollments
  for each row execute function public.set_profile_track_cttc();

-- ---------- Backfill dữ liệu hiện có (CTTC ưu tiên nếu dính cả 2, lý do ở trên) ----------
update public.profiles p set track = 'thpt'
where track is null
  and exists (select 1 from public.user_classes uc where uc.user_id = p.id);

update public.profiles p set track = 'cttc'
where exists (select 1 from public.course_enrollments ce where ce.student_id = p.id);
