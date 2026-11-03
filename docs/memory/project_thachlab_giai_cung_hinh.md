---
name: project_thachlab_giai_cung_hinh
description: Giải cùng hình + tóm đề cho dạng bài tập mẫu — mẫu bài 33 D3 xong ở xem thử, kế hoạch 9 đợt Opus/Sonnet
metadata:
  type: project
---
Nâng dạng bài tập mẫu thành "giải cùng hình" (hình SVG dính nửa trên điện thoại, mỗi bước tự trả lời) + "tóm đề" (dòng Tìm đầu khối dính; ≥1280 thẻ Cho/Tìm ở lề ghi chú). Skill: `.claude/skills/cap-nhat-dang-bai-tap/` (SKILL.md + KE-HOACH-MODEL.md: 492 dạng, 16 họ hình, 9 đợt Đ1–Đ9).

Hiện trạng 3/11/2026: mẫu bài 33 (lesson_id 33) Dạng 3 `giao_thoa_2_nguon` chạy ở `/dev/btm`; code đã vào main qua nhánh `claude/wave-exercises-interactive-graphics-a3ea00`. **Chưa deploy, chưa đăng 33.json lên DB** (phải deploy code trước rồi mới publish JSON).


L10 Ch.3 Động lực học (3/11/2026, nhánh `claude/l10-ch3-giai-cung-hinh-be4044`): họ `so_do_vecto` + `thanh_moment` = một component `SoDoVecto.tsx` (cảnh mat_nghieng/mat_ngang/nut/rong_roc/ban_rong_roc/thanh); 10 dạng có hình (58 D5–D6, 60 D2/D4, 62 D4–D5, 63 D4–D5, 66 D4–D5) + tóm đề 18 dạng còn lại. Chưa deploy, chưa đăng JSON. Hở `tom_de` ở dạng không hình đã vá 3/11 (`TomDeKhung` trong `TomDe.tsx`).

**Why:** thầy muốn HS không phải cuộn qua lại giữa hình và lời giải (N8).
Đ1 (23, 27, 31) và Đ2 (2, 11, 26 — họ `do_thi`, `tu_truong`, `thanh_nang_luong`) xong ở xem thử 3/11, chưa deploy/chưa đăng JSON. Treo: dạng chỉ `tom_de` chưa có UI hiện (chờ thầy chốt, mục F kế hoạch); học sinh ảo Đ2 đã chạy 3/11 (điểm 6,5–8,5; báo cáo ở side-session-notes `hs-ao-dot2.md`) — chưa sửa: 11·D5 khung không giống khung (thêm phối cảnh/AB = 6 cm, bước 6 xoay cả F, cung 30° giữa n′ và B); 26·D5 màu Wt/Wđ lệch hình đề; nhãn 2·D4 'nóng chảy' đè A, 11·D4 F/T₁/T₂ chật; bước có 2 câu chọn liên tiếp cần dòng 'Còn câu nữa ↓' (khung chung) và xáo phương án (nội dung, thầy quyết).
**How to apply:** phiên mới làm theo đợt trong KE-HOACH-MODEL.md, đợt kế tiếp là Đ1 (Opus: bài 23, 27, 31); 4 điểm chờ thầy chốt ở mục F. Liên quan [[project_thachlab_btm_quet_dang]].

**3/11/2026 tối: ĐÃ DEPLOY + ĐĂNG DB** bài 33, 23, 27, 31 (Đ1), 58, 60, 62, 63, 66 (L10 Ch.3); sao lưu `scripts/logs/bai-tap-mau-bai<id>-17937*.json`. Đ2 (2, 11, 26) CHƯA đăng — chờ phiên "Sửa hình Đ2" xong. Đăng JSON xong phải deploy lại (build-content đọc DB lúc build); publish cần `--yes` khi chạy vòng lặp.
