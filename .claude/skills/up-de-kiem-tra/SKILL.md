---
name: up-de-kiem-tra
description: >-
  Nhận MỘT file đề trắc nghiệm PDF/Word kiểu Azota ("Câu 1.", A–D, đáp án đánh dấu "*",
  có/không PHẦN I/II/III, MathType) và đăng vào mục Kiểm tra/Luyện tập của đúng Lớp →
  Chương → Bài trên LMS thachlab, chấm tự động. Dùng khi đính kèm file đề và nói "up đề
  này", "đăng đề kiểm tra", "đưa đề lên thachlab", "up đề lên lớp X bài Y". Đường chính:
  trang /quan-tri/dang-de với dòng "Chủ đề:"/"Dạng:" mỗi câu; JSON qua /quan-tri/nhap-bai
  chỉ khi cần vẽ SVG/ảnh scan. KHÁC dang-bai-hoc-thachlab (trọn bài từ .tex) và
  de-vat-ly-thpt (xuất Word, không ghi DB).
---

# Up đề kiểm tra Word → mục Kiểm tra/Luyện tập trên thachlab

## Trước tiên: hỏi xem người dùng có tự đăng được không

Trang **Đăng đề** `/quan-tri/dang-de` đọc thẳng file `.docx` hoặc văn bản dán vào: tách câu,
lấy đáp án dấu `*`, đổi công thức Office Math sang `$…$`, gom ảnh, và có bảng **Phân loại câu**
để chọn yêu cầu cần đạt + dạng cho từng câu — rồi Đăng, **không tốn token**. Xem
`docs/DANG-DE-TU-WORD.md`.

Chỉ dùng skill này khi đường đó không đi được:

- File còn công thức **MathType dạng OLE** mà người dùng không muốn/không thể bấm
  *Convert Equations → Microsoft Office Math* (trang sẽ báo "còn N công thức MathType").
- Đề là **PDF** hoặc ảnh chụp/scan.
- Cần **vẽ lại hình bằng SVG**, hoặc viết lời giải còn thiếu cho nhiều câu.
- Người dùng muốn mình **gắn nhãn thay** (chủ đề + dạng) cho cả đề thay vì chọn tay trên trang.

Nếu chỉ là file Word gõ công thức bằng Word (Alt + =) và có dấu `*` ở đáp án: **chỉ cần chỉ cho
người dùng trang đó**, đừng tự làm thay. Đề đã ở mẫu Azota (đáp án trong bảng sau HẾT) thì
skill `azota` bước 6 (`xuat_thachlab.py`) dựng sẵn file Word cho trang này, kèm nhãn.

## Đường chính — văn bản kiểu Azota vào /quan-tri/dang-de

Trang Đăng đề nhận **văn bản** (không phải JSON): đúng cách trình bày Azota mà thầy cô vẫn gõ,
cộng hai dòng nhãn cuối mỗi câu. Đây là đường đi cho PDF/MathType/đề cần viết lời giải:

```
PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn
Câu 1. Tốc độ trung bình của một vật được tính bằng
A. quãng đường nhân thời gian.   *B. quãng đường chia thời gian.
C. thời gian chia quãng đường.   D. quãng đường cộng thời gian.
Lời giải: $v_{tb} = \dfrac{s}{t}$.
Chủ đề: Nêu được định nghĩa tốc độ trung bình
Dạng: lý thuyết

PHẦN II. Câu trắc nghiệm đúng sai
Câu 2. Một vật chuyển động thẳng đều với tốc độ 5 m/s.
*a) Quãng đường đi được trong 4 s là 20 m.
b) Vận tốc của vật thay đổi theo thời gian.
…
Lời giải: …
Chủ đề: Mô tả chuyển động thẳng đều
Dạng: bài tập

PHẦN III. Câu trắc nghiệm trả lời ngắn
Câu 3. … (ghi số)
Đáp án: 2
Lời giải: dòng 1
dòng 2 (lời giải nhiều dòng: từ "Lời giải:" tới hết câu)
Chủ đề: …
Dạng: bài tập
```

Quy tắc: `*` trước phương án đúng / ý Đúng; Phần III dòng `Đáp án:`; `Lời giải:` kéo dài
tới hết câu (bỏ dòng nhãn); `Chủ đề:` = **tên yêu cầu cần đạt đúng như danh mục khối** (cũng
nhận `YCCĐ:` / `Năng lực:`); `Dạng:` chỉ nhận `lý thuyết` | `bài tập`. Nhãn đặt ở đâu trong
câu cũng được, trang tự bỏ khỏi đề dẫn. Công thức trong `$…$`. Số câu liên tục cả đề.

1. **Đọc đề** như mục "1. Đọc đề đã render" bên dưới (PDF → ảnh → subagent chép text).
2. **Soạn `de.txt`** theo mẫu trên: đáp án, lời giải (viết bù câu thiếu, giải lại Phần III),
   và **nhãn cho từng câu** — chọn trong danh mục khối, đừng đặt theo trí nhớ (xem mục
   "`topic` + `form`" bên dưới về hai tầng bài → yêu cầu cần đạt).
