---
name: project_thachlab_dashboard_gv_thpt
description: Dashboard giáo viên THPT (/dashboard-thpt) — sửa lẫn đề giữa khối, gộp tab, nút chiếu câu; commit 137387c07, chưa thử trên trình duyệt
metadata:
  type: project
---

**Mục tiêu**: tab Phân tích của `/dashboard-thpt` chỉ hiện đề của khối đó; chữa bài trên lớp nhanh hơn; bớt tab. Khởi từ bản nhận xét 2026-10-13 (thầy dán).

**Đã xong (2026-10-13, commit `137387c07`, trên main, chưa push)**:
- `components/dashboard/TeacherThptAnalysis.tsx`: danh sách đề lấy từ `exam_classes` của cả khối (`expandClassIdsByGrade`), đề HS tự làm ngoài khối xếp nhóm "Đề khác lớp đã làm"; mỗi đề hiện `n/N nộp` + nhãn `[Định kỳ]`; ô tìm đề khi >8 đề; nút "Chiếu câu này" trong mỗi câu sai.
- `components/dashboard/ReviewBoard.tsx`: nhận `?q=<chỉ số câu>` làm câu mở đầu (cả `/dashboard-thpt/chua-bai` và `/tro-giang/chua-bai`).
- `components/dashboard/TeacherThptDashboard.tsx`: 11 → 9 tab (Cảnh báo+Phụ đạo; Ghi danh+Nhập danh sách xếp chồng trong một tab). Kiểu `DashboardTab` vẫn giữ id `tutoring`/`roster` nhưng không còn tab tương ứng.

**Còn chờ**:
- Chưa mở trình duyệt thử (lọc đề, `n/N`, nút chiếu câu, 375px) — phải thử trước khi coi là xong.
- Chưa push.
- Hỏi thầy: đề gán theo KHỐI hay theo TỪNG LỚP? Đang lọc theo khối; nếu theo từng lớp thì đổi `classIds` thành `[classId]`.

**Quyết định**: không chia 3 nhóm điều hướng (tốn thêm một cú chạm, Điểm danh bị chôn sâu); chỉ gộp 2 cặp tab liên quan. Chỉ cân nhắc lại khi có số liệu mở tab.
Lint: 2 lỗi `set-state-in-effect` ở Analysis có từ trước (`setOverview(null)` trong effect), chưa sửa.

**13/10 tối — 5 tính năng đề xuất đã viết (chưa commit, chưa thử trình duyệt; tsc + eslint sạch, logic thử bằng tsx)**:
- Thầy chốt: đề gán theo KHỐI (giữ nguyên lọc hiện tại).
- `services/class-insights.ts` (mới): mastery tính client từ `exam_question_results`+`practice_question_results` (quy tắc `docs/mastery-rules.md`), nhóm 3 em + 1 em kèm, cảnh báo sớm (ngưỡng ở `EARLY_THRESHOLDS`: 10 ngày, giảm ≥1.5 điểm/3 đề, nhanh <35% trung vị mà <5 điểm — ĐOÁN, chỉnh theo lớp thật).
- `TeacherThptMastery.tsx`: tab Phân tích → nút "Bản đồ thành thạo" (ma trận HS × bài, "Nên nhóm lại trước", gợi ý nhóm, chép danh sách).
- `TeacherThptClassroomMode.tsx`: khối "Vào lớp" đầu tab Tổng quan (vắng/trễ buổi trước, 2 câu sai nhất đề gần nhất + nút Chiếu, ai chưa nộp, ghi chú localStorage — chỉ trên máy đó).
- `TeacherThptEarlyWarning.tsx`: "Cần để ý sớm" đầu tab Cảnh báo & phụ đạo.
- `TeacherThptAnalysis.tsx`: `AnswerSpread` — phân bố đáp án A–D, báo ≥30% lớp cùng chọn một đáp án sai; đúng–sai hiện % đúng từng ý.
- Chưa làm/hạn chế: không có nút tạo phụ đạo tự động; lượt >12 tháng đã rollup không tính; truy vấn tải toàn bộ dòng của lớp (chia 40 em/lượt, phân trang 1000) — nếu chậm thì làm RPC gộp.
- 13/10 muộn: Hồ sơ học sinh (GV) có thẻ Kiểm tra đầu vào + radar năng lực chương (`ChapterMasteryRadar` thêm prop `preloaded`; số liệu từ `buildChapterRadar` ở `services/class-insights.ts` vì RPC `get_my_chapter_mastery_pct` chỉ đọc theo auth.uid()). Chưa thử trình duyệt.
- 13/10 đêm: **Tiến trình dạy** — tab mới "Tiến trình dạy" (`TeachingProgressTree.tsx`, dùng chung với trợ giảng ở `/tro-giang/tien-trinh`): tick đã dạy theo bài (kèm ngày → tuần), ghi chú cải tiến lưu theo KHỐI qua các năm (năm sau thấy ghi chú cũ), lịch tuần lấy từ lịch khoá đã đăng. Tick đẩy mốc `thpt_courses.current_topic_id` (phục vụ bù bài). Migration 230000 + 233000 đã chạy. Nút "Mời làm kiểm tra đầu vào" ở Hồ sơ học sinh (RPC `thpt_invite_entry_diagnostic`: tạo đăng ký joined_late/active, cần đã đặt mốc). Chưa thử trình duyệt/tài khoản TA thật; TA phải có trong `ta_assistant_classes` và `active`.
