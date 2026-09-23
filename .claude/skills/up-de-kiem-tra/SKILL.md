---
name: up-de-kiem-tra
description: >-
  Nhận MỘT file đề trắc nghiệm — PDF hoặc Word (.docx) kiểu Azota: "Câu 1.", phương
  án A–D, đáp án đánh dấu bằng "*", có/không kèm PHẦN I/II/III, công thức MathType — rồi
  đăng thẳng đề đó vào một bài học trên LMS thachlab: gắn vào mục "Kiểm tra"
  (và/hoặc "Luyện tập") của đúng Lớp → Chương → Bài, chấm điểm tự động. Dùng skill
  này khi người dùng đính kèm một file đề thi/đề kiểm tra (.pdf hoặc .docx) và nói
  "up đề này", "đăng đề kiểm tra", "đưa đề này lên thachlab", "up đề lên lớp X bài Y",
  hoặc chỉ thả file đề kèm ý muốn đưa lên web. KHÁC với dang-bai-hoc-thachlab (đăng
  trọn bài học từ .tex: lý thuyết + dạng bài + đề) — skill này chỉ lo phần ĐỀ.
  KHÁC với de-vat-ly-thpt (soạn/chuẩn hoá đề ra file Word Azota) — skill này ghi
  vào database, không xuất Word. Trợ lý đăng bằng SCRIPT QUA TERMINAL
  (scripts/text-to-bundle.mts + scripts/upload-lesson.mts), KHÔNG mở trang admin trong
  trình duyệt. Đường chính: văn bản kiểu Azota kèm hai dòng "Chủ đề:" (yêu cầu cần đạt)
  và "Dạng:" (lý thuyết/bài tập) cho từng câu. Gói JSON qua build_bundle.py chỉ còn là
  đường dự phòng khi cần vẽ hình SVG hoặc ảnh scan.
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

## Đường chính — văn bản kiểu Azota, dựng gói + đăng bằng script qua terminal

Không mở trình duyệt / trang admin để đăng — trợ lý soạn một file `de.txt` **văn bản**
(không phải JSON): đúng cách trình bày Azota mà thầy cô vẫn gõ, cộng hai dòng nhãn cuối
mỗi câu, rồi hai script terminal (`text-to-bundle.mts` → `upload-lesson.mts`) lo hết phần
dựng gói + ghi database, dùng đúng bộ đọc/kiểm của trang `/quan-tri/dang-de`
(`docxTextToBundle`, `validateBundle`) nên không lệch quy tắc. Đây là đường đi cho
PDF/MathType/đề cần viết lời giải:

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
4. **Dựng gói + đăng bằng script**, không mở trình duyệt:
   ```bash
   npx tsx scripts/text-to-bundle.mts de.txt --title "Kiểm tra: ..." --duration 45 -o bundle.json
   npx tsx scripts/upload-lesson.mts bundle.json --lesson <id> --class <id> --target kiem_tra --mode replace
   ```
   `text-to-bundle.mts` dùng đúng `docxTextToBundle`/`validateBundle` của trang Đăng đề: in
   ghi chú câu thiếu đáp án/phương án, **chặn** nếu còn câu thiếu `Chủ đề:`/`Dạng:` hoặc lỗi
   khác, dòng cuối in `n câu · k chủ đề` khi qua. `upload-lesson.mts` hỏi
   `SUPABASE_SERVICE_ROLE_KEY` (nhập ẩn) — xem "An toàn" ở cuối. Cách tra `<id>` Lớp/Bài ở mục
   "4. Đăng — chạy script" trong phần Quy trình bên dưới.
5. Đọc log của `upload-lesson.mts` (exam id, mục đã gắn), mở link `/lop-hoc/bai/?id=<id>` in ở
   dòng cuối, kiểm mục Kiểm tra hiện đề, số câu đúng, bấm thử một câu. Báo link cho người dùng.

Ảnh: đường văn bản này không mang ảnh (giống văn bản dán trên trang). Đề có hình cần vẽ
SVG hoặc ảnh scan → đi đường dự phòng bên dưới.

