"""Bài tập mẫu Bài 12 "Hiện tượng cảm ứng điện từ" (Vật lí 12) — lesson_id 13. 5 dạng (quét dạng:
scripts/logs/batch-ra-soat/ket-qua/13.quet-dang.json). Hình: hinh_13.py. Ví dụ cũ: old/13.json (4 dạng cũ có hình gốc).
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-13.py   (idempotent, ghi 13.json với review.checked=false)"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from hinh_13 import *

J = os.path.join(HERE, "13.json")
T217 = "Từ thông qua khung dây"
T218 = "Định luật Faraday và định luật Lenz"

DANG = [
 dict(label="Dạng 1 · Dễ · Từ thông qua khung dây: góc của pháp tuyến", topic=T217,
      problem_html=r"""<p>Một khung dây dẫn phẳng hình tròn, bán kính $5{,}0\ \text{cm}$, đặt trong từ trường đều có cảm ứng từ $B=0{,}40\ \text{T}$. Mặt phẳng khung hợp với đường sức từ góc $30^\circ$.</p><ol type="a"><li>Tính từ thông qua khung.</li><li>Quay khung tới vị trí nào thì từ thông qua khung lớn nhất? Tính giá trị lớn nhất đó.</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Chiều dòng điện cảm ứng theo định luật Lenz", topic=T218,
      problem_html=r"""<p>Một vòng dây dẫn kín nằm trong mặt phẳng tờ giấy. Từ trường đều vuông góc với tờ giấy và hướng vào trong tờ giấy (kí hiệu ⊗; hướng ra khỏi tờ giấy kí hiệu ⊙). Chiều quay của kim đồng hồ được xét khi nhìn từ phía người đọc vào tờ giấy.</p><ol type="a"><li>Độ lớn của $\vec B$ tăng đều theo thời gian. Dòng điện cảm ứng trong vòng dây cùng chiều hay ngược chiều kim đồng hồ?</li><li>Nếu độ lớn của $\vec B$ giảm đều thì chiều dòng điện cảm ứng đổi thế nào?</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Suất điện động và dòng cảm ứng khi B biến thiên", topic=T218,
      problem_html=r"""<p>Một khung dây dẫn kín hình vuông cạnh $6{,}0\ \text{cm}$, điện trở $0{,}30\ \Omega$, đặt trong từ trường đều sao cho mặt khung vuông góc với đường sức từ. Cảm ứng từ giảm đều từ $0{,}50\ \text{T}$ xuống $0{,}20\ \text{T}$ trong $15\ \text{ms}$.</p><ol type="a"><li>Tính độ lớn suất điện động cảm ứng và cường độ dòng điện cảm ứng trong khung.</li><li>Nếu cảm ứng từ cũng giảm từ $0{,}50\ \text{T}$ xuống $0{,}20\ \text{T}$ nhưng trong thời gian chỉ bằng một nửa thì cường độ dòng điện cảm ứng là bao nhiêu?</li></ol>"""),
 dict(label="Dạng 4 · Khó · Cuộn N vòng, quay khung đổi góc α", topic=T218,
      problem_html=r"""<p>Một cuộn dây dẹt gồm $100$ vòng, diện tích mỗi vòng $50\ \text{cm}^2$, điện trở của cả cuộn $4{,}0\ \Omega$, đặt trong từ trường đều $B=0{,}40\ \text{T}$. Ban đầu mặt cuộn dây vuông góc với đường sức từ. Quay đều cuộn dây quanh trục nằm trong mặt phẳng cuộn dây và vuông góc với đường sức từ, trong $0{,}050\ \text{s}$, tới khi mặt cuộn dây hợp với đường sức từ góc $30^\circ$.</p><ol type="a"><li>Tính suất điện động cảm ứng trung bình và cường độ dòng điện trung bình trong cuộn dây.</li><li>Trong lúc quay, từ trường do dòng cảm ứng sinh ra cùng chiều hay ngược chiều với từ trường ngoài?</li></ol>"""),
 dict(label="Dạng 5 · Khó · Đọc đồ thị từ thông theo thời gian", topic=T218,
      problem_html=r"""<p>Một vòng dây dẫn kín có điện trở $0{,}50\ \Omega$ đặt trong từ trường vuông góc với mặt phẳng vòng dây, hướng vào trong tờ giấy (⊗); chọn pháp tuyến cùng chiều từ trường nên từ thông luôn dương. Từ thông qua vòng dây biến thiên theo thời gian như đồ thị: tăng đều từ $0$ đến $20\ \text{mWb}$ trong khoảng $0$ – $0{,}10\ \text{s}$ (đoạn 1); giữ nguyên $20\ \text{mWb}$ trong khoảng $0{,}10$ – $0{,}30\ \text{s}$ (đoạn 2); giảm đều về $0$ trong khoảng $0{,}30$ – $0{,}35\ \text{s}$ (đoạn 3).</p><ol type="a"><li>Trong những đoạn nào có dòng điện cảm ứng?</li><li>Tính cường độ dòng điện cảm ứng ở mỗi đoạn có dòng điện.</li><li>Nhìn từ phía người đọc vào tờ giấy, dòng điện cảm ứng ở mỗi đoạn đó chạy cùng chiều hay ngược chiều kim đồng hồ?</li></ol>"""),
]

ANALYSIS = [
 [(r"""\"khung dây dẫn phẳng hình tròn, bán kính $5{,}0\ \text{cm}$\"""", r"$r=5{,}0\ \text{cm}$", "Diện tích khung tròn; đổi sang m²"),
  (r"""\"từ trường đều có cảm ứng từ $B=0{,}40\ \text{T}$\"""", r"$B=0{,}40\ \text{T}$", "Từ trường đều, khung phẳng: dùng được công thức từ thông"),
  (r"""\"Mặt phẳng khung hợp với đường sức từ góc $30^\circ$\"""", r"Góc giữa MẶT khung và đường sức: $30^\circ$", "⚠ Kiểm tra đề cho góc của mặt khung hay của pháp tuyến; công thức dùng góc của pháp tuyến"),
  (r"""\"a) Tính từ thông qua khung\"""", r"Cần $\Phi$ (Wb)", "Đại lượng cần tìm"),
  (r"""\"b) Quay khung tới vị trí nào thì từ thông lớn nhất? Tính giá trị lớn nhất\"""", r"Cần vị trí khung và $\Phi_{\max}$", "Đại lượng cần tìm")],
 [(r"""\"vòng dây dẫn kín nằm trong mặt phẳng tờ giấy\"""", "Mạch kín; mặt vòng song song mặt giấy", "⚠ Dòng cảm ứng chỉ có khi mạch kín và từ thông biến thiên"),
  (r"""\"Từ trường đều vuông góc với tờ giấy, hướng vào trong (⊗)\"""", r"$\vec B$ hướng vào giấy", r"Từ thông qua vòng dây tính theo $B$, $S$, $\alpha$"),
  (r"""\"nhìn từ phía người đọc vào tờ giấy\"""", "Quy ước chiều quay kim đồng hồ theo người đọc", "⚠ Chiều quay chỉ có nghĩa khi nói rõ nhìn từ phía nào"),
  (r"""\"Độ lớn của $\vec B$ tăng đều theo thời gian\"""", r"$B$ tăng; $S$, $\alpha$ giữ nguyên", "Xét từ thông đổi thế nào, rồi áp dụng định luật Lenz"),
  (r"""\"a) cùng chiều hay ngược chiều kim đồng hồ?\"""", "Cần chiều dòng cảm ứng", "Đại lượng cần tìm"),
  (r"""\"b) Nếu độ lớn của $\vec B$ giảm đều\"""", "Cần so sánh với câu a", "Đại lượng cần tìm")],
 [(r"""\"khung dây dẫn kín hình vuông cạnh $6{,}0\ \text{cm}$, điện trở $0{,}30\ \Omega$\"""", r"$a=6{,}0\ \text{cm}$; $R=0{,}30\ \Omega$", "Diện tích khung vuông, đổi cm² sang m²; $R$ dùng cho dòng điện"),
  (r"""\"mặt khung vuông góc với đường sức từ\"""", r"Pháp tuyến và $\vec B$ cùng phương", r"Cho biết góc $\alpha$ giữa pháp tuyến và $\vec B$"),
  (r"""\"Cảm ứng từ giảm đều từ $0{,}50\ \text{T}$ xuống $0{,}20\ \text{T}$\"""", r"$B_1=0{,}50\ \text{T}$; $B_2=0{,}20\ \text{T}$", r"Từ thông biến thiên do $B$ đổi; $S$ không đổi"),
  (r"""\"trong $15\ \text{ms}$\"""", r"$\Delta t=15\ \text{ms}$", "⚠ Đổi ms ra giây trước khi dùng; mạch kín nên có dòng cảm ứng"),
  (r"""\"a) Tính độ lớn suất điện động cảm ứng và cường độ dòng điện\"""", r"Cần $|e_c|$ và $i$", "Đại lượng cần tìm"),
  (r"""\"b) trong thời gian chỉ bằng một nửa\"""", r"$\Delta t'=\Delta t/2$; $\Delta\Phi$ như cũ", "So sánh với câu a")],
 [(r"""\"cuộn dây dẹt gồm $100$ vòng, diện tích mỗi vòng $50\ \text{cm}^2$, điện trở của cả cuộn $4{,}0\ \Omega$\"""", r"$N=100$; $S=50\ \text{cm}^2$ (một vòng); $R=4{,}0\ \Omega$", "⚠ $S$ và $\\Phi$ là của MỘT vòng; cả cuộn có $N$ vòng nối tiếp; đổi cm² sang m²"),
  (r"""\"từ trường đều $B=0{,}40\ \text{T}$\"""", r"$B=0{,}40\ \text{T}$", "Từ trường đều"),
  (r"""\"Ban đầu mặt cuộn dây vuông góc với đường sức từ\"""", "Trạng thái 1: mặt vuông góc đường sức", r"Xác định góc $\alpha_1$ của pháp tuyến"),
  (r"""\"quay đều … trong $0{,}050\ \text{s}$, tới khi mặt cuộn dây hợp với đường sức từ góc $30^\circ$\"""", r"$\Delta t=0{,}050\ \text{s}$; trạng thái 2: mặt hợp đường sức $30^\circ$", r"⚠ $30^\circ$ là góc của MẶT cuộn dây, không phải của pháp tuyến; $B$, $S$ không đổi, chỉ $\alpha$ đổi"),
  (r"""\"a) Tính suất điện động cảm ứng trung bình và cường độ dòng điện trung bình\"""", r"Cần $e_c$ và $i$", "Đại lượng cần tìm"),
  (r"""\"b) từ trường do dòng cảm ứng sinh ra cùng chiều hay ngược chiều với từ trường ngoài\"""", r"Cần so sánh chiều $\vec B_c$ với $\vec B$", "Xét từ thông tăng hay giảm")],
 [(r"""\"vòng dây dẫn kín có điện trở $0{,}50\ \Omega$\"""", r"$R=0{,}50\ \Omega$; mạch kín", "Dòng cảm ứng chỉ có khi mạch kín và từ thông biến thiên"),
  (r"""\"hướng vào trong tờ giấy (⊗); chọn pháp tuyến cùng chiều từ trường\"""", r"$\vec B$ vào giấy; $\Phi\ge0$", "⚠ Chiều quay kim đồng hồ xét khi nhìn từ phía người đọc"),
  (r"""\"đoạn 1: tăng đều từ $0$ đến $20\ \text{mWb}$ trong $0$ – $0{,}10\ \text{s}$\"""", r"$\Delta\Phi_1=20\ \text{mWb}$; $\Delta t_1=0{,}10\ \text{s}$", "Đổi mWb ra Wb"),
  (r"""\"đoạn 2: giữ nguyên $20\ \text{mWb}$\"""", r"$\Phi$ không đổi", r"Cho biết $\Phi$ có biến thiên không"),
  (r"""\"đoạn 3: giảm đều về $0$ trong $0{,}30$ – $0{,}35\ \text{s}$\"""", r"$\Delta\Phi_3=20\ \text{mWb}$; $\Delta t_3=0{,}05\ \text{s}$", "Độ biến thiên từ thông trong đoạn này"),
  (r"""\"a) Trong những đoạn nào có dòng điện cảm ứng?\"""", "Cần nhận ra đoạn có dòng", "Đại lượng cần tìm"),
  (r"""\"b) cường độ dòng điện ở mỗi đoạn\"""", r"Cần $i$ của từng đoạn có dòng", "Đại lượng cần tìm"),
  (r"""\"c) cùng chiều hay ngược chiều kim đồng hồ\"""", "Cần chiều dòng (nhìn từ người đọc)", "Đại lượng cần tìm")],
]

