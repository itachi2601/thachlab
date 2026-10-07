# AGENTS — chi tiết (tách khỏi AGENTS.md để giảm token mỗi phiên)
Mục 1: migration (dòng 78–101 cũ). Mục 2: tối ưu tốc độ đăng nội dung. Mục 3: gọi AI provider.

## Vì sao phải là máy của Thạch
Sandbox đám mây và sandbox gắn thiết bị đều bị proxy chặn `*.supabase.co` (403 CONNECT),
và cũng không có `SUPABASE_SERVICE_ROLE_KEY` / mật khẩu DB. Khóa service role không được
đưa vào hội thoại. Claude Code chạy trên macOS có sẵn `.env.local` và CLI đã `link` —
đó là nơi duy nhất chạy được.

## Trước khi chạy migration — kiểm số thứ tự và kiểm đã chạy chưa
- Mảng `FILES` trong `scripts/run-migrations.sh` bị nhiều phiên cùng sửa, số thứ tự đổi bất ngờ (06/10/2026: `--only 4` chạy nhầm
  file sổ học phí thay vì dọn trùng). Ngay trước khi chạy: `bash scripts/run-migrations.sh --list`, đối chiếu **tên file**, rồi mới
  dùng `--only N` — hoặc chạy thẳng `supabase db query --linked -f <file>`.
- Kiểm migration đã chạy chưa: xem `scripts/logs/` (log cùng tên file), bảng sao lưu `*_backup_*` đã tồn tại chưa, và mục
  "ĐANG CHỜ" / "ĐÃ CHẠY" trong `STATE.md`. Chạy lại migration có `create table` sao lưu sẽ báo lỗi "already exists".
  Bổ sung sau khi file đã chạy → tách file mới (bảng sao lưu tên khác), không sửa file cũ.

## Dọn câu trùng ngân hàng câu hỏi — quét bằng ghép cặp, lặp tới khi sạch
- 2026-10-06 · Đợt dọn 1 dùng RPC `find_similar_bank_questions*` (giới hạn 20 cặp/câu, 300 cặp/lần, timeout ở chủ đề lớn) nên bỏ sót
  597 cặp giống 1,00 và 4 chủ đề khối 12; quét lại mới thấy → đợt 2. Dọn trùng: quét bằng truy vấn ghép cặp trực tiếp
  (`supabase db query --linked` với `set statement_timeout = 0`, `question_bank_plain_text(question) % ...`), xoá cặp 1,00 (giữ 1 câu/cụm),
  chỉ lưu trữ cặp 0,9–<1,00, rồi **quét lại ngay và lặp tới khi không còn cặp 1,00**. Mỗi đợt một bảng sao lưu tên khác
  (`question_bank_dedup_backup_<ngày>[b|c]`). Truy vấn đếm theo từng dải trên cả khối dễ bị gateway 524 — chỉ đếm dải ≥0,9.

## Bảng mới tạo trong `public` — bật RLS ngay trong cùng file
- 2026-10-07 · Supabase báo CRITICAL `rls_disabled_in_public` (3/10): 8 bảng sao lưu (`*_backup_*`, `*_fix_*`) tạo bằng `create table ... as select` không có RLS nên khoá `anon` đọc/ghi/xoá được. Mọi `create table` trong `public` (kể cả bảng sao lưu tạm) phải kèm `alter table ... enable row level security` và `revoke all ... from anon, authenticated` ngay trong file migration; bảng sao lưu không cần policy (service_role/postgres vẫn bypass). Sau mỗi đợt dọn dữ liệu, kiểm: `select relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where n.nspname='public' and c.relkind=chr(114) and not c.relrowsecurity` phải trả 0 dòng.


---

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

---

# Gọi AI provider trong code (DeepSeek/Anthropic) — đọc tài liệu hiện hành trước, test thật sau

- **Tên model bị khai tử theo thời gian** (`deepseek-chat`/`deepseek-reasoner` ngừng phục vụ 24/7/2026 → `deepseek-flash`
  / `deepseek-v4-pro`). Trước khi viết hoặc port một đoạn gọi AI, mở tài liệu hiện hành
  (api-docs.deepseek.com/updates, /api/create-chat-completion) xem tên model + tham số còn hợp lệ; code cũ KHÔNG phải
  nguồn tin. Gọi model đã khai tử → 400 `Model Not Exist`.
- Port tool use từ Anthropic sang DeepSeek: `tool_choice` chỉ đích danh hàm và `required` **không chạy khi thinking bật**
  (API trả 400) → phải đặt `thinking: {type:"disabled"}` và bù bằng model mạnh hơn.
- `supabase/functions/**` không nằm trong `tsconfig` và máy không có `deno` → **không typecheck được Edge Function**
  (chỉ kiểm được cú pháp). Vì vậy sau khi deploy phải **bấm thử thật trên web**. Deploy + `supabase secrets set` là việc
  của thầy trên Mac, agent không tự chạy.
- Script backfill chạy theo vòng "đọc các dòng còn thiếu nhãn → xử lý → đọc lại" **phải nhớ id đã thử trong chính lượt
  chạy đó** (kể cả câu AI trả lời không hợp lệ, kể cả khi `--dry-run` không ghi gì vào DB) rồi loại khỏi lượt đọc sau —
  không thì vòng lặp chạy vô hạn và đốt tiền API. Trước khi chạy thật, chạy `--dry-run` với số câu nhỏ và **đối chiếu
  tay vài dòng** với nội dung gốc — kiểm cả **một cặp câu cùng đề bài nhưng hỏi khác đại lượng** (nhãn phải khác
  nhau; nếu giống nhau là AI đang chép tên đề chứ không đọc nội dung câu).
- Trước khi viết lại cả một file (nhất là Edge Function / script dùng chung), so bản đang có với `git show HEAD:<file>`
  để biết có thay đổi chưa commit của phiên khác không — ghi đè là mất, không có backup. **Kiểm cả `git diff` của file
  trước khi commit**: nếu diff còn lẫn việc của phiên khác thì đừng commit cả file (bỏ lại cho phiên đó), và nhớ
  `git commit -- <path>` chỉ nhận file git đã biết — file MỚI phải `git add <path>` trước, nếu không sẽ báo
  `pathspec ... did not match any file(s) known to git`.


---
