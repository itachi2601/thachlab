-- ============================================================
-- Kiểm chứng thi thăng hạng thích ứng (rank_gate_*) — chạy SAU migration 20261003100000_rank_gate_adaptive.sql:
--   supabase db query --linked -f docs/supabase-test-rank-gate.sql
-- Toàn bộ nằm trong MỘT giao dịch và ROLLBACK ở cuối: không để lại dữ liệu (mùa test, lượt thi, RP… đều bị huỷ).
-- Lệch chỗ nào -> raise exception 'A…: …' đúng dòng đó; chạy xong không lỗi = đạt.
-- Dùng 1 học sinh THẬT lớp 11/12 làm "chuột bạch" (chỉ trong giao dịch) và ngân hàng câu hỏi thật.
-- ============================================================
begin;

-- Chấm đúng / sai một câu bất kể dạng (dùng cho ép trả lời trong bài test).
create or replace function pg_temp.good_resp(p_qid bigint) returns jsonb language sql as $$
  select case q ->> 'type'
    when 'multiple_choice' then to_jsonb((q ->> 'answer')::int)
    when 'true_false' then (select jsonb_agg(s -> 'answer' order by i) from jsonb_array_elements(q -> 'statements') with ordinality t (s, i))
    else to_jsonb(q ->> 'answer') end
  from (select question as q from public.question_bank where id = p_qid) x;
$$;
create or replace function pg_temp.bad_resp(p_qid bigint) returns jsonb language sql as $$
  select case q ->> 'type'
    when 'multiple_choice' then to_jsonb(-1)
    when 'true_false' then '[null,null,null,null]'::jsonb
    else to_jsonb(''::text) end
  from (select question as q from public.question_bank where id = p_qid) x;
$$;

-- Làm hết một lượt thi theo kiểu 'good' hoặc 'bad'; trả {result, q2_level} (mức của câu thứ 2 để kiểm bậc thang).
create or replace function pg_temp.run_attempt(p_aid bigint, p_qid bigint, p_mode text) returns jsonb language plpgsql as $$
declare
  v_qid bigint := p_qid;
  v_res jsonb;
  v_q2 text;
  v_i int;
begin
  for v_i in 1..60 loop
    v_res := public.rank_gate_answer(p_aid,
      case when p_mode = 'good' then pg_temp.good_resp(v_qid) else pg_temp.bad_resp(v_qid) end, v_qid);
    if v_i = 1 then
      select difficulty into v_q2 from public.question_bank where id = (v_res -> 'next_question' ->> 'qid')::bigint;
    end if;
    exit when (v_res ->> 'done')::boolean;
    v_qid := (v_res -> 'next_question' ->> 'qid')::bigint;
  end loop;
  return jsonb_build_object('result', v_res -> 'result', 'q2_level', v_q2, 'last', v_res);
end; $$;

do $$
declare
  v_student uuid;
  v_class bigint;
  v_season bigint;
  v_att jsonb;
  v_att2 jsonb;
  v_aid bigint;
  v_aid2 bigint;
  v_qid bigint;
  v_run jsonb;
  v_res jsonb;
  v_err text;
  v_n int;
  v_status jsonb;
  v_tier text;
  v_tf bigint;
