#!/usr/bin/env python3
"""Sinh 3 hình SVG + 3 bảng số liệu + số liệu trong lời văn cho bài 'Bài 6. Thực hành: Đo tốc độ của vật chuyển động'
(lesson 51), thay mốc <!--FIGn-->, __BANG_TNn__, @@TOKEN@@ và __PHUT__ trong theory.src.html -> theory.html,
và ghi 3 file thí nghiệm content/thi-nghiem/tn-l10-do-toc-do-0{1,2,3}.json (số liệu tính từ cùng mô hình).
Có lớp kiểm hình học: hộp nhãn không chồng nhau, không vượt viewBox; toạ độ điểm khớp phép ánh xạ.
Chạy: python3 build_figs.py   (sau đó: python3 build_bundle.py)"""
import json, math, pathlib, re, subprocess, sys
from decimal import Decimal, ROUND_HALF_UP
from svg_lib import RED, BLUE, ORG, GRN, wrap

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
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
        """Mũi tên có ĐỈNH đúng tại (x2,y2); marker cỡ cố định (userSpaceOnUse)."""
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        ex, ey = x2 - ux * head, y2 - uy * head
        self.markers.add((c, head))
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.body += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{COL[c]}" stroke-width="{w}"{d} '
                      f'marker-end="url(#{self.name}-{c}{head})"/>')
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
            if a[5] < 13:
                errs.append(f"{self.name}: nhãn '{a[0]}' cỡ {a[5]} < 13")
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

# ================= Mô hình số liệu (dùng chung cho hình, bảng, lời văn và file thí nghiệm). Số nguyên để khỏi sai số float.
# TN1 (bấm tay): s = 1,20 m, xe đều 0,40 m/s -> t thật 3,00 s; độ trễ phản xạ mỗi lần (cs) là mô hình giả định.
S1, DS1 = 1.20, 0.002
T1_TRUE_CS = 300
E1 = [12, -14, 4, 21, -8]                       # centi-giây
T1CS = [T1_TRUE_CS + e for e in E1]             # 312, 286, 304, 321, 292
TBAR1CS = Decimal(sum(T1CS)) / 5
assert TBAR1CS == Decimal("303")
DEV1CS = [abs(Decimal(t) - TBAR1CS) for t in T1CS]
DT1CS = sum(DEV1CS) / 5                         # 11,2 cs
TBAR1, DT1 = float(TBAR1CS) / 100, float(DT1CS) / 100
DLT1, DLS1 = DT1 / TBAR1 * 100, DS1 / S1 * 100
DLV1 = DLT1 + DLS1
VB1 = S1 / TBAR1

# TN2 (cổng quang): d = 5,0 cm (±0,1), xe đều 0,50 m/s -> t = 0,100 s; đồng hồ chia 0,001 s (ms).
D2, DD2 = 0.050, 0.001
T2MS = [98, 101, 100, 102, 99]
TBAR2MS = Decimal(sum(T2MS)) / 5
assert TBAR2MS == Decimal("100")
DEV2MS = [abs(Decimal(t) - TBAR2MS) for t in T2MS]
DT2MS = sum(DEV2MS) / 5                         # 1,2 ms
TBAR2, DT2 = float(TBAR2MS) / 1000, float(DT2MS) / 1000
DLT2, DLD2 = DT2 / TBAR2 * 100, DD2 / D2 * 100
DLV2 = DLT2 + DLD2
V2 = [round(D2 / (t / 1000), 3) for t in T2MS]
VB2 = D2 / TBAR2

# TN3 (tấm chắn rộng/hẹp, xe nhanh dần): v1 = 0,600 m/s tại mép trước, mỗi giây tăng 0,50 m/s.
V1, A3 = 0.600, 0.50
D3CM = [10.0, 5.0, 2.0, 1.0]
ROW3 = []
for dcm in D3CM:
    d = dcm / 100
    t = (-V1 + math.sqrt(V1 * V1 + 2 * A3 * d)) / A3       # d = v1 t + a t²/2
    tms = int(Decimal(repr(t * 1000)).quantize(Decimal(1), rounding=ROUND_HALF_UP))   # đồng hồ chia 1 ms
    v = d / (tms / 1000)
    ROW3.append((dcm, t, tms, v))