## Đường dự phòng — gói JSON build_bundle.py (khi cần hình SVG / ảnh scan)

Người dùng thả một file đề trắc nghiệm — **`.pdf` (nhanh nhất, khuyên dùng)** hoặc `.docx`. Skill:

1. Đọc đề đã render, **phiên âm công thức sang `$...$`**. PDF → đọc thẳng; docx → phải render trước.
2. Phân loại từng câu → `multiple_choice` / `true_false` / `short_answer`, lấy **đáp án**
   (dấu `*` hoặc dòng "Đáp án") + **lời giải** (dòng "Lời giải"/"Giải").
3. Dựng gói `thachlab.lesson-bundle/v1` (khối `exam`; `theory_html` để rỗng nếu chỉ đăng đề —
   khi đó mục Lý thuyết của bài được giữ nguyên) — xem mục "3. Dựng gói + tự kiểm" trong
   Quy trình bên dưới (`build_bundle.py`).
4. Đăng bằng `npx tsx scripts/upload-lesson.mts bundle.json --lesson <id> --class <id> --target
   kiem_tra --mode replace` — không mở trình duyệt. (Nhãn `topic`/`form` trong gói tương đương
   hai dòng `Chủ đề:`/`Dạng:` của đường chính.)
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
  (`.docx` → `word/media/*`; PDF → `pdfimages`), không tốn token vẽ/soát lại. Base64 vào
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
token. Spawn một agent `general-purpose` (`run_in_background: false` — bước sau cần kết
quả ngay), giao đúng việc chép đề:

> Đọc `out/page-*.png` (đề Vật lí THPT đã render). Chép lại **nguyên văn, đủ tất cả các
> trang**: số câu, đề bài, phương án A–D kèm **dấu `*` đánh dấu đáp án đúng**, phần
> "Lời giải" nếu có, mô tả hình vẽ/đồ thị. Công thức gõ sang `$...$` (LaTeX). Không tóm
> tắt, không bỏ câu nào. Trả về text thuần theo thứ tự câu.

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

Script chạy đúng bộ kiểm tra `validateBundle` mà `upload-lesson.mts`/trang admin dùng (4 phương
án, `answer` 0–3, 4 ý đúng–sai, đáp số ≤ 4 ký tự, `$` chẵn, không sót `\textbf{`/
`\includegraphics{`, placeholder ảnh đã khai báo), **cộng thêm soát nhãn**: thiếu `topic`/`form`,
hoặc `topic` không có trong danh mục khối → lỗi, kèm gợi ý tên gần nhất. Tên viết hoa/khoảng
trắng lệch thì script tự chuẩn hoá theo danh mục. Có `✕` thì sửa `draft.json` rồi chạy lại —
đừng chạy `upload-lesson.mts` khi còn lỗi.

Dòng cuối in `Nhãn: n/n câu · k chủ đề` (kèm `· m câu còn ở mức cả bài` nếu có) — n/n mới
được đi tiếp; có `m` thì xem lại, chọn đúng yêu cầu cần đạt script gợi ý. `--grade` cần mạng (REST
anon-key, tự đọc `.env.local`); offline thì `--topics topics.json` với danh mục tải sẵn.

### 4. Đăng — chạy script, không mở trình duyệt

Không mở Browser pane, không có trang admin nào trong bước này — `upload-lesson.mts` ghi
thẳng vào Supabase bằng service-role key, đúng cùng hai hàm (`validateBundle`/`bundleToRows`
trong `services/lesson-import.ts`) mà trang `/quan-tri/nhap-bai` dùng, nên không lệch quy tắc.

