"""Bài tập mẫu Bài 19 "Thế năng điện" (Vật lí 11) — lesson_id 38. 4 dạng. Hình: hinh_38.py.
Bài chưa có chủ đề riêng trong question-topics.json: dùng tên YCCĐ con của bài 39 (183 "Công của lực điện và thế năng điện";
184 "Điện thế, hiệu điện thế và liên hệ U = Ed" không dùng vì lý thuyết bài chỉ nối sang điện thế ở mục 6).
Quét dạng (lý thuyết lt-38 + ngân hàng chủ đề 183/51: câu tính công A = qEd, thế năng W = qEd có mốc, điện thế từ thế năng):
  1 (cấp 1) A = qEd: hình chiếu có dấu của MN, dấu của q, đổi chiều đi · 2 (cấp 2) công không phụ thuộc đường đi, vòng kín
  3 (cấp 3) thế năng W = qEd có mốc, A = W_M − W_N, đổi mốc · 4 (cấp 4) từ nghỉ chỉ có lực điện: A = ½mv², bài ngược tìm E.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-38.py   (idempotent, ghi 38.json với review.checked=false)"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_38 import *

J = os.path.join(HERE, "38.json")
ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
TOPICS = {t["id"]: t["name"] for t in json.load(open(os.path.join(ROOT, "scripts/data/question-topics.json")))}
T183 = TOPICS[183]
e = 1.6e-19


def near(x, y, tol): return abs(x - y) <= tol


# ═════════════ SỐ LIỆU + TỰ GIẢI ĐỘC LẬP (assert) ═════════════
# Dạng 1: electron, E = 5000 V/m (sang phải = +x), MN = 8,0 cm hợp chiều E góc 120°. Tích vô hướng F·Δr.
q1, E1, MN1 = -e, 5000.0, 0.080
dx = MN1 * math.cos(math.radians(120)); dy = MN1 * math.sin(math.radians(120))
A1 = (q1 * E1) * dx                                         # F = qE theo +x
assert near(dx, -0.040, 1e-12) and near(A1, 3.2e-17, 1e-22) and near(-A1, (q1 * E1) * (-dx), 1e-22)
assert q1 * E1 * (MN1 * math.sin(math.radians(120))) != A1 and near(q1 * E1 * MN1, -6.4e-17, 1e-22)   # cách sai: sin, cả MN
assert near(abs(q1) * E1 * abs(dx), 3.2e-17, 1e-22) and (-3.2e-17) != A1                                 # sai: bỏ dấu q hoặc d → ra −3,2e−17
# Dạng 2: q = −2,0 µC, E = 3000 V/m, AB = 6,0 cm dọc E, BC = 10 cm hợp E góc 60°, đường cong A→C dài 25 cm
q2, E2 = -2.0e-6, 3000.0
ptA = (0.0, 0.0); ptB = (0.06, 0.0); ptC = (0.06 + 0.10 * math.cos(math.radians(60)), 0.10 * math.sin(math.radians(60)))
A_AB = q2 * E2 * (ptB[0] - ptA[0]); A_BC = q2 * E2 * (ptC[0] - ptB[0]); A_ABC = A_AB + A_BC
assert near(A_AB, -3.6e-4, 1e-10) and near(A_BC, -3.0e-4, 1e-10) and near(A_ABC, -6.6e-4, 1e-10)
# đường cong lượn bất kì từ A tới C: cộng qE·Δx từng đoạn nhỏ (độ dài đường đi ≠ 25 cm là không cần; kiểm công theo điểm đầu, cuối)
n = 4000; Acurve = 0.0; prev = ptA
for i in range(1, n + 1):
    u = i / n
    cur = (ptC[0] * u + 0.03 * math.sin(2 * math.pi * u), ptC[1] * u + 0.04 * math.sin(math.pi * u))
    Acurve += q2 * E2 * (cur[0] - prev[0]); prev = cur
assert near(Acurve, A_ABC, 1e-9)
assert near(Acurve + q2 * E2 * (ptA[0] - ptC[0]), 0.0, 1e-9)                                            # vòng kín
assert near(q2 * E2 * 0.25, -1.5e-3, 1e-10)                                                             # sai: nhân quãng đường 25 cm
assert near(q2 * E2 * 0.10, -6.0e-4, 1e-10) and near(q2 * E2 * 0.10 * math.sin(math.radians(60)), -5.196e-4, 1e-7)   # sai: cả BC / sin60
assert near(-A_ABC, 6.6e-4, 1e-10) and near(A_AB, -3.6e-4, 1e-10)                                        # sai: bỏ dấu; bỏ BC
# Dạng 3 (cho W_M và A_MN, tìm E, W_N, vị trí N, đổi mốc): q = −5,0 nC, bản trên âm (E hướng LÊN), bản trên y=0, bản dưới y=−5 cm, M y=−1 cm.
q3 = -5.0e-9
def W(y, y_ref, E): return q3 * E * (y_ref - y)                                                         # W = công từ y tới mốc: qE·(y_mốc − y) (E hướng +y)
yTop, yBot, yM = 0.0, -0.05, -0.01
WM_given, A_given = -2.0e-7, 6.0e-7
E3 = WM_given / (q3 * (yTop - yM))
assert near(E3, 4000.0, 1e-6)
WN = WM_given - A_given
yN = yTop - WN / (q3 * E3)
assert near(WN, -8.0e-7, 1e-13) and near(yN, -0.04, 1e-9)
assert near(q3 * E3 * (yN - yM), A_given, 1e-13)                                                       # công trực tiếp F·Δy khớp
WN2, WM2 = W(yN, yBot, E3), W(yM, yBot, E3)
assert near(WN2, 2.0e-7, 1e-13) and near(WM2, 8.0e-7, 1e-13) and near(WM2 - WN2, A_given, 1e-13)
assert near(A_given / abs(q3 * E3), 0.03, 1e-12) and near(abs(WN2 - 0), 2.0e-7, 1e-13) and WN2 != WN   # sai: d_N = A/(qE) = 3 cm; giữ nguyên W_N
assert near(WM_given + A_given, 4.0e-7, 1e-13) and 4.0e-7 != WN                                        # sai: cộng công vào W_M
# Dạng 4: hạt bụi q = +4,0 nC, m = 2,0e-8 kg, từ nghỉ ở M cách bản âm 5,0 cm, tới bản âm v = 10 m/s. Tích phân số.
q4, m4, v4, d4v, dP = 4.0e-9, 2.0e-8, 10.0, 0.050, 0.020
A4 = 0.5 * m4 * v4 ** 2; E4 = A4 / (q4 * d4v)
assert near(A4, 1.0e-6, 1e-12) and near(E4, 5000.0, 1e-6)
a4 = q4 * E4 / m4; x = v = t = 0.0; dt = 1e-6; vP = None
while x < d4v:
    v += a4 * dt; x += v * dt; t += dt
    if vP is None and x >= d4v - dP: vP = v
assert near(v, 10.0, 0.01) and near(vP, math.sqrt(60), 0.01)
A4P = q4 * E4 * (d4v - dP)
assert near(A4P, 6.0e-7, 1e-12) and near(math.sqrt(2 * A4P / m4), 7.746, 1e-3)
WP = q4 * E4 * dP
assert near(WP, 4.0e-7, 1e-12) and near(A4 - WP, A4P, 1e-12)                                            # thế năng giảm = động năng tăng
assert math.sqrt(2 * q4 * E4 * dP / m4) != math.sqrt(60) and near(math.sqrt(2 * q4 * E4 * dP / m4), math.sqrt(40), 1e-9)  # sai: d = 2 cm
assert near(10.0 * (0.03 / 0.05), 6.0, 1e-12) and 6.0 != round(math.sqrt(60), 1)                          # sai: v tỉ lệ quãng đường
assert near(A4 / q4, 250.0, 1e-6) and 250.0 != E4 and near(m4 * v4 ** 2, 2.0e-6, 1e-12)                                                                # sai: thiếu ½

# ═════════════ ĐỀ ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Công của lực điện A = qEd: hình chiếu có dấu của đoạn đi và dấu của điện tích", topic=T183,
      problem_html=r"""<p>Điện trường đều có cường độ $E=5000\ \text{V/m}$, đường sức nằm ngang hướng sang phải. Một electron ($q=-1{,}6\cdot10^{-19}\ \text{C}$) đi thẳng từ điểm M đến điểm N, đoạn $MN=8{,}0\ \text{cm}$ hợp với chiều đường sức góc $120^\circ$ (từ M, MN hướng lên trên và chếch sang trái). Chỉ xét lực điện.</p><ol type="a"><li>Tìm độ dài đại số $d$ của hình chiếu MN lên đường sức.</li><li>Tính công $A_{MN}$ của lực điện.</li><li>Electron quay lại, đi thẳng từ N về M. Công $A_{NM}$ so với $A_{MN}$ thế nào?</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Công không phụ thuộc đường đi: đường gấp khúc, đường cong, vòng kín", topic=T183,
      problem_html=r"""<p>Điện trường đều $E=3000\ \text{V/m}$, đường sức nằm ngang hướng từ A sang B. Một hạt mang điện $q=-2{,}0\ \mu\text{C}$ đi từ A đến B theo đoạn thẳng $AB=6{,}0\ \text{cm}$ dọc đường sức, rồi từ B đến C theo đoạn thẳng $BC=10\ \text{cm}$ hợp với chiều đường sức góc $60^\circ$. Chỉ xét lực điện.</p><ol type="a"><li>Tính công của lực điện trên đường A → B → C.</li><li>Cũng hạt đó đi từ A tới điểm D theo một đường cong dài $25\ \text{cm}$. D nằm ngay dưới C, đoạn $CD=4{,}0\ \text{cm}$ vuông góc với đường sức. Tính công của lực điện.</li><li>Hạt đi hết đường A → B → C rồi trở về A theo đoạn thẳng CA. Tính công của lực điện trên cả vòng.</li></ol>"""),
