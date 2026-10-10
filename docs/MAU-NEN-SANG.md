# Bảng màu ThachLab — nền sáng là mặc định

**Chốt 11/10/2026.** Từ đợt này, giao diện ThachLab lấy **nền sáng (trắng)** làm mặc định trên
toàn site; **nền tối chỉ còn là tuỳ chọn** do người dùng tự bật (nút Trăng/Mặt trời ở navbar, hoặc
"Dịu mắt" ở trang bài học/phụ huynh).

Đọc kèm:
- `docs/QUY-TAC-THIET-KE.md` — quy tắc thị giác học sinh 14–18 (mã `N/C/M/B/H/V/D/L`).
- `docs/QUY-TAC-THIET-KE-PHU-HUYNH.md` — quy tắc cho phụ huynh 45–60 (mã `P…`).
- `docs/UI.md` — ngưỡng tương phản, sàn cỡ chữ, checklist.
- `app/globals.css` — **nguồn duy nhất** của màu: khối `@theme` (nền sáng) + khối
  `html[data-theme="dark"]` (nền tối).
- Trang xem thử: `http://localhost:3000/dev/giao-dien` (`?theme=dark`, `?aud=parent|teacher`).

---

## 1. Vì sao nền sáng

| Mã | Căn cứ | Hệ quả thiết kế |
|---|---|---|
| M1 | Piepenbrock, Mayr, Mund & Buchner 2013; Buchner & Baumgartner 2007 — đọc chữ sẫm trên nền sáng ("positive polarity") nhanh hơn và soát lỗi tốt hơn ở **mọi** lứa tuổi, ưu thế rõ nhất khi chữ nhỏ | Trang đọc/làm bài mặc định sáng; nền tối là tuỳ chọn, ghi nhớ lựa chọn |
| P5 | Cùng nguồn, nhóm 45–60 (thuỷ tinh thể ngả vàng làm giảm truyền bước sóng ngắn — chữ xanh nhỏ trên nền đen là tổ hợp tệ nhất) | Trang phụ huynh luôn sáng, có Dịu mắt + A−/A+ |
| M2 | WCAG 2.1 1.4.3; Material dark theme — không trắng tinh trên đen tinh | Nền tối giữ xám rất đậm `#05070b`, chữ ~95% trắng `#f1f5f9` |
| M3 | Von Restorff 1933; Treisman & Gelade 1980 — màu bão hoà bắt chú ý tiền ý thức | **Một** màu nhấn + **ba** màu trạng thái, còn lại trung tính |
| M6 | Mayer — nguyên tắc mạch lạc | Không gradient/quầng sáng/blur ở vùng đọc và làm bài (chỉ trang giới thiệu) |

**Vì sao không theo `prefers-color-scheme` nữa:** để màu sắc kiểm soát được và trang không "nửa
tối nửa sáng" giữa các phiên. Mặc định luôn sáng; chỉ đổi khi người dùng đã tự chọn.

---

## 2. Token màu (nguồn: `app/globals.css` khối `@theme`)

| Token | Nền sáng (mặc định) | Nền tối (tuỳ chọn) | Dùng ở đâu |
|---|---|---|---|
| `--color-bg` | `#f5f7fa` | `#05070b` | Nền trang |
| `--color-panel` | `#ffffff` | `#0b1020` | Mặt thẻ, navbar |
| `--color-panel-deep` | `#ffffff` | `#080d1d` | Thanh cố định |
| `--color-surface-2` | `rgba(15,23,42,.05)` | `rgba(255,255,255,.05)` | Ô nhạt trong thẻ, hàng bảng, nút phụ |
| `--color-primary` | `#1d4ed8` | `#2563eb` | **Màu nhấn duy nhất** cho thứ bấm được |
| `--color-primary-dark` | `#1e40af` | `#1d4ed8` | Hover/pressed |
| `--color-primary-soft` | `#eef2ff` | `rgba(37,99,235,.18)` | Nền "đang chọn" (tab, chip lọc) |
| `--color-ink` | `#0f172a` | `#f1f5f9` | Chữ thân |
| `--color-muted` | `#475569` | `#94a3b8` | Chữ phụ, chú thích, mốc thời gian |
| `--color-line` | `rgba(15,23,42,.10)` | `rgba(255,255,255,.08)` | Viền hairline giữa khối |
| `--color-line-strong` | `#8b93a1` | `rgba(255,255,255,.16)` | Viền ô nhập (đạt 3:1 — WCAG 1.4.11) |
| `--color-ok` / `-warn` / `-danger` | `#047857` / `#b45309` / `#b91c1c` | `#34d399` / `#fbbf24` / `#f87171` | Đúng–đạt / cần chú ý / sai–phá huỷ |
| ↑ trong khối phụ huynh | `#065f46` / `#78350f` / `#991b1b` (7,4 / 8,5 / 7,7:1 — P2 đòi AAA 7:1) | như trên | Trạng thái của khối `.parent-page` |
| `--color-cyan`, `--color-violet`, `--color-accent` | `#0e7490`, `#6d28d9`, `#b45309` | tông 300–400 | Chỉ cho nhãn chuyên đề, không dùng làm màu trang trí |
| `--color-slate-500` | `#64748b` (4,76:1) | `#7c8ba1` (5,47:1) | Mốc thời gian, placeholder |

