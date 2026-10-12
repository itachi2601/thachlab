"""Bài tập mẫu bài 83 — Bài 5. Khúc xạ ánh sáng (KHTN 9). Dựng 5 dạng + hình + lời giải + buoc[] -> 83.json.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-83.py   (idempotent: ghi lại toàn bộ 83.json, review.checked=false)
Danh sách dạng: scripts/data/bai-tap-mau/83.dang.md. Mọi số liệu tính ở đầu file, có assert."""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "83.json")
T80 = "Mô tả hiện tượng khúc xạ, vẽ đường truyền tia sáng"
T81 = "Chiết suất và định luật khúc xạ ánh sáng"
C = 3.0e8
sin = lambda d: math.sin(math.radians(d))
asin = lambda x: math.degrees(math.asin(x))

# ───────────── Số liệu (tính + kiểm) ─────────────
# Dạng 1: rượu n = 1,36 -> v ; nhựa v = 2,0e8 -> n ; so sánh
n_ruou, v_nhua = 1.36, 2.0e8
v_ruou = C / n_ruou
n_nhua = C / v_nhua
assert abs(v_ruou / 1e8 - 2.2059) < 1e-3 and abs(n_nhua - 1.5) < 1e-12 and n_nhua > n_ruou
assert abs(C * n_ruou / 1e8 - 4.08) < 1e-9                              # nhân thay vì chia (4,08) -> vô lí
assert abs(v_nhua / C - n_nhua) > 0.5                                    # n = v/c (0,667)

# Dạng 2: hợp mặt phân cách 40° và 62° -> i = 50°, r = 28°; đảo chiều -> 50°
a_t, a_k = 40, 62
i2, r2 = 90 - a_t, 90 - a_k
assert (i2, r2) == (50, 28) and r2 < i2
assert abs(i2 - a_t) > 5 and abs(r2 - a_k) > 5                           # giữ nguyên số đo của đề -> sai

# Dạng 3: thuỷ tinh 1,5 -> không khí, hợp mặt phân cách 65°
n3, a3 = 1.5, 65
i3 = 90 - a3
sr3 = n3 * sin(i3)
r3 = asin(sr3)
D3 = r3 - i3
assert i3 == 25 and abs(sr3 - 0.634) < 5e-4 and abs(r3 - 39.34) < 0.01 and abs(D3 - 14.34) < 0.01
assert abs(asin(sin(i3) / n3) - r3) > 10                                  # đặt n nhầm phía (16,4°)
assert abs(i3 / n3 - r3) > 10 and abs(a3 - r3) > 10                       # chia góc cho n (16,7°) · lấy 65° làm góc tới
assert n3 * sin(a3) > 1                                                   # nếu lấy 65° làm góc tới thì sin r > 1: vô lí
assert abs(abs(a3 - r3) - D3) > 5                                         # trừ góc khác gốc
assert abs((i3 + r3) - D3) > 10                                           # cộng thay vì trừ
assert abs(90 - r3 - 50.66) < 0.01                                        # góc hợp mặt phân cách của tia ló

# Dạng 4: không khí -> chất lỏng, hợp mặt chất lỏng 35°, góc giữa tia phản xạ và tia khúc xạ 95°
a4, g4 = 35, 95
i4 = 90 - a4
r4 = 180 - i4 - g4
n4 = sin(i4) / sin(r4)
v4 = C / n4
assert i4 == 55 and r4 == 30 and abs(n4 - 1.6383) < 1e-3 and abs(v4 / 1e8 - 1.8312) < 1e-3
assert round(n4, 2) == 1.64 and round(C / 1.64 / 1e8, 2) == 1.83
assert g4 - i4 == 40 and 90 - i4 == 35 and abs(sin(r4) / sin(i4) - n4) > 0.5   # r=95-i (40°) · r=90-i (35°) · lật tỉ số
assert abs(sin(35) / sin(30) - n4) > 0.3 and abs(i4 / r4 - n4) > 0.1             # lấy 35° làm góc tới · tỉ số góc (1,83)
assert abs(C * n4 / 1e8 - v4 / 1e8) > 1

# Dạng 5: không khí -> nước (4/3) -> thuỷ tinh (1,5), mặt song song; trong thuỷ tinh 28° với pháp tuyến
nw, ng, ang_g = 4 / 3, 1.5, 28
srw = ng * sin(ang_g) / nw
rw = asin(srw)
si5 = nw * srw
i5 = asin(si5)
assert abs(srw - 0.5282) < 1e-3 and abs(rw - 31.88) < 0.01 and abs(si5 - 0.7042) < 1e-3 and abs(i5 - 44.77) < 0.01
assert abs(si5 - ng * sin(ang_g)) < 1e-12                                 # nước triệt tiêu
assert abs(asin(nw * sin(ang_g)) - i5) > 5 and abs(asin(ng * sin(rw)) - i5) > 5   # 38,7° · 52,4°
assert abs(asin(si5 / ng) - ang_g) < 1e-9                                  # rút nước: vẫn 28°
assert ang_g < rw < i5

# ───────────── Hình: tiện ích ─────────────
def it_(s):
    return f'<tspan font-family="Georgia, \'Times New Roman\', serif" font-style="italic">{s}</tspan>'

def mkP(Ix, Ys, sgn):
    """Điểm cách I một đoạn L theo góc a (độ, hệ toán học, Oy lên); sgn=-1: lật dọc (ánh sáng đi từ dưới lên)."""
    def P(a, L):
        t = math.radians(a)
        return (Ix + L * math.cos(t), Ys - sgn * L * math.sin(t))
    return P

def arcA(P, R, a0, a1, c, sgn, w=2.0, dash=""):
    x0, y0 = P(a0, R); x1, y1 = P(a1, R)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="M{x0:.1f},{y0:.1f} A{R},{R} 0 0 {0 if sgn == 1 else 1} {x1:.1f},{y1:.1f}" fill="none" stroke="{c}" stroke-width="{w}"{d}/>'

def tag(P, a, R, s, c, size=16, dx=0, dy=5):
    x, y = P(a, R)
    return lbl(x + dx, y + dy, s, c, size, "middle", "700")

def pulse(pts, ts, T, dur, col=GRN, hide_until=None):
    """Chấm sáng chạy qua các điểm pts tại các thời điểm tuyệt đối ts (0 … T); MỘT lần khi bấm (begin=indefinite, freeze)."""
    pts = list(pts); ts = list(ts)
    if ts[-1] < T - 1e-9:
        pts.append(pts[-1]); ts.append(T)
    kt = ";".join(f"{t / T:.4f}" for t in ts)
    def anim(attr, k):
        return f'<animate attributeName="{attr}" values="{";".join(f"{p[k]:.1f}" for p in pts)}" keyTimes="{kt}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'
    op = ""
    extra = ""
    if hide_until is not None:
        op = ' opacity="0"'
        extra = f'<animate attributeName="opacity" values="0;1" keyTimes="0;{hide_until / T:.4f}" calcMode="discrete" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'
    return (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="5.5" fill="{col}" stroke="currentColor" stroke-width="1.4"{op}>'
            + anim("cx", 0) + anim("cy", 1) + extra + '</circle>')

VBS = "0 0 420 280"
SHADE = "rgba(56,189,248,.10)"

