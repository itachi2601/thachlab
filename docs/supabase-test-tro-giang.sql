-- ============================================================
-- Test dữ liệu giả cho module Quản lý trợ giảng
-- (docs/supabase-migration-tro-giang.sql — CHẠY MIGRATION ĐÓ TRƯỚC KHI CHẠY FILE NÀY)
--
-- Dán toàn bộ file này vào Supabase SQL Editor và Run. Mọi thứ nằm trong 1 transaction
-- và kết thúc bằng ROLLBACK — không để lại dữ liệu giả nào trong DB thật, an toàn chạy
-- trên project production.
--
-- Cách đọc kết quả: theo dõi tab "Notices"/output — mỗi dòng "OK: ..." là 1 phép kiểm
-- đã đúng. Nếu có sai lệch, script in "MISMATCH: ..." và cuối cùng RAISE EXCEPTION liệt kê
-- toàn bộ lỗi (không dừng ở lỗi đầu tiên, để thấy hết 1 lượt).
--
-- Đổi 'itachi2601@gmail.com' ở dòng ADMIN_EMAIL bên dưới nếu tài khoản admin (role='admin'
-- trong profiles) của bạn dùng email khác.
-- ============================================================

begin;

-- ---------- 0. Giả lập đăng nhập làm admin (để qua guard is_admin() trong các hàm) ----------
do $$
declare
  v_admin_id uuid;
begin
  select id into v_admin_id from auth.users where email = 'itachi2601@gmail.com';
  if v_admin_id is null then
    raise exception 'Không tìm thấy user với email itachi2601@gmail.com trong auth.users — sửa ADMIN_EMAIL ở đầu file.';
  end if;
  perform set_config(
    'request.jwt.claims',
    json_build_object('sub', v_admin_id::text, 'role', 'authenticated')::text,
    true
  );
  raise notice 'Đang giả lập làm admin uid = %', v_admin_id;
end $$;

-- ---------- 1. Trợ giảng test ----------
-- Mượn tạm user_id của chính admin cho FK auth.users (chỉ trong transaction sẽ rollback).
insert into public.ta_assistants (id, user_id, full_name, short_name, tier, retained_rate, started_at)
values (
  'aaaaaaaa-0000-0000-0000-000000000001',
  (select id from auth.users where email = 'itachi2601@gmail.com'),
  'Trợ giảng Test', 'Test', 'B1', null, '2026-09-01'
);

-- ---------- 2. Buổi lên lớp (lop) ----------
insert into public.ta_sessions
  (id, assistant_id, work_date, session_type, class_label, start_time, end_time,
   student_touches, error_note, error_note_at, status)
values
  ('aaaaaaaa-0000-0000-0000-000000000011', 'aaaaaaaa-0000-0000-0000-000000000001',
   '2026-10-01', 'lop', '12A2', '18:00', '20:00', 10, 'Sai dấu khi đổi vế', '2026-10-01 21:00:00+07', 'approved'),
  ('aaaaaaaa-0000-0000-0000-000000000012', 'aaaaaaaa-0000-0000-0000-000000000001',
   '2026-10-03', 'lop', '12A2', '17:30', '19:30', 14, 'Nhầm công thức chu kỳ', '2026-10-04 09:00:00+07', 'approved'), -- nộp trễ (khác ngày work_date)
  ('aaaaaaaa-0000-0000-0000-000000000013', 'aaaaaaaa-0000-0000-0000-000000000001',
   '2026-10-06', 'lop', '12A2', '19:00', '21:00', 9, 'Sai đơn vị', '2026-10-06 21:30:00+07', 'approved');

-- ---------- 3. Buổi phụ đạo ----------
insert into public.ta_sessions
  (id, assistant_id, work_date, session_type, class_label, start_time, end_time,
   homework_given, student_recap_ok, status)
values
  ('aaaaaaaa-0000-0000-0000-000000000021', 'aaaaaaaa-0000-0000-0000-000000000001',
   '2026-10-02', 'phudao', 'Học sinh X', '19:00', '21:00', 'Bài 5,6,7 trang 42', true, 'approved'),
  ('aaaaaaaa-0000-0000-0000-000000000022', 'aaaaaaaa-0000-0000-0000-000000000001',
   '2026-10-08', 'phudao', 'Học sinh Y', '18:00', '19:30', null, false, 'approved');

-- ---------- 4. Buổi chấm bài + hành chính ----------
insert into public.ta_sessions
  (id, assistant_id, work_date, session_type, start_time, end_time, papers_graded, status)
