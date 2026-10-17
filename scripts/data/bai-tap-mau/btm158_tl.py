# -*- coding: utf-8 -*-
"""CĐ14 Gương phẳng, bóng tối và nửa tối (lesson 158) — Bài tập tự luận (xếp từ dễ đến khó).
Xuất tu_luan() (dict label + body_html) và kiem_so() (assert mọi đáp số).
Tự soạn 17/10/2026 theo dàn ý content/hsg9/cd14-guong-phang-bong-toi/nguon.md (mục Tự luận, số đã tính ở tinh.py),
phỏng theo kiểu đề HSG 9 / tuyển sinh 10 chuyên phổ biến, không chép đề cụ thể nào; số liệu khác 7 dạng mẫu và khác docx.
Quy ước: góc tới đo với pháp tuyến; ánh sáng truyền thẳng; mọi khoảng cách trong bài bóng đo từ nguồn.
Đề kín: ghi rõ gương đủ rộng / vật đặt trong góc / tia nằm trong mặt phẳng nào (xem nguon.md mục "Sai sót docx")."""
from math import atan2, cos, degrees, isclose, pi, radians, sin, tan

TL = [
 # ── Bài 1 · Dễ: hắt nắng vào hang
 ("Dễ", r"""<p>Buổi sáng, tia nắng chiếu xuống theo phương hợp với phương nằm ngang góc $36^\circ$, đi từ trái sang phải. Một bạn đặt gương phẳng nhỏ tại điểm $I$ trên mặt đất để hắt nắng vào một cửa hang ngang tầm gương. Các tia tới, tia phản xạ và pháp tuyến cùng nằm trong một mặt phẳng thẳng đứng.</p>
<p>a) Cửa hang ở bên phải $I$: muốn tia phản xạ đi nằm ngang sang phải thì góc tới bằng bao nhiêu, gương hợp với phương nằm ngang góc bao nhiêu?</p>
<p>b) Cửa hang ở bên trái $I$ (tia phản xạ đi nằm ngang ngược về phía Mặt Trời): trả lời lại câu a.</p>
<p>c) Từ vị trí ở câu a sang vị trí ở câu b, tia phản xạ đổi hướng $180^\circ$. Gương đã phải quay một góc bao nhiêu? Kết quả có khớp quy tắc "gương quay $\delta$ thì tia phản xạ quay $2\delta$" không?</p>""",
  r"""<p>Pháp tuyến $IN$ là phân giác của góc $SIR$ giữa tia tới (vẽ ngược về phía Mặt Trời, $IS$) và tia phản xạ $IR$; gương vuông góc với $IN$.</p>
<p>a) $IS$ hợp với phương ngang bên trái góc $36^\circ$, $IR$ nằm ngang sang phải nên $\widehat{SIR}=180^\circ-36^\circ=144^\circ$.</p>
<p>Góc tới $i=\dfrac{144^\circ}{2}=72^\circ$.</p>
<p>Pháp tuyến hợp với $IR$ (phương ngang) góc $72^\circ$, gương vuông góc pháp tuyến nên gương hợp với phương ngang $90^\circ-72^\circ=18^\circ$ (gương gần nằm ngang, mặt phản xạ quay lên).</p>
<p>b) $IR$ nằm ngang sang trái nên $\widehat{SIR}=36^\circ$, $i=18^\circ$.</p>
<p>Pháp tuyến hợp phương ngang $18^\circ$ nên gương hợp phương ngang $90^\circ-18^\circ=72^\circ$ (gương gần dựng đứng, mặt phản xạ quay về phía Mặt Trời).</p>
<p>c) Pháp tuyến ở câu a hợp phương ngang (phía phải) $72^\circ$; ở câu b hợp phương ngang (phía trái) $18^\circ$, tức nằm ở góc $180^\circ-18^\circ=162^\circ$ tính từ phía phải.</p>
<p>Pháp tuyến (và gương) đã quay $162^\circ-72^\circ=90^\circ$.</p>
<p>Tia tới giữ nguyên, gương quay $\delta=90^\circ$ thì tia phản xạ quay $2\delta=180^\circ$: khớp quy tắc.</p>
<p>Bẫy: lấy $36^\circ$ (góc với phương ngang) làm góc tới, hoặc nhầm góc giữa gương và phương ngang với góc tới.</p>"""),

 # ── Bài 2 · Dễ: bóng nắng chạm tường
 ("Dễ", r"""<p>Cùng một thời điểm, một cọc thẳng đứng cao $1{,}0\ \text{m}$ có bóng trên sân nằm ngang dài $1{,}25\ \text{m}$. Một cột điện thẳng đứng đứng cách một bức tường thẳng đứng (đủ cao) $6{,}0\ \text{m}$. Bóng của cột trải hết $6{,}0\ \text{m}$ trên sân rồi in tiếp lên tường; đỉnh bóng trên tường cao $1{,}6\ \text{m}$. Tia nắng coi là song song, nằm trong mặt phẳng thẳng đứng vuông góc với tường.</p>
<p>a) Tính chiều cao của cột.</p>
<p>b) Nếu không có bức tường thì bóng của cột trên sân dài bao nhiêu?</p>
<p>c) Buổi chiều, bóng của cọc dài $2{,}0\ \text{m}$. Đỉnh bóng của cột trên tường lúc này cao bao nhiêu?</p>""",
  r"""<p>Tia nắng song song nên mọi vật thẳng đứng có cùng tỉ số "chiều cao : bóng". Tia nắng đi được $1{,}25\ \text{m}$ theo phương ngang thì hạ xuống $1{,}0\ \text{m}$, tức hạ $0{,}8\ \text{m}$ cho mỗi mét ngang.</p>
<p>a) Tia nắng qua đỉnh cột đi $6{,}0\ \text{m}$ ngang tới tường thì hạ $0{,}8\cdot6{,}0=4{,}8\ \text{m}$ và chạm tường ở độ cao $1{,}6\ \text{m}$.</p>
<p>Chiều cao cột: $H=4{,}8+1{,}6=6{,}4\ \text{m}$.</p>
<p>b) Không có tường: $\ell=\dfrac{H}{0{,}8}=\dfrac{6{,}4}{0{,}8}=8{,}0\ \text{m}$.</p>
<p>Kiểm lại: phần bóng $8{,}0-6{,}0=2{,}0\ \text{m}$ "dựng" lên tường thành $2{,}0\cdot0{,}8=1{,}6\ \text{m}$ ✓.</p>
<p>c) Tia nắng hạ $\dfrac{1{,}0}{2{,}0}=0{,}5\ \text{m}$ cho mỗi mét ngang; qua $6{,}0\ \text{m}$ hạ $3{,}0\ \text{m}$.</p>
<p>Đỉnh bóng trên tường cao $6{,}4-3{,}0=3{,}4\ \text{m}$: nắng càng xiên, bóng leo lên tường càng cao.</p>
<p>Bẫy: lấy chiều cao bóng trên tường cộng thẳng với bóng trên sân ($6{,}0+1{,}6$) rồi đưa vào tỉ lệ.</p>"""),

 # ── Bài 3 · Trung bình: tìm độ cao đèn
 ("Trung bình", r"""<p>Một bóng đèn nhỏ (coi là điểm sáng) treo ở đỉnh cột đèn thẳng đứng trên mặt đường nằm ngang. Một bạn cao $h=1{,}6\ \text{m}$ đứng cách chân cột $4{,}0\ \text{m}$ thì thấy bóng của mình trên đường dài $2{,}0\ \text{m}$.</p>
<p>a) Tính độ cao $H$ của bóng đèn.</p>
<p>b) Bạn đi thẳng ra xa chân cột với tốc độ không đổi $v=1{,}0\ \text{m/s}$. Đỉnh bóng chạy với tốc độ bao nhiêu? Bóng dài thêm bao nhiêu mỗi giây?</p>
<p>c) Kể từ vị trí ban đầu, sau bao lâu bóng dài $3{,}2\ \text{m}$?</p>""",
  r"""<p>a) Tam giác (đèn, chân cột, đỉnh bóng) đồng dạng với tam giác (đầu người, chân người, đỉnh bóng):</p>
<p>$\dfrac{H}{h}=\dfrac{x+\ell}{\ell}=\dfrac{4{,}0+2{,}0}{2{,}0}=3$ nên $H=3\cdot1{,}6=4{,}8\ \text{m}$.</p>
<p>b) Từ $\dfrac{\ell}{x}=\dfrac{h}{H-h}=\dfrac{1{,}6}{3{,}2}=\dfrac12$: bóng luôn dài bằng nửa khoảng cách tới chân cột, $\ell=\dfrac{x}{2}$.</p>
<p>Mỗi giây $x$ tăng $1{,}0\ \text{m}$ nên $\ell$ tăng $0{,}5\ \text{m}$.</p>
<p>Đỉnh bóng cách chân cột $x+\ell=\dfrac{3x}{2}$ nên chạy nhanh $1{,}5$ lần người: $v_{\text{đỉnh}}=\dfrac{vH}{H-h}=1{,}5\ \text{m/s}$.</p>
<p>c) $\ell=3{,}2\ \text{m}$ khi $x=6{,}4\ \text{m}$; bạn phải đi thêm $6{,}4-4{,}0=2{,}4\ \text{m}$, mất $2{,}4\ \text{s}$.</p>
<p>Bẫy: cho rằng đỉnh bóng chạy bằng tốc độ người.</p>"""),

 # ── Bài 4 · Trung bình: không biết vị trí và độ cao đèn
 ("Trung bình", r"""<p>Ban đêm, một bạn cao $1{,}5\ \text{m}$ đứng trên đường nằm ngang, gần một cột đèn (bóng đèn coi là điểm sáng, cột thẳng đứng) nhưng không biết mình đứng cách chân cột bao xa và đèn cao bao nhiêu. Bạn đo được bóng của mình dài $1{,}0\ \text{m}$. Bạn lùi thẳng ra xa cột, dọc đường thẳng qua chân cột, thêm $2{,}0\ \text{m}$ thì đo được bóng dài $1{,}8\ \text{m}$.</p>
<p>a) Lúc đầu bạn đứng cách chân cột bao nhiêu? Đèn cao bao nhiêu?</p>
<p>b) Đứng cách chân cột bao xa thì bóng dài đúng bằng chiều cao của bạn?</p>""",
  r"""<p>Đèn cao $H$, người cao $h$ cách chân cột $x$ thì bóng dài $\ell=\dfrac{h}{H-h}\,x=k\,x$: bóng tỉ lệ thuận với $x$, hệ số $k$ không đổi.</p>
<p>a) Lùi thêm $2{,}0\ \text{m}$ thì bóng dài thêm $1{,}8-1{,}0=0{,}8\ \text{m}$ nên $k=\dfrac{0{,}8}{2{,}0}=0{,}4$.</p>
<p>Lúc đầu: $x=\dfrac{\ell}{k}=\dfrac{1{,}0}{0{,}4}=2{,}5\ \text{m}$.</p>
<p>$\dfrac{h}{H-h}=0{,}4$ nên $H-h=\dfrac{1{,}5}{0{,}4}=3{,}75\ \text{m}$, $H=5{,}25\ \text{m}$.</p>
<p>Kiểm: ở $x=4{,}5\ \text{m}$, $\ell=0{,}4\cdot4{,}5=1{,}8\ \text{m}$ ✓.</p>
<p>b) $\ell=h=1{,}5\ \text{m}$ khi $x=\dfrac{1{,}5}{0{,}4}=3{,}75\ \text{m}$ (đúng bằng $H-h$: tam giác vuông cân).</p>"""),

 # ── Bài 5 · Trung bình: đếm và dựng ảnh qua hai gương hợp góc
 ("Trung bình", r"""<p>Hai gương phẳng $G_1$, $G_2$ đủ rộng, có mặt phản xạ quay vào nhau, hợp với nhau góc $\alpha$, giao tuyến (cạnh chung) qua $O$. Điểm sáng $S$ đặt trong góc giữa hai gương.</p>
<p>a) Với $\alpha=30^\circ$: hệ cho bao nhiêu ảnh của $S$? Kết quả có phụ thuộc vị trí của $S$ trong góc không?</p>
<p>b) Với $\alpha=120^\circ$: hệ cho bao nhiêu ảnh khi $S$ nằm trên phân giác của góc, và khi $S$ lệch khỏi phân giác?</p>
<p>c) Với $\alpha=120^\circ$, $S$ trên phân giác, $OS=10\ \text{cm}$. Chứng minh các ảnh nằm trên một đường tròn; tính khoảng cách giữa $S$ và ảnh $S_1$ của nó qua $G_1$.</p>""",
  r"""<p>Mỗi ảnh đối xứng với vật (hoặc ảnh trước) qua mặt gương; phép đối xứng giữ khoảng cách tới $O$ (điểm nằm trên gương), nên mọi ảnh cách $O$ một khoảng bằng $OS$.</p>
<p>a) $\dfrac{360^\circ}{30^\circ}=12$ là số nguyên chẵn nên có $12-1=11$ ảnh, với mọi vị trí của $S$ trong góc.</p>
<p>b) $\dfrac{360^\circ}{120^\circ}=3$ là số nguyên lẻ.</p>
<p>$S$ trên phân giác: hai ảnh cuối của hai chuỗi (qua $G_1$ trước và qua $G_2$ trước) trùng nhau, còn $3-1=2$ ảnh.</p>
<p>$S$ lệch phân giác: hai ảnh cuối tách ra, có $3$ ảnh.</p>
<p>c) Mọi ảnh cách $O$ đúng $10\ \text{cm}$ nên nằm trên đường tròn tâm $O$ bán kính $10\ \text{cm}$.</p>
<p>$S$ trên phân giác nên $OS$ hợp $G_1$ góc $60^\circ$; $S_1$ đối xứng qua $G_1$ nên $\widehat{SOS_1}=120^\circ$.</p>
<p>Tam giác $SOS_1$ cân tại $O$: $SS_1=2\cdot OS\cdot\sin60^\circ\approx17{,}3\ \text{cm}$ (cũng bằng hai lần khoảng cách từ $S$ tới $G_1$).</p>
<p>Bẫy: đếm cả vật $S$ là một ảnh; quên điều kiện $\dfrac{360^\circ}{\alpha}$ phải là số nguyên mới dùng được quy tắc đếm.</p>"""),

 # ── Bài 6 · Khó: kính tiềm vọng
 ("Khó", r"""<p>Một kính tiềm vọng gồm ống thẳng đứng, hai đầu gắn hai gương phẳng $G_1$ (trên) và $G_2$ (dưới) song song với nhau, mỗi gương nghiêng $45^\circ$ so với phương thẳng đứng; tâm hai gương nằm trên cùng một đường thẳng đứng, cách nhau $0{,}8\ \text{m}$. Ánh sáng từ phía trước đi ngang vào miệng trên, gặp $G_1$ hắt thẳng xuống $G_2$, rồi hắt ngang ra miệng dưới tới mắt. Một cột cờ thẳng đứng ở phía trước, cách tâm $G_1$ một khoảng $20\ \text{m}$ theo phương ngang. Khi tính vị trí ảnh, xét điểm $A$ của cột cờ ngang tầm tâm $G_1$. Hai gương đủ lớn để nhận chùm tia đang xét.</p>
<p>a) Vẽ đường đi của một tia sáng từ một điểm của cột cờ tới mắt.</p>
<p>b) Ảnh $A_1$ của điểm $A$ qua $G_1$ nằm ở đâu? Ảnh cuối cùng $A_2$ (qua $G_1$ rồi $G_2$) nằm ở đâu, cách tâm $G_2$ bao nhiêu?</p>
<p>c) Ảnh cuối cùng chiều hay ngược chiều với cột cờ? Cao bằng bao nhiêu lần cột cờ?</p>""",
  r"""<p>a) Tia ngang từ cột cờ tới $G_1$ có góc tới $45^\circ$, phản xạ hợp tia tới $90^\circ$: đi thẳng đứng xuống $G_2$. Tại $G_2$ góc tới lại $45^\circ$, tia hắt ra nằm ngang, cùng chiều tia ban đầu, thấp hơn $0{,}8\ \text{m}$.</p>
<p>b) Đặt gốc tại tâm $G_2$, trục $x$ nằm ngang hướng về cột cờ, trục $y$ thẳng đứng hướng lên; tâm $G_1$ ở $(0;\ 0{,}8)$, điểm $A$ ở $(20;\ 0{,}8)$.</p>
<p>Ảnh qua $G_1$: $A_1$ đối xứng với $A$ qua $G_1$, nằm ngay phía trên tâm $G_1$ (trên đường thẳng đứng qua tâm hai gương), cách tâm $G_1$ đúng $20\ \text{m}$: điểm $A_1(0;\ 20{,}8)$.</p>
<p>Cả cột cờ (thẳng đứng) qua $G_1$ cho ảnh là một đoạn <em>nằm ngang</em> đi qua $A_1$: gương nghiêng $45^\circ$ đổi phương thẳng đứng thành phương ngang.</p>
<p>$A_1$ là vật đối với $G_2$; $A_1$ cách tâm $G_2$ là $20+0{,}8=20{,}8\ \text{m}$ theo phương thẳng đứng.</p>
<p>Ảnh cuối $A_2$ đối xứng với $A_1$ qua $G_2$: điểm $A_2(20{,}8;\ 0)$, ngang tầm tâm $G_2$, ở phía trước, cách tâm $G_2$ đúng $20{,}8\ \text{m}$ (xa hơn cột cờ $0{,}8\ \text{m}$ và thấp hơn $A$ là $0{,}8\ \text{m}$).</p>
<p>Nhận xét: khoảng cách ảnh cuối tới $G_2$ bằng tổng quãng đường tia đi từ vật tới $G_2$: $20+0{,}8=20{,}8\ \text{m}$.</p>
<p>c) Mỗi lần phản xạ, ảnh bằng vật. Đỉnh cột (cao hơn $A$ một đoạn $\delta$) cho ảnh qua $G_1$ ở $(\delta;\ 20{,}8)$, ảnh cuối ở $(20{,}8;\ \delta)$: vẫn cao hơn $A_2$ đúng $\delta$.</p>
<p>Ảnh cuối cùng chiều với cột cờ và cao bằng cột cờ (gấp $1$ lần).</p>
<p>Bẫy: tính ảnh qua $G_2$ từ chính cột cờ (quên ảnh qua $G_1$ mới là vật của $G_2$), hoặc cho rằng hai lần phản xạ làm ảnh lộn ngược.</p>"""),

 # ── Bài 7 · Khó: gương quay đều, vệt sáng chạy trên tường
 ("Khó", r"""<p>Một chùm laser hẹp, cố định, chiếu vào một gương phẳng nhỏ. Gương quay đều quanh một trục nằm trong mặt gương và vuông góc với tia tới, tốc độ $2$ vòng/phút. Một bức tường phẳng thẳng đứng song song với trục quay, cách trục $R=5{,}0\ \text{m}$. Tia phản xạ quét qua tường và tạo một vệt sáng.</p>
<p>a) Tia phản xạ quay với tốc độ bao nhiêu vòng/phút, bao nhiêu độ mỗi giây?</p>
<p>b) Tính tốc độ của vệt sáng trên tường lúc tia phản xạ vuông góc với tường.</p>
<p>c) Tính tốc độ của vệt sáng lúc tia phản xạ hợp với pháp tuyến của tường góc $30^\circ$.</p>""",
  r"""<p>a) Tia tới cố định, gương quay góc $\delta$ thì tia phản xạ quay $2\delta$ cùng chiều. Tia phản xạ quay $2\cdot2=4$ vòng/phút.</p>
<p>$4$ vòng/phút $=\dfrac{4\cdot360^\circ}{60\ \text{s}}=24^\circ/\text{s}$, tức $\omega=\dfrac{4\cdot2\pi}{60}\approx0{,}419\ \text{rad/s}$.</p>
<p>b) Trong thời gian rất ngắn, tia phản xạ quay một góc nhỏ; đầu tia ở cách trục $R$ vạch một cung gần như thẳng, vuông góc với tia, tức dọc theo tường.</p>
<p>Tốc độ vệt sáng: $v=\omega R\approx0{,}419\cdot5{,}0\approx2{,}09\ \text{m/s}$.</p>
<p>c) Lúc tia hợp pháp tuyến tường góc $\theta=30^\circ$, vệt sáng cách trục $r=\dfrac{R}{\cos\theta}$.</p>
<p>Đầu tia vạch cung với tốc độ $\omega r$, theo phương vuông góc với tia; tường nghiêng góc $\theta$ so với phương đó nên vệt sáng chạy trên tường nhanh hơn: $v=\dfrac{\omega r}{\cos\theta}=\dfrac{\omega R}{\cos^2\theta}$.</p>
<p>$v=\dfrac{2{,}09}{0{,}75}\approx2{,}79\ \text{m/s}$.</p>
<p>Bẫy: dùng tốc độ quay của gương (2 vòng/phút) thay vì của tia phản xạ, ra $v\approx1{,}05\ \text{m/s}$ ở câu b.</p>"""),

 # ── Bài 8 · Nâng cao: đèn ống, vùng tối có còn không
 ("Nâng cao", r"""<p>Một đèn ống thẳng dài $1{,}2\ \text{m}$ treo nằm ngang, cách sàn $2{,}4\ \text{m}$. Ngay dưới đèn có một thước mảnh dài $0{,}3\ \text{m}$ đặt nằm ngang, song song với đèn, trung điểm của thước nằm trên đường thẳng đứng qua trung điểm của đèn. Coi đèn là một đoạn thẳng mà mọi điểm đều phát sáng như nhau (bỏ qua bề ngang của ống), thước là một đoạn thẳng; chỉ xét bóng trên đường thẳng của sàn nằm ngay dưới đèn, trong mặt phẳng thẳng đứng chứa đèn và thước.</p>
<p>a) Thước cách sàn $0{,}8\ \text{m}$. Trên sàn có vùng tối không? Tính độ dài phần sàn bị thước che (một phần hoặc hoàn toàn) ánh sáng.</p>
<p>b) Hạ thước xuống còn cách sàn $0{,}2\ \text{m}$. Tính độ dài vùng tối và độ dài toàn bộ phần bóng (vùng tối cộng vùng nửa tối).</p>
<p>c) Thước phải cách sàn không quá bao nhiêu thì trên sàn còn vùng tối?</p>""",
  r"""<p>Gọi $D_n=1{,}2\ \text{m}$ (đèn), $d=0{,}3\ \text{m}$ (thước), $a$ là khoảng cách đèn → thước, $L=2{,}4\ \text{m}$ là khoảng cách đèn → sàn (đo từ nguồn).</p>
<p>Mép vùng tối: tia "cùng mép" nối đầu trái đèn với đầu trái thước (và tương tự bên phải). Mép ngoài vùng nửa tối: tia "chéo mép" nối đầu phải đèn với đầu trái thước.</p>
<p>Đặt gốc trên đường thẳng đứng qua tâm, xét nửa bên trái; tia cùng mép đi từ hoành độ $-0{,}6$ (ở đèn) qua $-0{,}15$ (ở thước), mỗi mét xuống dịch $\dfrac{0{,}45}{a}$; tới sàn có hoành độ $-0{,}6+0{,}45\cdot\dfrac{L}{a}$.</p>
<p>Độ dài vùng tối: $d_t=D_n-(D_n-d)\dfrac{L}{a}$. Tương tự, mép ngoài nửa tối: $d_n=(D_n+d)\dfrac{L}{a}-D_n$.</p>
<p>a) $a=2{,}4-0{,}8=1{,}6\ \text{m}$, $\dfrac{L}{a}=1{,}5$.</p>
<p>$d_t=1{,}2-0{,}9\cdot1{,}5=-0{,}15\ \text{m}\lt0$: hai tia cùng mép đã cắt nhau phía trên sàn, trên sàn không có vùng tối.</p>
<p>Phần sàn bị che: $d_n=1{,}5\cdot1{,}5-1{,}2=1{,}05\ \text{m}$, toàn bộ là nửa tối (đoạn $0{,}15\ \text{m}$ ở giữa vẫn nhận sáng từ hai đầu đèn).</p>
<p>b) $a=2{,}2\ \text{m}$, $\dfrac{L}{a}=\dfrac{12}{11}$.</p>
<p>$d_t=1{,}2-0{,}9\cdot\dfrac{12}{11}\approx0{,}22\ \text{m}$; $d_n=1{,}5\cdot\dfrac{12}{11}-1{,}2\approx0{,}44\ \text{m}$.</p>
<p>c) Còn vùng tối khi $d_t\ge0$: $\dfrac{L}{a}\le\dfrac{D_n}{D_n-d}=\dfrac{1{,}2}{0{,}9}=\dfrac43$, tức $a\ge\dfrac34L=1{,}8\ \text{m}$.</p>
<p>Thước cách sàn không quá $2{,}4-1{,}8=0{,}6\ \text{m}$.</p>
<p>Bẫy: lấy khoảng cách thước → sàn thay cho khoảng cách đèn → sàn trong tỉ số; chỉ vẽ tia từ trung điểm đèn (coi như nguồn điểm) sẽ ra bóng $0{,}45\ \text{m}$ và luôn "có vùng tối".</p>"""),
]


