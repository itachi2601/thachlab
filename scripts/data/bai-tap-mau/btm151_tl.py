# -*- coding: utf-8 -*-
"""CĐ06 Khúc xạ ánh sáng, phản xạ toàn phần, lăng kính và tán sắc (lesson 151) — Bài tập tự luận (xếp từ dễ đến khó).
Xuất tu_luan() (dict label + body_html) và kiem_so() (assert mọi đáp số).
Tự soạn 17/10/2026 theo dàn ý content/hsg9/cd06-khuc-xa-phan-xa-toan-phan/nguon.md (mục Tự luận), phỏng theo kiểu đề
HSG 9 / tuyển sinh 10 chuyên phổ biến, không chép đề cụ thể nào. Số liệu khác 7 dạng mẫu (151.json) và khác ví dụ docx.
Quy ước: mọi góc đo so với PHÁP TUYẾN; không khí n = 1, nước n = 4/3, c = 3.10^8 m/s. Không dùng góc Brewster."""
from fractions import Fraction as F
from math import sin, cos, tan, asin, radians, degrees, sqrt, isclose

TL = [
 # ── Bài 1 · Dễ: đồng xu dưới đáy cốc
 ("Dễ", r"""<p>Một đồng xu nằm ở đáy cốc thuỷ tinh đựng nước, mực nước cao $12\ \text{cm}$. Cho chiết suất của nước $n=\dfrac43$, của không khí là $1$; bỏ qua bề dày đáy cốc.</p>
<p>a) Nhìn đồng xu theo phương gần vuông góc với mặt nước, đồng xu trông như nằm cách mặt nước bao nhiêu? Đồng xu trông như được nâng lên bao nhiêu?</p>
<p>b) Đặt một chiếc cốc rỗng có đồng xu ở đáy trên bàn, lùi mắt dần cho tới khi thành cốc vừa che khuất đồng xu. Giữ yên mắt rồi rót nước vào cốc thì lại nhìn thấy đồng xu. Vẽ đường truyền một tia sáng từ đồng xu tới mắt và giải thích.</p>""",
  r"""<p>a) Nhìn gần vuông góc với mặt nước, ảnh của đồng xu cách mặt nước:</p>
<p>$h'=\dfrac hn=\dfrac{12}{4/3}=9{,}0\ \text{cm}$.</p>
<p>Đồng xu trông như được nâng lên $12-9=3\ \text{cm}$.</p>
<p>b) Khi cốc rỗng, tia sáng từ đồng xu đi thẳng tới mắt bị thành cốc chắn.</p>
<p>Khi có nước, tia sáng từ đồng xu tới mặt nước rồi đi ra không khí (môi trường chiết quang kém hơn) nên bị lệch xa pháp tuyến, tức là ngả xuống phía mép cốc.</p>
<p>Tia ló đó vượt qua mép cốc và tới được mắt; mắt nhìn theo đường kéo dài của tia ló nên thấy ảnh đồng xu cao hơn vị trí thật.</p>
<p>Lỗi hay gặp: nhân thay vì chia, ra $h'=16\ \text{cm}$ — ảnh phải dịch về phía môi trường chiết quang kém (lên gần mặt nước).</p>
<p>Lỗi hay gặp: vẽ tia sáng đi từ mắt tới đồng xu rồi kết luận "mắt phát ra tia sáng".</p>"""),

 # ── Bài 2 · Dễ: màu sắc của vật, tấm lọc màu, trộn ánh sáng
 ("Dễ", r"""<p>Trong phòng tối có một chiếc áo trắng, một chiếc lá cây xanh lục và một tờ giấy trắng in chữ màu đỏ. Lần lượt chiếu sáng chúng bằng đèn chỉ phát ánh sáng đỏ, rồi bằng đèn chỉ phát ánh sáng lục. Bỏ qua ánh sáng từ nguồn khác.</p>
<p>a) Dưới mỗi đèn, áo, lá và chữ trông có màu gì? Dưới đèn nào thì khó đọc chữ đỏ trên giấy trắng nhất?</p>
<p>b) Dưới ánh sáng trắng, nhìn chiếc lá qua một tấm kính lọc màu đỏ thì lá trông màu gì? Vì sao?</p>
<p>c) Chiếu đồng thời một đèn đỏ và một đèn lục vào cùng một chỗ trên bức tường trắng thì chỗ đó có màu gì? Một bạn nói "đỏ trộn lục ra màu nâu như khi pha màu vẽ" — đúng hay sai?</p>
<p>d) Giải thích vì sao các điểm ảnh trên màn hình điện thoại chỉ cần ba màu đỏ, lục, lam mà vẫn hiện được rất nhiều màu, kể cả màu trắng.</p>""",
  r"""<p>Quy tắc: vật có màu nào thì hắt lại mạnh ánh sáng màu đó và hấp thụ phần lớn các màu khác; vật trắng hắt lại mọi màu; vật đen hấp thụ gần hết.</p>
<p>a) Dưới đèn đỏ: áo trắng hắt lại ánh sáng đỏ nên trông đỏ.</p>
<p>Lá xanh lục hấp thụ ánh sáng đỏ nên trông gần như đen.</p>
<p>Chữ đỏ trông đỏ, nền giấy cũng trông đỏ: chữ gần như lẫn vào nền, rất khó đọc.</p>
<p>Dưới đèn lục: áo trông lục, lá trông lục.</p>
<p>Chữ đỏ hấp thụ ánh sáng lục nên trông gần như đen trên nền lục, đọc rõ.</p>
<p>Vậy khó đọc nhất là dưới đèn đỏ.</p>
<p>b) Lá hắt lại chủ yếu ánh sáng lục; tấm lọc đỏ chỉ cho ánh sáng đỏ đi qua, hấp thụ ánh sáng lục. Rất ít ánh sáng từ lá tới được mắt nên lá trông gần như đen (tối sẫm).</p>
<p>c) Chỗ đó có màu vàng. Bạn kia sai: trộn <em>ánh sáng</em> là cộng thêm ánh sáng vào mắt, còn pha <em>màu vẽ</em> là mỗi chất màu hấp thụ bớt ánh sáng, nên kết quả khác nhau.</p>
<p>d) Mỗi điểm ảnh gồm ba điểm nhỏ đỏ, lục, lam đặt sát nhau, mắt không phân biệt được nên thấy màu trộn của chúng.</p>
<p>Thay đổi độ sáng từng điểm sẽ cho các màu trộn khác nhau: đỏ + lục ra vàng, đỏ + lam ra đỏ tím, lục + lam ra lam lục; cả ba cùng sáng mạnh như nhau thì ra trắng.</p>
<p>Lỗi hay gặp: nói "dưới đèn đỏ, lá vẫn xanh vì lá có màu xanh" — vật không tự phát ra màu, chỉ hắt lại phần ánh sáng chiếu tới nó.</p>"""),

 # ── Bài 3 · Trung bình: thời gian truyền và chiết suất
 ("Trung bình", r"""<p>Một xung ánh sáng laser đi được quãng đường $3\ \text{m}$. Cho tốc độ ánh sáng trong không khí xấp xỉ trong chân không $c=3\cdot10^8\ \text{m/s}$, chiết suất của nước $n=\dfrac43$.</p>
<p>a) Tính tốc độ ánh sáng trong nước.</p>
<p>b) Tính thời gian xung đi hết $3\ \text{m}$ trong nước và $3\ \text{m}$ trong không khí.</p>
<p>c) Trong khoảng thời gian xung đi hết $3\ \text{m}$ nước, nếu đi trong không khí thì nó đi được bao xa? Nhận xét mối liên hệ giữa kết quả và chiết suất.</p>""",
  r"""<p>a) $v=\dfrac cn=\dfrac{3\cdot10^8}{4/3}=2{,}25\cdot10^8\ \text{m/s}$.</p>
<p>b) Trong nước: $t_1=\dfrac{3}{2{,}25\cdot10^8}\approx1{,}33\cdot10^{-8}\ \text{s}=13{,}3\ \text{ns}$.</p>
<p>Trong không khí: $t_2=\dfrac{3}{3\cdot10^8}=1{,}0\cdot10^{-8}\ \text{s}=10{,}0\ \text{ns}$.</p>
<p>c) $s=c\,t_1=3\cdot10^8\cdot\dfrac{3}{2{,}25\cdot10^8}=4{,}0\ \text{m}$.</p>
<p>Nhận xét: $s=n\cdot3\ \text{m}$ — đi $1\ \text{m}$ trong môi trường chiết suất $n$ mất thời gian bằng đi $n$ mét trong không khí.</p>
<p>Lỗi hay gặp: viết $v=n\,c$, ra tốc độ lớn hơn $c$ — chiết suất càng lớn thì ánh sáng càng chậm.</p>
<p>Lỗi hay gặp: quên đổi $1\ \text{ns}=10^{-9}\ \text{s}$.</p>"""),

 # ── Bài 4 · Trung bình: nhìn cá theo phương xiên
 ("Trung bình", r"""<p>Một con cá nhỏ (coi như một điểm) ở độ sâu $0{,}6\ \text{m}$ dưới mặt nước phẳng lặng. Một người đứng trên bờ nhìn thấy cá nhờ một tia sáng từ cá ló ra không khí với góc khúc xạ $r$ thoả mãn $\sin r=0{,}8$. Chiết suất của nước $n=\dfrac43$. Coi ảnh của cá mà người thấy là giao điểm của đường kéo dài tia ló (về phía nước) với đường thẳng đứng đi qua cá.</p>
<p>a) Tính góc tới $i$ của tia sáng ở mặt nước (góc so với pháp tuyến).</p>
<p>b) Điểm ló của tia sáng cách điểm trên mặt nước ở ngay phía trên cá bao xa?</p>
<p>c) Ảnh của cá ở độ sâu bao nhiêu? So sánh với độ sâu ảnh khi nhìn gần vuông góc với mặt nước.</p>
<p>d) Người đâm cá đứng trên bờ, nhắm theo hướng nhìn thấy cá. Muốn trúng thì phải phóng lao thấp hơn hay cao hơn chỗ nhìn thấy? Nhìn càng xiên thì sai lệch tăng hay giảm?</p>""",
  r"""<p>a) Tia đi từ nước ra không khí: $n\sin i=1\cdot\sin r$ nên $\sin i=\dfrac{0{,}8}{4/3}=0{,}6$, $i\approx36{,}9^\circ$.</p>
<p>b) Gọi $H$ là điểm trên mặt nước ngay phía trên cá, $I$ là điểm ló. Trong tam giác vuông tạo bởi cá, $H$, $I$:</p>
<p>$HI=h\tan i=0{,}6\cdot\dfrac{0{,}6}{0{,}8}=0{,}45\ \text{m}$ (vì $\cos i=0{,}8$).</p>
<p>c) Đường kéo dài tia ló hợp với pháp tuyến góc $r$, với $\cos r=0{,}6$, $\tan r=\dfrac43$.</p>
<p>Ảnh $S'$ nằm trên đường thẳng đứng qua cá: $HS'=\dfrac{HI}{\tan r}=\dfrac{0{,}45}{4/3}\approx0{,}338\ \text{m}$.</p>
<p>Nhìn gần vuông góc: $h'=\dfrac hn=\dfrac{0{,}6}{4/3}=0{,}45\ \text{m}$.</p>
<p>Nhìn xiên, cá trông còn <em>nông hơn nữa</em> ($0{,}338\ \text{m}\lt0{,}45\ \text{m}$).</p>
<p>d) Cá thật ở sâu hơn ảnh nên phải phóng lao thấp hơn chỗ nhìn thấy. Nhìn càng xiên thì ảnh càng nông, sai lệch càng lớn.</p>
<p>Lỗi hay gặp: dùng công thức $h'=\dfrac hn$ cho trường hợp nhìn xiên — công thức đó chỉ đúng khi nhìn gần vuông góc.</p>
<p>Lỗi hay gặp: viết $\sin i=n\sin r$ (đặt $n$ sai bên), ra $\sin i\gt1$.</p>"""),

 # ── Bài 5 · Trung bình: bóng cọc dưới đáy bể
 ("Trung bình", r"""<p>Một bể nước có đáy phẳng nằm ngang, đầy nước tới độ sâu $0{,}8\ \text{m}$. Một cây cọc dài $1{,}2\ \text{m}$ cắm thẳng đứng, chân cọc chạm đáy bể. Ánh nắng (coi là chùm tia song song) chiếu tới mặt nước với góc tới $60^\circ$. Chiết suất của nước $n=\dfrac43$; bể đủ rộng, mặt nước phẳng lặng; bỏ qua ánh sáng phản xạ.</p>
<p>a) Vẽ đường truyền của tia sáng đi sát đỉnh cọc. Tính góc khúc xạ của nó trong nước.</p>
<p>b) Tính chiều dài bóng của cọc trên đáy bể (tính từ chân cọc).</p>
<p>c) Nếu bể cạn hết nước thì bóng cọc trên đáy dài bao nhiêu? Vì sao có nước thì bóng ngắn hơn?</p>""",
  r"""<p>a) Phần cọc nhô khỏi mặt nước dài $1{,}2-0{,}8=0{,}4\ \text{m}$.</p>
<p>Tia sát đỉnh cọc gặp mặt nước tại điểm $I$, khúc xạ: $\sin r=\dfrac{\sin60^\circ}{4/3}=\dfrac{0{,}8660}{1{,}3333}\approx0{,}6495$, $r\approx40{,}5^\circ$.</p>
<p>b) Bóng của phần cọc trên mặt nước (trên mặt thoáng): $0{,}4\tan60^\circ\approx0{,}693\ \text{m}$ — đó là khoảng cách từ cọc tới $I$.</p>
<p>Từ $I$ xuống đáy, tia lệch thêm theo phương ngang: $0{,}8\tan40{,}5^\circ\approx0{,}683\ \text{m}$.</p>
<p>Bóng trên đáy dài $0{,}693+0{,}683\approx1{,}38\ \text{m}$.</p>
<p>c) Bể cạn: tia đi thẳng, bóng dài $1{,}2\tan60^\circ\approx2{,}08\ \text{m}$.</p>
<p>Có nước, tia sáng vào nước bị lệch gần pháp tuyến (dốc xuống hơn) nên tới đáy gần cọc hơn, bóng ngắn lại.</p>
<p>Lỗi hay gặp: dùng $\tan60^\circ$ cho cả đoạn trong nước, quên tia đã khúc xạ.</p>
<p>Lỗi hay gặp: lấy $60^\circ$ là góc giữa tia nắng và mặt nước — đề cho góc tới, đo so với pháp tuyến.</p>"""),

 # ── Bài 6 · Khó: bản kính dày
 ("Khó", r"""<p>Một tấm kính phẳng hai mặt song song, dày $e=4\ \text{cm}$, chiết suất $n=1{,}6$, đặt trong không khí. Chiếu một tia sáng hẹp tới mặt trên với góc tới $i=45^\circ$ (cho $\sin45^\circ\approx0{,}7071$).</p>
<p>a) Tính góc khúc xạ $r$ ở mặt trên. Chứng minh tia ló ra ở mặt dưới song song với tia tới.</p>
<p>b) Chứng minh độ dời ngang giữa tia ló và tia tới (khoảng cách giữa hai đường thẳng song song) là $d=\dfrac{e\sin(i-r)}{\cos r}$, rồi tính $d$.</p>
<p>c) Đặt tấm kính lên một trang sách, nhìn chữ theo phương gần vuông góc. Chữ trông gần mắt hơn bao nhiêu so với khi bỏ tấm kính đi?</p>""",
  r"""<p>a) $\sin r=\dfrac{\sin45^\circ}{1{,}6}=\dfrac{0{,}7071}{1{,}6}\approx0{,}4419$, $r\approx26{,}2^\circ$.</p>
<p>Hai mặt kính song song nên hai pháp tuyến song song; góc tới ở mặt dưới bằng $r$ (so le trong).</p>
<p>Ở mặt dưới: $1{,}6\sin r=1\cdot\sin i'$ nên $\sin i'=\sin45^\circ$, $i'=45^\circ=i$: tia ló song song tia tới.</p>
<p>b) Gọi $I$, $J$ là điểm tới ở mặt trên và mặt dưới. Đoạn $IJ$ trong kính: $IJ=\dfrac{e}{\cos r}$.</p>
<p>Kẻ $JK$ vuông góc với đường kéo dài của tia tới (tại $K$). Góc giữa $IJ$ và tia tới kéo dài là $i-r$.</p>
<p>$d=JK=IJ\sin(i-r)=\dfrac{e\sin(i-r)}{\cos r}$.</p>
<p>$d=\dfrac{4\sin(45^\circ-26{,}2^\circ)}{\cos26{,}2^\circ}\approx\dfrac{4\cdot0{,}3218}{0{,}8970}\approx1{,}43\ \text{cm}$.</p>
<p>c) Nhìn gần vuông góc, ảnh của chữ qua lớp kính dày $e$ dịch lại gần mắt một đoạn:</p>
<p>$\Delta=e\left(1-\dfrac1n\right)=4\left(1-\dfrac1{1{,}6}\right)=1{,}50\ \text{cm}$.</p>
<p>Lỗi hay gặp: nghĩ tấm kính làm tia sáng đổi hướng — tia ló song song tia tới, chỉ bị dời ngang.</p>
<p>Lỗi hay gặp: lấy $d=e\tan i-e\tan r$ (đó là độ dời dọc theo mặt kính, chưa nhân $\cos i$).</p>"""),

 # ── Bài 7 · Nâng cao: khối lập phương trong suốt
 ("Nâng cao", r"""<p>Một khối lập phương bằng chất trong suốt chiết suất $n$, đặt trong không khí. Chiếu tia sáng tới mặt trên của khối với góc tới $i$ bất kì ($0^\circ\lt i\lt90^\circ$), mặt phẳng tới vuông góc với một mặt bên. Tia khúc xạ đi vào khối rồi gặp mặt bên đó (kề với mặt trên).</p>
<p>a) Gọi $r$ là góc khúc xạ ở mặt trên. Chứng minh góc tới của tia ở mặt bên là $90^\circ-r$.</p>
<p>b) Chứng minh: muốn <em>mọi</em> tia như trên đều bị phản xạ toàn phần ở mặt bên thì $n\ge\sqrt2\approx1{,}414$.</p>
<p>c) Áp dụng: khối thuỷ tinh $n=1{,}5$ và khối nhựa $n=1{,}3$ — khối nào thoả điều kiện ở câu b)? Với khối không thoả, nêu một góc tới $i$ ở mặt trên để tia ló ra được ở mặt bên.</p>""",
  r"""<p>a) Pháp tuyến của mặt trên thẳng đứng, pháp tuyến của mặt bên nằm ngang, hai pháp tuyến vuông góc nhau.</p>
<p>Tia trong khối hợp với pháp tuyến mặt trên góc $r$ nên hợp với pháp tuyến mặt bên góc $90^\circ-r$ (hai góc phụ nhau trong tam giác vuông).</p>
<p>b) Ở mặt bên, tia đi từ khối ra không khí; phản xạ toàn phần khi $90^\circ-r\ge i_{gh}$, với $\sin i_{gh}=\dfrac1n$.</p>
<p>Góc tới $90^\circ-r$ nhỏ nhất khi $r$ lớn nhất. $r$ lớn nhất khi $i\to90^\circ$: $\sin r_{max}=\dfrac1n$, tức $r_{max}=i_{gh}$.</p>
<p>Điều kiện cho mọi tia: $90^\circ-i_{gh}\ge i_{gh}$, tức $i_{gh}\le45^\circ$, hay $\dfrac1n\le\sin45^\circ=\dfrac{1}{\sqrt2}$.</p>
<p>Vậy $n\ge\sqrt2\approx1{,}414$.</p>
<p>c) $n=1{,}5$: $i_{gh}\approx41{,}8^\circ$, góc tới nhỏ nhất ở mặt bên $90^\circ-41{,}8^\circ=48{,}2^\circ\gt41{,}8^\circ$: thoả.</p>
<p>$n=1{,}3$: $i_{gh}\approx50{,}3^\circ$, góc tới nhỏ nhất ở mặt bên $90^\circ-50{,}3^\circ=39{,}7^\circ\lt50{,}3^\circ$: không thoả.</p>
<p>Với khối nhựa, cần $90^\circ-r\lt50{,}3^\circ$, tức $r\gt39{,}7^\circ$, hay $\sin i=1{,}3\sin r\gt1{,}3\cdot0{,}639\approx0{,}831$, $i\gt56{,}2^\circ$.</p>
<p>Ví dụ $i=70^\circ$: $\sin r=\dfrac{0{,}9397}{1{,}3}\approx0{,}723$, $r\approx46{,}3^\circ$, góc tới ở mặt bên $43{,}7^\circ\lt50{,}3^\circ$ nên tia ló ra được.</p>
<p>Lỗi hay gặp: chỉ thử một góc tới (ví dụ $i=45^\circ$) rồi kết luận cho mọi tia — phải xét trường hợp xấu nhất $r=r_{max}$.</p>"""),

 # ── Bài 8 · Nâng cao: lăng kính tam giác đều
 ("Nâng cao", r"""<p>Một lăng kính thuỷ tinh có tiết diện thẳng là tam giác đều $ABC$, chiết suất $n=1{,}5$, đặt trong không khí. Một tia sáng nằm trong mặt phẳng tiết diện, tới mặt $AB$ theo phương vuông góc, tại điểm gần đỉnh $A$ (giữa $A$ và trung điểm của $AB$).</p>
<p>a) Vẽ đường truyền của tia sáng qua lăng kính. Chứng minh góc tới ở mặt $AC$ bằng $60^\circ$ và tia bị phản xạ toàn phần ở đó.</p>
<p>b) Chứng minh tia phản xạ tới mặt $BC$ theo phương vuông góc với $BC$. Tia ló ra khỏi lăng kính hợp với phương tia tới ban đầu một góc bao nhiêu?</p>
<p>c) Chiết suất của lăng kính phải thoả điều kiện gì để tia vẫn phản xạ toàn phần ở mặt $AC$ như trên? Cho $\sin60^\circ\approx0{,}8660$.</p>""",
  r"""<p>a) Tia tới vuông góc mặt $AB$ (góc tới $0^\circ$) nên đi thẳng vào lăng kính.</p>
<p>Tia vuông góc với $AB$, pháp tuyến của $AC$ vuông góc với $AC$; góc giữa hai đường này bằng góc giữa $AB$ và $AC$ (góc có cạnh tương ứng vuông góc), tức bằng $\hat A=60^\circ$.</p>
<p>Góc giới hạn của thuỷ tinh ra không khí: $\sin i_{gh}=\dfrac1{1{,}5}$, $i_{gh}\approx41{,}8^\circ$.</p>
<p>$60^\circ\gt41{,}8^\circ$ và tia đi từ thuỷ tinh ra không khí nên phản xạ toàn phần ở $AC$.</p>
<p>b) Tia tới hợp với mặt $AC$ góc $90^\circ-60^\circ=30^\circ$; theo định luật phản xạ, tia phản xạ cũng hợp với $AC$ góc $30^\circ$ ở phía bên kia pháp tuyến.</p>
<p>Gọi $I$ là điểm tới trên $AC$, $J$ là giao của tia phản xạ với $BC$. Trong tam giác $IJC$: $\widehat{JIC}=30^\circ$, $\hat C=60^\circ$ nên $\widehat{IJC}=180^\circ-30^\circ-60^\circ=90^\circ$.</p>
<p>Vậy tia phản xạ vuông góc với $BC$, góc tới ở $BC$ bằng $0^\circ$, tia ló đi thẳng ra ngoài.</p>
<p>Tia đổi hướng chỉ một lần, ở $AC$: góc lệch $180^\circ-2\cdot60^\circ=60^\circ$. Tia ló hợp với phương tia tới $60^\circ$.</p>
<p>c) Cần $60^\circ\ge i_{gh}$, tức $\dfrac1n\le\sin60^\circ$, hay $n\ge\dfrac1{0{,}8660}\approx1{,}155$.</p>
<p>Lỗi hay gặp: coi góc tới ở $AC$ là $30^\circ$ (góc giữa tia và mặt $AC$) rồi kết luận tia ló ra ở $AC$.</p>
<p>Lỗi hay gặp: dùng công thức $D=r_2-A$ — công thức đó chỉ dùng khi tia ló ra ở mặt thứ hai, ở đây tia bị phản xạ toàn phần.</p>"""),
]