def scene(i, r, sgn=1, Ix=210, Ys=140, Lin=118, Lout=118, show_inc=True, show_ref=True, refl=False,
          lab_i="", lab_r="", lab_sf_i="", lab_sf_r="", lab_gap="", upper_txt="", lower_txt="", run=None, adj=None):
    """Mặt phân cách ngang tại Ys, điểm tới I=(Ix,Ys). Môi trường phía dưới được tô nền.
    sgn=1: ánh sáng đi từ trên xuống; sgn=-1: từ dưới lên. run=(n1,n2): thêm chấm sáng chạy (tốc độ tỉ lệ 1/n)."""
    adj = adj or {}
    P = mkP(Ix, Ys, sgn)
    b = f'<rect x="10" y="{Ys}" width="400" height="{280 - 10 - Ys}" fill="{SHADE}"/>'
    b += seg(10, Ys, 410, Ys, "currentColor", 2.4)
    b += seg(*P(90, 92), *P(-90, 92), "currentColor", 1.6, "5 4")
    b += lbl(P(90, 92)[0] + 8, P(90, 92)[1] + (6 if sgn == 1 else -2), "pháp tuyến", "currentColor", 12, "start", "600")
    S = P(90 + i, Lin); E = P(-90 + r, Lout); Rf = P(90 - i, Lin)
    if show_inc: b += arrow("", "r", round(S[0], 1), round(S[1], 1), Ix, Ys, 2.6)
    if show_ref: b += arrow("", "b", Ix, Ys, round(E[0], 1), round(E[1], 1), 2.6)
    if refl:     b += arrow("", "o", Ix, Ys, round(Rf[0], 1), round(Rf[1], 1), 2.2)
    b += dot(Ix, Ys, 4.5)
    if lab_i:
        b += arcA(P, 34, 90, 90 + i, RED, sgn) + tag(P, 90 + i / 2, adj.get("i", (52, 0, 15))[0], lab_i, RED, adj.get("i", (52, 0, 15))[2], dx=adj.get("i", (52, 0, 15))[1])
    if lab_r:
        b += arcA(P, 34, -90, -90 + r, BLUE, sgn) + tag(P, -90 + r / 2, adj.get("r", (52, 0, 15))[0], lab_r, BLUE, adj.get("r", (52, 0, 15))[2], dx=adj.get("r", (52, 0, 15))[1])
    if lab_sf_i:
        b += arcA(P, 66, 90 + i, 180, RED, sgn, 1.8, "4 3") + tag(P, (270 + i) / 2, 86, lab_sf_i, RED, 15)
    if lab_sf_r:
        b += arcA(P, 66, -90 + r, 0, BLUE, sgn, 1.8, "4 3") + tag(P, (-90 + r) / 2, 86, lab_sf_r, BLUE, 15)
    if lab_gap:
        b += arcA(P, 100, -90 + r, 90 - i, ORG, sgn, 1.8) + tag(P, (r - i) / 2, 116, lab_gap, ORG, 15, dx=8)
    if upper_txt: b += lbl(16, 24, upper_txt, "currentColor", 14, "start", "700")
    if lower_txt: b += lbl(16, 266, lower_txt, "currentColor", 14, "start", "700")
    if run:
        n1, n2 = run
        t1, t2 = Lin * n1, Lout * n2
        tr = Lin * n1
        T = max(t1 + t2, t1 + tr) if refl else t1 + t2
        b += pulse([S, (Ix, Ys), E], [0, t1, t1 + t2], T, 3.6, GRN)
        if refl:
            b += pulse([(Ix, Ys), (Ix, Ys), Rf], [0, t1, t1 + tr], T, 3.6, ORG, hide_until=t1)
    return b

# ───────────── Dạng 1: chiết suất và tốc độ ─────────────
def d1(k):
    if k == 0:
        # hình mẫu: nước (n = 4/3), KHÔNG phải chất trong đề; hai xung đi cùng quãng đường
        b = ""
        for y, txt in ((70, "Không khí"), (150, "Nước (hình mẫu)")):
            b += f'<rect x="40" y="{y - 26}" width="340" height="52" rx="6" fill="{SHADE if y > 100 else "none"}" stroke="currentColor" stroke-width="1.6"/>'
            b += lbl(48, y - 32, txt, "currentColor", 13, "start", "700")
        b += seg(60, 36, 60, 184, "currentColor", 1.4, "5 4") + seg(360, 36, 360, 184, "currentColor", 1.4, "5 4")
        b += lbl(60, 204, "xuất phát", "currentColor", 13, "middle", "600") + lbl(360, 204, "đích", "currentColor", 13, "middle", "600")
        n_mau = 4 / 3
        b += (f'<circle cx="60" cy="70" r="6" fill="{GRN}" stroke="currentColor" stroke-width="1.4">{smil("cx", [60, 360], 3.0)}</circle>')
        b += (f'<circle cx="60" cy="150" r="6" fill="{ORG}" stroke="currentColor" stroke-width="1.4">{smil("cx", [60, 360], 3.0 * n_mau)}</circle>')
        return fig("d1-0", "0 0 420 216", "Hai xung sáng xuất phát cùng lúc, cùng đi một quãng đường: xung trong không khí tới đích trước, xung trong môi trường mẫu tới sau", b,
                   "Mô phỏng (bấm Chạy mô phỏng): hai xung sáng xuất phát cùng lúc, đi cùng quãng đường.<br>Môi trường mẫu là nước, không phải chất trong đề.<br>Xung trong nước chạy chậm đi $\\dfrac{4}{3}$ lần so với trong không khí; tốc độ vẽ chỉ để minh hoạ.")
    b = ""
    rows = [(46, "Không khí (chân không)", r"c = 3·10⁸ m/s", "currentColor"),
            (112, "Rượu etilic", "n = 1,36;  v = ?", BLUE),
            (178, "Khối nhựa", "v = 2,0·10⁸ m/s;  n = ?", ORG)]
    for y, name, val, col in rows:
        b += f'<rect x="16" y="{y - 24}" width="388" height="48" rx="6" fill="none" stroke="{col}" stroke-width="1.8"/>'
        b += lbl(28, y - 4, name, "currentColor", 15, "start", "700") + lbl(28, y + 16, val, col, 15, "start", "700")
    return fig("d1-2", "0 0 420 212", "Ba môi trường và dữ kiện của đề: chân không có c, rượu có chiết suất, nhựa có tốc độ ánh sáng", b,
               "Dữ kiện: mỗi môi trường biết một trong hai đại lượng n hoặc v, cần tìm đại lượng còn lại.")

# ───────────── Dạng 2: đọc hình khúc xạ ─────────────
def d2(k):
    if k == 0:
        # hình mẫu KHÁC số đề: không khí (n=1) -> môi trường n=1,5, tia tới hợp mặt phân cách 30° (i = 60°)
        i_m = 60.0; r_m = asin(sin(i_m) / 1.5)
        b = scene(i_m, r_m, 1, refl=False, run=(1.0, 1.5), upper_txt="Môi trường (1)", lower_txt="Môi trường (2)")
        return fig("d2-0", VBS, "Một tia sáng đi từ môi trường trên xuống môi trường dưới qua mặt phân cách ngang và bị gãy khúc tại điểm tới", b,
                   "Mô phỏng (bấm Chạy mô phỏng): hình mẫu, số liệu khác đề.<br>Chấm sáng chạy chậm lại khi vào môi trường (2).")
    b = scene(r_to_i(a_t), r_to_i(a_k), 1, Ix=210, lab_sf_i="40°", lab_sf_r="62°", upper_txt="Môi trường (1)", lower_txt="Môi trường (2)",
              lab_i="i = ?", lab_r="r = ?", adj={"r": (52, -32, 15)})
    return fig("d2-2", VBS, "Tia tới hợp mặt phân cách góc 40 độ, tia khúc xạ hợp mặt phân cách góc 62 độ; góc tới và góc khúc xạ chưa biết", b,
               "Dữ kiện: hai góc đề cho đo từ mặt phân cách (nét đứt).<br>Góc tới i và góc khúc xạ r đo từ pháp tuyến.")

def r_to_i(a):  # từ góc hợp mặt phân cách sang góc với pháp tuyến (chỉ để dựng hình)
    return 90 - a

