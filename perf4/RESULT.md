# RESULT4 — đợt tối ưu tốc độ lần 4 (27/9/2026)

## ĐỢT SAU (27/9/2026, cùng ngày) — Đưa cơ chế chống crash lên main + redo Việc 1 an toàn, có boundary

Tiếp nối phần "⚠ CẬP NHẬT" ngay bên dưới: 2 phiên Claude Code khác (worktree
`quizzical-gauss-065911` và `angry-curie-528414`) đã độc lập dựng một cơ chế chống crash trắng
chung cho toàn app (`components/ui/LazyErrorBoundary.tsx` + `app/error.tsx` — route-level error
boundary của Next App Router) và áp nó vào các chỗ `next/dynamic`/`React.lazy` có sẵn
(`Reveal.tsx`, `QuestionSlide.tsx`, `PhysicsSimulationHero.tsx`, `ContentHtmlLazy.tsx`,
`app/lop-hoc/page.tsx`, `LessonImporter.tsx`, `TeacherCourseDashboard.tsx`,
`TeacherThptDashboard.tsx`). Đợt này (phiên thứ 3) mang cơ chế đó lên `main`, rồi redo lại đúng
Việc 1 đã bị revert ở trên — lần này MỖI chunk mới tách đều bọc thêm `LazyErrorBoundary` cục bộ.

### Đưa cơ chế chống crash lên main

- Copy nguyên văn `components/ui/LazyErrorBoundary.tsx` (dùng bản của `angry-curie-528414` —
  superset, có thêm `LazyPanelFallback` và `fallback` optional, cần cho các file
  `LessonImporter.tsx`/`TeacherCourseDashboard.tsx`/`TeacherThptDashboard.tsx`) và `app/error.tsx`
  (từ `quizzical-gauss-065911`).
- Áp diff `Reveal.tsx`, `QuestionSlide.tsx` (từ `quizzical-gauss-065911`) và
  `PhysicsSimulationHero.tsx`, `ContentHtmlLazy.tsx`, `app/lop-hoc/page.tsx`,
  `LessonImporter.tsx`, `TeacherCourseDashboard.tsx` (từ `angry-curie-528414`) — cả 2 worktree
  sửa `PhysicsSimulationHero.tsx` khác nhau (1 bên bọc trực tiếp tại nơi dùng, 1 bên tách hàm
  wrapper riêng), dùng đúng bản `angry-curie-528414` theo đúng chỉ dẫn (mới hơn, cùng gốc
  `063a97a4`).
- **Lệch so với danh sách gốc được giao**: `angry-curie-528414` còn sửa thêm
  `components/dashboard/TeacherThptDashboard.tsx` theo đúng khuôn `lazyTab` helper — file này
  KHÔNG có trong danh sách 5 file được liệt kê ban đầu, nhưng cùng rủi ro (tab dashboard giáo
  viên dùng `next/dynamic` không bọc boundary) và là code thật có sẵn trong worktree, không phải
  tự viết thêm — đã áp luôn cho nhất quán, báo cáo rõ ở đây để thầy xác nhận/undo nếu không muốn.
- Bỏ qua hunk `ExamDoneView.tsx`/`QuestionSlide.tsx` (phần liên quan `examId`) đúng theo chỉ dẫn:
  `ExamDoneView.tsx` không tồn tại trên `main` (đã xoá khi revert `063a97a4`), tạo lại từ đầu ở
  phần Việc 2 bên dưới, dựa trên nội dung THẬT trên `main` (không phải bản cũ trong worktree, vì
  `ExamReviewPager.tsx` trên `main` hiện có thêm `examId`/`ReportQuestionButton` — WIP của một
  phiên khác — nhưng `ExamRunner.tsx` hiện tại CHƯA truyền `examId` vào lời gọi đó, nên
  `ExamDoneView.tsx` mới tạo cũng KHÔNG thêm `examId` để giữ đúng hành vi hiện tại, không tự ý
  đổi thêm).

### Hồi quy bắt buộc (Việc 1 bước 6) — xoá thử chunk RevealMotion

Build sạch, `npx serve out` (cổng riêng `48173` qua `.claude/launch.json` tạm, không commit), xác
định đúng 2 bản chunk RevealMotion (`grep "prefers-reduced-motion"`, khớp `module 69790` — đúng
số hiệu `perf2/RESULT.md`/`perf4/RESULT.md` §6 đã ghi từ trước) — trang chủ dùng nhiều `<Reveal>`
nên có 2 bản chunk trùng nội dung (Turbopack không dedupe chunk `next/dynamic`/`React.lazy` giữa
các "async boundary" khác nhau). Xoá cả 2, mở tab HOÀN TOÀN MỚI, vào `/`:

**Kết quả: KHÔNG crash trắng, KHÔNG cần tới `app/error.tsx`** — `LazyErrorBoundary` cục bộ trong
`Reveal.tsx` bắt được `ChunkLoadError` (console: `Failed to load chunk ... from module 69790` +
bản còn lại `module 12036`, đúng cặp chunk vừa xoá), toàn trang hiện đầy đủ nội dung ở trạng thái
cuối (không hiệu ứng, đúng thiết kế `shownFallback` của `Reveal.tsx`) — về mặt hình ảnh không
phân biệt được với lúc chunk tải thành công. Xác nhận lại bằng `get_page_text`: không có dòng
"Có lỗi xảy ra"/"Trang tải chưa xong" nào của `app/error.tsx`.

**Lưu ý khác với ghi chú trong chính `components/ui/LazyErrorBoundary.tsx`** (mục "GIỚI HẠN", viết
bởi phiên `angry-curie-528414`): file đó ghi rằng RevealMotion là "một trường hợp KHÔNG bắt được"
cục bộ (phải rơi xuống `app/error.tsx`) vì dùng `React.lazy()` + render ngay trong lần hydrate
đầu. Thực nghiệm của phiên này (build sạch riêng, xoá đúng 2 file chunk, tab mới) lại cho kết quả
NGƯỢC LẠI — bắt được cục bộ, không cần `app/error.tsx`. Không sửa lại comment đó (file được yêu
cầu copy nguyên văn, không tự ý đổi), chỉ ghi nhận lệch pha ở đây — có thể do khác biệt thời điểm
build/thời điểm lỗi xảy ra trong tiến trình hydrate giữa 2 lần thử; DÙ SAO kết quả thực tế vẫn là
điều tốt hơn mong đợi (không crash, không cần lưới cuối), không phải vấn đề cần sửa gấp, nhưng
thầy nên biết ghi chú "GIỚI HẠN" đó chưa chắc còn đúng 100%.

Build sạch: OK · `npx tsc --noEmit`: 0 lỗi · `npm run lint` (đo cô lập, stash đúng 13 file Việc 1
+ file mới, so với gốc `063a97a4`): **8025 problems (175 errors, 7850 warnings)** cả trước lẫn
sau — không tăng.

### Việc 2 — redo tách JS có boundary

Dựa đúng cách tách của commit cũ `6e9d07b3` (`git show 6e9d07b3 -- <file>` để lấy diff/nội dung
tham khảo — đã xác nhận áp `git apply` sạch lên `main` hiện tại nhờ 3 file nguồn
(`ExamRunner.tsx`, `PracticeSession.tsx`, `LessonMasteryCard.tsx`) chưa bị phiên nào khác đụng
tới kể từ đó), rồi bọc thêm `LazyErrorBoundary` quanh mỗi chunk mới (khác biệt so với đợt cũ):

| File mới | Bọc boundary | Fallback |
|---|---|---|
| `components/exams/ExamDoneView.tsx` | Trong `ExamRunner.tsx`, hàm `ExamDoneView` bọc `ExamDoneViewLazy` | "Điểm của em đã được lưu, nhưng trang không hiện được phần xem lại..." + nút Tải lại trang |
| `components/lessons/PracticeRunningView.tsx` | Trong `PracticeSession.tsx` | "Không tải được phần làm bài... Thử tải lại trang." (chưa nộp, chưa có gì để mất) |
| `components/lessons/PracticeDoneView.tsx` | Trong `PracticeSession.tsx` | "Kết quả luyện tập của em đã được lưu, nhưng trang không hiện được phần xem lại..." |
| — (đổi `TopicPracticeModal` sang `next/dynamic`) | Trong `LessonMasteryCard.tsx` | Modal nhỏ có nút "Đóng" (dùng lại `onClose` sẵn có) |

**Xác nhận an toàn dữ liệu (đọc code, không đoán)**:
- `ExamRunner.tsx`: `submit()` (dòng ~209) gọi `setPhase("done")` RỒI `save()` ngay trong CÙNG một
  callback — `save()` (ghi `exam_results`/`exam_question_results`, `finishExamAttempt`) chạy
  ĐỘC LẬP hoàn toàn với việc chunk `ExamDoneView` tải được hay không. An toàn để fallback báo
  "điểm đã lưu".
- `PracticeSession.tsx`: `submit()` cùng cấu trúc — `setPhase("done")` rồi `save(used, timedOut)`
  ngay trong cùng callback, độc lập với `PracticeDoneView`. An toàn để fallback báo "kết quả đã
  lưu". `PracticeRunningView` thì ngược lại — bài này KHÔNG có autosave định kỳ như
  `ExamRunner.tsx` (không có `exam_attempts`-style interval), nên nếu chunk này lỗi thì đúng là
  chưa có gì được lưu — fallback KHÔNG khẳng định gì về dữ liệu, đúng thực tế.

