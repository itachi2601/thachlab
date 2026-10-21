# RESULT5 — chunk-error (27/9/2026)

Nhánh `perf5/chunk-error`, tách từ `main` tại `dd9bd74e`. Một trong 3 nhánh độc lập của đợt
tối ưu tải trang thứ 5 (perf5) — việc này lo lớp bắt lỗi tải chunk nằm ngoài tầm với của React
Error Boundary.

## 1. Lỗi gốc là gì

`components/ui/LazyErrorBoundary.tsx` (comment "GIỚI HẠN") và `perf4/RESULT.md` §6/"ĐỢT SAU" đã
ghi nhận: khi 1 chunk JS runtime của Turbopack tải lỗi, lỗi `ChunkLoadError` đôi khi xảy ra NGAY
TRONG `Promise.all` của cơ chế nạp chunk (`turbopack-*.js`), tức là một unhandled promise
rejection ở tầng trình duyệt — không đi qua đường render/commit của React nên không có
`getDerivedStateFromError` nào (kể cả `LazyErrorBoundary` bọc đúng vị trí, kể cả route-level
error boundary `app/error.tsx`) bắt được. Các báo cáo trước (`perf2/RESULT.md` §6,
`perf4/RESULT.md` §6) đã tái hiện được màn hình trắng "Uncaught ChunkLoadError" kiểu này trên
trang chủ khi xoá chunk `RevealMotion` — nhưng cùng các báo cáo đó cũng ghi nhận hành vi này
**không ổn định giữa các lần build** (`perf4/RESULT.md` mục "ĐỢT SAU" tái hiện lại chính kịch bản
đó và lại thấy `LazyErrorBoundary` bắt được cục bộ, ngược với lần trước).

## 2. Cách tái hiện đã thử (bước 1, trước khi vá)

Build tĩnh (`rm -rf .next out && npm run build`), serve `out/` bằng `npx serve out -l 4011`
(chạy nền), tìm chunk chứa `RevealMotion` bằng `grep -l "prefers-reduced-motion"` /
`grep -l "useReducedMotion"` trong `out/_next/static/chunks/`, xoá thử, mở **tab hoàn toàn mới**
mỗi lần, quan sát bằng Browser pane (`read_console_messages`, `get_page_text`, screenshot).

Đã thử 3 tổ hợp xoá trên trang chủ `/`:

| Tổ hợp xoá | Kết quả |
|---|---|
| Chỉ chunk component nhỏ (753 byte, chứa JSX thật của `RevealMotion`) | Console có `ChunkLoadError: Failed to load chunk .../1wdh1lu7tm9r1.js from module 12036 ... at async Promise.all (index 0)`, lặp lại nhiều lần — nhưng **trang render đầy đủ, không trắng** |
| Chỉ 1 trong 2 bản chunk framer-motion trùng (~139 KB, `module 69790`) | `ChunkLoadError ... from module 69790 ... at async Promise.all (index 1)` — **không trắng**, trang render đủ |
| Cả 3 chunk cùng lúc (2 bản framer-motion + chunk component) | Cùng lúc nhiều `ChunkLoadError` — **vẫn không trắng**, `get_page_text` xác nhận đủ mọi section (AboutFounder, Features, Testimonials…) |

**Không tái hiện được màn trắng trên build hiện tại** (nhánh từ `dd9bd74e`) — khớp với phát hiện
"ĐỢT SAU" của `perf4/RESULT.md`: `LazyErrorBoundary` cục bộ trong `Reveal.tsx` đã bắt được lỗi
này ở build hiện tại. Đã thử thêm 1 trang test tạm không bọc `LazyErrorBoundary`
(`app/test-chunk-boundary/page.tsx` + `components/system/TestDummyChunk.tsx`, đã XOÁ trước khi
commit, không có trong diff cuối — đúng tiền lệ `perf4/RESULT.md`): xoá chunk của component không
được bọc boundary cục bộ → **rơi đúng xuống `app/error.tsx`** (route-level error boundary của Next
App Router vẫn bắt được), không trắng, không cần `ChunkErrorGuard` can thiệp.

