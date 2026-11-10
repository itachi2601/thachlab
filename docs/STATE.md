# STATE — Hiện trạng ThachLab (rút gọn 30/10/2026)

File dùng chung, **nạp mỗi phiên — giữ dưới ~15 KB**: chỉ hiện trạng + việc ĐANG CHỜ, mỗi việc 1–2 dòng, chi tiết để ở
`docs/memory/project_*.md`. Xong mục nào → chuyển nguyên văn sang `docs/STATE-archive.md`. Bản đầy đủ trước mỗi lần rút gọn
nằm ở `STATE-archive.md` (mục "Bản STATE.md trước khi rút gọn …", mới nhất 30/10/2026) — grep ở đó khi cần chi tiết.

## Hạ tầng
- Next.js App Router + TS + Tailwind v4, `output: "export"`, deploy `scripts/deploy.sh` → nhánh `deploy`.
- Supabase `jgvbdbpvjdntdgzthumv` (Singapore, gói PRO từ 23/10, compute t3a.small). Sơ đồ: `docs/DATABASE.md`, RPC: `docs/DATABASE-RPC.md`.
- KaTeX 0.17; học liệu tĩnh `public/data/` sinh ở `prebuild` CHỈ cho bài xem thử (`lessons.is_preview`: 2, 20, 46) — bài khác HS đọc thẳng DB, ghi `cap-nhat-ly-thuyet.sh` là lên ngay, chỉ deploy khi đổi CSS/code (kiểm 1/11 22h30).
- Nền SÁNG mặc định (11/10), token `app/globals.css`, xem `docs/MAU-NEN-SANG.md`, thử `/dev/giao-dien`.

## Migration — ĐANG CHỜ (nguồn đúng: `bash scripts/run-migrations.sh --list` + `scripts/logs/`)
- `20261109120000_shcn_lesson_key` (9/11): cột bài đọc tuần SHCN; chạy TRƯỚC khi deploy trang `/sinh-hoat` + editor GVCN. Lúc nào cũng được.
- `20261028100000_bai_tap_ngay`: migration ĐÃ CHẠY (kiểm DB 30/10); còn `npx tsx scripts/tao-bai-tap-ngay-hsg9.mts --yes` + deploy `components/review/ClassRoster.tsx` (chưa rõ đã làm).
- `20261006120000_fix_grade_ngan_hang_5_de_l11`, `20261006130000_gan_lai_chu_de_5_de_l11`: chưa có trong `FILES`/chưa rõ.
- P0 #1 chặng 3 (thu quyền `exams.questions`): chờ RPC riêng cho CNC (`services/cnc-exam-bank.ts`); sau 22h. Còn lỗ `practice_sessions.score`, `question_bank` qua policy exit-quiz (chặng 4).
- Sau mỗi migration: `node scripts/gen-database-doc.mjs`.

