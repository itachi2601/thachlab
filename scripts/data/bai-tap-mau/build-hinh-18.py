"""Bài tập mẫu Bài 17 "Hiện tượng phóng xạ" (Vật lí 12) — lesson_id 18. 5 dạng (quét dạng:
scripts/logs/batch-ra-soat/ket-qua/18.quet-dang.json). Hình: hinh_18.py. Bài này CHƯA có mục bai_tap_mau trong DB nên không có ví dụ cũ
(old/) và tu_luan để trống.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-18.py   (idempotent, ghi 18.json với review.checked=false)"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_18 import *

J = os.path.join(HERE, "18.json")
T228 = "Các tia phóng xạ α, β, γ"
T229 = "Định luật phóng xạ và chu kì bán rã"
T230 = "Độ phóng xạ và bài toán xác định tuổi"

# ═════════════ KHỐI ASSERT: tự giải độc lập với lời giải ═════════════
# Dạng 1: chuỗi U-238 -α-> -β⁻-> -β⁻->
A0, Z0 = 238, 92
AX, ZX = A0 - 4, Z0 - 2
AY, ZY = AX, ZX + 1
AW, ZW = AY, ZY + 1
assert (AX, ZX, AY, ZY, AW, ZW) == (234, 90, 234, 91, 234, 92)
assert ZW == Z0 and A0 - AW == 4
# Dạng 2: Po-210
N0, T2 = 6.4e18, 138
n1, n2 = 552 / T2, 759 / T2
assert n1 == 4 and n2 == 5.5
assert abs(N0 * 2 ** -n1 - 4.0e17) < 1e10 and abs((1 - 2 ** -n1) * 100 - 93.75) < 1e-9
assert abs(2 ** -n2 * 100 - 2.2097) < 1e-3
# các cách sai ra kết quả khác đáp án: trung bình 5T và 6T; làm tròn xuống n = 5; làm tròn lên n = 6; N0/n; phần còn lại thay đã phân rã
assert abs((2 ** -5 + 2 ** -6) / 2 * 100 - 2.34375) < 1e-9 and 2 ** -5 * 100 != 2 ** -n2 * 100 and 2 ** -6 * 100 != 2 ** -n2 * 100
assert N0 / n1 != N0 * 2 ** -n1 and 2 ** -n1 * 100 != (1 - 2 ** -n1) * 100 and n1 * 50 != 93.75
# Dạng 3: I-131
m0, dm, t3 = 64, 56, 24
m24 = m0 - dm
n3 = math.log2(m0 / m24)
assert m24 == 8 and n3 == 3
T3 = t3 / n3
assert T3 == 8
m40 = m0 * 2 ** -(40 / T3)
assert m40 == 2
t_c = T3 * math.log2(m0 / 0.1)
assert abs(t_c - 74.575) < 0.01 and math.ceil(t_c) == 75
assert m0 * 2 ** -9 > 0.1 > m0 * 2 ** -10         # đếm trọn chu kì cho 80 ngày, khác 74,6
assert math.log2(m0 / dm) != n3 and m0 / m24 != n3 and T3 * n3 != T3 and m24 - (40 - 24) * dm / 24 != m40   # cách sai
# Dạng 4: Co-60
NA, mC, ACo, TCo = 6.022e23, 4.0, 60, 5.27
N04 = mC / ACo * NA
Ts = TCo * 365 * 86400
lam = 0.693 / Ts
H0 = lam * N04
assert abs(N04 / 1e22 - 4.0147) < 1e-3 and abs(Ts / 1e8 - 1.66195) < 1e-4
assert abs(lam / 1e-9 - 4.1698) < 1e-3
assert abs(H0 / 1e14 - 1.6741) < 1e-3 and abs(H0 / 3.7e10 - 4524) < 2
H2 = H0 / 2 ** (10.54 / TCo) / 3.7e10
assert abs(H2 - 1131) < 1
# cách sai ≠ đúng
assert abs(N04 / Ts - H0) > 1e13 and abs(H0 / 1e11 - H0 / 3.7e10) > 1 and H0 / 2 / 3.7e10 != H2 and H0 / 3.7e10 / 2 != H2
# Dạng 5: C-14
h = 0.360 / 5.0
h0 = 0.226
r = h / h0
n5 = math.log2(h0 / h)
t5 = n5 * 5730
assert abs(h - 0.072) < 1e-9 and abs(r - 0.31858) < 1e-4 and abs(n5 - 1.65025) < 1e-4 and abs(t5 - 9456) < 2
assert 1 < n5 < 2 and abs(0.226 * 2 ** -1.65 - 0.072) < 0.001
assert abs(h0 / h - n5) > 1 and abs((1 - r) - n5) > 0.5 and abs((1 - r) * 5730 - t5) > 1000

# ═════════════ ĐỀ ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Chuỗi phân rã α, β⁻: tìm hạt nhân con", topic=T228,
      problem_html=r"""<p>Hạt nhân $^{238}_{92}\text{U}$ phóng xạ $\alpha$ và biến thành hạt nhân X. Hạt nhân X phóng xạ $\beta^-$ thành hạt nhân Y, rồi Y lại phóng xạ $\beta^-$ thành hạt nhân W.</p><ol type="a"><li>Tìm số khối và số proton của X, Y, W.</li><li>So với $^{238}_{92}\text{U}$, hạt nhân W đứng ở ô nào trong bảng tuần hoàn (cùng ô, lùi hay tiến mấy ô)? Số khối thay đổi thế nào?</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Số hạt nhân còn lại và đã phân rã sau thời gian t", topic=T229,
      problem_html=r"""<p>Một mẫu chứa $N_0=6{,}4.10^{18}$ hạt nhân poloni $^{210}_{84}\text{Po}$ phóng xạ $\alpha$ với chu kì bán rã $T=138$ ngày.</p><ol type="a"><li>Sau $552$ ngày, còn bao nhiêu hạt nhân Po chưa phân rã?</li><li>Khi đó, bao nhiêu phần trăm số hạt nhân ban đầu đã phân rã?</li><li>Sau $759$ ngày kể từ lúc đầu, số hạt nhân Po còn lại bằng bao nhiêu phần trăm số hạt nhân ban đầu?</li></ol>"""),
 dict(label="Dạng 3 · Khá · Khối lượng đã phân rã: tìm chu kì bán rã và thời gian", topic=T229,
      problem_html=r"""<p>Một mẫu iốt-131 ($^{131}_{53}\text{I}$) dùng trong y học có khối lượng ban đầu $m_0=64\ \mu\text{g}$. Sau $24$ ngày, khối lượng iốt-131 đã phân rã (biến thành hạt nhân con) là $56\ \mu\text{g}$.</p><ol type="a"><li>Tính chu kì bán rã $T$ của iốt-131.</li><li>Tính khối lượng iốt-131 chưa phân rã còn lại sau $40$ ngày kể từ lúc đầu.</li><li>Sau ít nhất bao nhiêu ngày (kể từ lúc đầu) thì khối lượng iốt-131 chưa phân rã nhỏ hơn $0{,}1\ \mu\text{g}$? Làm tròn lên đến ngày.</li></ol><p>Gợi ý: câu c cần logarit cơ số $2$; trên máy tính, $\log_2x=\dfrac{\ln x}{\ln2}$.</p>"""),
 dict(label="Dạng 4 · Khá · Độ phóng xạ của nguồn: Bq, Ci và sự giảm theo thời gian", topic=T230,
      problem_html=r"""<p>Nguồn coban-60 ($^{60}_{27}\text{Co}$) trong máy xạ trị là $4{,}0\ \text{g}$ coban-60 nguyên chất, chu kì bán rã $T=5{,}27$ năm. Lấy $1$ năm $=365$ ngày, $N_A=6{,}022.10^{23}$ hạt/mol, khối lượng mol $A=60\ \text{g/mol}$ và $\ln2=0{,}693$.</p><ol type="a"><li>Tính số hạt nhân Co-60 trong nguồn lúc đầu và hằng số phóng xạ $\lambda$ (đơn vị $1/\text{s}$).</li><li>Tính độ phóng xạ ban đầu $H_0$ theo Bq và theo Ci.</li><li>Sau $10{,}54$ năm, độ phóng xạ của nguồn còn bao nhiêu Ci?</li></ol>"""),
 dict(label="Dạng 5 · Khó · Xác định tuổi mẫu cổ bằng carbon-14", topic=T230,
      problem_html=r"""<p>Cây còn sống có độ phóng xạ của $^{14}_6\text{C}$ là $0{,}226\ \text{Bq}$ trên mỗi gam carbon. Khi cây chết, không còn carbon mới đi vào cây, và $^{14}\text{C}$ phân rã với chu kì bán rã $T=5730$ năm. Giả sử tỉ lệ $^{14}\text{C}$ trong khí quyển không đổi suốt thời gian đó và mẫu không bị nhiễm carbon mới.</p><p>Một mẩu than gỗ cổ chứa $5{,}0\ \text{g}$ carbon, đo được độ phóng xạ của $^{14}\text{C}$ trong mẩu là $0{,}360\ \text{Bq}$.</p><ol type="a"><li>Tính độ phóng xạ riêng của mẫu (Bq trên mỗi gam carbon) và tỉ số của nó so với cây sống.</li><li>Tính tuổi của mẩu than gỗ.</li><li>Nếu mẩu than thực ra bị lẫn một ít carbon hiện đại (chứa nhiều $^{14}\text{C}$ hơn mức còn lại trong mẫu cổ), tuổi tính theo cách trên lớn hơn hay nhỏ hơn tuổi thật?</li></ol>"""),
]
BUILD = [d1, d2, d3, d4, d5]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 [("\"phóng xạ $\\alpha$ … phóng xạ $\\beta^-$ … lại phóng xạ $\\beta^-$\"", "Ba phân rã nối tiếp: $\\alpha$, $\\beta^-$, $\\beta^-$", "⚠ Mỗi phương trình phân rã phải bảo toàn số khối $A$ và điện tích $Z$; hạt nhân con của lần trước là hạt nhân mẹ của lần sau"),
  ("\"$^{238}_{92}\\text{U}$ phóng xạ $\\alpha$ … hạt nhân X\"", "Mẹ: $A=238$, $Z=92$; tia $\\alpha$", "Kí hiệu hạt nhân $^A_Z\\text{X}$ (số khối trên, số proton dưới); bản chất tia $\\alpha$"),
  ("\"X phóng xạ $\\beta^-$ … hạt nhân Y\"", "Mẹ X; tia $\\beta^-$", "Bản chất và kí hiệu của tia $\\beta^-$"),
  ("\"Y lại phóng xạ $\\beta^-$ … hạt nhân W\"", "Mẹ Y; tia $\\beta^-$", "Bản chất và kí hiệu của tia $\\beta^-$"),
  ("\"Tìm số khối và số proton của X, Y, W\"", "Cần $A$, $Z$ của ba hạt nhân", "Đại lượng cần tìm"),
  ("\"So với $^{238}_{92}\\text{U}$, hạt nhân W đứng ở ô nào\"", "Cần vị trí ô và thay đổi số khối của W", "Đại lượng cần tìm")],
 [("\"hạt nhân poloni $^{210}_{84}\\text{Po}$ phóng xạ $\\alpha$\"", "Mẫu chỉ có một chất phóng xạ", "⚠ $t$ và $T$ phải cùng đơn vị thời gian; công thức chỉ cho số hạt chất mẹ còn lại, không tính hạt nhân con"),
  ("\"$N_0=6{,}4.10^{18}$ hạt nhân\"", "$N_0=6{,}4.10^{18}$", "Số hạt nhân ban đầu $N_0$"),
  ("\"chu kì bán rã $T=138$ ngày\"", "$T=138$ ngày", "Chu kì bán rã: thời gian để số hạt giảm còn một nửa"),
  ("\"Sau $552$ ngày\"", "$t_1=552$ ngày", "Thời gian phân rã $t$, cùng đơn vị với $T$"),
  ("\"còn bao nhiêu hạt nhân Po chưa phân rã\"", "Cần số hạt còn lại lúc $t_1$", "Đại lượng cần tìm"),
  ("\"bao nhiêu phần trăm số hạt nhân ban đầu đã phân rã\"", "Cần phần đã phân rã lúc $t_1$", "Đại lượng cần tìm"),
  ("\"Sau $759$ ngày … còn lại bằng bao nhiêu phần trăm\"", "$t_2=759$ ngày; cần phần còn lại", "Đại lượng cần tìm")],
 [("\"khối lượng iốt-131 đã phân rã\"", "Phần đã phân rã, không phải phần còn lại", "⚠ Công thức $2^{-t/T}$ áp dụng cho chất mẹ; đọc kĩ đề cho phần nào của mẫu"),
  ("\"khối lượng ban đầu $m_0=64\\ \\mu\\text{g}$\"", "$m_0=64\\ \\mu\\text{g}$", "Khối lượng chất mẹ lúc đầu $m_0$"),
  ("\"Sau $24$ ngày … đã phân rã là $56\\ \\mu\\text{g}$\"", "$t=24$ ngày; $\\Delta m=56\\ \\mu\\text{g}$", "Khối lượng đã phân rã $\\Delta m$ sau thời gian $t$"),
  ("\"Tính chu kì bán rã $T$\"", "Cần $T$", "Đại lượng cần tìm"),
  ("\"sau $40$ ngày … chưa phân rã còn lại\"", "$t=40$ ngày; cần khối lượng còn lại", "Đại lượng cần tìm"),
  ("\"ít nhất bao nhiêu ngày … nhỏ hơn $0{,}1\\ \\mu\\text{g}$\"", "Ngưỡng $0{,}1\\ \\mu\\text{g}$; cần $t$", "Đại lượng cần tìm")],
 [("\"$T=5{,}27$ năm … $1$ năm $=365$ ngày\"", "$T=5{,}27$ năm", "⚠ Muốn $H$ ra Bq thì $\\lambda$ phải ở đơn vị $1/\\text{s}$; $A$ lấy gần đúng bằng khối lượng mol"),
  ("\"$4{,}0\\ \\text{g}$ coban-60 nguyên chất\"", "$m_0=4{,}0\\ \\text{g}$; $A=60\\ \\text{g/mol}$", "Khối lượng mol; số Avôgađrô $N_A$"),
  ("\"$N_A=6{,}022.10^{23}$ hạt/mol, $\\ln2=0{,}693$\"", "Hằng số cho sẵn", "Số Avôgađrô; hằng số phóng xạ $\\lambda$"),
  ("\"số hạt nhân Co-60 … hằng số phóng xạ $\\lambda$\"", "Cần $N_0$, $\\lambda$", "Đại lượng cần tìm"),
  ("\"độ phóng xạ ban đầu $H_0$ theo Bq và theo Ci\"", "Cần $H_0$ ở hai đơn vị", "Đại lượng cần tìm; đơn vị Bq và Ci"),
  ("\"Sau $10{,}54$ năm\"", "$t=10{,}54$ năm; cần $H$", "Thời gian $t$, cùng đơn vị với $T$")],
 [("\"tỉ lệ $^{14}\\text{C}$ trong khí quyển không đổi … không bị nhiễm carbon mới\"", "Hai giả thiết của phép định tuổi", "⚠ Phép định tuổi chỉ đúng khi cả hai giả thiết này đúng"),
  ("\"cây còn sống … $0{,}226\\ \\text{Bq}$ trên mỗi gam carbon\"", "$h_0=0{,}226\\ \\text{Bq/g}$ (trên $1$ g carbon)", "Độ phóng xạ riêng của cây sống"),
  ("\"$T=5730$ năm\"", "$T=5730$ năm", "Chu kì bán rã của $^{14}\\text{C}$"),
  ("\"chứa $5{,}0\\ \\text{g}$ carbon, đo được … $0{,}360\\ \\text{Bq}$\"", "$m_C=5{,}0\\ \\text{g}$; $H=0{,}360\\ \\text{Bq}$ (trên $5{,}0$ g carbon)", "Khái niệm độ phóng xạ riêng"),
  ("\"Tính độ phóng xạ riêng … và tỉ số so với cây sống\"", "Cần $h$ và $\\dfrac{h}{h_0}$", "Đại lượng cần tìm"),
  ("\"Tính tuổi của mẩu than gỗ\"", "Cần $t$", "Đại lượng cần tìm"),
  ("\"bị lẫn một ít carbon hiện đại\"", "Vi phạm giả thiết không nhiễm", "Ảnh hưởng của carbon lẫn vào lên độ phóng xạ riêng đo được")],
]