3. **Soát nhãn** (REST anon-key, tự đọc `.env.local`):
   ```bash
   python3 .claude/skills/up-de-kiem-tra/scripts/soat_nhan.py de.txt --grade 12 --fix
   ```
   `✗` = tên không có trong danh mục (kèm tên gần nhất) hoặc câu thiếu nhãn → sửa `de.txt`,
   chạy lại tới khi dòng cuối là `Nhãn: n/n câu đủ`. `--fix` tự chuẩn hoá hoa/thường theo
   danh mục. Chủ đề thật sự mới: nói với người dùng, tạo ở trang Chủ đề câu hỏi trước.
4. **Dán vào trang** `https://thachlab.id.vn/quan-tri/dang-de` (người dùng đã đăng nhập admin;
   chưa thì dừng, nhờ họ đăng nhập). Văn bản dài không gõ tay được — dùng relay như mục
   "4. Đăng qua trang admin", chỉ khác đích:
   ```bash
   python3 .claude/skills/up-de-kiem-tra/scripts/paste_relay.py de.txt --target https://thachlab.id.vn/quan-tri/dang-de/ &
   ```
   JS giải mã trong docstring của script gán vào `textarea` đầu tiên — ở trang này chính là ô
   nội dung đề. Trang tách câu ngay khi có văn bản.
5. Đọc cột phải: dòng `n/n câu dựng được`, ghi chú vàng (câu thiếu đáp án/phương án), bảng
   đáp án, và bảng **Phân loại câu** phải là **n/n câu đã gắn đủ**, không ô nào viền vàng.
6. **Bấm nút "AI gắn nhãn"** (biểu tượng Sparkles, cạnh bảng Phân loại câu) đúng 1 lần trước
   khi đăng — nút này gắn cả `topic`/`form` CÒN THIẾU lẫn **độ khó (Dễ/Trung bình/Khó)**, kể cả
   khi câu đã có sẵn `Chủ đề:`/`Dạng:` từ văn bản dán vào (định dạng dán không có dòng cho độ
   khó, nên câu nào cũng cần qua bước này để không phải chạy backfill riêng sau — xem
   `scripts/backfill-question-bank-difficulty.mts`, chỉ nên dùng cho đề CŨ đã lỡ đăng thiếu).
   Đợi toast "AI đã gắn nhãn cho n/n câu", xem lại vài câu trong bảng Phân loại nếu nghi ngờ mức
   độ AI chọn chưa hợp lý (sửa tay được, đổi nguồn từ "(AI)" sang "(GV)").
7. Mục 3: Tên đề, thời gian, Lớp → Chương → Bài, chọn **Kiểm tra** (mặc định) / Luyện tập /
   BTVN; mục đã có đề thì "Giữ + thêm" hay "Thay" — hỏi người dùng nếu đề cũ là đề thật.
   Bấm **Đăng đề**, theo dõi log, mở link bài học kiểm tra.

Ảnh: trang chỉ nhận ảnh khi đọc từ `.docx`; văn bản dán không mang ảnh. Đề có hình cần vẽ
SVG hoặc ảnh scan → đi đường dự phòng bên dưới.

### Có sẵn file `.docx` đã chuẩn (từ skill `azota`) — kéo-thả bằng relay, không gõ lại thành văn bản

Nếu đề đã qua `xuat_thachlab.py` (skill `azota`) — tức đã có `*` trước đáp án, `Lời giải:`,
`Chủ đề:`/`Dạng:` sẵn trong file — **đừng đọc lại rồi gõ thành `de.txt`**, phí token và dễ gõ
sai công thức. Trang Đăng đề có nút "Tải file Word" (một `<input type="file">` ẩn) nhận
thẳng `.docx`, tự trích câu/đáp án/ảnh — nhưng Browser pane không kéo-thả file thật từ Finder
được và không gán `input.value` bằng JS (trình duyệt chặn vì lý do bảo mật). Cách chạy được:
dùng `paste_relay.py` y hệt bước dán văn bản, nhưng bên phía trang đích tạo một `File` từ
byte giải mã rồi gán vào `input.files` (được phép, khác `.value`):

```bash
python3 .claude/skills/up-de-kiem-tra/scripts/paste_relay.py de_thachlab.docx \
  --target https://thachlab.id.vn/quan-tri/dang-de/ &
```

`navigate` tab tới URL relay in ra, đợi ~3s quay lại trang đích kèm `#b64=…`, rồi chạy JS này
(khác đoạn giải mã textarea ở "Đăng qua trang admin" — đây tạo file, không gán text):

```js
const b64 = location.hash.replace(/^#b64=/, '');
const bin = atob(b64);
const u8 = new Uint8Array(bin.length);
for (let i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
history.replaceState(null, '', location.pathname);
const file = new File([u8], 'de_thachlab.docx',
  { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
const dt = new DataTransfer();
dt.items.add(file);
const input = document.querySelector('input[type=file]');
input.files = dt.files;
input.dispatchEvent(new Event('change', { bubbles: true }));
```

