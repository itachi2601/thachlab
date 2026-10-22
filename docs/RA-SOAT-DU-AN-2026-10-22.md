# Rà soát dự án ThachLab — 22/10/2026

Phạm vi: đo trên cây `main` (commit `a723b3282`), **chỉ đọc** — không sửa mã, không gọi DB production.
Số liệu lấy bằng lệnh ghi ở §8, kiểm lại được bất cứ lúc nào. Bản rà soát bảo mật trước đó:
`docs/RA-SOAT-MA-NGUON-2026-10-17.md` (12 điểm; phần lớn đã xử lý, xem §4.1).

## 0. Bảng điểm

| Tiêu chí | Điểm | Một câu |
|---|---:|---|
| Tinh gọn | **5,5/10** | Code gọn (16 dependency, 83k dòng cho 91 route) nhưng **repo nặng**: 507 MB file tracked, `.git` 1,2 GB, 1.184 file trong `scripts/`. |
| Sạch sẽ | **6,5/10** | `tsc` sạch, gần như không `any`, sanitizer có kiểm chứng; nhưng **lint đỏ 94 lỗi**, 1 dependency chết, README trỏ tới file không tồn tại, 4 file > 1.100 dòng. |
| Bảo mật | **7,5/10** | RLS + Edge Function + header + rate limit làm đúng bài bản; còn **2 lỗ thật**: điểm do trình duyệt tính rồi ghi thẳng, và `Permissions-Policy` chặn camera làm hỏng quét QR. |
| Phát triển lâu dài | **6,0/10** | Tài liệu/memory xuất sắc, nhưng **không có hàng rào tự động** (CI chỉ gộp nhánh, không test/build), lịch sử migration không dựng lại được DB, không có giám sát lỗi runtime. |

Tổng: **6,4/10 — nền tốt, thiếu tự động hoá và kỷ luật cấu trúc.**

## 1. Độ tinh gọn

**Điểm mạnh**
- 16 dependency runtime, không framework UI nặng; `framer-motion`, `exceljs`, `xlsx`, `jsqr`, `heic2any` đều nạp động (lazy) đúng chỗ.
- 82.955 dòng TS/TSX cho 91 route, 99+ bảng — mật độ hợp lý, không có lớp abstraction thừa.
- Build tĩnh 106 MB, JS 11,5 MB toàn site; chunk lớn nhất 1,3 MB là ExcelJS (chỉ tải khi bấm xuất Excel).

**Điểm nặng**
| Thứ | Số đo | Vấn đề |
|---|---:|---|
| `content/` | 353 MB / 4.756 file | Ảnh `.webp` (2.268 file, 254 MB) + mp3 (1.899 file, 36 MB) + 1.827 HTML nằm trong git. Clone/backup/sao lưu đều phải kéo theo. |
| `.git` | 1,2 GB (pack lớn nhất 164 MB) | Lịch sử chứa toàn bộ media; mỗi lần sửa 1 ảnh là thêm 1 bản vào lịch sử. |
| `scripts/` | 1.184 file tracked, 264 file nằm phẳng ở gốc | 200 `.mts` + 174 `.py` một lần; 161 script tự `createClient`, 36 bản copy `readEnvLocal`. |
| `docs/` | 189 file gốc + 161 file `docs/memory/` | Tài liệu tốt nhưng không có chỉ mục; file cũ (BAN-GIAO-*, prompt-*) vẫn ngang hàng file đang sống. |
| Root | còn `perf/`, `book/` (63 MB), `bao-gia/`, `assets/` | Đã dọn một phần 21/10, còn sót thư mục chuyên biệt ở gốc. |

**Kết luận:** phần *code* tinh gọn; phần *dữ liệu và vận hành* phình. Nên tách “nguồn soạn nội dung” khỏi “repo web”.

## 2. Sạch sẽ

**Điểm mạnh**
- `npx tsc --noEmit`: **0 lỗi** (strict, `scripts` và `supabase/functions` đã loại khỏi tsconfig — hợp lý).
- Toàn cây app/components/lib/services: **1 chỗ `any`**, **1 TODO**, 35 `@ts-expect-error`/`eslint-disable`.
- Một nguồn Supabase client duy nhất; env đọc qua `lib/supabase-env.ts` (tách để không kéo SDK vào trang công khai).
- Sanitizer dùng chung `lib/sanitize-html.ts` + `sanitize-html-client.ts`, đã thử trên 27.600 chuỗi nội dung thật; 11 chỗ `dangerouslySetInnerHTML` đều có lý do (JSON-LD, blog từ repo, nội dung qua DOMPurify).

