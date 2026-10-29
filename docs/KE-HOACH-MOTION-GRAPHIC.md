# Kế hoạch: motion graphic trên thachlab — dùng vào đâu, dùng thế nào (29/10/2026)

"Motion graphic" ở thachlab = bộ dựng video `scripts/video-thi-nghiem/` (Python + Pillow + ffmpeg, khung dọc 9:16, không
giọng, phụ đề từ khoá + tiếng báo ở mốc; cấu trúc **Dự đoán → Tiến hành → Đáp án + Rút ra → Bẫy → Chốt + câu hỏi tự nhớ**),
cộng hai lớp đi kèm đã có trong repo:

| Lớp | Có gì | Trạng thái 29/10 |
|---|---|---|
| **A. Clip 9:16 tự dựng** | `engine.py`, `render.py`, 24 kịch bản `clips/*.py`; cổng A (`--kich-ban`), cổng B (`--sheet`), `--do-chu`; tải bucket `lesson-clips` bằng `tai-clip-len-storage.mts`; chèn bài bằng `chen-video-thi-nghiem.mts`; skill `dung-video-thi-nghiem` | 23 clip L12 đã lên web (16 bài + bài 126). Chi phí đo được **2,4–2,6 USD/clip**, render 2–4 phút |
| **B. Khung bán tương tác** | `components/lessons/VideoThiNghiemKhung.tsx` + `content/thi-nghiem/video-khung/*.json`: khung 6 ô sáng theo giây, **video tự dừng ở câu Dự đoán** chờ HS chọn; xem thử `/dev/video-tuong-tac` | 23 JSON xong, kiem-code đã soát (K1–K10); **chưa vào bài thật** |
| **C. SVG chuyển động** | agent `ve-hinh-dong` (SMIL, bấm mới chạy/≤ 2 lượt, ≤ 15 KB), quy tắc V10 | chặng 2 của `KE-HOACH-CLIP-ANH-DONG.md`, chưa chạy lô |

Quy tắc áp dụng: `docs/QUY-TAC-THIET-KE.md` **V1–V12** (V8 rút chữ, V9 phụ đề, V10 ảnh động, V11 hạn mức, V12 vùng an toàn
+ ≤ 200 từ/phút), T1–T12 (`docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md`), E1 (nhãn A. B. C. D.).

## 1. Tư vấn ngắn theo nghiên cứu đã có trong repo

- **Hợp**: clip là *quá trình động* mà hình tĩnh không cho thấy (Höffler & Leutner 2007, V10); dừng ở câu Dự đoán trước khi
  xem đáp án đúng tinh thần 先猜后学 của bài lý thuyết và tăng nhớ hơn xem thụ động (Mayer – segmenting, learner pacing);
  phụ đề từ khoá thay lời đọc dài hợp Mayer – redundancy/signaling; 35–50 s nằm dưới ngưỡng bỏ cuộc "chưa thấy phần thưởng"
  (`DE-XUAT-NGHIEN-CUU-HS-14-22`, mục Gloria Mark: không thiết kế cho 47 s, thiết kế cho "tới việc đầu" sớm).
- **Rủi ro**: (1) *dư thừa* — clip nói lại điều hộp chữ/mô phỏng đã nói → học kém đi (V6, V8; Harp & Mayer 1998);
  (2) *thông tin thoáng qua* (Leahy & Sweller 2011) — clip trôi là mất, nên luôn giữ 2 dòng Nhìn vào/Rút ra và cho bấm lại;
  (3) *tải nhận thức* khi mỗi bài chất thêm media → giữ hạn mức V11; (4) video **không** phải phần thưởng/huy hiệu
  (SDT, Deci 1999) — không gắn RP cho việc "đã xem".
- **Suy ra**: mảng đáng làm là nơi HS **phải đoán rồi mới thấy** (thí nghiệm, bẫy hay sai, ôn tập hỏi-trước); mảng không
  nên làm là nơi chữ/mô phỏng tương tác đã làm tốt hơn (bài tập mẫu từng bước, lời giải) hoặc đề thi (E1–E3: giống đề thật,
  tĩnh).
- **Đo**: tỉ lệ đúng quiz sau thí nghiệm + Trả bài của bài có clip, 2 tuần trước/sau; tỉ lệ bấm phát và tỉ lệ chọn ở
  điểm dừng Dự đoán (lớp B ghi được, hiện chưa có event nào về clip).

