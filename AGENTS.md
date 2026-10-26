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
| **Bảng màu nền sáng — mặc định toàn site từ 11/10/2026** (token, số đo tương phản, bảng quy đổi idiom nền tối → token, khác biệt theo nhóm tuổi, trang xem thử `/dev/giao-dien`) | `docs/MAU-NEN-SANG.md` |
| **Độ dài & nhịp bài lý thuyết** (hạn mức đo được, vì sao bài dài làm HS bỏ, cách kiểm chứng) | `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md` |
| **Thí nghiệm trong bài lý thuyết** viết theo cách đề TN THPT hỏi (khung 6 ô, T1–T12, checklist soát hộp `.tl-box--exp`) | `docs/QUY-TAC-THI-NGHIEM-TRONG-BAI.md` |
| Rút hộp có video, clip hiện tượng có phụ đề, SVG chuyển động (V8–V11; kế hoạch chặng 0–3, prompt, agent) | `docs/KE-HOACH-CLIP-ANH-DONG.md` |
| AI Tutor Socratic (GĐ 4, Q2–Q3/2027): quyết định kiến trúc không phụ thuộc model + eval offline `scripts/eval-ai-tutor.mts` | `docs/AI-TUTOR.md` |

Còn lại (`BRAND.md`, `UI.md`, `THONG-BAO.md`, `BAN-GIAO-*.md`, `prompt-toc-do-*.md`,
`prompt-toi-uu-font.md`, `rank-title-showcase-design.md`, `bai-viet-lo-trinh-*.md`) là log/prompt
lịch sử hoặc tài liệu chuyên biệt — grep theo từ khoá thay vì đọc hết khi cần tra.
<!-- END:thachlab-docs-index -->

<!-- BEGIN:thachlab-migrations -->
# Migration Supabase — quy tắc bắt buộc
- Schema/policy/hàm chỉ **viết thành file** `supabase/migrations/<timestamp>_*.sql` kèm rollback (cuối file hoặc `perf/rollback/*.down.sql`). Không `supabase db push`.
- Bảng mới trong `public` (kể cả bảng sao lưu): `enable row level security` + `revoke all from anon, authenticated` ngay trong file.
- Có file chờ chạy: nối vào mảng `FILES` của `scripts/run-migrations.sh`, ghi "ĐANG CHỜ" trong `docs/STATE.md`. Trên Mac: Claude chạy `bash scripts/run-migrations.sh --yes --only N` trong tab terminal rồi tự kiểm (xem mục "Có script thì chạy giúp"); phiên cloud in lệnh `cd /Users/MAC/Projects/thachlab && git pull origin main` + `bash scripts/run-migrations.sh`, kèm mỗi file làm gì / chạy ngoài giờ HS / rollback.
- Trước khi chạy: `--list`, đối chiếu TÊN file, kiểm `scripts/logs/` và STATE.md. Sau khi chạy: `node scripts/gen-database-doc.mjs`, chuyển mục sang `docs/STATE-archive.md`, đối chiếu RPC `npx tsx scripts/perf-compare-rpc.mts`.
- Đầy đủ (máy Thạch, merge cloud→main, stash khi pull, dọn câu trùng, backfill difficulty): `docs/AGENTS-CHI-TIET.md` mục 1 và mục 4.
<!-- END:thachlab-migrations -->

<!-- BEGIN:thachlab-perf-publish -->
# Đăng nội dung — luôn tối ưu tốc độ tải
- Ảnh đăng vào DB: nén trước, rộng ≤1200px, ≤150 KB; ảnh mới trong code → `.webp`; không nhúng base64 vào HTML lưu DB.
- Khối JS nặng mới ở trang HS: `next/dynamic({ssr:false})` + `LazyErrorBoundary`; KaTeX giữ đồng bộ ở trang HS.
- Không thêm round-trip Supabase cho `/`, `/lop-hoc/bai`, `/kiem-tra/lam` — dùng RPC gộp.
- Đầy đủ + checklist cuối đợt: `docs/AGENTS-CHI-TIET.md` mục 2.


