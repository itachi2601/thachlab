# STATE — Hiện trạng ThachLab (rút gọn 26/10/2026)

File dùng chung cho mọi phiên, **nạp mỗi phiên nên giữ dưới ~15 KB**: chỉ hiện trạng + việc ĐANG CHỜ, mỗi việc 1–2 dòng.
Xong mục nào → chuyển nguyên văn sang `docs/STATE-archive.md`. Chi tiết đầy đủ của các mục dưới đây (trước khi rút gọn)
nằm ở cuối `STATE-archive.md`, mục "Bản STATE.md trước khi rút gọn 26/10/2026" — grep ở đó khi cần.

## Hạ tầng
- Next.js App Router + TypeScript + Tailwind v4, `output: "export"` (xuất tĩnh), deploy bằng `scripts/deploy.sh` → nhánh `deploy`.
- Supabase `jgvbdbpvjdntdgzthumv`, Singapore, gói PRO (23/10–23/11, spend cap bật), compute t3a.small. Sơ đồ: `docs/DATABASE.md`, RPC: `docs/DATABASE-RPC.md`.
- KaTeX 0.17; font tự host qua `next/font`; học liệu tĩnh `public/data/` sinh ở `prebuild` — sửa lý thuyết phải **deploy lại** mới lên web.
- Giao diện: nền SÁNG mặc định (11/10/2026), token `app/globals.css`, xem `docs/MAU-NEN-SANG.md`, thử `/dev/giao-dien`.
- Deploy phải build từ worktree sạch khi `scripts/` có `.mts` chưa commit làm `next build` lỗi typecheck.

## Migration — ĐANG CHỜ (nguồn đúng: `bash scripts/run-migrations.sh --list`)
- **CHƯA CHẠY:** `20261024190000_lesson_notes.sql` (bảng `lesson_notes`, RLS chủ sở hữu; chạy lúc nào cũng được; rollback `drop table public.lesson_notes`).
- Chưa rõ đã chạy chưa (kiểm `--list`/log): `20261006120000_fix_grade_ngan_hang_5_de_l11`, `20261006130000_gan_lai_chu_de_5_de_l11`.
- **P0 #1 chặng 3** (thu quyền `exams.questions`, bỏ INSERT trực tiếp, bỏ `rank_fix_quiz_submit(int)`): chặn bởi CNC HS (`services/cnc-exam-bank.ts`, `CncCourseWorkspace`) còn đọc thẳng cột → cần RPC CNC trước; sau 22h. Chặng 4: `practice_sessions.score` client gửi, `question_bank` lộ qua policy exit-quiz/entry-diagnostic.
- Sau khi chạy migration: `node scripts/gen-database-doc.mjs` trên Mac.

