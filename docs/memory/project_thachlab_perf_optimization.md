---
name: project_thachlab_perf_optimization
description: "Đợt tối ưu tốc độ tải ThachLab 25-27/9/2026 (5 đợt) — đã merge+deploy xong; đợt 4 có sự cố crash-trắng do next/dynamic thiếu error boundary; đợt 5 (27/9) thêm ChunkErrorGuard window-level + tách SampleQuestionsGrid (chưa đạt <1000KB) + test luồng làm bài thật lần đầu — đã merge+push+deploy"
metadata:
  node_type: memory
  type: project
  originSessionId: 7f96de41-ea91-4412-b70a-8b68d2d82f5c
  modified: 2026-09-27T12:45:56.572Z
---

Đợt tối ưu tốc độ theo prompt điều phối của thầy, làm ngày 25/9/2026 (Pha 0 khảo sát → Pha 1 assets/db-index/bundle → Pha 2 queries-hs/rpc-gv → Pha 3 static-content → agent G kiểm tra cuối). **Mục tiêu**: trang nhanh hơn, không đổi hành vi.

**Trạng thái 25/9/2026 (xong):**
- Code: merged vào `main` (a37b21a2, 32 commit, đã push origin). Nhánh `perf/*` (assets, bundle, db-index, queries-hs, rpc-gv, static-content, result) còn để đối chiếu, có thể xoá.
- Báo cáo: `perf/RESULT.md` (tổng), `perf/BASELINE.md` (mốc), `perf/DB_REPORT.md`, `perf/RLS_REPORT.md`, `perf/PHASE1_NOTES.md`, `perf/chunks-report.mjs` (đo chunk JS theo trang sau build).
- Migration: 3 file `supabase/migrations/20260925120000_perf_indexes.sql`, `…130000_perf_rpc_gv.sql`, `…140000_perf_rls.sql` — **thầy đã chạy 25/9/2026** (xác nhận trong chat). Rollback: comment cuối 2 file đầu + `perf/rollback/20260925140000_perf_rls.down.sql`.
- Deploy: `scripts/deploy.sh` chạy 25/9/2026 16:16 (nhánh deploy 5476f9e). Bản deploy build từ working tree nên gồm cả WIP chưa commit của các phiên khác.
- Kết quả: trang chủ Lighthouse 68→91, LCP 4.0→1.9 s; bài học 78→83, Supabase 10→4 req; /dashboard JS 2430→931 KB; out/ 41→34 MB.

**Còn treo / cần thầy làm:**
- Chạy `npx tsx scripts/perf-compare-rpc.mts` để đối chiếu 5 RPC mới vs đường cũ (chỉ đọc). Chưa chạy sau migration.
- ~~Thầy tự test bằng tài khoản thật~~ — **agent đã làm được 26/9/2026**, xem [[project_thachlab_auth_regression_test]]. Còn thiếu so với RESULT.md §7 gốc: Teacher Studio 11 tab + xuất Excel, điểm tháng trợ giảng (chưa test).
- Quyết định (RESULT.md §9): 2 policy tautology `attendance_sessions`/`equipment_breakdown_reports` — **đã sửa + CHẠY xong lên production 26/9/2026** (migration `20260926140000_fix_rls_tautology.sql`, xác nhận trực tiếp bằng query policy thật trên DB); `class_assessments using (true)` — sửa chung, cũng đã chạy. drop `question_bank_grade_idx` sau khi theo dõi idx_scan; thêm `updated_at` cho lessons/lesson_items; cache header ảnh trong .htaccess; xoá `@xmldom/xmldom` + `services/excel-export.ts`; region Sydney→Singapore.

**Quyết định thiết kế đã chốt (đọc code không tự suy ra):**
- Nội dung lý thuyết sinh tĩnh vào `public/data/` lúc `prebuild` (`scripts/build-content.mjs`, anon key, chỉ mục `ly_thuyet`/video, KHÔNG đáp án/lời giải; ignore trong git). Trang HS đọc tĩnh trước rồi đối chiếu ngầm với DB (`services/static-content.ts`); admin/GV luôn đọc Supabase. **Sửa lý thuyết tại chỗ chỉ lên web sau khi chạy lại `scripts/deploy.sh`** (không có updated_at) — đã ghi README.
- 5 RPC GV (`services/class-rpc.ts`) `security invoker`, có fallback đường cũ khi hàm chưa tồn tại.
- KaTeX giữ đồng bộ ở trang HS (bài học, làm đề) — lazy chỉ ở admin/GV/tin-tức; framer-motion vẫn import tĩnh ở ExamRunner/QuestionCard/Rank (nơi dùng thật).
- Ảnh trong `public/lessons/**` được tham chiếu từ HTML trong DB → chỉ nén tại chỗ giữ tên; ảnh từ code → .webp. Bản gốc ở `public/_originals/` (ignore).
- Font self-host `next/font` (`app/fonts.ts`): Be Vietnam Pro 400/600/700/800, Inter 400/500/600, JetBrains Mono chỉ 400.

