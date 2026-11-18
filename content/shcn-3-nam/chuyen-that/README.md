# Kho "Chuyện người đi trước" — SHCN 3 năm

Kế hoạch: `docs/SHCN-KE-HOACH-CAU-CHUYEN-THAT.md`. Phiếu + tin mời: `phieu-va-tin-moi.md`. Mẫu biên tập: `_mau.md`.

Thư mục này **không** được `gen-shcn-bai-doc.mjs` hay `xuat-shcn-3-nam-docx.py` đọc. Chuyện chỉ lên web khi đã chép vào
mục `## Người đi trước kể` của bài `hk*/bNN.sv.md` rồi chạy lại gen.

## Quy trình một chuyện

1. Thầy nhận phiếu/bản chép lời → lưu gốc trên Mac `~/Documents/CTTC/Chuyen-that/` (không đưa vào repo).
2. Claude biên tập theo chuẩn mục 5 của kế hoạch → tạo `<ma>.md` ở đây, `duyet: ""`.
3. Thầy gửi bản biên tập cho người kể đọc lại → ghi ngày vào `duyet`.
4. Claude chèn vào `.sv.md` (+ phương án B ở Mở 2' của `.gv.md`), chạy `node scripts/gen-shcn-bai-doc.mjs`, cập nhật bảng dưới.

Mức đồng ý **c** (chỉ kể trong lớp): không tạo file ở đây — chỉ in ra giấy cho thầy.

## Khuôn file `<ma>.md`

```yaml
---
ma: tl-hk1-b10-01          # mảng-bài-số thứ tự
mang: TL                    # TL tự lập · HT hợp tác · LV làm việc
bai: hk1-b10
nguoi_ke: "Một thầy khoa Cơ khí, vào Cao Thắng năm 2005"   # mức a: tên thật + vai trò; mức b: chỉ vai trò
dong_y: b                   # a | b
duyet: ""                   # ngày người kể đọc lại bản biên tập, vd 2026-12-02
---

(150–250 chữ, ngôi thứ nhất)

**Bạn nghĩ sao:** (1 câu hỏi gợi mở)
```

## Bảng suất (29) — cập nhật mỗi khi thêm chuyện

| Mảng | Bài | Chủ đề bài | Người kể | Trạng thái |
|---|---|---|---|---|
| TL | hk1-b01 | Cao Thắng khác THPT | | trống |
| TL | hk1-b03 | Tiền tháng đầu | | trống |
| TL | hk1-b05 | Ở trọ/KTX, sống chung | | trống |
| TL | hk1-b06 | Ăn đủ chất 50.000đ/ngày | | trống |
| TL | hk1-b10 | Nhớ nhà và cô đơn | | trống — **ưu tiên** |
| TL | hk1-b13 | Khi bị ốm | | trống — **ưu tiên** |
| TL | hk2-b05 | Trì hoãn | | trống |
| TL | hk2-b13 | Đi làm thêm | | trống |
| TL | hk4-b13 | Đứng dậy sau thất bại | | trống |
| TL | hk6-b07 | Tháng lương đầu tiên | | trống |
| TL | hk6-b09 | Sống tự lập lâu dài | | trống |
| HT | hk3-b01 | Vì sao cần làm việc nhóm | | trống |
| HT | hk3-b02 | Các giai đoạn của nhóm | | trống |
| HT | hk3-b04 | Phân việc, hạn chót, biên bản | | trống |
| HT | hk3-b06 | Nói "không", nói điều khó | | trống |
| HT | hk3-b07 | Xung đột trong nhóm | | trống |
| HT | hk3-b08 | Góp ý và nhận góp ý | | trống |
| HT | hk3-b12 | Thuyết trình | | trống |
| HT | hk4-b05 | Kỹ sư thực hành giải quyết vấn đề | | trống |
| LV | hk4-b11 | Thái độ an toàn ở xưởng | | trống |
| LV | hk5-b01 | Trường học ≠ doanh nghiệp | | trống |
| LV | hk5-b02 | Tuần đầu đi làm | | trống |
| LV | hk5-b04 | Đúng giờ, báo khi trễ | | trống |
| LV | hk5-b06 | Chuẩn mực đạo đức nghề | | trống |
| LV | hk5-b07 | Trung thực số liệu, nhận lỗi | | trống |
| LV | hk5-b09 | Nhận việc, báo cáo cấp trên | | trống |
| LV | hk6-b04 | Phỏng vấn ứng tuyển | | trống |
| LV | hk6-b05 | Phỏng vấn thử | | trống |
| LV | hk6-b12 | Giữ quan hệ, nghỉ việc đúng cách | | trống |
