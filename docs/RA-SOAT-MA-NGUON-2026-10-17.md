# Rà soát mã nguồn Thachlab — 17/10/2026

Phạm vi: rà mẫu bằng grep + đọc các điểm nóng (Edge Function, migration, deploy.sh, ContentHtml). **Chưa** đọc toàn bộ 92k dòng, chưa chạy thử tấn công thật. Kết luận dưới đây là đề xuất, chưa sửa gì.

## Bối cảnh kiến trúc (quyết định mọi thứ còn lại)
Site là `output: "export"` (HTML tĩnh trên LiteSpeed) + Supabase (Postgres/RLS/Edge Function). Không có server Next.js → không có API route để bị tấn công; "tải" chia làm 2: (1) hosting tĩnh, (2) Supabase (RPC/RLS/Edge). Rủi ro lớn nhất nằm ở (2) và ở tiền API AI.

## A. Bảo mật — theo mức độ

**Cao**
1. `check-exam` (Anthropic) và `classify-questions` (DeepSeek) chỉ kiểm "đã đăng nhập", **không kiểm vai trò**. Học sinh nào có JWT cũng gọi được, mỗi lần tới 16000 token → đốt tiền API. `hsg-ai-grade` và `draw-figure` đã kiểm `is_staff`/role đúng — chép mẫu đó sang hai hàm kia. Thêm trần số lần/giờ theo user (bảng đếm).
2. `reset-password` nhánh `claim` **không cần đăng nhập, không giới hạn số lần thử mã**. An toàn hay không phụ thuộc độ dài/entropy của cột `code` (mặc định ở DB — chưa xác minh). Cần: mã ≥ 8 ký tự ngẫu nhiên mật mã, khoá sau 5 lần sai (theo IP/mã), hết hạn ngắn. Mật khẩu mới chỉ ≥ 6 ký tự; nhánh `admin` đặt mật khẩu = mã số HS (đoán được) — nên bắt đổi ở lần đăng nhập đầu.
3. `resolve_login_email` mở cho `anon`: ai cũng dò được username → email thật (liệt kê tài khoản, lộ email). Đổi sang Edge Function có giới hạn tần suất, hoặc đăng nhập bằng username qua hàm trả kết quả đồng nhất; tối thiểu không trả email về client.
4. RPC mở cho `anon` (`quiz_join`, `quiz_answer`, `quiz_state`, `rank_public_honor`): cần chặn spam (số người/phòng, độ dài, tần suất). Tạo hàng loạt `quiz_players` ẩn danh là vector làm đầy DB.

**Trung bình**
5. Edge Function đặt `Access-Control-Allow-Origin: *` — hạ xuống `https://thachlab.id.vn` (JWT vẫn bắt buộc nên rủi ro thấp, nhưng không cần mở).
6. 7 file migration có `security definer` nhiều hơn `set search_path` (perf_rls 19/18, difficulty_source 5/3, thpt_fee_ledger 13/12, quiz_live 14/13, …). Có thể do đếm trong comment, nhưng phải lập danh sách hàm definer thiếu `search_path` từ DB thật (`pg_proc.proconfig is null`) và vá bằng 1 migration.
7. Không có header bảo mật: `deploy.sh` ghi `.htaccess` chỉ có cache/nén/chặn PHP. Thêm `X-Content-Type-Options`, `Referrer-Policy`, `X-Frame-Options`/`frame-ancestors`, `Permissions-Policy`, HSTS; CSP bắt đầu ở chế độ `Report-Only` (site có script inline + KaTeX + YouTube nocookie nên cần chỉnh).
8. `dangerouslySetInnerHTML` ở 6 file; `ContentHtml` render HTML từ DB mà **không có sanitizer** (không DOMPurify). Nguồn là giáo viên/admin nên rủi ro thấp, nhưng nếu một tài khoản giáo viên/TA bị chiếm, XSS lan sang mọi học sinh (và phiên admin). Thêm sanitize (allowlist thẻ/thuộc tính, cho phép KaTeX/svg/iframe youtube-nocookie) ở thời điểm lưu hoặc render.
9. `heic2any`, `xlsx` lấy từ `cdn.sheetjs.com` (không qua npm, không khoá hash theo registry) — `npm audit` + ghim phiên bản/tarball hash; xlsx/exceljs chỉ dùng ở admin thì tách khỏi bundle HS.

**Thấp / vệ sinh**
10. Không có file `.env` bị commit, không có khoá hardcode (chỉ nhắc tên biến) — tốt.
11. Bảng mới: 47 `create table` vs 49 `enable rls` — khớp; vẫn nên có test CI quét `pg_tables where rowsecurity=false`.
12. Service-role chỉ ở script cục bộ + Edge Function — đúng thiết kế.

