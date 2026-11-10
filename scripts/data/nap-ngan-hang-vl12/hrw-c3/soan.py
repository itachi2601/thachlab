# Sinh cau-final.json + gan-nhan.json cho 20 câu Chương 3 Từ trường phỏng theo HRW 12e (27/10/2026).
# Chạy: python3 scripts/data/nap-ngan-hang-vl12/hrw-c3/soan.py
import json, os
P = lambda s: f'<p class="text-base leading-relaxed my-2">{s}</p>'
D = os.path.dirname(os.path.abspath(__file__))
Q = []

TABLE7 = '<table style="border-collapse:collapse;margin:0.5rem 0"><tr><th style="border:1px solid currentColor;padding:4px 10px">$I$ (A)</th><td style="border:1px solid currentColor;padding:4px 10px">0,50</td><td style="border:1px solid currentColor;padding:4px 10px">1,0</td><td style="border:1px solid currentColor;padding:4px 10px">1,5</td><td style="border:1px solid currentColor;padding:4px 10px">2,0</td></tr><tr><th style="border:1px solid currentColor;padding:4px 10px">$\\Delta m$ (g)</th><td style="border:1px solid currentColor;padding:4px 10px">1,2</td><td style="border:1px solid currentColor;padding:4px 10px">2,5</td><td style="border:1px solid currentColor;padding:4px 10px">3,7</td><td style="border:1px solid currentColor;padding:4px 10px">5,0</td></tr></table>'

def mc(key, lesson, topic, diff, nguon, q, opts, ans, exp):
    Q.append(dict(key=key, src="hrw-c3", lesson_id=lesson, form="bai_tap", type="multiple_choice", question=P(q), options=opts, answer=ans, explanation="".join(P(x) for x in exp), nguon=nguon, _topic=topic, _diff=diff))

def tf(key, lesson, topic, diff, nguon, q, sts, exp):
    Q.append(dict(key=key, src="hrw-c3", lesson_id=lesson, form="bai_tap", type="true_false", question="".join(x if x.startswith("<table") else P(x) for x in q) if isinstance(q, list) else P(q), statements=[dict(text=t, answer=a) for t, a in sts], explanation="".join(P(x) for x in exp), nguon=nguon, _topic=topic, _diff=diff))

def sa(key, lesson, topic, diff, nguon, q, ans, exp):
    Q.append(dict(key=key, src="hrw-c3", lesson_id=lesson, form="bai_tap", type="short_answer", question=P(q), answer=ans, explanation="".join(P(x) for x in exp), nguon=nguon, _topic=topic, _diff=diff))

# ---------- Bài 9 (lesson 10) Khái niệm từ trường ----------
mc("hrw-c3-mc-01", 10, "Từ trường của nam châm và của dòng điện", "de", "phỏng theo HRW 12e ch.29, bài 9",
   "Hai dây dẫn thẳng dài đặt song song trong không khí, mang hai dòng điện có cùng cường độ. Tại điểm M nằm trên đoạn nối hai dây và cách đều hai dây, cảm ứng từ tổng hợp bằng 0 khi",
   ["hai dòng điện ngược chiều nhau.", "hai dòng điện cùng chiều nhau.", "hai dòng điện có chiều bất kì, vì M cách đều hai dây.", "không có trường hợp nào, vì mỗi dây đều gây từ trường tại M."],
   1,
   ["Từ trường của dòng điện thẳng dài có đường sức là các đường tròn đồng tâm quanh dây, chiều theo quy tắc nắm tay phải; độ lớn chỉ phụ thuộc cường độ dòng và khoảng cách tới dây.",
    "M cách đều hai dây và hai dòng cùng cường độ nên hai vectơ cảm ứng từ thành phần tại M có cùng độ lớn. Khi hai dòng cùng chiều, quy tắc nắm tay phải cho hai vectơ này ngược chiều nhau tại M, nên chúng triệt tiêu: $B_M = 0$.",
    "A sai vì khi hai dòng ngược chiều, hai vectơ thành phần tại M cùng chiều và cộng lại, cảm ứng từ tại M gấp đôi từ trường của một dây.",
    "C và D không đúng vì cảm ứng từ là đại lượng vectơ: cùng độ lớn chưa đủ để triệt tiêu, còn phải ngược chiều; điều đó phụ thuộc chiều hai dòng.",
    "Chọn B."])

tf("hrw-c3-tf-02", 10, "Từ trường của nam châm và của dòng điện", "tb", "phỏng theo HRW 12e ch.29, bài 3",
   "Tại một địa điểm, từ trường Trái Đất coi như nằm ngang, hướng bắc, độ lớn $2{,}5\\cdot10^{-5}$ T. Người ta kéo một dây dẫn thẳng dài nằm ngang mang dòng điện cường độ $I$ sao cho tại điểm M nằm ngay phía trên dây, cách dây 20 cm, cảm ứng từ tổng hợp bằng 0. Cho biết độ lớn cảm ứng từ của dòng điện thẳng dài tại điểm cách dây một khoảng $r$ là $B = 2\\cdot10^{-7}\\dfrac{I}{r}$ (đơn vị SI).",
   [("Tại M, cảm ứng từ do dòng điện gây ra nằm ngang và vuông góc với dây.", True),
    ("Muốn cảm ứng từ tổng hợp tại M bằng 0, dây phải đặt theo phương bắc – nam.", False),
    ("Cường độ dòng điện trong dây là 25 A.", True),
    ("Nếu tăng cường độ dòng điện lên gấp đôi thì điểm có cảm ứng từ tổng hợp bằng 0 ở ngay phía trên dây sẽ dời lại gần dây hơn.", False)],
   ["Cảm ứng từ tổng hợp bằng 0 khi cảm ứng từ của dòng điện tại M cùng độ lớn và ngược chiều với từ trường Trái Đất; dùng quy tắc nắm tay phải cho dòng điện thẳng dài.",
    "a) Đúng. Đường sức từ của dòng điện thẳng là đường tròn nằm trong mặt phẳng vuông góc với dây; tại điểm ngay phía trên dây, tiếp tuyến của đường tròn nằm ngang và vuông góc với dây.",
    "b) Sai. Cảm ứng từ của dòng điện tại M phải hướng nam để ngược với từ trường Trái Đất hướng bắc; vectơ này vuông góc với dây nên dây phải đặt theo phương đông – tây, chứ không phải bắc – nam.",
    "c) Đúng. Độ lớn bằng nhau: $2\\cdot10^{-7}\\dfrac{I}{r} = B_{\\text{TĐ}}$, suy ra $I = \\dfrac{B_{\\text{TĐ}}\\,r}{2\\cdot10^{-7}} = \\dfrac{2{,}5\\cdot10^{-5}\\cdot0{,}20}{2\\cdot10^{-7}} = 25$ A.",
    "d) Sai. Khoảng cách của điểm triệt tiêu tỉ lệ thuận với cường độ dòng điện: $r = \\dfrac{2\\cdot10^{-7} I}{B_{\\text{TĐ}}}$; $I$ gấp đôi thì $r$ gấp đôi, điểm đó dời ra xa dây hơn (40 cm) chứ không lại gần."])