V3MM = [int(Decimal(repr(r[3] * 1000)).quantize(Decimal(1), rounding=ROUND_HALF_UP)) for r in ROW3]   # mm/s
assert [r[2] for r in ROW3] == [156, 81, 33, 17], ROW3
assert V3MM == [641, 617, 606, 588], V3MM
assert abs(ROW3[3][1] - 0.0166) < 5e-5                       # lời văn: "khoảng 0,0166 s"
assert abs(0.0005 / ROW3[3][1] * 100 - 3) < 0.1              # lời văn: "khoảng 3 %"
dev3 = [abs(m - 600) for m in V3MM]
assert dev3 == [41, 17, 6, 12] and dev3[2] == min(dev3)      # d = 2,0 cm lệch ít nhất; hàng cuối lệch xa hơn hàng ba

# Bài toán mẫu: d = 2,0 cm (±0,1), t = 0,050 s (±0,001)
def bt(dcm, ddcm, t, dt):
    v = dcm / 100 / t
    dld, dlt = ddcm / dcm * 100, dt / t * 100
    dlv = dld + dlt
    return v, dld, dlt, dlv, v * dlv / 100

VB3, DLD3, DLT3, DLV3, DV3 = bt(2.0, 0.1, 0.050, 0.001)
VB4, DLD4, DLT4, DLV4, DV4 = bt(4.0, 0.1, 0.100, 0.001)
VB5, _, DLT5, DLV5, _ = bt(2.0, 0.1, 0.100, 0.001)
assert (fmt(VB3), fmt(DLD3, 1), fmt(DLT3, 1), fmt(DLV3, 1), fmt(DV3, 2)) == ("0,40", "5,0", "2,0", "7,0", "0,03"), (VB3, DLD3, DLT3, DLV3, DV3)
assert (fmt(VB4), fmt(DLD4, 1), fmt(DLT4, 1), fmt(DLV4, 1), fmt(DV4, 2)) == ("0,40", "2,5", "1,0", "3,5", "0,01")
assert DLV4 < DLV3
assert (fmt(VB5), fmt(DLT5, 1), fmt(DLV5, 1)) == ("0,20", "1,0", "6,0")
assert DLD3 > DLT3 and DLD4 > DLT4
# Thử thách
C1 = 1.50 / 3.00
C2A, C2B = 0.15 / 6.00 * 100, 0.15 / 3.00 * 100
C3A, C3At = 0.1 / 1.0 * 100, 0.001 / 0.025 * 100
C3B, C3Bt = 0.1 / 2.0 * 100, 0.001 / 0.050 * 100
assert C2A < C2B and C3A + C3At > C3B + C3Bt
assert abs(0.010 / 0.40 - 0.025) < 1e-12 and abs(0.020 / 0.40 - 0.050) < 1e-12   # t ≈ 0,025 s và 0,050 s
# nhất quán số hiển thị (tổng các số đã làm tròn bằng số làm tròn của tổng)
for a, b, s in ((DLT1, DLS1, DLV1), (DLT2, DLD2, DLV2), (DLD3, DLT3, DLV3), (DLD4, DLT4, DLV4), (DLT5, DLD3, DLV5)):
    assert abs(float(fmt(a, 1).replace(",", ".")) + float(fmt(b, 1).replace(",", ".")) - float(fmt(s, 1).replace(",", "."))) < 0.051, (a, b, s)
assert abs(0.002 / 1.20 * 100 - 0.1667) < 1e-3
# Bấm tay: kết luận trong lời văn "v ≈ 0,40 m/s"
assert fmt(VB1) == "0,40"

TOK = {
    "TBAR": fmt(TBAR1), "DT1": fmt(DT1), "DLT1": fmt(DLT1, 1), "DLS1": fmt(DLS1, 1), "VB1": fmt(VB1), "DLV1": fmt(DLV1, 1),
    "TBAR2": fmt(TBAR2, 3), "DT2": fmt(DT2, 4), "DLT2": fmt(DLT2, 1), "DLD2": fmt(DLD2, 1), "DLV2": fmt(DLV2, 1),
    "VB3": fmt(VB3), "DLD3": fmt(DLD3, 1), "DLT3": fmt(DLT3, 1), "DLV3": fmt(DLV3, 1), "DLV3F": fmt(DLV3 / 100), "DV3R": fmt(DV3), "DV3F": fmt(DV3, 3), "DV4F": fmt(DV4, 3),
    "VB4": fmt(VB4), "DLD4": fmt(DLD4, 1), "DLT4": fmt(DLT4, 1), "DLV4": fmt(DLV4, 1), "DV4R": fmt(DV4),
    "VB5": fmt(VB5), "DLT5": fmt(DLT5, 1), "DLV5": fmt(DLV5, 1),
    "C1": fmt(C1), "C2A": fmt(C2A, 1), "C2B": fmt(C2B, 1),
    "C3A": fmt(C3A, 0), "C3At": fmt(C3At, 0), "C3AT": fmt(C3A + C3At, 0), "C3B": fmt(C3B, 0), "C3Bt": fmt(C3Bt, 0), "C3BT": fmt(C3B + C3Bt, 0),
}
assert TOK["DT1"] == "0,11" and TOK["DLT1"] == "3,7" and TOK["DLS1"] == "0,2" and TOK["DLV1"] == "3,9"
assert TOK["DT2"] == "0,0012" and TOK["DLT2"] == "1,2" and TOK["DLD2"] == "2,0" and TOK["DLV2"] == "3,2"
assert TOK["C3AT"] == "14" and TOK["C3BT"] == "7" and TOK["C1"] == "0,50" and TOK["C2A"] == "2,5" and TOK["C2B"] == "5,0"

