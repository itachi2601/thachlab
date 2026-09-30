---
name: "mathtype-sang-omml"
description: "Chuyển công thức MathType (MT7/Equation.DSMT4 và Equation.3 OLE) trong file Word sang công thức OMML gốc của Word bằng cách giải mã trực tiếp dữ liệu MTEF — không cần cài MathType, ghi đè thẳng lên file gốc."
---

Chuyển công thức MathType sang OMML (Office Math) trong file Word.

## When to use

Dùng khi người dùng nói: "chuyển công thức MathType sang OMML", "chuyển MT7 sang công thức Word", "công thức bị OLE", "convert equations", "công thức không sửa được trên Word/Azota", "chuẩn hoá công thức trước khi đưa lên thachlab / chuyển LaTeX".

Thường chạy TRƯỚC các skill `azota`, `de-vat-ly-thpt`, `ngan-hang-cau-hoi`, `latex` — vì OMML đọc được bằng script, còn MT7 là OLE nhị phân thì không.

## Quy tắc chung

- **KHÔNG sao lưu.** Người dùng tự quản lý bản sao lưu. Ghi đè trực tiếp lên đúng file được yêu cầu, giữ nguyên tên và vị trí. Không tạo thư mục `_backup*`, không thêm hậu tố `-OMML`, không hỏi xin xác nhận sao lưu.
- Đường mặc định là script có sẵn `scripts/mtef_to_omml.py` (Bước 1–2 dưới đây). Đường này tự động hoàn toàn, không cần cài MathType, không cần computer use, và giữ nguyên byte gốc của mọi thứ ngoài công thức (hình vẽ, bảng, màu, cỡ chữ). **Đừng tự viết lại parser MTEF từ đầu** — script đã giải mã và test khớp trên hàng trăm công thức thật (xem lịch sử trong docstring của script); chỉ sửa script khi nó thật sự báo lỗi trên file cụ thể.
- Chỉ dùng đường MathType thủ công (Phụ lục A) khi script báo lỗi rõ ràng trên một file cụ thể (không phải chỉ vì file lạ) VÀ máy có cài MathType.
- KHÔNG đề nghị macro VBA (không giao được file chạy). KHÔNG thử sửa OLE bằng Office.js.
- LibreOffice **không** chuyển được MathType OLE sang OMML, kể cả khi đã cài `libreoffice-math` và vòng qua .doc — đừng mất thì giờ thử lại. (LibreOffice vẫn dùng được để RENDER công thức đã ra OMML, ở bước xác minh.)

## Bước 1 — Quét hiện trạng

```bash
python3 scripts/mtef_to_omml.py scan *.docx
```

In bảng `MT7 | OMML | tên file` cho từng file. File đã 0 MT7 thì bỏ qua, không đụng vào.

Done when: có bảng số liệu MT7/OMML cho từng file.

## Bước 2 — Giải mã và ghi đè

```bash
python3 scripts/mtef_to_omml.py convert *.docx
```

Với mỗi file: đọc từng `word/embeddings/oleObjectN.bin`, giải mã MTEF, sinh OMML, thay `<w:r>` bọc `<w:object>` bằng `<m:oMath>`, đóng gói lại và **ghi đè thẳng lên file gốc** — script đã tự làm đúng quy tắc "không backup, không đổi tên" ở trên. Script tự in báo cáo `MT7: trước -> sau` và `OMML: trước -> sau` cho từng file; thoát mã khác 0 và in `ERR:`/`CANH BAO:` nếu có file lỗi hoặc còn sót MT7 — đọc kỹ các dòng đó trước khi báo cáo lại người dùng.

Nếu script báo lỗi (`ERR:`) trên một công thức cụ thể mà không lộ nguyên nhân rõ ràng: đọc phần "Phụ lục B" bên dưới để hiểu định dạng, in hex quanh vị trí lỗi, sửa trực tiếp trong `scripts/mtef_to_omml.py`, rồi chạy lại `scan`/`convert`. Nếu sửa được cho một dạng công thức mới, cân nhắc ghi chú lại trong docstring/comment của script để agent sau khỏi vấp lại.

## Bước 3 — Xác minh (bắt buộc)

