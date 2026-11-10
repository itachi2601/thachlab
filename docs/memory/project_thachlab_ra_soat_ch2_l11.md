---
name: project_thachlab_ra_soat_ch2_l11
description: Rà nội dung + vẽ lại hình Ch.2 Sóng L11 (8 bài) 30/10/2026 — đã đăng 30/10 (lesson 27, 29–34; Bài 9 id 28 không đổi)
metadata:
  type: project
---
30/10/2026, skill `ra-soat-bai-hoc`, nhánh `claude/laughing-wozniak-3cb1e2`. 8 bài trong `content/lesson-samples/l11-*`:
mo-ta-song, song-ngang-song-doc (không đổi), song-dien-tu, giao-thoa-song, song-dung, thuc-hanh-do-tan-so-am, thuc-hanh-do-toc-do-am, bai-tap-song.
- Vẽ lại 13 hình (chữ 11–13 → ≥14, marker tam giác → chevron, Δφ ghi trên trục t → "trễ d/v", người que, ukulele hai elip chồng), chỉnh nhỏ 4 hình; kiem-code soát độc lập, 1 hình vòng 2 (tay cắt đầu Mô tả sóng H1) — vòng 2 CHƯA soát độc lập lại.
- Nội dung: đảo đáp án quiz dồn chữ B (Mô tả sóng q3/q4, Bài 14 7 câu), "Mang về" ghi sai số hình (Sóng dừng, Giao thoa), Bài 15 q5 e ≈ 0,55.
- lesson_id: Mô tả sóng = 27; còn lại tra DB chỉ đọc lúc đăng (dry-run cap-nhat-ly-thuyet.sh in tiêu đề).
- Treo thầy chốt: Bài 9 q3 (điện thoại chạm đáy bình?), dòng 🔑 nối "·" ở nhiều bài (lint cảnh báo), build_bundle exam Mô tả sóng answer 1,1,1,1,0 dồn B.
- Đăng: đã đăng 30/10 22h35 bằng `cap-nhat-ly-thuyet.sh … --yes` (lesson 27, 29–34; item 45/304/155/157/163/165/168), dry-run khớp tiêu đề, chỉ mục ly_thuyet đổi; `/data/lessons/*.json` 404 nên kiểm bằng REST, không deploy. Log `scripts/logs/dang-l11-ch2-2026-10-30.log`.
- Lượt 2 (cùng ngày, nhánh `claude/bai-hoc-chuong-2-lop-11-014673`, rà lại cả 8 bài): 5 bài sạch; sửa thêm Bài 10 H2 (núm/dây/nhãn) + H4 (trục t thiếu đầu V) + q4 4,4 % → 4,3 %; Bài 11 H1 (chảo hướng vệ tinh, người có dáng); Bài 8 H3 (nhãn u_M chồng t, chỉ số dưới 11 → 13) + `$v_{\text{rắn}}$`. kiem-code soát 4 hình: ĐẠT. Treo thêm: Bài 14 name radio q5/q6 đảo (không ảnh hưởng chức năng), Bài 11 dài 2.724 từ.
