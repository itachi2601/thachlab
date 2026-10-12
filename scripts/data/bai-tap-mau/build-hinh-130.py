"""Bài tập mẫu bài 130 — Bài 3. Cơ năng (KHTN 9). Dựng 4 dạng + hình + lời giải + buoc[] → 130.json.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-130.py   (idempotent: ghi lại toàn bộ 130.json, review.checked=false)
Danh sách dạng: scripts/data/bai-tap-mau/130.dang.md. Mọi số liệu tính ở đầu file, có assert.
Quy ước KHTN 9: W_t = 10mh, W_đ = ½mv² (g ≈ 10 m/s²)."""
import json, math, os, sys, re as _re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "130.json")
T76 = "Sự chuyển hoá động năng – thế năng"
T77 = "Bảo toàn cơ năng trong chuyển động rơi, ném"
G = 10.0

# ───────────── Số liệu (tính + kiểm) ─────────────
# Dạng 1: con lắc m = 0,2 kg, A cao 0,2 m so với O, dây 0,8 m
m1, h1, L1 = 0.2, 0.2, 0.8
W1 = 10 * m1 * h1
v1 = math.sqrt(2 * W1 / m1)
assert abs(W1 - 0.4) < 1e-12 and abs(v1 - 2) < 1e-12
assert abs(math.sqrt(W1 / m1) - 1.414) < 1e-3 and abs(2 * W1 / m1 - 4) < 1e-12        # quên ½ (1,41) · quên căn (4)
TH1 = math.degrees(math.acos(1 - h1 / L1))
assert abs(TH1 - 41.41) < 0.01

# Dạng 2: quả dừa 1,2 kg rơi từ 7,2 m; điểm giữa ở 3,2 m
m2, h2, z2 = 1.2, 7.2, 3.2
W2 = 10 * m2 * h2
v2 = math.sqrt(2 * W2 / m2)
Wt2 = 10 * m2 * z2
Wd2 = W2 - Wt2
v2b = math.sqrt(2 * Wd2 / m2)
assert abs(W2 - 86.4) < 1e-9 and abs(v2 - 12) < 1e-9 and abs(Wt2 - 38.4) < 1e-9 and abs(Wd2 - 48) < 1e-9 and abs(v2b - 8.944) < 1e-3
assert abs(math.sqrt(2 * Wt2 / m2) - v2b) > 0.5                                         # nhầm lấy Wt ở 3,2 m (8,0)
assert abs(2 * W2 / m2 - 144) < 1e-9                                                    # quên căn

# Dạng 3: bóng 0,25 kg ném lên từ mặt đất 8 m/s; vị trí Wđ = 3Wt
m3, v03 = 0.25, 8.0
W3 = 0.5 * m3 * v03 ** 2
hmax3 = W3 / (10 * m3)
Wt3 = W3 / 4
h3 = Wt3 / (10 * m3)
Wd3 = 3 * Wt3
v3 = math.sqrt(2 * Wd3 / m3)
assert W3 == 8 and abs(hmax3 - 3.2) < 1e-12 and Wt3 == 2 and abs(h3 - 0.8) < 1e-12 and Wd3 == 6 and abs(v3 - 6.928) < 1e-3
assert abs(W3 / 3 / (10 * m3) - h3) > 0.2                                               # đặt Wt = W/3 (1,07 m)
assert abs(hmax3 / 3 - h3) > 0.2 and abs(v03 * 3 / 4 - v3) > 0.5                        # chia hmax cho 3 · lấy ¾ v0 (6)

# Dạng 4: bé 20 kg trượt từ cầu trượt cao 2,5 m, nghiêng 30°, tới chân v = 6 m/s
m4, h4, v4, ALPHA = 20.0, 2.5, 6.0, 30.0
W4a = 10 * m4 * h4
W4b = 0.5 * m4 * v4 ** 2
Q4 = W4a - W4b
pct4 = Q4 / W4a * 100
v4lt = math.sqrt(2 * W4a / m4)
assert W4a == 500 and W4b == 360 and Q4 == 140 and abs(pct4 - 28) < 1e-9 and abs(v4lt - 7.071) < 1e-3
assert abs(Q4 / W4b * 100 - pct4) > 5                                                   # chia cho W ở chân (38,9 %)
L4 = h4 / math.sin(math.radians(ALPHA))
a4 = v4 ** 2 / (2 * L4)
t4 = v4 / a4
assert abs(L4 - 5) < 1e-9 and abs(a4 - 3.6) < 1e-9 and abs(t4 - 1.6667) < 1e-3

# ───────────── Hình ─────────────
def it_(s):
    return f'<tspan font-family="Georgia, \'Times New Roman\', serif" font-style="italic">{s}</tspan>'

def subt(x, y, base, idx, rest="", c="currentColor", size=17, anchor="start"):
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="700" text-anchor="{anchor}">{base}'
            f'<tspan dy="5" font-size="{max(14, size - 3)}">{idx}</tspan><tspan dy="-5">{rest}</tspan></text>')

def ballc(x, y, r=9, fill="rgba(251,146,60,.4)", op=1, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="currentColor" stroke-width="2" opacity="{op}"{d}/>'

def hatch(y, x0, x1):
    b = seg(x0, y, x1, y, "currentColor", 2.6)
    for x in range(int(x0) + 8, int(x1), 18):
        b += seg(x, y, x - 8, y + 9, "currentColor", 1.3)
    return b

def vdim(x, y_top, y_bot, label, c=ORG, lx=None, anchor="end"):
    b = seg(x, y_top + 2, x, y_bot - 2, c, 2) + chevron(x, y_top + 1, 0, -1, c, 2, 9) + chevron(x, y_bot - 1, 0, 1, c, 2, 9)
    return b + lbl(lx if lx is not None else x - 8, (y_top + y_bot) / 2 + 6, label, c, 16, anchor, "700")

# Dạng 1: con lắc — tích phân θ'' = −(g/L)·sinθ (RK4) từ A tới B
PX, PY, LPX = 210, 34, 170
def pend_pts(n=40):
    th, om, dt, out = -math.radians(TH1), 0.0, 1e-4, []
    t, rec = 0.0, [(0.0, -math.radians(TH1))]
    f = lambda th_: -(G / L1) * math.sin(th_)
    while True:
        k1 = (om, f(th)); k2 = (om + dt / 2 * k1[1], f(th + dt / 2 * k1[0]))
        k3 = (om + dt / 2 * k2[1], f(th + dt / 2 * k2[0])); k4 = (om + dt * k3[1], f(th + dt * k3[0]))
        th += dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]); om += dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]); t += dt
        rec.append((t, th))
        if om < 0 and t > 0.1 or t > 5:
            break
    T_half = rec[-1][0]
    assert 0.9 < T_half < 1.05 and abs(rec[-1][1] - math.radians(TH1)) < 1e-3, (T_half, rec[-1][1])
    for i in range(n + 1):
        tt = T_half * i / n
        j = min(range(len(rec)), key=lambda k: abs(rec[k][0] - tt))
        out.append(rec[j][1])
    return T_half, out
