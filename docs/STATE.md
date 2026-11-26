# STATE — Hiện trạng ThachLab (rút gọn 25/11/2026)

Nạp mỗi phiên, giữ dưới 15 KB: hiện trạng + ĐANG CHỜ (1–2 dòng/việc). Xong → nguyên văn sang `docs/STATE-archive.md`; chi tiết ở `docs/memory/project_*.md`.

## Hạ tầng
- Next.js App Router + TS + Tailwind v4, `output: "export"`, deploy `scripts/deploy.sh` → nhánh `deploy`.
- Supabase `jgvbdbpvjdntdgzthumv` (Singapore, gói PRO). Sơ đồ: `docs/DATABASE.md`, RPC: `docs/DATABASE-RPC.md`.
- KaTeX 0.17; học liệu tĩnh `public/data/` sinh ở `prebuild` CHỈ cho bài xem thử (`lessons.is_preview`: 2, 20, 46) — bài khác HS đọc thẳng DB, ghi `cap-nhat-ly-thuyet.sh` là lên ngay, chỉ deploy khi đổi CSS/code.
- Nền SÁNG mặc định (11/10): token `app/globals.css`, `docs/MAU-NEN-SANG.md`.

## Migration — ĐANG CHỜ (nguồn đúng: `bash scripts/run-migrations.sh --list` + `scripts/logs/`; sau migration chạy `node scripts/gen-database-doc.mjs`)
- **AI sửa lỗi → sửa luôn câu gốc ngân hàng (16/11)**: `20261116120000_bank_apply_question_fix` ĐÃ CHẠY 16/11 (hàm tồn tại, chặn người không phải giáo viên). Client đã sửa (ExamSection + services/ai-check-exam) nhưng chưa vào main/deploy; chưa thử bấm AI sửa thật.
- Điểm học phần CNC (14/11): migration đã chạy, `/lop-hoc/cnc/bang-diem/` đã deploy 18/11; điểm Phay chưa nạp (mẫu `scripts/gui-diem-thi-tien-cnc.mts`, module 'phay').
- Bài tập ngày 28/10 (đề 1289–1293): chưa rõ đã deploy `ClassRoster.tsx`.
- L11 đề 693/701: đã bỏ 11 câu ngoài CT 22/11 (chi tiết STATE-archive 25/11).
- L11 đề 701 câu 16, 28: có dòng bank 1248678/1248701 (đúng chủ đề) nhưng hash lệch bản trong đề (đề đã sửa định dạng sau) → lưu lại đề 701 một lần ở /quan-tri/sua-de là `sync_exam_to_bank` cập nhật đúng dòng đó.
- **Vá bảo mật 11/11**: 3 migration ĐÃ CHẠY (bước 2 lúc 12/11 06:40; `20261112070000` kiểm đầu vào điểm CNC lúc 12/11 08:15), client đã deploy; 12/11 đã bấm thử bằng tài khoản admin (sửa đề THPT/CTTC, `/lop-hoc/cnc`, dashboard GV: mọi request 200). Chưa thử bằng tài khoản HS/TA thật; chưa bấm nút nhắc làm bài. Script đăng nhập tài khoản thường mà đọc `exams.questions` phải đổi sang `exams_staff`.
- **Quiz trắc nghiệm CNC chấm ở server (12/11)**: cả 2 bước ĐÃ CHẠY (bước 2 lúc 08:52), client deploy 12/11 ~08:50 (bản 11/11 19:01 = commit 874bef7f6 + 6 file vá bảo mật). Chưa thử bằng tài khoản SV thật (admin không ghi điểm) → buổi CNC tới xem `cnc_learning_records` có dòng mới của 15 bài có ngân hàng. Đáp án vẫn nằm trong `get_cnc_quiz_banks` (quiz cho xem đáp án và làm lại không giới hạn).
- Vá bảo mật 22/11 bước 2 ĐÃ CHẠY 23/11; chưa thử HS thật (luyện tập, phụ đạo) — rollback `perf/rollback/*buoc_2.down.sql`.
- Còn lỗ: bài CNC chấm ở máy (dịch lệnh trả lời ngắn, điền khuyết, viết chương trình, checklist — đáp án nằm trong mã client); `diagnostic_submit` vẫn nhận số đúng/sai từ client (chỉ ảnh hưởng mục phụ đạo của chính em); mật khẩu mặc định chỉ chặn ở client (chặn thật cần Auth/import-roster).
- **GitHub 12/11 06:46**: có ruleset `bao-ve-main-deploy` (chỉ admin cập nhật `main`/`deploy`) → workflow `gop-claude-vao-main.yml` KHÔNG đẩy được vào main nữa (GH013). Phiên Mac: `git push origin HEAD:main` (fast-forward, sau khi `git merge origin/main`); phiên cloud: không tự vào main được, chờ thầy quyết. Repo vẫn công khai, `nhmkct1`/`zKdKaidO` vẫn quyền ghi.
- **Sức khỏe mở cho HS/SV (19/11)**: `student` vào được `/suc-khoe` (THPT + CTTC), chương trình riêng không dụng cụ `PROGRAM_HS` (3 buổi ~30′), không thấy Số đo/ngực–eo; link ở `/tai-khoan/them`; localStorage tách theo tài khoản. Chưa deploy, chưa thử bằng tài khoản HS thật.
- 19/11 RPC gộp trang bài + buổi ôn: đã chạy + deploy; chưa thử bằng HS thật.
- **CNCTM 1 bài 5–6 (26/11)**: `20261126110500_cnctm1_bai_5_6` CHƯA CHẠY (chèn chương/bài 5, 6, published=false); nội dung `content/lesson-samples/cnctm1-bai-5-do-chinh-xac/`, `cnctm1-bai-6-thiet-ke-qtcn/` chờ thầy duyệt rồi mới chạy + upload-lesson.mts.
- **Ôn 5 phút (25/11)**: cả 2 migration đã chạy; 81 bài có thẻ + dòng ở /lop-hoc đã vào main, CHƯA deploy (chi tiết `docs/memory/project_thachlab_on_5_phut.md`).
- **Gọi tên ngẫu nhiên trong bài (26/11)**: `20261126090000_goi_ten_ngau_nhien` (hàm `class_call_roster`, chỉ đọc) ĐÃ CHẠY 26/11 bằng `supabase db query -f` (checkout chính kẹt thay đổi phiên khác nên không qua run-migrations.sh, chưa có log, chưa gen-database-doc); nút "Gọi tên"/phím G ở /lop-hoc/bai đã deploy 26/11 (deploy 1934227); chưa thử bằng tài khoản GV với lớp thật. 26/11 thêm chọn danh sách (lớp THPT + khoá CTTC): `20261126100000_goi_ten_chon_danh_sach` ĐÃ CHẠY bằng `db query -f`. Deploy 06118878f = nguồn 3ceceea96 + 2 file RandomCallFab (KHÔNG gồm code lớp CNCTM đang chờ migration).
- **CNCTM 1 Bài 3–4 (26/11)**: `20261126110000_cnctm1_bai_3_4` CHƯA CHẠY, chờ thầy duyệt `content/lesson-samples/cnctm1-bai-{3-phoi-luong-du,4-chuan}/xem-thu/xem-thu.html`; sau đó chạy migration rồi `upload-lesson.mts` 2 bundle, bật published.
- **CNCTM 1 Bài 10–13 (26/11)**: `20261126111500_cnctm1_bai_10_13` CHƯA CHẠY (4 chương/bài, published=false); 4 bundle ở `content/lesson-samples/cnctm1-bai-1{0,1,2,3}-*/` chờ thầy duyệt rồi mới upload-lesson.
- Sau mỗi migration: `node scripts/gen-database-doc.mjs`.