def tu_luan():
    parts = []
    for k, (muc, de, gi) in enumerate(TL, 1):
        parts.append(f"<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>{gi}</details>")
    return dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
                body_html="<p>Các bài còn lại của chuyên đề, xếp từ dễ đến khó. Tự giải trên giấy (vẽ hình trước) rồi mới mở hướng dẫn.</p>"
                          + "".join(parts))


def _refl(d, n):
    """Phản xạ véc-tơ d qua mặt có pháp tuyến n (đơn vị)."""
    k = d[0] * n[0] + d[1] * n[1]
    return (d[0] - 2 * k * n[0], d[1] - 2 * k * n[1])


def _mirror_pt(p, a, b, c):
    """Đối xứng điểm p qua đường ax + by + c = 0."""
    t = (a * p[0] + b * p[1] + c) / (a * a + b * b)
    return (p[0] - 2 * a * t, p[1] - 2 * b * t)


def _count(alpha, theta):
    """Đếm ảnh qua hai gương hợp góc alpha (độ), G1 theo tia 0°, G2 theo tia alpha, vật ở góc theta: dựng lần lượt hai chuỗi,
    một ảnh chỉ được phản xạ tiếp khi nằm hẳn phía trước gương kế tiếp (ảnh rơi vào vùng sau cả hai gương thì dừng)."""
    imgs = set()
    for first in (0, 1):
        ang, g = theta, first
        while True:
            ang = -ang if g == 0 else 2 * alpha - ang
            imgs.add(round(ang % 360, 6))
            g = 1 - g
            front = sin(radians(ang)) > 1e-9 if g == 0 else sin(radians(alpha - ang)) > 1e-9
            if not front:
                break
    imgs.discard(round(theta % 360, 6))
    return len(imgs)


