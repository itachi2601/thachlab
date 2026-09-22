-- ============================================================
-- Migration: Ghi nhận quá trình học tập — tách "hoàn thành" và "đạt yêu cầu"
-- Thiết kế: plan luminous-juggling-leaf (xem trong phiên làm việc)
-- Chạy SAU: supabase-schema.sql, supabase-migration-lessons.sql,
--           supabase-migration-lesson-sections-v4.sql,
--           supabase-migration-exam-analytics.sql
-- Idempotent — chạy lại được. KHÔNG đổi ngữ nghĩa cột cũ, chỉ cộng thêm.
-- ============================================================

-- ============================================================
-- 1. Ngưỡng "đạt" — tùy chọn, giáo viên tự cấu hình, mặc định null
--    (null = chưa cấu hình, không suy ra "chưa đạt")
-- ============================================================

-- Đề kiểm tra/BTVN: điểm đạt thang 10.
alter table public.exams add column if not exists pass_score numeric(4, 2);

-- Mục bài học:
--  quiz_min_correct     -> lý thuyết có quiz: số câu đúng tối thiểu để đạt
--  practice_pass_score  -> luyện tập: điểm đạt thang 10 (áp cho phiên cao nhất)
--  required             -> có tính vào tiến độ bắt buộc không (mặc định true,
--                          giữ nguyên hành vi % tiến độ hiện tại; giáo viên tắt
--                          cho mục đọc thêm/không giao).
alter table public.lesson_items add column if not exists quiz_min_correct int;
alter table public.lesson_items add column if not exists practice_pass_score numeric(4, 2);
alter table public.lesson_items add column if not exists required boolean not null default true;


-- ============================================================
-- 2. Chống nộp trùng khi mạng lỗi rồi thử lại — client_token do trình duyệt
--    sinh một lần/lượt làm, giữ nguyên khi bấm lại. Client tự SELECT theo
--    token trước khi INSERT (đã được đọc qua policy sẵn có "đọc của mình"),
--    không cần policy UPDATE mới (tránh học sinh tự sửa điểm qua REST).
-- ============================================================
alter table public.exam_results add column if not exists client_token uuid not null default gen_random_uuid();
create unique index if not exists exam_results_client_token_key on public.exam_results (client_token);

alter table public.practice_sessions add column if not exists client_token uuid not null default gen_random_uuid();
create unique index if not exists practice_sessions_client_token_key on public.practice_sessions (client_token);


-- ============================================================
-- 3. Chấm tay câu tự luận ("chờ chấm") — cộng cột, không đổi earned/max
--    tự động chấm hiện có (vẫn 0/0 cho tới khi giáo viên chấm).
-- ============================================================
alter table public.exam_question_results add column if not exists manual_earned numeric(4, 2);
alter table public.exam_question_results add column if not exists manual_max numeric(4, 2);
alter table public.exam_question_results add column if not exists graded_by uuid references public.profiles (id) on delete set null;
alter table public.exam_question_results add column if not exists graded_at timestamptz;

-- Chấm qua RPC security definer — không mở policy UPDATE rộng cho giáo viên
-- trên cả bảng (tránh sửa được earned/is_correct của câu tự động chấm).
create or replace function public.grade_essay_answer(
  p_exam_result_id bigint,
  p_question_index int,
  p_earned numeric,
  p_max numeric
)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  v_student uuid;
  v_qtype text;
begin
  select er.student_id, eqr.qtype into v_student, v_qtype
  from public.exam_question_results eqr
  join public.exam_results er on er.id = eqr.exam_result_id
  where eqr.exam_result_id = p_exam_result_id and eqr.question_index = p_question_index;

  if v_student is null then
    raise exception 'Không tìm thấy câu trả lời này';
  end if;
  if v_qtype <> 'essay' then
    raise exception 'Chỉ chấm tay được câu tự luận';
  end if;
  if not public.teaches_student(v_student) then
    raise exception 'Không có quyền chấm bài học sinh này';
  end if;
  if p_earned < 0 or p_max <= 0 or p_earned > p_max then
    raise exception 'Điểm không hợp lệ';
  end if;

  update public.exam_question_results
  set manual_earned = p_earned, manual_max = p_max, graded_by = auth.uid(), graded_at = now()
  where exam_result_id = p_exam_result_id and question_index = p_question_index;
