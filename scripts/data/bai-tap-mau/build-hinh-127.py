"""Bài tập mẫu bài 16 (lesson 127) — Điện từ trường. Mô hình sóng điện từ (Vật lí 12). 6 dạng, dễ → khó
(quét dạng: scripts/logs/batch-ra-soat/ket-qua/127.quet-dang.json; ví dụ cũ: old/127.json).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-127.py  → ghi scripts/data/bai-tap-mau/127.json.
Ví dụ cũ: VD6 (FM 100 MHz) → Dạng 2; VD7 (đổi môi trường) → Dạng 4; VD4 (Hertz), VD8, Bài 13.1 → tu_luan; VD3 (mạch LC, phụ thuộc hình) bỏ.
Topic: bài 127 không có dòng trong question-topics.json; chủ đề ngân hàng tương ứng là "Điện từ trường và sóng điện từ" (id 237)."""
import math, os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hinh_127 import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "127.json")
OLD = json.load(open(os.path.join(HERE, "old/127.json")))["questions"]
TOPIC = "Điện từ trường và sóng điện từ"

# ───────────── tự giải độc lập (Python) — mọi đáp số dùng bên dưới lấy từ đây ─────────────
c = 3e8
# D2
f_fm, lam_ir = 91e6, 940e-9
D2_lam = c / f_fm; D2_T = 1 / f_fm; D2_f = c / lam_ir
assert abs(D2_lam - 3.2967) < 1e-3 and abs(D2_T * 1e9 - 10.989) < 1e-3 and abs(D2_f - 3.1915e14) < 1e11
assert abs(D2_lam / c - D2_T) < 1e-15                                   # λ = cT khớp T = 1/f
assert not (abs(D2_lam / f_fm - D2_T) < 1e-9) and not (abs(f_fm - D2_T) < 1e-9)           # hai lựa chọn sai của bước 2
assert abs(1 / lam_ir - D2_f) > 1e10 and abs(c / 940 - D2_f) > 1e10                              # hai lựa chọn sai của bước 3
# D3
E0, B0 = 18.0, 60.0
D3_B = B0 * 6.0 / E0; D3_E = E0 * 45.0 / B0; D3_B_at_E0 = B0 * 0.0 / E0
assert abs(D3_B - 20) < 1e-9 and abs(D3_E - 13.5) < 1e-9 and D3_B_at_E0 == 0
assert abs(E0 * (1 - 45.0 / B0) - D3_E) > 1 and abs(E0 * B0 / 45.0 - D3_E) > 1                   # lựa chọn sai bước 2: tổng 1, tỉ lệ nghịch
assert abs(E0 / (B0 * 1e-9) - c) < 1                                                           # E0/B0 = c: số liệu thực tế
# D4
lam0, n = 540e-9, 4 / 3
D4_f = c / lam0; D4_v = c / n; D4_lam = D4_v / D4_f
assert abs(D4_f - 5.5556e14) < 1e10 and abs(D4_v - 2.25e8) < 1e3 and abs(D4_lam - 405e-9) < 1e-12
assert abs(D4_lam - lam0 / n) < 1e-15
assert abs(c / D4_f - D4_lam) > 1e-8 and abs(n * lam0 - D4_lam) > 1e-8                           # lựa chọn sai bước 3
assert abs(n * c - D4_v) > 1e7 and abs(lam0 * D4_f - D4_v) > 1e7                                  # lựa chọn sai bước 2
# D5
d, tp = 3.84e8, 2.50
D5_t1 = d / c; D5_t = 2 * d / c; D5_d2 = c * tp / 2
assert abs(D5_t1 - 1.28) < 1e-9 and abs(D5_t - 2.56) < 1e-9 and abs(D5_d2 - 3.75e8) < 1
assert 3.63e8 < D5_d2 < 4.06e8                                                                  # trong dải thực tế của khoảng cách Trái Đất - Mặt Trăng
assert abs(D5_t1 - D5_t) > 0.1 and abs(c / d - D5_t) > 0.1                                       # lựa chọn sai bước 2
assert abs(c * tp - D5_d2) > 1e7 and abs(c * (tp - D5_t1) - D5_d2) > 5e6                                    # lựa chọn sai bước 3
# D6
om = TAU * 1e8; ph0 = math.pi / 3
D6_T = TAU / om; D6_t0 = (math.pi / 2 - ph0) / om; D6_tmax = (TAU - ph0) / om
assert abs(D6_T - 1e-8) < 1e-20 and abs(D6_t0 - 1e-8 / 12) < 1e-20 and abs(D6_tmax - 5e-9 / 0.6) < 1e-20 and abs(D6_tmax - 1e-8 * 5 / 6) < 1e-20
# nghiệm nhỏ nhất dương, dò bằng vòng lặp
ts = [i * 1e-12 for i in range(1, 20000)]
first0 = next(t for t in ts if math.cos(om * t + ph0) * math.cos(om * (t - 1e-12) + ph0) <= 0)
firstmax = next(t for t in ts if math.cos(om * t + ph0) >= 1 - 1e-6)
assert abs(first0 - D6_t0) < 2e-12 and abs(firstmax - D6_tmax) < 4e-12
assert abs(math.pi / 2 / om - D6_T / 4) < 1e-20 and abs(D6_T / 4 - D6_t0) > 1e-10                  # lựa chọn sai: bỏ pha ban đầu (T/4)
assert abs(-(ph0) / om) > 0 and (0 - ph0) / om < 0                                              # pha = 0 cho t < 0
assert abs(D6_T - D6_tmax) > 1e-9                                                               # lựa chọn sai: t = T

def r2(x, nd=2): return round(x, nd)

# ───────────── Đề ─────────────
BUILD = [d1, d2, d3, d4, d5, d6]