T_HALF, TH_S = pend_pts()
def bob(th):
    return PX + LPX * math.sin(th), PY + LPX * math.cos(th)
A1, O1, B1 = bob(-math.radians(TH1)), bob(0), bob(math.radians(TH1))

def pend_base():
    b = seg(160, PY, 260, PY, "currentColor", 3)
    for k in range(6):
        b += seg(166 + 18 * k, PY, 158 + 18 * k, PY - 10, "currentColor", 1.4)
    arcp = [bob(-math.radians(TH1) + 2 * math.radians(TH1) * i / 40) for i in range(41)]
    b += pts_path(arcp, GRN, 2, "7 5")
    b += seg(40, O1[1], 400, O1[1], "currentColor", 1.4, "6 5", .7)
    b += seg(40, A1[1], A1[0] - 12, A1[1], "currentColor", 1.3, "4 4", .7)
    b += lbl(A1[0] - 16, A1[1] - 12, "A", "currentColor", 18, "end", "700") + lbl(B1[0] + 16, B1[1] - 12, "B", "currentColor", 18, "start", "700")
    b += lbl(O1[0], O1[1] + 34, "O", "currentColor", 18, "middle", "700")
    return b

def d1(k):
    b = pend_base()
    if k == 0:
        xs = [bob(t)[0] for t in TH_S]; ys = [bob(t)[1] for t in TH_S]
        DUR = T_HALF * 3
        b += (f'<line x1="{PX}" y1="{PY}" x2="{xs[0]:.1f}" y2="{ys[0]:.1f}" stroke="currentColor" stroke-width="2">'
              f'{smil("x2", xs, DUR)}{smil("y2", ys, DUR)}</line>')
        b += (f'<circle cx="{xs[0]:.1f}" cy="{ys[0]:.1f}" r="11" fill="rgba(251,146,60,.5)" stroke="currentColor" stroke-width="2">'
              f'{smil("cx", xs, DUR)}{smil("cy", ys, DUR)}</circle>')
        b += vdim(62, A1[1], O1[1], "0,2 m", ORG, 56)
        b += lbl(O1[0] + 18, O1[1] - 14, it_("v") + " = ?", RED, 17, "start", "700")
        b += lbl(20, 262, "Vật 0,2 kg, thả nhẹ từ A", BLUE, 16, "start", "700")
        return fig("d1-0", "0 0 420 276", "Con lắc đơn vật 0,2 kg thả từ A cao 0,2 mét so với O, đi qua O tới B; cần tìm vận tốc ở O", b,
                   f"Mô phỏng (bấm Chạy mô phỏng): vật đi một lượt từ A qua O tới B.<br>Chạy chậm 3 lần so với thật (dây dài 0,8 m).")
    b += seg(PX, PY, A1[0], A1[1], "currentColor", 2) + ballc(A1[0], A1[1], 11)
    b += ballc(O1[0], O1[1], 11, "none", .6, "4 3")
    b += vdim(62, A1[1], O1[1], "0,2 m", ORG, 56)
    b += lbl(400, O1[1] - 8, "gốc thế năng", "currentColor", 15, "end", "600")
    b += lbl(20, 262, "⚠ Bỏ qua lực cản: cơ năng ở A = ở O", RED, 16, "start", "700")
    return fig("d1-2", "0 0 420 276", "Dữ kiện con lắc: A cao 0,2 mét so với O, gốc thế năng tại O", b,
               "Dữ kiện: thả nhẹ ở A nên $v_A = 0$.<br>Gốc thế năng tại O nên $W_{t,O} = 0$.")

# Dạng 2: quả dừa rơi
GY2, S2, X2 = 236, 26.0, 150
def y2(z): return GY2 - S2 * z
def palm():
    b = f'<path d="M{X2 - 50},{GY2} C{X2 - 44},{GY2 - 80} {X2 - 30},{y2(7.2) + 40} {X2 - 22},{y2(7.2) - 4}" fill="none" stroke="currentColor" stroke-width="5"/>'
    for dx, dy in ((-60, 14), (-30, -22), (28, -18), (56, 14)):
        b += f'<path d="M{X2 - 22},{y2(7.2) - 4} q{dx / 2},{dy - 12} {dx},{dy}" fill="none" stroke="{GRN}" stroke-width="3"/>'
    return b
def d2(k):
    b = hatch(GY2, 14, 410) + palm()
    b += seg(X2 + 30, y2(7.2), 300, y2(7.2), "currentColor", 1.3, "4 4", .7)
    if k == 0:
        n = 30
        ys = [y2(h2 - 0.5 * G * (1.2 * i / n) ** 2) for i in range(n + 1)]
        ys[-1] = GY2 - 9
        b += f'<circle cx="{X2}" cy="{ys[0]:.1f}" r="9" fill="rgba(52,211,153,.5)" stroke="currentColor" stroke-width="2">{smil("cy", ys, 2.4)}</circle>'
        b += vdim(320, y2(7.2), GY2, "7,2 m", ORG, 330, "start")
        b += lbl(X2 + 16, GY2 - 14, it_("v") + " = ?", RED, 17, "start", "700")
        b += lbl(230, 30, "Quả dừa 1,2 kg", BLUE, 16, "start", "700")
        return fig("d2-0", "0 0 420 256", "Quả dừa 1,2 kg rụng từ độ cao 7,2 mét, rơi thẳng xuống đất; cần tìm vận tốc chạm đất", b,
                   "Mô phỏng (bấm Chạy mô phỏng): quả dừa rơi tự do từ 7,2 m.<br>Chạy chậm 2 lần so với thật.")
    b += ballc(X2, y2(7.2) + 9, 9, "rgba(52,211,153,.5)") + ballc(X2, y2(3.2), 9, "none", .7, "4 3") + ballc(X2, GY2 - 9, 9, "none", .7, "4 3")
    b += seg(X2 + 14, y2(3.2), 300, y2(3.2), "currentColor", 1.3, "4 4", .7)
    b += lbl(306, y2(7.2) + 6, "1: 7,2 m, " + it_("v") + " = 0", BLUE, 15, "start", "700")
    b += lbl(306, y2(3.2) + 6, "2: 3,2 m, " + it_("v") + " = ?", RED, 15, "start", "700")
    b += lbl(306, GY2 - 10, "3: đất, " + it_("v") + " = ?", RED, 15, "start", "700")
    return fig("d2-2", "0 0 420 256", "Ba vị trí: 1 ở 7,2 mét vận tốc 0; 2 ở 3,2 mét; 3 ở mặt đất", b,
               "Dữ kiện: gốc thế năng ở mặt đất.<br>Ở vị trí 1 vật chỉ có thế năng.")

