-- ============================================================
-- NGÂN HÀNG CÂU HỎI — gắn ảnh (đồ thị / hình vẽ) cho một câu đã có trong ngân hàng
-- ============================================================
-- Chạy SAU docs/supabase-migration-question-bank.sql. Idempotent.
--
-- Vấn đề: nhiều câu nhắc "đồ thị / như hình vẽ" nhưng lúc đăng bị mất hình. Thầy tải ảnh
-- ngay trên /quan-tri/ngan-hang-cau-hoi (mục "Nhắc hình, thiếu ảnh"); trang upload ảnh lên
-- Storage rồi gọi RPC này. RPC phải làm 2 việc trong MỘT transaction:
--   1. Sửa question_bank.question (chèn <img> vào câu dẫn) và tính lại content_hash.
--   2. Sửa đúng câu đó trong exams.questions của MỌI đề đang dùng (so theo hash cũ) — vì trang
--      làm bài đọc từ exams.questions, không đọc từ ngân hàng.
-- Thứ tự 1 → 2 là bắt buộc: trigger trg_exams_sync_bank chạy sau bước 2 sẽ upsert theo hash
-- MỚI, gặp đúng dòng vừa sửa ở bước 1 → cập nhật tại chỗ, không sinh dòng trùng.
-- Nếu câu dẫn còn mốc "⟦ảnh WMF⟧" / "⟦hình vẽ Word⟧" / "⟦hình TikZ⟧" thì ảnh thay vào mốc đầu
-- tiên; không có mốc thì nối ảnh vào cuối câu dẫn.
-- ============================================================

create or replace function public.bank_set_question_figure(p_bank_id bigint, p_img_html text)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  b public.question_bank%rowtype;
  v_old_hash text;
  v_target_hash text;
  v_stem text;
  v_new_q jsonb;
  v_dup bigint;
  v_n int := 0;
  e record;
  c_marks constant text := '⟦ảnh WMF⟧|⟦hình vẽ Word⟧|⟦hình TikZ⟧';
begin
  if not (public.is_admin() or exists (
    select 1 from public.profiles p
    where p.id = auth.uid() and p.role = 'instructor' and p.admin_area = 'thpt'
  )) then
    raise exception 'Chỉ giáo viên mới gắn ảnh được.';
  end if;
  if p_img_html is null or btrim(p_img_html) = '' or p_img_html !~* '<img\s' then
    raise exception 'p_img_html phải là một thẻ <img>.';
  end if;

  select * into b from public.question_bank where id = p_bank_id for update;
  if not found then
    raise exception 'Không thấy câu #% trong ngân hàng.', p_bank_id;
  end if;

  v_old_hash := b.content_hash;
  v_stem := coalesce(b.question->>'question', '');
  if v_stem ~ c_marks then
    v_stem := regexp_replace(v_stem, c_marks, p_img_html);      -- chỉ mốc đầu tiên
  else
    v_stem := rtrim(v_stem) || ' ' || p_img_html;
  end if;
  v_new_q := b.question || jsonb_build_object('question', v_stem);

  -- Hash đích = hash của câu ĐÃ SỬA theo bản nằm trong đề (nếu có đề đang dùng): trigger
  -- trg_exams_sync_bank sau đó upsert đúng vào dòng này. Lưu ý bản trong ngân hàng có thể
  -- mang thêm khoá "difficulty" (trg_bank_touch chèn vào) nên hash tính từ bản ngân hàng
  -- có thể lệch với bản trong đề — vì vậy ưu tiên hash theo đề.
  select public.question_content_hash(q.value || jsonb_build_object('question', v_stem))
    into v_target_hash
  from public.exams ex,
       jsonb_array_elements(ex.questions) with ordinality as q(value, ordinality)
  where jsonb_typeof(ex.questions) = 'array'
    and public.question_content_hash(q.value) = v_old_hash
  order by ex.id
  limit 1;

  select id into v_dup from public.question_bank
    where content_hash = coalesce(v_target_hash, public.question_content_hash(v_new_q)) and id <> p_bank_id;
  if found then
    raise exception 'Ngân hàng đã có câu y hệt kèm ảnh này (#%). Lưu trữ một trong hai câu rồi thử lại.', v_dup;
  end if;

  update public.question_bank set question = v_new_q where id = p_bank_id;
  -- Tính hash sau khi trigger trg_bank_touch đã chèn topic/form/difficulty vào question.
  update public.question_bank
    set content_hash = coalesce(v_target_hash, public.question_content_hash(question))
    where id = p_bank_id;

  for e in
    select ex.id, (q.ordinality - 1)::int as idx
    from public.exams ex,
         jsonb_array_elements(ex.questions) with ordinality as q(value, ordinality)
    where jsonb_typeof(ex.questions) = 'array'
      and public.question_content_hash(q.value) = v_old_hash
  loop
    update public.exams
      set questions = jsonb_set(questions, array[e.idx::text], (questions -> e.idx) || jsonb_build_object('question', v_stem))
      where id = e.id;
    v_n := v_n + 1;
  end loop;

  select * into b from public.question_bank where id = p_bank_id;
  return jsonb_build_object('question', b.question, 'content_hash', b.content_hash, 'exams_updated', v_n);
end; $$;

revoke all on function public.bank_set_question_figure(bigint, text) from public, anon;
grant execute on function public.bank_set_question_figure(bigint, text) to authenticated;

comment on function public.bank_set_question_figure(bigint, text) is
  'Gắn <img> vào câu dẫn của một câu trong ngân hàng và vào mọi exams.questions đang dùng câu đó (theo content_hash cũ).';
