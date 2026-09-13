# Deploy Edge Function `import-roster` (làm 1 lần)

Function này tạo tài khoản Supabase Auth cho sinh viên khi giảng viên nhập danh sách Excel —
cần `service_role key` nên phải chạy trên Supabase, không thể chạy trong trình duyệt (xem
`supabase/functions/import-roster/index.ts`). Chỉ cần deploy 1 lần; sau đó tính năng "Nhập danh
sách" trên dashboard hoạt động tự động, không cần làm lại các bước này trừ khi sửa code function.

## 1. Cài Supabase CLI (1 lần trên máy)

```bash
brew install supabase/tap/supabase
```

## 2. Đăng nhập & liên kết dự án (1 lần)

```bash
supabase login
```

Lệnh trên mở trình duyệt để đăng nhập tài khoản Supabase của anh. Sau đó, tại thư mục gốc dự án:

```bash
supabase link --project-ref <project-ref>
```

`<project-ref>` là đoạn mã trong URL dự án Supabase, ví dụ URL là
`https://abcdefgh.supabase.co` thì project-ref là `abcdefgh` (xem thêm ở Supabase Dashboard →
Settings → General → Reference ID).

## 3. Deploy function

```bash
supabase functions deploy import-roster
```

Không cần `supabase secrets set` — 3 biến `SUPABASE_URL`, `SUPABASE_ANON_KEY`,
`SUPABASE_SERVICE_ROLE_KEY` được Supabase tự động cấp cho mọi Edge Function.

## 4. Kiểm tra

Vào `/quan-tri/nhap-diem`, nhập thử 1 file Excel có 2–3 dòng, xác nhận tài khoản mới đăng nhập
được ở `/dang-nhap` bằng mã số sinh viên làm cả username lẫn mật khẩu.

Nếu cần sửa lại function sau này: sửa `supabase/functions/import-roster/index.ts` rồi chạy lại
`supabase functions deploy import-roster`.

---

# Deploy Edge Function `invite-staff` (làm 1 lần)

Function này gửi email mời giảng viên / trợ giảng từ trang **Quản trị → Phân công giảng viên**.
Cũng cần `service_role key` (`auth.admin.inviteUserByEmail`) nên phải chạy trên Supabase.

Các bước 1–2 ở trên (cài CLI, `supabase login`, `supabase link`) chỉ làm một lần cho cả dự án —
nếu đã làm khi deploy `import-roster` thì bỏ qua, chạy thẳng:

```bash
supabase functions deploy invite-staff
```

Trước đó nhớ chạy `docs/supabase-migration-staff-invites.sql` trong SQL Editor (tạo bảng
`staff_invites`, `ta_assistant_classes`, hàm `apply_staff_invite` và trigger tự nhận lời mời).

## Kiểm tra

Vào `/quan-tri/phan-cong-giang-vien` → mục **Mời người mới qua email**, mời thử một địa chỉ
email bạn kiểm tra được. Người được mời bấm link trong mail để đặt mật khẩu; đăng nhập xong là
đã có sẵn vai trò và lớp được phân công. Mời một email **đã có tài khoản** thì không gửi mail
lại, hệ thống cấp quyền và gán lớp ngay (thông báo "đã có tài khoản").

## Giới hạn email

Email mời do Supabase Auth gửi. Gói free giới hạn khoảng **4 email/giờ** và dễ vào thư mục spam.
Nếu cần mời nhiều người một lúc, vào Supabase Dashboard → Authentication → Emails → SMTP Settings
để cấu hình SMTP riêng (Resend, SendGrid, Gmail…). Không cấu hình thì vẫn dùng được, chỉ là mời
rải rác từng người.

Nếu email không tới nơi: bảo người đó tự đăng ký tại `/dang-ky` bằng **đúng địa chỉ email đã được
mời** — trigger `zz_claim_staff_invite` sẽ tự cấp quyền và gán lớp như khi nhận lời mời.