# Dạng 3: ném thẳng đứng lên từ mặt đất
GY3, S3, X3 = 240, 60.0, 190
def d3(k):
    b = hatch(GY3, 14, 410)
    if k == 0:
        Tt = 2 * v03 / G
        n = 32
        ys = [GY3 - 9 - S3 * (v03 * (Tt * i / n) - 0.5 * G * (Tt * i / n) ** 2) for i in range(n + 1)]
        assert abs(min(ys) - (GY3 - 9 - S3 * hmax3)) < 1 and min(ys) > 30
        b += f'<circle cx="{X3}" cy="{ys[0]:.1f}" r="9" fill="rgba(52,211,153,.5)" stroke="currentColor" stroke-width="2">{smil("cy", ys, 2 * Tt)}</circle>'
        b += seg(X3 - 34, GY3 - 20, X3 - 34, GY3 - 80, RED, 2.6) + chevron(X3 - 34, GY3 - 80, 0, -1, RED, 2.6, 11)
        b += subt(X3 - 44, GY3 - 46, it_("v"), "0", " = 8 m/s", RED, 16, "end")
        b += subt(X3 + 24, 40, it_("h"), "max", " = ?", ORG, 17)
        b += lbl(250, 228, "Bóng 0,25 kg", BLUE, 16, "start", "700")
        return fig("d3-0", "0 0 420 256", "Bóng 0,25 kg ném thẳng đứng lên từ mặt đất với vận tốc 8 m/s, lên tới độ cao lớn nhất rồi rơi về", b,
                   "Mô phỏng (bấm Chạy mô phỏng): bóng lên tới điểm cao nhất rồi rơi về.<br>Chạy chậm 2 lần so với thật.")
    b += ballc(X3, GY3 - 9, 9, "rgba(52,211,153,.5)")
    b += seg(X3 - 34, GY3 - 20, X3 - 34, GY3 - 80, RED, 2.6) + chevron(X3 - 34, GY3 - 80, 0, -1, RED, 2.6, 11)
    b += subt(X3 - 44, GY3 - 46, it_("v"), "0", " = 8 m/s", RED, 16, "end")
    b += ballc(X3, 140, 9, "none", .7, "4 3") + ballc(X3, 48, 9, "none", .7, "4 3")
    b += lbl(X3 + 20, 54, "cao nhất: " + it_("v") + " = 0", "currentColor", 15, "start", "700")
    sb = lambda i: f'<tspan dy="5" font-size="14">{i}</tspan><tspan dy="-5">'
    b += lbl(X3 + 20, 136, it_("W") + sb("đ") + " = 3" + it_("W") + "</tspan>" + sb("t") + "</tspan>", BLUE, 16, "start", "700")
    b += lbl(X3 + 20, 162, it_("h") + " = ?", ORG, 16, "start", "700")
    return fig("d3-2", "0 0 420 256", "Dữ kiện: ném từ mặt đất với 8 m/s; tìm vị trí động năng bằng ba lần thế năng; điểm cao nhất vận tốc bằng 0", b,
               "Dữ kiện: ném từ mặt đất nên lúc ném $W_t = 0$.<br>Hình không vẽ đúng tỉ lệ độ cao.")

# Dạng 4: cầu trượt nghiêng 30°
S4 = 44.0
TX, TY = 70, 50
BX, BY = TX + S4 * L4 * math.cos(math.radians(ALPHA)), TY + S4 * h4
def slide_base():
    b = hatch(BY + 8, 14, 410)
    b += f'<path d="M{TX - 10},{TY - 6} L{BX},{BY - 6} L{BX + 30},{BY - 6}" fill="none" stroke="currentColor" stroke-width="3"/>'
    b += seg(TX - 10, TY - 6, TX - 10, BY + 8, "currentColor", 2.6) + seg(TX - 30, TY - 6, TX - 30, BY + 8, "currentColor", 2.6)
    for yy in range(int(TY + 10), int(BY), 22):
        b += seg(TX - 30, yy, TX - 10, yy, "currentColor", 1.8)
    return b
def d4(k):
    b = slide_base()
    b += seg(BX + 50, TY - 6, BX + 50, BY + 6, ORG, 2) + chevron(BX + 50, TY - 5, 0, -1, ORG, 2, 9) + chevron(BX + 50, BY + 7, 0, 1, ORG, 2, 9)
    b += seg(TX, TY - 6, BX + 58, TY - 6, "currentColor", 1.2, "4 4", .6)
    b += lbl(BX + 58, (TY + BY) / 2 + 4, "2,5 m", ORG, 16, "start", "700")
    ux, uy = math.cos(math.radians(ALPHA)), math.sin(math.radians(ALPHA))
    nx, ny = uy, -ux                                       # pháp tuyến hướng lên trên mặt cầu trượt
    if k == 0:
        n = 30
        ss = [0.5 * a4 * (t4 * i / n) ** 2 for i in range(n + 1)]
        assert abs(ss[-1] - L4) < 1e-9
        xs = [TX + S4 * s * ux + 10 * nx for s in ss]; ys = [TY - 6 + S4 * s * uy + 10 * ny for s in ss]
        b += f'<circle cx="{xs[0]:.1f}" cy="{ys[0]:.1f}" r="10" fill="rgba(251,146,60,.5)" stroke="currentColor" stroke-width="2">{smil("cx", xs, 2 * t4)}{smil("cy", ys, 2 * t4)}</circle>'
        b += lbl(BX - 30, BY + 34, it_("v") + " = 6 m/s ở chân", RED, 16, "start", "700")
        b += lbl(150, 30, "Bé 20 kg, thả nhẹ ở đỉnh", BLUE, 16, "start", "700")
        return fig("d4-0", "0 0 420 256", "Bé 20 kg trượt từ đỉnh cầu trượt cao 2,5 mét, tới chân với vận tốc 6 m/s", b,
                   "Mô phỏng (bấm Chạy mô phỏng): bé trượt nhanh dần xuống chân cầu.<br>Chạy chậm 2 lần so với thật.")
    b += lbl(TX + 4, TY - 18, "đỉnh: " + it_("W") + " = ?", BLUE, 15, "start", "700")
    b += lbl(BX - 120, BY + 34, "chân: " + it_("W") + " = ?", BLUE, 15, "start", "700")
    b += lbl(20, 238, "ma sát → nhiệt năng = ?", RED, 16, "start", "700")
    return fig("d4-2", "0 0 420 256", "Dữ kiện: cầu trượt cao 2,5 mét, có ma sát; cần cơ năng ở đỉnh, ở chân và phần thành nhiệt", b,
               "Dữ kiện: gốc thế năng ở chân cầu.<br>⚠ Có ma sát: cơ năng ở chân nhỏ hơn ở đỉnh.")

