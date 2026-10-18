# Quy tắc viết lời giải trắc nghiệm trong ngân hàng (chốt 18/10/2026)

Rút từ lần cho "học sinh" làm thử + 3 đợt viết lại 1.130 câu (`scripts/ap-dung-viet-lai.mts`). Prompt gốc cho agent: `scripts/data/giai-lai/viet-lai3/HUONG-DAN.md` (thư mục gitignore, sinh lại được từ file này).

1. Mỗi bước một `<p class="text-base leading-relaxed my-2">`; công thức chữ trước, số sau; có đơn vị; dòng chốt cuối "Chọn X." (trả lời ngắn: "Đáp số: … đơn vị").
2. Mở đầu nêu vì sao chọn công thức/định luật và điều kiện áp dụng (nửa dòng).
3. Trắc nghiệm tính toán: có đoạn "Sai vì …"/"Không đúng vì …" cho ít nhất 2 phương án bẫy. Chỉ nêu LỖI TƯ DUY khi tính thử ra đúng con số đó và là lỗi học sinh thật hay mắc; phương án nhiễu ngẫu nhiên thì "không đúng vì" kèm phép kiểm số. Không bịa lỗi, không bịa hằng số tra cứu.
4. `$\Rightarrow$` chỉ cho bước SUY RA; thay số cùng dòng với công thức; không hai ⇒ trong một `<p>`; câu một phép tính thì không dùng ⇒.
5. Không dòng "Đề hiểu là …" chỉ để nhắc lại ký hiệu; không dấu `\"` trong chuỗi; `<`,`>` trong `$…$` viết `\lt`,`\gt`; `%` trong `$…$` viết `\%`.
6. Quy trình: agent Sonnet viết lại (đáp án phải khớp ngân hàng, lệch thì ghi chú) → **agent đóng vai học sinh làm 16 câu mẫu TRƯỚC khi xem lời giải rồi đối chiếu (tự tính lại số bẫy, số đọc từ hình)** → vá → ghi question_bank (sao lưu, KHÔNG đụng `exams`, tránh trigger đồng bộ đáp án).