# ───────────── Dạng 3: thuỷ tinh -> không khí ─────────────
def d3(k):
    if k == 0:
        # hình mẫu KHÁC số đề: thuỷ tinh n=1,5 -> không khí, hợp mặt phân cách 75° (i = 15°)
        i_m = 15.0; r_m = asin(1.5 * sin(i_m))
        b = scene(i_m, r_m, -1, Ix=210, Ys=140, run=(1.5, 1.0), upper_txt="Không khí", lower_txt="Thuỷ tinh (n = 1,5)")
        return fig("d3-0", VBS, "Tia sáng đi từ khối thuỷ tinh ở dưới ra không khí ở trên qua mặt phân cách ngang và bị gãy khúc", b,
                   "Mô phỏng (bấm Chạy mô phỏng): hình mẫu, số liệu khác đề.<br>Chấm sáng chạy nhanh lên khi ra không khí.")
    b = scene(i3, 20, -1, Ix=210, Ys=140, show_ref=False, lab_i="i = ?", lab_sf_i="65°", upper_txt="Không khí", lower_txt="Thuỷ tinh (n = 1,5)", adj={"i": (104, 0, 13)})
    b += lbl(300, 62, "tia ló: tự vẽ, tìm r", BLUE, 14, "start", "700")
    return fig("d3-2", VBS, "Tia sáng trong thuỷ tinh hợp mặt phân cách góc 65 độ; góc tới chưa biết; tia ló ra không khí cần tìm", b,
               "Dữ kiện: góc đề cho đo từ mặt phân cách (nét đứt).<br>Góc tới i đo từ pháp tuyến.<br>Tia ló và góc khúc xạ r là điều cần tìm.")

# ───────────── Dạng 4: phản xạ + khúc xạ ─────────────
def d4(k):
    if k == 0:
        # hình mẫu KHÁC số đề: không khí -> n = 1,5, hợp mặt phân cách 40° (i = 50°), có tia phản xạ
        i_m = 50.0; r_m = asin(sin(i_m) / 1.5)
        b = scene(i_m, r_m, 1, refl=True, run=(1.0, 1.5), upper_txt="Không khí", lower_txt="Chất lỏng (hình mẫu)")
        return fig("d4-0", VBS, "Tia laser tới mặt chất lỏng: một phần phản xạ lên trên, một phần khúc xạ xuống dưới", b,
                   "Mô phỏng (bấm Chạy mô phỏng): hình mẫu, số liệu khác đề, không có điều kiện góc giữa hai tia.<br>Chấm xanh lá đi vào chất lỏng, chấm cam phản xạ.")
    b = scene(i4, r4, 1, refl=True, lab_sf_i="35°", lab_i="i", lab_gap="95°", upper_txt="Không khí", lower_txt="Chất lỏng")
    return fig("d4-2", VBS, "Tia tới hợp mặt chất lỏng góc 35 độ, có tia phản xạ và tia khúc xạ; góc giữa hai tia này là 95 độ", b,
               "Dữ kiện: góc 35° đo từ mặt phân cách, góc 95° giữa tia phản xạ (cam) và tia khúc xạ (xanh).<br>Hình minh hoạ.")

# ───────────── Dạng 5: nhiều lớp song song ─────────────
Y1, Y2, Y3 = 108, 186, 268
def layer_bg():
    b = f'<rect x="10" y="{Y1}" width="400" height="{Y2 - Y1}" fill="{SHADE}"/>'
    b += f'<rect x="10" y="{Y2}" width="400" height="{Y3 - Y2}" fill="rgba(56,189,248,.24)"/>'
    b += seg(10, Y1, 410, Y1, "currentColor", 2.2) + seg(10, Y2, 410, Y2, "currentColor", 2.2) + seg(10, Y3, 410, Y3, "currentColor", 2.2)
    return b

def d5(k):
    if k == 0:
        # hình mẫu KHÁC số đề: tia tới từ không khí i = 60°
        i_m = 60.0; r1 = asin(sin(i_m) / nw); r2 = asin(sin(i_m) / ng)
        xI1 = 190.0
        S = (xI1 - (Y1 - 22) * math.tan(math.radians(i_m)), 22.0)
        I1 = (xI1, float(Y1)); I2 = (xI1 + (Y2 - Y1) * math.tan(math.radians(r1)), float(Y2))
        E = (I2[0] + (Y3 - Y2) * math.tan(math.radians(r2)), float(Y3))
        b = layer_bg()
        for (x, y) in (I1, I2):
            b += seg(x, y - 40, x, y + 40, "currentColor", 1.4, "5 4")
        b += arrow("", "r", round(S[0], 1), round(S[1], 1), round(I1[0], 1), round(I1[1], 1), 2.6)
        b += arrow("", "b", round(I1[0], 1), round(I1[1], 1), round(I2[0], 1), round(I2[1], 1), 2.6)
        b += arrow("", "o", round(I2[0], 1), round(I2[1], 1), round(E[0], 1), round(E[1], 1), 2.6)
        b += dot(*I1, 4.5) + dot(*I2, 4.5)
        b += lbl(330, 24, "Không khí", "currentColor", 13, "start", "700") + lbl(16, Y1 + 20, "Nước (n = 4/3)", "currentColor", 13, "start", "700") + lbl(16, Y2 + 20, "Thuỷ tinh (n = 1,5)", "currentColor", 13, "start", "700")
        lens = [math.dist(S, I1) * 1.0, math.dist(I1, I2) * nw, math.dist(I2, E) * ng]
        T = lens[0] + lens[1] + lens[2]
        # độ dài đoạn thật × n cho thời gian (tốc độ tỉ lệ 1/n)
        t0 = math.dist(S, I1) * 1.0; t1_ = t0 + math.dist(I1, I2) * nw; t2_ = t1_ + math.dist(I2, E) * ng
        b += pulse([S, I1, I2, E], [0, t0, t1_, t2_], t2_, 4.2, GRN)
        return fig("d5-0", "0 0 420 280", "Tia sáng đi từ không khí qua lớp nước rồi vào lớp thuỷ tinh, gãy khúc ở hai mặt phân cách song song", b,
                   "Mô phỏng (bấm Chạy mô phỏng): hình mẫu, tia tới từ không khí với góc khác đề.<br>Chấm sáng chạy chậm dần qua từng lớp.")
    xI2 = 210.0
    P = mkP(xI2, float(Y2), 1)
    b = layer_bg()
    b += seg(xI2, Y2 - 62, xI2, Y2 + 70, "currentColor", 1.4, "5 4")
    E = P(-90 + ang_g, 80)
    b += arrow("", "o", xI2, Y2, round(E[0], 1), round(E[1], 1), 2.6) + dot(xI2, Y2, 4.5)
    b += arcA(P, 36, -90, -90 + ang_g, ORG, 1) + tag(P, -90 + ang_g / 2, 56, "28°", ORG, 15, dx=2)
    b += lbl(16, 24, "Không khí", "currentColor", 13, "start", "700") + lbl(16, Y1 + 20, "Nước (n = 4/3)", "currentColor", 13, "start", "700") + lbl(16, Y2 + 20, "Thuỷ tinh (n = 1,5)", "currentColor", 13, "start", "700")
    xI1 = 130.0
    P1 = mkP(xI1, float(Y1), 1)
    b += seg(xI1, Y1 - 45, xI1, Y1 + 35, "currentColor", 1.4, "5 4") + dot(xI1, Y1, 4.5)
    b += arcA(P1, 30, 90, 120, RED, 1, 1.8, "4 3") + tag(P1, 105, 48, "i = ?", RED, 14)
    b += arcA(P, 30, 90, 120, BLUE, 1, 1.8, "4 3") + tag(P, 105, 48, 'r<tspan dy="4" font-size="11">1</tspan> = ?', BLUE, 14)
    return fig("d5-2", "0 0 420 280", "Ba lớp song song: không khí, nước, thuỷ tinh. Chỉ biết tia trong thuỷ tinh hợp pháp tuyến góc 28 độ; hai góc ở trên cần tìm", b,
               "Dữ kiện: chỉ có tia trong thuỷ tinh (cam) với góc 28° so với pháp tuyến.<br>Các mặt phân cách song song nên pháp tuyến song song.<br>Cung nét đứt đánh dấu hai góc cần tìm: i (góc tới ở mặt nước) và r₁ (góc trong nước); số đo chưa biết.")