# ---------- Bài 10 (lesson 11) Lực từ. Cảm ứng từ ----------
sa("hrw-c3-sa-03", 11, "Tính lực từ F = BIl·sinθ", "tb", "phỏng theo HRW 12e ch.28, bài 41",
   "Một đoạn dây đồng thẳng, khối lượng 30 g, dài 50 cm được treo nằm ngang bằng hai sợi dây dẫn mềm, nhẹ. Đoạn dây nằm trong từ trường đều có cảm ứng từ $B = 0{,}20$ T, phương nằm ngang và vuông góc với đoạn dây. Lấy $g = 9{,}8$ m/s$^2$. Cho dòng điện chạy qua đoạn dây theo chiều thích hợp để lực căng của hai sợi dây treo bằng 0. Cường độ dòng điện đó bằng bao nhiêu ampe (làm tròn đến chữ số hàng phần trăm)?",
   "2,94",
   ["Đoạn dây chịu ba lực: trọng lực hướng xuống, lực căng hai dây treo và lực từ. Dây vuông góc với $\\vec B$ nên lực từ có độ lớn $F = BIl$ và vuông góc với cả dây lẫn $\\vec B$, tức theo phương thẳng đứng.",
    "Lực căng bằng 0 khi lực từ hướng lên và cân bằng với trọng lực: $BIl = mg$.",
    "Suy ra $I = \\dfrac{mg}{Bl} = \\dfrac{0{,}030\\cdot9{,}8}{0{,}20\\cdot0{,}50} = 2{,}94$ A.",
    "Đáp số: 2,94 A."])

mc("hrw-c3-mc-04", 11, "Tính lực từ F = BIl·sinθ", "tb", "phỏng theo HRW 12e ch.28, bài 46",
   "Một thanh kim loại khối lượng 10 g đặt vuông góc trên hai thanh ray nằm ngang, song song, cách nhau 20 cm; thanh trượt không ma sát trên ray. Hệ đặt trong từ trường đều thẳng đứng có $B = 0{,}50$ T. Nối hai ray với nguồn để dòng điện không đổi 2,0 A chạy qua thanh. Thanh bắt đầu chuyển động từ trạng thái nghỉ. Sau 0,50 s, tốc độ của thanh là",
   ["10 m/s.", "0,010 m/s.", "20 m/s.", "2,5 m/s."],
   0,
   ["Thanh vuông góc với $\\vec B$ nên lực từ có độ lớn $F = BIl$, phương nằm ngang (vuông góc với thanh và với $\\vec B$); không ma sát nên lực từ là hợp lực theo phương chuyển động. Áp dụng định luật II Newton rồi công thức tốc độ của chuyển động nhanh dần đều.",
    "Lực từ: $F = BIl = 0{,}50\\cdot2{,}0\\cdot0{,}20 = 0{,}20$ N.",
    "Gia tốc: $a = \\dfrac{F}{m} = \\dfrac{0{,}20}{0{,}010} = 20$ m/s$^2$.",
    "Tốc độ sau 0,50 s: $v = at = 20\\cdot0{,}50 = 10$ m/s.",
    "B sai vì quên đổi 10 g ra 0,010 kg: lấy $m = 10$ kg cho $a = 0{,}020$ m/s$^2$ và $v = 0{,}010$ m/s.",
    "C sai vì lấy ngay gia tốc 20 m/s$^2$ làm tốc độ mà chưa nhân với thời gian.",
    "D không đúng vì $2{,}5$ m là quãng đường $s = \\tfrac12 at^2 = \\tfrac12\\cdot20\\cdot0{,}50^2$, không phải tốc độ.",
    "Chọn A."])

tf("hrw-c3-tf-05", 11, "Tính lực từ F = BIl·sinθ", "kho", "phỏng theo HRW 12e ch.28, bài 43 và 59",
   "Một khung dây cứng hình tam giác vuông ABC, vuông tại A, có $AB = 30$ cm, $AC = 40$ cm, $BC = 50$ cm, mang dòng điện 2,0 A. Khung đặt trong từ trường đều $B = 0{,}10$ T; $\\vec B$ nằm trong mặt phẳng khung và song song với cạnh huyền BC.",
   [("Lực từ tác dụng lên cạnh BC bằng 0.", True),
    ("Lực từ tác dụng lên cạnh AB có độ lớn 0,060 N.", False),
    ("Lực từ tác dụng lên cạnh AC có độ lớn lớn hơn lực từ tác dụng lên cạnh AB.", False),
    ("Hợp lực của các lực từ tác dụng lên khung bằng 0.", True)],
   ["Lực từ lên mỗi đoạn dây thẳng: $F = BIl\\sin\\theta$ với $\\theta$ là góc giữa đoạn dây và $\\vec B$. Vì $\\vec B$ song song BC nên góc của AB, AC với $\\vec B$ chính là góc của chúng với BC.",
    "a) Đúng. BC song song với $\\vec B$ nên $\\theta = 0$, $\\sin\\theta = 0$, lực từ lên BC bằng 0.",
    "b) Sai. Góc giữa AB và BC là góc $\\widehat{ABC}$ có $\\sin\\widehat{ABC} = \\dfrac{AC}{BC} = 0{,}8$, nên $F_{AB} = BIl\\sin\\theta = 0{,}10\\cdot2{,}0\\cdot0{,}30\\cdot0{,}8 = 0{,}048$ N. Giá trị 0,060 N là khi lấy $\\sin\\theta = 1$, tức coi AB vuông góc với $\\vec B$.",
    "c) Sai. Góc giữa AC và BC là góc $\\widehat{ACB}$ có $\\sin\\widehat{ACB} = \\dfrac{AB}{BC} = 0{,}6$, nên $F_{AC} = 0{,}10\\cdot2{,}0\\cdot0{,}40\\cdot0{,}6 = 0{,}048$ N, bằng đúng $F_{AB}$ chứ không lớn hơn.",
    "d) Đúng. Hai lực $F_{AB}$ và $F_{AC}$ cùng độ lớn, cùng vuông góc với mặt phẳng khung nhưng ngược chiều (dòng điện trên AB và AC chạy theo hai hướng đối với $\\vec B$), nên tổng bằng 0; cộng với $F_{BC} = 0$ ta được hợp lực lên khung kín trong từ trường đều bằng 0."])

