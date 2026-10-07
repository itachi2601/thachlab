"""Sinh 4 hình SVG + bảng số liệu cho bài 'Thực hành đo tiêu cự của thấu kính hội tụ' (lesson 87),
thay mốc <!--FIGn-->, __BANG_TN2__, __PHUT__ trong theory.src.html -> theory.html,
và ghi 3 file thí nghiệm content/thi-nghiem/tn-l9-tieucu-0{1,2,3}.json (số liệu tính từ cùng mô hình thấu kính).
Hình tia/ảnh đều TÍNH TOẠ ĐỘ bằng công thức thấu kính và assert (tia ló qua F', ba tia gặp nhau ở B').
Chạy: python3 build_figs.py   (sau đó: python3 build_bundle.py)"""
import json, math, pathlib, re, subprocess, sys
from svg_lib import RED, BLUE, ORG, GRN, wrap, chevron

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ERR = []


def ok(cond, msg):
    if not cond:
        ERR.append(str(msg))


def vn(x, nd=1):
    return f"{x:.{nd}f}".replace(".", ",")


def thinlens_image(f, d):
    """Công thức thấu kính 1/f = 1/d + 1/d' (đơn vị tuỳ ý) -> d'"""
    return f * d / (d - f)


# =========================================================== Canvas có kiểm hình học
class Canvas:
    def __init__(self, name, w, h):
        self.name, self.w, self.h = name, w, h
        self.body, self.labels, self.segs = "", [], []

    def add(self, s):
        self.body += s

    def line(self, x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, obstacle=True):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.body += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
        if obstacle:
            self.segs.append((x1, y1, x2, y2))

    def ray(self, x1, y1, x2, y2, c=RED, frac=0.55, w=2.4):
        """Tia sáng: nét liền + đầu V 30° đặt giữa đoạn (frac)."""
        self.line(x1, y1, x2, y2, c, w)
        px, py = x1 + (x2 - x1) * frac, y1 + (y2 - y1) * frac
        self.body += chevron(px + (x2 - x1) * 0.04, py + (y2 - y1) * 0.04, x2 - x1, y2 - y1, c, w, 11)

    def arrow(self, x1, y1, x2, y2, c, w=2.8):
        """Vectơ (vật/ảnh): thân + đầu V 30° ở đỉnh."""
        self.line(x1, y1, x2, y2, c, w)
        self.body += chevron(x2, y2, x2 - x1, y2 - y1, c, w, 11)

    def dim(self, x1, x2, y, c="currentColor"):
        """Đường kích thước hai đầu mũi tên V (chỉ vào hai đường gióng)."""
        self.line(x1, y, x2, y, c, 1.8, obstacle=False)
        self.body += chevron(x1, y, -1, 0, c, 1.8, 10) + chevron(x2, y, 1, 0, c, 1.8, 10)

    def dot(self, x, y, r=4, c="currentColor"):
        self.body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'

    def lens(self, x, yt, yb, bulge=11):
        ym = (yt + yb) / 2
        self.add(f'<path d="M{x},{yt} Q{x + 2 * bulge},{ym} {x},{yb} Q{x - 2 * bulge},{ym} {x},{yt} Z" '
                 f'fill="rgba(56,189,248,.20)" stroke="currentColor" stroke-width="2.2"/>')

    def lens_line(self, x, yt, yb):
        """Kí hiệu thấu kính hội tụ: đoạn thẳng đứng, hai đầu mũi tên V hướng ra ngoài."""
        self.line(x, yt, x, yb, "currentColor", 2.4)
        self.body += chevron(x, yt, 0, -1, "currentColor", 2.4, 12) + chevron(x, yb, 0, 1, "currentColor", 2.4, 12)

    def text(self, x, y, s, c="currentColor", size=17, anchor="start", weight="700", italic=False):
        st = ' font-style="italic" font-family="serif"' if italic else ""
        self.body += f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"{st}>{s}</text>'
        plain = re.sub(r"<[^>]+>", "", s)
        wdt = 0.55 * size * len(plain)
        x0 = x if anchor == "start" else (x - wdt / 2 if anchor == "middle" else x - wdt)
        self.labels.append((plain, x0, y - 0.78 * size, x0 + wdt, y + 0.22 * size, size))

    def check(self):
        errs = []
        for i, a in enumerate(self.labels):
            if a[5] < 17:
                errs.append(f"{self.name}: nhãn '{a[0]}' cỡ {a[5]} < 17")
            if a[1] < 2 or a[3] > self.w - 2 or a[2] < 0 or a[4] > self.h:
                errs.append(f"{self.name}: nhãn '{a[0]}' vượt viewBox {[round(v) for v in a[1:5]]}")
            for b in self.labels[i + 1:]:
                if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    errs.append(f"{self.name}: nhãn '{a[0]}' chồng '{b[0]}'")
            for (x1, y1, x2, y2) in self.segs:
                n = max(2, int(math.hypot(x2 - x1, y2 - y1)))
                for k in range(n + 1):
                    px, py = x1 + (x2 - x1) * k / n, y1 + (y2 - y1) * k / n
                    if a[1] - 1 < px < a[3] + 1 and a[2] < py < a[4]:
                        errs.append(f"{self.name}: nét cắt xuyên nhãn '{a[0]}' tại ({px:.0f},{py:.0f})")
                        break
        return errs

    def svg(self, label, cap):
        return wrap(f"0 0 {self.w} {self.h}", label, self.body, cap)


