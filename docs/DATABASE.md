# DATABASE — Lược đồ Supabase

Toàn bộ dữ liệu động của ThachLab nằm trên **Supabase Postgres**, truy cập từ
trình duyệt bằng anon key và được bảo vệ bằng **Row Level Security (RLS)**.

## Thứ tự chạy script

Chạy trong Supabase Dashboard → SQL Editor (các file **idempotent**, chạy lại được):

1. `supabase-schema.sql` — profiles, posts, exams, exam_results, messages.
2. `supabase-migration-classes.sql` — lớp học, quan hệ many-to-many, storage bucket.
3. `supabase-migration-lessons.sql` — chương → bài học → mục, tiến độ.
4. `supabase-seed-exams.sql` — dữ liệu đề mẫu (tuỳ chọn).

Sau khi thầy đăng ký tài khoản trên web, cấp quyền admin:

```sql
update public.profiles set role = 'admin'
where id = (select id from auth.users where email = 'itachi2601@gmail.com');
```

## Vai trò & phân quyền

- `profiles.role ∈ {student, admin}` (mặc định `student`).
- Hàm `is_admin()` (SECURITY DEFINER) tránh đệ quy RLS khi kiểm tra quyền.
- Trigger `on_auth_user_created` tự tạo `profiles` từ metadata lúc đăng ký
  (họ tên, lớp) và gán `user_classes` nếu có `class_id`.
- Học sinh **không tự thăng quyền** (policy update chặn `role != 'student'`).

## Các bảng

### profiles
Hồ sơ người dùng, khóa chính = `auth.users.id`. Trường: `full_name`,
`class_name`, `role`. RLS: đọc/sửa hồ sơ của chính mình; admin đọc tất cả.

### classes
Lớp học (`10A1`…`12A2`): `name`, `slug`, `color`, `icon` (emoji), `sort_order`,
`active`. Ai cũng đọc lớp đang `active`; admin quản lý.

### Quan hệ many-to-many
- `exam_classes` (exam ↔ class) — gán đề cho lớp.
- `post_classes` (post ↔ class) — gán bài đăng cho lớp.
- `user_classes` (user ↔ class) — học sinh thuộc nhiều lớp.
- `chapter_classes` (chapter ↔ class) — chương thuộc lớp (không gán = toàn trường).

### posts
Bài đăng / video / bài giảng: `title`, `body`, `video_url`, `published`, `topic`.
Ai cũng đọc bài đã `published`; admin quản lý.

### exams
Đề kiểm tra. `questions` (jsonb) là mảng câu hỏi, mỗi câu một trong **3 dạng**
theo cấu trúc đề 2025 (GDPT 2018):

```jsonc
{ "type":"multiple_choice", "question":html, "options":[html×4], "answer":0-3, "explanation":html }
{ "type":"true_false", "question":html, "statements":[{"text":html,"answer":bool}×4], "explanation":html }
{ "type":"short_answer", "question":html, "answer":"1,25", "explanation":html }
```

Cột generated: `question_count` (số câu), `type_counts` (đếm theo dạng TN/ĐS/TLN).
Trường lọc: `topic`, `difficulty ∈ {de, trung-binh, kho}`. Học sinh đọc đề đã
`published`; admin quản lý.

### exam_results
Kết quả bài làm: `student_id`, `exam_id`, `score` (numeric 4,2), `detail` (jsonb —
đáp án đã chọn, số câu đúng từng phần), `duration_seconds`. Học sinh chỉ ghi/đọc
kết quả của mình; admin đọc tất cả. Có index theo đề và theo học sinh.

### messages
Tin nhắn admin → học sinh: gửi cho 1 học sinh (`recipient_id`), cả lớp
(`class_name`), hoặc tất cả (đều null). Chỉ admin gửi; người nhận đọc tin của mình.

### chapters → lessons → lesson_items
Cấu trúc chương trình học:
- `chapters` — chương (`title`, `sort_order`).
- `lessons` — bài học trong chương (`published`).
- `lesson_items` — **6 mục cố định** mỗi bài, `kind ∈`:
  `ly_thuyet`, `video`, `bai_tap_mau`, `luyen_tap_sach`, `luyen_tap_de`, `kiem_tra`.
  Trường: `body_html` (HTML + `$LaTeX$`), `video_url`, `pdf_url`, `exam_id`.
- `lesson_progress` — tiến độ (user ↔ item đã hoàn thành).

Ai cũng đọc chương/mục và bài đã `published`; admin quản lý; học sinh quản lý
tiến độ của chính mình.

## Storage

Bucket **`exam-images`** (public) chứa ảnh công thức/hình vẽ khi import đề từ
Word. Chỉ admin upload; ai cũng đọc.
