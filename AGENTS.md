<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

<!-- BEGIN:thachlab-docs-index -->
# Tài liệu — đọc khi cần, đừng đọc hết docs/

`docs/STATE.md` (hiện trạng + ĐANG CHỜ) và `docs/DATABASE.md` (99 bảng, cột + khoá ngoại, sinh tự
động) là hai file nên đọc trước khi đụng vào schema hoặc bắt đầu đợt việc lớn — **đọc DATABASE.md
thay vì `select *`/dò schema**. Chữ ký 216 hàm RPC ở `docs/DATABASE-RPC.md` (chỉ mở khi cần tên
hàm/tham số). Log migration đã chạy ở `docs/STATE-archive.md`. Các file khác trong `docs/` chỉ đọc
đúng file khớp chủ đề đang làm:

| Chủ đề | File |
|---|---|
| Đăng đề không qua skill (form tay) | `docs/DANG-DE-TU-WORD.md` |
| Tích hợp AZOTA | `docs/AZOTA-INTEGRATION.md` |
| Mastery/YCCĐ | `docs/mastery-rules.md` |
| Khoá học, ghi danh | `docs/KHOA-HOC.md` |
| Phụ đạo theo chủ đề | `docs/PHU-DAO.md` |
| Module SHCN (sinh hoạt chủ nhiệm) | `docs/SHCN-MODULE.md` |
| Phụ huynh xem kết quả | `docs/PHU-HUYNH.md` |
| Phân tích điểm/chủ đề hay sai | `docs/ANALYTICS-SETUP.md` |
| LaTeX Editor | `docs/LATEX-EDITOR-GUIDE.md` |
| Deploy Edge Function `import-roster` | `docs/deploy-edge-function.md` |
| Roadmap / định hướng sản phẩm | `docs/ROADMAP.md`, `docs/MANIFESTO.md`, `docs/PROJECT.md` |

Còn lại (`BRAND.md`, `UI.md`, `THONG-BAO.md`, `BAN-GIAO-*.md`, `prompt-toc-do-*.md`,
`prompt-toi-uu-font.md`, `rank-title-showcase-design.md`, `bai-viet-lo-trinh-*.md`) là log/prompt
lịch sử hoặc tài liệu chuyên biệt — grep theo từ khoá thay vì đọc hết khi cần tra.
<!-- END:thachlab-docs-index -->

<!-- BEGIN:thachlab-migrations -->
# Migration Supabase — quy tắc bắt buộc

Hiện trạng dự án: `docs/STATE.md`. Đọc file đó trước khi bắt đầu một đợt việc lớn.

## Agent KHÔNG được tự chạy migration lên production
Mọi thay đổi schema/policy/hàm chỉ được **viết thành file** trong `supabase/migrations/`,
kèm khối rollback ở cuối file (hoặc file `.down.sql` riêng trong `perf/rollback/`).
Không `supabase db push` (thư mục migrations mới, CLI không biết ~99 migration cũ).
Không tự gọi `supabase db query --linked` với lệnh ghi.

## Khi có migration mới đang chờ → tự xuất lệnh cho Thạch chạy
Kết thúc đợt việc, nếu `supabase/migrations/` có file chưa chạy trên production:

1. Cập nhật mảng `FILES` trong `scripts/run-migrations.sh` theo đúng thứ tự chạy.
2. In ra cho Thạch **đúng khối này**, không diễn giải dài:

```
bash scripts/run-migrations.sh
```

3. Kèm 3 dòng: mỗi file làm gì, file nào cần chạy ngoài giờ học sinh làm bài, lệnh rollback nếu hỏng.
4. Ghi các file đang chờ vào mục "ĐANG CHỜ" của `docs/STATE.md`.

Script đã lo: hỏi xác nhận từng file, ghi log `scripts/logs/`, dừng ngay khi lỗi,
nhắc lệnh rollback. `--yes` chạy thẳng, `--only N` chạy riêng một file.

## Vì sao phải là máy của Thạch
Sandbox đám mây và sandbox gắn thiết bị đều bị proxy chặn `*.supabase.co` (403 CONNECT),
và cũng không có `SUPABASE_SERVICE_ROLE_KEY` / mật khẩu DB. Khóa service role không được
đưa vào hội thoại. Claude Code chạy trên macOS có sẵn `.env.local` và CLI đã `link` —
đó là nơi duy nhất chạy được.

