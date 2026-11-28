-- ABET MET (CĐ Công nghệ Kỹ thuật Cơ khí, Cao Thắng) — thu dữ liệu PI qua thachlab, chặng 1.
--
-- Thay cho file Excel "ABET MET - Theo dõi đánh giá SO-PI":
--   abet_sources  = tab "Kế hoạch PI" (mỗi dòng: một PI × một học phần × một khoá) + mã link nộp
--   abet_scores   = tab "Dữ liệu điểm" (MSSV + điểm câu PI; KHÔNG lưu họ tên)
--   abet_files    = minh chứng (đề + đáp án, 3 bài mẫu) trong bucket riêng tư 'abet-minh-chung'
--   abet_history  = tab "Lịch sử" (% đạt các năm trước, để so sánh)
--
-- Giáo viên (chủ PI) KHÔNG cần tài khoản: mở link /abet/nop/?ma=<token>, các hàm abet_nop_* (security
-- definer) kiểm token rồi mới đọc/ghi đúng dòng đó. Mọi bảng chỉ admin đọc/sửa (RLS is_admin()).
-- Trang: app/abet/nop (giáo viên), app/quan-tri/(cttc)/abet (điều phối).
--
-- Chạy lúc nào cũng được: chỉ tạo bảng mới + chèn ~30 dòng kế hoạch/lịch sử. Rollback: cuối file.

-- ─────────────────────────── Bảng ───────────────────────────
create table if not exists public.abet_sources (
  id bigint generated always as identity primary key,
  ma_dong text not null unique,                 -- '2526-1.1a'
  nam_hoc text not null,                        -- '2025-2026'
  so text not null,                             -- 'SO1'
  pi text not null,                             -- 'PI1.1'
  hk_ctdt smallint,                             -- học kì trong chương trình đào tạo
  hoc_ky text,                                  -- 'HK1' / 'HK2' của năm học
  khoa text,                                    -- 'CĐ CK 25'
  ma_hp text,
  hoc_phan text not null,
  cong_cu text,                                 -- Câu hỏi thi / Rubric / Bài thi thực hành / Báo cáo …
  noi_dung text,                                -- câu/phần lấy dữ liệu
  diem_toi_da numeric(7,2) check (diem_toi_da is null or diem_toi_da > 0),
  chu_pi text,                                  -- giáo viên dạy học phần
  phu_trach_so text,
  han_nop date,
  tuy_chon boolean not null default false,      -- nguồn phụ, PI đã đủ nguồn khác
  trang_thai text not null default 'chua_gui'
    check (trang_thai in ('chua_gui', 'da_gui', 'da_nop', 'da_duyet', 'khong_thu_duoc')),
  ghi_chu text,                                 -- ghi chú của điều phối
  nhan_xet_gv text,                             -- nhận xét của giáo viên học phần (mục 5 khi đóng năm)
  ly_do_khong_thu text,
  token text not null unique default replace(gen_random_uuid()::text, '-', ''),
  nop_luc timestamptz,
  cap_nhat_luc timestamptz not null default now()
);
create index if not exists abet_sources_nam_hoc_idx on public.abet_sources (nam_hoc, so, pi);

create table if not exists public.abet_scores (
  source_id bigint not null references public.abet_sources (id) on delete cascade,
  mssv text not null,
  diem numeric(7,2) not null check (diem >= 0),
  primary key (source_id, mssv)
);

create table if not exists public.abet_files (
  id bigint generated always as identity primary key,
  source_id bigint not null references public.abet_sources (id) on delete cascade,
  loai text not null check (loai in ('de_dap_an', 'bai_mau_cao', 'bai_mau_tb', 'bai_mau_thap', 'khac')),
  storage_path text not null unique,
  ten_file text not null,
  mime_type text,
  kich_thuoc bigint,
  tao_luc timestamptz not null default now()
);
create index if not exists abet_files_source_idx on public.abet_files (source_id);

