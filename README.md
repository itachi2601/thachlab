# ThachLab

Trang học Vật lí THPT + LMS (Next.js 16 App Router, `output: "export"`, mọi dữ liệu đọc từ trình duyệt qua Supabase anon key + RLS). Bản build là site tĩnh, deploy lên shared hosting LiteSpeed `thachlab.id.vn`.

## Chạy cục bộ

```bash
npm install
cp .env.example .env.local   # hoặc tự tạo, xem biến môi trường bên dưới
npm run dev
```

Biến môi trường trong `.env.local`:

| Biến | Dùng cho |
|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | URL project Supabase (bắt buộc) |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | anon key — trình duyệt và `scripts/build-content.mjs` (bắt buộc) |
| `NEXT_PUBLIC_SITE_URL` | URL công khai của site |
| `SUPABASE_SERVICE_ROLE_KEY` | chỉ vài script quản trị trong `scripts/`; KHÔNG commit, KHÔNG dùng trong app |

## Build và deploy

```bash
npm run build          # prebuild tự chạy: build-content (học liệu tĩnh) + gen-image-dimensions
scripts/deploy.sh      # build rồi force-push thư mục out/ lên nhánh `deploy`; hosting kéo về mỗi 10 phút
```

### Học liệu tĩnh (`public/data/`) — **sau khi đăng/sửa bài phải build lại**

`npm run build` chạy `scripts/build-content.mjs` trước: đọc Supabase bằng **anon key** (đúng những gì khách chưa đăng nhập xem được) và ghi

- `public/data/catalog.json` — lớp → chương → bài (kèm mô tả/YCCĐ) + tham chiếu mục (id, đề gắn);
- `public/data/lessons/<id>.json` — mỗi bài: lý thuyết/video có nội dung, các mục khác chỉ metadata;
- `public/data/manifest.json` — `generatedAt` + số lượng.

Trang học sinh (`/lop-hoc`, `/lop-hoc/bai`, trang chủ HS) đọc các file này trước (cùng origin, host cache 10 phút qua `out/data/.htaccess`), rồi gọi Supabase một truy vấn nhẹ để đối chiếu: danh sách bài, tên, mô tả, mục, đề gắn khác đi → tự tải bản mới. **Riêng nội dung lý thuyết sửa tại chỗ** (cùng tên, cùng mục) chỉ lên web sau khi chạy lại `scripts/deploy.sh` — các bảng chưa có cột `updated_at` để phát hiện.

File tĩnh không chứa đề thi, đáp án hay lời giải bài tập mẫu (những thứ đó vẫn lấy từ Supabase như cũ). Thư mục `public/data/` không commit (`.gitignore`); thiếu env hoặc Supabase lỗi thì script chỉ cảnh báo, giữ file cũ (không có thì ghi manifest rỗng) và trang tự lùi về gọi Supabase như trước. Khu quản trị/giáo viên không dùng lớp tĩnh.

### Cache & nén trên hosting (`.htaccess` sinh bởi `scripts/deploy.sh`)

`scripts/deploy.sh` tự sinh `out/.htaccess` sau mỗi lần build:

- `js|css|woff2?` — cache 1 năm (tên file có hash, đổi nội dung là đổi tên).
- `png|jpe?g|webp|svg|gif` — cache **30 ngày**. Ảnh KHÔNG có hash trong tên file, nên **sửa một
  ảnh đã đăng (bài học, đề thi...) phải upload với TÊN FILE MỚI, không được ghi đè file cũ** — nếu
  ghi đè, trình duyệt học sinh vẫn hiển thị ảnh cache cũ tối đa 30 ngày dù server đã có bản mới.
- Nén `html|css|js|json|svg`: `mod_brotli` nếu hosting LiteSpeed có bật, fallback `mod_deflate`
  (gzip) nếu không — cả hai khối đặt trong `<IfModule>` nên không hỏng nếu module không tồn tại.
- Riêng `out/data/*.json` (học liệu tĩnh, xem mục trên) có `.htaccess` **cache 10 phút riêng**,
  tách biệt với khối cache ảnh 30 ngày ở trên — đừng gộp hai khối này lại.

## Cấu trúc

- `app/` — route; `components/`, `features/`, `services/` (truy vấn Supabase), `lib/`.
- `docs/supabase-*.sql` — schema và các migration (chạy bằng `supabase db query --linked -f <file>`).
- `scripts/` — script build/quản trị; `perf/` — mốc đo tốc độ.
- Quy ước cho AI agent: xem `AGENTS.md`.
