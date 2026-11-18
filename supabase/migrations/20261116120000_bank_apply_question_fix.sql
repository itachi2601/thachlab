-- AI sửa lỗi câu trong bản nháp đề (trang đăng đề) → sửa LUÔN câu gốc trong ngân hàng + mọi đề đang dùng câu đó.
-- Trước đây nút "AI sửa" chỉ đổi bản nháp; khi đăng, hash đổi nên sync_exam_to_bank sinh THÊM dòng ngân hàng,
-- bản lỗi gốc vẫn nằm lại (và lần lưu đề khác chép lỗi quay lại).
--
-- bank_apply_question_fix(p_old, p_new): p_old = câu trước khi sửa, p_new = câu sau khi sửa (jsonb ExamQuestion).
--   * Không có dòng ngân hàng nào trùng hash(p_old) → trả {"status":"not_in_bank"} (đề mới; đăng bình thường sẽ chép vào ngân hàng).
--   * hash(p_new) đã có ở dòng ngân hàng khác → {"status":"duplicate","dup_id":N}, KHÔNG sửa gì (tránh trùng; giáo viên xử lý tay).
--   * Ngược lại: cập nhật question_bank.question + content_hash, và mọi exams.questions có câu hash = hash(p_old)
--     (giữ các khoá ngoài-hash như topic/difficulty/distractorNotes của chỗ đó, chỉ ghi đè khoá có trong p_new).
--     Hash đích tính theo bản mới trong đề để trigger trg_exams_sync_bank không sinh câu trùng.
-- Chỉ giáo viên (is_admin / instructor thpt) hoặc service_role. Mẫu: bank_replace_question_imgs (20261011140000).
-- Chạy lúc nào cũng được (hàm mới, không đụng dữ liệu cũ). Rollback: perf/rollback/20261116120000_bank_apply_question_fix.down.sql
--   (chỉ gỡ hàm; câu đã sửa nằm yên).

create or replace function public.bank_apply_question_fix(p_old jsonb, p_new jsonb)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare
  b public.question_bank%rowtype;
  v_old_hash text;
  v_new_hash text;
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
  if jsonb_typeof(p_old) <> 'object' or jsonb_typeof(p_new) <> 'object' or coalesce(p_new->>'question', '') = '' then
    raise exception 'p_old và p_new phải là câu hỏi (object, có "question").';
  end if;
  if p_new::text ~* '<script|javascript:|on[a-z]+\s*=|<foreignObject' then
    raise exception 'Nội dung câu sửa không hợp lệ.';
  end if;

  v_old_hash := public.question_content_hash(p_old);
  v_new_hash := public.question_content_hash(p_new);
  if v_old_hash = v_new_hash then
    return jsonb_build_object('status', 'unchanged');
  end if;

  select * into b from public.question_bank where content_hash = v_old_hash for update;
  if not found then
    return jsonb_build_object('status', 'not_in_bank');
  end if;

  select id into v_dup from public.question_bank where content_hash = v_new_hash and id <> b.id;
  if found then
    return jsonb_build_object('status', 'duplicate', 'dup_id', v_dup);
  end if;

  v_new_q := b.question || p_new;
  update public.question_bank set question = v_new_q where id = b.id;
  update public.question_bank set content_hash = v_new_hash where id = b.id;

  for e in
    select ex.id, (q.ordinality - 1)::int as idx, q.value as qv
    from public.exams ex,
         jsonb_array_elements(ex.questions) with ordinality as q(value, ordinality)
    where jsonb_typeof(ex.questions) = 'array'
      and public.question_content_hash(q.value) = v_old_hash
  loop
    update public.exams
      set questions = jsonb_set(questions, array[e.idx::text], e.qv || p_new)
      where id = e.id;
    v_n := v_n + 1;
  end loop;

  return jsonb_build_object('status', 'fixed', 'bank_id', b.id, 'exams_updated', v_n);
end; $$;

revoke all on function public.bank_apply_question_fix(jsonb, jsonb) from public, anon;
grant execute on function public.bank_apply_question_fix(jsonb, jsonb) to authenticated, service_role;

-- ROLLBACK: perf/rollback/20261116120000_bank_apply_question_fix.down.sql
-- drop function if exists public.bank_apply_question_fix(jsonb, jsonb);
