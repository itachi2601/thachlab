# AI Tutor Socratic — quyết định kiến trúc không phụ thuộc model (viết 6/10/2026)

Roadmap đặt AI Tutor ở Giai đoạn 4 (Q2–Q3/2027, `docs/ROADMAP.md`). File này ghi **những thứ chốt được từ bây giờ
mà không mục theo bảng giá**: tên model, giá, ngưỡng cache, tham số thinking đổi theo quý — tất cả đọc từ secret và
đo bằng log, không ghi cứng vào code hay vào file này. Khi tới lúc làm, việc còn lại là chạy eval, tra giá, điền tên model.

## 1. Những điều đã kiểm (6/10/2026) và kết luận còn dùng được

- Với 200 HS × 20 tin nhắn/tháng, chi phí API nằm trong khoảng **$2–$80/tháng** tuỳ tầng model. Con số này chịu được
  sai số gấp đôi, khớp dòng "API AI 1–8 triệu/tháng" trong bảo giá. **Chi phí API không phải nút thắt; chất lượng gợi ý
  mới là.** Không cần quay lại bảng giá cho tới khi có số đo thật.
- Tỉ lệ giá giữa các tầng ổn định nhiều đời (output ≈ 4–6× input; tầng "nano" rẻ hơn tầng "Haiku" ≈ 10×). Tên model thì
  đổi mỗi quý → **không ghi tên model vào code**.
- DeepSeek: giờ cao điểm là 01:00–04:00 và 06:00–10:00 UTC thứ Hai–Sáu (= 8–11h và 13–17h giờ VN). Tối và cuối tuần
  rẻ nửa giá. **Kênh phụ đạo buổi chiều** (nơi roadmap muốn chạy trước) **rơi đúng giờ cao điểm**. deepseek-flash mặc
  định BẬT thinking, token suy luận tính giá output → phải tắt cho tầng gợi ý (tiền lệ: `classify-questions`).
- Anthropic: cache tính theo workspace, không theo học sinh — prefix dùng chung nóng liên tục khi có ≥1 request mỗi
  5 phút. Nhưng ngưỡng tối thiểu cache được **khác nhau theo model** (Haiku 4.5: 4.096 token; dòng 5.5: 512) và dòng 5.5
  **không tắt được thinking** kiểu DeepSeek (Opus 5.5: không tắt được; Sonnet 5.5: chỉ `between_tools`) → cấu hình thinking
  phải nằm trong registry theo từng provider, không phải một cờ chung.
- Batch API (giảm 50%) không dùng được cho tutor (bất đồng bộ tới 24h); chỉ dùng cho backfill nhãn/lời giải.

## 2. Đơn vị đếm: "lượt" là gì

Mọi ước tính trước đây nhân theo "lượt" mà không định nghĩa. Chốt:

- **1 lượt = 1 tin nhắn của HS** (1 request). Một **hội thoại** gồm nhiều lượt, mỗi lượt gửi lại toàn bộ lịch sử.
- Hội thoại 6 lượt tốn input ≈ 15–20 request đơn (lịch sử cộng dồn), không phải 6. Đây là hệ số chi phí lớn nhất, lớn hơn
  thinking. Giới hạn **tối đa 8 lượt/hội thoại**, sau đó đóng bằng lời giải đầy đủ hoặc chuyển sang kênh trợ giảng.
- Log phải ghi `conversation_id` + `turn_index` để tính được chi phí **mỗi hội thoại**, không chỉ mỗi request.

## 3. State machine ở server — không tin model tự giữ

Quy tắc roadmap "chỉ đưa đáp án sau ≥2 gợi ý hoặc 'Em bó tay'" là ràng buộc kỹ thuật, thực thi trong Edge Function:

```
HINT_1 → HINT_2 → (HS bấm "Em bó tay" | lượt ≥ 3) → SOLUTION → CLOSED
```

- Ở trạng thái `HINT_*`, prompt **không chứa đáp án đúng ở dạng model có thể lặp lại**: gửi lời giải để model hiểu hướng,
  nhưng server **lọc đầu ra** (so khớp chuỗi đáp án/kết quả số với phản hồi) trước khi trả về HS. Lộ → bỏ, sinh lại 1 lần,
  vẫn lộ → trả gợi ý mẫu tĩnh.
- Chuyển trạng thái do server quyết theo **hành động của HS** (bấm nút, số lượt), không theo "độ khó câu" — độ khó không
  đoán trước được, hành động thì chắc chắn 100%.