## Chờ deploy / chờ thử thật
- Sức khỏe HS + trang chủ (23/11): đã deploy; 3 chỗ Sức khỏe chưa xem bằng tài khoản HS.
- Dashboard GV CNC tab "Buổi học" (`TeacherFlipBoard`): đã deploy 10/11; chưa thử trong buổi dạy thật.
- `ExamDoneLocked`: đã deploy 18/11; thử bằng HS thật (đề 1297, lớp 11, 375px).
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
- Mẹo từ khoá đợt 2 chờ số liệu Trả bài; 5 bài >2.500 từ để phiên video giảm chữ.
- Thí nghiệm L12: nhánh `claude/data-tap-lessons-16-19-e5e3b0` KHÔNG đăng từ đó (phải merge main trước); `video-theo-bai.json` còn vị trí cũ video id 12, 126.
- Motion graphic chặng C, D: đã deploy (1/11, 17/11); chưa xem 375px bằng HS, đo bằng `scripts/sql/do-clip-bay-phu-dao.sql`.
- 22/11 23h: đề chưa gán lớp 362 → 16 (còn 16 đề CNC không thuộc lớp nào trong `classes`): 146 suy từ bài học + 200 theo đề sinh đôi/môn (`gan-lop-de-song-sinh.mts`, undo bằng file `scripts/logs/gan-lop-*`). 16 câu L10 YCCĐ NONE vẫn chờ.
- Bài tập mẫu L12 soạn lại 12 bài (9, 11, 13–19, 125–127); kế hoạch 42 bài L10/L11 chờ duyệt.
- Bài 11 L12 Thực hành chưa ghi DB; 4 bài L12 sửa đường sức — kiểm `so-file-voi-db.mts` trước.
- Trùng slug lesson 126: `content/lesson-samples/l12-ung-dung-cam-ung/` là bản cũ, đừng đăng từ đó.
- Bài 65 L10: 3 góp ý Hình 3/4/5; bài 65/67 chưa xem 375 px.
- Audit đáp án ngân hàng: 127 câu `_can_xac_nhan`, `scripts/logs/db-sai-can-duyet.csv` (656 câu).
- Backfill mức độ: ~3.500 câu rỗng — `backfill-question-bank-difficulty.mts 20` (**ghi thật**).
- Video thí nghiệm: mọi TN đã có clip; lô 20 clip L12 + 3 mẫu đã lên DB (21–22/11). Lỗi 0 lượt ghi (`lesson_clip_views`, `lesson_clip_choices`) do thiếu `data-lesson-id` ở /lop-hoc/bai — sửa + deploy 25/11 (9e50dcab4); kiểm lại có dòng sau buổi học tới. Treo: sinh lại `thu-vien-mo-phong.json`.
- Lô 12/11: clip đề Bộ, 12 clip bẫy, `MoPhongPortals` bài 7, 8, 11 đã lên; bài 7, 8 `theory.src.html` còn trỏ clip cũ (DB/`theory.html` mới hơn).
- Rank mùa 2 (5/11): 4 mùa theo khối 02/11–17/01 đang chạy (id 26–29); chưa thử bằng HS thật — memory `project_thachlab_rank_system`.
- Rank: gắn `challenge_exam_id` season 4; spec `docs/BAN-GIAO-RANK-THI-THANG-HANG-2026-10-03.md`.
- KHTN 9 cơ học 129–131: chờ thầy duyệt (memory `project_thachlab_l9_co_hoc_129_131`).
- L10 Bài 6 Thực hành đo tốc độ (lesson 51): đã đăng 10/11; còn 4 điểm chờ thầy quyết — `content/lesson-samples/l10-thuc-hanh-do-toc-do/ra-soat.md`; đề quiz cũ 1227 chờ dọn.

