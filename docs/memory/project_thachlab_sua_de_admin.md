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

**2026-10-18 — rà dashboard bằng tài khoản admin (đề #975) rồi sửa cả 8 điểm, commit `be0c842e1` trên main, CHƯA deploy** (`bash scripts/deploy.sh`):
- `lib/question-lint.ts`: luật `muMatDau` đòi số mũ KHÔNG bắt đầu bằng 0 — "9·100/300" trong lời giải câu 6 bị bắt nhầm là "9·10 mất ^". Hệ số chữ cái (`a.109`, `x.105`) luật này không bắt, đó là việc của `scripts/sua-so-mu-ngan-hang.mts`.
- `ExamSection.tsx`: khung lỗi hiện thêm đoạn làm luật khớp (`flags[0].ctx`), khỏi phải rê chuột (điện thoại không rê được).
- `ExamLibraryAdmin.tsx`: cuộn tới editor SAU khi đề tải xong (effect theo `full.id`, trước đây cuộn lúc trang còn trống nên không tới); danh sách đề thu thành một dòng "Chọn đề khác" khi đang sửa; bộ lọc lớp (nối `filter_cls:exam_classes!inner`, select ghép chuỗi nên phải ép kiểu `any`); QR/Trợ giảng và "Cài đặt đề" thu gọn trong `<details>`; chip nhảy câu 1…n trong thanh Lưu (đỏ nếu câu có lỗi chặn); thanh Lưu `bottom-20` trên mobile để khỏi đè nút nổi.
- **Quyết định thiết kế**: cảnh báo "thiếu hình" ở trang sửa đề chỉ chặn Lưu với câu MỚI thiếu hình hoặc câu bị sửa phần đề (so theo chuỗi `question` lúc tải); câu thiếu hình có sẵn từ lúc đăng chỉ hiện một dòng ghi chú. Lý do: nhiều đề cũ nhắc "đồ thị" nhưng đã mô tả đủ bằng số liệu (như câu 4 đề #975), ai mở cũng bị đòi tích xác nhận.
- `ExamDraftEditor.tsx`: ô ý/phương án là `AutoText` (textarea tự giãn, Enter bị chặn); nút "Hoàn tác câu này" (snapshot lúc bấm Sửa) vì Cmd+Z không hoàn tác được ô nhập React.
- `app/quan-tri/(chooser)/page.tsx`: thẻ "Việc hay làm" gắn nhãn THPT–THCS/CTTC, thêm lối tắt "Sửa đề đã đăng".
- Đã kiểm trên localhost: lọc lớp 10 → 315 đề, mở #975 tự cuộn tới editor, lint hết báo sai, gõ thử + hoàn tác. KHÔNG bấm Lưu. Chưa chụp riêng 375px (Browser pane bị ẩn nên screenshot hết hạn, kiểm bằng JS/DOM).
- **Còn treo**: (1) deploy; (2) cột `question_bank.lint_flags` còn cờ "mất ^" cũ cho câu dạng `9·100` — chạy lại `scripts/cap-nhat-lint-flags.mts` (ghi DB, chờ thầy duyệt); (3) chụp 375px thật và thử Lưu trên một đề nháp; (4) ý chưa làm: xem trước ngay dưới ô đang gõ (hiện xem trước nằm ngay trên thẻ câu, tách khỏi ô sửa).
- **Bài học hạ tầng**: hai `next dev` (hoặc dev + `next build`) cùng thư mục làm hỏng `.next/dev/cache` ("missing required error components", "Failed to open SST file"). Xử lý: dừng mọi server, `rm -rf .next/dev .next/cache`, chạy lại một server (preview_start `thachlab-dev`). Dashboard cần phiên admin: tab Browser pane lưu phiên riêng (Supabase `jgvbdbpvjdntdgzthumv`); phiên cũ của `itachi2601@gmail.com` thuộc dự án Supabase cũ đã hết hạn, `hs.test1` đăng nhập sẵn thì trang báo "chỉ dành cho quản trị viên".