## Sau khi migration chạy xong
- Sinh lại sơ đồ bảng: `node scripts/gen-database-doc.mjs` (ghi `docs/DATABASE.md` + `DATABASE-RPC.md`),
  rồi chuyển mục vừa chạy từ "ĐANG CHỜ" trong `docs/STATE.md` sang `docs/STATE-archive.md`.
- Đối chiếu RPC: `npx tsx scripts/perf-compare-rpc.mts`
- Backfill mức độ câu hỏi — **GHI THẬT NGAY, không có dry-run**, tham số chỉ giới hạn số câu:
  `npx tsx scripts/backfill-question-bank-difficulty.mts 20` (thử nhỏ, xem lại UI rồi mới chạy hết)
<!-- END:thachlab-migrations -->

<!-- BEGIN:thachlab-perf-publish -->
# Đăng nội dung — luôn tối ưu tốc độ tải

5 đợt tối ưu tốc độ 25–27/9/2026 (`perf/RESULT.md`, memory `project_thachlab_perf_optimization`) đưa
Lighthouse trang chủ 68→91, trang bài 78→83, ảnh 4,6 MB→0,6 MB. **Mọi nội dung đăng MỚI** (bài học, đề,
ngân hàng câu hỏi, ảnh...) qua bất kỳ skill/route nào (`up-de-kiem-tra`, `dang-de-hang-loat`,
`dang-bai-hoc-thachlab`, `azota`, `ngan-hang-cau-hoi`, `/quan-tri/dang-de`, `/quan-tri/nhap-bai`) không
được kéo lùi kết quả này, và mọi code chạm tới các trang đó phải giữ nguyên tắc dưới đây.

## Ảnh
- Ảnh chèn vào HTML lưu DB (`raster_images[]` → Storage bucket `lesson-media`, `public/lessons/**`,
  `public/exams/**`): **nén trước khi đăng**, rộng tối đa ~1200px — đề/bài thường nhận thẳng ảnh scan
  gốc 2–5 MB/ảnh nếu không chủ động nén. `node scripts/optimize-images.mjs` lo ảnh trong `public/`; ảnh
  encode base64 vào bundle JSON (đi thẳng Storage, không qua `public/`) phải tự nén bằng `sharp`/công cụ
  tương đương TRƯỚC khi encode — không có bước nén tự động ở phía script/trang nhận.
- Ảnh mới thêm vào code (component, trang, không phải nội dung học liệu) → `.webp`, không PNG/JPG.
- Không nhúng base64 trực tiếp vào HTML lưu trong DB (nặng cả bản ghi lẫn payload tải trang) — trích ra
  file/Storage rồi tham chiếu `<img src="...">`.

## Component nặng
- Khối JS nặng thêm mới vào trang học sinh (đề dài, hoạt hình, thư viện lớn) phải tách bằng
  `next/dynamic({ssr:false})` và bọc `LazyErrorBoundary` (`components/ui/LazyErrorBoundary.tsx`) —
  không thêm chunk mới thiếu boundary (xem sự cố "crash trắng" đợt 4 trong memory
  `project_thachlab_perf_optimization`).
- Giữ KaTeX đồng bộ (không lazy) ở trang học sinh (bài học, làm đề); chỉ lazy ở trang admin/GV.

## Dữ liệu/Supabase
- Không tự thêm round-trip Supabase mới cho trang đã đo/tối ưu (`/`, `/lop-hoc/bai`, `/kiem-tra/lam`) —
  ưu tiên RPC gộp thay vì nhiều query rời khi đăng tính năng/nội dung mới chạm tới các trang này.

## Trước khi báo hoàn thành một đợt đăng có ảnh hoặc sửa code
Kiểm nhanh: ảnh mới > 150 KB đã nén chưa; nếu có sửa code trang, so dung lượng bundle JS liên quan (xem
`perf/chunks-report.mjs` nếu còn) hoặc chạy Lighthouse thủ công. Bỏ qua bước này khi chỉ đăng nội dung
text thuần (không ảnh, không đụng code).
<!-- END:thachlab-perf-publish -->
