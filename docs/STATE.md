# STATE — Hiện trạng ThachLab (cập nhật 28/09/2026)

File này là bản mô tả hiện trạng dùng chung cho mọi phiên Claude. Cập nhật sau mỗi đợt lớn.

## Hạ tầng
- Next.js App Router + TypeScript + Tailwind v4, `output: "export"` (xuất tĩnh), deploy bằng `scripts/deploy.sh` → nhánh `deploy`.
- Supabase project `jgvbdbpvjdntdgzthumv`, **region Singapore (ap-southeast-1)** — đã chuyển từ Sydney (project cũ `fxnqgmfqdbvnjawgnsfi`), thầy xác nhận xong 29/09/2026. Đã kiểm 29/09/2026 từ sandbox cloud (chỉ đọc): build học liệu tĩnh ra 4 lớp · 22 chương · 116 bài · 256 mục; dữ liệu bài không còn URL Storage của project cũ (0), 306 URL ảnh/tệp của project mới đều trả 200. Độ trễ round-trip từ VN chưa đo lại (số ~100–150 ms trong `perf*/` là của Sydney; sandbox không ở VN nên không dùng để đo).
- Công thức: **KaTeX 0.17** (không phải MathJax).
- Font tự host qua `next/font` (Be Vietnam Pro 400/600/700/800, Inter 400/500/600, JetBrains Mono 400).
- 56 route `page.tsx`, 69 trang tĩnh khi build.
- Học liệu tĩnh: `scripts/build-content.mjs` chạy ở `prebuild`, xuất `public/data/` (catalog + 116 file bài). Sửa lý thuyết phải **deploy lại** mới lên web.

## Đã hoàn thành
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

- **Chấm nhanh HSG 9 (10/10/2026):** `20261010300000_hsg_cham_nhanh.sql` CHƯA chạy (2 bảng hsg_grade_* + seed Pre-test) → `bash scripts/run-migrations.sh`; Edge Function `hsg-ai-grade` CHƯA deploy (cần secret DEEPSEEK_API_KEY và/hoặc ANTHROPIC_API_KEY); trang `/quan-tri/hsg-cham-bai`.
- **HSG KHTN 9 đợt 1 (10/10/2026):** `20261010200000_hsg9_dot1_muc_noi_dung.sql` CHƯA chạy (tạo mục cho CĐ00/10/11/13 = bài 160/155/154/162, bật Hiện 160) → `bash scripts/run-migrations.sh`; rồi `bash scripts/dang-hsg9-dot1.sh` (ghi lý thuyết + bài tập mẫu 4 CĐ), rồi deploy. Nội dung: `content/hsg9/cd{00,10,11,13}-*/`, `scripts/data/bai-tap-mau/{154,155,160,162}.json`. (Migration `20261010100000` thực tế ĐÃ chạy.)
- **Khoá Vật lí HSG & chuyên (10/10/2026):** `20261010100000_khoa_hsg9_vat_ly_khung.sql` CHƯA chạy — thêm môn `hsg-vat-ly` + 6 chương + 17 bài (ẩn) vào KHTN 9, mục rỗng cho CĐ01/CĐ02; cuối log in `lesson_id`. Nội dung CĐ01/02: `content/hsg9/`; bản đồ: `docs/HSG9-KHUNG.md`.
- **Trang chủ HS bản thích ứng (9/10/2026, nhánh claude/zealous-cori-27xlz3):** migration `20261009100000_notify_exam_assigned.sql` CHƯA chạy — `bash scripts/run-migrations.sh` (giờ nào cũng được; rollback `perf/rollback/20261009100000_notify_exam_assigned.down.sql`). Trang chủ HS không còn bài/BTVN giao chung; **phải chạy file này TRƯỚC khi deploy**, nếu không học sinh không còn chỗ nào thấy bài kiểm tra mới giao (trang `/kiem-tra` vẫn liệt kê đề). Đổi theo mẫu thầy duyệt: khung chào gộp chuỗi ngày + RP còn thiếu + "tiến bộ so với tuần trước"; thẻ Hôm nay có luyện kỹ năng yếu (nút luyện nhanh 10 câu); hàng "Dành cho em" ở `/luyen-tap`; ô tìm bài ở `/lop-hoc`; bỏ đồng hồ ở bước đọc lý thuyết thoát phụ đạo (máy chủ vẫn đòi đủ thời gian). Chưa chụp 375px bằng tài khoản HS.
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
