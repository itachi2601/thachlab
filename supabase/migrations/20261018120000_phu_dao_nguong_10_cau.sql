-- ============================================================================
-- Ngưỡng mở phụ đạo mới theo đề xuất của học sinh (khảo sát 18/10/2026, thầy chốt)
--
-- Trước: sai >= 50% trong 2 đề kiểm tra gần nhất, tối thiểu 3 câu -> mẫu quá nhỏ, dễ gắn nhãn oan.
-- Nay (mỗi em x bài x dạng, chỉ đề kiểm tra/BTVN/định kỳ - exam_is_assessment):
--   * Cửa sổ trượt: 12 câu gần nhất của nhóm (lấy từ lần làm cuối của mọi đề kiểm tra, không giới hạn 2 đề).
--   * Mở thường: có >= 10 câu trong cửa sổ và sai >= 50%.
--   * Mở đường tắt: 5-9 câu và sai >= 80% (em sai gần hết không phải chờ qua 3 đề).
--   * Không mở lại mục vừa đóng nếu 2 đề gần nhất vẫn làm đúng >= 75% (tránh mở-đóng lặp).
--   * Đóng mục (phần b) giữ nguyên: bài sau đúng >= 75%.
-- Dọn một lần: mục 'auto' đang 'open' (chưa giao trợ giảng) -> dismissed, rồi refresh từng em: mục nào còn đạt ngưỡng
-- mới tự mở lại. Mục assigned/tutored không đụng.
-- Chạy: bash scripts/run-migrations.sh --only N - lúc nào cũng được (thay hàm + cập nhật trạng thái mục phụ đạo).
-- Rollback: perf/rollback/20261018120000_phu_dao_nguong_10_cau.down.sql (khôi phục hàm 17/10; mục đã dismissed
-- thì chạy refresh lại cho từng em hoặc đổi note này về open).
-- ============================================================================

create or replace function public.refresh_tutoring_needs(p_student uuid)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  v_class bigint;
  v_window int := 2;          -- phần (b): xét 2 bài gần nhất
  v_roll int := 12;           -- phần (a): cửa sổ trượt 12 câu gần nhất
  v_min_q int := 10;          -- cần >= 10 câu mới dám kết luận
  v_need_pct numeric := 50;   -- sai >= 50% -> cần phụ đạo
  v_fast_q int := 5;          -- đường tắt: >= 5 câu ...
  v_fast_pct numeric := 80;   -- ... mà sai >= 80%
  v_clear_pct numeric := 25;  -- sai <= 25% (đúng >= 75%) -> coi như đã khắc phục
