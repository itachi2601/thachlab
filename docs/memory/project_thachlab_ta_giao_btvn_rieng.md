---
name: project-thachlab-ta-giao-btvn-rieng
description: Trợ giảng giao BTVN riêng từng em trên web (17/10/2026) - migration đã chạy, web đã deploy, chưa thử thật; còn nhắc trước hạn + bộ chọn câu ôn giữa kì
metadata:
  type: project
---

Trợ giảng giao BTVN riêng từng em/nhóm: bảng `ta_homework_assignments` + RPC `ta_homework_assign`, `my_pending_homework`, `ta_homework_overview` (migration 20261017180000, đã chạy 17/10). UI: `TaAssignHomework` cuối phiếu phụ đạo (`/tro-giang/ghi`), việc đầu thẻ Hôm nay của HS (`kind: "homework"` trong `features/learning/next-steps.ts`), `TaHomeworkOverview` ở Thông báo lớp. "Đã làm" = có `exam_results` sau lúc giao (không có cờ tay). Deploy 17/10 14:38.

**Why:** thầy muốn trợ giảng giao BTVN trên web thay vì báo miệng; chuông + thẻ Hôm nay chỉ là lối dẫn, nguồn thật là một chỗ.
**How to apply:** CHƯA làm: nhắc 1 lần trước hạn (cần pg_cron), bộ chọn câu 3 lớp (nền/giữ lại/kéo giãn) cho bài kiểm tra cuối buổi ôn giữa kì (cần thầy khai phạm vi giữa kì mỗi lớp), tính điểm trợ giảng cho BTVN nhóm. Thêm 1 RPC vào trang chủ HS là chủ ý lệch quy tắc "không thêm round-trip" (chạy song song) - gộp vào RPC có sẵn nếu thầy muốn. Tab terminal không gõ được `y` vào prompt đang chạy: dùng `run-migrations.sh --yes --only N`. Hai phiên cùng chạy deploy.sh sẽ đua force-push nhánh deploy: `pgrep -fl "deploy.sh|next build"` trước khi deploy.