BUILD = [d1, d2, d3, d4]

# ───────────── Đề ─────────────
DE = [
 dict(label="Dạng 1 · Con lắc đơn: chuyển hoá động năng – thế năng và vận tốc ở vị trí thấp nhất", topic=T76,
      problem_html=r"<p>Một con lắc đơn có vật nặng $0{,}2\ \text{kg}$. Kéo vật lên vị trí A cao $0{,}2\ \text{m}$ so với vị trí cân bằng O rồi thả nhẹ. Bỏ qua lực cản. Chọn gốc thế năng tại O.</p>"
                   r"<ol type=\"a\"><li>Ở vị trí nào thế năng của vật lớn nhất?</li><li>Khi vật đi từ A về O, năng lượng chuyển hoá thế nào?</li>"
                   r"<li>Tính cơ năng của con lắc.</li><li>Tính vận tốc của vật khi đi qua O.</li></ol>"),
 dict(label="Dạng 2 · Vật rơi không vận tốc đầu: vận tốc chạm đất và ở độ cao giữa chừng", topic=T77,
      problem_html=r"<p>Một quả dừa $1{,}2\ \text{kg}$ rụng (không vận tốc đầu) từ độ cao $7{,}2\ \text{m}$ so với mặt đất. Bỏ qua sức cản không khí. Chọn gốc thế năng ở mặt đất.</p>"
                   r"<ol type=\"a\"><li>Tính cơ năng của quả dừa.</li><li>Tính vận tốc của quả dừa lúc chạm đất.</li>"
                   r"<li>Tính vận tốc của quả dừa khi nó ở độ cao $3{,}2\ \text{m}$.</li></ol>"),
 dict(label="Dạng 3 · Ném thẳng đứng lên: độ cao lớn nhất và vị trí động năng gấp ba thế năng", topic=T77,
      problem_html=r"<p>Từ mặt đất, ném một quả bóng $0{,}25\ \text{kg}$ thẳng đứng lên với vận tốc $8\ \text{m/s}$. Bỏ qua sức cản không khí. Chọn gốc thế năng ở mặt đất.</p>"
                   r"<ol type=\"a\"><li>Tính cơ năng của bóng.</li><li>Tính độ cao lớn nhất bóng lên được.</li>"
                   r"<li>Ở độ cao nào thì động năng của bóng bằng ba lần thế năng? Tính vận tốc của bóng khi đó.</li></ol>"),
 dict(label="Dạng 4 · Có ma sát: cơ năng giảm, phần chuyển thành nhiệt năng", topic=T76,
      problem_html=r"<p>Một bé $20\ \text{kg}$ ngồi ở đỉnh cầu trượt cao $2{,}5\ \text{m}$ rồi trượt xuống (không vận tốc đầu). Tới chân cầu trượt, bé có vận tốc $6\ \text{m/s}$. Chọn gốc thế năng ở chân cầu trượt.</p>"
                   r"<ol type=\"a\"><li>Tính cơ năng của bé ở đỉnh và ở chân cầu trượt.</li>"
                   r"<li>Cơ năng có được bảo toàn không? Tính phần cơ năng đã chuyển thành nhiệt năng và cho biết nó bằng bao nhiêu phần trăm cơ năng ở đỉnh.</li>"
                   r"<li>Nếu bỏ qua được ma sát, bé tới chân cầu trượt với vận tốc bao nhiêu?</li></ol>"),
]
for d_ in DE:
    d_["problem_html"] = d_["problem_html"].replace('\\"', '"')
    d_["problem_html"] = _re.sub(r'<ol type="a">(.*?)</ol>', lambda m_: "".join(f"<p>{chr(97 + i)}) {t}</p>" for i, t in enumerate(_re.findall(r"<li>(.*?)</li>", m_.group(1)))), d_["problem_html"], flags=_re.S)
    assert "<ol" not in d_["problem_html"]