Trang tự đọc file, hiện `n/n câu dựng được · N ảnh`. Bấm **"AI gắn nhãn"** một lần (xem
mục "Đăng qua trang admin" bước 6 — gắn cả độ khó, kể cả khi file `.docx` đã có sẵn
`Chủ đề:`/`Dạng:`) trước khi set Lớp/Chương/Bài/Tên đề/Thời gian và bấm Đăng như bình thường — các `<select>` phải gán bằng **native setter + `change`**
(giống textarea, React bỏ qua gán trực tiếp):

```js
function setSelect(sel, value) {
  const setter = Object.getOwnPropertyDescriptor(Object.getPrototypeOf(sel), 'value').set;
  setter.call(sel, value);
  sel.dispatchEvent(new Event('change', { bubbles: true }));
}
```

Nút Đăng đề bị `disabled` khi còn nhãn "(không có trong danh mục)" hoặc còn cảnh báo đỏ
"Thiếu hình ở N câu" (site tự dò câu nhắc "hình vẽ/đồ thị" mà không thấy ảnh — xem skill
`dang-de-hang-loat` mục "Thiếu hình" về cách xử lý). Muốn biết vì sao nút đang khoá, đọc
`btn.disabled` bằng `javascript_tool` thay vì đoán qua ảnh chụp màn hình.

**Nhiều agent chạy song song → KHÔNG để mỗi agent tự làm bước Đăng này** (một Browser pane
dùng chung trong phiên, agent nọ điều hướng tab đè lên agent kia — xem
`feedback_batch_agent_upload_efficiency`). Để từng agent dừng lại ở việc tạo ra file
`de_thachlab.docx` đã soát sạch, rồi **phiên chính tự đăng tuần tự** bằng kỹ thuật relay ở
trên cho từng file một — vừa an toàn vừa không cần agent nào chạm service-role key.

**`paste_relay.py` chiếm cứng cổng 8791 — có phiên khác đang chạy song song (rất hay gặp,
xem `project_thachlab_concurrent_sessions`) thì bị `OSError: Address already in use`.** Đừng
`kill` tiến trình đang chiếm cổng (có thể là việc dở của phiên khác) — thêm `--port <số khác>`
và `navigate` tab tới đúng `http://127.0.0.1:<port>/relay.html`.

**Browser pane bị "hidden" giữa phiên** (người dùng chuyển sang xem pane khác trong app) làm
mọi lệnh dựa trên ảnh chụp màn hình (`computer`: click theo toạ độ, `type`, `screenshot`) báo
lỗi "the Browser pane is not displayed". `find` (lấy `ref`), `read_page`, `javascript_tool`
vẫn chạy bình thường vì không cần khung hình — và bất ngờ là **`form_input` cũng chạy được cả
khi pane ẩn** (test 27/9/2026: gán được cả `<input type=text>`/`type=number` lẫn `<select>`
khi pane hidden). Gặp lỗi "not displayed": chuyển hẳn sang `find` lấy `ref` rồi `form_input`
để điền field, và `btn.click()` qua `javascript_tool` để bấm nút — không cần đợi pane hiện lại.

**Sửa nội dung một câu ngay trên trang (ô nhỏ trong bảng preview, vd đáp án Phần III) bằng
`javascript_tool` gán trực tiếp `input.value` qua native setter + `dispatchEvent('input')`
KHÔNG chắc cập nhật state React của trang này** — DOM property đổi thật (đọc lại thấy giá trị
mới), nhưng khung cảnh báo lỗi tổng hợp phía dưới (vd "đáp án dài quá 4 ký tự") vẫn giữ nguyên
văn bản cũ, không tính lại (test 27/9/2026, đề "Trấn Biên Đồng Nai"). Đáng tin hơn: sửa thẳng
file `.docx` nguồn (`python-docx`, tìm đúng paragraph "Đáp án: …") rồi `paste_relay.py` lại từ
đầu — chậm hơn một nhịp nhưng chắc ăn, và đằng nào cũng cần giữ file nguồn đúng để lưu log.

## Đường dự phòng — gói JSON qua /quan-tri/nhap-bai (khi cần hình SVG / ảnh scan)

Người dùng thả một file đề trắc nghiệm — **`.pdf` (nhanh nhất, khuyên dùng)** hoặc `.docx`. Skill:

1. Đọc đề đã render, **phiên âm công thức sang `$...$`**. PDF → đọc thẳng; docx → phải render trước.
2. Phân loại từng câu → `multiple_choice` / `true_false` / `short_answer`, lấy **đáp án**
   (dấu `*` hoặc dòng "Đáp án") + **lời giải** (dòng "Lời giải"/"Giải").
3. Dựng gói `thachlab.lesson-bundle/v1` (khối `exam`; `theory_html` để rỗng nếu chỉ đăng đề —
   khi đó mục Lý thuyết của bài được giữ nguyên).