**Kỹ thuật cho agent/worktree:** symlink node_modules từ repo gốc + copy .env.local; Turbopack từ chối symlink ra ngoài /Users/MAC (root suy từ lockfile lạc `/Users/MAC/package-lock.json`) — lỗi cụ thể: "Symlink [project]/node_modules is invalid, it points out of the filesystem root". **Cách né (26/9/2026, đã test thành công):** đừng symlink, dùng `cp -al ../../../node_modules node_modules` (hardlink clone, cùng ổ đĩa nên gần như tức thời, không tốn thêm dung lượng thật) — Turbopack coi đây là thư mục thật trong worktree, không còn lỗi root. `tsconfig` include cả `scripts/` nên script WIP lỗi kiểu làm `next build` fail — 25/9 đã sửa 1 dòng ở `scripts/_tmp_bulk_upload_de_thi_thu.mts:180` (file WIP chưa commit của phiên khác).

**Đợt 4 (27/9/2026, XONG — đã push + deploy, xem diễn biến đầy đủ bên dưới):** tách JS riêng trang
`/kiem-tra/lam` và `/lop-hoc/bai` bằng `next/dynamic`, cộng cache header ảnh trong `scripts/deploy.sh`.
Có một sự cố giữa chừng (nhiều phiên song song làm trùng + phát hiện lỗi crash trắng) đã xử lý xong,
kết quả cuối: `/kiem-tra/lam` ~1030→998 KB (đạt <1000 KB), `/lop-hoc/bai` ~1041→~1037 KB (chưa đạt —
dư là `QuestionCard`/`SampleQuestionsGrid`/"Bài tập mẫu", nội dung chính hiển thị ngay, không động
tới theo đúng phạm vi). Cache ảnh 30 ngày qua `mod_headers` đã có trong `scripts/deploy.sh`.

**Diễn biến sự cố (để hiểu tại sao có nhiều commit revert/redo, không phải làm ẩu):**
1. Agent đầu tiên tách JS xong, commit `6e9d07b3`, nhưng bài test bắt buộc chỉ yêu cầu re-test chunk
   RevealMotion CŨ chứ không test chunk MỚI agent vừa tạo — bỏ lọt: `next/dynamic({ssr:false})`
   không có error boundary có thể crash TRẮNG TOÀN TRANG nếu chunk tải lỗi (mất mạng, hoặc đúng lúc
   site vừa deploy bản mới nên chunk cũ mất theo hash) — rơi đúng vào màn "sau khi nộp bài".
2. Đã revert phần tách JS đó (`063a97a4`), chỉ giữ cache ảnh, push + deploy an toàn trước.
3. Trong lúc đó, ít nhất 2 phiên khác (chạy song song, không biết nhau) độc lập dựng cơ chế chống
   crash chung cho toàn app: `components/ui/LazyErrorBoundary.tsx` (boundary dùng chung) +
   `app/error.tsx` (route-level error boundary của Next App Router — **đây mới là lớp thật sự chặn
   được crash**, không phải class boundary cục bộ) + áp dụng vào `Reveal.tsx`, `QuestionSlide.tsx`,
   `PhysicsSimulationHero.tsx`, `ContentHtmlLazy.tsx`, `app/lop-hoc/page.tsx`, `LessonImporter.tsx`,
   `TeacherCourseDashboard.tsx`, `TeacherThptDashboard.tsx`.
4. **Đã tự tay verify bằng thực nghiệm 2 lần** (không chỉ đọc code/tin báo cáo): build sạch, xoá đúng
   file chunk RevealMotion (`ChunkLoadError ... module 69790`, khớp y hệt lỗi gốc), mở tab hoàn toàn
   mới → **không còn crash trắng** — hiện `app/error.tsx` (thông báo tiếng Việt + nút "Tải lại
   trang"), bấm nút đó (sau khi phục hồi chunk) → trang về bình thường, 0 lỗi console. Lần 1 (chỉ có
   3 file lõi) lỗi rơi xuống tận `app/error.tsx` (mất cả header/nav); lần 2 (đủ toàn bộ thay đổi)
   `LazyErrorBoundary` cục bộ trong `Reveal.tsx` bắt được luôn, trang vẫn đầy đủ — **kết luận: việc
   local boundary có bắt được hay không là KHÔNG ổn định (timing-dependent), nhưng `app/error.tsx`
   luôn luôn chặn được ở lớp cuối trong cả 2 lần thử — đây là thuộc tính an toàn cốt lõi, không phải
   local boundary**.
