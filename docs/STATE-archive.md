# STATE-archive — log migration đã chạy (tách khỏi STATE.md 28/09/2026)

Lịch sử các đợt migration đã chạy xong trên production, chuyển sang đây để STATE.md chỉ còn việc
đang chờ/đang treo. Log chạy thực tế ở `scripts/logs/`, rollback ở `perf/rollback/`.

## Migration — 06/10/2026 (sổ học phí; đã chạy 17:14)
Log: `scripts/logs/20261006-171434-20261006120000_thpt_fee_ledger.log`. Đã xác nhận 4 bảng `thpt_fee_*` + 13 RPC trong DATABASE.md.

- `20261006120000_thpt_fee_ledger.sql` — sổ học phí theo tháng, **ẩn** (`staff_visible` và `family_visible` đều false, không có menu). Không đổi ô "Đã đóng" hiện tại. Bật cho giáo viên bằng SQL `update public.thpt_fee_settings set staff_visible = true, updated_at = now() where id;` rồi mở `/quan-tri/hoc-phi`. Phụ huynh chỉ thấy từng tháng sau khi admin bật "Phụ huynh thấy sổ tháng" trên trang đó. Rollback: cuối file và `perf/rollback/20261006120000_thpt_fee_ledger.down.sql`. Bất kỳ lúc nào.

## Migration — 03/10/2026 (đã chạy; dọn khỏi STATE.md 5/10/2026)
Log: `scripts/logs/20261003-225719-*` (130000, 140000, 150000 — chạy 3/10 22:57). `20261002110000`, `20261001100000`, `20260930160000_rank_title_distinct_questions` đã chạy trước 3/10 13:20 (kiểm trên production).
Chưa có UI gọi RPC `rank_theory_open/submit` (140000) và chưa bài nào có dòng khoá, nên chưa cộng RP cho ai.

- `20261003150000_phu_dao_kiem_tra_cuoi_buoi.sql` (bảng `tutoring_exit_windows`, cột `tutoring_exit_attempts.window_id`, guard cửa sổ 10 câu/70%, hàm `ta_tutoring_pass_ratio`, `ta_monthly_policy` tính 25đ phụ đạo theo tỉ lệ nhóm đạt ≥60%/40–59%/<40%; chạy lúc nào cũng được; rollback `perf/rollback/20261003150000_phu_dao_kiem_tra_cuoi_buoi.down.sql` — đọc đầu file về thứ tự) — ĐÃ CHẠY 3/10/2026 22:57 (log `scripts/logs/`), cùng `20261003130000` và `20261003140000`. UI trợ giảng (`PhudaoPlanner`) và học sinh (`ThptStudentHome`) chưa commit/deploy.
- `20261003130000_parent_attendance_announcements.sql` (policy cho phụ huynh đọc `class_announcements` của lớp con — sửa lỗi "Bài tập về nhà" luôn rỗng ở /phu-huynh — + RPC `parent_attendance_summary`; chỉ đọc, chạy lúc nào cũng được; rollback `perf/rollback/20261003130000_parent_attendance_announcements.down.sql`) — ĐANG CHỜ. Code client đã deploy trước, tự ẩn khối điểm danh tới khi chạy.
- `20261003140000_rank_theory_rp.sql` (RP bài lý thuyết: bảng `theory_quiz_keys`/`theory_sessions`, RPC `rank_theory_open`/`rank_theory_submit`, chỉ cộng RP; chạy lúc nào cũng được; rollback `perf/rollback/20261003140000_rank_theory_rp.down.sql`) — ĐANG CHỜ. Chưa có UI gọi RPC và chưa có bài nào có dòng khoá, nên chạy xong chưa cộng RP cho ai.
- **Lưu ý 3/10/2026 13:20 (kiểm trên production):** 6 file dưới đây (`20260930160000`, `…170000`, `…180000`, `20261001100000`, `20261002100000`, `20261002110000`) ĐÃ CHẠY rồi — hàm tồn tại trên DB, log `scripts/logs/`; 2 file `…170000`/`…180000` đã mất khỏi đĩa. Các dòng ĐANG CHỜ bên dưới của chúng là cũ, đã bỏ khỏi `FILES`; phiên nào sở hữu thì tự chuyển sang `STATE-archive.md`.
- `20261002110000_staff_student_account.sql` (hàm `staff_student_account`: thẻ "Thông tin tài khoản" trong hồ sơ HS cho admin/GV — username, email, SĐT, SĐT phụ huynh, ngày sinh; chạy lúc nào cũng được; rollback `perf/rollback/20261002110000_staff_student_account.down.sql`) — ĐANG CHỜ.
- `20261001100000_resolve_login_email.sql` (hàm `resolve_login_email`: đăng nhập bằng username cho tài khoản đăng ký kèm email thật; chạy lúc nào cũng được; rollback `perf/rollback/20261001100000_resolve_login_email.down.sql`) — ĐANG CHỜ. Client đã gọi RPC, chưa chạy thì tự rơi về `@thachlab.local`.
- `20260930160000_rank_title_distinct_questions.sql` (chống cày danh hiệu: đếm số câu khác nhau; `create or replace rank_title_stats`; chạy lúc nào cũng được; rollback `perf/rollback/20260930160000_rank_title_distinct_questions.down.sql`) — ĐANG CHỜ.
- `20260930170000_question_bank_hash_ignore_image_ts.sql` (gộp ~4,7k câu trùng, ngoài giờ HS) và
  `20260930180000_bank_similarity_per_topic.sql` (sửa trang "Nghi trùng lặp" luôn lỗi timeout: quét theo từng chủ đề).
  Code client đã sửa cùng lúc (`services/question-bank.ts`) — cần chạy migration TRƯỚC khi deploy.

## Migration — 04/10/2026 22:58 (đã chạy, log `scripts/logs/20261004-225841-*`)
- `20261004230000_thpt_course_pairs.sql` (lớp 12 học 2 buổi/tuần: điền `pair_key='Vật lí 12L1'`, `pair_slot` A/B cho 4 khoá id 5–8 + comment cột; CHỈ update dữ liệu, chạy lúc nào cũng được; rollback ở cuối file) — ĐÃ CHẠY 4/10/2026 22:58. Code (trang chủ, `/khoa-hoc`, `/khoa-hoc/dang-ky`) đã deploy 4/10 và tự suy buổi A/B từ tên khoá khi cột trống, nên chưa chạy vẫn hiện đúng; ràng buộc "chọn 1A + 1B" mới ép ở client, RPC `thpt_register` chưa ép.
- `20261004130000_phu_dao_xem_lai_ly_thuyet.sql` (bắt buộc xem lại lý thuyết tương tác trước bài tự kiểm tra thoát phụ đạo: bảng `tutoring_theory_reviews`, RPC `tutoring_review_start`/`tutoring_review_ping`, hàm `tutoring_theory_item`, thay guard `tutoring_exit_attempt_guard`; chạy lúc nào cũng được; rollback `perf/rollback/20261004130000_phu_dao_xem_lai_ly_thuyet.down.sql`) — ĐÃ CHẠY 4/10/2026 22:58. Client (`TheoryReviewStep`, `TutoringExitQuiz`) tự bỏ qua bước xem lại khi RPC chưa có. Test SQL bằng pglite 4/10/2026 qua; CHƯA test UI với tài khoản HS thật. Lớp 12: bộ Kiểm tra nhanh chưa đăng (xem mục dưới) nên phần "câu dễ từ quiz lý thuyết" chỉ có hiệu lực sau khi đăng bộ quiz.
- `20261004120000_phu_dao_hang_cho.sql` (bảng `tutoring_waitlist`, trigger tự đẩy em đầu hàng chờ lên khi có người huỷ — thay hàm `tutoring_slot_unregister`, RPC `tutoring_waitlist_mine` + `tutoring_slot_open_next`; chạy lúc nào cũng được; rollback ở cuối file) — ĐÃ CHẠY 4/10/2026 22:58. Client (`TutoringSlotsPlanner`, `ThptStudentHome`, `CatchupCard`) gọi bảng/RPC này; chưa chạy thì nút "vào hàng chờ" báo lỗi.
Sau khi chạy: `gen-database-doc.mjs` ghi 109 bảng/261 hàm; `pair_key`/`pair_slot` của 4 khoá 12L1 đã điền (kiểm REST).

## Migration — 04/10/2026 (đã chạy)
`20261004100000_bank_grade_thi_thu_tn.sql` — gắn `grade='12'` cho 5 899 câu `question_bank` từ đề thi thử TN/minh hoạ (trước đó `grade=''`, không chủ đề). Chỉ đụng cột grade.
Kết quả: khối 12 = 11 023 câu, còn 11 câu chưa rõ khối (đề 209, 258 — gắn tay ở "Câu chưa rõ khối"). Rollback ở cuối file; id lưu trong `question_bank_grade_fix_20261004`.

## Migration — 30/09/2026 17:15 (đã chạy)
`20260930160000_exit_quiz_bank_children.sql` — policy `student reads exit-quiz bank questions` trên `question_bank` mở cho HS đọc cả câu ở
YCCĐ con của bài đang cần phụ đạo (trước đó 11/25 cặp bài×dạng hiện "chưa có câu nào"). Log `scripts/logs/20260930-171530-*` OK.
Rollback: `perf/rollback/20260930160000_exit_quiz_bank_children.down.sql`. Client `fetchTopicFamilyIds` (services/tutoring.ts) sửa cùng đợt.
Chưa kiểm bằng tài khoản HS thật.

## Migration — đợt 29/09/2026 (đã chạy hết)
**File thứ 4 `20260929130000_rank_weekly_goal_adaptive.sql` (mục tiêu tuần thích ứng) đã chạy 29/9 17:43 VN** (log `scripts/logs/20260929-174330-*`, OK).
Xác nhận trên Singapore: `rank_weekly_goal_of` có mặt, gọi được bằng service_role, anon bị chặn (401), `rank_public_honor` vẫn 200.
Số liệu thật ngay sau khi chạy (chỉ đọc): mùa 4 tuần 28/9 có 59/164 em đủ lịch sử để có mục tiêu riêng, 49 em ra 1 bài và 10 em ra 2 bài,
ngưỡng 4,0–8,5; mục tiêu chung của mùa 4 là 2 bài ≥7. Mùa 5 (Alpha test) chỉ bật 2 nguồn `rank_sources` nên cả 42 em dùng mục tiêu chung
(mục tiêu riêng chỉ đếm bài thuộc nguồn tính RP của mùa). Lịch sử trung vị chỉ 3 bài/2 tuần vì mùa mới mở, nên đa số được mục tiêu 1 bài/tuần.
Chưa có lượt làm bài mới từ 14:04 VN nên chưa thấy RP mục tiêu tuần cộng theo luật mới.
Chi tiết thiết kế: `20260929130000_rank_weekly_goal_adaptive.sql` — GĐ 1b việc 2, mục tiêu tuần THÍCH ỨNG: mỗi em có mục tiêu riêng từ 2 tuần trước
  của chính em (số bài = nhịp x 75%, tối đa 5; ngưỡng điểm = mức ~80% bài gần đây của em đạt, làm tròn 0,5, trong 4–8,5).
  Chưa đủ lịch sử (<3 bài/2 tuần) thì dùng mục tiêu chung của mùa như cũ. Định nghĩa lại đúng 2 hàm
  (`rank_eval_weekly_goal`, `rank_status_of`) + thêm `rank_weekly_goal_of`; trạng thái thêm khoá `personal`. Tắt tức thì bằng
  `weekly_goal_personal = 0` trong cấu hình mùa (trang quản trị mùa, không cần rollback); mọi số chỉnh ở cùng chỗ. Đã kiểm trên
  Postgres 16 cục bộ (6 kiểu học sinh, chấm tuần không cộng đôi, công tắc, chỉnh độ khó, rollback + áp dụng lại), CHƯA chạy trên dữ liệu thật.
  Lưu ý: ROADMAP viết "ngưỡng nhỉnh hơn trung bình" nhưng cũng "nhắm ~80–85% thành công"; đã ưu tiên tỉ lệ thành công. Chuỗi ngày vẫn dùng ngưỡng chung.

**Cập nhật: file 3 (`rank_honor_progress`) bị Thạch rollback ~14:00 VN rồi cả 3 file được chạy lại đủ 14:04 VN (log `scripts/logs/20260929-140443-*`, đều OK). Đã xác nhận: `rank_public_honor` trả 200 cho anon, có khoá `improved_acc`.**
**Trạng thái xác nhận 29/09/2026 (project Singapore `jgvbdbpvjdntdgzthumv`)**: file 1 chạy OK (log máy Thạch); file 2 lần đầu
lỗi `TransportError` ở bước đăng nhập của CLI (chưa chạy câu SQL nào), chạy lại `--only 2` thì xong; file 3 lỡ chạy TRƯỚC
file 2 nên `rank_public_honor` báo lỗi 42883 (thiếu `rank_progress_calc`) trong một khoảng ngắn cho tới khi file 2 xong. Đã thêm chốt
chặn thứ tự vào file 3 (commit 517fa23). Còn phải làm: `node scripts/gen-database-doc.mjs` trên máy Thạch (cần supabase CLI
link), và cộng bù chuỗi ngày 26–29/9 (`select rank_recompute_season(4);` `(5)`) nếu thầy quyết. Chưa xác nhận chuỗi ngày và
tiến bộ tuần cộng RP thật: cần có lượt làm bài mới (ledger chưa có dòng nào từ 00:49 29/9 VN).

Ba file viết 29/09/2026, chạy trên máy Thạch bằng `bash scripts/run-migrations.sh`, theo thứ tự:
1. `20260929100000_rank_restore_daily_streak.sql` — **sửa lỗi**: chuỗi ngày ngừng cộng RP từ 26/9 00:03 (VN)
   vì migration `20260926110000_rank_exclude_staff` định nghĩa lại `rank_on_result` từ bản cũ, làm rơi dòng
   `rank_eval_daily_streak`. Bằng chứng: ledger có 29 dòng `daily_streak` ngày 25/9, sau đó 0 dòng dù >230 lượt
   luyện tập được cộng RP. Cộng bù 26–29/9 là tuỳ chọn: `select rank_recompute_season(4);` và `(5)` (RP các em tăng ngay).
2. `20260929110000_rank_progress_week.sql` — GĐ 1b việc 1, "tiến bộ so với chính em": tỉ lệ đúng tuần này so với 2 tuần
   trước; tăng ≥5 điểm % (và ≥15 câu mỗi bên) thì +15 RP, +5 RP mỗi 5 điểm % tăng thêm, tối đa 25. Mọi số
   chỉnh qua `rank_seasons.config` (`progress_min_gain_pct`, `progress_rp`, `progress_rp_max`,
   `progress_step_pct`, `progress_step_rp`, `progress_min_questions`), không cần sửa code — điều chỉnh sau mùa 1.
3. `20260929120000_rank_honor_progress.sql` — bảng vinh danh tuần trang chủ thêm "Tiến bộ nhất" theo tỉ lệ đúng
   (`improved_acc`); client đã sửa sẵn (`HonorBoardPanel`), client cũ vẫn chạy.
