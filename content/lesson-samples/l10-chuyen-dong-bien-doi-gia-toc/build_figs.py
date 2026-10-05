"""Sinh 4 hình SVG + bảng số liệu thí nghiệm cho bài 'Chuyển động biến đổi. Gia tốc' (lesson 53),
thay mốc <!--FIGn-->, __BANG_TN1__, __A_TONG__, __PHUT__ trong theory.src.html -> theory.html,
và ghi 3 file thí nghiệm content/thi-nghiem/tn-l10-gia-toc-0{1,2,3}.json (số liệu tính từ cùng mô hình).
Có lớp kiểm hình học: hộp nhãn không chồng nhau, không vượt viewBox; mũi tên đúng chiều vật lí.
Chạy: python3 build_figs.py   (sau đó: python3 build_bundle.py)"""
import json, math, pathlib, re, subprocess, sys
from svg_lib import RED, BLUE, ORG, GRN, wrap

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}


def sub(base, s, size=11):
    return f'{base}<tspan baseline-shift="sub" font-size="{size}">{s}</tspan>'


def vn(x, nd=2):
    """Số kiểu Việt Nam trong $…$: dấu phẩy thập phân viết {,}."""
    s = f"{x:.{nd}f}"
    return s.replace(".", "{,}")


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
            if a[5] < 13 and not a[0].isdigit():
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
G = 9.8

# ================= Mô hình số liệu (dùng chung cho hình, bảng và file thí nghiệm)
# TN2 (Hình 1): vị trí viên bi mỗi 0,2 s (cm). Bàn: v = 0,4 m/s; xuống dốc: v0 = 0, a = 1 m/s²; lên dốc: v0 = 0,8 m/s, a = −1 m/s².
DT1 = 0.2
ROWS = [("Trên bàn: gần thẳng đều", 0.4, 0.0), ("Xuống dốc: nhanh dần đều", 0.0, 1.0), ("Lên dốc: chậm dần đều", 0.8, -1.0)]
POS = [[round(100 * (v0 * n * DT1 + 0.5 * a * (n * DT1) ** 2), 2) for n in range(5)] for _, v0, a in ROWS]
assert all(abs(p[-1] - 32) < 1e-9 for p in POS), POS

# TN1: xe lăn xuống máng nghiêng, sinα = 0,05 (bỏ ma sát): a = g·sinα; v0 = 0,20 m/s; máy hiện tới 0,01 m/s.
SINA, V0 = 0.05, 0.20
A1 = G * SINA
T1 = [round(0.2 * k, 1) for k in range(5)]
VT = [V0 + A1 * t for t in T1]
VD = [round(v + 1e-9, 2) for v in VT]
AK = [None] + [round((VD[k] - VD[k - 1]) / (T1[k] - T1[k - 1]), 2) for k in range(1, 5)]
ATONG = (VD[-1] - VD[0]) / (T1[-1] - T1[0])
assert sorted(set(a for a in AK if a)) == [0.45, 0.5], AK   # khớp lời "có số 0,45 lẫn 0,50" trong details

# Bài toán mẫu: 54 km/h, dừng sau 5 s.
VB, TB = 54 / 3.6, 5.0
AB = (0 - VB) / TB
SB = 0.5 * VB * TB
assert abs(VB - 15) < 1e-9 and abs(AB + 3) < 1e-9 and abs(SB - 37.5) < 1e-9

