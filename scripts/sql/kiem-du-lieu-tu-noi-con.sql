-- Chỉ đọc: bao nhiêu học sinh THPT trong lớp đủ điều kiện để phụ huynh tự nối (ngày sinh + SĐT phụ huynh).
with hs as (
  select p.id, p.birth_date,
    length(regexp_replace(coalesce(u.raw_user_meta_data->>'parent_phone', ''), '\D', '', 'g')) >= 9 as co_sdt
  from public.profiles p join auth.users u on u.id = p.id
  where p.role = 'student' and p.track = 'thpt'
    and exists (select 1 from public.user_classes uc where uc.user_id = p.id)
)
select count(*) as hoc_sinh_thpt_trong_lop,
  count(*) filter (where birth_date is not null) as co_ngay_sinh,
  count(*) filter (where co_sdt) as co_sdt_phu_huynh,
  count(*) filter (where birth_date is not null and co_sdt) as du_dk_tu_noi,
  (select count(*) from public._bak_profiles_birth_20261015) as da_chep_lan_nay
from hs;