DANG = [
 dict(label="Dạng 1 · Dễ · Điện trường xoáy: nguồn gây ra và dạng đường sức", topic=TOPIC,
      problem_html=("<p>Thả một nam châm thẳng rơi vào lòng một ống dây được nối kín với điện kế nhạy. Khi nam châm đang chuyển động trong lòng ống, kim điện kế lệch. "
                    "Khi nam châm được giữ yên trong lòng ống, kim điện kế chỉ vạch $0$.</p>"
                    "<p>a) Điện trường trong dây dẫn do nguyên nhân nào gây ra?</p><p>b) Đường sức của điện trường đó có dạng nào?</p>")),
 dict(label="Dạng 2 · Dễ · Bước sóng, chu kì và tần số của sóng điện từ", topic=TOPIC,
      problem_html=(r"<p>Một kênh phát thanh FM phát sóng điện từ có tần số $91\ \text{MHz}$. Bộ điều khiển từ xa của quạt trần dùng đèn LED hồng ngoại phát sóng điện từ có bước sóng $940\ \text{nm}$. "
                    r"Coi hai sóng truyền trong không khí như trong chân không, lấy $c=3\cdot10^{8}\ \text{m/s}$.</p>"
                    "<p>a) Tính bước sóng của sóng FM.</p><p>b) Tính chu kì của sóng FM.</p><p>c) Tính tần số của sóng hồng ngoại.</p>")),
 dict(label="Dạng 3 · Trung bình · E và B cùng pha: tìm giá trị tức thời", topic=TOPIC,
      problem_html=(r"<p>Tại điểm M trong không gian có sóng điện từ truyền qua. Cường độ điện trường và cảm ứng từ tại M biến thiên điều hoà với giá trị cực đại lần lượt là $E_0=18\ \text{V/m}$ và $B_0=60\ \text{nT}$.</p>"
                    r"<p>a) Tại thời điểm cường độ điện trường có độ lớn $6{,}0\ \text{V/m}$, cảm ứng từ tại M có độ lớn bằng bao nhiêu?</p>"
                    r"<p>b) Tại thời điểm cảm ứng từ có độ lớn $45\ \text{nT}$, cường độ điện trường tại M có độ lớn bằng bao nhiêu?</p>"
                    "<p>c) Tại thời điểm cường độ điện trường bằng $0$, cảm ứng từ tại M bằng bao nhiêu?</p>")),
 dict(label="Dạng 4 · Trung bình · Sóng điện từ đổi môi trường: tần số, tốc độ, bước sóng", topic=TOPIC,
      problem_html=(r"<p>Ánh sáng lục có bước sóng $540\ \text{nm}$ trong chân không đi vào nước có chiết suất $n=\dfrac43$. Lấy $c=3\cdot10^{8}\ \text{m/s}$.</p>"
                    "<p>a) Tính tần số của ánh sáng.</p><p>b) Tính tốc độ truyền của ánh sáng trong nước.</p><p>c) Tính bước sóng của ánh sáng trong nước.</p>")),
 dict(label="Dạng 5 · Khó · Thời gian truyền xung vô tuyến và khoảng cách tới Mặt Trăng", topic=TOPIC,
      problem_html=(r"<p>Một ra-đa đặt trên Trái Đất phát xung sóng vô tuyến tới Mặt Trăng; xung phản xạ trên bề mặt Mặt Trăng rồi quay về ra-đa. "
                    r"Ở lần đo thứ nhất, khoảng cách Trái Đất - Mặt Trăng là $d=3{,}84\cdot10^{8}\ \text{m}$. Coi sóng truyền trong chân không với tốc độ $c=3\cdot10^{8}\ \text{m/s}$.</p>"
                    "<p>a) Tính thời gian xung đi từ Trái Đất đến Mặt Trăng.</p>"
                    "<p>b) Tính khoảng thời gian từ lúc phát đến lúc thu xung phản xạ ở lần đo thứ nhất.</p>"
                    r"<p>c) Ở lần đo thứ hai, xung phản xạ thu được sau $2{,}50\ \text{s}$ kể từ lúc phát. Tính khoảng cách Trái Đất - Mặt Trăng lúc đó.</p>")),
 dict(label="Dạng 6 · Khó · Thời điểm đầu tiên cường độ điện trường bằng 0 hoặc cực đại", topic=TOPIC,
      problem_html=(r"<p>Tại một điểm có sóng điện từ truyền qua, cảm ứng từ biến thiên theo phương trình $B=B_0\cos\left(2\pi\cdot10^{8}t+\dfrac{\pi}{3}\right)$, với $B_0\gt0$ và $t$ tính bằng giây.</p>"
                    "<p>a) Tính chu kì của sóng.</p>"
                    "<p>b) Kể từ $t=0$, tìm thời điểm đầu tiên cường độ điện trường tại điểm đó bằng $0$.</p>"
                    "<p>c) Kể từ $t=0$, tìm thời điểm đầu tiên cường độ điện trường tại điểm đó đạt giá trị cực đại.</p>")),
]

