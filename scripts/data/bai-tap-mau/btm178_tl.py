# -*- coding: utf-8 -*-
"""CĐ17 Thiên văn: Mặt Trăng, Hệ Mặt Trời và Ngân Hà (lesson 178) — Bài tập tự luận (xếp từ dễ đến khó).
Xuất tu_luan() (dict label + body_html) và kiem_so() (assert mọi đáp số).
Tự soạn 17/10/2026 theo dàn ý content/hsg9/cd17-thien-van/nguon.md (mục Tự luận 1–8), không chép đề cụ thể nào.
Số liệu khác 6 dạng mẫu (178.json) và khác luyện tập. Quy ước số liệu theo nguon.md:
AU = 1,5.10^8 km; c = 3.10^5 km/s; D_S = 1,39.10^6 km; D_E = 12 740 km (R_E = 6370 km); D_M = 3470 km;
d_M = 384 000 km; Tuần Trăng S = 29,5 ngày (đề dễ); năm 365,25 ngày; trục nghiêng 23,5°; h = 90° − |φ − δ|."""
from math import atan, degrees, radians, tan, pi

TL = [
 # ── Bài 1 · Dễ: lịch pha + giờ trăng mọc
 ("Dễ", r"""<p>Lúc $0$ giờ ngày $5/10$ là thời điểm không trăng (Mặt Trăng ở giữa Mặt Trời và Trái Đất). Lấy Tuần Trăng $S=29{,}5$ ngày; coi các pha cách đều nhau $\dfrac{S}{4}$.</p>
<p>a) Tìm ngày (và giờ gần đúng) có trăng thượng huyền, trăng tròn, trăng hạ huyền và lần không trăng tiếp theo. Tháng 10 có $31$ ngày.</p>
<p>b) Mỗi ngày Mặt Trăng mọc trễ hơn hôm trước khoảng bao nhiêu phút?</p>
<p>c) Hôm trăng tròn, Mặt Trăng mọc khoảng $18$ giờ. Ba ngày sau, Mặt Trăng mọc khoảng mấy giờ? Đêm hôm đó, đầu hôm (khoảng $19$ giờ) có nhìn thấy trăng không?</p>""",
  r"""<p>a) Mỗi pha chính cách nhau $\dfrac{S}{4}=\dfrac{29{,}5}{4}\approx7{,}4$ ngày.</p>
<p>Thượng huyền: $5+7{,}4=12{,}4$, tức khoảng $9$ giờ ngày $12/10$.</p>
<p>Trăng tròn: $5+14{,}75=19{,}75$, tức khoảng $18$ giờ ngày $19/10$.</p>
<p>Hạ huyền: $5+22{,}1=27{,}1$, tức khoảng $3$ giờ ngày $27/10$.</p>
<p>Không trăng tiếp theo: $5+29{,}5=34{,}5$; trừ $31$ ngày của tháng 10 được $3{,}5$, tức khoảng $12$ giờ ngày $3/11$.</p>
<p>b) Sau một Tuần Trăng, giờ mọc lùi trọn một vòng $24$ giờ, nên mỗi ngày trễ $\dfrac{24\cdot60}{29{,}5}\approx49$ phút.</p>
<p>c) Ba ngày sau trăng tròn, trăng mọc trễ $3\cdot49\approx146$ phút $\approx2$ giờ $26$ phút: khoảng $20$ giờ $30$.</p>
<p>Lúc $19$ giờ trăng chưa mọc nên chưa thấy; phải chờ sau $20$ giờ $30$ mới thấy trăng (khuyết dần) ló lên ở phía Đông.</p>
<p>Giả thiết đã dùng: các pha cách đều nhau và giờ mọc trễ đều mỗi ngày (thực tế thay đổi trong khoảng $30$–$70$ phút tuỳ mùa và vĩ độ).</p>"""),

 # ── Bài 2 · Dễ: giờ Mặt Trời theo kinh độ, múi giờ, chuyến bay
 ("Dễ", r"""<p>Trái Đất tự quay một vòng ($360^\circ$) trong $24$ giờ. Cả Việt Nam dùng chung giờ múi $+7$, tức giờ của kinh tuyến chuẩn $105^\circ$Đ. Bỏ qua sự chênh lệch nhỏ của giữa trưa thật theo mùa.</p>
<p>a) Trái Đất quay $1^\circ$ mất bao nhiêu phút? Huế ở kinh độ $107{,}6^\circ$Đ, Hà Nội ở $105{,}8^\circ$Đ. Nơi nào có giữa trưa (Mặt Trời lên cao nhất) sớm hơn, sớm hơn bao nhiêu phút?</p>
<p>b) TP.HCM ở kinh độ $106{,}7^\circ$Đ. Đồng hồ ở TP.HCM chỉ mấy giờ lúc giữa trưa thật?</p>
<p>c) Một chuyến bay cất cánh ở Hà Nội lúc $23$ giờ $30$ ngày $1/7$ (giờ Việt Nam), bay $13$ giờ tới Paris. Mùa hè Paris dùng giờ múi $+2$. Máy bay hạ cánh lúc mấy giờ, ngày nào theo giờ Paris?</p>""",
  r"""<p>a) $1^\circ$ ứng với $\dfrac{24\cdot60}{360}=4$ phút.</p>
<p>Trái Đất quay từ Tây sang Đông nên nơi ở phía Đông thấy Mặt Trời qua đỉnh trước: Huế sớm hơn Hà Nội.</p>
<p>Chênh lệch: $(107{,}6-105{,}8)\cdot4=1{,}8\cdot4\approx7{,}2$ phút.</p>
<p>b) TP.HCM ở phía Đông kinh tuyến chuẩn $106{,}7-105=1{,}7^\circ$, nên giữa trưa thật đến sớm hơn $12$ giờ đồng hồ một khoảng $1{,}7\cdot4\approx6{,}8$ phút.</p>
<p>Đồng hồ chỉ khoảng $11$ giờ $53$ phút.</p>
<p>c) Theo giờ Việt Nam, máy bay hạ cánh lúc $23$ giờ $30 + 13$ giờ $= 12$ giờ $30$ ngày $2/7$.</p>
<p>Paris chậm hơn Việt Nam $7-2=5$ giờ, nên giờ Paris là $7$ giờ $30$ ngày $2/7$.</p>
<p>Bẫy: cộng $5$ giờ thay vì trừ (Paris ở phía Tây nên giờ chậm hơn, tức đồng hồ chỉ số nhỏ hơn).</p>"""),

 # ── Bài 3 · Trung bình: bóng cọc ở Huế + tìm vĩ độ
 ("Trung bình", r"""<p>Huế ở vĩ độ $\varphi=16{,}5^\circ$B. Cắm thẳng đứng một cọc cao $1\ \text{m}$ trên sân phẳng. Góc cao Mặt Trời buổi trưa $h=90^\circ-|\varphi-\delta|$, với xích vĩ Mặt Trời $\delta=0^\circ$ (xuân phân, thu phân), $+23{,}5^\circ$ (hạ chí), $-23{,}5^\circ$ (đông chí). Coi tia nắng song song, bỏ qua khúc xạ khí quyển.</p>
<p>a) Tính góc cao Mặt Trời buổi trưa ở Huế vào xuân phân, hạ chí và đông chí.</p>
<p>b) Tính độ dài bóng cọc buổi trưa trong ba ngày đó và cho biết bóng ngả về phía nào.</p>
<p>c) Ở một nơi khác trên Bắc bán cầu, trưa ngày xuân phân bóng của cọc $1\ \text{m}$ dài $0{,}16\ \text{m}$, ngả về phía Bắc. Nơi đó ở vĩ độ bao nhiêu?</p>""",
  r"""<p>a) Xuân phân: $h=90^\circ-16{,}5^\circ=73{,}5^\circ$.</p>
<p>Hạ chí: $h=90^\circ-|16{,}5^\circ-23{,}5^\circ|=90^\circ-7^\circ=83{,}0^\circ$.</p>
<p>Đông chí: $h=90^\circ-|16{,}5^\circ+23{,}5^\circ|=90^\circ-40^\circ=50{,}0^\circ$.</p>
<p>b) Bóng cọc cao $1\ \text{m}$ dài $\ell=\dfrac{1}{\tan h}$.</p>
<p>Xuân phân: $\ell=\dfrac{1}{\tan73{,}5^\circ}\approx0{,}30\ \text{m}$, ngả về Bắc ($\delta\lt\varphi$: Mặt Trời ở phía Nam).</p>
<p>Hạ chí: $\ell=\dfrac{1}{\tan83^\circ}\approx0{,}12\ \text{m}$, ngả về <strong>Nam</strong> ($\delta=23{,}5^\circ\gt\varphi$: Mặt Trời ở phía Bắc đỉnh đầu).</p>
<p>Đông chí: $\ell=\dfrac{1}{\tan50^\circ}\approx0{,}84\ \text{m}$, ngả về Bắc.</p>
<p>c) Ngày xuân phân $\delta=0$ nên $h=90^\circ-\varphi$, tức góc giữa tia nắng và cọc bằng đúng $\varphi$.</p>
<p>$\tan\varphi=\dfrac{0{,}16}{1}$ nên $\varphi\approx9{,}1^\circ$B (gần vĩ độ Cà Mau).</p>
<p>Bẫy: lấy $h=90^\circ-(\varphi+\delta)$ cho ngày hạ chí sẽ ra $50^\circ$ (sai); quên đổi hướng bóng khi $\delta\gt\varphi$.</p>"""),

 # ── Bài 4 · Trung bình: Eratosthenes lịch sử + sai số stadion
 ("Trung bình", r"""<p>Khoảng năm $240$ TCN, Eratosthenes biết: trưa ngày hạ chí ở Syene (Ai Cập) Mặt Trời ở ngay đỉnh đầu (đáy giếng sâu được chiếu sáng), còn cùng lúc đó ở Alexandria, xa hơn về phía Bắc, tia nắng lệch phương thẳng đứng $7{,}2^\circ$. Khoảng cách Syene – Alexandria ước khoảng $5000$ stadia. Coi hai nơi cùng kinh tuyến, tia nắng tới Trái Đất song song, Trái Đất là quả cầu.</p>
<p>a) Vẽ hình, chứng minh góc ở tâm Trái Đất chắn cung Syene – Alexandria bằng $7{,}2^\circ$.</p>
<p>b) Giả thiết $1$ stadion $=157{,}5\ \text{m}$. Tính chu vi và bán kính Trái Đất theo cách của Eratosthenes.</p>
<p>c) Ở Alexandria, cọc thẳng đứng $1\ \text{m}$ có bóng dài bao nhiêu lúc đó?</p>
<p>d) Bàn về sai số: ngày nay ta biết chu vi kinh tuyến khoảng $40\,000\ \text{km}$. Nếu độ dài stadion thật ra là $185\ \text{m}$ thì kết quả thay đổi thế nào? Nêu thêm hai nguồn sai số khác của phép đo.</p>""",
  r"""<p>a) Ở Syene tia nắng đi theo bán kính (thẳng đứng). Ở Alexandria, phương thẳng đứng là bán kính $OA$. Tia nắng tới $A$ song song với tia tới Syene.</p>
<p>Góc giữa tia nắng và $OA$ tại $A$ và góc ở tâm $\widehat{SOA}$ là hai góc so le trong của hai đường song song cắt bởi đường $OA$, nên $\widehat{SOA}=7{,}2^\circ$.</p>
<p>b) $7{,}2^\circ=\dfrac{360^\circ}{50}$, nên cung Syene – Alexandria bằng $\dfrac{1}{50}$ chu vi.</p>
<p>$s=5000\cdot157{,}5\ \text{m}=787\,500\ \text{m}=787{,}5\ \text{km}$.</p>
<p>Chu vi $C=50\cdot787{,}5=39\,375\ \text{km}\approx39\,400\ \text{km}$.</p>
<p>Bán kính $R=\dfrac{C}{2\pi}\approx6270\ \text{km}$.</p>
<p>c) Bóng dài $\ell=1\cdot\tan7{,}2^\circ\approx0{,}126\ \text{m}\approx12{,}6\ \text{cm}$.</p>
<p>d) Với $1$ stadion $=157{,}5\ \text{m}$: sai số so với $40\,000\ \text{km}$ chỉ $\dfrac{40\,000-39\,375}{40\,000}\approx1{,}6\,\%$.</p>
<p>Với $1$ stadion $=185\ \text{m}$: $C=50\cdot5000\cdot0{,}185=46\,250\ \text{km}$, lớn hơn thực tế khoảng $16\,\%$.</p>
<p>Vậy độ chính xác "nổi tiếng" của Eratosthenes phụ thuộc nhiều vào việc ta tin stadion dài bao nhiêu; các sử gia chưa thống nhất con số này.</p>
<p>Nguồn sai số khác: Syene không nằm đúng trên chí tuyến và không cùng kinh tuyến với Alexandria (lệch khoảng $3^\circ$ kinh độ); khoảng cách $5000$ stadia chỉ là ước lượng theo thời gian đi đường; đo góc $7{,}2^\circ$ bằng bóng cọc có sai số vì Mặt Trời không phải điểm sáng (bóng nhoè mép).</p>
<p>Phương pháp vẫn đúng: chỉ cần một góc và một quãng đường đo trên mặt đất là ước được kích thước Trái Đất.</p>"""),

 # ── Bài 5 · Khó: nhật thực hình khuyên theo khoảng cách
 ("Khó", r"""<p>Xét nhật thực khi tâm Mặt Trời, tâm Mặt Trăng và mắt người quan sát thẳng hàng; người quan sát đứng ở điểm mặt đất ngay dưới Mặt Trăng, nên khoảng cách từ mắt tới Mặt Trăng là $d-R_E$ ($d$: khoảng cách tâm Trái Đất – tâm Mặt Trăng). Góc trông nhỏ: $\alpha\approx\dfrac{D}{\text{khoảng cách}}$ (rad). Cho $D_S=1{,}39\cdot10^6\ \text{km}$, $D_M=3470\ \text{km}$, $R_E=6370\ \text{km}$; khoảng cách Trái Đất – Mặt Trời $1\ \text{AU}=1{,}5\cdot10^8\ \text{km}$. Bỏ qua khí quyển.</p>
<p>a) Tính góc trông Mặt Trời và góc trông Mặt Trăng (ra độ) khi $d=395\,000\ \text{km}$. Đó là nhật thực loại gì? Phần trăm diện tích đĩa Mặt Trời bị che là bao nhiêu?</p>
<p>b) Khi $d=384\,000\ \text{km}$ (khoảng cách trung bình), nhật thực là toàn phần hay hình khuyên? Dùng nón bóng tối của Mặt Trăng (dài $L=\dfrac{a\,D_M}{D_S-D_M}$ với $a=\text{AU}-d$, như bài Bóng tối – nửa tối) để tính bề rộng vùng trên mặt đất thấy hình khuyên.</p>
<p>c) Đầu tháng 1, Trái Đất ở gần Mặt Trời nhất, cách $1{,}47\cdot10^8\ \text{km}$. Khi đó $d$ lớn nhất bằng bao nhiêu thì vẫn có thể có nhật thực toàn phần? Nhật thực toàn phần dễ xảy ra hơn vào tháng 1 hay tháng 7?</p>""",
  r"""<p>a) Mặt Trời: $\alpha_S=\dfrac{1{,}39\cdot10^6}{1{,}5\cdot10^8}\approx9{,}27\cdot10^{-3}\ \text{rad}\approx0{,}531^\circ$.</p>
<p>Mặt Trăng: $\alpha_M=\dfrac{3470}{395\,000-6370}=\dfrac{3470}{388\,630}\ \text{rad}\approx0{,}512^\circ$.</p>
<p>$\alpha_M\lt\alpha_S$: đĩa Mặt Trăng trông nhỏ hơn, che không kín, còn một vành sáng — nhật thực hình khuyên.</p>
<p>Diện tích đĩa tỉ lệ với bình phương góc trông: phần bị che $\left(\dfrac{0{,}512}{0{,}531}\right)^2\approx0{,}93=93\,\%$.</p>
<p>b) $\alpha_M=\dfrac{3470}{377\,630}\ \text{rad}\approx0{,}526^\circ\lt0{,}531^\circ$: vẫn là hình khuyên (che khoảng $98\,\%$).</p>
<p>Nón bóng tối: $a=1{,}5\cdot10^8-384\,000\approx1{,}496\cdot10^8\ \text{km}$, $L=\dfrac{a\cdot3470}{1{,}39\cdot10^6-3470}\approx374\,400\ \text{km}$.</p>
<p>Từ Mặt Trăng tới mặt đất $x=377\,630\ \text{km}\gt L$: chóp nón bóng tối không chạm đất.</p>
<p>Sau chóp, các tia mép kéo dài loe ra thành nón ngược; tại mặt đất bề rộng vùng hình khuyên (tam giác đồng dạng) là $D_M\dfrac{x-L}{L}=3470\cdot\dfrac{3190}{374\,400}\approx30\ \text{km}$.</p>
<p>Chỉ một dải rất hẹp thấy hình khuyên; nơi khác trong nửa tối chỉ thấy nhật thực một phần.</p>
<p>c) Điều kiện toàn phần: $\alpha_M\ge\alpha_S$, tức $\dfrac{D_M}{d-R_E}\ge\dfrac{D_S}{1{,}47\cdot10^8}$.</p>
<p>$d-R_E\le\dfrac{3470\cdot1{,}47\cdot10^8}{1{,}39\cdot10^6}\approx367\,000\ \text{km}$, nên $d\le373\,000\ \text{km}$ (xấp xỉ).</p>
<p>Với $1\ \text{AU}$ thì giới hạn là $d\le374\,000+6370\approx380\,000\ \text{km}$. Tháng 1 Mặt Trời trông to hơn nên Mặt Trăng phải ở gần hơn mới che kín: nhật thực toàn phần khó xảy ra hơn vào tháng 1, dễ hơn vào tháng 7 (Trái Đất xa Mặt Trời nhất).</p>
<p>Bẫy: quên trừ $R_E$ (dùng khoảng cách tới tâm Trái Đất); quên bình phương khi tính phần diện tích; dùng góc ở độ trong công thức $\alpha=D/d$ (công thức cho rad).</p>"""),

 # ── Bài 6 · Trung bình: mô hình Hệ Mặt Trời trên sân trường
 ("Trung bình", r"""<p>Lớp em muốn dựng mô hình Hệ Mặt Trời theo đúng tỉ lệ khoảng cách trên một sân trường dài $100\ \text{m}$: Mặt Trời đặt ở đầu sân, Sao Hải Vương ($30\ \text{AU}$) ở cuối sân. Cho $1\ \text{AU}=1{,}5\cdot10^8\ \text{km}$, $D_S=1{,}39\cdot10^6\ \text{km}$, $D_E=12\,740\ \text{km}$, khoảng cách Trái Đất – Mặt Trăng $384\,000\ \text{km}$; Sao Hoả $1{,}52$; Sao Mộc $5{,}2$; Sao Thổ $9{,}5\ \text{AU}$; sao gần nhất (Proxima Centauri) cách khoảng $2{,}67\cdot10^5\ \text{AU}$. Dùng cùng một tỉ lệ cho cả kích thước và khoảng cách.</p>
<p>a) Tìm tỉ lệ của mô hình ($1\ \text{AU}$ ứng với bao nhiêu mét; tỉ lệ $1:N$, tìm $N$).</p>
<p>b) Đặt Trái Đất, Sao Hoả, Sao Mộc, Sao Thổ cách Mặt Trời bao nhiêu mét?</p>
<p>c) Mô hình Mặt Trời và Trái Đất to bằng bao nhiêu? Mặt Trăng đặt cách Trái Đất bao xa?</p>
<p>d) Mô hình Proxima Centauri phải đặt cách sân trường bao xa? Rút ra nhận xét về "độ trống" của Hệ Mặt Trời.</p>""",
  r"""<p>a) $30\ \text{AU}\leftrightarrow100\ \text{m}$ nên $1\ \text{AU}\leftrightarrow\dfrac{100}{30}\approx3{,}33\ \text{m}$.</p>
<p>$N=\dfrac{1{,}5\cdot10^{11}\ \text{m}}{3{,}33\ \text{m}}=4{,}5\cdot10^{10}$: tỉ lệ $1:4{,}5\cdot10^{10}$.</p>
<p>b) Trái Đất $3{,}3\ \text{m}$; Sao Hoả $1{,}52\cdot3{,}33\approx5{,}1\ \text{m}$; Sao Mộc $5{,}2\cdot3{,}33\approx17\ \text{m}$; Sao Thổ $9{,}5\cdot3{,}33\approx32\ \text{m}$.</p>
<p>Bốn hành tinh đất đá chen trong khoảng $5\ \text{m}$ đầu sân; các hành tinh khổng lồ rải ra tới cuối sân.</p>
<p>c) Mặt Trời: $\dfrac{1{,}39\cdot10^9\ \text{m}}{4{,}5\cdot10^{10}}\approx0{,}031\ \text{m}=3{,}1\ \text{cm}$ (nhỏ hơn quả bóng bàn).</p>
<p>Trái Đất: $\dfrac{1{,}274\cdot10^7\ \text{m}}{4{,}5\cdot10^{10}}\approx2{,}8\cdot10^{-4}\ \text{m}=0{,}28\ \text{mm}$ (một hạt bụi).</p>
<p>Mặt Trăng cách Trái Đất $\dfrac{3{,}84\cdot10^8\ \text{m}}{4{,}5\cdot10^{10}}\approx8{,}5\ \text{mm}$.</p>
<p>d) Proxima: $2{,}67\cdot10^5\cdot3{,}33\ \text{m}\approx8{,}9\cdot10^5\ \text{m}\approx890\ \text{km}$ — ở một tỉnh khác.</p>
<p>Nhận xét: trên sân $100\ \text{m}$ chỉ có một viên bi $3\ \text{cm}$ và vài hạt bụi nhỏ hơn milimét; gần như toàn bộ là khoảng trống. Còn từ Mặt Trời tới sao gần nhất là cả chặng gần $900\ \text{km}$ không có gì.</p>
<p>Lưu ý: không thể vẽ cùng lúc kích thước và khoảng cách đúng tỉ lệ trên một trang sách — các hình Hệ Mặt Trời quen thuộc đều phóng to hành tinh.</p>"""),

 # ── Bài 7 · Khó: ngày sao, giờ mọc của sao theo ngày và theo kinh độ
 ("Khó", r"""<p>Ngày sao (thời gian Trái Đất tự quay đúng $360^\circ$ so với các ngôi sao xa) dài $23$ h $56$ min $4$ s, ngắn hơn ngày Mặt Trời $24$ h. Xét một ngôi sao nằm trên xích đạo trời: ở mọi nơi nó mọc đúng hướng Đông và giờ mọc không phụ thuộc vĩ độ. Bỏ qua khúc xạ khí quyển; cả nước dùng giờ múi $+7$.</p>
<p>a) Vẽ Trái Đất ở hai vị trí trên quỹ đạo cách nhau một ngày, giải thích (không cần tính) vì sao ngày sao ngắn hơn ngày Mặt Trời.</p>
<p>b) Đêm $1/1$, ở Hà Nội ngôi sao mọc lúc $20$ giờ (giờ đồng hồ). Mỗi đêm nó mọc sớm hơn bao nhiêu? Ngày $1/4$ (sau $90$ ngày) nó mọc lúc mấy giờ? Đầu hôm ngày $1/4$ có thấy cảnh nó mọc không?</p>
<p>c) Cũng đêm $1/1$, một bạn ở Đà Nẵng (kinh độ $108{,}2^\circ$Đ) quan sát cùng ngôi sao; Hà Nội ở $105{,}8^\circ$Đ. Theo đồng hồ, ở Đà Nẵng sao mọc sớm hơn hay muộn hơn Hà Nội, bao nhiêu phút?</p>
<p>d) Vì sao chòm sao thấy được lúc đầu hôm thay đổi theo mùa? Sau bao lâu thì bầu trời đầu hôm lặp lại như cũ?</p>""",
  r"""<p>a) Trong một ngày Trái Đất đi được $\dfrac{360^\circ}{365{,}25}\approx0{,}986^\circ$ trên quỹ đạo, cùng chiều tự quay.</p>
<p>Sao ở rất xa nên hướng tới sao không đổi: quay đủ $360^\circ$ là sao về lại chỗ cũ.</p>
<p>Hướng tới Mặt Trời đã lệch đi $0{,}986^\circ$, nên Trái Đất phải quay thêm chừng ấy (khoảng $4$ phút) Mặt Trời mới lại qua đỉnh: ngày Mặt Trời dài hơn ngày sao.</p>
<p>b) Mỗi đêm sao mọc sớm hơn $24\ \text{h}-23\ \text{h}\ 56\ \text{min}\ 4\ \text{s}=3$ min $56$ s $=236\ \text{s}$ (gần $4$ phút).</p>
<p>Sau $90$ ngày: $90\cdot236\ \text{s}=21\,240\ \text{s}\approx5{,}9$ giờ $\approx5$ giờ $54$ phút.</p>
<p>Ngày $1/4$ sao mọc khoảng $20$ giờ $-\ 5$ giờ $54$ phút $=14$ giờ $06$, lúc đang ban ngày: không thấy cảnh mọc; đầu hôm nó đã lên khá cao ở phía Đông.</p>
<p>c) Bầu trời "quay" từ Đông sang Tây, $1^\circ$ kinh độ ứng với khoảng $4$ phút. Đà Nẵng ở phía Đông Hà Nội $108{,}2^\circ-105{,}8^\circ=2{,}4^\circ$ nên thấy sao mọc trước.</p>
<p>Sớm hơn khoảng $2{,}4\cdot4\approx9{,}6$ phút: ở Đà Nẵng sao mọc lúc khoảng $19$ giờ $50$ (đồng hồ hai nơi chỉ cùng giờ $+7$).</p>
<p>d) Sau $30$ ngày sao mọc sớm hơn $30\cdot236\ \text{s}\approx118$ phút $\approx2$ giờ; sau nửa năm sớm khoảng $12$ giờ: chòm sao lúc đầu hôm mùa đông thì mùa hè lại ở trên trời ban ngày.</p>
<p>Sau một năm ($365{,}25$ ngày) tổng độ sớm là $365{,}25\cdot236\ \text{s}\approx24$ h, tức trọn một vòng: bầu trời đầu hôm lặp lại sau $1$ năm.</p>
<p>Bẫy: tưởng sao mọc muộn dần (lấy ngày sao $=24$ h $+4$ min); ở c) cho rằng phía Tây thấy trước.</p>"""),

 # ── Bài 8 · Khó (HSG): phương pháp bóng Trái Đất (ý tưởng của Aristarchus)
 ("Khó (HSG)", r"""<p>Khoảng năm $270$ TCN, Aristarchus đã dùng bóng Trái Đất trong nguyệt thực để so kích thước Mặt Trăng với Trái Đất (ông ước bóng rộng khoảng $2$ lần Mặt Trăng). Bài này làm lại cách nghĩ đó với số liệu tốt hơn. Giả sử khi nguyệt thực đo được bề rộng vùng bóng tối của Trái Đất tại quỹ đạo Mặt Trăng bằng $k=2{,}6$ lần đường kính Mặt Trăng, và góc trông Mặt Trăng xấp xỉ góc trông Mặt Trời (khoảng $0{,}52^\circ$). Coi tia sáng từ Mặt Trời tới là các tia thẳng, Mặt Trời ở rất xa so với Mặt Trăng; lấy $D_E=12\,740\ \text{km}$ (đo được bằng phương pháp Eratosthenes).</p>
<p>a) Chứng minh: khi đi ra xa Trái Đất một quãng $x$, bề rộng nón bóng tối của Trái Đất hẹp đi xấp xỉ $\alpha_S\,x$ ($\alpha_S$: góc trông Mặt Trời, tính bằng rad).</p>
<p>b) Suy ra tại quỹ đạo Mặt Trăng, bóng tối hẹp hơn $D_E$ đúng bằng $D_M$, từ đó $D_M\approx\dfrac{D_E}{1+k}$. Tính $D_M$.</p>
<p>c) Từ góc trông $0{,}52^\circ$, tính khoảng cách Trái Đất – Mặt Trăng.</p>
<p>d) So với giá trị ngày nay ($D_M=3470\ \text{km}$; $d=384\,000\ \text{km}$), sai số tương đối của mỗi kết quả là bao nhiêu? Đại lượng nào đo trong nguyệt thực ảnh hưởng nhiều nhất tới kết quả?</p>""",
  r"""<p>a) Hai tia đi qua mép trên Mặt Trời – mép trên Trái Đất và mép dưới Mặt Trời – mép dưới Trái Đất giới hạn nón bóng tối.</p>
<p>Mỗi tia nghiêng vào trong so với trục một góc $\dfrac{\alpha_S}{2}$ (nửa góc trông Mặt Trời nhìn từ Trái Đất, vì Mặt Trời rất xa).</p>
<p>Đi thêm quãng $x$, mỗi mép tiến vào trục $\dfrac{\alpha_S}{2}x$, nên bề rộng giảm $\alpha_S x$.</p>
<p>b) Tại quỹ đạo Mặt Trăng ($x=d$): bóng tối rộng $D_E-\alpha_S d$.</p>
<p>Vì $\alpha_S\approx\alpha_M=\dfrac{D_M}{d}$ nên $\alpha_S d\approx D_M$: bóng tối rộng $D_E-D_M$.</p>
<p>Theo quan sát $D_E-D_M=k\,D_M$, nên $D_M=\dfrac{D_E}{1+k}=\dfrac{12\,740}{3{,}6}\approx3540\ \text{km}$.</p>
<p>c) $0{,}52^\circ=0{,}52\cdot\dfrac{\pi}{180}\approx9{,}08\cdot10^{-3}\ \text{rad}$.</p>
<p>$d=\dfrac{D_M}{\alpha_M}=\dfrac{3540}{9{,}08\cdot10^{-3}}\approx390\,000\ \text{km}$.</p>
<p>d) $D_M$: $\dfrac{3540-3470}{3470}\approx2\,\%$; $d$: $\dfrac{390\,000-384\,000}{384\,000}\approx1{,}6\,\%$.</p>
<p>Kết quả nhạy nhất với $k$: chẳng hạn $k=2{,}5$ cho $D_M\approx3640\ \text{km}$ (sai $5\,\%$). Mép bóng tối nhoè (do nửa tối và khí quyển Trái Đất) nên $k$ khó đo chính xác.</p>
<p>Bẫy: lấy luôn $D_M=\dfrac{D_E}{k}\approx4900\ \text{km}$, quên rằng bóng tối đã hẹp đi một đoạn $D_M$ khi tới Mặt Trăng.</p>"""),
]


