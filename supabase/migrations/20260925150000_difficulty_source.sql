-- ============================================================================
-- feat(ngân hàng câu hỏi): question_bank.difficulty_source ('gv'|'ai')
-- Phase 0 mức độ Dễ/TB/Khó (Agent A) — 25/9/2026.
-- ============================================================================
-- Vì sao: cột question_bank.difficulty đã có sẵn + đồng bộ 2 chiều đề <-> ngân
-- hàng đã deploy (docs/supabase-migration-question-bank-difficulty.sql), nhưng
-- không phân biệt được "AI gợi ý chưa duyệt" với "giáo viên tự xác nhận tay".
-- File này CHỈ thêm 1 cột nullable + vá 3 hàm trigger để đọc/ghi thêm cột đó ở
-- cả 2 chiều — không đổi hành vi khác, không nới RLS, giữ nguyên chế độ bảo mật
-- (SECURITY DEFINER / INVOKER) của từng hàm như bản gốc.
--
-- Giá trị 'gv'/'ai' chỉ có ý nghĩa khi difficulty khác rỗng; null = không rõ
-- nguồn (đề/câu gắn từ trước khi có tính năng này, hoặc soạn tay ngoài UI).
--
-- Cách chạy: Dashboard → SQL Editor → dán cả file, Run (1 transaction).
--   hoặc: supabase db query --linked -f supabase/migrations/20260925150000_difficulty_source.sql
-- KHÔNG dùng `supabase db push`. Idempotent — chạy lại được.
-- ============================================================================

begin;

-- ---------- 0. Cột mới ----------
alter table public.question_bank
  add column if not exists difficulty_source text
  check (difficulty_source is null or difficulty_source in ('gv', 'ai'));

comment on column public.question_bank.difficulty_source is
  'Nguồn nhãn difficulty: gv = giáo viên tự bấm chọn, ai = AI gợi ý chưa được xác nhận lại. NULL = không rõ nguồn (dữ liệu cũ).';

-- ---------- 1. Đăng đề -> ngân hàng: đọc thêm questions[].difficultySource ----------
-- Giữ nguyên chữ ký, volatility, SECURITY DEFINER, search_path của bản gốc
-- (docs/supabase-migration-question-bank-difficulty.sql) — chỉ thêm difficulty_source.
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
end; $$;

revoke execute on function public.sync_exam_to_bank(bigint) from public, anon, authenticated;


-- ---------- 2. Ngân hàng -> đề: đồng bộ ngược difficulty_source vào questions[].difficultySource ----------
create or replace function public.trg_bank_tags_to_exams()
returns trigger language plpgsql security definer set search_path = public
as $$
declare
  e record;
  v_patch jsonb;
begin
  if new.topic_name is not distinct from old.topic_name
     and new.form is not distinct from old.form
     and new.difficulty is not distinct from old.difficulty
     and new.difficulty_source is not distinct from old.difficulty_source then
    return null;
  end if;
  v_patch := jsonb_build_object(
    'topic', new.topic_name,
    'form', new.form,
    'difficulty', new.difficulty,
    'difficultySource', new.difficulty_source
  );
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
create trigger trg_bank_tags_to_exams
  after update of topic_name, form, difficulty, difficulty_source on public.question_bank
  for each row execute function public.trg_bank_tags_to_exams();

-- ---------- 3. Sửa trực tiếp dòng ngân hàng: đồng bộ difficulty_source vào question jsonb của
--    CHÍNH dòng đó (giữ nguyên: KHÔNG có security definer trong bản gốc — before-trigger chạy
--    quyền người gọi, không nới RLS). ----------
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
  new.question := new.question || jsonb_build_object(
    'topic', new.topic_name,
    'form', new.form,
    'difficulty', new.difficulty,
    'difficultySource', new.difficulty_source
  );
  return new;
end; $$;

drop trigger if exists trg_bank_touch on public.question_bank;
create trigger trg_bank_touch before update on public.question_bank
  for each row execute function public.trg_bank_touch();

commit;

-- ---------- Sau khi chạy xong file này ----------
-- Backfill nốt 3534 câu question_bank.difficulty = '' còn thiếu (script có sẵn, đã sửa để ghi
-- kèm difficulty_source = 'ai'):
--   npx tsx scripts/backfill-question-bank-difficulty.mts
-- Xem feat/DIFFICULTY_REPORT.md để biết chi tiết + rủi ro trước khi chạy trên DB thật.
