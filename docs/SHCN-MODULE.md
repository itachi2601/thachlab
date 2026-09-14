# Module SHCN — sinh hoạt chủ nhiệm

Ba việc của lớp chủ nhiệm CTTC, tách bạch nhau:

| Việc | Ai làm | Ở đâu trong app |
| --- | --- | --- |
| Điểm danh **hàng ngày** (sĩ số + danh sách vắng) | Lớp trưởng / lớp phó | `/tai-khoan` → tab "Điểm danh lớp" |
| Nội dung sinh hoạt **tuần** (phổ biến + GDĐĐ&PTNN) | GVCN | `/dashboard` → tab "Sinh hoạt lớp" → "Nội dung sinh hoạt tuần" |
| Xem lại nội dung tuần | Sinh viên | `/tai-khoan` → tab "Sinh hoạt lớp" |

GVCN theo dõi điểm danh hàng ngày trước tiết SHCN ở `/dashboard` → tab "Sinh hoạt lớp" →
"Điểm danh hàng ngày" (bảng theo tuần, cảnh báo vắng nhiều, nút điền sẵn sĩ số cho biên bản).

Module này **không** thay quy trình nộp biên bản .docx lên portal.caothang.edu.vn — nó chỉ hiển
thị lại nội dung cho sinh viên và gom số liệu để soạn `tuan-XX.json` đỡ phải gõ tay.

## Khác gì so với bản spec

Spec mô tả ý định; phần dưới là cách đã triển khai cho khớp schema và kiến trúc đang chạy.

| Spec | Triển khai | Vì sao |
| --- | --- | --- |
| `users.lop_id` kiểu TEXT ("CD-CK-26C") | `course_id` → `course_offerings` | Repo không có bảng `users`; 1 lớp chủ nhiệm = 1 khóa dưới môn `gddd-ptnn` (xem `supabase-migration-cttc-homeroom.sql`). Năm học lấy từ `course_offerings.school_year` nên không lặp lại trong bảng tuần. |
| Thêm role `lop_truong` vào bảng người dùng | Bảng `homeroom_monitors` (`lop_truong` / `lop_pho`) | Lớp trưởng vẫn là sinh viên (`profiles.role = 'student'`, vẫn học và làm bài bình thường). Quyền nhập điểm danh cấp theo từng lớp, giống cách `course_instructors` cấp quyền cho giảng viên, và cho phép cả lớp phó. |
| Bảng `diem_danh_ngay`, `shcn_tuan` | `homeroom_daily_attendance`, `homeroom_weekly_sessions` | Bảng trong DB đặt tên tiếng Anh như phần còn lại của schema (`homeroom_term_records`, `attendance_sessions`…). Tên cột giữ ý nghĩa gốc. |
| `POST /api/diem-danh`, `GET /api/shcn-tuan`… | Hàm trong `services/homeroom-shcn.ts` + RLS | `next.config.ts` đặt `output: "export"` — site tĩnh trên LiteSpeed, không có Node.js server nên không có API route hay server action. Mọi ràng buộc quyền ("chỉ lớp mình", "chỉ ngày hôm nay") nằm ở RLS, không ở tầng ứng dụng. |

## Cài đặt

1. Chạy `docs/supabase-migration-shcn.sql` trong Supabase SQL editor (idempotent, chạy lại được).
2. Vào `/dashboard` → chọn môn **Giáo dục đạo đức & phát triển nghề nghiệp** → chọn lớp → tab
   **Sinh hoạt lớp** → mục "Lớp trưởng / lớp phó" → giao quyền điểm danh.
3. (Tuỳ chọn) Đổi link tài liệu GDĐĐ&PTNN bằng `NEXT_PUBLIC_GDDD_DOCS_URL` trong `.env.local`;
   mặc định là thư mục Drive chung trong `lib/shcn/gddd-topics.ts`.

## Nạp nội dung tuần từ tuan-XX.json

Hai cách, cùng bộ alias tên field:

- **Trên web:** tab "Sinh hoạt lớp" → "Nội dung sinh hoạt tuần" → nút **Dán tuan-XX.json** → dán
  nội dung file → "Điền vào form" → kiểm tra → lưu.
