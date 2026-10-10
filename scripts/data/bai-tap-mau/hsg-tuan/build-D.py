"""Phần D: Bài 10, 11, 12 của bộ 12 bài tự luận Cơ học HSG -> part-D.json (lesson 167). Chạy: python3 build-D.py"""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
HERE = os.path.dirname(os.path.abspath(__file__))
g = 10
def close(a, b, t=1e-6): assert abs(a - b) <= t * max(1, abs(b)), (a, b)

# ---------- số liệu (tính thật) ----------
m, l, h, v, Fc, H, q = 1200, 1000, 50, 36 / 3.6, 400, 0.25, 4.6e7
Ptl = g * m; Ph = Ptl * h / l; Fk = Ph + Fc; Pw = Fk * v; Acv = Fk * l; Q = Acv / H; mx = Q / q
close(v, 10); close(Ptl, 12000); close(Ph, 600); close(Fk, 1000); close(Pw, 10000); close(Acv, 1e6); close(Q, 4e6); close(mx * 1000, 86.96, 1e-3)
m2, h2m, MN, Fms = 0.5, 5, 10, 1
W0 = g * m2 * h2m; v11 = math.sqrt(2 * g * h2m); WN = W0 - Fms * MN; hh2 = WN / (g * m2); s_tong = W0 / Fms
close(W0, 25); close(v11, 10); close(WN, 15); close(hh2, 3); close(s_tong, 25); close(s_tong - 2 * MN, 5)
Pdc, Hb, hb, vb, Vbe = 1500, 0.6, 10, 4, 30
Pi = Pdc * Hb; qa = Pi / (g * hb); e = g * hb + vb ** 2 / 2; qb = Pi / e; t = Vbe * 1000 / qb; E = Pdc / 1000 * t / 3600
close(Pi, 900); close(qa, 9); close(e, 108); close(qb, 8.3333, 1e-4); close(t, 3600); close(E, 1.5)

# ---------- hình (tĩnh) ----------
def T(x, y, s, c="currentColor", size=13, anchor="start", w="600"): return lbl(x, y, s, c, size, anchor, w)
def slope_fig():
    A_, B_, C_ = (24, 190), (330, 190), (330, 70)
    body = f'<polygon points="{A_[0]},{A_[1]} {B_[0]},{B_[1]} {C_[0]},{C_[1]}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
    ang = math.degrees(math.atan2(120, 306)); ux, uy = 306 / math.hypot(306, 120), -120 / math.hypot(306, 120)
    x0, y0 = 24 + ux * 150, 190 + uy * 150
    body += (f'<g transform="translate({x0:.1f},{y0:.1f}) rotate({-ang:.1f})"><rect x="-30" y="-16" width="60" height="16" fill="none" stroke="currentColor" stroke-width="2.2"/>'
             '<rect x="-14" y="-28" width="26" height="12" fill="none" stroke="currentColor" stroke-width="2.2"/>'
             '<circle cx="-16" cy="2" r="4.5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="16" cy="2" r="4.5" fill="none" stroke="currentColor" stroke-width="2"/>'
             + arrow("", "r", 38, -8, 90, -8, 2.4) + T(40, -16, "v = 36 km/h", RED, 12, "start", "700") + '</g>')
    body += dim("", "o", 346, 70, 346, 190, "h = 50 m", 352, 134)
    body += dim("", "b", 24, 214, 330, 214, "dốc dài l = 1 km", 177, 234, "middle")
    body += '<text x="30" y="30" font-size="12" font-weight="600" fill="currentColor">m = 1 200 kg · F<tspan dy="4" font-size="9">c</tspan><tspan dy="-4"> = 400 N</tspan></text>'
    return fig("hsg-10-0", "0 0 440 244", "Ô tô khối lượng 1 200 kg chạy lên dốc dài 1 km, cao 50 m, tốc độ 36 km/h", body, "Hình minh hoạ, không đúng tỉ lệ.")
def mang_fig():
    body = '<path d="M30,30 Q 40,160 120,160" fill="none" stroke="currentColor" stroke-width="3"/>'
    body += seg(120, 160, 300, 160, "currentColor", 3) + '<path d="M300,160 Q 380,160 392,60" fill="none" stroke="currentColor" stroke-width="3"/>'
    body += "".join(seg(x, 160, x - 6, 168, "currentColor", 1) for x in range(126, 300, 12))
    body += dot(32, 30, 6, GRN) + T(46, 26, "m = 500 g, thả không vận tốc đầu", "currentColor", 12)
    body += seg(54, 44, 54, 160, "currentColor", 1, "3 3") + dim("", "o", 62, 44, 62, 160, "h = 5 m", 70, 106)
    body += T(120, 182, "M", "currentColor", 13, "middle", "700") + T(300, 182, "N", "currentColor", 13, "middle", "700")
    body += T(210, 196, "MN = 10 m, lực ma sát 1 N", "currentColor", 12, "middle") + T(70, 212, "máng (1) nhẵn", "currentColor", 11, "middle") + T(350, 212, "máng (2) nhẵn", "currentColor", 11, "middle")
    return fig("hsg-11-0", "0 0 420 222", "Hai máng cong nhẵn nối bằng đoạn nằm ngang MN có ma sát", body, "Hình minh hoạ, không đúng tỉ lệ.")