sa("hrw-c3-sa-06", 11, "Lực từ tác dụng lên khung dây. Ngẫu lực từ", "tb", "phỏng theo HRW 12e ch.28, bài 49",
   "Một khung dây chữ nhật gồm 20 vòng, kích thước 10 cm × 5,0 cm, có dòng điện 0,50 A chạy qua, đặt trong từ trường đều $B = 0{,}40$ T. Mặt phẳng khung hợp với đường sức từ một góc $30^\\circ$. Mômen ngẫu lực từ tác dụng lên khung bằng bao nhiêu mN·m (làm tròn đến chữ số hàng phần mười)?",
   "17,3",
   ["Mômen ngẫu lực từ lên khung dây phẳng: $M = NBIS\\sin\\alpha$, trong đó $\\alpha$ là góc giữa vectơ pháp tuyến của khung và $\\vec B$.",
    "Mặt phẳng khung hợp với $\\vec B$ góc $30^\\circ$ nên pháp tuyến hợp với $\\vec B$ góc $\\alpha = 90^\\circ - 30^\\circ = 60^\\circ$.",
    "Diện tích khung: $S = 0{,}10\\cdot0{,}050 = 5{,}0\\cdot10^{-3}$ m$^2$.",
    "$M = NBIS\\sin\\alpha = 20\\cdot0{,}40\\cdot0{,}50\\cdot5{,}0\\cdot10^{-3}\\cdot\\sin60^\\circ = 0{,}020\\cdot0{,}866 = 0{,}0173$ N·m $= 17{,}3$ mN·m.",
    "Nếu lấy nhầm $\\sin30^\\circ$ sẽ được 10,0 mN·m; đó là lỗi nhầm góc giữa mặt phẳng khung và góc giữa pháp tuyến với $\\vec B$.",
    "Đáp số: 17,3 mN·m."])

# ---------- Bài 11 (lesson 12) Thực hành đo độ lớn cảm ứng từ ----------
tf("hrw-c3-tf-07", 12, "Cảm ứng từ và đơn vị tesla", "tb", "phỏng theo HRW 12e ch.28, bài 41 (ý cân lực từ với trọng lực)",
   ["Để đo cảm ứng từ trong khe một nam châm chữ U, một nhóm học sinh đặt nam châm lên cân điện tử rồi luồn vào khe một đoạn dây dẫn thẳng nằm ngang dài $l = 5{,}0$ cm, vuông góc với đường sức từ; dây được giữ cố định bằng giá đỡ, không chạm cân. Khi cho dòng điện cường độ $I$ chạy qua dây, số chỉ của cân tăng thêm một lượng $\\Delta m$ so với lúc chưa có dòng. Kết quả đo:",
    TABLE7,
    "Lấy $g = 9{,}8$ m/s$^2$."],
   [("Độ lớn lực từ tác dụng lên đoạn dây bằng trọng lượng ứng với khối lượng chênh lệch $\\Delta m$.", True),
    ("Số liệu cho thấy $\\Delta m$ tỉ lệ với bình phương cường độ dòng điện.", False),
    ("Cảm ứng từ trong khe nam châm xấp xỉ 0,49 T.", True),
    ("Nếu đảo chiều dòng điện trong dây, số chỉ của cân vẫn tăng thêm cùng một lượng $\\Delta m$.", False)],
   ["Dòng điện trong dây chịu lực từ $F = BIl$ (dây vuông góc với $\\vec B$); theo định luật III Newton, nam châm chịu phản lực cùng độ lớn, ngược chiều, làm số chỉ cân thay đổi.",
    "a) Đúng. Dây được giữ cố định nên phần số chỉ tăng thêm chính là phản lực của lực từ ép nam châm xuống cân: $F = \\Delta m\\,g$.",
    "b) Sai. Tăng $I$ gấp đôi (0,50 A lên 1,0 A) thì $\\Delta m$ tăng gấp đôi (1,2 g lên 2,5 g, sai số đo); gấp bốn (2,0 A) thì $\\Delta m$ gấp bốn (5,0 g). Vậy $\\Delta m$ tỉ lệ thuận với $I$, đúng như $F = BIl$, không phải tỉ lệ với $I^2$.",
    "c) Đúng. Từ $\\Delta m\\,g = BIl$ suy ra $B = \\dfrac{\\Delta m\\,g}{Il}$. Lấy cặp (2,0 A; 5,0 g): $B = \\dfrac{5{,}0\\cdot10^{-3}\\cdot9{,}8}{2{,}0\\cdot0{,}050} = 0{,}49$ T; các cặp còn lại cho cùng giá trị trong sai số.",
    "d) Sai. Đảo chiều dòng điện thì lực từ lên dây đổi chiều (quy tắc bàn tay trái), phản lực lên nam châm hướng lên, số chỉ của cân giảm đi $\\Delta m$ chứ không tăng."])