1. Parse lại mọi `.xml` / `.rels` trong file đầu ra bằng `lxml` — phải không lỗi.
2. Chạy lại `python3 scripts/mtef_to_omml.py scan *.docx` **trên file đã ghi đè** — MT7 phải về 0, OMML tăng đúng bằng số công thức đã chuyển. (`convert` đã tự làm việc này và in ra sau mỗi file, nhưng chạy `scan` lại độc lập một lần nữa cho chắc, nhất là khi có nhiều file.)
3. Lấy ngẫu nhiên ~20 công thức: dựng một .docx tối giản chỉ chứa các `<m:oMath>` đó, render bằng LibreOffice sang PDF rồi PNG; đồng thời render các ảnh WMF gốc (từ `word/media/*.wmf`, ghép qua `.rels` như mô tả ở Phụ lục B); cắt viền trắng, ghép thành hai tấm có đánh số và **so bằng mắt**. Bước này bắt được lỗi ngữ nghĩa mà XML hợp lệ không lộ ra — KHÔNG có script làm sẵn, phải tự viết đoạn ngắn cho việc này mỗi lần (dùng `build_omath`/`convert_equation_bytes` trong `scripts/mtef_to_omml.py` làm thư viện import được).

**Cảnh báo:** LibreOffice KHÔNG phải công cụ kiểm định. Nó có thể báo lỗi hoặc timeout ngẫu nhiên trên file mà Word mở bình thường (lỗi dựng trang của riêng LO, phụ thuộc số công thức trên cùng một trang) — gặp vậy thì **thử lại lần nữa** trước khi kết luận, và chỉ dùng LO để render từng công thức rời hoặc xuất PDF kiểm tra mở được, đừng kết luận file hỏng chỉ vì LO không mở được cả file ở lần thử đầu.

Không nói "đã chuyển toàn bộ" nếu chưa chạy lại mục 2 và 3.

## Bước 4 — Báo cáo

Bảng theo từng file: MT7 trước / OMML sau / còn sót. Nêu rõ file nào không đụng tới và vì sao. Gợi ý skill tiếp theo: `azota` / `de-vat-ly-thpt` / `ngan-hang-cau-hoi` nếu là đề; `latex` / `dang-bai-hoc-thachlab` nếu là bài giảng.

## Phụ lục A — Đường MathType thủ công (chỉ khi script bó tay)

Kiểm tra máy có MathType không (`computer_resolve_access` với tên "MathType", hoặc nhìn ribbon Word có tab MathType). Không có thì đường này vô dụng — quay lại script.

1. `MathType → Preferences → Cut and Copy Preferences…` → **MathML or TeX** → **MathML 2.0 (m namespace)** → OK. Nếu đang là "MathType data (OLE)" thì paste lại vẫn ra MT7.
2. `MathType → Convert Equations…`: tick **MathType or Equation Editor equations**, Convert to **Office Math (OMML)**, Range **Whole document** → Convert.
3. Quét lại bằng `python3 scripts/mtef_to_omml.py scan *.docx`. Công thức hay sót nằm trong text box / shape, header–footer, footnote, ô bảng lồng nhau.
4. Sót ≤ 3: hướng dẫn làm tay — double-click công thức → `Cmd+A`, `Cmd+C` → `Cmd+W` → về Word công thức cũ vẫn đang chọn → `Cmd+V`.
5. Sót > 3: đọc skill `computer-use` trước bước đầu tiên rồi lặp thao tác trên. Sau mỗi lần paste layout đổi → chụp lại màn hình trước khi click tiếp, không dùng toạ độ cũ. Hai công thức liên tiếp paste vẫn ra MT7 → dừng, preference sai, quay lại mục 1. Một công thức hỏng 2 lần → bỏ qua, ghi lại vị trí. Mỗi 10 công thức nhắc `Cmd+S`.

## Phụ lục B — Chi tiết định dạng MTEF (để sửa `scripts/mtef_to_omml.py` khi cần)

Toàn bộ nội dung dưới đây đã được lập trình sẵn trong `scripts/mtef_to_omml.py` (đọc phần comment trong script — mỗi quy tắc dưới đây đều có comment tương ứng tại đúng chỗ code xử lý nó). Phần này chỉ để tra cứu khi cần **sửa** script trước một định dạng công thức mới mà nó chưa xử lý được, không phải để tự viết lại từ đầu.

### Vị trí dữ liệu