def bom_fig():
    body = '<rect x="20" y="140" width="110" height="50" fill="#d9e3ee" stroke="none" opacity=".6"/><path d="M20,120 L20,190 L130,190 L130,120" fill="none" stroke="currentColor" stroke-width="2.4"/>'
    body += seg(20, 140, 130, 140, "currentColor", 1.4) + T(75, 208, "giếng", "currentColor", 12, "middle")
    body += '<rect x="160" y="108" width="44" height="30" fill="none" stroke="currentColor" stroke-width="2.2"/>' + T(182, 128, "bơm", "currentColor", 12, "middle", "700")
    body += seg(75, 140, 75, 123, "currentColor", 2) + seg(75, 123, 160, 123, "currentColor", 2) + seg(204, 123, 250, 123, "currentColor", 2) + seg(250, 123, 250, 40, "currentColor", 2) + seg(250, 40, 290, 40, "currentColor", 2)
    body += '<rect x="290" y="50" width="100" height="40" fill="#d9e3ee" stroke="none" opacity=".6"/><path d="M290,30 L290,90 L390,90 L390,30" fill="none" stroke="currentColor" stroke-width="2.4"/>' + T(340, 108, "bể 30 m³", "currentColor", 12, "middle")
    body += arrow("", "r", 290, 40, 306, 54, 2.2) + T(312, 40, "v = 4 m/s", RED, 11, "start", "700")
    body += seg(30, 40, 290, 40, "currentColor", 1, "3 3") + dim("", "o", 36, 40, 36, 140, "h = 10 m", 44, 94)
    body += T(150, 168, "𝒫 = 1,5 kW, H = 60 %", "currentColor", 12, "start", "700")
    return fig("hsg-12-0", "0 0 420 218", "Máy bơm hút nước từ giếng lên bể cao hơn mặt nước giếng 10 mét", body, "Hình minh hoạ, không đúng tỉ lệ.")

# ---------- đề ----------
PROB = [
 '<p>Ô tô khối lượng $1\\,200\\ \\text{kg}$ chuyển động đều lên một dốc dài $1\\ \\text{km}$, cao $50\\ \\text{m}$ với tốc độ $36\\ \\text{km/h}$. Khi lên dốc, lực cản chuyển động (ma sát và không khí) không đổi và bằng $400\\ \\text{N}$. Lấy $g=10\\ \\text{N/kg}$.</p>'
 '<ol type="a"><li>Tính lực kéo của động cơ và công suất của động cơ.</li><li>Động cơ có hiệu suất $25\\ \\%$ ; xăng toả $4{,}6\\cdot10^{7}\\ \\text{J/kg}$ khi cháy. Tính lượng xăng tiêu thụ khi xe lên hết dốc.</li><li>Khi xuống dốc này, tài xế tắt máy và đạp phanh nhẹ để xe chạy đều. Tổng lực cản (ma sát, không khí và phanh) lúc đó bằng bao nhiêu?</li></ol>',
 '<p>Vật nhỏ khối lượng $500\\ \\text{g}$ được thả không vận tốc đầu từ độ cao $h=5\\ \\text{m}$ trên máng cong nhẵn (1). Chân máng nối với đoạn đường nằm ngang $MN$ dài $10\\ \\text{m}$ ; trên $MN$ lực ma sát không đổi $1\\ \\text{N}$. Đầu $N$ nối với máng cong nhẵn (2). Lấy $g=10\\ \\text{N/kg}$, bỏ qua sức cản không khí.</p>'
 '<ol type="a"><li>Tính tốc độ của vật khi tới $M$.</li><li>Vật lên tới độ cao lớn nhất bao nhiêu trên máng (2)?</li><li>Cuối cùng vật dừng lại ở đâu? Tính tổng quãng đường vật đã đi trên đoạn $MN$.</li></ol>',
 '<p>Một máy bơm có công suất tiêu thụ điện $1{,}5\\ \\text{kW}$, hiệu suất $60\\ \\%$, hút nước từ giếng lên bể đặt cao hơn mặt nước giếng $10\\ \\text{m}$. Khối lượng riêng của nước $1\\,000\\ \\text{kg/m}^3$, $g=10\\ \\text{N/kg}$.</p>'
 '<ol type="a"><li>Bỏ qua động năng của nước. Mỗi giây máy bơm được bao nhiêu lít nước?</li><li>Thực tế nước ra khỏi vòi (ở miệng bể) với tốc độ $4\\ \\text{m/s}$. Tính lại lượng nước bơm được mỗi giây.</li><li>Với kết quả câu b, bơm đầy bể $30\\ \\text{m}^3$ mất bao lâu? Máy tiêu thụ bao nhiêu kWh điện?</li></ol>',
]
FIGS = [slope_fig, mang_fig, bom_fig]