# ================= Hình 1: dấu vết viên bi mỗi 0,2 s
c = Canvas("f1", 420, 270)
X0, SC = 40, 340 / 32
for r, ((name, v0, a), pos) in enumerate(zip(ROWS, POS)):
    y = 70 + 80 * r
    c.line(28, y, 404, y, "currentColor", 2, op=.35)
    for p in pos:
        c.add(f'<circle cx="{X0 + p * SC:.1f}" cy="{y}" r="6" fill="{ORG}" stroke="currentColor" stroke-width="1.2"/>')
    c.text(14, y - 26, name, size=14)
    c.arr(f"v{r}", "b", 250, y - 31, 292, y - 31, 3)
    c.text(298, y - 26, "v", BLUE, 16, italic=True)
    if a == 0:
        c.text(330, y - 26, "a = 0", GRN, 14, italic=True)
    elif a > 0:
        c.arr(f"a{r}", "g", 330, y - 31, 372, y - 31, 3)
        c.text(378, y - 26, "a", GRN, 16, italic=True)
    else:
        c.arr(f"a{r}", "g", 372, y - 31, 330, y - 31, 3)
        c.text(378, y - 26, "a", GRN, 16, italic=True)
    c.text(X0 - 6, y + 24, "t = 0", size=13, weight="600")
    c.text(X0 + pos[-1] * SC, y + 24, "0,8 s", size=13, anchor="middle", weight="600")
    # kiểm: khoảng cách giữa các chấm đều / tăng / giảm đúng loại chuyển động
    gaps = [b - a_ for a_, b in zip(pos, pos[1:])]
    ok = (all(abs(g - gaps[0]) < 1e-9 for g in gaps) if a == 0 else
          all(g2 > g1 for g1, g2 in zip(gaps, gaps[1:])) if a > 0 else all(g2 < g1 for g1, g2 in zip(gaps, gaps[1:])))
    ERR += [] if ok else [f"f1: hàng {r} khoảng cách sai loại"]
    if a:
        x1, _, x2, _ = c.arrows[f"a{r}"]
        ERR += [] if (x2 - x1) * a > 0 else [f"f1: mũi tên a hàng {r} sai chiều"]
fig1 = c.svg("Ba hàng chấm vị trí viên bi sau mỗi 0,2 giây: trên bàn cách đều, xuống dốc khoảng cách tăng dần với gia tốc cùng chiều vận tốc, lên dốc khoảng cách giảm dần với gia tốc ngược chiều vận tốc",
             "Hình 1. Vị trí viên bi sau mỗi 0,2 s (số liệu minh hoạ). Khoảng cách đều: vận tốc không đổi. Dài dần: nhanh dần, <em>a</em> cùng chiều <em>v</em>. Ngắn dần: chậm dần, <em>a</em> ngược chiều <em>v</em>.",
             exp="tn-l10-gia-toc-02")
ERR += c.check()

# ================= Hình 2: đồ thị v–t ba loại chuyển động + tam giác độ dốc + diện tích
c = Canvas("f2", 420, 260)
OX, OY, XS, VS = 52, 220, 56, 14
X = lambda t: OX + XS * t
Y = lambda v: OY - VS * v
c.add(f'<rect x="{X(1):.1f}" y="{Y(5):.1f}" width="{X(3)-X(1):.1f}" height="{OY-Y(5):.1f}" fill="rgba(251,146,60,.2)"/>')
c.arr("tx", "k", OX, OY, 372, OY, 1.8, 9)
c.arr("vy", "k", OX, OY, OX, 30, 1.8, 9)
c.text(60, 40, "v (m/s)", size=13, weight="600")
c.text(362, 244, "t (s)", size=13, weight="600")
c.text(36, 238, "O", size=13, weight="600")
LINES = [("nhanh dần", GRN, 2, 1.8), ("đều", ORG, 5, 0), ("chậm dần", BLUE, 10, -1.6)]
for name, col, v0, a in LINES:
    c.line(X(0), Y(v0), X(5), Y(v0 + 5 * a), col, 3)
    c.text(X(5) + 6, Y(v0 + 5 * a) + 5, name, col, 14)
# tam giác độ dốc trên đường nhanh dần, t = 3 → 4 s
t1, t2 = 3, 4
va, vb = 2 + 1.8 * t1, 2 + 1.8 * t2
c.line(X(t1), Y(va), X(t2), Y(va), "currentColor", 1.6, "5 4")
c.line(X(t2), Y(va), X(t2), Y(vb), "currentColor", 1.6, "5 4")
c.text((X(t1) + X(t2)) / 2, Y(va) + 18, "Δt", size=14, anchor="middle")
c.text(X(t2) + 6, (Y(va) + Y(vb)) / 2 + 5, "Δv", size=14)
c.text((X(1) + X(3)) / 2, 196, "diện tích = d", size=13, anchor="middle", weight="600")
ERR += [] if Y(vb) < Y(va) else ["f2: tam giác độ dốc sai chiều"]
fig2 = c.svg("Đồ thị vận tốc theo thời gian: đường nằm ngang là chuyển động đều, đường đi lên là nhanh dần, đường đi xuống là chậm dần; tam giác Δt, Δv trên đường nhanh dần; vùng tô dưới đường nằm ngang là độ dịch chuyển",
             "Hình 2. Đồ thị <em>v</em>–<em>t</em> (với <em>v</em> &gt; 0): nằm ngang là thẳng đều; xiên lên là nhanh dần đều, xiên xuống là chậm dần đều. Độ dốc Δ<em>v</em>/Δ<em>t</em> là gia tốc; diện tích dưới đồ thị là độ dịch chuyển <em>d</em>.")