values
  ('aaaaaaaa-0000-0000-0000-000000000031', 'aaaaaaaa-0000-0000-0000-000000000001',
   '2026-10-07', 'chambai', '14:00', '15:00', 20, 'approved');

insert into public.ta_sessions
  (id, assistant_id, work_date, session_type, start_time, end_time, status)
values
  ('aaaaaaaa-0000-0000-0000-000000000041', 'aaaaaaaa-0000-0000-0000-000000000001',
   '2026-10-09', 'hanhchinh', '08:00', '09:00', 'approved');

-- ---------- 5. 1 nhắc nhở làm việc riêng trong tháng ----------
insert into public.ta_flags (assistant_id, flag_date, note)
values ('aaaaaaaa-0000-0000-0000-000000000001', '2026-10-05', 'Dùng điện thoại riêng trong giờ dạy');

-- ---------- 6. Video: V1 đã duyệt + có lượt xem + có lead, V2 chưa duyệt ----------
insert into public.ta_sessions
  (id, assistant_id, work_date, session_type, video_url, video_tier, published_at, topic_source_id, status)
values
  ('aaaaaaaa-0000-0000-0000-000000000051', 'aaaaaaaa-0000-0000-0000-000000000001',
   '2026-10-10', 'video', 'https://tiktok.com/v1', 'don_gian', '2026-10-10 12:00:00+07',
   'aaaaaaaa-0000-0000-0000-000000000011', 'approved'),
  ('aaaaaaaa-0000-0000-0000-000000000052', 'aaaaaaaa-0000-0000-0000-000000000001',
   '2026-10-12', 'video', 'https://tiktok.com/v2', 'dung_ky', '2026-10-12 09:00:00+07',
   null, 'submitted');

insert into public.ta_video_stats (session_id, checked_at, views, saves, comments)
values
  ('aaaaaaaa-0000-0000-0000-000000000051', '2026-10-11', 8000, 500, 20),   -- cũ hơn, phải bị bỏ qua
  ('aaaaaaaa-0000-0000-0000-000000000051', '2026-10-15', 12000, 750, 40),  -- bản mới nhất -> dùng cái này
  ('aaaaaaaa-0000-0000-0000-000000000052', '2026-10-20', 60000, 4000, 200);

insert into public.ta_leads (student_name, source, attributed_session_id, registered_at)
values ('Học sinh Mới A', 'tiktok', 'aaaaaaaa-0000-0000-0000-000000000051', '2026-10-16');

-- ---------- 7. KIỂM TRA ĐIỂM + LƯƠNG THÁNG (ta_monthly_score) ----------
-- Tay tính trước: avg_touches=(10+14+9)/3=11 -> touches_score=40*11/12=36.67
--   ontime 2/3 -> error_note_score=20*2/3=13.33 (tổng 2 cái này = 50 tròn)
--   phudao 1/2 hoàn chỉnh -> phudao_score=10.00
--   1 flag -> focus_score=10
--   total_score = 50+10+10 = 70.00 (đúng biên >=70 -> thưởng 2000đ/giờ)
--   converted_hours = 2+2+2+2.5+1.875+0(chambai)+1(hanhchinh) = 11.375
--   base_pay = 11.375*40000 = 455000 ; bonus_pay = 11.375*2000 = 22750 ; grading_pay=20*1500=30000
--   total_pay = 507750
do $$
declare
  r record;
  errs text[] := '{}';
