# Góp ý sau buổi chạy thử bài 23 Điện trở. Định luật Ohm (học sinh ảo, 6 điểm dừng)

**src** = `tren-lop.src.html` · **ghi chú** = `tren-lop-ghi-chu.html` · **.mjs** = `scripts/ruot-tap/l11-bai23.mjs`. Số ô [n] theo `sach-trong.md`.

| # | file · vị trí | sửa gì | ưu tiên | bằng chứng |
|---|---|---|---|---|
| 1 | src `#m6bd` (đáp án A và dòng "gần nguội 5,9 Ω; sáng đủ 12 Ω") | Số trên màn chỉ cho khoảng 2 lần, nhưng đáp án nói "mười mấy lần". Đổi đáp án thành "Dây tóc nguội có $R$ nhỏ hơn nhiều lúc sáng" (bỏ "mười mấy"), hoặc thêm dòng "dây tóc 4,0 Ω ở 20 °C, 48 Ω khi sáng (bài toán mẫu ô 17·2)" để khớp. Ghi 5,9 Ω là "gần nguội", không phải nguội. | cao | hs-6 "chỉ gấp khoảng 2 lần… chưa khớp 'mười mấy lần'" |
| 2 | src `#m3d` (ô mở `a3`) + ghi chú ĐD3 | Thêm một dòng giải thích vì sao độ dốc tốt hơn lấy một hàng/trung bình: "dùng cả 5 điểm, sai số từng điểm triệt nhau". | cao | hs-3 ô [37] ghi "trung bình" rồi "chưa hiểu vì sao độ dốc tốt hơn" |
| 3 | src `#m4b` dừng ② (so-lon "0,33/0,17 ≈ 1,9") | Thêm dòng "6,0 V: 0,50 A; 0,50/0,17 ≈ 2,9 lần" để khớp ô [67] "U tăng 6 lần, I tăng …". | cao | hs-4 ô 67 "số này không ai chỉ, em tự tính" |
| 4 | src `#m3d` + .mjs p2 ô 14·1 Sai số | Công thức $\Delta U/U+\Delta I/I$ chưa dạy ở màn nào. Thêm một dòng trên màn 3d: "sai số tương đối của R ≈ ΔU/U + ΔI/I". | vừa | hs-3 vướng (3) |
| 5 | src `#m4d` | Thêm "ρ: điện trở suất" ở dòng $\rho=\rho_0[\ldots]$ (ρ chỉ nhắc ở ô 14·3 về nhà). | vừa | hs-4 ô [78] "chỉ chép công thức" |
| 6 | src `#m4a` | Ô [57]: nói rõ "dao động nhiệt" là rung quanh vị trí nút mạng khi nóng. Một dòng trên màn. | vừa | hs-4 ô 57 "(đoán)… quanh nút mạng hay nhiệt" |
| 7 | src `#m5d` | Ghi trên màn "(1) đường liền đỏ, (2) đường đứt xanh" cho khớp hình Tập. | vừa | hs-5 vướng (3) |
| 8 | src `#m4b` dừng ①, `#m5a` dừng ① + .mjs bảng 15·2, 16·1 | Bảng in sẵn làm "dự đoán" thành phép tính. Giữ bảng in sẵn, nhưng đổi chữ trên màn từ "dự đoán" thành "đọc bảng, so sánh"; hoặc che hàng $I$ cuối. | vừa | hs-3 "dựa vào bảng I in sẵn"; hs-5 "hiệu từng cặp" |
| 9 | src `#m0` ↔ .mjs ô 13·1 | Ba mục tiêu trên màn mở khác ba mục của Tập 13·1: chép đúng ba mục của Tập lên màn mở. | vừa | hs-6 tích hết 13·1; nhật ký thầy mục 5 |
| 10 | .mjs p2 ô 14·1 caption `machDo` | Bỏ chữ "nối tiếp / song song" trong chú thích hình (trùng chỗ trống [19],[20]). | thấp | hs-3 điền từ lớp 9, không phụ thuộc chú thích |
| 11 | src `#m3c` | Ô [28],[29]: ghi trên màn "đồ thị cường độ dòng điện $I$ theo hiệu điện thế $U$". | thấp | hs-3 "hơi lẫn" |
| 12 | src `#m6a` / ghi chú | Gọi tên $t-t_0$ ("độ tăng nhiệt độ") ở màn 4d. | thấp | hs-6 câu 5 |
| 13 | .mjs ô 16·2 Bẫy 2 | Chữ trống [89] "Sai với …": chốt đáp án "NTC", bỏ "điện trở nhiệt" (có thể gạch chân trên màn clip). | thấp | hs-5 vướng (1) |
| 14 | lớp ảo | Ô [97]–[99] (đề 1218) không đo được vì lớp ảo không có đề. | thấp | hs-6 |

Tổng: cao 3, vừa 6, thấp 5.

## Đã xử lý (22/11/2026)
- Làm: #1 (đáp án 6bd bỏ "mười mấy lần", thêm 4,0→22 Ω ô 15·4), #2 + #4 (m3d: công thức sai số + vì sao độ dốc tốt hơn), #3 (m4b thêm 6,0 V: 2,9 lần), #5 + #12 (m4d: ρ, t−t₀), #6 (m4a: rung quanh nút mạng), #7 (m5d đường liền đỏ / đứt xanh), #8 (m4b ghi "đọc bảng, so sánh"), #9 (m0 chép đúng 3 mục tiêu 13·1), #11 (m3c tên đồ thị). Bỏ #10, #13 (thấp, sửa Tập không đáng), #14 (không đo được).
- Giảm 25 → 24 màn: bỏ m3f (PhET Ohm), chuyển link PhET vào ghi chú dạy.
- Kiểm máy ĐẠT (1280 + 1920, katex 0, 375px ok); PDF Tập `l11-bai23.mjs` không đổi, 12 trang.
