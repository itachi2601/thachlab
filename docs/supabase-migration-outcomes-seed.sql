-- ============================================================
-- Yêu cầu cần đạt (tầng con của question_topics)
-- ============================================================
-- Chạy SAU docs/supabase-migration-topic-outcomes.sql (đã có cột parent_id).
-- Chạy lại nhiều lần được: khớp theo (subject_code, grade, name), chỉ cập nhật
-- parent_id / sort_order — KHÔNG đụng nhãn đã gắn trên câu hỏi.
--
-- Nguồn: mục "Yêu cầu cần đạt" của Chương trình GDPT môn Vật lí 2018 (và KHTN 9),
-- rút gọn thành tên đủ tự mô tả để gắn nhãn câu hỏi. Tên phải DUY NHẤT trong một
-- khối vì câu hỏi lưu nhãn bằng tên (exams.questions[i].topic).
--
-- Đây là bản khởi đầu ~3 YCCĐ mỗi bài, đủ mịn để biết em hổng chỗ nào mà không làm
-- việc gắn nhãn quá nặng. Thầy sửa tên / thêm bớt ở /quan-tri/chu-de.
-- ============================================================

create temporary table tmp_outcomes (
  grade text, parent_name text, name text, idx int
) on commit drop;

insert into tmp_outcomes (grade, parent_name, name, idx) values
  -- ================= KHTN 9 =================
  ('9', 'Động năng. Thế năng', 'Khái niệm động năng và thế năng trọng trường', 1),
  ('9', 'Động năng. Thế năng', 'Tính động năng, thế năng của một vật', 2),
  ('9', 'Cơ năng', 'Sự chuyển hoá động năng – thế năng', 1),
  ('9', 'Cơ năng', 'Bảo toàn cơ năng trong chuyển động rơi, ném', 2),
  ('9', 'Công và công suất', 'Tính công của một lực', 1),
  ('9', 'Công và công suất', 'Tính công suất và ý nghĩa của công suất', 2),
  ('9', 'Khúc xạ ánh sáng', 'Mô tả hiện tượng khúc xạ, vẽ đường truyền tia sáng', 1),
  ('9', 'Khúc xạ ánh sáng', 'Chiết suất và định luật khúc xạ ánh sáng', 2),
  ('9', 'Phản xạ toàn phần', 'Điều kiện xảy ra phản xạ toàn phần', 1),
  ('9', 'Phản xạ toàn phần', 'Tính góc tới hạn, ứng dụng cáp quang', 2),
  ('9', 'Lăng kính', 'Đường truyền tia sáng qua lăng kính', 1),
  ('9', 'Lăng kính', 'Tán sắc ánh sáng qua lăng kính', 2),
  ('9', 'Thấu kính', 'Đặc điểm thấu kính hội tụ, phân kì và tiêu cự', 1),
  ('9', 'Thấu kính', 'Dựng ảnh của vật qua thấu kính', 2),
  ('9', 'Thấu kính', 'Công thức thấu kính và số phóng đại', 3),
  ('9', 'Điện trở. Định luật Ohm', 'Định luật Ohm cho một điện trở', 1),
  ('9', 'Điện trở. Định luật Ohm', 'Điện trở phụ thuộc kích thước và vật liệu dây dẫn', 2),
  ('9', 'Đoạn mạch nối tiếp, song song', 'Điện trở tương đương của đoạn mạch', 1),
  ('9', 'Đoạn mạch nối tiếp, song song', 'Tính U, I trong mạch hỗn hợp', 2),
  ('9', 'Năng lượng và công suất điện', 'Tính điện năng tiêu thụ và tiền điện', 1),
  ('9', 'Năng lượng và công suất điện', 'Công suất điện của dụng cụ và số ghi trên thiết bị', 2),
  ('9', 'Cảm ứng điện từ. Dòng điện xoay chiều', 'Điều kiện xuất hiện dòng điện cảm ứng', 1),
  ('9', 'Cảm ứng điện từ. Dòng điện xoay chiều', 'Nguyên tắc tạo ra dòng điện xoay chiều', 2),
  ('9', 'Tác dụng của dòng điện xoay chiều', 'Các tác dụng nhiệt, quang, từ của dòng xoay chiều', 1),
  ('9', 'Tác dụng của dòng điện xoay chiều', 'An toàn khi dùng điện xoay chiều', 2),
  ('9', 'Năng lượng hoá thạch', 'Vòng năng lượng trên Trái Đất', 1),
  ('9', 'Năng lượng hoá thạch', 'Ưu nhược điểm của nhiên liệu hoá thạch', 2),
  ('9', 'Năng lượng tái tạo', 'Các dạng năng lượng tái tạo và nguồn gốc', 1),
  ('9', 'Năng lượng tái tạo', 'Sử dụng năng lượng tiết kiệm, hiệu quả', 2),

  -- ================= LỚP 10 =================
  ('10', 'Phương pháp nghiên cứu và an toàn thí nghiệm', 'Đối tượng và phương pháp nghiên cứu Vật lí', 1),
  ('10', 'Phương pháp nghiên cứu và an toàn thí nghiệm', 'Quy tắc an toàn trong phòng thực hành', 2),
  ('10', 'Sai số trong phép đo', 'Sai số tuyệt đối, sai số tỉ đối', 1),
  ('10', 'Sai số trong phép đo', 'Ghi kết quả đo và chữ số có nghĩa', 2),
  ('10', 'Độ dịch chuyển, quãng đường, tốc độ, vận tốc', 'Phân biệt quãng đường và độ dịch chuyển', 1),
  ('10', 'Độ dịch chuyển, quãng đường, tốc độ, vận tốc', 'Tốc độ trung bình và vận tốc trung bình', 2),
  ('10', 'Độ dịch chuyển, quãng đường, tốc độ, vận tốc', 'Tổng hợp vận tốc, tính tương đối của chuyển động', 3),
  ('10', 'Đồ thị độ dịch chuyển – thời gian', 'Đọc đồ thị độ dịch chuyển – thời gian', 1),
  ('10', 'Đồ thị độ dịch chuyển – thời gian', 'Tính vận tốc từ độ dốc đồ thị', 2),
  ('10', 'Chuyển động thẳng biến đổi đều. Gia tốc', 'Khái niệm gia tốc và đồ thị vận tốc – thời gian', 1),
  ('10', 'Chuyển động thẳng biến đổi đều. Gia tốc', 'Các công thức của chuyển động thẳng biến đổi đều', 2),
  ('10', 'Chuyển động thẳng biến đổi đều. Gia tốc', 'Bài toán hai xe gặp nhau, phanh gấp', 3),
  ('10', 'Sự rơi tự do', 'Đặc điểm của rơi tự do và gia tốc rơi tự do', 1),
  ('10', 'Sự rơi tự do', 'Tính thời gian, quãng đường, vận tốc khi rơi tự do', 2),
  ('10', 'Chuyển động ném', 'Phân tích chuyển động ném ngang theo hai phương', 1),
  ('10', 'Chuyển động ném', 'Tầm xa, thời gian bay của vật bị ném', 2),
  ('10', 'Tổng hợp và phân tích lực. Cân bằng lực', 'Tổng hợp hai lực đồng quy', 1),
  ('10', 'Tổng hợp và phân tích lực. Cân bằng lực', 'Phân tích lực theo hai phương vuông góc', 2),
  ('10', 'Tổng hợp và phân tích lực. Cân bằng lực', 'Điều kiện cân bằng của chất điểm', 3),
  ('10', 'Ba định luật Newton', 'Định luật 1 Newton và quán tính', 1),
  ('10', 'Ba định luật Newton', 'Định luật 2 Newton — bài toán động lực học', 2),
  ('10', 'Ba định luật Newton', 'Định luật 3 Newton và lực tương tác', 3),
  ('10', 'Trọng lực và lực căng', 'Trọng lực, trọng lượng và trọng tâm', 1),
  ('10', 'Trọng lực và lực căng', 'Lực căng dây — hệ vật nối dây, ròng rọc', 2),
  ('10', 'Lực ma sát, lực cản và lực nâng', 'Lực ma sát nghỉ, ma sát trượt và hệ số ma sát', 1),
  ('10', 'Lực ma sát, lực cản và lực nâng', 'Vật trượt trên mặt phẳng nghiêng có ma sát', 2),
  ('10', 'Lực ma sát, lực cản và lực nâng', 'Lực cản của chất lưu và lực nâng', 3),
  ('10', 'Moment lực. Cân bằng của vật rắn', 'Moment lực và quy tắc moment', 1),
  ('10', 'Moment lực. Cân bằng của vật rắn', 'Ngẫu lực, cân bằng của vật rắn có trục quay', 2),
  ('10', 'Năng lượng. Công cơ học', 'Công của lực và trường hợp lực xiên góc', 1),
  ('10', 'Năng lượng. Công cơ học', 'Định luật bảo toàn và chuyển hoá năng lượng', 2),
  ('10', 'Công suất', 'Tính công suất trung bình và công suất tức thời', 1),
  ('10', 'Công suất', 'Công suất của động cơ, máy kéo', 2),
  ('10', 'Động năng, thế năng', 'Động năng và định lí động năng', 1),
  ('10', 'Động năng, thế năng', 'Thế năng trọng trường và mốc thế năng', 2),
  ('10', 'Cơ năng và định luật bảo toàn cơ năng', 'Bảo toàn cơ năng khi chỉ có trọng lực', 1),
  ('10', 'Cơ năng và định luật bảo toàn cơ năng', 'Biến thiên cơ năng khi có ma sát', 2),
  ('10', 'Hiệu suất', 'Tính hiệu suất của máy và động cơ', 1),
  ('10', 'Hiệu suất', 'Hao phí năng lượng và cách giảm hao phí', 2),
  ('10', 'Động lượng', 'Khái niệm động lượng, xung lượng của lực', 1),
  ('10', 'Động lượng', 'Độ biến thiên động lượng của một vật', 2),
  ('10', 'Bảo toàn động lượng và va chạm', 'Định luật bảo toàn động lượng cho hệ kín', 1),
  ('10', 'Bảo toàn động lượng và va chạm', 'Va chạm mềm, va chạm đàn hồi', 2),
  ('10', 'Động học của chuyển động tròn đều', 'Tốc độ góc, chu kì, tần số', 1),
  ('10', 'Động học của chuyển động tròn đều', 'Liên hệ tốc độ dài và tốc độ góc', 2),
  ('10', 'Lực hướng tâm và gia tốc hướng tâm', 'Tính gia tốc hướng tâm', 1),
  ('10', 'Lực hướng tâm và gia tốc hướng tâm', 'Lực hướng tâm trong các tình huống thực tế', 2),
  ('10', 'Biến dạng của vật rắn. Định luật Hooke', 'Biến dạng kéo, nén và giới hạn đàn hồi', 1),
  ('10', 'Biến dạng của vật rắn. Định luật Hooke', 'Định luật Hooke và lực đàn hồi của lò xo', 2),
  ('10', 'Khối lượng riêng. Áp suất chất lỏng', 'Khối lượng riêng và áp suất chất lỏng theo độ sâu', 1),
  ('10', 'Khối lượng riêng. Áp suất chất lỏng', 'Lực đẩy Archimedes và điều kiện nổi', 2),

  -- ================= LỚP 11 =================
  ('11', 'Dao động điều hoà', 'Li độ, biên độ, chu kì, tần số, pha ban đầu', 1),
  ('11', 'Dao động điều hoà', 'Viết phương trình dao động điều hoà', 2),
  ('11', 'Dao động điều hoà', 'Đọc đồ thị li độ – thời gian', 3),
  ('11', 'Vận tốc, gia tốc trong dao động điều hoà', 'Công thức vận tốc, gia tốc theo li độ', 1),
  ('11', 'Vận tốc, gia tốc trong dao động điều hoà', 'Quan hệ pha giữa x, v, a', 2),
  ('11', 'Vận tốc, gia tốc trong dao động điều hoà', 'Hệ thức độc lập với thời gian', 3),
  ('11', 'Năng lượng trong dao động điều hoà', 'Động năng, thế năng của vật dao động', 1),
  ('11', 'Năng lượng trong dao động điều hoà', 'Bảo toàn cơ năng trong dao động điều hoà', 2),
  ('11', 'Dao động tắt dần. Dao động cưỡng bức. Cộng hưởng', 'Dao động tắt dần và nguyên nhân', 1),
  ('11', 'Dao động tắt dần. Dao động cưỡng bức. Cộng hưởng', 'Dao động cưỡng bức và hiện tượng cộng hưởng', 2),
  ('11', 'Mô tả sóng', 'Bước sóng, chu kì, tần số, tốc độ truyền sóng', 1),
  ('11', 'Mô tả sóng', 'Phương trình sóng và đồ thị sóng', 2),
  ('11', 'Sóng ngang, sóng dọc. Truyền năng lượng của sóng cơ', 'Phân biệt sóng ngang và sóng dọc', 1),
  ('11', 'Sóng ngang, sóng dọc. Truyền năng lượng của sóng cơ', 'Sóng truyền năng lượng, không truyền phần tử môi trường', 2),
  ('11', 'Sóng điện từ', 'Đặc điểm và thang sóng điện từ', 1),
  ('11', 'Sóng điện từ', 'Ứng dụng sóng điện từ trong truyền thông', 2),
  ('11', 'Giao thoa sóng', 'Điều kiện giao thoa, cực đại và cực tiểu', 1),
  ('11', 'Giao thoa sóng', 'Xác định số điểm cực đại, cực tiểu trên đoạn thẳng', 2),
  ('11', 'Giao thoa sóng', 'Giao thoa ánh sáng qua khe Young', 3),
  ('11', 'Sóng dừng', 'Nút, bụng sóng và điều kiện có sóng dừng', 1),
  ('11', 'Sóng dừng', 'Tính bước sóng, tốc độ truyền sóng từ sóng dừng', 2),
  ('11', 'Sóng âm và đo tốc độ truyền âm', 'Đặc trưng vật lí và sinh lí của âm', 1),
  ('11', 'Sóng âm và đo tốc độ truyền âm', 'Đo tốc độ truyền âm bằng ống cộng hưởng', 2),
  ('11', 'Lực tương tác giữa hai điện tích', 'Định luật Coulomb', 1),
  ('11', 'Lực tương tác giữa hai điện tích', 'Cân bằng của điện tích chịu nhiều lực', 2),
  ('11', 'Khái niệm điện trường. Cường độ điện trường', 'Cường độ điện trường của điện tích điểm', 1),
  ('11', 'Khái niệm điện trường. Cường độ điện trường', 'Nguyên lí chồng chất điện trường', 2),
  ('11', 'Điện trường đều', 'Đặc điểm điện trường đều giữa hai bản song song', 1),
  ('11', 'Điện trường đều', 'Chuyển động của điện tích trong điện trường đều', 2),
  ('11', 'Thế năng điện. Điện thế', 'Công của lực điện và thế năng điện', 1),
  ('11', 'Thế năng điện. Điện thế', 'Điện thế, hiệu điện thế và liên hệ U = Ed', 2),
  ('11', 'Tụ điện và điện dung', 'Điện dung, ghép tụ nối tiếp và song song', 1),
  ('11', 'Tụ điện và điện dung', 'Năng lượng của tụ điện', 2),
  ('11', 'Cường độ dòng điện', 'Định nghĩa cường độ dòng điện và mật độ dòng', 1),
  ('11', 'Cường độ dòng điện', 'Liên hệ cường độ dòng điện với chuyển động hạt tải điện', 2),
  ('11', 'Điện trở. Định luật Ohm', 'Đường đặc trưng vôn – ampe', 1),
  ('11', 'Điện trở. Định luật Ohm', 'Điện trở phụ thuộc nhiệt độ', 2),
  ('11', 'Nguồn điện. Suất điện động', 'Suất điện động và điện trở trong của nguồn', 1),
  ('11', 'Nguồn điện. Suất điện động', 'Định luật Ohm cho toàn mạch', 2),
  ('11', 'Năng lượng điện. Công suất điện', 'Công và công suất của nguồn điện', 1),
  ('11', 'Năng lượng điện. Công suất điện', 'Hiệu suất nguồn điện, an toàn điện', 2),

  -- ================= LỚP 12 =================
  ('12', 'Sự chuyển thể', 'Cấu trúc chất rắn, lỏng, khí theo mô hình động học phân tử', 1),
  ('12', 'Sự chuyển thể', 'Nóng chảy, đông đặc, hoá hơi, ngưng tụ', 2),
  ('12', 'Thang nhiệt độ. Nhiệt kế', 'Thang Celsius và thang Kelvin', 1),
  ('12', 'Thang nhiệt độ. Nhiệt kế', 'Nhiệt độ và cân bằng nhiệt', 2),
  ('12', 'Nội năng. Định luật 1 của nhiệt động lực học', 'Nội năng và hai cách làm biến đổi nội năng', 1),
  ('12', 'Nội năng. Định luật 1 của nhiệt động lực học', 'Vận dụng ΔU = A + Q', 2),
  ('12', 'Nhiệt dung riêng, nhiệt nóng chảy riêng, nhiệt hoá hơi riêng', 'Tính nhiệt lượng theo nhiệt dung riêng', 1),
  ('12', 'Nhiệt dung riêng, nhiệt nóng chảy riêng, nhiệt hoá hơi riêng', 'Nhiệt nóng chảy riêng và nhiệt hoá hơi riêng', 2),
  ('12', 'Nhiệt dung riêng, nhiệt nóng chảy riêng, nhiệt hoá hơi riêng', 'Xử lí số liệu thí nghiệm đo nhiệt', 3),
  ('12', 'Thuyết động học phân tử chất khí', 'Nội dung thuyết động học phân tử', 1),
  ('12', 'Thuyết động học phân tử chất khí', 'Mol, số Avogadro và lượng chất khí', 2),
  ('12', 'Định luật Boyle. Định luật Charles', 'Quá trình đẳng nhiệt và định luật Boyle', 1),
  ('12', 'Định luật Boyle. Định luật Charles', 'Quá trình đẳng áp và định luật Charles', 2),
  ('12', 'Định luật Boyle. Định luật Charles', 'Đọc đồ thị các đẳng quá trình', 3),
  ('12', 'Phương trình trạng thái khí lí tưởng', 'Vận dụng phương trình trạng thái', 1),
  ('12', 'Phương trình trạng thái khí lí tưởng', 'Phương trình Clapeyron – Mendeleev', 2),
  ('12', 'Áp suất và động năng phân tử khí', 'Liên hệ áp suất với động năng phân tử', 1),
  ('12', 'Áp suất và động năng phân tử khí', 'Động năng trung bình phân tử và nhiệt độ', 2),
  ('12', 'Khái niệm từ trường', 'Đường sức từ và từ phổ', 1),
  ('12', 'Khái niệm từ trường', 'Từ trường của nam châm và của dòng điện', 2),
  ('12', 'Lực từ. Cảm ứng từ', 'Quy tắc bàn tay trái, xác định phương chiều lực từ', 1),
  ('12', 'Lực từ. Cảm ứng từ', 'Tính lực từ F = BIl·sinθ', 2),
  ('12', 'Từ thông. Hiện tượng cảm ứng điện từ', 'Từ thông qua khung dây', 1),
  ('12', 'Từ thông. Hiện tượng cảm ứng điện từ', 'Định luật Faraday và định luật Lenz', 2),
  ('12', 'Đại cương về dòng điện xoay chiều', 'Giá trị hiệu dụng của dòng điện xoay chiều', 1),
  ('12', 'Đại cương về dòng điện xoay chiều', 'Viết biểu thức u, i theo thời gian', 2),
  ('12', 'Cấu trúc hạt nhân', 'Kí hiệu hạt nhân, số nuclôn, đồng vị', 1),
  ('12', 'Cấu trúc hạt nhân', 'Kích thước, khối lượng hạt nhân và đơn vị u', 2),
  ('12', 'Độ hụt khối. Năng lượng liên kết hạt nhân', 'Tính độ hụt khối và năng lượng liên kết', 1),
  ('12', 'Độ hụt khối. Năng lượng liên kết hạt nhân', 'Năng lượng liên kết riêng và độ bền hạt nhân', 2),
  ('12', 'Phản ứng phân hạch, phản ứng nhiệt hạch', 'Định luật bảo toàn trong phản ứng hạt nhân', 1),
  ('12', 'Phản ứng phân hạch, phản ứng nhiệt hạch', 'Năng lượng toả ra của phản ứng hạt nhân', 2),
  ('12', 'Phản ứng phân hạch, phản ứng nhiệt hạch', 'Nhà máy điện hạt nhân và phản ứng nhiệt hạch', 3),
  ('12', 'Hiện tượng phóng xạ. Chu kì bán rã', 'Các tia phóng xạ α, β, γ', 1),
  ('12', 'Hiện tượng phóng xạ. Chu kì bán rã', 'Định luật phóng xạ và chu kì bán rã', 2),
  ('12', 'Hiện tượng phóng xạ. Chu kì bán rã', 'Độ phóng xạ và bài toán xác định tuổi', 3),
  ('12', 'An toàn phóng xạ', 'Liều chiếu xạ và tác hại của phóng xạ', 1),
  ('12', 'An toàn phóng xạ', 'Nguyên tắc an toàn khi làm việc với nguồn phóng xạ', 2)