# ═════════════ LỜI GIẢI ═════════════
RC1 = [r"<strong>Khái niệm:</strong> từ thông qua khung phẳng trong từ trường đều, đơn vị Wb.",
       r"<strong>Công thức:</strong> $\Phi=BS\cos\alpha$; khung tròn $S=\pi r^2$.",
       r"<strong>Góc:</strong> $\alpha$ là góc giữa pháp tuyến $\vec n$ và $\vec B$, không phải góc của mặt khung.",
       r"⚠ <strong>Điều kiện:</strong> từ trường đều, khung phẳng; $S$ phải ở m²."]
RC2 = [r"<strong>Khái niệm:</strong> dòng cảm ứng chỉ có khi mạch kín và từ thông qua mạch biến thiên.",
       r"<strong>Định luật Lenz:</strong> từ trường cảm ứng chống lại sự biến thiên của từ thông.",
       r"Từ thông tăng: $\vec B_c$ ngược chiều $\vec B$ ngoài; từ thông giảm: cùng chiều.",
       r"<strong>Nắm tay phải:</strong> ngón cái chỉ chiều $\vec B_c$, các ngón khum chỉ chiều dòng.",
       r"⚠ <strong>Điều kiện:</strong> vòng dây kín; chiều quay phải nói rõ nhìn từ phía nào."]
