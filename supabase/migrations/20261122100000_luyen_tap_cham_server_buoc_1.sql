-- ============================================================================
-- Vá bảo mật — practice_sessions.score do máy HS gửi — BƯỚC 1/2: thêm RPC chấm ở server (22/11/2026)
-- Lỗ: HS INSERT thẳng practice_sessions (score, correct_count, question_count) + practice_question_results
-- (earned/max/is_correct) với số tự đặt. score kéo theo RP luyện tập (trg_rank_practice_session → rank_on_result),
-- chuỗi ngày (rank_eval_daily_streak đọc ps.score), mục tiêu tuần, tiến độ chủ đề (trg_rank_progress_practice),
-- và created_at tự đặt (lấp chuỗi ngày đã lỡ).
--
-- Hàm mới (RPC cho authenticated) — CHỈ THÊM, client cũ chạy tiếp như cũ:
--   practice_session_submit(p_client_token, p_lesson_id, p_item_id, p_picks, p_responses, p_duration_seconds,
--                           p_timed_out, p_occurred_at) → jsonb {session_id, score10, correct_count, question_count, dropped}
--     * p_picks: [{exam_id, source_index} | {bank_id}] theo đúng thứ tự câu; p_responses: bài làm cùng thứ tự.
--     * Chấm từng câu bằng CHÍNH check_practice_answer / check_bank_practice_answer (cùng cổng quyền: đề published +
--       mở cho em, đề đánh giá chỉ khi đã mở đáp án, câu ngân hàng không lưu trữ/không lint/không nguồn đề đánh giá…).
--       Câu không qua cổng thì bỏ khỏi phiên (đếm ở 'dropped'); bỏ hết thì từ chối. Câu bỏ trống chấm như trả lời
--       sai (gửi -1 thay null: mọi dạng đều ra 0 điểm, max đúng).
--     * Điểm = Math.round(earned/max*1000)/100 như gradeExam; correct_count = số câu đủ điểm. Không tin số client gửi.
--     * created_at = p_occurred_at kẹp trong [now() − 7 ngày, now()] (hàng đợi mất mạng), null → now().
--     * Idempotent theo client_token: đã có phiên của em → trả lại phiên đó, không ghi thêm.
--     * Ghi practice_sessions + practice_question_results trong cùng giao dịch (trigger RP/sổ tay câu sai chạy như cũ).
--
-- Bước 2 (20261122110500): bỏ 2 policy INSERT trực tiếp của HS trên practice_sessions/practice_question_results.
-- Chạy bước 2 SAU khi client mới deploy ≥1 ngày (hàng đợi offline kiểu cũ đã kịp gửi), ngoài giờ HS làm bài.
--
-- Ai đọc/ghi được gì SAU bước 1 (bước 2 mới thu quyền INSERT cũ):
-- | Vai             | practice_sessions / practice_question_results          | practice_session_submit             |
-- |-----------------|---------------------------------------------------------|-------------------------------------|
-- | HS              | đọc của mình; INSERT thẳng còn được tới bước 2         | ghi phiên của mình, điểm do server  |
-- | Trợ giảng / GV  | đọc HS mình dạy (teaches_student) như cũ                | ghi phiên của CHÍNH mình (không RP: |
-- |                 |                                                         | rank_is_student loại staff)         |
-- | Admin           | như cũ (policy "admin manages …")                       | như trên                            |
-- | Phụ huynh       | đọc của con như cũ                                      | ghi phiên của chính mình (vô hại)   |
-- | anon            | không                                                   | không (revoke)                      |
--
-- Nặng không: chỉ tạo 1 hàm → lúc nào cũng được.
-- Kiểm thử sau khi chạy (đổi vai, tự rollback): cuối file.
-- Rollback: perf/rollback/20261122100000_luyen_tap_cham_server_buoc_1.down.sql
-- ============================================================================
begin;

create or replace function public.practice_session_submit(
  p_client_token uuid,
  p_lesson_id bigint,
  p_item_id bigint,
  p_picks jsonb,
  p_responses jsonb,
  p_duration_seconds int default null,
  p_timed_out boolean default false,
  p_occurred_at timestamptz default null)
