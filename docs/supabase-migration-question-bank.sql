-- ============================================================
-- NGÂN HÀNG CÂU HỎI — gom mọi câu của đề kiểm tra / thi / luyện tập / BTVN
-- ============================================================
-- Chạy SAU:
--   docs/supabase-migration-exam-analytics.sql   (question_topics)
--   docs/supabase-migration-topic-outcomes.sql   (question_topics.parent_id — yêu cầu cần đạt)
--   docs/supabase-migration-classes.sql          (exam_classes)
-- Idempotent — chạy lại được. Chạy xong file này thì chạy tiếp
--   docs/supabase-migration-question-bank-backfill.sql   (nạp lại toàn bộ đề đang có)
-- Nếu báo "deadlock detected": transaction đã bị huỷ, chưa ghi gì — chạy lại là được.
-- Trước khi chạy: đóng tab SQL Editor khác đang chạy dở, đóng trang admin đang mở
-- (nhất là dev local đang mở /quan-tri/ngan-hang-cau-hoi), rồi bấm Run lại.
--
-- CÁCH HOẠT ĐỘNG
-- Câu hỏi vẫn nằm trong exams.questions (jsonb) như trước — mọi trang làm bài,
-- chấm điểm, phân tích không đổi. Bảng question_bank là "bản sao có chỉ mục" của
-- từng câu: mỗi lần một đề được tạo/sửa, trigger tách câu ra và upsert vào ngân hàng.
-- Khoá chống trùng là content_hash = md5 của nội dung câu (bỏ nhãn topic/form và lời
-- giải): cùng một câu xuất hiện ở 3 đề chỉ có 1 dòng trong ngân hàng, nhãn/lời giải
-- lấy theo lần đăng gần nhất.
--
-- Ngân hàng xếp theo năng lực cần đạt: topic_id trỏ question_topics (tầng bài hoặc
-- yêu cầu cần đạt). Câu chưa gắn nhãn (topic_id null) gom vào mục "Chưa gắn nhãn"
-- để thầy gắn dần ngay trên trang /quan-tri/ngan-hang-cau-hoi.
-- ============================================================


-- ---------- 1. Bảng ----------
create table if not exists public.question_bank (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  subject_code text not null default 'vat-ly',
  grade text not null default '',                 -- '9' | '10' | '11' | '12' | '' (chưa rõ)
  topic_id bigint references public.question_topics (id) on delete set null,
  topic_name text not null default '',
  form text not null default '',                  -- 'ly_thuyet' | 'bai_tap' | ''
  qtype text not null,                            -- multiple_choice | true_false | short_answer | essay
  difficulty text not null default ''
    check (difficulty in ('', 'de', 'trung-binh', 'kho')),
  question jsonb not null,                        -- trọn câu (ExamQuestion), kể cả nhãn + lời giải
  content_hash text not null unique,
  source_exam_id bigint references public.exams (id) on delete set null, -- đề đầu tiên chứa câu này
  source_index int,                               -- vị trí (0-based) trong đề đó
  archived boolean not null default false,        -- ẩn khỏi danh sách bốc câu, không xoá
  note text not null default ''
);

create index if not exists question_bank_topic_idx on public.question_bank (topic_id, archived);
create index if not exists question_bank_grade_idx on public.question_bank (subject_code, grade, archived);
create index if not exists question_bank_source_idx on public.question_bank (source_exam_id);

comment on table public.question_bank is
  'Ngân hàng câu hỏi: mỗi câu trong exams.questions một dòng, chống trùng theo content_hash, xếp theo question_topics.';

alter table public.question_bank enable row level security;

-- Chỉ giáo viên (admin hoặc giảng viên THPT) — học sinh không đọc được đáp án trong ngân hàng.
drop policy if exists "staff manage question bank" on public.question_bank;
create policy "staff manage question bank" on public.question_bank
  for all to authenticated
  using (public.is_admin() or exists (
    select 1 from public.profiles p
    where p.id = auth.uid() and p.role = 'instructor' and p.admin_area = 'thpt'
  ))
  with check (public.is_admin() or exists (
    select 1 from public.profiles p
    where p.id = auth.uid() and p.role = 'instructor' and p.admin_area = 'thpt'
  ));


-- ---------- 2. Hàm băm nội dung ----------
-- Bỏ nhãn (topic, form) và lời giải: đổi nhãn hay bổ sung lời giải không tạo câu mới.
-- jsonb::text của Postgres sắp xếp khoá ổn định nên md5 ổn định.
create or replace function public.question_content_hash(q jsonb)
returns text language sql immutable
as $$
  select md5((q - 'topic' - 'form' - 'explanation' - 'bank_id')::text);
