"""Bài tập mẫu Bài 23 "Điện trở. Định luật Ohm" (Vật lí 11) — lesson_id 42. 5 dạng (quét: ket-qua/42.quet-dang.json).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-42.py   (idempotent) → 42.json (review.checked=false cho tới khi kiểm chéo)."""
import json, os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_42 import *

J = os.path.join(HERE, "42.json")
TOP_A = "Điện trở. Định luật Ohm"
TOP_B = "Đường đặc trưng vôn – ampe"
TOP_C = "Điện trở phụ thuộc nhiệt độ"

# ═════════════ TỰ GIẢI LẠI SỐ LIỆU (độc lập với lời giải) ═════════════
def near(a, b, tol=1e-9): return abs(a - b) <= tol * max(1, abs(b))
# Dạng 1
_I = 24e-3; _R = 6.0 / _I; _I2 = 15 / _R
assert near(_I, 0.024) and near(_R, 250) and near(_I2, 0.060) and near(15 / 6.0, _I2 / _I)
# Dạng 2 (X điện trở thuần 1,0 kΩ; Y điện trở nhiệt NTC)
_X = [(2.0, 2.0), (4.0, 4.0), (6.0, 6.0)]; _Y = [(1.0, 0.5), (3.0, 2.0), (6.0, 6.6)]   # I theo mA
assert all(near(u / i, 1.0) for u, i in _X)
_RY = [u / i for u, i in _Y]                                   # kΩ
assert [round(r, 3) for r in _RY] == [2.0, 1.5, 0.909] and abs(_RY[0] / _RY[2] - 2.2) < 1e-9
assert _RY[0] > _RY[1] > _RY[2] and abs(6.6 / 6 - 1.1) < 1e-12
# Dạng 3
_R1 = 6.0 / 3.0e-3; _R2 = 6.0 / 1.2e-3; _I9 = 9.0 / (_R2 / 1000)   # V / kΩ = mA
assert near(_R1, 2000) and near(_R2, 5000) and near(_I9, 1.8) and near(1.8 / 1.2, 9 / 6.0)
# Dạng 4 (Pt100-kiểu: t0 = 0 °C)
_Rl = 0.89 / 5.0e-3; _q = _Rl / 100; _t = (_q - 1) / 3.9e-3 + 0
assert near(_Rl, 178) and near(_q, 1.78) and near(_t, 200)
assert near(100 * (1 + 3.9e-3 * 200), 178)
assert abs(_q / 3.9e-3 - 200) > 100          # lỗi "quên số 1" cho kết quả khác hẳn
# Dạng 5 (nicrom: α nhỏ, cho nhiệt độ → tìm R, I, I lúc bật, ρ)
_f = 1 + 0.40e-3 * (270 - 20); _Rn = 40.0 * _f; _In = 220 / _Rn; _I0 = 220 / 40.0; _rn = 1.10e-6 * _f
assert near(_f, 1.10) and near(_Rn, 44.0) and near(_In, 5.0) and near(_I0, 5.5) and near(_I0 / _In, 1.1) and near(_rn, 1.21e-6)
assert abs((270 + 273 - 20) * 0.40e-3 + 1 - _f) > 0.1        # cộng 273 vào t cho kết quả khác hẳn

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Tính điện trở và dòng điện, có đổi mA sang A", topic=TOP_A,
      problem_html=r"""<p>Một điện trở được mắc vào nguồn điều chỉnh được, nhiệt độ của nó giữ ổn định. Khi hiệu điện thế hai đầu điện trở là $6{,}0$ V, ampe kế chỉ $24$ mA.</p><ol type="a"><li>Tính điện trở $R$ theo đơn vị ôm.</li><li>Tăng hiệu điện thế của nguồn lên $15$ V. Tính cường độ dòng điện qua điện trở theo đơn vị mA.</li></ol>"""),
dict(label="Dạng 2 · Dễ · Nhận biết đường đặc trưng của điện trở thuần và của điện trở nhiệt", topic=TOP_B,
      problem_html=r"""<p>Hai linh kiện X và Y: một là điện trở thuần, một là điện trở nhiệt NTC. Mắc lần lượt từng linh kiện vào nguồn điều chỉnh được; mỗi lần đổi hiệu điện thế $U$, chờ ổn định rồi ghi cường độ dòng điện $I$.</p><div class="table-scroll"><table class="tl-table"><thead><tr><th>Linh kiện</th><th>$U$ (V)</th><th>$I$ (mA)</th></tr></thead><tbody><tr><td>X</td><td>$2{,}0$</td><td>$2{,}0$</td></tr><tr><td>X</td><td>$4{,}0$</td><td>$4{,}0$</td></tr><tr><td>X</td><td>$6{,}0$</td><td>$6{,}0$</td></tr><tr><td>Y</td><td>$1{,}0$</td><td>$0{,}50$</td></tr><tr><td>Y</td><td>$3{,}0$</td><td>$2{,}0$</td></tr><tr><td>Y</td><td>$6{,}0$</td><td>$6{,}6$</td></tr></tbody></table></div><ol type="a"><li>Tính $U/I$ ở mỗi lần đo của từng linh kiện, theo kΩ.</li><li>Linh kiện nào có đường đặc trưng vôn – ampe là đường thẳng đi qua gốc toạ độ?</li><li>Giải thích vì sao đường đặc trưng của linh kiện còn lại không có dạng đó.</li></ol>"""),
  dict(label="Dạng 3 · Trung bình · So sánh hai đường đặc trưng, trục I tính bằng mA", topic=TOP_B,
      problem_html=r"""<p>Trên cùng một hệ trục (trục ngang $U$ tính bằng V, trục đứng $I$ tính bằng mA), đường đặc trưng vôn – ampe của hai điện trở $R_1$, $R_2$ là hai đường thẳng đi qua gốc toạ độ; nhiệt độ mỗi điện trở ổn định.</p><p>Đường (1) đi qua điểm $(6{,}0\ \text{V};\ 3{,}0\ \text{mA})$.</p><p>Đường (2) đi qua điểm $(6{,}0\ \text{V};\ 1{,}2\ \text{mA})$.</p><ol type="a"><li>Tính $R_1$ và $R_2$ theo đơn vị kΩ.</li><li>Đường nào dốc hơn? Điện trở ứng với đường đó lớn hơn hay nhỏ hơn?</li><li>Đặt hiệu điện thế $9{,}0$ V vào hai đầu $R_2$. Tính cường độ dòng điện qua nó theo đơn vị mA.</li></ol>"""),
 dict(label="Dạng 4 · Trung bình · Dây kim loại: từ U, I tìm nhiệt độ; so với NTC", topic=TOP_C,
      problem_html=r"""<p>Một nhiệt kế điện trở dùng dây platin có điện trở $R_0=100\ \Omega$ ở $t_0=0\ ^\circ\text{C}$; hệ số nhiệt điện trở của platin là $\alpha=3{,}9\cdot10^{-3}\ \text{K}^{-1}$. Đưa dây vào một lò nhỏ, đặt vào hai đầu dây hiệu điện thế $0{,}89$ V thì ampe kế chỉ $5{,}0$ mA.</p><ol type="a"><li>Tính điện trở của dây khi ở trong lò.</li><li>Tính nhiệt độ của lò.</li><li>Nếu thay dây platin bằng một điện trở nhiệt NTC thì khi nhiệt độ tăng, điện trở của nó tăng hay giảm?</li></ol>"""),
