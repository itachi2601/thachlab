---
name: dang-de-hang-loat
description: >-
  Đăng MỘT THƯ MỤC nhiều file đề .docx (hàng chục–hàng trăm) lên thachlab: lọc bằng
  script rẻ trước (loại đề thiếu đáp án, bỏ đề đã đăng, phân loại ảnh/OLE MathType/kiểu
  đáp án/nhãn Chủ đề-Dạng), file sạch đăng thẳng, chỉ file bẩn mới giao agent theo
  up-de-kiem-tra. Dùng khi nói "đăng cả thư mục", "up hết mấy trăm đề này", "kiểm tra
  đề nào thiếu đáp án trong thư mục X", "chạy batch đăng đề", hoặc muốn nhiều agent
  song song. KHÁC up-de-kiem-tra (một file đơn lẻ) — skill này là lớp điều phối bên trên.
---

# Đăng đề hàng loạt từ một thư mục

## QUY TẮC BẮT BUỘC (thầy chốt 28/9/2026) — đọc trước mọi bước bên dưới

Mặc định là **đường script**: máy lọc trước, agent chỉ vào file bị lọc bắt. KHÔNG giao cả
thư mục (hay cả lô) cho agent "tự xem rồi đăng" — đợt 26/9 làm vậy tốn 1,2 triệu token cho 5
file, không lặp lại.

Bốn lưới lọc, chạy theo thứ tự, lưới nào bắt được thì mới tốn suy luận ở lưới đó:

| Lưới | Chạy bằng | Bắt được | Tốn token AI |
|---|---|---|---|
| 1. Phân loại thư mục | `scripts/classify-exam-folder.mts` (Bước 1–2) | không có đáp án, đã đăng, cờ ảnh/OLE/shape/nhãn/kiểu đáp án | 0 |
| 2. `convert.log` | vòng lặp shell mtef + `convert_docx.py` cho CẢ ĐỢT ở phiên chính | thiếu đáp án / thiếu lời giải / dòng `[lưu ý]` từng câu | 0 |
| 3. Trang Đăng đề | khung đỏ "Thiếu hình ở N câu", cảnh báo câu trùng ngân hàng | câu nhắc hình mà không có ảnh, câu trùng | 0 |
| 4. Sau khi lên web | HS bấm "Báo lỗi câu này" → `/quan-tri/bao-loi` → nhảy đúng câu ở `/quan-tri/sua-de` | đáp án sai nội dung, lời giải lệch, thiếu dữ kiện | 0 |

Quy tắc xử lý theo kết quả lọc:

1. **File sạch** = bucket `needs_review` với `answerFormat` là `star` hoặc `dap_an_line`,
   `convert.log` không có dòng thiếu/lệch/`[lưu ý]` → **đăng thẳng ở phiên chính, không
   giao agent**. Mức soát tối thiểu: giải nhanh 2 câu Phần III bất kỳ + liếc bảng đáp án
   xem có ô trống. Không giải lại cả đề, không đối chiếu từng ô 3 bảng đáp án.
2. **File bẩn** = `convert.log` báo thiếu/lệch, `answerFormat` là `answer_table`/`unclear`,
   `hasVectorOrShape` cần vẽ lại, hoặc lưới 3 chặn mà xem không rõ → mới giao agent. Gộp
   2 file cùng loại/agent, prompt kèm sẵn kết quả phân loại + `convert.log` (Bước 5), báo
   cáo cuối chỉ nêu phần khác biệt (câu sửa, câu cần thầy quyết, chủ đề đề xuất).
3. **Ba loại lỗi máy không bắt được** (đáp án đúng định dạng nhưng sai nội dung; MTEF giải
   mã hỏng ra ký tự hợp lệ như số mũ đứng cạnh số thường không dấu phép tính; câu dùng
   chung đề dẫn bị tách rời) → chấp nhận để lưới 4 hứng, KHÔNG bắt agent giải lại cả lô để
   phòng. Chỉ nâng độ sâu soát cho đúng file thấy dấu hiệu lạ khi soát nhanh ở điểm 1.
4. Đề nào nghi ngờ mà chưa kịp xem → đăng ở trạng thái **Bản nháp** (ô "Xuất bản" ở
   `/quan-tri/sua-de`), không chặn cả lô vì một file.
