-- Chỉ đọc (dry-run): ngày sinh trong metadata đăng ký có hợp lệ để chép sang profiles.birth_date không.
with m as (
  select p.id, p.track, u.raw_user_meta_data->>'birth_date' as b
  from public.profiles p join auth.users u on u.id = p.id
  where p.birth_date is null and coalesce(u.raw_user_meta_data->>'birth_date', '') <> ''
)
select
  count(*) as tong,
  count(*) filter (where b ~ '^\d{4}-\d{2}-\d{2}$') as dung_dinh_dang,
  count(*) filter (where b ~ '^\d{4}-\d{2}-\d{2}$' and substr(b,1,4)::int between 2005 and 2014) as nam_hop_ly_thpt,
  string_agg(distinct b, ', ') filter (where b !~ '^\d{4}-\d{2}-\d{2}$' or substr(b,1,4)::int not between 2005 and 2014) as gia_tri_la
from m;
