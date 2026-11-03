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
**How to apply:** phiên mới làm theo đợt trong KE-HOACH-MODEL.md, đợt kế tiếp là Đ1 (Opus: bài 23, 27, 31); 4 điểm chờ thầy chốt ở mục F. Liên quan [[project_thachlab_btm_quet_dang]].
