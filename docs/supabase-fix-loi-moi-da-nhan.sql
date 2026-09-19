-- ============================================================
-- Sửa: người được mời bấm "Nhận lời mời" chỉ thấy "Không nhận được lời mời."
--
-- Nguyên nhân thường gặp nhất: lời mời ĐÃ được áp dụng từ trước — người đó đăng ký
-- tài khoản ngay trên link mời, trigger zz_claim_staff_invite cấp quyền và đóng dấu
-- claimed_at ngay lúc insert auth.users. Mở lại link rồi bấm nút thì claim_staff_invite
-- không còn dòng nào claimed_at is null nên raise, người dùng thấy một lỗi cụt lủn.
--
-- Bản này:
--   - chính chủ bấm lại mã mình đã nhận -> trả về quyền đang có (thành công, không lỗi);
--   - mã người khác đã nhận -> nói rõ ai nhận, lúc nào;
--   - mã không tồn tại -> nói rõ là mã sai, khác hẳn "đã dùng rồi".
--
-- Chạy được nhiều lần. Chạy trong Supabase → SQL Editor.
-- (Đã gộp sẵn vào docs/supabase-migration-staff-invites.sql cho DB dựng mới.)
-- ============================================================

create or replace function public.claim_staff_invite(p_code text)
returns table (role text, class_name text, tier text)
language plpgsql
security definer
set search_path = public
as $$
declare
  v_user uuid := auth.uid();
  v_code text := upper(trim(coalesce(p_code, '')));
  v_invite_id uuid;
  inv public.staff_invites%rowtype;
  v_owner_email text;
begin
  if v_user is null then
    raise exception 'Bạn cần đăng nhập trước khi nhận lời mời.';
  end if;

  -- Lấy cả lời mời đã nhận để phân biệt "mã sai" với "mã đã dùng" — hai việc phải xử lý khác nhau.
  select * into inv from public.staff_invites where upper(code) = v_code;

  if inv.id is null then
    raise exception 'Không có lời mời nào mang mã %. Nhờ thầy cô gửi lại link mời mới.', v_code;
  end if;

  if inv.claimed_at is not null then
    -- Chính chủ bấm lại (hay đăng ký xong quay lại link): quyền đã cấp từ lần trước, coi như xong.
    if inv.claimed_user_id = v_user then
      return query
      select inv.role,
             (select c.name from public.classes c where c.id = inv.class_id),
             inv.tier;
      return;
    end if;

    select u.email into v_owner_email from auth.users u where u.id = inv.claimed_user_id;
    raise exception 'Mã % đã được % nhận lúc %. Nhờ thầy cô tạo mã mới cho bạn.',
      v_code,
      coalesce(v_owner_email, 'một tài khoản khác'),
      to_char(inv.claimed_at at time zone 'Asia/Ho_Chi_Minh', 'HH24:MI "ngày" DD/MM/YYYY');
  end if;

  v_invite_id := public.apply_staff_invite(
    v_user,
    (select u.email from auth.users u where u.id = v_user),
    p_code
  );

  if v_invite_id is null then
    raise exception 'Không nhận được lời mời này — nhờ thầy cô tạo lại mã mời.';
  end if;

  return query
  select inv.role,
         (select c.name from public.classes c where c.id = inv.class_id),
         inv.tier;
end;
$$;

grant execute on function public.claim_staff_invite(text) to authenticated;

-- Xem nhanh một mã mời đang ở trạng thái nào (chạy bằng SQL Editor, không qua RLS):
-- select i.code, i.full_name, i.role, i.tier, i.claimed_at, u.email as nguoi_nhan
-- from public.staff_invites i
-- left join auth.users u on u.id = i.claimed_user_id
-- where upper(i.code) = '1445D376';
