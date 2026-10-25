---
name: cap-nhat-thi-nghiem-l12
description: Rà và viết lại PHẦN THÍ NGHIỆM (hộp `.tl-box--exp`, hộp Dự đoán mở bài, quiz sau thí nghiệm, bước Thử PhET) của các bài lý thuyết lớp 12 đã đăng theo cách đề thi tốt nghiệp THPT hỏi — khung 6 ô Giả thuyết → Dự đoán → Dụng cụ & cách đo → Quan sát → Rút ra → Chưa nói được gì, quy tắc T1–T12 trong docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md — rồi đăng thay bản cũ bằng cap-nhat-ly-thuyet.sh (chỉ ghi mục lý thuyết). Dùng khi thầy nói "cập nhật thí nghiệm bài X lớp 12", "làm tiếp các bài còn lại theo khung thí nghiệm", "rà hộp thí nghiệm chương 2", "/cap-nhat-thi-nghiem-l12". KHÁC soan-bai-ly-thuyet-tuong-tac (soạn bài mới) và cap-nhat-bai-hoc-theo-gemini (rà toàn bài bằng học sinh ảo) — skill này chỉ đụng phần thí nghiệm và những gì phải dịch theo để giữ hạn mức độ dài. Soạn + kiểm chạy được trên cloud; ĐĂNG DB chạy trên Mac.
---

# Cập nhật phần thí nghiệm các bài lớp 12 theo khung đề thi

Nguồn quy tắc (đọc trước, không chép lại ở đây): `docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md` — mục 1 (đề hỏi gì), mục 2 (T1–T12), mục 3 (checklist soát hộp). Bài mẫu đã làm: `content/lesson-samples/l12-hat-nhan-mo-hinh-nguyen-tu/` (commit `ff7746044`, 25/10/2026): xem mục I và II.3 của `theory.src.html` + `content/thi-nghiem/tn-l12-hatnhan-03.json` để chép đúng cấu trúc HTML.

## 0. Phạm vi của một lượt
- Một lượt = 1–3 bài cùng chương (chung ký hiệu, chung bẫy). Không làm cả lớp 12 trong một phiên.
- Chỉ sửa: hộp Dự đoán ở mục I nếu nó lộ kết quả (T2), hộp `.tl-box--exp` của thí nghiệm **có tên trong chương trình** (T1), quiz đứng ngay sau hộp đó (T9), bước Thử của iframe PhET có mô hình đối chứng (T12), file `tn-*.json` tương ứng (T11). Thí nghiệm minh hoạ nhỏ giữ 3 ô Làm – Quan sát – Rút ra, chỉ soát T3 (Quan sát không chứa suy luận) và T7 (sai số có chiều) nếu là thí nghiệm đo.
- Không đụng: Bẫy, Trả bài, Bài toán mẫu, Mang về, `data-tap` của tiêu đề (gắn với tập in), số lượng quiz (ảnh hưởng dòng "N câu tự kiểm tra" và tập in).

## 1. Danh mục bài L12 và thí nghiệm cần đưa về khung 6 ô

Cột "Kinh điển" = thí nghiệm đề thi có thể hỏi theo khung (T1). Đánh ✓ vào cột "Xong" + ngày khi đã đăng.