# ================= Hình 1: đường chạy, hai người bấm giờ ở vạch đích (không ghi số)
c = Canvas("f1", 420, 232)
YT = 140
XA, XB = 40, 380
c.line(XA - 14, YT, XB + 14, YT, "currentColor", 3, op=.55)
for xv in (XA, XB):
    c.line(xv, YT - 30, xv, YT + 20, "currentColor", 3)
c.text(XA, 186, "xuất phát", size=14, anchor="middle", weight="600")
c.text(XB, 186, "đích", size=14, anchor="middle", weight="600")
RX = 150
c.add(f'<circle cx="{RX}" cy="{YT-14}" r="10" fill="{ORG}" stroke="currentColor" stroke-width="1.5"/>')
c.arr("v", "b", RX + 18, YT - 14, RX + 78, YT - 14, 3)
c.text(RX + 86, YT - 9, "v", BLUE, 16, italic=True)
c.text(RX, YT - 44, "người chạy", size=14, anchor="middle", weight="600")
for k, cx in enumerate((300, 352), 1):
    cy = 62
    c.add(f'<circle cx="{cx}" cy="{cy}" r="15" fill="none" stroke="currentColor" stroke-width="2.5"/>')
    c.add(f'<rect x="{cx-3}" y="{cy-22}" width="6" height="6" fill="currentColor"/>')
    c.line(cx, cy, cx + 8, cy - 8, RED, 2.5)
    c.text(cx, 100, f"Bấm {k}", size=14, anchor="middle", weight="600")
c.arr("sL", "k", 210, 212, XA + 6, 212, 1.8, 9)
c.arr("sR", "k", 210, 212, XB - 6, 212, 1.8, 9)
c.text(210, 202, "quãng đường s (thước dây)", size=14, anchor="middle", weight="600")
ERR += [] if (c.arrows["v"][2] > c.arrows["v"][0]) else ["f1: mũi tên v sai chiều (phải hướng về đích)"]
ERR += [] if (XA + 6 < 210 < XB - 6) else ["f1: mũi tên khoảng cách lệch"]
fig1 = c.svg("Đường chạy có vạch xuất phát bên trái và vạch đích bên phải; người chạy hướng về đích; hai chiếc đồng hồ bấm giây đặt gần vạch đích, ghi là Bấm 1 và Bấm 2; quãng đường s đo bằng thước dây giữa hai vạch",
             "Hình 1. Hai bạn bấm giờ cho cùng một lượt chạy. Thước dây cho quãng đường <em>s</em>; hai đồng hồ cho hai số đo thời gian.")
ERR += c.check()

# ================= Hình 2: 5 lần bấm tay trên trục thời gian (TN1) + trung bình + dải sai số tuyệt đối
c = Canvas("f2", 420, 190)
TMIN, TMAX, XL, XR = 2.80, 3.30, 40, 380
X = lambda t: XL + (t - TMIN) / (TMAX - TMIN) * (XR - XL)
YA = 150
band_l, band_r = X(TBAR1 - DT1), X(TBAR1 + DT1)
c.add(f'<rect x="{band_l:.1f}" y="76" width="{band_r-band_l:.1f}" height="{YA-76}" fill="rgba(52,211,153,.18)"/>')
c.line(XL - 10, YA, XR + 10, YA, "currentColor", 2)
for k in range(6):
    tk = TMIN + 0.1 * k
    c.line(X(tk), YA, X(tk), YA + 7, "currentColor", 1.6)
    c.text(X(tk), YA + 24, fmt(tk, 1), size=13, anchor="middle", weight="600")
