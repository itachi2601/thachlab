---
title: "Vì Sao Chim Đậu Trên Dây Điện Không Bị Giật?"
description: "Dây điện mang dòng 200 A, nhưng chim đậu trên đó vẫn bình yên. Hiệu điện thế giữa hai chân chim chỉ cỡ vài milivôn, còn dòng qua thân chim cỡ một phần triệu ampe."
date: "2026-10-10"
author: "Thầy Thạch"
category: "Vật lý quanh ta"
tags:
  - "Nhà cửa & điện"
  - "KHTN 9"
  - "Lớp 11"
keywords:
  - "vì sao chim đậu trên dây điện không bị giật"
  - "hiệu điện thế giữa hai điểm trên dây"
  - "mạch song song"
  - "vật lý quanh ta"
  - "ThachLab"
---

Trên đường đi học, em hay thấy chim đậu thành hàng trên dây điện, rỉa lông, nhìn quanh, chẳng hề hấn gì. Thế mà ai cũng được dặn: "Chạm vào dây điện là nguy hiểm chết người."

Vì sao chim đậu trên dây điện lại không bị giật?

![Hai con chim đậu trên dây điện, cả hai chân cùng đặt trên một dây](/images/blog/vi-sao-chim-dau-day-dien-khong-bi-giat-canh.svg)

*Hai chân chim cùng đặt trên một sợi dây.*

*Mũi tên đỏ: chiều dòng điện tại một thời điểm (lưới điện xoay chiều nên chiều đổi liên tục).*

## Đoán thử trước khi đọc

Theo em, vì sao chim vẫn an toàn?

- A. Lông chim và chân chim là chất cách điện hoàn hảo, nên điện không đi qua được.
- B. Chim nhẹ quá, nên điện "không bám" vào chim.
- C. Giữa hai chân chim gần như không có hiệu điện thế, nên dòng qua chim rất nhỏ.

Chọn một đáp án trong đầu rồi đọc tiếp. Đáp án đúng là C. Phương án A nghe hợp lý nhưng sai: thân và chân chim dẫn điện kém, chứ không cách điện hoàn hảo.

## Điện chỉ chạy khi có hiệu điện thế

Dòng điện chạy qua một vật khi có **hiệu điện thế** U giữa hai đầu vật đó. Hiệu điện thế là "độ chênh" điện thế, giống độ chênh độ cao làm nước chảy xuống dốc.

Chim đâu có chạm đất. Điều quan trọng là **độ chênh giữa hai điểm chạm vào cơ thể chim**, tức giữa hai chân.

Hai chân chim cách nhau cỡ 10 cm trên cùng một sợi dây. Dây có điện trở, nên giữa hai điểm A và B vẫn có một hiệu điện thế rất nhỏ: U = I · R.

![Sơ đồ mạch: đoạn dây AB song song với thân chim](/images/blog/vi-sao-chim-dau-day-dien-khong-bi-giat-so-do-mach.svg)

*Đoạn dây giữa hai chân (từ A đến B) có điện trở R dây rất nhỏ.*

*Thân chim nối giữa A và B, song song với đoạn dây đó.*

*Hai nhánh song song có cùng hiệu điện thế U(AB).*

Thân chim là một **nhánh song song** với đoạn dây AB. Em đã học: hai nhánh song song có cùng hiệu điện thế, và nhánh có điện trở nhỏ nhận dòng lớn. Dây có điện trở nhỏ hơn thân chim hàng trăm triệu lần, nên gần như toàn bộ dòng điện đi qua dây.

## Thử ước lượng bằng số

Giả sử dây nhôm tiết diện S = 100 mm² = 1,0×10⁻⁴ m² đang tải dòng I = 200 A. Điện trở suất của nhôm ở 20 °C là ρ ≈ 2,8×10⁻⁸ Ω·m (đồng: khoảng 1,7×10⁻⁸ Ω·m).

- Đoạn dây giữa hai chân dài ℓ = 0,1 m: R = ρ·ℓ / S = 2,8×10⁻⁸ × 0,1 / 1,0×10⁻⁴ ≈ 2,8×10⁻⁵ Ω.
- Hiệu điện thế giữa hai chân: U = I·R = 200 × 2,8×10⁻⁵ ≈ 5,6×10⁻³ V = 5,6 mV.
- Điện trở thân chim, ước chừng R chim ≈ 5 kΩ = 5×10³ Ω. Dòng qua chim: I chim = U / R chim ≈ 5,6×10⁻³ / 5×10³ ≈ 1×10⁻⁶ A = 1 µA.

Dòng 1 µA nhỏ hơn dòng trong dây khoảng 200 triệu lần. Với người, dòng cỡ 0,5 mA trở xuống hầu như không cảm thấy gì, nên 1 µA là cực kỳ nhỏ.

Đây chỉ là ước lượng bậc độ lớn: điện trở thân chim thay đổi nhiều theo loài và độ ẩm. Kết luận không đổi: U rất nhỏ nên dòng qua chim rất nhỏ.

## Khi nào thì nguy hiểm?

