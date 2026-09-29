---
name: project_thachlab_sua_de_admin
description: "Trang admin THPT \"Sửa đề đã đăng\" — xem/sửa đề có sẵn trong exams, tái dùng ExamSection"
metadata:
  node_type: memory
  type: project
  originSessionId: 96a0c2c0-78d9-4ccd-8138-4f5dba03c54a
  modified: 2026-09-25T15:06:04.969Z
---

Trang `/quan-tri/sua-de` (component `ExamLibraryAdmin.tsx`) cho phép tìm một đề đã có trong bảng
`exams` (theo tên/mã, lọc nháp/xuất bản) rồi sửa trực tiếp nội dung/đáp án/lời giải/nhãn
Chủ đề-Dạng từng câu, tiêu đề, thời lượng, điểm đạt, xuất bản — lưu đè lên đúng id nên mọi
`lesson_items` đã gắn đề không cần đổi gì. Test đầy đủ (chọn đề, sửa, lưu, tải lại xác nhận) đã chạy
trên **localhost** qua Browser pane, đề #200 (có ảnh) — không phải trên web thật.

**Deploy thật 25/9/2026 ~22:04 (giờ VN)**: đã chạy `bash scripts/deploy.sh` (build export tĩnh + force-push
nhánh `deploy` — xem [[project_thachlab_hosting]], site KHÔNG tự deploy khi `git push` main, phải chạy
script này). Xác nhận qua `curl`: `/quan-tri/sua-de` trả 200 (301 chỉ là redirect thêm `/`), nội dung có
đúng chữ "Sửa đề đã đăng"; trang chủ rebuild lúc 15:00:07 GMT. Mở thử trên **web thật** (không phải
localhost) qua Browser pane: danh sách 179 đề tải đúng — **nhưng phiên bị ngắt ngay sau đó, CHƯA kịp
bấm vào một đề để test sửa+lưu trên web thật**. Việc còn treo: mở lại `/quan-tri/sua-de` trên web thật,
chọn một đề, sửa thử rồi Lưu, xác nhận không lỗi (nhất là đề có ảnh, vì bug validateBundle bên dưới chỉ
mới test kỹ ở localhost).

Kỹ thuật: không viết trình soạn câu hỏi mới — tái dùng `ExamSection`/`ExamDraftEditor` (khối "sửa
chi tiết từng câu" vốn dùng chung cho [[project_thachlab_dang_de_azota]] và Nhập bài) qua
`externalSeed` để nạp sẵn đề, cộng prop mới `hideRawText` (ẩn khối dán/thả đề — không có văn bản
gốc để "Quay lại văn bản").

**Bug đã sửa nhân tiện**: `validateBundle` (services/lesson-import.ts) có bước dò "placeholder ảnh
chưa khai báo" bằng regex `\bmedia\/...` — khớp nhầm cả URL ảnh đã tải lên thật, vì bucket Supstorage
tên `lesson-media` chứa chuỗi con `media/...`. Lỗi này ẩn từ trước vì luồng đăng đề cũ chỉ validate
TRƯỚC khi ảnh có URL thật; chỉ lộ ra khi trang sửa-đề mới validate lại đề đã publish. Đã thêm
`(?<!lesson-)` vào regex. Ảnh hưởng: mọi đề có ảnh, nút Lưu ở trang sửa-đề sẽ luôn bị khoá nếu chưa có
fix này — nếu sau này thấy lỗi giả "Còn placeholder ảnh chưa khai báo" ở nơi khác dùng validateBundle,
nhớ tới nguyên nhân này trước.

25/9/2026: thêm sửa lớp gán (`exam_classes`) ngay tại trang — tái dùng `ClassPicker` (component chip
chọn lớp đã dùng ở Thông báo/Xếp hạng), ghi qua `setItemClasses` cùng lúc với Lưu. Đã test add/remove/
lưu/tải lại trên đề thật (#200), khôi phục đúng trạng thái gốc sau test.
