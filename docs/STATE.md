# STATE — Hiện trạng ThachLab (rút gọn 30/10/2026)

File dùng chung, **nạp mỗi phiên — giữ dưới ~15 KB**: chỉ hiện trạng + việc ĐANG CHỜ, mỗi việc 1–2 dòng, chi tiết để ở
`docs/memory/project_*.md`. Xong mục nào → chuyển nguyên văn sang `docs/STATE-archive.md`. Bản đầy đủ trước mỗi lần rút gọn
nằm ở `STATE-archive.md` (mục "Bản STATE.md trước khi rút gọn …", mới nhất 30/10/2026) — grep ở đó khi cần chi tiết.

## Hạ tầng
- Next.js App Router + TS + Tailwind v4, `output: "export"`, deploy `scripts/deploy.sh` → nhánh `deploy`.
- Supabase `jgvbdbpvjdntdgzthumv` (Singapore, gói PRO từ 23/10, compute t3a.small). Sơ đồ: `docs/DATABASE.md`, RPC: `docs/DATABASE-RPC.md`.
- KaTeX 0.17; học liệu tĩnh `public/data/` sinh ở `prebuild` — sửa lý thuyết phải **deploy lại** mới lên web.
- Nền SÁNG mặc định (11/10), token `app/globals.css`, xem `docs/MAU-NEN-SANG.md`, thử `/dev/giao-dien`.

## Migration — ĐANG CHỜ (nguồn đúng: `bash scripts/run-migrations.sh --list` + `scripts/logs/`)
- `20261028100000_bai_tap_ngay`: migration ĐÃ CHẠY (kiểm DB 30/10); còn `npx tsx scripts/tao-bai-tap-ngay-hsg9.mts --yes` + deploy `components/review/ClassRoster.tsx` (chưa rõ đã làm).
- `20261006120000_fix_grade_ngan_hang_5_de_l11`, `20261006130000_gan_lai_chu_de_5_de_l11`: chưa có trong `FILES`/chưa rõ.
- `20261018170000_canh_bao_bo_bai_kt…`: chạy TRƯỚC deploy (code select `is_test`), rồi `don-canh-bao-gia.mts --dry-run` → `--apply`.
- P0 #1 chặng 3 (thu quyền `exams.questions`): chờ RPC riêng cho CNC (`services/cnc-exam-bank.ts`); sau 22h. Còn lỗ `practice_sessions.score`, `question_bank` qua policy exit-quiz (chặng 4).
- Sau mỗi migration: `node scripts/gen-database-doc.mjs`.

