#!/usr/bin/env python3
"""Sinh 3 hình SVG + 2 bảng số liệu + số liệu trong lời văn cho 'Bài 6. Thực hành: Đo tốc độ của vật chuyển động'
(lesson 51, bản soạn lại 10/11/2026 theo bài thực hành SGK: viên bi, máng nghiêng, hai cổng quang, đồng hồ hiện số).
Thay mốc <!--FIGn-->, __BANG_TNn__, @@TOKEN@@, __PHUT__ trong theory.src.html -> theory.html và ghi
content/thi-nghiem/tn-l10-do-toc-do-0{1,2}.json từ cùng mô hình. Có lớp kiểm nhãn chồng/vượt viewBox.
Chạy: python3 build_figs.py   (sau đó: python3 build_bundle.py)"""
import json, math, pathlib, re, subprocess, sys
from decimal import Decimal, ROUND_HALF_UP
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))   # svg_lib của skill (có chevron đầu V)
from svg_lib import RED, BLUE, ORG, GRN, wrap, chevron
COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}


def fmt(x, nd=2):
    """Làm tròn nửa lên, trả chuỗi dấu phẩy thập phân kiểu Việt."""
    q = Decimal(1).scaleb(-nd)
    return str(Decimal(repr(round(x, 10))).quantize(q, rounding=ROUND_HALF_UP)).replace(".", ",")


def mth(s):
    return s.replace(",", "{,}")


class Canvas:
    def __init__(self, name, w, h):
        self.name, self.w, self.h = name, w, h
        self.body, self.labels, self.markers, self.arrows = "", [], set(), {}

    def add(self, s):
        self.body += s

    def line(self, x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.body += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

    def dot(self, x, y, r=4, c="currentColor"):
        self.body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'

    def arr(self, tag, c, x1, y1, x2, y2, w=3, head=11, dash=""):
        """Mũi tên có ĐỈNH đúng tại (x2,y2); đầu chữ V 30° (chevron), không dùng marker tam giác."""
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        ex, ey = x2 - ux * w * 0.6, y2 - uy * w * 0.6          # thân dừng sát đỉnh để đầu V nhọn
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.body += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{COL[c]}" stroke-width="{w}"{d}/>'
                      + chevron(x2, y2, ux, uy, COL[c], min(w, 2.8), L=max(head, 9)))
        self.arrows[tag] = (x1, y1, x2, y2)

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
            if a[5] < 14:
                errs.append(f"{self.name}: nhãn '{a[0]}' cỡ {a[5]} < 14")
            if a[1] < 2 or a[3] > self.w - 2 or a[2] < 0 or a[4] > self.h:
                errs.append(f"{self.name}: nhãn '{a[0]}' vượt viewBox {a[1:5]}")
            for b in self.labels[i + 1:]:
                if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    errs.append(f"{self.name}: nhãn '{a[0]}' chồng '{b[0]}'")
        return errs

    def svg(self, label, cap, exp=None):
        s = wrap(f"0 0 {self.w} {self.h}", label, self.defs() + self.body, cap)
        if exp:
            s = s.replace('<figure class="fig" data-tl="1">', f'<figure class="fig" data-tl="1" data-exp="{exp}">', 1)
        return s



ERR = []

# ================= Mô hình số liệu (dùng chung cho hình, bảng, lời văn và file thí nghiệm). Thời gian tính bằng mili-giây (số nguyên).
# Viên bi thép lăn nhanh dần đều trên máng nghiêng, a = 0,60 m/s² (minh hoạ). Nam châm điện N giữ bi ở đỉnh;
# cổng E cách N 0,100 m, cổng F cách E s = 0,500 m. Bi đường kính d = 20,0 mm.
A_, NE, S1, D_ = 0.60, 0.100, 0.500, 0.0200
VE_T, VF_T = math.sqrt(2 * A_ * NE), math.sqrt(2 * A_ * (NE + S1))       # tốc độ thật tại E, F
TEF_T = (VF_T - VE_T) / A_                                               # thời gian thật E -> F
DS_MM, DD_MM = 0.5, 0.05                                                 # nửa ĐCNN: thước mm, thước kẹp 0,1 mm