dict(label="Dạng 3 · Trung bình · Thế năng điện có mốc: từ W_M và công tìm E, vị trí N, rồi đổi mốc", topic=T183,
      problem_html=r"""<p>Hai bản kim loại phẳng nằm ngang, song song, cách nhau $5{,}0\ \text{cm}$; bản trên tích điện âm, bản dưới tích điện dương; điện trường giữa hai bản là đều. Một hạt bụi mang điện $q=-5{,}0\ \text{nC}$. Chọn mốc thế năng ở bản trên. Tại điểm M cách bản trên $1{,}0\ \text{cm}$, thế năng của hạt là $W_M=-2{,}0\cdot10^{-7}\ \text{J}$. Hạt đi (theo một đường bất kì) từ M tới điểm N nằm dưới M; lực điện sinh công $A_{MN}=+6{,}0\cdot10^{-7}\ \text{J}$. Bỏ qua trọng lực.</p><ol type="a"><li>Tính cường độ điện trường giữa hai bản.</li><li>Tính thế năng $W_N$ của hạt tại N.</li><li>Tính khoảng cách từ N tới bản trên.</li><li>Đổi mốc sang bản dưới (bản dương). Tính thế năng của hạt tại N với mốc mới.</li></ol>"""),
 dict(label="Dạng 4 · Khó · Từ nghỉ, chỉ có lực điện: công = độ tăng động năng, bài ngược tìm cường độ điện trường", topic=T183,
      problem_html=r"""<p>Một hạt bụi mang điện $q=+4{,}0\ \text{nC}$, khối lượng $m=2{,}0\cdot10^{-8}\ \text{kg}$, được thả từ trạng thái nghỉ tại điểm M trong điện trường đều giữa hai bản kim loại phẳng song song nằm ngang (bản trên dương, bản dưới âm). M cách bản âm $5{,}0\ \text{cm}$. Hạt đi thẳng xuống theo đường sức và tới bản âm với tốc độ $10\ \text{m/s}$. Chỉ có lực điện tác dụng lên hạt.</p><ol type="a"><li>Tính công của lực điện từ M tới bản âm.</li><li>Tính cường độ điện trường giữa hai bản.</li><li>Tính tốc độ của hạt khi nó đi qua điểm P, cách bản âm $2{,}0\ \text{cm}$.</li></ol>"""),
]