ANALYSIS = [
 [("“nam châm thẳng rơi vào lòng một ống dây nối kín với điện kế”", "Mạch kín có điện kế", "Điện kế báo có dòng điện thì trong dây có điện trường"),
  ("“khi nam châm đang chuyển động … kim điện kế lệch”", "Có dòng điện", "So sánh với tình huống sau: điều gì ở ống dây thay đổi?"),
  ("“khi giữ yên … kim chỉ vạch $0$”", "Không có dòng điện", "⚠ Xác định nguồn gây điện trường trước khi nói về đường sức"),
  ("“do nguyên nhân nào gây ra”", "Nguyên nhân", "Đại lượng cần tìm"),
  ("“đường sức … có dạng nào”", "Dạng đường sức", "Đại lượng cần tìm")],
 [(r"“tần số $91\ \text{MHz}$”", r"$f=91$ MHz $=9{,}1\cdot10^{7}$ Hz", "Đổi MHz ra Hz"),
  (r"“bước sóng $940\ \text{nm}$”", r"$\lambda=940$ nm $=9{,}4\cdot10^{-7}$ m", "Đổi nm ra m"),
  (r"“như trong chân không, $c=3\cdot10^{8}\ \text{m/s}$”", r"$c=3\cdot10^{8}$ m/s", "⚠ Dùng $c$ vì coi không khí như chân không; đổi mọi đại lượng về Hz, m, s trước khi thế số"),
  ("“Tính bước sóng … chu kì của sóng FM”", r"Cần $\lambda$, $T$", "Đại lượng cần tìm"),
  ("“Tính tần số của sóng hồng ngoại”", "Cần $f$", "Đại lượng cần tìm")],
 [(r"“biến thiên điều hoà … $E_0=18\ \text{V/m}$ và $B_0=60\ \text{nT}$”", r"$E_0=18$ V/m; $B_0=60$ nT", "Giá trị cực đại của hai đại lượng"),
  ("“Tại điểm M … có sóng điện từ truyền qua”", "Một điểm, cùng một thời điểm", "⚠ Quan hệ giữa $E$ và $B$ dùng cho cùng một điểm, cùng một thời điểm của sóng điện từ truyền trong không gian"),
  (r"“độ lớn $6{,}0\ \text{V/m}$”", r"$E=6{,}0$ V/m", "Biết giá trị tức thời của một đại lượng, tìm đại lượng kia"),
  (r"“độ lớn $45\ \text{nT}$”", r"$B=45$ nT", "Biết giá trị tức thời của một đại lượng, tìm đại lượng kia"),
  ("“cường độ điện trường bằng $0$”", "$E=0$", "Xét đại lượng kia ở đúng thời điểm đó"),
  ("“bằng bao nhiêu” ở ba ý", r"Cần $B$, $E$, $B$", "Đại lượng cần tìm")],
 [(r"“bước sóng $540\ \text{nm}$ trong chân không”", r"$\lambda_0=540$ nm $=5{,}4\cdot10^{-7}$ m", "⚠ Đây là bước sóng trong chân không; công thức liên hệ $c$, $f$, $\\lambda$ ở chân không chỉ dùng cho bước sóng này"),
  (r"“đi vào nước có chiết suất $n=\dfrac43$”", r"$n=\dfrac43$", "Chiết suất cho biết sóng trong môi trường chậm hơn trong chân không bao nhiêu lần"),
  (r"“$c=3\cdot10^{8}\ \text{m/s}$”", r"$c=3\cdot10^{8}$ m/s", "Tốc độ trong chân không"),
  ("“Tính tần số”, “tốc độ … trong nước”, “bước sóng … trong nước”", r"Cần $f$, $v$, $\lambda'$", "Đại lượng cần tìm")],
 [(r"“khoảng cách … $d=3{,}84\cdot10^{8}\ \text{m}$”", r"$d=3{,}84\cdot10^{8}$ m", "Khoảng cách một chiều giữa Trái Đất và Mặt Trăng"),
  (r"“tốc độ $c=3\cdot10^{8}\ \text{m/s}$” trong chân không", r"$c=3\cdot10^{8}$ m/s", "⚠ Xung truyền thẳng đều với tốc độ $c$ và phản xạ về đúng đường cũ"),
  ("“thời gian xung đi từ Trái Đất đến Mặt Trăng”", "Cần $t_1$", "Đại lượng cần tìm"),
  ("“từ lúc phát đến lúc thu xung phản xạ”", "Cần $t$", "Trong khoảng thời gian này xung đi những đoạn nào?"),
  (r"“lần đo thứ hai … sau $2{,}50\ \text{s}$”", r"$t'=2{,}50$ s", "Thời gian đo gồm những đoạn nào?"),
  ("“khoảng cách … lúc đó”", r"Cần $d'$", "Đại lượng cần tìm")],
 [(r"“$B=B_0\cos\left(2\pi\cdot10^{8}t+\dfrac{\pi}{3}\right)$”", r"$\omega=2\pi\cdot10^{8}$ rad/s; pha ban đầu $\dfrac{\pi}{3}$", "Đọc tần số góc và pha ban đầu từ phương trình"),
  ("“Tại một điểm có sóng điện từ truyền qua”", "Một điểm cố định", "⚠ Quan hệ pha giữa $E$ và $B$ của sóng điện từ quyết định cách viết phương trình của $E$ từ phương trình của $B$"),
  ("“Tính chu kì của sóng”", "Cần $T$", "Đại lượng cần tìm"),
  ("“kể từ $t=0$ … thời điểm đầu tiên”", r"$t\gt0$ nhỏ nhất", "Nghiệm dương nhỏ nhất của phương trình về pha"),
  ("“điện trường bằng $0$”, “đạt giá trị cực đại”", "Cần hai thời điểm", "Đại lượng cần tìm")],
]
# sửa nhầm "\\lambda" trong chuỗi raw ở hàng ⚠ dạng 4
ANALYSIS[3][0] = (ANALYSIS[3][0][0], ANALYSIS[3][0][1], "⚠ Đây là bước sóng trong chân không; công thức liên hệ $c$, $f$, $\\lambda$ ở chân không chỉ dùng cho bước sóng này")

# ───────────── Lời giải ─────────────
R1 = ["<strong>Khái niệm:</strong> từ trường biến thiên theo thời gian sinh ra điện trường xoáy.",
      "Đường sức điện trường xoáy là đường cong kín, bao quanh các đường cảm ứng từ.",
      "Điện trường tĩnh do điện tích đứng yên gây ra, đường sức không khép kín.",
      "⚠ <strong>Điều kiện:</strong> điện trường xoáy chỉ xuất hiện ở nơi từ trường biến thiên; từ trường mạnh nhưng không đổi thì không sinh ra nó."]
R2 = [r"<strong>Khái niệm:</strong> bước sóng $\lambda$ là quãng đường sóng đi được trong một chu kì $T$.",
      r"<strong>Định luật:</strong> trong chân không mọi sóng điện từ truyền với tốc độ $c=3\cdot10^{8}$ m/s.",
      r"$\lambda=cT=\dfrac{c}{f}$ · $T=\dfrac{1}{f}$",
      r"Đổi: $1\ \text{MHz}=10^{6}$ Hz · $1\ \text{nm}=10^{-9}$ m",
      "⚠ <strong>Điều kiện:</strong> không khí coi như chân không; đổi mọi đại lượng về Hz, m, s trước khi thế số."]
R3 = [r"<strong>Khái niệm:</strong> sóng điện từ là sóng ngang, $\vec E\perp\vec B\perp$ phương truyền.",
      r"<strong>Định luật:</strong> $\vec E$ và $\vec B$ biến thiên điều hoà, luôn cùng pha.",
      r"Cùng pha: cùng đạt cực đại, cùng triệt tiêu, nên $\dfrac{E}{E_0}=\dfrac{B}{B_0}$ ở mọi thời điểm.",
      r"Đổi: $1\ \text{nT}=10^{-9}$ T (không cần đổi nếu so cùng loại với $B_0$).",
      "⚠ <strong>Điều kiện:</strong> $E$ và $B$ xét tại cùng một điểm, cùng một thời điểm, của sóng điện từ truyền trong không gian."]
R4 = [r"<strong>Khái niệm:</strong> tần số do nguồn quyết định, giữ nguyên khi sóng đổi môi trường.",
      r"<strong>Định luật:</strong> trong môi trường chiết suất $n$, tốc độ $v=\dfrac{c}{n}$, nhỏ hơn $c$.",
      r"$\lambda_0=\dfrac{c}{f}$ (chân không) · $\lambda'=\dfrac{v}{f}$ (môi trường)",
      r"Đổi: $1\ \text{nm}=10^{-9}$ m",
      "⚠ <strong>Điều kiện:</strong> $540$ nm là bước sóng trong chân không; trong nước phải dùng tốc độ $v$ của nước."]
