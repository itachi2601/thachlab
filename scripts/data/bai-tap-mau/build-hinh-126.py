"""Bài tập mẫu Bài 15 "Một số ứng dụng của cảm ứng điện từ" (Vật lí 12) — lesson_id 126. 4 dạng (quét dạng:
scripts/logs/batch-ra-soat/ket-qua/126.quet-dang.json). Hình: hinh_126.py. Ví dụ cũ (old/126.json): 0 dạng (mục bai_tap_mau
đã có trong DB, item 283, nhưng chưa có nội dung) nên không có tu_luan.
Bài 126 không có chủ đề riêng trong question-topics.json: dạng 1 gắn 218, dạng 2 gắn 238, dạng 3, 4 gắn chủ đề cha 67.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-126.py   (idempotent, ghi 126.json với review.checked=false)"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_126 import *

J = os.path.join(HERE, "126.json")
T218 = "Định luật Faraday và định luật Lenz"
T238 = "Máy biến áp"
T67 = "Từ thông. Hiện tượng cảm ứng điện từ"

# ═════════════ SỐ LIỆU + TỰ GIẢI ĐỘC LẬP (assert) ═════════════
# Dạng 1: ghi ta điện
f1, N1g, dPhi1 = 110.0, 6000, 0.30e-6
T1 = 1 / f1; dt1 = T1 / 2
e1 = N1g * dPhi1 / dt1
assert abs(dt1 * 1e3 - 4.5455) < 1e-3 and abs(e1 - 0.396) < 1e-3
# Dạng 2: sạc không dây
Np, Ns, Up, Um, Um2 = 24, 16, 12.0, 7.2, 5.4
ratio = Ns / Np; U2id = Up * ratio
pct1 = Um / U2id * 100; pct2 = Um2 / U2id * 100
assert abs(ratio - 0.6667) < 1e-3 and abs(U2id - 8.0) < 1e-9 and abs(pct1 - 90) < 1e-9 and abs(pct2 - 67.5) < 1e-9
assert abs(Up * Np / Ns - 18.0) < 1e-9 and abs(Up * (Np - Ns) / Np - 4.0) < 1e-9      # hai cách sai khác đáp án
# Dạng 4: bếp từ
P4, H4, V4, t1_, t2_, c4, rho = 2000.0, 0.80, 1.2e-3, 25.0, 100.0, 4200.0, 1000.0
m4 = rho * V4; Q4 = m4 * c4 * (t2_ - t1_); Pich = H4 * P4; tt = Q4 / Pich
assert abs(m4 - 1.2) < 1e-9 and abs(Q4 - 378000) < 1e-6 and abs(Pich - 1600) < 1e-9 and abs(tt - 236.25) < 1e-9
assert abs(Q4 / P4 - 189.0) < 1e-9 and abs(P4 / H4 - 2500) < 1e-9                    # cách sai: Q/P, P/H khác đáp án
assert abs(P4 * tt * H4 - Q4) < 1e-6                                                  # điện năng × H = Q

DANG = [
 dict(label="Dạng 1 · Dễ · Đàn ghi ta điện: dòng cảm ứng và suất điện động trung bình", topic=T218,
      problem_html=r"""<p>Dây La của một đàn ghi ta điện dao động với tần số $110\ \text{Hz}$ ngay phía trên bộ cảm ứng (pickup): một nam châm nhỏ quấn cuộn dây $6\,000$ vòng, nối với máy tăng âm. Dây thép đã bị nam châm từ hoá và không chạm vào cuộn dây; cuộn dây đứng yên. Trong mỗi nửa chu kì dao động của dây, từ thông qua mỗi vòng dây biến thiên một lượng $|\Delta\Phi|=0{,}30\ \mu\text{Wb}$ ($1\ \mu\text{Wb}=10^{-6}\ \text{Wb}$).</p><ol type="a"><li>Trong cuộn dây có dòng điện cảm ứng không? Nếu có, tần số của nó bằng bao nhiêu?</li><li>Tính độ lớn suất điện động cảm ứng trung bình trong cuộn dây trong nửa chu kì đó.</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Sạc không dây: điện áp thứ cấp lí tưởng và số đo", topic=T238,
      problem_html=r"""<p>Một đế sạc không dây có cuộn sơ cấp $N_1=24$ vòng nối nguồn xoay chiều, điện áp hiệu dụng $U_1=12\ \text{V}$. Cuộn thứ cấp sau lưng điện thoại có $N_2=16$ vòng. Hai cuộn đặt đồng trục, không có lõi sắt chung. Áp sát, vôn kế xoay chiều (sai số $\pm0{,}1\ \text{V}$) nối hai đầu cuộn thứ cấp chỉ $7{,}2\ \text{V}$.</p><ol type="a"><li>Coi hai cuộn ghép lí tưởng, tính điện áp $U_2$ ở cuộn thứ cấp.</li><li>Số đo $7{,}2\ \text{V}$ bằng bao nhiêu phần trăm giá trị lí tưởng? Vì sao số đo nhỏ hơn?</li><li>Kê thêm hai tấm bìa dày $1\ \text{cm}$ mỗi tấm vào giữa hai cuộn, vôn kế chỉ $5{,}4\ \text{V}$. Lúc này số đo bằng bao nhiêu phần trăm giá trị lí tưởng?</li></ol>"""),
 dict(label="Dạng 3 · Khá · Dòng điện Foucault: điều kiện xuất hiện, lực hãm và toả nhiệt", topic=T218,
      problem_html=r"""<p>Cho một tấm nhôm liền khối kích thước $100\times60\times3\ \text{mm}$ trong bốn tình huống (bỏ qua lực cản không khí):</p><ol><li>Tấm nằm yên cạnh một nam châm đứng yên.</li><li>Tấm rơi theo phương thẳng đứng qua khe giữa hai cực của một nam châm mạnh; mặt tấm vuông góc với đường sức từ.</li><li>Tấm nằm yên giữa hai cực của một nam châm điện, cường độ dòng điện nuôi nam châm tăng dần.</li><li>Tấm nằm yên trong một lò nướng đang nóng, không có nam châm nào ở gần.</li></ol><ol type="a"><li>Dòng điện Foucault xuất hiện trong tấm ở những tình huống nào?</li><li>So với khi rơi tự do không có nam châm, tấm ở tình huống (2) rơi nhanh hơn, chậm hơn hay như nhau?</li><li>Phần cơ năng của tấm mất đi trong tình huống (2) đã chuyển thành dạng năng lượng nào?</li><li>Thay bằng tấm nhôm cùng cỡ nhưng xẻ vài rãnh song song, tấm ở tình huống (2) rơi nhanh hơn hay chậm hơn tấm liền khối?</li></ol>"""),
 dict(label="Dạng 4 · Khó · Bếp từ: chọn nồi, nhiệt lượng, hiệu suất và thời gian đun", topic=T218,
      problem_html=r"""<p>Bếp từ nhà Lan ghi $2\,000\ \text{W}$ (công suất điện bếp tiêu thụ), hiệu suất $80\%$ (tỉ số giữa nhiệt lượng nước nhận được và điện năng bếp tiêu thụ). Lan có hai nồi cùng cỡ: một nồi nhôm và một nồi gang. Lan đun $1{,}2$ lít nước từ $25\ ^\circ\text{C}$ đến sôi ($100\ ^\circ\text{C}$). Nước có khối lượng riêng $1\,000\ \text{kg/m}^3$ và nhiệt dung riêng $4\,200\ \text{J/(kg·K)}$.</p><ol type="a"><li>Nên dùng nồi nào để đun nhanh hơn? Vì sao?</li><li>Tính nhiệt lượng nước nhận được.</li><li>Tính thời gian đun sôi nước.</li></ol>"""),
]

