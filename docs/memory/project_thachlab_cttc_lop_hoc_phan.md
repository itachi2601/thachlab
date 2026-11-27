---
name: project-thachlab-cttc-lop-hoc-phan
description: "Lớp học phần CTTC cho từng khoá (CĐ CK 25B GCPT, 25C CNCTM1): mã môn trong services/subjects.ts + trigger tự ghi danh từ user_classes"
metadata:
  type: project
---

Lớp học phần (course_offerings) CTTC phải có mã môn trong `services/subjects.ts` thì mới hiện trong bộ chọn
của dashboard GV và có nút "Học tiếp"; thiếu mã → lớp tạo tay rơi vào môn `khac` (đúng lỗi 27/11/2026).

- **GCPT — CĐ CK 25B**: lớp nội dung `classes.slug='gcpt'` id 24 (13 bài id 216–228, đều published), lớp học
  phần id 13 "Các PPGCPTT", mã `LOP-77B98E`, 10 SV (27/11). Trước đó lớp bị tạo với môn `khac`; migration
  `20261127170000` chuyển sang môn `gcpt` + ghi danh.
- **CNCTM 1 — CĐ CK 25C**: lớp nội dung `classes.slug='cnctm'` id 23 (13 bài 201–215), lớp học phần id 12
  "CĐ CK 25C - Công nghệ chế tạo máy 1", mã `CNCTM-25C`; thêm mã môn `cnctm` (joinPrefix `CNCTM`,
  `/lop-hoc/cnctm`) ngày 27/11.
- **Trigger `trg_sync_class_to_course`** (migration `20261127180000`): SV có `user_classes` active được ghi
  danh luôn vào lớp học phần khi slug lớp trùng mã môn VÀ môn chỉ có ĐÚNG MỘT lớp học phần đang hoạt động;
  0 hoặc ≥2 lớp (vd AVCN 24A/CGKL 25A) thì bỏ qua. Nhờ vậy SV tự vào lớp sau này vẫn có dòng bảng điểm.
- SV vào lớp CTTC trước khi có ghi danh bị `trg_set_track_thpt` đặt `profiles.track='thpt'`; ghi danh xong
  `trg_set_track_cttc` đổi lại `cttc`.
- Còn treo: 25B/25C chưa nhập danh sách chính thức (mã SV/ngày sinh) từ Excel; CNCTM 2 chưa có lớp học
  phần và chưa có mã môn trong `services/subjects.ts`.
