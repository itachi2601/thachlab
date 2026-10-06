<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

<!-- BEGIN:thachlab-docs-index -->
# Tài liệu — đọc khi cần, đừng đọc hết docs/

**Memory dự án nằm trong git: `docs/memory/`** (chỉ mục `docs/memory/MEMORY.md`; trên Mac là symlink của thư mục memory Claude Code). Phiên trên cloud không tự nạp — đọc `MEMORY.md` khi bắt đầu đợt việc lớn, rồi chỉ mở đúng file `project_*.md` liên quan (`ARCHIVE.md` chỉ grep). Cuối phiên ghi lại bằng `/ban-giao`. File `feedback_*`/`user_*` giữ riêng ở Mac (gitignore) nên cloud có thể không thấy — dòng trỏ tới chúng trong `MEMORY.md` cứ bỏ qua.

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
| Skill Claude còn thiếu (bản đồ quy trình, đề xuất chờ duyệt) | `docs/DE-XUAT-SKILL-2026-09-29.md` |
| **Mọi UI học sinh nhìn thấy** (quy tắc thiết kế có dẫn nghiên cứu tâm lý/thị giác, checklist) | `docs/QUY-TAC-THIET-KE.md` |
| **Mọi UI phụ huynh nhìn thấy** (`/phu-huynh`, dải phụ huynh ở trang chủ, `/loi-moi`, footer — bộ quy tắc P1..P21 cho tuổi 45–60, checklist) | `docs/QUY-TAC-THIET-KE-PHU-HUYNH.md` |
| Nghiên cứu nền cho UI phụ huynh (thị giác/nhận thức/tâm lý tuổi 45–60, 26 nguồn có nhãn bằng chứng) | `docs/NGHIEN-CUU-PHU-HUYNH-45-60.md` |
| **Độ dài & nhịp bài lý thuyết** (hạn mức đo được, vì sao bài dài làm HS bỏ, cách kiểm chứng) | `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md` |
| AI Tutor Socratic (GĐ 4, Q2–Q3/2027): quyết định kiến trúc không phụ thuộc model + eval offline `scripts/eval-ai-tutor.mts` | `docs/AI-TUTOR.md` |

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

## Script/migration viết trên cloud phải VÀO `main` trước khi giao lệnh cho Thạch
Mac của Thạch chỉ chạy được file có trong `main` (thường còn thay đổi chưa commit nên không checkout nhánh khác được).
Khi giao lệnh chạy (`run-migrations.sh`, file `.sql`, script `.mts`):
1. Đảm bảo file đã nằm trong `main` — cloud chỉ đẩy nhánh `claude/...`, nên in lệnh để Thạch merge nhánh vào `main` trên Mac (`git fetch origin && git merge origin/claude/<tên>`) rồi mới chạy. Không mở PR (repo chỉ có một người làm).
2. Lệnh đầu tiên luôn là `cd /Users/MAC/Projects/thachlab && git pull origin main`.
3. Nếu Mac báo "local changes would be overwritten": KHÔNG bảo bỏ thay đổi; hướng dẫn `git stash` → `git pull origin main` → `git stash pop`, hoặc `git diff --stat <file>` để xem trước.
4. Sau khi merge, kiểm lại `FILES` trong `scripts/run-migrations.sh` (bản trên `main`) khớp danh sách đang chờ.

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

# Đồng bộ giữa các phiên (cloud + Mac) — không giẫm chân nhau

Mỗi phiên cloud chạy trên nhánh `claude/<tên>` riêng, tách từ `main` lúc mở. Chỉ thứ đã **commit và vào `main`** mới tới
được phiên khác và máy Thạch. Việc nằm trên nhánh mà chưa merge coi như chưa tồn tại với phần còn lại.

## Đầu phiên
- `git fetch origin` rồi `git merge origin/main` vào nhánh phiên (không rebase nhánh đã push, không force-push).
- Chạy `/tinh-hinh`; xem `git branch -r --sort=-committerdate | head` để biết phiên khác đang đụng tới đâu.

## Trong phiên — giữ đúng phạm vi
- Chỉ sửa file thuộc việc được giao. Không "tiện tay" dọn/đổi tên/format file ngoài phạm vi.
- File dùng chung (`docs/STATE.md`, `docs/memory/MEMORY.md`, `scripts/run-migrations.sh`, `AGENTS.md`, `package.json`): chỉ
  **thêm dòng/mục mới**, không viết lại hay sắp xếp lại phần có sẵn — để hai phiên cùng thêm vẫn merge sạch.