ERR += c.check()

# ================= Hình 3: xe vào cua với tốc độ không đổi — Δv hướng vào trong cua
c = Canvas("f3", 420, 240)
CX, CY, R = 130, 215, 110
P = lambda deg: (CX + R * math.cos(math.radians(deg)), CY - R * math.sin(math.radians(deg)))
s0, s1 = P(165), P(15)
c.add(f'<path d="M{s0[0]:.1f},{s0[1]:.1f} A{R},{R} 0 0 1 {s1[0]:.1f},{s1[1]:.1f}" fill="none" stroke="currentColor" stroke-width="14" opacity=".15"/>')
c.add(f'<path d="M{s0[0]:.1f},{s0[1]:.1f} A{R},{R} 0 0 1 {s1[0]:.1f},{s1[1]:.1f}" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="6 5" opacity=".6"/>')
LV = 64
vecs = {}
for k, deg in ((1, 150), (2, 30)):
    px, py = P(deg)
    th = math.radians(deg)
    ux, uy = math.sin(th), math.cos(th)     # tiếp tuyến khi đi thuận kim (trái → phải qua đỉnh), toạ độ màn hình
    vecs[k] = (ux * LV, uy * LV)
    c.add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="7" fill="{ORG}" stroke="currentColor" stroke-width="1.2"/>')
    c.arr(f"v{k}", "b", px, py, px + ux * LV, py + uy * LV, 3)
    # kiểm: vận tốc vuông góc bán kính
    ERR += [] if abs(ux * (px - CX) + uy * (py - CY)) < 1e-6 else [f"f3: v{k} không tiếp tuyến"]
c.text(18, 120, sub("v", "1", 12), BLUE, 16, italic=True)
c.text(262, 200, sub("v", "2", 12), BLUE, 16, italic=True)
c.dot(CX, CY, 3.5)
c.text(CX, 234, "tâm cua", size=13, anchor="middle", weight="600")
# ghép gốc: v1, v2 từ cùng điểm Q; Δv từ đỉnh v1 tới đỉnh v2
QX, QY = 330, 80
(a1, b1), (a2, b2) = vecs[1], vecs[2]
c.arr("w1", "b", QX, QY, QX + a1, QY + b1, 3)
c.arr("w2", "b", QX, QY, QX + a2, QY + b2, 3)
c.arr("dv", "g", QX + a1, QY + b1, QX + a2, QY + b2, 3)
c.dot(QX, QY, 3)
c.text(QX + 6, QY + b1 + 30, sub("v", "1", 12), BLUE, 16, anchor="end", italic=True)
c.text(QX + 6, QY + b2 - 18, sub("v", "2", 12), BLUE, 16, anchor="end", italic=True)
c.text(QX + a1 + 8, QY + 6, "Δv", GRN, 16)
c.text(292, 168, "Δv hướng vào", size=13, weight="600")
c.text(292, 186, "phía trong cua", size=13, weight="600")
dvx, dvy = a2 - a1, b2 - b1
mx, my = P(90)
ERR += [] if (dvx * (CX - mx) + dvy * (CY - my)) > 0 and abs(dvx) < 1e-6 else ["f3: Δv không hướng vào tâm"]
ERR += [] if abs(math.hypot(a1, b1) - math.hypot(a2, b2)) < 1e-9 else ["f3: |v1| ≠ |v2|"]
fig3 = c.svg("Xe đi qua khúc cua tròn với tốc độ không đổi: vận tốc ở vị trí 1 và 2 dài bằng nhau nhưng khác hướng; ghép chung gốc, vectơ Δv từ đỉnh v1 tới đỉnh v2 hướng vào phía trong cua",
             "Hình 3. Vào cua với tốc độ không đổi: hai mũi tên vận tốc dài bằng nhau nhưng khác hướng. Ghép chung gốc, Δ<em>v</em> = <em>v</em><sub>2</sub> − <em>v</em><sub>1</sub> khác 0 và hướng vào phía trong cua, nên xe có gia tốc.")
