"""Sinh 3 hình SVG + bảng số liệu thí nghiệm cho bài 'Thực hành tính sai số trong phép đo. Ghi kết quả đo' (lesson 48),
thay mốc <!--FIGn-->, __BANG_TN1__, __PHUT__ trong theory.src.html -> theory.html,
và ghi 3 file thí nghiệm content/thi-nghiem/tn-l10-sai-so-0{1,2,3}.json (số liệu tính từ cùng mô hình).
Số liệu bảng sinh từ mô hình T = 2π√(l/g) cộng độ lệch bấm tay cố định; mọi số nêu trong lời văn được assert.
Có lớp kiểm hình học: hộp nhãn không chồng nhau, không vượt viewBox; chấm/vạch đặt theo công thức toạ độ.
Chạy: python3 build_figs.py   (sau đó: python3 build_bundle.py)"""
import json, math, pathlib, re, subprocess, sys
from fractions import Fraction
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

# ================= Mô hình số liệu (dùng chung cho hình, bảng, lời văn và file thí nghiệm)
# TN1: con lắc đơn l = 1,000 m, g = 9,81; t = thời gian 10 dao động = 10·T0 + độ lệch bấm tay (cố định); đồng hồ số 0,01 s.
L_DAY, G_CHUAN = 1.000, 9.81
T0 = 2 * math.pi * math.sqrt(L_DAY / G_CHUAN)
T10 = 10 * T0
NHIEU = [0.13, -0.21, 0.08, -0.12, 0.17]              # s, độ lệch do bấm tay
TC = [round((T10 + e) * 100 + 1e-9) for e in NHIEU]   # centi-giây (số nguyên, tránh sai số float)
assert TC == [2019, 1985, 2014, 1994, 2023], TC
assert sum(TC) % 5 == 0
MEAN_C = sum(TC) // 5                                  # 2007
DEV_C = [abs(MEAN_C - x) for x in TC]                  # [12, 22, 7, 13, 16]
assert MEAN_C == 2007 and DEV_C == [12, 22, 7, 13, 16] and sum(DEV_C) == 70
assert sum(DEV_C) % 5 == 0 and sum(DEV_C) // 5 == 14   # trung bình lệch 0,14 s
DC_C = 1                                               # sai số dụng cụ 0,01 s
DT_C = sum(DEV_C) // 5 + DC_C                          # 15 -> 0,15 s
assert DT_C == 15
assert max(DEV_C) == 22 and DEV_C.index(22) == 1       # "lệch lớn nhất là lần 2" (so số nguyên, không float)
TBAR, DT = MEAN_C / 100, DT_C / 100
dTrel = DT / TBAR * 100                                # %
assert f"{dTrel:.2f}" == "0.75" and f"{dTrel:.3f}" == "0.747", dTrel
LO, HI = TBAR - DT, TBAR + DT
assert (round(LO, 2), round(HI, 2)) == (19.92, 20.22)
OUT = [i + 1 for i, x in enumerate(TC) if not (round(LO * 100) <= x <= round(HI * 100))]
assert OUT == [2, 5], OUT                              # lần 2 và lần 5 nằm ngoài khoảng (caption Hình 2)