# ═════════════ PHÂN TÍCH ĐỀ (cột 3: khái niệm / điều kiện chung, không ghi kết luận hay hướng giải) ═════════════
ANALYSIS = [
 [(r'"điện trường đều có cường độ $E=5000$ V/m, đường sức nằm ngang hướng sang phải"', r"$E=5000$ V/m; $\vec E$ sang phải", "⚠ Công thức $A=qEd$ chỉ dùng cho điện trường đều; chỉ xét lực điện"),
  (r'"electron ($q=-1{,}6\cdot10^{-19}$ C)"', r"$q=-1{,}6\cdot10^{-19}$ C", "Lấy cả dấu của $q$ vào công thức"),
  (r'"đoạn $MN=8{,}0$ cm hợp với chiều đường sức góc $120^\circ$"', r"$MN=8{,}0$ cm; góc giữa MN và $\vec E$ là $120^\circ$", "$d$ là hình chiếu có dấu của MN lên đường sức, không phải độ dài đường đi. Góc tù thì dấu của $d$ thế nào?"),
  (r'"tìm độ dài đại số $d$ của hình chiếu"', r"Cần $d$", "Đại lượng cần tìm: chiếu MN lên đường sức"),
  (r'"tính công $A_{MN}$"', r"Cần $A_{MN}$", "Công của lực điện trong điện trường đều"),
  (r'"quay lại, đi thẳng từ N về M … so với $A_{MN}$"', r"Cần so sánh $A_{NM}$ với $A_{MN}$", "Đổi chiều đi thì hình chiếu có dấu đổi thế nào?")],
 [(r'"điện trường đều $E=3000$ V/m, đường sức từ A sang B"', r"$E=3000$ V/m; $\vec E$ từ A sang B", "⚠ Điện trường đều; chỉ xét lực điện"),
  (r'"hạt mang điện $q=-2{,}0\ \mu$C"', r"$q=-2{,}0\ \mu\text{C}=-2{,}0\cdot10^{-6}$ C", "Lấy cả dấu của $q$; đổi $\mu$C ra C"),
  (r'"$AB=6{,}0$ cm dọc đường sức"', r"$AB=6{,}0$ cm, cùng chiều $\vec E$", "Hình chiếu có dấu của đoạn dọc đường sức"),
  (r'"$BC=10$ cm hợp với chiều đường sức góc $60^\circ$"', r"$BC=10$ cm; góc với $\vec E$: $60^\circ$", "Chiếu BC lên đường sức; độ dài BC chưa phải $d$"),
  (r'"từ A tới D theo đường cong dài 25 cm … $CD=4{,}0$ cm vuông góc với đường sức"', r"Đường dài 25 cm; $CD=4{,}0$ cm, $CD\perp\vec E$", "Công của lực điện có phụ thuộc hình dạng và độ dài đường đi không? Hình chiếu của AD lên đường sức so với của AC?"),
  (r'"trở về A theo CA … cả vòng"', "Điểm đầu và điểm cuối của cả vòng", "Cả vòng đi qua những điểm nào? Điểm đầu và điểm cuối có gì đặc biệt?"),
  (r'"công trên A → B → C … đường cong … cả vòng"', r"Cần $A_{ABC}$, $A_{AD}$ (đường cong), $A_{\text{vòng}}$", "Đại lượng cần tìm")],
 [(r'"hai bản … cách nhau 5,0 cm; bản trên âm, bản dưới dương; điện trường đều"', r"Bản trên $-$; $\vec E$ hướng lên", "⚠ Điện trường đều giữa hai bản; mốc ở bản nào thì $d$ tính tới bản đó"),
  (r'"hạt bụi $q=-5{,}0$ nC"', r"$q=-5{,}0\cdot10^{-9}$ C", "Lấy cả dấu của $q$"),
  (r'"chọn mốc thế năng ở bản trên … M cách bản trên 1,0 cm … $W_M=-2{,}0\cdot10^{-7}$ J"', r"M cách bản trên 1,0 cm; $W_M=-2{,}0\cdot10^{-7}$ J", "Thế năng bằng công của lực điện từ điểm đó tới mốc. Từ M về mốc là xuôi hay ngược chiều $\\vec E$? Dấu của $d$?"),
  (r'"đi từ M tới N nằm dưới M; $A_{MN}=+6{,}0\cdot10^{-7}$ J"', r"$A_{MN}=+6{,}0\cdot10^{-7}$ J", "Công và độ biến thiên thế năng liên hệ thế nào?"),
  (r'"bỏ qua trọng lực"', "Chỉ có lực điện", "⚠ Chỉ xét lực điện"),
  (r'"cường độ điện trường … thế năng $W_N$ … khoảng cách từ N tới bản trên"', r"Cần $E$, $W_N$, $d_N$", "Đại lượng cần tìm: $W=qEd$ với $d$ tính tới mốc"),
  (r'"đổi mốc sang bản dưới … thế năng tại N với mốc mới"', "Mốc mới ở bản dưới; cần $W'_N$", "Từ N xuống mốc mới là xuôi hay ngược chiều $\\vec E$? Khoảng cách tới bản dưới là bao nhiêu?")],
 [(r'"hạt bụi $q=+4{,}0$ nC, $m=2{,}0\cdot10^{-8}$ kg, thả từ trạng thái nghỉ tại M"', r"$q=+4{,}0\cdot10^{-9}$ C; $m=2{,}0\cdot10^{-8}$ kg; $v_M=0$", "Động năng ban đầu của hạt"),
  (r'"bản trên dương, bản dưới âm; M cách bản âm 5,0 cm"', r"M cách bản âm 5,0 cm; đường sức đi xuống", "Chiều lực lên $q\gt0$; hạt đi dọc đường sức"),
  (r'"đi thẳng xuống theo đường sức, tới bản âm với tốc độ 10 m/s"', r"$v=10$ m/s tại bản âm", "Quan hệ giữa công và động năng"),
  (r'"chỉ có lực điện tác dụng"', "Không còn lực nào khác", "⚠ Chỉ có lực điện tác dụng"),
  (r'"công của lực điện từ M tới bản âm"', r"Cần $A$", "Đại lượng cần tìm"),
  (r'"cường độ điện trường"', r"Cần $E$", "Công và hình chiếu của đoạn đi lên đường sức"),
  (r'"tốc độ khi đi qua P, cách bản âm 2,0 cm"', r"Cần $v_P$", "Đoạn từ M tới P có hình chiếu bao nhiêu? Từ nghỉ nên công bằng gì?")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = ["<strong>Khái niệm:</strong> điện trường đều: lực $\\vec F=q\\vec E$ không đổi; công phụ thuộc hình chiếu của đoạn đi lên đường sức.",
      r"Công: $A_{MN}=qEd$ · $d$ = hình chiếu có dấu của MN lên chiều đường sức · $d=MN\cos\alpha$ ($\alpha$: góc giữa MN và chiều $\vec E$)",
      "$q$ lấy cả dấu; $d\\gt0$ nếu hình chiếu cùng chiều đường sức, $d\\lt0$ nếu ngược chiều.",
      "⚠ <strong>Điều kiện:</strong> điện trường đều; chỉ xét lực điện; đổi cm ra m."]
R2 = ["<strong>Khái niệm:</strong> công của lực điện chỉ phụ thuộc điểm đầu và điểm cuối, không phụ thuộc đường đi (lực thế); đi một vòng kín thì $A=0$.",
      r"Mỗi đoạn: $A=qEd$ với $d$ là hình chiếu có dấu lên đường sức · công cả đường = tổng công các đoạn",
      "⚠ <strong>Điều kiện:</strong> điện trường đều; chỉ xét lực điện; $q$ lấy cả dấu, đổi $\\mu$C ra C."]
R3 = ["<strong>Khái niệm:</strong> thế năng điện tại M = công của lực điện khi $q$ đi từ M tới mốc; phải chọn mốc.",
      r"Điện trường đều: $W_M=qEd$, $d$ = hình chiếu có dấu của đoạn từ M tới mốc lên đường sức",
      r"Công và thế năng: $A_{MN}=W_M-W_N$; công dương thì thế năng giảm",
      "⚠ <strong>Điều kiện:</strong> điện trường đều; chỉ xét lực điện. Đổi mốc thì từng $W$ đổi, hiệu $W_M-W_N$ không đổi."]
R4 = ["<strong>Khái niệm:</strong> chỉ có lực điện: thế năng giảm bao nhiêu, động năng tăng bấy nhiêu; từ nghỉ nên công = động năng cuối.",
      r"Công: $A=qEd$ ($d$ hình chiếu của đoạn đi) · $A=\tfrac12mv^2$ khi từ nghỉ",
      "⚠ <strong>Điều kiện:</strong> điện trường đều; không có lực nào khác (bỏ qua trọng lực)."]

SOLS = [
 sol(R1, [
  ("Hình chiếu có dấu của MN", [P("Góc giữa MN và chiều đường sức là $120^\\circ$."), M(r"d=MN\cos120^\circ=0{,}080\cdot(-0{,}5)"), A(r"d=-0{,}040\ \text{m}=-4{,}0\ \text{cm}"), P("$d\\lt0$: hình chiếu ngược chiều đường sức.")]),
  ("Công của lực điện", [M(r"A_{MN}=qEd"), M(r"A_{MN}=(-1{,}6\cdot10^{-19})\cdot5000\cdot(-0{,}040)"), A(r"A_{MN}=+3{,}2\cdot10^{-17}\ \text{J}"), P("Hai dấu âm nhân nhau cho công dương: lực điện lên electron ngược chiều $\\vec E$, tức hướng sang trái, cùng phía với thành phần chuyển động sang trái của MN.")]),
  ("Đi ngược từ N về M", [P("Đổi chiều đi thì hình chiếu có dấu đổi dấu: $d'=+0{,}040$ m."), M(r"A_{NM}=(-1{,}6\cdot10^{-19})\cdot5000\cdot0{,}040=-3{,}2\cdot10^{-17}\ \text{J}"), A("T:$A_{NM}=-A_{MN}$: cùng độ lớn, trái dấu.")]),
  ("Kiểm tra", [P(r"Đơn vị: $\text{C}\cdot\text{V/m}\cdot\text{m}=\text{C}\cdot\text{V}=\text{J}$ ✓"), P("$A_{MN}+A_{NM}=0$: đi một vòng kín về chỗ cũ thì công bằng 0 ✓")])],
  [r"a) $d=-4{,}0\ \text{cm}$", r"b) $A_{MN}=+3{,}2\cdot10^{-17}\ \text{J}$", r"c) $A_{NM}=-A_{MN}=-3{,}2\cdot10^{-17}\ \text{J}$"],
  "Nhận dạng: đề cho <strong>đoạn đi hợp với đường sức một góc</strong> → $d=MN\\cos\\alpha$ có dấu, rồi $A=qEd$ với $q$ có dấu."),
 sol(R2, [
  ("Công trên đoạn AB", [P(r"Đổi $q=-2{,}0\cdot10^{-6}\ \text{C}$. AB dọc đường sức, cùng chiều $\vec E$: $d_{AB}=+0{,}060\ \text{m}$."), M(r"A_{AB}=qEd_{AB}=(-2{,}0\cdot10^{-6})\cdot3000\cdot0{,}060"), A(r"A_{AB}=-3{,}6\cdot10^{-4}\ \text{J}=-0{,}36\ \text{mJ}")]),
  ("Công trên cả đường A → B → C", [P(r"Hình chiếu của BC lên đường sức: $d_{BC}=BC\cos60^\circ=0{,}10\cdot0{,}5=0{,}050\ \text{m}$."), M(r"A_{BC}=(-2{,}0\cdot10^{-6})\cdot3000\cdot0{,}050=-3{,}0\cdot10^{-4}\ \text{J}"), M(r"A_{ABC}=A_{AB}+A_{BC}=-3{,}6\cdot10^{-4}-3{,}0\cdot10^{-4}"), A(r"A_{ABC}=-6{,}6\cdot10^{-4}\ \text{J}=-0{,}66\ \text{mJ}")]),
  ("Công trên đường cong từ A tới D", [P("Công của lực điện chỉ phụ thuộc điểm đầu A và điểm cuối D, không phụ thuộc hình dạng hay độ dài đường đi."), P(r"CD vuông góc đường sức nên D và C có cùng hình chiếu lên đường sức: $d_{AD}=d_{AC}=d_{AB}+d_{BC}=0{,}060+0{,}050=0{,}110\ \text{m}$."), M(r"A_{AD}=qEd_{AD}=(-2{,}0\cdot10^{-6})\cdot3000\cdot0{,}110"), A(r"A_{AD}=-6{,}6\cdot10^{-4}\ \text{J}=-0{,}66\ \text{mJ}"), P("Bằng công trên đường gấp khúc A → B → C ✓.")]),
  ("Công trên cả vòng kín", [P("Cả vòng A → B → C → A có điểm cuối trùng điểm đầu: hình chiếu tổng cộng của cả vòng bằng 0."), M(r"A_{\text{vòng}}=A_{ABC}+A_{CA}=-6{,}6\cdot10^{-4}+6{,}6\cdot10^{-4}"), A(r"A_{\text{vòng}}=0")]),
  ("Kiểm tra", [P("Đường cong dài 25 cm nhưng độ dài không đi vào công thức; nếu nhân $qE$ với 0,25 m sẽ ra công khác (sai), vì lực điện không phải lực ma sát."), P(r"Đơn vị: $\text{C}\cdot\text{V/m}\cdot\text{m}=\text{J}$ ✓")])],
  [r"a) $A_{ABC}=-0{,}66\ \text{mJ}$", r"b) $A_{AD}=-0{,}66\ \text{mJ}$ (đường cong dài 25 cm cho cùng kết quả)", "c) $A_{\\text{vòng}}=0$"],
  "Nhận dạng: đề cho <strong>nhiều đường đi cùng điểm đầu, điểm cuối</strong> (hoặc vòng kín) → công như nhau; chỉ tính một lần theo hình chiếu của đoạn nối hai đầu."),
 sol(R3, [
  ("Cường độ điện trường", [P("Bản trên âm, bản dưới dương nên $\\vec E$ hướng từ dưới lên trên."), P("Từ M lên mốc (bản trên) là xuôi chiều $\\vec E$: $d_M=+0{,}010\\ \\text{m}$."), M(r"W_M=qEd_M\Rightarrow E=\dfrac{W_M}{qd_M}=\dfrac{-2{,}0\cdot10^{-7}}{(-5{,}0\cdot10^{-9})\cdot0{,}010}"), A(r"E=4000\ \text{V/m}")]),
  ("Thế năng tại N", [P("Công bằng độ giảm thế năng: $A_{MN}=W_M-W_N$."), M(r"W_N=W_M-A_{MN}=-2{,}0\cdot10^{-7}-6{,}0\cdot10^{-7}"), A(r"W_N=-8{,}0\cdot10^{-7}\ \text{J}")]),
  ("Khoảng cách từ N tới bản trên", [P("N cũng ở dưới mốc: từ N lên mốc là xuôi chiều $\\vec E$, $d_N\\gt0$."), M(r"W_N=qEd_N\Rightarrow d_N=\dfrac{W_N}{qE}=\dfrac{-8{,}0\cdot10^{-7}}{(-5{,}0\cdot10^{-9})\cdot4000}"), A(r"d_N=0{,}040\ \text{m}=4{,}0\ \text{cm}"), P("$4{,}0\\ \\text{cm}\\lt5{,}0\\ \\text{cm}$: N nằm giữa hai bản ✓.")]),
  ("Đổi mốc sang bản dưới", [P("N cách bản dưới $5{,}0-4{,}0=1{,}0\\ \\text{cm}$. Từ N xuống mốc mới là ngược chiều $\\vec E$: $d'_N=-0{,}010\\ \\text{m}$."), M(r"W'_N=qEd'_N=(-5{,}0\cdot10^{-9})\cdot4000\cdot(-0{,}010)"), A(r"W'_N=+2{,}0\cdot10^{-7}\ \text{J}")]),
  ("Kiểm tra", [P("Với mốc mới, M cách bản dưới $4{,}0$ cm nên $W'_M=+8{,}0\\cdot10^{-7}$ J."), P(r"$W'_M-W'_N=8{,}0\cdot10^{-7}-2{,}0\cdot10^{-7}=6{,}0\cdot10^{-7}\ \text{J}$: bằng $A_{MN}$, hiệu không đổi khi đổi mốc ✓")])],
  [r"a) $E=4000\ \text{V/m}$", r"b) $W_N=-8{,}0\cdot10^{-7}\ \text{J}$", r"c) $d_N=4{,}0\ \text{cm}$", r"d) $W'_N=+2{,}0\cdot10^{-7}\ \text{J}$"],
  "Nhận dạng: đề cho <strong>thế năng hoặc công, hỏi E hay vị trí</strong> → $W=qEd$ với $d$ tới mốc có dấu; đổi mốc thì $W$ đổi, hiệu $W_M-W_N$ không đổi."),
 sol(R4, [
  ("Công của lực điện từ M tới bản âm", [P("Thả từ nghỉ, chỉ có lực điện nên công của lực điện bằng động năng ở bản âm."), M(r"A=\tfrac12mv^2=\tfrac12\cdot2{,}0\cdot10^{-8}\cdot10^2"), A(r"A=1{,}0\cdot10^{-6}\ \text{J}")]),
  ("Cường độ điện trường", [P("Đoạn đi dọc đường sức, xuôi chiều $\\vec E$: $d=+0{,}050$ m."), M(r"A=qEd\Rightarrow E=\dfrac{A}{qd}=\dfrac{1{,}0\cdot10^{-6}}{4{,}0\cdot10^{-9}\cdot0{,}050}"), A(r"E=5000\ \text{V/m}")]),
  ("Công của lực điện từ M tới P", [P("Hình chiếu của MP lên đường sức: $d_{MP}=5{,}0-2{,}0=3{,}0\\ \\text{cm}=0{,}030\\ \\text{m}$ (xuôi chiều $\\vec E$)."), M(r"A_{MP}=qEd_{MP}=4{,}0\cdot10^{-9}\cdot5000\cdot0{,}030"), A(r"A_{MP}=6{,}0\cdot10^{-7}\ \text{J}")]),
  ("Tốc độ tại P", [P("Từ nghỉ, chỉ có lực điện: công bằng động năng tại P."), M(r"\tfrac12mv_P^2=A_{MP}\Rightarrow v_P=\sqrt{\dfrac{2A_{MP}}{m}}=\sqrt{\dfrac{2\cdot6{,}0\cdot10^{-7}}{2{,}0\cdot10^{-8}}}"), A(r"v_P\approx7{,}7\ \text{m/s}")]),
  ("Kiểm tra", [P(r"Thế năng tại P (chọn mốc ở bản âm): $W_P=qE\cdot0{,}020=4{,}0\cdot10^{-7}$ J; $W_M-W_P=1{,}0\cdot10^{-6}-4{,}0\cdot10^{-7}=6{,}0\cdot10^{-7}$ J = động năng tại P ✓"), P("$v_P\\lt10\\ \\text{m/s}$: hạt mới đi được một phần đường ✓")])],
  [r"a) $A=1{,}0\cdot10^{-6}\ \text{J}$", r"b) $E=5000\ \text{V/m}$", r"c) $v_P\approx7{,}7\ \text{m/s}$"],
  "Nhận dạng: đề cho <strong>hạt thả từ nghỉ, chỉ có lực điện</strong> và một tốc độ → công = động năng; thế năng giảm bao nhiêu thì động năng tăng bấy nhiêu."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 dict(nhan_dang="Thấy <b>đoạn đi hợp với đường sức một góc</b> → nghĩ tới <b>d = MN·cosα có dấu</b>, rồi <b>A = qEd</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Hình chiếu có dấu của MN", "Độ dài đại số d của hình chiếu MN lên đường sức bằng bao nhiêu cm?", -4.0, "cm", 0.1,
       loi="Lấy $d$ bằng cả độ dài MN, hoặc chiếu bằng $\\sin$ thay vì $\\cos$, hoặc thế sai dấu của $d$."),
  buoc("Công của lực điện", "Công $A_{MN}$ của lực điện bằng bao nhiêu? (nhập số, đơn vị $10^{-17}$ J)", 3.2, "×10⁻¹⁷ J", 0.05,
       loi="Thế sai dấu của $q$ hoặc của $d$; hoặc quên đổi cm ra m.",
       ke=[("Thế $q$ và $d$ cùng dấu của chúng vào $qEd$", True),
           ("Lấy $|q|\\cdot E\\cdot MN$ vì MN là quãng đường electron đi", "$d$ là hình chiếu có dấu lên đường sức, không phải độ dài đường đi, và $q$ phải mang dấu."),
           ("Lấy $qEd$ với $d=MN\\sin\\alpha$", "Hình chiếu lên đường sức là $MN\\cos\\alpha$; $\\sin\\alpha$ là thành phần vuông góc đường sức, không sinh công.")]),
  buoc("Đi ngược từ N về M", "Công $A_{NM}$ so với $A_{MN}$ thế nào?",
       lua_chon=[("Cùng độ lớn, trái dấu", True),
                 ("Giống hệt $A_{MN}$ vì cùng đoạn MN", "Đổi chiều đi thì hình chiếu có dấu đổi dấu, nên công đổi dấu."),
                 ("Bằng không vì electron về lại điểm cũ", "Chỉ cả vòng M → N → M mới bằng không; riêng đoạn N → M vẫn có công khác không.")],
       loi="Cho rằng công không đổi khi đảo chiều đi, hoặc cho rằng quay về chỗ cũ là công của đoạn về bằng không.",
       ke=[("Tính lại hình chiếu có dấu cho chiều đi N → M rồi thay vào $qEd$", True),
           ("Dùng lại đúng $d$ và $q$ của câu trước", "Đi ngược lại thì hình chiếu có dấu đổi dấu; dùng lại $d$ cũ sẽ sai dấu."),
           ("Tính lại $E$ vì electron đi theo chiều ngược", "$E$ là của điện trường, không đổi theo chiều đi của hạt.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>nhiều đường đi cùng điểm đầu, điểm cuối</b> hoặc <b>vòng kín</b> → nghĩ tới <b>công không phụ thuộc đường đi</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Công trên đoạn AB", "Công của lực điện trên đoạn AB bằng bao nhiêu mJ?", -0.36, "mJ", 0.01,
       loi="Thế sai dấu của $q$; hoặc đổi $\\mu$C ra C sai luỹ thừa mười."),
  buoc("Công trên cả đường A → B → C", "Công của lực điện trên cả đường A → B → C bằng bao nhiêu mJ?", -0.66, "mJ", 0.01,
       loi="Lấy cả độ dài BC (hoặc $\\sin$ của góc) làm hình chiếu lên đường sức; hoặc quên cộng công của một đoạn.",
       ke=[("Tính công đoạn BC theo hình chiếu của BC lên đường sức, rồi cộng với đoạn AB", True),
           ("Lấy cả độ dài BC làm $d$ rồi cộng với đoạn AB", "$d$ là hình chiếu lên đường sức; BC hợp với đường sức một góc nên chỉ một phần của nó dọc đường sức."),
           ("Chỉ tính đoạn BC vì AB nằm dọc đường sức", "AB dọc đường sức nên hình chiếu của nó là đầy đủ, công khác không; phải cộng cả hai đoạn.")]),
  buoc("Công trên đường cong từ A tới D", "Công của lực điện trên đường cong dài 25 cm từ A tới D bằng bao nhiêu mJ?", -0.66, "mJ", 0.01,
       loi="Nhân $qE$ với độ dài đường cong, coi lực điện như lực ma sát (công tỉ lệ quãng đường đi).",
       ke=[("Dùng điểm đầu A và điểm cuối D: hình chiếu của đoạn nối hai điểm lên đường sức", True),
           ("Nhân $qE$ với độ dài đường cong", "Độ dài quãng đường không phải $d$: lực điện là lực thế, công không tỉ lệ quãng đường đi."),
           ("Phải biết hình dạng chính xác của đường cong mới tính được", "Công của lực điện không phụ thuộc hình dạng đường đi, chỉ phụ thuộc điểm đầu và điểm cuối.")]),
  buoc("Công trên cả vòng kín", "Công của lực điện trên cả vòng A → B → C → A thế nào?",
       lua_chon=[("Bằng không", True),
                 ("Bằng công trên A → B → C vì chỉ lúc đi mới có công", "Đoạn trở về C → A cũng có công, cùng độ lớn và trái dấu với công lúc đi."),
                 ("Âm, vì hạt mang điện âm", "Dấu của công không do dấu của $q$ riêng quyết định; cả vòng cho tổng bằng không.")],
       loi="Chỉ cộng công của các đoạn lúc đi, quên đoạn trở về, hoặc nhân $qE$ với chu vi của vòng.",
       ke=[("Xét điểm đầu và điểm cuối của cả vòng", True),
           ("Nhân $qE$ với chu vi tam giác ABC", "Chu vi là độ dài đường đi; công của lực điện không tỉ lệ độ dài đường đi."),
           ("Cộng $A_{ABC}$ với $A_{CA}$, lấy $d_{CA}$ dương", "Đi từ C về A là ngược chiều đường sức nên hình chiếu có dấu $d_{CA}$ âm, không phải dương.")]),
  buoc("Kiểm tra")]),
dict(nhan_dang="Thấy <b>cho thế năng hoặc công, hỏi E hay vị trí</b> → nghĩ tới <b>W = qEd</b>, <b>A = W_M − W_N</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Cường độ điện trường", "Cường độ điện trường E bằng bao nhiêu V/m?", 4000, "V/m", 20,
       loi="Thế sai dấu của $q$ hoặc của $d$; hoặc để nguyên $d$ tính bằng cm."),
  buoc("Thế năng tại N", "Thế năng điện tại N bằng bao nhiêu? (nhập số, đơn vị $10^{-7}$ J)", -8.0, "×10⁻⁷ J", 0.05,
       loi="Cộng công vào $W_M$ thay vì trừ, hoặc coi $W_N$ bằng $W_M$ vì cùng một hạt.",
       ke=[("Từ liên hệ giữa công và hiệu hai thế năng, giải ra $W_N$", True),
           ("Cộng công đã cho vào $W_M$", "Công bằng độ giảm thế năng: $A_{MN}=W_M-W_N$, nên $W_N=W_M-A_{MN}$, không phải $W_M+A_{MN}$."),
           ("Coi $W_N=W_M$ vì cùng một hạt", "Thế năng phụ thuộc vị trí: hai điểm cách mốc khác nhau thì thế năng khác nhau.")]),
  buoc("Khoảng cách từ N tới bản trên", "Khoảng cách từ N tới bản trên bằng bao nhiêu cm?", 4.0, "cm", 0.1,
       loi="Lấy $d_N$ bằng công chia $qE$ (đó là hình chiếu của đoạn MN), hoặc dùng $W_M$ thay cho $W_N$.",
       ke=[("Dùng $W_N=qEd_N$ với $E$ đã tìm, rồi giải ra $d_N$", True),
           ("Lấy $d_N=\\dfrac{A_{MN}}{qE}$", "$A_{MN}/(qE)$ là hình chiếu của đoạn MN lên đường sức, không phải khoảng cách từ N tới mốc."),
           ("Lấy $d_N=\\dfrac{W_M}{qE}$", "Đó là khoảng cách của điểm M (đề đã cho), không phải của N.")]),
  buoc("Đổi mốc sang bản dưới", "Với mốc ở bản dưới, thế năng tại N bằng bao nhiêu? (nhập số, đơn vị $10^{-7}$ J)", 2.0, "×10⁻⁷ J", 0.05,
       loi="Thế sai dấu của $d$ khi đổi mốc, hoặc tính khoảng cách từ N tới bản trên thay vì tới bản dưới.",
       ke=[("Tính khoảng cách từ N tới bản dưới, xét chiều so với $\\vec E$, rồi thay vào $qEd$", True),
           ("Giữ nguyên $W_N$ vì hạt không đổi vị trí", "Thế năng đo bằng công tới mốc; đổi mốc thì giá trị $W_N$ đổi."),
           ("Lấy $d$ là khoảng cách từ N tới bản trên", "Mốc mới ở bản dưới; $d$ tính từ N tới bản dưới.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>thả từ nghỉ, chỉ có lực điện</b> và <b>tốc độ</b> → nghĩ tới <b>công = động năng</b>.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Công của lực điện từ M tới bản âm", "Công của lực điện từ M tới bản âm bằng bao nhiêu? (nhập số, đơn vị $10^{-6}$ J)", 1.0, "×10⁻⁶ J", 0.02,
       loi="Dùng $mv^2$ (thiếu hệ số một nửa) hoặc dùng $mgh$ cho lực điện."),
  buoc("Cường độ điện trường", "Cường độ điện trường E bằng bao nhiêu V/m?", 5000, "V/m", 50,
       loi="Dùng khoảng cách đổi sai (cm thay vì m) nên $E$ lệch $100$ lần; hoặc lấy công chia cho $q$ mà quên chia cho $d$.",
       ke=[("Đặt công bằng $qEd$ với $d$ là khoảng từ M tới bản âm", True),
           ("Lấy $E=\\dfrac{A}{q}$", "$A/q$ là hiệu điện thế, đơn vị V; cần chia thêm cho $d$ (công $A=qEd$) mới ra cường độ điện trường."),
           ("Lấy $E=\\dfrac{mv^2}{qd}$", "Công bằng $\\tfrac12mv^2$, có hệ số một nửa; thiếu hệ số này làm $E$ gấp đôi.")]),
  buoc("Công của lực điện từ M tới P", "Công của lực điện từ M tới P bằng bao nhiêu? (nhập số, đơn vị $10^{-7}$ J)", 6.0, "×10⁻⁷ J", 0.05,
       loi="Lấy $d$ là khoảng cách từ P tới bản âm (đoạn P tới mốc) thay vì hình chiếu của đoạn MP.",
       ke=[("Lấy hình chiếu của đoạn MP lên đường sức nhân $qE$", True),
           ("Lấy khoảng cách từ P tới bản âm làm $d$", "Đó là $d$ của đoạn từ P tới mốc, cho thế năng $W_P$; công của đoạn MP dùng hình chiếu của MP."),
           ("Lấy luôn công cả đoạn tới bản âm", "Hạt mới tới P, chưa tới bản âm; công của đoạn MP nhỏ hơn.")]),
  buoc("Tốc độ tại P", "Tốc độ của hạt tại P bằng bao nhiêu m/s?", 7.7, "m/s", 0.1,
       loi="Cho rằng tốc độ tỉ lệ thuận với quãng đường đã đi, hoặc dùng $d$ của đoạn P tới bản âm làm công.",
       ke=[("Từ nghỉ: đặt công bằng động năng tại P rồi giải ra $v_P$", True),
           ("Tốc độ tỉ lệ thuận với quãng đường đã đi nên lấy theo tỉ lệ so với tốc độ ở bản âm", "Lực điện không đổi nên $v^2$ tỉ lệ quãng đường, không phải $v$."),
           ("Dùng lại tốc độ ở bản âm vì hạt chỉ chịu lực điện", "Tốc độ tăng dần theo quãng đường; tốc độ ở bản âm là giá trị cuối, không phải tại P.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
BUILD = [d1, d2, d3, d4]
write(J, 38, "Bài 19. Thế năng điện", DANG, BUILD, ANALYSIS, SOLS, None)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-11-02"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code)"}
raw = json.dumps(d, ensure_ascii=False, indent=1)


def _walk(x):
    if isinstance(x, str): yield x
    elif isinstance(x, dict):
        for v in x.values(): yield from _walk(v)
    elif isinstance(x, list):
        for v in x: yield from _walk(v)
for _s in _walk(d):
    _m = re.search(r"[\x00-\x1f]", _s); assert not _m, "còn ký tự điều khiển/TAB: " + repr(_s[max(0, _m.start() - 50):_m.start() + 30])
    assert '\\"' not in _s, "còn dấu gạch chéo trước nháy: " + _s[:60]
open(J, "w").write(raw)
print("xong", J, "marker-end:", raw.count("marker-end"))
