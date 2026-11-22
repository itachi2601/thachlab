-- Lượt xem khung video thí nghiệm (Việc 6, docs/KE-HOACH-CAI-TIEN-CLIP-2026-11-19.md).
-- MỖI LƯỢT XEM một dòng: Dự đoán (chọn / bỏ qua), câu chốt (chọn / bỏ qua), số lần tua lại, xem hết, giây xa nhất.
-- Client (components/lessons/VideoThiNghiemKhung.tsx) sinh luot_id = crypto.randomUUID() khi mở khung, gửi lặp
-- nhiều lần cùng luot_id (ẩn tab, rời trang, xem hết) — mỗi lần là ẢNH CHỤP ĐẦY ĐỦ; server UPSERT gộp đơn điệu.
-- Gửi bằng RPC riêng log_clip_view lúc rời/xem hết, KHÔNG thêm round-trip khi tải /lop-hoc/bai.
-- Không đụng log_learning_events, không đụng lesson_clip_choices (bảng đó giữ lần ĐẦU mỗi HS / tn_id).
--
-- Payload log_clip_view(p jsonb), khoá camelCase:
--   {"luotId":"<uuid>","lessonId":12,"tnId":"nemngang-01","banClip":"tn-l12-nemngang-01-20261101.mp4",
--    "coCauChot":true,
--    "duDoan":2|null,"duDoanBoQua":false,"duDoanDung":true|null,
--    "chot":1|null,"chotBoQua":false,"chotDung":false|null,
--    "soXemLai":1,"xemHet":true,"giayMax":42.3,"batDau":"2026-11-20T08:00:00Z"}
--   duDoan null & duDoanBoQua false = chưa tới điểm dừng, hoặc đã trả lời ở lượt trước trong cùng trang.
--
-- Kiểm đầu vào (sai → return 0, KHÔNG raise, để không làm hỏng trang đang học):
--   * luotId dạng uuid; lessonId số nguyên và bài tồn tại (kiểm trước insert); tnId ~ '^[a-z0-9-]{1,60}$';
--     banClip ~ '^[a-z0-9._-]{1,100}$'; coCauChot boolean JSON (bắt buộc).
--   * duDoan/chot: số JSON 0..3 hoặc null/thiếu; *BoQua/*Dung/xemHet: boolean JSON hoặc null/thiếu.
--     Chuỗi "2", 1.5, 4, "true" → bỏ cả lần gửi.
--   * Chuẩn hoá (không coi là sai): đã chọn thì *BoQua ép false; chưa chọn thì *Dung ép null;
--     coCauChot=false thì chot/chotBoQua/chotDung ép null/false.
--   * soXemLai số nguyên >= 0, cắt ở 500; giayMax số >= 0, cắt ở 3600, làm tròn 0,1 s; thiếu → 0.
--   * batDau ngoài [now-1 ngày, now+5 phút] hoặc không đọc được → now().
--   * Chưa đăng nhập → 42501. Tài khoản staff (is_staff: admin/GV/TA) xem thử → return 0, không ghi.
--
-- Upsert on conflict (luot_id) do update CHỈ khi dòng là của chính HS (student_id = auth.uid()) và so_lan_gui < 200
-- (chặn spam). Gộp: du_doan/chot giữ giá trị có trước (coalesce(cũ, mới)) cùng *_dung đi kèm; bo_qua = cũ or mới,
-- nhưng đã có lựa chọn thì false; so_xem_lai/giay_max greatest; xem_het or; bat_dau least; cap_nhat now();
-- so_lan_gui + 1. tn_id/ban_clip/lesson_id giữ theo lần gửi đầu. Return 1 khi ghi, 0 khi bỏ.
--
-- Giữ DB không phình (quy tắc rollup > 12 tháng): rollup_lesson_clip_views() cộng dồn các THÁNG TRỌN VẸN
-- (giờ VN) cũ hơn mốc vào lesson_clip_view_rollups rồi xoá dòng gốc trong cùng một câu lệnh;
-- pg_cron '50 20 1 * *' = 3:50 VN rạng sáng ngày 2 hằng tháng (khác 20:00/20:30/20:45 của các job hiện có).
-- Mốc làm tròn về đầu tháng nên một tháng chỉ được gộp một lần → so_hs (HS khác nhau) trong tháng là chính xác.
--
-- Ai đọc / ghi được gì:
--   | Vai                               | lesson_clip_views (đọc)                       | lesson_clip_view_rollups (đọc) | Ghi                                     |
--   |-----------------------------------|-----------------------------------------------|--------------------------------|-----------------------------------------|
--   | anon                              | không                                         | không                          | không (RPC không grant cho anon)        |
--   | Học sinh                          | dòng của mình                                 | không                          | chỉ qua log_clip_view, student_id = auth.uid(); không đụng được luot_id của HS khác |
--   | Giảng viên (class_instructors)    | HS các lớp mình dạy (teaches_student)         | có (is_staff, chỉ số đếm)      | không (is_staff → return 0)             |
--   | Trợ giảng đang hoạt động          | mọi HS (teaches_student, như learning_events) | có                             | không                                   |
--   | Admin                             | tất cả                                        | có                             | không (trừ rollup chạy bằng cron/postgres) |
--   Không ai insert/update/delete trực tiếp bảng (revoke all, chỉ grant select).
--
-- Phụ thuộc: profiles, lessons, teaches_student(), is_admin(), is_staff() (đã có). Chạy giờ nào cũng được
-- (chỉ tạo bảng/hàm mới, không đụng dữ liệu cũ); khuyên sau 22h theo thói quen. Rollback ở cuối file.

begin;

-- ---------- 1. Bảng lượt xem ----------
create table if not exists public.lesson_clip_views (
  luot_id        uuid primary key,
  student_id     uuid not null references public.profiles(id) on delete cascade,
  tn_id          text not null check (tn_id ~ '^[a-z0-9-]{1,60}$'),
  lesson_id      bigint not null references public.lessons(id) on delete cascade,
  ban_clip       text not null check (ban_clip ~ '^[a-z0-9._-]{1,100}$'),
  co_cau_chot    boolean not null,
  du_doan        smallint check (du_doan is null or du_doan between 0 and 3),
  du_doan_bo_qua boolean not null default false,
  du_doan_dung   boolean,
  chot           smallint check (chot is null or chot between 0 and 3),
  chot_bo_qua    boolean not null default false,
  chot_dung      boolean,
  so_xem_lai     smallint not null default 0 check (so_xem_lai between 0 and 500),
  xem_het        boolean not null default false,
  giay_max       numeric(6,1) not null default 0 check (giay_max between 0 and 3600),
  bat_dau        timestamptz not null default now(),
  cap_nhat       timestamptz not null default now(),
  so_lan_gui     integer not null default 1 check (so_lan_gui >= 1),
  -- nhất quán: không vừa chọn vừa bỏ qua; *_dung null khi chưa chọn; clip không có câu chốt thì không có lựa chọn chốt
  constraint lesson_clip_views_du_doan_ck check (not (du_doan is not null and du_doan_bo_qua)
                                                 and (du_doan is not null or du_doan_dung is null)),
  constraint lesson_clip_views_chot_ck    check (not (chot is not null and chot_bo_qua)
                                                 and (chot is not null or chot_dung is null)),
  constraint lesson_clip_views_co_chot_ck check (co_cau_chot or (chot is null and not chot_bo_qua))
);
create index if not exists lesson_clip_views_clip_idx    on public.lesson_clip_views (tn_id, ban_clip);
create index if not exists lesson_clip_views_time_idx    on public.lesson_clip_views (bat_dau);
create index if not exists lesson_clip_views_student_idx on public.lesson_clip_views (student_id);

alter table public.lesson_clip_views enable row level security;
revoke all on public.lesson_clip_views from anon, authenticated;
grant select on public.lesson_clip_views to authenticated;

drop policy if exists "hs xem luot xem clip cua minh" on public.lesson_clip_views;
create policy "hs xem luot xem clip cua minh" on public.lesson_clip_views
  as permissive for select to authenticated
  using (student_id = (select auth.uid()));

drop policy if exists "giao vien xem luot xem clip cua lop" on public.lesson_clip_views;
create policy "giao vien xem luot xem clip cua lop" on public.lesson_clip_views
  as permissive for select to authenticated
  using (public.teaches_student(student_id) or public.is_admin());

-- ---------- 2. Bảng cộng dồn theo tháng (dữ liệu > 12 tháng) ----------
create table if not exists public.lesson_clip_view_rollups (
  thang           date not null,              -- ngày 1 của tháng (giờ VN)
  tn_id           text not null,
  ban_clip        text not null,
  so_luot         integer not null default 0,
  so_hs           integer not null default 0, -- HS khác nhau trong tháng
  du_doan_tra_loi integer not null default 0, -- số lượt đã chọn Dự đoán
  du_doan_dung    integer not null default 0,
  du_doan_bo_qua  integer not null default 0,
  chot_co         integer not null default 0, -- số lượt ở clip có câu chốt
  chot_tra_loi    integer not null default 0,
  chot_dung       integer not null default 0,
  chot_bo_qua     integer not null default 0,
  xem_het         integer not null default 0,
  primary key (thang, tn_id, ban_clip)
);

alter table public.lesson_clip_view_rollups enable row level security;
revoke all on public.lesson_clip_view_rollups from anon, authenticated;
grant select on public.lesson_clip_view_rollups to authenticated;

drop policy if exists "staff xem tong hop luot xem clip" on public.lesson_clip_view_rollups;
create policy "staff xem tong hop luot xem clip" on public.lesson_clip_view_rollups
  as permissive for select to authenticated
  using (public.is_admin() or public.is_staff());

-- ---------- 3. RPC ghi lượt xem ----------
create or replace function public.log_clip_view(p jsonb)
returns integer
language plpgsql security definer set search_path = public, pg_temp
as $$
declare
  v_uid uuid := auth.uid();
  v_luot uuid;
  v_lesson bigint;
  v_tn text;
  v_ban text;
  v_co_chot boolean;
  v_dd smallint; v_dd_bq boolean; v_dd_dung boolean;
  v_ch smallint; v_ch_bq boolean; v_ch_dung boolean;
  v_xl integer;
  v_het boolean;
  v_giay numeric;
  v_at timestamptz;
  v_n integer;
begin
  if v_uid is null then
    raise exception 'Chưa đăng nhập' using errcode = '42501';
  end if;
  if p is null or jsonb_typeof(p) <> 'object' then
    return 0;
  end if;
  if public.is_staff() then
    return 0;  -- admin/GV/TA xem thử bài: không ghi
  end if;

  -- định danh
  if coalesce(p ->> 'luotId', '') !~* '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' then
    return 0;
  end if;
  v_luot := (p ->> 'luotId')::uuid;
  v_tn := p ->> 'tnId';
  if v_tn is null or v_tn !~ '^[a-z0-9-]{1,60}$' then return 0; end if;
  v_ban := p ->> 'banClip';
  if v_ban is null or v_ban !~ '^[a-z0-9._-]{1,100}$' then return 0; end if;
  if jsonb_typeof(p -> 'lessonId') is distinct from 'number' or (p ->> 'lessonId') !~ '^[0-9]{1,18}$' then
    return 0;
  end if;
  v_lesson := (p ->> 'lessonId')::bigint;
  if not exists (select 1 from public.lessons l where l.id = v_lesson) then return 0; end if;
  if jsonb_typeof(p -> 'coCauChot') is distinct from 'boolean' then return 0; end if;
  v_co_chot := (p -> 'coCauChot')::boolean;

  -- lựa chọn: số JSON 0..3 hoặc null/thiếu
  if coalesce(jsonb_typeof(p -> 'duDoan'), 'null') = 'null' then
    v_dd := null;
  elsif jsonb_typeof(p -> 'duDoan') = 'number' and (p ->> 'duDoan') in ('0', '1', '2', '3') then
    v_dd := (p ->> 'duDoan')::smallint;
  else
    return 0;
  end if;
  if coalesce(jsonb_typeof(p -> 'chot'), 'null') = 'null' then
    v_ch := null;
  elsif jsonb_typeof(p -> 'chot') = 'number' and (p ->> 'chot') in ('0', '1', '2', '3') then
    v_ch := (p ->> 'chot')::smallint;
  else
    return 0;
  end if;

  -- boolean JSON hoặc null/thiếu
  if coalesce(jsonb_typeof(p -> 'duDoanBoQua'), 'null') not in ('null', 'boolean')
     or coalesce(jsonb_typeof(p -> 'duDoanDung'), 'null') not in ('null', 'boolean')
     or coalesce(jsonb_typeof(p -> 'chotBoQua'), 'null') not in ('null', 'boolean')
     or coalesce(jsonb_typeof(p -> 'chotDung'), 'null') not in ('null', 'boolean')
     or coalesce(jsonb_typeof(p -> 'xemHet'), 'null') not in ('null', 'boolean') then
    return 0;
  end if;
  v_dd_bq   := coalesce((p ->> 'duDoanBoQua')::boolean, false);
  v_dd_dung := (p ->> 'duDoanDung')::boolean;
  v_ch_bq   := coalesce((p ->> 'chotBoQua')::boolean, false);
  v_ch_dung := (p ->> 'chotDung')::boolean;
  v_het     := coalesce((p ->> 'xemHet')::boolean, false);

  -- chuẩn hoá cho khớp ràng buộc nhất quán
  if v_dd is not null then v_dd_bq := false; else v_dd_dung := null; end if;
  if not v_co_chot then
    v_ch := null; v_ch_bq := false; v_ch_dung := null;
  elsif v_ch is not null then
    v_ch_bq := false;
  else
    v_ch_dung := null;
  end if;

  -- số đếm
  if coalesce(jsonb_typeof(p -> 'soXemLai'), 'null') = 'null' then
    v_xl := 0;
  elsif jsonb_typeof(p -> 'soXemLai') = 'number' and (p ->> 'soXemLai') ~ '^[0-9]{1,9}$' then
    v_xl := least((p ->> 'soXemLai')::integer, 500);
  else
    return 0;
  end if;
  if coalesce(jsonb_typeof(p -> 'giayMax'), 'null') = 'null' then
    v_giay := 0;
  elsif jsonb_typeof(p -> 'giayMax') = 'number' and (p ->> 'giayMax') ~ '^[0-9]{1,9}(\.[0-9]+)?$' then
    v_giay := round(least((p ->> 'giayMax')::numeric, 3600), 1);
  else
    return 0;
  end if;

  begin
    v_at := (p ->> 'batDau')::timestamptz;
  exception when others then
    v_at := null;
  end;
  if v_at is null or v_at > now() + interval '5 minutes' or v_at < now() - interval '1 day' then
    v_at := now();
  end if;

  -- Chặn spam lượt MỚI: tối đa 300 lượt / HS / 24 giờ (một buổi học thật chỉ vài chục). Lượt đã có vẫn cập nhật được.
  if not exists (select 1 from public.lesson_clip_views x where x.luot_id = v_luot)
     and (select count(*) from public.lesson_clip_views x
          where x.student_id = v_uid and x.cap_nhat > now() - interval '24 hours') >= 300 then
    return 0;
  end if;

  insert into public.lesson_clip_views as t
    (luot_id, student_id, tn_id, lesson_id, ban_clip, co_cau_chot,
     du_doan, du_doan_bo_qua, du_doan_dung, chot, chot_bo_qua, chot_dung,
     so_xem_lai, xem_het, giay_max, bat_dau, cap_nhat, so_lan_gui)
  values
    (v_luot, v_uid, v_tn, v_lesson, v_ban, v_co_chot,
     v_dd, v_dd_bq, v_dd_dung, v_ch, v_ch_bq, v_ch_dung,
     v_xl, v_het, v_giay, v_at, now(), 1)
  on conflict (luot_id) do update set
    co_cau_chot    = t.co_cau_chot or excluded.co_cau_chot,
    du_doan        = coalesce(t.du_doan, excluded.du_doan),
    du_doan_dung   = case when t.du_doan is not null then t.du_doan_dung else excluded.du_doan_dung end,
    du_doan_bo_qua = case when coalesce(t.du_doan, excluded.du_doan) is not null then false
                          else t.du_doan_bo_qua or excluded.du_doan_bo_qua end,
    chot           = coalesce(t.chot, excluded.chot),
    chot_dung      = case when t.chot is not null then t.chot_dung else excluded.chot_dung end,
    chot_bo_qua    = case when coalesce(t.chot, excluded.chot) is not null then false
                          else t.chot_bo_qua or excluded.chot_bo_qua end,
    so_xem_lai     = greatest(t.so_xem_lai, excluded.so_xem_lai),
    xem_het        = t.xem_het or excluded.xem_het,
    giay_max       = greatest(t.giay_max, excluded.giay_max),
    bat_dau        = least(t.bat_dau, excluded.bat_dau),
    cap_nhat       = now(),
    so_lan_gui     = t.so_lan_gui + 1
  where t.student_id = excluded.student_id   -- luot_id của HS khác: không đụng
    and t.so_lan_gui < 200;                  -- chặn spam
  get diagnostics v_n = row_count;
  return v_n;
exception when foreign_key_violation or check_violation then
  -- bài bị xoá giữa chừng / dữ liệu lệch ràng buộc: bỏ êm, không làm hỏng trang đang học
  return 0;
end;
$$;
revoke all on function public.log_clip_view(jsonb) from public, anon;
grant execute on function public.log_clip_view(jsonb) to authenticated;

-- ---------- 4. Cộng dồn + xoá dữ liệu > 12 tháng ----------
-- Chỉ gộp các tháng TRỌN VẸN (giờ VN) trước mốc; trả số dòng gốc đã xoá.
create or replace function public.rollup_lesson_clip_views(p_before timestamptz default (now() - interval '12 months'))
returns bigint
language plpgsql security definer set search_path = public, pg_temp
as $$
declare
  v_cut timestamptz;
  v_n bigint;
begin
  v_cut := date_trunc('month', p_before at time zone 'Asia/Ho_Chi_Minh') at time zone 'Asia/Ho_Chi_Minh';
  with d as (
    delete from public.lesson_clip_views where bat_dau < v_cut
    returning *
  ), ins as (
    insert into public.lesson_clip_view_rollups as r
      (thang, tn_id, ban_clip, so_luot, so_hs, du_doan_tra_loi, du_doan_dung, du_doan_bo_qua,
       chot_co, chot_tra_loi, chot_dung, chot_bo_qua, xem_het)
    select date_trunc('month', d.bat_dau at time zone 'Asia/Ho_Chi_Minh')::date, d.tn_id, d.ban_clip,
           count(*)::int,
           count(distinct d.student_id)::int,
           count(d.du_doan)::int,
           count(*) filter (where d.du_doan_dung)::int,
           count(*) filter (where d.du_doan_bo_qua)::int,
           count(*) filter (where d.co_cau_chot)::int,
           count(d.chot)::int,
           count(*) filter (where d.chot_dung)::int,
           count(*) filter (where d.chot_bo_qua)::int,
           count(*) filter (where d.xem_het)::int
    from d
    group by 1, 2, 3
    on conflict (thang, tn_id, ban_clip) do update set
      so_luot         = r.so_luot + excluded.so_luot,
      so_hs           = r.so_hs + excluded.so_hs,
      du_doan_tra_loi = r.du_doan_tra_loi + excluded.du_doan_tra_loi,
      du_doan_dung    = r.du_doan_dung + excluded.du_doan_dung,
      du_doan_bo_qua  = r.du_doan_bo_qua + excluded.du_doan_bo_qua,
      chot_co         = r.chot_co + excluded.chot_co,
      chot_tra_loi    = r.chot_tra_loi + excluded.chot_tra_loi,
      chot_dung       = r.chot_dung + excluded.chot_dung,
      chot_bo_qua     = r.chot_bo_qua + excluded.chot_bo_qua,
      xem_het         = r.xem_het + excluded.xem_het
    returning 1
  )
  select count(*) into v_n from d;
  return v_n;
end;
$$;
revoke all on function public.rollup_lesson_clip_views(timestamptz) from public, anon, authenticated;

commit;

-- ---------- 5. Lịch pg_cron (ngoài giao dịch, như 20261030120000) ----------
do $$
begin
  if exists (select 1 from pg_extension where extname = 'pg_cron') then
    perform cron.unschedule(jobid) from cron.job where jobname = 'lesson-clip-views-rollup';
    perform cron.schedule('lesson-clip-views-rollup', '50 20 1 * *', 'select public.rollup_lesson_clip_views();');
    raise notice 'Đã đặt lịch pg_cron lesson-clip-views-rollup (3:50 VN rạng sáng ngày 2 hằng tháng)';
  else
    raise notice 'pg_cron chưa bật: chạy tay select public.rollup_lesson_clip_views(); mỗi học kì';
  end if;
end $$;

-- ---------- KIỂM THỬ (chạy trong giao dịch rồi rollback; thay <...> bằng id thật) ----------
-- begin;
--   set local role authenticated;
--   -- Học sinh: lần 1 chỉ có Dự đoán → 1; lần 2 cùng luot_id đổi đáp án + xem hết → 1, du_doan giữ 2
--   select set_config('request.jwt.claims', '{"sub":"<uuid_hs>","role":"authenticated"}', true);
--   select public.log_clip_view('{"luotId":"00000000-0000-4000-8000-000000000001","lessonId":<lesson>,"tnId":"thu-nghiem-01",
--     "banClip":"tn-thu-01.mp4","coCauChot":true,"duDoan":2,"duDoanDung":false,"soXemLai":0,"giayMax":12.34}');   -- 1
--   select public.log_clip_view('{"luotId":"00000000-0000-4000-8000-000000000001","lessonId":<lesson>,"tnId":"thu-nghiem-01",
--     "banClip":"tn-thu-01.mp4","coCauChot":true,"duDoan":0,"duDoanDung":true,"chot":null,"chotBoQua":true,
--     "soXemLai":3,"xemHet":true,"giayMax":5}');                                                                 -- 1
--   select du_doan, du_doan_dung, chot_bo_qua, so_xem_lai, xem_het, giay_max, so_lan_gui from public.lesson_clip_views;
--     -- kỳ vọng (2, false, true, 3, true, 12.3, 2), chỉ dòng của HS này
--   select public.log_clip_view('{"luotId":"x","lessonId":<lesson>,"tnId":"a","banClip":"a.mp4","coCauChot":true}');  -- 0 (luotId sai)
--   select public.log_clip_view('{"luotId":"00000000-0000-4000-8000-000000000002","lessonId":<lesson>,"tnId":"a",
--     "banClip":"a.mp4","coCauChot":true,"duDoan":"1"}');                                                        -- 0 (chuỗi)
--   insert into public.lesson_clip_views (luot_id, student_id, tn_id, lesson_id, ban_clip, co_cau_chot)
--     values (gen_random_uuid(), '<uuid_hs>', 'x', <lesson>, 'x.mp4', true);                                   -- permission denied
--   select count(*) from public.lesson_clip_view_rollups;                                                      -- 0 (HS không đọc)
--   -- HS khác gửi trùng luot_id của HS trên: 0, dòng không đổi
--   select set_config('request.jwt.claims', '{"sub":"<uuid_hs_khac>","role":"authenticated"}', true);
--   select public.log_clip_view('{"luotId":"00000000-0000-4000-8000-000000000001","lessonId":<lesson>,"tnId":"thu-nghiem-01",
--     "banClip":"tn-thu-01.mp4","coCauChot":true,"soXemLai":99}');                                              -- 0
--   select count(*) from public.lesson_clip_views;                                                             -- 0 (không thấy dòng HS khác)
--   -- Trợ giảng (ta_assistants.active): đọc được, ghi bị bỏ
--   select set_config('request.jwt.claims', '{"sub":"<uuid_tro_giang>","role":"authenticated"}', true);
--   select count(*) from public.lesson_clip_views where luot_id = '00000000-0000-4000-8000-000000000001';      -- 1
--   select public.log_clip_view('{"luotId":"00000000-0000-4000-8000-000000000003","lessonId":<lesson>,"tnId":"a",
--     "banClip":"a.mp4","coCauChot":false}');                                                                   -- 0
--   -- Admin: đọc tất cả + rollups
--   select set_config('request.jwt.claims', '{"sub":"<uuid_admin>","role":"authenticated"}', true);
--   select count(*) from public.lesson_clip_views; select count(*) from public.lesson_clip_view_rollups;
--   -- anon
--   reset role; set local role anon;
--   select count(*) from public.lesson_clip_views;                                                             -- permission denied
-- rollback;

-- ---------- ROLLBACK (cũng có ở perf/rollback/20261120120000_lesson_clip_views.down.sql) ----------
-- do $$ begin
--   if exists (select 1 from pg_extension where extname = 'pg_cron') then
--     perform cron.unschedule(jobid) from cron.job where jobname = 'lesson-clip-views-rollup';
--   end if;
-- end $$;
-- drop function if exists public.rollup_lesson_clip_views(timestamptz);
-- drop function if exists public.log_clip_view(jsonb);
-- drop table if exists public.lesson_clip_view_rollups;
-- drop table if exists public.lesson_clip_views;
