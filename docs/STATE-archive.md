# STATE-archive — log migration đã chạy (tách khỏi STATE.md 28/09/2026)

Lịch sử các đợt migration đã chạy xong trên production, chuyển sang đây để STATE.md chỉ còn việc
đang chờ/đang treo. Log chạy thực tế ở `scripts/logs/`, rollback ở `perf/rollback/`.

## Migration — 11/10/2026 (đã chạy xong 9 file)
Log: `scripts/logs/` đợt 11/10/2026. Tất cả đã chạy thành công trên production.
1. `20261010500000_notify_rp_thuong.sql` — Báo chuông khi em được cộng RP thưởng mục tiêu tuần / tiến bộ tuần / mục tiêu cả lớp (trigger trên rank_rp_ledger, kèm phụ huynh); chỉ thêm hàm + trigger, không gửi bù [rollback perf/rollback/20261010500000_notify_rp_thuong.down.sql].
2. `20261010600000_lop_hsg_vat_ly_9_duyet_tay.sql` — Thêm lớp Học sinh giỏi & Chuyên Vật lý 9 vào chỗ chọn lớp đăng ký, học sinh chỉ gửi yêu cầu chờ thầy duyệt (cột classes.requires_approval + sửa 2 policy user_classes) [rollback ở cuối file].
3. `20261010700000_ta_doc_thanh_vien_lop.sql` — Cho trợ giảng đọc danh sách thành viên lớp (1 policy SELECT trên user_classes) để dùng trang Chữa bài /tro-giang/chua-bai [rollback ở cuối file].
4. `20261011100000_exam_ta_preview.sql` — Gửi đề cho trợ giảng xem trước: bảng exam_ta_previews (+RLS) và 1 policy SELECT trên exams cho TA đọc đề đã gửi dù còn ẩn [rollback perf/rollback/20261011100000_exam_ta_preview.down.sql].
5. `20261010800000_an_cau_cat_cut_hien_thi.sql` — Ẩn 181 câu ngân hàng còn lỗi cắt cụt/hiển thị (phương án rỗng, dính tab, đề thiếu giá trị); có bảng sao lưu [rollback ở cuối file].
6. `20261010150000_ta_sua_buoi_7_ngay_va_doi_anh.sql` — Trợ giảng sửa buổi chưa duyệt trong 7 ngày (policy ta_sessions, trước là 3) + hàm set_my_avatar để trợ giảng/giáo viên đổi ảnh đại diện [rollback ở cuối file].
7. `20261011120000_question_bank_lint_flags.sql` — Thêm cột question_bank.lint_flags (text[], index GIN) cho lọc "Chỉ câu sạch" + question_content_hash bỏ khoá lint_ignored; chạy xong chạy `npx tsx scripts/cap-nhat-lint-flags.mts --ghi` [rollback ở cuối file].
8. `20261011130000_bank_set_question_figure_service.sql` — Thêm hàm bank_set_question_figure_svc (chỉ service_role) để script ghi hình Gemini đã duyệt vào câu ngân hàng; chỉ thêm hàm, không đụng dữ liệu [rollback ở cuối file].
9. `20261011140000_bank_replace_question_imgs.sql` — Thêm 2 hàm (bank_replace_imgs_in_json, bank_replace_question_imgs, chỉ service_role/giáo viên) để thay ảnh công thức bằng chữ LaTeX trong câu ngân hàng + đề đang dùng; chỉ thêm hàm, không đụng dữ liệu [rollback ở cuối file].

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
  mobile trang chủ 80→92 điểm (đo lab, kiểm độc lập). Chi tiết: `docs/archive/perf3/RESULT.md`. Đã push nhánh
  `deploy`, hosting cập nhật trong ~10 phút — **chờ đo lại PageSpeed trên site thật**.
- **Đợt tối ưu tải số 4 (split-js5 + cache ảnh, 27/9/2026)** — **ĐÃ XONG + verify độc lập +
  deploy** (commit `f068cf95`, kiểm bởi phiên riêng: `docs/archive/perf4/BASELINE.md` + `docs/archive/perf4/RESULT.md`).
  Lần 1 (`6e9d07b3` perf/split-js4) tách JS `ExamRunner`/`PracticeSession`/`LessonMasteryCard`
  bị **revert** (`063a97a4`) vì crash trắng; sau khi có lưới an toàn `app/error.tsx` +
  `LazyErrorBoundary` (`9d22e14c`) mới làm lại an toàn (`f068cf95`), mỗi chunk mới bọc riêng
  `LazyErrorBoundary` cục bộ. Cộng thêm: cache header `Cache-Control` tường minh cho ảnh trong
  `scripts/deploy.sh` (đã kiểm cú pháp Apache `httpd -t` OK). Verify độc lập xác nhận: build/tsc
  sạch, không lỗi console 2 trang mục tiêu, KaTeX/framer-motion vẫn ngoài JS ban đầu (đúng từ
  đợt 2, không phải việc mới). **3 việc cần quyết (xem `docs/archive/perf4/RESULT.md` §6–7)**:
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

- 11/10/2026 đã chạy: `20261011160000_rank_bat_nguon_thuong_chenh_lech` — bật nguồn RP cho đề/luyện tập HS mùa 4 đã nộp, `rp_first_attempt_only=0` (làm lại thưởng chênh lệch), tính lại mùa 4; chạy NGOÀI giờ học. Kèm code thông báo RP ở màn vào bài (ExamRunner) — cần deploy.

- 11/10/2026: chạy `20261011170000_ta_reminders` (log scripts/logs/20261011-095954-…ta_reminders.log); gửi nhắc tuần 05–11/10 cho 6 trợ giảng, chạy lại xác nhận không gửi trùng.

- 11/10/2026 đã chạy (10:44): `20261011170000_rank_lop10_bat_nguon` — lớp 10 thuộc mùa 5 (Alpha test) chưa có nguồn RP: bật nguồn + làm lại thưởng chênh lệch + tính lại mùa 5; chạy NGOÀI giờ học. Kết quả: +310 nguồn mùa 5, cộng bù 3305 RP/51 HS (max 207/HS).

- ĐÃ CHẠY 14/10: `20261014120000_staff_sua_sdt_hoc_sinh` — thêm hàm `staff_set_student_phones` (sửa SĐT em + phụ huynh trong tab Liên lạc gia đình); chạy lúc nào cũng được; rollback: `drop function public.staff_set_student_phones(uuid,text,text);`.
- `20261014160000_course_mastery_radar` (14/10): thêm hàm đọc `get_my_course_mastery_pct` cho mạng nhện Theo chương / Cả khoá (HSG: Theo mảng). Chỉ thêm hàm, chạy lúc nào cũng được. Rollback: `drop function if exists public.get_my_course_mastery_pct(timestamptz);`. UI `ChapterMasteryRadar` đã sửa, chưa thử 375px với dữ liệu thật; chưa có "Theo học kì" (DB chưa có trường học kì). (đã chạy 14/10/2026 17:41, log scripts/logs/20261014-174104-*)

