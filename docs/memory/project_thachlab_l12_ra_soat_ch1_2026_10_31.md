---
name: project-thachlab-l12-ra-soat-ch1
description: Rà soát 4 bài L12 Chương 1 (Vật lí nhiệt, lesson 2–5) 31/10/2026 — 10 hình vẽ lại, ĐÃ ĐĂNG DB 31/10, chờ deploy bản tĩnh
metadata:
  type: project
---

4 bài `content/lesson-samples/l12-*`: su-chuyen-the (B1, lesson 2), thang-nhiet-do (B2, lesson 3), noi-nang-dl1 (B3, lesson 4), thuc-hanh-nhiet (B4, lesson 5) — lesson_id theo [[project-thachlab-vl12-chuong1-ly-thuyet]]. Rà 31/10: 10 hình SVG vẽ lại (B1 H1, H4; B2 H1; B3 H1, H2, H4; B4 H1–4), kiem-code soát vòng 1 đạt 10/10; vòng 2 góp ý nhỏ chưa soát độc lập. Commit e223b5280, 82b79c2a7, 18726bef4, dbf27f8bb. Sửa nội dung: B1 "Mang về: 5 hình" → 4; B2 câu Fahrenheit (32/212 °F là mốc hiệu chỉnh về sau); B3 "miếng sắt nhỏ … có thể nhỏ hơn".

**Treo chờ thầy:** B1 video "thăng hoa của iốt" gắn ngay sau hộp thí nghiệm bay hơi `tn-l12-chuyenthe-03` (mốc `<!--video:sau:…-->`); B4 bài toán mẫu L đo ra 6,80·10⁶ (gấp 3 tra bảng, hao 67% nhiệt — số cố ý để bẫy chia nhầm m₁ nhưng khó tin là phép đo thật).

**Why:** để phiên sau không rà lại chương này. **How to apply:** đã đăng DB 31/10 (sau khi gộp thẻ "Thử nghĩ" 1f0303d0b — nhánh claude/ice-water-experiment-description-827f6e chưa vào main, bài L12 khác đăng lại phải gộp trước); còn `bash scripts/deploy.sh` cho bản tĩnh.