**Kết luận về bước 1**: trên chính xác build hôm nay, không ép được lỗi thoát hẳn ra ngoài MỌI
React Error Boundary (kể cả `app/error.tsx`) — nhất quán với việc `perf2`/`perf4` đã tự ghi nhận
hành vi này KHÔNG ổn định giữa các lần build (phụ thuộc thời điểm lỗi xảy ra trong tiến trình
hydrate). Vì lớp bảo vệ được yêu cầu (`window.addEventListener`) chỉ có tác dụng đúng cho đúng
kịch bản "thoát khỏi mọi boundary", đã xác nhận bằng thực nghiệm trực tiếp (mục 4) rằng cơ chế mới
thêm hoạt động đúng khi được kích hoạt, thay vì chỉ dựa vào việc ép được crash thật trên build này.

Thông điệp lỗi THẬT quan sát được (dùng để xây pattern nhận diện, không đoán):
```
ChunkLoadError: Failed to load chunk /_next/static/chunks/<hash>.js from module <id>
    at .../turbopack-<hash>.js:1:6391
    at async Promise.all (index N)
```

## 3. Đã vá gì

Thêm `components/system/ChunkErrorGuard.tsx` (client component, không render gì —
`return null`) và mount trong `app/layout.tsx` (root layout, áp dụng cho MỌI route vì đây là
layout gốc duy nhất bọc `<body>`), đặt trước `<ToastProvider>` để chạy sớm nhất có thể.

```tsx
window.addEventListener("error", onError);
window.addEventListener("unhandledrejection", onRejection);
```

- Nhận diện: message chứa 1 trong các chuỗi `"ChunkLoadError"`, `"Failed to load chunk"`,
  `"Loading chunk"` (2 chuỗi đầu khớp trực tiếp thông điệp thật quan sát được ở mục 2;
  `"Loading chunk"` giữ thêm phòng khi runtime đổi cách viết; `"Failed to fetch dynamically
  imported module"` — thông điệp gốc trình duyệt Firefox/Safari dùng cho `import()` lỗi khi không
  đi qua wrapper `ChunkLoadError` của bundler).
- Xử lý: `sessionStorage.setItem("thachlab-chunk-reload", "1")` rồi `location.reload()` — chỉ 1
  lần. Nếu đã có flag (đã reload rồi mà lỗi vẫn còn) → không làm gì thêm, để rơi xuống
  `app/error.tsx` (nếu lỗi đi qua React) hoặc tự nó dừng lại (không vòng lặp).
- `sessionStorage` bị chặn (ẩn danh nghiêm ngặt…) → bắt lỗi, không reload (thà không tự động còn
  hơn lặp vô hạn).
- Không đụng `Reveal.tsx`, `app/error.tsx`, `LazyErrorBoundary.tsx` — cả 3 giữ nguyên 100%.

## 4. Kiểm chứng cơ chế hoạt động đúng (vì không ép được crash thật trên build này)

Vì bước 1 không tái hiện được đúng kịch bản "thoát mọi boundary" trên build hiện tại, đã kiểm
trực tiếp `ChunkErrorGuard` bằng cách dispatch thật `ErrorEvent`/`unhandledrejection` (code thật
đang chạy trong trang thật, không mock) qua Browser pane:

| Test | Cách làm | Kết quả |
|---|---|---|
| Bắt đúng pattern + reload đúng 1 lần | `window.dispatchEvent(new ErrorEvent("error", {error: new Error("ChunkLoadError: Failed to load chunk .../testhash123.js from module 99999")}))` trên tab `/` sạch | `sessionStorage` set `"1"` ngay, biến global đánh dấu trước-dispatch bị mất sau đó (`window.__testMarker` undefined) → xác nhận trang đã RELOAD thật |
| Không lặp lại reload lần 2 | Dispatch lại đúng lỗi đó sau khi flag đã set | Biến đánh dấu mới (`window.__testMarker2`) vẫn còn nguyên sau 800ms → **không reload lần 2**, đúng thiết kế |
| Không báo động giả (false positive) | Dispatch `ErrorEvent` với message không liên quan ("TypeError: something unrelated broke") | `sessionStorage` vẫn `null`, không reload |
| `unhandledrejection` cũng hoạt động | `Promise.reject(new Error("ChunkLoadError: ... from module 55555"))` (promise reject thật, không dispatch tay) | Script bị cắt ngang do trang điều hướng lại (navigated) — xác nhận reload đã kích hoạt qua đúng đường `unhandledrejection` |

