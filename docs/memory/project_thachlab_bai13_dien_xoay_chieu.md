---
name: project-thachlab-bai13-dien-xoay-chieu
description: "Bài 13 Đại cương về dòng điện xoay chiều (lớp 12, lesson 14) — 2 đề Bài tập về nhà đã đăng (exam 21, exam 22) tính đến 19/09/2026; vài câu có lỗi trong đề gốc chờ thầy quyết"
metadata: 
  node_type: memory
  type: project
  originSessionId: 08bc2ed8-9609-4440-ac1f-615db374168e
  modified: 2026-09-19T13:16:40.699Z
---

Ngày 2026-09-19: đăng đề "Bài tập về nhà: Đại cương về dòng điện xoay chiều" (43 câu TN, 60 phút,
exam id **21**) vào lesson 14 (Lớp 12 → Chương 3: Từ trường → Bài 13), `lesson_items` id 72,
kind `bai_tap_ve_nha`, `due_at` chưa đặt (null). Nguồn: file Word "CĐ3-Bài 4. Điện xoay chiều_Trắc
nghiệm_ChuanHoa.docx" trong thư viện tài liệu cá nhân của thầy (không phải file .tex của skill
dang-bai-hoc-thachlab), chỉ đăng phần đề — mục Lý thuyết của bài 14 vẫn trống, chưa đụng tới.

**Đường đi:** file có 43 công thức OLE MathType + 3 ảnh nhúng thật → đi đường dự phòng
(`build_bundle.py` → `/quan-tri/nhap-bai`) — xem [[project_thachlab_up_de_skill]] mục 19/09/2026.
Đăng tạm dưới "Kiểm tra" rồi đổi kind sang "Bài tập về nhà" qua `/quan-tri/bai-hoc` (cách gọn, xem
[[project-thachlab-lesson-sections]]) vì trang nhập bài không có ô BTVN.

**Nhãn chủ đề (question_topics, lesson 14):** dùng 2 yêu cầu cần đạt có sẵn (Giá trị hiệu dụng của
dòng điện xoay chiều — 13 câu; Viết biểu thức u, i theo thời gian — 14 câu), tạo mới 1 yêu cầu cần
đạt **"Nguyên tắc tạo ra dòng điện xoay chiều"** (10 câu: khung dây quay, suất điện động/từ thông
cảm ứng, máy phát điện) qua `--new-topic` của `build_bundle.py`. 6 câu còn gắn ở mức cả bài (ba pha,
mạch điện trở thuần, tần số mạng điện dân dụng — không khớp yêu cầu cần đạt nào có sẵn, số câu lẻ
tẻ nên không tạo thêm chủ đề mới).

**Câu 44** dùng nguyên 3 ảnh trích từ `word/media/` của chính file gốc (đồ thị u–t dạng cos + 2 giản
đồ tròn trong lời giải) — không vẽ lại SVG. Cách tìm: `unzip -o de.docx "word/media/*"`, phần lớn ảnh
trong file này (43/52) là preview WMF của công thức OLE (bỏ qua), 9 ảnh PNG còn lại phải mở từng cái
xem — vài cái là icon trang trí không liên quan (ký tự π, √6, ảnh máy phát điện minh hoạ), chỉ 3 cái
là nội dung thật cần giữ.

**Lỗi phát hiện khi soát lại lời giải gốc (đã sửa khi soạn draft, đáp án cuối vẫn khớp bảng đáp án
gốc của file):**
- Câu 26 (thứ tự trong đề gốc — điện áp sớm pha so với dòng điện): lời giải gốc viết nhầm "π/6" ở
  bước trung gian dù đề bài và kết quả cuối đều dùng π/3 → đã sửa lời giải cho nhất quán.
- Câu 27 (vuông pha, tính U hiệu dụng): đề bài ghi "điện áp ... là 100 V" nhưng số đúng để ra đáp án
  200V (theo bảng đáp án) phải là **100√6 V** — dấu căn bị rơi mất khi OCR/convert file gốc. Đã sửa
  lại đề bài + lời giải cho khớp.
- Câu 24 (suất điện động cảm ứng máy phát): lời giải gốc ghi diện tích "600×10⁻²" (đúng ra
  600 cm² = 6×10⁻² m²) — chỉ là lỗi trình bày số mũ, số cuối cùng 4,8π V vẫn đúng, đã viết lại bước
  trung gian cho rõ.
- Câu 38: bảng đáp án cuối file bỏ trống ô này — suy ra đáp án D (1,41 A) từ chính lời giải gốc.

