# Đọc file đề Word (kiểu Azota) → câu hỏi chấm điểm

## Cấu trúc đề thường gặp

Đề của thầy theo mẫu thi tốt nghiệp từ 2025, có thể có 1–3 phần:

| Tiêu đề trong file | Loại câu | Ghi chú |
|---|---|---|
| `PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn` | `multiple_choice` | 4 phương án A–D, 1 đúng |
| `PHẦN II. Câu trắc nghiệm đúng sai` | `true_false` | mỗi câu 4 ý a/b/c/d, mỗi ý Đ hoặc S |
| `PHẦN III. Câu trắc nghiệm trả lời ngắn` | `short_answer` | đáp án là **một số**, ≤ 4 ký tự |

Nhiều đề (đặc biệt đề 15 phút / đề chương) **không có tiêu đề phần** — chỉ một mạch
`Câu 1.` … `Câu n.`, tất cả 4 phương án A–D → coi hết là `multiple_choice`.

Kết đề thường có dòng `---HẾT---`. Sau đó có thể có **bảng đáp án** và **phần lời giải**.

## Mốc để cắt

- **Câu:** `Câu 1.` / `Câu 1:` / `**Câu 1.**` (in đậm). Đánh số lại từ 1 theo thứ tự xuất hiện
  trong gói (gộp cả 3 phần thành một mảng `questions`).
- **Phương án Phần I:** `A.` `B.` `C.` `D.` hoặc `A)` … — thường 2 phương án / dòng, ngăn bằng
  tab. Gộp lại rồi tách theo nhãn.
- **Ý đúng–sai:** `a)` `b)` `c)` `d)` (đôi khi trong bảng "Phát biểu | Đúng | Sai").
  Tiền tố Azota `a) [1, NB] …` → **bỏ** `[1, NB]`, LMS không có trường ma trận.

## Lấy đáp án

1. **Dấu `*`** ở đầu phương án đúng: `*A. …` hoặc `… \t *D. …` → `answer` = chỉ số (A=0, B=1,
   C=2, D=3). Đây là quy ước hay gặp nhất trong file của thầy.
2. **Dòng "Đáp án"** ngay sau câu: `Đáp án: B`, `Đáp án đúng: C`, `Đáp số: 19`.
3. **Bảng đáp án cuối file:** hàng `Câu | 1 | 2 | 3 …` và `Chọn | B | A | D …`; Phần II là
   bảng cột-là-số-câu, 4 hàng `a) b) c) d)` ghi `Đ`/`S`.
4. Đúng–sai còn có dạng `Đáp án: a) Đ  b) Đ  c) S  d) Đ` hoặc `Đúng: a, d`.

Nếu **không tìm được đáp án** cho một câu → không đoán bừa: tự giải câu đó, ghi đáp án mình
tính và **nêu rõ trong lời cho người dùng** là câu này tự suy đáp án.

## Lấy / viết lời giải

- Đoạn `Lời giải` / `Giải` / `HD` / `Hướng dẫn` ngay sau câu (trước `Câu` kế tiếp) → `explanation`.
- File thường **chỉ có lời giải ở một số câu**. Câu nào trống → **tự viết 1–3 câu** giải thích
  ngắn gọn, đúng trọng tâm. Không để `explanation` rỗng (trang cảnh báo; câu đúng–sai/ngắn nên
  luôn có).
- Trả lời ngắn: **tự tính lại bằng số hai lần**; nếu ra khác đáp án trong file → tin phép tính
  của mình, ghi chú cho người dùng.

## Công thức (MathType → `$...$`)

Đọc `out/equations/sheet_NN.png`, gõ lại LaTeX **tối giản** (chạy với KaTeX mặc định, không gói
ngoài). Ghi vào `eq_index.json`.