1. Tra `<id>` Lớp → Chương → Bài (nếu người dùng chưa nói rõ bài nào — hỏi, hoặc REST
   anon-key, chỉ đọc):
   ```bash
   source <(grep -E '^NEXT_PUBLIC_SUPABASE' .env.local | sed 's/^/export /')
   curl -s "$NEXT_PUBLIC_SUPABASE_URL/rest/v1/chapters?select=id,title,subject_code,chapter_classes(class_id)&order=sort_order" \
     -H "apikey: $NEXT_PUBLIC_SUPABASE_ANON_KEY" -H "Authorization: Bearer $NEXT_PUBLIC_SUPABASE_ANON_KEY"
   curl -s "$NEXT_PUBLIC_SUPABASE_URL/rest/v1/lessons?select=id,chapter_id,title&chapter_id=eq.<ID>" \
     -H "apikey: $NEXT_PUBLIC_SUPABASE_ANON_KEY" -H "Authorization: Bearer $NEXT_PUBLIC_SUPABASE_ANON_KEY"
   ```
2. Chạy:
   ```bash
   npx tsx scripts/upload-lesson.mts bundle.json --lesson <id> --class <id> --target kiem_tra --mode replace
   ```
   `--target luyen_tap|kiem_tra|both` (thêm cả hai nếu người dùng muốn học sinh luyện không
   tính điểm ngoài mục Kiểm tra). `--mode replace` xoá đề cũ ở mục đó trước khi gắn đề mới
   (mặc định cho skill này — dùng `--mode skip` nếu người dùng muốn giữ đề cũ, hỏi trước nếu
   đề cũ là đề thật). Script hỏi `SUPABASE_SERVICE_ROLE_KEY` (nhập ẩn) — **chỉ dùng khi người
   dùng tự cung cấp key ngay lúc đó**, không lấy từ memory phiên trước. Ảnh raster (nếu có,
   đường build_bundle.py) phải nén sẵn — script không có canvas để nén.
3. Đọc log từng bước in ra (tải ảnh, tạo đề, gán lớp, gắn mục Kiểm tra/Luyện tập). Có lỗi
   Postgres (cột thiếu, ràng buộc) thì sửa `bundle.json` hoặc tham số rồi chạy lại — script
   không tự lùi bước đã chạy (đề đã tạo phải xoá tay qua REST nếu bỏ giữa đường).
4. Dòng cuối in `Xong. Kiểm tra: /lop-hoc/bai/?id=<lesson_id>` — mở link đó, kiểm mục Kiểm tra
   hiện đề, số câu đúng, bấm thử một câu. Báo link cho người dùng.

Chủ đề thật sự mới (không có trong danh mục khối) không tự tạo được từ hai script này —
`soat_nhan.py`/`build_bundle.py` đã chặn ở bước dựng gói; nói với người dùng để tạo ở trang
**Chủ đề câu hỏi** trước, rồi chạy lại từ bước soát nhãn.

### Deploy — hầu như không cần

Nội dung + ảnh Storage **không cần deploy**. Chỉ chạy `./scripts/deploy.sh` khi có sửa **code**
(trang, component). Kiểm `git status --short` trước; working tree có thay đổi không liên quan
→ hỏi người dùng (xem memory `feedback_thachlab_deploy_scope`).

## An toàn — không thương lượng

- **Không bao giờ tự nhập mật khẩu** (mật khẩu DB, service-role key) dù người dùng dán trong
  chat với ý "dùng luôn cho lần sau" — chỉ dùng key khi người dùng tự cung cấp ngay lúc đó,
  không lấy từ memory phiên trước; không có key → dừng, nhờ người dùng dán.
- **Luôn đọc log + dòng `✕`/lỗi của `text-to-bundle.mts` và `upload-lesson.mts`** trước khi
  báo đã xong. Không bỏ qua cảnh báo/lỗi validate.
- Nếu mục Kiểm tra/Luyện tập của bài đã có đề thật → **hỏi** trước khi chạy `--mode replace`.
- Mỗi lần đăng tạo một dòng `exams` mới (không có khóa tự nhiên). Up lại cùng đề → giữ
  `--mode replace` (script tự xoá đề cũ ở mục đó).
- Không `git push` / deploy khi working tree có thay đổi không liên quan chưa được xác nhận.
- Chỉ commit/deploy đúng phần vừa làm nếu buộc phải đụng tới code.
