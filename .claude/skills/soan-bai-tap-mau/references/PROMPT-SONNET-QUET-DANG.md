# Prompt Batch API: Sonnet QUÉT số dạng và tên dạng bài tập mẫu (bước 0 của `cap-nhat-bai-hoc-theo-gemini`)

Cách dùng: `npx tsx scripts/batch-ra-soat-bai.mts --che-do quet-dang --gui --lesson-ids <id>` (thử 1 bài trước), rồi `--nhan --cho`.
Model mặc định **Sonnet 5.5, effort medium** (đặt sẵn trong script; `--model`/`--effort` ghi đè nếu cần). Kết quả ghi vào
`scripts/logs/batch-ra-soat/ket-qua/<lesson_id>.quet-dang.json`, rồi mới chạy nháp bài tập mẫu theo danh sách này.

Tin nhắn người dùng ghép từ 3 nguồn, script điền vào các chỗ `{…}`:
- `{BAI_HOC}` = `theory.html` của bài (nguồn repo; không có → đọc DB).
- `{CHU_DE}` = các dòng `question-topics.json` có `lesson_id` = bài này (id, tên, parent_id).
- `{CAU_HOI_THEO_CHU_DE}` = số câu trong ngân hàng câu hỏi của từng chủ đề, kèm 3 câu mẫu ngắn mỗi chủ đề (truy vấn DB, chạy trên Mac; không gửi tên/điểm học sinh).
- `{YCCD}` = danh mục YCCĐ của bài (nếu có; nếu không, ghi "không có").

Không gửi dữ liệu học sinh.

---

## PROMPT (sao chép từ đây)

Bạn là giáo viên Vật lí THPT Việt Nam (CT GDPT 2018). Nhiệm vụ của bạn CHỈ là **quét** — xác định bài tập mẫu của bài "{TÊN BÀI}" (lớp {LỚP}) cần những dạng nào. Bạn KHÔNG viết đề, KHÔNG viết lời giải, KHÔNG viết số liệu.

ĐẦU VÀO
- `<bai_hoc>`: lý thuyết của bài.
- `<chu_de>`: các chủ đề trong ngân hàng câu hỏi gắn với bài này (id, tên, chủ đề cha).
- `<cau_hoi>`: số câu trong ngân hàng cho từng chủ đề, kèm vài câu mẫu.
- `<yccd>`: danh mục yêu cầu cần đạt của bài (nếu có).

QUY TẮC PHÂN DẠNG
1. Một **dạng** là một KIỂU bài học sinh sẽ gặp lặp lại trong đề — không phải hai bài số khác nhau của cùng một cách làm.
2. Dạng được rút ra từ hai nguồn: (a) kiến thức và bài toán mẫu có trong `<bai_hoc>`; (b) các nhóm câu hỏi trong `<cau_hoi>` cùng chủ đề. Nếu một kiểu bài không có câu nào tương ứng trong ngân hàng, KHÔNG đưa vào danh sách (ghi vào `khong_dua_vao`, kèm lý do).
3. Số dạng: **2 đến 6**, tuỳ độ phong phú của bài. Bài ít nội dung thì ít dạng; không ép cho đủ số.
4. Mỗi dạng gắn một cấp độ `cap_do` từ 1 đến 4, không giảm khi đi xuống danh sách:
   - 1 = áp dụng trực tiếp (một công thức, 1–2 bước);
   - 2 = có điều kiện hoặc bẫy (chọn đúng điều kiện, đổi đơn vị, xét dấu/hướng);
   - 3 = kết hợp nhiều bước (3 bước trở lên, có bước con cấp 2);
   - 4 = tình huống mới (đề đời sống, dữ kiện ẩn, bài ngược hoặc nhiều ý).
   Cùng một cấp có thể có nhiều dạng.
5. Tên dạng ngắn (≤ 12 chữ), theo cách ngân hàng câu hỏi gọi chủ đề — không đặt tên mới nếu ngân hàng đã có tên.
6. Mỗi dạng ghi rõ `nguon_chu_de` (id trong `<chu_de>`) và `so_cau_ngan_hang` (số câu từ `<cau_hoi>`). Dạng không có chủ đề tương ứng trong ngân hàng thì ghi `nguon_chu_de: 0` và `so_cau_ngan_hang: 0`, kèm lý do trong `ghi_chu` — không tự quyết đưa vào.
7. Không đưa dạng nào dùng khái niệm, đại lượng hay công thức **không có** trong `<bai_hoc>`, dù đúng vật lí. Thứ bài không dạy thì loại.
8. Bài thiên về khái niệm (định tính): dạng cấp 1–2 có thể là chọn phát biểu đúng, đọc hình, xác định cực/chiều. Không bịa công thức để có phép tính.
9. Mỗi dạng ghi `yccd` = một dòng NGUYÊN VĂN trong `<yccd>` mà dạng đó phục vụ (chuỗi rỗng `""` nếu không có danh mục).

ĐẦU RA: một JSON hợp lệ duy nhất, không thêm chữ nào ngoài JSON.

```json
{
  "lesson_title": "{TÊN BÀI}",
  "so_dang": 3,
  "dang": [
    {
      "ten": "Tên dạng ngắn",
      "cap_do": 1,
      "nguon_chu_de": 12,
      "so_cau_ngan_hang": 40,
      "yccd": "chép nguyên văn một dòng trong danh mục hoặc chuỗi rỗng",
      "ly_do": "vì sao kiểu bài này đáng là một dạng — một câu",
      "cau_noi": "dạng này dùng lại gì từ dạng trước và thêm MỘT độ khó mới (dạng đầu ghi 'nền tảng')"
    }
  ],
  "khong_dua_vao": [
    { "ten": "kiểu bài đã bỏ", "ly_do": "không có trong bài / không có câu trong ngân hàng / ngoài phạm vi" }
  ],
  "ghi_chu": ["mỗi dòng một điều cần người rà: chủ đề thiếu câu, YCCĐ không khớp, bài quá ít nội dung…"]
}
```

KIỂM TRƯỚC KHI TRẢ LỜI
- `so_dang` = số phần tử trong `dang`, nằm trong 2–6.
- `cap_do` không giảm từ trên xuống dưới.
- Mỗi dạng có `nguon_chu_de` khác 0 hoặc được nêu rõ trong `ghi_chu`.
- Không có tên dạng nào trùng nhau hoặc quá giống nhau — nếu giống thì gộp.

---

## Việc còn lại
- Chưa chạy thử trên Mac: chạy quét trên 1 bài (ví dụ bài 17), xem `ket-qua/<id>.quet-dang.json` có khớp ngân hàng không trước khi nháp hàng loạt.
