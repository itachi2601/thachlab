# Góp ý lớp ảo · L10 Bài 23 (HS haiku: 10 ô đoán, 10 ô không có dữ liệu)

Lưu ý: HS ảo đọc tài liệu sạch (không có khối riêng thầy) nhưng vẫn chỉ là ước lượng; tin mục "phải đoán" và "lệch nhau".

| # | File · vị trí | Sửa gì | Ưu tiên | Bằng chứng |
|---|---|---|---|---|
| 1 | Tập ô 2·2 · chú thích hình dauCong | Chú thích bảo "Điền >, =, <" nhưng không có ô → đổi thành "Ghi dấu của A vào bảng bên trái" | cao | hs-3 "chỗ rối nhất" |
| 2 | Tập ô 3·3 · Trả bài câu 2 | Một dòng không đủ viết lần 1 + sửa → 2 dòng (giữ 12 trang) | vừa | hs-6, hs-4 |
| 3 | Màn m2a · "1 cal" | Màn 4,184 J, Tập ô 5·2 4,18 J → thống nhất 4,18 | vừa | hs-2 |
| 4 | Ghi chú dạy ĐD5 | Ghi chú nói bảng 3·1 chỉ in hai hàng, Tập in bốn hàng s → sửa lời | vừa | hs-5 |
| 5 | Màn m3b · hỏi α = 180° | Không có chỗ ghi A = −Fs; Tập ô 2·2 đã có dòng "ngược hướng: A =" nên đủ | bỏ | hs-3 (đã có chỗ) |
| 6 | Ô 3·3 bạn cùng bàn, 4·1 điểm đề 1244, 5·1 đề BTVN | Không có dữ liệu trong lớp ảo, bản chất là việc lớp thật | bỏ | hs-6 |
| 7 | Ô 1·2 lời giải, 2·4 lời giải câu 1–2 | HS đoán, dòng "Vì sao?" đủ cho bước đầu; không đổi | bỏ | hs-1, hs-4 |
| 8 | Ô 1·4 "cột đỏ", khối lượng bóng 57 g | Là chữ trên clip, không cần ô trong Tập | bỏ | hs-2 |
| 9 | Tập ô 4·5, tr.5 thiếu g | Bài về nhà, g = 10 đã ghi ở đầu Tập | bỏ | hs-6 |

## Đã xử lý
- #1: `hinh-l10-bai23.mjs` đổi caption dauCong.
- #2: `l10-bai23.mjs` Trả bài câu 2 lines(2); PDF vẫn 12 trang.
- #3: `tren-lop.src.html` m2a 4,184 → 4,18.
- #4: `tren-lop-ghi-chu.html` sửa lời ĐD5.
- Làm 4, bỏ 5 (nhóm #5–#9).
