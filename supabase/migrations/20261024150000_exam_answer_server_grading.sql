-- ============================================================================
-- P0 #1 — Chặng 1: chấm điểm phía server + đường đọc đề đã lược đáp án (24/10/2026)
-- Thiết kế: side-session-notes thiet-ke-p0-1.md (kien-truc-du-lieu). Thầy chốt: Q1 RPC check_practice_answer
-- từng câu · Q2 giấu đáp án mọi đề · Q3 mất mạng thì chờ server · Q4 hàng đợi luyện tập cũ ghi estimated (chặng 4)
-- · Q5 trợ giảng chỉ đọc đáp án đề lớp mình + đề đã gửi xem trước · Q6 exams + rank_fix_quiz · Q7 trễ giờ chỉ đánh dấu.
--
-- CHỈ THÊM — không thu quyền cột, không xoá policy (việc của chặng 3). Client hiện tại chạy tiếp như cũ, khác duy nhất:
--   * trigger BEFORE INSERT chấm lại exam_results.score / detail.correctCount và exam_question_results.earned/max/
--     is_correct từ exams.questions (bỏ số client gửi) với HS và trợ giảng → điểm hết giả được ngay;
--     điểm client gửi mà lệch thì giữ ở detail.client_score để tra.
--   * exam_question_results: chặn gắn dòng vào bài làm của người khác / lệch exam_id (trước đây RLS không kiểm).
--
-- Hàm mới (RPC cho authenticated):
--   get_exam_for_taking(p_exam_ids bigint[])               → setof jsonb  đề để làm; HS nhận bản LƯỢC đáp án
--   submit_exam_attempt(p_exam_id, p_client_token, p_responses, p_duration_seconds, p_violations) → jsonb
--                                                           chấm + ghi exam_results/exam_question_results/exam_attempts, idempotent theo client_token
--   get_exam_review(p_exam_ids bigint[])                    → setof jsonb  đề đủ đáp án, chỉ đề em đã nộp (hoặc staff được phép)
--   check_practice_answer(p_exam_id, p_index, p_response)   → jsonb        chấm 1 câu luyện tập "Từng câu" (không phải đề đánh giá)
--   rank_fix_quiz_open(p_exam_result_id, p_topic_id)        → jsonb        như rank_fix_quiz_start nhưng câu đã lược
--   rank_fix_quiz_submit(p_attempt_id, p_responses jsonb)   → jsonb        chấm server (bản p_correct int bỏ ở chặng 3)
--   view exams_staff                                        → đề đủ đáp án cho admin/GV/TA theo exam_staff_can_read
-- Hàm nội bộ (không cấp cho authenticated): exam_js_round, exam_js_trim, exam_translation_tokens, exam_grade_question,
--   exam_grade_responses, exam_q_public, exam_submit_payload, 2 hàm trigger. exam_staff_can_read cấp cho authenticated.
--
-- Chấm = port từng dòng gradeQuestion/gradeExam/translationScore (features/exams/types.ts), tính bằng float8 theo đúng
-- thứ tự phép tính của JS và Math.round (làm tròn nửa lên) → trùng bit với client. Chỗ lệch có chủ ý (đều là ca client
-- cũ văng lỗi/NaN, không lưu được bài): type lạ → 0/0 thay vì NaN; translation.points không phải số → 0,5; answer/answers
-- không phải chuỗi → so dạng text. topic_id khi trùng tên chủ đề: lấy min(id) (client cũ lấy dòng cuối, không xác định).
--
-- Ai đọc/ghi được gì SAU file này (chặng 3 mới thu quyền đọc trực tiếp exams.questions + INSERT trực tiếp):
-- | Vai        | exams.questions                         | đáp án qua RPC/view                              | ghi exam_results / eqr                 |
-- |------------|-----------------------------------------|--------------------------------------------------|----------------------------------------|
-- | HS         | (còn đọc được tới chặng 3)              | lược khi làm; đủ khi đã nộp (get_exam_review);   | INSERT cũ vẫn được nhưng điểm bị chấm  |
-- |            |                                         | 1 câu sau khi trả lời nếu đề không phải đánh giá | lại; hoặc qua submit_exam_attempt      |
-- | Trợ giảng  | (như cũ tới chặng 3)                    | exams_staff/get_exam_review: đề đã gửi xem trước,| như HS (điểm bị chấm lại)              |
-- |            |                                         | đề gán lớp mình trợ giảng (published), đề TA giao|                                        |
-- |            |                                         | BTVN lớp mình, đề HS lớp mình đã nộp             |                                        |
-- | GV         | như cũ                                  | exams_staff: mọi đề published                    | không bị chấm lại (bỏ qua trigger)     |
-- | Admin      | như cũ                                  | exams_staff: mọi đề                              | không bị chấm lại                      |
-- | anon       | không                                   | không (revoke)                                   | không                                  |
--
-- Nặng không: chỉ tạo hàm/view/trigger + 1 cột nullable (rank_fix_attempts.responses) → chạy giờ nào cũng được.
-- Trước khi chạy: so rank_fix_quiz_start/_submit trên prod với docs/supabase-migration-rank-system.sql
--   select pg_get_functiondef('public.rank_fix_quiz_submit(bigint,int)'::regprocedure);
-- (bản mới rank_fix_quiz_submit(bigint, jsonb) chép phần cộng RP từ file đó).
-- Sau khi chạy: npx tsx scripts/doi-chieu-cham-diem-exam.mts 500  (chỉ đọc; TS vs SQL phải lệch 0).
-- Rollback: khối ROLLBACK cuối file.
-- ============================================================================