- Migration: tên file theo timestamp, không sửa/xoá migration của phiên khác; chỉ nối thêm vào mảng `FILES`.
- Không xoá, reset, force-push nhánh hay worktree của phiên khác. Thấy lạ thì ghi vào `STATE.md`, đừng tự dọn.
- Skill mới/sửa: chỉ ở `.claude/skills/<tên>/` trong repo (nguồn duy nhất). Không chép tay sang `~/.codex`, Library plugin.

## Cuối phiên — việc "xong" nghĩa là đã tới `main`
1. Commit đúng file của mình (`git commit -- <path>`), push nhánh.
2. KHÔNG mở PR (repo chỉ có Thạch làm). Báo ngắn: nhánh nào, đổi gì, file chung nào đã đụng, rồi in lệnh để Thạch merge trên Mac: `git -C ~/Projects/thachlab fetch origin && git -C ~/Projects/thachlab merge origin/claude/<tên>`. Phiên chạy trên Mac thì commit thẳng `main`.
3. Phiên cloud không merge được thì **báo rõ "chưa vào main, cần merge nhánh claude/…"** — không báo "xong".
4. Có skill mới/sửa → in kèm lệnh cho Thạch trên Mac, sau khi nhánh đã merge:
```
git -C ~/Projects/thachlab pull && bash ~/Projects/thachlab/scripts/cai-skill.sh
```
5. Có migration → theo mục "Migration Supabase" ở trên. Ghi mục "ĐANG CHỜ" trong `docs/STATE.md`, rồi `/ban-giao`.

## Xung đột
Hai phiên cùng sửa một file riêng (không phải file dùng chung) → phiên merge sau tự gộp và kiểm lại; nếu ý định mâu thuẫn
thì dừng, hỏi Thạch, không ghi đè bản của phiên kia.

# Cập nhật bài lý thuyết đã đăng — chỉ đẩy phần lý thuyết

Sửa/đăng lại nội dung lý thuyết của bài có sẵn: dùng `bash scripts/cap-nhat-ly-thuyet.sh <theory.html|bundle.json> <lesson_id>`
(chỉ ghi cột `body_html` của mục `ly_thuyet`, tự sao lưu ra `scripts/logs/`; hoàn tác bằng `scripts/khoi-phuc-ly-thuyet.mts`).
Không dùng `upload-lesson.mts` cho việc này — nó tạo/ghi cả đề Luyện tập. Công thức có `<`/`>` trong `$…$` phải viết `\lt`/`\gt`.

**Quy tắc (thầy chốt 4/10/2026): đăng lý thuyết chỉ ghi đúng mục Lý thuyết của bài đó, không làm ảnh hưởng
phần còn lại** (Luyện tập, Kiểm tra, Bài tập mẫu, tiêu đề, tiến độ học) hay bài khác. Script đã thực thi quy tắc
này, không dựa vào việc người chạy nhớ: dry-run in rõ phạm vi (mục nào ghi, mục nào bỏ qua), UPDATE ràng buộc cả
`id` lẫn `kind='ly_thuyet'` và đòi đúng 1 dòng, rồi chụp toàn bộ `lesson_items` của bài TRƯỚC/SAU để đối chiếu —
lệch là exit 1 kèm lệnh hoàn tác. Sửa script thì giữ nguyên phần kiểm này, đừng gỡ.

# Thiết kế UI học sinh — đọc `docs/QUY-TAC-THIET-KE.md` trước, không chờ nhắc

Mọi UI học sinh nhìn thấy (`/lop-hoc/**`, `/kiem-tra/**`, trang chủ HS, xếp hạng, phụ đạo, thông báo) phải theo
`docs/QUY-TAC-THIET-KE.md` — quy tắc rút từ nghiên cứu tâm lý nhận thức & thị giác của học sinh 14–18 tuổi
(tải nhận thức, đa phương tiện Mayer, não vị thành niên, F-pattern, độ dài dòng, cực tính nền, đích chạm…).
Khi đề xuất hay sửa UI: **nêu mã quy tắc** (N1, C2, M5…), chạy checklist mục 8 (chụp 375px trước), và ghi mã vào
mô tả commit; cố ý phá quy tắc thì ghi lý do. Phụ lục A của file là bản rà trang bài học 2/10/2026 còn chờ sửa.

# Rút kinh nghiệm cuối phiên — bắt buộc với bài lý thuyết, đề thi, đề kiểm tra (thầy chốt 5/10/2026)