Số đo: `npm run check:a11y` (đo cả token nền sáng, khối phụ huynh, nền tối và chế độ Dịu mắt).

---

## 3. Khác nhau theo nhóm người xem (cùng một hệ màu)

| Nhóm | Phạm vi CSS | Khác biệt có chủ ý | Mã quy tắc |
|---|---|---|---|
| Học sinh 14–18 + trang công khai | mặc định (`:root`) | Thân bài 16–18px, đích chạm ≥44px, một điểm nổi bật mỗi màn | C1, D2, B2 |
| Phụ huynh 45–60 | `.parent-page` | Nền ngả ấm `#f7f7f4`; chữ phụ `#3d4653` (≥7:1, AAA); nhấn navy `#1e40af`; viền ô nhập `#767f8d`; thân 1,125rem; đích chạm ≥48px; số `tabular-nums` | P1, P2, P4, P5, P6 |
| Giáo viên / quản trị | `.teacher-dashboard`, `.admin-shell` | Nền trung tính hơn `#f4f5f7`, cỡ chữ gốc 14px, mật độ cao (nhiều bảng) | — |

Bản thân **màu** không đổi theo nhóm (đổi màu theo trang là phá M3/N4); chỉ **số đo thị giác** đổi.

---

## 4. Bảng quy đổi: idiom nền tối → token nền sáng

Khi sửa một component cũ, quy đổi theo bảng này (đây cũng là việc đã làm ở đợt 11/10/2026):

| Class cũ (viết cho nền tối) | Thay bằng |
|---|---|
| `bg-[#05070B]`, `bg-[#080D1A]`, `bg-[#0B1020]`, `bg-[#080d1d]`, `bg-[#10192a]`, `bg-[#111a2e]`, `bg-[#172033]` | `bg-panel` (nền cả trang: `bg-bg`) |
| `text-white` (chữ thân) | `text-ink` — **giữ `text-white`** khi nằm trên nền màu đặc (`bg-primary`, `bg-emerald-*`, `bg-red-*`) |
| `text-slate-200`, `text-slate-300` | `text-ink` |
| `text-slate-400` | `text-muted` |
| `text-slate-500` | giữ nguyên (đạt 4,5:1); riêng khối phụ huynh đổi sang `text-muted` |
| `border-white/10`, `border-white/15`, `border-white/[0.07]` | `border-line`; viền ô nhập → `border-line-strong` |
| `bg-white/5`, `bg-white/[0.04]`, `bg-white/[0.06]`, `bg-white/[0.07]`, `bg-white/10` | `bg-surface-2` (kể cả `hover:`) |
| `bg-gradient-to-*`, `from-[#172c46]`, `via-[#0e1c32]`, `to-[#071426]` | bỏ → `bg-panel` + `border-line` |
| `shadow-[0_0_24px_rgba(...)]` (quầng sáng) | bỏ → `shadow-sm` hoặc không |
| `text-cyan-300`, `text-violet-400`, `text-sky-300` (trang trí) | `text-primary`; nếu là trạng thái → `text-ok`/`text-danger`/`text-warn` |
| `bg-[#155e75]` (nút teal) | `bg-primary` + `text-white`, hover `bg-primary-dark` |

---

## 5. Lưới an toàn trong `globals.css` (đọc trước khi định xoá)

Vì theme tối từng là mặc định, hàng trăm chỗ trong JSX viết thẳng class màu nền tối. Cuối
`app/globals.css` có khối **"NỀN SÁNG — QUÉT NỐT MÀU TỐI / NEON HARD-CODE"** phủ các idiom đó
(quét cả biến thể hoa/thường và độ mờ). Khối này **không phải nguồn màu** — nó chỉ để không còn ô
tối nào lọt ra khi component chưa được dọn. Khi một idiom đã sạch khỏi mã nguồn (kiểm bằng
`grep -rn 'bg-white/5' components app`) thì rule tương ứng trong lưới có thể xoá; xoá hết lưới là
đích cuối, nhưng **không xoá trước khi grep thấy sạch**.

---

## 6. Quy trình đổi màu (đừng đoán bằng mắt)

1. Sửa **chỉ** khối `@theme` (nền sáng) và `html[data-theme="dark"]` (nền tối) trong `app/globals.css`.
2. `npm run check:a11y` — phải xanh (script đo tương phản token + bắt chữ < 12px).
3. Mở `http://localhost:3000/dev/giao-dien` — xem bảng màu và bộ dựng ở cả hai theme, cả ba nhóm.
4. Chụp 375px **và** 1440 (checklist §8 của `docs/QUY-TAC-THIET-KE.md`) trước khi báo xong.
5. Ghi mã quy tắc (`M1`, `P2`…) vào mô tả commit.

