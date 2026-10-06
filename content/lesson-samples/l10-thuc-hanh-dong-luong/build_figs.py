"""Sinh 3 hình SVG + các bảng số liệu cho bài 'Thực hành: Xác định động lượng của vật trước và sau va chạm' (lesson 75),
thay mốc <!--FIGn-->, __BANG_*__, __PHUT__ trong theory.src.html -> theory.html,
và ghi 3 file thí nghiệm content/thi-nghiem/tn-l10-thuchanhdl-0{1,2,3}.json (số liệu tính từ cùng mô hình, làm tròn half-up bằng Decimal).
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


def sg(x, n=4):
    x = q(x, n)
    return ("+" if x > 0 else "−" if x < 0 else "") + str(abs(x)).replace(".", ",")


S = D("0.0500")
DM = D("0.001")
DT = D("0.001")


# ================= Mô hình số liệu TN1 (va chạm mềm): xe 2 đứng yên
def va_cham_mem(m1, m2, t1, tp):
    m1, m2, t1, tp = map(D, (m1, m2, t1, tp))
    v1 = q(S / t1, 3)
    p = q(m1 * v1, 4)
    vp = q(S / tp, 3)
    pp = q((m1 + m2) * vp, 4)
    dl = abs(pp - p) / p
    eps = DM / m1 + DT / t1 + 2 * DM / (m1 + m2) + DT / tp
    return dict(m1=m1, m2=m2, t1=t1, tp=tp, v1=v1, p=p, vp=vp, pp=pp, delta=dl, eps=eps, ratio=pp / p)


A = [va_cham_mem("0.205", "0.198", "0.099", "0.199"),
     va_cham_mem("0.405", "0.198", "0.101", "0.153"),
     va_cham_mem("0.405", "0.398", "0.105", "0.214")]
for r, (v1, p, vp, pp) in zip(A, [("0.505", "0.1035", "0.251", "0.1012"), ("0.495", "0.2005", "0.327", "0.1972"),
                                  ("0.476", "0.1928", "0.234", "0.1879")]):
    ok((str(r["v1"]), str(r["p"]), str(r["vp"]), str(r["pp"])) == (v1, p, vp, pp), ("A", r))
ok([fmt(r["delta"] * 100, 1) for r in A] == ["2,2", "1,6", "2,5"], [fmt(r["delta"] * 100, 1) for r in A])
ok([fmt(r["eps"] * 100, 1) for r in A] == ["2,5", "2,2", "1,9"], [fmt(r["eps"] * 100, 1) for r in A])
ok(all(r["pp"] < r["p"] for r in A), "TN1: cả 3 lần p' < p (hệ thống)")
ok(A[0]["delta"] <= A[0]["eps"] and A[1]["delta"] <= A[1]["eps"] and A[2]["delta"] > A[2]["eps"], "TN1: lần 1,2 trong sai số, lần 3 vượt")
# Lần 1 trong bài: các thành phần ε
r = A[0]
ok(f"{DM / r['m1'] + DT / r['t1']:.4f}" == "0.0150" and f"{2 * DM / (r['m1'] + r['m2']) + DT / r['tp']:.4f}" == "0.0100", "ε lần 1")
ok(r["m1"] + r["m2"] == D("0.403"), "m1+m2 lần 1")

# ================= TN2 (hai xe đẩy nhau)
def day_nhau(m1, m2, t1, t2):
    m1, m2, t1, t2 = map(D, (m1, m2, t1, t2))
    v1, v2 = q(S / t1, 3), q(S / t2, 3)
    p1, p2 = -q(m1 * v1, 4), q(m2 * v2, 4)
    P = p1 + p2
    dP = abs(p1) * (DM / m1 + DT / t1) + abs(p2) * (DM / m2 + DT / t2)
    return dict(m1=m1, m2=m2, t1=t1, t2=t2, v1=v1, v2=v2, p1=p1, p2=p2, P=P, dP=dP)


B = [day_nhau("0.205", "0.198", "0.205", "0.195"),
     day_nhau("0.405", "0.198", "0.404", "0.200"),
     day_nhau("0.205", "0.398", "0.205", "0.402")]
ok([sg(b["P"]) for b in B] == ["+0,0007", "−0,0007", "−0,0006"], [sg(b["P"]) for b in B])
ok(all(abs(b["P"]) <= b["dP"] for b in B), "TN2: |p'| ≤ Δp' cả 3 lần")
ok([fmt(b["dP"], 4) for b in B] == ["0,0010", "0,0007", "0,0007"], [fmt(b["dP"], 4) for b in B])

# ================= Số liệu trong quiz / bài giải
ok(str(q(S / D("0.099"), 3)) == "0.505" and str(q(D("0.205") * D("0.505"), 4)) == "0.1035", "lần 1 bước 1")
ok(str(q(D("0.403") * D("0.251"), 4)) == "0.1012" and fmt(D("0.1035") - D("0.1012"), 4) == "0,0023", "lần 1 bước 2")
# Q2: p = 0,405 * 0,476 = 0,1928; s = 5 cm -> 100 lần
ok(str(q(D("0.405") * q(S / D("0.105"), 3), 3)) == "0.193", "Q2")
ok(str(q(D("0.405") * (D("0.403") * 0 + 0), 3)) == "0.000" or True, "")
ok(str(q((D("0.405") + D("0.398")) * q(S / D("0.105"), 3), 3)) == "0.382", "Q2 B: 0,803 x 0,476 = 0,382")
ok(str(q(D("0.405") * D("0.05") * D("0.105"), 4)) == "0.0021", "Q2 C: m·s·t")
ok(str(q(D("0.405") * D("5.00") / D("0.105"), 1)) == "19.3", "Q2 A: s = 5,00 cm chưa đổi")
# Q3: t1' = t2' * m1/m2
ok(D("0.150") * D("0.300") / D("0.150") == D("0.300") and D("0.150") / 2 == D("0.075") and D("0.150") * 3 == D("0.450"), "Q3")
# Q4: chiều dương sang trái
ok(D("0.250") * D("0.400") == D("0.100") and D("0.500") * D("0.200") == D("0.100"), "Q4")
# Q5
ok(str(q((D("0.205") + D("0.398")) * D("0.170"), 3)) == "0.103" and str(q(D("0.205") * D("0.170"), 4)) == "0.0349"
   and str(q(D("0.398") * D("0.170"), 4)) == "0.0677" and (D("0.205") + D("0.398")) == D("0.603"), "Q5")
# Q7 (lý thuyết): v' = m1/(m1+m2) v1 không đổi khi nhân đôi cả hai m
ok(D("0.205") / (D("0.205") + D("0.198")) == D("0.410") / (D("0.410") + D("0.396")), "Q7")
# Bài toán mẫu
M = va_cham_mem("0.305", "0.200", "0.083", "0.140")
ok((str(M["v1"]), str(M["p"]), str(M["vp"]), str(M["pp"])) == ("0.602", "0.1836", "0.357", "0.1803"), M)
ok(fmt(M["delta"] * 100, 1) == "1,8" and fmt(M["eps"] * 100, 1) == "2,6", (M["delta"], M["eps"]))
ok(f"{DM / D('0.305') + DT / D('0.083'):.4f}" == "0.0153" and f"{2 * DM / D('0.505') + DT / D('0.140'):.4f}" == "0.0111", "ε bài mẫu")
ok(M["delta"] < M["eps"], "bài mẫu: trong sai số")
F = va_cham_mem("0.405", "0.398", "0.110", "0.221")
ok((str(F["v1"]), str(F["p"]), str(F["vp"]), str(F["pp"])) == ("0.455", "0.1843", "0.226", "0.1815"), F)
ok(fmt(F["delta"] * 100, 1) == "1,5" and fmt(F["eps"] * 100, 1) == "1,9" and F["delta"] < F["eps"], (F["delta"], F["eps"]))
# thử sức đổi chiều
pt = D("0.205") * D("0.500") - D("0.198") * D("0.250")
ok(str(pt) == "0.053000" and str(q(pt / D("0.403"), 4)) == "0.1315" and str(q(S / q(pt / D("0.403"), 4), 3)) == "0.380", (pt,))
# thử thách
ok(q(D("0.205") * q(S / D("0.125"), 3) / D("0.410"), 3) == D("0.200") and q(S / D("0.125"), 3) == D("0.400"), "⭐")
ok(q(D("0.250") * D("0.250") / D("0.400") * 0 + D("0.250") * D("0.250") / D("0.400"), 5) == D("0.15625"), "⭐⭐")

# ================= TN3: băng nghiêng
G = 9.8
L_BANG, X_BANG, V_CONG = 1.20, 0.300, 0.505
NG = []
for h in (2, 4, 6):
    a = G * h / 1000 / L_BANG
    vc = math.sqrt(V_CONG ** 2 + 2 * a * X_BANG)
    NG.append((h, a, vc, (vc / V_CONG - 1) * 100))
ok([f"{a:.3f}" for _, a, _, _ in NG] == ["0.016", "0.033", "0.049"], [a for _, a, _, _ in NG])
ok([f"{p:.1f}" for _, _, _, p in NG] == ["1.9", "3.8", "5.6"], [p for _, _, _, p in NG])

# ================= Hình 1: bố trí thí nghiệm 1
c = Canvas("f1", 420, 272)
c.add('<rect x="16" y="190" width="388" height="14" fill="rgba(128,128,128,.25)" stroke="currentColor" stroke-width="2"/>')
for xc, nm in ((68, "xe 1"), (218, "xe 2")):
    c.add(f'<rect x="{xc - 28}" y="160" width="56" height="26" rx="3" fill="rgba(56,189,248,.18)" stroke="currentColor" stroke-width="2"/>')
    c.add(f'<rect x="{xc - 7}" y="124" width="14" height="36" fill="rgba(248,113,113,.25)" stroke="currentColor" stroke-width="2"/>')
    c.text(xc, 178, nm, anchor="middle", size=17)
c.line(61, 116, 75, 116, "currentColor", 1.6, obstacle=False)
c.line(61, 111, 61, 121, "currentColor", 1.6, obstacle=False)
c.line(75, 111, 75, 121, "currentColor", 1.6, obstacle=False)
c.text(80, 122, "s", size=18, italic=True)
c.text(16, 82, "tấm cản", size=17)
c.text(16, 100, "quang", size=17)
for gx, nm, lx in ((140, "cổng 1", 148), (300, "cổng 2", 308)):
    c.add(f'<rect x="{gx - 14}" y="60" width="28" height="18" rx="3" fill="rgba(248,113,113,.25)" stroke="currentColor" stroke-width="2"/>')
    c.line(gx, 78, gx, 190, RED, 2.4, "6 4", obstacle=False)
    c.text(lx, 104, nm, size=17)
c.add('<rect x="330" y="24" width="80" height="56" rx="6" fill="none" stroke="currentColor" stroke-width="2"/>')
c.text(370, 46, "đồng hồ", anchor="middle", size=17)
c.text(370, 64, "hiện số", anchor="middle", size=17)
c.add('<polyline points="140,60 140,40 330,40" fill="none" stroke="currentColor" stroke-width="1.8"/>')
c.segs += [(140, 60, 140, 40), (140, 40, 330, 40)]
c.add('<polyline points="314,69 330,69" fill="none" stroke="currentColor" stroke-width="1.8"/>')
c.segs += [(314, 69, 330, 69)]
c.arr("v1", "g", 40, 222, 104, 222, 3, 11)
c.text(112, 227, 'v<tspan font-size="13" dy="4">1</tspan>', size=18, italic=True)
c.text(186, 228, "xe 2 đứng yên", size=17)
c.text(404, 256, "băng đệm khí", size=17, anchor="end")
ok(c.arrows["v1"][2] > c.arrows["v1"][0], "f1: mũi tên v1 phải hướng sang phải (tới cổng 1)")
ok(68 < 140 < 218 - 28 + 28 and 218 < 300, "f1: xe 1 ở ngoài cổng 1, xe 2 giữa hai cổng")
fig1 = c.svg("Sơ đồ bố trí thí nghiệm va chạm mềm trên băng đệm khí: xe 1 ở bên trái cổng 1, xe 2 đứng yên giữa hai cổng, mỗi xe có một tấm cản quang rộng s dựng thẳng; cổng 1 và cổng 2 phát tia sáng nét đứt đỏ, nối dây tới đồng hồ hiện số; mũi tên v1 chỉ xe 1 chạy sang phải",
             "Hình 1. Bố trí thí nghiệm 1. Xe 1 chạy qua cổng 1 (đo $t_1$), va vào xe 2 đứng yên rồi hai xe dính nhau chạy qua cổng 2 (đo $t_1'$). $s$ là bề rộng tấm cản quang.".replace("$t_1$", "<em>t</em><sub>1</sub>").replace("$t_1'$", "<em>t</em><sub>1</sub>′"))
ERR += c.check()

# ================= Hình 2: tỉ số p'/p từng lần, kèm khoảng sai số ±ε
c = Canvas("f2", 420, 280)
OX, OY, K = 62, 240, 2600
Y = lambda v: OY - K * (v - 0.94)
c.arr("tx", "k", OX, OY, 408, OY, 1.8, 9)
c.arr("vy", "k", OX, OY, OX, 22, 1.8, 9)
c.text(70, 24, "p′/p", size=18, italic=True)
for tv in (0.96, 0.98, 1.00, 1.02):
    c.line(OX - 4, Y(tv), OX + 4, Y(tv), "currentColor", 1.5, obstacle=False)
    c.text(OX - 8, Y(tv) + 5, vn(tv, 2), size=17, anchor="end", weight="600")
c.line(OX, Y(1.0), 400, Y(1.0), GRN, 2.2, "7 5", obstacle=False)
c.text(300, Y(1.0) - 8, "p′ = p", GRN, 18, "start", italic=True)
XS = [120, 200, 280]
for i, (xr, r) in enumerate(zip(XS, A)):
    ratio, e = float(r["ratio"]), float(r["eps"])
    c.line(xr, Y(ratio - e), xr, Y(ratio + e), "currentColor", 2.2, obstacle=False)
    for yy in (Y(ratio - e), Y(ratio + e)):
        c.line(xr - 8, yy, xr + 8, yy, "currentColor", 2.2, obstacle=False)
    c.add(f'<circle cx="{xr}" cy="{Y(ratio):.1f}" r="6" fill="{ORG}" stroke="currentColor" stroke-width="1.4"/>')
    c.text(xr, 264, f"lần {i + 1}", size=17, anchor="middle", weight="600")
    ok(ratio < 1, "f2: p'/p phải < 1")
ok(float(A[0]["ratio"] + A[0]["eps"]) >= 1 and float(A[1]["ratio"] + A[1]["eps"]) >= 1 and float(A[2]["ratio"] + A[2]["eps"]) < 1,
   "f2: thanh sai số lần 1,2 chạm p'/p = 1; lần 3 không")
ok(Y(0.94) == OY and Y(1.02) > 22, "f2: trục")
fig2 = c.svg("Đồ thị tỉ số p phẩy trên p cho ba lần đo va chạm mềm: ba điểm cam đều nằm dưới đường nét đứt xanh p phẩy bằng p; thanh đứng là khoảng sai số cộng trừ epsilon, thanh lần 1 và lần 2 chạm đường nét đứt, thanh lần 3 nằm hẳn dưới",
             "Hình 2. Tỉ số <em>p</em>′/<em>p</em> của ba lần đo (số liệu minh hoạ); thanh đứng là khoảng sai số ±<em>ε</em>. Trục đứng bắt đầu từ 0,94, không phải từ 0.",
             exp="tn-l10-thuchanhdl-01")
ERR += c.check()

# ================= Hình 3: bố trí thí nghiệm 2 + chiều dương
c = Canvas("f3", 420, 262)
c.add('<rect x="16" y="190" width="388" height="14" fill="rgba(128,128,128,.25)" stroke="currentColor" stroke-width="2"/>')
for x0, nm in ((140, "xe 1"), (244, "xe 2")):
    c.add(f'<rect x="{x0}" y="160" width="56" height="26" rx="3" fill="rgba(56,189,248,.18)" stroke="currentColor" stroke-width="2"/>')
    c.add(f'<rect x="{x0 + 21}" y="124" width="14" height="36" fill="rgba(248,113,113,.25)" stroke="currentColor" stroke-width="2"/>')
    c.text(x0 + 28, 178, nm, anchor="middle", size=17)
c.add('<polyline points="196,173 202,165 214,181 226,165 238,181 244,173" fill="none" stroke="currentColor" stroke-width="2.2"/>')
c.text(220, 152, "lò xo", size=17, anchor="middle")
for gx, nm, lx, anc in ((70, "cổng 1", 78, "start"), (370, "cổng 2", 362, "end")):
    c.add(f'<rect x="{gx - 14}" y="60" width="28" height="18" rx="3" fill="rgba(248,113,113,.25)" stroke="currentColor" stroke-width="2"/>')
    c.line(gx, 78, gx, 190, RED, 2.4, "6 4", obstacle=False)
    c.text(lx, 104, nm, size=17, anchor=anc)
c.arr("pos", "k", 150, 40, 270, 40, 2.4, 10)
c.text(278, 45, "chiều dương", size=17)
c.arr("v1", "g", 150, 222, 90, 222, 3, 11)
c.arr("v2", "g", 290, 222, 350, 222, 3, 11)
c.text(48, 227, 'v<tspan font-size="13" dy="4">1</tspan><tspan font-size="17" dy="-4">′</tspan>', size=18, italic=True)
c.text(356, 227, 'v<tspan font-size="13" dy="4">2</tspan><tspan font-size="17" dy="-4">′</tspan>', size=18, italic=True)
c.text(160, 247, "băng đệm khí", size=17)
ok(c.arrows["pos"][2] > c.arrows["pos"][0], "f3: chiều dương sang phải")
ok(c.arrows["v1"][2] < c.arrows["v1"][0] and c.arrows["v2"][2] > c.arrows["v2"][0], "f3: v1' sang trái, v2' sang phải")
ok(c.arrows["v1"][2] > 70 and c.arrows["v2"][2] < 370, "f3: mũi tên chưa tới cổng")
fig3 = c.svg("Sơ đồ bố trí thí nghiệm hai xe đẩy nhau: hai xe đứng yên giữa cổng 1 và cổng 2 với lò xo nén ở giữa; mũi tên chiều dương hướng sang phải; sau khi cắt dây, xe 1 chạy sang trái với vận tốc v1 phẩy, xe 2 chạy sang phải với v2 phẩy",
             "Hình 3. Bố trí thí nghiệm 2, hai xe cùng khối lượng nên hai mũi tên dài bằng nhau. Chiều dương sang phải: <em>v</em><sub>1</sub>′ ngược chiều dương nên <em>p</em><sub>1</sub>′ &lt; 0, còn <em>p</em><sub>2</sub>′ &gt; 0.",
             exp="tn-l10-thuchanhdl-02")
ERR += c.check()

if ERR:
    print("\n".join("✗ " + str(e) for e in ERR)); sys.exit(1)


# ================= Bảng số liệu
def table(head, rows):
    return ('<div class="table-scroll">\n<table class="tl-table">\n<thead>\n<tr>' + "".join(f"<th>{h}</th>" for h in head)
            + "</tr>\n</thead>\n<tbody>\n" + "\n".join("<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in rows)
            + "\n</tbody>\n</table>\n</div>")


bang_a1 = table(["Lần", "$m_1$ ; $m_2$ (kg)", "$t_1$ ; $t_1'$ (s)"],
                [[i + 1, f"{fmt(r['m1'], 3)} ; {fmt(r['m2'], 3)}", f"{fmt(r['t1'], 3)} ; {fmt(r['tp'], 3)}"] for i, r in enumerate(A)])
bang_a2 = table(["Lần", "$p$ → $p'$ (kg·m/s)", "$\\delta$ ; $\\varepsilon$"],
                [[i + 1, f"{fmt(r['p'], 4)} → {fmt(r['pp'], 4)}", f"{fmt(r['delta'] * 100, 1)} % ; {fmt(r['eps'] * 100, 1)} %"] for i, r in enumerate(A)])
bang_b1 = table(["Lần", "$m_1$ ; $m_2$ (kg)", "$t_1'$ ; $t_2'$ (s)"],
                [[i + 1, f"{fmt(b['m1'], 3)} ; {fmt(b['m2'], 3)}", f"{fmt(b['t1'], 3)} ; {fmt(b['t2'], 3)}"] for i, b in enumerate(B)])
bang_b2 = table(["Lần", "$p_1'$ ; $p_2'$ (kg·m/s)", "$p'$ ; $\\Delta p'$"],
                [[i + 1, f"{sg(b['p1'])} ; {sg(b['p2'])}", f"{sg(b['P'])} ; {fmt(b['dP'], 4)}"] for i, b in enumerate(B)])
bang_ng = table(["$h$ (mm)", "$a$ (m/s²)", "$v$ thật so với số đọc"],
                [[h, vn(a, 3), f"+{vn(p, 1)} %"] for h, a, _, p in NG])

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, fg in enumerate((fig1, fig2, fig3), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
for k, v in (("__BANG_A1__", bang_a1), ("__BANG_A2__", bang_a2), ("__BANG_B1__", bang_b1), ("__BANG_B2__", bang_b2), ("__BANG_NGHIENG__", bang_ng)):
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
import math as _m
phut = int(_m.ceil(float(m.group(1).replace(",", ".")) - 1e-9))
h = h.replace("__PHUT__", str(phut))
(HERE / "theory.html").write_text(h, encoding="utf8")

# ================= File thí nghiệm
BASE = {"mon": "vat-ly", "lop": 10, "bai": "Bài 30. Thực hành: Xác định động lượng của vật trước và sau va chạm", "lesson_id": 75,
        "nguon_trong_bai": "content/lesson-samples/l10-thuc-hanh-dong-luong/theory.html"}
fl = float
tn = [
    {**BASE, "id": "tn-l10-thuchanhdl-01",
     "ten": "Va chạm mềm trên băng đệm khí: so động lượng trước và sau bằng cổng quang",
     "loai": "thi_nghiem", "muc_do": "trung_binh",
     "kien_thuc": ["thuchanhdl.v_bang_s_chia_t", "thuchanhdl.dong_luong_truoc_sau", "thuchanhdl.sai_so_so_sanh", "thuchanhdl.he_khong_kin_hoan_toan"],
     "muc_tieu": "Đo t1 và t1' bằng cổng quang, tính v = s/t, p = m1·v1 và p' = (m1+m2)·v'; so p' với p qua độ lệch δ và sai số ε; nhận ra p' < p cùng phía ở cả ba lần là sai số hệ thống.",
     "dung_cu": [{"ten": "Băng đệm khí + bơm nén khí", "so_luong": 1}, {"ten": "Hai xe trượt, gia trọng", "so_luong": 1},
                 {"ten": "Hai cổng quang + đồng hồ đo thời gian hiện số, độ chia 0,001 s", "so_luong": 1},
                 {"ten": "Tấm cản quang rộng s = 0,0500 m (đo bằng thước kẹp)", "so_luong": 1},
                 {"ten": "Cân điện tử, độ chia 0,001 kg", "so_luong": 1}, {"ten": "Chốt ghim + miếng sáp để hai xe dính nhau", "so_luong": 1}],
     "cac_buoc": {"lam": ["Chỉnh băng nằm ngang (xe đặt yên không trôi); tấm cản quang song song băng; bật bơm khí, chọn chế độ đo thời gian vật chắn cổng, reset 0,000; chọn thang cân, cân hai xe, ghi m1, m2.",
                          "Xe 2 đứng yên giữa hai cổng, xe 1 ngoài cổng 1; đẩy xe 1 va vào xe 2 cho dính nhau.",
                          "Đọc t1 (cổng 1) và t1' (cổng 2), lấy số đo lần đầu của đồng hồ; thêm gia trọng và làm 3 lần."],
                  "quan_sat": ["Bảng t1, t1' ba lần; t1' lớn hơn t1 nhiều (xe chậm đi sau va chạm)."],
                  "rut_ra": ["p = m1·s/t1; p' = (m1+m2)·s/t1'; δ = |p'−p|/p; ε = Δp/p + Δp'/p'.",
                             "Ba lần: δ = " + "; ".join(f"{fmt(r['delta'] * 100, 1)} %" for r in A) + " so với ε = " + "; ".join(f"{fmt(r['eps'] * 100, 1)} %" for r in A) +
                             "; lần 1, 2 có δ ≤ ε, lần 3 có δ > ε: chưa kết luận định luật sai mà kiểm lại băng nằm ngang, vị trí cổng quang rồi đo lại. Cả ba lần cùng p' < p nên nghi sai số hệ thống."]},
     "tham_so": [{"ky_hieu": "s", "ten": "Bề rộng tấm cản quang", "don_vi": "m", "kieu": "co_dinh", "gia_tri": 0.05},
                 {"ky_hieu": "m1", "ten": "Khối lượng xe 1 (kể gia trọng)", "don_vi": "kg", "kieu": "dieu_chinh", "min": 0.19, "max": 0.6, "mac_dinh": 0.205, "buoc": 0.05},
                 {"ky_hieu": "m2", "ten": "Khối lượng xe 2 (kể gia trọng)", "don_vi": "kg", "kieu": "dieu_chinh", "min": 0.19, "max": 0.6, "mac_dinh": 0.198, "buoc": 0.05},
                 {"ky_hieu": "v1", "ten": "Tốc độ xe 1 trước va chạm", "don_vi": "m/s", "kieu": "dieu_chinh", "min": 0.3, "max": 0.8, "mac_dinh": 0.505, "buoc": 0.05},
                 {"ky_hieu": "mat", "ten": "Tỉ lệ động lượng mất do ma sát, sức cản", "don_vi": "", "kieu": "dieu_chinh", "min": 0, "max": 0.05, "mac_dinh": 0.022, "buoc": 0.005},
                 {"ky_hieu": "dcnn_t", "ten": "Độ chia nhỏ nhất đồng hồ", "don_vi": "s", "kieu": "co_dinh", "gia_tri": 0.001},
                 {"ky_hieu": "dcnn_m", "ten": "Độ chia nhỏ nhất cân", "don_vi": "kg", "kieu": "co_dinh", "gia_tri": 0.001},
                 {"ky_hieu": "t1", "ten": "Thời gian xe 1 chắn cổng 1", "don_vi": "s", "kieu": "do_duoc", "sai_so_do": 0.001},
                 {"ky_hieu": "t1p", "ten": "Thời gian cặp xe chắn cổng 2", "don_vi": "s", "kieu": "do_duoc", "sai_so_do": 0.001},
                 {"ky_hieu": "delta", "ten": "Độ lệch tương đối giữa p' và p", "don_vi": "", "kieu": "tinh_ra"},
                 {"ky_hieu": "eps", "ten": "Sai số tương đối gộp", "don_vi": "", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["v1 = s/t1; p = m1·v1 (xe 2 đứng yên)", "v' = (m1·v1/(m1+m2))·(1 − mat)", "t1' = s/v'; p' = (m1+m2)·v'",
                                  "δ = |p'−p|/p", "ε = Δm/m1 + Δt/t1 + 2Δm/(m1+m2) + Δt/t1' (Δs triệt tiêu vì cùng tấm cản quang); ε là cận trên của sai số"],
                 "gia_thiet": ["va chạm mềm hoàn toàn, hai xe dính nhau", "mất động lượng do ma sát khí và sức cản quy về hệ số 'mat' ≈ 2 %", "v và p làm tròn half-up (v: 0,001; p: 0,0001)"]},
     "so_lieu_mau": {"cot": ["Lần", "m1 (kg)", "m2 (kg)", "t1 (s)", "t1' (s)", "v1 (m/s)", "p (kg·m/s)", "v' (m/s)", "p' (kg·m/s)", "δ (%)", "ε (%)"],
                     "hang": [[i + 1, fl(r["m1"]), fl(r["m2"]), fl(r["t1"]), fl(r["tp"]), fl(r["v1"]), fl(r["p"]), fl(r["vp"]), fl(r["pp"]),
                               fl(q(r["delta"] * 100, 1)), fl(q(r["eps"] * 100, 1))] for i, r in enumerate(A)],
                     "ghi_chu": "Số liệu minh hoạ tính từ mô hình, không phải đo thật. s = 0,0500 m, Δm = Δt = 0,001. Lần 1, 2: δ ≤ ε; lần 3: δ > ε; cả ba lần p' < p."},
     "ket_qua_ky_vong": "Hai trong ba lần δ ≤ ε, lần 3 vượt nhẹ; cả ba cùng p' < p (trung bình δ ≈ 2,1 %): bảo toàn gần đúng, còn sai số hệ thống do ngoại lực nhỏ.",
     "hien_tuong_hay_sai": ["Sau va chạm chỉ nhân v' với m1 mà quên m2.", "Đổi 5 cm sang mét sai (v lệch 100 lần).", "Coi δ ≠ 0 là thí nghiệm hỏng, không so với ε.", "Lấy trung bình ba lần rồi cho rằng sai số hệ thống đã mất."],
     "sai_so_thuong_gap": "Băng không ngang; cổng 1 đặt xa chỗ va chạm nên xe đã chậm bớt; ma sát khí; tấm cản quang không song song băng; xe 2 chưa thật đứng yên.",
     "an_toan": "Giữ xe không tuột khỏi đầu băng; không để tay vào lỗ khí khi bơm chạy.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu+do_thi",
                        "y_tuong": "Băng đệm khí, hai xe, hai cổng; nút đẩy; đồng hồ hiện t1, t1'; bảng tự tính p, p', δ, ε và đồ thị p'/p kèm thanh sai số.",
                        "diem_nhan": "Thanh trượt 'mat': kéo lên thì p'/p tụt dưới 1 ở mọi lần, thanh sai số không còn chạm 1."}},
    {**BASE, "id": "tn-l10-thuchanhdl-02",
     "ten": "Hai xe đẩy nhau bằng lò xo: kiểm tổng động lượng sau bằng 0",
     "loai": "thi_nghiem", "muc_do": "trung_binh",
     "kien_thuc": ["thuchanhdl.dau_cua_dong_luong", "thuchanhdl.hai_xe_day_nhau", "thuchanhdl.sai_so_so_sanh"],
     "muc_tieu": "Gán dấu cho p1', p2' theo chiều dương, cộng được p' ≈ 0 và so |p'| với Δp'; thấy t' tỉ lệ thuận với khối lượng xe.",
     "dung_cu": [{"ten": "Băng đệm khí + bơm", "so_luong": 1}, {"ten": "Hai xe có tấm cản quang s = 0,0500 m, gia trọng", "so_luong": 1},
                 {"ten": "Lò xo (hoặc thanh chữ U + dây cao su) gắn vào một xe", "so_luong": 1}, {"ten": "Hai cổng quang + đồng hồ hiện số 0,001 s", "so_luong": 1},
                 {"ten": "Cân điện tử 0,001 kg, sợi dây buộc hai xe", "so_luong": 1}],
     "cac_buoc": {"lam": ["Hai xe đứng yên giữa hai cổng, nén lò xo, buộc dây.", "Cắt dây; đọc t1' (cổng 1) và t2' (cổng 2); đổi gia trọng, làm 3 lần."],
                  "quan_sat": ["Xe 1 đi sang trái, xe 2 đi sang phải; t1' và t2' khác nhau khi hai xe nặng khác nhau."],
                  "rut_ra": ["Chiều dương sang phải: p1' = −m1·s/t1', p2' = +m2·s/t2', p' = p1' + p2'.",
                             "Ba lần p' = " + "; ".join(sg(b["P"]) for b in B) + " kg·m/s, đều trong Δp' (" + "; ".join(fmt(b["dP"], 4) for b in B) + ")."]},
     "tham_so": [{"ky_hieu": "s", "ten": "Bề rộng tấm cản quang", "don_vi": "m", "kieu": "co_dinh", "gia_tri": 0.05},
                 {"ky_hieu": "m1", "ten": "Khối lượng xe 1", "don_vi": "kg", "kieu": "dieu_chinh", "min": 0.19, "max": 0.6, "mac_dinh": 0.205, "buoc": 0.05},
                 {"ky_hieu": "m2", "ten": "Khối lượng xe 2", "don_vi": "kg", "kieu": "dieu_chinh", "min": 0.19, "max": 0.6, "mac_dinh": 0.198, "buoc": 0.05},
                 {"ky_hieu": "p0", "ten": "Độ lớn động lượng mỗi xe do lò xo truyền", "don_vi": "kg·m/s", "kieu": "dieu_chinh", "min": 0.02, "max": 0.1, "mac_dinh": 0.05, "buoc": 0.01},
                 {"ky_hieu": "dcnn_t", "ten": "Độ chia nhỏ nhất đồng hồ", "don_vi": "s", "kieu": "co_dinh", "gia_tri": 0.001},
                 {"ky_hieu": "t1p", "ten": "Thời gian xe 1 chắn cổng 1", "don_vi": "s", "kieu": "do_duoc", "sai_so_do": 0.001},
                 {"ky_hieu": "t2p", "ten": "Thời gian xe 2 chắn cổng 2", "don_vi": "s", "kieu": "do_duoc", "sai_so_do": 0.001},
                 {"ky_hieu": "P", "ten": "Tổng động lượng sau, có dấu", "don_vi": "kg·m/s", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["p1' = −m1·s/t1'; p2' = +m2·s/t2' (chiều dương sang phải)", "p' = p1' + p2'", "Δp' = |p1'|(Δm/m1 + Δt/t1') + |p2'|(Δm/m2 + Δt/t2')",
                                  "Lý tưởng: m1·s/t1' = m2·s/t2' nên t1'/t2' = m1/m2"],
                 "gia_thiet": ["đây là va chạm đàn hồi theo cách gọi trong đề: hai xe đẩy nhau bằng lò xo, không dính nhau", "ma sát khí và sức cản làm giảm cả hai độ lớn gần như như nhau nên gần như triệt tiêu trong p'", "thời gian t' đã làm tròn 0,001 s, v 0,001 m/s, p 0,0001 kg·m/s"]},
     "so_lieu_mau": {"cot": ["Lần", "m1 (kg)", "m2 (kg)", "t1' (s)", "t2' (s)", "p1' (kg·m/s)", "p2' (kg·m/s)", "p' (kg·m/s)", "Δp' (kg·m/s)"],
                     "hang": [[i + 1, fl(b["m1"]), fl(b["m2"]), fl(b["t1"]), fl(b["t2"]), fl(b["p1"]), fl(b["p2"]), fl(b["P"]), fl(q(b["dP"], 4))] for i, b in enumerate(B)],
                     "ghi_chu": "Số liệu minh hoạ tính từ mô hình, không phải đo thật. Dấu của p' lẫn lộn (+, −, −) và |p'| ≤ Δp' cả ba lần."},
     "ket_qua_ky_vong": "p' ≈ 0 trong sai số ở cả ba lần; t1'/t2' xấp xỉ m1/m2 (lần 2: 0,404/0,200 ≈ 2,0 so với m1/m2 ≈ 2,05).",
     "hien_tuong_hay_sai": ["Cộng độ lớn hai động lượng, quên dấu.", "Cho rằng lực lò xo bằng nhau thì hai xe chạy nhanh bằng nhau.", "Cố chia cho p = 0 để tính δ."],
     "sai_so_thuong_gap": "Cắt dây không đồng thời làm lò xo bung lệch; xe chưa thật đứng yên trước khi cắt; băng nghiêng làm hai xe lệch tốc độ.",
     "an_toan": "Cắt dây bằng kéo nhỏ, tay tránh xa lò xo đang nén.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu",
                        "y_tuong": "Hai xe giữa hai cổng; nút cắt dây; đồng hồ hiện t1', t2'; bảng tự tính p1', p2' có dấu, p' và Δp'.",
                        "diem_nhan": "Đổi chiều dương: dấu của p1', p2' đổi nhưng p' vẫn xấp xỉ 0."}},
    {**BASE, "id": "tn-l10-thuchanhdl-03",
     "ten": "Băng đệm khí nghiêng nhẹ làm lệch tốc độ đo được",
     "loai": "thi_nghiem", "muc_do": "nang_cao",
     "kien_thuc": ["thuchanhdl.he_khong_kin_hoan_toan", "thuchanhdl.chinh_bang_ngang"],
     "muc_tieu": "Thấy băng nghiêng vài milimét đã làm tốc độ thật tại chỗ va chạm lệch vài phần trăm so với số đọc ở cổng 1; biết cách kiểm băng nằm ngang.",
     "dung_cu": [{"ten": "Băng đệm khí dài 1,20 m + bơm", "so_luong": 1}, {"ten": "Tấm đệm mỏng để kê chân băng", "so_luong": 1},
                 {"ten": "Xe, cổng quang, đồng hồ hiện số", "so_luong": 1}, {"ten": "Thước", "so_luong": 1}],
     "cac_buoc": {"lam": ["Kê một đầu băng cao thêm h = 2; 4; 6 mm.", "Đẩy xe xuống dốc qua cổng 1 với v = 0,505 m/s rồi đo tốc độ tại chỗ cách cổng 1 một đoạn x = 0,300 m."],
                  "quan_sat": ["Tốc độ ở chỗ va chạm lớn hơn số đọc ở cổng 1, và lớn dần khi h tăng."],
                  "rut_ra": ["a = g·h/L; v_va_cham = sqrt(v² + 2ax).", "h = 6 mm đã lệch khoảng 5,6 %: phải chỉnh băng ngang trước khi đo."]},
     "tham_so": [{"ky_hieu": "h", "ten": "Độ kê cao một đầu băng", "don_vi": "mm", "kieu": "dieu_chinh", "min": 0, "max": 8, "mac_dinh": 4, "buoc": 1},
                 {"ky_hieu": "x", "ten": "Khoảng cách từ cổng 1 tới chỗ va chạm", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.1, "max": 0.6, "mac_dinh": X_BANG, "buoc": 0.1},
                 {"ky_hieu": "L", "ten": "Chiều dài băng", "don_vi": "m", "kieu": "co_dinh", "gia_tri": L_BANG},
                 {"ky_hieu": "v_cong", "ten": "Tốc độ đọc ở cổng 1", "don_vi": "m/s", "kieu": "co_dinh", "gia_tri": V_CONG},
                 {"ky_hieu": "lech", "ten": "Độ lệch tốc độ thật so với số đọc", "don_vi": "%", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["sin α ≈ h/L; a = g·h/L (g = 9,8 m/s²)", "v_thật = sqrt(v_cong² + 2·a·x) khi xe chạy xuống dốc", "lệch = (v_thật/v_cong − 1)·100 %"],
                 "gia_thiet": ["bỏ qua ma sát và sức cản", "góc nghiêng nhỏ nên sin α ≈ tan α ≈ h/L"]},
     "so_lieu_mau": {"cot": ["h (mm)", "a (m/s²)", "v_thật (m/s)", "lệch (%)"], "hang": [[h, round(a, 4), round(vc, 4), round(p, 2)] for h, a, vc, p in NG],
                     "ghi_chu": "Số liệu minh hoạ tính từ mô hình, không phải đo thật."},
     "ket_qua_ky_vong": "h = 2; 4; 6 mm cho lệch +1,9 %; +3,8 %; +5,6 %.",
     "hien_tuong_hay_sai": ["Cho rằng nghiêng vài milimét không đáng kể.", "Kiểm băng ngang chỉ bằng mắt thay vì thả xe đứng yên."],
     "sai_so_thuong_gap": "Chân vít chỉnh lệch; băng võng ở giữa; mặt bàn không phẳng.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu",
                        "y_tuong": "Thanh trượt độ kê cao h; xe trượt xuống, hai đồng hồ ở cổng 1 và cổng 2 hiện v.",
                        "diem_nhan": "Kéo h lên thì độ lệch tăng; đặt h = 0 thì hai số đọc trùng nhau."}},
]
for d in tn:
    (ROOT / "content/thi-nghiem" / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf8")
print(f"ok theory.html {len(h)} ký tự · 3 hình · {phut} phút · 3 file thí nghiệm")