5. Kỳ vọng tỉ lệ: ~60–70% file sạch đi thẳng điểm 1; chỉ 30–40% còn lại tới agent. Nếu
   một đợt thấy tỉ lệ file bẩn cao bất thường, dừng lại xem script lọc/convert có bug
   (xem lịch sử vá ở skill `azota`) trước khi đổ thêm agent.

## Vì sao cần bước lọc trước (đừng giao thẳng cả thư mục cho agent)

Đợt thử 26/9/2026 (xem memory `feedback_batch_agent_upload_efficiency` +
`project_thachlab_de_thi_thu_truong_so`): giao thẳng 5 file cho 4 agent tự dùng skill
`up-de-kiem-tra` tốn **1,23 triệu token** (~246k/file). Bốn nguyên nhân:

1. Agent tự dò pipeline nào cần dùng (dán văn bản / gói JSON vì có ảnh / cần skill
   `azota` vì OLE MathType) — không được báo trước.
2. Mỗi agent tự nghĩ lại cách chống race condition khi nhiều agent cùng ghi vào một
   `lesson_items.exam_ids`.
3. Không lọc trước file "thiếu đáp án hoàn toàn" (không đăng được, phí công) hay file
   "đã đăng rồi" (khỏi làm lại) khỏi phần việc thật.
4. File dễ (chuẩn, có nhãn, đáp án rõ) và file khó (ảnh thật cần trích, lời giải lệch
   câu, thiếu dữ kiện gốc) bị đối xử tốn kém như nhau.

Skill này giải quyết cả 4 điểm trên bằng MỘT bước lọc rẻ chạy trước, rồi mới điều phối.

## Bước 1 — Lọc + phân loại bằng script (bắt buộc, không gọi AI, chạy trong vài phút)

```bash
npx tsx scripts/classify-exam-folder.mts "<đường dẫn thư mục>" \
  --log=scripts/data/bulk-de-thi-thu-log.json \
  --out=scripts/data/classify-report.json
```

(`--log` trỏ file log tên-file ↔ exam_id của lần đăng trước, nếu có — không có thì bỏ
cờ này, script coi như chưa file nào đăng.)

Script đọc thô từng `.docx` bằng `services/docx-reader.ts` (KHÔNG chạy qua
`services/docx-exam-parser.ts` — parser đó chỉ hiểu 1-2 kiểu trình bày đáp án, nhiều đề
cũ dùng kiểu khác vẫn đủ đáp án nhưng sẽ bị báo nhầm là thiếu, xem bài học ở
`project_thachlab_de_thi_thu_truong_so`) rồi chia mỗi file vào một `bucket`:

- **`already_uploaded`** — tên file đã có trong log → bỏ qua hẳn, không giao ai làm lại.
- **`missing_answers`** — 0 dấu hiệu đáp án nào (không `*`, không "Đáp án:", không
  "Chọn đáp án"/"Đáp số", không bảng "Chọn…", không tiêu đề "ĐÁP ÁN") → xử lý ở Bước 2.
- **`needs_review`** — phần việc thật, kèm sẵn các cờ để KHÔNG phải dò lại:
  - `answerFormat`: `"star"` (đã có dấu `*`, đi thẳng đường chính) | `"dap_an_line"` (có
    dòng "Đáp án:" tường minh, đi thẳng đường chính) | `"answer_table"` (bảng "Chọn" +
    lời giải cuối bài — kiểu cũ, PHẢI đọc lời giải để đối chiếu từng câu, không suy
    diễn máy móc) | `"unclear"` (không khớp kiểu nào đã biết — ưu tiên xem tay trước).
  - `hasRealImages` / `imageCount`: có ảnh nhúng thật (`word/media/*`) → **không cần đường
    dự phòng chỉ vì có ảnh** — trang `/quan-tri/dang-de` đọc thẳng file `.docx` (khác với
    dán văn bản) và tự trích ảnh y như `/quan-tri/nhap-bai`. Chỉ cần gói JSON dự phòng khi
    có hình cần **vẽ lại bằng SVG** (hình vẽ Word/shape, không có file ảnh nhúng để trích).
  - `hasMathTypeOle` / `mathTypeCount`: có công thức MathType OLE chưa chuyển → cần
    chạy skill `azota` (`convert_docx.py` → `xuat_thachlab.py`) trước khi đăng. Từ 26/9/2026
    hai script này đã tự đọc đáp án từ dòng "Câu N: Chọn đáp án…"/"a) đúng" trong lời giải
    (không chỉ từ bảng đáp án) và tự chuyển ảnh EMF/WMF — kể cả ảnh nằm trong OLE không phải
    công thức (biểu đồ/hình vẽ nhúng) — sang PNG, xem chi tiết ở skill `azota`. Việc tay còn
    lại chủ yếu là đối chiếu câu nào script tự báo thật sự thiếu (thường do dùng chung đề dẫn
    với câu trước), không phải gõ lại toàn bộ đáp án như trước.
  - `hasVectorOrShape`: có ảnh WMF/EMF hoặc hình vẽ Word. Ảnh WMF/EMF giờ được skill `azota`
    tự chuyển PNG (xem trên) — chỉ hình vẽ Word/shape THẬT SỰ không có file ảnh nhúng mới cần
    vẽ lại bằng SVG (`svglib.py`).
  - `hasTopicFormLabels`: đã có sẵn 2 dòng "Chủ đề:"/"Dạng:" trong file chưa (hầu hết
    file cũ chưa có — vẫn phải gắn nhãn dù các cờ khác đều "sạch").
  - `readerWarnings`: cảnh báo gốc từ `docx-reader.ts` (công thức MathType, ảnh vector,
    đánh số tự động…) — đọc trước khi giao file cho agent.