def r_half(x, nd=0):
    return float(Decimal(repr(round(x, 9))).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))


def bao_cao(L_m, dL_mm, t_ms):
    """Xử lý như báo cáo thực hành: t̄ làm tròn tới 1 ms, độ lệch tính từ t̄ đã làm tròn, Δt = lệch TB + 1 ms (đồng hồ hiện số)."""
    tb = int(r_half(sum(t_ms) / len(t_ms)))
    dev = [abs(t - tb) for t in t_ms]
    dtb = int(r_half(sum(dev) / len(dev)))
    dt = dtb + 1
    v = L_m / (tb / 1000)
    dll, dlt = dL_mm / 1000 / L_m * 100, dt / tb * 100
    return dict(tb=tb, dev=dev, dtb=dtb, dt=dt, v=v, dll=dll, dlt=dlt, dlv=dll + dlt, dv=v * (dll + dlt) / 100)


T1 = [835, 838, 837]                       # MODE A<->B, đoạn EF
T2 = [24, 23, 24]                          # MODE B, bi chắn cổng F
R1, R2 = bao_cao(S1, DS_MM, T1), bao_cao(D_, DD_MM, T2)
assert abs(TEF_T * 1000 - R1["tb"]) < 1, TEF_T                     # bảng khớp mô hình: 0,837 s
assert min(T2) <= D_ / VF_T * 1000 <= max(T2), D_ / VF_T           # 23,6 ms nằm giữa 23 và 24
TE_MS = int(r_half(D_ / VE_T * 1000)); assert TE_MS == 58
VE = D_ / (TE_MS / 1000)
RM, RN = bao_cao(0.600, DS_MM, [776, 780, 778]), bao_cao(0.500, DS_MM, [612, 615, 618])
assert (R1["tb"], R1["dtb"], R1["dt"]) == (837, 1, 2) and (R2["tb"], R2["dtb"], R2["dt"]) == (24, 0, 1)
assert (RM["tb"], RM["dtb"], RM["dt"]) == (778, 1, 2) and (RN["tb"], RN["dtb"], RN["dt"]) == (615, 2, 3)
assert RM["dev"] == [2, 2, 0] and RN["dev"] == [3, 0, 3]           # lời giải viết sẵn ba độ lệch
assert R2["v"] > R1["v"] and R2["dt"] < R1["dt"] and R2["dlt"] > 10 * R1["dlt"]     # bẫy 1 và bẫy 3
DAY = 2 * math.sqrt(10 ** 2 - 6 ** 2); LECH = (20 / DAY - 1) * 100
assert DAY == 16 and abs(LECH - 25) < 1e-9
VEd, VFd = float(fmt(VE, 3).replace(",", ".")), float(fmt(R2["v"], 2).replace(",", "."))
VTBC = r_half((VEd + VFd) / 2, 3)
VLECH = abs(float(fmt(R1["v"], 3).replace(",", ".")) - VTBC)
assert VLECH < r_half(R2["dv"], 2)
C2V, C2D, C2T = 0.0160 / 0.020, 0.05 / 16.0 * 100, 0.001 / 0.020 * 100
ms = lambda t: fmt(t / 1000, 3)
TOK = {
    "TB1": ms(R1["tb"]), "DTB1": ms(R1["dtb"]), "DT1": ms(R1["dt"]), "V1": fmt(R1["v"], 3), "DLT1": fmt(R1["dlt"], 2),
    "DLS1": fmt(R1["dll"], 2), "DLV1": fmt(R1["dlv"], 2), "DLV1F": fmt(R1["dlv"] / 100, 4), "DV1": fmt(R1["dv"], 3),
    "TB2": ms(R2["tb"]), "DTB2": ms(R2["dtb"]), "DT2": ms(R2["dt"]), "V2": fmt(R2["v"], 2), "DLT2": fmt(R2["dlt"], 2),
    "DLD2": fmt(R2["dll"], 2), "DLV2": fmt(R2["dlv"], 1), "DV2": fmt(R2["dv"], 2),
    "DAY": fmt(DAY, 0), "LECH": fmt(LECH, 0),
    "MT": ms(RM["tb"]), "MDTB": ms(RM["dtb"]), "MDT": ms(RM["dt"]), "MV": fmt(RM["v"], 3), "MDLS": fmt(RM["dll"], 2),
    "MDLT": fmt(RM["dlt"], 2), "MDLV": fmt(RM["dlv"], 2), "MDLVF": fmt(RM["dlv"] / 100, 4), "MDV": fmt(RM["dv"], 3),
    "MVLO": fmt(0.600 / 0.780, 3), "MVHI": fmt(0.600 / 0.776, 3),
    "NT": ms(RN["tb"]), "NDTB": ms(RN["dtb"]), "NDT": ms(RN["dt"]), "NV": fmt(RN["v"], 3), "NDLS": fmt(RN["dll"], 2),
    "NDLT": fmt(RN["dlt"], 2), "NDLV": fmt(RN["dlv"], 2), "NDV": fmt(RN["dv"], 3),
    "TE": ms(TE_MS), "VE": fmt(VE, 3), "DLTE": fmt(1 / TE_MS * 100, 1),
    "C1": fmt(0.400 / 0.500, 2), "C2V": fmt(C2V, 2), "C2D": fmt(C2D, 2), "C2T": fmt(C2T, 1), "C2S": fmt(C2D + C2T, 1),
    "VTBC": fmt(VTBC, 3), "VLECH": fmt(VLECH, 3),
}
f2 = lambda s: float(s.replace(",", "."))
# số hiển thị nhất quán: tổng hai số đã làm tròn = số làm tròn của tổng
for a, b, s in (("DLS1", "DLT1", "DLV1"), ("MDLS", "MDLT", "MDLV"), ("NDLS", "NDLT", "NDLV")):
    assert abs(f2(TOK[a]) + f2(TOK[b]) - f2(TOK[s])) < 1e-9, (a, b, s)
