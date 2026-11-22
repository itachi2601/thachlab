# STATE — Hiện trạng ThachLab (rút gọn 18/11/2026)

Nạp mỗi phiên, giữ dưới 15 KB: hiện trạng + ĐANG CHỜ (1–2 dòng/việc). Xong → nguyên văn sang `docs/STATE-archive.md`; chi tiết ở `docs/memory/project_*.md`.

## Hạ tầng
- Next.js App Router + TS + Tailwind v4, `output: "export"`, deploy `scripts/deploy.sh` → nhánh `deploy`.
- Supabase `jgvbdbpvjdntdgzthumv` (Singapore, gói PRO). Sơ đồ: `docs/DATABASE.md`, RPC: `docs/DATABASE-RPC.md`.
- KaTeX 0.17; học liệu tĩnh `public/data/` sinh ở `prebuild` CHỈ cho bài xem thử (`lessons.is_preview`: 2, 20, 46) — bài khác HS đọc thẳng DB, ghi `cap-nhat-ly-thuyet.sh` là lên ngay, chỉ deploy khi đổi CSS/code.
- Nền SÁNG mặc định (11/10): token `app/globals.css`, `docs/MAU-NEN-SANG.md`.

## Migration — ĐANG CHỜ (nguồn đúng: `bash scripts/run-migrations.sh --list` + `scripts/logs/`; sau migration chạy `node scripts/gen-database-doc.mjs`)
- **AI sửa lỗi → sửa luôn câu gốc ngân hàng (16/11)**: `20261116120000_bank_apply_question_fix` ĐÃ CHẠY 16/11 (hàm tồn tại, chặn người không phải giáo viên). Client đã sửa (ExamSection + services/ai-check-exam) nhưng chưa vào main/deploy; chưa thử bấm AI sửa thật.
- **Điểm học phần CNC (14/11)**: `20261114120000_cnc_diem_hoc_phan` ĐÃ CHẠY (bảng `cnc_grades`, RLS SV chỉ đọc dòng mình); 28 SV lớp 10 đã nạp điểm Tiện + gửi thông báo trỏ `/lop-hoc/cnc/bang-diem/`. Trang bảng điểm ĐÃ DEPLOY 18/11 (thachlab.id.vn/lop-hoc/cnc/bang-diem/ trả 200). Điểm Phay chưa có (nạp bằng `scripts/gui-diem-thi-tien-cnc.mts` làm mẫu, module 'phay').
- Bài tập ngày 28/10 (đề 1289–1293): chưa rõ đã deploy `ClassRoster.tsx`.
- L11 5 đề 638/639/658/693/701: `fix_grade` ĐÃ ÁP (còn 1 câu 684939 grade 10). `20261006130000_gan_lai_chu_de_5_de_l11` CHƯA ÁP (123/129 câu còn lệch chủ đề; 94 câu mang chủ đề Newton/Hooke) và KHÔNG chạy trực tiếp được: 14/11 bị timeout 57014, trigger `trg_bank_tags_to_exams` → `sync_exam_to_bank` chạy lại cả đề; đã rollback sạch. Làm lại theo mẫu `lib/sua-dinh-dang.ts` (tắt `trg_exams_sync_bank`, sửa cả bank lẫn `exams.questions`, sau 22h).
- L11 đề 701/638: đã vá tên chủ đề 15/11 (chi tiết ở STATE-archive). Treo: câu 16, 28 đề 701 không có dòng bank; câu chủ đề rỗng chờ thầy.
- **Vá bảo mật 11/11**: 3 migration ĐÃ CHẠY (bước 2 lúc 12/11 06:40; `20261112070000` kiểm đầu vào điểm CNC lúc 12/11 08:15), client đã deploy; 12/11 đã bấm thử bằng tài khoản admin (sửa đề THPT/CTTC, `/lop-hoc/cnc`, dashboard GV: mọi request 200). Chưa thử bằng tài khoản HS/TA thật; chưa bấm nút nhắc làm bài. Script đăng nhập tài khoản thường mà đọc `exams.questions` phải đổi sang `exams_staff`.
- **Quiz trắc nghiệm CNC chấm ở server (12/11)**: cả 2 bước ĐÃ CHẠY (bước 2 lúc 08:52), client deploy 12/11 ~08:50 (bản 11/11 19:01 = commit 874bef7f6 + 6 file vá bảo mật). Chưa thử bằng tài khoản SV thật (admin không ghi điểm) → buổi CNC tới xem `cnc_learning_records` có dòng mới của 15 bài có ngân hàng. Đáp án vẫn nằm trong `get_cnc_quiz_banks` (quiz cho xem đáp án và làm lại không giới hạn).
- Còn lỗ cần chấm ở server (đổi client, thầy quyết): bài CNC chấm ở máy (dịch lệnh trả lời ngắn, điền khuyết, viết chương trình, checklist — đáp án nằm trong mã client), `practice_sessions.score`, `question_bank` lộ đáp án qua policy exit-quiz/diagnostic (chặng 4); mật khẩu mặc định = mã số HS.
- **GitHub 12/11 06:46**: có ruleset `bao-ve-main-deploy` (chỉ admin cập nhật `main`/`deploy`) → workflow `gop-claude-vao-main.yml` KHÔNG đẩy được vào main nữa (GH013). Phiên Mac: `git push origin HEAD:main` (fast-forward, sau khi `git merge origin/main`); phiên cloud: không tự vào main được, chờ thầy quyết. Repo vẫn công khai, `nhmkct1`/`zKdKaidO` vẫn quyền ghi.
- **Sức khỏe › Dinh dưỡng `/suc-khoe/dinh-duong` (19/11)**: `20261119090000_dinh_duong` ĐÃ CHẠY 19/11 ~08:05 (bảng `nutrition_days`, `nutrition_profile`, RLS chủ tài khoản); kcal Mifflin–St Jeor + nhật ký món + chỉnh theo xu hướng cân tuần (`lib/suc-khoe/dinh-duong.ts`). Thầy cần điền năm sinh lần đầu.
- **Sức khỏe › Kiểu build (19/11)**: migration `20261119120000_body_measurements_neck_wrist` CHỜ CHẠY (thêm `neck_cm`, `wrist_cm`, chỉ thêm cột, chạy lúc nào cũng được; chưa chạy thì app vẫn lưu/đọc số đo cũ, chỉ không lưu cổ/cổ tay). Code ở `lib/suc-khoe/build.ts`, `components/suc-khoe/KieuBuild.tsx`; chưa deploy.
- **Mục Sức khỏe `/suc-khoe` (19/11)**: đường vào + tập luyện chuyển về `/suc-khoe/tap-luyen` (địa chỉ cũ tự chuyển); chỉ admin/giảng viên (`lib/suc-khoe/modules.ts`). Đã deploy 19/11 ~0h từ worktree tạm (main 9eda42b96 + file Sức khỏe) để KHÔNG kéo trang bài học RPC gộp `get_lesson_page_student` lên site — deploy main lần sau phải chạy migration 20261118150000 trước. **Ứng dụng tập (18/11)**: `20261118120000_tap_luyen` ĐÃ CHẠY 18/11 ~22:50 (bảng `workout_logs`, `body_measurements`, RLS chủ tài khoản, anon không đọc; log `scripts/logs/*tap_luyen.log` ở checkout chính). Đã deploy 18/11 ~23:00, mở được trên site bằng tài khoản thầy; chưa ghi buổi tập thật. Chương trình A/B/C ở `lib/tap-luyen/chuong-trinh.ts`.
- **Sức khỏe mở cho HS/SV (19/11)**: `student` vào được `/suc-khoe` (THPT + CTTC), chương trình riêng không dụng cụ `PROGRAM_HS` (3 buổi ~30′), không thấy Số đo/ngực–eo; link ở `/tai-khoan/them`; localStorage tách theo tài khoản. Chưa deploy, chưa thử bằng tài khoản HS thật.
- **19/11 07:15**: ĐÃ CHẠY `20261118150000_get_lesson_page_student` + `20261118200000_review_stage_exams` (log `scripts/logs/20261119_*.log` ở checkout chính), deploy main fd5c6342f lúc ~07:20. Chưa thử trang bài + buổi ôn bằng tài khoản HS thật.
- Sau mỗi migration: `node scripts/gen-database-doc.mjs`.

