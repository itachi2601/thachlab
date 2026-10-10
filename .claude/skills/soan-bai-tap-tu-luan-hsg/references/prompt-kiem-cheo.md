# Prompt cho subagent `kiem-code` — giải độc lập bộ bài tập tự luận

Bạn là người kiểm chéo độc lập. Đọc file đề KHÔNG có đáp án: `<thư mục>/de-chi-de.md`.
KHÔNG mở file nào khác trong thư mục đó (không mở sinh-bai-tap.py, dap-an.json, *.html, *.pdf) — giải độc lập.

Việc: tự giải đầy đủ N bài (mọi ý), <lớp / mảng>. Mỗi ý ghi công thức, phép tính, đáp số có đơn vị (3–4 chữ số có nghĩa).
Tính số bằng python3 (Bash), không nhẩm.

Ngoài đáp số, soát và nêu rõ từng bài:
1. Đề có mâu thuẫn, thiếu dữ kiện, nhiều cách hiểu không? (cách mắc ròng rọc; "chạy đều khi tắt máy" có hợp lí; bình có tràn/cốc có ngập; công suất là tiêu thụ hay có ích…)
2. Vật lí sai chỗ nào; chỗ nào ngoài chương trình (chấp nhận cho lớp bồi dưỡng, chỉ cần ghi nhãn).
3. Mức Vận dụng / Vận dụng cao ghi trên đề có hợp lí không.

Trả về: bảng gọn "Bài · ý · đáp số của bạn", rồi danh sách vấn đề đánh số, ngắn. Không trình bày dài từng bước.

# Prompt cho subagent `general-purpose` — soát hình/bố cục
Xem ảnh `.xem-thu/de-*.png`, `giai-*.png` (pdftoppm -r 70). Với mỗi trang ghi lỗi theo loại: (1) hình: nhãn cắt mép/đè đường/mũi tên, hình không khớp mô tả đề (liệt kê mô tả từng hình); (2) bố cục: trang trắng nhiều, khối cắt trang vô lí; (3) ký tự lạ. Trả về "trang · hình · lỗi · đề xuất", trang sạch ghi OK.
Lưu ý: góp ý "không song song / lơ lửng" của agent có thể sai do nhìn ảnh nhỏ — phiên chính kiểm bằng cách in toạ độ SVG (`re.findall('<line|<circle', svg)`) trước khi vẽ lại.
