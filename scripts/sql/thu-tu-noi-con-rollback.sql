-- Thử luồng phụ huynh tự nối con trên production TRONG MỘT GIAO DỊCH rồi ROLLBACK (không để lại dữ liệu).
-- HS Test 1 = "con" (gán tạm ngày sinh + SĐT phụ huynh), HS Test 2 = "phụ huynh".
begin;
select set_config('t.hs1', (select id::text from auth.users where email = 'hs.test1@thachlab.local'), true);
select set_config('t.hs2', (select id::text from auth.users where email = 'hs.test2@thachlab.local'), true);
update public.profiles set birth_date = '2008-03-15' where id = current_setting('t.hs1')::uuid;
update auth.users set raw_user_meta_data = coalesce(raw_user_meta_data, '{}'::jsonb) || '{"parent_phone":"0912 345 678"}'
  where id = current_setting('t.hs1')::uuid;
create temp table kq (buoc text, ket_qua text);
grant all on kq to authenticated;

set local role authenticated;
select set_config('request.jwt.claims', json_build_object('sub', current_setting('t.hs2'), 'role', 'authenticated')::text, true);
insert into kq select '1 sai SĐT', status from public.claim_parent_by_child_info('HS Test 1', '2008-03-15', '0900000000');
insert into kq select '2 đúng cả 3', status || ' / ' || coalesce(student_name, '') from public.claim_parent_by_child_info('hs  test 1', '2008-03-15', '+84 912-345-678');
insert into kq select '3 bấm lại', status from public.claim_parent_by_child_info('HS Test 1', '2008-03-15', '0912345678');
insert into kq select '4 gửi yêu cầu', public.request_parent_link_review('Em Khong Ton Tai', '2009-01-01', '0911111111', 'thử')::text;
insert into kq select '5 PH thấy yêu cầu của mình', count(*)::text from public.parent_link_requests;
reset role;

insert into kq select '6 liên kết đã tạo', count(*)::text from public.parent_links
  where student_id = current_setting('t.hs1')::uuid and parent_id = current_setting('t.hs2')::uuid and claimed_at is not null;
insert into kq select '7 thông báo cho con', count(*)::text from public.notifications
  where user_id = current_setting('t.hs1')::uuid and kind = 'parent_linked';
insert into kq select '8 thông báo cho staff', count(*)::text from public.notifications
  where kind in ('parent_linked', 'parent_link_request') and created_at > now() - interval '1 minute' and user_id <> current_setting('t.hs1')::uuid;
insert into kq select '9 lượt sai đã ghi', count(*)::text from public.parent_link_attempts where user_id = current_setting('t.hs2')::uuid and not success;
select * from kq order by buoc;
rollback;