**Điểm chưa sạch**
1. **Lint đỏ: 94 error + 20 warning** (`npm run lint` sẽ fail). 77 lỗi `react-hooks/set-state-in-effect`, 7 `preserve-manual-memoization`, 4 `refs` — đây là rule mới của React 19/Next 16, phần lớn là nợ kỹ thuật thật (state đồng bộ trong effect), không chỉ là style.
2. **Dependency chết**: `@xmldom/xmldom` (không file nào import; đã ghi nhận từ `perf/BASELINE.md` mà chưa gỡ).
3. **`dompurify` nằm ở `devDependencies`** nhưng import trong code chạy thật (`lib/sanitize-html-client.ts`). Build hiện vẫn qua vì cài đủ devDeps; `npm ci --omit=dev` sẽ gãy.
4. **README hướng dẫn `cp .env.example .env.local` nhưng repo không có `.env.example`** — người mới (hoặc phiên cloud) không biết cần biến nào ngoài bảng trong README.
5. **File quá lớn** (khó review, dễ xung đột khi hai phiên cùng sửa):
   `app/lop-hoc/bai/page.tsx` 2.348 · `LessonsAdmin` 1.430 · `CncCourseWorkspace` 1.389 · `QuestionBankAdmin` 1.306 · `ExamSection` 1.193 · `StudentResultsDashboard` 1.097 · `services/analytics.ts` 1.070.
6. **Hai quy ước cùng tồn tại**: `services/` (94 file phẳng) và `features/` (20 file, gần như bỏ hoang). `components/` vẫn gọi thẳng `supabase.from(...)` 40 chỗ, còn `services/` 68 chỗ — không có ranh giới rõ.
7. Không có `.nvmrc`/`engines`: Node 20 vs 22 có thể cho kết quả build khác nhau.
8. Số liệu trong tài liệu nạp mỗi phiên dễ lỗi thời: `AGENTS.md` còn ghi “99 bảng”, trong khi `docs/DATABASE.md` sinh tự động 20/10 đã là **157 bảng**; README vẫn hướng dẫn `.env.example` không tồn tại.

## 3. Bảo mật

### 3.1 Đã làm tốt (đáng giữ)
- **RLS là hàng rào chính** và được làm nghiêm: 152 `create policy`, có báo cáo kiểm chứng bằng pglite (`perf/RLS_REPORT.md`), 2 policy tautology (`e.course_id = e.course_id`) và `class_assessments using (true)` **đã sửa và chạy production 26/9**.
- **Edge Function kiểm vai trò thật**, không chỉ “đã đăng nhập”: `check-exam` và `classify-questions` gọi `is_staff` + hạn mức giờ; `reset-password` nhánh admin dùng `teaches_student`; CORS đã hạ từ `*` về `https://thachlab.id.vn`.
- **Chống dò mã**: `rl_allow` theo IP cho `reset-password` claim, `quiz_join`, `resolve_login_email`.
- **Header bảo mật** trong `scripts/deploy.sh`: HSTS, nosniff, Referrer-Policy, X-Frame-Options, Permissions-Policy, CSP **Report-Only** đã có nội dung.
- **Không lộ khoá**: không có `service_role`/API key trong file tracked; `.env*` bị gitignore; service role chỉ dùng ở script cục bộ + Edge Function.
- **Chống tự nâng quyền**: policy update `profiles` chỉ cho `role='student'` khi `id = auth.uid()`; `anon` đã bị thu hồi khỏi các RPC definer nguy hiểm (migration 21/10).

### 3.2 Lỗ hổng / rủi ro còn lại
| Mức | Vấn đề | Bằng chứng | Hướng xử lý |
|---|---|---|---|
| **Cao (toàn vẹn dữ liệu)** | Điểm bài làm do **trình duyệt tính** rồi `insert` thẳng vào `exam_results`; policy chỉ ràng `student_id = auth.uid()`. Học sinh mở DevTools là chèn được điểm 10 cho bất kỳ đề nào (không sửa/xoá được sau đó, nhưng đủ làm sai lệch xếp hạng, danh hiệu, báo cáo phụ huynh). | `components/exams/ExamRunner.tsx:217-229`, policy `student inserts own result` | RPC `submit_exam_result` tính điểm phía server từ đáp án đã lưu; giữ insert trực tiếp cho bài luyện tập không tính điểm. |
| **Cao (chức năng)** | `Permissions-Policy: camera=()` chặn `getUserMedia` → **quét QR đề không mở được camera** trên bản deploy, dù code có `QrScannerCard` dùng camera. | `scripts/deploy.sh:59` vs `components/scan/QrScannerCard.tsx:77` | Đổi thành `camera=(self)`; thử lại trên iPhone + Android thật. |
| Trung bình | CSP mới ở Report-Only, chưa chặn; `unsafe-inline`/`unsafe-eval` còn cần cho Next export + KaTeX. | `deploy.sh:61-65` | Rà console trên 5 trang đại diện rồi chuyển sang enforcing. |
| Trung bình | `resolve_login_email` vẫn trả **email thật** cho `anon` (chỉ giảm tốc độ dò). | migration `20261017120000` | Trả kết quả đồng nhất hoặc chuyển sang Edge Function. |
| Trung bình | 215 chỗ `security definer` nhưng chỉ 91 file migration nhắc `search_path`; **chưa xác minh trên DB thật** hàm nào thiếu `set search_path`. | `pg_proc.proconfig` chưa được đối chiếu | 1 migration vá theo danh sách sinh từ DB, như A6 của báo cáo 17/10. |
| Thấp | `xlsx` cài từ URL CDN `cdn.sheetjs.com` (không qua registry, không ghim hash). | `package.json` | Tải về `vendor/` kèm hash, hoặc thay bằng `exceljs` đã có. |
| Thấp | `dompurify` ở devDependencies; thiếu `.env.example`; không có CAPTCHA/Turnstile (chưa xác minh dashboard Supabase). | `package.json`, README | Sửa 3 dòng; xác minh Auth rate limit trên dashboard. |