# Bài toán mẫu: g = 4π² l / T²; Δl = 0,001 m (một ĐCNN); T = t/10; bỏ qua sai số π
T_BAR = TBAR / 10
G_BAR = 4 * math.pi ** 2 * L_DAY / T_BAR ** 2
assert f"{T_BAR:.3f}" == "2.007" and f"{G_BAR:.2f}" == "9.80", (T_BAR, G_BAR)
dl = 0.001 / L_DAY * 100
assert abs(dl - 0.1) < 1e-9
dg = dl + 2 * dTrel
assert f"{dg:.1f}" == "1.6" and f"{2 * dTrel:.3f}" == "1.495", dg           # lời giải ghi 2·0,747 ≈ 1,6 %
Dg = G_BAR * dg / 100
assert f"{Dg:.2f}" == "0.16" and round(9.80 * 0.016, 2) == 0.16               # ghi Δg = 9,80·0,016 ≈ 0,16
assert round(9.80 - 0.16, 2) == 9.64 and round(9.80 + 0.16, 2) == 9.96 and 9.64 < G_CHUAN < 9.96
# bước điền: Δl = 0,003 m
dg2 = 0.3 + 2 * dTrel
assert f"{dg2:.1f}" == "1.8" and f"{2 * dTrel:.3f}" == "1.495"
assert f"{G_BAR * dg2 / 100:.2f}" == "0.18" and round(9.80 * 0.018, 2) == 0.18
# biến thể 20 dao động (giả định Δt giữ 0,15 s, t̄ = 40,14 s)
dT20 = DT / (2 * TBAR) * 100
assert f"{dT20:.3f}" == "0.374" and f"{0.1 + 2 * dT20:.2f}" == "0.85" and f"{G_BAR * (0.1 + 2 * dT20) / 100:.2f}" == "0.08"
assert 2 * TBAR == 40.14 or abs(2 * TBAR - 40.14) < 1e-9
# TN2: thước thép 1 mm, ΔA = 0,5 mm
D_TAM, D_CHOT, DA = 250.0, 12.0, 0.5
assert f"{DA / D_TAM * 100:.1f}" == "0.2" and f"{DA / D_CHOT * 100:.1f}" == "4.2"
assert abs(0.005 * 12 - 0.06) < 1e-12
# thử thách
assert f"{0.5 / 143.0 * 100:.2f}" == "0.35"
assert abs(0.2 / 20.0 * 100 - 1) < 1e-9 and abs(2 * 1 - 2) < 1e-9 and 20.0 ** 2 == 400 and abs(0.02 * 400 - 8) < 1e-9
dm, da = 5 / 1000 * 100, 0.05 / 5.00 * 100
assert abs(dm - 0.5) < 1e-9 and abs(da - 1) < 1e-9 and abs(dm + 3 * da - 3.5) < 1e-9
assert 1000 / 5.00 ** 3 == 8.0 and abs(8.0 * 0.035 - 0.28) < 1e-9
# quiz và ví dụ lời văn
assert abs(3 * 0.5 - 1.5) < 1e-9 and f"{0.5 / 3:.2f}" == "0.17"
assert f"{12.5 * 16 * 15.88:.0f}" == "3176"            # 3,2·10³ (2 CSCN)
assert f"{1.52723:.3f}" == "1.527" and f"{1.5273:.3f}" == "1.527"
assert f"{0.3 / 1 * 0.2:.2f}" == "0.06"                # quiz 6: 0,3/5 = 0,06 (đáp án sai C)
assert f"{0.3 / 5:.2f}" == "0.06"
LISTEN = lambda t: f"{t:.2f}".replace(".", ",")


def vc(x, nd=2):
    return f"{x:.{nd}f}".replace(".", ",")


# ================= Hình 1: thước 1 mm, đầu chốt ở vạch 12
c = Canvas("f1", 410, 215)
X1 = lambda v: 40 + (v - 9) * 55
c.add(f'<rect x="12" y="28" width="{X1(12) - 12}" height="42" fill="{ORG}" fill-opacity=".35" stroke="currentColor" stroke-width="2"/>')
c.text(26, 55, "chốt", size=14)
c.add('<rect x="14" y="90" width="382" height="62" fill="none" stroke="currentColor" stroke-width="2"/>')
for v in range(9, 16):
    c.line(X1(v), 90, X1(v), 112, "currentColor", 2)
    c.text(X1(v), 140, str(v), size=14, anchor="middle", weight="600")
