-- ============================================================================
-- Ôn 5 phút — lịch ôn giãn cách theo từng thẻ (25/11/2026)
-- Thẻ ôn là JSON tĩnh trong repo (content/on-tap/<slug>.json, mỗi thẻ có id ngắn). DB chỉ lưu trạng thái
-- học của từng người với từng thẻ: bậc (1..5), hạn ôn, số lần ôn/quên.
--
-- Bảng mới: public.on_tap_the — RLS bật, KHÔNG có policy, revoke hết anon/authenticated → chỉ vào qua 3 RPC.
-- RPC (security definer, search_path = public, luôn lọc theo auth.uid()):
--   on_tap_ghi(p_slug text, p_ket_qua jsonb) returns void
--       p_ket_qua = [{"id":"a1b2c3d4","danh_gia":"nho"|"lomo"|"quen"}, …]; lấy tối đa 40 phần tử đầu, bỏ phần tử
--       sai định dạng; cùng id lặp trong một lượt → chỉ tính lần cuối.
--       Thẻ mới coi như bac = 0. nho → least(bac+1, 5) nếu đã tới hạn, chưa tới hạn thì giữ bậc; lomo → greatest(bac, 1); quen → 1 và lan_quen + 1.
--       han_on = now() + {1:1, 2:3, 3:7, 4:21, 5:60} ngày theo bac SAU cập nhật; lan_on + 1; lan_cuoi = now().
--   on_tap_den_han(p_limit int default 8) returns table(slug, the_id, bac, han_on, tong_den_han)
--   on_tap_trang_thai(p_slug text) returns table(the_id, bac, han_on)
--
-- Ai đọc/ghi được gì:
-- | Vai                 | Bảng on_tap_the trực tiếp | on_tap_ghi                     | on_tap_den_han / on_tap_trang_thai |
-- |---------------------|---------------------------|--------------------------------|------------------------------------|
-- | HS                  | không (revoke, không policy) | ghi thẻ của CHÍNH mình        | đọc thẻ của CHÍNH mình             |
-- | Trợ giảng / GV      | không                     | ghi thẻ của CHÍNH mình         | đọc thẻ của CHÍNH mình (không thấy HS) |
-- | Admin (đăng nhập web)| không                    | như trên                       | như trên                           |
-- | Phụ huynh           | không                     | như trên (vô hại)              | như trên                           |
-- | anon                | không                     | không (revoke execute)         | không                              |
-- | service_role / SQL Editor | toàn quyền (bỏ qua RLS) | —                           | —                                  |
-- Không hàm nào nhận user_id từ client → không có đường ghi/đọc thẻ người khác.
--
-- Nặng không: chỉ tạo 1 bảng rỗng + 3 hàm → chạy giờ nào cũng được.
-- Kiểm thử + rollback: cuối file.
-- ============================================================================
begin;

create table if not exists public.on_tap_the (
  user_id   uuid        not null references auth.users(id) on delete cascade,
  slug      text        not null check (char_length(slug) between 1 and 80),
  the_id    text        not null check (char_length(the_id) between 1 and 16),
  bac       smallint    not null default 1 check (bac between 1 and 5),
  han_on    timestamptz not null,
  lan_on    int         not null default 0,
  lan_quen  int         not null default 0,
  lan_cuoi  timestamptz not null default now(),
  primary key (user_id, slug, the_id)
);

create index if not exists on_tap_the_user_han_on_idx on public.on_tap_the (user_id, han_on);

alter table public.on_tap_the enable row level security;
revoke all on table public.on_tap_the from anon, authenticated;

comment on table public.on_tap_the is
  'Ôn 5 phút: trạng thái lịch ôn giãn cách của từng người với từng thẻ (thẻ là JSON tĩnh content/on-tap/<slug>.json). Chỉ truy cập qua RPC on_tap_ghi / on_tap_den_han / on_tap_trang_thai.';

-- ---------------------------------------------------------------------------
-- Ghi kết quả một lượt ôn
-- ---------------------------------------------------------------------------
create or replace function public.on_tap_ghi(p_slug text, p_ket_qua jsonb)
returns void
language plpgsql volatile security definer set search_path = public
as $$
declare
  v_uid uuid := (select auth.uid());
  v_so_the int;
  r record;