| Ảnh | LaTeX |
|---|---|
| phân số chồng `a/b` | `\frac{a}{b}` — dạng nghiêng thì `a/b` |
| `v₀`, `s₁`, `t²` | `v_0`, `s_1`, `t^2` — nhiều ký tự bọc ngoặc: `10^{-3}`, `v_{max}` |
| `6,02.10²³` | `6{,}02 \cdot 10^{23}` (giữ **dấu phẩy** thập phân — quy ước SGK VN) |
| `2 × 10⁻³` | `2 \times 10^{-3}` |
| `√`, `∛` | `\sqrt{}`, `\sqrt[3]{}` |
| `≈ ≤ ≥ ≠` | `\approx \le \ge \ne` |
| `⇒ ⇔ →` | `\Rightarrow \Leftrightarrow \to` |
| `Δv`, `α β γ ρ ω` | `\Delta v`, `\alpha \beta \gamma \rho \omega` |
| vector `v⃗` | `\vec{v}` |
| `25°C` | `25^\circ\text{C}` hoặc `25\,^\circ\mathrm{C}` |
| gạch trên `x̄` | `\overline{x}` |

Chỉ số tiếng Việt (`T_đ`, `s_{đầu}`) → dùng `T_{d}`, `s_{dau}` cho chắc (`\text{}` có thể không có).

Công thức đứng riêng cả dòng → `$$...$$`; nằm trong câu → `$...$`. **Số dấu `$` phải chẵn.**

## HTML cho `question` / `explanation` / `theory_html`

`build_bundle.py` tự bọc `<p>` cho `question`/`explanation` nếu là văn bản thường. Khi tự viết
HTML, dùng đúng class (khớp bộ convert của trang admin):

| Phần tử | Class |
|---|---|
| `<h2>` | `text-xl font-bold mt-3 mb-1.5` |
| `<h3>` | `text-lg font-semibold mt-2 mb-1` |
| `<p>` | `text-base leading-relaxed my-2` |
| `<ul>` | `list-disc list-inside my-2 ml-4` |
| `<ol>` | `list-decimal list-inside my-2 ml-4` |
| `<li>` | `my-1` |
| `<strong>` | `font-bold` |

Không dùng `<h1>`. Không `<script>`/`<style>`/`on*=`.

### Ảnh trích từ file gốc → `raster_images[]` (ưu tiên số 1)

"Như hình bên", đồ thị `v–t` / `x–t`, mặt phẳng nghiêng, sơ đồ lực: **thử trích đúng ảnh
trong file gốc trước** — rẻ gần như miễn phí (chạy lệnh, không cần LLM nhìn/vẽ/soát lại),
và giữ đúng hình thầy cô đã làm thay vì một bản vẽ lại có thể lệch chi tiết.

- **`.docx`**: ảnh nhúng nằm sẵn trong file zip.
  ```bash
  unzip -o de.docx "word/media/*" -d out/docx_media
  ```
  Đối chiếu thứ tự ảnh trong `out/docx_media/` với thứ tự xuất hiện trong văn bản (mở
  `word/document.xml` hoặc chỉ nhìn đề đã render) để biết ảnh nào của câu nào.
- **PDF xuất từ Word**: nếu hình gốc là ảnh chèn (đồ thị vẽ bằng Excel/GeoGebra rồi chụp/dán
  vào Word, ảnh chụp, sơ đồ scan) thì PDF vẫn giữ nguyên ảnh đó dạng đối tượng nhúng, trích
  bằng `pdfimages`:
  ```bash
  pdfimages -all -p de.pdf out/pdf_img   # ra out/pdf_img-<trang>-<số>.png/.jpg
  ```
  Tên file có kèm số trang → khớp thẳng với trang chứa câu hỏi đó, không cần đoán.
- Nếu hình là **Word tự vẽ bằng shape/canvas** (đường thẳng/mũi tên vẽ trực tiếp, không phải
  ảnh chèn) thì hai lệnh trên sẽ không ra gì — thử cắt đúng vùng hình từ ảnh trang đã render
  (`out/page-N.png`, xem mục "Đọc đề đã render") bằng toạ độ (Pillow `Image.crop`), chỉ cần
  nhìn một lần để lấy toạ độ, không phải vòng vẽ-soát lặp lại.
- Không trích/cắt được sạch (ảnh vỡ, chữ trong hình bị mất nét, hình cần ghép nhiều chi tiết
  rời) → mới rơi xuống vẽ SVG bên dưới.

Ảnh trích ra nén ~1400px JPEG 0.8, base64 vào `raster_images[]`:

```jsonc
{ "name": "do-thi-v-t.jpg", "dataUri": "data:image/jpeg;base64,…",
  "alt": "Đồ thị v-t", "placeholder": "media/do-thi-v-t.jpg" }
```

Dùng đúng `media/do-thi-v-t.jpg` làm `src` trong HTML — trang thay bằng URL Storage lúc
Đăng — và bọc `<img>` trong khung nền sáng bo góc để không chỏi với nền tối `#0B1020`:

```html
<figure class="fig">
  <div class="rounded-lg bg-white p-2">
    <img src="media/do-thi-v-t.jpg" alt="Đồ thị v-t" class="w-full h-auto rounded" />
  </div>
  <figcaption>Đồ thị vận tốc – thời gian</figcaption>
</figure>
```

### Đồ thị / hình vẽ → SVG nội tuyến (chỉ khi không trích được ảnh gốc)

**Đồ thị hàm số thì dùng `scripts/svglib.py`** (`Plot.axes/ytick/ttick/curve/marker/label`),
đừng dựng tay — lớp đó đã chặn sẵn ba lỗi hay gặp: mũi tên/nhãn trục tràn viewBox, đường cong
cắt ngang chữ số trên trục, nhãn đường đặt lạc khỏi đường của nó. Xem docstring đầu file.
Phần dưới đây là quy ước chung, cần cho hình vẽ tay (sơ đồ lực, mặt phẳng nghiêng…).
Nền site tối `#0B1020`:

```html
<figure class="fig">
  <svg viewBox="0 0 320 200" xmlns="http://www.w3.org/2000/svg">
    <line x1="30" y1="170" x2="300" y2="170" stroke="currentColor" stroke-opacity="0.4"/>
    <line x1="30" y1="170" x2="30" y2="20"  stroke="currentColor" stroke-opacity="0.4"/>
    <path d="M30 170 L 240 40" fill="none" stroke="#60A5FA" stroke-width="2"/>
    <text x="292" y="185" fill="currentColor" font-size="11">t</text>
    <text x="14" y="26"  fill="currentColor" font-size="11">v</text>
  </svg>
  <figcaption>Đồ thị vận tốc – thời gian</figcaption>
</figure>
```

Nét/chữ `stroke="currentColor"` / `fill="currentColor"` — **không bao giờ** `#000`. Nhấn:
`#60A5FA` xanh, `#34D399` lục, `#F59E0B` hổ phách. `viewBox`, không đặt `width`/`height`.
KaTeX không chạy trong SVG → nhãn dùng `<text>` unicode (`v₀`, `Δt`) hoặc để ở `<figcaption>`.

## Ví dụ một câu mỗi loại (trong `draft.json`)

```json
{ "type": "multiple_choice",
  "question": "Một ô tô chuyển động chậm dần đều với $v_0 = 20$ m/s, $a = -2$ m/s². Quãng đường đến khi dừng là",
  "options": ["50 m", "100 m", "200 m", "400 m"],
  "answer": 1,
  "explanation": "$s = \\dfrac{v_0^2}{2|a|} = \\dfrac{400}{4} = 100$ m." }
```

```json
{ "type": "true_false",
  "question": "Xét chuyển động rơi tự do (bỏ qua sức cản, $g = 10$ m/s²):",
  "statements": [
    { "text": "Là chuyển động thẳng nhanh dần đều.", "answer": true },
    { "text": "Vận tốc tỉ lệ với bình phương thời gian.", "answer": false },
    { "text": "Quãng đường sau $t$ giây là $s = \\tfrac12 g t^2$.", "answer": true },
    { "text": "Hai vật khác khối lượng rơi từ cùng độ cao chạm đất cùng lúc.", "answer": true } ],
  "explanation": "Rơi tự do: $v = gt$ (tỉ lệ với $t$), $s = \\tfrac12 gt^2$; gia tốc $g$ như nhau với mọi vật." }
```

```json
{ "type": "short_answer",
  "question": "Vật rơi tự do từ độ cao 45 m, $g = 10$ m/s². Thời gian rơi (giây)?",
  "answer": "3",
  "explanation": "$t = \\sqrt{2h/g} = \\sqrt{9} = 3$ s." }
```
