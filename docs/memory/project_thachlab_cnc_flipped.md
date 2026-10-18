---
name: project-thachlab-cnc-flipped
description: "Khung CNC lớp đảo ngược (CĐ, 12 buổi x 5 giờ, 30 em/6 máy + WinNC 3D View); bài 1 mẫu đã ghi cnc_lessons id flip-1 ngày 18/10/2026"
metadata:
  type: project
---

Thầy dạy CNC ở CĐ: buổi 5 giờ (GV dạy 1–2 giờ đầu), 6 buổi/tuần x 2 tuần = 12 buổi, ~30 em, 6 máy, xưởng có WinNC 3D View (số máy tính chưa rõ). Khung: `docs/CHUONG-TRINH-CNC-FLIPPED.md` (A tối trước ≤20', B 300', C sau buổi; nhóm chia hai trạm máy thật/WinNC, đổi trạm).

- Bài mẫu (buổi 1 nhập môn, làm lại 18/10 theo đúng chương trình thầy): `content/lesson-samples/cnc-flipped-buoi-1/`; ghi DB bằng `scripts/them-bai-cnc.mts --meta meta.json` → `cnc_lessons.id='flip-1'` (sort_order 8, hoàn tác `delete from cnc_lessons where id='flip-1'`). Bài cũ lesson-1…6 và intro KHÔNG bị đụng.
- Phải vá `CncCourseWorkspace.tsx` (fallback `itemMeta`) và deploy TRƯỚC khi thêm dòng DB: id lạ làm trắng trang CNC.
- Treo: thầy chưa xác nhận số máy tính WinNC, thứ tự 12 buổi (vận hành trước lập trình), cổng 4/5; 4 buổi cần bài mới (lập trình tiện/phay 2, sửa lỗi–chế độ cắt, dự án). Tiêu đề trang vẫn ghi "7 bài học" cứng.
- Bản commit cũ 8d47b8ace ghi nhầm "buổi 180 phút, thầy chốt" — đã sửa lại 5 giờ.
- Bài học 18/10: thầy sửa "bài 1 chưa hợp lý" — buổi đầu của thầy gồm nội quy, giới thiệu máy, điểm chuẩn, hệ điều khiển WinNC, lệnh, chương trình cơ bản; 12 buổi phải bám 7 bài hiện có (70 tiết) chứ không tự bịa bài/đảo thứ tự. Trước khi thiết kế chương trình: đọc mục lục các bài đã có và hỏi thầy buổi đầu dạy gì. O0001 chưa chạy thử trên WinNC thật.