# ───────────── Phân tích đề ─────────────
ANALYSIS = [
 [(r"&quot;vật nặng 0,2 kg&quot;", r"$m=0{,}2\ \text{kg}$", r"$W_đ=\frac{1}{2}mv^2$, $W_t=10mh$"),
  (r"&quot;cao 0,2 m so với vị trí cân bằng O&quot;", r"$h_A=0{,}2\ \text{m}$", r"Độ cao tính từ gốc thế năng"),
  (r"&quot;thả nhẹ&quot;", r"$v_A=0$", r"Ở A chỉ có thế năng"),
  (r"&quot;Bỏ qua lực cản&quot;", r"Không mất cơ năng", r"⚠ Điều kiện để cơ năng bảo toàn: $W_A=W_O$"),
  (r"&quot;Chọn gốc thế năng tại O&quot;", r"$h_O=0$", r"Ở O thế năng bằng 0"),
  (r"&quot;Tính vận tốc của vật khi đi qua O&quot;", r"Cần $v_O$", r"$W=\frac{1}{2}mv_O^2$")],
 [(r"&quot;quả dừa 1,2 kg&quot;", r"$m=1{,}2\ \text{kg}$", r"Dùng trong cả $W_t$ và $W_đ$"),
  (r"&quot;rụng (không vận tốc đầu) từ độ cao 7,2 m&quot;", r"$v_1=0$; $h_1=7{,}2\ \text{m}$", r"Lúc đầu $W=W_t=10mh$"),
  (r"&quot;Bỏ qua sức cản không khí&quot;", r"Không mất cơ năng", r"⚠ Điều kiện: cơ năng như nhau ở mọi độ cao"),
  (r"&quot;vận tốc lúc chạm đất&quot;", r"$h=0$; cần $v$", r"$W=\frac{1}{2}mv^2$"),
  (r"&quot;ở độ cao 3,2 m&quot;", r"$h_2=3{,}2\ \text{m}$; cần $v_2$", r"$W_{đ2}=W-W_{t2}$")],
 [(r"&quot;Từ mặt đất … ném … với vận tốc 8 m/s&quot;", r"$h_0=0$; $v_0=8\ \text{m/s}$", r"Lúc ném $W=W_đ$"),
  (r"&quot;quả bóng 0,25 kg&quot;", r"$m=0{,}25\ \text{kg}$", r"$W_đ=\frac{1}{2}mv^2$, $W_t=10mh$"),
  (r"&quot;Bỏ qua sức cản không khí&quot;", r"Không mất cơ năng", r"⚠ Điều kiện để cơ năng bảo toàn"),
  (r"&quot;độ cao lớn nhất&quot;", r"Ở đó $v=0$", r"$W=10mh_{\max}$"),
  (r"&quot;động năng … bằng ba lần thế năng&quot;", r"$W_đ=3W_t$", r"$W=W_đ+W_t$: viết $W$ theo $W_t$"),
  (r"&quot;Tính vận tốc của bóng khi đó&quot;", r"Cần $v$", r"$W_đ=\frac{1}{2}mv^2$")],
 [(r"&quot;bé 20 kg&quot;", r"$m=20\ \text{kg}$", r"$W_t=10mh$, $W_đ=\frac{1}{2}mv^2$"),
  (r"&quot;đỉnh cầu trượt cao 2,5 m … không vận tốc đầu&quot;", r"$h=2{,}5\ \text{m}$; $v=0$", r"Ở đỉnh $W=W_t$"),
  (r"&quot;Tới chân … vận tốc 6 m/s&quot;", r"$v=6\ \text{m/s}$; $h=0$", r"Ở chân $W=W_đ$"),
  (r"&quot;Cơ năng có được bảo toàn không?&quot;", r"So hai cơ năng", r"⚠ Có ma sát thì cơ năng giảm; năng lượng toàn phần vẫn bảo toàn"),
  (r"&quot;phần cơ năng đã chuyển thành nhiệt năng&quot;", r"Cần $Q$", r"$Q=W_{\text{đỉnh}}-W_{\text{chân}}$"),
  (r"&quot;Nếu bỏ qua được ma sát&quot;", r"Cơ năng bảo toàn", r"$W_{\text{đỉnh}}=\frac{1}{2}mv^2$")],
]

# ───────────── Lời giải ─────────────
RW = [r"<strong>Khái niệm:</strong> cơ năng là tổng động năng và thế năng.",
      r"Công thức: $W=\frac{1}{2}mv^2+10mh$.",
      r"Đơn vị: $m$ (kg), $v$ (m/s), $h$ (m), $W$ (J).",
      r"⚠ <strong>Điều kiện:</strong> không có lực cản, ma sát thì cơ năng không đổi ở mọi vị trí."]

