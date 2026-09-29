---
name: project-thachlab-lesson-sections
description: "6 mục bài học thachlab (bài tập mẫu tự chấm, phiên luyện tập, bài tập về nhà) — xong và đã deploy 18/09/2026"
metadata: 
  node_type: memory
  type: project
  originSessionId: 08bc2ed8-9609-4440-ac1f-615db374168e
  modified: 2026-09-19T12:35:45.880Z
---

Bài học trên thachlab được phân loại lại thành 6 mục (`lesson_items.kind`): lý thuyết trọng tâm · video · bài tập mẫu · luyện tập · **bài tập về nhà (mới)** · kiểm tra (giữ nguyên cho bài chính thức + kiểm tra định kỳ).

Thầy đã chốt (18/09/2026): bài tập mẫu gắn ĐỀ để máy chấm được (chọn đáp án → "Kiểm tra" → lời giải); luyện tập đếm ngược TỔNG thời lượng (15″ câu lý thuyết + 45″ câu bài tập, lấy từ nhãn `form` sẵn có); điểm luyện tập lưu ở `practice_sessions`/`practice_question_results` để phân tích lỗ hổng, KHÔNG vào bảng điểm.

Commit 7bb1fa06, migration đã chạy, test trọn vẹn trên bài 20 (gắn đề tạm rồi gỡ), đã deploy 18/09/2026. Phần Phân tích/Cảnh báo phụ đạo ([[project-thachlab-exam-analytics]]) chưa đọc hai bảng practice_* — nối sau. Ngân hàng luyện tập mới chỉ lấy đề trong mục Luyện tập của chính bài đó; câu tự luận bị loại khỏi phiên luyện.

**Why:** mục Luyện tập và Bài tập mẫu chỉ sống được khi thầy gắn đề — hiện hầu hết bài chưa gắn đề nào.
**How to apply:** khi thầy hỏi "sao luyện tập trống", kiểm tra `lesson_items.exam_ids` của mục đó trước.

**Đăng đề vào mục Bài tập về nhà (19/09/2026).** Trang `/quan-tri/nhap-bai` chỉ có hai ô
tick `luyen_tap` / `kiem_tra` — KHÔNG gắn được `bai_tap_ve_nha`. Đường đi: đăng đề qua
nhập bài với ô **Luyện tập + chế độ "Giữ + thêm"** (chế độ mặc định "Thay" sẽ XÓA đề cũ),
rồi sang `/quan-tri/bai-hoc` → Soạn mục → **+ Thêm mục** kind `bai_tap_ve_nha`, chọn đề
bằng ExamPicker, và **Sửa** mục Luyện tập để bỏ chọn đề vừa mượn đường.

Bẫy: mỗi lần nhập bài gắn đề vào một mục, nó **ghi đè `subtitle` của mục đó** theo meta
đề mới ("46 câu (46 TN) — 60 phút"). Gỡ đề ra rồi thì subtitle vẫn còn, học sinh thấy số
câu sai — phải sửa tay subtitle ở `/quan-tri/bai-hoc`.

**Cách gọn hơn (dùng 19/09/2026, đề Bài 13 Điện xoay chiều — xem [[project_thachlab_bai13_dien_xoay_chieu]]):**
không cần tạo mục mới rồi gỡ đề khỏi mục mượn đường. Ở `/quan-tri/nhap-bai` tick tạm
**"Gắn vào Kiểm tra"** (nhớ bỏ tick "Luyện tập" mặc định đang bật sẵn) rồi Đăng — tạo đúng
1 `lesson_items` row kind=`kiem_tra` với `exam_ids=[id]`. Sang `/quan-tri/bai-hoc` → Soạn
mục → **Sửa** đúng mục đó → đổi select loại mục sang **🏠 Bài tập về nhà** (select này set
qua `form_input` ăn bình thường, không cần javascript hack) → đề đã chọn giữ nguyên, subtitle
"43 câu (43 TN) — 60 phút" cũng giữ nguyên vì vẫn là cùng 1 row, không có mục thứ hai nào để
lệch subtitle → sửa tiêu đề mục (ô "Tiêu đề mục") → Lưu mục. Không cần fetch/PATCH tay.