# Đồng bộ giữa các phiên (cloud + Mac) — không giẫm chân nhau
- Đầu phiên: `git fetch origin && git merge origin/main` (không rebase nhánh đã push, không force-push); `/tinh-hinh`.
- Chỉ sửa file thuộc việc được giao. File dùng chung (`docs/STATE.md`, `docs/memory/MEMORY.md`, `scripts/run-migrations.sh`, `AGENTS.md`, `package.json`): chỉ thêm dòng/mục, không sắp xếp lại (trừ khi dọn theo hạn mức "Giữ file nạp-mỗi-phiên gọn").
- Commit theo đường dẫn cụ thể (`git commit -- <path>`), KHÔNG `git commit -a`/`git add .`; script ghi file nguồn → commit ngay; không dọn cây bằng `stash` + `reset`.
- Không xoá/reset/force-push nhánh hay worktree của phiên khác. Xung đột ý định → dừng, hỏi Thạch.
- Cuối phiên: commit, push nhánh `claude/*` (tự gộp vào main, xem mục dưới); không mở PR; job đỏ → báo "chưa vào main". Skill sửa → nhắc `bash ~/Projects/thachlab/scripts/cai-skill.sh`.
- Đầy đủ: `docs/AGENTS-CHI-TIET.md` mục 5.

# Cập nhật bài lý thuyết đã đăng
**Sửa lý thuyết bài đã đăng**: chỉ dùng `bash scripts/cap-nhat-ly-thuyet.sh <file> <lesson_id>` (chỉ ghi mục `ly_thuyet`, không dùng `upload-lesson.mts`). Chi tiết: mục "Cập nhật bài lý thuyết" trong `docs/AGENTS-CHUYEN-DE.md`.

# Thiết kế UI học sinh — đọc `docs/QUY-TAC-THIET-KE.md` trước, không chờ nhắc

Mọi UI học sinh nhìn thấy (`/lop-hoc/**`, `/kiem-tra/**`, trang chủ HS, xếp hạng, phụ đạo, thông báo) phải theo
`docs/QUY-TAC-THIET-KE.md` — quy tắc rút từ nghiên cứu tâm lý nhận thức & thị giác của học sinh 14–18 tuổi
(tải nhận thức, đa phương tiện Mayer, não vị thành niên, F-pattern, độ dài dòng, cực tính nền, đích chạm…).
Khi đề xuất hay sửa UI: **nêu mã quy tắc** (N1, C2, M5…), chạy checklist mục 8 (chụp 375px trước), và ghi mã vào
mô tả commit; cố ý phá quy tắc thì ghi lý do. Phụ lục A của file là bản rà trang bài học 2/10/2026 còn chờ sửa.

# Rút kinh nghiệm cuối phiên — bắt buộc với bài lý thuyết, đề thi, đề kiểm tra (thầy chốt 5/10/2026)
Phiên có soạn/sửa/đăng lý thuyết, đề, quiz, ngân hàng câu phải kết thúc bằng "Rút kinh nghiệm" (3–6 gạch, hoặc "không có bài học mới") và **ghi vào file**: skill tương ứng `.claude/skills/<tên>/SKILL.md` mục `## Nhật ký rút kinh nghiệm`; skill ngoài repo → `docs/memory/project_*.md`; quy tắc chung → AGENTS.md. Dạng `- YYYY-MM-DD · <sự cố> → <quy tắc>`. Đầy đủ: `docs/AGENTS-CHI-TIET.md` mục 6.

# Gọi AI provider trong code (DeepSeek/Anthropic) — đọc tài liệu hiện hành trước, test thật sau
- Tên model bị khai tử theo thời gian: mở tài liệu hiện hành trước khi viết/port; code cũ không phải nguồn tin.
- Edge Function không typecheck được → deploy xong phải bấm thử thật; deploy/secrets là việc của thầy.
- Script backfill phải nhớ id đã thử trong lượt chạy; `--dry-run` nhỏ + đối chiếu tay trước khi chạy thật.
- Trước khi viết lại file dùng chung: so với `git show HEAD:<file>`; `git diff` trước commit; file mới phải `git add`.
- Đầy đủ (gồm tool_choice DeepSeek): `docs/AGENTS-CHI-TIET.md` mục 3.

# Phân công mô hình (thầy chốt 6/10/2026)
- Subagent ghim model: `kien-truc-du-lieu` (opus: schema/RLS/migration/kiến trúc), `kiem-code` (sonnet: review diff, soát lý thuyết/UI), `chep-de` (sonnet: chép đề từ ảnh), `nhap-du-lieu-hoc-sinh` (haiku: mọi dữ liệu có tên HS). Soạn bài/quiz/UI HS: phiên chính.
- Việc ngoài Claude (OCR đề nhiều hình/PDF scan, lời giải hàng loạt, code thường không đụng schema, tin real-time X): KHÔNG tự làm, in hướng dẫn + prompt cho Thạch chạy trên Cursor rồi chờ.
- Dữ liệu định danh HS chỉ qua Claude. Model rẻ làm → `kiem-code` kiểm; lời giải model ngoài → Claude đối chiếu. Model trong app chọn bằng env/bảng cấu hình. Đầy đủ: `docs/AGENTS-CHI-TIET.md` mục 7.

