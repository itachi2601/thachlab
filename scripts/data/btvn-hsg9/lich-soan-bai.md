# Lịch soạn nội dung web cho khoá HSG Vật lí 9 (giao Opus, thầy duyệt)

Lập 16/10/2026 từ `31_lo-trinh-17-buoi-thu-7.md`. Quy trình mỗi chuyên đề: skill `soan-bai-hsg9` (`.claude/skills/soan-bai-hsg9/SKILL.md`) (4 subagent song song → 2×kiem-code → sửa → ghi bằng `cap-nhat-ly-thuyet.sh` + `publish-bai-tap-mau.mts`). Bật Hiện sau khi thầy duyệt, TRƯỚC ngày `gui_ngay` của tuần dùng bài đó (xem `tuan.json`), vì thông báo chỉ gắn link bài đã Hiện.

| Hạn bật Hiện | Bài (id) | Cần có | Dùng ở buổi |
|---|---|---|---|
| đang Hiện | CĐ00 (160), CĐ01 (161), CĐ02 (166), CĐ10 (155), CĐ11 (154), CĐ13 (162), BT tuần (167) | thiếu 6+ câu `luyen_tap` tự chấm mỗi bài (hiện chưa có) | 3–6 |
| 14/11 | CĐ12 Nhiệt (153), CĐ16 Truyền nhiệt (164) | ĐÃ GHI DB 16/10 (lý thuyết, 6 dạng + 8 tự luận, luyện tập 8 câu: đề 932, 931), đã deploy; chờ thầy duyệt + bật Hiện | 7 (21/11) |
| 21/11 | CĐ03 Ohm (159) | đã ghi DB, cần thầy duyệt + Hiện | 8 (28/11) |
| 28/11 | CĐ04 (157) | đã ghi DB, cần duyệt + Hiện | 9 (05/12) |
| 12/12 | CĐ05 (165) | đã ghi DB, cần duyệt + Hiện | 11 (19/12) |
| 26/12 | CĐ14 (158), CĐ06 (151), CĐ17 (178) | soạn mới trọn bộ | 13 (02/01) |
| 02/01 | CĐ07 Thấu kính (156) | soạn mới trọn bộ | 14 (09/01) |
| 16/01 | CĐ08 (152), CĐ09 (163), CĐ15 (150) | CĐ15 đã soạn (commit 40ad9346b), cần Hiện; CĐ08, CĐ09 soạn mới | 16 (23/01) |
| 05/12 | Bộ 12 câu tự luyện CĐ04 + CĐ05 | tuần 12 (26/12) dùng | 12 |
| 09/01 | 12 câu tự luyện CĐ07 | tuần 15 (16/01) dùng | 15 |

Đề: Thi thử 1 (12/12), Thi thử 2 (30/01), Thi thử 3 (20/02), Kiểm tra 1 (14/11), 2 (26/12), 3 (16/01) thầy cung cấp hoặc giao riêng. Hai đề tự làm trên web cho phiếu Tết cần có trước 30/01.
