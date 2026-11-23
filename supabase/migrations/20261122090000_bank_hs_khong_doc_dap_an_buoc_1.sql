-- ============================================================================
-- Vá bảo mật chặng 4 — question_bank lộ đáp án cho HS — BƯỚC 1/2: thêm hàm (22/11/2026)
-- Lỗ: 2 policy SELECT "student reads exit-quiz bank questions" + "student reads entry-diagnostic bank questions"
-- cho HS đọc NGUYÊN dòng question_bank (cột question có answer/answers/statements[].answer/explanation) của chủ đề
-- em đang cần phụ đạo hoặc đang làm chẩn đoán. Ngân hàng là bản sao exams.questions → kể cả câu của ĐỀ ĐÁNH GIÁ
-- (kiểm tra/BTVN) mà chặng 1–3 đã giấu. Thêm nữa: bài tự kiểm tra thoát phụ đạo do máy HS tự chấm rồi INSERT
-- tutoring_exit_attempts.correct → gửi thẳng 20/20 là gỡ được mục phụ đạo.
--
-- Hàm mới (RPC cho authenticated) — CHỈ THÊM, client cũ chạy tiếp như cũ:
--   bank_questions_for_student(p_topic_ids, p_form, p_source_exam_ids, p_limit) → jsonb
--       câu ngân hàng ĐÃ LƯỢC đáp án (exam_q_public), đúng phạm vi 2 policy cũ (mục phụ đạo còn mở + bài chẩn đoán
--       đầu vào chưa nộp, kể cả YCCĐ con); admin/GV THPT đọc mọi chủ đề như policy staff.
--   tutoring_exit_quiz_submit(p_need_id, p_question_ids, p_responses, p_window_id) → jsonb
--       chấm ở server từ question_bank (exam_grade_responses), rồi INSERT tutoring_exit_attempts (trigger guard cũ
--       vẫn kiểm cooldown 24h, xem lại lý thuyết, cửa sổ cuối buổi; trigger cũ tự tính pct/passed và gỡ mục).
--       Kiểm: câu thuộc chủ đề của mục (kể cả YCCĐ con), không lưu trữ, không tự luận, không trùng; đủ số câu
--       (20 tự kiểm tra / 10 cuối buổi, hoặc cả kho nếu kho ít hơn). Trả per_question = [is_correct…] (KHÔNG trả đáp án).
--   diagnostic_check_answer(p_bank_id, p_response) → jsonb {bank_id, is_correct}
--       chấm 1 câu chẩn đoán đầu vào (bài thích ứng cần biết đúng/sai từng câu). Chỉ khi em đang được làm chẩn đoán
--       (diagnostic_bank_topic_ids() khác rỗng) và câu thuộc bài của em. LẦN TRẢ LỜI ĐẦU TIÊN được ghi vào
--       entry_diagnostic_checks và trả lại y nguyên ở các lần gọi sau → không dò được đáp án bằng cách thử từng phương án.
-- Bảng mới: entry_diagnostic_checks (RLS bật, không cấp quyền cho anon/authenticated; chỉ hàm definer ghi/đọc).
--   Trigger trên entry_diagnostics: nộp (INSERT) hoặc "Cho làm lại" (diagnostic_reset DELETE) → xoá các lượt chấm của em.
--
-- Bước 2 (20261122110000): bỏ 2 policy SELECT trên question_bank + policy INSERT trực tiếp tutoring_exit_attempts.
-- Chạy bước 2 SAU khi client mới đã deploy và tab cũ đã tải lại (≥1 ngày), ngoài giờ HS làm bài.
--
-- Ai đọc/ghi được gì SAU bước 1 (bước 2 mới thu quyền cũ):
-- | Vai                | question_bank (bảng)              | câu không đáp án (RPC)               | ghi tutoring_exit_attempts      |
-- |--------------------|-----------------------------------|--------------------------------------|---------------------------------|
-- | HS                 | (còn đọc nguyên dòng tới bước 2)  | chủ đề phụ đạo mở + bài chẩn đoán    | RPC chấm server (+ INSERT cũ    |
-- |                    |                                   |                                      |  tới bước 2)                    |
-- | Trợ giảng          | không (như cũ)                    | chỉ chủ đề phụ đạo của chính TA (≈0) | không (guard đòi mục của mình)  |
-- | GV THPT / admin    | đọc/ghi tất cả (policy staff)     | mọi chủ đề                           | không (guard đòi mục của mình)  |
-- | anon               | không                             | không (revoke)                       | không                           |
-- entry_diagnostic_checks: không vai nào đọc/ghi trực tiếp (chỉ diagnostic_check_answer + trigger).
--
-- Nặng không: chỉ tạo hàm + 1 bảng rỗng + 1 trigger → lúc nào cũng được.
-- Kiểm thử sau khi chạy (đổi vai trong giao dịch rồi tự rollback): cuối file, mục "KIỂM THỬ".
-- Rollback: perf/rollback/20261122090000_bank_hs_khong_doc_dap_an_buoc_1.down.sql
-- ============================================================================
begin;

