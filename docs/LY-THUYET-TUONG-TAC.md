# Chuẩn viết lý thuyết tương tác (bản 01/10/2026)

Áp dụng cho mọi mục `lesson_items.kind = 'ly_thuyet'` của ThachLab. Mục đích: học sinh đọc
**hiểu ngay lượt đầu**, tự đoán trước khi được xem kết quả, và tự đo được mình hiểu tới đâu —
thay vì một khối chữ + công thức như bản sao SGK.

Tài liệu này là **hợp đồng giữa người viết nội dung và code**: các class HTML, tên widget và
đường đăng dưới đây đã có sẵn trong repo, không cần viết code mới khi chỉ soạn nội dung.

---

## 1. Ba tầng tương tác (làm từ rẻ tới đắt)

| Tầng | Làm bằng gì | Chi phí | Dùng khi |
|---|---|---|---|
| 0. Nhịp dẫn dắt | HTML/CSS thuần (`<details>`, khối `.tl-*`) | 0 code, 0 KB JS | Mặc định cho **mọi** mục |
| 1. Kiểm tra hiểu bài | `exams` gắn vào `lesson_items.exam_ids` + `quiz_min_correct` (RPC/UI đã có) | Rẻ, tái dùng hạ tầng | Khi muốn đo được + cộng vào danh hiệu/YCCĐ |
| 2. Widget React | Thẻ `<div data-tl-widget="…">` + component trong `TheoryWidget.tsx` | Viết code, chunk tải riêng | Khi khái niệm **phải** thấy mới hiểu (mô phỏng, thanh trượt) |

Nguyên tắc: **không nhảy sang tầng 2 khi tầng 0 + 1 đã đủ.** Mỗi widget là một chunk JS phải
tải thêm trên điện thoại — chỉ dùng khi hình động thật sự dạy được điều chữ không dạy được.

---

## 2. Khuôn 6 nhịp cho một mục lý thuyết

Soạn theo đúng thứ tự này; mục nào không cần nhịp nào thì bỏ, nhưng **không đảo**:

| Nhịp | Mục đích | HTML |
|---|---|---|
| 1. Móc thực tế | Một tình huống đời thường + câu hỏi mở, chưa có lời giải | `<div class="tl-moc">` |
| 2. Dự đoán | Học sinh tự nghĩ trước khi xem đáp án | `<details class="tl-reveal">` |
| 3. Kiến thức | Định nghĩa + công thức + đơn vị, mỗi đoạn một ý | `<h3>`, `<p>`, `<div class="tl-formula">`, `.tl-note` |
| 4. Ví dụ mẫu theo bước | Giải từng bước, nói rõ "vì sao bước này" | `<ol class="tl-steps">`, `.tl-real` |
| 5. Bẫy + tự kiểm | 3 bẫy hay mắc + 3–5 câu tự kiểm | `.tl-trap`, `<details class="tl-check">` |
| 6. Chốt | `summary_html` (Tóm tắt ý chính cần thuộc) + 1 việc về nhà | `.tl-note` trong body + `summary_html` |

**Hai thứ bắt buộc giữ khi viết lại:**
1. **Mỗi đoạn lớn là một `<h3>`** — quiz "Kiểm tra nhanh" dựa vào đó để cuộn + tô vàng đúng đoạn
   khi học sinh trả lời sai (`features/lessons/theory-sections.ts`). Viết bằng `<p><strong>` thì
   mất tính năng này.
2. **`summary_html`** — khối "📌 Tóm tắt ý chính cần thuộc" hiện ngay cả khi mục đang thu gọn;
   đây là phần học sinh dùng để ôn nhanh. Không để rỗng, không nhét cả bài vào đây.

---

## 3. Kho HTML/CSS có sẵn (không cần biết Tailwind)

Toàn bộ class dưới đây đã có trong `app/globals.css` và ăn theo khối lớp (THPT xanh, CTTC cam):