BUILD = [d1, d2, d3, d4, d5]

# ───────────── Đề ─────────────
DE = [
 dict(label="Dạng 1 · Chiết suất và tốc độ ánh sáng trong môi trường", topic=T81,
      problem_html=r"<p>Lấy tốc độ ánh sáng trong chân không $c = 3 \cdot 10^8\ \text{m/s}$.</p>"
                   r"<ol type=\"a\"><li>Rượu etilic có chiết suất $n = 1{,}36$. Tính tốc độ ánh sáng trong rượu.</li>"
                   r"<li>Trong một khối nhựa trong suốt, ánh sáng truyền với tốc độ $2{,}0 \cdot 10^8\ \text{m/s}$. Tính chiết suất của nhựa.</li>"
                   r"<li>Trong hai môi trường trên, môi trường nào chiết quang hơn?</li></ol>"),
 dict(label="Dạng 2 · Đọc góc trên hình khúc xạ: góc tới, góc khúc xạ, chiều lệch", topic=T80,
      problem_html=r"<p>Tia sáng truyền từ môi trường (1) sang môi trường (2) qua mặt phân cách phẳng nằm ngang như hình. Tia tới hợp với mặt phân cách góc $40^\circ$; tia khúc xạ hợp với mặt phân cách góc $62^\circ$.</p>"
                   r"<ol type=\"a\"><li>Tính góc tới $i$ và góc khúc xạ $r$.</li>"
                   r"<li>Tia khúc xạ lệch lại gần hay ra xa pháp tuyến so với tia tới? Môi trường nào chiết quang hơn?</li>"
                   r"<li>Cho tia sáng đi ngược lại, từ môi trường (2) theo đúng đường của tia khúc xạ. Tia ló ra môi trường (1) hợp với pháp tuyến góc bao nhiêu?</li></ol>"),
 dict(label="Dạng 3 · Tia sáng đi từ thuỷ tinh ra không khí: góc khúc xạ và góc lệch", topic=T81,
      problem_html=r"<p>Một tia sáng truyền trong khối thuỷ tinh có chiết suất $n = 1{,}5$ tới mặt phân cách với không khí. Tia tới hợp với mặt phân cách góc $65^\circ$.</p>"
                   r"<ol type=\"a\"><li>Tính góc tới.</li>"
                   r"<li>Tính góc khúc xạ của tia ló ra không khí.</li>"
                   r"<li>Tính góc lệch $D$ giữa tia ló và phương của tia tới.</li></ol>"),
 dict(label="Dạng 4 · Tia phản xạ và tia khúc xạ: tìm chiết suất và tốc độ ánh sáng", topic=T81,
      problem_html=r"<p>Tia laser truyền trong không khí tới mặt một chất lỏng trong suốt, hợp với mặt chất lỏng góc $35^\circ$. Tia phản xạ và tia khúc xạ hợp nhau góc $95^\circ$. Lấy $c = 3 \cdot 10^8\ \text{m/s}$.</p>"
                   r"<ol type=\"a\"><li>Tính góc tới và góc khúc xạ.</li>"
                   r"<li>Tính chiết suất của chất lỏng.</li>"
                   r"<li>Tính tốc độ ánh sáng trong chất lỏng.</li></ol>"),
 dict(label="Dạng 5 · Nhiều lớp song song: không khí, nước, thuỷ tinh", topic=T81,
      problem_html=r"<p>Chiếu một tia laser từ không khí xuống một bể nước. Đáy bể là một tấm thuỷ tinh phẳng. Các mặt phân cách song song với nhau. Chiết suất của nước là $\dfrac{4}{3}$, của thuỷ tinh là $1{,}5$.</p>"
                   r"<p>Trong tấm thuỷ tinh, tia laser hợp với pháp tuyến góc $28^\circ$.</p>"
                   r"<ol type=\"a\"><li>Trong nước, tia laser hợp với pháp tuyến góc bao nhiêu?</li>"
                   r"<li>Tính góc tới của tia laser ở mặt nước.</li>"
                   r"<li>Rút hết nước, giữ nguyên góc tới ở câu b. Góc khúc xạ trong thuỷ tinh thay đổi thế nào?</li></ol>"),
]
for d_ in DE:
    d_["problem_html"] = d_["problem_html"].replace('\\"', '"')

# ───────────── Phân tích đề ─────────────
ANALYSIS = [
 [(r"&quot;tốc độ ánh sáng trong chân không $c = 3 \cdot 10^8$ m/s&quot;", r"$c = 3\cdot10^8\ \text{m/s}$", r"Chiết suất $n$ so tốc độ trong môi trường với $c$"),
  (r"&quot;Rượu etilic có chiết suất $n = 1{,}36$. Tính tốc độ&quot;", r"$n = 1{,}36$; cần $v$", r"$n=\dfrac{c}{v}$"),
  (r"&quot;khối nhựa … tốc độ $2{,}0 \cdot 10^8$ m/s. Tính chiết suất&quot;", r"$v = 2{,}0\cdot10^8\ \text{m/s}$; cần $n$", r"$n=\dfrac{c}{v}$"),
  (r"&quot;môi trường nào chiết quang hơn&quot;", r"So hai môi trường", r"⚠ Chiết quang hơn là so <strong>chiết suất</strong> $n$ của hai môi trường, không so tốc độ trực tiếp")],
 [(r"&quot;mặt phân cách phẳng nằm ngang … pháp tuyến&quot;", r"Mặt phân cách ngang", r"⚠ $i$ và $r$ đo từ <strong>pháp tuyến</strong>; pháp tuyến vuông góc mặt phân cách"),
  (r"&quot;Tia tới hợp với mặt phân cách góc $40^\circ$&quot;", r"Góc hợp mặt phân cách: $40^\circ$", r"Đây có phải góc tới không? Pháp tuyến tạo với mặt phân cách góc bao nhiêu?"),
  (r"&quot;tia khúc xạ hợp với mặt phân cách góc $62^\circ$&quot;", r"Góc hợp mặt phân cách: $62^\circ$", r"Làm tương tự cho tia khúc xạ"),
  (r"&quot;Tính góc tới $i$ và góc khúc xạ $r$&quot;", r"Cần $i$, $r$", r"Hai góc đo từ pháp tuyến"),
  (r"&quot;lệch lại gần hay ra xa pháp tuyến … môi trường nào chiết quang hơn&quot;", r"So $r$ với $i$", r"Đối chiếu bảng hai trường hợp ở mục định luật khúc xạ"),
  (r"&quot;Cho tia sáng đi ngược lại … theo đúng đường của tia khúc xạ&quot;", r"Đảo chiều truyền", r"Tính thuận nghịch của đường truyền ánh sáng")],
 [(r"&quot;khối thuỷ tinh có chiết suất $n = 1{,}5$ tới mặt phân cách với không khí&quot;", r"Tia tới trong thuỷ tinh: $n_1 = 1{,}5$; tia khúc xạ trong không khí: $n_2 = 1$", r"⚠ $n_1$ là chiết suất của môi trường chứa <strong>tia tới</strong>, $n_2$ của môi trường chứa tia khúc xạ"),
  (r"&quot;Tia tới hợp với mặt phân cách góc $65^\circ$&quot;", r"Góc hợp mặt phân cách: $65^\circ$", r"⚠ Chưa phải góc tới: đo góc từ pháp tuyến"),
  (r"&quot;Tính góc tới&quot;", r"Cần $i$", r"Pháp tuyến vuông góc mặt phân cách"),
  (r"&quot;Tính góc khúc xạ của tia ló&quot;", r"Cần $r$", r"$n_1\sin i=n_2\sin r$; rút $\sin r$ trước rồi mới tìm góc"),
  (r"&quot;góc lệch $D$ giữa tia ló và phương của tia tới&quot;", r"Cần $D$", r"$D=|i-r|$")],
 [(r"&quot;truyền trong không khí tới mặt một chất lỏng&quot;", r"$n_1 = 1$; chất lỏng: $n_2$ chưa biết", r"⚠ Các góc trong định luật đều đo từ <strong>pháp tuyến</strong>"),
  (r"&quot;hợp với mặt chất lỏng góc $35^\circ$&quot;", r"Góc hợp mặt phân cách: $35^\circ$", r"Đổi sang góc với pháp tuyến"),
  (r"&quot;Tia phản xạ và tia khúc xạ hợp nhau góc $95^\circ$&quot;", r"Góc giữa hai tia: $95^\circ$", r"Góc phản xạ so với góc tới; hai tia nằm hai bên pháp tuyến"),
  (r"&quot;Tính góc tới và góc khúc xạ&quot;", r"Cần $i$, $r$", r"Quan hệ giữa $i'$, $r$ và góc giữa hai tia"),
  (r"&quot;Tính chiết suất&quot;", r"Cần $n_2$", r"$n_1\sin i=n_2\sin r$"),
  (r"&quot;Tính tốc độ ánh sáng trong chất lỏng&quot;", r"$c = 3\cdot10^8\ \text{m/s}$; cần $v$", r"$n=\dfrac{c}{v}$")],
 [(r"&quot;Các mặt phân cách song song với nhau&quot;", r"Hai mặt phân cách song song", r"⚠ Điều kiện: các pháp tuyến cũng song song nhau"),
  (r"&quot;nước $\dfrac{4}{3}$, thuỷ tinh $1{,}5$&quot;", r"$n_{\text{nước}}=\dfrac43$; $n_{\text{kính}}=1{,}5$; không khí $n=1$", r"Mỗi mặt phân cách có một cặp $n_1$, $n_2$ riêng"),
  (r"&quot;Trong tấm thuỷ tinh, tia laser hợp với pháp tuyến góc $28^\circ$&quot;", r"Góc trong thuỷ tinh: $28^\circ$", r"Đây là góc khúc xạ hay góc tới, ở mặt phân cách nào?"),
  (r"&quot;Trong nước, tia laser hợp với pháp tuyến góc bao nhiêu&quot;", r"Cần góc trong nước", r"$n_1\sin i=n_2\sin r$ ở mặt nước–thuỷ tinh"),
  (r"&quot;Tính góc tới của tia laser ở mặt nước&quot;", r"Cần $i$ ở mặt không khí–nước", r"Tia khúc xạ ở mặt này nằm trong môi trường nào?"),
  (r"&quot;Rút hết nước, giữ nguyên góc tới ở câu b&quot;", r"Còn một mặt không khí–thuỷ tinh", r"$n_1\sin i=n_2\sin r$ cho mặt phân cách còn lại")],
]