# =========================================================== MÔ HÌNH SỐ LIỆU
F_TRUE = 10.0       # cm, thấu kính minh hoạ
# TN1: vật rất xa (20 m), 3 lần đọc d'
D_FAR = 2000.0
D1_MODEL = thinlens_image(F_TRUE, D_FAR)
N1 = [0.15, -0.15, 0.05]
DP1 = [round(D1_MODEL + n, 1) for n in N1]
DP1_MEAN = round(sum(DP1) / 3, 1)
ok(abs(D1_MODEL - 10.0503) < 1e-3 and round((D1_MODEL - F_TRUE) * 10, 1) == 0.5, ("lệch cách 1 ~0,5 mm", D1_MODEL))
ok(DP1 == [10.2, 9.9, 10.1] and DP1_MEAN == 10.1, DP1)
# vật cách 2 m (thử thách ⭐⭐⭐)
d2m = thinlens_image(F_TRUE, 200.0)
ok(f"{d2m:.1f}" == "10.5" and f"{(d2m - F_TRUE) / F_TRUE * 100:.0f}" == "5", d2m)
ok(f"{(D1_MODEL - F_TRUE) / F_TRUE * 100:.1f}" == "0.5", "20 m lệch 0,5 %")

# TN2: 5 vị trí vật
D2 = [15.0, 20.0, 25.0, 30.0, 40.0]
N2 = [0.4, -0.3, 0.2, -0.4, 0.3]
DP2 = [round(thinlens_image(F_TRUE, d) + n, 1) for d, n in zip(D2, N2)]
F2 = [round(d * dp / (d + dp), 1) for d, dp in zip(D2, DP2)]
F2_MEAN = round(sum(F2) / 5, 1)
DEV2 = [round(abs(f - F2_MEAN), 1) for f in F2]
DF2 = max(DEV2)
ok(DP2 == [30.4, 19.7, 16.9, 14.6, 13.6], DP2)
ok(F2 == [10.0, 9.9, 10.1, 9.8, 10.1], F2)
ok(F2_MEAN == 10.0 and abs(sum(F2) / 5 - 9.98) < 1e-9, (F2_MEAN, sum(F2) / 5))
ok(DEV2 == [0.0, 0.1, 0.1, 0.2, 0.1] and DF2 == 0.2, DEV2)
ok(sum(1 for v in DEV2 if abs(v - DF2) < 1e-6) == 1 and DEV2.index(DF2) == 3, "lệch lớn nhất duy nhất ở d = 30")
ok(F2_MEAN - DF2 <= 10.1 <= F2_MEAN + DF2 and F2_MEAN - DF2 <= F_TRUE <= F2_MEAN + DF2, "khoảng 9,8–10,2 chứa 10,0 và 10,1")
ok(all(d > F_TRUE for d in D2), "d phải > f")

# TN3: ảnh bằng vật
H_OBJ = 3.0
L3 = 4 * F_TRUE + 0.4
F3 = round(L3 / 4, 1)
ok(L3 == 40.4 and F3 == 10.1, (L3, F3))
ok(abs(thinlens_image(F_TRUE, 2 * F_TRUE) - 2 * F_TRUE) < 1e-9, "d=2f -> d'=2f")

# Quiz / bài mẫu
ok(f"{30.0 * 20.0 / 50.0:.1f}" == "12.0", "⭐")
ok(f"{50.0 / 4:.1f}" == "12.5" and f"{0.4 / 4:.1f}" == "0.1", "⭐⭐")
ok(abs(48.0 / 4 - 12.0) < 1e-9 and 2 * 12.0 == 24.0, "Q4")
ok(f"{19.0 * 19.0 / 38.0:.1f}" == "9.5" and round(thinlens_image(10, 20), 6) == 20, "Q5 (bẫy giá đỡ)")
ok(f"{(19.4 + 20.6) / 2:.1f}" == "20.0" and f"{20.6 - 19.4:.1f}" == "1.2", "Q6")
ok(0.2 / 10.0 == 0.02, "Q7: 0,2 cm ~ 2 % của f")
ok(f"{100.0 * 15.2 / 115.2:.1f}" == "13.2" and f"{1 / 100 + 1 / 15.2:.4f}" == "0.0758", "Q2: f từ d = 100, d' = 15,2")
# bài mẫu: f = 20, h = 10, d = 30
FM, HM, DM = 20.0, 10.0, 30.0
DPM = thinlens_image(FM, DM)
KM = DPM / DM
ok(DPM == 60.0 and KM == 2.0 and KM * HM == 20.0 and abs(1 / 20 - 1 / 30 - 1 / 60) < 1e-12, "bài mẫu")
# điền bước: d = 60
DPB = thinlens_image(FM, 60.0)
ok(DPB == 30.0 and DPB / 60.0 * HM == 5.0 and abs(1 / 20 - 1 / 60 - 1 / 30) < 1e-12, "bước điền")
# biến thể d = 40
DPV = thinlens_image(FM, 50.0)
ok(f"{DPV:.1f}" == "33.3" and f"{DPV / 50.0:.2f}" == "0.67" and f"{1 / (1 / 20 + 1 / 50):.1f}" == "14.3" and 50 + 20 == 70, "biến thể d = 50")
ok(thinlens_image(FM, 10.0) == -20.0 and abs(thinlens_image(FM, 10.0)) / 10.0 == 2.0, "⭐⭐⭐ d < f: d' = -20, h'/h = 2")
# quiz 1 / mục tiêu hình 1 (d = 30, f = 10)
ok(thinlens_image(10, 30) == 15.0, "Hình 1: d'=15")