begin
  select uc.user_id, uc.class_id into v_student, v_class
  from public.user_classes uc
  join public.profiles p on p.id = uc.user_id and p.role = 'student'
  join public.classes c on c.id = uc.class_id
  where uc.status = 'active' and c.name in ('11', '12')
  order by uc.user_id limit 1;
  if v_student is null then raise exception 'A0: không có học sinh lớp 11/12 để thử'; end if;
  perform set_config('request.jwt.claims', json_build_object('sub', v_student, 'role', 'authenticated')::text, true);

  -- ---------- hàm chấm 1 câu ----------
  if not public.rank_grade_question('{"type":"multiple_choice","answer":2}', '2') then raise exception 'A1a: MC đúng bị chấm sai'; end if;
  if public.rank_grade_question('{"type":"multiple_choice","answer":2}', '1') then raise exception 'A1b: MC sai bị chấm đúng'; end if;
  if public.rank_grade_question('{"type":"multiple_choice","answer":2}', '"2"') then raise exception 'A1c: MC nhận chuỗi'; end if;
  if public.rank_grade_question('{"type":"multiple_choice","answer":2}', 'null') then raise exception 'A1d: MC nhận null'; end if;
  if not public.rank_grade_question('{"type":"true_false","statements":[{"answer":true},{"answer":false},{"answer":true},{"answer":false}]}', '[true,false,true,false]') then raise exception 'A1e: ĐS khớp hết bị chấm sai'; end if;
  if public.rank_grade_question('{"type":"true_false","statements":[{"answer":true},{"answer":false},{"answer":true},{"answer":false}]}', '[true,false,true,true]') then raise exception 'A1f: ĐS sai 1 ý vẫn đúng'; end if;
  if public.rank_grade_question('{"type":"true_false","statements":[{"answer":true},{"answer":false},{"answer":true},{"answer":false}]}', '[true,false,true]') then raise exception 'A1g: ĐS thiếu ý vẫn đúng'; end if;
  if not public.rank_grade_question('{"type":"short_answer","answer":"1,5"}', '"1.5"') then raise exception 'A1h: 1.5 phải bằng 1,5'; end if;
  if not public.rank_grade_question('{"type":"short_answer","answer":"-3"}', '" -3 "') then raise exception 'A1i: khoảng trắng'; end if;
  if public.rank_grade_question('{"type":"short_answer","answer":"3"}', '""') then raise exception 'A1j: trả lời rỗng vẫn đúng'; end if;
  if public.rank_grade_question('{"type":"essay"}', '"abc"') then raise exception 'A1k: tự luận không được chấm đúng'; end if;

  -- ---------- câu gửi client không chứa đáp án ----------
  select id into v_tf from public.question_bank where qtype = 'true_false' and not archived limit 1;
  v_att := public.rank_gate_public_question(v_tf, (select question from public.question_bank where id = v_tf));
  if v_att ? 'answer' or v_att ? 'explanation' or v_att ? 'topic' or v_att ? 'difficulty' then raise exception 'A2a: payload lộ khoá %', v_att; end if;
  if exists (select 1 from jsonb_array_elements(v_att -> 'statements') s where s ? 'answer') then raise exception 'A2b: ý đúng–sai lộ answer'; end if;
  if jsonb_array_length(v_att -> 'statements') <> 4 or (v_att ->> 'qid')::bigint <> v_tf then raise exception 'A2c: payload sai dạng %', v_att; end if;

  -- ---------- mùa thử ----------
  update public.rank_seasons set status = 'closed' where status = 'active';
  insert into public.rank_seasons (name, starts_on, ends_on, class_ids, status, config)
  values ('TEST gate', current_date - 1, current_date + 30, array[v_class], 'active',
          '{"gate_quiz_count":12,"gate_cooldown_hours":48}'::jsonb)
  returning id into v_season;
  perform public.rank_seed_tiers(v_season);
  update public.rank_tiers set required_title_count = 0 where season_id = v_season;   -- chỉ thử phần thi, bỏ điều kiện danh hiệu
  perform public.rank_ensure_member(v_season, v_student);
  insert into public.rank_rp_awards (season_id, student_id, source_kind, source_ref, awarded)
  values (v_season, v_student, 'practice', 'test:1', 600);
  perform public.rank_refresh_student(v_season, v_student);
  select tier_code into v_tier from public.rank_student_seasons where season_id = v_season and student_id = v_student;
  if v_tier <> 'chien_binh' then raise exception 'A3a: đủ RP nhưng chưa thi phải đứng ở chien_binh, được %', v_tier; end if;

  -- mặc định ngưỡng
  if (select pct from public.rank_gate_rule(v_season, 'dai_su')) <> 75 or (select hard from public.rank_gate_rule(v_season, 'dai_su')) <> 2
     or (select lvl from public.rank_gate_rule(v_season, 'thach_dau')) <> 'kho' then raise exception 'A3b: ngưỡng mặc định sai'; end if;
  update public.rank_tiers set gate_pass_pct = 90 where season_id = v_season and code = 'dai_su';
  if (select pct from public.rank_gate_rule(v_season, 'dai_su')) <> 90 then raise exception 'A3c: ngưỡng ghi đè không ăn'; end if;
  update public.rank_tiers set gate_pass_pct = null where season_id = v_season and code = 'dai_su';

  -- trạng thái trước khi thi
  v_status := public.rank_status_of(v_student);
  if (v_status #>> '{next,code}') <> 'tinh_anh' or (v_status #>> '{next,gate,adaptive}')::boolean is not true
     or (v_status #>> '{next,gate,can_start}')::boolean is not true then
    raise exception 'A3d: status_of chưa báo được can_start: %', v_status -> 'next';
  end if;

  -- ---------- bắt đầu: không lộ đáp án, đúng 12 câu, mở lại trả đúng lượt ----------
  begin perform public.rank_gate_start('tinh_nhue'); v_err := null; exception when others then v_err := sqlerrm; end;
  if v_err is null or v_err not like '%chưa tới lượt%' then raise exception 'A4a: thi nhảy bậc phải bị chặn, được %', v_err; end if;

  v_att := public.rank_gate_start('tinh_anh');
  v_aid := (v_att ->> 'attempt_id')::bigint;
  v_qid := (v_att #>> '{question,qid}')::bigint;
  if (v_att ->> 'total')::int <> 12 or (v_att ->> 'index')::int <> 0 then raise exception 'A4b: total/index sai %', v_att; end if;
  if v_att -> 'question' ? 'answer' or v_att -> 'question' ? 'explanation' then raise exception 'A4c: câu thi lộ đáp án'; end if;
  if (select difficulty from public.question_bank where id = v_qid) <> 'trung-binh' then raise exception 'A4d: câu đầu phải ở mức trung-binh'; end if;
  v_att2 := public.rank_gate_start('tinh_anh');
  if (v_att2 ->> 'attempt_id')::bigint <> v_aid or (v_att2 #>> '{question,qid}')::bigint <> v_qid then raise exception 'A4e: start lần 2 phải trả lại lượt đang mở'; end if;

  -- bấm trùng: gửi câu cũ sau khi đã chuyển câu -> không chấm
  v_res := public.rank_gate_answer(v_aid, pg_temp.good_resp(v_qid), v_qid);
  v_res := public.rank_gate_answer(v_aid, pg_temp.good_resp(v_qid), v_qid);
  if (v_res ->> 'stale')::boolean is not true or (v_res ->> 'index')::int <> 1 then raise exception 'A4f: câu trả lời trùng phải bị bỏ qua (stale) %', v_res; end if;
  v_qid := (v_res -> 'next_question' ->> 'qid')::bigint;
  if (select difficulty from public.question_bank where id = v_qid) <> 'kho' then raise exception 'A4g: đúng câu đầu -> câu 2 phải mức kho'; end if;

  begin perform public.rank_gate_finish(v_aid); v_err := null; exception when others then v_err := sqlerrm; end;
  if v_err is null or v_err not like '%chưa làm hết%' then raise exception 'A4h: nộp khi chưa làm hết phải bị chặn, được %', v_err; end if;

  -- ---------- đỗ: làm đúng hết ----------
  v_run := pg_temp.run_attempt(v_aid, v_qid, 'good');
  v_res := v_run -> 'result';
  if (v_res ->> 'passed')::boolean is not true or (v_res ->> 'pct')::int <> 100 or v_res ->> 'level_end' <> 'kho' then
    raise exception 'A5a: làm đúng hết phải đỗ 100%% ở mức kho: %', v_res;
  end if;
  if (v_res ->> 'promoted')::boolean is not true or v_res ->> 'tier' <> 'tinh_anh' then raise exception 'A5b: đỗ phải lên tinh_anh ngay: %', v_res; end if;
  select jsonb_array_length(answers) into v_n from public.rank_gate_attempts where id = v_aid;
  if v_n <> 12 or (select count(distinct x) from public.rank_gate_attempts a, unnest(a.question_ids) x where a.id = v_aid) <> 12 then
    raise exception 'A5c: phải đúng 12 câu khác nhau';
  end if;
  if not exists (select 1 from public.rank_gate_passes where season_id = v_season and student_id = v_student and tier_code = 'tinh_anh' and (evidence ->> 'adaptive')::boolean) then
    raise exception 'A5d: thiếu rank_gate_passes có evidence thích ứng';
  end if;
  if (select count(*) from public.practice_question_results where student_id = v_student and created_at > now() - interval '1 minute') > 0 then
    raise exception 'A5e: thi thăng hạng không được ghi practice_question_results';
  end if;
  if (select coalesce(sum(awarded), 0) from public.rank_rp_awards where season_id = v_season and student_id = v_student) <> 600 then
    raise exception 'A5f: thi thăng hạng không được đổi RP';
  end if;
  -- gọi finish lại -> kết quả đã lưu
  if (public.rank_gate_finish(v_aid) ->> 'pct')::int <> 100 then raise exception 'A5g: finish lần 2 phải trả kết quả đã lưu'; end if;
  begin perform public.rank_gate_start('tinh_anh'); v_err := null; exception when others then v_err := sqlerrm; end;
  if v_err is null or v_err not like '%đã vượt%' then raise exception 'A5h: đã vượt rồi mà vẫn start được: %', v_err; end if;

  -- ---------- trượt + cooldown ----------
  delete from public.rank_gate_passes where season_id = v_season and student_id = v_student;
  delete from public.rank_gate_attempts where season_id = v_season and student_id = v_student;
  perform public.rank_refresh_student(v_season, v_student);
  select tier_code into v_tier from public.rank_student_seasons where season_id = v_season and student_id = v_student;
  if v_tier <> 'chien_binh' then raise exception 'A6a: sau khi xoá cửa phải về chien_binh, được %', v_tier; end if;

  v_att := public.rank_gate_start('tinh_anh');
  v_aid := (v_att ->> 'attempt_id')::bigint;
  v_qid := (v_att #>> '{question,qid}')::bigint;
  v_run := pg_temp.run_attempt(v_aid, v_qid, 'bad');
  v_res := v_run -> 'result';
  if v_run ->> 'q2_level' <> 'de' then raise exception 'A6b: sai câu đầu -> câu 2 phải mức de, được %', v_run ->> 'q2_level'; end if;
  if (v_res ->> 'passed')::boolean is not false or (v_res ->> 'pct')::int <> 0 or v_res ->> 'level_end' <> 'de' then raise exception 'A6c: sai hết phải trượt 0%% ở mức de: %', v_res; end if;
  if v_res ->> 'cooldown_until' is null or jsonb_array_length(v_res -> 'weak_topics') < 1 then raise exception 'A6d: trượt phải có cooldown + chủ đề yếu: %', v_res; end if;
  if (v_res ->> 'promoted')::boolean is not false then raise exception 'A6e: trượt không được lên bậc'; end if;
  select tier_code into v_tier from public.rank_student_seasons where season_id = v_season and student_id = v_student;
  if v_tier <> 'chien_binh' then raise exception 'A6f: trượt vẫn phải ở chien_binh, được %', v_tier; end if;

  v_status := public.rank_status_of(v_student);
  if (v_status #>> '{next,gate,attempts}')::int <> 1 or (v_status #>> '{next,gate,can_start}')::boolean is not false
     or v_status #>> '{next,gate,cooldown_until}' is null or (v_status #>> '{next,gate,last_passed}')::boolean is not false then
    raise exception 'A6g: status_of sau khi trượt sai: %', v_status -> 'next';
  end if;
  begin perform public.rank_gate_start('tinh_anh'); v_err := null; exception when others then v_err := sqlerrm; end;
  if v_err is null or v_err not like '%thời gian chờ%' then raise exception 'A6h: trong cooldown phải bị chặn, được %', v_err; end if;

  -- hết cooldown -> thi lại được, lượt mới
  update public.rank_gate_attempts set submitted_at = now() - interval '49 hours' where id = v_aid;
  v_status := public.rank_status_of(v_student);
  if (v_status #>> '{next,gate,can_start}')::boolean is not true then raise exception 'A7a: hết cooldown phải can_start: %', v_status -> 'next'; end if;
  v_att2 := public.rank_gate_start('tinh_anh');
  v_aid2 := (v_att2 ->> 'attempt_id')::bigint;
  if v_aid2 = v_aid then raise exception 'A7b: phải là lượt mới'; end if;
  if exists (select 1 from public.rank_gate_attempts a where a.id = v_aid2 and a.question_ids && (select question_ids from public.rank_gate_attempts where id = v_aid)) then
    raise exception 'A7c: lượt mới không được lặp câu của lượt trước';
  end if;

  -- điều kiện "số câu Khó đúng": đúng 100% nhưng đòi 99 câu khó -> trượt
  update public.rank_tiers set gate_min_hard_correct = 99 where season_id = v_season and code = 'tinh_anh';
  v_run := pg_temp.run_attempt(v_aid2, (v_att2 #>> '{question,qid}')::bigint, 'good');
  v_res := v_run -> 'result';
  if (v_res ->> 'pct')::int <> 100 or (v_res ->> 'passed')::boolean is not false then raise exception 'A7d: thiếu câu khó đúng phải trượt dù 100%%: %', v_res; end if;
  update public.rank_tiers set gate_min_hard_correct = null where season_id = v_season and code = 'tinh_anh';

  -- hết pool: đòi nhiều câu hơn cả ngân hàng
  update public.rank_gate_attempts set submitted_at = now() - interval '49 hours' where id = v_aid2;
  update public.rank_seasons set config = config || '{"gate_quiz_count":100000}'::jsonb where id = v_season;
  begin perform public.rank_gate_start('tinh_anh'); v_err := null; exception when others then v_err := sqlerrm; end;
  if v_err is null or v_err not like '%chưa đủ câu%' then raise exception 'A8a: thiếu câu phải báo ngân hàng chưa đủ, được %', v_err; end if;
  update public.rank_seasons set config = config || '{"gate_quiz_count":12}'::jsonb where id = v_season;

  -- ---------- chế độ đề tĩnh ----------
  update public.rank_seasons set config = config || '{"gate_adaptive":0}'::jsonb where id = v_season;
  begin perform public.rank_gate_start('tinh_anh'); v_err := null; exception when others then v_err := sqlerrm; end;
  if v_err is null or v_err not like '%không có bài thi%' then raise exception 'A9a: mode static phải chặn thi thích ứng, được %', v_err; end if;
  if public.rank_tier_needs_gate((select t from public.rank_tiers t where season_id = v_season and code = 'tinh_anh')) then
    raise exception 'A9b: static + 0 danh hiệu -> tinh_anh không cần cửa';
  end if;
  update public.rank_seasons set config = config - 'gate_adaptive' where id = v_season;
  if not public.rank_tier_needs_gate((select t from public.rank_tiers t where season_id = v_season and code = 'tinh_anh')) then
    raise exception 'A9c: adaptive -> tinh_anh phải cần cửa';
  end if;

  -- ---------- danh sách lượt cho GV + RLS ----------
  v_res := public.rank_gate_attempts_of(v_student);
  if jsonb_array_length(v_res) < 2 or jsonb_array_length(v_res -> 0 -> 'answers') <> 12 or (v_res -> 0 -> 'answers' -> 0) ? 'correct' is not true then
    raise exception 'A10a: rank_gate_attempts_of thiếu dòng/câu: %', v_res;
  end if;
  begin
    set local role authenticated;
    select count(*) into v_n from public.rank_gate_attempts;
    reset role;
    if v_n <> (select count(*) from public.rank_gate_attempts where student_id = v_student) then
      raise exception 'A10b: RLS để lộ lượt thi của HS khác (thấy % dòng)', v_n;
    end if;
  exception when insufficient_privilege then
    reset role;   -- phiên chạy không được đổi role: bỏ qua bước RLS
  end;
end $$;

rollback;
