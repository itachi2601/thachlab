# Phản biện báo cáo rà soát 22/10/2026 — đối chiếu lại bằng lệnh thật

Đối chiếu `docs/RA-SOAT-DU-AN-2026-10-22.md` trên nhánh `claude/busy-noether-y0efeg` (= `main@8a14e4894`), cùng ngày.
Kết luận chung: **số liệu đo lại khớp ~95 %**, hai lỗ bảo mật là thật, nhưng có **1 khẳng định sai**, **1 lỗ bị bỏ sót nặng hơn
lỗ #1**, và vài chỗ điểm/ưu tiên cần chỉnh.

## 1. Khớp (đã chạy lại)

| Khẳng định | Đo lại | Kết quả |
|---|---|---|
| 10.614 file tracked, 507 MB | 10.615 · 506,7 MB | khớp |
| 146 migration / 53 trong `FILES` | 146 / 53 | khớp |
| `tsc --noEmit` 0 lỗi | exit 0 | khớp |
| ESLint 94 error / 20 warning; 77 `set-state-in-effect`, 7 `preserve-manual-memoization`, 4 `refs` | 94/20; 77/7/4 (+2 purity, 2 immutability, 2 no-unescaped-entities), **52 file** | khớp |
| `components/**` gọi `supabase.from(` 40 chỗ | 40 (143 nếu đếm mọi `.from(`) | khớp |
| 36 bản copy `readEnvLocal` | 36 file, 36 định nghĩa riêng | khớp |
| `dompurify` ở devDependencies, import trong `lib/sanitize-html-client.ts` | đúng | khớp |
| Không có `.env.example`, README dòng 9 vẫn trỏ tới | đúng | khớp |
| Không `.nvmrc`/`engines`; `xlsx` cài từ `cdn.sheetjs.com` | đúng | khớp |
| CI chỉ gộp nhánh | `gop-claude-vao-main.yml` không có bước tsc/lint/build | khớp |
| 157 bảng (AGENTS.md ghi 99) | cộng tiêu đề mục DATABASE.md = 157 | khớp |
| 4 file > 1.100 dòng | 2.348 / 1.430 / 1.306 / 1.070 | khớp |
| `Permissions-Policy: camera=()` vs `getUserMedia` trong `QrScannerCard` | `deploy.sh:59` · `QrScannerCard.tsx:77` | khớp — `camera=()` là allowlist rỗng, chặn cả same-origin |
| Điểm tính ở client rồi insert | `ExamRunner.tsx:206` `gradeExam` → `:224` `insert` ; policy insert chỉ ràng `student_id`, `exam_open_to_student` | khớp |
| HS không sửa/xoá được kết quả sau đó | không có policy update/delete cho `authenticated` trên `exam_results` | khớp |

Không kiểm được trên cloud: `.git` 1,2 GB (ở đây clone 401 MB), `pg_proc.proconfig`, dashboard Supabase.

## 2. Sai hoặc thiếu

### 2.1 SAI: `@xmldom/xmldom` không phải dependency chết
Báo cáo: "không file nào import". Thực tế 3 script dùng: `scripts/classify-exam-folder.mts`, `scripts/fix-formula-images.mts`,
`scripts/upload-exam-docx.mts`. Chỉ app không import. **Không gỡ** khỏi `package.json`; nếu muốn tách thì chuyển sang
`devDependencies` (script chạy bằng `npx tsx`, không vào bundle). Mục P0 #3 cần sửa lại câu này.