# =========================================================== HÌNH 1: bố trí thí nghiệm
c = Canvas("f1", 420, 256)
S1 = 8.0                       # px / cm
F1, D1 = 10.0, 30.0
DP1F = thinlens_image(F1, D1)  # 15
AX, RAIL = 110, 176
XV = 24
XL = XV + D1 * S1
XM = XL + DP1F * S1
ok(XL == 264 and XM == 384, (XL, XM))
HV = 3.0 * S1
HI = DP1F / D1 * HV            # ảnh nhỏ hơn vật, k = 0,5
c.line(10, AX, 412, AX, "currentColor", 1.4, "7 5", 0.55, obstacle=False)    # trục chính
# ghế quang học
c.add(f'<rect x="10" y="{RAIL}" width="402" height="8" rx="2" fill="currentColor" opacity=".18" stroke="currentColor" stroke-width="1.5"/>')
x = XV
while x < 410:
    c.line(x, RAIL, x, RAIL + 5, "currentColor", 1.2, obstacle=False)
    x += 5 * S1
# chân đỡ
for xx, y0 in ((XV, AX), (XL, AX + 38), (XM, AX + 38)):
    c.line(xx, y0, xx, RAIL, "currentColor", 3, obstacle=False)
c.arrow(XV, AX, XV, AX - HV, ORG)                          # vật
c.lens(XL, AX - 38, AX + 38)
c.add(f'<rect x="{XM - 3}" y="{AX - 38}" width="6" height="76" rx="1" fill="currentColor" opacity=".28" stroke="currentColor" stroke-width="1.4"/>')
c.arrow(XM, AX, XM, AX + HI, GRN)                          # ảnh ngược trên màn
ok(HI > 0 and abs(HI / HV - DP1F / D1) < 1e-9, "H1: k = d'/d")
# kích thước d, d'
YD = 214
for xx in (XV, XL, XM):
    c.line(xx, RAIL + 8, xx, YD + 6, "currentColor", 1.2, "3 3", 0.6, obstacle=False)
c.dim(XV, XL, YD)
c.dim(XL, XM, YD)
c.text((XV + XL) / 2, 206, "d", anchor="middle", italic=True)
c.text((XL + XM) / 2, 206, "d′", anchor="middle", italic=True)
c.text(XV - 12, 72, "vật")
c.text(XL, 62, "thấu kính", anchor="middle")
c.text(XM, 62, "màn", anchor="middle")
c.text(XM - 10, 146, "ảnh", anchor="end", c=GRN)
c.text(12, 246, "ghế quang học (thước)")
ERR += c.check()
fig1 = c.svg("Bố trí đo trên ghế quang học: vật hình mũi tên, thấu kính hội tụ và màn nằm trên cùng một trục; đoạn d là khoảng cách từ vật đến thấu kính, đoạn d′ là khoảng cách từ thấu kính đến màn.",
             "Hình 1. Bố trí đo. <em>d</em> là khoảng cách từ vật tới tâm thấu kính, <em>d</em>′ là khoảng cách từ tâm thấu kính tới màn.")

# =========================================================== HÌNH 2: cách 1, chùm song song hội tụ ở F'
c = Canvas("f2", 420, 270)
S2 = 17.0
AX = 130
XL = 160
XF = XL + F_TRUE * S2          # F' = 330
c.line(10, AX, 412, AX, "currentColor", 1.4, "7 5", 0.55, obstacle=False)
c.lens(XL, AX - 62, AX + 62, 12)
c.add(f'<rect x="{XF - 3}" y="{AX - 62}" width="6" height="124" rx="1" fill="currentColor" opacity=".28" stroke="currentColor" stroke-width="1.4"/>')
for dy in (-50, -24, 24, 50):
    yl = AX + dy
    c.ray(12, yl, XL, yl, RED, 0.5)
    # tia ló qua F': đoạn từ (XL, yl) tới (XF, AX)
    c.ray(XL, yl, XF, AX, RED, 0.5)
    # kiểm: điểm trên tia ló tại x = XL + f/2 phải có y = AX + dy/2
    xm_ = XL + (XF - XL) / 2
    ym_ = yl + (AX - yl) * (xm_ - XL) / (XF - XL)
    ok(abs(ym_ - (AX + dy / 2)) < 1e-9, "H2: tia ló phải qua F'")
c.dot(XF, AX, 4.5, RED)
c.dim(XL, XF, 222)
for xx in (XL, XF):
    c.line(xx, AX + 62, xx, 228, "currentColor", 1.2, "3 3", 0.6, obstacle=False)
