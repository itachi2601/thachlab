# RESULT3 — kiểm tra ĐỘC LẬP đợt tối ưu font lần 3 (9/2026)

Kiểm bởi phiên riêng, không phải người viết commit `11aed966` (cha: `b6f224be`, 4 file:
`app/fonts.ts`, `components/rank/rank-fonts.ts` mới, `TierName.tsx`, `TierLadder.tsx`). Build
sạch 2 bên trong 2 git worktree riêng (`.claude/worktrees/perf3-before` tại `b6f224be`,
`.claude/worktrees/perf3-after` tại `11aed966`, `git merge-base --is-ancestor` xác nhận đúng
quan hệ cha–con) — không đụng working tree chính (đang có ~15 file WIP không liên quan của
phiên khác). Copy `.env.local` sang cả 2 worktree, `npm install` + `rm -rf .next out && npm run
build` mỗi bên → `manifest.json` có 116 bài học thật (không rỗng), serve bằng `npx serve out`
trên 2 cổng riêng (3510 = trước, 3511 = sau, không đụng 3000/4173 đang dùng bởi phiên khác).

**Tóm tắt 6 dòng**
1. Số liệu file/KB font trang chủ đo lại **khớp chính xác** báo cáo của người làm: **trước 20
   file/323 KB → sau 17 file/262 KB**. Mục tiêu **<10 file/<170 KB** — **KHÔNG đạt**, đúng như
   người làm đã tự nhận, không có gì phóng đại.
2. Xác nhận đúng cơ chế: 3 file biến mất khỏi trang chủ (9+38+15 = 62 KB) là Cinzel+Playfair,
   và đúng 3 file đó vẫn xuất hiện trên `/lop-hoc/xep-hang` (dù không đăng nhập được, do
   `page.tsx` import tĩnh `RankPage`→`TierName`→`rank-fonts` nên next/font preload theo bundle
   route, không theo điều kiện render). Không phát hiện lỗi hiển thị nào ở 4 trang chụp thử.
3. Phát hiện phụ (người làm không nói tới): **lợi ích không chỉ riêng trang chủ** — trang bài
   học `/lop-hoc/bai/?id=49` (không dùng component rank) cũng giảm từ 20/355 KB → 17/293 KB,
   vì trước đây Cinzel/Playfair nạp ở root layout nên preload trên **mọi** trang, không chỉ `/`.
4. `tsc --noEmit` 0 lỗi cả 2 bên. `npm run lint` build sạch (không WIP): **64 problems (54 lỗi,
   10 cảnh báo) — giống hệt nhau ở cả trước và sau** → xác nhận không tăng lỗi lint do commit
   này (con số 8024 người làm báo là đo trên working tree chính có WIP, không phải commit này).
5. Lighthouse mobile (máy dùng chung, xem lưu ý ở §5): trang chủ cải thiện rõ **80→92 điểm,
   FCP/LCP 3,8s→2,7s**; trang bài học gần như không đổi (71→72, LCP 6,2s→5,9s) vì phần chặn
   render của trang này không phải do 3 file font Cinzel/Playfair (chỉ ~62 KB trong tổng ~1 MB+
   JS/font của trang).
6. Đánh giá riêng về quyết định "bỏ qua tách Be Vietnam Pro 800": **hợp lý về rủi ro/công sức**,
   nhưng lý do kỹ thuật người làm nêu là đúng — xem §6, kèm gợi ý cho đợt sau (không sửa code).
   Không có migration SQL nào trong đợt này.

## 1. Build / kiểu / lint (2 worktree, so sánh trực tiếp)

| Bước | Trước (`b6f224be`) | Sau (`11aed966`) |
|---|---|---|
| `npm install` + `rm -rf .next out && npm run build` | OK, 116 bài học (Supabase thật, không rỗng) | OK, 116 bài học |
| `npx tsc --noEmit` | OK, 0 lỗi | OK, 0 lỗi |
| `npm run lint` | **64 problems (54 lỗi, 10 cảnh báo)** | **64 problems (54 lỗi, 10 cảnh báo)** — giống hệt |