Kết luận: cơ chế hoạt động đúng như thiết kế — sẵn sàng cho đúng kịch bản mà `perf2`/`perf4` đã
từng quan sát thấy trên các build khác (lỗi thoát khỏi mọi React Error Boundary), mà không can
thiệp/gây reload thừa khi lỗi đã được `LazyErrorBoundary`/`app/error.tsx` bắt đúng cách (xác nhận ở
mục 2: cả 3 tổ hợp xoá chunk RevealMotion đều để `sessionStorage` flag ở trạng thái `null` — guard
không hề kích hoạt vì không cần).

## 5. Kiểm lại bước 3 (build sạch lại, xoá lại đúng chunk RevealMotion + 1 chunk khác)

Build lại `out/` từ đầu sau khi thêm `ChunkErrorGuard`, serve lại cổng `4011`, xoá lại đúng 3 chunk
liên quan `RevealMotion` (2 bản framer-motion trùng + chunk component nhỏ) cùng lúc, tab hoàn toàn
mới:

- **Không crash trắng** — trang render đủ nội dung, `LazyErrorBoundary` cục bộ vẫn bắt được như
  trước (không đổi hành vi so với trước khi vá).
- `sessionStorage` flag `thachlab-chunk-reload` = `null` sau khi load — `ChunkErrorGuard` không
  kích hoạt (đúng, vì không cần).
- Thử thêm 1 chunk KHÁC không phải `RevealMotion`: dựng trang test tạm
  `app/test-chunk-boundary/page.tsx` với 1 `next/dynamic()` KHÔNG bọc `LazyErrorBoundary` (mô
  phỏng "quên bọc boundary"), xoá chunk tương ứng, tab mới → rơi đúng xuống `app/error.tsx` (route
  error boundary bắt được ở tầng route, không cần `ChunkErrorGuard`) — xác nhận cơ chế 3 lớp
  (`LazyErrorBoundary` cục bộ → `app/error.tsx` route-level → `ChunkErrorGuard` window-level) hoạt
  động đúng thứ tự ưu tiên, lớp ngoài cùng chỉ kích hoạt khi 2 lớp trong không bắt được. Đã xoá 2
  file test tạm (`app/test-chunk-boundary/page.tsx`, `components/system/TestDummyChunk.tsx`)
  trước khi commit — không có trong diff.

## 6. Số liệu tsc/lint — gốc vs sau khi sửa

Đo trên **đúng commit `dd9bd74e`** (không dùng `git stash` — xem mục 7 về sự cố suýt xảy ra):

| | tsc --noEmit | lint |
|---|---|---|
| Gốc (`dd9bd74e`, chưa sửa) | 0 lỗi | 68 problems (57 errors, 11 warnings) |
| Sau khi sửa (thêm `ChunkErrorGuard.tsx` + mount trong `layout.tsx`) | 0 lỗi | 68 problems (57 errors, 11 warnings) |

Không tăng. `rm -rf .next out && npm run build` xanh cả trước/sau (66 trang tĩnh).

Smoke test mắt + console khi mạng bình thường (không giả lập lỗi chunk), tab sạch mỗi lần:

| Trang | Kết quả |
|---|---|
| `/` | Render đủ, 0 lỗi console, `sessionStorage` flag không bị set |
| `/lop-hoc/bai/?id=49` | Đúng bài "Bài 4. Độ dịch chuyển và quãng đường đi được", đủ mục Lý thuyết/Bài tập mẫu/Luyện tập, 0 lỗi console |
| `/kiem-tra/lam/?id=118` | Đúng màn "Em cần đăng nhập để sử dụng tính năng này" (không tạo tài khoản thật), 0 lỗi console |
| `/` ở 375px (mobile) | Bố cục không vỡ, không lỗi console |