| Thư mục `content/lesson-samples/` | id | Hộp exp | Kinh điển cần khung 6 ô | Xong | Rà 25/10 (3 agent kiem-code) |
|---|---|---|---|---|---|
| l12-su-chuyen-the | 2 | 3 | Đun nước đá ghi nhiệt độ mỗi phút (đồ thị nóng chảy/sôi) — T7, T8 | | CẦN · 2 611 từ · T2 mở bài lộ "kim đứng yên ở 0 °C"; bảng đun đá không khớp công suất không đổi (sửa số hoặc ghi minh hoạ) |
| l12-thang-nhiet-do | 3 | 4 | Kiểm hai mốc 0 °C và 100 °C; trộn nước nóng–lạnh (giả thuyết nhiệt độ cân bằng) | | CẦN · 2 658 · T2 mở bài ghi 311,5 K = đáp án; hộp (1),(3) thiếu nhiều ô |
| l12-noi-nang-dl1 | 4 | 2 | Bơm xe nóng ở đâu (giả thuyết: công → nội năng); nên THÊM thí nghiệm Joule (cánh khuấy) dạng `vi_du` || ✓ 25/10 (2 638 → 2 492) | CẦN · 2 638 · hộp đo c có chiều sai số nhưng thiếu cách giảm, chưa nói "Δt lớn → mất mát lớn"; chưa có Joule |
| l12-thuc-hanh-nhiet | 5 | 2 | Đo nhiệt dung riêng (đề 2026 II.4) và nhiệt nóng chảy riêng (đề 2025 II.1): giai đoạn đối chứng, "coi rằng/bỏ qua", chiều mất mát — T6, T7 **ưu tiên 1** || ✓ 25/10 (2 799 → 2 487) | CẦN ưu tiên 1 · 2 799 (2 lỗi cứng) · Dự đoán lộ "nhiệt kế chỉ 0 °C"; thiếu hẳn phễu + dây điện trở, hai giai đoạn, m₂−m₁ của đề 2025 II.1 |
| l12-thuyet-dong-hoc-phan-tu | 6 | 3 | Chuyển động Brown (hạt khói) — giả thuyết phân tử chuyển động | | CẦN (thấp) · 2 498, hết quỹ · Brown thiếu 3 ô; mở bài kể hiện tượng trước Dự đoán |
| l12-boyle-charles | 7 | 2 | Nén khí xilanh (Boyle), cột khí áp suất không đổi (Charles) — T8 tích/tỉ số không đổi | đăng 25/10 (nhánh cfad9c, chưa kiểm chéo); soát 25/10 CHƯA ĐẠT: T2 dòng 🔑 + công thức đứng trước hai hộp; Coi rằng nằm trong details (T6); Rút ra thiếu cơ chế (T4), feedback Câu 3 gọi C là "cơ chế" (thật ra là điều kiện bố trí); "Ô cuối ra 801", "0,0371" lộ ô tự tính; Charles ghi lệch 1,4% (đúng 1,2%) → vá ở Lô 5 | CẦN (gần đạt) · 2 524 · chỉ thiếu Giả thuyết/Dự đoán/Coi rằng/Chưa nói; số liệu đúng |
| l12-phuong-trinh-trang-thai | 8 | 2 | Bình kín ngâm nước năm nhiệt độ — T8 | | CẦN · 2 541 · T2 mở bài "5,0 → 5,3 bar" lộ đáp án B; hộp bình kín thiếu ô |
| l12-ap-suat-dong-nang | 9 | 2 | Áp suất khí theo nhiệt độ trong bình kín — T8 | | CẦN · 2 567 · hộp p/T thiếu 3 ô, không có quiz sau hộp; T2 nhẹ |
| l12-khai-niem-tu-truong | 10 | 3 | Oersted (dòng điện lệch kim la bàn): giả thuyết – quan sát – giới hạn | | CẦN · 2 607 · Oersted thiếu 3 ô, quiz sau hộp lạc đề (hai dây song song) |
| l12-luc-tu-cam-ung-tu | 11 | 2 | Đo lực từ bằng cân/dây treo (đề 2025 II.2): hướng B, hướng lực, cân tăng/giảm — **ưu tiên 2** | ✓ 25/10 (2 640 → 2 494) | CẦN · 2 640 · hai hộp thiếu ≥2 ô; không có hướng B N→S, bàn tay trái, cân (đề 2025 II.2) |
| l12-thuc-hanh-cam-ung-tu | 12 | 2 | Đo B theo I và theo số vòng — T7, T8 | ✓ 25/10 (2 556 → 2 496) | CẦN · 2 556 · T2 nặng: mở bài + video lộ "1,45 g"; `<h4>Thử trên mô phỏng</h4>` trống; tn-03/-04 không có hộp |
| l12-cam-ung-dien-tu | 13 | 3 | Faraday: nam châm và cuộn dây (có số liệu), quay khung — giả thuyết từ thông đổi | đăng 25/10 (nhánh cfad9c, chưa kiểm chéo); soát 25/10: Faraday đủ 6 ô, số liệu + Lenz đúng; còn: chú thích Hình 2 + hộp rule trước hộp Faraday lộ kết quả (T2); Coi rằng trong details (T6); hộp khung quay vẫn 3 ô, Quan sát chứa suy luận (T3); Câu 2 thiếu ý "giới hạn"; chưa có thanh trượt trên ray → vá ở Lô 6 | CẦN · 2 505 · Faraday thiếu 3 ô; T3 hộp khung quay; không có thanh trượt trên ray (đề 2026 III.1–2) |
| l12-dong-dien-xoay-chieu | 14 | 3 | Máy phát mini quay tay; hai LED ngược chiều | | NÊN · 1 920 (còn 580 từ) · T5, T6, T7 cách giảm |
| l12-hat-nhan-mo-hinh-nguyen-tu | 15 | 3 | Tán xạ alpha Rutherford | ✓ 25/10 | mẫu |
| l12-nang-luong-lien-ket | 16 | 3 | Phổ kế khối lượng (đo khối lượng hạt nhân → độ hụt khối) | | CẦN · 2 525 · phổ kế khối lượng thiếu ≥2 ô; Dự đoán hỏi kết luận |
| l12-phan-hach-nhiet-hach | 17 | 3 | Cân khối lượng tìm năng lượng toả ra; bàn ghim dây chuyền (mô hình) | | NÊN · 2 559 · không có thí nghiệm thật; đổi nhãn "Cân khối lượng" → Ví dụ, vá T7 |
| l12-phong-xa | 18 | 2 | Đo nhịp đếm theo thời gian → đọc T (T8 bảng, T7 nền phông) | | CẦN ưu tiên · 2 596 · T2 mở bài lộ "máy vẫn kêu đúng nhịp"; LỖI SỐ: bảng hộp 2 chưa trừ phông 23 xung/phút (mốc cuối 24) |
| l12-an-toan-phong-xa | 19 | 1 | Suất liều theo khoảng cách — T8 tỉ lệ nghịch bình phương | | CẦN (nhẹ) · 2 559 · hộp 1/r² thiếu ô; thêm cột N·d²; số liệu khớp mô hình tuyệt đối |
| l12-may-phat-dien-bien-ap | 125 | 4 | Quay đều đếm tần số; biến áp đo U1/U2 theo N1/N2 — T8 | | NÊN · 2 604 · hộp biến áp khá, thêm Giả thuyết/Dự đoán/Chưa nói + cách giảm |
| l12-ung-dung-cam-ung-dien-tu | 126 | 2 | Bếp từ đun 1 lít nước (đo hiệu suất) — T7. **Chỉ thư mục này khớp DB**; `l12-ung-dung-cam-ung.cu` là bản nháp, bỏ | | CẦN · 2 507 · T2 mở bài lộ "kính chỉ hơi ấm"; bếp từ không chiều sai số, không đối chứng |
| l12-dien-tu-truong-song-dien-tu | 127 | 2 | Nam châm rơi qua ống dây; dòng xoay chiều qua tụ | | NÊN · 2 474 · vá T6, T7, T9, ghi nguồn số liệu |

