# Prompt bàn giao Gemini/Cursor — Sơ đồ mạng nhện năng lực theo bài trong chương

Dán nguyên khối dưới vào Cursor (chế độ Auto) tại thư mục `~/Projects/thachlab`. Phần RPC + hàm service đã do Claude
làm sẵn, Gemini chỉ làm UI. Kết quả nộp lại: 2 file ở mục "Nộp lại" cuối prompt. Claude `kiem-code` soát trước khi
merge; sau merge chạy `bash scripts/run-migrations.sh` (file `20261013150000_chapter_mastery_radar.sql`) rồi deploy.

---

## Bối cảnh

thachlab là LMS Vật lí cho học sinh 14–18 tuổi (Next.js App Router, TypeScript, Tailwind v4, `output: "export"`,
Supabase). Trang kết quả cá nhân `/lop-hoc/ket-qua` dùng `components/results/StudentResultsDashboard.tsx`
(prop `viewer = "student" | "parent"`; trang `/phu-huynh` dùng cùng component với `viewer="parent"`).

Cần thêm **sơ đồ mạng nhện (radar chart)** cho học sinh thấy mức nắm từng **bài** trong **chương đang học**, đặt ngay
trong trang kết quả, dẫn tới hành động "Ôn bài yếu nhất".

**Không làm cho phụ huynh** (`viewer === "parent"` không render gì, giữ nguyên trang phụ huynh).

## Dữ liệu — đã có sẵn, KHÔNG sửa migration, KHÔNG tạo RPC mới

Hàm `fetchMyChapterMasteryPct(before?: Date)` trong `services/mastery.ts` trả `ChapterLessonMastery[]`:

```ts
interface ChapterLessonMastery {
  chapterId: number; chapterTitle: string;
  lessonId: number; lessonTitle: string; sortOrder: number;
  answeredCount: number;
  pct: number | null;          // 0–100, null khi bài chưa có lượt nào
  level: "mastered" | "practicing" | "weak" | "insufficient";
}
```

- Gọi 2 lần song song (`Promise.all`): không tham số = hiện tại; `new Date(Date.now() - 30*86400e3)` = "chính em
  tháng trước". Kết quả đã sắp theo `sortOrder`, cùng danh sách bài ở cả 2 lần (cùng chương).
- Trả `[]` khi học sinh chưa làm bài nào → không render gì.
- Hàm **ném lỗi khi RPC chưa chạy trên production** → bắt lỗi, không render gì, không log ồn (`catch (() => null)`).
- Nhãn/màu/icon của `level` dùng đúng `MASTERY_LABEL`, `MASTERY_ICON`, `MASTERY_TONE` đã export trong
  `services/mastery.ts` và `components/ui/Badge.tsx` (tone `success/warning/error/neutral`). Không bịa màu hex.
- Ngưỡng "Nắm vững" = 80%, "Cần luyện thêm" = 50% (`docs/mastery-rules.md`). Vẽ vòng mục tiêu ở 80%.

## Thành phần cần làm

### 1. `components/results/ChapterMasteryRadar.tsx` (client component, `"use client"`)

Props: `{ studentId: string }` (chỉ để làm key tải lại). Tự tải dữ liệu bằng `fetchMyChapterMasteryPct`.

**Chọn hình vẽ theo số bài có dữ liệu** (bài có `pct !== null`):
- **≥ 3 bài có dữ liệu → radar**. Chỉ vẽ trục cho những bài có `pct !== null` (bài chưa học thì không có trục, tránh
  biểu đồ méo đầu năm). Tối đa 8 trục; nếu chương có hơn 8 bài có dữ liệu thì lấy 8 bài gần nhất theo `sortOrder`.
- **1–2 bài có dữ liệu → thanh ngang** (mỗi bài một thanh, số % bên phải, nhãn mức bằng chữ). Không radar.
- **0 bài có dữ liệu → không render**.

**Radar vẽ bằng SVG thuần** (repo không có thư viện biểu đồ, không cài thêm package):
- `viewBox="0 0 320 320"`, `width="100%"`, `max-width: 360px`, căn giữa. Nhãn trục = tên bài rút gọn ≤ 14 ký tự
  (cắt + "…"), `font-size: 11`, đặt ngoài vòng ngoài; `title` của `<text>` ghi tên đầy đủ.
- 3 lớp, theo thứ tự vẽ:
  1. Lưới: 4 vòng 25/50/75/100 nét mảnh màu `var(--color-border)` (hoặc token viền hiện có trong `app/globals.css`).
  2. **Vòng mục tiêu 80%**: nét đứt, màu token `success` (emerald) mờ. Chú thích "Mục tiêu: Nắm vững (80%)".
  3. **Chính em tháng trước**: đa giác viền nét đứt màu `var(--color-muted)`, không tô. Chỉ vẽ khi dữ liệu tháng trước
     có ≥ 3 bài `pct !== null`; nếu không thì bỏ lớp này và bỏ dòng chú thích tương ứng.
  4. **Hiện tại**: đa giác tô màu nhấn `var(--color-primary)` opacity 0.18, viền 2px cùng màu, chấm tròn r=3 ở đỉnh.
     Đỉnh của bài `level === "weak"` tô màu `error`, `practicing` tô `warning` (M3: một màu nhấn + ba màu trạng thái).
