# -*- coding: utf-8 -*-
"""CĐ16 Truyền nhiệt và sự nở vì nhiệt (lesson 164) — Bài tập tự luận (xếp từ dễ đến khó).
Xuất tu_luan() (dict label + body_html) và kiem_so() (assert mọi đáp số).
Tự soạn 16/10/2026, phỏng theo kiểu đề HSG 9 / tuyển sinh 10 chuyên phổ biến, không chép đề cụ thể nào.
Số liệu khác 6 dạng mẫu D1–D6 trong content/hsg9/cd16-truyen-nhiet-no-vi-nhiet/nguon.md."""
from fractions import Fraction as F
from math import isclose

TL = [
 # ── Bài 1 · Dễ: ba cách truyền nhiệt (giải thích)
 ("Dễ", r"""<p>a) Phích (bình thuỷ) giữ nước nóng được lâu. Nêu tác dụng của từng bộ phận: lớp chân không giữa hai vỏ thuỷ tinh, mặt tráng bạc sáng bóng của hai vỏ, nút phích. Mỗi bộ phận chặn cách truyền nhiệt nào?</p>
<p>b) Mùa đông, mặc hai áo mỏng chồng lên nhau thấy ấm hơn mặc một áo dày có cùng khối lượng vải. Giải thích.</p>
<p>c) Trong một căn phòng để lâu, tay nắm cửa bằng đồng và cánh cửa gỗ có cùng nhiệt độ. Vì sao sờ vào tay nắm đồng lại thấy lạnh hơn? Bạn Bình nói "vì đồng truyền lạnh sang tay". Câu nói đó sai ở đâu?</p>""",
  r"""<p>a) Lớp chân không: chân không không có hạt vật chất nên chặn dẫn nhiệt và đối lưu giữa hai vỏ.</p>
<p>Mặt tráng bạc: phản xạ bức xạ nhiệt trở lại nước, chặn truyền nhiệt bằng bức xạ.</p>
<p>Nút phích: ngăn không khí nóng trên mặt nước bay ra ngoài, chặn đối lưu (và bay hơi) qua miệng phích.</p>
<p>b) Giữa hai áo có một lớp không khí bị giữ lại; không khí dẫn nhiệt rất kém và bị kẹp nên khó đối lưu.</p>
<p>Lớp không khí này cản nhiệt từ người truyền ra ngoài tốt hơn phần vải dày thêm.</p>
<p>c) Đồng dẫn nhiệt tốt hơn gỗ rất nhiều. Tay ấm hơn tay nắm nên nhiệt truyền từ tay sang đồng, rồi lan nhanh đi khắp tay nắm, nên chỗ tiếp xúc luôn nguội và tay mất nhiệt nhanh: cảm giác lạnh.</p>
<p>Gỗ dẫn nhiệt kém, chỗ tiếp xúc nhanh chóng ấm lên bằng tay nên tay mất nhiệt chậm.</p>
<p>Câu của Bình sai: không có "lạnh" truyền đi; chỉ có nhiệt truyền từ vật nóng hơn (tay) sang vật lạnh hơn (đồng).</p>
<p>Lỗi hay gặp: kết luận tay nắm đồng có nhiệt độ thấp hơn cánh cửa — cảm giác nóng lạnh là tốc độ tay mất nhiệt, không phải nhiệt độ của vật.</p>"""),

 # ── Bài 2 · Dễ: sự nở vì nhiệt (băng kép, nước 4 °C, khe hở)
 ("Dễ", r"""<p>a) Trong bàn là có một băng kép gồm một lá đồng và một lá thép tán chặt vào nhau (đồng nở vì nhiệt nhiều hơn thép), đầu tự do của băng kép tì lên một tiếp điểm nằm <b>phía dưới</b> nó để dòng điện chạy qua. Khi bàn là quá nóng, băng kép phải cong <b>lên trên</b>, rời tiếp điểm để ngắt điện. Phải đặt lá đồng ở trên hay ở dưới? Giải thích.</p>
<p>b) Ở xứ lạnh, mùa đông mặt hồ đóng băng nhưng cá dưới đáy hồ sâu vẫn sống. Giải thích dựa vào sự nở vì nhiệt đặc biệt của nước.</p>
<p>c) Vì sao giữa hai đầu thanh ray xe lửa phải chừa khe hở, còn ống dẫn hơi nóng dài thường có đoạn uốn cong?</p>""",
  r"""<p>a) Khi nóng, lá nở nhiều hơn dài hơn nên nằm ở mặt lồi; băng kép cong về phía lá nở ít (thép).</p>
<p>Muốn băng kép cong lên trên thì mặt lồi ở dưới, tức lá đồng ở dưới, lá thép ở trên.</p>
<p>b) Nước từ $0\ ^\circ\text{C}$ đến $4\ ^\circ\text{C}$ co lại, nên khối lượng riêng của nước lớn nhất ở $4\ ^\circ\text{C}$.</p>
<p>Khi trời lạnh dần, nước ở $4\ ^\circ\text{C}$ nặng nhất chìm xuống đáy; nước lạnh hơn ($0$–$4\ ^\circ\text{C}$) nhẹ hơn nổi lên trên và đóng băng ở mặt.</p>
<p>Lớp băng ở mặt dẫn nhiệt kém, che cho nước bên dưới, đáy hồ giữ khoảng $4\ ^\circ\text{C}$ nên cá sống được.</p>
<p>c) Thanh ray, ống dẫn nở ra khi nóng; nếu bị giữ chặt không cho nở thì sinh lực rất lớn làm cong vênh ray, nứt ống.</p>
<p>Khe hở cho ray chỗ để dài ra; đoạn uốn cong của ống co giãn được, hấp thụ phần dài thêm.</p>
<p>Lỗi hay gặp: nghĩ băng kép cong về phía kim loại nở nhiều — ngược lại, kim loại nở nhiều nằm ở mặt lồi.</p>
<p>Lỗi hay gặp: cho rằng nước càng lạnh càng nặng nên chìm xuống, hồ đóng băng từ đáy.</p>"""),

 # ── Bài 3 · Trung bình: thước kim loại bị nở
 ("Trung bình", r"""<p>Một thước nhôm được khắc vạch chính xác ở $20\ ^\circ\text{C}$. Ở $50\ ^\circ\text{C}$, dùng thước này đo một thanh đồng thì đọc được $80{,}00\ \text{cm}$. Hệ số nở dài của nhôm $\alpha_{Al} = 24\cdot10^{-6}\ \text{K}^{-1}$, của đồng $\alpha_{Cu} = 17\cdot10^{-6}\ \text{K}^{-1}$, của thép $\alpha_{Fe} = 12\cdot10^{-6}\ \text{K}^{-1}$. Thước và thanh đồng có cùng nhiệt độ lúc đo.</p>
<p>a) Tính chiều dài thật của thanh đồng ở $50\ ^\circ\text{C}$.</p>
<p>b) Tính chiều dài của thanh đồng ở $20\ ^\circ\text{C}$.</p>
<p>c) Nếu dùng thước thép (khắc đúng ở $20\ ^\circ\text{C}$) đo thanh đồng đó ở $50\ ^\circ\text{C}$ thì đọc được bao nhiêu? Nên chọn thước bằng vật liệu thế nào để đo chính xác khi nhiệt độ thay đổi?</p>""",
  r"""<p>a) Ở $50\ ^\circ\text{C}$ mỗi vạch "1 cm" của thước nhôm dài thật $1\cdot(1 + 24\cdot10^{-6}\cdot30) = 1{,}00072\ \text{cm}$.</p>
<p>Thanh đồng dài $80{,}00$ vạch, nên chiều dài thật $l_{50} = 80\cdot1{,}00072 \approx 80{,}058\ \text{cm}$.</p>
<p>Thước dãn ra nên mỗi vạch dài hơn 1 cm, số đọc nhỏ hơn chiều dài thật.</p>
<p>b) $l_{50} = l_{20}(1 + \alpha_{Cu}\cdot30)$, nên $l_{20} = \dfrac{80{,}0576}{1{,}00051} \approx 80{,}017\ \text{cm}$.</p>
<p>c) Mỗi vạch thước thép ở $50\ ^\circ\text{C}$ dài $1{,}00036\ \text{cm}$, số đọc $= \dfrac{80{,}0576}{1{,}00036} \approx 80{,}029\ \text{cm}$.</p>
<p>Thước nở càng ít thì số đọc càng sát chiều dài thật: nên dùng vật liệu có hệ số nở dài nhỏ (hoặc hiệu chỉnh theo nhiệt độ).</p>
<p>Lỗi hay gặp: chia $80$ cho $1{,}00072$ (ra $79{,}942\ \text{cm}$) — thước dãn thì đọc thiếu, chiều dài thật phải lớn hơn số đọc.</p>
<p>Lỗi hay gặp: ở câu b lấy luôn số đọc $80{,}00\ \text{cm}$ làm chiều dài ở $50\ ^\circ\text{C}$ (ra $79{,}959\ \text{cm}$), quên hiệu chỉnh thước trước.</p>"""),

 # ── Bài 4 · Trung bình: hao phí không đổi — đun hai lần với hai công suất
 ("Trung bình", r"""<p>Dùng một ấm điện đun $1{,}2$ lít nước từ $20\ ^\circ\text{C}$ đến sôi. Lần thứ nhất bếp có công suất $1000\ \text{W}$, nước sôi sau $8$ phút. Lần thứ hai (cùng ấm, cùng lượng nước, cùng nhiệt độ đầu $20\ ^\circ\text{C}$) điện yếu, bếp chỉ còn công suất $700\ \text{W}$, nước sôi sau $12$ phút. Coi công suất hao phí ra môi trường không đổi và như nhau ở hai lần đun; vỏ ấm có nhiệt dung $C$ chưa biết và luôn cùng nhiệt độ với nước.</p>
<p>a) Tính công suất hao phí.</p>
<p>b) Tính nhiệt dung $C$ của vỏ ấm.</p>
<p>c) Tính hiệu suất của lần đun thứ nhất (chỉ tính phần nhiệt nước nhận).</p>
<p>d) Theo giả thiết hao phí không đổi của đề, nếu điện yếu tới mức bếp chỉ còn $400\ \text{W}$ thì sau bao lâu nước sôi? Bếp có công suất bao nhiêu thì không bao giờ đun sôi được?</p>""",
  r"""<p>Nhiệt cần đun ấm và nước tới sôi là $Q$, như nhau ở hai lần. Phần công suất làm nóng ấm và nước là $P - P_{hp}$.</p>
<p>a) $(1000 - P_{hp})\cdot480 = (700 - P_{hp})\cdot720$.</p>
<p>$480\,000 - 480P_{hp} = 504\,000 - 720P_{hp}$, nên $240P_{hp} = 24\,000$ và $P_{hp} = 100\ \text{W}$.</p>
<p>b) $Q = (1000 - 100)\cdot480 = 432\,000\ \text{J}$.</p>
<p>Nước nhận $Q_n = 1{,}2\cdot4200\cdot80 = 403\,200\ \text{J}$, vỏ ấm nhận $Q - Q_n = 28\,800\ \text{J}$.</p>
<p>$C = \dfrac{28\,800}{80} = 360\ \text{J/K}$.</p>
<p>c) $H = \dfrac{403\,200}{1000\cdot480} = 0{,}84 = 84\%$.</p>
<p>d) Bếp $400\ \text{W}$: $t = \dfrac{432\,000}{400 - 100} = 1440\ \text{s} = 24$ phút.</p>
<p>Bếp có công suất $P \le 100\ \text{W}$ thì toàn bộ nhiệt bị hao phí, nước không nóng thêm được tới sôi.</p>
<p>Ghi chú: thực tế hao phí tăng khi nước nóng hơn; "hao phí không đổi" là giả thiết đề cho để tính gần đúng.</p>
<p>Lỗi hay gặp: viết $1000\cdot480 = 700\cdot720$ (bỏ hao phí) — hai vế không bằng nhau, chứng tỏ phải có hao phí.</p>
<p>Lỗi hay gặp: tính hao phí dưới dạng nhiệt lượng chung cho hai lần — hao phí không đổi về công suất, lần đun lâu hơn mất nhiều nhiệt hơn.</p>"""),

 # ── Bài 5 · Khó: ấm nguội dần, hao phí tỉ lệ hiệu nhiệt độ
 ("Khó", r"""<p>Một ấm điện chứa $1{,}5$ lít nước, vỏ ấm có nhiệt dung $700\ \text{J/K}$ và luôn cùng nhiệt độ với nước. Phòng luôn ở $25\ ^\circ\text{C}$. Ở chế độ giữ ấm, bếp cấp đều $120\ \text{W}$ thì nhiệt độ nước ổn định ở $85\ ^\circ\text{C}$. Coi công suất hao phí ra môi trường tỉ lệ với hiệu nhiệt độ nước – phòng, ấm đậy kín (bỏ qua bay hơi).</p>
<p>a) Tìm hệ số $k$ trong $P_{hp} = k(t - t_0)$.</p>
<p>b) Ngắt điện khi nước ở $95\ ^\circ\text{C}$. Tính tốc độ giảm nhiệt độ (°C/phút) ngay lúc ngắt điện, và khi nước còn $40\ ^\circ\text{C}$. Nhận xét.</p>
<p>c) Ước lượng thời gian nước nguội từ $95\ ^\circ\text{C}$ xuống $93\ ^\circ\text{C}$.</p>
<p>d) Muốn giữ ấm ở $70\ ^\circ\text{C}$ thì bếp phải cấp đều bao nhiêu oát?</p>""",
  r"""<p>a) Khi ổn định, công suất cấp bằng công suất hao phí: $120 = k(85 - 25)$, nên $k = 2\ \text{W/}^\circ\text{C}$.</p>
<p>b) Nhiệt dung của ấm và nước: $C_{tp} = 1{,}5\cdot4200 + 700 = 7000\ \text{J/K}$.</p>
<p>Đã ngắt điện, nhiệt mất mỗi giây là $P_{hp}$, nên nhiệt độ giảm mỗi giây $\dfrac{P_{hp}}{C_{tp}}$.</p>
<p>Ở $95\ ^\circ\text{C}$: $P_{hp} = 2\cdot70 = 140\ \text{W}$, tốc độ $\dfrac{140}{7000} = 0{,}02\ ^\circ\text{C/s} = 1{,}2\ ^\circ\text{C/phút}$.</p>
<p>Ở $40\ ^\circ\text{C}$: $P_{hp} = 2\cdot15 = 30\ \text{W}$, tốc độ $\dfrac{30}{7000}\ ^\circ\text{C/s} \approx 0{,}26\ ^\circ\text{C/phút}$.</p>
<p>Nhận xét: nước càng gần nhiệt độ phòng thì nguội càng chậm (tốc độ giảm $\tfrac{70}{15} \approx 4{,}7$ lần).</p>
<p>c) Từ $95$ xuống $93\ ^\circ\text{C}$ hiệu nhiệt độ thay đổi ít, lấy giá trị trung bình $t = 94\ ^\circ\text{C}$: $P_{hp} \approx 2\cdot69 = 138\ \text{W}$.</p>
<p>Nhiệt mất: $Q = 7000\cdot2 = 14\,000\ \text{J}$, nên $t \approx \dfrac{14\,000}{138} \approx 101\ \text{s}$ (khoảng $1{,}7$ phút).</p>
<p>d) $P = k(70 - 25) = 2\cdot45 = 90\ \text{W}$.</p>
<p>Lỗi hay gặp: dùng $k = \dfrac{120}{85}$ (lấy nhiệt độ nước thay cho hiệu nhiệt độ nước – phòng).</p>
<p>Lỗi hay gặp: coi hao phí không đổi rồi tính tốc độ nguội ở $40\ ^\circ\text{C}$ bằng ở $95\ ^\circ\text{C}$ — đề cho hao phí tỉ lệ hiệu nhiệt độ.</p>
<p>Lỗi hay gặp: quên nhiệt dung vỏ ấm, chỉ chia cho $6300\ \text{J/K}$ của nước.</p>"""),

 # ── Bài 6 · Khó: bình thuỷ tinh đầy thuỷ ngân nóng lên
 ("Khó", r"""<p>Một bình thuỷ tinh có dung tích $500\ \text{cm}^3$ ở $0\ ^\circ\text{C}$, chứa đầy thuỷ ngân tới miệng. Hệ số nở khối của thuỷ ngân $\beta_{Hg} = 1{,}8\cdot10^{-4}\ \text{K}^{-1}$, hệ số nở dài của thuỷ tinh $\alpha = 9\cdot10^{-6}\ \text{K}^{-1}$ (lấy $\beta \approx 3\alpha$). Khối lượng riêng thuỷ ngân ở $0\ ^\circ\text{C}$ là $13{,}6\ \text{g/cm}^3$. Đun nóng cả bình và thuỷ ngân lên $100\ ^\circ\text{C}$.</p>
<p>a) Tính thể tích thuỷ ngân tràn ra.</p>
<p>b) Tính khối lượng thuỷ ngân tràn ra.</p>
<p>c) Ở $0\ ^\circ\text{C}$ chỉ được rót bao nhiêu $\text{cm}^3$ thuỷ ngân vào bình để khi nóng tới $100\ ^\circ\text{C}$ thuỷ ngân vừa đầy tới miệng, không tràn?</p>
<p>d) Nếu bỏ qua sự nở của bình thì tính được thể tích tràn bao nhiêu? Sai lệch bao nhiêu phần trăm so với câu a?</p>""",
  r"""<p>a) Ở $100\ ^\circ\text{C}$, thuỷ ngân chiếm $500(1 + 1{,}8\cdot10^{-4}\cdot100) = 509\ \text{cm}^3$.</p>
<p>Bình nở theo $\beta_b = 3\alpha = 27\cdot10^{-6}\ \text{K}^{-1}$, dung tích mới $500(1 + 27\cdot10^{-6}\cdot100) = 501{,}35\ \text{cm}^3$.</p>
<p>Thể tích tràn: $\Delta V = 509 - 501{,}35 = 7{,}65\ \text{cm}^3$ (cũng bằng $V_0(\beta_{Hg} - \beta_b)\Delta t$).</p>
<p>b) Ở $100\ ^\circ\text{C}$: $D = \dfrac{13{,}6}{1 + 1{,}8\cdot10^{-4}\cdot100} = \dfrac{13{,}6}{1{,}018} \approx 13{,}36\ \text{g/cm}^3$.</p>
<p>$m = 13{,}36\cdot7{,}65 \approx 102\ \text{g}$.</p>
<p>c) Gọi $V_1$ là thể tích rót ở $0\ ^\circ\text{C}$: $V_1\cdot1{,}018 = 501{,}35$, nên $V_1 \approx 492{,}5\ \text{cm}^3$.</p>
<p>d) Bỏ qua nở của bình: $\Delta V' = 509 - 500 = 9\ \text{cm}^3$, lớn hơn $1{,}35\ \text{cm}^3$, tức lệch khoảng $17{,}6\%$.</p>
<p>Lỗi hay gặp: lấy $\beta_b = \alpha = 9\cdot10^{-6}$ (quên bình nở theo cả ba chiều), ra $\Delta V = 8{,}55\ \text{cm}^3$.</p>
<p>Lỗi hay gặp: dùng $13{,}6\ \text{g/cm}^3$ cho thuỷ ngân ở $100\ ^\circ\text{C}$ (ra $104\ \text{g}$) — thuỷ ngân nóng nở ra nên nhẹ hơn trên mỗi $\text{cm}^3$.</p>"""),

 # ── Bài 7 · Nâng cao: thanh ghép hai kim loại
 ("Nâng cao", r"""<p>Một thanh thép và một thanh nhôm được hàn nối đầu với nhau thành một thanh thẳng dài $1{,}000\ \text{m}$ ở $20\ ^\circ\text{C}$. Khi nung cả thanh tới $120\ ^\circ\text{C}$ thì thanh dài thêm $1{,}68\ \text{mm}$. Hệ số nở dài của thép $12\cdot10^{-6}\ \text{K}^{-1}$, của nhôm $24\cdot10^{-6}\ \text{K}^{-1}$, của đồng $17\cdot10^{-6}\ \text{K}^{-1}$.</p>
<p>a) Tính chiều dài mỗi đoạn ở $20\ ^\circ\text{C}$.</p>
<p>b) Coi thanh ghép như một thanh đồng chất, tính hệ số nở dài "trung bình" của nó.</p>
<p>c) Ở $20\ ^\circ\text{C}$, đặt thanh ghép giữa hai bức tường cố định, hai tường cách nhau $1{,}0005\ \text{m}$. Nung nóng đều thanh tới nhiệt độ nào thì thanh bắt đầu chạm cả hai tường?</p>
<p>d) Muốn thanh ghép thép – nhôm dài $1\ \text{m}$ nở giống hệt một thanh đồng dài $1\ \text{m}$ thì đoạn nhôm phải dài bao nhiêu?</p>""",
  r"""<p>a) Gọi $l_1$, $l_2$ là chiều dài đoạn thép, đoạn nhôm: $l_1 + l_2 = 1\ \text{m}$.</p>
<p>Độ dãn: $(12 l_1 + 24 l_2)\cdot10^{-6}\cdot100 = 1{,}68\cdot10^{-3}$, tức $12 l_1 + 24 l_2 = 16{,}8$.</p>
<p>Thay $l_1 = 1 - l_2$: $12 + 12 l_2 = 16{,}8$, nên $l_2 = 0{,}4\ \text{m}$ và $l_1 = 0{,}6\ \text{m}$.</p>
<p>b) $\alpha_{tb} = \dfrac{\Delta l}{l_0\,\Delta t} = \dfrac{1{,}68\cdot10^{-3}}{1\cdot100} = 16{,}8\cdot10^{-6}\ \text{K}^{-1}$.</p>
<p>c) Khe hở tổng $0{,}5\ \text{mm}$: $1\cdot16{,}8\cdot10^{-6}\cdot\Delta t = 0{,}5\cdot10^{-3}$, nên $\Delta t \approx 29{,}8\ ^\circ\text{C}$.</p>
<p>Thanh chạm hai tường ở khoảng $20 + 29{,}8 \approx 50\ ^\circ\text{C}$; nóng hơn nữa thanh bị cản nở, ép lên tường một lực rất lớn.</p>
<p>d) Cần $12(1 - x) + 24x = 17$, nên $12x = 5$ và $x = \dfrac{5}{12} \approx 0{,}417\ \text{m}$ (khoảng $41{,}7\ \text{cm}$ nhôm).</p>
<p>Lỗi hay gặp: lấy trung bình cộng $\dfrac{12 + 24}{2} = 18\cdot10^{-6}$ làm hệ số của thanh ghép — chỉ đúng khi hai đoạn dài bằng nhau.</p>
<p>Lỗi hay gặp: dùng $\Delta t = 120\ ^\circ\text{C}$ thay vì $100\ ^\circ\text{C}$.</p>"""),

 # ── Bài 8 · Nâng cao: ấm hai dây điện trở + hao phí tỉ lệ hiệu nhiệt độ
 ("Nâng cao", r"""<p>Một ấm điện có hai dây điện trở: dây 1 ghi $220\ \text{V} - 400\ \text{W}$, dây 2 ghi $220\ \text{V} - 600\ \text{W}$. Ấm luôn dùng ở hiệu điện thế $220\ \text{V}$, phòng ở $20\ ^\circ\text{C}$. Coi điện trở các dây không đổi theo nhiệt độ, công suất hao phí ra môi trường tỉ lệ với hiệu nhiệt độ nước – phòng (kể cả khi nước đang sôi). Chỉ dùng dây 1 thì đun mãi nước cũng chỉ nóng tới $60\ ^\circ\text{C}$ rồi giữ nguyên.</p>
<p>a) Tìm hệ số hao phí $k$ (W/°C). Chỉ dùng dây 2 thì nhiệt độ nước ổn định ở bao nhiêu?</p>
<p>b) Mắc hai dây nối tiếp vào $220\ \text{V}$: nước ổn định ở bao nhiêu độ?</p>
<p>c) Mắc hai dây song song vào $220\ \text{V}$: nước có sôi không? Nếu sôi, mỗi phút có bao nhiêu gam nước hoá hơi? Nhiệt hoá hơi của nước $L = 2{,}3\cdot10^6\ \text{J/kg}$.</p>""",
  r"""<p>a) Dây 1 dùng đúng $220\ \text{V}$ nên $P_1 = 400\ \text{W}$. Khi ổn định: $400 = k(60 - 20)$, nên $k = 10\ \text{W/}^\circ\text{C}$.</p>
<p>Dây 2: $600 = 10(t_2 - 20)$, nên $t_2 = 80\ ^\circ\text{C}$.</p>
<p>b) $R_1 = \dfrac{U^2}{P_1}$, $R_2 = \dfrac{U^2}{P_2}$. Nối tiếp: $P_{nt} = \dfrac{U^2}{R_1 + R_2} = \dfrac{P_1P_2}{P_1 + P_2} = \dfrac{400\cdot600}{1000} = 240\ \text{W}$.</p>
<p>$240 = 10(t - 20)$, nên $t = 44\ ^\circ\text{C}$.</p>
<p>c) Song song, mỗi dây vẫn chịu $220\ \text{V}$: $P_{ss} = 400 + 600 = 1000\ \text{W}$.</p>
<p>Muốn giữ nước ở $100\ ^\circ\text{C}$ chỉ cần bù hao phí $10\cdot(100 - 20) = 800\ \text{W}$ $\lt 1000\ \text{W}$, nên nước sôi.</p>
<p>Khi sôi nhiệt độ không tăng nữa; phần dư $200\ \text{W}$ làm nước hoá hơi.</p>
<p>Mỗi phút: $Q = 200\cdot60 = 12\,000\ \text{J}$, $m = \dfrac{12\,000}{2{,}3\cdot10^6} \approx 5{,}2\cdot10^{-3}\ \text{kg} \approx 5{,}2\ \text{g}$.</p>
<p>Lỗi hay gặp: cộng công suất khi mắc nối tiếp ($1000\ \text{W}$) — nối tiếp thì điện trở tăng, công suất giảm.</p>
<p>Lỗi hay gặp: tính nhiệt độ ổn định song song $= 20 + \dfrac{1000}{10} = 120\ ^\circ\text{C}$ — nước sôi ở $100\ ^\circ\text{C}$ và không nóng hơn; phần dư thành nhiệt hoá hơi.</p>"""),
]


