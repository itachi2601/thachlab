"""Bài 74 — "Bài 29. Định luật bảo toàn động lượng" (Vật lí 10, chương 5). 5 dạng + tự luận (ví dụ cũ chưa biên tập).
Mẫu: build-hinh-57.py / 58. Chạy: python3 scripts/data/bai-tap-mau/build-hinh-74.py  → ghi scripts/data/bai-tap-mau/74.json
Dạng theo quét: scripts/logs/batch-ra-soat/ket-qua/74.quet-dang.json. Hình: hinh_74.py (vec_luc: độ dài mũi tên = k·v).
Ví dụ cũ (old/74.json, 4 mục = 4 "Dạng" gồm ~30 câu):
  biên tập thành dạng mới: Dạng 1 (D1·Câu 4: hai quả cầu, tìm vận tốc sau va chạm), Dạng 2 (D2·Câu 1, 4: va chạm mềm, vật đứng yên/đang chạy),
  Dạng 3 (D1·Câu 3: va chạm đàn hồi khối lượng tỉ lệ 3:1), Dạng 4 (D2·Câu 3: hai xe dính nhau, ngược chiều), Dạng 5 (D3·Câu 1, 3: súng giật).
  vào tự luận (9 câu): D2·Câu 4, D1·Câu 2, D2·Câu 6, D1·Câu 5, D1·Câu 1, D1·Câu 8, D4·Câu 1, D3·Câu 8, D2·Câu 5 — công thức bị lỗi bóc tách
  (\\frac{m_{1}}{v}_{1}…) được gõ lại, nội dung/đáp số giữ nguyên.
  BỎ: D1·Câu 7 (đáp số 20,39 và 20,93 mâu thuẫn trong cùng lời giải), D1·Câu 9 (đáp số ghi m/s trong khi đề cho cm/s; dùng công thức đàn hồi ngoài bài),
  D1·Câu 10 và D3·Câu 2, 7, 10, 11 (vận tốc khí/đạn/người nhảy "đối với tên lửa/súng/xe" không nói trước hay sau khi tách → đáp số cũ phụ thuộc cách hiểu),
  D3·Câu 4, 5, 9 (lặp Câu 11), D3·Câu 6 (trùng ý Câu 8 bệ pháo), D4·Câu 2 (đạn nổ có phương xiên, lời giải cũ chưa kiểm được)."""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from hinh_74 import BUILD

J = os.path.join(HERE, "74.json")
T144, T145 = "Định luật bảo toàn động lượng cho hệ kín", "Va chạm mềm, va chạm đàn hồi"

# ═════════════ KIỂM SỐ LIỆU: tự giải lại độc lập, assert khớp số hiển thị ═════════════
def ok(name, got, want, tol):
    assert abs(got - want) <= tol, f"{name}: tính {got} ≠ hiển thị {want}"
# D1: ray đệm khí, xe 1 0,30 kg 0,60 m/s; xe 2 0,20 kg đứng yên, sau đó 0,45 m/s
m1, v1, m2, v2p = 0.30, 0.60, 0.20, 0.45
p0 = m1 * v1; ok("D1 p", p0, 0.18, 1e-12)
v1p = (p0 - m2 * v2p) / m1; ok("D1 v1'", v1p, 0.30, 1e-12)
ok("D1 kiểm", m1 * v1p + m2 * v2p, 0.18, 1e-12)
assert 0.5 * m1 * v1p**2 + 0.5 * m2 * v2p**2 < 0.5 * m1 * v1**2          # vật lí: động năng không tăng
assert abs(p0 - 0.30) > 0.05 and abs(v1p - p0) > 0.05                     # p ≠ v1' (không lẫn hai ô nhập)
assert abs((p0 - 0.45) / m1 - v1p) > 0.1 and abs(p0 / m1 - v1p) > 0.1     # cách sai: quên trừ động lượng xe 2 / bỏ m2
assert abs((p0 + m2 * v2p) - 0.18) > 0.05              # D1 s2: cộng cả động lượng xe 2 sau va chạm
assert abs(p0 / (m1 + m2) - v1p) > 0.05 and abs(p0 - v1p) > 0.05      # D1 s3 sai
# D2: xe đẩy A 150 kg 2,0 m/s, B 250 kg; a) B đứng yên b) B +0,40 m/s
mA, mB, vA = 150.0, 250.0, 2.0
pa = mA * vA; ok("D2 pa", pa, 300, 1e-9); va = pa / (mA + mB); ok("D2 va", va, 0.75, 1e-12)
pb = mA * vA + mB * 0.40; ok("D2 pb", pb, 400, 1e-9); vb = pb / (mA + mB); ok("D2 vb", vb, 1.0, 1e-12)
assert abs(pa / mA - va) > 0.5 and abs(mA * vA + mB * 0.4 - mA * vA * 0 - pb) < 1e-9
assert 0.40 < vb < vA                                                     # vận tốc chung nằm giữa hai vận tốc ban đầu
assert abs((pa - mB * 0.4) / (mA + mB) - vb) > 0.1                        # sai: trừ động lượng B
assert abs(300 / 250 - 0.75) > 0.3 and abs(300 / 150 - 0.75) > 0.3 and abs(400 / 150 - 1.0) > 0.3 and abs((2.0 + 0.4) / 2 - 1.0) > 0.1 and abs((300 - 100) / 400 - 1.0) > 0.3  # D2 các lựa chọn sai
# D3: xe 1 0,30 kg 0,80 m/s; xe 2 0,10 kg; sau 0,40 và 1,2 m/s
m1, v1, m2, a1, a2 = 0.30, 0.80, 0.10, 0.40, 1.2
ok("D3 p0", m1 * v1, 0.24, 1e-12); ok("D3 p", m1 * a1 + m2 * a2, 0.24, 1e-12)
W0 = 0.5 * m1 * v1**2; W1 = 0.5 * m1 * a1**2 + 0.5 * m2 * a2**2
ok("D3 W0", W0, 0.096, 1e-12); ok("D3 W1", W1, 0.096, 1e-12)
vc = m1 * v1 / (m1 + m2); ok("D3 vc", vc, 0.60, 1e-12); Wd = 0.5 * (m1 + m2) * vc**2; ok("D3 Wd", Wd, 0.072, 1e-12)
ok("D3 tỉ lệ", Wd / W0, m1 / (m1 + m2), 1e-12); ok("D3 75%", Wd / W0, 0.75, 1e-12)
assert abs(m1 * v1 - 0.096) > 0.1 and abs((m1 * a1 + m2 * a2) - W1) > 0.1  # p và W khác số
assert abs(0.5 * m1 * v1 ** 2 - 0.5 * (m1 + m2) * v1 ** 2) > 0.01         # sai: dùng v1 cho cả hệ
assert abs(0.5 * 0.30 * 0.40**2 - 0.072) > 0.01 and abs(0.5*(0.30+0.10)*(0.40+1.2)**2 - 0.096) > 0.01   # D3 các lựa chọn sai
# D4: goòng A 900 kg 2,0 m/s; B 600 kg ngược chiều 1,0 m/s (a) và 4,0 m/s (b)
mA, mB = 900.0, 600.0
pA = mA * 2.0 + mB * (-1.0); ok("D4 p", pA, 1200, 1e-9); v = pA / (mA + mB); ok("D4 v", v, 0.8, 1e-12)
u = mA * 2.0 / mB; ok("D4 u", u, 3.0, 1e-12); ok("D4 kiểm b", mA * 2.0 + mB * (-u), 0, 1e-9)
assert abs((mA * 2.0 + mB * 1.0) / (mA + mB) - v) > 0.3                   # sai: quên dấu −
assert abs(u - 2.0) > 0.5 and abs(u - mA * 2.0 / (mA + mB)) > 0.5 and abs(u - 1800 / 900) > 0.5   # sai: u = v_A; chia cho khối lượng cả hệ; chia cho m_A
assert abs(pA / mA - v) > 0.3
assert abs((2.0 + 1.0) / 2 - v) > 0.3 and abs(mA * 2.0 / (mA + mB) - v) > 0.1
assert abs((mA*2.0+mB*1.0)/(mA+mB) - v) > 0.3 and abs(mA*2.0/(mA+mB) - v) > 0.3 and abs(pA/mA - v) > 0.3 and abs((2.0-1.0)/2 - 0.8) > 0.2 and abs((2.0+1.0)/2 - v) > 0.3
# D5
Msg, mdn, vd = 2.5, 0.010, 400.0
V = mdn * vd / Msg; ok("D5 V", V, 1.6, 1e-12); ok("D5 kiểm", -Msg * V + mdn * vd, 0, 1e-12)
Mr = 0.60 - 0.10; ok("D5 Mr", Mr, 0.50, 1e-12); V2 = 0.10 * 30.0 / Mr; ok("D5 V2", V2, 6.0, 1e-12); ok("D5 kiểm2", -Mr * V2 + 0.10 * 30.0, 0, 1e-12)
assert abs(0.10 * 30.0 / 0.60 - V2) > 0.5 and abs(0.2 * vd / Msg - V) > 0.5      # sai: chia cho khối lượng cả tên lửa; đổi nhầm 10 g = 0,2 kg
assert abs(10 * 400 / 2.5 - 1.6) > 1 and abs(2.5 * 400 / 0.010 - 1.6) > 1 and abs(0.10 - 0.50) > 0.3 and abs(0.10 * 30 / 0.60 - 6.0) > 0.5 and abs(30 - 6.0) > 5  # D5 các lựa chọn sai
# Tự luận cũ
ok("TL1a", 0.035 * 475 / 5.035, 3.3, 0.05); ok("TL1b", (0.035 * 475 + 5 * 0.5) / 5.035, 3.8, 0.05); ok("TL1c", (0.035 * 475 - 5 * 0.5) / 5.035, 2.8, 0.05)
ok("TL2", 3.0 / 2.0, 1.5, 1e-12)                                          # m·3 = −m v + 3m v → v = 1,5
ok("TL3a", (38 * 1 - 2 * 7) / 40, 0.6, 1e-12); ok("TL3b", (38 * 1 + 2 * 7) / 40, 1.3, 1e-12)
ok("TL4a", (390 * 8 - 10 * 12) / 400, 7.5, 1e-12); ok("TL4b", 390 * 8 / 400, 7.8, 1e-12)
m2x = (0.2 * (-1.8) - 0.2 * 3) / (-1.0 - 2.2); ok("TL5 m2", m2x, 0.3, 1e-12)
# bi thép / bi ve: 5m·4 − m·1 = 5m v1' + m·5v1'
ok("TL6", 19 / 10, 1.9, 1e-12); ok("TL6b", 5 * 1.9, 9.5, 1e-12)
ok("TL7", (2.5 * 10 - 1.5 * 25) / 1.0, -12.5, 1e-12)
ok("TL8a", 5 * 600 / 1500, 2, 1e-12); ok("TL8b", 5 * 600 * math.cos(math.radians(60)) / 1500, 1, 1e-9)
vv = math.sqrt(2 * 9.8 * 0.05); ok("TL9 v", vv, 0.99, 0.005); ok("TL9 v0", 1.005 * vv / 0.005, 199, 0.5)

