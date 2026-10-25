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

| Thư mục `content/lesson-samples/` | id | Hộp exp | Kinh điển cần khung 6 ô | Xong |
|---|---|---|---|---|
| l12-su-chuyen-the | 2 | 3 | Đun nước đá ghi nhiệt độ mỗi phút (đồ thị nóng chảy/sôi) — T7, T8 | |
| l12-thang-nhiet-do | 3 | 4 | Kiểm hai mốc 0 °C và 100 °C; trộn nước nóng–lạnh (giả thuyết nhiệt độ cân bằng) | |
| l12-noi-nang-dl1 | 4 | 2 | Bơm xe nóng ở đâu (giả thuyết: công → nội năng); nên THÊM thí nghiệm Joule (cánh khuấy) dạng `vi_du` | |
| l12-thuc-hanh-nhiet | 5 | 2 | Đo nhiệt dung riêng (đề 2026 II.4) và nhiệt nóng chảy riêng (đề 2025 II.1): giai đoạn đối chứng, "coi rằng/bỏ qua", chiều mất mát — T6, T7 **ưu tiên 1** | |
| l12-thuyet-dong-hoc-phan-tu | 6 | 3 | Chuyển động Brown (hạt khói) — giả thuyết phân tử chuyển động | |
| l12-boyle-charles | 7 | 2 | Nén khí xilanh (Boyle), cột khí áp suất không đổi (Charles) — T8 tích/tỉ số không đổi | |
| l12-phuong-trinh-trang-thai | 8 | 2 | Bình kín ngâm nước năm nhiệt độ — T8 | |
| l12-ap-suat-dong-nang | 9 | 2 | Áp suất khí theo nhiệt độ trong bình kín — T8 | |
| l12-khai-niem-tu-truong | 10 | 3 | Oersted (dòng điện lệch kim la bàn): giả thuyết – quan sát – giới hạn | |
| l12-luc-tu-cam-ung-tu | 11 | 2 | Đo lực từ bằng cân/dây treo (đề 2025 II.2): hướng B, hướng lực, cân tăng/giảm — **ưu tiên 2** | |
| l12-thuc-hanh-cam-ung-tu | 12 | 2 | Đo B theo I và theo số vòng — T7, T8 | |
| l12-cam-ung-dien-tu | 13 | 3 | Faraday: nam châm và cuộn dây (có số liệu), quay khung — giả thuyết từ thông đổi | |
| l12-dong-dien-xoay-chieu | 14 | 3 | Máy phát mini quay tay; hai LED ngược chiều | |
| l12-hat-nhan-mo-hinh-nguyen-tu | 15 | 3 | Tán xạ alpha Rutherford | ✓ 25/10 |
| l12-nang-luong-lien-ket | 16 | 3 | Phổ kế khối lượng (đo khối lượng hạt nhân → độ hụt khối) | |
| l12-phan-hach-nhiet-hach | 17 | 3 | Cân khối lượng tìm năng lượng toả ra; bàn ghim dây chuyền (mô hình) | |
| l12-phong-xa | 18 | 2 | Đo nhịp đếm theo thời gian → đọc T (T8 bảng, T7 nền phông) | |
| l12-an-toan-phong-xa | 19 | 1 | Suất liều theo khoảng cách — T8 tỉ lệ nghịch bình phương | |
| l12-may-phat-dien-bien-ap | 125 | 4 | Quay đều đếm tần số; biến áp đo U1/U2 theo N1/N2 — T8 | |
| l12-ung-dung-cam-ung-dien-tu | 126 | 2 | Bếp từ đun 1 lít nước (đo hiệu suất) — T7. **Chỉ thư mục này khớp DB**; `l12-ung-dung-cam-ung.cu` là bản nháp, bỏ | |
| l12-dien-tu-truong-song-dien-tu | 127 | 2 | Nam châm rơi qua ống dây; dòng xoay chiều qua tụ | |

Thứ tự đề xuất: 5 → 11 → 13 → 7 → 4 → còn lại (hai bài đầu là hai dạng đề đã ra 2025–2026).

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
Mỗi agent một thư mục bài + bộ `tn-l12-<slug>-*.json` riêng → không đụng nhau. File dùng chung chỉ **thêm dòng**: `content/thi-nghiem/index.json` (sinh lại bằng `thi_nghiem.py`, lấy bản cuối), bảng mục 1 ở đây, `docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md` mục 4, `docs/STATE.md`. Prompt agent chép nguyên mục 2–3 + bảng ký hiệu của chương (bài học 7/10 skill soạn bài).

## Nhật ký rút kinh nghiệm
- 2026-10-25 · Bài 14: khung 6 ô + bảng số liệu đẩy bài từ 2 508 lên 2 800 từ hiện ngay; cắt về 2 497 bằng đúng thứ tự mục 3 (details cho Dụng cụ/bảng/analog, chuyển Hình 2 về đúng mục thay 3 gạch đầu dòng). Đo lint TRƯỚC khi sửa để biết quỹ chữ. Worktree thiếu `.env.local` → đăng từ checkout chính với đường dẫn tuyệt đối.