# ---------- Bài 16 (lesson 127) Điện từ trường ----------
tf("hrw-c3-tf-08", 127, "Điện từ trường và sóng điện từ", "de", "phỏng theo HRW 12e ch.30 mục 30.6 (ý định tính về điện trường cảm ứng)",
   "Đưa nhanh một thanh nam châm lại gần một vòng dây dẫn kín đặt cố định; trong vòng dây xuất hiện dòng điện cảm ứng.",
   [("Từ trường biến thiên tại chỗ đặt vòng dây đã sinh ra một điện trường xoáy, chính điện trường này đẩy các electron tự do trong dây chuyển động thành dòng.", True),
    ("Đường sức của điện trường xoáy xuất phát từ điện tích dương và kết thúc ở điện tích âm.", False),
    ("Nếu bỏ vòng dây đi mà vẫn đưa nam châm lại gần như cũ thì tại chỗ đó không còn điện trường xoáy.", False),
    ("Điện trường biến thiên đến lượt nó lại sinh ra từ trường; hai trường biến thiên này lan truyền trong không gian tạo thành sóng điện từ.", True)],
   ["Theo thuyết điện từ của Maxwell, từ trường biến thiên theo thời gian sinh ra điện trường xoáy, và điện trường biến thiên sinh ra từ trường; hai trường gắn bó với nhau thành điện từ trường.",
    "a) Đúng. Dòng điện cảm ứng là hệ quả của điện trường xoáy do từ trường biến thiên sinh ra; điện trường này tác dụng lực lên electron tự do trong dây.",
    "b) Sai. Điện trường xoáy có đường sức là những đường cong kín, không có điểm đầu điểm cuối; chỉ điện trường tĩnh của điện tích mới có đường sức xuất phát từ điện tích dương và kết thúc ở điện tích âm.",
    "c) Sai. Điện trường xoáy do từ trường biến thiên sinh ra, tồn tại trong không gian bất kể có vòng dây hay không; vòng dây chỉ là nơi để điện trường ấy biểu hiện thành dòng điện.",
    "d) Đúng. Điện trường biến thiên sinh ra từ trường và ngược lại, quá trình lan truyền của điện từ trường biến thiên trong không gian chính là sóng điện từ."])

# ---------- Bài 12 (lesson 13) Cảm ứng điện từ ----------
tf("hrw-c3-tf-09", 13, "Định luật Faraday và định luật Lenz", "tb", "phỏng theo HRW 12e ch.30, bài 4",
   ["Một vòng dây dẫn kín phẳng có diện tích 20 cm$^2$, điện trở 0,10 Ω, đặt vuông góc với một từ trường đều có độ lớn $B$ thay đổi theo thời gian như sau:",
    "từ $t = 0$ đến $t = 2{,}0$ s: $B$ tăng đều từ 0 đến 0,40 T;",
    "từ $t = 2{,}0$ s đến $t = 4{,}0$ s: $B$ giữ nguyên 0,40 T;",
    "từ $t = 4{,}0$ s đến $t = 6{,}0$ s: $B$ giảm đều từ 0,40 T về 0."],
   [("Trong khoảng từ 0 đến 2,0 s, suất điện động cảm ứng trong vòng dây có độ lớn 0,40 mV.", True),
    ("Trong khoảng từ 2,0 s đến 4,0 s, dòng điện cảm ứng lớn nhất vì từ thông qua vòng dây lớn nhất.", False),
    ("Dòng điện cảm ứng trong khoảng từ 4,0 s đến 6,0 s ngược chiều với dòng điện cảm ứng trong khoảng từ 0 đến 2,0 s.", True),
    ("Trong khoảng từ 0 đến 2,0 s, cường độ dòng điện cảm ứng bằng 0,40 mA.", False)],
   ["Định luật Faraday: độ lớn suất điện động cảm ứng $e = \\left|\\dfrac{\\Delta\\Phi}{\\Delta t}\\right|$ với $\\Phi = BS$ (vòng dây vuông góc từ trường, một vòng); dòng cảm ứng $i = \\dfrac{e}{R}$; chiều theo định luật Lenz.",
    "a) Đúng. $S = 20$ cm$^2 = 2{,}0\\cdot10^{-3}$ m$^2$; $e = S\\dfrac{\\Delta B}{\\Delta t} = 2{,}0\\cdot10^{-3}\\cdot\\dfrac{0{,}40}{2{,}0} = 4{,}0\\cdot10^{-4}$ V $= 0{,}40$ mV.",
    "b) Sai. Suất điện động cảm ứng phụ thuộc tốc độ biến thiên của từ thông chứ không phụ thuộc độ lớn từ thông; trong khoảng này $B$ không đổi nên $\\Delta\\Phi = 0$, $e = 0$ và không có dòng cảm ứng.",
    "c) Đúng. Từ 0 đến 2,0 s từ thông tăng, dòng cảm ứng sinh từ trường chống lại sự tăng; từ 4,0 s đến 6,0 s từ thông giảm, dòng cảm ứng sinh từ trường chống lại sự giảm, nên hai dòng ngược chiều nhau.",
    "d) Sai. $i = \\dfrac{e}{R} = \\dfrac{4{,}0\\cdot10^{-4}}{0{,}10} = 4{,}0\\cdot10^{-3}$ A $= 4{,}0$ mA, chứ không phải 0,40 mA (đó là số đo của $e$ tính bằng mV, chưa chia cho điện trở)."])

