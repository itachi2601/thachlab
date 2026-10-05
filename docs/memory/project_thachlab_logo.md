---
name: project-thachlab-logo
description: Dấu ThạchLab — chén cầu, nêm, ròng rọc — từ phác thảo tay 5/10/2026
metadata:
  node_type: memory
  type: project
---

Dấu chính là hình thầy phác: chén cầu mặt cắt nghiêng, nêm đỡ, ròng rọc treo quả cân. Code: `components/brand/Logo.tsx` + `LogoMark.tsx`, favicon `app/icon.svg`, file tĩnh `public/brand/`, quy ước `docs/BRAND.md`.

**Why:** chữ T trong ô xanh không nói gì về vật lý. Phác thảo gộp cân bằng, nêm và ròng rọc — đúng cả THPT lẫn Cơ khí.

**How to apply:** đừng ghi "Vật lý 10" vào dấu navbar (dấu dùng cho mọi lớp). Chữ đó chỉ thuộc emblem nếu thầy muốn biến thể riêng. Footer marketing và sidebar quản trị luôn nền tối → `surface="dark"`. Đổi hình thì sửa cả component lẫn `public/brand/` và `app/icon.svg`, rồi sinh lại `public/images/logo.png`.