---

## 7. Việc còn treo sau đợt 11/10/2026

- **Canvas mô phỏng vẫn vẽ nền tối** trong theme sáng (`PhysicsSimulationHero` và các mô phỏng
  canvas khác): màu nằm trong JS nên lưới CSS không với tới. Nên cho canvas đọc token theme hoặc
  bọc trong khung "màn hình" có viền — hiện là một khối đen giữa trang sáng (đã có viền bo nên
  đọc được như "màn hình thí nghiệm", nhưng chưa phải giải pháp đẹp).
- **Màu bậc rank nằm trong JS** (`features/rank/types.ts`: `color`/`light`/`tone`, MEDAL,
  AURORA/METAL) và đĩa huy hiệu `rgba(11,16,32,.9)` ở `TierLadder` — cùng loại với canvas: đổi
  theo theme thì phải sửa trong JS, không phải class.
- **Màn ăn mừng (`RankCelebrationModal`) và toast "Lên hạng!" cố ý giữ nền tối** — L3 cho phép
  hiệu ứng ở màn kết thúc; chữ trong đó đặt `text-white` (không dùng token, vì token ở nền sáng là
  chữ sẫm, sẽ thành sẫm-trên-tối).
- **M4 còn thiếu ở `QuestionCard`** chế độ xem lại câu Đúng/Sai: trạng thái chỉ hiện bằng màu, ô
  Đ/S không có ✓/✗. Sửa được nhưng phải thêm phần tử → đổi bố cục, để đợt sau.
- **Nút nhận màu đặc qua prop `color`** (`PracticeSession`…): giữ `text-white` theo quy tắc 2, nên
  amber/violet vẫn dưới 4,5:1 — muốn đạt thì nơi gọi phải truyền màu đậm hơn.
- **Còn component dùng idiom nền tối** (lưới an toàn che nên không lộ ra): `StudentAttendancePanel`,
  `StudentFinalGradeCard`, `PwaInstallCard`, `StudentCodeField`, `QuickPractice`, `ForParents` (một
  vài hex trung tính cho nền sáng). Dọn dần khi đụng tới file.
- **`text-slate-600/700`** còn vài chỗ (thứ trong tuần ở `ClassRankBoard`/`ClassRankGroups`, mũi tên
  `RankPage`): nền sáng đạt ~7:1, theme tối hơi thấp — chưa có token cho mức này.

---

## 8. Nhật ký rút kinh nghiệm

- **2026-10-11 · Chụp 375px bằng `chrome --headless --window-size=375,812` KHÔNG cho viewport 375px**
  → ảnh bị cắt còn 375 trong khi trang được dàn ở ~500px, nhìn như "nội dung tràn ngang, chữ bị cắt"
  và suýt bị sửa theo một lỗi không tồn tại. Cách đúng: đặt `Emulation.setDeviceMetricsOverride`
  rồi mới chụp/đo — dùng `node scripts/do-bo-cuc.mjs <url> --rong=375 --cao=812 --anh=/tmp/x.png`
  (công cụ in luôn `scrollWidth` và danh sách phần tử tràn THẬT, phân biệt với phần tử bị cha cắt
  như marquee). Kiểm chứng: trang chủ ở 375px có `scrollWidth = 375`, tràn thật = 0.
- **2026-10-11 · Hai phiên cùng mở một cây làm việc thì `git commit -a` của phiên này nuốt thay đổi
  chưa commit của phiên kia** → khối CSS của đợt này bị commit kèm vào commit "RP lý thuyết" của
  phiên khác, còn phần bảng màu ở đầu file thì không; hậu quả là `globals.css` trên main ở trạng
  thái nửa vời cho tới khi đợt này commit. Quy tắc: commit theo **đường dẫn cụ thể**, commit sớm
  thành nhiều mẻ nhỏ; thấy file dùng chung "tự nhiên" khác đi thì tra `git log -S '<chuỗi>' -- <file>`
  trước khi sửa tiếp.
- **2026-10-11 · Kiểm chứng "chỉ đổi màu" nên làm bằng máy, không đọc mắt** → `scripts/kiem-doi-mau.mts`
  bỏ mọi chuỗi rồi so bản HEAD với bản đang làm việc; 100/112 file kết luận "chỉ đổi chuỗi class",
  12 file còn lại đọc tay (đều là chủ ý: xoá quầng sáng, gỡ inline style). Lưu ý khi viết công cụ
  loại này: phải bỏ cả chuỗi nằm trong `${…}` của template literal, nếu không sẽ báo động giả hàng
  loạt vì class hay viết trong nhánh ternary.

