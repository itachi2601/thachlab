---
name: project_thachlab_hk2_lop10_4chuong
description: "Đăng 4 chương HK2 lớp 10 (IV Năng lượng-Công-Công suất, V Động lượng, VI Chuyển động tròn, VII Biến dạng vật rắn-Áp suất chất lỏng) lên LMS thachlab — nguồn docx GV, chạy song song qua 4 agent."
metadata:
  node_type: memory
  type: project
  originSessionId: b870550a-d2a0-448b-b869-ab7525857bae
  modified: 2026-09-24T04:20:26.672Z
---

Nguồn: `/Users/MAC/Documents/THPT/số hoá THPT/Vật Lý 10 - Dùng cho 3 sách - Bộ 1 - Theo form mới 2025(Xong)/HKII/` — 4 thư mục Chương IV-VII, 12 file .docx "Chủ đề N - GV" (lý thuyết + bài tập mẫu + 3 mục câu hỏi trắc nghiệm/đúng-sai/trả lời ngắn, đáp án phải tự suy từ "Hướng dẫn giải" vì đề GV không đánh dấu sẵn).

Đích: class_id=16 (Lớp 10), chapter_id 13/14/15/16, 12 lesson_id (68-79, xem chi tiết bảng ánh xạ trong lịch sử phiên 23/9/2026 nếu cần tra lại).

Quy trình: skill `mathtype-sang-omml` (ghi đè docx gốc, không backup) → skill `latex` (docx→LaTeX sạch) → tự dựng `exam.questions[]` (không có sẵn trong split_parts.py) → skill `dang-bai-hoc-thachlab` (bundle JSON) → `validateBundle` → lưu JSON vào `/Users/MAC/Documents/THPT/số hoá THPT/` (chưa upload — bước `upload-lesson.mts` cần thầy tự gõ SUPABASE_SERVICE_ROLE_KEY ở Terminal riêng, agent không được đụng key này).

**Trạng thái 23-24/9/2026:**
- ✅ Chương V (bài 28,29,30): `10-bai28-dong-luong.json`, `10-bai29-bao-toan-dong-luong.json`, `10-bai30-thuc-hanh-dong-luong.json` — validate sạch. Lưu ý: ~11% công thức lồng ngoặc/phân số phức tạp bị lỗi nhóm hiển thị (cần rà mắt), topic/form gán theo từ khóa chưa soát từng câu (nên chạy "AI gắn nhãn" sau đăng), 1 câu ĐS bị loại (đề gốc bỏ trống đáp án), vài câu TLN đã làm tròn cần xác nhận quy ước.
- ✅ Chương VI (bài 31,32): `10-bai31-dong-hoc-tron-deu.json`, `10-bai32-luc-huong-tam.json` — validate sạch, topic/form để trống toàn bộ (chưa chắc khớp danh mục con). 2 chỗ cần thầy chốt tay: Bài 31 MC Câu 36 (4 phương án gốc giống hệt nhau, thiếu đáp án nhiễu), Bài 32 MC Câu 8 (đọc hình vector 4 mũi tên chưa chắc chắn).
- ✅ Chương VII (bài 33,34): `10-bai33-bien-dang-vat-ran.json`, `10-bai34-khoi-luong-rieng-ap-suat.json` — validate sạch. 9 câu bị loại do đề gốc mâu thuẫn/thiếu hình rõ ràng (chi tiết trong báo cáo agent, không lưu lại đây).
- ✅ Chương IV (bài 23,24,25,26,27 — file "Chủ đề 2" đã TÁCH thành Bài 24 Công suất + Bài 27 Hiệu suất, file "Chủ đề 3"+"Chủ đề 4" đã GỘP thành Bài 25 Động năng-Thế năng): `10-bai23-nang-luong-cong.json`, `10-bai24-cong-suat.json`, `10-bai25-dong-nang-the-nang.json`, `10-bai26-co-nang.json`, `10-bai27-hieu-suat.json` — validate sạch, tổng 248 câu. Lưu ý: Bài 24 thiếu topic ở 22/44 câu (chạy "AI gắn nhãn" sau đăng); ~45+ câu bị loại toàn chương do lời giải nguồn không đủ rõ; 1 câu Bài 24 agent tự sửa đáp án đúng-sai lệch với lời giải gốc (15,3kW→13,5kW, cần rà kỹ vì là thay đổi nội dung Vật lý); Bài 26 Ví dụ 11 (Dạng 1, worked_examples) còn 1 chuỗi công thức dài agent tái dựng từ mạch lời giải, nên xem lại. Quá trình bị 2 lần gián đoạn (chạm hạn mức chi tiêu, rồi mất mạng ENOTFOUND) — cả 2 lần đều resume thành công qua SendMessage tới agent, xem [[feedback_spend_limit_auto_resume]].

**Đã đăng xong toàn bộ 12/12 bài lên Supabase 24/9/2026** (thầy tự chạy `upload-lesson.mts --target luyen_tap` qua Terminal riêng cho từng bài) — exam_id 102 (bài 68) → 113 (bài 79) liên tục, đã xác nhận qua REST `lesson_items`. Việc còn lại chỉ là rà các điểm lưu ý nêu trên (đặc biệt Chương V lỗi hiển thị công thức, Chương IV câu đáp án bị sửa/Bài 26 chuỗi công thức, Chương IV Bài 24 thiếu nhãn topic) và chạy "AI gắn nhãn" ở `/quan-tri/ngan-hang-cau-hoi` cho các câu còn thiếu topic/form.