dict(label="Dạng 5 · Khó · Dây nung nicrom của bàn là: điện trở khi nóng, dòng lúc cắm điện, điện trở suất", topic=TOP_C,
      problem_html=r"""<p>Dây nung của một bàn là bằng nicrom. Ở $20\ ^\circ\text{C}$, dây có điện trở $R_0=40{,}0\ \Omega$ và điện trở suất $\rho_0=1{,}10\cdot10^{-6}\ \Omega\cdot\text{m}$; hệ số nhiệt điện trở của nicrom là $\alpha=0{,}40\cdot10^{-3}\ \text{K}^{-1}$. Bàn là cắm vào mạng điện $220$ V; khi nóng ổn định, dây nung ở $270\ ^\circ\text{C}$.</p><ol type="a"><li>Tính điện trở của dây nung khi nóng ổn định.</li><li>Tính cường độ dòng điện qua dây khi đó.</li><li>Lúc vừa cắm điện, dây còn $20\ ^\circ\text{C}$. Tính dòng điện lúc đó; gấp bao nhiêu lần dòng khi nóng ổn định?</li><li>Tính điện trở suất của dây nung khi nóng ổn định.</li></ol>"""),

]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (⚠ chỉ nêu điều kiện; cột 3 không ghi công thức/kết luận) ═════════════
ANALYSIS = [
 [(r'"nhiệt độ của nó giữ ổn định"', r"Nhiệt độ không đổi", r"⚠ Điều kiện: điện trở chỉ giữ nguyên giá trị khi nhiệt độ ổn định"),
  (r'"hiệu điện thế hai đầu điện trở là $6{,}0$ V"', r"$U=6{,}0$ V", r"Hiệu điện thế hai đầu vật dẫn"),
  (r'"ampe kế chỉ $24$ mA"', r"$I=24$ mA", r"Đơn vị của cường độ dòng điện dùng trong công thức"),
  (r'"tính điện trở $R$ theo đơn vị ôm"', r"Cần: $R$ (Ω)", r"Định nghĩa điện trở"),
  (r'"tăng hiệu điện thế … lên $15$ V"', r"$U'=15$ V", r"Quan hệ giữa dòng điện, hiệu điện thế và điện trở"),
  (r'"tính cường độ dòng điện … theo đơn vị mA"', r"Cần: $I'$ (mA)", r"Định luật Ohm ; đơn vị của đáp số")],
[(r'"một là điện trở thuần, một là điện trở nhiệt NTC"', r"Hai loại linh kiện", r"⚠ Điều kiện: kết luận về dạng đường chỉ rút ra khi so các lần đo của cùng một linh kiện"),
  (r'"mỗi lần đổi $U$, chờ ổn định rồi ghi $I$"', r"Nhiều lần đo, mỗi lần chờ ổn định", r"Trạng thái của linh kiện lúc ghi số"),
  (r'"X: $(2{,}0;\,2{,}0)$, $(4{,}0;\,4{,}0)$, $(6{,}0;\,6{,}0)$"', r"Ba cặp $(U;\,I)$ của X", r"Điện trở tính từ một cặp số đo"),
  (r'"Y: $(1{,}0;\,0{,}50)$, $(3{,}0;\,2{,}0)$, $(6{,}0;\,6{,}6)$"', r"Ba cặp $(U;\,I)$ của Y", r"Điện trở tính từ một cặp số đo"),
  (r'"đường thẳng đi qua gốc toạ độ"', r"Cần: nhận dạng đồ thị", r"Điều kiện để đồ thị $I$ theo $U$ là đường thẳng qua gốc"),
  (r'"vì sao … không có dạng đó"', r"Cần: nguyên nhân", r"Đặc điểm của điện trở nhiệt")],
  [(r'"hai đường thẳng đi qua gốc toạ độ ; nhiệt độ ổn định"', r"Đồ thị $I$ theo $U$, thẳng qua gốc", r"⚠ Điều kiện: điện trở không đổi nên đọc được từ một điểm trên đường"),
  (r'"trục ngang $U$ (V), trục đứng $I$ (mA)"', r"$U$ ở trục ngang ; $I$ ở trục đứng", r"Độ dốc của đồ thị gắn với đại lượng nào"),
  (r'"Đường (1) đi qua $(6{,}0\ \text{V};\ 3{,}0\ \text{mA})$"', r"$U=6{,}0$ V ; $I_1=3{,}0$ mA", r"Đơn vị mA trong công thức điện trở"),
  (r'"Đường (2) đi qua $(6{,}0\ \text{V};\ 1{,}2\ \text{mA})$"', r"$U=6{,}0$ V ; $I_2=1{,}2$ mA", r"Đơn vị mA trong công thức điện trở"),
  (r'"tính $R_1$ và $R_2$ theo đơn vị kΩ"', r"Cần: $R_1$, $R_2$ (kΩ)", r"Định nghĩa điện trở ; bội số của ôm"),
  (r'"đường nào dốc hơn"', r"Cần: so sánh hai đường", r"Độ dốc của đường thẳng qua gốc ứng với đại lượng nào"),
  (r'"đặt hiệu điện thế $9{,}0$ V vào hai đầu $R_2$"', r"$U'=9{,}0$ V", r"Định luật Ohm")],
 [(r'"$R_0=100\ \Omega$ ở $t_0=0\ ^\circ\text{C}$"', r"$R_0=100\ \Omega$ ; $t_0=0\ ^\circ\text{C}$", r"⚠ Điều kiện: $t_0$ là nhiệt độ ứng với $R_0$, đọc từ đề, không mặc định $20\ ^\circ\text{C}$"),
  (r'"$\alpha=3{,}9\cdot10^{-3}\ \text{K}^{-1}$"', r"$\alpha$ của platin", r"Hệ số nhiệt điện trở của kim loại"),
  (r'"hiệu điện thế $0{,}89$ V"', r"$U=0{,}89$ V", r"Điện trở xác định từ hiệu điện thế và dòng điện"),
  (r'"ampe kế chỉ $5{,}0$ mA"', r"$I=5{,}0$ mA", r"Đơn vị ampe trong công thức"),
  (r'"tính điện trở của dây khi ở trong lò"', r"Cần: $R$", r"Định nghĩa điện trở"),
  (r'"tính nhiệt độ của lò"', r"Cần: $t$", r"Điện trở của kim loại phụ thuộc nhiệt độ"),
  (r'"điện trở nhiệt NTC … tăng hay giảm"', r"NTC", r"Hệ số nhiệt của điện trở nhiệt so với kim loại")],
 [(r'"ở $20\ ^\circ\text{C}$ … $R_0=40{,}0\ \Omega$ và $\rho_0=1{,}10\cdot10^{-6}\ \Omega\cdot\text{m}$"', r"$R_0$, $\rho_0$ ; $t_0=20\ ^\circ\text{C}$", r"⚠ Điều kiện: $R_0$, $\rho_0$ chỉ đúng ở $t_0$ ; ở nhiệt độ khác điện trở của dây khác"),
  (r'"$\alpha=0{,}40\cdot10^{-3}\ \text{K}^{-1}$"', r"$\alpha$ của nicrom", r"Hệ số nhiệt điện trở của kim loại"),
  (r'"mạng điện $220$ V"', r"$U=220$ V", r"Cường độ dòng điện từ hiệu điện thế và điện trở"),
  (r'"nóng ổn định, dây nung ở $270\ ^\circ\text{C}$"', r"$t=270\ ^\circ\text{C}$", r"Điện trở kim loại phụ thuộc nhiệt độ"),
  (r'"tính điện trở … cường độ dòng điện qua dây khi đó"', r"Cần: $R$ ; $I$", r"Điện trở ở nhiệt độ $t$ ; định luật Ohm"),
  (r'"lúc vừa cắm điện, dây còn $20\ ^\circ\text{C}$"', r"$t=t_0$", r"Điện trở của dây ở nhiệt độ $t_0$"),
  (r'"gấp bao nhiêu lần dòng khi nóng ổn định"', r"Cần: tỉ số hai dòng điện", r"So sánh hai dòng điện cùng hiệu điện thế"),
  (r'"điện trở suất … khi nóng ổn định"', r"Cần: $\rho$", r"Điện trở suất của kim loại theo nhiệt độ")]]

