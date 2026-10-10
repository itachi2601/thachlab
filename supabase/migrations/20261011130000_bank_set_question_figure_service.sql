-- Cho script trên Mac (service_role) gắn hình vẽ lại vào câu ngân hàng sau khi thầy duyệt
-- (scripts/ghi-hinh-sau-duyet.mts). bank_set_question_figure chỉ nhận admin đăng nhập (auth.uid()),
-- service_role không có uid → hàm bọc này giả lập uid của một admin RỒI gọi đúng hàm gốc, nên mọi
-- kiểm tra/ghi (câu ngân hàng + exams.questions + xoá ai_figure) giữ nguyên. Chỉ service_role gọi được.

create or replace function public.bank_set_question_figure_svc(p_bank_id bigint, p_img_html text)
returns jsonb
language plpgsql security definer set search_path = public
as $$
declare v_admin uuid;
begin
  if coalesce(auth.role(), '') <> 'service_role' then
    raise exception 'Chỉ service_role.';
  end if;
  select id into v_admin from public.profiles where role = 'admin' order by created_at limit 1;
  if v_admin is null then raise exception 'Không có tài khoản admin.'; end if;
  perform set_config('request.jwt.claim.sub', v_admin::text, true);
  perform set_config('request.jwt.claims', json_build_object('sub', v_admin, 'role', 'authenticated')::text, true);
  return public.bank_set_question_figure(p_bank_id, p_img_html);
end $$;

revoke all on function public.bank_set_question_figure_svc(bigint, text) from public, anon, authenticated;
grant execute on function public.bank_set_question_figure_svc(bigint, text) to service_role;

-- ROLLBACK:
-- drop function if exists public.bank_set_question_figure_svc(bigint, text);
