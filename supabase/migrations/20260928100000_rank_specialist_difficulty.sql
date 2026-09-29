-- ============================================================================
-- feat(rank): 3 mức danh hiệu chuyên môn khớp 3 mức độ câu hỏi Dễ/TB/Khó
-- 28/9/2026 — theo yêu cầu thầy: "mức độ mở danh hiệu nên đi kèm với điều kiện
-- giải được số lượng câu hỏi ở mức độ tương ứng".
-- ============================================================================
-- Trước: Thức Tỉnh/Làm Chủ xét theo TỔNG số câu đã làm + % chính xác + độ phủ
-- chủ đề (rank_title_stats/rank_eval_titles cũ); Huyền Thoại xét % điểm một đề
-- thử thách riêng (rank_titles.legend_challenge_exam_id) — không liên quan gì
-- đến mức độ khó của CÂU HỎI đã giải.
--
-- Sau: mỗi mức xét ĐỘC LẬP theo đúng độ khó — Thức Tỉnh cần đủ số câu Dễ giải
-- ĐÚNG, Làm Chủ cần đủ số câu Trung bình, Huyền Thoại cần đủ số câu Khó — tính
-- trên MỌI lượt làm (đề + luyện tập) có gắn chủ đề của danh hiệu đó, không kể
-- nguồn đề. Bỏ điều kiện đề thử thách riêng cho mức Huyền Thoại (cột
-- legend_challenge_exam_id GIỮ NGUYÊN trong schema — vẫn được dùng cho danh
-- hiệu thành tích "Bách Phát Bách Trúng", không xoá).
--
-- Cách lấy độ khó của câu đã giải: exam_question_results/practice_question_results
-- vốn đã lưu sẵn topic_id/topic_name/form của từng câu ngay lúc nộp bài (đọc từ
-- exam.questions[i] ở client — xem buildQuestionResults() trong
-- features/exams/types.ts) — thêm đúng 1 cột `difficulty` theo cùng cách, KHÔNG
-- cần join ngược sang question_bank (câu hỏi có thể trùng nội dung nhưng khác
-- nhãn độ khó tuỳ đề). Cột mới cho lượt làm SAU migration này tự có giá trị vì
-- code app đã được sửa cùng đợt; lượt làm CŨ được backfill 1 lần dưới đây bằng
-- cách đọc lại exams.questions tại đúng vị trí câu (ước lượng tốt nhất — đề có
-- thể đã bị sửa sau khi HS làm, cùng rủi ro với topic_name/form vốn đã chấp
-- nhận từ trước).
--
-- Cách chạy: supabase db query --linked -f supabase/migrations/20260928100000_rank_specialist_difficulty.sql
-- KHÔNG dùng `supabase db push`. Idempotent — chạy lại được.
-- Rollback: perf/rollback/20260928100000_rank_specialist_difficulty.down.sql
--
-- SAU KHI CHẠY: chạy tiếp docs/supabase-recompute-rank-titles-20260928.sql để
-- xét lại danh hiệu cho mọi học sinh trong 2 mùa đang mở (dùng dữ liệu vừa
-- backfill) — không tự cộng RP, chỉ có thể MỞ THÊM danh hiệu đã đủ điều kiện.
-- ============================================================================

begin;

-- ---------- 0. Cột độ khó denormalize trên từng dòng câu đã giải ----------
alter table public.exam_question_results
  add column if not exists difficulty text not null default ''
  check (difficulty in ('', 'de', 'trung-binh', 'kho'));

alter table public.practice_question_results
  add column if not exists difficulty text not null default ''
  check (difficulty in ('', 'de', 'trung-binh', 'kho'));

comment on column public.exam_question_results.difficulty is
  'Độ khó của câu tại thời điểm nộp bài (đọc từ exams.questions[i].difficulty) — dùng để xét danh hiệu chuyên môn theo mức độ.';
comment on column public.practice_question_results.difficulty is
  'Độ khó của câu tại thời điểm nộp bài — cùng ý nghĩa với exam_question_results.difficulty.';

-- ---------- 1. Ngưỡng số câu theo từng mức, thay cho % chính xác + đề thử thách ----------
alter table public.rank_titles add column if not exists min_de int not null default 12;
alter table public.rank_titles add column if not exists min_tb int not null default 8;
alter table public.rank_titles add column if not exists min_kho int not null default 5;

comment on column public.rank_titles.min_de is 'Thức Tỉnh: số câu Dễ tối thiểu phải giải ĐÚNG (thuộc chủ đề danh hiệu).';
comment on column public.rank_titles.min_tb is 'Làm Chủ: số câu Trung bình tối thiểu phải giải ĐÚNG.';
comment on column public.rank_titles.min_kho is 'Huyền Thoại: số câu Khó tối thiểu phải giải ĐÚNG.';
comment on column public.rank_titles.min_questions is
  'CŨ — không còn dùng để xét danh hiệu chuyên môn (xem min_de/min_tb/min_kho). Giữ cột lại, không xoá dữ liệu.';
