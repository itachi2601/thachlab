---
name: project-thachlab-mixed-worked-examples-audit
description: "Lỗi 'Dạng N: Bài tập' bị lẫn vào lý thuyết (kiểu Bài 6) — khảo sát xong, đã sửa cả 2 bài còn lại (83, 131) 25/9/2026; KHÔNG phải lỗi hệ thống ~118 bài; script khảo sát ở docs/supabase-audit-mixed-worked-examples-in-theory.sql"
metadata:
  node_type: memory
  type: project
  originSessionId: 0a0a340b-27fd-41ee-8110-02ec3ec17320
  modified: 2026-09-25T15:07:53.644Z
---

**Cập nhật 25/9/2026: đã sửa xong cả 2 bài — script khảo sát chạy lại ra 0 kết quả.** Cách sửa:
viết script Node (một lần, không lưu vào repo — chỉ scratch) tách `body_html` tại đúng heading
`<h3>Dạng 1. Bài tập lý thuyết...</h3>`, cắt theo từng `<strong>Câu N.</strong>` thành các object
`{label: "Câu N", body_html}` riêng lẻ (giống định dạng thật của bài 6, KHÔNG gộp chung một "Dạng"
thành 1 blob), rồi ghép vào ĐẦU mảng `questions` hiện có của mục bai_tap_mau (giữ nguyên các phần
tử "Dạng 2"/"Dạng 3" cũ, chỉ label kiểu khác — chấp nhận mảng có granularity không đồng nhất vì
component `WorkedQuestionsGrid` render chung, không phân biệt). Chạy UPDATE qua
`supabase db query --linked` với dollar-quoting (tránh escape thủ công chuỗi HTML/LaTeX lớn),
bọc `begin;...commit;`, test bằng `rollback;` trước. Kết quả: item 274/271 (lý thuyết) mất hẳn
phần "Dạng 1" kẹt lại; item 275 có 12 questions (Câu 1-11 + Dạng 2 cũ), item 272 có 4 questions
(Câu 1-2 + Dạng 2 + Dạng 3 cũ). Không cần deploy code (chỉ sửa data Supabase, giống lần sửa bài 84).

25/9/2026: sau khi sửa tay lesson_id=84 (Bài 6. Phản xạ toàn phần — nội dung "Dạng 1: Bài tập lý
thuyết" kèm các "Câu N. ... Hướng dẫn giải" bị kẹt trong `lesson_items.body_html` của mục
`ly_thuyet` thay vì nằm trong `questions` jsonb của mục `bai_tap_mau` cùng bài), đã chạy khảo sát
toàn bộ `lesson_items(kind='ly_thuyet')` để tìm lỗi tương tự — xem [[project-thachlab-lesson-sections]].

**Kết quả: KHÔNG phải lỗi hệ thống lặp lại ở ~118 bài như nghi ban đầu — chỉ tìm thêm đúng 2 bài:**
- lesson_id=83 (Bài 5. Khúc xạ ánh sáng) — theory item id=274 còn kẹt "Dạng 1" (~24 câu tổng,
  đoạn kẹt ~17 916 ký tự); mục bai_tap_mau id=275 đã có "Dạng 2" (Câu 12-18) nhưng thiếu Dạng 1.
- lesson_id=131 (Bài 4. Công và công suất) — theory item id=271 còn kẹt "Dạng 1" (Câu 1-2, đoạn
  kẹt ~1 709 ký tự); mục bai_tap_mau id=272 đã có Dạng 2 (Câu 3-17) + Dạng 3 (Câu 18-34) nhưng
  thiếu Dạng 1.

Dấu hiệu chung: mục bai_tap_mau **không rỗng** (đã có 1-2 phần tử questions) — chỉ đúng Dạng 1 bị
bỏ sót khi tách dữ liệu gốc, không phải "để trống hoàn toàn" như ban đầu đoán. Kiểm tra "questions
rỗng" một mình KHÔNG đủ để bắt lỗi này.

**Đã loại trừ (không phải lỗi, chỉ trùng từ khóa "Hướng dẫn giải" nhiều lần):**
- lesson_id=63 (Bài 18. Lực ma sát): 15 "Ví dụ N" SGK minh hoạ xen kẽ suốt lý thuyết theo từng
  mục — thiết kế có chủ đích, không phải "Dạng N: Bài tập" bị lẫn.
- lesson_id=129, 130 (Động năng—Thế năng, Cơ năng): heading "Dạng 1: Câu hỏi lý thuyết" nhưng câu
  hỏi KHÔNG đánh số "Câu N." (chỉ là câu hỏi thảo luận ngắn) — khác hẳn "Dạng N: Bài tập" có đánh
  số của lỗi thật; có vẻ là loại nội dung cố ý khác (câu hỏi ôn khái niệm), không di chuyển.
- lesson_id=73 (Bài 28. Động lượng): có "RÈN LUYỆN LÍ THUYẾT" (Câu 1:, Câu 2: — dùng dấu `:` chứ
  không phải `.` nên không khớp mẫu lỗi) + đoạn cuối body_html có tiêu đề mồ côi
  `<strong>BÀI TẬP MẪU PHÂN DẠNG</strong>` không kèm nội dung gì theo sau (rác cosmetic từ lúc
  nhập bài, không mất dữ liệu) — có thể dọn sau nhưng ưu tiên thấp, khác mức độ với lỗi thật.

**Script khảo sát (chỉ đọc, đã lưu lại để dùng cho lần sửa hàng loạt sau):**
[docs/supabase-audit-mixed-worked-examples-in-theory.sql](../../../../Projects/thachlab/docs/supabase-audit-mixed-worked-examples-in-theory.sql)
— chạy bằng `supabase db query --linked -f docs/supabase-audit-mixed-worked-examples-in-theory.sql`
(xem [[reference-supabase-db-query-cli]]). Logic cốt lõi: lấy các số "Dạng N" xuất hiện trong
body_html lý thuyết, so với các số "Dạng N" đã có trong label của questions[] ở mục bai_tap_mau
cùng lesson_id — Dạng nào có trong lý thuyết mà thiếu trong bai_tap_mau là nghi vấn mạnh.

**Why:** thầy lo lỗi lặp lại ở nhiều bài (~118 bài THPT), cần biết quy mô thật trước khi quyết định
có viết script tự động sửa hàng loạt hay không — kết quả là quy mô nhỏ (chỉ 2 bài) nên đã sửa tay
luôn trong phiên tiếp theo, không cần script tự động hoá hàng loạt (xem cập nhật 25/9/2026 ở đầu).
**How to apply:** nếu sau này phát hiện thêm bài tương tự, chạy lại
`docs/supabase-audit-mixed-worked-examples-in-theory.sql` trước để xác nhận đúng là "Dạng N thiếu
trong bai_tap_mau" (không phải chỉ trùng từ khóa như 4 bài đã loại trừ ở trên), rồi lặp lại đúng
quy trình đã dùng cho 83/131 ở phần đầu file này. Việc dọn cosmetic ở lesson_id=73 (tiêu đề mồ côi
"BÀI TẬP MẪU PHÂN DẠNG") vẫn còn treo, ưu tiên thấp, thầy chưa yêu cầu.