$$;


-- ---------- 3. Đồng bộ một đề vào ngân hàng ----------
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

    insert into public.question_bank as b (
      subject_code, grade, topic_id, topic_name, form, qtype, question,
      content_hash, source_exam_id, source_index
    ) values (
      v_q_subject,
      v_q_grade,
      v_topic_id,
      v_topic_name,
      case when r.q->>'form' in ('ly_thuyet', 'bai_tap') then r.q->>'form' else '' end,
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
      grade      = case when excluded.grade <> '' then excluded.grade else b.grade end,
      subject_code = excluded.subject_code,
      qtype      = excluded.qtype,
      updated_at = now();
    v_n := v_n + 1;
  end loop;
  return v_n;
end; $$;

-- Chỉ trigger (security definer) gọi; app không gọi trực tiếp.
revoke execute on function public.sync_exam_to_bank(bigint) from public, anon, authenticated;


-- ---------- 4. Trigger: đề tạo/sửa → ngân hàng cập nhật ----------
create or replace function public.trg_exams_sync_bank()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  if tg_op = 'INSERT' or new.questions is distinct from old.questions then
    perform public.sync_exam_to_bank(new.id);
  end if;
  return null;
end; $$;

drop trigger if exists trg_exams_sync_bank on public.exams;
create trigger trg_exams_sync_bank after insert or update of questions on public.exams
  for each row execute function public.trg_exams_sync_bank();

-- Gán lớp cho đề SAU khi tạo đề (trang Đăng đề làm vậy) → cập nhật khối cho câu chưa rõ khối.
create or replace function public.trg_exam_classes_sync_bank()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  perform public.sync_exam_to_bank(new.exam_id);
  return null;
end; $$;

drop trigger if exists trg_exam_classes_sync_bank on public.exam_classes;
create trigger trg_exam_classes_sync_bank after insert on public.exam_classes
  for each row execute function public.trg_exam_classes_sync_bank();


-- ---------- 5. Đổi tên / gộp chủ đề → tên trên câu theo kịp ----------
create or replace function public.trg_question_topics_rename_bank()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  if new.name is distinct from old.name then
    update public.question_bank
      set topic_name = new.name,
          question = question || jsonb_build_object('topic', new.name),
          updated_at = now()
      where topic_id = new.id;
  end if;
  return null;
end; $$;

drop trigger if exists trg_question_topics_rename_bank on public.question_topics;
create trigger trg_question_topics_rename_bank after update on public.question_topics
  for each row execute function public.trg_question_topics_rename_bank();


-- ---------- 6. Gắn nhãn từ trang ngân hàng → đồng bộ ngược vào các đề ----------
-- Thầy sửa topic/form của một câu trong ngân hàng thì mọi đề đang chứa đúng câu đó
-- (cùng content_hash) cũng nhận nhãn mới, để phân tích sau này gom đúng chủ đề.
create or replace function public.trg_bank_tags_to_exams()
returns trigger language plpgsql security definer set search_path = public
as $$
declare
  e record;
  v_patch jsonb;
begin
  if new.topic_name is not distinct from old.topic_name
     and new.form is not distinct from old.form then
    return null;
  end if;
  v_patch := jsonb_build_object('topic', new.topic_name, 'form', new.form);
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
create trigger trg_bank_tags_to_exams after update of topic_name, form on public.question_bank
  for each row execute function public.trg_bank_tags_to_exams();

-- Cập nhật question jsonb khi thầy đổi nhãn/đáp án trực tiếp trên dòng ngân hàng.
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
  new.question := new.question || jsonb_build_object('topic', new.topic_name, 'form', new.form);
  return new;
end; $$;

drop trigger if exists trg_bank_touch on public.question_bank;
create trigger trg_bank_touch before update on public.question_bank
  for each row execute function public.trg_bank_touch();


-- ---------- 7. Thống kê theo chủ đề (cho cây năng lực) ----------
create or replace view public.question_bank_topic_counts with (security_invoker = true) as
  select subject_code, grade, topic_id, archived, count(*)::int as n
  from public.question_bank
  group by subject_code, grade, topic_id, archived;

grant select on public.question_bank_topic_counts to authenticated;


-- ---------- 8. NẠP LẠI toàn bộ đề đang có ----------
-- Chạy RIÊNG, sau khi file này chạy xong: docs/supabase-migration-question-bank-backfill.sql
-- (tách ra để bước nạp lại — đọc toàn bộ exams — không nằm chung transaction với
-- các lệnh CREATE TRIGGER cần khoá độc quyền bảng exams → tránh deadlock với app đang chạy).
