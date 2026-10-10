-- Thay ảnh CÔNG THỨC (MathType xuất thành PNG nhỏ, hay vỡ/mất) bằng chữ LaTeX `$…$` trong một câu ngân hàng
-- VÀ trong mọi exams.questions đang dùng câu đó — cùng cách bank_set_question_figure làm cho hình vẽ
-- (sửa ngân hàng trước, hash đích lấy theo bản trong đề để trigger trg_exams_sync_bank không sinh câu trùng).
-- p_map: [{"src": "<URL ảnh trong câu>", "text": "$\\vec{d}$"}, …]. Mỗi thẻ <img …src="URL"…> khớp src bị thay bằng text.
-- Gọi bởi scripts/thay-anh-cong-thuc.mts (service_role) — giáo viên admin cũng gọi được.

create or replace function public.bank_replace_imgs_in_json(p_q jsonb, p_map jsonb)
returns jsonb
language plpgsql immutable set search_path = public
as $$
declare
  t text := p_q::text;
  m jsonb;
  src text;
  esc text;
  tag text;
  rep text;
begin
  for m in select * from jsonb_array_elements(p_map) loop
    src := m->>'src';
    rep := substr(to_jsonb(m->>'text')::text, 2, length(to_jsonb(m->>'text')::text) - 2); -- thoát JSON
    esc := regexp_replace(src, '([.\\+*?\[^\]$(){}=!<>|:\-])', '\\\1', 'g');
    for tag in select x[1] from regexp_matches(t, '(<img[^>]*' || esc || '[^>]*>)', 'g') as x loop
      t := replace(t, tag, rep);
    end loop;
  end loop;
  return t::jsonb;
end; $$;

create or replace function public.bank_replace_question_imgs(p_bank_id bigint, p_map jsonb)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  b public.question_bank%rowtype;
  v_old_hash text;
  v_target_hash text;
  v_new_q jsonb;
  v_dup bigint;
  v_n int := 0;
  e record;
begin
  if not (coalesce(auth.role(), '') = 'service_role' or public.is_admin() or exists (
    select 1 from public.profiles p
    where p.id = auth.uid() and p.role = 'instructor' and p.admin_area = 'thpt'
  )) then
    raise exception 'Chỉ giáo viên mới sửa được.';
  end if;
  if jsonb_typeof(p_map) <> 'array' or jsonb_array_length(p_map) = 0 then
    raise exception 'p_map phải là mảng khác rỗng.';
  end if;
  if p_map::text ~* '<script|javascript:|on[a-z]+\s*=|<foreignObject' then
    raise exception 'Nội dung thay thế không hợp lệ.';
  end if;

  select * into b from public.question_bank where id = p_bank_id for update;
  if not found then
    raise exception 'Không thấy câu #% trong ngân hàng.', p_bank_id;
  end if;

  v_old_hash := b.content_hash;
  v_new_q := public.bank_replace_imgs_in_json(b.question, p_map);
  if v_new_q = b.question then
    raise exception 'Câu #% không có ảnh nào khớp p_map (có thể đã thay rồi).', p_bank_id;
  end if;

  select public.question_content_hash(public.bank_replace_imgs_in_json(q.value, p_map))
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
    raise exception 'Ngân hàng đã có câu y hệt sau khi thay (#%). Lưu trữ một trong hai câu rồi thử lại.', v_dup;
  end if;

  update public.question_bank set question = v_new_q where id = p_bank_id;
  update public.question_bank
    set content_hash = coalesce(v_target_hash, public.question_content_hash(question))
    where id = p_bank_id;

  for e in
    select ex.id, (q.ordinality - 1)::int as idx, q.value as qv
    from public.exams ex,
         jsonb_array_elements(ex.questions) with ordinality as q(value, ordinality)
    where jsonb_typeof(ex.questions) = 'array'
      and public.question_content_hash(q.value) = v_old_hash
  loop
    update public.exams
      set questions = jsonb_set(questions, array[e.idx::text], public.bank_replace_imgs_in_json(e.qv, p_map))
      where id = e.id;
    v_n := v_n + 1;
  end loop;

  select * into b from public.question_bank where id = p_bank_id;
  return jsonb_build_object('content_hash', b.content_hash, 'exams_updated', v_n);
end; $$;

revoke all on function public.bank_replace_imgs_in_json(jsonb, jsonb) from public, anon;
revoke all on function public.bank_replace_question_imgs(bigint, jsonb) from public, anon, authenticated;
grant execute on function public.bank_replace_question_imgs(bigint, jsonb) to service_role;

-- ROLLBACK:
-- drop function if exists public.bank_replace_question_imgs(bigint, jsonb);
-- drop function if exists public.bank_replace_imgs_in_json(jsonb, jsonb);
