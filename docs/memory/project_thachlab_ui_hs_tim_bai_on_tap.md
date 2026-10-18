---
name: project_thachlab_ui_hs_tim_bai_on_tap
description: "Rà UI học sinh 2026-10-17 (đóng vai HS Test 1, 375px): tìm bài đã làm / ôn tập / việc hôm nay — 9 điểm, 4 đợt sửa đã lên site; còn 2 điểm nhỏ + 2 chỗ chưa kiểm"
metadata:
  type: project
---

**Mục tiêu:** học sinh vào thachlab tìm lại bài đã làm, ôn tập, hoặc tìm việc hôm nay mà không lạc, không bị thông điệp mâu thuẫn.

**Bản rà 2026-10-17** (9 điểm, đều đã sửa): Hôm nay lệch Cần chú ý · phụ đạo mở từ đề luyện 5 câu · "đừng làm lại" cạnh nút Làm lại · "Điểm đã đạt 0,5/1,25" · Bài đã làm nằm cuối trang, tên trang khác menu · kệ đề lớp 12 có 809 đề lẫn lớp 11, nhãn Chưa làm lặp · radar hiện chương lớp 11 · số câu đổi trước nội dung · xem lại bài kết thúc cụt.

**Đã lên site (deploy cuối 2026-10-17 23:24):**
- Đợt A `9a0d144a9`: Hôm nay lấy đề lớp chưa làm cùng nguồn với Cần chú ý (mọi lớp, bỏ cửa sổ 21 ngày); `shouldOfferRetry` (5 ≤ điểm < 6,5) ở `features/learning/next-steps.ts` dùng chung 3 chỗ; `ExamResultSummary` bỏ dòng Điểm đã đạt.
- Đợt B `1c64f73ea`: `StudentResultsDashboard` tên "Bài đã làm & kết quả", danh sách lên đầu (phụ huynh giữ thứ tự cũ); `features/exams/exam-grade.ts` lọc kệ đề theo lớp (vá tạm, nay DB đã gán lớp — có thể gỡ sau); `ExamShelf` chỉ gắn nhãn khi đã làm.
- Đợt 3 (phiên Sonnet) `12cceb054` radar theo lớp em (chương lớp khác dưới "Lớp khác"), `397a7097d` bỏ AnimatePresence mode=wait, `ba28581b8` `components/exams/ExamNextSteps.tsx` hàng nút cuối xem lại bài.
- `310fab3ca`: câu "Làm lại không cộng thêm RP" → "chỉ cộng phần điểm vượt lần trước" (mùa 4/5 `rp_first_attempt_only = 0`).
- Phụ đạo không sinh từ đề luyện: xem [[project_thachlab_phu_dao]] (migration 20261017230000).

**Đã kiểm 2026-10-17 trên dev 375px bằng HS Test 1** (đề 908 lớp 11, đề 903 lớp 12): màn nộp bài, Hôm nay, Bài đã làm, kệ đề lớp 12 (809 → 396).

**Còn treo (nhỏ, chưa sửa):**
- Radar ghi "Chương này em đã nắm vững, học tiếp bài mới" ngay dưới bài 20% "Chưa đủ dữ liệu" (`components/results/ChapterMasteryRadar.tsx`) — nên im khi chưa đủ dữ liệu.
- Bài đã làm hiện "(Đề đã xóa)" khi đề đã bị gán lớp khác (RLS exams) — nên ghi "Đề không còn mở cho lớp em".
- Chưa kiểm: kệ lớp 11 bằng tài khoản lớp 11; giao diện site thật sau đăng nhập (không nhập mật khẩu thử ngoài localhost).
- Thầy quyết: 3 đề #206, #209 (mùa 4), #7 (mùa 5) giữ 20 RP, không hạ.

Liên quan: [[project_thachlab_gan_lop_de]], [[project_thachlab_hs_test_accounts]], [[project_thachlab_rank_system]].