ANALYSIS = [
 [(r"“dây La … dao động với tần số $110\ \text{Hz}$ ngay phía trên bộ cảm ứng”", r"$f=110\ \text{Hz}$", r"⚠ Điều kiện có dòng cảm ứng trong mạch kín: từ thông qua mạch biến thiên"),
  (r"“cuộn dây $6\,000$ vòng, nối với máy tăng âm”", r"$N=6\,000$; mạch kín qua máy tăng âm", r"Cuộn có $N$ vòng nối tiếp"),
  (r"“không chạm vào cuộn dây; cuộn dây đứng yên”", r"Cuộn dây đứng yên", r"⚠ Xét từ thông qua cuộn dây, không xét cuộn dây có chuyển động hay không"),
  (r"“trong mỗi nửa chu kì dao động của dây”", r"$\Delta t$ = nửa chu kì", r"Liên hệ chu kì với tần số"),
  (r"“từ thông qua mỗi vòng dây biến thiên $|\Delta\Phi|=0{,}30\ \mu\text{Wb}$”", r"$|\Delta\Phi|=0{,}30\ \mu\text{Wb}$ (một vòng)", r"Đổi $\mu\text{Wb}$ ra Wb"),
  (r"“a) có dòng điện cảm ứng không? tần số?”", r"Cần kết luận và $f$ của dòng", r"Đại lượng cần tìm"),
  (r"“b) độ lớn suất điện động cảm ứng trung bình”", r"Cần $|e_c|$ (V)", r"Đại lượng cần tìm")],
 [(r"“cuộn sơ cấp $N_1=24$ vòng … $U_1=12\ \text{V}$”", r"$N_1=24$; $U_1=12\ \text{V}$ (hiệu dụng)", r"⚠ $\dfrac{U_2}{U_1}=\dfrac{N_2}{N_1}$ với $U$ là điện áp hiệu dụng"),
  (r"“cuộn thứ cấp sau lưng điện thoại có $N_2=16$ vòng”", r"$N_2=16$", r"Cuộn thứ cấp là cuộn nối với thiết bị cần nạp"),
  (r"“đồng trục, không có lõi sắt chung”", r"Không có lõi dẫn từ chung", r"Điều kiện áp dụng công thức máy biến áp"),
  (r"“vôn kế (sai số $\pm0{,}1\ \text{V}$) … chỉ $7{,}2\ \text{V}$”", r"$U_{\text{đo}}=7{,}2\pm0{,}1\ \text{V}$", r"Số đo kèm sai số; so với giá trị lí tưởng"),
  (r"“c) hai tấm bìa dày $1\ \text{cm}$ … chỉ $5{,}4\ \text{V}$”", r"Khe $2\ \text{cm}$; $U'_{\text{đo}}=5{,}4\ \text{V}$", r"Công thức $\dfrac{U_2}{U_1}=\dfrac{N_2}{N_1}$"),
  (r"“a) tính điện áp $U_2$”", r"Cần $U_2$ lí tưởng (V)", r"Đại lượng cần tìm"),
  (r"“b) bao nhiêu phần trăm … Vì sao số đo nhỏ hơn?”", r"Cần tỉ lệ (%) và nguyên nhân", r"Đại lượng cần tìm")],
 [(r"“(1) tấm nằm yên cạnh nam châm đứng yên”", r"Tấm đứng yên; nam châm đứng yên", r"⚠ Dòng Foucault là dòng cảm ứng trong khối vật dẫn; điều kiện có dòng cảm ứng là gì?"),
  (r"“(2) tấm rơi qua khe giữa hai cực nam châm mạnh”", r"Tấm chuyển động; nam châm đứng yên", r"Xét từ thông qua tấm khi tấm đi vào và đi qua khe"),
  (r"“(3) nam châm điện, dòng nuôi tăng dần”", r"Tấm đứng yên; dòng nuôi nam châm điện tăng dần", r"Cường độ dòng điện đổi thì từ trường đổi"),
  (r"“(4) trong lò nướng nóng, không có nam châm”", r"Có nhiệt độ cao; không có từ trường", r"Xét có từ trường tác dụng lên tấm hay không"),
  (r"“b) so với rơi tự do không có nam châm”", r"Cần so sánh chuyển động", r"Định luật Lenz; tác dụng của từ trường lên dòng điện"),
  (r"“c) phần cơ năng mất đi … dạng năng lượng nào”", r"Cần dạng năng lượng mới", r"Bảo toàn năng lượng: năng lượng không tự mất đi"),
  (r"“d) tấm nhôm cùng cỡ nhưng xẻ vài rãnh song song”", r"Tấm cùng cỡ, có vài rãnh song song", r"So hai tấm cùng rơi qua khe")],
 [(r"“bếp từ ghi $2\,000\ \text{W}$ (công suất điện bếp tiêu thụ)”", r"$P=2\,000\ \text{W}$ (điện tiêu thụ)", r"⚠ Phân biệt công suất điện tiêu thụ với công suất hữu ích"),
  (r"“hiệu suất $80\%$ (nhiệt nước nhận / điện năng tiêu thụ)”", r"$H=80\%$", r"Định nghĩa hiệu suất: tỉ số nhiệt hữu ích và điện năng"),
  (r"“hai nồi cùng cỡ: một nồi nhôm, một nồi gang”", r"Hai loại vật liệu đáy nồi", r"⚠ So sánh vật liệu đáy hai nồi"),
  (r"“$1{,}2$ lít nước từ $25\ ^\circ\text{C}$ đến $100\ ^\circ\text{C}$”", r"$V=1{,}2$ lít; $t_1=25\ ^\circ\text{C}$; $t_2=100\ ^\circ\text{C}$", r"Đổi lít ra kg bằng khối lượng riêng; độ tăng nhiệt độ"),
  (r"“khối lượng riêng $1\,000\ \text{kg/m}^3$; nhiệt dung riêng $4\,200\ \text{J/(kg·K)}$”", r"$D=1\,000\ \text{kg/m}^3$; $c=4\,200\ \text{J/(kg·K)}$", r"Nhiệt lượng vật thu vào khi nóng lên"),
  (r"“a) nên dùng nồi nào? Vì sao?”", r"Cần chọn nồi và lí do", r"Đại lượng cần tìm"),
  (r"“b) nhiệt lượng nước nhận”", r"Cần $Q$", r"Đại lượng cần tìm"),
  (r"“c) thời gian đun sôi”", r"Cần $t$", r"Đại lượng cần tìm")],
]

