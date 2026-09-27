# RESULT-samplegrid — perf5/split-samplegrid (27/9/2026)

Nhánh độc lập trong đợt tối ưu tải trang thứ 5 (perf5), tách từ `main` tại commit `dd9bd74e`.
Việc được giao: tách `SampleQuestionsGrid` (mục "Bài tập mẫu") bằng `next/dynamic({ssr:false})` +
`LazyErrorBoundary`, xác nhận `/lop-hoc/bai` xuống dưới 1000 KB.

## Tóm tắt 5 dòng

1. Đã tách đúng pattern `f068cf95` (dynamic + LazyErrorBoundary cục bộ), file mới
   `components/lessons/SampleQuestionsGridLazy.tsx`, đổi 2 nơi dùng (`app/lop-hoc/bai/page.tsx`,
   `components/lessons/InlineLessonAccordion.tsx`) sang import bản Lazy — xác nhận bằng
   Network log: chunk `SampleQuestionsGrid`/`QuestionCard` chỉ tải SAU khi bấm mở mục, không nằm
   trong `<script>` ban đầu của trang.
2. **`/lop-hoc/bai` KHÔNG đạt <1000 KB**: 1038 KB → **1029 KB** (giảm chỉ ~9–10 KB, không phải
   ~34 KB như `perf4/RESULT.md` §7 ước tính) — xem mục 3 lý do.
3. Build sạch OK, `npx tsc --noEmit` 0 lỗi (trước/sau như nhau), `npm run lint` **68 problems (57
   errors, 11 warnings)** trước và sau — không tăng.
4. Test mắt qua Browser pane (`npx serve out -l 4012`, bài 2 — mục "Bài tập mẫu" có exam thật gắn
   sẵn): mở/đóng/mở lại nhiều lần, nội dung hiện đúng (chưa đăng nhập nên hiện đúng dòng "Đăng
   nhập để làm bài tập mẫu tự chấm." — không tạo tài khoản thật, đúng tiền lệ các đợt trước), 0
   lỗi console, không nhảy layout.
5. **Phát hiện quan trọng cần thầy biết**: trong lúc làm việc, một phiên Claude Code KHÁC chạy
   song song đã thao tác TRỰC TIẾP trên cùng thư mục worktree này (không phải một worktree khác)
   — thêm `components/system/ChunkErrorGuard.tsx` + sửa `app/layout.tsx`, và việc dùng chung
   `git stash`/`git stash pop` (stash là ngăn xếp DÙNG CHUNG giữa các worktree của cùng repo) đã
   làm mất tạm 2 dòng sửa của tôi giữa chừng — đã phát hiện qua `git diff` rỗng bất thường, soát
   lại và áp lại đúng 2 dòng, KHÔNG đụng gì tới file của phiên kia. Xem mục 6.

## 1. Vì sao chỉ giảm ~10 KB thay vì ~34 KB

`perf4/RESULT.md` ước tính phần dư ~34 KB của `/lop-hoc/bai` "toàn bộ là `QuestionCard.tsx` qua
`SampleQuestionsGrid.tsx`". Đo lại kỹ (so sánh 2 chunk riêng-trang trước/sau bằng cách đối chiếu
chuỗi định danh duy nhất trong `QuestionCard.tsx`, ví dụ `"motion-reduce:active:scale-100"`, và
kiểm tra số trang dùng mỗi chunk):

- **Trước**: 2 chunk riêng trang cho `/lop-hoc/bai` — 1 chunk 33,5 KB (chứa logic
  `SampleQuestionsGrid.tsx`, nhận diện qua chuỗi `"revealed"`) + 1 chunk 76,1 KB (chứa
  `QuestionCard.tsx` LẪN `LessonMasteryCard.tsx`/`LazyErrorBoundary`/`TopicPracticeModal` wrapper —
  không phải riêng `QuestionCard`).
