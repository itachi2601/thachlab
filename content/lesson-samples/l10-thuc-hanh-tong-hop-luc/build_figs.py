"""Sinh 3 hình SVG + các bảng số liệu cho bài 'Thực hành: Tổng hợp lực' (lesson 67),
thay mốc <!--FIGn-->, __BANG_*__, __PHUT__ trong theory.src.html -> theory.html,
và ghi 3 file thí nghiệm content/thi-nghiem/tn-l10-thuchanhthl-0{1,2,3}.json (số liệu tính từ cùng mô hình, làm tròn half-up bằng Decimal).
Có lớp kiểm hình học: nhãn không chồng nhau / không vượt viewBox / không bị nét cắt xuyên; mũi tên đúng chiều.
Chạy: python3 build_figs.py   (sau đó: python3 build_bundle.py)"""
import json, math, pathlib, re, subprocess, sys
from decimal import Decimal as D, ROUND_HALF_UP
from svg_lib import RED, BLUE, ORG, GRN, wrap

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}


def vn(x, nd=2):
    return f"{x:.{nd}f}".replace(".", ",")


class Canvas:
    def __init__(self, name, w, h):
        self.name, self.w, self.h = name, w, h
        self.body, self.labels, self.markers, self.arrows, self.segs = "", [], set(), {}, []

    def add(self, s):
        self.body += s

    def line(self, x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, obstacle=True):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.body += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
        if obstacle:
            self.segs.append((x1, y1, x2, y2))

    def dot(self, x, y, r=4, c="currentColor"):
        self.body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'

    def arr(self, tag, c, x1, y1, x2, y2, w=3, head=11, dash=""):
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        ex, ey = x2 - ux * head, y2 - uy * head
        self.markers.add((c, head))
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.body += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{COL[c]}" stroke-width="{w}"{d} '
                      f'marker-end="url(#{self.name}-{c}{head})"/>')
        self.arrows[tag] = (x1, y1, x2, y2)
        self.segs.append((x1, y1, x2, y2))

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

    def check(self):
        errs = []
        for i, a in enumerate(self.labels):
            if a[5] < 17:
                errs.append(f"{self.name}: nhãn '{a[0]}' cỡ {a[5]} < 17")
            if a[1] < 2 or a[3] > self.w - 2 or a[2] < 0 or a[4] > self.h:
                errs.append(f"{self.name}: nhãn '{a[0]}' vượt viewBox {a[1:5]}")
            for b in self.labels[i + 1:]:
                if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    errs.append(f"{self.name}: nhãn '{a[0]}' chồng '{b[0]}'")
            # nét cắt xuyên hộp nhãn (lấy mẫu mỗi 1 đơn vị)
            for (x1, y1, x2, y2) in self.segs:
                n = max(2, int(math.hypot(x2 - x1, y2 - y1)))
                for k in range(n + 1):
                    px, py = x1 + (x2 - x1) * k / n, y1 + (y2 - y1) * k / n
                    if a[1] - 1 < px < a[3] + 1 and a[2] < py < a[4]:
                        errs.append(f"{self.name}: nét cắt xuyên nhãn '{a[0]}' tại ({px:.0f},{py:.0f})")
                        break
        return errs

    def svg(self, label, cap, exp=None):
        s = wrap(f"0 0 {self.w} {self.h}", label, self.defs() + self.body, cap)
        if exp:
            s = s.replace('<figure class="fig" data-tl="1">', f'<figure class="fig" data-tl="1" data-exp="{exp}">', 1)
        return s




ERR = []


def ok(cond, msg):
    if not cond:
        ERR.append(msg)


def q(x, n):
    return D(x).quantize(D(1).scaleb(-n), rounding=ROUND_HALF_UP)


def fmt(x, n):
    """Decimal -> chuỗi dấu phẩy, làm tròn half-up n chữ số."""
    return str(q(x, n)).replace(".", ",")


XICH = D("0.5")        # 1 cm ứng với 0,5 N
DF = D("0.1")          # sai số mỗi lực kế (một độ chia)
DELTA_BIG = 3 * DF     # Δ = ΔF1 + ΔF2 + ΔF3


def F_cong_thuc(f1, f2, al):
    return math.sqrt(f1 * f1 + f2 * f2 + 2 * f1 * f2 * math.cos(math.radians(al)))


def lan(f1, f2, al, f3, so0=0):
    f1, f2, f3, so0 = D(f1), D(f2), D(f3), D(so0)
    F = F_cong_thuc(float(f1), float(f2), al)
    cheo = q(D(repr(F)) / XICH, 1)               # đo chéo tới 1 mm
    fve = cheo * XICH
    f3d = f3 - so0                                # F3 sau khi trừ số 0 lệch
    dl, dl2 = abs(fve - f3), abs(fve - f3d)
    # độ nhạy của F theo góc ±1° (N)
    sens = float(f1) * float(f2) * math.sin(math.radians(al)) / F * math.radians(1)
    return dict(f1=f1, f2=f2, al=al, f3=f3, so0=so0, F=F, cheo=cheo, fve=fve, f3d=f3d, dl=dl, dl2=dl2, sens=sens)


