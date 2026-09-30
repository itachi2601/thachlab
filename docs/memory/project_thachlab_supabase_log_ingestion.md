---
name: project_thachlab_supabase_log_ingestion
description: Supabase Log Ingestion Free plan 1 GB/chu kỳ — 28/9/2026 dùng 0,83 GB, đã giảm 3 nguồn poll phía client; chưa tính phí tới 2027
metadata:
  type: project
---

28/9/2026 thầy đưa ảnh Usage: Log Ingestion 0,83/1 GB (chu kỳ bắt đầu ~8/9), tăng từ ~10 MB/ngày
lên 100–200 MB/ngày trong tuần 22–27/9. Supabase ghi rõ chưa tính phí mục này tới đầu 2027.
Nguyên nhân: đột biến do admin (agent đăng đề hàng loạt, backfill, migration, gộp trùng câu hỏi);
mức nền tăng do poll client sau 24/9.

Đã làm (commit af656f0a, deploy 28/9): autosave ExamRunner 15s vô điều kiện → 30s chỉ khi đáp án
đổi, tối đa 2 phút/lần để seconds_left không lệch; heartbeat học bài 60s→120s; chuông thông báo
60s→120s + bỏ qua khi tab ẩn, tải lại khi tab hiện.

**Why:** Free plan sẽ vượt 1 GB đều mỗi tháng nếu mức nền 50 MB/ngày; từ 2027 phần vượt bị tính phí.
**How to apply:** Thêm poll/heartbeat mới ở trang HS phải bỏ qua khi tab ẩn và ≥2 phút. Còn treo:
gom script đăng hàng loạt thành insert batch; kiểm tab API Gateway lọc 4xx; chốt Pause/Delete project
Sydney cũ vì usage tính cả tổ chức (xem [[project_thachlab_supabase_region_migration]]).
