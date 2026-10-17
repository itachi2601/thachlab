# -*- coding: utf-8 -*-
"""CĐ09 Năng lượng với cuộc sống (lesson 163) — Bài tập tự luận (xếp từ dễ đến khó).
Xuất tu_luan() (dict label + body_html) và kiem_so() (assert mọi đáp số).
Tự soạn 17/10/2026 theo dàn ý content/hsg9/cd09-nang-luong-cuoc-song/nguon.md (mục Tự luận TL1–TL6), số liệu
tính ở tinh.py cùng thư mục; khác 5 dạng bài tập mẫu và khác ví dụ docx (nguon.txt).
Ranh giới: không đun nước bằng bếp (CĐ12), không hao phí truyền tải (CĐ08), không biểu giá điện bậc thang (CĐ05),
không phương trình hoá học. Mọi đề ghi rõ "bỏ qua hao phí trên đường dây tải điện".
Ký hiệu theo nguon.md: lưu lượng L (m³/s), trọng lượng riêng d = 10D, hiệu suất chuỗi H = H1·H2·…"""
from math import isclose, pi, ceil

TL = [
 # ── Bài 1 · Dễ: chuỗi năng lượng và phân loại nguồn
 ("Dễ", r"""<p>a) Viết chuỗi biến đổi năng lượng, bắt đầu từ nguồn gốc đầu tiên, cho bốn trường hợp sau:</p>
<p>(1) điện do tuabin gió phát ra;</p>
<p>(2) điện do nhà máy thuỷ điện phát ra;</p>
<p>(3) nhiệt toả ra khi đốt củi;</p>
<p>(4) điện do nhà máy nhiệt điện than phát ra.</p>
<p>b) Phân loại tám nguồn năng lượng: gió, than đá, thuỷ triều, địa nhiệt, sinh khối, dầu mỏ, urani, sóng biển theo hai tiêu chí: có nguồn gốc từ bức xạ Mặt Trời hay không; có phải năng lượng tái tạo hay không. Trình bày thành bảng.</p>
<p>c) Sóng biển và thuỷ triều đều là chuyển động của nước biển. Vì sao phải xếp chúng vào hai ô khác nhau ở câu b)?</p>""",
  r"""<p>a) (1) Bức xạ Mặt Trời → nhiệt làm nóng không khí không đều → động năng của gió → cơ năng của cánh quạt tuabin → điện năng.</p>
<p>(2) Bức xạ Mặt Trời → nhiệt làm nước bốc hơi → hơi nước bay lên, ngưng thành mây, mưa xuống vùng cao → thế năng của nước trong hồ chứa → động năng dòng nước → cơ năng tuabin → điện năng.</p>
<p>(3) Bức xạ Mặt Trời → quang hợp, tích trữ thành hoá năng trong gỗ → đốt củi → nhiệt năng.</p>
<p>(4) Bức xạ Mặt Trời → quang hợp của thực vật cổ → sinh khối bị chôn vùi hàng trăm triệu năm thành than (hoá năng) → đốt than, nhiệt làm nước thành hơi → cơ năng tuabin → điện năng.</p>
<p>b) Bảng phân loại:</p>
<table>
<tr><th>Nguồn</th><th>Gốc Mặt Trời?</th><th>Tái tạo?</th></tr>
<tr><td>Gió</td><td>Có</td><td>Có</td></tr>
<tr><td>Sóng biển</td><td>Có</td><td>Có</td></tr>
<tr><td>Sinh khối</td><td>Có</td><td>Có</td></tr>
<tr><td>Than đá</td><td>Có</td><td>Không</td></tr>
<tr><td>Dầu mỏ</td><td>Có</td><td>Không</td></tr>
<tr><td>Thuỷ triều</td><td>Không</td><td>Có</td></tr>
<tr><td>Địa nhiệt</td><td>Không</td><td>Có</td></tr>
<tr><td>Urani</td><td>Không</td><td>Không</td></tr>
</table>
<p>c) Sóng biển do gió thổi trên mặt biển, mà gió có gốc từ bức xạ Mặt Trời.</p>
<p>Thuỷ triều do lực hấp dẫn của Mặt Trăng (và Mặt Trời) kết hợp với chuyển động tự quay của Trái Đất, không do bức xạ Mặt Trời.</p>
<p>Lỗi hay gặp: viết "mọi nguồn năng lượng đều từ Mặt Trời" — có ba ngoại lệ: địa nhiệt, hạt nhân (urani), thuỷ triều.</p>
<p>Lỗi hay gặp: xếp than, dầu vào "không có gốc Mặt Trời" vì quên chúng là năng lượng Mặt Trời được thực vật cổ tích trữ.</p>"""),

 # ── Bài 2 · Dễ: công suất bức xạ Mặt Trời tới Sao Hoả (khác ví dụ Trái Đất trong lý thuyết)
 ("Dễ", r"""<p>Sao Hoả ở xa Mặt Trời hơn Trái Đất. Ở rìa khí quyển Sao Hoả, bức xạ Mặt Trời chiếu vuông góc lên mỗi mét vuông với công suất khoảng $I=590\ \text{W/m}^2$. Coi chùm tia Mặt Trời tới Sao Hoả là chùm song song; bán kính Sao Hoả $R=3390\ \text{km}$. Để so sánh: toàn bộ loài người hiện tiêu thụ năng lượng với công suất trung bình khoảng $2{,}0\cdot10^{13}\ \text{W}$. Một năm có $365$ ngày.</p>
<p>a) Tính công suất bức xạ Mặt Trời chiếu tới Sao Hoả (ngay ngoài khí quyển).</p>
<p>b) Công suất đó gấp bao nhiêu lần công suất loài người tiêu thụ?</p>
<p>c) Năng lượng loài người dùng trong một năm, Mặt Trời gửi tới Sao Hoả trong bao lâu?</p>
<p>d) Khoảng $25\,\%$ bức xạ tới bị Sao Hoả phản xạ ngược về vũ trụ, phần còn lại được hấp thụ. Tính trung bình mỗi mét vuông của quả cầu Sao Hoả (tính chung ngày và đêm, mọi vĩ độ) hấp thụ công suất bao nhiêu.</p>
<p>e) Ở Trái Đất, con số tương ứng với $I$ là $1360\ \text{W/m}^2$. Giải thích định tính vì sao ở Sao Hoả nhỏ hơn nhiều.</p>""",
  r"""<p>a) Chùm tia song song bị Sao Hoả chặn lại đúng bằng phần đi qua một hình tròn bán kính $R$ (hình chiếu của hành tinh), không phải cả mặt cầu.</p>
<p>$S=\pi R^2=\pi\cdot(3{,}39\cdot10^6)^2\approx3{,}61\cdot10^{13}\ \text{m}^2$.</p>
<p>$P=IS\approx590\cdot3{,}61\cdot10^{13}\approx2{,}13\cdot10^{16}\ \text{W}$.</p>
<p>b) $\dfrac{2{,}13\cdot10^{16}}{2{,}0\cdot10^{13}}\approx1065$ lần.</p>
<p>c) Năng lượng loài người dùng một năm: $A=2{,}0\cdot10^{13}\cdot365\cdot86\,400\approx6{,}31\cdot10^{20}\ \text{J}$.</p>
<p>Thời gian: $t=\dfrac{A}{P}=\dfrac{365\cdot86\,400}{1065}\approx2{,}96\cdot10^4\ \text{s}\approx8{,}2$ giờ.</p>
<p>d) Công suất hấp thụ $0{,}75P$ được chia đều trên toàn mặt cầu $4\pi R^2$:</p>
<p>$\dfrac{0{,}75\,I\,\pi R^2}{4\pi R^2}=\dfrac{0{,}75\cdot590}{4}\approx111\ \text{W/m}^2$.</p>
<p>e) Năng lượng Mặt Trời phát ra mỗi giây toả đều ra mọi phía; càng xa Mặt Trời, cùng năng lượng đó trải trên mặt cầu càng lớn nên mỗi mét vuông nhận càng ít. Sao Hoả xa Mặt Trời khoảng $1{,}5$ lần Trái Đất nên mỗi mét vuông chỉ nhận chưa tới một nửa ($1360:590\approx2{,}3$ lần).</p>
<p>Lỗi hay gặp ở a): dùng diện tích mặt cầu $4\pi R^2$, ra $8{,}5\cdot10^{16}\ \text{W}$ (gấp 4 lần) — nửa hành tinh là ban đêm, nửa còn lại phần lớn bị chiếu xiên.</p>
<p>Lỗi hay gặp: quên đổi $3390\ \text{km}$ ra mét.</p>"""),

 # ── Bài 3 · Trung bình: thay đèn tiết kiệm → than và CO₂ ở nhà máy
 ("Trung bình", r"""<p>Một trường học thay $120$ bóng đèn ống huỳnh quang $40\ \text{W}$ bằng $120$ bóng đèn LED $18\ \text{W}$ sáng tương đương. Mỗi ngày đèn bật $8$ giờ, mỗi tháng học $22$ ngày; coi các đèn hoạt động đúng công suất định mức.</p>
<p>Điện của trường do một nhà máy nhiệt điện than có hiệu suất $36\,\%$ cung cấp; bỏ qua hao phí trên đường dây tải điện. Than có năng suất toả nhiệt $q=2{,}7\cdot10^7\ \text{J/kg}$; cứ đốt $1\ \text{kg}$ than thì thải ra $2{,}5\ \text{kg}$ khí CO₂. Đơn giá điện của trường là $2900$ đồng/kWh (một giá cố định).</p>
<p>a) Mỗi tháng trường tiết kiệm được bao nhiêu kWh điện?</p>
<p>b) Nhờ đó nhà máy bớt đốt bao nhiêu kilôgam than và bớt thải bao nhiêu kilôgam CO₂ mỗi tháng?</p>
<p>c) Mỗi tháng trường bớt bao nhiêu tiền điện? Một năm học $9$ tháng tiết kiệm bao nhiêu kWh?</p>
<p>d) Cùng độ sáng mà đèn LED tốn ít điện hơn. Giải thích bằng hiệu suất chuyển hoá năng lượng.</p>""",
  r"""<p>a) Mỗi bóng giảm $40-18=22\ \text{W}=0{,}022\ \text{kW}$.</p>
<p>$\Delta A=120\cdot0{,}022\cdot8\cdot22=464{,}64\ \text{kWh}$ mỗi tháng.</p>
<p>b) Đổi ra jun: $464{,}64\cdot3{,}6\cdot10^6\approx1{,}673\cdot10^9\ \text{J}$.</p>
<p>Ở nhà máy, nhiệt than toả ra phải lớn hơn điện năng: $Q=\dfrac{\Delta A}{H}=\dfrac{1{,}673\cdot10^9}{0{,}36}\approx4{,}646\cdot10^9\ \text{J}$.</p>
<p>$m=\dfrac{Q}{q}=\dfrac{4{,}646\cdot10^9}{2{,}7\cdot10^7}\approx172{,}1\ \text{kg}$ than.</p>
<p>$m_{CO_2}=2{,}5\cdot172{,}1\approx430\ \text{kg}$ CO₂.</p>
<p>c) Tiền: $464{,}64\cdot2900\approx1\,347\,000$ đồng mỗi tháng.</p>
<p>Năm học: $464{,}64\cdot9\approx4182\ \text{kWh}$.</p>
<p>d) Cả hai đèn đều biến điện năng thành quang năng (có ích) và nhiệt năng (hao phí).</p>
<p>Đèn LED có hiệu suất phát sáng cao hơn: phần điện năng biến thành nhiệt ít hơn, nên để cho cùng một lượng ánh sáng nó cần điện năng toàn phần nhỏ hơn.</p>
<p>Lỗi hay gặp ở b): nhân với $H$ ($\Delta A\cdot0{,}36$) thay vì chia — nhiệt toàn phần ở nhà máy phải lớn hơn điện năng có ích.</p>
<p>Lỗi hay gặp: tính tiết kiệm bằng $120\cdot18$ W (công suất đèn mới) thay vì hiệu $40-18$.</p>"""),

 # ── Bài 4 · Trung bình: thuỷ điện tích năng
 ("Trung bình", r"""<p>Một nhà máy thuỷ điện tích năng có hồ trên cao hơn hồ dưới $h=300\ \text{m}$. Ban đêm, khi lưới điện thừa điện, máy bơm đưa $3{,}6\cdot10^6\ \text{m}^3$ nước từ hồ dưới lên hồ trên với hiệu suất bơm $85\,\%$. Ban ngày, toàn bộ lượng nước đó được xả qua tuabin để phát điện, hiệu suất phát (tuabin và máy phát) $88\,\%$.</p>
<p>Coi độ chênh mực nước $300\ \text{m}$ không đổi trong suốt quá trình; trọng lượng riêng của nước $d=10\,000\ \text{N/m}^3$; bỏ qua hao phí trên đường dây tải điện.</p>
<p>a) Tính phần thế năng mà nước nhận thêm sau khi bơm (đơn vị J và MWh).</p>
<p>b) Tính điện năng tiêu thụ để bơm, điện năng phát lại ban ngày và hiệu suất của cả chu trình bơm – phát.</p>
<p>c) Nếu xả đều trong $6$ giờ thì công suất điện trung bình và lưu lượng nước qua tuabin là bao nhiêu?</p>
<p>d) Cả chu trình "lỗ" khoảng một phần tư điện năng. Vì sao người ta vẫn xây nhà máy loại này? Nêu hai lí do.</p>""",
  r"""<p>a) Trọng lượng nước được bơm: $P=dV=10^4\cdot3{,}6\cdot10^6=3{,}6\cdot10^{10}\ \text{N}$.</p>
<p>Thế năng tăng: $W_t=Ph=3{,}6\cdot10^{10}\cdot300=1{,}08\cdot10^{13}\ \text{J}$.</p>
<p>Đổi: $\dfrac{1{,}08\cdot10^{13}}{3{,}6\cdot10^6}=3\cdot10^6\ \text{kWh}=3000\ \text{MWh}$.</p>
<p>b) Thế năng là phần có ích của máy bơm: $A_{bơm}=\dfrac{W_t}{H_{bơm}}=\dfrac{3000}{0{,}85}\approx3529\ \text{MWh}$.</p>
<p>Khi phát, thế năng là phần toàn phần: $A_{phát}=H_{phát}W_t=0{,}88\cdot3000=2640\ \text{MWh}$.</p>
<p>Hiệu suất chu trình: $H=H_{bơm}H_{phát}=0{,}85\cdot0{,}88=0{,}748=74{,}8\,\%$ (kiểm tra: $\dfrac{2640}{3529}\approx0{,}748$).</p>
<p>c) $P_đ=\dfrac{2640\ \text{MWh}}{6\ \text{h}}=440\ \text{MW}$.</p>
<p>$L=\dfrac{V}{t}=\dfrac{3{,}6\cdot10^6}{6\cdot3600}\approx166{,}7\ \text{m}^3/\text{s}$.</p>
<p>d) Điện ban đêm đang thừa: nhà máy nhiệt điện than, điện hạt nhân không giảm công suất nhanh được, nên điện đêm rẻ; trữ lại để dùng lúc cao điểm ban ngày, khi điện thiếu và đắt.</p>
<p>Tuabin thuỷ điện khởi động trong vài phút, bù kịp lúc lưới điện thiếu đột ngột; hồ chứa giống một "acquy khổng lồ", giúp dùng được nhiều hơn điện gió, điện Mặt Trời vốn lúc thừa lúc thiếu.</p>
<p>Lỗi hay gặp: tính điện bơm bằng $0{,}85\cdot3000$ (nhân thay vì chia) — máy bơm phải tiêu thụ nhiều hơn thế năng nó tạo ra.</p>
<p>Lỗi hay gặp: lấy hiệu suất chu trình bằng trung bình cộng $\dfrac{85+88}{2}\,\%$.</p>"""),

 # ── Bài 5 · Khó: điện hạt nhân so với nhiệt điện than
 ("Khó", r"""<p>Một nhà máy điện hạt nhân có công suất điện $1000\ \text{MW}$, hiệu suất $33\,\%$, chạy liên tục đủ $365$ ngày. Biết $1\ \text{g}$ U-235 phân hạch hết toả ra khoảng $8{,}2\cdot10^{10}\ \text{J}$. Bỏ qua hao phí trên đường dây tải điện.</p>
<p>a) Tính điện năng nhà máy phát ra trong một năm và năng lượng nhiên liệu hạt nhân cần cung cấp.</p>
<p>b) Mỗi năm nhà máy cần bao nhiêu kilôgam U-235 phân hạch?</p>
<p>c) Một nhà máy nhiệt điện than hiệu suất $36\,\%$ phát cùng lượng điện năng đó. Than có $q=2{,}7\cdot10^7\ \text{J/kg}$, mỗi kilôgam than cháy thải $2{,}5\ \text{kg}$ CO₂. Tính khối lượng than đốt và CO₂ thải ra mỗi năm. Khối lượng than gấp bao nhiêu lần khối lượng U-235 ở câu b)?</p>
<p>d) Nêu hai ưu điểm và hai nhược điểm của điện hạt nhân. Vì sao năng lượng hạt nhân không được xếp vào năng lượng tái tạo? Nhà máy điện hạt nhân dùng phản ứng phân hạch hay nhiệt hạch, hai phản ứng đó khác nhau thế nào?</p>""",
  r"""<p>a) $t=365\cdot86\,400=3{,}1536\cdot10^7\ \text{s}$.</p>
<p>Điện năng: $A=P_đt=10^9\cdot3{,}1536\cdot10^7\approx3{,}15\cdot10^{16}\ \text{J}$.</p>
<p>Năng lượng nhiên liệu: $E=\dfrac{A}{H}=\dfrac{3{,}1536\cdot10^{16}}{0{,}33}\approx9{,}56\cdot10^{16}\ \text{J}$.</p>
<p>b) $m_U=\dfrac{9{,}56\cdot10^{16}}{8{,}2\cdot10^{10}}\approx1{,}165\cdot10^6\ \text{g}\approx1165\ \text{kg}$ — khoảng $1{,}2$ tấn mỗi năm.</p>
<p>c) Nhiệt than toả: $Q=\dfrac{A}{0{,}36}\approx8{,}76\cdot10^{16}\ \text{J}$.</p>
<p>$m_{than}=\dfrac{Q}{q}\approx3{,}24\cdot10^9\ \text{kg}\approx3{,}24$ triệu tấn.</p>
<p>$m_{CO_2}=2{,}5\cdot3{,}24\cdot10^9\approx8{,}11\cdot10^9\ \text{kg}\approx8{,}11$ triệu tấn.</p>
<p>Tỉ số: $\dfrac{3{,}24\cdot10^9}{1165}\approx2{,}8\cdot10^6$ — than nặng gấp khoảng $2{,}8$ triệu lần.</p>
<p>(Riêng về nhiên liệu, $1\ \text{g}$ U-235 toả bằng khoảng $3$ tấn than; tỉ số ở đây nhỏ hơn $3$ triệu một chút vì nhà máy than có hiệu suất cao hơn: $36\,\%$ so với $33\,\%$.)</p>
<p>d) Ưu điểm: khi vận hành không thải CO₂; nhiên liệu cực gọn (hơn một tấn mỗi năm thay cho hàng triệu tấn than), phát điện ổn định ngày đêm.</p>
<p>Nhược điểm: chất thải phóng xạ phải cất giữ an toàn rất lâu; nguy cơ sự cố gây ô nhiễm phóng xạ; vốn xây dựng lớn.</p>
<p>Không tái tạo vì urani là khoáng chất có hạn trong vỏ Trái Đất, dùng tới đâu hết tới đó, tự nhiên không bổ sung lại.</p>
<p>Nhà máy dùng phân hạch: hạt nhân nặng (U-235) hấp thụ nơtron rồi vỡ thành hai hạt nhân nhẹ hơn và vài nơtron, toả năng lượng; phản ứng dây chuyền được điều khiển trong lò.</p>
<p>Nhiệt hạch là các hạt nhân nhẹ (hiđrô) kết hợp thành hạt nhân nặng hơn (heli) ở nhiệt độ hàng chục triệu độ — xảy ra trong lõi Mặt Trời, chưa dùng phát điện thương mại.</p>
<p>Lỗi hay gặp: dùng $1000\ \text{MW}$ làm công suất nhiên liệu (quên chia $H$), ra $385\ \text{kg}$ U-235.</p>
<p>Lỗi hay gặp: nói nhà máy "đốt" urani — không có sự cháy, năng lượng đến từ biến đổi hạt nhân.</p>"""),

 # ── Bài 6 · Nâng cao: hệ điện lai cho một đảo
 ("Nâng cao", r"""<p>Một đảo nhỏ có $200$ hộ, trung bình mỗi hộ dùng $5\ \text{kWh}$ điện mỗi ngày. Hệ điện của đảo gồm:</p>
<p>• một tuabin gió có công suất định mức $100\ \text{kW}$ tại tốc độ gió $12\ \text{m/s}$, bắt đầu quay khi gió từ $3\ \text{m/s}$; khi gió từ $3$ đến dưới $12\ \text{m/s}$ thì công suất tỉ lệ với lập phương tốc độ gió;</p>
<p>• một dàn pin Mặt Trời hiệu suất $19\,\%$, nối qua biến tần hiệu suất $95\,\%$; ở đảo, mỗi ngày tương đương $4{,}5$ giờ nắng đỉnh với cường độ bức xạ $1000\ \text{W/m}^2$;</p>
<p>• một dàn acquy và một máy phát điện chạy dầu diesel dự phòng.</p>
<p>Điện năng gió và pin phát ra trong ngày: $60\,\%$ được dùng ngay, $40\,\%$ phải nạp vào acquy rồi mới dùng vào ban đêm; hiệu suất nạp – xả của acquy là $85\,\%$. Bỏ qua hao phí trên đường dây tải điện và mọi hao phí khác.</p>
<p>a) Hôm khảo sát có $10$ giờ gió $6\ \text{m/s}$ và $14$ giờ gió $9\ \text{m/s}$. Tính điện năng tuabin gió phát ra trong ngày.</p>
<p>b) Để các hộ nhận đủ điện, gió và pin phải phát ra tổng cộng bao nhiêu kWh mỗi ngày?</p>
<p>c) Với ngày gió như câu a), dàn pin phải có diện tích tối thiểu bao nhiêu mét vuông?</p>
<p>d) Một ngày lặng gió, trời u ám (coi gió và pin không phát điện), máy diesel chạy trực tiếp theo nhu cầu, không qua acquy. Máy có hiệu suất $35\,\%$; dầu có $q=4{,}4\cdot10^7\ \text{J/kg}$, khối lượng riêng $0{,}84\ \text{kg/L}$; đốt $1\ \text{kg}$ dầu thải $3{,}2\ \text{kg}$ CO₂. Tính khối lượng dầu, thể tích dầu và lượng CO₂ thải ra trong ngày đó.</p>""",
  r"""<p>a) Công suất theo lập phương tốc độ (cả $6$ và $9\ \text{m/s}$ đều trong khoảng $3$ đến dưới $12\ \text{m/s}$):</p>
<p>$P(6)=100\cdot\left(\dfrac{6}{12}\right)^3=12{,}5\ \text{kW}$.</p>
<p>$P(9)=100\cdot\left(\dfrac{9}{12}\right)^3\approx42{,}19\ \text{kW}$.</p>
<p>$A_{gió}=12{,}5\cdot10+42{,}1875\cdot14=125+590{,}6\approx715{,}6\ \text{kWh}$.</p>
<p>b) Nhu cầu: $E=200\cdot5=1000\ \text{kWh}$. Gọi $G$ là tổng điện năng gió và pin phát ra.</p>
<p>Phần dùng ngay: $0{,}6G$. Phần qua acquy chỉ còn $0{,}4G\cdot0{,}85=0{,}34G$.</p>
<p>$0{,}6G+0{,}34G=1000$ nên $G=\dfrac{1000}{0{,}94}\approx1063{,}8\ \text{kWh}$.</p>
<p>c) Pin phải phát: $1063{,}8-715{,}6\approx348{,}2\ \text{kWh}$.</p>
<p>Mỗi mét vuông pin mỗi ngày cho: $0{,}19\cdot1\ \text{kW}\cdot4{,}5\ \text{h}\cdot0{,}95\approx0{,}812\ \text{kWh}$.</p>
<p>$S=\dfrac{348{,}2}{0{,}812}\approx428{,}7\ \text{m}^2$, làm tròn lên: tối thiểu khoảng $429\ \text{m}^2$.</p>
<p>d) Điện năng: $1000\ \text{kWh}=3{,}6\cdot10^9\ \text{J}$. Nhiệt dầu toả: $Q=\dfrac{3{,}6\cdot10^9}{0{,}35}\approx1{,}029\cdot10^{10}\ \text{J}$.</p>
<p>$m=\dfrac{Q}{q}\approx233{,}8\ \text{kg}$.</p>
<p>$V=\dfrac{233{,}8}{0{,}84}\approx278\ \text{L}$.</p>
<p>$m_{CO_2}=3{,}2\cdot233{,}8\approx748\ \text{kg}$.</p>
<p>Lỗi hay gặp ở a): dùng bình phương tốc độ gió (ra $25$ và $56{,}25\ \text{kW}$).</p>
<p>Lỗi hay gặp ở b): chia cả $1000\ \text{kWh}$ cho $0{,}85$ (ra $1176\ \text{kWh}$) — chỉ phần đi qua acquy mới chịu hao phí.</p>
<p>Lỗi hay gặp ở c): lấy cả ngày $12$ giờ trời sáng thay cho $4{,}5$ giờ nắng đỉnh.</p>"""),
]


