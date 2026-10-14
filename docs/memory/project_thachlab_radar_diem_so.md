---
name: project-thachlab-radar-diem-so
description: Mạng nhện năng lực có điểm trên đỉnh, mã B1..Bn, chạm đỉnh↔hàng; deploy 14/10/2026
metadata:
  type: project
---

14/10/2026: `components/results/ChapterMasteryRadar.tsx` thêm vòng điểm trên đỉnh (viền theo mức), nhãn B1..Bn, số chia thang 25–100, chạm đỉnh ↔ hàng bảng, bản gọn đóng khung bài yếu nhất. Mẫu: `docs/mau-thiet-ke-radar-diem-so.html`. Đã vào main (ab0accbf1) và deploy.

**Why:** học theo biểu đồ UI GreenMetric thầy đưa; không đụng RPC/migration.
**How to apply:** CHƯA thử 375px với dữ liệu thật (đỉnh gần điểm nhau có thể đè). Còn treo: chế độ "Theo chủ đề YCCĐ / Cả năm", bản phụ huynh riêng (≤4 trục, chữ ≥18px), chồng nhiều em cho GV. Không làm "so với trung bình lớp" cho HS. Liên quan [[project_thachlab_dashboard_gv_thpt]].

**14/10 (tối):** thêm bộ chuyển phạm vi — `CourseRadar` bọc `RadarView`: "Theo chương" (đỉnh = bài, có ô chọn chương) / "Cả khoá" (đỉnh = chương, gộp Σđiểm/Σmax; khoá HSG mặc định "Theo mảng", mảng chưa làm vẽ ở tâm dấu –). RPC mới `get_my_course_mastery_pct` (migration 20261014160000), chưa chạy thì tự lùi về RPC cũ, không có bộ chuyển. Giáo viên (preloaded) giữ bản cũ. Chưa làm "Theo học kì" (không có trường học kì); chưa thử 375px dữ liệu thật.