sa("hrw-c3-sa-10", 13, "Từ thông qua khung dây", "kho", "phỏng theo HRW 12e ch.30, bài 13 và 20",
   "Một cuộn dây dẹt gồm 100 vòng, diện tích mỗi vòng 4,0 cm$^2$, được nối với một điện kế; điện trở toàn mạch (cuộn dây và điện kế) là 2,0 Ω. Cuộn dây đặt trong từ trường đều $B = 0{,}050$ T, mặt phẳng cuộn dây vuông góc với đường sức từ. Người ta lật nhanh cuộn dây một góc $180^\\circ$ quanh một trục nằm trong mặt phẳng cuộn dây. Điện lượng chuyển qua điện kế trong quá trình lật bằng bao nhiêu milicoulomb (làm tròn đến chữ số hàng phần mười)?",
   "2,0",
   ["Dùng định luật Faraday $e = N\\left|\\dfrac{\\Delta\\Phi}{\\Delta t}\\right|$ kết hợp định luật Ohm $i = \\dfrac{e}{R}$ và điện lượng $q = i\\,\\Delta t$ ($i$ là cường độ dòng điện trung bình trong thời gian lật): suy ra $q = \\dfrac{N\\,|\\Delta\\Phi|}{R}$, không phụ thuộc thời gian lật nhanh hay chậm.",
    "Trước khi lật, từ thông qua mỗi vòng là $\\Phi_1 = BS\\cos0^\\circ = BS$; sau khi lật $180^\\circ$, pháp tuyến đổi chiều nên $\\Phi_2 = BS\\cos180^\\circ = -BS$.",
    "Độ biến thiên từ thông qua mỗi vòng: $|\\Delta\\Phi| = 2BS = 2\\cdot0{,}050\\cdot4{,}0\\cdot10^{-4} = 4{,}0\\cdot10^{-5}$ Wb.",
    "Điện lượng: $q = \\dfrac{N\\,|\\Delta\\Phi|}{R} = \\dfrac{100\\cdot4{,}0\\cdot10^{-5}}{2{,}0} = 2{,}0\\cdot10^{-3}$ C $= 2{,}0$ mC.",
    "Nếu quên rằng từ thông đổi dấu (lấy $|\\Delta\\Phi| = BS$) sẽ được 1,0 mC, chỉ bằng một nửa.",
    "Đáp số: 2,0 mC."])

sa("hrw-c3-sa-12", 13, "Suất điện động do thanh dẫn chuyển động", "tb", "phỏng theo HRW 12e ch.30, bài 29 và 35",
   "Một thanh kim loại dài $L = 40$ cm trượt trên hai thanh ray nằm ngang, song song, hai đầu ray nối với nhau bằng một điện trở 0,20 Ω; bỏ qua điện trở thanh và ray, bỏ qua ma sát. Hệ đặt trong từ trường đều thẳng đứng $B = 0{,}50$ T. Người ta kéo thanh chuyển động thẳng đều với tốc độ 2,0 m/s, thanh luôn vuông góc với ray. Lực kéo bằng bao nhiêu newton?",
   "0,4",
   ["Thanh dẫn chuyển động cắt đường sức từ nên có suất điện động cảm ứng $e = BLv$ (thanh, vận tốc và $\\vec B$ đôi một vuông góc). Mạch kín có dòng $i = \\dfrac{e}{R}$; dòng này chịu lực từ $F = BiL$ cản chuyển động (định luật Lenz), nên muốn thanh chuyển động đều thì lực kéo phải cân bằng với lực từ.",
    "Suất điện động: $e = BLv = 0{,}50\\cdot0{,}40\\cdot2{,}0 = 0{,}40$ V.",
    "Cường độ dòng điện: $i = \\dfrac{e}{R} = \\dfrac{0{,}40}{0{,}20} = 2{,}0$ A.",
    "Lực từ cản thanh: $F = BiL = 0{,}50\\cdot2{,}0\\cdot0{,}40 = 0{,}40$ N; lực kéo bằng lực này.",
    "Kiểm tra: công suất lực kéo $Fv = 0{,}40\\cdot2{,}0 = 0{,}80$ W đúng bằng công suất toả nhiệt $i^2R = 2{,}0^2\\cdot0{,}20 = 0{,}80$ W.",
    "Đáp số: 0,4 N."])

# ---------- Bài 15 (lesson 126) Ứng dụng cảm ứng điện từ ----------
tf("hrw-c3-tf-13", 126, "Suất điện động do thanh dẫn chuyển động", "kho", "phỏng theo HRW 12e ch.30, bài 34",
   "Một khung dây dẫn hình chữ nhật, cạnh ngang dài $L = 20$ cm, cạnh đứng khá dài, khối lượng 20 g, điện trở 0,10 Ω, được thả rơi theo phương thẳng đứng. Trong suốt quá trình xét, chỉ có cạnh ngang phía dưới nằm trong vùng từ trường đều $B = 0{,}50$ T nằm ngang, vuông góc với mặt phẳng khung; cạnh ngang phía trên nằm ngoài vùng từ trường. Lấy $g = 9{,}8$ m/s$^2$, bỏ qua lực cản không khí.",
   [("Lực từ tác dụng lên cạnh dưới của khung hướng xuống, cùng chiều chuyển động của khung.", False),
    ("Lực từ tác dụng lên khung có độ lớn tỉ lệ thuận với tốc độ rơi của khung.", True),
    ("Khung sẽ đạt tốc độ giới hạn xấp xỉ 1,96 m/s.", True),
    ("Nếu thay khung bằng một khung cùng kích thước, cùng khối lượng nhưng điện trở lớn hơn thì tốc độ giới hạn nhỏ hơn.", False)],
   ["Cạnh dưới chuyển động cắt đường sức nên có suất điện động $e = BLv$; mạch khung kín nên có dòng $i = \\dfrac{e}{R}$; cạnh dưới mang dòng chịu lực từ $F = BiL$. Đây là nguyên tắc của phanh điện từ.",
    "a) Sai. Theo định luật Lenz, dòng cảm ứng có tác dụng chống lại chuyển động sinh ra nó, nên lực từ lên cạnh dưới hướng lên, ngược chiều rơi; đó là lực hãm.",
    "b) Đúng. $F = BiL = B\\dfrac{BLv}{R}L = \\dfrac{B^2L^2}{R}v$, tỉ lệ thuận với $v$: khung rơi càng nhanh thì lực hãm càng lớn.",
    "c) Đúng. Tốc độ giới hạn đạt được khi lực hãm cân bằng trọng lực: $\\dfrac{B^2L^2}{R}v = mg$, suy ra $v = \\dfrac{mgR}{B^2L^2} = \\dfrac{0{,}020\\cdot9{,}8\\cdot0{,}10}{0{,}50^2\\cdot0{,}20^2} = \\dfrac{0{,}0196}{0{,}010} = 1{,}96$ m/s.",
    "d) Sai. Từ $v = \\dfrac{mgR}{B^2L^2}$, điện trở $R$ lớn hơn thì dòng cảm ứng nhỏ hơn, lực hãm yếu hơn, khung phải rơi nhanh hơn mới cân bằng được trọng lực: tốc độ giới hạn lớn hơn chứ không nhỏ hơn."])