create table if not exists public.abet_history (
  nam_hoc text not null,
  ma text not null,                             -- 'PI1.1' hoặc 'SO1'
  ti_le numeric(6,4) not null,
  nguon text,
  primary key (nam_hoc, ma)
);

-- ─────────────────────────── Quyền ───────────────────────────
alter table public.abet_sources enable row level security;
alter table public.abet_scores enable row level security;
alter table public.abet_files enable row level security;
alter table public.abet_history enable row level security;
revoke all on public.abet_sources, public.abet_scores, public.abet_files, public.abet_history from anon, authenticated;
-- Chỉ admin (RLS bên dưới); anon không có quyền bảng nào, chỉ gọi hàm abet_nop_*.
grant select, insert, update, delete on public.abet_sources, public.abet_scores, public.abet_files, public.abet_history to authenticated;

drop policy if exists abet_sources_admin on public.abet_sources;
create policy abet_sources_admin on public.abet_sources for all to authenticated
  using ((select public.is_admin())) with check ((select public.is_admin()));
drop policy if exists abet_scores_admin on public.abet_scores;
create policy abet_scores_admin on public.abet_scores for all to authenticated
  using ((select public.is_admin())) with check ((select public.is_admin()));
drop policy if exists abet_files_admin on public.abet_files;
create policy abet_files_admin on public.abet_files for all to authenticated
  using ((select public.is_admin())) with check ((select public.is_admin()));
drop policy if exists abet_history_admin on public.abet_history;
create policy abet_history_admin on public.abet_history for all to authenticated
  using ((select public.is_admin())) with check ((select public.is_admin()));

-- ─────────────────────────── Hàm cho link nộp (anon) ───────────────────────────
-- Token hợp lệ và dòng còn nhận nộp (chưa được điều phối duyệt chốt). Dùng cả trong policy Storage.
create or replace function public.abet_token_mo(p_token text)
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1 from public.abet_sources
    where token = p_token and trang_thai <> 'da_duyet'
  );
$$;

-- Thông tin một dòng cho trang nộp: chỉ trả đúng những gì giáo viên cần, không trả MSSV/điểm đã nộp.
create or replace function public.abet_nop_xem(p_token text)
returns jsonb
language sql
stable
security definer
set search_path = public
as $$
  select jsonb_build_object(
    'ma_dong', s.ma_dong, 'nam_hoc', s.nam_hoc, 'so', s.so, 'pi', s.pi,
    'hoc_ky', s.hoc_ky, 'khoa', s.khoa, 'ma_hp', s.ma_hp, 'hoc_phan', s.hoc_phan,
    'cong_cu', s.cong_cu, 'noi_dung', s.noi_dung, 'diem_toi_da', s.diem_toi_da,
    'chu_pi', s.chu_pi, 'han_nop', s.han_nop, 'trang_thai', s.trang_thai,
    'nop_luc', s.nop_luc, 'nhan_xet_gv', s.nhan_xet_gv, 'ly_do_khong_thu', s.ly_do_khong_thu,
    'so_sv', (select count(*) from public.abet_scores sc where sc.source_id = s.id),
    'so_dat', (select count(*) from public.abet_scores sc
               where sc.source_id = s.id and s.diem_toi_da is not null and sc.diem >= 0.6 * s.diem_toi_da),
    'tep', coalesce((select jsonb_agg(jsonb_build_object('id', f.id, 'loai', f.loai, 'ten_file', f.ten_file) order by f.id)
                     from public.abet_files f where f.source_id = s.id), '[]'::jsonb)
  )
  from public.abet_sources s
  where s.token = p_token;
$$;

-- Nộp (hoặc nộp lại) bảng điểm câu PI: thay toàn bộ điểm cũ của dòng này.
-- p_rows: [{"mssv": "0306241234", "diem": 7.5}, …]
create or replace function public.abet_nop_diem(p_token text, p_diem_toi_da numeric, p_rows jsonb, p_nhan_xet text default null)
returns integer
language plpgsql
security definer
set search_path = public
as $$
declare
  v_id bigint;
  v_n integer;