c.text((XL + XF) / 2, 212, "f", anchor="middle", italic=True)
c.text(XL, 38, "thấu kính", anchor="middle")
c.text(XF, 38, "màn", anchor="middle")
c.text(XF + 12, 152, "F′", italic=True)
c.dot(XL, AX, 3.5)
c.text(XL - 22, 146, "O", anchor="end", italic=True)
c.text(12, 244, "chùm tia song song")
c.text(12, 264, "từ vật rất xa")
ERR += c.check()
fig2 = c.svg("Chùm tia sáng song song tới thấu kính hội tụ rồi ló qua tiêu điểm ảnh F′; màn đặt tại F′ nên khoảng cách từ thấu kính tới màn bằng tiêu cự f.",
             "Hình 2. Vật rất xa: chùm tia tới song song, hội tụ tại <em>F</em>′. Màn đặt tại <em>F</em>′ nên khoảng cách từ thấu kính tới màn xấp xỉ <em>f</em>.")

# =========================================================== HÌNH 3: d = d' = 2f, ảnh bằng vật
c = Canvas("f3", 420, 278)
AX, XO, FP = 135, 210, 60.0               # F = XO - 60, F' = XO + 60
XA = XO - 2 * FP                          # vật ở 2f = 120 px bên trái
HB = 48.0
DPX = thinlens_image(FP, 2 * FP)          # d' tính từ công thức = 120
XAI = XO + DPX
KK = DPX / (2 * FP)
HI3 = KK * HB
ok(DPX == 120.0 and KK == 1.0 and HI3 == HB, "H3: d'=2f, k=1")
B = (XA, AX - HB)
Bp = (XAI, AX + HI3)                      # ảnh thật ngược chiều
# tia 1: song song trục tới thấu kính tại (XO, B_y), ló qua F'; tia 2: qua O
P1 = (XO, B[1])
slope1 = (AX - P1[1]) / (XO + FP - XO)                  # đi qua F'
yB1 = P1[1] + slope1 * (XAI - XO)
slope2 = (AX - B[1]) / (XO - XA)
yB2 = B[1] + slope2 * (XAI - XA)
ok(abs(yB1 - Bp[1]) < 1e-9 and abs(yB2 - Bp[1]) < 1e-9, "H3: hai tia gặp nhau ở B'")
ok(abs((P1[1] + slope1 * FP) - AX) < 1e-9, "H3: tia ló phải qua F'")
c.line(10, AX, 412, AX, "currentColor", 1.4, "7 5", 0.55, obstacle=False)
c.lens_line(XO, 40, 232)
c.arrow(XA, AX, B[0], B[1], ORG)
c.arrow(XAI, AX, Bp[0], Bp[1], GRN)
c.ray(B[0], B[1], P1[0], P1[1], RED, 0.5)                # tia 1 tới
c.ray(P1[0], P1[1], Bp[0], Bp[1], RED, 0.78)             # tia 1 ló (qua F')
c.ray(B[0], B[1], Bp[0], Bp[1], RED, 0.28)               # tia 2 qua O
c.dot(XO - FP, AX, 3.5)
c.dot(XO + FP, AX, 3.5)
c.dot(XO, AX, 3.5)
c.text(XO - FP, 158, "F", anchor="middle", italic=True)
c.text(XO + FP + 4, 124, "F′", italic=True)
c.text(XO + 8, 158, "O", italic=True)
c.text(XA - 8, 152, "A", anchor="end", italic=True)
c.text(XA, 76, "B", anchor="middle", italic=True)
c.text(XAI + 9, 126, "A′", italic=True)
c.text(XAI + 9, 196, "B′", italic=True)
YD = 246
for xx, y0 in ((XA, AX + 20), (XO, 232), (XAI, AX + 70)):
    c.line(xx, y0, xx, YD + 6, "currentColor", 1.2, "3 3", 0.6, obstacle=False)
c.dim(XA, XO, YD)
c.dim(XO, XAI, YD)
c.text((XA + XO) / 2, 270, "d = 2f", anchor="middle", italic=True)
c.text((XO + XAI) / 2, 270, "d′ = 2f", anchor="middle", italic=True)
ERR += c.check()
fig3 = c.svg("Vật AB đặt cách thấu kính hội tụ hai lần tiêu cự: tia song song trục ló qua F′ và tia qua tâm O gặp nhau tại B′; ảnh A′B′ thật, ngược chiều, cao bằng vật và cũng cách thấu kính hai lần tiêu cự.",
             "Hình 3. Khi <em>d</em> = 2<em>f</em> thì <em>d</em>′ = 2<em>f</em>: ảnh thật, ngược chiều, cao đúng bằng vật.")

# =========================================================== HÌNH 4: sơ đồ tỉ lệ bài mẫu (1 ô = 10 cm)
c = Canvas("f4", 420, 256)
CELL = 36.0
GX0, GY0 = 12.0, 30.0
NX, NY = 11, 6
XO = GX0 + 4 * CELL                       # O cách mép trái 4 ô
AX = GY0 + 3 * CELL
fcell, dcell, hcell = FM / 10, DM / 10, HM / 10     # 2, 3, 1 ô
dpcell = thinlens_image(fcell, dcell)               # 6 ô
hpcell = dpcell / dcell * hcell                     # 2 ô
ok(dpcell == 6.0 and hpcell == 2.0, "H4: d'=6 ô, h'=2 ô")
for i in range(NX + 1):
    c.line(GX0 + i * CELL, GY0, GX0 + i * CELL, GY0 + NY * CELL, "currentColor", 1, "", 0.22, obstacle=False)