R5 = [r"<strong>Khái niệm:</strong> ra-đa đo khoảng cách bằng thời gian sóng đi tới vật rồi phản xạ về.",
      r"<strong>Định luật:</strong> sóng điện từ truyền thẳng đều trong chân không với tốc độ $c$.",
      r"Quãng đường $s=ct$ · đi - về: $s=2d$",
      r"Khoảng cách thật Trái Đất - Mặt Trăng thay đổi theo quỹ đạo nên mỗi lần đo cho một giá trị riêng.",
      "⚠ <strong>Điều kiện:</strong> xung đi thẳng tới vật rồi phản xạ về đúng đường cũ; giữa hai nơi coi như chân không."]
R6 = [r"<strong>Khái niệm:</strong> $\vec E$ và $\vec B$ cùng pha nên có cùng tần số góc $\omega$ và cùng pha dao động.",
      r"<strong>Công thức:</strong> $\omega=\dfrac{2\pi}{T}$ · $E=E_0\cos(\omega t+\varphi)$",
      r"$E=0$ khi pha $=\dfrac{\pi}{2}+k\pi$ · $E=E_0$ khi pha $=k2\pi$",
      r"Thời điểm “đầu tiên kể từ $t=0$” là nghiệm dương nhỏ nhất.",
      "⚠ <strong>Điều kiện:</strong> chỉ dùng được pha của $B$ cho $E$ vì hai đại lượng cùng pha."]