- Routing model cũng theo trạng thái: `HINT_*` dùng model rẻ, thinking tắt/thấp; `SOLUTION` dùng model mạnh hơn, cho phép
  suy luận (cần đúng vật lí).

## 4. Grounding quan trọng hơn chọn model

Prompt luôn kèm dữ liệu của **chính câu đó**: đề + phương án HS chọn + đáp án + lời giải (`exams.questions[i].explanation`
hoặc `question_bank`) + đoạn lý thuyết của bài (`lesson_items.summary_html` của mục `ly_thuyet`). Thiếu grounding thì
model đắt cũng bịa; có grounding thì model rẻ đủ dùng. Cấu trúc prefix để cache:

```
[system cố định] → breakpoint 1 (nóng toàn hệ thống)
[lý thuyết bài + lời giải câu] → breakpoint 2 (nóng theo bài đang được học)
[lịch sử hội thoại + tin nhắn mới]
```

## 5. Dữ liệu cá nhân của trẻ vị thành niên

- Chỉ gửi mã băm (`student_hash`), **không** gửi tên, email, lớp, điểm thô. Chủ đề yếu gửi dưới dạng tên YCCĐ, không kèm
  danh tính.
- Rà nghĩa vụ dữ liệu trẻ em theo quy định hiện hành **trước** khi chọn provider; provider có DPA rõ ràng được ưu tiên dù
  đắt hơn vài trăm nghìn/tháng — đúng tinh thần "chi phí API không phải vấn đề".
- Không lưu nội dung hội thoại quá 90 ngày; chỉ giữ số liệu usage để tính chi phí.

## 6. Registry model + log usage thật

Một Edge Function `ai-tutor`, không SDK (theo mẫu `classify-questions`). Mọi thứ đổi theo thời gian đọc từ secret:

| Secret | Ý nghĩa |
|---|---|
| `TUTOR_HINT_PROVIDER` / `TUTOR_HINT_MODEL` | model tầng gợi ý |
| `TUTOR_SOLUTION_PROVIDER` / `TUTOR_SOLUTION_MODEL` | model tầng lời giải |
| `TUTOR_<PROVIDER>_THINKING` | cấu hình thinking theo provider (`disabled` / `between_tools` / `effort:low`…) |

Bảng `ai_tutor_usage` (viết migration khi làm, chỉ ghi số, không ghi nội dung): `conversation_id`, `turn_index`, `state`,
`provider`, `model`, `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_write_tokens`, `reasoning_tokens`,
`latency_ms`, `called_at`, `is_peak` (DeepSeek), `stop_reason`. Chốt model bằng số liệu bảng này sau 2 tuần chạy thật,
không bằng bảng giá của người khác.

## 7. Eval offline — làm được ngay, không cần xây tutor

`scripts/eval-ai-tutor.mts` lấy N câu HS **làm sai thật** (`exam_question_results` + đáp án đã chọn trong
`exam_results.detail.responses`), cho từng model sinh **gợi ý tầng 1** với grounding như mục 4, rồi xuất phiếu chấm mù
(nhãn A/B/C đã xáo) để thầy chấm 3 tiêu chí: **không lộ đáp án · đúng vật lí · trúng chỗ sai**. Chi phí thật tự ra từ
usage kèm theo. Cách chạy xem đầu file script. Cần key của provider nào thì chạy provider đó; thiếu key thì bỏ qua.

Thử 6/10/2026 (2 câu, chỉ DeepSeek vì `.env.local` mới có `DEEPSEEK_API_KEY`): pipeline chạy, mỗi gợi ý ≈ 616 token vào /
142 token ra / 1,4 s, ≈ $0,34 cho 1.000 gợi ý ở giá peak (lúc chạy là 9h sáng thứ Hai giờ VN = peak). Hai điều rút ra:
- Bộ lọc "nghi lộ" bằng máy bắt hụt: gợi ý diễn giải "Wb chia giây" thay vì viết "Wb/s" → chỉ thầy chấm mới kết luận được.
- `exam_question_results.is_correct` có dòng lệch với đề hiện tại (chấm lại theo `exams.questions` thì đúng) — đề đã sửa đáp
  án sau khi HS làm. Script chấm lại trước khi dùng; thống kê chủ đề yếu (`tutoring_needs`) cũng đang đọc cột này.

## 8. Việc còn lại khi tới Giai đoạn 4