begin;

-- ---------- 0. Cột lưu bài làm của lượt sửa sai (để chấm server, tra lại khi cần) ----------
alter table public.rank_fix_attempts add column if not exists responses jsonb;

-- ---------- 1. Nền chấm điểm: bắt chước JS ----------
-- Math.round(x) của JS: làm tròn nửa lên (về +∞). Không dùng floor(x + 0.5) vì cộng float có thể làm tròn sai.
create or replace function public.exam_js_round(x double precision)
returns double precision
language sql immutable strict set search_path = public
as $$ select floor(x) + case when x - floor(x) >= 0.5 then 1 else 0 end $$;

-- String.prototype.trim(): cắt cả khoảng trắng Unicode JS coi là \s (NBSP, BOM, U+2000–U+200A…).
create or replace function public.exam_js_trim(t text)
returns text
language sql immutable set search_path = public
as $$
  select regexp_replace(coalesce(t, ''),
    '^[\s   -     　﻿]+|[\s   -     　﻿]+$',
    '', 'g')
$$;

-- translationTokens(): NFD → bỏ dấu (\p{M}) → chữ thường → đ→d → ký tự không phải chữ/số/khoảng trắng thành dấu cách → tách.
create or replace function public.exam_translation_tokens(t text)
returns text[]
language sql immutable set search_path = public
as $$
  select coalesce(array_agg(s.w order by s.ord), '{}'::text[])
  from regexp_split_to_table(
    regexp_replace(
      regexp_replace(
        translate(lower(regexp_replace(normalize(coalesce(t, ''), NFD),
          '[̀-ͯ҃-҉֑-ֽ᪰-᫿᷀-᷿⃐-⃿︠-︯]', '', 'g')),
          'đĐ', 'dd'),
        '[   -     　﻿]', ' ', 'g'),
      '[^[:alnum:][:space:]]', ' ', 'g'),
    '[[:space:]]+') with ordinality as s (w, ord)
  where s.w <> ''
$$;

-- gradeQuestion(): r = SQL NULL nghĩa là responses[i] === undefined (mảng ngắn hơn); 'null'::jsonb là null của JSON.
create or replace function public.exam_grade_question(q jsonb, r jsonb, out earned double precision, out max_pts double precision)
language plpgsql immutable set search_path = public
as $$
declare
  v_correct int;
  v_given text;
  v_want text;
  v_max double precision;
  v_best double precision := 0;
  v_g text[];
  v_r text[];
  v_hit int;
  v_ans jsonb;
