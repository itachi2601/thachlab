---
name: project-thachlab-cttc-roster-import
description: "CTTC roster-import feature (Excel → tài khoản + bảng điểm), Edge Function đầu tiên của dự án"
metadata: 
  node_type: memory
  type: project
  originSessionId: f6eb9462-f20f-4c77-9bf3-e1574d16ad49
  modified: 2026-09-21T15:44:58.507Z
---

Tính năng "Nhập danh sách & Bảng điểm" (2026-08-26): giảng viên CTTC upload file Excel danh
sách lớp (mẫu phòng đào tạo cấp, `.xls` cũ hoặc `.xlsx`) → tự tạo tài khoản Supabase Auth
(mật khẩu = mã số sinh viên) + ghi danh, và cuối kỳ xuất lại đúng file mẫu kèm điểm.

**Chuyển vào dashboard giảng viên (2026-08-28)**: bỏ hẳn trang `/quan-tri/nhap-diem` +
`components/admin/RosterAdmin.tsx`. Giờ là:
- CTTC: tab "Nhập danh sách & điểm" trong `TeacherCourseDashboard` →
  `components/dashboard/CourseRosterPanel.tsx` (chứa cả `LtGradebook`), bám theo bộ chọn
  "Lớp đang dạy" sẵn có. Nút "+ Tạo lớp học phần" chỉ hiện với `role === "admin"`. Thêm môn
  `khac` (isPracticum:false) vào `services/subjects.ts` SUBJECTS để giảng viên chọn được lớp LT.
- THPT: tab "Nhập danh sách" trong `TeacherThptDashboard` →
  `components/dashboard/ClassRosterImportPanel.tsx` (chỉ nhập, không xuất — tab Bảng điểm
  THPT đã có Xuất CSV). Edge Function `import-roster` nhận thêm `body.classId` → ghi vào
  `user_classes`, kiểm quyền qua RPC mới `can_manage_class` (migration
  `docs/supabase-migration-roster-import-thpt.sql` — cần chạy + deploy lại function).
- RLS `course_offerings`/`can_manage_course` (migration course-instructors) tự giới hạn giảng
  viên chỉ thấy lớp được phân công — không cần lọc thêm ở client.
- `InstructorAssignmentManager` tab CTTC giờ dùng `CTTC_SUBJECTS = SUBJECTS` (cả `khac`) thay
  vì lọc `isPracticum`, để admin phân công giảng viên vào lớp học phần lý thuyết.
- Commit gộp toàn bộ WIP: `4998cd8` (2026-08-28), đã push origin/main. Migration
  `can_manage_class` + deploy lại Edge Function `import-roster` vẫn phải làm thủ công trên Supabase.

- **Edge Function đầu tiên của dự án**: `supabase/functions/import-roster/index.ts`. Bắt buộc
  vì site build tĩnh (`output: "export"`, không server Node) nên trình duyệt không thể cầm
  `service_role key` để gọi `auth.admin.createUser`. Cần deploy thủ công 1 lần — hướng dẫn ở
  `docs/deploy-edge-function.md` (cài Supabase CLI, `supabase login`, `supabase link`,
  `supabase functions deploy import-roster`; KHÔNG cần `supabase secrets set` vì
  SUPABASE_URL/ANON_KEY/SERVICE_ROLE_KEY được Supabase tự bơm vào mọi Edge Function). Nếu user
  báo tính năng import không tạo được tài khoản, việc đầu tiên cần hỏi là **đã deploy function
  chưa** — code đúng nhưng chưa deploy sẽ lỗi ở bước gọi `supabase.functions.invoke`.
- Dùng lại đúng cơ chế đăng nhập username-trần-thành-email đã có (`${maSV}@thachlab.local`,
  xem `app/dang-nhap/page.tsx`) — không tạo cơ chế mật khẩu riêng.
- 2 mẫu file đã xác nhận từ file thật của user: môn LT (lý thuyết, vd "Tiếng Anh chuyên ngành")
  có 10 cột điểm (Chuyên Cần, KT HS1×3, KT HS2×3, TB Kiểm Tra, Thi Lần 1, Tổng Kết 1) — **tất cả
  đều nhập tay**, không suy đoán công thức TB Kiểm Tra/Tổng Kết vì hỏi user 2 lần đều không xác
  nhận được công thức cụ thể. Môn TH (thực hành, CNC/Tiện-Phay) chỉ có 1 cột Tổng Kết, được lấy
  thẳng từ công thức chính thức đã có (45% Thi Tiện GV + 45% Thi Phay GV + 10% Chuyên cần + cộng
  trừ, `services/cnc-final-grade.ts` — tách ra từ `TeacherFinalGradebook.tsx` để dùng chung giữa
  UI và export, không lặp công thức 2 nơi).
- Subject bucket mặc định cho lớp LT mới (chưa có subject riêng): `subjects.code = 'khac'`
  (migration `docs/supabase-migration-roster-import.sql`).
- `profiles.birth_date` (date) mới thêm — lưu ngày sinh đọc từ Excel để xuất file cuối kỳ đủ cột
  như file gốc (trước đây không có chỗ lưu ngày sinh).
- Đọc Excel bằng `xlsx` (SheetJS) — cài từ `https://cdn.sheetjs.com/xlsx-latest/xlsx-latest.tgz`
  (package.json ghi tarball URL này), KHÔNG cài từ npm registry thường (`xlsx@0.18.5` trên npm
  có 2 lỗ hổng high-severity chưa vá — Prototype Pollution + ReDoS — SheetJS chỉ vá qua CDN riêng
  của họ do chính sách npm registry).
- Parser tự nhận diện tên cột theo text (không phân biệt dấu/hoa-thường) thay vì cố định số thứ
  tự cột — 2 file mẫu thật có offset hàng tiêu đề khác nhau (`services/roster-schema.ts`
  `classifyGradeHeader`).

**Xác nhận 2026-09-14: function VẪN CHƯA deploy** (curl trả 404). Cách kiểm tra nhanh: `curl -X POST
https://fxnqgmfqdbvnjawgnsfi.supabase.co/functions/v1/import-roster` — 404 = chưa deploy, 401 = đã deploy
(chỉ thiếu auth header, bình thường).

**Cập nhật 2026-09-21: đã deploy.** Curl lại trả `401` thay vì `404` → function tồn tại rồi.

Liên quan: [[project-thachlab-lms]]