# ═════════════ LỜI GIẢI ═════════════
R1 = [r"<strong>Khái niệm:</strong> điện trở đo mức cản dòng của vật dẫn ; đơn vị ôm, $1\ \Omega=1$ V/A.",
      r"<strong>Công thức:</strong> $R=\dfrac{U}{I}$ ; định luật Ohm $I=\dfrac{U}{R}$.",
      r"Đổi đơn vị: $1\ \text{mA}=10^{-3}\ \text{A}$ ; $1\ \text{k}\Omega=10^{3}\ \Omega$.",
      r"⚠ <strong>Điều kiện:</strong> nhiệt độ ổn định thì $R$ không đổi ; thế $U$ (V), $I$ (A) rồi mới tính."]
R2 = [r"<strong>Khái niệm:</strong> đường đặc trưng vôn – ampe là đồ thị $I$ theo $U$ của linh kiện.",
      r"<strong>Công thức:</strong> $R=\dfrac{U}{I}$ tính ở từng lần đo.",
      r"Điện trở thuần: $U/I$ không đổi, đồ thị là đường thẳng qua gốc.",
      r"NTC: nóng lên thì $R$ giảm, đồ thị cong.",
      r"⚠ <strong>Điều kiện:</strong> $I$ tăng theo $U$ chưa đủ để kết luận là đường thẳng, phải xét $U/I$ có đổi không."]
R3 = [r"<strong>Khái niệm:</strong> điện trở nhiệt độ ổn định cho đường $I$ theo $U$ là đường thẳng qua gốc.",
      r"<strong>Công thức:</strong> $R=\dfrac{U}{I}$ ; độ dốc của đường $I$ theo $U$ là $\dfrac{I}{U}=\dfrac{1}{R}$.",
      r"Đổi đơn vị: $1\ \text{mA}=10^{-3}\ \text{A}$ ; $1\ \text{k}\Omega=10^{3}\ \Omega$ ; V/kΩ cho kết quả mA.",
      r"⚠ <strong>Điều kiện:</strong> trục đứng là $I$ thì độ dốc là $1/R$ ; chỉ khi trục đứng là $U$ độ dốc mới là $R$."]
R4 = [r"<strong>Khái niệm:</strong> kim loại nóng lên, ion nút mạng dao động mạnh hơn, êlectron va chạm nhiều hơn nên $R$ tăng.",
      r"<strong>Công thức:</strong> $R=\dfrac{U}{I}$ ; $R=R_0\,[1+\alpha\,(t-t_0)]$.",
      r"NTC là điện trở nhiệt có hệ số nhiệt âm.",
      r"⚠ <strong>Điều kiện:</strong> $R_0$ ứng với $t_0$ nào thì thế đúng $t_0$ đó ; đổi mA ra A trước khi tính."]
