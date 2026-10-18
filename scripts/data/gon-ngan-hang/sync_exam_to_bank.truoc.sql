CREATE OR REPLACE FUNCTION public.sync_exam_to_bank(p_exam_id bigint)
 RETURNS integer
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
declare
  v_exam public.exams%rowtype;
  v_grade text := '';
  v_subject text := 'vat-ly';
  v_n int := 0;
  r record;
  v_topic public.question_topics%rowtype;
  v_topic_id bigint;
  v_topic_name text;
  v_q_grade text;
  v_q_subject text;
  v_difficulty text;
  v_difficulty_source text;
begin
  select * into v_exam from public.exams where id = p_exam_id;
  if not found then
    return 0;
  end if;
  if jsonb_typeof(v_exam.questions) <> 'array' then
    return 0;
  end if;

  -- Khối của đề: theo lớp được gán (exam_classes → classes.name có chữ số).
  select substring(c.name from '\d+') into v_grade
  from public.exam_classes ec
  join public.classes c on c.id = ec.class_id
  where ec.exam_id = p_exam_id and c.name ~ '\d'
  order by c.sort_order
  limit 1;
  v_grade := coalesce(v_grade, '');

  for r in
    select q.value as q, (q.ordinality - 1)::int as idx
    from jsonb_array_elements(v_exam.questions) with ordinality as q(value, ordinality)
  loop
    if jsonb_typeof(r.q) <> 'object' or coalesce(r.q->>'question', '') = '' then
      continue;
    end if;

    v_topic_name := regexp_replace(btrim(coalesce(r.q->>'topic', '')), '\s+', ' ', 'g');
    v_topic_id := null;
    v_q_grade := v_grade;
    v_q_subject := v_subject;
    if v_topic_name <> '' then
      -- Ưu tiên đúng khối của đề; không có thì khớp tên ở khối bất kì (đề chưa gán lớp).
      select * into v_topic from public.question_topics t
      where lower(t.name) = lower(v_topic_name)
        and (v_grade = '' or t.grade = v_grade)
      order by (t.grade = v_grade) desc, t.id
      limit 1;
      if found then
        v_topic_id := v_topic.id;
        v_topic_name := v_topic.name;
        v_q_grade := v_topic.grade;
        v_q_subject := v_topic.subject_code;
      end if;
    end if;

    v_difficulty := case when r.q->>'difficulty' in ('de', 'trung-binh', 'kho') then r.q->>'difficulty' else '' end;
    v_difficulty_source := case when r.q->>'difficultySource' in ('gv', 'ai') then r.q->>'difficultySource' else null end;

    insert into public.question_bank as b (
      subject_code, grade, topic_id, topic_name, form, difficulty, difficulty_source, qtype, question,
      content_hash, source_exam_id, source_index
    ) values (
      v_q_subject,
      v_q_grade,
      v_topic_id,
      v_topic_name,
      case when r.q->>'form' in ('ly_thuyet', 'bai_tap') then r.q->>'form' else '' end,
      v_difficulty,
      v_difficulty_source,
      coalesce(r.q->>'type', 'multiple_choice'),
      r.q,
      public.question_content_hash(r.q),
      p_exam_id,
      r.idx
    )
    on conflict (content_hash) do update set
      question   = excluded.question,
      -- Nhãn: lần đăng sau ghi đè nếu có nhãn; đề không nhãn thì giữ nhãn cũ.
      topic_id   = coalesce(excluded.topic_id, b.topic_id),
      topic_name = case when excluded.topic_name <> '' then excluded.topic_name else b.topic_name end,
      form       = case when excluded.form <> '' then excluded.form else b.form end,
      difficulty = case when excluded.difficulty <> '' then excluded.difficulty else b.difficulty end,
      -- Nguồn đi kèm difficulty: chỉ ghi đè khi đề mới có cả difficulty lẫn nguồn; đề cũ không
      -- ghi nguồn (đăng lại không đổi mức độ) thì giữ nguyên nguồn đã có trong ngân hàng.
      difficulty_source = case
        when excluded.difficulty <> '' and excluded.difficulty_source is not null then excluded.difficulty_source
        else b.difficulty_source
      end,
      grade      = case when excluded.grade <> '' then excluded.grade else b.grade end,
      subject_code = excluded.subject_code,
      qtype      = excluded.qtype,
      updated_at = now();
    v_n := v_n + 1;
  end loop;
  return v_n;
end; $function$
;