SOLS = [
 sol([r"<strong>Khái niệm:</strong> đi lên thì động năng chuyển thành thế năng; đi xuống thì ngược lại."] + RW[1:], [
  ("Vị trí thế năng lớn nhất", [P("Thế năng lớn nhất ở chỗ cao nhất:"), A("T:ở hai biên A và B.")]),
  ("Chuyển hoá từ A về O", [P("Vật thấp dần, nhanh dần:"), A("T:thế năng chuyển dần thành động năng.")]),
  ("Cơ năng", [P("Ở A: $v_A=0$, nên $W=W_{tA}$:"), M(r"W=10mh_A"), M(r"W=10\cdot0{,}2\cdot0{,}2"), A(r"W=0{,}4\ \text{J}")]),
  ("Vận tốc ở O", [P("Ở O: $W_t=0$, nên $W=W_{đO}$:"), M(r"\frac{1}{2}mv_O^2=W"), M(r"v_O^2=\frac{2\cdot0{,}4}{0{,}2}=4"), A(r"v_O=2\ \text{m/s}")]),
  ("Kiểm tra", [P("Thử lại: $\\frac{1}{2}\\cdot0{,}2\\cdot2^2=0{,}4\\ \\text{J}$ ✓"), P("Đơn vị: J chia kg ra m²/s², lấy căn ra m/s ✓")])],
  [r"a) Ở hai biên A và B", r"b) Thế năng chuyển dần thành động năng", r"c) $W=0{,}4\ \text{J}$", r"d) $v_O=2\ \text{m/s}$"],
  "Nhận dạng: <strong>thả nhẹ ở độ cao h, hỏi vận tốc ở chỗ thấp nhất</strong> → $W=10mh$ ở chỗ thả, $=\\frac{1}{2}mv^2$ ở chỗ thấp nhất."),
 sol(RW, [
  ("Cơ năng", [P("Lúc rụng $v=0$, nên $W=W_t$:"), M(r"W=10\cdot1{,}2\cdot7{,}2"), A(r"W=86{,}4\ \text{J}")]),
  ("Vận tốc chạm đất", [P("Chạm đất: $W_t=0$, $W=W_đ$:"), M(r"v^2=\frac{2W}{m}=\frac{2\cdot86{,}4}{1{,}2}=144"), A(r"v=12\ \text{m/s}")]),
  ("Động năng ở độ cao 3,2 m", [M(r"W_{t2}=10\cdot1{,}2\cdot3{,}2=38{,}4\ \text{J}"), M(r"W_{đ2}=W-W_{t2}=86{,}4-38{,}4"), A(r"W_{đ2}=48\ \text{J}")]),
  ("Vận tốc ở độ cao 3,2 m", [M(r"v_2^2=\frac{2\cdot48}{1{,}2}=80"), A(r"v_2\approx8{,}94\ \text{m/s}")]),
  ("Kiểm tra", [P("$8{,}94\\ \\text{m/s}$ nhỏ hơn $12\\ \\text{m/s}$: chưa tới đất nên chậm hơn ✓"), P("Cộng lại: $38{,}4+48=86{,}4\\ \\text{J}$ ✓")])],
  [r"a) $W=86{,}4\ \text{J}$", r"b) $v=12\ \text{m/s}$", r"c) $v_2\approx8{,}94\ \text{m/s}$"],
  "Nhận dạng: <strong>rơi không vận tốc đầu, hỏi vận tốc ở độ cao khác</strong> → $W=10mh$ lúc đầu, $W_đ=W-W_t$ ở chỗ cần tìm."),
 sol(RW, [
  ("Cơ năng", [P("Ném từ mặt đất: $W_t=0$, $W=W_đ$:"), M(r"W=\frac{1}{2}\cdot0{,}25\cdot8^2"), A(r"W=8\ \text{J}")]),
  ("Độ cao lớn nhất", [P("Ở điểm cao nhất $v=0$, $W=W_t$:"), M(r"h_{\max}=\frac{W}{10m}=\frac{8}{10\cdot0{,}25}"), A(r"h_{\max}=3{,}2\ \text{m}")]),
  ("Thế năng ở vị trí cần tìm", [P("$W_đ=3W_t$ nên:"), M(r"W=W_đ+W_t=4W_t"), M(r"W_t=\frac{W}{4}=\frac{8}{4}"), A(r"W_t=2\ \text{J}")]),
  ("Độ cao ở vị trí đó", [M(r"h=\frac{W_t}{10m}=\frac{2}{2{,}5}"), A(r"h=0{,}8\ \text{m}")]),
  ("Vận tốc ở vị trí đó", [M(r"W_đ=3W_t=6\ \text{J}"), M(r"v^2=\frac{2\cdot6}{0{,}25}=48"), A(r"v\approx6{,}93\ \text{m/s}")]),
  ("Kiểm tra", [P("$h=0{,}8\\ \\text{m}=\\frac{1}{4}h_{\\max}$: đúng vì $W_t=\\frac{1}{4}W$ ✓"), P("$W_đ+W_t=6+2=8\\ \\text{J}$ ✓")])],
  [r"a) $W=8\ \text{J}$", r"b) $h_{\max}=3{,}2\ \text{m}$", r"c) $h=0{,}8\ \text{m}$", r"$v\approx6{,}93\ \text{m/s}$"],
  "Nhận dạng: <strong>động năng bằng n lần thế năng</strong> → $W=(n+1)W_t$, suy ra $W_t$ rồi $h$."),
 sol([r"<strong>Khái niệm:</strong> có ma sát, một phần cơ năng chuyển thành nhiệt năng.", r"Công thức: $W=\frac{1}{2}mv^2+10mh$.",
      r"Nhiệt năng sinh ra: $Q=W_{\text{đầu}}-W_{\text{sau}}$.",
      r"⚠ <strong>Điều kiện:</strong> cơ năng chỉ bảo toàn khi không có ma sát, lực cản; năng lượng toàn phần thì luôn bảo toàn."], [
  ("Cơ năng ở đỉnh", [P("Ở đỉnh $v=0$:"), M(r"W_1=10mh=10\cdot20\cdot2{,}5"), A(r"W_1=500\ \text{J}")]),
  ("Cơ năng ở chân", [P("Ở chân $h=0$:"), M(r"W_2=\frac{1}{2}mv^2=\frac{1}{2}\cdot20\cdot6^2"), A(r"W_2=360\ \text{J}")]),
  ("Phần thành nhiệt năng", [P("$W_2\\lt W_1$: cơ năng không bảo toàn."), M(r"Q=W_1-W_2=500-360"), A(r"Q=140\ \text{J}")]),
  ("Phần trăm so với cơ năng ở đỉnh", [M(r"\frac{Q}{W_1}\cdot100\ \%=\frac{140}{500}\cdot100\ \%"), A(r"28\ \%")]),
  ("Vận tốc nếu không ma sát", [P("Cơ năng bảo toàn: $\\frac{1}{2}mv^2=W_1$:"), M(r"v^2=\frac{2\cdot500}{20}=50"), A(r"v\approx7{,}07\ \text{m/s}")]),
  ("Kiểm tra", [P("Không ma sát thì nhanh hơn: $7{,}07\\gt6$ ✓"), P("$360+140=500\\ \\text{J}$: năng lượng toàn phần không mất ✓")])],
  [r"a) $W_1=500\ \text{J}$; $W_2=360\ \text{J}$", r"b) Không bảo toàn; $Q=140\ \text{J}$, bằng $28\ \%$", r"c) $v\approx7{,}07\ \text{m/s}$"],
  "Nhận dạng: đề cho <strong>vận tốc thật ở chân dốc</strong> (có ma sát) → tính cơ năng hai đầu, hiệu số là nhiệt năng."),
]

