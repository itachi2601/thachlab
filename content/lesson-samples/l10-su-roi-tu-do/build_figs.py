"""Sinh 4 hình SVG + bảng số liệu thí nghiệm cho bài 'Sự rơi tự do' (lesson 55),
thay mốc <!--FIGn-->, __BANG_TN3__, các số __X__ và __PHUT__ trong theory.src.html -> theory.html,
và ghi 3 file thí nghiệm content/thi-nghiem/tn-l10-roi-tu-do-0{1,2,3}.json (số liệu tính từ cùng mô hình).
Có lớp kiểm hình học: hộp nhãn không chồng nhau, không vượt viewBox, cỡ chữ >= 14; mũi tên đúng chiều.
Chạy: python3 build_figs.py   (sau đó: python3 build_bundle.py)"""
import json, math, pathlib, re, subprocess, sys
from svg_lib import RED, BLUE, ORG, GRN, wrap

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}


def vn(x, nd=2):
    """Số kiểu Việt Nam trong $…$: dấu phẩy thập phân viết {,}; bỏ số 0 thừa."""
    s = f"{x:.{nd}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace(".", "{,}")


def vt(x, nd=2):
    """Số kiểu Việt Nam ngoài công thức (trong <text> SVG, ô bảng)."""
    return vn(x, nd).replace("{,}", ",")