;

-- Chủ đề cha không tìm thấy thì dừng, đừng chèn nửa vời.
do $$
declare v_missing text;
begin
  select string_agg(distinct o.grade || ' · ' || o.parent_name, ', ') into v_missing
  from tmp_outcomes o
  where not exists (
    select 1 from public.question_topics p
    where p.subject_code = 'vat-ly' and p.grade = o.grade
      and p.name = o.parent_name and p.parent_id is null
  );
  if v_missing is not null then
    raise exception 'Không tìm thấy chủ đề cha: %', v_missing;
  end if;
end $$;

insert into public.question_topics
  (subject_code, grade, parent_id, chapter_id, lesson_id, name, sort_order)
select 'vat-ly', o.grade, p.id, p.chapter_id, p.lesson_id, o.name, p.sort_order + o.idx
from tmp_outcomes o
join public.question_topics p
  on p.subject_code = 'vat-ly' and p.grade = o.grade
 and p.name = o.parent_name and p.parent_id is null
on conflict (subject_code, grade, name) do update
  set parent_id = excluded.parent_id,
      sort_order = excluded.sort_order;

do $$
declare v_count int;
begin
  select count(*) into v_count from public.question_topics where parent_id is not null;
  raise notice 'Danh mục hiện có % yêu cầu cần đạt.', v_count;
end $$;
