# Prompt bàn giao Gemini/Cursor — Canvas mô phỏng theo theme nền sáng

Dán nguyên khối dưới vào Cursor (chế độ Auto) tại thư mục `~/Projects/thachlab`. Việc thuần UI/JS, không đụng
schema/RLS. Kết quả nộp lại: các file ở mục "Nộp lại" cuối prompt. Claude `kiem-code` soát trước khi merge
(đối chiếu `docs/MAU-NEN-SANG.md` §4, §7 và checklist §8 `docs/QUY-TAC-THIET-KE.md`).

Nguồn gốc việc: bản nhận xét UI ngày 13/10/2026 chỉ ra "mảng tối đột ngột" của canvas giữa trang sáng. Claude đã
phản biện: KHÔNG thêm bezel trang trí (vi phạm coherence Mayer, N-rules), mà cho canvas đọc token theme.
Đây là mục đầu tiên của `docs/MAU-NEN-SANG.md` §7 "Việc còn treo".

---

## Bối cảnh

thachlab là LMS Vật lí cho học sinh 14–18 tuổi (Next.js App Router, TypeScript, Tailwind v4, `output: "export"`).
Từ 11/10/2026 **nền sáng là mặc định toàn site**; nền tối là tuỳ chọn, bật bằng `html[data-theme="dark"]`
(`components/layout/ThemeToggle.tsx`, lưu `localStorage["thachlab-theme"]`). Màu nền sáng/tối định nghĩa ở
`app/globals.css`: khối `@theme` (sáng) và khối `html[data-theme="dark"]` (tối), dạng CSS variable
`--color-bg`, `--color-panel`, `--color-surface-2`, `--color-ink`, `--color-muted`, `--color-line`,
`--color-line-strong`, `--color-primary`, `--color-accent`, `--color-ok`, `--color-warn`, `--color-danger`,
`--color-cyan`.

Vấn đề: 4 mô phỏng canvas vẽ nền bằng hằng số JS nên lưới CSS không với tới, thành khối đen giữa trang sáng:

| File | Hằng số nền tối | Dùng ở |
|---|---|---|
| `components/physics/ProjectileSimulation.tsx` | `STAGE_BG_TOP = "#070C15"`, `STAGE_BG_BOTTOM = "#04070C"`, `ACCENT = "#22D3EE"`, `SLATE_*` | Hero trang chủ `components/home/PhysicsSimulationHero.tsx` |
| `components/physics/RescueDropSimulation.tsx` | như trên | Hero trang chủ |
| `components/physics/InterferenceSimulation.tsx` | `STAGE_BG_TOP = [7,12,21]`, `STAGE_BG_BOTTOM = [4,7,12]` (mảng RGB, vì tô pixel), `TEXT = "#E2E8F0"`, `M_MAX`, `M_MIN` | Hero trang chủ |
| `components/physics/ShadowSpringSimulation.tsx` | như Projectile + `PEND_*`, `TEXT = "#E2E8F0"` | `components/home/PhysicsEverywhere.tsx` |
| `components/physics/SoundInterferenceSimulation.tsx` | không có canvas nền; nhưng JSX dùng idiom nền tối: `bg-white/10`, `bg-white/[0.03]`, `border-white/10`, `text-slate-400`, `text-slate-300`, `text-white`, `bg-black/50` | Hero + `app/(public)/mo-phong/giao-thoa-am/page.tsx` |

## Việc cần làm

### 1. Tạo `components/physics/stage-theme.ts` — một nguồn màu cho mọi canvas

```ts
export interface StagePalette {
  bgTop: string; bgBottom: string;   // nền sân khấu (gradient nhẹ, KHÔNG neon)
  bgRgb: [number, number, number];   // bản RGB của bgBottom cho sim tô pixel
  grid: string; gridStrong: string;  // lưới mờ / trục
  ink: string; muted: string;        // chữ số liệu / chữ phụ
  line: string;                      // viền, thước
  accent: string; accentSoft: string;// họ màu chính (quỹ đạo, bóng)
  warm: string;                      // điểm nhấn ấm (vật thể, mốc)
  primary: string; primaryEdge: string; // họ xanh (con lắc, nguồn sóng)
  waveMax: string; waveMin: string;  // cực đại / cực tiểu giao thoa
}
export function getStagePalette(): StagePalette
export function subscribeStageTheme(cb: () => void): () => void
```

- `getStagePalette()` đọc `document.documentElement.dataset.theme`. Theme sáng trả bảng màu **đọc từ CSS variable**
  bằng `getComputedStyle(document.documentElement).getPropertyValue("--color-…")` (bg = `--color-surface-2`,
  ink = `--color-ink`, muted = `--color-muted`, line = `--color-line-strong`, accent = `--color-cyan`,
  warm = `--color-accent`, primary = `--color-primary`, waveMax = `--color-primary`, waveMin = `--color-surface-2`…),
  có fallback hex cứng cho SSR/khi biến rỗng. Theme tối trả đúng các hằng số hiện có (giữ nguyên hình ảnh cũ,
  không đổi gì cho người đang dùng nền tối).
