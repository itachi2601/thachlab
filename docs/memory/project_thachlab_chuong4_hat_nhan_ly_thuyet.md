---
name: project-thachlab-chuong4-hat-nhan-ly-thuyet
description: "Sửa lý thuyết Chương 4: Vật lí hạt nhân lớp 12 (Bài 14-18) từ file GV mới — đã xong và deploy nội dung lên Supabase 2026-09-24"
metadata:
  node_type: memory
  type: project
  originSessionId: 5fd28a5e-fc5a-4962-a7d3-32de57ee237e
  modified: 2026-09-24T02:20:27.138Z
---

**Mục tiêu:** thay toàn bộ mục "Lý thuyết trọng tâm" (`lesson_items.kind=ly_thuyet`) của 5 bài
Chương 4 lớp 12 (chapter id 5, "Chương 4: Vật lí hạt nhân") bằng nội dung soạn từ file GV
`"/Users/MAC/Documents/THPT/số hoá THPT/Vật Lý 12 2024 - bộ 3/lý thuyết  Chuyên đề 4 Vật lý Hạt nhân file GV.docx"`.
Thầy chọn rõ **"Thay toàn bộ 5 bài bằng nội dung file GV mới"** (không phải chỉ sửa lỗi cục bộ) —
xem lịch sử hội thoại 2026-09-24 nếu cần đối chiếu lại quyết định này.

**Lesson/lesson_items liên quan** (chapter_id=5):

| Bài | lesson_id | lesson_items.id (ly_thuyet) | slug ảnh |
|---|---|---|---|
| Bài 14. Hạt nhân và mô hình nguyên tử | 15 | 138 | `12-hat-nhan-mo-hinh-nguyen-tu` |
| Bài 15. Năng lượng liên kết hạt nhân | 16 | 147 | `12-nang-luong-lien-ket-hat-nhan` |
| Bài 16. Phản ứng phân hạch, phản ứng nhiệt hạch và ứng dụng | 17 | 181 | `12-phan-hach-nhiet-hach` |
| Bài 17. Hiện tượng phóng xạ | 18 | 160 | `12-hien-tuong-phong-xa` |
| Bài 18. An toàn phóng xạ | 19 | 150 | `12-an-toan-phong-xa` |

**Đã xong (2026-09-24):** chạy [scripts/update-ly-thuyet-l12-cd4-hat-nhan.mts](../../../../Projects/thachlab/scripts/update-ly-thuyet-l12-cd4-hat-nhan.mts)
(file untracked, chưa commit) — UPDATE trực tiếp `body_html` của 5 dòng trên qua REST (service-role
key thầy tự dán, không qua chat), tải 9 ảnh thật lên bucket `lesson-media`. Đã verify lại bằng GET
anon key: cả 5 `body_html` đều đổi độ dài/nội dung, ảnh (`lesson-media` URL) xuất hiện đúng ở Bài 14
(1 ảnh), 16 (4 ảnh), 18 (4 ảnh); Bài 15, 17 không có ảnh (đúng vì file gốc không có ảnh nội dung ở
2 phần đó).

**Quyết định thiết kế quan trọng (đọc code không tự suy ra được):**
- File GV gốc dùng chung pipeline skill `latex` (docx→LaTeX→HTML), nhưng đây là **một file lý
  thuyết gộp cho cả chương** (chỉ ~390 dòng .tex sau khi trích, không có mốc `\section` rõ ràng
  theo từng Bài) — phải tự đọc nội dung rồi cắt tay theo đúng mô tả yêu cầu cần đạt của từng
  `lessons.description` (đã query DB để lấy) để chia thành 5 file `final.tex` con, KHÔNG dùng
  `split_parts.py` để tách theo bài (nó chỉ tách theo `ly_thuyet/bai_tap_mau/luyen_tap_sach`).
- File gốc có 2 loại rác đã lọc bỏ thủ công trước khi generate HTML:
  1. ~27 ảnh `dNN.png` — banner trang trí hoặc mảnh vỡ đồ họa (số/kí tự rời rạc trùng lặp nội
     dung bảng đã có) — bỏ hết, không dùng.
  2. 2 ảnh là **screenshot nguyên cửa sổ Microsoft Word** (`fig24.png`, `fig25.png` — lộ cả
     ribbon, taskbar) thay vì hình vẽ thật — bỏ hẳn 2 dòng bảng chứa chúng; thông tin (tia lệch
     trong điện trường, đồ thị phân rã N-t) đã có đủ ở dạng bảng/text ngay bên cạnh.
  Khoảng 20 công thức ngắn bị nhúng dạng ảnh mờ trong docx gốc (kí hiệu hạt nhân, khối lượng
  proton/neutron, bán kính hạt nhân, đồng vị, CO₂/CO, ²²³Ra, ¹⁷⁷Lu, ³²P...) đã được gõ lại thành
  LaTeX thay vì giữ nguyên ảnh — xem lại nếu cần đối chiếu số liệu.
- **Không có bản sao nội dung `body_html` CŨ** trước khi UPDATE (script ghi đè trực tiếp, không
  backup). Nếu sau này thầy muốn khôi phục bản trước (nội dung khi đó dài/chi tiết hơn, ví dụ Bài
  16 từng có mục "II. PHẢN ỨNG PHÂN HẠCH HẠT NHÂN" với đồ thị Elkr theo A từ ảnh SGK thật) thì
  phải trông vào Supabase point-in-time recovery (nếu gói dịch vụ có), KHÔNG có trong git.

**Còn treo / chưa làm:**
- Thầy **chưa tự mở web xem trực quan** — mới verify qua REST (nội dung/độ dài/URL ảnh đúng),
  chưa xác nhận hiển thị đẹp trên `/lop-hoc/bai/?id=15,16,17,18,19`.
- 7 file bundle JSON ở gốc repo (`bundle-bai14-chu-de-1.json`, `bundle-bai14-chu-de-2.json`,
  `bundle-bai15-chu-de-3.json`, `bundle-bai15-chu-de-4.json`, `bundle-bai17-chu-de-5.json`,
  `bundle-bai17-chu-de-6.json`, `bundle-bai18-an-toan-phong-xa.json`) là **WIP CŨ, chưa từng
  upload lên Supabase**, và giờ đã bị nội dung mới này vượt qua (không dùng nữa cho Chương 4).
  Chưa hỏi thầy có muốn xoá hay giữ tham khảo — phiên sau không cần dùng lại các file này.
- Phần "phản ứng hạt nhân / định luật bảo toàn" trong nội dung mới khá tối giản (chỉ liệt kê 4
  định luật bảo toàn, không có ví dụ số) so với bản cũ — nếu thầy thấy sơ sài có thể cần bổ sung
  thêm ví dụ tính toán sau.
- Script + dữ liệu trung gian (final.tex, parts/, media/) nằm trong scratchpad phiên
  (`/private/tmp/claude-501/.../scratchpad/l12-cd4-hat-nhan/`) — **sẽ mất khi dọn tmp**; nếu cần
  chạy lại hoặc đối chiếu nội dung đã sinh, phải làm lại từ file GV gốc.

Xem thêm [[project_thachlab_dang_ly_thuyet_only]], [[feedback_lesson_item_edit_via_rest]],
[[project_thachlab_latex_skill]].