-- ---------- 1. Câu ngân hàng cho HS: đã lược đáp án ----------
create or replace function public.bank_questions_for_student(
  p_topic_ids bigint[],
  p_form text default null,
  p_source_exam_ids bigint[] default null,
  p_limit int default 500)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  v_uid uuid := (select auth.uid());
  v_staff boolean;
  v_allowed bigint[] := '{}';
  v_out jsonb;
begin
  if v_uid is null then raise exception 'Cần đăng nhập' using errcode = '42501'; end if;
  if p_topic_ids is null or cardinality(p_topic_ids) = 0 then return '[]'::jsonb; end if;

  -- Như policy "staff manage question bank": admin, hoặc giảng viên mảng THPT.
  v_staff := exists (select 1 from public.profiles p
                     where p.id = v_uid and (p.role = 'admin' or (p.role = 'instructor' and p.admin_area = 'thpt')));
  if not v_staff then
    -- Như 2 policy cũ: mục phụ đạo còn mở của em + các bài em đang được làm chẩn đoán đầu vào.
    select coalesce(array_agg(distinct x), '{}') into v_allowed
    from (
      select n.topic_id as x from public.tutoring_needs n
      where n.student_id = v_uid and n.status in ('open', 'assigned', 'tutored')
      union
      select unnest(public.diagnostic_bank_topic_ids())
    ) s
    where x is not null;
    if cardinality(v_allowed) = 0 then return '[]'::jsonb; end if;
  end if;

  select coalesce(jsonb_agg(jsonb_build_object(
           'id', b.id, 'topic_id', b.topic_id, 'topic_name', b.topic_name, 'form', b.form, 'qtype', b.qtype,
           'difficulty', b.difficulty, 'source_exam_id', b.source_exam_id, 'source_index', b.source_index,
           'question', public.exam_q_public(b.question))
         order by b.topic_id nulls last, b.source_exam_id, b.source_index, b.id), '[]'::jsonb)
  into v_out
  from (
    select q.* from public.question_bank q
    where q.topic_id = any (p_topic_ids[1:200])
      and not q.archived
      and (coalesce(p_form, '') = '' or q.form = p_form)
      and (p_source_exam_ids is null or cardinality(p_source_exam_ids) = 0 or q.source_exam_id = any (p_source_exam_ids))
      and (v_staff
           or q.topic_id = any (v_allowed)
           or exists (select 1 from public.question_topics t where t.id = q.topic_id and t.parent_id = any (v_allowed)))
    order by q.topic_id nulls last, q.source_exam_id, q.source_index, q.id
    limit least(greatest(coalesce(p_limit, 500), 1), 500)
  ) b;
  return v_out;
end;
$$;
revoke all on function public.bank_questions_for_student(bigint[], text, bigint[], int) from public, anon;
grant execute on function public.bank_questions_for_student(bigint[], text, bigint[], int) to authenticated;

-- ---------- 2. Nộp bài tự kiểm tra / kiểm tra cuối buổi phụ đạo: chấm ở server ----------
create or replace function public.tutoring_exit_quiz_submit(
  p_need_id bigint,
  p_question_ids bigint[],
  p_responses jsonb,
  p_window_id uuid default null)
returns jsonb
language plpgsql volatile security definer set search_path = public
as $$
declare
  v_uid uuid := (select auth.uid());
  v_need public.tutoring_needs%rowtype;
  v_n int;
  v_found int;
  v_pool int;
  v_qs jsonb;
  v_g jsonb;
  v_row public.tutoring_exit_attempts%rowtype;
