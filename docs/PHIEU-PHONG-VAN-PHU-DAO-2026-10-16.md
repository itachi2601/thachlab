# Phiếu phỏng vấn HS + khảo sát 1 câu — vì sao kênh tự thoát phụ đạo ít được dùng (16/10/2026)

**Hướng kết hợp (thầy chốt 16/10):** (A) 3 buổi phỏng vấn ngắn do **trợ giảng** làm — để lấy ĐÚNG các lựa chọn cho (B) khảo sát 1 câu
trong web, rồi đối chiếu với hành vi thật. Thầy không tự phỏng vấn (em dễ nói điều thầy muốn nghe). Lý do và phản biện: hội thoại 16/10.

Bước **Thấu cảm** của Design Thinking (`docs/thachlab-design-thinking-audit.md`). Vấn đề gốc và chỉ số: `docs/ROADMAP.md`
mục "Vấn đề gốc đã chốt". Mục đích: **hiểu**, không phải thuyết phục em dùng. Phỏng vấn xong mới bàn cách sửa.

## A. Chọn 3 em, trợ giảng phỏng vấn (không ghi tên vào file này)
- 1 em đang "đang mở khoá" (có `tutoring_needs` mở) mà **chưa mở** bài tự kiểm tra 20 câu.
- 1 em đã mở bài tự kiểm tra nhưng bỏ giữa chừng hoặc trượt.
- 1 em đã thoát bằng bài tự kiểm tra (đạt ≥80%) — nói được điều gì khiến làm đến cùng.
Khác lớp nếu được. Trợ giảng do thầy chọn, hỏi riêng từng em; thầy không có mặt. Ghi mỗi em bằng mã `E1..E3`, không lưu tên/SĐT ở đây (dữ liệu định danh chỉ đi qua Claude, không gửi model ngoài).

## Cách hỏi (≈10 phút/em, hỏi riêng, không có bạn cùng lớp bên cạnh)
- Mở đầu: "Thầy đang sửa web cho dễ học hơn. Em nói thật, em nói chê cũng được, không bị trừ điểm gì."
- Hỏi mở, để em kể; không gợi đáp án; không nói "phụ đạo" nếu em nói "mở khoá" thì dùng đúng từ của em.
- Ghi **nguyên văn câu em nói**, không diễn giải. Hỏi "vì sao?" tối đa 2 lần mỗi ý.
- Không hứa sẽ sửa; chỉ cảm ơn.

## Câu hỏi
1. Lần gần nhất em thấy chủ đề bị gắn "đang mở khoá" trên web, em nghĩ gì, cảm thấy gì? (nhớ lại tình huống cụ thể)
2. Em hiểu "đang mở khoá" nghĩa là gì? Em nghĩ web muốn em làm gì tiếp theo?
3. Sau đó em làm gì? (làm gì / không làm gì / đi hỏi ai)
4. Em có biết có bài tự kiểm tra 20 câu để thoát không? Biết từ đâu? Em thấy nó ở chỗ nào?
5. (Em chưa mở) Điều gì khiến em chưa bấm vào? Nếu nói thật lòng thì lý do chính là gì?
6. (Em đã mở nhưng bỏ/trượt) Lúc bỏ/trượt em đang ở câu nào, đang nghĩ gì? Ngay sau đó em làm gì?
7. (Em đã thoát) Điều gì khiến em làm đến cùng? Lúc thoát em thấy gì?
8. Nếu phải ôn trước khi làm bài tự kiểm tra, em muốn ôn bằng cách nào? Em đọc lại lý thuyết chỗ nào, bằng gì?
9. 20 câu 1 lượt: dài, vừa hay ngắn? Làm lúc nào trong ngày/ở đâu (điện thoại hay máy tính)?
10. Em có ngại bạn hoặc thầy cô thấy mình trong danh sách này không? Cái gì khiến em thấy dễ chịu hơn?
11. Nếu em có cây đũa thần sửa đúng một thứ ở phần này của web, em sửa gì?

## Bảng ghi (mỗi em một hàng; điền nguyên văn)
| Em | Nhóm | Hiểu "mở khoá" thế nào | Biết có bài tự kiểm tra? | Rào cản (nguyên văn) | Điều muốn thay đổi |
|---|---|---|---|---|---|
| E1 | chưa mở | | | | |
| E2 | bỏ/trượt | | | | |
| E3 | thoát bằng tự kiểm tra | | | | |

## Sau khi xong (bước Define → Ideate)
- Gom các câu nguyên văn thành nhóm rào cản (không biết / không hiểu nghĩa / ngại nhãn / quá dài / không biết ôn gì / khác).
- Nhóm nào ≥3/5 em thì mới đáng sửa. Viết lại một câu "Điểm nhìn" (HMW) vào ROADMAP trước khi đề xuất giải pháp.
- Chưa đổi giao diện trước khi có bảng này và trước 25/10 (GĐ 1: không thêm lớp động lực mới).

## B. Khảo sát 1 câu trong web (làm SAU khi có bảng A; chưa sửa code)
Lựa chọn của câu hỏi lấy từ bảng A, không đoán. Quy tắc (phản biện 16/10: ngắt giữa chừng làm hỏng thứ đang đo; nhóm bỏ ngang ít trả lời nhất):
- **Ai thấy**: chỉ em đang "đang mở khoá" mà chưa mở bài tự kiểm tra; **tối đa 1 lần/tuần/em**; không hiện nếu em đã bấm Bỏ qua 2 lần.
- **Khi nào**: ở điểm ngắt tự nhiên — ngay sau khi nộp xong một bài, hoặc lần mở trang chủ kế tiếp. **Không** hiện lúc đang làm bài hay đọc lý thuyết (tải nhận thức, N/C trong `docs/QUY-TAC-THIET-KE.md`).
- **Hỏi gì**: 1 câu, bấm 1 lần: "Vì sao chưa làm bài tự kiểm tra?" + 4–5 lựa chọn từ bảng A + "Khác (gõ)" + nút "Bỏ qua" rõ, đích chạm ≥44px, đọc được ở 375px.
- **Lưu**: bảng mới nhỏ (mã HS, lý do, thời điểm), RLS chỉ HS tự ghi, GV/TA đọc gộp; retention ngắn; không gửi ra model ngoài. Migration chỉ viết file, chạy theo `run-migrations.sh`.
- **Đối chiếu**: so câu trả lời với hành vi thật (mở bài lúc nào, dừng ở câu nào) — dùng `learning_events` DT-01 khi có; câu trả lời chỉ là giả thuyết.
- **Cắt lỗ**: tỉ lệ bấm Bỏ qua >60% hoặc số HS than phiền → gỡ ngay.
