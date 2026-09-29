# BASELINE2 — mốc trước đợt tối ưu tốc độ lần 2 (9/2026)

Đo trên `main` `aaf7e464` (đã bao gồm đợt perf 9/2026 + rank Vô Song). Build sạch trong worktree
riêng `perf2/baseline` (không đụng working tree chính — repo đang có ~99 phiên khác dùng chung).
Build tĩnh serve bằng `python3 -m http.server`, Chrome headless, KHÔNG đăng nhập (trang cần đăng
nhập chỉ hiện màn yêu cầu, không có nội dung/Supabase thật).

## 1. Build

`npm run build` (Turbopack) — OK, ~21 s, 66 trang tĩnh.

## 2. JS ban đầu — 2 trang mục tiêu (`perf/chunks-report.mjs`)

| Trang | KB (raw) | Số chunk |
|---|---:|---:|
| `/lop-hoc/bai` | **1441** | 14 |
| `/kiem-tra/lam` | **1424** | 13 |

Không đổi so với đợt trước (1395/1399 → nay đo lại ra 1441/1424, chênh do cách đo — cùng thứ tự
độ lớn). Thủ phạm không đổi: KaTeX ~290 KB + framer-motion ~139 KB nằm trong JS ban đầu.

10 trang nặng nhất (đầy đủ xem `perf2/chunks-baseline.txt` nếu cần): `/tai-khoan` 1621 KB,
`/lop-hoc/bai` 1441, `/kiem-tra/lam` 1424, `/lop-hoc/ket-qua/chi-tiet` 1413, `/lop-hoc/cnc` 1378,
`/phu-huynh` 1308, `/lop-hoc/ket-qua` 1287, `/quan-tri/xep-hang` 1141, `/lop-hoc/xep-hang` 1116,
`/quan-tri/nhap-bai` 1042.

## 3. JS nền dùng chung 66/66 trang

10 chunk xuất hiện trên **cả 66 trang tĩnh**:

| Chunk | KB raw | KB gzip | Ghi chú |
|---|---:|---:|---|
| `2buj0879okv_k.js` | 222 | 69 | react-dom |
| `3i5wqgcrghw_j.js` | 211 | 52 | supabase-js + GoTrue |
| `38qn247ecd_3u.js` | 144 | 39 | |
| `2ulmuk4xe5w1r.js` | 55 | 13 | |
| `34db8mjs30y0h.js` | 44 | 9 | |
| `1i0u1ck1kuytp.js` | 35 | 12 | |
| `0qej0tqfzx6l1.js` | 28 | 9 | |
| `3mrciss18_5f3.js` | 19 | 7 | |
| `turbopack-1eln-2r904oan.js` | 11 | 4 | |
| **Tổng** | **880** | **253** | |

Khớp với con số đợt trước (880/253 — không giảm). `supabase-js`+GoTrue (211 KB) và `react-dom`
(222 KB) là 2 khoản lớn nhất, tải trên **mọi trang kể cả trang công khai chưa đăng nhập**.

## 4. Lighthouse mobile preset (mặc định CLI, không `--preset=desktop`), Chrome headless, throttle
mobile mô phỏng mặc định của Lighthouse (CPU 4×, mạng "Slow 4G" mô phỏng — số tuyệt đối sẽ bi quan
hơn mobile thật, nhưng so sánh trước/sau vẫn có ý nghĩa)

| Trang | Score | FCP | LCP | TBT | SpeedIndex | JS transfer | Ảnh transfer | Supabase request |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `/` | 65 | 4,06 s | 10,41 s | 20 ms | 4,06 s | 793 KB | 89 KB | 0 |
| `/lop-hoc/bai/?id=49` | 71 | 2,71 s | 9,34 s | 55 ms | 2,71 s | 1398 KB | 0 | 0 |
| `/kiem-tra/lam/?id=118` | 70 | 3,16 s | 7,47 s | 43 ms | 3,16 s | 1382 KB | 0 | 0 |
| `/lop-hoc/lop-10/` | 82 | 1,07 s | 4,93 s | 19 ms | 1,07 s | 450 KB | 0 | 0 |

**Không có request Supabase nào** ở cả 4 trang khi chưa đăng nhập — lý thuyết và catalog đã tới từ
`/data/*.json` tĩnh (đợt trước), `/kiem-tra/lam` chưa đăng nhập chỉ hiện màn yêu cầu đăng nhập.
Điểm mobile thấp hơn nhiều so với desktop preset đợt trước (68/78 desktop → 65/71 mobile ở cùng 2
trang) vì mobile mô phỏng CPU yếu hơn + mạng chậm hơn — **đúng như ghi chú trong yêu cầu, số desktop
đợt trước "đẹp hơn thực tế"**.

## 5. Round-trip Supabase (Sydney) — đo trực tiếp bằng `curl`, không qua trình duyệt

Vì trang ẩn danh không gọi Supabase, đo thẳng round-trip TCP+TLS+TTFB tới
`fxnqgmfqdbvnjawgnsfi.supabase.co` (3 lần, từ máy đo tại VN):

| Lần | connect | TLS xong | TTFB | Tổng |
|---|---:|---:|---:|---:|
| 1 | 96 ms | 147 ms | 216 ms | 217 ms |
| 2 | 52 ms | 109 ms | 168 ms | 169 ms |
| 3 | 1050 ms* | 1106 ms | 1254 ms | 1255 ms |

(*lần 3 có nhiễu mạng cục bộ, bỏ qua khi so sánh.) TCP connect ổn định ~50–100 ms, **TLS handshake
cộng thêm ~50–60 ms** — đúng khoản mà `preconnect` (Agent B, mục 2) có thể chạy song song thay vì
chờ tuần tự. Không đo được round-trip cho truy vấn thật (cần đăng nhập HS/GV, không có tài khoản
test sẵn trong phiên này) — Agent D nên đo lại bằng tài khoản thật nếu có.

## 6. Kết luận cho 3 agent

- Agent A (`split-js`): mục tiêu `/lop-hoc/bai` và `/kiem-tra/lam` xuống dưới 1000 KB — hiện
  1441/1424 KB.
- Agent B (`shell`): mục tiêu giảm 880 KB raw / 253 KB gzip nền dùng chung, đặc biệt xác nhận trang
  công khai (`/`, `/tin-tuc`) có thật sự cần tải GoTrue (211 KB, nằm trong `3i5wqgcrghw_j.js`) hay
  không; preconnect tới Supabase tiết kiệm ước lượng 50–150 ms/round-trip theo mục 5.
- Agent C (`hosting`): không đo được ở bước này (không chạm hosting thật/`.htaccess` khi serve bằng
  `python http.server`) — Agent D kiểm bằng cách đọc `.htaccess` sinh ra từ `scripts/deploy.sh`.
