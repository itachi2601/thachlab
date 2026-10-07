---
name: thachlab-class-rank-board
description: "Bảng tuần của lớp — 7/10/2026 chuyển từ trang chủ HS sang /lop-hoc/xep-hang (RankPage nhận classId): top 3 theo RP tuần, vị trí của em + hàng xóm, ghi nhận tuần — đã chạy migration + deploy 25/9/2026; khối 3 (phân bố bậc) chưa làm"
metadata:
  type: project
---

Bảng tuần của lớp (25/9/2026): component `components/rank/ClassRankBoard.tsx` gắn ngay dưới RankCard
trong `ThptStudentHome.tsx`; dữ liệu từ RPC `rank_class_board(p_class_id)`
(`docs/supabase-migration-rank-class-board.sql`, ĐÃ chạy trên Supabase, test SQL rollback qua).
Commit 770438c8, push main + deploy branch xong 25/9/2026 (build từ worktree sạch).

**Why:** thầy muốn bảng xếp hạng RP tạo động lực; chốt thiết kế "không xếp cả lớp theo RP tổng"
(top cố định sau 2 tuần, 70% còn lại bỏ cuộc). Chỉ xếp theo RP KIẾM TRONG TUẦN (reset Thứ Hai giờ VN),
em chỉ thấy 1 bạn ngay trên/ngay dưới, "tiến bộ nhất tuần" chỉ tính bạn NGOÀI top 3 để nhóm dưới được xuất hiện.

**How to apply:**
- 4 khối đã đề xuất: (1) top tuần, (2) vị trí của em, (3) phân bố bậc của lớp, (4) ghi nhận tuần.
  Đã làm 1, 2, 4. Khối 3 CHƯA làm — nếu thầy muốn thì thêm vào cùng RPC (đếm thành viên theo tier_code).
- RP tổng từng bạn KHÔNG trả về ở RPC này; đừng thêm bảng xếp hạng RP tổng nếu thầy không yêu cầu lại.
- Chống farm đã có sẵn: rank_award khoá (kind, ref) và chỉ cộng phần tăng, nên làm lại cùng đề không cộng thêm.
- Admin (thầy) xem /tai-khoan bằng "Xem như học sinh" thì khối 2 ẩn (me = null vì lọc role='student') — bình thường.
- Chưa test bằng tài khoản HS thật với dữ liệu thật (tuần 21/9 chưa có ledger, chỉ test bằng row tạm cho 4 tài khoản test rồi xoá).
- Trang chủ công khai: 28/9/2026 đã làm "Vinh danh tuần theo khối" — xem [[thachlab-public-honor-board]]; "Vinh danh mùa" (2 tuần sau khi mùa kết thúc) vẫn chưa làm.

- 7/10/2026: thầy chốt chuyển `ClassRankBoard` + `HonorVisibilityPicker` từ trang chủ HS sang `RankPage` (`/lop-hoc/xep-hang`
  tự lấy lớp qua `fetchMyClassRequest`); trang chủ chỉ còn `RankCard` + `DailyStreakCard`. Lý do: L3/N1 — phần thưởng không
  chen vào phần học. Chưa kiểm bằng tài khoản HS thật sau khi chuyển.
