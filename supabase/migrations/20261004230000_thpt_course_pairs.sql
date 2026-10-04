-- ============================================================================
-- Lớp học thêm 2 buổi/tuần (lớp 12): gắn nhãn buổi A / buổi B cho các khoá đã tách.
--
-- Hiện lớp "Vật lí 12L1" tách thành 4 khoá, mỗi khoá một buổi: Thứ 4 (A4), Thứ 5 (A5), Thứ 7 (B7),
-- Chủ nhật (B8). Học sinh học 2 buổi/tuần: chọn MỘT buổi A (T4 hoặc T5) + MỘT buổi B (T7 hoặc CN).
-- Hai cột pair_key / pair_slot đã có sẵn trong thpt_courses nhưng còn trống; code (services/
-- thpt-courses-public.ts derivePair) ưu tiên cột, cột trống thì suy từ tên "… — buổi A · …".
-- File này điền cột cho 4 khoá để dữ liệu rõ ràng, không còn phụ thuộc cách đặt tên; thêm comment cột.
-- Chỉ UPDATE dữ liệu + comment, không đổi schema/policy/hàm. Chạy lúc nào cũng được.
--
-- Ràng buộc "phải chọn đủ 1A + 1B" hiện kiểm ở client (/khoa-hoc, /khoa-hoc/dang-ky), RPC thpt_register
-- vẫn nhận từng khoá — chưa ép ở server.
-- Rollback: khối cuối file.
-- ============================================================================
begin;

comment on column public.thpt_courses.pair_key is
  'Lớp học nhiều buổi/tuần tách thành nhiều khoá: các khoá cùng pair_key là một lớp. null = khoá đơn.';
comment on column public.thpt_courses.pair_slot is
  'Loại buổi trong lớp tách buổi ("A", "B"): học sinh chọn đúng một khoá cho mỗi pair_slot của cùng pair_key.';

update public.thpt_courses
set pair_key = 'Vật lí 12L1',
    pair_slot = case
      when name ilike '%buổi A%' then 'A'
      when name ilike '%buổi B%' then 'B'
    end
where name like 'Vật lí 12L1 — buổi %'
  and (pair_key is null or pair_slot is null);

commit;

-- ---------------------------------------------------------------------------
-- ROLLBACK (chạy tay nếu cần quay lại):
-- update public.thpt_courses set pair_key = null, pair_slot = null where pair_key = 'Vật lí 12L1';
-- comment on column public.thpt_courses.pair_key is null;
-- comment on column public.thpt_courses.pair_slot is null;
-- ---------------------------------------------------------------------------