Mỗi công thức nằm ở `word/embeddings/oleObjectN.bin` — một OLE compound file. Dùng `olefile`, mở stream `Equation Native`, **bỏ 28 byte đầu** (EQNOLEFILEHDR). Byte đầu tiên của phần còn lại là phiên bản MTEF: `5` = MathType 7, `3` = Equation Editor 3.0.

Ghép công thức với vị trí trong văn bản qua `word/_rels/document.xml.rels` (hoặc `.rels` riêng của header/footer/footnote/endnote nếu có): mỗi `<w:object>` có `<o:OLEObject r:id=...>` (trỏ tới file .bin) và `<v:imagedata r:id=...>` (ảnh WMF hiển thị — dùng làm ảnh đối chiếu ở bước xác minh). Chỉ những `<w:object>` có `ProgID` chứa `"Equation"` mới là công thức MathType — object khác (ảnh, bảng tính nhúng...) phải bỏ qua.

### MTEF 5 (MathType 7)

Header: `ver, platform, product, version, subversion` (5 byte) → chuỗi khoá ứng dụng kết thúc `\0` ("DSMT6"/"DSMT7") → 1 byte tuỳ chọn.

Sau đó là các bản ghi định nghĩa, lặp khi byte đầu thuộc `{0x10, 0x11, 0x13}`:
- `0x13` ENCODING_DEF: cstr
- `0x11` FONT_DEF: 1 byte index + cstr
- `0x10` COLOR_DEF: 3×u16 + cstr (**không có byte index ở đầu** — sai chỗ này là parser lệch ngay)
- Byte khác (đã gặp `0x66`, sinh ra khi công thức được nhập bằng "TeX Input Language" trong MathType): coi là bản ghi mở rộng độc quyền `[tag][1 byte length][length byte payload]`, bỏ qua nội dung, chỉ cần nhảy đúng số byte để không lệch offset.

Rồi `0x12` EQN_PREFS:
- 1 byte options
- 2 mảng "dimension" mã hoá theo **nibble**: 1 byte đếm, rồi đọc từng nibble (nibble cao trước); mỗi dimension = nibble đơn vị + các nibble chữ số, kết thúc bằng nibble `0xF`; đọc đủ số lượng thì **căn lại biên byte**.
- 1 byte đếm styles, rồi `count × 2` byte = bảng style `(font_index, char_style)`. `char_style` bit0/bit1 là **cờ ghi đè thêm** (đậm/nghiêng) chồng lên quy ước mặc định của từng typeface, KHÔNG phải toàn bộ style — typeface 3 (Variable) mặc định đã nghiêng dù char_style=0. Style thứ n ứng với typeface `0x80 + n`; với typeface mở rộng (n ≥ 8, style tự đặt tên trong MathType) thì không có quy ước mặc định, phải dùng thẳng char_style.

Thân công thức bắt đầu ngay sau bảng styles. Mỗi bản ghi = 1 byte tag (giá trị đầy đủ, không phải nibble):

```
0 END        5 MATRIX          10 FULL   15 COLOR
1 LINE       6 EMBELL          11 SUB    16 COLOR_DEF
2 CHAR       7 RULER           12 SUB2   17 FONT_DEF
3 TMPL       8 FONT_STYLE_DEF  13 SYM    18 EQN_PREFS
4 PILE       9 SIZE            14 SUBSYM 19 ENCODING_DEF
```

Các tag 10–14 (FULL/SUB/SUB2/SYM/SUBSYM) và 15–19 (COLOR/COLOR_DEF/FONT_DEF/EQN_PREFS/ENCODING_DEF) có thể xuất hiện **xen giữa danh sách con của LINE/TMPL/PILE**, không chỉ ở phần định nghĩa đầu file. Chúng là các "marker" giữ chỗ vai trò slot hoặc đổi trạng thái định dạng, KHÔNG mang nội dung hiển thị — luôn lọc bỏ chúng trước khi ghép các phần tử còn lại thành danh sách "atom" để dựng OMML (nếu không lọc, việc lấy slot thứ 0/1 theo chỉ số cố định sẽ sai — ví dụ `TMPL` phân số/căn có thể có một `FULL` marker chen giữa slot tử và slot mẫu).