## 2. Mảng ứng dụng — xếp theo ưu tiên

| # | Mảng | Hình thức | Vì sao hợp / quy tắc | Ưu tiên |
|---|---|---|---|---|
| 1 | **Thí nghiệm trong bài lý thuyết** (đang làm) | Lớp A + **lớp B** (dừng ở Dự đoán) | Đã có 23 clip L12; còn **211 TN / 65 bài** L9–L11 chưa clip; nhóm C (không có YouTube) 64 clip còn lại, nhóm B 88 chờ thầy chọn. V1, V8, V9, V12, T2 | ★★★ |
| 2 | **Phụ đạo theo chủ đề + Trả bài** | "Clip bẫy" 20–30 s: tình huống → HS chọn → vì sao sai → quy tắc 1 dòng; 1 clip/bẫy, lấy từ chủ đề hay sai của lớp (`docs/ANALYTICS-SETUP.md`) | HS vào phụ đạo đã "sai rồi", xem lý do sai dạng động hợp Mayer – signaling + quyền được sai (Dahl–Steinberg). Không thay 20 câu thoát phụ đạo | ★★★ |
| 3 | **Ôn tập theo chặng** (3 màn hình, chưa deploy) | Video ôn chương 60–90 s dạng **hỏi trước – hiện sau**: 4–6 câu từ khoá, mỗi câu dừng 4 s rồi hiện đáp án | Retrieval practice; thay "tóm tắt có giọng" (thụ động). Chèn ở màn hình 1 của chặng, bấm mới phát (V5) | ★★ |
| 4 | **Sách in** (`sach-in-tu-web`) | QR cạnh hộp thí nghiệm trỏ thẳng tới clip (`lesson-clips/...mp4`) | Đã có pipeline QR; không cần dựng thêm, chỉ in link. Clip 9:16 xem trên điện thoại khi đang cầm sách | ★★ (rẻ) |
| 5 | **HSG KHTN 9 / KHTN 9 cơ học** | Lớp A cho thí nghiệm cơ–nhiệt khó quay (ròng rọc, bình thông nhau) | Cùng engine, số liệu từ `so_lieu_mau`; làm sau khi L10–L11 xong | ★ |
| 6 | **Phụ huynh / tuyển sinh** (ngoài bài học) | 1 clip 30 s "thachlab học thế nào" cho `/phu-huynh`, `/loi-moi`; bản 9:16 dùng cho Zalo/Reels tuyển sinh | Hợp kế hoạch tự tuyển sinh; theo P1..P21 (chữ lớn, chậm, phụ đề). Một lần, không lặp | ★ (một lần) |
| — | **Không làm**: hình động trong câu hỏi đề/ngân hàng (E1–E3), video lời giải bài tập mẫu (đã có `buoc[]` tương tác, V6), clip mở bài bịa cảnh (V7), autoplay/GIF (B4, V10), gắn RP cho việc xem | | | |

## 3. Cách dùng (quy trình đã có, không viết lại)

1. **Chọn chỗ**: hộp `.tl-box--exp` chưa có clip, hiện tượng động, YouTube không có (nhóm C trong
   `content/thi-nghiem/danh-sach-tu-dung.md`). Mỗi hộp ≤ 1 clip (V1), mỗi bài theo hạn mức V11.
2. **Dựng**: `/dung-video-thi-nghiem <tn-id>` → copy kịch bản gần nhất trong `clips/`, số liệu từ `so_lieu_mau` của
   `tn-*.json` → cổng A `render.py <tên> --kich-ban` → cổng B `--sheet` (kiem-code đọc ảnh, phiên chính không mở) →
   `--do-chu` ≤ 200 từ/phút → `render.py <tên>` **trong tab terminal** (2–4 phút, chạy song song được).
3. **Lên web**: `npx tsx scripts/tai-clip-len-storage.mts ra/<id>.mp4 --tn <id> --nhan "Xem thí nghiệm dựng lại: …" --nhin-vao "…" --apply`
   → `chen-video-thi-nghiem.mts` → build bài → `bash scripts/cap-nhat-ly-thuyet.sh <file> <lesson_id>` (chỉ mục lý thuyết,
   sau khi thầy duyệt lô). Ghi DB hàng loạt chỉ sau 22h.
