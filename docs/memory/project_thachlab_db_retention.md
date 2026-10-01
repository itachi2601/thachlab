---
name: project_thachlab_db_retention
description: "Giữ Supabase không phình vô hạn — rollup + xoá kết quả từng câu > 12 tháng, dọn JSON tạm exam_attempts; migration 20260928170000 ĐÃ CHẠY 28/9/2026 11:39, pg_cron bật + job hằng tháng; dry-run 0 lượt"
metadata:
  type: project
---

Đợt rà hạn mức Supabase Free 28/9/2026 (ảnh Usage: Log 83%, DB 21%, còn lại < 20%).
Kết luận cho thầy: gói Pro 25 USD chấp nhận được; trên Pro dung lượng vượt 8 GB chỉ 0,125 USD/GB/tháng
nên "phình" không làm hoá đơn phình; rủi ro hoá đơn thật là compute (Small +15 USD) và egress.

**Đã làm 28/9/2026**
- Xoá `question_bank_backup_20260925` (migration 20260928150000, thầy đã chạy 10:55): DB 106 MB → 76 MB.
- Autosave ExamRunner chỉ ghi khi đổi đáp án (commit af656f0a, phiên khác, đã deploy 10:43).
- Viết migration `supabase/migrations/20260928170000_question_results_retention.sql`
  (rollback `perf/rollback/…down.sql`): bảng `question_result_rollups` (student × source × topic ×
  form × qtype × difficulty), hàm `rollup_question_results(p_before default 12 tháng, p_dry)`
  gộp+xoá `exam_question_results`/`practice_question_results` cũ (GIỮ lượt có câu essay để không mất
  điểm chấm tay), đánh dấu `exam_results/practice_sessions.results_rolled_up_at`; `rank_title_stats`
  cộng phần gộp; xoá `responses/seconds_left` trong `exam_attempts` đã nộp; lịch pg_cron 3:00 VN ngày 1
  hằng tháng (ĐÃ bật 28/9). Code: `finishExamAttempt` xoá JSON tạm khi nộp,
  `scripts/backfill-exam-analytics.mjs` bỏ qua lượt đã gộp. Cú pháp đã parse offline bằng pgsql-parser,
  Migration ĐÃ CHẠY 11:39, dry-run trả 0 lượt (đúng), pg_cron bật được, job đặt xong. Code commit 5be86330, deploy 28/9 13:11.
- Hàm rollup KHÔNG chạy lúc migration; chưa có lượt nào > 12 tháng → lần gộp đầu ~9/2027.

**Mất gì khi gộp (đã nói với thầy, chấp nhận):** phân tích từng câu/ma trận GV cho đề > 1 năm trống;
mastery "10 lượt gần nhất" và Lật Kèo chỉ nhìn dữ liệu còn lại; danh hiệu đã trao giữ nguyên.

**Còn treo:** thầy chạy migration; bật pg_cron ở Dashboard → Database → Extensions (hoặc chạy tay mỗi
học kì); bỏ cột `topic_name` trong exam_question_results (mục 2, cần rà RPC get_class_topic_matrix +
fetchMyTopicGaps đang group theo tên); Pause project Sydney cũ (xem
[[project_thachlab_supabase_region_migration]]).

**Deploy khi mạng yếu (28/9/2026):** push full 30 MB bị GitHub 408 trên hotspot iPhone (~15 KB/s upload).
Đã sửa `scripts/deploy.sh`: fetch --depth=1 nhánh deploy trước rồi commit mồ côi → chỉ gửi phần khác
biệt (1 557 object, 9 giây). Vẫn giữ đúng 1 commit trên nhánh deploy.