comment on column public.rank_titles.awaken_accuracy is 'CŨ — không còn dùng, thay bằng min_de.';
comment on column public.rank_titles.master_accuracy is 'CŨ — không còn dùng, thay bằng min_tb.';
comment on column public.rank_titles.legend_accuracy is 'CŨ — không còn dùng để xét mức Huyền Thoại chuyên môn; đề thử thách ở legend_challenge_exam_id giờ chỉ tính vào danh hiệu "Bách Phát Bách Trúng".';

-- ---------- 2. Backfill difficulty cho các lượt làm đã có trước migration ----------
update public.exam_question_results eqr
set difficulty = case when ex.questions -> eqr.question_index ->> 'difficulty' in ('de', 'trung-binh', 'kho')
                       then ex.questions -> eqr.question_index ->> 'difficulty' else '' end
from public.exams ex
where ex.id = eqr.exam_id and eqr.difficulty = '';

update public.practice_question_results pqr
set difficulty = case when ex.questions -> pqr.source_index ->> 'difficulty' in ('de', 'trung-binh', 'kho')
                       then ex.questions -> pqr.source_index ->> 'difficulty' else '' end
from public.exams ex
where ex.id = pqr.exam_id and pqr.exam_id is not null and pqr.difficulty = '';

-- ---------- 3. rank_title_stats: cộng thêm số câu ĐÚNG theo từng mức độ ----------
-- Đổi OUT parameters (thêm 3 cột) — CREATE OR REPLACE không cho phép, phải DROP trước.
drop function if exists public.rank_title_stats(uuid, text);
create function public.rank_title_stats(p_student uuid, p_title text)
returns table(n int, correct int, covered int, total_topics int, acc int, de_correct int, tb_correct int, kho_correct int)
language sql stable set search_path = public
as $$
  with topics as (
    select tt.topic_id from public.rank_title_topics tt where tt.title_code = p_title
  ),
  rows_ as (
    select coalesce(t.parent_id, t.id) as lesson_topic, eqr.is_correct, eqr.difficulty
    from public.exam_question_results eqr
    join public.question_topics t on t.id = eqr.topic_id
    where eqr.student_id = p_student
      and coalesce(t.parent_id, t.id) in (select topic_id from topics)
    union all
    select coalesce(t.parent_id, t.id) as lesson_topic, pqr.is_correct, pqr.difficulty
    from public.practice_question_results pqr
    join public.question_topics t on t.id = pqr.topic_id
    where pqr.student_id = p_student
      and coalesce(t.parent_id, t.id) in (select topic_id from topics)
  ),
  per_topic as (
    select lesson_topic, count(*) as c from rows_ group by lesson_topic
  )
  select
    (select count(*) from rows_)::int,
    (select count(*) filter (where is_correct) from rows_)::int,
    (select count(*) from per_topic where c >= 3)::int,
    (select count(*) from topics)::int,
    case when (select count(*) from rows_) > 0
      then round((select count(*) filter (where is_correct) from rows_) * 100.0 / (select count(*) from rows_))::int
      else 0 end,
    (select count(*) filter (where is_correct and difficulty = 'de') from rows_)::int,
    (select count(*) filter (where is_correct and difficulty = 'trung-binh') from rows_)::int,
    (select count(*) filter (where is_correct and difficulty = 'kho') from rows_)::int;
$$;

-- ---------- 4. rank_eval_titles: xét 3 mức độc lập theo đúng độ khó ----------
create or replace function public.rank_eval_titles(p_student uuid, p_season bigint default null)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  t public.rank_titles%rowtype;
  st record;
  v_req_titles text[];
  v_req_level text;
  v_ok boolean;
begin
  -- (a) chuyên môn: Thức Tỉnh (Dễ) · Làm Chủ (Trung bình) · Huyền Thoại (Khó) — độc lập theo độ khó
  for t in select * from public.rank_titles where kind = 'specialist' and enabled and public.rank_title_is_active(code) loop
    select * into st from public.rank_title_stats(p_student, t.code);
    if st.de_correct >= t.min_de then
      perform public.rank_grant_title(p_student, t.code, 'thuc_tinh', p_season, jsonb_build_object('de_correct', st.de_correct, 'need', t.min_de));
    end if;
    if st.tb_correct >= t.min_tb then
      perform public.rank_grant_title(p_student, t.code, 'lam_chu', p_season, jsonb_build_object('tb_correct', st.tb_correct, 'need', t.min_tb));
    end if;
    if st.kho_correct >= t.min_kho then
      perform public.rank_grant_title(p_student, t.code, 'huyen_thoai', p_season, jsonb_build_object('kho_correct', st.kho_correct, 'need', t.min_kho));
    end if;
  end loop;

  -- (b) bộ sưu tập: mọi danh hiệu thành phần ĐANG ACTIVE đạt từ mức yêu cầu
  for t in select * from public.rank_titles where kind = 'collection' and enabled and (requires ? 'titles') loop
    select array_agg(x) into v_req_titles from jsonb_array_elements_text(t.requires -> 'titles') x;
    v_req_level := coalesce(t.requires ->> 'level', 'lam_chu');
    if not exists (select 1 from unnest(v_req_titles) c where public.rank_title_is_active(c)) then
      continue;
    end if;
    select bool_and(exists (
      select 1 from public.rank_title_awards a
      where a.student_id = p_student and a.title_code = c and public.rank_level_rank(a.level) >= public.rank_level_rank(v_req_level)
    )) into v_ok
    from unnest(v_req_titles) c where public.rank_title_is_active(c);
    if coalesce(v_ok, false) then
      perform public.rank_grant_title(p_student, t.code, 'don', p_season, jsonb_build_object('level', v_req_level));
    end if;
  end loop;

  -- (c) "Kẻ Giải Mã Vũ Trụ": mọi bộ sưu tập đang khả dụng
  for t in select * from public.rank_titles where kind = 'collection' and enabled and coalesce((requires ->> 'collections')::boolean, false) loop
    select bool_and(exists (
      select 1 from public.rank_title_awards a where a.student_id = p_student and a.title_code = c.code
    )) into v_ok
    from public.rank_titles c
    where c.kind = 'collection' and c.enabled and (c.requires ? 'titles')
      and exists (select 1 from jsonb_array_elements_text(c.requires -> 'titles') x where public.rank_title_is_active(x));
    if coalesce(v_ok, false) then
      perform public.rank_grant_title(p_student, t.code, 'don', p_season, '{}'::jsonb);
    end if;
  end loop;
