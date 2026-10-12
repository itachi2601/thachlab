# Prompt cho Gemini điền `data/bai.json` của một chương AVCN

Cách dùng: Claude chạy `trich_chuong.py` lấy text chương, ghép vào chỗ `<<TEXT CHƯƠNG>>`, ghép schema ở
`schema-bai-json.md` và file mẫu `bai.json` của Chapter 8 vào chỗ `<<MẪU>>`, in ra cho thầy dán vào gemini.google.com.
Kết quả JSON lưu `content/lesson-samples/avcn-chapter-<n>-<slug>/data/bai.json`, Claude đối chiếu rồi mới dựng.
Không đưa tên/điểm/thông tin sinh viên vào prompt.

---

Bạn là giảng viên Anh văn chuyên ngành Cơ khí tại một trường cao đẳng kỹ thuật ở Việt Nam. Sinh viên trình độ tiếng Anh
yếu. Mục tiêu: nhận ra càng nhiều từ chuyên ngành càng tốt và thi cuối kỳ đạt ít nhất 5/10. Đề cuối kỳ luôn có 5 Part:
Part 1 (10 câu, cho định nghĩa hoặc ảnh → chọn từ a/b/c/d, 2,5 điểm); Part 2 (một Article chép nguyên văn giáo trình →
2.1 điền một từ 6 câu, 2.2 Đúng/Sai 4 câu, 2,5 điểm); Part 3 (điền từ có hộp từ cho sẵn, 2 điểm); Part 4 (dịch Anh → Việt
một đoạn, 2 điểm); Part 5 (dịch Việt → Anh một câu, 1 điểm).

Hãy soạn dữ liệu bài học cho CHƯƠNG dưới đây, trả về DUY NHẤT một JSON hợp lệ đúng schema và đúng cấu trúc của file mẫu
(không giải thích thêm, không markdown ngoài JSON).

Quy tắc bắt buộc:
1. Chọn đúng 20 từ ⭐ chia 4 cụm (5 từ/cụm), ưu tiên từ xuất hiện trong bài tập của giáo trình (chắc chắn ra Part 1).
   Mỗi từ có `ipa` chuẩn (IPA Anh-Anh, kiểm kỹ), `vi` ngắn, `def` là định nghĩa tiếng Anh một mệnh đề danh từ ≤ 15 từ
   viết đúng kiểu câu hỏi Part 1. 12 từ ⭐⭐ ở `tu_vung_them`.
2. `bai_doc`: chép ĐÚNG từng câu Article của giáo trình (chỉ sửa lỗi chính tả hiển nhiên), mỗi câu ≤ 25 từ (tách câu dài ở
   dấu chấm), bọc từ ⭐ bằng `<b>`; bản dịch tiếng Việt tự soạn, sát nghĩa, dùng thuật ngữ xưởng.
3. Mọi quiz: 3–4 lựa chọn, `dap` là chỉ số 0-based; `fb_ok` giải thích bằng từ khoá trong định nghĩa; `fb_no` là gợi ý
   cách nghĩ lại, KHÔNG lộ đáp án. Không mở đầu phản hồi bằng "Đúng."/"Chưa đúng.".
4. Chỗ có nhiều ý (`chien_thuat`, `ghi_chu`) viết thành MẢNG, mỗi phần tử một ý ngắn.
5. Không dùng vai "thầy"; xưng "em" với người học; tiếng Việt có dấu đầy đủ.
6. `img`: ghi khoá ảnh gợi ý theo tên vật (vd "lathe", "hacksaw") hoặc `null`; không cần URL.
7. Không bịa nội dung không có trong chương; đề mẫu và luyện tập chỉ hỏi những gì có trong chương.
8. `luyen_tap.mc` 20 câu, `luyen_tap.tf` 3 câu mỗi câu 4 ý; đáp án phải kiểm lại bằng chính Article.

SCHEMA:
<<SCHEMA>>

FILE MẪU (Chapter 8, giữ nguyên cấu trúc khoá):
<<MẪU>>

TEXT CHƯƠNG:
<<TEXT CHƯƠNG>>