## 4. Khả năng phát triển lâu dài

### 4.1 So với báo cáo 17/10
Đã xử lý: A1 (vai trò + hạn mức AI), A2 (giới hạn claim), A4 (rate limit `quiz_join`), A5 (CORS), A7 (header), A8 (sanitizer), A9 một phần.
Còn: A3 (email enumeration), A6 (search_path chưa đối chiếu), A9 (`xlsx` CDN).

### 4.2 Rủi ro cấu trúc (quan trọng hơn lỗi lẻ)
1. **Không có cổng kiểm tra trước khi vào `main`.** `.github/workflows/gop-claude-vao-main.yml` chỉ *gộp nhánh*; không chạy `tsc`, `eslint`, `build` hay test. Nghĩa là code lỗi lint/type vẫn vào `main` (thực tế `tsc` đang sạch, nhưng không ai gác).
2. **Lịch sử migration không dựng lại được production.** 146 file trong `supabase/migrations/` nhưng `scripts/run-migrations.sh` chỉ liệt kê 53 file; hàm cũ hơn 9/2026 “không có trong repo” (ghi chính thức ở đầu `docs/DATABASE-RPC.md`). Không thể `supabase db reset` ra đúng schema đang chạy → mọi phân tích RLS/schema phải hỏi DB thật.
3. **Không có test tự động cho logic nghiệp vụ.** 6 file `scripts/tests/*.mjs` + 4 script `test:*` chạy tay; không có Vitest/Playwright, không chạy trong CI. RLS check bằng pglite có nhưng cũng chạy tay.
4. **Deploy tay từ Mac**, phụ thuộc cây làm việc sạch; đã có sự cố mất file vì `reset --hard`/`stash`. Không có môi trường staging.
5. **Không có giám sát lỗi runtime** (không Sentry/analytics); chỉ có bảng `bug_reports` do người dùng tự gửi. Lỗi JS trên máy học sinh hiện “vô hình”.
6. **Bus factor = 1.** Bù lại bằng tài liệu/memory rất tốt — đây là tài sản lớn nhất của dự án, nhưng cũng là chi phí token mỗi phiên (AGENTS 27 KB + STATE 14 KB).
7. **Không có chuẩn hoá Node/dependency**: không `.nvmrc`, không Dependabot/Renovate, `npm audit` không chạy định kỳ.

## 5. Cải tiến cấu trúc — theo thứ tự ưu tiên

### P0 — làm trong 1 tuần (rủi ro cao, công nhỏ)
| # | Việc | Vì sao | Công |
|---|---|---|---|
| 1 | RPC `submit_exam_result` tính điểm server-side | Bịt lỗ toàn vẹn điểm; giữ insert trực tiếp cho luyện tập | 1–2 ngày |
| 2 | `camera=(self)` trong `deploy.sh` + thử QR thật | Đang hỏng chức năng đã deploy | 15 phút |
| 3 | `dompurify` → dependencies, thêm `.env.example`, gỡ `@xmldom/xmldom` | Build/onboarding đúng | 15 phút |
| 4 | CI gate: `tsc --noEmit`, `eslint`, `next build`, `rls-pglite-check` trên push `main` + `claude/**` | Chặn hồi quy tự động; hiện chỉ gộp nhánh | 0,5 ngày |
| 5 | `supabase/baseline.sql` (dump schema hiện tại) + bảng `schema_migrations` thay mảng `FILES` | Dựng lại DB được, hết drift | 1 ngày |

