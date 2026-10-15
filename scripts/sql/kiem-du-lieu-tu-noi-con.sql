-- Chỉ đọc: kiểm hàm của migration 20261015180000 + bao nhiêu học sinh đủ điều kiện để phụ huynh tự nối.
select public.pl_fold_name('  Nguyễn   ĐỨC Phú ') as fold, public.pl_digits('0912 345-678') as digits,
  (select count(*) from pg_proc where proname in ('claim_parent_by_child_info','request_parent_link_review','review_parent_link_request','search_students_for_link')) as so_rpc;

with hs as (
  select p.id, p.birth_date
  from public.profiles p
  where p.role = 'student'
    and exists (select 1 from public.user_classes uc where uc.user_id = p.id)
)
select
  count(*) as hoc_sinh_trong_lop,
  count(*) filter (where birth_date is not null) as co_ngay_sinh,
  count(*) filter (where exists (
    select 1 from auth.users u where u.id = hs.id
      and length(regexp_replace(coalesce(u.raw_user_meta_data->>'parent_phone', ''), '\D', '', 'g')) >= 9
  )) as co_sdt_phu_huynh_ho_so
from hs;
