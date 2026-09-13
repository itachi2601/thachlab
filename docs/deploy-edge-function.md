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