for j in range(NY + 1):
    c.line(GX0, GY0 + j * CELL, GX0 + NX * CELL, GY0 + j * CELL, "currentColor", 1, "", 0.22, obstacle=False)
c.line(GX0, AX, GX0 + NX * CELL, AX, "currentColor", 1.8, "7 5", 0.8, obstacle=False)
XA = XO - dcell * CELL
XF = XO - fcell * CELL
XFP = XO + fcell * CELL
XAI = XO + dpcell * CELL
B = (XA, AX - hcell * CELL)
Bp = (XAI, AX + hpcell * CELL)
c.lens_line(XO, GY0 + 6, GY0 + NY * CELL - 6)
# tia 1: song song trục -> ló qua F'
t1 = (XO, B[1])
# tia 3: qua F -> ló song song trục
slope3 = (AX - B[1]) / (XF - XA)
y3 = B[1] + slope3 * (XO - XA)
t3 = (XO, y3)
ok(abs(slope3 - 1.0) < 1e-9 and abs(y3 - Bp[1]) < 1e-9, "H4: tia qua F chạm thấu kính ở độ cao của B'")
sl1 = (AX - t1[1]) / (XFP - XO)
ok(abs(t1[1] + sl1 * (XAI - XO) - Bp[1]) < 1e-9, "H4: tia 1 ló qua F' và tới B'")
sl2 = (AX - B[1]) / (XO - XA)
ok(abs(B[1] + sl2 * (XAI - XA) - Bp[1]) < 1e-9, "H4: tia 2 qua O tới B'")
c.arrow(XA, AX, B[0], B[1], ORG)
c.arrow(XAI, AX, Bp[0], Bp[1], GRN)
c.ray(B[0], B[1], t1[0], t1[1], RED, 0.5)
c.ray(t1[0], t1[1], Bp[0], Bp[1], RED, 0.66)
c.ray(B[0], B[1], Bp[0], Bp[1], RED, 0.3)
c.ray(B[0], B[1], t3[0], t3[1], RED, 0.5)
c.ray(t3[0], t3[1], Bp[0], Bp[1], RED, 0.5)
for xx in (XF, XO, XFP):
    c.dot(xx, AX, 3.5)
c.text(XF, 160, "F", anchor="middle", italic=True)
c.text(XFP, 124, "F′", anchor="middle", italic=True)
c.text(XO + 8, 160, "O", italic=True)
c.text(XA - 8, 160, "A", anchor="end", italic=True)
c.text(XA - 8, 100, "B", anchor="end", italic=True)
c.text(XAI + 9, 130, "A′", italic=True)
c.text(XAI + 9, 218, "B′", italic=True)
c.text(12, 20, "1 ô = 10 cm")
ERR += c.check()
fig4 = c.svg("Sơ đồ tỉ lệ một ô bằng mười xăng-ti-mét: thấu kính hội tụ tiêu cự hai ô, vật AB cao một ô cách thấu kính ba ô; ba tia gặp nhau tại B′, ảnh A′B′ thật, ngược chiều, cách thấu kính sáu ô và cao hai ô.",
             "Hình 4. Sơ đồ tỉ lệ 1 ô = 10 cm: ba tia gặp nhau tại <em>B</em>′; ảnh nằm cách thấu kính 6 ô và cao 2 ô.")

if ERR:
    print("\n".join("✗ " + e for e in ERR))
    sys.exit(1)