def tu_luan():
    parts = []
    for k, (muc, de, gi) in enumerate(TL, 1):
        parts.append(f"<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>{gi}</details>")
    return dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
                body_html="<p>Các bài còn lại của chuyên đề, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>"
                          + "".join(parts))


def kiem_so():
    AU, D_S, D_E, R_E, D_M = 1.5e8, 1.39e6, 12_740, 6370, 3470
    r = round
    # Bài 1
    S = 29.5
    assert r(S / 4, 1) == 7.4 and 5 + S / 4 == 12.375 and 5 + S / 2 == 19.75 and r(5 + 3 * S / 4, 1) == 27.1
    assert 5 + S - 31 == 3.5 and r(24 * 60 / S) == 49 and r(3 * 24 * 60 / S) == 146
    assert 18 * 60 + r(3 * 24 * 60 / S) == 20 * 60 + 26
    # Bài 2
    assert 24 * 60 / 360 == 4 and r((107.6 - 105.8) * 4, 1) == 7.2 and r((106.7 - 105) * 4, 1) == 6.8
    assert r(12 * 60 - (106.7 - 105) * 4) == 11 * 60 + 53
    assert (23.5 + 13) - 24 == 12.5 and 12.5 - (7 - 2) == 7.5
    # Bài 3
    phi = 16.5
    hs = [90 - abs(phi - d) for d in (0, 23.5, -23.5)]
    assert [r(x, 1) for x in hs] == [73.5, 83.0, 50.0]
    assert [r(1 / tan(radians(x)), 2) for x in hs] == [0.30, 0.12, 0.84]
    assert r(degrees(atan(0.16)), 1) == 9.1
    assert 90 - (phi + 23.5) == 50  # bẫy: lấy φ + δ ngày hạ chí
    # Bài 4
    s = 5000 * 0.1575
    assert 360 / 7.2 == 50 and s == 787.5 and 50 * s == 39375 and r(50 * s, -2) == 39400
    assert r(50 * s / (2 * pi), -1) == 6270 and r(tan(radians(7.2)), 3) == 0.126
    assert r((40000 - 39375) / 40000 * 100, 1) == 1.6
    C2 = 50 * 5000 * 0.185; assert r(C2) == 46250 and r((C2 - 40000) / 40000 * 100) == 16
    # Bài 5
    aS = degrees(D_S / AU); assert r(aS, 3) == 0.531 and r(D_S / AU * 1e3, 2) == 9.27
    aM = degrees(D_M / (395_000 - R_E)); assert r(aM, 3) == 0.512 and r((aM / aS) ** 2, 2) == 0.93
    aM2 = degrees(D_M / (384_000 - R_E)); assert r(aM2, 3) == 0.526 and r((aM2 / aS) ** 2, 2) == 0.98
    a = AU - 384_000; L = a * D_M / (D_S - D_M); x = 384_000 - R_E
    assert r(a / 1e8, 3) == 1.496 and r(L, -2) == 374_400 and x == 377_630 and x > L
    assert r(x - L, -1) == 3190
    assert r(D_M * (x - L) / L) == 30
    thr = D_M * 1.47e8 / D_S; assert r(thr, -3) == 367_000 and r(thr + R_E, -3) == 373_000
    assert r(D_M * AU / D_S, -3) == 374_000 and r(374_000 + R_E, -4) == 380_000
    # Bài 6
    k = 100 / 30; N = 1.5e11 / k
    assert r(k, 2) == 3.33 and r(N / 1e10, 2) == 4.5
    assert [r(au * k, 1) for au in (1, 1.52)] == [3.3, 5.1] and [r(au * k) for au in (5.2, 9.5)] == [17, 32]
    assert r(1.39e9 / N * 100, 1) == 3.1 and r(1.274e7 / N * 1e3, 2) == 0.28 and r(3.84e8 / N * 1e3, 1) == 8.5
    ly = 3e5 * 365.25 * 86400
    assert r(4.24 * 63_000, -3) == 267_000 and r(2.67e5 * k / 1e3, -1) == 890
    # Bài 7
    assert r(360 / 365.25, 3) == 0.986
    sid = 23 * 3600 + 56 * 60 + 4; sid_tinh = 1 / (1 / 24 + 1 / (365.25 * 24)) * 3600
    assert abs(sid - sid_tinh) < 1
    dd = 24 * 3600 - sid; assert dd == 236 and 90 * dd == 21_240 and r(90 * dd / 3600, 1) == 5.9
    assert r(20 * 60 - 90 * dd / 60) == 14 * 60 + 6
    assert r((108.2 - 105.8) * 4, 1) == 9.6 and r(20 * 60 - 9.6) == 19 * 60 + 50
    assert r(30 * dd / 60) == 118 and r(365.25 * dd / 3600, 1) == 23.9
    # Bài 8
    DM = D_E / (1 + 2.6); assert r(DM, -1) == 3540
    assert r(radians(0.52) * 1e3, 2) == 9.08 and r(3540 / radians(0.52), -4) == 390_000
    assert r((3540 - 3470) / 3470 * 100) == 2 and r((390_000 - 384_000) / 384_000 * 100, 1) == 1.6
    assert r(D_E / 3.5, -1) == 3640 and r((3640 - 3470) / 3470 * 100) == 5 and r(D_E / 2.6, -2) == 4900
    print("kiểm số liệu tự luận 178: đạt")


if __name__ == "__main__":
    kiem_so()
    print(len(tu_luan()["body_html"]))