5. Gộp cơ chế trên lên `main` (`9d22e14c`), rồi redo lại việc tách JS có bọc `LazyErrorBoundary` cho
   từng chunk mới (`f068cf95`) — đã tự đọc code xác nhận (không đoán): `ExamRunner.submit()` và
   `PracticeSession.submit()` đều gọi `save()`/ghi Supabase **ngay trong cùng callback** với
   `setPhase("done")`, KHÔNG chờ chunk màn kết quả tải xong — nên dù chunk đó lỗi, điểm/tiến độ vẫn
   đã lưu, học sinh chỉ cần tải lại trang là thấy lại kết quả.
6. Đã tự build + tsc + lint độc lập (worktree cô lập, không lẫn WIP phiên khác) xác nhận sạch, rồi
   `git push origin main` + deploy thật qua `scripts/deploy.sh` (build từ worktree cô lập, không kéo
   theo ~70 file WIP nửa vời của các phiên khác đang có trong working tree chính).

**Bài học rút ra (quan trọng cho đợt sau):** khi yêu cầu "xoá thử 1 chunk cũ để test cơ chế chống
crash", PHẢI test cả chunk MỚI mà chính đợt đó tạo ra, không chỉ chunk cũ đề bài nêu sẵn — đây là lỗ
hổng đã gây ra toàn bộ chuỗi revert/redo ở trên.

**Đợt 5 (27/9/2026, XONG — 3 worktree/agent song song từ `main` dd9bd74e, gộp `perf5/integration`,
đã merge vào `main` `6dddfc85`, push + deploy `scripts/deploy.sh` thật):**
1. `perf5/chunk-error` (`d275112a`) — vá đúng lỗ hổng ghi ở mục 1-6 phía trên (crash trắng ngoài
   tầm React Error Boundary): thêm `components/system/ChunkErrorGuard.tsx`, mount ở `app/layout.tsx`,
   bắt `window.error`/`unhandledrejection`, nhận diện `ChunkLoadError`/"Loading chunk...failed", tự
   `location.reload()` đúng 1 lần (đánh dấu bằng `sessionStorage`), lỗi lại sau reload thì rơi xuống
   `app/error.tsx` bình thường — không đụng `Reveal.tsx`/`LazyErrorBoundary.tsx`/`app/error.tsx` sẵn
   có. Lưu ý: agent KHÔNG tái hiện được crash trắng bằng xoá chunk `RevealMotion` trên bản build hiện
   tại (khác đợt 4 — có thể do cấu trúc chunk đã đổi), chỉ verify cơ chế bằng cách bắn thẳng sự kiện
   lỗi giả lập đúng định dạng đã ghi nhận. Nên nếu sau này vẫn thấy màn trắng thật, phải tái kiểm bằng
   thực nghiệm xoá-chunk-thật như đợt 4 đã làm, đừng chỉ tin lại báo cáo này.
2. `perf5/split-samplegrid` (`ffa5e2c8`) — tách `SampleQuestionsGrid` → `SampleQuestionsGridLazy.tsx`
   bằng `next/dynamic({ssr:false})` + `LazyErrorBoundary`, dùng ở `app/lop-hoc/bai/page.tsx` +
   `InlineLessonAccordion.tsx`. Kết quả: `/lop-hoc/bai` 1038→1029 KB — **CHƯA đạt** mục tiêu <1000 KB.
   Phát hiện quan trọng: ước tính "~34 KB dư là SampleQuestionsGrid" ở `perf4/RESULT.md` §1 SAI — phần
   dư thật nằm ở `LessonMasteryCard.tsx` + code Navbar/Footer, không phải `SampleQuestionsGrid`. Muốn
   đạt <1000 KB thật sự phải làm đợt riêng động vào `LessonMasteryCard.tsx`/`page.tsx`.