begin
  select id into v_id from public.abet_sources where token = p_token and trang_thai <> 'da_duyet';
  if v_id is null then
    raise exception 'Link không đúng hoặc dòng này đã được khoá.';
  end if;
  if p_diem_toi_da is null or p_diem_toi_da <= 0 or p_diem_toi_da > 1000 then
    raise exception 'Điểm tối đa của câu PI phải lớn hơn 0.';
  end if;
  if p_rows is null or jsonb_typeof(p_rows) <> 'array' or jsonb_array_length(p_rows) = 0 then
    raise exception 'Chưa có dòng điểm nào.';
  end if;
  if jsonb_array_length(p_rows) > 400 then
    raise exception 'Quá 400 sinh viên trong một lần nộp.';
  end if;
  if exists (
    select 1 from jsonb_array_elements(p_rows) r
    where coalesce(r->>'mssv', '') !~ '^[A-Za-z0-9]{4,20}$'
       or jsonb_typeof(r->'diem') is distinct from 'number'
       or coalesce(case when jsonb_typeof(r->'diem') = 'number' then (r->>'diem')::numeric end, -1) < 0
       or coalesce(case when jsonb_typeof(r->'diem') = 'number' then (r->>'diem')::numeric end, 0) > p_diem_toi_da
  ) then
    raise exception 'Có MSSV sai dạng hoặc điểm nằm ngoài 0 – %.', p_diem_toi_da;
  end if;
  if (select count(distinct r->>'mssv') from jsonb_array_elements(p_rows) r) <> jsonb_array_length(p_rows) then
    raise exception 'Có MSSV bị lặp.';
  end if;

  delete from public.abet_scores where source_id = v_id;
  insert into public.abet_scores (source_id, mssv, diem)
  select v_id, r->>'mssv', round((r->>'diem')::numeric, 2) from jsonb_array_elements(p_rows) r;
  get diagnostics v_n = row_count;

  update public.abet_sources
     set diem_toi_da = p_diem_toi_da,
         nhan_xet_gv = coalesce(nullif(btrim(left(p_nhan_xet, 4000)), ''), nhan_xet_gv),
         trang_thai = 'da_nop',
         ly_do_khong_thu = null,
         nop_luc = now(),
         cap_nhat_luc = now()
   where id = v_id;
  return v_n;
end;
$$;

-- Ghi lại một tệp minh chứng vừa tải lên Storage (đường dẫn phải nằm trong thư mục <token>/).
create or replace function public.abet_nop_tep(p_token text, p_loai text, p_path text, p_ten text, p_mime text, p_size bigint)
returns bigint
language plpgsql
security definer
set search_path = public
as $$
declare
  v_id bigint;
  v_file bigint;
begin
  select id into v_id from public.abet_sources where token = p_token and trang_thai <> 'da_duyet';
  if v_id is null then
    raise exception 'Link không đúng hoặc dòng này đã được khoá.';
  end if;
  if p_path is null or left(p_path, length(p_token) + 1) <> p_token || '/' or p_path like '%..%' then
    raise exception 'Đường dẫn tệp không hợp lệ.';
  end if;
  if (select count(*) from public.abet_files where source_id = v_id) >= 40 then
    raise exception 'Đã đủ 40 tệp cho dòng này.';
  end if;
  insert into public.abet_files (source_id, loai, storage_path, ten_file, mime_type, kich_thuoc)
  values (v_id, p_loai, p_path, left(coalesce(nullif(btrim(p_ten), ''), 'tep'), 200), left(p_mime, 100), p_size)
  returning id into v_file;
  update public.abet_sources set cap_nhat_luc = now() where id = v_id;
  return v_file;
end;
$$;

