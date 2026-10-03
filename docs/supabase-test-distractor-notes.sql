-- ============================================================
-- Kiểm chứng ghi chú phương án nhiễu — chạy SAU migration 20261003120000_distractor_notes.sql:
--   supabase db query --linked -f docs/supabase-test-distractor-notes.sql
-- Một giao dịch, ROLLBACK ở cuối. Lệch chỗ nào -> raise exception 'D…: …'; chạy xong không lỗi = đạt.
-- Kiểm: hash không đổi khi thêm distractorNotes · hàm ghi vào cả ngân hàng lẫn đề · không sinh dòng ngân hàng mới ·
-- HS thường bị chặn.
-- ============================================================
begin;

do $$
declare
  v_admin uuid;
  v_student uuid;
  b public.question_bank%rowtype;
  v_n_before int;
  v_n_after int;
  v_touched int;
  v_hash0 text;
  v_err text;
begin
  select id into v_admin from public.profiles where role = 'admin' order by id limit 1;
  select id into v_student from public.profiles where role = 'student' order by id limit 1;
  select * into b from public.question_bank
  where not archived and qtype = 'multiple_choice' and source_exam_id is not null
    and question ? 'options' and not (question ? 'distractorNotes')
    and public.question_content_hash(question) = content_hash      -- hàng "sạch": hash khớp
  order by id limit 1;
  if v_admin is null or v_student is null or b.id is null then raise exception 'D0: thiếu admin/HS/câu để thử'; end if;
  v_hash0 := b.content_hash;

  -- hash bỏ qua distractorNotes
  if public.question_content_hash(b.question || '{"distractorNotes":{"A":"x"}}'::jsonb) <> v_hash0 then
    raise exception 'D1: thêm distractorNotes làm đổi content_hash';
  end if;

  select count(*) into v_n_before from public.question_bank;

  -- HS thường không được ghi
  perform set_config('request.jwt.claims', json_build_object('sub', v_student, 'role', 'authenticated')::text, true);
  begin
    perform public.bank_set_distractor_notes(b.id, '{"A":"x"}'::jsonb);
    v_err := null;
  exception when others then v_err := sqlerrm; end;
  if v_err is null or v_err not like '%quyền%' then raise exception 'D2: HS không được ghi ghi chú, được %', v_err; end if;

  -- admin ghi: khoá lạ/rỗng bị lọc, khoá A–D giữ
  perform set_config('request.jwt.claims', json_build_object('sub', v_admin, 'role', 'authenticated')::text, true);
  v_touched := public.bank_set_distractor_notes(b.id, '{"A":"  Nhầm công thức.  ","Z":"bỏ","B":""}'::jsonb);
  if v_touched < 1 then raise exception 'D3: phải ghi được vào ít nhất 1 đề chứa câu này, được %', v_touched; end if;

  select * into b from public.question_bank where id = b.id;
  if b.question #>> '{distractorNotes,A}' <> 'Nhầm công thức.' or b.question -> 'distractorNotes' ? 'Z' or b.question -> 'distractorNotes' ? 'B' then
    raise exception 'D4: ghi chú ngân hàng sai: %', b.question -> 'distractorNotes';
  end if;
  if b.content_hash <> v_hash0 or public.question_content_hash(b.question) <> v_hash0 then raise exception 'D5: hash đổi sau khi ghi'; end if;
  select count(*) into v_n_after from public.question_bank;
  if v_n_after <> v_n_before then raise exception 'D6: ghi chú sinh thêm % dòng ngân hàng (trigger đồng bộ theo hash)', v_n_after - v_n_before; end if;

  if not exists (
    select 1 from public.exams ex, jsonb_array_elements(ex.questions) q
    where jsonb_typeof(ex.questions) = 'array' and ex.id = b.source_exam_id
      and public.question_content_hash(q) = v_hash0 and q #>> '{distractorNotes,A}' = 'Nhầm công thức.'
  ) then raise exception 'D7: đề nguồn chưa có ghi chú'; end if;

  -- ghi toàn khoá rỗng -> không đụng gì
  if public.bank_set_distractor_notes(b.id, '{"Z":"x"}'::jsonb) <> 0 then raise exception 'D8: khoá không hợp lệ phải trả 0'; end if;
end $$;

rollback;
