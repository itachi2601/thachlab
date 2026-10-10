"""Bài tập mẫu Bài 14 "Hạt nhân và mô hình nguyên tử" (Vật lí 12) — lesson_id 15. 5 dạng (quét: ket-qua/15.quet-dang.json).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-15.py   (idempotent) → 15.json (review.checked=false cho tới khi kiểm chéo)."""
import json, os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_15 import *

J = os.path.join(HERE, "15.json")
TOP_A = "Kí hiệu hạt nhân, số nuclôn, đồng vị"
TOP_B = "Kích thước, khối lượng hạt nhân và đơn vị u"

# ═════════════ TỰ GIẢI LẠI SỐ LIỆU (độc lập với lời giải) ═════════════
NA = 6.022e23; E = 1.6e-19; U_KG = 1.66054e-27; U_MEV = 931.5
assert 63 - 29 == 34 and 82 + 124 == 206
assert [a - z for a, z in [(12, 6), (14, 6), (14, 7), (15, 7), (16, 8), (17, 8)]] == [6, 8, 7, 8, 8, 9]
_iso = [(12, 6), (14, 6), (14, 7), (15, 7), (16, 8), (17, 8)]
_pairs = [(i, j) for i in range(6) for j in range(i + 1, 6) if _iso[i][1] == _iso[j][1] and _iso[i][0] != _iso[j][0]]
assert len(_pairs) == 3
RZn = 1.2 * 64 ** (1 / 3); RU = 1.2 * 238 ** (1 / 3)
assert abs(RZn - 4.8) < 1e-9 and abs(RU - 7.4366) < 1e-3
assert abs(RU / RZn - 1.55) < 0.01 and abs((RU / RZn) ** 3 - 3.72) < 0.01 and abs(238 / 64 - 3.72) < 0.01
_n = 14 / 56; _N = _n * NA
assert abs(_n - 0.25) < 1e-12 and abs(_N / 1e23 - 1.5055) < 1e-3
assert abs(_N * 30 / 1e24 - 4.5165) < 1e-3 and abs(_N * 26 * E / 1e5 - 6.2629) < 1e-3
_x = (11.009 - 10.811) / (11.009 - 10.013)
assert abs(_x - 0.1988) < 1e-3 and abs(1 - _x - 0.8012) < 1e-3
assert abs(11.009 * U_KG / 1e-26 - 1.828) < 1e-3 and abs(11.009 * U_MEV / 1e4 - 1.0255) < 1e-3
assert abs((10.013 + 11.009) / 2 - 10.511) < 1e-9

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Đọc kí hiệu hạt nhân: đếm prôtôn, nơtron, êlectron và điện tích", topic=TOP_A,
      problem_html=r"""<p>Đồng vị bền phổ biến nhất của đồng có kí hiệu hạt nhân $^{63}_{29}\text{Cu}$. Gọi $e$ là điện tích nguyên tố.</p><ol type="a"><li>Hạt nhân này có bao nhiêu prôtôn, bao nhiêu nuclôn?</li><li>Hạt nhân này có bao nhiêu nơtron?</li><li>Nguyên tử đồng trung hoà có bao nhiêu êlectron ở vỏ? Điện tích hạt nhân bằng bao nhiêu lần $e$?</li><li>Một hạt nhân khác có $82$ prôtôn và $124$ nơtron. Tính số khối của nó và viết kí hiệu hạt nhân (nguyên tố có $Z=82$ là chì, kí hiệu $\text{Pb}$).</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Nhận ra đồng vị: cùng số prôtôn, khác số nơtron", topic=TOP_A,
      problem_html=r"""<p>Cho sáu hạt nhân: $^{12}_{6}\text{C}$, $^{14}_{6}\text{C}$, $^{14}_{7}\text{N}$, $^{15}_{7}\text{N}$, $^{16}_{8}\text{O}$, $^{17}_{8}\text{O}$.</p><ol type="a"><li>Tính số nơtron của từng hạt nhân.</li><li>Trong sáu hạt nhân này có bao nhiêu cặp đồng vị? Kể tên các cặp.</li><li>Hai hạt nhân $^{14}_{6}\text{C}$ và $^{14}_{7}\text{N}$ có phải là đồng vị của nhau không? Vì sao?</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Bán kính và thể tích hạt nhân theo số khối", topic=TOP_B,
      problem_html=r"""<p>Bán kính hạt nhân có số khối $A$ cho bởi $R=1{,}2\cdot10^{-15}\,A^{1/3}$ (m). Coi hạt nhân là hình cầu. Xét hạt nhân kẽm $^{64}_{30}\text{Zn}$ và hạt nhân urani $^{238}_{92}\text{U}$.</p><ol type="a"><li>Tính bán kính hạt nhân kẽm, theo đơn vị $10^{-15}\ \text{m}$.</li><li>Tính bán kính hạt nhân urani, theo đơn vị $10^{-15}\ \text{m}$.</li><li>Bán kính hạt nhân urani gấp bao nhiêu lần bán kính hạt nhân kẽm?</li><li>Thể tích hạt nhân urani gấp bao nhiêu lần thể tích hạt nhân kẽm?</li></ol>"""),
 dict(label="Dạng 4 · Khó · Đếm hạt trong một khối lượng chất: mol, N_A, nơtron, điện tích", topic=TOP_A,
      problem_html=r"""<p>Một mẫu sắt $^{56}_{26}\text{Fe}$ có khối lượng $14\ \text{g}$, khối lượng mol xấp xỉ $56\ \text{g/mol}$. Lấy $N_A=6{,}022\cdot10^{23}\ \text{mol}^{-1}$ và $e=1{,}6\cdot10^{-19}\ \text{C}$.</p><ol type="a"><li>Tính số mol sắt trong mẫu.</li><li>Mẫu có bao nhiêu hạt nhân sắt?</li><li>Mẫu có bao nhiêu nơtron?</li><li>Tính tổng điện tích của các prôtôn trong mẫu, theo culông.</li></ol>"""),
 dict(label="Dạng 5 · Nâng cao · Khối lượng nguyên tử trung bình: tìm tỉ lệ đồng vị, đổi u, kg, MeV/c²", topic=TOP_B,
      problem_html=r"""<p>Bo tự nhiên gồm hai đồng vị: $^{10}_{5}\text{B}$ có khối lượng nguyên tử $10{,}013\ \text{u}$ và $^{11}_{5}\text{B}$ có khối lượng nguyên tử $11{,}009\ \text{u}$. Khối lượng nguyên tử trung bình của bo tự nhiên là $10{,}811\ \text{u}$. Lấy $1\ \text{u}\approx1{,}66054\cdot10^{-27}\ \text{kg}\approx931{,}5\ \text{MeV}/c^2$.</p><ol type="a"><li>Tìm phần trăm số nguyên tử của mỗi đồng vị trong bo tự nhiên.</li><li>Tính khối lượng một nguyên tử $^{11}_{5}\text{B}$ ra kilôgam.</li><li>Tính khối lượng đó ra $\text{MeV}/c^2$.</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (⚠ chỉ nêu điều kiện; cột 3 không ghi kết luận) ═════════════
ANALYSIS = [
 [(r'"kí hiệu hạt nhân $^{63}_{29}\text{Cu}$"', r"Hai chỉ số: $63$ và $29$", r"⚠ Hai chỉ số có vị trí quy ước, không đọc đảo ngược; số êlectron chỉ gắn với nguyên tử trung hoà"),
  (r'"bao nhiêu prôtôn, bao nhiêu nuclôn"', r"Cần: số prôtôn, số nuclôn", r"Ý nghĩa chỉ số dưới và chỉ số trên của kí hiệu"),
  (r'"bao nhiêu nơtron"', r"Cần: số nơtron", r"Nuclôn gồm những loại hạt nào"),
  (r'"nguyên tử đồng trung hoà … êlectron"', r"Nguyên tử trung hoà điện", r"Điện tích của êlectron so với prôtôn"),
  (r'"điện tích hạt nhân bằng bao nhiêu lần $e$"', r"Cần: điện tích theo $e$", r"Loại hạt nào trong hạt nhân mang điện"),
  (r'"$82$ prôtôn và $124$ nơtron … số khối"', r"$Z=82$ ; $N=124$", r"Số khối đếm những hạt nào")],
 [(r'"sáu hạt nhân $^{12}_{6}\text{C}$ … $^{17}_{8}\text{O}$"', r"Sáu kí hiệu hạt nhân", r"⚠ Điều kiện để hai hạt nhân là đồng vị nằm ở định nghĩa đồng vị trong bài"),
  (r'"tính số nơtron của từng hạt nhân"', r"Cần: $N$ của sáu hạt nhân", r"Liên hệ giữa số khối, số prôtôn và số nơtron"),
  (r'"bao nhiêu cặp đồng vị"', r"Cần: số cặp", r"Định nghĩa đồng vị"),
  (r'"kể tên các cặp"', r"Cần: tên các cặp", r"Định nghĩa đồng vị"),
  (r'"$^{14}_{6}\text{C}$ và $^{14}_{7}\text{N}$ có phải đồng vị không"', r"Hai kí hiệu cho trước", r"Đối chiếu từng thông tin của hai hạt nhân với định nghĩa đồng vị")],
 [(r'"$R=1{,}2\cdot10^{-15}A^{1/3}$ (m)"', r"Công thức cho trước ; $A$ là số khối", r"⚠ Công thức thực nghiệm, cho giá trị gần đúng ; $R$ tính ra mét"),
  (r'"hạt nhân kẽm $^{64}_{30}\text{Zn}$"', r"Một trong hai chỉ số của kí hiệu", r"Số khối nằm ở vị trí nào của kí hiệu"),
  (r'"hạt nhân urani $^{238}_{92}\text{U}$"', r"Một trong hai chỉ số của kí hiệu", r"Số khối nằm ở vị trí nào của kí hiệu"),
  (r'"tính bán kính hạt nhân kẽm, urani"', r"Cần: $R_{\text{Zn}}$, $R_{\text{U}}$", r"Cách bán kính phụ thuộc vào số khối"),
  (r'"bán kính urani gấp bao nhiêu lần kẽm"', r"Cần: tỉ số hai bán kính", r"So sánh hai bán kính vừa tính"),
  (r'"coi hạt nhân là hình cầu … thể tích gấp bao nhiêu lần"', r"Cần: tỉ số hai thể tích", r"Thể tích hình cầu phụ thuộc bán kính thế nào")],
 [(r'"mẫu sắt $^{56}_{26}\text{Fe}$ có khối lượng $14$ g"', r"$m=14$ g ; hai chỉ số $56$ và $26$", r"⚠ Khối lượng mol cho theo g/mol thì khối lượng phải ở đơn vị gam"),
  (r'"khối lượng mol xấp xỉ $56$ g/mol"', r"$M\approx56$ g/mol", r"Khối lượng mol là khối lượng của một mol"),
  (r'"$N_A=6{,}022\cdot10^{23}$ mol$^{-1}$"', r"$N_A$", r"Một mol chứa bao nhiêu hạt"),
  (r'"bao nhiêu hạt nhân sắt"', r"Cần: số hạt nhân", r"Mỗi nguyên tử có bao nhiêu hạt nhân"),
  (r'"bao nhiêu nơtron"', r"Cần: số nơtron cả mẫu", r"Số nơtron của mỗi hạt nhân đọc từ kí hiệu"),
  (r'"tổng điện tích của các prôtôn … $e=1{,}6\cdot10^{-19}$ C"', r"$e=1{,}6\cdot10^{-19}$ C ; cần: $Q$", r"Điện tích mỗi prôtôn ; số prôtôn của mỗi hạt nhân")],
 [(r'"khối lượng nguyên tử $10{,}013$ u và $11{,}009$ u"', r"Khối lượng hai đồng vị", r"⚠ Khối lượng nguyên tử ghi trong bảng là con số gắn với tỉ lệ các đồng vị trong tự nhiên "),
  (r'"khối lượng nguyên tử trung bình của bo tự nhiên là $10{,}811$ u"', r"$10{,}811$ u", r"Khối lượng trung bình của một hỗn hợp nhiều loại nguyên tử"),
  (r'"phần trăm số nguyên tử của mỗi đồng vị"', r"Cần: hai tỉ lệ", r"Hai tỉ lệ liên hệ với nhau thế nào"),
  (r'"$1\ \text{u}\approx1{,}66054\cdot10^{-27}$ kg"', r"Hệ số đổi u sang kg", r"Đơn vị khối lượng nguyên tử"),
  (r'"ra kilôgam"', r"Cần: khối lượng theo kg", r"Đổi đơn vị theo hệ số đã cho"),
  (r'"$\approx931{,}5\ \text{MeV}/c^2$ … ra $\text{MeV}/c^2$"', r"Hệ số đổi u sang $\text{MeV}/c^2$", r"Đổi đơn vị theo hệ số đã cho")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = [r"<strong>Khái niệm:</strong> hạt nhân gồm prôtôn ($+e$) và nơtron (không mang điện), gọi chung là nuclôn.",
      r"<strong>Kí hiệu</strong> $^A_Z X$: $Z$ là số prôtôn, $A$ là số nuclôn (số khối).",
      r"<strong>Công thức:</strong> $N=A-Z$ là số nơtron.",
      r"⚠ <strong>Điều kiện:</strong> chỉ số dưới là $Z$, chỉ số trên là $A$ ; nguyên tử trung hoà thì số êlectron bằng số prôtôn."]
R2 = [r"<strong>Khái niệm:</strong> đồng vị là những nguyên tử cùng số prôtôn $Z$, khác số nơtron $N$ (nên khác $A$).",
      r"<strong>Công thức:</strong> $N=A-Z$ để tìm số nơtron từng hạt nhân.",
      r"Cùng $Z$ là cùng nguyên tố, cùng số êlectron, tính chất hoá học giống nhau.",
      r"⚠ <strong>Điều kiện:</strong> chỉ cùng số khối, hoặc chỉ cùng số nơtron, thì chưa phải đồng vị."]
R3 = [r"<strong>Khái niệm:</strong> hạt nhân coi là hình cầu, bán kính tăng chậm theo số khối.",
      r"<strong>Công thức:</strong> $R=1{,}2\cdot10^{-15}A^{1/3}$ (m) ; thể tích hình cầu $V=\dfrac{4}{3}\pi R^3$.",
      r"⚠ <strong>Điều kiện:</strong> $A$ là số khối (chỉ số trên) ; công thức thực nghiệm nên chỉ cho giá trị gần đúng."]
R4 = [r"<strong>Khái niệm:</strong> một mol chứa $N_A$ hạt ; khối lượng mol $M$ là khối lượng của một mol (g/mol).",
      r"<strong>Công thức:</strong> $n=\dfrac{m}{M}$ ; $N_{\text{hn}}=n\,N_A$ ; số nơtron mỗi hạt nhân $N=A-Z$.",
      r"Số hạt trong mẫu bằng số hạt nhân nhân với số hạt trong mỗi hạt nhân.",
      r"⚠ <strong>Điều kiện:</strong> $M$ tính bằng g/mol thì $m$ phải tính bằng gam."]
R5 = [r"<strong>Khái niệm:</strong> khối lượng nguyên tử trung bình của nguyên tố là trung bình theo tỉ lệ các đồng vị trong tự nhiên.",
      r"<strong>Công thức:</strong> $\bar m=x_1m_1+x_2m_2$ với $x_1+x_2=1$ ; $1\ \text{u}\approx1{,}66054\cdot10^{-27}\ \text{kg}\approx931{,}5\ \text{MeV}/c^2$.",
      r"⚠ <strong>Điều kiện:</strong> tỉ lệ tính theo số nguyên tử ; đổi đơn vị bằng cách nhân với hệ số cho sẵn."]

SOLS = [
 sol(R1, [
  ("Đọc hai chỉ số",
   [P(r"Chỉ số dưới là số prôtôn $Z$, chỉ số trên là số nuclôn $A$."), M(r"{}^{63}_{29}\text{Cu}:\quad Z=29,\quad A=63"),
    A(r"T:Hạt nhân có <strong>29 prôtôn</strong> và <strong>63 nuclôn</strong>.")]),
  ("Số nơtron",
   [P("Nuclôn gồm prôtôn và nơtron nên:"), M(r"N=A-Z=63-29"), A(r"N=34\ \text{nơtron}")]),
  ("Êlectron và điện tích hạt nhân",
   [P("Nguyên tử trung hoà nên số êlectron bằng số prôtôn. Chỉ prôtôn mang điện ($+e$), nơtron không mang điện:"),
    M(r"N_e=Z=29"), M(r"q=+Ze=+29\,e"), A(r"T:Có <strong>29 êlectron</strong> ; điện tích hạt nhân bằng <strong>$+29e$</strong>.")]),
  ("Hạt nhân có 82 prôtôn và 124 nơtron",
   [P("Số khối bằng tổng số prôtôn và số nơtron:"), M(r"A=Z+N=82+124"), A(r"A=206"),
    P(r"Chì có $Z=82$ nên kí hiệu hạt nhân là:"), A(r"{}^{206}_{82}\text{Pb}")]),
  ("Kiểm tra",
   [P(r"$29+34=63=A$ ✓ khớp số nuclôn."),
    P(r"$206-82=124$ ✓ khớp số nơtron đề cho."),
    P(r"Lấy $A$ làm điện tích hạt nhân sẽ ra $63e$ — sai vì nơtron không mang điện.")])],
  [r"a) $29$ prôtôn ; $63$ nuclôn", r"b) $34$ nơtron", r"c) $29$ êlectron ; điện tích hạt nhân $+29e$", r"d) $A=206$ ; kí hiệu $^{206}_{82}\text{Pb}$"],
  r"Nhận dạng: đề cho <strong>kí hiệu hạt nhân</strong> hoặc <strong>số prôtôn và nơtron</strong> → đọc $Z$ (dưới), $A$ (trên) và dùng $A=Z+N$."),
 sol(R2, [
  ("Số nơtron của sáu hạt nhân",
   [P(r"Dùng $N=A-Z$ cho từng hạt nhân:"),
    M(r"{}^{12}_{6}\text{C}:\ 12-6=6"), M(r"{}^{14}_{6}\text{C}:\ 14-6=8"), M(r"{}^{14}_{7}\text{N}:\ 14-7=7"),
    M(r"{}^{15}_{7}\text{N}:\ 15-7=8"), M(r"{}^{16}_{8}\text{O}:\ 16-8=8"), M(r"{}^{17}_{8}\text{O}:\ 17-8=9")]),
  ("Điều kiện để là đồng vị",
   [P(r"Đồng vị: hai hạt nhân <strong>cùng $Z$</strong> (cùng nguyên tố), <strong>khác $N$</strong> (nên khác $A$)."),
    P(r"Chỉ số dưới $Z$ là căn cứ đầu tiên để ghép cặp.")]),
  ("Ghép theo số prôtôn, đếm cặp",
   [P("Nhóm theo chỉ số dưới:"),
    M(r"Z=6:\ {}^{12}_{6}\text{C},\ {}^{14}_{6}\text{C}\quad(N=6;\ 8)"),
    M(r"Z=7:\ {}^{14}_{7}\text{N},\ {}^{15}_{7}\text{N}\quad(N=7;\ 8)"),
    M(r"Z=8:\ {}^{16}_{8}\text{O},\ {}^{17}_{8}\text{O}\quad(N=8;\ 9)"),
    P("Mỗi nhóm có hai hạt nhân khác $N$, tạo thành một cặp:"),
    A(r"T:Có <strong>3 cặp</strong> đồng vị: C-12 và C-14 ; N-14 và N-15 ; O-16 và O-17.")]),
  ("Hai hạt nhân cùng số khối",
   [P(r"$^{14}_{6}\text{C}$ có $Z=6$, $^{14}_{7}\text{N}$ có $Z=7$ : hai nguyên tố khác nhau, chỉ giống nhau ở số khối."),
    A(r"T:<strong>Không</strong> phải đồng vị, vì khác số prôtôn."),
    P(r"Tương tự, $^{14}_{6}\text{C}$, $^{15}_{7}\text{N}$, $^{16}_{8}\text{O}$ cùng $N=8$ nhưng khác $Z$ nên không phải đồng vị.")]),
  ("Kiểm tra",
   [P(r"Ba cặp tìm được đều cùng $Z$ ($6$, $7$, $8$) và khác $N$ ✓."),
    P(r"Các cặp cùng số khối hoặc cùng số nơtron đều khác $Z$ ✓ nên không đưa vào.")])],
  [r"a) $N=6;\ 8;\ 7;\ 8;\ 8;\ 9$", r"b) $3$ cặp : C-12 và C-14 ; N-14 và N-15 ; O-16 và O-17", r"c) Không, vì $^{14}_{6}\text{C}$ và $^{14}_{7}\text{N}$ khác số prôtôn"],
  r"Nhận dạng: đề hỏi <strong>có phải đồng vị không</strong> hoặc <strong>chọn cặp đồng vị</strong> → so $Z$ trước (phải bằng nhau), rồi mới xét $N$ khác nhau."),
 sol(R3, [
  ("Bán kính hạt nhân kẽm",
   [P(r"Số khối $A=64$ (chỉ số trên) ; $64^{1/3}=4$ vì $4^3=64$:"),
    M(r"R_{\text{Zn}}=1{,}2\cdot10^{-15}\cdot64^{1/3}=1{,}2\cdot10^{-15}\cdot4"), A(r"R_{\text{Zn}}=4{,}8\cdot10^{-15}\ \text{m}")]),
  ("Bán kính hạt nhân urani",
   [P(r"Số khối $A=238$ ; $238^{1/3}\approx6{,}197$:"),
    M(r"R_{\text{U}}=1{,}2\cdot10^{-15}\cdot238^{1/3}"), A(r"R_{\text{U}}\approx7{,}44\cdot10^{-15}\ \text{m}")]),
  ("Tỉ số hai bán kính",
   [M(r"\dfrac{R_{\text{U}}}{R_{\text{Zn}}}=\dfrac{7{,}44}{4{,}8}"), A(r"\dfrac{R_{\text{U}}}{R_{\text{Zn}}}\approx1{,}55")]),
  ("Tỉ số hai thể tích",
   [P(r"Hình cầu có $V=\dfrac{4}{3}\pi R^3$ nên $V$ tỉ lệ với $R^3$:"),
    M(r"\dfrac{V_{\text{U}}}{V_{\text{Zn}}}=\left(\dfrac{R_{\text{U}}}{R_{\text{Zn}}}\right)^3=1{,}55^3"), A(r"\dfrac{V_{\text{U}}}{V_{\text{Zn}}}\approx3{,}72")]),
  ("Kiểm tra",
   [P(r"$R\propto A^{1/3}$ nên $V\propto R^3\propto A$ : $\dfrac{238}{64}\approx3{,}72$ ✓ khớp."),
    P(r"Số khối tăng $3{,}72$ lần mà bán kính chỉ tăng $1{,}55$ lần ✓ hợp lí : bán kính tăng chậm theo căn bậc ba.")])],
  [r"a) $R_{\text{Zn}}=4{,}8\cdot10^{-15}\ \text{m}$", r"b) $R_{\text{U}}\approx7{,}44\cdot10^{-15}\ \text{m}$", r"c) Gấp khoảng $1{,}55$ lần", r"d) Gấp khoảng $3{,}72$ lần"],
  r"Nhận dạng: đề cho <strong>số khối</strong> và hỏi <strong>bán kính, tỉ số bán kính hay thể tích</strong> → $R\propto A^{1/3}$, $V\propto R^3\propto A$."),
 sol(R4, [
  ("Số mol sắt",
   [P("Khối lượng đã ở đơn vị gam, cùng đơn vị với $M$:"), M(r"n=\dfrac{m}{M}=\dfrac{14}{56}"), A(r"n=0{,}25\ \text{mol}")]),
  ("Số hạt nhân sắt",
   [P(r"Một mol chứa $N_A$ nguyên tử, mỗi nguyên tử có một hạt nhân:"), M(r"N_{\text{hn}}=n\,N_A=0{,}25\cdot6{,}022\cdot10^{23}"), A(r"N_{\text{hn}}\approx1{,}51\cdot10^{23}\ \text{hạt nhân}")]),
  ("Số nơtron trong một hạt nhân",
   [P(r"Từ kí hiệu $^{56}_{26}\text{Fe}$: $A=56$, $Z=26$."), M(r"N=A-Z=56-26"), A(r"N=30\ \text{nơtron}")]),
  ("Số nơtron trong cả mẫu",
   [P("Số nơtron cả mẫu bằng số hạt nhân nhân với số nơtron mỗi hạt nhân:"), M(r"N_{\text{nt}}=N_{\text{hn}}\cdot N=1{,}5055\cdot10^{23}\cdot30"), A(r"N_{\text{nt}}\approx4{,}52\cdot10^{24}\ \text{nơtron}")]),
  ("Tổng điện tích các prôtôn",
   [P(r"Mỗi hạt nhân có $Z=26$ prôtôn, mỗi prôtôn mang $+e$:"), M(r"Q=N_{\text{hn}}\,Z\,e=1{,}5055\cdot10^{23}\cdot26\cdot1{,}6\cdot10^{-19}"), A(r"Q\approx6{,}26\cdot10^{5}\ \text{C}")]),
  ("Kiểm tra",
   [P(r"$\dfrac{N_{\text{nt}}}{N_{\text{hn}}}=30=A-Z$ ✓."),
    P(r"Số prôtôn cả mẫu $26\cdot1{,}5055\cdot10^{23}\approx3{,}91\cdot10^{24}$, nhân $e$ ra $6{,}26\cdot10^{5}\ \text{C}$ ✓ khớp."),
    P(r"Nơtron nhiều hơn prôtôn ($30\gt26$) đúng với hạt nhân sắt ✓.")])],
  [r"a) $n=0{,}25\ \text{mol}$", r"b) $N_{\text{hn}}\approx1{,}51\cdot10^{23}$ hạt nhân", r"c) $\approx4{,}52\cdot10^{24}$ nơtron", r"d) $Q\approx6{,}26\cdot10^{5}\ \text{C}$"],
  r"Nhận dạng: đề cho <strong>khối lượng chất</strong> và hỏi <strong>số nơtron, prôtôn hay điện tích</strong> → $n=\dfrac{m}{M}$, $N_{\text{hn}}=nN_A$, rồi nhân với số hạt trong mỗi hạt nhân."),
 sol(R5, [
  ("Lập phương trình khối lượng trung bình",
   [P(r"Gọi $x$ là tỉ lệ của $^{10}_{5}\text{B}$ ; tỉ lệ của $^{11}_{5}\text{B}$ là $1-x$ vì tổng hai tỉ lệ bằng $1$:"),
    M(r"10{,}013\,x+11{,}009\,(1-x)=10{,}811")]),
  ("Tìm tỉ lệ của ¹⁰B",
   [P("Rút gọn rồi giải:"), M(r"11{,}009-0{,}996\,x=10{,}811"), M(r"x=\dfrac{11{,}009-10{,}811}{0{,}996}=\dfrac{0{,}198}{0{,}996}"),
    A(r"x\approx0{,}199=19{,}9\ \%")]),
  ("Tỉ lệ của ¹¹B",
   [P("Hai tỉ lệ cộng lại bằng $100\\ \\%$:"), M(r"1-x=100\ \%-19{,}9\ \%"), A(r"80{,}1\ \%")]),
  ("Khối lượng một nguyên tử ¹¹B ra kilôgam",
   [P(r"Nhân khối lượng theo u với số kg ứng với $1\ \text{u}$:"), M(r"m=11{,}009\cdot1{,}66054\cdot10^{-27}"), A(r"m\approx1{,}83\cdot10^{-26}\ \text{kg}")]),
  ("Khối lượng một nguyên tử ¹¹B ra MeV/c²",
   [P(r"Nhân khối lượng theo u với số $\text{MeV}/c^2$ ứng với $1\ \text{u}$:"), M(r"m=11{,}009\cdot931{,}5"), A(r"m\approx1{,}025\cdot10^{4}\ \text{MeV}/c^2")]),
  ("Kiểm tra",
   [P(r"$0{,}199\cdot10{,}013+0{,}801\cdot11{,}009\approx10{,}81$ ✓ khớp khối lượng trung bình."),
    P(r"Trung bình cộng đơn giản của hai khối lượng chỉ là $10{,}511\ \text{u}$, khác $10{,}811\ \text{u}$ vì $^{11}_{5}\text{B}$ chiếm đa số ✓."),
    P(r"$1{,}83\cdot10^{-26}\ \text{kg}$ nhỏ cỡ $10^{-26}$ kg ✓ hợp lí với khối lượng một nguyên tử.")])],
  [r"a) $^{10}_{5}\text{B}$ khoảng $19{,}9\ \%$ ; $^{11}_{5}\text{B}$ khoảng $80{,}1\ \%$", r"b) $m\approx1{,}83\cdot10^{-26}\ \text{kg}$", r"c) $m\approx1{,}025\cdot10^{4}\ \text{MeV}/c^2$"],
  r"Nhận dạng: đề cho <strong>khối lượng các đồng vị và khối lượng trung bình</strong> → lập $x_1m_1+x_2m_2=\bar m$ với $x_1+x_2=1$ ; đổi u bằng hệ số cho sẵn."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>kí hiệu hạt nhân</b> hoặc <b>số prôtôn, nơtron</b> → đọc <b>Z (dưới), A (trên)</b>, dùng <b>A = Z + N</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Đọc hai chỉ số", r"Trong kí hiệu $^A_Z X$, chỉ số dưới $Z$ và chỉ số trên $A$ là gì?",
       loi=r"Đọc ngược hai chỉ số: coi chỉ số trên là số prôtôn và chỉ số dưới là số nuclôn.",
       lua_chon=[(r"$Z$ là số nuclôn, $A$ là số prôtôn", r"Đọc ngược. Số nuclôn gồm cả nơtron nên lớn hơn số prôtôn, và nó nằm ở chỉ số trên."),
                 (r"$Z$ là số prôtôn, $A$ là số nuclôn", True),
                 (r"$Z$ là số nơtron, $A$ là số prôtôn", r"Số nơtron không có chỉ số riêng trong kí hiệu mà suy ra từ $A-Z$.")]),
  buoc("Số nơtron", "Hạt nhân có bao nhiêu nơtron?", 34, "nơtron", 0,
       loi=r"Lấy luôn chỉ số trên làm số nơtron, hoặc cộng thay vì trừ hai chỉ số.",
       ke=[(r"Lấy số nuclôn trừ số prôtôn : $N=A-Z$", True),
           (r"Lấy số nuclôn cộng số prôtôn : $N=A+Z$", r"Nuclôn đã gồm cả prôtôn lẫn nơtron ; cộng thêm $Z$ là đếm prôtôn hai lần."),
           (r"Lấy luôn chỉ số trên làm số nơtron", r"Chỉ số trên là tổng nuclôn gồm cả prôtôn, chưa trừ prôtôn đi.")]),
  buoc("Êlectron và điện tích hạt nhân", r"Điện tích hạt nhân bằng bao nhiêu lần $e$?", 29, "lần e", 0,
       loi=r"Tính cả nơtron vào điện tích hạt nhân (dùng chỉ số trên thay chỉ số dưới), hoặc nghĩ nguyên tử trung hoà thì hạt nhân không mang điện.",
       ke=[(r"Chỉ prôtôn mang điện : $q=+Ze$, bằng số êlectron của nguyên tử trung hoà", True),
           (r"Cộng điện tích của mọi nuclôn : $q=+Ae$", r"Nơtron không mang điện nên không góp vào điện tích hạt nhân."),
           (r"Điện tích hạt nhân bằng $0$ vì nguyên tử trung hoà", r"Nguyên tử trung hoà vì êlectron bù lại điện dương của hạt nhân ; riêng hạt nhân vẫn mang điện dương.")]),
  buoc("Hạt nhân có 82 prôtôn và 124 nơtron", r"Số khối $A$ của hạt nhân có $82$ prôtôn và $124$ nơtron?", 206, "", 0,
       loi=r"Lấy hiệu số nơtron trừ số prôtôn, hoặc lấy luôn số prôtôn làm số khối.",
       ke=[(r"Số khối bằng tổng số prôtôn và số nơtron : $A=Z+N$", True),
           (r"Số khối bằng số nơtron trừ số prôtôn", r"Ngược chiều : $N=A-Z$ cho nơtron, còn $A$ là tổng $Z+N$."),
           (r"Số khối chính là số prôtôn", r"Số prôtôn là chỉ số dưới $Z$ ; số khối phải tính thêm nơtron.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>có phải đồng vị không</b> hoặc <b>chọn cặp đồng vị</b> → so <b>Z</b> trước (phải bằng nhau), rồi xét <b>N</b> khác nhau.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Số nơtron của sáu hạt nhân", r"Hạt nhân $^{14}_{6}\text{C}$ có bao nhiêu nơtron?", 8, "nơtron", 0,
       loi=r"Lấy số khối làm số nơtron, hoặc trừ nhầm chỉ số."),
  buoc("Điều kiện để là đồng vị", "Hai hạt nhân là đồng vị của nhau khi nào?",
       loi=r"Cho rằng cùng số khối hoặc cùng số nơtron là đủ để thành đồng vị.",
       lua_chon=[(r"Cùng số khối $A$", r"Ví dụ $^{40}_{18}\text{Ar}$ và $^{40}_{20}\text{Ca}$ cùng $A$ nhưng là hai nguyên tố khác nhau."),
                 (r"Cùng số nơtron $N$", r"Ví dụ $^{39}_{19}\text{K}$ và $^{40}_{20}\text{Ca}$ cùng $N$ nhưng là hai nguyên tố khác nhau."),
                 (r"Cùng số prôtôn $Z$, khác số nơtron $N$", True)],
       ke=[(r"Tìm điều kiện hai hạt nhân phải thoả để là đồng vị", True),
           (r"Cộng số nơtron của cả sáu hạt nhân", r"Tổng số nơtron không giúp biết hai hạt nhân nào là đồng vị của nhau."),
           (r"Xếp các hạt nhân theo số khối tăng dần", r"Cách xếp chỉ cho thứ tự ; điều kiện đồng vị nằm ở số prôtôn, không nằm ở số khối.")]),
  buoc("Ghép theo số prôtôn, đếm cặp", "Có bao nhiêu cặp đồng vị trong sáu hạt nhân?", 3, "cặp", 0,
       loi=r"Đếm cả cặp cùng số khối hoặc cùng số nơtron, hoặc bỏ sót một nhóm.",
       ke=[(r"Nhóm các hạt nhân có cùng chỉ số dưới rồi ghép cặp trong mỗi nhóm", True),
           (r"Ghép các hạt nhân có cùng số khối", r"Cùng số khối chưa chắc cùng nguyên tố nên không dùng để ghép cặp đồng vị."),
           (r"Ghép các hạt nhân có cùng số nơtron", r"Cùng số nơtron chưa chắc cùng nguyên tố nên không dùng để ghép cặp đồng vị.")]),
  buoc("Hai hạt nhân cùng số khối", r"$^{14}_{6}\text{C}$ và $^{14}_{7}\text{N}$ có phải đồng vị của nhau không?",
       loi=r"Thấy cùng số khối thì kết luận là đồng vị mà không kiểm số prôtôn.",
       lua_chon=[(r"Có, vì cùng số khối", r"Điều kiện đồng vị là cùng số prôtôn, không phải cùng số khối."),
                 (r"Không, vì khác số prôtôn", True),
                 (r"Có, vì khác số nơtron", r"Khác số nơtron chỉ là điều kiện cần ; đồng vị còn đòi cùng số prôtôn.")],
       ke=[(r"Đối chiếu cặp cùng số khối với điều kiện vừa tìm", True),
           (r"Kết luận ngay là đồng vị vì cùng số khối", r"Điều kiện đồng vị là cùng số prôtôn, không phải cùng số khối."),
           (r"Bỏ qua cặp này vì không cần xét", r"Câu c hỏi đúng về cặp này nên phải xét.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>số khối</b> và hỏi <b>bán kính, tỉ số bán kính hay thể tích</b> → <b>R ∝ A^(1/3)</b>, <b>V ∝ R³ ∝ A</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Bán kính hạt nhân kẽm", r"Bán kính hạt nhân kẽm theo đơn vị $10^{-15}\ \text{m}$?", 4.8, "×10⁻¹⁵ m", 0.05,
       loi=r"Nhân $1{,}2\cdot10^{-15}$ trực tiếp với số khối (quên lấy căn bậc ba), hoặc chia $A$ cho $3$."),
  buoc("Bán kính hạt nhân urani", r"Bán kính hạt nhân urani theo đơn vị $10^{-15}\ \text{m}$?", 7.44, "×10⁻¹⁵ m", 0.05,
       loi=r"Lấy căn bậc hai thay căn bậc ba, hoặc đổi $A^{1/3}$ thành $A/3$.",
       ke=[(r"Thế số khối của urani vào cùng công thức : $R=1{,}2\cdot10^{-15}A^{1/3}$", True),
           (r"Lấy bán kính kẽm nhân với tỉ số số khối", r"Bán kính không tỉ lệ thẳng với số khối mà với căn bậc ba của nó."),
           (r"Lấy bán kính kẽm nhân với bình phương tỉ số số khối", r"Bán kính tăng chậm hơn số khối nhiều ; nhân với $A^2$ là quá lớn, phải thế số khối vào $A^{1/3}$.")]),
  buoc("Tỉ số hai bán kính", "Bán kính hạt nhân urani gấp bao nhiêu lần của kẽm?", 1.55, "lần", 0.02,
       loi=r"Chia hai số khối rồi dừng lại, không lấy căn bậc ba.",
       ke=[(r"Lấy $R_{\text{U}}$ chia $R_{\text{Zn}}$", True),
           (r"Lấy tỉ số hai số khối", r"Bán kính tỉ lệ với căn bậc ba của số khối, không tỉ lệ thẳng với số khối."),
           (r"Lấy bình phương tỉ số hai số khối", r"Bán kính tỉ lệ với căn bậc ba của số khối, không tỉ lệ với bình phương.")]),
  buoc("Tỉ số hai thể tích", "Thể tích hạt nhân urani gấp bao nhiêu lần của kẽm?", 3.72, "lần", 0.05,
       loi=r"Cho rằng thể tích tỉ lệ với bán kính (hoặc bình phương bán kính) thay vì lập phương.",
       ke=[(r"Thể tích hình cầu tỉ lệ $R^3$ : lập phương tỉ số bán kính", True),
           (r"Thể tích tỉ lệ $R$ : lấy luôn tỉ số bán kính", r"Thể tích có ba chiều, nên phụ thuộc $R^3$ chứ không phải $R$."),
           (r"Thể tích tỉ lệ $R^2$ : bình phương tỉ số bán kính", r"$R^2$ là của diện tích mặt cầu ; thể tích cần $R^3$.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>khối lượng chất</b>, hỏi <b>số nơtron</b> → <b>n = m/M</b>, <b>N = n·N_A</b>, nhân số nơtron mỗi hạt nhân.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Số mol sắt", "Số mol sắt trong mẫu?", 0.25, "mol", 0.005,
       loi=r"Nhân $m$ với $M$ thay vì chia, hoặc đổi khối lượng sang kg mà vẫn dùng $M$ tính bằng g/mol."),
  buoc("Số hạt nhân sắt", r"Số hạt nhân sắt trong mẫu, theo đơn vị $10^{23}$?", 1.5055, "×10²³ hạt nhân", 0.02,
       loi=r"Chia $n$ cho $N_A$ (ra số rất nhỏ), hoặc quên rằng mỗi nguyên tử có đúng một hạt nhân.",
       ke=[(r"Nhân số mol với $N_A$ : $N_{\text{hn}}=n\,N_A$", True),
           (r"Chia số mol cho $N_A$ : $N_{\text{hn}}=\dfrac{n}{N_A}$", r"Ra số cực nhỏ ; một mol chứa $N_A$ hạt nên phải nhân."),
           (r"Nhân khối lượng với $N_A$ : $N_{\text{hn}}=m\,N_A$", r"Khối lượng không cho biết số hạt ; phải đi qua số mol $n=\dfrac{m}{M}$.")]),
  buoc("Số nơtron trong một hạt nhân", "Số nơtron trong mỗi hạt nhân sắt?", 30, "nơtron", 0,
       loi=r"Dùng $Z$ hoặc $A$ làm số nơtron của mỗi hạt nhân.",
       ke=[(r"Đọc kí hiệu rồi lấy số nuclôn trừ số prôtôn : $N=A-Z$", True),
           (r"Lấy số khối làm số nơtron", r"Số khối gồm cả prôtôn ; phải trừ số prôtôn."),
           (r"Lấy số prôtôn làm số nơtron", r"Số prôtôn là $Z$ ; số nơtron suy ra từ $A-Z$, hai số này khác nhau.")]),
  buoc("Số nơtron trong cả mẫu", r"Số nơtron trong cả mẫu, theo đơn vị $10^{24}$?", 4.5165, "×10²⁴ nơtron", 0.05,
       loi=r"Nhân số nơtron mỗi hạt nhân với số mol thay vì số hạt nhân.",
       ke=[(r"Nhân số hạt nhân với số nơtron mỗi hạt nhân", True),
           (r"Nhân số mol với số nơtron mỗi hạt nhân", r"Số mol chưa phải số hạt ; phải nhân với số hạt nhân."),
           (r"Chia số hạt nhân cho số nơtron mỗi hạt nhân", r"Phép chia cho ra số hạt nhân gộp, không phải số nơtron.")]),
  buoc("Tổng điện tích các prôtôn", r"Tổng điện tích các prôtôn trong mẫu, theo đơn vị $10^{5}\ \text{C}$?", 6.2629, "×10⁵ C", 0.05,
       loi=r"Dùng số khối hoặc số nơtron thay cho số prôtôn, hoặc quên nhân với $e$.",
       ke=[(r"Nhân số hạt nhân với $Z$ rồi với $e$", True),
           (r"Nhân số hạt nhân với $A$ rồi với $e$", r"$A$ là số nuclôn ; nơtron không mang điện nên chỉ đếm $Z$ prôtôn."),
           (r"Nhân số nơtron cả mẫu với $e$", r"Nơtron không mang điện, nên số nơtron không cho tổng điện tích.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>khối lượng các đồng vị và khối lượng trung bình</b> → lập <b>x₁m₁ + x₂m₂ = m̄</b> với <b>x₁ + x₂ = 1</b>.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Lập phương trình khối lượng trung bình", r"Phương trình nào đúng, với $x$ là tỉ lệ của $^{10}_{5}\text{B}$?",
       loi=r"Lấy trung bình cộng của hai khối lượng, hoặc dùng cùng một tỉ lệ $x$ cho cả hai đồng vị.",
       lua_chon=[(r"$\dfrac{10{,}013+11{,}009}{2}=10{,}811$", r"Trung bình cộng bằng $10{,}511$ u, không bằng $10{,}811$ u ; hai đồng vị không có số nguyên tử bằng nhau."),
                 (r"$10{,}013\,x+11{,}009\,x=10{,}811$", r"Dùng cùng tỉ lệ $x$ cho cả hai đồng vị ; tỉ lệ của $^{11}_{5}\text{B}$ phải là $1-x$ vì tổng hai tỉ lệ bằng $1$."),
                 (r"$10{,}013\,x+11{,}009\,(1-x)=10{,}811$", True)]),
  buoc("Tìm tỉ lệ của ¹⁰B", r"Phần trăm số nguyên tử $^{10}_{5}\text{B}$ trong bo tự nhiên?", 19.9, "%", 0.2,
       loi=r"Nhầm $x$ với tỉ lệ của đồng vị còn lại, hoặc chia sai khi giải phương trình.",
       ke=[(r"Giải phương trình vừa lập để tìm $x$", True),
           (r"Lấy $\dfrac{10{,}811-10{,}013}{10{,}013}$ làm tỉ lệ", r"Phép chia này không liên hệ với tỉ lệ số nguyên tử ; $x$ phải thoả phương trình trung bình."),
           (r"Lấy $\dfrac{10{,}811}{11{,}009}$ làm tỉ lệ", r"Đó là tỉ số hai khối lượng, không phải phần trăm số nguyên tử.")]),
  buoc("Tỉ lệ của ¹¹B", r"Phần trăm số nguyên tử $^{11}_{5}\text{B}$?", 80.1, "%", 0.2,
       loi=r"Quên rằng hai tỉ lệ cộng lại bằng $100\ \%$, hoặc lấy phần trăm của một đồng vị làm cho cả hai.",
       ke=[(r"Lấy $100\ \%$ trừ tỉ lệ của $^{10}_{5}\text{B}$", True),
           (r"Lấy tỉ lệ $^{11}_{5}\text{B}$ bằng tỉ lệ $^{10}_{5}\text{B}$", r"Hai tỉ lệ không bằng nhau nếu không thì khối lượng trung bình đã là trung bình cộng."),
           (r"Lấy tỉ lệ $^{11}_{5}\text{B}$ bằng $\dfrac{11{,}009}{10{,}811}$", r"Đó là tỉ số hai khối lượng, không phải phần trăm số nguyên tử.")]),
  buoc("Khối lượng một nguyên tử ¹¹B ra kilôgam", r"Khối lượng một nguyên tử $^{11}_{5}\text{B}$ theo đơn vị $10^{-26}\ \text{kg}$?", 1.828, "×10⁻²⁶ kg", 0.01,
       loi=r"Nhân hệ số đổi theo hướng ngược (chia), hoặc dùng số khối thay khối lượng nguyên tử.",
       ke=[(r"Nhân khối lượng theo u với số kg ứng với $1\ \text{u}$", True),
           (r"Chia khối lượng theo u cho $1{,}66054\cdot10^{-27}$", r"Phép chia ra số cỡ $10^{27}$ ; hệ số này là số kg ứng với 1 u nên phải nhân."),
           (r"Nhân với $931{,}5$ rồi đổi tiếp", r"$931{,}5$ là hệ số đổi u sang $\text{MeV}/c^2$, không phải sang kg.")]),
  buoc("Khối lượng một nguyên tử ¹¹B ra MeV/c²", r"Khối lượng đó theo đơn vị $10^{4}\ \text{MeV}/c^2$?", 1.0255, "×10⁴ MeV/c²", 0.002,
       loi=r"Lẫn $931{,}5\ \text{MeV}/c^2$ với $1{,}66054\cdot10^{-27}$ kg, hoặc nhân hai hệ số vào nhau.",
       ke=[(r"Nhân khối lượng theo u với $931{,}5\ \text{MeV}/c^2$ ứng với mỗi u", True),
           (r"Nhân khối lượng theo kg với $931{,}5$", r"$931{,}5$ là số $\text{MeV}/c^2$ ứng với 1 u ; áp vào kg thì sai đơn vị."),
           (r"Nhân khối lượng theo u với $1{,}6\cdot10^{-13}$", r"$1{,}6\cdot10^{-13}$ là số J ứng với 1 MeV, không dùng để đổi u sang $\text{MeV}/c^2$.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
write(J, 15, "Bài 14. Hạt nhân và mô hình nguyên tử", DANG, BUILD, ANALYSIS, SOLS, None)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code) — đã tự giải lại bằng Python 10/10/2026"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