# ---------- bảng phân tích ----------
ANA = [[
 ('"chuyển động đều lên một dốc dài $1$ km, cao $50$ m"', '$l=1000$ m ; $h=50$ m', '⚠ Chuyển động đều → hợp lực bằng $0$ ; dọc dốc chỉ có thành phần trọng lực $P\\dfrac{h}{l}$ (không phải cả $P$) cần cân bằng'),
 ('"khối lượng $1\\,200$ kg … Lấy $g=10$"', '$m=1200$ kg ; $P=10m$', 'Trọng lượng $P=10m$'),
 ('"tốc độ $36$ km/h"', '$v=36$ km/h', '⚠ Đổi ra m/s trước khi dùng $\\mathcal{P}=Fv$'),
 ('"lực cản … không đổi $400$ N"', '$F_c=400$ N', 'Lực cản cùng chiều với thành phần trọng lực (cùng ngược chiều chuyển động lên dốc)'),
 ('"Tính lực kéo … và công suất"', 'Cần tìm $F_k$ ; $\\mathcal{P}$', '$F_k=P\\dfrac{h}{l}+F_c$ ; $\\mathcal{P}=F_k v$'),
 ('"hiệu suất $25\\ \\%$ ; xăng toả $4{,}6\\cdot10^{7}$ J/kg"', '$H=0{,}25$ ; $q=4{,}6\\cdot10^{7}$ J/kg', '⚠ $H=\\dfrac{A}{Q}$ nên $Q=\\dfrac{A}{H}$ (lớn hơn $A$) ; $m=\\dfrac{Q}{q}$ ; $A=F_k l$'),
 ('"xuống dốc, tắt máy … chạy đều"', 'Lực kéo $=0$ ; thêm lực phanh', '⚠ Chạy đều → tổng lực cản cân bằng thành phần trọng lực dọc dốc $P\\dfrac{h}{l}$'),
],[
 ('"máng cong nhẵn (1) … thả từ $h=5$ m"', '$h=5$ m ; $m=0{,}5$ kg (đổi từ $500$ g)', '⚠ Máng nhẵn → cơ năng bảo toàn : $mgh=\\dfrac12 mv^2$'),
 ('"đoạn nằm ngang $MN$ dài $10$ m ; ma sát $1$ N"', '$MN=10$ m ; $F_{ms}=1$ N', '⚠ Chỉ trên $MN$ cơ năng giảm đúng bằng công ma sát : $\\Delta W=F_{ms}\\,s$'),
 ('"Đầu $N$ nối với máng cong nhẵn (2)"', 'Máng (2) không ma sát', 'Cơ năng tại $N$ biến hết thành thế năng ở độ cao cực đại : $mgh_2=W_N$'),
 ('"Tính tốc độ khi tới $M$ ; độ cao lớn nhất trên máng (2)"', 'Cần tìm $v_M$ ; $h_2$', '$v_M=\\sqrt{2gh}$ ; $h_2=\\dfrac{W_N}{mg}$'),
 ('"Cuối cùng vật dừng lại ở đâu ? Tổng quãng đường trên $MN$"', 'Cần tìm vị trí dừng ; $s_{\\text{tổng}}$', '⚠ Dừng hẳn khi mất hết cơ năng : $F_{ms}\\,s_{\\text{tổng}}=W_0$ ; vật có thể qua $MN$ nhiều lần'),
],[
 ('"công suất tiêu thụ điện $1{,}5$ kW, hiệu suất $60\\ \\%$"', '$\\mathcal{P}=1500$ W ; $H=0{,}6$', '⚠ Công suất có ích $\\mathcal{P}_{\\text{ích}}=H\\mathcal{P}$ ; điện năng tiêu thụ tính theo $\\mathcal{P}$ toàn phần'),
 ('"lên bể cao hơn mặt nước giếng $10$ m"', '$h=10$ m', 'Thế năng $1$ kg nước tăng $gh$'),
 ('"Bỏ qua động năng … mỗi giây được bao nhiêu lít"', 'Cần tìm lưu lượng', '$\\mathcal{P}_{\\text{ích}}=m\\,g\\,h$ ; $1$ kg nước $=1$ lít'),
 ('"nước ra khỏi vòi với tốc độ $4$ m/s"', '$v=4$ m/s', '⚠ Mở rộng ngoài chuẩn KHTN 9 : động năng dòng nước ; $1$ kg cần $gh+\\dfrac12 v^2$'),
 ('"bơm đầy bể $30$ m³ … bao nhiêu kWh"', '$V=30$ m³ ; cần $t$ và $A$', '$t=\\dfrac{V}{\\text{lưu lượng}}$ ; $A=\\mathcal{P}\\,t$ (đổi $t$ ra giờ)'),
]]

