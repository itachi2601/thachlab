-- ============================================================================
-- Ghi chú phương án nhiễu (distractorNotes) cho Luyện tập "Từng câu" — việc B của
-- docs/BAN-GIAO-RANK-THI-THANG-HANG-2026-10-03.md
--
-- Vì sao cần migration dù spec nói "không thêm migration cho việc B":
--  1. Luyện tập đọc câu từ exams.questions (không đọc question_bank), nên ghi chú phải nằm trong exams.questions.
--  2. question_content_hash là KHOÁ NHẬN DIỆN chung của câu giữa đề và ngân hàng (sync_exam_to_bank upsert theo
--     content_hash; trg_bank_tags_to_exams, rank_fix_quiz_start, rank_gate_pool_ids so hash). Hàm hiện bỏ
--     topic/form/explanation/bank_id/difficulty/difficultySource — chưa bỏ distractorNotes. Thêm key mới vào câu
--     mà không sửa hàm này thì hash đổi → trigger tạo THÊM dòng ngân hàng trùng. Nên bỏ distractorNotes khỏi hash:
--     hash của mọi câu hiện có KHÔNG đổi (chưa câu nào có key đó).
--
-- 1. create or replace question_content_hash (thêm "- 'distractorNotes'").
-- 2. bank_set_distractor_notes(p_bank_id, p_notes): chỉ staff/service_role. Ghi ghi chú vào question_bank.question
--    VÀ vào mọi exams.questions có câu cùng content_hash (trigger trg_exams_sync_bank tự đồng bộ ngược ngân hàng,
--    hash không đổi nên không sinh dòng mới). Script scripts/backfill-distractor-notes.mts gọi hàm này.
--
-- Chạy SAU 20260930170000_question_bank_hash_ignore_image_ts.sql nếu file đó còn chờ (thứ tự trong scripts/run-migrations.sh).
-- Cách chạy: bash scripts/run-migrations.sh — nên NGOÀI giờ HS làm bài (hàm hash được dùng khi nộp/đăng đề).
-- Rollback: perf/rollback/20261003120000_distractor_notes.down.sql (chỉ gỡ hàm mới + trả hash cũ; ghi chú đã ghi vào
--   đề/ngân hàng nằm yên, vô hại — nhưng khi đó phải gỡ trước bằng: update exams/question_bank bỏ key distractorNotes,
--   nếu không hash các câu đã ghi chú sẽ đổi).
-- ============================================================================

create or replace function public.question_content_hash(q jsonb)
returns text
language sql
immutable
as $$
  select md5(regexp_replace(
    (q - 'topic' - 'form' - 'explanation' - 'bank_id' - 'difficulty' - 'difficultySource' - 'distractorNotes')::text,
    '/[0-9]{10,}-', '/', 'g'));
$$;

create or replace function public.bank_set_distractor_notes(p_bank_id bigint, p_notes jsonb)
returns int
language plpgsql security definer set search_path = public
as $$
declare
  b public.question_bank%rowtype;
  e record;
  v_clean jsonb;
  v_n int := 0;
begin
  if not (public.rank_is_staff() or coalesce(auth.role(), '') = 'service_role') then
    raise exception 'Không có quyền ghi chú phương án nhiễu';
  end if;
  select * into b from public.question_bank where id = p_bank_id;
  if not found then raise exception 'Không tìm thấy câu #%', p_bank_id; end if;

  -- Chỉ nhận khoá A–D (trắc nghiệm) hoặc 0–3 (đúng–sai), giá trị chuỗi không rỗng, tối đa 300 ký tự.
  select coalesce(jsonb_object_agg(t.k, left(btrim(t.v), 300)), '{}'::jsonb) into v_clean
  from jsonb_each_text(coalesce(p_notes, '{}'::jsonb)) as t (k, v)
  where t.k ~ '^[A-D0-3]$' and btrim(t.v) <> '';
  if v_clean = '{}'::jsonb then return 0; end if;

  -- Đề chứa câu này: lọc nhanh bằng containment theo đề bài trước, rồi so hash từng câu.
  for e in
    select ex.id, (q.ordinality - 1)::int as idx
    from public.exams ex,
         jsonb_array_elements(ex.questions) with ordinality as q (value, ordinality)
    where jsonb_typeof(ex.questions) = 'array'
      and ex.questions @> jsonb_build_array(jsonb_build_object('question', b.question ->> 'question'))
      and public.question_content_hash(q.value) = b.content_hash
  loop
    update public.exams
      set questions = jsonb_set(questions, array[e.idx::text], (questions -> e.idx) || jsonb_build_object('distractorNotes', v_clean))
    where id = e.id;
    v_n := v_n + 1;
  end loop;

  update public.question_bank
    set question = question || jsonb_build_object('distractorNotes', v_clean)
  where id = p_bank_id;
  return v_n;
end; $$;

revoke execute on function public.bank_set_distractor_notes(bigint, jsonb) from public, anon;
grant execute on function public.bank_set_distractor_notes(bigint, jsonb) to authenticated, service_role;