**Câu chờ thầy chốt (exam 21):** Câu 19 (đề gốc, "u = 100cos(100πt+π/3) V, đáp án không chính xác?")
có **2 mệnh đề cùng sai về số học** (mệnh đề hiệu dụng "50V" và mệnh đề tần số "100Hz" đều không khớp
U₀=100V), trong khi bảng đáp án gốc chỉ chọn 1 đáp án (tần số). Đây là lỗi có sẵn trong đề gốc, đã
giữ nguyên theo đáp án chính thức của tài liệu — thầy xem lại nếu muốn chỉnh số liệu cho khớp.

---

**Ngày 2026-09-19 (tiếp, cùng ngày): đăng đề thứ 2** — "Bài tập về nhà: Ứng dụng máy phát điện – Máy
biến áp – Điện từ trường" (37 câu TN, 45 phút, exam id **22**) vào cùng lesson 14, `lesson_items` id
73, kind `bai_tap_ve_nha`, tiêu đề mục "Bài tập về nhà số 2" (mục đầu id 72 vẫn giữ tiêu đề cũ
"Bài tập về nhà", không đổi tên thành "số 1"). Nguồn: file "CĐ3-Bài 5. Ứng dụng máy phát điện_Trắc
nghiệm_ChuanHoa.docx", cùng thư mục thư viện với đề 21 (`Chủ đề 3. Từ trường/`). Người dùng gọi tắt
là "bài số 15" khi yêu cầu (không khớp file nào tên "Bài 15" trong thư viện — hỏi lại xác nhận đúng
là file "Bài 5" này, có thể do gõ/nghe nhầm số 5 → 15).

**Lưu ý cho lần sau:** nội dung file "Bài 5" (máy phát điện, máy biến áp, sóng điện từ) KHÔNG cùng
yêu cầu cần đạt với "Đại cương về dòng điện xoay chiều" (lesson 14 trong CTGD hiện có trên LMS) —
chỉ trùng chương SGK (Chương 3: Từ trường) và cùng "Bài 13" là lesson cuối cùng của chương này trên
LMS (LMS chưa có lesson riêng cho máy biến áp/sóng điện từ). Thầy xác nhận vẫn muốn gắn vào Bài 13.

**Nhãn chủ đề đề 22:** câu 1–15 dùng lại "Nguyên tắc tạo ra dòng điện xoay chiều" (đã tạo từ đề 21);
tạo mới 2 yêu cầu cần đạt: **"Điện từ trường và sóng điện từ"** (câu 16–28, 13 câu) và **"Máy biến
áp"** (câu 29–37, 9 câu).

**Ảnh trích từ file gốc:** 4 ảnh PNG thật trong `word/media/` (image21/32/39/48.png) khớp đúng 4 câu
có hình (câu 11 máy phát điện, câu 25 & 26 sóng điện từ, câu 30 máy biến áp) — không vẽ lại SVG.

**Lỗi phát hiện trong đề gốc (đã xử lý khi soạn draft):**
- Câu 8: hai phương án A và C **giống hệt nhau** ($\omega NBS/\sqrt2$) — lỗi có sẵn trong file gốc
  (đáp án đúng là C theo highlight), đã giữ nguyên không tự sửa, gắn lời giải để thầy biết mà xem
  lại nếu muốn sửa phương án A.
- Câu 26: hình vẽ trong đề ghi bước sóng λ = 5 m, nhưng lời giải gốc + đáp án chính thức (B, 50 MHz)
  chỉ khớp khi λ = 6 m — mâu thuẫn có sẵn giữa hình và lời giải trong file gốc. Đã giữ đáp án B theo
  bảng đáp án chính thức, ghi rõ mâu thuẫn trong lời giải hiển thị cho học sinh, thầy xem lại nếu
  muốn chỉnh số liệu.
- Câu 35 (10 vòng quấn ngược): lời giải gốc trình bày số liệu lộn xộn/khó theo dõi nhưng đáp án cuối
  đúng (9,37 V) — đã viết lại lời giải rõ ràng bằng phương pháp "số vòng hiệu dụng" ($N_1'=N_1-2\times10$).
- Câu 36: lời giải gốc viết "600/12" (thiếu một số 0, đúng ra "600/120") — lỗi đánh máy/OCR giống
  kiểu lỗi đã gặp ở câu 27 đề 21; đã sửa lại phép tính cho đúng, đáp án D (200 vòng) không đổi.

Liên quan: [[project-thachlab-lesson-sections]], [[project_thachlab_up_de_skill]],
[[project-thachlab-bai9-tu-truong]] (mẫu ghi chú tương tự cho bài khác), [[feedback-token-discipline]].
