# Prompt cho Cursor (chế độ Auto) — rà hình AI vẽ cho câu hỏi Vật lí

Đính kèm `input.json` (mỗi phần tử: `id`, `grade`, `topic_name`, `question`, `ai_figure`). `ai_figure` là SVG/thông số đồ thị do AI vẽ cho câu đó.

Với MỖI câu, đối chiếu hình với đề bài (câu dẫn, phương án, số liệu) và trả về một phần tử JSON:

```json
{"id": 123, "verdict": "ok|sai|khong_chac", "van_de": ["..."], "de_xuat": "giữ|vẽ lại|bỏ|cần ảnh thật"}
```

Kiểm cụ thể: (1) số liệu/đơn vị/trục trên hình khớp đề; (2) pha, chiều, độ lớn, cực trị, giao điểm đúng; (3) hình có tiết lộ đáp án không; (4) nhãn, góc, chiều mũi tên đúng; (5) SVG có vỡ/tràn khung. Không đoán: thiếu dữ kiện thì `khong_chac` và nói thiếu gì. Chỉ trả mảng JSON, không giải thích thêm.

Lưu kết quả thành `scripts/data/ai-figure-review/output.json` rồi nộp lại cho Claude đối chiếu trước khi bấm "Dùng hình này".