-- Bỏ một tệp đã nộp nhầm (xoá dòng ghi; tệp trong Storage điều phối dọn sau).
create or replace function public.abet_nop_xoa_tep(p_token text, p_file_id bigint)
returns void
language sql
security definer
set search_path = public
as $$
  delete from public.abet_files f
  using public.abet_sources s
  where f.id = p_file_id and f.source_id = s.id and s.token = p_token and s.trang_thai <> 'da_duyet';
$$;

-- Giáo viên báo không còn dữ liệu (bài thi/điểm từng câu đã mất) — lấy bù năm sau.
-- Chỉ khi dòng CHƯA có bảng điểm: không để link ghi đè dòng đã nộp/đã duyệt.
create or replace function public.abet_nop_khong_thu(p_token text, p_ly_do text)
returns void
language plpgsql
security definer
set search_path = public
as $$
begin
  update public.abet_sources
     set trang_thai = 'khong_thu_duoc',
         ly_do_khong_thu = left(coalesce(nullif(btrim(p_ly_do), ''), 'Không còn dữ liệu'), 1000),
         cap_nhat_luc = now()
   where token = p_token and trang_thai in ('chua_gui', 'da_gui', 'khong_thu_duoc');
  if not found then
    raise exception 'Link không đúng, hoặc dòng này đã có bảng điểm (muốn đổi thì nộp lại bảng điểm).';
  end if;
end;
$$;

revoke all on function public.abet_token_mo(text) from public;
revoke all on function public.abet_nop_xem(text) from public;
revoke all on function public.abet_nop_diem(text, numeric, jsonb, text) from public;
revoke all on function public.abet_nop_tep(text, text, text, text, text, bigint) from public;
revoke all on function public.abet_nop_xoa_tep(text, bigint) from public;
revoke all on function public.abet_nop_khong_thu(text, text) from public;
grant execute on function public.abet_token_mo(text) to anon, authenticated;
grant execute on function public.abet_nop_xem(text) to anon, authenticated;
grant execute on function public.abet_nop_diem(text, numeric, jsonb, text) to anon, authenticated;
grant execute on function public.abet_nop_tep(text, text, text, text, text, bigint) to anon, authenticated;
grant execute on function public.abet_nop_xoa_tep(text, bigint) to anon, authenticated;
grant execute on function public.abet_nop_khong_thu(text, text) to anon, authenticated;