- **Chạy hàng loạt trên máy:**

  ```bash
  SUPABASE_SERVICE_ROLE_KEY=xxx NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co \
    node scripts/import-shcn-tuan.mjs --lop CD-CK-26C ~/Documents/CTTC/.../ND-SHCN/tuan-*.json
  ```

  Thêm `--dry-run` để xem trước, `--course-id <id>` nếu tên lớp trùng nhau. Service role key là
  secret: không commit, không để chung `.env.local` với các biến `NEXT_PUBLIC_*`.

Bộ alias đang nhận: `tuan_so|tuan|week|so_tuan`, `ngay_sinh_hoat|ngay|ngay_shcn|date`,
`noi_dung_pho_bien|noi_dung|pho_bien|muc`, `gdnn_chu_de|chu_de|gddd_chu_de`,
`gdnn_da_day|da_day|gddd_da_day|trong_tam`, `si_so|siso|tong_so`, `co_mat|comat|hien_dien`.
Nếu file thật trên máy thầy dùng tên khác, bổ sung vào `lib/shcn/tuan-json.ts` **và**
`scripts/import-shcn-tuan.mjs` (script chạy Node thuần nên giữ bản sao riêng).

## Còn thiếu / chờ chốt

- **Mục con của 4 chủ đề còn lại.** `lib/shcn/gddd-topics.ts` đã có đủ tên 12 chủ đề và mục con
  của 8 chủ đề (đọc từ các file PDF trong thư mục tài liệu chung). Còn thiếu: "Sinh hoạt đầu
  khóa" và chủ đề 1 (thư mục chưa có tài liệu riêng — file "1. Tai lieu long ghep Ky nang
  mem.pdf" là tài liệu tư vấn chung cho giáo viên), chủ đề 4 (chưa có file), chủ đề 7 (bản PDF
  đọc được dừng giữa chừng nên chưa chắc đủ mục). Bốn chủ đề đó để `complete: false` — giao
  diện **không** hiện dòng "Tự đọc thêm" thay vì liệt kê thiếu; có tài liệu đủ thì thêm vào
  `items` rồi đổi `complete: true`.
- **Cách ghi trọng tâm đã dạy.** Ghi trùng tên mục con trong `gddd-topics.ts` thì phần "Tự đọc
  thêm" mới trừ đúng (so khớp bỏ dấu, chấp nhận một bên chứa bên kia). Ghi gộp hai mục vào một
  dòng, vd "Những điều cần cảnh giác và số điện thoại khẩn cấp", thì chỉ mục khớp được trừ.
- **Số chủ đề in trong PDF lệch số thứ tự.** Vài file tài liệu còn ghi số của bản chương trình
  cũ (file "3. 5S va tac phong cong nghiep.pdf" ghi "CHỦ ĐỀ 8"). Số dùng trong code theo bảng
  12 chủ đề hiện hành, cũng là số đầu tên file.
- **Giờ chốt khóa điểm danh trong ngày.** Hiện chưa khóa theo giờ: lớp trưởng sửa được cả ngày
  hôm nay, sang ngày mới thì RLS chặn. Muốn chốt theo giờ thì siết trong policy
  `monitors update today attendance` (thêm điều kiện giờ vào `public.vn_today()`).
- **Ngưỡng cảnh báo vắng nhiều.** Đang cố định `ABSENCE_ALERT_THRESHOLD = 3` buổi/tuần trong
  `services/homeroom-shcn.ts`.

## File liên quan

```
docs/supabase-migration-shcn.sql          bảng + RLS + hàm vn_today()/is_homeroom_monitor()
services/homeroom-shcn.ts                 truy vấn + tổng hợp vắng + điền sẵn sĩ số
lib/shcn/gddd-topics.ts                   12 chủ đề, link Drive chung, tính "tự đọc thêm"
lib/shcn/tuan-json.ts                     đọc tuan-XX.json (bản dùng cho web)
scripts/import-shcn-tuan.mjs              nạp hàng loạt bằng service role key
components/dashboard/HomeroomShcnPanel.tsx      tab "Sinh hoạt lớp" của GVCN
components/dashboard/HomeroomDailyReport.tsx    bảng điểm danh tuần + cảnh báo + giao lớp trưởng
components/dashboard/HomeroomWeeklyEditor.tsx   soạn nội dung tuần + dán JSON + điền sẵn sĩ số
components/dashboard/HomeroomStudentHome.tsx    không gian lớp chủ nhiệm của sinh viên
components/dashboard/ShcnWeekList.tsx           thẻ tuần sinh viên xem
components/attendance/MonitorDailyAttendancePanel.tsx  form điểm danh của lớp trưởng
```