RC3 = [r"<strong>Khái niệm:</strong> suất điện động cảm ứng là tốc độ biến thiên từ thông qua mạch.",
       r"<strong>Định luật Faraday:</strong> $|e_c|=\left|\dfrac{\Delta\Phi}{\Delta t}\right|$; mạch kín có $R$: $i=\dfrac{|e_c|}{R}$.",
       r"<strong>Từ thông:</strong> $\Phi=BS\cos\alpha$; chỉ $B$ đổi thì $\Delta\Phi=\Delta B\cdot S\cos\alpha$.",
       r"⚠ <strong>Điều kiện:</strong> mạch kín; lấy độ lớn $\Delta\Phi$; $S$ ra m², $\Delta t$ ra giây."]
RC4 = [r"<strong>Từ thông một vòng:</strong> $\Phi=BS\cos\alpha$, $\alpha$ là góc của pháp tuyến.",
       r"<strong>Faraday cho cuộn $N$ vòng:</strong> $|e_c|=N\left|\dfrac{\Delta\Phi}{\Delta t}\right|$ với $\Phi$ qua một vòng; $i=\dfrac{|e_c|}{R}$.",
       r"<strong>Lenz:</strong> từ thông giảm: $\vec B_c$ cùng chiều $\vec B$ ngoài; tăng: ngược chiều.",
       r"⚠ <strong>Điều kiện:</strong> $\Delta\Phi$ tính cho một vòng; $S$ ra m²; $\alpha$ là góc của pháp tuyến."]
RC5 = [r"<strong>Khái niệm:</strong> trên đồ thị $\Phi$–$t$, độ dốc đoạn thẳng là tốc độ biến thiên từ thông.",
       r"<strong>Faraday:</strong> $|e_c|=\left|\dfrac{\Delta\Phi}{\Delta t}\right|$, $i=\dfrac{|e_c|}{R}$.",
       r"<strong>Lenz:</strong> $\Phi$ tăng: $\vec B_c$ ngược chiều $\vec B$ ngoài; $\Phi$ giảm: cùng chiều; rồi nắm tay phải.",
       r"⚠ <strong>Điều kiện:</strong> đoạn nằm ngang ($\Phi$ không đổi) không có dòng dù $\Phi$ lớn; đổi mWb ra Wb."]