# Chạy lệnh dài/quan trọng — luôn để thầy theo dõi được (thầy chốt 6/10/2026)

Mọi phiên chạy trên Mac (có Terminal panel) phải theo một quy tắc, không tuỳ phiên:
- Lệnh chạy lâu (>30 giây), có tiến trình cần xem (build, deploy, migration, backfill, script đăng đề/bài, `npm run dev`) hoặc cần mạng/`.env.local`
  (Supabase CLI, `*.mts` ghi DB): **mở tab terminal bằng `ToolSearch select:mcp__terminal__run_in_terminal,mcp__terminal__read_terminal,mcp__terminal__open_terminal_tab`**
  rồi chạy ở đó, sau đó `read_terminal` để theo dõi và báo kết quả. Không giấu vào `Bash` nền.
- Lệnh ngắn, chỉ đọc (git status, grep, ls, tsc) vẫn dùng `Bash`.
- `Bash` bị sandbox chặn `*.supabase.co` — gặp 403 CONNECT thì chuyển sang tab terminal, đừng thử lại.
- Phiên cloud không có Terminal panel: in lệnh cho thầy chạy trên Mac, đừng giả vờ chạy được.
- Lệnh ghi production vẫn theo mục "Migration Supabase": agent không tự chạy.

# Quy tắc hình và chú thích trong bài học
**Hình/chú thích bài học**: mỗi ý một dòng; đường sức từ nét đứt, mũi tên chevron 30°. Chi tiết: `docs/AGENTS-CHUYEN-DE.md`.

# Rút kinh nghiệm về cách làm việc — MỌI phiên, không riêng nội dung (thầy chốt 7/10/2026)

Cuối mỗi phiên (trước khi báo xong / `/ban-giao`), thêm 1–3 gạch đầu dòng ngắn "Rút kinh nghiệm phiên" vào câu trả lời cuối, về hai mảng:
1. **Token**: việc nào đốt token vô ích (đọc cả file lớn thay vì grep/đọc đoạn, đọc ảnh ở phiên chính, dò schema thay vì `docs/DATABASE.md`, lặp tool call, báo tiến độ giữa chừng…), cách làm rẻ hơn lần sau. Nếu phiên đọc file nạp-mỗi-phiên (`AGENTS.md`, `MEMORY.md`, `STATE.md`) thấy phình thì rút gọn/chuyển bớt ngay.
2. **Đối thoại**: thầy chỉnh/khen cách trả lời nào (độ dài, giọng, mức hỏi lại, mức tự quyết) → ghi vào `docs/memory/user_thach_phong_cach_doi_thoai.md` (thêm mục, không viết lại), không chỉ nói miệng.
Không có gì mới thì ghi "không có bài học mới" — không bịa cho đủ. Bài học nhỏ, gộp vào mục có sẵn thay vì tạo file mới.

# Nhánh claude/* tự vào main (từ 8/10/2026)
Workflow `.github/workflows/gop-claude-vao-main.yml`: mỗi lần push nhánh `claude/*`, GitHub tự fast-forward hoặc merge sạch vào
`main`. Chỉ khi job báo đỏ (xung đột) mới cần merge tay trên Mac. Cuối phiên vẫn báo tên nhánh, nhưng không cần in lệnh merge
nếu job xanh — kiểm tại tab Actions. Trên Mac chỉ cần `git pull origin main`.

# Nơi lưu nội dung bồi dưỡng HSG KHTN 9 – Vật lí
**Nội dung HSG KHTN 9 Vật lí** lưu gốc ở `/Users/MAC/Documents/THPT/Lop09/00_Dung_chung/HSG_KHTN9_Vat_li/` (đọc README ở đó). Chi tiết: `docs/AGENTS-CHUYEN-DE.md`.

# Trang mẫu chuẩn cho tài liệu/sách của thầy
**Tài liệu/sách in của thầy**: dàn trang bằng `_tools/trang-mau-sach/sach_mau.py` (luôn có số trang; `school=True` chỉ khi thầy yêu cầu). Chi tiết: `docs/AGENTS-CHUYEN-DE.md`.