- Chú thích (legend) dưới hình: 3 dòng chữ nhỏ có mẫu nét, mỗi mục một dòng.
- **Không hoạt hình** (không transition khi vào trang, không hover nhấp nháy). Quy tắc B4.
- Màu phải nhìn được cả nền sáng (mặc định) và nền tối (`[data-theme="dark"]`): chỉ dùng token CSS, không hex.

**Dưới hình, bảng số** (bắt buộc, vì màu không được là kênh thông tin duy nhất): mỗi bài một dòng:
`<icon mức> Tên bài — 72% · Cần luyện thêm` (dùng `MASTERY_ICON` + `MASTERY_LABEL`). Bài chưa có dữ liệu ghi
"chưa làm". Nếu có dữ liệu tháng trước thì thêm chênh lệch bằng chữ: "tăng 15 điểm %" / "giảm 5 điểm %" / "giữ nguyên".

**Một nút chính duy nhất** ở cuối khối: `Ôn bài yếu nhất` → bài có `pct` thấp nhất trong các bài `level` là `weak`
hoặc `practicing`; link `/lop-hoc/bai/?id=<lessonId>#secondary-stage-ly_thuyet`. Dùng cùng kiểu nút chính đang có
trong `StudentResultsDashboard.tsx` (xem nút "Ôn lại bài" ~dòng 405). Không có bài yếu → thay nút bằng một dòng chữ
"Chương này em đã nắm vững, học tiếp bài mới." (không nút).

Tiêu đề khối: `Năng lực chương: <chapterTitle>`; dòng phụ: "So với chính em 30 ngày trước và mục tiêu 80%".
Không có chữ "trung bình lớp", không xếp hạng, không so với bạn.

### 2. Đặt vào `components/results/StudentResultsDashboard.tsx`

- Chỉ khi `viewer === "student"`.
- Đặt **thay thế** khối `Chủ đề cần ôn` (section `priorityGaps.length > 0`, ~dòng 804) chứ không thêm chồng: giữ nguyên
  nhánh `viewer === "parent"` của khối đó ("Phần con còn sai"); với học sinh, render `<ChapterMasteryRadar>` ở vị trí
  đó, còn danh sách `shownGaps` của học sinh chuyển vào `<details>` thu gọn ngay dưới radar với tóm tắt
  "Xem các yêu cầu cần đạt còn sai (n)".
- Không đụng thứ tự các khối khác, không đổi phần phụ huynh.
- Tải dữ liệu radar không được chặn render phần còn lại (loading riêng trong component, placeholder chiều cao cố định
  ~ 280px để không nhảy bố cục).

## Quy tắc giao diện bắt buộc (từ `docs/QUY-TAC-THIET-KE.md` — đọc mục 1, 3, 4, 6, 7 trước khi code)

- **N2** ≤ 4 thao tác nhìn thấy trong khối. **B2** đúng một điểm nổi bật: nút "Ôn bài yếu nhất".
- **B4** không có gì tự chuyển động. **M3** một màu nhấn + ba màu trạng thái, dùng token. **M7** nền sáng mặc định.
- **D2** đích chạm ≥ 44px, nhãn nút 1 dòng. Radar + bảng + nút phải nằm gọn trong **375px**, không cuộn ngang.
- **L3/L4** không hiện huy hiệu/RP/xếp hạng trong khối; chữ hướng vào việc tiếp theo, không dùng vai "thầy".
- **C3** ≤ 4 cỡ chữ trong khối.

## Kiểm trước khi nộp

1. `npx tsc --noEmit -p .` và `npm run lint` sạch.
2. Chụp màn hình 375×812 và 1440 ở nền sáng + nền tối, dùng dữ liệu giả (mock `fetchMyChapterMasteryPct` tạm trong
   lúc chụp rồi gỡ): (a) 5 bài có dữ liệu + tháng trước, (b) 4 bài hiện tại nhưng tháng trước chỉ 1 bài, (c) 2 bài
   (thanh ngang), (d) `[]`, (e) hàm ném lỗi. Trường hợp (d)(e) trang phải y như cũ.
3. Không thêm dependency vào `package.json`. Không sửa `supabase/`, `services/mastery.ts`, `docs/`.

## Nộp lại

- `components/results/ChapterMasteryRadar.tsx` (mới)
- `components/results/StudentResultsDashboard.tsx` (sửa đúng khối nêu trên)
- Ảnh chụp 5 trường hợp ở `scripts/logs/radar-nang-luc/` (không commit ảnh, chỉ để Claude soát).
- Mô tả commit đề xuất: `feat(ket-qua): sơ đồ mạng nhện năng lực theo bài trong chương (N2, B2, B4, M3, D2, L3)`.
