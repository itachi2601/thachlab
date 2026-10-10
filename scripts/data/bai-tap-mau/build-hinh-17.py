"""Bài tập mẫu Bài 16 "Phản ứng phân hạch, phản ứng nhiệt hạch và ứng dụng" (Vật lí 12) — lesson_id 17. 5 dạng (quét dạng:
scripts/logs/batch-ra-soat/ket-qua/17.quet-dang.json). Hình: hinh_17.py. Bài chưa có mục bai_tap_mau trong DB nên không có ví dụ cũ / tự luận.
Hằng số đúng như lý thuyết bài: 1 u = 931,5 MeV/c²; 1 MeV = 1,6·10⁻¹³ J; N_A = 6,02·10²³ mol⁻¹; than 2,7·10⁷ J/kg.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-17.py   (idempotent, ghi 17.json với review.checked=false)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_17 import *

J = os.path.join(HERE, "17.json")
T71 = "Phản ứng phân hạch, phản ứng nhiệt hạch"
T225 = "Định luật bảo toàn trong phản ứng hạt nhân"
T226 = "Năng lượng toả ra của phản ứng hạt nhân"
T227 = "Nhà máy điện hạt nhân và phản ứng nhiệt hạch"

# ═════════════ KIỂM SỐ (độc lập với lời giải: nếu lệch thì dừng) ═════════════
U, MEV, NA, QCOAL = 931.5, 1.6e-13, 6.02e23, 2.7e7
# D1: hệ số nhân
assert abs(50200 / 50000 - 1.004) < 1e-9 and abs(50400 / 50200 - 1.004) < 5e-5
# D2: bảo toàn A, Z
_x = (235 + 1) - (139 + 95); assert _x == 2 and 92 + 0 == 54 + 38 + _x * 0
_A = 2 + 2 - 3; _Z = 1 + 1 - 2; assert (_A, _Z) == (1, 0)
for A_, Z_ in ((1, 1), (0, -1)):          # lựa chọn sai ở bước "hạt X" phải KHÔNG thoả cả hai phương trình
    assert not (2 + 2 == 3 + A_ and 1 + 1 == 2 + Z_)
assert 235 != 139 + 95                    # bỏ nơtron bắn vào → x lệch 1
# D3: D–T và N + α
mD, mT, mHe, mn = 2.013553, 3.015501, 4.001506, 1.008665
mN, mO, mp = 13.999231, 16.994740, 1.007276
dm1 = mD + mT - mHe - mn; W1 = dm1 * U
assert abs(dm1 - 0.018883) < 1e-9 and abs(W1 - 17.5895) < 1e-3 and abs(W1 * MEV - 2.8143e-12) < 1e-15
dm2 = mN + mHe - mO - mp; W2 = dm2 * U
assert abs(dm2 + 0.001279) < 1e-9 and abs(W2 + 1.1914) < 1e-3
assert abs((mD + mT - mHe) * U - 17.589) > 1          # quên nơtron → lệch hẳn
assert abs(round(dm2, 4) * U - W2) < 0.1              # làm tròn 4 chữ số vẫn đủ trong sai số bước (cho phép)
# D4: 1,0 g đơteri
N4 = 1.0 / 2.0 * NA; E4 = N4 * 17.6 * MEV; m4 = E4 / QCOAL
assert abs(N4 - 3.01e23) < 1e19 and abs(17.6 * MEV - 2.816e-12) < 1e-15 and abs(E4 - 8.476e11) < 2e8 and abs(m4 - 3.139e4) < 5
# D5: lò 900 MW, 30 ngày
t5 = 30 * 24 * 3600; E5 = 900e6 * t5; w5 = 200 * MEV; N5 = E5 / w5; mU = N5 / NA * 235 / 1000; coal5 = E5 / QCOAL / 1000
assert t5 == 2592000 and abs(E5 - 2.3328e15) < 1e10 and abs(w5 - 3.2e-11) < 1e-15 and abs(N5 - 7.29e25) < 1e22
assert abs(mU - 28.46) < 0.01 and abs(coal5 - 86400) < 1

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
FIS = r"${}^{1}_{0}\text{n}+{}^{235}_{92}\text{U}\to{}^{95}_{39}\text{Y}+{}^{138}_{53}\text{I}+3\,{}^{1}_{0}\text{n}$"
DT = r"${}^{2}_{1}\text{H}+{}^{3}_{1}\text{H}\to{}^{4}_{2}\text{He}+{}^{1}_{0}\text{n}$"
CONST = r"Lấy $1\ \text{MeV}=1{,}6\cdot10^{-13}\ \text{J}$, $N_A=6{,}02\cdot10^{23}\ \text{mol}^{-1}$."
DANG = [
 dict(label="Dạng 1 · Dễ · Phân hạch, nhiệt hạch và hệ số nhân nơtron k", topic=T71,
      problem_html=r"<p>Hai phản ứng sau xảy ra ở hai thiết bị khác nhau:</p><p>(1) " + FIS + r"</p><p>(2) " + DT + r"</p>"
      r"<p>Phản ứng (1) xảy ra trong một lò phản ứng. Người vận hành đếm số nơtron ở ba thế hệ liên tiếp: $50\,000$; $50\,200$; $50\,400$.</p>"
      r"""<ol type="a"><li>Phản ứng (1) và (2) thuộc loại nào?</li><li>Tính hệ số nhân nơtron $k$ của lò và cho biết công suất lò thay đổi thế nào.</li><li>Muốn công suất lò ổn định, người vận hành phải làm gì với thanh điều khiển?</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Bảo toàn số nuclôn và điện tích, tìm hạt x", topic=T225,
      problem_html=r"<p>Cho hai phản ứng hạt nhân:</p><p>(1) ${}^{1}_{0}\text{n}+{}^{235}_{92}\text{U}\to{}^{139}_{54}\text{Xe}+{}^{95}_{38}\text{Sr}+x\,{}^{1}_{0}\text{n}$</p>"
      r"<p>(2) ${}^{2}_{1}\text{H}+{}^{2}_{1}\text{H}\to{}^{3}_{2}\text{He}+{}^{A}_{Z}\text{X}$</p>"
      r"""<ol type="a"><li>Tìm số nơtron $x$ ở phản ứng (1) và kiểm tra điện tích hai vế có bằng nhau không.</li><li>Xác định hạt X ở phản ứng (2).</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Năng lượng toả ra hay thu vào của một phản ứng", topic=T226,
      problem_html=r"<p>Xét hai phản ứng hạt nhân:</p><p>(1) " + DT + r"</p><p>(2) ${}^{14}_{7}\text{N}+{}^{4}_{2}\text{He}\to{}^{17}_{8}\text{O}+{}^{1}_{1}\text{p}$</p>"
      r"<p>Khối lượng các hạt nhân: $m_{\text{D}}=2{,}013553\ \text{u}$; $m_{\text{T}}=3{,}015501\ \text{u}$; $m_{\text{He}}=4{,}001506\ \text{u}$; $m_{\text{n}}=1{,}008665\ \text{u}$; "
      r"$m_{\text{N}}=13{,}999231\ \text{u}$; $m_{\text{O}}=16{,}994740\ \text{u}$; $m_{\text{p}}=1{,}007276\ \text{u}$.</p>"
      r"<p>Cho $1\ \text{u}=931{,}5\ \text{MeV}/c^2$; $1\ \text{MeV}=1{,}6\cdot10^{-13}\ \text{J}$.</p>"
      r"""<ol type="a"><li>Tính năng lượng của phản ứng (1) theo MeV và theo jun.</li><li>Phản ứng (2) toả hay thu năng lượng? Tính năng lượng đó theo MeV.</li></ol>"""),
 dict(label="Dạng 4 · Khá · Năng lượng của cả lượng nhiên liệu nhiệt hạch, so với than", topic=T226,
      problem_html=r"<p>Phản ứng nhiệt hạch " + DT + r" toả ra $17{,}6\ \text{MeV}$. Một lò thử nghiệm đốt hết $1{,}0\ \text{g}$ đơteri (D, khối lượng mol $2{,}0\ \text{g/mol}$) với lượng triti dư.</p>"
      r"<p>" + CONST + r" Than đá toả $2{,}7\cdot10^{7}\ \text{J/kg}$.</p>"
      r"""<ol type="a"><li>Tính số phản ứng đã xảy ra.</li><li>Tính năng lượng toả ra theo jun.</li><li>Năng lượng đó bằng đốt bao nhiêu kilôgam than đá?</li></ol>"""),
 dict(label="Dạng 5 · Khó · Công suất lò phản ứng và lượng U-235 phân hạch", topic=T227,
      problem_html=r"<p>Một lò phản ứng hạt nhân có công suất nhiệt $900\ \text{MW}$, chạy liên tục $30$ ngày. Giả sử toàn bộ nhiệt toả ra đến từ phân hạch ${}^{235}_{92}\text{U}$, mỗi phân hạch toả trung bình $200\ \text{MeV}$.</p>"
      r"<p>" + CONST + r" Khối lượng mol của U-235 là $235\ \text{g/mol}$; than đá toả $2{,}7\cdot10^{7}\ \text{J/kg}$.</p>"
      r"""<ol type="a"><li>Tính năng lượng lò toả ra trong $30$ ngày, theo jun.</li><li>Tính khối lượng U-235 đã phân hạch.</li><li>Năng lượng đó bằng đốt bao nhiêu tấn than đá?</li></ol>"""),
]
FORMS = ["ly_thuyet", "bai_tap", "bai_tap", "bai_tap", "bai_tap"]

BUILD = [d1, d2, d3, d4, d5]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (hàng "cần tìm" chỉ ghi "Đại lượng cần tìm"; ô ⚠ chỉ nêu câu hỏi điều kiện) ═════════════
ANALYSIS = [
 [(r"“(1) $\ldots{}^{235}_{92}\text{U}\ldots3\,{}^{1}_{0}\text{n}$”", r"Hạt nhân tham gia: ${}^{235}_{92}\text{U}$ và một nơtron; sản phẩm: hai hạt nhân và $3$ nơtron", "Khái niệm: phản ứng hạt nhân; hạt nhân nặng hay nhẹ"),
  (r"“(2) ${}^{2}_{1}\text{H}+{}^{3}_{1}\text{H}\to{}^{4}_{2}\text{He}+{}^{1}_{0}\text{n}$”", r"Hạt nhân tham gia: hai hạt nhân hiđrô; sản phẩm: heli và một nơtron", "Khái niệm: phản ứng hạt nhân; hạt nhân nặng hay nhẹ"),
  (r"“a) thuộc loại nào”", "Cần loại của (1) và (2)", "⚠ Hạt nhân tham gia là nặng hay nhẹ? Việc có nơtron ở vế phải có đủ để phân biệt hai loại không?"),
  (r"“số nơtron ở ba thế hệ liên tiếp: $50\,000$; $50\,200$; $50\,400$”", r"$N_1=50\,000$; $N_2=50\,200$; $N_3=50\,400$", "Khái niệm: thế hệ nơtron, hệ số nhân"),
  (r"“b) hệ số nhân nơtron $k$”", "Cần $k$", "Đại lượng cần tìm"),
  (r"“công suất lò thay đổi thế nào”", "Cần kết luận về công suất", "⚠ So $k$ với mốc nào thì biết số nơtron tăng, giữ hay giảm?"),
  (r"“c) thanh điều khiển”", "Cần thao tác với thanh điều khiển", "Vai trò của thanh điều khiển trong lò phản ứng")],
 [(r"“(1) $\ldots{}^{139}_{54}\text{Xe}+{}^{95}_{38}\text{Sr}+x\,{}^{1}_{0}\text{n}$”", r"Sản phẩm: Xe ($A=139$, $Z=54$), Sr ($A=95$, $Z=38$), $x$ nơtron", "Khái niệm: số nuclôn $A$ và số prôtôn $Z$ của từng hạt"),
  (r"“(1) ${}^{1}_{0}\text{n}+{}^{235}_{92}\text{U}\to\ldots$”", r"Vế trái: nơtron ($A=1$, $Z=0$) và U ($A=235$, $Z=92$)", "⚠ Vế trái có những hạt nào? Có hạt nào dễ bị bỏ sót khi cộng không?"),
  (r"“a) tìm số nơtron $x$”", "Cần $x$", "Đại lượng cần tìm"),
  (r"“kiểm tra điện tích hai vế có bằng nhau không”", "Cần tổng $Z$ của hai vế", "Định luật bảo toàn điện tích"),
  (r"“(2) ${}^{2}_{1}\text{H}+{}^{2}_{1}\text{H}\to{}^{3}_{2}\text{He}+{}^{A}_{Z}\text{X}$”", r"Vế trái: hai hạt có $A=2$, $Z=1$; vế phải: He ($A=3$, $Z=2$) và X chưa biết", "⚠ Có mấy ẩn số? Cần mấy phương trình để tìm hạt X?"),
  (r"“b) xác định hạt X”", r"Cần $A$ và $Z$ của X", "Đại lượng cần tìm")],
 [(r"“(1) ${}^{2}_{1}\text{H}+{}^{3}_{1}\text{H}\to{}^{4}_{2}\text{He}+{}^{1}_{0}\text{n}$”", "Vế trái: hai hạt; vế phải: hai hạt", r"⚠ Đã cộng đủ khối lượng mọi hạt ở mỗi vế, kể cả nơtron, chưa?"),
  (r"“$m_{\text{D}}=2{,}013553\ \text{u}$; $m_{\text{T}}=3{,}015501\ \text{u}$; $m_{\text{He}}=4{,}001506\ \text{u}$; $m_{\text{n}}=1{,}008665\ \text{u}$”", r"Khối lượng bốn hạt của (1), đơn vị u", "Khái niệm: khối lượng nghỉ của các hạt trước và sau phản ứng"),
  (r"“(2) ${}^{14}_{7}\text{N}+{}^{4}_{2}\text{He}\to{}^{17}_{8}\text{O}+{}^{1}_{1}\text{p}$” và khối lượng của N, O, p", r"Bốn hạt của (2); $m_{\text{N}}$, $m_{\text{O}}$, $m_{\text{p}}$ cho trong đề, $m_{\text{He}}$ dùng lại", "Khái niệm: khối lượng nghỉ của các hạt trước và sau phản ứng"),
  (r"“$1\ \text{u}=931{,}5\ \text{MeV}/c^2$; $1\ \text{MeV}=1{,}6\cdot10^{-13}\ \text{J}$”", "Hai hệ số đổi", "Hệ thức khối lượng – năng lượng; đổi MeV sang jun"),
  (r"“a) năng lượng của phản ứng (1) theo MeV và theo jun”", r"Cần $W$ (MeV) và $W$ (J)", "Đại lượng cần tìm"),
  (r"“b) phản ứng (2) toả hay thu năng lượng”", r"Cần dấu và độ lớn của $W$", "⚠ Hiệu hai tổng khối lượng mang dấu gì thì phản ứng toả, mang dấu gì thì thu?")],
 [(r"“toả ra $17{,}6\ \text{MeV}$”", r"$W=17{,}6\ \text{MeV}$ mỗi phản ứng", "Khái niệm: năng lượng toả ra của một phản ứng"),
  (r"“$1{,}0\ \text{g}$ đơteri (khối lượng mol $2{,}0\ \text{g/mol}$)”", r"$m=1{,}0\ \text{g}$; $M=2{,}0\ \text{g/mol}$", "Khái niệm: số mol, số hạt nhân, hằng số Avôgađrô"),
  (r"“với lượng triti dư”", "Chất nào hết trước là đơteri", "⚠ Chất nào hết trước thì quyết định số phản ứng? Mỗi phản ứng dùng mấy hạt đơteri?"),
  (r"“$1\ \text{MeV}=1{,}6\cdot10^{-13}\ \text{J}$, $N_A=6{,}02\cdot10^{23}\ \text{mol}^{-1}$”", "Hai hằng số đổi", "Đổi MeV sang jun; số hạt trong một mol"),
  (r"“than đá toả $2{,}7\cdot10^{7}\ \text{J/kg}$”", r"$q=2{,}7\cdot10^{7}\ \text{J/kg}$", "Năng suất toả nhiệt của nhiên liệu"),
  (r"“a) số phản ứng; b) năng lượng toả ra theo jun; c) bao nhiêu kilôgam than”", r"Cần $N$, $E$ (J), $m_{than}$", "Đại lượng cần tìm")],
 [(r"“công suất nhiệt $900\ \text{MW}$”", r"$P=900\ \text{MW}$", "Khái niệm: công suất"),
  (r"“chạy liên tục $30$ ngày”", r"$t=30$ ngày", "⚠ Đơn vị thời gian đi cùng đơn vị oát là gì? Có cần đổi không?"),
  (r"“toàn bộ nhiệt toả ra đến từ phân hạch ${}^{235}_{92}\text{U}$; mỗi phân hạch toả $200\ \text{MeV}$”", r"$W_1=200\ \text{MeV}$ mỗi phân hạch", "⚠ Nhiệt của lò đến từ đâu? Mỗi hạt nhân U-235 phân hạch mấy lần?"),
  (r"“$1\ \text{MeV}=\ldots$; $N_A=\ldots$; $235\ \text{g/mol}$; than đá $2{,}7\cdot10^{7}\ \text{J/kg}$”", "Các hằng số đổi và năng suất toả nhiệt của than", "Đổi MeV sang jun; số hạt trong một mol; năng suất toả nhiệt"),
  (r"“a) năng lượng trong $30$ ngày; b) khối lượng U-235; c) bao nhiêu tấn than”", r"Cần $E$ (J), $m_{U}$, $m_{than}$", "Đại lượng cần tìm")],
]

# ═════════════ LỜI GIẢI ═════════════
RC1 = [r"<strong>Khái niệm:</strong> phân hạch là hạt nhân rất nặng hấp thụ nơtron rồi vỡ thành hai hạt nhân nhẹ hơn; nhiệt hạch là hạt nhân rất nhẹ kết hợp thành hạt nhân nặng hơn.",
       r"<strong>Khái niệm:</strong> hệ số nhân $k$ là tỉ số số nơtron thế hệ sau so với thế hệ trước.",
       r"<strong>Định luật:</strong> $k\lt1$ phản ứng dây chuyền tắt dần; $k=1$ tự duy trì; $k\gt1$ tăng nhanh theo từng thế hệ.",
       r"<strong>Công thức:</strong> $k=\dfrac{N_{sau}}{N_{trước}}$.",
       r"⚠ <strong>Điều kiện:</strong> mốc so sánh của $k$ là $1$; thanh điều khiển hấp thụ nơtron, đẩy vào thì $k$ giảm, kéo ra thì $k$ tăng."]
RC2 = [r"<strong>Khái niệm:</strong> mỗi hạt có số nuclôn $A$ và điện tích $Z$ (nơtron: $A=1$, $Z=0$).",
       r"<strong>Định luật:</strong> phản ứng hạt nhân bảo toàn điện tích và bảo toàn số nuclôn.",
       r"<strong>Công thức:</strong> $\sum A_{trước}=\sum A_{sau}$ · $\sum Z_{trước}=\sum Z_{sau}$.",
       r"⚠ <strong>Điều kiện:</strong> cộng đủ mọi hạt ở mỗi vế, kể cả nơtron bắn vào; mỗi ẩn cần một phương trình riêng."]
RC3 = [r"<strong>Khái niệm:</strong> độ hụt khối của phản ứng $\Delta m=\sum m_{trước}-\sum m_{sau}$ (khác độ hụt khối của một hạt nhân).",
       r"<strong>Định luật:</strong> $W=\Delta m\,c^2$ với $1\ \text{u}\cdot c^2=931{,}5\ \text{MeV}$.",
       r"<strong>Công thức:</strong> $W=\Delta m\cdot931{,}5$ (MeV) · $1\ \text{MeV}=1{,}6\cdot10^{-13}\ \text{J}$.",
       r"⚠ <strong>Điều kiện:</strong> trước nặng hơn thì toả ($W\gt0$), trước nhẹ hơn thì thu ($W\lt0$); cộng đủ mọi hạt ở mỗi vế, giữ 6 chữ số thập phân."]
RC4 = [r"<strong>Khái niệm:</strong> số hạt nhân trong mẫu $N=\dfrac{m}{M}N_A$; mỗi hạt đơteri tham gia đúng một phản ứng nên số phản ứng bằng số hạt đơteri.",
       r"<strong>Định luật:</strong> các phản ứng toả năng lượng độc lập nên năng lượng cộng được.",
       r"<strong>Công thức:</strong> $E=N\cdot W$ · $m_{than}=\dfrac{E}{q}$.",
       r"⚠ <strong>Điều kiện:</strong> triti dư nên đơteri hết trước; $W$ đề cho bằng MeV, phải đổi sang jun."]
RC5 = [r"<strong>Khái niệm:</strong> công suất $P$ là năng lượng toả ra trong một giây; nhiệt của lò đến từ các phân hạch U-235.",
       r"<strong>Định luật:</strong> các phân hạch độc lập nên năng lượng cộng được; mỗi hạt nhân U-235 phân hạch một lần.",
       r"<strong>Công thức:</strong> $E=Pt$ · $N=\dfrac{E}{W_1}$ · $m=\dfrac{N}{N_A}M$.",
       r"⚠ <strong>Điều kiện:</strong> $t$ phải đổi ra giây khi $P$ tính bằng oát; $W_1$ phải đổi từ MeV ra jun."]

SOLS = [
 sol(RC1, [
  ("Nhận ra loại phản ứng (câu a)", [P(r"Phản ứng (1): hạt nhân ${}^{235}_{92}\text{U}$ rất nặng hấp thụ một nơtron, vỡ thành hai hạt nhân nhẹ hơn và thải $3$ nơtron."),
        P(r"Phản ứng (2): hai hạt nhân hiđrô rất nhẹ kết hợp thành hạt nhân heli."),
        A(r"T:(1) là <strong>phân hạch</strong>; (2) là <strong>nhiệt hạch</strong>.")]),
  ("Hệ số nhân (câu b)", [M(r"k=\dfrac{N_2}{N_1}=\dfrac{50\,200}{50\,000}"), A(r"k=1{,}004")]),
  ("Công suất thay đổi thế nào (câu b)", [P(r"Mốc so sánh là $1$:"), M(r"k=1{,}004\gt1"),
        A(r"T:Mỗi thế hệ có nhiều nơtron hơn thế hệ trước một chút: số nơtron và công suất <strong>tăng dần</strong>.")]),
  ("Thanh điều khiển (câu c)", [P(r"Muốn đưa $k$ về đúng $1$ phải bớt nơtron; thanh điều khiển (bo, cađimi) hấp thụ nơtron mạnh."),
        A(r"T:<strong>Đẩy thanh điều khiển sâu thêm</strong> cho tới khi $k=1$.")]),
  ("Kiểm tra", [M(r"50\,200\cdot1{,}004=50\,400{,}8\approx50\,400"),
        P(r"Khớp với thế hệ thứ ba. Dù $k$ chỉ hơn $1$ bốn phần nghìn, số nơtron vẫn tăng theo cấp số nhân qua nhiều thế hệ nên phải chỉnh $k$ về $1$.")])],
  [r"a) (1) phân hạch ; (2) nhiệt hạch", r"b) $k=1{,}004$ ; công suất tăng dần", r"c) Đẩy thanh điều khiển sâu thêm để $k=1$"],
  r"Nhận dạng: đề cho <strong>hạt nhân tham gia</strong> hoặc <strong>số nơtron các thế hệ</strong> → xét hạt nhân nặng vỡ hay nhẹ ghép, $k=\dfrac{N_{sau}}{N_{trước}}$ rồi so với $1$."),
 sol(RC2, [
  ("Tổng số nuclôn vế trái", [P(r"Cộng cả nơtron bắn vào và hạt nhân urani:"), M(r"A_{trái}=235+1"), A(r"A_{trái}=236")]),
  ("Tìm số nơtron $x$ (câu a)", [P(r"Số nuclôn hai vế bằng nhau:"), M(r"236=139+95+x"), M(r"x=236-234"), A(r"x=2")]),
  ("Kiểm tra điện tích (câu a)", [P(r"Nơtron không mang điện nên $Z=0$:"), M(r"Z_{trái}=92+0=92"), M(r"Z_{phải}=54+38+x\cdot0=92"),
        A(r"T:Hai vế cùng bằng $92$: điện tích bảo toàn, kết quả $x=2$ hợp lí.")]),
  ("Xác định hạt X (câu b)", [P(r"Hai ẩn $A$ và $Z$ cần hai phương trình:"), M(r"2+2=3+A\Rightarrow A=1"), M(r"1+1=2+Z\Rightarrow Z=0"),
        A(r"T:Hạt có $A=1$, $Z=0$ là <strong>nơtron</strong> ${}^{1}_{0}\text{n}$.")]),
  ("Kiểm tra", [P(r"Phản ứng (2) là ${}^{2}_{1}\text{H}+{}^{2}_{1}\text{H}\to{}^{3}_{2}\text{He}+{}^{1}_{0}\text{n}$, một phản ứng nhiệt hạch có nơtron bay ra."),
        P(r"Phân hạch thải từ $2$ đến $3$ nơtron mỗi lần, như đã nêu ở bài lý thuyết: $x=2$ nằm trong khoảng đó.")])],
  [r"a) $x=2$ ; điện tích hai vế cùng bằng $92$", r"b) X là nơtron ${}^{1}_{0}\text{n}$"],
  r"Nhận dạng: phương trình có <strong>hạt hoặc số hạt chưa biết</strong> → viết hai phương trình $\sum A$ và $\sum Z$, nhớ cộng cả hạt bắn vào."),
 sol(RC3, [
  ("Độ hụt khối phản ứng (1)", [P(r"Cộng đủ các hạt ở mỗi vế, kể cả nơtron:"), M(r"\sum m_{trước}=m_D+m_T=2{,}013553+3{,}015501=5{,}029054\ \text{u}"),
        M(r"\sum m_{sau}=m_{He}+m_n=4{,}001506+1{,}008665=5{,}010171\ \text{u}"), M(r"\Delta m=5{,}029054-5{,}010171"), A(r"\Delta m=0{,}018883\ \text{u}")]),
  ("Năng lượng phản ứng (1) theo MeV (câu a)", [P(r"Hệ số $931{,}5\ \text{MeV/u}$ đã chứa sẵn $c^2$:"), M(r"W=\Delta m\cdot931{,}5=0{,}018883\cdot931{,}5"), A(r"W\approx17{,}59\ \text{MeV}")]),
  ("Đổi sang jun (câu a)", [M(r"W=17{,}59\cdot1{,}6\cdot10^{-13}"), A(r"W\approx2{,}81\cdot10^{-12}\ \text{J}")]),
  ("Độ hụt khối phản ứng (2)", [M(r"\sum m_{trước}=m_N+m_{He}=13{,}999231+4{,}001506=18{,}000737\ \text{u}"),
        M(r"\sum m_{sau}=m_O+m_p=16{,}994740+1{,}007276=18{,}002016\ \text{u}"), M(r"\Delta m=18{,}000737-18{,}002016"), A(r"\Delta m=-0{,}001279\ \text{u}")]),
  ("Toả hay thu (câu b)", [P(r"$\Delta m\lt0$: khối lượng nghỉ sau phản ứng lớn hơn trước."), A(r"T:Phản ứng (2) <strong>thu</strong> năng lượng, cần cấp năng lượng cho phản ứng.")]),
  ("Năng lượng phản ứng (2) (câu b)", [M(r"W=\Delta m\cdot931{,}5=-0{,}001279\cdot931{,}5"), A(r"W\approx-1{,}19\ \text{MeV}")]),
  ("Kiểm tra", [P(r"Phản ứng D–T toả cỡ $17{,}6\ \text{MeV}$ như đã nêu ở bài lý thuyết: khớp."),
        P(r"Với (2), $|\Delta m|$ chỉ cỡ $10^{-3}\ \text{u}$ nên mỗi khối lượng phải giữ $6$ chữ số thập phân; làm tròn xuống $3$ chữ số thập phân thì $\Delta m$ còn $-0{,}001\ \text{u}$ (khoảng $-0{,}93\ \text{MeV}$), lệch khoảng $20\ \%$."),
        P(r"Phản ứng thu năng lượng chỉ xảy ra khi hạt bắn vào mang đủ động năng.")])],
  [r"a) $W\approx17{,}59\ \text{MeV}\approx2{,}81\cdot10^{-12}\ \text{J}$", r"b) Phản ứng (2) thu năng lượng, $W\approx-1{,}19\ \text{MeV}$"],
  r"Nhận dạng: đề cho <strong>khối lượng các hạt hai vế</strong> và hỏi năng lượng → $\Delta m=\sum m_{trước}-\sum m_{sau}$, xét dấu rồi nhân $931{,}5$."),
 sol(RC4, [
  ("Số phản ứng (câu a)", [P(r"Số hạt nhân đơteri trong mẫu; mỗi hạt tham gia một phản ứng:"), M(r"N=\dfrac{m}{M}N_A=\dfrac{1{,}0}{2{,}0}\cdot6{,}02\cdot10^{23}"), A(r"N=3{,}01\cdot10^{23}\ \text{phản ứng}")]),
  ("Năng lượng một phản ứng theo jun", [M(r"W=17{,}6\cdot1{,}6\cdot10^{-13}"), A(r"W=2{,}82\cdot10^{-12}\ \text{J}")]),
  ("Năng lượng cả mẫu (câu b)", [M(r"E=N\cdot W=3{,}01\cdot10^{23}\cdot2{,}816\cdot10^{-12}"), A(r"E\approx8{,}48\cdot10^{11}\ \text{J}")]),
  ("Khối lượng than tương đương (câu c)", [M(r"m_{than}=\dfrac{E}{q}=\dfrac{8{,}48\cdot10^{11}}{2{,}7\cdot10^{7}}"), A(r"m_{than}\approx3{,}14\cdot10^{4}\ \text{kg}")]),
  ("Kiểm tra", [P(r"Cỡ $31$ tấn than cho $1{,}0\ \text{g}$ đơteri. Bài lý thuyết: $1\ \text{g}$ U-235 phân hạch tương đương cỡ $2{,}6$ tấn than, nên mỗi gam đơteri (có triti dư đi kèm) toả nhiều hơn cỡ $12$ lần mỗi gam U-235; nếu tính cả khối lượng triti đã dùng thì chỉ còn nhiều hơn cỡ $5$ lần."),
        P(r"Đơn vị: $\text{J}\ /\ (\text{J/kg})=\text{kg}$, đúng.")])],
  [r"a) $N\approx3{,}01\cdot10^{23}$ phản ứng", r"b) $E\approx8{,}48\cdot10^{11}\ \text{J}$", r"c) $m_{than}\approx3{,}14\cdot10^{4}\ \text{kg}$ (cỡ $31$ tấn)"],
  r"Nhận dạng: đề cho <strong>khối lượng nhiên liệu (gam)</strong> và hỏi năng lượng → đếm $N=\dfrac{m}{M}N_A$ rồi nhân năng lượng một phản ứng."),
 sol(RC5, [
  ("Năng lượng lò toả ra trong 30 ngày (câu a)", [P(r"Đổi thời gian ra giây:"), M(r"t=30\cdot24\cdot3600=2{,}592\cdot10^{6}\ \text{s}"),
        M(r"E=Pt=900\cdot10^{6}\cdot2{,}592\cdot10^{6}"), A(r"E\approx2{,}33\cdot10^{15}\ \text{J}")]),
  ("Năng lượng một phân hạch theo jun", [M(r"W_1=200\cdot1{,}6\cdot10^{-13}"), A(r"W_1=3{,}2\cdot10^{-11}\ \text{J}")]),
  ("Số phân hạch", [M(r"N=\dfrac{E}{W_1}=\dfrac{2{,}33\cdot10^{15}}{3{,}2\cdot10^{-11}}"), A(r"N\approx7{,}29\cdot10^{25}\ \text{hạt nhân}")]),
  ("Khối lượng U-235 (câu b)", [P(r"Đổi số hạt ra mol rồi ra khối lượng:"), M(r"n=\dfrac{N}{N_A}=\dfrac{7{,}29\cdot10^{25}}{6{,}02\cdot10^{23}}\approx121\ \text{mol}"),
        M(r"m=n\cdot M=121{,}1\cdot235\approx2{,}85\cdot10^{4}\ \text{g}"), A(r"m\approx28{,}5\ \text{kg}")]),
  ("Khối lượng than tương đương (câu c)", [M(r"m_{than}=\dfrac{E}{q}=\dfrac{2{,}33\cdot10^{15}}{2{,}7\cdot10^{7}}\approx8{,}64\cdot10^{7}\ \text{kg}"), A(r"m_{than}\approx8{,}64\cdot10^{4}\ \text{tấn}")]),
  ("Kiểm tra", [P(r"Bài lý thuyết: $1\ \text{g}$ U-235 tương đương cỡ $2{,}6$ tấn than; $28\,460\ \text{g}$ tương đương cỡ $7{,}4\cdot10^{4}$ tấn, cùng bậc với kết quả (đề dùng $200\ \text{MeV}$ thay vì $173\ \text{MeV}$ nên lớn hơn một chút)."),
        P(r"Đơn vị: $\text{W}\cdot\text{s}=\text{J}$ và $\text{J}\ /\ (\text{J/kg})=\text{kg}$, đúng.")])],
  [r"a) $E\approx2{,}33\cdot10^{15}\ \text{J}$", r"b) $m_{U}\approx28{,}5\ \text{kg}$", r"c) $m_{than}\approx8{,}64\cdot10^{4}$ tấn"],
  r"Nhận dạng: đề cho <strong>công suất và thời gian chạy</strong> của lò → tính năng lượng lò toả ra, chia cho năng lượng một phân hạch để đếm hạt nhân."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC (khớp 1-1 với .bt-step của SOLS) ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>hạt nhân tham gia</b> hoặc <b>số nơtron các thế hệ</b> → nghĩ tới <b>loại phản ứng</b> và <b>hệ số nhân $k$</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Nhận ra loại phản ứng", "Phản ứng (1) và (2) lần lượt thuộc loại nào?",
       loi=r"Thấy nơtron ở vế phải của cả hai phản ứng nên cho cả hai là phân hạch, hoặc gán nhầm tên loại cho hạt nhân nặng và nhẹ.",
       lua_chon=[(r"(1) phân hạch ; (2) nhiệt hạch", True),
                 (r"(1) nhiệt hạch ; (2) phân hạch", r"Phân hạch là hạt nhân nặng (U-235) vỡ ra; nhiệt hạch là hạt nhân nhẹ (hiđrô) kết hợp lại. Đáp án này đảo hai loại."),
                 (r"Cả hai đều là phân hạch vì đều thải nơtron", r"Có nơtron ở vế phải không quyết định loại phản ứng. Phải nhìn hạt nhân tham gia: nặng vỡ ra hay nhẹ kết hợp lại.")]),
  buoc("Hệ số nhân", "Hệ số nhân nơtron $k$ của lò bằng bao nhiêu?", 1.004, "", 0.0005,
       loi=r"Lấy số nơtron thế hệ trước chia thế hệ sau nên ra số nhỏ hơn $1$ và kết luận lò đang tắt dần, hoặc lấy hiệu hai thế hệ thay vì tỉ số.",
       ke=[(r"Lấy số nơtron thế hệ sau chia số nơtron thế hệ trước", True),
           (r"Lấy hiệu số nơtron hai thế hệ liên tiếp", r"$k$ là tỉ số không có đơn vị; hiệu hai thế hệ là một số nơtron, không phải hệ số nhân."),
           (r"Lấy số nơtron thế hệ trước chia số nơtron thế hệ sau", r"Phép chia ngược cho số nhỏ hơn $1$ dù số nơtron đang tăng, làm kết luận bị đảo chiều.")]),
  buoc("Công suất thay đổi thế nào", "Công suất của lò thay đổi thế nào?",
       loi=r"Thấy $k$ gần $1$ nên kết luận công suất giữ nguyên, hoặc so $k$ với mốc $2$ thay vì mốc $1$.",
       lua_chon=[(r"Tăng dần theo từng thế hệ, vì $k$ lớn hơn $1$", True),
                 (r"Giữ nguyên, vì $k$ xấp xỉ $1$", r"Chỉ khi $k$ đúng bằng $1$ công suất mới giữ nguyên. $k$ lớn hơn $1$ dù chỉ một chút thì mỗi thế hệ vẫn nhiều nơtron hơn thế hệ trước."),
                 (r"Giảm dần, vì $k$ nhỏ hơn $2$", r"Mốc so sánh của $k$ là $1$, không phải $2$. $k$ lớn hơn $1$ thì số nơtron tăng.")],
       ke=[(r"Đặt $k$ cạnh mốc $1$: lớn hơn thì tăng, bằng thì giữ, nhỏ hơn thì giảm", True),
           (r"Đặt $k$ cạnh mốc $2$", r"Mốc $2$ không có ý nghĩa gì với phản ứng dây chuyền; mốc đúng là $1$ (mỗi thế hệ vừa đủ thay thế thế hệ trước)."),
           (r"So $k$ với mốc $0$: $k$ dương thì số nơtron tăng", r"$k$ là tỉ số của hai số nơtron nên luôn dương; mốc $0$ không phân biệt được tăng, giữ hay giảm. Mốc đúng là $1$.")]),
  buoc("Thanh điều khiển", "Người vận hành phải làm gì với thanh điều khiển để công suất ổn định?",
       loi=r"Rút thanh điều khiển ra vì nghĩ thanh làm tăng công suất, hoặc để nguyên vì $k$ chỉ hơn $1$ rất ít.",
       lua_chon=[(r"Đẩy thanh sâu thêm để hấp thụ nơtron, đưa $k$ về đúng $1$", True),
                 (r"Rút thanh ra thêm cho $k$ lớn hơn nữa", r"Rút thanh làm bớt chất hấp thụ nơtron nên $k$ tăng, công suất càng tăng thêm."),
                 (r"Giữ nguyên thanh, vì $k$ chỉ hơn $1$ rất ít nên vẫn an toàn", r"Số nơtron tăng theo cấp số nhân qua nhiều thế hệ, nên chênh lệch nhỏ cũng tích lại thành công suất lớn; phải đưa $k$ về đúng $1$.")],
       ke=[(r"Xác định thanh điều khiển tác động lên lượng nơtron theo hướng nào, rồi chọn chiều di chuyển thanh", True),
           (r"Thêm thanh nhiên liệu vào lò để lò tự cân bằng", r"Thêm nhiên liệu làm có nhiều hạt nhân phân hạch hơn, $k$ càng tăng; việc điều chỉnh $k$ là của thanh điều khiển."),
           (r"Coi thanh điều khiển là nguồn nơtron: đưa vào để sinh thêm nơtron", r"Thanh điều khiển hấp thụ nơtron chứ không sinh nơtron.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>phương trình có hạt hoặc số hạt chưa biết</b> → nghĩ tới <b>cân bằng số nuclôn $A$ và điện tích $Z$</b> hai vế.",
  cap_do=1, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Tổng số nuclôn vế trái", "Tổng số nuclôn ở vế trái của phản ứng (1) là bao nhiêu?", 236, "", 0,
       loi=r"Bỏ quên nơtron bắn vào ở vế trái, chỉ tính số nuclôn của hạt nhân urani."),
  buoc("Tìm số nơtron $x$", "Số nơtron $x$ sinh ra ở phản ứng (1) là bao nhiêu?", 2, "", 0,
       loi=r"Lấy số khối của urani trừ tổng số khối hai mảnh vỡ nên $x$ lệch đi một đơn vị.",
       ke=[(r"Cân bằng số nuclôn: tổng ở vế trái bằng tổng ở vế phải", True),
           (r"Lấy số khối của urani trừ tổng số khối của hai mảnh vỡ", r"Vế trái còn có nơtron bắn vào; bỏ nó thì $x$ lệch đi một."),
           (r"Cân bằng điện tích, vì nơtron không mang điện nên suy ra $x$", r"Nơtron có $Z=0$ nên $x$ biến mất khỏi phương trình điện tích. $x$ chỉ tìm được từ số nuclôn.")]),
  buoc("Kiểm tra điện tích", "Tổng điện tích ($Z$) ở vế phải của phản ứng (1) bằng bao nhiêu?", 92, "", 0,
       loi=r"Coi mỗi nơtron có $Z=1$ nên cộng thêm vào tổng, hoặc cộng số khối thay vì số prôtôn.",
       ke=[(r"Cộng điện tích ($Z$) của mọi hạt ở vế phải", True),
           (r"Cộng $Z$ của Xe, Sr rồi cộng thêm $x$ nơtron, coi mỗi nơtron có $Z=1$", r"Nơtron không mang điện, $Z=0$; chỉ prôtôn mới có $Z=1$."),
           (r"Cộng số khối $A$ của Xe, Sr và $x$ nơtron", r"Đó là phương trình số nuclôn, đã dùng ở bước trước; bước này cần tổng $Z$.")]),
  buoc("Xác định hạt X", "Hạt X ở phản ứng (2) là hạt nào?",
       loi=r"Chỉ cân bằng số nuclôn rồi chọn đại một hạt có $A=1$ (prôtôn hoặc nơtron) mà không dùng phương trình điện tích.",
       lua_chon=[(r"Nơtron ${}^{1}_{0}\text{n}$", True),
                 (r"Prôtôn ${}^{1}_{1}\text{p}$", r"Với prôtôn thì tổng $Z$ ở vế phải là $3$, khác tổng $Z$ ở vế trái là $2$."),
                 (r"Êlectron ${}^{0}_{-1}\text{e}$", r"Với $A=0$ thì tổng số nuclôn ở vế phải chỉ là $3$, khác vế trái là $4$.")],
       ke=[(r"Lập hai phương trình: tổng $A$ và tổng $Z$ hai vế bằng nhau", True),
           (r"Chỉ cân bằng số nuclôn $A$, điện tích tự suy ra", r"Hai ẩn $A$ và $Z$ cần hai phương trình; với $A=1$ vẫn còn cả prôtôn lẫn nơtron, phải xét $Z$ mới chọn được."),
           (r"Chọn X sao cho tổng khối lượng hai vế bằng nhau", r"Khối lượng nghỉ không bảo toàn trong phản ứng hạt nhân; chỉ $A$ và $Z$ mới bảo toàn.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>khối lượng các hạt hai vế</b> và hỏi năng lượng → nghĩ tới <b>độ hụt khối của phản ứng</b> và <b>dấu</b> của nó.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Độ hụt khối phản ứng (1)", "Độ hụt khối $\\Delta m$ của phản ứng (1) (tổng khối lượng trước trừ tổng khối lượng sau) bằng bao nhiêu u?", 0.018883, "u", 0.0003,
       loi=r"Quên cộng khối lượng nơtron ở vế phải, hoặc lấy tổng sau trừ tổng trước nên ra số âm."),
  buoc("Năng lượng (1) theo MeV", "Năng lượng của phản ứng (1) là bao nhiêu MeV?", 17.59, "MeV", 0.1,
       loi=r"Nhân thêm $c^2$ sau khi đã nhân hệ số $931{,}5$, hoặc chia cho $931{,}5$ thay vì nhân.",
       ke=[(r"Nhân $\Delta m$ (u) với $931{,}5\ \text{MeV/u}$", True),
           (r"Nhân $\Delta m$ với $c^2=9\cdot10^{16}$ rồi đọc ra MeV", r"$931{,}5\ \text{MeV/u}$ đã chứa sẵn $c^2$; nhân thêm là sai cả đơn vị."),
           (r"Chia $\Delta m$ cho $931{,}5$", r"Đổi từ u sang MeV là nhân với $931{,}5$; chia cho ra số rất nhỏ.")]),
  buoc("Đổi sang jun", "Năng lượng của phản ứng (1) theo jun là bao nhiêu (nhập hệ số $a$ của kết quả $a\\cdot10^{n}\\ \\text{J}$)?", 2.81, "×10ⁿ J", 0.03,
       loi=r"Dùng $1\ \text{eV}=1{,}6\cdot10^{-19}\ \text{J}$ cho MeV nên lệch sáu bậc mười, hoặc chia thay vì nhân.",
       ke=[(r"Nhân năng lượng (MeV) với $1{,}6\cdot10^{-13}\ \text{J/MeV}$", True),
           (r"Nhân năng lượng (MeV) với $1{,}6\cdot10^{-19}$", r"$1{,}6\cdot10^{-19}\ \text{J}$ là $1\ \text{eV}$; một MeV gấp $10^6$ lần một eV."),
           (r"Chia năng lượng (MeV) cho $1{,}6\cdot10^{-13}$", r"Đổi MeV sang jun là nhân với hệ số đổi; chia cho ra số rất lớn, sai đơn vị.")]),
  buoc("Độ hụt khối phản ứng (2)", "Với phản ứng (2), tổng khối lượng trước trừ tổng khối lượng sau bằng bao nhiêu u (kể cả dấu)?", -0.001279, "u", 0.0003,
       loi=r"Lấy sau trừ trước nên đổi dấu và kết luận phản ứng toả năng lượng, hoặc làm tròn khối lượng làm mất hiệu số.",
       ke=[(r"Cộng khối lượng N và He ở vế trái, cộng O và p ở vế phải, rồi lấy trước trừ sau", True),
           (r"Lấy tổng khối lượng trước chia tổng khối lượng sau", r"$\Delta m$ là hiệu hai tổng khối lượng, không phải tỉ số; thương này không có đơn vị u."),
           (r"Tính độ hụt khối của từng hạt nhân rồi lấy hiệu hai vế", r"Đó là độ hụt khối của hạt nhân (liên quan năng lượng liên kết), khác độ hụt khối của phản ứng; đề cũng không cho độ hụt khối từng hạt.")]),
  buoc("Toả hay thu", "Phản ứng (2) toả hay thu năng lượng?",
       loi=r"Thấy $\Delta m$ khác $0$ là kết luận toả, hoặc quên xét dấu của $\Delta m$.",
       lua_chon=[(r"Thu năng lượng, vì tổng khối lượng trước nhỏ hơn tổng khối lượng sau", True),
                 (r"Toả năng lượng, vì $\Delta m$ khác $0$", r"$\Delta m$ khác $0$ chỉ cho biết có trao đổi năng lượng; dấu của $\Delta m$ mới cho biết chiều: trước nhẹ hơn sau thì thu."),
                 (r"Không toả, không thu, vì $\Delta m$ rất nhỏ", r"$\Delta m$ nhỏ nhưng nhân với $931{,}5\ \text{MeV/u}$ vẫn ra cỡ MeV, không bỏ qua được.")],
       ke=[(r"Xét dấu của $\Delta m$ vừa tính: âm thì khối lượng nghỉ tăng", True),
           (r"So tổng điện tích hai vế", r"Điện tích luôn bảo toàn ở mọi phản ứng nên hai vế luôn bằng nhau, không cho biết toả hay thu."),
           (r"So tổng số nuclôn hai vế", r"Số nuclôn cũng luôn bảo toàn, không phân biệt được toả hay thu.")]),
  buoc("Năng lượng (2) theo MeV", "Năng lượng của phản ứng (2) bằng bao nhiêu MeV (kể cả dấu)?", -1.19, "MeV", 0.03,
       loi=r"Bỏ dấu âm nên đọc nhầm là phản ứng toả, hoặc quên nhân hệ số đổi.",
       ke=[(r"Nhân $\Delta m$ (kể cả dấu) với $931{,}5\ \text{MeV/u}$", True),
           (r"Nhân độ lớn của $\Delta m$ rồi bỏ dấu", r"Dấu âm cho biết phản ứng thu năng lượng; bỏ dấu là mất thông tin này."),
           (r"Chia $\Delta m$ cho $931{,}5$", r"Đổi u sang MeV là nhân với $931{,}5$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>khối lượng nhiên liệu (gam)</b> và hỏi năng lượng → nghĩ tới <b>đếm số hạt nhân</b> rồi nhân năng lượng một phản ứng.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Số phản ứng", "Số phản ứng đã xảy ra là bao nhiêu (nhập hệ số $a$ của kết quả $a\\cdot10^{n}$)?", 3.01, "×10ⁿ", 0.02,
       loi=r"Dừng ở số mol, hoặc lấy khối lượng mol phân tử D₂ ($4\ \text{g/mol}$) thay cho khối lượng mol của đơteri nên số hạt lệch hẳn."),
  buoc("Năng lượng một phản ứng theo jun", "Năng lượng một phản ứng theo jun là bao nhiêu (nhập hệ số $a$ của kết quả $a\\cdot10^{n}\\ \\text{J}$)?", 2.82, "×10ⁿ J", 0.02,
       loi=r"Dùng $1\ \text{eV}=1{,}6\cdot10^{-19}\ \text{J}$ cho MeV nên lệch sáu bậc mười.",
       ke=[(r"Nhân năng lượng (MeV) với $1{,}6\cdot10^{-13}\ \text{J/MeV}$", True),
           (r"Nhân năng lượng (MeV) với $1{,}6\cdot10^{-19}$", r"$1{,}6\cdot10^{-19}\ \text{J}$ là $1\ \text{eV}$; một MeV gấp $10^6$ lần một eV."),
           (r"Chia năng lượng (MeV) cho $1{,}6\cdot10^{-13}$", r"Đổi MeV sang jun là nhân với hệ số đổi; chia cho ra số rất lớn, sai đơn vị.")]),
  buoc("Năng lượng cả mẫu", "Năng lượng toả ra khi đốt hết mẫu là bao nhiêu (nhập hệ số $a$ của kết quả $a\\cdot10^{n}\\ \\text{J}$)?", 8.48, "×10ⁿ J", 0.05,
       loi=r"Quên nhân với số phản ứng nên chỉ ra năng lượng của một phản ứng, hoặc nhân hai số mũ sai chiều.",
       ke=[(r"Nhân năng lượng một phản ứng với số phản ứng", True),
           (r"Nhân năng lượng một phản ứng với số mol đơteri", r"Năng lượng một phản ứng ứng với một hạt nhân, nên phải nhân với số hạt (số phản ứng), không phải số mol."),
           (r"Nhân năng lượng một phản ứng với khối lượng đơteri (gam)", r"Khối lượng không phải số phản ứng; mỗi phản ứng dùng một hạt, không dùng một gam.")]),
  buoc("Khối lượng than tương đương", "Khối lượng than đá cho cùng năng lượng là bao nhiêu (nhập hệ số $a$ của kết quả $a\\cdot10^{n}\\ \\text{kg}$)?", 3.14, "×10ⁿ kg", 0.03,
       loi=r"Nhân thay vì chia cho năng suất toả nhiệt, hoặc đọc kilôgam thành tấn.",
       ke=[(r"Chia năng lượng (J) cho năng suất toả nhiệt của than (J/kg)", True),
           (r"Nhân năng lượng với năng suất toả nhiệt", r"Kết quả có đơn vị $\text{J}^2/\text{kg}$, không phải kilôgam."),
           (r"Chia năng suất toả nhiệt cho năng lượng", r"Cho đơn vị $\text{kg}^{-1}$, không phải khối lượng than.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>công suất và thời gian chạy</b> của lò → nghĩ tới <b>năng lượng lò toả ra</b>, rồi <b>số phân hạch</b>.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Năng lượng lò toả ra", "Lò toả ra bao nhiêu năng lượng trong $30$ ngày (nhập hệ số $a$ của kết quả $a\\cdot10^{n}\\ \\text{J}$)?", 2.33, "×10ⁿ J", 0.01,
       loi=r"Thế $t=30$ (ngày) thẳng vào công thức, hoặc đổi nhầm số giây trong một ngày nên lệch nhiều bậc mười."),
  buoc("Năng lượng một phân hạch", "Năng lượng một phân hạch theo jun là bao nhiêu (nhập hệ số $a$ của kết quả $a\\cdot10^{n}\\ \\text{J}$)?", 3.2, "×10ⁿ J", 0.05,
       loi=r"Dùng $1\ \text{eV}=1{,}6\cdot10^{-19}\ \text{J}$ cho MeV, hoặc quên đổi MeV sang jun.",
       ke=[(r"Nhân năng lượng (MeV) với $1{,}6\cdot10^{-13}\ \text{J/MeV}$", True),
           (r"Nhân năng lượng (MeV) với $1{,}6\cdot10^{-19}$", r"$1{,}6\cdot10^{-19}\ \text{J}$ là $1\ \text{eV}$; một MeV gấp $10^6$ lần một eV."),
           (r"Chia năng lượng (MeV) cho $1{,}6\cdot10^{-13}$", r"Đổi MeV sang jun là nhân với hệ số đổi; chia cho ra số rất lớn.")]),
  buoc("Số phân hạch", "Số hạt nhân U-235 đã phân hạch là bao nhiêu (nhập hệ số $a$ của kết quả $a\\cdot10^{n}$)?", 7.29, "×10ⁿ", 0.05,
       loi=r"Nhân thay vì chia, hoặc chia luỹ thừa mười sai nên lệch bậc.",
       ke=[(r"Chia năng lượng của lò cho năng lượng một phân hạch", True),
           (r"Nhân năng lượng của lò với năng lượng một phân hạch", r"Kết quả có đơn vị $\text{J}^2$, không phải số hạt."),
           (r"Chia năng lượng một phân hạch cho năng lượng của lò", r"Cho số nhỏ hơn $1$, vô lí vì ít nhất phải có một phân hạch.")]),
  buoc("Khối lượng U-235", "Khối lượng U-235 đã phân hạch là bao nhiêu kilôgam?", 28.5, "kg", 0.3,
       loi=r"Quên nhân khối lượng mol $235\ \text{g/mol}$ nên chỉ ra số mol, hoặc quên đổi gam sang kilôgam.",
       ke=[(r"Chia số hạt nhân cho $N_A$ để ra số mol, rồi nhân với khối lượng mol", True),
           (r"Nhân số hạt nhân với $N_A$ rồi chia cho khối lượng mol", r"Nhân với $N_A$ làm số hạt lớn thêm cỡ $10^{23}$ lần, kết quả vô nghĩa."),
           (r"Chia số hạt nhân cho khối lượng mol rồi nhân với $N_A$", r"Chia cho $235$ không đổi số hạt ra số mol; số mol có được khi chia cho $N_A$.")]),
  buoc("Khối lượng than tương đương", "Khối lượng than đá cho cùng năng lượng là bao nhiêu (nhập hệ số $a$ của kết quả $a\\cdot10^{n}$ tấn)?", 8.64, "×10ⁿ tấn", 0.05,
       loi=r"Nhân thay vì chia cho năng suất toả nhiệt, hoặc đọc kilôgam thành tấn.",
       ke=[(r"Chia năng lượng (J) cho năng suất toả nhiệt (J/kg) rồi đổi kilôgam sang tấn", True),
           (r"Nhân năng lượng với năng suất toả nhiệt", r"Kết quả có đơn vị $\text{J}^2/\text{kg}$, không phải khối lượng."),
           (r"Chia năng suất toả nhiệt cho năng lượng của lò", r"Cho đơn vị $\text{kg}^{-1}$, không phải khối lượng than.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
write(J, 17, "Bài 16. Phản ứng phân hạch, phản ứng nhiệt hạch và ứng dụng", DANG, BUILD, ANALYSIS, SOLS, None)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
for q, f in zip(d["dang_bai"], FORMS): q["form"] = f
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code)"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