### 2.2 BỎ SÓT (nặng hơn lỗ #1): đáp án đúng được gửi nguyên về trình duyệt
`app/kiem-tra/lam/page.tsx:55` select cột `questions` (jsonb) của `exams` — trong đó có khoá đáp án, vì `gradeExam`
(`features/exams/types.ts:242`) chấm được ngay tại client. Nghĩa là HS không cần giả điểm: mở Network tab là **đọc được đáp án
trước khi làm**. RPC `submit_exam_result` tính điểm server-side (P0 #1) **không bịt được lỗ này**. Phạm vi đúng của P0 #1 phải là
hai việc đi cùng nhau:
1. RPC/view trả đề **đã lược khoá đáp án** cho vai học sinh (giữ nguyên cho staff và cho đề luyện tập có bật "hiện đáp án").
2. RPC `submit_exam_result(exam_id, responses, client_token, duration, violations)` chấm từ `exams.questions` phía server, ghi
   `exam_results` + `exam_question_results`; thu hồi policy insert trực tiếp của HS cho đề tính điểm.
Công ước lượng tăng từ 1–2 ngày lên 2–3 ngày; `gradeQuestion` đang là TS nên cần port sang plpgsql (hoặc Edge Function dùng
lại đúng file `features/exams/types.ts`). Chọn Edge Function sẽ tránh viết lại logic chấm hai lần.

### 2.3 Thiếu bằng chứng: "215 chỗ security definer, 91 file nhắc search_path"
Đếm lại: 246 lần `security definer` trong 87 file; 91 file có `search_path`. Hai số đếm khác đơn vị (lần vs file) nên câu
"215 nhưng chỉ 91" không nói lên gì. Giữ đúng kết luận gốc: **chưa xác minh trên DB thật**, cần 1 truy vấn `pg_proc.proconfig`
trên Mac rồi mới xếp mức.

### 2.4 Điểm "Tinh gọn 5,5" trộn hai thứ khác bản chất
Repo nặng vì `content/` (356 MB ảnh/mp3 là **học liệu**, không phải code). Trừ điểm code vì học liệu nằm chung repo là
đúng về vận hành, nhưng phần "Code gọn" đáng 8/10; nên tách thành hai dòng để quyết định P1 #6 (đưa media ra Storage) không bị
hiểu là "code bẩn".

### 2.5 CI gate (P0 #4) — cảnh báo thực thi
`npm run lint` đang đỏ 94 lỗi → bật gate `eslint` ngay sẽ **chặn mọi nhánh claude/\*** vào `main` cho tới khi dọn xong. Thứ tự
đúng: dọn lint trước (mục 3 dưới đây), rồi bật gate với `--max-warnings` lỏng, siết dần. `tsc` và `next build` bật được ngay.

### 2.6 Lộ trình: P0 #5 (`baseline.sql`) không làm được trên cloud
Cần `pg_dump --schema-only` từ production — việc của Mac. Nên ghi rõ "Mac" để phiên cloud không nhận nhầm.

## 3. Phần giao DeepSeek (theo phân công AGENTS.md: code thường, không đụng schema/RLS)

Trong báo cáo, việc hợp DeepSeek nhất là **dọn 94 lỗi ESLint trong 52 file** — lặp, có máy kiểm (eslint + tsc), không chạm dữ
liệu học sinh, không đụng RLS. Đã viết `scripts/deepseek-sua-lint.mts` (+ `scripts/lib/env.mts` dùng chung, bắt đầu gom 36 bản
`readEnvLocal`):
- Gửi từng file + danh sách lỗi, yêu cầu sửa tối thiểu theo đúng mẫu React 19 cho từng rule; trả JSON.
- Hàng rào máy: từ chối nếu file ngắn/dài bất thường, thêm `eslint-disable`/`as any`, đổi export, import module mới; chạy lại
  eslint cho file; cuối lượt `tsc --noEmit`; đỏ → `git checkout` hoàn tác. File > 900 dòng bỏ qua (Claude tách trước).
- Dry-run mặc định (đề xuất + diff ghi vào `scripts/logs/deepseek-lint/`), `--apply` mới ghi cây làm việc; nhớ file đã thử.
- Sau `--apply`: agent `kiem-code` soát `git diff` (nhất là `set-state-in-effect` — sửa sai làm mất đồng bộ state), rồi commit
  theo đường dẫn.

**Không giao DeepSeek**: tách 4 file lớn (cần hiểu luồng dữ liệu), RPC chấm điểm (schema/RLS → `kien-truc-du-lieu`), đổi
`Permissions-Policy` (1 dòng, Claude sửa thẳng), CI workflow.

Chạy trên Mac (cloud chặn `api.deepseek.com`):
```
cd /Users/MAC/Projects/thachlab && git pull origin main
npx tsx scripts/deepseek-sua-lint.mts --limit 3            # dry-run, xem scripts/logs/deepseek-lint/<mốc>/TONG-KET.md
npx tsx scripts/deepseek-sua-lint.mts --limit 15 --apply   # ghi thật; rồi gọi kiem-code soát git diff trước khi commit
```

## 4. Điểm tổng sau phản biện
Giữ 6,4/10 nhưng **Bảo mật hạ 7,5 → 7,0** (thêm lỗ lộ đáp án), **Tinh gọn tách thành Code 8 / Repo 4**. Ưu tiên P0 #1 giữ
nguyên vị trí đầu, mở rộng phạm vi như 2.2.

## 5. Nhật ký lượt chạy DeepSeek
- 2026-10-22 · Lượt 1 (`--limit 15 --apply`, nhánh `deepseek/lint-1`): 14/15 file sạch eslint, 1 file tsc đỏ tự hoàn tác, 1 file
  298 dòng bị cắt phản hồi (đặt `DEEPSEEK_MAX_TOKENS=32000`). `kiem-code` soát: 13 đạt, 1 đổi hành vi thật
  (`TeacherChecklistPanel` mất reset danh sách khi không chọn phiên) → Claude sửa bằng mẫu state gắn khoá. Hai file rườm rà
  (`CncMillingLiveMonitor`, `HsgGradingAdmin`) giữ nguyên. Chi phí ~160k token DeepSeek cho 14 file.
  → Quy tắc: model rẻ hay "bỏ nhánh reset" để qua lint; prompt lượt sau đã nhấn mạnh giữ mọi nhánh `setState([])`/`null`.
- 2026-10-22 · Lượt 2 (`--limit 20 --apply`): chạy trên cây chưa `git pull` nên làm lại 14 file đã soát → bỏ, giữ 6 file mới
  (nhánh `deepseek/lint-2`). Soát: 4 đạt; `PhysicsPostRibbon` cập nhật cache cả khi `setItem` lỗi (lệch với localStorage) →
  `return` trong catch; `Hsg9WeekCard` tính ngày/giờ trong `useState` làm mất chống lệch hydrate → `useSyncExternalStore` với
  server snapshot null. Script thêm bước dừng khi cây tụt sau `origin/main`. Lint toàn repo còn 74 lỗi / 32 file.
- 2026-10-22 · Lượt 3 (`--limit 20 --apply`, nhánh `deepseek/lint-3`, 40 lỗi/20 file, ~260k token): 2 agent `kiem-code` soát song
  song → 19 đạt, 1 sửa nhẹ (`TeacherThptDashboard`: effect đếm "chưa làm bài" thêm dep `selectedClassId` nên chạy với students
  lớp cũ khi vừa đổi lớp → gắn kết quả với tham chiếu `students`, dep chỉ `[students]`). Góp ý không chặn: `lo-trinh-hsg` cache
  tick cấp module chỉ nạp lại khi đổi key; `AdminShell` drawer nhớ trạng thái theo path. Lint còn 34 lỗi / 12 file, trong đó
  5 file > 900 dòng (LessonsAdmin, QuestionBankAdmin, CncCourseWorkspace, `lop-hoc/bai`, `lop-hoc`) cần Claude tách trước.
