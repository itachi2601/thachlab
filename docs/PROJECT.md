# PROJECT — Kiến trúc ThachLab

Nền tảng học Vật lý THPT của thầy Thạch (`thachlab.id.vn`). Tài liệu này mô tả
công nghệ, cấu trúc thư mục và cách triển khai.

## Công nghệ

| Lớp | Công nghệ |
|-----|-----------|
| Framework | **Next.js 16** (App Router, `output: export` — xuất tĩnh) |
| UI | **React 19**, **Tailwind CSS v4**, `framer-motion` |
| Ngôn ngữ | **TypeScript 5** |
| Dữ liệu / Auth | **Supabase** (Postgres + Auth + Storage), truy cập client-side qua anon key, bảo mật bằng **RLS** |
| Nội dung | Markdown (`gray-matter` + `marked`) cho blog; `katex` cho công thức |
| Import đề | `mammoth` (đọc file `.docx`) |
| Icon | `lucide-react` |

> ⚠️ Đây **không phải** Next.js quen thuộc — đọc `node_modules/next/dist/docs/`
> trước khi viết code (xem `AGENTS.md`).

## Mô hình triển khai

- **Xuất tĩnh** (`output: export`) → deploy lên shared hosting **LiteSpeed**
  (`thachlab.id.vn`), nơi **không có Node.js server**.
- Mọi tương tác dữ liệu là **client component** gọi thẳng Supabase.
- `trailingSlash: true` — mỗi trang thành `thư-mục/index.html`, bắt buộc với
  Apache/LiteSpeed để tránh lỗi 403 khi có route con (vd `/lop-hoc/bai`).
- Biến môi trường (`.env.local`): `NEXT_PUBLIC_SUPABASE_URL`,
  `NEXT_PUBLIC_SUPABASE_ANON_KEY`.

## Cấu trúc thư mục

```
app/                 Route (App Router)
  page.tsx           Trang chủ (landing)
  dang-ky, dang-nhap Xác thực học sinh
  tai-khoan          Trang tài khoản
  quan-tri           Trang quản trị (admin)
  lop-hoc, lop-hoc/bai   Chương → bài học
  kiem-tra, kiem-tra/lam Danh sách & làm bài thi
  tin-tuc, tin-nhan  Bài đăng & tin nhắn
  blog, blog/[slug]  Blog tĩnh (SEO)
components/          UI theo miền (home, admin, exams, physics, auth, blog, layout, ui)
features/            Kiểu dữ liệu & logic miền (exams, lessons); wordImport
services/            Tầng truy cập Supabase (supabase, content, classes, lessons)
lib/                 Physics engine + tiện ích (blog, physics)
content/blog/        Bài viết Markdown
docs/                Tài liệu + SQL schema/migration/seed
public/              Ảnh, tài nguyên tĩnh
```

## Luồng dữ liệu

1. Trang tĩnh render sẵn khung; component client fetch dữ liệu từ Supabase.
2. RLS quyết định quyền: học sinh chỉ thấy dữ liệu của mình / lớp mình; admin
   quản trị toàn bộ (hàm `is_admin()`).
3. Admin nhập liệu qua `/quan-tri`; học sinh học ở `/lop-hoc` và thi ở `/kiem-tra`.

Xem thêm: [`DATABASE.md`](./DATABASE.md), [`UI.md`](./UI.md),
[`BRAND.md`](./BRAND.md), [`ROADMAP.md`](./ROADMAP.md).

## Lệnh

```bash
npm run dev     # phát triển
npm run build   # build + xuất tĩnh ra ./out
npm run lint    # eslint
```
