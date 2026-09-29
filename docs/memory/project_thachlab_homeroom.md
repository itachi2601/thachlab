---
name: project_thachlab_homeroom
description: "Trang \"Lớp chủ nhiệm\" CTTC — điểm danh + bảng điểm + hạnh kiểm môn GDĐĐ&PTNN"
metadata: 
  node_type: memory
  type: project
  originSessionId: 31afff40-46fa-4ec9-8c4d-94e62bbf28fc
  modified: 2026-09-21T15:44:20.741Z
---

Giáo viên chủ nhiệm CTTC cần trang quản lý lớp chủ nhiệm, chủ yếu điểm danh cho môn
"Giáo dục đạo đức và phát triển nghề nghiệp" (1 môn, không phải 2). Yêu cầu chốt: bảng
điểm thang 10, mỗi học kì 1 bài kiểm tra; có hạnh kiểm (GVCN chọn tay Tốt/Khá/TB/Yếu);
KHÔNG làm điểm rèn luyện thang 100.

Đã code xong (commit 547dfd0). **Cập nhật 2026-09-21 tối:** thầy xác nhận đã chạy
`docs/supabase-migration-cttc-homeroom.sql` + test + deploy. Coi như xong.

Mô hình: 1 lớp chủ nhiệm = 1 course_offering dưới môn code `gddd-ptnn`. GVCN gán qua
course_instructors (dùng lại can_manage_course). Điểm danh dùng lại attendance_sessions/
attendance_records (bonus_points = điểm nề nếp). Bảng mới `homeroom_term_records`
(course_id, student_id, term hk1/hk2/ca_nam, exam_score 0-10, conduct, note).

Files: services/homeroom-records.ts, components/dashboard/HomeroomAttendancePanel.tsx +
HomeroomGradebook.tsx; TeacherCourseDashboard nhánh theo `subjectCode === HOMEROOM_SUBJECT_CODE`
(tab Điểm danh/Bảng điểm/Danh sách lớp). Học sinh tự điểm danh: dùng lại StudentAttendancePanel
qua /tai-khoan (môn hasCurriculum=false).

Sau khi chạy migration: admin tạo lớp học phần môn này ở tab Danh sách lớp → gán GVCN ở
/quan-tri/phan-cong-giang-vien → import Excel danh sách. Liên quan [[feedback_thachlab_deploy_scope]].
