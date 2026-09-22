# Khoá học THPT: đăng lịch, phụ huynh / học sinh tự ghi danh

Trả lời: **lớp nào đang mở, học ngày nào, còn chỗ không, đăng ký thế nào** — không cần
nhắn qua lại rồi giáo viên gõ tay vào roster.

## Luồng

1. Giáo viên `/dashboard-thpt` → chọn khối → tab **Ghi danh** → **Mở lớp mới**: tên, năm
   học, khai giảng, sĩ số tối đa, ghi chú học phí, lịch tuần (nhiều buổi), công khai hay ẩn.
   Nút chép link đưa thẳng tới trang đăng ký của lớp.
2. `/khoa-hoc` (không cần đăng nhập, có trên menu "Đăng ký học"): lớp đang mở gom theo
   khối, lịch tuần, số chỗ còn, học phí. Lớp đã khai giảng hiện dòng "sẽ được xếp bù bài".
3. Bấm **Đăng ký** → `/khoa-hoc/dang-ky?id=…` → đăng nhập:
   - **Phụ huynh** (đã nối con qua `docs/PHU-HUYNH.md`): chọn con, hoặc "Con chưa có tài
     khoản" rồi khai tên + liên hệ.
   - **Học sinh**: đăng ký cho chính mình.
   - Giáo viên/trợ giảng: được chuyển sang dashboard.
4. Đăng ký có tài khoản → tự thêm `user_classes` **pending** cho khối, nên `/tai-khoan` của
   em hiện "Đang chờ giáo viên duyệt" và hàng chờ vào lớp sẵn có vẫn thấy em.
5. Giáo viên duyệt trong tab Ghi danh (hoặc duyệt ở hàng chờ cũ — trigger đồng bộ hai chiều)
   → `user_classes` active → em đọc được bài, có trong bảng điểm. Đăng ký "chưa có tài khoản"
   phải **Gắn tài khoản** (chọn trong học sinh chưa xếp lớp / học sinh của khối) rồi mới duyệt.
6. Học phí: cột phí trên dòng đã vào lớp — `Chưa đóng` / `Đã đóng tại trung tâm` /
   `Đã chuyển khoản`. Hiện tại tích tay sau khi trung tâm báo; tách khỏi trung tâm thì bật
   hướng dẫn chuyển khoản ở trang đăng ký và dùng nhánh `paid_transfer`, không đổi schema.
7. Phụ huynh xem trạng thái đăng ký ở `/phu-huynh` (mục "Đăng ký học").

## Chạy lần đầu

**SQL Editor** → `docs/supabase-migration-khoa-hoc-thpt.sql` (sau `supabase-migration-phu-huynh.sql`).

## Vì sao không dùng `course_offerings`

Bảng đó là của hệ CTTC: trigger `set_profile_track_cttc` đổi `profiles.track` sang `cttc`
ngay khi có `course_enrollments`, và `/tai-khoan` coi mọi enrollment là khoá CTTC. Khoá THPT
có bộ bảng riêng; "vào lớp" vẫn là `user_classes` như trước nên toàn bộ bài học, đề, bảng
điểm, phụ đạo không phải sửa gì.

## Bảng & hàm

| Tên | Vai trò |
|---|---|
| `thpt_courses` | Lớp: khối (`class_id` → `classes`), tên, năm học, khai giảng/kết thúc, `capacity`, `fee_note`, `is_public`, `status` |
| `thpt_course_schedules` | Lịch tuần: `weekday` 1 = Thứ 2 … 7 = CN, giờ, địa điểm |
| `thpt_registrations` | Đăng ký: `student_id` (null = chưa có tài khoản), `registered_by`, `status` pending/catchup/active/rejected/left, `joined_late`, `payment_status`, `payment_note` |
| `thpt_course_seats(bigint[])` | Số chỗ đã lấy cho trang công khai (anon), không lộ dòng đăng ký |
| `thpt_register(...)` | Ghi danh: kiểm quyền (mình / con đã nối), sức chứa, ghi `joined_late`, thêm `user_classes` pending |
| `thpt_review_registration(id, status)` | Duyệt / từ chối / cho nghỉ, ghi `user_classes` tương ứng |
| `thpt_attach_student(id, uuid)` | Gắn tài khoản cho đăng ký "chưa có tài khoản" |
| `thpt_has_registration(bigint)` | Cho người đã đăng ký đọc khoá đã đóng (tránh đệ quy RLS) |
| `trg_sync_thpt_registration` | Duyệt ở hàng chờ `user_classes` cũ → đăng ký cũng đổi trạng thái |