3. `perf5/test-exam-flow` (`169a494c`, không sửa code) — lần đầu tiên test được luồng làm bài + nộp
   bài thật ở `/kiem-tra/lam` (đợt 4 chưa test được vì thiếu tài khoản). Tạo tài khoản throwaway qua
   `/dang-ky` (tự động active `user_classes`, KHÔNG cần service-role như từng nghĩ — file
   `docs/*.sql` là snapshot cũ, không phải schema sống, xem cảnh báo trong `AGENTS.md`). Làm đề
   `id=8` (đủ TN/Đúng-Sai/Trả lời ngắn) — chấm điểm đúng kể cả điểm bộ phận, trang xem lại đúng, khôi
   phục bài làm dở PASS (test thật lần đầu). Nghi vấn re-render đồng hồ đếm ngược (`docs/STATE.md`):
   **xác nhận đúng về code** (`ExamRunner.tsx` giữ timer + state câu hỏi chung 1 component,
   `QuestionCard` chưa memo hoá) nhưng ở đề 8 câu chưa thấy lag thật — đáng test lại ở đề 70+ câu.
   Dọn dẹp: RLS chặn học sinh tự xoá dữ liệu mình tạo (`exam_attempts`/`exam_results`/
   `exam_question_results`/`user_classes` chỉ có INSERT/SELECT) — **CÒN SÓT trên Supabase thật, thầy
   cần tự xoá bằng service-role/dashboard**: tài khoản `perf5-test-1790508919@thachlab.local`
   (id `c5466c57-b633-4da9-9088-f8ae12a0f8e0`), `user_classes` class_id 16, `exam_attempts` id 290,
   `exam_results` id 423, 8 dòng `exam_question_results`.
4. **Phát hiện phụ ngoài phạm vi (đã tách task riêng `task_412f3530`, thầy đã bấm chạy ở phiên khác,
   ĐANG CHẠY lúc bàn giao — chưa biết kết quả):** `/kiem-tra/lam` KHÔNG kiểm tra học sinh có thuộc
   lớp gán đề hay không — bất kỳ ai đăng nhập cũng mở/nộp được mọi đề đã đăng qua URL trực tiếp (đoán
   `?id=`). Chưa sửa trong đợt 5.
5. **Sự cố kỹ thuật mới phát hiện (bổ sung cho mục "Kỹ thuật cho agent/worktree" ở trên):**
   `git stash`/`git stash pop` dùng CHUNG 1 stash-stack cho TOÀN REPO — kể cả giữa các `git worktree`
   khác nhau, không cô lập theo từng worktree. 2 agent (chunk-error + split-samplegrid) cùng lúc
   dùng `git stash` để đo baseline tsc/lint đã bị lẫn thay đổi của nhau (file của người này bị pop
   nhầm vào thư mục người kia). Cả 2 tự phát hiện (diff lạ sau khi pop) và tự khôi phục đúng bằng
   `git fsck --no-reflog` tìm lại dangling commit + `git stash store`/`git stash apply <hash>` theo
   đúng hash, không mất dữ liệu — nhưng đây là may, không phải chắc chắn. **Từ nay: KHÔNG dùng
   `git stash` trần khi có nhiều worktree/agent chạy song song trên cùng repo** — đo baseline bằng
   cách khác (copy file ra `/tmp` rồi `git checkout -- <file>`, hoặc `git show HEAD:<path>`, hoặc
   commit tạm rồi `git reset --soft`), hoặc nếu bắt buộc stash thì phải gắn message riêng biệt +
   dùng `git stash apply <hash-cụ-thể>` (không dùng `pop` trần) + tự tay đối chiếu ngay sau đó.
   4 worktree đợt 5 (`perf5-chunk-error`, `perf5-split-samplegrid`, `perf5-test-exam-flow`,
   `perf5-integration`) vẫn còn trên đĩa (`.claude/worktrees/`), chưa dọn — an toàn để xoá
   (`git worktree remove`) vì đã merge xong hết vào `main`.

**Why:** việc lớn nhiều pha, nhiều phiên song song từng đưa main vào trạng thái rủi ro thật (dù ngắn,
đã kịp phát hiện trước khi deploy) — phiên sau cần hiểu rõ diễn biến để không hoảng khi thấy nhiều
commit revert/redo liên tiếp trong git log, và biết `app/error.tsx` mới là lưới an toàn thật.
**How to apply:** trước khi tách thêm JS bằng `next/dynamic`, luôn bọc `LazyErrorBoundary` (đã có sẵn
ở `components/ui/LazyErrorBoundary.tsx`) và tin rằng `app/error.tsx` là lưới cuối — nhưng vẫn phải tự
test xoá-chunk-mở-tab-mới cho MỌI chunk mới, không chỉ chunk cũ. Đọc `perf4/RESULT.md` rồi
`perf5/RESULT-*.md` (3 file: chunk-error, samplegrid, exam-flow — đọc để thấy trạng thái cuối) trước
khi làm đợt 6. Đợt 6 nên nhắm `/lop-hoc/bai` còn dư ở `LessonMasteryCard.tsx` (xem mục Đợt 5 §2) để
đạt <1000 KB, và test lại re-render đồng hồ đếm ngược ở đề 70+ câu (mục Đợt 5 §3). Khi chạy nhiều
worktree/agent song song trên cùng repo: KHÔNG dùng `git stash` trần (xem mục Đợt 5 §5). Liên quan
[[project_thachlab_concurrent_sessions]], [[feedback_thachlab_deploy_scope]],
[[reference_supabase_db_query_cli]].
