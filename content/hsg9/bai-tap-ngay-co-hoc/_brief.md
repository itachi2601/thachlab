# Brief: bộ "Bài tập mỗi ngày" Cơ học — HSG KHTN 9 Vật lí (lớp 19)

Học sinh giỏi lớp 9 đã học: chuyển động cơ học, đồ thị chuyển động, tổng hợp và phân tích lực, định luật 1 Newton
(tham khảo `content/hsg9/cd13-chuyen-dong-va-do-thi/theory.src.html` và `content/hsg9/cd10-luc/theory.src.html` để dùng đúng
kí hiệu, phạm vi, g = 10 m/s²; KHÔNG dùng kiến thức ngoài chương trình lớp 9 như định luật 2, 3 Newton dạng tính gia tốc, đạo hàm).
Mỗi ngày 4 bài, tổng 30–45 phút, tự chấm theo đáp số. Cấp độ: bài 1 vận dụng (≈6 phút), bài 2–3 vận dụng cao (≈10 phút), bài 4 nhanh bẫy khái niệm (≈6 phút).

## Đầu ra
Một file JSON `content/hsg9/bai-tap-ngay-co-hoc/ngay-<N>.json` dạng:
{ "ngay": N, "chu_de": "…", "questions": [ 4 câu ] }
Mỗi câu theo ĐÚNG schema câu hỏi của bundle (xem mẫu `content/hsg9/cd03-dien-tro-dinh-luat-ohm/luyen-tap/bundle.json`):
- short_answer: {type, question, answer:"0,51" (dấu phẩy thập phân kiểu Việt, một số, KHÔNG đơn vị), explanation, topic, form:"bai_tap", difficulty}
  — đề phải nói rõ làm tròn đến mấy chữ số và đơn vị cần điền.
- multiple_choice: {type, question, options[4] (không đánh A/B/C/D), answer: chỉ số 0–3, explanation, distractorNotes{A,B,C,D trừ đáp án đúng}, topic, form, difficulty}; đáp án đúng phân bố không dồn một vị trí.
- true_false: {type, question, statements:[{text, answer:true|false} ×4], explanation, topic, form, difficulty}
- difficulty ∈ "de" | "trung-binh" | "kho"; form ∈ "ly_thuyet" | "bai_tap".
Nội dung HTML: `<p>…</p>`, công thức KaTeX trong `$…$`, đơn vị `\ \text{m/s}`, số thập phân kiểu Việt `0{,}5`. Mỗi ý một đoạn `<p>`, không viết cả khối.
Giọng văn: không dùng vai "thầy", gọi "em" khi cần; đề ngắn gọn, số liệu gọn; một bối cảnh đời thường nếu tự nhiên (không gượng).
Lời giải (explanation): từng bước, mỗi bước một `<p>`, nêu rõ bẫy hay gặp ("Bẫy: …") và cách phát hiện.
Hình (cần cho bài đồ thị): SVG inline trong câu hỏi, ≤3 KB, `viewBox`, không width/height cứng, nét và chữ dùng `currentColor`
(hoặc `fill="none" stroke="currentColor"`), chữ ≥ 12 trong viewBox, có tên trục + đơn vị, không nền tô màu.
## Kiểm chứng bắt buộc
Mỗi đáp số phải được TÍNH LẠI bằng Python (chạy bằng Bash) và đối chiếu; đề phải có đúng MỘT đáp án; câu đúng/sai mỗi mệnh đề kiểm riêng.
Không bài nào được trùng với bài tập mẫu có sẵn trong `scripts/data/bai-tap-mau/162.json`, `155.json`, `167.json` (đọc lướt tiêu đề/dạng để tránh lặp đề).
Cuối cùng chạy kiểm hợp lệ: `python3 -c "import json;d=json.load(open('<file>'));print(len(d['questions']))"` rồi báo cáo ngắn: đề → đáp số đã tính.