c.line(X1(12), 70, X1(12), 112, ORG, 2, dash="5 4")
c.line(X1(13), 74, X1(13), 90, BLUE, 2)
c.line(X1(14), 74, X1(14), 90, BLUE, 2)
mid = (X1(13) + X1(14)) / 2
c.arr("l", "b", mid, 82, X1(13) + 2, 82, 3)
c.arr("r", "b", mid, 82, X1(14) - 2, 82, 3)
c.text(mid, 64, "ĐCNN = 1 mm", BLUE, 14, anchor="middle")
b1, b2 = X1(11.5), X1(12.5)
c.line(b1, 172, b2, 172, GRN, 4)
c.line(b1, 164, b1, 180, GRN, 3)
c.line(b2, 164, b2, 180, GRN, 3)
c.text(X1(12), 200, "12,0 ± 0,5 mm", GRN, 14, anchor="middle")
# kiểm toạ độ: vạch cách đều, khoảng ± nửa ĐCNN đối xứng quanh vạch 12, mũi tên a↔b nằm giữa hai vạch 13 và 14
ERR += [] if all(abs((X1(v + 1) - X1(v)) - 55) < 1e-9 for v in range(9, 15)) else ["f1: vạch thước không cách đều"]
ERR += [] if abs((X1(12) - b1) - (b2 - X1(12))) < 1e-9 and abs((b2 - b1) - 55) < 1e-9 else ["f1: khoảng ±0,5 mm lệch tâm"]
ERR += [] if (c.arrows["l"][2] > X1(13) and c.arrows["r"][2] < X1(14)) else ["f1: mũi tên ĐCNN ra ngoài hai vạch"]
fig1 = c.svg("Thước thép vạch chia 1 milimét; đầu chiếc chốt nằm đúng vạch 12; dưới thước là khoảng 12,0 ± 0,5 mm",
             "Hình 1. Thước vạch 1 mm (ĐCNN = 1 mm). Đầu chốt nằm đúng vạch 12: kết quả ghi (12,0 ± 0,5) mm, với sai số dụng cụ bằng nửa ĐCNN.",
             exp="tn-l10-sai-so-02")
ERR += c.check()

# ================= Hình 2: 5 lần đo + khoảng t̄ ± Δt
c = Canvas("f2", 420, 240)
X2 = lambda t: 30 + (t - 19.7) / 0.8 * 360
c.line(24, 200, 396, 200, "currentColor", 2)
for tv in (19.8, 20.0, 20.2, 20.4):
    c.line(X2(tv), 195, X2(tv), 205, "currentColor", 2)
    c.text(X2(tv), 224, vc(tv, 1), size=14, anchor="middle", weight="600")
c.text(398, 190, "t (s)", size=14, anchor="end", weight="600")
c.line(X2(TBAR), 46, X2(TBAR), 200, BLUE, 2, dash="5 4")
c.text(X2(TBAR), 40, "trung bình", BLUE, 14, anchor="middle")
for x in TC:
    c.dot(X2(x / 100), 90, 6, ORG)
c.text(300, 95, "5 lần đo", ORG, 14)
c.line(X2(LO), 140, X2(HI), 140, GRN, 5)
c.line(X2(LO), 130, X2(LO), 150, GRN, 3)
c.line(X2(HI), 130, X2(HI), 150, GRN, 3)
c.text(X2(TBAR) + 10, 124, "20,07 ± 0,15 s", GRN, 14)
c.text(X2(LO), 172, vc(LO), GRN, 14, anchor="middle")
c.text(X2(HI), 172, vc(HI), GRN, 14, anchor="middle")
# kiểm toạ độ: trục tuyến tính, đoạn xanh đối xứng quanh vạch trung bình, hai chấm ngoài đoạn đúng lần 2 và 5
ERR += [] if abs((X2(TBAR) - X2(LO)) - (X2(HI) - X2(TBAR))) < 1e-9 else ["f2: đoạn ± không đối xứng quanh trung bình"]
ERR += [] if abs((X2(20.2) - X2(20.0)) - (X2(20.0) - X2(19.8))) < 1e-9 else ["f2: trục không tuyến tính"]
ngoai = [i + 1 for i, x in enumerate(TC) if not (X2(LO) <= X2(x / 100) <= X2(HI))]
ERR += [] if ngoai == [2, 5] else [f"f2: chấm ngoài đoạn {ngoai} khác lần 2, 5"]
ERR += [] if all(X2(19.7) >= 30 - 1e-9 and 24 <= X2(x / 100) <= 396 for x in TC) else ["f2: chấm ra ngoài trục"]
fig2 = c.svg("Trục thời gian: năm chấm là năm lần đo, vạch xanh dương là giá trị trung bình 20,07 s, đoạn xanh lá từ 19,92 s đến 20,22 s là kết quả 20,07 ± 0,15 s",
             "Hình 2. Năm lần đo thời gian 10 dao động (chấm cam) và kết quả <em>t</em> = (20,07 ± 0,15) s (đoạn xanh lá). Lần 2 (19,85 s) và lần 5 (20,23 s) nằm ngoài đoạn: Δ<em>t</em> là sai số trung bình, không phải sai số lớn nhất. Số liệu minh hoạ.",
             exp="tn-l10-sai-so-01")