R5 = [r"<strong>Khái niệm:</strong> kim loại nóng lên thì $R$ và $\rho$ tăng, nicrom tăng rất ít vì $\alpha$ nhỏ.",
      r"<strong>Công thức:</strong> $R=R_0\,[1+\alpha\,(t-t_0)]$ và $\rho=\rho_0\,[1+\alpha\,(t-t_0)]$.",
      r"Định luật Ohm cho từng trạng thái: $I=\dfrac{U}{R}$ với $R$ ở nhiệt độ lúc đó.",
      r"⚠ <strong>Điều kiện:</strong> $R_0$, $\rho_0$ ứng với $t_0=20\ ^\circ\text{C}$.",
      r"⚠ Mỗi trạng thái (nguội, nóng) dùng điện trở của chính trạng thái ấy."]

def _br(x): return x.replace(" ; ", "<br>")
ANALYSIS = [[tuple(_br(c) for c in r) for r in rows] for rows in ANALYSIS]
_sol = sol
def sol(recall, steps, finals, note): return _sol([_br(x) for x in recall], steps, [_br(x) for x in finals], note)

SOLS = [
 sol(R1, [
  ("Đổi mA sang A",
   [P("Công thức dùng ampe nên đổi trước khi thế số:"), M(r"I=24\ \text{mA}=24\cdot10^{-3}\ \text{A}"), A(r"I=0{,}024\ \text{A}")]),
  ("Tính điện trở",
   [P("Điện trở bằng hiệu điện thế chia cường độ dòng điện:"), M(r"R=\dfrac{U}{I}"), M(r"R=\dfrac{6{,}0}{0{,}024}"), A(r"R=250\ \Omega")]),
  ("Dòng điện khi hiệu điện thế là 15 V",
   [P("Nhiệt độ ổn định nên $R$ giữ nguyên giá trị vừa tìm:"), M(r"I'=\dfrac{U'}{R}"), M(r"I'=\dfrac{15}{250}"),
    A(r"I'=0{,}060\ \text{A}=60\ \text{mA}")]),
  ("Kiểm tra",
   [P(r"$\dfrac{U'}{U}=\dfrac{15}{6{,}0}=2{,}5$ và $\dfrac{I'}{I}=\dfrac{60}{24}=2{,}5$ ✓ dòng điện tỉ lệ thuận với hiệu điện thế."),
    P(r"Đơn vị: V/A = Ω ✓."),
    P(r"$250\ \Omega$ cỡ điện trở thông dụng ✓.")])],
  [r"a) $R=250\ \Omega$ ($=0{,}25\ \text{k}\Omega$)", r"b) $I'=60\ \text{mA}$"],
  r"Nhận dạng: đề cho <strong>số chỉ mA hoặc kΩ</strong> và hỏi <strong>$R$ hoặc $I$</strong> → đổi về A, Ω rồi dùng $R=U/I$ ; $R$ không đổi khi nhiệt độ ổn định."),
 sol(R2, [
  ("Tính U/I của X",
   [P("Mỗi lần đo lấy hiệu điện thế chia cường độ dòng điện (V/mA = kΩ):"),
    M(r"R_X=\dfrac{2{,}0}{2{,}0}=1{,}0\ \text{k}\Omega"), M(r"R_X=\dfrac{4{,}0}{4{,}0}=1{,}0\ \text{k}\Omega"), M(r"R_X=\dfrac{6{,}0}{6{,}0}=1{,}0\ \text{k}\Omega"),
    A(r"T:$U/I$ của X bằng $1{,}0\ \text{k}\Omega$ ở cả ba lần đo.")]),
  ("Tính U/I của Y",
   [P("Làm tương tự cho ba lần đo của Y:"),
    M(r"R_Y=\dfrac{1{,}0}{0{,}50}=2{,}0\ \text{k}\Omega"), M(r"R_Y=\dfrac{3{,}0}{2{,}0}=1{,}5\ \text{k}\Omega"), M(r"R_Y=\dfrac{6{,}0}{6{,}6}\approx0{,}91\ \text{k}\Omega"),
    A(r"T:$U/I$ của Y giảm dần, lần đầu gấp $\dfrac{2{,}0}{0{,}91}\approx2{,}2$ lần lần cuối.")]),
  ("Dạng đường đặc trưng",
   [P(r"$U/I$ không đổi thì $I$ tỉ lệ thuận với $U$: đồ thị là đường thẳng qua gốc toạ độ."),
    A(r"T:Linh kiện <strong>X</strong> có đường đặc trưng là đường thẳng qua gốc.")]),
  ("Vì sao đường của Y không thẳng",
   [P("Dòng điện chạy qua làm Y nóng dần lên."),
    P("Y là NTC: nóng lên thì điện trở giảm, nên $U/I$ giảm khi $U$ tăng."),
    A(r"T:Đường của <strong>Y</strong> cong, độ dốc tăng dần.")]),
  ("Kiểm tra",
   [P(r"X: $\dfrac{I}{U}=1{,}0\ \text{mA/V}$ ở cả ba lần đo ✓ độ dốc không đổi."),
    P(r"Y: $\dfrac{I}{U}$ tăng từ $0{,}50$ lên $1{,}1\ \text{mA/V}$ ✓ độ dốc tăng, khớp $R$ giảm."),
    P(r"Y: $R$ lần cuối nhỏ hơn lần đầu ✓ cùng chiều với NTC nóng lên.")])],
  [r"a) X: $1{,}0\ \text{k}\Omega$ ở cả ba lần<br>Y: $2{,}0\ \text{k}\Omega$, $1{,}5\ \text{k}\Omega$, $0{,}91\ \text{k}\Omega$", r"b) Linh kiện X", r"c) Y là NTC, nóng dần khi dòng chạy qua nên $R$ giảm, $I$ không tỉ lệ thuận với $U$"],
  r"Nhận dạng: đề cho <strong>bảng $U$, $I$</strong> và hỏi <strong>dạng đồ thị</strong> → tính $U/I$ từng lần: không đổi thì thẳng qua gốc, đổi thì cong."),
 sol(R3, [
  ("Điện trở R₁",
   [P("Đổi $3{,}0$ mA ra ampe rồi lấy $U$ chia $I$:"), M(r"R_1=\dfrac{U}{I_1}=\dfrac{6{,}0}{3{,}0\cdot10^{-3}}"), M(r"R_1=2000\ \Omega"),
    A(r"R_1=2{,}0\ \text{k}\Omega")]),
  ("Điện trở R₂",
   [P("Làm tương tự với đường (2):"), M(r"R_2=\dfrac{U}{I_2}=\dfrac{6{,}0}{1{,}2\cdot10^{-3}}"), M(r"R_2=5000\ \Omega"),
    A(r"R_2=5{,}0\ \text{k}\Omega")]),
  ("So sánh độ dốc",
   [P("Trục đứng là $I$ nên độ dốc của mỗi đường là $\\dfrac{I}{U}=\\dfrac{1}{R}$:"),
    M(r"\dfrac{I_1}{U}=\dfrac{3{,}0}{6{,}0}=0{,}50\ \text{mA/V}"), M(r"\dfrac{I_2}{U}=\dfrac{1{,}2}{6{,}0}=0{,}20\ \text{mA/V}"),
    A(r"T:Đường (1) dốc hơn và ứng với điện trở <strong>nhỏ hơn</strong> ($2{,}0\ \text{k}\Omega\lt5{,}0\ \text{k}\Omega$).")]),
  ("Dòng điện qua R₂ khi U = 9,0 V",
   [P(r"$R_2$ không đổi (nhiệt độ ổn định). Với V và kΩ, kết quả ra mA:"), M(r"I=\dfrac{U'}{R_2}=\dfrac{9{,}0}{5{,}0}"), A(r"I=1{,}8\ \text{mA}")]),
  ("Kiểm tra",
   [P(r"$\dfrac{U'}{U}=\dfrac{9{,}0}{6{,}0}=1{,}5$ và $\dfrac{1{,}8}{1{,}2}=1{,}5$ ✓ tỉ lệ thuận."),
    P(r"Cùng $U=6{,}0$ V, đường có $I$ lớn hơn thì $R$ nhỏ hơn ✓ khớp kết quả."),
    P(r"Đơn vị: V/kΩ = mA ✓.")])],
  [r"a) $R_1=2{,}0\ \text{k}\Omega$ ; $R_2=5{,}0\ \text{k}\Omega$", r"b) Đường (1) dốc hơn ; điện trở ứng với nó nhỏ hơn", r"c) $I=1{,}8\ \text{mA}$"],
  r"Nhận dạng: đề cho <strong>hai đường $I$ theo $U$, trục mA</strong> và hỏi <strong>đường nào dốc hơn, $R$ lớn hơn</strong> → đổi mA ra A, tính $R=U/I$ từng điểm ; dốc hơn là $R$ nhỏ hơn."),
 sol(R4, [
  ("Điện trở của dây",
   [P("Đổi $5{,}0$ mA ra ampe rồi lấy $U$ chia $I$:"), M(r"R=\dfrac{U}{I}=\dfrac{0{,}89}{5{,}0\cdot10^{-3}}"), A(r"R=178\ \Omega")]),
  ("Tỉ số R/R₀",
   [P("So $R$ với điện trở $R_0$ ở nhiệt độ $t_0$ của đề:"), M(r"\dfrac{R}{R_0}=\dfrac{178}{100}"), A(r"\dfrac{R}{R_0}=1{,}78")]),
  ("Nhiệt độ của lò",
   [P(r"Từ $R=R_0\,[1+\alpha\,(t-t_0)]$ rút ra:"), M(r"\dfrac{R}{R_0}-1=\alpha\,(t-t_0)"),
    M(r"t-t_0=\dfrac{1{,}78-1}{3{,}9\cdot10^{-3}}=200\ \text{K}"), M(r"t=t_0+200=0+200"), A(r"t=200\ ^\circ\text{C}")]),
  ("Điện trở nhiệt NTC",
   [P("NTC có hệ số nhiệt âm, ngược với kim loại."), A(r"T:Nhiệt độ tăng thì điện trở của NTC <strong>giảm</strong>.")]),
  ("Kiểm tra",
   [P(r"Thế ngược: $R=100\,[1+3{,}9\cdot10^{-3}\cdot200]$"), M(r"R=178\ \Omega"),
    P(r"✓ khớp $R=178\ \Omega$ tính từ $U$ và $I$."),
    P(r"Đây là nguyên lí nhiệt kế điện trở: đo $R$ rồi suy ra nhiệt độ.")])],
  [r"a) $R=178\ \Omega$", r"b) $t=200\ ^\circ\text{C}$", r"c) Điện trở của NTC giảm khi nhiệt độ tăng"],
  r"Nhận dạng: đề cho <strong>$R_0$ ở $t_0$, $\alpha$</strong> và <strong>$U$, $I$ lúc nóng</strong> → $R=U/I$, rồi $(R/R_0-1)/\alpha$ ra $t-t_0$."),
 sol(R5, [
  ("Hệ số nhiệt của điện trở",
   [P(r"Độ chênh nhiệt độ lấy so với $t_0=20\ ^\circ\text{C}$:"), M(r"t-t_0=270-20=250\ \text{K}"),
    M(r"1+\alpha\,(t-t_0)=1+0{,}40\cdot10^{-3}\cdot250"), A(r"1+\alpha\,(t-t_0)=1{,}10")]),
  ("Điện trở khi nóng",
   [P(r"Nhân $R_0$ với hệ số vừa tìm:"), M(r"R=R_0\,[1+\alpha\,(t-t_0)]=40{,}0\cdot1{,}10"), A(r"R=44{,}0\ \Omega")]),
  ("Dòng điện khi nóng",
   [P(r"Dùng điện trở lúc nóng:"), M(r"I=\dfrac{U}{R}=\dfrac{220}{44{,}0}"), A(r"I=5{,}0\ \text{A}")]),
  ("Dòng điện lúc vừa cắm",
   [P(r"Dây còn $20\ ^\circ\text{C}$ nên điện trở là $R_0$, hiệu điện thế vẫn $220$ V:"), M(r"I_0=\dfrac{U}{R_0}=\dfrac{220}{40{,}0}"), A(r"I_0=5{,}5\ \text{A}"),
    P("So với dòng khi nóng ổn định:"), M(r"\dfrac{I_0}{I}=\dfrac{5{,}5}{5{,}0}=1{,}1"), A(r"T:Dòng lúc vừa cắm chỉ gấp <strong>1,1 lần</strong> dòng khi nóng, vì $\alpha$ của nicrom nhỏ.")]),
  ("Điện trở suất khi nóng",
   [P(r"$\rho$ đổi theo nhiệt độ cùng quy luật với $R$, nhân với cùng hệ số:"), M(r"\rho=\rho_0\,[1+\alpha\,(t-t_0)]=1{,}10\cdot10^{-6}\cdot1{,}10"),
    A(r"\rho=1{,}21\cdot10^{-6}\ \Omega\cdot\text{m}")]),
  ("Kiểm tra",
   [P(r"$\dfrac{R}{R_0}=\dfrac{44{,}0}{40{,}0}=1{,}10=\dfrac{\rho}{\rho_0}$ ✓ cùng hệ số nhân."),
    P(r"$R$ lúc nguội nhỏ hơn nên $I_0\gt I$ ✓."),
    P(r"Dòng $5{,}0$ A với $220$ V cho công suất cỡ nghìn oát, hợp lí với bàn là ✓.")])],
  [r"a) $R=44{,}0\ \Omega$", r"b) $I=5{,}0\ \text{A}$", r"c) $I_0=5{,}5\ \text{A}$, gấp $1{,}1$ lần dòng khi nóng", r"d) $\rho=1{,}21\cdot10^{-6}\ \Omega\cdot\text{m}$"],
  r"Nhận dạng: đề cho <strong>nhiệt độ dây nung</strong> và hỏi <strong>dòng lúc vừa cắm điện</strong> → tính $R$ ở nhiệt độ đó, lúc nguội dùng $R_0$ với cùng $U$."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>mA hoặc kΩ</b> trong đề, hỏi <b>R hoặc I</b> → đổi về <b>A, Ω</b> rồi dùng <b>R = U/I</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Đổi mA sang A", r"Cường độ dòng điện của ampe kế, đổi ra đơn vị ampe, bằng bao nhiêu?", 0.024, "A", 0.0005,
       loi=r"Thế thẳng số mA vào công thức mà không đổi ra ampe, kết quả lệch đi một nghìn lần."),
  buoc("Tính điện trở", r"Điện trở $R$ bằng bao nhiêu ôm?", 250, "Ω", 2,
       loi=r"Lấy $I$ chia $U$ (ra $1/R$, đơn vị A/V), hoặc nhân $U$ với $I$.",
       ke=[(r"Lấy hiệu điện thế chia cường độ dòng điện đã đổi ra ampe", True),
           (r"Lấy cường độ dòng điện chia hiệu điện thế", r"Phép chia này cho $1/R$, đơn vị A/V, không phải ôm."),
           (r"Lấy hiệu điện thế nhân cường độ dòng điện", r"Tích $U\cdot I$ có đơn vị V·A, không phải V/A của ôm.")]),
  buoc("Dòng điện khi hiệu điện thế là 15 V", r"Cường độ dòng điện khi hiệu điện thế là $15$ V, theo đơn vị mA?", 60, "mA", 0.5,
       loi=r"Cho rằng điện trở tăng cùng hiệu điện thế, hoặc nhân dòng cũ với số vôn mới.",
       ke=[(r"Giữ nguyên $R$ vừa tìm, lấy hiệu điện thế mới chia $R$", True),
           (r"Tính lại $R$ theo hiệu điện thế mới, coi $R$ tăng cùng $U$", r"$R$ do vật liệu, kích thước và nhiệt độ quyết định ; nhiệt độ ổn định thì $R$ không đổi."),
           (r"Lấy dòng điện cũ nhân với số vôn mới", r"$I$ tỉ lệ thuận với $U$, tức nhân với tỉ số hai hiệu điện thế, không nhân với số vôn.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>bảng U, I của một linh kiện</b>, hỏi <b>dạng đồ thị</b> → tính <b>U/I từng lần</b>: không đổi là thẳng qua gốc.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Tính U/I của X", r"Điện trở của X ở lần đo $U=4{,}0$ V là bao nhiêu kΩ?", 1.0, "kΩ", 0.02,
       loi=r"Lấy $I$ chia $U$ (ra $1/R$), hoặc quên rằng V chia mA cho kết quả theo kΩ."),
  buoc("Tính U/I của Y", r"Điện trở của Y ở $U=1{,}0$ V lớn gấp bao nhiêu lần ở $U=6{,}0$ V?", 2.2, "lần", 0.05,
       loi=r"Chỉ tính một lần đo của Y rồi cho rằng $R$ giữ nguyên ở các lần còn lại.",
       ke=[(r"Tính $U/I$ ở lần đo đầu và lần đo cuối của Y rồi so hai kết quả", True),
           (r"Chỉ lấy lần đo cuối, coi $R$ không đổi", r"Muốn biết $R$ có đổi không phải so các lần đo với nhau."),
           (r"Cộng các cường độ dòng điện của Y lại", r"Tổng dòng điện không cho biết $R$ ; $R$ tính từ từng cặp $U$, $I$.")]),
  buoc("Dạng đường đặc trưng", r"Linh kiện nào có đường đặc trưng vôn – ampe là đường thẳng qua gốc toạ độ?",
       loi=r"Thấy $I$ của cả hai đều tăng khi $U$ tăng liền cho rằng cả hai thẳng qua gốc.",
       lua_chon=[(r"Chỉ X", True),
                 (r"Chỉ Y", r"$U/I$ của Y thay đổi giữa các lần đo nên đường của Y không thẳng qua gốc."),
                 (r"Cả X và Y, vì $I$ của cả hai đều tăng khi $U$ tăng", r"$I$ tăng theo $U$ chưa đủ: thẳng qua gốc đòi $U/I$ không đổi.")],
       ke=[(r"So $U/I$ của từng linh kiện giữa các lần đo, rồi kết luận", True),
           (r"Chọn linh kiện có $I$ lớn nhất", r"Độ lớn của $I$ không quyết định dạng đường ; dạng đường do $U/I$ có đổi hay không."),
           (r"Chọn linh kiện có nhiều lần đo hơn", r"Số lần đo không liên quan dạng đường.")]),
  buoc("Vì sao đường của Y không thẳng", r"Điện trở của Y đổi như vậy khi $U$ tăng cho biết điều gì về Y?",
       loi=r"Cho rằng $U$ lớn hơn làm $R$ đổi theo công thức $R=U/I$: công thức chỉ là cách tính, không phải nguyên nhân.",
       lua_chon=[(r"Dòng điện làm Y nóng lên và điện trở của Y giảm khi nóng", True),
                 (r"Dòng điện làm Y nóng lên và điện trở của Y tăng khi nóng", r"Đó là tính chất của kim loại ; điện trở nhiệt NTC có hệ số nhiệt âm."),
                 (r"Hiệu điện thế lớn hơn nên điện trở nhỏ hơn ở mọi vật dẫn", r"X vẫn giữ nguyên điện trở dù hiệu điện thế đổi, nên $U$ lớn không tự làm $R$ nhỏ đi.")],
       ke=[(r"Tìm yếu tố làm điện trở của Y đổi giữa các lần đo", True),
           (r"Cho rằng dụng cụ đo sai", r"Sai số dụng cụ không làm $U/I$ giảm đều theo $U$ như vậy."),
           (r"Cho rằng Y chỉ có một điện trở cố định", r"Bảng đo cho thấy $U/I$ đổi, nên điện trở không cố định.")]),
  buoc("Kiểm tra")]),
  # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>hai đường I theo U</b>, hỏi <b>đường nào dốc hơn</b> → đổi <b>mA ra A</b>, dốc hơn là <b>R nhỏ hơn</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Điện trở R₁", r"Điện trở $R_1$ bằng bao nhiêu kΩ?", 2.0, "kΩ", 0.05,
       loi=r"Thế thẳng số mA vào công thức mà chưa đổi ra ampe, kết quả lệch đi một nghìn lần."),
  buoc("Điện trở R₂", r"Điện trở $R_2$ bằng bao nhiêu kΩ?", 5.0, "kΩ", 0.1,
       loi=r"Cho rằng $R_2=R_1$ vì cùng $U$, hoặc nhân tỉ số dòng điện thay vì chia.",
       ke=[(r"Làm như bước trước với đường (2), đổi mA ra ampe trước", True),
           (r"Lấy $R_2$ bằng $R_1$ vì cùng $U=6{,}0$ V", r"Cùng $U$ mà $I$ khác thì $R$ khác ; $R=U/I$ phải tính riêng cho từng đường."),
           (r"Lấy $R_2=R_1\cdot\dfrac{1{,}2}{3{,}0}$", r"Cùng $U$ thì $R$ tỉ lệ nghịch với $I$ ; nhân với tỉ số dòng là thuận chiều, sai.")]),
  buoc("So sánh độ dốc", r"Đường nào dốc hơn, và điện trở ứng với đường đó lớn hơn hay nhỏ hơn?",
       loi=r"Áp nhầm quy tắc của đồ thị $U$ theo $I$ cho đồ thị $I$ theo $U$.",
       lua_chon=[(r"Đường (1) dốc hơn ; điện trở ứng với nó nhỏ hơn", True),
                 (r"Đường (1) dốc hơn ; điện trở ứng với nó lớn hơn", r"Trục đứng là $I$ nên độ dốc là $1/R$: dốc hơn nghĩa là $R$ nhỏ hơn."),
                 (r"Đường (2) dốc hơn ; điện trở ứng với nó lớn hơn", r"Cùng $U$, đường (1) có $I$ lớn hơn nên đường (1) mới là đường dốc hơn.")],
       ke=[(r"So độ dốc của hai đường, nhớ độ dốc ứng với đại lượng nào của đồ thị $I$ theo $U$", True),
           (r"Áp quy tắc của đồ thị $U$ theo $I$: dốc hơn thì $R$ lớn hơn", r"Quy tắc đó chỉ đúng khi trục đứng là $U$ ; ở đây trục đứng là $I$."),
           (r"So điểm cắt trục tung của hai đường", r"Cả hai đi qua gốc nên điểm cắt giống nhau, không phân biệt được.")]),
  buoc("Dòng điện qua R₂ khi U = 9,0 V", r"Cường độ dòng điện qua $R_2$ khi đặt $9{,}0$ V là bao nhiêu mA?", 1.8, "mA", 0.03,
       loi=r"Giữ nguyên $I$ cũ vì quên rằng $U$ đã đổi, hoặc dùng $R_1$ thay cho $R_2$.",
       ke=[(r"Dùng $R_2$ vừa tìm với hiệu điện thế mới: $I=U'/R_2$", True),
           (r"Dùng $R_1$ vì hai điện trở cùng loại", r"Đề hỏi dòng qua $R_2$ ; $R_1$ là điện trở khác."),
           (r"Giữ nguyên $I=1{,}2$ mA vì $R_2$ không đổi", r"$R_2$ không đổi nhưng $U$ đổi từ $6{,}0$ V sang $9{,}0$ V nên $I$ phải đổi theo.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>R₀ ở t₀, α</b> và <b>U, I lúc nóng</b> → tính <b>R = U/I</b>, rồi <b>(R/R₀ − 1)/α</b> ra <b>t − t₀</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Điện trở của dây", r"Điện trở của dây khi ở trong lò bằng bao nhiêu ôm?", 178, "Ω", 2,
       loi=r"Thế thẳng số mA như số ampe, kết quả nhỏ đi một nghìn lần."),
  buoc("Tỉ số R/R₀", r"Tỉ số $R/R_0$ bằng bao nhiêu?", 1.78, "", 0.02,
       loi=r"Lấy $R_0/R$ (ngược), hoặc lấy hiệu $R-R_0$ rồi dừng lại.",
       ke=[(r"Lập tỉ số $R$ với $R_0$ ở nhiệt độ $t_0$ của đề", True),
           (r"Lấy $R$ cộng $R_0$", r"Cộng hai điện trở không có ý nghĩa ở đây ; công thức so $R$ với $R_0$ bằng phép chia."),
           (r"Lấy $R_0$ chia $R$", r"Ngược chiều : công thức có $R$ ở tử số.")]),
  buoc("Nhiệt độ của lò", r"Nhiệt độ của lò bằng bao nhiêu °C?", 200, "°C", 2,
       loi=r"Quên trừ $1$ ở tỉ số $R/R_0$, hoặc thế $t_0$ theo thói quen thay vì đọc $t_0$ trong đề.",
       ke=[(r"Rút $t-t_0$ từ công thức theo nhiệt độ, rồi cộng $t_0$ của đề", True),
           (r"Lấy $R/R_0$ chia $\alpha$", r"Quên số $1$ trong ngoặc: $R/R_0=1+\alpha(t-t_0)$ chứ không phải $\alpha(t-t_0)$."),
           (r"Lấy $(R-R_0)$ nhân $\alpha$", r"Nhân thay vì chia: $\alpha(t-t_0)=\dfrac{R-R_0}{R_0}$, phải chia cho $\alpha$ để tìm $t-t_0$.")]),
  buoc("Điện trở nhiệt NTC", r"Điện trở nhiệt NTC: nhiệt độ tăng thì điện trở thay đổi thế nào?",
       loi=r"Cho rằng mọi vật dẫn nóng lên đều tăng điện trở như kim loại.",
       lua_chon=[(r"Giảm", True),
                 (r"Tăng, như kim loại", r"Kim loại mới tăng ; NTC có hệ số nhiệt âm."),
                 (r"Không đổi", r"Điện trở nhiệt được chế tạo để $R$ đổi rất mạnh theo nhiệt độ.")],
       ke=[(r"Nhớ dấu hệ số nhiệt của NTC, so với kim loại", True),
           (r"Dùng luôn công thức bậc nhất với $\alpha\gt0$", r"Công thức đó với $\alpha\gt0$ là của kim loại ; NTC có hệ số nhiệt âm."),
           (r"Đo lại $U$ và $I$ của dây", r"Câu hỏi là tính chất của NTC, không cần số liệu của dây platin.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>nhiệt độ dây nung</b>, hỏi <b>dòng lúc vừa cắm điện</b> → tính <b>R ở nhiệt độ đó</b>; lúc nguội dùng <b>R₀</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Hệ số nhiệt của điện trở", r"Hệ số $1+\alpha\,(t-t_0)$ bằng bao nhiêu?", 1.10, "", 0.005,
       loi=r"Thế $t$ thay cho độ chênh $t-t_0$, hoặc cộng $273$ vào $t$ mà không cộng vào $t_0$."),
  buoc("Điện trở khi nóng", r"Điện trở của dây nung khi nóng ổn định bằng bao nhiêu ôm?", 44.0, "Ω", 0.5,
       loi=r"Cộng $R_0$ với hệ số thay vì nhân.",
       ke=[(r"Nhân $R_0$ với hệ số vừa tìm", True),
           (r"Cộng $R_0$ với hệ số vừa tìm", r"$R_0$ (ôm) và hệ số (không đơn vị) khác bản chất ; công thức nhân $R_0$ với cả ngoặc."),
           (r"Lấy $R_0$ chia hệ số", r"Dây nóng lên thì $R$ phải tăng, phép chia làm $R$ giảm.")]),
  buoc("Dòng điện khi nóng", r"Cường độ dòng điện qua dây khi nóng ổn định bằng bao nhiêu ampe?", 5.0, "A", 0.05,
       loi=r"Dùng $R_0$ thay cho điện trở lúc nóng.",
       ke=[(r"Lấy hiệu điện thế chia điện trở lúc nóng", True),
           (r"Lấy hiệu điện thế chia $R_0$", r"$R_0$ là điện trở ở $20\ ^\circ\text{C}$, không phải lúc dây đã nóng."),
           (r"Lấy điện trở chia hiệu điện thế", r"Phép chia này cho $1/I$, đơn vị Ω/V, không phải ampe.")]),
  buoc("Dòng điện lúc vừa cắm", r"Dòng điện lúc vừa cắm điện, khi dây còn $20\ ^\circ\text{C}$, bằng bao nhiêu ampe?", 5.5, "A", 0.06,
       loi=r"Dùng điện trở lúc nóng cho cả lúc nguội, ra dòng cũ.",
       ke=[(r"Dây còn $20\ ^\circ\text{C}$: dùng $R_0$ với cùng hiệu điện thế", True),
           (r"Dùng điện trở lúc nóng, vì cùng một bàn là", r"Điện trở đổi theo nhiệt độ ; lúc nguội điện trở là $R_0$, không phải điện trở lúc nóng."),
           (r"Cho rằng dòng lúc cắm phải gấp nhiều lần dòng khi nóng", r"Mức gấp bao nhiêu do $R/R_0$ quyết định, phải tính từ số liệu chứ không áp từ ví dụ khác.")]),
  buoc("Điện trở suất khi nóng", r"Điện trở suất của dây khi nóng, theo đơn vị $10^{-6}\ \Omega\cdot\text{m}$?", 1.21, "×10⁻⁶ Ω·m", 0.01,
       loi=r"Giữ $\rho=\rho_0$ vì coi điện trở suất là hằng số của nicrom.",
       ke=[(r"Nhân $\rho_0$ với cùng hệ số $1+\alpha(t-t_0)$ của điện trở", True),
           (r"Giữ $\rho=\rho_0$ vì điện trở suất là hằng số của nicrom", r"$\rho$ cũng phụ thuộc nhiệt độ, cùng quy luật với $R$."),
           (r"Tính $\rho=\dfrac{RS}{l}$ từ dữ liệu của đề", r"Đề không cho $S$ và $l$ ; đã có quy luật theo nhiệt độ của $\rho$.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
write(J, 42, "Bài 23. Điện trở. Định luật Ohm", DANG, BUILD, ANALYSIS, SOLS, None)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code) — đã tự giải lại bằng Python 10/10/2026"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
