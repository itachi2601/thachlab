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

## Chi tiết migration (lý do máy Thạch, kiểm số thứ tự/đã chạy chưa, dọn câu trùng, RLS bảng mới)
- Chỉ chạy được trên Mac của Thạch (sandbox chặn `*.supabase.co`). Trước khi chạy: `bash scripts/run-migrations.sh --list`, đối chiếu TÊN file, kiểm `scripts/logs/` và STATE.md.
- Bảng mới trong `public` (kể cả bảng sao lưu) phải `enable row level security` + `revoke all from anon, authenticated` ngay trong file.
- Dọn câu trùng ngân hàng: quét ghép cặp trực tiếp, lặp tới khi sạch, mỗi đợt một bảng sao lưu tên khác.
- Đầy đủ: `docs/AGENTS-CHI-TIET.md` mục 1.

## Sau khi migration chạy xong
- Sinh lại sơ đồ bảng: `node scripts/gen-database-doc.mjs` (ghi `docs/DATABASE.md` + `DATABASE-RPC.md`),
  rồi chuyển mục vừa chạy từ "ĐANG CHỜ" trong `docs/STATE.md` sang `docs/STATE-archive.md`.
- Đối chiếu RPC: `npx tsx scripts/perf-compare-rpc.mts`
- Backfill mức độ câu hỏi — **GHI THẬT NGAY, không có dry-run**, tham số chỉ giới hạn số câu:
  `npx tsx scripts/backfill-question-bank-difficulty.mts 20` (thử nhỏ, xem lại UI rồi mới chạy hết)
<!-- END:thachlab-migrations -->

<!-- BEGIN:thachlab-perf-publish -->
# Đăng nội dung — luôn tối ưu tốc độ tải
- Ảnh đăng vào DB: nén trước, rộng ≤1200px, ≤150 KB; ảnh mới trong code → `.webp`; không nhúng base64 vào HTML lưu DB.
- Khối JS nặng mới ở trang HS: `next/dynamic({ssr:false})` + `LazyErrorBoundary`; KaTeX giữ đồng bộ ở trang HS.
- Không thêm round-trip Supabase cho `/`, `/lop-hoc/bai`, `/kiem-tra/lam` — dùng RPC gộp.
- Đầy đủ + checklist cuối đợt: `docs/AGENTS-CHI-TIET.md` mục 2.


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
- Tên model bị khai tử theo thời gian: mở tài liệu hiện hành trước khi viết/port; code cũ không phải nguồn tin.
- Edge Function không typecheck được → deploy xong phải bấm thử thật; deploy/secrets là việc của thầy.
- Script backfill phải nhớ id đã thử trong lượt chạy; `--dry-run` nhỏ + đối chiếu tay trước khi chạy thật.
- Trước khi viết lại file dùng chung: so với `git show HEAD:<file>`; `git diff` trước commit; file mới phải `git add`.
- Đầy đủ (gồm tool_choice DeepSeek): `docs/AGENTS-CHI-TIET.md` mục 3.

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

# Chạy lệnh dài/quan trọng — luôn để thầy theo dõi được (thầy chốt 6/10/2026)

Mọi phiên chạy trên Mac (có Terminal panel) phải theo một quy tắc, không tuỳ phiên:
- Lệnh chạy lâu (>30 giây), có tiến trình cần xem (build, deploy, migration, backfill, script đăng đề/bài, `npm run dev`) hoặc cần mạng/`.env.local`
  (Supabase CLI, `*.mts` ghi DB): **mở tab terminal bằng `ToolSearch select:mcp__terminal__run_in_terminal,mcp__terminal__read_terminal,mcp__terminal__open_terminal_tab`**
  rồi chạy ở đó, sau đó `read_terminal` để theo dõi và báo kết quả. Không giấu vào `Bash` nền.
- Lệnh ngắn, chỉ đọc (git status, grep, ls, tsc) vẫn dùng `Bash`.
- `Bash` bị sandbox chặn `*.supabase.co` — gặp 403 CONNECT thì chuyển sang tab terminal, đừng thử lại.
- Phiên cloud không có Terminal panel: in lệnh cho thầy chạy trên Mac, đừng giả vờ chạy được.
- Lệnh ghi production vẫn theo mục "Migration Supabase": agent không tự chạy.

# Quy tắc hình và chú thích trong bài học (thầy chốt 7/10/2026)

- Chú thích, ghi chú, đáp án, bảng ký hiệu có nhiều ý (kể cả trong bài lý thuyết và bài tập): **mỗi ý một dòng riêng**, không ghép nhiều ý vào một dòng bằng "·", ";" hay dấu phẩy. Ngoại lệ duy nhất: dòng 🔑 từ khoá 3–6 chữ.
- **Đường sức từ vẽ nét đứt; đầu mũi tên là hai vạch chéo lệch 30° so với đường chính, đầu nhọn** (helper `field_line`/`field_path`/`chevron` trong `.claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/svg_lib.py`; chi tiết ở `references/hinh-svg.md`). Hình cũ vẽ đường sức bằng `arrow()`/marker đặc thì sửa khi đụng tới bài.

# Rút kinh nghiệm về cách làm việc — MỌI phiên, không riêng nội dung (thầy chốt 7/10/2026)

Cuối mỗi phiên (trước khi báo xong / `/ban-giao`), thêm 1–3 gạch đầu dòng ngắn "Rút kinh nghiệm phiên" vào câu trả lời cuối, về hai mảng:
1. **Token**: việc nào đốt token vô ích (đọc cả file lớn thay vì grep/đọc đoạn, đọc ảnh ở phiên chính, dò schema thay vì `docs/DATABASE.md`, lặp tool call, báo tiến độ giữa chừng…), cách làm rẻ hơn lần sau. Nếu phiên đọc file nạp-mỗi-phiên (`AGENTS.md`, `MEMORY.md`, `STATE.md`) thấy phình thì rút gọn/chuyển bớt ngay.
2. **Đối thoại**: thầy chỉnh/khen cách trả lời nào (độ dài, giọng, mức hỏi lại, mức tự quyết) → ghi vào `docs/memory/user_thach_phong_cach_doi_thoai.md` (thêm mục, không viết lại), không chỉ nói miệng.
Không có gì mới thì ghi "không có bài học mới" — không bịa cho đủ. Bài học nhỏ, gộp vào mục có sẵn thay vì tạo file mới.

# Nhánh claude/* tự vào main (từ 8/10/2026)
Workflow `.github/workflows/gop-claude-vao-main.yml`: mỗi lần push nhánh `claude/*`, GitHub tự fast-forward hoặc merge sạch vào
`main`. Chỉ khi job báo đỏ (xung đột) mới cần merge tay trên Mac. Cuối phiên vẫn báo tên nhánh, nhưng không cần in lệnh merge
nếu job xanh — kiểm tại tab Actions. Trên Mac chỉ cần `git pull origin main`.
