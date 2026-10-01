---
name: project_thachlab_title_grade_roadmap
description: "Tab 'Theo lớp' ở trang Rank — gợi ý huy hiệu chuyên môn nên nhắm theo Lớp 10/11/12, dùng huy hiệu đã có sẵn (không vẽ ảnh mới); đã deploy 28/9/2026"
metadata:
  node_type: memory
  type: project
  originSessionId: a81af6f0-bbef-410b-95ee-543b61a769a2
  modified: 2026-09-28T16:18:19.190Z
---

28/9/2026 thầy yêu cầu "bộ huy hiệu cần sưu tầm cho mỗi lớp 10/11/12 dựa trên kiến thức cần đạt" — làm rõ lại: KHÔNG
phải huy hiệu mới, mà là **bảng gợi ý** dùng 28 danh hiệu chuyên môn đã có sẵn (trong 30 danh hiệu `kind=specialist`,
trừ 2 cái thuần KHTN9), nhóm lại theo lớp — giống một bước xây lộ trình học cho học sinh.

**Đã làm (commit 03f6b735 + merge 7fd5aa33, đã push origin/main + deploy 22e4ceb):**
- `features/rank/title-grades.ts`: config **tĩnh** `SPECIALIST_TITLE_GRADES` map code→lớp, suy từ
  `question_topics.grade` qua `rank_title_topics` (tra bằng `supabase db query --linked` read-only, không migration).
  Lớp 10: 7 danh hiệu (Cơ học). Lớp 11: 9 (Dao động&Sóng + nửa đầu Điện từ). Lớp 12: 13 (nửa sau Điện từ + Nhiệt +
  Hiện đại; "Chúa Tể Của Những Loại Sóng" xuất hiện cả 11 và 12). Cố định tĩnh (không thêm RPC/round-trip Supabase)
  vì ánh xạ chủ đề→lớp theo chương trình, hiếm đổi.
- `components/rank/TitleGradeRoadmap.tsx`: card gọn (không nút đeo), nhóm theo `GRADE_LABELS`, tái dùng
  `titleBadgeSrc`/`titleBadgeLockedSrc` có sẵn.
- `components/rank/RankPage.tsx`: thêm toggle "Theo chủ đề" / "Theo lớp" cạnh `TitleCollection` trong section
  "Bộ sưu tập danh hiệu".

**Sự cố merge khi push (đã xử lý an toàn):** lúc push, origin/main đã có 2 commit mới của phiên khác (e235cb80 đổi
tên 7 bậc rank sang "Liên Quân Mobile", 70a07fa5 fix mobile ngân hàng câu hỏi) — không đụng vùng code của em nên
merge tự động sạch. Deploy lần đầu (03f6b735, trước khi merge) bị thiếu 2 commit đó — kiểm tra giờ commit so với
deploy trước (853948d9, 13:45 — trước cả 2 commit kia) xác nhận KHÔNG regress gì, rồi build+deploy lại lần 2 từ
commit đã merge (7fd5aa33) để đưa đủ mọi thứ lên. Dùng worktree tạm (`git worktree add --detach`) để merge, không
đụng WIP nửa vời trong working tree chính — xem [[feedback_thachlab_deploy_scope]].

**Còn treo:** chưa test UI thật bằng tài khoản HS (chỉ xác nhận build/tsc/eslint sạch + trang login-gate render
đúng, không crash). Local `main` branch trong working tree chính vẫn đứng ở 03f6b735 (sau origin 1 commit) — cố ý
không fast-forward vì sẽ đụng WIP uncommitted của phiên khác trên `docs/STATE.md`/`scripts/run-migrations.sh`;
lần fetch/pull sau sẽ tự merge sạch (không mất gì, chỉ là local ref tạm lùi).