ERR += c.check()

# ================= Hình 3: sai số hệ thống (lệch) và sai số ngẫu nhiên (tản)
c = Canvas("f3", 420, 230)
XT = 210
RA = [262, 277, 291, 306, 322]
RB = [150, 185, 205, 240, 268]
mA, mB = sum(RA) / len(RA), sum(RB) / len(RB)
YA, YB = 100, 190
c.line(20, YA, 400, YA, "currentColor", 2, op=.35)
c.line(20, YB, 400, YB, "currentColor", 2, op=.35)
c.line(XT, 46, XT, 206, "currentColor", 2, dash="6 5")
c.text(XT, 34, "giá trị thật", size=14, anchor="middle")
c.text(14, 80, "Hệ thống: lệch một phía", size=14, weight="600")
c.text(14, 170, "Ngẫu nhiên: tản ra", size=14, weight="600")
for x in RA:
    c.dot(x, YA, 6, ORG)
for x in RB:
    c.dot(x, YB, 6, ORG)
c.line(mA, YA - 12, mA, YA + 12, RED, 3)
c.line(mB, YB - 12, mB, YB + 12, RED, 3)
c.arr("gap", "o", XT + 4, 122, mA - 2, 122, 3)
c.text((XT + mA) / 2, 146, "vẫn lệch", ORG, 14, anchor="middle")
# kiểm: hàng A lệch hẳn một phía; hàng B tản hai phía quanh giá trị thật và trung bình sát giá trị thật; mũi tên chỉ về phía trung bình A
ERR += [] if all(x > XT for x in RA) and mA - XT > 40 else ["f3: hàng A phải lệch hẳn một phía"]
ERR += [] if any(x < XT for x in RB) and any(x > XT for x in RB) and abs(mB - XT) < 2 else ["f3: hàng B phải tản hai phía, trung bình sát giá trị thật"]
ERR += [] if c.arrows["gap"][2] > c.arrows["gap"][0] and abs(c.arrows["gap"][2] - mA) < 3 else ["f3: mũi tên 'vẫn lệch' sai chiều"]
fig3 = c.svg("Hai hàng năm lần đo quanh đường nét đứt giá trị thật: hàng trên cả năm chấm nằm lệch về bên phải nên trung bình vẫn lệch; hàng dưới các chấm tản hai bên và trung bình trùng giá trị thật",
             "Hình 3. Năm lần đo (chấm cam) so với giá trị thật (nét đứt; số liệu minh hoạ). Vạch đỏ là trung bình. Hàng trên: sai số hệ thống, trung bình vẫn lệch. Hàng dưới: sai số ngẫu nhiên, trung bình sát giá trị thật.")
ERR += c.check()

if ERR:
    print("\n".join("✗ " + e for e in ERR)); sys.exit(1)