## Chờ deploy / chờ thử thật
- Dashboard GV CNC: tab "Buổi học" theo nhịp lớp đảo ngược (10/11, `TeacherFlipBoard`, xem thử `/dev/cnc-bang-buoi`) — ĐÃ DEPLOY 10/11 từ commit c9eb40921 (kèm `dac7911f7` đáp án sau 2 lượt + `d72917876` cổng G tính `final`; CHƯA gồm CTTC thanh đáy `db053cc45`). Mở được bằng tài khoản thầy với lớp CĐ CK 24A; chưa thử trong một buổi dạy thật.
- `ExamDoneLocked` ĐÃ DEPLOY 18/11 (migration đáp án sau 2 lượt chạy 10/11, chi tiết STATE-archive); còn thử bằng HS thật (đề 1297, lớp 11, 375px).
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
- Sách in Ch.2 L10: bản 7 (134 trang, dựng từ DB 10/11) chờ thầy xem + chỉnh `book/sach/l10-ch2-dong-hoc.json` (Dạng chung, vạch tiết); `public/sach-data` bản 7 CHƯA commit/deploy; chặng C–E theo `docs/THIET-KE-SKILL-SACH-DONG-BO.md` chưa làm.
- Sách in Ch.3 L10 (Động lực học): bản 1 (144 trang, 10/11) chờ thầy xem; `public/sach-data` ch3 CHƯA commit/deploy (sinh lại bằng `make.py l10-ch3-dong-luc-hoc`).
- Ruột tập VL10 Ch.4 (bài 23–27): bản 1, 60 trang (`bash scripts/ruot-tap/dung-l10-chuong4.sh`), đã sửa theo HS ảo; Bài tương tự tr.8–9 = bài về nhà giải vào vở (thầy chốt 10/11, giấy chỉ có ô đáp số); **thầy chốt bản 1 ngày 14/11** (VL10 Ch.4 + VL11 Ch.3); PDF in từ `scripts/ruot-tap/out/` (gitignore), chưa ai cầm bản in giấy.
- `.htaccess` thêm `Cache-Control: no-cache` cho HTML — chờ thầy gật.