A = [lan("1.6", "2.1", 80, "2.9"), lan("2.0", "2.0", 60, "3.5"), lan("1.4", "1.6", 110, "2.1", "0.3")]
ok([str(r["cheo"]) for r in A] == ["5.7", "6.9", "3.5"], [str(r["cheo"]) for r in A])
ok([str(r["fve"]) for r in A] == ["2.85", "3.45", "1.75"], [str(r["fve"]) for r in A])
ok([str(r["dl"]) for r in A] == ["0.05", "0.05", "0.35"], [str(r["dl"]) for r in A])
ok([str(r["dl2"]) for r in A] == ["0.05", "0.05", "0.05"], [str(r["dl2"]) for r in A])
ok(A[0]["dl"] <= DELTA_BIG and A[1]["dl"] <= DELTA_BIG and A[2]["dl"] > DELTA_BIG and A[2]["dl2"] <= DELTA_BIG, "TN1: lần 1,2 trong Δ; lần 3 vượt rồi hết sau trừ số 0")
ok(all(r["sens"] < 0.03 for r in A), [r["sens"] for r in A])
ok(max(r["dl"] for r in A) == A[2]["dl"] and DELTA_BIG == D("0.3"), "Δ")
ok(all(abs(float(r["f3d"]) - r["F"]) <= 0.2 for r in A), "F3 (đã trừ số 0) lệch F công thức không quá 0,2 N")
ok(all(r["f3d"] != r["f3"] for r in A[2:]) and A[2]["f3"] - A[2]["so0"] == D("1.8"), "lần 3 sau trừ số 0")
# nối ba cột bảng: F vẽ trong bài viết
ok(abs(A[1]["F"] - 3.4641) < 1e-3, "lần 2 công thức")

# Quiz 2 (Câu 1): 1,2 và 1,6 vuông góc
ok(round(F_cong_thuc(1.2, 1.6, 90), 3) == 2.0 and D("1.2") + D("1.6") == D("2.8") and D("1.6") - D("1.2") == D("0.4") and (D("1.2") + D("1.6")) / 2 == D("1.4"), "Q2")
# Quiz 3 (Câu 2): 1,0 ; 1,0 ; 90° ; F3 = 1,9
Q3 = lan("1.0", "1.0", 90, "1.9")
ok(str(Q3["cheo"]) == "2.8" and str(Q3["fve"]) == "1.40" and str(Q3["dl"]) == "0.50" and Q3["dl"] > DELTA_BIG, ("Q3", Q3["cheo"], Q3["fve"], Q3["dl"]))
ok(D("1.0") / XICH == D("2.0"), "Q3 cạnh")
# Quiz 4 (Câu 3) chỉ định tính
# Quiz 5 (Câu 4): 2,0 ; 3,0 ; 120°
ok(round(F_cong_thuc(2, 3, 120) ** 2, 6) == 7.0 and q(D(repr(F_cong_thuc(2, 3, 120))), 1) == D("2.6"), "Q5 B")
ok(str(q(D(repr(F_cong_thuc(2, 3, 60))), 1)) == "4.4" and str(q(D(repr(F_cong_thuc(2, 3, 90))), 1)) == "3.6" and 2 + 3 == 5, "Q5 C,D,A")
ok(2 * 2 + 3 * 3 + 2 * 2 * 3 * math.cos(math.radians(120)) > 6.999 and 13 - 6 == 7, "Q5 phép tính")
# Quiz 7 (Câu 6): 2,0 ; 2,0 ; 60° -> 90°
ok(round(F_cong_thuc(2, 2, 60), 2) == 3.46 and round(F_cong_thuc(2, 2, 90), 2) == 2.83, "Q7")
# Bài toán mẫu
ok(D("1.8") / XICH == D("3.6") and D("2.4") / XICH == D("4.8") and math.isclose(math.hypot(3.6, 4.8), 6.0), "mẫu: cạnh, chéo")
M = lan("1.8", "2.4", 90, "3.1")
ok(str(M["cheo"]) == "6.0" and str(M["fve"]) == "3.00" and str(M["dl"]) == "0.10" and M["dl"] < DELTA_BIG, ("M", M["cheo"], M["fve"], M["dl"]))
ok(math.isclose(math.hypot(1.8, 2.4), 3.0), "mẫu: F công thức")
# Điền bước thiếu
Fb = lan("1.5", "2.0", 90, "2.6")
ok(D("1.5") / XICH == D("3.0") and D("2.0") / XICH == D("4.0") and str(Fb["cheo"]) == "5.0" and str(Fb["fve"]) == "2.50" and str(Fb["dl"]) == "0.10" and Fb["dl"] < DELTA_BIG, ("Fb", Fb["dl"]))
# Thử sức đổi góc
ok(round(F_cong_thuc(2, 2, 120), 6) == 2.0 and round(2 * 2 * math.cos(math.radians(60)), 6) == 2.0 and D("2.0") / XICH == D("4.0"), "đổi góc")
# Thử thách
ok(math.isclose(math.hypot(3, 4), 5.0), "⭐")
ok(math.isclose(1.5 ** 2, 2 * 1.5 ** 2 * (1 + math.cos(math.radians(120)))), "⭐⭐")

# ================= TN3: treo vật bằng hai dây, T = P/(2cos(α/2))
P3 = D("2.0")
TN3 = []
for al in (60, 90, 120, 150):
    T = float(P3) / (2 * math.cos(math.radians(al / 2)))
    TN3.append((al, D(repr(T)), T / float(P3) * 100))
ok([str(q(t, 2)) for _, t, _ in TN3] == ["1.15", "1.41", "2.00", "3.86"], [str(q(t, 2)) for _, t, _ in TN3])
ok([f"{p:.0f}" for _, _, p in TN3] == ["58", "71", "100", "193"], [f"{p:.0f}" for _, _, p in TN3])