# ---------- lời giải ----------
SOLS = [
 sol(["<strong>Công thức:</strong> chuyển động đều lên dốc → $F_k=P\\dfrac{h}{l}+F_c$ ; $\\mathcal{P}=F_k v$ ; $H=\\dfrac{A}{Q}$ ; $m=\\dfrac{Q}{q}$.",
      "⚠ <strong>Điều kiện:</strong> đổi tốc độ ra m/s ; hiệu suất nhỏ hơn $1$ nên nhiệt toả ra lớn hơn công có ích.",
      "<strong>Xuống dốc đều:</strong> tổng lực cản cân bằng thành phần trọng lực dọc dốc."],
  [("Đổi tốc độ", [P("Quãng đường tính bằng mét nên đổi tốc độ ra m/s :"), M("v=\\dfrac{36}{3{,}6}"), A("v=10\\ \\text{m/s}")]),
   ("Thành phần trọng lực dọc dốc", [P("Trọng lượng của xe :"), M("P=10m=10\\cdot1200=12\\,000\\ \\text{N}"), P("Thành phần dọc dốc :"), M("P\\dfrac{h}{l}=12\\,000\\cdot\\dfrac{50}{1000}"), A("P\\dfrac{h}{l}=600\\ \\text{N}")]),
   ("Lực kéo của động cơ", [P("Chuyển động đều : lực kéo cân bằng thành phần trọng lực và lực cản :"), M("F_k=P\\dfrac{h}{l}+F_c=600+400"), A("F_k=1000\\ \\text{N}")]),
   ("Công suất của động cơ", [M("\\mathcal{P}=F_k v=1000\\cdot10"), A("\\mathcal{P}=10\\,000\\ \\text{W}=10\\ \\text{kW}")]),
   ("Công động cơ sinh ra", [P("Lên hết dốc, động cơ đi quãng đường $l$ :"), M("A=F_k l=1000\\cdot1000"), A("A=1\\,000\\,000\\ \\text{J}=1\\ \\text{MJ}")]),
   ("Nhiệt lượng xăng toả ra", [P("Từ $H=\\dfrac{A}{Q}$ :"), M("Q=\\dfrac{A}{H}=\\dfrac{1\\,000\\,000}{0{,}25}"), A("Q=4\\,000\\,000\\ \\text{J}=4\\ \\text{MJ}")]),
   ("Lượng xăng tiêu thụ", [M("m=\\dfrac{Q}{q}=\\dfrac{4\\,000\\,000}{4{,}6\\cdot10^{7}}"), A("m\\approx0{,}087\\ \\text{kg}\\approx87\\ \\text{g}")]),
   ("Xuống dốc, tắt máy, chạy đều", [P("Không còn lực kéo. Chạy đều nên tổng lực cản cân bằng thành phần trọng lực dọc dốc :"), M("F_{\\text{cản}}=P\\dfrac{h}{l}"), A("F_{\\text{cản}}=600\\ \\text{N}"), P("Trong đó ma sát và không khí vẫn khoảng $400\\ \\text{N}$ nên lực phanh khoảng $200\\ \\text{N}$.")])],
  ["a) $F_k=1000\\ \\text{N}$ ; $\\mathcal{P}=10\\ \\text{kW}$", "b) $m\\approx0{,}087\\ \\text{kg}$ (khoảng $87\\ \\text{g}$)", "c) $600\\ \\text{N}$"],
  "Nhận dạng: thấy <strong>xe lên dốc đều, có lực cản</strong> → $F_k=P\\dfrac{h}{l}+F_c$, công suất $=Fv$ (đổi $v$ ra m/s) ; hiệu suất thì $Q=\\dfrac{A}{H}$."),
 sol(["<strong>Cơ năng:</strong> $W=mgh$ (thế năng, mốc ở mặt $MN$) hoặc $W=\\dfrac12mv^2$ (ở mặt $MN$).",
      "⚠ <strong>Điều kiện:</strong> máng nhẵn thì cơ năng bảo toàn ; chỉ đoạn có ma sát làm cơ năng giảm : $\\Delta W=F_{ms}\\,s$.",
      "<strong>Dừng hẳn:</strong> $F_{ms}\\,s_{\\text{tổng}}=W_0$ ; vật có thể qua $MN$ nhiều lần."],
  [("Cơ năng ban đầu", [P("Đổi $m=500\\ \\text{g}=0{,}5\\ \\text{kg}$. Chọn mốc ở mặt $MN$ :"), M("W_0=mgh=0{,}5\\cdot10\\cdot5"), A("W_0=25\\ \\text{J}")]),
   ("Tốc độ tại $M$", [P("Máng (1) nhẵn nên cơ năng bảo toàn, thế năng biến hết thành động năng :"), M("\\dfrac12mv^2=W_0"), M("v=\\sqrt{\\dfrac{2W_0}{m}}=\\sqrt{\\dfrac{2\\cdot25}{0{,}5}}"), A("v=10\\ \\text{m/s}")]),
   ("Cơ năng tại $N$", [P("Qua $MN$ lần 1 vật mất công ma sát :"), M("A_{ms}=F_{ms}\\cdot MN=1\\cdot10=10\\ \\text{J}"), M("W_N=W_0-A_{ms}=25-10"), A("W_N=15\\ \\text{J}")]),
   ("Độ cao lớn nhất trên máng (2)", [P("Máng (2) nhẵn : cơ năng tại $N$ biến hết thành thế năng ở đỉnh :"), M("mgh_2=W_N"), M("h_2=\\dfrac{W_N}{mg}=\\dfrac{15}{0{,}5\\cdot10}"), A("h_2=3\\ \\text{m}")]),
   ("Tổng quãng đường trên $MN$", [P("Dừng hẳn thì toàn bộ cơ năng ban đầu đã biến thành công ma sát :"), M("F_{ms}\\,s_{\\text{tổng}}=W_0"), M("s_{\\text{tổng}}=\\dfrac{W_0}{F_{ms}}=\\dfrac{25}{1}"), A("s_{\\text{tổng}}=25\\ \\text{m}")]),
   ("Vị trí dừng", [P("Chia cho chiều dài $MN$ :"), M("\\dfrac{s_{\\text{tổng}}}{MN}=\\dfrac{25}{10}=2{,}5"), P("Vật đi hết $MN$ hai lần (từ $M$ tới $N$ rồi về $M$), còn dư $5\\ \\text{m}$ kể từ $M$ về phía $N$ :"), A("\\text{dừng cách }M\\text{ là }5\\ \\text{m (giữa }MN\\text{)}"), P("Kiểm tra : $10+10+5=25\\ \\text{m}$ ✓. Lần về $M$ thứ hai vật còn $5\\ \\text{J}$ nên lên máng (1) cao $1\\ \\text{m}$ rồi trượt lại.")])],
  ["a) $v=10\\ \\text{m/s}$", "b) $h_2=3\\ \\text{m}$", "c) Dừng cách $M$ là $5\\ \\text{m}$ (giữa $MN$) ; tổng quãng đường trên $MN$ là $25\\ \\text{m}$"],
  "Nhận dạng: thấy <strong>máng nhẵn nối đoạn có ma sát</strong> → cơ năng chỉ mất trên đoạn ma sát : $\\Delta W=F_{ms}\\,s$ ; hỏi \"dừng ở đâu\" thì lấy $\\dfrac{W_0}{F_{ms}}$ rồi chia theo chiều dài đoạn."),
 sol(["<strong>Hiệu suất:</strong> $\\mathcal{P}_{\\text{ích}}=H\\,\\mathcal{P}$ ; điện năng tiêu thụ $A=\\mathcal{P}\\,t$ (toàn phần).",
      "<strong>Mỗi kg nước</strong> lên cao $h$ cần thế năng $gh$ ; nếu ra vòi với tốc độ $v$ thì thêm động năng $\\dfrac12v^2$.",
      "⚠ <strong>Điều kiện:</strong> $1\\ \\text{kg}$ nước $=1\\ \\text{lít}$ ; kWh cần $t$ tính bằng giờ."],
  [("Công suất có ích", [M("\\mathcal{P}_{\\text{ích}}=H\\,\\mathcal{P}=0{,}6\\cdot1500"), A("\\mathcal{P}_{\\text{ích}}=900\\ \\text{W}")]),
   ("Lưu lượng khi bỏ qua động năng (câu a)", [P("Mỗi giây công có ích chỉ làm tăng thế năng của $m$ kilôgam nước :"), M("\\mathcal{P}_{\\text{ích}}=m\\,g\\,h"), M("m=\\dfrac{900}{10\\cdot10}=9\\ \\text{kg}"), A("9\\ \\text{kg nước}=9\\ \\text{lít mỗi giây}")]),
   ("Năng lượng cần cho 1 kg nước (câu b)", [P("Mỗi kilôgam nước vừa được nâng lên vừa ra vòi với tốc độ $4\\ \\text{m/s}$ :"), M("e=gh+\\dfrac12v^2=10\\cdot10+\\dfrac12\\cdot4^2"), A("e=108\\ \\text{J/kg}")]),
   ("Lưu lượng thực tế (câu b)", [P("Số kilôgam nước mỗi giây $=$ năng lượng có ích mỗi giây chia năng lượng cần cho $1$ kg :"), M("m=\\dfrac{\\mathcal{P}_{\\text{ích}}}{e}=\\dfrac{900}{108}"), A("m\\approx8{,}33\\ \\text{kg}\\approx8{,}33\\ \\text{lít mỗi giây}")]),
   ("Thời gian bơm đầy bể (câu c)", [P("Đổi $30\\ \\text{m}^3=30\\,000$ lít, chia cho lưu lượng câu b :"), M("t=\\dfrac{30\\,000}{8{,}33}"), A("t\\approx3600\\ \\text{s}=1\\ \\text{h}")]),
   ("Điện năng tiêu thụ (câu c)", [P("Điện năng tính theo công suất toàn phần, thời gian đổi ra giờ :"), M("A=\\mathcal{P}\\,t=1{,}5\\ \\text{kW}\\cdot1\\ \\text{h}"), A("A=1{,}5\\ \\text{kWh}")])],
  ["a) $9$ lít/s", "b) $\\approx8{,}33$ lít/s", "c) $t=3600\\ \\text{s}=1\\ \\text{h}$ ; điện năng $1{,}5\\ \\text{kWh}$"],
  "Nhận dạng: thấy <strong>máy bơm, hiệu suất, mỗi giây</strong> → viết năng lượng có ích trong $1\\ \\text{s}$ $=\\left(gh+\\dfrac12v^2\\right)\\times$ khối lượng nước mỗi giây."),
]