4. **Khung tương tác** (lớp B): viết `content/thi-nghiem/video-khung/<tn>.json` (mốc giây 6 ô + mốc dừng Dự đoán + 4 lựa chọn
   A.–D.), kiểm `--kiem`, xem ở `/dev/video-tuong-tac`.
5. **Commit theo đường dẫn** ngay sau render/chèn (`clips/*.py`, `tn-*.json`, `video-khung/*.json`, `theory.*`, `bundle.json`);
   mp4 ở `ra/` không vào git. Ghi sổ `content/thi-nghiem/so-clip-anh-dong.md`.

## 4. Chặng triển khai

| Chặng | Việc | Thời gian | Xong khi | Ai |
|---|---|---|---|---|
| **A. Đưa khung tương tác vào bài thật** | Deploy CSS `tl-video--doc` còn treo; `ContentHtml`/chèn bài nhận `data-khung` để render `VideoThiNghiemKhung` cho 23 clip L12; thêm event `clip_choice` (chọn ở điểm dừng) ghi gộp theo heartbeat, **không thêm round-trip** cho `/lop-hoc/bai`; chụp 375 px sáng/tối | 30/10–3/11 (1–2 phiên) | 23 clip L12 dừng ở Dự đoán trên web; có số lượt chọn đúng/sai | phiên chính Sonnet + `kiem-code` |
| **B. Phủ L10–L11 nhóm C** | 64 clip còn lại theo chương **sắp dạy** (lịch `lich-tuan`), lô 7–10 clip/phiên, mỗi clip kèm JSON khung | 3–22/11 | 64 dòng "đã đăng/bỏ qua"; ≈ 150–170 USD | Opus dựng (song song ≤ 3), Sonnet `kiem-code` cổng B |
| **B'. Nhóm B 88 TN** | Thầy duyệt danh sách: dùng YouTube có sẵn (0 USD, V3–V5) hay tự dựng | chờ thầy | danh sách có cột "YT/tự dựng" | thầy |
| **C. Clip bẫy cho phụ đạo** | Thí điểm 1 chương L12 đang dạy: lấy 5 chủ đề sai nhiều nhất từ Trả bài → 5 clip 20–30 s → nhúng ở `/phu-dao` chủ đề đó + bài lý thuyết liên quan; mẫu kịch bản `clips/bay-*.py` (cảnh: tình huống → chọn → sai vì → quy tắc) | 10–20/11 | 5 clip + kịch bản mẫu được thầy duyệt; đo tỉ lệ thoát phụ đạo trước/sau | Opus (mẫu), Sonnet (lô) |
| **D. Video ôn chương hỏi-trước** | 1 chương L12 thử (60–90 s, 5 câu từ khoá dừng 4 s); gắn vào màn hình 1 của Ôn tập theo chặng khi deploy | tháng 12 | thầy duyệt 1 clip; quyết định mở rộng | Opus |
| **E. QR sách in** | Thêm QR clip cạnh hộp thí nghiệm trong `book/` cho chương đã có clip | khi dựng lại sách | QR giải mã đúng (`scripts/kiem-qr.mts`) | Sonnet |
| **F. Clip phụ huynh / tuyển sinh** | 1 clip 30 s theo P1..P21, đặt ở `/phu-huynh`; bản 9:16 cho Zalo | khi thầy cần | thầy duyệt | Opus |

Ranh giới: L12 `theory.src.html` đang có phiên mẹo 🧠 và thí nghiệm khung 6 ô — trước khi sửa bài nào chạy
`git log origin/main -3 -- content/lesson-samples/<bài>/theory.src.html`, có commit 24 h qua thì chờ. Chặng A chỉ đụng
component video + CSS, không sửa chữ bài.

## 5. Đo hiệu quả (sau chặng A, trước khi mở chặng C)

- Bài có clip L12: tỉ lệ đúng quiz sau thí nghiệm + Trả bài, 2 tuần trước/sau 28/10 (số liệu có sẵn).
- Lớp B: % HS bấm phát; % chọn ở điểm dừng; phân bố A–D (câu bẫy tốt phải có ≥ 30 % chọn sai).
- Nếu bấm phát < 20 % → đổi ảnh bìa/nhãn trước khi dựng thêm; nếu chọn đúng ở điểm dừng > 85 % → câu Dự đoán quá dễ, sửa JSON.
