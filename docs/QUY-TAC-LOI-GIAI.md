# Quy tắc viết lời giải trắc nghiệm trong ngân hàng (chốt 18/10/2026)

Rút từ lần cho "học sinh" làm thử + 3 đợt viết lại 1.130 câu (`scripts/ap-dung-viet-lai.mts`). Prompt gốc cho agent: `scripts/data/giai-lai/viet-lai3/HUONG-DAN.md` (thư mục gitignore, sinh lại được từ file này).

1. Mỗi bước một `<p class="text-base leading-relaxed my-2">`; công thức chữ trước, số sau; có đơn vị; dòng chốt cuối "Chọn X." (trả lời ngắn: "Đáp số: … đơn vị").
2. Mở đầu nêu vì sao chọn công thức/định luật và điều kiện áp dụng (nửa dòng).
3. Trắc nghiệm tính toán: có đoạn "Sai vì …"/"Không đúng vì …" cho ít nhất 2 phương án bẫy. Chỉ nêu LỖI TƯ DUY khi tính thử ra đúng con số đó và là lỗi học sinh thật hay mắc; phương án nhiễu ngẫu nhiên thì "không đúng vì" kèm phép kiểm số. Không bịa lỗi, không bịa hằng số tra cứu.
4. `$\Rightarrow$` chỉ cho bước SUY RA; thay số cùng dòng với công thức; không hai ⇒ trong một `<p>`; câu một phép tính thì không dùng ⇒.
5. Không dòng "Đề hiểu là …" chỉ để nhắc lại ký hiệu; không dấu `\"` trong chuỗi; `<`,`>` trong `$…$` viết `\lt`,`\gt`; `%` trong `$…$` viết `\%`.
6. Quy trình: agent Sonnet viết lại (đáp án phải khớp ngân hàng, lệch thì ghi chú) → **agent đóng vai học sinh làm 16 câu mẫu TRƯỚC khi xem lời giải rồi đối chiếu (tự tính lại số bẫy, số đọc từ hình)** → vá → ghi question_bank (sao lưu, KHÔNG đụng `exams`, tránh trigger đồng bộ đáp án).
7. Đúng–sai (19/10/2026): mỗi ý a), b), c), d) MỘT `<p>` riêng, mở đầu bằng "a) Đúng." / "a) Sai." rồi lý do (công thức chữ trước số sau, có đơn vị). Ý Sai nêu giá trị/phát biểu đúng thay thế ("… chứ không phải …"). Không `<br>`, không ⇒ trong cùng `<p>` với kết luận Đúng/Sai.
8. Trả lời ngắn: các bước như mục 1, mở đầu nêu định luật + điều kiện, dòng cuối "Đáp số: … đơn vị" đúng định dạng đáp án (dấu phẩy thập phân kiểu Việt, làm tròn theo đề).
9. Chuẩn hoá HÌNH THỨC tự động (không agent): `scripts/chuan-hoa-loi-giai.mts [--apply]` bọc mỗi dòng `<br>` thành `<p class="text-base leading-relaxed my-2">` và thêm "Chọn X." theo đáp án DB nếu lời giải chưa nêu; chỉ ghi `question_bank`, sao lưu `scripts/logs/chuan-hoa-loi-giai-backup-*.json`. Bỏ qua lời giải có bảng/ảnh/danh sách/`<p>` kiểu khác.
