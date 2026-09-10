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
  vào database, không xuất Word.
---

# Up đề kiểm tra Word → mục Kiểm tra/Luyện tập trên thachlab

## Skill này làm gì

Người dùng thả một file đề trắc nghiệm — **`.pdf` (nhanh nhất, khuyên dùng)** hoặc `.docx`. Skill:

1. Đọc đề đã render, **phiên âm công thức sang `$...$`**. PDF → đọc thẳng; docx → phải render trước.
2. Phân loại từng câu → `multiple_choice` / `true_false` / `short_answer`, lấy **đáp án**
   (dấu `*` hoặc dòng "Đáp án") + **lời giải** (dòng "Lời giải"/"Giải").
3. Dựng gói `thachlab.lesson-bundle/v1` (chỉ khối `exam` + một khối "Công thức trọng tâm"
   ngắn cho mục Lý thuyết — trang admin bắt buộc mục này không rỗng).
4. Đăng qua `https://thachlab.id.vn/quan-tri/nhap-bai`: chọn Lớp→Chương→Bài, dán gói,
   xem preview + bảng validate, tick **Kiểm tra** (mặc định) → **Đăng bài học**.
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
- Ảnh: đồ thị/sơ đồ **vẽ lại được** → `<svg>` nội tuyến trong HTML câu hỏi (quy tắc màu:
  nền tối `#0B1020`, nét `stroke="currentColor"`, nhấn `#60A5FA`). Ảnh chụp/scan thật →
  base64 vào `raster_images[]`, `placeholder` dạng `media/<ten>.jpg`, dùng đúng chuỗi đó làm
  `src`. Trang tự upload lên Storage bucket `lesson-media`. **Không** commit ảnh, **không**
  cần deploy.

## Quy trình

### 1. Đọc đề đã render (text + công thức)

Công thức MathType trong file Word là **OLE** (`word/embeddings/oleObject*.bin`) — pandoc,
python-docx **không đọc được**, chỉ thấy ảnh WMF. Phải nhìn công thức đã render.

**Cách chính — thầy xuất PDF từ Word rồi thả file PDF.** Không cần LibreOffice, không đổi định
dạng gì. Đọc thẳng `de.pdf` bằng Read (theo trang), hoặc tách ảnh cho nét:

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

Đọc hết các trang: đề bài, công thức, phương án, **dấu `*` ở đáp án đúng**, dòng "Lời giải".
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
- **`topic` + `form` cho từng câu** (cho tính năng phân tích chủ đề & cảnh báo phụ đạo):
  - `form`: `"ly_thuyet"` nếu câu hỏi lý thuyết / nhận biết / khái niệm; `"bai_tap"` nếu phải
    tính toán / vận dụng công thức. (Gần đúng: Phần I nhiều câu lý thuyết, Phần III toàn bài tập.)
  - `topic`: **tên chủ đề con** ngắn gọn (vd `"Nội năng"`, `"Thang nhiệt độ"`, `"Sai số phép đo"`).
    Đọc danh mục chuẩn của lớp trước rồi **dùng lại đúng tên** (tránh tạo trùng khác hoa/thường):
    ```bash
    source <(grep -E '^NEXT_PUBLIC_SUPABASE' .env.local | sed 's/^/export /')
    curl -s "$NEXT_PUBLIC_SUPABASE_URL/rest/v1/question_topics?select=name,grade&grade=eq.12" \
      -H "apikey: $NEXT_PUBLIC_SUPABASE_ANON_KEY" -H "Authorization: Bearer $NEXT_PUBLIC_SUPABASE_ANON_KEY"
    ```
    Chủ đề mới (chưa có trong danh mục) vẫn cứ đặt tên hợp lý — admin sẽ gắn nó vào bài học sau
    ở trang **Quản trị → Chủ đề câu hỏi** để nút "Ôn lại" nhảy đúng chỗ.
- `question`, `options`, `explanation`: giữ `$...$`. Đồ thị "như hình bên/hình vẽ" → vẽ
  `<svg>` chèn vào `question`.
- `meta.title`: ưu tiên tiêu đề trong file; nếu chỉ là "Mã đề 0001" thì đặt theo chủ đề, vd
  `"Kiểm tra: Chuyển động biến đổi đều & Rơi tự do"`. `meta.duration_minutes`: theo đề, mặc
  định 45 cho đề kiểm tra 1 tiết, 15 cho đề 15 phút.