- Mọi màu chữ trên nền sáng phải đạt **≥4,5:1** trên `bgTop`/`bgBottom`; lưới ≥3:1 với nền (WCAG 1.4.11).
  Không dùng `#22D3EE` (cyan neon) hay `#FBBF24` trên nền sáng: chỉ 1,6:1 và 1,7:1. Dùng `--color-cyan` (#0e7490)
  và `--color-accent` (#b45309).
- `subscribeStageTheme`: `MutationObserver` trên `attributes: ["data-theme"]` của `<html>`, gọi `cb` để sim
  vẽ lại khi người dùng bấm ThemeToggle. Trả hàm huỷ.
- Chỉ chạy phía client (`typeof document !== "undefined"`); sim đã là client component.

### 2. Sửa 4 sim canvas dùng `getStagePalette()`

- Xoá các hằng số `STAGE_BG_*`, `ACCENT*`, `WARM`, `TEXT`, `SLATE_*`, `PEND_*`, `M_MAX/M_MIN` ở đầu file; thay bằng
  `const p = paletteRef.current` truyền vào hàm vẽ (hàm vẽ nhận thêm tham số `p: StagePalette`).
- Trong `useEffect` của mỗi sim: `paletteRef.current = getStagePalette()`; đăng ký `subscribeStageTheme` để cập nhật
  ref rồi vẽ lại một khung; cleanup huỷ đăng ký.
- `InterferenceSimulation` tô pixel bằng `ImageData`: dùng `p.bgRgb` và nội suy sang `waveMax`/`waveMin`; ở nền
  sáng cực đại phải **đậm hơn** nền, cực tiểu nhạt hơn (đảo chiều so với bản tối). Kiểm bằng mắt: vân phải nhìn
  thấy rõ ở cả hai theme, không trắng xoá.
- Không đổi vật lý, không đổi bố cục, không đổi số liệu, không đổi kích thước canvas. Chỉ màu.
- Giữ `prefers-reduced-motion` và mọi `requestAnimationFrame` như cũ.

### 3. Dọn `SoundInterferenceSimulation.tsx` theo bảng quy đổi `docs/MAU-NEN-SANG.md` §4

`bg-white/10` → `bg-surface-2`; `bg-white/[0.03]`/`[0.02]` → `bg-surface-2`; `border-white/10` → `border-line`;
`text-slate-400` → `text-muted`; `text-slate-300`/`text-slate-200` → `text-ink`; `text-white` (chữ thân) →
`text-ink`; `bg-black/50 text-white/80` (nhãn nổi trên canvas) → `bg-panel/90 text-ink border border-line`.
Giữ `text-white` nếu nằm trên nền màu đặc (`bg-primary`).

### 4. Không làm

- Không thêm bezel, viền "màn hình dao động ký", bóng đổ, quầng sáng (M6).
- Không đổi màu ở `RankCelebrationModal` (cố ý giữ nền tối, L3) hay `LessonPresenter`.
- Không sửa `app/globals.css` (nếu thấy thiếu token thì ghi vào mục "Ghi chú" khi nộp, đừng tự thêm).
- Không đổi `features/rank/types.ts` (mục khác trong §7, đợt sau).

## Kiểm trước khi nộp

```
npm run lint && npx tsc --noEmit && npm run check:a11y && npm run build
```

Rồi chạy `npm run dev`, mở `http://localhost:3000/` và `/mo-phong/giao-thoa-am`:
- Chụp 4 ảnh **375px** (theme sáng: hero + sim giao thoa âm; theme tối: hai cái tương tự) + 2 ảnh 1440 theme sáng,
  lưu `docs/anh/giao-dien-nen-sang/canvas-*.png` (nén ≤150 KB mỗi ảnh).
- Bấm ThemeToggle khi sim đang chạy: canvas phải đổi màu ngay, không cần tải lại trang.
- Kéo bệ phóng / thả hàng / đổi tần số: hành vi y như trước.

## Nộp lại

1. `components/physics/stage-theme.ts` (mới)
2. 5 file sim đã sửa trong `components/physics/`
3. 6 ảnh chụp ở `docs/anh/giao-dien-nen-sang/canvas-*.png`
4. Một đoạn "Ghi chú" ngắn: số đo tương phản của ink/muted/grid trên nền sáng mới (tính bằng
   `node scripts/check-a11y.mjs` hoặc công cụ bất kỳ), token nào còn thiếu, chỗ nào phải đoán.

Commit riêng, mô tả ghi mã quy tắc: `M1, M3, M6, G2 — canvas đọc token theme (MAU-NEN-SANG §7)`.
Không `git add .`; chỉ add đúng các file trên.