Mọi phiên có làm bài học lý thuyết, đề thi, đề kiểm tra, quiz, ngân hàng câu hỏi (soạn, sửa, lọc, đăng) **phải kết thúc bằng
phần "Rút kinh nghiệm"** — không có thì chưa tính là xong phiên. Làm trước khi báo hoàn thành / chạy `/ban-giao`:

1. **Viết ngắn trong câu trả lời cuối** (3–6 gạch đầu dòng, mỗi dòng một bài học cụ thể): lỗi đã gặp + nguyên nhân thật,
   cách phát hiện, cách làm đúng lần sau, việc gì tốn token/thời gian vô ích. Không có gì mới thì ghi rõ "không có bài học mới".
2. **Ghi vào đúng nơi, không chỉ nói miệng**:
   - Bài học gắn với một quy trình → mục `## Nhật ký rút kinh nghiệm` ở cuối skill tương ứng trong `.claude/skills/<tên>/SKILL.md`
     (`soan-bai-ly-thuyet-tuong-tac`, `soan-quiz-ly-thuyet`, `up-de-kiem-tra`, `dang-de-hang-loat`). Skill nằm ngoài repo
     (`azota`, `ngan-hang-cau-hoi`, `dang-bai-hoc-thachlab`, `latex`) → ghi vào file `project_*.md` liên quan trong `docs/memory/`
     và nhắc thầy cập nhật skill đó.
   - Bài học áp cho mọi phiên/mọi skill → thêm quy tắc ngắn vào `AGENTS.md` (chỉ thêm, không viết lại phần có sẵn).
3. **Dạng mỗi mục**: `- YYYY-MM-DD · <sự cố/phát hiện> → <quy tắc làm đúng>`. Sửa ngay bước trong skill nếu bước đó sai, đừng chỉ
   chất thêm ghi chú. Mục trùng ý đã có thì gộp, không lặp.
4. Báo trong câu trả lời cuối: đã ghi vào file nào.

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

# Phân công mô hình (thầy chốt 6/10/2026) — Claude làm việc của Claude, việc khác gợi ý Cursor

Hai nhánh, không trộn:

**Nhánh Claude — giao subagent trong `.claude/agents/`, mỗi agent đã ghim model:**

| Việc | Agent | Model |
|---|---|---|
| Schema, RLS, migration, YCCĐ–danh hiệu–phụ đạo, backup, đổi vùng, dependency lớn | `kien-truc-du-lieu` | opus |
| Review diff trước commit/merge; soát nội dung lý thuyết sắp đăng; soát UI | `kiem-code` | sonnet |
| Chép đề từ ảnh trang đã render (thay cho `general-purpose`) | `chep-de` | sonnet |
| Import roster, điểm danh Zalo, bảng điểm, học phí — mọi dữ liệu có tên học sinh | `nhap-du-lieu-hoc-sinh` | haiku |
| Soạn bài lý thuyết, quiz, tin tức, AI tutor giải đủ, UI học sinh | phiên chính (sonnet/opus) | — |

**Nhánh ngoài Claude — KHÔNG tự làm, KHÔNG viết router gọi API ngoài. Dừng lại, in hướng dẫn cho Thạch làm trên Cursor
(chế độ Auto, Cursor tự chọn model), kèm prompt mẫu và tên file kết quả cần nộp lại, rồi chờ:**
- OCR đề thi nhiều hình vẽ / công thức MathType dạng ảnh, PDF scan dày (Gemini Flash làm tốt và rẻ hơn).
- Sinh lời giải chi tiết hàng loạt cho ngân hàng câu (Gemini/DeepSeek), sau đó quay lại Claude đối chiếu đáp án.
- Code thường không đụng schema/RLS: bugfix, refactor component, script một lần.
- Tin tức/xu hướng cần dữ liệu thời gian thực từ X (Grok).

**Ranh giới không đổi:**
- Dữ liệu định danh học sinh (tên, điểm, phụ huynh, SĐT) chỉ đi qua Claude — không đưa vào prompt gửi Cursor/DeepSeek/Gemini.
- Model rẻ làm → `kiem-code` kiểm trước khi merge. Lời giải do model ngoài sinh → Claude đối chiếu đáp án trước khi đăng.
- Model chạy TRONG app (Edge Function `classify-questions`, `ai-tutor`) chọn bằng env/bảng cấu hình, không hard-code tên model (xem mục "Gọi AI provider trong code").