4. Đăng qua `https://thachlab.id.vn/quan-tri/nhap-bai`: dán gói bằng relay (xem mục "Đăng qua
   trang admin"), chọn Lớp→Chương→Bài, xem preview + bảng validate, tick **Kiểm tra**
   (mặc định) → **Đăng bài học**. (Nhãn `topic`/`form` trong gói tương đương hai dòng
   `Chủ đề:`/`Dạng:` của đường chính.)
5. Báo link `/lop-hoc/bai/?id=<id>` để kiểm tra.

Đây là thao tác lên **hệ thống sống** (DB + web học sinh đang dùng). Phần "An toàn" ở cuối
quan trọng ngang phần quy trình.

## Cấu trúc dữ liệu cần biết

- Cây nội dung: **Lớp → `chapters` → `lessons` → 5 mục** (`ly_thuyet`, `video`, `bai_tap_mau`,
  `luyen_tap`, `kiem_tra`) — xem `features/lessons/types.ts`.
- **"Kiểm tra" và "Luyện tập" KHÔNG chứa câu hỏi trực tiếp.** Cột `exam_ids` của chúng trỏ tới
  dòng trong bảng `exams`. Trang `/quan-tri/nhap-bai` tạo dòng `exams` từ khối `exam` của gói
  rồi tự gắn `exam_ids`. (Đây là lý do không "nhập" câu hỏi được ở trang Bài học — ở đó chỉ
  tick chọn đề đã có.)
- **Kiểm tra** = có tính giờ, nộp bài, lưu bảng điểm. **Luyện tập** = học sinh tự làm, xem đáp
  án ngay, không vào điểm. File tên "Kiểm tra…" → mặc định tick **Kiểm tra**; hỏi người dùng
  nếu muốn cả hai.
- Câu hỏi được chấm bằng `gradeExam` (`features/exams/types.ts`): mỗi câu cần `answer` đúng +
  `explanation`. Nội dung là **HTML thuần**, công thức để nguyên `$...$` / `$$...$$`.
- Ảnh: **ưu tiên trích thẳng ảnh gốc**, đừng vẽ lại nếu không cần — đề đã có ảnh nhúng
  (đồ thị vẽ bằng Excel/GeoGebra rồi chèn ảnh, ảnh chụp, sơ đồ scan) thì lấy đúng file đó
  (`.docx` → `word/media/*`; PDF → `pdfimages`), không tốn token vẽ/soát lại. **Nén trước
  khi encode base64** (rộng tối đa ~1200px, ví dụ `sharp` hoặc `magick <in> -resize 1200x -quality
  80 <out>`) — ảnh trích thẳng từ Word/PDF scan thường 2–5 MB, trang không tự nén khi upload lên
  Storage (xem quy tắc "Đăng nội dung — luôn tối ưu tốc độ tải" ở `AGENTS.md`). Base64 vào
  `raster_images[]`, `placeholder` dạng `media/<ten>.jpg`, dùng đúng chuỗi đó làm `src`.
  Bọc `<img>` trong khung nền sáng bo góc (xem `references/docx-de-format.md` §"Ảnh trích
  từ file gốc") để không chỏi với nền tối `#0B1020` của site. Trang tự upload lên Storage
  bucket `lesson-media`. **Không** commit ảnh, **không** cần deploy.
  Chỉ khi hình là **Word tự vẽ bằng shape/canvas** (không có file ảnh nhúng để trích, không
  cắt được vùng sạch từ trang PDF) mới vẽ lại bằng `<svg>` nội tuyến trong HTML câu hỏi (quy
  tắc màu: nét `stroke="currentColor"`, nhấn `#60A5FA`) — xem mục "`topic` + `form`" bên
  dưới về cách vẽ và soát hình SVG.

## Quy trình

### 1. Đọc đề đã render (text + công thức)

Công thức MathType trong file Word là **OLE** (`word/embeddings/oleObject*.bin`) — pandoc,
python-docx **không đọc được**, chỉ thấy ảnh WMF. Phải nhìn công thức đã render.

**Cách chính — thầy xuất PDF từ Word rồi thả file PDF.** Không cần LibreOffice, không đổi định
dạng gì. Tách trang thành ảnh cho nét:

```bash
pdftoppm -png -r 130 "duong/dan/de.pdf" out/page       # -> out/page-1.png, …
```

Nếu chỉ có `.docx` và **không xin được PDF**, tự render (cần LibreOffice):

```bash
soffice --version || echo "CẦN CÀI: brew update && brew reinstall --cask libreoffice"
mkdir -p out && soffice --headless --convert-to pdf --outdir out "duong/dan/de.docx"
pdftoppm -png -r 130 out/*.pdf out/page
```
Chạy nền (`run_in_background: true`); đề nhiều đối tượng nhúng có thể mất vài phút.

**Đọc ảnh trang trong subagent, không đọc thẳng ở phiên chính.** Một trang PNG ≈ 1,5k token
và nằm lại context đến hết phiên; đề 13 trang nhân với vài trăm request là hàng chục triệu
token. Spawn agent **`chep-de`** (đã ghim sonnet, xem `.claude/agents/`; `run_in_background: false`
— bước sau cần kết quả ngay), giao đúng việc chép đề:

> Đọc `out/page-*.png` (đề Vật lí THPT đã render). Chép lại **nguyên văn, đủ tất cả các
> trang**: số câu, đề bài, phương án A–D kèm **dấu `*` đánh dấu đáp án đúng**, phần
> "Lời giải" nếu có, mô tả hình vẽ/đồ thị. Công thức gõ sang `$...$` (LaTeX). Không tóm
> tắt, không bỏ câu nào. Trả về text thuần theo thứ tự câu.

**Đường "ngoài Claude" (thầy chốt 6/10/2026) — khi đề ≥ 10 trang, nhiều hình vẽ/đồ thị, hoặc
PDF scan mờ:** không chép trong Claude. Dừng lại và in cho Thạch khối sau để làm trên **Cursor
(Auto)**, rồi chờ file kết quả:

```
Mở Cursor tại thư mục có out/page-*.png, chế độ Auto, dán:
"Đọc toàn bộ out/page-*.png (đề Vật lí THPT). Chép nguyên văn đủ mọi trang: số câu, đề bài,
A–D kèm dấu * ở đáp án đúng, Lời giải nếu có, hình vẽ mô tả trong [hình: ...]. Công thức
viết $...$ (LaTeX). Không tóm tắt, không bỏ câu. Ghi ra out/de.txt"
→ nộp lại out/de.txt cho phiên này.
```
Nhận `out/de.txt` xong vẫn đi tiếp Bước 2 như thường; Claude chỉ đối chiếu số câu và đáp án
bị đánh `*` với ảnh ở vài câu ngẫu nhiên, không đọc lại cả đề. Không dán tên học sinh hay dữ
liệu cá nhân vào prompt Cursor.

Ảnh chết theo subagent; phiên chính chỉ nhận text. Nếu đề ngắn (≤ 3 trang) thì đọc thẳng
cũng được. Cùng lý do: đừng `Read` lại `de.pdf` sau khi đã có text.

Gõ lại công thức sang `$...$` theo `references/docx-de-format.md` §"Công thức".

Đối chiếu số câu (từ text thô nếu có `.docx`):

```bash
python3 -c "import docx; [print(p.text) for p in docx.Document('de.docx').paragraphs if p.text.strip()]" | grep -c '^Câu'
```

**Đếm số câu phải khớp đề gốc** trước khi qua bước 2.

### 2. Soạn `draft.json`

Theo mẫu trong đầu `scripts/build_bundle.py` và `references/docx-de-format.md`.

- Tách câu theo mốc `Câu n.` / `Câu n:`. Đánh số theo thứ tự xuất hiện.
- **Xác định loại câu** theo tiêu đề `PHẦN I/II/III` nếu có; nếu đề chỉ có một mạch "Câu 1..n"
  toàn 4 phương án A–D → tất cả là `multiple_choice`.
- **Đáp án:**
  - Trắc nghiệm: phương án có dấu `*` ở đầu (`*A.`, `*B.`…) là đáp án → `answer` = chỉ số 0–3.
    Nếu không có `*`, tìm bảng đáp án cuối file hoặc dòng "Đáp án: B".
  - Đúng–sai: dòng "Đáp án: a) Đ b) S c) Đ d) Đ" → `statements[k].answer`.
  - Trả lời ngắn: dòng "Đáp án:"/"Đáp số:" → chuỗi số (≤ 4 ký tự, phẩy thập phân).
- **Lời giải:** đoạn "Lời giải"/"Giải"/"Hướng dẫn" ngay sau câu → `explanation`. **Câu nào
  thiếu lời giải thì tự viết ngắn gọn** (1–3 câu, đủ để học sinh hiểu vì sao). Với trả lời
  ngắn: **tự giải ra số hai lần** để chắc đáp án.
- **`topic` + `form` cho từng câu — bắt buộc** (phân tích chủ đề & cảnh báo phụ đạo sống nhờ
  hai trường này; `build_bundle.py` chặn nếu thiếu):
  - `form`: `"ly_thuyet"` nếu câu hỏi lý thuyết / nhận biết / khái niệm; `"bai_tap"` nếu phải
    tính toán / vận dụng công thức. (Gần đúng: Phần I nhiều câu lý thuyết, Phần III toàn bài tập.)
  - `topic`: **đúng tên trong danh mục `question_topics` của khối** — không gọi tắt. Danh mục
    hai tầng: **bài học → yêu cầu cần đạt**; gắn vào *yêu cầu cần đạt* (vd "Viết phương trình
    dao động điều hoà") chứ đừng dừng ở tên bài ("Dao động điều hoà") — mục phụ đạo vẫn gom
    lên tầng bài, còn nhãn mịn mới cho thầy biết em hổng phần nào. Gắn ở mức cả bài là cảnh
    báo, không chặn.
    `ExamRunner` tra `topic_id` theo đúng tên, mà `tutoring_needs.topic_id` là NOT NULL: lệch một
    chữ (`"Nội năng"` thay vì `"Nội năng. Định luật 1 của nhiệt động lực học"`) là câu đó rơi khỏi
    mọi thống kê chủ đề mà **không báo lỗi ở đâu cả**. Không cần tra tay: chạy
    `build_bundle.py --grade <9|10|11|12>`, script tự tải danh mục rồi báo lỗi kèm tên gần nhất.
  - Chủ đề **thật sự mới** (danh mục chưa có): khai báo `--new-topic "Tên chủ đề"`. Trang nhập bài
    sẽ tạo chủ đề đó gắn sẵn vào đúng Chương → Bài đang chọn, nên nút "Ôn lại" của học sinh nhảy
    đúng chỗ ngay. Chỉ đặt tên mới khi chắc danh mục không có — đừng tạo bản gọi tắt của tên đã có.
- `question`, `options`, `explanation`: giữ `$...$`. Đồ thị "như hình bên/hình vẽ": **trước
  tiên thử trích ảnh gốc** (xem mục "Cấu trúc dữ liệu cần biết" phía trên và
  `references/docx-de-format.md` §"Ảnh trích từ file gốc") — chỉ khi không trích/cắt được
  mới vẽ `<svg>` chèn vào `question`, **bằng `scripts/svglib.py`** — đừng viết tay từ đầu:

  ```python
  import sys, math; sys.path.insert(0, '.claude/skills/up-de-kiem-tra/scripts')
  from svglib import Plot, txt, BLUE, GREEN, AMBER, AX

  f = lambda t: 10 * math.sin(2 * math.pi * t)
  p = Plot(w=370, h=215, ox=48, oy=105, sx=250, sy=6.5, tmax=1.06, ymax=11)
  p.axes(); p.ytick(10, '10', dashed_to=0.25); p.ttick(0.5, '0,5')
  p.curve(f, 0, 1.0)
  html = p.svg('Đồ thị li độ – thời gian')
  ```

  Lớp này đã xử lý sẵn ba lỗi từng phải sửa lại cả loạt hình: mũi tên/nhãn trục **tràn
  viewBox**, **đường cong cắt ngang chữ số** trên trục, và nhãn đường đặt xa đường của
  nó. Đọc docstring đầu file trước khi dùng; `python3 svglib.py` sinh trang demo 3 hình.

  Vẽ xong, soát theo hai bước — **đừng đảo thứ tự**:
  1. `ok, lines = check_bounds(list(FIGS.values()))` — bắt tràn viewBox bằng số học, không
     tốn ảnh. Còn `✗` thì nới `w`/`h` rồi chạy lại.
  2. Chỉ khi đã sạch mới **xem bằng mắt** (chồng chữ, nhãn lạc đường, sai pha thì chỉ mắt
     mới thấy): gom hình vào một trang HTML, mở trong Browser pane, đọc ảnh **trong
     subagent** — một trang PNG ≈ 1,5k token và nằm lại context đến hết phiên.
- `meta.title`: ưu tiên tiêu đề trong file; nếu chỉ là "Mã đề 0001" thì đặt theo chủ đề, vd
  `"Kiểm tra: Chuyển động biến đổi đều & Rơi tự do"`. `meta.duration_minutes`: theo đề, mặc
  định 45 cho đề kiểm tra 1 tiết, 15 cho đề 15 phút.
- **`theory_html`**: để `""` nếu chỉ đăng đề (mục Lý thuyết của bài giữ nguyên). Bài chưa có lý
  thuyết và người dùng muốn có phần ôn nhanh → soạn khối "Công thức trọng tâm" ngắn cho chủ đề
  của đề (~5–12 dòng, class Tailwind trong `references/docx-de-format.md` §"HTML").

### 3. Dựng gói + tự kiểm

```bash
python3 .claude/skills/up-de-kiem-tra/scripts/build_bundle.py draft.json --grade 12 -o bundle.json
```

Script chạy đúng bộ kiểm tra của trang admin (4 phương án, `answer` 0–3, 4 ý đúng–sai, đáp số
≤ 4 ký tự, `$` chẵn, không sót `\textbf{`/`\includegraphics{`, placeholder ảnh đã khai báo),
**cộng thêm soát nhãn**: thiếu `topic`/`form`, hoặc `topic` không có trong danh mục khối →
lỗi, kèm gợi ý tên gần nhất. Tên viết hoa/khoảng trắng lệch thì script tự chuẩn hoá theo danh
mục. Có `✕` thì sửa `draft.json` rồi chạy lại — đừng mở trình duyệt khi còn lỗi.

Dòng cuối in `Nhãn: n/n câu · k chủ đề` (kèm `· m câu còn ở mức cả bài` nếu có) — n/n mới
được đi tiếp; có `m` thì xem lại, chọn đúng yêu cầu cần đạt script gợi ý. `--grade` cần mạng (REST
anon-key, tự đọc `.env.local`); offline thì `--topics topics.json` với danh mục tải sẵn.

### 4. Đăng qua trang admin

Thao tác pane: **đừng `resize_window`** để emulate viewport — toạ độ click lệch khỏi ảnh
chụp, bấm trượt nút mà không báo lỗi. Dùng `ref` từ `find`/`read_page`, và `form_input`
cho `<select>`.

1. Mở `https://thachlab.id.vn/quan-tri/nhap-bai` trong Browser pane (người dùng đã đăng nhập
   admin — nếu chưa, **dừng, nhờ người dùng tự đăng nhập**).
2. **Dán gói trước, chọn bài sau.** Gói ~70 KB: không gõ tay vào textarea được, trang không
   có ô upload, và `cmd+v` / `fetch` localhost / `window.open` đều bị Browser pane chặn.
   Dùng relay:

   ```bash
   python3 .claude/skills/up-de-kiem-tra/scripts/paste_relay.py bundle.json &
   ```

   `navigate` tab tới URL relay script in ra → sau ~3 s tab tự quay về trang nhập bài với
   payload trong `#b64=…` → chạy đoạn JS trong docstring của script để giải mã và gán vào
   textarea (phải dùng **native setter** + `dispatchEvent('input')`, React bỏ qua `ta.value=`).
   Ô JSON nằm trong khối gập **"Nâng cao: dán gói JSON…"** ở đầu trang — script gán DOM thẳng
   nên gập/mở không ảnh hưởng giá trị, nhưng khối phải **mở** (bấm dòng tóm tắt) thì nút
   "Nạp gói" mới hiện ra bấm được (bước 4). Relay làm tab điều hướng nên **mọi lựa chọn
   Lớp/Chương/Bài trước đó mất sạch** — vì vậy làm bước này trước bước 3. Xong thì
   `pkill -f paste_relay.py`.
3. Mục 1: chọn **Lớp → Môn → Chương → Bài**. Nếu người dùng chưa nói rõ bài nào: hỏi, hoặc tra
   bằng REST anon-key (chỉ đọc):
   ```bash
   source <(grep -E '^NEXT_PUBLIC_SUPABASE' .env.local | sed 's/^/export /')
   curl -s "$NEXT_PUBLIC_SUPABASE_URL/rest/v1/chapters?select=id,title,subject_code,chapter_classes(class_id)&order=sort_order" \
     -H "apikey: $NEXT_PUBLIC_SUPABASE_ANON_KEY" -H "Authorization: Bearer $NEXT_PUBLIC_SUPABASE_ANON_KEY"
   curl -s "$NEXT_PUBLIC_SUPABASE_URL/rest/v1/lessons?select=id,chapter_id,title&chapter_id=eq.<ID>" \
     -H "apikey: $NEXT_PUBLIC_SUPABASE_ANON_KEY" -H "Authorization: Bearer $NEXT_PUBLIC_SUPABASE_ANON_KEY"
   ```
4. Mở khối **"Nâng cao"** (nếu relay chưa làm tab điều hướng qua bước khác khiến nó đóng lại),
   rồi bấm **Nạp gói**. Trang nạp gói vào cả mục 2 (Lý thuyết & dạng bài) và mục 3 (Đề).
5. Mục 3 (Đề luyện tập / kiểm tra): xem preview — từng câu tô đáp án đúng + lời giải. Lỗi
   chặn đăng (nếu có) hiện ở khung đỏ ngay trên nút **"Đăng bài học"** ở cuối trang; có lỗi
   thì sửa gói, dán lại. Mục 4 (**"Nhãn chủ đề trước khi đăng"**, ngay sau mục 3):
   - phải là **"đã gắn n/n câu"**, các chip chủ đề đều xanh (có trong danh mục khối);
   - chip vàng "chưa có trong danh mục" → để nguyên ô **"Tạo … chủ đề mới cho <bài>"** (tick sẵn):
     trang tạo chúng thành **yêu cầu cần đạt con** của chủ đề bài đang chọn;
   - dòng vàng "⚠ Còn gắn ở mức cả bài" → nhãn còn thô, sửa `draft.json` cho mịn nếu kịp;
   - nút Đăng bị chặn khi nhãn chưa đủ. Ô **"Đăng dù nhãn chưa đủ"** chỉ tick khi người dùng
     đồng ý bỏ số liệu phân tích cho những câu đó — nhãn được chốt lúc học sinh nộp bài, gắn
     sau **không** cứu được các lượt đã nộp.
6. Mục 5 (**"Gắn đề & xử lý nội dung đã có"**):
   - Tick **"Gắn vào Kiểm tra"** (mặc định cho skill này). Thêm **"Luyện tập"** nếu người dùng
     muốn học sinh luyện không tính điểm.
   - **Lý thuyết**: gói không có `theory_html` thì trang tự giữ nguyên mục cũ. Nếu gói có mà bài
     cũng đã có lý thuyết thật → chọn **Bỏ qua**, đừng đè.
   - **Đề cũ ở mục đã chọn**: nếu mục Kiểm tra/Luyện tập đã có đề → chọn **Thay** (trang tự xóa
     đề cũ, tránh tồn đọng) trừ khi người dùng muốn giữ.
7. **Đăng bài học**. Theo dõi log từng bước.
8. Mở `https://thachlab.id.vn/lop-hoc/bai/?id=<lesson_id>`, kiểm mục Kiểm tra hiện đề, số câu
   đúng, bấm thử một câu. Báo link cho người dùng.

### Dự phòng: không mở được trang admin

```bash
npx tsx scripts/upload-lesson.mts bundle.json --lesson <id> --class <id> --target kiem_tra --mode replace
```

Script hỏi `SUPABASE_SERVICE_ROLE_KEY` (nhập ẩn) — **chỉ dùng khi người dùng tự cung cấp key
ngay lúc đó**, không lấy từ memory phiên trước. Ảnh raster phải nén sẵn.

### Deploy — hầu như không cần

Nội dung + ảnh Storage **không cần deploy**. Chỉ chạy `./scripts/deploy.sh` khi có sửa **code**
(trang, component). Kiểm `git status --short` trước; working tree có thay đổi không liên quan
→ hỏi người dùng (xem memory `feedback_thachlab_deploy_scope`).

## An toàn — không thương lượng

- **Không bao giờ tự nhập mật khẩu** (đăng nhập admin, mật khẩu DB, service-role key) dù người
  dùng dán trong chat. Không có phiên admin trong Browser pane → dừng, nhờ người dùng đăng nhập.
- **Luôn xem preview + bảng validate** trước khi bấm Đăng. Không bỏ qua `errors`.
- Nếu mục Kiểm tra/Luyện tập của bài đã có đề thật → **hỏi** trước khi chọn "Thay". Riêng khi
  mục đó đang gom NHIỀU đề cùng lúc (kiểu "Đề thi thử các trường, sở…" chứa hàng chục đề) thì
  **luôn chọn "Giữ + thêm"** — "Thay" ở đây xoá sạch toàn bộ đề cũ trong mục, không chỉ đề vừa
  đăng lại.
- Mỗi lần Đăng tạo một dòng `exams` mới (không có khóa tự nhiên). Up lại cùng đề → chọn "Thay"
  (mục đơn-đề) hoặc đăng thêm bản đã sửa rồi tắt xuất bản bản lỗi (xem mục sửa/gỡ bên dưới).
- **Trước khi đăng, kiểm tra đề đã có sẵn chưa** nếu ngờ trùng nguồn (ví dụ xử lý từ nhiều thư
  mục khác nhau của cùng một bộ đề thi thử) — gõ tên đề vào ô tìm ở `/quan-tri/sua-de`; có kết
  quả thì bỏ qua, đừng đăng trùng (xem bài học "trùng thư mục nguồn" ở skill `dang-de-hang-loat`).
- **Sửa/gỡ một đề đã lỡ đăng sai** (ví dụ phát hiện thiếu ảnh sau khi Đăng): sửa file, đăng lại
  bằng "Giữ + thêm" để tạo bản mới đúng, rồi vào `/quan-tri/sua-de`, tìm bản CŨ theo mã `#N`,
  bấm vào, bỏ tick **"Xuất bản (học sinh thấy được)"**, bấm Lưu — chuyển thành "Bản nháp", ẩn
  khỏi học sinh mà không đụng tới `exam_ids` hay xoá dữ liệu. Không tự chạy SQL `UPDATE`/
  `DELETE` lên `lesson_items`/`exams` qua `supabase db query --linked` (xem `AGENTS.md`).
- Không `git push` / deploy khi working tree có thay đổi không liên quan chưa được xác nhận.
- Chỉ commit/deploy đúng phần vừa làm nếu buộc phải đụng tới code.

## Nhật ký rút kinh nghiệm (bắt buộc cập nhật cuối MỖI phiên dùng skill này — xem `AGENTS.md`)

Cuối phiên, thêm vào đây mỗi bài học một dòng `- YYYY-MM-DD · <sự cố/phát hiện> → <cách làm đúng>`; nếu bài học làm
một bước phía trên sai/thiếu thì sửa luôn bước đó. Phiên không có bài học mới thì ghi "không có bài học mới" trong câu trả lời, không cần thêm dòng.

- 2026-10-06 · Bảng `exams` có `question_count` là generated column → khi update mảng `questions` qua Supabase REST API, KHÔNG được truyền kèm trường `question_count` (gây lỗi 400 `Column is a generated column`), Postgres tự tính lại.
- 2026-10-06 · Câu trắc nghiệm chứa hai đơn vị tương đương cùng đúng về mặt vật lý (ví dụ: `400 K.` và `127°C.`) nhưng hệ thống chỉ gắn 1 đáp án đúng → phải đổi số của phương án nhiễu (ví dụ `27°C.`) để tránh học sinh làm đúng nhưng bị chấm sai.
- 2026-10-06 · Các câu hỏi nhắc tới "hình bên", "đồ thị bên" bị mất hình scan/ảnh từ Word → cần cô lập tạm thời khỏi mảng `questions` trong `exams` và đánh dấu `archived=true` trong `question_bank` kèm file backup để học sinh không gặp đề lỗi trong lúc chờ bổ sung ảnh.
- 2026-10-10 · Trang Đăng đề có HAI chỗ điền Tên đề/Thời gian (khối ngoài của `ExamSection` và `ExamDraftEditor` bên trong). Khi bấm "Sửa chi tiết từng câu" thì khối ngoài là **ô chết** — gõ vào không lưu, phải gõ lại lần hai. → Đã gộp còn MỘT khối ở đầu `ExamSection`, luôn hiện; ai sửa tiếp phần đề thì đừng thêm ô Tên đề/Thời gian ở chỗ khác.
- 2026-10-10 · Thời gian mặc định cũ là 45 phút cho mọi đề (đề 8 câu hay 40 câu cũng vậy) → giờ lấy theo ước lượng số câu/dạng câu (`features/exams/duration.ts`: TN 1,5′ · ĐS 2′ · TLN 2,5′ · tự luận 8′, làm tròn lên bội số 5). Số này chỉ là GỢI Ý, vẫn phải nhìn lại theo lớp trước khi Đăng.