class Canvas:
    def __init__(self, name, w, h):
        self.name, self.w, self.h = name, w, h
        self.body, self.labels, self.markers, self.arrows = "", [], set(), {}

    def add(self, s):
        self.body += s

    def line(self, x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.body += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

    def ball(self, x, y, r=6, c=ORG, op=1):
        self.body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" stroke="currentColor" stroke-width="1.2" opacity="{op}"/>'

    def arr(self, tag, c, x1, y1, x2, y2, w=3, head=11, dash=""):
        """Mũi tên có ĐỈNH đúng tại (x2,y2); marker cỡ cố định (userSpaceOnUse)."""
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        ex, ey = x2 - ux * head, y2 - uy * head
        self.markers.add((c, head))
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.body += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{COL[c]}" stroke-width="{w}"{d} '
                      f'marker-end="url(#{self.name}-{c}{head})"/>')
        self.arrows[tag] = (x1, y1, x2, y2)

    def bracket(self, x, y1, y2, c="currentColor", tick=6):
        """Ngoặc đứng từ y1 tới y2 (hai vạch ngang ở đầu)."""
        self.body += (f'<path d="M{x - tick:.1f},{y1:.1f} H{x:.1f} V{y2:.1f} H{x - tick:.1f}" fill="none" '
                      f'stroke="{c}" stroke-width="1.6"/>')

    def text(self, x, y, s, c="currentColor", size=14, anchor="start", weight="700", italic=False):
        st = ' font-style="italic" font-family="serif"' if italic else ""
        self.body += f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"{st}>{s}</text>'
        plain = re.sub(r"<[^>]+>", "", s)
        wdt = 0.58 * size * len(plain)
        x0 = x if anchor == "start" else (x - wdt / 2 if anchor == "middle" else x - wdt)
        self.labels.append((plain, x0, y - 0.78 * size, x0 + wdt, y + 0.22 * size, size))

    def defs(self):
        out = "<defs>"
        for c, hd in sorted(self.markers):
            out += (f'<marker id="{self.name}-{c}{hd}" viewBox="0 0 10 10" refX="0" refY="5" markerWidth="{hd}" markerHeight="{hd}" '
                    f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{COL[c]}"/></marker>')
        return out + "</defs>"

    def check(self, obstacles=()):
        """Nhãn: cỡ >= 14, trong viewBox, không chồng nhau, không đè vật cản (hộp x0,y0,x1,y1)."""
        errs = []
        for i, a in enumerate(self.labels):
            if a[5] < 14:
                errs.append(f"{self.name}: nhãn '{a[0]}' cỡ {a[5]} < 14")
            if a[1] < 2 or a[3] > self.w - 2 or a[2] < 0 or a[4] > self.h:
                errs.append(f"{self.name}: nhãn '{a[0]}' vượt viewBox {[round(v) for v in a[1:5]]}")
            for b in self.labels[i + 1:]:
                if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    errs.append(f"{self.name}: nhãn '{a[0]}' chồng '{b[0]}'")
            for o in obstacles:
                if a[1] < o[2] and o[0] < a[3] and a[2] < o[3] and o[1] < a[4]:
                    errs.append(f"{self.name}: nhãn '{a[0]}' đè vật {o}")
        return errs

    def svg(self, label, cap, exp=None):
        s = wrap(f"0 0 {self.w} {self.h}", label, self.defs() + self.body, cap)
        if exp:
            s = s.replace('<figure class="fig" data-tl="1">', f'<figure class="fig" data-tl="1" data-exp="{exp}">', 1)
        return s


ERR = []
G = 9.8
near = lambda a, b, tol=1e-9: abs(a - b) < tol

# ================= Mô hình số liệu (dùng chung cho hình, bảng, lời văn, file thí nghiệm)
s_ff = lambda g, t: 0.5 * g * t * t          # quãng đường rơi tự do từ nghỉ
t_ff = lambda g, h: math.sqrt(2 * h / g)    # thời gian rơi tới độ sâu h

# TN1: rơi trong không khí, lực cản tỉ lệ v² -> s(t) = (vt²/g)·ln cosh(g t/vt); thời gian rơi H = 1,5 m
H1 = 1.5
VT_LIST = [("Hòn bi thép (đường kính 2 cm)", 40.0), ("Viên giấy vo chặt", 8.0), ("Tờ giấy A4 để phẳng", 1.5)]
t_drag = lambda vt, h: (vt / G) * math.acosh(math.exp(G * h / vt ** 2))
T_DRAG = [round(t_drag(vt, H1), 3) for _, vt in VT_LIST]
T_FREE1 = round(t_ff(G, H1), 3)
assert T_DRAG[0] - T_FREE1 < 0.01 and T_DRAG[1] - T_DRAG[0] < 0.05 and T_DRAG[2] > 1.8 * T_DRAG[0], T_DRAG

# TN2: ảnh chụp nhiều lần mỗi 0,1 s (cm)
T2 = 0.1
POS2 = [100 * s_ff(G, n * T2) for n in range(6)]          # 0; 4,9; 19,6; 44,1; 78,4; 122,5
GAP2 = [b - a for a, b in zip(POS2, POS2[1:])]            # 4,9; 14,7; 24,5; 34,3; 44,1
DGAP = [b - a for a, b in zip(GAP2, GAP2[1:])]
assert all(near(d, 100 * G * T2 * T2, 1e-6) for d in DGAP), DGAP     # mỗi khoảng dài thêm g·T² = 9,8 cm
assert all(near(g / GAP2[0], 2 * k + 1, 1e-6) for k, g in enumerate(GAP2))  # 1 : 3 : 5 : 7 : 9
DSS = f"${vn(100 * G * T2 * T2, 1)}\\ \\text{{cm}}$"

# TN3: đo g bằng cổng quang; nam châm nhả trễ TAU (sai số hệ thống); đồng hồ đọc tới 0,001 s
TAU = 0.003
S3 = [0.2, 0.4, 0.6, 0.8, 1.0]
T3_TRUE = [t_ff(G, s) for s in S3]
T3 = [round(t + TAU + 1e-12, 3) for t in T3_TRUE]
G3 = [round(2 * s / t ** 2, 2) for s, t in zip(S3, T3)]
assert all(g < G for g in G3), G3                          # lời văn: "mọi giá trị g đều nhỏ hơn 9,8"
DEV = [abs(g - G) for g in G3]
LECH = [i for i, d in enumerate(DEV) if d >= max(DEV) - 0.01]   # so tập có dung sai, không dùng max() trần
assert LECH == [0], (LECH, G3)                             # lời văn: lệch nhiều nhất ở hàng s = 0,20 m
assert all(b >= a - 1e-9 for a, b in zip(G3, G3[1:])), G3  # s càng lớn, g càng sát 9,8
GMEAN = sum(G3) / len(G3)

# Câu 2 (q3): t = 3 s, g = 9,8
Q3V, Q3S, Q3A, Q3B = G * 3, s_ff(G, 3), G * 9, 0.5 * G * 3
assert near(Q3V, 29.4, 1e-9) and near(Q3S, 44.1, 1e-9) and near(Q3A, 88.2, 1e-9) and near(Q3B, 14.7, 1e-9)
# Câu 4 (q5): giây thứ 2, g = 9,8
S1, S2 = s_ff(G, 1), s_ff(G, 2)
DS2 = S2 - S1
assert near(DS2, 14.7, 1e-9) and near(0.5 * G * 2, 9.8)    # phương án C: ½·9,8·2 = 9,8
# Câu 5 (q6): h -> 4h, t0 = 0,6 s
assert near(0.6 * math.sqrt(4), 1.2) and near(0.6 * 4, 2.4) and near(0.6 * 16, 9.6) and round(0.6 * math.sqrt(2), 2) == 0.85
# Câu 3 (q4): Mặt Trăng g ≈ 1,6; Trái Đất/Mặt Trăng ≈ 6
assert round(9.8 / 1.62) == 6
# Bài toán mẫu: h = 20 m, g = 10
GB = 10
VD_T = t_ff(GB, 20); VD_V = GB * VD_T; VD_S1 = s_ff(GB, VD_T - 1); VD_DS = 20 - VD_S1
assert near(VD_T, 2) and near(VD_V, 20) and near(VD_S1, 5) and near(VD_DS, 15) and near(VD_V ** 2, 2 * GB * 20)
assert near(VD_V * 3.6, 72)                                 # đời sống: 20 m/s = 72 km/h
# Điền bước: h = 45 m
DB_T = t_ff(GB, 45); DB_V = GB * DB_T; DB_DS = 45 - s_ff(GB, 2)
assert near(DB_T, 3) and near(DB_V, 30) and near(DB_DS, 25)
assert [s_ff(GB, k) - s_ff(GB, k - 1) for k in (1, 2, 3)] == [5, 15, 25]
# Thử sức: h = 80 m
TS_T = t_ff(GB, 80); TS_V = GB * TS_T; TS_DS = 80 - s_ff(GB, 3)
assert near(TS_T, 4) and near(TS_V, 40) and near(TS_DS, 35) and near(TS_T / VD_T, 2)
# Mẹo 5 – 20 – 45 – 80; ví dụ thả từ 5 m
assert [s_ff(GB, k) for k in (1, 2, 3, 4)] == [5, 20, 45, 80] and near(t_ff(GB, 5), 1)
# Câu 6 (q7): v = 25 m/s, g = 10
Q7A, Q7B, Q7C, Q7D = 25 ** 2 / (2 * GB), 25 ** 2 / GB, 25 / GB, 25 / (2 * GB)
assert near(Q7A, 31.25) and near(Q7B, 62.5) and near(Q7C, 2.5) and near(Q7D, 1.25) and near(s_ff(GB, 2.5), Q7A)
# Thử thách
TT1_T = t_ff(GB, 3.2); TT1_V = GB * TT1_T
assert near(TT1_T, 0.8) and near(TT1_V, 8)
TT2_T = t_ff(G, 0.2)
assert round(TT2_T, 2) == 0.2
assert all(near(s_ff(GB, t + 1) - s_ff(GB, t), 10 * t + 5) for t in (0, 0.5, 1, 2.3))

# ================= Hình 1: ống Newton — có không khí / đã hút hết không khí
c = Canvas("f1", 400, 300)
TOP, BOT = 44, 262
TUBES = [(100, "Có không khí"), (280, "Đã hút hết không khí")]
for cx, name in TUBES:
    c.add(f'<rect x="{cx - 32}" y="{TOP}" width="64" height="{BOT - TOP}" rx="12" fill="rgba(56,189,248,.08)" stroke="currentColor" stroke-width="2"/>')
    c.text(cx, 28, name, size=14, anchor="middle")
c.line(60, 62, 340, 62, "currentColor", 1.4, "5 4", op=.5)   # mức thả chung


def feather(x, y):
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate(18)">'
            f'<path d="M0,-17 C8,-9 8,9 0,17 C-8,9 -8,-9 0,-17 Z" fill="rgba(56,189,248,.35)" stroke="{BLUE}" stroke-width="2"/>'
            f'<line x1="0" y1="-17" x2="0" y2="22" stroke="{BLUE}" stroke-width="1.6"/></g>')


