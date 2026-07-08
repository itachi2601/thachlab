-- ============================================================
-- Migration: Thêm topic cho mỗi câu hỏi trong exam
-- Chạy trong Supabase Dashboard → SQL Editor
-- ============================================================

-- Cập nhật cấu trúc câu hỏi để thêm topic field
-- Mỗi question trong mảng questions sẽ có thêm field "topic": "Tên chủ đề"
-- Ví dụ:
-- {
--   "type": "multiple_choice",
--   "topic": "Lực & chuyển động",
--   "question": "...",
--   "options": [...],
--   "answer": 0,
--   "explanation": "..."
-- }

-- Ghi chú: Nếu exam cũ không có topic, admin có thể cập nhật thủ công hoặc
-- tạo câu hỏi mới với topic đúng trong supabase dashboard

-- Tạo bảng để lưu detail chi tiết kết quả từng câu (tùy chọn, để query nhanh hơn)
create table if not exists public.exam_question_results (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  exam_result_id bigint not null references public.exam_results (id) on delete cascade,
  question_index int not null, -- vị trí câu hỏi trong đề (0, 1, 2, ...)
  topic text not null, -- chủ đề/kiến thức của câu hỏi
  is_correct boolean not null, -- true nếu trả lời đúng, false nếu sai
  constraint fk_result unique (exam_result_id, question_index)
);

create index if not exists exam_question_results_result_idx on public.exam_question_results (exam_result_id);
create index if not exists exam_question_results_topic_idx on public.exam_question_results (topic);

alter table public.exam_question_results enable row level security;

create policy "student reads own question results" on public.exam_question_results
  for select to authenticated using (
    exam_result_id in (
      select id from public.exam_results
      where student_id = auth.uid()
    )
    or (select public.is_admin())
  );

create policy "admin manages question results" on public.exam_question_results
  for all to authenticated using (public.is_admin()) with check (public.is_admin());
