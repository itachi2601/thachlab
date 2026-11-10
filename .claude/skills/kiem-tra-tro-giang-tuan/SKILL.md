---
name: kiem-tra-tro-giang-tuan
description: Kiểm tra tiến trình trợ giảng trong tuần (ta_sessions) rồi gửi nhắc nhẹ trong web cho từng trợ giảng, giọng thầy gọi "con", tăng dần mức nhắc (ta_reminders). Dùng khi thầy nói "kiểm tra trợ giảng tuần này", "nhắc trợ giảng", "trợ giảng ai chưa làm gì", "/kiem-tra-tro-giang-tuan".
---

# Kiểm tra trợ giảng hằng tuần — đọc dữ liệu, nhắc nhẹ, nhớ lịch sử

**Mục đích (thầy chốt 11/10/2026):** trợ giảng làm việc nghiêm túc, không chỉ vì lương mà vì sự tiến bộ của các em. Giọng **nhẹ nhàng, thúc đẩy**; thầy gọi trợ giảng là **"con"**, xưng **"thầy"**. Chi tiết giọng: `references/giong-nhac.md`.

## Phạm vi (bản 1)
Chỉ kiểm những gì **phiếu đã ghi** trong `ta_sessions` (chưa có lịch lên lớp dự kiến nên chưa bắt lỗi "vắng buổi"; trợ giảng được gắn lớp mà cả tuần không ghi buổi nào thì nhắc mềm, vì có thể nghỉ có phép). Muốn kiểm "thiếu buổi" thật cần thêm bảng lịch — hỏi thầy trước khi làm.

Các mục kiểm (mã trong `items`): `chua_ghi_buoi`, `phieu_tra_ve`, `it_tiep_xuc` (<70% mục tiêu 12 lượt/buổi), bốn mục tick của buổi lớp (`arrived_early`, `homework_checked`, `walked_tables`, `reported_students`), `chuyen_can` (trễ/vắng không phép), `chua_phu_dao`, ba mục tick của buổi phụ đạo (`pd_prepared`, `pd_recalled`, `pd_asked_each`), `em_cho_phu_dao` (em được giao >14 ngày chưa phụ đạo).

## Quy trình
1. **Dry-run** (chỉ đọc) trên Mac, ở tab terminal (cần `.env.local`, sandbox Bash chặn Supabase):
```
cd /Users/MAC/Projects/thachlab && npx tsx .claude/skills/kiem-tra-tro-giang-tuan/scripts/kiem-tra-tuan.mts
```
   Thêm `--tuan YYYY-MM-DD` để kiểm một tuần khác (ngày bất kỳ trong tuần). Kết quả cũng ghi `scripts/logs/ta-nhac-<thứ Hai>.json`.
2. **Đọc và rà bản nháp** với thầy: ai đủ việc, ai cần nhắc, nội dung từng tin. Phiên Claude chỉnh lời nếu thầy muốn (sửa `compose()` hoặc `references/giong-nhac.md`), **không tự gửi**.
3. **Gửi thật** chỉ khi thầy đồng ý: thêm `--yes`. Script ghi `notifications` (chuông + `/thong-bao` của trợ giảng, bấm vào tới `/tro-giang`) và `ta_reminders`. Chạy lại cùng tuần không gửi trùng (mỗi người ≤1 tin/tuần).
4. **Báo thầy** tổng hợp ngắn: ai đủ việc, ai được nhắc (mức mấy), ai nhắc liên tiếp 2–3 tuần (cần thầy gặp trực tiếp).

## Mức nhắc (từ lịch sử `ta_reminders`)
- Mức 1: tuần đầu bị nhắc — nhẹ, tin tưởng.
- Mức 2: tuần liền trước đã nhắc — hỏi "con gặp khó gì?".
- Mức 3: 2 tuần liền trước đã nhắc — nói thẳng về trách nhiệm với các em, mời nói chuyện. **Câu "nếu chưa đủ thời gian thì nói với thầy" chỉ xuất hiện ở mức 3**, không dùng lời đe doạ/"tự rút" trong tin gửi.

## Ràng buộc
- Chỉ nói việc của chính người nhận; **không nêu điểm, lương, tên trợ giảng khác**. Tên học sinh không đưa vào tin (chỉ đếm số).
- Không gửi cho người chưa gắn `user_id`; script báo "THIẾU user_id".
- Migration `20261011170000_ta_reminders` phải chạy trước khi gửi thật (dry-run vẫn chạy được khi chưa có bảng, mức nhắc luôn là 1).
- Lên lịch tự động (Chủ nhật tối) chỉ được tạo **bản nháp chờ thầy duyệt**, không tự `--yes`.

## Nhật ký rút kinh nghiệm
- 2026-10-11 · tạo skill · DB đã ép đủ trường phiếu (`ta_policy_session_guard`) nên không có "phiếu thiếu trường"; việc bỏ sót thật nằm ở các ô tick = false và ở số lượt tiếp xúc → kiểm theo đó, đừng kiểm null.