## Nội dung đang treo
- Sửa định dạng ngân hàng+đề (11/11 06:44, nhánh `claude/ai-question-review-feature-8b092c`): đã ghi 1.910 câu NH + 666 đề, ẩn 670225; sao lưu `bk_sua_dinh_dang_202611101518_{bank,exams}`. Treo: 29 câu bộ sửa bỏ qua (KaTeX), 74 nghi ngờ trong đề, deploy docx-reader + cảnh báo soạn đề.
- 5/11 · Giải cùng hình: Đ1–Đ8 đã đăng DB + deploy (51 bài); Đ9 (KHTN 9 + HSG 9, 25 bài) đã vào main, CHƯA HS ảo/CHƯA đăng DB; ~20 nhánh `claude/*` >4 ngày chưa vào main chờ thầy chỉ (memory `project_thachlab_giai_cung_hinh`).
- 7/11 · BTM "một dạng — một hình": repo xong 97/97; DB đã đăng 51, CHƯA đăng 46 (danh sách: `docs/MOT-DANG-MOT-HINH.md` mục Trạng thái 7/11) — chờ soát ảnh + thầy duyệt → publish → deploy.
- Mẹo từ khoá đợt 2 chờ số liệu Trả bài; 5 bài >2.500 từ để phiên video giảm chữ.
- Thí nghiệm L12: nhánh `claude/data-tap-lessons-16-19-e5e3b0` KHÔNG đăng từ đó (phải merge main trước); `video-theo-bai.json` còn vị trí cũ video id 12, 126.
- Motion graphic chặng A: code + DB xong (23/23 hộp khung L12 trên DB, kiểm 6/11); chờ có lượt chọn đầu tiên ở `lesson_clip_choices` để đo % đúng (mục 5) — `docs/KE-HOACH-MOTION-GRAPHIC.md`.
- Motion graphic chặng D: ĐÃ DEPLOY 17/11 (chi tiết STATE-archive); chưa xem 375px bằng tài khoản HS, chưa có sự kiện đo phát/xem (`docs/KE-HOACH-MOTION-GRAPHIC.md`).
- Motion graphic chặng C: ĐÃ DEPLOY 1/11 (chi tiết STATE-archive); đo 15/11 bằng `scripts/sql/do-clip-bay-phu-dao.sql`.
- 23 đề chưa gán lớp: `scripts/logs/gan-lop-de-khong-suy-duoc-*.json`; 16 câu L10 YCCĐ NONE chờ thầy.
- Bài tập mẫu L12 soạn lại 12 bài (9, 11, 13–19, 125–127); kế hoạch 42 bài L10/L11 chờ duyệt.
- Bài 11 L12 Thực hành chưa ghi DB; 4 bài L12 sửa đường sức — kiểm `so-file-voi-db.mts` trước.
- Trùng slug lesson 126: `content/lesson-samples/l12-ung-dung-cam-ung/` là bản cũ, đừng đăng từ đó.
- Bài 65 L10: 3 góp ý Hình 3/4/5; bài 65/67 chưa xem 375 px.
- Audit đáp án ngân hàng: 127 câu `_can_xac_nhan`, `scripts/logs/db-sai-can-duyet.csv` (656 câu).
- Backfill mức độ: ~3.500 câu rỗng — `backfill-question-bank-difficulty.mts 20` (**ghi thật**).
- Video thí nghiệm: mọi TN loại `thi_nghiem` đã có clip hoặc bỏ có lý do (20/11: thêm newton3-05 bài 61, motasong-02 bài 27 — ĐÃ ĐĂNG DB 20/11 sáng, thầy cho đăng ngay). Việc 4: 3 clip mẫu `-20261120` thầy duyệt 20/11, ĐÃ GHI DB 21/11 06:29 (bài 57, 83, 12; hẹn 22:05 treo vì máy ngủ; log `scripts/logs/dang-viec4-20261121.log`, 3/3 ✓). Lô 20 clip L12 `-20261121`: thầy duyệt 21/11, kho + 15 bài + khung đã vào main; HẸN GHI DB 22:05 22/11 (`dang-lo20.sh --yes --22h05` + caffeinate, log `scripts/video-thi-nghiem/ra/lo20-dang.log`). Code việc 1, 2, 6 chưa deploy.
- Lô 12/11 (14/11): 7 clip đề Bộ bản 2 đã trên DB từ 13/11 (nhánh review-experiment gộp main 14/11); 12 clip bẫy Ch.1/2/4 vào `lib/clip-bay.ts`; mô phỏng tự kéo `MoPhongPortals` ở bài 7, 8, 11 (DB ghi 14/11 8h50, deploy 8h47). Chưa thử HS thật; bài 7, 8 `theory.src.html` còn trỏ clip cũ (DB/`theory.html` mới hơn).
- Rank mùa 2 (5/11): 4 mùa theo khối 02/11–17/01 đang chạy (id 26–29); chưa thử bằng HS thật — memory `project_thachlab_rank_system`.
- Rank: gắn `challenge_exam_id` season 4; spec `docs/BAN-GIAO-RANK-THI-THANG-HANG-2026-10-03.md`.
- KHTN 9 cơ học 129–131: chờ thầy duyệt (memory `project_thachlab_l9_co_hoc_129_131`).
- **L10 Bài 6 Thực hành đo tốc độ (lesson 51) soạn lại 10/11**: lý thuyết + bài tập mẫu 4 dạng + quiz 20 câu, thầy duyệt, **đã ghi DB 10/11 08:25** (lý thuyết item 287, mục bài tập mẫu mới id 456, quiz exam 1352; đề quiz cũ 1227 còn nguyên chờ thầy dọn), đã deploy 08:50 và xem trên web; còn 4 điểm chờ thầy quyết — `content/lesson-samples/l10-thuc-hanh-do-toc-do/ra-soat.md`.

