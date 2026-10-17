# -*- coding: utf-8 -*-
"""CĐ08 Cảm ứng điện từ và dòng điện xoay chiều (lesson 152) — Bài tập tự luận (xếp từ dễ đến khó).
Xuất tu_luan() (dict label + body_html) và kiem_so() (assert mọi đáp số).
Tự soạn 17/10/2026 theo dàn ý content/hsg9/cd08-cam-ung-dien-tu/nguon.md (mục Tự luận), phỏng theo kiểu đề HSG 9 /
tuyển sinh 10 chuyên phổ biến, không chép đề cụ thể nào. Số liệu khác 6 dạng mẫu (152.json) và khác ví dụ docx (nguon.txt).
Quy ước theo nguon.md: R là điện trở TỔNG cả hai dây; P, U là công suất và hiệu điện thế ở ĐẦU đường dây;
bỏ qua hệ số công suất (công suất xoay chiều = UI với giá trị hiệu dụng). Không có lực từ / quy tắc bàn tay trái,
không có dạng tính tiền điện (thuộc CĐ05)."""
from fractions import Fraction as F
from math import sqrt, isclose

TL = [
 # ── Bài 1 · Dễ: nắm tay phải, kim nam châm gần đầu ống dây
 ("Dễ", r"""<p>Một ống dây dài đặt nằm ngang, đầu bên trái là $A$, đầu bên phải là $B$, nối với nguồn điện một chiều. Nhìn từ phía đầu $B$ vào lòng ống, dòng điện trong các vòng dây chạy theo chiều kim đồng hồ.</p>
<p>a) Dùng quy tắc nắm tay phải, xác định chiều đường sức từ trong lòng ống và tên cực từ ở mỗi đầu ống.</p>
<p>b) Đặt một kim nam châm nhỏ, quay tự do quanh trục thẳng đứng, trên trục của ống và ở gần đầu $B$. Khi kim đứng yên, cực nào của kim hướng về phía $B$?</p>
<p>c) Đổi chiều dòng điện trong ống dây. Kim nam châm thay đổi thế nào?</p>
<p>d) Giữ dòng điện như câu c), luồn một lõi sắt non vào lòng ống. Có gì thay đổi? Nếu thay lõi sắt non bằng một thanh đồng thì sao?</p>""",
  r"""<p>a) Nắm tay phải sao cho bốn ngón tay chỉ theo chiều dòng điện trong các vòng dây; ngón cái choãi ra chỉ chiều đường sức từ trong lòng ống.</p>
<p>Nhìn từ $B$ thấy dòng chạy cùng chiều kim đồng hồ, nên đường sức trong lòng ống đi ra xa người nhìn: từ $B$ sang $A$.</p>
<p>Đường sức đi ra ở đầu $A$, nên $A$ là cực Bắc, $B$ là cực Nam.</p>
<p>Kiểm tra bằng mẹo: nhìn vào một đầu ống thấy dòng ngược chiều kim đồng hồ thì đầu đó là cực Bắc; ở đây nhìn từ $B$ thấy cùng chiều kim đồng hồ nên $B$ là cực Nam ✓.</p>
<p>b) $B$ là cực Nam, các cực khác tên hút nhau nên cực Bắc của kim hướng về $B$.</p>
<p>c) Đổi chiều dòng điện thì hai cực của ống đổi chỗ: $B$ thành cực Bắc.</p>
<p>Kim quay nửa vòng, cực Nam của kim hướng về $B$.</p>
<p>d) Sắt non bị nhiễm từ, ống dây thành nam châm điện mạnh hơn nhiều; tên các cực không đổi, kim vẫn chỉ như câu c) nhưng bị định hướng mạnh hơn (đặt xa hơn vẫn thấy rõ).</p>
<p>Đồng không bị nhiễm từ nên thay bằng thanh đồng thì hầu như không có gì thay đổi.</p>
<p>Lỗi hay gặp: nghĩ đầu dòng điện "đi vào" là cực Bắc — tên cực do chiều dòng điện quanh ống quyết định, không do đầu nối dây.</p>"""),

 # ── Bài 2 · Dễ: khung dây đi qua vùng từ trường; nam châm rơi qua vòng nhôm
 ("Dễ", r"""<p>Một khung dây dẫn kín hình vuông cạnh $10\ \text{cm}$ chuyển động thẳng đều với tốc độ $5\ \text{cm/s}$ đi xuyên qua một vùng có từ trường đều rộng $30\ \text{cm}$. Mặt khung luôn vuông góc với đường sức từ; hai biên của vùng từ trường song song với cạnh trước của khung; bên ngoài vùng không có từ trường. Chọn mốc thời gian $t=0$ lúc cạnh trước của khung vừa chạm biên thứ nhất.</p>
<p>a) Trong những khoảng thời gian nào khung có dòng điện cảm ứng? Giải thích.</p>
<p>b) So sánh chiều dòng cảm ứng trong khung lúc khung đi vào và lúc khung đi ra khỏi vùng từ trường.</p>
<p>c) Làm lại câu a) khi vùng từ trường chỉ rộng $6\ \text{cm}$ (hẹp hơn khung).</p>
<p>d) Thả một nam châm thẳng rơi theo phương thẳng đứng xuyên qua một vòng nhôm kín đặt nằm ngang. Nam châm rơi nhanh hơn, chậm hơn hay như rơi tự do? Nếu vòng nhôm bị cắt một khe hở nhỏ thì sao? Bỏ qua sức cản không khí.</p>""",
  r"""<p>a) Dòng cảm ứng chỉ xuất hiện khi số đường sức từ xuyên qua khung <em>biến thiên</em>.</p>
<p>Khung đi vào vùng từ trường: từ $t=0$ đến $t=\dfrac{10}{5}=2\ \text{s}$; phần diện tích khung nằm trong vùng tăng dần, số đường sức tăng, có dòng cảm ứng.</p>
<p>Khung nằm hẳn trong vùng: từ $2\ \text{s}$ đến $t=\dfrac{30}{5}=6\ \text{s}$ (cạnh trước chạm biên thứ hai); số đường sức không đổi, không có dòng dù khung vẫn chuyển động.</p>
<p>Khung đi ra: từ $6\ \text{s}$ đến $t=\dfrac{30+10}{5}=8\ \text{s}$; số đường sức giảm, có dòng cảm ứng.</p>
<p>Sau $8\ \text{s}$ khung ở ngoài vùng, không có dòng.</p>
<p>Vậy có dòng trong hai khoảng $0$–$2\ \text{s}$ và $6$–$8\ \text{s}$, tổng cộng $4\ \text{s}$.</p>
<p>b) Lúc đi vào, dòng cảm ứng chống lại sự tăng của số đường sức; lúc đi ra, chống lại sự giảm. Hai nguyên nhân ngược nhau nên dòng cảm ứng ở hai giai đoạn có chiều ngược nhau.</p>
<p>c) Từ $t=0$ đến $t=\dfrac{6}{5}=1{,}2\ \text{s}$: phần vùng từ trường lọt vào trong khung tăng dần, có dòng.</p>
<p>Từ $1{,}2\ \text{s}$ đến $t=\dfrac{10}{5}=2\ \text{s}$ (cạnh sau của khung chạm biên thứ nhất): cả vùng từ trường nằm gọn trong khung, số đường sức không đổi, không có dòng.</p>
<p>Từ $2\ \text{s}$ đến $t=\dfrac{10+6}{5}=3{,}2\ \text{s}$: cạnh sau đi qua vùng, số đường sức giảm, có dòng.</p>
<p>Có dòng trong $0$–$1{,}2\ \text{s}$ và $2$–$3{,}2\ \text{s}$, tổng cộng $2{,}4\ \text{s}$.</p>
<p>d) Vòng nhôm kín: khi nam châm lại gần, số đường sức qua vòng tăng, vòng có dòng cảm ứng và mặt trên của vòng thành cực cùng tên với cực dưới của nam châm, đẩy nó lên.</p>
<p>Khi nam châm đã qua và đi xa dần, mặt dưới của vòng thành cực khác tên với cực trên của nam châm, hút nó lại.</p>
<p>Cả hai lúc đều cản chuyển động nên nam châm rơi chậm hơn rơi tự do. Đó là định luật Lenz: phần cơ năng mất đi biến thành nhiệt trong vòng nhôm.</p>
<p>Vòng có khe hở không kín, không có dòng cảm ứng, nam châm rơi như rơi tự do.</p>
<p>Lỗi hay gặp: cho rằng "khung đang chuyển động thì có dòng" — giai đoạn khung nằm hẳn trong vùng từ trường đều không có dòng.</p>"""),

 # ── Bài 3 · Trung bình: máy biến áp nhiều đầu ra, nối tiếp hai cuộn thứ cấp
 ("Trung bình", r"""<p>Các máy biến áp trong bài coi là lí tưởng; mọi cuộn dây quấn trên cùng một lõi; cuộn sơ cấp đều có $1100$ vòng và nối vào nguồn xoay chiều $220\ \text{V}$.</p>
<p>a) Máy thứ nhất có cuộn thứ cấp rút nhiều đầu ra để lấy các hiệu điện thế $3$, $6$, $9$, $12\ \text{V}$ (tính từ một đầu chung). Các đầu ra phải rút ở vòng thứ bao nhiêu của cuộn thứ cấp?</p>
<p>b) Máy thứ hai có hai cuộn thứ cấp riêng: cuộn X $60$ vòng, cuộn Y $30$ vòng. Tính hiệu điện thế giữa hai đầu mỗi cuộn.</p>
<p>c) Nối tiếp hai cuộn X và Y (nối một đầu của X với một đầu của Y, lấy điện ở hai đầu còn lại). Hiệu điện thế lấy ra là bao nhiêu nếu hai cuộn quấn cùng chiều nối tiếp nhau? Nếu nối sao cho chúng ngược chiều nhau?</p>
<p>d) Chỉ dùng cuộn X, cuộn Y và các cách nối ở câu b), c), có lấy được $3\ \text{V}$ không?</p>""",
  r"""<p>a) Mỗi vòng dây có hiệu điện thế như nhau: $\dfrac{220}{1100}=0{,}2\ \text{V}$ trên một vòng.</p>
<p>Từ $\dfrac{U_1}{U_2}=\dfrac{N_1}{N_2}$: $N_2=\dfrac{N_1U_2}{U_1}=\dfrac{U_2}{0{,}2}$.</p>
<p>$3\ \text{V}$: vòng thứ $15$.</p>
<p>$6\ \text{V}$: vòng thứ $30$.</p>
<p>$9\ \text{V}$: vòng thứ $45$.</p>
<p>$12\ \text{V}$: vòng thứ $60$ (cuối cuộn).</p>
<p>b) Cuộn X: $U_X=0{,}2\cdot60=12\ \text{V}$. Cuộn Y: $U_Y=0{,}2\cdot30=6\ \text{V}$.</p>
<p>c) Nối tiếp cùng chiều: hai cuộn như một cuộn $60+30=90$ vòng, $U=0{,}2\cdot90=18\ \text{V}$.</p>
<p>Nối tiếp ngược chiều: phần $30$ vòng của Y "trừ" bớt $30$ vòng của X, còn tương đương $60-30=30$ vòng, $U=6\ \text{V}$.</p>
<p>d) Các giá trị lấy được chỉ là $6$, $12$, $18\ \text{V}$ (và $6\ \text{V}$ khi nối ngược chiều), nên không lấy được $3\ \text{V}$; cần một cuộn $15$ vòng.</p>
<p>Lỗi hay gặp: viết ngược $N_2=\dfrac{N_1U_1}{U_2}$, ra hàng chục nghìn vòng — máy hạ áp phải có $N_2\lt N_1$.</p>
<p>Lỗi hay gặp: nghĩ nối tiếp hai cuộn thứ cấp thì luôn cộng hiệu điện thế, quên trường hợp nối ngược chiều.</p>"""),

 # ── Bài 4 · Trung bình: máy biến áp + cầu chì sơ cấp, số đèn tối đa
 ("Trung bình", r"""<p>Một máy biến áp lí tưởng có cuộn sơ cấp $2000$ vòng, cuộn thứ cấp $100$ vòng; cuộn sơ cấp nối vào nguồn xoay chiều $220\ \text{V}$ qua một cầu chì chịu được dòng tối đa $0{,}5\ \text{A}$ (dòng lớn hơn thì cầu chì đứt). Ở cuộn thứ cấp mắc song song các bóng đèn loại $11\ \text{V}$ – $20\ \text{W}$. Bỏ qua điện trở dây nối.</p>
<p>a) Tính hiệu điện thế ở hai đầu cuộn thứ cấp. Các đèn có sáng bình thường không?</p>
<p>b) Mắc được nhiều nhất bao nhiêu bóng đèn mà cầu chì không đứt?</p>
<p>c) Với số đèn ở câu b), tính cường độ dòng điện qua cuộn thứ cấp và qua cuộn sơ cấp.</p>
<p>d) Mắc thêm một bóng nữa thì điều gì xảy ra? Vì sao dây cuộn thứ cấp thường to hơn dây cuộn sơ cấp?</p>""",
  r"""<p>a) $U_2=U_1\dfrac{N_2}{N_1}=220\cdot\dfrac{100}{2000}=11\ \text{V}$, bằng hiệu điện thế định mức nên các đèn mắc song song đều sáng bình thường.</p>
<p>b) Máy lí tưởng nên công suất lấy ở thứ cấp bằng công suất đưa vào sơ cấp: $P_2=P_1=U_1I_1$.</p>
<p>Cầu chì không đứt khi $I_1\le0{,}5\ \text{A}$, tức $P_1\le220\cdot0{,}5=110\ \text{W}$.</p>
<p>Mỗi đèn $20\ \text{W}$: số đèn $n\le\dfrac{110}{20}=5{,}5$, nên mắc được nhiều nhất $5$ bóng.</p>
<p>c) $P_2=5\cdot20=100\ \text{W}$.</p>
<p>$I_2=\dfrac{P_2}{U_2}=\dfrac{100}{11}\approx9{,}09\ \text{A}$.</p>
<p>$I_1=\dfrac{P_1}{U_1}=\dfrac{100}{220}\approx0{,}455\ \text{A}$ (kiểm tra: $I_1=I_2\dfrac{N_2}{N_1}=\dfrac{9{,}09}{20}\approx0{,}455\ \text{A}$ ✓).</p>
<p>d) $6$ bóng: $P_1=120\ \text{W}$, $I_1=\dfrac{120}{220}\approx0{,}545\ \text{A}\gt0{,}5\ \text{A}$, cầu chì đứt, tất cả các đèn tắt.</p>
<p>Máy hạ áp $20$ lần thì dòng thứ cấp lớn gấp $20$ lần dòng sơ cấp; dây thứ cấp phải có tiết diện lớn để không nóng quá.</p>
<p>Lỗi hay gặp: so $0{,}5\ \text{A}$ với dòng qua đèn ($I_2$) thay vì dòng qua cầu chì ở sơ cấp ($I_1$).</p>"""),

 # ── Bài 5 · Trung bình: hao phí ở hai hiệu điện thế, điện năng hao phí mỗi ngày
 ("Trung bình", r"""<p>Một trạm điện truyền đi công suất $300\ \text{kW}$ (đo ở đầu đường dây, không đổi suốt ngày) đến một khu sản xuất. Điện trở tổng cộng của cả hai dây là $8\ \Omega$.</p>
<p>a) Truyền tải ở hiệu điện thế $6\ \text{kV}$. Tính cường độ dòng điện trên dây, công suất hao phí và điện năng hao phí trên dây trong một ngày ($24\ \text{h}$), theo kWh.</p>
<p>b) Dùng máy biến áp (coi là lí tưởng) nâng hiệu điện thế ở đầu đường dây lên $30\ \text{kV}$, công suất truyền đi vẫn $300\ \text{kW}$. Tính lại các đại lượng ở câu a).</p>
<p>c) Mỗi ngày bớt được bao nhiêu kWh điện hao phí? Hiệu điện thế tăng bao nhiêu lần thì hao phí giảm bao nhiêu lần?</p>""",
  r"""<p>a) $I=\dfrac{P}{U}=\dfrac{300\,000}{6000}=50\ \text{A}$.</p>
<p>$P_{\text{hp}}=RI^2=8\cdot50^2=20\,000\ \text{W}=20\ \text{kW}$.</p>
<p>$A_{\text{hp}}=P_{\text{hp}}t=20\cdot24=480\ \text{kWh}$ mỗi ngày.</p>
<p>b) $I=\dfrac{300\,000}{30\,000}=10\ \text{A}$.</p>
<p>$P_{\text{hp}}=8\cdot10^2=800\ \text{W}=0{,}8\ \text{kW}$.</p>
<p>$A_{\text{hp}}=0{,}8\cdot24=19{,}2\ \text{kWh}$ mỗi ngày.</p>
<p>c) Bớt được $480-19{,}2=460{,}8\ \text{kWh}$ mỗi ngày.</p>
<p>Hiệu điện thế tăng $\dfrac{30}{6}=5$ lần thì hao phí giảm $\dfrac{20}{0{,}8}=25=5^2$ lần, đúng với $P_{\text{hp}}=\dfrac{P^2R}{U^2}$.</p>
<p>Lỗi hay gặp: tính $I=\dfrac{U}{R}=\dfrac{6000}{8}$ — $U$ là hiệu điện thế ở đầu đường dây, không phải hiệu điện thế đặt lên hai đầu dây; dòng trên dây phải tính từ $I=\dfrac{P}{U}$.</p>"""),

 # ── Bài 6 · Khó: dây đồng hay dây nhôm (cùng chiều dài, cùng khối lượng)
 ("Khó", r"""<p>Cần chọn dây cho một đường dây tải điện. Có hai phương án: dây đồng và dây nhôm có <em>cùng chiều dài</em> $\ell$ và <em>cùng khối lượng</em> $m$. Cho điện trở suất $\rho_{\text{đồng}}=1{,}7\cdot10^{-8}\ \Omega\cdot\text{m}$, $\rho_{\text{nhôm}}=2{,}8\cdot10^{-8}\ \Omega\cdot\text{m}$; khối lượng riêng $D_{\text{đồng}}=8900\ \text{kg/m}^3$, $D_{\text{nhôm}}=2700\ \text{kg/m}^3$.</p>
<p>a) Chứng minh điện trở của một dây đồng chất, tiết diện đều có chiều dài $\ell$, khối lượng $m$ là $R=\dfrac{\rho D\ell^2}{m}$.</p>
<p>b) Tính tỉ số điện trở $\dfrac{R_{\text{nhôm}}}{R_{\text{đồng}}}$ và tỉ số tiết diện $\dfrac{S_{\text{nhôm}}}{S_{\text{đồng}}}$.</p>
<p>c) Truyền cùng một công suất, ở cùng một hiệu điện thế. Hao phí trên dây nhôm bằng bao nhiêu phần hao phí trên dây đồng?</p>
<p>d) Giải thích vì sao dây cao thế thường làm bằng nhôm (có lõi thép) chứ không bằng đồng, dù đồng dẫn điện tốt hơn.</p>""",
  r"""<p>a) Thể tích dây $V=S\ell=\dfrac{m}{D}$ nên $S=\dfrac{m}{D\ell}$.</p>
<p>Thay vào $R=\rho\dfrac{\ell}{S}$: $R=\rho\ell\cdot\dfrac{D\ell}{m}=\dfrac{\rho D\ell^2}{m}$.</p>
<p>b) Cùng $\ell$ và $m$ nên $R\propto\rho D$:</p>
<p>$\dfrac{R_{\text{nhôm}}}{R_{\text{đồng}}}=\dfrac{2{,}8\cdot2700}{1{,}7\cdot8900}=\dfrac{7560}{15\,130}\approx0{,}50$.</p>
<p>$\dfrac{S_{\text{nhôm}}}{S_{\text{đồng}}}=\dfrac{D_{\text{đồng}}}{D_{\text{nhôm}}}=\dfrac{8900}{2700}\approx3{,}3$.</p>
<p>c) Cùng $P$ và $U$ thì cùng $I=\dfrac PU$, hao phí $P_{\text{hp}}=RI^2$ tỉ lệ với $R$: hao phí trên dây nhôm chỉ bằng khoảng một nửa hao phí trên dây đồng cùng khối lượng.</p>
<p>d) Với cùng khối lượng kim loại (tức cùng sức nặng treo lên cột), dây nhôm to hơn khoảng $3{,}3$ lần và có điện trở chỉ bằng khoảng một nửa, nên hao phí ít hơn.</p>
<p>Nhôm còn rẻ hơn đồng. Nhôm kém bền khi bị kéo căng giữa hai cột nên có lõi thép để chịu lực kéo.</p>
<p>Lỗi hay gặp: so sánh chỉ theo điện trở suất ($\rho_{\text{nhôm}}\gt\rho_{\text{đồng}}$) mà quên điều kiện "cùng khối lượng" làm tiết diện dây nhôm lớn hơn nhiều.</p>"""),

 # ── Bài 7 · Khó: đo bằng vôn kế và công tơ ở hai đầu đường dây
 ("Khó", r"""<p>Để kiểm tra một đường dây tải điện, người ta đặt ở đầu đường dây (nơi phát) và ở cuối đường dây (nơi tiêu thụ) mỗi nơi một vôn kế và một công tơ điện. Vôn kế ở đầu đường dây chỉ $6000\ \text{V}$, vôn kế ở cuối đường dây chỉ $5700\ \text{V}$. Sau $24\ \text{h}$, số chỉ của công tơ ở đầu đường dây tăng nhiều hơn số chỉ của công tơ ở cuối đường dây là $216\ \text{kWh}$. Coi công suất truyền đi không đổi trong thời gian đó; bỏ qua hệ số công suất (công suất $=UI$).</p>
<p>a) Tính công suất hao phí trên đường dây.</p>
<p>b) Tính cường độ dòng điện trên dây và điện trở tổng cộng của đường dây.</p>
<p>c) Tính công suất truyền đi và hiệu suất truyền tải.</p>
<p>d) Muốn hao phí chỉ còn $1\,\%$ công suất truyền đi (công suất truyền đi và đường dây giữ nguyên) thì hiệu điện thế ở đầu đường dây phải là bao nhiêu, tức tăng bao nhiêu lần?</p>""",
  r"""<p>a) Hai công tơ chênh nhau đúng bằng điện năng hao phí trên dây: $P_{\text{hp}}=\dfrac{216\ \text{kWh}}{24\ \text{h}}=9\ \text{kW}$.</p>
<p>b) Độ giảm thế trên dây: $\Delta U=6000-5700=300\ \text{V}$.</p>
<p>$P_{\text{hp}}=\Delta U\cdot I$ (vì $P_{\text{hp}}=RI^2=(IR)I$) nên $I=\dfrac{9000}{300}=30\ \text{A}$.</p>
<p>$R=\dfrac{\Delta U}{I}=\dfrac{300}{30}=10\ \Omega$.</p>
<p>c) $P=UI=6000\cdot30=180\,000\ \text{W}=180\ \text{kW}$.</p>
<p>$H=1-\dfrac{P_{\text{hp}}}{P}=1-\dfrac{9}{180}=0{,}95=95\,\%$.</p>
<p>d) $\dfrac{P_{\text{hp}}}{P}=\dfrac{PR}{U^2}=0{,}01$ nên $U=\sqrt{\dfrac{PR}{0{,}01}}=\sqrt{\dfrac{180\,000\cdot10}{0{,}01}}\approx13\,416\ \text{V}\approx13{,}4\ \text{kV}$.</p>
<p>Tỉ lệ hao phí giảm từ $5\,\%$ xuống $1\,\%$, tức $5$ lần, nên $U$ tăng $\sqrt5\approx2{,}24$ lần: $6000\cdot2{,}24\approx13{,}4\ \text{kV}$ ✓.</p>
<p>Lỗi hay gặp: tính $I=\dfrac{U}{R}$ với $U=6000\ \text{V}$, hoặc lấy $P_{\text{hp}}=\dfrac{U^2}{R}$ — hiệu điện thế đặt lên dây chỉ là $\Delta U=300\ \text{V}$.</p>
<p>Lỗi hay gặp: muốn hao phí giảm $5$ lần thì tăng $U$ lên $5$ lần.</p>"""),

 # ── Bài 8 · Nâng cao: hệ hai máy biến áp, biện luận khi bỏ máy tăng áp
 ("Nâng cao", r"""<p>Một máy phát điện xoay chiều cung cấp công suất $200\ \text{kW}$ ở hiệu điện thế $1\ \text{kV}$. Điện được đưa qua máy tăng áp có tỉ số vòng dây $\dfrac{N_1}{N_2}=\dfrac{1}{10}$, truyền trên đường dây có điện trở tổng cộng $20\ \Omega$, rồi qua máy hạ áp ở nơi tiêu thụ để có $220\ \text{V}$. Hai máy biến áp coi là lí tưởng; bỏ qua hệ số công suất.</p>
<p>a) Tính hiệu điện thế ở đầu đường dây, cường độ dòng điện trên dây, công suất hao phí và hiệu suất truyền tải.</p>
<p>b) Tính hiệu điện thế ở đầu vào máy hạ áp và tỉ số vòng dây $\dfrac{N_3}{N_4}$ của máy hạ áp ($N_3$ là cuộn nối với đường dây).</p>
<p>c) Tính công suất nơi tiêu thụ nhận được.</p>
<p>d) Một bạn đề nghị bỏ máy tăng áp, nối thẳng máy phát vào đường dây cho "đỡ tốn". Hãy biện luận để chỉ ra đề nghị đó không thực hiện được.</p>""",
  r"""<p>a) Máy tăng áp: $U=1000\cdot10=10\,000\ \text{V}$ ở đầu đường dây; máy lí tưởng nên công suất đầu dây vẫn là $200\ \text{kW}$.</p>
<p>$I=\dfrac{P}{U}=\dfrac{200\,000}{10\,000}=20\ \text{A}$.</p>
<p>$P_{\text{hp}}=RI^2=20\cdot20^2=8000\ \text{W}=8\ \text{kW}$.</p>
<p>$H=1-\dfrac{8}{200}=0{,}96=96\,\%$.</p>
<p>b) Độ giảm thế: $\Delta U=IR=20\cdot20=400\ \text{V}$.</p>
<p>Đầu vào máy hạ áp: $U_3=10\,000-400=9600\ \text{V}$.</p>
<p>$\dfrac{N_3}{N_4}=\dfrac{U_3}{U_4}=\dfrac{9600}{220}\approx43{,}6$.</p>
<p>c) $P_{\text{tt}}=P-P_{\text{hp}}=200-8=192\ \text{kW}$ (máy hạ áp lí tưởng không làm mất thêm).</p>
<p>d) Nối thẳng ở $1\ \text{kV}$: muốn truyền $200\ \text{kW}$ thì dòng phải là $I=\dfrac{200\,000}{1000}=200\ \text{A}$.</p>
<p>Độ giảm thế trên dây khi đó là $IR=200\cdot20=4000\ \text{V}$, lớn hơn cả $1000\ \text{V}$ của máy phát — vô lí.</p>
<p>Tương tự, hao phí sẽ là $20\cdot200^2=800\ \text{kW}$, lớn hơn cả công suất máy phát.</p>
<p>Vậy với đường dây $20\ \Omega$ không thể truyền $200\ \text{kW}$ ở $1\ \text{kV}$: máy tăng áp là bắt buộc.</p>
<p>Lỗi hay gặp: lấy $\dfrac{N_3}{N_4}=\dfrac{10\,000}{220}\approx45{,}5$, quên độ giảm thế $400\ \text{V}$ trên dây.</p>
<p>Lỗi hay gặp ở d): tính ra $P_{\text{hp}}=800\ \text{kW}\gt P$ mà vẫn ghi kết quả, không nhận ra vô lí.</p>"""),
]


