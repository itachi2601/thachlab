# Bài 15. Tác dụng của dòng điện xoay chiều — KHTN 9 (lesson_id 93)

## Chặng hiện tại
Chặng 1 xong (soạn + kiểm máy + tự xem ảnh 375px), 18/11/2026. CHƯA kiểm chéo `kiem-code`, CHƯA commit, CHƯA đăng DB.

Dựng lại: `python3 build_figs.py && python3 build_bundle.py` (build_figs sinh SVG, theory.html, 2 file thí nghiệm).

## Ý bắt buộc (YCCĐ KHTN 9 — tác dụng dòng điện xoay chiều) — đã có đủ
- [x] Bốn tác dụng nhiệt, phát sáng, từ, sinh lí, mỗi cái có ví dụ đồ dùng trong nhà (mục II.1–4)
- [x] Tác dụng từ đổi chiều theo dòng: kim nam châm lệch một phía với dòng một chiều, rung tại chỗ với xoay chiều (TN1, Hình 2, Câu 3)
- [x] Tác dụng sinh lí + an toàn điện 220 V (aptomat, xử lí người bị điện giật, Câu 4)
- [x] Dụng cụ đo xoay chiều: kí hiệu AC / ~, chốt không phân cực, thang ACV của đồng hồ vạn năng (TN2, Hình 3)
- [x] Hiểu sai: "đổi chiều nên không nóng, đèn chớp thấy được" (Bẫy 1); "ampe kế một chiều đo được xoay chiều" (Bẫy 2)
- [x] Đọc nhãn thiết bị + A = P·t, tiền điện (V. Tình huống mẫu)
- [x] Giá trị hiệu dụng (chỉ trong details, mức giới thiệu)

## Số liệu kiểm
2.169 từ hiện ngay, 16 phút · 8 quiz + 2 câu hành trang · đáp án A/B/C/D = 2/2/2/2 · 3 hình · bundle 6 câu exam.
Mẹo 🧠: **Nóng – Sáng – Hút – Giật**.

## Đề xuất clip mở bài (chưa chèn)
Clip cận cảnh 10–15 giây: kim nam châm đặt cạnh nam châm điện; bật nguồn một chiều thì kim lệch hẳn một phía, chuyển sang xoay chiều thì kim chỉ rung tại chỗ. Không lời giải thích (để HS dự đoán ở Câu 3). Phương án dự phòng: quay chậm đèn LED bằng điện thoại, thấy nhấp nháy mà mắt thường không thấy.

## Treo
- Thêm mẹo "Nóng – Sáng – Hút – Giật" vào `docs/BANG-MEO-TU-KHOA.md` (file chung, chưa sửa).
- Chạy `thi_nghiem.py` trên kho thật khi gộp lô (cập nhật `content/thi-nghiem/index.json`); đã kiểm trên bản sao scratchpad: 2 file của bài không lỗi.
- Kiểm chéo bằng agent `kiem-code` (số liệu, quiz, hình).
- Đăng: lesson 93 chưa có lesson_items → dùng `upload-lesson.mts` / `/quan-tri/nhap-bai`, KHÔNG dùng `cap-nhat-ly-thuyet.sh`.
- `content/hanh-trang/l9-tac-dung-dong-dien-xoay-chieu.json` (đã chèn) cần commit cùng bài; không commit `xem-thu/`.