LINE / CHAR / TMPL / PILE / MATRIX / EMBELL có **1 byte options riêng** ngay sau tag. Bit `0x08` = có nudge (2 byte; nếu cả hai byte = 128 thì đọc thêm 2×i16).

- **LINE**: options bit0 = dòng rỗng; ngược lại đọc các bản ghi con tới END.
- **CHAR**: 1 byte typeface, rồi u16 mtcode (bỏ nếu options bit5); bit2 → thêm 1 byte char 8-bit; bit4 → thêm u16; bit0 → danh sách embellishment tới END. mtcode gần như là Unicode, dùng thẳng được. Nếu bit5 bật (không có mtcode), lấy mã từ `extra_u16` rồi mới tới `extra_char`.
- **TMPL**: 1 byte selector, 1 byte variation (nếu bit7 thì ghép thêm 1 byte nữa), 1 byte options, rồi các slot tới END.
- **PILE**: 2 byte (halign, valign) rồi các LINE con → dựng thành `<m:eqArr>`. Có thể là nội dung của một `<m:d>` (hệ phương trình trong ngoặc) hoặc đứng một mình ở cấp cao nhất (lời giải nhiều dòng không có ngoặc bọc) — cả hai trường hợp phải xử lý được, kể cả khi PILE là bản ghi TOP-LEVEL duy nhất của cả công thức.
- **SIZE (9)**: 1 byte; nếu = 100 thì đọc thêm i16, ngược lại 1 byte.
- **EMBELL** đứng riêng ở thân công thức (không gắn vào CHAR nào) có gặp trong thực tế (mã 11) nhưng KHÔNG rõ nghĩa gì — ảnh WMF gốc đối chiếu không hiện dấu phụ nào cả (có thể là artefact preview, hoặc là một loại đánh dấu không hiển thị). Script hiện đang BỎ QUA hoàn toàn embellishment (kể cả gắn trong `CHAR.embell`) — nếu gặp file mà công thức bị thiếu dấu phụ (dấu nháy, mũi tên nhỏ...) so với WMF gốc, đây là chỗ đầu tiên cần tra.

**Selector của TMPL (MTEF 5) — đã xác nhận bằng cách đối chiếu render WMF thật, KHÔNG phải suy đoán:**

| sel | ý nghĩa | slot |
|---|---|---|
| 1 | ngoặc tròn `( )` | slot0 = thân (LINE hoặc PILE); CHAR typeface `0x96` theo sau là glyph ngoặc |
| 2 | ngoặc nhọn `{ }` | như trên — dùng cho hệ phương trình khi slot0 là PILE nhiều dòng |
| 3 | ngoặc vuông `[ ]` | như trên |
| 4 | trị tuyệt đối `\| \|` | như selector 1/2/3 nhưng 2 glyph đuôi là mã vùng riêng (PUA, glyph ghép hình ảnh phóng to của MathType) chứ không phải ký tự `\|` thật — **luôn ép về `\|`**, đừng dùng thẳng mtcode của glyph |
| 10 | căn | slot0 = biểu thức dưới căn, slot1 = chỉ số căn (rỗng/không có → căn bậc hai) |
| 11 | phân số | slot0 = tử, slot1 = mẫu (có thể có `FULL` marker chen giữa — xem trên) |
| 13 | **accent** (gạch ngang/overline) | slot duy nhất = nội dung; KHÔNG có glyph đuôi. Sinh `<m:bar>` phủ toàn bộ nội dung slot (kể cả nếu bên trong còn có số mũ) |
| 14 | mũi tên có chú thích phía trên (hiếm, kiểu phản ứng/quá trình) | 1 CHAR (typeface `0x96`, chính là mũi tên, ví dụ mtcode `8594` = `→`) + tối đa 1 LINE không rỗng làm chú thích. Sinh `<m:limUpp>` (chú thích ở trên). Mới gặp đúng 1 lần trong thực tế — nếu gặp biến thể có chú thích DƯỚI mũi tên, phải tự thêm xử lý (script hiện chỉ lấy chú thích đầu tiên tìm thấy) |
| 27 | chỉ số dưới (postfix) | 1 slot LINE không rỗng = nội dung sub; **base = phần tử liền TRƯỚC** template này trong danh sách atom của LINE cha |
| 28 | chỉ số trên (postfix) | tương tự 27 nhưng có thể có thêm 1 LINE rỗng đệm trước LINE nội dung thật — luôn lấy LINE không rỗng CUỐI CÙNG làm sup |
| 29 | **tiền-tố** sub+sup (ký hiệu hạt nhân/đồng vị, ví dụ ₉₂²³⁵U) | 2 slot LINE không rỗng theo thứ tự (sub rồi sup); **base = phần tử liền SAU** template này, KHÁC HẲN 27/28 (không phải liền trước!) — nhầm chỗ này sẽ ra ký hiệu hạt nhân sai vị trí |
| 31 | **accent** có glyph tường minh (dấu vector, ví dụ `\vec{F}`) | slot0 = LINE nội dung, slot tiếp theo = 1 CHAR typeface `0x96` chính là glyph accent (mtcode `8407` = U+20D7 combining right arrow above). Dùng chung hàm sinh accent với selector 13: có glyph tường minh → `<m:acc m:chr=...>`, không có → `<m:bar>` |

