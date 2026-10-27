---
name: project_thachlab_khung_chuong_bai
description: Khung trang chương ↔ trang bài theo bản duyệt 26/10/2026 và đợt nới màn rộng ≥1280 (27/10)
metadata:
  type: project
---

Khung trang chương (`.lesson-layout--pick`, `components/lessons/class-overview.css`) và trang bài (`.lesson-layout--rail`, cuối `app/globals.css`) làm khớp trang mẫu https://claude.ai/artifact/USkMkiVrmdq6AyLsyFcxH2 ngày 26/10/2026 (rail 248 + cột 720, khung 1200).

- 2026-10-27 · Màn ≥1280 (commit be2b2e1e8): biến `--wide-bleed` nới thẻ lý thuyết + cột giữa trang chương tới mép 100vw−72px; chữ giữ 646px/62ch, chỉ PhET/video/bảng (max-content)/hình khổ ≥600 hoặc `.fig--wide` lan; trang chương 2 cột; `.hub-grid` 3 cột; <1280 giống từng byte. Hướng 2 (cột lề kiểu Tufte cho `.tl-fn`/`.tl-term`/`.tl-nums`) mới là trang mẫu https://claude.ai/artifact/BXikspAiK5RZ9EteMUEc8C, chờ thầy duyệt 2 câu (định nghĩa hiện sẵn hay bấm mới hiện; ô số ở lề vẫn che). [[project_thachlab_nen_sang]]