begin
  select uc.class_id into v_class
  from public.user_classes uc
  where uc.user_id = p_student and uc.status = 'active'
  order by uc.class_id desc
  limit 1;

  -- (a) mở / cập nhật mục còn hổng - CHỈ xét đề kiểm tra / BTVN / định kỳ (exam_is_assessment).
  with last_try as (
    select distinct on (er.exam_id) er.id, er.created_at
    from public.exam_results er
    where er.student_id = p_student
      and public.exam_is_assessment(er.exam_id)
    order by er.exam_id, er.created_at desc
  ),
  qs as (
    select lt.created_at, q.question_index, q.is_correct,
           coalesce(t.parent_id, q.topic_id) as topic_id,
           coalesce(nullif(q.form, ''), '') as form
    from last_try lt
    join public.exam_question_results q on q.exam_result_id = lt.id
    join public.question_topics t on t.id = q.topic_id
    where q.student_id = p_student and q.topic_id is not null
  ),
  ranked as (
    select qs.*, row_number() over (partition by topic_id, form
                                    order by created_at desc, question_index) as rn
    from qs
  ),
  agg as (
    select topic_id, form,
           (count(*))::int as total,
           (count(*) filter (where not is_correct))::int as wrong
    from ranked
    where rn <= v_roll
    group by topic_id, form
  ),
  recent as (
    select exam_id from (
      select er.exam_id, max(er.created_at) as last_at
      from public.exam_results er
      where er.student_id = p_student and public.exam_is_assessment(er.exam_id)
      group by er.exam_id
      order by last_at desc
      limit v_window
    ) x
  ),
  cur_try as (
    select distinct on (er.exam_id) er.id
    from public.exam_results er
    join recent r on r.exam_id = er.exam_id
    where er.student_id = p_student
    order by er.exam_id, er.created_at desc
  ),
  cur as (
    select coalesce(t.parent_id, q.topic_id) as topic_id,
           coalesce(nullif(q.form, ''), '') as form,
           (count(*))::int as total,
           (count(*) filter (where not q.is_correct))::int as wrong
    from public.exam_question_results q
    join cur_try ct on ct.id = q.exam_result_id
    join public.question_topics t on t.id = q.topic_id
    where q.student_id = p_student and q.topic_id is not null
    group by coalesce(t.parent_id, q.topic_id), coalesce(nullif(q.form, ''), '')
  )
  insert into public.tutoring_needs
    (student_id, class_id, topic_id, form, wrong, total, pct, source, status)
  select p_student, v_class, a.topic_id, a.form, a.wrong, a.total,
         round(a.wrong * 100.0 / a.total)::int, 'auto', 'open'
  from agg a
  left join cur c on c.topic_id = a.topic_id and c.form = a.form
  where ((a.total >= v_min_q and a.wrong * 100.0 / a.total >= v_need_pct)
      or (a.total >= v_fast_q and a.wrong * 100.0 / a.total >= v_fast_pct))
    and not (c.total >= 2 and c.wrong * 100.0 / c.total <= v_clear_pct)
  on conflict (student_id, topic_id, form) do update set
    wrong = excluded.wrong,
    total = excluded.total,
    pct = excluded.pct,
    class_id = coalesce(excluded.class_id, tutoring_needs.class_id),
    last_seen_at = now(),
    status = case when tutoring_needs.status in ('cleared', 'dismissed')
                  then 'open' else tutoring_needs.status end,
    cleared_at = case when tutoring_needs.status in ('cleared', 'dismissed')
                  then null else tutoring_needs.cleared_at end,
    note = case when tutoring_needs.status in ('cleared', 'dismissed')
                  then '' else tutoring_needs.note end;

  -- (b) làm đúng lại -> đóng mục (giữ nguyên như bản 17/10/2026)
  with recent as (
    select er.exam_id
    from public.exam_results er
    where er.student_id = p_student
    group by er.exam_id
    order by max(er.created_at) desc
    limit v_window
  ),
  last_try as (
    select distinct on (er.exam_id) er.id
    from public.exam_results er
    join recent r on r.exam_id = er.exam_id
    where er.student_id = p_student
    order by er.exam_id, er.created_at desc
  ),
  agg as (
    select coalesce(t.parent_id, q.topic_id) as topic_id,
           coalesce(nullif(q.form, ''), '') as form,
           (count(*))::int as total,
           (count(*) filter (where not q.is_correct))::int as wrong
    from public.exam_question_results q
    join last_try lt on lt.id = q.exam_result_id
    join public.question_topics t on t.id = q.topic_id
    where q.student_id = p_student and q.topic_id is not null
    group by coalesce(t.parent_id, q.topic_id), coalesce(nullif(q.form, ''), '')
  )
  update public.tutoring_needs n
  set status = 'cleared',
      cleared_at = now(),
      last_seen_at = now(),
      wrong = a.wrong,
      total = a.total,
      pct = round(a.wrong * 100.0 / a.total)::int,
      note = case when n.note <> '' then n.note
                  when n.tutored_at is not null then 'đã phụ đạo, bài sau làm đúng lại'
                  else 'tự khắc phục, không cần phụ đạo' end
  from agg a
  where n.student_id = p_student
    and n.topic_id = a.topic_id
    and n.form = a.form
    and n.status in ('open', 'assigned', 'tutored')
    and a.total >= 2
    and a.wrong * 100.0 / a.total <= v_clear_pct;
end;
$$;

-- Dọn một lần: mục auto đang mở (chưa giao) -> dismissed, rồi refresh để mục còn đạt ngưỡng mới tự mở lại.
do $$
declare r record; v_before int; v_after int;
begin
  select count(*) into v_before from public.tutoring_needs where source = 'auto' and status = 'open';
  update public.tutoring_needs
    set status = 'dismissed', note = 'đổi ngưỡng 10 câu, bỏ 18/10/2026', updated_at = now()
  where source = 'auto' and status = 'open';
  for r in select distinct student_id from public.tutoring_needs where note = 'đổi ngưỡng 10 câu, bỏ 18/10/2026' loop
    perform public.refresh_tutoring_needs(r.student_id);
  end loop;
  select count(*) into v_after from public.tutoring_needs where source = 'auto' and status = 'open';
  raise notice 'Mục auto đang mở: trước % → sau % (còn dismissed vì không đạt ngưỡng mới: %)',
    v_before, v_after, (select count(*) from public.tutoring_needs where note = 'đổi ngưỡng 10 câu, bỏ 18/10/2026');
end $$;