# ================= Bảng số liệu TN1 (chèn vào bài)
rows = [f"<tr><td>{i + 1}</td><td>{vc(x / 100)}</td><td>{vc(d / 100)}</td></tr>" for i, (x, d) in enumerate(zip(TC, DEV_C))]
bang = ('<div class="table-scroll">\n<table class="tl-table">\n<thead>\n'
        '<tr><th>Lần đo</th><th>$t$ (s)</th><th>$\\Delta t_i$ (s)</th></tr>\n</thead>\n<tbody>\n'
        + "\n".join(rows) + "\n</tbody>\n</table>\n</div>")

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, fg in enumerate((fig1, fig2, fig3), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
h = h.replace("__BANG_TN1__", bang)
assert "__" not in h.replace("__PHUT__", "")
# các số nêu trong lời văn phải có đúng trong bản đã dựng
for s in ("$\\overline{t} = 20{,}07\\ \\text{s}$", "0{,}12 + 0{,}22 + 0{,}07 + 0{,}13 + 0{,}16", "$t = (20{,}07 \\pm 0{,}15)\\ \\text{s}$",
          "\\approx 0{,}747\\,\\%", "\\approx 9{,}80\\ \\text{m/s}^2", "(9{,}80 \\pm 0{,}16)", "(9{,}80 \\pm 0{,}18)", "2{,}007"):
    assert s in h, s
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
BASE = {"mon": "vat-ly", "lop": 10, "bai": "Bài 3. Thực hành tính sai số trong phép đo. Ghi kết quả đo", "lesson_id": 48,
        "nguon_trong_bai": "content/lesson-samples/l10-thuc-hanh-sai-so/theory.html"}
tn = [
    {**BASE,
     "id": "tn-l10-sai-so-01",
     "ten": "Đo thời gian 10 dao động của con lắc đơn 5 lần: trung bình, sai số tuyệt đối và tỉ đối",
     "loai": "thi_nghiem", "muc_do": "trung_binh",
     "kien_thuc": ["saiso.trung_binh", "saiso.tuyet_doi_do_truc_tiep", "saiso.ti_doi", "saiso.ngau_nhien"],
     "muc_tieu": "Từ bảng 5 lần đo, tính giá trị trung bình, sai số tuyệt đối từng lần, sai số tuyệt đối của phép đo (cộng sai số dụng cụ), sai số tỉ đối; ghi kết quả đúng dạng t = trung bình ± Δt.",
     "dung_cu": [{"ten": "Con lắc đơn dây dài 1,000 m, vật nặng nhỏ", "so_luong": 1},
                 {"ten": "Đồng hồ bấm giây số (ĐCNN 0,01 s)", "so_luong": 1},
                 {"ten": "Thước dây (đo chiều dài dây)", "so_luong": 1}],
     "cac_buoc": {"lam": ["Treo con lắc đơn dài 1,000 m, kéo lệch khoảng 5° rồi thả nhẹ.",
                          "Bấm đồng hồ đo thời gian t của 10 dao động toàn phần; lặp lại 5 lần."],
                  "quan_sat": ["t lần lượt " + "; ".join(vc(x / 100) for x in TC) + " s.",
                               "Các lần đo tản quanh 20,07 s, lệch trung bình 0,14 s."],
                  "rut_ra": ["Trung bình 20,07 s; sai số tuyệt đối Δt = 0,14 + 0,01 = 0,15 s; sai số tỉ đối ≈ 0,75 %.",
                             "Kết quả ghi: t = (20,07 ± 0,15) s. Sai số ngẫu nhiên (do bấm tay) lấn át sai số dụng cụ."]},
     "tham_so": [{"ky_hieu": "l", "ten": "Chiều dài dây", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.5, "max": 1.5, "mac_dinh": 1.0, "buoc": 0.05},
                 {"ky_hieu": "do_lech_bam_tay", "ten": "Độ lệch bấm tay tối đa", "don_vi": "s", "kieu": "dieu_chinh", "min": 0.0, "max": 0.3, "mac_dinh": 0.25, "buoc": 0.05},
                 {"ky_hieu": "g", "ten": "Gia tốc rơi tự do", "don_vi": "m/s²", "kieu": "co_dinh", "gia_tri": G_CHUAN},
                 {"ky_hieu": "dcnn_dong_ho", "ten": "Độ chia nhỏ nhất đồng hồ", "don_vi": "s", "kieu": "co_dinh", "gia_tri": 0.01},
                 {"ky_hieu": "t", "ten": "Thời gian 10 dao động", "don_vi": "s", "kieu": "do_duoc", "sai_so_do": 0.01},
                 {"ky_hieu": "delta_t", "ten": "Sai số tuyệt đối của phép đo", "don_vi": "s", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["t_i = 10·2π·√(l/g) + e_i, làm tròn tới 0,01 s", "t̄ = (t_1 + … + t_5)/5", "Δt_i = |t̄ − t_i|",
                                  "Δt = trung bình(Δt_i) + Δt_dc, với Δt_dc = 0,01 s", "δt = Δt/t̄ · 100 %"],
                 "gia_thiet": ["e_i là dãy độ lệch cố định (+0,13; −0,21; +0,08; −0,12; +0,17 s) mô phỏng phản xạ bấm tay", "góc lệch nhỏ", "g = 9,81 m/s²"]},
     "so_lieu_mau": {"cot": ["Lần đo", "t (s)", "Δt_i (s)"],
                     "hang": [[i + 1, x / 100, d / 100] for i, (x, d) in enumerate(zip(TC, DEV_C))],
                     "ghi_chu": f"Số liệu minh hoạ tính từ mô hình (T0 = {T0:.4f} s, 10·T0 = {T10:.4f} s) cộng độ lệch bấm tay cố định, làm tròn 0,01 s. t̄ = 20,07 s; trung bình Δt_i = 0,14 s; Δt = 0,15 s; δt ≈ {dTrel:.2f} %."},
     "ket_qua_ky_vong": "t = (20,07 ± 0,15) s; δt ≈ 0,75 %.",
     "hien_tuong_hay_sai": ["Quên cộng sai số dụng cụ (ra 0,14 s thay vì 0,15 s).", "Lấy độ lệch lớn nhất (0,22 s) làm sai số.", "Tưởng đồng hồ chia 0,01 s thì sai số cũng cỡ 0,01 s."],
     "sai_so_thuong_gap": "Phản xạ bấm đồng hồ sớm hoặc muộn; đếm nhầm số dao động; kéo lệch góc lớn.",
     "an_toan": "Buộc chắc vật nặng, tránh vùng đầu người đứng.",
     "goi_y_mo_phong": {"loai": "bang_so_lieu+do_thi",
                        "y_tuong": "Con lắc đơn thả được; mỗi lần bấm sinh một số đo = giá trị thật + nhiễu; bảng tự điền Δt_i và vẽ chấm cùng đoạn t̄ ± Δt trên trục thời gian.",
                        "diem_nhan": "Thanh trượt 'độ lệch bấm tay' và số lần đo: đo nhiều lần thì t̄ ổn định hơn, nhưng đổi sang đồng hồ chia nhỏ hơn thì Δt gần như không đổi."}},
    {**BASE,
     "id": "tn-l10-sai-so-02",
     "ten": "Một thước thép, hai chi tiết CNC: cùng sai số tuyệt đối, khác sai số tỉ đối",
     "loai": "thi_nghiem", "muc_do": "co_ban",
     "kien_thuc": ["saiso.dung_cu_dcnn", "saiso.ti_doi", "saiso.so_sanh_do_chinh_xac"],
     "muc_tieu": "Hiểu sai số dụng cụ bằng nửa ĐCNN và so độ chính xác của hai phép đo bằng sai số tỉ đối, không bằng sai số tuyệt đối.",
     "dung_cu": [{"ten": "Thước thép vạch chia 1 mm", "so_luong": 1}, {"ten": "Tấm nhôm dài khoảng 250 mm", "so_luong": 1},
                 {"ten": "Chốt nhôm đường kính khoảng 12 mm", "so_luong": 1}],
     "cac_buoc": {"lam": ["Đo 1 lần chiều dài tấm nhôm và đường kính chốt bằng thước vạch 1 mm.", "Lấy sai số dụng cụ bằng nửa ĐCNN = 0,5 mm."],
                  "quan_sat": ["Tấm: (250,0 ± 0,5) mm. Chốt: (12,0 ± 0,5) mm.", "Hai phép đo có cùng sai số tuyệt đối 0,5 mm."],
                  "rut_ra": ["Sai số tỉ đối: tấm 0,5/250,0 ≈ 0,2 %; chốt 0,5/12,0 ≈ 4,2 %.", "Phải so δ, không so Δ: phép đo tấm chính xác hơn."]},
     "tham_so": [{"ky_hieu": "d", "ten": "Kích thước vật đo", "don_vi": "mm", "kieu": "dieu_chinh", "min": 5, "max": 300, "mac_dinh": 12, "buoc": 1},
                 {"ky_hieu": "dcnn", "ten": "Độ chia nhỏ nhất của dụng cụ", "don_vi": "mm", "kieu": "dieu_chinh", "min": 0.01, "max": 1, "mac_dinh": 1, "buoc": 0.01},
                 {"ky_hieu": "delta_A", "ten": "Sai số dụng cụ (= nửa ĐCNN)", "don_vi": "mm", "kieu": "tinh_ra"},
                 {"ky_hieu": "delta_ti_doi", "ten": "Sai số tỉ đối", "don_vi": "%", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["ΔA = ĐCNN/2", "δA = ΔA/d · 100 %", "ΔA cần có để δA ≤ 0,5 % : ΔA ≤ 0,005·d"],
                 "gia_thiet": ["đo 1 lần, chỉ có sai số dụng cụ", "đầu vật nằm đúng vạch"]},
     "so_lieu_mau": {"cot": ["Chi tiết", "d (mm)", "ΔA (mm)", "δA (%)"],
                     "hang": [["Tấm nhôm", D_TAM, DA, round(DA / D_TAM * 100, 2)], ["Chốt", D_CHOT, DA, round(DA / D_CHOT * 100, 2)]],
                     "ghi_chu": "Số liệu minh hoạ tính từ mô hình. Chốt cần δ ≤ 0,5 % thì ΔA ≤ 0,06 mm (thước cặp/panme)."},
     "ket_qua_ky_vong": "δ tấm ≈ 0,2 %, δ chốt ≈ 4,2 %: phép đo tấm chính xác hơn dù cùng ΔA = 0,5 mm.",
     "hien_tuong_hay_sai": ["So hai sai số tuyệt đối rồi kết luận hai phép đo như nhau.", "Cho rằng vật nhỏ thì ít sai số."],
     "sai_so_thuong_gap": "Đặt thước không sát đầu vật; nhìn xiên gây sai số thị sai.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu",
                        "y_tuong": "Thước kéo được trên vật đo; thanh trượt kích thước vật và ĐCNN; bảng hiện ΔA và δA, thanh màu δA đổi theo.",
                        "diem_nhan": "Giảm ĐCNN từ 1 mm xuống 0,05 mm để thấy δ của chốt rơi từ 4,2 % xuống dưới 0,5 %."}},
    {**BASE,
     "id": "tn-l10-sai-so-03",
     "ten": "Đo g bằng con lắc đơn: sai số của phép đo gián tiếp",
     "loai": "vi_du", "muc_do": "nang_cao",
     "kien_thuc": ["saiso.gian_tiep_tich_thuong", "saiso.gian_tiep_so_mu", "saiso.ghi_ket_qua"],
     "muc_tieu": "Tính g = 4π²l/T² từ l và T đo trực tiếp; cộng sai số tỉ đối (số mũ 2 nhân với δT); ghi g = trung bình ± Δg đúng chữ số có nghĩa.",
     "dung_cu": [{"ten": "Không cần (bài toán mẫu dùng số liệu của TN1)", "so_luong": 0}],
     "cac_buoc": {"lam": ["Dùng l = 1,000 m (thước ĐCNN 1 mm; đề quy ước lấy Δl = một ĐCNN = 1 mm, không phải nửa ĐCNN) và t = (20,07 ± 0,15) s cho 10 dao động; T = t/10."],
                  "quan_sat": ["T = 2,007 s, δT ≈ 0,747 %; δl = 0,1 %."],
                  "rut_ra": ["δg = δl + 2δT ≈ 1,6 %; g ≈ 9,80 m/s²; Δg ≈ 0,16 m/s².", "Kết quả g = (9,80 ± 0,16) m/s²; giá trị chuẩn 9,81 nằm trong khoảng."]},
     "tham_so": [{"ky_hieu": "dl", "ten": "Sai số tuyệt đối của chiều dài", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.0005, "max": 0.005, "mac_dinh": 0.001, "buoc": 0.0005},
                 {"ky_hieu": "n_dao_dong", "ten": "Số dao động mỗi lần bấm", "don_vi": "", "kieu": "dieu_chinh", "min": 10, "max": 30, "mac_dinh": 10, "buoc": 10},
                 {"ky_hieu": "l", "ten": "Chiều dài dây", "don_vi": "m", "kieu": "co_dinh", "gia_tri": 1.0},
                 {"ky_hieu": "delta_t", "ten": "Sai số tuyệt đối của t (bấm tay)", "don_vi": "s", "kieu": "co_dinh", "gia_tri": 0.15},
                 {"ky_hieu": "g", "ten": "Gia tốc rơi tự do đo được", "don_vi": "m/s²", "kieu": "tinh_ra"},
                 {"ky_hieu": "delta_g", "ten": "Sai số tuyệt đối của g", "don_vi": "m/s²", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["T = t/(số dao động)", "g = 4π²·l/T²", "δg = δl + 2·δT", "Δg = g·δg", "đo 20 dao động: t̄ gấp đôi, Δt giữ nguyên → δT giảm một nửa"],
                 "gia_thiet": ["bỏ qua sai số của π", "Δt cố định 0,15 s (giả định ở biến thể 20 dao động)", "góc lệch nhỏ"]},
     "so_lieu_mau": {"cot": ["Đại lượng", "Giá trị", "Sai số tuyệt đối", "Sai số tỉ đối (%)"],
                     "hang": [["l (m)", 1.0, 0.001, 0.1], ["T (s)", round(T_BAR, 3), round(T_BAR * dTrel / 100, 3), round(dTrel, 3)],
                              ["g (m/s²)", round(G_BAR, 2), round(Dg, 2), round(dg, 1)]],
                     "ghi_chu": "Số liệu tính từ mô hình của bài toán mẫu; g = 9,80 ± 0,16 m/s². Biến thể 20 dao động: δg ≈ 0,85 %, Δg ≈ 0,08 m/s² (giả định)."},
     "ket_qua_ky_vong": "g = (9,80 ± 0,16) m/s²; sai số chủ yếu đến từ T vì số mũ 2.",
     "hien_tuong_hay_sai": ["Quên nhân đôi δT vì T² có số mũ 2.", "Cộng sai số tuyệt đối thay vì sai số tỉ đối khi nhân chia.", "Ghi g = 9,8008 ± 0,16 (nhiều chữ số thập phân hơn Δg)."],
     "sai_so_thuong_gap": "Đo l không tính tới bán kính vật nặng; góc lệch lớn.",
     "goi_y_mo_phong": {"loai": "bang_so_lieu+do_thi",
                        "y_tuong": "Thanh trượt Δl và số dao động; thanh cột chồng thể hiện đóng góp của δl và 2δT vào δg.",
                        "diem_nhan": "Tăng số dao động từ 10 lên 20: cột của 2δT thấp xuống một nửa, thấy rõ đo nhiều dao động trong một lần bấm có lợi."}},
]
for d in tn:
    (ROOT / "content/thi-nghiem" / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"ok theory.html {len(h)} ký tự · 3 hình · {phut} phút · 3 file thí nghiệm · δt = {dTrel:.3f} % · g = {G_BAR:.4f}")
