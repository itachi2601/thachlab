-- ============================================================================
-- 9/10/2026 — Báo qua chuông thông báo khi thầy giao bài kiểm tra / bài tập có đề cho lớp
--
-- Thầy chốt 8/10/2026: trang chủ học sinh không còn hiện bài kiểm tra/BTVN giao chung cho cả lớp (chỉ gợi việc thích ứng).
-- Để em không lỡ bài, mỗi lần giao bài có đề, mọi học sinh đã vào lớp (user_classes.status = 'active') nhận một thông báo
-- ở chuông (/thong-bao) có đường dẫn thẳng tới đề.
--   * class_assessments (INSERT, published_at rỗng hoặc đã tới giờ): kind 'assessment_new'.
--   * class_announcements (INSERT, có exam_id): kind 'homework_new'.
-- Chỉ gửi cho tài khoản có role = 'student'. Chỉ thêm hàm + trigger mới (không đổi dữ liệu cũ); không gửi bù cho bài đã giao trước đây.
-- Bài hẹn giờ (published_at trong tương lai) chưa báo — sẽ không có thông báo khi tới giờ (cần job riêng nếu thầy dùng hẹn giờ).
-- Cách chạy: bash scripts/run-migrations.sh — giờ nào cũng được.
-- Rollback: perf/rollback/20261009100000_notify_exam_assigned.down.sql
-- ============================================================================

create or replace function public.notify_class_students(p_class_id bigint, p_kind text, p_title text, p_body text, p_href text)
returns void
language sql security definer set search_path = public
as $$
  insert into public.notifications (user_id, kind, title, body, href)
  select uc.user_id, p_kind, p_title, coalesce(p_body, ''), coalesce(p_href, '')
  from public.user_classes uc
  join public.profiles p on p.id = uc.user_id and p.role = 'student'
  where uc.class_id = p_class_id and uc.status = 'active';
$$;
revoke all on function public.notify_class_students(bigint, text, text, text, text) from public, anon, authenticated;

create or replace function public.trg_notify_assessment_assigned()
returns trigger
language plpgsql security definer set search_path = public
as $$
declare
  v_title text;
begin
  if new.published_at is not null and new.published_at > now() then return new; end if;
  select title into v_title from public.exams where id = new.exam_id;
  perform public.notify_class_students(
    new.class_id, 'assessment_new',
    'Bài kiểm tra mới: ' || coalesce(v_title, 'đề của lớp'),
    'Em làm khi đã sẵn sàng.',
    '/kiem-tra/lam?id=' || new.exam_id);
  return new;
end; $$;

drop trigger if exists trg_notify_assessment_assigned on public.class_assessments;
create trigger trg_notify_assessment_assigned
  after insert on public.class_assessments
  for each row execute function public.trg_notify_assessment_assigned();

create or replace function public.trg_notify_homework_assigned()
returns trigger
language plpgsql security definer set search_path = public
as $$
declare
  v_title text;
begin
  if new.exam_id is null then return new; end if;
  select title into v_title from public.exams where id = new.exam_id;
  perform public.notify_class_students(
    new.class_id, 'homework_new',
    'Bài tập mới: ' || coalesce(v_title, 'đề của lớp'),
    left(coalesce(new.body, ''), 140),
    '/kiem-tra/lam?id=' || new.exam_id);
  return new;
end; $$;

drop trigger if exists trg_notify_homework_assigned on public.class_announcements;
create trigger trg_notify_homework_assigned
  after insert on public.class_announcements
  for each row execute function public.trg_notify_homework_assigned();
