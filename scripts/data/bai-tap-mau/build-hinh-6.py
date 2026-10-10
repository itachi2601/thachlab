"""Bài tập mẫu Bài 5 "Thuyết động học phân tử chất khí" (Vật lí 12) — lesson_id 6. 5 dạng (quét: ket-qua/6.quet-dang.json).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-6.py   (idempotent) → 6.json (review.checked=false cho tới khi kiểm chéo)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_6 import *

J = os.path.join(HERE, "6.json")
TOP_A = "Nội dung thuyết động học phân tử"
TOP_B = "Mol, số Avogadro và lượng chất khí"

# ═════════════ ĐỀ CÁC DẠNG (dễ → khó) ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Đối chiếu phát biểu với thuyết động học phân tử (Brown, áp suất, nhiệt độ)", topic=TOP_A,
      problem_html=r"""<p>Một hộp kín đựng khói hương. Rọi chùm sáng ngang qua hộp và quan sát bằng kính lúp, thấy mỗi hạt khói là một chấm sáng đi theo đường gấp khúc, không dừng lại. Có bốn phát biểu:</p><ol><li>Hạt khói bị phân tử khí va đập từ mọi phía; hai phía không bao giờ cân bằng nên hạt bị đẩy lệch liên tục.</li><li>Chuyển động của hạt khói chứng tỏ các phân tử khí chuyển động hỗn loạn, không ngừng.</li><li>Áp suất của khí lên thành hộp là do trọng lượng của khí đè xuống đáy hộp.</li><li>Nhiệt độ khí càng cao thì các phân tử khí chuyển động càng chậm.</li></ol><p>Có bao nhiêu phát biểu đúng? Sửa lại các phát biểu sai cho đúng.</p>"""),
 dict(label="Dạng 2 · Dễ · Từ khối lượng khí tính số mol và số phân tử", topic=TOP_B,
      problem_html=r"""<p>Một bình kín chứa $0{,}16\ \text{kg}$ khí oxygen ($\text{O}_2$). Khối lượng mol của oxygen là $M=32\ \text{g/mol}$. Lấy $N_A=6{,}02\cdot10^{23}\ \text{mol}^{-1}$.</p><ol type="a"><li>Tính số mol khí trong bình.</li><li>Tính số phân tử oxygen trong bình.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Từ số phân tử tính khối lượng, thể tích ở đktc và so sánh hai bình", topic=TOP_B,
      problem_html=r"""<p>Một bình kín chứa $1{,}505\cdot10^{23}$ nguyên tử khí helium ở điều kiện tiêu chuẩn ($0\ ^\circ\text{C}$, $1\ \text{atm}$). Khối lượng mol của helium là $4\ \text{g/mol}$. Lấy $N_A=6{,}02\cdot10^{23}\ \text{mol}^{-1}$.</p><ol type="a"><li>Tính số mol helium trong bình.</li><li>Tính khối lượng helium.</li><li>Tính thể tích của bình, theo lít.</li><li>Một bình thứ hai có cùng thể tích, cùng điều kiện, đựng khí hydrogen ($\text{H}_2$, $M=2\ \text{g/mol}$). Tính khối lượng hydrogen và số phân tử hydrogen trong bình thứ hai.</li></ol>"""),
 dict(label="Dạng 4 · Khó · Chuỗi nhiều khâu: thể tích, khối lượng riêng, khối lượng, số mol, số phân tử", topic=TOP_B,
      problem_html=r"""<p>Một giọt nước hình cầu có đường kính $4{,}0\ \text{mm}$. Nước có khối lượng riêng $\rho=1{,}0\ \text{g/cm}^3$ và khối lượng mol $M=18\ \text{g/mol}$. Lấy $N_A=6{,}02\cdot10^{23}\ \text{mol}^{-1}$.</p><ol type="a"><li>Tính thể tích giọt nước, theo $\text{cm}^3$.</li><li>Tính khối lượng giọt nước.</li><li>Tính số mol nước trong giọt.</li><li>Tính số phân tử nước trong giọt.</li></ol>"""),
 dict(label="Dạng 5 · Nâng cao · Khoảng cách giữa các phân tử khí so với kích thước phân tử", topic=TOP_B,
      problem_html=r"""<p>Khí nitrogen ở điều kiện tiêu chuẩn. Coi mỗi phân tử nằm ở tâm một hình lập phương nhỏ; các hình lập phương xếp khít nhau và lấp đầy thể tích khí. Thể tích mol ở điều kiện tiêu chuẩn là $22{,}4\ \text{L}$. Lấy $N_A=6{,}02\cdot10^{23}\ \text{mol}^{-1}$. Đường kính phân tử nitrogen cỡ $D=3{,}0\cdot10^{-10}\ \text{m}$.</p><ol type="a"><li>Tính thể tích của mỗi hình lập phương nhỏ, theo $\text{m}^3$.</li><li>Tính cạnh $d$ của hình lập phương, coi là khoảng cách giữa hai phân tử kề nhau.</li><li>Khoảng cách đó gấp bao nhiêu lần đường kính phân tử? Kết quả khớp với nội dung nào của thuyết động học phân tử?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 [(r'"hộp kín … khói hương … hạt khói đi theo đường gấp khúc"', r"Hộp kín, không gió; hạt khói to hơn phân tử khí rất nhiều", r"⚠ Chuyển động Brown chỉ giải thích được khi tính đến các phân tử khí rất nhỏ va đập vào hạt"),
  (r'"(1) hạt khói bị phân tử khí va đập từ mọi phía … không cân bằng"', r"Phát biểu (1)", r"Nguyên nhân của chuyển động Brown"),
  (r'"(2) chứng tỏ các phân tử khí chuyển động hỗn loạn, không ngừng"', r"Phát biểu (2)", r"Chuyển động Brown là bằng chứng gián tiếp về chuyển động của phân tử"),
  (r'"(3) áp suất … do trọng lượng của khí đè xuống đáy hộp"', r"Phát biểu (3)", r"Áp suất khí tác dụng lên những thành nào? Nguyên nhân gây áp suất theo thuyết"),
  (r'"(4) nhiệt độ càng cao thì … càng chậm"', r"Phát biểu (4)", r"Liên hệ giữa nhiệt độ và tốc độ chuyển động của phân tử"),
  (r'"có bao nhiêu phát biểu đúng?"', r"Cần tìm: số phát biểu đúng", r"Đối chiếu từng phát biểu với thuyết rồi đếm")],
 [(r'"bình kín chứa $0{,}16$ kg khí oxygen"', r"$m=0{,}16$ kg", r"⚠ $M$ tính bằng g/mol nên phải đổi $m$ ra gam trước khi chia"),
  (r'"khối lượng mol $M=32$ g/mol"', r"$M=32$ g/mol", r"$n=\dfrac{m}{M}$"),
  (r'"lấy $N_A=6{,}02\cdot10^{23}$ mol$^{-1}$"', r"$N_A=6{,}02\cdot10^{23}$ mol$^{-1}$", r"$N=n\,N_A$ (số phân tử trong $n$ mol)"),
  (r'"tính số mol khí"', r"Cần $n$", r"$n=\dfrac{m}{M}$"),
  (r'"tính số phân tử oxygen"', r"Cần $N$", r"$N=n\,N_A$")],
 [(r'"$1{,}505\cdot10^{23}$ nguyên tử khí helium"', r"$N=1{,}505\cdot10^{23}$", r"$n=\dfrac{N}{N_A}$"),
  (r'"khối lượng mol của helium là $4$ g/mol"', r"$M=4$ g/mol", r"$m=n\,M$"),
  (r'"ở điều kiện tiêu chuẩn ($0\ ^\circ$C, $1$ atm)"', r"Thể tích mol $22{,}4$ lít", r"⚠ Chỉ ở điều kiện tiêu chuẩn mới dùng $V=22{,}4\,n$ (lít), với mọi chất khí"),
  (r'"tính số mol, khối lượng, thể tích bình"', r"Cần $n$, $m$, $V$", r"$n=\dfrac{N}{N_A}$ ; $m=n\,M$ ; $V=22{,}4\,n$"),
  (r'"bình thứ hai cùng thể tích, cùng điều kiện, đựng $\text{H}_2$"', r"$V$ và điều kiện như bình 1 ; $M'=2$ g/mol", r"⚠ Ở đktc mọi khí có cùng thể tích mol nên cùng thể tích thì cùng số mol ; khối lượng mol khác thì khối lượng khác"),
  (r'"khối lượng hydrogen và số phân tử hydrogen"', r"Cần $m'$, $N'$", r"$m'=n\,M'$ ; $N'=n\,N_A$")],
 [(r'"giọt nước hình cầu, đường kính $4{,}0$ mm"', r"$d=4{,}0$ mm", r"⚠ Thể tích hình cầu $V=\dfrac{\pi d^3}{6}$ ; đổi $d$ ra cm vì $\rho$ cho bằng g/cm$^3$"),
  (r'"khối lượng riêng $\rho=1{,}0$ g/cm$^3$"', r"$\rho=1{,}0$ g/cm$^3$", r"$m=\rho\,V$"),
  (r'"khối lượng mol $M=18$ g/mol"', r"$M=18$ g/mol", r"$n=\dfrac{m}{M}$ (nước là chất lỏng, không dùng $22{,}4$ lít)"),
  (r'"lấy $N_A=6{,}02\cdot10^{23}$ mol$^{-1}$"', r"$N_A=6{,}02\cdot10^{23}$ mol$^{-1}$", r"$N=n\,N_A$"),
  (r'"tính thể tích … khối lượng … số mol … số phân tử"', r"Cần $V$, $m$, $n$, $N$", r"$V\to m\to n\to N$, mỗi đại lượng đi qua đại lượng đứng trước")],
 [(r'"khí nitrogen ở điều kiện tiêu chuẩn … thể tích mol $22{,}4$ L"', r"$V_{mol}=22{,}4$ L", r"⚠ Đổi $1\ \text{L}=10^{-3}\ \text{m}^3$ trước khi tính trong hệ SI"),
  (r'"mỗi phân tử ở tâm một hình lập phương, xếp khít, lấp đầy thể tích"', r"1 phân tử ↔ 1 ô ; $N_A$ ô ↔ 1 mol", r"Thể tích một ô bằng thể tích mol chia cho số phân tử trong một mol"),
  (r'"thể tích của mỗi hình lập phương nhỏ"', r"Cần $V_1$", r"$V_1=\dfrac{V_{mol}}{N_A}$"),
  (r'"cạnh $d$ = khoảng cách giữa hai phân tử kề nhau"', r"Cần $d$", r"$V_1=d^3$ nên $d=\sqrt[3]{V_1}$"),
  (r'"đường kính phân tử $D=3{,}0\cdot10^{-10}$ m"', r"$D=3{,}0\cdot10^{-10}$ m", r"Tỉ số $\dfrac{d}{D}$"),
  (r'"khớp với nội dung nào của thuyết?"', r"So khoảng cách $d$ với kích thước $D$", r"Nội dung 1 của thuyết: kích thước phân tử so với khoảng cách giữa chúng")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = [r"<strong>Khái niệm:</strong> chuyển động Brown là chuyển động gấp khúc, không ngừng của hạt nhỏ lơ lửng trong khí hay lỏng.",
      r"<strong>Thuyết:</strong> phân tử khí chuyển động hỗn loạn, không ngừng ; nhiệt độ càng cao, tốc độ càng lớn.",
      r"<strong>Áp suất:</strong> do vô số va chạm của phân tử vào thành bình, mỗi va chạm tác dụng một lực lên thành.",
      r"⚠ <strong>Điều kiện:</strong> đối chiếu cả phần giải thích của mỗi phát biểu, không chỉ phần đầu nghe quen."]
R2 = [r"<strong>Khái niệm:</strong> mol là lượng chất chứa $N_A$ phân tử ; khối lượng mol $M$ là khối lượng của 1 mol (g/mol).",
      r"<strong>Công thức:</strong> $n=\dfrac{m}{M}$ ; $N=n\,N_A$ với $N_A\approx6{,}02\cdot10^{23}\ \text{mol}^{-1}$.",
      r"⚠ <strong>Điều kiện:</strong> $M$ tính bằng g/mol thì $m$ phải tính bằng gam (đổi $1\ \text{kg}=1000\ \text{g}$)."]
R3 = [r"<strong>Khái niệm:</strong> số mol $n$ nối số phân tử $N$, khối lượng $m$ và thể tích khí $V$.",
      r"<strong>Công thức:</strong> $n=\dfrac{N}{N_A}$ ; $m=n\,M$ ; $V=22{,}4\,n$ (lít, ở đktc).",
      r"⚠ <strong>Điều kiện:</strong> $22{,}4$ lít/mol chỉ đúng ở điều kiện tiêu chuẩn ($0\ ^\circ\text{C}$, $1\ \text{atm}$), cho mọi chất khí.",
      r"Cùng thể tích, cùng điều kiện thì cùng số mol, khác khí thì khác khối lượng."]
R4 = [r"<strong>Khái niệm:</strong> khối lượng riêng $\rho=\dfrac{m}{V}$ nối thể tích và khối lượng của chất.",
      r"<strong>Công thức:</strong> $V=\dfrac{\pi d^3}{6}$ (hình cầu) ; $m=\rho V$ ; $n=\dfrac{m}{M}$ ; $N=n\,N_A$.",
      r"⚠ <strong>Điều kiện:</strong> đổi đơn vị độ dài trước ($1\ \text{mm}=0{,}1\ \text{cm}$) ; $22{,}4$ lít chỉ dùng cho chất khí ở đktc, không dùng cho nước."]
R5 = [r"<strong>Khái niệm:</strong> thể tích mol $V_{mol}$ chứa $N_A$ phân tử, mỗi phân tử chiếm một ô.",
      r"<strong>Công thức:</strong> $V_1=\dfrac{V_{mol}}{N_A}$ ; $V_1=d^3\Rightarrow d=\sqrt[3]{V_1}$.",
      r"<strong>Thuyết:</strong> kích thước phân tử rất nhỏ so với khoảng cách giữa chúng.",
      r"⚠ <strong>Điều kiện:</strong> đổi $22{,}4$ lít sang $\text{m}^3$ ; hình lập phương xếp khít chỉ là ước lượng cỡ độ lớn."]

SOLS = [
 sol(R1, [
  ("Phát biểu (1): nguyên nhân hạt khói đi gấp khúc",
   [P("Hộp kín nên không có gió ; chùm sáng chỉ giúp nhìn thấy hạt."),
    P("Hạt khói to hơn phân tử khí rất nhiều và bị phân tử va đập từ mọi phía. Hai phía không bao giờ cân bằng tuyệt đối nên hạt bị đẩy lệch liên tục."),
    A(r"T:Phát biểu (1) <strong>đúng</strong>.")]),
  ("Phát biểu (2): hạt khói cho biết gì về phân tử",
   [P("Hạt khói không tự đi được, cái đẩy nó là phân tử khí."),
    P("Hạt đi mãi, hướng luôn đổi, nên phân tử khí chuyển động hỗn loạn, không ngừng."),
    A(r"T:Phát biểu (2) <strong>đúng</strong>.")]),
  ("Phát biểu (3): nguồn gốc của áp suất khí",
   [P("Khí tác dụng áp suất lên mọi thành hộp : nắp trên, thành bên và đáy. Trọng lượng chỉ hướng xuống đáy nên không giải thích được."),
    P("Nguyên nhân đúng : vô số va chạm của phân tử vào thành hộp, mỗi va chạm tác dụng một lực nhỏ."),
    A(r"T:Phát biểu (3) <strong>sai</strong>. Sửa : áp suất khí lên thành hộp do vô số va chạm của phân tử khí vào thành hộp.")]),
  ("Phát biểu (4): nhiệt độ và tốc độ phân tử",
   [P("Nhiệt độ càng cao thì phân tử chuyển động càng nhanh, va đập vào hạt khói và thành hộp càng mạnh."),
    A(r"T:Phát biểu (4) <strong>sai</strong>. Sửa : nhiệt độ khí càng cao thì các phân tử khí chuyển động càng nhanh.")]),
  ("Đếm số phát biểu đúng",
   [P("Đúng ở (1) và (2), sai ở (3) và (4):"), M(r"1+1+0+0"), A(r"\text{Số phát biểu đúng}=2")])],
  [r"Có $2$ phát biểu đúng : (1) và (2).", r"Sửa (3) : áp suất khí do vô số va chạm của phân tử vào thành hộp.", r"Sửa (4) : nhiệt độ càng cao, phân tử chuyển động càng nhanh."],
  r"Nhận dạng: đề cho <strong>hiện tượng nhìn thấy</strong> và các phát biểu giải thích → so từng phát biểu với <strong>3 nội dung của thuyết</strong>, đặc biệt phần giải thích."),
 sol(R2, [
  ("Số mol khí",
   [P("$M$ tính bằng g/mol nên đổi khối lượng ra gam :"), M(r"m=0{,}16\ \text{kg}=160\ \text{g}"),
    M(r"n=\dfrac{m}{M}=\dfrac{160}{32}"), A(r"n=5\ \text{mol}")]),
  ("Số phân tử oxygen",
   [P("Một mol chứa $N_A$ phân tử nên $n$ mol chứa :"), M(r"N=n\,N_A=5\cdot6{,}02\cdot10^{23}"), A(r"N=3{,}01\cdot10^{24}\ \text{phân tử}")]),
  ("Kiểm tra",
   [P(r"Đổi ngược : $n\,M=5\cdot32=160\ \text{g}=0{,}16\ \text{kg}$ ✓ khớp khối lượng đề cho."),
    P(r"$N$ gấp $n=5$ lần $N_A$ ✓."),
    P(r"Quên đổi kg ra g sẽ ra $\dfrac{0{,}16}{32}=0{,}005\ \text{mol}$ — nhỏ hơn thực tế $1000$ lần.")])],
  [r"a) $n=5\ \text{mol}$", r"b) $N=3{,}01\cdot10^{24}$ phân tử"],
  r"Nhận dạng: đề cho <strong>khối lượng khí và khối lượng mol</strong> → $n=\dfrac{m}{M}$ (đổi $m$ ra gam), rồi $N=n\,N_A$."),
 sol(R3, [
  ("Số mol helium",
   [M(r"n=\dfrac{N}{N_A}=\dfrac{1{,}505\cdot10^{23}}{6{,}02\cdot10^{23}}"), A(r"n=0{,}25\ \text{mol}")]),
  ("Khối lượng helium",
   [P("Khối lượng bằng số mol nhân khối lượng của 1 mol :"), M(r"m=n\,M=0{,}25\cdot4"), A(r"m=1{,}0\ \text{g}")]),
  ("Thể tích bình",
   [P("Ở điều kiện tiêu chuẩn, 1 mol khí chiếm $22{,}4$ lít :"), M(r"V=22{,}4\,n=22{,}4\cdot0{,}25"), A(r"V=5{,}6\ \text{lít}")]),
  ("Bình thứ hai đựng hydrogen",
   [P("Cùng thể tích, cùng điều kiện tiêu chuẩn nên cùng số mol :"), M(r"n'=n=0{,}25\ \text{mol}"),
    P("Số phân tử cũng bằng bình thứ nhất :"), M(r"N'=n'\,N_A=1{,}505\cdot10^{23}\ \text{phân tử}"),
    P("Khối lượng khác vì khối lượng mol khác :"), M(r"m'=n'\,M'=0{,}25\cdot2"), A(r"m'=0{,}5\ \text{g}")]),
  ("Kiểm tra",
   [P(r"$\dfrac{V}{22{,}4}=\dfrac{5{,}6}{22{,}4}=0{,}25\ \text{mol}$ ✓ khớp câu a."),
    P(r"Hydrogen có khối lượng mol nhỏ hơn helium nên cùng số mol thì nhẹ hơn : $0{,}5\ \text{g}\lt1{,}0\ \text{g}$ ✓.")])],
  [r"a) $n=0{,}25\ \text{mol}$", r"b) $m=1{,}0\ \text{g}$", r"c) $V=5{,}6\ \text{lít}$", r"d) $m'=0{,}5\ \text{g}$ ; $N'=1{,}505\cdot10^{23}$ phân tử"],
  r"Nhận dạng: đề cho <strong>số phân tử</strong> và <strong>điều kiện tiêu chuẩn</strong> → qua số mol : $n=\dfrac{N}{N_A}$, $m=nM$, $V=22{,}4\,n$ ; hai bình cùng $V$ thì cùng $n$."),
 sol(R4, [
  ("Thể tích giọt nước",
   [P(r"Đổi đường kính ra cm vì $\rho$ cho bằng g/cm$^3$ : $d=4{,}0\ \text{mm}=0{,}40\ \text{cm}$."),
    M(r"V=\dfrac{\pi d^3}{6}=\dfrac{\pi\cdot0{,}40^3}{6}"), A(r"V\approx0{,}0335\ \text{cm}^3")]),
  ("Khối lượng giọt nước",
   [M(r"m=\rho\,V=1{,}0\cdot0{,}0335"), A(r"m\approx0{,}0335\ \text{g}")]),
  ("Số mol nước",
   [P(r"Nước là chất lỏng nên dùng khối lượng mol, không dùng $22{,}4$ lít :"), M(r"n=\dfrac{m}{M}=\dfrac{0{,}0335}{18}"), A(r"n\approx1{,}86\cdot10^{-3}\ \text{mol}")]),
  ("Số phân tử nước",
   [M(r"N=n\,N_A=1{,}86\cdot10^{-3}\cdot6{,}02\cdot10^{23}"), A(r"N\approx1{,}12\cdot10^{21}\ \text{phân tử}")]),
  ("Kiểm tra",
   [P(r"Giọt nặng $0{,}0335\ \text{g}$, bằng $\dfrac{0{,}0335}{18}\approx\dfrac{1}{540}$ mol nên $N\approx\dfrac{6{,}02\cdot10^{23}}{540}\approx1{,}1\cdot10^{21}$ ✓."),
    P("Một giọt nhỏ xíu đã chứa cỡ một nghìn tỉ tỉ phân tử.")])],
  [r"a) $V\approx0{,}0335\ \text{cm}^3$", r"b) $m\approx0{,}0335\ \text{g}$", r"c) $n\approx1{,}86\cdot10^{-3}\ \text{mol}$", r"d) $N\approx1{,}12\cdot10^{21}$ phân tử"],
  r"Nhận dạng: đề cho <strong>kích thước vật và khối lượng riêng</strong> → $V\to m=\rho V\to n=\dfrac{m}{M}\to N=n\,N_A$ ; đổi đơn vị độ dài trước."),
 sol(R5, [
  ("Đổi thể tích mol ra mét khối",
   [P(r"$1\ \text{L}=10^{-3}\ \text{m}^3$ nên :"), M(r"V_{mol}=22{,}4\ \text{L}=22{,}4\cdot10^{-3}\ \text{m}^3"), A(r"V_{mol}=0{,}0224\ \text{m}^3")]),
  ("Thể tích của mỗi hình lập phương",
   [P("$N_A$ phân tử chiếm $V_{mol}$, mỗi phân tử chiếm một phần $N_A$ :"), M(r"V_1=\dfrac{V_{mol}}{N_A}=\dfrac{0{,}0224}{6{,}02\cdot10^{23}}"), A(r"V_1\approx3{,}72\cdot10^{-26}\ \text{m}^3")]),
  ("Cạnh hình lập phương",
   [P("Hình lập phương có $V_1=d^3$ :"), M(r"d=\sqrt[3]{V_1}=\sqrt[3]{37{,}2\cdot10^{-27}}"), A(r"d\approx3{,}34\cdot10^{-9}\ \text{m}")]),
  ("So với đường kính phân tử",
   [M(r"\dfrac{d}{D}=\dfrac{3{,}34\cdot10^{-9}}{3{,}0\cdot10^{-10}}"), A(r"\dfrac{d}{D}\approx11\ \text{lần}")]),
  ("Đối chiếu với thuyết",
   [P("Khoảng cách giữa hai phân tử khí lớn gấp cỡ chục lần kích thước phân tử."),
    A(r"T:Khớp nội dung 1 : kích thước phân tử rất nhỏ so với khoảng cách giữa chúng ; vì vậy lực liên kết yếu và khí dễ nén.")]),
  ("Kiểm tra",
   [P(r"$d^3\cdot N_A=(3{,}34\cdot10^{-9})^3\cdot6{,}02\cdot10^{23}\approx0{,}0224\ \text{m}^3$ ✓ khớp $V_{mol}$."),
    P("Quên đổi lít ra mét khối sẽ làm $d$ lớn gấp 10 lần, ra $3{,}34\\cdot10^{-8}\\ \\text{m}$ — vô lí.")])],
  [r"a) $V_1\approx3{,}72\cdot10^{-26}\ \text{m}^3$", r"b) $d\approx3{,}34\cdot10^{-9}\ \text{m}$", r"c) $\dfrac{d}{D}\approx11$ lần ; khớp nội dung : phân tử rất nhỏ so với khoảng cách giữa chúng"],
  r"Nhận dạng: đề hỏi <strong>khoảng cách giữa các phân tử</strong> → $V_1=\dfrac{V_{mol}}{N_A}$, $d=\sqrt[3]{V_1}$, rồi so với kích thước phân tử."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>hạt khói gấp khúc</b> hoặc <b>áp suất khí</b> → nghĩ tới <b>phân tử va chạm hỗn loạn</b>, không phải trọng lượng.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Phát biểu (1): nguyên nhân hạt khói đi gấp khúc", "Điều nào đúng về nguyên nhân khiến hạt khói đi gấp khúc?",
       loi=r"Đổ cho chùm sáng rọi vào hoặc cho dòng khí — trong khi hộp kín, không có gió, còn mọi hạt đi mỗi hạt một kiểu.",
       lua_chon=[(r"Hạt khói bị phân tử khí va đập không cân bằng từ mọi phía", True),
                 (r"Chùm sáng rọi vào đẩy hạt khói đi", r"Chùm sáng chỉ giúp nhìn thấy hạt, không đủ lực đẩy; hộp kín nên cũng không có tác nhân bên ngoài."),
                 (r"Dòng khí trong hộp cuốn mọi hạt khói theo một chiều", r"Dòng khí làm mọi hạt đi cùng chiều, còn thực tế mỗi hạt đi một kiểu và hộp kín không có gió.")]),
  buoc("Phát biểu (2): hạt khói cho biết gì về phân tử", "Chuyển động của hạt khói cho biết điều gì về phân tử khí?",
       loi=r"Cho rằng phân tử khí đứng yên còn hạt khói tự chuyển động — nhưng hạt khói không tự đi được, phải có lực đẩy từ phân tử.",
       lua_chon=[(r"Phân tử khí chuyển động hỗn loạn, không ngừng", True),
                 (r"Phân tử khí đứng yên, chỉ hạt khói chuyển động", r"Nếu phân tử đứng yên thì không có lực va đập nào đẩy hạt khói."),
                 (r"Mọi phân tử khí cùng chuyển động theo một hướng", r"Nếu cùng một hướng, hạt khói sẽ bị cuốn một chiều chứ không đi gấp khúc.")]),
  buoc("Phát biểu (3): nguồn gốc của áp suất khí", "Áp suất khí lên thành hộp sinh ra từ đâu?",
       loi=r"Đổ cho trọng lượng khí đè xuống đáy — quên rằng khí còn tác dụng áp suất lên nắp trên và thành bên.",
       lua_chon=[(r"Từ vô số va chạm của phân tử khí vào thành hộp", True),
                 (r"Từ trọng lượng của khí đè xuống đáy hộp", r"Khí còn tác dụng áp suất lên nắp trên và thành bên, trọng lượng chỉ hướng xuống đáy nên không giải thích được."),
                 (r"Từ lực hút giữa các phân tử khí", r"Lực hút giữa các phân tử khí rất yếu và nằm bên trong khối khí, không tạo ra áp suất lên thành.")]),
  buoc("Phát biểu (4): nhiệt độ và tốc độ phân tử", "Khi nhiệt độ khí tăng thì tốc độ trung bình của phân tử thay đổi thế nào?",
       loi=r"Cho rằng nóng lên thì phân tử mất năng lượng nên chậm lại — ngược với thuyết : nhiệt độ càng cao, chuyển động càng nhanh.",
       lua_chon=[(r"Tăng lên", True),
                 (r"Giảm đi vì phân tử mất năng lượng", r"Ngược lại : nhiệt độ càng cao, phân tử càng có nhiều năng lượng chuyển động nên càng nhanh."),
                 (r"Không đổi vì phân tử luôn chuyển động hỗn loạn", r"Hỗn loạn nói về hướng chuyển động, không nói về tốc độ ; tốc độ phụ thuộc nhiệt độ.")]),
  buoc("Đếm số phát biểu đúng", "Có bao nhiêu phát biểu đúng?", 2, "phát biểu", 0,
       loi=r"Tính cả phát biểu (3) hoặc (4) vì nghe quen tai, hoặc bỏ sót một trong hai phát biểu đúng.")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>khối lượng khí và khối lượng mol</b> → <b>n = m/M</b> (m đổi ra gam), rồi <b>N = n·N_A</b>.",
  cap_do=1, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Số mol khí", "Số mol khí trong bình bằng bao nhiêu?", 5, "mol", 0.05,
       loi=r"Chia thẳng khối lượng tính bằng kg cho $M$ tính bằng g/mol, nên số mol nhỏ hơn thực tế đúng $1000$ lần."),
  buoc("Số phân tử oxygen", "Số phân tử oxygen trong bình?", 3.01, "×10²⁴ phân tử", 0.02,
       loi=r"Chia $n$ cho $N_A$ (ra số rất nhỏ) hoặc nhân $N_A$ với khối lượng thay vì với số mol.",
       ke=[(r"Nhân số mol với $N_A$ : $N=n\,N_A$", True),
           (r"Chia số mol cho $N_A$ : $N=\dfrac{n}{N_A}$", r"Chia ra số rất nhỏ cỡ $10^{-24}$ ; mỗi mol chứa $N_A$ phân tử nên phải nhân với $N_A$."),
           (r"Nhân khối lượng với $N_A$ : $N=m\,N_A$", r"Khối lượng không cho biết số phân tử ; phải đi qua số mol $n=\dfrac{m}{M}$ trước.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>số phân tử và điều kiện tiêu chuẩn</b> → <b>n = N/N_A</b>, rồi <b>m = nM</b> và <b>V = 22,4·n</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Số mol helium", "Số mol helium trong bình?", 0.25, "mol", 0.005,
       loi=r"Nhân $N$ với $N_A$ thay vì chia, hoặc lấy luôn $N$ làm số mol."),
  buoc("Khối lượng helium", "Khối lượng helium trong bình?", 1.0, "g", 0.02,
       loi=r"Chia số mol cho $M$ thay vì nhân, hoặc dùng khối lượng mol của hydrogen.",
       ke=[(r"Nhân số mol với khối lượng mol : $m=n\,M$", True),
           (r"Chia số mol cho khối lượng mol : $m=\dfrac{n}{M}$", r"Khối lượng bằng số mol nhân khối lượng của 1 mol, không chia."),
           (r"Nhân số phân tử với khối lượng mol : $m=N\,M$", r"$N$ là số phân tử ; nhân với $M$ ra giá trị lớn hơn thực tế $N_A$ lần. Phải dùng số mol $n$.")]),
  buoc("Thể tích bình", "Thể tích bình theo lít?", 5.6, "lít", 0.1,
       loi=r"Lấy luôn $22{,}4$ lít làm thể tích bình (đó là thể tích của đúng 1 mol), hoặc nhân $22{,}4$ với khối lượng.",
       ke=[(r"Nhân số mol với $22{,}4$ lít/mol : $V=22{,}4\,n$", True),
           (r"Nhân khối lượng với $22{,}4$ : $V=22{,}4\,m$", r"$22{,}4$ lít là thể tích của 1 mol, không phải của 1 gam ; phải nhân với số mol."),
           (r"Lấy $V=22{,}4$ lít vì đó là thể tích mol", r"$22{,}4$ lít chỉ là thể tích của đúng 1 mol ; bình này không phải 1 mol nên phải nhân với số mol.")]),
  buoc("Bình thứ hai đựng hydrogen", "Khối lượng hydrogen trong bình thứ hai?", 0.5, "g", 0.02,
       loi=r"Cho rằng cùng thể tích thì cùng khối lượng (lấy bằng khối lượng helium), hoặc nghĩ khí nhẹ hơn chiếm ít chỗ hơn nên ít mol hơn.",
       ke=[(r"Cùng thể tích, cùng đktc nên cùng số mol ; khối lượng tính bằng $m'=n\,M'$", True),
           (r"Cùng thể tích nên cùng khối lượng : $m'=m$", r"Cùng thể tích chỉ cho cùng số mol ; hydrogen có khối lượng mol khác helium nên khối lượng khác."),
           (r"Hydrogen nhẹ hơn nên chiếm ít chỗ hơn, số mol ít hơn", r"Ở đktc mọi khí đều có thể tích mol $22{,}4$ lít ; thể tích bằng nhau thì số mol bằng nhau, khí nhẹ hay nặng đều thế.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>kích thước vật, khối lượng riêng</b> → <b>V → m=ρV → n=m/M → N=nN_A</b>, đổi đơn vị trước.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Thể tích giọt nước", "Thể tích giọt nước theo cm³?", 0.0335, "cm³", 0.0005,
       loi=r"Thế $d=4{,}0$ vào công thức khi chưa đổi mm ra cm (ra thể tích lớn hơn $1000$ lần), hoặc dùng $\dfrac{4}{3}\pi d^3$ thay vì $\dfrac{4}{3}\pi r^3$."),
  buoc("Khối lượng giọt nước", "Khối lượng giọt nước?", 0.0335, "g", 0.0005,
       loi=r"Chia thể tích cho khối lượng riêng, hoặc nhân $\rho$ với đường kính thay vì thể tích.",
       ke=[(r"Nhân khối lượng riêng với thể tích : $m=\rho\,V$", True),
           (r"Chia thể tích cho khối lượng riêng : $m=\dfrac{V}{\rho}$", r"Đơn vị ra $\text{cm}^6/\text{g}$, không phải khối lượng ; khối lượng bằng khối lượng riêng nhân thể tích."),
           (r"Nhân khối lượng riêng với đường kính : $m=\rho\,d$", r"$d$ là độ dài, không phải thể tích ; $\rho$ chỉ nhân với thể tích.")]),
  buoc("Số mol nước", "Số mol nước trong giọt?", 1.86, "×10⁻³ mol", 0.03,
       loi=r"Lấy $V$ chia $22{,}4$ — nhưng nước là chất lỏng, thể tích mol $22{,}4$ lít chỉ dùng cho chất khí ở đktc.",
       ke=[(r"Chia khối lượng cho khối lượng mol : $n=\dfrac{m}{M}$", True),
           (r"Chia thể tích cho $22{,}4$ : $n=\dfrac{V}{22{,}4}$", r"$22{,}4$ lít/mol chỉ đúng cho chất khí ở điều kiện tiêu chuẩn ; nước là chất lỏng."),
           (r"Nhân khối lượng với khối lượng mol : $n=m\,M$", r"Đơn vị ra $\text{g}^2/\text{mol}$, vô nghĩa ; số mol là số lần $M$ chứa trong $m$.")]),
  buoc("Số phân tử nước", "Số phân tử nước trong giọt?", 1.12, "×10²¹ phân tử", 0.02,
       loi=r"Chia $n$ cho $N_A$ hoặc nhân $N_A$ với khối lượng, nên ra con số không cỡ $10^{21}$.",
       ke=[(r"Nhân số mol với $N_A$ : $N=n\,N_A$", True),
           (r"Chia số mol cho $N_A$ : $N=\dfrac{n}{N_A}$", r"Ra số cực nhỏ ; mỗi mol chứa $N_A$ phân tử nên phải nhân."),
           (r"Nhân khối lượng với $N_A$ : $N=m\,N_A$", r"Phải đi qua số mol : khối lượng chia $M$ mới cho số mol.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>khoảng cách giữa các phân tử</b> → mỗi phân tử chiếm <b>V₁ = V_mol/N_A</b>, khoảng cách là <b>∛V₁</b>.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Đổi thể tích mol ra mét khối", "Thể tích mol $22{,}4$ lít bằng bao nhiêu $\\text{m}^3$?", 0.0224, "m³", 0.0002,
       loi=r"Đổi sai hệ số ($1\ \text{L}=10^{-3}\ \text{m}^3$) hoặc quên đổi nên cạnh ô ra lớn gấp 10 lần."),
  buoc("Thể tích của mỗi hình lập phương", "Thể tích $V_1$ của mỗi hình lập phương?", 3.72, "×10⁻²⁶ m³", 0.03,
       loi=r"Nhân $V_{mol}$ với $N_A$ thay vì chia, hoặc dùng thể tích của chính phân tử thay cho thể tích ô.",
       ke=[(r"Chia thể tích mol cho $N_A$ : $V_1=\dfrac{V_{mol}}{N_A}$", True),
           (r"Nhân thể tích mol với $N_A$ : $V_1=V_{mol}\,N_A$", r"Ra thể tích lớn hơn cả $V_{mol}$ ; mỗi phân tử chiếm một phần nhỏ của $V_{mol}$."),
           (r"Dùng thể tích phân tử : $V_1=\dfrac{\pi D^3}{6}$", r"Đó là thể tích của chính phân tử ; ô còn gồm khoảng trống quanh phân tử nên lớn hơn rất nhiều.")]),
  buoc("Cạnh hình lập phương", "Cạnh $d$ của hình lập phương?", 3.34, "×10⁻⁹ m", 0.03,
       loi=r"Lấy căn bậc hai thay căn bậc ba, hoặc chọn $d=V_1$ (nhầm thể tích với độ dài).",
       ke=[(r"Lấy căn bậc ba : $d=\sqrt[3]{V_1}$", True),
           (r"Lấy căn bậc hai : $d=\sqrt{V_1}$", r"Căn bậc hai ứng với hình vuông ; hình lập phương có $V_1=d^3$ nên phải lấy căn bậc ba."),
           (r"Lấy luôn $d=V_1$", r"$V_1$ là thể tích ($\text{m}^3$), $d$ là độ dài ($\text{m}$) ; phải lấy căn bậc ba.")]),
  buoc("So với đường kính phân tử", "Khoảng cách $d$ gấp bao nhiêu lần đường kính phân tử?", 11.1, "lần", 0.3,
       loi=r"Lấy $D$ chia $d$ (ra số nhỏ hơn $1$) hoặc nhân hai độ dài với nhau.",
       ke=[(r"Chia $d$ cho $D$ : $\dfrac{d}{D}$", True),
           (r"Chia $D$ cho $d$ : $\dfrac{D}{d}$", r"Ngược rồi : hỏi khoảng cách gấp mấy lần đường kính nên lấy $\dfrac{d}{D}$, kết quả lớn hơn $1$."),
           (r"Nhân hai độ dài : $d\cdot D$", r"Tích hai độ dài là diện tích, không cho biết gấp bao nhiêu lần.")]),
  buoc("Đối chiếu với thuyết", "Kết quả này khớp với nội dung nào của thuyết?",
       loi=r"Cho rằng phân tử khí gần như chạm nhau như ở thể lỏng — trái với kết quả $d$ lớn hơn $D$ cỡ chục lần.",
       lua_chon=[(r"Phân tử khí rất nhỏ so với khoảng cách giữa chúng", True),
                 (r"Phân tử khí nằm sát nhau như ở thể lỏng", r"Khoảng cách lớn hơn đường kính phân tử cỡ chục lần, giữa hai phân tử còn khoảng trống rất lớn."),
                 (r"Kích thước phân tử khí lớn hơn khoảng cách giữa chúng", r"Ngược lại : đường kính $D$ nhỏ hơn khoảng cách $d$ nhiều lần.")],
       ke=[(r"Đối chiếu $d$ và $D$ với các nội dung của thuyết", True),
           (r"Tính tiếp tốc độ trung bình của phân tử", r"Đề không cho dữ kiện về tốc độ, và câu hỏi chỉ yêu cầu nối kết quả với nội dung của thuyết."),
           (r"Tính lại $d$ cho khí oxygen", r"Chất khí khác không làm đổi kết luận cỡ độ lớn, và đề không yêu cầu.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ GHI FILE ═════════════
write(J, 6, "Bài 5. Thuyết động học phân tử chất khí", DANG, BUILD, ANALYSIS, SOLS, None)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["dang_bai"][0]["form"] = "ly_thuyet"     # dạng khái niệm: chủ đề 204 chỉ có 2 câu bai_tap, 127 câu ly_thuyet
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code) — đã tự giải lại bằng Python 10/10/2026"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