end; $$;

-- ---------- 5. rank_titles_of: tiến độ hiển thị cho HS theo 3 mức độ ----------
create or replace function public.rank_titles_of(p_student uuid)
returns jsonb
language plpgsql security definer stable set search_path = public
as $$
declare
  v_out jsonb := '[]'::jsonb;
  t public.rank_titles%rowtype;
  st record;
  v_levels jsonb;
  v_have text;
  v_visible boolean;
  v_progress jsonb;
  v_req int;
  v_met int;
begin
  if not public.rank_can_view(p_student) then return null; end if;

  for t in select * from public.rank_titles where enabled order by
    case group_code when 'co_hoc' then 1 when 'dao_dong_song' then 2 when 'dien_tu' then 3 when 'nhiet_hoc' then 4 when 'hien_dai' then 5 when 'bo_suu_tap' then 6 else 7 end, sort
  loop
    select coalesce(jsonb_object_agg(a.level, a.awarded_at), '{}'::jsonb) into v_levels
    from public.rank_title_awards a where a.student_id = p_student and a.title_code = t.code;
    select a.level into v_have from public.rank_title_awards a
    where a.student_id = p_student and a.title_code = t.code
    order by public.rank_level_rank(a.level) desc limit 1;

    v_progress := null;
    if t.kind = 'specialist' then
      v_visible := exists (
        select 1 from public.rank_title_topics tt
        join public.question_topics qt on qt.id = tt.topic_id
        left join public.chapter_classes cc on cc.chapter_id = qt.chapter_id
        where tt.title_code = t.code
          and (cc.class_id is null or cc.class_id in (
            select class_id from public.user_classes where user_id = p_student and status = 'active'))
      );
      select * into st from public.rank_title_stats(p_student, t.code);
      v_progress := jsonb_build_object('n', st.n, 'correct', st.correct,
        'de_correct', st.de_correct, 'de_need', t.min_de,
        'tb_correct', st.tb_correct, 'tb_need', t.min_tb,
        'kho_correct', st.kho_correct, 'kho_need', t.min_kho,
        'topics', (select coalesce(jsonb_agg(jsonb_build_object('id', qt.id, 'name', qt.name, 'lesson_id', qt.lesson_id) order by qt.grade, qt.sort_order), '[]'::jsonb)
                   from public.rank_title_topics tt join public.question_topics qt on qt.id = tt.topic_id where tt.title_code = t.code));
    elsif t.kind = 'collection' and (t.requires ? 'titles') then
      select count(*) filter (where public.rank_title_is_active(x)),
             count(*) filter (where public.rank_title_is_active(x) and exists (
               select 1 from public.rank_title_awards a where a.student_id = p_student and a.title_code = x
                 and public.rank_level_rank(a.level) >= public.rank_level_rank(coalesce(t.requires ->> 'level', 'lam_chu'))))
      into v_req, v_met
      from jsonb_array_elements_text(t.requires -> 'titles') x;
      v_visible := v_req > 0;
      v_progress := jsonb_build_object('required', v_req, 'met', v_met, 'level', coalesce(t.requires ->> 'level', 'lam_chu'),
        'titles', t.requires -> 'titles');
    else
      v_visible := true;
    end if;

    v_out := v_out || jsonb_build_object(
      'code', t.code, 'group', t.group_code, 'kind', t.kind, 'name', t.name, 'description', t.description,
      'visible', v_visible, 'active', case when t.kind = 'specialist' then public.rank_title_is_active(t.code) else v_visible end,
      'level', v_have, 'levels', v_levels, 'progress', v_progress
    );
  end loop;
  return v_out;
end; $$;

commit;