# ống 1 (có không khí): bi đã gần đáy, lông chim mới rơi một đoạn ngắn
Y_BI, Y_LONG1 = 240, 112
c.ball(100, Y_BI, 8)
c.add(feather(100, Y_LONG1))
c.text(140, Y_LONG1 + 5, "lông chim", size=14)
c.text(140, Y_BI + 5, "hòn bi", size=14)
# ống 2 (chân không): cả hai ngang nhau
c.ball(266, Y_BI, 8)
c.add(feather(294, Y_BI - 4))
c.text(100, 290, "lông chim chậm hơn", size=14, anchor="middle")
c.text(280, 290, "rơi như nhau", size=14, anchor="middle")
ERR += [] if Y_LONG1 < Y_BI - 80 else ["f1: ống 1 lông chim phải ở cao hơn hẳn bi"]
fig1 = c.svg("Hai ống Newton thả cùng lúc một lông chim và một hòn bi: ống còn không khí thì bi gần chạm đáy, lông chim mới rơi một đoạn; ống đã hút hết không khí thì hai vật rơi ngang nhau",
             "Hình 1. Ống Newton. Còn không khí: lông chim bị cản nhiều, rơi chậm hơn hòn bi. Hút hết không khí: hai vật rơi như nhau. Đường đứt nét là mức thả chung.",
             exp="tn-l10-roi-tu-do-01")
ERR += c.check(obstacles=[(68, TOP, 132, BOT), (248, TOP, 312, BOT)])

# ================= Hình 2: ảnh chụp nhiều lần viên bi, mỗi 0,1 s, cạnh thước và dây dọi
c = Canvas("f2", 400, 396)
Y0, SC = 44, 2.2            # 1 cm = 2,2 đơn vị
RX, BX = 72, 136            # thước, dây dọi / bi
c.line(RX, Y0, RX, Y0 + SC * 150, "currentColor", 2)
for cm in range(0, 151, 20):
    y = Y0 + SC * cm
    c.line(RX, y, RX + 10, y, "currentColor", 2)
    c.text(RX - 8, y + 5, str(cm), size=14, anchor="end", weight="600")
for cm in range(10, 151, 20):
    y = Y0 + SC * cm
    c.line(RX, y, RX + 6, y, "currentColor", 1.4)
c.text(14, 22, "s (cm)", size=14, weight="600")
c.line(BX, 18, BX, 372, "currentColor", 1.2, "3 4", op=.6)    # dây dọi
c.add(f'<path d="M{BX - 7},372 L{BX + 7},372 L{BX},386 Z" fill="currentColor" opacity=".6"/>')
YS = [Y0 + SC * p for p in POS2]
for k, y in enumerate(YS):
    c.ball(BX, y, 5)
    c.line(BX + 9, y, BX + 17, y, "currentColor", 1.4)
for k, (ya, yb) in enumerate(zip(YS, YS[1:])):
    c.text(BX + 24, (ya + yb) / 2 + 5, f"{vt(GAP2[k], 1)} cm", size=14, weight="600")
