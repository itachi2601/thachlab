---
name: project_thachlab_khoa_hsg9_vat_ly
description: Khoá "Vật lí HSG & chuyên" trong KHTN 9 (tab môn hsg-vat-ly) — khung 17 bài đã seed 10/10/2026, CĐ01+CĐ02 đã ghi DB; còn 12 chuyên đề + 3 mới + đề luyện/đề thật
metadata:
  type: project
---

Thầy chốt 10/10/2026: mở khoá luyện HSG KHTN 9 phần Vật lí + luyện chuyên Lê Hồng Phong/TĐN/HSG thành phố. Đặt như **môn thứ 4 trong lớp KHTN 9** (`academic_subjects.code='hsg-vat-ly'`, class_id 15), không tạo lớp mới (classGrade gom theo chữ số 9). Bản đồ + id: `docs/HSG9-KHUNG.md`. Nguồn: 14 docx ở `~/Documents/THPT/Lop09/00_Dung_chung/HSG_KHTN9_Vat_li/01_Chuyen_de/` (đã trích `.txt` vào `content/hsg9/<cd>/nguon.txt` cho CĐ01, 02).

**Đã xong:** migration `20261010100000` chạy 10/10 (17 bài, ẩn; CĐ01=161, CĐ02=166); lý thuyết nâng cao + bài tập mẫu 7 dạng của CĐ01, CĐ02 ghi DB (đã kiểm chéo); tab môn thêm vào `services/academic-subjects.ts` (cần deploy).
**Còn:** bật published hai bài sau khi thầy duyệt; deploy; 12 chuyên đề còn lại (docx có sẵn); 3 chuyên đề mới chưa có docx (CĐ10 Lực, CĐ15 Âm thanh, CĐ16 Truyền nhiệt & nở vì nhiệt); đề luyện + đề thật thầy cung cấp sau; sửa docx gốc (xem sai sót trong HSG9-KHUNG/báo cáo: 960→1200 J, G1 cách mắc ròng rọc, G4 thiếu tanβ>μ).
**Why:** đề cương "THI HSG 9 KHTN 26-27" cần đủ Lực, Âm, Truyền nhiệt mà docx chưa có.
**How to apply:** mỗi chuyên đề = 1 phiên: 4 subagent song song (lý thuyết, bài tập mẫu) → 2×kiem-code → sửa → ghi bằng cap-nhat-ly-thuyet.sh + publish-bai-tap-mau.mts. Topic "bài tương tự" dùng YCCĐ lớp 10 vì KHTN 9 chưa có YCCĐ.

**Cập nhật 10/10 (đợt 1):** CĐ13(162), CĐ10 Lực(155, mới), CĐ11(154), CĐ00(160) đã soạn + kiểm chéo + sửa, commit 08bcf5f12 (lý thuyết ở `content/hsg9/cd{13,10,11,00}-*/`, bài tập mẫu `scripts/data/bai-tap-mau/{162,155,154,160}.json`, `review.checked=true`). **Treo:** thầy chạy `bash scripts/run-migrations.sh` (tạo mục + bật Hiện 160) rồi `bash scripts/dang-hsg9-dot1.sh`, rồi deploy. Còn: CĐ03,04,05 (điện), 08, 06,07,14 (quang), 16 (mới), 12, 15 (mới), 09; sửa docx gốc G1 ròng rọc chưa xác định được bài. Quy ước chốt: sai số 1 chữ số có nghĩa; góc dây đo so với thẳng đứng ở lý thuyết, ghi rõ khi bài tập dùng góc với phương ngang.

- 2026-10-11: `~/Documents/THPT` (gồm HSG_KHTN9_Vat_li) đã bị xoá không sao lưu — nguồn gốc không còn; xem [[project_thachlab_may_mac_dung_luong]].
- 2026-10-10: bộ **Bài tập tự luận Cơ học VD–VDC** (12 bài, 11 hình, gợi ý 3 tầng + lời giải) ở `01_Chuyen_de/Bai_tap_tu_luan_Co_hoc_VD-VDC/` (nguồn `sinh-bai-tap.py`), kiểm chéo 12/12; skill mới `.claude/skills/soan-bai-tap-tu-luan-hsg/`. Chưa số hoá lên web.
- 2026-10-10: bộ Cơ học VD–VDC đã lên web: PDF đề `public/hsg9/bai-tap-co-hoc-vd-vdc-2026-10.pdf` (deployed) + post 5 (tai_lieu, lớp 19 `hsg-vat-ly-9`) kèm lịch 2 bài/ngày CN 11/10→T6 16/10, T7 17/10 sửa. Lời giải CHƯA đăng (giữ tới T7). Đăng thông báo lớp: `scripts/dang-thong-bao-hsg9.mts` (RPC create_post_with_targets đòi is_admin nên script ghi thẳng posts+post_classes).
- 2026-10-11: sửa cách giao bài — bộ Cơ học VD–VDC làm trên web: lesson 167 "Bài tập tuần này" (đầu chương Cơ học, published, 12 dạng buoc[] fading giau_het, nguồn `scripts/data/bai-tap-mau/167.json`, part-A..D + build-*.py ở `hsg-tuan/`); post 5 trỏ `/lop-hoc/bai/?id=167`, PDF chỉ còn là bản in. Validator nâng tối đa 12 dạng. Chưa có mô phỏng chuyển động cho bài 4–12; `parseNumber` ở StepwiseSolution chỉ đọc số đầu nên "5/3" thành 5 (nên thêm phân số). Lời giải đầy đủ mở được ngay qua nút "Xem cả lời giải", không khoá tới T7.
