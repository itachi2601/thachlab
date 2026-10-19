# STATE — Hiện trạng ThachLab (rút gọn 10/10/2026)

File dùng chung cho mọi phiên, **nạp mỗi phiên nên giữ dưới ~15 KB**: chỉ hiện trạng + việc ĐANG CHỜ. Xong mục nào → chuyển
- Push thông báo (18/10): 2 migration (150000, 160000) + 2 Edge Function ĐÃ chạy/deploy. CÒN: đặt cron mỗi phút `send-notification-push` (SQL ở cuối `docs/PUSH-NHAC-HANG-NGAY.md`, cần PUSH_CRON_SECRET), deploy web (sw.js v5, chuông, PushOptInPrompt), thử điện thoại thật.
- HSG9 đợt 4 (17/10): cả 6 CĐ (151/152/163/156/158/178) đã ghi DB (ẩn) + deploy; chờ thầy xem `/lop-hoc/bai/?id=…` rồi bật Hiện (bật xong deploy lại để có file tĩnh) — xem `docs/memory/project_thachlab_khoa_hsg9_vat_ly.md`.
nguyên văn sang `docs/STATE-archive.md` (đừng để ở đây). Bản đầy đủ trước khi rút gọn nằm ở cuối `STATE-archive.md`
(mục "Bản STATE.md trước khi rút gọn") — grep ở đó khi cần chi tiết một việc cũ.

## Hạ tầng
- Next.js App Router + TypeScript + Tailwind v4, `output: "export"` (xuất tĩnh), deploy bằng `scripts/deploy.sh` → nhánh `deploy`.
- Supabase `jgvbdbpvjdntdgzthumv`, region Singapore. Sơ đồ bảng: `docs/DATABASE.md`; RPC: `docs/DATABASE-RPC.md`.
- KaTeX 0.17; font tự host qua `next/font`; học liệu tĩnh `public/data/` sinh ở `prebuild` — sửa lý thuyết phải **deploy lại** mới lên web.
- Giao diện: nền SÁNG mặc định toàn site (11/10/2026), token ở `app/globals.css`, xem `docs/MAU-NEN-SANG.md`, thử ở `/dev/giao-dien`.