```html
<!-- 1. Móc thực tế: tình huống + câu hỏi mở -->
<div class="tl-moc">
  <p><strong>Tình huống mở đầu.</strong> …</p>
  <p>Vậy làm sao …?</p>
</div>

<!-- 2. Dự đoán: học sinh tự trả lời rồi mới mở -->
<details class="tl-reveal">
  <summary>Đoán trước: vì sao …?</summary>
  <p>Vì …</p>
</details>

<!-- 3. Công thức trọng tâm + ghi chú -->
<div class="tl-formula">$$x = A\cos(\omega t + \varphi)$$</div>
<div class="tl-note"><p><strong>Chú ý:</strong> …</p></div>

<!-- 4. Ví dụ mẫu giải theo bước (số thứ tự do CSS tự đánh) -->
<ol class="tl-steps">
  <li>So sánh với phương trình tổng quát …</li>
  <li>Thay số …</li>
</ol>
<div class="tl-real"><p><strong>Ví dụ thực tế:</strong> …</p></div>

<!-- 5. Bẫy thường gặp + tự kiểm nhanh -->
<div class="tl-trap"><p><strong>Ba bẫy hay mắc:</strong></p><ul><li>…</li></ul></div>
<details class="tl-check">
  <summary>1. Câu hỏi tự kiểm…</summary>
  <p class="tl-answer">Đáp án + vì sao.</p>
</details>

<!-- 6. Việc về nhà -->
<div class="tl-note"><p>Mở lại mô phỏng ở mục 4, …</p></div>
```

Quy ước nội dung (để "dễ hiểu" không chỉ là cảm tính):
- Câu ≤ ~20 từ; mỗi đoạn một ý; nói "vì sao" sau mỗi bước biến đổi.
- Mọi đại lượng đi kèm **đơn vị + một con số thật** ("54 km/h = 15 m/s", không nói chung chung).
- Ví dụ lấy từ đời sống người Việt: xe máy, cầu thang cuốn, quạt trần, nồi cơm điện…
- Công thức viết LaTeX trong `$…$` (giữa dòng) và `$$…$$` (riêng dòng) — KaTeX render sẵn.
- Không dùng ảnh base64; ảnh mới phải nén ≤1200px (`.webp` nếu là ảnh trang trí).

---

## 4. Khối tương tác React (tầng 2)

### 4.1. Cách dùng trong nội dung

Chèn một thẻ rỗng đúng tên widget, đặt **ở ranh giới đoạn** (ngay trước `<h3>` kế tiếp hoặc sau
khi hết ý của đoạn):

```html
<div class="tl-widget" data-tl-widget="dao-dong-dieu-hoa"></div>
```

- Đặt **giữa đoạn** vẫn chạy, nhưng đoạn đó bị cắt làm hai: phần tô vàng khi học sinh làm sai
  quiz chỉ phủ nửa đầu. Ưu tiên đặt ở cuối đoạn.
- Ở nơi chưa hỗ trợ widget (trang admin, xem trước), thẻ này chỉ là một `div` rỗng — vô hình,
  không gây lỗi.
- Widget hiện có:

| Tên (`data-tl-widget`) | Component | Dùng cho |
|---|---|---|
| `dao-dong-dieu-hoa` | `components/physics/HarmonicMotionLab.tsx` | Li độ là hình chiếu của chuyển động tròn đều; A, ω, φ |

### 4.2. Ba luật bắt buộc khi thêm widget mới

1. **`next/dynamic({ ssr: false })`** trong `components/lessons/TheoryWidget.tsx` — chunk chỉ tải
   khi cần, không vào JS ban đầu của trang bài học (AGENTS.md – mục tốc độ tải).
2. **Bọc `LazyErrorBoundary`** (`components/ui/LazyErrorBoundary.tsx`) — chunk lỗi/mất mạng chỉ
   hỏng đúng khối mô phỏng, phần chữ vẫn đọc được.
