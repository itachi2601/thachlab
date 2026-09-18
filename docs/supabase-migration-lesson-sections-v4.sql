-- ============================================================
-- Migration: phân loại lại các mục trong bài học
--   §1 Lý thuyết trọng tâm  (ly_thuyet)      — HTML + LaTeX
--   §2 Video bài giảng      (video)
--   §3 Bài tập mẫu          (bai_tap_mau)    — nay gắn ĐỀ (exam_ids): em chọn đáp án,
--        bấm "Kiểm tra" mới hiện lời giải chi tiết. Các "dạng bài" tự luận cũ nằm
--        trong questions jsonb vẫn hiển thị như trước — không mất gì.
--   §4 Luyện tập            (luyen_tap)      — phiên luyện ngẫu nhiên có chấm điểm
--   §5 Bài tập về nhà       (bai_tap_ve_nha) — MỚI: chạy như bài kiểm tra, có hạn nộp
--   §6 Kiểm tra             (kiem_tra)       — giữ nguyên cho bài kiểm tra chính thức
--
-- Chạy SAU: supabase-migration-lessons.sql, supabase-migration-lessons-restructure2.sql,
--           supabase-migration-exam-analytics.sql
-- Idempotent — chạy lại được.
-- ============================================================

-- ---------- 1. Mục mới "bài tập về nhà" + hạn nộp ----------
alter table public.lesson_items drop constraint if exists lesson_items_kind_check;
alter table public.lesson_items
  add constraint lesson_items_kind_check check (kind in
    ('ly_thuyet', 'video', 'bai_tap_mau', 'luyen_tap', 'bai_tap_ve_nha', 'kiem_tra'));

-- Hạn nộp của bài tập về nhà (null = không đặt hạn).
alter table public.lesson_items
  add column if not exists due_at timestamptz;


-- ============================================================
-- 2. Phiên luyện tập — KHÔNG vào bảng điểm, chỉ để em tự theo dõi
--    và để thầy/trợ giảng thấy em hổng chủ đề nào.
-- ============================================================
create table if not exists public.practice_sessions (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  student_id uuid not null references public.profiles (id) on delete cascade,
  lesson_id bigint references public.lessons (id) on delete set null,
  item_id bigint references public.lesson_items (id) on delete set null,
  question_count int not null default 0,
  correct_count int not null default 0,
  score numeric(5,2) not null default 0,       -- thang 10
  duration_seconds int not null default 0,
  timed_out boolean not null default false
);
create index if not exists practice_sessions_student_idx
  on public.practice_sessions (student_id, created_at desc);
create index if not exists practice_sessions_lesson_idx
  on public.practice_sessions (lesson_id, created_at desc);

-- Đúng/sai từng câu kèm nhãn chủ đề — cùng shape với exam_question_results
-- để phần Phân tích/Cảnh báo phụ đạo gộp hai nguồn được về sau.
create table if not exists public.practice_question_results (
  session_id bigint not null references public.practice_sessions (id) on delete cascade,
  question_index int not null,                 -- thứ tự trong phiên (0-based)
  student_id uuid not null references public.profiles (id) on delete cascade,
  exam_id bigint references public.exams (id) on delete set null,
  source_index int not null default 0,         -- vị trí câu trong đề gốc
  topic_id bigint references public.question_topics (id) on delete set null,
  topic_name text not null default '',
  form text not null default '',               -- 'ly_thuyet' | 'bai_tap' | ''
  qtype text not null,
  earned numeric(4,2) not null default 0,
  max numeric(4,2) not null default 0,
  is_correct boolean not null default false,
  created_at timestamptz not null default now(),
  primary key (session_id, question_index)
);
create index if not exists pqr_topic_idx on public.practice_question_results (topic_id);
create index if not exists pqr_student_idx on public.practice_question_results (student_id, created_at desc);

alter table public.practice_sessions enable row level security;
alter table public.practice_question_results enable row level security;

drop policy if exists "student reads own practice sessions" on public.practice_sessions;
create policy "student reads own practice sessions" on public.practice_sessions
  for select to authenticated
  using (student_id = auth.uid() or public.teaches_student(student_id));

drop policy if exists "student inserts own practice sessions" on public.practice_sessions;
create policy "student inserts own practice sessions" on public.practice_sessions
  for insert to authenticated with check (student_id = auth.uid());

drop policy if exists "admin manages practice sessions" on public.practice_sessions;
create policy "admin manages practice sessions" on public.practice_sessions
  for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop policy if exists "student reads own practice question results" on public.practice_question_results;
create policy "student reads own practice question results" on public.practice_question_results
  for select to authenticated
  using (student_id = auth.uid() or public.teaches_student(student_id));

drop policy if exists "student inserts own practice question results" on public.practice_question_results;
create policy "student inserts own practice question results" on public.practice_question_results
  for insert to authenticated with check (student_id = auth.uid());

drop policy if exists "admin manages practice question results" on public.practice_question_results;
create policy "admin manages practice question results" on public.practice_question_results
  for all to authenticated using (public.is_admin()) with check (public.is_admin());