# ================= TN2: hai lực song song cùng chiều
L_THANH, P2 = 60, D("3.0")
TN2 = []
for dA in (10, 20, 30):
    dB = L_THANH - dA
    FA = q(P2 * dB / L_THANH, 1)
    FB = q(P2 * dA / L_THANH, 1)
    TN2.append((dA, dB, FA, FB))
ok([(str(a), str(b)) for _, _, a, b in TN2] == [("2.5", "0.5"), ("2.0", "1.0"), ("1.5", "1.5")], TN2)
ok(all(a + b == P2 for _, _, a, b in TN2), "ΣF = P")
ok(all(a * dA == b * dB for dA, dB, a, b in TN2), "moment")

# ================= Hình 1: bố trí thí nghiệm
c = Canvas("f1", 420, 310)
c.add('<rect x="12" y="48" width="396" height="252" rx="4" fill="rgba(128,128,128,.12)" stroke="currentColor" stroke-width="1.6"/>')
c.add('<rect x="80" y="28" width="272" height="8" fill="rgba(128,128,128,.35)" stroke="currentColor" stroke-width="2"/>')
P1, P2c, O = (96, 40), (324, 40), (210, 176)
for px, py in (P1, P2c):
    c.add(f'<circle cx="{px}" cy="{py}" r="4" fill="currentColor"/>')
    c.add(f'<line x1="{px}" y1="36" x2="{px}" y2="{py}" stroke="currentColor" stroke-width="2"/>')
c.line(P1[0], P1[1], O[0], O[1], "currentColor", 2)
c.line(P2c[0], P2c[1], O[0], O[1], "currentColor", 2)
ang = math.degrees(math.atan2(O[0] - P1[0], O[1] - P1[1]))
for (px, py), sgn in ((P1, -1), (P2c, 1)):
    cx, cy = px + (O[0] - px) * 0.4, py + (O[1] - py) * 0.4
    c.add(f'<g transform="rotate({sgn * ang:.1f} {cx:.1f} {cy:.1f})"><rect x="{cx - 8:.1f}" y="{cy - 24:.1f}" width="16" height="48" rx="3" '
          f'fill="rgba(56,189,248,.25)" stroke="currentColor" stroke-width="2"/><line x1="{cx - 8:.1f}" y1="{cy:.1f}" x2="{cx + 8:.1f}" y2="{cy:.1f}" stroke="currentColor" stroke-width="1.6"/></g>')
c.line(O[0], O[1], O[0], 200, "currentColor", 2)
c.add('<rect x="202" y="200" width="16" height="46" rx="3" fill="rgba(56,189,248,.25)" stroke="currentColor" stroke-width="2"/>')
c.add('<line x1="202" y1="223" x2="218" y2="223" stroke="currentColor" stroke-width="1.6"/>')
c.line(O[0], 246, O[0], 258, "currentColor", 2)
c.add('<rect x="190" y="258" width="40" height="30" rx="3" fill="rgba(251,146,60,.30)" stroke="currentColor" stroke-width="2"/>')
c.add(f'<circle cx="{O[0]}" cy="{O[1]}" r="5" fill="{RED}" stroke="currentColor" stroke-width="1.4"/>')
r = 36
ux, uy = (P1[0] - O[0]) / math.hypot(P1[0] - O[0], P1[1] - O[1]), (P1[1] - O[1]) / math.hypot(P1[0] - O[0], P1[1] - O[1])
ax, ay = O[0] + r * ux, O[1] + r * uy
c.add(f'<path d="M{ax:.1f},{ay:.1f} A{r},{r} 0 0 1 {2 * O[0] - ax:.1f},{ay:.1f}" fill="none" stroke="{RED}" stroke-width="2.4"/>')
c.text(205, 134, "α", size=18, italic=True, anchor="middle")
c.text(12, 40, "giá đỡ", size=17)
c.text(20, 122, "lực kế 1", size=17)
c.text(400, 122, "lực kế 2", size=17, anchor="end")
c.text(222, 196, "nút O", size=17)
c.text(192, 232, "lực kế 3", size=17, anchor="end")
c.text(238, 280, "vật nặng", size=17)
c.text(20, 292, "bảng giấy", size=17)
ok(O[1] > P1[1] and O[0] - P1[0] == P2c[0] - O[0], "f1: nút O đối xứng dưới hai chốt")
ERR += c.check()
fig1 = c.svg("Sơ đồ bố trí thí nghiệm tổng hợp lực: hai lực kế 1 và 2 móc vào hai chốt trên giá đỡ, hai dây nghiêng gặp nhau ở nút O; từ nút O một dây thẳng đứng đi xuống qua lực kế 3 tới vật nặng; góc alpha là góc giữa hai dây ở nút O; nền là bảng giấy",
             "Hình 1. Bố trí thí nghiệm. Ba dây gặp nhau ở nút O; vật nặng kéo nút O xuống qua lực kế 3. Góc <em>α</em> là góc giữa hai dây ở O.",
             exp="tn-l10-thuchanhthl-01")

