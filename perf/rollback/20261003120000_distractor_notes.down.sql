-- Rollback 20261003120000_distractor_notes.sql: gỡ hàm ghi chú + trả question_content_hash về bản trước.
-- LƯU Ý: nếu đã ghi distractorNotes vào đề/ngân hàng, hash các câu đó sẽ đổi sau rollback — gỡ key đó trước
--   (update exams/question_bank bỏ 'distractorNotes') hoặc đừng rollback.
begin;

CREATE OR REPLACE FUNCTION public.question_content_hash(q jsonb)
 RETURNS text
 LANGUAGE sql
 IMMUTABLE
AS $$
  select md5(regexp_replace(
    (q - 'topic' - 'form' - 'explanation' - 'bank_id' - 'difficulty' - 'difficultySource')::text,
    '/[0-9]{10,}-', '/', 'g'));
$$;

drop function if exists public.bank_set_distractor_notes(bigint, jsonb);

commit;