def kiem_so():
    # Bài 1 — kiểm bằng phản xạ véc-tơ
    def guong_cho(inc_deg, out_deg):
        dsun = (cos(radians(inc_deg)), sin(radians(inc_deg)))          # hướng truyền của tia nắng
        r = (cos(radians(out_deg)), sin(radians(out_deg)))
        nx, ny = r[0] - dsun[0], r[1] - dsun[1]
        L = (nx * nx + ny * ny) ** 0.5
        n = (nx / L, ny / L)
        assert all(isclose(u, v, abs_tol=1e-12) for u, v in zip(_refl(dsun, n), r))
        i = degrees(atan2(abs(n[0] * dsun[1] - n[1] * dsun[0]), abs(n[0] * dsun[0] + n[1] * dsun[1])))
        nang = degrees(atan2(n[1], n[0])) % 180
        mir = (nang + 90) % 180
        return i, min(mir, 180 - mir), nang
    ia, ga, na = guong_cho(-36, 0)
    ib, gb, nb = guong_cho(-36, 180)
    assert round(ia, 6) == 72 and round(ga, 6) == 18 and round(ib, 6) == 18 and round(gb, 6) == 72
    assert round(na, 6) == 72 and round(nb, 6) == 162 and round(nb - na, 6) == 90
    # Bài 2
    k = 1.0 / 1.25
    H = k * 6.0 + 1.6; assert isclose(H, 6.4)
    assert isclose(H / k, 8.0) and isclose((8.0 - 6.0) * k, 1.6)
    assert isclose(H - 6.0 * (1.0 / 2.0), 3.4)
    # Bài 3
    h, x, l = 1.6, 4.0, 2.0
    H3 = h * (x + l) / l; assert isclose(H3, 4.8)
    kk = h / (H3 - h); assert isclose(kk, 0.5)
    assert isclose(1.0 * H3 / (H3 - h), 1.5) and isclose(1.0 * kk, 0.5)
    assert isclose(3.2 / kk - 4.0, 2.4)
    # Bài 4
    h4 = 1.5; k4 = (1.8 - 1.0) / 2.0; assert isclose(k4, 0.4)
    x4 = 1.0 / k4; H4 = h4 + h4 / k4
    assert isclose(x4, 2.5) and isclose(H4, 5.25) and isclose(h4 / (H4 - h4) * (x4 + 2), 1.8)
    assert isclose(h4 / k4, 3.75) and isclose(h4 / k4, H4 - h4)
    # Bài 5
    assert _count(30, 15) == 11 and _count(30, 7) == 11
    assert _count(120, 60) == 2 and _count(120, 30) == 3
    assert round(2 * 10 * sin(radians(60)), 1) == 17.3
    assert _count(72, 36) == 4 and _count(72, 20) == 5 and _count(45, 10) == 7 and _count(60, 30) == 5   # khớp nguon.md D7
    # Bài 6 — hai lần đối xứng: G1: y = x + 0,8 ; G2: y = x
    for dlt in (0.0, 1.0, 3.0):
        s1 = _mirror_pt((20.0, 0.8 + dlt), 1, -1, 0.8)
        s2 = _mirror_pt(s1, 1, -1, 0.0)
        assert isclose(s1[0], dlt, abs_tol=1e-9) and isclose(s1[1], 20.8, abs_tol=1e-9)
        assert isclose(s2[0], 20.8, abs_tol=1e-9) and isclose(s2[1], dlt, abs_tol=1e-9)
    # hướng tia: ngang (-1,0) → xuống (0,-1) → ngang (-1,0)
    n1 = (1 / 2 ** 0.5, -1 / 2 ** 0.5)
    d1 = _refl((-1.0, 0.0), n1); assert isclose(d1[0], 0, abs_tol=1e-12) and isclose(d1[1], -1)
    d2 = _refl(d1, n1); assert isclose(d2[0], -1) and isclose(d2[1], 0, abs_tol=1e-12)
    # Bài 7
    w = 4 * 2 * pi / 60; assert round(w, 3) == 0.419 and 4 * 360 / 60 == 24
    assert round(w * 5.0, 2) == 2.09 and round(w * 5.0 / cos(radians(30)) ** 2, 2) == 2.79
    assert round(2.09 / 0.75, 2) == 2.79 and round(2 * 2 * pi / 60 * 5.0, 2) == 1.05
    # kiểm c) bằng sai phân: x = R tan(theta)
    th, dt = radians(30), 1e-6
    assert isclose((5.0 * tan(th + w * dt) - 5.0 * tan(th)) / dt, w * 5.0 / cos(th) ** 2, rel_tol=1e-4)
    # Bài 8
    Dn, d, L = 1.2, 0.3, 2.4
    def bong(a):
        return Dn - (Dn - d) * L / a, (Dn + d) * L / a - Dn
    dt8, dn8 = bong(1.6); assert isclose(dt8, -0.15) and isclose(dn8, 1.05)
    dt8, dn8 = bong(2.2); assert round(dt8, 2) == 0.22 and round(dn8, 2) == 0.44
    a_min = L * (Dn - d) / Dn; assert isclose(a_min, 1.8) and isclose(L - a_min, 0.6)
    assert isclose(bong(a_min)[0], 0, abs_tol=1e-12)
    assert isclose(d * L / 1.6, 0.45)
    # kiểm d_t bằng giao điểm trực tiếp (nửa trái): tia từ (-0,6; 0) qua (-0,15; a)
    for a in (1.6, 2.2, 1.8):
        xt = -0.6 + 0.45 * L / a
        assert isclose(-2 * xt, bong(a)[0], abs_tol=1e-12)
        xn = 0.6 + (-0.15 - 0.6) * L / a
        assert isclose(-2 * xn, bong(a)[1], abs_tol=1e-12)
    print("kiểm số liệu tự luận 158: đạt")


if __name__ == "__main__":
    kiem_so()
    print(len(tu_luan()["body_html"]))