# ───────────── Lời giải ─────────────
R1 = [r"<strong>Khái niệm:</strong> chiết suất $n$ cho biết môi trường làm ánh sáng chậm đi bao nhiêu lần so với trong chân không.",
      r"Công thức: $n=\dfrac{c}{v}$, suy ra $v=\dfrac{c}{n}$.",
      r"Đơn vị: $c$ và $v$ cùng m/s nên $n$ không có đơn vị; $c=3\cdot10^8\ \text{m/s}$.",
      r"⚠ <strong>Điều kiện:</strong> so độ chiết quang là so $n$ của hai môi trường; $n$ lớn hơn thì chiết quang hơn."]
R2 = [r"<strong>Khái niệm:</strong> góc tới $i$ và góc khúc xạ $r$ đều đo từ <strong>pháp tuyến</strong>, vuông góc với mặt phân cách.",
      r"<strong>Định luật:</strong> tia tới và tia khúc xạ nằm hai bên pháp tuyến, trong cùng một mặt phẳng.",
      r"Vào môi trường chiết quang hơn: $r\lt i$. Vào môi trường kém chiết quang hơn: $r\gt i$.",
      r"Tính thuận nghịch: ánh sáng đi ngược lại thì đi đúng đường cũ.",
      r"⚠ <strong>Điều kiện:</strong> đề cho góc hợp với <strong>mặt phân cách</strong> thì đổi sang góc với pháp tuyến trước."]
R3 = [r"<strong>Khái niệm:</strong> tia sáng gãy khúc khi truyền xiên qua mặt phân cách; $i$, $r$ đo từ pháp tuyến.",
      r"<strong>Định luật:</strong> $n_1\sin i=n_2\sin r$.",
      r"$n_1$: chiết suất môi trường chứa tia tới; $n_2$: môi trường chứa tia khúc xạ.",
      r"Góc lệch giữa tia khúc xạ và phương tia tới: $D=|i-r|$.",
      r"⚠ <strong>Điều kiện:</strong> đổi góc hợp mặt phân cách sang góc tới; rút $\sin r$ trước rồi mới bấm $\sin^{-1}$ (máy để chế độ độ)."]
R4 = [r"<strong>Định luật phản xạ:</strong> góc phản xạ bằng góc tới, $i'=i$; tia tới và tia phản xạ nằm hai bên pháp tuyến.",
      r"<strong>Định luật khúc xạ:</strong> $n_1\sin i=n_2\sin r$.",
      r"Chiết suất: $n=\dfrac{c}{v}$, $c=3\cdot10^8\ \text{m/s}$.",
      r"⚠ <strong>Điều kiện:</strong> các góc đo từ pháp tuyến; tia tới ở không khí nên $n_1=1$."]
R5 = [r"<strong>Định luật khúc xạ:</strong> $n_1\sin i=n_2\sin r$ ở mỗi mặt phân cách.",
      r"Tia khúc xạ ở mặt phân cách này là tia tới của mặt phân cách kế tiếp.",
      r"⚠ <strong>Điều kiện:</strong> các mặt phân cách song song nên các pháp tuyến song song nhau."]