# ================= Hình 2: hình bình hành lần 2 (F1 = F2 = 2,0 N, α = 60°)
c = Canvas("f2", 420, 310)
PX = 18                                   # px mỗi cm; 1 cm ứng 0,5 N
O = (210, 170)
side = float(D("2.0") / XICH) * PX        # 4,0 cm
s30, c30 = math.sin(math.radians(30)), math.cos(math.radians(30))
e1 = (O[0] - side * s30, O[1] - side * c30)
e2 = (O[0] + side * s30, O[1] - side * c30)
tip = (O[0], O[1] - 2 * side * c30)
f3len = float(A[1]["f3"] / XICH) * PX
c.line(e1[0], e1[1], tip[0], tip[1], "currentColor", 1.8, "6 4", 0.7, obstacle=False)
c.line(e2[0], e2[1], tip[0], tip[1], "currentColor", 1.8, "6 4", 0.7, obstacle=False)
c.arr("f1", "r", O[0], O[1], e1[0], e1[1], 3, 11)
c.arr("f2", "r", O[0], O[1], e2[0], e2[1], 3, 11)
c.arr("f", "g", O[0], O[1], tip[0], tip[1], 3, 11)
c.arr("f3", "b", O[0], O[1], O[0], O[1] + f3len, 3, 11)
c.add(f'<circle cx="{O[0]}" cy="{O[1]}" r="4" fill="currentColor"/>')
rr = 28
c.add(f'<path d="M{O[0] - rr * s30:.1f},{O[1] - rr * c30:.1f} A{rr},{rr} 0 0 1 {O[0] + rr * s30:.1f},{O[1] - rr * c30:.1f}" fill="none" stroke="currentColor" stroke-width="1.8"/>')
FI = '<tspan font-style="italic" font-family="serif">F</tspan>'
SUB = lambda n: f'<tspan font-size="13" dy="4">{n}</tspan><tspan dy="-4" font-weight="400">'
c.text(168, 134, f'{FI}{SUB(1)} = 2,0 N</tspan>', anchor="end", size=17)
c.text(252, 134, f'{FI}{SUB(2)} = 2,0 N</tspan>', size=17)
c.text(210, 30, f'{FI}<tspan font-weight="400"> = 3,45 N</tspan>', anchor="middle", size=17)
c.text(224, 246, f'{FI}{SUB(3)} = 3,5 N</tspan>', size=17)
ok(c.arrows["f"][3] < c.arrows["f1"][3] < O[1], "f2: chéo dài hơn cạnh")
ok(c.arrows["f3"][3] > O[1] and abs(c.arrows["f3"][2] - c.arrows["f"][2]) < 1e-6, "f2: F3 ngược chiều F, cùng phương")
ok(abs(math.hypot(tip[0] - O[0], tip[1] - O[1]) / PX - 6.93) < 0.01, "f2: chéo ≈ 6,93 cm")
ok(c.arrows["f3"][3] - O[1] == 126, "f2: F3 vẽ 7,0 cm")
ERR += c.check()
fig2 = c.svg("Hình bình hành lực của lần 2: từ nút O vẽ hai vectơ F1 và F2 bằng nhau, dài 4,0 xentimet, hợp nhau góc 60 độ về hai phía của phương thẳng đứng; hai đường nét đứt hoàn thành hình thoi; đường chéo hướng lên là lực tổng hợp F; vectơ F3 hướng xuống cùng phương và bằng độ lớn với F",
             "Hình 2. Hình bình hành lần 2, tỉ lệ xích 1 cm ứng với 0,5 N; cung nhỏ ở O là góc <em>α</em> = 60°. Đường chéo hướng lên dài 6,9 cm, tức <em>F</em> ≈ 3,45 N; <em>F</em><sub>3</sub> hướng xuống cùng phương và gần bằng độ lớn.",
             exp="tn-l10-thuchanhthl-01")

# ================= Hình 3: độ lệch δ ba lần, đường Δ
c = Canvas("f3", 420, 290)
OX, OY, K = 70, 238, 500
Y = lambda v: OY - K * v
c.arr("tx", "k", OX, OY, 410, OY, 1.8, 9)
c.arr("vy", "k", OX, OY, OX, 22, 1.8, 9)
c.text(78, 24, "δ (N)", size=18, italic=True)
for tv in (0.1, 0.2, 0.3, 0.4):
    c.line(OX - 4, Y(tv), OX + 4, Y(tv), "currentColor", 1.5, obstacle=False)
    c.text(OX - 8, Y(tv) + 5, vn(tv, 1), size=17, anchor="end", weight="600")
c.line(OX, Y(0.3), 408, Y(0.3), GRN, 2.2, "7 5", obstacle=False)
c.text(76, Y(0.3) - 8, "Δ = 0,3 N", GRN, 18, "start")
XS = [120, 200, 280]
for i, (xr, r_) in enumerate(zip(XS, A)):
    h_ = K * float(r_["dl"])
    col = RED if r_["dl"] > DELTA_BIG else ORG
    c.add(f'<rect x="{xr - 20}" y="{OY - h_:.1f}" width="40" height="{h_:.1f}" fill="{col}" fill-opacity=".75" stroke="currentColor" stroke-width="1.6"/>')
    c.text(xr, 262, f"lần {i + 1}", size=17, anchor="middle", weight="600")