# Link sâu vào trang cần đăng nhập
**Link sâu vào trang cần đăng nhập**: giữ `?next=` cả phần query, đừng truyền `loginHref` cứng; kiểm QR bằng giải mã lại (`scripts/kiem-qr.mts`). Chi tiết: `docs/AGENTS-CHUYEN-DE.md`.

# Giữ file nạp-mỗi-phiên gọn (thầy chốt 10/10/2026)
`docs/STATE.md` (<15 KB), `docs/memory/MEMORY.md` (<10 KB), `AGENTS.md` nạp mỗi phiên nên mỗi byte thừa là token mất ở MỌI phiên sau.
- Khi chốt phiên (`/ban-giao`, `/xong-viec`): mục nào trong STATE.md đã xong/đã chạy → chuyển **nguyên văn** sang `docs/STATE-archive.md`, STATE.md chỉ giữ hiện trạng + việc ĐANG CHỜ, mỗi việc 1–2 dòng (chi tiết để ở `docs/memory/project_*.md`).
- MEMORY.md: mỗi file memory đúng MỘT dòng, một câu hook; không dán lại tóm tắt nhiều câu; không lặp file đã có; việc xong → chuyển dòng sang `docs/memory/ARCHIVE.md`.
- Thấy hai file trên vượt hạn mức thì dọn ngay trước khi làm tiếp (không cần hỏi).

# Có script thì chạy giúp và kiểm tra (thầy chốt 11/10/2026)
Việc cần chạy script/migration (`scripts/run-migrations.sh --yes --only N`, `*.mts`): Claude chạy trong tab terminal rồi tự kiểm kết quả (log, truy vấn lại), không chỉ in lệnh. Dry-run trước; không `db push`; việc không hoàn tác được vẫn hỏi lại. Điều này thay cho câu "agent không tự chạy migration" ở mục trên.

# Mọi quyết định đổi/thêm tính năng: tư vấn theo nghiên cứu giáo dục & tâm lý lứa tuổi TRƯỚC khi làm (thầy chốt 11/10/2026)
Khi thầy ra quyết định thay đổi hoặc bổ sung tính năng trên thachlab, bước đầu tiên là **tư vấn ngắn** (3–6 dòng), rồi mới làm:
1. **Dựa vào nghiên cứu đã có trong repo, KHÔNG tìm lại tài liệu**: `docs/DE-XUAT-NGHIEN-CUU-HS-14-22-2026-10-11.md` (CLT/Mayer, Gloria Mark, Dahl–Steinberg, Ryan–Deci/SDT, Deterding + Sailer & Homner; có chỗ "tóm tắt nói quá"), `docs/QUY-TAC-THIET-KE.md` (G1–G3, N/C/M/B/H/V/D/L), `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md`, `docs/NGHIEN-CUU-PHU-HUYNH-45-60.md` + `docs/QUY-TAC-THIET-KE-PHU-HUYNH.md` (phụ huynh), `docs/mastery-rules.md`. Chỉ lên mạng khi các file đó không phủ chủ đề, và nói rõ.
2. **Nêu**: (a) nghiên cứu/mã quy tắc nào liên quan, (b) quyết định của thầy hợp hay đi ngược chỗ nào (đặc biệt rủi ro đã ghi: thưởng hữu hình làm giảm động lực nội tại, tải nhận thức, nhạy địa vị bạn cùng lứa tuổi 14–18, ngưỡng bỏ cuộc), (c) cách làm đề xuất / điều chỉnh nhỏ nếu cần, (d) cách đo hiệu quả nếu đáng đo.
3. **Thầy vẫn là người quyết**: tư vấn xong thì làm theo ý thầy, trừ khi vi phạm nặng — khi đó nói rõ rồi hỏi một lần. Không lặp lại tư vấn khi thầy đã nghe và giữ nguyên quyết định.
4. Ghi mã quy tắc/nghiên cứu vào mô tả commit. Phạm vi: tính năng nhìn thấy bởi HS/phụ huynh hoặc ảnh hưởng cách học; sửa lỗi, hạ tầng, script nội bộ không cần.

# Nhãn câu hỏi phải y như đề thi thật (thầy chốt 11/10/2026)
Mọi chỗ HS làm/xem câu hỏi (kiểm tra, luyện tập, thăng hạng, xem thử trang chủ): Phần I **A. B. C. D.**, Phần II **a) b) c) d)** + Đúng/Sai, Phần III ô đáp số. Làm UI/đăng đề có câu hỏi thì soát theo `docs/QUY-TAC-THIET-KE.md` mục E1–E3. Đã rà 11/10: chỉ `ExamSamplePreview` thiếu a)–d), đã sửa.

