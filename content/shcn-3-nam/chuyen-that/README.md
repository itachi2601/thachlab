# Kho "Chuyện người đi trước" — SHCN 3 năm

**Giai đoạn 1 (18/11/2026):** 29 chuyện có thật từ báo chí/báo cáo chính thức ở `bai/*.md`, chèn vào bài bằng `node scripts/chen-chuyen-that-shcn.mjs` (mục `## Chuyện có thật` bản SV, `## Chuyện có thật — cách dùng` bản GV). Giai đoạn 2: thầy cô góp ý/bổ sung chuyện của mình theo phiếu.

Kế hoạch: `docs/SHCN-KE-HOACH-CAU-CHUYEN-THAT.md`. Phiếu + tin mời: `phieu-va-tin-moi.md`. Mẫu biên tập: `_mau.md`.

Thư mục này **không** được `gen-shcn-bai-doc.mjs` hay `xuat-shcn-3-nam-docx.py` đọc. Chuyện chỉ vào bài khi chạy
`node scripts/chen-chuyen-that-shcn.mjs` (khối giữa `<!-- chuyen-that:start/end -->`, chạy lại thay khối cũ); chỉ HK đã mở
trong `gen-shcn-bai-doc.mjs` mới hiện trên web. Chuyện thầy cô kể (gđ 2) thay file báo chí cùng suất trong `bai/`.

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
| TL | hk1-b01 | Cao Thắng khác THPT | Báo chí: Tuổi Trẻ, 24/10/2018 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| TL | hk1-b03 | Tiền tháng đầu | Báo chí: VnExpress, 18/10/2022 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| TL | hk1-b05 | Ở trọ/KTX, sống chung | Báo chí: Tuổi Trẻ, 28/8/2026 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| TL | hk1-b06 | Ăn đủ chất 50.000đ/ngày | Báo chí: Thanh Niên, 08/9/2023 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| TL | hk1-b10 | Nhớ nhà và cô đơn | Báo chí: Thanh Niên, 24/02/2022 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| TL | hk1-b13 | Khi bị ốm | Báo chí: VnExpress, 18/11/2024 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| TL | hk2-b05 | Trì hoãn | Báo chí: Dân trí, 11/02/2023 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| TL | hk2-b13 | Đi làm thêm | Báo chí: Thanh Niên, 23/8/2024 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| TL | hk4-b13 | Đứng dậy sau thất bại | Báo chí: VnExpress, 19/9/2019 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| TL | hk6-b07 | Tháng lương đầu tiên | Báo chí: VnExpress, 13/6/2013 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| TL | hk6-b09 | Sống tự lập lâu dài | Báo chí: Tuổi Trẻ, 07/7/2020 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| HT | hk3-b01 | Vì sao cần làm việc nhóm | Báo chí: Tuổi Trẻ, 18/9/2026 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| HT | hk3-b02 | Các giai đoạn của nhóm | Báo chí: Tuổi Trẻ, 03/6/2026 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| HT | hk3-b04 | Phân việc, hạn chót, biên bản | Báo chí: NASA, báo cáo Hội đồng điều tra Mars Climate Orbiter, 10/11/1999 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| HT | hk3-b06 | Nói "không", nói điều khó | Báo chí: Báo cáo Ủy ban Rogers về tai nạn tàu Challenger, chương V, 1986 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| HT | hk3-b07 | Xung đột trong nhóm | Báo chí: Thanh Niên, 03/6/2026 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| HT | hk3-b08 | Góp ý và nhận góp ý | Báo chí: Tuổi Trẻ, 17/9/2024 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| HT | hk3-b12 | Thuyết trình | Báo chí: Tuổi Trẻ, 09/01/2020 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| HT | hk4-b05 | Kỹ sư thực hành giải quyết vấn đề | Báo chí: This American Life (NPR), tập 403 "NUMMI", 26/3/2010 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| LV | hk4-b11 | Thái độ an toàn ở xưởng | Báo chí: Sức khỏe & Đời sống, 08/11/2026 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| LV | hk5-b01 | Trường học ≠ doanh nghiệp | Báo chí: VietNamNet, 06/9/2023 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| LV | hk5-b02 | Tuần đầu đi làm | Báo chí: Báo Thái Nguyên, 13/3/2012 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| LV | hk5-b04 | Đúng giờ, báo khi trễ | Báo chí: VnExpress (Góc nhìn), 28/9/2024 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| LV | hk5-b06 | Chuẩn mực đạo đức nghề | Báo chí: The New Yorker, 29/5/1995 (bài "The Fifty-Nine-Story Crisis" của Joe Morgenstern) | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| LV | hk5-b07 | Trung thực số liệu, nhận lỗi | Báo chí: VnExpress, 13/3/2023 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| LV | hk5-b09 | Nhận việc, báo cáo cấp trên | Báo chí: VietNamNet, 02/10/2016 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| LV | hk6-b04 | Phỏng vấn ứng tuyển | Báo chí: Tuổi Trẻ, 13/7/2025 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| LV | hk6-b05 | Phỏng vấn thử | Báo chí: Tuổi Trẻ, 18/7/2025 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
| LV | hk6-b12 | Giữ quan hệ, nghỉ việc đúng cách | Báo chí: VnExpress (Góc nhìn), 23/6/2026 | chuyện có thật (gđ 1) — chờ thầy cô bổ sung |