3. **Chỉ mount sau một tương tác** (nút "Mở mô phỏng") — `dynamic({ssr:false})` mount ngay lúc
   hydrate trang đầu có thể phát sinh `ChunkLoadError` mà boundary không bắt (đã kiểm thực nghiệm,
   `perf4/RESULT.md` §6). Nút mở cũng chính là nhịp "dự đoán trước khi xem".

Widget **không** gọi Supabase, không đọc `localStorage`, không nhận props từ HTML (muốn cấu hình
thì thêm prop và đọc `data-*` trong `TheoryWidget.tsx`).

### 4.3. Thêm widget mới = 3 bước

1. Viết component (client, tự chứa state, có `aria-label`, tôn trọng `prefers-reduced-motion`).
2. Thêm 1 mục vào hằng `WIDGETS` trong `components/lessons/TheoryWidget.tsx` (tên + tiêu đề + gợi ý).
3. Chèn thẻ `data-tl-widget` vào `body_html` và **đo lại dung lượng JS trang bài** trước khi báo xong.

---

## 5. Quy trình soạn một bài (1 bài/phiên)

Vì SGK của thầy là **PDF scan ảnh, không có lớp text** (xem
`docs/memory/reference_sgk_pdf_text_cache.md`):

| Bước | Việc | Ghi chú |
|---|---|---|
| A | Đọc ảnh PDF **qua subagent** → chép ra `<tên-pdf>-text/baiNN-slug.md` cạnh file PDF | Ảnh không nằm lại context chính; lần sau đọc `.md` rẻ hơn nhiều |
| B | Viết "bản đồ bài" ~15 dòng: YCCĐ/mục nào, phần nào để HS tự khám phá, ví dụ thật lấy ở đâu | Thầy duyệt nhanh trước khi viết HTML |
| C | Viết HTML theo khuôn 6 nhịp, giữ `<h3>` + `summary_html` | Nguồn: `scripts/data/ly-thuyet-tuong-tac/<bài>.body.html` + `.summary.html` |
| D | Áp + xem trước cục bộ | `node scripts/apply-theory-content.mjs --lesson <id> --item <id> --body … --summary …` rồi `npm run dev` |
| E | Đăng: PATCH REST (thầy chạy, cần service role key) → `bash scripts/deploy.sh` → kiểm 375px | Lệnh in sẵn ở bước D; xem `docs/memory/feedback_lesson_item_edit_via_rest.md` |
| F | Gắn quiz "Kiểm tra hiểu bài" cho mục đó | Skill `soan-quiz-ly-thuyet` (≥18 câu, `quiz_min_correct` = 75%) rồi `scripts/publish-theory-quiz.mts --lesson <id>` |

Bước F là phần **đo được**: không có quiz thì không biết viết lại có hiệu quả hay không. Ưu tiên
gắn quiz cho các mục đang dạy trước, vì chỉ 1/81 mục lý thuyết hiện có quiz (đo 01/10/2026).

---

## 6. Checklist trước khi báo hoàn thành

- [ ] Giữ `<h3>` cho từng đoạn; `summary_html` không rỗng.
- [ ] Không có ảnh base64; ảnh mới ≤1200px (nén trước khi đăng).
- [ ] Ví dụ đời thường + ít nhất 1 con số thật kèm đơn vị.
- [ ] 3 bẫy + 3–5 câu tự kiểm (đáp án nằm trong `<details>`, không lộ sẵn).
- [ ] Widget (nếu có) nằm ở ranh giới đoạn, có `aria-label`, không thêm round-trip Supabase.
- [ ] Mở thử 375px bằng mắt: không tràn ngang, chữ ≥15px, nút bấm được bằng ngón tay.
- [ ] So dung lượng bundle JS trang `/lop-hoc/bai` trước/sau nếu có thêm widget.
- [ ] Nếu có quiz: `npx tsx scripts/publish-theory-quiz.mts --dry-run` sạch lỗi trước khi đăng.

---

## 7. Những điều KHÔNG làm

