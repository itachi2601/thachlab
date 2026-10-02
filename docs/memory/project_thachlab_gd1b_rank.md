---
name: GĐ 1b rank – đã hoàn tất
description: GĐ 1b (10 việc) đã vào main + migration đã chạy + deploy; việc dở đã xong 2/10; chỉ còn thầy tự kiểm bằng mắt
type: project
---
Cập nhật 2026-10-02.

GĐ 1b rank (tiến bộ so với chính em, mục tiêu tuần thích ứng, phụ đạo "đang mở khoá", luyện tăng dần độ khó,
bảng theo bậc, mục tiêu lớp, giãn cách, đóng băng chuỗi, danh sách thứ Hai, đo nhóm thấp) — **xong toàn bộ**.

- Merge main: cd4b80e6 (30/9). Lỗi kiểu `features/rank/preview.ts` đã sửa trên main; `tsc --noEmit` sạch.
- Migration 20260929100000…130000, 20260930100000, 20260930110000…150000 đều ĐÃ CHẠY production.
- 2/10 làm nốt 2 việc dở (nhánh claude/gd1b-hoan-tat): màn kết quả bài tự kiểm tra thoát phụ đạo liệt kê đúng YCCĐ
  còn sai; sổ câu sai hiện lịch ôn 2 ngày/1 tuần/1 tháng (chỉ client, không migration).
- Thầy tự kiểm bằng mắt trên web thật (tài khoản HS) — chưa ai xác nhận.

Giới hạn còn lại: lý thuyết chưa cuộn tới đúng YCCĐ (bài chưa có mốc theo YCCĐ); lịch ôn chưa lưu lịch sử từng lần ôn.

Bài học: nhánh song song đổi kiểu dùng chung → sau merge phải `npx tsc --noEmit` trước deploy.
