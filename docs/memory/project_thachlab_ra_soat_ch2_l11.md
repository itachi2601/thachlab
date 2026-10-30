---
name: project_thachlab_ra_soat_ch2_l11
description: Rà nội dung + vẽ lại hình Ch.2 Sóng L11 (8 bài) 30/10/2026 — commit ở repo, CHƯA đăng DB, chờ thầy duyệt ảnh
metadata:
  type: project
---
30/10/2026, skill `ra-soat-bai-hoc`, nhánh `claude/laughing-wozniak-3cb1e2`. 8 bài trong `content/lesson-samples/l11-*`:
mo-ta-song, song-ngang-song-doc (không đổi), song-dien-tu, giao-thoa-song, song-dung, thuc-hanh-do-tan-so-am, thuc-hanh-do-toc-do-am, bai-tap-song.
- Vẽ lại 13 hình (chữ 11–13 → ≥14, marker tam giác → chevron, Δφ ghi trên trục t → "trễ d/v", người que, ukulele hai elip chồng), chỉnh nhỏ 4 hình; kiem-code soát độc lập, 1 hình vòng 2 (tay cắt đầu Mô tả sóng H1) — vòng 2 CHƯA soát độc lập lại.
- Nội dung: đảo đáp án quiz dồn chữ B (Mô tả sóng q3/q4, Bài 14 7 câu), "Mang về" ghi sai số hình (Sóng dừng, Giao thoa), Bài 15 q5 e ≈ 0,55.
- lesson_id: Mô tả sóng = 27; còn lại tra DB chỉ đọc lúc đăng (dry-run cap-nhat-ly-thuyet.sh in tiêu đề).
- Treo thầy chốt: Bài 9 q3 (điện thoại chạm đáy bình?), dòng 🔑 nối "·" ở nhiều bài (lint cảnh báo), build_bundle exam Mô tả sóng answer 1,1,1,1,0 dồn B.
- Đăng: chỉ khi thầy chốt, ngoài giờ HS, `bash scripts/cap-nhat-ly-thuyet.sh <bài>/bundle.json <id> --yes`.
