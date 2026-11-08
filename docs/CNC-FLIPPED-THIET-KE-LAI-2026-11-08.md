# CNC lớp đảo ngược — rà tiến trình và thiết kế lại (8/11/2026)

Bám đúng cấu trúc môn đang có trên web: Mở đầu + 7 bài (`cnc_lessons`: `intro`, `lesson-1`, `lesson-2`, `lesson-3`, `lesson-4-turn`, `lesson-4-mill`, `lesson-5`, `lesson-6`), 70 tiết, 2 cổng an toàn. Không thêm bài, không đảo thứ tự bài. Khung cũ: `docs/CHUONG-TRINH-CNC-FLIPPED.md` (18/10).

## 1. Tiến trình đến nay

| Hạng mục | Trạng thái | Ghi chú |
|---|---|---|
| 8 bài tự học (nguồn `content/lesson-samples/cnc-*`) | Xong, đã đăng | Cùng khung: Mở bài · Kiến thức · 3 bẫy · Trả bài · Bài toán/tình huống mẫu · Tổng kết; 7–8 hộp quiz mỗi bài; 22–28 KB |
| Khung 12 buổi × 5 giờ (6 buổi/tuần × 2 tuần) | Đề xuất, **chưa được thầy chốt** | 4 câu hỏi còn treo (thứ tự, cổng 4/5, số máy WinNC, video) |
| Buổi 1 mẫu (`flip-1`) | Đã đăng 18/10 | Trang A (GV dạy 5 khối) · B (2 trạm) · C (dặn buổi 2); O0001 chưa chạy thử trên WinNC thật |
| Buổi 2–12 | Chưa soạn | |
| Kiểm tra/khóa bài (`CNC_ASSESSMENT_PLAN`, checklist, `cnc_competency_permissions`) | Có sẵn, chạy được | Gắn theo **bài**, không theo **buổi**; `flip-1` không nằm trong kế hoạch đánh giá |

## 2. Vấn đề phát hiện khi rà

1. **Phần "ở nhà" chưa có chỗ trên web.** Khung cũ giao "đọc mục 2–3 + quiz 5 câu" nhưng bài tự học là một trang dài, không có gói riêng cho tối trước, không có quiz 5 câu theo buổi, không ghi được kết quả. Giảng viên không biết trước lớp sai câu nào → 15 phút đầu giờ chữa mò.
2. **Bài vận hành quá dài cho 20 phút tối trước.** Bài 4 (tiện) và Bài 5 (phay) mỗi bài 10 mục, ~28 KB; khung cũ dồn cả bài vào một tối. Bài 2, 3 (6–7 mục) chia đôi thì vừa.
3. **Bốn buổi lập trình (2–5) máy thật gần như để không.** 6 máy chỉ "chạy từng khối, không phôi" vì đặt W/offset nằm ở Bài 4–5. Sinh viên CĐ học tiện/phay vạn năng rồi, 4 ngày không chạm phôi dễ mất hứng.
4. **Buổi 1 trùng nội dung bài tự học.** `flip-1` viết lại 5 khối (an toàn, máy, điểm chuẩn, WinNC, lệnh) thay vì trỏ vào Mở đầu + Bài 1 → hai nơi phải sửa khi đổi nội dung.
5. **Lệch số giờ:** chương trình 70 tiết, khung 12 buổi × 5 giờ = 60 giờ. Cần biết tiết thực hành ở trường tính 45 hay 60 phút.
6. **Chữ cứng trong code:** "70 tiết · 7 bài học" (`components/lessons/CncCourseWorkspace.tsx:563`), "/7 bài" (`components/dashboard/TeacherOverview.tsx:41`); thêm trang buổi sẽ đếm sai.
7. **Chưa có kênh "câu em chưa rõ"** và chưa có màn hình cho giảng viên xem lớp chuẩn bị tới đâu trước buổi.

## 3. Nguyên tắc thiết kế lại (sinh viên CĐ 18–21 tuổi)

Cơ sở (nhớ từ tài liệu, chưa tra lại nguồn — cần kiểm trước khi trích chính thức): dạy học đúng lúc JiTT (Novak) — giảng viên đọc kết quả quiz tối trước rồi mới chọn phần giảng; video tự học ≤6 phút giữ người xem tốt nhất (Guo và cộng sự, 2014); ví dụ mẫu rồi rút dần bước (Sweller, hiệu ứng ví dụ mẫu); luyện có chủ đích với phản hồi ngay ở máy; hỏi đáp cặp (Mazur, peer instruction). Mã quy tắc trong `docs/QUY-TAC-THIET-KE.md` áp dụng: N1 (tải nhận thức), C2, M5.

