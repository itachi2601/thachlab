"""Bài tập mẫu Bài 21 "Moment lực. Cân bằng của vật rắn" (Vật lí 10) — lesson_id 66. 5 dạng (quét dạng:
scripts/logs/batch-ra-soat/ket-qua/66.quet-dang.json). Hình: hinh_66.py.
Ví dụ cũ (old/66.json, 15 ví dụ): VD4 cối xay → biên tập thành Dạng 2; VD9 thanh + giá đỡ → biên tập thành Dạng 4 (đổi số, thêm lực giá đỡ);
VD1, VD3 (cột điện), VD6, VD7, VD14 → tu_luan (viết lại sạch, tự tính lại đáp số); 8 ví dụ còn lại BỎ vì phụ thuộc hình không kiểm được / hình lệch lời giải.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-66.py   (idempotent, ghi 66.json với review.checked=false)"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_66 import *

J = os.path.join(HERE, "66.json")
T130 = "Moment lực và quy tắc moment"
T131 = "Ngẫu lực, cân bằng của vật rắn có trục quay"

# ═════════════ KIỂM SỐ (độc lập với lời giải: lệch thì dừng) ═════════════
# D1
assert abs(20 * 0.75 - 15) < 1e-9 and abs(15 / 0.15 - 100) < 1e-9
assert abs(20 * 0.75 / 0.15 - 100) < 1e-9
# D2
a_ = math.radians(40); dd2 = 0.30 * math.sin(a_); M2 = 80 * dd2; Ft = M2 / 0.30
assert abs(dd2 - 0.1928) < 1e-4 and abs(M2 - 15.43) < 5e-3 and abs(Ft - 51.42) < 5e-3 and abs(Ft - 80 * math.sin(a_)) < 1e-9
assert abs(80 * 0.30 - 24) < 1e-9 and abs(80 * math.cos(a_) * 0.30 - 18.4) < 0.05          # lựa chọn sai: F·r, F·cosα·r
assert abs(M2 / dd2 - 80) < 1e-9                                                          # lựa chọn sai: chia cho r·sinα ra lại 80 N
# D3
M3 = 30 * 0.90
assert abs(M3 - 27) < 1e-9 and abs(36 / 0.90 - 40) < 1e-9 and abs(30 * 0.45 - 13.5) < 1e-9 and abs(36 / 0.45 - 80) < 1e-9
# D4: x = OA; 40x = 20(0,5-x) + 20(1-x)
x4 = (20 * 0.5 + 20 * 1.0) / (40 + 20 + 20)
assert abs(x4 - 0.375) < 1e-12 and 0 < x4 < 0.5
assert abs(40 * x4 - (20 * (0.5 - x4) + 20 * (1.0 - x4))) < 1e-9
N4 = 40 + 20 + 20
assert N4 == 80 and abs(N4 * x4 - (20 * 0.5 + 20 * 1.0)) < 1e-9                         # kiểm moment quanh A
assert 40 + 20 != N4                                                                      # lựa chọn sai: quên thanh
assert abs((40 * 0.5) / 80 - 0.25) < 1e-9 and 0.5 != x4                                   # OA = OB = 0,5 là sai
# D5
dT = 1.2 * math.sin(math.radians(30)); Msum = 40 * 0.75 + 16 * 1.5; T5 = Msum / dT
Ty = T5 * math.sin(math.radians(30)); Ny = 40 + 16 - Ty
assert abs(dT - 0.6) < 1e-12 and abs(Msum - 54) < 1e-9 and abs(T5 - 90) < 1e-9 and abs(Ty - 45) < 1e-9 and abs(Ny - 11) < 1e-9
assert abs(Ny * 1.5 + Ty * 0.3 - 40 * 0.75) < 1e-9                                       # moment quanh B
assert abs(40 * 1.5 + 16 * 1.5 - 84) < 1e-9 and abs(84 / dT - 140) < 1e-9                 # sai: arm cả thanh
assert abs(54 / 1.2 - 45) < 1e-9 and (40 + 16) != T5                                      # sai: quên sin30 / T = tổng trọng lượng
# tu_luan
assert abs(200 * 1.5 - 300 * 1.0) < 1e-9
assert abs(1.5 * 10 * 0.4 / 1.0 - 6) < 1e-9
assert abs(500 / math.sin(math.radians(30)) - 1000) < 1e-9
assert abs(100 * math.cos(math.radians(30)) - 50 * math.sqrt(3)) < 1e-9 and abs(50 * math.sqrt(3) - 86.60) < 0.01
assert abs(math.sqrt(10 ** 2 - 6 ** 2) - 8) < 1e-9 and abs(30 * 8 / 6 - 40) < 1e-9

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Moment của lực: tính M, tìm lực khi đổi chỗ đặt", topic=T130,
      problem_html=r"<p>Một cánh cửa rộng $0{,}90\ \text{m}$ quay quanh bản lề. Em đẩy cửa bằng lực $F=20\ \text{N}$ vuông góc với mặt cửa, tại điểm cách bản lề $75\ \text{cm}$.</p>"
      r"""<ol type="a"><li>Tính moment của lực đối với trục bản lề.</li><li>Em đổi sang đẩy tại điểm cách bản lề $15\ \text{cm}$ mà vẫn muốn có đúng moment đó. Lực đẩy lúc này là bao nhiêu?</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Lực xiên: tìm cánh tay đòn rồi tính moment", topic=T130,
      problem_html=r"<p>Để quay một cối xay đá, người ta đẩy vào núm cầm gắn trên mặt đá. Núm cách tâm cối $r=0{,}30\ \text{m}$. Lực đẩy $F=80\ \text{N}$ nằm trong mặt phẳng nằm ngang, giá của lực hợp với đường thẳng nối núm và tâm cối góc $40^\circ$. Trục quay đi qua tâm cối, vuông góc với mặt phẳng ngang.</p>"
      r"""<ol type="a"><li>Tìm cánh tay đòn $d$ của lực $F$.</li><li>Tính moment của lực $F$ đối với trục quay.</li><li>Nếu người đẩy vuông góc với đường nối núm – tâm thì phải đẩy bằng lực bao nhiêu để có cùng moment?</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Ngẫu lực: hợp lực và moment", topic=T131,
      problem_html=r"<p>Một bánh lái tàu thuyền quay quanh trục đi qua tâm bánh lái. Người lái đặt hai tay vào hai tay nắm ở hai đầu một đường kính của bánh lái; hai tay nắm cách nhau $0{,}90\ \text{m}$. Mỗi tay đẩy một lực $30\ \text{N}$ theo phương tiếp tuyến với vành bánh lái, hai lực ngược chiều nhau và làm bánh lái quay cùng một chiều.</p>"
      r"""<ol type="a"><li>Hợp lực của hai lực là bao nhiêu?</li><li>Tính moment của cặp lực đối với trục quay.</li><li>Muốn tạo moment $36\ \text{N}\cdot\text{m}$ thì mỗi tay phải đẩy một lực bao nhiêu?</li></ol>"""),
 dict(label="Dạng 4 · Khá · Thanh có trọng lượng trên giá đỡ: tìm vị trí giá đỡ và lực giá đỡ", topic=T130,
      problem_html=r"<p>Hai khối nặng được gắn chặt vào hai đầu $A$, $B$ của một thanh đồng chất $AB$ dài $1{,}0\ \text{m}$, trọng lượng $20\ \text{N}$. Khối ở $A$ nặng $40\ \text{N}$, khối ở $B$ nặng $20\ \text{N}$ (kích thước các khối bỏ qua). Thanh được đặt trên một giá đỡ nhọn $O$ dưới thanh và nằm ngang cân bằng.</p>"
      r"""<ol type="a"><li>Tính khoảng cách $OA$.</li><li>Tính lực giá đỡ tác dụng lên thanh.</li></ol>"""),
 dict(label="Dạng 5 · Khó · Thanh gắn bản lề giữ bằng dây xiên: lực căng và lực bản lề", topic=T130,
      problem_html=r"<p>Một thanh đồng chất $AB$ dài $1{,}5\ \text{m}$, trọng lượng $40\ \text{N}$, nằm ngang, đỡ một biển hiệu quán ăn nặng $16\ \text{N}$ gắn chặt vào đầu $B$ (kích thước biển hiệu bỏ qua). Đầu $A$ gắn vào tường bằng bản lề. Một sợi dây buộc vào điểm $C$ trên thanh với $AC=1{,}2\ \text{m}$, đầu kia buộc vào tường ở phía trên bản lề; dây hợp với thanh góc $30^\circ$ và giữ thanh nằm ngang.</p>"
      r"""<ol type="a"><li>Tính lực căng của dây.</li><li>Tính thành phần thẳng đứng của lực bản lề tác dụng lên thanh và cho biết nó hướng lên hay hướng xuống.</li></ol>"""),
]
FORMS = ["bai_tap"] * 5
BUILD = [d1, d2, d3, d4, d5]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (hàng "cần tìm" chỉ ghi "Đại lượng cần tìm"; ô ⚠ chỉ nêu câu hỏi điều kiện) ═════════════
ANALYSIS = [
 [(r"“cánh cửa rộng $0{,}90\ \text{m}$ quay quanh bản lề”", r"Trục quay là bản lề; bề rộng cửa $0{,}90$ m", "Khái niệm: moment lực đối với một trục quay"),
  (r"“đẩy cửa bằng lực $F=20\ \text{N}$ vuông góc với mặt cửa”", r"$F=20$ N; giá của lực vuông góc mặt cửa", "⚠ Cánh tay đòn đo từ đâu tới đâu? Đường nào là giá của lực?"),
  (r"“tại điểm cách bản lề $75\ \text{cm}$”", r"$75$ cm (đơn vị là cm)", "⚠ Công thức moment dùng đơn vị nào của khoảng cách?"),
  (r"“a) moment của lực”", r"Cần $M$", "Đại lượng cần tìm"),
  (r"“đẩy tại điểm cách bản lề $15\ \text{cm}$ mà vẫn muốn có đúng moment đó”", r"$15$ cm; moment không đổi", "Khái niệm: hai lực cho cùng tác dụng làm quay"),
  (r"“b) lực đẩy lúc này”", r"Cần $F'$", "Đại lượng cần tìm")],
 [(r"“núm cách tâm cối $r=0{,}30\ \text{m}$”", r"$r=0{,}30$ m (từ trục tới điểm đặt)", "Khái niệm: trục quay qua tâm cối"),
  (r"“lực đẩy $F=80\ \text{N}$ nằm trong mặt phẳng nằm ngang”", r"$F=80$ N", "Khái niệm: giá của lực — đường thẳng chứa lực"),
  (r"“giá của lực hợp với đường thẳng nối núm và tâm cối góc $40^\circ$”", r"$\alpha=40^\circ$", "⚠ Góc $40^\circ$ là góc giữa hai đường nào? Cánh tay đòn đo từ đâu tới đâu?"),
  (r"“a) cánh tay đòn $d$”", r"Cần $d$", "Đại lượng cần tìm"),
  (r"“b) moment của lực $F$”", r"Cần $M$", "Đại lượng cần tìm"),
  (r"“c) vuông góc với đường nối núm – tâm … cùng moment”", r"Lực vuông góc đường nối; $M$ như câu b", "⚠ Giá của lực mới nằm thế nào so với đường nối núm – tâm?")],
 [(r"“hai tay nắm cách nhau $0{,}90\ \text{m}$”", r"Khoảng cách giữa hai giá: $0{,}90$ m", "Khái niệm: ngẫu lực; khoảng cách giữa hai giá"),
  (r"“mỗi tay đẩy một lực $30\ \text{N}$ … tiếp tuyến … ngược chiều nhau”", r"$F_1=F_2=30$ N; song song, ngược chiều", "⚠ Hai lực này có thoả định nghĩa ngẫu lực không? Cần kiểm tra những tính chất nào?"),
  (r"“a) hợp lực của hai lực”", r"Cần hợp lực", "Đại lượng cần tìm"),
  (r"“b) moment của cặp lực”", r"Cần $M$", "Đại lượng cần tìm"),
  (r"“c) moment $36\ \text{N}\cdot\text{m}$ … mỗi tay đẩy một lực bao nhiêu”", r"$M'=36$ N·m; hai lực vẫn bằng nhau", "Đại lượng cần tìm")],
 [(r"“thanh đồng chất $AB$ dài $1{,}0\ \text{m}$, trọng lượng $20\ \text{N}$”", r"$AB=1{,}0$ m; $P=20$ N", "Khái niệm: trọng tâm của vật đồng chất"),
  (r"“khối ở $A$ nặng $40\ \text{N}$, khối ở $B$ nặng $20\ \text{N}$”", r"$P_A=40$ N tại $A$; $P_B=20$ N tại $B$", "Khái niệm: moment của mỗi trọng lực đối với trục"),
  (r"“đặt trên một giá đỡ nhọn $O$ dưới thanh”", r"Lực $N$ của giá đỡ đặt tại $O$, chưa biết", "⚠ Chọn trục ở đâu để lực chưa biết không xuất hiện trong phương trình moment?"),
  (r"“nằm ngang cân bằng”", "Cân bằng", "Định luật: điều kiện cân bằng của vật rắn"),
  (r"“a) khoảng cách $OA$”", r"Cần $OA$", "Đại lượng cần tìm"),
  (r"“b) lực giá đỡ”", r"Cần $N$", "Đại lượng cần tìm")],
 [(r"“thanh đồng chất $AB$ dài $1{,}5\ \text{m}$, trọng lượng $40\ \text{N}$, nằm ngang”", r"$AB=1{,}5$ m; $P=40$ N", "Khái niệm: trọng tâm của thanh đồng chất"),
  (r"“biển hiệu nặng $16\ \text{N}$ gắn chặt vào đầu $B$”", r"$P_1=16$ N tại $B$", "Khái niệm: moment của trọng lực"),
  (r"“đầu $A$ gắn vào tường bằng bản lề”", "Lực của bản lề chưa biết cả độ lớn lẫn hướng", "⚠ Chọn trục ở đâu để lực chưa biết đó không xuất hiện trong phương trình moment?"),
  (r"“dây buộc vào $C$ với $AC=1{,}2\ \text{m}$ … hợp với thanh góc $30^\circ$”", r"$AC=1{,}2$ m; $\alpha=30^\circ$; lực căng $T$ chưa biết", "⚠ Góc $30^\circ$ là góc giữa dây và đường nào? Cánh tay đòn của lực căng đo thế nào?"),
  (r"“giữ thanh nằm ngang”", "Thanh cân bằng", "Định luật: điều kiện cân bằng của vật rắn"),
  (r"“a) lực căng của dây”", r"Cần $T$", "Đại lượng cần tìm"),
  (r"“b) thành phần thẳng đứng của lực bản lề”", r"Cần độ lớn và hướng của $N_y$", "Đại lượng cần tìm")],
]

# ═════════════ LỜI GIẢI ═════════════
RC1 = [r"<strong>Khái niệm:</strong> moment lực đặc trưng cho tác dụng làm quay của lực quanh một trục.",
       r"<strong>Khái niệm:</strong> cánh tay đòn $d$ là khoảng cách từ trục quay tới giá của lực, đo vuông góc.",
       r"<strong>Công thức:</strong> $M=F\cdot d$ (đơn vị $\text{N}\cdot\text{m}$).",
       r"⚠ <strong>Điều kiện:</strong> $d$ phải đổi ra mét; giá của lực đi qua trục thì $d=0$ và $M=0$."]
RC2 = [r"<strong>Khái niệm:</strong> cánh tay đòn $d$ là khoảng cách từ trục tới <em>giá của lực</em>, đo vuông góc.",
       r"<strong>Công thức:</strong> $M=F\cdot d$.",
       r"Lực hợp với đường nối trục – điểm đặt (dài $r$) góc $\alpha$: $d=r\sin\alpha$.",
       r"⚠ <strong>Điều kiện:</strong> $r$ là khoảng tới điểm đặt, không phải cánh tay đòn; lực vuông góc đường nối ($\alpha=90^\circ$) thì $d=r$."]
RC3 = [r"<strong>Khái niệm:</strong> ngẫu lực là hai lực song song, ngược chiều, cùng độ lớn, cùng đặt vào một vật.",
       r"<strong>Định luật:</strong> tổng hai lực của ngẫu lực bằng $\vec 0$ nên ngẫu lực chỉ làm vật quay.",
       r"<strong>Công thức:</strong> $M=F\cdot d$, với $d$ là khoảng cách giữa hai giá của hai lực.",
       r"⚠ <strong>Điều kiện:</strong> $F$ là độ lớn của MỘT lực; $d$ đổi ra mét."]
RC4 = [r"<strong>Khái niệm:</strong> thanh đồng chất có trọng tâm $G$ ở giữa; trọng lượng của thanh đặt tại $G$.",
       r"<strong>Định luật:</strong> quy tắc moment: tổng moment thuận chiều kim đồng hồ bằng tổng moment ngược chiều. Vật cân bằng còn có tổng lực bằng $\vec 0$.",
       r"<strong>Công thức:</strong> $M=F\cdot d$ cho từng lực.",
       r"⚠ <strong>Điều kiện:</strong> chọn trục qua $O$ để lực $N$ chưa biết có $d=0$; viết mọi khoảng cách theo cùng một ẩn $OA$."]
RC5 = [r"<strong>Khái niệm:</strong> $d=r\sin\alpha$ cho lực xiên; thanh đồng chất có trọng tâm ở giữa.",
       r"<strong>Định luật:</strong> vật rắn cân bằng khi tổng lực bằng $\vec 0$ và tổng moment bằng $0$.",
       r"<strong>Công thức:</strong> $M=F\cdot d$ · theo phương thẳng đứng $\sum F_y=0$.",
       r"⚠ <strong>Điều kiện:</strong> trục qua bản lề để lực bản lề có $d=0$; lực căng xiên chỉ có thành phần thẳng đứng $T\sin30^\circ$ trong phương trình lực theo phương đứng."]

SOLS = [
 sol(RC1, [
  ("Cánh tay đòn (đổi ra mét)", [P("Lực vuông góc mặt cửa nên cánh tay đòn là khoảng từ bản lề tới điểm đẩy:"), M(r"d=75\ \text{cm}=0{,}75\ \text{m}")]),
  ("Moment của lực", [M(r"M=F\cdot d"), M(r"M=20\cdot0{,}75"), A(r"M=15\ \text{N}\cdot\text{m}")]),
  ("Lực đẩy ở điểm gần bản lề", [P(r"Cùng moment, cánh tay đòn mới $d'=15\ \text{cm}=0{,}15\ \text{m}$:"), M(r"F'=\dfrac{M}{d'}"), M(r"F'=\dfrac{15}{0{,}15}"), A(r"F'=100\ \text{N}")]),
  ("Kiểm tra", [P(r"Cánh tay đòn ngắn đi $5$ lần thì lực tăng $5$ lần: $20\cdot5=100\ \text{N}$ ✓"), P(r"Đơn vị: $\text{N}\cdot\text{m}$ chia cho $\text{m}$ ra $\text{N}$ ✓")])],
  [r"a) $M=15\ \text{N}\cdot\text{m}$", r"b) $F'=100\ \text{N}$"],
  r"Nhận dạng: đề cho <strong>lực vuông góc</strong> và <strong>khoảng cách từ trục tới điểm đặt</strong> → $M=F\cdot d$, nhớ đổi cm sang m."),
 sol(RC2, [
  ("Cánh tay đòn của lực xiên", [P(r"Giá của lực hợp với đường nối núm – tâm góc $40^\circ$ nên:"), M(r"d=r\sin\alpha=0{,}30\cdot\sin40^\circ"), A(r"d\approx0{,}193\ \text{m}")]),
  ("Moment của lực", [M(r"M=F\cdot d=80\cdot0{,}1928"), A(r"M\approx15{,}4\ \text{N}\cdot\text{m}")]),
  ("Lực đẩy vuông góc đường nối núm – tâm", [P(r"Lực vuông góc đường nối thì cánh tay đòn bằng $r$:"), M(r"F_t=\dfrac{M}{r}=\dfrac{15{,}43}{0{,}30}"), A(r"F_t\approx51{,}4\ \text{N}")]),
  ("Kiểm tra", [P(r"$d\lt r$ nên lực xiên phải lớn hơn lực vuông góc: $80\gt51{,}4$ ✓"), P(r"Chỉ thành phần $F\sin40^\circ=51{,}4\ \text{N}$ vuông góc đường nối mới làm quay; thành phần dọc đường nối có giá qua trục nên $M=0$.")])],
  [r"a) $d\approx0{,}193\ \text{m}$", r"b) $M\approx15{,}4\ \text{N}\cdot\text{m}$", r"c) $F_t\approx51{,}4\ \text{N}$"],
  r"Nhận dạng: đề cho <strong>lực hợp góc</strong> với đường nối trục – điểm đặt → cánh tay đòn $d=r\sin\alpha$, không phải $r$."),
 sol(RC3, [
  ("Hợp lực của hai lực", [P("Hai lực song song, ngược chiều, cùng độ lớn nên cộng vectơ cho:"), A("T:Hợp lực bằng <strong>0</strong>. Bánh lái <strong>không tịnh tiến</strong>, chỉ quay quanh trục.")]),
  ("Moment của ngẫu lực", [P(r"$d$ là khoảng cách giữa hai giá, $F$ là độ lớn một lực:"), M(r"M=F\cdot d=30\cdot0{,}90"), A(r"M=27\ \text{N}\cdot\text{m}"),
                           P(r"Kiểm tra từng lực: mỗi lực có cánh tay đòn $0{,}45\ \text{m}$ và cùng làm quay một chiều:"), M(r"M=30\cdot0{,}45+30\cdot0{,}45=27\ \text{N}\cdot\text{m}")]),
  ("Lực mỗi tay để có moment lớn hơn", [M(r"F=\dfrac{M'}{d}=\dfrac{36}{0{,}90}"), A(r"F=40\ \text{N}")]),
  ("Kiểm tra", [P(r"Moment tăng $\dfrac{36}{27}=\dfrac{4}{3}$ lần thì lực tăng $\dfrac{4}{3}$ lần: $30\cdot\dfrac{4}{3}=40\ \text{N}$ ✓")])],
  [r"a) Hợp lực bằng $0$", r"b) $M=27\ \text{N}\cdot\text{m}$", r"c) $F=40\ \text{N}$"],
  r"Nhận dạng: đề cho <strong>hai lực song song ngược chiều bằng nhau</strong> → hợp lực bằng $0$, moment $M=F\cdot d$ với $d$ là khoảng cách giữa hai giá."),
 sol(RC4, [
  ("Trọng tâm của thanh", [P("Thanh đồng chất nên trọng tâm $G$ ở giữa thanh:"), M(r"AG=\dfrac{AB}{2}"), A(r"AG=0{,}5\ \text{m}")]),
  ("Quy tắc moment, tìm $OA$", [P(r"Đặt $OA=x$. Khối $A$ nặng hơn khối $B$ nên giả sử $O$ nằm giữa $A$ và $G$; sẽ kiểm lại sau."),
                                P(r"Khi đó $OG=0{,}5-x$ và $OB=1{,}0-x$."),
                                P(r"Chọn trục qua $O$ (lực $N$ có $d=0$). Moment làm phía $A$ đi xuống bằng moment làm phía $B$ đi xuống:"),
                                M(r"P_A\cdot x=P\cdot(0{,}5-x)+P_B\cdot(1{,}0-x)"), M(r"40x=20(0{,}5-x)+20(1{,}0-x)"), M(r"80x=30"), A(r"OA=0{,}375\ \text{m}")]),
  ("Lực giá đỡ", [P("Tổng lực theo phương thẳng đứng bằng $0$, lực giá đỡ hướng lên:"), M(r"N=P_A+P+P_B=40+20+20"), A(r"N=80\ \text{N}")]),
  ("Kiểm tra", [P(r"$x=0{,}375\lt0{,}5$ nên $G$ đúng ở phía $B$ của $O$ ✓"), P(r"Moment quanh $A$: $N\cdot x=80\cdot0{,}375=30\ \text{N}\cdot\text{m}$; $P\cdot0{,}5+P_B\cdot1{,}0=10+20=30\ \text{N}\cdot\text{m}$ ✓")])],
  [r"a) $OA=0{,}375\ \text{m}$", r"b) $N=80\ \text{N}$"],
  r"Nhận dạng: đề hỏi <strong>vị trí giá đỡ</strong> của thanh có vật ở hai đầu → trục qua giá đỡ, đặt $OA=x$ và nhớ trọng lượng thanh đặt ở giữa."),
 sol(RC5, [
  ("Cánh tay đòn của lực căng", [P(r"Đối với trục qua bản lề $A$, dây hợp với thanh góc $30^\circ$:"), M(r"d_T=AC\cdot\sin30^\circ=1{,}2\cdot0{,}5"), A(r"d_T=0{,}6\ \text{m}")]),
  ("Moment của hai trọng lực", [P(r"Lực của bản lề có $d=0$ nên không có mặt. Trọng lượng thanh đặt ở $G$ cách $A$ nửa chiều dài; biển hiệu ở $B$:"),
                                M(r"M_P=P\cdot\dfrac{AB}{2}=40\cdot0{,}75=30\ \text{N}\cdot\text{m}"), M(r"M_{P_1}=P_1\cdot AB=16\cdot1{,}5=24\ \text{N}\cdot\text{m}"), A(r"M_P+M_{P_1}=54\ \text{N}\cdot\text{m}")]),
  ("Lực căng dây", [P("Thanh cân bằng nên moment của lực căng bằng tổng moment của hai trọng lực:"), M(r"T\cdot d_T=M_P+M_{P_1}"), M(r"T=\dfrac{54}{0{,}6}"), A(r"T=90\ \text{N}")]),
  ("Lực bản lề theo phương thẳng đứng", [P("Thành phần thẳng đứng của lực căng hướng lên:"), M(r"T_y=T\sin30^\circ=90\cdot0{,}5=45\ \text{N}"),
                                         P("Tổng lực theo phương thẳng đứng bằng $0$ (chiều lên là dương):"), M(r"T_y+N_y-P-P_1=0"), M(r"N_y=40+16-45"), A(r"N_y=11\ \text{N}")]),
  ("Hướng của lực bản lề", [A(r"T:$N_y\gt0$ nên thành phần thẳng đứng của lực bản lề hướng <strong>lên</strong>: dây đỡ được $45\ \text{N}$ trong $56\ \text{N}$ trọng lượng, bản lề đỡ nốt phần còn lại.")]),
  ("Kiểm tra", [P(r"Lấy trục qua $B$: lực bản lề ở cách $B$ đoạn $1{,}5\ \text{m}$, thành phần đứng của lực căng cách $B$ đoạn $0{,}3\ \text{m}$ (cả hai hướng lên), trọng lượng thanh cách $B$ đoạn $0{,}75\ \text{m}$ (hướng xuống):"),
                M(r"N_y\cdot1{,}5+T_y\cdot0{,}3=11\cdot1{,}5+45\cdot0{,}3=30\ \text{N}\cdot\text{m}"), M(r"P\cdot0{,}75=40\cdot0{,}75=30\ \text{N}\cdot\text{m}"), P("Hai vế bằng nhau ✓")])],
  [r"a) $T=90\ \text{N}$", r"b) $N_y=11\ \text{N}$, hướng lên"],
  r"Nhận dạng: đề cho <strong>thanh gắn bản lề, dây xiên giữ</strong> → trục qua bản lề để tìm lực căng, rồi tổng lực theo phương đứng bằng $0$."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>lực vuông góc</b> và <b>khoảng cách từ trục</b> → nghĩ tới <b>moment M = F·d</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Cánh tay đòn (đổi ra mét)", "Cánh tay đòn $d$ của lực bằng bao nhiêu mét?", 0.75, "m", 0.005,
       loi=r"Dùng luôn số đo theo cm nên moment gấp $100$ lần giá trị đúng, hoặc lấy bề rộng cửa làm cánh tay đòn trong khi lực không đặt ở mép cửa."),
  buoc("Moment của lực", "Moment $M$ của lực bằng bao nhiêu $\\text{N}\\cdot\\text{m}$?", 15, "N·m", 0.1,
       loi=r"Chia $F$ cho $d$ thay vì nhân, hoặc lấy bề rộng cửa làm cánh tay đòn.",
       ke=[(r"Nhân độ lớn lực với cánh tay đòn (đã đổi ra mét)", True),
           (r"Chia độ lớn lực cho cánh tay đòn", r"Chia cho đơn vị $\text{N}/\text{m}$, không phải đơn vị moment $\text{N}\cdot\text{m}$."),
           (r"Nhân lực với bề rộng cả cánh cửa", r"Cánh tay đòn tính từ trục tới giá của lực. Lực đặt ở điểm đã cho chứ không đặt ở mép cửa, nên bề rộng cửa không phải $d$.")]),
  buoc("Lực đẩy ở điểm gần bản lề", "Đẩy tại điểm cách bản lề $15\\ \\text{cm}$ thì lực cần bao nhiêu $\\text{N}$ để có cùng moment?", 100, "N", 1,
       loi=r"Nhân moment với cánh tay đòn mới thay vì chia, hoặc để cánh tay đòn mới theo cm nên lực lệch nhiều bậc.",
       ke=[(r"Chia moment cho cánh tay đòn mới (đã đổi ra mét)", True),
           (r"Giữ nguyên lực, vì moment đã bằng nhau", r"Giữ nguyên lực mà cánh tay đòn đã đổi thì moment không còn bằng nhau."),
           (r"Nhân moment với cánh tay đòn mới", r"Nhân ra đơn vị $\text{N}\cdot\text{m}^2$, không phải đơn vị lực.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>lực hợp góc</b> với đường nối trục – điểm đặt → nghĩ tới <b>cánh tay đòn d, không phải r</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Cánh tay đòn của lực xiên", "Cánh tay đòn $d$ của lực $F$ bằng bao nhiêu mét?", 0.193, "m", 0.002,
       loi=r"Lấy cánh tay đòn bằng khoảng cách tới điểm đặt, hoặc dùng $\cos40^\circ$ thay cho $\sin40^\circ$."),
  buoc("Moment của lực", "Moment $M$ của lực $F$ bằng bao nhiêu $\\text{N}\\cdot\\text{m}$?", 15.4, "N·m", 0.2,
       loi=r"Nhân $F$ với khoảng cách tới điểm đặt (bỏ qua góc), hoặc nhân với thành phần dọc đường nối núm – tâm của lực.",
       ke=[(r"Nhân độ lớn lực với cánh tay đòn vừa tìm", True),
           (r"Nhân lực với khoảng cách từ trục tới núm", r"Khoảng cách tới núm không phải cánh tay đòn khi lực xiên; cánh tay đòn đo vuông góc tới giá của lực."),
           (r"Nhân thành phần của lực dọc đường nối núm – tâm với khoảng cách tới núm", r"Thành phần dọc đường nối có giá đi qua trục nên không gây quay; thành phần gây quay vuông góc với đường nối.")]),
  buoc("Lực đẩy vuông góc đường nối núm – tâm", "Lực $F_t$ vuông góc đường nối núm – tâm cần bao nhiêu $\\text{N}$ để có cùng moment?", 51.4, "N", 0.6,
       loi=r"Chia moment cho cánh tay đòn cũ của lực xiên nên ra lại đúng lực ban đầu, hoặc vẫn dùng góc $40^\circ$ cho lực mới.",
       ke=[(r"Chia moment cho cánh tay đòn mới của lực vuông góc đường nối", True),
           (r"Chia moment cho cánh tay đòn của lực xiên ở câu a", r"Đó là cánh tay đòn của lực cũ. Lực mới vuông góc đường nối nên có cánh tay đòn khác; chia như vậy chỉ ra lại lực ban đầu."),
           (r"Giữ nguyên lực ban đầu vì cùng moment", r"Lực mới có giá khác lực cũ nên cánh tay đòn khác; cùng moment không có nghĩa là cùng lực.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>hai lực song song, ngược chiều, bằng nhau</b> → nghĩ tới <b>ngẫu lực</b>: hợp lực bằng 0, M = F·d.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Hợp lực của hai lực", "Hợp lực của hai lực này là gì?",
       loi=r"Cộng độ lớn hai lực vì cả hai cùng làm bánh lái quay, hoặc cho rằng có quay thì phải có hợp lực khác không.",
       lua_chon=[(r"Bằng không, vì hai lực song song, ngược chiều, cùng độ lớn", True),
                 (r"Bằng tổng hai độ lớn, vì cả hai cùng làm bánh lái quay", r"Cùng làm quay một chiều không có nghĩa là hai lực cùng chiều. Hai lực ngược chiều nên cộng vectơ cho không."),
                 (r"Khác không, vì bánh lái đang quay nên phải có hợp lực", r"Hợp lực chỉ quyết định chuyển động tịnh tiến của tâm. Ngẫu lực có hợp lực bằng không và chỉ làm vật quay tại chỗ.")]),
  buoc("Moment của ngẫu lực", "Moment $M$ của ngẫu lực bằng bao nhiêu $\\text{N}\\cdot\\text{m}$?", 27, "N·m", 0.2,
       loi=r"Chỉ tính một lực với bán kính nên được nửa moment thật, hoặc cộng hai lực rồi nhân khoảng cách.",
       ke=[(r"Nhân độ lớn một lực với khoảng cách giữa hai giá", True),
           (r"Cộng độ lớn hai lực rồi nhân với khoảng cách giữa hai giá", r"Mỗi lực chỉ có cánh tay đòn bằng một nửa khoảng cách giữa hai giá (trục ở giữa); cộng độ lớn rồi nhân cả khoảng cách là tính cánh tay đòn hai lần."),
           (r"Nhân một lực với bán kính bánh lái", r"Chỉ tính một trong hai lực, trong khi cả hai lực cùng làm quay một chiều nên đều phải tính.")]),
  buoc("Lực mỗi tay để có moment lớn hơn", "Để $M'=36\\ \\text{N}\\cdot\\text{m}$ thì mỗi tay phải đẩy một lực bao nhiêu $\\text{N}$?", 40, "N", 0.5,
       loi=r"Chia moment cho bán kính thay vì khoảng cách giữa hai giá, nên lực tìm được gấp đôi lực cần thiết.",
       ke=[(r"Chia moment cho khoảng cách giữa hai giá", True),
           (r"Chia moment cho bán kính bánh lái", r"Bán kính không phải cánh tay đòn của ngẫu lực; $d$ là khoảng cách giữa hai giá."),
           (r"Nhân moment với khoảng cách giữa hai giá", r"Nhân ra đơn vị $\text{N}\cdot\text{m}^2$, không phải đơn vị lực.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>thanh trên giá đỡ, vật ở hai đầu</b> → nghĩ tới <b>trục qua giá đỡ</b> và <b>trọng lượng thanh ở giữa</b>.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Trọng tâm của thanh", "Trọng tâm $G$ của thanh cách đầu $A$ bao nhiêu mét?", 0.5, "m", 0.005,
       loi=r"Quên rằng thanh có trọng lượng riêng đặt ở trọng tâm, hoặc đặt trọng tâm ở một đầu thanh."),
  buoc("Quy tắc moment, tìm $OA$", "Khoảng cách $OA$ bằng bao nhiêu mét?", 0.375, "m", 0.005,
       loi=r"Bỏ trọng lượng của thanh khỏi phương trình moment, hoặc viết các khoảng cách theo những ẩn khác nhau nên phương trình có hai ẩn.",
       ke=[(r"Chọn trục qua giá đỡ, đặt $OA=x$, viết $OG$ và $OB$ theo $x$ rồi cho hai tổng moment bằng nhau", True),
           (r"Cho tổng các lực bằng không để tìm $OA$", r"Phương trình tổng lực chỉ cho lực của giá đỡ. Vị trí $O$ nằm trong điều kiện về moment."),
           (r"Lấy $OA=OB$ vì thanh đồng chất", r"Đồng chất chỉ cho biết trọng tâm ở giữa thanh, không cho biết vị trí giá đỡ.")]),
  buoc("Lực giá đỡ", "Lực $N$ của giá đỡ tác dụng lên thanh bằng bao nhiêu $\\text{N}$?", 80, "N", 1,
       loi=r"Quên cộng trọng lượng của thanh, hoặc dùng lại phương trình moment quanh $O$ (trong đó $N$ không có mặt).",
       ke=[(r"Cho tổng các lực theo phương thẳng đứng bằng không", True),
           (r"Dùng thêm phương trình moment quanh $O$", r"Quanh $O$ lực $N$ có cánh tay đòn bằng không nên biến mất khỏi phương trình, không tìm được $N$."),
           (r"Lấy $N$ bằng tổng trọng lượng hai khối, bỏ qua thanh", r"Thanh cũng có trọng lượng nên phải có mặt trong phương trình lực.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>thanh gắn bản lề và dây hợp góc với thanh</b> → nghĩ tới <b>trục qua bản lề</b>, cánh tay đòn <b>AC·sinα</b>.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Cánh tay đòn của lực căng", "Cánh tay đòn của lực căng dây đối với trục qua $A$ bằng bao nhiêu mét?", 0.6, "m", 0.01,
       loi=r"Lấy cánh tay đòn bằng khoảng cách tới điểm buộc dây vì nhầm với giá của lực căng."),
  buoc("Moment của hai trọng lực", "Tổng moment của trọng lượng thanh và trọng lượng biển hiệu đối với trục qua $A$ bằng bao nhiêu $\\text{N}\\cdot\\text{m}$?", 54, "N·m", 0.5,
       loi=r"Bỏ trọng lượng thanh, hoặc lấy cánh tay đòn của trọng lượng thanh bằng cả chiều dài thanh thay vì nửa chiều dài.",
       ke=[(r"Chọn trục qua bản lề $A$, cộng moment của trọng lượng thanh (đặt ở trọng tâm) và của biển hiệu", True),
           (r"Bỏ qua trọng lượng thanh vì thanh nằm ngang", r"Thanh đồng chất có trọng lượng riêng đặt ở trọng tâm, cách $A$ nửa chiều dài; không thể bỏ."),
           (r"Lấy cánh tay đòn của trọng lượng thanh bằng cả chiều dài thanh", r"Trọng lượng của thanh đặt ở trọng tâm ở giữa thanh nên cánh tay đòn chỉ bằng nửa chiều dài.")]),
  buoc("Lực căng dây", "Lực căng $T$ của dây bằng bao nhiêu $\\text{N}$?", 90, "N", 1,
       loi=r"Quên nhân $\sin30^\circ$ nên cánh tay đòn của lực căng quá dài, hoặc cho lực căng bằng tổng hai trọng lượng.",
       ke=[(r"Cho moment của lực căng bằng tổng moment của hai trọng lực", True),
           (r"Cho lực căng bằng tổng hai trọng lượng", r"Lực căng được xác định bởi phương trình moment, không phải bằng cách cộng các trọng lượng."),
           (r"Nhân lực căng với $AC$ rồi cho bằng tổng moment", r"Quên $\sin30^\circ$: lực căng xiên với thanh nên cánh tay đòn không phải $AC$.")]),
  buoc("Lực bản lề theo phương thẳng đứng", "Độ lớn thành phần thẳng đứng của lực bản lề bằng bao nhiêu $\\text{N}$?", 11, "N", 0.3,
       loi=r"Cho lực bản lề bằng tổng hai trọng lượng (bỏ dây), hoặc lấy cả lực căng chứ không chỉ thành phần thẳng đứng của nó.",
       ke=[(r"Cho tổng các lực theo phương thẳng đứng bằng không, kể cả thành phần thẳng đứng của lực căng", True),
           (r"Cho lực bản lề theo phương đứng bằng tổng hai trọng lượng", r"Cách này bỏ qua thành phần thẳng đứng của lực căng trong phương trình lực theo phương đứng."),
           (r"Cho lực bản lề bằng đúng lực căng của dây", r"Lực căng xiên nên chỉ thành phần thẳng đứng của nó nằm trong phương trình theo phương đứng.")]),
  buoc("Hướng của lực bản lề", "Thành phần thẳng đứng của lực bản lề hướng lên hay hướng xuống?",
       loi=r"Đoán hướng theo cảm giác mà không xét dấu: thấy dây kéo lên nên cho bản lề kéo xuống.",
       lua_chon=[(r"Hướng lên, vì dây mới đỡ được một phần trọng lượng", True),
                 (r"Hướng xuống, vì dây kéo thanh lên", r"Hướng của lực bản lề do dấu của kết quả quyết định, không đoán theo việc dây kéo lên."),
                 (r"Bằng không, vì đã có dây đỡ", r"Có dây chưa suy ra bản lề không chịu lực theo phương đứng; phải kiểm bằng phương trình lực.")],
       ke=[(r"Xét dấu của kết quả trong phương trình lực theo phương thẳng đứng", True),
           (r"Chọn hướng bản lề ngược chiều trọng lực rồi bỏ qua dấu của kết quả", r"Phải đối chiếu dấu của kết quả với chiều đã chọn; chọn trước rồi bỏ qua dấu có thể sai hướng."),
           (r"Cho lực bản lề nằm ngang vì thanh nằm ngang", r"Thanh nằm ngang không có nghĩa lực bản lề nằm ngang; trọng lượng và dây đều có thành phần thẳng đứng cần cân bằng.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ TỰ LUẬN (ví dụ cũ viết lại sạch, đã tính lại; ví dụ phụ thuộc hình bị bỏ) ═════════════
def tl(k, muc, de, giai):
    return f'<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>{giai}</details>'

TU_LUAN = dict(label="Bài tập tự luận (xếp từ dễ đến khó)", body_html=(
    "<p>Các bài còn lại của bài học, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>"
    + tl(1, "Dễ",
         r"<p>Hai chị em chơi bập bênh có trục quay đặt ở giữa ván, bỏ qua trọng lượng ván. Người chị (bên phải) nặng $P_2=300\ \text{N}$, ngồi cách trục $d_2=1{,}0\ \text{m}$. Người em (bên trái) nặng $P_1=200\ \text{N}$. Người em phải ngồi cách trục bao nhiêu để bập bênh cân bằng?</p>",
         r"<p>Trục qua trục bập bênh, quy tắc moment: $P_1d_1=P_2d_2$.</p><p>$200\,d_1=300\cdot1{,}0$ nên $d_1=1{,}5\ \text{m}$.</p><p>Kiểm tra: người nhẹ hơn ngồi xa trục hơn ✓</p>")
    + tl(2, "Dễ",
         r"<p>Một thanh dài $l=1{,}0\ \text{m}$, khối lượng $m=1{,}5\ \text{kg}$. Một đầu thanh gắn vào trần nhà bằng bản lề, đầu kia được giữ bằng sợi dây treo thẳng đứng. Trọng tâm của thanh cách bản lề $0{,}4\ \text{m}$. Lấy $g=10\ \text{m/s}^2$. Tính lực căng của dây.</p>",
         r"<p>Trục qua bản lề (lực bản lề có $d=0$). Trọng lượng $P=mg=15\ \text{N}$ cách trục $0{,}4\ \text{m}$; lực căng $T$ cách trục $1{,}0\ \text{m}$ (cả hai lực thẳng đứng, thanh nằm ngang).</p><p>$T\cdot l=P\cdot d$ nên $T=\dfrac{15\cdot0{,}4}{1{,}0}=6\ \text{N}$.</p>")
    + tl(3, "Trung bình",
         r"<p>Một cột điện được giữ thẳng đứng nhờ một dây thép buộc vào đầu cột và gắn xuống đất; dây thép hợp với cột góc $30^\circ$. Các dây cáp điện kéo đầu cột một lực $F=500\ \text{N}$ theo phương ngang, vuông góc với cột. Tính lực căng của dây thép để cột cân bằng.</p>",
         r"<p>Trục qua chân cột (lực của đất có $d=0$). Gọi $h$ là chiều cao cột.</p><p>$F$ vuông góc cột nên cánh tay đòn là $h$. Lực căng $T$ hợp với cột góc $30^\circ$ nên cánh tay đòn là $h\sin30^\circ$.</p><p>$F\cdot h=T\cdot h\sin30^\circ$ nên $T=\dfrac{500}{0{,}5}=1000\ \text{N}$.</p>")
    + tl(4, "Trung bình",
         r"<p>Một người nâng một tấm gỗ đồng chất, tiết diện đều, trọng lượng $P=200\ \text{N}$, bằng lực $\vec F$ vuông góc với tấm gỗ, đặt ở đầu trên, để tấm gỗ hợp với mặt đất góc $\alpha=30^\circ$. Đầu dưới tựa trên mặt đất không trượt. Tính độ lớn lực $F$.</p>",
         r"<p>Trục qua đầu dưới của tấm gỗ. Gọi $l$ là chiều dài tấm gỗ.</p><p>$F$ vuông góc tấm gỗ nên cánh tay đòn là $l$. Trọng lượng đặt ở giữa tấm, cánh tay đòn là $\dfrac{l}{2}\cos30^\circ$.</p><p>$F\cdot l=P\cdot\dfrac{l}{2}\cos30^\circ$ nên $F=200\cdot\dfrac{1}{2}\cdot\dfrac{\sqrt3}{2}=50\sqrt3\approx86{,}6\ \text{N}$.</p>")
    + tl(5, "Khó",
         r"<p>Một bánh xe bán kính $R=10\ \text{cm}$, khối lượng $3\ \text{kg}$, nằm sát một bậc cao $h=4\ \text{cm}$. Người ta kéo bánh xe bằng lực $F$ theo phương ngang, đặt vào trục bánh xe, để bánh xe leo lên bậc. Bỏ qua ma sát, lấy $g=10\ \text{m/s}^2$. Tìm lực $F$ nhỏ nhất.</p>",
         r"<p>Khi bánh xe sắp rời mặt đất, nó chỉ còn tiếp xúc ở mép bậc $I$. Chọn trục qua $I$ (lực của bậc có $d=0$).</p><p>Cánh tay đòn của $F$ (nằm ngang) là khoảng cách thẳng đứng từ trục bánh xe tới $I$: $R-h=6\ \text{cm}$.</p><p>Cánh tay đòn của trọng lượng $P=30\ \text{N}$ là khoảng cách ngang từ trục bánh xe tới $I$: $\sqrt{R^2-(R-h)^2}=8\ \text{cm}$.</p><p>$F\cdot6\ge30\cdot8$ nên $F\ge40\ \text{N}$; lực nhỏ nhất là $40\ \text{N}$.</p>")
))

# ═════════════ GHI FILE ═════════════
write(J, 66, "Bài 21. Moment lực. Cân bằng của vật rắn", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
for q, f in zip(d["dang_bai"], FORMS): q["form"] = f
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code)"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
