---
name: project_thachlab_track_student_home
description: Tách hệ CTTC/THPT bằng profiles.track + trang tài khoản học sinh THPT thành dashboard — đã chạy migration, test và deploy 21/9/2026
metadata: 
  node_type: memory
  type: project
  originSessionId: d859e0b3-b815-4afe-b13a-a17460aa5c3b
  modified: 2026-09-21T15:44:14.035Z
---

**Cập nhật 2026-09-21 tối:** thầy xác nhận đã chạy `student-track.sql` + `student-rank.sql`
+ test + deploy. Hạng học sinh và nhãn CTTC/THPT giờ hoạt động thật, không còn "—".

2026-09-12, một đợt liền mạch sau khi user báo "học sinh CTTC bị add nhầm vào lớp 12, không xoá được, không biết được".

**Gốc vấn đề:** 2 hệ dùng chung `profiles`, hệ chỉ suy ra ngầm qua `user_classes` (THPT) vs
`course_enrollments` (CTTC) → cứ query "toàn bộ học sinh" là lẫn. Đã vá 3 chỗ trong 1 ngày
trước khi làm gốc: `fetchUnassignedStudents`, nhãn roster, `MessagesAdmin`.

**Chốt:** cột `profiles.track` ('thpt'|'cttc') là nguồn sự thật duy nhất, set bằng trigger khi
có dòng mới ở `user_classes`/`course_enrollments`, **CTTC ưu tiên khi xung đột** (ghi danh CTTC
cần nhập mã khóa → đáng tin hơn dòng user_classes có thể do gán nhầm).

**2 migration user CẦN chạy tay trong Supabase SQL Editor (tính tới lúc ghi memory này là CHƯA):**
- `docs/supabase-migration-student-track.sql` — cột track + trigger + backfill.
- `docs/supabase-migration-student-rank.sql` — RPC `get_exam_rank`/`get_periodic_rank` cho thứ hạng.
Chưa chạy thì UI vẫn chạy bình thường, chỉ là hạng hiện "—" và nhãn CTTC chưa chuẩn.

**Trải nghiệm học sinh:** user chê trang `/tai-khoan` của học sinh THPT "quá đơn điệu" (chỉ 1 hộp
xanh 2 dòng) trong khi CTTC có `StudentLearningDashboard` đầy đủ, và ghét phải chọn lại khối 12
ở `/lop-hoc` dù hệ thống đã biết lớp. Đã làm `ThptStudentHome` mirror đúng ngôn ngữ hình ảnh của
bản CTTC (thanh "Năng lượng học tập", ô Stat) + `/lop-hoc` mở thẳng lớp của mình.
→ **Quy tắc rút ra:** trang cho học sinh THPT nên ngang bằng CTTC về độ "đã tay", và đừng bắt
chọn lại thứ hệ thống đã biết.

**Giới hạn khi test:** mình KHÔNG được nhập mật khẩu để đăng nhập, nên không tự kiểm chứng được
các trang sau đăng nhập bằng tài khoản học sinh — chỉ test được đường khách/admin (trình duyệt
trên máy user thường sẵn session admin.test.thachlab@gmail.com). Với trang student-facing: nói
thẳng là chưa kiểm chứng, nhờ user đăng nhập trên localhost rồi mình soi, đừng tuyên bố "chạy tốt".

Liên quan: [[project_thachlab_exam_analytics]], [[feedback_thachlab_deploy_scope]], [[project_thachlab_lms]]