mc("hrw-c3-mc-14", 126, "Định luật Faraday và định luật Lenz", "de", "phỏng theo HRW 12e ch.30, Question 12",
   "Hai vòng dây có cùng hình dạng và kích thước, một vòng bằng đồng và một vòng bằng nhựa, được kéo ra khỏi vùng có từ trường đều với cùng tốc độ, mặt phẳng vòng vuông góc với đường sức từ. Phát biểu nào sau đây đúng?",
   ["Vòng nhựa cần lực kéo lớn hơn vì nhựa là chất cách điện.", "Hai vòng cần lực kéo như nhau vì từ thông qua chúng biến thiên như nhau.", "Trong vòng nhựa cũng có dòng điện cảm ứng nhưng yếu hơn trong vòng đồng.", "Vòng đồng cần lực kéo lớn hơn vì trong nó có dòng điện cảm ứng chịu lực từ cản lại chuyển động."],
   3,
   ["Khi kéo vòng ra khỏi từ trường, từ thông qua vòng giảm, trong vòng xuất hiện suất điện động cảm ứng; theo định luật Lenz, dòng cảm ứng (nếu có) sinh ra lực từ chống lại chuyển động kéo.",
    "Vòng đồng dẫn điện nên có dòng cảm ứng, dòng này chịu lực từ cản chuyển động; muốn kéo đều phải thêm lực để thắng lực cản ấy. Vòng nhựa không có electron tự do nên dù suất điện động cảm ứng vẫn có, không có dòng điện, không có lực từ; chỉ cần lực kéo rất nhỏ.",
    "A sai vì chất cách điện không có dòng cảm ứng, do đó không có lực từ cản; không có lí do gì để cần lực lớn hơn.",
    "B sai vì từ thông biến thiên như nhau chỉ cho suất điện động như nhau; lực cản còn phụ thuộc có dòng điện hay không, mà điều này phụ thuộc vật liệu.",
    "C sai vì trong nhựa không có hạt mang điện tự do, không thể có dòng điện cảm ứng.",
    "Chọn D."])

# ---------- Bài 13 (lesson 14) Đại cương về dòng điện xoay chiều ----------
mc("hrw-c3-mc-15", 14, "Giá trị hiệu dụng của dòng điện xoay chiều", "de", "phỏng theo HRW 12e ch.31, bài 54 và 55",
   "Một dòng điện xoay chiều có cường độ cực đại 2,0 A chạy qua một điện trở. Muốn một dòng điện không đổi chạy qua cùng điện trở đó toả ra nhiệt lượng bằng với dòng xoay chiều trong cùng thời gian thì cường độ dòng không đổi phải bằng",
   ["2,0 A.", "1,41 A.", "2,83 A.", "1,0 A."],
   1,
   ["Giá trị hiệu dụng của dòng xoay chiều được định nghĩa đúng bằng cường độ dòng không đổi gây cùng tác dụng nhiệt trên cùng điện trở trong cùng thời gian: $I = \\dfrac{I_0}{\\sqrt2}$.",
    "$I = \\dfrac{I_0}{\\sqrt2} = \\dfrac{2{,}0}{1{,}414} = 1{,}41$ A.",
    "A sai vì đồng nhất giá trị cực đại với giá trị hiệu dụng; dòng xoay chiều chỉ đạt 2,0 A trong những thời điểm rất ngắn, phần lớn thời gian nhỏ hơn, nên tác dụng nhiệt trung bình kém dòng không đổi 2,0 A.",
    "C sai vì nhân với $\\sqrt2$ thay vì chia: $2{,}0\\cdot1{,}414 = 2{,}83$ A.",
    "D không đúng vì chia cho 2 thay vì cho $\\sqrt2$; tác dụng nhiệt tỉ lệ với $i^2$ nên hệ số là $\\sqrt2$.",
    "Chọn B."])

sa("hrw-c3-sa-16", 14, "Giá trị hiệu dụng của dòng điện xoay chiều", "de", "phỏng theo HRW 12e ch.31, bài 53 (ý thiết bị gia đình quy về điện trở)",
   "Một ấm đun nước ghi 220 V – 1100 W được cắm vào mạng điện xoay chiều có điện áp hiệu dụng 220 V. Coi dây đốt của ấm là một điện trở thuần. Điện trở của dây đốt bằng bao nhiêu ôm?",
   "44",
   ["Với mạch chỉ có điện trở thuần, công suất tiêu thụ tính theo giá trị hiệu dụng: $P = UI = \\dfrac{U^2}{R}$; số ghi 220 V – 1100 W là điện áp hiệu dụng định mức và công suất định mức.",
    "$R = \\dfrac{U^2}{P} = \\dfrac{220^2}{1100} = \\dfrac{48400}{1100} = 44$ Ω.",
    "Có thể kiểm lại qua dòng hiệu dụng: $I = \\dfrac{P}{U} = \\dfrac{1100}{220} = 5{,}0$ A, rồi $R = \\dfrac{U}{I} = \\dfrac{220}{5{,}0} = 44$ Ω.",
    "Đáp số: 44 Ω."])