for t in T1CS:
    c.dot(X(t / 100), 112, 7, ORG)
    ERR += [] if TMIN < t / 100 < TMAX else [f"f2: điểm {t} ngoài trục"]
c.line(X(TBAR1), 66, X(TBAR1), YA, GRN, 3)
c.text(X(TBAR1), 58, "trung bình", GRN, 14, anchor="middle")
c.text(12, 40, "5 lần bấm", size=14, weight="600")
c.text(X(TBAR1) + 8, 96, "dải ± Δt", size=14, weight="600")
c.text(XR + 18, YA - 10, "t (s)", size=13, anchor="end", weight="600")
ERR += [] if abs(X(3.0) - (XL + 0.2 / 0.5 * 340)) < 1e-9 else ["f2: ánh xạ trục lệch"]
ERR += [] if band_l < min(X(t / 100) for t in T1CS if abs(t / 100 - TBAR1) <= DT1 + 1e-9) else ["f2: dải không phủ điểm"]
inside = [t for t in T1CS if abs(Decimal(t) - TBAR1CS) <= DT1CS]
assert len(inside) == 3, inside      # 3/5 điểm nằm trong dải ±Δt (3,04; 3,12; 2,92 → độ lệch 1, 9, 11 cs)
fig2 = c.svg("Trục thời gian từ 2,8 đến 3,3 giây có năm chấm cam là năm lần bấm tay, nằm rải hai phía vạch trung bình màu xanh lá; dải mờ quanh vạch trung bình thể hiện sai số tuyệt đối",
             "Hình 2. Năm lần bấm tay ở Thí nghiệm 1 (số liệu minh hoạ). Các chấm rải hai phía trung bình <em>t̄</em> = " + TOK["TBAR"] + " s; dải xanh là ± sai số tuyệt đối Δ<em>t</em> = " + TOK["DT1"] + " s.",
             exp="tn-l10-do-toc-do-01")
ERR += c.check()

# ================= Hình 3: xe + tấm chắn + cổng quang + đồng hồ hiện số
c = Canvas("f3", 420, 250)
YR = 158
c.line(20, YR, 400, YR, "currentColor", 3, op=.55)
# xe
c.add(f'<rect x="100" y="124" width="80" height="22" rx="3" fill="{ORG}" stroke="currentColor" stroke-width="1.5"/>')
for wx in (118, 162):
    c.add(f'<circle cx="{wx}" cy="152" r="6" fill="none" stroke="currentColor" stroke-width="2"/>')