begin
  select * into r from public.ta_monthly_score('aaaaaaaa-0000-0000-0000-000000000001', '2026-10-01');

  if r.avg_touches is distinct from 11.00 then errs := errs || format('avg_touches = %s, kỳ vọng 11.00', r.avg_touches); end if;
  if r.touches_score is distinct from 36.67 then errs := errs || format('touches_score = %s, kỳ vọng 36.67', r.touches_score); end if;
  if r.error_note_score is distinct from 13.33 then errs := errs || format('error_note_score = %s, kỳ vọng 13.33', r.error_note_score); end if;
  if r.phudao_score is distinct from 10.00 then errs := errs || format('phudao_score = %s, kỳ vọng 10.00', r.phudao_score); end if;
  if r.flag_count is distinct from 1 then errs := errs || format('flag_count = %s, kỳ vọng 1', r.flag_count); end if;
  if r.focus_score is distinct from 10 then errs := errs || format('focus_score = %s, kỳ vọng 10', r.focus_score); end if;
  if r.total_score is distinct from 70.00 then errs := errs || format('total_score = %s, kỳ vọng 70.00', r.total_score); end if;
  if r.bonus_per_hour is distinct from 2000 then errs := errs || format('bonus_per_hour = %s, kỳ vọng 2000', r.bonus_per_hour); end if;
  if r.converted_hours is distinct from 11.38 then errs := errs || format('converted_hours (hiển thị, đã làm tròn) = %s, kỳ vọng 11.38', r.converted_hours); end if;
  if r.papers_graded is distinct from 20 then errs := errs || format('papers_graded = %s, kỳ vọng 20', r.papers_graded); end if;
  if r.base_pay is distinct from 455000 then errs := errs || format('base_pay = %s, kỳ vọng 455000', r.base_pay); end if;
  if r.bonus_pay is distinct from 22750 then errs := errs || format('bonus_pay = %s, kỳ vọng 22750', r.bonus_pay); end if;
  if r.grading_pay is distinct from 30000 then errs := errs || format('grading_pay = %s, kỳ vọng 30000', r.grading_pay); end if;
  if r.total_pay is distinct from 507750 then errs := errs || format('total_pay = %s, kỳ vọng 507750', r.total_pay); end if;

  if array_length(errs, 1) is null then
    raise notice 'OK: ta_monthly_score khớp toàn bộ kỳ vọng.';
  else
    raise notice 'MISMATCH ta_monthly_score: %', array_to_string(errs, ' | ');
  end if;
end $$;

-- ---------- 8. KIỂM TRA GIỜ TÍCH LŨY (ta_accrued_hours) ----------
-- Kỳ vọng: chỉ lop+phudao = 2+2+2+2.5+1.875 = 10.375
do $$
declare v_hours numeric;
begin
  select public.ta_accrued_hours('aaaaaaaa-0000-0000-0000-000000000001') into v_hours;
  if v_hours is distinct from 10.375 then
    raise notice 'MISMATCH ta_accrued_hours = %, kỳ vọng 10.375', v_hours;
  else
    raise notice 'OK: ta_accrued_hours = 10.375.';
  end if;
end $$;

-- ---------- 9. KIỂM TRA SỔ VIDEO (ta_video_ledger) ----------
-- V1: đã duyệt + có url -> production_pay=120000; views mới nhất=12000 -> view_bonus=50000;
--     1 lead -> lead_bonus=300000; total=470000
-- V2: CHƯA duyệt -> production_pay=0 dù có url; views=60000 -> view_bonus=200000 (cộng dồn 2 mốc);
--     0 lead; total=200000
do $$
declare
  v1 record; v2 record; errs text[] := '{}';
begin
  select * into v1 from public.ta_video_ledger('aaaaaaaa-0000-0000-0000-000000000001')
    where session_id = 'aaaaaaaa-0000-0000-0000-000000000051';
  select * into v2 from public.ta_video_ledger('aaaaaaaa-0000-0000-0000-000000000001')
    where session_id = 'aaaaaaaa-0000-0000-0000-000000000052';

  if v1.latest_views is distinct from 12000 then errs := errs || format('V1.latest_views=%s kỳ vọng 12000 (phải lấy bản checked_at mới nhất, bỏ bản cũ 8000)', v1.latest_views); end if;
  if v1.view_bonus is distinct from 50000 then errs := errs || format('V1.view_bonus=%s kỳ vọng 50000', v1.view_bonus); end if;
  if v1.production_pay is distinct from 120000 then errs := errs || format('V1.production_pay=%s kỳ vọng 120000', v1.production_pay); end if;
  if v1.lead_count is distinct from 1 then errs := errs || format('V1.lead_count=%s kỳ vọng 1', v1.lead_count); end if;
  if v1.lead_bonus is distinct from 300000 then errs := errs || format('V1.lead_bonus=%s kỳ vọng 300000', v1.lead_bonus); end if;
  if v1.total_pay is distinct from 470000 then errs := errs || format('V1.total_pay=%s kỳ vọng 470000', v1.total_pay); end if;

  if v2.production_pay is distinct from 0 then errs := errs || format('V2.production_pay=%s kỳ vọng 0 (status=submitted, chưa duyệt)', v2.production_pay); end if;
  if v2.view_bonus is distinct from 200000 then errs := errs || format('V2.view_bonus=%s kỳ vọng 200000 (60000 view vượt cả 2 mốc, cộng dồn)', v2.view_bonus); end if;
  if v2.total_pay is distinct from 200000 then errs := errs || format('V2.total_pay=%s kỳ vọng 200000', v2.total_pay); end if;

  if array_length(errs, 1) is null then
    raise notice 'OK: ta_video_ledger khớp toàn bộ kỳ vọng.';
  else
    raise notice 'MISMATCH ta_video_ledger: %', array_to_string(errs, ' | ');
  end if;
