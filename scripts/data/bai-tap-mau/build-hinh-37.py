"""Bài tập mẫu Bài 18 "Điện trường đều" (Vật lí 11) — lesson_id 37. 5 dạng (quét dạng:
scripts/logs/batch-ra-soat/ket-qua/37.quet-dang.json). Hình: hinh_37.py. Ví dụ cũ (old/37.json, 23 ví dụ trong 3 nhóm + 1 mục ôn lý thuyết):
- mục "Ôn nhanh lý thuyết": bỏ (không phải bài tập).
- VD 2.6 (electron dọc đường sức, dừng sau 2 cm) → biên tập thành Dạng 2 (đổi số).
- BỎ vì sai/mơ hồ: 2.3 (đáp án (a) tự mâu thuẫn dấu: 250 V rồi −250 V), 2.7 (E = 2,84·10³ và a = 5·10⁷ sai luỹ thừa: đúng
  E ≈ 2,84·10⁻³ V/m, a ≈ 5·10⁸ m/s²), 2.11 (không nói bản A, B là bản nào nên dấu U_AB không xác định),
  2.12 (M cách bản âm 6 cm nhưng hai bản chỉ cách nhau 5 cm), 3.4 (nhận xét "đủ giữ lơ lửng" sai thực tế, đề tự mâu thuẫn bỏ trọng lực mà lơ lửng).
- Còn lại (17 ví dụ, đã tính lại đúng) vào tu_luan.
Chủ đề: dạng 1 gắn 181 (Đặc điểm điện trường đều giữa hai bản song song); dạng 2-5 gắn 182 (Chuyển động của điện tích trong điện trường đều).
Dạng ngoài lý thuyết bài (cân bằng, công lực điện, thế năng) không đưa vào dạng mới; ví dụ cũ loại đó nằm ở tu_luan.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-37.py   (idempotent, ghi 37.json với review.checked=false)"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_37 import *

J = os.path.join(HERE, "37.json")
ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
TOPICS = {t["id"]: t["name"] for t in json.load(open(os.path.join(ROOT, "scripts/data/question-topics.json"))) if t["lesson_id"] == 37}
T181, T182 = TOPICS[181], TOPICS[182]
e, me = 1.6e-19, 9.1e-31


def near(x, y, tol): return abs(x - y) <= tol


# ═════════════ SỐ LIỆU + TỰ GIẢI ĐỘC LẬP (assert) ═════════════
# Dạng 1: hạt q = −2,5 nC giữa hai bản d = 8,0 mm, U = 240 V
d1v, U1, q1, d1b = 8.0e-3, 240.0, 2.5e-9, 4.0e-3
E1 = U1 / d1v; F1 = q1 * E1; E1b = U1 / d1b; F1b = q1 * E1b
assert near(E1, 30000, 1e-6) and near(F1, 7.5e-5, 1e-12) and near(E1b, 60000, 1e-6) and near(F1b, 1.5e-4, 1e-12) and near(F1b / F1, 2, 1e-9)
assert near(U1 / 8.0, 30, 1e-9) and near(U1 * d1v, 1.92, 1e-9) and near(q1 * (U1 / 8.0), 7.5e-8, 1e-12)   # cách sai (d giữ mm; nhân thay chia) khác đáp số
# Dạng 2: electron dọc đường sức, E = 1820, v0 = 8,0e6 — tích phân số độc lập
E2, v02 = 1820.0, 8.0e6
a2 = e * E2 / me; s2 = v02 ** 2 / (2 * a2); t12 = v02 / a2
assert near(a2, 3.2e14, 1e8) and near(s2, 0.10, 1e-9) and near(t12, 2.5e-8, 1e-14)
x, v, t, dt = 0.0, v02, 0.0, 1e-11
stop_t = stop_x = back_t = None
while t < 1e-7:
    v_new = v - a2 * dt
    x += 0.5 * (v + v_new) * dt; t += dt
    if stop_t is None and v > 0 >= v_new: stop_t, stop_x = t, x
    if stop_t and x <= 0: back_t = t; break
    v = v_new
assert near(stop_x, 0.10, 2e-4) and near(stop_t, 2.5e-8, 1e-10) and near(back_t, 5.0e-8, 2e-10)
assert near(v02 * t12, 0.2, 1e-9) and near(v02 / a2 * 1, 2.5e-8, 1e-12)              # sai: s = v0·t = 20 cm khác 10 cm
assert near(s2 / v02, 1.25e-8, 1e-12)                                                # sai: t = s/v0 = 12,5 ns khác 50 ns
# Dạng 3: electron vào giữa hai bản, v0 = 1,0e7, L = 4,5 cm, d = 1,0 cm, U = 36,4 V
v03, L3, dd3, U3 = 1.0e7, 0.045, 0.010, 36.4
E3 = U3 / dd3; a3 = e * E3 / me; t3 = L3 / v03; y3 = 0.5 * a3 * t3 ** 2; tc3 = math.sqrt(dd3 / a3); xc3 = v03 * tc3
assert near(E3, 3640, 1e-6) and near(a3, 6.4e14, 1e9) and near(t3, 4.5e-9, 1e-15) and near(y3, 6.48e-3, 1e-6) and y3 > dd3 / 2
assert near(xc3, 0.03953, 2e-5) and xc3 < L3
xx, yy, vy, dt = 0.0, 0.0, 0.0, 1e-12; hit = None
while xx < L3:
    vy += a3 * dt; yy += vy * dt; xx += v03 * dt
    if yy >= dd3 / 2 and hit is None: hit = xx; break
assert near(hit, xc3, 3e-5)                                                           # tích phân số khớp công thức
assert y3 < dd3 and abs(y3 - dd3 / 2) > 1e-3                                            # bẫy: so với d (10 mm) thì tưởng ra được
assert near(0.5 * a3 * (xc3 / v03) ** 2, 0.005, 1e-9)
# Dạng 4: giọt mực
m4, q4, v04, L4_, d4_, U4, D4_ = 1.0e-10, 2.0e-12, 20.0, 0.010, 0.004, 1600.0, 0.020
E4 = U4 / d4_; F4 = q4 * E4; a4 = F4 / m4; t4 = L4_ / v04; vy4 = a4 * t4; tan4 = vy4 / v04; al4 = math.degrees(math.atan(tan4))
y4 = 0.5 * a4 * t4 ** 2; Y4 = y4 + D4_ * tan4
assert near(E4, 4.0e5, 1e-3) and near(F4, 8.0e-7, 1e-15) and near(a4, 8.0e3, 1e-6) and near(t4, 5.0e-4, 1e-12)
assert near(vy4, 4.0, 1e-9) and near(tan4, 0.2, 1e-9) and near(al4, 11.31, 0.01) and near(y4, 1.0e-3, 1e-9) and y4 < d4_ / 2
assert near(Y4, 5.0e-3, 1e-9) and near((L4_ / 2 + D4_) * tan4, Y4, 1e-12)             # kiểm bằng trung điểm
assert near(0.5 * a4 * ((L4_ + D4_) / v04) ** 2, 9.0e-3, 1e-9) and 9.0e-3 != Y4       # sai: coi lực tác dụng suốt tới màn
assert m4 * 9.8 / F4 < 2e-3                                                           # bỏ qua trọng lực hợp lý
# Dạng 5: bài ngược
v05, L5_, d5_ = 1.6e7, 0.040, 0.020
t5 = L5_ / v05; amax = d5_ / t5 ** 2; Umax = me * d5_ * amax / e
assert near(t5, 2.5e-9, 1e-15) and near(amax, 3.2e15, 1e9) and near(Umax, 364.0, 1e-6)


def exits(U):                                  # tích phân số: electron có ra khỏi bản không
    a = e * (U / d5_) / me; xx = yy = vy = 0.0; dt = 2e-13
    while xx < L5_:
        vy += a * dt; yy += vy * dt; xx += v05 * dt
        if yy >= d5_ / 2: return False, xx
    return True, xx
lo, hi = 100.0, 1000.0
for _ in range(40):
    mid = (lo + hi) / 2
    if exits(mid)[0]: lo = mid
    else: hi = mid
assert near(lo, 364.0, 0.5)
U5b = 546.0
a5b = e * (U5b / d5_) / me; xc5 = v05 * math.sqrt(d5_ / a5b)
assert not exits(U5b)[0] and near(exits(U5b)[1], xc5, 5e-5) and near(xc5, 0.03266, 1e-5) and near(L5_ * math.sqrt(Umax / U5b), xc5, 1e-9)
assert near(U5b / Umax, 1.5, 1e-9) and near(a5b, 4.8e15, 1e9)
assert near(me * d5_ ** 2 * v05 ** 2 / (e * (L5_ / 2) ** 2), 1456.0, 1e-6)   # nhầm L → L/2 cho 1456 V khác 364 V
# Số mẫu của hình mô phỏng khác đáp số của đề (không lộ)
a_s3, a_s4U, a_s5 = 3.2e14, 1000.0, 2.2e15
assert a_s3 != a3 and 0.5 * a_s3 * t3 ** 2 != y3
a_s4 = 2.0e-12 * a_s4U / (1.0e-10 * 4.0e-3)
assert near(a_s4, 5.0e3, 1e-6) and near(0.5 * a_s4 * t4 ** 2 + D4_ * (a_s4 * t4 / v04), 3.125e-3, 1e-9) and 3.125e-3 != Y4   # hạt mẫu U = 1000 V: Y = 3,125 mm khác 5,0 mm
assert a_s5 != a5b and a_s5 != amax

# ═════════════ ĐỀ ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Hai bản song song: cường độ điện trường, lực điện và chiều của lực", topic=T181,
      problem_html=r"""<p>Hai bản kim loại phẳng song song nằm ngang, cách nhau $d=8{,}0\ \text{mm}$, được nối với hiệu điện thế $U=240\ \text{V}$. Bản trên tích điện dương, bản dưới tích điện âm. Một hạt bụi mang điện $q=-2{,}5\ \text{nC}$ nằm ở giữa hai bản, xa mép bản. Bỏ qua trọng lực.</p><ol type="a"><li>Tính cường độ điện trường giữa hai bản.</li><li>Tính độ lớn lực điện tác dụng lên hạt bụi.</li><li>Lực điện hướng lên hay hướng xuống?</li><li>Giữ nguyên $U$, đưa hai bản lại gần nhau để $d$ chỉ còn một nửa. Lực điện tác dụng lên hạt bụi thay đổi thế nào?</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Bay dọc đường sức: gia tốc, quãng đường đến khi dừng và quay lại", topic=T182,
      problem_html=r"""<p>Một electron bay vào điện trường đều $E=1820\ \text{V/m}$ theo phương đường sức, cùng chiều $\vec E$, với tốc độ $v_0=8{,}0\cdot10^{6}\ \text{m/s}$. Điện trường đủ rộng, bỏ qua trọng lực. Cho $|e|=1{,}6\cdot10^{-19}\ \text{C}$, $m_e=9{,}1\cdot10^{-31}\ \text{kg}$.</p><ol type="a"><li>Lực điện cùng chiều hay ngược chiều với vận tốc? Tính độ lớn gia tốc của electron.</li><li>Tính quãng đường electron đi được kể từ lúc vào cho đến khi dừng lại.</li><li>Sau khi dừng, electron chuyển động thế nào? Tính thời gian kể từ lúc vào điện trường đến lúc nó trở lại điểm vào.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Bay vuông góc đường sức: độ lệch và có chạm bản không", topic=T182,
      problem_html=r"""<p>Một electron bay vào chính giữa hai bản kim loại phẳng nằm ngang, theo phương song song với hai bản, với tốc độ $v_0=1{,}0\cdot10^{7}\ \text{m/s}$. Hai bản dài $L=4{,}5\ \text{cm}$, cách nhau $d=1{,}0\ \text{cm}$, hiệu điện thế giữa hai bản $U=36{,}4\ \text{V}$; bản dưới tích điện dương. Bỏ qua trọng lực. Cho $|e|=1{,}6\cdot10^{-19}\ \text{C}$, $m_e=9{,}1\cdot10^{-31}\ \text{kg}$.</p><ol type="a"><li>Tính cường độ điện trường và gia tốc của electron. Electron lệch về phía bản nào?</li><li>Electron có bay ra khỏi khoảng giữa hai bản không? Nếu không, nó chạm bản ở điểm cách mép vào bao nhiêu cm?</li></ol>"""),
 dict(label="Dạng 4 · Khó · Ra khỏi hai bản: vận tốc, góc lệch và vệt trên màn", topic=T182,
      problem_html=r"""<p>Trong máy in phun, hai bản kim loại phẳng nằm ngang dùng để lái giọt mực. Một giọt mực khối lượng $m=1{,}0\cdot10^{-10}\ \text{kg}$, mang điện $q=-2{,}0\cdot10^{-12}\ \text{C}$, bay ngang vào chính giữa hai bản với tốc độ $v_0=20\ \text{m/s}$. Hai bản dài $L=1{,}0\ \text{cm}$, cách nhau $d=4{,}0\ \text{mm}$, hiệu điện thế $U=1600\ \text{V}$, bản trên tích điện dương. Ra khỏi hai bản, giọt mực bay thêm $D=2{,}0\ \text{cm}$ theo phương ngang rồi chạm tờ giấy đặt vuông góc với $\vec v_0$. Bỏ qua trọng lực và lực cản của không khí.</p><ol type="a"><li>Tính gia tốc của giọt mực khi ở giữa hai bản.</li><li>Tính thành phần vận tốc $v_y$ và góc lệch $\alpha$ của vận tốc so với $\vec v_0$ lúc giọt mực ra khỏi hai bản.</li><li>Tính khoảng cách $Y$ từ điểm giọt mực chạm giấy tới đường bay ban đầu.</li></ol>"""),
 dict(label="Dạng 5 · Khó · Bài ngược: hiệu điện thế lớn nhất để electron còn ra khỏi hai bản", topic=T182,
      problem_html=r"""<p>Một electron bay vào chính giữa hai bản kim loại phẳng nằm ngang, theo phương song song với hai bản, với tốc độ $v_0=1{,}6\cdot10^{7}\ \text{m/s}$. Hai bản dài $L=4{,}0\ \text{cm}$, cách nhau $d=2{,}0\ \text{cm}$; bản trên tích điện dương. Bỏ qua trọng lực. Cho $|e|=1{,}6\cdot10^{-19}\ \text{C}$, $m_e=9{,}1\cdot10^{-31}\ \text{kg}$.</p><ol type="a"><li>Tìm hiệu điện thế lớn nhất giữa hai bản để electron còn bay ra khỏi khoảng giữa hai bản.</li><li>Đặt hiệu điện thế $U=546\ \text{V}$. Electron có bay ra khỏi hai bản không? Nếu không, nó chạm bản nào, ở điểm cách mép vào bao nhiêu cm?</li></ol>"""),
]

# ═════════════ PHÂN TÍCH ĐỀ (cột 3: khái niệm / điều kiện chung, không ghi kết luận hay hướng giải) ═════════════
ANALYSIS = [
 [(r'"hai bản kim loại phẳng song song … hiệu điện thế $U=240$ V"', r"$U=240$ V", "⚠ Điện trường đều chỉ có giữa hai bản, xa mép bản"),
  (r'"cách nhau $d=8{,}0$ mm"', r"$d=8{,}0$ mm", "Liên hệ giữa $E$, $U$ và $d$; $d$ tính bằng mét"),
  (r'"bản trên tích điện dương, bản dưới tích điện âm"', "Bản trên $+$, bản dưới $-$", "Quy ước chiều đường sức (chiều $\\vec E$)"),
  (r'"hạt bụi mang điện $q=-2{,}5$ nC"', r"$q=-2{,}5$ nC", "Lực điện lên điện tích đặt trong điện trường; dấu của $q$"),
  (r'"bỏ qua trọng lực"', "Chỉ còn lực điện", "⚠ Chỉ xét lực điện"),
  (r'"giữ nguyên $U$ … $d$ chỉ còn một nửa"', r"$U$ không đổi; $d'=\dfrac{d}{2}$", "Liên hệ giữa $E$, $U$ và $d$"),
  (r'"cường độ điện trường … độ lớn lực điện … hướng lên hay xuống … thay đổi thế nào"', r"Cần $E$, $F$, chiều của $\vec F$, $F'$", "Đại lượng cần tìm")],
 [(r'"electron bay vào điện trường đều $E=1820$ V/m"', r"$E=1820$ V/m", "⚠ Điện trường đều: $\\vec E$ như nhau mọi điểm"),
  (r'"theo phương đường sức, cùng chiều $\vec E$"', r"$\vec v_0$ cùng phương, cùng chiều $\vec E$", "Chiều đường sức; chiều lực điện phụ thuộc dấu của điện tích"),
  (r'"$v_0=8{,}0\cdot10^{6}$ m/s"', r"$v_0=8{,}0\cdot10^{6}$ m/s", "Vận tốc đầu"),
  (r'"cho $|e|$, $m_e$"', r"$|e|=1{,}6\cdot10^{-19}$ C; $m_e=9{,}1\cdot10^{-31}$ kg", "Định luật II Newton"),
  (r'"điện trường đủ rộng, bỏ qua trọng lực"', "Chỉ có lực điện, suốt chuyển động", "⚠ Chỉ xét lực điện; hạt không ra khỏi điện trường"),
  (r'"cùng chiều hay ngược chiều với vận tốc … gia tốc"', r"Cần chiều của $\vec F$ và $a$", "Đại lượng cần tìm"),
  (r'"quãng đường … cho đến khi dừng lại"', r"Cần $s$", "Đại lượng cần tìm"),
  (r'"thời gian … trở lại điểm vào"', r"Cần $t$", "Đại lượng cần tìm")],
 [(r'"bay vào chính giữa … song song với hai bản"', r"$\vec v_0\perp\vec E$; cách mỗi bản một nửa khoảng cách hai bản", "Chuyển động theo hai phương vuông góc nhau"),
  (r'"$v_0=1{,}0\cdot10^{7}$ m/s"', r"$v_0=1{,}0\cdot10^{7}$ m/s", "Vận tốc theo phương song song với bản"),
  (r'"dài $L=4{,}5$ cm, cách nhau $d=1{,}0$ cm"', r"$L=4{,}5$ cm; $d=1{,}0$ cm", "Quãng bay trong điện trường; khoảng cách hai bản"),
  (r'"$U=36{,}4$ V; bản dưới tích điện dương"', r"$U=36{,}4$ V; bản dưới $+$", "Liên hệ giữa $E$, $U$ và $d$; chiều đường sức"),
  (r'"bỏ qua trọng lực"', r"$|e|=1{,}6\cdot10^{-19}$ C; $m_e=9{,}1\cdot10^{-31}$ kg", "⚠ Chỉ xét lực điện"),
  (r'"cường độ điện trường và gia tốc … lệch về phía bản nào"', r"Cần $E$, $a$, phía lệch", "Đại lượng cần tìm"),
  (r'"có bay ra khỏi khoảng giữa hai bản không … chạm bản ở điểm cách mép vào bao nhiêu"', "Cần kết luận và vị trí chạm", "Đại lượng cần tìm")],
 [(r'"giọt mực khối lượng $m$, mang điện $q=-2{,}0\cdot10^{-12}$ C"', r"$m=1{,}0\cdot10^{-10}$ kg; $q=-2{,}0\cdot10^{-12}$ C", "Lực điện lên điện tích; dấu của $q$"),
  (r'"bay ngang vào chính giữa hai bản, $v_0=20$ m/s"', r"$v_0=20$ m/s; $\vec v_0\perp\vec E$", "Chuyển động theo hai phương vuông góc nhau"),
  (r'"dài $L=1{,}0$ cm, cách nhau $d=4{,}0$ mm, $U=1600$ V; bản trên dương"', r"$L=1{,}0$ cm; $d=4{,}0$ mm; $U=1600$ V; bản trên $+$", "Liên hệ giữa $E$, $U$ và $d$ (đổi đơn vị); chiều đường sức"),
  (r'"bỏ qua trọng lực và lực cản"', "Chỉ có lực điện khi ở giữa hai bản", "⚠ Chỉ xét lực điện"),
  (r'"ra khỏi hai bản, giọt mực bay thêm $D=2{,}0$ cm"', r"$D=2{,}0$ cm", "⚠ Ngoài hai bản không còn điện trường"),
  (r'"gia tốc … thành phần $v_y$ và góc lệch $\alpha$ lúc ra khỏi hai bản"', r"Cần $a$, $v_y$, $\alpha$", "Đại lượng cần tìm"),
  (r'"khoảng cách $Y$ từ điểm chạm giấy tới đường bay ban đầu"', r"Cần $Y$", "Đại lượng cần tìm")],
 [(r'"bay vào chính giữa … song song với hai bản, $v_0=1{,}6\cdot10^{7}$ m/s"', r"$v_0=1{,}6\cdot10^{7}$ m/s; $\vec v_0\perp\vec E$", "Chuyển động theo hai phương vuông góc nhau"),
  (r'"dài $L=4{,}0$ cm, cách nhau $d=2{,}0$ cm"', r"$L=4{,}0$ cm; $d=2{,}0$ cm", "Quãng bay trong điện trường; khoảng cách hai bản"),
  (r'"bản trên tích điện dương"', "Bản trên $+$", "Chiều đường sức; dấu của điện tích"),
  (r'"bỏ qua trọng lực"', r"$|e|=1{,}6\cdot10^{-19}$ C; $m_e=9{,}1\cdot10^{-31}$ kg", "⚠ Chỉ xét lực điện"),
  (r'"hiệu điện thế lớn nhất … để electron còn bay ra khỏi khoảng giữa hai bản"', r"Cần $U_{\max}$", "Đại lượng cần tìm"),
  (r'"đặt $U=546$ V … chạm bản nào, cách mép vào bao nhiêu"', r"$U=546$ V; cần kết luận và vị trí chạm", "Đại lượng cần tìm")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = ["<strong>Khái niệm:</strong> giữa hai bản phẳng song song, xa mép, điện trường đều: $\\vec E$ như nhau mọi điểm.",
      "<strong>Quy ước:</strong> đường sức đi từ bản dương sang bản âm; lực lên $q\\gt0$ cùng chiều $\\vec E$, lên $q\\lt0$ ngược chiều $\\vec E$.",
      r"Cường độ: $E=\dfrac{U}{d}$ ($d$ ra mét) · lực: $F=|q|E$",
      "⚠ <strong>Điều kiện:</strong> xa mép bản; chỉ xét lực điện (bỏ qua trọng lực)."]
R2 = ["<strong>Khái niệm:</strong> electron có $q\\lt0$: lực điện ngược chiều $\\vec E$.",
      "<strong>Định luật:</strong> điện trường đều nên lực không đổi; định luật II Newton cho gia tốc không đổi.",
      r"Gia tốc: $a=\dfrac{|e|E}{m_e}$ · thẳng biến đổi đều: $v^2-v_0^2=2as$ · $v=v_0+at$",
      "⚠ <strong>Điều kiện:</strong> chỉ có lực điện; điện trường đủ rộng."]
R3 = ["<strong>Khái niệm:</strong> $\\vec v_0\\perp\\vec E$: Ox thẳng đều, Oy (cùng chiều lực) nhanh dần đều.",
      r"Lực điện $F=|e|E$ với $E=\dfrac{U}{d}$ · gia tốc $a=\dfrac{|e|U}{m_ed}$",
      r"Ox: $x=v_0t$ · Oy: $y=\dfrac{1}{2}at^2$",
      "Electron ($q\\lt0$) lệch về phía bản dương.",
      "⚠ <strong>Điều kiện:</strong> chỉ có lực điện; hạt vào chính giữa nên cách mỗi bản $\\dfrac{d}{2}$."]
R4 = ["<strong>Khái niệm:</strong> trong hai bản: Ox đều, Oy nhanh dần đều (như ném ngang, thay $g$ bằng $a$).",
      r"Gia tốc: $a=\dfrac{|q|U}{md}$ · $v_y=at$ · $\tan\alpha=\dfrac{v_y}{v_0}$",
      "⚠ <strong>Điều kiện:</strong> ra khỏi hai bản là hết lực điện: hạt đi thẳng theo hướng vận tốc lúc ra."]
R5 = ["<strong>Khái niệm:</strong> trường hợp giới hạn: electron vừa sượt mép bản ở cuối đường bay.",
      r"Ox: $t=\dfrac{L}{v_0}$ · Oy: $y=\dfrac{1}{2}at^2$ · $a=\dfrac{|e|U}{m_ed}$",
      "⚠ <strong>Điều kiện:</strong> chỉ có lực điện; hạt vào chính giữa nên cách mỗi bản $\\dfrac{d}{2}$."]

SOLS = [
 sol(R1, [
  ("Cường độ điện trường", [P(r"Đổi $d=8{,}0\ \text{mm}=0{,}0080\ \text{m}$."), M(r"E=\dfrac{U}{d}=\dfrac{240}{0{,}0080}"), A(r"E=3{,}0\cdot10^{4}\ \text{V/m}")]),
  ("Độ lớn lực điện", [P(r"Đổi $|q|=2{,}5\ \text{nC}=2{,}5\cdot10^{-9}\ \text{C}$."), M(r"F=|q|E=2{,}5\cdot10^{-9}\cdot3{,}0\cdot10^{4}"), A(r"F=7{,}5\cdot10^{-5}\ \text{N}=75\ \mu\text{N}")]),
  ("Chiều của lực", [P("Bản trên dương nên $\\vec E$ hướng xuống (từ bản dương sang bản âm)."), P("$q\\lt0$ nên lực ngược chiều $\\vec E$."), A("T:Lực điện <strong>hướng lên</strong>, về phía bản dương.")]),
  ("Khi hai bản lại gần", [P(r"$d'=\dfrac{d}{2}=4{,}0\ \text{mm}$, $U$ giữ nguyên:"), M(r"E'=\dfrac{U}{d'}=\dfrac{240}{0{,}0040}=6{,}0\cdot10^{4}\ \text{V/m}"), M(r"F'=|q|E'=2{,}5\cdot10^{-9}\cdot6{,}0\cdot10^{4}=1{,}5\cdot10^{-4}\ \text{N}"), A("T:$F'=2F$: lực điện <strong>tăng gấp đôi</strong>, chiều không đổi.")]),
  ("Kiểm tra", [P(r"Đơn vị: $1\ \text{V/m}=1\ \text{N/C}$ nên $\text{N/C}\cdot\text{C}=\text{N}$ ✓"), P("$d$ giảm một nửa thì $E$ và $F$ gấp đôi, khớp bước 4.")])],
  [r"a) $E=3{,}0\cdot10^{4}\ \text{V/m}$", r"b) $F=7{,}5\cdot10^{-5}\ \text{N}$", "c) Hướng lên (về phía bản dương)", "d) $F'=2F=1{,}5\\cdot10^{-4}\\ \\text{N}$"],
  "Nhận dạng: đề cho <strong>hai bản song song kèm U và d</strong> → điện trường đều; đổi $d$ ra mét, chiều lực theo dấu của $q$."),
 sol(R2, [
  ("Chiều lực và loại chuyển động", [P("$\\vec E$ cùng chiều $\\vec v_0$. Electron có $q\\lt0$ nên $\\vec F$ ngược chiều $\\vec E$, tức ngược chiều $\\vec v_0$."), A("T:Electron chuyển động <strong>chậm dần đều</strong>.")]),
  ("Gia tốc", [M(r"a=\dfrac{|e|E}{m_e}=\dfrac{1{,}6\cdot10^{-19}\cdot1820}{9{,}1\cdot10^{-31}}"), A(r"a=3{,}2\cdot10^{14}\ \text{m/s}^2"), P("Hướng ngược $\\vec v_0$ và không đổi (điện trường đều).")]),
  ("Quãng đường đến khi dừng", [P("Chọn chiều dương theo $\\vec v_0$, gia tốc là $-a$. Lúc dừng $v=0$:"), M(r"0-v_0^2=-2as"), M(r"s=\dfrac{v_0^2}{2a}=\dfrac{(8{,}0\cdot10^{6})^2}{2\cdot3{,}2\cdot10^{14}}"), A(r"s=0{,}10\ \text{m}=10\ \text{cm}")]),
  ("Thời gian đến lúc trở lại điểm vào", [P("Thời gian đến lúc dừng:"), M(r"t_1=\dfrac{v_0}{a}=\dfrac{8{,}0\cdot10^{6}}{3{,}2\cdot10^{14}}=2{,}5\cdot10^{-8}\ \text{s}"), P("Lực điện vẫn còn, hướng ngược $\\vec v_0$: electron dừng rồi nhanh dần đều quay lại."), P("Đi quãng $s$ từ nghỉ với gia tốc $a$ mất $\\sqrt{2s/a}=t_1$, bằng thời gian đi."), M(r"t=2t_1"), A(r"t=5{,}0\cdot10^{-8}\ \text{s}=50\ \text{ns}")]),
  ("Kiểm tra", [P(r"Đơn vị: $\dfrac{\text{C}\cdot\text{V/m}}{\text{kg}}=\dfrac{\text{N}}{\text{kg}}=\text{m/s}^2$ ✓"), P(r"Về tới điểm vào, tốc độ $at_1=8{,}0\cdot10^{6}\ \text{m/s}$, bằng tốc độ lúc vào và ngược chiều ✓")])],
  [r"a) Ngược chiều vận tốc; $a=3{,}2\cdot10^{14}\ \text{m/s}^2$", r"b) $s=10\ \text{cm}$", "c) Dừng rồi quay lại; $t=50\\ \\text{ns}$"],
  "Nhận dạng: electron <strong>bay dọc đường sức</strong> → lực không đổi, chuyển động thẳng biến đổi đều; xét chiều lực theo dấu của $q$."),
 sol(R3, [
  ("Cường độ điện trường", [P(r"Đổi $d=1{,}0\ \text{cm}=0{,}010\ \text{m}$."), M(r"E=\dfrac{U}{d}=\dfrac{36{,}4}{0{,}010}"), A(r"E=3640\ \text{V/m}")]),
  ("Gia tốc", [M(r"a=\dfrac{|e|E}{m_e}=\dfrac{1{,}6\cdot10^{-19}\cdot3640}{9{,}1\cdot10^{-31}}"), A(r"a=6{,}4\cdot10^{14}\ \text{m/s}^2")]),
  ("Phía lệch", [P("Bản dưới dương nên $\\vec E$ hướng lên."), P("$q\\lt0$ nên lực ngược chiều $\\vec E$: hướng xuống."), A("T:Electron lệch về <strong>bản dưới</strong> (bản dương).")]),
  ("Độ lệch nếu bay hết chiều dài bản", [P("Ox thẳng đều:"), M(r"t=\dfrac{L}{v_0}=\dfrac{0{,}045}{1{,}0\cdot10^{7}}=4{,}5\cdot10^{-9}\ \text{s}"), P("Oy nhanh dần đều:"), M(r"y=\dfrac{1}{2}at^2=\dfrac{1}{2}\cdot6{,}4\cdot10^{14}\cdot(4{,}5\cdot10^{-9})^2"), A(r"y\approx6{,}48\cdot10^{-3}\ \text{m}=6{,}48\ \text{mm}")]),
  ("So với khoảng cách tới bản", [P("Electron vào chính giữa nên cách bản dưới chỉ $\\dfrac{d}{2}=5{,}0\\ \\text{mm}$."), M(r"6{,}48\ \text{mm}\gt5{,}0\ \text{mm}"), A("T:Electron <strong>chạm bản dưới</strong> trước khi ra khỏi hai bản.")]),
  ("Điểm chạm", [P("Chạm bản khi $y=\\dfrac{d}{2}$:"), M(r"\dfrac{1}{2}at_c^2=\dfrac{d}{2}\Rightarrow t_c=\sqrt{\dfrac{d}{a}}=\sqrt{\dfrac{0{,}010}{6{,}4\cdot10^{14}}}\approx3{,}95\cdot10^{-9}\ \text{s}"), M(r"x_c=v_0t_c=1{,}0\cdot10^{7}\cdot3{,}95\cdot10^{-9}"), A(r"x_c\approx3{,}95\ \text{cm}")]),
  ("Kiểm tra", [P("$x_c\\lt L=4{,}5\\ \\text{cm}$ ✓ (chạm trước khi hết bản)."), P(r"Trọng lực $m_eg\approx8{,}9\cdot10^{-30}\ \text{N}$ nhỏ hơn lực điện $\approx5{,}8\cdot10^{-16}\ \text{N}$ cỡ $10^{14}$ lần: bỏ qua là đúng.")])],
  [r"a) $E=3640\ \text{V/m}$; $a=6{,}4\cdot10^{14}\ \text{m/s}^2$; lệch về bản dưới (bản dương)", r"b) Không ra được: chạm bản dưới, cách mép vào $\approx3{,}95\ \text{cm}$"],
  "Nhận dạng: hạt <strong>bay vuông góc đường sức</strong> → hai chuyển động thành phần; luôn kiểm tra xem hạt có chạm bản không."),
 sol(R4, [
  ("Gia tốc", [P(r"Đổi $d=4{,}0\ \text{mm}=4{,}0\cdot10^{-3}\ \text{m}$."), M(r"E=\dfrac{U}{d}=\dfrac{1600}{4{,}0\cdot10^{-3}}=4{,}0\cdot10^{5}\ \text{V/m}"), M(r"F=|q|E=2{,}0\cdot10^{-12}\cdot4{,}0\cdot10^{5}=8{,}0\cdot10^{-7}\ \text{N}"), M(r"a=\dfrac{F}{m}=\dfrac{8{,}0\cdot10^{-7}}{1{,}0\cdot10^{-10}}"), A(r"a=8{,}0\cdot10^{3}\ \text{m/s}^2=8{,}0\ \text{km/s}^2")]),
  ("Vận tốc dọc lúc ra khỏi bản", [P("Thời gian ở giữa hai bản (Ox đều):"), M(r"t=\dfrac{L}{v_0}=\dfrac{0{,}010}{20}=5{,}0\cdot10^{-4}\ \text{s}"), M(r"v_y=at=8{,}0\cdot10^{3}\cdot5{,}0\cdot10^{-4}"), A(r"v_y=4{,}0\ \text{m/s}")]),
  ("Góc lệch", [M(r"\tan\alpha=\dfrac{v_y}{v_0}=\dfrac{4{,}0}{20}=0{,}20"), A(r"\alpha\approx11{,}3^\circ")]),
  ("Độ lệch lúc ra khỏi bản", [M(r"y=\dfrac{1}{2}at^2=\dfrac{1}{2}\cdot8{,}0\cdot10^{3}\cdot(5{,}0\cdot10^{-4})^2=1{,}0\cdot10^{-3}\ \text{m}"), P("$y=1{,}0\\ \\text{mm}\\lt\\dfrac{d}{2}=2{,}0\\ \\text{mm}$: giọt mực ra khỏi hai bản, không chạm bản."), A(r"y=1{,}0\ \text{mm}")]),
  ("Vệt trên giấy", [P("Ra khỏi hai bản không còn lực điện: giọt mực đi thẳng theo hướng vận tốc lúc ra, lệch thêm:"), M(r"D\tan\alpha=20\ \text{mm}\cdot0{,}20=4{,}0\ \text{mm}"), M(r"Y=y+D\tan\alpha=1{,}0+4{,}0"), A(r"Y=5{,}0\ \text{mm}")]),
  ("Kiểm tra", [P(r"Đường thẳng sau khi ra, kéo ngược lại, đi qua trung điểm hai bản: $Y=\left(\dfrac{L}{2}+D\right)\tan\alpha=(5{,}0+20)\cdot0{,}20=5{,}0\ \text{mm}$ ✓"), P(r"Trọng lực $mg\approx10^{-9}\ \text{N}$ nhỏ hơn lực điện $8{,}0\cdot10^{-7}\ \text{N}$ khoảng $10^3$ lần: bỏ qua là đúng.")])],
  [r"a) $a=8{,}0\cdot10^{3}\ \text{m/s}^2$", r"b) $v_y=4{,}0\ \text{m/s}$; $\alpha\approx11{,}3^\circ$", r"c) $Y=5{,}0\ \text{mm}$ (lệch về phía bản trên)"],
  "Nhận dạng: giọt/hạt <strong>ra khỏi hai bản rồi bay tới màn</strong> → hết lực thì đi thẳng; độ lệch trên màn = độ lệch lúc ra + phần đi thẳng."),
 sol(R5, [
  ("Thời gian bay trong hai bản", [M(r"t=\dfrac{L}{v_0}=\dfrac{0{,}040}{1{,}6\cdot10^{7}}"), A(r"t=2{,}5\cdot10^{-9}\ \text{s}"), P("$t$ chỉ phụ thuộc $L$ và $v_0$, không phụ thuộc $U$.")]),
  ("Điều kiện giới hạn", [P("Electron vừa bay ra khi sượt mép bản: cuối đường bay độ lệch bằng nửa khoảng cách hai bản."), M(r"y(t)=\dfrac{d}{2}")]),
  ("Gia tốc lớn nhất", [M(r"\dfrac{1}{2}a_{\max}t^2=\dfrac{d}{2}\Rightarrow a_{\max}=\dfrac{d}{t^2}=\dfrac{0{,}020}{(2{,}5\cdot10^{-9})^2}"), A(r"a_{\max}=3{,}2\cdot10^{15}\ \text{m/s}^2")]),
  ("Hiệu điện thế lớn nhất", [P(r"Từ $a=\dfrac{|e|U}{m_ed}$:"), M(r"U_{\max}=\dfrac{m_e\,d\,a_{\max}}{|e|}=\dfrac{9{,}1\cdot10^{-31}\cdot0{,}020\cdot3{,}2\cdot10^{15}}{1{,}6\cdot10^{-19}}"), A(r"U_{\max}=364\ \text{V}")]),
  ("Với $U=546\\ \\text{V}$", [M(r"546\ \text{V}\gt364\ \text{V}"), P("$U$ vượt giá trị lớn nhất nên electron lệch quá nửa khoảng cách trước khi hết bản. Bản trên dương hút electron."), A("T:Electron <strong>không ra được</strong>, chạm <strong>bản trên</strong> (bản dương).")]),
  ("Điểm chạm", [P(r"Gia tốc tỉ lệ với $U$: $a=a_{\max}\cdot\dfrac{546}{364}=4{,}8\cdot10^{15}\ \text{m/s}^2$."), M(r"t_c=\sqrt{\dfrac{d}{a}}=\sqrt{\dfrac{0{,}020}{4{,}8\cdot10^{15}}}\approx2{,}04\cdot10^{-9}\ \text{s}"), M(r"x_c=v_0t_c=1{,}6\cdot10^{7}\cdot2{,}04\cdot10^{-9}"), A(r"x_c\approx3{,}27\ \text{cm}")]),
  ("Kiểm tra", [P(r"Cách khác: $x_c=L\sqrt{\dfrac{U_{\max}}{U}}=4{,}0\sqrt{\dfrac{364}{546}}\approx3{,}27\ \text{cm}$ ✓"), P("$x_c\\lt L=4{,}0\\ \\text{cm}$ ✓, và $U=U_{\\max}$ cho $x_c=L$ ✓.")])],
  [r"a) $U_{\max}=364\ \text{V}$", r"b) Không ra được: chạm bản trên, cách mép vào $\approx3{,}27\ \text{cm}$"],
  "Nhận dạng: đề hỏi <strong>“lớn nhất / nhỏ nhất để còn …”</strong> → xét trường hợp giới hạn, đặt điều kiện sượt mép bản."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 dict(nhan_dang="Thấy <b>hai bản song song, có U và d</b> → nghĩ tới <b>điện trường đều</b>; đổi d ra mét, xét dấu của q.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Cường độ điện trường", "Cường độ điện trường E giữa hai bản bằng bao nhiêu V/m?", 30000, "V/m", 100,
       loi="Để nguyên $d$ tính bằng mm nên $E$ nhỏ hơn đúng $1000$ lần; hoặc nhân $U$ với $d$ thay vì chia."),
  buoc("Độ lớn lực điện", "Độ lớn lực điện lên hạt bụi bằng bao nhiêu µN?", 75, "µN", 0.5,
       loi="Đổi nC sai luỹ thừa mười (nhân $10^{-6}$ thay vì $10^{-9}$), hoặc giữ dấu trừ của $q$ rồi báo lực âm.",
       ke=[("Tính lực từ độ lớn của điện tích và $E$ vừa tìm", True),
           ("Chia $E$ thêm cho $d$ một lần nữa", "$E$ đã là $U/d$; chia thêm $d$ là tính $d$ hai lần."),
           ("Lấy $F=E\\cdot d$ vì vừa dùng $d$", "$E\\cdot d$ chính là $U$, không phải lực. Lực cần $E$ nhân điện tích.")]),
  buoc("Chiều của lực", "Lực điện lên hạt bụi hướng thế nào?",
       lua_chon=[("Hướng lên, về phía bản dương", True),
                 ("Hướng xuống, cùng chiều $\\vec E$", "Cùng chiều $\\vec E$ chỉ đúng với $q\\gt0$; hạt này có $q\\lt0$."),
                 ("Bằng không vì đã bỏ qua trọng lực", "Bỏ qua trọng lực chỉ loại lực khác; lực điện $|q|E$ vẫn tác dụng.")],
       loi="Cho rằng lực điện luôn cùng chiều đường sức, quên xét dấu của $q$.",
       ke=[("Xác định chiều $\\vec E$ (từ bản dương sang bản âm), rồi xét dấu của $q$", True),
           ("Chiều lực luôn cùng chiều đường sức", "Chỉ đúng với điện tích dương; điện tích âm chịu lực ngược chiều."),
           ("Chiều lực hướng về bản gần hạt hơn", "Hạt ở giữa, cách đều hai bản; chiều lực theo dấu của $q$ và chiều $\\vec E$, không theo khoảng cách.")]),
  buoc("Khi hai bản lại gần", "Giữ nguyên $U$, $d$ giảm một nửa. Lực điện thay đổi thế nào?",
       lua_chon=[("Tăng gấp đôi", True),
                 ("Giảm một nửa", "$d$ giảm thì $E=U/d$ tăng; lực $|q|E$ tăng theo."),
                 ("Không đổi vì $U$ không đổi", "$U$ không đổi nhưng $E$ phụ thuộc cả $d$; lực phụ thuộc $E$."),
                 ("Tăng gấp bốn", "$E$ tỉ lệ nghịch với $d$ (bậc một), không phải bậc hai.")],
       loi="Cho rằng $U$ không đổi thì $E$ và lực không đổi, quên rằng $d$ nằm ở mẫu số.",
       ke=[("Tính lại $E'$ với $d'$ rồi tính $F'=|q|E'$", True),
           ("Giữ $E$ như cũ vì $U$ không đổi", "$E=U/d$: đổi $d$ thì $E$ đổi dù $U$ cố định."),
           ("Tính lại $q$ vì hai bản gần nhau hơn", "$q$ là điện tích của hạt, không đổi theo khoảng cách hai bản.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>electron bay dọc đường sức</b> → nghĩ tới <b>lực không đổi, chuyển động thẳng biến đổi đều</b>; xét chiều lực theo dấu q.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Chiều lực và loại chuyển động", "Electron chuyển động thế nào ngay sau khi vào điện trường?",
       lua_chon=[("Chậm dần đều, vì lực điện ngược chiều vận tốc", True),
                 ("Nhanh dần đều, vì lực điện cùng chiều $\\vec E$ và $\\vec v_0$", "Lực cùng chiều $\\vec E$ chỉ đúng với $q\\gt0$; electron chịu lực ngược chiều $\\vec E$."),
                 ("Thẳng đều, vì $\\vec v_0$ song song đường sức", "Song song đường sức không làm mất lực; lực điện $|e|E$ vẫn tác dụng và làm đổi vận tốc.")],
       loi="Đối xử với electron như điện tích dương: cho lực cùng chiều $\\vec E$ nên kết luận nhanh dần."),
  buoc("Gia tốc", "Độ lớn gia tốc a của electron bằng bao nhiêu? (nhập hệ số a của kết quả a·10ⁿ)", 3.2, "×10ⁿ m/s²", 0.05,
       loi="Đảo tỉ số (lấy $m_e/(|e|E)$) hoặc sai luỹ thừa mười của $m_e$.",
       ke=[("Lấy lực điện $|e|E$ chia cho khối lượng electron", True),
           ("Lấy $m_eE$ chia cho $|e|$", "Đảo tỉ số: gia tốc tỉ lệ thuận với lực, tỉ lệ nghịch với khối lượng."),
           ("Lấy $a=g$", "Trọng lực đã bỏ qua; gia tốc ở đây do lực điện gây ra.")]),
  buoc("Quãng đường đến khi dừng", "Electron đi được bao xa (cm) thì dừng lại?", 10, "cm", 0.2,
       loi="Dùng $s=v_0t$ như chuyển động đều, hoặc quên bình phương $v_0$.",
       ke=[("Chậm dần đều tới $v=0$: dùng hệ thức không có thời gian giữa $v$, $v_0$, $a$, $s$", True),
           ("Dùng $s=v_0t$ với một thời gian bất kì", "Công thức đó chỉ đúng khi vận tốc không đổi; ở đây vận tốc giảm dần."),
           ("Dùng $s=\\dfrac{v_0^2}{2g}$", "Gia tốc ở đây là $a=|e|E/m_e$, không phải $g$.")]),
  buoc("Thời gian đến lúc trở lại điểm vào", "Thời gian từ lúc vào điện trường đến lúc trở lại điểm vào bằng bao nhiêu ns?", 50, "ns", 1,
       loi="Chỉ tính tới lúc dừng rồi dừng bài, quên rằng lực điện vẫn còn nên electron quay lại.",
       ke=[("Tính thời gian đến lúc dừng rồi cộng thời gian quay về (bằng nhau)", True),
           ("Dừng lại ở lúc $v=0$ vì electron đã hết chuyển động", "Lực điện vẫn tác dụng nên electron không đứng yên mà quay lại."),
           ("Lấy $t=\\dfrac{s}{v_0}$", "Vận tốc không đều nên không dùng $s/v_0$ cho cả quá trình.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>hạt bay vào vuông góc đường sức</b> → nghĩ tới <b>hai chuyển động thành phần</b>; kiểm tra xem hạt có chạm bản không.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 4}, buoc=[
  buoc("Cường độ điện trường", "Cường độ điện trường E giữa hai bản bằng bao nhiêu V/m?", 3640, "V/m", 20,
       loi="Để nguyên $d$ tính bằng cm nên $E$ nhỏ hơn đúng $100$ lần so với số đúng."),
  buoc("Gia tốc", "Độ lớn gia tốc a của electron bằng bao nhiêu? (nhập hệ số a của kết quả a·10ⁿ)", 6.4, "×10ⁿ m/s²", 0.1,
       loi="Đảo tỉ số khối lượng và lực, hoặc sai luỹ thừa mười của $m_e$.",
       ke=[("Lấy lực điện $|e|E$ chia cho khối lượng electron", True),
           ("Lấy $a=g$ như ném ngang", "Gia tốc ở đây do lực điện, không phải $g$."),
           ("Lấy $a=\\dfrac{U}{d}$", "$U/d$ là cường độ điện trường $E$, chưa phải gia tốc.")]),
  buoc("Phía lệch", "Electron lệch về phía bản nào?",
       lua_chon=[("Bản dưới (bản dương)", True),
                 ("Bản trên (bản âm)", "Electron mang điện âm bị bản âm đẩy ra, bản dương hút vào."),
                 ("Không lệch vì bay song song với hai bản", "Có lực điện vuông góc $\\vec v_0$ nên quỹ đạo cong dần về một phía.")],
       loi="Cho electron lệch về phía bản âm (như điện tích dương), quên rằng lực ngược chiều $\\vec E$.",
       ke=[("Xác định chiều $\\vec E$ từ bản dương sang bản âm, rồi đảo chiều vì $q\\lt0$", True),
           ("Chiều lệch cùng chiều đường sức", "Chỉ đúng với điện tích dương; electron lệch ngược chiều đường sức."),
           ("Chiều lệch theo chiều $\\vec v_0$", "$\\vec v_0$ vuông góc với lực; độ lệch ngang không do $\\vec v_0$ quyết định.")]),
  buoc("Độ lệch nếu bay hết chiều dài bản", "Nếu electron bay hết chiều dài $L$ mà không bị chặn, độ lệch y bằng bao nhiêu mm?", 6.48, "mm", 0.05,
       loi="Dùng $y=v_0t$ (coi như đều) hoặc quên bình phương $t$ trong $y=\\dfrac{1}{2}at^2$.",
       ke=[("Tính $t=L/v_0$ trước, rồi độ lệch theo phương nhanh dần đều", True),
           ("Dùng $y=\\dfrac{1}{2}at$", "Độ lệch tỉ lệ với $t^2$, không phải $t$."),
           ("Dùng $y=\\dfrac{1}{2}gt^2$ như ném ngang", "Gia tốc ở đây là $a$ do lực điện, không phải $g$.")]),
  buoc("So với khoảng cách tới bản", "Electron có bay ra khỏi khoảng giữa hai bản không?",
       lua_chon=[("Không: độ lệch lớn hơn khoảng cách từ đường bay tới bản", True),
                 ("Có: độ lệch nhỏ hơn khoảng cách hai bản $d$", "Electron vào chính giữa nên cách mỗi bản chỉ $d/2$, không phải $d$."),
                 ("Có: electron chỉ bay ngang nên không chạm", "Lực điện làm vận tốc dọc tăng dần; electron lệch dần về phía bản.")],
       loi="So độ lệch với $d$ thay vì với $d/2$ nên kết luận hạt ra được.",
       ke=[("So độ lệch với khoảng cách từ đường bay ban đầu tới bản", True),
           ("So độ lệch với $d$", "Hạt vào chính giữa nên cách bản chỉ bằng một nửa $d$."),
           ("So độ lệch với chiều dài $L$", "$L$ là chiều dài bản, không phải khoảng cách theo phương lệch.")]),
  buoc("Điểm chạm", "Nếu bị chặn, electron chạm bản ở điểm cách mép vào bao nhiêu cm?", 3.95, "cm", 0.05,
       loi="Lấy $x=L$ (coi như chạm ở cuối bản) hoặc tính $t_c$ với độ lệch bằng $d$ thay vì $d/2$.",
       ke=[("Đặt độ lệch bằng khoảng cách tới bản để tìm thời điểm chạm, rồi nhân $v_0$", True),
           ("Lấy $x=L$", "Chạm trước khi hết bản nên $x$ nhỏ hơn $L$."),
           ("Đặt độ lệch bằng $d$ để tìm thời điểm chạm", "Khoảng cách tới bản là $d/2$, không phải $d$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>hạt ra khỏi hai bản rồi bay tới màn</b> → nghĩ tới <b>hết trường là đi thẳng</b>, theo vận tốc lúc ra.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 4}, buoc=[
  buoc("Gia tốc", "Gia tốc của giọt mực bằng bao nhiêu (đơn vị ×10³ m/s²)?", 8.0, "×10³ m/s²", 0.05,
       loi="Để nguyên $d$ tính bằng mm khi tính $E$, hoặc quên rằng đơn vị đang là ×10³ m/s²."),
  buoc("Vận tốc dọc lúc ra khỏi bản", "Thành phần vận tốc $v_y$ lúc giọt mực ra khỏi hai bản bằng bao nhiêu m/s?", 4.0, "m/s", 0.05,
       loi="Lấy thời gian là $\\dfrac{L+D}{v_0}$ (kể cả quãng tới màn) thay vì chỉ quãng $L$ trong hai bản.",
       ke=[("Tính thời gian ở giữa hai bản từ $L$ và $v_0$, rồi nhân gia tốc", True),
           ("Lấy thời gian từ $L+D$ vì giọt mực bay tới màn", "Chỉ khi ở giữa hai bản mới có gia tốc; ngoài hai bản $v_y$ giữ nguyên."),
           ("Lấy $v_y=v_0$ vì giọt mực bay ngang", "$v_0$ là thành phần ngang; thành phần dọc do lực điện tạo ra và tăng dần.")]),
  buoc("Góc lệch", "Góc lệch $\\alpha$ của vận tốc so với $\\vec v_0$ bằng bao nhiêu độ?", 11.3, "°", 0.2,
       loi="Lấy $\\tan\\alpha=v_0/v_y$ (đảo tỉ số) sẽ ra góc với phương thẳng đứng.",
       ke=[("Lấy tang của góc bằng thành phần dọc chia thành phần ngang", True),
           ("Lấy tang của góc bằng thành phần ngang chia thành phần dọc", "Đó là góc so với phương thẳng đứng; góc so với $\\vec v_0$ có cạnh đối là $v_y$."),
           ("Cộng $v_0+v_y$ rồi tìm góc", "Hai thành phần vuông góc, không cộng đại số.")]),
  buoc("Độ lệch lúc ra khỏi bản", "Độ lệch y của giọt mực lúc ra khỏi hai bản bằng bao nhiêu mm?", 1.0, "mm", 0.05,
       loi="Dùng $y=v_yt$ thay vì $\\dfrac{1}{2}v_yt$ (bỏ quên hệ số $\\dfrac{1}{2}$ của chuyển động nhanh dần).",
       ke=[("Dùng công thức nhanh dần đều từ nghỉ theo phương lực với thời gian ở giữa hai bản", True),
           ("Dùng $y=v_y\\,t$", "$v_y$ chỉ là vận tốc lúc cuối; độ lệch trung bình bằng một nửa."),
           ("Dùng $y=\\dfrac{1}{2}at^2$ với $t=\\dfrac{L+D}{v_0}$", "Tính thời gian trong hai bản, không phải tới màn.")]),
  buoc("Vệt trên giấy", "Khoảng cách Y từ điểm chạm giấy tới đường bay ban đầu bằng bao nhiêu mm?", 5.0, "mm", 0.1,
       loi="Lấy $Y=y$ vì tưởng ra khỏi hai bản là hết lệch, hoặc tính $Y$ như thể còn lực điện suốt quãng tới màn.",
       ke=[("Cộng độ lệch lúc ra khỏi bản với phần lệch thêm khi đi thẳng", True),
           ("Lấy $Y=y$ vì đã ra khỏi hai bản", "Ra khỏi bản giọt mực vẫn bay tiếp tới giấy với vận tốc có thành phần dọc, nên lệch thêm."),
           ("Tính $\\dfrac{1}{2}a\\left(\\dfrac{L+D}{v_0}\\right)^2$ coi lực tác dụng suốt tới màn", "Ngoài hai bản không còn điện trường nên không còn gia tốc.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>điều kiện “lớn nhất / nhỏ nhất để còn …”</b> → nghĩ tới <b>trường hợp giới hạn</b> của quỹ đạo.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Thời gian bay trong hai bản", "Thời gian electron bay giữa hai bản bằng bao nhiêu ns?", 2.5, "ns", 0.05,
       loi="Chia $v_0$ cho $L$ (đảo tỉ số), hoặc để $L$ tính bằng cm khi đổi sang mét."),
  buoc("Điều kiện giới hạn", "Electron vừa đủ bay ra (sượt mép bản) thì điều kiện nào đúng?",
       lua_chon=[("Cuối đường bay, độ lệch bằng nửa khoảng cách hai bản", True),
                 ("Cuối đường bay, độ lệch bằng cả khoảng cách $d$ giữa hai bản", "Hạt vào chính giữa nên cách bản chỉ $d/2$."),
                 ("Giữa đường bay, độ lệch bằng nửa khoảng cách hai bản", "Phải xét ở cuối đường bay (hết chiều dài bản), không phải giữa chừng.")],
       loi="Đặt độ lệch bằng $d$ thay vì $d/2$ nên $U_{\\max}$ ra gấp đôi giá trị đúng.",
       ke=[("Chọn điều kiện biên: tại hết chiều dài bản, độ lệch bằng khoảng cách tới bản", True),
           ("Chọn điều kiện biên: tại hết chiều dài bản, vận tốc dọc bằng $v_0$", "Không có điều kiện đó để vừa chạm; điều kiện nằm ở độ lệch."),
           ("Bỏ qua điều kiện biên, thử các giá trị $U$ tuỳ ý", "Không có điều kiện thì không tìm được giá trị lớn nhất.")]),
  buoc("Gia tốc lớn nhất", "Gia tốc lớn nhất để electron còn bay ra khỏi hai bản bằng bao nhiêu? (nhập hệ số a của kết quả a·10ⁿ)", 3.2, "×10ⁿ m/s²", 0.05,
       loi="Quên bình phương $t$ trong $y=\\dfrac{1}{2}at^2$, hoặc dùng $y=d$.",
       ke=[("Từ độ lệch cuối đường bay và thời gian bay, giải ra gia tốc", True),
           ("Lấy $a=g$ vì ném ngang", "Gia tốc ở đây do lực điện và thay đổi theo $U$."),
           ("Lấy $a=\\dfrac{v_0}{t}$", "$v_0$ không đổi theo phương ngang nên $a_x=0$; gia tốc nằm theo phương lệch.")]),
  buoc("Hiệu điện thế lớn nhất", "Hiệu điện thế lớn nhất để electron còn bay ra bằng bao nhiêu V?", 364, "V", 2,
       loi="Dùng nhầm $a=\\dfrac{|e|U}{m_e}$ (quên chia cho $d$) nên $U$ lệch lớn.",
       ke=[("Từ gia tốc lớn nhất suy ra $U$ qua biểu thức gia tốc theo $U$, $d$, $m_e$", True),
           ("Lấy $U=E\\,d$ với $E=a$", "$a$ là gia tốc, không phải cường độ điện trường."),
           ("Lấy $U=\\dfrac{m_ea}{|e|}$", "Thiếu $d$: $E=\\dfrac{m_ea}{|e|}$, còn $U=E\\,d$.")]),
  buoc("Với U = 546 V", "Đặt $U=546\\ \\text{V}$. Electron có bay ra khỏi hai bản không?",
       lua_chon=[("Không ra được: chạm bản trên (bản dương)", True),
                 ("Ra được vì $U$ lớn nên electron bay nhanh hơn", "$U$ không làm tăng $v_0$ theo phương ngang; $U$ lớn làm lệch nhiều hơn."),
                 ("Không ra được: chạm bản dưới (bản âm)", "Electron bị bản dương hút và bản âm đẩy, nên chạm bản dương.")],
       loi="Cho rằng electron chạm bản âm (như điện tích dương).",
       ke=[("So $U$ với giá trị lớn nhất vừa tìm", True),
           ("Lấy $U=546\\ \\text{V}$ làm hiệu điện thế lớn nhất", "$546\\ \\text{V}$ là giá trị đề cho để kiểm tra; ngưỡng là $U_{\\max}$ vừa tìm ở bước trước."),
           ("Tính ngay điểm chạm mà chưa so với ngưỡng", "Phải biết hạt có chạm bản hay không trước, bằng cách so $U$ với $U_{\\max}$ ở bước trước.")]),
  buoc("Điểm chạm", "Electron chạm bản ở điểm cách mép vào bao nhiêu cm?", 3.27, "cm", 0.05,
       loi="Lấy $x=L$ hoặc dùng gia tốc ứng với $U_{\\max}$ thay vì ứng với $546\\ \\text{V}$.",
       ke=[("Tính gia tốc ứng với $U$ mới, tìm thời điểm độ lệch bằng khoảng cách tới bản, nhân $v_0$", True),
           ("Dùng gia tốc ứng với $U_{\\max}$", "Gia tốc phải ứng với hiệu điện thế mới của đề."),
           ("Lấy $x=L$", "Hạt chạm trước khi hết bản nên $x$ nhỏ hơn $L$.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ TỰ LUẬN: ví dụ cũ đã tính lại ═════════════
OLD = json.load(open(os.path.join(HERE, "old/37.json")))["questions"]


def vd_list(i):
    parts = re.split(r'(?=<p class="text-base leading-relaxed my-2"><strong class="font-bold">Đề: )', OLD[i]["body_html"])
    return [p for p in parts if "Đề: " in p]


def vd(i, k):
    p = vd_list(i)[k]
    m = re.match(r'<p class="[^"]*"><strong class="font-bold">Đề: </strong>(.*?)</p><p class="[^"]*"><strong class="font-bold">Lời giải: </strong>(.*?)</p>\s*$', p, flags=re.S)
    assert m, (i, k)
    de, gi = m.group(1), m.group(2)
    de = re.sub(r"<(?![a-zA-Z/!?])", r"\\lt ", de); gi = re.sub(r"<(?![a-zA-Z/!?])", r"\\lt ", gi)
    return de, gi


# tính lại từng ví dụ giữ lại
assert near(120e3 / 0.02, 6e6, 1) and near(e * 6e6, 9.6e-13, 1e-17)                                            # 1.1
assert near(750 / 15e-3, 5e4, 1e-6) and near(1.2e-7 / 5e4, 2.4e-12, 1e-17)                                    # 1.2
assert near(math.sqrt(4e12 + 2 * e * 15 / me), 3.045e6, 2e3)                                                    # 2.1
assert near(math.sqrt(2 * e * 6000 * 0.01 / me), 4.59e6, 3e4)                                                   # 2.2
assert near(0.5 * me * 64e12 / e, 182, 0.5)                                                                     # 2.4
assert near(math.sqrt(2 * 8e-5 * 12 / 3e-3), 0.8, 1e-9) and near(8e-5 * 60 / 3e-3 * 0.2 * 2, 0.64, 1e-9)       # 2.5
assert near(e * 100, 1.6e-17, 1e-22) and near(e * 100 * 1e-7 / me, 1.758e6, 2e3) and near(math.hypot(2e6, 1.758e6), 2.663e6, 3e3)   # 2.8
assert near(me * 1e12 / e, 5.69, 0.01)                                                                          # 2.9
assert near(e * 1.7e6 / 1.7e-27, 1.6e14, 1e11) and near(math.sqrt(2 * 1.6e14 * 0.2), 8e6, 1e4)                 # 2.10
assert near(me * 9e10 / (2 * e * 100), 2.56e-3, 1e-5)                                                           # 2.13
assert near(3.06e-15 * 10 * 0.02 / 4.8e-18, 127.5, 1e-6)                                                        # 3.1
assert near(1e-6 * 100 / (9.8 * 0.015), 6.8e-4, 1e-5)                                                           # 3.2
assert near(0.1e-3 * 10 * math.tan(math.radians(14)) / 1e3, 2.493e-7, 1e-9)                                    # 3.3
assert near(1e-8 * 1e5 / (0.1e-3 * 10), 1.0, 1e-9)                                                              # 3.5
assert near(2.5e-7 * 1e6 / (0.025 * 10), 1.0, 1e-9)                                                             # 3.6
assert near(math.sqrt(2 * 0.008 * 300 / (60 * 9.8)), 0.0904, 1e-3)                                              # 3.7
assert near(0.1e-3 * 10 * 0.01 * math.tan(math.radians(10)) / 1000, 1.763e-9, 1e-12)                           # 3.8

# Chỉ số (nhóm, k): nhóm = chỉ số mục trong OLD; k = vị trí VD trong mục (0-based). Ánh xạ thủ công theo bảng tính ở trên:
#   mục 1: [0]=ống tia X, [1]=hai bản F→q
#   mục 2: [0]=2.1, [1]=2.2, [2]=2.3 (bỏ), [3]=2.4, [4]=2.5, [5]=2.6 (→ Dạng 2, bỏ khỏi tự luận), [6]=2.7 (bỏ), [7]=2.8,
#          [8]=2.9, [9]=2.10, [10]=2.11 (bỏ), [11]=2.12 (bỏ), [12]=2.13
#   mục 3: [0]=3.1 … [7]=3.8 (bỏ [3]=3.4)
KEEP = [(1, 0, "Dễ"), (1, 1, "Dễ"), (2, 8, "Dễ"), (2, 9, "Dễ"), (2, 12, "Trung bình"), (2, 0, "Trung bình"), (2, 1, "Trung bình"),
        (2, 3, "Trung bình"), (2, 4, "Trung bình"), (2, 7, "Trung bình"),
        (3, 0, "Trung bình"), (3, 1, "Trung bình"), (3, 2, "Trung bình"), (3, 4, "Trung bình"), (3, 5, "Trung bình"), (3, 7, "Trung bình"),
        (3, 6, "Khó")]
# kiểm: vd_list đúng số VD và nội dung các VD bị bỏ / chuyển
L1, L2, L3_ = vd_list(1), vd_list(2), vd_list(3)
assert len(L1) == 2 and len(L2) == 13 and len(L3_) == 8, (len(L1), len(L2), len(L3_))
assert "250\\,\\text{eV}" in L2[2] and "10^{4}\\,\\text{m/s}$ dọc theo" in L2[6] and "$U_{AB}$ giữa hai bản" in L2[10] and "cách bản âm $6\\,\\text{cm}$" in L2[11]
assert "1250\\,\\text{V/m}" in L2[5]                                                      # 2.6 → Dạng 2
assert "PM2.5" in L3_[3]
parts = []
for n, (g, k, muc) in enumerate(KEEP, 1):
    de, gi = vd(g, k)
    parts.append(f'<h4>Bài {n} · {muc}</h4><p>{de}</p><details><summary>Hướng dẫn giải</summary><p>{gi}</p></details>')
TU_LUAN = dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
               body_html="<p>Các bài còn lại của bài học, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn. Một số bài dùng định lí động năng hoặc điều kiện cân bằng nên có thể cần kiến thức của bài sau.</p>" + "".join(parts))

# ═════════════ GHI FILE ═════════════
BUILD = [d1, d2, d3, d4, d5]
import re as _re
def _cdot(m):
    return _re.sub(r'(?<=[\d}])\.(?=\d|\\)', r'\\cdot ', m.group(0))
TU_LUAN["body_html"] = _re.sub(r'\$[^$]+\$', _cdot, TU_LUAN["body_html"])
write(J, 37, "Bài 18. Điện trường đều", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code)"}
raw = json.dumps(d, ensure_ascii=False, indent=1)


def _walk(x):
    if isinstance(x, str): yield x
    elif isinstance(x, dict):
        for v in x.values(): yield from _walk(v)
    elif isinstance(x, list):
        for v in x: yield from _walk(v)
for _s in _walk(d):
    assert not re.search(r"[\x00-\x1f]", _s), "còn ký tự điều khiển/TAB: " + repr(_s[:60])
    assert '\\"' not in _s, "còn dấu gạch chéo trước nháy: " + _s[:60]
open(J, "w").write(raw)
print("xong", J, "marker-end:", raw.count("marker-end"), "tu_luan:", len(KEEP))