ERR += c.check()

# ================= Hình 4: đồ thị v–t của ô tô hãm phanh (bài toán mẫu) — chỉ ghi dữ liệu đề cho
c = Canvas("f4", 400, 250)
OX, OY, XS, VS = 56, 210, 56, 10
X = lambda t: OX + XS * t
Y = lambda v: OY - VS * v
c.add(f'<polygon points="{X(0)},{Y(VB):.1f} {X(TB)},{OY} {OX},{OY}" fill="rgba(56,189,248,.2)"/>')
c.arr("tx", "k", OX, OY, 372, OY, 1.8, 9)
c.arr("vy", "k", OX, OY, OX, 26, 1.8, 9)
c.line(X(0), Y(VB), X(TB), Y(0), BLUE, 3)
c.dot(X(0), Y(VB), 4, BLUE)
c.dot(X(TB), Y(0), 4, BLUE)
c.text(48, Y(VB) + 5, "15", size=13, anchor="end", weight="600")
c.text(X(TB), 230, "5", size=13, anchor="middle", weight="600")
c.text(40, 228, "O", size=13, weight="600")
c.text(66, 34, "v (m/s)", size=13, weight="600")
c.text(348, 192, "t (s)", size=13, weight="600")
c.text(110, 186, "s = diện tích", size=13, weight="600")
# kiểm: nhãn diện tích nằm trong tam giác (dưới đường thẳng)
for xx in (110, 110 + 0.58 * 13 * 13):
    ytop = Y(VB) + (xx - OX) / (X(TB) - OX) * (OY - Y(VB))
    ERR += [] if 176 > ytop else ["f4: nhãn diện tích lọt ra ngoài tam giác"]
fig4 = c.svg("Đồ thị vận tốc theo thời gian của ô tô hãm phanh: đoạn thẳng đi xuống từ 15 m/s lúc t = 0 tới 0 lúc t = 5 s; vùng tam giác dưới đồ thị được tô",
             "Hình 4. Đồ thị <em>v</em>–<em>t</em> của ô tô hãm phanh: từ 15 m/s giảm đều về 0 sau 5 s. Quãng đường hãm phanh bằng diện tích tam giác tô màu.",
             exp="tn-l10-gia-toc-03")
ERR += c.check()

if ERR:
    print("\n".join("✗ " + e for e in ERR)); sys.exit(1)

# ================= Bảng số liệu TN1 (chèn vào bài)
rows = []
for t, v, a in zip(T1, VD, AK):
    rows.append(f"<tr><td>{vn(t,1).replace('{,}', ',')}</td><td>{vn(v).replace('{,}', ',')}</td>"
                f"<td>{'—' if a is None else vn(a).replace('{,}', ',')}</td></tr>")
bang = ('<div class="table-scroll">\n<table class="tl-table">\n<thead>\n'
        '<tr><th>$t$ (s)</th><th>$v$ (m/s)</th><th>$\\Delta v/\\Delta t$ (m/s²)</th></tr>\n</thead>\n<tbody>\n'
        + "\n".join(rows) + "\n</tbody>\n</table>\n</div>")
atong = (f"$\\dfrac{{{vn(VD[-1])} - {vn(VD[0])}}}{{{vn(T1[-1],1)}}} \\approx {vn(ATONG)}\\ \\text{{m/s}}^2$")

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, fg in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
h = h.replace("__BANG_TN1__", bang).replace("__A_TONG__", atong)
assert "__" not in h.replace("__PHUT__", "")
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
BASE = {"mon": "vat-ly", "lop": 10, "bai": "Bài 8. Chuyển động biến đổi. Gia tốc", "lesson_id": 53,
        "nguon_trong_bai": "content/lesson-samples/l10-chuyen-dong-bien-doi-gia-toc/theory.html"}