assert (TOK["V1"], TOK["DV1"], TOK["V2"], TOK["DV2"]) == ("0,597", "0,002", "0,83", "0,04"), TOK
assert (TOK["MV"], TOK["MDV"], TOK["NV"], TOK["NDV"]) == ("0,771", "0,003", "0,813", "0,005"), TOK
assert f2(TOK["MVLO"]) >= f2(TOK["MV"]) - f2(TOK["MDV"]) and f2(TOK["MVHI"]) <= f2(TOK["MV"]) + f2(TOK["MDV"])
assert abs(f2(TOK["V2"]) - VF_T) < f2(TOK["DV2"]) and abs(f2(TOK["V1"]) - S1 / TEF_T) < f2(TOK["DV1"])    # giá trị thật nằm trong khoảng sai số

# ================= Hình 1: cổng quang điện + đồng hồ đo thời gian hiện số
c = Canvas("f1", 420, 222)
c.text(90, 30, "Cổng quang điện", anchor="middle")
c.add('<path d="M50,150 L50,56 L130,56 L130,150" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/>')
c.line(56, 112, 124, 112, RED, 2.5, dash="6 5")
c.dot(56, 112, 4, RED); c.dot(124, 112, 4, RED)
c.text(90, 136, "tia sáng", RED, anchor="middle")
c.line(30, 152, 150, 152, w=2)
c.text(305, 30, "Đồng hồ hiện số", anchor="middle")
c.add('<rect x="212" y="50" width="190" height="126" rx="8" fill="none" stroke="currentColor" stroke-width="2.5"/>')
c.add('<rect x="226" y="62" width="100" height="38" rx="4" fill="none" stroke="currentColor" stroke-width="2"/>')
c.text(276, 89, "0,000", GRN, size=22, anchor="middle")
c.add('<circle cx="366" cy="78" r="11" fill="none" stroke="currentColor" stroke-width="2"/>')
c.text(366, 110, "RESET", size=14, anchor="middle")
c.add('<circle cx="250" cy="130" r="15" fill="none" stroke="currentColor" stroke-width="2"/>')
c.line(250, 130, 259, 120, ORG, 3)
c.text(250, 164, "MODE", ORG, size=14, anchor="middle")
for x, n in ((330, "A"), (372, "B")):
    c.add(f'<circle cx="{x}" cy="150" r="7" fill="none" stroke="currentColor" stroke-width="2"/>')
    c.text(x, 136, n, BLUE, anchor="middle")