# tấm chắn rộng d: từ x=150 tới x=172, cao từ 92 tới 124
SH0, SH1, SHT, SHB = 150, 172, 92, 124
c.add(f'<rect x="{SH0}" y="{SHT}" width="{SH1-SH0}" height="{SHB-SHT}" fill="rgba(56,189,248,.35)" stroke="{BLUE}" stroke-width="2"/>')
# cổng quang chữ U ngược, tia sáng ở y = 110 (nằm trong tầm cao của tấm chắn)
GL, GR, GT, YBEAM = 236, 276, 72, 110
c.add(f'<path d="M{GL},{YR} L{GL},{GT} L{GR},{GT} L{GR},{YR}" fill="none" stroke="currentColor" stroke-width="3"/>')
c.line(GL + 4, YBEAM, GR - 4, YBEAM, RED, 2.5, "5 4")
ERR += [] if SHT < YBEAM < SHB else ["f3: tia sáng không nằm trong tầm cao tấm chắn"]
# kích thước d phía trên tấm chắn
c.line(SH0, 84, SH1, 84, "currentColor", 1.6)
c.line(SH0, 79, SH0, 89, "currentColor", 1.6)
c.line(SH1, 79, SH1, 89, "currentColor", 1.6)
c.text((SH0 + SH1) / 2, 74, "d", size=16, anchor="middle", italic=True)
# vận tốc
c.arr("v", "b", 110, 44, 190, 44, 3)
c.text(198, 49, "v", BLUE, 16, italic=True)
c.text(144, 108, "tấm chắn", size=14, anchor="end", weight="600")
c.text((GL + GR) / 2, 64, "cổng quang", size=14, anchor="middle", weight="600")
c.text(20, 186, "đường ray", size=14, weight="600")
# đồng hồ
BX0, BY0, BW, BH = 270, 188, 130, 50
c.add(f'<rect x="{BX0}" y="{BY0}" width="{BW}" height="{BH}" rx="6" fill="none" stroke="currentColor" stroke-width="2.5"/>')
c.line(GR, YR, GR, BY0, "currentColor", 2)
c.text(BX0 + BW / 2, BY0 + 21, "đồng hồ", size=14, anchor="middle", weight="600")
c.text(BX0 + BW / 2, BY0 + 40, "hiện số", size=14, anchor="middle", weight="600")
ERR += [] if (c.arrows["v"][2] > c.arrows["v"][0] and c.arrows["v"][2] < GL) else ["f3: mũi tên v phải hướng về cổng"]
ERR += [] if (SH1 - SH0) > 0 and SH1 < GL else ["f3: tấm chắn phải ở phía trước cổng và chưa qua"]
fig3 = c.svg("Xe nhỏ trên đường ray có gắn tấm chắn rộng d đang chạy về phía cổng quang chữ U; tia hồng ngoại nằm ngang giữa hai chân cổng; cổng nối dây tới đồng hồ hiện số",
             "Hình 3. Cổng quang: tấm chắn rộng <em>d</em> che tia sáng trong thời gian <em>t</em>; đồng hồ hiện số cho <em>t</em>, tốc độ là <em>v</em> = <em>d</em>/<em>t</em>.",
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

b1 = table(["Lần", "$t$ (s)", "$|t - \\bar t|$ (s)"],
           [[i + 1, fmt(t / 100), fmt(float(d) / 100)] for i, (t, d) in enumerate(zip(T1CS, DEV1CS))],
           ["Trung bình", fmt(TBAR1), fmt(DT1)])
b2 = table(["Lần", "$t$ (s)", "$v = d/t$ (m/s)"],
           [[i + 1, fmt(t / 1000, 3), fmt(v, 3)] for i, (t, v) in enumerate(zip(T2MS, V2))],
           ["Trung bình", fmt(TBAR2, 3), fmt(VB2, 3)])
b3 = table(["$d$ (cm)", "$t$ hiện (s)", "$d/t$ (m/s)"],
           [[fmt(dcm, 1), fmt(tms / 1000, 3), fmt(vmm / 1000, 3)] for (dcm, _, tms, _), vmm in zip(ROW3, V3MM)])

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, fg in enumerate((fig1, fig2, fig3), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
for k, b in (("__BANG_TN1__", b1), ("__BANG_TN2__", b2), ("__BANG_TN3__", b3)):
    assert k in h, k
    h = h.replace(k, b)
# @@TOKEN:m@@ (trong công thức, {,}) và @@TOKEN@@ (chữ thường)
def rep(m):
    name, mode = m.group(1), m.group(2)
    assert name in TOK, name
    return mth(TOK[name]) if mode else TOK[name]
h = re.sub(r"@@([A-Za-z0-9]+)(:m)?@@", rep, h)
assert "@@" not in h and "__" not in h.replace("__PHUT__", "")
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
BASE = {"mon": "vat-ly", "lop": 10, "bai": "Bài 6. Thực hành: Đo tốc độ của vật chuyển động", "lesson_id": 51,
        "nguon_trong_bai": "content/lesson-samples/l10-thuc-hanh-do-toc-do/theory.html"}
vn1 = lambda x, nd=2: fmt(x, nd)
tn = [
    {**BASE,
     "id": "tn-l10-do-toc-do-01",
     "ten": "Đo tốc độ xe đồ chơi bằng thước và đồng hồ bấm giây, 5 lần bấm",
     "loai": "thi_nghiem", "muc_do": "co_ban",
     "kien_thuc": ["dotocdo.v_bang_s_chia_t", "dotocdo.sai_so_tuyet_doi", "dotocdo.sai_so_tuong_doi", "dotocdo.do_tre_phan_xa"],
     "muc_tieu": "Từ năm số đo thời gian bấm tay, tính giá trị trung bình, sai số tuyệt đối, sai số tương đối và tốc độ trung bình của xe; nhận ra nguồn sai số chính là độ trễ phản xạ của người bấm.",
     "dung_cu": [{"ten": "Thước dây (chia 1 mm)", "so_luong": 1}, {"ten": "Xe đồ chơi chạy đều (pin)", "so_luong": 1},
                 {"ten": "Đồng hồ bấm giây", "so_luong": 1}, {"ten": "Băng dính đánh dấu vạch xuất phát và vạch đích", "so_luong": 2}],
     "cac_buoc": {"lam": ["Kẻ vạch xuất phát và vạch đích cách nhau 1,20 m bằng thước dây (sai số 0,002 m).",
                          "Cho xe chạy đều qua; một bạn bấm khi xe qua vạch đầu và bấm lại khi qua vạch cuối. Lặp 5 lần."],
                  "quan_sat": ["Năm số đo t: " + "; ".join(vn1(t / 100) for t in T1CS) + " s.", "Số đo lệch hai phía quanh giá trị trung bình, cỡ vài phần mười giây."],
                  "rut_ra": [f"t̄ = {TOK['TBAR']} s; Δt = {TOK['DT1']} s; δt ≈ {TOK['DLT1']} %.",
                             f"v̄ = s/t̄ ≈ {TOK['VB1']} m/s với δv ≈ {TOK['DLV1']} % (δs ≈ {TOK['DLS1']} %). Sai số chủ yếu do độ trễ phản xạ; kéo dài đường chạy làm δt nhỏ đi."]},
     "tham_so": [{"ky_hieu": "s", "ten": "Quãng đường đo", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.5, "max": 3.0, "mac_dinh": S1, "buoc": 0.1},
                 {"ky_hieu": "v_that", "ten": "Tốc độ thật của xe", "don_vi": "m/s", "kieu": "dieu_chinh", "min": 0.2, "max": 1.0, "mac_dinh": 0.4, "buoc": 0.05},
                 {"ky_hieu": "tre", "ten": "Độ lệch phản xạ cực đại mỗi lần bấm", "don_vi": "s", "kieu": "dieu_chinh", "min": 0.0, "max": 0.3, "mac_dinh": 0.2, "buoc": 0.01},
                 {"ky_hieu": "t", "ten": "Thời gian đo (đồng hồ bấm tay)", "don_vi": "s", "kieu": "do_duoc", "sai_so_do": DT1},
                 {"ky_hieu": "v", "ten": "Tốc độ trung bình", "don_vi": "m/s", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["t_thật = s/v_thật", "t_i = t_thật + e_i (e_i: độ trễ phản xạ ngẫu nhiên hai phía)", "t̄ = Σt_i/n", "Δt = Σ|t_i − t̄|/n", "δt = Δt/t̄", "δv = δs + δt"],
                 "gia_thiet": ["xe chạy đều", "e_i là dãy giả định (+0,12; −0,14; +0,04; +0,21; −0,08 s), không phải đo thật", "sai số thước dây Δs = 0,002 m"]},
     "so_lieu_mau": {"cot": ["Lần", "t (s)", "|t − t̄| (s)"],
                     "hang": [[i + 1, t / 100, float(d) / 100] for i, (t, d) in enumerate(zip(T1CS, DEV1CS))],
                     "ghi_chu": f"Số liệu minh hoạ tính từ mô hình (t thật = 3,00 s). t̄ = {TOK['TBAR']} s, Δt = {TOK['DT1']} s (11,2 cs), δt = {TOK['DLT1']} %."},
     "ket_qua_ky_vong": f"v̄ ≈ {TOK['VB1']} m/s, δv ≈ {TOK['DLV1']} %.",
     "hien_tuong_hay_sai": ["Chỉ bấm một lần rồi kết luận.", "Tưởng đồng hồ bấm giây đắt hơn thì hết sai số do phản xạ.", "Rút ngắn đường chạy cho dễ quan sát, làm δt tăng lên."],
     "sai_so_thuong_gap": "Độ trễ phản xạ của người bấm (đầu và cuối đoạn), vạch kẻ lệch, xe không chạy thật đều.",
     "an_toan": "Chặn cuối đường chạy để xe không rơi khỏi bàn.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu",
                        "y_tuong": "Xe chạy qua hai vạch; người dùng bấm hai nút Bắt đầu/Dừng, mô phỏng thêm độ trễ ngẫu nhiên; bảng điền dần sau mỗi lần chạy.",
                        "diem_nhan": "Kéo thanh trượt độ trễ và độ dài đường chạy để thấy δt thay đổi."}},
    {**BASE,
     "id": "tn-l10-do-toc-do-02",
     "ten": "Đo tốc độ xe bằng cổng quang và tấm chắn 5,0 cm, 5 lần đo",
     "loai": "thi_nghiem", "muc_do": "trung_binh",
     "kien_thuc": ["dotocdo.cong_quang", "dotocdo.v_bang_d_chia_t", "dotocdo.sai_so_tuong_doi", "dotocdo.nguon_sai_so_lon_nhat"],
     "muc_tieu": "Từ năm số đo thời gian che cổng quang, tính v = d/t từng lần và trung bình, tính δt, δd, δv và chỉ ra nguồn sai số lớn nhất là phép đo bề rộng tấm chắn.",
     "dung_cu": [{"ten": "Cổng quang nối đồng hồ hiện số (chia 0,001 s)", "so_luong": 1}, {"ten": "Xe nhỏ trên đường ray", "so_luong": 1},
                 {"ten": "Tấm chắn rộng 5,0 cm", "so_luong": 1}, {"ten": "Thước chia mm", "so_luong": 1}],
     "cac_buoc": {"lam": ["Gắn tấm chắn d = 5,0 cm lên xe, đo d bằng thước chia mm (Δd = 0,1 cm).",
                          "Cho xe chạy đều qua cổng quang, ghi thời gian che tia sáng. Lặp 5 lần."],
                  "quan_sat": ["Năm số đo t: " + "; ".join(vn1(t / 1000, 3) for t in T2MS) + " s.", "Số đo chỉ lệch nhau vài phần nghìn giây."],
                  "rut_ra": [f"t̄ = {TOK['TBAR2']} s; δt ≈ {TOK['DLT2']} %; δd = {TOK['DLD2']} %; δv ≈ {TOK['DLV2']} %.",
                             "Nguồn sai số lớn nhất là đo bề rộng tấm chắn bằng thước, không phải đồng hồ."]},
     "tham_so": [{"ky_hieu": "d", "ten": "Bề rộng tấm chắn", "don_vi": "cm", "kieu": "dieu_chinh", "min": 1.0, "max": 10.0, "mac_dinh": 5.0, "buoc": 0.5},
                 {"ky_hieu": "v_that", "ten": "Tốc độ thật của xe", "don_vi": "m/s", "kieu": "dieu_chinh", "min": 0.2, "max": 1.0, "mac_dinh": 0.5, "buoc": 0.05},
                 {"ky_hieu": "Dd", "ten": "Sai số đo bề rộng tấm chắn", "don_vi": "cm", "kieu": "co_dinh", "gia_tri": 0.1},
                 {"ky_hieu": "t", "ten": "Thời gian che cổng", "don_vi": "s", "kieu": "do_duoc", "sai_so_do": DT2},
                 {"ky_hieu": "v", "ten": "Tốc độ", "don_vi": "m/s", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["t = d/v_thật", "v = d/t", "δt = Δt/t̄", "δd = Δd/d", "δv = δd + δt"],
                 "gia_thiet": ["xe chạy đều", "dãy t là giả định (98; 101; 100; 102; 99 ms), không phải đo thật", "đồng hồ chia 0,001 s"]},
     "so_lieu_mau": {"cot": ["Lần", "t (s)", "v = d/t (m/s)"],
                     "hang": [[i + 1, t / 1000, v] for i, (t, v) in enumerate(zip(T2MS, V2))],
                     "ghi_chu": f"Số liệu minh hoạ. t̄ = {TOK['TBAR2']} s, Δt = 0,0012 s, v̄ = d/t̄ = {fmt(VB2, 3)} m/s."},
     "ket_qua_ky_vong": f"v̄ ≈ {fmt(VB2, 2)} m/s, δv ≈ {TOK['DLV2']} %; δd lớn hơn δt.",
     "hien_tuong_hay_sai": ["Tưởng đồng hồ hiện số thì kết quả hoàn toàn không có sai số.", "Bỏ qua sai số của phép đo d."],
     "sai_so_thuong_gap": "Đo bề rộng tấm chắn bằng thước chia mm; tấm chắn nghiêng; mép tấm chắn không vuông.",
     "an_toan": "Chặn cuối đường ray để xe không rơi.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu",
                        "y_tuong": "Xe mang tấm chắn qua cổng; đồng hồ hiện số hiện t, bảng tính v = d/t từng lần và trung bình.",
                        "diem_nhan": "Thanh trượt bề rộng tấm chắn: thấy δd đổi theo d trong khi δt thay đổi ngược lại."}},
    {**BASE,
     "id": "tn-l10-do-toc-do-03",
     "ten": "Tấm chắn rộng hay hẹp: d/t với xe đang nhanh dần",
     "loai": "thi_nghiem", "muc_do": "trung_binh",
     "kien_thuc": ["dotocdo.toc_do_trung_binh_tren_d", "dotocdo.toc_do_tuc_thoi", "dotocdo.do_phan_giai_dong_ho"],
     "muc_tieu": "Thấy d/t là tốc độ trung bình trên bề rộng tấm chắn: d giảm thì sát tốc độ lúc vào cổng, nhưng d quá hẹp thì độ phân giải của đồng hồ gây sai số lớn.",
     "dung_cu": [{"ten": "Cổng quang nối đồng hồ hiện số (chia 0,001 s)", "so_luong": 1}, {"ten": "Xe nhanh dần trên máng nghiêng", "so_luong": 1},
                 {"ten": "Bốn tấm chắn rộng 10,0; 5,0; 2,0; 1,0 cm", "so_luong": 4}],
     "cac_buoc": {"lam": ["Xe thả từ trên máng nghiêng, mép trước tấm chắn vào cổng với tốc độ 0,600 m/s (minh hoạ, mỗi giây tăng thêm 0,50 m/s).",
                          "Lần lượt thay bốn tấm chắn, ghi t và tính d/t."],
                  "quan_sat": ["d/t: " + "; ".join(fmt(v / 1000, 3) for v in V3MM) + " m/s ứng với d = 10,0; 5,0; 2,0; 1,0 cm."],
                  "rut_ra": ["d giảm thì d/t tiến sát 0,600 m/s (tốc độ lúc mép trước vào cổng).",
                             "Tới d = 1,0 cm, t = 0,0166 s mà đồng hồ chỉ hiện 0,017 s nên sai số làm tròn (khoảng 3 %) lấn át, d/t = 0,588 m/s lệch xa hơn hàng d = 2,0 cm."]},
     "tham_so": [{"ky_hieu": "d", "ten": "Bề rộng tấm chắn", "don_vi": "cm", "kieu": "dieu_chinh", "min": 0.5, "max": 10.0, "mac_dinh": 2.0, "buoc": 0.5},
                 {"ky_hieu": "v1", "ten": "Tốc độ lúc mép trước vào cổng", "don_vi": "m/s", "kieu": "dieu_chinh", "min": 0.2, "max": 1.0, "mac_dinh": V1, "buoc": 0.05},
                 {"ky_hieu": "a", "ten": "Mức tăng tốc độ mỗi giây", "don_vi": "m/s²", "kieu": "dieu_chinh", "min": 0.1, "max": 1.0, "mac_dinh": A3, "buoc": 0.05},
                 {"ky_hieu": "buoc_dh", "ten": "Bước chia của đồng hồ", "don_vi": "s", "kieu": "co_dinh", "gia_tri": 0.001},
                 {"ky_hieu": "t", "ten": "Thời gian che cổng", "don_vi": "s", "kieu": "do_duoc", "sai_so_do": 0.0005},
                 {"ky_hieu": "v_tb", "ten": "d/t", "don_vi": "m/s", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["d = v1·t + a·t²/2", "t = (−v1 + √(v1² + 2·a·d))/a", "t hiện = t làm tròn tới 0,001 s", "v_tb = d/t hiện"],
                 "gia_thiet": ["xe nhanh dần đều trong lúc tấm chắn qua", "đồng hồ chia 0,001 s, không thêm nhiễu"]},
     "so_lieu_mau": {"cot": ["d (cm)", "t thật (s)", "t hiện (s)", "d/t (m/s)"],
                     "hang": [[dcm, round(t, 4), tms / 1000, vmm / 1000] for (dcm, t, tms, _), vmm in zip(ROW3, V3MM)],
                     "ghi_chu": "Số liệu minh hoạ tính từ mô hình v1 = 0,600 m/s, a = 0,50 m/s²; d/t tính từ t hiện (đã làm tròn 0,001 s)."},
     "ket_qua_ky_vong": "d/t = 0,641; 0,617; 0,606; 0,588 m/s; lệch nhỏ nhất so với 0,600 ở d = 2,0 cm.",
     "hien_tuong_hay_sai": ["Tưởng d/t luôn là tốc độ tức thời tại cổng.", "Cho rằng tấm chắn càng hẹp càng tốt, bỏ qua độ phân giải của đồng hồ."],
     "sai_so_thuong_gap": "Làm tròn 0,001 s của đồng hồ; mép tấm chắn không vuông góc.",
     "goi_y_mo_phong": {"loai": "do_thi+bang_so_lieu",
                        "y_tuong": "Thanh trượt bề rộng tấm chắn; bảng cập nhật t hiện và d/t, đường chấm 0,600 m/s để so sánh.",
                        "diem_nhan": "Đặt d rất nhỏ để thấy d/t dao động vì làm tròn."}},
]
for d in tn:
    (ROOT / "content/thi-nghiem" / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"ok theory.html {len(h)} ký tự · 3 hình · {phut} phút · 3 file thí nghiệm")