r2 = lambda x: round(x, 3)
tn = [
    {**BASE,
     "id": "tn-l10-gia-toc-01",
     "ten": "Đo gia tốc xe lăn xuống máng nghiêng từ vận tốc ở 5 thời điểm",
     "loai": "thi_nghiem", "muc_do": "trung_binh",
     "kien_thuc": ["giatoc.dinh_nghia", "giatoc.a_bang_dv_chia_dt", "giatoc.nhanh_dan_deu"],
     "muc_tieu": "Từ bảng vận tốc của xe ở các thời điểm cách đều 0,2 s, tính Δv/Δt từng khoảng, thấy nó gần như không đổi (chuyển động nhanh dần đều) và nhận xét sai số do làm tròn số đo.",
     "dung_cu": [{"ten": "Máng nghiêng thẳng (sinα ≈ 0,05)", "so_luong": 1},
                 {"ten": "Xe lăn nhẹ, ít ma sát", "so_luong": 1},
                 {"ten": "Cảm biến chuyển động nối máy tính, hoặc điện thoại quay video + phần mềm Tracker", "so_luong": 1}],
     "cac_buoc": {"lam": ["Đặt máng nghiêng có sinα ≈ 0,05, thả xe lăn xuống (xe đã có vận tốc nhỏ khi bắt đầu ghi).",
                          "Ghi vận tốc của xe ở 5 thời điểm cách nhau 0,2 s (t = 0; 0,2; 0,4; 0,6; 0,8 s), máy hiện tới 0,01 m/s."],
                  "quan_sat": ["Vận tốc lần lượt " + "; ".join(f"{v:.2f}".replace(".", ",") for v in VD) + " m/s.",
                               "Sau mỗi 0,2 s vận tốc tăng gần như cùng một lượng (0,09–0,10 m/s)."],
                  "rut_ra": ["Xe chuyển động nhanh dần đều; Δv/Δt gần như không đổi, đó là gia tốc a ≈ 0,49 m/s².",
                             "Lấy khoảng thời gian dài cho gia tốc tin cậy hơn vì sai số làm tròn chiếm phần nhỏ hơn."]},
     "tham_so": [{"ky_hieu": "sin_alpha", "ten": "Sin góc nghiêng máng", "don_vi": "", "kieu": "dieu_chinh", "min": 0.02, "max": 0.15, "mac_dinh": SINA, "buoc": 0.01},
                 {"ky_hieu": "v0", "ten": "Vận tốc lúc bắt đầu ghi", "don_vi": "m/s", "kieu": "dieu_chinh", "min": 0, "max": 0.5, "mac_dinh": V0, "buoc": 0.05},
                 {"ky_hieu": "g", "ten": "Gia tốc rơi tự do", "don_vi": "m/s²", "kieu": "co_dinh", "gia_tri": G},
                 {"ky_hieu": "v", "ten": "Vận tốc máy ghi", "don_vi": "m/s", "kieu": "do_duoc", "sai_so_do": 0.005},
                 {"ky_hieu": "a", "ten": "Gia tốc", "don_vi": "m/s²", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["a = g·sinα", "v = v0 + a·t", "v (đọc) = v làm tròn tới 0,01 m/s", "a_khoảng = Δv/Δt"],
                 "gia_thiet": ["bỏ qua ma sát và quán tính bánh xe", "máng thẳng", "g = 9,8 m/s²"]},
     "so_lieu_mau": {"cot": ["t (s)", "v tính (m/s)", "v đọc (m/s)", "Δv/Δt (m/s²)"],
                     "hang": [[t, r2(vt), vd, a] for t, vt, vd, a in zip(T1, VT, VD, AK)],
                     "ghi_chu": f"Số liệu minh hoạ tính từ mô hình (a = 9,8·0,05 = {A1:.2f} m/s², v0 = 0,20 m/s), chỉ làm tròn tới 0,01 m/s, không thêm nhiễu. Δv/Δt cả khoảng 0–0,8 s = {ATONG:.4f} m/s²."},
     "ket_qua_ky_vong": "Δv/Δt từng khoảng dao động 0,45–0,50 m/s² do làm tròn; cả khoảng 0–0,8 s cho ≈ 0,49 m/s², khớp g·sinα.",
     "hien_tuong_hay_sai": ["Thấy 0,45 và 0,50 lệch nhau, tưởng chuyển động không đều.", "Lấy v/t thay vì Δv/Δt (quên vận tốc đầu khác 0)."],
     "sai_so_thuong_gap": "Làm tròn số đo vận tốc, máng cong, ma sát ở trục bánh xe.",
     "an_toan": "Chặn cuối máng để xe không rơi khỏi bàn.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu+do_thi",
                        "y_tuong": "Xe lăn trên máng có thanh trượt góc nghiêng; bảng tự điền v mỗi 0,2 s (làm tròn 0,01) và vẽ điểm (t, v) cùng đường thẳng v = v0 + at.",
                        "diem_nhan": "Cho chọn độ chính xác máy đo (0,01 hoặc 0,001 m/s) để thấy Δv/Δt các khoảng sát nhau hơn."}},
    {**BASE,
     "id": "tn-l10-gia-toc-02",
     "ten": "Dấu vết viên bi qua video: đều, nhanh dần, chậm dần",
     "loai": "thi_nghiem", "muc_do": "co_ban",
     "kien_thuc": ["giatoc.chuyen_dong_bien_doi", "giatoc.nhanh_dan_deu", "giatoc.cham_dan_deu"],
     "muc_tieu": "Nhìn khoảng cách giữa các vị trí cách đều thời gian để nhận ra chuyển động đều, nhanh dần, chậm dần.",
     "dung_cu": [{"ten": "Viên bi thép", "so_luong": 1}, {"ten": "Máng nghiêng", "so_luong": 1},
                 {"ten": "Điện thoại quay video (30 hình/s)", "so_luong": 1}, {"ten": "Thước dán dọc đường lăn", "so_luong": 1}],
     "cac_buoc": {"lam": ["Quay video bi lăn trên mặt bàn ngang, lăn xuống máng nghiêng, rồi lăn lên máng nghiêng.",
                          "Dừng hình mỗi 0,2 s (cứ 6 khung hình), lấy 5 vị trí từ t = 0 đến 0,8 s, chấm lên giấy."],
                  "quan_sat": ["Trên bàn: các chấm gần cách đều.", "Xuống dốc: khoảng cách dài dần.", "Lên dốc: khoảng cách ngắn dần."],
                  "rut_ra": ["Khoảng đi được trong mỗi 0,2 s thay đổi thì vận tốc thay đổi: chuyển động biến đổi.",
                             "Dài dần: nhanh dần (a cùng chiều v); ngắn dần: chậm dần (a ngược chiều v)."]},
     "tham_so": [{"ky_hieu": "a", "ten": "Gia tốc dọc đường lăn", "don_vi": "m/s²", "kieu": "dieu_chinh", "min": -2, "max": 2, "mac_dinh": 1, "buoc": 0.1},
                 {"ky_hieu": "v0", "ten": "Vận tốc đầu", "don_vi": "m/s", "kieu": "dieu_chinh", "min": 0, "max": 1, "mac_dinh": 0, "buoc": 0.1},
                 {"ky_hieu": "dt", "ten": "Khoảng thời gian giữa hai chấm", "don_vi": "s", "kieu": "co_dinh", "gia_tri": DT1},
                 {"ky_hieu": "x", "ten": "Vị trí bi", "don_vi": "cm", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["x = v0·t + a·t²/2 (cm = 100·m)", "t = n·0,2 s, n = 0…4"],
                 "gia_thiet": ["bàn ngang coi như đều (bỏ ma sát lăn)", "bi lăn không trượt, coi như chất điểm"]},
     "so_lieu_mau": {"cot": ["Đoạn", "v0 (m/s)", "a (m/s²)", "x0", "x1", "x2", "x3", "x4 (cm)"],
                     "hang": [[nm, v0, a] + pos for (nm, v0, a), pos in zip(ROWS, POS)],
                     "ghi_chu": "Số liệu minh hoạ tính từ mô hình, dùng vẽ Hình 1; cả ba hàng cùng đi 32 cm trong 0,8 s."},
     "ket_qua_ky_vong": "Khoảng cách các chấm: đều (8 cm), tăng dần (2, 6, 10, 14 cm), giảm dần (14, 10, 6, 2 cm).",
     "hien_tuong_hay_sai": ["Tưởng bi lên dốc có gia tốc bằng 0 vì vẫn đang tiến tới.", "Chỉ nhìn vị trí cuối (cùng 32 cm) rồi kết luận ba chuyển động như nhau."],
     "sai_so_thuong_gap": "Video mờ khi bi nhanh; chấm vị trí lệch tâm bi.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc",
                        "y_tuong": "Ba làn song song, bi để lại chấm mỗi 0,2 s; thanh trượt v0, a; hiện mũi tên v (xanh dương) và a (xanh lá).",
                        "diem_nhan": "Đặt a âm với v0 lớn để thấy bi dừng rồi lăn ngược — mở đường cho bài sau."}},
    {**BASE,
     "id": "tn-l10-gia-toc-03",
     "ten": "Ô tô hãm phanh: gia tốc âm và quãng đường từ đồ thị v–t",
     "loai": "vi_du", "muc_do": "trung_binh",
     "kien_thuc": ["giatoc.a_bang_dv_chia_dt", "giatoc.cham_dan_deu", "giatoc.do_thi_v_t_dien_tich"],
     "muc_tieu": "Tính gia tốc hãm phanh, xác định chiều gia tốc, đọc quãng đường hãm phanh là diện tích dưới đồ thị v–t.",
     "dung_cu": [{"ten": "Không cần (ví dụ phân tích, bài toán mẫu)", "so_luong": 0}],
     "cac_buoc": {"lam": ["Ô tô đang chạy 54 km/h thì hãm phanh, dừng sau 5 s; vẽ đồ thị v–t."],
                  "quan_sat": ["Đồ thị là đoạn thẳng đi xuống từ 15 m/s về 0 trong 5 s."],
                  "rut_ra": ["a = (0 − 15)/5 = −3 m/s², ngược chiều chuyển động.", "Quãng đường = diện tích tam giác = 37,5 m."]},
     "tham_so": [{"ky_hieu": "v0", "ten": "Vận tốc lúc bắt đầu hãm", "don_vi": "m/s", "kieu": "dieu_chinh", "min": 5, "max": 30, "mac_dinh": VB, "buoc": 1},
                 {"ky_hieu": "t_dung", "ten": "Thời gian hãm đến khi dừng", "don_vi": "s", "kieu": "dieu_chinh", "min": 2, "max": 10, "mac_dinh": TB, "buoc": 0.5},
                 {"ky_hieu": "a", "ten": "Gia tốc", "don_vi": "m/s²", "kieu": "tinh_ra"},
                 {"ky_hieu": "s", "ten": "Quãng đường hãm phanh", "don_vi": "m", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["a = (0 − v0)/t_dung", "v = v0 + a·t", "s(t) = v0·t + a·t²/2", "s_dung = v0·t_dung/2 (diện tích tam giác)"],
                 "gia_thiet": ["chậm dần đều", "chiều dương là chiều chuyển động"]},
     "so_lieu_mau": {"cot": ["t (s)", "v (m/s)", "s (m)"],
                     "hang": [[t, r2(VB + AB * t), r2(VB * t + 0.5 * AB * t * t)] for t in range(6)],
                     "ghi_chu": "Số liệu tính từ mô hình của bài toán mẫu."},
     "ket_qua_ky_vong": "a = −3 m/s²; s = 37,5 m.",
     "hien_tuong_hay_sai": ["Quên đổi 54 km/h ra 15 m/s.", "Cho rằng a âm luôn là chậm dần (đổi chiều dương thì a = +3 m/s² mà xe vẫn chậm dần).",
                            "Tính quãng đường bằng v0·t = 75 m (quên vận tốc giảm dần)."],
     "goi_y_mo_phong": {"loai": "do_thi+2d_dong_hoc",
                        "y_tuong": "Xe chạy rồi hãm; đồ thị v–t vẽ dần, vùng diện tích tô dần cùng lúc với quãng đường xe đi.",
                        "diem_nhan": "Nút đổi chiều dương: dấu của v và a cùng đảo, kết luận chậm dần không đổi."}},
]
for d in tn:
    (ROOT / "content/thi-nghiem" / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"ok theory.html {len(h)} ký tự · 4 hình · {phut} phút · 3 file thí nghiệm · a_tong = {ATONG:.4f}")