Số 64 (không phải 63 như `perf2/RESULT.md` baseline hồi trước) — lệch 1, nhiều khả năng do các
commit khác giữa 2 lần đo (không liên quan tới font), không phải do commit `11aed966` vì cả
trước/sau ở đây đều ra đúng 64. Không đối chiếu tới từng dòng lỗi cụ thể (không cần thiết vì số
khớp nhau tuyệt đối).

## 2. Font trang chủ — đúng phép đo người làm dùng

```js
performance.getEntriesByType('resource').filter(e => /\.woff2/.test(e.name))
  .map(e => ({ f: e.name.split('/').pop(), KB: Math.round(e.decodedBodySize/1024) }))
```

| | Số file | Tổng KB | Đạt <10 file/<170 KB? |
|---|---:|---:|---|
| Trước (port 3510) | **20** | **323** (tổng cộng dồn từng file ra 324, lệch do làm tròn) | — |
| Sau (port 3511) | **17** | **262** | **KHÔNG đạt** (dư 7 file, 92 KB) |

Khớp **chính xác** con số người làm tự báo (20/323 → 17/262). Mục tiêu <10 file/<170 KB **không
đạt** — không làm tròn hay nói giảm cho đẹp, người làm cũng đã tự nhận đúng như vậy.

## 3. Xác nhận Cinzel/Playfair biến mất khỏi trang chủ

Đối chiếu danh sách 20 file (trước) với 17 file (sau) theo tên hash: **3 file biến mất đúng
bằng hiệu 20−17**:

| Hash file | KB | Trước | Sau |
|---|---:|---|---|
| `14e23f9b59180572-*.woff2` | 9 | có | **không** |
| `2a65768255d6b625-*.woff2` | 38 | có | **không** |
| `fd5073be3e923c20-*.woff2` | 15 | có | **không** |

Tổng 62 KB (9+38+15), khớp đúng 323−262≈61–62 KB chênh lệch. 3 file này đổi trạng thái
`preload` (đuôi `.p.` trong tên) — đúng dấu hiệu của font Cinzel (1 weight 700) + Playfair
Display (2 weight 600/700, nhưng chỉ có 2 file — nhiều khả năng 1 subset latin+vietnamese gộp
thành ít file hơn 3 weight khai báo, next/font tự gộp subset khi trùng unicode-range). File
`19087af2bdec32b5` (JetBrains Mono, 21 KB) vẫn còn ở cả 2 bên nhưng **đổi từ preload sang không
preload** — đúng thay đổi `preload:false` trong commit.

## 4. `/lop-hoc/xep-hang` vẫn tải Cinzel/Playfair

Không có tài khoản test (giống hạn chế `perf2/RESULT.md` §5) → trang chỉ hiện "Em cần đăng nhập
để sử dụng tính năng này." ở cả 2 bên, không xem được `TierName`/`TierLadder` render thật
(không chụp được ảnh 2 kiểu chữ Anh-lớn/Việt-nhỏ như yêu cầu mục 4 — hạn chế môi trường, không
phải lỗi code).

Tuy vậy vẫn xác nhận được phần quan trọng: đo `performance.getEntriesByType('resource')` trên
route này (dù chưa đăng nhập) cho ra đúng 3 hash file Cinzel/Playfair ở mục 3 — vì
`app/lop-hoc/xep-hang/page.tsx` là `"use client"` và import tĩnh `RankPage` (→`TierName`→
`rank-fonts.ts`) ngay ở đầu file, nên next/font gắn `<link rel=preload>` theo **bundle của cả
route** (phân tích tĩnh lúc build), không phụ thuộc `RequireAuth` có mount `<Content/>` hay
không lúc runtime. Nghĩa là: đúng ý đồ — chỉ route nào có khả năng render component rank mới
tải 2 font này, kể cả khi người dùng đó cuối cùng bị chặn đăng nhập.