`variation` của nhóm ngoặc/trị tuyệt đối (1/2/3/4): bit0 = hiện glyph trái, bit1 = hiện glyph phải (hệ phương trình `{` một vế là `var=1`, chỉ bit0). Với 27/28/29 thì variation không đổi ngữ nghĩa quan sát được — cứ xét slot LINE nào không rỗng.

**Typeface** = `0x80 + style index`: 1 text, 2 function, 3 variable (**nghiêng**), 4 LC Greek (**đứng, KHÔNG nghiêng** — đã kiểm bằng ký tự μ trong ảnh WMF thật, khác quy ước LaTeX quen thuộc), 5 UC Greek (đứng, đã kiểm bằng Δ), 6 symbol (đứng), 7 vector (**đậm**, không nghiêng), 8 number (đứng). Style index ≥ 8 là style mở rộng do người dùng tự đặt tên trong MathType — không có quy ước mặc định, phải tra bảng styles của chính công thức đó (xem EQN_PREFS ở trên); nếu không có entry, mặc định nghiêng (an toàn hơn cho biến số). Hai giá trị đặc biệt: `0x96` = glyph ngoặc/accent của template (**không sinh nội dung chữ**, chỉ dùng làm begChr/endChr hoặc glyph accent), `0x98` = font MT Extra — trong đó `0xEF02` là **dấu cách**, các mã `0xEF00–0xEFFF` khác thì bỏ.

### MTEF 3 (Equation Editor 3.0)

Không có ENCODING_DEF / FONT_DEF / EQN_PREFS. **Thân bắt đầu ngay ở offset 5.** Tag byte: nibble thấp = loại, nibble cao = options (không có byte options riêng).
- CHAR = `[typeface][u16 char]`.
- LINE: options bit0 = dòng rỗng.
- TMPL = `[selector][variation][options]`.
- Selector khác MTEF 5: `14` = phân số, `15` = script (sub/sup), `1` = ngoặc tròn, `13` = căn. Map về đánh số MTEF 5 rồi dùng chung bộ sinh OMML.

Lưu ý: nhánh MTEF 3 trong script **chưa từng gặp trong thực tế** (370/370 công thức của batch đầu tiên đều là MTEF 5) — nếu file có `Equation.3` (không phải `Equation.DSMT4`), kiểm tra kỹ hơn bình thường ở bước xác minh, và báo lại nếu selector map ở trên sai.

### Sinh OMML và ghép vào file

