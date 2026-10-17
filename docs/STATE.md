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
- `20261017150000_reset_code_manh_hon`: mã reset RS+10 hex, CHECK hạn ≤7 ngày. Chạy: `bash scripts/run-migrations.sh --only 25` (rollback cuối file).
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
- Chấm nhanh HSG 9: Edge Function `hsg-ai-grade` chưa deploy (cần secret `DEEPSEEK_API_KEY`/`ANTHROPIC_API_KEY`).
- Nền sáng: đã deploy `9077fbd47`; còn treo việc nhỏ ở `docs/MAU-NEN-SANG.md`.
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
- Đề xuất từ nghiên cứu HS 14–22 (11/10/2026, chờ thầy chốt mục 5): `docs/DE-XUAT-NGHIEN-CUU-HS-14-22-2026-10-11.md` — đo mùa 1 trước, fading theo mastery, đề dài làm theo phần, PhET gắn YCCĐ.

- 11/10/2026 · **UI bài lý thuyết, 5 việc CSS nhỏ thầy đã duyệt (mục 1,3,4,5,6)** — chỗ sửa + cách làm ở `docs/PHAN-TICH-HIEN-THI-LY-THUYET-TUONG-TAC-2026-10-11.md` mục 5; chưa sửa code.

## 12/10/2026 — KHTN 9 cơ học 129–131 (chưa đăng)
- Soạn + kiểm chéo xong, chờ thầy duyệt ảnh xem thử, chọn clip, bấm thử PhET, gắn topic; chi tiết `docs/memory/project_thachlab_l9_co_hoc_129_131.md`. Skill mới `.claude/skills/phet/` — Mac: `git -C ~/Projects/thachlab pull && bash ~/Projects/thachlab/scripts/cai-skill.sh`.