SOLS = [
 sol(R1, [
  ("Tốc độ ánh sáng trong rượu", [P("Từ $n=\\dfrac{c}{v}$:"), M(r"v=\dfrac{c}{n}"), M(r"v=\dfrac{3\cdot10^8}{1{,}36}"), A(r"v\approx2{,}21\cdot10^8\ \text{m/s}")]),
  ("Chiết suất của nhựa", [M(r"n=\dfrac{c}{v}"), M(r"n=\dfrac{3\cdot10^8}{2{,}0\cdot10^8}"), A(r"n=1{,}5")]),
  ("Môi trường chiết quang hơn", [M(r"n_{\text{nhựa}}=1{,}5\gt n_{\text{rượu}}=1{,}36"), A(r"T:Nhựa chiết quang hơn rượu."), P("Ánh sáng trong nhựa chậm hơn: $2{,}0\\cdot10^8$ so với $2{,}21\\cdot10^8$ m/s.")]),
  ("Kiểm tra", [P("Cả hai đều có $n\\gt1$ và $v\\lt c$: hợp lí."), P("Đơn vị: m/s chia m/s nên $n$ không có đơn vị ✓")])],
  [r"a) $v\approx2{,}21\cdot10^8\ \text{m/s}$", r"b) $n=1{,}5$", r"c) Nhựa chiết quang hơn"],
  "Nhận dạng: đề cho <strong>chiết suất</strong> hoặc <strong>tốc độ ánh sáng trong môi trường</strong> → $n=\\dfrac{c}{v}$; $n$ lớn hơn thì chiết quang hơn."),
 sol(R2, [
  ("Góc tới", [P("Pháp tuyến vuông góc mặt phân cách, nên góc tới cộng góc hợp mặt phân cách bằng $90^\\circ$:"), M(r"i=90^\circ-40^\circ"), A(r"i=50^\circ")]),
  ("Góc khúc xạ", [P("Làm tương tự cho tia khúc xạ:"), M(r"r=90^\circ-62^\circ"), A(r"r=28^\circ")]),
  ("Chiều lệch và môi trường chiết quang hơn", [P("So sánh: $r=28^\\circ\\lt i=50^\\circ$."), A(r"T:Tia khúc xạ lệch <strong>lại gần</strong> pháp tuyến; môi trường (2) chiết quang hơn."), P("Khớp bảng: vào môi trường chiết quang hơn thì $r\\lt i$.")]),
  ("Đảo chiều tia sáng", [P("Ánh sáng đi ngược lại thì vẫn đi đúng đường cũ (tính thuận nghịch)."), P("Tia tới lúc này nằm trong môi trường (2), tia ló trùng với tia tới ban đầu ở môi trường (1)."), A(r"i_{\text{ló}}=50^\circ")]),
  ("Kiểm tra", [P("Đi từ (2) sang (1) là ra môi trường kém chiết quang hơn nên góc ló lớn hơn góc vào."), M(r"50^\circ\gt28^\circ\ \checkmark")])],
  [r"a) $i=50^\circ$; $r=28^\circ$", r"b) Lệch lại gần pháp tuyến; môi trường (2) chiết quang hơn", r"c) $50^\circ$"],
  "Nhận dạng: đề cho <strong>góc hợp với mặt phân cách</strong> → lấy $90^\\circ$ trừ đi để được góc với pháp tuyến; so $r$ với $i$ để biết môi trường nào chiết quang hơn."),
 sol(R3, [
  ("Góc tới", [P("Góc hợp mặt phân cách là $65^\\circ$, nên góc với pháp tuyến:"), M(r"i=90^\circ-65^\circ"), A(r"i=25^\circ")]),
  ("Tính sin của góc khúc xạ", [P("Tia tới ở trong thuỷ tinh: $n_1=1{,}5$. Tia khúc xạ ở không khí: $n_2=1$."), M(r"n_1\sin i=n_2\sin r"), M(r"\sin r=1{,}5\cdot\sin25^\circ"), A(r"\sin r\approx0{,}634")]),
  ("Góc khúc xạ", [P("Bấm $\\sin^{-1}$ (máy ở chế độ độ):"), M(r"r=\sin^{-1}(0{,}634)"), A(r"r\approx39{,}3^\circ")]),
  ("Góc lệch", [M(r"D=|i-r|=|25^\circ-39{,}3^\circ|"), A(r"D\approx14{,}3^\circ")]),
  ("Kiểm tra", [P("Ra không khí (kém chiết quang hơn) nên $r\\gt i$:"), M(r"39{,}3^\circ\gt25^\circ\ \checkmark"), P("Tia ló hợp mặt phân cách $90^\\circ-39{,}3^\\circ=50{,}7^\\circ$, nghiêng thêm về phía mặt phân cách so với tia tới.")])],
  [r"a) $i=25^\circ$", r"b) $r\approx39{,}3^\circ$", r"c) $D\approx14{,}3^\circ$"],
  "Nhận dạng: tia <strong>đi ra từ môi trường có $n$</strong> và đề cho <strong>góc hợp mặt phân cách</strong> → đổi sang $i$, đặt đúng $n_1$ (môi trường chứa tia tới), rồi bấm $\\sin^{-1}$."),
 sol(R4, [
  ("Góc tới", [P("Góc hợp mặt chất lỏng là $35^\\circ$:"), M(r"i=90^\circ-35^\circ"), A(r"i=55^\circ")]),
  ("Góc khúc xạ", [P("Góc phản xạ: $i'=i=55^\\circ$."), P("Hai tia nằm hai bên pháp tuyến, nên góc giữa chúng là $180^\\circ-i'-r$:"), M(r"180^\circ-55^\circ-r=95^\circ"), A(r"r=30^\circ")]),
  ("Chiết suất", [P("Tia tới ở không khí, $n_1=1$:"), M(r"n_1\sin i=n_2\sin r"), M(r"n=\dfrac{\sin55^\circ}{\sin30^\circ}=\dfrac{0{,}819}{0{,}5}"), A(r"n\approx1{,}64")]),
  ("Tốc độ ánh sáng trong chất lỏng", [M(r"v=\dfrac{c}{n}"), M(r"v=\dfrac{3\cdot10^8}{1{,}64}"), A(r"v\approx1{,}83\cdot10^8\ \text{m/s}")]),
  ("Kiểm tra", [P("Vào môi trường chiết quang hơn nên $r\\lt i$: $30^\\circ\\lt55^\\circ$ ✓"), P("$n\\gt1$ và $v\\lt c$: hợp lí.")])],
  [r"a) $i=55^\circ$; $r=30^\circ$", r"b) $n\approx1{,}64$", r"c) $v\approx1{,}83\cdot10^8\ \text{m/s}$"],
  "Nhận dạng: đề cho <strong>tia phản xạ</strong> cùng <strong>tia khúc xạ</strong> → $i'=i$, rồi $180^\\circ-i'-r$ là góc giữa hai tia; có $i$, $r$ thì tìm $n$ và $v$."),
 sol(R5, [
  ("Góc trong nước", [P("Mặt nước–thuỷ tinh: tia tới nằm trong nước, góc $r_1$ (cần tìm); tia khúc xạ nằm trong thuỷ tinh, góc $28^\\circ$."), M(r"\dfrac43\sin r_1=1{,}5\sin28^\circ"), M(r"\sin r_1=\dfrac{1{,}5\cdot\sin28^\circ}{4/3}\approx0{,}528"), A(r"r_1\approx31{,}9^\circ")]),
  ("Góc tới ở mặt nước", [P("Mặt không khí–nước: tia khúc xạ nằm trong nước, góc $r_1$ (pháp tuyến song song nên cùng góc với tia tới của mặt dưới)."), M(r"1\cdot\sin i=\dfrac43\sin r_1"), M(r"\sin i=\dfrac43\cdot0{,}528\approx0{,}704"), A(r"i\approx44{,}8^\circ")]),
  ("Rút hết nước", [P("Còn một mặt không khí–thuỷ tinh với đúng góc tới $i$ ở câu b:"), M(r"\sin r_2=\dfrac{\sin i}{1{,}5}=\dfrac{0{,}704}{1{,}5}\approx0{,}469"), P("Chiết suất nước triệt tiêu giữa hai lần khúc xạ:"), M(r"\sin i=\dfrac43\sin r_1=1{,}5\sin28^\circ"), A(r"T:Góc khúc xạ trong thuỷ tinh <strong>không đổi</strong>, vẫn $28^\circ$.")]),
  ("Kiểm tra", [P("Cách khác, bỏ qua lớp nước:"), M(r"\sin i=1{,}5\sin28^\circ\approx0{,}704\ \checkmark"), P("Mỗi lần vào môi trường chiết quang hơn, tia lại gần pháp tuyến hơn:"), M(r"28^\circ\lt31{,}9^\circ\lt44{,}8^\circ\ \checkmark")])],
  [r"a) $r_1\approx31{,}9^\circ$", r"b) $i\approx44{,}8^\circ$", r"c) Không đổi, vẫn $28^\circ$"],
  "Nhận dạng: <strong>nhiều lớp song song</strong> → áp dụng định luật từng mặt, góc khúc xạ lớp trên là góc tới lớp dưới; chiết suất lớp giữa không ảnh hưởng góc ngoài cùng."),
]

