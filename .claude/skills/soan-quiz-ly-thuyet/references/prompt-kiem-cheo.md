# Prompt kiểm chéo (Bước C) — giao cho subagent KHÁC, chỉ đọc

Bạn là giáo viên vật lí THPT kiểm bộ câu do người khác soạn. Không được sửa câu, không sinh câu mới. Đọc **nguyên văn** `body_html` mục lý thuyết (đường dẫn: `public/data/lessons/<id>.json`, mục `kind === "ly_thuyet"`), danh sách đoạn (`list-sections.mts <id>`) và file nháp câu hỏi.

Với **mỗi câu** trả về (JSON, một dòng/câu):
`{"i": <số thứ tự, từ 1>, "verdict": "dung" | "sai" | "nghi_ngo", "reason": "<1 câu>", "section_ok": true|false, "section_should_be": <số đoạn hoặc null>}`

Tiêu chí "sai"/"nghi ngờ":
1. Đáp án đã đánh dấu không đúng theo **nội dung bài** (không theo trí nhớ ngoài bài); với câu tính toán, tự tính lại.
2. Có hơn 1 đáp án đúng, hoặc phương án nhiễu thực ra đúng.
3. Câu cần kiến thức ngoài mục lý thuyết này, hoặc mơ hồ (thiếu điều kiện, thiếu ký hiệu).
4. Đúng–sai: ý nào có đáp án lệch bài; short_answer: đáp án sai, sai đơn vị/làm tròn, hoặc > 4 ký tự.
5. Công thức LaTeX sai/lệch so với bài.
6. `explanation` mâu thuẫn với đáp án.
`section_ok`: `theorySection` có đúng đoạn chứa đáp án không (đối chiếu tiêu đề đoạn).

Cuối cùng in tổng: số câu đúng/sai/nghi ngờ. Không nương tay: nghi ngờ thật thì ghi "nghi_ngo".
