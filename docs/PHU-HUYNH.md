# Phụ huynh xem kết quả học tập của con

Trả lời một câu: **phụ huynh muốn biết con học thế nào trên thachlab thì làm sao** — không
cần mượn tài khoản của con, không cần giáo viên chụp màn hình gửi Zalo.

## Luồng

1. Giáo viên vào `/dashboard-thpt` → tab **Hồ sơ** → chọn em → thẻ **Phụ huynh** → bấm
   **Tạo mã & chép link**. Link dạng `https://thachlab.id.vn/loi-moi?ma=PH1A2B3C` đã nằm
   trong clipboard, dán vào Zalo gửi phụ huynh. Bố và mẹ cùng xem thì tạo hai mã.
2. Phụ huynh mở link:
   - chưa có tài khoản → điền họ tên, email, mật khẩu ngay tại đó; tạo xong là đã nối;
   - đã có tài khoản → đăng nhập rồi bấm **Nối với con**.
3. Phụ huynh vào **menu tài khoản → Kết quả của con** (`/phu-huynh`): điểm theo thời gian,
   hạng trong lớp theo bài định kỳ, bài đã làm (mở được chi tiết từng câu), phần đang được
   phụ đạo và trạng thái, chủ đề còn sai nhiều. Nối nhiều con thì có ô chọn.
4. Muốn cắt quyền: thẻ Phụ huynh → nút thùng rác trên dòng đã nối. Phụ huynh mất quyền
   xem ngay, tài khoản của họ vẫn còn.

## Chạy lần đầu

**SQL Editor** → chạy `docs/supabase-migration-phu-huynh.sql` (idempotent). Không cần
Edge Function, không cần gửi email.

## Nguyên tắc quyền

- Phụ huynh **chỉ đọc**. Mọi policy trong migration đều là `select`; không policy
  `insert`/`update` nào dùng `is_parent_of()`. Không sửa `teaches_student()` vì hàm đó
  đang gác quyền chấm bài, sửa cảnh báo, thêm mục phụ đạo.
- Phụ huynh thấy đúng những gì con thấy ở `/lop-hoc/ket-qua`, trừ nút "Ôn lại bài" (họ
  không ở trong lớp nên không mở được bài học). Cảnh báo `student_alerts` chỉ hiện khi
  thầy đã xử lý (`status <> 'open'`), giống con.
- Không thấy: điểm của bạn khác, tin nhắn thầy–trò, nội dung đề chưa làm.
- Mã phụ huynh luôn là `PH` + 6 ký tự hex; mã mời nhân sự là 8 hex thuần — `/loi-moi`
  rẽ nhánh theo tiền tố, hai hàm `apply_*` không nhận nhầm mã của nhau.
- Tài khoản mới tinh nhận mã → `profiles.role = 'parent'`. Giảng viên / trợ giảng / học
  sinh đang học nhận mã thì giữ vai trò cũ, vẫn xem được con qua `is_parent_of()`.

## Bảng & hàm

| Tên | Vai trò |
|---|---|
| `parent_links` | Một dòng vừa là mã (chưa nhận) vừa là liên kết (đã nhận): `code`, `student_id`, `parent_id`, `claimed_at` |
| `is_parent_of(uuid)` | Dùng trong mọi policy đọc của phụ huynh |
| `apply_parent_link(uuid, text)` | Áp mã — chỉ `service_role`, gọi từ trigger và `claim_parent_link` |
| `claim_parent_link(text)` | Người đang đăng nhập tự nhận mã |
| `zz_claim_parent_link` | Trigger trên `auth.users`: đăng ký kèm `invite_code` = PH… thì nối luôn |
| `get_periodic_rank_of(uuid, bigint)` | Hạng của một em cụ thể, tự kiểm quyền; `get_periodic_rank(bigint)` cũ gọi qua nó |
| `student_outcome_gaps` | Thêm nhánh `is_parent_of` vào bộ lọc đầu vào |

## Code

- `services/parent-links.ts` — tạo/đọc/gỡ mã, nhận mã, danh sách con.
- `components/results/StudentResultsDashboard.tsx` — bảng kết quả dùng chung cho
  `/lop-hoc/ket-qua` (viewer `student`) và `/phu-huynh` (viewer `parent`).
- `components/dashboard/ParentLinkCard.tsx` — thẻ Phụ huynh trong hồ sơ học sinh.
- `app/phu-huynh/page.tsx`, `app/loi-moi/page.tsx` (nhánh mã PH).

## Bước sau (đã thống nhất, chưa làm)

1. Trang khoá học công khai + lịch học tuần + ghi danh (`course_offerings`, bảng
   `course_schedules`, `payment_status` unpaid / paid_center / paid_transfer).
2. Vào lớp trễ: chọn chương đã học nơi khác, phần còn lại thành `catchup_topic_ids`, đăng
   ký ca trong lịch tuần của trợ giảng khối (`tutoring_slots`), chương gần nhất trước rồi
   lùi dần; đủ buổi thì enrollment sang `active`.