# ═════════════ LỜI GIẢI ═════════════
RC1 = [r"<strong>Khái niệm:</strong> từ thông qua mạch kín biến thiên thì có suất điện động và dòng cảm ứng; mạch không cần chuyển động.",
       r"<strong>Đàn ghi ta điện:</strong> dây thép bị từ hoá dao động làm từ thông qua cuộn dây biến thiên cùng nhịp với dây.",
       r"<strong>Công thức:</strong> $e_c=-N\dfrac{\Delta\Phi}{\Delta t}$; độ lớn $|e_c|=N\left|\dfrac{\Delta\Phi}{\Delta t}\right|$, $\Delta\Phi$ là của MỘT vòng.",
       r"⚠ <strong>Điều kiện:</strong> $\Delta\Phi$ ra Wb ($1\ \mu\text{Wb}=10^{-6}\ \text{Wb}$), $\Delta t$ ra giây."]
RC2 = [r"<strong>Khái niệm:</strong> sạc không dây là máy biến áp không lõi: cuộn sơ cấp trong đế sạc, cuộn thứ cấp sau lưng điện thoại.",
       r"<strong>Công thức:</strong> $\dfrac{U_2}{U_1}=\dfrac{N_2}{N_1}$, $U$ là điện áp hiệu dụng.",
       r"<strong>Tỉ lệ phần trăm:</strong> $\dfrac{U_{\text{đo}}}{U_{\text{lí tưởng}}}\cdot100\%$.",
       r"⚠ <strong>Điều kiện:</strong> công thức chỉ đúng khi mọi từ thông của cuộn sơ cấp xuyên qua cuộn thứ cấp; $N_2$ là cuộn nối với thiết bị cần nạp."]
RC3 = [r"<strong>Khái niệm:</strong> dòng Foucault là dòng cảm ứng khép kín trong khối vật dẫn chuyển động trong từ trường hoặc nằm trong từ trường biến thiên.",
       r"<strong>Điều kiện:</strong> từ thông qua khối biến thiên; khối nằm yên cạnh nam châm đứng yên thì không có dòng.",
       r"<strong>Hai tác dụng:</strong> lực hãm điện từ (Lenz: chống lại sự biến thiên từ thông, tức chống lại chuyển động) và toả nhiệt Joule $Q=I^2Rt$.",
       r"<strong>Dòng:</strong> $I=\dfrac{|e_c|}{R}$; điện trở của mạch dòng tăng thì dòng giảm.",
       r"⚠ <strong>Điều kiện:</strong> nhôm không nhiễm từ nhưng vẫn dẫn điện, nên vẫn có dòng Foucault."]
RC4 = [r"<strong>Bếp từ:</strong> dòng xoay chiều tần số cao trong cuộn dây tạo từ trường biến thiên; dòng Foucault toả nhiệt ngay trong đáy nồi, không có mâm nóng.",
       r"<strong>Chọn nồi:</strong> đáy nhiễm từ (gang, thép) toả nhiệt lớn; nhôm không nhiễm từ, điện trở suất thấp nên toả nhiệt rất ít.",
       r"<strong>Nhiệt lượng nước nhận:</strong> $Q=mc\Delta t$ với $\Delta t=t_2-t_1$; $m=D\cdot V$.",
       r"<strong>Hiệu suất:</strong> $H=\dfrac{Q}{A}$; công suất hữu ích $P_{\text{ích}}=H\cdot P$; thời gian $t=\dfrac{Q}{P_{\text{ích}}}$.",
       r"⚠ <strong>Điều kiện:</strong> $2\,000\ \text{W}$ là công suất điện tiêu thụ; đổi kJ ra J trước khi chia cho W."]