c.text(244, 70, "Mỗi khoảng dài", GRN, 14)
c.text(244, 90, "hơn khoảng trước", GRN, 14)
c.text(244, 110, f"{vt(100 * G * T2 * T2, 1)} cm", GRN, 14)
c.arr("g", "g", 300, 170, 300, 250, 3)
c.text(312, 216, "g", GRN, 18, italic=True)
c.text(150, 386, "dây dọi", size=14, weight="600")
x1, y1, x2, y2 = c.arrows["g"]
ERR += [] if y2 > y1 and x1 == x2 else ["f2: mũi tên g phải thẳng đứng hướng xuống"]
ERR += [] if all(b > a for a, b in zip(YS, YS[1:])) else ["f2: vị trí bi phải đi xuống"]
fig2 = c.svg("Vị trí viên bi rơi sau mỗi 0,1 giây cạnh thước dựng đứng và dây dọi: bi rơi dọc dây dọi, các khoảng 4,9; 14,7; 24,5; 34,3; 44,1 cm dài dần, mỗi khoảng dài hơn khoảng trước 9,8 cm",
             "Hình 2. Ảnh chụp nhiều lần (số liệu minh hoạ): vị trí bi sau mỗi 0,1 s. Bi rơi dọc dây dọi; các khoảng dài dần đều đặn, tỉ lệ 1 : 3 : 5 : 7 : 9 — chuyển động nhanh dần đều.",
             exp="tn-l10-roi-tu-do-02")
ERR += c.check(obstacles=[(BX - 6, Y0 - 6, BX + 6, YS[-1] + 6), (292, 170, 308, 250), (RX, Y0, RX + 10, Y0 + SC * 150)])

# ================= Hình 3: "giây thứ n" và "n giây đầu" (g = 9,8), đặt SAU Câu 4
c = Canvas("f3", 400, 310)
Y0, SC, AX = 40, 5.0, 150
PTS = [s_ff(G, k) for k in range(4)]                     # 0; 4,9; 19,6; 44,1 m
YP = [Y0 + SC * s for s in PTS]
c.arr("s", "k", AX, 28, AX, 290, 1.8, 9)
c.text(AX + 10, 302, "s (m)", size=14, weight="600")
for k, y in enumerate(YP):
    c.ball(AX, y, 6)
    c.text(AX - 14, y + 5, f"t = {k} s", size=14, anchor="end", weight="600")
c.bracket(178, YP[1], YP[2], BLUE)
c.text(188, (YP[1] + YP[2]) / 2 + 5, f"giây thứ 2: {vt(PTS[2] - PTS[1], 1)} m", BLUE, 14)
c.bracket(178, YP[2], YP[3], ORG)
c.text(188, (YP[2] + YP[3]) / 2 + 5, f"giây thứ 3: {vt(PTS[3] - PTS[2], 1)} m", ORG, 14)
c.bracket(390, YP[0], YP[3], GRN)
c.text(378, (YP[0] + YP[3]) / 2 - 2, "3 s đầu:", GRN, 14, anchor="end")
c.text(378, (YP[0] + YP[3]) / 2 + 16, f"{vt(PTS[3], 1)} m", GRN, 14, anchor="end")
ERR += [] if near(PTS[2] - PTS[1], DS2) else ["f3: giây thứ 2 lệch Câu 4"]
fig3 = c.svg("Vị trí vật rơi tự do lúc t bằng 0, 1, 2, 3 giây trên trục thẳng đứng; ngoặc chỉ quãng đường giây thứ 2 là 14,7 m, giây thứ 3 là 24,5 m, cả 3 giây đầu là 44,1 m",
             "Hình 3. Với <em>g</em> = 9,8 m/s²: giây thứ 2 rơi 19,6 − 4,9 = 14,7 m; giây thứ 3 rơi 24,5 m; cả 3 giây đầu rơi 44,1 m. \"Giây thứ <em>n</em>\" chỉ là một đoạn của \"<em>n</em> giây đầu\".")
ERR += c.check(obstacles=[(AX - 6, 28, AX + 6, 290)])

# ================= Hình 4: bài toán mẫu — chỉ ghi dữ liệu đề cho
c = Canvas("f4", 400, 300)
Y_NUT, SC = 66, 10.0                       # 1 m = 10 đơn vị
Y_SAN = Y_NUT + SC * 20
Y_T1 = Y_NUT + SC * s_ff(GB, VD_T - 1)     # vị trí lúc t − 1 (vẽ đúng tỉ lệ, không ghi số)
NX = 170
c.add(f'<rect x="40" y="26" width="290" height="10" fill="currentColor" opacity=".45"/>')
c.line(NX, 36, NX, 54, "currentColor", 2)
c.add(f'<path d="M{NX},54 q-7,0 -7,6" fill="none" stroke="currentColor" stroke-width="2"/>')
# chậu hoa vẽ hình tròn (cam), vị trí lúc t − 1 vẽ vòng nét đứt
c.add(f'<circle cx="{NX}" cy="{Y_NUT}" r="8" fill="{ORG}" stroke="currentColor" stroke-width="1.2"/>')
c.line(NX, Y_NUT + 10, NX, Y_SAN, "currentColor", 1.2, "3 4", op=.5)
c.add(f'<circle cx="{NX}" cy="{Y_T1}" r="8" fill="none" stroke="{ORG}" stroke-width="1.6" stroke-dasharray="3 2"/>')
c.line(NX + 12, Y_T1, NX + 26, Y_T1, "currentColor", 1.4)
c.text(NX + 32, Y_T1 + 5, "lúc t − 1", size=14, weight="600")
c.line(30, Y_SAN, 370, Y_SAN, "currentColor", 2.5)
for xx in range(36, 370, 14):
    c.line(xx, Y_SAN + 2, xx - 8, Y_SAN + 10, "currentColor", 1, op=.5)
