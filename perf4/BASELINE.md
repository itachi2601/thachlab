# BASELINE4 — mốc trước đợt tối ưu tốc độ lần 4 (27/9/2026)

Đo trên `main` tại thời điểm bắt đầu đợt việc (working tree có nhiều WIP không liên quan của các
phiên khác — không đụng tới, chỉ đo). `rm -rf .next out && npm run build` sạch, 66 trang tĩnh, sau
đó `node perf/chunks-report.mjs .` + script riêng liệt kê từng chunk theo trang (giữ ở
`/tmp/page-chunks.mjs` trong phiên, không commit).

## Đọc trước khi làm (bước 0, đã đọc kỹ)

- `docs/STATE.md` — mục "Việc ngoài roadmap đang treo" liệt kê 2 việc của đợt này, NHƯNG con số
  "~1,4 MB" ghi trong đó đã CŨ — `perf2/RESULT.md` (đợt tối ưu lần 2, đã merge vào main qua
  `1700f56f`) cho thấy KaTeX/framer-motion đã được tách lazy đúng cách từ trước (commit
  `b5822063`, `382b4204`…), 2 trang này đã giảm xuống còn ~1039/1023 KB — GẦN đạt mục tiêu
  <1000 KB, không phải "vẫn 1,4 MB" như STATE.md mô tả. STATE.md chưa được cập nhật lại sau khi
  perf2 merge — đợt này coi `perf2/RESULT.md` §3 là số liệu đúng, không làm lại KaTeX/framer từ
  đầu.
- Tương tự, việc 2 (cache ảnh) **đã có một phần** trong `scripts/deploy.sh` — commit `ec21f5fb`
  (26/9/2026) đã thêm `ExpiresDefault "access plus 30 days"` cho ảnh qua `mod_expires`. Đợt này bổ
  sung THÊM khối `mod_headers`/`Cache-Control` tường minh theo đúng yêu cầu (không thay thế, không
  xoá khối `mod_expires` đã có — 2 cơ chế không xung đột, cùng giá trị 30 ngày).
- `components/exams/ContentHtml.tsx` — đã đọc kỹ cơ chế `hasMath()` + `loadKatex()` (chỉ
  `import("katex")` khi effect chạy VÀ nội dung có `$…$`) trước khi đụng vào bất cứ file nào dùng
  component này.
- `components/ui/Reveal.tsx` — đã đọc kỹ `PendingFallback` (timeout 4 giây) + `RevealErrorBoundary`
  trước khi làm gì — đợt này KHÔNG sửa file này, KHÔNG sửa `RevealMotion.tsx`.

## Số liệu JS ban đầu 2 trang mục tiêu (trước khi sửa)

| Trang | KB | Số chunk |
|---|---:|---:|
| `/lop-hoc/bai` | **1040,1** | 15 |
| `/kiem-tra/lam` | **1027,3** | 14 |

Chi tiết `/lop-hoc/bai` (15 chunk): 2 chunk riêng trang (1/66) — `33t5cyslwfeo5.js` 71,3 KB
(PracticeSession.tsx — chứa `practice_sessions`, `exam_attempts`…) và `1hk66gps0_3yb.js` 39,0 KB
(SampleQuestionsGrid.tsx — chứa `"revealed"`, `"checked"`…). 8 chunk nền dùng chung 66/66 trang.

Chi tiết `/kiem-tra/lam` (14 chunk): 1 chunk riêng trang (1/66) — `3xjt9iazxak7w.js` 97,6 KB
(ExamRunner.tsx — chứa `exam_question_results`, `student_alerts`…, gồm cả màn "done" tức
ExamResultSummary + ExamReviewPager vốn CHƯA lazy).

Không chunk nào có kích thước ~290 KB (KaTeX) hay ~139 KB (framer-motion) trong danh sách
`<script>` ban đầu của 2 trang — xác nhận lại phát hiện của `perf2/RESULT.md` §3: phần dư so với
mục tiêu <1000 KB là logic riêng của trang (PracticeSession/SampleQuestionsGrid/ExamRunner), không
phải KaTeX/framer.

## `npm run lint` gốc (trước khi sửa gì, đo trên đúng các file sẽ sửa — stash tạm 3 file đã sửa +
   cất riêng 2 file mới để loại trừ WIP không liên quan khỏi phép so sánh)

**8025 problems (175 errors, 7850 warnings)** — số này bao gồm rất nhiều WIP chưa commit của các
phiên khác trong cùng working tree (không phải lỗi do đợt này); dùng làm mốc so sánh "không tăng"
sau khi sửa.