1. Chạy eval mục 7 với các model hiện hành lúc đó, thầy chấm. 2. Tra giá chính thức (api-docs.deepseek.com,
platform.claude.com/docs/en/about-claude/pricing, developers.openai.com/api/docs/pricing). 3. Viết migration
`ai_tutor_usage` + Edge Function theo mục 3–6. 4. Chạy 2 tuần trong kênh phụ đạo, đọc bảng usage, mới chốt model.
5. Prompt hệ thống của tutor phải thể hiện mục 9; thêm tiêu chí chấm thứ 4 vào phiếu eval: **đúng phong cách thầy**.

## 9. Phong cách dạy của thầy Thạch — nguồn cho prompt tutor (ghi từ 6/10/2026, bổ sung dần)

Tutor không mang phong cách thầy nhờ "học từ hội thoại" — model không nhớ gì qua phiên. Phong cách phải nằm ở đây, chép
vào prompt hệ thống và vào tiêu chí eval. Mỗi lần thầy nói thêm một điều cốt lõi về cách học, **nối mục mới** vào mục này
(chỉ thêm, không viết lại). Bản nháp gốc ở memory `user_thach_phong_cach_hoc_va_day` (chỉ có trên Mac).

### 9.1 Trước khi giải: gọi kiến thức theo đúng thứ tự, điều kiện áp dụng là trọng tâm

Khi giải một bài, thầy luôn gọi lại kiến thức liên quan trước, theo thứ tự: **khái niệm → định luật/định lý → công thức →
điều kiện nào thì dùng được định luật đó** → rồi mới giải từng bài. Điều kiện áp dụng là phần quan trọng nhất và là chỗ
HS vấp nhiều nhất (thuộc công thức nhưng dùng sai hoàn cảnh: bảo toàn cơ năng khi có ma sát, bỏ qua lực cản khi đề không
cho phép…).

Áp vào tutor: câu hỏi Socratic đầu tiên hỏi về **điều kiện**, không gợi công thức. Ví dụ: *"Trong bài này có lực nào
không phải lực thế không? Vậy đại lượng nào được bảo toàn?"* — thay vì *"Em thử dùng W = ½mv² xem"*. Gợi ý tầng 1 chỉ
được nhắc tên khái niệm/định luật; tầng 2 mới hỏi về điều kiện; tầng 3 mới chạm công thức.

### 9.2 Nền tảng trước, kỹ năng sau — không học "như cây cột thẳng đứng"

Thầy học trượt băng ở tuổi 35 theo đúng trình tự: luyện edge inside/outside thật thuần thục → các loại turn → waltz jump,
spin. Bài học thầy rút: muốn học gì cũng phải có nền tốt thì mới phát triển được kỹ năng và định hướng riêng; học như một
cây cột thẳng đứng thì sớm ngã.

Áp vào tutor: không đẩy HS sang bài khó khi dạng cơ bản của cùng chủ đề chưa đạt (khớp mastery theo YCCĐ, `docs/mastery-
rules.md`, và phụ đạo theo chủ đề). Khi HS sai bài khó vì hổng nền, tutor lùi về bài nền tương ứng thay vì gợi tiếp bài
đang sai. Hình ảnh "cây cột thẳng đứng sẽ ngã" dùng được khi giải thích cho HS vì sao phải quay lại bài dễ.

### 9.3 Nhớ bằng cách lôi ra, không bằng cách nhìn lại (retrieval practice)

Thầy dẫn Karpicke & Roediger (*Science* 2008, cặp từ Swahili–Anh: học lặp lại nhớ ~36%, tự kiểm tra lặp lại nhớ ~80%;
Karpicke & Blunt, *Science* 2011 với văn bản). Ngồi xem lại lời giải chính là nhóm nhớ 36%. Ba cách học đúng thầy chốt:
1. Chữa bài xong, gấp vở, tự giải lại trên giấy trắng.
2. Công thức: tự viết lại từ trí nhớ, làm ngay một bài mới không mở vở.
3. Bài đã chữa: 3 ngày sau che lời giải, giải lại.

Hai ràng buộc đi kèm: retrieval phải có **đối chiếu đáp án** sau khi thử (không thì củng cố luôn lỗi); và **ví dụ mẫu đi
trước** khi HS chưa hiểu lần đầu (Sweller), retrieval đi sau.

Áp vào tutor và UI: sau khi tutor dẫn HS tới đáp án, bước kết thúc không phải "xem lời giải" mà là *"gấp lại, tự trình bày
từ đầu"*; bài sai được hẹn lại sau 3 ngày rồi 7 ngày; công thức đưa dạng thẻ "viết ra rồi mới bấm xem".