end;
$$;

-- Điểm cuối cùng của một lượt làm, cộng cả câu tự luận đã chấm — không đụng
-- gradeQuestion()/gradeExam() phía client (dùng để xem lại bài làm ở nhiều nơi).
create or replace view public.exam_result_scores as
select
  eqr.exam_result_id,
  sum(eqr.earned) as auto_earned,
  sum(eqr.max) as auto_max,
  sum(coalesce(eqr.manual_earned, 0)) filter (where eqr.qtype = 'essay') as manual_earned_sum,
  sum(coalesce(eqr.manual_max, 0)) filter (where eqr.qtype = 'essay') as manual_max_sum,
  count(*) filter (where eqr.qtype = 'essay' and eqr.graded_at is null) as pending_essay_count,
  case
    when sum(eqr.max) + sum(coalesce(eqr.manual_max, 0)) filter (where eqr.qtype = 'essay') > 0
      then round(
        (sum(eqr.earned) + sum(coalesce(eqr.manual_earned, 0)) filter (where eqr.qtype = 'essay'))
        / (sum(eqr.max) + sum(coalesce(eqr.manual_max, 0)) filter (where eqr.qtype = 'essay')) * 10,
        2
      )
    else null
  end as final_score10
from public.exam_question_results eqr
group by eqr.exam_result_id;

-- View thừa hưởng RLS của bảng gốc qua security_invoker (Postgres 15+/Supabase hỗ trợ).
alter view public.exam_result_scores set (security_invoker = true);


-- ============================================================
-- 4. Thời điểm bắt đầu/nộp một lượt làm (đề kiểm tra/BTVN/quiz lý thuyết,
--    đều chạy qua ExamRunner) — bảng riêng, KHÔNG đụng exam_results để
--    không phá vỡ các truy vấn/trigger/RPC đang coi mỗi dòng exam_results
--    là một lần nộp đã có điểm (phân tích, cảnh báo, xếp hạng, bảng điểm).
-- ============================================================
create table if not exists public.exam_attempts (
  id bigint generated always as identity primary key,
  client_token uuid not null,
  student_id uuid not null references public.profiles (id) on delete cascade,
  exam_id bigint not null references public.exams (id) on delete cascade,
  item_id bigint references public.lesson_items (id) on delete set null,
  started_at timestamptz not null default now(),
  submitted_at timestamptz,
  exam_result_id bigint references public.exam_results (id) on delete set null
);
create unique index if not exists exam_attempts_client_token_key on public.exam_attempts (client_token);
create index if not exists exam_attempts_student_idx on public.exam_attempts (student_id, started_at desc);
create index if not exists exam_attempts_open_idx on public.exam_attempts (exam_id, started_at) where submitted_at is null;

alter table public.exam_attempts enable row level security;

drop policy if exists "student inserts own attempt" on public.exam_attempts;
create policy "student inserts own attempt" on public.exam_attempts
  for insert to authenticated with check (student_id = auth.uid());

drop policy if exists "student updates own open attempt" on public.exam_attempts;
create policy "student updates own open attempt" on public.exam_attempts
  for update to authenticated
  using (student_id = auth.uid() and submitted_at is null)
  with check (student_id = auth.uid());

drop policy if exists "student reads own attempts" on public.exam_attempts;
create policy "student reads own attempts" on public.exam_attempts
  for select to authenticated
  using (student_id = auth.uid() or public.teaches_student(student_id));

drop policy if exists "admin manages attempts" on public.exam_attempts;
create policy "admin manages attempts" on public.exam_attempts
  for all to authenticated using (public.is_admin()) with check (public.is_admin());


-- ============================================================
-- 5. Vá RLS: lesson_progress chưa từng cho giảng viên (không phải admin)
--    đọc tiến độ học sinh mình phụ trách — cần cho bảng "Quá trình học tập".
-- ============================================================
drop policy if exists "instructor reads student progress" on public.lesson_progress;
create policy "instructor reads student progress" on public.lesson_progress
  for select to authenticated
  using (public.teaches_student(user_id));