def tu_luan():
    parts = []
    for k, (muc, de, gi) in enumerate(TL, 1):
        parts.append(f"<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>{gi}</details>")
    return dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
                body_html="<p>Các bài còn lại của chuyên đề, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>"
                          + "".join(parts))


def kiem_so():
    KWH, NGAY = 3.6e6, 86400
    NAM = 365 * NGAY
    r = lambda x, n=0: round(x, n)
    # Bài 2 (Sao Hoả)
    I0, R = 590, 3.39e6
    S = pi * R ** 2
    P = I0 * S
    assert r(S / 1e13, 2) == 3.61 and r(P / 1e16, 2) == 2.13
    k = P / 2.0e13; assert r(k) == 1065
    A_nguoi = 2.0e13 * NAM; assert r(A_nguoi / 1e20, 2) == 6.31
    t = A_nguoi / P; assert r(t / 1e4, 2) == 2.96 and r(t / 3600, 1) == 8.2
    assert r(I0 * 4 * pi * R ** 2 / 1e16, 1) == 8.5
    assert r(0.75 * P / (4 * pi * R ** 2)) == 111 and r(1360 / 590, 1) == 2.3
    # Bài 3
    dA = 120 * (0.040 - 0.018) * 8 * 22; assert isclose(dA, 464.64)
    J = dA * KWH; assert r(J / 1e9, 3) == 1.673
    Q3 = J / 0.36; assert r(Q3 / 1e9, 3) == 4.646
    m3 = Q3 / 2.7e7; assert r(m3, 1) == 172.1 and r(2.5 * m3) == 430
    assert r(dA * 2900, -3) == 1347000 and r(dA * 9) == 4182
    # Bài 4
    V, h = 3.6e6, 300
    W = 1e4 * V * h; assert isclose(W, 1.08e13) and isclose(W / KWH / 1e3, 3000)
    Ab = 3000 / 0.85; Ap = 0.88 * 3000
    assert r(Ab) == 3529 and isclose(Ap, 2640) and isclose(0.85 * 0.88, 0.748) and r(Ap / Ab, 3) == 0.748
    assert isclose(Ap / 6, 440) and r(V / (6 * 3600), 1) == 166.7
    # Bài 5
    A5 = 1e9 * NAM; assert isclose(A5, 3.1536e16)
    E5 = A5 / 0.33; assert r(E5 / 1e16, 2) == 9.56
    mU = E5 / 8.2e10 / 1e3; assert r(mU) == 1165
    Qt = A5 / 0.36; assert r(Qt / 1e16, 2) == 8.76
    mt = Qt / 2.7e7; assert r(mt / 1e9, 2) == 3.24 and r(2.5 * mt / 1e9, 2) == 8.11
    assert r(mt / mU / 1e6, 1) == 2.8 and r(8.2e10 * 1e3 / 2.7e7 / 1e6, 2) == 3.04   # 1 g U ≈ 3037 kg than
    assert r(1e9 * NAM / 8.2e10 / 1e3) == 385                                           # bẫy quên chia H
    # Bài 6
    Pw = lambda v: 100 * (v / 12) ** 3
    assert 3 <= 6 < 12 and 3 <= 9 < 12
    assert isclose(Pw(6), 12.5) and r(Pw(9), 2) == 42.19
    Ag = 10 * Pw(6) + 14 * Pw(9); assert r(14 * Pw(9), 1) == 590.6 and r(Ag, 1) == 715.6
    G = 1000 / (0.6 + 0.4 * 0.85); assert isclose(0.6 + 0.4 * 0.85, 0.94) and r(G, 1) == 1063.8
    Ap6 = G - Ag; assert r(Ap6, 1) == 348.2
    a = 0.19 * 1 * 4.5 * 0.95; assert r(a, 3) == 0.812
    S6 = Ap6 / a; assert r(S6, 1) == 428.7 and ceil(S6) == 429
    Qd = 1000 * KWH / 0.35; assert r(Qd / 1e10, 3) == 1.029
    md = Qd / 4.4e7; assert r(md, 1) == 233.8 and r(md / 0.84) == 278 and r(3.2 * md) == 748
    assert isclose(100 * 0.25, 25) and isclose(100 * 0.5625, 56.25) and r(1000 / 0.85) == 1176   # các bẫy
    print("kiểm số liệu tự luận 163: đạt")


if __name__ == "__main__":
    kiem_so()
    print(len(tu_luan()["body_html"]))
