-- ============================================================================
-- rank_my_status: thêm trường on_tap_den_han (Ôn 5 phút) — 25/11/2026
-- Trang /lop-hoc đã gọi rank_my_status() (fetchMyRankStatus) → gắn thêm số thẻ "Ôn 5 phút" đến hạn của
-- CHÍNH người đăng nhập vào cùng jsonb, không thêm round-trip.
--
-- Định nghĩa hiện hành (nguồn: 20260925140000_perf_rls.sql — file migration DUY NHẤT định nghĩa hàm này;
-- bản gốc ở docs/supabase-migration-rank-system.sql):
--   select public.rank_status_of((select auth.uid()));
-- Bản mới: giữ nguyên kết quả đó, chỉ nối thêm khoá on_tap_den_han (int, 0..99).
--   * Điều kiện "đến hạn" y hệt RPC on_tap_den_han: user_id = auth.uid() and han_on <= now().
--   * Đếm có trần 99 (limit trong subquery) — dùng index on_tap_the_user_han_on_idx (user_id, han_on) đã có
--     trong 20261125120000_on_tap_lich_on.sql, không cần index mới.
--   * rank_status_of trả null (chưa đăng nhập / không xem được) → vẫn trả null như cũ (null || jsonb = null).
-- Không đổi chữ ký (() → jsonb), không đổi security definer / stable / search_path.
-- CREATE OR REPLACE giữ nguyên grant hiện có (execute cho authenticated); không đụng rank_status_of
-- (phụ huynh/GV gọi rank_status_of(<id HS>) KHÔNG nhận trường mới → không lộ lịch ôn của HS cho người khác).
--
-- PHỤ THUỘC: phải chạy SAU 20261125120000_on_tap_lich_on.sql (thân hàm SQL được kiểm khi tạo → thiếu bảng
-- on_tap_the thì lỗi và giao dịch tự huỷ, không hỏng gì).
--
-- Ai đọc được gì (không đổi RLS; chỉ đổi dữ liệu trả về của RPC):
-- | Vai             | rank_my_status().on_tap_den_han            | Bảng on_tap_the trực tiếp |
-- |-----------------|--------------------------------------------|---------------------------|
-- | HS              | số thẻ đến hạn của CHÍNH mình              | không (revoke, không policy) |
-- | Trợ giảng / GV  | số thẻ của CHÍNH mình (thường 0); không thấy của HS | không              |
-- | Admin           | như trên                                   | không (qua web)           |
-- | Phụ huynh       | trang /lop-hoc gọi rank_status_of(con) → không có trường này | không    |
-- | anon            | không (không có execute)                    | không                     |
-- Không ai ghi được gì mới qua hàm này (stable, chỉ đọc).
--
-- Nặng không: chỉ thay 1 hàm → chạy giờ nào cũng được.
-- Rollback: perf/rollback/20261125180000_rank_my_status_on_tap.down.sql
-- ============================================================================
begin;

create or replace function public.rank_my_status()
 returns jsonb
 language sql
 stable security definer
 set search_path to 'public'
as $function$
  select public.rank_status_of((select auth.uid()))
         || jsonb_build_object('on_tap_den_han', (
              select count(*)::int
              from (select 1
                    from public.on_tap_the t
                    where t.user_id = (select auth.uid())
                      and t.han_on <= now()
                    limit 99) d));
$function$;

commit;

-- ---------------------------------------------------------------------------
-- KIỂM THỬ sau khi chạy (mỗi khối tự huỷ bằng raise; thay <uuid …> bằng id thật):
-- HS — có trường mới, các trường cũ vẫn đủ:
--   do $t$ declare j jsonb; begin
--     perform set_config('request.jwt.claims', json_build_object('sub','<uuid HS>','role','authenticated')::text, true);
--     set local role authenticated;
--     j := public.rank_my_status();
--     raise exception 'on_tap=% keys=%', j->'on_tap_den_han', (select string_agg(k, ',') from jsonb_object_keys(j) k);
--     -- mong đợi: on_tap=0 (hoặc số thẻ đến hạn), keys gồm season,rp,tier,next,...,on_tap_den_han
--   end $t$;
-- HS — đếm khớp on_tap_den_han() (đẩy hạn về quá khứ trong giao dịch):
--   do $t$ declare a int; b int; begin
--     update public.on_tap_the set han_on = now() - interval '1 hour' where user_id = '<uuid HS>';
--     perform set_config('request.jwt.claims', json_build_object('sub','<uuid HS>','role','authenticated')::text, true);
--     set local role authenticated;
--     a := (public.rank_my_status()->>'on_tap_den_han')::int;
--     select coalesce(max(tong_den_han), 0) into b from public.on_tap_den_han(1);
--     raise exception 'rank_my_status=% on_tap_den_han=%', a, b;   -- mong đợi: a = least(b, 99)
--   end $t$;
-- Trợ giảng — chỉ thấy số của chính TA:
--   do $t$ declare j jsonb; begin
--     perform set_config('request.jwt.claims', json_build_object('sub','<uuid TA>','role','authenticated')::text, true);
--     set local role authenticated;
--     j := public.rank_my_status();
--     raise exception 'TA: %', coalesce(j->>'on_tap_den_han', 'null (rank_status_of null)');  -- mong đợi: 0
--   end $t$;
-- Admin — như TA (dùng <uuid admin>); phụ huynh/GV xem HS qua rank_status_of(<uuid HS>) KHÔNG có khoá on_tap_den_han:
--   do $t$ declare j jsonb; begin
--     perform set_config('request.jwt.claims', json_build_object('sub','<uuid admin>','role','authenticated')::text, true);
--     set local role authenticated;
--     j := public.rank_status_of('<uuid HS>');
--     raise exception 'co khoa on_tap? %', j ? 'on_tap_den_han';   -- mong đợi: false
--   end $t$;
-- anon: set role anon; select public.rank_my_status();  → permission denied for function
-- Grant không đổi:
--   select grantee, privilege_type from information_schema.routine_privileges where routine_name = 'rank_my_status';