### 9.4 Ví dụ hội thoại mẫu (chờ thầy viết)

Cần 5–10 cặp *HS hỏi → thầy hỏi lại* do chính thầy viết hoặc chụp từ tin nhắn thật; giá trị hơn mọi quy tắc trên vì eval
chấm được theo mẫu thật. Không ghi tên HS (mục 5). Lời thầy giữ nguyên chính tả/xưng hô "thầy – con".

**Tình huống 1 (tin nhắn thật, 6/10/2026).** HS lớp 10 tự đặt một bài toán cho bài thuyết trình về định luật vạn vật hấp dẫn
(cho bán kính Trái Đất 4,258 750 456×10⁻⁵ AU, khối lượng TĐ, khoảng cách TĐ–MT 149 597 870,7 km, khối lượng MT
1 988 550,1021 tấn… hỏi lực hấp dẫn TĐ–MT), gửi kèm công thức $F_{hd} = G\dfrac{m_1 m_2}{r^2}$ và hỏi:
- HS: "Có bị sai chỗ hay thiếu chỗ nào không ạ"
- Thầy: "1- Cái này con cho bán kính trái đất mà ko cho bán kính mặt trời, 2- khoảng cách mà con ghi đang là khoảng cách
  tính từ tâm hay tính từ bề mặt của TĐ đến MT"
- Thầy: "Thêm nữa là chữ số có nghĩa nhiều quá" / "Con cho khoảng 3 đến 4 chữ số có nghĩa thôi"

*Nhận xét (suy diễn của agent):* thầy không sửa hộ đề, không nói "r phải là khoảng cách hai tâm" — thầy chỉ ra chỗ đề
**không nhất quán** (cho bán kính một vật mà không cho vật kia) rồi đặt câu hỏi về **điều kiện áp dụng** (r trong công thức
là gì) để HS tự nhận ra; mục thứ ba là thói quen trình bày (chữ số có nghĩa) nói thẳng. Đánh số 1-2, câu ngắn, không khen.

**Tình huống 2 (tin nhắn thật, 6/10/2026).** Cùng HS, hỏi về bản chất công thức:
- HS: "thầy ơi, cái công thức này sao người ta nhân với G v ạ"
- Thầy: "đó là hằng số hấp dẫn con ạ" / "trong các định luật vật lý, người ta tìm ra mối quan hệ tỉ lệ thuận và nghịch
  giữa các đại lượng" / "rồi tìm ra hằng số liên hệ giữa các đại lượng đó và phát biểu thành định luật"

*Nhận xét (suy diễn của agent):* câu hỏi về **khái niệm** thì thầy trả lời thẳng, không hỏi ngược — nhưng không dừng ở
"G là hằng số" mà nâng lên cách mọi định luật vật lí được hình thành (quan hệ tỉ lệ → hằng số → phát biểu), để HS mang
được sang định luật khác (Coulomb, Hooke…). Ba câu ngắn, mỗi câu một ý.

### 9.5 Khi nào hỏi ngược, khi nào trả lời thẳng (rút từ 9.4, 6/10/2026)

Từ hai tình huống thật: thầy **không Socratic mọi lúc**.
- HS đưa **bài làm/đề tự soạn/lời giải của mình** → thầy chỉ chỗ thiếu/mâu thuẫn và hỏi về điều kiện, để HS tự sửa (9.1).
- HS hỏi **"cái này là gì / vì sao có"** (khái niệm, hằng số, ký hiệu) → thầy trả lời thẳng, ngắn, rồi **khái quát hoá**
  lên nguyên lý chung để HS dùng được ở chỗ khác.
- Lỗi **trình bày** (chữ số có nghĩa, đơn vị, ký hiệu) → nói thẳng kèm con số cụ thể ("3 đến 4 chữ số có nghĩa").

Áp vào tutor: phân loại câu hỏi trước khi chọn tầng gợi ý. Câu hỏi khái niệm mà tutor cũng hỏi ngược ("Em nghĩ G là
gì?") là **sai phong cách** — HS đã hỏi vì không biết. Câu hỏi về bài làm mà tutor sửa hộ ("r phải là khoảng cách hai tâm")
cũng sai. Giọng: xưng "thầy – con", câu ngắn, đánh số khi có nhiều ý, không mở đầu bằng khen.