tf("hrw-c3-tf-17", 14, "Giá trị hiệu dụng của dòng điện xoay chiều", "tb", "phỏng theo HRW 12e ch.31, bài 93",
   "Một người vô ý chạm hai bàn tay vào hai điểm của mạng điện xoay chiều có điện áp hiệu dụng 220 V. Coi cơ thể người là một điện trở 500 Ω nối tiếp với hai điện trở của lớp da ở hai bàn tay; điện trở lớp da mỗi bàn tay là 50 kΩ khi da khô và 1,0 kΩ khi da ướt mồ hôi. Biết dòng điện xoay chiều qua người cỡ 1 mA gây cảm giác giật, cỡ 10 mA làm cơ co cứng khiến người không tự buông tay được, từ 100 mA trở lên có thể gây rung tim.",
   [("Khi da khô, cường độ dòng điện hiệu dụng qua người xấp xỉ 4,4 mA.", False),
    ("Khi da ướt, cường độ dòng điện hiệu dụng qua người xấp xỉ 88 mA.", True),
    ("Khi da ướt, người này khó có thể tự buông tay khỏi mạng điện.", True),
    ("Khi da ướt, dòng điện qua người đã vượt ngưỡng có thể gây rung tim.", False)],
   ["Ba điện trở nối tiếp nên điện trở toàn mạch là tổng của chúng; cường độ hiệu dụng tính theo định luật Ohm với giá trị hiệu dụng: $I = \\dfrac{U}{R_{\\text{tổng}}}$.",
    "a) Sai. Da khô: $R_{\\text{tổng}} = 500 + 2\\cdot50000 = 100500$ Ω, $I = \\dfrac{220}{100500} = 2{,}2\\cdot10^{-3}$ A $= 2{,}2$ mA. Giá trị 4,4 mA là khi chỉ tính điện trở da của một bàn tay ($220/50000$), bỏ sót bàn tay kia và cơ thể.",
    "b) Đúng. Da ướt: $R_{\\text{tổng}} = 500 + 2\\cdot1000 = 2500$ Ω, $I = \\dfrac{220}{2500} = 0{,}088$ A $= 88$ mA.",
    "c) Đúng. 88 mA lớn hơn nhiều so với ngưỡng 10 mA làm cơ co cứng, nên người này không tự buông tay được; đây là lí do tay ướt chạm điện nguy hiểm hơn hẳn tay khô.",
    "d) Sai. 88 mA vẫn nhỏ hơn ngưỡng 100 mA nêu trong đề, nên chưa tới ngưỡng rung tim, dù đã rất gần và cực kì nguy hiểm."])

mc("hrw-c3-mc-18", 14, "Viết biểu thức u, i theo thời gian", "de", "phỏng theo HRW 12e ch.31, bài 67 (ý đọc thời điểm từ biểu thức)",
   "Điện áp giữa hai đầu một ổ cắm trong nhà có biểu thức $u = 220\\sqrt2\\cos(100\\pi t)$ (V), với $t$ tính bằng giây. Kể từ thời điểm $t = 0$, điện áp tức thời bằng 0 lần đầu tiên vào thời điểm",
   ["2,5 ms.", "10 ms.", "5,0 ms.", "20 ms."],
   2,
   ["Từ biểu thức $u = U_0\\cos(\\omega t)$ với $\\omega = 100\\pi$ rad/s, chu kì $T = \\dfrac{2\\pi}{\\omega} = \\dfrac{2\\pi}{100\\pi} = 0{,}02$ s $= 20$ ms (tần số 50 Hz).",
    "Tại $t = 0$, $u = U_0$ (cực đại). Hàm cosin giảm từ cực đại về 0 sau một phần tư chu kì: $t = \\dfrac{T}{4} = 5{,}0$ ms.",
    "Kiểm tra: $u = 0$ khi $100\\pi t = \\dfrac{\\pi}{2}$, tức $t = \\dfrac{1}{200}$ s $= 5{,}0$ ms.",
    "B sai vì 10 ms là $T/2$, lúc đó $u = -U_0$, điện áp đạt cực tiểu chứ không bằng 0.",
    "D sai vì 20 ms là trọn một chu kì, điện áp trở lại cực đại $U_0$.",
    "A không đúng vì 2,5 ms là $T/8$, khi đó $u = U_0\\cos\\dfrac{\\pi}{4} \\ne 0$.",
    "Chọn C."])

# ---------- Bài 14 (lesson 125) Máy phát điện. Máy biến áp ----------
mc("hrw-c3-mc-11", 125, "Nguyên tắc tạo ra dòng điện xoay chiều", "tb", "phỏng theo HRW 12e ch.30, bài 19",
   "Phần ứng của một máy phát điện xoay chiều nhỏ là một cuộn dây gồm 200 vòng, diện tích mỗi vòng 50 cm$^2$, quay đều với tốc độ 600 vòng/phút quanh một trục nằm trong mặt phẳng cuộn dây và vuông góc với từ trường đều có $B = 0{,}20$ T. Suất điện động cực đại xuất hiện trong cuộn dây là",
   ["120 V.", "8,9 V.", "12,6 V.", "2,0 V."],
   2,
   ["Cuộn dây quay đều trong từ trường đều thì từ thông biến thiên điều hoà, suất điện động cảm ứng có dạng $e = NBS\\omega\\sin(\\omega t)$, giá trị cực đại $E_0 = NBS\\omega$ với $\\omega$ là tốc độ góc tính bằng rad/s.",
    "Đổi tốc độ quay: $600$ vòng/phút $= 10$ vòng/s, nên $\\omega = 2\\pi\\cdot10 = 20\\pi \\approx 62{,}8$ rad/s.",
    "$E_0 = NBS\\omega = 200\\cdot0{,}20\\cdot50\\cdot10^{-4}\\cdot62{,}8 = 0{,}20\\cdot62{,}8 = 12{,}6$ V.",
    "A sai vì lấy thẳng 600 vòng/phút làm $\\omega$: $0{,}20\\cdot600 = 120$ V, quên đổi ra rad/s.",
    "B sai vì chia thêm cho $\\sqrt2$: $12{,}6/\\sqrt2 = 8{,}9$ V là giá trị hiệu dụng, đề hỏi giá trị cực đại.",
    "D sai vì dùng tần số $f = 10$ Hz thay cho $\\omega$: $0{,}20\\cdot10 = 2{,}0$ V, thiếu thừa số $2\\pi$.",
    "Chọn C."])

