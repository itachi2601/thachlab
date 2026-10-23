# Prompt cho subagent gán dạng (model sonnet, mỗi file in/ một agent, nhóm file nhỏ chung một agent)

Nhiệm vụ: gán mỗi câu hỏi Vật lí trong ngân hàng vào ĐÚNG MỘT "dạng bài tập" của bài học (hoặc null). Làm việc trong <thu_muc_lam_viec>.

Đọc in/<bài>_<chủ đề>.json (lesson_id, topic_id, `dang` = các dạng của bài dùng chung chủ đề này, mỗi dạng có ord, label có mức Dễ/Trung bình/Khá/Khó, problem = đề mẫu; `questions` = id, type, diff, q — có thể bị cắt ~420 ký tự).

Quy tắc:
- Gán câu vào dạng nào mà cách giải/kiến thức trọng tâm GIỐNG đề mẫu (cùng loại tình huống, cùng quy tắc/công thức chính). Tên dạng + đề mẫu là căn cứ chính; mức khó chỉ là gợi ý phụ.
- Không khớp rõ / khớp hai dạng ngang nhau / bị cắt không đủ biết / lạc đề → null. Thà null còn hơn gán sai: bộ này dùng để biết em yếu ở dạng nào.
- Chủ đề rộng nhưng khác loại bài (chỉ hỏi định nghĩa, đơn vị, tình huống khác hẳn) → null, kể cả khi file chỉ có MỘT dạng.
- Dạng là một tình huống ứng dụng cụ thể (đàn ghi ta, bếp từ, Foucault…) thì chỉ nhận câu ĐÚNG bối cảnh đó, không nhận câu lí thuyết chung của chủ đề.
- Một câu một dạng. Không sửa câu, không bịa số liệu. Liệt kê `unsure` các id chưa tới ~70% chắc.

Kết quả: ghi out/<tên file vào> dạng {"assign": {"<id>": <ord hoặc null>}, "unsure": [id…]}, đủ mọi id (kiểm bằng Python). Đọc từng câu rồi tự phân loại bằng suy luận — KHÔNG viết heuristic từ khoá. Báo ngắn: số câu mỗi dạng, null, unsure.