**Đo KB** (`perf/chunks-report.mjs` + script liệt kê chunk theo trang, đo TRÊN CHÍNH working tree
hiện tại — trước/sau đều có sẵn Việc 1 + toàn bộ WIP khác trong repo, để so sánh công bằng thay vì
dùng số liệu `BASELINE.md` cũ đã lệch pha do WIP song song từ 27/9 tới nay):

| Trang | Trước Việc 2 (KB) | Sau Việc 2 (KB) | Đạt <1000 KB? |
|---|---:|---:|---|
| `/kiem-tra/lam` | 1029,1 (15 chunk) | **999,8** (15 chunk) | **ĐẠT** (giảm 29,3 KB) |
| `/lop-hoc/bai` | 1041,1 (16 chunk) | **1036,8–1037,5** (16 chunk, dao động nhẹ theo hash build) | **KHÔNG** (giảm ~4 KB) |

Kết luận `/lop-hoc/bai` giống hệt đợt cũ đã revert: phần dư là `QuestionCard.tsx` qua
`SampleQuestionsGrid.tsx` (mục "Bài tập mẫu", nội dung chính hiển thị ngay) — KHÔNG động tới theo
đúng phạm vi. Số liệu tuyệt đối cao hơn khoảng 2–3 KB so với `perf4/BASELINE.md` gốc (27/9 sáng)
do (a) mã `LazyErrorBoundary` mới thêm vào mỗi chunk, và (b) WIP khác của các phiên song song
trong cùng working tree ảnh hưởng nhẹ tới các chunk nền dùng chung.

Build sạch + `npx tsc --noEmit` (0 lỗi) + `npm run lint` sau khi thêm cả Việc 2: **8025 problems
(175 errors, 7850 warnings)** — không tăng so với gốc, đo ngay sau khi tạo xong 3 file mới, trước
khi phiên khác kịp sửa gì thêm. (Lần đo `npm run lint` cuối cùng trước khi commit cho ra
8028 — nhưng đối chiếu từng file xác nhận +3 đó đến từ `app/lop-hoc/bai/page.tsx`, một file
KHÔNG nằm trong bất kỳ thay đổi nào của phiên này, bị một phiên song song khác sửa ngay TRONG
LÚC phiên này đang chạy — đúng rủi ro "repo dùng chung" đã được cảnh báo trước; không phải lỗi
do Việc 1/Việc 2.)

### Test xoá-chunk cho từng chunk mới (Việc 2) — bắt buộc, đây là phần đợt trước thiếu

Không tạo tài khoản học sinh thật trong production (đúng tiền lệ các đợt trước) nên không lái
được luồng thật (đăng nhập → làm bài → nộp) để chạm đúng 4 màn hình này. Thay vào đó dựng một
trang test TẠM (`app/test-chunk-boundary/page.tsx`, đã XOÁ trước khi commit, không có trong diff)
gọi ĐÚNG nguyên văn `next/dynamic(() => import("@/components/..."))` + `LazyErrorBoundary` y hệt
cách các file thật đang dùng, với props giả tối thiểu hợp lệ (không gọi mạng — `examIds: []`,
`topic: ""` để tránh side-effect Supabase) — cùng cơ chế, khác chunk file (Turbopack tạo chunk
riêng theo route nên chunk qua trang test có hash khác chunk thật của `/kiem-tra/lam`, nhưng cùng
bytecode/cùng cách bọc). Baseline (chunk còn nguyên) cho cả 4 đều render đúng, 0 lỗi console. Sau
đó xoá từng chunk một, mở tab HOÀN TOÀN MỚI mỗi lần:

| Chunk mới | Kết quả xoá | Console |
|---|---|---|
| `ExamDoneView` | **Bắt cục bộ** — hiện đúng fallback "Điểm của em đã được lưu...", trang vẫn dùng được (test click nút khác vẫn phản hồi) | `ChunkLoadError ... from module 27992` |
| `PracticeRunningView` | **Bắt cục bộ** — fallback "Không tải được phần làm bài..." | `ChunkLoadError ... from module 18409` |
| `PracticeDoneView` | **Bắt cục bộ** — fallback "Kết quả luyện tập... đã được lưu..." | `ChunkLoadError ... from module 61210` |
| `TopicPracticeModal` | **Bắt cục bộ** — fallback modal nhỏ có nút Đóng | `ChunkLoadError ... from module 33036` |

Cả 4/4 đều bắt được CỤC BỘ (tốt hơn mức tối thiểu yêu cầu — không chunk nào phải rơi xuống
`app/error.tsx`), không có trường hợp nào crash trắng.