SOLS = [
 sol(R1, [
  ("Nguyên nhân sinh điện trường trong dây", [P("Hai tình huống chỉ khác nhau ở chuyển động của nam châm: khi chuyển động kim lệch, khi đứng yên kim về vạch $0$."),
                                              P("Nam châm đứng yên thì từ trường qua ống dây vẫn còn nhưng không đổi theo thời gian, nên không có dòng điện."),
                                              A("T:Nguyên nhân là <strong>từ trường biến thiên</strong> theo thời gian, không phải độ mạnh của từ trường.")]),
  ("Dạng đường sức", [P("Điện trường này không do điện tích nào gây ra mà do từ trường biến thiên sinh ra, nên đường sức không có điểm đầu hay điểm cuối."),
                      A("T:Đường sức là <strong>đường cong kín, bao quanh các đường cảm ứng từ</strong>.")]),
  ("Kiểm tra", [P(r"Nam châm dừng lại: $\vec B$ không đổi, không có điện trường xoáy, kim về vạch $0$ ✓."),
                P("Thả nam châm nhanh hơn thì từ trường biến thiên nhanh hơn, kim lệch mạnh hơn: đúng với thí nghiệm nam châm rơi qua ống dây ✓.")])],
  ["a) Từ trường biến thiên theo thời gian", "b) Đường cong kín, bao quanh các đường cảm ứng từ"],
  "Nhận dạng: đề cho <strong>dòng điện chỉ xuất hiện khi nam châm chuyển động</strong> → điện trường xoáy do từ trường biến thiên, đường sức khép kín."),
 sol(R2, [
  ("Bước sóng của sóng FM", [P(r"Đổi tần số ra Hz: $f=91\ \text{MHz}=9{,}1\cdot10^{7}\ \text{Hz}$."), M(r"\lambda=\dfrac{c}{f}"), M(r"\lambda=\dfrac{3\cdot10^{8}}{9{,}1\cdot10^{7}}"), A(r"\lambda\approx3{,}30\ \text{m}")]),
  ("Chu kì của sóng FM", [M(r"T=\dfrac{1}{f}"), M(r"T=\dfrac{1}{9{,}1\cdot10^{7}}\approx1{,}10\cdot10^{-8}\ \text{s}"), A(r"T\approx11{,}0\ \text{ns}")]),
  ("Tần số của sóng hồng ngoại", [P(r"Đổi bước sóng ra mét: $\lambda=940\ \text{nm}=9{,}4\cdot10^{-7}\ \text{m}$."), M(r"f=\dfrac{c}{\lambda}"), M(r"f=\dfrac{3\cdot10^{8}}{9{,}4\cdot10^{-7}}"), A(r"f\approx3{,}19\cdot10^{14}\ \text{Hz}")]),
  ("Kiểm tra", [P(r"Với sóng FM: $\lambda=cT=3\cdot10^{8}\cdot1{,}10\cdot10^{-8}\approx3{,}3$ m, khớp bước 1 ✓."),
                P("Tia hồng ngoại có bước sóng ngắn hơn sóng FM hàng triệu lần nên tần số lớn hơn hàng triệu lần ✓.")])],
  [r"a) $\lambda\approx3{,}30\ \text{m}$", r"b) $T\approx11{,}0\ \text{ns}$", r"c) $f\approx3{,}19\cdot10^{14}\ \text{Hz}$"],
  r"Nhận dạng: đề cho <strong>tần số hoặc bước sóng</strong> của sóng điện từ → liên hệ qua tốc độ $c$, đổi MHz, nm về Hz, m trước."),
 sol(R3, [
  ("Cảm ứng từ khi E = 6,0 V/m", [P("Hai vectơ cùng pha nên tỉ số giữa giá trị tức thời và giá trị cực đại của chúng bằng nhau:"), M(r"\dfrac{B}{B_0}=\dfrac{E}{E_0}"),
                                  M(r"B=B_0\dfrac{E}{E_0}=60\cdot\dfrac{6{,}0}{18}"), A(r"B=20\ \text{nT}")]),
  ("Điện trường khi B = 45 nT", [P("Dùng lại tỉ lệ trên, giải ra $E$:"), M(r"E=E_0\dfrac{B}{B_0}=18\cdot\dfrac{45}{60}"), A(r"E=13{,}5\ \text{V/m}")]),
  ("Cảm ứng từ khi E = 0", [P(r"Với $E=0$ thì $\dfrac{E}{E_0}=0$, nên:"), M(r"B=B_0\cdot0"), A(r"B=0\ \text{nT}")]),
  ("Kiểm tra", [P(r"Tỉ số $\dfrac{B}{B_0}=\dfrac{20}{60}=\dfrac{6{,}0}{18}=\dfrac13$ ✓ và $\dfrac{E}{E_0}=\dfrac{13{,}5}{18}=\dfrac{45}{60}=0{,}75$ ✓."),
                P("Cả hai giá trị tính được đều nhỏ hơn giá trị cực đại tương ứng ✓.")])],
  [r"a) $B=20\ \text{nT}$", r"b) $E=13{,}5\ \text{V/m}$", r"c) $B=0$"],
  r"Nhận dạng: đề cho <strong>E hoặc B tức thời</strong> cùng $E_0$, $B_0$ → $E$, $B$ cùng pha nên $\dfrac{E}{E_0}=\dfrac{B}{B_0}$."),
 sol(R4, [
  ("Tần số của ánh sáng", [P(r"Đổi bước sóng ra mét: $\lambda_0=540\ \text{nm}=5{,}4\cdot10^{-7}\ \text{m}$."), M(r"f=\dfrac{c}{\lambda_0}"), M(r"f=\dfrac{3\cdot10^{8}}{5{,}4\cdot10^{-7}}"), A(r"f\approx5{,}56\cdot10^{14}\ \text{Hz}")]),
  ("Tốc độ trong nước", [M(r"v=\dfrac{c}{n}"), M(r"v=\dfrac{3\cdot10^{8}}{4/3}"), A(r"v=2{,}25\cdot10^{8}\ \text{m/s}")]),
  ("Bước sóng trong nước", [P("Tần số không đổi khi sóng đổi môi trường, nên dùng $f$ ở bước 1 với $v$ của nước:"), M(r"\lambda'=\dfrac{v}{f}"), M(r"\lambda'=\dfrac{2{,}25\cdot10^{8}}{5{,}56\cdot10^{14}}"), A(r"\lambda'\approx405\ \text{nm}")]),
  ("Kiểm tra", [P(r"Có thể kiểm tra bằng $\lambda'=\dfrac{\lambda_0}{n}=\dfrac{540}{4/3}=405$ nm ✓."),
                P("Bước sóng trong nước ngắn hơn trong chân không vì sóng chậm lại còn tần số giữ nguyên ✓.")])],
  [r"a) $f\approx5{,}56\cdot10^{14}\ \text{Hz}$", r"b) $v=2{,}25\cdot10^{8}\ \text{m/s}$", r"c) $\lambda'\approx405\ \text{nm}$"],
  r"Nhận dạng: đề cho <strong>sóng điện từ đi vào môi trường chiết suất $n$</strong> → $f$ giữ nguyên, $v$ và $\lambda$ đổi."),
 sol(R5, [
  ("Thời gian xung đi tới Mặt Trăng", [M(r"t_1=\dfrac{d}{c}"), M(r"t_1=\dfrac{3{,}84\cdot10^{8}}{3\cdot10^{8}}"), A(r"t_1=1{,}28\ \text{s}")]),
  ("Thời gian từ lúc phát đến lúc thu", [P("Xung đi tới Mặt Trăng rồi quay về nên quãng đường gồm hai lần khoảng cách:"), M(r"t=\dfrac{2d}{c}"), M(r"t=2t_1"), A(r"t=2{,}56\ \text{s}")]),
  ("Khoảng cách ở lần đo thứ hai", [P(r"Thời gian $t'=2{,}50\ \text{s}$ là thời gian đi - về, nên quãng đường đi - về là $s=ct'$ và khoảng cách bằng một nửa:"),
                                    M(r"d'=\dfrac{ct'}{2}"), M(r"d'=\dfrac{3\cdot10^{8}\cdot2{,}50}{2}"), A(r"d'=3{,}75\cdot10^{8}\ \text{m}")]),
  ("Kiểm tra", [P("Lần đo thứ hai có $t'\\lt t$ nên $d'\\lt d$ ✓."),
                P(r"Khoảng cách thật Trái Đất - Mặt Trăng thay đổi trong khoảng $3{,}6$ đến $4{,}1$ triệu km vì quỹ đạo hình elip; $3{,}75\cdot10^{8}$ m nằm trong khoảng đó ✓.")])],
  [r"a) $t_1=1{,}28\ \text{s}$", r"b) $t=2{,}56\ \text{s}$", r"c) $d'=3{,}75\cdot10^{8}\ \text{m}$"],
  r"Nhận dạng: đề cho <strong>thời gian từ lúc phát đến lúc thu xung phản xạ</strong> → quãng đường đi - về, khoảng cách $d=\dfrac{ct}{2}$."),
 sol(R6, [
  ("Chu kì của sóng", [P(r"Đọc tần số góc từ phương trình: $\omega=2\pi\cdot10^{8}$ rad/s."), M(r"T=\dfrac{2\pi}{\omega}"), M(r"T=\dfrac{2\pi}{2\pi\cdot10^{8}}"), A(r"T=10^{-8}\ \text{s}=10\ \text{ns}")]),
  ("Phương trình của cường độ điện trường", [P(r"$E$ cùng pha với $B$: cùng $\omega$ và cùng pha ban đầu."), A(r"E=E_0\cos\left(2\pi\cdot10^{8}t+\dfrac{\pi}{3}\right)")]),
  ("Thời điểm đầu tiên E = 0", [P(r"Lúc $t=0$ pha là $\dfrac{\pi}{3}$ (chưa tới $\dfrac{\pi}{2}$). $E=0$ lần đầu khi pha bằng $\dfrac{\pi}{2}$:"), M(r"\omega t+\dfrac{\pi}{3}=\dfrac{\pi}{2}"),
                               M(r"t=\dfrac{\pi/6}{\omega}=\dfrac{T}{12}"), A(r"t=\dfrac{10^{-8}}{12}\approx8{,}33\cdot10^{-10}\ \text{s}\approx0{,}833\ \text{ns}")]),
  ("Thời điểm đầu tiên E cực đại", [P(r"Pha tăng dần từ $\dfrac{\pi}{3}$; nghiệm $\text{pha}=0$ nằm trước $t=0$ nên không lấy. Cực đại kế tiếp khi pha bằng $2\pi$:"), M(r"\omega t+\dfrac{\pi}{3}=2\pi"),
                                   M(r"t=\dfrac{5\pi/3}{\omega}=\dfrac{5T}{6}"), A(r"t=\dfrac{5\cdot10^{-8}}{6}\approx8{,}33\cdot10^{-9}\ \text{s}\approx8{,}33\ \text{ns}")]),
  ("Kiểm tra", [P(r"Từ lúc $E=0$ (đang giảm) đến cực đại kế tiếp mất $8{,}33-0{,}833=7{,}5$ ns $=\dfrac{3T}{4}$ ✓."),
                P("Cả hai thời điểm đều dương và nhỏ hơn một chu kì $T=10$ ns ✓.")])],
  [r"a) $T=10\ \text{ns}$", r"b) $t\approx0{,}833\ \text{ns}$", r"c) $t\approx8{,}33\ \text{ns}$"],
  r"Nhận dạng: đề cho <strong>phương trình theo thời gian</strong> và hỏi <strong>thời điểm đầu tiên</strong> → giải phương trình về pha, lấy nghiệm dương nhỏ nhất."),
]

