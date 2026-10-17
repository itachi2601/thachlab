---
name: project_thachlab_dt_audit
description: "Chương trình DT (design thinking) 16 hạng mục 16–18/10/2026: đã làm DT-01/03/04/07/12/16, còn dữ liệu thật + RLS + deploy hsg-ai-grade; tổng kết ở docs/thachlab-design-thinking-audit.md"
metadata:
  type: project
---

Nguồn: `docs/thachlab-design-thinking-audit.md` (bảng 16 hạng mục + mục "TỔNG KẾT TRIỂN KHAI 18/10/2026" có việc còn lại xếp ưu tiên).

**Đã chạy trên production (17/10):** `learning_events` (+client open/leave/submit), `feature_flags`, cảnh báo `inactive_7d`/`absent_streak` (cron 6:00 VN), lịch ôn 1/3/7 theo cờ `on_tap_1_3_7` (đang bật lớp 12, class_id 18; lớp 11 đối chứng), 35 đề Kiểm tra nhanh (exam 937, 941–974), gán YCCĐ 196/212 câu L10.

**Why:** thầy muốn thử MỘT thay đổi trên một lớp rồi so với lớp cũ (tuần 6), thay vì đổi cả hệ thống.

**How to apply:** trước khi làm tiếp DT-05/06/15 phải có dữ liệu `learning_events` thật và kết quả thử DT-04; dữ liệu HS chỉ qua Claude (đã gỡ DeepSeek khỏi `hsg-ai-grade`, thầy tự deploy). HS thật dùng email `@thachlab.local` — chỉ `hs.test%` là tài khoản thử. `next build` ở main có thể lỗi typecheck do script `.mts` chưa chuẩn của phiên khác → build từ worktree sạch (xem STATE.md).