## Chờ deploy / chờ thử thật
- Dashboard GV CNC: tab "Buổi học" theo nhịp lớp đảo ngược (10/11, `TeacherFlipBoard`, xem thử `/dev/cnc-bang-buoi`) — ĐÃ DEPLOY 10/11 từ commit c9eb40921 (kèm `dac7911f7` đáp án sau 2 lượt + `d72917876` cổng G tính `final`; CHƯA gồm CTTC thanh đáy `db053cc45`). Mở được bằng tài khoản thầy với lớp CĐ CK 24A; chưa thử trong một buổi dạy thật.
- 10/11: `20261109140000_de_danh_gia_mo_dap_an_sau_2_luot` ĐÃ CHẠY (đáp án mở sau 2 lượt, hàm `get_exam_wrong_notes`); chờ deploy `ExamDoneLocked` để hiện "vì sao sai" + thử 375px bằng tài khoản HS làm đề 1297 (lớp 11). Script `run-migrations.sh` trong worktree lỗi IPv6 → chạy `supabase db query --linked -f` từ thư mục chính.
- 30/10 · Công TA hằng tháng tự chạy (cron `ta-month-cycle`): báo 19h cuối tháng → mở ngày 1–3 → khoá, báo thầy chốt; khiếu nại ở /tro-giang. T10 đang mở, 1/11 tự kéo hạn tới 23:59 03/11. Chưa thử bằng tài khoản TA thật. Thấy lạ: `.claude/worktrees/deploy-tree` có `app/globals.css` sửa dở chưa commit, HEAD kẹt ở ac5a22baf.
- Ôn tập theo chặng + Tự học ở nhà + "Việc hôm nay": đã deploy, chưa thử bằng HS thật/tivi; thông báo buổi tạo MỚI chưa thử (memory `project_thachlab_on_tap_theo_chang`).
- Ngân hàng→Luyện tập chặng 0: đã deploy; còn gắn `lint_flags` cho 127 câu `_can_xac_nhan`, thử ghi `bank_id` bằng HS thật (`docs/BAO-CAO-NGAN-HANG-THEO-BAI-2026-10-24.md`).
- Quiz lý thuyết: 129–131 chờ đăng lý thuyết tương tác trước; 178 còn 18 câu.
- Hình OpenStax L10/L11 (nhánh `claude/distracted-gauss-2d45d4`, 20 bài): CHƯA đăng DB/deploy ảnh; L12 chờ thầy xem 375 px (`docs/ra-soat/hinh-openstax-*.md`).
- Làm bài "tự nhảy câu" (24/10): 4 sửa đã deploy, chờ HS phản hồi.
- Push thông báo: đã chạy cron; chưa thử điện thoại thật. Push nhắc hằng ngày: còn VAPID + `send-daily-push` (`docs/PUSH-NHAC-HANG-NGAY.md`).
- AVCN: chờ thầy nghe thử giọng Guy/Andrew/Brian.
- Mạng nhện Theo chương: chờ thầy xem 375 px; chưa có "Theo học kì".
- Kiểm tra hành trang (L10 ch.3, bài 58–67): chờ đo tỉ lệ đọc hết + đúng quiz.
- Mã QR đề: chưa thử iPhone/Android thật; chưa có QR cho CNC, `LessonImporter`.
- RP lý thuyết: chưa có khoá → `sinh-khoa-quiz-ly-thuyet.mts` rồi `--ghi`; chưa thử nộp thật.
- Độ sâu đọc: chưa có UI GV đọc `teacher_lesson_read_depth`. DT-01: kiểm `learning_events` có dữ liệu chưa.
- DT-16 RLS: chưa kiểm grant cho `anon` và `learning_events`.
- Casio: mini-test WP-01 lặp bài luyện, kiểm `suggestedAnswer` markdown trên trang HS.
- Sự cố 23/10 (CF chậm, Disk IO): chưa xác nhận lớp thật; 30/10 đo lại CPU + mean_ms `rank_my_status` (mốc 80 % / 272 ms).
- Lint 0 lỗi: thầy thử `/lop-hoc` trên điện thoại; bật CI gate eslint/tsc (P0 #4).
- Sách in Ch.2 L10 v6: chờ thầy chỉnh `book/src/dang-chung.json`, `tiet.json`.
- `.htaccess` thêm `Cache-Control: no-cache` cho HTML — chờ thầy gật.

## Nội dung đang treo
- 5/11 · Giải cùng hình: Đ1–Đ8 đã đăng DB + deploy (51 bài); Đ9 (KHTN 9 + HSG 9, 25 bài) đã vào main, CHƯA HS ảo/CHƯA đăng DB; ~20 nhánh `claude/*` >4 ngày chưa vào main chờ thầy chỉ (memory `project_thachlab_giai_cung_hinh`).
- 7/11 · BTM "một dạng — một hình": repo xong 97/97; DB đã đăng 51, CHƯA đăng 46 (danh sách: `docs/MOT-DANG-MOT-HINH.md` mục Trạng thái 7/11) — chờ soát ảnh + thầy duyệt → publish → deploy.
- Mẹo từ khoá đợt 2 chờ số liệu Trả bài; 5 bài >2.500 từ để phiên video giảm chữ.
- Thí nghiệm L12: nhánh `claude/data-tap-lessons-16-19-e5e3b0` KHÔNG đăng từ đó (phải merge main trước); `video-theo-bai.json` còn vị trí cũ video id 12, 126.
- Chặng B L11 Dao động: 7 clip bài 21, 22, 23, 24, 26 đã đăng DB 1/11 12h23, thầy duyệt lô 1/11 tối, kiểm dry-run 22h40 khớp DB; chưa thử HS thật.
- Motion graphic chặng A: code + DB xong (23/23 hộp khung L12 trên DB, kiểm 6/11); chờ có lượt chọn đầu tiên ở `lesson_clip_choices` để đo % đúng (mục 5) — `docs/KE-HOACH-MOTION-GRAPHIC.md`.
- Motion graphic chặng D (7/11): thầy duyệt; clip ôn L12 Ch.3 (89 s) đã lên Storage (`content/phu-dao/clip-on/on-l12-ch3.json`) và hiện thẻ "Ôn nhanh" ở `ReviewStudent` (buổi ở nhà + chờ chặng 1; khớp chữ "từ trường/lực từ…" trong tên buổi, `lib/clip-on-tap.ts`). CHƯA deploy, chưa thấy 375px bằng tài khoản HS, chưa có sự kiện đo phát/xem (cách đo ở `docs/KE-HOACH-MOTION-GRAPHIC.md` mục Chặng D).
- Motion graphic chặng C (1/11): 5 clip bẫy L12 Ch.3 (`content/phu-dao/clip-bay/`, khuôn `clips/bay_chung.py`) hiện trong thẻ mục phụ đạo `/lop-hoc/ket-qua` (thử `/dev/clip-bay`); clip 01 chèn hộp Bẫy 3 bài Lực từ, thầy duyệt 1/11, ĐÃ DEPLOY 1/11 17h40 (thẻ phụ đạo có clip); lý thuyết lesson 11 (item 52) đã ghi DB 22h05, đã kiểm DB + deploy lại 22h25 1/11; đo 15/11 bằng `scripts/sql/do-clip-bay-phu-dao.sql` (mốc D đặt 2026-11-01 17:40+07).
- 23 đề chưa gán lớp: `scripts/logs/gan-lop-de-khong-suy-duoc-*.json`; 16 câu L10 YCCĐ NONE chờ thầy.
- Bài tập mẫu L12 soạn lại 12 bài (9, 11, 13–19, 125–127); kế hoạch 42 bài L10/L11 chờ duyệt.
- Bài 11 L12 Thực hành chưa ghi DB; 4 bài L12 sửa đường sức — kiểm `so-file-voi-db.mts` trước.
- Trùng slug lesson 126: `content/lesson-samples/l12-ung-dung-cam-ung/` là bản cũ, đừng đăng từ đó.
- Bài 65 L10: 3 góp ý Hình 3/4/5; bài 65/67 chưa xem 375 px.
- Audit đáp án ngân hàng: 127 câu `_can_xac_nhan`, `scripts/logs/db-sai-can-duyet.csv` (656 câu).
- Backfill mức độ: ~3.500 câu rỗng — `backfill-question-bank-difficulty.mts 20` (**ghi thật**).
- Clip tự dựng L9 nhóm C (5/11): 8 clip, 6 bài (lesson 87, 89, 91, 129–131) thầy duyệt, ĐÃ ĐĂNG DB 23h35 5/11 (--chi-video, kiểm DB đủ 8 clip); chưa thử HS thật — sổ `content/thi-nghiem/so-clip-anh-dong.md`.
- Clip L10 lô 1/11 (8 clip: tdvt1, giatoc1, dog3, trondeu3, biendang3, saiso2, antoan1/2 — lesson 50, 53, 56, 76, 78, 48, 47) ĐÃ ĐĂNG DB 6/11 ~23h55 (`--chi-video`, kiểm DB 8/8 có khung); giữ nguyên dòng Quan sát như L9; chưa thử HS thật.
- Video thí nghiệm: 211 thí nghiệm / 65 bài chưa có clip.
- Clip tự dựng Ch.4 L11: 6 clip đã đăng DB (bài 41, 42, 44, 45 ngày 31/10; bài 43 nguondien1/2 + 4 chỉ số tspan 14 ngày 1/11 22h30, sao lưu `scripts/logs/ly-thuyet-bai43-backup-1793546652365.json`); chưa thử HS thật.
- Rank mùa 2 (5/11): 4 mùa theo khối 02/11–17/01 đang chạy (id 26–29); chưa thử bằng HS thật — memory `project_thachlab_rank_system`.
- Rank: gắn `challenge_exam_id` season 4; spec `docs/BAN-GIAO-RANK-THI-THANG-HANG-2026-10-03.md`.
- KHTN 9 cơ học 129–131: chờ thầy duyệt (memory `project_thachlab_l9_co_hoc_129_131`).
- **L10 Bài 6 Thực hành đo tốc độ (lesson 51) soạn lại 10/11**: lý thuyết + bài tập mẫu 4 dạng + quiz 20 câu, đã kiểm chéo, chờ thầy duyệt rồi đăng DB (lý thuyết trước, quiz sau) — `content/lesson-samples/l10-thuc-hanh-do-toc-do/ra-soat.md`.

## CHƯA làm (roadmap)
- `/luyen-tap` lọc Lớp → Chương → Bài → YCCĐ → mức; `/lo-trinh`; Động học 10 ≥30 câu/bài.
- Trang chương: `docs/DE-XUAT-TRANG-CHUONG-2026-10.md` (§7), `docs/NGHIEN-CUU-DONG-BO-TRANG-CHUONG-TRANG-BAI.md` (§9).
- Bài tập mẫu → ngân hàng → nút "Bài tương đương" (RPC gộp).
- Đo độ trễ Supabase từ VN trước khi xoá project Sydney; cột `updated_at` cho `lessons`/`lesson_items`.
- Đề xuất nghiên cứu HS 14–22 (chờ chốt mục 5): `docs/DE-XUAT-NGHIEN-CUU-HS-14-22-2026-10-11.md`.
- 5 việc CSS bài lý thuyết đã duyệt (mục 1,3,4,5,6): `docs/PHAN-TICH-HIEN-THI-LY-THUYET-TUONG-TAC-2026-10-11.md` §5.
- "Một dạng — một hình" L12+L11 (8/11): 27 bài (L12 3 4 6 7 8 9 15 16 17 19; L11 20–22 24 25 28 30–36 39 40 43 44) đã lên DB + deploy; đã kiểm live 375px (43, 33); 7 chỗ lệch nhỏ cần sửa component ở `docs/MOT-DANG-MOT-HINH.md` mục 8/11 L12+L11.
- "Một dạng — một hình" L10+KHTN9 (8/11): 19 bài (L10 45–53, 62–79 chọn lọc; KHTN9 156) đã lên DB + deploy; còn treo ở `docs/MOT-DANG-MOT-HINH.md` mục 8/11.
