-- ============================================================
-- Thoát phụ đạo bằng tự kiểm tra — cách 2 bên cạnh đăng ký học (tutoring-slots.sql)
-- ============================================================
-- Chạy SAU:
--   docs/supabase-migration-tutoring-needs.sql   (tutoring_needs, teaches_student)
--   docs/supabase-migration-question-bank.sql    (question_bank)
-- Idempotent — chạy lại được.
--
-- Em tự ôn rồi làm một bài ~20 câu bốc ngẫu nhiên từ ngân hàng đúng chủ đề đang hổng
-- (features/exams/types.ts:pickRandom, chấm ở client như mọi đề khác trong app — xem
-- ExamRunner/PracticeSession). Phần không thể để client tự khai nằm ở DB: đếm lượt còn
-- lại, tính lại pct/passed, và tự đóng mục tutoring_needs khi đạt — theo đúng khuôn
-- tutoring_slot_register()/trg_tutoring_covered() ở hai file trên.
-- ============================================================


-- ---------- 1. Một lượt tự kiểm tra ----------
create table if not exists public.tutoring_exit_attempts (
  id bigint generated always as identity primary key,
  tutoring_need_id bigint not null references public.tutoring_needs (id) on delete cascade,
  student_id uuid not null references public.profiles (id) on delete cascade,
  topic_id bigint,                      -- do trigger điền từ tutoring_needs, client không gửi
  form text not null default '',
  question_ids bigint[] not null default '{}',
  total int not null check (total > 0),
  correct int not null check (correct >= 0 and correct <= total),
  pct int not null default 0,           -- do trigger tính
  passed boolean not null default false, -- do trigger tính
  created_at timestamptz not null default now()
);
create index if not exists tutoring_exit_attempts_need_idx
  on public.tutoring_exit_attempts (tutoring_need_id, student_id);

alter table public.tutoring_exit_attempts enable row level security;

drop policy if exists "student logs own exit attempt" on public.tutoring_exit_attempts;
create policy "student logs own exit attempt" on public.tutoring_exit_attempts
  for insert to authenticated
  with check (student_id = auth.uid());

drop policy if exists "read own exit attempts" on public.tutoring_exit_attempts;
create policy "read own exit attempts" on public.tutoring_exit_attempts
  for select to authenticated
  using (student_id = auth.uid() or public.teaches_student(student_id));


-- ---------- 2. Chặn gian lận lượt + tự tính pct/passed ----------
-- Tối đa 3 lượt/mục; mục phải còn đang cần phụ đạo và đúng là của em gửi lên.
create or replace function public.tutoring_exit_attempt_guard()
returns trigger language plpgsql security definer set search_path = public
as $$
declare
  v_need public.tutoring_needs%rowtype;
  v_count int;
begin
  select * into v_need from public.tutoring_needs where id = new.tutoring_need_id;
  if not found or v_need.student_id <> new.student_id then
    raise exception 'Không tìm thấy mục cần phụ đạo của em';
  end if;
  if v_need.status not in ('open', 'assigned', 'tutored') then
    raise exception 'Chủ đề này không còn cần phụ đạo';
  end if;

  select count(*) into v_count from public.tutoring_exit_attempts
    where tutoring_need_id = new.tutoring_need_id and student_id = new.student_id;
  if v_count >= 3 then
    raise exception 'Em đã dùng hết 3 lượt tự kiểm tra cho chủ đề này — hãy đăng ký buổi phụ đạo.';
  end if;

  new.topic_id := v_need.topic_id;
  new.form := v_need.form;
  new.pct := round(new.correct * 100.0 / new.total)::int;
  new.passed := new.pct >= 80;
  return new;
end; $$;
drop trigger if exists trg_tutoring_exit_attempt_guard on public.tutoring_exit_attempts;
create trigger trg_tutoring_exit_attempt_guard before insert on public.tutoring_exit_attempts
  for each row execute function public.tutoring_exit_attempt_guard();


-- ---------- 3. Đạt 80% -> tự đóng mục cần phụ đạo ----------
create or replace function public.trg_tutoring_exit_attempt_clear()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  if new.passed then
    update public.tutoring_needs
      set status = 'cleared',
          cleared_at = now(),
          last_seen_at = now(),
          note = 'Tự kiểm tra thoát phụ đạo, đạt ' || new.pct || '%'
      where id = new.tutoring_need_id and status in ('open', 'assigned', 'tutored');
  end if;
  return new;
end; $$;
drop trigger if exists trg_tutoring_exit_attempt_clear on public.tutoring_exit_attempts;
create trigger trg_tutoring_exit_attempt_clear after insert on public.tutoring_exit_attempts
  for each row execute function public.trg_tutoring_exit_attempt_clear();


-- ---------- 4. Học sinh đọc được câu hỏi đúng chủ đề mình đang hổng ----------
-- question_bank trước giờ chỉ giáo viên đọc được (kể cả câu của đề chưa publish) — mở hẹp
-- thêm cho học sinh, chỉ đúng chủ đề đang trong danh sách cần phụ đạo của chính em, không
-- phải toàn bộ ngân hàng.
drop policy if exists "student reads exit-quiz bank questions" on public.question_bank;
create policy "student reads exit-quiz bank questions" on public.question_bank
  for select to authenticated
  using (
    archived = false
    and exists (
      select 1 from public.tutoring_needs n
      where n.student_id = auth.uid()
        and n.topic_id = question_bank.topic_id
        and n.status in ('open', 'assigned', 'tutored')
    )
  );