# ═════════════ LỜI GIẢI ═════════════
SOLS = [
 sol([r"Tia $\alpha$ là hạt nhân $^4_2\text{He}$ ($A=4$, $Z=2$); tia $\beta^-$ là electron $^0_{-1}e$ ($A=0$, $Z=-1$).",
      r"Mỗi phương trình phân rã bảo toàn số khối $A$ (dòng trên) và điện tích $Z$ (dòng dưới).",
      r"Trong bảng tuần hoàn: $\alpha$ làm hạt nhân con lùi $2$ ô, $\beta^-$ làm hạt nhân con tiến $1$ ô.",
      r"Điều kiện: viết lần lượt từng phân rã; hạt nhân con của lần trước là hạt nhân mẹ của lần sau."],
  [("Phân rã $\\alpha$: số khối của X", [P(r"$^{238}_{92}\text{U}\to\ ^{A_X}_{Z_X}\text{X}+\ ^4_2\text{He}$"), M(r"238=A_X+4"), A(r"A_X=234")]),
   ("Phân rã $\\alpha$: số proton của X", [M(r"92=Z_X+2"), A(r"Z_X=90"), P(r"Hạt nhân $^{234}_{90}\text{X}$ là thori, lùi $2$ ô so với urani.")]),
   ("Phân rã $\\beta^-$ thứ nhất: hạt nhân Y", [P(r"$^{234}_{90}\text{X}\to\ ^{A_Y}_{Z_Y}\text{Y}+\ ^0_{-1}e$"), M(r"234=A_Y+0\Rightarrow A_Y=234"), M(r"90=Z_Y+(-1)\Rightarrow Z_Y=91"), A(r"^{234}_{91}\text{Y}"), P("Hạt nhân Y là protactini, tiến $1$ ô so với X.")]),
   ("Phân rã $\\beta^-$ thứ hai: hạt nhân W", [P(r"$^{234}_{91}\text{Y}\to\ ^{A_W}_{Z_W}\text{W}+\ ^0_{-1}e$"), M(r"234=A_W+0\Rightarrow A_W=234"), M(r"91=Z_W+(-1)\Rightarrow Z_W=92"), A(r"^{234}_{92}\text{W}"), P("Hạt nhân W là urani-234.")]),
   ("Kiểm tra", [P(r"Phân rã $\alpha$: $238=234+4$ và $92=90+2$, hai vế bằng nhau."),
                 P(r"Cả chuỗi: $\alpha$ lùi $2$ ô, hai lần $\beta^-$ tiến $1+1=2$ ô, nên W trở về đúng ô của urani."),
                 P(r"Số khối giảm đúng $4$ (chỉ hạt $\alpha$ lấy đi nuclôn), khớp $238\to234$.")])],
  [r"a) X: $A=234$, $Z=90$; Y: $A=234$, $Z=91$; W: $A=234$, $Z=92$",
   r"b) W cùng ô với $^{238}_{92}\text{U}$ (cùng số proton); số khối nhỏ hơn $4$ đơn vị"],
  r"Nhận dạng: đề cho <strong>chuỗi phân rã $\alpha$, $\beta^-$ nối tiếp</strong> → viết từng phương trình, bảo toàn $A$ và $Z$ ở mỗi lần."),

 sol([r"Số hạt nhân còn lại: $N=N_0\,2^{-t/T}=\dfrac{N_0}{2^n}$ với $n=\dfrac{t}{T}$.",
      r"Phần còn lại $\dfrac{N}{N_0}=2^{-n}$; phần đã phân rã $\dfrac{\Delta N}{N_0}=1-2^{-n}$.",
      r"Điều kiện: $t$ và $T$ cùng đơn vị (ngày); $n$ không nguyên vẫn thế được vào $2^{-n}$.",
      r"Đọc kĩ đề hỏi phần “còn lại” hay “đã phân rã”."],
  [("Số chu kì đã qua sau $552$ ngày", [M(r"n=\dfrac{t_1}{T}=\dfrac{552}{138}"), A(r"n=4")]),
   ("Số hạt nhân còn lại (câu a)", [M(r"N=\dfrac{N_0}{2^n}=\dfrac{6{,}4.10^{18}}{2^4}"), A(r"N=4{,}0.10^{17}\ \text{hạt nhân}")]),
   ("Phần trăm đã phân rã (câu b)", [M(r"\dfrac{\Delta N}{N_0}=1-2^{-4}=1-0{,}0625"), A(r"\dfrac{\Delta N}{N_0}=0{,}9375=93{,}75\%")]),
   ("Phần trăm còn lại sau $759$ ngày (câu c)", [M(r"n=\dfrac{759}{138}=5{,}5"), P(r"$n$ không nguyên vẫn thế được vào hàm mũ (dùng máy tính)."), M(r"\dfrac{N}{N_0}=2^{-5{,}5}"), A(r"\dfrac{N}{N_0}\approx0{,}0221=2{,}21\%")]),
   ("Kiểm tra", [P(r"Câu a và b: phần còn lại $\dfrac{1}{16}=6{,}25\%$, cộng $93{,}75\%$ đã phân rã được $100\%$."),
                 P(r"Câu c: sau $5$ chu kì còn $\dfrac{1}{32}=3{,}125\%$, sau $6$ chu kì còn $\dfrac{1}{64}\approx1{,}56\%$; $2{,}21\%$ nằm giữa hai mốc, khớp $n=5{,}5$.")])],
  [r"a) $N=4{,}0.10^{17}$ hạt nhân", r"b) $93{,}75\%$ số hạt nhân ban đầu đã phân rã", r"c) còn lại $\approx2{,}21\%$ số hạt nhân ban đầu"],
  r"Nhận dạng: đề cho <strong>sau thời gian $t$, chu kì bán rã $T$</strong> → áp dụng định luật phóng xạ, đọc kĩ hỏi “còn lại” hay “đã phân rã”."),

 sol([r"Chất mẹ còn lại: $m_t=m_0\,2^{-n}$ với $n=\dfrac{t}{T}$, tức $\dfrac{m_0}{m_t}=2^n$.",
      r"Khối lượng đã phân rã: $\Delta m=m_0-m_t=m_0(1-2^{-n})$.",
      r"Điều kiện: $2^{-n}$ chỉ cho phần CÒN LẠI; $n$ được phép không nguyên.",
      r"Muốn tìm $n$ từ $2^n=k$: dùng logarit cơ số $2$, $n=\log_2k$."],
  [("Khối lượng còn lại sau $24$ ngày", [M(r"m_{24}=m_0-\Delta m=64-56"), A(r"m_{24}=8\ \mu\text{g}")]),
   ("Số chu kì đã qua", [M(r"2^n=\dfrac{m_0}{m_{24}}=\dfrac{64}{8}=8"), A(r"n=3")]),
   ("Chu kì bán rã (câu a)", [M(r"T=\dfrac{t}{n}=\dfrac{24}{3}"), A(r"T=8\ \text{ngày}")]),
   ("Khối lượng còn lại sau $40$ ngày (câu b)", [M(r"n'=\dfrac{40}{T}=\dfrac{40}{8}=5"), M(r"m=\dfrac{m_0}{2^5}=\dfrac{64}{32}"), A(r"m=2\ \mu\text{g}")]),
   ("Thời gian để còn dưới $0{,}1\\ \\mu\\text{g}$ (câu c)", [M(r"m_0\,2^{-n}\lt0{,}1\Rightarrow2^n\gt\dfrac{64}{0{,}1}=640"), M(r"n\gt\log_2640\approx9{,}32"), M(r"t=nT\gt9{,}32\cdot8"), A(r"t\gt74{,}6\ \text{ngày}"), P(r"Làm tròn lên đến ngày: sau ít nhất $75$ ngày.")]),
   ("Kiểm tra", [P(r"$2^3=8$ khớp $\dfrac{64}{8}$; $T=8$ ngày đúng cỡ chu kì bán rã thực tế của iốt-131."),
                 P(r"Câu c: sau $9$ chu kì ($72$ ngày) còn $\dfrac{64}{512}=0{,}125\ \mu\text{g}\gt0{,}1$; sau $10$ chu kì ($80$ ngày) còn $0{,}0625\ \mu\text{g}$; $74{,}6$ ngày nằm giữa hai mốc."),
                 P(r"Sau $40$ ngày còn $2\ \mu\text{g}$, ít hơn $8\ \mu\text{g}$ của ngày thứ $24$: hợp lí.")])],
  [r"a) $T=8$ ngày", r"b) $m=2\ \mu\text{g}$", r"c) $t\gt74{,}6$ ngày, tức sau ít nhất $75$ ngày"],
  r"Nhận dạng: đề cho <strong>khối lượng đã phân rã</strong> và hỏi chu kì hoặc thời gian → đổi sang phần còn lại trước, rồi dùng $2^{-n}$ và logarit cơ số $2$."),

 sol([r"Số hạt nhân: $N_0=\dfrac{m_0}{A}N_A$ ($m_0$ theo g, $A$ lấy bằng khối lượng mol theo g/mol).",
      r"Hằng số phóng xạ $\lambda=\dfrac{\ln2}{T}$ với $T$ tính bằng giây; độ phóng xạ $H=\lambda N$.",
      r"$H_t=H_0\,2^{-t/T}$; $1\ \text{Ci}=3{,}7.10^{10}\ \text{Bq}$.",
      r"Điều kiện: muốn $H$ ra Bq thì $\lambda$ phải ở đơn vị $1/\text{s}$."],
  [("Số hạt nhân ban đầu (câu a)", [M(r"N_0=\dfrac{m_0}{A}N_A=\dfrac{4{,}0}{60}\cdot6{,}022.10^{23}"), A(r"N_0\approx4{,}01.10^{22}\ \text{hạt nhân}")]),
   ("Hằng số phóng xạ (câu a)", [P(r"$T=5{,}27\cdot365\cdot86\,400\approx1{,}662.10^{8}\ \text{s}$."), M(r"\lambda=\dfrac{0{,}693}{T}=\dfrac{0{,}693}{1{,}662.10^{8}}"), A(r"\lambda\approx4{,}17.10^{-9}\ \text{s}^{-1}")]),
   ("Độ phóng xạ ban đầu theo Bq (câu b)", [M(r"H_0=\lambda N_0=4{,}17.10^{-9}\cdot4{,}01.10^{22}"), P("Dùng $\\lambda$ và $N_0$ chưa làm tròn (hai số trên đã làm tròn nên tích ghi ra hơi lệch):"), A(r"H_0\approx1{,}674.10^{14}\ \text{Bq}")]),
   ("Đổi ra curi (câu b)", [M(r"H_0=\dfrac{1{,}674.10^{14}}{3{,}7.10^{10}}\ \text{Ci}"), A(r"H_0\approx4{,}52.10^{3}\ \text{Ci}")]),
   ("Độ phóng xạ sau $10{,}54$ năm (câu c)", [P(r"$n=\dfrac{10{,}54}{5{,}27}=2$, không cần tính lại $\lambda$."), M(r"H=\dfrac{H_0}{2^2}=\dfrac{4{,}52.10^{3}}{4}"), A(r"H\approx1{,}13.10^{3}\ \text{Ci}")]),
   ("Kiểm tra", [P(r"Tính cách khác: $N=\dfrac{N_0}{4}\approx1{,}004.10^{22}$ hạt, $H=\lambda N\approx4{,}19.10^{13}\ \text{Bq}\approx1{,}13.10^{3}\ \text{Ci}$ (dùng $\lambda$ chưa làm tròn), khớp câu c."),
                 P(r"Độ lớn hợp lí: nguồn xạ trị thực tế có độ phóng xạ cỡ hàng nghìn curi.")])],
  [r"a) $N_0\approx4{,}01.10^{22}$ hạt nhân; $\lambda\approx4{,}17.10^{-9}\ \text{s}^{-1}$", r"b) $H_0\approx1{,}67.10^{14}\ \text{Bq}\approx4{,}52.10^{3}\ \text{Ci}$", r"c) $H\approx1{,}13.10^{3}\ \text{Ci}$"],
  r"Nhận dạng: đề cho <strong>khối lượng nguồn, $T$ tính bằng năm, hỏi Bq hoặc Ci</strong> → đếm $N_0$, đổi $T$ ra giây rồi lấy $H=\lambda N$."),

 sol([r"Độ phóng xạ riêng $h=\dfrac{H}{m_C}$ (Bq trên $1$ g carbon): chỉ so được hai mẫu khi cùng khối lượng carbon.",
      r"Sau khi cây chết: $h=h_0\,2^{-n}$ với $n=\dfrac{t}{T}$, tức $\dfrac{h_0}{h}=2^n$.",
      r"Điều kiện (giả thiết): tỉ lệ $^{14}\text{C}$ trong khí quyển không đổi; mẫu không trao đổi carbon sau khi chết và không nhiễm carbon mới."],
  [("Độ phóng xạ riêng của mẫu (câu a)", [M(r"h=\dfrac{H}{m_C}=\dfrac{0{,}360}{5{,}0}"), A(r"h=0{,}0720\ \text{Bq/g}")]),
   ("Tỉ số so với cây sống (câu a)", [M(r"\dfrac{h}{h_0}=\dfrac{0{,}0720}{0{,}226}"), A(r"\dfrac{h}{h_0}\approx0{,}319")]),
   ("Số chu kì đã qua (câu b)", [M(r"2^n=\dfrac{h_0}{h}=\dfrac{0{,}226}{0{,}0720}\approx3{,}14"), M(r"n=\log_2 3{,}14"), A(r"n\approx1{,}65")]),
   ("Tuổi của mẩu than (câu b)", [M(r"t=nT=1{,}6504\cdot5730"), A(r"t\approx9455\ \text{năm}\approx9{,}5.10^{3}\ \text{năm}")]),
   ("Khi mẫu bị lẫn carbon hiện đại (câu c)", [P(r"$^{14}\text{C}$ thêm vào làm độ phóng xạ riêng $h$ đo được lớn hơn $h$ thật của mẫu cổ, nên tỉ số $\dfrac{h}{h_0}$ gần $1$ hơn và $n$ nhỏ đi."), A("T:Tuổi tính ra nhỏ hơn tuổi thật.")]),
   ("Kiểm tra", [P(r"$0{,}319$ nằm giữa $0{,}5$ và $0{,}25$ nên $1\lt n\lt2$; $n=1{,}65$ hợp lí."),
                 M(r"h=h_0\,2^{-n}=0{,}226\cdot2^{-1{,}65}\approx0{,}0720\ \text{Bq/g}"),
                 P(r"Tuổi cỡ $9{,}5$ nghìn năm, còn trong tầm đo của $^{14}\text{C}$ (tới khoảng $50\,000$ năm).")])],
  [r"a) $h=0{,}0720\ \text{Bq/g}$; $\dfrac{h}{h_0}\approx0{,}319$", r"b) $t\approx9455$ năm (cỡ $9{,}5$ nghìn năm)", r"c) Tuổi tính ra nhỏ hơn tuổi thật"],
  r"Nhận dạng: đề cho <strong>hai mẫu có khối lượng carbon khác nhau và giả thiết khí quyển</strong> → đưa về độ phóng xạ riêng, tìm $n$ bằng logarit rồi $t=nT$."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>chuỗi phân rã nối tiếp, hỏi hạt nhân con</b> → nghĩ tới <b>bảo toàn A và Z</b> ở từng phương trình.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Số khối của X", "Hạt nhân X có số khối bằng bao nhiêu?", 234, "", 0,
       loi=r"Nhầm vai trò số khối và điện tích của hạt $\alpha$, hoặc cộng thay vì trừ."),
  buoc("Số proton của X", "Hạt nhân X có bao nhiêu proton?", 90, "", 0,
       loi=r"Trừ $4$ cho số proton (lấy nhầm số khối của hạt $\alpha$), hoặc coi số proton không đổi.",
       ke=[(r"Viết phương trình bảo toàn điện tích cho phân rã $\alpha$, với điện tích của hạt $\alpha$", True),
           (r"Số proton của mẹ bằng số proton của X cộng $4$, vì hạt $\alpha$ có số khối $4$", r"Số khối $4$ là tổng proton và nơtron; chỉ phần proton (điện tích $+2e$) đi vào phương trình điện tích."),
           (r"Số proton không đổi vì hạt $\alpha$ chỉ lấy đi nơtron", r"Hạt $\alpha$ gồm $2$ proton và $2$ nơtron, nên lấy đi cả hai proton.")]),
  buoc("Số proton của Y", "Hạt nhân Y có bao nhiêu proton?", 91, "", 0,
       loi=r"Cho số proton giảm $1$ vì thấy electron mang điện âm, hoặc coi số proton không đổi vì electron rất nhẹ.",
       ke=[(r"Viết phương trình bảo toàn số khối và điện tích cho phân rã $\beta^-$, với kí hiệu của electron", True),
           (r"Phân rã $\beta^-$: số proton giảm $1$ vì electron mang điện âm bay đi", r"Electron điện $-e$ bay đi thì hạt nhân con phải tăng $1$ proton để tổng điện tích không đổi: $Z_X=Z_Y+(-1)$."),
           (r"Phân rã $\beta^-$: số proton không đổi vì electron quá nhẹ, không đáng kể", r"Electron mang điện $-e$, không thể bỏ qua trong bảo toàn điện tích.")]),
  buoc("Số proton của W", "Hạt nhân W có bao nhiêu proton?", 92, "", 0,
       loi=r"Cộng $1$ vào số proton của X (bỏ qua Y), hoặc giữ nguyên số proton của Y.",
       ke=[(r"Viết lại phương trình bảo toàn số khối và điện tích cho phân rã $\beta^-$ của Y", True),
           (r"Cộng $1$ vào số proton của X, vì X mới là hạt nhân có sẵn từ đầu", r"X đã phân rã thành Y rồi; W là con của Y nên phải cộng $1$ vào số proton của Y."),
           (r"Số proton không đổi, lần này chỉ phát thêm tia $\gamma$", r"Đề cho Y phóng xạ $\beta^-$ nên số proton vẫn tăng $1$; tia $\gamma$ mới là tia không đổi ô.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang=r"Thấy <b>sau thời gian t, chu kì bán rã T</b> → nghĩ tới <b>định luật phóng xạ</b>: mỗi chu kì còn một nửa.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Số chu kì", "Sau $552$ ngày, mẫu đã qua bao nhiêu chu kì bán rã?", 4, "chu kì", 0.01,
       loi=r"Chia ngược $T$ cho $t$ nên ra số nhỏ hơn $1$, hoặc lấy thẳng số ngày làm số mũ."),
  buoc("Số hạt nhân còn lại", "Số hạt nhân Po chưa phân rã bằng bao nhiêu, tính theo đơn vị $10^{17}$ hạt?", 4.0, "·10¹⁷ hạt", 0.05,
       loi=r"Lấy số hạt đã phân rã làm số hạt còn lại, hoặc chia $N_0$ cho $n$ thay vì cho $2^n$.",
       ke=[(r"$N=\dfrac{N_0}{2^n}$ với $n$ vừa tính", True),
           (r"$N=\dfrac{N_0}{n}$", r"Mỗi chu kì số hạt chia $2$, qua $n$ chu kì phải chia $2^n$, không chia $n$."),
           (r"$N=N_0\left(1-\dfrac{1}{2^n}\right)$", r"Đó là số hạt đã phân rã; đề hỏi số hạt chưa phân rã.")]),
  buoc("Phần trăm đã phân rã", "Bao nhiêu phần trăm số hạt nhân ban đầu đã phân rã?", 93.75, "%", 0.1,
       loi=r"Ghi phần còn lại làm đáp số, hoặc cộng thêm một lượng cố định cho mỗi chu kì.",
       ke=[(r"Phần đã phân rã bằng $1-\dfrac{1}{2^n}$", True),
           (r"Phần đã phân rã bằng $\dfrac{1}{2^n}$", r"$\dfrac{1}{2^n}$ là phần còn lại; đề hỏi phần đã phân rã."),
           (r"Mỗi chu kì phân rã $50\%$ nên cộng $n\cdot50\%$", r"Mỗi chu kì chỉ phân rã một nửa số hạt đang còn, không phải một nửa số hạt ban đầu; cộng như vậy sẽ vượt quá $100\%$.")]),
  buoc("Phần trăm còn lại sau $759$ ngày", "Sau $759$ ngày, số hạt nhân còn lại bằng bao nhiêu phần trăm số hạt nhân ban đầu?", 2.21, "%", 0.02,
       loi=r"Làm tròn $n$ thành số nguyên rồi mới lấy $2^{-n}$, hoặc lấy trung bình của hai mốc nguyên.",
       ke=[(r"Tính $n=\dfrac{t}{T}$ rồi thế vào $2^{-n}$ bằng máy tính, kể cả khi $n$ không nguyên", True),
           (r"Lấy trung bình phần còn lại ở hai mốc chu kì nguyên kề nhau", r"Phần còn lại giảm theo cấp số nhân chứ không đều, nên trung bình cộng hai mốc lớn hơn giá trị thật ở chính giữa."),
           (r"Làm tròn $n$ xuống số nguyên gần nhất rồi lấy $2^{-n}$", r"Làm tròn bỏ mất nửa chu kì, nên phần còn lại bị tính cao hơn thật.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang=r"Thấy <b>khối lượng đã phân rã, hỏi chu kì hoặc thời gian</b> → nghĩ tới <b>định luật phóng xạ</b> và logarit cơ số $2$.",
  cap_do=3, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Khối lượng còn lại sau $24$ ngày", "Sau $24$ ngày, khối lượng iốt-131 chưa phân rã còn lại là bao nhiêu microgam?", 8, "μg", 0.1,
       loi=r"Lấy khối lượng đã phân rã làm khối lượng còn lại."),
  buoc("Số chu kì đã qua", "Trong $24$ ngày, khối lượng đã giảm đi một nửa bao nhiêu lần (số chu kì $n$)?", 3, "chu kì", 0.02,
       loi=r"Lấy $n$ bằng chính tỉ số khối lượng (đó là $2^n$), hoặc thế khối lượng đã phân rã vào $2^{-n}$.",
       ke=[(r"Từ $m_t=m_0\,2^{-n}$ suy ra $2^n=\dfrac{m_0}{m_t}$ rồi tìm $n$", True),
           (r"Lấy $n=\dfrac{m_0}{m_t}$", r"Tỉ số khối lượng là $2^n$, không phải $n$: mỗi chu kì khối lượng chia $2$ chứ không trừ đi một lượng đều."),
           (r"Thế khối lượng đã phân rã vào $2^{-n}$", r"$2^{-n}$ chỉ tính phần CÒN LẠI; khối lượng đã phân rã là $m_0(1-2^{-n})$.")]),
  buoc("Chu kì bán rã", "Chu kì bán rã $T$ bằng bao nhiêu ngày?", 8, "ngày", 0.1,
       loi=r"Nhân $t$ với $n$ thay vì chia, hoặc chia ngược $n$ cho $t$.",
       ke=[(r"$T=\dfrac{t}{n}$", True),
           (r"$T=n\cdot t$", r"Mẫu đã qua nhiều chu kì trong thời gian $t$ nên một chu kì phải ngắn hơn $t$, không dài hơn."),
           (r"$T=\dfrac{n}{t}$", r"Đó là số chu kì trên mỗi ngày (nghịch đảo của $T$), đơn vị là $1/\text{ngày}$.")]),
  buoc("Khối lượng còn lại sau $40$ ngày", "Sau $40$ ngày kể từ lúc đầu, khối lượng iốt-131 chưa phân rã còn lại là bao nhiêu microgam?", 2, "μg", 0.05,
       loi=r"Cho khối lượng giảm đều theo ngày như $24$ ngày đầu, hoặc lấy số ngày làm số mũ.",
       ke=[(r"Tính $n'=\dfrac{40}{T}$ rồi $m=\dfrac{m_0}{2^{n'}}$", True),
           (r"Cho khối lượng giảm đều theo ngày, cùng tốc độ như $24$ ngày đầu", r"Phóng xạ giảm theo hàm mũ: lượng mất mỗi ngày nhỏ dần theo lượng còn lại."),
           (r"Dùng $m=m_0\cdot2^{-40}$", r"Số mũ phải là $\dfrac{t}{T}$ (số chu kì), không phải số ngày $t$.")]),
  buoc("Thời gian để còn dưới $0{,}1\\ \\mu\\text{g}$", "Thời gian $t$ để khối lượng còn lại đúng bằng $0{,}1\\ \\mu\\text{g}$ là bao nhiêu ngày?", 74.6, "ngày", 0.3,
       loi=r"Đếm trọn số chu kì rồi tính (ra số lớn hơn thời gian ít nhất), hoặc cho rằng mẫu phân rã hết hoàn toàn.",
       ke=[(r"Giải $m_0\,2^{-n}=0{,}1$ bằng logarit cơ số $2$, rồi nhân với $T$", True),
           (r"Chia đôi khối lượng liên tiếp tới khi dưới $0{,}1\ \mu\text{g}$ rồi lấy trọn số chu kì đó", r"Khối lượng chỉ cần giảm qua ngưỡng; thời điểm đó nằm giữa hai mốc chu kì nguyên, nên đếm trọn chu kì cho đáp số lớn hơn thời gian ít nhất."),
           (r"Cho khối lượng còn lại bằng $0$ (phân rã hết)", r"Hàm mũ không bao giờ bằng $0$; phải đặt ngưỡng $0{,}1\ \mu\text{g}$ của đề.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang=r"Thấy <b>khối lượng nguồn, T bằng năm, hỏi Bq hoặc Ci</b> → nghĩ tới <b>H = λN</b>, chú ý đơn vị.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Số hạt nhân ban đầu", "Số hạt nhân Co-60 trong nguồn lúc đầu bằng bao nhiêu, tính theo đơn vị $10^{22}$ hạt?", 4.01, "·10²² hạt", 0.02,
       loi=r"Quên chia cho khối lượng mol, hoặc nhân thêm với một đại lượng không liên quan."),
  buoc("Hằng số phóng xạ", "Hằng số phóng xạ $\\lambda$ bằng bao nhiêu, tính theo đơn vị $10^{-9}\\ \\text{s}^{-1}$?", 4.17, "·10⁻⁹ s⁻¹", 0.03,
       loi=r"Để $T$ tính bằng năm rồi dùng luôn (ra đơn vị $1/\text{năm}$), hoặc đổi năm sang giây thiếu một bước.",
       ke=[(r"$\lambda=\dfrac{0{,}693}{T}$ với $T$ đổi ra giây", True),
           (r"$\lambda=\dfrac{0{,}693}{T}$ với $T$ tính bằng năm rồi dùng luôn", r"Khi đó $\lambda$ có đơn vị $1/\text{năm}$; $H=\lambda N$ sẽ ra số phân rã mỗi năm, không phải Bq."),
           (r"$\lambda=\dfrac{T}{0{,}693}$", r"Đó là nghịch đảo: $\lambda$ càng nhỏ khi $T$ càng dài.")]),
  buoc("Độ phóng xạ ban đầu (Bq)", "Độ phóng xạ ban đầu $H_0$ bằng bao nhiêu, tính theo đơn vị $10^{14}\\ \\text{Bq}$?", 1.674, "·10¹⁴ Bq", 0.01,
       loi=r"Bỏ quên $\ln2$ (lấy $\dfrac{N_0}{T}$), hoặc nhân $\lambda$ với khối lượng thay vì số hạt nhân.",
       ke=[(r"$H_0=\lambda N_0$", True),
           (r"$H_0=\dfrac{N_0}{T}$", r"Bỏ mất thừa số $\ln2$: số phân rã mỗi giây là $\lambda N_0$ với $\lambda=\dfrac{\ln2}{T}$, không phải $\dfrac{N_0}{T}$."),
           (r"$H_0=\lambda m_0$", r"$H$ tỉ lệ với số hạt nhân $N_0$, không tỉ lệ với khối lượng tính bằng gam.")]),
  buoc("Đổi ra curi", "Độ phóng xạ ban đầu bằng bao nhiêu curi?", 4520, "Ci", 30,
       loi=r"Nhân với hệ số đổi thay vì chia (curi là đơn vị rất lớn), hoặc lấy $1\ \text{Ci}$ bằng một lũy thừa tròn của $10$ Bq.",
       ke=[(r"Đổi Bq sang Ci theo định nghĩa của $1\ \text{Ci}$", True),
           (r"Nhân với $3{,}7.10^{10}$", r"Đổi sang đơn vị lớn thì con số phải nhỏ đi."),
           (r"Chia cho $10^{11}$ cho tròn số", r"$1\ \text{Ci}=3{,}7.10^{10}\ \text{Bq}$ theo định nghĩa, không phải $10^{11}$.")]),
  buoc("Độ phóng xạ sau $10{,}54$ năm", "Sau $10{,}54$ năm, độ phóng xạ của nguồn còn bao nhiêu curi?", 1130, "Ci", 10,
       loi=r"Chia $H_0$ cho $n$ thay vì cho $2^n$, hoặc chỉ cho giảm một nửa dù đã qua nhiều chu kì.",
       ke=[(r"Tính $n=\dfrac{t}{T}$ rồi $H=\dfrac{H_0}{2^n}$, không cần tính lại $\lambda$", True),
           (r"$H=\dfrac{H_0}{n}$", r"Mỗi chu kì độ phóng xạ chia $2$; qua $n$ chu kì phải chia $2^n$."),
           (r"$H=\dfrac{H_0}{2}$ vì độ phóng xạ giảm một nửa", r"Thời gian khảo sát dài hơn một chu kì nên độ phóng xạ đã giảm một nửa nhiều lần.")]),
  buoc("Kiểm tra")]),

 dict(nhan_dang=r"Thấy <b>hai mẫu khác khối lượng carbon, có giả thiết khí quyển</b> → nghĩ tới <b>độ phóng xạ riêng</b>, rồi logarit.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Độ phóng xạ riêng của mẫu", "Độ phóng xạ riêng của mẫu (Bq trên mỗi gam carbon) bằng bao nhiêu?", 0.0720, "Bq/g", 0.001,
       loi=r"Dùng thẳng số đo của cả mẩu mà không chia cho khối lượng carbon."),
  buoc("Tỉ số so với cây sống", "Tỉ số $\\dfrac{h}{h_0}$ giữa độ phóng xạ riêng của mẫu và của cây sống bằng bao nhiêu?", 0.319, "", 0.003,
       loi=r"So hai số đo ứng với khối lượng carbon khác nhau, hoặc lấy tỉ số ngược.",
       ke=[(r"So hai độ phóng xạ riêng, cùng tính trên $1$ g carbon", True),
           (r"So trực tiếp $0{,}360\ \text{Bq}$ với $0{,}226\ \text{Bq}$", r"Hai số đo ứng với $5{,}0$ g và $1$ g carbon; phải đưa về cùng khối lượng carbon mới so được."),
           (r"Lấy tỉ số khối lượng carbon $\dfrac{5{,}0}{1{,}0}$", r"Phần lớn carbon trong mẫu là $^{12}\text{C}$ không phân rã; chỉ độ phóng xạ của $^{14}\text{C}$ cho biết tuổi.")]),
  buoc("Số chu kì đã qua", "Số chu kì $n$ mà mẫu đã trải qua bằng bao nhiêu?", 1.65, "chu kì", 0.02,
       loi=r"Lấy $n$ bằng chính tỉ số $\dfrac{h_0}{h}$, hoặc lấy $n=1-\dfrac{h}{h_0}$ (phần đã phân rã).",
       ke=[(r"Từ $\dfrac{h_0}{h}=2^n$ tìm $n$ bằng logarit cơ số $2$", True),
           (r"Lấy $n=\dfrac{h_0}{h}$", r"Tỉ số $\dfrac{h_0}{h}$ bằng $2^n$ chứ không bằng $n$."),
           (r"Lấy $n=1-\dfrac{h}{h_0}$", r"Đó là phần đã phân rã, không phải số chu kì.")]),
  buoc("Tuổi của mẩu than", "Tuổi của mẩu than gỗ bằng bao nhiêu năm?", 9455, "năm", 60,
       loi=r"Đổi $T$ sang đơn vị khác rồi vẫn ghi năm, hoặc dùng phần trăm đã phân rã thay cho số chu kì.",
       ke=[(r"$t=n\cdot T$", True),
           (r"$t=nT$ nhưng đổi $T$ ra giây rồi vẫn ghi đáp số bằng năm", r"Đổi $T$ ra giây thì $t$ ra giây; ghi là năm sẽ sai hệ số hơn $10^7$ lần."),
           (r"$t=\left(1-\dfrac{h}{h_0}\right)T$", r"Phần trăm đã phân rã không phải số chu kì; tuổi phải tính từ $n$.")]),
  buoc("Khi mẫu bị lẫn carbon hiện đại", "Nếu mẫu lẫn carbon hiện đại, tuổi tính theo cách trên so với tuổi thật thế nào?",
       loi=r"Nghĩ rằng thêm carbon thì mẫu trông già hơn, hoặc cho rằng giả thiết không ảnh hưởng kết quả.",
       lua_chon=[(r"Nhỏ hơn: $^{14}\text{C}$ thêm vào làm độ phóng xạ riêng đo được cao, mẫu trông trẻ hơn", True),
                 (r"Lớn hơn: thêm carbon làm mẫu trông nhiều tuổi hơn", r"Carbon hiện đại có nhiều $^{14}\text{C}$ làm $h$ đo được cao hơn, tỉ số $\dfrac{h}{h_0}$ gần $1$ hơn, nên tuổi tính ra nhỏ hơn."),
                 (r"Không đổi: $^{14}\text{C}$ mới cũng phân rã theo $T$ nên tuổi vẫn đúng", r"Phép tính coi mọi $^{14}\text{C}$ trong mẫu đã phân rã từ khi cây chết; $^{14}\text{C}$ thêm vào chưa trải qua thời gian đó.")],
       ke=[(r"Xét carbon lẫn vào làm độ phóng xạ riêng đo được thay đổi thế nào", True),
           (r"Tính lại $T$ cho carbon hiện đại", r"$T$ của $^{14}\text{C}$ là hằng số, không đổi dù carbon cũ hay mới."),
           (r"Bỏ qua: giả thiết chỉ là thủ tục, không ảnh hưởng kết quả", r"Tuổi chỉ đúng khi giả thiết đúng; vi phạm giả thiết thì tuổi tính ra lệch.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
write(J, 18, "Bài 17. Hiện tượng phóng xạ", DANG, BUILD, ANALYSIS, SOLS, None)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code)"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
