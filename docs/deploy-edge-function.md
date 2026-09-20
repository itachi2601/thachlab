# Deploy Edge Functions (làm 1 lần mỗi function)

Các function dưới đây cần `service_role key` nên phải chạy trên Supabase, không thể chạy trong
trình duyệt (site build tĩnh, không có server Node):

- `import-roster` — tạo tài khoản Supabase Auth cho sinh viên khi giảng viên nhập danh sách Excel
  (`supabase/functions/import-roster/index.ts`).
- `reset-student-password` — giáo viên đặt lại mật khẩu cho học sinh không có email thật, dùng khi
  học sinh quên mật khẩu nhưng không tự dùng được `/quen-mat-khau`
  (`supabase/functions/reset-student-password/index.ts`).

Chỉ cần deploy 1 lần mỗi function; sau đó tính năng tương ứng hoạt động tự động, không cần làm
lại các bước này trừ khi sửa code function.

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
supabase functions deploy reset-student-password
```

Không cần `supabase secrets set` — 3 biến `SUPABASE_URL`, `SUPABASE_ANON_KEY`,
`SUPABASE_SERVICE_ROLE_KEY` được Supabase tự động cấp cho mọi Edge Function.

## 4. Kiểm tra

- `import-roster`: vào `/quan-tri/nhap-diem`, nhập thử 1 file Excel có 2–3 dòng, xác nhận tài
  khoản mới đăng nhập được ở `/dang-nhap` bằng mã số sinh viên làm cả username lẫn mật khẩu.
- `reset-student-password`: vào mục Học sinh trong `/quan-tri`, chọn 1 học sinh, bấm "Đặt lại
  mật khẩu", xác nhận học sinh đăng nhập lại được bằng mật khẩu mới.

Nếu cần sửa lại function nào sau này: sửa file trong `supabase/functions/<tên function>/index.ts`
rồi chạy lại `supabase functions deploy <tên function>`.