yv = Y(float(A[2]["dl2"]))
c.add(f'<circle cx="{XS[2]}" cy="{yv:.1f}" r="6" fill="{GRN}" stroke="currentColor" stroke-width="1.6"/>')
c.line(XS[2] + 8, yv, 304, yv, "currentColor", 1.4, obstacle=False)
c.text(310, yv - 4, "sau khi", size=17)
c.text(310, yv + 14, "trừ số 0", size=17)
ok(A[2]["dl"] > DELTA_BIG and A[0]["dl"] < DELTA_BIG and A[1]["dl"] < DELTA_BIG and A[2]["dl2"] < DELTA_BIG, "f3: chỉ lần 3 vượt Δ, sau trừ số 0 thì dưới")
ok(Y(0.4) > 22, "f3: trục")
ERR += c.check()
fig3 = c.svg("Biểu đồ cột độ lệch delta của ba lần đo: lần 1 và lần 2 là hai cột thấp màu cam cùng 0,05 N, nằm dưới đường nét đứt xanh Delta bằng 0,3 N; lần 3 là cột đỏ cao 0,35 N vượt đường nét đứt; chấm xanh trên cột lần 3 ở 0,05 N là giá trị sau khi trừ số 0 lệch của lực kế 3",
             "Hình 3. Độ lệch <em>δ</em> ba lần đo (số liệu minh hoạ). Đường nét đứt là <em>Δ</em> = 0,3 N; lần 3 (lực kế 3 đổi cái khác, chưa chỉnh số 0) vượt đường cho tới khi trừ số 0 lệch (chấm xanh).",
             exp="tn-l10-thuchanhthl-01")

if ERR:
    print("\n".join("✗ " + str(e) for e in ERR)); sys.exit(1)