Quyền: khoá `is_public + active` ai cũng đọc; giáo viên phụ trách khối (`manages_class`)
làm mọi thứ với khoá và đăng ký của khối; người đăng ký chỉ đọc dòng của mình / của con.

## Code

- `services/thpt-courses.ts` — đọc/tạo/sửa khoá, lịch, ghi danh, duyệt, phí.
- `app/khoa-hoc/page.tsx` — danh sách công khai; `app/khoa-hoc/dang-ky/page.tsx` — form đăng ký.
- `components/dashboard/TeacherThptEnrollment.tsx` — tab Ghi danh.
- `app/phu-huynh/page.tsx` — mục "Đăng ký học" + nút đăng ký cho con.

## Vào lớp trễ — bù bài trước khi vào lớp chính thức

Migration: `docs/supabase-migration-bu-bai.sql` (chạy sau file khoá học).

1. Giáo viên đặt mốc **Lớp đang dạy tới bài** cho từng lớp (tab Ghi danh, chọn trong chủ đề
   tầng bài của khối). Cập nhật mỗi khi qua bài mới. Chưa đặt mốc thì không tính được phần bù.
2. Đăng ký sau khai giảng: form hiện phần lớp đã học (bài gần nhất trước) để em / phụ huynh
   tick **bài đã học ở nơi khác**. Bài chưa tick thành danh sách cần bù. Chưa học ở đâu thì
   không tick gì, bù toàn bộ.
3. Thứ tự bù: **bài lớp vừa học trước**, rồi lùi dần về các bài trước — buổi đầu bù đúng phần
   lớp đang học để em theo kịp ngay.
4. Giáo viên duyệt ("Duyệt · bù bài trước") → em vào khối (`user_classes` active, đọc được bài,
   đăng ký được ca phụ đạo) nhưng trạng thái ghi danh là **Đang bù bài**.
5. Trang tài khoản của em và trang phụ huynh hiện thẻ **Bù bài**: danh sách bài theo thứ tự,
   bài đã bù gạch đi, và các ca trong lịch tuần của trợ giảng khối (`tutoring_slots`). Ca dạy
   đúng bài kế tiếp được gợi ý lên đầu; ca không đúng bài xếp ở mục "Ca khác". Phụ huynh đăng
   ký ca cho con được (policy `parent registers child`).
6. Trợ giảng ghi buổi phụ đạo như bình thường (`/tro-giang/ghi`, tick bài đã dạy). Trigger
   `trg_catchup_progress` gạch bài đó khỏi danh sách; hết danh sách → **Đã vào lớp**. Giáo
   viên cũng bấm "Xong bù bài · vào lớp" được.

| Tên | Vai trò |
|---|---|
| `thpt_courses.current_topic_id` | Mốc lớp đang dạy tới (chủ đề tầng bài) |
| `thpt_registrations.known_topic_ids` | Bài em đã học nơi khác |
| `thpt_registrations.catchup_topic_ids` | Bài cần bù, phần tử đầu là bài kế tiếp |
| `thpt_registrations.catchup_done_topic_ids` | Bài đã bù |
| `thpt_taught_topics(course)` | Phần lớp đã học, gần nhất trước (anon đọc được) |
| `thpt_set_catchup(reg, known[])` | Chốt danh sách bù; đang catchup mà trống → active |
| `trg_catchup_progress` | Buổi phụ đạo ghi xong → gạch bài, hết → active |

`components/results/CatchupCard.tsx` dùng chung cho `ThptStudentHome` và `/phu-huynh`.
