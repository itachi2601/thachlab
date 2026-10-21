---
name: project-thachlab-on-tap-theo-chang
description: Buổi ôn tập theo chặng (21/10/2026) — thầy/TA điều phối, tivi, học sinh; mỗi chặng là một đề Kiểm tra nhanh; migration đã chạy, client chưa deploy
metadata:
  type: project
---

21/10/2026 thầy muốn ôn cả lớp cùng nhịp (ví dụ chương 3 từ trường) mà không theo dõi được em nào làm tới đâu. Làm 3 màn hình trên đề **Kiểm tra nhanh đã có** (không thêm loại đề mới), thầy bỏ qua mối lo "phình chức năng".

**Cấu trúc:** bảng `review_sessions` (lớp, ngưỡng %, `stages` jsonb `[{exam_id,item_id,title,minutes}]`, chặng hiện tại, `extra_seconds`) + 8 hàm `review_*` (migration `20261021120000_on_tap_theo_chang`, ĐÃ CHẠY 21/10, rollback `perf/rollback/…down.sql`). Không có bảng tiến độ riêng: đọc `exam_attempts` (đáp án tự lưu) + `exam_results`, chỉ tính lượt từ lúc buổi ôn được tạo. "Đạt" = điểm tốt nhất ≥ ngưỡng, **chỉ là mốc hiển thị**, không khoá máy chủ (em chưa đạt vẫn làm lại).
- Nhân sự (`/tro-giang/on-tap/`, dùng chung thầy + TA, `?id=` mở bảng điều phối): `components/review/ReviewHome` (tạo: lớp → chương → tick đề Kiểm tra nhanh, hoặc nhập mã đề), `ReviewConsole` (đồng hồ, +2 phút, mở chặng, lọc theo trạng thái, em đứng yên ≥3 phút, "Hỏi thăm" lưu localStorage, câu sai nhiều nhất + nút Chiếu).
- Tivi (`/tro-giang/on-tap/chieu/?id=`): chỉ số liệu chung, QR đề + số đề lớn, KHÔNG tên em (nhạy địa vị bạn bè 14–18).
- Học sinh (`/lop-hoc/on-tap/` + thẻ `ReviewBanner` ở `/lop-hoc`): chặng, đồng hồ, một nút việc của em, "x/y bạn đã nộp" ẩn danh.

**Kiểm 21/10:** bản thử SQL tự hoàn tác (103 em lớp 12, đếm câu đã trả lời đúng, giờ = phút + extra), thử trọn luồng bằng tài khoản nhân sự trên lớp 21 (0 học sinh, đã dọn), 375px học sinh ổn, QR `?id=&item=` giải mã đúng (`kiem-qr.mts`), `next build` qua.
**Chưa làm / treo:** CHƯA DEPLOY client; chưa thử với học sinh thật + tivi thật; chưa kiểm ghi đáp án theo thời gian thực khi 30 em cùng làm (tải RPC ~7 lượt/giây); chưa có báo cáo cuối buổi và tự chuyển câu sai sang phụ đạo (ý 8–9 trong thiết kế); mục chặng đứng yên dựa `exam_attempts.saved_at` (chỉ ghi khi đáp án đổi).
**Cách dùng cho thầy:** Menu tài khoản → "Ôn tập theo chặng" → tạo → mở "Màn hình chiếu" ở tab khác nối tivi → bấm "Bắt đầu chặng 1".