# ================= Bảng số liệu
def table(head, rows):
    return ('<div class="table-scroll">\n<table class="tl-table">\n<thead>\n<tr>' + "".join(f"<th>{h}</th>" for h in head)
            + "</tr>\n</thead>\n<tbody>\n" + "\n".join("<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in rows)
            + "\n</tbody>\n</table>\n</div>")


bang_a1 = table(["Lần", "$F_1$ ; $F_2$ (N)", "$\\alpha$ ; $F_3$ (độ ; N)"],
                [[i + 1, f"{fmt(r['f1'], 1)} ; {fmt(r['f2'], 1)}", f"{r['al']}° ; {fmt(r['f3'], 1)}"] for i, r in enumerate(A)])
bang_a2 = table(["Lần", "Chéo → $F$ vẽ", "$\\delta$ ; $\\Delta$ (N)"],
                [[i + 1, f"{fmt(r['cheo'], 1)} cm → {fmt(r['fve'], 2)} N", f"{fmt(r['dl'], 2)} ; {fmt(DELTA_BIG, 2)}"] for i, r in enumerate(A)])
bang_tn3 = table(["$\\alpha$ (độ)", "$T$ mỗi dây (N)", "$T$ so với $P$"],
                 [[al, fmt(t, 2), f"{p:.0f} %"] for al, t, p in TN3])
bang_ss = table(["$d_A$ (cm)", "$F_A$ ; $F_B$ (N)", "$F_Ad_A$ ; $F_Bd_B$ (N·cm)"],
                [[dA, f"{fmt(a, 1)} ; {fmt(b, 1)}", f"{fmt(a * dA, 0)} ; {fmt(b * dB, 0)}"] for dA, dB, a, b in TN2])

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, fg in enumerate((fig1, fig2, fig3), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
for k, v in (("__BANG_A1__", bang_a1), ("__BANG_A2__", bang_a2), ("__BANG_TN3__", bang_tn3), ("__BANG_SS__", bang_ss)):
    assert k in h, k
    h = h.replace(k, v)
assert "__" not in h.replace("__PHUT__", "")
tmp = HERE / ".theory.tmp.html"
tmp.write_text(h.replace("__PHUT__", "15"), encoding="utf8")
lint = ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = subprocess.run([sys.executable, str(lint), str(tmp)], capture_output=True, text=True).stdout
tmp.unlink()
m = re.search(r"~?(\d+(?:[.,]\d+)?)\s*phút", out)
if not m:
    print("! không đọc được số phút từ lint_do_dai:\n" + out[:600]); sys.exit(1)
phut = int(math.ceil(float(m.group(1).replace(",", ".")) - 1e-9))
h = h.replace("__PHUT__", str(phut))
(HERE / "theory.html").write_text(h, encoding="utf8")

# ================= File thí nghiệm
BASE = {"mon": "vat-ly", "lop": 10, "bai": "Bài 22. Thực hành: Tổng hợp lực", "lesson_id": 67,
        "nguon_trong_bai": "content/lesson-samples/l10-thuc-hanh-tong-hop-luc/theory.html"}
fl = float
tn = [
    {**BASE, "id": "tn-l10-thuchanhthl-01",
     "ten": "Tổng hợp hai lực đồng quy bằng ba lực kế: so F vẽ với lực cân bằng đo được",
     "loai": "thi_nghiem", "muc_do": "trung_binh",
     "kien_thuc": ["thuchanhthl.hinh_binh_hanh", "thuchanhthl.luc_can_bang", "thuchanhthl.sai_so_so_sanh", "thuchanhthl.so_0_luc_ke"],
     "muc_tieu": "Tổng hợp F1, F2 bằng hình bình hành theo tỉ lệ xích 1 cm ứng 0,5 N, so F vẽ với F3 đọc trên lực kế 3 qua độ lệch δ và sai số Δ = 0,3 N; nhận ra lần 3 vượt Δ là do đổi sang lực kế 3 khác chưa chỉnh số 0.",
     "dung_cu": [{"ten": "Giá đỡ + bảng giấy", "so_luong": 1}, {"ten": "Lực kế 5 N, độ chia 0,1 N", "so_luong": 3},
                 {"ten": "Dây mảnh buộc nút O", "so_luong": 1}, {"ten": "Vật nặng móc vào lực kế 3", "so_luong": 1},
                 {"ten": "Thước kẻ (1 mm), thước đo độ (1°), bút", "so_luong": 1}],
     "cac_buoc": {"lam": ["Chỉnh số 0 từng lực kế ở đúng tư thế dùng; buộc ba dây vào nút O; hai lực kế móc vào hai chốt trên giá, lực kế 3 treo vật.",
                          "Đợi nút O đứng yên; chấm hai điểm trên mỗi dây để đánh dấu phương; đọc F1, F2, F3 (nhìn thẳng mặt chỉ).",
                          "Lấy giấy ra, nối các chấm qua O, đo góc α giữa hai dây; làm 3 lần, đổi vị trí chốt hoặc đổi vật."],
                  "quan_sat": ["Bảng F1, F2, α, F3 ba lần; nút O đứng yên mỗi lần; F3 giảm khi α tăng nếu F1, F2 giữ nguyên."],
                  "rut_ra": ["Vẽ hình bình hành cạnh F1/0,5 và F2/0,5 cm, hợp góc α; đo chéo (cm), F vẽ = chéo·0,5; δ = |F vẽ − F3|; Δ = ΔF1 + ΔF2 + ΔF3 = 0,3 N.",
                             "Ba lần: δ = " + "; ".join(fmt(r["dl"], 2) for r in A) + " N so với Δ = 0,3 N; lần 3 vượt vì đổi sang lực kế 3 khác chưa chỉnh số 0 (treo thẳng đứng, chưa móc vật chỉ 0,3 N; hai lần đầu lực kế 3 đã chỉnh đúng); trừ số lệch thì F3 = 1,8 N, δ = 0,05 N. Sai số thước (0,05 N) và góc (~0,02 N) không đủ giải thích; vượt sát Δ thì tìm nguyên nhân hệ thống trước khi kết luận."]},
     "tham_so": [{"ky_hieu": "F1", "ten": "Lực kế 1 chỉ", "don_vi": "N", "kieu": "dieu_chinh", "min": 0.5, "max": 2.5, "mac_dinh": 2.0, "buoc": 0.1},
                 {"ky_hieu": "F2", "ten": "Lực kế 2 chỉ", "don_vi": "N", "kieu": "dieu_chinh", "min": 0.5, "max": 2.5, "mac_dinh": 2.0, "buoc": 0.1},
                 {"ky_hieu": "alpha", "ten": "Góc giữa hai dây ở nút O", "don_vi": "độ", "kieu": "dieu_chinh", "min": 0, "max": 180, "mac_dinh": 60, "buoc": 5},
                 {"ky_hieu": "so_0", "ten": "Số 0 lệch của lực kế 3", "don_vi": "N", "kieu": "dieu_chinh", "min": 0, "max": 0.4, "mac_dinh": 0, "buoc": 0.1},
                 {"ky_hieu": "xich", "ten": "Tỉ lệ xích", "don_vi": "N/cm", "kieu": "co_dinh", "gia_tri": 0.5},
                 {"ky_hieu": "dF", "ten": "Sai số một lực kế (độ chia)", "don_vi": "N", "kieu": "co_dinh", "gia_tri": 0.1},
                 {"ky_hieu": "F3", "ten": "Lực kế 3 chỉ (treo vật)", "don_vi": "N", "kieu": "do_duoc", "sai_so_do": 0.1},
                 {"ky_hieu": "F_ve", "ten": "Lực tổng hợp đo trên hình vẽ", "don_vi": "N", "kieu": "tinh_ra"},
                 {"ky_hieu": "delta", "ten": "Độ lệch |F vẽ − F3|", "don_vi": "N", "kieu": "tinh_ra"},
                 {"ky_hieu": "Delta", "ten": "Sai số gộp ΔF1 + ΔF2 + ΔF3", "don_vi": "N", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["F = sqrt(F1² + F2² + 2·F1·F2·cos α) (α là góc giữa hai lực chung gốc O)", "chéo (cm) = F/0,5 làm tròn 0,1 cm; F vẽ = chéo·0,5",
                                  "F3 (lý tưởng) = F vì nút O đứng yên: F3 cân bằng với F", "F3 đọc = F3 thật + số 0 lệch", "δ = |F vẽ − F3 đọc|; Δ = 3·0,1 = 0,3 N (cận trên: ΔF vẽ ≤ ΔF1 + ΔF2)"],
                 "gia_thiet": ["dây không dãn, bỏ qua ma sát ở nút", "sai số góc ±1° gây dưới 0,03 N trong ba lần đo nên bỏ qua", "số liệu F1, F2, F3 là số đọc minh hoạ (độ chia 0,1 N), F3 thật lệch công thức không quá 0,2 N", "F1, F2 tối đa 2,5 N để F3 ≈ F không vượt thang lực kế 5 N"]},
     "so_lieu_mau": {"cot": ["Lần", "F1 (N)", "F2 (N)", "α (độ)", "F3 đọc (N)", "số 0 lệch (N)", "chéo (cm)", "F vẽ (N)", "δ (N)", "Δ (N)"],
                     "hang": [[i + 1, fl(r["f1"]), fl(r["f2"]), r["al"], fl(r["f3"]), fl(r["so0"]), fl(r["cheo"]), fl(r["fve"]), fl(r["dl"]), 0.3] for i, r in enumerate(A)],
                     "ghi_chu": "Số liệu minh hoạ, không phải đo thật. Lần 3: đổi sang lực kế 3 khác chưa chỉnh số 0, F3 đọc 2,1 N gồm số 0 lệch 0,3 N (hai lần đầu số 0 đã chỉnh đúng); trừ ra 1,8 N thì δ = 0,05 N. Lần 1, 2: δ ≤ Δ; lần 3 (chưa trừ): δ = 0,35 N > Δ."},
     "ket_qua_ky_vong": "Hai lần δ ≤ Δ ngay; lần 3 vượt Δ do dùng lực kế 3 khác chưa chỉnh số 0 và hết vượt sau khi trừ số lệch: hợp quy tắc hình bình hành trong sai số.",
     "hien_tuong_hay_sai": ["Cộng hai độ lớn F1 + F2 như hai lực cùng phương, cùng chiều.", "Dùng góc bù 180° − α khi vẽ hai lực chung gốc.", "Quên chỉnh số 0 đúng tư thế rồi coi δ > Δ là quy tắc sai.", "Cho rằng lực tổng hợp F cùng chiều với F3 thay vì ngược chiều."],
     "sai_so_thuong_gap": "Số 0 lực kế lệch khi đổi tư thế; chấm phương dây không chính xác; đọc số nhìn xiên mặt chỉ; nút O chưa đứng yên; thước đo độ đặt lệch tâm O.",
     "an_toan": "Vật nặng móc chắc vào lực kế, không đứng dưới vật khi treo.",
     "goi_y_mo_phong": {"loai": "so_do_luc+bang_so_lieu",
                        "y_tuong": "Nút O trên bảng; kéo hai lực kế quanh O đổi F1, F2, α; vẽ hình bình hành, lực kế 3 hiện F; bảng tự tính chéo, F vẽ, δ, Δ.",
                        "diem_nhan": "Thanh trượt 'số 0 lệch' của lực kế 3: kéo lên thì δ vượt Δ; đặt về 0 thì δ trở lại dưới Δ."}},
    {**BASE, "id": "tn-l10-thuchanhthl-02",
     "ten": "Tổng hợp hai lực song song cùng chiều bằng thanh nhẹ và hai lực kế",
     "loai": "thi_nghiem", "muc_do": "trung_binh",
     "kien_thuc": ["thuchanhthl.luc_song_song", "thuchanhthl.quy_tac_momen_hai_luc"],
     "muc_tieu": "Thấy hợp lực hai lực song song cùng chiều bằng tổng độ lớn và đặt tại điểm treo vật; F_A·d_A = F_B·d_B.",
     "dung_cu": [{"ten": "Thanh nhẹ AB dài 60 cm (trọng lượng nhỏ hơn 0,1 N)", "so_luong": 1}, {"ten": "Lực kế 5 N, độ chia 0,1 N", "so_luong": 2},
                 {"ten": "Vật nặng 3,0 N có móc", "so_luong": 1}, {"ten": "Giá đỡ, dây treo, thước", "so_luong": 1}],
     "cac_buoc": {"lam": ["Chỉnh số 0 hai lực kế khi treo thẳng đứng; treo hai đầu thanh AB vào hai lực kế, thanh nằm ngang.",
                          "Treo vật P = 3,0 N cách A một đoạn d_A = 10; 20; 30 cm, đọc F_A và F_B."],
                  "quan_sat": ["F_A + F_B = 3,0 N mọi lần; lực kế ở đầu gần vật chỉ lớn hơn."],
                  "rut_ra": ["Hợp lực F = F_A + F_B = P đặt tại điểm treo vật; F_A·d_A = F_B·d_B (d_B = 60 − d_A)."]},
     "tham_so": [{"ky_hieu": "dA", "ten": "Khoảng cách từ A tới điểm treo vật", "don_vi": "cm", "kieu": "dieu_chinh", "min": 5, "max": 55, "mac_dinh": 20, "buoc": 5},
                 {"ky_hieu": "P", "ten": "Trọng lượng vật", "don_vi": "N", "kieu": "dieu_chinh", "min": 1.0, "max": 5.0, "mac_dinh": 3.0, "buoc": 0.5},
                 {"ky_hieu": "L", "ten": "Chiều dài thanh", "don_vi": "cm", "kieu": "co_dinh", "gia_tri": 60},
                 {"ky_hieu": "FA", "ten": "Lực kế A chỉ", "don_vi": "N", "kieu": "do_duoc", "sai_so_do": 0.1},
                 {"ky_hieu": "FB", "ten": "Lực kế B chỉ", "don_vi": "N", "kieu": "do_duoc", "sai_so_do": 0.1}],
     "mo_hinh": {"phuong_trinh": ["d_B = L − d_A", "F_A = P·d_B/L; F_B = P·d_A/L", "F_A + F_B = P; F_A·d_A = F_B·d_B"],
                 "gia_thiet": ["thanh nhẹ, bỏ qua trọng lượng thanh", "số đọc làm tròn 0,1 N, ba vị trí chọn để tích F·d là số nguyên"]},
     "so_lieu_mau": {"cot": ["d_A (cm)", "d_B (cm)", "F_A (N)", "F_B (N)", "F_A·d_A (N·cm)", "F_B·d_B (N·cm)"],
                     "hang": [[dA, dB, fl(a), fl(b), fl(a * dA), fl(b * dB)] for dA, dB, a, b in TN2],
                     "ghi_chu": "Số liệu minh hoạ tính từ mô hình thanh nhẹ, không phải đo thật."},
     "ket_qua_ky_vong": "F_A + F_B = 3,0 N ở cả ba vị trí; F_A·d_A = F_B·d_B.",
     "hien_tuong_hay_sai": ["Lấy hiệu hai lực như hai lực ngược chiều.", "Quên đổi d_B = L − d_A.", "Cho rằng điểm đặt của hợp lực nằm giữa thanh bất kể vị trí treo vật."],
     "sai_so_thuong_gap": "Số 0 lực kế chỉnh sai tư thế; thanh không thật nằm ngang; trọng lượng thanh không nhỏ.",
     "goi_y_mo_phong": {"loai": "so_do_luc+bang_so_lieu",
                        "y_tuong": "Thanh AB, vật trượt dọc thanh; hai lực kế hiện F_A, F_B; bảng tính tổng và mô-men.",
                        "diem_nhan": "Kéo vật về phía A: F_A tăng, F_B giảm, tổng vẫn bằng P."}},
    {**BASE, "id": "tn-l10-thuchanhthl-03",
     "ten": "Treo vật bằng hai dây: lực căng mỗi dây tăng khi góc giữa hai dây tăng",
     "loai": "vi_du", "muc_do": "co_ban",
     "kien_thuc": ["thuchanhthl.hinh_binh_hanh", "thuchanhthl.luc_cang_hai_day"],
     "muc_tieu": "Thấy lực căng mỗi dây T = P/(2cos(α/2)) tăng theo α và bằng P khi α = 120°; hai lực tổng hợp luôn bằng P.",
     "dung_cu": [{"ten": "Vật nặng 2,0 N", "so_luong": 1}, {"ten": "Hai dây giống nhau + hai lực kế 5 N", "so_luong": 1}, {"ten": "Hai móc dời được trên giá", "so_luong": 1}],
     "cac_buoc": {"lam": ["Treo vật P = 2,0 N bằng hai dây giống nhau, đối xứng, hai lực kế đo lực căng T.", "Dời hai móc để α = 60°, 90°, 120°, 150° và đọc T."],
                  "quan_sat": ["T tăng dần theo α: 1,15; 1,41; 2,00; 3,86 N."],
                  "rut_ra": ["T = P/(2cos(α/2)); hai lực T tổng hợp bằng P hướng lên; α = 120° thì T = P."]},
     "tham_so": [{"ky_hieu": "alpha", "ten": "Góc giữa hai dây", "don_vi": "độ", "kieu": "dieu_chinh", "min": 0, "max": 160, "mac_dinh": 60, "buoc": 10},
                 {"ky_hieu": "P", "ten": "Trọng lượng vật", "don_vi": "N", "kieu": "dieu_chinh", "min": 0.5, "max": 4.0, "mac_dinh": 2.0, "buoc": 0.5},
                 {"ky_hieu": "T", "ten": "Lực căng mỗi dây", "don_vi": "N", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["2·T·cos(α/2) = P", "T = P/(2cos(α/2))"], "gia_thiet": ["hai dây giống nhau, đối xứng, dây không dãn", "số liệu tính từ mô hình, làm tròn 0,01 N"]},
     "so_lieu_mau": {"cot": ["α (độ)", "T (N)", "T so với P (%)"], "hang": [[al, fl(q(t, 2)), fl(q(D(repr(p)), 0))] for al, t, p in TN3],
                     "ghi_chu": "Số liệu minh hoạ tính từ mô hình, không phải đo thật. P = 2,0 N."},
     "ket_qua_ky_vong": "T tăng từ 1,15 N (α = 60°) lên 3,86 N (α = 150°); bằng P tại α = 120°.",
     "hien_tuong_hay_sai": ["Cho rằng mỗi dây luôn chịu P/2.", "Cho rằng dây xoạc ra thì lực căng giảm."],
     "goi_y_mo_phong": {"loai": "so_do_luc+do_thi",
                        "y_tuong": "Khung ảnh treo bằng hai dây, kéo hai đinh xa nhau; hai mũi tên T và hình bình hành lực; đồ thị T theo α.",
                        "diem_nhan": "Kéo α lên gần 180° thì T tăng rất nhanh; dây phơi căng thẳng thì dễ đứt."}},
]
for d in tn:
    (ROOT / "content/thi-nghiem" / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf8")

# kiểm giản lược như thi_nghiem.py (không ghi index.json)
BAT_BUOC = ["id", "ten", "loai", "muc_do", "mon", "lop", "bai", "kien_thuc", "muc_tieu", "dung_cu", "cac_buoc", "tham_so", "mo_hinh", "so_lieu_mau", "ket_qua_ky_vong", "hien_tuong_hay_sai", "goi_y_mo_phong"]
SIM = {"2d_dong_hoc", "so_do_luc", "do_thi", "bang_so_lieu"}
for d in tn:
    assert all(k in d for k in BAT_BUOC), d["id"]
    assert d["muc_do"] in {"co_ban", "trung_binh", "nang_cao"} and d["loai"] in {"thi_nghiem", "vi_du"}
    assert all(len(r) == len(d["so_lieu_mau"]["cot"]) for r in d["so_lieu_mau"]["hang"]), d["id"]
    assert any(t["kieu"] == "dieu_chinh" for t in d["tham_so"])
    assert all(re.fullmatch(r"[a-z0-9_]+\.[a-z0-9_]+", k) for k in d["kien_thuc"])
    assert d["goi_y_mo_phong"]["loai"].split("+")[0] in SIM
    assert 'data-exp="' + d["id"] + '"' in h, d["id"]
print(f"ok theory.html {len(h)} ký tự · 3 hình · {phut} phút · 3 file thí nghiệm")