Báo cáo đầy đủ nằm ở `--out` (JSON, 1 object/file) — đọc bằng `jq`/script nhỏ để lọc
theo bucket, đừng `Read` nguyên file JSON vào phiên chính nếu thư mục lớn (hàng trăm
file) — có thể vài trăm KB, tốn context không cần thiết.

## Bước 2 — Loại đề thiếu đáp án khỏi thư mục

```bash
npx tsx scripts/classify-exam-folder.mts "<đường dẫn thư mục>" --log=... --apply-missing
```

Chuyển (không xoá) toàn bộ file `missing_answers` vào thư mục con `_thieu_dap_an/` bên
trong thư mục gốc. Nếu bucket này rỗng thì không đụng file nào — báo cho người dùng biết
kết quả (có thể là "không có file nào thiếu đáp án", như đợt kiểm tra thư mục "các đề đã
xong" 26/9/2026 — 363/363 file đều có đáp án, chỉ khác định dạng trình bày).

## Bước 3 — Xác định đích đăng

Hỏi người dùng (hoặc dùng đích đã biết từ yêu cầu trước): Lớp → Chương → Bài → mục
("Kiểm tra" / "Luyện tập" / "BTVN"). Tra nhanh bằng REST anon-key nếu cần (xem mục
"Mục 1" trong skill `up-de-kiem-tra`).

Đề thi thử tổng hợp (kiểu "Đề thi thử các trường, sở…") trộn cả kiến thức lớp dưới — danh
mục `question_topics` lưu riêng theo từng khối, nên câu hỏi lớp 10/11 lẫn trong đề lớp 12 sẽ
không khớp yêu cầu-cần-đạt nào của khối 12 dù nội dung đó đã có sẵn ở khối 10/11 (hai "ngăn"
khác nhau). Cách xử lý đã thống nhất với người dùng 26/9/2026: tạo yêu cầu-cần-đạt MỚI ngay
dưới bài đích (ở `/quan-tri/chu-de`, chọn đúng khối đang đăng → bài đích → ô "+ Thêm yêu cầu
cần đạt") thay vì cố ép vào một mục có sẵn không đúng nghĩa — nhãn sẽ hơi thô (không nằm
đúng cây yêu cầu-cần-đạt gốc của bài lớp dưới) nhưng nhanh, an toàn, không đụng danh mục cũ.

**Sửa 27/9/2026 — cách trên CHỈ áp dụng cho tên thật sự mới (chưa có ở đâu trong khối).**
Phổ biến hơn nhiều là trường hợp câu hỏi thuộc ĐÚNG chương trình khối đang đăng (vd lớp 12
"Nội năng và hai cách làm biến đổi nội năng") nhưng khác BÀI so với bài đích ("Đề thi thử…" là
một bài/chương riêng, không có yêu cầu-cần-đạt nào của chính nó) — nhãn vẫn hiện
"(không có trong danh mục)" ở trang Đăng đề y hệt trường hợp cross-khối, dễ tưởng cùng một lỗi.
Đừng thêm tay ở `/quan-tri/chu-de`: tạo một tên ĐÃ TỒN TẠI ở bài khác trong cùng khối sẽ báo
lỗi `409` (ràng buộc unique theo tên trong `question_topics`, không phân biệt theo bài) — tốn
công vô ích. Kiểm tra trước bằng REST xem tên đó có nằm ở lesson_id khác trong cùng khối
không (`question_topics?select=id,name,lesson_id&name=eq.<tên>`); có thì đây là trường hợp
này. Cách xử lý đã dùng cho các đề thi thử up trước đó trong đúng mục này (vd đề #220/225–227):
**để nguyên "không có trong danh mục"**, trang tự lưu nguyên văn (không chặn Đăng) — chấp nhận
câu đó không vào thống kê phân tích theo yêu cầu-cần-đạt mịn (chỉ mất độ chi tiết phân tích,
không mất dữ liệu). Chỉ dùng cách "+ Thêm yêu cầu cần đạt" ở trên khi tên đó KHÔNG tồn tại ở
bất kỳ bài nào khác trong khối (thật sự cross-khối, vd kiến thức lớp 10/11 xen trong đề lớp 12).

## Bước 4 — Thử một batch nhỏ trước khi chạy hết thư mục

**Luôn thử 4–8 file trước** (đủ đa dạng: có file `answer_table`, có file `hasRealImages`,
có file `hasMathTypeOle` nếu có) trước khi chạy toàn bộ `needs_review` — mục đích là lộ
ra lỗi/hình dạng phổ biến của lô file này (thiếu ảnh gốc thật, lời giải lệch câu, thiếu
dữ kiện gốc…) khi số lượng còn nhỏ, dễ sửa hướng dẫn agent trước khi nhân rộng. Đây là
lô "đại diện", không phải lô "dễ nhất" — chọn xen kẽ các `answerFormat`/cờ khác nhau
trong `classify-report.json`, đừng chỉ lấy 5 file đầu bảng chữ cái.

**Trước khi giao bất kỳ file nào cho agent — tự tra trùng bằng phiên trình duyệt đã
đăng nhập, KHÔNG dùng REST anon-key.** Đợt 27/9/2026: query REST anon-key lên bảng
`exams` trả về RỖNG dù đề có tồn tại thật (RLS chặn đọc ẩn danh) — tưởng lầm là "không
trùng" nên vẫn giao file cho agent, tốn nguyên một agent (~115k token) xử lý xong xuôi
(đọc đề, đối chiếu đáp án, gắn nhãn, xuất file) rồi mới phát hiện trùng lúc đăng, vì lúc
đó mới mở `/quan-tri/sua-de` bằng phiên có đăng nhập. Bài học: bước kiểm tra trùng ở
điểm 4 của Bước 5 phải làm **NGAY BÂY GIỜ, trước khi dispatch agent** — mở
`https://thachlab.id.vn/quan-tri/sua-de/`, gõ tên trường/sở của TỪNG file định giao (vài
giây/file, rẻ hơn rất nhiều so với 1 agent chạy oan), bỏ hẳn file nào đã có kết quả khớp
ra khỏi batch trước khi gọi `Agent`. Không lùi bước này xuống "trước khi đăng" (điểm 4
Bước 5) — lúc đó agent đã tốn công xong rồi, chỉ còn cứu được phần đăng trùng, không cứu
được token đã tốn.

## Bước 5 — Chia việc cho agent, LUÔN kèm sẵn kết quả phân loại trong prompt

Với mỗi file thuộc `needs_review`, giao cho một agent chạy skill `up-de-kiem-tra`
(`Skill({ skill: "up-de-kiem-tra" })` bên trong agent, hoặc agent tự đọc file skill đó)
— nhưng KHÔNG để agent tự khám phá những gì script đã biết. Prompt cho từng agent phải
nói rõ ngay từ đầu:

1. Đường dẫn file `.docx`, đích đăng (Lớp/Chương/Bài/mục) — cố định, không đổi giữa
   các agent trong cùng batch.
2. Kết quả phân loại của file đó (`answerFormat`, `hasRealImages`, `hasMathTypeOle`,
   `hasVectorOrShape`) → nói thẳng nên đi đường nào (chính/dự phòng/cần `azota` trước),
   đừng để agent tự thử-sai.
3. **Mỗi agent DỪNG LẠI ở việc tạo ra file đã soát sạch, KHÔNG tự đăng.** Không để agent
   nào mở Browser pane hay chạy script service-role key — pane dùng chung trong cùng phiên
   nên nhiều agent cùng đăng sẽ giẫm tab nhau (xem bài học ở
   `feedback_batch_agent_upload_efficiency`), còn service-role key thì không được lấy từ
   phiên trước hay giao cho agent tự nhập. **Phiên chính (điều phối) tự đăng tuần tự** cho
   cả lô sau khi các agent báo xong, bằng kỹ thuật relay + `DataTransfer` ghi trong skill
   `up-de-kiem-tra` mục "Có sẵn file .docx đã chuẩn — kéo-thả bằng relay" — đăng an toàn,
   không cần service-role key, không cần trình duyệt thật.
4. **Kiểm tra trùng nội dung với đề đã đăng trước khi đăng**, đặc biệt khi xử lý nhiều thư
   mục nguồn khác nhau của cùng một bộ đề: gõ tên đề vào ô tìm ở `/quan-tri/sua-de`. Đợt
   26/9/2026 xử lý thư mục "250+ DE THI THU 2025" phát hiện 2/5 file trùng với đề đã đăng
   từ thư mục "các đề đã xong" khác — cùng nội dung nhưng TÊN FILE khác nhau nên Bước 1 (lọc
   theo tên file trong log) không bắt được. Script lọc theo tên file chỉ đủ khi chắc chắn
   các thư mục nguồn không chồng lấp nội dung. **Trùng cũng có thể xảy ra NGAY TRONG CÙNG một
   thư mục**: đợt kế tiếp cùng ngày phát hiện file "59. KY ANH HA TINH 2025.docx" và
   "180. KY ANH HA TINH 2025.docx" (cùng thư mục "250+ DE THI THU 2025") là ĐÚNG MỘT đề, chỉ
   khác số thứ tự file — kiểm tra sua-de trước khi đăng bắt được ngay cả trường hợp này, vì
   vậy bước kiểm tra này áp dụng cho MỌI file trong batch thử, không chỉ khi nghi ngờ trùng
   thư mục khác.
5. Câu lệnh gắn `exam_id` vào `lesson_items.exam_ids`: nếu mục đó đang gom nhiều đề (kiểu
   "Đề thi thử các trường, sở…") thì trang Đăng đề đã tự làm việc này an toàn khi chọn
   **"Giữ + thêm"** (không cần agent tự viết SQL `array_append`) — trang tự thêm `exam_id`
   mới vào mảng mà không đụng các phần tử cũ, không có race condition vì mỗi lượt Đăng chạy
   tuần tự ở phiên chính (điểm 3). Không tự chạy `UPDATE`/`DELETE` qua
   `supabase db query --linked` lên `lesson_items`/`exams` (xem `AGENTS.md`) — kể cả để gỡ
   một đề lỡ đăng sai: dùng ô "Xuất bản (học sinh thấy được)" ở `/quan-tri/sua-de` để chuyển
   thành Bản nháp thay vì xoá/sửa mảng.
6. Site tự chặn Đăng khi phát hiện câu nhắc tới "hình vẽ/đồ thị" mà không có ảnh kèm theo
   (khung đỏ "Thiếu hình ở N câu", liệt kê đúng số câu) — đây là lưới an toàn cuối, không
   phải lỗi cần vá bằng tay; chỉ tick ô xác nhận bỏ qua sau khi đã tự xem từng câu đó thật
   sự không cần hình.
7. Yêu cầu báo cáo cuối: số câu, MỌI nội dung agent tự sửa/tự phục hồi trong file gốc
   (đáp án sai, đoạn dẫn thiếu, ảnh thiếu…) — không tự quyết âm thầm, phải nêu ra để người
   dùng xác nhận lại (xem mục "An toàn" bên dưới). Agent không có exam_id để báo (đăng do
   phiên chính làm sau) — báo đường dẫn file `de_thachlab.docx` cuối cùng thay vào đó.

Số agent chạy song song: giới hạn hợp lý theo hướng dẫn workflow (mặc định vừa, dưới
10 agent/đợt) — không cần chạy hết cả trăm file cùng lúc, xong một đợt rồi mở đợt sau.

## Giảm token cho các đợt sau (rút kinh nghiệm 26/9/2026)

Vá xong 2 lỗi hệ thống trong `convert_docx.py`/`xuat_thachlab.py` chỉ giảm chi phí **rất
ít** (đợt trước khi vá ~221k token/file, đợt sau khi vá ~195k/file — chưa tới 15%). Lý do:
phần tốn token nhất KHÔNG phải chạy script (gần như miễn phí) mà là suy luận — agent giải
lại toàn bộ Phần III, đối chiếu từng chữ 3 bảng đáp án, và tự đọc-so-ảnh cho MỌI file dù
file đó có gì bất thường hay không. Ba việc giảm số agent song song hoặc số file/đợt không
đụng tới nguồn tốn chính này. Bốn thay đổi sau mới thật sự giảm:

1. **Phiên điều phối tự chạy trước 2 bước máy (mtef + convert_docx) cho CẢ ĐỢT bằng vòng
   lặp shell, KHÔNG giao việc này cho agent** — hai bước này thuần cơ khí, không cần suy
   luận, tốn gần như 0 token khi chạy ở phiên chính:
   ```bash
   for d in scripts/data/batch-XXX/agent*/; do
     python3 "$MTEF" convert "$d/de_goc.docx"
     python3 "$AZOTA/convert_docx.py" "$d/de_goc.docx" "$d/de_azota.docx" 2>"$d/convert.log"
   done
   ```
   Giao cho agent **file `de_azota.docx` đã có sẵn + nội dung `convert.log`** ngay trong
   prompt (dán thẳng vài dòng thống kê, không bắt agent tự chạy lại) — agent bắt đầu thẳng
   vào việc cần suy luận (đối chiếu, gắn nhãn, xuất file), không tốn lượt đọc tool-output
   của 2 script này nữa (mỗi lượt gọi + đọc kết quả cũng cộng dồn, dù bản thân script rẻ).
2. **Chỉ bắt buộc soát toàn bộ (giải lại cả 6 câu Phần III, đối chiếu từng ô 3 bảng đáp
   án) khi `convert.log` báo thật sự thiếu/lệch.** File `convert.log` sạch (không thiếu
   đáp án, không thiếu lời giải, không dòng `[lưu ý]`) → chỉ cần **soát nhanh 2 câu Phần
   III bất kỳ** (không phải cả 6) + đọc lướt qua bảng đáp án xem có ô nào trống — script đã
   được kiểm chứng đủ tin cậy trên nhiều file khác nhau (xem lịch sử vá lỗi ở skill
   `azota`), không cần nghi ngờ mọi file như lúc đầu vá. Tăng lại độ sâu soát khi thấy bất
   kỳ dấu hiệu lạ (điểm số ra lẻ khó tin, công thức có kí tự lạ kiểu số mũ đứng cạnh số
   thường không dấu phép tính — dấu hiệu MTEF giải mã hỏng đã gặp, xem skill `azota`).
3. **Báo cáo cuối chỉ cần liệt kê phần khác biệt** (câu nào sửa, câu nào cần thầy quyết,
   chủ đề đề xuất) — không cần viết lại lời giải/phép tính đầy đủ cho những câu đã khớp
   sẵn, không cần tường thuật lại nội dung câu hỏi. Đây là phần sinh ra nhiều token ĐẦU RA
   nhất ở các báo cáo trước mà không ai đọc lại chi tiết.
4. **Cân nhắc giao 2 file/agent thay vì 1/agent** khi các file trong lô cùng loại (cùng
   `answerFormat`, cùng khoảng `imageCount`) — chi phí "khởi động" (đọc skill, hiểu quy
   trình) là chi phí cố định trả một lần nhưng đang bị nhân theo số agent; gộp 2 file/agent
   khi lô không quá phức tạp giúp chia đều chi phí này. Không gộp quá 2-3 file/agent — mất
   lợi ích song song và agent dễ lẫn file nọ với file kia trong báo cáo.

## Đăng bằng script khi không có phiên đăng nhập trình duyệt (29/9/2026)

`npx tsx scripts/upload-exam-docx.mts <de_thachlab.docx> --title "<Tên đề>" --lesson <id> --item <lesson_item_id>
[--duration 50] [--dry] [--drop-vector-marks] [--log scripts/data/bulk-de-thi-thu-log.json --src "<tên file gốc>"]`
— dùng chung `readDocx → docxTextToBundle → bundleToRows` với trang Đăng đề, tải ảnh lên `lesson-media`,
append `exam_ids` kiểu "Giữ + thêm", tự rollback khi lỗi. Luôn chạy `--dry` trước: nó in số câu dựng
được, câu thiếu đáp án/thiếu hình, dạng câu. KHÔNG gắn nhãn AI được (Edge Function cần phiên người
dùng) — câu để trống Chủ đề, chấp nhận với đề thi thử tổng hợp ở mục 277. `--drop-vector-marks` bỏ mốc
⟦ảnh WMF⟧/⟦hình vẽ Word⟧ khi đã xem chắc đó là ảnh trang trí. Ảnh phải nén trước (script không có canvas).

**Bài học 29/9:** `mtef_to_omml` ghi đè thẳng `de_goc.docx` trong thư mục agent → không còn khớp MD5/kích
cỡ với file nguồn; muốn biết thư mục agent nào ứng với file nguồn nào thì dò một câu chữ đặc trưng trong
các file nguồn (unzip `word/document.xml` + tìm chuỗi), đừng tin MD5. Đợt này 11 thư mục agent để lại
từ các phiên trước hoá ra 8 là đề đã đăng (220, 225–230, 176, 227) — kiểm trước bằng cách này rồi mới đăng.

## Bước 6 — Cập nhật log, lặp lại

Sau khi phiên chính đăng xong cả lô (Bước 5 điểm 3), thêm các file vừa đăng vào file log
JSON (tên file ↔ `examId` — lấy từ dòng log "✓ đề số N" khi Đăng) để đợt lọc sau (Bước 1) tự
động coi chúng là `already_uploaded`, không giao lại. File nào bị bỏ qua vì trùng nội dung
với đề đã đăng trước đó (Bước 5 điểm 4) cũng nên ghi vào log, trỏ tới `examId` đã có sẵn —
không chỉ ghi cho file thật sự vừa đăng mới.

Không phải lúc nào cũng thấy được dòng "✓ đề số N" (vd đọc trạng thái nút bằng `javascript_tool`
khi pane đang ẩn, không đọc được log console/toast) — lấy `examId` chắc ăn hơn bằng cách mở
`/quan-tri/sua-de`, gõ đúng tên đề vừa đăng (nguyên văn ô "Tên đề"), đọc số `#N` ở kết quả.

**27/9/2026 — đừng hoảng nếu `exam_ids` của mục không tăng đúng bằng số đề vừa thêm.** Ghi
"Giữ + thêm" có vẻ tự dọn (không rõ chủ động hay hệ quả phụ) các `examId` cũ không còn trỏ tới
dòng `exams` nào (tham chiếu hỏng từ trước, không phải do đợt đăng này) — quan sát được khi
đăng 3 đề, mảng tăng đúng 3 ID mới nhưng có đúng 1 ID cũ rất lâu (không tồn tại, gõ vào
`/quan-tri/sua-de` ra "Không có đề phù hợp") biến mất khỏi mảng. Trước khi nghi ngờ mất dữ liệu:
so `exam_ids` trước/sau, với mỗi ID lệch (mất hoặc thừa ngoài dự kiến) tra `#ID` ở `/quan-tri/
sua-de` — ID đó *thật sự không tồn tại* thì không có gì phải cứu; ID đó *có tồn tại* mới là sự
cố thật (báo ngay cho người dùng, đừng tự ý ghi đè lại `exam_ids` bằng SQL).

## An toàn — kế thừa từ skill up-de-kiem-tra

- Đây là thao tác lên **hệ thống sống** (DB + web học sinh đang dùng) — áp dụng nguyên
  mục "An toàn — không thương lượng" của skill `up-de-kiem-tra` cho từng file.
- Cũng kế thừa quy tắc "Đăng nội dung — luôn tối ưu tốc độ tải" ở `AGENTS.md`: file nào có
  ảnh nhúng thật (không phải công thức MathType) phải nén trước khi giao agent đăng — nhắc
  rõ trong prompt chia việc ở Bước 5, đừng để agent tự quên.
- Bước lọc (Bước 1–2) chỉ ĐỌC file và (nếu `--apply-missing`) DI CHUYỂN file trong thư
  mục nguồn cục bộ — không đụng Supabase, an toàn chạy lại nhiều lần.
- Không tự ý xoá file — `--apply-missing` chỉ di chuyển vào thư mục con, không xoá.
- Nội dung agent tự sửa/phục hồi trong đề gốc (đáp án sai, đoạn dẫn thiếu…) luôn phải
  báo lại cho người dùng, không âm thầm coi là xong.