returns jsonb
language plpgsql volatile security definer set search_path = public
as $$
declare
  v_uid uuid := (select auth.uid());
  v_id bigint;
  v_owner uuid;
  v_n int;
  v_i int;
  v_pick jsonb;
  v_resp jsonb;
  v_exam bigint;
  v_idx int;
  v_bank bigint;
  v_res jsonb;
  v_q jsonb;
  v_e double precision := 0;
  v_m double precision := 0;
  v_cc int := 0;
  v_kept int := 0;
  v_dropped int := 0;
  v_rows jsonb := '[]'::jsonb;
  v_at timestamptz;
  v_score numeric;
begin
  if v_uid is null then raise exception 'Cần đăng nhập' using errcode = '42501'; end if;
  if p_client_token is null then raise exception 'Thiếu mã phiên (client_token)' using errcode = '22023'; end if;

  -- (1) Idempotent: phiên đã ghi bằng token này → trả lại, không ghi gì.
  select id, student_id into v_id, v_owner from public.practice_sessions where client_token = p_client_token;
  if v_id is not null then
    if v_owner is distinct from v_uid then raise exception 'Mã phiên không thuộc về em' using errcode = '42501'; end if;
    return (select jsonb_build_object('session_id', s.id, 'score10', s.score, 'correct_count', s.correct_count,
                                      'question_count', s.question_count, 'dropped', 0, 'existing', true)
            from public.practice_sessions s where s.id = v_id);
  end if;

  if p_picks is null or jsonb_typeof(p_picks) <> 'array' or p_responses is null or jsonb_typeof(p_responses) <> 'array' then
    raise exception 'Phiên luyện tập không hợp lệ' using errcode = '22023';
  end if;
  v_n := jsonb_array_length(p_picks);
  if v_n = 0 or v_n > 100 or jsonb_array_length(p_responses) <> v_n
     or octet_length(p_responses::text) > 262144 then
    raise exception 'Phiên luyện tập không hợp lệ' using errcode = '22023';
  end if;
  if p_item_id is not null and not exists (
       select 1 from public.lesson_items li where li.id = p_item_id
         and (p_lesson_id is null or li.lesson_id = p_lesson_id)) then
    raise exception 'Không tìm thấy mục bài học này' using errcode = 'P0002';
  end if;

  -- (2) Chấm từng câu qua đúng hàm chấm luyện tập hiện hành (cùng cổng quyền). Trùng câu trong phiên → bỏ bản sau.
  for v_i in 0 .. v_n - 1 loop
    v_pick := p_picks -> v_i;
    v_resp := p_responses -> v_i;
    if v_resp is null or v_resp = 'null'::jsonb then v_resp := '-1'::jsonb; end if;
    v_bank := case when jsonb_typeof(v_pick -> 'bank_id') = 'number' then (v_pick ->> 'bank_id')::bigint end;
    v_exam := case when jsonb_typeof(v_pick -> 'exam_id') = 'number' then (v_pick ->> 'exam_id')::bigint end;
    v_idx  := case when jsonb_typeof(v_pick -> 'source_index') = 'number' then (v_pick ->> 'source_index')::int end;
    v_res := null;
    if (v_bank is not null and exists (select 1 from jsonb_array_elements(v_rows) r where (r ->> 'bank_id')::bigint = v_bank))
       or (v_bank is null and exists (select 1 from jsonb_array_elements(v_rows) r
                                      where (r ->> 'exam_id')::bigint = v_exam and (r ->> 'source_index')::int = v_idx)) then
      v_dropped := v_dropped + 1;
      continue;
    end if;
    begin
      if v_bank is not null then
        v_res := public.check_bank_practice_answer(v_bank, v_resp);
      elsif v_exam is not null and v_exam > 0 and v_idx is not null then
        v_res := public.check_practice_answer(v_exam, v_idx, v_resp);
      end if;
    exception when others then
      v_res := null;
    end;
    if v_res is null then
      v_dropped := v_dropped + 1;
      continue;
    end if;
    v_q := v_res -> 'question';
    v_e := v_e + (v_res ->> 'earned')::double precision;
    v_m := v_m + (v_res ->> 'max')::double precision;
    if (v_res ->> 'is_correct')::boolean then v_cc := v_cc + 1; end if;
    v_rows := v_rows || jsonb_build_array(jsonb_build_object(
      'question_index', v_kept,
      'exam_id', case when v_bank is null then v_exam end,
      'source_index', case when v_bank is null then v_idx else 0 end,
      'bank_id', v_bank,
      'topic_name', public.exam_js_trim(case when jsonb_typeof(v_q -> 'topic') = 'string' then v_q ->> 'topic' else '' end),
      'form', coalesce(v_q ->> 'form', ''),
      'qtype', coalesce(v_q ->> 'type', ''),
      'earned', (v_res ->> 'earned')::numeric,
      'max', (v_res ->> 'max')::numeric,
      'is_correct', (v_res ->> 'is_correct')::boolean,
      'difficulty', coalesce(v_q ->> 'difficulty', '')));
    v_kept := v_kept + 1;
  end loop;

  if v_kept = 0 then
    raise exception 'Không chấm được câu nào trong phiên này' using errcode = '22023';
  end if;

  v_score := case when v_m > 0 then public.exam_js_round(v_e / v_m * 1000) / 100 else 0 end;
  v_at := case when p_occurred_at is null then now()
               else greatest(least(p_occurred_at, now()), now() - interval '7 days') end;

  -- (3) Ghi phiên + kết quả từng câu (cùng giao dịch).
  -- Không dùng ON CONFLICT: chạy được cả khi chỉ mục duy nhất trên client_token chưa có.
  begin
    insert into public.practice_sessions
      (student_id, lesson_id, item_id, question_count, correct_count, score, duration_seconds, timed_out, client_token, created_at)
    values (v_uid, p_lesson_id, p_item_id, v_kept, v_cc, v_score,
            least(greatest(coalesce(p_duration_seconds, 0), 0), 86400), coalesce(p_timed_out, false), p_client_token, v_at)
    returning id into v_id;
  exception when unique_violation then
    v_id := null;
  end;

  if v_id is null then -- hai lượt gửi cùng lúc: lượt kia đã ghi
    select id, student_id into v_id, v_owner from public.practice_sessions where client_token = p_client_token;
    if v_owner is distinct from v_uid then raise exception 'Mã phiên không thuộc về em' using errcode = '42501'; end if;
    return (select jsonb_build_object('session_id', s.id, 'score10', s.score, 'correct_count', s.correct_count,
                                      'question_count', s.question_count, 'dropped', 0, 'existing', true)
            from public.practice_sessions s where s.id = v_id);
  end if;

  insert into public.practice_question_results
    (session_id, question_index, student_id, exam_id, source_index, bank_id, topic_id, topic_name, form, qtype,
     earned, max, is_correct, difficulty, created_at)
  select v_id, (r ->> 'question_index')::int, v_uid, (r ->> 'exam_id')::bigint, (r ->> 'source_index')::int,
         (r ->> 'bank_id')::bigint,
         (select min(t.id) from public.question_topics t where t.name = r ->> 'topic_name' and r ->> 'topic_name' <> ''),
         r ->> 'topic_name', r ->> 'form', r ->> 'qtype',
         (r ->> 'earned')::numeric, (r ->> 'max')::numeric, (r ->> 'is_correct')::boolean, r ->> 'difficulty', v_at
  from jsonb_array_elements(v_rows) as r;

  return jsonb_build_object('session_id', v_id, 'score10', v_score, 'correct_count', v_cc,
                            'question_count', v_kept, 'dropped', v_dropped, 'existing', false);
