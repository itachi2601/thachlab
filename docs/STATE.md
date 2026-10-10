# STATE — Hiện trạng ThachLab (rút gọn 10/10/2026)

File dùng chung cho mọi phiên, **nạp mỗi phiên nên giữ dưới ~15 KB**: chỉ hiện trạng + việc ĐANG CHỜ. Xong mục nào → chuyển
nguyên văn sang `docs/STATE-archive.md` (đừng để ở đây). Bản đầy đủ trước khi rút gọn nằm ở cuối `STATE-archive.md`
(mục "Bản STATE.md trước khi rút gọn") — grep ở đó khi cần chi tiết một việc cũ.

## Hạ tầng
- Next.js App Router + TypeScript + Tailwind v4, `output: "export"` (xuất tĩnh), deploy bằng `scripts/deploy.sh` → nhánh `deploy`.
- Supabase `jgvbdbpvjdntdgzthumv`, region Singapore. Sơ đồ bảng: `docs/DATABASE.md`; RPC: `docs/DATABASE-RPC.md`.
- KaTeX 0.17; font tự host qua `next/font`; học liệu tĩnh `public/data/` sinh ở `prebuild` — sửa lý thuyết phải **deploy lại** mới lên web.
- Giao diện: nền SÁNG mặc định toàn site (11/10/2026), token ở `app/globals.css`, xem `docs/MAU-NEN-SANG.md`, thử ở `/dev/giao-dien`.

## Migration — ĐANG CHỜ (nguồn đúng: `bash scripts/run-migrations.sh --list`)
1. `20261010500000_notify_rp_thuong` — chuông "+N RP" thưởng.
2. `20261010600000_lop_hsg_vat_ly_9_duyet_tay` — lớp HSG Vật lý 9 duyệt tay; **chạy TRƯỚC khi deploy** phần `/dang-ky`.
3. `20261010700000_ta_doc_thanh_vien_lop` — TA đọc thành viên lớp (`/tro-giang/chua-bai`).
4. `20261011100000_exam_ta_preview` — gửi đề cho TA xem trước (`/tro-giang/xem-truoc`).
5. `20261010800000_an_cau_cat_cut_hien_thi` — ẩn 181 câu ngân hàng lỗi hiển thị (có bảng sao lưu).
6. `20261010150000_ta_sua_buoi_7_ngay_va_doi_anh` — TA sửa buổi 7 ngày + đổi ảnh đại diện.
7. `20261011120000_question_bank_lint_flags` — cột `lint_flags`; xong chạy `npx tsx scripts/cap-nhat-lint-flags.mts --ghi`.
- `20261011130000_bank_set_question_figure_service` — hàm `_svc` (service_role) cho `scripts/ghi-hinh-sau-duyet.mts` ghi hình Gemini đã duyệt.
- Chưa có trong `FILES` hoặc chưa rõ (kiểm `--list`/log trước khi chạy): `20261006120000_fix_grade_ngan_hang_5_de_l11`, `20261006130000_gan_lai_chu_de_5_de_l11` (129 câu đề 638/639/658/693/701), `20261006150000_quiz_live` (Đố vui lớp học `/choi`, `/tro-giang/do-vui`; chưa thử 2 điện thoại).
- Tất cả đều giờ nào chạy cũng được; rollback ở cuối file hoặc `perf/rollback/`. Sau khi chạy: `node scripts/gen-database-doc.mjs`.

## Chờ deploy / chờ kiểm
- 25 bài lý thuyết L10 (lesson 46–48, 58–79) đã ghi DB 10/10, **chưa deploy**. Main local có thể ahead origin — xem trước khi push.
- Mã QR đề (`ExamQrPanel`, `/quet-ma`): chưa thử iPhone + Android thật; chưa làm QR cho CNC và `LessonImporter`.
- RP lý thuyết: UI đã gọi `rank_theory_open/submit`; **chưa có khoá** → `npx tsx scripts/sinh-khoa-quiz-ly-thuyet.mts` (xem thử) rồi `--ghi`. Chưa chụp 375px bằng tài khoản HS, chưa thử nộp thật.
- Chấm nhanh HSG 9: Edge Function `hsg-ai-grade` chưa deploy (cần secret `DEEPSEEK_API_KEY`/`ANTHROPIC_API_KEY`).
- Nền sáng: đã deploy `9077fbd47`; còn treo việc nhỏ ở `docs/MAU-NEN-SANG.md`.
- Nhánh `perf-tach-js` (3 commit, JS theo vai) chưa vào main; chưa kiểm bằng đăng nhập thật.
- Sách in Chương 2 L10 bản v6: chờ thầy chỉnh `book/src/dang-chung.json`, `tiet.json`; `public/sach-data/*.json` v6 chưa commit/deploy (xem `docs/memory/project_thachlab_sach_in_chuong2.md`).
- Push nhắc hằng ngày: còn VAPID secrets + deploy `send-daily-push` + cron (`docs/PUSH-NHAC-HANG-NGAY.md`).
- HTML chưa có `Cache-Control: no-cache` trong `.htaccess` của `scripts/deploy.sh` — chờ thầy gật.

## Nội dung đang treo
- Bài tập mẫu L12 còn soạn lại 12 bài: 9, 11, 13–19, 125–127; kế hoạch 42 bài L10/L11 chờ thầy duyệt (`docs/memory/project_thachlab_btm_quet_dang.md`).
- Bài 11 L12 Thực hành: chưa ghi DB (`upload-lesson.mts content/lesson-samples/l12-thuc-hanh-cam-ung-tu/bundle.json --lesson 12 --mode replace`); 4 bài L12 sửa đường sức chờ `cap-nhat-ly-thuyet-hang-loat.sh l12-luc-tu-cam-ung-tu:11 l12-khai-niem-tu-truong:10 l12-cam-ung-dien-tu:13 l12-dong-dien-xoay-chieu:14` — kiểm `so-file-voi-db.mts` trước vì có thể đã đăng.
- Lỗi nội dung quiz lý thuyết L12 chưa sửa: bài 8 `summary_html` (273 K ↔ 298 K), bài 19 Xofigo Z=88, bài 10 "d gấp đôi → B còn 1/8", bài 126 mục tiêu 8 câu thực tế 7, bài 13 còn vai "Thầy". Đề cũ 209, 239–257 vẫn trong DB — kiểm `exam_results` rồi dọn tay.
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
