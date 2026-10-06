---
name: project-thachlab-vi-du-doi-song-thay-xuong
description: 6/10/2026 thay ví dụ xưởng cơ khí/CNC bằng ví dụ đời sống ở 53 bài lý thuyết L10–L12; đã commit + ghi DB; quy tắc trong skill soan-bai-ly-thuyet-tuong-tac
metadata:
  type: project
---

6/10/2026: ví dụ "xưởng cơ khí/CNC" lẫn ~50 bài lý thuyết L10–L12 (HS chưa có khái niệm) → thay bằng xe đạp, thang máy chung cư, máy giặt, bếp từ… Commit 9adfeda66 + d840ea842, ghi DB 53 bài (log `scripts/logs/dang-ly-thuyet-hang-loat-20261006-223506.log`, sao lưu `ly-thuyet-bai<N>-backup-*.json`), deploy từ deploy-tree.

**Why:** thầy chốt ví dụ phải là thứ HS 15–18 tuổi gặp hằng ngày. Quy tắc đã ghi cuối SKILL.md `soan-bai-ly-thuyet-tuong-tac`.
**How to apply:** soạn bài mới → grep `xưởng|CNC|phôi|cầu trục|máy tiện|cơ khí` phải rỗng. Treo: `xem-thu/` đã commit của các bài vẫn là bản cũ còn chữ xưởng/CNC (sinh lại bằng build_preview + chup_anh hoặc gỡ khỏi git); 4 bài L10 mới (biến dạng, giải bài toán động lực học, khối lượng riêng–áp suất, thực hành tổng hợp lực) của phiên khác chưa commit, chưa kiểm ví dụ xưởng.
