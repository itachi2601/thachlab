-- ÔN TẬP THEO CHẶNG — phần ôn CÁC DẠNG BÀI TẬP (23/10/2026).
-- "Dạng" = các dạng trong mục Bài tập mẫu của bài (lesson_items.kind='bai_tap_mau', questions[].label bắt đầu bằng "Dạng").
-- Câu ngân hàng chỉ gắn với yêu cầu cần đạt (nhiều dạng dùng chung một yêu cầu cần đạt) nên cần bảng gán riêng
-- question_dang: câu nào thuộc dạng nào của bài nào. Bảng này do script/Claude điền (thí điểm Chương 3 lớp 12),
-- câu nào không chắc thì để trống — không gán bừa vì kết luận "em vướng dạng nào" dựa vào đó.
--   * review_build_dang_exam: dựng MỘT đề cho một bài, mỗi dạng bốc p_per_dang câu bài tập đã gán, gán đề cho lớp của
--     buổi ôn; trả về dang_by_index (nhãn dạng của từng câu) để lưu vào định nghĩa chặng.
--   * review_board: thêm by_dang (sai theo dạng ở chặng hiện tại) và nhãn dạng cho câu sai nhiều.
-- Chạy lúc nào cũng được: thêm bảng + hàm mới, review_board thay bằng bản có thêm trường (không bớt trường cũ).
-- Rollback ở cuối file và perf/rollback/20261023120000_on_tap_dang_bai_tap.down.sql.
begin;

create table if not exists public.question_dang (
  question_id bigint not null references public.question_bank (id) on delete cascade,
  lesson_id bigint not null references public.lessons (id) on delete cascade,
  dang_label text not null,
  source text not null default 'claude-2026-10-23',
  unsure boolean not null default false,
  created_at timestamptz not null default now(),
  primary key (question_id, lesson_id)
);
create index if not exists question_dang_lesson_label_idx on public.question_dang (lesson_id, dang_label);
alter table public.question_dang enable row level security;
revoke all on public.question_dang from anon, authenticated;

-- Dạng của một bài, theo thứ tự trong Bài tập mẫu.
create or replace function public.lesson_dang_labels(p_lesson bigint)
returns table (ord int, label text)
language sql stable security definer set search_path = public
as $$
  select (d.ord)::int, d.q ->> 'label'
  from public.lesson_items i
  cross join lateral jsonb_array_elements(i.questions) with ordinality as d(q, ord)
  where i.lesson_id = p_lesson and i.kind = 'bai_tap_mau' and d.q ->> 'label' like 'Dạng%'
  order by d.ord;
$$;
revoke execute on function public.lesson_dang_labels(bigint) from public, anon, authenticated;

create or replace function public.review_build_dang_exam(p_class bigint, p_lesson bigint, p_per_dang int default 3)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  v_lesson_title text;
  v_questions jsonb;
  v_by_index jsonb;
  v_dang jsonb;
  v_n int;
  v_exam bigint;
  v_title text;
begin
  if not public.is_staff() then raise exception 'forbidden'; end if;
  if p_per_dang is null or p_per_dang not between 1 and 6 then raise exception 'per_dang_invalid'; end if;
  select title into v_lesson_title from public.lessons where id = p_lesson;
  if not found then raise exception 'lesson_not_found'; end if;
  if not exists (select 1 from public.classes where id = p_class) then raise exception 'class_not_found'; end if;

  with picked as (
    select dl.ord, dl.label, qb.question,
           row_number() over (partition by dl.label order by random()) as pick
    from public.lesson_dang_labels(p_lesson) dl
    join public.question_dang qd on qd.lesson_id = p_lesson and qd.dang_label = dl.label and not qd.unsure
    join public.question_bank qb on qb.id = qd.question_id and not qb.archived and qb.form = 'bai_tap'
      and coalesce(array_length(qb.lint_flags, 1), 0) = 0
      and coalesce(qb.question ->> 'question', '') <> ''
  ),
  chosen as (select * from picked where pick <= p_per_dang)
  select
    coalesce(jsonb_agg(question order by ord, pick), '[]'::jsonb),
    coalesce(jsonb_agg(label order by ord, pick), '[]'::jsonb),
    coalesce((select jsonb_agg(jsonb_build_object('label', g.label, 'n', g.n) order by g.ord)
              from (select ord, label, count(*)::int as n from chosen group by ord, label) g), '[]'::jsonb)
  into v_questions, v_by_index, v_dang
  from chosen;

  v_n := jsonb_array_length(v_questions);
  if v_n = 0 then raise exception 'no_dang:%', p_lesson; end if;

  v_title := 'Ôn dạng — ' || v_lesson_title;
  insert into public.exams (title, duration_minutes, published, questions, topic, difficulty, subject_code, pass_score)
  values (v_title, greatest(10, v_n * 2), true, v_questions, v_lesson_title, 'trung-binh', 'vat-ly', 7.5)
  returning id into v_exam;

  insert into public.exam_classes (exam_id, class_id) values (v_exam, p_class) on conflict do nothing;

  return jsonb_build_object('exam_id', v_exam, 'title', v_title, 'question_count', v_n, 'dang', v_dang, 'dang_by_index', v_by_index);
end;
$$;
revoke execute on function public.review_build_dang_exam(bigint, bigint, int) from public, anon;
grant execute on function public.review_build_dang_exam(bigint, bigint, int) to authenticated;