### P1 — 2–4 tuần
6. **Đưa media ra khỏi git**: ảnh/mp3 lên Supabase Storage (bucket public + CDN) hoặc Git LFS; `content/` giữ markdown/bundle nguồn. Mục tiêu: repo < 100 MB. Kèm `git gc` và (tuỳ thầy) `filter-repo` để giảm lịch sử.
7. **Tổ chức lại `scripts/`**: `scripts/{db,content,ops,tests,archive}/`, mỗi script one-off đã chạy → `archive/`; tạo `scripts/lib/db.ts` + `env.ts` dùng chung (thay 36 bản `readEnvLocal`), `scripts/README.md` làm chỉ mục.
8. **Chốt một kiến trúc**: `features/<domain>/{api.ts,hooks/,components/,types.ts}`; rule lint cấm `components/**` import `@/services/supabase` trực tiếp (buộc qua `api.ts`). Chuyển dần 40 chỗ đang gọi Supabase trong component; **không di chuyển hàng loạt**, chỉ chuyển khi sửa file.
9. **Tách file lớn theo “đụng tới đâu sửa tới đó”**: bắt đầu `app/lop-hoc/bai/page.tsx` (hook dữ liệu / khung / từng tab), `QuestionBankAdmin`, `LessonsAdmin`.
10. **Sinh RLS vào `docs/DATABASE.md`**: thêm mục “bảng → RLS bật/tắt, policy, grant anon”; CI assert `pg_tables.rowsecurity = false` rỗng.

### P2 — quý
11. **Test**: Vitest cho `features/*`, `lib/*` (thuần, dễ test) + Playwright smoke 5 luồng (đăng nhập, làm bài, nộp, xem kết quả, phụ huynh). Chạy trong CI.
12. **Giám sát**: error boundary gửi `bug_reports` (đã có bảng) + uptime check; tuỳ chọn Sentry free.
13. **Dọn tài liệu**: chuyển `BAN-GIAO-*`, `prompt-*` vào `docs/archive/`; sinh `docs/INDEX.md`; giữ kỷ luật STATE.md (hiện còn lẫn việc đã xong trong mục “ĐANG CHỜ”).
14. **Chuẩn hoá toolchain**: `.nvmrc` + `engines`, Dependabot/Renovate, `npm audit` trong CI.

## 6. Cấu trúc đích gợi ý

```
app/                      # chỉ routing + layout, mỏng, không query DB
features/<domain>/        # lessons exams rank admin parent ...
  api.ts                  # mọi supabase.from/rpc của domain
  hooks/                  # use-*.ts (dữ liệu + trạng thái)
  components/             # UI riêng của domain
  types.ts
components/ui/            # design system thuần, không biết Supabase
lib/                      # hạ tầng: supabase, sanitize, format, env
supabase/
  baseline.sql            # schema hiện tại (nguồn sự thật để dựng lại)
  migrations/             # chỉ migration SAU baseline
  functions/
scripts/
  db/ content/ ops/ tests/ archive/
docs/
  INDEX.md  STATE.md  DATABASE.md (kèm RLS)
```

Nguyên tắc: **một chiều phụ thuộc** `app → features → lib`; `components/ui` không biết dữ liệu; `scripts` chỉ gọi API công khai hoặc SQL, không copy logic nghiệp vụ.

## 7. Lộ trình đề xuất

- **Đợt 1 (tuần này):** P0 #1–#5. Sau đợt này, mọi thay đổi đều có máy gác và DB dựng lại được từ git.
- **Đợt 2 (tháng này):** P1 #6–#8. Repo nhẹ, script gọn, ranh giới UI/dữ liệu rõ.
- **Đợt 3 (quý):** P1 #9–#10 + P2. Test, giám sát, tài liệu, toolchain.

Đo lại sau mỗi đợt bằng đúng §8: mục tiêu repo < 100 MB, 0 lint error, CI xanh, `run-migrations.sh --list` khớp 100% file đã chạy.

## 8. Phụ lục — số liệu và lệnh tái lập

```bash
git ls-files | wc -l                                   # 10.614 file
git ls-files -z | xargs -0 du -k | awk '{s+=$1} END {print s/1024" MB"}'   # 507 MB tracked
du -sh .git content public scripts                      # 1,2G · 353M · 79M · 435M (scripts gồm data/logs chưa tracked)
git ls-files '*.webp' | wc -l                           # 2.268 ảnh
git ls-files 'supabase/migrations/*.sql' | wc -l        # 146 migration
grep -c '^\s*"' scripts/run-migrations.sh               # 53 file trong FILES
npx tsc --noEmit                                        # 0 lỗi
npx eslint app components lib services features hooks   # 94 error / 20 warning
git grep -c 'supabase\.from(' -- 'components/**'        # 40 chỗ UI gọi thẳng
git grep -l 'readEnvLocal' -- 'scripts/**' | wc -l      # 36 bản copy
```

Tham chiếu chính: `perf/RLS_REPORT.md`, `docs/RA-SOAT-MA-NGUON-2026-10-17.md`,
`docs/DATABASE.md` (157 bảng), `docs/DATABASE-RPC.md` (372 hàm), `docs/STATE.md`.