# Bản quyền khi soạn bài và tìm tài nguyên
**Bản quyền** (`/dieu-khoan`): không chép nguyên văn SGK; ghi nguồn đề trích; tài nguyên ngoài chỉ giấy phép mở và ghi tác giả; không rõ giấy phép = không dùng. Chi tiết: `docs/AGENTS-CHUYEN-DE.md`.

# Chất lượng đề & câu hỏi khi nạp vào web
**Chất lượng đề/câu hỏi khi nạp**: nhãn như đề thật, đúng một đáp án, hình rõ ≤150 KB, dò 2 lần (máy + mắt, agent `kiem-code`) trước khi bật Hiện; sửa hàng loạt phải dry-run → sao lưu → kiểm lại bản đã ghi. Chi tiết: `docs/AGENTS-CHUYEN-DE.md`.

# Sửa hàng loạt ký hiệu trong ngân hàng câu
**Sửa hàng loạt ký hiệu ngân hàng câu** (S1→$S_1$): dry-run, `kiem-code` chạy KaTeX, `EXCLUDE_IDS`. Chi tiết: `docs/AGENTS-CHUYEN-DE.md`.

# Rà UI bằng tài khoản đăng nhập sẵn trong trình duyệt
**Rà UI bằng tài khoản đang đăng nhập**: xác định tài khoản/lớp/role trước khi kết luận "trống" (RLS); prettier dùng `--print-width 120`. Chi tiết: `docs/AGENTS-CHUYEN-DE.md`.

# Rà lỗi hàng loạt ngân hàng câu hỏi: ca chắc thì sửa, ca nghi ngờ đưa thầy duyệt bằng HTML
**Rà lỗi hàng loạt ngân hàng câu**: ca chắc sửa bằng script (dry-run → `--apply`), ca nghi ngờ đưa thầy duyệt qua `lap-duyet-html.mts`. Chi tiết: `docs/AGENTS-CHUYEN-DE.md`.

# Lệnh chạy trên hosting — không bao giờ đưa dạng khối bash trần (sự cố 17/10/2026)
Lệnh cron hosting `git fetch && git reset --hard origin/deploy && git clean -fdx` đã bị chạy nhầm trong repo trên Mac: xoá `.env.local`,
memory `feedback_*`/`user_*`, script chưa commit, `scripts/logs/` (sao lưu DB), `node_modules`. Không có Time Machine; phải dựng lại từ transcript Claude.
- Lệnh phá huỷ (`reset --hard`, `clean -fdx`, `rm -rf`) dành cho máy khác: chỉ mô tả bằng lời hoặc kèm `cd <đường dẫn trên máy đó> &&` + cảnh báo "KHÔNG chạy trên Mac"; không đặt trong khối ```bash``` (app có nút Run).
- Commit sớm, kể cả ghi chú/memory; file chỉ có ở Mac (`.env.local`, `feedback_*`) nên có bản sao ngoài repo.

# Lời giải trắc nghiệm trong ngân hàng
**Lời giải trắc nghiệm**: theo `docs/QUY-TAC-LOI-GIAI.md`; ghi hàng loạt chỉ vào `question_bank`.

# Sửa hàng loạt câu trong đề/ngân hàng
**Sửa hàng loạt câu trong đề/ngân hàng**: luôn qua SQL giao dịch (tắt `trg_exams_sync_bank`, sao lưu, đếm dòng trước/sau). Chi tiết: `docs/AGENTS-CHUYEN-DE.md`.

# Script ghi hàng loạt vào DB chỉ chạy sau 22h (sự cố 23/10/2026: Supabase cạn Disk IO budget)
Script/migration ghi hoặc quét hàng chục nghìn dòng (`question_bank`, `exams.questions`, quét trùng `question_bank_plain_text`, backfill) ăn hết ngân sách IO burst của gói compute, cả ngày sau đó DB chậm cho học sinh. Chỉ chạy sau 22h hoặc trước 6h; chia mẻ ≤2.000 dòng, nghỉ giữa mẻ; ghi giờ chạy vào STATE.md. Tra nhanh khi nghi DB chậm: `pg_stat_statements` sắp theo `shared_blks_read` và `wal_bytes` (file mẫu: memory `project_thachlab_hosting`).
