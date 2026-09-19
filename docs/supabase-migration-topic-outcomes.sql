-- ============================================================
-- Chủ đề hai tầng: BÀI HỌC → YÊU CẦU CẦN ĐẠT
-- ============================================================
-- Chạy SAU:
--   docs/supabase-migration-exam-analytics.sql        (question_topics, exam_question_results)
--   docs/supabase-migration-question-topics-seed.sql  (73 chủ đề tầng bài)
--   docs/supabase-migration-tutoring-needs.sql        (mục cần phụ đạo)
-- Idempotent — chạy lại được.
--
-- VÌ SAO HAI TẦNG
-- Một "yêu cầu cần đạt" (CT GDPT 2018) là một mẩu nhỏ trong bài, nên nhãn chủ đề phải
-- mịn tới mức đó thì thầy mới biết em hổng đúng chỗ nào. Nhưng một đề 40 câu trải 6–8
-- bài: nếu kết luận phụ đạo cũng tính ở tầng YCCĐ thì mỗi YCCĐ chỉ còn 1–2 câu, không
-- bao giờ đạt ngưỡng 3 câu của refresh_tutoring_needs -> hệ thống im lặng.
-- Nên: GẮN NHÃN MỊN (câu hỏi trỏ YCCĐ), KẾT LUẬN THÔ (mục phụ đạo mở ở tầng bài, vì
-- một buổi phụ đạo dạy cả bài chứ không dạy một YCCĐ 5 phút). Chi tiết "hổng cụ thể
-- phần nào" đọc thẳng từ exam_question_results, không cần lưu thêm.
--
-- Dữ liệu cũ không phải sửa: câu hỏi đang trỏ chủ đề tầng bài (parent_id null) thì
-- coalesce(parent_id, id) trả về chính nó.
-- ============================================================


-- ---------- 1. Cây chủ đề ----------
alter table public.question_topics
  add column if not exists parent_id bigint references public.question_topics (id) on delete cascade;

create index if not exists question_topics_parent_idx
  on public.question_topics (parent_id, sort_order);

-- Tên vẫn phải duy nhất trong một khối: nhãn trên câu hỏi lưu bằng TÊN
-- (exams.questions[i].topic) rồi mới tra ra id, nên hai YCCĐ trùng tên trong cùng lớp
-- là mất dấu. Đặt tên YCCĐ đủ tự mô tả ("Viết phương trình dao động điều hoà"), đừng
-- đặt kiểu "Bài tập vận dụng".
-- (unique (subject_code, grade, name) đã có từ migration exam-analytics — giữ nguyên.)

-- Chỉ hai tầng, và YCCĐ luôn nằm đúng bài của chủ đề cha.
create or replace function public.question_topic_tree_guard()
returns trigger language plpgsql set search_path = public
as $$
declare p public.question_topics%rowtype;
begin
  if new.parent_id is null then
    return new;
  end if;
  if new.parent_id = new.id then
    raise exception 'Chủ đề không thể là cha của chính nó';
  end if;
  select * into p from public.question_topics where id = new.parent_id;
  if not found then
    raise exception 'Không có chủ đề cha #%', new.parent_id;
  end if;
  if p.parent_id is not null then
    raise exception 'Danh mục chủ đề chỉ hai tầng: bài học → yêu cầu cần đạt';
  end if;
  if exists (select 1 from public.question_topics c where c.parent_id = new.id) then
    raise exception 'Chủ đề "%" đang có yêu cầu cần đạt con nên không thể thành con của chủ đề khác', new.name;
  end if;
  -- YCCĐ thuộc về bài của cha: khối, chương, bài lấy theo cha để nút "Ôn lại" luôn đúng.
  new.subject_code := p.subject_code;
  new.grade := p.grade;
  new.chapter_id := p.chapter_id;
  new.lesson_id := p.lesson_id;
  return new;
end; $$;

drop trigger if exists trg_question_topic_tree on public.question_topics;
create trigger trg_question_topic_tree before insert or update on public.question_topics
  for each row execute function public.question_topic_tree_guard();

-- Cha đổi bài -> con theo cha.
create or replace function public.question_topic_sync_children()
returns trigger language plpgsql set search_path = public
as $$
begin
  if new.parent_id is null and (
       new.chapter_id is distinct from old.chapter_id
    or new.lesson_id is distinct from old.lesson_id
    or new.grade is distinct from old.grade
  ) then
    update public.question_topics c
      set chapter_id = new.chapter_id,
          lesson_id = new.lesson_id,
          grade = new.grade
    where c.parent_id = new.id;
  end if;
  return null;
end; $$;

drop trigger if exists trg_question_topic_sync_children on public.question_topics;
create trigger trg_question_topic_sync_children after update on public.question_topics
  for each row execute function public.question_topic_sync_children();