begin
  if v_uid is null then raise exception 'Cần đăng nhập' using errcode = '42501'; end if;
  select * into v_need from public.tutoring_needs where id = p_need_id;
  if not found or v_need.student_id is distinct from v_uid then
    raise exception 'Không tìm thấy mục cần phụ đạo của em' using errcode = 'P0002';
  end if;

  v_n := coalesce(cardinality(p_question_ids), 0);
  if v_n = 0 or v_n > 60
     or v_n <> (select count(distinct x) from unnest(p_question_ids) as x where x is not null) then
    raise exception 'Danh sách câu hỏi không hợp lệ' using errcode = '22023';
  end if;
  if p_responses is null or jsonb_typeof(p_responses) <> 'array' or jsonb_array_length(p_responses) <> v_n
     or octet_length(p_responses::text) > 262144 then
    raise exception 'Bài làm không hợp lệ' using errcode = '22023';
  end if;

  -- Câu phải thuộc chủ đề của mục (kể cả YCCĐ con), chưa lưu trữ, không phải tự luận. Giữ đúng thứ tự client gửi.
  select coalesce(jsonb_agg(b.question order by u.ord), '[]'::jsonb), count(*)
  into v_qs, v_found
  from unnest(p_question_ids) with ordinality as u (id, ord)
  join public.question_bank b on b.id = u.id
  where not b.archived
    and coalesce(b.qtype, b.question ->> 'type', '') <> 'essay'
    and (b.topic_id = v_need.topic_id
         or exists (select 1 from public.question_topics t where t.id = b.topic_id and t.parent_id = v_need.topic_id));
  if v_found <> v_n then
    raise exception 'Có câu không thuộc chủ đề này' using errcode = '22023';
  end if;

  -- Đủ số câu như client bốc: 20 (tự kiểm tra) / 10 (cuối buổi), hoặc cả kho nếu kho của chủ đề ít hơn.
  select count(*) into v_pool
  from (select 1 from public.question_bank b
        where not b.archived
          and coalesce(b.qtype, b.question ->> 'type', '') <> 'essay'
          and (v_need.form not in ('ly_thuyet', 'bai_tap') or v_need.form is null or b.form = v_need.form)
          and (b.topic_id = v_need.topic_id
               or exists (select 1 from public.question_topics t where t.id = b.topic_id and t.parent_id = v_need.topic_id))
        limit 500) s;
  if v_n < least(case when p_window_id is null then 20 else 10 end, v_pool) then
    raise exception 'Bài làm thiếu câu — em tải lại trang rồi làm lượt mới nhé' using errcode = '22023';
  end if;

  v_g := public.exam_grade_responses(v_qs, p_responses);

  -- Trigger guard (tutoring_exit_attempt_guard) kiểm cooldown/xem lại lý thuyết/cửa sổ và tính pct, passed.
  insert into public.tutoring_exit_attempts (tutoring_need_id, student_id, question_ids, total, correct, window_id)
  values (v_need.id, v_uid, p_question_ids, v_n, (v_g ->> 'correct_count')::int, p_window_id)
  returning * into v_row;

  return jsonb_build_object(
    'id', v_row.id, 'tutoring_need_id', v_row.tutoring_need_id, 'total', v_row.total, 'correct', v_row.correct,
    'pct', v_row.pct, 'passed', v_row.passed, 'created_at', v_row.created_at, 'window_id', v_row.window_id,
    'per_question', (select coalesce(jsonb_agg((x.v ->> 'is_correct')::boolean order by x.i), '[]'::jsonb)
                     from jsonb_array_elements(v_g -> 'per_question') with ordinality as x (v, i)));
end;
$$;
revoke all on function public.tutoring_exit_quiz_submit(bigint, bigint[], jsonb, uuid) from public, anon;
grant execute on function public.tutoring_exit_quiz_submit(bigint, bigint[], jsonb, uuid) to authenticated;

-- ---------- 3. Chẩn đoán đầu vào: chấm từng câu ở server, lần trả lời đầu là lần tính ----------
create table if not exists public.entry_diagnostic_checks (
  student_id uuid not null references public.profiles (id) on delete cascade,
  bank_id bigint not null references public.question_bank (id) on delete cascade,
  is_correct boolean not null,
  created_at timestamptz not null default now(),
  primary key (student_id, bank_id)
);
comment on table public.entry_diagnostic_checks is
  'Lần trả lời ĐẦU của từng câu chẩn đoán đầu vào (diagnostic_check_answer). Xoá khi em nộp hoặc được cho làm lại.';
alter table public.entry_diagnostic_checks enable row level security;
revoke all on public.entry_diagnostic_checks from anon, authenticated;

create or replace function public.diagnostic_check_answer(p_bank_id bigint, p_response jsonb)
returns jsonb
language plpgsql volatile security definer set search_path = public
as $$
declare
  v_uid uuid := (select auth.uid());
  v_allowed bigint[];
  b public.question_bank%rowtype;
  v_prev boolean;
  g record;
  v_ok boolean;