c.add('<path d="M130,70 C175,70 170,205 250,200 C310,196 330,190 330,157" fill="none" stroke="' + BLUE + '" stroke-width="2" stroke-dasharray="5 4"/>')
c.text(170, 214, "dây nối vào ổ A", BLUE, anchor="middle")
fig1 = c.svg("Bên trái là cổng quang điện hình chữ U úp, giữa hai trụ có tia hồng ngoại nét đứt màu đỏ; bên phải là đồng hồ đo thời gian hiện số có màn hình 0,000, nút RESET, núm MODE và hai ổ cắm A, B; dây nối cổng quang vào ổ A",
              "Hình 1. Cổng quang điện và đồng hồ đo thời gian hiện số.<br>Vật chắn tia hồng ngoại thì cổng báo cho đồng hồ.<br>Núm MODE có năm vị trí: A, B, A + B, A ↔ B, T.")
ERR += c.check()

# ================= Hình 2: bố trí máng nghiêng, nam châm điện, hai cổng E, F
c = Canvas("f2", 420, 214)
X0, Y0, X1, Y1 = 40, 70, 390, 180
LR = math.hypot(X1 - X0, Y1 - Y0); ux, uy = (X1 - X0) / LR, (Y1 - Y0) / LR; nx, ny = uy, -ux      # n: vuông góc máng, hướng lên
P = lambda q, h=0: (X0 + ux * q + nx * h, Y0 + uy * q + ny * h)
SC = 300                                           # px cho mỗi mét dọc máng
qN, qE = 22, 22 + NE * SC; qF = qE + S1 * SC
assert abs((qF - qE) / (qE - qN) - S1 / NE) < 1e-9 and qF < LR - 10       # tỉ lệ NE : EF đúng 1 : 5
c.line(X0, Y0, X1, Y1, w=4)
c.line(X0, Y0, X0, 190, w=2); c.line(X0 - 10, 190, 400, 190, w=2)
bx, by = P(qN, 10)
c.add(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="9" fill="{ORG}"/>')
mx, my = P(qN - 17, 10)
c.add(f'<rect x="{mx - 7:.1f}" y="{my - 10:.1f}" width="14" height="20" fill="none" stroke="currentColor" stroke-width="2" transform="rotate({math.degrees(math.atan2(uy, ux)):.1f} {mx:.1f} {my:.1f})"/>')
c.text(16, 34, "Nam châm điện")
for q, n in ((qE, "E"), (qF, "F")):
    (ax, ay), (tx, ty) = P(q, 0), P(q, 40)
    c.line(ax, ay, tx, ty, BLUE, 4)
    hx, hy = P(q, 10); c.dot(hx, hy, 3.5, RED)                 # tia sáng ngang tâm bi (bán kính 9-10 px)
    lx, ly = P(q + 10, 26)
    c.text(lx, ly + 5, n, BLUE, size=16)
(e1x, e1y), (f1x, f1y) = P(qE, -16), P(qF, -16)
mxs, mys = (e1x + f1x) / 2, (e1y + f1y) / 2
c.arr("s1", "g", mxs, mys, e1x, e1y, w=2.5); c.arr("s2", "g", mxs, mys, f1x, f1y, w=2.5)
c.text(mxs - 18, mys + 30, "s = EF", GRN, anchor="middle")
(a1x, a1y), (a2x, a2y) = P(qE + 55, 24), P(qE + 110, 24)
c.arr("v", "o", a1x, a1y, a2x, a2y, w=2.5)
fig2 = c.svg("Máng nghiêng dốc từ trái xuống phải; ở đỉnh máng có nam châm điện giữ viên bi thép; dọc máng có hai cổng quang E ở trên và F ở dưới, chấm đỏ ở mỗi cổng là tia sáng; mũi tên hai đầu màu xanh lá dọc máng chỉ quãng đường s bằng EF; mũi tên cam chỉ chiều bi lăn",
              "Hình 2. Bố trí thí nghiệm đo tốc độ trung bình.<br>Cổng E nối ổ A, cổng F nối ổ B của đồng hồ.<br>Chấm đỏ: tia sáng của cổng, đi ngang tâm viên bi.",
              exp="tn-l10-do-toc-do-01")
ERR += c.check()

# ================= Hình 3: viên bi chắn tia — qua tâm và lệch tâm (3 px = 1 mm, r = 10 mm)
c = Canvas("f3", 420, 256)
K, RB = 3, 30
def hang(yc, lech_mm, nhan, dong1, dong2):
    half = math.sqrt(10 ** 2 - lech_mm ** 2) * K          # nửa dây cung (px)
    xb, yb = 200, yc - lech_mm * K                        # vị trí tia sáng
    c1, c2 = xb - half, xb + half                         # tâm bi lúc bắt đầu chắn / lúc hết chắn
    assert abs(math.hypot(xb - c1, yb - yc) - RB) < 1e-6 and abs(math.hypot(xb - c2, yb - yc) - RB) < 1e-6    # tia nằm đúng trên mép bi
    c.add(f'<circle cx="{c1:.1f}" cy="{yc}" r="{RB}" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="6 5"/>')
    c.add(f'<circle cx="{c2:.1f}" cy="{yc}" r="{RB}" fill="none" stroke="currentColor" stroke-width="2.5"/>')
    c.dot(c1, yc, 2.5); c.dot(c2, yc, 2.5)
    c.dot(xb, yb, 5, RED)
    ya = yc + RB + 12
    xm = (c1 + c2) / 2
    c.arr(nhan + "a", "g", xm, ya, c1, ya, w=2.5, head=9); c.arr(nhan + "b", "g", xm, ya, c2, ya, w=2.5, head=9)
    c.text(xm, ya + 19, nhan, GRN, anchor="middle")
    c.text(286, yc - 4, dong1); c.text(286, yc + 16, dong2)
    return c2 - c1
w1 = hang(72, 0, "d = 20 mm", "Tia qua tâm:", "bi đi được d")
w2 = hang(190, 6, "16 mm", "Tia lệch tâm:", "bi chỉ đi 16 mm")
assert abs(w1 - 20 * K) < 1e-6 and abs(w2 - DAY * K) < 1e-6
c.text(200, 24, "tia sáng", RED, anchor="middle")
fig3 = c.svg("Hai hàng hình. Hàng trên: tia sáng là chấm đỏ nằm ngang tâm viên bi; vòng tròn nét đứt là viên bi lúc bắt đầu chắn tia, vòng tròn nét liền là lúc hết chắn; hai tâm cách nhau đúng một đường kính d bằng 20 mm. Hàng dưới: tia sáng lệch lên trên tâm 6 mm; hai vị trí của bi chỉ cách nhau 16 mm",
              "Hình 3. Viên bi chắn tia sáng (tia vuông góc với trang giấy).<br>Nét đứt: lúc bắt đầu chắn. Nét liền: lúc hết chắn.<br>Tia lệch tâm thì quãng đường chắn tia ngắn hơn $d$.",
              exp="tn-l10-do-toc-do-02")
ERR += c.check()

if ERR:
    print("\n".join("✗ " + e for e in ERR)); sys.exit(1)

# ================= Bảng số liệu
def table(head, rows, last=None):
    out = '<div class="table-scroll">\n<table class="tl-table">\n<thead>\n<tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr>\n</thead>\n<tbody>\n"
    for r in rows:
        out += "<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>\n"
    if last:
        out += "<tr>" + "".join(f"<td><strong>{x}</strong></td>" for x in last) + "</tr>\n"
    return out + "</tbody>\n</table>\n</div>"

HEAD = ["Lần", "$t$ (s)", "$|t - \\bar t|$ (s)"]
b1 = table(HEAD, [[i + 1, ms(t), ms(d)] for i, (t, d) in enumerate(zip(T1, R1["dev"]))], ["Trung bình", ms(R1["tb"]), ms(R1["dtb"])])
b2 = table(HEAD, [[i + 1, ms(t), ms(d)] for i, (t, d) in enumerate(zip(T2, R2["dev"]))], ["Trung bình", ms(R2["tb"]), ms(R2["dtb"])])

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, fg in enumerate((fig1, fig2, fig3), 1):
    assert h.count(f"<!--FIG{n}-->") == 1, n
    h = h.replace(f"<!--FIG{n}-->", fg)
for k, b in (("__BANG_TN1__", b1), ("__BANG_TN2__", b2)):
    assert k in h, k
    h = h.replace(k, b)
used = set()
def rep(m):
    name, mode = m.group(1), m.group(2)
    assert name in TOK, name
    used.add(name)
    return mth(TOK[name]) if mode else TOK[name]
h = re.sub(r"@@([A-Za-z0-9]+)(:m)?@@", rep, h)
assert "@@" not in h and "__" not in h.replace("__PHUT__", "")
assert used == set(TOK), set(TOK) - used
tmp = HERE / ".theory.tmp.html"
tmp.write_text(h.replace("__PHUT__", "15"), encoding="utf8")
lint = ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = subprocess.run([sys.executable, str(lint), str(tmp)], capture_output=True, text=True).stdout
tmp.unlink()
m = re.search(r"~?(\d+(?:[.,]\d+)?)\s*phút", out)
if not m:
    print("! không đọc được số phút từ lint_do_dai:\n" + out[:600]); sys.exit(1)
h = h.replace("__PHUT__", str(round(float(m.group(1).replace(",", ".")))))
(HERE / "theory.html").write_text(h, encoding="utf8")

# ================= File thí nghiệm (số liệu từ cùng mô hình). tn-l10-do-toc-do-03 (tấm chắn rộng/hẹp, có clip) giữ nguyên trong kho, bài không còn dùng.
BASE = {"mon": "vat-ly", "lop": 10, "bai": "Bài 6. Thực hành: Đo tốc độ của vật chuyển động", "lesson_id": 51,
        "nguon_trong_bai": "content/lesson-samples/l10-thuc-hanh-do-toc-do/theory.html"}
GT = ["bi lăn nhanh dần đều trên máng, a = 0,60 m/s² (giả định)", "nam châm điện thả bi không tốc độ đầu, cách cổng E 0,100 m",
      "ba số đo là dãy giả định quanh giá trị tính từ mô hình, không phải đo thật", "đồng hồ hiện số chia 0,001 s"]
tn = [
    {**BASE, "id": "tn-l10-do-toc-do-01",
     "ten": "Đo tốc độ trung bình của viên bi trên máng nghiêng bằng hai cổng quang (MODE A↔B)",
     "loai": "thi_nghiem", "muc_do": "co_ban",
     "kien_thuc": ["dotocdo.cong_quang", "dotocdo.mode_a_b", "dotocdo.v_bang_s_chia_t", "dotocdo.sai_so_tuyet_doi", "dotocdo.sai_so_tuong_doi"],
     "muc_tieu": "Đo thời gian viên bi đi giữa hai cổng quang E, F cách nhau 0,500 m, tính tốc độ trung bình và viết kết quả kèm sai số.",
     "dung_cu": [{"ten": "Máng nghiêng có thước chia mm", "so_luong": 1}, {"ten": "Nam châm điện và công tắc", "so_luong": 1},
                 {"ten": "Viên bi thép đường kính 20,0 mm", "so_luong": 1}, {"ten": "Cổng quang điện", "so_luong": 2},
                 {"ten": "Đồng hồ đo thời gian hiện số (chia 0,001 s)", "so_luong": 1}],
     "cac_buoc": {"lam": ["Đặt hai cổng quang E, F cách nhau s = 0,500 m; nối E vào ổ A, F vào ổ B; chọn MODE A↔B.",
                          "Cho nam châm điện giữ bi ở đỉnh máng, bấm RESET, ngắt công tắc cho bi lăn. Lặp 3 lần."],
                  "quan_sat": ["Ba số chỉ: " + "; ".join(ms(t) for t in T1) + " s, lệch nhau vài phần nghìn giây."],
                  "rut_ra": [f"t̄ = {TOK['TB1']} s; Δt = {TOK['DTB1']} + 0,001 = {TOK['DT1']} s; δt ≈ {TOK['DLT1']} %; δs = {TOK['DLS1']} %.",
                             f"v_tb = s/t̄ = {TOK['V1']} ± {TOK['DV1']} m/s (δv = {TOK['DLV1']} %). Đây là tốc độ trung bình trên EF, không phải tốc độ tại F."]},
     "tham_so": [{"ky_hieu": "s", "ten": "Khoảng cách hai cổng quang", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.2, "max": 0.7, "mac_dinh": S1, "buoc": 0.05},
                 {"ky_hieu": "a", "ten": "Mức tăng tốc độ mỗi giây của bi", "don_vi": "m/s²", "kieu": "dieu_chinh", "min": 0.2, "max": 1.5, "mac_dinh": A_, "buoc": 0.05},
                 {"ky_hieu": "x_E", "ten": "Khoảng cách từ nam châm tới cổng E", "don_vi": "m", "kieu": "co_dinh", "gia_tri": NE},
                 {"ky_hieu": "t", "ten": "Thời gian đi từ E tới F", "don_vi": "s", "kieu": "do_duoc", "sai_so_do": R1["dt"] / 1000},
                 {"ky_hieu": "v_tb", "ten": "Tốc độ trung bình trên EF", "don_vi": "m/s", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["v_E = √(2·a·x_E)", "v_F = √(2·a·(x_E + s))", "t = (v_F − v_E)/a", "v_tb = s/t",
                                  "Δt = trung bình |t_i − t̄| + 0,001 s", "δv = Δs/s + Δt/t̄"],
                 "gia_thiet": GT + ["thước mm: Δs = 0,0005 m"]},
     "so_lieu_mau": {"cot": ["Lần", "t (s)", "|t − t̄| (s)"],
                     "hang": [[i + 1, t / 1000, d / 1000] for i, (t, d) in enumerate(zip(T1, R1["dev"]))],
                     "ghi_chu": f"Số liệu minh hoạ; mô hình cho t = {fmt(TEF_T, 4)} s. t̄ = {TOK['TB1']} s (làm tròn tới 0,001 s), độ lệch tính từ t̄ đã làm tròn."},
     "ket_qua_ky_vong": f"v_tb = {TOK['V1']} ± {TOK['DV1']} m/s.",
     "hien_tuong_hay_sai": ["Thả bi bằng tay nên mỗi lần bi tới E với một tốc độ khác.", "Chọn nhầm MODE A hoặc A+B.", "Coi s/t là tốc độ của bi tại F."],
     "sai_so_thuong_gap": "Đọc vị trí cổng quang trên thước; bi rời nam châm không cùng vị trí; máng bị rung.",
     "an_toan": "Đặt hộp hứng bi ở chân máng; không để bi thép rơi xuống sàn.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu",
                        "y_tuong": "Bi lăn trên máng qua hai cổng quang kéo được; đồng hồ hiện số có núm MODE, bảng điền dần sau mỗi lần thả.",
                        "diem_nhan": "Chọn sai MODE thì số chỉ không dùng được cho s/t; kéo cổng F để thấy t đổi theo s."}},
    {**BASE, "id": "tn-l10-do-toc-do-02",
     "ten": "Đo tốc độ tức thời của viên bi tại cổng quang F (MODE B, v = d/t)",
     "loai": "thi_nghiem", "muc_do": "trung_binh",
     "kien_thuc": ["dotocdo.cong_quang", "dotocdo.mode_b", "dotocdo.v_bang_d_chia_t", "dotocdo.toc_do_tuc_thoi", "dotocdo.tia_qua_tam", "dotocdo.sai_so_tuong_doi"],
     "muc_tieu": "Đo thời gian viên bi đường kính 20,0 mm chắn tia sáng của cổng F, tính tốc độ tức thời v = d/t và nhận ra vì sao sai số tỉ đối lớn hơn phép đo tốc độ trung bình.",
     "dung_cu": [{"ten": "Máng nghiêng, nam châm điện và công tắc", "so_luong": 1}, {"ten": "Viên bi thép", "so_luong": 1},
                 {"ten": "Thước kẹp (chia 0,1 mm)", "so_luong": 1}, {"ten": "Cổng quang điện", "so_luong": 1},
                 {"ten": "Đồng hồ đo thời gian hiện số (chia 0,001 s)", "so_luong": 1}],
     "cac_buoc": {"lam": ["Đo đường kính bi bằng thước kẹp: d = 20,0 mm.",
                          "Giữ cổng F nối ổ B, chọn MODE B; chỉnh cổng cho tia sáng đi ngang tâm bi.",
                          "Thả bi bằng công tắc nam châm điện. Lặp 3 lần."],
                  "quan_sat": ["Ba số chỉ: " + "; ".join(ms(t) for t in T2) + " s."],
                  "rut_ra": [f"t̄ = {TOK['TB2']} s; Δt = {TOK['DT2']} s; δt ≈ {TOK['DLT2']} %; δd = {TOK['DLD2']} %.",
                             f"v_F = d/t̄ = {TOK['V2']} ± {TOK['DV2']} m/s (δv ≈ {TOK['DLV2']} %), lớn hơn tốc độ trung bình {TOK['V1']} m/s trên EF vì bi lăn nhanh dần.",
                             "Thời gian chắn tia chỉ khoảng 24 độ chia của đồng hồ nên sai số tỉ đối lớn."]},
     "tham_so": [{"ky_hieu": "d", "ten": "Đường kính viên bi", "don_vi": "mm", "kieu": "dieu_chinh", "min": 10.0, "max": 30.0, "mac_dinh": 20.0, "buoc": 1.0},
                 {"ky_hieu": "lech", "ten": "Độ lệch của tia sáng so với tâm bi", "don_vi": "mm", "kieu": "dieu_chinh", "min": 0.0, "max": 8.0, "mac_dinh": 0.0, "buoc": 1.0},
                 {"ky_hieu": "v_F", "ten": "Tốc độ thật của bi tại F", "don_vi": "m/s", "kieu": "co_dinh", "gia_tri": round(VF_T, 3)},
                 {"ky_hieu": "t", "ten": "Thời gian chắn tia", "don_vi": "s", "kieu": "do_duoc", "sai_so_do": R2["dt"] / 1000},
                 {"ky_hieu": "v", "ten": "d/t", "don_vi": "m/s", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["dây cung = 2·√((d/2)² − lech²)", "t = dây cung / v_F", "t hiện = t làm tròn tới 0,001 s", "v = d/t hiện",
                                  "Δt = trung bình |t_i − t̄| + 0,001 s", "δv = Δd/d + Δt/t̄"],
                 "gia_thiet": GT + ["tốc độ coi như không đổi trong lúc bi chắn tia", "thước kẹp: Δd = 0,05 mm"]},
     "so_lieu_mau": {"cot": ["Lần", "t (s)", "|t − t̄| (s)"],
                     "hang": [[i + 1, t / 1000, d / 1000] for i, (t, d) in enumerate(zip(T2, R2["dev"]))],
                     "ghi_chu": f"Số liệu minh hoạ; mô hình cho v_F = {fmt(VF_T, 3)} m/s, t = {fmt(D_ / VF_T, 4)} s nên đồng hồ hiện 0,023 hoặc 0,024 s. Tia lệch tâm 6 mm: dây cung 16 mm, d/t lớn hơn thật 25 %."},
     "ket_qua_ky_vong": f"v_F = {TOK['V2']} ± {TOK['DV2']} m/s.",
     "hien_tuong_hay_sai": ["Tia sáng không qua tâm bi nên thời gian chắn ngắn, tốc độ tính ra lớn hơn thật.", "Lấy bán kính thay cho đường kính.", "Quên đổi mm ra m."],
     "sai_so_thuong_gap": "Tia sáng lệch tâm bi (lệch một phía, làm d/t lớn hơn thật); thời gian chắn quá ngắn so với độ chia của đồng hồ.",
     "an_toan": "Đặt hộp hứng bi ở chân máng; không để bi thép rơi xuống sàn.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu",
                        "y_tuong": "Phóng to cảnh bi đi qua tia sáng; thanh trượt nâng hạ cổng quang để tia lệch tâm; đồng hồ hiện thời gian chắn.",
                        "diem_nhan": "Nâng cổng lên thì thời gian chắn giảm, d/t tăng dù bi vẫn lăn như cũ."}},
]
KHO = ROOT / "content/thi-nghiem"
for t in tn:
    (KHO / f"{t['id']}.json").write_text(json.dumps(t, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
print(f"theory.html: {len(h)/1024:.1f} KB · {len(TOK)} số liệu · 3 hình · 2 bảng · 2 file thí nghiệm")