Rà 25/10/2026 (20 bài còn lại): **16 CẦN, 4 NÊN, 0 đạt**. Không bài nào có khung 6 ô, dòng Coi rằng/Bỏ qua, ô Chưa nói được gì, quiz trộn 4 kiểu, hay trường T11 trong JSON. 8 bài lộ kết quả trước Dự đoán (T2). 17/20 bài đã vượt trần 2 500 từ TRƯỚC khi sửa → cắt theo mục 3 trước khi thêm ô.
Thứ tự đề xuất: 5 → 12 → 18 → 11 → 13 → 2 → 8 → 3 → 126 → 4 → còn lại (bài 5, 12 là hai dạng đề đã ra; bài 18 có lỗi số liệu).

## 2. Quy trình cho MỘT bài

1. **Đo trước**: `python3 .claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py <dir>/theory.html` — ghi số từ hiện ngay. Khung 6 ô dài gấp đôi 3 ô (+120–180 từ/hộp), nên bài ≥ 2 300 từ phải chuẩn bị chỗ cắt ngay từ đầu (mục 3).
2. **Soát hộp** theo checklist mục 3 của `docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md`; ghi ra 3–6 dòng "bài này thiếu ô nào, lộ kết quả ở đâu" trước khi sửa. Đối chiếu đề thật nếu có câu cùng thí nghiệm (`~/Documents/THPT/Lop12/Ngan_hang_de/`), lấy đúng từ ngữ của đề (T10).
3. **Sửa `theory.src.html` bằng script Python** có `assert` chuỗi cũ (như `scratchpad/sua_bai14.py` của phiên 25/10): không sửa tay trong editor, không sửa `theory.html` (file sinh). Mẫu HTML:
   - Hộp 6 ô: `<div class="tl-box tl-box--exp tl-note" data-exp="tn-l12-<slug>-NN">` + `<ol class="tl-steps">` với 6 `<li><strong>Ô:</strong> …</li>`; ô "Dụng cụ và cách đo" chứa `<details class="tl-details tl-more">` nếu dài; dòng "Coi rằng/Bỏ qua" in đậm chữ đầu (T6).
   - Bảng số liệu thật + câu "em tự tính ô cuối" → `<details>` ngay sau hộp (T8), kèm `<small>` nguồn.
   - Quiz sau hộp: "phát biểu nào sai?" 4 phương án A–D = hiện tượng / kết luận / cơ chế / giới hạn, một ý sai; dòng `⚠ Khung: hiện tượng – kết luận – cơ chế – giới hạn.`; feedback nhắc đúng tên phương án.
   - PhET có hai mô hình: bước 1 chạy mô hình sai (T12).