-- ---------- 2. Mục phụ đạo gom lên tầng bài ----------
-- Khác bản cũ đúng một chỗ: agg gom theo coalesce(t.parent_id, q.topic_id).
create or replace function public.refresh_tutoring_needs(p_student uuid)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  v_class bigint;
  v_window int := 2;        -- xét 2 bài gần nhất
  v_min_q int := 3;         -- cần ít nhất 3 câu cùng chủ đề mới dám kết luận
  v_need_pct numeric := 50; -- sai từ 50% -> cần phụ đạo
  v_clear_pct numeric := 25;-- sai ≤ 25% (đúng ≥ 75%) -> coi như đã khắc phục
begin
  select uc.class_id into v_class
  from public.user_classes uc
  where uc.user_id = p_student and uc.status = 'active'
  order by uc.class_id desc
  limit 1;

  -- (a) mở / cập nhật mục còn hổng
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
  insert into public.tutoring_needs
    (student_id, class_id, topic_id, form, wrong, total, pct, source, status)
  select p_student, v_class, a.topic_id, a.form, a.wrong, a.total,
         round(a.wrong * 100.0 / a.total)::int, 'auto', 'open'
  from agg a
  where a.total >= v_min_q and a.wrong * 100.0 / a.total >= v_need_pct
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

  -- (b) làm đúng lại -> đóng mục
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


-- ---------- 3. Trợ giảng tick một YCCĐ -> đóng mục ở tầng bài ----------
create or replace function public.trg_tutoring_covered()
returns trigger language plpgsql security definer set search_path = public
as $$
declare v_topic bigint;
begin
  select coalesce(t.parent_id, t.id) into v_topic
  from public.question_topics t where t.id = new.topic_id;
  v_topic := coalesce(v_topic, new.topic_id);

  update public.tutoring_needs n
    set status = case when n.status in ('open', 'assigned') then 'tutored' else n.status end,
        tutored_at = coalesce(n.tutored_at, now())
  where n.student_id = new.student_id and n.topic_id = v_topic
    and n.status in ('open', 'assigned');
  return new;
end; $$;


-- ---------- 4. Chi tiết: em hổng những yêu cầu cần đạt nào ----------
-- Dùng cho tab Phụ đạo của thầy, phiếu của trợ giảng và trang kết quả của học sinh:
-- với mỗi mục phụ đạo (tầng bài), liệt kê YCCĐ con còn sai trong cửa sổ xét.
-- Nhận cả danh sách em để một màn hình cả lớp chỉ gọi đúng một lần.
-- security definer + tự kiểm quyền: trợ giảng đọc được exam_question_results nhưng
-- KHÔNG đọc được exam_results (chỉ thầy được phân công), nên hàm invoker sẽ trả rỗng
-- cho đúng người cần dùng nó nhất.
drop function if exists public.student_outcome_gaps(uuid, int);
create or replace function public.student_outcome_gaps(p_students uuid[], p_window int default 2)
returns table (
  student_id uuid,
  parent_topic_id bigint,
  topic_id bigint,
  topic_name text,
  form text,
  total int,
  wrong int
)
language sql stable security definer set search_path = public
as $$
  with students as (
    select s.id
    from unnest(coalesce(p_students, '{}'::uuid[])) as s(id)
    where s.id = auth.uid() or public.teaches_student(s.id)
  ),
  recent as (
    select er.student_id, er.exam_id, row_number() over (
             partition by er.student_id order by max(er.created_at) desc
           ) as rn
    from public.exam_results er
    join students s on s.id = er.student_id
    group by er.student_id, er.exam_id
  ),
  last_try as (
    select distinct on (er.student_id, er.exam_id) er.id
    from public.exam_results er
    join recent r on r.student_id = er.student_id and r.exam_id = er.exam_id
    where r.rn <= greatest(p_window, 1)
    order by er.student_id, er.exam_id, er.created_at desc
  )
  select q.student_id,
         coalesce(t.parent_id, q.topic_id) as parent_topic_id,
         q.topic_id,
         coalesce(t.name, q.topic_name) as topic_name,
         coalesce(nullif(q.form, ''), '') as form,
         (count(*))::int as total,
         (count(*) filter (where not q.is_correct))::int as wrong
  from public.exam_question_results q
  join last_try lt on lt.id = q.exam_result_id
  left join public.question_topics t on t.id = q.topic_id
  where q.topic_id is not null
  group by q.student_id, coalesce(t.parent_id, q.topic_id), q.topic_id,
           coalesce(t.name, q.topic_name), coalesce(nullif(q.form, ''), '')
  having count(*) filter (where not q.is_correct) > 0
  order by 1, 2, 7 desc, 6 desc;
$$;

grant execute on function public.student_outcome_gaps(uuid[], int) to authenticated;