begin
  earned := 0;
  max_pts := 0;
  case q ->> 'type'
    when 'multiple_choice' then
      max_pts := 0.25;
      -- r === q.answer (cả hai undefined cũng "bằng" như JS; mảng/object trong JS so tham chiếu nên luôn khác)
      if (r is not distinct from (q -> 'answer'))
         and coalesce(jsonb_typeof(q -> 'answer'), '') not in ('array', 'object') then
        earned := 0.25;
      end if;
    when 'true_false' then
      max_pts := 1;
      if jsonb_typeof(q -> 'statements') = 'array' then
        select count(*) into v_correct
        from jsonb_array_elements(q -> 'statements') with ordinality as s (v, i)
        where (case when jsonb_typeof(r) = 'array' then r -> ((s.i - 1)::int) end) is not distinct from (s.v -> 'answer')
          and coalesce(jsonb_typeof(s.v -> 'answer'), '') not in ('array', 'object');
        earned := case v_correct when 1 then 0.1 when 2 then 0.25 when 3 then 0.5 when 4 then 1 else 0 end;
      end if;
    when 'short_answer' then
      max_pts := 0.25;
      v_given := case when jsonb_typeof(r) = 'string' then r #>> '{}' else '' end;
      v_want := coalesce(q ->> 'answer', '');
      -- .replace(".", ",") chỉ đổi dấu chấm ĐẦU TIÊN → regexp_replace không cờ g
      if v_given <> ''
         and regexp_replace(public.exam_js_trim(v_given), '\.', ',') = regexp_replace(public.exam_js_trim(v_want), '\.', ',') then
        earned := 0.25;
      end if;
    when 'essay' then
      null; -- giáo viên chấm (grade_essay_answer), 0/0
    when 'translation' then
      v_max := case jsonb_typeof(q -> 'points') when 'number' then (q ->> 'points')::double precision else 0.5 end;
      max_pts := v_max;
      v_given := case when jsonb_typeof(r) = 'string' then r #>> '{}' else '' end;
      v_g := public.exam_translation_tokens(v_given);
      if cardinality(v_g) > 0 and jsonb_typeof(q -> 'answers') = 'array' then
        for v_ans in select x from jsonb_array_elements(q -> 'answers') as a (x) loop
          v_r := public.exam_translation_tokens(v_ans #>> '{}');
          continue when cardinality(v_r) = 0;
          select coalesce(sum(least(gg.c, rr.c)), 0)::int into v_hit
          from (select w, count(*) as c from unnest(v_g) as w group by w) gg
          join (select w, count(*) as c from unnest(v_r) as w group by w) rr using (w);
          v_best := greatest(v_best, v_hit::double precision / greatest(cardinality(v_r), cardinality(v_g)));
        end loop;
      end if;
      earned := public.exam_js_round(v_best * v_max * 100) / 100;
    else
      null; -- dạng lạ: JS ra NaN (không lưu được), ở đây 0/0
  end case;
end;
$$;

-- gradeExam() + per_question (buildQuestionResults). Trả {score10, earned, max, correct_count, per_question:[{earned,max,is_correct}]}.
create or replace function public.exam_grade_responses(p_questions jsonb, p_responses jsonb)
returns jsonb
language plpgsql immutable set search_path = public
as $$
declare
  v_e double precision := 0;
  v_m double precision := 0;
  v_cc int := 0;
  v_per jsonb := '[]'::jsonb;
  v_n int;
  g record;
  i int;
begin
  v_n := case when jsonb_typeof(p_questions) = 'array' then jsonb_array_length(p_questions) else 0 end;
  for i in 0 .. v_n - 1 loop
    select * into g from public.exam_grade_question(
      p_questions -> i,
      case when jsonb_typeof(p_responses) = 'array' then p_responses -> i end);
    v_e := v_e + g.earned;
    v_m := v_m + g.max_pts;
    if g.max_pts > 0 and g.earned = g.max_pts then v_cc := v_cc + 1; end if;
    v_per := v_per || jsonb_build_array(jsonb_build_object(
      'earned', g.earned, 'max', g.max_pts, 'is_correct', g.max_pts > 0 and g.earned = g.max_pts));
  end loop;
  return jsonb_build_object(
    'score10', case when v_m > 0 then public.exam_js_round(v_e / v_m * 1000) / 100 else 0 end,
    'earned', v_e, 'max', v_m, 'correct_count', v_cc, 'per_question', v_per);
end;
$$;

-- Câu hỏi đưa cho HS lúc làm bài: DANH SÁCH TRẮNG (thêm khoá mới vào ExamQuestion sẽ không tự lộ).
-- Bỏ: answer, answers, explanation, statements[].answer, suggestedAnswer, gradingGuide, distractorNotes, difficultySource, lint_ignored.
create or replace function public.exam_q_public(q jsonb)
returns jsonb
language sql immutable set search_path = public
as $$
  select case when jsonb_typeof(q) <> 'object' then '{}'::jsonb else jsonb_strip_nulls(jsonb_build_object(
    'type', q -> 'type',
    'question', q -> 'question',
    'options', q -> 'options',
    'statements', case when jsonb_typeof(q -> 'statements') = 'array' then (
      select coalesce(jsonb_agg(jsonb_build_object('text', s.v -> 'text') order by s.i), '[]'::jsonb)
      from jsonb_array_elements(q -> 'statements') with ordinality as s (v, i)) end,
    'points', q -> 'points',
    'topic', q -> 'topic',
    'form', q -> 'form',
    'difficulty', q -> 'difficulty',
    'theorySection', q -> 'theorySection')) end
$$;

-- ---------- 2. Ai được xem ĐÁP ÁN (Q5-b) ----------
create or replace function public.exam_staff_can_read(p_exam_id bigint)
returns boolean
language sql stable security definer set search_path = public
as $$
  select case (select p.role from public.profiles p where p.id = (select auth.uid()))
    when 'admin' then exists (select 1 from public.exams e where e.id = p_exam_id)
    when 'instructor' then exists (select 1 from public.exams e where e.id = p_exam_id and e.published)
    when 'tro_giang' then
         exists (select 1 from public.exam_ta_previews t where t.exam_id = p_exam_id and public.assists_class(t.class_id))
      or exists (select 1 from public.exams e join public.exam_classes ec on ec.exam_id = e.id
                 where e.id = p_exam_id and e.published and public.assists_class(ec.class_id))
      or exists (select 1 from public.ta_homework_assignments h where h.exam_id = p_exam_id and public.assists_class(h.class_id))
      -- đề toàn trường (không gán lớp): chỉ khi đã có HS lớp mình nộp → để chữa bài
      or exists (select 1 from public.exam_results er
                 join public.user_classes uc on uc.user_id = er.student_id and uc.status = 'active'
                 where er.exam_id = p_exam_id and public.assists_class(uc.class_id))
    else false
  end
$$;

-- View cho trang quản trị/trợ giảng (chặng 2 đổi .from("exams").select(...questions...) sang đây).
-- Không cập nhật được qua view (chỉ cấp SELECT); ghi vẫn vào public.exams theo RLS cũ.
drop view if exists public.exams_staff;
create view public.exams_staff with (security_barrier = true) as
  select e.* from public.exams e where public.exam_staff_can_read(e.id);
revoke all on public.exams_staff from public, anon, authenticated;
grant select on public.exams_staff to authenticated;

-- ---------- 3. Đọc đề để làm ----------
create or replace function public.get_exam_for_taking(p_exam_ids bigint[])
returns setof jsonb
language sql stable security definer set search_path = public
as $$
  select jsonb_build_object(
      'id', e.id, 'title', e.title, 'duration_minutes', e.duration_minutes, 'published', e.published,
      'pass_score', e.pass_score, 'question_count', e.question_count, 'cnc_key', e.cnc_key,
      'full', x.full_access,
      'questions', case when x.full_access then coalesce(e.questions, '[]'::jsonb) else (
        select coalesce(jsonb_agg(public.exam_q_public(q.v) order by q.i), '[]'::jsonb)
        from jsonb_array_elements(case when jsonb_typeof(e.questions) = 'array' then e.questions else '[]'::jsonb end)
          with ordinality as q (v, i)) end)
  from public.exams e
  cross join lateral (select public.exam_staff_can_read(e.id) as full_access) x
  where (select auth.uid()) is not null
    and e.id = any (p_exam_ids[1:200])
    and (x.full_access
         or (e.published and (e.cnc_key is not null
                              or public.exam_open_to_student(e.id, (select auth.uid()))
                              or public.is_staff())))
  order by array_position(p_exam_ids, e.id)
$$;

-- ---------- 4. Nộp bài ----------
-- Gói kết quả trả về client (màn Done/Review): đủ đáp án + lời giải, điểm từng câu từ exam_question_results.
create or replace function public.exam_submit_payload(p_result_id bigint)
returns jsonb
language sql stable set search_path = public
as $$
  select jsonb_build_object(
    'result_id', er.id, 'exam_id', er.exam_id, 'score10', er.score, 'duration_seconds', er.duration_seconds,
    'created_at', er.created_at, 'correct_count', (er.detail ->> 'correctCount')::int,
    'responses', er.detail -> 'responses', 'violations', er.violations,
    'earned', coalesce(pq.earned, (g.v ->> 'earned')::numeric),
    'max', coalesce(pq.max, (g.v ->> 'max')::numeric),
    'per_question', coalesce(pq.rows, g.v -> 'per_question'),
    'questions', e.questions)
  from public.exam_results er
  join public.exams e on e.id = er.exam_id
  left join lateral (
    select sum(q.earned) as earned, sum(q.max) as max,
           jsonb_agg(jsonb_build_object('question_index', q.question_index, 'earned', q.earned, 'max', q.max,
                                        'is_correct', q.is_correct, 'manual_earned', q.manual_earned,
                                        'manual_max', q.manual_max) order by q.question_index) as rows
    from public.exam_question_results q where q.exam_result_id = er.id
    having count(*) > 0) pq on true
  cross join lateral (select public.exam_grade_responses(e.questions, er.detail -> 'responses') as v) g
  where er.id = p_result_id
$$;

create or replace function public.submit_exam_attempt(
  p_exam_id bigint,
  p_client_token uuid,
  p_responses jsonb,
  p_duration_seconds int default null,
  p_violations jsonb default '[]'::jsonb)
returns jsonb
language plpgsql volatile security definer set search_path = public
as $$
declare
  v_uid uuid := auth.uid();
  v_exam public.exams%rowtype;
  v_owner uuid;
  v_id bigint;
  v_n int;
  v_resp jsonb;
  v_viol jsonb;
  v_g jsonb;
  v_started timestamptz;
  v_elapsed int;
  v_limit int;
  v_dur int;
begin
  if v_uid is null then raise exception 'Cần đăng nhập' using errcode = '42501'; end if;
  if p_client_token is null then raise exception 'Thiếu mã lượt làm (client_token)' using errcode = '22023'; end if;

  -- (1) Idempotent: đã nộp bằng token này → trả lại kết quả cũ, không ghi gì.
  select id, student_id into v_id, v_owner from public.exam_results where client_token = p_client_token;
  if v_id is not null then
    if v_owner is distinct from v_uid then raise exception 'Mã lượt làm không thuộc về em' using errcode = '42501'; end if;
    return public.exam_submit_payload(v_id);
  end if;

  -- (2) Quyền: như RLS đọc đề hiện hành (published + lớp/CNC), hoặc staff được xem đáp án.
  select * into v_exam from public.exams where id = p_exam_id;
  if not found or not (
       (v_exam.published and (v_exam.cnc_key is not null or public.exam_open_to_student(v_exam.id, v_uid) or public.is_staff()))
       or public.exam_staff_can_read(v_exam.id)) then
    raise exception 'Không tìm thấy đề này' using errcode = 'P0002';
  end if;
  if p_responses is null or jsonb_typeof(p_responses) <> 'array' then
    raise exception 'Bài làm không hợp lệ' using errcode = '22023';
  end if;
  if octet_length(p_responses::text) > 262144 then
    raise exception 'Bài làm quá dài' using errcode = '22023';
  end if;

  v_n := case when jsonb_typeof(v_exam.questions) = 'array' then jsonb_array_length(v_exam.questions) else 0 end;
  v_resp := case when jsonb_array_length(p_responses) <= v_n then p_responses else (
    select coalesce(jsonb_agg(t.x order by t.i), '[]'::jsonb)
    from jsonb_array_elements(p_responses) with ordinality as t (x, i) where t.i <= v_n) end;
  v_viol := case when jsonb_typeof(p_violations) = 'array' then p_violations else '[]'::jsonb end;

  -- (3) Thời gian: tin exam_attempts.started_at nếu có; Q7 — quá giờ + 10 phút chỉ đánh dấu, không từ chối.
  select started_at into v_started from public.exam_attempts
  where client_token = p_client_token and student_id = v_uid order by id desc limit 1;
  v_limit := case when coalesce(v_exam.duration_minutes, 0) > 0 then v_exam.duration_minutes * 60 + 600 end;
  if v_started is not null then v_elapsed := greatest(0, extract(epoch from now() - v_started))::int; end if;
  v_dur := least(greatest(coalesce(p_duration_seconds, v_elapsed, 0), 0), coalesce(v_elapsed, v_limit, 2147483647));
  if v_elapsed is not null and v_limit is not null and v_elapsed > v_limit then
    v_viol := v_viol || jsonb_build_array(jsonb_build_object(
      'type', 'late', 'at', now(), 'away_ms', (v_elapsed - v_limit)::bigint * 1000));
  end if;

  -- (4) Chấm + ghi. Cờ GUC để 2 trigger chấm lại không chấm thêm lần nữa.
  v_g := public.exam_grade_responses(v_exam.questions, v_resp);
  perform set_config('thachlab.server_grading', 'on', true);

  insert into public.exam_results (student_id, exam_id, score, duration_seconds, detail, violation_count, violations, client_token)
  values (v_uid, v_exam.id, (v_g ->> 'score10')::numeric, v_dur,
          jsonb_build_object('responses', v_resp, 'correctCount', (v_g ->> 'correct_count')::int, 'graded_by_server', true),
          jsonb_array_length(v_viol), v_viol, p_client_token)
  on conflict (client_token) do nothing
  returning id into v_id;

  if v_id is null then -- hai lượt nộp cùng lúc: lượt kia đã ghi
    perform set_config('thachlab.server_grading', 'off', true);
    select id, student_id into v_id, v_owner from public.exam_results where client_token = p_client_token;
    if v_owner is distinct from v_uid then raise exception 'Mã lượt làm không thuộc về em' using errcode = '42501'; end if;
    return public.exam_submit_payload(v_id);
  end if;

  insert into public.exam_question_results
    (exam_result_id, question_index, student_id, exam_id, topic_id, topic_name, form, qtype, earned, max, is_correct, difficulty)
  select v_id, (q.i - 1)::int, v_uid, v_exam.id,
         (select min(t.id) from public.question_topics t where t.name = tn.name and tn.name <> ''),
         tn.name, coalesce(q.v ->> 'form', ''), q.v ->> 'type',
         (p.v ->> 'earned')::numeric, (p.v ->> 'max')::numeric, (p.v ->> 'is_correct')::boolean,
         coalesce(q.v ->> 'difficulty', '')
  from jsonb_array_elements(v_exam.questions) with ordinality as q (v, i)
  cross join lateral (select public.exam_js_trim(case when jsonb_typeof(q.v -> 'topic') = 'string' then q.v ->> 'topic' end) as name) tn
  cross join lateral (select v_g -> 'per_question' -> ((q.i - 1)::int) as v) p
  where v_n > 0
  on conflict do nothing;

  perform set_config('thachlab.server_grading', 'off', true);

  update public.exam_attempts
     set submitted_at = now(), exam_result_id = v_id, responses = null, seconds_left = null
   where client_token = p_client_token and student_id = v_uid;

  return public.exam_submit_payload(v_id);
end;
$$;

-- ---------- 5. Xem lại đề đã nộp (đủ đáp án) ----------
create or replace function public.get_exam_review(p_exam_ids bigint[])
returns setof jsonb
language sql stable security definer set search_path = public
as $$
  select jsonb_build_object('id', e.id, 'title', e.title, 'pass_score', e.pass_score,
                            'questions', coalesce(e.questions, '[]'::jsonb))
  from public.exams e
  where (select auth.uid()) is not null
    and e.id = any (p_exam_ids[1:200])
    and (exists (select 1 from public.exam_results er where er.exam_id = e.id and er.student_id = (select auth.uid()))
         or public.exam_staff_can_read(e.id))
  order by array_position(p_exam_ids, e.id)
$$;

-- ---------- 6. Luyện tập "Từng câu" (Q1) ----------
-- Trả đáp án + lời giải + distractorNotes của ĐÚNG 1 câu. Đề đánh giá (kiểm tra/BTVN/định kỳ — exam_is_assessment)
-- chỉ trả khi em đã nộp đề đó, để không moi đáp án đề kiểm tra từng câu một.
create or replace function public.check_practice_answer(p_exam_id bigint, p_index int, p_response jsonb)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  v_uid uuid := auth.uid();
  v_exam public.exams%rowtype;
  v_q jsonb;
  g record;
begin
  if v_uid is null then raise exception 'Cần đăng nhập' using errcode = '42501'; end if;
  select * into v_exam from public.exams where id = p_exam_id;
  if not found then raise exception 'Không tìm thấy đề này' using errcode = 'P0002'; end if;
  if not public.exam_staff_can_read(v_exam.id) then
    if not (v_exam.published and (v_exam.cnc_key is not null or public.exam_open_to_student(v_exam.id, v_uid) or public.is_staff())) then
      raise exception 'Không tìm thấy đề này' using errcode = 'P0002';
    end if;
    if public.exam_is_assessment(v_exam.id)
       and not exists (select 1 from public.exam_results er where er.exam_id = v_exam.id and er.student_id = v_uid) then
      raise exception 'Đề kiểm tra chỉ xem đáp án sau khi nộp bài' using errcode = '42501';
    end if;
  end if;
  if p_response is null or p_response = 'null'::jsonb then
    raise exception 'Cần chọn đáp án trước khi xem đáp án' using errcode = '22023';
  end if;
  if p_index is null or p_index < 0 or jsonb_typeof(v_exam.questions) <> 'array'
     or p_index >= jsonb_array_length(v_exam.questions) then
    raise exception 'Không có câu này' using errcode = '22023';
  end if;
  v_q := v_exam.questions -> p_index;
  select * into g from public.exam_grade_question(v_q, p_response);
  return jsonb_build_object('exam_id', v_exam.id, 'question_index', p_index,
    'earned', g.earned, 'max', g.max_pts, 'is_correct', g.max_pts > 0 and g.earned = g.max_pts,
    'question', v_q);
end;
$$;

-- ---------- 7. Sửa sai nhận RP: chấm server ----------
create or replace function public.rank_fix_quiz_open(p_exam_result_id bigint, p_topic_id bigint)
returns jsonb
language plpgsql volatile security definer set search_path = public
as $$
declare
  v jsonb;
begin
  v := public.rank_fix_quiz_start(p_exam_result_id, p_topic_id);
  return jsonb_set(v, '{questions}', (
    select coalesce(jsonb_agg(public.exam_q_public(x.q) order by x.i), '[]'::jsonb)
    from jsonb_array_elements(coalesce(v -> 'questions', '[]'::jsonb)) with ordinality as x (q, i)));
end;
$$;

-- Bản cộng RP chép từ rank_fix_quiz_submit(bigint, int) (docs/supabase-migration-rank-system.sql), khác ở chỗ
-- số câu đúng do DB chấm từ p_responses (mảng song song với questions của rank_fix_quiz_open).
create or replace function public.rank_fix_quiz_submit(p_attempt_id bigint, p_responses jsonb)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_student uuid := auth.uid();
  a public.rank_fix_attempts%rowtype;
  v_qs jsonb;
  v_g jsonb;
  v_correct int;
  v_pass int;
  v_wrong int;
  v_fixed int;
  v_max int;
  v_delta int;
  v_title text;
begin
  select * into a from public.rank_fix_attempts where id = p_attempt_id and student_id = v_student for update;
  if not found then raise exception 'Không tìm thấy lượt sửa sai'; end if;
  if a.status <> 'open' then raise exception 'Lượt này đã nộp rồi'; end if;
  if p_responses is null or jsonb_typeof(p_responses) <> 'array' or octet_length(p_responses::text) > 65536 then
    raise exception 'Bài làm không hợp lệ' using errcode = '22023';
  end if;

  select coalesce(jsonb_agg(qb.question order by array_position(a.question_ids, qb.id)), '[]'::jsonb) into v_qs
  from public.question_bank qb where qb.id = any (a.question_ids);
  v_g := public.exam_grade_responses(v_qs, p_responses);
  v_correct := least((v_g ->> 'correct_count')::int, a.total);

  v_pass := public.rank_cfg(a.season_id, 'fix_pass_pct', 80)::int;
  update public.rank_fix_attempts
    set correct = v_correct,
        pct = round(v_correct * 100.0 / a.total)::int,
        passed = round(v_correct * 100.0 / a.total)::int >= v_pass,
        responses = p_responses,
        status = 'done', submitted_at = now()
  where id = p_attempt_id
  returning * into a;

  select count(distinct coalesce(t.parent_id, t.id)) into v_wrong
  from public.exam_question_results eqr join public.question_topics t on t.id = eqr.topic_id
  where eqr.exam_result_id = a.exam_result_id and not eqr.is_correct;
  select count(distinct topic_id) into v_fixed from public.rank_fix_attempts
  where exam_result_id = a.exam_result_id and passed;

  v_max := public.rank_cfg(a.season_id, 'fix_max_rp', 10)::int;
  select title into v_title from public.exams where id = a.exam_id;
  v_delta := public.rank_award(a.season_id, v_student, 'fix', 'exam_result:' || a.exam_result_id,
    case when v_wrong = 0 then 0 else round(v_max * v_fixed::numeric / v_wrong)::int end,
    'Sửa sai: ' || coalesce(v_title, '') || ' (' || v_fixed || '/' || v_wrong || ' chủ đề)', a.exam_result_id);
  perform public.rank_refresh_student(a.season_id, v_student);

  return jsonb_build_object('pct', a.pct, 'passed', a.passed, 'rp_delta', v_delta,
    'fixed_topics', v_fixed, 'wrong_topics', v_wrong,
    'correct', v_correct, 'total', a.total,
    'per_question', v_g -> 'per_question', 'questions', v_qs);
end;
$$;

-- ---------- 8. Cầu chuyển tiếp: chấm lại khi client cũ INSERT trực tiếp ----------
-- Bỏ qua: trong submit_exam_attempt (cờ GUC), không đăng nhập (SQL editor/service role/script), admin/GV.
-- HS và trợ giảng: điểm = điểm server. Lưu mảng điểm từng câu vào detail (server_earned/server_max) để trigger
-- exam_question_results không phải đọc lại exams.questions cho từng dòng.
create or replace function public.trg_exam_results_server_grade()
returns trigger
language plpgsql security definer set search_path = public
as $$
declare
  v_role text;
  v_q jsonb;
  v_g jsonb;
  v_resp jsonb;
  v_detail jsonb;
begin
  if coalesce(current_setting('thachlab.server_grading', true), '') = 'on' then return new; end if;
  if (select auth.uid()) is null then return new; end if;
  select role into v_role from public.profiles where id = (select auth.uid());
  if v_role in ('admin', 'instructor') then return new; end if;

  select questions into v_q from public.exams where id = new.exam_id;
  if not found then return new; end if; -- khoá ngoại sẽ báo lỗi

  v_detail := case when jsonb_typeof(new.detail) = 'object' then new.detail else '{}'::jsonb end;
  v_resp := case when jsonb_typeof(v_detail -> 'responses') = 'array' then v_detail -> 'responses' else '[]'::jsonb end;
  v_g := public.exam_grade_responses(coalesce(v_q, '[]'::jsonb), v_resp);

  new.detail := v_detail
    || jsonb_build_object(
         'correctCount', (v_g ->> 'correct_count')::int,
         'graded_by_server', true,
         'server_earned', (select coalesce(jsonb_agg(x -> 'earned' order by i), '[]'::jsonb)
                           from jsonb_array_elements(v_g -> 'per_question') with ordinality as t (x, i)),
         'server_max', (select coalesce(jsonb_agg(x -> 'max' order by i), '[]'::jsonb)
                        from jsonb_array_elements(v_g -> 'per_question') with ordinality as t (x, i)))
    || case when new.score is distinct from (v_g ->> 'score10')::numeric
            then jsonb_build_object('client_score', new.score) else '{}'::jsonb end;
  new.score := (v_g ->> 'score10')::numeric;
  return new;
end;
$$;

drop trigger if exists trg_exam_results_server_grade on public.exam_results;
create trigger trg_exam_results_server_grade
  before insert on public.exam_results
  for each row execute function public.trg_exam_results_server_grade();

create or replace function public.trg_exam_question_results_server_grade()
returns trigger
language plpgsql security definer set search_path = public
as $$
declare
  v_role text;
  v_owner uuid;
  v_exam bigint;
  v_detail jsonb;
  v_q jsonb;
  g record;
begin
  if coalesce(current_setting('thachlab.server_grading', true), '') = 'on' then return new; end if;
  if (select auth.uid()) is null then return new; end if;
  select role into v_role from public.profiles where id = (select auth.uid());
  if v_role in ('admin', 'instructor') then return new; end if;

  select er.student_id, er.exam_id, er.detail into v_owner, v_exam, v_detail
  from public.exam_results er where er.id = new.exam_result_id;
  if not found then return new; end if; -- khoá ngoại sẽ báo lỗi
  if v_owner is distinct from new.student_id or v_exam is distinct from new.exam_id then
    raise exception 'Dòng kết quả từng câu không khớp bài làm' using errcode = '42501';
  end if;

  if jsonb_typeof(v_detail -> 'server_earned') = 'array'
     and new.question_index >= 0 and new.question_index < jsonb_array_length(v_detail -> 'server_earned') then
    new.earned := (v_detail -> 'server_earned' ->> new.question_index)::numeric;
    new.max := (v_detail -> 'server_max' ->> new.question_index)::numeric;
  else
    -- bài nộp trước khi có trigger trên (thử lại muộn) hoặc chỉ số lạ: chấm từ đề
    select e.questions -> new.question_index into v_q from public.exams e where e.id = new.exam_id;
    if v_q is null then
      new.earned := 0; new.max := 0;
    else
      select * into g from public.exam_grade_question(v_q,
        case when jsonb_typeof(v_detail -> 'responses') = 'array' then v_detail -> 'responses' -> new.question_index end);
      new.earned := g.earned; new.max := g.max_pts;
      new.qtype := v_q ->> 'type';
    end if;
  end if;
  new.is_correct := new.max > 0 and new.earned = new.max;
  return new;
end;
$$;

drop trigger if exists trg_exam_question_results_server_grade on public.exam_question_results;
create trigger trg_exam_question_results_server_grade
  before insert on public.exam_question_results
  for each row execute function public.trg_exam_question_results_server_grade();

-- ---------- 9. Quyền ----------
revoke all on function public.exam_js_round(double precision) from public, anon, authenticated;
revoke all on function public.exam_js_trim(text) from public, anon, authenticated;
revoke all on function public.exam_translation_tokens(text) from public, anon, authenticated;
revoke all on function public.exam_grade_question(jsonb, jsonb) from public, anon, authenticated;
revoke all on function public.exam_grade_responses(jsonb, jsonb) from public, anon, authenticated;
revoke all on function public.exam_q_public(jsonb) from public, anon, authenticated;
revoke all on function public.exam_submit_payload(bigint) from public, anon, authenticated;
revoke all on function public.trg_exam_results_server_grade() from public, anon, authenticated;
revoke all on function public.trg_exam_question_results_server_grade() from public, anon, authenticated;

revoke all on function public.exam_staff_can_read(bigint) from public, anon;
revoke all on function public.get_exam_for_taking(bigint[]) from public, anon;
revoke all on function public.submit_exam_attempt(bigint, uuid, jsonb, int, jsonb) from public, anon;
revoke all on function public.get_exam_review(bigint[]) from public, anon;
revoke all on function public.check_practice_answer(bigint, int, jsonb) from public, anon;
revoke all on function public.rank_fix_quiz_open(bigint, bigint) from public, anon;
revoke all on function public.rank_fix_quiz_submit(bigint, jsonb) from public, anon;
grant execute on function public.exam_staff_can_read(bigint) to authenticated;
grant execute on function public.get_exam_for_taking(bigint[]) to authenticated;
grant execute on function public.submit_exam_attempt(bigint, uuid, jsonb, int, jsonb) to authenticated;
grant execute on function public.get_exam_review(bigint[]) to authenticated;
grant execute on function public.check_practice_answer(bigint, int, jsonb) to authenticated;
grant execute on function public.rank_fix_quiz_open(bigint, bigint) to authenticated;
grant execute on function public.rank_fix_quiz_submit(bigint, jsonb) to authenticated;

commit;

-- ============================================================================
-- TRUY VẤN KIỂM (SQL editor hoặc `supabase db query --linked -f`, trong begin … rollback; thay <…>)
-- ============================================================================
-- Giả lập một vai:
--   begin;
--   select set_config('request.jwt.claims', json_build_object('sub','<uuid>','role','authenticated')::text, true);
--   set local role authenticated;
--
-- HỌC SINH (<uuid HS>, <đề lớp em chưa làm>, <đề em đã nộp>):
--   select q ? 'answer' or q ? 'explanation' or q ? 'distractorNotes' as lo_dap_an          -- phải toàn false
--     from get_exam_for_taking(array[<đề chưa làm>]::bigint[]) x, jsonb_array_elements(x -> 'questions') q;
--   select (x -> 'full')::boolean from get_exam_for_taking(array[<đề chưa làm>]::bigint[]) x;  -- false
--   select count(*) from get_exam_review(array[<đề chưa làm>]::bigint[]);                      -- 0
--   select count(*) from get_exam_review(array[<đề em đã nộp>]::bigint[]);                     -- 1
--   select count(*) from exams_staff;                                                          -- 0
--   select check_practice_answer(<đề kiểm tra chưa nộp>, 0, '0'::jsonb);                       -- lỗi 42501
--   insert into exam_results (student_id, exam_id, score, detail)
--     values ('<uuid HS>', <đề chưa làm>, 10, '{"responses":[]}') returning score, detail -> 'client_score';
--                                                       -- score = 0 (chấm lại), client_score = 10
--   select submit_exam_attempt(<đề chưa làm>, '00000000-0000-0000-0000-000000000001', '[0,1,2]'::jsonb, 60) ->> 'score10';
--   select submit_exam_attempt(<đề chưa làm>, '00000000-0000-0000-0000-000000000001', '[]'::jsonb, 60) ->> 'score10';
--                                                       -- lần 2 trả đúng điểm lần 1 (idempotent), không thêm dòng
--   rollback;
--
-- TRỢ GIẢNG (<uuid TA>, <đề đã gửi xem trước>, <đề lớp khác không liên quan>):
--   select exam_staff_can_read(<đề đã gửi xem trước>);                                     -- true
--   select exam_staff_can_read(<đề lớp khác>);                                             -- false
--   select count(*) from exams_staff;                                                      -- chỉ đề lớp mình + xem trước
--   select (x -> 'full')::boolean from get_exam_for_taking(array[<đề lớp khác>]::bigint[]) x; -- false (đề lược)
--   select count(*) from get_exam_review(array[<đề đã gửi xem trước>]::bigint[]);          -- 1
--   rollback;
--
-- ADMIN (<uuid admin>):
--   select count(*) = (select count(*) from exams) from exams_staff;   -- (đọc bằng role authenticated) true
--   select (x -> 'full')::boolean from get_exam_for_taking(array[<id>]::bigint[]) x;       -- true
--   insert into exam_results (student_id, exam_id, score, detail) values ('<uuid admin>', <id>, 7, '{}') returning score; -- 7 (không chấm lại)
--   rollback;
--
-- Không vai (anon) không gọi được:
--   select has_function_privilege('anon', 'public.submit_exam_attempt(bigint,uuid,jsonb,int,jsonb)', 'execute'); -- false
--   select has_table_privilege('anon', 'public.exams_staff', 'select');                                           -- false
--   select has_table_privilege('authenticated', 'public.exams_staff', 'update');                                  -- false
--
-- Đối chiếu điểm cũ (chỉ đọc): npx tsx scripts/doi-chieu-cham-diem-exam.mts 500

-- ============================================================================
-- ROLLBACK (bỏ "-- " đầu dòng rồi chạy)
-- ============================================================================
-- begin;
-- drop trigger if exists trg_exam_question_results_server_grade on public.exam_question_results;
-- drop trigger if exists trg_exam_results_server_grade on public.exam_results;
-- drop function if exists public.trg_exam_question_results_server_grade();
-- drop function if exists public.trg_exam_results_server_grade();
-- drop function if exists public.rank_fix_quiz_submit(bigint, jsonb);
-- drop function if exists public.rank_fix_quiz_open(bigint, bigint);
-- drop function if exists public.check_practice_answer(bigint, int, jsonb);
-- drop function if exists public.get_exam_review(bigint[]);
-- drop function if exists public.submit_exam_attempt(bigint, uuid, jsonb, int, jsonb);
-- drop function if exists public.exam_submit_payload(bigint);
-- drop function if exists public.get_exam_for_taking(bigint[]);
-- drop view if exists public.exams_staff;
-- drop function if exists public.exam_staff_can_read(bigint);
-- drop function if exists public.exam_q_public(jsonb);
-- drop function if exists public.exam_grade_responses(jsonb, jsonb);
-- drop function if exists public.exam_grade_question(jsonb, jsonb);
-- drop function if exists public.exam_translation_tokens(text);
-- drop function if exists public.exam_js_trim(text);
-- drop function if exists public.exam_js_round(double precision);
-- alter table public.rank_fix_attempts drop column if exists responses;
-- commit;
