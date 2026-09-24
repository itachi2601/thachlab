# ROADMAP ThachLab (cập nhật 23/09/2026 — bản đối chiếu mã nguồn)

Triết lý: **"Cho hết kiến thức. Bán sự đồng hành."**
Khác biệt: *Hệ thống biết học sinh đang yếu ở đâu và biết đưa học sinh đi đâu tiếp theo.*

Nguyên tắc: mọi tính năng phía học sinh (Learning Journey, AI Tutor, phân tích lỗi sai) đứng trên **một bộ khung kỹ năng + dữ liệu làm bài**. Khung đó nay đã có — từ đây ưu tiên quay về **phía học sinh**, không mở rộng thêm mảng quản lý cho tới khi Learning Journey ra mắt.

Quy ước mức độ câu hỏi: **Dễ / Trung bình / Khó** (thay cho NB/TH/VD/VDC — dùng chữ học sinh hiểu ngay).

---

## Giai đoạn 0 — Nền dữ liệu ✅ (xong 9/2026, còn 1 việc)
Đã có:
- Khung kỹ năng = `question_topics` (Lớp → Chương → Bài) + tầng con **yêu cầu cần đạt** (`parent_id`), seed ~3 YCCĐ/bài cho lớp 9–12. Sửa tại /quan-tri/chu-de.
- Câu hỏi gắn Chủ đề + Dạng (lý thuyết/bài tập) khi đăng đề; AI tự gắn nhãn phần thiếu (`classify-questions`).
- Dữ liệu làm bài: `exam_attempts`, `exam_question_results` (từng câu), `practice_question_results`, `lesson_progress`.
- Native quiz: TN / đúng–sai / trả lời ngắn, chấm ngay, làm từng câu, chống rời tab, xem lại bài.
- Azota: chỉ nhập/xuất đề, không tích hợp điểm.
- Bug CNC bài 2–3: đã sửa toàn bộ (redesign CNC 21–22/09).

Còn lại:
- [ ] Gắn **mức độ Dễ / Trung bình / Khó** cho câu hỏi (cột `difficulty`) ngay ở trang Đăng đề; AI gợi ý mức khi thiếu. Đây là nút thắt cuối cùng trước khi lọc luyện tập và tạo đề theo ma trận.

## Giai đoạn 1 — Học + Luyện tập có phản hồi (Q4/2026, đang ~60%)
Đã có: phiên luyện tập bốc từ ngân hàng theo bài, đếm giờ, lời giải; 6 loại mục trong bài học; phân tích lỗi sai rule-based (`tutoring_needs`: sai ≥50% trong 2 bài gần nhất → cần phụ đạo), cảnh báo điểm thấp, panel "Ôn lại lỗi sai".
Còn lại:
- [ ] Nhãn sau mỗi bài: *Nắm vững / Cần luyện thêm / Chưa đạt* tính theo tỉ lệ đúng **trên từng YCCĐ** (không chỉ hoàn thành/đạt cả bài).
- [ ] Trang Luyện tập lọc theo lớp / chương / bài / YCCĐ / mức độ Dễ–TB–Khó.
- [ ] Hiện "3 kỹ năng yếu nhất" ngay cho học sinh (dữ liệu đã có ở tab Phụ đạo của GV, chỉ cần mở ra phía học sinh).
- [ ] Chương mẫu **Vật lý 10 – Động học**: đủ ảnh lý thuyết + ngân hàng ≥ 30 câu/bài có mức độ, đo trên lớp offline 1 tháng.

## Giai đoạn 2 — Learning Journey (Q1/2027 — mốc ThachLab 2.0)
Đã có: thẻ "Tiếp tục từ nơi em đã dừng", % hoàn thành bài, `StudentCompetencyCard`.
- [ ] Trang lộ trình cá nhân theo chương: % hoàn thành, trạng thái từng bài ✅ 🟡 🔴 từ nhãn ở GĐ 1.
- [ ] Đề xuất rule-based: YCCĐ yếu nhất chưa qua ngưỡng → bài học + 10 câu luyện đúng YCCĐ đó (dùng `tutoring_needs`).
- [ ] Ra mắt công khai ThachLab 2.0 với chương Động học 10 hoàn chỉnh.

## Giai đoạn 3 — Khám phá / Mô phỏng (song song từ Q1/2027, 1–2 mô phỏng/tháng)
Đã có: con lắc lò xo SVG + rAF (`SpringSimulation`) — đang làm hero trang chủ.
- [ ] Nhúng con lắc vào bài Dao động kèm bộ câu hỏi (không để mô phỏng đứng rời).
- [ ] Đồ thị x–t, v–t → rơi tự do, ném ngang → sóng → nhiệt học → điện học.
- Không làm mô phỏng nào không gắn với một bài học + một bộ câu hỏi.

## Giai đoạn 4 — AI Tutor Socratic (Q2–Q3/2027)
- [ ] MVP trên Claude API: prompt Socratic — hỏi gợi mở, chia nhỏ bài, phát hiện lỗi tư duy; chỉ đưa đáp án sau ≥2 gợi ý hoặc khi bấm "Em bó tay".
- [ ] AI đọc `exam_question_results` + `tutoring_needs` của học sinh để gợi ý đúng chỗ yếu.
- [ ] Giới hạn lượt/ngày cho tài khoản miễn phí → tính năng trả phí đầu tiên.
- Cách làm: tự dựng MVP, chạy thật 1 học kỳ, rồi mới thuê dev làm bản production.

## Giai đoạn 5 — Teacher Studio (đã làm sớm ~70%, chỉ hoàn thiện)
Đã có: quản lý lớp/khoá học, ghi danh, import roster, giao bài, gradebook, điểm danh, phân tích lỗi sai theo lớp, phụ đạo, phụ huynh, thông báo, tin nhắn, báo lỗi, mời giáo viên/trợ giảng.
- [ ] Tạo đề tự động theo ma trận (YCCĐ × Dễ–TB–Khó) từ ngân hàng — chờ GĐ 0 gắn xong mức độ.
- [ ] Nút xuất Word/PDF trong web (tận dụng skill de-vat-ly-thpt).
- Không thêm tính năng quản lý mới cho tới khi ThachLab 2.0 ra mắt. Mở cho giáo viên khác chỉ khi có ≥3 người xin dùng.

## Giai đoạn 6 — Premium & mở rộng (2028)
- Gói trả phí = AI Tutor không giới hạn + lớp online có giáo viên theo dõi + luyện đề chuyên sâu. Kiến thức nền giữ miễn phí.
- Lớp 9: đã seed KHTN 9 + YCCĐ, mở nội dung khi lớp 10–12 ổn. Mobile app chỉ khi web đạt ≥500 học sinh hoạt động hàng tuần.

## Ngoài roadmap Vật lý (giữ, không mở rộng thêm)
Mảng CNC/CTTC (điểm danh máy, checklist, rubric, bản vẽ, thiết bị, chủ nhiệm) và hệ trợ giảng đã hoàn chỉnh cho nhu cầu hiện tại — chỉ sửa lỗi, không thêm tính năng.

---

## Việc bắt đầu ngay (tuần 23/09/2026)
1. Thêm chọn mức độ **Dễ / Trung bình / Khó** ở trang Đăng đề + backfill ngân hàng (AI gợi ý).
2. Commit/nạp ~25 bundle bài học đang chờ ở thư mục gốc.
3. Bắt đầu nhãn *Nắm vững / Cần luyện thêm / Chưa đạt* theo YCCĐ cho Động học 10.