## CHƯA làm (roadmap)
- `/luyen-tap` lọc Lớp → Chương → Bài → YCCĐ → mức; `/lo-trinh`; Động học 10 ≥30 câu/bài.
- Trang chương: `docs/DE-XUAT-TRANG-CHUONG-2026-10.md` (§7), `docs/NGHIEN-CUU-DONG-BO-TRANG-CHUONG-TRANG-BAI.md` (§9).
- Bài tập mẫu → ngân hàng → nút "Bài tương đương" (RPC gộp).
- Đo độ trễ Supabase từ VN trước khi xoá project Sydney; cột `updated_at` cho `lessons`/`lesson_items`.
- Đề xuất nghiên cứu HS 14–22 (chờ chốt mục 5): `docs/DE-XUAT-NGHIEN-CUU-HS-14-22-2026-10-11.md`.
- Lộ trình học kiểu Duolingo (bản thiết kế, chờ chốt mục 9): `docs/LO-TRINH-KIEU-DUOLINGO.md`.
- 5 việc CSS bài lý thuyết đã duyệt (mục 1,3,4,5,6): `docs/PHAN-TICH-HIEN-THI-LY-THUYET-TUONG-TAC-2026-10-11.md` §5.
- "Một dạng — một hình" (8/11): 46 bài L10/L11/L12/KHTN9 đã lên DB + deploy; 7 chỗ lệch nhỏ chờ sửa component (`docs/MOT-DANG-MOT-HINH.md` mục 8/11).
- Dụng cụ đo tương tác · thư viện `/mo-phong` công khai · thí nghiệm ảo theo bộ thiết bị SGK (kế hoạch 21/11, chưa bắt đầu, giao phiên khác): `docs/KE-HOACH-MO-PHONG-HOC-TU-EDUTOOLKIT.md`.
- `/mo-phong` Gói B + 4 dụng cụ đo Gói A: đã lên production 23–25/11. Thêm trang: 1 dòng `lib/mo-phong-trang.ts` + 1 dòng `MoPhongTheoSlug.tsx` → `npx tsx scripts/gen-thu-vien-mo-phong.mts`.