c.text(NX + 32, Y_SAN - 8, "chạm đất: lúc t", size=14, weight="600")
c.bracket(118, Y_NUT, Y_SAN)
c.text(106, (Y_NUT + Y_SAN) / 2 + 5, "h = 20 m", size=14, anchor="end")
c.bracket(352, Y_T1, Y_SAN, ORG)
c.text(344, (Y_T1 + Y_SAN) / 2 + 5, "giây cuối: ?", ORG, 14, anchor="end")
c.arr("duong", "k", 40, 60, 40, 118, 2, 10)
c.text(14, 136, "chiều (+)", size=14, weight="600")
c.arr("g", "g", 204, 52, 204, 96, 3)
c.text(214, 82, "g", GRN, 18, italic=True)
ERR += [] if near((Y_T1 - Y_NUT) / (Y_SAN - Y_NUT), 0.25) else ["f4: vị trí t − 1 sai tỉ lệ"]
ERR += [] if c.arrows["g"][3] > c.arrows["g"][1] and c.arrows["duong"][3] > c.arrows["duong"][1] else ["f4: g / chiều dương phải hướng xuống"]
fig4 = c.svg("Chậu hoa treo ở móc ban công cao 20 m so với mặt đất, rơi thẳng xuống; trục dương hướng xuống; đánh dấu vị trí lúc t trừ 1 giây và lúc chạm đất, ngoặc 'giây cuối' chưa biết",
             "Hình 4. Chậu hoa tuột khỏi móc ở ban công cao 20 m. Chiều dương hướng xuống, gốc tại móc. Quãng \"giây cuối\" là từ vị trí lúc <em>t</em> − 1 tới mặt đất.")
ERR += c.check(obstacles=[(NX - 9, Y_NUT - 9, NX + 9, Y_NUT + 9), (NX - 9, Y_T1 - 9, NX + 9, Y_T1 + 9), (196, 52, 212, 96)])

if ERR:
    print("\n".join("✗ " + e for e in ERR)); sys.exit(1)

# ================= Bảng số liệu TN3 (chèn vào bài)
rows = [f"<tr><td>{vt(s, 2) if s != 1 else '1,00'}</td><td>{f'{t:.3f}'.replace('.', ',')}</td><td>{f'{g:.2f}'.replace('.', ',')}</td></tr>"
        for s, t, g in zip(S3, T3, G3)]
rows = [r.replace("<td>0,2</td>", "<td>0,20</td>").replace("<td>0,4</td>", "<td>0,40</td>")
         .replace("<td>0,6</td>", "<td>0,60</td>").replace("<td>0,8</td>", "<td>0,80</td>") for r in rows]
bang = ('<div class="table-scroll">\n<table class="tl-table">\n<thead>\n'
        '<tr><th>$s$ (m)</th><th>$t$ (s)</th><th>$g = 2s/t^2$ (m/s²)</th></tr>\n</thead>\n<tbody>\n'
        + "\n".join(rows) + "\n</tbody>\n</table>\n</div>")

f2s = lambda x: f"{x:.2f}".replace(".", "{,}")
REPL = {
    "__BANG_TN3__": bang,
    "__DSS__": DSS,
    "__GMIN__": f"${f2s(min(G3))}$", "__GMAX__": f"${f2s(max(G3))}\\ \\text{{m/s}}^2$",
    "__HANG_LECH__": f"${{s = {vn(S3[LECH[0]], 1)}0\\ \\text{{m}}}}$",
    "__G_LECH__": f2s(G3[LECH[0]]),
    "__Q3V__": vn(Q3V, 1), "__Q3S__": vn(Q3S, 1), "__Q3A__": vn(Q3A, 1), "__Q3B__": vn(Q3B, 1),
    "__S1__": vn(S1, 1), "__S2__": vn(S2, 1), "__DS2__": vn(DS2, 1),
    "__VD_T__": vn(VD_T), "__VD_V__": vn(VD_V), "__VD_T1__": vn(VD_T - 1), "__VD_S1__": vn(VD_S1),
    "__VD_DS__": vn(VD_DS), "__VD_V2__": vn(VD_V ** 2),
    "__DB_T__": vn(DB_T), "__DB_V__": vn(DB_V), "__DB_DS__": vn(DB_DS),
    "__TS_T__": vn(TS_T), "__TS_V__": vn(TS_V), "__TS_DS__": vn(TS_DS),
    "__Q7A__": vn(Q7A), "__Q7B__": vn(Q7B), "__Q7C__": vn(Q7C), "__Q7D__": vn(Q7D),
    "__TT1_T__": vn(TT1_T), "__TT1_V__": vn(TT1_V), "__TT2_T__": f2s(TT2_T),
}

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, fg in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
for k, v in REPL.items():
    assert k in h, k
    h = h.replace(k, v)