# ───────────── Tự giải từng bước ─────────────
STEPS = [
 dict(nhan_dang=r"Thấy <b>chiết suất</b> hoặc <b>tốc độ ánh sáng trong môi trường</b> → nghĩ tới $n=\dfrac{c}{v}$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Tốc độ ánh sáng trong rượu", r"Tốc độ ánh sáng trong rượu bằng bao nhiêu (đơn vị $10^8\ \text{m/s}$)?", 2.21, "·10⁸ m/s", 0.02,
       loi=r"Hay nhân $c$ với $n$. Ánh sáng trong môi trường luôn chậm hơn trong chân không, nên $v$ phải nhỏ hơn $c$."),
  buoc("Chiết suất của nhựa", "Chiết suất của nhựa bằng bao nhiêu?", 1.5, None, 0.03,
       loi=r"Hay lật tỉ số thành $\dfrac{v}{c}$. Chiết suất không bao giờ nhỏ hơn $1$.",
       ke=[(r"$n=\dfrac{c}{v}$", True),
           (r"$n=\dfrac{v}{c}$", r"Lật ngược tỉ số: $v\le c$ nên $\dfrac{v}{c}\le1$, mà chiết suất luôn từ $1$ trở lên."),
           (r"$n=c\cdot v$", r"Tích hai tốc độ không phải đại lượng không có đơn vị như chiết suất.")]),
  buoc("Môi trường chiết quang hơn", "Môi trường nào chiết quang hơn?",
       loi=r"Hay so tốc độ rồi chọn môi trường có tốc độ lớn hơn. Chiết quang hơn là chiết suất lớn hơn.",
       lua_chon=[("Nhựa", True),
                 ("Rượu", r"Tốc độ lớn hơn nghĩa là môi trường làm ánh sáng chậm ít hơn, tức chiết suất nhỏ hơn."),
                 ("Bằng nhau, vì cả hai đều trong suốt", r"Trong suốt chỉ cho ánh sáng đi qua được; độ chiết quang do chiết suất quyết định.")],
       ke=[(r"So hai chiết suất vừa có", True),
           (r"So khối lượng riêng của hai chất", r"Độ chiết quang do chiết suất quyết định, không phải khối lượng riêng."),
           (r"Môi trường có tốc độ ánh sáng lớn hơn thì chiết quang hơn", r"Ngược lại: tốc độ lớn hơn thì chiết suất nhỏ hơn.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>góc hợp với mặt phân cách</b> → đổi sang <b>góc với pháp tuyến</b> trước, rồi so $r$ với $i$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Góc tới", "Góc tới $i$ bằng bao nhiêu độ?", 50, "°", 0.5,
       loi=r"Hay lấy luôn số đo của đề làm góc tới. Góc tới đo từ pháp tuyến, không đo từ mặt phân cách."),
  buoc("Góc khúc xạ", "Góc khúc xạ $r$ bằng bao nhiêu độ?", 28, "°", 0.5,
       loi=r"Đổi sang pháp tuyến cho tia tới nhưng để nguyên số đo của tia khúc xạ.",
       ke=[(r"Cũng đổi sang pháp tuyến: $r=90^\circ-$ góc hợp mặt phân cách", True),
           (r"Giữ nguyên số đo của đề: góc khúc xạ là góc hợp với mặt phân cách", r"Chỉ góc đo từ pháp tuyến mới là góc khúc xạ."),
           (r"Dùng định luật khúc xạ để tính $r$", r"Đề chưa cho chiết suất nên không dùng được định luật; hình học đã đủ để suy ra $r$.")]),
  buoc("Chiều lệch và môi trường chiết quang hơn", "Môi trường nào chiết quang hơn?",
       loi=r"Hay cho rằng môi trường có góc lớn hơn thì chiết quang hơn. Xem lại bảng hai trường hợp ở mục định luật khúc xạ.",
       lua_chon=[(r"Môi trường (2), vì tia khúc xạ lại gần pháp tuyến hơn tia tới", True),
                 (r"Môi trường (1), vì góc tới lớn hơn", r"Góc tới lớn hơn góc khúc xạ nghĩa là tia đi vào môi trường chiết quang hơn, tức môi trường chứa tia khúc xạ."),
                 (r"Không so sánh được vì chưa biết chiết suất", r"Không cần giá trị chiết suất: so $r$ với $i$ là đủ để biết môi trường nào chiết quang hơn.")],
       ke=[(r"So $r$ với $i$ rồi đối chiếu bảng hai trường hợp", True),
           (r"Môi trường ở phía dưới hình luôn chiết quang hơn", r"Độ chiết quang không phụ thuộc vị trí trên hình; mặt phân cách nằm ngang chỉ là cách đặt hình."),
           (r"So độ dài hai đoạn tia vẽ trong hình", r"Độ dài đoạn tia vẽ không mang ý nghĩa vật lí.")]),
  buoc("Đảo chiều tia sáng", "Tia ló ra môi trường (1) hợp với pháp tuyến góc bao nhiêu độ?", 50, "°", 0.5,
       loi=r"Hay tính lại bằng cách tự đặt chiết suất, hoặc cho rằng góc ló phải giống góc đang có trong môi trường (2).",
       ke=[(r"Áp dụng tính thuận nghịch của đường truyền ánh sáng", True),
           (r"Góc ló bằng góc đang có trong môi trường (2)", r"Hai môi trường có chiết suất khác nhau nên góc ở hai bên mặt phân cách khác nhau."),
           (r"Tia ló đi thẳng, không bị gãy", r"Tia vẫn xiên góc qua mặt phân cách nên vẫn gãy khúc; chỉ chiếu vuông góc mới đi thẳng.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy tia <b>đi ra từ thuỷ tinh</b> (hoặc nước) → $n_1\sin i=n_2\sin r$ với $n_1$ là của môi trường chứa tia tới.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Góc tới", "Góc tới $i$ bằng bao nhiêu độ?", 25, "°", 0.5,
       loi=r"Hay lấy luôn số đo của đề làm góc tới. Góc tới đo từ pháp tuyến, không đo từ mặt phân cách."),
  buoc("Tính sin của góc khúc xạ", r"$\sin r$ bằng bao nhiêu?", 0.634, None, 0.005,
       loi=r"Hay đặt $n$ nhầm phía. Tia tới nằm trong môi trường nào thì $n_1$ là chiết suất của môi trường đó.",
       ke=[(r"$1{,}5\sin i=1\cdot\sin r$: tia tới ở trong thuỷ tinh", True),
           (r"$1\cdot\sin i=1{,}5\sin r$: coi như tia đi từ không khí vào thuỷ tinh", r"Tia tới ở trong thuỷ tinh nên $n_1=1{,}5$; đặt ngược là tính cho đường đi từ không khí vào thuỷ tinh."),
           (r"$r=\dfrac{i}{1{,}5}$: chia góc cho chiết suất", r"Định luật liên hệ sin của các góc, không phải bản thân các góc.")]),
  buoc("Góc khúc xạ", "Góc khúc xạ $r$ bằng bao nhiêu độ?", 39.3, "°", 0.3,
       loi=r"Hay bấm nhầm phím $\sin$ thay vì $\sin^{-1}$, hoặc để máy tính ở chế độ radian.",
       ke=[(r"Bấm $\sin^{-1}$ của giá trị $\sin r$ vừa có, máy ở chế độ độ", True),
           (r"Bấm $\sin$ của giá trị $\sin r$ vừa có", r"Đã có $\sin r$ thì phải bấm $\sin^{-1}$ để ra góc; bấm $\sin$ lần nữa sẽ cho kết quả không phải góc."),
           (r"Lấy kết quả rồi cộng thêm $90^\circ$ vì $r$ đo từ mặt phân cách", r"$r$ đo từ pháp tuyến; $\sin^{-1}$ cho thẳng góc này, không cần đổi.")]),
  buoc("Góc lệch", "Góc lệch $D$ bằng bao nhiêu độ?", 14.3, "°", 0.3,
       loi=r"Hay trừ góc đo từ hai gốc khác nhau (một góc đo từ mặt phân cách, một góc đo từ pháp tuyến).",
       ke=[(r"$D=|i-r|$ với $i$, $r$ cùng đo từ pháp tuyến", True),
           (r"$D=|65^\circ-r|$, dùng góc hợp mặt phân cách", r"$65^\circ$ đo từ mặt phân cách còn $r$ đo từ pháp tuyến: hai góc khác gốc, không trừ cho nhau được."),
           (r"$D=i+r$", r"Phương truyền đổi một lượng bằng hiệu của hai góc cùng đo từ pháp tuyến, không phải tổng.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>tia phản xạ</b> cùng <b>tia khúc xạ</b> → $i'=i$, rồi $180^\circ-i'-r$ là góc giữa hai tia.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Góc tới", "Góc tới $i$ bằng bao nhiêu độ?", 55, "°", 0.5,
       loi=r"Hay lấy luôn số đo của đề làm góc tới. Góc tới đo từ pháp tuyến, không đo từ mặt phân cách."),
  buoc("Góc khúc xạ", "Góc khúc xạ $r$ bằng bao nhiêu độ?", 30, "°", 0.5,
       loi=r"Hay coi góc giữa hai tia bằng tổng $i'+r$, hoặc dùng điều kiện của trường hợp hai tia vuông góc.",
       ke=[(r"$i'=i$, rồi $180^\circ-i'-r$ bằng góc giữa hai tia", True),
           (r"Góc giữa hai tia bằng $i'+r$, nên $r=95^\circ-i'$", r"Hai tia nằm hai bên pháp tuyến: góc giữa chúng cộng với $i'$ và $r$ mới bằng $180^\circ$."),
           (r"$i'+r=90^\circ$ như khi hai tia vuông góc", r"Chỉ đúng khi góc giữa hai tia là $90^\circ$; đề cho góc khác.")]),
  buoc("Chiết suất", "Chiết suất của chất lỏng bằng bao nhiêu?", 1.64, None, 0.02,
       loi=r"Hay lật tỉ số hai sin, hoặc dùng góc hợp mặt phân cách thay cho góc tới.",
       ke=[(r"$n=\dfrac{\sin i}{\sin r}$ với $n_1=1$", True),
           (r"$n=\dfrac{\sin r}{\sin i}$", r"Lật ngược tỉ số cho $n$ nhỏ hơn $1$, vô lí với chất lỏng."),
           (r"$n=\dfrac{\sin35^\circ}{\sin r}$, lấy góc hợp mặt chất lỏng làm góc tới", r"$35^\circ$ đo từ mặt phân cách, không phải góc tới.")]),
  buoc("Tốc độ ánh sáng trong chất lỏng", r"Tốc độ ánh sáng trong chất lỏng bằng bao nhiêu (đơn vị $10^8\ \text{m/s}$)?", 1.83, "·10⁸ m/s", 0.02,
       loi=r"Hay nhân $c$ với $n$. Trong chất lỏng ánh sáng chậm hơn trong chân không.",
       ke=[(r"$v=\dfrac{c}{n}$", True),
           (r"$v=c\cdot n$", r"Ánh sáng trong môi trường chậm hơn trong chân không, nên $v$ phải nhỏ hơn $c$."),
           (r"$v=\dfrac{n}{c}$", r"Sai đơn vị: kết quả không còn là m/s.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>nhiều lớp song song</b> → áp dụng định luật từng mặt phân cách; góc khúc xạ lớp trên là góc tới lớp dưới.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Góc trong nước", "Trong nước, tia laser hợp với pháp tuyến góc bao nhiêu độ?", 31.9, "°", 0.3,
       loi=r"Hay dùng cùng một chiết suất cho cả hai phía của mặt phân cách. Ở mặt nước–thuỷ tinh, một phía là nước, một phía là thuỷ tinh."),
  buoc("Góc tới ở mặt nước", "Góc tới ở mặt nước bằng bao nhiêu độ?", 44.8, "°", 0.3,
       loi=r"Hay lấy góc trong thuỷ tinh áp thẳng cho mặt nước. Ở mặt này, tia khúc xạ nằm trong nước.",
       ke=[(r"Mặt không khí–nước: $\sin i=\dfrac43\sin r_1$, với $r_1$ là góc trong nước", True),
           (r"Dùng góc trong thuỷ tinh: $\sin i=\dfrac43\sin28^\circ$", r"Tia ở mặt nước khúc xạ vào nước, không phải vào thuỷ tinh; góc trong nước mới là góc khúc xạ ở mặt này."),
           (r"$\sin i=1{,}5\sin r_1$", r"Mặt nước là mặt phân cách không khí–nước; chiết suất $1{,}5$ là của thuỷ tinh, không có mặt ở đây.")]),
  buoc("Rút hết nước", "Rút hết nước, giữ nguyên góc tới ở câu b. Góc khúc xạ trong thuỷ tinh thay đổi thế nào?",
       loi=r"Hay nghĩ bỏ lớp nước thì tia phải lệch khác đi. Thử tính lại với mặt không khí–thuỷ tinh rồi so với góc đề cho.",
       lua_chon=[(r"Không đổi", True),
                 (r"Lớn hơn, vì không còn nước làm tia lệch thêm", r"Thử tính $\sin r_2=\dfrac{\sin i}{1{,}5}$ với $\sin i$ ở câu b rồi so với góc đề cho."),
                 (r"Nhỏ hơn, vì thuỷ tinh tiếp xúc trực tiếp với không khí", r"Cũng thử tính như trên: kết quả không nhỏ hơn góc đề cho.")],
       ke=[(r"Áp dụng định luật cho mặt không khí–thuỷ tinh với $i$ ở câu b", True),
           (r"Tia vào thuỷ tinh với góc tới bằng góc trong nước vừa tính", r"Khi không còn nước thì góc tới thuỷ tinh là góc đã tính ở mặt không khí, không phải góc trong nước."),
           (r"Không tính được vì thiếu chiết suất của nước", r"Chiết suất nước không còn cần nữa: chỉ còn mặt phân cách không khí–thuỷ tinh.")]),
  buoc("Kiểm tra")]),
]

# ───────────── Ghi JSON ─────────────
d = {"lesson_id": 83, "lesson_title": "Bài 5. Khúc xạ ánh sáng", "generated_at": "2026-10-12",
     "review": {"checked": True, "notes": "Soạn 12/10/2026 (chặng 3). Kiểm chéo kiem-code 12/10: đáp số 5 dạng đúng, đã sửa 6 mục hình/lựa chọn. Chưa đối chiếu ngân hàng câu hỏi (topic 80/81): không có DB trong phiên."},
     "dang_bai": [dict(form="bai_tap", solution_html="", **x) for x in DE]}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
assert all(len(s["buoc"]) == SOLS[i].count('class="bt-step"') for i, s in enumerate(STEPS)), [(len(s["buoc"]), SOLS[i].count('class="bt-step"')) for i, s in enumerate(STEPS)]
inject(J, BUILD, ANALYSIS, SOLS, STEPS)

# Quét ký tự điều khiển (\t, \b… do chuỗi thường chứa `\text`, `\beta`) và `<`/`>` trần trong $…$
raw = open(J, encoding="utf8").read()
import re as _re
assert not _re.search(r"\\u000[0-8bcef]|\\t", raw.replace("\\\\t", "")), "ký tự điều khiển trong JSON"
for q in json.load(open(J))["dang_bai"]:
    for f in ("problem_html", "analysis_html", "solution_html"):
        h_ = _re.sub(r"<svg.*?</svg>", "", q[f], flags=_re.S)
        ms = _re.findall(r"\$\$(.+?)\$\$", h_, flags=_re.S)
        ms += _re.findall(r"\$([^$]+)\$", _re.sub(r"\$\$.+?\$\$", "", h_, flags=_re.S))
        for m_ in ms:
            assert "<" not in m_ and ">" not in m_, (f, m_[:60])
print("quét xong")
