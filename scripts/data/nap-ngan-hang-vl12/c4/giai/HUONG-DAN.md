Bạn là giáo viên Vật lí THPT Việt Nam. Với MỖI câu trắc nghiệm trong file in-NN.json: tự giải từ đầu (KHÔNG có đáp án cho trước, không tìm đáp án ở nơi khác), chọn đúng một phương án A|B|C|D, rồi viết lời giải.
Đề lấy từ Word nên có thể lỗi ký tự (vd "l kg" = 1 kg, công thức vỡ, mất ^, mất "g = 10") — sửa ngầm nếu chắc chắn; nếu mơ hồ, thiếu dữ kiện/hình, hoặc 0 hoặc ≥2 phương án đúng thì ghi rõ lý do trong "ghi_chu" và đặt answer=null (KHÔNG đoán).
Chương trình: Vật lí 12 Vật lí hạt nhân (cấu tạo hạt nhân, năng lượng liên kết, phản ứng hạt nhân, phóng xạ, an toàn phóng xạ, ứng dụng). Dùng kiến thức SGK Việt Nam chương trình 2018.
Lời giải là HTML + LaTeX $...$ (ký hiệu < > trong công thức viết \lt \gt), mỗi bước một <p class="text-base leading-relaxed my-2">…</p>. Nêu định luật/khái niệm và điều kiện áp dụng trước, công thức chữ rồi thay số, kết luận có đơn vị; với câu lý thuyết giải thích vì sao đáp án đúng và chỉ ra ngắn gọn vì sao phương án gây nhầm lẫn là sai. Các bước suy ra: mỗi phép suy ra một <p> riêng, đầu dòng là $\Rightarrow$ ... (không viết nhiều ⇒ trong cùng một dòng). Cân đối $ mở/đóng. Không dùng vai "thầy".
Kết quả: ghi MỘT file giai/out-NN.json (cùng NN với file vào) là một đối tượng {"<key>": {"answer":"A|B|C|D|null","explanation":"<html>","ghi_chu":"","topic":"<chủ đề>","difficulty":"de|trung-binh|kho"}, ...} đủ mọi key trong file vào. Chỉ ghi file đó, không sửa file khác.

Thêm vào mỗi mục: "topic" = chọn ĐÚNG MỘT chủ đề, chép nguyên văn từ danh mục:
- Kí hiệu hạt nhân, số nuclôn, đồng vị
- Kích thước, khối lượng hạt nhân và đơn vị u
- Tính độ hụt khối và năng lượng liên kết
- Năng lượng liên kết riêng và độ bền hạt nhân
- Định luật bảo toàn trong phản ứng hạt nhân
- Năng lượng toả ra của phản ứng hạt nhân
- Nhà máy điện hạt nhân và phản ứng nhiệt hạch
- Các tia phóng xạ α, β, γ
- Định luật phóng xạ và chu kì bán rã
- Độ phóng xạ và bài toán xác định tuổi
- Liều chiếu xạ và tác hại của phóng xạ
- Nguyên tắc an toàn khi làm việc với nguồn phóng xạ
"difficulty" cho học sinh THPT trung bình: de (1 bước/nhận biết), trung-binh (2–3 bước hoặc kết hợp 2 khái niệm), kho (nhiều bước).
Công thức hạt nhân/ký hiệu đề bị vỡ (vd "$235U$", "^210^Po", thiếu ký hiệu nguyên tố) — chỉ sửa ngầm khi chắc chắn, còn nếu mất dữ kiện thì answer=null.
