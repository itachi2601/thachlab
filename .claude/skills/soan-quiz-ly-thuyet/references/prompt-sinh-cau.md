# Prompt sinh câu (Bước B)

Bạn soạn bộ "Kiểm tra nhanh" lý thuyết cho học sinh lớp 12, từ **duy nhất** phiếu kiến thức của bài (Bước A). Đầu vào: `body_html`, `summary_html`, danh sách đoạn từ `list-sections.mts`.

Sinh **20 câu**: 10 kiến thức + 10 công thức; 10 trắc nghiệm (4 phương án khác nhau, `answer` 0–3), 4 đúng–sai (4 ý/câu xoay quanh 1 định luật hoặc công thức, ≥ 1 ý sai), 6 trả lời ngắn (đáp án ≤ 4 ký tự: chữ số, `,`, `-`; hoặc hệ số/số mũ).

Quy tắc:
- Câu kiến thức: định nghĩa, phát biểu định luật, hiện tượng, điều kiện áp dụng, đơn vị/ý nghĩa ký hiệu (`kind`: dinh_nghia | dinh_luat | hien_tuong | dieu_kien).
- Câu công thức: chọn công thức đúng, suy đại lượng từ công thức, biến đổi một bước, tính một bước với số tròn (`kind`: cong_thuc | don_vi | tinh_nhanh | bien_doi).
- Phương án nhiễu của câu công thức = lỗi học sinh hay mắc (đảo tử/mẫu, thiếu bình phương, sai dấu, nhầm đơn vị). Không bịa công thức vô nghĩa.
- Mức độ: ≥ 14 câu `"de"`, còn lại `"trung-binh"`, **không có** khó. `difficultySource: "ai"`, `form: "ly_thuyet"`.
- Mọi câu phải trả lời được chỉ bằng nội dung mục lý thuyết của bài này; không dùng kiến thức bài khác, không đề cập hình mà học sinh không thấy trong câu.
- `theorySection` = chỉ số đoạn (từ `list-sections.mts`) nơi có đáp án; bài không có đoạn thì bỏ trường này.
- `explanation` không rỗng, 1–2 câu, nêu căn cứ ở bài. Công thức LaTeX `$…$`, cân dấu `$`; `\\` trong JSON phải viết `\\\\`.
- Không trùng câu; ưu tiên phủ đều các đoạn. Bài ít công thức: lấy hết công thức có, bù bằng câu kiến thức, ghi `review.counts` đúng thực tế.
- Nếu bài chỉ là công thức chung chung mà hệ số phụ thuộc số liệu ngoài bài → không hỏi số liệu đó.