## 5. Ảnh chụp 390px — 4 trang, trước/sau

Lighthouse + browser pane chạy trên máy dùng chung (nhiều phiên Claude khác), số tuyệt đối có
thể nhiễu — nhưng phép so sánh trước/sau trong CÙNG 1 lần chụp/đo thì đáng tin.

| Trang | Kết quả |
|---|---|
| `/` | **Giống hệt** — header, hero, 2 thẻ chọn hệ, khối "Tại sao mọi thứ lại dao động?" cùng font/độ đậm, cùng bố cục. |
| `/lop-hoc/bai/?id=49` | **Giống hệt** — tiêu đề "Bài 4. Độ dịch chuyển...", 5 công thức `.katex` (đếm bằng `document.querySelectorAll('.katex').length` = 5 cả 2 bên); chụp cận cảnh 1 công thức (`x = \overline{OM}`) render đúng, không vỡ, không đổi kiểu chữ. |
| `/lop-hoc/xep-hang/` | Cả 2 bên đều chặn ở màn "Em cần đăng nhập" (không có tài khoản test) — **không đủ điều kiện so sánh hiển thị 2 kiểu chữ tên bậc**, xem §4. |
| `/kiem-tra/lam/?id=118` | Cả 2 bên đều chặn ở màn "Em cần đăng nhập để sử dụng tính năng này." — không xem được nội dung đề/công thức thật. Dùng `/lop-hoc/bai/?id=49` (mục trên) làm trang có công thức thay thế, đã xác nhận bằng mắt trước khi chụp. |

Không có lỗi console (`read_console_messages onlyErrors` rỗng) ở cả 4 lượt kiểm.

## 6. Lighthouse mobile (Chrome headless, throttle mô phỏng mặc định)

**Lưu ý môi trường:** máy đo là máy chia sẻ với nhiều phiên Claude khác (nhiều worktree/agent
đang chạy song song lúc đo, xem `git worktree list` ở đầu phiên) — số tuyệt đối có thể nhiễu vài
trăm ms, giống lưu ý `perf2/RESULT.md` §2. Đọc kết quả theo hướng "cải thiện rõ hay không", không
lấy số thập phân làm chuẩn tuyệt đối.

| Trang | Score (trước→sau) | FCP | LCP | TBT | Speed Index |
|---|---:|---:|---:|---:|---:|
| `/` | 80 → **92** | 3,8s → **2,7s** | 3,8s → **2,7s** | 60ms → 60ms | 3,8s → **2,7s** |
| `/lop-hoc/bai/?id=49` | 71 → 72 | 2,3s → 2,5s | 6,2s → 5,9s | 100ms → 40ms | 5,2s → 5,1s |

Trang chủ cải thiện rõ và nhất quán trên mọi chỉ số chính (điểm, FCP, LCP, Speed Index đều giảm
~1,1s) — đúng hướng kỳ vọng của đợt tối ưu, dù chưa đạt mốc <10 file/<170 KB. Trang bài học gần
như đi ngang (71→72, LCP giảm nhẹ 0,3s, TBT giảm) — hợp lý, vì phần "nặng" của trang này không
phải 3 file Cinzel/Playfair (chỉ 62 KB) mà là JS + nội dung bài học (đã ghi nhận ở `perf/` và
`perf2/RESULT.md` — không phải phạm vi đợt font lần này).

## 7. Đánh giá quyết định "bỏ tách Be Vietnam Pro 800"

Đọc `app/globals.css` dòng 860 (`.hub-tile { ... font-family: var(--font-display), sans-serif;
font-weight: 800; }`) và dòng 918 (`.cnc-live-hero h2 { font-family: var(--font-display); ...
font-weight: 900; }`), và `components/rank/ClassRankBoard.tsx` dòng 72
(`className="font-display ... font-black ..."` — Tailwind `font-black` = `font-weight: 900`).