## B. Chịu tải / chống tấn công lưu lượng
- Phần tĩnh: không có CDN. Mọi lượt tải ~40MB asset đổ vào shared hosting. → Đặt Cloudflare (gói free) trước tên miền: cache, WAF, rate-limit, chặn bot; cache ảnh/JS dài hạn đã có sẵn header nên đổi gần như không tốn công.
- Hosting dùng chung có quota (sự cố `tmp_pack` hết quota 17/10): đặt cảnh báo dung lượng, và không để repo/`.git` nằm trong web root.
- Supabase là điểm nghẽn thật (lúc cả lớp vào bài cùng lúc): đã có RPC gộp (`/`, `/lop-hoc/bai`, `/kiem-tra/lam`). Việc cần làm: bật Supabase **Auth rate limits + CAPTCHA (Turnstile) ở đăng nhập/đăng ký**, kiểm gói (pool kết nối, giới hạn Realtime cho quiz live), thêm pooler transaction mode; đo bằng k6 một kịch bản 100–300 HS làm bài đồng thời (có `perf*/` làm nền).
- Giới hạn tần suất cho RPC ghi từ client (nộp bài, heartbeat live, quiz): hiện chưa thấy cơ chế. Thêm kiểm "mỗi user ≤ N lần/phút" trong hàm SQL (bảng `rate_hits`) cho các hàm ghi.
- Heartbeat/presence: đảm bảo khoảng ≥ 20–30s và tắt khi tab ẩn, tránh tự DDoS khi cả trường dùng.

## C. Tinh gọn & bảo trì
- Repo: `.git` 930MB (có `garbage tmp_pack` 4MB), `content` 338MB/4.4k file, `public` 83MB. → `git gc --prune=now`; đưa ảnh/media nặng ra Supabase Storage hoặc Git LFS; cân nhắc tách `content/` thành repo riêng.
- Thư mục rác ở gốc: `perf`, `perf2..perf5`, `feat`, `home`, `tmp`, `bao-gia`, `GEMINI.md`, `tsconfig.tsbuildinfo` → gom vào `docs/archive/` hoặc xoá (hỏi thầy từng thư mục; `home/` có thể là component còn dùng — kiểm import trước).
- Cấu trúc code rải rác: `components/`, `features/`, `home/`, `hooks/`, `services/`, `lib/` đều chứa logic. Chọn một quy ước (`features/<tên>/{components,services,hooks}`) và áp dụng dần cho module mới, không di chuyển hàng loạt.
- File quá lớn: `app/lop-hoc/bai/page.tsx` 2244 dòng, `CncCourseWorkspace` 1389, `LessonsAdmin` 1317, `QuestionBankAdmin` 1297, `services/analytics.ts` 1064, `tutoring.ts` 1050. Tách theo vùng chức năng (hook dữ liệu / phần hiển thị / phần admin), đụng tới khi nào sửa tới đó.
- `scripts/` 740 file tracked: phân thư mục `scripts/{migrate,backfill,dang-de,kiem-tra,one-off}`; one-off đã chạy xong → `scripts/archive/`.
- Test tự động chỉ có 3 script `test:*`; thêm CI (GitHub Actions đã có workflow gộp nhánh) chạy `tsc --noEmit`, `eslint`, `build`, và test RLS bằng `perf/rls-pglite-check.mjs` mỗi lần có migration.
- `package.json`: `framer-motion`, `heic2any`, `exceljs`, `xlsx` — kiểm xem có nằm trong bundle trang HS (dùng `@next/bundle-analyzer` đã có).

## D. Đề xuất chia đợt
| Đợt | Nội dung | Rủi ro | Cần thầy |
|---|---|---|---|
| 1 (ngay, nhỏ) | Mục A1 (kiểm vai trò + trần lượt gọi 2 Edge Function), A5, kiểm entropy mã reset (A2), `git gc` | Thấp | Deploy Edge Function |
| 2 | Cloudflare + header `.htaccess` + CSP Report-Only; Auth rate limit + Turnstile | Thấp–TB | Cấu hình DNS/Supabase dashboard |
| 3 | Migration: giới hạn `claim` reset, `resolve_login_email`, rate-limit RPC `anon`/ghi, vá `search_path` | TB (động DB) | Chạy `run-migrations.sh` ngoài giờ HS |
| 4 | Sanitize HTML (`ContentHtml` + nơi lưu), `npm audit`/ghim phụ thuộc | TB | Rà trên bài thật để không vỡ KaTeX/SVG |
| 5 | Kiểm thử tải k6 100–300 HS; điều chỉnh theo kết quả | Thấp | Chạy ngoài giờ |
| 6 | Dọn repo/thư mục, tách file lớn, CI | Thấp | Duyệt danh sách xoá |

Chưa xác minh (cần xem DB thật, sandbox không với tới Supabase): entropy cột `password_reset_codes.code`, danh sách hàm definer thiếu `search_path` thực tế, policy RLS từng bảng, cấu hình Auth rate limit hiện tại.
