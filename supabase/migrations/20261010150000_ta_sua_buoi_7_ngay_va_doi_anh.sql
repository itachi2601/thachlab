-- Báo lỗi #85 + #84 (10/10/2026)
-- 1) Trợ giảng sửa lại buổi của mình (chưa được duyệt) trong 7 ngày kể từ ngày làm (trước là 3 ngày), quá hạn thì khoá.
drop policy if exists "ta sua buoi trong han" on public.ta_sessions;
create policy "ta sua buoi trong han" on public.ta_sessions
  for update to authenticated
  using (
    assistant_id = ta_current_assistant_id()
    and status = 'submitted'
    and work_date >= (current_date - 7)
  )
  with check (
    assistant_id = ta_current_assistant_id()
    and status = 'submitted'
    and work_date between (current_date - 7) and current_date
  );

-- 2) Trợ giảng / giáo viên đổi ảnh đại diện: chính sách "update own profile" chỉ cho role='student' nên PATCH bị chặn.
--    Hàm này chỉ đụng đúng cột avatar_url của chính người gọi, không mở thêm quyền nào khác.
create or replace function public.set_my_avatar(p_url text)
returns void
language sql
security definer
set search_path = public
as $$
  update public.profiles set avatar_url = p_url where id = auth.uid();
$$;
revoke all on function public.set_my_avatar(text) from public, anon;
grant execute on function public.set_my_avatar(text) to authenticated;

-- ROLLBACK:
--   drop function if exists public.set_my_avatar(text);
--   drop policy if exists "ta sua buoi trong han" on public.ta_sessions;
--   create policy "ta sua buoi trong han" on public.ta_sessions for update to authenticated
--     using (assistant_id = ta_current_assistant_id() and status = 'submitted' and work_date >= (current_date - 3))
--     with check (assistant_id = ta_current_assistant_id() and status = 'submitted');
