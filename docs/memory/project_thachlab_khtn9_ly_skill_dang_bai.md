---
name: project_thachlab_khtn9_ly_skill_dang_bai
description: "Dùng skill dang-bai-hoc-thachlab để đăng phần Vật lí trong môn KHTN lớp 9 lên LMS — mới bắt đầu, chưa làm gì thực chất."
metadata:
  node_type: memory
  type: project
  originSessionId: b870550a-d2a0-448b-b869-ab7525857bae
  modified: 2026-09-24T07:13:30.296Z
---

Yêu cầu 2026-09-24: "Skill đăng bài cho phần vật lý trong môn KHTN lớp 9". Phiên bị ngắt (`/ban-giao`) ngay sau bước tra cứu ban đầu — **chưa hỏi thầy cụ thể muốn đăng chương/bài nào**, chưa mở file nguồn, chưa dựng bundle nào.

## Đã tra được (chỉ tra cứu, chưa xử lý nội dung)

- **class_id = 15** = "KHTN 9" trong bảng `classes` (khác lớp 10=16, 11=17, 12=18).
- Chapters đã có sẵn gắn với class_id=15 (`chapter_classes`), tất cả `subject_code="vat-ly"`:
  - id=22 "Mở đầu" (sort_order=1)
  - id=23 "Chương 1: Năng lượng cơ học" (sort_order=2)
  - id=18 "Chương 2: Ánh sáng" (sort_order=17)
  - id=19 "Chương 3: Điện" (sort_order=18)
  - id=20 "Chương 4: Điện từ" (sort_order=19)
  - id=21 "Chương 5: Năng lượng với cuộc sống" (sort_order=20)
  - Khoảng trống sort_order 3-16 là các môn KHTN khác (Hóa/Sinh) dùng chung bảng `chapters`/`classes`, không phải chương Vật lí còn thiếu.
  - **Chưa tra `lessons` dưới các chapter này** — chưa biết đã có sẵn bao nhiêu bài/tên bài, hay phải tạo mới.
- Nguồn khả dĩ (chưa mở xem nội dung bên trong):
  - `/Users/MAC/Documents/THPT/Lop09/00_Dung_chung/TÀI LIỆU DẠY THÊM KHTN 9 PHẦN VẬT LÍ KNTT2025 WORD` (thư mục, chưa liệt kê file con)
  - `~/Downloads/YEU_CAU_CAN_DAT_MON_KHTN_42a89.pdf` và `...-2.pdf` — có thể là YCCĐ gốc Bộ GD cho môn KHTN (dùng để tra tên YCCĐ gắn `topic`, giống cách đã làm ở [[project_thachlab_lesson_description]] "2 bài KHTN9 đã có YCCĐ").

## Việc cần làm khi tiếp tục

1. Hỏi thầy: đăng **chương/bài nào** trong 5 chương trên (hay toàn bộ), và nguồn chính xác là thư mục "TÀI LIỆU DẠY THÊM..." hay file khác.
2. Liệt kê nội dung thư mục nguồn, xem cấu trúc file (giống mẫu "Chủ đề N - GV.docx" như lớp 10 HK2 hay khác).
3. Tra `lessons` hiện có dưới chapter_id 22/23/18/19/20/21 để biết ánh xạ file→bài (như đã làm ở [[project_thachlab_hk2_lop10_4chuong]]).
4. Theo đúng quy trình đã dùng cho lớp 10 HK2: `mathtype-sang-omml` → `latex` → tự dựng `exam.questions[]` → `dang-bai-hoc-thachlab` (bundle JSON) → `validateBundle` → lưu JSON, KHÔNG tự chạy `upload-lesson.mts` (cần thầy gõ service-role key ở Terminal riêng).