# ───────────── Tự giải từng bước ─────────────
STEPS = [
 dict(nhan_dang=r"Thấy <b>thả nhẹ ở độ cao h</b> và <b>bỏ qua lực cản</b> → $10mh=\frac{1}{2}mv^2$ ở chỗ thấp nhất.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Vị trí thế năng lớn nhất", "Thế năng của vật lớn nhất ở đâu?",
       loi=r"Hay chọn O vì ở đó vật chạy nhanh nhất. Chạy nhanh nhất là động năng lớn nhất; thế năng lớn nhất ở chỗ cao nhất.",
       lua_chon=[("Ở hai biên A và B", True),
                 ("Ở vị trí cân bằng O", r"O là chỗ thấp nhất, thế năng bằng 0 (gốc thế năng)."),
                 ("Ở mọi vị trí như nhau", r"Cơ năng mới không đổi; thế năng thay đổi theo độ cao.")]),
  buoc("Chuyển hoá từ A về O", "Khi vật đi từ A về O, năng lượng chuyển hoá thế nào?",
       loi=r"Hay nói ngược chiều. Từ A về O vật thấp dần (thế năng giảm) và nhanh dần (động năng tăng).",
       lua_chon=[("Thế năng chuyển dần thành động năng", True),
                 ("Động năng chuyển dần thành thế năng", r"Đó là lúc vật đi từ O lên A hoặc B."),
                 ("Không có chuyển hoá vì cơ năng không đổi", r"Tổng không đổi nhưng từng phần vẫn tăng giảm.")],
       ke=[(r"Xét độ cao và tốc độ của vật thay đổi thế nào", True),
           (r"Xét khối lượng vật thay đổi thế nào", r"Khối lượng không đổi khi vật chuyển động."),
           (r"Xét chiều dài dây thay đổi thế nào", r"Dây không dãn, chiều dài không đổi.")]),
  buoc("Cơ năng", "Cơ năng của con lắc bằng bao nhiêu jun?", 0.4, "J", 0.005,
       loi=r"Hay quên số 10 trong $W_t=10mh$, ra $0{,}04$ J. Thế năng là trọng lượng $P=10m$ nhân độ cao.",
       ke=[(r"Tính ở A: $W=W_t=10mh$", True),
           (r"Tính ở A: $W=\frac{1}{2}mv^2$", r"Ở A vật được thả nhẹ, $v=0$ nên động năng bằng 0."),
           (r"Tính ở O: $W=10mh$ với $h=0{,}2\ \text{m}$", r"O là gốc thế năng, ở O thì $h=0$.")]),
  buoc("Vận tốc ở O", "Vận tốc của vật khi đi qua O bằng bao nhiêu?", 2, "m/s", 0.02,
       loi=r"Hay quên lấy căn: $v^2=4$ mới là bình phương vận tốc. Hoặc quên $\frac{1}{2}$, ra $v^2=2$.",
       ke=[(r"Đặt $\frac{1}{2}mv_O^2=W$ rồi lấy căn", True),
           (r"Đặt $mv_O^2=W$", r"Thiếu $\frac{1}{2}$: động năng là $\frac{1}{2}mv^2$."),
           (r"Đặt $v_O=\frac{W}{m}$", r"Thiếu bình phương: động năng tỉ lệ với $v^2$, không phải $v$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>rơi không vận tốc đầu</b> và hỏi <b>vận tốc ở độ cao khác</b> → $W=10mh$, rồi $W_đ=W-W_t$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Cơ năng", "Cơ năng của quả dừa bằng bao nhiêu jun?", 86.4, "J", 0.3,
       loi=r"Hay cộng thêm động năng lúc rụng. Rụng không vận tốc đầu nên lúc đó $W_đ=0$, $W=W_t$."),
  buoc("Vận tốc chạm đất", "Vận tốc lúc chạm đất bằng bao nhiêu?", 12, "m/s", 0.1,
       loi=r"Hay dừng ở $v^2=144$ mà quên lấy căn.",
       ke=[(r"$\frac{1}{2}mv^2=W$ (ở đất $W_t=0$)", True),
           (r"$\frac{1}{2}mv^2=W_t$ ở độ cao $3{,}2\ \text{m}$", r"Chạm đất thì toàn bộ cơ năng là động năng."),
           (r"$v=\frac{W}{m}$", r"Thiếu $\frac{1}{2}$ và bình phương của $v$.")]),
  buoc("Động năng ở độ cao 3,2 m", "Động năng của quả dừa ở độ cao 3,2 m bằng bao nhiêu jun?", 48, "J", 0.3,
       loi=r"Hay lấy luôn thế năng ở $3{,}2\ \text{m}$ làm động năng. Động năng là phần còn lại: $W-W_t$.",
       ke=[(r"$W_đ=W-10mh$ với $h=3{,}2\ \text{m}$", True),
           (r"$W_đ=10mh$ với $h=3{,}2\ \text{m}$", r"Đó là thế năng ở độ cao này, không phải động năng."),
           (r"$W_đ=10m(7{,}2+3{,}2)$", r"Độ cao không cộng dồn; vật đã rơi xuống, còn cách đất $3{,}2\ \text{m}$.")]),
  buoc("Vận tốc ở độ cao 3,2 m", "Vận tốc ở độ cao 3,2 m bằng bao nhiêu?", 8.94, "m/s", 0.05,
       loi=r"Hay dùng nhầm cơ năng cả vật thay cho động năng ở độ cao này: kết quả sẽ bằng vận tốc chạm đất.",
       ke=[(r"$v_2^2=\frac{2W_{đ2}}{m}$ rồi lấy căn", True),
           (r"$v_2^2=\frac{2W}{m}$", r"$W$ là cả cơ năng; ở độ cao này chỉ một phần là động năng."),
           (r"Lấy nửa vận tốc chạm đất vì đã rơi được hơn nửa đường", r"Vận tốc không tỉ lệ với quãng đường rơi.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>động năng bằng n lần thế năng</b> → $W=(n+1)W_t$, tìm $W_t$ rồi $h$.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Cơ năng", "Cơ năng của bóng bằng bao nhiêu jun?", 8, "J", 0.05,
       loi=r"Hay quên $\frac{1}{2}$ trong động năng. Ném từ mặt đất nên $W=W_đ=\frac{1}{2}mv_0^2$."),
  buoc("Độ cao lớn nhất", "Độ cao lớn nhất bóng lên được là bao nhiêu mét?", 3.2, "m", 0.03,
       loi=r"Hay cho rằng ở điểm cao nhất cơ năng bằng 0. Ở đó $W_đ=0$ nhưng $W=W_t=10mh_{\max}$.",
       ke=[(r"Ở điểm cao nhất $v=0$: $10mh_{\max}=W$", True),
           (r"Ở điểm cao nhất $W=0$ vì bóng dừng lại", r"Bóng dừng thì động năng bằng 0, thế năng lúc đó lớn nhất."),
           (r"$h_{\max}=\frac{v_0}{10}$", r"Thiếu bình phương: $h_{\max}=\frac{v_0^2}{20}$.")]),
  buoc("Thế năng ở vị trí Wđ = 3Wt", "Thế năng của bóng ở vị trí động năng bằng ba lần thế năng là bao nhiêu jun?", 2, "J", 0.02,
       loi=r"Hay đặt $W_t=\frac{W}{3}$. Đúng là $W=W_đ+W_t=3W_t+W_t=4W_t$.",
       ke=[(r"$W=W_đ+W_t=4W_t$", True),
           (r"$W=3W_t$", r"Quên cộng chính $W_t$: cơ năng gồm cả động năng lẫn thế năng."),
           (r"$W_t=3W_đ$", r"Đảo ngược: đề cho động năng bằng ba lần thế năng.")]),
  buoc("Độ cao ở vị trí đó", "Độ cao của bóng khi động năng bằng ba lần thế năng là bao nhiêu mét?", 0.8, "m", 0.01,
       loi=r"Hay lấy $\frac{h_{\max}}{3}$. Vì $W_t=\frac{W}{4}$ nên độ cao bằng $\frac{1}{4}h_{\max}$.",
       ke=[(r"$h=\frac{W_t}{10m}$", True),
           (r"$h=\frac{h_{\max}}{3}$", r"Thế năng chiếm $\frac{1}{4}$ cơ năng, không phải $\frac{1}{3}$."),
           (r"$h=\frac{W_t}{m}$", r"Thiếu số 10: $W_t=10mh$.")]),
  buoc("Vận tốc ở vị trí đó", "Vận tốc của bóng khi đó bằng bao nhiêu?", 6.93, "m/s", 0.05,
       loi=r"Hay lấy $\frac{3}{4}v_0$. Động năng là $\frac{3}{4}W$, mà động năng tỉ lệ với $v^2$, không tỉ lệ với $v$.",
       ke=[(r"$W_đ=3W_t$, rồi $v^2=\frac{2W_đ}{m}$", True),
           (r"$v=\frac{3}{4}v_0$", r"Động năng tỉ lệ với $v^2$; phải tính qua $W_đ$ rồi lấy căn."),
           (r"$v^2=\frac{2W}{m}$", r"Đó là vận tốc lúc ném; ở vị trí này chỉ $\frac{3}{4}W$ là động năng.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>vận tốc thật ở chân dốc nhỏ hơn khi không ma sát</b> → cơ năng hai đầu, hiệu là nhiệt năng.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Cơ năng ở đỉnh", "Cơ năng của bé ở đỉnh cầu trượt là bao nhiêu jun?", 500, "J", 2,
       loi=r"Hay quên số 10 trong $W_t=10mh$. Ở đỉnh $v=0$ nên $W=10mh$."),
  buoc("Cơ năng ở chân", "Cơ năng của bé ở chân cầu trượt là bao nhiêu jun?", 360, "J", 2,
       loi=r"Hay cho rằng cơ năng ở chân bằng ở đỉnh. Có ma sát nên phải tính lại từ vận tốc thật ở chân.",
       ke=[(r"Ở chân $h=0$: $W_2=\frac{1}{2}mv^2$ với vận tốc đề cho", True),
           (r"$W_2=W_1$ vì cơ năng bảo toàn", r"Đề cho vận tốc thật ở chân; có ma sát nên phải kiểm tra, không được giả sử bảo toàn."),
           (r"$W_2=10mh+\frac{1}{2}mv^2$ với $h=2{,}5\ \text{m}$", r"Ở chân cầu trượt (gốc thế năng) $h=0$.")]),
  buoc("Phần thành nhiệt năng", "Phần cơ năng đã chuyển thành nhiệt năng là bao nhiêu jun?", 140, "J", 2,
       loi=r"Hay nói năng lượng đã mất. Phần cơ năng giảm không mất đi, nó thành nhiệt năng ở mặt trượt và quần áo.",
       ke=[(r"$Q=W_1-W_2$", True),
           (r"$Q=W_1+W_2$", r"Nhiệt năng là phần cơ năng bị hụt, phải trừ, không cộng."),
           (r"$Q=0$ vì năng lượng được bảo toàn", r"Năng lượng toàn phần bảo toàn, nhưng cơ năng thì giảm và phần giảm thành nhiệt.")]),
  buoc("Phần trăm so với cơ năng ở đỉnh", "Nhiệt năng bằng bao nhiêu phần trăm cơ năng ở đỉnh?", 28, "%", 0.3,
       loi=r"Hay chia cho cơ năng ở chân. Đề hỏi phần trăm so với cơ năng ở đỉnh nên chia cho $W_1$.",
       ke=[(r"$\frac{Q}{W_1}\cdot100\ \%$", True),
           (r"$\frac{Q}{W_2}\cdot100\ \%$", r"Đề so với cơ năng ở đỉnh, không phải ở chân."),
           (r"$\frac{W_2}{W_1}\cdot100\ \%$", r"Đó là phần cơ năng còn lại, không phải phần thành nhiệt.")]),
  buoc("Vận tốc nếu không ma sát", "Nếu bỏ qua ma sát, vận tốc ở chân cầu trượt là bao nhiêu?", 7.07, "m/s", 0.05,
       loi=r"Hay dùng cơ năng ở chân (đã bị ma sát lấy bớt). Không ma sát thì toàn bộ cơ năng ở đỉnh thành động năng.",
       ke=[(r"$\frac{1}{2}mv^2=W_1$", True),
           (r"$\frac{1}{2}mv^2=W_2$", r"$W_2$ là cơ năng khi có ma sát; ra lại vận tốc đề đã cho."),
           (r"$\frac{1}{2}mv^2=Q$", r"$Q$ chỉ là phần thành nhiệt, không phải động năng.")]),
  buoc("Kiểm tra")]),
]

# ───────────── Ghi JSON ─────────────
d = {"lesson_id": 130, "lesson_title": "Bài 3. Cơ năng", "generated_at": "2026-10-12",
     "review": {"checked": True, "checked_at": "2026-10-12", "notes": "Soạn 12/10/2026 (chặng 3). Kiểm chéo kiem-code 12/10/2026: không lỗi chặn, đáp số đúng; đã sửa nhãn a)–d), đáp án nhiễu dạng 3. Chưa đối chiếu ngân hàng câu hỏi (topic 76/77, lesson_id đang null)."},
     "dang_bai": [dict(form="bai_tap", solution_html="", **x) for x in DE]}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
assert all(len(s["buoc"]) == SOLS[i].count('class="bt-step"') for i, s in enumerate(STEPS))
inject(J, BUILD, ANALYSIS, SOLS, STEPS)

raw = open(J, encoding="utf8").read()
assert not _re.search(r"\\u000[0-8bcef]|\\t", raw.replace("\\\\t", "")), "ký tự điều khiển trong JSON"
assert "marker-end" not in raw
for q in json.load(open(J))["dang_bai"]:
    for f in ("problem_html", "analysis_html", "solution_html"):
        h_ = _re.sub(r"<svg.*?</svg>", "", q[f], flags=_re.S)
        ms = _re.findall(r"\$\$(.+?)\$\$", h_, flags=_re.S)
        ms += _re.findall(r"\$([^$]+)\$", _re.sub(r"\$\$.+?\$\$", "", h_, flags=_re.S))
        for m in ms:
            assert "<" not in m and ">" not in m, (f, m)
    assert len(_re.findall(r"<svg", q["problem_html"])) == 1
    for s_ in _re.findall(r"<svg.*?</svg>", q["problem_html"] + q["analysis_html"], flags=_re.S):
        assert len(s_) < 7000, len(s_)
        assert not _re.search(r'font-size="(1[0-3]|[0-9])"', s_), "chữ SVG < 14px"
print("xong 130.json")