## Chờ thử thật / chờ deploy
- **Ôn tập theo chặng — Tự học ở nhà** (migration ĐÃ CHẠY 25/10): client CHƯA thử UI bằng tài khoản thầy, CHƯA deploy. Memory `project_thachlab_on_tap_theo_chang`.
- Ôn tập theo chặng (21/10, 24/10 xem lại chặng + em sai) + ôn dạng bài tập (L11 Ch.1–2, L12 Ch.1–3 đã gán): ĐÃ DEPLOY, chưa thử HS/tivi thật. L12 Bài 4 chưa gán dạng.
- Ngân hàng→Luyện tập (24/10, mở cả kho): ĐÃ DEPLOY; còn gắn `lint_flags` 127 câu `_can_xac_nhan`, thử ghi `bank_id` bằng HS thật. Báo cáo `docs/BAO-CAO-NGAN-HANG-THEO-BAI-2026-10-24.md`.
- Làm bài (24/10, "tự nhảy câu"): 4 sửa đã deploy; nếu HS còn báo → hỏi trang nào, máy gì.
- 18/10 `is_test` + cảnh báo "Bỏ bài KT": còn `npx tsx scripts/don-canh-bao-gia.mts --dry-run` → `--apply`; sweep vẫn sinh inactive_7d cho tài khoản thử.
- Độ sâu đọc (18/10): chưa có UI GV đọc `teacher_lesson_read_depth`. DT-01 `learning_events`: kiểm `select kind, count(*) … group by 1` sau vài ngày.
- DT-03 (17/10): 16 câu L10 NONE chờ thầy thêm YCCĐ mới.
- Casio (`casio-vat-ly`, 5 bài đã Hiện): còn mini-test WP-01 lặp bài luyện, kiểm `suggestedAnswer` markdown trang HS.
- Push: cron `send-notification-push` chạy; CÒN thử điện thoại thật; push nhắc hằng ngày còn VAPID + deploy `send-daily-push` + cron (`docs/PUSH-NHAC-HANG-NGAY.md`).
- HSG9 đợt 4: 6 CĐ (151/152/163/156/158/178) đã ghi DB (ẩn) — chờ thầy xem rồi bật Hiện + deploy lại.
- AVCN: 10 chương, giọng Guy — chờ thầy nghe thử rồi chốt giọng (đổi: `tao_giong_doc.py` + `cap-nhat-ly-thuyet.sh` + `deploy.sh`).
- Mạng nhện Theo chương/Cả khoá: chờ thầy xem 375px dữ liệu thật; chưa có "Theo học kì".
- "🧰 Kiểm tra hành trang" (lesson 58–67 L10): chờ đo đọc hết bài + quiz giữa bài; ổn thì `scripts/chen-hanh-trang.py` cho chương khác.
- Mã QR đề: chưa thử iPhone/Android thật; chưa QR cho CNC và `LessonImporter`.
- RP lý thuyết: chưa có khoá → `npx tsx scripts/sinh-khoa-quiz-ly-thuyet.mts` rồi `--ghi`; chưa thử nộp bằng HS.
- Chấm nhanh HSG 9: Edge Function `hsg-ai-grade` chưa deploy (cần `ANTHROPIC_API_KEY`).
- DT-16 RLS: chưa kiểm grant bảng cho `anon` và `learning_events`.
- Sách in Ch.2 L10 v6: chờ thầy chỉnh `book/src/dang-chung.json`, `tiet.json` (memory `project_thachlab_sach_in_chuong2`).
- HTML chưa có `Cache-Control: no-cache` trong `.htaccess` của `deploy.sh` — chờ thầy gật.
- Lint 0 lỗi (22/10): chờ thầy thử `/lop-hoc` trên điện thoại; bật CI gate eslint/tsc (P0 #4). `docs/RA-SOAT-DU-AN-2026-10-22-PHAN-BIEN.md`.
- 23/10 sự cố chậm (Cloudflare→origin, Disk IO): DNS đã về đám mây xám, cache RPC rank 2 phút. **30/10 đo lại** CPU + mean_ms `rank_my_status` (mốc 80 % / 272 ms); chưa xác nhận với lớp thật. Memory `project_thachlab_hosting`.

## Nội dung đang treo
- Mẹo từ khoá đợt 1: 17 bài đã đăng + CSS deploy 26/10; bảng `docs/BANG-MEO-TU-KHOA.md`; đợt 2 chờ số liệu Trả bài. 5 bài vượt 2.500 từ (l10 giai-bai-toan-dlh, chuyen-dong-nem; l11 tat-dan, song-dung, khai-niem-dien-truong) — để phiên làm video giảm chữ.
- Thí nghiệm theo khung đề thi: xong 21 bài L12. Còn: nhánh local `claude/data-tap-lessons-16-19-e5e3b0` (ruột tập) sửa theory.* từ bản cũ — merge main trước, KHÔNG đăng từ nhánh đó; `video-theo-bai.json` còn vi_tri/nhin_vao cũ cho video 12, 126.
- Quiz lý thuyết chuẩn mới: 26 bộ đã đăng + deploy 25/10; 129–131 chờ đăng lý thuyết tương tác trước rồi gán `theorySection`; 178 còn 18 câu (thiếu 2 câu Eratosthenes).
- KHTN 9 cơ học 129–131: chờ thầy duyệt ảnh, clip, PhET, topic (memory `project_thachlab_l9_co_hoc_129_131`).
- Hệ khung lý thuyết L9–L12 (90 bài, đã deploy 23/10): chưa `kiem-code` soát công thức agent thêm.
- 23 đề chưa gán lớp (mồ côi bài #99–101, #209, #239–257…): `scripts/logs/gan-lop-de-khong-suy-duoc-*.json`, chờ thầy chọn lớp. Vá tạm theo tiêu đề ở `features/exams/exam-grade.ts` gỡ được sau.
- Bài tập mẫu L12 soạn lại 12 bài (9, 11, 13–19, 125–127); kế hoạch 42 bài L10/L11 chờ duyệt (memory `project_thachlab_btm_quet_dang`).
- Bài 11 L12 Thực hành chưa ghi DB (`upload-lesson.mts content/lesson-samples/l12-thuc-hanh-cam-ung-tu/bundle.json --lesson 12 --mode replace`); 4 bài L12 sửa đường sức (11, 10, 13, 14) — kiểm `so-file-voi-db.mts` trước.
- Trùng slug lesson 126: `content/lesson-samples/l12-ung-dung-cam-ung/` là bản cũ, đăng từ đó sẽ LÙI bài.
- Bài 65 L10: 3 góp ý Hình 3/4/5 chưa sửa; 65/67 chưa xem 375px.
- Audit đáp án ngân hàng: chờ duyệt 127 câu `_can_xac_nhan` (`scripts/data/bank-answer-fixes.json`), `scripts/logs/db-sai-can-duyet.csv` (556 + 100), 8 `khong_ro` + 2 `cho_phan_xu`.
- Backfill mức độ: ~3.500 câu `difficulty` rỗng — `npx tsx scripts/backfill-question-bank-difficulty.mts 20` (**ghi thật**, sau 22h).
- Video thí nghiệm: 211 thí nghiệm / 65 bài chưa có clip.
- Rank: gắn `challenge_exam_id` cao_thu/thach_dau season 4; spec `docs/BAN-GIAO-RANK-THI-THANG-HANG-2026-10-03.md`.
- UI bài lý thuyết 5 việc CSS thầy đã duyệt (11/10, mục 1,3,4,5,6): `docs/PHAN-TICH-HIEN-THI-LY-THUYET-TUONG-TAC-2026-10-11.md` mục 5; chưa sửa code.

## CHƯA làm (roadmap)
- `/luyen-tap` lọc Lớp → Chương → Bài → YCCĐ → Dễ/TB/Khó; `/lo-trinh`; Động học 10 ≥30 câu/bài.
- Trang chương: `docs/DE-XUAT-TRANG-CHUONG-2026-10.md` (chờ chốt §7), `docs/NGHIEN-CUU-DONG-BO-TRANG-CHUONG-TRANG-BAI.md` (chờ chốt §9).
- Bài tập mẫu → ngân hàng → nút "Bài tương đương" (30/9): RPC gộp, không thêm round-trip.
- Đo độ trễ Supabase từ VN trước khi xoá project Sydney; thêm `updated_at` cho `lessons`/`lesson_items`.
- Đề xuất nghiên cứu HS 14–22 (chờ chốt mục 5): `docs/DE-XUAT-NGHIEN-CUU-HS-14-22-2026-10-11.md`.
