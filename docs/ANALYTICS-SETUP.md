# Hướng dẫn thiết lập Phân tích điểm số và Chủ đề hay sai

## 📋 Tổng quan

Tính năng phân tích giúp học sinh:
- Xem xu hướng điểm qua các bài kiểm tra
- Xác định chủ đề/kiến thức em hay sai
- Nhận lời khuyên ôn tập lại

## 🔧 Bước 1: Chạy Migration Supabase

1. Mở **Supabase Dashboard → SQL Editor**
2. Chạy toàn bộ file: `docs/supabase-migration-topics.sql`
3. Điều này sẽ tạo bảng `exam_question_results`

```sql
-- Kết quả: Tạo bảng exam_question_results với các field:
-- - id (PK)
-- - exam_result_id (FK → exam_results)
-- - question_index (vị trí câu hỏi: 0, 1, 2...)
-- - topic (tên chủ đề: "Lực & chuyển động", "Năng lượng", ...)
-- - is_correct (true/false)
```

## 📝 Bước 2: Cấu trúc Câu hỏi với Topic

Khi tạo đề thi trong Supabase, **mỗi question phải có field `topic`**:

### Ví dụ: Multiple Choice
```json
{
  "type": "multiple_choice",
  "topic": "Lực & chuyển động",
  "question": "<p>Định luật II Newton phát biểu rằng?</p>",
  "options": [
    "<p>F = ma</p>",
    "<p>F = mv</p>",
    "<p>F = m/a</p>",
    "<p>F = a/m</p>"
  ],
  "answer": 0,
  "explanation": "<p>Theo định luật II Newton, lực tác dụng bằng khối lượng nhân gia tốc...</p>"
}
```

### Ví dụ: True/False
```json
{
  "type": "true_false",
  "topic": "Năng lượng",
  "question": "<p>Năng lượng không bao giờ bị mất?</p>",
  "statements": [
    {
      "text": "<p>Đúng, năng lượng chỉ chuyển hóa</p>",
      "answer": true
    },
    {
      "text": "<p>Sai, năng lượng có thể bị mất</p>",
      "answer": false
    },
    {
      "text": "<p>Phụ thuộc vào loại năng lượng</p>",
      "answer": false
    },
    {
      "text": "<p>Chỉ đúng với năng lượng cơ học</p>",
      "answer": false
    }
  ],
  "explanation": "<p>Theo định luật bảo toàn năng lượng...</p>"
}
```

### Ví dụ: Short Answer
```json
{
  "type": "short_answer",
  "topic": "Chuyển động thẳng",
  "question": "<p>Một xe chuyển động với vận tốc 20 m/s. Quãng đường xe đi được trong 5 giây là bao nhiêu mét?</p>",
  "answer": "100",
  "explanation": "<p>S = v × t = 20 × 5 = 100 mét</p>"
}
```

## 📊 Bước 3: Chi tiết câu sai được lưu tự động

Không cần nhập tay nữa — khi học sinh nộp bài, `ExamRunner` tự chấm từng câu và
lưu ngay vào `exam_question_results` (topic lấy từ câu hỏi, hoặc từ `topic`
của cả đề nếu câu không gán riêng, mặc định "Chưa phân loại" nếu cả hai đều
trống). Vì việc lưu này chạy ở phía trình duyệt học sinh, bảng cần có policy
insert cho học sinh — đã được thêm vào `docs/supabase-migration-topics.sql`
(chạy lại file này nếu bạn đã tạo bảng từ trước khi có policy insert).

Muốn phân tích chi tiết hơn theo từng câu (không chỉ theo cả đề), vào **Quản
trị → Đề kiểm tra**, mở từng câu và điền ô "Chủ đề riêng của câu" (tùy chọn).

## 🎯 Danh sách Topics Đề xuất

Sử dụng những topic này trong câu hỏi để phân loại nhất quán:

**Vật Lý 10:**
- Lực & chuyển động
- Năng lượng
- Chuyển động thẳng
- Chuyển động tròn
- Điện tĩnh học
- Từ trường

**Vật Lý 11:**
- Dao động điều hòa
- Sóng cơ
- Sóng ánh sáng
- Quang học
- Nhiệt học
- Động lực học

**Vật Lý 12:**
- Điện từ học
- Vật lý hiện đại
- Nguyên tử & hạt nhân
- Lượng tử
- Vũ trụ học

## 📈 Kết quả

Sau khi có dữ liệu:

1. **Biểu đồ điểm số** sẽ hiển thị xu hướng điểm qua các bài thi
2. **Bảng chủ đề hay sai** sẽ hiển thị:
   - Chủ đề
   - Tổng số câu
   - Số câu sai
   - % câu sai (color-coded: 🔴 đỏ nếu > 50%, 🟡 vàng nếu 30-50%, 🔵 xanh nếu < 30%)
3. Học sinh có thể bấm "Ôn tập" trong bảng chủ đề (hoặc nút gợi ý ở khối "Hôm
   nay học gì" đầu trang `/kiem-tra`) để lọc thẳng danh sách đề theo chủ đề đó

Hai khối này cùng biểu đồ điểm được gắn sẵn ở đầu trang `/kiem-tra` cho học
sinh (`components/analytics/TodayFocus.tsx`, `ScoreChart.tsx`,
`WrongTopicsTable.tsx`).

## 📞 Câu hỏi thường gặp

**Q: Nếu thêm topic sau khi tạo đề thi?**
A: Có thể cập nhật field `questions` trong bảng `exams`. Dùng Supabase Dashboard hoặc PostgreSQL UPDATE statement.

**Q: Topic có phải duy nhất không?**
A: Không, một câu hỏi chỉ thuộc một topic, nhưng có thể có nhiều câu cùng một topic.

**Q: Nếu học sinh chưa làm bài nào?**
A: Biểu đồ sẽ trống, bảng chủ đề sẽ hiển thị "Tuyệt vời! 🎉" message.