- **`theory_html`** (bắt buộc, không rỗng): soạn một khối "Công thức trọng tâm" ngắn cho chủ
  đề của đề (các công thức chính, ~5–12 dòng, class Tailwind trong
  `references/docx-de-format.md` §"HTML"). Đây vừa là nội dung ôn nhanh có ích, vừa để qua
  validator.

### 3. Dựng gói + tự kiểm

```bash
python3 .claude/skills/up-de-kiem-tra/scripts/build_bundle.py draft.json -o bundle.json
```

Script chạy đúng bộ kiểm tra của trang admin (4 phương án, `answer` 0–3, 4 ý đúng–sai, đáp số
≤ 4 ký tự, `$` chẵn, không sót `\textbf{`/`\includegraphics{`, placeholder ảnh đã khai báo).
Có `✕` thì sửa `draft.json` rồi chạy lại — đừng mở trình duyệt khi còn lỗi.

### 4. Đăng qua trang admin

1. Mở `https://thachlab.id.vn/quan-tri/nhap-bai` trong Browser pane (người dùng đã đăng nhập
   admin — nếu chưa, **dừng, nhờ người dùng tự đăng nhập**).
2. Mục 1: chọn **Lớp → Môn → Chương → Bài**. Nếu người dùng chưa nói rõ bài nào: hỏi, hoặc tra
   bằng REST anon-key (chỉ đọc):
   ```bash
   source <(grep -E '^NEXT_PUBLIC_SUPABASE' .env.local | sed 's/^/export /')
   curl -s "$NEXT_PUBLIC_SUPABASE_URL/rest/v1/chapters?select=id,title,subject_code,chapter_classes(class_id)&order=sort_order" \
     -H "apikey: $NEXT_PUBLIC_SUPABASE_ANON_KEY" -H "Authorization: Bearer $NEXT_PUBLIC_SUPABASE_ANON_KEY"
   curl -s "$NEXT_PUBLIC_SUPABASE_URL/rest/v1/lessons?select=id,chapter_id,title&chapter_id=eq.<ID>" \
     -H "apikey: $NEXT_PUBLIC_SUPABASE_ANON_KEY" -H "Authorization: Bearer $NEXT_PUBLIC_SUPABASE_ANON_KEY"
   ```
3. Mục 2: dán `bundle.json` → **Nạp gói**.
4. Mục 3: xem preview — từng câu tô đáp án đúng + lời giải — và **bảng validate**. `errors` đỏ
   chặn Đăng; sửa gói, dán lại.
5. Mục 4:
   - Tick **"Gắn vào Kiểm tra"** (mặc định cho skill này). Thêm **"Luyện tập"** nếu người dùng
     muốn học sinh luyện không tính điểm.
   - **Lý thuyết**: nếu bài đã có nội dung Lý thuyết thật → chọn **Bỏ qua** (khối "Công thức
     trọng tâm" chỉ để qua validator, đừng đè lý thuyết cũ). Bài mới trống → để **Ghi đè**.
   - **Đề cũ ở mục đã chọn**: nếu mục Kiểm tra/Luyện tập đã có đề → chọn **Thay** (trang tự xóa
     đề cũ, tránh tồn đọng) trừ khi người dùng muốn giữ.
6. **Đăng bài học**. Theo dõi log từng bước.
7. Mở `https://thachlab.id.vn/lop-hoc/bai/?id=<lesson_id>`, kiểm mục Kiểm tra hiện đề, số câu
   đúng, bấm thử một câu. Báo link cho người dùng.

### Dự phòng: không mở được trang admin

```bash
node scripts/upload-lesson.mjs bundle.json --lesson <id> --class <id> --target kiem_tra --mode replace
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
- Nếu mục Kiểm tra/Luyện tập của bài đã có đề thật → **hỏi** trước khi chọn "Thay".
- Mỗi lần Đăng tạo một dòng `exams` mới (không có khóa tự nhiên). Up lại cùng đề → chọn "Thay".
- Không `git push` / deploy khi working tree có thay đổi không liên quan chưa được xác nhận.
- Chỉ commit/deploy đúng phần vừa làm nếu buộc phải đụng tới code.