# =========================================================== Bảng số liệu
def table(head, rows):
    return ('<div class="table-scroll">\n<table class="tl-table">\n<thead>\n<tr>' + "".join(f"<th>{h}</th>" for h in head)
            + "</tr>\n</thead>\n<tbody>\n" + "\n".join("<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in rows)
            + "\n</tbody>\n</table>\n</div>")


bang2 = table(["$d$ (cm)", "$d'$ (cm)", "$f$ (cm)"],
              [[vn(d), vn(dp), vn(f)] for d, dp, f in zip(D2, DP2, F2)])

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, fg in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
h = h.replace("__BANG_TN2__", bang2)
assert "__" not in h.replace("__PHUT__", "")
tmp = HERE / ".theory.tmp.html"
tmp.write_text(h.replace("__PHUT__", "15"), encoding="utf8")
lint = ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = subprocess.run([sys.executable, str(lint), str(tmp)], capture_output=True, text=True).stdout
tmp.unlink()
m = re.search(r"~?(\d+(?:[.,]\d+)?)\s*phút", out)
if not m:
    print("! không đọc được số phút từ lint_do_dai:\n" + out[:800]); sys.exit(1)
phut = math.ceil(float(m.group(1).replace(",", ".")) - 1e-9)
h = h.replace("__PHUT__", str(phut))
(HERE / "theory.html").write_text(h, encoding="utf8")

# =========================================================== File thí nghiệm
BASE = {"mon": "vat-ly", "lop": 9, "bai": "Bài 9. Thực hành đo tiêu cự của thấu kính hội tụ", "lesson_id": 87,
        "nguon_trong_bai": "content/lesson-samples/l9-thuc-hanh-tieu-cu/theory.html"}
DUNG_CU_CHUNG = [{"ten": "Ghế quang học (hoặc thước dài 1 m, độ chia 1 mm)", "so_luong": 1},
                 {"ten": "Thấu kính hội tụ có giá đỡ, f cỡ 10 cm", "so_luong": 1},
                 {"ten": "Màn trắng có giá, trượt được dọc thước", "so_luong": 1}]
tn = [
    {**BASE, "id": "tn-l9-tieucu-01",
     "ten": "Cách 1: hứng ảnh của vật rất xa, đo gần đúng tiêu cự",
     "loai": "thi_nghiem", "muc_do": "co_ban",
     "kien_thuc": ["tieucu.cach_vat_xa", "tieucu.chum_song_song_hoi_tu_tai_f"],
     "muc_tieu": "Nhận ra khi vật rất xa thì ảnh nằm ở tiêu điểm, nên khoảng cách từ màn tới thấu kính xấp xỉ tiêu cự; dùng kết quả gần đúng này để biết cỡ f trước khi làm cách 2.",
     "dung_cu": DUNG_CU_CHUNG + [{"ten": "Cây hoặc toà nhà cách 20 m trở lên nhìn qua cửa sổ (không dùng Mặt Trời)", "so_luong": 1}],
     "cac_buoc": {"lam": ["Hướng thấu kính ra cây ở xa (từ 20 m trở lên) qua cửa sổ, đặt màn sau thấu kính.",
                          "Dịch màn tới lui cho ảnh nét nhất, đo khoảng cách từ màn tới tâm thấu kính; lặp 3 lần."],
                  "quan_sat": ["Ảnh cây nhỏ xíu, ngược chiều.", "d' = " + "; ".join(vn(x) for x in DP1) + " cm."],
                  "rut_ra": [f"Trung bình {vn(DP1_MEAN)} cm nên f ≈ {vn(DP1_MEAN)} cm.",
                             "Kết quả gần đúng vì ảnh nét nhất là một đoạn vài mm và vật không ở vô cực; dùng để biết cỡ f."]},
     "tham_so": [{"ky_hieu": "f", "ten": "Tiêu cự thật của thấu kính", "don_vi": "cm", "kieu": "dieu_chinh", "min": 5, "max": 20, "mac_dinh": F_TRUE, "buoc": 0.5},
                 {"ky_hieu": "d", "ten": "Khoảng cách vật – thấu kính", "don_vi": "cm", "kieu": "dieu_chinh", "min": 200, "max": 5000, "mac_dinh": D_FAR, "buoc": 100},
                 {"ky_hieu": "nhieu", "ten": "Biên độ sai lệch khi xác định vị trí ảnh nét", "don_vi": "cm", "kieu": "dieu_chinh", "min": 0, "max": 0.4, "mac_dinh": 0.15, "buoc": 0.05},
                 {"ky_hieu": "dcnn", "ten": "Độ chia nhỏ nhất của thước", "don_vi": "cm", "kieu": "co_dinh", "gia_tri": 0.1},
                 {"ky_hieu": "dp", "ten": "Khoảng cách màn – thấu kính đo được", "don_vi": "cm", "kieu": "do_duoc", "sai_so_do": 0.1},
                 {"ky_hieu": "f_do", "ten": "Tiêu cự ước lượng", "don_vi": "cm", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["d' = f·d/(d − f)", "khi d rất lớn: d' → f", "f_ước_lượng ≈ trung bình các lần đo d'"],
                 "gia_thiet": ["thấu kính mỏng, tia gần trục", "d = 20 m, f = 10 cm: d' lớn hơn f khoảng 0,5 mm",
                               "nhiễu là dãy cố định để tái lập: +0,15; −0,15; +0,05 cm"]},
     "so_lieu_mau": {"cot": ["Lần đo", "d' (cm)"], "hang": [[i + 1, x] for i, x in enumerate(DP1)],
                     "ghi_chu": f"Số liệu minh hoạ tính từ mô hình (f = 10,0 cm; vật cách 20 m) rồi thêm sai lệch nhỏ làm tròn mm, không phải đo thật. Trung bình {DP1_MEAN} cm."},
     "ket_qua_ky_vong": f"f ≈ {vn(DP1_MEAN)} cm (gần đúng); vật cách 2 m thì d' ≈ {vn(d2m)} cm, lệch khoảng 5 % nên phải dùng vật từ 20 m trở lên.",
     "hien_tuong_hay_sai": ["Dùng Mặt Trời làm vật rất xa: nguy hiểm và có thể gây cháy.", "Dùng vật quá gần (vài mét) rồi coi d' = f.", "Dừng ngay khi thấy ảnh tạm nét, không tìm điểm giữa khoảng nét."],
     "sai_so_thuong_gap": "Ảnh nét nhất là một đoạn vài mm; đo từ mép giá đỡ thay vì tâm thấu kính; vật chưa đủ xa.",
     "an_toan": "Không nhìn Mặt Trời qua thấu kính; không để thấu kính hứng nắng gần giấy, vải, da.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu",
                        "y_tuong": "Chùm tia song song tới thấu kính; kéo màn tới lui, ảnh nét nhất khi màn chạm F'. Thanh trượt 'khoảng cách vật' cho thấy d' tiến dần tới f.",
                        "diem_nhan": "Kéo d từ 2 m lên 20 m: độ lệch d' − f giảm từ 5 % xuống 0,5 %."}},
    {**BASE, "id": "tn-l9-tieucu-02",
     "ten": "Cách 2: đo d và d' ở 5 vị trí vật, tính f trung bình và sai số",
     "loai": "thi_nghiem", "muc_do": "trung_binh",
     "kien_thuc": ["tieucu.cong_thuc_f_tu_d_dp", "tieucu.sai_so_do_lech_lon_nhat", "tieucu.do_toi_tam_thau_kinh"],
     "muc_tieu": "Đo d và d' khi ảnh rõ nét ở 5 vị trí vật, tính f từ f = dd'/(d + d'), lấy trung bình và sai số bằng độ lệch lớn nhất, viết f = f̄ ± Δf.",
     "dung_cu": DUNG_CU_CHUNG + [{"ten": "Vật sáng hình mũi tên cao 3,0 cm (khe mũi tên trước đèn LED)", "so_luong": 1}],
     "cac_buoc": {"lam": ["Đặt vật tại d = " + "; ".join(vn(d) for d in D2) + " cm (đo tới tâm thấu kính).",
                          "Mỗi lần dịch màn cho ảnh nét nhất, đọc d' trên thước chia tới 1 mm, rồi tính f = dd'/(d + d')."],
                  "quan_sat": ["d càng lớn thì d' càng nhỏ.", "d' = " + "; ".join(vn(x) for x in DP2) + " cm.", "f = " + "; ".join(vn(x) for x in F2) + " cm."],
                  "rut_ra": [f"f̄ = {sum(F2) / 5:.2f} cm, làm tròn {vn(F2_MEAN)} cm (cùng độ chia 0,1 cm) rồi mới tính độ lệch.",
                             "Δf_i = " + "; ".join(vn(x) for x in DEV2) + " cm; Δf = độ lệch lớn nhất = " + vn(DF2) + " cm.",
                             f"f = {vn(F2_MEAN)} ± {vn(DF2)} cm; khoảng 9,8 – 10,2 cm khớp cách 1 (10,1) và cách 3 (10,1)."]},
     "tham_so": [{"ky_hieu": "f", "ten": "Tiêu cự thật của thấu kính", "don_vi": "cm", "kieu": "dieu_chinh", "min": 5, "max": 10, "mac_dinh": F_TRUE, "buoc": 0.5},
                 {"ky_hieu": "d", "ten": "Khoảng cách vật – thấu kính", "don_vi": "cm", "kieu": "dieu_chinh", "min": 12, "max": 50, "mac_dinh": 20.0, "buoc": 1},
                 {"ky_hieu": "nhieu", "ten": "Biên độ sai lệch khi xác định vị trí ảnh nét", "don_vi": "cm", "kieu": "dieu_chinh", "min": 0, "max": 0.6, "mac_dinh": 0.3, "buoc": 0.1},
                 {"ky_hieu": "lech_goc", "ten": "Đoạn đo hụt do đo tới mặt giá đỡ thay vì tâm (mỗi phía)", "don_vi": "cm", "kieu": "dieu_chinh", "min": 0, "max": 2, "mac_dinh": 0, "buoc": 0.5},
                 {"ky_hieu": "dcnn", "ten": "Độ chia nhỏ nhất của thước", "don_vi": "cm", "kieu": "co_dinh", "gia_tri": 0.1},
                 {"ky_hieu": "dp", "ten": "Khoảng cách màn – thấu kính đo được", "don_vi": "cm", "kieu": "do_duoc", "sai_so_do": 0.1},
                 {"ky_hieu": "f_do", "ten": "Tiêu cự tính từ từng lần đo", "don_vi": "cm", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["d'_lý_thuyết = f·d/(d − f)", "d'_đo = d'_lý_thuyết + nhiễu_lần, làm tròn 0,1 cm", "f_i = d·d'_đo/(d + d'_đo), làm tròn 0,1 cm",
                                  "f̄ = trung bình f_i; Δf_i = |f_i − f̄|; Δf = max Δf_i", "f = f̄ ± Δf"],
                 "gia_thiet": ["thấu kính mỏng, tia gần trục", "f thật = 10,0 cm", "nhiễu là dãy cố định để tái lập: +0,4; −0,3; +0,2; −0,4; +0,3 cm",
                               "phải giữ d ≥ 1,2·f (ảnh thật, không quá xa): với f ≤ 10 cm thì d ≥ 12 cm", "khi lech_goc > 0: d và d' cùng giảm lech_goc nên f tính ra nhỏ hơn thật"]},
     "so_lieu_mau": {"cot": ["d (cm)", "d' (cm)", "f (cm)"], "hang": [[d, dp, f] for d, dp, f in zip(D2, DP2, F2)],
                     "ghi_chu": f"Số liệu minh hoạ tính từ mô hình (f = 10,0 cm) rồi thêm sai lệch nhỏ làm tròn mm, không phải đo thật. f̄ = {sum(F2) / 5:.2f} ≈ {F2_MEAN}; Δf = {DF2}."},
     "ket_qua_ky_vong": f"f = {vn(F2_MEAN)} ± {vn(DF2)} cm; lệch lớn nhất ở lần d = 30,0 cm (f = 9,8 cm).",
     "hien_tuong_hay_sai": ["Đo d, d' tới mép giá đỡ: d và d' cùng hụt nên f nhỏ hơn thật (d = d' = 19,0 cm cho f = 9,5 cm thay vì 10,0 cm).",
                            "Ghi d' khi ảnh mới 'tạm nét', không lấy trung điểm khoảng nét.", "Chỉ đo một lần rồi lấy luôn f."],
     "sai_so_thuong_gap": "Xác định vị trí ảnh nét (khoảng nét rộng cỡ 1 cm); đo từ mép giá đỡ; vật và màn không vuông góc trục.",
     "an_toan": "Dùng đèn LED, không cầm bóng đèn nóng; không để thấu kính hứng nắng.",
     "goi_y_mo_phong": {"loai": "so_do_luc+bang_so_lieu",
                        "y_tuong": "Ghế quang học: kéo vật tới d, kéo màn tìm ảnh nét; bảng tự điền d, d', f và tính f̄, Δf.",
                        "diem_nhan": "Thanh trượt 'đo hụt ở giá đỡ': kéo lên thì cả năm lần f cùng nhỏ đi, lấy trung bình không sửa được."}},
    {**BASE, "id": "tn-l9-tieucu-03",
     "ten": "Cách 3: tìm vị trí ảnh bằng vật, f = L/4",
     "loai": "thi_nghiem", "muc_do": "co_ban",
     "kien_thuc": ["tieucu.cach_anh_bang_vat", "tieucu.d_bang_dp_bang_2f"],
     "muc_tieu": "Nhận ra khi ảnh cao đúng bằng vật thì d = d' = 2f, nên khoảng cách vật – màn L = 4f và f = L/4; sai số của L chia cho 4 khi tính f.",
     "dung_cu": DUNG_CU_CHUNG + [{"ten": "Vật sáng hình mũi tên cao 3,0 cm (khe mũi tên trước đèn LED)", "so_luong": 1}],
     "cac_buoc": {"lam": ["Đặt vật, thấu kính, màn trên ghế quang học.",
                          "Dịch thấu kính và màn cho ảnh nét và cao đúng 3,0 cm như vật, rồi đo khoảng cách L từ vật tới màn."],
                  "quan_sat": [f"L = {vn(L3)} cm.", "Ảnh thật, ngược chiều, cao bằng vật."],
                  "rut_ra": [f"f = L/4 = {vn(L3)}/4 = {vn(F3)} cm, khớp cách 1 và cách 2.",
                             "ΔL chia 4 khi tính f nên cách này cho f khá chính xác."]},
     "tham_so": [{"ky_hieu": "f", "ten": "Tiêu cự thật của thấu kính", "don_vi": "cm", "kieu": "dieu_chinh", "min": 5, "max": 20, "mac_dinh": F_TRUE, "buoc": 0.5},
                 {"ky_hieu": "sai_L", "ten": "Sai lệch khi xác định L (ảnh bằng vật chưa thật chuẩn)", "don_vi": "cm", "kieu": "dieu_chinh", "min": 0, "max": 1, "mac_dinh": 0.4, "buoc": 0.1},
                 {"ky_hieu": "h", "ten": "Chiều cao vật", "don_vi": "cm", "kieu": "co_dinh", "gia_tri": H_OBJ},
                 {"ky_hieu": "L", "ten": "Khoảng cách vật – màn đo được", "don_vi": "cm", "kieu": "do_duoc", "sai_so_do": 0.1},
                 {"ky_hieu": "f_do", "ten": "Tiêu cự tính ra", "don_vi": "cm", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["d = d' = 2f khi k = d'/d = 1", "L = d + d' = 4f", "L_đo = 4f + sai_L", "f = L/4; Δf = ΔL/4"],
                 "gia_thiet": ["thấu kính mỏng, tia gần trục", "f thật = 10,0 cm", "sai_L = +0,4 cm"]},
     "so_lieu_mau": {"cot": ["L (cm)", "f = L/4 (cm)"], "hang": [[L3, F3]],
                     "ghi_chu": "Số liệu minh hoạ tính từ mô hình (f = 10,0 cm, L lệch +0,4 cm), không phải đo thật."},
     "ket_qua_ky_vong": f"f = {vn(F3)} cm; với L = 48,0 cm thì f = 12,0 cm.",
     "hien_tuong_hay_sai": ["Nhớ nhầm f = L/2 (đó là d, không phải f).", "Coi ảnh bằng vật khi chỉ mới gần bằng, không so chiều cao ảnh với vật bằng thước.", "Quên L = d + d' gồm hai đoạn 2f."],
     "sai_so_thuong_gap": "Ảnh bằng vật chỉ nhận ra với sai lệch cỡ mm; đo L từ mặt giá đỡ thay vì từ vật và màn.",
     "an_toan": "Dùng đèn LED, không cầm bóng đèn nóng.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc+so_do_luc",
                        "y_tuong": "Kéo thấu kính dọc ghế; hiện chiều cao ảnh so với vật, khi hai chiều cao bằng nhau thì hiện L và f = L/4.",
                        "diem_nhan": "Thanh trượt L: nếu L < 4f thì không có vị trí nào cho ảnh nét hứng được trên màn."}},
]
for t in tn:
    f_ = ROOT / "content" / "thi-nghiem" / f"{t['id']}.json"
    f_.write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf8")
print(f"theory.html: {len(h) / 1024:.1f} KB · phút = {phut} · tn: {[t['id'] for t in tn]}")