Mọi chuyện đổi khác nếu hai điểm trên cơ thể chạm vào hai chỗ **có điện thế khác nhau nhiều**. Ví dụ chim sải cánh chạm sang dây thứ hai khác pha, hoặc một chân chạm dây còn thân chạm cột điện nối đất. Khi đó U giữa hai điểm có thể lên tới hàng nghìn vôn, và dòng qua thân đủ lớn để gây hại.

Vì vậy người ta giữ các dây cách nhau khá xa. Với con người, chạm dây điện không bao giờ an toàn, vì chân ta thường đứng trên đất nên dây điện có điện thế cao hơn đất rất nhiều. **Em tuyệt đối không được leo lên cột điện, thả diều gần đường dây hay chạm vào dây điện đứt**, dù thấy chim đậu trên đó.

## Tự thử ở nhà

Em cần một pin 1,5 V, hai bóng đèn pin nhỏ (loại 1,5 V) và vài đoạn dây có kẹp cá sấu. Chỉ dùng pin, tuyệt đối không dùng ổ cắm điện trong nhà.

1. Mắc nối tiếp pin, bóng A và bóng B thành một vòng kín. Cả hai bóng sáng mờ (mỗi bóng chỉ nhận khoảng một nửa hiệu điện thế của pin). Chọn bóng nhỏ, cỡ 0,1–0,3 A.
2. Nối thêm một đoạn dây dẫn ngắn song song với bóng B, tức là hai đầu dây nối vào hai đầu bóng B (xem hình dưới).
3. Quan sát: bóng A sáng hơn trước, còn bóng B tắt.
4. Tháo đoạn dây ra, bóng B sáng lại.

![Sơ đồ thí nghiệm: pin, bóng A, và bóng B mắc song song với một đoạn dây dẫn ngắn](/images/blog/vi-sao-chim-dau-day-dien-khong-bi-giat-thi-nghiem.svg)

*Bóng B đóng vai "con chim", đoạn dây ngắn đóng vai "dây điện".*

*Bóng A giữ cho dòng điện không quá lớn, nên mạch an toàn.*

Vì sao? Đoạn dây ngắn có điện trở rất nhỏ, nên hiệu điện thế giữa hai đầu bóng B gần bằng 0 và dòng qua B gần như bằng 0. Gần như cả dòng điện đi qua dây. Đừng nối dây thẳng hai cực pin mà không có bóng, vì pin sẽ nóng lên.

## Hiểu lầm hay gặp

- ❌ Chim không bị giật vì chân chim cách điện. → ✅ Chân chim dẫn điện kém nhưng không cách điện hoàn hảo. Chim an toàn chủ yếu vì hiệu điện thế giữa hai chân rất nhỏ.
- ❌ Chim đậu trên cao không chạm đất nên người đứng trên cao chạm dây cũng an toàn. → ✅ Người chạm dây điện đang có điện sẽ nguy hiểm, kể cả đứng trên cao, vì chỉ cần chạm thêm một vật khác điện thế (cột, tường, thang kim loại, cây ướt) là có dòng qua người.

## Em đã học ở đâu?

- [KHTN 9 · Bài 11. Điện trở. Định luật Ohm](/lop-hoc/bai?id=89&subject=vat-ly&chapter=19)
- [KHTN 9 · Bài 12. Đoạn mạch nối tiếp, song song](/lop-hoc/bai?id=90&subject=vat-ly&chapter=19)
- [Lớp 11 · Bài 22. Cường độ dòng điện](/lop-hoc/bai?id=41&subject=vat-ly&chapter=9)
- [Lớp 11 · Bài 23. Điện trở. Định luật Ohm](/lop-hoc/bai?id=42&subject=vat-ly&chapter=9)

## Nghĩ tiếp

Nếu hai chân chim đứng cách nhau xa hơn, ví dụ một con chim lớn dang chân cách nhau 50 cm, thì hiệu điện thế giữa hai chân tăng hay giảm, và tăng bao nhiêu lần?

Gợi ý: điện trở của đoạn dây tỉ lệ thuận với chiều dài.

## Nguồn

- [Electronics Notes — Electrical Resistivity Table for Common Materials](https://www.electronics-notes.com/articles/basic_concepts/resistance/electrical-resistivity-table-materials.php) (truy cập 10/10/2026): đồng 1,7×10⁻⁸ Ω·m, nhôm 2,8×10⁻⁸ Ω·m ở 20 °C.
- [Science Focus — Why don't birds get electrocuted while perching on power lines?](https://www.sciencefocus.com/science/why-dont-birds-get-electrocuted-while-perching-on-power-lines/) (truy cập 10/10/2026): chim an toàn vì hai chân cùng điện thế và không tạo mạch kín.
- [EMF-Portal — Background information for limit values (IEC 60479-1)](https://emf-portal.org/en/cms/page/home/more/electrical-injuries/background-information-for-limit-values) (truy cập 10/10/2026): dòng xoay chiều đến khoảng 0,5 mA hầu như không cảm nhận được.
- SGK Vật lí 11 (Kết nối tri thức), Bài 23. Điện trở. Định luật Ohm.
