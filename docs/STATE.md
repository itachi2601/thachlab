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

## Migration — ĐANG CHỜ

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
- Đã chạy: `20260930160000_exit_quiz_bank_children.sql` 30/9/2026 17:15 (xem STATE-archive.md). Đợt GĐ 1b (5 file `20260930110000`–`150000`) đã chạy 30/9/2026 16:07 (xem STATE-archive.md).
  Đã cấp bù thành tích `tien_bo_tuan` cho 7 em từng nhận RP tiến bộ (30/9/2026, chạy tay, kiểm lại = 0 em thiếu).
- **Bộ Kiểm tra nhanh lý thuyết (không phải migration, không đổi schema)** — 20 file JSON lớp 12 chờ đăng
  (đã kiểm chéo + validate, đã gắn YCCĐ + mức độ 1/10/2026 — sẵn sàng đăng): `scripts/data/theory-quiz/{2,3,4,5,6,7,8,9,10,11,13,14,15,16,17,18,19,125,126,127}.json`.
  Thầy chạy trên Mac, theo thứ tự:
  `npx tsx scripts/export-question-topics.mts` → `npx tsx scripts/publish-theory-quiz.mts --lesson 2 --lesson 3 … --lesson 127` (liệt kê đủ 20 id)
  (thử trước bằng `--dry-run`) → `bash scripts/deploy.sh`. Chưa đăng nên các mục lý thuyết này chưa có `exam_ids`.
  Rollback: gỡ `exam_ids`/`quiz_min_correct` của mục đó + xoá exam mới tạo. Skill `soan-quiz-ly-thuyet`
  (`.claude/skills/soan-quiz-ly-thuyet/`) cần đồng bộ sang 2 bản còn lại (Library plugin + `~/.codex`) trên Mac: `bash scripts/sync-skill.sh`.
Mọi file trong `supabase/migrations/` tính tới 30/09/2026 đã chạy trên production.
Lịch sử các đợt đã chạy: `docs/STATE-archive.md`. Sơ đồ bảng hiện tại: `docs/DATABASE.md`
(sinh lại bằng `node scripts/gen-database-doc.mjs` sau mỗi đợt migration).

## Việc tay còn lại
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

(KaTeX/framer-motion đã xác nhận ngoài JS ban đầu từ đợt 2; cache header ảnh đã làm ở đợt 4 —
xem mục "Đợt tối ưu tải số 4" ở trên.)
