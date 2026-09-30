---
name: project_thachlab_preview_cttc_student
description: "Nút admin \"Xem như SV CTTC (CNC · Tiện phay · SHCN)\" — ghi danh thật tài khoản admin vào 3 môn rồi giả lập role/track; đã deploy 25/9/2026"
metadata:
  node_type: memory
  type: project
  originSessionId: ecda7e72-74b4-4d45-9c2b-9bb3ed91e09d
  modified: 2026-09-25T04:04:33.423Z
---

Nút nổi góc trái dưới (components/auth/PreviewAsStudentToggle.tsx) từ 25/9/2026 có 2 lựa chọn:
"Xem như học sinh" (cũ) và "Xem như SV CTTC (CNC · Tiện phay · SHCN)" (mới, commit fb8ff139, đã deploy).

Cơ chế: RPC `preview_cttc_enroll` (chỉ admin, docs/supabase-migration-preview-cttc-student.sql,
đã chạy trên DB) ghi danh CHÍNH user_id admin vào khóa active mới nhất của cnc / tien-phay /
gddd-ptnn, status active; trả lại track thật của admin sau khi trigger đổi. Trình duyệt ghi đè
role=student + track=cttc (AuthProvider.previewMode = "student" | "cttc" | null, sessionStorage
"thachlab_preview_as_student" = "1" | "cttc"). Bấm Thoát → RPC `preview_cttc_unenroll` xoá 3 dòng
ghi danh. Điểm danh/bài làm trong lúc thử ghi dưới user_id admin và KHÔNG bị xoá khi thoát.

**Phát hiện khi test:** /tai-khoan của sinh viên CTTC chỉ hiện MỘT ghi danh mới nhất
(fetchMyEnrollment) — không có chỗ chuyển giữa 3 môn. Hàm cố tình xếp enrolled_at để SHCN là
mới nhất (→ /tai-khoan ra lớp chủ nhiệm); CNC và Tiện phay vào qua /lop-hoc/cnc, /lop-hoc/tien-phay.
Thầy chưa nói có muốn sửa /tai-khoan cho SV nhiều môn hay không.

Liên quan: [[project_thachlab_homeroom]], [[feedback_thachlab_deploy_scope]].