SOLS = [
 sol(RC1, [
  ("Dòng cảm ứng và tần số (câu a)", [P(r"Cuộn dây đứng yên, nhưng dây thép bị từ hoá dao động làm từ thông qua cuộn dây biến thiên liên tục. Mạch kín (nối máy tăng âm) và từ thông biến thiên nên có suất điện động cảm ứng và dòng cảm ứng."), P(r"Mỗi chu kì dao động của dây, từ thông tăng rồi giảm đúng một lần nên dòng cảm ứng lặp lại cùng nhịp với dây."), A(r"T:Câu a: <strong>có</strong> dòng cảm ứng, tần số bằng tần số của dây: $f=110\ \text{Hz}$.")]),
  ("Thời gian nửa chu kì", [M(r"T=\dfrac{1}{f}=\dfrac{1}{110}\approx9{,}09\cdot10^{-3}\ \text{s}"), M(r"\Delta t=\dfrac{T}{2}"), A(r"\Delta t\approx4{,}55\cdot10^{-3}\ \text{s}=4{,}55\ \text{ms}")]),
  ("Suất điện động cảm ứng (câu b)", [P(r"$|\Delta\Phi|=0{,}30\ \mu\text{Wb}=3{,}0\cdot10^{-7}\ \text{Wb}$ là của một vòng; cuộn có $N=6\,000$ vòng nối tiếp:"), M(r"|e_c|=N\,\dfrac{|\Delta\Phi|}{\Delta t}"), M(r"|e_c|=6\,000\cdot\dfrac{3{,}0\cdot10^{-7}}{4{,}55\cdot10^{-3}}"), A(r"|e_c|\approx0{,}40\ \text{V}")]),
  ("Kiểm tra", [P(r"Đơn vị: $\text{Wb/s}=\text{V}$."), P(r"Nếu lấy $\Delta t$ bằng cả chu kì thì $e_c$ chỉ còn một nửa; sai vì $\Delta\Phi$ đề cho là trong NỬA chu kì."), P(r"Cỡ vài trăm mV, hợp với tín hiệu thực tế của bộ cảm ứng; tín hiệu nhỏ nên phải qua máy tăng âm.")])],
  [r"a) Có dòng cảm ứng, tần số $110\ \text{Hz}$ (bằng tần số dây)", r"b) $|e_c|\approx0{,}40\ \text{V}$"],
  r"Nhận dạng: đề cho <strong>dây đàn rung trên cuộn dây đứng yên</strong> → từ thông qua cuộn biến thiên cùng tần số dây; $|e_c|=N\dfrac{|\Delta\Phi|}{\Delta t}$."),
 sol(RC2, [
  ("Tỉ số số vòng", [M(r"\dfrac{N_2}{N_1}=\dfrac{16}{24}"), A(r"\dfrac{N_2}{N_1}\approx0{,}667"), P(r"Cuộn thứ cấp ít vòng hơn sơ cấp: máy hạ áp, $U_2\lt U_1$.")]),
  ("Điện áp thứ cấp lí tưởng (câu a)", [M(r"\dfrac{U_2}{U_1}=\dfrac{N_2}{N_1}"), M(r"U_2=12\cdot\dfrac{16}{24}"), A(r"U_2=8{,}0\ \text{V}")]),
  ("Số đo so với lí tưởng (câu b)", [M(r"\dfrac{U_{\text{đo}}}{U_2}\cdot100\%=\dfrac{7{,}2}{8{,}0}\cdot100\%"), A(r"\dfrac{U_{\text{đo}}}{U_2}=90\%"), P(r"Số đo thấp hơn lí tưởng $0{,}8\ \text{V}$, lớn hơn nhiều so với sai số $\pm0{,}1\ \text{V}$ của vôn kế.")]),
  ("Nguyên nhân số đo nhỏ hơn (câu b)", [P(r"Hai cuộn rời nhau, không có lõi sắt dẫn từ chung nên một phần từ thông của cuộn sơ cấp rò ra ngoài, không xuyên qua cuộn thứ cấp. Từ thông qua cuộn thứ cấp biến thiên ít hơn nên suất điện động cảm ứng nhỏ hơn giá trị lí tưởng."), A(r"T:Nguyên nhân chính: <strong>từ thông rò</strong>, mô hình lí tưởng chỉ gần đúng.")]),
  ("Khi kê hai tấm bìa (câu c)", [P(r"Giá trị lí tưởng chỉ phụ thuộc $U_1$, $N_1$, $N_2$ nên vẫn là $8{,}0\ \text{V}$; khe hở chỉ làm số đo tụt."), M(r"\dfrac{5{,}4}{8{,}0}\cdot100\%"), A(r"\dfrac{U'_{\text{đo}}}{U_2}=67{,}5\%")]),
  ("Kiểm tra", [P(r"Nếu đảo tỉ số vòng thì $U_2=18\ \text{V}\gt U_1$, vô lí với cuộn thứ cấp ít vòng hơn."), P(r"Khe hở tăng, tỉ lệ giảm từ $90\%$ xuống $67{,}5\%$: hợp với từ thông rò tăng theo khe hở.")])],
  [r"a) $U_2=8{,}0\ \text{V}$", r"b) Số đo bằng $90\%$ giá trị lí tưởng; nhỏ hơn vì từ thông rò (hai cuộn không có lõi chung)", r"c) $67{,}5\%$"],
  r"Nhận dạng: đề cho <strong>hai cuộn dây với số vòng khác nhau</strong> → $\dfrac{U_2}{U_1}=\dfrac{N_2}{N_1}$ cho giá trị lí tưởng; số đo luôn thấp hơn."),
 sol(RC3, [
  ("Tình huống có dòng Foucault (câu a)", [P(r"(1): tấm và nam châm cùng đứng yên, từ thông qua tấm không đổi nên không có dòng."), P(r"(2): tấm chuyển động vào vùng có từ trường, từ thông qua tấm biến thiên nên có dòng."), P(r"(3): tấm đứng yên nhưng từ trường biến thiên theo dòng nuôi nam châm điện, từ thông qua tấm biến thiên nên có dòng."), P(r"(4): lò nướng nóng nhưng không có từ trường nên không có dòng cảm ứng; tấm nóng do truyền nhiệt."), A(r"T:Câu a: tình huống <strong>(2) và (3)</strong>.")]),
  ("Tấm rơi trong tình huống (2) (câu b)", [P(r"Từ thông qua tấm thay đổi khi tấm đi vào khe nên có dòng Foucault. Theo Lenz, từ trường cảm ứng chống lại sự biến thiên từ thông, tức chống lại chuyển động của tấm: dòng cảm ứng chịu lực từ cản tấm."), P(r"Nhôm không bị nam châm hút; lực cản do dòng cảm ứng sinh ra."), A(r"T:Câu b: tấm rơi <strong>chậm hơn</strong> rơi tự do.")]),
  ("Năng lượng (câu c)", [P(r"Lực hãm điện từ thực hiện công cản nên cơ năng của tấm giảm. Năng lượng không tự mất: cơ năng chuyển thành điện năng của dòng Foucault, rồi toả thành nhiệt trong chính tấm."), M(r"Q=I^2Rt"), A(r"T:Câu c: <strong>nhiệt Joule</strong> toả ra trong tấm nhôm.")]),
  ("Tấm có rãnh xẻ (câu d)", [P(r"Hai tấm cùng cỡ, từ thông qua tấm biến thiên như nhau nên suất điện động cảm ứng như nhau. Rãnh xẻ cắt các đường dòng khép kín, điện trở của mạch dòng tăng."), M(r"I=\dfrac{|e_c|}{R}"), P(r"$R$ tăng thì $I$ giảm, lực hãm điện từ yếu đi."), A(r"T:Câu d: tấm có rãnh <strong>rơi nhanh hơn</strong> tấm liền khối.")]),
  ("Kiểm tra", [P(r"Khớp thí nghiệm trong bài: tấm nhôm liền khối giữa hai cực tắt dao động sau khoảng $3{,}8\ \text{s}$, tấm có rãnh xẻ sau khoảng $13{,}3\ \text{s}$."), P(r"Nhôm không nhiễm từ nhưng vẫn dẫn điện; dòng Foucault chỉ cần từ thông biến thiên.")])],
  ["a) Tình huống (2) và (3)", "b) Rơi chậm hơn rơi tự do, do lực hãm điện từ", "c) Nhiệt Joule toả ra trong tấm", "d) Tấm có rãnh xẻ rơi nhanh hơn tấm liền khối"],
  r"Nhận dạng: đề có <strong>khối kim loại trong từ trường</strong> → xét từ thông có biến thiên không; có thì có lực hãm và toả nhiệt."),
 sol(RC4, [
  ("Chọn nồi (câu a)", [P(r"Bếp từ không có mâm nóng: nhiệt sinh ngay trong đáy nồi nhờ dòng Foucault."), P(r"Nồi gang nhiễm từ nên tập trung được từ thông, dòng Foucault toả nhiệt lớn. Nồi nhôm không nhiễm từ và có điện trở suất thấp nên toả nhiệt rất ít."), A(r"T:Câu a: nên dùng <strong>nồi gang</strong>.")]),
  ("Nhiệt lượng nước nhận (câu b)", [M(r"m=D\cdot V=1\,000\cdot1{,}2\cdot10^{-3}=1{,}2\ \text{kg}"), M(r"Q=mc\Delta t=1{,}2\cdot4\,200\cdot(100-25)"), A(r"Q=378\,000\ \text{J}=378\ \text{kJ}")]),
  ("Công suất hữu ích", [M(r"P_{\text{ích}}=H\cdot P=0{,}80\cdot2\,000"), A(r"P_{\text{ích}}=1\,600\ \text{W}")]),
  ("Thời gian đun sôi (câu c)", [M(r"t=\dfrac{Q}{P_{\text{ích}}}=\dfrac{378\,000}{1\,600}"), A(r"t\approx236\ \text{s}\approx3{,}9\ \text{phút}")]),
  ("Kiểm tra", [P(r"Đơn vị: $\text{J}/\text{W}=\text{s}$."), P(r"Cùng cỡ thí nghiệm trong bài: $1{,}0$ lít nước từ $25{,}0\ ^\circ\text{C}$ sôi sau $4$ phút ở $2\,000\ \text{W}$."), P(r"Điện năng tiêu thụ $A=P\,t\approx2\,000\cdot236\approx472\ \text{kJ}$; $80\%$ của nó là $378\ \text{kJ}$, khớp $Q$.")])],
  ["a) Nồi gang", r"b) $Q=378\ \text{kJ}$", r"c) $t\approx236\ \text{s}\approx3{,}9$ phút"],
  r"Nhận dạng: đề có <strong>bếp từ, hiệu suất, đun nước</strong> → chọn nồi nhiễm từ; $Q=mc\Delta t$; $t=\dfrac{Q}{H\cdot P}$."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC (khớp 1-1 với .bt-step của SOLS) ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>dây đàn rung trên cuộn dây đứng yên</b> → nghĩ tới <b>từ thông biến thiên</b>, rồi <b>|e_c| = N|ΔΦ|/Δt</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Dòng cảm ứng và tần số", r"Cuộn dây đứng yên, dây không chạm vào cuộn dây. Dòng cảm ứng trong cuộn dây thế nào?",
       loi=r"Buộc dòng cảm ứng vào chuyển động của cuộn dây; điều kiện thật là từ thông qua cuộn dây biến thiên.",
       lua_chon=[(r"Có dòng, tần số bằng tần số dao động của dây", True),
                 (r"Không có dòng, vì cuộn dây đứng yên", r"Điều kiện là từ thông qua cuộn dây biến thiên, không đòi cuộn dây chuyển động. Dây thép bị từ hoá dao động làm từ thông qua cuộn đổi liên tục."),
                 (r"Có dòng, nhưng chỉ khi dây chạm vào cuộn dây", r"Dây không cần chạm; dây thép bị từ hoá dao động làm từ thông qua cuộn dây biến thiên ngay từ xa.")]),
  buoc("Thời gian nửa chu kì", r"Khoảng thời gian $\Delta t$ của nửa chu kì dao động bằng bao nhiêu (đơn vị ms)?", 4.55, "ms", 0.05,
       loi=r"Lấy $\Delta t$ bằng cả chu kì (quên chia đôi), hoặc để $\Delta t$ ở giây rồi trộn với ms.",
       ke=[(r"Tính chu kì $T=\dfrac{1}{f}$ rồi lấy một nửa", True),
           (r"Lấy luôn $\Delta t=f$", r"Tần số có đơn vị Hz, không phải thời gian; thời gian là nghịch đảo của tần số."),
           (r"Lấy $\Delta t=T$, cả một chu kì", r"Đề cho $\Delta\Phi$ trong nửa chu kì nên $\Delta t$ phải là nửa chu kì; lấy cả chu kì thì $\Delta t$ gấp đôi.")]),
  buoc("Suất điện động cảm ứng", r"Độ lớn suất điện động cảm ứng trung bình trong cuộn dây bằng bao nhiêu (đơn vị V)?", 0.396, "V", 0.01,
       loi=r"Quên nhân với $N$ (chỉ lấy suất điện động của một vòng), hoặc quên đổi $\mu\text{Wb}$ ra Wb nên lệch rất nhiều lần.",
       ke=[(r"$|e_c|=N\dfrac{|\Delta\Phi|}{\Delta t}$ với $\Delta\Phi$ của một vòng, đổi ra Wb", True),
           (r"$|e_c|=\dfrac{|\Delta\Phi|}{\Delta t}$ (bỏ $N$)", r"Cuộn gồm $N$ vòng nối tiếp, mỗi vòng cho suất điện động như nhau nên cả cuộn gấp $N$ lần."),
           (r"$|e_c|=N\,|\Delta\Phi|\cdot\Delta t$", r"Faraday là tốc độ biến thiên từ thông, phải chia cho $\Delta t$; nhân thì đơn vị không phải V.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>hai cuộn dây khác số vòng</b> → nghĩ tới <b>U₂/U₁ = N₂/N₁</b> (lí tưởng), rồi so số đo với lí tưởng.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Tỉ số số vòng", r"Tỉ số $\dfrac{N_2}{N_1}$ bằng bao nhiêu?", 0.667, "", 0.005,
       loi=r"Đảo tỉ số (chia $N_1$ cho $N_2$) vì nhầm cuộn nào là thứ cấp."),
  buoc("Điện áp thứ cấp lí tưởng", r"Điện áp thứ cấp lí tưởng $U_2$ bằng bao nhiêu (đơn vị V)?", 8.0, "V", 0.1,
       loi=r"Dùng tỉ số đảo nên điện áp thứ cấp lớn hơn sơ cấp, trái với việc thứ cấp ít vòng hơn; hoặc coi điện áp không đổi qua hai cuộn.",
       ke=[(r"Áp dụng $\dfrac{U_2}{U_1}=\dfrac{N_2}{N_1}$ của máy biến áp lí tưởng rồi suy ra $U_2$", True),
           (r"Lấy $U_2=U_1\dfrac{N_1}{N_2}$", r"$N_2$ là cuộn nối với thiết bị cần nạp; thứ cấp ít vòng hơn sơ cấp thì điện áp thứ cấp phải nhỏ hơn, công thức này cho lớn hơn."),
           (r"Lấy $U_2=U_1\dfrac{N_1-N_2}{N_1}$", r"Điện áp tỉ lệ với số vòng chứ không tỉ lệ với hiệu số vòng.")]),
  buoc("Số đo so với lí tưởng", r"Số đo $7{,}2\ \text{V}$ đạt bao nhiêu phần trăm giá trị lí tưởng?", 90, "%", 0.5,
       loi=r"Chia ngược (lí tưởng chia cho số đo) nên ra hơn $100\%$, hoặc lấy hiệu của hai giá trị làm phần trăm.",
       ke=[(r"Chia số đo cho giá trị lí tưởng rồi nhân $100\%$", True),
           (r"Chia giá trị lí tưởng cho số đo", r"Ra tỉ số lớn hơn $1$, nghĩa là số đo vượt giá trị lí tưởng; ngược với thực tế vì có từ thông rò."),
           (r"Lấy hiệu hai giá trị chia cho $U_1$", r"Mẫu số phải là giá trị lí tưởng mà đề so sánh, không phải $U_1$; hiệu số cũng cho phần hụt chứ không cho phần đạt được.")]),
  buoc("Nguyên nhân số đo nhỏ hơn", r"Nguyên nhân chính khiến số đo nhỏ hơn giá trị lí tưởng là gì?",
       loi=r"Quy hết cho sai số dụng cụ hoặc cho tần số, quên rằng hai cuộn không có lõi sắt chung.",
       lua_chon=[(r"Một phần từ thông của cuộn sơ cấp rò ra ngoài, không xuyên qua cuộn thứ cấp", True),
                 (r"Sai số $\pm0{,}1\ \text{V}$ của vôn kế", r"Sai số này nhỏ hơn rất nhiều so với độ chênh giữa số đo và giá trị lí tưởng nên không giải thích được."),
                 (r"Tần số ở cuộn thứ cấp nhỏ hơn tần số ở cuộn sơ cấp", r"Tần số của suất điện động cảm ứng bằng tần số biến thiên của từ thông, tức bằng tần số cuộn sơ cấp; thứ thay đổi là độ lớn.")],
       ke=[(r"Xét nguyên nhân làm số đo khác giá trị lí tưởng", True),
           (r"Tính lại $U_2$ bằng $U_1\dfrac{N_1}{N_2}$ xem có khớp số đo không", r"Đảo tỉ số cho giá trị lớn hơn $U_1$, càng xa số đo; và công thức lí tưởng đúng là $U_2=U_1\dfrac{N_2}{N_1}$."),
           (r"Lấy số đo làm $U_2$ rồi tính ngược số vòng $N_2$", r"Đề đã cho $N_2$; đổi $N_2$ cho khớp số đo không giải thích vì sao số đo thấp hơn giá trị lí tưởng của số vòng thật.")]),
  buoc("Khi kê hai tấm bìa", r"Với hai tấm bìa, số đo $5{,}4\ \text{V}$ đạt bao nhiêu phần trăm giá trị lí tưởng?", 67.5, "%", 0.5,
       loi=r"Tính lại giá trị lí tưởng theo khe hở mới; giá trị lí tưởng chỉ phụ thuộc điện áp sơ cấp và tỉ số vòng.",
       ke=[(r"Giữ nguyên giá trị lí tưởng đã tính, chia số đo mới cho nó", True),
           (r"Tính lại giá trị lí tưởng với khe hở mới", r"Công thức lí tưởng không chứa khoảng cách; khe hở chỉ làm số đo tụt, không đổi tỉ số vòng."),
           (r"Lấy hiệu hai số đo chia cho $U_1$", r"Đề hỏi số đo mới so với giá trị lí tưởng; hiệu hai số đo chia cho $U_1$ không trả lời câu đó.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>khối kim loại trong từ trường</b> → hỏi <b>từ thông có biến thiên không</b>, rồi xét lực hãm và nhiệt Joule.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Tình huống có dòng Foucault", r"Dòng điện Foucault xuất hiện trong tấm ở những tình huống nào?",
       loi=r"Cho rằng cứ ở cạnh nam châm là có dòng, hoặc chỉ tính khi tấm chuyển động.",
       lua_chon=[(r"Tình huống (2) và (3)", True),
                 (r"Chỉ tình huống (2), vì chỉ khi tấm chuyển động mới có dòng", r"Ở (3) tấm đứng yên nhưng từ trường biến thiên nên từ thông qua tấm vẫn biến thiên, vẫn có dòng Foucault."),
                 (r"Tình huống (1), (2) và (3), vì cứ có nam châm là có dòng", r"Ở (1) tấm và nam châm cùng đứng yên, từ thông không đổi nên không có dòng; điều kiện là từ thông biến thiên, không phải có mặt trong từ trường.")]),
  buoc("Tấm rơi trong tình huống (2)", r"So với rơi tự do khi không có nam châm, tấm ở tình huống (2) rơi thế nào?",
       loi=r"Nghĩ rằng nam châm hút nhôm, hoặc cho rằng dòng cảm ứng chỉ làm nóng mà không tác dụng lực.",
       lua_chon=[(r"Chậm hơn, vì dòng Foucault chịu lực từ chống lại chuyển động của tấm", True),
                 (r"Nhanh hơn, vì nam châm hút tấm xuống", r"Nhôm không bị nam châm hút; lực tác dụng lên tấm là lực từ lên dòng cảm ứng, theo Lenz lực này chống lại chuyển động."),
                 (r"Như nhau, vì dòng cảm ứng chỉ làm tấm nóng lên", r"Dòng điện trong từ trường chịu lực từ; theo Lenz lực này chống lại sự biến thiên từ thông, tức cản chuyển động của tấm.")],
       ke=[(r"Xét từ thông qua tấm khi tấm đi vào khe, rồi áp dụng định luật Lenz cho dòng cảm ứng", True),
           (r"Bỏ qua dòng cảm ứng vì nhôm không nhiễm từ", r"Nhôm vẫn dẫn điện: từ thông biến thiên là có dòng cảm ứng, không cần vật liệu nhiễm từ."),
           (r"Chỉ xét trọng lực vì nam châm không tác dụng lên nhôm", r"Nam châm không hút nhôm, nhưng từ trường vẫn tác dụng lực lên dòng cảm ứng trong nhôm.")]),
  buoc("Năng lượng", r"Phần cơ năng của tấm mất đi trong lúc rơi qua nam châm chuyển thành gì?",
       loi=r"Cho rằng cơ năng vẫn bảo toàn, hoặc cho rằng năng lượng mất đi biến mất.",
       lua_chon=[(r"Nhiệt Joule toả ra trong tấm do dòng Foucault", True),
                 (r"Không mất: cơ năng của tấm vẫn bảo toàn", r"Có lực hãm điện từ thực hiện công cản nên cơ năng của tấm giảm, không bảo toàn."),
                 (r"Điện năng cất giữ trong nam châm", r"Nam châm chỉ tạo từ trường, không tích điện năng; năng lượng của dòng cảm ứng toả thành nhiệt ngay trong tấm.")],
       ke=[(r"Áp dụng bảo toàn năng lượng: tìm dạng năng lượng mà hệ nhận thêm", True),
           (r"Lấy độ giảm thế năng bằng độ tăng động năng của tấm", r"Đó là bảo toàn cơ năng, chỉ đúng khi không có lực cản; ở đây có lực hãm điện từ nên phần thế năng giảm lớn hơn phần động năng tăng."),
           (r"Tính công của trọng lực rồi dừng, không xét năng lượng của dòng cảm ứng", r"Công của trọng lực chỉ cho phần thế năng giảm; phần không thành động năng phải đi đâu đó, chính là năng lượng của dòng cảm ứng.")]),
  buoc("Tấm có rãnh xẻ", r"Tấm xẻ rãnh ở tình huống (2) rơi nhanh hơn hay chậm hơn tấm liền khối?",
       loi=r"Cho rằng rãnh làm tấm dẫn điện tốt hơn, hoặc cho rằng rãnh làm tấm nhẹ hơn nên đổi hẳn chuyển động.",
       lua_chon=[(r"Nhanh hơn, vì rãnh cắt đường dòng nên điện trở mạch dòng tăng, dòng nhỏ, lực hãm yếu", True),
                 (r"Chậm hơn, vì rãnh làm tấm dẫn điện tốt hơn nên dòng lớn hơn", r"Rãnh cắt các đường dòng khép kín nên điện trở của mạch dòng tăng chứ không giảm; cùng suất điện động mà điện trở lớn thì dòng nhỏ."),
                 (r"Như nhau, vì rãnh không làm đổi từ thông qua tấm", r"Từ thông và suất điện động không đổi, nhưng dòng $I=\dfrac{|e_c|}{R}$ còn phụ thuộc điện trở; điện trở tăng thì dòng giảm, lực hãm yếu đi.")],
       ke=[(r"Xét rãnh xẻ làm đổi đại lượng nào của mạch dòng cảm ứng", True),
           (r"So khối lượng của hai tấm", r"Rãnh chỉ lấy đi vài gam nhôm, không đủ làm đổi hẳn chuyển động."),
           (r"So từ thông qua hai tấm, cho rằng tấm có rãnh nhận ít từ thông hơn", r"Hai tấm cùng cỡ nên từ thông qua chúng gần như nhau; chỗ khác nhau nằm ở mạch dòng.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>bếp từ, hiệu suất, đun nước</b> → nghĩ tới <b>nhiệt sinh ở đâu</b>, rồi <b>nhiệt nước nhận</b> và <b>công suất hữu ích</b>.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Chọn nồi", r"Nên dùng nồi nào để đun nhanh hơn, và vì sao?",
       loi=r"Nghĩ bếp từ truyền nhiệt từ mặt bếp sang nồi như bếp điện nên chọn nồi dẫn nhiệt tốt.",
       lua_chon=[(r"Nồi gang: đáy nhiễm từ nên dòng Foucault toả nhiệt lớn ngay trong đáy nồi", True),
                 (r"Nồi nhôm, vì nhôm dẫn nhiệt tốt nên nhiệt từ mặt bếp truyền vào nồi nhanh", r"Bếp từ không có mâm nóng để truyền nhiệt; nhiệt sinh ngay trong đáy nồi nhờ dòng Foucault, nên tính chất điện từ của đáy nồi mới quyết định."),
                 (r"Nồi nào cũng được, vì dòng Foucault xuất hiện ở mọi kim loại nên nhiệt toả ra như nhau", r"Nhôm cũng có dòng Foucault, nhưng không nhiễm từ và điện trở suất thấp nên công suất toả nhiệt rất nhỏ; nồi gang nóng nhanh hơn rõ rệt.")]),
  buoc("Nhiệt lượng nước nhận", r"Nước nhận nhiệt lượng $Q$ bằng bao nhiêu (đơn vị kJ)?", 378, "kJ", 2,
       loi=r"Thế nhiệt độ cuối $100\ ^\circ\text{C}$ thay cho độ tăng nhiệt độ, hoặc quên đổi lít ra kilôgam, hoặc ghi kết quả ở J cạnh đơn vị kJ.",
       ke=[(r"Đổi thể tích sang khối lượng, rồi $Q=mc\Delta t$ với $\Delta t$ là độ tăng nhiệt độ", True),
           (r"Lấy $Q=mc\,t_2$ với $t_2$ là nhiệt độ sôi", r"Nhiệt lượng cần độ tăng nhiệt độ $\Delta t=t_2-t_1$, không phải nhiệt độ cuối."),
           (r"Lấy $Q=P\cdot t$ với $P$ là công suất ghi trên bếp", r"Chưa biết $t$; hơn nữa $P\,t$ là điện năng bếp tiêu thụ, không phải nhiệt lượng nước nhận.")]),
  buoc("Công suất hữu ích", r"Công suất hữu ích truyền vào nước bằng bao nhiêu (đơn vị W)?", 1600, "W", 10,
       loi=r"Lấy luôn công suất ghi trên bếp làm công suất hữu ích, hoặc chia cho hiệu suất thay vì nhân.",
       ke=[(r"Nhân công suất điện với hiệu suất", True),
           (r"Chia công suất điện cho hiệu suất", r"Chia cho số nhỏ hơn $1$ nên ra số lớn hơn công suất bếp, vô lí vì công suất hữu ích không thể vượt công suất điện."),
           (r"Lấy công suất hữu ích bằng công suất ghi trên bếp", r"Công suất ghi trên bếp là công suất điện tiêu thụ; một phần hao đi (nung nóng nồi, toả ra không khí) nên không truyền hết vào nước.")]),
  buoc("Thời gian đun sôi", r"Thời gian đun sôi nước bằng bao nhiêu (đơn vị giây)?", 236, "s", 2,
       loi=r"Chia nhiệt lượng cho công suất ghi trên bếp (bỏ qua hao phí), hoặc thế $Q$ ở kJ cùng $P$ ở W.",
       ke=[(r"Chia nhiệt lượng nước nhận (đã đổi ra J) cho công suất hữu ích", True),
           (r"Chia nhiệt lượng cho công suất ghi trên bếp", r"Nhiệt lượng nước nhận chỉ được cấp với công suất hữu ích; chia cho công suất ghi trên bếp cho thời gian ngắn hơn thực tế."),
           (r"Nhân nhiệt lượng với công suất hữu ích", r"Từ $P=\dfrac{Q}{t}$ suy ra $t=\dfrac{Q}{P}$; phép nhân cho đơn vị J·W, không phải giây.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
write(J, 126, "Bài 15. Một số ứng dụng của cảm ứng điện từ", DANG, BUILD, ANALYSIS, SOLS)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code)"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
