"""Bài tập mẫu Bài 15 "Năng lượng liên kết hạt nhân" (Vật lí 12) — lesson_id 16. 6 dạng (quét dạng:
scripts/logs/batch-ra-soat/ket-qua/16.quet-dang.json). Hình: hinh_16.py. Bài chưa có mục bai_tap_mau trong DB nên không có ví dụ cũ / tự luận.
Hằng số đúng như lý thuyết bài: m_p = 1,007276 u; m_n = 1,008665 u; m_e = 0,000549 u; 1 u = 931,5 MeV/c².
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-16.py   (idempotent, ghi 16.json với review.checked=false)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_16 import *

J = os.path.join(HERE, "16.json")
T223 = "Tính độ hụt khối và năng lượng liên kết"
T224 = "Năng lượng liên kết riêng và độ bền hạt nhân"

# ═════════════ KIỂM SỐ (độc lập với lời giải: nếu lệch thì dừng) ═════════════
mp, mn, me, U = 1.007276, 1.008665, 0.000549, 931.5
def dmass(Z, A, mX): return Z * mp + (A - Z) * mn - mX
_d1 = dmass(7, 14, 13.999231);   assert abs(_d1 - 0.112356) < 1e-9 and abs(_d1 * U - 104.66) < 0.01
_d2 = dmass(10, 20, 19.986950);  assert abs(_d2 - 0.17246) < 1e-9 and abs(_d2 * U / 20 - 8.0323) < 0.001
_d4 = dmass(20, 40, 39.962591 - 20 * me); assert abs(_d4 - 0.367209) < 1e-9 and abs(_d4 * U / 40 - 8.5514) < 0.001
_dm5 = 8.72 * 84 / U; _m5 = 36 * mp + 48 * mn - _dm5; assert abs(_dm5 - 0.786345) < 1e-5 and abs(_m5 - 83.891512) < 1e-4
_E6 = 0.098940 * U; _N6 = 3.0 / 12 * 6.02e23; _J6 = _N6 * _E6 * 1.6e-13
assert abs(_E6 - 92.16) < 0.01 and abs(_J6 / 1e12 - 2.2193) < 0.001 and abs(_J6 / 2.9e7 - 76527) < 5
for A_, E_, want in ((9, 58.16, 6.462), (20, 160.64, 8.032), (90, 782.63, 8.696), (208, 1636.43, 7.867)):
    assert abs(E_ / A_ - want) < 0.001
_order = sorted([(58.16 / 9, "Be"), (160.64 / 20, "Ne"), (782.63 / 90, "Sr"), (1636.43 / 208, "Pb")])
assert [n for _, n in _order] == ["Be", "Pb", "Ne", "Sr"]

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
HANGSO = r"Cho $m_p = 1{,}007276\ \text{u}$, $m_n = 1{,}008665\ \text{u}$, $1\ \text{u} = 931{,}5\ \text{MeV}/c^2$."
DANG = [
 dict(label="Dạng 1 · Dễ · Độ hụt khối và năng lượng liên kết từ khối lượng hạt nhân",
      topic=T223,
      problem_html=r"<p>Hạt nhân nitơ $^{14}_{7}\text{N}$ là thành phần chính của khí quyển. Hạt nhân này có khối lượng hạt nhân $m_X = 13{,}999231\ \text{u}$.</p><p>" + HANGSO + r"</p><ol type=\"a\"><li>Tính độ hụt khối của hạt nhân.</li><li>Tính năng lượng liên kết của hạt nhân.</li></ol>".replace('\\"', '"')),
 dict(label="Dạng 2 · Trung bình · Năng lượng liên kết riêng và so sánh với hạt nhân đã biết",
      topic=T224,
      problem_html=r"<p>Hạt nhân neon $^{20}_{10}\text{Ne}$ có khối lượng hạt nhân $m_X = 19{,}986950\ \text{u}$.</p><p>" + HANGSO + r"</p><ol type=\"a\"><li>Tính năng lượng liên kết riêng của hạt nhân neon.</li><li>So với heli-4 ($7{,}07\ \text{MeV}$/nuclôn) và sắt-56 ($8{,}79\ \text{MeV}$/nuclôn), hạt nhân neon bền vững hơn hay kém bền hơn mỗi hạt nhân đó?</li></ol>".replace('\\"', '"')),
 dict(label="Dạng 3 · Trung bình · Sắp xếp các hạt nhân theo độ bền vững",
      topic=T224,
      problem_html=r"""<p>Bảng cho số khối và năng lượng liên kết của bốn hạt nhân.</p><div class="table-scroll"><table class="tl-table"><thead><tr><th>Hạt nhân</th><th>Số khối $A$</th><th>Năng lượng liên kết $E_{lk}$ (MeV)</th></tr></thead><tbody><tr><td>$^{9}_{4}\text{Be}$</td><td>9</td><td>58,16</td></tr><tr><td>$^{20}_{10}\text{Ne}$</td><td>20</td><td>160,64</td></tr><tr><td>$^{90}_{38}\text{Sr}$</td><td>90</td><td>782,63</td></tr><tr><td>$^{208}_{82}\text{Pb}$</td><td>208</td><td>1636,43</td></tr></tbody></table></div><ol type="a"><li>Tính năng lượng liên kết riêng của từng hạt nhân.</li><li>Sắp xếp bốn hạt nhân theo thứ tự tăng dần độ bền vững.</li></ol>"""),
 dict(label="Dạng 4 · Khá · Đề cho khối lượng nguyên tử",
      topic=T223,
      problem_html=r"<p>Nguyên tử canxi $^{40}_{20}\text{Ca}$ có khối lượng nguyên tử $m_{nt} = 39{,}962591\ \text{u}$.</p><p>Cho $m_p = 1{,}007276\ \text{u}$, $m_n = 1{,}008665\ \text{u}$, $m_e = 0{,}000549\ \text{u}$, $1\ \text{u} = 931{,}5\ \text{MeV}/c^2$.</p><ol type=\"a\"><li>Tính độ hụt khối của hạt nhân canxi.</li><li>Tính năng lượng liên kết và năng lượng liên kết riêng của hạt nhân canxi.</li></ol>".replace('\\"', '"')),
 dict(label="Dạng 5 · Khá · Bài ngược: từ năng lượng liên kết riêng tìm khối lượng hạt nhân",
      topic=T223,
      problem_html=r"<p>Hạt nhân kripton $^{84}_{36}\text{Kr}$ có năng lượng liên kết riêng $8{,}72\ \text{MeV}$/nuclôn.</p><p>" + HANGSO + r"</p><ol type=\"a\"><li>Tính độ hụt khối của hạt nhân kripton.</li><li>Tính khối lượng của hạt nhân kripton.</li></ol>".replace('\\"', '"')),
 dict(label="Dạng 6 · Khó · Năng lượng của cả lượng hạt nhân, so với than đá",
      topic=T223,
      problem_html=r"<p>Hạt nhân cacbon $^{12}_{6}\text{C}$ có độ hụt khối $\Delta m = 0{,}098940\ \text{u}$. Lấy $1\ \text{u} = 931{,}5\ \text{MeV}/c^2$, $1\ \text{MeV} = 1{,}6\cdot10^{-13}\ \text{J}$, $N_A = 6{,}02\cdot10^{23}\ \text{mol}^{-1}$; khối lượng mol của cacbon-12 là $12\ \text{g/mol}$.</p><ol type=\"a\"><li>Tính năng lượng toả ra khi tạo thành $3{,}0\ \text{g}$ cacbon-12 từ các nuclôn rời, theo đơn vị jun.</li><li>Năng lượng đó bằng năng lượng toả ra khi đốt bao nhiêu kilôgam than đá? Năng suất toả nhiệt của than là $2{,}9\cdot10^{7}\ \text{J/kg}$.</li></ol>".replace('\\"', '"')),
]

BUILD = [d1, d2, d3, d4, d5, d6]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (hàng "cần tìm" chỉ ghi "Cần X"; ô ⚠ chỉ nêu câu hỏi điều kiện) ═════════════
ANALYSIS = [
 [("\"hạt nhân nitơ $^{14}_{7}\\text{N}$\"", "$Z=7$; $A=14$", "Kí hiệu hạt nhân: số prôtôn, số nơtron, số khối"),
  ("\"khối lượng hạt nhân $m_X = 13{,}999231\\ \\text{u}$\"", "$m_X=13{,}999231\\ \\text{u}$", "⚠ Đề cho khối lượng của hạt nhân hay của cả nguyên tử? Việc này quyết định tổng hạt rời có kèm êlectron hay không"),
  ("\"$m_p = 1{,}007276\\ \\text{u}$, $m_n = 1{,}008665\\ \\text{u}$\"", "$m_p$, $m_n$", "Khối lượng của prôtôn và nơtron khi đứng rời"),
  ("\"$1\\ \\text{u} = 931{,}5\\ \\text{MeV}/c^2$\"", "$1\\ \\text{u}\\cdot c^2=931{,}5\\ \\text{MeV}$", "Hệ thức khối lượng – năng lượng của Einstein; hệ số đã chứa sẵn $c^2$"),
  ("\"a) Tính độ hụt khối\"", "Cần $\\Delta m$", "Khái niệm độ hụt khối"),
  ("\"b) Tính năng lượng liên kết\"", "Cần $E_{lk}$", "Khái niệm năng lượng liên kết")],
 [("\"hạt nhân neon $^{20}_{10}\\text{Ne}$\"", "$Z=10$; $A=20$", "Số prôtôn, số nơtron, số khối"),
  ("\"khối lượng hạt nhân $m_X = 19{,}986950\\ \\text{u}$\"", "$m_X=19{,}986950\\ \\text{u}$", "⚠ Khối lượng của hạt nhân hay của nguyên tử? Quyết định cách lập tổng hạt rời"),
  ("\"$m_p$, $m_n$, $1\\ \\text{u} = 931{,}5\\ \\text{MeV}/c^2$\"", "$m_p$, $m_n$; hệ số đổi", "Khối lượng nuclôn rời; hệ thức khối lượng – năng lượng"),
  ("\"a) năng lượng liên kết riêng của hạt nhân neon\"", "Cần $E_{lkr}$", "Khái niệm năng lượng liên kết riêng"),
  ("\"So với heli-4 ($7{,}07$) và sắt-56 ($8{,}79$) MeV/nuclôn\"", "Hai mốc: $7{,}07$ và $8{,}79\\ \\text{MeV}$/nuclôn", "⚠ Chỉ so hai đại lượng cùng loại và cùng đơn vị với nhau"),
  ("\"b) bền vững hơn hay kém bền hơn\"", "Cần kết luận về độ bền", "Quan hệ giữa độ bền và đại lượng ở câu a")],
 [("\"bảng cho số khối và năng lượng liên kết của bốn hạt nhân\"", "$A=9;\\ 20;\\ 90;\\ 208$ ; $E_{lk}=58{,}16;\\ 160{,}64;\\ 782{,}63;\\ 1636{,}43\\ \\text{MeV}$", "Số khối, năng lượng liên kết của từng hạt nhân"),
  ("\"bốn hạt nhân\" có số khối rất khác nhau", "$A$ từ $9$ đến $208$", "⚠ Có so thẳng được các số trong cột $E_{lk}$ không? Xét xem các hạt nhân có cùng cơ sở so sánh hay không"),
  ("\"a) Tính năng lượng liên kết riêng của từng hạt nhân\"", "Cần $E_{lkr}$ của 4 hạt nhân", "Khái niệm năng lượng liên kết riêng"),
  ("\"b) Sắp xếp theo thứ tự tăng dần độ bền vững\"", "Cần thứ tự tăng dần", "Quan hệ giữa độ bền và đại lượng ở câu a")],
 [("\"nguyên tử canxi $^{40}_{20}\\text{Ca}$\"", "$Z=20$; $A=40$", "Số prôtôn, số nơtron, số khối; nguyên tử trung hoà có $Z$ êlectron"),
  ("\"khối lượng nguyên tử $m_{nt} = 39{,}962591\\ \\text{u}$\"", "$m_{nt}=39{,}962591\\ \\text{u}$", "⚠ Khối lượng này gồm những hạt nào? Quyết định cách lập tổng khối lượng hạt rời để so cùng loại"),
  ("\"$m_p$, $m_n$, $m_e = 0{,}000549\\ \\text{u}$\"", "$m_p$, $m_n$, $m_e$", "Khối lượng prôtôn, nơtron, êlectron"),
  ("\"$1\\ \\text{u} = 931{,}5\\ \\text{MeV}/c^2$\"", "Hệ số đổi", "Hệ thức khối lượng – năng lượng; hệ số đã chứa sẵn $c^2$"),
  ("\"a) độ hụt khối của hạt nhân canxi\"", "Cần $\\Delta m$", "Khái niệm độ hụt khối"),
  ("\"b) năng lượng liên kết và năng lượng liên kết riêng\"", "Cần $E_{lk}$ và $E_{lkr}$", "Khái niệm năng lượng liên kết, năng lượng liên kết riêng")],
 [("\"hạt nhân kripton $^{84}_{36}\\text{Kr}$\"", "$Z=36$; $A=84$; $A-Z=48$", "Số prôtôn, số nơtron, số khối"),
  ("\"năng lượng liên kết riêng $8{,}72\\ \\text{MeV}$/nuclôn\"", "$E_{lkr}=8{,}72\\ \\text{MeV}$/nuclôn", "Khái niệm năng lượng liên kết riêng: tính cho một nuclôn"),
  ("\"$m_p$, $m_n$, $1\\ \\text{u} = 931{,}5\\ \\text{MeV}/c^2$\"", "$m_p$, $m_n$; hệ số đổi", "⚠ Đại lượng cần tìm là khối lượng của hạt nhân hay nguyên tử? Quyết định tổng hạt rời cần loại nào"),
  ("\"a) độ hụt khối của hạt nhân kripton\"", "Cần $\\Delta m$", "Quan hệ giữa độ hụt khối và năng lượng liên kết"),
  ("\"b) khối lượng của hạt nhân kripton\"", "Cần $m_X$", "Khái niệm độ hụt khối")],
 [("\"độ hụt khối $\\Delta m = 0{,}098940\\ \\text{u}$\" của hạt nhân $^{12}_{6}\\text{C}$", "$\\Delta m=0{,}098940\\ \\text{u}$", "⚠ Số này ứng với MỘT hạt nhân hay cả mẫu? Quyết định có phải đếm số hạt nhân hay không"),
  ("\"$1\\ \\text{u} = 931{,}5\\ \\text{MeV}/c^2$, $1\\ \\text{MeV} = 1{,}6\\cdot10^{-13}\\ \\text{J}$\"", "Hai hệ số đổi", "Hệ thức khối lượng – năng lượng; đổi MeV sang jun"),
  ("\"$N_A = 6{,}02\\cdot10^{23}\\ \\text{mol}^{-1}$; $12\\ \\text{g/mol}$\"", "$N_A$; $M=12\\ \\text{g/mol}$", "Số mol, hằng số Avôgađrô, số hạt trong một lượng chất"),
  ("\"tạo thành $3{,}0\\ \\text{g}$ cacbon-12\"", "$m=3{,}0\\ \\text{g}$", "Lượng chất cho bằng khối lượng"),
  ("\"a) năng lượng toả ra, theo đơn vị jun\"", "Cần $E$ (J)", "Năng lượng toả ra khi các nuclôn kết hợp thành hạt nhân"),
  ("\"b) bao nhiêu kilôgam than đá\"", "Cần $m_{than}$; $q=2{,}9\\cdot10^{7}\\ \\text{J/kg}$", "Năng suất toả nhiệt của nhiên liệu")],
]

# ═════════════ LỜI GIẢI ═════════════
RC1 = [r"<strong>Khái niệm:</strong> độ hụt khối là phần khối lượng mất đi khi các nuclôn rời kết hợp thành hạt nhân; năng lượng liên kết ứng với phần khối lượng đó.",
       r"<strong>Định luật:</strong> hệ thức Einstein $E=mc^2$; $1\ \text{u}\cdot c^2=931{,}5\ \text{MeV}$.",
       r"<strong>Công thức:</strong> $\Delta m=Zm_p+(A-Z)m_n-m_X$ · $E_{lk}=\Delta m\cdot931{,}5$.",
       r"⚠ <strong>Điều kiện:</strong> $m_X$ là khối lượng hạt nhân (không kèm êlectron); giữ đủ chữ số, không làm tròn khối lượng."]
RC2 = [r"<strong>Khái niệm:</strong> năng lượng liên kết riêng là năng lượng liên kết tính cho một nuclôn; càng lớn thì hạt nhân càng bền.",
       r"<strong>Định luật:</strong> $E_{lk}=\Delta m\,c^2$ với $1\ \text{u}\cdot c^2=931{,}5\ \text{MeV}$.",
       r"<strong>Công thức:</strong> $E_{lkr}=\dfrac{E_{lk}}{A}$.",
       r"⚠ <strong>Điều kiện:</strong> chỉ so $E_{lkr}$ với $E_{lkr}$ (cùng MeV/nuclôn); $A$ là số khối, không phải $Z$."]
RC3 = [r"<strong>Khái niệm:</strong> năng lượng liên kết là của cả hạt nhân nên tăng theo số nuclôn; năng lượng liên kết riêng là của mỗi nuclôn.",
       r"<strong>Định luật:</strong> $E_{lkr}$ càng lớn, hạt nhân càng bền vững.",
       r"<strong>Công thức:</strong> $E_{lkr}=\dfrac{E_{lk}}{A}$.",
       r"⚠ <strong>Điều kiện:</strong> hạt nhân khác số khối thì không so thẳng $E_{lk}$, phải so $E_{lkr}$."]
RC4 = [r"<strong>Khái niệm:</strong> độ hụt khối tính theo khối lượng hạt nhân; bảng đo được cho khối lượng cả nguyên tử.",
       r"<strong>Định luật:</strong> $E_{lk}=\Delta m\,c^2$ với $1\ \text{u}\cdot c^2=931{,}5\ \text{MeV}$.",
       r"<strong>Công thức:</strong> $\Delta m=Zm_p+(A-Z)m_n+Zm_e-m_{nt}$ · $E_{lkr}=\dfrac{E_{lk}}{A}$.",
       r"⚠ <strong>Điều kiện:</strong> khối lượng nguyên tử đã gồm $Z$ êlectron nên tổng hạt rời phải cộng thêm $Zm_e$."]
RC5 = [r"<strong>Khái niệm:</strong> $E_{lkr}$ là năng lượng liên kết cho một nuclôn; độ hụt khối là khối lượng ứng với $E_{lk}$.",
       r"<strong>Định luật:</strong> $E_{lk}=\Delta m\,c^2$; khối lượng hạt nhân nhỏ hơn tổng nuclôn rời đúng một độ hụt khối.",
       r"<strong>Công thức:</strong> $E_{lk}=E_{lkr}\cdot A$ · $\Delta m=\dfrac{E_{lk}}{931{,}5}$ · $m_X=Zm_p+(A-Z)m_n-\Delta m$.",
       r"⚠ <strong>Điều kiện:</strong> $m_X$ cần tìm là khối lượng hạt nhân nên tổng hạt rời không kèm êlectron."]
RC6 = [r"<strong>Khái niệm:</strong> năng lượng liên kết một hạt nhân toả ra khi nuclôn rời kết hợp lại; mẫu có rất nhiều hạt nhân.",
       r"<strong>Định luật:</strong> $E=\Delta m\,c^2$ cho MỘT hạt nhân; các hạt nhân toả năng lượng độc lập, cộng lại được.",
       r"<strong>Công thức:</strong> $N=\dfrac{m}{M}N_A$ · $E=N\cdot E_1$ · $m_{than}=\dfrac{E}{q}$.",
       r"⚠ <strong>Điều kiện:</strong> $\Delta m$ đề cho là của một hạt nhân; $1\ \text{MeV}=1{,}6\cdot10^{-13}\ \text{J}$ mới ra jun."]

SOLS = [
 sol(RC1, [
  ("Tổng khối lượng nuclôn rời", [P(r"Hạt nhân có $Z=7$ prôtôn và $A-Z=7$ nơtron:"), M(r"Zm_p=7\cdot1{,}007276=7{,}050932\ \text{u}"),
        M(r"(A-Z)m_n=7\cdot1{,}008665=7{,}060655\ \text{u}"), A(r"Zm_p+(A-Z)m_n=14{,}111587\ \text{u}")]),
  ("Độ hụt khối (câu a)", [M(r"\Delta m=Zm_p+(A-Z)m_n-m_X"), M(r"\Delta m=14{,}111587-13{,}999231"), A(r"\Delta m=0{,}112356\ \text{u}"),
        P(r"$\Delta m$ chỉ chiếm khoảng $0{,}8\ \%$ khối lượng nên làm tròn khối lượng về $14{,}00\ \text{u}$ là mất sạch kết quả.")]),
  ("Năng lượng liên kết (câu b)", [P(r"Hệ số $931{,}5\ \text{MeV/u}$ đã chứa sẵn $c^2$ nên không nhân thêm:"), M(r"E_{lk}=\Delta m\cdot931{,}5"),
        M(r"E_{lk}=0{,}112356\cdot931{,}5"), A(r"E_{lk}\approx104{,}7\ \text{MeV}")]),
  ("Kiểm tra", [M(r"E_{lkr}=\dfrac{104{,}66}{14}\approx7{,}48\ \text{MeV/nuclôn}"),
        P(r"Nằm giữa $7{,}07$ của heli-4 và $7{,}98$ của oxi-16: hợp lí cho hạt nhân nhẹ cỡ $A=14$.")])],
  [r"a) $\Delta m\approx0{,}1124\ \text{u}$", r"b) $E_{lk}\approx104{,}7\ \text{MeV}$"],
  r"Nhận dạng: đề cho sẵn <strong>khối lượng hạt nhân</strong> và hỏi độ hụt khối, năng lượng liên kết → $\Delta m=Zm_p+(A-Z)m_n-m_X$, rồi nhân $931{,}5$."),
 sol(RC2, [
  ("Độ hụt khối", [P(r"Neon có $Z=10$ prôtôn và $A-Z=10$ nơtron:"), M(r"Zm_p+(A-Z)m_n=10\cdot1{,}007276+10\cdot1{,}008665=20{,}159410\ \text{u}"),
        M(r"\Delta m=20{,}159410-19{,}986950"), A(r"\Delta m=0{,}172460\ \text{u}")]),
  ("Năng lượng liên kết", [M(r"E_{lk}=\Delta m\cdot931{,}5=0{,}172460\cdot931{,}5"), A(r"E_{lk}\approx160{,}6\ \text{MeV}")]),
  ("Năng lượng liên kết riêng (câu a)", [P(r"Chia cho số khối $A=20$ (cả prôtôn lẫn nơtron):"), M(r"E_{lkr}=\dfrac{E_{lk}}{A}=\dfrac{160{,}65}{20}"), A(r"E_{lkr}\approx8{,}03\ \text{MeV/nuclôn}")]),
  ("So sánh độ bền (câu b)", [P(r"$E_{lkr}$ lớn hơn thì hạt nhân bền hơn. So với hai mốc:"), M(r"7{,}07\lt8{,}03\lt8{,}79"),
        A(r"T:Neon <strong>bền hơn</strong> heli-4 và <strong>kém bền hơn</strong> sắt-56.")]),
  ("Kiểm tra", [P(r"Sắt-56 gần đỉnh của đường cong ($\approx8{,}8$) nên mọi hạt nhân khác đều kém bền hơn nó: kết quả hợp lí."),
        P(r"Hạt nhân nhẹ cỡ $A=20$ thường có $E_{lkr}$ vào khoảng $7$–$8{,}5\ \text{MeV/nuclôn}$.")])],
  [r"a) $E_{lkr}\approx8{,}03\ \text{MeV/nuclôn}$", r"b) Bền hơn heli-4, kém bền hơn sắt-56"],
  r"Nhận dạng: đề hỏi <strong>năng lượng liên kết riêng hoặc độ bền</strong> → $E_{lkr}=\dfrac{E_{lk}}{A}$ rồi đặt cạnh hạt nhân đã biết."),
 sol(RC3, [
  ("Chọn đại lượng để so độ bền", [P(r"Bốn hạt nhân có số khối từ $9$ đến $208$; $E_{lk}$ tăng theo số nuclôn nên cột $E_{lk}$ không so thẳng được."),
        A(r"T:So bằng <strong>năng lượng liên kết riêng</strong> (năng lượng tính cho một nuclôn).")]),
  ("Năng lượng liên kết riêng của từng hạt nhân (câu a)", [M(r"E_{lkr}=\dfrac{E_{lk}}{A}"),
        M(r"\text{Be}:\ \dfrac{58{,}16}{9}\approx6{,}46\qquad \text{Ne}:\ \dfrac{160{,}64}{20}\approx8{,}03"),
        M(r"\text{Sr}:\ \dfrac{782{,}63}{90}\approx8{,}70\qquad \text{Pb}:\ \dfrac{1636{,}43}{208}\approx7{,}87"),
        A(r"E_{lkr}\ (\text{MeV/nuclôn}):\ 6{,}46;\ 8{,}03;\ 8{,}70;\ 7{,}87")]),
  ("Sắp xếp theo độ bền (câu b)", [P(r"$E_{lkr}$ càng lớn càng bền; xếp từ nhỏ đến lớn:"), M(r"6{,}46\lt7{,}87\lt8{,}03\lt8{,}70"),
        A(r"T:Tăng dần độ bền: $^{9}_{4}\text{Be}$, $^{208}_{82}\text{Pb}$, $^{20}_{10}\text{Ne}$, $^{90}_{38}\text{Sr}$.")]),
  ("Kiểm tra", [P(r"Stronti ($A=90$) nằm gần vùng đỉnh $A\approx50$–$80$ nên bền nhất là hợp lí; chì nặng đã đi xuống sau đỉnh nên $E_{lkr}$ thấp hơn."),
        P(r"Nếu xếp theo $E_{lk}$ thô thì chì đứng đầu: sai vì chì có $208$ nuclôn.")])],
  [r"a) $E_{lkr}$: $6{,}46$ ; $8{,}03$ ; $8{,}70$ ; $7{,}87\ \text{MeV/nuclôn}$", r"b) Be $\lt$ Pb $\lt$ Ne $\lt$ Sr"],
  r"Nhận dạng: đề cho <strong>nhiều hạt nhân khác số khối</strong> và hỏi độ bền → tính $E_{lkr}=\dfrac{E_{lk}}{A}$ cho từng hạt nhân rồi xếp."),
 sol(RC4, [
  ("Nhận ra loại khối lượng", [P(r"Đề ghi rõ <strong>khối lượng nguyên tử</strong>: gồm hạt nhân và $Z=20$ êlectron ở vỏ."),
        A(r"T:Tổng hạt rời cần có đủ prôtôn, nơtron <strong>và</strong> êlectron để cùng loại với nguyên tử.")]),
  ("Tổng khối lượng hạt rời", [M(r"Zm_p=20\cdot1{,}007276=20{,}145520\ \text{u}"), M(r"(A-Z)m_n=20\cdot1{,}008665=20{,}173300\ \text{u}"),
        M(r"Zm_e=20\cdot0{,}000549=0{,}010980\ \text{u}"), A(r"Zm_p+(A-Z)m_n+Zm_e=40{,}329800\ \text{u}")]),
  ("Độ hụt khối (câu a)", [M(r"\Delta m=40{,}329800-39{,}962591"), A(r"\Delta m=0{,}367209\ \text{u}")]),
  ("Năng lượng liên kết (câu b)", [M(r"E_{lk}=\Delta m\cdot931{,}5=0{,}367209\cdot931{,}5"), A(r"E_{lk}\approx342{,}1\ \text{MeV}")]),
  ("Năng lượng liên kết riêng (câu b)", [M(r"E_{lkr}=\dfrac{E_{lk}}{A}=\dfrac{342{,}06}{40}"), A(r"E_{lkr}\approx8{,}55\ \text{MeV/nuclôn}")]),
  ("Kiểm tra", [P(r"Nếu quên $Zm_e$ thì $\Delta m'=0{,}356229\ \text{u}$, $E_{lk}'\approx331{,}8\ \text{MeV}$: lệch khoảng $10\ \text{MeV}$, gần $3\ \%$."),
        P(r"$E_{lkr}\approx8{,}55$ gần đỉnh $\approx8{,}8$ quanh sắt-56, hợp lí vì $A=40$ ở gần vùng đỉnh của đường cong.")])],
  [r"a) $\Delta m\approx0{,}3672\ \text{u}$", r"b) $E_{lk}\approx342{,}1\ \text{MeV}$ ; $E_{lkr}\approx8{,}55\ \text{MeV/nuclôn}$"],
  r"Nhận dạng: đề ghi <strong>khối lượng nguyên tử</strong> → cộng $Zm_e$ vào tổng hạt rời trước khi trừ."),
 sol(RC5, [
  ("Năng lượng liên kết của cả hạt nhân", [P(r"$E_{lkr}$ là của một nuclôn, hạt nhân có $A=84$ nuclôn:"), M(r"E_{lk}=E_{lkr}\cdot A=8{,}72\cdot84"), A(r"E_{lk}=732{,}48\ \text{MeV}")]),
  ("Độ hụt khối (câu a)", [P(r"Đổi MeV sang u: $1\ \text{u}$ ứng với $931{,}5\ \text{MeV}$."), M(r"\Delta m=\dfrac{E_{lk}}{931{,}5}=\dfrac{732{,}48}{931{,}5}"), A(r"\Delta m\approx0{,}7863\ \text{u}")]),
  ("Tổng khối lượng nuclôn rời", [P(r"Kripton có $Z=36$ prôtôn và $A-Z=48$ nơtron:"), M(r"36\cdot1{,}007276+48\cdot1{,}008665=36{,}261936+48{,}415920"),
        A(r"Zm_p+(A-Z)m_n=84{,}677856\ \text{u}")]),
  ("Khối lượng hạt nhân (câu b)", [P(r"Hạt nhân nhẹ hơn các nuclôn rời đúng một độ hụt khối:"), M(r"m_X=84{,}677856-0{,}786345"), A(r"m_X\approx83{,}8915\ \text{u}")]),
  ("Kiểm tra", [P(r"$m_X\lt$ tổng nuclôn rời và rất gần số khối $84$ (lệch khoảng $0{,}11\ \text{u}$): hợp lí."),
        P(r"Chiều ngược lại: $\Delta m\cdot931{,}5=0{,}7863\cdot931{,}5\approx732{,}4\ \text{MeV}$, chia cho $84$ lại ra $8{,}72$.")])],
  [r"a) $\Delta m\approx0{,}7863\ \text{u}$", r"b) $m_X\approx83{,}8915\ \text{u}$"],
  r"Nhận dạng: đề cho <strong>$E_{lkr}$</strong> và hỏi khối lượng hạt nhân → đi ngược: nhân $A$, chia $931{,}5$, rồi lấy tổng nuclôn rời trừ $\Delta m$."),
 sol(RC6, [
  ("Số hạt nhân trong mẫu", [P(r"Số mol, rồi đổi sang số hạt nhân bằng $N_A$:"), M(r"n=\dfrac{m}{M}=\dfrac{3{,}0}{12}=0{,}25\ \text{mol}"),
        M(r"N=n\cdot N_A=0{,}25\cdot6{,}02\cdot10^{23}"), A(r"N=1{,}505\cdot10^{23}\ \text{hạt nhân}")]),
  ("Năng lượng của một hạt nhân", [M(r"E_1=\Delta m\cdot931{,}5=0{,}098940\cdot931{,}5"), A(r"E_1\approx92{,}16\ \text{MeV}")]),
  ("Năng lượng của cả mẫu, theo jun (câu a)", [M(r"E=N\cdot E_1=1{,}505\cdot10^{23}\cdot92{,}16\approx1{,}387\cdot10^{25}\ \text{MeV}"),
        M(r"E=1{,}387\cdot10^{25}\cdot1{,}6\cdot10^{-13}"), A(r"E\approx2{,}22\cdot10^{12}\ \text{J}")]),
  ("Khối lượng than tương đương (câu b)", [M(r"m_{than}=\dfrac{E}{q}=\dfrac{2{,}22\cdot10^{12}}{2{,}9\cdot10^{7}}"), A(r"m_{than}\approx7{,}65\cdot10^{4}\ \text{kg}")]),
  ("Kiểm tra", [P(r"Cỡ $76$ tấn than cho chỉ $3{,}0\ \text{g}$ cacbon: đúng cỡ so với $1\ \text{g}$ heli-4 ở bài lý thuyết (cỡ $23$ tấn than)."),
        P(r"Đơn vị: $\text{J}\ /\ (\text{J/kg})=\text{kg}$, đúng.")])],
  [r"a) $E\approx2{,}22\cdot10^{12}\ \text{J}$", r"b) $m_{than}\approx7{,}65\cdot10^{4}\ \text{kg}$ (khoảng $76$ tấn)"],
  r"Nhận dạng: đề cho <strong>khối lượng chất (gam)</strong> và hỏi năng lượng → $N=\dfrac{m}{M}N_A$, rồi nhân năng lượng một hạt nhân."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC (khớp 1-1 với .bt-step của SOLS) ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>khối lượng hạt nhân</b> cho sẵn → nghĩ tới <b>$\Delta m$ = tổng nuclôn rời − $m_X$</b>, rồi nhân <b>931,5</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Tổng khối lượng nuclôn rời", "Tổng khối lượng của các nuclôn rời trong hạt nhân là bao nhiêu u?", 14.111587, "u", 0.001,
       loi=r"Nhân cả $14$ nuclôn với $m_p$ (quên nơtron nặng hơn prôtôn), hoặc nhân nhầm hệ số $Z$, $A-Z$."),
  buoc("Độ hụt khối", "Độ hụt khối của hạt nhân là bao nhiêu u?", 0.1124, "u", 0.0005,
       loi=r"Lấy $m_X$ trừ tổng nuclôn rời nên ra số âm, hoặc làm tròn khối lượng về hai chữ số thập phân nên hiệu số mất sạch.",
       ke=[(r"Lấy tổng khối lượng nuclôn rời trừ khối lượng hạt nhân", True),
           (r"Lấy khối lượng hạt nhân trừ tổng khối lượng nuclôn rời", r"Hạt nhân luôn nhẹ hơn các nuclôn rời; hiệu này âm, mà độ hụt khối là đại lượng dương."),
           (r"Lấy khối lượng hạt nhân chia cho số khối $A$", r"Chia cho $A$ chỉ cho khối lượng trung bình một nuclôn, không phải phần khối lượng hụt đi.")]),
  buoc("Năng lượng liên kết", "Năng lượng liên kết của hạt nhân là bao nhiêu MeV?", 104.7, "MeV", 0.3,
       loi=r"Nhân thêm $c^2$ sau khi đã nhân $931{,}5$, hoặc chia cho $931{,}5$ thay vì nhân.",
       ke=[(r"Nhân $\Delta m$ (đơn vị u) với $931{,}5\ \text{MeV/u}$", True),
           (r"Nhân $\Delta m$ với $c^2=9\cdot10^{16}$ rồi đọc ra MeV", r"$931{,}5\ \text{MeV/u}$ đã chứa sẵn $c^2$; nhân thêm là sai cả đơn vị."),
           (r"Chia $\Delta m$ cho $931{,}5$", r"Đổi từ u sang MeV là nhân với $931{,}5$ (mỗi u ứng với $931{,}5\ \text{MeV}$); chia cho ra số rất nhỏ.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>năng lượng liên kết riêng</b> hoặc <b>độ bền</b> → nghĩ tới <b>$E_{lk}$ chia cho $A$</b>, rồi so với hạt nhân đã biết.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Độ hụt khối", "Độ hụt khối của hạt nhân neon là bao nhiêu u?", 0.1725, "u", 0.0005,
       loi=r"Dùng $10$ prôtôn và $10$ nơtron nhưng nhân nhầm khối lượng, hoặc bỏ sót chữ số thập phân nên hiệu số lệch."),
  buoc("Năng lượng liên kết", "Năng lượng liên kết của hạt nhân neon là bao nhiêu MeV?", 160.6, "MeV", 0.3,
       loi=r"Quên nhân $931{,}5$ và đọc luôn $\Delta m$ là MeV, hoặc nhân thêm $A$.",
       ke=[(r"Nhân $\Delta m$ với $931{,}5\ \text{MeV/u}$", True),
           (r"Chia $\Delta m$ cho $931{,}5\ \text{MeV/u}$", r"Đổi từ u sang MeV là nhân với $931{,}5$; chia cho ra số rất nhỏ."),
           (r"Nhân $\Delta m$ với số khối $A$", r"Số khối chưa liên quan tới việc đổi khối lượng sang năng lượng; phải dùng $931{,}5\ \text{MeV/u}$.")]),
  buoc("Năng lượng liên kết riêng", "Năng lượng liên kết riêng của neon là bao nhiêu MeV/nuclôn?", 8.03, "MeV/nuclôn", 0.02,
       loi=r"Chia cho số prôtôn $Z$ thay vì số khối $A$, hoặc không chia và đọc $E_{lk}$ là $E_{lkr}$.",
       ke=[(r"Chia $E_{lk}$ cho số khối $A$", True),
           (r"Chia $E_{lk}$ cho số prôtôn $Z$", r"Mỗi nuclôn gồm cả prôtôn lẫn nơtron; phải chia cho cả số khối $A$."),
           (r"Nhân $E_{lk}$ với số khối $A$", r"Năng lượng cho MỘT nuclôn phải nhỏ hơn năng lượng của cả hạt nhân; nhân thêm $A$ làm số lớn lên.")]),
  buoc("So sánh độ bền", "Neon so với heli-4 và sắt-56 thì thế nào?", loi=r"So $E_{lk}$ của neon với $E_{lkr}$ của hai mốc, hoặc đoán theo số nuclôn.",
       lua_chon=[(r"Bền hơn heli-4, kém bền hơn sắt-56", True),
                 (r"Bền hơn cả hai vì $E_{lk}$ của neon lớn hơn", r"So độ bền phải dùng $E_{lkr}$, không dùng $E_{lk}$ của cả hạt nhân; $E_{lk}$ tăng theo số nuclôn."),
                 (r"Kém bền hơn heli-4, bền hơn sắt-56", r"Nếu $E_{lkr}$ vừa tính lớn hơn mốc của heli-4 thì neon phải bền hơn heli-4.")],
       ke=[(r"Đặt $E_{lkr}$ vừa tính cạnh hai mốc rồi so: lớn hơn thì bền hơn", True),
           (r"So $E_{lk}$ của neon với $E_{lkr}$ của hai mốc", r"Hai đại lượng khác loại (cả hạt nhân và mỗi nuclôn) nên so không có nghĩa."),
           (r"Đổi $E_{lkr}$ ra jun rồi so", r"Hai mốc đã cùng đơn vị MeV/nuclôn; đổi đơn vị không giúp so sánh.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>nhiều hạt nhân khác số khối</b> hỏi độ bền → nghĩ tới <b>$E_{lkr}=E_{lk}/A$</b> rồi xếp theo $E_{lkr}$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Chọn đại lượng để so độ bền", "Đại lượng nào dùng để so độ bền của các hạt nhân khác số khối?",
       loi=r"Thấy cột $E_{lk}$ có sẵn nên xếp luôn theo cột đó, bỏ qua việc số khối rất khác nhau.",
       lua_chon=[(r"Năng lượng liên kết riêng", True),
                 (r"Năng lượng liên kết $E_{lk}$", r"$E_{lk}$ tăng theo số nuclôn nên hạt nhân to có số lớn dù chưa chắc bền hơn."),
                 (r"Độ hụt khối $\Delta m$", r"Độ hụt khối cũng là đại lượng của cả hạt nhân, tăng theo số nuclôn giống $E_{lk}$.")]),
  buoc("Năng lượng liên kết riêng của từng hạt nhân", "Năng lượng liên kết riêng của chì $^{208}_{82}\\text{Pb}$ là bao nhiêu MeV/nuclôn?", 7.87, "MeV/nuclôn", 0.02,
       loi=r"Chia cho số prôtôn hoặc số nơtron thay vì số khối, hoặc chia nhầm cho số khối của hạt nhân khác trong bảng.",
       ke=[(r"Chia $E_{lk}$ cho số khối $A$ của từng hạt nhân", True),
           (r"Chia $E_{lk}$ cho số prôtôn $Z$", r"Mỗi nuclôn gồm cả prôtôn lẫn nơtron; phải chia cho cả số khối."),
           (r"Chọn hạt nhân có $E_{lk}$ lớn nhất làm bền nhất, không cần chia", r"Hạt nhân to luôn có $E_{lk}$ lớn nên cách này luôn chọn hạt nhân nặng nhất; độ bền nằm ở mức chia đều cho mỗi nuclôn.")]),
  buoc("Sắp xếp theo độ bền", "Thứ tự tăng dần độ bền vững của bốn hạt nhân là gì?",
       loi=r"Xếp theo cột $E_{lk}$ ban đầu, hoặc xếp giảm dần trong khi đề hỏi tăng dần.",
       lua_chon=[(r"Be-9, Pb-208, Ne-20, Sr-90", True),
                 (r"Be-9, Ne-20, Sr-90, Pb-208", r"Đây là thứ tự theo $E_{lk}$ thô; phải xếp theo $E_{lkr}$ đã chia cho $A$."),
                 (r"Sr-90, Ne-20, Pb-208, Be-9", r"Đây là thứ tự giảm dần độ bền; đề hỏi tăng dần.")],
       ke=[(r"Xếp các giá trị $E_{lkr}$ từ nhỏ đến lớn", True),
           (r"Xếp các hạt nhân theo số khối $A$ tăng dần", r"Số khối không cho biết độ bền; hạt nhân nặng nhất không bền nhất."),
           (r"Xếp theo $E_{lk}$ tăng dần", r"$E_{lk}$ tăng theo số nuclôn nên thứ tự đó chỉ phản ánh kích thước hạt nhân.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>khối lượng nguyên tử</b> trong đề → chú ý <b>êlectron ở vỏ</b> trước khi trừ.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Nhận ra loại khối lượng", "Khối lượng $39{,}962591\\ \\text{u}$ gồm những hạt nào?",
       loi=r"Thấy chữ «khối lượng» là coi luôn là khối lượng hạt nhân, bỏ qua chữ «nguyên tử» trong đề.",
       lua_chon=[(r"Hạt nhân và cả $20$ êlectron ở vỏ", True),
                 (r"Chỉ hạt nhân, vì êlectron quá nhẹ nên bỏ qua", r"Đề ghi nguyên tử nên khối lượng gồm cả êlectron; ở độ chính xác phần triệu của bài, êlectron không bỏ qua được."),
                 (r"Chỉ $20$ prôtôn và $20$ nơtron rời", r"Đó là tổng nuclôn rời; khối lượng đo được của một nguyên tử luôn nhỏ hơn tổng đó.")]),
  buoc("Tổng khối lượng hạt rời", "Tổng khối lượng của các hạt rời cần dùng là bao nhiêu u?", 40.3298, "u", 0.001,
       loi=r"Quên cộng $Zm_e$, hoặc cộng $m_e$ một lần thay vì $Z$ lần.",
       ke=[(r"Cộng thêm $Zm_e$ vào tổng khối lượng prôtôn và nơtron rời", True),
           (r"Dùng thẳng $Zm_p+(A-Z)m_n$ như khi đề cho khối lượng hạt nhân", r"Khối lượng nguyên tử đã gồm $Z$ êlectron; tổng hạt rời cũng phải có đủ êlectron mới so cùng loại."),
           (r"Cộng $Zm_e$ vào khối lượng nguyên tử rồi trừ", r"Nguyên tử đã có sẵn $Z$ êlectron; cộng thêm là đếm êlectron hai lần.")]),
  buoc("Độ hụt khối", "Độ hụt khối của hạt nhân canxi là bao nhiêu u?", 0.3672, "u", 0.0005,
       loi=r"Lấy khối lượng nguyên tử trừ tổng hạt rời nên ra số âm, hoặc trừ thêm một lần nữa khối lượng êlectron.",
       ke=[(r"Lấy tổng hạt rời vừa tính trừ khối lượng nguyên tử", True),
           (r"Lấy khối lượng nguyên tử trừ tổng hạt rời", r"Nguyên tử nhẹ hơn các hạt rời; hiệu này âm, mà độ hụt khối là đại lượng dương."),
           (r"Lấy tổng hạt rời trừ khối lượng nguyên tử, rồi trừ tiếp $Zm_e$", r"Êlectron đã được cộng vào tổng hạt rời để cân với nguyên tử; trừ thêm là bù hai lần.")]),
  buoc("Năng lượng liên kết", "Năng lượng liên kết của hạt nhân canxi là bao nhiêu MeV?", 342.1, "MeV", 0.5,
       loi=r"Quên nhân $931{,}5$ hoặc nhân với $c^2$ sau khi đã đổi sang MeV.",
       ke=[(r"Nhân $\Delta m$ (u) với $931{,}5\ \text{MeV/u}$", True),
           (r"Nhân $\Delta m$ với $c^2$ tính bằng $\text{m}^2/\text{s}^2$ rồi đọc ra MeV", r"$931{,}5\ \text{MeV/u}$ đã chứa sẵn $c^2$ và hệ số đổi đơn vị."),
           (r"Chia $\Delta m$ cho $931{,}5$", r"Muốn đổi u sang MeV phải nhân với $931{,}5$.")]),
  buoc("Năng lượng liên kết riêng", "Năng lượng liên kết riêng của hạt nhân canxi là bao nhiêu MeV/nuclôn?", 8.55, "MeV/nuclôn", 0.02,
       loi=r"Chia cho số nơtron hoặc số prôtôn thay vì số khối.",
       ke=[(r"Chia $E_{lk}$ cho số khối $A$", True),
           (r"Chia $E_{lk}$ cho số nơtron $A-Z$", r"Mỗi nuclôn gồm cả prôtôn lẫn nơtron; phải chia cho cả số khối."),
           (r"Chia $E_{lk}$ cho tổng số hạt kể cả êlectron", r"Năng lượng liên kết riêng tính theo số nuclôn của hạt nhân; êlectron ở vỏ không phải nuclôn.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>cho $E_{lkr}$, hỏi khối lượng hạt nhân</b> → nghĩ tới <b>đi ngược</b>: nhân $A$, chia $931{,}5$, rồi trừ.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Năng lượng liên kết của cả hạt nhân", "Năng lượng liên kết của cả hạt nhân kripton là bao nhiêu MeV?", 732.5, "MeV", 0.5,
       loi=r"Dùng thẳng $E_{lkr}$ làm $E_{lk}$, hoặc nhân với số prôtôn thay vì số khối."),
  buoc("Độ hụt khối", "Độ hụt khối của hạt nhân kripton là bao nhiêu u?", 0.7863, "u", 0.0005,
       loi=r"Nhân thay vì chia cho $931{,}5$, hoặc chia $E_{lkr}$ (chưa nhân $A$) nên ra độ hụt khối của một nuclôn.",
       ke=[(r"Chia $E_{lk}$ cho $931{,}5$ để đổi MeV sang u", True),
           (r"Nhân $E_{lk}$ với $931{,}5$", r"Đã có MeV, muốn ra u thì chia; nhân sẽ ra số hàng trăm nghìn."),
           (r"Chia $E_{lkr}$ (không nhân $A$) cho $931{,}5$", r"Cách đó cho độ hụt khối trung bình của một nuclôn, không phải của cả hạt nhân.")]),
  buoc("Tổng khối lượng nuclôn rời", "Tổng khối lượng của các nuclôn rời là bao nhiêu u?", 84.6779, "u", 0.001,
       loi=r"Cộng $84$ khối lượng prôtôn, hoặc làm tròn mỗi nuclôn về $1\ \text{u}$ nên mất sạch độ hụt khối.",
       ke=[(r"Cộng khối lượng của $36$ prôtôn và $48$ nơtron", True),
           (r"Cộng khối lượng của $84$ prôtôn", r"Hạt nhân chỉ có $36$ prôtôn; các nuclôn còn lại là nơtron có khối lượng khác."),
           (r"Lấy $1\ \text{u}$ cho mỗi nuclôn", r"Làm tròn mỗi nuclôn về $1\ \text{u}$ làm mất cả độ hụt khối vốn chỉ cỡ phần trăm.")]),
  buoc("Khối lượng hạt nhân", "Khối lượng của hạt nhân kripton là bao nhiêu u?", 83.8915, "u", 0.001,
       loi=r"Cộng độ hụt khối vào tổng nuclôn rời thay vì trừ.",
       ke=[(r"Lấy tổng nuclôn rời trừ độ hụt khối", True),
           (r"Lấy tổng nuclôn rời cộng độ hụt khối", r"Hạt nhân nhẹ hơn các nuclôn rời nên phải trừ phần hụt đi."),
           (r"Lấy độ hụt khối trừ tổng nuclôn rời", r"Cho kết quả âm, không phải khối lượng.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>khối lượng chất (gam)</b> và hỏi năng lượng → nghĩ tới <b>$N=\dfrac{m}{M}N_A$</b>, rồi nhân năng lượng một hạt nhân.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Số hạt nhân trong mẫu", "Mẫu có bao nhiêu hạt nhân cacbon-12 (đơn vị $10^{23}$ hạt nhân)?", 1.505, "×10²³", 0.01,
       loi=r"Lấy $\dfrac{M}{m}$ ngược, hoặc quên nhân $N_A$ nên chỉ ra số mol."),
  buoc("Năng lượng của một hạt nhân", "Năng lượng toả ra khi tạo thành một hạt nhân cacbon-12 là bao nhiêu MeV?", 92.16, "MeV", 0.05,
       loi=r"Quên nhân $931{,}5$ hoặc đổi sang jun sớm làm sai lũy thừa mười ở bước sau.",
       ke=[(r"Nhân $\Delta m$ (u) với $931{,}5\ \text{MeV/u}$", True),
           (r"Chia $\Delta m$ cho $931{,}5$", r"Đổi u sang MeV là nhân với $931{,}5$; chia cho ra số rất nhỏ."),
           (r"Nhân $\Delta m$ với khối lượng mol $12$", r"Khối lượng mol dùng để đếm số hạt nhân, không dùng để đổi khối lượng sang năng lượng.")]),
  buoc("Năng lượng của cả mẫu", "Năng lượng toả ra khi tạo thành cả mẫu là bao nhiêu (đơn vị $10^{12}$ J)?", 2.22, "×10¹² J", 0.02,
       loi=r"Quên đổi MeV sang jun, hoặc dùng $1\ \text{eV}=1{,}6\cdot10^{-19}\ \text{J}$ cho MeV nên lệch sáu bậc.",
       ke=[(r"Nhân số hạt nhân với năng lượng một hạt nhân, rồi đổi MeV sang jun", True),
           (r"Chỉ đổi năng lượng của một hạt nhân ra jun", r"Mẫu có cỡ $10^{23}$ hạt nhân, mỗi hạt nhân toả năng lượng như nhau; phải nhân với số hạt nhân."),
           (r"Nhân số mol với năng lượng một hạt nhân, không cần $N_A$", r"Năng lượng đã tính ở bước trước là của MỘT hạt nhân; phải đổi số mol thành số hạt nhân bằng $N_A$ rồi mới nhân.")]),
  buoc("Khối lượng than tương đương", "Khối lượng than đá cho cùng năng lượng là bao nhiêu (đơn vị $10^{4}$ kg)?", 7.65, "×10⁴ kg", 0.1,
       loi=r"Nhân thay vì chia cho năng suất toả nhiệt, hoặc đọc tấn thành kilôgam.",
       ke=[(r"Chia năng lượng (J) cho năng suất toả nhiệt của than (J/kg)", True),
           (r"Nhân năng lượng với năng suất toả nhiệt", r"Kết quả có đơn vị $\text{J}^2/\text{kg}$, không phải kilôgam."),
           (r"Chia năng suất toả nhiệt cho năng lượng", r"Phép chia ngược cho một số rất nhỏ với đơn vị $\text{kg}^{-1}$, không phải khối lượng than.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
write(J, 16, "Bài 15. Năng lượng liên kết hạt nhân", DANG, BUILD, ANALYSIS, SOLS, None)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code)"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