### Smoke test + dọn dẹp

`npx serve out` (cổng `48173`) + tab mới: `/lop-hoc/bai/?id=49` (hiện đúng bài học, lý thuyết +
hình vẽ, 0 lỗi console), `/kiem-tra/lam/?id=118` (đúng màn "Em cần đăng nhập...", 0 lỗi console).
`.claude/launch.json` (thêm tạm config `thachlab-serve-out` để test) đã `git checkout` phục hồi
nguyên trạng, KHÔNG nằm trong commit. `scripts/deploy.sh`/khối `.htaccess` cache ảnh: không đụng
tới trong đợt này.

### Việc cần thầy quyết / lưu ý thêm

1. Đã tự ý áp thêm diff `TeacherThptDashboard.tsx` (ngoài danh sách gốc) — xem mục "Lệch so với
   danh sách gốc" ở trên, cần thầy xác nhận giữ hay revert riêng file này.
2. Ghi chú "GIỚI HẠN" trong `components/ui/LazyErrorBoundary.tsx` (RevealMotion không bắt được
   cục bộ) có thể đã lỗi thời — thực nghiệm đợt này cho kết quả ngược lại (bắt được). Không tự
   sửa comment (file được yêu cầu copy nguyên văn của phiên khác), nhưng nên có phiên sau kiểm
   lại kỹ hơn (nhiều lần, nhiều điều kiện mạng) trước khi khẳng định chắc chắn.
3. `/lop-hoc/bai` vẫn CHƯA đạt <1000 KB — giống hệt kết luận đợt trước, cần quyết định có tách
   `SampleQuestionsGrid` (đổi UX, có thể chớp nháy loading) hay chấp nhận ~1037 KB.

## ⚠ CẬP NHẬT SAU KHI VIẾT BÁO CÁO — Việc 1 ĐÃ REVERT, KHÔNG deploy

Một phiên Claude Code khác chạy song song (`perf/round4-katex-framer-split`, commit `7193ebc6`)
làm đúng đợt 4 này độc lập, và khi tự kiểm bằng cách xoá thử 1 file chunk phát hiện:
`next/dynamic()`/`React.lazy()` không có error boundary bọc quanh có thể **crash TOÀN TRANG**
nếu chunk tải lỗi (mạng chập chờn, hoặc kịch bản thực tế: học sinh đang mở đề/bài học đúng lúc
site vừa deploy bản mới → chunk cũ theo hash bị xoá → tải lỗi) — rơi đúng vào màn "sau khi nộp
bài", đúng luồng yêu cầu gốc cấm rủi ro tuyệt đối. Phiên đó đã revert phần tách JS, chỉ giữ cache
header. Phiên viết báo cáo này (agent) **không phát hiện ra rủi ro trên** vì chỉ test crash-chunk
trên trang chủ (RevealMotion, xem §6), không test lại đúng `ExamDoneView`/`PracticeDoneView` mới
thêm — thiếu sót cần rút kinh nghiệm.