Xác nhận đúng cơ chế người làm mô tả: next/font sinh 1 tên `font-family` nội bộ (hash) riêng cho
**mỗi lần gọi** `Be_Vietnam_Pro({...})`. Nếu tách weight 800 ra một instance font riêng (biến CSS
mới, ví dụ `--font-display-black`), thì `var(--font-display)` gốc chỉ còn 400/600/700 — 3 phần tử
trên (`.hub-tile`, `.cnc-live-hero h2`, `ClassRankBoard` `font-black`) đang xin weight 800/900
nhưng KHÔNG đổi sang biến mới sẽ bị trình duyệt khớp về **700** (nhẹ hơn) thay vì 800 như hiện
tại — đổi giao diện thật, đúng như người làm lo ngại. `/lop-hoc/xep-hang` (chứa
`ClassRankBoard`) nằm trong bộ ảnh chụp bắt buộc — nên nếu làm ẩu sẽ bị phát hiện ngay ở đợt kiểm
tiếp theo.

**Đánh giá: quyết định bỏ qua là hợp lý** cho phạm vi hẹp của commit này (chỉ đổi rank fonts,
không đụng Be Vietnam Pro). Gợi ý cho đợt sau (không sửa code, chỉ ghi nhận): nếu vẫn muốn tách
weight 800 để giảm tải cho các trang không cần nó, cách an toàn hơn là **cập nhật luôn 3 điểm
dùng weight 800/900** (`.hub-tile`, `.cnc-live-hero h2`, `ClassRankBoard.tsx`) sang biến font mới
trong CÙNG 1 commit — quét đủ bằng `grep -rn "font-display" app/globals.css components --include="*.tsx" --include="*.css"` rồi lọc `900|800|font-black` (đã chạy thử, chỉ ra đúng 3 chỗ, không
sót). Ngoài ra: `.hub-tile`/`.cnc-live-hero h2`/`ClassRankBoard` đều KHÔNG xuất hiện trên trang
chủ `/` (đã kiểm — trang chủ không có class `hub-tile`/`cnc-live-hero`/`ClassRankBoard`) nên tách
weight 800 ra khỏi root layout sẽ không giúp gì thêm cho mục tiêu <170 KB của trang chủ — cơ hội
giảm KB rõ hơn nằm ở Inter latin-ext (83 KB, 1 file, ký tự thật đang hiển thị) mà người làm đã
đúng khi kết luận không thể bỏ mà không đổi giao diện.

## 8. Dọn dẹp

Đã `git worktree remove` cả 2 worktree tạm (`perf3-before`, `perf3-after`), dừng 2 server
`npx serve` ở cổng 3510/3511. Không có file/tiến trình nào còn sót từ đợt kiểm này.

## 9. Việc còn lại

1. Mục tiêu <10 file/<170 KB font trang chủ **vẫn chưa đạt** (còn 17 file/262 KB) — phần dư chủ
   yếu là ký tự thật (Inter latin-ext 83 KB, vài file Be Vietnam Pro/JetBrains Mono khác) mà
   người làm đã xác nhận không thể bỏ mà không đổi giao diện. Không có hướng giảm thêm rõ ràng
   trong phạm vi "không đổi giao diện".
2. Chưa xác nhận được bằng mắt 2 kiểu chữ (Cinzel/Playfair) thật sự hiển thị đúng trên
   `/lop-hoc/xep-hang` vì không có tài khoản test — chỉ xác nhận được bằng phân tích network/code
   (§4). Thầy tự xem lại trang này sau khi deploy nếu cần chắc chắn 100%.
3. Gợi ý kỹ thuật not-urgent ở §7 (gộp việc tách Be Vietnam Pro 800 nếu muốn làm ở đợt sau).

**Không có migration SQL nào trong đợt này** — thuần frontend (font), không có file mới trong
`supabase/migrations/`. Sau khi merge: chạy `scripts/deploy.sh` rồi đo lại PageSpeed trên site
thật (giống cách `docs/STATE.md` đã ghi nhận cho đợt trước).