## Chờ deploy / chờ thử thật
- 30/10 · Công TA hằng tháng tự chạy (cron `ta-month-cycle`): báo 19h cuối tháng → mở ngày 1–3 → khoá, báo thầy chốt; khiếu nại ở /tro-giang. T10 đang mở, 1/11 tự kéo hạn tới 23:59 03/11. Chưa thử bằng tài khoản TA thật. Thấy lạ: `.claude/worktrees/deploy-tree` có `app/globals.css` sửa dở chưa commit, HEAD kẹt ở ac5a22baf.
- Ôn tập theo chặng + Tự học ở nhà + "Việc hôm nay": đã deploy, chưa thử bằng HS thật/tivi; thông báo buổi tạo MỚI chưa thử (memory `project_thachlab_on_tap_theo_chang`).
- Ngân hàng→Luyện tập chặng 0: đã deploy; còn gắn `lint_flags` cho 127 câu `_can_xac_nhan`, thử ghi `bank_id` bằng HS thật (`docs/BAO-CAO-NGAN-HANG-THEO-BAI-2026-10-24.md`).
- Quiz lý thuyết đợt 2 (73 bài, exam 1102–1174) đã ghi DB, CHƯA DEPLOY. 129–131 chờ đăng lý thuyết tương tác trước; 178 còn 18 câu.
- Hình OpenStax L10/L11 (nhánh `claude/distracted-gauss-2d45d4`, 20 bài): CHƯA đăng DB/deploy ảnh; L12 chờ thầy xem 375 px (`docs/ra-soat/hinh-openstax-*.md`).
- L10 8 bài nâng chỉ số SVG lên 14 + B34 H2 đầu V (31/10, đã vào main): CHƯA đăng DB — gộp đợt đăng sau: `cap-nhat-ly-thuyet.sh` B4, 5, 9, 12, 25, 26, 27, 34 (lesson_id suy 45+n: 49, 50, 54, 57, 70, 71, 72, 79; dry-run kiểm tiêu đề).
- Làm bài "tự nhảy câu" (24/10): 4 sửa đã deploy, chờ HS phản hồi.
- Push thông báo: đã chạy cron; chưa thử điện thoại thật. Push nhắc hằng ngày: còn VAPID + `send-daily-push` (`docs/PUSH-NHAC-HANG-NGAY.md`).
- HSG9 đợt 4 (6 CĐ ẩn): chờ thầy xem rồi bật Hiện + deploy (memory `project_thachlab_khoa_hsg9_vat_ly`).
- AVCN: chờ thầy nghe thử giọng Guy/Andrew/Brian.
- Mạng nhện Theo chương: chờ thầy xem 375 px; chưa có "Theo học kì".
- Kiểm tra hành trang (L10 ch.3, bài 58–67): chờ đo tỉ lệ đọc hết + đúng quiz.
- Mã QR đề: chưa thử iPhone/Android thật; chưa có QR cho CNC, `LessonImporter`.
- RP lý thuyết: chưa có khoá → `sinh-khoa-quiz-ly-thuyet.mts` rồi `--ghi`; chưa thử nộp thật.
- `hsg-ai-grade` chưa deploy (cần `ANTHROPIC_API_KEY`).
- Độ sâu đọc: chưa có UI GV đọc `teacher_lesson_read_depth`. DT-01: kiểm `learning_events` có dữ liệu chưa.
- DT-16 RLS: chưa kiểm grant cho `anon` và `learning_events`.
- Casio: mini-test WP-01 lặp bài luyện, kiểm `suggestedAnswer` markdown trên trang HS.
- Sự cố 23/10 (CF chậm, Disk IO): chưa xác nhận lớp thật; 30/10 đo lại CPU + mean_ms `rank_my_status` (mốc 80 % / 272 ms).
- Lint 0 lỗi: thầy thử `/lop-hoc` trên điện thoại; bật CI gate eslint/tsc (P0 #4).
- Sách in Ch.2 L10 v6: chờ thầy chỉnh `book/src/dang-chung.json`, `tiet.json`.
- `.htaccess` thêm `Cache-Control: no-cache` cho HTML — chờ thầy gật.

## Nội dung đang treo
- Mẹo từ khoá đợt 2 chờ số liệu Trả bài; 5 bài >2.500 từ để phiên video giảm chữ.
- Thí nghiệm L12: nhánh `claude/data-tap-lessons-16-19-e5e3b0` KHÔNG đăng từ đó (phải merge main trước); `video-theo-bai.json` còn vị trí cũ video id 12, 126.
- Motion graphic chặng A (23 clip L12, CSS `tl-video--doc` chưa deploy) chờ thầy chốt — `docs/KE-HOACH-MOTION-GRAPHIC.md`.
- 23 đề chưa gán lớp: `scripts/logs/gan-lop-de-khong-suy-duoc-*.json`; 16 câu L10 YCCĐ NONE chờ thầy.
- Bài tập mẫu L12 soạn lại 12 bài (9, 11, 13–19, 125–127); kế hoạch 42 bài L10/L11 chờ duyệt.
- Bài 11 L12 Thực hành chưa ghi DB; 4 bài L12 sửa đường sức — kiểm `so-file-voi-db.mts` trước.
- Trùng slug lesson 126: `content/lesson-samples/l12-ung-dung-cam-ung/` là bản cũ, đừng đăng từ đó.
- Bài 65 L10: 3 góp ý Hình 3/4/5; bài 65/67 chưa xem 375 px.
- Audit đáp án ngân hàng: 127 câu `_can_xac_nhan`, `scripts/logs/db-sai-can-duyet.csv` (656 câu).
- Backfill mức độ: ~3.500 câu rỗng — `backfill-question-bank-difficulty.mts 20` (**ghi thật**).
- Video thí nghiệm: 211 thí nghiệm / 65 bài chưa có clip.
- Rank: gắn `challenge_exam_id` season 4; spec `docs/BAN-GIAO-RANK-THI-THANG-HANG-2026-10-03.md`.
- KHTN 9 cơ học 129–131: chờ thầy duyệt (memory `project_thachlab_l9_co_hoc_129_131`).

## CHƯA làm (roadmap)
- `/luyen-tap` lọc Lớp → Chương → Bài → YCCĐ → mức; `/lo-trinh`; Động học 10 ≥30 câu/bài.
- Trang chương: `docs/DE-XUAT-TRANG-CHUONG-2026-10.md` (§7), `docs/NGHIEN-CUU-DONG-BO-TRANG-CHUONG-TRANG-BAI.md` (§9).
- Bài tập mẫu → ngân hàng → nút "Bài tương đương" (RPC gộp).
- Đo độ trễ Supabase từ VN trước khi xoá project Sydney; cột `updated_at` cho `lessons`/`lesson_items`.
- Đề xuất nghiên cứu HS 14–22 (chờ chốt mục 5): `docs/DE-XUAT-NGHIEN-CUU-HS-14-22-2026-10-11.md`.
- 5 việc CSS bài lý thuyết đã duyệt (mục 1,3,4,5,6): `docs/PHAN-TICH-HIEN-THI-LY-THUYET-TUONG-TAC-2026-10-11.md` §5.
