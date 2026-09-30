# Prompt sinh câu (Bước B) — sửa ở đây, không sửa trong SKILL.md

Bạn soạn bộ "Kiểm tra nhanh" lý thuyết cho MỘT bài Vật lí THPT. Nguồn duy nhất: `summary_html` + `body_html`
của mục lý thuyết (đã kèm ở dưới) và bảng đoạn từ `list-sections.mts`. Không dùng kiến thức bài khác.

Sinh đúng 12 câu:
- 5 trắc nghiệm 4 đáp án: 2 định nghĩa/định luật, 2 chọn công thức đúng, 1 đơn vị/ý nghĩa ký hiệu.
- 3 đúng–sai: mỗi câu 4 ý xoay quanh 1 định luật/hiện tượng, ≥ 1 ý sai, ý sai phải sai tinh vi (đảo quan hệ,
  bỏ điều kiện áp dụng), không sai hiển nhiên.
- 4 trả lời ngắn: tính 1 bước với số tròn, hoặc điền hệ số/số mũ; đáp án ≤ 4 ký tự, chỉ gồm `0-9 , -`.
- Bài không có công thức → thay câu công thức bằng câu định nghĩa/hiện tượng.
- Mức độ: ≥ 8 câu Dễ, còn lại Trung bình, không Khó.
- Phương án nhiễu của câu công thức = lỗi HS hay mắc (đảo tử/mẫu, thiếu bình phương, sai dấu, nhầm đơn vị);
  không bịa công thức vô nghĩa. 4 phương án khác nhau, độ dài gần nhau, đáp án đúng rải đều A–D.
- Mọi câu có `explanation` ngắn (1–2 câu, nêu căn cứ trong bài). Công thức LaTeX `$…$`, $ phải cân.
- Mỗi câu gắn `theorySection` = chỉ số đoạn chứa căn cứ (đúng bảng `list-sections.mts`), `kind`, `topic`
  (có `question-topics.json` → tên YCCĐ của bài; không thì đúng `lesson.title`), `form: "ly_thuyet"`,
  `difficultySource: "ai"`.
- Trả về mảng JSON `questions` theo schema trong SKILL.md, không thêm key nào khác.
