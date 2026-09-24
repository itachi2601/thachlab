-- ============================================================
-- NGÂN HÀNG CÂU HỎI — vá: đồng bộ cột difficulty (Dễ/Trung bình/Khó)
-- ============================================================
-- Chạy SAU docs/supabase-migration-question-bank.sql.
-- Idempotent — chạy lại được.
--
-- Vì sao cần: cột question_bank.difficulty đã có sẵn từ bản gốc, nhưng
-- sync_exam_to_bank() và trg_bank_tags_to_exams() chưa từng đọc/ghi nó — đề đã
-- đăng có gắn "Mức độ: …" ở trang Đăng đề vẫn rơi mất khi vào ngân hàng, và sửa
-- mức độ trong /quan-tri/ngan-hang-cau-hoi không đồng bộ ngược lại đề gốc.
-- File này vá hai hàm đó (giữ nguyên mọi hành vi khác) rồi CHẠY LẠI backfill:
--   docs/supabase-migration-question-bank-backfill.sql
-- để câu đã có "Mức độ:" trong đề nhưng đăng trước khi vá này chạy cũng được nạp.
-- ============================================================

-- ---------- 3. Đồng bộ một đề vào ngân hàng (thêm difficulty) ----------
create or replace function public.sync_exam_to_bank(p_exam_id bigint)
returns int
language plpgsql security definer set search_path = public
as $$
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

    insert into public.question_bank as b (
      subject_code, grade, topic_id, topic_name, form, difficulty, qtype, question,
      content_hash, source_exam_id, source_index
    ) values (
      v_q_subject,
      v_q_grade,
      v_topic_id,
      v_topic_name,
      case when r.q->>'form' in ('ly_thuyet', 'bai_tap') then r.q->>'form' else '' end,
      v_difficulty,
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
      grade      = case when excluded.grade <> '' then excluded.grade else b.grade end,
      subject_code = excluded.subject_code,
      qtype      = excluded.qtype,
      updated_at = now();
    v_n := v_n + 1;
  end loop;
  return v_n;
end; $$;

revoke execute on function public.sync_exam_to_bank(bigint) from public, anon, authenticated;


-- ---------- 6. Gắn nhãn từ trang ngân hàng → đồng bộ ngược vào các đề (thêm difficulty) ----------
create or replace function public.trg_bank_tags_to_exams()
returns trigger language plpgsql security definer set search_path = public
as $$
declare
  e record;
  v_patch jsonb;
begin
  if new.topic_name is not distinct from old.topic_name
     and new.form is not distinct from old.form
     and new.difficulty is not distinct from old.difficulty then
    return null;
  end if;
  v_patch := jsonb_build_object('topic', new.topic_name, 'form', new.form, 'difficulty', new.difficulty);
  for e in
    select ex.id, q.ordinality - 1 as idx
    from public.exams ex,
         jsonb_array_elements(ex.questions) with ordinality as q(value, ordinality)
    where public.question_content_hash(q.value) = new.content_hash
  loop
    update public.exams
      set questions = jsonb_set(questions, array[e.idx::text], (questions -> e.idx::int) || v_patch)
      where id = e.id;
  end loop;
  return null;
end; $$;

drop trigger if exists trg_bank_tags_to_exams on public.question_bank;
create trigger trg_bank_tags_to_exams after update of topic_name, form, difficulty on public.question_bank
  for each row execute function public.trg_bank_tags_to_exams();

-- Cập nhật question jsonb khi thầy đổi nhãn/mức độ trực tiếp trên dòng ngân hàng.
create or replace function public.trg_bank_touch()
returns trigger language plpgsql set search_path = public
as $$
declare t public.question_topics%rowtype;
begin
  new.updated_at := now();
  new.topic_name := regexp_replace(btrim(coalesce(new.topic_name, '')), '\s+', ' ', 'g');
  -- topic_id theo tên nếu app chỉ gửi tên
  if new.topic_name <> '' and (new.topic_id is null or new.topic_name is distinct from old.topic_name) then
    select * into t from public.question_topics x
    where lower(x.name) = lower(new.topic_name)
      and (new.grade = '' or x.grade = new.grade)
    order by (x.grade = new.grade) desc, x.id
    limit 1;
    if found then
      new.topic_id := t.id;
      new.topic_name := t.name;
      new.grade := t.grade;
      new.subject_code := t.subject_code;
    else
      new.topic_id := null;
    end if;
  end if;
  if new.topic_name = '' then
    new.topic_id := null;
  end if;
  new.question := new.question || jsonb_build_object('topic', new.topic_name, 'form', new.form, 'difficulty', new.difficulty);
  return new;
end; $$;

drop trigger if exists trg_bank_touch on public.question_bank;
create trigger trg_bank_touch before update on public.question_bank
  for each row execute function public.trg_bank_touch();


-- ---------- Sau khi chạy xong file này ----------
-- Chạy lại (an toàn, chỉ upsert theo content_hash):
--   docs/supabase-migration-question-bank-backfill.sql