SOLS = [
 sol(RC1, [
  ("Diện tích khung", [P(r"Khung tròn bán kính $r=5{,}0\ \text{cm}=0{,}050\ \text{m}$:"), M(r"S=\pi r^2=\pi\cdot0{,}050^2"), A(r"S\approx7{,}85\cdot10^{-3}\ \text{m}^2")]),
  ("Góc α của pháp tuyến", [P(r"Đề cho góc giữa mặt khung và đường sức là $30^\circ$. Pháp tuyến vuông góc với mặt khung nên:"), M(r"\alpha=90^\circ-30^\circ"), A(r"\alpha=60^\circ")]),
  ("Từ thông qua khung (câu a)", [M(r"\Phi=BS\cos\alpha"), M(r"\Phi=0{,}40\cdot7{,}85\cdot10^{-3}\cdot\cos60^\circ"), A(r"\Phi\approx1{,}57\cdot10^{-3}\ \text{Wb}=1{,}57\ \text{mWb}")]),
  ("Từ thông lớn nhất (câu b)", [P(r"$\Phi$ lớn nhất khi $\cos\alpha=1$, tức $\alpha=0^\circ$: pháp tuyến song song $\vec B$, mặt khung vuông góc đường sức."), M(r"\Phi_{\max}=BS=0{,}40\cdot7{,}85\cdot10^{-3}"), A(r"\Phi_{\max}\approx3{,}14\cdot10^{-3}\ \text{Wb}")]),
  ("Kiểm tra", [P(r"$1{,}57\ \text{mWb}\lt3{,}14\ \text{mWb}$: hợp lí vì $\cos60^\circ=0{,}5$."), P(r"Nếu thế nhầm $\cos30^\circ$ thì ra $2{,}72\ \text{mWb}$, lớn hơn đúng. Đơn vị: $\text{T}\cdot\text{m}^2=\text{Wb}$.")])],
  [r"a) $\Phi\approx1{,}57\ \text{mWb}$", r"b) Khung vuông góc đường sức; $\Phi_{\max}\approx3{,}14\ \text{mWb}$"],
  r"Nhận dạng: đề cho <strong>góc giữa mặt khung và đường sức</strong> → đổi sang góc của pháp tuyến rồi dùng $\Phi=BS\cos\alpha$."),
 sol(RC2, [
  ("Từ thông tăng hay giảm", [P(r"Mạch kín; $S$ và $\alpha$ không đổi, $B$ tăng nên $\Phi=BS\cos\alpha$ tăng. Từ thông biến thiên nên có dòng cảm ứng."), A(r"T:Từ thông qua vòng dây <strong>tăng</strong>.")]),
  ("Chiều từ trường cảm ứng", [P(r"Từ thông tăng nên $\vec B_c$ ngược chiều $\vec B$ ngoài (chống lại sự tăng)."), P(r"$\vec B$ ngoài hướng vào giấy (⊗) nên trong lòng vòng dây $\vec B_c$ hướng ra khỏi giấy (⊙)."), A(r"T:$\vec B_c$ hướng <strong>ra khỏi giấy</strong>.")]),
  ("Chiều dòng điện (câu a)", [P(r"Nắm tay phải: ngón cái chỉ ra phía người đọc, các ngón khum chỉ chiều dòng. Nhìn từ phía người đọc, mặt vòng dây hướng về người đọc có đường sức đi ra (mặt Bắc)."), A(r"T:Câu a: dòng cảm ứng <strong>ngược chiều kim đồng hồ</strong>.")]),
  ("Trường hợp B giảm (câu b)", [P(r"$B$ giảm nên $\Phi$ giảm: $\vec B_c$ cùng chiều $\vec B$ ngoài, hướng vào giấy (⊗)."), P(r"Nắm tay phải: ngón cái chỉ vào trong giấy, nhìn từ phía người đọc các ngón khum cùng chiều kim đồng hồ."), A(r"T:Câu b: dòng cảm ứng <strong>cùng chiều kim đồng hồ</strong>.")]),
  ("Kiểm tra", [P(r"Hai trường hợp ngược nhau: chiều dòng do từ thông tăng hay giảm quyết định, không do hướng của $\vec B$ ngoài."), P(r"Nếu vòng dây bị cắt hở một chỗ thì vẫn có suất điện động nhưng không có dòng điện (mạch không kín).")])],
  ["a) Ngược chiều kim đồng hồ", "b) Cùng chiều kim đồng hồ"],
  r"Nhận dạng: đề hỏi <strong>chiều dòng điện cảm ứng</strong> → xét từ thông tăng hay giảm, dùng Lenz rồi nắm tay phải."),
 sol(RC3, [
  ("Đổi sang đơn vị SI", [M(r"a=6{,}0\ \text{cm}=0{,}060\ \text{m}"), M(r"S=a^2=0{,}060^2"), A(r"S=3{,}6\cdot10^{-3}\ \text{m}^2"), P(r"$\Delta t=15\ \text{ms}=0{,}015\ \text{s}$.")]),
  ("Độ biến thiên từ thông", [P(r"Mặt khung vuông góc đường sức nên $\cos\alpha=1$; chỉ $B$ đổi."), M(r"|\Delta\Phi|=|B_2-B_1|\,S=|0{,}20-0{,}50|\cdot3{,}6\cdot10^{-3}"), A(r"|\Delta\Phi|=1{,}08\cdot10^{-3}\ \text{Wb}")]),
  ("Suất điện động cảm ứng (câu a)", [M(r"|e_c|=\left|\dfrac{\Delta\Phi}{\Delta t}\right|=\dfrac{1{,}08\cdot10^{-3}}{0{,}015}"), A(r"|e_c|=0{,}072\ \text{V}=72\ \text{mV}")]),
  ("Cường độ dòng điện (câu a)", [M(r"i=\dfrac{|e_c|}{R}=\dfrac{0{,}072}{0{,}30}"), A(r"i=0{,}24\ \text{A}")]),
  ("Rút ngắn thời gian (câu b)", [P(r"$\Delta\Phi$ không đổi, $\Delta t'=0{,}0075\ \text{s}$:"), M(r"|e'_c|=\dfrac{1{,}08\cdot10^{-3}}{0{,}0075}=0{,}144\ \text{V}"), M(r"i'=\dfrac{0{,}144}{0{,}30}"), A(r"i'=0{,}48\ \text{A}")]),
  ("Kiểm tra", [P(r"Đơn vị: $\text{Wb/s}=\text{V}$; $\text{V}/\Omega=\text{A}$."), P(r"$\Delta t$ giảm một nửa, $\Delta\Phi$ không đổi nên $i'=2i=2\cdot0{,}24=0{,}48\ \text{A}$, khớp.")])],
  [r"a) $|e_c|=0{,}072\ \text{V}$; $i=0{,}24\ \text{A}$", r"b) $i'=0{,}48\ \text{A}$"],
  r"Nhận dạng: đề cho <strong>cảm ứng từ đổi đều trong khoảng thời gian Δt</strong> → $|e_c|=\left|\dfrac{\Delta\Phi}{\Delta t}\right|$, rồi chia cho $R$."),
 sol(RC4, [
  ("Góc α lúc sau", [P(r"Ban đầu mặt cuộn vuông góc đường sức nên pháp tuyến song song $\vec B$: $\alpha_1=0^\circ$. Lúc sau mặt hợp đường sức $30^\circ$ nên:"), M(r"\alpha_2=90^\circ-30^\circ"), A(r"\alpha_2=60^\circ")]),
  ("Độ biến thiên từ thông qua một vòng", [M(r"S=50\ \text{cm}^2=5{,}0\cdot10^{-3}\ \text{m}^2"), M(r"\Phi_1=BS\cos0^\circ=0{,}40\cdot5{,}0\cdot10^{-3}=2{,}0\cdot10^{-3}\ \text{Wb}"), M(r"\Phi_2=BS\cos60^\circ=1{,}0\cdot10^{-3}\ \text{Wb}"), A(r"|\Delta\Phi|=|\Phi_2-\Phi_1|=1{,}0\cdot10^{-3}\ \text{Wb}")]),
  ("Suất điện động của cả cuộn (câu a)", [P(r"Cuộn $N=100$ vòng:"), M(r"|e_c|=N\left|\dfrac{\Delta\Phi}{\Delta t}\right|=100\cdot\dfrac{1{,}0\cdot10^{-3}}{0{,}050}"), A(r"|e_c|=2{,}0\ \text{V}")]),
  ("Cường độ dòng điện (câu a)", [M(r"i=\dfrac{|e_c|}{R}=\dfrac{2{,}0}{4{,}0}"), A(r"i=0{,}50\ \text{A}")]),
  ("Chiều từ trường cảm ứng (câu b)", [P(r"$\Phi$ giảm từ $2{,}0\ \text{mWb}$ xuống $1{,}0\ \text{mWb}$ nên theo Lenz, dòng cảm ứng bù lại phần giảm:"), A(r"T:$\vec B_c$ <strong>cùng chiều</strong> $\vec B$ ngoài.")]),
  ("Kiểm tra", [P(r"Một vòng cho $\dfrac{1{,}0\cdot10^{-3}}{0{,}050}=0{,}020\ \text{V}$; nhân $100$ vòng ra $2{,}0\ \text{V}$, khớp."), P(r"Nếu thế nhầm $\alpha_2=30^\circ$ thì $\Delta\Phi$ chỉ còn khoảng $0{,}27\ \text{mWb}$ và $e_c$ nhỏ hơn nhiều so với đúng.")])],
  [r"a) $|e_c|=2{,}0\ \text{V}$; $i=0{,}50\ \text{A}$", r"b) $\vec B_c$ cùng chiều $\vec B$ ngoài"],
  r"Nhận dạng: đề có <strong>cuộn N vòng quay, đổi góc</strong> → $\Delta\Phi=BS(\cos\alpha_2-\cos\alpha_1)$ cho một vòng, nhân $N$ ở suất điện động."),
 sol(RC5, [
  ("Đoạn có dòng cảm ứng (câu a)", [P(r"Đoạn (1): $\Phi$ tăng; đoạn (3): $\Phi$ giảm. Mạch kín, từ thông biến thiên nên có dòng."), P(r"Đoạn (2): $\Phi$ giữ $20\ \text{mWb}$, $\Delta\Phi=0$ nên $e_c=0$, không có dòng dù $\Phi$ đang lớn nhất."), A(r"T:Có dòng ở <strong>đoạn (1) và đoạn (3)</strong>.")]),
  ("Đoạn (1) (câu b)", [M(r"|e_1|=\dfrac{\Delta\Phi}{\Delta t}=\dfrac{20\cdot10^{-3}}{0{,}10}=0{,}20\ \text{V}"), M(r"i_1=\dfrac{|e_1|}{R}=\dfrac{0{,}20}{0{,}50}"), A(r"i_1=0{,}40\ \text{A}")]),
  ("Đoạn (3) (câu b)", [M(r"|e_3|=\dfrac{20\cdot10^{-3}}{0{,}35-0{,}30}=\dfrac{20\cdot10^{-3}}{0{,}050}=0{,}40\ \text{V}"), M(r"i_3=\dfrac{0{,}40}{0{,}50}"), A(r"i_3=0{,}80\ \text{A}")]),
  ("Chiều dòng điện (câu c)", [P(r"Đoạn (1): $\Phi$ tăng, $\vec B$ ngoài hướng vào giấy (⊗) nên $\vec B_c$ hướng ra (⊙): dòng ngược chiều kim đồng hồ."), P(r"Đoạn (3): $\Phi$ giảm nên $\vec B_c$ cùng chiều $\vec B$ ngoài, hướng vào (⊗): dòng cùng chiều kim đồng hồ."), A(r"T:Hai đoạn có dòng <strong>ngược chiều nhau</strong>.")]),
  ("Kiểm tra", [P(r"Cùng $\Delta\Phi=20\ \text{mWb}$ nhưng $\Delta t$ đoạn (3) nhỏ hơn đoạn (1) $2$ lần nên $i_3=2i_1=2\cdot0{,}40=0{,}80\ \text{A}$, khớp.")])],
  ["a) Đoạn (1) và đoạn (3)", r"b) $i_1=0{,}40\ \text{A}$; $i_3=0{,}80\ \text{A}$", "c) Ngược chiều nhau: đoạn (1) ngược chiều kim đồng hồ, đoạn (3) cùng chiều kim đồng hồ"],
  r"Nhận dạng: đề cho <strong>đồ thị Φ–t nhiều đoạn</strong> → độ dốc từng đoạn là $e_c$; độ dốc từng đoạn là $e_c$."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC (khớp 1-1 với .bt-step của SOLS) ═════════════
STEPS = [
 dict(nhan_dang=r"Thấy <b>mặt khung hợp với đường sức góc …</b> → chú ý <b>góc của pháp tuyến</b> trong <b>Φ = BS cos α</b>.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Diện tích khung", r"Diện tích khung tròn $S$ bằng bao nhiêu (đơn vị $10^{-3}\ \text{m}^2$)?", 7.85, "×10⁻³ m²", 0.03,
       loi=r"Quên đổi cm sang m (thế $5{,}0$ thay cho $0{,}050$), hoặc dùng chu vi $2\pi r$ thay cho $\pi r^2$."),
  buoc("Góc α của pháp tuyến", r"Góc $\alpha$ giữa pháp tuyến và $\vec B$ bằng bao nhiêu độ?", 60, "°", 0.5,
       loi=r"Lấy luôn $30^\circ$ (góc của mặt khung) làm $\alpha$ rồi thế vào $\cos$.",
       ke=[(r"Pháp tuyến vuông góc với mặt khung nên $\alpha=90^\circ-30^\circ$", True),
           (r"Góc $30^\circ$ của đề chính là $\alpha$, thế thẳng vào $\cos$", r"$30^\circ$ là góc giữa MẶT khung và đường sức; $\alpha$ đo từ pháp tuyến, vuông góc với mặt khung."),
           (r"Khung phẳng nên $\alpha=0^\circ$ ở mọi vị trí", r"$\alpha=0^\circ$ chỉ khi mặt khung vuông góc đường sức; ở đây khung đang nghiêng $30^\circ$ so với đường sức.")]),
  buoc("Từ thông qua khung", r"Từ thông qua khung bằng bao nhiêu (đơn vị mWb)?", 1.57, "mWb", 0.02,
       loi=r"Thế $\cos30^\circ$ thay cho cosin của góc pháp tuyến nên kết quả lớn hơn đúng; hoặc để $S$ ở cm² nên lệch $10^4$ lần.",
       ke=[(r"$\Phi=BS\cos\alpha$ với $S$ ở m² và $\alpha$ vừa tìm", True),
           (r"$\Phi=BS\sin\alpha$", r"Chỉ dùng $\sin$ khi $\alpha$ là góc của mặt khung; $\alpha$ là góc của pháp tuyến nên dùng $\cos\alpha$."),
           (r"$\Phi=BS$ vì từ trường đều", r"$\Phi=BS$ chỉ khi mặt khung vuông góc đường sức ($\cos\alpha=1$); khung đang nghiêng nên còn thừa số $\cos\alpha$.")]),
  buoc("Từ thông lớn nhất", r"Từ thông lớn nhất qua khung bằng bao nhiêu (đơn vị mWb)?", 3.14, "mWb", 0.03,
       loi=r"Cho rằng khung song song đường sức thì từ thông lớn nhất; khi đó không có đường sức nào xuyên qua nên $\Phi=0$.",
       ke=[(r"$\Phi_{\max}$ khi $\cos\alpha=1$, tức mặt khung vuông góc đường sức", True),
           (r"$\Phi_{\max}$ khi $\cos\alpha=0$, tức mặt khung song song đường sức", r"$\cos\alpha=0$ cho $\Phi=0$, đó là giá trị nhỏ nhất chứ không phải lớn nhất."),
           (r"Từ thông cứ tăng khi quay khung, không có giá trị lớn nhất", r"$|\cos\alpha|\le1$ nên $\Phi\le BS$; quay quá vị trí vuông góc thì $\Phi$ giảm lại.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>hỏi chiều dòng cảm ứng</b> → nghĩ tới <b>Lenz: chống lại sự biến thiên</b>, rồi nắm tay phải.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Từ thông tăng hay giảm", r"Khi $B$ tăng đều, từ thông qua vòng dây thay đổi thế nào?",
       loi=r"Cho rằng từ trường đều thì từ thông không đổi, quên rằng $\Phi=BS\cos\alpha$ đổi khi $B$ đổi.",
       lua_chon=[(r"Tăng", True),
                 (r"Giảm", r"$S$ và $\alpha$ giữ nguyên, $B$ tăng nên $\Phi=BS\cos\alpha$ tăng chứ không giảm."),
                 (r"Không đổi vì từ trường đều", r"Từ trường đều chỉ nói $B$ giống nhau mọi điểm; $B$ vẫn đổi theo thời gian nên $\Phi$ đổi.")]),
  buoc("Chiều từ trường cảm ứng", r"Trong lòng vòng dây, từ trường cảm ứng $\vec B_c$ hướng thế nào?",
       loi=r"Cho rằng từ trường cảm ứng luôn cùng chiều từ trường ngoài.",
       lua_chon=[(r"Ra khỏi tờ giấy (⊙)", True),
                 (r"Vào trong tờ giấy (⊗)", r"Đó là chiều của $\vec B$ ngoài; từ thông tăng nên $\vec B_c$ phải ngược chiều nó."),
                 (r"Nằm trong mặt phẳng tờ giấy", r"Trong lòng vòng dây $\vec B_c$ vuông góc mặt vòng, không nằm trong mặt phẳng vòng.")],
       ke=[(r"Từ thông tăng nên $\vec B_c$ ngược chiều $\vec B$ ngoài (chống lại sự tăng)", True),
           (r"$\vec B_c$ cùng chiều $\vec B$ ngoài để giữ từ trường", r"Cùng chiều chỉ khi từ thông giảm; từ thông tăng thì phải cản lại."),
           (r"Bỏ qua $\vec B_c$, lấy chiều dòng cùng chiều $\vec B$ ngoài", r"Dòng điện là hệ quả; phải xác định $\vec B_c$ trước, rồi suy chiều dòng bằng nắm tay phải.")]),
  buoc("Chiều dòng điện (câu a)", r"Nhìn từ phía người đọc, dòng điện cảm ứng chạy thế nào?",
       loi=r"Dùng nắm tay phải với $\vec B$ ngoài thay cho $\vec B_c$ nên ra chiều ngược lại.",
       lua_chon=[(r"Ngược chiều kim đồng hồ", True),
                 (r"Cùng chiều kim đồng hồ", r"Cùng chiều kim đồng hồ tạo ra từ trường hướng vào giấy, trùng $\vec B$ ngoài; ở đây cần $\vec B_c$ hướng ra."),
                 (r"Không có dòng điện", r"Vòng kín và từ thông biến thiên nên chắc chắn có dòng cảm ứng.")],
       ke=[(r"Nắm tay phải: ngón cái theo $\vec B_c$, các ngón khum chỉ chiều dòng", True),
           (r"Nắm tay phải: ngón cái theo $\vec B$ ngoài", r"Chiều dòng gắn với từ trường do chính nó sinh ra ($\vec B_c$), không gắn với từ trường ngoài."),
           (r"Dòng chạy theo chiều của $\vec B$ ngoài, tức vào giấy", r"Dòng điện chạy trong mặt phẳng vòng dây; chiều của nó là quay thuận hay ngược kim đồng hồ, không phải vào hay ra giấy.")]),
  buoc("Trường hợp B giảm (câu b)", r"Nếu $B$ giảm đều, dòng cảm ứng chạy thế nào (nhìn từ phía người đọc)?",
       loi=r"Giữ nguyên kết luận của câu a, quên rằng từ thông giảm thì $\vec B_c$ đổi sang cùng chiều $\vec B$ ngoài.",
       lua_chon=[(r"Cùng chiều kim đồng hồ", True),
                 (r"Ngược chiều kim đồng hồ", r"Đó là chiều khi $B$ tăng; khi $B$ giảm $\vec B_c$ đổi thành hướng vào giấy nên dòng đổi chiều."),
                 (r"Không có dòng điện", r"$B$ giảm vẫn là từ thông biến thiên nên vẫn có dòng cảm ứng.")],
       ke=[(r"$\Phi$ giảm nên $\vec B_c$ cùng chiều $\vec B$ ngoài (bù lại phần giảm)", True),
           (r"$\vec B_c$ vẫn ngược chiều $\vec B$ ngoài như câu a", r"Ngược chiều chỉ khi từ thông tăng; từ thông giảm thì phải bù lại."),
           (r"$B$ giảm dần về nhỏ nên không còn từ trường cảm ứng", r"Dòng cảm ứng tồn tại chừng nào $\Phi$ còn biến thiên, kể cả đang giảm.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>cảm ứng từ đổi đều trong Δt</b> → nghĩ tới <b>|e_c| = |ΔΦ|/Δt</b>, rồi i = |e_c|/R.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Đổi sang đơn vị SI", r"Diện tích khung $S$ bằng bao nhiêu (đơn vị $10^{-3}\ \text{m}^2$)?", 3.6, "×10⁻³ m²", 0.05,
       loi=r"Quên đổi cm sang m (thế $6{,}0$ thay cho $0{,}060$) nên $S$ lệch $10^4$ lần."),
  buoc("Độ biến thiên từ thông", r"Độ lớn $|\Delta\Phi|$ bằng bao nhiêu (đơn vị mWb)?", 1.08, "mWb", 0.02,
       loi=r"Lấy $B_2S$ làm $\Delta\Phi$ (bỏ quên trừ từ thông đầu), hoặc quên đổi cm² sang m².",
       ke=[(r"$|\Delta\Phi|=|B_2-B_1|\,S\cos\alpha$ với $\alpha=0^\circ$ vì khung vuông góc đường sức", True),
           (r"$|\Delta\Phi|=B_2S$ (chỉ lấy giá trị cuối)", r"$\Delta\Phi$ là hiệu hai từ thông $\Phi_2-\Phi_1$, không phải từ thông cuối."),
           (r"$|\Delta\Phi|=|B_2-B_1|\,S\cos90^\circ$", r"Mặt khung vuông góc đường sức thì pháp tuyến song song $\vec B$, $\alpha=0^\circ$; $\cos90^\circ=0$ cho $\Delta\Phi=0$, vô lí vì khung có dòng.")]),
  buoc("Suất điện động cảm ứng", r"Độ lớn suất điện động cảm ứng bằng bao nhiêu (đơn vị mV)?", 72, "mV", 1,
       loi=r"Không đổi ms sang giây (chia cho $15$) nên lệch $1000$ lần, hoặc nhân $\Delta\Phi$ với $\Delta t$ thay vì chia.",
       ke=[(r"$|e_c|=\dfrac{|\Delta\Phi|}{\Delta t}$ với $\Delta t$ đổi ra giây", True),
           (r"$|e_c|=|\Delta\Phi|\cdot\Delta t$", r"Faraday là tốc độ biến thiên, phải chia cho $\Delta t$; nhân cho đơn vị Wb·s, không phải V."),
           (r"$|e_c|=\dfrac{|\Delta\Phi|}{\Delta t}$ với $\Delta t=15$ (giữ ms)", r"Wb/ms không phải V; phải đổi $\Delta t$ ra giây trước khi chia.")]),
  buoc("Cường độ dòng điện", r"Cường độ dòng điện cảm ứng trong khung bằng bao nhiêu (đơn vị A)?", 0.24, "A", 0.005,
       loi=r"Nhân $e_c$ với $R$ thay vì chia, hoặc chia khi $e_c$ còn tính bằng mV.",
       ke=[(r"$i=\dfrac{|e_c|}{R}$ với $e_c$ ở V", True),
           (r"$i=|e_c|\cdot R$", r"Định luật Ôm cho $i=\dfrac{U}{R}$; nhân với $R$ cho đơn vị V·Ω, không phải A."),
           (r"$i=\dfrac{R}{|e_c|}$", r"Lật ngược tỉ số; $R$ lớn thì dòng phải nhỏ, còn công thức này cho dòng lớn.")]),
  buoc("Rút ngắn thời gian (câu b)", r"Nếu thời gian giảm $B$ chỉ bằng một nửa, cường độ dòng điện bằng bao nhiêu (đơn vị A)?", 0.48, "A", 0.01,
       loi=r"Nghĩ rằng thời gian ngắn hơn thì dòng nhỏ đi, hoặc cho rằng $i$ không đổi vì $\Delta\Phi$ không đổi.",
       ke=[(r"$\Delta\Phi$ không đổi, $\Delta t$ giảm một nửa nên $e_c$ và $i$ đều gấp đôi", True),
           (r"$\Delta\Phi$ không đổi nên $i$ không đổi", r"$e_c$ phụ thuộc tốc độ biến thiên $\dfrac{\Delta\Phi}{\Delta t}$; $\Delta t$ đổi thì $e_c$ đổi."),
           (r"$\Delta t$ giảm một nửa nên $i$ giảm một nửa", r"$e_c$ tỉ lệ nghịch với $\Delta t$: biến thiên nhanh hơn thì $e_c$ và $i$ lớn hơn.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>cuộn N vòng quay, đổi góc</b> → nghĩ tới <b>ΔΦ = BS(cos α₂ − cos α₁)</b> một vòng, nhân N.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Góc α lúc sau", r"Lúc sau, góc $\alpha$ giữa pháp tuyến và $\vec B$ bằng bao nhiêu độ?", 60, "°", 0.5,
       loi=r"Dùng luôn $30^\circ$ của đề (góc của mặt cuộn dây) làm $\alpha_2$."),
  buoc("Độ biến thiên từ thông qua một vòng", r"$|\Delta\Phi|$ qua một vòng dây bằng bao nhiêu (đơn vị mWb)?", 1.0, "mWb", 0.02,
       loi=r"Lấy từ thông lúc sau làm $\Delta\Phi$ (quên trừ từ thông đầu), hoặc quên đổi cm² sang m².",
       ke=[(r"$|\Delta\Phi|=BS\,|\cos\alpha_2-\cos\alpha_1|$ với $\alpha_1=0^\circ$ vì mặt vuông góc đường sức", True),
           (r"$|\Delta\Phi|=BS\cos\alpha_2$ (từ thông lúc sau)", r"Chỉ đúng nếu từ thông ban đầu bằng $0$; ở đây $\Phi_1=BS\neq0$."),
           (r"$|\Delta\Phi|=BS\,|\cos30^\circ-\cos0^\circ|$", r"$30^\circ$ là góc của mặt cuộn dây; $\alpha$ trong công thức đo từ pháp tuyến.")]),
  buoc("Suất điện động của cả cuộn", r"Độ lớn suất điện động cảm ứng trung bình trong cuộn dây bằng bao nhiêu (đơn vị V)?", 2.0, "V", 0.05,
       loi=r"Quên hệ số $N$ nên $e_c$ nhỏ hơn đúng $100$ lần.",
       ke=[(r"$|e_c|=N\,\dfrac{|\Delta\Phi|}{\Delta t}$ với $\Delta\Phi$ của một vòng", True),
           (r"$|e_c|=\dfrac{|\Delta\Phi|}{\Delta t}$ (bỏ $N$)", r"Cuộn $N$ vòng nối tiếp, mỗi vòng cho suất điện động như nhau nên cả cuộn gấp $N$ lần."),
           (r"$|e_c|=N\,|\Delta\Phi|\cdot\Delta t$", r"Faraday chia cho $\Delta t$ chứ không nhân.")]),
  buoc("Cường độ dòng điện", r"Cường độ dòng điện trung bình trong cuộn dây bằng bao nhiêu (đơn vị A)?", 0.5, "A", 0.01,
       loi=r"Nhân thêm $N$ lần nữa (đã tính $N$ trong $e_c$ rồi), hoặc nhân $e_c$ với $R$.",
       ke=[(r"$i=\dfrac{|e_c|}{R}$ với $R$ là điện trở cả cuộn", True),
           (r"$i=\dfrac{N|e_c|}{R}$", r"$e_c$ vừa tính đã là của cả cuộn $N$ vòng; nhân thêm $N$ là đếm hai lần."),
           (r"$i=|e_c|\cdot R$", r"Ôm cho $i=\dfrac{U}{R}$; nhân với $R$ cho đơn vị V·Ω.")]),
  buoc("Chiều từ trường cảm ứng", r"Từ trường do dòng cảm ứng sinh ra so với từ trường ngoài thế nào?",
       loi=r"Cho rằng từ trường cảm ứng luôn ngược chiều từ trường ngoài.",
       lua_chon=[(r"Cùng chiều", True),
                 (r"Ngược chiều", r"Ngược chiều chỉ khi từ thông tăng; ở đây từ thông qua mỗi vòng giảm theo thời gian."),
                 (r"Không có từ trường cảm ứng", r"Từ thông biến thiên và mạch kín nên có dòng cảm ứng, do đó có từ trường cảm ứng.")],
       ke=[(r"Từ thông giảm nên $\vec B_c$ bù lại, cùng chiều $\vec B$ ngoài", True),
           (r"Từ thông tăng nên $\vec B_c$ ngược chiều $\vec B$ ngoài", r"Từ thông ban đầu $BS$ lớn hơn từ thông lúc sau nên từ thông giảm, không tăng."),
           (r"Chiều của $\vec B_c$ phụ thuộc chiều quay của cuộn dây", r"Chiều của $\vec B_c$ chỉ phụ thuộc từ thông tăng hay giảm, không phụ thuộc cách quay.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>đồ thị Φ–t nhiều đoạn</b> → nghĩ tới <b>độ dốc từng đoạn là e_c</b>.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Đoạn có dòng cảm ứng", r"Mạch có dòng điện cảm ứng ở những đoạn nào?",
       loi=r"Cho rằng từ thông lớn nhất thì dòng lớn nhất, nên chọn đoạn nằm ngang.",
       lua_chon=[(r"Đoạn (1) và đoạn (3)", True),
                 (r"Cả ba đoạn vì mạch luôn kín", r"Mạch kín chưa đủ; đoạn (2) từ thông không đổi nên không có dòng."),
                 (r"Chỉ đoạn (2), vì lúc đó từ thông lớn nhất", r"Điều kiện là từ thông biến thiên, không phải từ thông lớn; đoạn (2) có $\Delta\Phi=0$.")]),
  buoc("Đoạn (1)", r"Cường độ dòng điện cảm ứng ở đoạn (1) bằng bao nhiêu (đơn vị A)?", 0.4, "A", 0.01,
       loi=r"Không đổi mWb ra Wb nên lệch $1000$ lần, hoặc lấy độ cao của đồ thị làm $e_c$.",
       ke=[(r"$|e|=\dfrac{\Delta\Phi}{\Delta t}$ (độ dốc đoạn (1), đổi mWb ra Wb), rồi $i=\dfrac{|e|}{R}$", True),
           (r"$|e|$ bằng giá trị $\Phi$ ở cuối đoạn", r"Faraday cần tốc độ biến thiên (độ dốc), không phải độ lớn của $\Phi$."),
           (r"$|e|$ bằng diện tích dưới đồ thị $\Phi$–$t$", r"Diện tích dưới đồ thị có đơn vị Wb·s, không phải V.")]),
  buoc("Đoạn (3)", r"Cường độ dòng điện cảm ứng ở đoạn (3) bằng bao nhiêu (đơn vị A)?", 0.8, "A", 0.02,
       loi=r"Lấy lại kết quả đoạn (1) vì $\Delta\Phi$ cũng bằng $20\ \text{mWb}$, quên $\Delta t$ của hai đoạn khác nhau.",
       ke=[(r"Làm như đoạn (1) nhưng dùng $\Delta t$ của chính đoạn (3)", True),
           (r"Lấy lại $i$ của đoạn (1) vì $\Delta\Phi$ cũng là $20\ \text{mWb}$", r"$\Delta t$ của đoạn (3) khác đoạn (1) nên độ dốc khác, $i$ khác."),
           (r"Lấy $\Delta t$ là toàn bộ thời gian từ $0$ đến $0{,}35\ \text{s}$", r"$\Delta t$ phải là độ dài của chính đoạn đang xét, không cộng các đoạn trước.")]),
  buoc("Chiều dòng điện (câu c)", r"Nhìn từ phía người đọc, chiều dòng điện ở đoạn (1) và đoạn (3) thế nào?",
       loi=r"Cho rằng dòng cùng chiều ở mọi đoạn vì $\vec B$ ngoài không đổi hướng; chiều phụ thuộc $\Phi$ tăng hay giảm.",
       lua_chon=[(r"Đoạn (1) ngược chiều kim đồng hồ, đoạn (3) cùng chiều kim đồng hồ", True),
                 (r"Cả hai đoạn cùng ngược chiều kim đồng hồ", r"Đoạn (3) $\Phi$ giảm nên $\vec B_c$ đổi sang cùng chiều $\vec B$ ngoài, dòng đổi chiều."),
                 (r"Đoạn (1) cùng chiều kim đồng hồ, đoạn (3) ngược chiều kim đồng hồ", r"Đoạn (1) $\Phi$ tăng nên $\vec B_c$ hướng ra khỏi giấy, tạo bởi dòng ngược chiều kim đồng hồ; hai chiều bị đảo.")],
       ke=[(r"Lenz: $\Phi$ tăng thì $\vec B_c$ ngược $\vec B$ ngoài, $\Phi$ giảm thì cùng chiều; rồi nắm tay phải", True),
           (r"Dòng cùng chiều ở mọi đoạn có dòng vì $\vec B$ ngoài không đổi hướng", r"Chiều dòng phụ thuộc từ thông tăng hay giảm, không phụ thuộc hướng $\vec B$ ngoài."),
           (r"Đoạn có $e_c$ lớn hơn thì dòng cùng chiều kim đồng hồ", r"Chiều dòng không phụ thuộc độ lớn của $e_c$.")]),
  buoc("Kiểm tra")]),
]

# ═════════════ TỰ LUẬN: ví dụ cũ chưa biên tập ═════════════
OLD = json.load(open(os.path.join(HERE, "old/13.json")))["questions"]

def vd_segments(html):
    return re.split(r'(?=<p class="[^"]*"><strong class="font-bold">VD\d+\.</strong>)', html)

def tl_bai(entry, vd, k, muc):
    segs = vd_segments(OLD[entry]["body_html"])
    seg_ = [s for s in segs if f"VD{vd}." in s[:120]][0]
    seg_ = re.sub(r'<p class="[^"]*"><strong class="font-bold">II- BÀI TẬP.*', "", seg_, flags=re.S)
    seg_ = re.sub(r'<strong class="font-bold">VD\d+\.</strong>', f'<strong class="font-bold">Bài {k}.</strong>', seg_, count=1)
    m = re.search(r'<p class="[^"]*"><strong class="font-bold">Hướng dẫn giải</strong></p>', seg_)
    de, gi = seg_[:m.start()], seg_[m.end():]
    de = re.sub(r"<(?![a-zA-Z/!?])", r"\\lt ", de); gi = re.sub(r"<(?![a-zA-Z/!?])", r"\\lt ", gi)
    return f'<h4>Bài {k} · {muc}</h4>{de}<details><summary>Hướng dẫn giải</summary>{gi}</details>'

TU_LUAN = dict(label="Bài tập tự luận (xếp từ dễ đến khó)",
  body_html="<p>Các bài còn lại của bài học, xếp từ dễ đến khó. Tự giải trên giấy rồi mới mở hướng dẫn.</p>"
  + tl_bai(1, 1, 1, "Dễ") + tl_bai(2, 5, 2, "Dễ") + tl_bai(2, 1, 3, "Trung bình") + tl_bai(2, 2, 4, "Khó"))

# ═════════════ GHI FILE ═════════════
write(J, 13, "Bài 12. Hiện tượng cảm ứng điện từ", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
d = json.load(open(J))
d["generated_at"] = "2026-10-10"
d["review"] = {"checked": False, "notes": "chờ kiểm chéo (kiem-code)"}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
print("xong", J)
