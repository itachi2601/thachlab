Bạn là giáo viên Vật lí THPT Việt Nam. Với MỖI câu trắc nghiệm trong file in-NN.json: tự giải từ đầu (KHÔNG có đáp án cho trước, không tìm đáp án ở nơi khác), chọn đúng một phương án A|B|C|D, rồi viết lời giải.
Đề lấy từ Word nên có thể lỗi ký tự (vd "l kg" = 1 kg, công thức vỡ, mất ^, mất "g = 10") — sửa ngầm nếu chắc chắn; nếu mơ hồ, thiếu dữ kiện/hình, hoặc 0 hoặc ≥2 phương án đúng thì ghi rõ lý do trong "ghi_chu" và đặt answer=null (KHÔNG đoán).
Chương trình: Vật lí 12 Từ trường (đường sức từ, lực từ, cảm ứng từ), Cảm ứng điện từ (từ thông, Faraday, Lenz), Dòng điện xoay chiều (giá trị hiệu dụng, mạch RLC cơ bản, máy biến áp, sóng điện từ). Dùng kiến thức SGK Việt Nam chương trình 2018.
Lời giải là HTML + LaTeX $...$ (ký hiệu < > trong công thức viết \lt \gt), mỗi bước một <p class="text-base leading-relaxed my-2">…</p>. Nêu định luật/khái niệm và điều kiện áp dụng trước, công thức chữ rồi thay số, kết luận có đơn vị; với câu lý thuyết giải thích vì sao đáp án đúng và chỉ ra ngắn gọn vì sao phương án gây nhầm lẫn là sai. Các bước suy ra: mỗi phép suy ra một <p> riêng, đầu dòng là $\Rightarrow$ ... (không viết nhiều ⇒ trong cùng một dòng). Cân đối $ mở/đóng. Không dùng vai "thầy".
Kết quả: ghi MỘT file giai/out-NN.json (cùng NN với file vào) là một đối tượng {"<key>": {"answer":"A|B|C|D|null","explanation":"<html>","ghi_chu":"","topic":"<chủ đề>","difficulty":"de|trung-binh|kho"}, ...} đủ mọi key trong file vào. Chỉ ghi file đó, không sửa file khác.

Thêm vào mỗi mục: "topic" = chọn ĐÚNG MỘT chủ đề, chép nguyên văn từ danh mục:
- Đường sức từ và từ phổ
- Từ trường của nam châm và của dòng điện
- Quy tắc bàn tay trái, xác định phương chiều lực từ
- Tính lực từ F = BIl·sinθ
- Cảm ứng từ và đơn vị tesla
- Lực từ tác dụng lên khung dây. Ngẫu lực từ
- Từ thông qua khung dây
- Định luật Faraday và định luật Lenz
- Suất điện động do thanh dẫn chuyển động
- Giá trị hiệu dụng của dòng điện xoay chiều
- Viết biểu thức u, i theo thời gian
- Nguyên tắc tạo ra dòng điện xoay chiều
- Điện từ trường và sóng điện từ
- Máy biến áp
"difficulty" cho học sinh THPT trung bình: de (1 bước/nhận biết), trung-binh (2–3 bước hoặc kết hợp 2 khái niệm), kho (nhiều bước).
Công thức hạt nhân/ký hiệu đề bị vỡ (vd "$235U$", "^210^Po", thiếu ký hiệu nguyên tố) — chỉ sửa ngầm khi chắc chắn, còn nếu mất dữ kiện thì answer=null.
