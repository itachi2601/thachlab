# Khung bài "Vật lý quanh ta"

## Frontmatter (bắt buộc)

```yaml
---
title: "Vì Sao Nồi Áp Suất Nấu Chín Nhanh Hơn?"   # câu hỏi, ≤ 70 ký tự
description: "…"                                  # 1–2 câu, 120–180 ký tự, nói được câu trả lời ngắn gọn (SEO)
date: "2026-10-10"
author: "Thầy Thạch"
category: "Vật lý quanh ta"                       # đúng chuỗi này
tags:
  - "Nhà bếp"                                     # 1 nhóm đời sống (xem kho-chu-de.md)
  - "Lớp 12"                                      # khối có bài liên quan: "KHTN 9", "Lớp 10", "Lớp 11", "Lớp 12"
keywords:
  - "vì sao nồi áp suất nấu nhanh"
  - "vật lý quanh ta"
  - "ThachLab"
cover: "/images/blog/<slug>-cover.png"            # tuỳ chọn
---
```

Slug = tiêu đề không dấu, gạch nối, bỏ "vi-sao" thừa nếu quá dài: `vi-sao-noi-ap-suat-nau-nhanh`.

## Thân bài — đúng thứ tự, tiêu đề mục `##` giữ nguyên chữ in đậm dưới đây

1. **Mở (không tiêu đề, 2–4 câu).** Một cảnh em đã thấy, cụ thể, có giác quan: "Tiếng xì của van nồi áp suất…".
   Kết bằng chính câu hỏi. Ngay sau đoạn mở: **hình 1 — cảnh đời sống** + chú thích in nghiêng.
2. **`## Đoán thử trước khi đọc`** — 2–3 phương án, có ít nhất 1 phương án "nghe hợp lý mà sai" (quan niệm sai phổ biến).
   Dặn: "Chọn một đáp án trong đầu rồi đọc tiếp." (dự đoán trước làm người đọc nhớ lâu hơn — hiệu ứng thế hệ/kiểm tra trước).
   Câu trả lời đúng phải lộ ra ở mục kế tiếp, nói rõ phương án nào đúng.
3. **1–3 mục giải thích** (`## …` tiêu đề là một ý, không phải "Phần 1"). Đi từ cái thấy được → đại lượng → định luật.
   Mỗi mục một ý chính, in đậm từ khoá 1–2 lần/mục, không hơn. Đặt **hình 2 — sơ đồ vật lí** (có nhãn đại lượng)
   ở mục giải thích chính. Cả bài cần **≥ 2 hình** (tối đa 4).
4. **`## Thử ước lượng bằng số`** — một phép tính 3–5 dòng bằng công thức trong sách (Unicode, có đơn vị), số làm tròn,
   kết luận bằng lời ("tức là gấp khoảng 3 lần…"). Đây là chỗ cho em thấy Vật lí *đo được*, không chỉ kể chuyện.
5. **`## Tự thử ở nhà`** — 3–5 bước đánh số, dụng cụ an toàn, "Em sẽ thấy…", "Vì sao?" (một câu nối lại lý thuyết).
   Không có thí nghiệm an toàn thì thay bằng "Quan sát ở nhà" (quan sát chứ không làm).
6. **`## Hiểu lầm hay gặp`** — 1–3 gạch đầu dòng dạng "❌ … → ✅ …".
7. **`## Em đã học ở đâu?`** — gạch đầu dòng, mỗi dòng một bài: `[Lớp 12 · Bài 6. …](/lop-hoc/bai?id=…&subject=vat-ly&chapter=…)`
   (lấy bằng `kiem-bai.py --tim`). Bài chưa có trên web thì ghi tên bài SGK, không link.
8. **`## Nghĩ tiếp`** — 1–2 câu hỏi mở nối sang hiện tượng khác (giữ tò mò), có thể kèm "Gợi ý:" một dòng. Không đưa đáp án đầy đủ.
9. **`## Nguồn`** — gạch đầu dòng: `[Tên nguồn — tên bài](https://…) (ngày)`. SGK ghi "SGK Vật lí 12 (KNTT), Bài …".

## Câu tốt / câu xấu

- ✓ "Ở đỉnh Fansipan, nước sôi ở khoảng 90 °C, nên luộc trứng lâu chín hơn ở Hà Nội."
- ✗ "Nồi áp suất là một phát minh vĩ đại làm thay đổi căn bếp!" — sáo rỗng, không có đại lượng.
- ✓ "Áp suất là lực ép lên mỗi mét vuông: p = F / S." (định nghĩa ngay khi dùng)
- ✗ "Do hiện tượng nhiệt động lực học phức tạp…" — né giải thích.
- ✗ Dồn 4 công thức vào một mục; giải thích bằng kiến thức đại học không báo trước.
- ✗ "Các nhà khoa học đã chứng minh…" mà không nói ai, ở đâu, đo gì.
