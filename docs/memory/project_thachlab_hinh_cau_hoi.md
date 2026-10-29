---
name: project-thachlab-hinh-cau-hoi
description: Hình SVG minh hoạ cho câu hỏi ngân hàng thiếu hình — thí điểm L10 Động lực học xong 57 câu, còn nhóm mơ hồ và đổi bố cục hình kế bên đề
metadata:
  type: project
---

**Mục tiêu (thầy yêu cầu 2026-10-29):** câu có mô tả hiện tượng/đồ thị/sơ đồ thì có hình minh hoạ; đồ thị/sơ đồ vẽ SVG, hiện tượng thực tế ưu tiên ảnh nguồn mở. Quy trình đầy đủ + nhật ký: `.claude/skills/ve-hinh-cau-hoi/SKILL.md`.

**Đã xong (nhánh claude/visual-illustrations-questions-dcd5bd, đã vào main 2026-10-29):**
- 57 hình L10 Động lực học ghi vào `question_bank` + đề đang dùng; `scripts/kiem-hinh-da-ghi.mts hinh-cau-hoi` → 57/57, sai số hình 0.
- #339825 từng bị 2 hình, đã khôi phục (`scripts/logs/khoi-phuc-339825.sql`, không commit). Chưa kiểm riêng bản sao trong `exams`.
- Nguồn vẽ: `scripts/data/hinh-cau-hoi/` (ve-mau.py, ve-so-do.py, ve-do-thi.mts, quyet-dinh.json).

**2026-10-29 chiều:** hình cạnh đề (ContentHtml.withFigureBeside, commit 7ddc18fb9, chưa push/deploy); 10 hình Opus vẽ (subagent) cho câu hệ vật/ròng rọc đã ghi 10/10 (scripts/data/hinh-cau-hoi/opus/). 5 câu 'như hình vẽ': tìm mạng không có nguồn mở → chưa vẽ, chờ thầy quyết ẩn hay giữ. Tìm hình trên mạng cho câu kiểu hệ vật không ra gì — vẽ thẳng.

**Còn chờ:**
- Hình đang nằm DƯỚI đề, thầy muốn "kế bên" → cần đổi UI hiển thị câu hỏi (theo `docs/QUY-TAC-THIET-KE.md`, chụp 375px); chưa làm.
- 109 câu hệ vật nối dây + 14 câu ròng rọc (mơ hồ) chưa vẽ; 5 câu "như hình vẽ" thiếu hình cần đề gốc.
- Chưa mở thử câu trên web (KaTeX + hình); chưa tìm ảnh thật nguồn mở (nhảy dù, phanh gấp…).
- Mở rộng L10 chương khác, L11, L12 chưa bắt đầu (script quét hiện chỉ lọc lớp 10).

**Quyết định chốt:** không vẽ phản lực/thành phần lực (lộ đáp án); chỉ ghi nhãn số liệu đề đã cho; ghi DB giờ học rất chậm (~2 phút/câu) nên báo thầy trước.
