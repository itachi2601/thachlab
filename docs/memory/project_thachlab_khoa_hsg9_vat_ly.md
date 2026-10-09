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