## Chuyển từ STATE.md ngày 15/10/2026 (đã chạy/đã deploy, nguyên văn)
- `20261014150000_giao_em_cho_tro_giang` (nhánh claude/giao-tro-giang): bảng `ta_student_handoffs` + `ta_handoff_*` + trigger tự gán mục phụ đạo mới cho trợ giảng được giao; nút "Giao trợ giảng" ở hồ sơ học sinh (DiagnosticAdmin). Chạy lúc nào cũng được. Rollback: `perf/rollback/20261014150000_giao_em_cho_tro_giang.down.sql`.
- `20261014140000_chan_doan_ban_do_xuat_phat` (commit d3e158338, nhánh cursor/ui-c3, CHƯA vào main): chỉ thay hàm `diagnostic_submit`/`diagnostic_get` + thêm `diagnostic_maps` (độ chắc 3 mức → 4 nhóm; phụ huynh chỉ thấy bản cắt). Chạy lúc nào cũng được (không đụng bảng). Rollback: `perf/rollback/20261014140000_chan_doan_ban_do_xuat_phat.down.sql`.
- Đã chạy 11/10 16:58: `20261011200000_streak_moi_bai` + `20261011210000_live_study_summary` (hàm có trong DB; chưa thử bằng HS thật; heartbeat mới chỉ có ở `InlineLessonAccordion`).
- Đã chạy 11/10 13:57: `20261011150000` (kho bẫy), `20261011170000_rank_lop10_bat_nguon`, `20261011170000_ta_reminders`, `20261011190000_mistake_review_mix_ok` (lượt ôn trộn bẫy/câu ok, tỉ lệ thích ứng 0,4–0,7). Chưa thử UI bằng HS thật; 2 file `20261006120000/130000_*_l11` chưa trong FILES, chưa rõ đã chạy. Chuỗi ngày nay tính mọi bài (`20261011200000`, đã chạy + deploy 11/10 14:50).
- Đã chạy 11/10: `20261011180000_ta_doc_ket_qua_lam_bai` (TA đọc exam_results; chờ thầy thử bằng tài khoản trợ giảng); `20261011170000_ta_reminders` (skill kiem-tra-tro-giang-tuan, đã gửi nhắc tuần 05–11/10 cho 6 trợ giảng); `20261011160000_rank_bat_nguon_thuong_chenh_lech` (+30 nguồn, cộng bù 4185 RP/131 HS, max 158/HS); còn cần deploy code thông báo RP ở ExamRunner.
- Đợt 11/10/2026: Đã chạy xong 9 file (đã chuyển sang `docs/STATE-archive.md`).
- Đã chạy + deploy 14/10 (c56a0c917): `20261014100000_phu_dao_dang_ky_theo_chu_de` + `20261014110000_phu_dao_diem_danh_noi_phieu` (đăng ký chọn 1–3 chủ đề ≥12 câu, chốt 6 giờ trước, điểm danh, slot_id phiếu/bài kiểm tra, RPC `tutoring_followup_report`). Chưa thử bằng HS/TA thật. Còn làm: mục 3 (TA tự mời em chưa đánh giá, ≤6 em/tuần), mục 6 (giờ lương neo số em có mặt). Chi tiết: `docs/memory/project_thachlab_phu_dao.md`.
- Đã chạy 13/10 10:01–10:02: `20261013230000_tien_trinh_day_va_moi_chan_doan` (bảng thpt_teaching_progress/notes + teaching_get/set/note_*, thpt_invite_entry_diagnostic) và `20261013233000_tien_trinh_day_ds_khoa` (teaching_courses). Code UI (tab Tiến trình dạy, `/tro-giang/tien-trinh`, nút mời chẩn đoán) chưa deploy, chưa thử bằng tài khoản thầy/TA thật. Rollback ở cuối mỗi file.
- Đã chạy 12/10 20:09: `20261012120000_kiem_tra_dau_vao` (bảng entry_diagnostics + diagnostic_get/submit/reset). Code UI chưa deploy, chưa thử HS thật; nút "cho làm lại" + chip đã chẩn đoán đã có ở UI thầy (13/10).
- Đã chạy 13/10 07:02: `20261013200000_mon_va_lop_avcn_cttc.sql` (môn `avcn` trong `subjects` + mở 2 lớp học phần `CĐN CGKL 23A` và `CĐ CK 23A` CTTC năm học 2026-2027). Skill soạn 9 chương còn lại: `.claude/skills/soan-bai-avcn/`.
- Đã chạy 13/10 00:44: `20261013150000_chapter_mastery_radar` (RPC `get_my_chapter_mastery_pct`). UI mạng nhện giao Gemini/Cursor theo `docs/PROMPT-GEMINI-RADAR-NANG-LUC-2026-10-13.md`; Claude `kiem-code` soát trước khi merge.
- 25 bài lý thuyết L10 (lesson 46–48, 58–79) đã ghi DB 10/10, **chưa deploy**. Main local có thể ahead origin — xem trước khi push.
- Nhánh `perf-tach-js` (3 commit, JS theo vai) chưa vào main; chưa kiểm bằng đăng nhập thật.
- Đã chạy 15/10 19:14: `20261015120000_vinh_danh_hoa_diem_xoay_vong` (rank_public_honor: hoà điểm xoay theo md5(user_id||tuần), bỏ `acc` khỏi RPC công khai, thêm khối `me` cho dòng "Tuần của em"). Đã kiểm: anon không có `me`/`acc`, HS giả lập nhận {rp_week, rp_prev}.

- 15/10/2026 23:18 ĐÃ CHẠY `20261015200000_rank_ho_so_thanh_tuu_mua` (log scripts/logs/20261015-231800-…): cột bản chụp hồ sơ mùa + `rank_snapshot_season(p_season, p_force)`. Chụp thử mùa 4 trong transaction tự huỷ: 198 HS, TB 2,3 YCCĐ Nắm vững (max 13), 3 em thiếu lớp. Đóng mùa 4 sau 25/10 bằng `/quan-tri/xep-hang`.

- 15/10/2026 23:19 ĐÃ CHẠY `20261015180000_phu_huynh_tu_noi_con` (log scripts/logs/20261015-231939-…): bảng `parent_link_attempts`, `parent_link_requests` + RPC `claim_parent_by_child_info`, `request_parent_link_review`, `review_parent_link_request`, `search_students_for_link`. Thử trong giao dịch tự huỷ (`scripts/sql/thu-tu-noi-con-rollback.sql`): 9/9 bước đúng, kiểm lại không còn dữ liệu thử. Dữ liệu: 309 HS trong lớp, 0 có ngày sinh, 125 có SĐT phụ huynh → tự nối chưa khớp được ai cho tới khi nhập ngày sinh; hiện mọi phụ huynh đi đường "gửi yêu cầu → thầy duyệt".

- 15/10/2026 23:40 ĐÃ CHẠY `20261015233000_ngay_sinh_tu_dang_ky`: ngày sinh HS khai ở /dang-ky nằm trong metadata nhưng `handle_new_user` không chép sang `profiles.birth_date` → chép 142 dòng (năm 1990–2015; bỏ 8 giá trị năm 2026), sao lưu id ở `_bak_profiles_birth_20261015`; trigger giờ tự chép (`pl_safe_birth`, không raise). Kết quả: 126/291 HS THPT có ngày sinh, 106 đủ điều kiện phụ huynh tự nối (trước 0).
- 15/10/2026 23:41 ĐÃ CHẠY `20261015234500_staff_sua_ngay_sinh`: `staff_set_student_birth` (ghi profiles + metadata), ô Ngày sinh ở thẻ Liên lạc gia đình. Thử 7 bước trong giao dịch tự huỷ (`scripts/sql/thu-ngay-sinh-rollback.sql`) đều đúng.
- ĐÃ CHẠY 17/10/2026 `20261017180000_ta_giao_btvn_rieng` — bảng + 3 hàm BTVN giao riêng từng em (trợ giảng giao ở phiếu phụ đạo, thẻ Hôm nay của HS, tổng quan ở Thông báo lớp). Code đã commit và chạy được trước migration (RPC lỗi thì thẻ chỉ thiếu việc này). Chưa làm: nhắc 1 lần trước hạn, bộ chọn câu 3 lớp ôn giữa kì. Đã kiểm: bảng RLS bật, anon/authenticated không đọc trực tiếp, 3 hàm chỉ authenticated gọi được. Chưa thử luồng giao thật và chưa deploy web.