## Migration — ĐANG CHỜ (nguồn đúng: `bash scripts/run-migrations.sh --list`)
- **18/10:** `20261018170000_canh_bao_bo_bai_kt_dung_han_va_is_test` — "Bỏ bài KT" chỉ khi quá hạn (`class_assessments.due_at`) hoặc ≥50% lớp nộp; thêm `profiles.is_test`; sweep chỉ tính HS thật. **Chạy migration TRƯỚC khi deploy** (code select `is_test`). Rồi `npx tsx scripts/don-canh-bao-gia.mts --dry-run` → `--apply` (dry-run thử 18/10: 321 mở → 116 giả). Sweep_engagement_alerts vẫn sinh inactive_7d cho tài khoản thử (UI đã ẩn).
- **Việc 6 đo độ sâu đọc + quiz:** migration `20261018150000_read_depth_quiz` đã chạy 18/10 22:13; client (4c9f40545) CHƯA DEPLOY; chưa có UI GV đọc RPC `teacher_lesson_read_depth(class, lesson)`.
- **17/10 DT-03 đã đăng:** 34 đề Kiểm tra nhanh lớp 10 (exam 941–974, bài 46–79, 666 câu; 9 bài còn 18–19 câu) + exam 937 (bài 12 lớp 12), đã deploy. Tồn đọng: (1) ĐÃ XỬ LÝ 18/10: gán YCCĐ cho 196/212 câu của 11 bài lớp 10 (bảng duyệt `scripts/data/duyet/gan-yccd-l10/`, script `scripts/gan-yccd-ngan-hang-l10.mts`, sao lưu `scripts/logs/sao-luu-gan-yccd-l10-*.json`, hoàn tác bằng `--undo`); còn 16 câu NONE (chuyển động cơ/hệ quy chiếu, phương án đo cổng quang, hiệu chỉnh dụng cụ) chờ thầy quyết thêm YCCĐ mới; (2) đáp án đúng là phương án dài nhất ở 40% câu trắc nghiệm (thầy chọn không sửa); (3) `next build` ở main LỖI typecheck do `scripts/{ap-dung-giai-lai-khop,batch-giai-lai,sinh-loi-giai-ngan-hang,lib/giai-lai-chung}.mts` (phiên khác commit: import đuôi .mts, cờ regex) — deploy 17/10 phải build từ worktree đã xoá 4 file đó; phiên sở hữu cần sửa hoặc thêm `scripts` vào `exclude` của tsconfig.
- **Đã chạy 17/10 23:24:** `20261017235000_rank_bat_kiem_tra_nhanh_10rp` — bật RP 10 cho 26 đề Kiểm tra nhanh/Kiểm tra hiểu bài/Luyện tập lẻ mùa 4 (mùa 5 không thêm), tính lại mùa; đề trong mục Luyện tập của bài vẫn đi đường practice_item. 3 đề cũ (#206, #209 mùa 4; #7 mùa 5) đang 20 RP giữ nguyên — thầy muốn hạ 10 thì sửa tay ở /quan-tri (rank). Sao lưu `rank_sources_backup_20261017b`.
- **17/10 23:23:** `20261018131000_sua_loc_hs_test_canh_bao` đã chạy — sửa lỗi DT-07 loại nhầm mọi email `@thachlab.local` (153 HS thật dùng đuôi này; chỉ `hs.test%` là tài khoản thử). Thử quét lại: 95 cảnh báo inactive_7d (64 urgent), lớp 12 có 41. **Đã BẬT cờ `on_tap_1_3_7` cho lớp 12 (class_id 18, 110 HS thật, 1235 bẫy đang mở)**; bẫy đã có giữ lịch cũ tới lần ghi tiếp theo. Tắt: `update feature_flags set enabled=false where flag='on_tap_1_3_7'`. So sánh lớp 11 (đối chứng) sau ~3 tuần.
- **Đã chạy 18/10:** `20261018120000_phu_dao_nguong_10_cau` (ngưỡng 12 câu/≥10 câu sai ≥50%, open 574→205) + `20261018133000_phu_dao_khong_mo_lai_muc_da_dong` (không mở lại mục đã đóng khi chưa có đề KT mới). Chi tiết/treo: `docs/memory/project_thachlab_phu_dao.md`.
- **Đã chạy 17/10 18:44:** `20261017230000_phu_dao_bo_de_luyen_tap` — phụ đạo chỉ sinh từ đề kiểm tra/BTVN/định kỳ (`exam_is_assessment`), không từ đề luyện/Kiểm tra nhanh. Dọn một lần: 192 mục auto đang mở (110 em) chuyển dismissed ghi chú "sinh từ đề luyện tập, bỏ 17/10/2026"; còn 530 mục open. Mục assigned/tutored không đụng. Rollback `perf/rollback/…down.sql`. Chưa báo trợ giảng về việc mục giảm.
- **Đã chạy 17/10 18:41:** `20261018110000_on_tap_1_3_7_theo_co` (DT-04: lịch ôn câu sai 1/3/7 ngày cho lớp có cờ `on_tap_1_3_7`; hậu kiểm bằng giao dịch rollback đạt cả 4 bước + tắt cờ). CHƯA bật cờ cho lớp nào: `insert into feature_flags (flag, class_id, note) values ('on_tap_1_3_7', <class_id>, 'thử 1/3/7')`. Lớp có cờ cần 3 lần đúng để xoá bẫy (lớp thường 2). So sánh sau ~3 tuần: tỉ lệ đúng khi ôn + số bẫy cleared.
- **Đã chạy 17/10 18:07:** `20261018100000_canh_bao_vang_mat_inactive_absent` (DT-07). Thử quét trong giao dịch rollback: 63 cảnh báo inactive_7d (45 urgent, 18 warning; lớp 10:12, 11:17, 12:28, KHTN 9:6), absent_streak 0. Cron 6:00 VN sẽ tạo thật ngày mai. Chưa có nút "Rà lại" trên dashboard. Còn: `node scripts/gen-database-doc.mjs`.
- **Đã chạy 17/10 17:52:** `20261017230000_learning_events` (DT-01) + `20261017231000_feature_flags` (DT-12); hậu kiểm RLS/grant/cron/hàm đạt, thử hàm trong giao dịch rollback. Chưa có code client gọi `log_learning_events`/`feature_enabled`; kế hoạch ở `docs/thachlab-design-thinking-audit.md`. Còn: chạy `node scripts/gen-database-doc.mjs`.
- **DT-01 client deploy 17/10 (563d50df6), chưa xác nhận bằng dữ liệu thật:** sau vài ngày có HS dùng, chạy `select kind, count(*), avg(duration_s) from learning_events group by 1` (qua `supabase db query --linked`); không thấy dòng nào thì kiểm `InlineLessonAccordion` + `services/learning-events.ts`. Deploy phải build từ worktree sạch khi `scripts/` có file `.mts` chưa commit làm `next build` lỗi typecheck.
- **Đã chạy 17/10 14:28:** `20261017150000_reset_code_manh_hon` (mã reset RS+10 hex, CHECK hạn ≤7 ngày; đã hậu kiểm default + ràng buộc).
- **Đã chạy 17/10 14:22:** `20261017120000_rate_limit_hardening` (rate_hits + rl_allow, trần resolve_login_email/quiz_join, vá search_path; hậu kiểm definer thiếu = 0) + deploy lại reset-password. Còn lại của rà soát: `docs/RA-SOAT-MA-NGUON-2026-10-17.md` mục D (Đợt 4–6); chưa kiểm entropy mã reset (`scripts/sql/kiem-do-manh-ma-reset.sql`).
- **Đã chạy 16/10 22:43:** `20261016130000_hsg9_dot3_muc_noi_dung` (mục rỗng Lý thuyết + BTM cho bài 150/153/164). CĐ15 Âm (150) đã ghi nội dung, bài ẩn, chờ deploy + thầy duyệt.
- Không còn migration nào chờ (kiểm 15/10: log `scripts/logs/` khớp hết). Vừa chạy 15/10 10:57: `20261014150000_giao_em_cho_tro_giang` (nút Giao trợ giảng, chưa thử thao tác thật) + `20261014150000_hsg9_cd17_thien_van` (CĐ17 bài 178 đang ẩn). `run-migrations.sh --list` vẫn liệt kê cả file đã chạy — đối chiếu log.
- Chưa có trong `FILES` hoặc chưa rõ (kiểm `--list`/log trước khi chạy): `20261006120000_fix_grade_ngan_hang_5_de_l11`, `20261006130000_gan_lai_chu_de_5_de_l11` (129 câu đề 638/639/658/693/701).
- **Đã chạy 16/10 14:19:** `20261016120000_ta_phong_van_phu_dao` (bảng `ta_interviews` RLS bật, 2 hàm security definer chỉ `authenticated`; trang `/tro-giang/phong-van` cho TA ghi phỏng vấn phụ đạo). Chưa deploy, chưa thử đăng nhập TA/375px. Rollback: `perf/rollback/20261016120000_ta_phong_van_phu_dao.down.sql`.
- Sau khi chạy migration: chạy `node scripts/gen-database-doc.mjs` trên Mac để cập nhật `docs/DATABASE.md` + `docs/DATABASE-RPC.md`.

## Chờ deploy / chờ kiểm
- **Deploy 5a977bddd (15/10):** sửa 5 lỗi UI học sinh (đếm câu `-conf` ở bước xem lại lý thuyết phụ đạo, danh hiệu đã nhận luôn hiện, chủ đề đã chọn dưới buổi phụ đạo, lời chào em mới, mô tả thành tích lặp). Đã kiểm trên dev local bằng HS Test (`scripts/tao-hs-test.mjs`, `gieo-hs-test.mjs`); chưa deploy, chưa chụp 375px, chưa thử đường đạt ≥80% của bài thoát phụ đạo. Chi tiết: `docs/memory/project_thachlab_hs_test_accounts.md`. Cây làm việc còn thay đổi chưa commit của phiên khác (đăng nhập/PublicAuthGate, AdminHomeToday) — KHÔNG deploy khi chưa hỏi.
- Mạng nhện Theo chương / Cả khoá (HSG: Theo mảng): migration `20261014160000` đã chạy 14/10 17:41, deploy 14/10 (commit 10eed8050). Chờ thầy xem 375px với dữ liệu thật; chưa có "Theo học kì" (DB chưa có trường học kì).
- Thử "🧰 Kiểm tra hành trang" (2 câu kiến thức nền + Nhắc nhanh) ở 10 bài chương 3 L10 (lesson 58–67), đã đăng DB 13/10, không cần deploy. Chờ đo: tỉ lệ đọc hết bài + đúng quiz giữa bài trước/sau; ổn thì làm chương khác (`scripts/chen-hanh-trang.py`, PHUONG-PHAP §4.2b).
- Mã QR đề (`ExamQrPanel`, `/quet-ma`): chưa thử iPhone + Android thật; chưa làm QR cho CNC và `LessonImporter`.
- RP lý thuyết: UI đã gọi `rank_theory_open/submit`; **chưa có khoá** → `npx tsx scripts/sinh-khoa-quiz-ly-thuyet.mts` (xem thử) rồi `--ghi`. Chưa chụp 375px bằng tài khoản HS, chưa thử nộp thật.
- Chấm nhanh HSG 9: Edge Function `hsg-ai-grade` chưa deploy (cần secret `ANTHROPIC_API_KEY`; DeepSeek đã gỡ 17/10, commit e1a9ca706). Thầy deploy lại để có hiệu lực.
- DT-16 kiểm RLS 17/10 (chỉ đọc `pg_policies`): bảng `exam_results`, `lesson_progress`, `theory_sessions`, `theory_reviews` đều bật RLS, không có policy cho `anon`; `theory_*` chỉ cho `auth.uid()` = học sinh hoặc staff. Policy `public` còn lại là bảng nội dung công khai. Chưa kiểm grant bảng cho `anon` và `learning_events` (migration 9c50d5f0c chưa chạy).
- Nền sáng: đã deploy `9077fbd47`; còn treo việc nhỏ ở `docs/MAU-NEN-SANG.md`.
- Sách in Chương 2 L10 bản v6: chờ thầy chỉnh `book/src/dang-chung.json`, `tiet.json`; `public/sach-data/*.json` v6 chưa commit/deploy (xem `docs/memory/project_thachlab_sach_in_chuong2.md`).
- Push nhắc hằng ngày: còn VAPID secrets + deploy `send-daily-push` + cron (`docs/PUSH-NHAC-HANG-NGAY.md`).
- HTML chưa có `Cache-Control: no-cache` trong `.htaccess` của `scripts/deploy.sh` — chờ thầy gật.

## Nội dung đang treo
- 17/10/2026: đã gán lớp cho 664/687 đề published chưa có exam_classes (`scripts/gan-lop-de-chua-gan.mts`, suy theo bài học chứa đề; sao lưu + hoàn tác trong `scripts/logs/gan-lop-de-*.json`). Kệ đề lớp 10/11/12 giờ lọc đúng bằng DB; vá tạm bằng tiêu đề ở `features/exams/exam-grade.ts` có thể gỡ sau.
- 17/10/2026 (sau đó): gỡ gán 10 đề `avcn` (lớp AVCN vào tự do, migration 20261013180000) bằng `scripts/go-gan-lop-de-avcn.mts`; script gán lớp giờ bỏ qua `avcn`. 23 đề không suy được: thầy duyệt 17/10 (22 → lớp 12, đề 99 → lớp 11), đã áp dụng bằng `ap-dung-duyet-lop-de.mts` (sao lưu `scripts/logs/ap-dung-duyet-lop-de-*.json`). Mọi đề published giờ đều có lớp trừ 10 đề `avcn` (cố ý).
- Còn 23 đề chưa gán (không suy được: 19 "Kiểm tra nhanh"/"Luyện tập" mồ côi bài học #99–101, #209, #239–257 + vài đề khác): danh sách `scripts/logs/gan-lop-de-khong-suy-duoc-*.json`, chờ thầy chọn lớp.
- Bài tập mẫu L12 còn soạn lại 12 bài: 9, 11, 13–19, 125–127; kế hoạch 42 bài L10/L11 chờ thầy duyệt (`docs/memory/project_thachlab_btm_quet_dang.md`).
- Bài 11 L12 Thực hành: chưa ghi DB (`upload-lesson.mts content/lesson-samples/l12-thuc-hanh-cam-ung-tu/bundle.json --lesson 12 --mode replace`); 4 bài L12 sửa đường sức chờ `cap-nhat-ly-thuyet-hang-loat.sh l12-luc-tu-cam-ung-tu:11 l12-khai-niem-tu-truong:10 l12-cam-ung-dien-tu:13 l12-dong-dien-xoay-chieu:14` — kiểm `so-file-voi-db.mts` trước vì có thể đã đăng.
- Lỗi nội dung L12 (bài 8, 10, 13, 19, 126): ĐÃ SỬA hết (18/10/2026; bài 8 `summary_html` ghi DB, sao lưu `scripts/logs/summary-bai8-backup-*.json`). Đề cũ 209, 239–257 vẫn trong DB — kiểm `exam_results` rồi dọn tay.
- Trùng slug lesson 126: `content/lesson-samples/l12-ung-dung-cam-ung/` là bản cũ, đăng từ đó sẽ LÙI bài; nên đổi tên/xoá khi rảnh.
- Bài 65 L10: 3 góp ý nhỏ về Hình 3/4/5 chưa sửa; 2 bài 65/67 chưa xem 375px trên web.
- Audit đáp án ngân hàng: chờ thầy duyệt 127 câu `_can_xac_nhan` (`scripts/data/bank-answer-fixes.json`), `scripts/logs/db-sai-can-duyet.csv` (556 + 100 câu), 8 `khong_ro` + 2 `cho_phan_xu`.
- Backfill mức độ câu hỏi: còn ~3.500 câu `difficulty` rỗng — `npx tsx scripts/backfill-question-bank-difficulty.mts 20` (**ghi thật, không dry-run**).
- Video thí nghiệm: 211 thí nghiệm / 65 bài chưa có clip (quy ước `content/thi-nghiem/README.md`, `docs/QUY-TAC-THIET-KE.md` mục 5b).
- Rank: gắn `challenge_exam_id` cho cao_thu/thach_dau season 4 ở `/quan-tri/xep-hang`; spec thi thăng hạng thích ứng `docs/BAN-GIAO-RANK-THI-THANG-HANG-2026-10-03.md`.

## Credit $100 Anthropic API — hết hạn 22/10/2026
- Chỉ áp dụng API/Batch, không áp dụng Claude Code. `scripts/batch-ra-soat-bai.mts` (chi tiết `docs/memory/project_thachlab_anthropic_credit.md`). Chế độ `sua-ly-thuyet` đã chạy cho 20 bài L12; chế độ `bai-tap-mau` dùng khi thầy bảo.

## CHƯA làm (roadmap)
- `/luyen-tap` có bộ lọc Lớp → Chương → Bài → YCCĐ → Dễ/TB/Khó; `/lo-trinh`; câu Động học 10 đủ ≥30 câu/bài.
- Trang chương: `docs/DE-XUAT-TRANG-CHUONG-2026-10.md` (chờ thầy chốt 3 câu §7) và `docs/NGHIEN-CUU-DONG-BO-TRANG-CHUONG-TRANG-BAI.md` (chờ chốt §9).
- **Bài tập mẫu → ngân hàng câu hỏi → "Bài tương đương"** (thầy ghi 30/9): lưu bài mẫu vào `/quan-tri/ngan-hang-cau-hoi` kèm nhãn + chống trùng; nút "Bài tương đương" dưới mỗi bài mẫu và ở `/luyen-tap`. Dùng RPC gộp, không thêm round-trip; migration chỉ viết file.
- Đo lại độ trễ Supabase từ máy ở VN sau khi chuyển Singapore, trước khi xoá project Sydney; thêm cột `updated_at` cho `lessons`/`lesson_items`.
- Đề xuất từ nghiên cứu HS 14–22 (11/10/2026, chờ thầy chốt mục 5): `docs/DE-XUAT-NGHIEN-CUU-HS-14-22-2026-10-11.md` — đo mùa 1 trước, fading theo mastery, đề dài làm theo phần, PhET gắn YCCĐ.

- 11/10/2026 · **UI bài lý thuyết, 5 việc CSS nhỏ thầy đã duyệt (mục 1,3,4,5,6)** — chỗ sửa + cách làm ở `docs/PHAN-TICH-HIEN-THI-LY-THUYET-TUONG-TAC-2026-10-11.md` mục 5; chưa sửa code.

## 12/10/2026 — KHTN 9 cơ học 129–131 (chưa đăng)
- Soạn + kiểm chéo xong, chờ thầy duyệt ảnh xem thử, chọn clip, bấm thử PhET, gắn topic; chi tiết `docs/memory/project_thachlab_l9_co_hoc_129_131.md`. Skill mới `.claude/skills/phet/` — Mac: `git -C ~/Projects/thachlab pull && bash ~/Projects/thachlab/scripts/cai-skill.sh`.
