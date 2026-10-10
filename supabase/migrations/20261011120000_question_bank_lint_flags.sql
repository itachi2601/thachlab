-- Cờ lint cho ngân hàng câu hỏi: cột question_bank.lint_flags (mã cờ mức "lỗi" còn hiệu lực, vd {dollarLe,phuongAnRong}).
-- Rỗng '{}' = câu sạch → trang ngân hàng lọc "Chỉ câu sạch" bằng .eq('lint_flags','{}') thay vì lint lại trên trình duyệt.
-- KHÔNG có regex trong SQL: giá trị do scripts/cap-nhat-lint-flags.mts ghi, dùng lib/question-lint.ts (một nguồn quy tắc).
-- Trigger sync_exam_to_bank (ON CONFLICT … DO UPDATE) và trg_bank_touch không đụng cột này → đồng bộ đề ↔ ngân hàng giữ nguyên lint_flags
-- (câu mới nạp có '{}' mặc định cho tới lần chạy script kế tiếp).
-- Kèm: question_content_hash() bỏ khoá 'lint_ignored' (giáo viên bấm "Bỏ qua cảnh báo" thì câu KHÔNG đổi hash → không sinh câu trùng trong ngân hàng).
-- Hàm hash chỉ đổi kết quả cho câu CÓ khoá lint_ignored; mọi câu hiện có chưa có khoá này nên hash cũ giữ nguyên.

begin;

alter table public.question_bank add column if not exists lint_flags text[] not null default '{}';
create index if not exists idx_question_bank_lint_flags on public.question_bank using gin (lint_flags);

create or replace function public.question_content_hash(q jsonb)
returns text
language sql
immutable
as $$
  select md5(regexp_replace(
    (q - 'topic' - 'form' - 'explanation' - 'bank_id' - 'difficulty' - 'difficultySource' - 'distractorNotes' - 'lint_ignored')::text,
    '/[0-9]{10,}-', '/', 'g'));
$$;

commit;

-- ROLLBACK (chạy tay nếu cần):
-- begin;
-- drop index if exists public.idx_question_bank_lint_flags;
-- alter table public.question_bank drop column if exists lint_flags;
-- create or replace function public.question_content_hash(q jsonb)
-- returns text language sql immutable as $$
--   select md5(regexp_replace(
--     (q - 'topic' - 'form' - 'explanation' - 'bank_id' - 'difficulty' - 'difficultySource' - 'distractorNotes')::text,
--     '/[0-9]{10,}-', '/', 'g'));
-- $$;
-- commit;