4. **File `tn-*.json`**: thí nghiệm lịch sử → file mới `loai: "vi_du"` với `gia_thuyet`, `du_doan_neu_dung`, `khong_chung_minh`; thí nghiệm đo có sẵn → chỉ bổ sung 3 trường đó + `sai_so_thuong_gap` có chiều. `so_lieu_mau` phải khớp bảng trong bài (kiểm bằng script, không bằng mắt — bài học 22/25 của skill soạn bài).
5. **Build + kiểm**: `python3 build_figs.py` (trong thư mục bài; sinh `theory.html`) → `build_bundle.py` → `lint_theory.py`, `lint_do_dai.py` (0 lỗi cứng), `check_quizzes.py`, `thi_nghiem.py` (lỗi `video-theo-bai.json` của bài `cd*` là của phiên khác, bỏ qua) → `build_preview.py <theory.html> <dir>/xem-thu` + `chup_anh.py <dir>/xem-thu`.
6. **Kiểm chéo** bằng agent `kiem-code` (ảnh 375px + tự tính lại bảng, tự giải quiz, kiểm "kết quả không lộ trước Dự đoán", `grep thầy`). Ảnh chỉ agent đọc.
7. **Đăng** (Mac): `bash scripts/cap-nhat-ly-thuyet.sh <dir>/theory.html <id> --yes` trong tab terminal, đọc dòng "đã đối chiếu trước/sau: N mục khác không đổi". Worktree không có `.env.local` → chạy từ `/Users/MAC/Projects/thachlab` với đường dẫn tuyệt đối tới `theory.html` (script cùng bản). Ghi tên file sao lưu `scripts/logs/ly-thuyet-bai<id>-backup-*.json` vào báo cáo, không in lệnh hoàn tác.
8. **Ghi sổ**: đánh ✓ + ngày vào bảng mục 1 ở đây và bảng "Bài đã áp dụng" trong `docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md`; commit theo đường dẫn (`theory.src.html`, `theory.html`, `bundle.json`, `tn-*.json`, `index.json`, hai file docs); không commit `xem-thu/`.

