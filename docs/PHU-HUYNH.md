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

## Giao diện cho phụ huynh (45–60 tuổi)

Người đọc `/phu-huynh` là cha/mẹ 45–60 tuổi, không phải học sinh — bộ quy tắc riêng ở
`docs/QUY-TAC-THIET-KE-PHU-HUYNH.md` (chữ thân 18px, nhãn ≥15px, tương phản 7:1, đích chạm 48px, nền
sáng mặc định, không jargon, không biểu đồ, liên hệ thầy ở đầu **và** cuối trang); nghiên cứu nền 26
nguồn ở `docs/NGHIEN-CUU-PHU-HUYNH-45-60.md`.

- Khách chưa đăng nhập: `components/parent/ParentGuestLanding.tsx` — 3 bước lấy quyền xem, Zalo/gọi là
  hành động chính, ảnh thật + khối "Thầy đứng lớp", FAQ.
- Đã đăng nhập: `StudentResultsDashboard viewer="parent"` có thêm khối **"Tóm tắt cho anh chị"** (bài gần
  nhất, điểm trung bình, so với bài trước, phần còn sai nhất, đang phụ đạo) và prop `afterSummary` để
  trang chèn "Bài tập về nhà" + "Bù bài" ngay dưới tóm tắt.
- Cỡ chữ/tương phản/đích chạm nâng theo phạm vi trang bằng class `.parent-page` (`app/globals.css`) —
  không sửa trực tiếp trong component dùng chung với học sinh.

## Các bước sau đã làm

- Trang khoá học công khai + lịch tuần + ghi danh — `docs/KHOA-HOC.md`.
- Vào lớp trễ, bù bài trước khi vào lớp — mục cuối `docs/KHOA-HOC.md`.

## Đề xuất 15/10/2026 — phụ huynh tự nối với con (CHỜ THẦY DUYỆT, chưa code)

Hiện nay chỉ có đường **link mời `PH…` do thầy tạo** — chắc chắn nhưng thầy phải làm tay cho từng phụ huynh.
Đề xuất thêm đường tự phục vụ ở trang "Tài khoản này chưa nối với con":

| Cách khớp | Rủi ro | Kết luận |
|---|---|---|
| Họ tên con + ngày sinh con | Bạn cùng lớp biết sinh nhật nhau (Facebook, Zalo) → tự tạo tài khoản "phụ huynh" xem điểm bạn. HS 14–18 rất nhạy chuyện điểm bị bạn biết (Dahl–Steinberg, `DE-XUAT-NGHIEN-CUU-HS-14-22`) | **Không đủ** một mình |
| SĐT của con | Bạn bè biết số; con có thể đổi số; con có thể tự nối tài khoản giả để "phụ huynh" không phải bố mẹ thật | **Không dùng** |
| **Họ tên con + ngày sinh con + SĐT phụ huynh đã khai lúc đăng ký học** (`thpt_registration_requests.parent_phone` / `thpt_registrations.contact`) | SĐT phụ huynh là thứ chỉ phụ huynh và thầy có | **Đề xuất** |

Luật đi kèm:
1. Cả 3 phải khớp (tên so không dấu, bỏ khoảng trắng thừa; SĐT so 9 số cuối). Khớp → nối ngay.
2. Nối xong **báo cho thầy và cho con** ("Tài khoản phụ huynh Nguyễn Văn A vừa nối với con lúc …") — người lạ nối được thì
   con/thầy thấy ngay và gỡ một chạm. Đây là lớp bảo vệ chính, không dựa vào việc "đoán không ra".
3. Tối đa 5 lần thử sai / tài khoản / ngày; sai không nói sai ở ô nào (tránh dò từng trường).
4. Không khớp (thường do lúc đăng ký chưa khai SĐT phụ huynh) → nút **"Gửi yêu cầu để thầy duyệt"**: tạo yêu cầu chờ,
   thầy duyệt một chạm trong hồ sơ học sinh. Link mời `PH…` giữ nguyên làm đường nhanh.

Cần làm khi thầy duyệt: migration bảng `parent_link_requests` (RLS + revoke anon), RPC `security definer`
`claim_parent_by_child_info(p_name, p_birth date, p_phone)` có đếm lượt sai, thông báo qua `notifications`; form 3 ô
ở `app/phu-huynh/page.tsx` (`NoChildYet`). Trước đó kiểm: bao nhiêu học sinh có `profiles.birth_date` và SĐT phụ huynh.
