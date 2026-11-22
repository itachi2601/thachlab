# Góp ý sau lớp ảo — L10 Bài 20 (Giải bài toán động lực học)

Nguồn: mục "phải đoán" trong hs-1..3, "lệch tài liệu" trong nhat-ky-thay.md, các "(đoán)" trong sach-hs.md. Không dùng tỉ lệ đúng.

| # | File | Vị trí | Sửa gì | Ưu tiên | Bằng chứng |
|---|---|---|---|---|---|
| 1 | scripts/ruot-tap/l10-bai20.mjs | ô 5·2 (tr.5) | bảng 6 dòng → "Đề 1241 (20 câu, cuối tiết)": Điểm /20 · câu sai · câu đoán mò | cao | nhat-ky-thay "Ô 5·2 lệch đề"; hs-3 chưa điền 91–96 |
| 2 | tren-lop.src.html | màn 4b | bỏ câu "Trong a còn m không?" khỏi trước clip, chuyển vào khối "rút ra" màn 4d | cao | hs-2: chọn C nhờ màn 4b đã lộ |
| 3 | .mjs | Đề BTVN (K.btvn) | thêm mã ô 5·1 | cao | hs-3 "Đề BTVN không có thông tin"; màn 6c nhắc "ô 5·1" |
| 4 | ghi chú | mục "thiếu giờ", ĐD3–5 | ghi rõ ô cho điền ở nhà (6 chỗ kéo xiên, 2 chỗ nằm yên, 2 chỗ sai số) | cao | nhat-ky-thay "rất dày"; ĐD3 9+6 ô, ĐD4 10, ĐD5 6+5+4 |
| 5 | .mjs | Bước 4 ô 1·5 | "theo Ox, Oy" → "chiếu lên Ox, Oy" | vừa | hs-1, nhat-ky-thay |
| 6 | .mjs | ô 3·2 | ghi 0,1 kg / 0,4 kg, "hai ván giống nhau nghiêng 30°" cho khớp màn 4c | vừa | hs-2 "Tập một ván, màn hai ván; khối lượng chỉ có trên màn" |
| 7 | tren-lop.src.html + ghi chú | màn 6c Về nhà | ô 4·2: bẫy 1, 2, 4 đã gặp trên lớp; bẫy 3 gợi "lực nào đổi chiều khi vật quay đầu" | vừa | hs-3 ô 75–76 (đoán); nhat-ky-thay "bẫy 3 chưa dạy" |
| 8 | tren-lop.src.html + ghi chú | màn 1b | "Khoanh vào Tập" → "viết chữ cái vào ô Em chọn" | vừa | hs-1 |
| 9 | tren-lop.src.html | CSS ≤760px, bảng màn 5e | `.bang` chữ 15px, rộng 100% (cuộn ngang 388px) | vừa | kiem-tren-lop.mjs: 375px scrollWidth 388 |
| 10 | .mjs | ô 4·3 câu 3 chỉ 1 dòng, 3 ý | thêm dòng | vừa | hs-3 ô 81 |
| 11 | .mjs/màn | câu A–D màn 4c, 5b, 5d không có chỗ ghi lựa chọn trong Tập | thêm dòng "Em chọn" | vừa | hs-2, hs-3 |
| 12 | màn 2a | ô 1·5 hiện sẵn chữ, không có nút Mở | thêm nút Mở | thấp | nhat-ky-thay |
| 13 | màn 5d | lời thầy "5 lần" nhưng clip chỉ hiện lần 1 | sửa | thấp | nhat-ky-thay |
| 14 | .mjs | "Câu 3" trùng nhau (ô 3·4 và ô 4·3), thứ tự điền 4·1 | đổi nhãn | thấp | nhat-ky-thay |
| 15 | .mjs | ô 53 (μ_n), 70 (sai số hệ thống), 98 (lực hãm) phải đoán | thêm định nghĩa | thấp | sach-hs "(đoán)", hs-2, hs-3 |

## Đã xử lý

Làm 1–9 (9 mục), bỏ 10–15 (6 mục).
- 1: ô 5·2 là một thẻ "Đề 1241 (20 câu, cuối tiết)"; PDF vẫn 12 trang (trước 12, sau 12), tr.5 dư 10 mm.
- 2: màn 4b chỉ còn phương trình Ox; câu về m nằm trong khối "quan sát, rút ra" của màn 4d (sau clip). Không thêm nút mới vì màn 4d tràn khi để thêm một khối.
- 3, 5, 6: sửa trong `l10-bai20.mjs`; ô 5·1 gắn nhãn bằng `K.btvn().replace`. Tập đã chạy lại, 12 trang, mọi trang dư ≥ 0 mm.
- 4: không cắt nội dung (ba ô nhỏ cho điền ở nhà), ghi vào mục "Nếu thiếu giờ" của ghi chú.
- 7: Tập giữ nguyên ô bẫy 3; chỉ gợi ý ở màn 6c và nói trên lớp, không lộ đáp án.
- 8, 9: sửa màn + ghi chú; kiểm máy đạt (1280×720, 1920×1080, 375px, katex-error 0); hình web sáng rõ trên nền trắng (xem m3b, m5a).
- Bỏ 10: trang 4 chỉ dư 2 mm, thêm dòng làm tràn sang 13 trang. 11: giơ tay là chủ ý của bước biểu quyết, Tập hết chỗ. 12: chủ ý, ô này chỉ để chép lại. 13, 14: lệch nhỏ, không gây sai. 15: ô về nhà, màn 4d/5e đã giải thích; để thầy quyết nếu muốn thêm chữ vào Tập.