- Không viết lại hàng loạt nhiều bài trong một phiên — mỗi bài ~9 KB HTML + quiz, làm loạt sẽ
  không kiểm được chất lượng và đốt token vô ích.
- Không đổi cấu trúc `<h3>` / `summary_html` (phá "Ôn ngay" và khối tóm tắt).
- Không thêm round-trip Supabase mới cho trang bài học; dữ liệu tĩnh nằm trong `public/data`.
- Không nhúng `<iframe>`, thư viện nặng, hay JS chạy ngay khi tải trang cho widget.
- Không đưa nội dung của bài sau vào bài trước (ví dụ: Bài 1 lớp 11 **không** định nghĩa chu kì
  $T$, tần số $f$ — SGK để dành cho Bài 2).
- Không tự chạy PATCH/migration bằng service role key trong phiên agent (AGENTS.md).

---

## 8. Trạng thái pilot (01/10/2026)

- Bài mẫu: **Vật lí 11 – Bài 1. Dao động điều hoà**, mục `lesson_items.id = 2` (bài 20).
  Nguồn: `scripts/data/ly-thuyet-tuong-tac/bai20-dao-dong-dieu-hoa.{body,summary}.html`.
- Widget pilot: `dao-dong-dieu-hoa` — con lắc lò xo + điểm M quay tròn + bóng Q + đồ thị một chu kì,
  thanh trượt $A$, $\omega$, $\varphi$.
- Hạ tầng đã thêm: `components/lessons/TheoryContent.tsx` (cắt chuỗi tại thẻ widget rồi bọc đoạn
  theo `startIndex`), `components/lessons/TheoryWidget.tsx` (đăng ký + lazy + boundary),
  `splitTheoryWidgets`/`wrapTheorySections(…, startIndex)` trong `features/lessons/theory-sections.ts`,
  khối CSS `.tl-*` trong `app/globals.css`, script `scripts/apply-theory-content.mjs`.
- Việc tiếp theo: thầy duyệt nội dung trên 375px → PATCH + deploy → gắn quiz 18 câu cho mục 2 →
  đo (số lượt mở mô phỏng không đo được, nhưng điểm quiz và tỉ lệ đúng theo YCCĐ thì đo được).

---

## Phụ lục — tự chụp ảnh kiểm ở 375px (không cần mở tay trình duyệt)

Chrome headless CLI trên máy này **luôn dựng layout 500px** rồi cắt ảnh theo `--window-size`
(đã đo bằng cách in `document.documentElement.clientWidth` ra ảnh: luôn = 500), nên ảnh
`--window-size=375,812` là ảnh *cắt* của layout 500px — dễ tưởng nhầm là tràn ngang. Muốn đo
đúng 375px, nhúng trang vào `<iframe width="375">`:

```bash
# 1. Tạo tạm public/__tmp-frame.html: <iframe src="/lop-hoc/bai/?id=20#theory-sec-2-3" style="width:375px;height:5400px;border:0"></iframe>
# 2. Chụp (cửa sổ cao bằng iframe để thấy hết nội dung), rồi cắt lát bằng Pillow
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --no-sandbox --disable-crash-reporter --disable-breakpad --hide-scrollbars --no-first-run \
  --user-data-dir=/tmp/chrome-shot --window-size=500,5400 --virtual-time-budget=15000 \
  --screenshot=.preview/full.png "http://localhost:3020/__tmp-frame.html"
# 3. XOÁ file tạm trong public/ ngay sau khi chụp (không để lọt vào bản build)
```

Mẹo: `#theory-sec-<item>-<n>` làm trang **tự mở** mục lý thuyết và cuộn tới đúng đoạn, nên
không cần bấm gì. Kết nối thẳng Chrome DevTools Protocol vào tab không nhận lệnh trên Chrome
154 headless (đã thử: socket mở rồi đóng 1006; đi qua browser endpoint thì lệnh theo `sessionId`
không phản hồi) — đừng mất thời gian viết lại, dùng iframe + CLI.