- **Một bài — nhiều gói.** Không viết lại nội dung: mỗi buổi trỏ vào đúng mục của bài tự học (neo `#muc-n`), mỗi gói tối trước ≤ 20 phút.
- **Quiz tối trước = dữ liệu cho giảng viên**, không tính điểm; điểm vẫn lấy từ checklist/rubric hiện có.
- **Máy thật có việc từ buổi 2** bằng cách dạy *thao tác* vận hành sớm (đã có ở Buổi 1: Reference, JOG, MDI), còn *lý thuyết* vận hành vẫn ở Bài 4–5 đúng thứ tự.
- **Mọi chương trình qua WinNC 3D trước máy thật** (đã có trong khung cũ, giữ).

## 4. Cấu trúc mới

### 4.1 Ba tầng
| Tầng | Là gì | Ở đâu trên web |
|---|---|---|
| Bài (7 + Mở đầu) | Nội dung lý thuyết, giữ nguyên | `cnc_lessons` hiện có |
| Buổi (12) | **Phiếu buổi** ngắn: mục tiêu · gói tối trước (link mục) · quiz 5 câu · kế hoạch 300 phút · nhiệm vụ 2 trạm · phiếu thoát | trang `flip-N` (như `flip-1` nhưng chỉ trỏ, không chép) |
| Cổng năng lực (5) | Điều kiện đứng máy / lên bước | `CNC_ASSESSMENT_PLAN` + checklist có sẵn |

### 4.2 Năm cổng gắn vào đánh giá sẵn có
| Cổng | Sau buổi | Điều kiện | Dùng cái có sẵn |
|---|---|---|---|
| G1 An toàn | 1 | quiz an toàn đạt + ký nội quy | `lesson-1: final` |
| G2 Viết chương trình tiện chạy WinNC không lỗi | 3 | bài tập 1–2 Win-NC32 | `lesson-2: exercise-*` |
| G3 Viết chương trình phay chạy WinNC không lỗi | 5 | | `lesson-3: exercise-*` |
| G4 Vận hành + cài dao (tiện, phay) | 6, 7 | đạt thì mới cắt thật | `lesson-4-*: machine-operation, tool-setup, checklist` |
| G5 Chi tiết đạt dung sai | 9, 11, 12 | rubric | `lesson-5/6: rubric-exam` |

**Hiển thị trên web (việc 4, làm 8/11):** dải 5 ô G1–G5 ở đầu trang khoá (`CncGateStrip`, dữ liệu `CNC_GATES` trong `services/cnc-progress.ts`; xem thử `/dev/cnc-cong`). Tư vấn theo nghiên cứu:
- Hợp: mốc năng lực cụ thể là thưởng hữu hình gắn với *quyền đứng máy* (L5 việc dở trỏ đúng chỗ, hiệu ứng tiến gần đích); 5 mốc có thứ tự đọc như một khối (G1 trí nhớ làm việc).
- Ngược: 5 ô bấm được vượt N2 (≤4) → chỉ ô "cổng tiếp theo" được tô nổi (B2) + 1 dòng "Tiếp theo: … còn N bài"; ô đã đạt không bấm. Trạng thái luôn chữ + icon (M4), ô 52px (D2), cả dải ~96px = 12% màn 375×812 (B6).
- Ngưỡng bỏ cuộc: G4 làm đủ bài nhưng chờ giảng viên duyệt hiện "Chờ duyệt" (không phải "chưa đạt") để SV không tưởng mình trượt. Cổng chưa mở bấm vào dẫn về việc còn thiếu ở cổng trước.
- Đo: tỉ lệ SV bấm ô cổng (log sau), số SV kẹt "Chờ duyệt" quá 1 buổi → nhắc giảng viên. Bảng giảng viên chưa thêm (ma trận năng lực đã có duyệt G4); quiz `flip-N`/`prep-N` không thuộc cổng nào.