- **Sau**: 2 chunk riêng trang còn lại — 30,9 KB (page.tsx, KHÔNG còn `"revealed"`) + 68,5 KB
  (LessonMasteryCard + Navbar/Footer icon + glue code `next/dynamic`, KHÔNG còn chuỗi định danh
  `QuestionCard`). `SampleQuestionsGrid.tsx` + `QuestionCard.tsx` chuyển hẳn sang chunk tải-sau
  riêng `214y-2spk6bjk.js` — chỉ **11 KB**, xác nhận bằng Network log chỉ tải chunk này SAU khi
  bấm mở mục "Bài tập mẫu" (không nằm trong danh sách `<script>` ban đầu).

Tức là việc tách **đúng kỹ thuật, đã loại đúng component khỏi bundle ban đầu** — nhưng
`QuestionCard.tsx` tự nó khi minify chỉ nặng khoảng 7–10 KB thực sự "độc quyền" (phần còn lại của
2 chunk cũ là `LessonMasteryCard`/`Navbar`/`Footer`/glue code của `next/dynamic`, những thứ đã có
sẵn từ trước, không đổi khi tách `SampleQuestionsGrid`) — nhỏ hơn nhiều so với con số 34 KB
`perf4/RESULT.md` suy luận (có thể do đo trên nhánh `main` đầy WIP song song, hash chunk khác,
hoặc gộp nhầm với phần khác). **Kết luận: đã làm đúng việc được giao, nhưng mục tiêu <1000 KB
KHÔNG đạt được chỉ bằng việc tách riêng `SampleQuestionsGrid`** — phần dư còn lại (~29 KB, từ 1029
xuống 1000) nằm ở chỗ khác (`LessonMasteryCard.tsx` hiển thị chính + `page.tsx` bản thân + phần
dùng chung Navbar/Footer cho trang này), ngoài phạm vi được giao (không tự ý mở rộng sang
`LessonMasteryCard`/`page.tsx`).

## 2. Pattern đã áp dụng

File mới `components/lessons/SampleQuestionsGridLazy.tsx` (bám đúng khuôn
`components/exams/ContentHtmlLazy.tsx` và `TopicPracticeModal` trong commit `f068cf95`):

```tsx
const SampleQuestionsGridLazyInner = dynamic(() => import("@/components/lessons/SampleQuestionsGrid"), {
  ssr: false,
  loading: () => <p className="text-sm text-slate-400">Đang tải bài tập mẫu…</p>,
});

function SampleQuestionsGridLazy(props: ComponentProps<typeof SampleQuestionsGridLazyInner>) {
  return (
    <LazyErrorBoundary
      fallback={<p className="text-sm text-slate-400">Không tải được bài tập mẫu. Thử tải lại trang.</p>}
    >
      <SampleQuestionsGridLazyInner {...props} />
    </LazyErrorBoundary>
  );
}
export default SampleQuestionsGridLazy;
```

`loading`/`fallback` dùng ĐÚNG nguyên văn 2 dòng chữ mà `SampleQuestionsGrid.tsx` tự có sẵn cho
trạng thái tải dữ liệu/lỗi của chính nó — chunk chưa về trông giống hệt lúc chunk đã về nhưng dữ
liệu Supabase chưa tải xong, không có skeleton lạ, không nhảy layout.

Đổi import ở 2 nơi dùng (giữ nguyên tên biến cục bộ `SampleQuestionsGrid`, chỉ đổi đường dẫn —
đúng cách `ContentHtmlLazy` đang được dùng ở 12 file khác trong repo):

- `app/lop-hoc/bai/page.tsx` dòng 12
- `components/lessons/InlineLessonAccordion.tsx` dòng 9

**Xác nhận đúng chỗ gọi chỉ mount khi mở mục** (không phải ẩn CSS): cả 2 nơi đều nằm trong
`{isOpen && (...)}` / `{open && (...)}` — khi đóng, cả cây JSX con (gồm `SampleQuestionsGrid`)
KHÔNG được React render ra, tức unmount thật, không phải `display:none`. Next/dynamic vì vậy tiết
kiệm được thật.

## 3. Đo kích thước (`perf/chunks-report.mjs`)