# ---------- bước tự giải ----------
B = lambda **k: buoc(**k)
STEPS = [
 dict(nhan_dang="Thấy <b>xe lên dốc đều, có lực cản</b> → nghĩ tới <b>F<sub>kéo</sub> = P·h/l + F<sub>cản</sub></b>, công suất = F·v", cap_do=3, fading="giau_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  B(tieu_de="Đổi tốc độ", hoi="Tốc độ 36 km/h bằng bao nhiêu mét trên giây?", dap_so=10, sai_so=0.1, don_vi="m/s",
    loi="Nhân với $3{,}6$ thay vì chia, hoặc để nguyên km/h khi quãng đường tính bằng mét."),
  B(tieu_de="Thành phần trọng lực dọc dốc", hoi="Thành phần của trọng lực dọc theo dốc (P·h/l) bằng bao nhiêu niutơn?", dap_so=600, sai_so=5, don_vi="N",
    loi="Lấy cả trọng lượng $P$ làm lực cần thắng dọc dốc, hoặc lấy $P\\cdot\\dfrac{l}{h}$ thay vì $P\\cdot\\dfrac{h}{l}$.",
    ke=[("Tính thành phần trọng lực dọc dốc $P\\dfrac{h}{l}$ (mặt nghiêng giúp lợi về lực)", True),
        ("Lấy cả trọng lượng $P$ làm lực cản dọc dốc", "Xe không bị nâng thẳng đứng : dọc theo dốc chỉ có thành phần $P\\dfrac{h}{l}$ cần cân bằng."),
        ("Bỏ qua trọng lực vì xe chuyển động đều", "Chuyển động đều chỉ nói hợp lực bằng $0$ ; lực kéo vẫn phải cân bằng thành phần trọng lực, không bỏ được.")]),
  B(tieu_de="Lực kéo của động cơ", hoi="Lực kéo của động cơ khi lên dốc đều bằng bao nhiêu niutơn?", dap_so=1000, sai_so=10, don_vi="N",
    loi="Cho $F_k=F_c$ (quên thành phần trọng lực) hoặc trừ lực cản thay vì cộng.",
    ke=[("Cân bằng lực dọc dốc : $F_k=P\\dfrac{h}{l}+F_c$", True),
        ("$F_k=P\\dfrac{h}{l}-F_c$", "Lực cản ngược chiều chuyển động giống thành phần trọng lực nên lực kéo phải thắng cả hai, không phải trừ."),
        ("$F_k=F_c$ vì chạy đều", "Chạy đều trên dốc còn thành phần trọng lực kéo xe xuống ; lực kéo phải cân bằng cả nó nữa.")]),
  B(tieu_de="Công suất của động cơ", hoi="Công suất của động cơ bằng bao nhiêu kilôoát?", dap_so=10, sai_so=0.1, don_vi="kW",
    loi="Dùng $v=36$ thẳng vào công thức (được số lớn gấp $3{,}6$ lần), hoặc quên đổi W sang kW.",
    ke=[("$\\mathcal{P}=F_k v$ với $v$ tính bằng m/s", True),
        ("$\\mathcal{P}=F_k v$ với $v$ giữ nguyên km/h", "Đơn vị lệch nhau : phải đổi $v$ ra m/s mới ra oát."),
        ("$\\mathcal{P}=F_k\\,l$", "$F_k\\,l$ là công của lực kéo, không phải công suất ; công suất là công chia thời gian hay $F\\,v$.")]),
  B(tieu_de="Công động cơ sinh ra", hoi="Công động cơ sinh ra khi lên hết dốc bằng bao nhiêu mêgajun (MJ)?", dap_so=1, sai_so=0.02, don_vi="MJ",
    loi="Tính công nâng $P\\cdot h$ (quên công thắng lực cản) hoặc lấy $\\mathcal{P}\\cdot l$.",
    ke=[("$A=F_k\\,l$ (lực kéo nhân quãng đường dọc dốc)", True),
        ("$A=P\\,h$", "$P\\,h$ chỉ là công nâng xe lên ; động cơ còn phải thắng lực cản dọc suốt quãng đường nên công lớn hơn."),
        ("$A=\\mathcal{P}\\,l$", "Công suất nhân quãng đường không ra công ; công $=$ lực $\\times$ quãng đường hoặc công suất $\\times$ thời gian.")]),
  B(tieu_de="Nhiệt lượng xăng toả ra", hoi="Nhiệt lượng xăng phải toả ra bằng bao nhiêu mêgajun (MJ)?", dap_so=4, sai_so=0.05, don_vi="MJ",
    loi="Nhân công với hiệu suất ($Q=A\\cdot H$) nên ra nhỏ hơn công có ích.",
    ke=[("$Q=\\dfrac{A}{H}$", True),
        ("$Q=A\\cdot H$", "Hiệu suất nhỏ hơn $1$ nên nhiệt toả ra phải lớn hơn công có ích ; nhân với $H$ sẽ ra nhỏ hơn."),
        ("$Q=A$", "Động cơ có hiệu suất nên chỉ một phần nhiệt của xăng thành công ; không thể lấy $Q$ bằng $A$.")]),
  B(tieu_de="Lượng xăng tiêu thụ", hoi="Lượng xăng tiêu thụ bằng bao nhiêu gam?", dap_so=87, sai_so=1, don_vi="g",
    loi="Quên đổi kg sang gam, hoặc dùng công $A$ thay vì nhiệt lượng $Q$ để chia cho $q$.",
    ke=[("$m=\\dfrac{Q}{q}$", True),
        ("$m=\\dfrac{A}{q}$", "$q$ là nhiệt toả ra khi đốt $1$ kg xăng nên phải chia nhiệt lượng $Q$, không phải công có ích $A$."),
        ("$m=Q\\cdot q$", "Đơn vị thành $\\text{J}\\cdot\\text{J/kg}$, không ra kilôgam.")]),
  B(tieu_de="Xuống dốc, tắt máy, chạy đều", hoi="Tổng lực cản (kể cả phanh) khi xuống dốc đều bằng bao nhiêu niutơn?", dap_so=600, sai_so=5, don_vi="N",
    loi="Cho tổng lực cản vẫn bằng lực cản cũ, quên rằng thành phần trọng lực dọc dốc đang kéo xe xuống.",
    ke=[("Chạy đều : tổng lực cản cân bằng thành phần trọng lực dọc dốc", True),
        ("Tổng lực cản bằng lực cản cũ vì ma sát và không khí không đổi", "Còn lực phanh nữa, và xe chạy đều nên tổng lực cản phải cân bằng thành phần trọng lực, không chỉ ma sát và không khí."),
        ("Tổng lực cản bằng cả trọng lượng $P$", "Chỉ thành phần $P\\dfrac{h}{l}$ nằm dọc theo dốc mới cần cân bằng.")]),
 ]),
 dict(nhan_dang="Thấy <b>máng nhẵn nối đoạn có ma sát</b> → nghĩ tới <b>ΔW = F<sub>ms</sub>·s</b>; hỏi dừng ở đâu thì lấy W₀/F<sub>ms</sub>", cap_do=3, fading="giau_het", go_roi={"buoc_hay_sai": 5}, buoc=[
  B(tieu_de="Cơ năng ban đầu", hoi="Cơ năng ban đầu của vật (mốc ở mặt MN) bằng bao nhiêu jun?", dap_so=25, sai_so=0.5, don_vi="J",
    loi="Thế khối lượng $500$ (gam) vào công thức thay vì $0{,}5$ kg."),
  B(tieu_de="Tốc độ tại M", hoi="Tốc độ của vật khi tới M bằng bao nhiêu mét trên giây?", dap_so=10, sai_so=0.1, don_vi="m/s",
    loi="Trừ công ma sát của $MN$ trước khi tới $M$, hoặc quên căn bậc hai ($v=2gh$).",
    ke=[("Máng (1) nhẵn nên cơ năng bảo toàn : $\\dfrac12mv^2=W_0$", True),
        ("Trừ công ma sát của $MN$ trước khi tính", "Tới $M$ vật chưa vào đoạn $MN$ nên ma sát chưa sinh công."),
        ("Dùng $v=g\\,t$ với gia tốc không đổi", "Máng cong nên gia tốc dọc máng thay đổi và thời gian chưa biết ; phải dùng bảo toàn cơ năng.")]),
  B(tieu_de="Cơ năng tại N", hoi="Cơ năng của vật khi tới N (sau lần qua MN đầu tiên) bằng bao nhiêu jun?", dap_so=15, sai_so=0.5, don_vi="J",
    loi="Cho cơ năng không đổi (quên ma sát trên $MN$), hoặc lấy chính công ma sát làm cơ năng còn lại.",
    ke=[("$W_N=W_0-F_{ms}\\cdot MN$", True),
        ("$W_N=W_0$ vì hai máng đều nhẵn", "Giữa hai máng là đoạn $MN$ có ma sát nên cơ năng giảm."),
        ("$W_N=F_{ms}\\cdot MN$", "Đó là phần cơ năng đã mất, không phải phần còn lại.")]),
  B(tieu_de="Độ cao lớn nhất trên máng (2)", hoi="Vật lên tới độ cao lớn nhất bao nhiêu mét trên máng (2)?", dap_so=3, sai_so=0.05, don_vi="m",
    loi="Dùng cơ năng ban đầu $W_0$ (ra $5\\ \\text{m}$) hoặc dùng tốc độ tại $M$ cho điểm $N$.",
    ke=[("Máng (2) nhẵn : $mgh_2=W_N$", True),
        ("$mgh_2=W_0$", "Vật đã mất công ma sát trên $MN$ nên chỉ còn $W_N$ khi tới chân máng (2)."),
        ("$\\dfrac12mv_M^2=mgh_2$ với $v_M$ là tốc độ tại $M$", "Tốc độ tại $N$ đã giảm do ma sát, không bằng tốc độ tại $M$.")]),
  B(tieu_de="Tổng quãng đường trên MN", hoi="Tổng quãng đường vật đi trên đoạn MN cho tới khi dừng hẳn bằng bao nhiêu mét?", dap_so=25, sai_so=0.5, don_vi="m",
    loi="Cho rằng vật chỉ qua $MN$ một lần ($s=MN$), hoặc dùng $W_N$ thay vì $W_0$.",
    ke=[("Toàn bộ cơ năng ban đầu thành công ma sát : $F_{ms}\\,s=W_0$", True),
        ("$F_{ms}\\,s=W_N$", "$W_N$ chỉ là cơ năng sau lần qua đầu tiên ; vật còn quay lại, phải mất hết $W_0$ mới dừng."),
        ("$s=MN$ vì vật qua $MN$ một lần", "Hai máng nhẵn nên vật quay lại và qua $MN$ nhiều lần.")]),
  B(tieu_de="Vị trí dừng", hoi="Vật dừng lại cách M bao nhiêu mét?", dap_so=5, sai_so=0.1, don_vi="m",
    loi="Kết luận dừng cách $M$ cả $s_{\\text{tổng}}$ (dài hơn $MN$), hoặc bỏ phần dư rồi cho dừng ở $M$ hay $N$.",
    ke=[("Chia $s_{\\text{tổng}}$ cho $MN$ : số lượt đi hết $MN$ cộng phần dư", True),
        ("Lấy luôn $s_{\\text{tổng}}$ làm khoảng cách tới $M$", "$s_{\\text{tổng}}$ dài hơn $MN$ vì vật đã quay lại nhiều lần ; vị trí phải tính từ phần dư."),
        ("Bỏ phần dư, kết luận dừng đúng ở $M$ hoặc $N$", "Phần dư khác $0$ nên vật dừng ở giữa $MN$, không phải ở hai đầu.")]),
 ]),
 dict(nhan_dang="Thấy <b>máy bơm, hiệu suất, mỗi giây</b> → viết <b>năng lượng có ích trong 1 s</b> = (gh + ½v²) × m mỗi giây", cap_do=3, fading="giau_het", go_roi={"buoc_hay_sai": 3}, buoc=[
  B(tieu_de="Công suất có ích", hoi="Công suất có ích của máy bơm bằng bao nhiêu oát?", dap_so=900, sai_so=5, don_vi="W",
    loi="Lấy luôn $1500\\ \\text{W}$ làm công suất có ích, hoặc nhân hiệu suất với $60$ thay vì $0{,}6$."),
  B(tieu_de="Lưu lượng khi bỏ qua động năng", hoi="Bỏ qua động năng, mỗi giây máy bơm được bao nhiêu lít nước?", dap_so=9, sai_so=0.1, don_vi="lít",
    loi="Dùng công suất toàn phần ($1500\\ \\text{W}$) trong $\\mathcal{P}=mgh$, hoặc đổi sang lít bằng cách nhân $1000$.",
    ke=[("Công có ích mỗi giây làm tăng thế năng : $\\mathcal{P}_{\\text{ích}}=m\\,g\\,h$", True),
        ("Dùng công suất điện : $\\mathcal{P}=m\\,g\\,h$", "Công suất điện là phần máy tiêu thụ ; chỉ phần có ích (nhân hiệu suất) mới nâng nước."),
        ("Tính $m$ rồi nhân $1000$ để ra lít", "Khối lượng riêng $1000\\ \\text{kg/m}^3$ tức $1\\ \\text{kg}=1\\ \\text{lít}$ ; nhân thêm $1000$ là nhầm với đổi sang m³ hay cm³.")]),
  B(tieu_de="Năng lượng cần cho 1 kg nước", hoi="Mỗi kilôgam nước ra khỏi vòi cần được cấp bao nhiêu jun (thế năng cộng động năng)?", dap_so=108, sai_so=1, don_vi="J",
    loi="Lấy động năng bằng $v$ hoặc $\\dfrac12v$ thay vì $\\dfrac12v^2$, hoặc bỏ luôn động năng.",
    ke=[("Cộng thế năng $gh$ với động năng $\\dfrac12v^2$ của $1$ kg nước", True),
        ("Cộng $gh$ với $v$", "Động năng của $1$ kg là $\\dfrac12v^2$ (có bình phương và hệ số $\\dfrac12$), không phải $v$."),
        ("Chỉ có thế năng, động năng bằng $0$ vì nước dừng ở bể", "Đề cho nước ra khỏi vòi với tốc độ xác định nên phần năng lượng này phải tính.")]),
  B(tieu_de="Lưu lượng thực tế", hoi="Kể cả động năng, mỗi giây máy bơm được bao nhiêu lít nước?", dap_so=8.33, sai_so=0.05, don_vi="lít",
    loi="Giữ nguyên kết quả câu a, hoặc nhân thay vì chia ($m=\\mathcal{P}_{\\text{ích}}\\cdot e$).",
    ke=[("$m=\\dfrac{\\mathcal{P}_{\\text{ích}}}{e}$ (năng lượng có ích mỗi giây chia năng lượng mỗi kg)", True),
        ("Giữ kết quả câu a vì công suất không đổi", "Công suất không đổi nhưng mỗi kg nay cần nhiều năng lượng hơn nên số kg mỗi giây phải giảm."),
        ("$m=\\mathcal{P}_{\\text{ích}}\\cdot e$", "Số kilôgam mỗi giây là năng lượng có ích mỗi giây chia năng lượng mỗi kilôgam, không phải nhân.")]),
  B(tieu_de="Thời gian bơm đầy bể", hoi="Bơm đầy bể 30 m³ mất bao nhiêu giây (dùng lưu lượng câu b)?", dap_so=3600, sai_so=20, don_vi="s",
    loi="Chia thẳng $30$ cho lưu lượng lít/s (quên đổi m³ sang lít) hoặc dùng lưu lượng câu a.",
    ke=[("Đổi thể tích ra lít rồi chia cho lưu lượng câu b", True),
        ("Chia cho lưu lượng câu a", "Đề bảo dùng kết quả câu b (có tính động năng) ; lưu lượng câu a lớn hơn thực tế."),
        ("Chia thẳng thể tích tính bằng m³ cho lưu lượng tính bằng lít/s", "Đơn vị lệch nhau : $1\\ \\text{m}^3=1000$ lít.")]),
  B(tieu_de="Điện năng tiêu thụ", hoi="Máy tiêu thụ bao nhiêu kilôoát giờ (kWh) điện?", dap_so=1.5, sai_so=0.05, don_vi="kWh",
    loi="Tính theo công suất có ích, hoặc nhân kW với số giây rồi ghi là kWh.",
    ke=[("$A=\\mathcal{P}\\,t$ với công suất điện của máy, $t$ đổi ra giờ", True),
        ("$A=\\mathcal{P}_{\\text{ích}}\\,t$", "Điện năng máy tiêu thụ tính theo công suất tiêu thụ (toàn phần), không phải phần có ích."),
        ("Nhân công suất (kW) với số giây rồi ghi là kWh", "kWh cần thời gian tính bằng giờ ; kW nhân giây không phải kWh.")]),
 ]),
]