begin
  if v_uid is null then raise exception 'Cần đăng nhập' using errcode = '42501'; end if;
  if p_slug is null or p_slug !~ '^[a-z0-9][a-z0-9-]{0,79}$' then
    raise exception 'slug không hợp lệ' using errcode = '22023';
  end if;
  if p_ket_qua is null or jsonb_typeof(p_ket_qua) <> 'array' then
    raise exception 'p_ket_qua phải là mảng' using errcode = '22023';
  end if;

  -- Chặn phình bảng: mỗi tài khoản tối đa 5.000 thẻ (đủ cho mọi bài của 3 khối). Vượt thì chỉ cập nhật thẻ đã có.
  select count(*) into v_so_the from public.on_tap_the where user_id = v_uid;

  for r in
    select distinct on (e ->> 'id') e ->> 'id' as the_id, e ->> 'danh_gia' as dg
    from jsonb_array_elements(p_ket_qua) with ordinality as x(e, ord)
    where x.ord <= 40
      and jsonb_typeof(x.e) = 'object'
      and jsonb_typeof(x.e -> 'id') = 'string'
      and (x.e ->> 'id') ~ '^[A-Za-z0-9_-]{1,16}$'
      and (x.e ->> 'danh_gia') in ('nho', 'lomo', 'quen')
    order by e ->> 'id', x.ord desc
  loop
    if v_so_the >= 5000
       and not exists (select 1 from public.on_tap_the t
                       where t.user_id = v_uid and t.slug = p_slug and t.the_id = r.the_id) then
      continue;
    end if;

    -- Thẻ mới (bac = 0 trước cập nhật): cả 3 đánh giá đều ra bac 1 → hạn 1 ngày.
    -- Nhớ rõ khi CHƯA tới hạn (ôn sớm, ôn lại cả bài nhiều lần trong ngày) thì giữ bậc — khỏi leo bậc ảo.
    insert into public.on_tap_the as t (user_id, slug, the_id, bac, han_on, lan_on, lan_quen, lan_cuoi)
    values (v_uid, p_slug, r.the_id, 1, now() + interval '1 day', 1, case when r.dg = 'quen' then 1 else 0 end, now())
    on conflict (user_id, slug, the_id) do update
      set bac = case r.dg when 'nho'  then case when t.han_on <= now() then least(t.bac + 1, 5) else t.bac end
                          when 'lomo' then greatest(t.bac, 1)
                          else 1 end,
          han_on = now() + make_interval(days => (array[1, 3, 7, 21, 60])[
                     case r.dg when 'nho'  then case when t.han_on <= now() then least(t.bac + 1, 5) else t.bac end
                               when 'lomo' then greatest(t.bac, 1)
                               else 1 end]),
          lan_on = t.lan_on + 1,
          lan_quen = t.lan_quen + case when r.dg = 'quen' then 1 else 0 end,
          lan_cuoi = now();

    v_so_the := v_so_the + 1; -- đếm thô (cả lượt cập nhật), chỉ để chặn trần
  end loop;
end;
$$;

-- ---------------------------------------------------------------------------
-- Thẻ đến hạn của tôi (mọi bài)
-- ---------------------------------------------------------------------------
create or replace function public.on_tap_den_han(p_limit int default 8)
returns table (slug text, the_id text, bac smallint, han_on timestamptz, tong_den_han int)
language sql stable security definer set search_path = public
as $$
  select t.slug, t.the_id, t.bac, t.han_on, (count(*) over ())::int as tong_den_han
  from public.on_tap_the t
  where t.user_id = (select auth.uid())
    and t.han_on <= now()
  order by t.han_on, t.slug, t.the_id
  limit least(greatest(coalesce(p_limit, 8), 1), 40);
$$;