| Mốc | `/lop-hoc/bai` | Số chunk |
|---|---:|---:|
| Trước (gốc, `dd9bd74e`) | 1038 KB | 16 |
| Sau (đã tách, đo cô lập lúc 18:33, trước khi phiên khác thêm `ChunkErrorGuard`) | 1028 KB | 16 |
| Sau (đo lại lần cuối, working tree hiện tại — có thêm `ChunkErrorGuard.tsx`/`app/layout.tsx` của phiên khác, KHÔNG phải việc của tôi) | 1029 KB | 16 |

**KHÔNG đạt** mục tiêu <1000 KB — xem mục 1 để biết lý do và mục 5 việc cần thầy quyết.

## 4. Build / kiểu / lint

| Bước | Trước | Sau |
|---|---|---|
| `npx tsc --noEmit` | 0 lỗi | 0 lỗi |
| `npm run lint` | 68 problems (57 errors, 11 warnings) | 68 problems (57 errors, 11 warnings) — không tăng |
| `rm -rf .next out && npm run build` | OK | OK, 66 trang tĩnh |

(Số liệu lint đo trên đúng worktree này — SẠCH hơn nhiều so với 8025 problems ghi trong
`perf4/RESULT.md`, vì đó là đo trên `main` với rất nhiều WIP chưa commit của các phiên khác; ở đây
worktree mới tách, chỉ có đúng thay đổi của đợt này + `ChunkErrorGuard` của phiên song song.)

## 5. Test mắt (Browser pane, `npx serve out -l 4012`)

- `/lop-hoc/bai/?id=2` (Bài 1 — Sự chuyển thể, có mục "Bài tập mẫu" gắn đề thật `exam_ids=[88]`,
  tìm bằng cách quét `public/data/lessons/*.json` — lesson 49 dùng làm ví dụ ở các đợt trước lại
  KHÔNG có exam gắn cho "Bài tập mẫu" nên đổi sang lesson 2): danh sách 6 mục thu gọn hiện đúng,
  bấm mở "Bài tập mẫu" → hiện đúng "Đăng nhập để làm bài tập mẫu tự chấm." (chưa đăng nhập, không
  tạo tài khoản thật — đúng tiền lệ các đợt trước), đóng rồi mở lại 2 lần liên tiếp không lỗi.
  Network log xác nhận chunk `214y-2spk6bjk.js` (11 KB) chỉ được tải SAU khi bấm mở mục, không nằm
  trong danh sách `<script>` ban đầu của trang. `read_console_messages(onlyErrors:true)`: rỗng ở
  mọi bước.
- `/lop-hoc` (nơi dùng `InlineLessonAccordion.tsx`, nơi thứ 2 đổi import): tải đúng, 0 lỗi console
  — không đi sâu test accordion ở đây vì đây là trang phụ (đã <1000 KB từ trước, 985 KB, không
  phải trang mục tiêu), component dùng lại y hệt bản đã kiểm ở `/lop-hoc/bai`.
- **Hạn chế**: không tự test được luồng có tài khoản học sinh thật (chấm điểm, chọn đáp án, xem
  lời giải) — không tạo tài khoản production trong phiên này, đúng tiền lệ.

## 6. Sự cố phiên chạy song song trong CÙNG thư mục worktree (ghi nhận, không phải lỗi của tôi)

Trong lúc đo lại (khoảng 18:33–18:37), phát hiện `git status` bất ngờ có `app/layout.tsx` (modified)
và `components/system/` (untracked, chứa `ChunkErrorGuard.tsx`) — KHÔNG phải do tôi tạo. Đối chiếu
timestamp (`BUILD_ID` mới nhất trùng giờ các file này xuất hiện: 18:35:48) xác nhận một phiên Claude
Code KHÁC (đúng như lưu ý trong yêu cầu: "nhánh khác đang làm việc" logic bắt lỗi chunk-load-failure
ở mức root) đang thao tác TRỰC TIẾP trên cùng đường dẫn thư mục
`/Users/MAC/Projects/thachlab/.claude/worktrees/perf5-split-samplegrid` — không phải một worktree
khác biệt như mô tả trong yêu cầu ban đầu, mà là CÙNG một thư mục vật lý (browser pane cũng cho
thấy tab của tôi lẫn với tab cổng `3011`/`4011` của phiên kia).