left = set(re.findall(r"__[A-Z0-9_]+__", h)) - {"__PHUT__"}
assert not left, left
# số phút: điền từ lint_do_dai (đo trên chính bản đã chèn hình)
tmp = HERE / ".theory.tmp.html"
tmp.write_text(h.replace("__PHUT__", "15"), encoding="utf8")
lint = ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = subprocess.run([sys.executable, str(lint), str(tmp)], capture_output=True, text=True).stdout
tmp.unlink()
m = re.search(r"~?(\d+(?:[.,]\d+)?)\s*phút", out)
phut = round(float(m.group(1).replace(",", "."))) if m else None
if phut is None:
    print("! không đọc được số phút từ lint_do_dai:\n" + out[:600]); sys.exit(1)
h = h.replace("__PHUT__", str(phut))
(HERE / "theory.html").write_text(h, encoding="utf8")

# ================= File thí nghiệm (số liệu tính từ cùng mô hình ở trên)
BASE = {"mon": "vat-ly", "lop": 10, "bai": "Bài 10. Sự rơi tự do", "lesson_id": 55,
        "nguon_trong_bai": "content/lesson-samples/l10-su-roi-tu-do/theory.html"}
r3 = lambda x: round(x, 3)
tn = [
    {**BASE,
     "id": "tn-l10-roi-tu-do-01",
     "ten": "Ba lần thả (giấy phẳng, giấy trên sách, giấy vo viên) và ống Newton",
     "loai": "thi_nghiem", "muc_do": "co_ban",
     "kien_thuc": ["roitudo.luc_can_khong_khi", "roitudo.dinh_nghia", "roitudo.moi_vat_nhu_nhau"],
     "muc_tieu": "Thấy rằng trong không khí vật rơi nhanh hay chậm do lực cản so với trọng lượng, không do nặng nhẹ; bỏ không khí thì mọi vật rơi như nhau.",
     "dung_cu": [{"ten": "Tờ giấy A4 (hoặc nhỏ hơn bìa sách)", "so_luong": 2}, {"ten": "Quyển sách bìa cứng", "so_luong": 1},
                 {"ten": "Hòn bi thép", "so_luong": 1}, {"ten": "Ống Newton có van + bơm hút chân không (hoặc video)", "so_luong": 1}],
     "cac_buoc": {"lam": ["Thả cùng lúc tờ giấy phẳng và quyển sách từ cùng độ cao.",
                          "Đặt tờ giấy (nhỏ hơn bìa) nằm phẳng trên quyển sách rồi thả.",
                          "Vo tròn tờ giấy, thả cùng lúc với hòn bi từ độ cao khoảng 1,5 m.",
                          "Lật ống Newton khi còn không khí, rồi khi đã hút hết không khí; quan sát lông chim và hòn bi."],
                  "quan_sat": ["Sách chạm sàn trước tờ giấy phẳng.", "Tờ giấy rơi sát theo sách, không tách ra.",
                               "Viên giấy và hòn bi chạm sàn gần như cùng lúc.", "Ống đã hút không khí: lông chim và bi rơi như nhau."],
                  "rut_ra": ["Nhanh hay chậm do lực cản không khí so với trọng lượng.",
                             "Không có lực cản (chỉ còn trọng lực): rơi tự do, mọi vật rơi như nhau."]},
     "tham_so": [{"ky_hieu": "h", "ten": "Độ cao thả", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.5, "max": 3, "mac_dinh": H1, "buoc": 0.1},
                 {"ky_hieu": "v_gh", "ten": "Vận tốc giới hạn của vật (đặc trưng lực cản)", "don_vi": "m/s", "kieu": "dieu_chinh", "min": 0.5, "max": 60, "mac_dinh": 8, "buoc": 0.5},
                 {"ky_hieu": "g", "ten": "Gia tốc rơi tự do", "don_vi": "m/s²", "kieu": "co_dinh", "gia_tri": G},
                 {"ky_hieu": "t", "ten": "Thời gian rơi", "don_vi": "s", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["lực cản F_c = m·g·(v/v_gh)²", "s(t) = (v_gh²/g)·ln cosh(g·t/v_gh)",
                                  "t(h) = (v_gh/g)·arccosh(exp(g·h/v_gh²))", "chân không (v_gh → ∞): t = √(2h/g)"],
                 "gia_thiet": ["lực cản tỉ lệ bình phương vận tốc", "tờ giấy phẳng coi như rơi thẳng (bỏ qua chao lượn)", "g = 9,8 m/s²"]},
     "so_lieu_mau": {"cot": ["Vật", "v_gh (m/s)", "t rơi 1,5 m (s)"],
                     "hang": [[nm, vt_, t] for (nm, vt_), t in zip(VT_LIST, T_DRAG)] + [["Bất kì vật nào trong chân không", None, T_FREE1]],
                     "ghi_chu": "Số liệu minh hoạ tính từ mô hình; v_gh là ước lượng cỡ độ lớn, không phải số đo."},
     "ket_qua_ky_vong": f"Bi thép {T_DRAG[0]} s, viên giấy {T_DRAG[1]} s (gần như cùng lúc), tờ giấy phẳng {T_DRAG[2]} s; chân không {T_FREE1} s cho mọi vật.",
     "hien_tuong_hay_sai": ["Cho rằng vật nặng rơi nhanh hơn.", "Cho rằng viên giấy vẫn rơi chậm vì khối lượng không đổi.",
                            "Cho rằng trong chân không lông chim lơ lửng."],
     "sai_so_thuong_gap": "Thả không cùng lúc; tờ giấy phẳng chao lượn nên thời gian rơi thay đổi nhiều giữa các lần.",
     "an_toan": "Ống Newton bằng thuỷ tinh: lật nhẹ, không va đập.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu",
                        "y_tuong": "Hai làn thả song song; chọn vật (bi, viên giấy, tờ giấy, lông chim) và công tắc 'có không khí / chân không'; hiện thời gian chạm sàn.",
                        "diem_nhan": "Cho học sinh dự đoán trước khi bấm thả; tắt không khí thì mọi cặp chạm sàn cùng lúc."}},
    {**BASE,
     "id": "tn-l10-roi-tu-do-02",
     "ten": "Dây dọi và video quay chậm: vị trí bi rơi sau mỗi 0,1 s",
     "loai": "thi_nghiem", "muc_do": "co_ban",
     "kien_thuc": ["roitudo.phuong_thang_dung", "roitudo.chieu_tren_xuong", "roitudo.nhanh_dan_deu"],
     "muc_tieu": "Từ vị trí bi cách đều thời gian, nhận ra rơi tự do theo phương thẳng đứng, chiều từ trên xuống, nhanh dần đều (các khoảng tỉ lệ 1 : 3 : 5…).",
     "dung_cu": [{"ten": "Dây dọi", "so_luong": 1}, {"ten": "Thước dài 1,5 m dựng đứng", "so_luong": 1},
                 {"ten": "Hòn bi thép", "so_luong": 1}, {"ten": "Điện thoại quay chậm (≥ 120 hình/s)", "so_luong": 1}],
     "cac_buoc": {"lam": ["Treo dây dọi cạnh thước dài 1,5 m dựng đứng.", "Thả hòn bi sát dây, quay video chậm.",
                          "Dừng hình mỗi 0,1 s, đánh dấu vị trí bi (6 vị trí từ t = 0 đến 0,5 s)."],
                  "quan_sat": ["Bi rơi dọc theo dây dọi.",
                               "Các khoảng giữa hai vị trí liền nhau: " + "; ".join(vt(g_, 1) for g_ in GAP2) + " cm — mỗi khoảng dài hơn khoảng trước 9,8 cm."],
                  "rut_ra": ["Phương thẳng đứng, chiều từ trên xuống.", "Các khoảng dài thêm đều đặn: vận tốc tăng đều, chuyển động nhanh dần đều."]},
     "tham_so": [{"ky_hieu": "T", "ten": "Khoảng thời gian giữa hai hình", "don_vi": "s", "kieu": "dieu_chinh", "min": 0.05, "max": 0.2, "mac_dinh": T2, "buoc": 0.05},
                 {"ky_hieu": "g", "ten": "Gia tốc rơi tự do", "don_vi": "m/s²", "kieu": "co_dinh", "gia_tri": G},
                 {"ky_hieu": "s", "ten": "Vị trí bi tính từ điểm thả", "don_vi": "cm", "kieu": "do_duoc", "sai_so_do": 0.5},
                 {"ky_hieu": "ds", "ten": "Khoảng giữa hai vị trí liền nhau", "don_vi": "cm", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["s = g·t²/2 (cm = 100·m)", "t = n·T, n = 0…5", "ds_(n+1) − ds_n = g·T²"],
                 "gia_thiet": ["bỏ qua lực cản không khí", "thả không vận tốc đầu", "g = 9,8 m/s²"]},
     "so_lieu_mau": {"cot": ["n", "t (s)", "s (cm)", "khoảng tới vị trí sau (cm)"],
                     "hang": [[n, round(n * T2, 1), r3(p), (r3(GAP2[n]) if n < len(GAP2) else None)] for n, p in enumerate(POS2)],
                     "ghi_chu": "Số liệu minh hoạ tính từ mô hình, dùng vẽ Hình 2; không thêm nhiễu."},
     "ket_qua_ky_vong": "Các khoảng 4,9; 14,7; 24,5; 34,3; 44,1 cm, tỉ lệ 1 : 3 : 5 : 7 : 9; hiệu hai khoảng liền nhau 9,8 cm = g·T².",
     "hien_tuong_hay_sai": ["Tưởng rơi tự do là chuyển động đều vì nhìn bằng mắt quá nhanh.",
                            "Đo vị trí ở mép bi thay vì tâm bi, các khoảng lệch nhau."],
     "sai_so_thuong_gap": "Ảnh mờ khi bi nhanh; thước không thẳng đứng; thời điểm t = 0 lấy sai.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu",
                        "y_tuong": "Bi rơi cạnh thước, để lại 'bóng' mỗi T giây; bảng tự điền s và khoảng ds.",
                        "diem_nhan": "Thanh trượt T: khoảng nào cũng dài thêm đúng g·T²."}},
    {**BASE,
     "id": "tn-l10-roi-tu-do-03",
     "ten": "Đo gia tốc rơi tự do bằng nam châm điện, cổng quang và đồng hồ hiện số",
     "loai": "thi_nghiem", "muc_do": "trung_binh",
     "kien_thuc": ["roitudo.gia_toc_g", "roitudo.s_bang_mot_nua_g_t_binh", "do_luong.sai_so_he_thong"],
     "muc_tieu": "Đo thời gian rơi ở 5 quãng rơi khác nhau, tính g = 2s/t², nhận ra sai số hệ thống (mọi giá trị cùng nhỏ hơn 9,8) và cách giảm.",
     "dung_cu": [{"ten": "Nam châm điện + công tắc", "so_luong": 1}, {"ten": "Cổng quang điện", "so_luong": 1},
                 {"ten": "Đồng hồ đo thời gian hiện số (0,001 s)", "so_luong": 1}, {"ten": "Hòn bi thép", "so_luong": 1},
                 {"ten": "Giá đỡ có thước dựng đứng", "so_luong": 1}],
     "cac_buoc": {"lam": ["Nam châm điện giữ hòn bi ở đầu thước dựng đứng.",
                          "Đặt cổng quang lần lượt cách điểm thả s = 0,20; 0,40; 0,60; 0,80; 1,00 m; mỗi vị trí thả một lần.",
                          "Ngắt điện: bi rơi, đồng hồ bắt đầu đếm; bi qua cổng quang thì đồng hồ dừng."],
                  "quan_sat": ["Thời gian đo: " + "; ".join(f"{t:.3f}".replace(".", ",") for t in T3) + " s.",
                               "g = 2s/t² tính ra: " + "; ".join(f"{g:.2f}".replace(".", ",") for g in G3) + " m/s²."],
                  "rut_ra": ["Các giá trị g sát nhau và gần 9,8 m/s²: tại một nơi, vật rơi với cùng gia tốc.",
                             "Mọi giá trị cùng nhỏ hơn 9,8 và lệch nhiều nhất ở quãng rơi ngắn nhất: sai số hệ thống do nam châm nhả bi trễ."]},
     "tham_so": [{"ky_hieu": "s", "ten": "Khoảng cách điểm thả – cổng quang", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.1, "max": 1.2, "mac_dinh": 0.6, "buoc": 0.1},
                 {"ky_hieu": "tau", "ten": "Độ trễ nhả bi của nam châm", "don_vi": "s", "kieu": "dieu_chinh", "min": 0, "max": 0.01, "mac_dinh": TAU, "buoc": 0.001},
                 {"ky_hieu": "g", "ten": "Gia tốc rơi tự do thật", "don_vi": "m/s²", "kieu": "co_dinh", "gia_tri": G},
                 {"ky_hieu": "t", "ten": "Thời gian đồng hồ hiện", "don_vi": "s", "kieu": "do_duoc", "sai_so_do": 0.0005},
                 {"ky_hieu": "g_do", "ten": "g tính từ số đo", "don_vi": "m/s²", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["t_thật = √(2s/g)", "t_đo = t_thật + tau, làm tròn tới 0,001 s", "g_do = 2s/t_đo²"],
                 "gia_thiet": ["bỏ qua lực cản không khí", "tau không đổi giữa các lần thả", "g = 9,8 m/s²"]},
     "so_lieu_mau": {"cot": ["s (m)", "t thật (s)", "t đo (s)", "g = 2s/t² (m/s²)"],
                     "hang": [[s, r3(tt), t, g] for s, tt, t, g in zip(S3, T3_TRUE, T3, G3)],
                     "ghi_chu": f"Số liệu minh hoạ tính từ mô hình với tau = {TAU} s (sai số hệ thống), làm tròn 0,001 s, không thêm nhiễu ngẫu nhiên. g trung bình = {GMEAN:.3f} m/s²."},
     "ket_qua_ky_vong": f"g từ {min(G3):.2f} đến {max(G3):.2f} m/s², đều nhỏ hơn 9,8; lệch nhiều nhất ở s = 0,20 m.",
     "hien_tuong_hay_sai": ["Thấy g < 9,8 rồi cho rằng thí nghiệm hỏng, không nhận ra sai số hệ thống.",
                            "Lấy trung bình để 'khử' sai số hệ thống (trung bình không khử được sai số cùng một phía).",
                            "Dùng g = s/t² (quên hệ số 2)."],
     "sai_so_thuong_gap": "Nam châm dư từ nhả bi trễ; cổng quang đặt lệch; đo s từ mép bi thay vì tâm bi.",
     "an_toan": "Đặt hộp đựng cát/khăn dưới chỗ bi rơi.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu+do_thi",
                        "y_tuong": "Kéo cổng quang lên xuống, bấm thả; bảng điền t và g; vẽ g theo s.",
                        "diem_nhan": "Thanh trượt tau: đặt tau = 0 thì mọi hàng ra đúng 9,8; tau > 0 thì hàng s nhỏ lệch nhiều nhất."}},
]
for d in tn:
    (ROOT / "content/thi-nghiem" / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"ok theory.html {len(h)} ký tự · 4 hình · {phut} phút · 3 file thí nghiệm · G3 = {G3} · T_DRAG = {T_DRAG}")