### 4.3 Bảng 12 buổi (giữ thứ tự bài, sửa cách chia gói)
| Buổi | Bài · mục | Tối trước (≤20') | Máy thật | WinNC |
|---|---|---|---|---|
| 1 | Mở đầu + Bài 1 | — | nhận máy, Reference, JOG, MDI | chạy O0001 |
| 2 | Bài 2 mục 1–3 | Bài 2 mục 1–2 | **luyện vận hành tay**: JOG/MDI theo phiếu, chạy khối không phôi | viết trục bậc G00/G01 |
| 3 | Bài 2 mục 4–6 + mẫu | mục 4–5 | gá phôi, tiện mặt đầu bằng tay (Bài 4 mục 5–6 dạy *thao tác*) | bù mũi dao, chu trình · **G2** |
| 4 | Bài 3 mục 1–3 | mục 1–2 | MILL: JOG, thay dao, MDI | rãnh, bậc |
| 5 | Bài 3 mục 4–7 + mẫu | mục 4–5 | phay mặt phẳng bằng tay | contour, 4 lỗ · **G3** |
| 6 | Bài 4 (tiện) | mục 7–9 (W, offset); mục 1–6 đã làm tay ở buổi 2–3 | đặt W, đo dao, chạy chương trình buổi 3 trên phôi | nhập offset, mô phỏng · **G4 tiện** |
| 7 | Bài 5 (phay) | mục 7–9 | dò cạnh, bù dài/bán kính, chạy chương trình buổi 5 | · **G4 phay** |
| 8 | Bài 6 mục 1–3 | mục 1–2 | cắt trục bậc vát/bo | kiểm trước |
| 9 | Bài 6 mục 4–5 + mẫu | mục 4 | trục côn, ren; đo, ghi sai lệch · **G5** | |
| 10 | Bài 7 mục 1–2 | mục 1 | phay bậc, cung | kiểm trước |
| 11 | Bài 7 mục 3–5 + mẫu | mục 3–4 | tấm đế 4 lỗ ren · **G5** | |
| 12 | Dự án nhóm (đề mới duy nhất) | đọc đề, lập thứ tự nguyên công | từ bản vẽ đến chi tiết | chạy thử toàn bộ |

Điểm khác khung cũ: buổi 2–5 máy thật có nhiệm vụ vận hành tay (lấy *thao tác* Bài 4–5 mục 2–6 dạy sớm theo kiểu "làm theo phiếu", lý thuyết vẫn đọc ở buổi 6–7); gói tối trước luôn ≤2 mục; Bài 4–5 chia thành phần "đã làm tay" và phần "đặt W/offset".

### 4.4 Nhịp 300 phút (giữ khung cũ, thêm bước JiTT)
| Phần | Phút | Đổi so với cũ |
|---|---|---|
| Tối trước | ≤20 | 1 gói + quiz 5 câu + 1 câu "chưa rõ" **ghi lên web** |
| Mở buổi | 15 | giảng viên chữa **2 câu sai nhiều nhất** theo bảng kết quả, không chữa đều |
| GV dạy | 60 (tối đa 90) | 3 khối ≤20' trên máy, mỗi khối 1 câu hỏi cặp; bỏ phần đã đọc ở nhà |
| Nghỉ | 15 | |
| Thực hành 2 trạm | 85 + 10 + 85 | nhiệm vụ 1 · 2 · thử thách; đổi trạm |
| Kết buổi | 30 | phiếu thoát 3 câu + 5S, bàn giao máy |

## 5. Việc cần làm trên web (theo thứ tự ưu tiên)
1. **Quiz tối trước theo buổi + bảng kết quả cho giảng viên** — dùng lại `exams.cnc_key` (mỗi buổi một khoá `flip-N-pre`) và `cnc_learning_records`; trang giảng viên lọc câu sai nhiều nhất. Cần agent `kien-truc-du-lieu` xem có phải thêm cột không.
2. **Neo mục trong 7 bài** (`id="muc-1"`…) để phiếu buổi trỏ tới; sửa qua `scripts/cap-nhat-cnc-ly-thuyet.mts`. — **Xong 8/11**: tiêu đề "N. …" có `id="muc-N"`, "V. Bài toán mẫu" có `id="bai-mau"` (sao lưu `scripts/logs/cnc-lesson-*-body-backup-1794154*.html`); `CNC_PREP_SESSIONS.anchor` + `cncLessonHref()`; `CncCourseWorkspace` cuộn tới `#neo` sau `?bai=`.
3. **Viết lại `flip-1` thành phiếu buổi** (trỏ Mở đầu + Bài 1), soạn `flip-2` … `flip-12` theo cùng khuôn. — **Xong 8/11**: nguồn `content/lesson-samples/cnc-phieu-buoi/build.mjs` (dữ liệu 12 buổi → `out/flip-N.html`), ghi DB bằng `dang.sh` (flip-1 sao lưu `scripts/logs/cnc-flip-1-row-backup-1794154420513.json`); xem ở `/lop-hoc/cnc/buoi/?so=N` (không cần đăng nhập), link "Phiếu 12 buổi học" trong cột bài + dòng nhắc quiz chuẩn bị; `flip-*` lọc khỏi danh sách bài. Không đổi schema. Phiếu theo bảng 4.3 (vận hành tay buổi 2–5) — chờ thầy chốt câu 1 mục 6.
4. **Gắn `flip-N` vào `CNC_ASSESSMENT_PLAN`** (chỉ quiz tối trước, không khoá bài) và hiện cổng G1–G5 trên trang lớp.
5. **Ô "câu em chưa rõ"** dưới quiz tối trước.
6. Bỏ chữ cứng "70 tiết · 7 bài học", "/7 bài" → đếm từ dữ liệu.

## 6. Cần thầy quyết
1. Dạy *thao tác* vận hành tay ở buổi 2–5 (máy thật không để không) — đồng ý hay giữ "chạy khối không phôi" như cũ?
2. 70 tiết khớp 12 buổi × 5 giờ thế nào (tiết 45 hay 60 phút)?
3. Cổng G2–G5: bắt buộc mới đứng máy hay chỉ ghi nhận?
4. Số máy tính WinNC ở xưởng; chạy thử O0001 trên WinNC thật.
5. Quiz tối trước: Claude soạn từ bài hiện có (5 câu/buổi × 11 buổi) hay thầy đưa câu?
