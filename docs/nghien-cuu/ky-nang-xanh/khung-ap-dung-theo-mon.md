# Khung áp dụng kỹ năng xanh theo mô-đun — mẫu trống và ví dụ CNC

Căn cứ: Thông tư 55/2026/TT-BGDĐT, Điều 5.3.a (xem [van-ban-phap-ly.md](van-ban-phap-ly.md)). Chưa có khung kỹ năng xanh quốc gia, nên 5 nhóm dưới đây lấy đúng 5 nội dung mà Điều 5.3.a liệt kê; cách gắn hoạt động vào nhóm là **đề xuất của người soạn**, cần bộ môn thống nhất trước khi dùng chung.

| Mã (tự đặt) | Nội dung theo TT 55/2026 Điều 5.3.a | Trong xưởng cơ khí thường là |
|---|---|---|
| X1 | Sử dụng tài nguyên hiệu quả | phôi, dao, dung dịch trơn nguội, khí nén |
| X2 | Tiết kiệm năng lượng | chế độ cắt, thời gian chạy không, tắt máy/bơm/đèn |
| X3 | Giảm chất thải | phân loại phoi, dầu thải, giẻ dầu, dao hỏng |
| X4 | Bảo vệ môi trường (và sức khoẻ người làm) | bụi dầu, da tiếp xúc dung dịch, nồng độ, thải bỏ đúng quy định |
| X5 | Thích ứng chuyển đổi xanh trong sản xuất | so sánh phương án (MQL, gia công khô), đề xuất cải tiến chỗ làm |

## Cách điền (3 bước)

1. **Liệt kê việc người học tự làm** có dính tới tài nguyên, năng lượng, chất thải. Chỉ tính việc tạo ra thứ nhìn thấy được; giảng viên nói thì không tính.
2. **Gắn mỗi việc với 1–2 mã X1–X5.** 3–5 dòng một bài là đủ; không cố phủ đủ 5 nhóm.
3. **Minh chứng là số đo hoặc sản phẩm**, không phải phiếu tự đánh giá. Nghiên cứu hiện có đều thấy "ý thức cao, thực hành yếu" khi chỉ hỏi ý kiến ([nghien-cuu.md](nghien-cuu.md), C1–C2, B4) — nên đo: kWh, ml dung dịch, kg phoi đã phân loại, % nồng độ, ảnh khu vực.

## Mẫu trống

**Mô-đun:** …  **Bài:** …  **Thời lượng:** …  **Người soạn:** …  **Ngày:** …

| # | Hoạt động của người học | Mã X | Dụng cụ / số đo | Minh chứng và tiêu chí đạt |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

**Tự soát**
- [ ] Mỗi dòng là việc người học làm, có sản phẩm hoặc số đo nộp được.
- [ ] Tiêu chí đạt công bố trước cho người học.
- [ ] Không thêm giờ lý thuyết riêng: hoạt động nằm trong nguyên công đang dạy.

## Ví dụ đã điền — CNC phay

**Mô-đun:** Gia công phay CNC  **Bài:** Phay hốc chữ nhật trên thép C45  **Thời lượng:** 1 buổi thực hành

| # | Hoạt động của người học | Mã X | Dụng cụ / số đo | Minh chứng và tiêu chí đạt |
|---|---|---|---|---|
| 1 | Đo công suất máy lúc **chạy không** (trục chính quay, không cắt) và lúc cắt ở hai chế độ có MRR khác nhau; tính năng lượng riêng J/mm³ | X2 | Đồng hồ kẹp hoặc ổ đo điện; đồng hồ bấm giờ | Bảng số đo + phép tính; chỉ ra chế độ nào tốn ít kWh hơn cho cùng thể tích phoi và giải thích bằng P₀ |
| 2 | Lập chương trình bỏ bớt đường chạy không và dừng chờ thừa (G00 vòng xa, M03 bật sớm) | X2, X1 | Mô phỏng CAM / màn hình máy | Thời gian chu trình trước–sau; giảm được ≥ 1 đoạn chạy thừa |
| 3 | Đo nồng độ dung dịch trơn nguội bằng khúc xạ kế, chỉnh đúng khuyến cáo của nhà sản xuất | X1, X4 | Khúc xạ kế | Ghi % đo được, % khuyến cáo, việc đã làm |
| 4 | Phân loại phoi thép / nhôm / giẻ dầu vào đúng thùng, cân phoi | X3 | Cân, thùng có nhãn | Ảnh khu vực máy sau buổi + số kg phoi theo loại |
| 5 | So sánh tưới tràn với MQL hoặc khí nén cho nguyên công này (đọc bảng số liệu, nêu ưu – nhược, chi phí, sức khoẻ) | X5, X4 | Bảng số liệu trong `nghien-cuu.md` mục D | Đề xuất 3–5 dòng có lý do và giới hạn |

### Gợi ý dàn bài cho hoạt động 1 (con số minh hoạ)

- Mô hình: năng lượng riêng e = P₀/MRR + k. Bóc chậm thì phần P₀ chia cho ít mm³ hơn → mỗi mm³ tốn hơn (Gutowski 2006).
- Ví dụ với mô hình đo trên máy Mori Seiki NV1500 (Diaz 2011: e = 1481/MRR + 3,7 J/mm³), bóc 20 cm³ = 20 000 mm³:
  - MRR 10 mm³/s → e ≈ 151,8 J/mm³ → ≈ 3,04 MJ ≈ 0,84 kWh, mất 2 000 s.
  - MRR 50 mm³/s → e ≈ 33,3 J/mm³ → ≈ 0,67 MJ ≈ 0,19 kWh, mất 400 s.
- **Số trên chỉ đúng cho máy đó.** Cho sinh viên đo trên máy của xưởng để ra P₀ và k riêng — đó chính là bài học. Giới hạn: MRR tăng thì mòn dao, độ nhám, an toàn cũng đổi; không tối ưu năng lượng bằng mọi giá.

### Chọn mức yêu cầu theo năm học (đề xuất)

| Người học… | Mức |
|---|---|
| làm đúng quy định có sẵn (phân loại phoi, tắt máy, đo nồng độ theo hướng dẫn) | 1 — năm 1 |
| tự đo, tự tính và so sánh hai phương án trên cùng nguyên công | 2 — năm 2 |
| đề xuất cải tiến có số liệu cho một quy trình xưởng hoặc doanh nghiệp thực tập | 3 — năm 3 / đồ án |
