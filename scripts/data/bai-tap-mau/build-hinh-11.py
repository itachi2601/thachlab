"""Bài tập mẫu Bài 10 "Lực từ. Cảm ứng từ" (Vật lí 12) — lesson_id 11. 5 dạng (quét dạng:
scripts/logs/batch-ra-soat/ket-qua/11.quet-dang.json). Hình: hinh_11.py. Ví dụ cũ (8 mục) giữ nguyên vào tu_luan.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-11.py   (idempotent, ghi 11.json với review.checked=false)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_11 import *

J = os.path.join(HERE, "11.json")
T215 = "Quy tắc bàn tay trái, xác định phương chiều lực từ"
T216 = "Tính lực từ F = BIl·sinθ"
T233 = "Cảm ứng từ và đơn vị tesla"
T234 = "Lực từ tác dụng lên khung dây. Ngẫu lực từ"

DANG = [
 dict(label="Dạng 1 · Dễ · Quy tắc bàn tay trái: chiều lực từ", topic=T215,
      problem_html=r"""<p>Đoạn dây dẫn thẳng MN nằm ngang trong mặt phẳng hình vẽ, M ở bên trái, N ở bên phải. Dây đặt trong từ trường đều có các đường sức vuông góc với mặt phẳng hình vẽ và hướng ra phía người nhìn (kí hiệu ⊙). Các hướng "lên", "xuống", "sang trái", "sang phải" là hướng trong mặt phẳng hình vẽ.</p><ol type="a"><li>Cho dòng điện chạy từ M đến N. Lực từ tác dụng lên dây có phương và chiều thế nào?</li><li>Đảo chiều dòng điện (chạy từ N đến M), giữ nguyên từ trường. Lực từ có chiều thế nào?</li><li>Từ tình huống ở câu a, đảo đồng thời cả chiều dòng điện và chiều từ trường (đường sức hướng vào mặt phẳng hình, kí hiệu ⊗). Lực từ có chiều thế nào?</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Tính lực từ F = BIl·sinα khi dây hợp đường sức một góc", topic=T216,
      problem_html=r"""<p>Một đoạn dây dẫn thẳng dài $15\ \text{cm}$ mang dòng điện $4{,}0\ \text{A}$, đặt trong từ trường đều có cảm ứng từ $0{,}25\ \text{T}$. Tính độ lớn lực từ tác dụng lên dây khi:</p><ol type="a"><li>dây vuông góc với đường sức từ;</li><li>dây hợp với đường sức từ góc $30^\circ$;</li><li>dây hợp với đường sức từ góc $150^\circ$;</li><li>dây nằm dọc theo đường sức từ.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Tìm cảm ứng từ B từ lực từ đo được", topic=T233,
      problem_html=r"""<p>Một đoạn dây dẫn thẳng dài $12\ \text{cm}$ có dòng điện $2{,}5\ \text{A}$ chạy qua, đặt trong từ trường đều sao cho dây hợp với đường sức từ góc $30^\circ$. Lực từ đo được tác dụng lên dây là $15\ \text{mN}$.</p><ol type="a"><li>Tính cảm ứng từ $B$ của từ trường.</li><li>Tăng dòng điện lên $5{,}0\ \text{A}$, giữ nguyên dây, vị trí dây và từ trường. Cảm ứng từ tại chỗ đặt dây khi đó bằng bao nhiêu? Lực từ tác dụng lên dây bằng bao nhiêu mN?</li></ol>"""),
 dict(label="Dạng 4 · Khó · Dây nằm cân bằng trong từ trường: chiều dòng điện, cường độ và lực căng", topic=T216,
      problem_html=r"""<p>Đoạn dây đồng MN dài $20\ \text{cm}$, khối lượng $8{,}0\ \text{g}$, được treo nằm ngang bằng hai sợi chỉ nhẹ, mảnh (M ở bên trái, N ở bên phải). Dây nằm trong từ trường đều $B=0{,}10\ \text{T}$ có các đường sức vuông góc với mặt phẳng hình vẽ và hướng ra phía người nhìn (kí hiệu ⊙). Lấy $g=10\ \text{m/s}^2$.</p><ol type="a"><li>Dòng điện phải chạy theo chiều nào và có cường độ bao nhiêu để lực căng của các sợi chỉ bằng không?</li><li>Giảm dòng điện xuống $2{,}4\ \text{A}$ (giữ chiều như câu a). Tổng lực căng của hai sợi chỉ bằng bao nhiêu mN?</li></ol>"""),
 dict(label="Dạng 5 · Khó · Khung dây trong từ trường: lực từng cạnh, hợp lực và mômen ngẫu lực", topic=T234,
      problem_html=r"""<p>Khung dây phẳng hình chữ nhật ABCD có $AB=6{,}0\ \text{cm}$, $BC=4{,}0\ \text{cm}$, gồm $N=50$ vòng, mang dòng điện $I=2{,}0\ \text{A}$. Khung đặt trong từ trường đều $B=0{,}20\ \text{T}$ sao cho mặt phẳng khung song song với đường sức từ và các đường sức vuông góc với cạnh AB. Hình vẽ nhìn dọc theo cạnh AB: cạnh AB và cạnh CD vuông góc với mặt phẳng hình vẽ.</p><ol type="a"><li>Những cạnh nào của khung chịu lực từ? Tính độ lớn lực từ tác dụng lên mỗi cạnh ấy.</li><li>Hợp lực của các lực từ tác dụng lên khung bằng bao nhiêu?</li><li>Tính mômen của ngẫu lực từ làm khung quay.</li><li>Khung quay đến vị trí mà vectơ pháp tuyến của mặt phẳng khung hợp với đường sức từ góc $30^\circ$. Tính mômen của ngẫu lực từ khi đó.</li></ol>"""),
]
BUILD = [d1, d2, d3, d4, d5]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 [("\"Đoạn dây dẫn thẳng MN nằm ngang trong mặt phẳng hình vẽ\"", "MN nằm trong mặt phẳng hình, theo phương ngang", "Lực từ tác dụng lên đoạn dây mang dòng điện đặt trong từ trường"),
  ("\"đường sức vuông góc với mặt phẳng hình vẽ, hướng ra (⊙)\"", r"$\vec B$ hướng ra khỏi mặt phẳng hình", r"⚠ Quy tắc bàn tay trái chỉ dùng khi dây không song song đường sức; dây song song đường sức thì $F=0$"),
  ("\"dòng điện chạy từ M đến N\"", r"$I$ theo chiều M → N", "Chiều từ cổ tay đến ngón tay trùng chiều dòng điện; đường sức xuyên vào lòng bàn tay"),
  ("\"Lực từ có phương và chiều thế nào?\"", r"Cần phương và chiều của $\vec F$", r"Phương vuông góc dây và vuông góc đường sức; chiều là chiều ngón cái choãi $90^\circ$"),
  ("\"Đảo chiều dòng điện (từ N đến M)\"", r"$I$ theo chiều N → M, $\vec B$ giữ nguyên", r"Chiều $\vec F$ phụ thuộc chiều $I$ và chiều $\vec B$"),
  ("\"đảo đồng thời cả chiều dòng điện và chiều từ trường\"", r"$I$ theo N → M; $\vec B$ hướng vào (⊗)", "Xét tác động của từng thay đổi lên chiều lực, rồi ghép hai thay đổi")],
 [("\"dây dẫn thẳng dài $15\\ \\text{cm}$\"", r"$l=15\ \text{cm}$", "Đổi ra mét: $1\\ \\text{cm}=10^{-2}\\ \\text{m}$"),
  ("\"dòng điện $4{,}0\\ \\text{A}$ … cảm ứng từ $0{,}25\\ \\text{T}$\"", r"$I=4{,}0\ \text{A}$; $B=0{,}25\ \text{T}$", r"Lực từ $F=BIl\sin\alpha$"),
  ("\"vuông góc với đường sức từ\"", r"$\alpha=90^\circ$", r"⚠ $\alpha$ là góc giữa đoạn dây và $\vec B$, đi với $\sin\alpha$ (không dùng $\cos\alpha$)"),
  ("\"hợp với đường sức từ góc $30^\\circ$\"", r"$\alpha=30^\circ$", r"Cùng công thức, thay $\alpha$ tương ứng"),
  ("\"hợp với đường sức từ góc $150^\\circ$\"", r"$\alpha=150^\circ$", r"Góc tù vẫn là góc giữa dây và $\vec B$; thế vào $\sin\alpha$"),
  ("\"nằm dọc theo đường sức từ\"", r"Dây song song $\vec B$", r"Xét $\sin\alpha$ khi dây dọc theo đường sức"),
  ("\"Tính độ lớn lực từ\"", r"Cần $F$ ở từng trường hợp", r"$F=BIl\sin\alpha$")],
 [("\"dây dẫn thẳng dài $12\\ \\text{cm}$\"", r"$l=12\ \text{cm}$", "Đổi ra mét"),
  ("\"dòng điện $2{,}5\\ \\text{A}$\"", r"$I=2{,}5\ \text{A}$", r"$F=BIl\sin\alpha$"),
  ("\"dây hợp với đường sức từ góc $30^\\circ$\"", r"$\alpha=30^\circ$", r"⚠ $\alpha$ là góc giữa dây và đường sức; dây không vuông góc đường sức nên không được bỏ $\sin\alpha$"),
  ("\"Lực từ đo được … là $15\\ \\text{mN}$\"", r"$F=15\ \text{mN}$", r"Đổi ra newton: $1\ \text{mN}=10^{-3}\ \text{N}$"),
  ("\"Tính cảm ứng từ $B$\"", r"Cần $B$", r"Đơn vị tesla: $1\ \text{T}=1\ \text{N}/(\text{A}\cdot\text{m})$; $F=BIl\sin\alpha$"),
  ("\"Tăng dòng điện lên $5{,}0\\ \\text{A}$, giữ nguyên … vị trí dây và từ trường\"", r"$I'=5{,}0\ \text{A}$; $l$, $\alpha$ không đổi", r"Xét xem $B$ và $F$ phụ thuộc vào những đại lượng nào"),
  ("\"Lực từ tác dụng lên dây bằng bao nhiêu mN?\"", r"Cần $F'$", r"$F=BIl\sin\alpha$")],
 [("\"dây đồng MN dài $20\\ \\text{cm}$, khối lượng $8{,}0\\ \\text{g}$\"", r"$l=20\ \text{cm}$; $m=8{,}0\ \text{g}$", r"Đổi ra mét, kilôgam; trọng lượng $P=mg$"),
  ("\"treo nằm ngang bằng hai sợi chỉ nhẹ\"", "Dây nằm yên; sợi chỉ chỉ tạo lực căng", r"⚠ Dây nằm yên nên hợp các lực tác dụng lên dây bằng $0$"),
  ("\"đường sức vuông góc với mặt phẳng hình vẽ, hướng ra (⊙)\"", r"$\vec B$ hướng ra khỏi hình; $B=0{,}10\ \text{T}$", r"⚠ Kiểm dây có song song đường sức không, rồi mới dùng bàn tay trái"),
  ("\"lực căng của các sợi chỉ bằng không\"", r"$T=0$", "Liệt kê các lực tác dụng lên dây: trọng lực, lực từ, lực căng"),
  ("\"Dòng điện phải chạy theo chiều nào\"", r"Cần chiều của $I$", "Chiều lực từ xác định bằng bàn tay trái từ chiều $I$ và chiều $\\vec B$"),
  ("\"có cường độ bao nhiêu\"", r"Cần $I$", r"$F=BIl\sin\alpha$"),
  ("\"Giảm dòng điện xuống $2{,}4\\ \\text{A}$\"", r"$I'=2{,}4\ \text{A}$", "Lực từ thay đổi theo cường độ dòng điện"),
  ("\"Tổng lực căng của hai sợi chỉ\"", r"Cần $T$ (tổng hai sợi)", "Dây vẫn nằm yên: viết điều kiện cân bằng các lực")],
 [("\"Khung phẳng ABCD, $AB=6{,}0\\ \\text{cm}$, $BC=4{,}0\\ \\text{cm}$\"", r"$AB=6{,}0\ \text{cm}$; $BC=4{,}0\ \text{cm}$", r"Đổi ra mét; diện tích $S=AB\cdot BC$"),
  ("\"$N=50$ vòng … $I=2{,}0\\ \\text{A}$ … $B=0{,}20\\ \\text{T}$\"", r"$N=50$; $I=2{,}0\ \text{A}$; $B=0{,}20\ \text{T}$", r"Mỗi vòng dây chịu lực như nhau nên lực nhân với $N$; $F=BIl\sin\alpha$"),
  ("\"mặt phẳng khung song song với đường sức, đường sức vuông góc với cạnh AB\"", r"AB $\perp$ $\vec B$; BC, AD nằm trong mặt phẳng khung", r"⚠ Xét từng cạnh với đường sức: cạnh song song đường sức thì $F=0$"),
  ("\"Tính độ lớn lực từ tác dụng lên mỗi cạnh ấy\"", r"Cần $F$ mỗi cạnh chịu lực", r"$F=BIl\sin\alpha$ cho cả $N$ vòng"),
  ("\"Hợp lực của các lực từ tác dụng lên khung\"", "Cần hợp lực", "Cộng vectơ các lực từ lên bốn cạnh"),
  ("\"mômen của ngẫu lực từ làm khung quay\"", r"Cần $M$", r"⚠ $M=NBIS\sin\alpha$, trong đó $\alpha$ là góc giữa $\vec B$ và pháp tuyến của khung"),
  ("\"vectơ pháp tuyến … hợp với đường sức từ góc $30^\\circ$\"", r"$\alpha=30^\circ$", r"⚠ $\alpha$ là góc giữa $\vec B$ và pháp tuyến, không phải góc giữa $\vec B$ và mặt phẳng khung")],
]

# ═════════════ LỜI GIẢI ═════════════
RC1 = [r"<strong>Khái niệm:</strong> lực từ lên đoạn dây mang dòng điện có điểm đặt ở trung điểm, phương vuông góc dây và vuông góc đường sức từ.",
       r"<strong>Quy tắc bàn tay trái:</strong> đường sức xuyên vào lòng bàn tay, chiều từ cổ tay đến ngón tay trùng chiều $I$, ngón cái choãi $90^\circ$ chỉ chiều $\vec F$.",
       r"<strong>Kí hiệu:</strong> ⊙ hướng ra khỏi mặt phẳng hình, ⊗ hướng vào mặt phẳng hình.",
       r"⚠ <strong>Điều kiện:</strong> dây không song song đường sức; song song thì $F=0$."]
RC2 = [r"<strong>Khái niệm:</strong> $\alpha$ là góc giữa đoạn dây và $\vec B$; $l$ là chiều dài đoạn dây trong từ trường (mét).",
       r"<strong>Định luật:</strong> lực từ tỉ lệ với $B$, $I$, $l$ và $\sin\alpha$.",
       r"<strong>Công thức:</strong> $F=BIl\sin\alpha$.",
       r"⚠ <strong>Điều kiện:</strong> đổi $l$ ra mét; $\alpha=0^\circ$ hoặc $180^\circ$ thì $F=0$, $\alpha=90^\circ$ thì $F=BIl$."]
RC3 = [r"<strong>Khái niệm:</strong> cảm ứng từ $B$ đặc trưng cho từ trường về mặt tác dụng lực; đơn vị tesla, $1\ \text{T}=1\ \text{N}/(\text{A}\cdot\text{m})$.",
       r"<strong>Định luật:</strong> $F=BIl\sin\alpha$, giải ngược để tìm $B$.",
       r"<strong>Công thức:</strong> $B=\dfrac{F}{Il\sin\alpha}$.",
       r"⚠ <strong>Điều kiện:</strong> $F$ đổi ra N, $l$ ra m; $B$ là tính chất của từ trường tại chỗ đặt dây, không phụ thuộc dòng điện thử."]
RC4 = [r"<strong>Khái niệm:</strong> dây nằm yên thì hợp lực tác dụng lên dây bằng $0$; trọng lượng $P=mg$.",
       r"<strong>Định luật:</strong> chiều lực từ theo bàn tay trái; độ lớn $F=BIl\sin\alpha$.",
       r"<strong>Công thức:</strong> lực căng bằng $0$ thì $F=P$; lực căng khác $0$ thì $T+F=P$ (lực từ hướng lên).",
       r"⚠ <strong>Điều kiện:</strong> lực từ phải hướng lên mới đỡ được trọng lượng; đổi $g$ sang kg, mN sang N khi thế số."]
RC5 = [r"<strong>Khái niệm:</strong> khung có $N$ vòng, mỗi cạnh chịu lực nhân với $N$; hai cạnh đối diện chịu hai lực cùng độ lớn, ngược chiều, không cùng giá là ngẫu lực từ.",
       r"<strong>Định luật:</strong> ngẫu lực có hợp lực bằng $0$ nhưng mômen khác $0$ nên làm khung quay.",
       r"<strong>Công thức:</strong> $F=NBIl\sin\alpha$ cho một cạnh · $M=NBIS\sin\alpha$.",
       r"⚠ <strong>Điều kiện:</strong> cạnh song song đường sức không chịu lực; $\alpha$ trong $M$ là góc giữa $\vec B$ và pháp tuyến khung, $M_{\max}=NBIS$ khi mặt phẳng khung song song đường sức."]

SOLS = [
 sol(RC1, [
  ("Kiểm tra dây với đường sức", [P("Dây MN nằm trong mặt phẳng hình, đường sức vuông góc với mặt phẳng hình nên dây vuông góc với đường sức."), A("T:Có lực từ, dùng được quy tắc bàn tay trái.")]),
  ("Phương của lực từ", [P("Lực từ vuông góc với dây (phương ngang) và vuông góc với đường sức (phương ra khỏi hình)."), A("T:Lực từ có phương thẳng đứng, nằm trong mặt phẳng hình.")]),
  ("Chiều lực khi dòng điện từ M đến N (câu a)", [P("Đặt bàn tay trái sao cho đường sức ⊙ xuyên vào lòng bàn tay; chiều từ cổ tay đến ngón tay hướng sang phải (chiều $I$). Ngón cái choãi $90^\\circ$ chỉ xuống."), A("T:Lực từ hướng xuống.")]),
  ("Đảo chiều dòng điện (câu b)", [P("Chiều ngón tay quay sang trái, đường sức vẫn xuyên vào lòng bàn tay, ngón cái chỉ lên."), A("T:Lực từ hướng lên; độ lớn không đổi.")]),
  ("Đảo cả dòng điện và từ trường (câu c)", [P("Đảo chiều $I$ thì chiều lực đổi một lần."), P("Đảo thêm chiều $\\vec B$ thì chiều lực đổi thêm một lần nữa."), A("T:Lực từ trở lại hướng xuống, giống câu a.")]),
  ("Kiểm tra", [P("Mỗi lần đảo một yếu tố ($I$ hoặc $\\vec B$) thì lực đổi chiều; đảo hai yếu tố thì kết quả trùng với ban đầu."), P("Lực luôn nằm trên phương thẳng đứng, vuông góc dây và đường sức.")])],
  ["a) Lực từ có phương thẳng đứng, chiều hướng xuống", "b) Lực từ hướng lên", "c) Lực từ hướng xuống, như câu a"],
  r"Nhận dạng: đề cho <strong>chiều dòng điện và hướng đường sức (⊙, ⊗)</strong> → dùng <strong>quy tắc bàn tay trái</strong>; đảo một yếu tố thì đổi chiều lực."),
 sol(RC2, [
  ("Đổi chiều dài ra mét", [M(r"l=15\ \text{cm}=0{,}15\ \text{m}"), A(r"l=0{,}15\ \text{m}")]),
  ("Dây vuông góc đường sức (câu a)", [P("$\\alpha=90^\\circ$ nên $\\sin\\alpha=1$:"), M(r"F=BIl\sin\alpha=0{,}25\cdot4{,}0\cdot0{,}15\cdot1"), A(r"F=0{,}15\ \text{N}")]),
  ("Dây hợp đường sức góc $30^\\circ$ (câu b)", [M(r"F=0{,}25\cdot4{,}0\cdot0{,}15\cdot\sin30^\circ"), M(r"F=0{,}15\cdot0{,}5"), A(r"F=0{,}075\ \text{N}")]),
  ("Dây hợp đường sức góc $150^\\circ$ (câu c)", [P("$\\sin150^\\circ=\\sin30^\\circ=0{,}5$ nên:"), M(r"F=0{,}15\cdot0{,}5"), A(r"F=0{,}075\ \text{N}")]),
  ("Dây dọc theo đường sức (câu d)", [P("$\\alpha=0^\\circ$ nên $\\sin\\alpha=0$:"), M(r"F=0{,}25\cdot4{,}0\cdot0{,}15\cdot0"), A(r"F=0")]),
  ("Kiểm tra", [P("Lực lớn nhất khi vuông góc đường sức; giảm dần khi dây nghiêng, bằng $0$ khi dây dọc theo đường sức."), P("Hai góc bù nhau ($30^\\circ$ và $150^\\circ$) cho cùng độ lớn lực; chiều lực khác nhau do bàn tay trái.")])],
  ["a) $F=0{,}15\\ \\text{N}$", "b) $F=0{,}075\\ \\text{N}$", "c) $F=0{,}075\\ \\text{N}$", "d) $F=0$"],
  r"Nhận dạng: đề cho <strong>dây hợp đường sức góc $\alpha$</strong> và dài tính bằng cm → <strong>$F=BIl\sin\alpha$</strong>, đổi cm ra mét."),
 sol(RC3, [
  ("Đổi đơn vị sang SI", [M(r"l=12\ \text{cm}=0{,}12\ \text{m}"), M(r"F=15\ \text{mN}=0{,}015\ \text{N}"), A(r"l=0{,}12\ \text{m}\ ;\ F=0{,}015\ \text{N}")]),
  ("Cảm ứng từ B (câu a)", [P("Giải ngược $F=BIl\\sin\\alpha$ với $\\sin30^\\circ=0{,}5$:"), M(r"B=\dfrac{F}{Il\sin\alpha}=\dfrac{0{,}015}{2{,}5\cdot0{,}12\cdot0{,}5}"), M(r"B=\dfrac{0{,}015}{0{,}15}"), A(r"B=0{,}10\ \text{T}")]),
  ("Cảm ứng từ khi tăng dòng điện (câu b)", [P("$B$ là tính chất của từ trường tại chỗ đặt dây; dòng điện của dây chỉ dùng để đo."), A(r"B=0{,}10\ \text{T}\ \text{(không đổi)}")]),
  ("Lực từ khi dòng điện $5{,}0\\ \\text{A}$ (câu b)", [M(r"F'=BI'l\sin\alpha=0{,}10\cdot5{,}0\cdot0{,}12\cdot0{,}5"), M(r"F'=0{,}030\ \text{N}"), A(r"F'=30\ \text{mN}")]),
  ("Kiểm tra", [P("$B$ có cỡ $0{,}1$ T, hợp lí với khe nam châm chữ U."), P("Dòng điện tăng gấp đôi thì lực từ tăng gấp đôi ($15\\ \\text{mN}\\to30\\ \\text{mN}$), còn $B$ giữ nguyên.")])],
  ["a) $B=0{,}10\\ \\text{T}$", "b) $B=0{,}10\\ \\text{T}$ (không đổi); $F'=30\\ \\text{mN}$"],
  r"Nhận dạng: đề cho <strong>lực đo được, $I$, $l$, góc</strong> và hỏi $B$ → <strong>$B=\dfrac{F}{Il\sin\alpha}$</strong>; $B$ không đổi khi đổi dòng thử."),
 sol(RC4, [
  ("Chiều dòng điện để lực từ hướng lên (câu a)", [P("Đường sức ⊙ xuyên vào lòng bàn tay trái. Muốn ngón cái chỉ lên thì chiều từ cổ tay đến ngón tay phải hướng sang trái, tức dòng điện chạy từ N đến M."), A("T:Dòng điện chạy từ N đến M.")]),
  ("Trọng lượng của dây (câu a)", [M(r"m=8{,}0\ \text{g}=0{,}008\ \text{kg}"), M(r"P=mg=0{,}008\cdot10"), A(r"P=0{,}080\ \text{N}")]),
  ("Cường độ dòng điện (câu a)", [P("Lực căng bằng $0$ nên lực từ đỡ cả trọng lượng; dây vuông góc đường sức ($\\sin\\alpha=1$):"), M(r"BIl=P"), M(r"I=\dfrac{P}{Bl}=\dfrac{0{,}080}{0{,}10\cdot0{,}20}"), A(r"I=4{,}0\ \text{A}")]),
  ("Lực từ khi $I'=2{,}4\\ \\text{A}$ (câu b)", [M(r"F'=BI'l=0{,}10\cdot2{,}4\cdot0{,}20"), M(r"F'=0{,}048\ \text{N}"), A(r"F'=48\ \text{mN}")]),
  ("Tổng lực căng (câu b)", [P("Dây vẫn nằm yên, lực từ hướng lên cùng chiều lực căng:"), M(r"T+F'=P"), M(r"T=P-F'=80-48"), A(r"T=32\ \text{mN}")]),
  ("Kiểm tra", [P("Mỗi sợi chỉ chịu $16\\ \\text{mN}$, nhỏ hơn nửa trọng lượng $40\\ \\text{mN}$: hợp lí vì lực từ đỡ bớt một phần."), P("Với $I=4{,}0\\ \\text{A}$ thì $F=80\\ \\text{mN}=P$, lực căng bằng $0$ đúng như đề.")])],
  ["a) Dòng điện chạy từ N đến M; $I=4{,}0\\ \\text{A}$", "b) Tổng lực căng $T=32\\ \\text{mN}$"],
  r"Nhận dạng: đề nói <strong>dây nằm yên, lực căng bằng không hoặc cho trọng lượng</strong> → <strong>lực từ cân bằng trọng lượng</strong>; chiều $I$ lấy bằng bàn tay trái."),
 sol(RC5, [
  ("Cạnh nào chịu lực (câu a)", [P("AB và CD vuông góc đường sức nên chịu lực."), P("BC và AD song song đường sức ($\\alpha=0^\\circ$) nên $F=0$."), A("T:Chỉ AB và CD chịu lực từ.")]),
  ("Lực từ lên cạnh AB và CD (câu a)", [P("Khung có $N=50$ vòng, mỗi vòng chịu lực như nhau:"), M(r"F=NBI\cdot AB=50\cdot0{,}20\cdot2{,}0\cdot0{,}060"), A(r"F_{AB}=F_{CD}=1{,}2\ \text{N}")]),
  ("Hợp lực lên khung (câu b)", [P("Hai lực lên AB và CD cùng độ lớn, ngược chiều:"), M(r"\vec F_{AB}+\vec F_{CD}=\vec 0"), A("T:Hợp lực bằng 0, khung chỉ quay, không dịch chuyển.")]),
  ("Diện tích khung", [M(r"S=AB\cdot BC=0{,}060\cdot0{,}040"), A(r"S=2{,}4\cdot10^{-3}\ \text{m}^2")]),
  ("Mômen ngẫu lực lúc đầu (câu c)", [P("Mặt phẳng khung song song đường sức nên pháp tuyến vuông góc đường sức, $\\alpha=90^\\circ$:"), M(r"M=NBIS\sin90^\circ=50\cdot0{,}20\cdot2{,}0\cdot2{,}4\cdot10^{-3}"), A(r"M=0{,}048\ \text{N·m}")]),
  ("Mômen khi pháp tuyến hợp đường sức $30^\\circ$ (câu d)", [M(r"M=NBIS\sin30^\circ=0{,}048\cdot0{,}5"), A(r"M=0{,}024\ \text{N·m}")]),
  ("Kiểm tra", [P("Cách khác cho câu c: hai lực $1{,}2$ N cách nhau $BC=0{,}040$ m, $M=F\\cdot BC=1{,}2\\cdot0{,}040=0{,}048\\ \\text{N·m}$, khớp."), P("Khi pháp tuyến quay từ $90^\\circ$ về $30^\\circ$ so với $\\vec B$, mômen giảm còn một nửa; mặt phẳng khung vuông góc đường sức thì $M=0$.")])],
  ["a) Hai cạnh AB và CD, mỗi cạnh $1{,}2\\ \\text{N}$", "b) Hợp lực bằng $0$", "c) $M=0{,}048\\ \\text{N·m}$", "d) $M=0{,}024\\ \\text{N·m}$"],
  r"Nhận dạng: đề cho <strong>khung dây $N$ vòng trong từ trường, hỏi mômen</strong> → <strong>$M=NBIS\sin\alpha$</strong>, $\alpha$ là góc giữa $\vec B$ và pháp tuyến."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC (khớp 1-1 với .bt-step của SOLS) ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>chiều dòng điện và đường sức ⊙, ⊗</b> → nghĩ tới <b>quy tắc bàn tay trái</b>; đảo một yếu tố, lực đổi chiều.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Kiểm tra dây với đường sức", "Dây MN và đường sức hợp với nhau thế nào?",
       loi=r"Thấy dây «nằm trong từ trường» là kết luận ngay mà không kiểm góc, hoặc nhầm mặt phẳng hình với đường sức.",
       lua_chon=[(r"Vuông góc nhau, nên có lực từ", True),
                 (r"Song song nhau, nên $F=0$", r"Dây nằm trong mặt phẳng hình còn đường sức vuông góc mặt phẳng ấy, nên không thể song song."),
                 (r"Chưa biết được vì đề không cho độ lớn của $B$", r"Chỉ cần biết góc giữa dây và đường sức để biết có lực hay không; độ lớn $B$ chỉ ảnh hưởng độ lớn lực.")]),
  buoc("Phương của lực từ", "Lực từ có phương nào?",
       loi=r"Cho lực từ nằm dọc theo dây hoặc dọc theo đường sức.",
       lua_chon=[(r"Thẳng đứng, trong mặt phẳng hình", True),
                 (r"Nằm ngang, dọc theo dây", r"Lực từ luôn vuông góc với dây; lực dọc dây chỉ kéo căng dây, không làm dây lệch."),
                 (r"Vuông góc mặt phẳng hình, cùng phương đường sức", r"Lực từ vuông góc với đường sức, không cùng phương với nó.")],
       ke=[(r"Xác định phương: vuông góc với dây và vuông góc với đường sức", True),
           (r"Tính $F=BIl$ ngay", r"Đề chỉ hỏi phương và chiều, không cho số để tính độ lớn."),
           (r"Dùng quy tắc nắm tay phải", r"Nắm tay phải tìm chiều đường sức của dòng điện, không tìm chiều lực từ.")]),
  buoc("Chiều lực khi dòng điện từ M đến N", "Với dòng điện từ M đến N, lực từ hướng nào?",
       loi=r"Đặt tay cho đường sức đâm vào mu bàn tay thay vì lòng bàn tay, hoặc nhầm chiều ngón tay nên ra chiều ngược lại.",
       lua_chon=[(r"Xuống", True),
                 (r"Lên", r"Kiểm lại: ngón tay theo chiều $I$ (sang phải), đường sức ⊙ xuyên vào lòng bàn tay; ngón cái không hướng lên."),
                 (r"Sang phải, cùng chiều dòng điện", r"Lực từ vuông góc với dây, không cùng phương với dòng điện.")],
       ke=[(r"Bàn tay trái: đường sức xuyên vào lòng bàn tay, ngón tay theo chiều $I$, ngón cái chỉ chiều lực", True),
           (r"Bàn tay phải: ngón cái theo $I$, bốn ngón khum theo chiều lực", r"Đó là quy tắc nắm tay phải, dùng tìm chiều đường sức, không phải chiều lực từ."),
           (r"Lấy chiều lực cùng chiều với đường sức ⊙", r"Lực từ vuông góc với đường sức, không cùng chiều với nó.")]),
  buoc("Đảo chiều dòng điện", "Đảo chiều dòng điện thì lực từ hướng nào?",
       loi=r"Cho rằng lực không đổi vì độ lớn $I$ và $B$ không đổi, quên rằng chiều lực phụ thuộc chiều $I$.",
       lua_chon=[(r"Lên", True),
                 (r"Xuống, như cũ", r"Độ lớn lực không đổi nhưng chiều lực phụ thuộc chiều $I$; đảo $I$ thì chiều lực đổi."),
                 (r"Sang trái, cùng chiều dòng điện mới", r"Lực từ vuông góc với dây, không cùng phương với dòng điện.")],
       ke=[(r"Giữ nguyên đường sức, đổi chiều ngón tay theo $I$ mới rồi đọc chiều ngón cái", True),
           (r"Lực không đổi vì $B$, $I$, $l$ không đổi", r"Độ lớn không đổi nhưng chiều lực đổi theo chiều $I$."),
           (r"Tính lại $F=BIl\sin\alpha$", r"Đề chỉ hỏi chiều, không cho số để tính.")]),
  buoc("Đảo cả dòng điện và từ trường", "Đảo cả chiều dòng điện và chiều từ trường thì lực từ hướng nào?",
       loi=r"Cho rằng hai lần đảo triệt tiêu nên lực bằng không, hoặc chỉ tính một lần đảo.",
       lua_chon=[(r"Xuống, như câu a", True),
                 (r"Lên", r"Chỉ một yếu tố đảo mới làm lực đổi chiều; đảo cả hai thì lực đổi chiều hai lần."),
                 (r"Bằng không, vì hai lần đảo triệt tiêu nhau", r"Hai lần đảo chiều trả chiều lực về như cũ, nhưng độ lớn vẫn là $BIl$, không bằng không.")],
       ke=[(r"Xét riêng tác động của từng lần đảo lên chiều lực, rồi ghép lại", True),
           (r"Đảo hai yếu tố thì lực đổi chiều hai lần nên bằng không", r"Đổi chiều hai lần đưa chiều lực về như cũ, không làm lực mất đi."),
           (r"Chỉ cần đảo $\vec B$, vì đảo $I$ không ảnh hưởng", r"Đảo $I$ cũng làm lực đổi chiều.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>dây hợp đường sức góc α</b>, chiều dài tính bằng cm → nghĩ tới <b>F = BIl·sinα</b>, đổi cm ra mét.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Đổi chiều dài ra mét", "Chiều dài dây theo mét là bao nhiêu?", 0.15, "m", 0.005,
       loi=r"Thế thẳng số đo bằng cm vào công thức, làm lực lớn gấp 100 lần."),
  buoc("Dây vuông góc đường sức", "Lực từ khi dây vuông góc đường sức là bao nhiêu newton?", 0.15, "N", 0.005,
       loi=r"Dùng $\cos\alpha$ thay cho $\sin\alpha$ nên ra lực bằng không khi dây vuông góc đường sức.",
       ke=[(r"Xác định $\alpha$ khi dây vuông góc đường sức rồi thế vào $F=BIl\sin\alpha$", True),
           (r"Vuông góc nên $\sin\alpha=0$ và $F=0$", r"$\sin90^\circ=1$; dây vuông góc đường sức là lúc lực lớn nhất."),
           (r"Dùng $\cos\alpha$ thay cho $\sin\alpha$", r"Công thức có $\sin\alpha$; $\cos90^\circ=0$ cho lực bằng không, vô lí khi dây vuông góc đường sức.")]),
  buoc("Dây hợp đường sức 30°", "Lực từ khi dây hợp với đường sức góc 30° là bao nhiêu newton?", 0.075, "N", 0.003,
       loi=r"Dùng $\cos30^\circ$ hoặc $\sin60^\circ$ (góc phụ) thay cho $\sin30^\circ$.",
       ke=[(r"Thế $\alpha=30^\circ$ vào $F=BIl\sin\alpha$", True),
           (r"$F=BIl\cos30^\circ$", r"$\alpha$ là góc giữa dây và đường sức, đi với $\sin\alpha$; dùng $\cos$ cho kết quả sai."),
           (r"$F=BIl\sin60^\circ$, lấy góc phụ với đường sức", r"Đề cho góc giữa dây và đường sức là $30^\circ$, không phải $60^\circ$.")]),
  buoc("Dây hợp đường sức 150°", "Lực từ khi dây hợp với đường sức góc 150° là bao nhiêu newton?", 0.075, "N", 0.003,
       loi=r"Cho rằng góc tù thì $\sin$ âm hoặc lực bằng không, hoặc bấm máy tính ở chế độ radian.",
       ke=[(r"Thế $\alpha=150^\circ$ vào $F=BIl\sin\alpha$", True),
           (r"$\sin150^\circ$ âm nên lực ngược chiều và có độ lớn khác", r"$\sin150^\circ$ dương, bằng $\sin30^\circ$; chiều lực xét bằng bàn tay trái, không xét bằng dấu của $\sin$."),
           (r"Góc tù thì $F=0$ như dây song song đường sức", r"$F=0$ chỉ khi $\alpha=0^\circ$ hoặc $180^\circ$.")]),
  buoc("Dây dọc theo đường sức", "Lực từ khi dây nằm dọc theo đường sức là bao nhiêu newton?", 0, "N", 0.001,
       loi=r"Cho rằng dây «nằm trong» từ trường thì vẫn có lực, hoặc lấy $\alpha=90^\circ$.",
       ke=[(r"Xác định $\alpha$ khi dây dọc theo đường sức rồi thế vào công thức", True),
           (r"$\alpha=90^\circ$ vì dây nằm trong từ trường nên lực lớn nhất", r"$\alpha=90^\circ$ là dây vuông góc đường sức; dọc theo đường sức thì $\alpha=0^\circ$."),
           (r"$B$ vẫn khác không nên $F$ vẫn khác không", r"$F$ còn phụ thuộc $\sin\alpha$; $\sin\alpha=0$ thì $F=0$ dù $B$ khác không.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>lực từ đo được, hỏi B</b> → nghĩ tới <b>B = F/(Il·sinα)</b>; B không đổi khi đổi dòng thử.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Đổi đơn vị sang SI", "Lực từ 15 mN bằng bao nhiêu newton?", 0.015, "N", 0.0005,
       loi=r"Đổi mN sang N sai hệ số ($10^{-2}$ hoặc $10^{-6}$) hoặc để nguyên mN khi thế số."),
  buoc("Cảm ứng từ B", "Cảm ứng từ B bằng bao nhiêu tesla?", 0.10, "T", 0.005,
       loi=r"Bỏ $\sin\alpha$ vì lực đã «đo được», làm B nhỏ hơn thực tế; hoặc nhân thay vì chia.",
       ke=[(r"Giải ngược $F=BIl\sin\alpha$ cho $B$, giữ $\sin\alpha$ rồi thế số", True),
           (r"$B=F\cdot Il\sin\alpha$", r"Từ $F=BIl\sin\alpha$ phải chia hai vế cho $Il\sin\alpha$; nhân sẽ sai đơn vị tesla."),
           (r"Bỏ $\sin\alpha$ vì lực đã đo được", r"Lực đo được là lực tại góc $30^\circ$ nên phải giữ $\sin\alpha$; bỏ đi sẽ ra $B$ nhỏ hơn thực tế.")]),
  buoc("Cảm ứng từ khi tăng dòng điện", "Tăng dòng điện lên 5,0 A thì cảm ứng từ tại chỗ đặt dây bằng bao nhiêu tesla?", 0.10, "T", 0.005,
       loi=r"Thấy $I$ ở mẫu số của $B=\dfrac{F}{Il\sin\alpha}$ nên tưởng $B$ giảm khi $I$ tăng, quên rằng $F$ cũng tăng theo.",
       ke=[(r"Xét xem $B$ có do dòng điện của dây tạo ra hay không", True),
           (r"$B$ tỉ lệ nghịch với $I$ theo công thức nên giảm đi một nửa", r"Công thức chỉ là cách đo; $F$ cũng tăng theo $I$ nên thương số không đổi."),
           (r"$B$ tăng theo vì dòng điện mạnh hơn", r"Dòng điện của dây chỉ để đo; từ trường có sẵn ở chỗ đó, không đổi.")]),
  buoc("Lực từ khi dòng điện 5,0 A", "Lực từ khi dòng điện 5,0 A là bao nhiêu mN?", 30, "mN", 0.5,
       loi=r"Giữ nguyên lực cũ vì cho rằng lực chỉ do từ trường quyết định, hoặc cho lực tỉ lệ với bình phương dòng điện.",
       ke=[(r"Dùng lại $B$ vừa tìm với $I$ mới: $F'=BI'l\sin\alpha$", True),
           (r"Giữ $F$ không đổi vì từ trường không đổi", r"$F$ còn phụ thuộc $I$; $I$ tăng thì $F$ tăng."),
           (r"$F$ tăng bốn lần vì lực tỉ lệ với $I^2$", r"$F=BIl\sin\alpha$ tỉ lệ bậc nhất với $I$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>dây treo, lực căng bằng không</b> → nghĩ tới <b>lực từ cân bằng trọng lượng</b>; chiều I theo bàn tay trái.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Chiều dòng điện để lực từ hướng lên", "Dòng điện phải chạy theo chiều nào để lực từ hướng lên?",
       loi=r"Đặt tay trái ngược (đường sức vào mu bàn tay) nên ra chiều dòng điện ngược lại.",
       lua_chon=[(r"Từ N đến M", True),
                 (r"Từ M đến N", r"Với đường sức ⊙ và dòng từ M đến N (sang phải), ngón cái bàn tay trái chỉ xuống: lực từ kéo dây xuống, cùng chiều trọng lượng."),
                 (r"Chiều nào cũng được vì chỉ cần lực từ đủ lớn", r"Lực từ chỉ đỡ được dây khi hướng lên; chiều dòng điện quyết định chiều lực.")]),
  buoc("Trọng lượng của dây", "Trọng lượng của dây $P=mg$ bằng bao nhiêu newton?", 0.08, "N", 0.002,
       loi=r"Quên đổi gam sang kilôgam nên trọng lượng lớn gấp 1000 lần.",
       ke=[(r"Tính trọng lượng $P=mg$, đổi $8{,}0\ \text{g}$ ra kg", True),
           (r"Tính $F=BIl$ ngay với một giá trị $I$ bất kì", r"Cường độ $I$ là ẩn cần tìm, chưa thể thế số."),
           (r"Cho lực căng bằng $mg$ vì dây đang treo", r"Đề yêu cầu lực căng bằng không; khi đó trọng lượng do lực từ đỡ.")]),
  buoc("Cường độ dòng điện", "Cường độ dòng điện cần dùng bằng bao nhiêu ampe?", 4.0, "A", 0.05,
       loi=r"Chia trọng lượng cho hai vì có hai sợi chỉ, hoặc quên đổi cm sang m.",
       ke=[(r"Viết điều kiện cân bằng của dây khi lực căng bằng không", True),
           (r"$BIl=\dfrac{P}{2}$ vì có hai sợi chỉ", r"Lực căng bằng không nên hai sợi chỉ không đỡ gì; lực từ phải đỡ cả trọng lượng."),
           (r"$BIl=0$ vì dây nằm yên", r"Nằm yên là hợp lực bằng không, không có nghĩa từng lực bằng không.")]),
  buoc("Lực từ khi dòng điện giảm", "Lực từ khi dòng điện 2,4 A là bao nhiêu mN?", 48, "mN", 1,
       loi=r"Cho lực từ vẫn bằng trọng lượng vì dây còn treo yên, hoặc dùng cường độ dòng điện của câu a.",
       ke=[(r"$F'=BI'l$ với $I'$ mới", True),
           (r"$F'=P$ vì dây vẫn treo yên", r"Lực từ phụ thuộc $I$; dòng giảm thì lực từ giảm, phần còn thiếu do sợi chỉ đỡ."),
           (r"$F'=BIl$ với $I$ của câu a", r"Dòng điện đã đổi thành $I'$.")]),
  buoc("Tổng lực căng", "Tổng lực căng của hai sợi chỉ là bao nhiêu mN?", 32, "mN", 1,
       loi=r"Cộng lực từ vào trọng lượng thay vì trừ, hoặc cho lực căng bằng lực từ.",
       ke=[(r"Viết điều kiện cân bằng với lực căng, lực từ và trọng lượng", True),
           (r"$T=P+F'$", r"Lực từ hướng lên, cùng chiều lực căng, cùng đỡ trọng lượng; không cộng vào trọng lượng."),
           (r"$T=F'$", r"Lực căng đỡ phần trọng lượng mà lực từ chưa đỡ hết, không bằng lực từ.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>khung dây N vòng trong từ trường, hỏi lực mỗi cạnh hoặc mômen</b> → nghĩ tới <b>F = NBIl·sinα</b> và <b>M = NBIS·sinα</b>.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 4}, buoc=[
  buoc("Cạnh nào chịu lực", "Những cạnh nào của khung chịu lực từ?",
       loi=r"Cho cả bốn cạnh đều chịu lực, hoặc chọn cạnh nằm trong mặt phẳng khung mà quên xét góc với đường sức.",
       lua_chon=[(r"Chỉ AB và CD, vì vuông góc đường sức; BC và AD song song đường sức", True),
                 (r"Cả bốn cạnh, mỗi cạnh một lực $BIl$", r"BC và AD song song đường sức ($\alpha=0^\circ$) nên lực bằng không."),
                 (r"Chỉ BC và AD vì nằm trong mặt phẳng khung", r"Nằm trong mặt phẳng khung không có nghĩa là vuông góc đường sức; BC và AD song song đường sức.")]),
  buoc("Lực từ lên cạnh AB", "Lực từ tác dụng lên cạnh AB (cả khung) bằng bao nhiêu newton?", 1.2, "N", 0.05,
       loi=r"Quên nhân với số vòng $N$, hoặc dùng chiều dài cạnh BC thay cho AB.",
       ke=[(r"Khung có $N$ vòng: $F=NBI\cdot AB$", True),
           (r"$F=BI\cdot AB$, chỉ tính một vòng", r"Mỗi vòng dây đều chịu lực; $N$ vòng thì lực nhân với $N$."),
           (r"$F=NBI\cdot BC$", r"Lực lên cạnh AB tính với chiều dài chính cạnh AB.")]),
  buoc("Hợp lực lên khung", "Hợp lực của các lực từ lên khung là bao nhiêu?",
       loi=r"Cộng độ lớn hai lực thay vì cộng vectơ, quên rằng hai lực ngược chiều.",
       lua_chon=[(r"Bằng không: hai lực cùng độ lớn, ngược chiều", True),
                 (r"Gấp đôi lực lên một cạnh, vì hai lực cùng tác dụng lên khung", r"Hai lực ngược chiều nên triệt tiêu khi cộng vectơ, không cộng độ lớn."),
                 (r"Bằng lực lên một cạnh, vì chỉ một cạnh gây chuyển động", r"Cả hai cạnh đều chịu lực như nhau; hợp lực là tổng vectơ của hai lực ngược chiều.")],
       ke=[(r"Cộng vectơ hai lực lên AB và CD, chú ý chiều của chúng", True),
           (r"Cộng độ lớn hai lực vì cùng tác dụng lên khung", r"Lực là vectơ; hai lực ngược chiều thì triệt tiêu."),
           (r"Dùng $M=NBIS$ ngay", r"Chưa xét hợp lực; mômen là một câu hỏi khác.")]),
  buoc("Diện tích khung", "Diện tích khung bằng bao nhiêu mét vuông?", 0.0024, "m²", 0.0001,
       loi=r"Quên đổi cm sang m (ra diện tích gấp 10000 lần) hoặc lấy chu vi thay cho diện tích.",
       ke=[(r"$S=AB\cdot BC$, đổi ra mét", True),
           (r"$S=2(AB+BC)$", r"Đó là chu vi, không phải diện tích."),
           (r"$S=AB\cdot BC$ giữ nguyên đơn vị cm", r"$M=NBIS$ với tesla, ampe đòi $S$ theo mét vuông.")]),
  buoc("Mômen ngẫu lực lúc đầu", "Mômen của ngẫu lực từ lúc đầu bằng bao nhiêu N·m?", 0.048, "N·m", 0.002,
       loi=r"Lấy $\alpha=0^\circ$ vì mặt phẳng song song đường sức nên ra mômen bằng không; hoặc quên nhân $N$.",
       ke=[(r"Xác định $\alpha$ là góc giữa $\vec B$ và pháp tuyến rồi thế vào $M=NBIS\sin\alpha$", True),
           (r"$M=NBIS\sin\alpha$ với $\alpha=0^\circ$ vì mặt phẳng song song đường sức", r"$\alpha$ là góc giữa $\vec B$ và pháp tuyến; mặt phẳng song song $\vec B$ thì pháp tuyến vuông góc $\vec B$, $\alpha=90^\circ$."),
           (r"$M=BIl$", r"Đó là lực của một cạnh, một vòng; không phải mômen.")]),
  buoc("Mômen khi pháp tuyến hợp đường sức 30°", "Khi pháp tuyến hợp đường sức góc 30°, mômen bằng bao nhiêu N·m?", 0.024, "N·m", 0.002,
       loi=r"Dùng góc giữa mặt phẳng khung và đường sức (60°) hoặc dùng $\cos$ thay cho $\sin$.",
       ke=[(r"Thế $\alpha$ là góc giữa $\vec B$ và pháp tuyến vào $M=NBIS\sin\alpha$", True),
           (r"$M=NBIS\cos30^\circ$", r"Khi mặt phẳng song song $\vec B$ thì $M$ lớn nhất; dùng $\cos$ sẽ cho $M$ nhỏ nhất ở đúng vị trí đó."),
           (r"$M=NBIS\sin60^\circ$, lấy góc giữa mặt phẳng khung và $\vec B$", r"$\alpha$ là góc giữa $\vec B$ và pháp tuyến ($30^\circ$), không phải góc với mặt phẳng khung ($60^\circ$).")]),
  buoc("Kiểm tra")]),
]

# ═════════════ TỰ LUẬN: 8 ví dụ cũ giữ nguyên ═════════════
OLD = json.load(open(os.path.join(HERE, "old", "11.json")))["questions"]
ORDER = [0, 5, 6, 7, 1, 2, 4, 3]
MUC = {0: "Dễ", 5: "Dễ", 6: "Trung bình", 7: "Trung bình", 1: "Trung bình", 2: "Khó", 4: "Khó", 3: "Khó"}
TU_LUAN = tu_luan_tu(OLD, ORDER, MUC)
for a_, b_ in ((r"2T+F+P=0=>2T+R=0\Leftrightarrow", r"2T+F+P=0\Rightarrow 2T+R=0\Leftrightarrow"), ("B_{1}>B_{2}", r"B_{1}\gt B_{2}")):
    assert TU_LUAN["body_html"].count(a_) >= 1, a_
    TU_LUAN["body_html"] = TU_LUAN["body_html"].replace(a_, b_)

# ═════════════ GHI FILE ═════════════
write(J, 11, "Bài 10. Lực từ. Cảm ứng từ", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code)"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
