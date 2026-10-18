---
name: project_thachlab_dt_audit
description: "Chương trình DT (design thinking) 16 hạng mục 16–18/10/2026: đã chạy DT-01/03/04/07/12 + DT-16 (code), còn xác nhận dữ liệu thật, RLS pg_policies, deploy hsg-ai-grade, báo cáo lớp 12 vs 11; tổng kết ở docs/thachlab-design-thinking-audit.md"
metadata:
  type: project
---

Nguồn: `docs/thachlab-design-thinking-audit.md` (bảng 16 hạng mục + mục "TỔNG KẾT TRIỂN KHAI 18/10/2026" có việc còn lại xếp ưu tiên). Mục tiêu của thầy: thử MỘT thay đổi trên MỘT lớp rồi so với lớp cũ (tuần 6), không đổi cả hệ thống.

**Đã chạy trên production (17–18/10/2026)**
- DT-01 `learning_events` + RPC `log_learning_events` + purge 12 tháng: migration `20261017230000`; client `services/learning-events.ts` gọi từ `components/lessons/InlineLessonAccordion.tsx` (open/leave kèm giây tab hiển thị, submit khi hoàn thành mục; chỉ `role==='student'`; hàng đợi 60 giây, gửi khi ẩn tab). **Lúc 18/10 có 0 dòng** (T7, chưa rõ HS chưa mở bài hay client lỗi).
- DT-12 `feature_flags` + `feature_enabled(flag)`: migration `20261017231000`.
- DT-07 `sweep_engagement_alerts(p_class, p_days, p_absent_min)` + cron `engagement-alerts-sweep` 23:00 UTC (6:00 VN): migration `20261018100000`, sửa lọc HS Test ở `20261018131000`. Thử quét 18/10: 95 inactive (64 urgent; lớp 12: 41), 0 absent. **Cron chưa chạy lần đầu.** `fetchMyAlert` lọc bỏ 2 loại mới (HS không thấy); `ParentCareLog` bỏ cảnh báo `handled_note like 'tự đóng%'`.
- DT-04 lịch ôn 1/3/7 ngày: trigger BEFORE `trg_mistake_lich_137` trên `student_mistakes` (migration `20261018110000`) chỉ chỉnh HS thuộc lớp có cờ `on_tap_1_3_7`; **cờ bật cho lớp 12 (class_id 18, 110 HS thật, 1235 bẫy)**, lớp 11 đối chứng. Lớp có cờ cần 3 lần đúng để xoá bẫy (lớp thường 2). Tắt: `update feature_flags set enabled=false where flag='on_tap_1_3_7'`.
- DT-03: lớp 12 đã phủ đủ quiz `.tl-quiz` (6–8/bài) + bộ 20 câu (bài 12 mới làm: exam 937). Lớp 10: 34 bài (id 46–79) exam 941–974, 666 câu (9 bài còn 18–19 câu). Gán YCCĐ 196/212 câu thiếu `topic_id` bằng `scripts/gan-yccd-ngan-hang-l10.mts` (`--apply` sinh SQL, chạy bằng `supabase db query -f`, rồi `--verify`; `--undo <sao lưu>`); bảng duyệt ở `scripts/data/duyet/gan-yccd-l10/`; 16 câu NONE giữ nguyên (chuyển động cơ/hệ quy chiếu, phương án cổng quang, hiệu chỉnh dụng cụ) chờ thầy quyết có thêm YCCĐ mới không.
- DT-16: `hsg-ai-grade` bỏ DeepSeek (commit e1a9ca706) — **thầy tự deploy Edge Function**; RLS các bảng hành vi chưa soát bằng `pg_policies`.

**Còn chờ (ưu tiên)**
1. Sau vài ngày: `select kind, count(*), avg(duration_s) from learning_events group by 1`; vẫn 0 → kiểm client. Sau 6:00 xem 95 cảnh báo có hợp lý với GV/TA không.
2. Deploy `hsg-ai-grade` + soát RLS.
3. Báo cáo so lớp 12 vs lớp 11 (tỉ lệ đúng khi ôn, số bẫy cleared) sau ~3 tuần; nút "Rà lại" cảnh báo ở dashboard.
4. Phủ nốt bộ 20 câu: KHTN 9 (20 bài), L11 (bài 23, 26, 29), AVCN. DT-05/06 sau khi có dữ liệu DT-01 + kết quả DT-04; DT-15 chờ hết mùa xếp hạng (25/10); DT-08 hoãn Q2/2027.

**Quyết định/bẫy không suy ra được từ code**
- HS thật dùng email `@thachlab.local` (~153); chỉ `hs.test%` là tài khoản thử — đừng lọc theo cả đuôi.
- Đáp án đúng là phương án dài nhất ở 40% câu trắc nghiệm L10 (thầy chọn KHÔNG sửa); ghi vào nhật ký skill `soan-quiz-ly-thuyet`.
- Update `exams.questions` qua REST bị `statement timeout` (trigger `trg_exams_sync_bank` đồng bộ cả đề vào ngân hàng); ghi hàng loạt phải qua SQL file có `set local statement_timeout` (mẫu: sinh bởi `scripts/gan-yccd-ngan-hang-l10.mts`). Hash câu bỏ qua `topic` nên đổi topic không sinh dòng ngân hàng trùng.
- `next build` ở main từng lỗi typecheck do script `.mts` của phiên khác (`scripts/*giai-lai*.mts`); deploy 17/10 build từ worktree sạch (`git worktree add … HEAD --detach`, `cp -Rc node_modules`, `cp .env.local`, `bash scripts/deploy.sh`, xoá worktree). Kiểm cảnh báo `manifest rỗng` của build-content: Supabase chậm sau ghi hàng loạt thì chạy lại.
- Brief agent soạn quiz song song: cấm câu "đếm số mục đã liệt kê", `explanation` gọi phương án bằng A–D, `theorySection` lấy từ `sections<id>.txt`, mỗi agent thư mục scratch riêng (xem nhật ký skill).

Liên quan: [[project_thachlab_rank_system]], [[project_thachlab_phu_dao]], [[project_thachlab_hs_test_accounts]]
