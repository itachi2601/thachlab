# Thông báo tự động

Chuông trên thanh điều hướng (mọi tài khoản đã đăng nhập) + trang `/thong-bao`. Không gửi
email/Zalo — chỉ trong web. Đếm chưa đọc mỗi phút và khi quay lại tab.

## Chạy lần đầu

**SQL Editor** → `docs/supabase-migration-thong-bao.sql` (sau `supabase-migration-bu-bai.sql`).

## Sự kiện → ai nhận

| Sự kiện | Người nhận | Bấm vào tới |
|---|---|---|
| Đăng ký khoá mới | Giáo viên phụ trách khối + admin (trừ người vừa đăng ký) | `/dashboard-thpt` |
| Duyệt vào lớp | Em + phụ huynh đã nối + người đăng ký hộ | `/tai-khoan` · `/phu-huynh` |
| Duyệt nhưng phải bù bài | Em + phụ huynh (số bài cần bù) | mục Bù bài |
| Từ chối | Em + phụ huynh | `/khoa-hoc` |
| Buổi phụ đạo gạch được một bài | Em + phụ huynh (còn mấy bài, bài kế tiếp) | mục Bù bài |
| Bù xong, chính thức vào lớp | Em + phụ huynh; giáo viên khối | |
| Trợ giảng mở ca có bài em đang cần bù | Em + phụ huynh của các em `catchup` trong khối | mục Bù bài |
| Phụ huynh nối tài khoản với con | Giáo viên khối; chính phụ huynh | `/dashboard-thpt` · `/phu-huynh` |
| Gắn tài khoản cho đăng ký "con chưa có tài khoản" | Phụ huynh đã đăng ký hộ | `/phu-huynh` |

## Nguyên tắc

- Mọi thông báo do **trigger trong DB** sinh ra (`security definer`). Client chỉ đọc, đánh dấu
  đã đọc, xoá dòng của mình. Không có policy insert cho `authenticated`.
- Ba hàm gửi: `notify_user`, `notify_class_staff(class_id, …, p_except)`,
  `notify_student_side(student, …, p_extra)` (em + phụ huynh đã nối + người đăng ký hộ).
- Thêm sự kiện mới = viết một trigger gọi ba hàm trên, không cần sửa client. Trường `kind`
  chỉ để lọc/phân tích sau này; `href` là đường dẫn nội bộ.

## Code

- `services/notifications.ts`, `components/layout/NotificationBell.tsx`, `app/thong-bao/page.tsx`.