-- Số câu đã gán theo dạng của một bài (để màn tạo buổi ôn báo bài nào đủ câu).
create or replace function public.review_dang_pool(p_lesson bigint)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
begin
  if not public.is_staff() then raise exception 'forbidden'; end if;
  return coalesce((
    select jsonb_agg(jsonb_build_object('label', dl.label, 'n', coalesce(c.n, 0)) order by dl.ord)
    from public.lesson_dang_labels(p_lesson) dl
    left join (
      select qd.dang_label, count(*)::int as n
      from public.question_dang qd
      join public.question_bank qb on qb.id = qd.question_id and not qb.archived and qb.form = 'bai_tap'
      where qd.lesson_id = p_lesson and not qd.unsure
      group by qd.dang_label
    ) c on c.dang_label = dl.label
  ), '[]'::jsonb);
end;
$$;
revoke execute on function public.review_dang_pool(bigint) from public, anon;
grant execute on function public.review_dang_pool(bigint) to authenticated;

-- Bảng điều phối: thêm by_dang + nhãn dạng cho câu sai nhiều. Còn lại giữ nguyên bản 20261021120000.
create or replace function public.review_board(p_session bigint)
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  r public.review_sessions;
  v_idx int;
  v_students jsonb;
  v_wrong jsonb := '[]'::jsonb;
  v_dang jsonb := '[]'::jsonb;
  v_exam bigint;
  v_map jsonb;
begin
  if not public.is_staff() then raise exception 'forbidden'; end if;
  select * into r from public.review_sessions where id = p_session;
  if not found then raise exception 'not_found'; end if;
  v_idx := r.current_stage;

  select coalesce(jsonb_agg(
    jsonb_build_object('id', p.id, 'name', p.full_name)
    || case when v_idx >= 0
         then public.review_student_stage(r, p.id, v_idx)
         else jsonb_build_object('state', 'idle', 'answered', 0, 'total', 0, 'best_pct', null, 'tries', 0, 'idle_secs', null)
       end
  ), '[]'::jsonb)
  into v_students
  from public.user_classes uc
  join public.profiles p on p.id = uc.user_id
  where uc.class_id = r.class_id and uc.status = 'active' and p.role = 'student' and coalesce(p.is_test, false) = false;

  if v_idx >= 0 then
    v_exam := (r.stages -> v_idx ->> 'exam_id')::bigint;
    v_map := r.stages -> v_idx -> 'dang_by_index';
    select coalesce(jsonb_agg(t order by t.pct desc, t.total desc), '[]'::jsonb) into v_wrong
    from (
      select q.question_index as idx,
             case when jsonb_typeof(v_map) = 'array' then v_map ->> q.question_index end as dang,
             count(*)::int as total,
             count(*) filter (where q.is_correct is false)::int as wrong,
             round(100.0 * count(*) filter (where q.is_correct is false) / count(*))::int as pct
      from public.exam_question_results q
      join public.exam_results er on er.id = q.exam_result_id
      join public.user_classes uc on uc.user_id = q.student_id and uc.class_id = r.class_id and uc.status = 'active'
      where q.exam_id = v_exam and er.created_at >= r.created_at and q.is_correct is not null and q.max > 0
      group by q.question_index
      having count(*) filter (where q.is_correct is false) > 0
      order by pct desc, total desc
      limit 8
    ) t;

    if jsonb_typeof(v_map) = 'array' then
      select coalesce(jsonb_agg(t order by t.pct desc, t.total desc), '[]'::jsonb) into v_dang
      from (
        select v_map ->> q.question_index as label,
               count(*)::int as total,
               count(*) filter (where q.is_correct is false)::int as wrong,
               round(100.0 * count(*) filter (where q.is_correct is false) / count(*))::int as pct,
               count(distinct q.student_id) filter (where q.is_correct is false)::int as students_wrong,
               count(distinct q.student_id)::int as students
        from public.exam_question_results q
        join public.exam_results er on er.id = q.exam_result_id
        join public.user_classes uc on uc.user_id = q.student_id and uc.class_id = r.class_id and uc.status = 'active'
        where q.exam_id = v_exam and er.created_at >= r.created_at and q.is_correct is not null and q.max > 0
          and v_map ->> q.question_index is not null
        group by v_map ->> q.question_index
      ) t;
    end if;
  end if;

  return jsonb_build_object(
    'now', now(),
    'session', jsonb_build_object(
      'id', r.id, 'title', r.title, 'class_id', r.class_id, 'threshold', r.threshold, 'status', r.status,
      'current_stage', r.current_stage, 'stage_started_at', r.stage_started_at,
      'secs_left', public.review_secs_left(r), 'stages', r.stages
    ),
    'students', v_students,
    'wrongest', v_wrong,
    'by_dang', v_dang
  );
end;
$$;

commit;

-- ROLLBACK (cũng ở perf/rollback/20261023120000_on_tap_dang_bai_tap.down.sql):
-- begin;
-- drop function if exists public.review_dang_pool(bigint);
-- drop function if exists public.review_build_dang_exam(bigint, bigint, int);
-- drop function if exists public.lesson_dang_labels(bigint);
-- drop table if exists public.question_dang;
-- -- review_board: chạy lại phần review_board của supabase/migrations/20261021120000_on_tap_theo_chang.sql
-- commit;