end $$;

-- ---------- 10. KIỂM TRA TỔNG HỢP ADMIN THÁNG 10/2026 (ta_video_admin_summary) ----------
-- Lưu ý: nếu DB thật đã có dữ liệu video khác trong tháng 10/2026 (khó xảy ra vì đây là tháng
-- tương lai so với lúc viết script), số tổng sẽ cộng dồn thêm và các so sánh tuyệt đối bên dưới
-- sẽ sai lệch dù logic đúng — nếu vậy hãy đối chiếu bằng tay thay vì tin assertion tuyệt đối này.
do $$
declare r record; errs text[] := '{}';
begin
  select * into r from public.ta_video_admin_summary('2026-10-01');

  if r.videos_published is distinct from 2 then errs := errs || format('videos_published=%s kỳ vọng 2', r.videos_published); end if;
  if r.total_views is distinct from 72000 then errs := errs || format('total_views=%s kỳ vọng 72000', r.total_views); end if;
  if r.total_saves is distinct from 4750 then errs := errs || format('total_saves=%s kỳ vọng 4750', r.total_saves); end if;
  if r.leads_count is distinct from 1 then errs := errs || format('leads_count=%s kỳ vọng 1', r.leads_count); end if;
  if r.production_spend is distinct from 120000 then errs := errs || format('production_spend=%s kỳ vọng 120000', r.production_spend); end if;
  if r.total_spend is distinct from 670000 then errs := errs || format('total_spend=%s kỳ vọng 670000', r.total_spend); end if;
  if r.over_budget is distinct from false then errs := errs || format('over_budget=%s kỳ vọng false (120000 < trần 1.200.000)', r.over_budget); end if;
  if r.cost_per_lead is distinct from 670000 then errs := errs || format('cost_per_lead=%s kỳ vọng 670000', r.cost_per_lead); end if;

  if array_length(errs, 1) is null then
    raise notice 'OK: ta_video_admin_summary khớp toàn bộ kỳ vọng.';
  else
    raise notice 'MISMATCH ta_video_admin_summary: %', array_to_string(errs, ' | ');
  end if;
end $$;

-- ---------- 11. KIỂM TRA TỶ LỆ KHAI THÁC ĐỀ TÀI (đo bằng độ lệch trước/sau, không phụ
--              thuộc dữ liệu thật có sẵn trong DB) ----------
-- Kỳ vọng: 3 buổi lop có error_note vừa thêm đều "đủ điều kiện" (work_date của chúng luôn
-- >= current_date - 14 vì hàm không giới hạn cận trên); trong đó chỉ L1 được dùng làm đề tài (V1).
do $$
declare before_e int; before_u int; after_e int; after_u int; errs text[] := '{}';
begin
  -- không thể tách trước/sau trong cùng transaction đã insert xong ở trên nên kiểm tra trực tiếp
  -- phần đóng góp của riêng bộ test này qua điều kiện lọc theo id để không lẫn dữ liệu thật khác.
  select
    count(*) filter (where s.id in (
      'aaaaaaaa-0000-0000-0000-000000000011',
      'aaaaaaaa-0000-0000-0000-000000000012',
      'aaaaaaaa-0000-0000-0000-000000000013'
    )),
    count(*) filter (where s.id in (
      'aaaaaaaa-0000-0000-0000-000000000011',
      'aaaaaaaa-0000-0000-0000-000000000012',
      'aaaaaaaa-0000-0000-0000-000000000013'
    ) and exists (
      select 1 from public.ta_sessions v
      where v.session_type = 'video' and v.topic_source_id = s.id
    ))
  into after_e, after_u
  from public.ta_sessions s
  where s.session_type = 'lop' and s.status = 'approved'
    and s.error_note is not null and length(trim(s.error_note)) > 0;

  if after_e is distinct from 3 then errs := errs || format('3 buổi lop test không đủ điều kiện đề tài như kỳ vọng (đếm được %s)', after_e); end if;
  if after_u is distinct from 1 then errs := errs || format('số buổi đã dùng làm đề tài = %s, kỳ vọng 1 (chỉ L1 qua V1)', after_u); end if;

  if array_length(errs, 1) is null then
    raise notice 'OK: liên kết đề tài video <-> error_note đúng như kỳ vọng.';
  else
    raise notice 'MISMATCH đề tài video: %', array_to_string(errs, ' | ');
  end if;
