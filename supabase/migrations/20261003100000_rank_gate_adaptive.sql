-- ============================================================================
-- Thi thăng hạng thích ứng (3/10/2026) — việc A của docs/BAN-GIAO-RANK-THI-THANG-HANG-2026-10-03.md
--
-- RP đo nỗ lực (giữ dễ); LÊN BẬC phải qua một bài thi bốc từ ngân hàng câu hỏi, độ khó đi theo bậc thang:
-- bắt đầu Trung bình, đúng -> lên 1 mức (tối đa Khó), sai -> xuống 1 mức (tối thiểu Dễ). Server chọn câu kế
-- tiếp và chấm; client không thấy đáp án/lời giải và không được chọn câu.
--
-- 1. rank_tiers thêm 3 cột ngưỡng (null = mặc định theo mã bậc): gate_pass_pct, gate_min_hard_correct,
--    gate_min_level_held. Mặc định: tinh_anh 70/0/de · tinh_nhue 70/0/trung-binh · dai_su 75/2/trung-binh ·
--    cao_thu 80/3/trung-binh · thach_dau 80/4/kho. (chien_binh không thi.)
-- 2. Bảng rank_gate_attempts (mỗi lượt thi) — HS đọc dòng của mình, staff đọc hết, ghi chỉ qua RPC.
-- 3. RPC: rank_gate_start, rank_gate_answer, rank_gate_finish, rank_gate_attempts_of.
--    Hàm phụ: rank_gate_mode, rank_gate_rule, rank_gate_grade, rank_gate_pool_ids, rank_gate_pool_size,
--    rank_gate_pick, rank_gate_public_question, rank_gate_current_payload, rank_grade_question.
-- 4. Định nghĩa lại: rank_tier_needs_gate (IMMUTABLE -> STABLE, thêm "bậc cần thi thích ứng"),
--    rank_eval_gates (bản docs/supabase-migration-rank-system.sql, nhánh thích ứng), rank_status_of
--    (bản 20260930130000, thêm khoá next.gate.adaptive/attempts/last_passed/cooldown_until/can_start/...;
--    khoá cũ giữ nguyên, client cũ bỏ qua khoá lạ).
--
-- Config mùa (rank_seasons.config, đọc qua rank_cfg): gate_quiz_count (12), gate_cooldown_hours (48),
--   gate_adaptive (1 = thích ứng, 0 = đề tĩnh) — hoặc chuỗi gate_mode = 'adaptive' | 'static' ghi tay bằng SQL.
--   Bậc có challenge_exam_id KHÁC null luôn dùng đề tĩnh cũ.
--
-- Đỗ KHÔNG cộng RP, KHÔNG ghi practice_question_results (không lệch mastery/danh hiệu). Trượt: không trừ gì,
-- chờ gate_cooldown_hours rồi thi lại. Điều kiện danh hiệu (required_title_*) giữ nguyên và CỘNG THÊM điều kiện thi.
-- Điều kiện thích ứng cũ chưa từng có nên KHÔNG đụng tới rank_gate_passes đã có (HS đã qua cửa bằng danh hiệu
-- vẫn giữ — xem khối tuỳ chọn ở cuối file nếu muốn bắt thi lại).
--
-- Cách chạy: bash scripts/run-migrations.sh — nên chạy NGOÀI giờ học sinh làm bài (create or replace
-- rank_status_of/rank_eval_gates và alter table rank_tiers cần khoá ngắn).
-- Rollback: perf/rollback/20261003100000_rank_gate_adaptive.down.sql
-- ============================================================================

-- ---------- 1. Cột ngưỡng ----------
alter table public.rank_tiers
  add column if not exists gate_pass_pct int check (gate_pass_pct between 0 and 100),
  add column if not exists gate_min_hard_correct int check (gate_min_hard_correct >= 0),
  add column if not exists gate_min_level_held text check (gate_min_level_held in ('de', 'trung-binh', 'kho'));

-- ---------- 2. Bảng lượt thi ----------
create table if not exists public.rank_gate_attempts (
  id bigint generated always as identity primary key,
  season_id bigint not null references public.rank_seasons (id) on delete cascade,
  student_id uuid not null references public.profiles (id) on delete cascade,
  tier_code text not null,
  status text not null default 'open' check (status in ('open', 'done')),
  -- Khi đang mở: question_ids dài hơn answers đúng 1 phần tử (phần tử cuối = câu đang chờ trả lời).
  question_ids bigint[] not null default '{}',
  answers jsonb not null default '[]'::jsonb,      -- [{qid, level, correct}]
  pool_ids bigint[] not null default '{}',         -- câu đủ điều kiện, chốt lúc bắt đầu (đã loại câu em từng gặp)
  level_cur text not null default 'trung-binh' check (level_cur in ('de', 'trung-binh', 'kho')),
  correct int not null default 0,
  total int not null,
  hard_correct int not null default 0,
  pct int,
  passed boolean,
  level_end text,
  created_at timestamptz not null default now(),
  submitted_at timestamptz
);
create unique index if not exists rank_gate_attempts_one_open
  on public.rank_gate_attempts (season_id, student_id, tier_code) where status = 'open';
create index if not exists rank_gate_attempts_student_idx
  on public.rank_gate_attempts (student_id, season_id, tier_code, created_at desc);

alter table public.rank_gate_attempts enable row level security;
drop policy if exists "read own rank_gate_attempts" on public.rank_gate_attempts;
create policy "read own rank_gate_attempts" on public.rank_gate_attempts
  for select to authenticated
  using (student_id = (select auth.uid()) or public.rank_is_staff());
