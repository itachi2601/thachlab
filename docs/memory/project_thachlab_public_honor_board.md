---
name: thachlab-public-honor-board
description: Vinh danh tuần theo khối trên trang chủ công khai (top 3 RP tuần + ghi nhận) — code commit 1f2b0a48 + deploy 28/9/2026; migration 20260928160000 CHƯA chạy nên mục còn ẩn
metadata:
  node_type: memory
  type: project
  originSessionId: e1e17567-a8dd-4d41-afc1-b4fecaf3951f
  modified: 2026-09-28T04:18:50.661Z
---

Mục "Vinh danh tuần" trên trang chủ `/` (28/9/2026): tab Khối 10/11/12, bục top 3 theo RP KIẾM
TRONG TUẦN (đồng hạng giữ cả, tối đa 5 ô), khung avatar + huy chương (RankAvatarFrame prop `tier`),
danh hiệu đang đeo, 3 dòng ghi nhận (tiến bộ nhất ngoài top 3, lên bậc, chuỗi ngày). Khối chưa ai có
RP tuần này → dùng tuần trước (`use_prev`). Component `components/home/HonorBoard.tsx` (sentinel +
IntersectionObserver rootMargin 600px) → `HonorBoardPanel.tsx` (dynamic ssr:false + LazyErrorBoundary).
Service `fetchPublicHonor()` cache sessionStorage 1 giờ. Học sinh chọn mức hiện tên bằng
`HonorVisibilityPicker` dưới ClassRankBoard ở trang HS.

**Trạng thái:** v1 commit `1f2b0a48`, migration 20260928160000 thầy ĐÃ chạy 28/9/2026 11:39; gọi RPC
thật (qua terminal của thầy, sandbox + browser pane đều bị chặn supabase.co) trả đúng 3 khối.
Phát hiện từ dữ liệu thật: tên HS tự nhập bẩn ("đỗ đăng duy(oguri cap number one fan)",
"7A4-45- Nguyễn Minh Bảo Trân", "Gia Huy 10a1"), sáng Thứ Hai khối 10 có >5 bạn đồng hạng 1.
→ v2 `20260928180000_rank_public_honor_v2.sql` (rank_honor_name làm sạch + top_more) commit
`06283b5b` + deploy 28/9/2026; thầy ĐÃ chạy 13:46 (log scripts/logs/20260928-134634-*), kiểm lại RPC thật: khối 10 "Duy Đ." + top_more=1, khối 11/12 đúng. Chưa nhìn thấy mục trên web thật bằng mắt (browser
pane không gọi được Supabase) — nhờ thầy tự xem hoặc dùng Chrome thật.
Tài khoản test còn nằm trong lớp 10/11/12 ("Học sinh Test 010/011/012", "Perf5 Test Account") có thể
lên bục nếu làm bài — thầy nên xoá hoặc đặt honor_visibility='hidden'.

**Why:** thầy muốn vinh danh HS theo khối trên trang chủ; giữ quyết định cũ "không xếp RP tổng"
(xem [[thachlab-class-rank-board]]). Thầy yêu cầu rõ: hiện avatar + huy hiệu như trên web.

**How to apply:**
- Quyết định đã chốt: mặc định `honor_visibility='short'` = tên rút gọn "Minh N." + ảnh đại diện;
  'full' tên đầy đủ; 'hidden' không xuất hiện (bảng tuần trong lớp vẫn thấy). Rút gọn làm trong SQL
  (`rank_honor_name`), client không bao giờ nhận tên đầy đủ khi em chọn short.
- Khối suy từ chữ số đầu trong `classes.name` — lớp 9 KHTN sẽ tự xuất hiện nếu một mùa rank gồm
  class 15; thầy chưa quyết mở lớp 9, hiện chưa thuộc mùa nào nên không hiện.
- Nhãn tiêu đề cố ý là "Các bạn học chăm nhất tuần này" (RP = nỗ lực), không dùng chữ "Xếp hạng".
- Phương án dự phòng chưa làm: quy tắc "ở bục 2 tuần liền → tuần 3 chuyển sang dòng Giữ vững phong
  độ" nếu thấy cùng vài gương mặt lặp lại; ẩn tab khối chưa ai đạt 20 RP.
- Sau khi migration chạy: mở `/` cuộn xuống dưới Lộ trình học để kiểm; nếu trống → gọi thử
  `select public.rank_public_honor();` xem `grades[].top`.