# ═════════════ Đề chữ (hình mô phỏng do BUILD chèn dưới đề) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Nhận biết hệ kín và áp dụng định luật bảo toàn động lượng", topic=T144,
      problem_html=r"""<p>Trên đường ray đệm khí nằm ngang (ma sát coi như bằng $0$), xe 1 khối lượng $0{,}30\ \text{kg}$ chạy với tốc độ $0{,}60\ \text{m/s}$ tới đẩy xe 2 khối lượng $0{,}20\ \text{kg}$ đang đứng yên. Ngay sau va chạm, xe 2 chạy cùng chiều với xe 1, tốc độ $0{,}45\ \text{m/s}$.</p>
<ol type="a"><li>Hệ gồm hai xe có coi là hệ kín trong lúc va chạm không? Vì sao?</li>
<li>Tính vận tốc của xe 1 ngay sau va chạm (độ lớn và chiều).</li></ol>"""),
 dict(label="Dạng 2 · Dễ · Va chạm mềm: tính vận tốc chung", topic=T145,
      problem_html=r"""<p>Trong một kho hàng, xe đẩy A khối lượng $150\ \text{kg}$ chạy với tốc độ $2{,}0\ \text{m/s}$ trên nền phẳng nhẵn tới va vào xe đẩy B khối lượng $250\ \text{kg}$. Sau va chạm hai xe móc dính vào nhau. Bỏ qua ma sát. Tính tốc độ của hai xe ngay sau va chạm khi:</p>
<ol type="a"><li>xe B đang đứng yên;</li><li>xe B đang chạy cùng chiều với xe A, tốc độ $0{,}40\ \text{m/s}$.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Phân biệt va chạm mềm và va chạm đàn hồi", topic=T145,
      problem_html=r"""<p>Trên đường ray đệm khí, xe 1 khối lượng $0{,}30\ \text{kg}$ chạy với tốc độ $0{,}80\ \text{m/s}$ tới va vào xe 2 khối lượng $0{,}10\ \text{kg}$ đang đứng yên. Sau va chạm hai xe tách nhau và cùng chạy theo chiều ban đầu của xe 1: xe 1 có tốc độ $0{,}40\ \text{m/s}$, xe 2 có tốc độ $1{,}2\ \text{m/s}$.</p>
<ol type="a"><li>Tổng động lượng của hệ có được bảo toàn không?</li>
<li>Tổng động năng của hệ có được bảo toàn không? Va chạm này là mềm hay đàn hồi?</li>
<li>Nếu hai xe dính nhau sau va chạm (cùng điều kiện đầu) thì tổng động năng của hệ ngay sau đó là bao nhiêu?</li></ol>"""),
 dict(label="Dạng 4 · Trung bình · Bảo toàn động lượng với vận tốc ngược chiều", topic=T144,
      problem_html=r"""<p>Hai goòng chạy ngược chiều nhau trên đường ray thẳng nằm ngang của một hầm mỏ, tới đâm vào nhau rồi móc dính. Goòng A khối lượng $900\ \text{kg}$, tốc độ $2{,}0\ \text{m/s}$; goòng B khối lượng $600\ \text{kg}$, tốc độ $1{,}0\ \text{m/s}$. Bỏ qua ma sát.</p>
<ol type="a"><li>Tính vận tốc của hai goòng ngay sau va chạm (độ lớn và chiều).</li>
<li>Goòng A giữ nguyên số liệu. Goòng B phải chạy ngược chiều A với tốc độ bao nhiêu để sau va chạm hai goòng đứng yên?</li></ol>"""),
 dict(label="Dạng 5 · Khó · Chuyển động bằng phản lực: súng giật, tên lửa", topic=T144,
      problem_html=r"""<p>Cả hai hệ dưới đây ban đầu đứng yên.</p>
<ol type="a"><li>Một khẩu súng khối lượng $2{,}5\ \text{kg}$ (không kể đạn) đặt tự do trên mặt phẳng nhẵn, bắn viên đạn khối lượng $10\ \text{g}$ theo phương ngang với tốc độ $400\ \text{m/s}$ so với mặt đất. Tính tốc độ giật lùi của súng.</li>
<li>Một tên lửa mô hình khối lượng $0{,}60\ \text{kg}$ (kể cả khí) đặt trên đường ray đệm khí nằm ngang. Khi bật động cơ, nó phụt tức thời $0{,}10\ \text{kg}$ khí về phía sau với tốc độ $30\ \text{m/s}$ so với mặt đất. Tính tốc độ của tên lửa ngay sau khi phụt khí.</li></ol>"""),
]
FORMS = ["bai_tap"] * 5

# ═════════════ Bảng phân tích đề: Câu trong đề | Dữ liệu | Kiến thức liên quan ═════════════
ANALYSIS = [
 [(r"“đường ray đệm khí nằm ngang (ma sát coi như bằng $0$)”", r"Ma sát $\approx0$", r"⚠ Điều kiện dùng định luật: xét hệ có kín không (ngoại lực bằng $0$ hay cân bằng nhau?)"),
  (r"“xe 1 khối lượng $0{,}30$ kg chạy với tốc độ $0{,}60$ m/s”", r"$m_1=0{,}30\ \text{kg}$; $v_1=0{,}60\ \text{m/s}$", r"Động lượng $p=mv$; chọn chiều dương theo xe 1"),
  (r"“xe 2 khối lượng $0{,}20$ kg đang đứng yên”", r"$m_2=0{,}20\ \text{kg}$; $v_2=0$", r"Động lượng của vật đứng yên"),
  (r"“Ngay sau va chạm, xe 2 chạy cùng chiều xe 1, tốc độ $0{,}45$ m/s”", r"$v_2'=+0{,}45\ \text{m/s}$", r"Va chạm rất ngắn: so sánh trạng thái ngay trước và ngay sau"),
  (r"“a) có coi là hệ kín không?”", r"Cần nhận xét về ngoại lực", r"Hệ kín; nội lực và ngoại lực"),
  (r"“b) vận tốc của xe 1 ngay sau va chạm (độ lớn và chiều)”", r"Cần $v_1'$ (m/s) có dấu", r"Tổng động lượng trước = tổng động lượng sau; dấu của kết quả cho biết chiều")],
 [(r"“nền phẳng nhẵn … Bỏ qua ma sát”", r"Ngoại lực cân bằng", r"⚠ Hệ kín (ngoại lực cân bằng hoặc bỏ qua được) thì mới dùng được bảo toàn động lượng"),
  (r"“xe đẩy A khối lượng $150$ kg chạy với tốc độ $2{,}0$ m/s”", r"$m_A=150\ \text{kg}$; $v_A=2{,}0\ \text{m/s}$", r"Chọn chiều dương theo xe A"),
  (r"“xe đẩy B khối lượng $250$ kg”", r"$m_B=250\ \text{kg}$", r"Khối lượng vật bị va vào"),
  (r"“Sau va chạm hai xe móc dính vào nhau”", r"Hai xe chung vận tốc $v$", r"Va chạm mềm: $m_1\vec v_1+m_2\vec v_2=(m_1+m_2)\vec v$"),
  (r"“a) xe B đang đứng yên”", r"$v_B=0$", r"Vật đứng yên có động lượng bằng bao nhiêu?"),
  (r"“b) xe B chạy cùng chiều xe A, tốc độ $0{,}40$ m/s”", r"$v_B=+0{,}40\ \text{m/s}$", r"⚠ Vận tốc cùng chiều dương mang dấu $+$"),
  (r"“tốc độ của hai xe ngay sau va chạm”", r"Cần $v$ (m/s) ở hai trường hợp", r"Đại lượng cần tìm")],
 [(r"“Trên đường ray đệm khí”", r"Ma sát $\approx0$", r"⚠ Hệ kín là điều kiện dùng bảo toàn động lượng; động năng phải kiểm riêng"),
  (r"“xe 1 khối lượng $0{,}30$ kg … tốc độ $0{,}80$ m/s”", r"$m_1=0{,}30\ \text{kg}$; $v_1=0{,}80\ \text{m/s}$", r"Động lượng $p=mv$; động năng $W_{\text{đ}}=\tfrac12mv^2$"),
  (r"“xe 2 khối lượng $0{,}10$ kg đang đứng yên”", r"$m_2=0{,}10\ \text{kg}$; $v_2=0$", r"Vật đứng yên: động lượng và động năng"),
  (r"“hai xe tách nhau … xe 1 $0{,}40$ m/s, xe 2 $1{,}2$ m/s”", r"$v_1'=0{,}40\ \text{m/s}$; $v_2'=1{,}2\ \text{m/s}$", r"Hai xe có vận tốc riêng sau va chạm"),
  (r"“a) động lượng có bảo toàn không?”", r"So tổng $p$ trước và sau", r"Cộng động lượng của từng xe"),
  (r"“b) động năng có bảo toàn không? mềm hay đàn hồi?”", r"So tổng $W_{\text{đ}}$ trước và sau", r"⚠ Muốn phân loại va chạm phải kiểm cả động lượng lẫn động năng"),
  (r"“c) nếu hai xe dính nhau sau va chạm”", r"Hai xe chung vận tốc $v$", r"Va chạm mềm: tìm $v$ rồi tính $W_{\text{đ}}$ của cả hệ")],
 [(r"“đường ray thẳng nằm ngang … Bỏ qua ma sát”", r"Ngoại lực cân bằng", r"⚠ Hệ kín mới dùng được bảo toàn động lượng"),
  (r"“chạy ngược chiều nhau”", r"Hai vận tốc trái dấu", r"⚠ Chọn chiều dương trước khi thế số; vận tốc ngược chiều dương mang dấu $-$"),
  (r"“goòng A khối lượng $900$ kg, tốc độ $2{,}0$ m/s”", r"$m_A=900\ \text{kg}$; $v_A=2{,}0\ \text{m/s}$", r"Động lượng $p=mv$ (đại số)"),
  (r"“goòng B khối lượng $600$ kg, tốc độ $1{,}0$ m/s”", r"$m_B=600\ \text{kg}$; $\lvert v_B\rvert=1{,}0\ \text{m/s}$", r"Tốc độ là số không âm; vận tốc thì có dấu"),
  (r"“tới đâm vào nhau rồi móc dính”", r"Chung vận tốc $v$", r"Va chạm mềm: $m_Av_A+m_Bv_B=(m_A+m_B)v$"),
  (r"“a) vận tốc … (độ lớn và chiều)”", r"Cần $v$ có dấu", r"Dấu của $v$ cho biết chiều chuyển động"),
  (r"“b) goòng B phải chạy với tốc độ bao nhiêu để sau va chạm hai goòng đứng yên”", r"Cần tốc độ $u$ của goòng B; sau va chạm $v=0$", r"Điều kiện để hai vật đứng yên sau va chạm")],
 [(r"“ban đầu đứng yên”", r"Tổng động lượng trước $=0$", r"⚠ Hệ đứng yên rồi tách làm hai: tổng động lượng sau cũng phải bằng $\vec0$"),
  (r"“súng khối lượng $2{,}5$ kg (không kể đạn)”", r"$M=2{,}5\ \text{kg}$", r"Phần còn lại sau khi đạn rời đi"),
  (r"“viên đạn khối lượng $10$ g … $400$ m/s so với mặt đất”", r"$m=10\ \text{g}$; $v=400\ \text{m/s}$", r"⚠ Đổi khối lượng ra kg trước khi thế số"),
  (r"“a) tốc độ giật lùi của súng”", r"Cần $\lvert V\rvert$ (m/s)", r"$m\vec v+M\vec V=\vec0$"),
  (r"“tên lửa mô hình khối lượng $0{,}60$ kg (kể cả khí)”", r"Tổng khối lượng trước khi phụt", r"⚠ Sau khi phụt, khối lượng phần còn lại là bao nhiêu?"),
  (r"“phụt tức thời $0{,}10$ kg khí … $30$ m/s so với mặt đất”", r"$m=0{,}10\ \text{kg}$; $v=30\ \text{m/s}$", r"Phần tách ra đi về một hướng"),
  (r"“b) tốc độ của tên lửa ngay sau khi phụt khí”", r"Cần $\lvert V\rvert$ (m/s)", r"Phần còn lại chuyển động thế nào so với phần tách ra?")],
]

# ═════════════ Lời giải từng bước ═════════════
R_KIN = [r"<strong>Hệ</strong> là nhóm vật xét; <strong>nội lực</strong> là lực giữa các vật trong hệ, <strong>ngoại lực</strong> là lực từ bên ngoài.",
         r"<strong>Hệ kín:</strong> không có ngoại lực, hoặc các ngoại lực cân bằng nhau.",
         r"<strong>Định luật:</strong> hệ kín thì tổng vectơ động lượng không đổi: $m_1\vec v_1+m_2\vec v_2=m_1\vec v_1'+m_2\vec v_2'$.",
         r"Chọn chiều dương rồi thế vận tốc có dấu.",
         r"⚠ <strong>Điều kiện:</strong> chỉ dùng cho hệ kín (hoặc va chạm rất ngắn, ngoại lực không đáng kể)."]
R_MEM = [r"<strong>Va chạm mềm:</strong> sau va chạm hai vật dính nhau, chuyển động với cùng vận tốc $v$.",
         r"Hệ kín: $m_1\vec v_1+m_2\vec v_2=(m_1+m_2)\vec v$.",
         r"$v=\dfrac{m_1v_1+m_2v_2}{m_1+m_2}$ (giá trị đại số).",
         r"Vật đứng yên: $v_2=0$.",
         r"⚠ <strong>Điều kiện:</strong> hệ kín trong lúc va chạm; chọn chiều dương trước khi thế số."]
R_PL = [r"Cả hai loại va chạm: <strong>động lượng bảo toàn</strong> ($p=mv$).",
        r"<strong>Mềm:</strong> dính nhau, động năng giảm.",
        r"<strong>Đàn hồi:</strong> rời nhau, động năng giữ nguyên ($W_{\text{đ}}=\tfrac12mv^2$).",
        r"Hai vật dính nhau: $v=\dfrac{m_1v_1+m_2v_2}{m_1+m_2}$.",
        r"⚠ <strong>Điều kiện:</strong> muốn phân loại phải kiểm <em>cả</em> động lượng <em>lẫn</em> động năng — chỉ động lượng bảo toàn thì chưa kết luận được."]
R_NC = [r"<strong>Hệ kín:</strong> $m_1\vec v_1+m_2\vec v_2=m_1\vec v_1'+m_2\vec v_2'$.",
        r"Va chạm mềm: $m_Av_A+m_Bv_B=(m_A+m_B)v$.",
        r"Chọn <strong>chiều dương</strong>; vận tốc ngược chiều dương mang dấu $-$.",
        r"Dấu của $v$ sau va chạm cho biết chiều chuyển động.",
        r"⚠ <strong>Điều kiện:</strong> phương trình vectơ thế số thành phương trình đại số theo chiều dương đã chọn."]
R_PH = [r"<strong>Chuyển động bằng phản lực:</strong> một phần của hệ tách ra theo một hướng, phần còn lại đi ngược hướng.",
        r"Hệ ban đầu đứng yên: $m\vec v+M\vec V=\vec0\ \Rightarrow\ V=-\dfrac{m}{M}v$ (dấu $-$: ngược chiều).",
        r"Đổi khối lượng ra kg: $1\ \text{g}=0{,}001\ \text{kg}$.",
        r"⚠ <strong>Điều kiện:</strong> $M$ là khối lượng <em>phần còn lại</em> sau khi tách; hệ đứng yên thì tổng động lượng trước bằng $0$."]

SOLS = [
 sol(R_KIN, [
  (r"Chọn hệ và kiểm tra hệ kín", [P(r"Hệ gồm hai xe. Lực xe 1 đẩy xe 2 và lực xe 2 đẩy xe 1 là nội lực."), P(r"Ngoại lực: trọng lực cân bằng với phản lực của đệm khí; ma sát coi như bằng $0$."), A(r"T:Hệ hai xe là <strong>hệ kín</strong> trong lúc va chạm, nên động lượng được bảo toàn.")]),
  (r"Tổng động lượng trước va chạm", [P(r"Chọn chiều dương theo chiều chuyển động của xe 1; xe 2 đứng yên:"), M(r"p=m_1v_1+m_2v_2=0{,}30\cdot0{,}60+0{,}20\cdot0"), A(r"p=0{,}18\ \text{kg}\cdot\text{m/s}")]),
  (r"Vận tốc xe 1 sau va chạm", [P(r"Tổng động lượng sau bằng tổng động lượng trước:"), M(r"m_1v_1'+m_2v_2'=p"), M(r"v_1'=\dfrac{p-m_2v_2'}{m_1}=\dfrac{0{,}18-0{,}20\cdot0{,}45}{0{,}30}"), A(r"v_1'=0{,}30\ \text{m/s}"), P(r"$v_1'\gt0$: xe 1 vẫn chạy theo chiều cũ, chậm lại vì đã đẩy xe 2.")]),
  (r"Kiểm tra", [M(r"m_1v_1'+m_2v_2'=0{,}30\cdot0{,}30+0{,}20\cdot0{,}45=0{,}18\ \text{kg}\cdot\text{m/s}"), P(r"Bằng $p$ trước va chạm ✓."), P(r"Động năng sau ($0{,}034\ \text{J}$) nhỏ hơn trước ($0{,}054\ \text{J}$): hợp lí, va chạm không làm động năng tăng.")])],
  [r"a) Có: trọng lực cân bằng phản lực, ma sát coi như bằng $0$", r"b) $v_1'=0{,}30\ \text{m/s}$, cùng chiều chuyển động ban đầu"],
  r"Nhận dạng: đề cho <strong>vận tốc trước, một vận tốc sau và mặt không ma sát</strong> → kiểm hệ kín rồi bảo toàn tổng động lượng."),
 sol(R_MEM, [
  (r"Tổng động lượng trước va chạm (a)", [P(r"Chọn chiều dương theo xe A; xe B đứng yên:"), M(r"p=m_Av_A+m_Bv_B=150\cdot2{,}0+250\cdot0"), A(r"p=300\ \text{kg}\cdot\text{m/s}")]),
  (r"Vận tốc chung (a)", [P(r"Sau va chạm hai xe dính nhau, khối lượng chung $m_A+m_B$:"), M(r"v=\dfrac{p}{m_A+m_B}=\dfrac{300}{150+250}"), A(r"v=0{,}75\ \text{m/s}"), P(r"Cùng chiều với xe A.")]),
  (r"Tổng động lượng trước va chạm (b)", [P(r"Xe B chạy cùng chiều dương nên $v_B=+0{,}40\ \text{m/s}$:"), M(r"p=m_Av_A+m_Bv_B=150\cdot2{,}0+250\cdot0{,}40=300+100"), A(r"p=400\ \text{kg}\cdot\text{m/s}")]),
  (r"Vận tốc chung (b)", [M(r"v=\dfrac{p}{m_A+m_B}=\dfrac{400}{150+250}"), A(r"v=1{,}0\ \text{m/s}"), P(r"Cùng chiều với xe A.")]),
  (r"Kiểm tra", [P(r"Hai xe dính nhau chạy với một vận tốc nằm giữa hai vận tốc ban đầu: ở (a) từ $0$ đến $2{,}0\ \text{m/s}$; ở (b) từ $0{,}40$ đến $2{,}0\ \text{m/s}$ ✓."), P(r"Xe B có thêm động lượng ở (b) nên hai xe chạy nhanh hơn ở (a) ✓.")])],
  [r"a) $v=0{,}75\ \text{m/s}$", r"b) $v=1{,}0\ \text{m/s}$", r"Cả hai: cùng chiều chuyển động ban đầu của xe A"],
  r"Nhận dạng: đề nói <strong>hai vật dính nhau / móc vào nhau</strong> sau va chạm → va chạm mềm: cộng khối lượng, chia tổng động lượng."),
 sol(R_PL, [
  (r"Động lượng trước và sau", [P(r"Chọn chiều dương theo chiều chuyển động của xe 1:"), M(r"p_{\text{trước}}=m_1v_1=0{,}30\cdot0{,}80=0{,}24"), M(r"p_{\text{sau}}=m_1v_1'+m_2v_2'=0{,}30\cdot0{,}40+0{,}10\cdot1{,}2"), A(r"p_{\text{sau}}=0{,}24\ \text{kg}\cdot\text{m/s}"), P(r"Bằng $p_{\text{trước}}$: động lượng bảo toàn ✓.")]),
  (r"Động năng trước và sau", [M(r"W_{\text{trước}}=\tfrac12m_1v_1^2=\tfrac12\cdot0{,}30\cdot0{,}80^2=0{,}096"), M(r"W_{\text{sau}}=\tfrac12m_1v_1'^2+\tfrac12m_2v_2'^2=\tfrac12\cdot0{,}30\cdot0{,}40^2+\tfrac12\cdot0{,}10\cdot1{,}2^2"), A(r"W_{\text{sau}}=0{,}096\ \text{J}"), P(r"Bằng $W_{\text{trước}}$: động năng cũng bảo toàn.")]),
  (r"Phân loại va chạm", [A(r"T:Cả động lượng lẫn động năng đều bảo toàn, hai xe tách nhau: đây là va chạm <strong>đàn hồi</strong>.")]),
  (r"Nếu hai xe dính nhau", [P(r"Va chạm mềm, cùng điều kiện đầu: tìm vận tốc chung rồi tính động năng của cả hệ."), M(r"v=\dfrac{m_1v_1}{m_1+m_2}=\dfrac{0{,}24}{0{,}40}=0{,}60\ \text{m/s}"), M(r"W=\tfrac12(m_1+m_2)v^2=\tfrac12\cdot0{,}40\cdot0{,}60^2"), A(r"W=0{,}072\ \text{J}")]),
  (r"Kiểm tra", [M(r"\dfrac{W}{W_{\text{trước}}}=\dfrac{0{,}072}{0{,}096}=0{,}75=\dfrac{m_1}{m_1+m_2}"), P(r"Va chạm mềm mất $25\,\%$ động năng (thành nhiệt, biến dạng) ✓."), P(r"Động lượng ở cả hai trường hợp đều là $0{,}24\ \text{kg}\cdot\text{m/s}$.")])],
  [r"a) Có: $p_{\text{trước}}=p_{\text{sau}}=0{,}24\ \text{kg}\cdot\text{m/s}$", r"b) Có: $W_{\text{trước}}=W_{\text{sau}}=0{,}096\ \text{J}$, va chạm đàn hồi", r"c) $W=0{,}072\ \text{J}$"],
  r"Nhận dạng: đề hỏi <strong>mềm hay đàn hồi</strong> → tính cả tổng động lượng và tổng động năng trước, sau rồi so."),
 sol(R_NC, [
  (r"Chọn chiều dương và gán dấu", [P(r"Chọn chiều dương theo chiều chuyển động của goòng A."), M(r"v_A=+2{,}0\ \text{m/s}"), M(r"v_B=-1{,}0\ \text{m/s}"), P(r"Đề cho tốc độ của B là số dương, nhưng B chạy ngược chiều dương nên vận tốc mang dấu $-$.")]),
  (r"Tổng động lượng trước va chạm (a)", [M(r"p=m_Av_A+m_Bv_B=900\cdot2{,}0+600\cdot(-1{,}0)=1800-600"), A(r"p=1200\ \text{kg}\cdot\text{m/s}")]),
  (r"Vận tốc chung (a)", [M(r"v=\dfrac{p}{m_A+m_B}=\dfrac{1200}{900+600}"), A(r"v=0{,}8\ \text{m/s}"), P(r"$v\gt0$: hai goòng chạy theo chiều của goòng A, tốc độ $0{,}8\ \text{m/s}$.")]),
  (r"Tốc độ goòng B để hai goòng đứng yên (b)", [P(r"Sau va chạm hai goòng đứng yên nên tổng động lượng sau bằng $0$, cũng là tổng trước. Gọi $u$ là tốc độ goòng B ($v_B=-u$):"), M(r"m_Av_A+m_B(-u)=0"), M(r"u=\dfrac{m_Av_A}{m_B}=\dfrac{900\cdot2{,}0}{600}"), A(r"u=3{,}0\ \text{m/s}")]),
  (r"Kiểm tra", [M(r"p=900\cdot2{,}0+600\cdot(-3{,}0)=1800-1800=0"), P(r"Động lượng goòng A được goòng B triệt tiêu đúng ✓."), P(r"Hai goòng đứng yên nên toàn bộ động năng ban đầu biến thành nhiệt và biến dạng.")])],
  [r"a) $v=0{,}8\ \text{m/s}$, theo chiều của goòng A", r"b) Goòng B phải chạy với tốc độ $3{,}0\ \text{m/s}$"],
  r"Nhận dạng: đề cho <strong>hai vật chạy ngược chiều</strong> → chọn chiều dương trước, vận tốc ngược chiều mang dấu $-$, đọc chiều từ dấu của kết quả; muốn hai vật đứng yên thì cho tổng động lượng bằng $0$."),
 sol(R_PH, [
  (r"Đổi đơn vị khối lượng", [M(r"m=10\ \text{g}=10\cdot0{,}001\ \text{kg}"), A(r"m=0{,}010\ \text{kg}")]),
  (r"Súng giật lùi (a)", [P(r"Hệ ban đầu đứng yên nên tổng động lượng trước bằng $0$. Chọn chiều dương theo chiều đạn bay:"), M(r"mv+MV=0"), M(r"V=-\dfrac{mv}{M}=-\dfrac{0{,}010\cdot400}{2{,}5}"), A(r"V=-1{,}6\ \text{m/s}"), P(r"Dấu $-$: súng giật ngược chiều đạn, tốc độ $1{,}6\ \text{m/s}$.")]),
  (r"Khối lượng phần tên lửa còn lại (b)", [P(r"Khối lượng $0{,}60\ \text{kg}$ gồm cả khí; sau khi phụt, phần còn lại:"), M(r"M'=0{,}60-0{,}10"), A(r"M'=0{,}50\ \text{kg}")]),
  (r"Tốc độ tên lửa (b)", [P(r"Chọn chiều dương theo chiều khí phụt:"), M(r"mv+M'V=0"), M(r"V=-\dfrac{mv}{M'}=-\dfrac{0{,}10\cdot30}{0{,}50}"), A(r"V=-6{,}0\ \text{m/s}"), P(r"Tên lửa chạy ngược chiều khí phụt, tốc độ $6{,}0\ \text{m/s}$.")]),
  (r"Kiểm tra", [M(r"MV+mv=2{,}5\cdot(-1{,}6)+0{,}010\cdot400=0"), M(r"M'V+mv=0{,}50\cdot(-6{,}0)+0{,}10\cdot30=0"), P(r"Cả hai: tổng động lượng sau bằng $0$, đúng bằng trước khi tách ✓.")])],
  [r"a) Súng giật lùi với tốc độ $1{,}6\ \text{m/s}$", r"b) Tên lửa chạy với tốc độ $6{,}0\ \text{m/s}$, ngược chiều khí phụt"],
  r"Nhận dạng: <strong>hệ đứng yên rồi tách làm hai phần</strong> → tổng động lượng bằng $0$: phần nhỏ đi nhanh một hướng, phần lớn đi chậm hướng ngược lại."),
]

# ═════════════ Tự giải từng bước ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>va chạm trên đệm khí, ma sát bằng 0</b> → nghĩ tới <b>hệ kín</b>: tổng động lượng trước = sau.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc(r"Chọn hệ và kiểm tra hệ kín", r"Chọn nhận xét đúng về hệ hai xe trong lúc va chạm.",
       loi=r"Cho rằng có trọng lực tác dụng thì hệ không kín, hoặc coi lực giữa hai xe là ngoại lực.",
       lua_chon=[(r"Kín: trọng lực cân bằng phản lực đệm khí, ma sát bằng $0$", True),
                 (r"Không kín, vì trọng lực vẫn tác dụng lên hai xe", r"Trọng lực bị phản lực của đệm khí cân bằng; hệ kín cho phép các ngoại lực cân bằng nhau."),
                 (r"Không kín, vì hai xe tác dụng lực lên nhau", r"Lực giữa hai xe nằm trong hệ nên là nội lực; nội lực không làm mất tính kín.")]),
  buoc(r"Tổng động lượng trước va chạm", r"Tổng động lượng của hệ ngay trước va chạm bằng bao nhiêu? (chiều dương theo xe 1)", 0.18, "kg·m/s", 0.005,
       loi=r"Cộng thêm động lượng cho xe 2 dù nó đang đứng yên, hoặc quên nhân với khối lượng.",
       ke=[(r"Cộng động lượng từng xe theo vận tốc trước va chạm", True),
           (r"Lấy tổng khối lượng nhân với tốc độ của xe 1", r"Hai xe chưa chuyển động cùng nhau trước va chạm; xe 2 đứng yên."),
           (r"Cộng cả động lượng xe 2 theo tốc độ sau va chạm", r"Tổng trước va chạm chỉ dùng vận tốc trước va chạm; tốc độ của xe 2 sau va chạm thuộc vế sau.")]),
  buoc(r"Vận tốc xe 1 sau va chạm", r"Vận tốc của xe 1 ngay sau va chạm bằng bao nhiêu? (cùng chiều dương)", 0.30, "m/s", 0.01,
       loi=r"Đặt tổng động lượng sau bằng động lượng của riêng xe 1, quên phần động lượng xe 2 mang đi.",
       ke=[(r"Tổng động lượng sau = tổng trước, rồi rút $v_1'$", True),
           (r"Cho $m_1v_1'$ bằng tổng trước, bỏ phần xe 2 mang đi", r"Sau va chạm xe 2 cũng mang động lượng, không thể bỏ."),
           (r"Cho $v_1'=v_2'$ vì hai xe cùng chiều sau va chạm", r"Hai xe cùng chiều nhưng không dính nhau, vận tốc không bắt buộc bằng nhau.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>hai vật dính / móc vào nhau</b> sau va chạm → nghĩ tới <b>va chạm mềm</b>: chung vận tốc $v$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc(r"Tổng động lượng trước va chạm (a)", r"Tổng động lượng của hệ ngay trước va chạm ở câu a) bằng bao nhiêu?", 300, "kg·m/s", 5,
       loi=r"Cộng khối lượng hai xe rồi nhân với tốc độ của xe A, coi cả hai đã chạy từ trước."),
  buoc(r"Vận tốc chung (a)", r"Tốc độ của hai xe sau va chạm ở câu a) bằng bao nhiêu?", 0.75, "m/s", 0.02,
       loi=r"Chia tổng động lượng cho khối lượng của xe A thay vì của cả hai xe dính nhau.",
       ke=[(r"Chia tổng động lượng cho tổng khối lượng hai xe", True),
           (r"Chia cho khối lượng xe A, vì xe A là xe chạy tới", r"Sau khi móc dính, cả hai xe cùng mang động lượng nên phải chia cho tổng khối lượng."),
           (r"Chia cho khối lượng xe B, vì xe B bị va vào", r"Sau khi móc dính, hai xe thành một vật có khối lượng chung bằng tổng.")]),
  buoc(r"Tổng động lượng trước va chạm (b)", r"Tổng động lượng của hệ ngay trước va chạm ở câu b) bằng bao nhiêu?", 400, "kg·m/s", 5,
       loi=r"Bỏ qua động lượng xe B vì nó chạy chậm, hoặc trừ thay vì cộng dù cùng chiều.",
       ke=[(r"Cộng động lượng hai xe, cùng chiều dương nên cùng dấu", True),
           (r"Chỉ tính động lượng xe A, như ở câu a) khi xe B đứng yên", r"Ở câu b) xe B đang chạy nên cũng mang động lượng."),
           (r"Trừ động lượng xe B vì nó chạy chậm hơn", r"Cùng chiều với xe A nên động lượng cùng dấu; chỉ vận tốc ngược chiều mới mang dấu $-$.")]),
  buoc(r"Vận tốc chung (b)", r"Tốc độ của hai xe sau va chạm ở câu b) bằng bao nhiêu?", 1.0, "m/s", 0.02,
       loi=r"Dùng lại kết quả câu a) hoặc chia cho khối lượng một xe.",
       ke=[(r"Chia tổng động lượng mới cho tổng khối lượng hai xe", True),
           (r"Chia động lượng mới cho khối lượng xe A", r"Hai xe dính nhau nên phải chia cho khối lượng chung của cả hai xe."),
           (r"Lấy trung bình cộng hai tốc độ ban đầu", r"Vận tốc chung phụ thuộc khối lượng, không phải trung bình cộng của các tốc độ.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy hỏi <b>mềm hay đàn hồi</b> → nghĩ tới <b>kiểm cả động lượng lẫn động năng</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc(r"Động lượng trước và sau", r"Tổng động lượng của hệ ngay sau va chạm bằng bao nhiêu?", 0.24, "kg·m/s", 0.005,
       loi=r"Tính $(m_1+m_2)v$ như va chạm mềm, trong khi hai xe tách nhau và mỗi xe có vận tốc riêng."),
  buoc(r"Động năng trước và sau", r"Tổng động năng của hệ ngay sau va chạm bằng bao nhiêu?", 0.096, "J", 0.002,
       loi=r"Quên bình phương vận tốc, hoặc lấy động năng của tổng vận tốc thay vì cộng động năng từng xe.",
       ke=[(r"Cộng $\tfrac12mv^2$ tính riêng cho từng xe", True),
           (r"Dùng $\tfrac12(m_1+m_2)(v_1'+v_2')^2$", r"Động năng không cộng theo kiểu gộp vận tốc; mỗi xe có $\tfrac12mv^2$ riêng."),
           (r"Cộng các động lượng $mv$ của hai xe", r"Đó là tổng động lượng, đơn vị khác với động năng.")]),
  buoc(r"Phân loại va chạm", r"Kết luận nào đúng về loại va chạm?",
       loi=r"Chỉ kiểm động lượng rồi kết luận, bỏ qua động năng.",
       lua_chon=[(r"Đàn hồi: cả động lượng lẫn động năng đều bảo toàn", True),
                 (r"Mềm: động lượng bảo toàn nhưng động năng giảm", r"Với số liệu đã tính ở hai bước trước, động năng sau va chạm không giảm."),
                 (r"Đàn hồi, vì chỉ cần động lượng bảo toàn là đủ", r"Va chạm mềm cũng bảo toàn động lượng; phải kiểm thêm động năng.")],
       ke=[(r"So tổng động năng trước với sau va chạm", True),
           (r"Kết luận từ việc động lượng được bảo toàn", r"Động lượng bảo toàn trong cả hai loại va chạm nên chưa phân biệt được."),
           (r"Kết luận từ việc hai xe tách nhau sau va chạm", r"Cần số liệu để kiểm; tách nhau chưa chắc là đàn hồi.")]),
  buoc(r"Nếu hai xe dính nhau", r"Nếu hai xe dính nhau, tổng động năng ngay sau va chạm bằng bao nhiêu?", 0.072, "J", 0.002,
       loi=r"Dùng vận tốc sau va chạm của trường hợp tách nhau, hoặc quên khối lượng chung.",
       ke=[(r"Tìm $v$ chung từ động lượng rồi tính động năng cả hệ", True),
           (r"Giữ động năng như câu b) vì hệ vẫn là hệ kín", r"Hệ kín chỉ giữ động lượng; va chạm mềm làm giảm động năng."),
           (r"Tính động năng bằng $\tfrac12m_1v_1'^2$ của câu b)", r"Hai xe dính nhau thì chung vận tốc mới; $v_1'$ của câu b) ứng với trường hợp tách nhau.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>chạy ngược chiều</b> → nghĩ tới <b>chọn chiều dương</b>: vận tốc ngược chiều mang dấu $-$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc(r"Chọn chiều dương và gán dấu", r"Chọn chiều dương theo goòng A. Cặp vận tốc đại số nào đúng?",
       loi=r"Thế mọi tốc độ là số dương dù hai goòng chạy ngược chiều.",
       lua_chon=[(r"$v_A=+2{,}0\ \text{m/s}$ và $v_B=-1{,}0\ \text{m/s}$", True),
                 (r"$v_A=+2{,}0\ \text{m/s}$ và $v_B=+1{,}0\ \text{m/s}$", r"Goòng B chạy ngược chiều dương nên vận tốc của nó mang dấu $-$."),
                 (r"$v_A=-2{,}0\ \text{m/s}$ và $v_B=+1{,}0\ \text{m/s}$", r"Chiều dương đã chọn theo goòng A nên $v_A$ phải dương.")]),
  buoc(r"Tổng động lượng trước va chạm (a)", r"Tổng động lượng của hệ ngay trước va chạm ở câu a) bằng bao nhiêu?", 1200, "kg·m/s", 10,
       loi=r"Cộng hai độ lớn động lượng bất kể chiều.",
       ke=[(r"Cộng động lượng có dấu của cả hai goòng", True),
           (r"Cộng độ lớn động lượng của hai goòng", r"Động lượng là vectơ; hai goòng ngược chiều thì có dấu trái nhau."),
           (r"Chỉ lấy động lượng của goòng nặng hơn", r"Cả hai goòng đều góp động lượng vào tổng.")]),
  buoc(r"Vận tốc chung (a)", r"Vận tốc của hai goòng sau va chạm ở câu a) bằng bao nhiêu? (theo chiều dương đã chọn)", 0.8, "m/s", 0.02,
       loi=r"Chia cho khối lượng một goòng thay vì tổng khối lượng, hoặc đọc sai chiều từ dấu của kết quả.",
       ke=[(r"Chia tổng động lượng cho tổng khối lượng hai goòng", True),
           (r"Chia tổng động lượng cho khối lượng goòng A", r"Sau khi móc dính, cả hai goòng chuyển động cùng nhau với khối lượng chung."),
           (r"Lấy trung bình cộng hai vận tốc ban đầu", r"Vận tốc chung phụ thuộc khối lượng của từng goòng.")]),
  buoc(r"Tốc độ goòng B để hai goòng đứng yên (b)", r"Goòng B phải chạy với tốc độ bao nhiêu để hai goòng đứng yên sau va chạm?", 3.0, "m/s", 0.05,
       loi=r"Thế $v_B$ không mang dấu $-$, hoặc cho tốc độ goòng B bằng tốc độ goòng A.",
       ke=[(r"Cho tổng động lượng trước bằng $0$ rồi rút $u$", True),
           (r"Cho tốc độ goòng B bằng tốc độ goòng A", r"Hai goòng khác khối lượng nên tốc độ bằng nhau chưa cho động lượng bằng nhau."),
           (r"Thế $v_B=+u$ không dấu rồi cho tổng bằng $0$", r"Goòng B ngược chiều dương nên $v_B=-u$; thế dấu $+$ thì hai động lượng không thể triệt tiêu.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>hệ đứng yên rồi tách làm hai phần</b> → nghĩ tới <b>tổng động lượng bằng 0</b>, hai phần đi ngược chiều.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc(r"Đổi đơn vị khối lượng", r"Khối lượng viên đạn tính bằng kg là bao nhiêu?", 0.010, "kg", 0.0005,
       loi=r"Đổi nhầm $1\ \text{g}=0{,}1\ \text{kg}$ hoặc để nguyên gam khi các khối lượng khác tính bằng kilôgam."),
  buoc(r"Súng giật lùi (a)", r"Tốc độ giật lùi của súng bằng bao nhiêu?", 1.6, "m/s", 0.05,
       loi=r"Lấy $V=v$ vì lực giữa súng và đạn bằng nhau, hoặc đảo ngược tỉ số khối lượng.",
       ke=[(r"Cho tổng động lượng sau bằng $0$, rồi rút $V$ ra", True),
           (r"Thế khối lượng đạn là $10$ (gam) vào, không đổi sang kg", r"Khối lượng súng tính bằng kg nên khối lượng đạn cũng phải đổi sang kg; thế gam chưa đổi cho kết quả sai bậc."),
           (r"Rút $V$ theo tỉ số $\dfrac{M}{m}$ nhân với $v$", r"Đảo ngược tỉ số khối lượng: từ $MV=mv$ suy ra $V=\dfrac{m}{M}v$.")]),
  buoc(r"Khối lượng phần tên lửa còn lại (b)", r"Sau khi phụt khí, khối lượng phần tên lửa còn lại bằng bao nhiêu?", 0.5, "kg", 0.01,
       loi=r"Dùng nguyên khối lượng ban đầu của tên lửa, quên rằng một phần đã tách ra.",
       ke=[(r"Lấy khối lượng ban đầu trừ khối lượng khí đã phụt", True),
           (r"Lấy khối lượng của khí làm khối lượng phần còn lại", r"Khí là phần đã tách ra; phần còn lại là tên lửa sau khi khí rời đi."),
           (r"Giữ nguyên khối lượng ban đầu", r"Khối lượng $0{,}60\ \text{kg}$ gồm cả khí; sau khi phụt, phần còn lại không còn khí đó.")]),
  buoc(r"Tốc độ tên lửa (b)", r"Tốc độ của tên lửa ngay sau khi phụt khí bằng bao nhiêu?", 6.0, "m/s", 0.1,
       loi=r"Chia cho khối lượng ban đầu của tên lửa thay vì phần còn lại.",
       ke=[(r"Chia động lượng của khí cho khối lượng phần còn lại", True),
           (r"Chia động lượng của khí cho khối lượng ban đầu", r"Khí đã tách khỏi tên lửa; phần chuyển động ngược lại chỉ là phần còn lại."),
           (r"Cho tốc độ tên lửa bằng tốc độ của khí phụt ra", r"Hai phần có khối lượng khác nhau nên tốc độ khác nhau.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ Tự luận: ví dụ cũ chưa biên tập (gõ lại công thức, giữ đáp số), xếp dễ → khó ═════════════
def TL(k, muc, de, gi):
    return f"<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>{gi}</details>"

_TL = [
 ("Dễ", r"""<p>Một viên đạn khối lượng $35{,}0\ \text{g}$ được bắn theo phương ngang với vận tốc $475\ \text{m/s}$ đến cắm chặt vào một tấm bia gỗ khối lượng $5\ \text{kg}$. Tìm vận tốc của bia ngay sau khi đạn cắm chặt vào gỗ, biết ban đầu:</p>
<ol type="a"><li>bia đứng yên;</li><li>bia chuyển động với tốc độ $0{,}5\ \text{m/s}$ cùng chiều viên đạn;</li><li>bia chuyển động với tốc độ $0{,}5\ \text{m/s}$ ngược chiều viên đạn.</li></ol>""",
  r"""<p>Chọn chiều dương theo chiều viên đạn bay. Va chạm mềm, hệ kín:</p>
$$m_1v_1+m_2v_2=(m_1+m_2)v'\ \Rightarrow\ v'=\dfrac{m_1v_1+m_2v_2}{m_1+m_2}$$
<p>Với $m_1=0{,}035\ \text{kg}$, $v_1=475\ \text{m/s}$, $m_2=5\ \text{kg}$:</p>
<p>a) $v_2=0$: $v'=\dfrac{0{,}035\cdot475}{5{,}035}\approx3{,}3\ \text{m/s}$.</p>
<p>b) $v_2=+0{,}5\ \text{m/s}$: $v'=\dfrac{0{,}035\cdot475+5\cdot0{,}5}{5{,}035}\approx3{,}8\ \text{m/s}$.</p>
<p>c) $v_2=-0{,}5\ \text{m/s}$: $v'=\dfrac{0{,}035\cdot475-5\cdot0{,}5}{5{,}035}\approx2{,}8\ \text{m/s}$.</p>"""),
 ("Dễ", r"""<p>Quả cầu 1 chuyển động trên mặt phẳng ngang với vận tốc không đổi $3{,}0\ \text{m/s}$ đến đập trực diện vào quả cầu 2 đang đứng yên. Sau va chạm, hai quả cầu có các vận tốc ngược hướng nhau và cùng độ lớn. Biết khối lượng quả cầu 2 gấp ba lần khối lượng quả cầu 1. Tính tốc độ của mỗi quả cầu sau va chạm.</p>""",
  r"""<p>Chọn chiều dương theo chiều chuyển động ban đầu của quả cầu 1. Theo đề: $m_2=3m_1$, $v_2=0$, $v_1'=-v$, $v_2'=+v$ (cùng độ lớn $v$).</p>
$$m_1v_1=m_1v_1'+m_2v_2'\ \Rightarrow\ m_1\cdot3{,}0=-m_1v+3m_1v$$
$$3{,}0=2v\ \Rightarrow\ v=1{,}5\ \text{m/s}$$
<p>Vậy $v_1'=-1{,}5\ \text{m/s}$ (bật ngược lại) và $v_2'=+1{,}5\ \text{m/s}$.</p>"""),
 ("Trung bình", r"""<p>Một xe chở cát khối lượng $38\ \text{kg}$ đang chạy trên đường nằm ngang không ma sát với vận tốc $1\ \text{m/s}$. Một vật nhỏ khối lượng $2\ \text{kg}$ bay theo phương chuyển động của xe với vận tốc $7\ \text{m/s}$ (đối với mặt đất), đến chui vào cát và nằm yên trong đó. Xác định vận tốc mới của xe trong hai trường hợp:</p>
<ol type="a"><li>vật bay đến ngược chiều xe chạy;</li><li>vật bay đến cùng chiều xe chạy.</li></ol>""",
  r"""<p>Chọn chiều dương cùng chiều chuyển động của xe. Va chạm mềm, hệ kín theo phương ngang:</p>
$$m_1v_1+m_2v_2=(m_1+m_2)v\ \Rightarrow\ v=\dfrac{m_1v_1+m_2v_2}{m_1+m_2}$$
<p>a) Vật ngược chiều ($v_2=-7\ \text{m/s}$): $v=\dfrac{38\cdot1-2\cdot7}{40}=0{,}6\ \text{m/s}$.</p>
<p>b) Vật cùng chiều ($v_2=+7\ \text{m/s}$): $v=\dfrac{38\cdot1+2\cdot7}{40}=1{,}3\ \text{m/s}$.</p>"""),
 ("Trung bình", r"""<p>Một xe chở cát khối lượng $m_1=390\ \text{kg}$ chuyển động theo phương ngang với tốc độ $v_1=8\ \text{m/s}$ thì có một hòn đá khối lượng $m_2=10\ \text{kg}$ bay đến cắm vào cát. Tìm tốc độ của xe sau khi hòn đá rơi vào xe trong hai trường hợp:</p>
<ol type="a"><li>hòn đá bay ngang, ngược chiều chuyển động của xe với tốc độ $v_2=12\ \text{m/s}$;</li><li>hòn đá rơi thẳng đứng.</li></ol>""",
  r"""<p>Chọn chiều dương theo chiều chuyển động ban đầu của xe. Khi đá cắm vào cát, ngoại lực (trọng lực, phản lực) đều thẳng đứng và cân bằng nhau nên theo phương ngang hệ là hệ kín.</p>
$$m_1v_1+m_2v_2=(m_1+m_2)v$$
<p>a) $v_2=-12\ \text{m/s}$: $v=\dfrac{390\cdot8-10\cdot12}{400}=7{,}5\ \text{m/s}$.</p>
<p>b) Đá rơi thẳng đứng nên theo phương ngang $v_2=0$: $v=\dfrac{390\cdot8}{400}=7{,}8\ \text{m/s}$.</p>"""),
 ("Trung bình", r"""<p>Hai quả cầu 1 và 2 chuyển động trên cùng một đường thẳng, hướng trực diện vào nhau. Ngay trước va chạm, tốc độ hai quả cầu lần lượt là $3{,}0\ \text{m/s}$ và $1{,}0\ \text{m/s}$. Ngay sau va chạm, cả hai bị bật ngược trở lại với các tốc độ lần lượt $1{,}8\ \text{m/s}$ và $2{,}2\ \text{m/s}$. Biết quả cầu 1 có khối lượng $m_1=200\ \text{g}$. Tính khối lượng của quả cầu 2.</p>""",
  r"""<p>Chọn chiều dương theo chiều chuyển động ban đầu của quả cầu 1: $v_1=+3{,}0$, $v_2=-1{,}0$, $v_1'=-1{,}8$, $v_2'=+2{,}2$ (m/s).</p>
$$m_1v_1+m_2v_2=m_1v_1'+m_2v_2'$$
$$0{,}2\cdot3{,}0+m_2\cdot(-1{,}0)=0{,}2\cdot(-1{,}8)+m_2\cdot2{,}2$$
$$0{,}96=3{,}2\,m_2\ \Rightarrow\ m_2=0{,}3\ \text{kg}$$"""),
 ("Trung bình", r"""<p>Bắn một hòn bi thép với vận tốc $4\ \text{m/s}$ vào một hòn bi ve đang chuyển động ngược chiều với vận tốc $1\ \text{m/s}$, biết khối lượng bi thép gấp $5$ lần bi ve. Sau va chạm, hai hòn bi cùng chuyển động về phía trước, nhưng bi ve có vận tốc gấp $5$ lần bi thép. Xác định vận tốc của bi thép và bi ve sau va chạm.</p>""",
  r"""<p>Gọi $m$ là khối lượng bi ve, bi thép có khối lượng $5m$. Chọn chiều dương theo chiều chuyển động của bi thép trước va chạm: $v_1=+4$, $v_2=-1$ (m/s); sau va chạm $v_2'=5v_1'$.</p>
$$m_1v_1+m_2v_2=m_1v_1'+m_2v_2'$$
$$5m\cdot4+m\cdot(-1)=5m\,v_1'+m\cdot5v_1'$$
$$19=10v_1'\ \Rightarrow\ v_1'=1{,}9\ \text{m/s},\quad v_2'=5\cdot1{,}9=9{,}5\ \text{m/s}$$"""),
 ("Trung bình", r"""<p>Một quả lựu đạn đang bay theo phương ngang với vận tốc $10\ \text{m/s}$ thì nổ và tách thành hai mảnh có trọng lượng $10\ \text{N}$ và $15\ \text{N}$. Sau khi nổ, mảnh to vẫn chuyển động theo phương ngang với vận tốc $25\ \text{m/s}$ cùng chiều chuyển động ban đầu. Lấy $g\approx10\ \text{m/s}^2$. Xác định vận tốc và phương chuyển động của mảnh nhỏ.</p>""",
  r"""<p>Khi nổ, nội lực rất lớn, ngoại lực bỏ qua được nên hệ hai mảnh coi là kín. Khối lượng hai mảnh: $m_1=1{,}0\ \text{kg}$ (mảnh nhỏ), $m_2=1{,}5\ \text{kg}$ (mảnh to).</p>
<p>Chọn chiều dương theo chiều chuyển động của quả lựu đạn lúc đầu:</p>
$$(m_1+m_2)v_0=m_1v_1+m_2v_2$$
$$v_1=\dfrac{(m_1+m_2)v_0-m_2v_2}{m_1}=\dfrac{2{,}5\cdot10-1{,}5\cdot25}{1{,}0}=-12{,}5\ \text{m/s}$$
<p>Dấu $-$: mảnh nhỏ bay ngược hướng với vận tốc ban đầu của quả lựu đạn, tốc độ $12{,}5\ \text{m/s}$.</p>"""),
 ("Khó", r"""<p>Một bệ pháo khối lượng $1500\ \text{kg}$ bắn một viên đạn khối lượng $5\ \text{kg}$ với vận tốc khi ra khỏi nòng là $600\ \text{m/s}$. Tính vận tốc giật lùi của bệ pháo trong hai trường hợp:</p>
<ol type="a"><li>đạn được bắn theo phương ngang;</li><li>đạn được bắn theo phương hợp với phương ngang một góc $60^\circ$.</li></ol>""",
  r"""<p>Hệ ban đầu đứng yên nên tổng động lượng trước bằng $0$. Gọi $M$ là khối lượng bệ pháo, $m$ khối lượng đạn.</p>
<p>a) Chọn chiều dương theo chiều đạn bay: $mv-MV=0$, suy ra $V=\dfrac{mv}{M}=\dfrac{5\cdot600}{1500}=2\ \text{m/s}$.</p>
<p>b) Bắn xiên: trọng lực và phản lực mặt đất đều thẳng đứng (không cân bằng trong lúc bắn) nên chỉ bảo toàn động lượng theo phương ngang. Thành phần ngang vận tốc đạn là $v\cos60^\circ$:</p>
$$mv\cos60^\circ-MV=0\ \Rightarrow\ V=\dfrac{mv\cos60^\circ}{M}=\dfrac{5\cdot600\cdot0{,}5}{1500}=1\ \text{m/s}$$"""),
 ("Khó", r"""<p>Con lắc đạn đạo là thiết bị dùng để đo tốc độ của viên đạn: viên đạn được bắn vào một khúc gỗ lớn treo bằng dây nhẹ, không dãn; sau va chạm viên đạn ghim vào khối gỗ, rồi cả hệ chuyển động như một con lắc lên độ cao cực đại $h$. Xét viên đạn khối lượng $m_1=5\ \text{g}$, khối gỗ khối lượng $m_2=1\ \text{kg}$ và $h=5\ \text{cm}$. Lấy $g=9{,}8\ \text{m/s}^2$, bỏ qua sức cản của không khí.</p>
<ol type="a"><li>Tính vận tốc của hệ ngay sau khi viên đạn ghim vào khối gỗ.</li><li>Tính tốc độ ban đầu của viên đạn.</li></ol>""",
  r"""<p>a) Chọn gốc thế năng tại vị trí thấp nhất. Từ ngay sau va chạm đến độ cao cực đại, cơ năng bảo toàn:</p>
$$\tfrac12(m_1+m_2)v^2=(m_1+m_2)gh\ \Rightarrow\ v=\sqrt{2gh}=\sqrt{2\cdot9{,}8\cdot0{,}05}\approx0{,}99\ \text{m/s}$$
<p>b) Ngay trước và ngay sau va chạm (rất ngắn), động lượng bảo toàn:</p>
$$m_1v_0=(m_1+m_2)v\ \Rightarrow\ v_0=\dfrac{(m_1+m_2)v}{m_1}=\dfrac{1{,}005\cdot0{,}98995}{0{,}005}\approx199\ \text{m/s}$$""")]
TU_LUAN = dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
               body_html="<p>Các bài còn lại của bài học, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>"
               + "".join(TL(k, m, d, g) for k, (m, d, g) in enumerate(_TL, 1)))

write(J, 74, "Bài 29. Định luật bảo toàn động lượng", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
for q, f in zip(d["dang_bai"], FORMS):
    q["form"] = f
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