-- ─────────────────────────── Storage ───────────────────────────
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('abet-minh-chung', 'abet-minh-chung', false, 15728640, array[
  'image/jpeg', 'image/png', 'image/webp', 'image/heic', 'application/pdf',
  'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  'application/octet-stream'])
on conflict (id) do update set
  public = excluded.public, file_size_limit = excluded.file_size_limit, allowed_mime_types = excluded.allowed_mime_types;

drop policy if exists "abet nop tep theo link" on storage.objects;
create policy "abet nop tep theo link" on storage.objects
  for insert to anon, authenticated
  with check (bucket_id = 'abet-minh-chung' and public.abet_token_mo((storage.foldername(name))[1]));
drop policy if exists "abet admin doc tep" on storage.objects;
create policy "abet admin doc tep" on storage.objects
  for select to authenticated
  using (bucket_id = 'abet-minh-chung' and public.is_admin());
drop policy if exists "abet admin xoa tep" on storage.objects;
create policy "abet admin xoa tep" on storage.objects
  for delete to authenticated
  using (bucket_id = 'abet-minh-chung' and public.is_admin());

-- ─────────────────────────── Dữ liệu kế hoạch (từ file Excel theo dõi 12/11/2026) ───────────────────────────
insert into public.abet_sources
  (ma_dong, nam_hoc, so, pi, hk_ctdt, hoc_ky, khoa, ma_hp, hoc_phan, cong_cu, noi_dung, phu_trach_so, han_nop, tuy_chon, ghi_chu)
values
  ('2526-1.1a','2025-2026','SO1','PI1.1',1,'HK1','CĐ CK 25','3421030','Cơ lý thuyết','Câu hỏi thi','Câu 1: xác định phản lực liên kết','Đặng Ngọc Lê Văn','2026-11-30',false,null),
  ('2526-1.1b','2025-2026','SO1','PI1.1',3,'HK1','CĐ CK 24','3421070','Nguyên lý máy - Chi tiết máy','Câu hỏi thi','Câu 1a: chiều quay và tốc độ quay của trục','Đặng Ngọc Lê Văn','2026-11-30',false,null),
  ('2526-1.1c','2025-2026','SO1','PI1.1',4,'HK2','CĐ CK 24','3421080','BTL Chi tiết máy','Điểm thành phần','Chọn động cơ điện','Đặng Ngọc Lê Văn','2026-12-15',true,'Tuỳ chọn: PI1.1 đã đủ hai học phần HK1. Năm 2023-2024 dòng này không có dữ liệu.'),
  ('2526-1.2a','2025-2026','SO1','PI1.2',1,'HK1','CĐ CK 25','3221060','Toán cao cấp','Câu hỏi thi','Tổng điểm câu 3 (hình học), 6 (ma trận), 9 (phương trình vi phân)','Đặng Ngọc Lê Văn','2026-11-30',false,null),
  ('2526-1.2b','2025-2026','SO1','PI1.2',1,'HK1','CĐ CK 25','3221090','Vật lý đại cương','Câu hỏi thi','Tổng điểm câu 11 (động năng), 13 (mômen), 14 (sai số)','Đặng Ngọc Lê Văn','2026-11-30',false,null),
  ('2526-1.2c','2025-2026','SO1','PI1.2',3,'HK1','CĐ CK 24','3611320','Ứng dụng CNTT cơ bản','Bài thi thực hành','Điểm phần Excel','Đặng Ngọc Lê Văn','2026-11-30',false,null),
  ('2526-1.3a','2025-2026','SO1','PI1.3',1,'HK1','CĐ CK 25','3322020','Thực tập nguội cơ bản','Rubric','Điểm tổng bài thực hành theo rubric','Đặng Ngọc Lê Văn','2026-11-30',false,null),
  ('2526-1.3b','2025-2026','SO1','PI1.3',3,'HK1','CĐ CK 24','3312012','Thực tập tiện phay 2','Bài thi thực hành','Điểm kỹ thuật (thang 5)','Đặng Ngọc Lê Văn','2026-11-30',false,null),
  ('2526-1.4a','2025-2026','SO1','PI1.4',4,'HK2','CĐ CK 24','3311070','Máy cắt và máy ĐKCTS','Câu hỏi thi','Tổng điểm các câu bài thi','Đặng Ngọc Lê Văn','2026-12-15',true,'Tuỳ chọn: PI1.4 đã có Tiện phay 3 (HK1).'),
  ('2526-1.4b','2025-2026','SO1','PI1.4',5,'HK1','CĐ CK 23','3312013','Thực tập tiện phay 3','Bài thi thực hành','Điểm bài thực hành (kỹ thuật và thành phần)','Đặng Ngọc Lê Văn','2026-11-30',false,null),
  ('2526-2.1','2025-2026','SO2','PI2.1',4,'HK2','CĐ CK 24','3311041','Công nghệ chế tạo máy 1','Câu hỏi thi','Câu 1: phân tích 4 yếu tố độ chính xác gia công','Trần Trọng Thuyết','2026-12-15',false,'Đã có bảng điểm tổng CĐ CK 24E. Cần điểm câu 1 trên bài gốc.'),
  ('2526-2.2','2025-2026','SO2','PI2.2',5,'HK1','CĐ CK 23','3311042','Công nghệ chế tạo máy 2','Câu hỏi thi','Câu lập quy trình công nghệ','Trần Trọng Thuyết','2026-11-30',false,null),
  ('2526-2.3','2025-2026','SO2','PI2.3',5,'HK1','CĐ CK 23','3311080','Đồ gá','Câu hỏi thi','Câu tính lực kẹp cần thiết Wct','Trần Trọng Thuyết','2026-11-30',false,null),
  ('2526-4.1','2025-2026','SO4','PI4.1',6,'HK2','CĐ CK 23','3317010','Đồ án tốt nghiệp','Rubric','Điểm thành phần thuyết minh và bản vẽ','Nguyễn Văn Thông','2026-12-15',false,'Xin phiếu chấm ở văn phòng khoa. Dự phòng: thuyết minh và bản vẽ BTL CNCTM (HK1).'),
  ('2526-4.2','2025-2026','SO4','PI4.2',4,'HK2','CĐ CK 24','3311090','Các phương pháp gia công mới','Báo cáo','Điểm thuyết trình video trước lớp','Nguyễn Văn Thông','2026-12-15',false,'Nếu giáo viên không còn điểm thành phần: Không thu được, lấy bù HK2 2026-2027.'),
  ('2526-4.3','2025-2026','SO4','PI4.3',5,'HK1','CĐ CK 23','3311050','BTL Công nghệ chế tạo máy','Điểm thành phần','Bảng quy trình công nghệ A3','Nguyễn Văn Thông','2026-11-30',false,null),
  ('2627-3.1','2026-2027','SO3','PI3.1',2,'HK2','CĐ CK 26','3311020','Dung sai - Kỹ thuật đo','Câu hỏi thi','Câu 1: bậc dung sai','Dương Văn Ba','2027-06-30',false,'Đưa câu PI vào đề thi ngay từ đầu HK2.'),
  ('2627-3.2','2026-2027','SO3','PI3.2',2,'HK2','CĐ CK 26','3312011','Thực tập tiện phay 1','Bài thi thực hành','Điểm đo lường','Dương Văn Ba','2027-06-30',false,null),
  ('2627-3.3','2026-2027','SO3','PI3.3',1,'HK1','CĐ CK 26','3221090','Vật lý đại cương (thí nghiệm)','Báo cáo thí nghiệm','Điểm báo cáo thí nghiệm vật lý','Dương Văn Ba','2027-01-31',false,'Đang học HK1 2026-2027: gửi mẫu cho giáo viên trước kì thi.'),
  ('2627-5.1','2026-2027','SO5','PI5.1',3,'HK1','CĐ CK 25',null,'Giáo dục đạo đức và phát triển nghề nghiệp','Trắc nghiệm','Điểm trắc nghiệm chủ đề 5 (làm việc nhóm)','Nguyễn Đức Tài 91','2027-01-31',false,'Đang học HK1 2026-2027: gửi mẫu cho giáo viên trước kì thi.'),
  ('2627-5.2a','2026-2027','SO5','PI5.2',2,'HK2','CĐ CK 26','3322030','Thực tập nguội tháo lắp','Bài thi thực hành','Điểm làm việc nhóm','Nguyễn Đức Tài 91','2027-06-30',false,null),
  ('2627-5.2b','2026-2027','SO5','PI5.2',6,'HK2','CĐ CK 24','3315010','Thực tập tốt nghiệp','Báo cáo','Điểm tổng kết thực tập','Nguyễn Đức Tài 91','2027-03-31',false,'Thực tập từ giữa tháng 12, 6 tuần trước Tết và 6 tuần sau Tết.'),
  ('2627-5.3','2026-2027','SO5','PI5.3',6,'HK2','CĐ CK 24','3317010','Đồ án tốt nghiệp','Rubric','Điểm thành phần lập kế hoạch do giáo viên hướng dẫn chấm','Nguyễn Đức Tài 91','2027-06-30',false,null)
on conflict (ma_dong) do nothing;

insert into public.abet_history (nam_hoc, ma, ti_le, nguon) values
  ('2023-2024','PI1.1',0.3793,'Outcome 1.xlsx 2023-2024'),
  ('2023-2024','PI1.2',0.6434,'Outcome 1.xlsx 2023-2024'),
  ('2023-2024','PI1.3',0.7258,'Outcome 1.xlsx 2023-2024'),
  ('2023-2024','PI1.4',0.6714,'Outcome 1.xlsx 2023-2024'),
  ('2023-2024','PI2.1',0.7000,'Outcome 2.xlsx 2023-2024'),
  ('2023-2024','PI2.2',0.4310,'Outcome 2.xlsx 2023-2024'),
  ('2023-2024','PI2.3',0.4821,'Outcome 2.xlsx 2023-2024'),
  ('2023-2024','PI4.1',0.7600,'Outcome 4.xlsx 2023-2024'),
  ('2023-2024','PI4.2',0.8846,'Outcome 4.xlsx 2023-2024'),
  ('2023-2024','PI4.3',0.8000,'Outcome 4.xlsx 2023-2024'),
  ('2023-2024','SO1',0.5831,'Outcome 1.xlsx 2023-2024'),
  ('2023-2024','SO2',0.5195,'Outcome 2.xlsx 2023-2024'),
  ('2023-2024','SO4',0.8455,'Outcome 4.xlsx 2023-2024'),
  ('2022-2023','PI3.1',0.70,'Slide ABET và quy trình cải tiến hằng năm (12/2025)'),
  ('2022-2023','PI3.2',0.97,'Slide ABET và quy trình cải tiến hằng năm (12/2025)'),
  ('2022-2023','PI3.3',0.90,'Slide ABET và quy trình cải tiến hằng năm (12/2025)'),
  ('2022-2023','PI5.1',0.56,'Slide ABET và quy trình cải tiến hằng năm (12/2025)'),
  ('2022-2023','PI5.2',0.73,'Slide ABET và quy trình cải tiến hằng năm (12/2025)'),
  ('2022-2023','PI5.3',0.71,'Slide ABET và quy trình cải tiến hằng năm (12/2025)'),
  ('2024-2025','PI3.1',0.83,'Slide ABET và quy trình cải tiến hằng năm (12/2025)'),
  ('2024-2025','PI3.2',0.93,'Slide ABET và quy trình cải tiến hằng năm (12/2025)'),
  ('2024-2025','PI3.3',0.82,'Slide ABET và quy trình cải tiến hằng năm (12/2025)'),
  ('2024-2025','PI5.1',0.87,'Slide ABET và quy trình cải tiến hằng năm (12/2025)'),
  ('2024-2025','PI5.2',0.84,'Slide ABET và quy trình cải tiến hằng năm (12/2025)'),
  ('2024-2025','PI5.3',0.80,'Slide ABET và quy trình cải tiến hằng năm (12/2025)')
on conflict (nam_hoc, ma) do nothing;

-- ─────────────────────────── ROLLBACK ───────────────────────────
-- (Bucket chỉ xoá được khi đã trống: xoá tệp trong 'abet-minh-chung' qua Storage trước.)
-- drop policy if exists "abet nop tep theo link" on storage.objects;
-- drop policy if exists "abet admin doc tep" on storage.objects;
-- drop policy if exists "abet admin xoa tep" on storage.objects;
-- delete from storage.buckets where id = 'abet-minh-chung';
-- drop function if exists public.abet_nop_khong_thu(text, text);
-- drop function if exists public.abet_nop_xoa_tep(text, bigint);
-- drop function if exists public.abet_nop_tep(text, text, text, text, text, bigint);
-- drop function if exists public.abet_nop_diem(text, numeric, jsonb, text);
-- drop function if exists public.abet_nop_xem(text);
-- drop function if exists public.abet_token_mo(text);
-- drop table if exists public.abet_files, public.abet_scores, public.abet_history, public.abet_sources;