## CHƯA làm (roadmap)
- `/luyen-tap` lọc Lớp → Chương → Bài → YCCĐ → mức; `/lo-trinh`; Động học 10 ≥30 câu/bài.
- Trang chương: `docs/DE-XUAT-TRANG-CHUONG-2026-10.md` (§7), `docs/NGHIEN-CUU-DONG-BO-TRANG-CHUONG-TRANG-BAI.md` (§9).
- Bài tập mẫu → ngân hàng → nút "Bài tương đương" (RPC gộp).
- Đo độ trễ Supabase từ VN trước khi xoá project Sydney; cột `updated_at` cho `lessons`/`lesson_items`.
- Đề xuất nghiên cứu HS 14–22 (chờ chốt mục 5): `docs/DE-XUAT-NGHIEN-CUU-HS-14-22-2026-10-11.md`.
- 5 việc CSS bài lý thuyết đã duyệt (mục 1,3,4,5,6): `docs/PHAN-TICH-HIEN-THI-LY-THUYET-TUONG-TAC-2026-10-11.md` §5.
- "Một dạng — một hình" L12+L11 (8/11): 27 bài (L12 3 4 6 7 8 9 15 16 17 19; L11 20–22 24 25 28 30–36 39 40 43 44) đã lên DB + deploy; đã kiểm live 375px (43, 33); 7 chỗ lệch nhỏ cần sửa component ở `docs/MOT-DANG-MOT-HINH.md` mục 8/11 L12+L11.
- "Một dạng — một hình" L10+KHTN9 (8/11): 19 bài (L10 45–53, 62–79 chọn lọc; KHTN9 156) đã lên DB + deploy; còn treo ở `docs/MOT-DANG-MOT-HINH.md` mục 8/11.
- Dụng cụ đo tương tác · thư viện `/mo-phong` công khai · thí nghiệm ảo theo bộ thiết bị SGK (kế hoạch 21/11, chưa bắt đầu, giao phiên khác): `docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md`.
- Gói B `/mo-phong` (21/11, nhánh `claude/goi-b-thu-vien-mo-phong-cb60a5`): trang chỉ mục + 5 trang mô phỏng đã làm, CHƯA deploy (hỏi thầy). Dụng cụ đo Gói A thêm sau: 1 dòng `lib/mo-phong-trang.ts` + 1 dòng `components/mo-phong/MoPhongTheoSlug.tsx`, rồi `npx tsx scripts/gen-thu-vien-mo-phong.mts`; kiểm link `scripts/kiem-link-thu-vien-mo-phong.mts --mang`.