def tu_luan():
    parts = []
    for k, (muc, de, gi) in enumerate(TL, 1):
        parts.append(f"<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>{gi}</details>")
    return dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
                body_html="<p>Các bài còn lại của chuyên đề, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>"
                          + "".join(parts))


def line(P, U, R):
    I = F(P) / U
    Php = R * I * I
    return I, Php, 1 - Php / P, I * R, U - I * R


def kiem_so():
    RHO_CU, RHO_AL, D_CU, D_AL = F(17, 10), F(28, 10), 8900, 2700   # ρ tính theo 1e-8 Ω·m (tỉ số không đổi)
    # Bài 2: khung 10 cm, v = 5 cm/s, vùng 30 cm rồi 6 cm
    a, v, Lw = 10, 5, 30
    assert (F(a, v), F(Lw, v), F(Lw + a, v)) == (2, 6, 8) and 2 * F(a, v) == 4
    Ln = 6
    assert (F(Ln, v), F(a, v), F(a + Ln, v)) == (F(6, 5), 2, F(16, 5)) and 2 * F(Ln, v) == F(12, 5)
    # Bài 3
    vpv = F(220, 1100); assert vpv == F(1, 5)
    assert [u / vpv for u in (3, 6, 9, 12)] == [15, 30, 45, 60]
    assert 60 * vpv == 12 and 30 * vpv == 6 and 90 * vpv == 18 and 30 * vpv == 6
    assert 3 not in {60 * vpv, 30 * vpv, 90 * vpv, 30 * vpv}
    # Bài 4
    U2 = F(220 * 100, 2000); assert U2 == 11
    P1max = 220 * F(1, 2); assert P1max == 110 and int(P1max // 20) == 5
    I2, I1 = F(100) / 11, F(100) / 220
    assert round(float(I2), 2) == 9.09 and round(float(I1), 3) == 0.455 and I1 == I2 * F(100, 2000)
    assert F(120, 220) > F(1, 2) and round(120 / 220, 3) == 0.545
    # Bài 5
    I, Php, H, _, _ = line(300_000, 6000, 8); assert I == 50 and Php == 20_000 and Php * 24 / 1000 == 480
    I_, Php_, _, _, _ = line(300_000, 30_000, 8); assert I_ == 10 and Php_ == 800 and Php_ * 24 / 1000 == F(192, 10)
    assert (Php - Php_) * 24 / 1000 == F(4608, 10) and Php / Php_ == 25
    # Bài 6
    rR = (RHO_AL * D_AL) / (RHO_CU * D_CU); assert RHO_AL * D_AL == 7560 and RHO_CU * D_CU == 15130
    assert round(float(rR), 2) == 0.50 and round(D_CU / D_AL, 1) == 3.3
    # Bài 7
    Php7 = F(216_000, 24); dU = 6000 - 5700; I7 = Php7 / dU; R7 = dU / I7; P7 = 6000 * I7
    assert Php7 == 9000 and I7 == 30 and R7 == 10 and P7 == 180_000 and 1 - Php7 / P7 == F(95, 100)
    assert R7 * I7 ** 2 == Php7
    U7 = sqrt(float(P7 * R7) / 0.01); assert round(U7) == 13416 and isclose(U7 / 6000, sqrt(5)) and round(sqrt(5), 2) == 2.24
    # Bài 8
    I8, Php8, H8, dU8, U3 = line(200_000, 10_000, 20)
    assert I8 == 20 and Php8 == 8000 and H8 == F(96, 100) and dU8 == 400 and U3 == 9600
    assert round(float(U3 / 220), 1) == 43.6 and round(10_000 / 220, 1) == 45.5 and 200_000 - Php8 == 192_000
    I0 = F(200_000, 1000); assert I0 == 200 and I0 * 20 == 4000 > 1000 and 20 * I0 ** 2 == 800_000 > 200_000
    print("kiểm số liệu tự luận 152: đạt")


if __name__ == "__main__":
    kiem_so()
    print(len(tu_luan()["body_html"]))
