---
name: project_thachlab_giai_cung_hinh
description: Giải cùng hình + tóm đề cho dạng bài tập mẫu — mẫu bài 33 D3 xong ở xem thử, kế hoạch 9 đợt Opus/Sonnet
metadata:
  type: project
---
Nâng dạng bài tập mẫu thành "giải cùng hình" (hình SVG dính nửa trên điện thoại, mỗi bước tự trả lời) + "tóm đề" (dòng Tìm đầu khối dính; ≥1280 thẻ Cho/Tìm ở lề ghi chú). Skill: `.claude/skills/cap-nhat-dang-bai-tap/` (SKILL.md + KE-HOACH-MODEL.md: 492 dạng, 16 họ hình, 9 đợt Đ1–Đ9).

Hiện trạng 3/11/2026: mẫu bài 33 (lesson_id 33) Dạng 3 `giao_thoa_2_nguon` chạy ở `/dev/btm`; code đã vào main qua nhánh `claude/wave-exercises-interactive-graphics-a3ea00`. Đã deploy + đăng DB 2026-11-03 (thứ tự: deploy code → publish JSON → deploy lại).


L10 Ch.3 Động lực học (3/11/2026, nhánh `claude/l10-ch3-giai-cung-hinh-be4044`): họ `so_do_vecto` + `thanh_moment` = một component `SoDoVecto.tsx` (cảnh mat_nghieng/mat_ngang/nut/rong_roc/ban_rong_roc/thanh); 10 dạng có hình (58 D5–D6, 60 D2/D4, 62 D4–D5, 63 D4–D5, 66 D4–D5) + tóm đề 18 dạng còn lại. Đã deploy + đăng DB 2026-11-03. Hở `tom_de` ở dạng không hình đã vá 3/11 (`TomDeKhung` trong `TomDe.tsx`).

**Why:** thầy muốn HS không phải cuộn qua lại giữa hình và lời giải (N8).
Đ1 (23, 27, 31) và Đ2 (2, 11, 26 — họ `do_thi`, `tu_truong`, `thanh_nang_luong`) đã deploy + đăng DB 2026-11-03 (Đ2 sau khi phiên "Sửa hình Đ2" sửa xong lỗi HS ảo, commit c4616ef98). **Còn chờ thầy quyết:** bước có 2 câu chọn liên tiếp cần dòng 'Còn câu nữa ↓' (khung chung) và xáo phương án (nội dung, thầy quyết).
**How to apply:** phiên mới làm theo đợt trong KE-HOACH-MODEL.md, Đ3 (37, 43) đã soạn + xem thử 375px 3/11 (nhánh `claude/wave-exercises-interactive-graphics-a3ea00`), **chưa HS ảo, chưa deploy/đăng DB**; đợt kế tiếp Đ4 (50, 57, 79; 66 đã xong), Đ5, rồi các đợt Sonnet; mỗi đợt: phiên nhánh soạn → HS ảo 375px → sửa → deploy → publish `--yes` → deploy lại → kiểm live `/lop-hoc/bai/?id=<n>#muc=bai-tap-mau`, bấm "Giải từng bước". Điểm chờ thầy chốt ở mục F. Liên quan [[project_thachlab_btm_quet_dang]].

**3/11/2026 tối: ĐÃ DEPLOY + ĐĂNG DB** bài 33, 23, 27, 31 (Đ1), 58, 60, 62, 63, 66 (L10 Ch.3); sao lưu `scripts/logs/bai-tap-mau-bai<id>-17937*.json`. Đ2 (2, 11, 26) CHƯA đăng — chờ phiên "Sửa hình Đ2" xong. Đăng JSON xong phải deploy lại (build-content đọc DB lúc build); publish cần `--yes` khi chạy vòng lặp.
- 3/11/2026 khuya: ĐÃ ĐĂNG DB + DEPLOY Đ2 (bài 2, 11, 26) sau phiên 'Sửa hình Đ2'; sao lưu scripts/logs/bai-tap-mau-bai{2,11,26}-179371*.json. Bài 11 thêm mục 6 'Bài tập tự luận' (tu_luan, cố ý). Còn: Đ3 (37, 43), Đ4 (50, 57, 79), Đ5.
- 3/11/2026: Đ3 xong phần soạn — họ mới `dien_truong_deu` (DienTruongDeu.tsx), `mach_dien` (MachDien.tsx); 37 D3, D5 + 43 D3, D4 có hình, các dạng còn lại tóm đề. Còn: HS ảo → thầy duyệt → deploy → publish 37, 43 `--giu-cu --yes` → deploy lại.
- 4/11/2026: ĐÃ ĐĂNG DB Đ3 (37, 43) + Đ4 (50, 57, 79) bằng `--giu-cu --yes` (sao lưu scripts/logs/bai-tap-mau-bai{37,43,50,57,79}-179377*.json trong worktree khanh-class); Đ5 (83, 156) đăng + deploy trước đó. Đã deploy 4/11, kiểm live: 10 dạng có hình đều hiện hình. Đợt kế tiếp: Đ6, Đ7, Đ8 (Sonnet) chạy song song từ 4/11; 125–127 đã xác nhận thuộc L12 Ch.3.
