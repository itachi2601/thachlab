-- ============================================================
-- NGÂN HÀNG CÂU HỎI — cờ "không cần hình" + RPC gắn hình nhận cả SVG (AI vẽ)
-- ============================================================
-- Chạy SAU docs/supabase-migration-question-bank-figure.sql. Idempotent.
-- figure_not_needed: thầy đánh dấu câu nhắc "đồ thị/hình vẽ" nhưng thực ra là câu lý thuyết,
-- không cần hình — mục "Nhắc hình, thiếu ảnh" bỏ qua các câu này.
-- ============================================================

alter table public.question_bank add column if not exists figure_not_needed boolean not null default false;
comment on column public.question_bank.figure_not_needed is 'Thầy xác nhận câu không cần hình dù câu dẫn nhắc đồ thị/hình vẽ.';

-- Cho phép p_img_html là <svg …> inline (AI vẽ) bên cạnh <img>.
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
  if p_img_html is null or btrim(p_img_html) = '' or p_img_html !~* '^\s*<(img|svg)[\s>]' then
    raise exception 'p_img_html phải là một thẻ <img> hoặc <svg>.';
  end if;
  if p_img_html ~* '<script|javascript:|on[a-z]+\s*=|<foreignObject' then
    raise exception 'Nội dung hình không hợp lệ.';
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

  update public.question_bank set question = v_new_q, figure_not_needed = false where id = p_bank_id;
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