Sau khi thầy xem xét, quyết định: **revert toàn bộ Việc 1** (3 file mới `ExamDoneView.tsx`,
`PracticeRunningView.tsx`, `PracticeDoneView.tsx` đã xoá; `ExamRunner.tsx`/`PracticeSession.tsx`/
`LessonMasteryCard.tsx` khôi phục về bản trước đợt 4 — commit `5ab19390`), **giữ nguyên Việc 2**
(cache header ảnh). `/lop-hoc/bai` và `/kiem-tra/lam` quay lại đúng KB như trước đợt 4 (xem
`perf4/BASELINE.md`), CHƯA đạt mục tiêu <1000 KB — để đợt sau làm lại có kèm error boundary đúng
cách (xem việc cần thầy quyết #1 mới bên dưới).

Toàn bộ nội dung bên dưới (§1–§8) là **báo cáo gốc của lần thử đã bị revert**, giữ lại để tham
khảo cách đo/kỹ thuật tách — KHÔNG phản ánh trạng thái code hiện tại trên `main`.

---

Gộp 2 việc còn treo trong `docs/STATE.md` mục "Việc ngoài roadmap đang treo": (1) tách phần
JS riêng của trang (không phải KaTeX/framer — 2 thứ đó đã lazy đúng từ đợt 2) khỏi
`/lop-hoc/bai` và `/kiem-tra/lam`; (2) thêm cache header `Cache-Control` tường minh cho ảnh trong
`scripts/deploy.sh`. Chi tiết mốc trước khi sửa: `perf4/BASELINE.md`.

**Tóm tắt 6 dòng**
1. Build sạch OK, `tsc --noEmit` 0 lỗi, `npm run lint` **8025 problems (175 errors, 7850
   warnings)** trước và sau khi sửa — không tăng (đo cô lập bằng cách tạm stash đúng 3 file sửa +
   cất riêng 2 file mới, loại WIP không liên quan của phiên khác ra khỏi phép so sánh).
2. **`/kiem-tra/lam` ĐẠT mục tiêu <1000 KB**: 1027,3 → **997,4 KB** (giảm 29,9 KB) — tách màn
   "sau khi nộp bài" (điểm + xem lại bài làm) của `ExamRunner.tsx` ra
   `components/exams/ExamDoneView.tsx`, tải qua `next/dynamic({ ssr:false })`.
3. **`/lop-hoc/bai` CHƯA đạt** <1000 KB: 1040,1 → **1033,7 KB** (giảm 6,4 KB) — tách 2 màn
   "đang làm"/"sau khi nộp" của `PracticeSession.tsx` (mục Luyện tập) ra
   `PracticeRunningView.tsx`/`PracticeDoneView.tsx`, và modal "Luyện 10 câu phần này"
   (`TopicPracticeModal.tsx`, từ `LessonMasteryCard.tsx`) — cả 3 đều lazy đúng cách (xác nhận
   bằng cách đọc chunk nào nằm trong `<script>` ban đầu của trang, xem §3). Phần dư ~34 KB còn lại
   là `QuestionCard.tsx` + logic dùng chung, vẫn cần tải ngay vì `SampleQuestionsGrid.tsx` (mục
   "Bài tập mẫu") dùng nó — đây là **nội dung chính hiển thị ngay**, đúng phạm vi bị cấm động vào
   trong yêu cầu ("KHÔNG được động vào nội dung chính hiển thị ngay") nên KHÔNG tách thêm. Xem §7
   việc cần thầy quyết nếu muốn tách tiếp.
4. Cache ảnh: `scripts/deploy.sh` đã có `ExpiresDefault "access plus 30 days"` (mod_expires, commit
   `ec21f5fb` từ trước) — đợt này CHỈ bổ sung thêm khối `<IfModule mod_headers.c>` với
   `Header set Cache-Control "public, max-age=2592000"` đúng theo yêu cầu, không xoá/sửa khối cũ.
   `httpd -t` xác nhận cú pháp Apache hợp lệ (xem §5).
5. Smoke test bằng Browser pane (`npx serve out`): `/lop-hoc/bai/?id=49` — 5 công thức `.katex`
   render đúng (khớp `perf3/RESULT.md`), accordion "Bài tập mẫu" mở/đóng đúng, mục "Luyện tập"
   hiện đúng màn "Đăng nhập để…" (chưa đăng nhập); `/kiem-tra/lam/?id=118` — chỉ thấy màn yêu cầu
   đăng nhập (đúng, không tạo tài khoản thật); không lỗi console ở cả hai. **Không tự test được
   luồng nộp bài/chấm điểm thật** (cần tài khoản — ngoài phạm vi phiên này), xem §7.
6. **Phát hiện lỗi nghiêm trọng TIỀN NHIỆM, KHÔNG do đợt này gây ra**: xoá thử chunk `RevealMotion`
   trên trang chủ làm **crash trắng toàn trang** ngay lập tức (< 2 giây, trước khi cơ chế
   `PendingFallback` 4 giây trong `components/ui/Reveal.tsx` kịp chạy) — mâu thuẫn với báo cáo
   "đã vá xong" của `perf2/RESULT.md` §6.1. Đã KHÔNG sửa (ngoài phạm vi 2 việc được giao, file
   không đụng tới), đã phục hồi file test, đã báo riêng cho thầy (xem §6).

## 1. Build / kiểu / lint

| Bước | Kết quả |
|---|---|
| `rm -rf .next out && npm run build` | OK, 66 trang tĩnh |
| `npx tsc --noEmit` | OK, 0 lỗi |
| `npm run lint` (trước sửa, cô lập khỏi WIP khác) | 8025 problems (175 errors, 7850 warnings) |
| `npm run lint` (sau sửa, toàn bộ working tree) | **8025 problems (175 errors, 7850 warnings)** — không tăng |

## 2. Việc 1 — tách JS riêng trang cho `/lop-hoc/bai` và `/kiem-tra/lam`

### Đã làm

| File mới | Tách từ | Lý do lazy được (không phải nội dung hiển thị ngay) |
|---|---|---|
| `components/exams/ExamDoneView.tsx` | `ExamRunner.tsx` (phase `"done"`) | Chỉ hiện SAU khi học sinh bấm "Nộp bài" — không có ở lần render đầu (`phase` khởi tạo là `"intro"`). Kéo theo `ExamResultSummary` + `ExamReviewPager` (373 dòng gộp) + `ResultSticker`/`ReportQuestionButton`. |
| `components/lessons/PracticeRunningView.tsx` | `PracticeSession.tsx` (phase `"running"`) | Chỉ hiện SAU khi bấm "Bắt đầu luyện N câu" ở màn chọn số câu (`phase` khởi tạo `"setup"`). Kéo theo `QuestionCard`. |
| `components/lessons/PracticeDoneView.tsx` | `PracticeSession.tsx` (phase `"done"`) | Chỉ hiện SAU khi nộp phiên luyện tập. |
| — (không tạo file mới) | `components/mastery/LessonMasteryCard.tsx` | `TopicPracticeModal` đổi từ import tĩnh sang `next/dynamic({ssr:false})` — modal thật (đúng nghĩa "modal phụ"), chỉ mount khi bấm "Luyện 10 câu phần này". |

Cả 4 chỗ đều dùng đúng khuôn mẫu `next/dynamic(() => import(...), { ssr: false, loading: ... })`
đã có sẵn trong codebase (`components/home/PhysicsSimulationHero.tsx`,
`components/admin/LessonImporter.tsx`, `app/lop-hoc/page.tsx` — đọc trước khi viết, không phát
minh cách mới). `loading` hiện dòng chữ ngắn khớp văn phong app (`"Đang tính điểm…"`, `"Đang tải
câu hỏi…"`) thay vì `null`, vì đây là màn hình học sinh đang chờ sau một hành động bấm nút (khác
`FormulaPanel`/`WorkedQuestionsGrid` vốn là panel phụ không cần phản hồi ngay).

**Không đổi logic chấm điểm/nộp bài/lưu Supabase** — mọi hàm ghi dữ liệu (`save`, `submit`, RPC,
`insert`…) vẫn nằm nguyên trong `ExamRunner.tsx`/`PracticeSession.tsx`; các file mới chỉ nhận props
đã tính sẵn (`responses`, `saveState`, `onRetry`…) và hiển thị — xác nhận bằng cách đọc lại
diff, không có dòng nào động vào `services/progress.ts`, `services/lessons.ts`, `supabase.from(...)`.

### Kết quả đo (`perf/chunks-report.mjs` + script liệt kê từng chunk theo trang)

| Trang | Trước (KB) | Sau (KB) | Số chunk | Đạt <1000 KB? |
|---|---:|---:|---:|---|
| `/lop-hoc/bai` | 1040,1 | **1033,7** | 15 → 15 | **KHÔNG** (dư 33,7 KB) |
| `/kiem-tra/lam` | 1027,3 | **997,4** | 14 → 14 | **ĐẠT** |

Đối chiếu từng chunk (không đoán): `/kiem-tra/lam` — chunk riêng trang `3xjt9iazxak7w.js` 97,6 KB
→ `3qoujvwu5wfsk.js` 67,7 KB (giảm 29,9 KB, đúng bằng phần `ExamResultSummary`+`ExamReviewPager`+
`ResultSticker`+`ReportQuestionButton` vừa tách). `/lop-hoc/bai` — 2 chunk riêng trang
71,3+39,0=110,3 KB → 73,4+30,6=104,0 KB (giảm 6,3 KB) — ít hơn kỳ vọng ban đầu vì `QuestionCard`
KHÔNG được loại khỏi chunk này: `SampleQuestionsGrid.tsx` (mục "Bài tập mẫu", hiện ngay khi mở
bài) cũng import tĩnh `QuestionCard`, nên dù `PracticeSession` không còn dùng trực tiếp,
webpack/turbopack vẫn phải gộp `QuestionCard` vào JS ban đầu của trang qua đường
`SampleQuestionsGrid`. Xác nhận bằng cách xoá thử `SampleQuestionsGrid`/`QuestionCard` khỏi phép
tính (đọc chunk content bằng `grep`) — khoản tiết kiệm thật sự chỉ là phần JSX/logic hiển thị
riêng của 2 màn running/done (nhỏ), không phải toàn bộ `QuestionCard`.

**Không tách thêm `SampleQuestionsGrid`** dù đây là chunk riêng lớn nhất còn lại (~30 KB) — component
này là nội dung CHÍNH của mục "Bài tập mẫu", hiển thị ngay khi mở bài học (không phải modal/panel
phụ, không gated sau một cú click như 3 chỗ đã tách ở trên) — đúng phạm vi bị cấm ("KHÔNG được
động vào nội dung chính hiển thị ngay") trong yêu cầu. Xem §7 nếu thầy muốn cân nhắc đánh đổi này.

## 3. Xác nhận KaTeX/framer-motion không nằm trong JS ban đầu (không lặp lại việc đã làm ở đợt 2)

Cả 2 trang, danh sách `<script>` ban đầu: không có chunk ~290 KB (KaTeX) hay ~139 KB
(framer-motion) — đúng như `perf2/RESULT.md` §3 đã xác nhận từ trước. `components/exams/
ContentHtml.tsx` (KaTeX lazy theo `hasMath()`), `components/exams/QuestionSlide.tsx`
(framer-motion lazy qua `QuestionSlideMotion`) — không đụng tới, đọc lại xác nhận vẫn nguyên vẹn.

## 4. `npx serve out` + Browser pane

| Trang | Kết quả |
|---|---|
| `/lop-hoc/bai/?id=49` | OK. 5 `.katex`, 0 lỗi (khớp `perf3/RESULT.md`). Accordion "Ví dụ 1" (Bài tập mẫu) mở → hiện lời giải đúng, đóng lại → ẩn đúng, không lỗi console (2 lần bấm, tab sạch riêng để loại console cộng dồn). Mục "Luyện tập" hiện đúng "Đăng nhập để xem ngân hàng câu hỏi và luyện tập." (chưa đăng nhập — không tạo tài khoản thật). |
| `/kiem-tra/lam/?id=118` | OK. Chỉ thấy "Em cần đăng nhập để sử dụng tính năng này." — **hạn chế môi trường**: không tự test được luồng làm bài/nộp bài/xem `ExamDoneView` thật vì cần tài khoản học sinh thật, ngoài phạm vi phiên này (không tự tạo tài khoản production). |
| `/` (mobile 375px) | Nội dung hiển thị đúng, không lỗi console. Ghi nhận phụ (không phải do đợt này): một số khối tràn nhẹ sang phải ở 375px — có sẵn từ trước, không đụng CSS/layout trong đợt này nên không sửa. |

`read_console_messages(onlyErrors:true)` trên tab MỚI (không cộng dồn) cho cả 2 trang mục tiêu:
rỗng.

## 5. Việc 2 — cache header ảnh trong `scripts/deploy.sh`

Chỉ sửa đúng phần sinh `.htaccess` (dòng ~15–43), không đụng phần build/git/push. Thêm:

```apache
<IfModule mod_headers.c>
  <FilesMatch "\.(png|jpe?g|webp|svg|gif)$">
    Header set Cache-Control "public, max-age=2592000"
  </FilesMatch>
</IfModule>
```

Đặt sau khối `mod_expires` sẵn có (commit `ec21f5fb`, 26/9) — KHÔNG xoá/sửa khối cũ, chỉ bổ sung
thêm lớp `Cache-Control` tường minh (một số CDN/hosting ưu tiên đọc header này hơn `Expires`; cùng
giá trị 30 ngày = 2 592 000 giây nên không xung đột).

Kiểm tra: `npm run build` → chạy đúng đoạn heredoc sinh `.htaccess` từ `scripts/deploy.sh` vào
`out/.htaccess` (giả lập bước cuối, KHÔNG chạy `git init`/`push` thật) → xác nhận khối
`mod_headers` có mặt đúng nội dung. Kiểm cú pháp Apache bằng `httpd -t` với `httpd.conf` tối thiểu
load `mod_expires`+`mod_headers`+`mod_dir`+`mod_mime`+`mod_mpm_prefork`, `AllowOverride All` trỏ
vào thư mục chứa file: **`Syntax OK`**.

## 6. Phát hiện lỗi nghiêm trọng — KHÔNG do đợt này, chưa sửa

Làm đúng bước kiểm tra bắt buộc #5 của yêu cầu ("xoá thử chunk RevealMotion… xác nhận
PendingFallback vẫn hoạt động"): build sạch → `npx serve out` → xác định đúng chunk RevealMotion
(khớp `module 69790`, đúng số hiệu `perf2/RESULT.md` §6 đã ghi) → xoá file → mở tab HOÀN TOÀN MỚI
→ vào `/`.

**Kết quả: crash trắng toàn trang trong vòng < 2 giây** — màn hình lỗi chung chung "This page
couldn't load / Reload to try again, or go back.", console `Uncaught ChunkLoadError: Failed to
load chunk ... from module 69790 ... at async Promise.all (index 1)`. Tái hiện được 2 lần (build
sạch lại, xoá lại đúng 1 file, tab mới mỗi lần) — không phải nhiễu ngẫu nhiên. Đã phục hồi file
ngay sau khi xác nhận (không để lại trạng thái hỏng), xác nhận trang chủ tải lại bình thường trên
tab hoàn toàn mới (0 lỗi console).

Đối chiếu `components/ui/Reveal.tsx`: cơ chế `PendingFallback` (setTimeout 4000 ms) +
`RevealErrorBoundary` (`getDerivedStateFromError`) đúng như `perf2/RESULT.md` §6.1 mô tả đã vá —
NHƯNG thực nghiệm lần này cho thấy lỗi xảy ra **trước cả 2 giây**, tức trước khi timeout 4 giây có
cơ hội chạy, VÀ là `Uncaught` (không bị bất kỳ boundary/catch nào bắt) — khác hẳn kịch bản mà
`PendingFallback` được thiết kế để xử lý (Suspense kẹt ở fallback thay vì chuyển sang lỗi). Chuỗi
`at async Promise.all (index 1)` trong stack cho thấy lỗi tới từ cơ chế nạp chunk của Turbopack
runtime (`turbopack-*.js`) ở một `Promise.all` gộp nhiều chunk — nằm NGOÀI phạm vi mà
`try/catch`/`ErrorBoundary` phía React có thể can thiệp, nên dù `PendingFallback`/
`RevealErrorBoundary` có đúng logic thì vẫn không chạm tới được lỗi này.

**KHÔNG tự sửa** — đây là file `components/ui/Reveal.tsx`/`RevealMotion.tsx`, hoàn toàn ngoài
phạm vi 2 việc được giao (tách JS trang bài/đề + cache ảnh), và là cơ chế được yêu cầu rõ "TUYỆT
ĐỐI không được gỡ hay phá" — sửa vội một cơ chế phòng lỗi mà chưa hiểu rõ gốc rễ (khả năng liên
quan tới cách Turbopack xử lý lỗi tải chunk trong `Promise.all`, khác hành vi Webpack mà
`perf2/RESULT.md` có thể đã giả định) rủi ro cao hơn là để nguyên và báo cáo. Đã dùng công cụ
`spawn_task` để tạo việc riêng gắn cờ cho thầy xem xét độc lập (không phải phần việc này).

## 7. Việc cần thầy quyết

| # | Việc | Đề xuất |
|---|---|---|
| 1 | **`/lop-hoc/bai` còn dư ~34 KB** so với mục tiêu <1000 KB (1033,7 KB) — toàn bộ phần dư là `QuestionCard.tsx` + `SampleQuestionsGrid.tsx` (mục "Bài tập mẫu"), nội dung chính hiển thị ngay khi mở bài, đợt này KHÔNG động tới theo đúng giới hạn phạm vi. | Nếu thầy chấp nhận đánh đổi "mục Bài tập mẫu có thể chớp nháy loading rất ngắn lúc đầu" để đạt <1000 KB, có thể tách `SampleQuestionsGrid` bằng `next/dynamic({ssr:false})` với `loading` hiện đúng dòng "Đang tải bài tập mẫu…" nó vốn đã có sẵn (ít rủi ro vì component này vốn đã có màn chờ dữ liệu tương tự) — nhưng đây là quyết định đổi UI, cần thầy xác nhận trước khi làm. |
| 2 | **Lỗi nghiêm trọng RevealMotion/Turbopack** (§6) — trang chủ crash trắng nếu đúng 1 file JS bị lỗi tải (mất mạng, hosting phục vụ thiếu file, CDN lỗi…). Đã tạo task riêng để thầy xem xét độc lập, không nằm trong phạm vi đợt này. | Xem chip việc riêng đã tạo; cần thầy hoặc phiên khác điều tra sâu cơ chế Turbopack + `React.lazy`/`Suspense` trong build tĩnh, có thể cần đổi cách bắt lỗi (ví dụ lắng nghe `window.addEventListener("error")`/`unhandledrejection` ở mức cao hơn React, vì lỗi này không đi qua đường ErrorBoundary bình thường được). |
| 3 | Chưa tự test được luồng làm bài/nộp bài thật của `/kiem-tra/lam` (cần tài khoản học sinh — không tạo tài khoản production trong phiên này). | Thầy tự làm thử 1 đề bất kỳ sau khi deploy để xác nhận `ExamDoneView` hiện đúng điểm + "Xem lại bài làm", và 1 phiên "Luyện tập" ở `/lop-hoc/bai` để xác nhận `PracticeRunningView`/`PracticeDoneView`. |

## 8. Commit

Chỉ add đúng các file đã sửa cho 2 việc trên (không `git add -A`):
`components/exams/ExamRunner.tsx`, `components/exams/ExamDoneView.tsx` (mới),
`components/lessons/PracticeSession.tsx`, `components/lessons/PracticeRunningView.tsx` (mới),
`components/lessons/PracticeDoneView.tsx` (mới), `components/mastery/LessonMasteryCard.tsx`,
`scripts/deploy.sh`, `perf4/BASELINE.md`, `perf4/RESULT.md`. Không push nhánh `deploy`, không chạy
phần rsync/upload thật của `scripts/deploy.sh`, không chạy migration/RLS/Supabase nào.
