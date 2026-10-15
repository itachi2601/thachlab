-- Thử 20261015233000 + 20261015234500 TRONG GIAO DỊCH rồi ROLLBACK (không để lại dữ liệu).
begin;
create temp table kq (buoc text, ket_qua text);
grant all on kq to authenticated;
select set_config('t.hs1', (select id::text from auth.users where email = 'hs.test1@thachlab.local'), true);
select set_config('t.admin', (select id::text from public.profiles where role = 'admin' limit 1), true);

-- 1. Thầy sửa ngày sinh
set local role authenticated;
select set_config('request.jwt.claims', json_build_object('sub', current_setting('t.admin'), 'role', 'authenticated')::text, true);
select public.staff_set_student_birth(current_setting('t.hs1')::uuid, '2009-08-15');
insert into kq select '1 RPC đọc lại', birth_date from public.staff_student_account(current_setting('t.hs1')::uuid);
-- 2. HS tự gọi cho bạn khác → phải bị chặn
select set_config('request.jwt.claims', json_build_object('sub', current_setting('t.hs1'), 'role', 'authenticated')::text, true);
do $$ begin
  perform public.staff_set_student_birth((select id from public.profiles where role = 'admin' limit 1), '2009-01-01');
  insert into kq values ('2 HS sửa người khác', 'KHÔNG bị chặn (lỗi!)');
exception when others then insert into kq values ('2 HS sửa người khác', 'bị chặn: ' || sqlerrm);
end $$;
reset role;
insert into kq select '3 profiles.birth_date', birth_date::text from public.profiles where id = current_setting('t.hs1')::uuid;
insert into kq select '4 metadata', raw_user_meta_data->>'birth_date' from auth.users where id = current_setting('t.hs1')::uuid;

-- 5. Năm vô lý bị chặn
do $$ begin
  perform set_config('request.jwt.claims', json_build_object('sub', current_setting('t.admin'), 'role', 'authenticated')::text, true);
  perform public.staff_set_student_birth(current_setting('t.hs1')::uuid, '2026-01-17');
  insert into kq values ('5 năm 2026', 'KHÔNG bị chặn (lỗi!)');
exception when others then insert into kq values ('5 năm 2026', 'bị chặn: ' || sqlerrm);
end $$;

-- 6. Đăng ký mới qua trigger handle_new_user
insert into auth.users (id, instance_id, aud, role, email, raw_user_meta_data, created_at, updated_at)
values ('00000000-0000-4000-8000-00000000abcd', '00000000-0000-0000-0000-000000000000', 'authenticated', 'authenticated',
  'thu.ngaysinh@thachlab.local', '{"full_name":"Thu Ngay Sinh","birth_date":"2010-05-20"}', now(), now());
insert into kq select '6 tài khoản mới', coalesce(birth_date::text, 'NULL') from public.profiles where id = '00000000-0000-4000-8000-00000000abcd';
insert into auth.users (id, instance_id, aud, role, email, raw_user_meta_data, created_at, updated_at)
values ('00000000-0000-4000-8000-00000000abce', '00000000-0000-0000-0000-000000000000', 'authenticated', 'authenticated',
  'thu.ngaysinh2@thachlab.local', '{"full_name":"Thu Ngay Sai","birth_date":"2010-02-31"}', now(), now());
insert into kq select '7 ngày sai vẫn tạo được TK', coalesce(birth_date::text, 'NULL (đúng)') from public.profiles where id = '00000000-0000-4000-8000-00000000abce';
select * from kq order by buoc;
rollback;