def tu_luan():
    parts = []
    for k, (muc, de, gi) in enumerate(TL, 1):
        parts.append(f"<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>{gi}</details>")
    return dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
                body_html="<p>Các bài còn lại của chuyên đề, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>"
                          + "".join(parts))


def kiem_so():
    c = 4200
    aAl, aCu, aFe = F(24, 10**6), F(17, 10**6), F(12, 10**6)
    # Bài 3 — thước nhôm
    vach = 1 + aAl * 30; assert vach == F(100072, 100000)
    l50 = 80 * vach; assert l50 == F(800576, 10000) and abs(float(l50) - 80.058) < 5e-4
    l20 = l50 / (1 + aCu * 30); assert abs(float(l20) - 80.017) < 5e-4
    doc_thep = l50 / (1 + aFe * 30); assert abs(float(doc_thep) - 80.029) < 5e-4
    assert abs(80 / float(vach) - 79.942) < 5e-4
    assert abs(80 / float(1 + aCu * 30) - 79.959) < 5e-4
    # Bài 4 — hai công suất, hao phí không đổi
    t1, t2 = 8 * 60, 12 * 60
    php = F(1000 * t1 - 700 * t2, t1 - t2); assert php == 100
    Q = (1000 - php) * t1; assert Q == 432000 and (700 - php) * t2 == Q
    Qn = F(12, 10) * c * 80; assert Qn == 403200 and (Q - Qn) / 80 == 360
    assert Qn / (1000 * t1) == F(84, 100) and Q / (400 - php) == 1440 == 24 * 60
    assert 1000 * t1 != 700 * t2
    # Bài 5 — nguội dần
    k = F(120, 85 - 25); assert k == 2
    Ctp = F(15, 10) * c + 700; assert Ctp == 7000
    r95 = k * 70 / Ctp; assert r95 == F(1, 50) and r95 * 60 == F(6, 5)
    r40 = k * 15 / Ctp; assert abs(float(r40 * 60) - 0.26) < 5e-3 and abs(70 / 15 - 4.7) < 0.05
    tc = Ctp * 2 / (k * 69); assert abs(float(tc) - 101) < 0.5 and abs(float(tc) / 60 - 1.7) < 0.05
    assert k * 45 == 90
    # Bài 6 — thuỷ ngân tràn
    bHg, bg = F(18, 10**5), 3 * F(9, 10**6)
    VHg, Vb = 500 * (1 + bHg * 100), 500 * (1 + bg * 100)
    assert VHg == 509 and Vb == F(50135, 100) and VHg - Vb == F(765, 100) == 500 * (bHg - bg) * 100
    D100 = F(136, 10) / (1 + bHg * 100); assert abs(float(D100) - 13.36) < 5e-3
    m = D100 * (VHg - Vb); assert abs(float(m) - 102) < 0.5 and abs(13.6 * 7.65 - 104) < 0.1
    V1 = Vb / (1 + bHg * 100); assert abs(float(V1) - 492.5) < 0.05
    assert VHg - 500 == 9 and abs(float((9 - (VHg - Vb)) / (VHg - Vb)) - 0.176) < 5e-4
    assert abs(float(500 * (bHg - F(9, 10**6)) * 100) - 8.55) < 1e-9
    # Bài 7 — thanh ghép
    l2 = (F(168, 10) - 12) / 12; l1 = 1 - l2; assert (l1, l2) == (F(3, 5), F(2, 5))
    assert (aFe * l1 + aAl * l2) * 100 == F(168, 100000)
    atb = F(168, 100000) / 100; assert atb == F(168, 10**7)
    dt = F(5, 10000) / atb; assert abs(float(dt) - 29.8) < 0.05 and abs(20 + float(dt) - 50) < 0.5
    x = F(17 - 12, 12); assert x == F(5, 12) and abs(float(x) - 0.417) < 5e-4
    # Bài 8 — hai dây + hao phí tỉ lệ
    P1, P2, U = 400, 600, 220
    k8 = F(P1, 60 - 20); assert k8 == 10 and 20 + P2 / k8 == 80
    R1, R2 = F(U * U, P1), F(U * U, P2); Pnt = U * U / (R1 + R2)
    assert Pnt == 240 == F(P1 * P2, P1 + P2) and 20 + Pnt / k8 == 44
    assert P1 + P2 == 1000 and k8 * 80 == 800 < 1000
    mh = F(200 * 60) / F(23 * 10**5); assert abs(float(mh) * 1000 - 5.2) < 0.05
    print("kiểm số liệu tự luận 164: đạt")


if __name__ == "__main__":
    kiem_so()
    print(len(tu_luan()["body_html"]))
