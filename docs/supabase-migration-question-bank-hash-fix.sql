-- ============================================================
-- NGÂN HÀNG CÂU HỎI — vá hàm băm (bỏ khoá difficulty) + gộp câu trùng
-- ============================================================
-- Chạy SAU docs/supabase-migration-question-bank-difficulty.sql. Chạy lại được (idempotent):
-- lần 2 không còn dòng trùng, hash đã đúng, không đổi gì.
--
-- LỖI: trg_bank_touch (bản difficulty) chèn khoá "difficulty" vào question_bank.question,
-- nhưng question_content_hash() không loại khoá này → content_hash lưu ≠ hash tính lại từ
-- bản ngân hàng. Mỗi lần đề đăng lại, sync_exam_to_bank băm câu trong đề (không có difficulty)
-- ra hash KHÁC → insert dòng mới thay vì cập nhật → ngân hàng phình câu trùng (25/9/2026:
-- 10 768 dòng nhưng chỉ 7 203 nội dung khác nhau).
--
-- SỬA: (1) hàm băm loại thêm 'difficulty'; (2) nhóm các dòng theo hash mới, giữ 1 dòng mỗi nhóm
-- (ưu tiên đã gắn năng lực > có mức độ > chưa lưu trữ > id nhỏ nhất), gộp nhãn/ghi chú từ các dòng
-- bị xoá vào dòng giữ; (3) ánh xạ id cũ → id giữ trong rank_fix_attempts / tutoring_exit_attempts;
-- (4) xoá dòng trùng; (5) tính lại content_hash toàn bảng. Có bảng backup để hoàn tác.
-- ============================================================

begin;

-- 0. Backup (không đụng nếu đã có)
create table if not exists public.question_bank_backup_20260925 as
  select * from public.question_bank;

-- 1. Hàm băm mới: nhãn (topic/form/difficulty), lời giải, bank_id không tạo câu mới
create or replace function public.question_content_hash(q jsonb)
returns text language sql immutable
as $$
  select md5((q - 'topic' - 'form' - 'explanation' - 'bank_id' - 'difficulty')::text);
$$;

-- Tạm tắt trigger đẩy nhãn vào đề (quét toàn bộ exams mỗi dòng — chậm và không cần khi gộp)
alter table public.question_bank disable trigger trg_bank_tags_to_exams;

-- 2. Hash mới của từng dòng + dòng giữ lại cho mỗi hash
create temp table qb_new on commit drop as
  select b.id, public.question_content_hash(b.question) as new_hash
  from public.question_bank b;
create index on qb_new (new_hash);

create temp table qb_keep on commit drop as
  select distinct on (n.new_hash) n.new_hash, b.id as keep_id
  from qb_new n join public.question_bank b on b.id = n.id
  order by n.new_hash,
           (b.topic_id is not null) desc,
           (b.difficulty <> '') desc,
           (not b.archived) desc,
           b.id;

create temp table qb_map on commit drop as
  select n.id as old_id, k.keep_id
  from qb_new n join qb_keep k on k.new_hash = n.new_hash
  where n.id <> k.keep_id;

-- 3. Gộp nhãn / ghi chú từ dòng sắp xoá vào dòng giữ (chỉ điền chỗ dòng giữ còn trống)
update public.question_bank k set
  topic_id   = coalesce(k.topic_id, m.topic_id),
  topic_name = case when k.topic_id is not null then k.topic_name
                    when m.topic_id is not null then m.topic_name
                    when k.topic_name <> '' then k.topic_name
                    else m.any_topic_name end,
  form       = case when k.form <> '' then k.form else m.form end,
  difficulty = case when k.difficulty <> '' then k.difficulty else m.difficulty end,
  grade      = case when k.grade <> '' then k.grade else m.grade end,
  archived   = k.archived and m.all_archived,
  note       = concat_ws(' | ', nullif(k.note, ''), m.notes)
from (
  select mp.keep_id,
    (array_agg(b.topic_id   order by b.updated_at desc) filter (where b.topic_id is not null))[1] as topic_id,
    coalesce((array_agg(b.topic_name order by b.updated_at desc) filter (where b.topic_id is not null))[1], '') as topic_name,
    coalesce((array_agg(b.topic_name order by b.updated_at desc) filter (where b.topic_name <> ''))[1], '') as any_topic_name,
    coalesce((array_agg(b.form       order by b.updated_at desc) filter (where b.form <> ''))[1], '') as form,
    coalesce((array_agg(b.difficulty order by b.updated_at desc) filter (where b.difficulty <> ''))[1], '') as difficulty,
    coalesce((array_agg(b.grade      order by b.updated_at desc) filter (where b.grade <> ''))[1], '') as grade,
    bool_and(b.archived) as all_archived,
    string_agg(distinct nullif(b.note, ''), ' | ') as notes
  from qb_map mp join public.question_bank b on b.id = mp.old_id
  group by mp.keep_id
) m
where k.id = m.keep_id;

-- 4. Ánh xạ id cũ → id giữ ở các bảng lưu mảng id câu ngân hàng
do $$
declare t text;
begin
  foreach t in array array['public.rank_fix_attempts', 'public.tutoring_exit_attempts'] loop
    if to_regclass(t) is null then continue; end if;
    execute format($f$
      update %s a
      set question_ids = (
        select coalesce(array_agg(coalesce(mp.keep_id, x.id) order by x.ord), '{}')
        from unnest(a.question_ids) with ordinality as x(id, ord)
        left join qb_map mp on mp.old_id = x.id)
      where a.question_ids && (select coalesce(array_agg(old_id), '{}') from qb_map)
    $f$, t);
  end loop;
end $$;

-- 5. Xoá dòng trùng
delete from public.question_bank b using qb_map mp where b.id = mp.old_id;

-- 6. Tính lại content_hash theo hàm mới (trigger touch vẫn chạy, giữ question đồng bộ nhãn)
update public.question_bank b
  set content_hash = n.new_hash
  from qb_new n
  where n.id = b.id and b.content_hash <> n.new_hash;

alter table public.question_bank enable trigger trg_bank_tags_to_exams;

-- 7. Kiểm tra: hash duy nhất và khớp hàm băm; không còn id mồ côi trong bảng attempts
do $$
declare c_all int; c_distinct int; c_bad int;
begin
  select count(*), count(distinct content_hash) into c_all, c_distinct from public.question_bank;
  if c_all <> c_distinct then raise exception 'content_hash chưa duy nhất (% dòng, % hash)', c_all, c_distinct; end if;
  select count(*) into c_bad from public.question_bank where content_hash <> public.question_content_hash(question);
  if c_bad > 0 then raise exception '% dòng có content_hash lệch với hàm băm', c_bad; end if;
  if to_regclass('public.rank_fix_attempts') is not null then
    execute 'select count(*) from public.rank_fix_attempts a, unnest(a.question_ids) x(id) where not exists (select 1 from public.question_bank q where q.id = x.id)' into c_bad;
    if c_bad > 0 then raise exception 'rank_fix_attempts còn % id mồ côi', c_bad; end if;
  end if;
  raise notice 'OK: % dòng, hash duy nhất & khớp', c_all;
end $$;

commit;