## 3. Giữ hạn mức độ dài khi hộp dài ra (thứ tự ưu tiên cắt)
1. Dụng cụ + Làm → `<details>` trong `<li>` (giữ 4 ô còn lại hiện ngay).
2. Bảng số liệu → `<details>` (T8 cho phép).
3. Thí nghiệm mô hình/analog (bắn bi, bàn ghim…) → `<details>` giữ `data-exp`.
4. Gạch đầu dòng trùng ý với hộp hoặc với hình/bảng ở mục khác → bỏ; hình đặt sai mục → chuyển về mục đúng thay chữ (H1).
5. Quiz: rút ngắn phương án, không rút feedback (feedback không tính vào "hiện ngay").
6. Vẫn vượt 2 500 → DỪNG, hỏi thầy tách mục/tách bài; không cắt Bẫy/Trả bài để lấy chỗ.

## 4. Chạy song song nhiều bài
Prompt chép sẵn cho phiên chính (A), agent `general-purpose` soạn một bài (B), agent `kiem-code` (C) và lệnh đăng (D), kèm bảng 8 lô: `prompts.md` cùng thư mục.
Mỗi agent một thư mục bài + bộ `tn-l12-<slug>-*.json` riêng → không đụng nhau. File dùng chung chỉ **thêm dòng**: `content/thi-nghiem/index.json` (sinh lại bằng `thi_nghiem.py`, lấy bản cuối), bảng mục 1 ở đây, `docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md` mục 4, `docs/STATE.md`. Prompt agent chép nguyên mục 2–3 + bảng ký hiệu của chương (bài học 7/10 skill soạn bài).

## Nhật ký rút kinh nghiệm
- 2026-10-25 · Bài 14: khung 6 ô + bảng số liệu đẩy bài từ 2 508 lên 2 800 từ hiện ngay; cắt về 2 497 bằng đúng thứ tự mục 3 (details cho Dụng cụ/bảng/analog, chuyển Hình 2 về đúng mục thay 3 gạch đầu dòng). Đo lint TRƯỚC khi sửa để biết quỹ chữ. Worktree thiếu `.env.local` → đăng từ checkout chính với đường dẫn tuyệt đối.
- 2026-10-25 · Lô 1 (bài 5, 4) chạy song song 2 agent soạn + 2 kiem-code: cả hai về ~2 490 từ nhờ cắt theo mục 3 (bảng/hình/hộp phụ vào details, rút phương án quiz). kiem-code bắt được feedback gọi sai tên loại phương án (gọi ý "chiều mất nhiệt" là "giới hạn") → khi viết quiz T9, ghi nhãn loại cho TỪNG phương án trong script trước rồi mới viết feedback. kiem-code hai lần đề nghị bỏ dòng "⚠ Khung" — giữ vì là mẫu chuẩn bài 14; nêu sẵn điều này trong prompt C để khỏi tranh luận lại. Agent soạn nhớ `git checkout -- index.json` sau `thi_nghiem.py`, phiên chính sinh lại một lần.
- 2026-10-25 · Lô 2 (bài 12, 11): kiem-code bắt lộ kết quả ở TIÊU ĐỀ mục I và dòng MỤC TIÊU đầu bài ("cân chỉ đổi số", "cân đo được lực") — prompt B phải nói rõ T2 áp cả tiêu đề h3, mục tiêu, aria-label của hình, chú thích video. Phát hiện phiên khác (nhánh local `claude/cap-nhat-thi-nghiem-l12-cfad9c`, chưa push) đã đăng id 5, 11, 13, 7, 4 lúc 17:13 mà không ghi sổ vào main → Lô 1, 2 ghi đè 5, 4, 11. TRƯỚC KHI ĐĂNG: đọc dòng "Khác biệt ngoài khối video" của cap-nhat-ly-thuyet.sh ở chế độ xem thử; DB khác ở chỗ mình không sửa = DB có bản chưa vào git → dừng, tra `git log --all -S '<chuỗi DB>'`.
- 2026-10-25 · Lấy bản id 7, 13 của nhánh cfad9c vào main (khớp DB) và soát bằng kiem-code: bản Sonnet không qua kiểm chéo vẫn phạm T2 (công thức/kết luận đứng TRƯỚC hộp), T6 (Coi rằng nhét trong details) và lộ đáp số ô "em tự tính" ngay cạnh bảng → kiem-code là bước bắt buộc, không bỏ dù agent soạn báo lint sạch.
