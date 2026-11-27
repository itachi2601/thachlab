---
name: project-thachlab-gcpt
description: "Học phần Các phương pháp gia công phi truyền thống (gcpt): lớp nội dung 24 + lớp học phần CĐ CK 25B (id 13, LOP-77B98E) có 10 SV"
metadata:
  type: project
---

Học phần CTTC "Các phương pháp gia công phi truyền thống" (thầy dạy ở CĐ Cao Thắng):
- Nội dung: lớp `classes` slug `gcpt` id 24 (vào có duyệt), môn `subject_code='gcpt'`, 13 bài id 216–228
  (12 bài theo công nghệ + bài 228 "Hướng dẫn thuyết trình nhóm"), tất cả `published=true`; đề 1423.
- Lớp học phần cho khoá CĐ CK 25B: `course_offerings` id 13, tên "Các PPGCPTT", `class_label='CĐ CK 25B'`,
  `join_code='LOP-77B98E'`, môn `gcpt`, 10 SV `course_enrollments` active (27/11/2026).
  Trước đó lớp này bị tạo với môn `khac` vì `services/subjects.ts` chưa có mã `gcpt` → đã thêm (joinPrefix GCPT,
  `learningHrefOf('gcpt')` → `/lop-hoc/gcpt`) + thêm vào danh sách môn hiện cho giảng viên ở
  `TeacherCourseDashboard` (migration `20261127170000_gcpt_lop_hoc_phan_cdck_25b.sql`).
- Còn treo: tổng kết thuyết trình nhóm theo bài; chưa nhập danh sách chính thức (mã SV/ngày sinh) cho 25B;
  CNCTM 1 (offering 12, CĐ CK 25C) và CNCTM 2 chưa có mã môn trong `services/subjects.ts` nên cũng chưa hiện
  trong bộ chọn lớp của dashboard GV.