LABELS = ["Bài 10 · Vận dụng · Ô tô lên dốc — lực kéo, công suất, nhiên liệu · Thứ Năm 15/10",
          "Bài 11 · Vận dụng cao · Hai máng nhẵn nối bằng đoạn đường có ma sát · Thứ Sáu 16/10",
          "Bài 12 · Vận dụng cao · Máy bơm nước — công suất, hiệu suất, động năng dòng nước · Thứ Sáu 16/10"]
TOPICS = ["Công suất của động cơ, máy kéo", "Biến thiên cơ năng khi có ma sát", "Tính hiệu suất của máy và động cơ"]
dang = []
for i in range(3):
    n_step = SOLS[i].count('class="bt-step"')
    assert n_step == len(STEPS[i]["buoc"]), (i, n_step, len(STEPS[i]["buoc"]))
    d = dict(label=LABELS[i], topic=TOPICS[i], form="bai_tap", problem_html=PROB[i] + FIGS[i](), analysis_html=tbl(ANA[i]), solution_html=SOLS[i])
    d.update(STEPS[i]); dang.append(d)
out = {"lesson_id": 167, "lesson_title": "Bài tập tuần này: 12 bài tự luận Cơ học", "review": {"checked": True, "notes": "tạm, chờ kiểm chéo"}, "dang_bai": dang}
json.dump(out, open(os.path.join(HERE, "part-D.json"), "w"), ensure_ascii=False, indent=1)
print("ok", len(dang))
