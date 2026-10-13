---
name: project-thachlab-chua-bai-mobile-ta
description: Bảng chữa bài chiếu từ iPhone ngang + trợ giảng vào Phân tích/Chữa bài (RLS exam_results) + sửa UI trang Xếp hạng mobile (11/10/2026)
metadata:
  type: project
---

**Mục tiêu:** thầy/trợ giảng chiếu bảng chữa bài từ iPhone (AirPlay/cáp HDMI) lên tivi; trợ giảng dùng được tab Phân tích như thầy.

**Đã xong (đều đã deploy, đã push main, 2026-10-11):**
- `d87b5bd81` — `components/dashboard/ReviewBoard.tsx` + `app/globals.css` (khối "Nút chạm… iPhone xoay ngang", `@media (orientation: landscape) and (max-height: 520px)`): thanh trên/dưới gọn, đáp án 2 cột, nút ‹ Hiện đáp án/lời giải Ẩn ›, vuốt ngang đổi câu, Wake Lock giữ sáng, ẩn nút Toàn màn hình khi trình duyệt không hỗ trợ (iPhone Safari). Ở chế độ ngang trên điện thoại ô lọc "<70%" và chú giải màu bị ẩn.
- `57936b2c8` — `TeacherThptAnalysis.tsx`: trợ giảng bấm "Trình chiếu chữa bài" → `/tro-giang/chua-bai` (trang `/dashboard-thpt/chua-bai` có `RequireAuth area="thpt"` chặn TA).
- `45095b973` + chạy tay trong SQL Editor — migration `20261011180000_ta_doc_ket_qua_lam_bai`: policy `ta read student results` trên `exam_results` dùng `teaches_student(student_id)`. **Nguyên nhân gốc:** `exam_results` chỉ cho đọc: chính HS, `is_admin()` (role='admin'), `class_instructors`; TA không thuộc nhóm nào nên danh sách đề rỗng. Ghi chú cũ ở `20261010700000_ta_doc_thanh_vien_lop` ("đọc được qua teaches_student") chỉ đúng cho `exam_question_results`/`exam_attempts`.
- `3c7f94005` — trang Xếp hạng mobile: `TierLadder.tsx` bỏ `truncate` ở dải RP phân bậc (ô xếp dọc), nhãn ≥13px màu `text-muted`; `RankPage.tsx` tách dòng Mùa; `BugReportWidget.tsx` thu thành nút tròn icon <640px (C1, D2, B6, M2).

**Còn chờ / chưa kiểm:**
- Chưa thử trên iPhone thật + tivi (xoay ngang, AirPlay), chưa chụp 375px trang Xếp hạng sau sửa (cần tài khoản HS).
- Chưa xác nhận bằng tài khoản trợ giảng thật rằng danh sách đề đã hiện sau migration; nếu vẫn rỗng kiểm `ta_assistants` (tài khoản phải `active`).
- Trang Xếp hạng trên điện thoại thầy hiện NỀN TỐI dù M7 mặc định sáng — chưa rõ do HS chọn tối, build cũ hay trang đang cố định màu tối.
- Chưa làm: chữ giải thích "cả bậc Đồng / phân bậc III" ở chỗ 0–199 RP và 0–65 RP đứng gần nhau.
- Quyền TA đọc `exam_results` áp mọi lớp (do `ta_all_classes`); nếu sau này giới hạn TA theo lớp phải sửa cả `teaches_student`.

**Bài học:** chức năng của một vai "trống" → kiểm RLS bảng nguồn, đừng tin ghi chú migration cũ. Deploy từ worktree sạch: `rm -rf` worktree xong còn sót `node_modules` ("Directory not empty") — chạy lại `rm -rf` sau vài giây; thầy từng phải xoá tay `.claude/worktrees/deploy-xh`. Liên quan: [[project_thachlab_ta_policy]], [[feedback_deploy_autonomy]].