-- Không có policy ghi: HS không insert/update/delete trực tiếp; mọi ghi đi qua RPC security definer bên dưới.

-- ---------- 3. Hàm phụ ----------
create or replace function public.rank_gate_lvl(p text)
returns int language sql immutable set search_path = public
as $$ select case p when 'de' then 1 when 'trung-binh' then 2 when 'kho' then 3 else 0 end; $$;

create or replace function public.rank_gate_lvl_name(p int)
returns text language sql immutable set search_path = public
as $$ select case greatest(1, least(3, p)) when 1 then 'de' when 2 then 'trung-binh' else 'kho' end; $$;

-- Bậc nào có bài thi thích ứng (chien_binh không thi).
create or replace function public.rank_gate_adaptive_code(p_code text)
returns boolean language sql immutable set search_path = public
as $$ select p_code in ('tinh_anh', 'tinh_nhue', 'dai_su', 'cao_thu', 'thach_dau'); $$;

-- 'adaptive' (mặc định) hay 'static' (chỉ đề thử thách tĩnh như trước).
create or replace function public.rank_gate_mode(p_season bigint)
returns text language sql stable set search_path = public
as $$
  select case
           when coalesce(s.config ->> 'gate_mode', '') in ('static', '0') then 'static'
           when coalesce(s.config ->> 'gate_adaptive', '1') in ('0', 'false') then 'static'
           else 'adaptive'
         end
  from public.rank_seasons s where s.id = p_season;
$$;

-- Ngưỡng qua bài của một bậc: cột trong rank_tiers, null thì dùng mặc định theo mã bậc.
create or replace function public.rank_gate_rule(p_season bigint, p_code text)
returns table (pct int, hard int, lvl text)
language sql stable set search_path = public
as $$
  select coalesce(t.gate_pass_pct, d.pct, 70),
         coalesce(t.gate_min_hard_correct, d.hard, 0),
         coalesce(t.gate_min_level_held, d.lvl, 'de')
  from public.rank_tiers t
  left join (values
    ('tinh_anh', 70, 0, 'de'),
    ('tinh_nhue', 70, 0, 'trung-binh'),
    ('dai_su', 75, 2, 'trung-binh'),
    ('cao_thu', 80, 3, 'trung-binh'),
    ('thach_dau', 80, 4, 'kho')
  ) as d (code, pct, hard, lvl) on d.code = t.code
  where t.season_id = p_season and t.code = p_code;
$$;

-- Khối lớp (10/11/12) của học sinh trong mùa: lớp THPT đang học thuộc mùa, lấy khối cao nhất.
create or replace function public.rank_gate_grade(p_season bigint, p_student uuid)
returns text language sql stable set search_path = public
as $$
  select c.name
  from public.user_classes uc
  join public.classes c on c.id = uc.class_id
  join public.rank_seasons s on s.id = p_season
  where uc.user_id = p_student and uc.status = 'active'
    and c.name in ('10', '11', '12')
    and (cardinality(s.class_ids) = 0 or uc.class_id = any (s.class_ids))
  order by c.name::int desc
  limit 1;
$$;

-- Số câu đủ điều kiện của khối (chưa loại câu em đã gặp) — để biết có mở được bài thi không.
create or replace function public.rank_gate_pool_size(p_season bigint, p_grade text)
returns int language sql stable set search_path = public
as $$
  select count(*)::int
  from public.question_bank qb
  join public.question_topics t on t.id = qb.topic_id
  where not qb.archived and qb.qtype <> 'essay' and qb.difficulty in ('de', 'trung-binh', 'kho')
    and qb.grade = p_grade
    and (qb.topic_id in (select rtt.topic_id from public.rank_title_topics rtt
                         join public.rank_titles rt on rt.code = rtt.title_code and rt.kind = 'specialist' and rt.enabled)
         or t.parent_id in (select rtt.topic_id from public.rank_title_topics rtt
                            join public.rank_titles rt on rt.code = rtt.title_code and rt.kind = 'specialist' and rt.enabled));
$$;

-- Các câu bốc được cho một lượt thi: chủ đề của mọi danh hiệu chuyên môn, đúng khối lớp, không phải tự luận,
-- đã gắn mức độ, và em CHƯA từng gặp (content_hash không có trong bài làm/luyện tập của em, không nằm trong
-- các lượt thi trước). Cùng cách rank_fix_quiz_start dùng question_content_hash.
create or replace function public.rank_gate_pool_ids(p_season bigint, p_student uuid, p_grade text)
returns bigint[] language sql stable set search_path = public
as $$
  with seen as (
    select public.question_content_hash(e.questions -> r.idx) as h
    from (
      select exam_id, question_index as idx from public.exam_question_results where student_id = p_student
      union
      select exam_id, source_index from public.practice_question_results where student_id = p_student and source_index is not null
    ) r
    join public.exams e on e.id = r.exam_id
    where jsonb_typeof(e.questions) = 'array' and (e.questions -> r.idx) is not null
  ),
  prev as (
    select distinct unnest(question_ids) as qid from public.rank_gate_attempts where student_id = p_student
  )
  select coalesce(array_agg(qb.id), '{}'::bigint[])
  from public.question_bank qb
  join public.question_topics t on t.id = qb.topic_id
  where not qb.archived and qb.qtype <> 'essay' and qb.difficulty in ('de', 'trung-binh', 'kho')
    and qb.grade = p_grade
    and (qb.topic_id in (select rtt.topic_id from public.rank_title_topics rtt
                         join public.rank_titles rt on rt.code = rtt.title_code and rt.kind = 'specialist' and rt.enabled)
         or t.parent_id in (select rtt.topic_id from public.rank_title_topics rtt
                            join public.rank_titles rt on rt.code = rtt.title_code and rt.kind = 'specialist' and rt.enabled))
    and qb.content_hash not in (select h from seen)
    and qb.id not in (select qid from prev);