- Thay **toàn bộ `<w:r>…</w:r>` bao quanh `<w:object>`** bằng `<m:oMath>` (OMML không hợp lệ nếu nằm trong `<w:r>`).
- Khai báo `xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"` ngay trên từng `<m:oMath>` được chèn (đơn giản và chắc chắn hơn là cố thêm một lần vào thẻ gốc của part — XML dư namespace ở nhiều chỗ vẫn hợp lệ và Word đọc bình thường).
- KHÔNG chép `<w:rPr>` của run gốc sang `<m:rPr>` — dùng `<m:sty m:val="p|i|b|bi"/>` theo bảng typeface ở trên để quyết định nghiêng/đậm, không dựa vào `w:i`/`w:b` cũ (để sót `w:i` trong run cũ sẽ xung đột / không áp dụng vì đã bị thay nguyên khối).
- Template sub/sup (27/28) lấy **phần tử liền trước** làm base; nếu phần tử đó là run nhiều ký tự thì tách ký tự cuối ra làm base. Template 29 (tiền-tố) lấy **phần tử liền sau** làm base — xem bảng selector ở trên.
- Ánh xạ: `11 → <m:f>`, `10 → <m:rad>` (`<m:degHide m:val="1"/>` khi không có chỉ số), `1/2/3/4 → <m:d>` với `begChr`/`endChr` + `<m:grow m:val="1"/>`, `27 → <m:sSub>`, `28 → <m:sSup>`, `29 → <m:sPre>` (không phải `<m:sSubSup>` — đó là hậu tố, khác với hạt nhân/đồng vị là tiền tố), `13/31 → <m:bar>` hoặc `<m:acc>`, `14 → <m:limUpp>`, PILE → `<m:eqArr>` (dùng trực tiếp trong `<m:oMath>` khi PILE là top-level, hoặc lồng trong `<m:e>` của `<m:d>` khi là hệ phương trình).
- Xử lý cả các part ngoài `document.xml`: `header*.xml`, `footer*.xml`, `footnotes.xml`, `endnotes.xml` — mỗi part có file `.rels` riêng (batch đầu tiên, 25/9/2026, không có file nào dùng các part này nên nhánh này CHƯA được test bằng dữ liệu thật, chỉ test logic).
- Đóng gói lại bằng cách chép nguyên mọi entry của zip gốc, chỉ thay các part đã sửa. Giữ lại `word/embeddings/` và `word/media/` cũ (quan hệ mồ côi vô hại, và còn dùng làm ảnh đối chiếu).
- Bỏ qua hoàn toàn thông tin màu (`COLOR`/`COLOR_DEF`) — chữ có màu trong MathType gốc sẽ ra màu đen. Đây là giới hạn đã biết, không phải lỗi; nếu người dùng cần giữ màu, phải tự thêm `<m:rPr><w:color .../></m:rPr>` (script chưa làm).

## Lỗi hay gặp

- **Parser lệch vài byte rồi báo tag lạ:** gần như luôn do COLOR_DEF (`0x10`) hoặc mảng nibble trong EQN_PREFS bị đọc sai độ dài, hoặc một bản ghi mở rộng độc quyền lạ (như tag `0x66` ở trên) chưa được liệt vào danh sách bỏ qua. In hex quanh vị trí lỗi rồi dò lại.
- **Công thức rỗng (`<m:oMath></m:oMath>`) dù script báo `converted` thành công:** top-level record là `PILE` chứ không phải `LINE` (lời giải nhiều dòng) — kiểm tra hàm dựng OMML cấp cao nhất có xử lý cả nhánh PILE/CHAR/TMPL, không chỉ LINE.
- **Phân số/căn thiếu mẫu số hoặc chỉ số:** đang lấy slot theo chỉ số cố định (`slots[0]`, `slots[1]`) mà không lọc marker (`FULL`,...) ra khỏi danh sách slot trước — xem mục "marker" ở trên.
- **Ký hiệu hạt nhân/đồng vị bị đảo lộn hoặc base rỗng:** selector 29 lấy base ở phần tử liền SAU, không phải liền trước như 27/28.
- **Công thức đúng nhưng chữ nghiêng hết/hoặc thiếu nghiêng:** tra nhầm bảng `BASE_STYLE`, hoặc quên cộng dồn cờ override từ bảng style riêng của công thức (đặc biệt với style mở rộng ≥ 8).
- **Thiếu dấu cách giữa các cụm:** chưa map `0xEF02` (MT Extra) thành dấu cách.
- **Ngoặc/trị tuyệt đối bị lặp:** đã sinh cả `<m:d>` lẫn các CHAR typeface `0x96` như nội dung — glyph này chỉ dùng cho begChr/endChr hoặc accent, không bao giờ tự sinh chữ.
- **`Equation.3` không chuyển hoặc chuyển sai:** đó là MTEF 3, nhánh code riêng, chưa được test bằng dữ liệu thật (xem ghi chú ở trên) — kiểm tra kỹ.
- **Convert Equations bị mờ (Phụ lục A):** file đang ở Protected View hoặc là .doc cũ → Save As .docx rồi mở lại.