Vì `git stash` dùng chung 1 ngăn xếp `refs/stash` cho MỌI worktree của cùng repository (không
cô lập theo từng worktree), khi tôi tạm `git stash` (để đo bản gốc so sánh) rồi `git stash pop`,
2 dòng sửa import của tôi biến mất khỏi `git diff` dù lệnh pop báo thành công — nghi do phiên kia
cũng thao tác `git stash`/build gần như đồng thời, chồng lấn lên đúng lúc đó. Phát hiện qua
`git diff --stat` bất thường (rỗng), kiểm tra lại bằng `grep`, và ÁP LẠI TRỰC TIẾP 2 dòng sửa bằng
Edit (không dùng `git stash` nữa từ lúc đó) — xác nhận đúng nội dung, không đụng
`app/layout.tsx`/`components/system/` của phiên kia. `git stash list` hiện còn 1 entry trùng nội
dung 2 dòng sửa của tôi (dư thừa, vô hại vì tôi đã áp lại trực tiếp) — CHƯA xoá, để tránh rủi ro
đụng vào ngăn xếp dùng chung thêm lần nữa; thầy có thể `git stash drop` thủ công nếu muốn dọn.

**Bài học cho lần sau**: không dùng `git stash`/`git stash pop` khi nghi ngờ có phiên khác đang
chạy trong CÙNG thư mục (không chỉ CÙNG repo) — nên dùng `git diff > /tmp/x.patch` +
`git checkout -- <file>` + `git apply /tmp/x.patch` (thao tác trên đúng file, không đụng ngăn xếp
dùng chung) nếu cần build bản "gốc" để so sánh.

## 7. Phạm vi — xác nhận KHÔNG đụng

- KHÔNG đụng `components/ui/Reveal.tsx`, `app/error.tsx`.
- KHÔNG đụng `components/exams/ExamRunner.tsx` hay logic nộp bài/chấm điểm.
- KHÔNG đụng `app/layout.tsx`/`components/system/ChunkErrorGuard.tsx` (của phiên song song khác —
  xem mục 6) — 2 file này CHƯA được `git add`/commit trong đợt này, cố tình để nguyên cho phiên kia
  tự commit.
- KHÔNG `git push`, KHÔNG tạo PR, KHÔNG merge, KHÔNG đụng branch/worktree khác.

## 8. File đã sửa (commit trong đợt này)

- `app/lop-hoc/bai/page.tsx` (đổi 1 dòng import)
- `components/lessons/InlineLessonAccordion.tsx` (đổi 1 dòng import)
- `components/lessons/SampleQuestionsGridLazy.tsx` (mới)
- `perf5/RESULT-samplegrid.md` (mới, file này)

## 9. Việc cần thầy quyết

| # | Việc | Đề xuất |
|---|---|---|
| 1 | `/lop-hoc/bai` còn ~29 KB nữa mới đạt <1000 KB, nằm ở `LessonMasteryCard.tsx` (hiển thị chính, không phải modal) + `page.tsx` bản thân + phần Navbar/Footer riêng trang — ngoài phạm vi được giao (chỉ `SampleQuestionsGrid`). | Cần một đợt riêng nếu muốn đạt <1000 KB tuyệt đối; hoặc chấp nhận ~1029 KB (đã giảm so với 1038 KB gốc, đúng hướng dù chưa đạt mốc tròn). |
| 2 | `git stash@{0}` dư thừa (nội dung trùng 2 dòng sửa đã áp trực tiếp) còn trong ngăn xếp dùng chung. | Vô hại, có thể `git stash drop` thủ công khi thầy rảnh, không vội. |
| 3 | Phiên song song đang sửa `app/layout.tsx`/`components/system/ChunkErrorGuard.tsx` ngay trong CÙNG thư mục worktree này (không phải worktree riêng như kỳ vọng) — rủi ro tái diễn nếu có đợt sau dùng lại đúng thư mục này trước khi phiên kia commit/dọn xong. | Thầy nên xác nhận với phiên kia đã commit xong chưa trước khi giao việc mới vào đúng thư mục `perf5-split-samplegrid`. |