$$;

-- Bốc 1 câu trong pool chưa dùng: ưu tiên đúng mức, hết thì lấy mức kề (gần nhất), cùng khoảng cách thì ngẫu nhiên.
create or replace function public.rank_gate_pick(p_pool bigint[], p_used bigint[], p_level text)
returns bigint language sql set search_path = public
as $$
  select qb.id
  from public.question_bank qb
  where qb.id = any (p_pool) and not (qb.id = any (p_used)) and not qb.archived
  order by abs(public.rank_gate_lvl(qb.difficulty) - public.rank_gate_lvl(p_level)), random()
  limit 1;
$$;

-- Câu hỏi gửi cho client: bỏ đáp án, lời giải, ghi chú phương án nhiễu, nhãn chủ đề/dạng/mức (client không được
-- thấy mức để đoán), đúng–sai chỉ còn phần chữ của từng ý.
create or replace function public.rank_gate_public_question(p_id bigint, q jsonb)
returns jsonb language sql immutable set search_path = public
as $$
  select jsonb_build_object('qid', p_id)
    || (q - 'answer' - 'explanation' - 'distractorNotes' - 'suggestedAnswer' - 'gradingGuide' - 'topic' - 'form'
          - 'difficulty' - 'difficultySource' - 'theorySection' - 'bank_id' - 'statements')
    || case when jsonb_typeof(q -> 'statements') = 'array' then
         jsonb_build_object('statements', (
           select coalesce(jsonb_agg(jsonb_build_object('text', s.v ->> 'text') order by s.i), '[]'::jsonb)
           from jsonb_array_elements(q -> 'statements') with ordinality as s (v, i)))
       else '{}'::jsonb end;
$$;

-- Chấm 1 câu phía DB, cùng luật gradeQuestion (features/exams/types.ts):
--  options -> chỉ số đáp án (số); statements -> đúng–sai phải khớp CẢ các ý; answer text -> so sau khi cắt khoảng
--  trắng và đổi dấu chấm đầu tiên thành dấu phẩy. Dạng khác (tự luận) luôn sai — đã loại khỏi pool.
create or replace function public.rank_grade_question(q jsonb, r jsonb)
returns boolean language plpgsql immutable set search_path = public
as $$
declare
  v_given text;
  v_want text;