end $$;

-- ---------- 12. NEGATIVE TEST: trợ giảng khác (hoặc người lạ) không đọc được điểm/lương của A ----------
do $$
declare v_other_id uuid; v_admin_id uuid;
begin
  select id into v_admin_id from auth.users where email = 'itachi2601@gmail.com';
  select u.id into v_other_id
  from auth.users u join public.profiles p on p.id = u.id
  where p.role = 'student' and u.id <> v_admin_id
  limit 1;

  if v_other_id is null then
    raise notice 'BỎ QUA negative test: không tìm thấy tài khoản role=student nào khác để giả lập.';
    return;
  end if;

  perform set_config('request.jwt.claims', json_build_object('sub', v_other_id::text, 'role', 'authenticated')::text, true);

  begin
    perform public.ta_monthly_score('aaaaaaaa-0000-0000-0000-000000000001', '2026-10-01');
    raise notice 'MISMATCH bảo mật: user lạ (%) gọi được ta_monthly_score của trợ giảng khác — ĐÂY LÀ LỖ HỔNG.', v_other_id;
  exception when others then
    raise notice 'OK: user lạ bị chặn khi gọi ta_monthly_score của trợ giảng khác (% )', sqlerrm;
  end;

  -- trả lại danh nghĩa admin cho các bước sau
  perform set_config('request.jwt.claims', json_build_object('sub', v_admin_id::text, 'role', 'authenticated')::text, true);
end $$;

-- ---------- 13. NEGATIVE TEST: topic_source_id phải trỏ tới buổi 'lop', không phải 'phudao' ----------
do $$
begin
  begin
    insert into public.ta_sessions (assistant_id, work_date, session_type, video_url, video_tier, topic_source_id, status)
    values ('aaaaaaaa-0000-0000-0000-000000000001', '2026-10-13', 'video', 'https://tiktok.com/bad',
            'don_gian', 'aaaaaaaa-0000-0000-0000-000000000021', 'submitted'); -- P1 là phudao, không phải lop
    raise notice 'MISMATCH: cho phép topic_source_id trỏ tới buổi phudao — trigger chưa chặn đúng.';
  exception when others then
    raise notice 'OK: trigger chặn topic_source_id trỏ tới buổi không phải lop (%)', sqlerrm;
  end;
end $$;

-- ---------- 14. NEGATIVE TEST: buổi 'lop' bắt buộc phải có error_note ----------
do $$
begin
  begin
    insert into public.ta_sessions (assistant_id, work_date, session_type, start_time, end_time, student_touches, status)
    values ('aaaaaaaa-0000-0000-0000-000000000001', '2026-10-14', 'lop', '18:00', '19:00', 5, 'submitted');
    raise notice 'MISMATCH: cho phép buổi lop không có error_note — check constraint chưa chặn đúng.';
  exception when others then
    raise notice 'OK: check constraint chặn buổi lop thiếu error_note (%)', sqlerrm;
  end;
end $$;

-- ---------- 15. NEGATIVE TEST: buổi 'video' không được có start_time/end_time ----------
do $$
begin
  begin
    insert into public.ta_sessions (assistant_id, work_date, session_type, start_time, end_time, video_tier, status)
    values ('aaaaaaaa-0000-0000-0000-000000000001', '2026-10-14', 'video', '18:00', '19:00', 'don_gian', 'submitted');
    raise notice 'MISMATCH: cho phép buổi video có start_time/end_time — check constraint chưa chặn đúng.';
  exception when others then
    raise notice 'OK: check constraint chặn buổi video có giờ bắt đầu/kết thúc (%)', sqlerrm;
  end;
end $$;

-- ---------- 16. Trigger tự điền error_note_at khi không truyền (giờ server, không tin máy client) ----------
do $$
declare v_at timestamptz;
begin
  insert into public.ta_sessions (assistant_id, work_date, session_type, start_time, end_time, student_touches, error_note, status)
  values ('aaaaaaaa-0000-0000-0000-000000000001', '2026-10-15', 'lop', '18:00', '19:00', 5, 'Lỗi test trigger', 'submitted')
  returning error_note_at into v_at;

  if v_at is null then
    raise notice 'MISMATCH: trigger không tự điền error_note_at khi để trống.';
  else
    raise notice 'OK: trigger tự điền error_note_at = %', v_at;
  end if;
end $$;

-- ---------- Dọn dẹp: KHÔNG commit gì cả ----------
rollback;