begin
  if v_uid is null then raise exception 'Cần đăng nhập' using errcode = '42501'; end if;
  v_allowed := public.diagnostic_bank_topic_ids();
  if cardinality(v_allowed) = 0 then
    raise exception 'Em không có bài kiểm tra đầu vào đang mở' using errcode = '42501';
  end if;
  select * into b from public.question_bank q
  where q.id = p_bank_id and not q.archived
    and (q.topic_id = any (v_allowed)
         or exists (select 1 from public.question_topics t where t.id = q.topic_id and t.parent_id = any (v_allowed)));
  if not found then raise exception 'Không tìm thấy câu này' using errcode = 'P0002'; end if;
  if p_response is null or p_response = 'null'::jsonb then
    raise exception 'Cần chọn đáp án trước' using errcode = '22023';
  end if;

  select c.is_correct into v_prev from public.entry_diagnostic_checks c
  where c.student_id = v_uid and c.bank_id = b.id;
  if found then return jsonb_build_object('bank_id', b.id, 'is_correct', v_prev); end if;

  select * into g from public.exam_grade_question(b.question, p_response);
  v_ok := g.max_pts > 0 and g.earned = g.max_pts;
  insert into public.entry_diagnostic_checks (student_id, bank_id, is_correct)
  values (v_uid, b.id, v_ok)
  on conflict (student_id, bank_id) do nothing;
  -- Hai lượt gọi cùng lúc: lượt kia đã ghi → trả kết quả đã ghi.
  select c.is_correct into v_ok from public.entry_diagnostic_checks c where c.student_id = v_uid and c.bank_id = b.id;
  return jsonb_build_object('bank_id', b.id, 'is_correct', v_ok);
end;
$$;
revoke all on function public.diagnostic_check_answer(bigint, jsonb) from public, anon;
grant execute on function public.diagnostic_check_answer(bigint, jsonb) to authenticated;

-- Nộp chẩn đoán (INSERT entry_diagnostics) hoặc "Cho làm lại" (diagnostic_reset DELETE) → bỏ các lượt chấm cũ của em.
create or replace function public.trg_entry_diagnostic_checks_clear()
returns trigger
language plpgsql security definer set search_path = public
as $$
begin
  delete from public.entry_diagnostic_checks
  where student_id = case when tg_op = 'DELETE' then old.student_id else new.student_id end;
  return null;
end;
$$;
revoke all on function public.trg_entry_diagnostic_checks_clear() from public, anon, authenticated;
drop trigger if exists trg_entry_diagnostic_checks_clear on public.entry_diagnostics;
create trigger trg_entry_diagnostic_checks_clear after insert or delete on public.entry_diagnostics
  for each row execute function public.trg_entry_diagnostic_checks_clear();

commit;

-- ---------------------------------------------------------------------------
-- KIỂM THỬ sau khi chạy (mỗi khối tự rollback bằng raise; thay <…> bằng id thật):
-- (a) HS có mục phụ đạo mở — nhận câu KHÔNG có đáp án, chỉ chủ đề của em:
--   do $t$ declare r jsonb; begin
--     perform set_config('request.jwt.claims', json_build_object('sub','<uuid HS>','role','authenticated')::text, true);
--     set local role authenticated;
--     r := public.bank_questions_for_student(array[<topic_id của mục phụ đạo>]::bigint[]);
--     raise exception 'KETQUA n=% co_dap_an=%', jsonb_array_length(r),
--       (select count(*) from jsonb_array_elements(r) e where e->'question' ? 'answer' or e->'question' ? 'answers'
--          or e->'question' ? 'explanation' or e->'question'->'statements'->0 ? 'answer');
--   end $t$;                               -- mong đợi: n > 0, co_dap_an = 0
--   (cùng khối với topic_id KHÔNG thuộc mục của em → n = 0)
-- (b) Trợ giảng (role tro_giang, không có mục phụ đạo): như (a) với topic bất kỳ → n = 0.
-- (c) Admin: như (a) với topic bất kỳ → n > 0, co_dap_an = 0 (admin đọc đáp án ở bảng/trang quản trị như cũ).
-- (d) HS nộp bài: gửi 1 câu thay vì 20 → lỗi 'Bài làm thiếu câu'; gửi câu của chủ đề khác → 'Có câu không thuộc chủ đề này'.
-- (e) HS gọi diagnostic_check_answer khi đã nộp chẩn đoán → 'Em không có bài kiểm tra đầu vào đang mở'.
-- (f) anon: select public.bank_questions_for_student(array[1]::bigint[]); → permission denied.