Đã kiểm trên Postgres 16 cục bộ (bảng giả + hàm `rank_award` thật): 7 ca (đúng ngưỡng, gần 100%, thiếu dữ liệu,
tự luận, luyện tập, giáo viên, lặp lại không cộng đôi), quyền anon, rollback + áp dụng lại — đều đạt. Đã xác nhận trên Singapore sau khi chạy (hàm có mặt, RPC vinh danh trả 200 cho anon, quyền đúng); CHƯA thấy
hoạt động thật vì chưa có lượt làm bài mới từ lúc chạy. Chưa có: thành tích/huy hiệu "Tiến bộ tuần" (để đợt sau). Tiến bộ chỉ tính khi có lượt làm bài mới,
không cộng bù tuần đã qua.

## Migration — đợt 28/09/2026 (đã chạy hết)
- **Đổi tên 7 bậc rank theo Liên Quân Mobile** (28/9/2026) → ĐÃ CHẠY 28/9 23:47 (log
  `scripts/logs/20260928-234708-*`), kiểm tra `rank_tiers` cả 2 mùa đã mang tên mới: Tinh Quang…Chí Tôn → Đồng, Bạc, Vàng,
  Bạch Kim, Kim Cương, Tinh Anh, Cao Thủ (đúng thứ tự thấp → cao của LQM); danh vị Vô Song/Paragon
  đổi tên hiển thị thành "Thách Đấu" (bậc thứ 8 của LQM, chỉ ở frontend — không thêm dòng vào
  `rank_tiers`). Chỉ đổi cột `name` + hàm `rank_seed_tiers` (tên mùa mới), không đổi `code`/min_rp/
  điều kiện lên bậc nên không ảnh hưởng RP đã tính. Phần frontend (features/rank/types.ts,
  components/rank/*, components/admin/RankAdmin.tsx) đã đổi tên xong, chỉ còn phần DB.
  Migration: `supabase/migrations/20260928190000_rank_tier_names_lien_quan.sql`
  (rollback `perf/rollback/20260928190000_rank_tier_names_lien_quan.down.sql`).
- **Vinh danh tuần v2** (28/9/2026): CẢ HAI ĐÃ CHẠY — 20260928160000 lúc 11:39, 20260928180000 lúc 13:46 (log `scripts/logs/20260928-134634-*`), RPC thật kiểm OK. Ghi lại để tham khảo: bản 160000 ĐÃ chạy 11:39 (log `scripts/logs/20260928-113911-*`),
  RPC trả dữ liệu thật OK. Bản v2 sửa 2 điểm thấy từ dữ liệu thật: `rank_honor_name` bỏ phần trong ngoặc,
  từ có chữ số, ký tự lạ (tên HS tự nhập bẩn: "đỗ đăng duy(oguri cap...)" → "Duy Đ."); `rank_public_honor`
  trả thêm `top_more` (số bạn đồng hạng bị cắt khỏi bục 5 ô). Chỉ thay 2 hàm.
  Migration: `supabase/migrations/20260928180000_rank_public_honor_v2.sql`
  (rollback `perf/rollback/20260928180000_rank_public_honor_v2.down.sql`). Chạy giờ nào cũng được.
- **Giữ database không phình vô hạn** (28/9/2026, đợt rà hạn mức Supabase Free) → ĐÃ CHẠY 28/9 11:39
  (log `scripts/logs/20260928-113911-*`), pg_cron bật được, job `question-results-rollup` 20:00 UTC ngày 1
  hằng tháng, dry-run sau migration 0 lượt cần gộp (đúng). Code đã commit 5be86330 + push + deploy 13:11 (thin push d806d77). Cơ chế: bảng gộp
  `question_result_rollups` + hàm `rollup_question_results(p_before, p_dry)` gộp rồi xoá dòng
  `exam_question_results`/`practice_question_results` của lượt làm cũ hơn 12 tháng (giữ lượt có câu tự
  luận), đánh dấu `results_rolled_up_at`; `rank_title_stats` cộng thêm phần gộp; xoá đáp án JSON tạm
  trong `exam_attempts` đã nộp (code `finishExamAttempt` cũng xoá từ nay); lịch pg_cron 3:00 ngày 1
  hằng tháng nếu extension bật được, không thì chạy tay `select public.rollup_question_results();`.
  Migration: `supabase/migrations/20260928170000_question_results_retention.sql`
  (rollback `perf/rollback/20260928170000_question_results_retention.down.sql`). Migration KHÔNG tự
  xoá dữ liệu; hiện chưa có lượt nào > 12 tháng nên lần gộp đầu thực sự diễn ra ~9/2027.
  Script `scripts/backfill-exam-analytics.mjs` đã sửa để bỏ qua lượt đã gộp.
- (Bảng `question_bank_backup_20260925` đã xoá 28/9/2026 10:55 qua
  `20260928150000_drop_question_bank_backup.sql`, log `scripts/logs/20260928-105508-*`.)

## Migration — ĐÃ CHẠY XONG (27/09/2026, 07:32)
Cả 8 file trong `supabase/migrations/` đã chạy lên production qua `bash scripts/run-migrations.sh`:
perf_indexes, perf_rpc_gv, perf_rls, difficulty_source, mastery, lesson_item_draft_publish,
exam_violation_alert, fix_question_bank_similarity_timeout. Cộng rank_paragon, rank_exclude_staff,
fix_rls_tautology chạy trước đó. Rollback từng file ở `perf/rollback/`.

- Cột `exam_id` trên `class_announcements` (gắn đề vào "Việc cần làm hôm nay", nút "Làm bài" ở
  trang chủ HS): migration `20260927100000_class_announcement_exam.sql` ĐÃ chạy 27/9/2026 (log
  `scripts/logs/20260927-084117-*`, rollback `perf/rollback/20260927100000_class_announcement_exam.down.sql`).
  Code (services/announcements.ts, ClassAnnouncementsPanel, ThptStudentHome) đã deploy 27/9/2026.

- **Báo lỗi gắn vào đúng câu hỏi**: cột `exam_id`/`question_index` trên `bug_reports` + nhãn
  `category='cau_hoi'` — migration `20260927110000_bug_report_question_link.sql` ĐÃ chạy 27/9/2026
  (log `scripts/logs/20260927-104450-*`, rollback
  `perf/rollback/20260927110000_bug_report_question_link.down.sql`). Học sinh bấm "Báo lỗi câu này"
  ở màn Xem lại bài làm ([ReportQuestionButton.tsx](../components/exams/ReportQuestionButton.tsx));
  admin ở `/quan-tri/bao-loi` bấm link "Đề #… · Câu N →" nhảy thẳng vào `/quan-tri/sua-de?exam=&q=`,
  tự mở đúng đề + tô khung vàng đúng câu. Tiện thể vá luôn 1 lỗi nhỏ: nút "Báo lỗi / Góp ý" chung
  (mọi trang) trước làm rớt mất `#hash` của URL nên link báo lỗi lý thuyết chỉ mở tới đầu trang, mất
  luôn đoạn `#theory-sec-…` — đã sửa trong `BugReportWidget.tsx`. Đã deploy 27/9/2026 — **chưa test
  UI thật bằng tài khoản có login**.

## Migration — ĐÃ CHẠY 28/9/2026 10:42 (thầy chạy qua scripts/run-migrations.sh, log scripts/logs/20260928-104205-*)
- **Mã danh hiệu đang đeo trong RPC lớp** (28/9/2026, tính năng "đeo danh hiệu dưới tên + khung sưu tập
  huy hiệu", xem `docs/rank-title-showcase-design.md`): `rank_class_groups` trả thêm `title.code`,
  `rank_class_board` trả thêm `top_week[].title` → chip bạn cùng lớp và top tuần hiện logo huy hiệu.
  Client chấp nhận cả dạng cũ. ĐÃ CHẠY 28/9 10:42. Migration:
  `supabase/migrations/20260928130000_rank_title_code_in_class_rpcs.sql`
  (rollback `perf/rollback/20260928130000_rank_title_code_in_class_rpcs.down.sql`).

- **3 mức danh hiệu chuyên môn khớp độ khó câu hỏi** (28/9/2026, theo yêu cầu thầy): Thức Tỉnh cần
  đủ số câu Dễ giải đúng, Làm Chủ cần đủ số câu Trung bình, Huyền Thoại cần đủ số câu Khó (bỏ điều
  kiện % chính xác + đề thử thách riêng cũ), tính trên mọi lượt làm đề + luyện tập. Thêm cột
  `difficulty` vào `exam_question_results`/`practice_question_results` (backfill dữ liệu cũ từ
  `exams.questions`), cột `min_de`/`min_tb`/`min_kho` vào `rank_titles`. Code (services/rank.ts,
  features/rank/types.ts, components/rank/TitleCollection.tsx, components/admin/RankAdmin.tsx,
  features/rank/preview.ts, services/lessons.ts, features/exams/types.ts) đã commit + deploy 28/9/2026.
  Migration: `supabase/migrations/20260928100000_rank_specialist_difficulty.sql`
  (rollback `perf/rollback/20260928100000_rank_specialist_difficulty.down.sql`). Chạy xong thì chạy
  tiếp `docs/supabase-recompute-rank-titles-20260928.sql` để xét lại danh hiệu cho HS đã đủ điều
  kiện theo logic mới. → ĐÃ CHẠY 28/9 ~10:50 (rank_recompute_season(4) + (5); CLI chỉ in kết quả lệnh cuối: 42 HS mùa 5).

- **Vá lỗ hổng phân quyền `/kiem-tra/lam`** (27/9/2026, phát hiện lúc test `perf5/test-exam-flow`)
  — học sinh đã đăng nhập có thể làm và NỘP bất kỳ đề `published` nào qua
  `/kiem-tra/lam?id=<id>` dù không thuộc lớp mình (URL chia sẻ / đoán id tăng dần), vì
  `RequireAuth` ở trang đó không kiểm tra lớp, và RLS `exams`/`exam_results`/
  `exam_question_results` cũ chỉ yêu cầu `published`/`student_id = auth.uid()`, không đối
  chiếu `exam_classes` ↔ `user_classes`. Đã sửa UI (`app/kiem-tra/lam/page.tsx`, chặn sớm +
  báo "Đề này không thuộc lớp của em") + migration
  `20260927150000_exam_class_access.sql` — thêm 3 policy RLS **restrictive** trên
  `exams`/`exam_results`/`exam_question_results` (AND với policy cũ, không đổi hành vi
  admin/instructor/tro_giang, không đổi đề "toàn trường" không gán lớp — đúng logic
  `services/content.ts#visibleTo` đang dùng). **ĐÃ CHẠY production 27/9/2026** qua
  `supabase db query --linked -f` (worktree không có `supabase link` nên chạy trực tiếp bằng
  đường dẫn tuyệt đối tới file trong worktree, không qua `scripts/run-migrations.sh`) — đã soi
  lại `pg_policies` xác nhận 3 policy restrictive lên đúng, không đụng 2 policy "parent reads…"
  mới hơn (khác lệnh SELECT/INSERT nên không xung đột). Rollback nếu cần:
  `supabase db query --linked -f perf/rollback/20260927150000_exam_class_access.down.sql`.
  Code UI đã commit (nhánh `claude/cranky-colden-989171`, chưa merge/deploy) — **chưa tự kiểm
  bằng tài khoản học sinh thật** (mở đề lớp khác phải báo "không thuộc lớp", mở đúng đề lớp mình
  phải làm/nộp bình thường); merge + deploy để lên web thật.

- **Chấm BTVN trên lớp + BTVN ôn tập tự động sau chữa bài** (27/9/2026) — 2 migration
  `20260927130000_homework_check.sql` (bảng `class_homework_checks` + RPC
  `homework_check_set`, cộng RP) và `20260927140000_class_review_homework.sql` (bảng
  `class_review_homework`) ĐÃ CHẠY (log `scripts/logs/20260927-182457-*`, rollback ở
  `perf/rollback/`). Đã nối dây đủ 4 chỗ: `ClassAnnouncementsPanel.tsx` (nút chấm BTVN
  cạnh mỗi thông báo), `app/phu-huynh/page.tsx` (ParentHomeworkNotes), `ThptStudentHome.tsx`
  (mục "Việc cần làm hôm nay"), `ReviewBoard.tsx` (nút "Tạo BTVN ôn tập"). Đã
  `bash scripts/deploy.sh` — **đã lên web thật** (commit dd9bd74e). Chưa tự kiểm bằng
  tài khoản đăng nhập thật (chấm 1 BTVN, xem trang phụ huynh, bấm "Tạo BTVN ôn tập").

Cột `lesson_items.summary_html` (Tóm tắt ý
chính cần thuộc) ĐÃ chạy 27/9/2026 (`20260927120000_lesson_item_summary.sql`,
log `scripts/logs/20260927-173722-*`, rollback
`perf/rollback/20260927120000_lesson_item_summary.down.sql`). Backfill đã xong: cả 81/81 mục
`ly_thuyet` có `summary_html` (script `scripts/backfill-lesson-summary.mts` — không rõ ai chạy,
kiểm tra thấy đã có dữ liệu sẵn khi thầy chạy lại 27/9 tối). Đã `bash scripts/deploy.sh` lại
(file tĩnh `public/data/` đã có nội dung mới, 81/81 file có `summary_html`) — khối "📌 Tóm tắt ý
chính" giờ lên web thật.


- 30/9/2026: `20260930100000_tutoring_exit_cooldown.sql` đã chạy (GĐ 1b #3 — chờ 24 giờ thay giới hạn 3 lượt; rollback `perf/rollback/20260930100000_tutoring_exit_cooldown.down.sql`).
- 30/9/2026 16:07: đợt GĐ 1b — 5 file đã chạy OK (log `scripts/logs/20260930-160718-*`), rollback ở `perf/rollback/`:
  `20260930110000_rank_board_by_tier` (bảng lớp theo bậc), `20260930120000_rank_gd1b_spacing_progress` (thành tích Tiến Bộ Tuần + Huyền Thoại rải ≥ 2 tuần),
  `20260930130000_rank_streak_freeze` (đóng băng chuỗi 1 ngày/tuần, ngày mới từ 3h sáng), `20260930140000_rank_class_goal` (mục tiêu chung lớp, trigger trên `rank_title_awards`),
  `20260930150000_rank_teacher_reports` (`rank_monday_list`, `rank_quartile_metrics`). Cấu hình mùa mới: `legend_min_weeks`, `streak_day_offset_hours`, `streak_freeze_per_week`, `class_goal_*`.

- 30/9/2026 19:59: `20260930160000_rank_title_distinct_questions.sql`, `20260930170000_question_bank_hash_ignore_image_ts.sql` (hash bỏ tiền tố ảnh + `difficultySource`; ngân hàng 12 925 → 7 869 dòng; backup `*_backup_20260930` — drop khi chắc chắn).
- 3/10/2026 13:30: `20261003100000_rank_gate_adaptive.sql` (thi thăng hạng thích ứng: bảng rank_gate_attempts, RPC rank_gate_*, 3 cột ngưỡng rank_tiers, sửa rank_eval_gates/rank_tier_needs_gate/rank_status_of), `20261003110000_rank_rp_first_attempt.sql` (RP chỉ tính lượt đầu, cờ rp_first_attempt_only=1), `20261003120000_distractor_notes.sql` (hash bỏ distractorNotes + bank_set_distractor_notes). Log scripts/logs/20261003-133029-*. Spec: docs/BAN-GIAO-RANK-THI-THANG-HANG-2026-10-03.md. Kiểm sau chạy: rank_gate_mode(4)=adaptive, pool lớp 12/11/10 = 4721/1702/779 câu, HS Đại Sư top có can_start=true cho cao_thu.
  Dòng ĐANG CHỜ gốc: - `20261003120000_distractor_notes.sql` (**ghi chú phương án nhiễu** cho Luyện tập "Từng câu": `question_content_hash` bỏ qua key `distractorNotes` — bắt buộc trước khi ghi ghi chú, nếu không trigger đồng bộ đề↔ngân hàng sinh dòng trùng — + hàm `bank_set_distractor_notes`; ngoài giờ HS; rollback `perf/rollback/20261003120000_distractor_notes.down.sql`; test `docs/supabase-test-distractor-notes.sql` — sạch trong begin…rollback) — ĐANG CHỜ. Client Luyện tập Từng câu (`PracticeStepView`, công tắc Từng câu/Cả bài) KHÔNG cần migration này (chưa có ghi chú thì chỉ hiện lời giải). Sau khi chạy: thử `npx tsx scripts/backfill-distractor-notes.mts 20 --dry-run` rồi `… 20` (ghi thật, cần service role + ANTHROPIC_API_KEY), xem trong Luyện tập, rồi mới chạy hết. | - `20261003110000_rank_rp_first_attempt.sql` (**RP chỉ tính lượt đầu** của mỗi bài trong mùa: `create or replace rank_on_result`, cờ mùa `rp_first_attempt_only` mặc định 1; RP đã cộng giữ nguyên; ngoài giờ HS làm bài; rollback `perf/rollback/20261003110000_rank_rp_first_attempt.down.sql`; test `docs/supabase-test-rank-rp-first.sql` — chạy thử trong begin…rollback: FAIL khi chưa có migration, PASS khi có) — ĐANG CHỜ. Đề xuất config **mùa 2** (thầy quyết lúc mở mùa): `practice_max_rp 30`, `weekly_goal_rp 40`, giữ `fix_max_rp 30`. Việc tay: gắn `challenge_exam_id` cho cao_thu/thach_dau season 4 để 3 em Đại Sư có đích; sau khi thi thích ứng chạy thì bỏ gán. | - `20261003100000_rank_gate_adaptive.sql` (**thi thăng hạng thích ứng**: b

- **ĐÃ CHẠY 7/10/2026:** `20261007120000_tu_vao_lop_thpt.sql` — học sinh THPT tự vào lớp (RLS `user_classes` cho ghi `active`); 17 yêu cầu đang chờ đã chuyển `active`, sao lưu ở `user_classes_backup_20261007`. Đã đối chiếu DB: 0 pending, 2 policy đúng. Còn lại: deploy code.

## Chuyển từ STATE.md ngày 7/10/2026 (mục "Đã hoàn thành" cũ)
- **Hero có tab 4 "Hình chiếu" — bóng của M quay đều đồng nhịp với con lắc lò xo (4/10/2026)**:
  `components/physics/ShadowSpringSimulation.tsx` + `hooks/useCircularProjection.ts` + `lib/circularProjection.ts`
  (toán thuần; 34 kiểm ở `tmp/hero-review/hinhchieu-check.mts`, gồm đối chiếu `so_lieu_mau` của spec
  `tn-l11-daodongdieuhoa-03`). Hai hệ chạy trên **cùng một trục x**: làn trên là đường tròn bán kính A₁ = 6 cm có
  điểm M quay đều (Q là hình chiếu, có chấm mỗi 0,1 s để thấy bóng KHÔNG chuyển động đều), làn dưới là con lắc
  lò xo **nằm ngang** (k = 4 N/m, chỉnh m) — học sinh tự khớp ω = √(k/m) rồi tự thử câu hỏi chính: *kéo con lắc
  ra xa gấp đôi thì nhịp có đổi không?* (không: T = 2π√(m/k) không chứa A).
  Câu nhận xét tách **5 trạng thái**; `samePeriod` là chỗ dễ nói sai nhất: **khớp ω chỉ làm hiệu pha THÔI TĂNG,
  không xoá phần đã lệch** — cùng chu kì vẫn có thể khác pha, muốn trùng nhau phải thả cùng lúc (nút "Đặt lại").
  Tab nạp chậm qua `next/dynamic` + `LazyErrorBoundary`: JS tải đầu trang chủ **216 KB gzip — không đổi** so với
  baseline 3 tab, chunk riêng 17 KB raw / 6 KB gzip. Hàng tab 4 mục lộ hết ở 360px, mỗi nhãn 1 dòng, không tràn
  ngang (D4 — nhãn phải `whitespace-nowrap` + chữ 13px ở mobile). Quy tắc áp dụng: B4, B8, N1, N2, N7, C1, D2,
  D4, M2, M4, H3.
  **Chặng 2 CHƯA làm**: nhúng bản tương tác này vào bài 1 lớp 11 (lesson 20, mục 5 "Liên hệ với chuyển động tròn
  đều") — chưa có cơ chế nào để nhúng mô phỏng vào `theory.html`; phải thêm placeholder + mount trong
  `components/exams/ContentHtml.tsx` (nhớ: mount SAU khi KaTeX render xong, và chỉ bài đó trả giá chunk).
  **Chưa deploy.**
- **Hero: tab 2 đổi từ "Dao động" (con lắc lò xo) sang "Thả hàng" — máy bay cứu hộ thả gói hàng (5/10/2026)**:
  đúng cảnh mở bài của **Bài 12. Chuyển động ném, Vật lí 10 (lesson 57, đang published)** và đúng cái bẫy đã
  ghi trong `content/thi-nghiem/tn-l10-nemngang-01.json` ("máy bay bay nhanh hơn thì gói rơi lâu hơn").
  `components/physics/RescueDropSimulation.tsx` + `hooks/useRescueDrop.ts` + `lib/horizontalProjectile.ts`
  (toán thuần, kiểm bằng `tmp/hero-review/thahang-check.mts`: thả đúng vạch → trúng tâm bãi đáp sai số 0 với
  **mọi** cặp h–v₀; chấm 0,1 s cách đều theo phương ngang; t = √(2h/g) không phụ thuộc v₀). Bãi đáp rộng 40 m
  và sau mỗi lượt hiện vạch "phải thả ở đây" + độ lệch — cố ý để không thành bài đo phản xạ. Không tự bay khi
  mới mở, chỉ chạy khi học sinh bấm (B4). Tab nạp chậm qua `next/dynamic` + `LazyErrorBoundary` → JS tải đầu
  trang chủ không đổi. `HarmonicPanel`/`SpringSimulation` **giữ nguyên code**, chờ nhúng vào bài Dao động
  (Giai đoạn 3). Hero còn 3 tab: Ném xiên · Thả hàng · Giao thoa. Quy tắc áp dụng: B1, B4, B8, D2, M2, M5, C1.
- **Hero có thêm tab "Giao thoa" — khay sóng hai nguồn (5/10/2026)**: mô phỏng theo đúng spec
  `content/thi-nghiem/tn-l11-giaothoa-01.json` (Bài 12 Giao thoa sóng, Vật lí 11):
  `components/physics/InterferenceSimulation.tsx` + `hooks/useInterferenceTank.ts` + `lib/interference.ts`
  (toán thuần, test được). Hai chế độ hình trên canvas 2D: **đứng yên** (vẽ bao hình biên độ — đúng cái khay
  sóng thật cho thấy vân sáng/tối đứng yên) và **"Chạy sóng"** do học sinh bấm (li độ tức thời
  u = Σaᵢ·cos(ωt − k·dᵢ), tua chậm 0,4–1,5 s mỗi chu kỳ; pha C = Σaᵢcos(k·dᵢ), S = Σaᵢsin(k·dᵢ) tính sẵn một
  lần khi đổi f/v/AB nên mỗi khung hình chỉ còn 2 phép nhân + tra bảng màu — đo được **60 khung hình/giây** ở
  375px). Vòng lặp tự dừng khi bấm Dừng, khi khay ra khỏi tầm mắt (IntersectionObserver) hoặc khi đổi tab
  (B4, không đốt pin). Học sinh chạm/kéo điểm M để tự đọc ra d₂ − d₁ = kλ (cực đại) và (k + ½)λ (cực tiểu),
  bấm **tắt nguồn B** để thấy vân biến mất; N_max/N_min khớp cả 4 hàng `so_lieu_mau` của spec (kiểm bằng
  `tmp/hero-review/interference-math.mts`); ảnh động kiểm bằng `tmp/hero-review/interference-anim.py`
  (trung bình theo thời gian trùng ảnh bao hình, tương quan **0,998** → vân đứng yên còn nước thì chạy, cột
  nút tối nhất vẫn tối). Tab nạp chậm qua `next/dynamic` + `LazyErrorBoundary`; `lib/interference.ts` chỉ được
  hai file trên import (đã grep) nên **chunk tải đầu trang chủ không đổi**. Quy tắc áp dụng: B4, D2, D4 (3 tab
  vẫn lộ hết ở 375px), M2, M4 (nói bằng chữ, không chỉ bằng màu), N7, C1, H3. Phần gắn tab trong
  `components/home/PhysicsSimulationHero.tsx` đã vào main ở commit của phiên kia (`be5bc6a76`).
- **Hero trang chủ thành mô phỏng chuyển động ném xiên (5/10/2026)**: thay con lắc lò xo mặc định bằng
  thí nghiệm kéo-thả ná cao su (`components/physics/ProjectileSimulation.tsx` + `hooks/useProjectileMotion.ts`
  + `lib/projectile.ts`), con lắc lò xo chuyển thành tab 2 và được **nạp chậm** (`HarmonicPanel.tsx` qua
  `next/dynamic`), không tự chạy khi mới mở. Học sinh tự tìm ra α = 45° cho tầm xa lớn nhất, phát hiện hai
  góc phụ nhau cho cùng tầm xa, so Trái Đất ↔ Mặt Trăng (g nhỏ 6 lần). JS tải đầu trang chủ 213 → 215 KB
  gzip (đo bằng `tmp/hero-review/firstload.mjs`). Quy tắc áp dụng: B1, B4, B8, N2, D2, D3, C1, M5.
- **Nốt 13 bài Vật lí 12 còn lại thành lý thuyết tương tác (4/10/2026)**: soạn theo skill
  `soan-bai-ly-thuyet-tuong-tac` cho toàn bộ bài học lớp 12 còn thiếu, **trừ các bài Kiểm tra và hai bài
  Thực hành đo** (Bài 4 id 5, Bài 11 id 12 — Bài 4 đã do phiên khác làm). Danh sách đã đăng DB (chỉ ghi mục
  Lý thuyết, tự sao lưu): **Bài 5 (id 6), Bài 6 (7), Bài 7 (8), Bài 8 (9)** chương Khí lí tưởng · **Bài 9
  (10), Bài 10 (11), Bài 14 (125), Bài 16 (127)** chương Từ trường · **Bài 14 hạt nhân (15), Bài 15 (16),
  Bài 16 (17), Bài 17 (18), Bài 18 (19)** chương Vật lí hạt nhân. Mỗi bài: theory.html 6 phần + 3–4 hình SVG
  tự vẽ + 2–4 file `content/thi-nghiem/tn-l12-*` + bundle.json, mỗi bài 7–8 quiz tự chấm, mục Trả bài, bài
  toán mẫu có bảng *Câu trong đề/Dữ liệu/Kiến thức* + bài điền bước trống + biến thể, thử thách ⭐–⭐⭐⭐,
  khung "Mang về". Lint sạch toàn bộ (`lint_theory` · `lint_do_dai` 2.4–2.5k từ hiện ngay · `check_quizzes` ·
  `thi_nghiem` 96 mục · `validate_bundle` ok:true) · `--kiem-tran` không mục nào tràn ngang ở 375 px.
  Cách làm: **1 bài chạy thử + 3 lô subagent song song (3+5+5 bài), mỗi bài có một subagent kiểm chéo độc lập
  rồi một subagent sửa**; ~50 lượt subagent, ~2 giờ. Mọi bài đều bị kiểm chéo bắt ít nhất 1 lỗi `chan`
  (số liệu thí nghiệm mâu thuẫn, mũi tay SVG ngược chiều, phản hồi quiz gọi tên phương án không có, số hình
  sai thứ tự); 5 bài phải sửa hai vòng (6, 7, 10, 16, 19). Quy trình + bài học đã ghi vào SKILL.md mục
  "Làm nhiều bài một đợt — thuê subagent song song". File bài nằm trong `content/lesson-samples/l12-*`;
  **`xem-thu/` (43 MB cho 13 bài) không commit** — sinh lại bằng `build_preview.py` + `chup_anh.py`.
  Log đăng: `scripts/logs/dang-13-bai-l12-*.log` (0 bài lỗi). **CHƯA deploy** — deploy xong mới lên web.
  Lưu ý: **bài 15 (id 126)** do một phiên khác đã soạn (`content/lesson-samples/l12-ung-dung-cam-ung/`) và
  đăng trước, nên **không ghi đè** (bản của phiên này ở `l12-ung-dung-cam-ung-dien-tu/`, để nguyên, chưa đăng).
  `scripts/chup_anh.py` cũng được vá: mục dài >5 000 px tự cắt thành `sec-2a/sec-2b…` (WebP có trần 16 383 px).
- **Chương 1 Vật lí 12 — nốt hai bài còn lại thành lý thuyết tương tác (4/10/2026)**: soạn theo skill
  `soan-bai-ly-thuyet-tuong-tac`, **CHƯA ghi DB** (chờ thầy duyệt + chạy trên Mac).
  (1) **Bài 3. Nội năng. Định luật 1 của nhiệt động lực học** — `content/lesson-samples/l12-noi-nang-dl1/`
  (`theory.html` 40 KB, `bundle.json`, `build_figs.py`, bản xem thử 375px). Bản cũ trên web chỉ
  460 từ và **thiếu hẳn định luật I** (item `ly_thuyet` 173, lesson 4); bản mới 6 mục: mở bài thanh chắn kim loại
  ở 5 °C, nội năng, hai cách đổi nội năng, `Q = mcΔt`, `ΔU = A + Q` với quy ước dấu, bảng số liệu đo c
  bằng bếp 500 W; 3 cái bẫy (nội năng ↔ nhiệt độ, nhiệt lượng không chứa trong vật, dấu của A), Trả bài
  6 câu, bài toán mẫu bơm xe + điền bước trống + biến thể, thử thách ⭐–⭐⭐⭐. 6 quiz, 4 thí nghiệm/ví dụ
  mới `tn-l12-noinang-01..02`.
  (2) **Bài 4. Thực hành đo nhiệt dung riêng, nhiệt nóng chảy riêng, nhiệt hoá hơi riêng** —
  `content/lesson-samples/l12-thuc-hanh-nhiet/` (44 KB + bundle + 4 hình SVG + xem thử). Bản cũ là văn SGK
  (lesson 5, item `ly_thuyet` 175); bản mới xoay sang **kỹ năng thực hành**: dụng cụ và cách suy Q = Pτ,
  đọc đồ thị t(τ) (đoạn ngang = chuyển thể), công thức `c`, `λ`, `L` kèm hai bảng số liệu thật, 3 cái bẫy
  (nhiệt kế đứng yên ≠ hết truyền nhiệt · hai cách tính c · trộn đơn vị), Trả bài 6 câu, bài toán mẫu
  nhiệt hoá hơi + điền bước + biến thể, thử thách ⭐–⭐⭐⭐. 6 quiz, 2 mục mới `tn-l12-thuchanh-01..02`.
  Lint cả hai bài: `lint_theory` OK · `check_quizzes` OK · `thi_nghiem` OK (41 mục trong `index.json`) ·
  `validate_bundle` ok:true; `lint_do_dai` **2.496** và **2.491** từ hiện ngay (~18 phút, còn 1 cảnh báo ⚠
  tổng > 2.000 mỗi bài; từng mục ≤ 467 từ). Đã soát ảnh 375px từng mục + từng hình bằng mắt (sửa 6 lỗi
  chồng nhãn) và **kiểm chéo độc lập bằng subagent** — lượt đó tìm ra 11 mục sai, đã sửa hết: 1 lỗi chết
  người (bài 4 câu 3 có **hai phương án cùng đúng** $3\ 750$ J/(kg·K)), **hướng sai số hệ thống bị viết
  ngược** (mất nhiệt ⇒ $\Delta t$ nhỏ đi ⇒ $c$ đo được **cao hơn** thật, ở 4 vị trí), bảng bài 4 trộn hai
  khối lượng (0,100 kg nhưng lấy thời gian của 0,200 kg → 838 s phải là 419 s), Hình 3 sai phần trăm
  (phải là 0,7 / 11,0 / 13,8 / 74,5%), "gần 7 lần" (thực 5,4), thiếu heading III ở bài 3, `$c = 4180$`
  trong `<text>` SVG (SVG không vẽ `<span>` của KaTeX → mất chữ), và xáo lại vị trí đáp án đúng (bài 3
  B–C–A–B–D–B, bài 4 B–A–B–B–C–B). Chi tiết + bài học quy trình: `docs/memory/project_thachlab_vl12_chuong1_ly_thuyet.md`.
  Lệnh đăng (chỉ ghi mục Lý thuyết):
  `bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/l12-noi-nang-dl1/theory.html 4` rồi
  `bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/l12-thuc-hanh-nhiet/theory.html 5`, sau đó deploy.
- **Bài 13. Sóng dừng (Vật lí 11) — bản lý thuyết tương tác (3/10/2026)**: soạn theo skill
  `soan-bai-ly-thuyet-tuong-tac` tại `content/lesson-samples/l11-song-dung/` (`theory.html` 44 KB + `bundle.json`
  + `build_figs.py` 4 hình SVG + bản xem thử 375px). 8 quiz tự chấm, 3 thí nghiệm (dây thun rung tay · đo
  λ, v bằng bảng số liệu thật · đổi sang đầu tự do), 3 cái bẫy, mục Trả bài, bài toán mẫu + điền bước trống,
  thử thách ⭐–⭐⭐⭐. Lint sạch: `lint_theory` OK · `check_quizzes` OK · `thi_nghiem` OK (4 mục mới
  `tn-l11-songdung-01..04`) · `validate_bundle` ok:true; `lint_do_dai` 2.384 từ hiện ngay (~17 phút, còn 1
  cảnh báo ⚠ tổng > 2.000 — từng mục ≤ 288 từ, đoạn liền dài nhất 205 từ). Đã kiểm chéo độc lập 8 quiz +
  5 câu đề (13/13 đáp án đúng) và sửa theo góp ý: Hình 1 (ngón bấm đúng trung điểm, vẫn 1 bó), phản hồi
  câu 6–7, số liệu đo có sai số ±0,1 m/s, xáo vị trí đáp án (A2/B2/C2/D2). **CHƯA ghi DB**, chờ thầy xem
  `content/lesson-samples/l11-song-dung/xem-thu/xem-thu.html`: `bash scripts/cap-nhat-ly-thuyet.sh
  content/lesson-samples/l11-song-dung/theory.html 32` rồi deploy. Bộ "Kiểm tra nhanh" 20 câu
  (`scripts/data/theory-quiz/32.json`) đã có trong git, validate đạt, cũng chưa đăng.
- **Bài 13. Tổng hợp và phân tích lực. Cân bằng lực (Vật lí 10, lesson 58) — bản lý thuyết tương tác (3/10/2026)**:
  soạn theo skill `soan-bai-ly-thuyet-tuong-tac` tại `content/lesson-samples/l10-tong-hop-phan-tich-luc/` (`theory.html`
  39 KB + `bundle.json` + `build_figs.py` 4 hình SVG + bản xem thử 375px). 6 mục, 7 quiz tự chấm, 3 thí nghiệm
  (`tn-l10-tonghopluc-01..03`), 3 cái bẫy, mục Trả bài (6 câu), 2 bài toán mẫu + điền bước trống + biến thể,
  thử thách ⭐–⭐⭐⭐. Lint sạch: `lint_theory` OK · `check_quizzes` OK · `thi_nghiem` OK · `validate_bundle`
  ok:true; `lint_do_dai` 2.307 từ hiện ngay (~16 phút, 1 cảnh báo ⚠ tổng > 2.000). Đã kiểm chéo độc lập
  (subagent tính lại toàn bộ): 7/7 quiz + 5 câu đề + 2 bài toán mẫu + bảng số liệu + thử thách đều ĐÚNG; sửa
  theo góp ý: Hình 4 (nhãn α đè vectơ T₂), **xáo vị trí đáp án đúng** (trước đó cả 7 quiz và 5 câu đề Luyện tập
  đều đúng ở B → nay A2/B1/C2/D2), ví dụ kẹp phôi CNC (bỏ suy luận "đối diện thì vô dụng"), định nghĩa
  $d_1, d_2$, $F_y$ của lực kéo vali, ba lực cân bằng (nói rõ đồng phẳng), mẹo kề/đối, phản hồi sai câu 1, đổi
  tên nhóm radio "Em chắc" cho khỏi trùng id phương án. **ĐÃ ĐĂNG 4/10/2026**: ghi đúng mục Lý thuyết
  (item 108, `body_html` 10.981 → 39.581 ký tự; mục Bài tập mẫu và Luyện tập giữ nguyên) bằng
  `bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/l10-tong-hop-phan-tich-luc/theory.html 58 --yes`,
  sao lưu `scripts/logs/ly-thuyet-bai58-backup-1791083195069.json`, hoàn tác
  `npx tsx scripts/khoi-phuc-ly-thuyet.mts <file sao lưu>`; đã deploy (`bash scripts/deploy.sh`). Chưa có bộ
  "Kiểm tra nhanh" 20 câu (`scripts/data/theory-quiz/58.json`).
- **Đợt tối ưu tốc độ (perf, 24–25/09)**: Lighthouse trang chủ 68→91, trang bài 78→83; `out/` 41→34 MB; ảnh 4,6 MB→0,6 MB; bỏ Google Fonts; Supabase request trang bài 10→4. Chi tiết: `perf/RESULT.md`.
- **Đợt Giai đoạn 0–1 (feat, 25/09)**: cột `difficulty` + `difficulty_source`, UI chọn mức ở Đăng đề, backfill bằng AI; nạp bundle lý thuyết lớp 12; RPC `get_lesson_mastery` / `get_chapter_mastery` + nhãn Nắm vững / Cần luyện thêm / Chưa đạt. Chi tiết: `feat/RESULT.md`.
- Hệ thống Rank/RP 7 bậc (Đồng → Cao Thủ, đổi theo bậc Liên Quân Mobile 28/9/2026 — migration đã chạy 23:47, xem `STATE-archive.md`), nhiệm vụ hằng ngày, chuỗi ngày.
- Danh vị Thách Đấu (Vô Song/Paragon) trên Cao Thủ: migration `20260926100000_rank_paragon.sql` ĐÃ chạy 26/9/2026 (rollback `perf/rollback/…rank_paragon.down.sql`); chế độ admin "Xem như học sinh" mở khoá hết (features/rank/preview.ts).
- Loại GV/admin khỏi rank RP: migration `20260926110000_rank_exclude_staff.sql` ĐÃ chạy 26/9/2026 — chặn tận gốc (3 hàm) việc tài khoản không phải role='student' bị cộng RP/lọt bảng xếp hạng khi tự test bài, đã dọn sạch dữ liệu rác (rollback `perf/rollback/20260926110000_rank_exclude_staff.down.sql`).
- Vá 2 lỗ hổng RLS tautology + `class_assessments using(true)`: migration `20260926140000_fix_rls_tautology.sql` ĐÃ chạy 26/9/2026 (rollback `perf/rollback/20260926140000_fix_rls_tautology.down.sql`).
- Sửa `find_similar_bank_questions` (quét câu trùng ở `/quan-tri/ngan-hang-cau-hoi`) bị `statement
  timeout` vì self-join O(n²) mỗi topic → nested loop dùng index GIN trigram + set_limit + cap 20
  câu giống/mỗi câu: migration `20260926150000_fix_question_bank_similarity_timeout.sql` ĐÃ chạy
  27/9/2026 (log `scripts/logs/20260927-073246-*`, rollback
  `perf/rollback/20260926150000_fix_question_bank_similarity_timeout.down.sql`). Chưa xác nhận lại
  trên UI thật là mục "Nghi trùng lặp" đã lên danh sách.
- **Bảng chào mừng theo vai (30/9/2026, PR #17, đã merge main + deploy)**: `components/account/WelcomePanel.tsx`
  gắn ở `Account()` (`app/tai-khoan/page.tsx`) — 11 tình huống (HS THPT/CTTC theo trạng thái ghi danh, GV,
  admin, trợ giảng, phụ huynh); đóng được, nhớ localStorage `thachlab_welcome_off_<userId>_<variant>`.
  Kèm gợi ý theo số liệu thật: HS THPT "Còn X RP là lên {bậc}" (X≤50) ở `ThptStudentHome.tsx`; GV THPT khối
  "Nên làm trước" ở `TeacherThptOverview.tsx`. KHÔNG thêm truy vấn Supabase, không migration. **Chưa kiểm bằng
  mắt trên web thật** từng vai. Còn lại: gợi ý số liệu cho phụ huynh/admin/CTTC (cần RPC gộp = migration mới);
  số bài tự luận chưa chấm của GV chưa có nguồn dữ liệu.
- **Trang chủ ghép 4 ý từ bản DeepSeek (1/10/2026, nhánh `claude/gracious-mayer-53030i`)**: thanh vào nhanh dưới Navbar
  (`components/home/PublicSubNav.tsx`: KHTN 9 · Lý 10/11/12 · CTTC · Xếp hạng · Phụ huynh, chỉ ở `/`); lưới 4 lớp
  kèm số chương · bài · mục + dải tổng "4 lớp · 22 chương · 116 bài · 257 mục" (`OpenClasses.tsx`, thay
  `AudienceChooser.tsx`); số đọc LÚC BUILD từ `public/data/home-stats.json` (sinh thêm trong
  `scripts/build-content.mjs`, đọc bằng `home-stats.server.ts`) — KHÔNG thêm truy vấn Supabase khi tải `/`;
  Testimonials mặc định 4 ảnh. Giữ nguyên nền tối/cyan, hero mô phỏng, HonorBoard, AboutFounder. Số liệu chỉ
  cập nhật khi deploy lại (prebuild chạy build-content).
  Sửa tiếp cùng ngày: bỏ thanh phụ (2 dòng nav xấu) → menu thả xuống dưới "THPT – THCS" ở Navbar (desktop hover/focus,
  mobile hàng chip) `components/layout/Navbar.tsx`; `/phu-huynh` khách thấy lời nhắc riêng cho phụ huynh (prop
  `guestNotice`/`loginHref`/`showSignUp` của `RequireAuth`), `/dang-nhap?next=/duong-dan` quay lại trang vừa chặn,
  phụ huynh đăng nhập mặc định về `/phu-huynh`; Footer thêm link "Phụ huynh xem kết quả của con".
- **Đồng bộ trang chương ↔ trang bài, đợt 1 (2/10/2026, PR #33, đã merge main)**: `chapterDisplayTitle` dời sang
  `features/lessons/types.ts` + thêm `chapterLabel`; cây chương trang bài hết lặp số chương và có đơn vị "bài";
  breadcrumb/link quay lại/tiêu đề ngăn kéo dùng "Chương N · Tên" (`chapterFullLabel`); trang chương đổi thanh
  tiến độ thành "x/y mục", hai nút "Tiếp tục học". Không đổi bố cục, không thêm request Supabase, không migration.
  Ảnh: `docs/anh/trang-chuong-2026-10/`. Đợt 2–4 chỉ bắt đầu sau khi PR này merge (prompt
  `docs/prompt-dong-bo-trang-chuong-2026-10.md`, prompt này chưa có trên `main`).
- **Đồng bộ trang chương ↔ trang bài, đợt 2 (2/10/2026, PR #38, đã merge main)**: tách `components/lessons/ChapterTree.tsx`
  dùng chung cho trang bài (mode `learn`) và trang chương (mode `pick`); trang chương ≥1024 dùng `.lesson-layout`
  (cột trái 272px là cây chương, cột giữa chỉ chương đang chọn, thẻ "Tiếp tục học" lên cột trái), <1024 giữ nguyên
  accordion; chọn chương ghi `?chapter=` lên URL. Đo hình học: 375/768 không đổi, 1024/1280 cột giữa bằng trang bài.
  Ảnh `dot2-*.webp` trong `docs/anh/trang-chuong-2026-10/`. Không xoá rule `.class-*` (để đợt 4). Đợt 3 làm sau khi PR này merge.

- **Rà phần Báo lỗi & Góp ý (30/9/2026, chỉ đọc code — sandbox không truy cập được bảng `bug_reports` thật)**: đã sửa 4 điểm
  không cần quyết định: (1) form chung không còn cho chọn loại `cau_hoi` (chỉ dành cho nút "Báo lỗi câu này" có gắn
  đề/câu); (2) ô chọn ảnh chỉ nhận png/jpeg/webp/heic (bucket từ chối gif/svg → trước đó báo lỗi khó hiểu); (3) ô ghi
  chú xử lý trước ghi "chỉ admin thấy" nhưng `/bao-loi-cua-toi` hiển thị cho học sinh → đổi lại nhãn cho đúng;
  (4) `BugReportsAdmin` chống kết quả tab cũ ghi đè tab mới + xoá lỗi cũ khi tải lại. Chưa deploy. Còn chờ thầy quyết:
  chống spam khách (không giới hạn), báo cho admin khi có báo lỗi mới, báo cho học sinh khi được phản hồi, đọc ~15 báo lỗi thật.

- **Đọc 31 báo lỗi thật (30/9/2026, sau khi có env)** — 22 mục còn "Mới". Phát hiện: (a) **đăng nhập Google đang TẮT** trên
  Supabase project mới (`/auth/v1/settings` → `external.google=false`; 3 báo lỗi #22/#27/#30) — khả năng mất cấu hình khi
  chuyển Singapore, thầy phải bật lại ở Dashboard; (b) **watermark "thukhoadaihoc.vn" rác trong lời giải** ~409 chỗ / 34 đề
  (chỉ trong `explanation`) — script `scripts/clean-exam-watermark.mjs` (dry-run mặc định, `--apply` có backup), CHƯA chạy;
  (c) báo lỗi #23/#24/#26/#28 chọn loại "câu hỏi" ở form chung nên không gắn được câu (đã ẩn loại này khỏi form chung);
  (d) đề 237 câu 3 mở đầu "(Tiếp câu trên)" — hỏng ngữ cảnh khi đảo thứ tự câu.
- **Xử lý đợt báo lỗi 06/10/2026 (58 báo lỗi, đóng 14 mục `da_xu_ly`)**:
  (1) Sửa câu 71 Đề 72 (Bài 8 Lớp 12): phương án B `127°C.` -> `27°C.` tránh trùng với đáp án đúng `400 K.` (giải quyết #57).
  (2) Cô lập 24 câu thiếu ảnh/đồ thị khỏi đề luyện tập & ngân hàng câu hỏi: Đề 44 (20 câu, còn 35 câu), Đề 49 (3 câu, còn 66 câu), Đề 259 (câu 21, còn 20 câu); đã sao lưu đầy đủ vào `scripts/logs/isolated-questions-backup-*.json` và đánh dấu `archived=true` trong `question_bank` (giải quyết #58, #55, #54, #44).
  (3) Mở rộng hạn mức học sinh phụ đạo (`lib/tro-giang/policy.ts` + `GhiBuoiForm.tsx`): bỏ giới hạn chặn 4 học sinh, giữ hệ số 1.4 cho từ 3 em trở lên (giải quyết #56, #49).
  (4) Chuẩn hoá câu 2 đề 474 bỏ dấu sao thừa, giải thích & đóng các báo lỗi #4, #5, #45, #47, #48, #51, #52.


- **Luyện tập: thời gian mỗi câu tăng 15s/45s → 30s/90s** (30/9/2026, theo góp ý #21 của học sinh, thầy duyệt): `SECONDS_PER_FORM`
  ở `features/exams/types.ts` + dòng mô tả ở `PracticeSession.tsx`. Chỉ tính phía client, không đổi DB. **Chưa deploy** (`bash scripts/deploy.sh`).
  Phiên đang dở đã lưu vẫn giữ tổng giờ cũ.
- **Đồng bộ trang chương ↔ trang bài, đợt 3 (2/10/2026, PR #41, đã merge main + deploy cùng ngày)**: trang chương dưới 640px có thanh đáy
  3 nút (‹ Lớp học · Tiếp tục học · Mở tất cả/Thu gọn) dùng lại CSS `.lesson-bottombar--mobile` của trang bài; thanh này
  **thay** tabbar toàn site (2 rule `:has()` ở cuối `globals.css`), chừa đáy đúng 62px như trang bài. Đợt 4 (cột giữa giàu
  thông tin + rail phải) chờ `docs/DE-XUAT-TRANG-CHUONG-2026-10.md` vào `main`.
- **Bài Mô tả sóng soạn lại + chốt phong cách soạn bài (2/10/2026, đã commit `main`)**: bản xem thử Bài 8 Mô tả sóng
  (lớp 11) ở `content/lesson-samples/l11-mo-ta-song/` (theory.html + bundle.json + 2 thí nghiệm trong
  `content/thi-nghiem/` + ảnh xem thử `xem-thu/`) — **CHƯA ghi DB, chưa deploy**, chờ thầy duyệt
  (`bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/l11-mo-ta-song/theory.html 27` rồi deploy).
  Skill `soan-bai-ly-thuyet-tuong-tac` đã cập nhật: **bỏ vai "thầy" trong bài**, checklist 14 nét dạy học Trung Quốc
  (`references/phuong-phap-day-tq.md`), thêm `scripts/build_preview.py` + `chup_anh.py` (xem thử **đúng 375 px** bằng Chrome qua CDP,
  Mac không có Playwright) + cờ `--kiem-tran` soát tràn ngang/công thức phải cuộn + `check_quizzes.py` (kiểm tự chấm không cần trình duyệt); đã sync Library plugin + `~/.codex`.
- **Độ dài bài lý thuyết — hạn mức + bộ đo (2/10/2026)**: `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md` (cơ chế bỏ cuộc,
  hạn mức, cách kiểm chứng bằng mastery) + `scripts/lint_do_dai.py` trong skill soạn bài (exit 1 khi vượt trần).
  Đo 5 bài: bài Mô tả sóng là bài dài nhất (3.021 từ hiện ngay, mục con 489 từ, đoạn liền 478 từ) → **đã cắt còn
  2.457 từ**, 3 bảng 3 cột bị bóp chữ ở 375px đưa về 2 cột. Dòng ở mục trên ("CHƯA ghi DB") là **đã cũ**: log
  `scripts/logs/ly-thuyet-bai27-backup-*.json` (22:51) cho thấy bản Mô tả sóng **đã ghi DB**; bản cắt này
  **chưa ghi DB, chưa deploy** — chờ thầy duyệt rồi chạy `bash scripts/cap-nhat-ly-thuyet.sh content/lesson-samples/l11-mo-ta-song/theory.html 27` + deploy.
  3/10/2026: cắt thêm đoạn mở bài trùng câu Dự đoán → "tới việc đầu" 165→142 từ (lint mới, xem
  `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md` mục 3); theory.html + bundle.json đã đồng bộ. **Thầy đã ghi DB 3/10/2026**
  (item 45, sao lưu `scripts/logs/ly-thuyet-bai27-backup-1790986956595.json`), deploy lại để bản tĩnh 27.json cập nhật.


- **Đã chạy 8/10/2026 23:27:** `20261008120000_rank_streak_week_theory_review.sql` — RPC `rank_my_streak_days` (dải chuỗi 7 ngày), bảng `theory_reviews`, RPC `rank_theory_review_open/submit` (RP ôn lại lý thuyết, cấu hình `theory_review_*`). Rollback: `perf/rollback/20261008120000_rank_streak_week_theory_review.down.sql`.

- **Đã chạy 11/10/2026:** `20261011120000_question_bank_lint_flags.sql` (cột `question_bank.lint_flags` + GIN, `question_content_hash` bỏ khoá `lint_ignored`); rồi `cap-nhat-lint-flags.mts --ghi` ghi 229 dòng (deQuaNgan 14, matMu 123, anhSrcTuongDoi 68, phuongAnLanDe 25), hoàn tác `--undo scripts/logs/lint-flags-1791634389029.json`. `20261010800000_an_cau_cat_cut_hien_thi.sql` (ẩn 181 câu cắt cụt, sao lưu `question_bank_cat_cut_20261010`) cũng đã chạy.


---
## Bản STATE.md trước khi rút gọn (dọn 10/10/2026)
Nguyên văn toàn bộ STATE.md lúc đó (44 KB); grep khi cần tra mục cũ.

File này là bản mô tả hiện trạng dùng chung cho mọi phiên Claude. Cập nhật sau mỗi đợt lớn.

## Hạ tầng
- Next.js App Router + TypeScript + Tailwind v4, `output: "export"` (xuất tĩnh), deploy bằng `scripts/deploy.sh` → nhánh `deploy`.
- Supabase project `jgvbdbpvjdntdgzthumv`, **region Singapore (ap-southeast-1)** — đã chuyển từ Sydney (project cũ `fxnqgmfqdbvnjawgnsfi`), thầy xác nhận xong 29/09/2026. Đã kiểm 29/09/2026 từ sandbox cloud (chỉ đọc): build học liệu tĩnh ra 4 lớp · 22 chương · 116 bài · 256 mục; dữ liệu bài không còn URL Storage của project cũ (0), 306 URL ảnh/tệp của project mới đều trả 200. Độ trễ round-trip từ VN chưa đo lại (số ~100–150 ms trong `perf*/` là của Sydney; sandbox không ở VN nên không dùng để đo).
- Công thức: **KaTeX 0.17** (không phải MathJax).
- Font tự host qua `next/font` (Be Vietnam Pro 400/600/700/800, Inter 400/500/600, JetBrains Mono 400).
- 56 route `page.tsx`, 69 trang tĩnh khi build.
- Học liệu tĩnh: `scripts/build-content.mjs` chạy ở `prebuild`, xuất `public/data/` (catalog + 116 file bài). Sửa lý thuyết phải **deploy lại** mới lên web.

## Đã hoàn thành
- **11/10/2026 — Giao diện NỀN SÁNG (trắng) là mặc định toàn site** (thầy chốt; trước đây mặc định nền tối "deep space", theme sáng chỉ là chồng `!important` nên màu bết).
  Bảng màu mới light-first trong `app/globals.css`: khối `@theme` = nền sáng, `html[data-theme="dark"]` = nền tối (nay chỉ là **tuỳ chọn**, không theo `prefers-color-scheme`); thêm token `surface-2`, `line-strong` (3,2:1 — đạt WCAG 1.4.11), `ok/warn/danger`, `primary-soft`.
  Khác biệt theo nhóm người xem: `.parent-page` nền ấm + chữ phụ 8,9:1 (AAA) + navy `#1e40af` + viền ô nhập đậm hơn; `.teacher-dashboard`/`.admin-shell` nền trung tính, mật độ cao; học sinh + trang công khai dùng mặc định.
  Đã dọn class màu nền tối/neon/gradient/quầng sáng ở ~112 file component (5 phiên con; kiểm chứng bằng `scripts/kiem-doi-mau.mts`: 100/112 file kết luận "chỉ đổi chuỗi class"); cuối `globals.css` còn **lưới an toàn** phủ nốt idiom cũ (`bg-white/5`, `border-white/10`, `bg-[#0B1020]`, `shadow-[0_0_…]`).
  Mặc định theme đổi ở `app/layout.tsx` + `components/ui/ReadingZone.tsx` + `components/layout/ThemeToggle.tsx` (snapshot SSR = light, tự cập nhật `meta theme-color`), `app/manifest.ts` + `viewport.themeColor` sang nền sáng.
  Xem thử: **`/dev/giao-dien`** (`?theme=dark`, `?aud=parent|teacher`) — bảng token + bộ dựng + 3 nhóm người xem.
  Kiểm: `npm run check:a11y` ĐẠT (0 cặp màu lỗi, 0 chỗ chữ <12px — đã nâng 4 chỗ có sẵn ở `class-num--exam`, `SoundInterferenceSimulation`, `ExamSection`, `ExamQrPanel`), `npx tsc --noEmit` sạch, ảnh 375px/1440px hai theme bằng `scripts/do-bo-cuc.mjs` (device emulation — `chrome --window-size` KHÔNG cho viewport 375px, xem `docs/MAU-NEN-SANG.md` §8), tràn ngang thật = 0.
  Tài liệu: `docs/MAU-NEN-SANG.md` (mới: bảng quy đổi idiom + việc còn treo), cập nhật `docs/UI.md` §1–2/§5 và `docs/QUY-TAC-THIET-KE.md` (thêm M7). **ĐÃ DEPLOY 10/10 13:11** (`deploy` = `9077fbd47`, build sạch từ worktree tại `main` @ `b37f7c7dc`; hosting cron kéo trong ~10 phút) — thầy chốt "cập nhật web" sau khi xem `/dev/giao-dien`. Bản deploy **không** chứa WIP untracked của phiên khác (`components/quiz-live/`, `app/tro-giang/do-vui/`, `app/(public)/choi/`) — đã kiểm lại nhánh `deploy`.
- **10/10/2026 — 25 bài lý thuyết L10 (lesson 46–48, 58–79) từ mẻ `sua-ly-thuyet` 9/10: ĐÃ GHI DB** (kiểm chéo 5 agent `kiem-code`, trần từ nới 5% cho bài 67/75/79; file = DB). **CHƯA DEPLOY** — `public/data` sinh lúc build nên web chỉ thấy sau deploy; main local đang ahead origin 11 commit (còn việc phiên khác: QR đề, HSG chấm nhanh, BTM L12), xem trước khi push. Sao lưu `scripts/logs/ly-thuyet-bai{46..79}-backup-1791605*`.
- **10/10/2026 — Mã QR cho từng đề (thầy chiếu lên bảng, học sinh quét là vào đúng đề).** Bước 1 (phía thầy):
  `components/admin/ExamQrPanel.tsx` hiện ở `/quan-tri/sua-de` (chọn đề nào là có QR) và ở `/quan-tri/dang-de`
  (hiện ngay sau khi đăng xong) — QR + link + sao chép + tải PNG + nút **“Chiếu lên bảng”** (toàn màn hình, nền
  trắng, QR lớn, mã đề lớn; Esc để đóng). QR sinh tại máy bằng `qrcode-generator` ở `lib/qr.ts`, không gọi dịch vụ
  ngoài. Bước 2 (phía học sinh): trang mới `/quet-ma` — camera quét (Android dùng `BarcodeDetector` sẵn có, iPhone
  tải chậm `jsqr` ngay lúc quét) + ô gõ số đề dự phòng; vào từ menu **“Thêm”** ở thanh đáy và nút **“Quét mã”** ở
  trang chủ HS. `RequireAuth` nay giữ `?next=` nên quét lúc chưa đăng nhập vẫn quay về đúng đề sau khi đăng nhập.
  Kiểm máy: `npx tsx scripts/kiem-qr.mts` (dựng ảnh từ `lib/qr.ts` rồi giải mã lại, 4/4 đúng), parser 15/15 ca,
  `tsc` + `eslint` sạch, `next build` ra 88 trang tĩnh. **Chưa deploy, CHƯA thử bằng điện thoại thật** (cần thầy
  chiếu thử một đề trên lớp và quét bằng cả iPhone + Android). Chưa làm: QR cho đề CNC (`CncExamComposer`) và cho
  trang đăng bài học (`LessonImporter`).
- **9/10/2026 — 6 bài lý thuyết tương tác L11 còn lại (B4, B7, B9, B10, B11, B15; id 23/26/28/29/30/34)** soạn bằng 6 agent + 6 kiểm chéo, ĐÃ GHI DB + deploy (commit `e37d29cc7`; bài 23/26/29 rỗng nên đăng bằng `upload-lesson.mts`, tạo đề 906–908; sao lưu `scripts/logs/ly-thuyet-bai{28,30,34}-backup-*`). Treo: video 4c, thầy đối chiếu SGK (xem `docs/memory/project_thachlab_l11_6_bai_con_lai.md`). L10/L11/L12 không còn bài thiếu.
- [x] **Trang chủ HS: sửa sau khi xem trên web thật** (7/10/2026 tối, commit 1fdb79a27 + 0b7eff921, đã deploy + host đã kéo):
  thẻ Rank/Chuỗi ngày hết tràn mép phải ở 375px (grid item thiếu `min-w-0`), nút Luyện nhanh một dòng, chủ đề mở khoá gập còn 3;
  thanh đáy theo vai (c86298e6f) nhận đúng phiên — trước đó render ngoài AuthProvider nên HS đã đăng nhập thấy tab "Đăng nhập"
  (`useAuthSnapshot` trong `auth-context.tsx`). Còn treo: HTML không có `Cache-Control` nên trình duyệt giữ bản cũ nhiều giờ —
  đề xuất thêm `no-cache` cho `.html`/`.txt` vào `.htaccess` trong `scripts/deploy.sh`, chờ thầy gật.
- [x] **Trang chủ HS gọn lại** (7/10/2026, commit 273585178 + 4cd492776): một thẻ "Hôm nay em làm gì" (`TodayCard`), một khối
  Phụ đạo chỉ hiện khi có việc (`TutoringSection`), bù bài bỏ danh sách buổi, rank gọn; `ClassRankBoard` + `HonorVisibilityPicker`
  sang `/lop-hoc/xep-hang`; xoá `NextStepsCard`, `TitleShowcase`. **Chưa chụp 375px bằng tài khoản HS** — thầy xem thật sau deploy
  (ghi chú ở phụ lục B1 `docs/QUY-TAC-THIET-KE.md`).
- (Các mục hoàn thành trước 7/10/2026 đã chuyển sang `docs/STATE-archive.md`, mục cuối file; grep khi cần.)
- **Tách JS theo vai (6/10/2026, nhánh `perf-tach-js`, CHƯA vào main/CHƯA deploy)** — 3 commit `2cd436588`, `00e5ba526`, `669f7be9f`. JS đầu (KB thô, chunks-report): `/tai-khoan` 1468→973, `/phu-huynh` 1174→989, `/lop-hoc/bai` 1107→1092 (chưa <1000: QuestionCard còn dùng chung WorkedQuestionsGrid), `/kiem-tra/lam` 1045→1046 (không đổi). Chưa kiểm bằng đăng nhập thật (HS THPT/CNC, GV, PH) và chưa làm thực nghiệm xoá-chunk A6. Spec: `docs/BAN-GIAO-PERF-TACH-JS-2026-10-06.md`.

## Credit $100 Anthropic API — ĐANG CHỜ thầy chạy (hết hạn 22/10/2026)
- Credit chỉ áp dụng API/Batch/Agent SDK, không áp dụng Claude Code. Script mới `scripts/batch-ra-soat-bai.mts` (8/10/2026): Batch API,
  Claude rà từng bài lý thuyết như "lượt Claude" (bước 1b skill cap-nhat-bai-hoc-theo-gemini). Cần `ANTHROPIC_API_KEY` trong `.env.local`.
  Thứ tự: `--du-toan` (miễn phí) → `--gui --lesson-ids 10` (thử 1 bài, xem `scripts/logs/batch-ra-soat/ket-qua/10.json`) → `--gui` cả kho →
  `--nhan --cho` → đọc `scripts/logs/batch-ra-soat/BAO-CAO.md`, chọn bài sửa theo chế độ 2 của skill.
  Chế độ 2: `--che-do bai-tap-mau --gui --lesson-ids <id>` → nháp 4 dạng bài tập mẫu bắc cầu bám lý thuyết + YCCĐ, tự kiểm máy, báo cáo `BAO-CAO-BAI-TAP-MAU.md`; viết lại theo skill soan-bai-tap-mau trước khi đăng. Chi tiết: memory `project_thachlab_anthropic_credit.md`.

- 8/10 chiều: key đã vào .env.local (workspace Default), batch chạy thật. Bài 10 lý thuyết + BTM đã đăng. Đang chạy: rà 20 bài L12 + nháp BTM 18 bài L12. Chế độ mới `sua-ly-thuyet` (API tự sửa HTML, máy build/lint) chưa chạy thật. Thầy chốt: Claude tự chốt góp ý và đăng, trợ giảng rà trên web, Gemini bỏ khỏi đường chính.

- **8/10 tối — mẻ `sua-ly-thuyet` 20 bài L12 tưởng mất, đã tìm lại trong `stash@{0}`.** Batch ghi thẳng vào `theory.src.html` trong working tree lúc 8/10 13:04 nhưng KHÔNG commit; 22:44 cùng ngày một bước dọn cây (`git stash` rồi `reset` để pull) đã cất chúng vào `stash@{0}` và trả cây về bản trước khi sửa. Hệ quả cần nhớ: DB của bài **4, 14, 15, 17, 18, 125, 126** đang là bản ĐÃ SỬA (đăng 8/10 13:20) còn file trong repo là bản cũ → đăng lại từ repo sẽ LÙI nội dung (dùng `so-file-voi-db.mts` để thấy).
- **8/10 khuya — xong nốt 16 bài L12 cùng mẻ `sua-ly-thuyet`** (lesson 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 125, 126, 127): khôi phục `theory.src.html` (+ `build_figs.py` khi bản rà dùng mốc FIG khác) từ `stash@{2}`, build lại, soát vật lí độc lập từng bài, cắt còn 1.753–2.446 từ hiện ngay (trần 2.500), `lint_theory` + `lint_do_dai` + `check_quizzes` + `validate_bundle` sạch, đăng lý thuyết (16 item) rồi deploy; `npx tsx scripts/so-file-voi-db.mts` xác nhận file = DB cho cả 16. Sửa đáng kể: bài 11 phải lấy ĐÚNG bản rà trong `stash@{2}` (cây đang giữ bản 6/10 cũ), bài 126 sửa cơ chế bếp từ (nhôm không tập trung từ trường) + đồng bộ `build_bundle.py`, bài 7 sửa nhãn Hình 2 sang so cùng $p$ (Charles), bài 127 bỏ 2 dòng lộ đáp án trước hộp Dự đoán (V7). **Cả 20 bài của mẻ `sua-ly-thuyet` L12 đã xong.**
- **9/10 — Lớp 12 lý thuyết tương tác: ĐỦ 20/20 bài** (`so-file-voi-db.mts`: 20 bài khớp DB). Đã đẩy nốt bản sửa bếp từ bài 126 (commit 00e00432c) lên DB item #145 (sao lưu `scripts/logs/ly-thuyet-bai126-backup-1791532108342.json`) + deploy. Không còn bài L12 nào cần soạn; không thuê agent.
- **Đã xử lý chương 1 L12 (Bài 1–4, lesson 2–5):** khôi phục `git show stash@{0}:content/lesson-samples/<bài>/theory.src.html` → build lại → soát vật lí độc lập (4 subagent: sửa 3 chỗ phản hồi quiz/định nghĩa λ ở bài 3, sửa định nghĩa nhiệt năng + dòng 🔑 ở bài 2, sửa chú thích Hình 2 ở bài 4 thực hành, đồng bộ với "nội năng = động năng + thế năng" của bài 3) → cắt còn **2.434 / 2.445 / 2.484 / 2.436** từ hiện ngay (trần 2.500) → `lint_theory` + `lint_do_dai` + `check_quizzes` + `validate_bundle` sạch, 375px không tràn ngang → đăng lý thuyết cả 4 bài (bài 3 đăng lại vì soát vật lí sửa 3 chỗ) + deploy; `npx tsx scripts/so-file-voi-db.mts` xác nhận **file = DB** cho cả 4. **15 bài còn lại CHƯA khôi phục** (cùng mẻ, cùng cách làm). Quy tắc mới ở `AGENTS.md`: batch ghi nguồn xong phải commit ngay, đừng để uncommitted rồi `stash`/`reset`.
- **Đã xử lý chương 1 L12 (Bài 1–4, lesson 2–5):** khôi phục `git show stash@{0}:content/lesson-samples/<bài>/theory.src.html` → build lại → soát vật lí độc lập (4 subagent: sửa 3 chỗ phản hồi quiz/định nghĩa λ ở bài 3, sửa định nghĩa nhiệt năng + dòng 🔑 ở bài 2, sửa chú thích Hình 2 ở bài 4 thực hành, đồng bộ với "nội năng = động năng + thế năng" của bài 3) → cắt còn **2.434 / 2.445 / 2.484 / 2.436** từ hiện ngay (trần 2.500) → `lint_theory` + `lint_do_dai` + `check_quizzes` + `validate_bundle` sạch, 375px không tràn ngang → đăng lý thuyết cả 4 bài (bài 3 đăng lại vì soát vật lí sửa 3 chỗ) + deploy; `npx tsx scripts/so-file-voi-db.mts` xác nhận **file = DB** cho cả 4. **16 bài còn lại CHƯA khôi phục** (cùng mẻ, cùng cách làm): lesson 6, 7, 8, 9 (chương 2) · 11, 12, 13, 14, 125, 126, 127 (chương 3; bài 11 giữ được bản sửa trong cây nhưng chưa đăng) · 15, 16, 17, 18, 19 (chương 4). Quy tắc mới ở `AGENTS.md`: batch ghi nguồn xong phải commit ngay, đừng để uncommitted rồi `stash`/`reset`.
- **Cảnh báo trùng slug lesson 126:** hai thư mục cùng trỏ lesson 126 — `content/lesson-samples/l12-ung-dung-cam-ung-dien-tu/` (đúng, vừa đăng 8/10) và `content/lesson-samples/l12-ung-dung-cam-ung/` (bản cũ, lệch 4.198 ký tự). Đăng từ thư mục cũ sẽ LÙI bài 126 (`so-file-voi-db.mts` in ra cả hai dòng). Nên xoá/đổi tên thư mục cũ khi rảnh.
- **Cảnh báo lặp lại:** đúng lúc phiên này đang làm (23:18 và 23:24), một tiến trình khác trong cùng repo lại `git stash` + `git reset` để dọn cây → việc chưa commit bị nuốt lần hai. Đã cứu từ `stash@{0}` mới rồi commit qua worktree riêng và push thẳng `origin/main` (`7c0ea1254`) vì cây chính đang ở giữa một merge của phiên khác. Phiên nào chạy song song trên Mac: **đừng** dọn cây bằng `stash` + `reset`; muốn cây sạch thì tạo worktree/nhánh riêng.

## Migration — ĐANG CHỜ


- **Gửi trợ giảng xem trước (11/10/2026):** `20261011100000_exam_ta_preview.sql` CHƯA chạy (bảng `exam_ta_previews` + RLS, 1 policy SELECT `exams` cho TA đọc đề đã gửi dù còn ẩn) → `bash scripts/run-migrations.sh`; rollback `perf/rollback/20261011100000_exam_ta_preview.down.sql`. UI: panel "Gửi trợ giảng xem trước" ở /quan-tri/dang-de + /quan-tri/sua-de; TA làm ở `/tro-giang/xem-truoc` (đáp án hiện ngay mỗi câu) rồi sang `/tro-giang/chua-bai`. Chưa thử trên máy thật.

- **Lớp "Học sinh giỏi & Chuyên Vật lý 9" duyệt tay (10/10/2026):** `20261010600000_lop_hsg_vat_ly_9_duyet_tay.sql` CHƯA chạy (thêm lớp slug `hsg-vat-ly-9` + cột `classes.requires_approval` + sửa 2 policy `user_classes`) → `bash scripts/run-migrations.sh` TRƯỚC khi deploy. Học sinh chọn ở `/dang-ky`, thầy duyệt ở /quan-tri học sinh → tab chờ duyệt. Chưa chặn nội dung HSG theo lớp này (nội dung nằm trong lớp KHTN 9).

- **Chấm nhanh HSG 9 (10/10/2026):** `20261010300000_hsg_cham_nhanh.sql` ĐÃ CÓ trên DB (bảng + 1 Pre-test; chạy lại báo policy tồn tại) (2 bảng hsg_grade_* + seed Pre-test) → `bash scripts/run-migrations.sh`; Edge Function `hsg-ai-grade` CHƯA deploy (cần secret DEEPSEEK_API_KEY và/hoặc ANTHROPIC_API_KEY); trang `/quan-tri/hsg-cham-bai`.
- **HSG KHTN 9 đợt 1 (10/10/2026): XONG (kiểm DB 13:20 — 4 bài 154/155/160/162 đã có mục lý thuyết + bài tập mẫu có nội dung, đã Hiện; migration 20261010200000 không cần chạy).** Ghi chú cũ: `20261010200000_hsg9_dot1_muc_noi_dung.sql` CHƯA chạy (tạo mục cho CĐ00/10/11/13 = bài 160/155/154/162, bật Hiện 160) → `bash scripts/run-migrations.sh`; rồi `bash scripts/dang-hsg9-dot1.sh` (ghi lý thuyết + bài tập mẫu 4 CĐ), rồi deploy. Nội dung: `content/hsg9/cd{00,10,11,13}-*/`, `scripts/data/bai-tap-mau/{154,155,160,162}.json`. (Migration `20261010100000` thực tế ĐÃ chạy.)
- **Khoá Vật lí HSG & chuyên (10/10/2026):** `20261010100000_khoa_hsg9_vat_ly_khung.sql` CHƯA chạy — thêm môn `hsg-vat-ly` + 6 chương + 17 bài (ẩn) vào KHTN 9, mục rỗng cho CĐ01/CĐ02; cuối log in `lesson_id`. Nội dung CĐ01/02: `content/hsg9/`; bản đồ: `docs/HSG9-KHUNG.md`.
- **Trang chủ HS bản thích ứng (9/10/2026, nhánh claude/zealous-cori-27xlz3):** migration `20261009100000_notify_exam_assigned.sql` CHƯA chạy — `bash scripts/run-migrations.sh` (giờ nào cũng được; rollback `perf/rollback/20261009100000_notify_exam_assigned.down.sql`). Trang chủ HS không còn bài/BTVN giao chung; **phải chạy file này TRƯỚC khi deploy**, nếu không học sinh không còn chỗ nào thấy bài kiểm tra mới giao (trang `/kiem-tra` vẫn liệt kê đề). Đổi theo mẫu thầy duyệt: khung chào gộp chuỗi ngày + RP còn thiếu + "tiến bộ so với tuần trước"; thẻ Hôm nay có luyện kỹ năng yếu (nút luyện nhanh 10 câu); hàng "Dành cho em" ở `/luyen-tap`; ô tìm bài ở `/lop-hoc`; bỏ đồng hồ ở bước đọc lý thuyết thoát phụ đạo (máy chủ vẫn đòi đủ thời gian). Chưa chụp 375px bằng tài khoản HS.
- **Báo RP thưởng (10/10/2026):** `20261010500000_notify_rp_thuong.sql` CHƯA chạy → `bash scripts/run-migrations.sh` (giờ nào cũng được; rollback `perf/rollback/20261010500000_notify_rp_thuong.down.sql`). Trigger trên `rank_rp_ledger`: chuông "+N RP" cho mục tiêu tuần / tiến bộ tuần / mục tiêu cả lớp; bài về nhà vốn đã có chuông "+N RP" (homework_check_set), không thêm.
- **ĐÃ CHẠY + DEPLOY 10/10/2026 13:08–13:12:** `20261010400000` (chặn thưởng), `20261010410000` (thu hồi 4.350 RP/79 dòng: 52 em giảm 90→30, 5 em mục tiêu tuần về 0, 13 em tiến bộ về 0; sao lưu `rank_rp_awards_backup_20261010`), `20261010420000` (mức RP lý thuyết 15/45/100, ôn 5×3), cùng `20261009180000` (ẩn 599 câu đề hỏng), `20261009100000` (chuông báo bài giao). UI lý thuyết (dòng luật + lượt ôn) đã deploy `b37f7c7dc`; còn thiếu: chụp 375px bằng tài khoản HS, thử nộp thật 1 bài, xem em nào tụt bậc.
- **Chặn thưởng quá cao (10/10/2026):** `20261010400000_rank_chan_thuong_qua_cao.sql` CHƯA chạy → `bash scripts/run-migrations.sh` (giờ nào cũng được; rollback `perf/rollback/20261010400000_*.down.sql`). Nguyên nhân ca 4,5 điểm = 90 RP: mùa 4 có `weekly_goal_rp=90` + mục tiêu riêng tụt sàn 4 điểm + tiến bộ tuần từ mốc rất thấp. RP đã cộng KHÔNG bị sửa (thầy quyết có thu hồi không).
- **RP lý thuyết (10/10/2026, commit 6ce301576):** UI `components/lessons/TheoryRpBar.tsx` đã gọi `rank_theory_open/submit` (chưa gọi `rank_theory_review_*`). CHƯA có khoá: chạy `npx tsx scripts/sinh-khoa-quiz-ly-thuyet.mts` (xem thử) rồi `--ghi` trên Mac; chưa chụp 375px bằng tài khoản HS.
- **Trang chủ HS + RP ôn lại (8/10/2026):** migration `20261008120000` ĐÃ CHẠY 23:27 (xem STATE-archive.md). **Còn thiếu:** UI gọi `rank_theory_open/submit` + `rank_theory_review_*` và dòng khoá `theory_quiz_keys` cho từng bài — chưa bài nào có nên chưa cộng RP lý thuyết cho ai. Chưa chụp 375px pop-up/dải 7 ngày bằng tài khoản HS.
- **Bài 11 VL12 Thực hành cảm ứng từ (7/10/2026, commit a04812d1c):** CHƯA ghi DB — `upload-lesson.mts content/lesson-samples/l12-thuc-hanh-cam-ung-tu/bundle.json --lesson 12 --mode replace`; 4 bài L12 đã sửa đường sức nét đứt chờ `cap-nhat-ly-thuyet-hang-loat.sh l12-luc-tu-cam-ung-tu:11 l12-khai-niem-tu-truong:10 l12-cam-ung-dien-tu:13 l12-dong-dien-xoay-chieu:14`; sau đó deploy (CSS `.tl-sim` mới). Clip mở bài/hộp đo chưa xác nhận mốc cắt bằng mắt.
- **Sách in Chương 2 lớp 10 — bản v6 (7/10/2026, 123 trang, commit book/):** dùng TRÊN LỚP; Dạng chung nhất có ô lời giải, Luyện thêm chỉ đề, ⏱ 1′, vạch chia tiết, bảng đáp án thuần 2 trang cuối. **Chờ thầy chỉnh (đang là MẶC ĐỊNH):** `book/src/dang-chung.json` (Dạng 1–2 mỗi bài) và `book/src/tiet.json` (tiết 1 hết mục II, tiết 2 hết Bài tập mẫu). **Web đáp án:** `public/sach-data/*.json` bản v6 CHƯA commit/deploy (bản v5 đang chạy, số thứ tự trùng nên QR vẫn đúng); trang `/sach/dap-an` chưa kiểm lại sau v6 → kiểm rồi mới commit + deploy. Chưa in thử giấy thật. Chi tiết: `docs/memory/project_thachlab_sach_in_chuong2.md`, skill `.claude/skills/sach-in-tu-web/SKILL.md`.
- **Đã đăng 7/10/2026:** hình 1 bài Chuyển động ném L10 có mô phỏng (commit e568477ec) ghi vào lesson 57 bằng `cap-nhat-ly-thuyet.sh`; chưa xem trên web thật.

- **Đã chạy 7/10/2026:** `20261007070000_rls_backup_tables.sql` — bật RLS + revoke anon trên 7 bảng sao lưu (Supabase báo CRITICAL `rls_disabled_in_public` 3/10). Chạy tay thêm `revoke all on question_bank_grade_fix_20261005 from anon, authenticated` (bảng này đã có RLS, chỉ thu quyền). Kiểm lại: 0 bảng `*_backup_*`/`*_fix_*` thiếu RLS. Rollback ở cuối file.
- **Đã chạy 6/10/2026 23:14 (xác nhận 7/10 qua log):** `20261006180000_similar_bank_questions.sql` — RPC `get_similar_bank_questions(p_topic_id, p_form, p_exclude_ids, p_limit)` SECURITY DEFINER cho HS đã đăng nhập lấy câu tương tự (chủ đề + con 1 tầng, ưu tiên cùng Dạng, loại essay, ≤10 câu). **Trả cả đáp án** — chỉ dùng cho bài luyện tự chấm. Kèm index `idx_question_bank_topic_form_active`. Rollback ở cuối file.
- **Đã chạy 6/10/2026:** `20261005140000_weakest_topics.sql` — RPC `get_my_weakest_topics` cho thẻ "3 kỹ năng yếu nhất" (`WeakestSkillsCard`, trang chủ HS `/tai-khoan`). Thẻ tự ẩn khi RPC chưa có. Rollback ở cuối file.
- **Đã chạy 5–6/10/2026 (xác nhận 7/10 qua log):** `20261005100000_bank_grade_lop10.sql` — gắn `grade='10'` cho 6.262 câu `question_bank` (277 đề lớp 10, grade đang rỗng). Rollback ở cuối file. Sau đó còn ~10,5k câu chưa có mức độ → `backfill-question-bank-difficulty.mts`.
- **Đã ghi DB 9/10/2026 (audit đáp án ngân hàng):** `fix-bank-answers.mts --apply` ghi 171 câu `db_sai` hai lượt đồng thuận (mẫu 24 câu: 12/12 máy đúng). Lỗi kiểu dữ liệu do chép mục `_can_xac_nhan` (mc lưu chữ cái, short lưu số, tf lưu chuỗi) đã sửa bằng `repair-bank-answer-types.mts` (80 câu, sao lưu `scripts/logs/repair-types-backup-*.json`). Còn chờ thầy duyệt: 127 câu trong `_can_xac_nhan` của `scripts/data/bank-answer-fixes.json`; 590 `db_dung` không làm gì; 8 `khong_ro` + 2 `cho_phan_xu` xem tay.
- **Đã chạy 9/10/2026 20:04:** `20261009180000_an_cau_de_hong_audit.sql` — ẩn 599 câu `question_bank` bị audit đáp án AI gắn `de_hong` (id ở `scripts/data/audit-de-hong-ids.json`); có bảng sao lưu, rollback ở cuối file. Còn lại sau audit: 656 `db_sai` đã thu hẹp: 556 câu hai lượt cùng đề xuất một đáp án khác DB, 100 câu bất đồng, file `scripts/logs/db-sai-can-duyet.csv` chờ thầy duyệt, 8 `khong_ro` + 2 `cho_phan_xu` xem tay; 590 `db_dung` không làm gì.
- **Chờ chạy:** `20261006130000_gan_lai_chu_de_5_de_l11.sql` — gắn lại chủ đề cho 129 câu lớp 11 của 5 đề 638/639/658/693/701 (trước đó dính chủ đề lớp 10 như Newton, Hooke). 11 câu ngoài chương trình lớp 11 mới (7 điện xoay chiều lớp 12, bán dẫn, chất khí, điện phân) để trống chủ đề, thầy xử lý riêng. Chạy sau `fix_grade_ngan_hang_5_de_l11`. Trigger tự đồng bộ nhãn sang `exams.questions`.
- **Chờ chạy:** `20261006120000_fix_grade_ngan_hang_5_de_l11.sql` — đổi `grade` 10→11 cho 129 câu `question_bank` thuộc 5 đề lớp 11 (638, 639, 658, 693, 701) bị gắn nhầm. Phát hiện bằng `scripts/audit-lech-lop-ngan-hang.mts`. Rollback ở cuối file. Còn ~190 câu lệch kiểu 9→12, 10→12, 11→12, 9→11 chưa sửa (xem log `scripts/logs/lech-lop-*.csv`, cần xem tay).
- **Đã chạy 6/10/2026:** `20261005140000_weakest_topics.sql` — RPC `get_my_weakest_topics` cho thẻ "3 kỹ năng yếu nhất" (`WeakestSkillsCard`, trang chủ HS `/tai-khoan`). Thẻ tự ẩn khi RPC chưa có. Rollback ở cuối file.
- **Chờ chạy:** `20261006150000_quiz_live.sql` — Đố vui lớp học (4 bảng `quiz_*`, RPC `quiz_join/state/answer` cho học sinh ẩn danh, `quiz_host_*` cho thầy/trợ giảng, `quiz_bank_search`, `quiz_set_to_bank`). Rollback: `perf/rollback/20261006150000_quiz_live.down.sql`. Giao diện: học sinh `/choi` (PIN, không đăng nhập), thầy/TA `/tro-giang/do-vui` (soạn bộ câu: gõ/dán/ngân hàng; đưa câu tự gõ vào ngân hàng), chiếu lớp `/tro-giang/do-vui/phong?id=`. SQL mới kiểm cú pháp bằng pglast, CHƯA chạy thật → sau migration phải thử 1 vòng với 2 điện thoại. Đọc trạng thái bằng polling 1–2 s (không dùng Realtime).
- **Chờ chạy:** `20261005100000_bank_grade_lop10.sql` — gắn `grade='10'` cho 6.262 câu `question_bank` (277 đề lớp 10, grade đang rỗng). Rollback ở cuối file. Sau đó còn ~10,5k câu chưa có mức độ → `backfill-question-bank-difficulty.mts`.
- **Migration đã chạy 6/10/2026; còn việc tay (VAPID, deploy, cron):** `20261005160000_push_subscriptions.sql` — bảng `push_subscriptions` + RPC `upsert_my_push_subscription`, `claim_push_reminders_due` (M4 nhắc Web Push). Rollback: `perf/rollback/20261005160000_push_subscriptions.down.sql`. Kèm việc tay: VAPID secrets + deploy `send-daily-push` + lịch cron, xem `docs/PUSH-NHAC-HANG-NGAY.md`.
- (Không còn migration chờ — 5/10/2026. Các file 20260930160000…20261003150000 đã chạy, xem `STATE-archive.md`. `FILES` trong `scripts/run-migrations.sh` đang rỗng.)
- Đã chạy: `20260930160000_exit_quiz_bank_children.sql` 30/9/2026 17:15 (xem STATE-archive.md). Đợt GĐ 1b (5 file `20260930110000`–`150000`) đã chạy 30/9/2026 16:07 (xem STATE-archive.md).
  Đã cấp bù thành tích `tien_bo_tuan` cho 7 em từng nhận RP tiến bộ (30/9/2026, chạy tay, kiểm lại = 0 em thiếu).
- **Bộ Kiểm tra nhanh lý thuyết lớp 12 — ĐÃ ĐĂNG 5/10/2026** (20 bài, lesson 2–11, 13–19, 125–127): soạn lại theo bài tương tác 6 đoạn, đăng bằng `publish-theory-quiz.mts --replace` → exam 751–770, đã `deploy.sh`.
  Còn treo: đề cũ 209, 239–257 vẫn nằm trong DB (script không xoá) — kiểm `exam_results` rồi dọn tay. Bài 9/17/126 còn 18–19 câu (đã loại câu sai).
  Lỗi nội dung bài phát hiện khi kiểm chéo, chưa sửa: bài 8 `summary_html` (273 K ↔ 24,79 lít phải 298 K); bài 19 Xofigo `^{223}_{86}Ra` phải Z=88; bài 10 "d gấp đôi → B còn 1/8" chỉ đúng lần 2→4 cm; bài 126 mục tiêu ghi 8 câu thực tế 7; bài 13 còn vai "Thầy". Skill `soan-quiz-ly-thuyet` cần đồng bộ 2 bản còn lại: `bash scripts/sync-skill.sh`.
Mọi file trong `supabase/migrations/` tính tới 30/09/2026 đã chạy trên production.
Lịch sử các đợt đã chạy: `docs/STATE-archive.md`. Sơ đồ bảng hiện tại: `docs/DATABASE.md`
(sinh lại bằng `node scripts/gen-database-doc.mjs` sau mỗi đợt migration).

## Việc tay còn lại
- **5 bài lý thuyết tương tác Chương 4 Vật lí 11 (id 41–45) — thầy duyệt + ĐÃ GHI DB + deploy 5/10/2026 (sao lưu `scripts/logs/ly-thuyet-bai4{1..5}-backup-*.json`); web thật đã kiểm 12:57 5/10: 5/5 bài có quiz tương tác**: `content/lesson-samples/l11-{cuong-do-dong-dien,dien-tro-dinh-luat-ohm,nguon-dien,nang-luong-cong-suat-dien,thuc-hanh-do-sdd-pin}/` (mỗi bài 2 vòng kiểm chéo sạch, xem thử `xem-thu/xem-thu.html` trong thư mục bài). Đăng: `bash scripts/cap-nhat-ly-thuyet.sh <thư-mục>/theory.html <id> --yes` ×5 rồi deploy 1 lần. Chờ thầy chốt: α đồng bài 23 dùng 3,9·10⁻³ K⁻¹ (SGK 4,3). Chi tiết: `docs/memory/project_thachlab_l11_chuong4_ly_thuyet.md`.
- **Rank — thi thăng hạng thích ứng + luyện từng câu (giao Sonnet 3/10/2026)**: spec `docs/BAN-GIAO-RANK-THI-THANG-HANG-2026-10-03.md`; migration dự kiến `20261003100000_rank_gate_adaptive.sql` + `20261003110000_rank_rp_first_attempt.sql` (chưa viết lúc ghi dòng này). Việc tay ngay: gắn `challenge_exam_id` cho cao_thu/thach_dau season 4 ở `/quan-tri/xep-hang` (3 em đang kẹt Đại Sư); mùa 2 cân nhắc `practice_max_rp 30`, `weekly_goal_rp 40`.
- [x] **Trang bài học: 6 mục thu gọn thành danh sách + Tóm tắt ý chính cần thuộc**
  (27/9/2026) — `app/lop-hoc/bai/page.tsx`: cả 6 mục (Lý thuyết/Video/Bài tập mẫu/
  Luyện tập/BTVN/Kiểm tra) giờ hiện dạng danh sách thu gọn, bấm mục nào xổ mục đó
  (mặc định đóng hết, trừ khi có link "Ôn ngay" hoặc "Tiếp tục học" trỏ thẳng vào 1
  mục thì tự mở mục đó). Mỗi mục lý thuyết có thêm khối "📌 Tóm tắt ý chính cần
  thuộc" (nếu có `summary_html`) — tự thu gọn riêng, độc lập với nội dung đầy đủ.
  Code đã deploy 27/9, backfill 81/81 mục xong, đã deploy lại — **đã lên web thật**,
  chưa tự kiểm bằng mắt trên trình duyệt thật.
  ở đâu cả vì `summary_html` chưa có dữ liệu**, chờ backfill (mục trên) rồi deploy lại.
- [x] **Backfill RP cho Kiểm tra lớp 10/11/12** (27/9/2026) — thầy đã chạy
  `docs/supabase-recompute-rank-backfill-20260927.sql`. exam 224/12/205/206/219 đã lên RP đầy đủ (trong
  khung mùa). exam 23 (lớp 10) và exam 9 (lớp 12) vẫn 0 RP vì toàn bộ lượt làm nằm TRƯỚC ngày mở mùa
  (season 5 mở 26/9, season 4 mở 21/9) — `rank_recompute_student` chỉ tính trong khung `starts_on..ends_on`,
  đây là thiết kế đúng, không phải lỗi. exam 214 chỉ có 1 lượt của tài khoản admin Thạch, bị loại đúng
  theo rank_exclude_staff.
- [ ] **Backfill mức độ câu hỏi** — còn ~3541/7223 câu `question_bank.difficulty` rỗng.
  Script **ghi thật ngay, không có dry-run**; tham số chỉ giới hạn số câu:
  `npx tsx scripts/backfill-question-bank-difficulty.mts 20` (thử nhỏ, xem lại
  `/quan-tri/ngan-hang-cau-hoi`, rồi chạy không giới hạn). Tốn API Anthropic (~90 lô × 40 câu).
- [x] **Kiểm hồi quy bằng tài khoản thật** (26/9/2026) — tạo 3 tài khoản test throwaway (student/
  instructor/admin, gán lớp 12) trên local dev server cô lập (git worktree riêng, port 3010, không
  đụng dev server phiên khác), 3 agent song song đăng nhập 3 vai + tự kiểm tay lại vai HS 1 lần
  riêng lẻ. Kết quả: HS làm đề 96 (nộp + chấm điểm đúng) + trang Rank, GV xem gradebook (208 lượt
  làm lớp 12) + phụ đạo (46 HS cần phụ đạo) + phân tích/cảnh báo, admin vào `/quan-tri/dang-de`
  (dropdown Lớp→Chương nạp đúng dữ liệu) + trang CNC `/quan-tri/cnc-bai-hoc` — **tất cả PASS, không
  phát hiện lỗi do AuthProvider mới**. Tài khoản test + dữ liệu liên quan đã xoá sạch sau khi xong.
  Ghi chú phụ (không phải lỗi AuthProvider): 3 agent chạy song song trên cùng origin bị đá phiên
  chéo nhau do Supabase dùng chung `localStorage` theo origin — xác nhận lại bằng cách chạy 1 mình
  thì không xảy ra. Phát hiện thêm (đã tách việc riêng): nút đáp án trong ExamRunner có thể re-render
  quá thường xuyên do đồng hồ đếm ngược, đáng xem lại hiệu năng (không phải lỗi chức năng).
- [x] **Đo lại PageSpeed trên site thật** (26/9/2026) — desktop **100**; mobile **74**; CrUX field
  (người dùng thật, 28 ngày) **LCP 2,7s → Core Web Vitals Failed** (ngưỡng đạt 2,5s, thiếu 0,2s),
  INP 172ms, CLS 0,07, TTFB 0,7s. Lighthouse lab mobile: LCP 5,5s, FCP 2,4s, **TBT chỉ 40ms**.
  Chẩn đoán (đo bằng Chrome trên production): brotli ĐÃ bật và chạy đúng; nghẽn nằm ở **font** —
  trang chủ tải **20 file woff2 = 323 KB**, và woff2 nén sẵn nên brotli không giúp gì. 15 file font
  được preload nằm ở request #2–#16, hai file CSS mãi #17–#18, tức font giành băng thông của CSS
  trước lúc vẽ trang. So sánh: JS 856 KB → ~250 KB sau brotli, CSS 280 KB → ~45 KB.
  → Đợt xử lý: `docs/prompt-toi-uu-font.md` — **ĐÃ XONG + deploy 26/9/2026** (commit `11aed966`).
  Cinzel/Playfair (tên bậc rank) tách khỏi root layout, chỉ trang có component rank mới tải;
  JetBrains Mono bỏ preload. Trang chủ: 20 file/323 KB → 17 file/262 KB (chưa đạt mục tiêu
  <10 file/<170 KB — phần còn lại là ký tự thật, không bỏ được mà không đổi giao diện). Lighthouse
  mobile trang chủ 80→92 điểm (đo lab, kiểm độc lập). Chi tiết: `perf3/RESULT.md`. Đã push nhánh
  `deploy`, hosting cập nhật trong ~10 phút — **chờ đo lại PageSpeed trên site thật**.
- **Đợt tối ưu tải số 4 (split-js5 + cache ảnh, 27/9/2026)** — **ĐÃ XONG + verify độc lập +
  deploy** (commit `f068cf95`, kiểm bởi phiên riêng: `perf4/BASELINE.md` + `perf4/RESULT.md`).
  Lần 1 (`6e9d07b3` perf/split-js4) tách JS `ExamRunner`/`PracticeSession`/`LessonMasteryCard`
  bị **revert** (`063a97a4`) vì crash trắng; sau khi có lưới an toàn `app/error.tsx` +
  `LazyErrorBoundary` (`9d22e14c`) mới làm lại an toàn (`f068cf95`), mỗi chunk mới bọc riêng
  `LazyErrorBoundary` cục bộ. Cộng thêm: cache header `Cache-Control` tường minh cho ảnh trong
  `scripts/deploy.sh` (đã kiểm cú pháp Apache `httpd -t` OK). Verify độc lập xác nhận: build/tsc
  sạch, không lỗi console 2 trang mục tiêu, KaTeX/framer-motion vẫn ngoài JS ban đầu (đúng từ
  đợt 2, không phải việc mới). **3 việc cần quyết (xem `perf4/RESULT.md` §6–7)**:
  1. `/lop-hoc/bai` còn dư ~34 KB so với mục tiêu <1000 KB (1033,7 KB) — toàn bộ phần dư là
     `QuestionCard`/`SampleQuestionsGrid` (mục "Bài tập mẫu", nội dung chính hiện ngay khi mở
     bài) — đợt 4 **không động tới** theo đúng phạm vi được giao. Muốn đạt <1000 KB thì phải
     tách `SampleQuestionsGrid` bằng `next/dynamic({ssr:false})` — đổi UX (chớp loading ngắn lúc
     đầu), cần quyết trước khi làm.
  2. **[ĐÃ VÁ 29/9/2026 — `ChunkErrorGuard` (d275112) + script inline sớm trong `<head>` của `app/layout.tsx`, reload 1 lần/phiên tab; chưa tái kiểm trên build thật]** Lỗi nghiêm trọng phát hiện ngoài phạm vi đợt này**: xoá thử chunk `RevealMotion` (mô
     phỏng lỗi tải mạng/CDN) → trang chủ **crash trắng `Uncaught ChunkLoadError`** trong <2s,
     KHÔNG bị `RevealErrorBoundary`/`PendingFallback` bắt được (lỗi nằm trong
     `Promise.all` của runtime nạp chunk Turbopack, ngoài tầm với của ErrorBoundary React
     thường). Tái hiện 2 lần, đã phục hồi file ngay sau khi xác nhận. Đã `spawn_task` gắn cờ
     riêng cho thầy xem xét độc lập, KHÔNG sửa trong đợt 4 (đúng phạm vi được giao).
  3. Chưa tự test được luồng làm bài/nộp bài thật của `/kiem-tra/lam` (cần tài khoản học sinh
     thật, ngoài phạm vi phiên verify).

## CHƯA làm (đợt kế tiếp — prompt `prompt-giai-doan-1-2.md`)
- `/luyen-tap` có bộ lọc Lớp → Chương → Bài → YCCĐ → Dễ/TB/Khó (route chưa tồn tại).
- Thẻ "3 kỹ năng yếu nhất" trên dashboard học sinh + trọng số mức độ trong mastery.
- Bổ sung câu hỏi chương Động học 10 cho đủ ≥30 câu/bài.
- `/lo-trinh` — Learning Journey (route chưa tồn tại).
- Trang chương (`/lop-hoc/<slug>`) — đề xuất hiển thị thêm cho học sinh + phụ huynh, kèm mockup và
  phát hiện lỗi P0 (phụ huynh đang thấy "Chưa học" ở mọi bài): `docs/DE-XUAT-TRANG-CHUONG-2026-10.md` — **chờ thầy chốt 3 câu ở §7**, chưa code.
- Trang chương ↔ trang bài học lệch khung xương (760px một cột vs 1320px ba cột; hai bộ idiom
  `.class-*` / `.lesson-tree`): nghiên cứu + wireframe so sánh ở
  `docs/NGHIEN-CUU-DONG-BO-TRANG-CHUONG-TRANG-BAI.md` — **chờ thầy chốt 3 câu ở §9**, chưa code.

## LÀM NGAY KHI CÓ TOKEN (thầy ghi 30/09/2026)
**Bài tập mẫu → ngân hàng câu hỏi → tìm bài tương đương để rèn luyện.**
1. Bài tập mẫu (các dạng bài có lời giải trong `lesson_items`, mục bài tập của bài học đã đăng) phải
   lưu được vào ngân hàng câu hỏi (`/quan-tri/ngan-hang-cau-hoi`), giữ nguyên lời giải, kèm nhãn
   Lớp/Chương/Bài/YCCĐ/Dạng/mức độ. Cần: kiểm tra hiện chưa có đường nào đưa bài mẫu vào ngân hàng
   (đọc `docs/DATABASE.md` trước), viết nút/script "lưu vào ngân hàng" + chống trùng.
2. "Tìm bài tương đương": từ một bài mẫu, gợi ý các câu trong ngân hàng cùng Dạng/YCCĐ và mức độ tương
   đương (ưu tiên khớp nhãn, sau đó mới độ tương tự nội dung) để học sinh rèn luyện. Gắn vào
   `/luyen-tap` (đang ở mục "CHƯA làm" phía trên) và nút "Bài tương đương" dưới mỗi bài mẫu.
3. Lưu ý: không thêm round-trip Supabase cho trang học sinh đã tối ưu — dùng RPC gộp; migration chỉ
   viết file, Thạch chạy (xem AGENTS.md).

## Việc ngoài roadmap đang treo
- Đo lại độ trễ Supabase từ VN sau khi chuyển Singapore (PageSpeed/CrUX hoặc đo tay từ máy ở VN) và cập nhật số liệu nền. Rà URL Storage cũ đã xong ở cả 99 bảng (29/09/2026, chỉ đọc): 0 dòng còn ref project cũ; 2334 URL Storage của project mới đều tải được; 14 tệp bucket riêng (ảnh báo lỗi, tệp CNC) đều có. Chỉ còn việc đo độ trễ từ VN trước khi xoá/tạm dừng project Sydney.
- Cột `updated_at` cho `lessons`/`lesson_items` để lớp tĩnh biết lý thuyết đã sửa.
- **Kiểm loạt file `theory.html` ↔ DB (6/10/2026, chỉ đọc, 1 truy vấn — `npx tsx scripts/so-file-voi-db.mts`)**: 60/66 bài khớp.
  **5 bài lớp 10 `60, 62, 63, 64, 66` — bản tương tác CHƯA TỪNG được đăng** (DB còn bản cũ `<h2>LÝ THUYẾT</h2>` + ảnh raster, 0 quiz/hộp tương tác; không có backup `ly-thuyet-bai6*-*.json` nào). File đã ở trong git, `bundle.json` khớp `theory.html`, `lint_theory` + `lint_do_dai` sạch, dry-run chỉ chạm mục `ly_thuyet` (giữ `bai_tap_mau`/`luyen_tap`) → lệnh đăng:
  `bash scripts/cap-nhat-ly-thuyet-hang-loat.sh l10-dinh-luat-2-newton:60 l10-trong-luc-luc-cang:62 l10-luc-ma-sat:63 l10-luc-can-luc-nang:64 l10-moment-luc:66 --yes` (**KHÔNG kèm `--chi-video`** — đây là thay cả nội dung, không phải chỉ thêm video). Bản cũ có ảnh raster sẽ mất khỏi phần lý thuyết (ảnh vẫn nằm trong Storage, và script tự sao lưu `body_html` cũ vào `scripts/logs/`).
  **Bài 126 KHÔNG phải "file cũ hơn DB"**: cả thư mục `content/lesson-samples/l12-ung-dung-cam-ung-dien-tu/` **chưa vào git** — WIP của phiên khác (sửa lần cuối 4/10 14:55, cùng 3 thư mục `l12-dong-dien-xoay-chieu`, `l12-su-chuyen-the`, `l12-ung-dung-cam-ung` cũng chưa vào git). **Không đăng, không commit hộ**; DB đang là bản publish trước đó, nên `--chi-video` chặn bài này là đúng.
- **Đã gắn 5 clip cho bài 126 "Một số ứng dụng của cảm ứng điện từ" (7/10/2026, commit f89521898)**: bảng đề xuất `content/thi-nghiem/video-de-xuat-l12-ungdungcutu.md` (clip mở bài bếp từ + 4 hộp `tn-l12-ungdungcutu-01…04`), thầy chốt "đăng lên hết luôn"; đã nhập kho + chèn `theory.src.html`/`theory.html`/`bundle.json` + ghi DB item **#145** (46 291 → 48 919 ký tự, ngoài khối video không đổi, 2 mục #146/#283 giữ nguyên; sao lưu `scripts/logs/ly-thuyet-bai126-backup-1791376046541.json`) + deploy. **Cùng ngày thay tiếp clip hộp 04 bằng clip tiếng Anh `MglUIiBy2lQ` (0:51–1:51, 60 s — đúng ba lần thử liền mạch) và cắt lại hộp 01 còn 1:16–2:11** (đoạn cũ 1:25–2:55 rơi vào lời giảng cơ chế + hoạt hình pickup, trùng SVG — V6); mốc cắt lấy từ **phụ đề chính thức** (`yt-dlp --write-subs`, không còn ước từ storyboard), commit `3f37fd7f5`, đã ghi DB lại (sao lưu `scripts/logs/ly-thuyet-bai126-backup-1791376523277.json`) và deploy. `scripts/chen-video-thi-nghiem.mts` được sửa `findAnchor` để nhận `<details data-exp>` (2/4 hộp của bài này nằm trong `<details>`, trước đây bị bỏ qua im lặng). `so-file-voi-db --bai 126` báo `l12-ung-dung-cam-ung-dien-tu` **khớp DB** (mục 140 ở trên đã cũ: thư mục này nay đã vào git); lưu ý `content/lesson-samples/l12-ung-dung-cam-ung/` là **bản nháp thứ hai cũng trỏ lesson 126** (khác DB 5 160 ký tự) với bộ `tn-l12-udcamung-*` riêng.
- **Video thí nghiệm cho bài lý thuyết tương tác — có bộ khung (6/10/2026), còn thiếu dữ liệu clip**: kho `content/thi-nghiem/` đã nhận field `video` (quy ước: `content/thi-nghiem/README.md`); `scripts/chen-video-thi-nghiem.mts` chèn khối `.tl-box--video` ngay sau hộp thí nghiệm (mặc định xem thử, `--apply` mới ghi, `--kiem` kiểm link bằng oEmbed) và `scripts/cap-nhat-ly-thuyet-hang-loat.sh` đăng nhiều bài trong một lượt deploy; `components/exams/ContentHtml.tsx` đổi video thành ảnh bìa + nút phát (bấm mới nhúng player, V5). **Còn phải làm**: tìm clip cho 211 thí nghiệm của 65 bài (hiện chỉ bài Giao thoa có 4 clip chèn tay) rồi chèn + đăng. Quy tắc: `docs/QUY-TAC-THIET-KE.md` mục 5b (V1–V7). 6/10 bổ sung **clip mở bài**: khai ở `content/thi-nghiem/video-theo-bai.json` (`vi_tri: "mo_bai"`), script chèn ngay trước hộp "Dự đoán trước khi học" của mục I (thấy hiện tượng rồi mới dự đoán), clip không được lộ đáp án. **Chưa deploy** — đổi renderer chỉ thấy trên web sau `bash scripts/deploy.sh`.

(KaTeX/framer-motion đã xác nhận ngoài JS ban đầu từ đợt 2; cache header ảnh đã làm ở đợt 4 —
xem mục "Đợt tối ưu tải số 4" ở trên.)

- **9/10/2026 — L10 đủ 34/34 bài lý thuyết tương tác:** bài 65 (B20) và 67 (B22) soạn từ 6/10 nhưng chưa từng lên DB (lesson_items rỗng); 9/10 kiểm chéo lại, sửa bài 67 (commit 4f56f73e9), đăng bằng `upload-lesson.mts` → mục Lý thuyết + đề Luyện tập 904/905, deploy xong (out/data/lessons/65|67.json có tl-quiz). Treo: chưa xem 2 bài trên web thật ở 375px; bài 65 còn 3 góp ý nhỏ về Hình 3/4/5 (tỉ lệ mũi tên lặp số quiz, F_ms nằm trong khối) chưa sửa.

- **BTM L12 đợt 1 (10/10/2026):** bài 2,3,4,6,7,8 đã đăng (dòng bai_tap_mau mới 327–329 cho bài 6,7,8). Còn soạn lại 12 bài L12: 9,11,13–19,125–127 (nháp cũ batch 9/10 không đạt). Kế hoạch 42 bài L10/L11 chờ thầy duyệt.