- 18/10/2026 · `20261018140000_sync_exam_to_bank_khong_sinh_trung.sql` đã chạy: sync_exam_to_bank cập nhật dòng ngân hàng cũ (cùng đề + vị trí) khi câu trong đề bị sửa, không chèn dòng trùng. Hoàn tác: `scripts/data/gon-ngan-hang/sync_exam_to_bank.truoc.sql`. Dọn bằng `scripts/gon-ngan-hang.mts`: lưu trữ 1.650 dòng (1.469 bản cũ + 181 trùng), sao lưu `scripts/logs/gon-ngan-hang-backup-1792321715189.json`.

## Migration — 18/10/2026 22:13: `20261018150000_read_depth_quiz.sql`
- **Đã chạy 18/10 22:13** (log `scripts/logs/20261018-221305-…`): `20261018150000_read_depth_quiz` — độ sâu đọc h3 + quiz đã bấm cho mục lý thuyết (sự kiện `read_depth` qua `log_learning_events`, bảng `lesson_read_depth` + rollup 90 ngày, RPC `teacher_lesson_read_depth(class, lesson)`); đã thử trên pglite. Client gửi sẵn (commit 4c9f40545, chưa deploy); chưa có UI GV đọc RPC.
- Hậu kiểm: 2 bảng bật RLS, anon không quyền, authenticated chỉ SELECT, 4 policy SELECT, cron `lesson-read-depth-rollup` (CN 21:00 UTC) active, rollup dry-run 0 dòng; thử ghi vai HS trong giao dịch rollback: lấy MAX đúng, dòng h3Max>h3Total bị bỏ. Đã sinh lại DATABASE.md.
- 21/10/2026: `20261021200000_quiz_ch3_l12_don_cu_bat_nguon_moi.sql` ĐÃ CHẠY (log scripts/logs/20261021-quiz-ch3-l12-don-cu.log): ẩn 160 câu của 8 đề Kiểm tra nhanh cũ Ch.3 L12 (#759–762, #768–770, #937), bật 10 RP cho 8 đề mới #1055–1062 ở mùa 4, thông báo 8 em đã làm đề cũ; RP cũ (61) giữ nguyên. Sao lưu quiz_ch3_l12_*_backup_20261021; rollback perf/rollback/20261021200000_*.down.sql.


## Chuyển từ STATE.md ngày 22/10/2026 (migration đã chạy)
- **Đã chạy 17/10 23:24:** `20261017235000_rank_bat_kiem_tra_nhanh_10rp` — bật RP 10 cho 26 đề Kiểm tra nhanh/Kiểm tra hiểu bài/Luyện tập lẻ mùa 4 (mùa 5 không thêm), tính lại mùa; đề trong mục Luyện tập của bài vẫn đi đường practice_item. 3 đề cũ (#206, #209 mùa 4; #7 mùa 5) đang 20 RP giữ nguyên — thầy muốn hạ 10 thì sửa tay ở /quan-tri (rank). Sao lưu `rank_sources_backup_20261017b`.
- **17/10 23:23:** `20261018131000_sua_loc_hs_test_canh_bao` đã chạy — sửa lỗi DT-07 loại nhầm mọi email `@thachlab.local` (153 HS thật dùng đuôi này; chỉ `hs.test%` là tài khoản thử). Thử quét lại: 95 cảnh báo inactive_7d (64 urgent), lớp 12 có 41. **Đã BẬT cờ `on_tap_1_3_7` cho lớp 12 (class_id 18, 110 HS thật, 1235 bẫy đang mở)**; bẫy đã có giữ lịch cũ tới lần ghi tiếp theo. Tắt: `update feature_flags set enabled=false where flag='on_tap_1_3_7'`. So sánh lớp 11 (đối chứng) sau ~3 tuần.
- **Đã chạy 18/10:** `20261018120000_phu_dao_nguong_10_cau` (ngưỡng 12 câu/≥10 câu sai ≥50%, open 574→205) + `20261018133000_phu_dao_khong_mo_lai_muc_da_dong` (không mở lại mục đã đóng khi chưa có đề KT mới). Chi tiết/treo: `docs/memory/project_thachlab_phu_dao.md`.
- **Đã chạy 17/10 18:44:** `20261017230000_phu_dao_bo_de_luyen_tap` — phụ đạo chỉ sinh từ đề kiểm tra/BTVN/định kỳ (`exam_is_assessment`), không từ đề luyện/Kiểm tra nhanh. Dọn một lần: 192 mục auto đang mở (110 em) chuyển dismissed ghi chú "sinh từ đề luyện tập, bỏ 17/10/2026"; còn 530 mục open. Mục assigned/tutored không đụng. Rollback `perf/rollback/…down.sql`. Chưa báo trợ giảng về việc mục giảm.
- **Đã chạy 17/10 18:41:** `20261018110000_on_tap_1_3_7_theo_co` (DT-04: lịch ôn câu sai 1/3/7 ngày cho lớp có cờ `on_tap_1_3_7`; hậu kiểm bằng giao dịch rollback đạt cả 4 bước + tắt cờ). CHƯA bật cờ cho lớp nào: `insert into feature_flags (flag, class_id, note) values ('on_tap_1_3_7', <class_id>, 'thử 1/3/7')`. Lớp có cờ cần 3 lần đúng để xoá bẫy (lớp thường 2). So sánh sau ~3 tuần: tỉ lệ đúng khi ôn + số bẫy cleared.
- **Đã chạy 17/10 18:07:** `20261018100000_canh_bao_vang_mat_inactive_absent` (DT-07). Thử quét trong giao dịch rollback: 63 cảnh báo inactive_7d (45 urgent, 18 warning; lớp 10:12, 11:17, 12:28, KHTN 9:6), absent_streak 0. Cron 6:00 VN sẽ tạo thật ngày mai. Chưa có nút "Rà lại" trên dashboard. Còn: `node scripts/gen-database-doc.mjs`.
- **Đã chạy 17/10 17:52:** `20261017230000_learning_events` (DT-01) + `20261017231000_feature_flags` (DT-12); hậu kiểm RLS/grant/cron/hàm đạt, thử hàm trong giao dịch rollback. Chưa có code client gọi `log_learning_events`/`feature_enabled`; kế hoạch ở `docs/thachlab-design-thinking-audit.md`. Còn: chạy `node scripts/gen-database-doc.mjs`.
- **Đã chạy 17/10 14:28:** `20261017150000_reset_code_manh_hon` (mã reset RS+10 hex, CHECK hạn ≤7 ngày; đã hậu kiểm default + ràng buộc).
- **Đã chạy 17/10 14:22:** `20261017120000_rate_limit_hardening` (rate_hits + rl_allow, trần resolve_login_email/quiz_join, vá search_path; hậu kiểm definer thiếu = 0) + deploy lại reset-password. Còn lại của rà soát: `docs/RA-SOAT-MA-NGUON-2026-10-17.md` mục D (Đợt 4–6); chưa kiểm entropy mã reset (`scripts/sql/kiem-do-manh-ma-reset.sql`).
- **Đã chạy 16/10 22:43:** `20261016130000_hsg9_dot3_muc_noi_dung` (mục rỗng Lý thuyết + BTM cho bài 150/153/164). CĐ15 Âm (150) đã ghi nội dung, bài ẩn, chờ deploy + thầy duyệt.
- Không còn migration nào chờ (kiểm 15/10: log `scripts/logs/` khớp hết). Vừa chạy 15/10 10:57: `20261014150000_giao_em_cho_tro_giang` (nút Giao trợ giảng, chưa thử thao tác thật) + `20261014150000_hsg9_cd17_thien_van` (CĐ17 bài 178 đang ẩn). `run-migrations.sh --list` vẫn liệt kê cả file đã chạy — đối chiếu log.
- **Đã chạy 16/10 14:19:** `20261016120000_ta_phong_van_phu_dao` (bảng `ta_interviews` RLS bật, 2 hàm security definer chỉ `authenticated`; trang `/tro-giang/phong-van` cho TA ghi phỏng vấn phụ đạo). Chưa deploy, chưa thử đăng nhập TA/375px. Rollback: `perf/rollback/20261016120000_ta_phong_van_phu_dao.down.sql`.

## Chuyển từ STATE.md 24/10/2026 (mục đã xong, chép nguyên văn)
- 22/10 10:47: toàn bộ main@ee71b2bd1 đã deploy (gồm khoá nội dung bài cần đăng nhập, ôn tập theo chặng, CSS khung có nghĩa .tl-fx/.tl-trap/.tl-check/.tl-note — chỉ có tác dụng khi bài có dùng lớp mới; Bài 14 Sóng L11 vẫn là bản mẫu chưa đăng).
- **Deploy 5a977bddd (15/10):** sửa 5 lỗi UI học sinh (đếm câu `-conf` ở bước xem lại lý thuyết phụ đạo, danh hiệu đã nhận luôn hiện, chủ đề đã chọn dưới buổi phụ đạo, lời chào em mới, mô tả thành tích lặp). Đã kiểm trên dev local bằng HS Test (`scripts/tao-hs-test.mjs`, `gieo-hs-test.mjs`); chưa deploy, chưa chụp 375px, chưa thử đường đạt ≥80% của bài thoát phụ đạo. Chi tiết: `docs/memory/project_thachlab_hs_test_accounts.md`. Cây làm việc còn thay đổi chưa commit của phiên khác (đăng nhập/PublicAuthGate, AdminHomeToday) — KHÔNG deploy khi chưa hỏi.
- 22/10 ĐÃ DEPLOY: đề **kiểm tra** trong trang bài có "Mã đề #N" + nút "Mã QR" (màn chiếu QR lớn, full màn hình) — dùng cho KT chương AVCN/CTTC (916, 1051, 1053…) và KT chương THPT; CTTC vào `/quet-ma` được (icon Navbar + menu Thêm thanh đáy). Chờ thử camera thật iPhone/Android.
- Nền sáng: đã deploy `9077fbd47`; còn treo việc nhỏ ở `docs/MAU-NEN-SANG.md`.
- Lỗi nội dung L12 (bài 8, 10, 13, 19, 126): ĐÃ SỬA hết (18/10/2026; bài 8 `summary_html` ghi DB, sao lưu `scripts/logs/summary-bai8-backup-*.json`). Đề cũ 209, 239–257 vẫn trong DB — kiểm `exam_results` rồi dọn tay.
## Credit $100 Anthropic API — hết hạn 22/10/2026
- Chỉ áp dụng API/Batch, không áp dụng Claude Code. `scripts/batch-ra-soat-bai.mts` (chi tiết `docs/memory/project_thachlab_anthropic_credit.md`). Chế độ `sua-ly-thuyet` đã chạy cho 20 bài L12; chế độ `bai-tap-mau` dùng khi thầy bảo.

## Tuyển sinh GĐ 0 (T1/T1b) — ĐÃ CHẠY 24/10/2026 22:23
- **24/10 tuyển sinh GĐ 0 (T1/T1b) migration đã chạy, kiểm lại đạt (RLS bật cả 3 bảng, cron public-stats-refresh có, get_public_stats trả số, anon: SĐT sai → invalid_phone, đọc trial_requests bị chặn):** `20261024160000_tuyen_sinh_trial_and_stats.sql` (trial_requests, RPC số liệu ẩn danh, referrals), sau 22h, rollback `perf/rollback/20261024160000_*.down.sql`. Trang `/gioi-thieu` có khối `TrialSignup` (chờ thầy duyệt chữ, chưa deploy; form chỉ chạy sau khi migration chạy). Kế hoạch: `user_thach_chien_luoc_chuyen_doi_tuyen_sinh` (Mac-only).

## Thí nghiệm L12 theo khung đề thi — 25–26/10/2026 (chuyển nguyên văn từ STATE.md)
- 25/10 · L12 Bài 14 (id 15) ĐÃ ĐĂNG phần thí nghiệm Rutherford theo khung đề thi (sao lưu `scripts/logs/ly-thuyet-bai15-backup-1792921923643.json`); 21 bài L12 còn lại làm bằng skill `cap-nhat-thi-nghiem-l12` (ưu tiên id 5 → 11 → 13 → 7 → 4), chưa bắt đầu.
- 25/10 · Thí nghiệm L12 Lô 1 ĐÃ ĐĂNG: id 5 thực hành nhiệt (sao lưu `ly-thuyet-bai5-backup-1792931370948.json`), id 4 nội năng (`ly-thuyet-bai4-backup-1792931379865.json`). Tiếp: Lô 2 (id 12, 11) theo `.claude/skills/cap-nhat-thi-nghiem-l12/prompts.md`.
- 25/10 · Thí nghiệm L12 Lô 2 ĐÃ ĐĂNG: id 12 (`ly-thuyet-bai12-backup-1792934115774.json`), id 11 (`ly-thuyet-bai11-backup-1792934145440.json`). ⚠ Nhánh local `claude/cap-nhat-thi-nghiem-l12-cfad9c` (chưa push) đã đăng id 5, 11, 13, 7, 4 lúc 17:13; Lô 1–2 ghi đè 5, 4, 11. Thầy chốt giữ bản phiên này cho 5, 4, 11; bản id 13, 7 của nhánh đó đã lấy vào main (commit d77363941, khớp DB), đã vá theo soát và ĐĂNG LẠI 25/10 (sao lưu `ly-thuyet-bai7-backup-1792942430701.json`, `ly-thuyet-bai13-backup-1792942448702.json`). Lô 3 (id 18 `ly-thuyet-bai18-backup-1792944539580.json`, id 19 `ly-thuyet-bai19-backup-1792944548428.json`) ĐÃ ĐĂNG 25/10. Lô 4 (id 2 `ly-thuyet-bai2-backup-1792945961694.json`, id 3 `ly-thuyet-bai3-backup-1792945967851.json`) ĐÃ ĐĂNG 25/10. Lô 5 (id 8 `ly-thuyet-bai8-backup-1792974326653.json`, id 9 `ly-thuyet-bai9-backup-1792974332782.json`) ĐÃ ĐĂNG 26/10. Lô 6 (id 10 `ly-thuyet-bai10-backup-1792981920723.json`, id 126 `ly-thuyet-bai126-backup-1792981928649.json`) ĐÃ ĐĂNG 26/10. Lô 7 (id 6 `ly-thuyet-bai6-backup-1792982860166.json`, id 16 `…bai16-backup-1792982866307.json`, id 17 `…bai17-backup-1792982870656.json`) ĐÃ ĐĂNG 26/10. Lô 8 (id 14, 125, 127) ĐÃ ĐĂNG 26/10 → **xong cả 21 bài L12**. ĐANG CHỜ: (1) bài id 6 trên main có thêm mẹo "NHỎ – LOẠN – ĐẬP" (commit 7f2a7009f, phiên khác) đã gộp với bản thí nghiệm nhưng CHƯA đăng lại — thầy quyết; (2) nhánh ruột tập data-tap phải merge main trước khi gộp/đăng. `video-theo-bai.json` còn vi_tri/nhin_vao cũ cho video bài id 12, 126 (lộ kết quả nếu chèn lại).
- 26/10 · ⚠ Nhánh local `claude/data-tap-lessons-16-19-e5e3b0` (ruột tập, chưa push) sửa theory.* hầu hết bài L12 từ bản trước khi làm thí nghiệm → khi gộp vào main sẽ xung đột; đã nhắn phiên đó merge main trước, KHÔNG đăng lý thuyết từ nhánh đó. Nhánh cfad9c còn lại KHÔNG merge.
- **26/10 Bucket clip tự dựng — ĐÃ CHẠY 26/10 13:39 (log scripts/logs/20261026-133941-…); clip bóng bay đã tải, bài 6 L12 đã đăng 26/10 ~13:55, phát thử trên web OK.** `20261026200000_bucket_lesson_clips.sql` (bucket công khai `lesson-clips`, mp4+webp ≤ 5 MB; rollback xoá bucket khi trống). Sau đó tải clip bóng bay (`tai-clip-len-storage.mts`) và chèn vào bài 6 L12 — `docs/KE-HOACH-CLIP-ANH-DONG.md`.


## Bản STATE.md trước khi rút gọn 26/10/2026 (nguyên văn)

## Hạ tầng
- Next.js App Router + TypeScript + Tailwind v4, `output: "export"` (xuất tĩnh), deploy bằng `scripts/deploy.sh` → nhánh `deploy`.
- Supabase `jgvbdbpvjdntdgzthumv`, region Singapore. Sơ đồ bảng: `docs/DATABASE.md`; RPC: `docs/DATABASE-RPC.md`.
- KaTeX 0.17; font tự host qua `next/font`; học liệu tĩnh `public/data/` sinh ở `prebuild` — sửa lý thuyết phải **deploy lại** mới lên web.
- Giao diện: nền SÁNG mặc định toàn site (11/10/2026), token ở `app/globals.css`, xem `docs/MAU-NEN-SANG.md`, thử ở `/dev/giao-dien`.

## Migration — ĐANG CHỜ (nguồn đúng: `bash scripts/run-migrations.sh --list`)
- **24/10 Ghi chú HS theo mục bài học — CHƯA CHẠY:** `20261024190000_lesson_notes.sql` (bảng mới `lesson_notes`, RLS chỉ chủ sở hữu 4 thao tác, giáo viên/TA không đọc; lúc nào cũng được; rollback: `drop table public.lesson_notes`).
- **25/10 Ôn tập theo chặng — chế độ Tự học ở nhà:** migration `20261025100000_on_tap_tu_hoc_ve_nha` ĐÃ CHẠY 25/10 (thử trong giao dịch tự huỷ trước). Client xong trên nhánh, CHƯA thử UI bằng tài khoản thầy trên local, CHƯA deploy. Chi tiết: memory `project_thachlab_on_tap_theo_chang`.
- **24/10 P0 #1 chặng 1 (chấm server):** `20261024150000_exam_answer_server_grading` ĐÃ CHẠY 24/10 11:21 (đối chiếu 500 bài/10.057 câu: TS≠SQL = 0, TS≠đã lưu = 0; hàm anon không gọi được; `rank_fix_quiz_submit(bigint,int)` cũ còn grant anon — bỏ ở chặng 3) — chỉ thêm hàm/view/trigger; từ lúc chạy, điểm HS do DB chấm lại (điểm client lệch giữ ở `detail.client_score`). Còn chặng 2 (client dùng RPC + `exams_staff`) và 3 (thu quyền đọc `exams.questions`, bỏ INSERT trực tiếp, bỏ `rank_fix_quiz_submit(int)`).
- **24/10 Ôn theo chặng — xem lại chặng cũ + em sai (migration ĐÃ CHẠY 24/10 14:49, đã thử; client ĐÃ DEPLOY 24/10 14:57):** `20261024170000_on_tap_xem_lai_chang_em_sai.sql` (hàm `review_board_stage`, `review_wrong_students`; rollback `perf/rollback/…down.sql`). Thử lớp 18/đề 20 (104 em): tổng `students_wrong` theo câu = số dòng `review_wrong_students` = 762, `review_board` cũ = `review_board_stage`, chưa đăng nhập → forbidden, chặng ngoài khoảng → stage_invalid. Client (`ReviewConsole`: bấm chặng xem lại, bấm câu/dạng/em thấy tên) đã kiểm 375px bằng dữ liệu giả; chưa thử đăng nhập thật với lớp thật.
- **24/10 Ngân hàng→Luyện tập chặng 0 (migration ĐÃ CHẠY 24/10 ~19:30, client ĐÃ DEPLOY 24/10 ~23:00 (build wvm8aBimOsraIKTVjZTWm, main 2e6749a3e; 37 câu _can_xac_nhan còn sống đã gắn cờ `canXacNhanDapAn`, log hoàn tác scripts/logs/can-xac-nhan-1792855986756.json; chưa thử ghi bank_id bằng HS thật); thử local L12 Bài 1 OK: 98 câu, chấm câu ngân hàng 200):** `20261024200000_lesson_practice_pool_ngan_hang` — RPC `lesson_practice_pool`, `check_bank_practice_answer`, cột `practice_question_results.bank_id`. Báo cáo + kế hoạch 4 chặng: `docs/BAO-CAO-NGAN-HANG-THEO-BAI-2026-10-24.md`. Còn: (1) kho hiện chỉ ~61/568 câu ở L12 Bài 1 vì `exam_is_assessment` loại cả đề thi thử gắn mục Kiểm tra — đề xuất lọc `not assessment OR exam_answers_revealed` → `20261024210000_lesson_practice_pool_noi_loc_de_danh_gia` ĐÃ CHẠY 24/10 (đo: kho L12 Bài 1 tối đa 118 câu cho em mới, +1 khi em mở đáp án 1 đề thi thử; ~500 câu còn khoá sau cổng 3 lượt/đạt điểm → thầy chốt mở cả kho: `20261024220000_lesson_practice_pool_mo_ca_kho` ĐÃ CHẠY 24/10 (đo em mới L12 Bài 1, 100/mức: 203 câu gồm 19 Khó, không lộ đáp án, câu đề giao thật chưa mở bị từ chối; 425 đề "Kiểm tra chương/HK" cũng được mở — xem đầu file); (2) gắn `lint_flags` cho 127 câu `_can_xac_nhan`; (3) chưa thử ghi `bank_id` bằng tài khoản HS thật.
- **24/10 P0 #1 chặng 2 xong, ĐÃ DEPLOY 24/10 (sw v6), ĐANG CHỜ chặng 3:** client đã dùng RPC (commit e146b8cab…e145838f7), đề đánh giá bị loại khỏi pool luyện tập/phụ đạo. **Chặng 3 (thu quyền `exams.questions`) CHƯA làm được vì CNC học sinh** (`services/cnc-exam-bank.ts` `fetchCncQuizBanks`, `CncCourseWorkspace`) còn đọc thẳng cột này → cần RPC riêng cho CNC trước. Chặng 3 sau 22h, ≥3 ngày sau khi client lên; chạy truy vấn `pg_proc` tìm hàm security invoker còn đọc `questions`. Còn lỗ khác: `practice_sessions.score` client tự gửi, `question_bank` đọc được qua policy exit-quiz/entry-diagnostic (chặng 4).
- **21/10 Ôn tập theo chặng:** `20261021120000_on_tap_theo_chang` ĐÃ CHẠY (bảng `review_sessions` + 8 hàm `review_*`). Client (`/tro-giang/on-tap`, `/lop-hoc/on-tap`, banner ở `/lop-hoc`) ĐÃ DEPLOY 21/10 (main@585514553, gồm cả mọi client chưa deploy của các phiên khác tới thời điểm đó); chưa thử học sinh/tivi thật. Chi tiết: `docs/memory/project_thachlab_on_tap_theo_chang.md`.
- **23/10 Ôn dạng bài tập L11:** `gan-dang-chuong1-l11.sql` (380 câu, Dao động) + `gan-dang-chuong2-l11.sql` (411 câu, Sóng) ĐÃ CHẠY. Dạng thiếu câu (<3 chắc chắn): xem memory `project_thachlab_on_tap_theo_chang`.
- **24/10 Ôn dạng bài tập L12 Ch.1+2:** `gan-dang-chuong1-l12.sql` (165 câu, Vật lí nhiệt) + `gan-dang-chuong2-l12.sql` (255 câu, Khí lí tưởng; tổng 92 `unsure`) ĐÃ CHẠY. Bài 4 (thực hành) chưa gán được. Dạng <3 câu chắc: xem memory `project_thachlab_on_tap_theo_chang`.
- **23/10 Hệ khung lý thuyết L9–L12:** 90 bài (L9 9, L10 34, L11 26, L12 21 — trừ 3 bài KHTN9 Bài 2–4 chưa đăng bản tương tác và thư mục trùng `l12-ung-dung-cam-ung.cu`) ĐÃ GHI DB (chỉ mục Lý thuyết, kiểm lại 90/90 khớp file; sao lưu `scripts/logs/ly-thuyet-bai*-backup-*.json`). ĐÃ DEPLOY 23/10 (deploy@c0fe33f); kiểm web thật 375px bài 43 (L11) và 18 (L12): khung/công thức đúng, không tràn ngang, KaTeX 0 lỗi. Chưa kiem-code soát công thức do agent thêm.
- **23/10 Ôn dạng bài tập:** `20261023120000_on_tap_dang_bai_tap` + `gan-dang-chuong3-l12.sql` ĐÃ CHẠY (bảng `question_dang`, 362 câu Chương 3 L12 do Claude gán, 89 câu `unsure` không dùng). Client ĐÃ DEPLOY 24/10 (deploy@834e4a6); chưa thử học sinh thật. Chi tiết: memory `project_thachlab_on_tap_theo_chang`.
- **19/10 Casio:** `20261019120000_lop_casio_giai_vat_li_mtct` ĐÃ CHẠY (lớp+môn `casio-vat-ly`, bài 179–183, đề 980–984, 5 bài). 24/10: kiem-code soát (đã sửa tiêu đề nhóm WP-01), đăng lại + `--publish` → 5 bài + 5 đề ĐÃ HIỆN; client hub `/lop-hoc/casio-vat-ly` ĐÃ DEPLOY. Còn: mini-test WP-01 lặp bài luyện, kiểm `suggestedAnswer` markdown trên trang HS. Nguồn `content/casio-vat-ly/`, dựng lại: `bash scripts/dang-casio-vat-ly.sh`.
- **18/10:** `20261018170000_canh_bao_bo_bai_kt_dung_han_va_is_test` — "Bỏ bài KT" chỉ khi quá hạn (`class_assessments.due_at`) hoặc ≥50% lớp nộp; thêm `profiles.is_test`; sweep chỉ tính HS thật. **Chạy migration TRƯỚC khi deploy** (code select `is_test`). Rồi `npx tsx scripts/don-canh-bao-gia.mts --dry-run` → `--apply` (dry-run thử 18/10: 321 mở → 116 giả). Sweep_engagement_alerts vẫn sinh inactive_7d cho tài khoản thử (UI đã ẩn).
- **Việc 6 đo độ sâu đọc + quiz:** migration `20261018150000_read_depth_quiz` đã chạy 18/10 22:13; client ĐÃ DEPLOY 24/10 (deploy@834e4a6); chưa có UI GV đọc RPC `teacher_lesson_read_depth(class, lesson)`.
- **17/10 DT-03 đã đăng:** 34 đề Kiểm tra nhanh lớp 10 (exam 941–974, bài 46–79, 666 câu; 9 bài còn 18–19 câu) + exam 937 (bài 12 lớp 12), đã deploy. Tồn đọng: (1) ĐÃ XỬ LÝ 18/10: gán YCCĐ cho 196/212 câu của 11 bài lớp 10 (bảng duyệt `scripts/data/duyet/gan-yccd-l10/`, script `scripts/gan-yccd-ngan-hang-l10.mts`, sao lưu `scripts/logs/sao-luu-gan-yccd-l10-*.json`, hoàn tác bằng `--undo`); còn 16 câu NONE (chuyển động cơ/hệ quy chiếu, phương án đo cổng quang, hiệu chỉnh dụng cụ) chờ thầy quyết thêm YCCĐ mới; (2) đáp án đúng là phương án dài nhất ở 40% câu trắc nghiệm (thầy chọn không sửa); (3) ĐÃ XỬ LÝ (tsconfig loại `scripts`, commit 12bc84943; `tsc --noEmit` sạch 19/10): `next build` từng LỖI typecheck do `scripts/{ap-dung-giai-lai-khop,batch-giai-lai,sinh-loi-giai-ngan-hang,lib/giai-lai-chung}.mts` (phiên khác commit: import đuôi .mts, cờ regex) — deploy 17/10 phải build từ worktree đã xoá 4 file đó; phiên sở hữu cần sửa hoặc thêm `scripts` vào `exclude` của tsconfig.
- **DT-01 client deploy 17/10 (563d50df6), chưa xác nhận bằng dữ liệu thật:** sau vài ngày có HS dùng, chạy `select kind, count(*), avg(duration_s) from learning_events group by 1` (qua `supabase db query --linked`); không thấy dòng nào thì kiểm `InlineLessonAccordion` + `services/learning-events.ts`. Deploy phải build từ worktree sạch khi `scripts/` có file `.mts` chưa commit làm `next build` lỗi typecheck.
- Chưa có trong `FILES` hoặc chưa rõ (kiểm `--list`/log trước khi chạy): `20261006120000_fix_grade_ngan_hang_5_de_l11`, `20261006130000_gan_lai_chu_de_5_de_l11` (129 câu đề 638/639/658/693/701).
- Sau khi chạy migration: chạy `node scripts/gen-database-doc.mjs` trên Mac để cập nhật `docs/DATABASE.md` + `docs/DATABASE-RPC.md`.

## Chờ deploy / chờ kiểm
- 24/10 Làm bài (báo "tự nhảy câu, đáp án sai" + #140/#142): ĐÃ DEPLOY 4 sửa — chạm lại phương án/Đúng-Sai đang chọn không bỏ chọn; `/kiem-tra/lam` chỉ tải đề 1 lần theo (user, đề); lưới chống chunk 404 trong layout hết SyntaxError (trước nay chưa chạy); luôn xác nhận trước khi nộp. Code không có auto-advance, 36 bài đề 752 lưu đúng. CÒN: chờ HS phản hồi — nếu vẫn "nhảy câu" thì hỏi trang nào (Kiểm tra/Luyện tập Từng câu/Thăng hạng), máy gì.
- Push thông báo (18/10): 2 migration (150000, 160000) + 2 Edge Function ĐÃ chạy/deploy. Cron `send-notification-push` ĐÃ đặt (jobid 6, mỗi phút trong khung 6–22h VN, active; kiểm 19/10). CÒN: thử điện thoại thật (web đã deploy 19/10 từ 53f8b3cfa: sw.js v5, chuông, PushOptInPrompt, độ sâu đọc, lịch tuần).
- HSG9 đợt 4 (17/10): cả 6 CĐ (151/152/163/156/158/178) đã ghi DB (ẩn) + deploy; chờ thầy xem `/lop-hoc/bai/?id=…` rồi bật Hiện (bật xong deploy lại để có file tĩnh) — xem `docs/memory/project_thachlab_khoa_hsg9_vat_ly.md`.
- AVCN (20/10): 10 bài tách thành **10 chương** (migration `20261020190000_avcn_tach_10_chuong`, mỗi chương 1 bài, tiêu đề chương bỏ "Chapter n:"); cả 10 bài đã có dòng 🎧 nghe lại câu tình huống bằng **giọng nam Guy** (bài 168–177, body_html đã ghi + deploy); mục tiêu/chuẩn đầu ra viết theo nội dung bài, bỏ "(Part 1/2…)"; tối 20/10 viết lại thành **4 gạch kiến thức/chương**, bỏ bảng 5 Part khỏi tab Học (đã ghi DB + deploy). Ch9 nay có đủ mp3 (trước 0 file). Chờ thầy nghe thử 1–2 bài rồi chốt giọng (Guy/Andrew/Brian) — đổi thì chạy lại `tao_giong_doc.py` + `cap-nhat-ly-thuyet.sh` + `deploy.sh`.
- Mạng nhện Theo chương / Cả khoá (HSG: Theo mảng): migration `20261014160000` đã chạy 14/10 17:41, deploy 14/10 (commit 10eed8050). Chờ thầy xem 375px với dữ liệu thật; chưa có "Theo học kì" (DB chưa có trường học kì).
- Thử "🧰 Kiểm tra hành trang" (2 câu kiến thức nền + Nhắc nhanh) ở 10 bài chương 3 L10 (lesson 58–67), đã đăng DB 13/10, không cần deploy. Chờ đo: tỉ lệ đọc hết bài + đúng quiz giữa bài trước/sau; ổn thì làm chương khác (`scripts/chen-hanh-trang.py`, PHUONG-PHAP §4.2b).
- Mã QR đề (`ExamQrPanel`, `/quet-ma`): chưa thử iPhone + Android thật; chưa làm QR cho CNC và `LessonImporter`.
- RP lý thuyết: UI đã gọi `rank_theory_open/submit`; **chưa có khoá** → `npx tsx scripts/sinh-khoa-quiz-ly-thuyet.mts` (xem thử) rồi `--ghi`. Chưa chụp 375px bằng tài khoản HS, chưa thử nộp thật.
- Chấm nhanh HSG 9: Edge Function `hsg-ai-grade` chưa deploy (cần secret `ANTHROPIC_API_KEY`; DeepSeek đã gỡ 17/10, commit e1a9ca706). Thầy deploy lại để có hiệu lực.
- DT-16 kiểm RLS 17/10 (chỉ đọc `pg_policies`): bảng `exam_results`, `lesson_progress`, `theory_sessions`, `theory_reviews` đều bật RLS, không có policy cho `anon`; `theory_*` chỉ cho `auth.uid()` = học sinh hoặc staff. Policy `public` còn lại là bảng nội dung công khai. Chưa kiểm grant bảng cho `anon` và `learning_events` (migration 9c50d5f0c chưa chạy).
- Sách in Chương 2 L10 bản v6: chờ thầy chỉnh `book/src/dang-chung.json`, `tiet.json`; `public/sach-data/*.json` v6 chưa commit/deploy (xem `docs/memory/project_thachlab_sach_in_chuong2.md`).
- Push nhắc hằng ngày: còn VAPID secrets + deploy `send-daily-push` + cron (`docs/PUSH-NHAC-HANG-NGAY.md`).
- HTML chưa có `Cache-Control: no-cache` trong `.htaccess` của `scripts/deploy.sh` — chờ thầy gật.

## Nội dung đang treo
- 26/10 · Mẹo từ khoá đợt 1: 17 bài (21 thư mục, L10–12) đã đăng 26/10/2026 + CSS `.tl-meo` đã deploy; bảng mẹo `docs/BANG-MEO-TU-KHOA.md`; đợt 2 (○) chờ số liệu Trả bài một chương. 5 bài vốn đã vượt 2.500 từ (l10 giai-bai-toan-dlh, chuyen-dong-nem; l11 tat-dan, song-dung, khai-niem-dien-truong) nay +6…+80 từ — KHÔNG cắt riêng: thầy để phiên làm video giảm chữ (26/10).
- 26/10 · Thí nghiệm theo khung đề thi: **xong cả 21 bài L12** (đã đăng, sao lưu từng bài ở `STATE-archive.md` mục "Thí nghiệm L12"). ĐANG CHỜ: (1) id 6 bản gộp thí nghiệm + mẹo "NHỎ – LOẠN – ĐẬP" (7f2a7009f) ĐÃ ĐĂNG LẠI 26/10 (`ly-thuyet-bai6-backup-1792987021489.json`); (2) nhánh local `claude/data-tap-lessons-16-19-e5e3b0` (ruột tập) sửa theory.* từ bản cũ — phải merge main trước, KHÔNG đăng từ nhánh đó; (3) `video-theo-bai.json` còn vi_tri/nhin_vao cũ cho video id 12, 126.
- 17/10/2026: đã gán lớp cho 664/687 đề published chưa có exam_classes (`scripts/gan-lop-de-chua-gan.mts`, suy theo bài học chứa đề; sao lưu + hoàn tác trong `scripts/logs/gan-lop-de-*.json`). Kệ đề lớp 10/11/12 giờ lọc đúng bằng DB; vá tạm bằng tiêu đề ở `features/exams/exam-grade.ts` có thể gỡ sau.
- 17/10/2026 (sau đó): gỡ gán 10 đề `avcn` (lớp AVCN vào tự do, migration 20261013180000) bằng `scripts/go-gan-lop-de-avcn.mts`; script gán lớp giờ bỏ qua `avcn`. 23 đề không suy được: thầy duyệt 17/10 (22 → lớp 12, đề 99 → lớp 11), đã áp dụng bằng `ap-dung-duyet-lop-de.mts` (sao lưu `scripts/logs/ap-dung-duyet-lop-de-*.json`). Mọi đề published giờ đều có lớp trừ 10 đề `avcn` (cố ý).
- Còn 23 đề chưa gán (không suy được: 19 "Kiểm tra nhanh"/"Luyện tập" mồ côi bài học #99–101, #209, #239–257 + vài đề khác): danh sách `scripts/logs/gan-lop-de-khong-suy-duoc-*.json`, chờ thầy chọn lớp.
- Bài tập mẫu L12 còn soạn lại 12 bài: 9, 11, 13–19, 125–127; kế hoạch 42 bài L10/L11 chờ thầy duyệt (`docs/memory/project_thachlab_btm_quet_dang.md`).
- Bài 11 L12 Thực hành: chưa ghi DB (`upload-lesson.mts content/lesson-samples/l12-thuc-hanh-cam-ung-tu/bundle.json --lesson 12 --mode replace`); 4 bài L12 sửa đường sức chờ `cap-nhat-ly-thuyet-hang-loat.sh l12-luc-tu-cam-ung-tu:11 l12-khai-niem-tu-truong:10 l12-cam-ung-dien-tu:13 l12-dong-dien-xoay-chieu:14` — kiểm `so-file-voi-db.mts` trước vì có thể đã đăng.
- Trùng slug lesson 126: `content/lesson-samples/l12-ung-dung-cam-ung/` là bản cũ, đăng từ đó sẽ LÙI bài; nên đổi tên/xoá khi rảnh.
- Bài 65 L10: 3 góp ý nhỏ về Hình 3/4/5 chưa sửa; 2 bài 65/67 chưa xem 375px trên web.
- Audit đáp án ngân hàng: chờ thầy duyệt 127 câu `_can_xac_nhan` (`scripts/data/bank-answer-fixes.json`), `scripts/logs/db-sai-can-duyet.csv` (556 + 100 câu), 8 `khong_ro` + 2 `cho_phan_xu`.
- Backfill mức độ câu hỏi: còn ~3.500 câu `difficulty` rỗng — `npx tsx scripts/backfill-question-bank-difficulty.mts 20` (**ghi thật, không dry-run**).
- Video thí nghiệm: 211 thí nghiệm / 65 bài chưa có clip (quy ước `content/thi-nghiem/README.md`, `docs/QUY-TAC-THIET-KE.md` mục 5b).
- Rank: gắn `challenge_exam_id` cho cao_thu/thach_dau season 4 ở `/quan-tri/xep-hang`; spec thi thăng hạng thích ứng `docs/BAN-GIAO-RANK-THI-THANG-HANG-2026-10-03.md`.

## CHƯA làm (roadmap)
- `/luyen-tap` có bộ lọc Lớp → Chương → Bài → YCCĐ → Dễ/TB/Khó; `/lo-trinh`; câu Động học 10 đủ ≥30 câu/bài.
- Trang chương: `docs/DE-XUAT-TRANG-CHUONG-2026-10.md` (chờ thầy chốt 3 câu §7) và `docs/NGHIEN-CUU-DONG-BO-TRANG-CHUONG-TRANG-BAI.md` (chờ chốt §9).
- **Bài tập mẫu → ngân hàng câu hỏi → "Bài tương đương"** (thầy ghi 30/9): lưu bài mẫu vào `/quan-tri/ngan-hang-cau-hoi` kèm nhãn + chống trùng; nút "Bài tương đương" dưới mỗi bài mẫu và ở `/luyen-tap`. Dùng RPC gộp, không thêm round-trip; migration chỉ viết file.
- Đo lại độ trễ Supabase từ máy ở VN sau khi chuyển Singapore, trước khi xoá project Sydney; thêm cột `updated_at` cho `lessons`/`lesson_items`.
- Đề xuất từ nghiên cứu HS 14–22 (11/10/2026, chờ thầy chốt mục 5): `docs/DE-XUAT-NGHIEN-CUU-HS-14-22-2026-10-11.md` — đo mùa 1 trước, fading theo mastery, đề dài làm theo phần, PhET gắn YCCĐ.

- 11/10/2026 · **UI bài lý thuyết, 5 việc CSS nhỏ thầy đã duyệt (mục 1,3,4,5,6)** — chỗ sửa + cách làm ở `docs/PHAN-TICH-HIEN-THI-LY-THUYET-TUONG-TAC-2026-10-11.md` mục 5; chưa sửa code.

## 12/10/2026 — KHTN 9 cơ học 129–131 (chưa đăng)
- Soạn + kiểm chéo xong, chờ thầy duyệt ảnh xem thử, chọn clip, bấm thử PhET, gắn topic; chi tiết `docs/memory/project_thachlab_l9_co_hoc_129_131.md`. Skill mới `.claude/skills/phet/` — Mac: `git -C ~/Projects/thachlab pull && bash ~/Projects/thachlab/scripts/cai-skill.sh`.
- **22/10 Phản biện rà soát + dọn lint:** `docs/RA-SOAT-DU-AN-2026-10-22-PHAN-BIEN.md` — báo cáo khớp ~95 %, sửa 1 câu sai (`@xmldom/xmldom` còn 3 script dùng), thêm lỗ lộ đáp án qua `exams.questions` (P0 #1 phải lược đáp án + chấm server). Lint 94 → 0 lỗi (DeepSeek 4 lượt qua `scripts/deepseek-sua-lint.mts` + Claude 6 file lớn, `kiem-code` soát hết). ĐANG CHỜ: thầy thử `/lop-hoc` trên điện thoại (4 effect đổi sang render-phase); bật CI gate eslint/tsc (P0 #4).
- **23/10 tối — sự cố lớp 40 em không vào được:** nghẽn ở đoạn Cloudflare→origin với file không cache (HTML, RSC .txt, .json): qua CF 1–5 s/request, thẳng origin 0,17 s (đo + cách đo lại: memory `project_thachlab_hosting`). Thầy chuyển DNS về đám mây xám; đã deploy 71858c3b3 (tắt prefetch Link điều hướng, SW `updateViaCache: none`). CHƯA xác nhận với lớp thật; nếu còn chậm thì đo lại bằng `--resolve` và xem Supabase `rank_my_status` (mean 272 ms, max 7,9 s).
- **23/10 tối — Supabase cạn Disk IO budget (email):** deploy f838ccc82 cache 2 phút `rank_my_status`/`rank_my_titles` + Watcher 1 lần/2 phút; quy tắc batch sau 22h ở AGENTS.md. CHƯA: thầy xem biểu đồ IO theo giờ + gói compute (Micro → Small nếu còn chậm); kiểm số lượt gọi RPC rank giảm sau 1 tuần (`pg_stat_statements`).
- **23/10 tối: Supabase lên gói PRO** (chu kỳ 23/10–23/11, spend cap bật, 8 GB đĩa). Compute đã đổi sang t3a.small 23/10 ~20:30 (thầy bấm, DB khởi động lại ~5 phút). Sau 1 tuần (30/10) đo lại CPU + mean_ms rank_my_status (mốc cũ 80 % / 272 ms).
- **25/10 quiz lý thuyết chuẩn mới (29 bộ làm lại, `scripts/data/theory-quiz/`):** 26 bộ (83–91, 150–166, 178) ĐÃ GHI DB 25/10 22:13 (exam 1076–1101, kiểm lại: exam_ids/quiz_min_correct/số câu khớp 26/26; đề cũ 1021–1049 giữ nguyên, log `scripts/logs/publish-quiz-26-20261025.log`) — ĐÃ DEPLOY 25/10 22:3x (deploy@f7bd8ea, build từ nhánh quiz b71f02cb8, không kèm client "Tự học ở nhà" chưa thử UI). 129–131 CHƯA đăng được: DB còn lý thuyết cũ (3 đoạn), phải đăng lý thuyết tương tác trước rồi gán lại `theorySection`. 178 còn 18 câu (thiếu 2 câu Eratosthenes).
