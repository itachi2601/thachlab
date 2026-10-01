# STATE-archive — log migration đã chạy (tách khỏi STATE.md 28/09/2026)

Lịch sử các đợt migration đã chạy xong trên production, chuyển sang đây để STATE.md chỉ còn việc
đang chờ/đang treo. Log chạy thực tế ở `scripts/logs/`, rollback ở `perf/rollback/`.

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