end;
$$;
revoke all on function public.practice_session_submit(uuid, bigint, bigint, jsonb, jsonb, int, boolean, timestamptz) from public, anon;
grant execute on function public.practice_session_submit(uuid, bigint, bigint, jsonb, jsonb, int, boolean, timestamptz) to authenticated;

commit;

-- ---------------------------------------------------------------------------
-- KIỂM THỬ sau khi chạy (tự rollback; thay <…> bằng id thật của một đề luyện tập em mở được):
--   do $t$ declare r jsonb; begin
--     perform set_config('request.jwt.claims', json_build_object('sub','<uuid HS>','role','authenticated')::text, true);
--     set local role authenticated;
--     r := public.practice_session_submit(gen_random_uuid(), null, null,
--            '[{"exam_id":<đề>,"source_index":0},{"exam_id":<đề>,"source_index":1}]'::jsonb, '[0, 1]'::jsonb, 60, false, null);
--     raise exception 'KETQUA %', r;   -- score10 do server tính (0 / 5 / 10), question_count = 2
--   end $t$;
-- Trợ giảng/GV: cùng khối với sub = uuid TA → ghi được phiên của CHÍNH TA, không đổi gì của HS.
-- Admin: như trên. Đề đánh giá chưa mở đáp án → câu bị bỏ (dropped), toàn bộ → lỗi 'Không chấm được câu nào'.
-- anon: select public.practice_session_submit(gen_random_uuid(), null, null, '[]', '[]'); → permission denied.