-- ---------------------------------------------------------------------------
-- Trạng thái mọi thẻ của tôi trong một bài
-- ---------------------------------------------------------------------------
create or replace function public.on_tap_trang_thai(p_slug text)
returns table (the_id text, bac smallint, han_on timestamptz)
language sql stable security definer set search_path = public
as $$
  select t.the_id, t.bac, t.han_on
  from public.on_tap_the t
  where t.user_id = (select auth.uid())
    and t.slug = left(p_slug, 80)
  order by t.the_id;
$$;

revoke all on function public.on_tap_ghi(text, jsonb) from public, anon;
revoke all on function public.on_tap_den_han(int) from public, anon;
revoke all on function public.on_tap_trang_thai(text) from public, anon;
grant execute on function public.on_tap_ghi(text, jsonb) to authenticated;
grant execute on function public.on_tap_den_han(int) to authenticated;
grant execute on function public.on_tap_trang_thai(text) to authenticated;

commit;

-- ---------------------------------------------------------------------------
-- KIỂM THỬ sau khi chạy (mỗi khối tự rollback bằng raise; thay <uuid …> bằng id thật):
-- HS — ghi rồi đọc lại thẻ của mình:
--   do $t$ declare r text; begin
--     perform set_config('request.jwt.claims', json_build_object('sub','<uuid HS>','role','authenticated')::text, true);
--     set local role authenticated;
--     perform public.on_tap_ghi('l11-nguon-dien',
--       '[{"id":"aaaa1111","danh_gia":"nho"},{"id":"bbbb2222","danh_gia":"quen"},{"id":"x y","danh_gia":"nho"},{"id":"cccc3333","danh_gia":"sai"}]');
--     perform public.on_tap_ghi('l11-nguon-dien', '[{"id":"aaaa1111","danh_gia":"nho"}]');
--     select string_agg(the_id||':'||bac||':'||to_char(han_on - now(), 'DD'), ' ') into r
--       from public.on_tap_trang_thai('l11-nguon-dien');
--     raise exception 'KETQUA %', r;   -- mong đợi: aaaa1111:2:~03  bbbb2222:1:~01 (2 phần tử sai bị bỏ)
--   end $t$;
-- HS — không đọc thẳng bảng được:
--   do $t$ begin
--     perform set_config('request.jwt.claims', json_build_object('sub','<uuid HS>','role','authenticated')::text, true);
--     set local role authenticated;
--     perform 1 from public.on_tap_the;   -- mong đợi: permission denied for table on_tap_the
--   end $t$;
-- Trợ giảng — chỉ thấy thẻ của chính TA, không thấy thẻ HS (chạy sau khi HS có thẻ thật):
--   do $t$ declare n int; begin
--     perform set_config('request.jwt.claims', json_build_object('sub','<uuid TA>','role','authenticated')::text, true);
--     set local role authenticated;
--     select count(*) into n from public.on_tap_trang_thai('l11-nguon-dien');
--     raise exception 'TA thay % the', n;   -- mong đợi: chỉ số thẻ TA tự ôn (thường 0)
--   end $t$;
-- Admin — giống TA (dùng <uuid admin>); đối chiếu bằng SQL Editor (service role):
--   select user_id, count(*) from public.on_tap_the group by 1;
-- Thẻ đến hạn (đẩy hạn về quá khứ trong giao dịch rồi gọi):
--   do $t$ declare r text; begin
--     update public.on_tap_the set han_on = now() - interval '1 hour' where user_id = '<uuid HS>';
--     perform set_config('request.jwt.claims', json_build_object('sub','<uuid HS>','role','authenticated')::text, true);
--     set local role authenticated;
--     select string_agg(slug||'/'||the_id||' tong='||tong_den_han, ', ') into r from public.on_tap_den_han(1);
--     raise exception 'KETQUA %', r;   -- 1 dòng, tong = tổng số thẻ của HS
--   end $t$;
-- anon: set role anon; select public.on_tap_den_han();  → permission denied for function
--
-- ROLLBACK (chạy tay nếu cần gỡ; mất toàn bộ lịch ôn đã ghi):
--   begin;
--   drop function if exists public.on_tap_ghi(text, jsonb);
--   drop function if exists public.on_tap_den_han(int);
--   drop function if exists public.on_tap_trang_thai(text);
--   drop table if exists public.on_tap_the;
--   commit;