## 7. Sự cố ngoài phạm vi kỹ thuật — `git stash` dùng chung stash stack giữa các worktree

Khi đo baseline lint bằng `git stash -u` / `git stash pop`, một phiên khác (nhánh
`perf5/split-samplegrid`, worktree riêng) cũng đang thao tác `git stash` cùng lúc — `git stash`
dùng CHUNG 1 stash stack cho toàn repo (không tách theo từng worktree, khác branch). Lệnh
`git stash pop` của tôi đã pop nhầm đúng stash MỚI NHẤT tại thời điểm đó — của phiên kia
(`app/lop-hoc/bai/page.tsx`, `components/lessons/InlineLessonAccordion.tsx` trỏ sang
`SampleQuestionsGridLazy`), không phải của tôi.

Đã xử lý ngay khi phát hiện (trước khi coordinator kịp cảnh báo):
1. `git checkout --` 2 file lạ đó khỏi working tree của mình.
2. Tìm lại đúng stash của phiên kia qua `git fsck --no-reflog` (dangling commit sau khi bị
   "Dropped"), `git stash store` để trả nó về lại stash list — không drop, không mất.
3. Tìm lại đúng stash CỦA MÌNH (dangling commit khác cùng cơ chế, message "WIP on
   perf5/chunk-error...") rồi `git stash apply <hash>` — đối chiếu nội dung khớp 100% bản đã viết
   (`app/layout.tsx` +2 dòng, `components/system/ChunkErrorGuard.tsx` nguyên vẹn).
4. Từ đó về sau đo baseline bằng cách copy file ra `/tmp` + `git checkout -- app/layout.tsx` thay
   vì `git stash`, không dùng `git stash` thêm lần nào nữa trong phần còn lại của việc.

Đã xác nhận lại bằng `git status`/`git diff --stat` trước khi commit: chỉ đúng 2 thay đổi của việc
này (`app/layout.tsx`, `components/system/ChunkErrorGuard.tsx`), `git stash list` còn đúng 2 mục
không phải của mình, không đụng tới.

## 8. File đã sửa

- `app/layout.tsx` — thêm import + mount `<ChunkErrorGuard />` (2 dòng).
- `components/system/ChunkErrorGuard.tsx` — mới.
- `perf5/RESULT-chunk-error.md` — báo cáo này.

Không đụng `components/lessons/SampleQuestionsGrid.tsx`, không đụng
`components/exams/ExamRunner.tsx` hay bất kỳ file exam nào khác, không đụng
`components/ui/Reveal.tsx`/`LazyErrorBoundary.tsx`/`app/error.tsx`.

## 9. Bất thường khác cần thầy biết

1. **Không tái hiện được màn trắng thật trên build hôm nay** dù đã thử 3 tổ hợp xoá chunk
   `RevealMotion` khác nhau — khác với 1 số báo cáo trước (`perf2`, `perf4` lần đầu). Đã đối chiếu
   kỹ và xác nhận đây là hành vi timing-sensitive đã được chính `perf4/RESULT.md` ghi nhận trước
   đó (không phải lỗi thao tác của tôi). `ChunkErrorGuard` được thêm làm lưới dự phòng cho đúng
   kịch bản đó dựa trên bằng chứng lịch sử + kiểm chứng cơ chế trực tiếp (mục 4), không dựa vào
   việc ép crash thật hôm nay.
2. **Sự cố `git stash` dùng chung giữa các worktree** (mục 7) — đã xử lý xong, không mất dữ liệu
   của phiên nào, nhưng đáng lưu ý cho các đợt việc song song sau này: KHÔNG dùng `git stash` khi
   nhiều worktree cùng hoạt động trên 1 repo, dùng cách khác (copy file ra ngoài, hoặc
   `git worktree add` riêng để đo baseline).