tf("hrw-c3-tf-19", 125, "Máy biến áp", "kho", "phỏng theo HRW 12e ch.31, bài 65",
   "Một trạm phát điện nhỏ truyền công suất 100 kW đến một xưởng sản xuất bằng đường dây gồm hai dây dẫn (dây đi và dây về), điện trở mỗi dây là 2,0 Ω. Coi điện áp và dòng điện cùng pha, hao phí chỉ do toả nhiệt trên đường dây. Xét hai phương án: dùng máy tăng áp để điện áp hiệu dụng ở đầu đường dây là 10 kV, hoặc truyền trực tiếp với điện áp 1,0 kV.",
   [("Khi truyền ở 10 kV, công suất hao phí trên đường dây là 200 W.", False),
    ("Khi truyền ở 10 kV, cường độ dòng điện hiệu dụng trên đường dây là 10 A.", True),
    ("Giảm điện áp truyền tải từ 10 kV xuống 1,0 kV thì công suất hao phí tăng 100 lần.", True),
    ("Khi truyền ở 1,0 kV, độ sụt áp trên đường dây là 200 V.", False)],
   ["Với dòng và điện áp cùng pha, công suất truyền $P = UI$ nên $I = \\dfrac{P}{U}$; công suất hao phí trên đường dây $P_{\\text{hp}} = I^2R$ với $R$ là điện trở của cả hai dây; độ sụt áp trên dây $\\Delta U = IR$.",
    "a) Sai. Điện trở đường dây gồm cả dây đi và dây về: $R = 2\\cdot2{,}0 = 4{,}0$ Ω. Ở 10 kV: $I = \\dfrac{100000}{10000} = 10$ A, $P_{\\text{hp}} = I^2R = 10^2\\cdot4{,}0 = 400$ W. Giá trị 200 W là khi chỉ tính điện trở của một dây.",
    "b) Đúng. $I = \\dfrac{P}{U} = \\dfrac{100\\cdot10^3}{10\\cdot10^3} = 10$ A.",
    "c) Đúng. $P_{\\text{hp}} = \\dfrac{P^2R}{U^2}$ tỉ lệ nghịch với $U^2$; $U$ giảm 10 lần thì $P_{\\text{hp}}$ tăng 100 lần: ở 1,0 kV, $I = 100$ A, $P_{\\text{hp}} = 100^2\\cdot4{,}0 = 40$ kW, bằng 40 % công suất phát. Đó là lí do phải tăng áp trước khi truyền tải đi xa.",
    "d) Sai. Ở 1,0 kV: $\\Delta U = IR = 100\\cdot4{,}0 = 400$ V, tức sụt mất 40 % điện áp đầu đường dây, chứ không phải 200 V (giá trị khi chỉ tính một dây)."])

sa("hrw-c3-sa-20", 125, "Máy biến áp", "tb", "phỏng theo HRW 12e ch.31, bài 63",
   "Một máy biến áp lí tưởng có cuộn sơ cấp 1100 vòng, cuộn thứ cấp 60 vòng. Cuộn sơ cấp nối với mạng điện xoay chiều có điện áp hiệu dụng 220 V; cuộn thứ cấp nối với một bóng đèn coi như điện trở thuần 4,0 Ω. Cường độ dòng điện hiệu dụng trong cuộn sơ cấp bằng bao nhiêu miliampe (làm tròn đến hàng đơn vị)?",
   "164",
   ["Máy biến áp lí tưởng: $\\dfrac{U_2}{U_1} = \\dfrac{N_2}{N_1}$ và bỏ qua hao phí nên công suất hai cuộn bằng nhau $U_1I_1 = U_2I_2$, suy ra $\\dfrac{I_1}{I_2} = \\dfrac{N_2}{N_1}$ (dòng tỉ lệ nghịch với số vòng).",
    "Điện áp thứ cấp: $U_2 = U_1\\dfrac{N_2}{N_1} = 220\\cdot\\dfrac{60}{1100} = 12$ V.",
    "Dòng thứ cấp qua bóng đèn: $I_2 = \\dfrac{U_2}{R} = \\dfrac{12}{4{,}0} = 3{,}0$ A.",
    "Dòng sơ cấp: $I_1 = I_2\\dfrac{N_2}{N_1} = 3{,}0\\cdot\\dfrac{60}{1100} = 0{,}164$ A $= 164$ mA.",
    "Kiểm tra: $U_1I_1 = 220\\cdot0{,}164 = 36$ W, bằng $U_2I_2 = 12\\cdot3{,}0 = 36$ W. Nếu nhầm chiều tỉ lệ (lấy $I_1 = I_2 N_1/N_2$) sẽ được 55 A, lớn hơn nhiều dòng thứ cấp, vô lí với máy hạ áp.",
    "Đáp số: 164 mA."])

# ---------- xuất file ----------
order = ["hrw-c3-mc-01", "hrw-c3-tf-02", "hrw-c3-sa-03", "hrw-c3-mc-04", "hrw-c3-tf-05", "hrw-c3-sa-06", "hrw-c3-tf-07", "hrw-c3-tf-08",
         "hrw-c3-tf-09", "hrw-c3-sa-10", "hrw-c3-mc-11", "hrw-c3-sa-12", "hrw-c3-tf-13", "hrw-c3-mc-14", "hrw-c3-mc-15", "hrw-c3-sa-16",
         "hrw-c3-tf-17", "hrw-c3-mc-18", "hrw-c3-tf-19", "hrw-c3-sa-20"]
Q.sort(key=lambda q: order.index(q["key"]))
for i, q in enumerate(Q, 1): q["num"] = i
nhan = {q["key"]: {"topic": q.pop("_topic"), "difficulty": q.pop("_diff")} for q in Q}
json.dump(Q, open(os.path.join(D, "cau-final.json"), "w"), ensure_ascii=False, indent=1)
json.dump(nhan, open(os.path.join(D, "gan-nhan.json"), "w"), ensure_ascii=False, indent=1)
import collections
print(len(Q), collections.Counter(q["type"] for q in Q), collections.Counter(n["difficulty"] for n in nhan.values()), collections.Counter(q["lesson_id"] for q in Q))