begin
  if r is null or jsonb_typeof(r) = 'null' then return false; end if;
  case q ->> 'type'
    when 'multiple_choice' then
      if jsonb_typeof(r) <> 'number' then return false; end if;
      return (r #>> '{}')::numeric = (q ->> 'answer')::numeric;
    when 'true_false' then
      if jsonb_typeof(r) <> 'array' or jsonb_typeof(q -> 'statements') <> 'array' then return false; end if;
      if jsonb_array_length(r) <> jsonb_array_length(q -> 'statements') then return false; end if;
      return not exists (
        select 1 from jsonb_array_elements(q -> 'statements') with ordinality as s (v, i)
        where (r -> (s.i - 1)::int) is distinct from (s.v -> 'answer'));
    when 'short_answer' then
      if jsonb_typeof(r) <> 'string' then return false; end if;
      v_given := regexp_replace(btrim(r #>> '{}'), '\.', ',');
      v_want := regexp_replace(btrim(coalesce(q ->> 'answer', '')), '\.', ',');
      return v_given <> '' and v_given = v_want;
    else
      return false;
  end case;
end; $$;

-- Payload của câu đang chờ trả lời (không có đáp án).
create or replace function public.rank_gate_current_payload(a public.rank_gate_attempts)
returns jsonb language plpgsql stable set search_path = public
as $$
declare
  v_qid bigint := a.question_ids[cardinality(a.question_ids)];
  v_q jsonb;
  v_rule record;
begin
  select question into v_q from public.question_bank where id = v_qid;
  select * into v_rule from public.rank_gate_rule(a.season_id, a.tier_code);
  return jsonb_build_object(
    'attempt_id', a.id,
    'tier_code', a.tier_code,
    'total', a.total,
    'index', jsonb_array_length(a.answers),
    'pass_pct', v_rule.pct,
    'question', public.rank_gate_public_question(v_qid, coalesce(v_q, '{}'::jsonb))
  );
end; $$;

-- Bậc cần cửa: điều kiện cũ (danh hiệu / đề thử thách / Cao Thủ–Thách Đấu) HOẶC bậc thi thích ứng
-- (mùa ở chế độ adaptive và bậc chưa gán đề tĩnh).
create or replace function public.rank_tier_needs_gate(t public.rank_tiers)
returns boolean language sql stable set search_path = public
as $$
  select t.required_title_count > 0 or t.challenge_exam_id is not null or t.code in ('cao_thu', 'thach_dau')
      or (t.challenge_exam_id is null and public.rank_gate_adaptive_code(t.code)
          and public.rank_gate_mode(t.season_id) = 'adaptive');
$$;

-- ---------- Điều kiện lên hạng: thêm nhánh thích ứng ----------
create or replace function public.rank_eval_gates(p_season bigint, p_student uuid)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  t public.rank_tiers%rowtype;
  s public.rank_seasons%rowtype;
  a public.rank_gate_attempts%rowtype;
  v_titles int;
  v_pct int;
  v_titles_ok boolean;
  v_chal_ok boolean;
  v_evidence jsonb;
begin
  select * into s from public.rank_seasons where id = p_season;
  for t in select * from public.rank_tiers where season_id = p_season order by sort loop
    if not public.rank_tier_needs_gate(t) then continue; end if;
    if exists (select 1 from public.rank_gate_passes g where g.season_id = p_season and g.student_id = p_student and g.tier_code = t.code) then
      continue;
    end if;

    v_titles := public.rank_titles_at_level(p_student, coalesce(t.required_title_level, 'thuc_tinh'));
    v_titles_ok := v_titles >= t.required_title_count;
    v_evidence := '{}'::jsonb;
    v_pct := null;

    if t.challenge_exam_id is not null then
      -- Đề thử thách tĩnh (cơ chế cũ).
      v_pct := public.rank_best_pct(p_student, t.challenge_exam_id,
        (s.starts_on::timestamp) at time zone 'Asia/Ho_Chi_Minh',
        ((s.ends_on + 1)::timestamp) at time zone 'Asia/Ho_Chi_Minh');
      v_chal_ok := v_pct is not null and v_pct >= round(coalesce(t.challenge_pass_score, 8) * 10);
    elsif public.rank_gate_adaptive_code(t.code) and public.rank_gate_mode(p_season) = 'adaptive' then
      -- Bài thi thăng hạng thích ứng: có một lượt đã đỗ trong mùa.
      select * into a from public.rank_gate_attempts g
      where g.season_id = p_season and g.student_id = p_student and g.tier_code = t.code and g.passed
      order by g.submitted_at desc limit 1;
      v_chal_ok := found;
      if found then
        v_evidence := jsonb_build_object('adaptive', true, 'attempt_id', a.id, 'pct', a.pct,
                                         'hard_correct', a.hard_correct, 'level_end', a.level_end);
      end if;
    else
      -- Cao Thủ / Thách Đấu ở chế độ đề tĩnh bắt buộc có thử thách; chưa gán -> chưa thể vượt.
      v_chal_ok := t.code not in ('cao_thu', 'thach_dau');
    end if;

    if v_titles_ok and v_chal_ok then
      insert into public.rank_gate_passes (season_id, student_id, tier_code, evidence)
      values (p_season, p_student, t.code, jsonb_build_object('titles', v_titles, 'challenge_pct', v_pct) || v_evidence)
      on conflict do nothing;
    end if;
  end loop;
end; $$;

-- ---------- 4. RPC thi thăng hạng ----------

-- Bắt đầu (hoặc tiếp tục lượt đang mở). Trả {attempt_id, tier_code, total, index, pass_pct, question}.
create or replace function public.rank_gate_start(p_tier_code text)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_student uuid := auth.uid();
  v_season bigint;
  t public.rank_tiers%rowtype;
  m public.rank_student_seasons%rowtype;
  v_cur_sort int;
  a public.rank_gate_attempts%rowtype;
  v_total int;
  v_hours int;
  v_last_fail timestamptz;
  v_grade text;
  v_pool bigint[];
  v_first bigint;
begin
  if v_student is null then raise exception 'Cần đăng nhập'; end if;
  if not public.rank_is_student(v_student) then raise exception 'Chỉ học sinh mới thi thăng hạng'; end if;

  v_season := public.rank_season_for_at(v_student, now());
  if v_season is null then raise exception 'Hiện chưa có mùa xếp hạng nào đang mở cho lớp em'; end if;

  select * into t from public.rank_tiers where season_id = v_season and code = p_tier_code;
  if not found or t.challenge_exam_id is not null
     or not public.rank_gate_adaptive_code(t.code) or public.rank_gate_mode(v_season) <> 'adaptive' then
    raise exception 'Bậc này không có bài thi thăng hạng thích ứng';
  end if;

  perform public.rank_ensure_member(v_season, v_student);
  select * into m from public.rank_student_seasons where season_id = v_season and student_id = v_student;
  select sort into v_cur_sort from public.rank_tiers where season_id = v_season and code = m.tier_code;
  if exists (select 1 from public.rank_gate_passes g where g.season_id = v_season and g.student_id = v_student and g.tier_code = t.code) then
    raise exception 'Em đã vượt điều kiện lên bậc này rồi';
  end if;
  if t.sort <> coalesce(v_cur_sort, 1) + 1 then raise exception 'Em chưa tới lượt thi bậc này'; end if;
  if m.rp < t.min_rp then raise exception 'Em chưa đủ RP để thi (cần % RP)', t.min_rp; end if;

  -- Lượt đang mở -> trả lại đúng câu đang chờ, không bốc bộ mới.
  select * into a from public.rank_gate_attempts
  where season_id = v_season and student_id = v_student and tier_code = t.code and status = 'open';
  if found then return public.rank_gate_current_payload(a); end if;

  if exists (select 1 from public.rank_gate_attempts g
             where g.season_id = v_season and g.student_id = v_student and g.tier_code = t.code and g.passed) then
    raise exception 'Em đã đạt bài thi này — còn thiếu điều kiện danh hiệu để lên bậc';
  end if;

  v_hours := public.rank_cfg(v_season, 'gate_cooldown_hours', 48)::int;
  select max(g.submitted_at) into v_last_fail from public.rank_gate_attempts g
  where g.season_id = v_season and g.student_id = v_student and g.tier_code = t.code
    and g.status = 'done' and not coalesce(g.passed, false);
  if v_last_fail is not null and v_last_fail + make_interval(hours => v_hours) > now() then
    raise exception 'Chưa hết thời gian chờ — em thi lại được sau % (giờ VN)',
      to_char((v_last_fail + make_interval(hours => v_hours)) at time zone 'Asia/Ho_Chi_Minh', 'HH24:MI "ngày" DD/MM');
  end if;

  v_total := greatest(3, public.rank_cfg(v_season, 'gate_quiz_count', 12)::int);
  v_grade := public.rank_gate_grade(v_season, v_student);
  if v_grade is null then raise exception 'Chưa xác định được khối lớp của em'; end if;
  v_pool := public.rank_gate_pool_ids(v_season, v_student, v_grade);
  if cardinality(v_pool) < v_total then
    raise exception 'Ngân hàng chưa đủ câu mới cho khối % (có %, cần ít nhất %) — nhờ thầy cô bổ sung', v_grade, cardinality(v_pool), v_total;
  end if;

  v_first := public.rank_gate_pick(v_pool, '{}'::bigint[], 'trung-binh');
  begin
    insert into public.rank_gate_attempts (season_id, student_id, tier_code, question_ids, pool_ids, level_cur, total)
    values (v_season, v_student, t.code, array[v_first], v_pool, 'trung-binh', v_total)
    returning * into a;
  exception when unique_violation then
    -- Hai tab cùng bấm: lấy lượt vừa được tạo.
    select * into a from public.rank_gate_attempts
    where season_id = v_season and student_id = v_student and tier_code = t.code and status = 'open';
  end;
  return public.rank_gate_current_payload(a);
end; $$;

-- Trả lời câu hiện tại. Server chấm, đổi mức theo bậc thang, bốc câu kế. p_question_id (tuỳ chọn) chống bấm trùng:
-- nếu khác câu đang chờ thì không chấm gì cả, chỉ trả lại trạng thái hiện tại (stale = true).
-- Trả {correct, done, index, next_question | result}. Câu cuối -> tự gọi rank_gate_finish, trả thêm result.
create or replace function public.rank_gate_answer(p_attempt_id bigint, p_response jsonb, p_question_id bigint default null)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_student uuid := auth.uid();
  a public.rank_gate_attempts%rowtype;
  v_qid bigint;
  v_q jsonb;
  v_level text;
  v_ok boolean;
  v_new_level int;
  v_next bigint;
  v_n int;
  v_result jsonb;
begin
  select * into a from public.rank_gate_attempts where id = p_attempt_id and student_id = v_student for update;
  if not found then raise exception 'Không tìm thấy lượt thi của em'; end if;
  if a.status <> 'open' then raise exception 'Lượt thi này đã nộp rồi'; end if;

  v_n := jsonb_array_length(a.answers);
  if cardinality(a.question_ids) <> v_n + 1 then raise exception 'Lượt thi không hợp lệ'; end if;
  v_qid := a.question_ids[cardinality(a.question_ids)];

  if p_question_id is not null and p_question_id <> v_qid then
    return jsonb_build_object('stale', true, 'done', false, 'index', v_n,
      'next_question', public.rank_gate_current_payload(a) -> 'question');
  end if;

  select question, difficulty into v_q, v_level from public.question_bank where id = v_qid;
  v_ok := public.rank_grade_question(coalesce(v_q, '{}'::jsonb), p_response);

  v_n := v_n + 1;
  v_new_level := public.rank_gate_lvl(a.level_cur) + case when v_ok then 1 else -1 end;
  a.level_cur := public.rank_gate_lvl_name(v_new_level);
  a.answers := a.answers || jsonb_build_array(jsonb_build_object('qid', v_qid, 'level', v_level, 'correct', v_ok));
  a.correct := a.correct + case when v_ok then 1 else 0 end;
  a.hard_correct := a.hard_correct + case when v_ok and v_level = 'kho' then 1 else 0 end;

  if v_n < a.total then
    v_next := public.rank_gate_pick(a.pool_ids, a.question_ids, a.level_cur);
    if v_next is null then raise exception 'Hết câu trong ngân hàng — nhờ thầy cô bổ sung'; end if;
    a.question_ids := a.question_ids || v_next;
  end if;

  update public.rank_gate_attempts
    set answers = a.answers, question_ids = a.question_ids, level_cur = a.level_cur,
        correct = a.correct, hard_correct = a.hard_correct
  where id = a.id
  returning * into a;

  if v_n >= a.total then
    v_result := public.rank_gate_finish(a.id);
    return jsonb_build_object('correct', v_ok, 'done', true, 'index', v_n, 'next_question', null, 'result', v_result);
  end if;

  return jsonb_build_object('correct', v_ok, 'done', false, 'index', v_n,
    'next_question', public.rank_gate_current_payload(a) -> 'question');
end; $$;

-- Chốt lượt thi: tính đỗ/trượt, đỗ -> rank_eval_gates ghi rank_gate_passes (nếu đủ cả danh hiệu) rồi rank_refresh_student.
-- Gọi lại sau khi đã nộp thì trả đúng kết quả đã lưu (idempotent).
create or replace function public.rank_gate_finish(p_attempt_id bigint)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_student uuid := auth.uid();
  a public.rank_gate_attempts%rowtype;
  v_rule record;
  v_pass boolean;
  v_pct int;
  v_hours int;
  v_titles int;
  v_need int;
  t public.rank_tiers%rowtype;
  v_promoted boolean;
  v_tier_now text;
  v_weak jsonb;
begin
  select * into a from public.rank_gate_attempts where id = p_attempt_id and student_id = v_student for update;
  if not found then raise exception 'Không tìm thấy lượt thi của em'; end if;

  if a.status = 'open' then
    if jsonb_array_length(a.answers) < a.total then raise exception 'Em chưa làm hết bài thi'; end if;
    select * into v_rule from public.rank_gate_rule(a.season_id, a.tier_code);
    v_pct := round(a.correct * 100.0 / a.total)::int;
    v_pass := v_pct >= v_rule.pct
              and a.hard_correct >= v_rule.hard
              and public.rank_gate_lvl(a.level_cur) >= public.rank_gate_lvl(v_rule.lvl);
    update public.rank_gate_attempts
      set status = 'done', pct = v_pct, passed = v_pass, level_end = a.level_cur, submitted_at = now()
    where id = a.id
    returning * into a;
    if a.passed then
      perform public.rank_eval_gates(a.season_id, v_student);
      perform public.rank_refresh_student(a.season_id, v_student);
    end if;
  end if;

  select * into v_rule from public.rank_gate_rule(a.season_id, a.tier_code);
  select * into t from public.rank_tiers where season_id = a.season_id and code = a.tier_code;
  v_hours := public.rank_cfg(a.season_id, 'gate_cooldown_hours', 48)::int;
  v_promoted := exists (select 1 from public.rank_gate_passes g
                        where g.season_id = a.season_id and g.student_id = v_student and g.tier_code = a.tier_code);
  select tier_code into v_tier_now from public.rank_student_seasons where season_id = a.season_id and student_id = v_student;
  v_titles := public.rank_titles_at_level(v_student, coalesce(t.required_title_level, 'thuc_tinh'));
  v_need := greatest(0, t.required_title_count - v_titles);

  -- 2 chủ đề (tầng bài) em sai nhiều nhất trong lượt này — gợi ý ôn.
  select coalesce(jsonb_agg(jsonb_build_object('topic_id', x.tid, 'name', x.name, 'wrong', x.n) order by x.n desc, x.name), '[]'::jsonb)
  into v_weak
  from (
    select coalesce(tp.parent_id, tp.id) as tid, max(coalesce(pt.name, tp.name)) as name, count(*) as n
    from jsonb_array_elements(a.answers) e
    join public.question_bank qb on qb.id = (e ->> 'qid')::bigint
    join public.question_topics tp on tp.id = qb.topic_id
    left join public.question_topics pt on pt.id = tp.parent_id
    where not coalesce((e ->> 'correct')::boolean, false)
    group by 1
    order by n desc, 2
    limit 2
  ) x;

  return jsonb_build_object(
    'attempt_id', a.id,
    'tier_code', a.tier_code,
    'passed', a.passed,
    'pct', a.pct,
    'correct', a.correct,
    'total', a.total,
    'hard_correct', a.hard_correct,
    'level_end', a.level_end,
    'pass_pct', v_rule.pct,
    'min_hard_correct', v_rule.hard,
    'min_level', v_rule.lvl,
    'promoted', v_promoted,
    'tier', v_tier_now,
    'missing_titles', v_need,
    'cooldown_until', case when a.passed then null else a.submitted_at + make_interval(hours => v_hours) end,
    'weak_topics', v_weak
  );
end; $$;

-- Cho tab GV/admin (và chính em): danh sách lượt thi của một học sinh, kèm từng câu đúng/sai + chủ đề.
create or replace function public.rank_gate_attempts_of(p_student uuid, p_season bigint default null)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
begin
  if not (p_student = auth.uid() or public.rank_is_staff() or public.teaches_student(p_student)) then
    return '[]'::jsonb;
  end if;
  return coalesce((
    select jsonb_agg(jsonb_build_object(
      'id', a.id, 'season_id', a.season_id, 'tier_code', a.tier_code, 'status', a.status,
      'correct', a.correct, 'total', a.total, 'hard_correct', a.hard_correct, 'pct', a.pct,
      'passed', a.passed, 'level_end', a.level_end, 'created_at', a.created_at, 'submitted_at', a.submitted_at,
      'answers', (
        select coalesce(jsonb_agg(jsonb_build_object(
                 'n', e.i, 'qid', e.v ->> 'qid', 'level', e.v ->> 'level', 'correct', (e.v ->> 'correct')::boolean,
                 'topic', coalesce(pt.name, tp.name)) order by e.i), '[]'::jsonb)
        from jsonb_array_elements(a.answers) with ordinality as e (v, i)
        left join public.question_bank qb on qb.id = (e.v ->> 'qid')::bigint
        left join public.question_topics tp on tp.id = qb.topic_id
        left join public.question_topics pt on pt.id = tp.parent_id)
    ) order by a.created_at desc)
    from public.rank_gate_attempts a
    where a.student_id = p_student and (p_season is null or a.season_id = p_season)
  ), '[]'::jsonb);
end; $$;

revoke execute on function public.rank_gate_start(text) from public, anon;
revoke execute on function public.rank_gate_answer(bigint, jsonb, bigint) from public, anon;
revoke execute on function public.rank_gate_finish(bigint) from public, anon;
revoke execute on function public.rank_gate_attempts_of(uuid, bigint) from public, anon;
grant execute on function public.rank_gate_start(text) to authenticated;
grant execute on function public.rank_gate_answer(bigint, jsonb, bigint) to authenticated;
grant execute on function public.rank_gate_finish(bigint) to authenticated;
grant execute on function public.rank_gate_attempts_of(uuid, bigint) to authenticated;

-- ---------- 5. rank_status_of: thêm khoá next.gate.* cho bài thi thăng hạng ----------
-- (bản gốc 20260930130000_rank_streak_freeze.sql; chỉ thêm biến, khối v_adaptive và các khoá cuối next.gate)
CREATE OR REPLACE FUNCTION public.rank_status_of(p_student uuid)
 RETURNS jsonb
 LANGUAGE plpgsql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $$
declare
  v_season bigint;
  s public.rank_seasons%rowtype;
  m public.rank_student_seasons%rowtype;
  info record;
  nxt public.rank_tiers%rowtype;
  v_next jsonb := null;
  v_gate jsonb := null;
  v_titles int;
  v_pct int;
  v_chal_title text;
  v_passed boolean;
  v_week date := public.rank_week_start(now());
  v_week_done int;
  v_goal record;
  v_display jsonb := null;
  p public.profiles%rowtype;
  v_rp int := 0;
  v_code text := 'tan_binh';
  v_day date := public.rank_vn_date(now());
  v_sc record;
  v_fmax int;
  v_adaptive boolean := false;
  v_rule record;
  v_att_n int := 0;
  v_att_pass boolean := false;
  v_open boolean := false;
  v_cool timestamptz;
  v_hours int;
  v_quiz int;
  v_grade text;
  v_can boolean := false;
begin
  if not public.rank_can_view(p_student) then return null; end if;
  select * into p from public.profiles where id = p_student;
  if p.display_title_code is not null then
    select jsonb_build_object('code', t.code, 'name', t.name, 'level', p.display_title_level, 'group', t.group_code)
    into v_display from public.rank_titles t where t.code = p.display_title_code;
  end if;

  v_season := public.rank_season_for_at(p_student, now());
  if v_season is null then
    return jsonb_build_object('season', null, 'display_title', v_display,
      'titles_count', (select count(distinct title_code) from public.rank_title_awards where student_id = p_student));
  end if;
  select * into s from public.rank_seasons where id = v_season;
  -- GĐ 1b #8: ngày của chuỗi đổi mốc khỏi 0h (rank_streak_day) + đóng băng
  v_day := public.rank_streak_day(v_season, now());
  select * into v_sc from public.rank_daily_streak_calc(v_season, p_student, now());
  v_fmax := public.rank_cfg(v_season, 'streak_freeze_per_week', 1)::int;
  select * into v_goal from public.rank_weekly_goal_of(v_season, p_student, v_week);
  select * into m from public.rank_student_seasons where season_id = v_season and student_id = p_student;
  if found then v_rp := m.rp; v_code := m.tier_code; end if;
  select * into info from public.rank_tier_info(v_season, v_code, v_rp);

  -- bậc kế tiếp + điều kiện còn thiếu
  select * into nxt from public.rank_tiers where season_id = v_season and sort = info.sort + 1;
  if found then
    v_passed := exists (select 1 from public.rank_gate_passes g where g.season_id = v_season and g.student_id = p_student and g.tier_code = nxt.code);
    if public.rank_tier_needs_gate(nxt) then
      v_titles := public.rank_titles_at_level(p_student, coalesce(nxt.required_title_level, 'thuc_tinh'));
      if nxt.challenge_exam_id is not null then
        select title into v_chal_title from public.exams where id = nxt.challenge_exam_id;
        v_pct := public.rank_best_pct(p_student, nxt.challenge_exam_id,
          (s.starts_on::timestamp) at time zone 'Asia/Ho_Chi_Minh',
          ((s.ends_on + 1)::timestamp) at time zone 'Asia/Ho_Chi_Minh');
      end if;
      -- Bài thi thăng hạng thích ứng (migration 20261003100000): trạng thái lượt thi của em.
      v_adaptive := nxt.challenge_exam_id is null and public.rank_gate_adaptive_code(nxt.code)
                    and public.rank_gate_mode(v_season) = 'adaptive';
      if v_adaptive then
        select * into v_rule from public.rank_gate_rule(v_season, nxt.code);
        v_hours := public.rank_cfg(v_season, 'gate_cooldown_hours', 48)::int;
        v_quiz := greatest(3, public.rank_cfg(v_season, 'gate_quiz_count', 12)::int);
        select count(*) filter (where a.status = 'done'),
               coalesce(bool_or(coalesce(a.passed, false)), false),
               max(a.submitted_at) filter (where a.status = 'done' and not coalesce(a.passed, false)),
               coalesce(bool_or(a.status = 'open'), false)
          into v_att_n, v_att_pass, v_cool, v_open
        from public.rank_gate_attempts a
        where a.season_id = v_season and a.student_id = p_student and a.tier_code = nxt.code;
        if v_cool is not null then v_cool := v_cool + make_interval(hours => v_hours); end if;
        v_can := v_open;
        if not v_can and not v_passed and not v_att_pass and v_rp >= nxt.min_rp
           and (v_cool is null or v_cool <= now()) then
          v_grade := public.rank_gate_grade(v_season, p_student);
          v_can := v_grade is not null and public.rank_gate_pool_size(v_season, v_grade) >= v_quiz;
        end if;
      end if;
      v_gate := jsonb_build_object(
        'passed', v_passed,
        'required_title_count', nxt.required_title_count,
        'required_title_level', nxt.required_title_level,
        'titles_have', v_titles,
        'challenge_required', nxt.challenge_exam_id is not null or (nxt.code in ('cao_thu', 'thach_dau') and not v_adaptive),
        'challenge_exam_id', nxt.challenge_exam_id,
        'challenge_title', v_chal_title,
        'challenge_pass_pct', round(coalesce(nxt.challenge_pass_score, 8) * 10),
        'challenge_best_pct', v_pct,
        'adaptive', v_adaptive,
        'attempts', v_att_n,
        'last_passed', v_att_pass,
        'cooldown_until', v_cool,
        'can_start', v_can,
        'open_attempt', v_open,
        'pass_pct', case when v_adaptive then v_rule.pct end,
        'min_hard_correct', case when v_adaptive then v_rule.hard end,
        'min_level', case when v_adaptive then v_rule.lvl end,
        'quiz_count', case when v_adaptive then v_quiz end,
        'cooldown_hours', case when v_adaptive then v_hours end
      );
    end if;
    v_next := jsonb_build_object('code', nxt.code, 'name', nxt.name, 'min_rp', nxt.min_rp,
      'rp_needed', greatest(0, nxt.min_rp - v_rp), 'gate', v_gate);
  end if;

  select count(*) into v_week_done from (
    select er.exam_id from public.exam_results er
    join public.rank_sources rs on rs.season_id = v_season and rs.enabled and rs.source_kind = 'exam' and rs.source_id = er.exam_id
    where er.student_id = p_student and public.rank_week_start(er.created_at) = v_week
    group by er.exam_id having max(er.score) >= v_goal.min_score
    union all
    select ps.item_id from public.practice_sessions ps
    join public.rank_sources rs on rs.season_id = v_season and rs.enabled and rs.source_kind = 'practice_item' and rs.source_id = ps.item_id
    where ps.student_id = p_student and public.rank_week_start(ps.created_at) = v_week
    group by ps.item_id having max(ps.score) >= v_goal.min_score
  ) x;

  return jsonb_build_object(
    'season', jsonb_build_object('id', s.id, 'name', s.name, 'starts_on', s.starts_on, 'ends_on', s.ends_on, 'status', s.status),
    'rp', v_rp,
    'tier', jsonb_build_object('code', info.code, 'name', info.name, 'sort', info.sort, 'tier_min', info.tier_min,
      'next_min', info.next_min, 'division', info.division, 'div_min', info.div_min, 'div_max', info.div_max,
      'paragon', v_code = 'thach_dau' and public.rank_is_paragon(p_student)),
    'next', v_next,
    'tier_reached_at', m.tier_reached_at,
    'joined_at', m.joined_at,
    'display_title', v_display,
    'titles_count', (select count(distinct title_code) from public.rank_title_awards where student_id = p_student),
    'weekly', jsonb_build_object('week_start', v_week, 'done', v_week_done,
      'target', v_goal.target,
      'min_score', v_goal.min_score,
      'personal', v_goal.personal,
      'rp', public.rank_cfg(v_season, 'weekly_goal_rp', 30)::int,
      'achieved', exists (select 1 from public.rank_rp_awards a where a.season_id = v_season and a.student_id = p_student and a.source_kind = 'weekly_goal' and a.source_ref = v_week::text and a.awarded > 0)),
    'daily', jsonb_build_object('date', v_day,
      'streak', v_sc.len,
      'reset_hour', public.rank_streak_offset(v_season),
      'freeze_per_week', v_fmax,
      'freeze_used_week', (select count(*) from unnest(v_sc.frozen) f where date_trunc('week', f) = date_trunc('week', v_day::timestamp))::int,
      'freeze_saved_recent', exists (select 1 from unnest(v_sc.frozen) f where f >= v_day - 1),
      'min_score', public.rank_cfg(v_season, 'weekly_goal_min_score', 7),
      'rp', public.rank_cfg(v_season, 'daily_streak_rp', 5)::int,
      'today_done', exists (select 1 from public.rank_rp_awards a where a.season_id = v_season and a.student_id = p_student and a.source_kind = 'daily_streak' and a.source_ref = v_day::text and a.awarded > 0))
  );
end; $$;
grant execute on function public.rank_status_of(uuid) to authenticated;

-- ============================================================================
-- TUỲ CHỌN (KHÔNG chạy tự động) — bắt HS đã có cửa bằng danh hiệu phải thi lại.
-- Migration này giữ nguyên mọi rank_gate_passes sẵn có (ai đã vượt cửa Tinh Anh/… bằng danh hiệu vẫn lên bậc
-- khi đủ RP, không phải thi). Nếu thầy muốn BẮT BUỘC thi thăng hạng cả với những em đó, chạy tay khối dưới
-- (xoá cửa của các bậc em CHƯA đạt tới, rồi tính lại) — làm trong giao dịch, xem số dòng rồi mới commit:
--
--   begin;
--   delete from public.rank_gate_passes g
--   using public.rank_tiers t, public.rank_student_seasons m
--   where t.season_id = g.season_id and t.code = g.tier_code
--     and m.season_id = g.season_id and m.student_id = g.student_id
--     and t.sort > m.tier_sort                       -- chỉ bậc em chưa đạt tới
--     and public.rank_gate_adaptive_code(g.tier_code)
--     and public.rank_gate_mode(g.season_id) = 'adaptive'
--     and g.season_id = <ID_MUA>;
--   select public.rank_recompute_season(<ID_MUA>);   -- cần quyền staff; hoặc rank_refresh_student từng em
--   commit;
-- ============================================================================
