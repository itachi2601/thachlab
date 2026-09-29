---
name: project-thachlab-dang-ly-thuyet-only
description: Đăng riêng mục lý thuyết phải dùng /quan-tri/bai-hoc (không phải /quan-tri/nhap-bai) — kèm 2 mẹo thao tác
metadata:
  type: project
---

**Đăng chỉ mỗi lý thuyết thì KHÔNG dùng `/quan-tri/nhap-bai`.** Trang nhập bài luôn `insert` một dòng `exams` trước khi ghi lý thuyết, và `canPublish` bắt buộc `exam.questions.length > 0` + tick ít nhất một trong Luyện tập / Kiểm tra → gói chỉ có lý thuyết sẽ bị chặn, hoặc phải bịa đề rác. Đường đúng: `/quan-tri/bai-hoc` → chọn lớp → môn → chương → **Soạn bài** → **Soạn mục** → **+ Thêm mục**, kind `ly_thuyet`, bấm **♯ HTML** rồi dán HTML thẳng vào textarea.

**Why:** skill `dang-bai-hoc-thachlab` chỉ mô tả đường `/quan-tri/nhap-bai`, dễ đi nhầm rồi kẹt.

**How to apply:** yêu cầu "đăng bài … lý thuyết" (không kèm đề) → đi thẳng `/quan-tri/bai-hoc`. Đặt tên mục theo nếp cũ: `Lý thuyết — <tên bài>`.

Hai mẹo thao tác kèm theo (19/09/2026, khi đăng Bài 10 Lực từ · Cảm ứng từ):

- **Browser pane bấm chuột không ăn trên thachlab.id.vn** — `computer left_click` (cả `ref` lẫn toạ độ đúng) không kích hoạt `onClick` của React, dù toạ độ nằm trong `getBoundingClientRect()` của nút. Phải dùng `javascript_tool` gọi `el.click()`. Điền input/textarea thì dùng native setter + `new Event('input',{bubbles:true})` — cách này né luôn bẫy `pbcopy` mojibake ở [[project-thachlab-latex-skill]].
- **Mã QR trong sách giải mã được ngay tại máy**: `pip install opencv-python-headless`, `pdfimages -png` tách ảnh rồi `cv2.QRCodeDetector().detectAndDecode(cv2.resize(img,None,fx=3,fy=3))` → ra link YouTube thật. Trên web nên thay ảnh QR bằng thẻ `<a>` bấm được.

Ảnh bài học vẫn theo nếp `public/lessons/<slug>/media/*.png` + `src="/lessons/<slug>/media/…"`, phải chạy `./scripts/deploy.sh` rồi **chờ ~6–10 phút** cron hosting kéo về mới hết 404. Xem [[feedback-thachlab-deploy-scope]] về việc stash WIP trước khi deploy.