STEPS = [
 dict(nhan_dang="Thấy <b>dòng điện chỉ xuất hiện khi nam châm chuyển động</b> → nghĩ tới <b>điện trường xoáy</b> và đường sức của nó.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Nguyên nhân sinh điện trường trong dây", "Điện trường trong dây dẫn do nguyên nhân nào gây ra?",
       loi="Cho rằng từ trường càng mạnh thì càng sinh điện trường, bỏ qua dữ kiện kim về vạch $0$ khi nam châm đứng yên.",
       lua_chon=[("Từ trường biến thiên theo thời gian tại ống dây", True),
                 ("Từ trường mạnh của nam châm", "Nếu chỉ do từ trường mạnh thì kim vẫn phải lệch khi nam châm đứng yên trong ống, nhưng thực tế kim về vạch $0$. Hãy so sánh lại hai tình huống của đề."),
                 ("Điện tích tích tụ ở hai đầu ống dây", "Điện tích đứng yên chỉ gây điện trường tĩnh, không duy trì được dòng điện chạy vòng quanh mạch kín; ở đây không có nguồn điện tích nào.")]),
  buoc("Dạng đường sức", "Đường sức của điện trường này có dạng nào?",
       loi="Vẽ đường sức đi ra từ điện tích dương rồi vào điện tích âm như điện trường tĩnh.",
       lua_chon=[("Đường cong kín, bao quanh các đường cảm ứng từ", True),
                 ("Đường cong đi ra từ điện tích dương rồi vào điện tích âm", "Đó là đường sức của điện trường tĩnh, do điện tích gây ra. Ở đây điện trường không do điện tích nào sinh ra."),
                 ("Đường cong hở, nối hai điểm ở xa vô cùng", "Đường sức hở phải bắt đầu và kết thúc ở những điểm nào đó (như trên các điện tích); ở đây không có điện tích nào.")],
       ke=[("Xét nguồn của điện trường này rồi nhớ lại dạng đường sức của loại điện trường đó", True),
           ("Chọn dạng đường sức giống điện trường của điện tích điểm", "Nguồn ở đây không phải điện tích mà là từ trường biến thiên (kết luận bước 1)."),
           ("Đo cường độ dòng điện trong ống dây rồi suy ra dạng đường sức", "Điện kế chỉ cho biết có dòng điện hay không, không cho biết hình dạng đường sức.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>tần số, bước sóng hoặc chu kì</b> của sóng điện từ → nghĩ tới <b>sóng này truyền với tốc độ nào</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Bước sóng của sóng FM", "Bước sóng của sóng FM bằng bao nhiêu mét?", r2(D2_lam), "m", 0.02,
       loi="Thế $91$ thay cho $9{,}1\\cdot10^{7}$ (quên đổi MHz ra Hz) hoặc lật ngược thành $\\dfrac{f}{c}$."),
  buoc("Chu kì của sóng FM", "Chu kì của sóng FM bằng bao nhiêu giây (nhập hệ số $a$ của kết quả $a\\cdot10^{n}$)?", r2(D2_T * 1e8, 2), "×10ⁿ s", 0.01,
       loi="Quên đổi MHz ra Hz (lấy $T=\\dfrac{1}{91}$ s) hoặc viết sai lũy thừa của 10.",
       ke=[("Lấy nghịch đảo của tần số đã đổi ra Hz", True),
           (r"$T=\dfrac{\lambda}{f}$", r"Đơn vị không phải giây (m·s). Chu kì là nghịch đảo của tần số, hoặc $T=\dfrac{\lambda}{c}$."),
           ("Lấy chu kì bằng tần số đã đổi ra Hz", "Tần số tính bằng Hz còn chu kì tính bằng giây: hai đại lượng nghịch đảo nhau, không bằng nhau.")]),
  buoc("Tần số của sóng hồng ngoại", "Tần số của sóng hồng ngoại bằng bao nhiêu Hz (nhập hệ số $a$ của kết quả $a\\cdot10^{n}$)?", r2(D2_f / 1e14), "×10ⁿ Hz", 0.02,
       loi="Giữ nguyên $940$ nm khi thế vào công thức (không đổi ra mét) nên kết quả lệch rất nhiều lần.",
       ke=[(r"Lấy $c$ chia cho bước sóng đã đổi ra mét", True),
           (r"$f=\dfrac{1}{\lambda}$", r"Thiếu tốc độ: $\dfrac{1}{\lambda}$ chỉ là nghịch đảo của độ dài, không phải tần số; phải nhân với $c$."),
           (r"$f=\dfrac{c}{\lambda}$ với $\lambda=940$ (giữ nguyên nm)", r"Phải đổi nm ra m vì $c$ tính bằng m/s.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>E hoặc B tức thời</b> cùng <b>E₀, B₀</b> → nghĩ tới <b>quan hệ giữa hai đại lượng tại cùng thời điểm</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Cảm ứng từ khi E = 6,0 V/m", "Khi E = 6,0 V/m thì B bằng bao nhiêu nT?", r2(D3_B, 1), "nT", 0.3,
       loi="Nhân $\\dfrac{E}{E_0}$ với $E_0$ thay vì $B_0$, hoặc lập tỉ lệ ngược giữa hai đại lượng."),
  buoc("Điện trường khi B = 45 nT", "Khi B = 45 nT thì E bằng bao nhiêu V/m?", r2(D3_E, 1), "V/m", 0.2,
       loi="Coi $E$ giảm khi $B$ tăng, hoặc lập tỉ lệ nghịch giữa hai đại lượng.",
       ke=[(r"Dùng lại tỉ lệ giữa giá trị tức thời và giá trị cực đại, giải ra $E$", True),
           (r"Cho tổng hai tỉ số $\dfrac{E}{E_0}+\dfrac{B}{B_0}$ bằng $1$", "Hai vectơ cùng pha nên khi một đại lượng tăng thì đại lượng kia cũng tăng, không bù trừ nhau."),
           (r"Lập tỉ lệ nghịch: $E=E_0\dfrac{B_0}{B}$", "Tỉ lệ nghịch trái với cùng pha: $B$ tăng thì $E$ cũng tăng.")]),
  buoc("Cảm ứng từ khi E = 0", "Khi E = 0 thì B bằng bao nhiêu nT?", 0, "nT", 0.5,
       loi="Dùng độ lệch pha $\\dfrac{\\pi}{2}$ của dòng và áp trên tụ điện cho sóng điện từ.",
       ke=[(r"Áp dụng tỉ lệ $\dfrac{E}{E_0}=\dfrac{B}{B_0}$ với $E=0$", True),
           (r"Dùng độ lệch pha $\dfrac{\pi}{2}$ giữa $\vec E$ và $\vec B$", r"Độ lệch pha $\dfrac{\pi}{2}$ là của dòng và áp trong mạch có tụ hoặc cuộn cảm, không phải của $\vec E$ và $\vec B$ trong sóng điện từ."),
           ("Nói không đủ dữ kiện vì chưa biết thời điểm cụ thể", "Giá trị tức thời của $E$ và $B$ ở cùng một thời điểm liên hệ với nhau, nên không cần biết thời điểm cụ thể.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>sóng điện từ đi vào môi trường chiết suất n</b> → nghĩ tới <b>đại lượng nào giữ nguyên, đại lượng nào đổi</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Tần số của ánh sáng", "Tần số của ánh sáng bằng bao nhiêu Hz (nhập hệ số $a$ của kết quả $a\\cdot10^{n}$)?", r2(D4_f / 1e14), "×10ⁿ Hz", 0.03,
       loi="Thế $540$ khi chưa đổi nm ra m, hoặc lấy $f=c\\cdot\\lambda_0$."),
  buoc("Tốc độ trong nước", "Tốc độ ánh sáng trong nước bằng bao nhiêu m/s (nhập hệ số $a$ của kết quả $a\\cdot10^{n}$)?", r2(D4_v / 1e8), "×10ⁿ m/s", 0.02,
       loi="Nhân $c$ với $n$ thay vì chia, ra tốc độ lớn hơn $c$.",
       ke=[(r"Lấy $c$ chia cho chiết suất $n$", True),
           (r"$v=n\cdot c$", r"Trong môi trường sóng chậm hơn chân không nên $v$ phải nhỏ hơn $c$, trong khi $n\cdot c$ lớn hơn $c$."),
           (r"$v=\lambda_0 f$", r"$\lambda_0 f$ bằng $c$, là tốc độ trong chân không, không phải trong nước.")]),
  buoc("Bước sóng trong nước", "Bước sóng của ánh sáng trong nước bằng bao nhiêu nm?", round(D4_lam * 1e9), "nm", 3,
       loi="Dùng $c$ của chân không thay cho $v$ của nước (ra lại đúng $540$ nm), hoặc nhân với $n$ thay vì chia.",
       ke=[(r"Lấy tốc độ trong nước chia cho tần số ở bước 1", True),
           (r"$\lambda'=\dfrac{c}{f}$", "$c$ là tốc độ trong chân không; trong nước tốc độ nhỏ hơn nên bước sóng phải khác."),
           (r"$\lambda'=n\lambda_0$", "Sóng chậm lại trong nước nên bước sóng ngắn đi, không dài ra.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>thời gian từ lúc phát đến lúc thu xung phản xạ</b> → nghĩ tới <b>sóng đã đi những đoạn đường nào</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Thời gian xung đi tới Mặt Trăng", "Xung đi từ Trái Đất đến Mặt Trăng mất bao nhiêu giây?", r2(D5_t1), "s", 0.01,
       loi="Nhân $d$ với $c$ thay vì chia, hoặc lật ngược thành $\\dfrac{c}{d}$."),
  buoc("Thời gian từ lúc phát đến lúc thu", "Từ lúc phát đến lúc thu xung phản xạ mất bao nhiêu giây?", r2(D5_t), "s", 0.02,
       loi="Lấy luôn thời gian một chiều, quên rằng xung còn phải quay về.",
       ke=[("Tính quãng đường xung đi cả lượt đi lẫn lượt về", True),
           ("Lấy thời gian một chiều vì sóng chỉ đi tới Mặt Trăng", "Ra-đa chỉ thu được xung sau khi nó đã phản xạ và quay về, nên khoảng thời gian đó chưa phải thời gian một chiều."),
           (r"Lấy $t=\dfrac{c}{d}$", r"Đơn vị không phải giây: $\dfrac{c}{d}$ có đơn vị 1/s.")]),
  buoc("Khoảng cách ở lần đo thứ hai", "Khoảng cách lúc đó bằng bao nhiêu mét (nhập hệ số $a$ của kết quả $a\\cdot10^{n}$)?", r2(D5_d2 / 1e8), "×10ⁿ m", 0.02,
       loi="Lấy luôn $c\\cdot t'$ làm khoảng cách, quên rằng đó là quãng đường đi - về.",
       ke=[(r"Quãng đường đi - về là $ct'$, khoảng cách bằng một nửa quãng đường đó", True),
           (r"Lấy $d'=ct'$ vì sóng truyền với tốc độ $c$", r"$ct'$ là quãng đường xung đã đi cả lượt đi lẫn lượt về, chưa phải khoảng cách tới Mặt Trăng."),
           (r"Trừ thời gian một chiều: $d'=c(t'-t_1)$", "$t'$ là thời gian cả lượt đi và lượt về ở lần đo này; không trừ đi thời gian một chiều của lần đo trước.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>phương trình theo thời gian</b> và hỏi <b>thời điểm đầu tiên</b> → nghĩ tới <b>pha dao động</b> và tính cùng pha.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Chu kì của sóng", "Chu kì của sóng bằng bao nhiêu giây (nhập hệ số $a$ của kết quả $a\\cdot10^{n}$)?", r2(D6_T * 1e8, 2), "×10ⁿ s", 0.01,
       loi="Đọc tần số góc thành tần số (lấy $T=\\dfrac{1}{\\omega}$) hoặc viết sai lũy thừa của 10."),
  buoc("Phương trình của cường độ điện trường", "Phương trình nào đúng cho cường độ điện trường E tại điểm đó?",
       loi="Cho $E$ lệch pha $\\dfrac{\\pi}{2}$ so với $B$ như dòng và áp trong mạch có tụ điện.",
       lua_chon=[(r"$E=E_0\cos\left(2\pi\cdot10^{8}t+\dfrac{\pi}{3}\right)$", True),
                 (r"$E=E_0\cos\left(2\pi\cdot10^{8}t+\dfrac{\pi}{3}+\dfrac{\pi}{2}\right)$", "Thêm $\\dfrac{\\pi}{2}$ nghĩa là lệch pha, trái với tính chất của sóng điện từ: $\\vec E$ và $\\vec B$ cùng pha."),
                 (r"$E=E_0\sin\left(2\pi\cdot10^{8}t+\dfrac{\pi}{3}\right)$", "Hàm sin của cùng đối số lệch pha $\\dfrac{\\pi}{2}$ so với hàm cos; $\\vec E$ phải cùng pha với $\\vec B$."),
                 ],
       ke=[("Dùng cùng tần số góc và cùng pha ban đầu với $B$", True),
           (r"Dùng $\varphi=0$ vì $E$ là đại lượng khác $B$", "Pha ban đầu của $E$ phải liên hệ với pha ban đầu của $B$, không tự chọn bằng $0$."),
           (r"Cộng $\dfrac{\pi}{2}$ vào pha vì $E\perp B$", "Vuông góc về phương không có nghĩa lệch pha về thời gian.")]),
  buoc("Thời điểm đầu tiên E = 0", "Thời điểm đầu tiên E = 0 là bao nhiêu giây (nhập hệ số $a$ của kết quả $a\\cdot10^{n}$)?", r2(D6_t0 * 1e10, 2), "×10ⁿ s", 0.05,
       loi="Đặt pha bằng $0$ hoặc bằng $\\pi$ (nhầm với điều kiện để $\\cos$ bằng $0$), hoặc bỏ qua pha ban đầu.",
       ke=[(r"Giải pha $=\dfrac{\pi}{2}$ và lấy nghiệm dương nhỏ nhất", True),
           (r"Đặt pha bằng $0$ vì “E bằng 0”", r"$\cos0=1$ chứ không phải $0$; $E=0$ khi $\cos$ của pha bằng $0$, tức pha $=\dfrac{\pi}{2}+k\pi$."),
           (r"Đặt $\omega t=\dfrac{\pi}{2}$ (bỏ qua pha ban đầu)", "Pha ban đầu đã có sẵn ở lúc $t=0$; bỏ nó đi thì thời điểm tìm được sai.")]),
  buoc("Thời điểm đầu tiên E cực đại", "Thời điểm đầu tiên E đạt cực đại là bao nhiêu giây (nhập hệ số $a$ của kết quả $a\\cdot10^{n}$)?", r2(D6_tmax * 1e9, 2), "×10ⁿ s", 0.05,
       loi="Đặt pha bằng $0$ ra thời điểm âm (đã qua) rồi lấy trị tuyệt đối, hoặc lấy luôn một chu kì.",
       ke=[("Tìm pha kế tiếp lớn hơn pha lúc $t=0$ mà $\\cos$ bằng $1$", True),
           ("Đặt pha bằng $0$ rồi lấy trị tuyệt đối của nghiệm", "Nghiệm đó là thời điểm trước $t=0$ (cực đại đã xảy ra); đề hỏi thời điểm đầu tiên kể từ $t=0$."),
           ("Lấy $t=T$ vì cực đại lặp lại sau mỗi chu kì", "Lúc $t=0$ pha là $\\dfrac{\\pi}{3}$, chưa phải cực đại; chu kì tính từ lúc cực đại, không phải từ $t=0$.")]),
  buoc("Kiểm tra")]),
]

# ───────────── tu_luan: ví dụ cũ chưa vào dạng (VD4 Hertz, VD8, Bài 13.1), tách từng ví dụ, tự tính lại ─────────────
assert abs(3e8 / 340 - 8.82e5) < 1e3                      # VD8: λ1/λ2 = v1/v2
assert 800e3 / 1000 == 800                                 # Bài 13.1: f_mang / f_am

def tach(h, k, muc):
    h = re.sub(r"<strong[^>]*>(Ví dụ \d+:|Bài 13\.1/)</strong>\s*", f"<strong>Bài {k}.</strong> ", h, count=1)
    m = re.search(r"<p[^>]*><strong[^>]*>Giải</strong></p>", h)
    if m: de, gi = h[:m.start()], h[m.end():]
    else:
        e = h.index("</p>") + 4; de, gi = h[:e], h[e:]
    return f'<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>{gi}</details>'

h8 = OLD[4]["body_html"]
h8 = re.sub(r"Ta có: \$[^$]*\$", r"Ta có: $v_{1}=c=3\\cdot10^{8}\\ \\text{m/s},\\ v_{2}=340\\ \\text{m/s},\\ f_{1}=f_{2}$", h8, count=1)
h8 = h8.replace("=8,82.10^{5}$", r"=8{,}82\cdot10^{5}$")
assert "v_{2}=340" in h8 and "8{,}82" in h8
h8 = h8.replace("Một sóng vô tuyến và một sóng cơ có cùng tần số, khi truyền trong không khí tốc độ hai sóng lần lượt là $300000km/s$ và $340m/s.$",
                r"Một sóng vô tuyến và một sóng cơ có cùng tần số, khi truyền trong không khí tốc độ hai sóng lần lượt là $300000\ \text{km/s}$ và $340\ \text{m/s}$.")
h13 = OLD[5]["body_html"].replace("só tần số", "có tần số").replace("ân tần", "âm tần")
h13 = re.sub(r"\$(\d+) (kHz|Hz|s)([.,]?)\$", lambda m: "$" + m.group(1) + r"\ \text{" + m.group(2) + "}$" + m.group(3), h13)
TU_LUAN = dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
               body_html=("<p>Các bài còn lại của bài học, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>"
                          + tach(h8, 1, "Dễ") + tach(h13, 2, "Trung bình") + tach(OLD[1]["body_html"].replace(" vào năm 1886", ""), 3, "Trung bình")))

if __name__ == "__main__":
    write(J, 127, "Bài 16. Điện từ trường. Mô hình sóng điện từ", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
    _d = json.load(open(J)); _d["dang_bai"][0]["form"] = "ly_thuyet"       # Dạng 1 là câu khái niệm (ngân hàng: form ly_thuyet)
    json.dump(_d, open(J, "w"), ensure_ascii=False, indent=1)
    inject(J, BUILD, ANALYSIS, SOLS, STEPS)