def tu_luan():
    parts = []
    for k, (muc, de, gi) in enumerate(TL, 1):
        parts.append(f"<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>{gi}</details>")
    return dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
                body_html="<p>Các bài còn lại của chuyên đề, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>"
                          + "".join(parts))


def kiem_so():
    nw, c = F(4, 3), 3e8
    d = lambda x: degrees(x)
    sd, td = (lambda a: sin(radians(a))), (lambda a: tan(radians(a)))
    igh = lambda n: d(asin(1 / n))
    # Bài 1
    assert 12 / nw == 9 and 12 - 12 / nw == 3 and 12 * nw == 16
    # Bài 3
    v = c / float(nw); assert isclose(v, 2.25e8)
    assert round(3 / v * 1e9, 1) == 13.3 and round(3 / c * 1e9, 1) == 10.0 and isclose(c * 3 / v, 4.0)
    # Bài 4
    si = F(8, 10) / nw; assert si == F(3, 5)
    i4 = d(asin(0.6)); r4 = d(asin(0.8)); assert round(i4, 1) == 36.9 and round(r4, 1) == 53.1
    HI = 0.6 * 0.6 / 0.8; assert isclose(HI, 0.45) and isclose(HI, 0.6 * td(i4))
    hs = HI / td(r4); assert isclose(hs, 0.3375) and round(0.6 / float(nw), 2) == 0.45 and hs < 0.45
    # Bài 5
    sr5 = sd(60) / float(nw); r5 = d(asin(sr5)); assert round(sr5, 4) == 0.6495 and round(r5, 1) == 40.5
    a5, b5 = 0.4 * td(60), 0.8 * td(r5); assert round(a5, 3) == 0.693 and round(b5, 3) == 0.683
    assert round(a5 + b5, 2) == 1.38 and round(1.2 * td(60), 2) == 2.08
    # Bài 6
    sr6 = sd(45) / 1.6; r6 = d(asin(sr6)); assert round(sr6, 4) == 0.4419 and round(r6, 1) == 26.2
    assert round(sd(45 - r6), 4) == 0.3218 and round(cos(radians(r6)), 4) == 0.8970
    d6 = 4 * sd(45 - r6) / cos(radians(r6)); assert round(d6, 2) == 1.43
    assert round(4 * (1 - 1 / 1.6), 2) == 1.50
    # Bài 7
    for n, ok in ((1.5, True), (1.3, False)):
        g = igh(n); assert ((90 - g) >= g) == ok and (n >= sqrt(2)) == ok
    assert round(igh(1.5), 1) == 41.8 and round(90 - igh(1.5), 1) == 48.2
    assert round(igh(1.3), 1) == 50.3 and round(90 - igh(1.3), 1) == 39.7
    assert round(sd(90 - igh(1.3)), 3) == 0.639 and round(1.3 * sd(90 - igh(1.3)), 3) == 0.831
    assert round(d(asin(1.3 * sd(90 - igh(1.3)))), 1) == 56.2
    sr7 = sd(70) / 1.3; r7 = d(asin(sr7)); assert round(sd(70), 4) == 0.9397 and round(sr7, 3) == 0.723
    assert round(r7, 1) == 46.3 and round(90 - r7, 1) == 43.7 and 90 - r7 < igh(1.3)
    # Bài 8: lần theo vectơ trong tam giác đều AB nằm ngang
    A, B, C = (0, 0), (1, 0), (0.5, sqrt(3) / 2)
    vin = (0, 1)
    u = (C[0] - A[0], C[1] - A[1]); L = sqrt(u[0] ** 2 + u[1] ** 2); u = (u[0] / L, u[1] / L)
    nac = (-u[1], u[0])  # pháp tuyến AC
    inc = d(__import__("math").acos(abs(vin[0] * nac[0] + vin[1] * nac[1]))); assert round(inc, 6) == 60
    k = vin[0] * u[0] + vin[1] * u[1]; vr = (2 * k * u[0] - vin[0], 2 * k * u[1] - vin[1])
    w = (C[0] - B[0], C[1] - B[1]); assert abs(vr[0] * w[0] + vr[1] * w[1]) < 1e-12   # ⊥ BC
    dev = d(__import__("math").acos(vin[0] * vr[0] + vin[1] * vr[1])); assert round(dev, 6) == 60 == 180 - 2 * 60
    assert 60 > igh(1.5) and round(1 / sd(60), 3) == 1.155
    # tia vào gần A (x < 0,5) gặp AC: x = 0,3 → AC tại y = 0,3·√3 < C_y
    assert 0.3 * sqrt(3) < sqrt(3) / 2
    print("kiểm số liệu tự luận 151: đạt")


if __name__ == "__main__":
    kiem_so()
    print(len(tu_luan()["body_html"]))
