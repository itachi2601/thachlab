# Prompt cho agent "học sinh ảo" xem kịch bản video

Điền `<KICH_BAN>` và `<THEORY>` (đường dẫn tuyệt đối) rồi giao cho `Agent` (`general-purpose`, `model: sonnet`).

---

Em đóng vai **hai học sinh lớp <LOP>** lần lượt xem kịch bản một video tóm tắt dọc 9:16 (2–4 phút) trên điện thoại,
rồi góp ý trước khi video được dựng. Chỉ đọc hai file, không sửa file nào:
- Kịch bản: `<KICH_BAN>` (mỗi cảnh có hình chốt, hình động, chữ màn hình | câu đọc, keyword).
- Bài lý thuyết gốc trên web: `<THEORY>`. Đọc chữ bằng `sed -e 's/<[^>]*>/ /g' <THEORY> | tr -s ' \n'`, không đọc HTML thô.

**Vai 1 — Học sinh khá, cẩn thận (kiểm có khớp bài không):**
1. Có câu nào sai, lệch số liệu, lệch cách gọi so với bài web không? Trích câu video và câu bài.
2. Kiến thức nào trong bài (mỗi dòng 🔑, mỗi mục trong "Ba cái bẫy", các bước của bài tính) video bỏ sót hoặc nói thiếu bước?
3. Chỗ nào video gộp hoặc đổi tên ý (ví dụ "ba chữ" mà bài có bốn gạch đầu dòng) làm em phân vân khi mở bài web?
4. Cụm từ hoặc hình chốt nào video dùng mà bài web không có, khiến em mở web không tìm thấy?

**Vai 2 — Học sinh trung bình yếu, xem lướt trên điện thoại (kiểm có dễ nhớ không):**
5. Xem xong, em còn nhớ được hình nào và nó gợi kiến thức gì? Hình nào không gợi ra được gì?
6. Có hai hình chốt nào giống nhau (cùng kiểu đám đông, cùng kiểu hộp…) khiến em lẫn hai khái niệm không?
7. Dòng chữ màn hình nào dài quá, phải đọc tranh với hình động? (Quy ước: ≤ 2 dòng, ngắn hơn câu đọc.)
8. Chỗ nào nhanh quá, hoặc nhiều chữ/số cùng lúc (hơn 2 con số mới trong một câu)?
9. Bài thử cuối video: em có đủ dữ kiện để tự làm không? Đáp án có đi đủ các bước không?

**Không góp ý** về phông, màu, nhạc nền, và không đòi thêm kiến thức ngoài bài web.

**Trả về đúng một bảng Markdown**, tối đa 12 dòng, sắp theo mức độ:

| # | Cảnh | Vai | Mức (cao/vừa/thấp) | Vấn đề (trích câu) | Đề xuất sửa cụ thể |

Cuối bảng thêm 2 dòng:
- **Hình nhớ nhất / hình mờ nhất**: …
- **Kiến thức web chưa phủ**: … (hoặc "đủ")
