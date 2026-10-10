---
name: xu-ly-bao-loi
description: Kiểm tra mục Báo lỗi & góp ý (bảng bug_reports, trang /quan-tri/bao-loi) — đọc, phân loại, lập danh sách việc cụ thể, giao đúng agent rẻ nhất làm được, sửa lỗi, đối chiếu rồi đóng báo. Dùng khi thầy nói "kiểm tra báo lỗi", "xử lý góp ý", "học sinh báo lỗi gì", "sửa các lỗi được báo".
---

# Xử lý báo lỗi & góp ý — đọc rẻ, giao đúng người, sửa, đóng

Nguyên tắc tiết kiệm token: **phiên chính chỉ điều phối + sửa việc cần phán đoán**; đọc/kiểm/tự giải giao agent; không đọc ảnh chụp ở phiên chính; không đọc cả file lớn (grep + đọc đoạn).

## B1. Đọc (script, 0 token suy luận) — chạy trên Mac, tab terminal
```
cd /Users/MAC/Projects/thachlab && npx tsx .claude/skills/xu-ly-bao-loi/scripts/doc-bao-loi.mts --json
```
(mặc định chỉ status=moi; `--status dang_xu_ly|all`). Script chỉ ĐỌC, in danh sách đã nhóm A–F kèm agent gợi ý, và ghi `scripts/logs/bao-loi-<ngày>.json`.
Cloud không có service_role → in lệnh cho thầy chạy, đừng giả vờ.

## B2. Lập danh sách việc (phiên chính, ngắn)
Đọc kết quả B1, **gộp báo trùng** (cùng trang/cùng câu), loại spam/không tái hiện được. Ghi bảng:
`# | nhóm | trang/đề-câu | triệu chứng 1 dòng | nguyên nhân giả định | agent | trạng thái`
Báo có ảnh 📷: giao agent đọc ảnh (xem bảng), phiên chính không mở ảnh. Ảnh nằm ở bucket `bug-report-screenshots`.

## B3. Phân công — mỗi việc một agent, đúng sức
| Nhóm | Việc | Agent (model) | Ghi chú tiết kiệm |
|---|---|---|---|
| A. Câu đề sai (`cau_hoi`, có exam_id) | Tự giải độc lập câu bị báo, đối chiếu đáp án đang lưu, kết luận ĐÚNG/SAI/MƠ HỒ | `kiem-code` (sonnet) | Giao theo lô ≤10 câu/agent; chỉ đưa đề-câu + mô tả, không đưa cả đề |
| A (sửa) | Sửa câu đã kết luận SAI | phiên chính, qua `/quan-tri/sua-de?exam=&q=` hoặc PATCH REST (xem memory `feedback_lesson_item_edit_via_rest`) | Không đăng lại cả đề |
| B. Nội dung bài học sai | Soát công thức/đơn vị/số liệu của đoạn bị báo | `kiem-code` | Đưa đúng đoạn HTML, không đưa cả bài |
| B (sửa) | Sửa `theory.src.html` → build → `scripts/cap-nhat-ly-thuyet.sh` | phiên chính theo skill `soan-bai-ly-thuyet-tuong-tac` | Chỉ ghi mục lý thuyết |
| C. Giao diện/code | Tái hiện + sửa component | agent `claude` (hoặc phiên chính nếu nhỏ); sau đó `kiem-code` soát diff theo QUY-TAC-THIET-KE | Mỗi agent một file/cụm file riêng, không chồng lên nhau; chụp 375px |
| D. Điểm/rank/đăng nhập/RLS | Chỉ ĐỌC dữ liệu để tìm nguyên nhân | `kien-truc-du-lieu` (opus) | Chỉ gọi khi thật sự đụng schema/RLS; sửa DB = file migration, **không tự chạy** |
| E. Đề xuất tính năng | Không sửa | — | Gom thành 1 danh sách hỏi thầy |
| F. Chưa rõ | Hỏi lại người báo (qua `admin_note`) | phiên chính | Đừng đoán |
Việc ngoài khả năng Claude (OCR đề nhiều hình, sinh lời giải hàng loạt) → dừng, in hướng dẫn Cursor theo AGENTS.md "Phân công mô hình". Dữ liệu định danh học sinh không đưa ra ngoài Claude.
Các việc độc lập thì **gọi agent song song trong một lượt**. Brief mỗi agent: mục tiêu, đường dẫn/ID cụ thể, "không sửa file ngoài phạm vi", dạng trả về (bảng ngắn).

## B4. Sửa
- Tuân theo AGENTS.md: commit theo đường dẫn cụ thể, không `git add .`; migration chỉ viết file, thầy chạy; sửa lý thuyết chỉ đẩy mục Lý thuyết.
- Lỗi nội dung đã đăng: sửa xong ghi vào `admin_note` đã sửa gì.

## B5. Đối chiếu & đóng báo
- Mỗi mục: `kiem-code` (hoặc tự kiểm với diff nhỏ) xác nhận đã hết lỗi; UI thì xem 375px.
- Đóng báo: trang `/quan-tri/bao-loi` đổi sang "Đã xử lý" + ghi `admin_note` (hoặc đưa thầy danh sách `#id` để đóng). Agent không tự xoá báo.
- Báo cuối cho thầy MỘT lần: bảng `# | đã làm gì | file | còn treo`, kèm các mục E chờ quyết định và mục F chờ hỏi lại.

## Nhật ký rút kinh nghiệm
- 2026-10-10 · tạo skill; chưa chạy thật vòng nào → sau vòng đầu, sửa quy tắc phân nhóm trong `doc-bao-loi.mts` (hàm `route`) cho khớp báo thật.
