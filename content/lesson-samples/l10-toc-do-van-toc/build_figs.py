"""Sinh 4 hình SVG + bảng số liệu cho bài 'Tốc độ và vận tốc' (lesson 50), thay mốc <!--FIGn--> / <!--BANG1-->
trong theory.src.html -> theory.html.
Có lớp kiểm: hộp nhãn không chồng nhau, không vượt viewBox, cỡ chữ ≥ 13; độ dài vectơ tỉ lệ độ lớn;
v13 nằm đúng trên đường đi A→C; bảng số liệu tính lại từ mô hình của tn-l10-tdvt-01.json.
Chạy: python3 build_figs.py   (sau đó: python3 build_bundle.py)"""
import json, math, pathlib, re, subprocess, sys
from svg_lib import RED, BLUE, ORG, GRN, wrap

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN}


def sub(base, s, size=12):
    return f'{base}<tspan baseline-shift="sub" font-size="{size}">{s}</tspan>'


def vlab(s):
    return sub("v", s)


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
                errs.append(f"{self.name}: nhãn '{a[0]}' vượt viewBox {tuple(round(v) for v in a[1:5])}")
            for b in self.labels[i + 1:]:
                if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    errs.append(f"{self.name}: nhãn '{a[0]}' chồng '{b[0]}'")
        return errs

    def label_hits_arrow(self, tags, pad=2):
        """Nhãn không được bị mũi tên (đoạn thẳng) cắt xuyên."""
        errs = []
        for tag in tags:
            x1, y1, x2, y2 = self.arrows[tag]
            for lab in self.labels:
                X0, Y0, X1, Y1 = lab[1] - pad, lab[2] - pad, lab[3] + pad, lab[4] + pad
                for k in range(41):
                    px, py = x1 + (x2 - x1) * k / 40, y1 + (y2 - y1) * k / 40
                    if X0 < px < X1 and Y0 < py < Y1:
                        errs.append(f"{self.name}: mũi tên {tag} cắt nhãn '{lab[0]}'")
                        break
        return errs

    def svg(self, label, cap, exp=None):
        s = wrap(f"0 0 {self.w} {self.h}", label, self.defs() + self.body, cap)
        if exp:
            s = s.replace('<figure class="fig" data-tl="1">', f'<figure class="fig" data-tl="1" data-exp="{exp}">', 1)
        return s


ERR = []

# ---------------- Hình 1: đường đua trượt băng nhìn từ trên xuống (mở bài, KHÔNG ghi đáp án)
c = Canvas("f1", 400, 262)
CXL, CXR, CY, RC = 130, 270, 130, 70        # đường tâm làn trượt: hai đoạn thẳng + hai nửa tròn bán kính 70


def stadium(r):
    return (f"M{CXL},{CY - r} L{CXR},{CY - r} A{r},{r} 0 0 1 {CXR},{CY + r} "
            f"L{CXL},{CY + r} A{r},{r} 0 0 1 {CXL},{CY - r} Z")


c.add(f'<path d="{stadium(RC)}" fill="none" stroke="rgba(56,189,248,.18)" stroke-width="30"/>')
c.add(f'<path d="{stadium(RC + 15)}" fill="none" stroke="currentColor" stroke-width="2"/>')
c.add(f'<path d="{stadium(RC - 15)}" fill="none" stroke="currentColor" stroke-width="1.5" opacity=".6"/>')
SX = 200
c.line(SX, CY + RC - 15, SX, CY + RC + 15, RED, 3.5)                  # vạch xuất phát = về đích
c.text(SX, CY + RC + 40, "vạch xuất phát / về đích", RED, 13, "middle", "600")
c.add(f'<circle cx="{SX + 14}" cy="{CY + RC}" r="6" fill="{ORG}" stroke="currentColor" stroke-width="1.5"/>')
c.text(SX + 14, CY + RC - 24, "VĐV", ORG, 13, "middle")
# chiều trượt: ngược chiều kim đồng hồ khi nhìn từ trên (đáy đi sang phải, đỉnh đi sang trái)
c.arr("d1", "g", 236, CY + RC, 290, CY + RC, 2.6, 10)
c.arr("d2", "g", 230, CY - RC, 170, CY - RC, 2.6, 10)
c.text(200, CY - RC - 22, "chiều trượt", GRN, 13, "middle", "600")
c.text(200, CY + 5, "1 vòng ≈ 111 m", size=14, anchor="middle")
x1, y1, x2, y2 = c.arrows["d1"]; ERR += [] if x2 > x1 else ["f1: chiều trượt ở đáy phải sang phải"]
x1, y1, x2, y2 = c.arrows["d2"]; ERR += [] if x2 < x1 else ["f1: chiều trượt ở đỉnh phải sang trái"]
fig1 = c.svg("Đường đua trượt băng hình bầu dục nhìn từ trên xuống, vạch xuất phát trùng vạch về đích, vận động viên trượt một vòng ngược chiều kim đồng hồ",
             "Hình 1. Đường đua trượt băng cự li ngắn nhìn từ trên xuống: xuất phát và về đích ở cùng một vạch (hình không theo tỉ lệ).")
ERR += c.check()

# ---------------- Hình 2: xe đồ chơi đi nửa vòng tròn — quãng đường (cam) và độ dịch chuyển (đỏ)
c = Canvas("f2", 400, 262)
OX, OY, R = 200, 178, 120                    # R = 120 px ứng với 20 cm
AX, BX = OX - R, OX + R
end_ang = math.radians(6)                    # cung dừng trước B một chút để đỉnh marker rơi đúng quanh B
ex, ey = OX + R * math.cos(end_ang), OY - R * math.sin(end_ang)
c.markers.add(("o", 12))
c.add(f'<path d="M{AX},{OY} A{R},{R} 0 0 1 {ex:.1f},{ey:.1f}" fill="none" stroke="{ORG}" stroke-width="3.2" '
      f'marker-end="url(#f2-o12)"/>')
# kiểm: đỉnh marker (dài 12 theo tiếp tuyến chiều kim đồng hồ trên màn hình) gần B
tx, ty = math.sin(end_ang), math.cos(end_ang)           # tiếp tuyến chiều xe chạy tại điểm cuối (đi xuống)
tipx, tipy = ex + 12 * tx, ey + 12 * ty
if math.hypot(tipx - BX, tipy - OY) > 6:
    ERR.append(f"f2: đầu mũi cung lệch B {math.hypot(tipx - BX, tipy - OY):.1f}px")
c.arr("d", "r", AX, OY, BX, OY, 3.2, 12)
c.dot(OX, OY, 3.5)
c.text(OX, OY + 22, "O", size=14, anchor="middle", italic=True)
c.line(OX, OY, OX, OY - R, "currentColor", 1.4, "4 4", .6)
c.text(OX + 7, OY - R / 2 + 5, "R", size=15, italic=True)
c.dot(AX, OY, 4); c.dot(BX, OY, 4)
c.text(AX - 8, OY + 5, "A", size=15, anchor="end", italic=True)
c.text(BX + 8, OY + 5, "B", size=15, italic=True)
MA = math.radians(135)
MX, MY = OX + R * math.cos(MA), OY - R * math.sin(MA)
c.dot(MX, MY, 4.5)
c.text(MX - 10, MY - 8, "M", size=15, anchor="end", italic=True)
c.text(OX, OY - R - 14, "quãng đường s = πR", ORG, 13, "middle", "600")
c.text(OX, OY + 50, "độ dịch chuyển d = AB = 2R", RED, 13, "middle", "600")
fig2 = c.svg("Nửa đường tròn tâm O bán kính R từ A tới B: cung màu cam là quãng đường, mũi tên đỏ từ A tới B là độ dịch chuyển, điểm M trên cung",
             "Hình 2. Xe đi nửa vòng tròn từ <em>A</em> tới <em>B</em>: quãng đường là cung cam ($s = \\pi R$), độ dịch chuyển là mũi tên đỏ thẳng ($d = 2R$).",
             exp="tn-l10-tdvt-02")
ERR += c.check()
ERR += c.label_hits_arrow(["d"])

# ---------------- Hình 3: ba trường hợp cộng vận tốc (độ dài tỉ lệ độ lớn, K px/đơn vị)
c = Canvas("f3", 420, 214)
K = 20
Y0 = 64
# (a) cùng chiều: v12 = 3, v23 = 2 -> v13 = 5
xa = 20
c.arr("a12", "b", xa, Y0, xa + 3 * K, Y0, 3, 10)
c.arr("a23", "o", xa + 3 * K, Y0, xa + 5 * K, Y0, 3, 10)
c.arr("a13", "g", xa, Y0 + 30, xa + 5 * K, Y0 + 30, 3, 10)
c.text(xa + 12, Y0 - 12, vlab("12"), BLUE, 16, italic=True)
c.text(xa + 3 * K + 6, Y0 - 12, vlab("23"), ORG, 16, italic=True)
c.text(xa + 40, Y0 + 52, vlab("13"), GRN, 16, italic=True)
c.text(70, 140, "5 = 3 + 2", size=13, anchor="middle", weight="600")
c.text(70, 200, "(a) cùng chiều", size=13, anchor="middle", weight="600")
# (b) ngược chiều: v12 = 3 sang phải, v23 = 2 sang trái -> v13 = 1 sang phải
xb = 150
c.arr("b12", "b", xb, Y0, xb + 3 * K, Y0, 3, 10)
c.arr("b23", "o", xb + 3 * K, Y0 + 12, xb + 1 * K, Y0 + 12, 3, 10)
c.arr("b13", "g", xb, Y0 + 40, xb + 1 * K, Y0 + 40, 3, 10)
c.line(xb + 3 * K, Y0, xb + 3 * K, Y0 + 12, "currentColor", 1, "2 2", .5)
c.text(xb + 12, Y0 - 12, vlab("12"), BLUE, 16, italic=True)
c.text(xb + 3 * K + 8, Y0 + 18, vlab("23"), ORG, 16, italic=True)
c.text(xb + 1 * K + 8, Y0 + 46, vlab("13"), GRN, 16, italic=True)
c.text(200, 140, "1 = 3 − 2", size=13, anchor="middle", weight="600")
c.text(200, 200, "(b) ngược chiều", size=13, anchor="middle", weight="600")
# (c) vuông góc: v12 = 4 lên, v23 = 3 sang phải -> v13 = 5
xc, yc = 296, 172
c.arr("c12", "b", xc, yc, xc, yc - 4 * K, 3, 10)
c.arr("c23", "o", xc, yc - 4 * K, xc + 3 * K, yc - 4 * K, 3, 10)
c.arr("c13", "g", xc, yc, xc + 3 * K, yc - 4 * K, 3, 10)
c.text(xc - 8, yc - 30, vlab("12"), BLUE, 16, anchor="end", italic=True)
c.text(xc + 18, yc - 4 * K - 10, vlab("23"), ORG, 16, italic=True)
c.text(xc + 38, yc - 26, vlab("13"), GRN, 16, italic=True)
c.text(340, 40, "5² = 4² + 3²", size=13, anchor="middle", weight="600")
c.text(340, 200, "(c) vuông góc", size=13, anchor="middle", weight="600")
# kiểm tỉ lệ + tổng vectơ
def vec(tag):
    x1, y1, x2, y2 = c.arrows[tag]; return x2 - x1, y2 - y1
for p, want in (("a", 5), ("b", 1), ("c", 5)):
    s12, s23, s13 = vec(p + "12"), vec(p + "23"), vec(p + "13")
    if abs(s12[0] + s23[0] - s13[0]) > .01 or abs(s12[1] + s23[1] - s13[1]) > .01:
        ERR.append(f"f3({p}): v13 ≠ v12 + v23")
    if abs(math.hypot(*s13) / K - want) > .01:
        ERR.append(f"f3({p}): |v13| = {math.hypot(*s13)/K} ≠ {want}")
fig3 = c.svg("Ba trường hợp cộng vận tốc: cùng chiều độ lớn cộng, ngược chiều độ lớn trừ, vuông góc dùng định lí Pythagore",
             "Hình 3. Cộng vận tốc: xanh dương $\\vec v_{12}$ (tương đối), cam $\\vec v_{23}$ (kéo theo), xanh lá $\\vec v_{13}$ (tuyệt đối). Độ dài mũi tên tỉ lệ độ lớn.")
ERR += c.check()
ERR += c.label_hits_arrow(["a12", "a23", "a13", "b12", "b23", "b13", "c12", "c23", "c13"])

# ---------------- Hình 4: ca nô qua sông (bài toán mẫu: v12 = 4, v23 = 3, rộng 120 m, trôi 90 m)
c = Canvas("f4", 400, 300)
TOPB, BOTB = 64, 244                  # bờ bên kia / bờ xuất phát; 180 px = 120 m -> 1,5 px/m
PXM = (BOTB - TOPB) / 120
AX, AY = 110, BOTB
BXp, BYp = AX, TOPB
CXp = AX + 90 * PXM
c.add(f'<rect x="10" y="{TOPB}" width="380" height="{BOTB-TOPB}" fill="rgba(56,189,248,.10)"/>')
c.line(10, TOPB, 390, TOPB, "currentColor", 2.4)
c.line(10, BOTB, 390, BOTB, "currentColor", 2.4)
c.line(AX, AY, BXp, BYp, "currentColor", 1.3, "3 5", .55)          # dóng thẳng sang điểm đối diện B
c.line(AX, AY, CXp, TOPB, GRN, 1.6, "6 5", .8)                     # đường đi thật A -> C
# dòng nước (cam, mảnh)
for yy in (104, 206):
    c.arr(f"w{yy}", "o", 290, yy, 350, yy, 1.8, 9)
c.text(320, 126, "dòng nước", ORG, 13, "middle", "600")
# ca nô
c.add(f'<ellipse cx="{AX}" cy="{AY - 8}" rx="7" ry="15" fill="rgba(148,163,184,.45)" stroke="currentColor" stroke-width="1.6"/>')
VK = 16                                # px / (m/s)
c.arr("v12", "b", AX, AY, AX, AY - 4 * VK, 3, 11)
c.arr("v23", "o", AX, AY - 4 * VK, AX + 3 * VK, AY - 4 * VK, 3, 11)
c.arr("v13", "g", AX, AY, AX + 3 * VK, AY - 4 * VK, 3, 11)
c.text(AX - 10, AY - 30, vlab("12"), BLUE, 16, anchor="end", italic=True)
c.text(AX + 8, AY - 4 * VK - 10, vlab("23"), ORG, 16, italic=True)
c.text(AX + 3 * VK + 4, AY - 24, vlab("13"), GRN, 16, italic=True)
c.text(AX, AY + 22, "A", size=15, anchor="middle", italic=True)
c.text(BXp, TOPB - 10, "B", size=15, anchor="middle", italic=True)
c.text(CXp, TOPB - 10, "C", size=15, anchor="middle", italic=True)
c.text((BXp + CXp) / 2, TOPB - 10, "BC = ?", size=13, anchor="middle", weight="600")
c.line(66, TOPB + 2, 66, BOTB - 2, "currentColor", 1.4)
for yy in (TOPB + 2, BOTB - 2):
    c.line(60, yy, 72, yy, "currentColor", 1.4)
c.text(58, 160, "120 m", size=13, anchor="end", weight="600")
c.text(20, 290, "bờ xuất phát", size=13, weight="600")
c.text(20, 30, "bờ bên kia", size=13, weight="600")
c.dot(BXp, TOPB, 3.5); c.dot(CXp, TOPB, 3.5)
# kiểm: v13 = v12 + v23; v13 cùng phương với đường đi A->C; |v13| = 5
x1, y1, x2, y2 = c.arrows["v13"]
if abs((x2 - x1) * (TOPB - AY) - (y2 - y1) * (CXp - AX)) > 1e-6:
    ERR.append("f4: v13 không cùng phương AC")
if abs(math.hypot(x2 - x1, y2 - y1) / VK - 5) > 1e-9:
    ERR.append("f4: |v13| ≠ 5")
fig4 = c.svg("Ca nô xuất phát ở A, mũi hướng vuông góc bờ; vận tốc so với nước hướng sang bờ bên kia, nước chảy dọc bờ, vận tốc so với bờ hướng xiên theo đường A tới C; B là điểm đối diện A",
             "Hình 4. Ca nô sang sông: $\\vec v_{12}$ (so với nước) vuông góc bờ, $\\vec v_{23}$ (nước so với bờ) dọc bờ, $\\vec v_{13}$ (so với bờ) xiên theo đường đi thật $AC$.")
ERR += c.check()
ERR += c.label_hits_arrow(["v12", "v23", "v13"])

# ---------------- Bảng 1: số liệu đo tốc độ đi bộ — lấy từ file thí nghiệm, tính lại v = s/t
tn = json.loads((ROOT / "content/thi-nghiem/tn-l10-tdvt-01.json").read_text(encoding="utf8"))
S = 10.0
rows = tn["so_lieu_mau"]["hang"]
for lan, t, v in rows:
    if abs(round(S / t, 2) - v) > 1e-9:
        ERR.append(f"bảng: lần {lan}: v = {v} nhưng s/t = {S/t:.4f}")
    if abs(t - 8.0) > 0.3 + 1e-9:
        ERR.append(f"bảng: lần {lan}: nhiễu vượt 0,3 s")
tmean = sum(r[1] for r in rows) / len(rows)
vmean = sum(r[2] for r in rows) / len(rows)
if abs(tmean - 8.0) > 1e-9 or abs(round(vmean, 2) - 1.25) > 1e-9:
    ERR.append(f"bảng: trung bình t={tmean}, v={vmean} không khớp lời bài (8,0 s; 1,25 m/s)")
dmax = max(abs(r[1] - tmean) for r in rows)
worst = {r[0] for r in rows if abs(abs(r[1] - tmean) - dmax) < 1e-6}
if worst != {2, 4}:
    ERR.append(f"bảng: các lần lệch nhiều nhất là {sorted(worst)}, lời bài nói lần 2 và lần 4")


def vn(x, nd):
    return f"{x:.{nd}f}".replace(".", "{,}")


bang = "\n".join(f"<tr><td>{lan}</td><td>${vn(t, 1)}$</td><td>${vn(v, 2)}$</td></tr>" for lan, t, v in rows)
bang += f"\n<tr><td>Trung bình</td><td>${vn(tmean, 1)}$</td><td>${vn(vmean, 2)}$</td></tr>"

if ERR:
    print("\n".join("✗ " + e for e in ERR)); sys.exit(1)

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, fg in enumerate((fig1, fig2, fig3, fig4), 1):
    assert h.count(f"<!--FIG{n}-->") == 1, n
    h = h.replace(f"<!--FIG{n}-->", fg)
assert h.count("<!--BANG1-->") == 1
h = h.replace("<!--BANG1-->", bang)
# kiểm thứ tự hình theo xuất hiện
pos = [h.find(f"Hình {n}.") for n in range(1, 5)]
if pos != sorted(pos) or -1 in pos:
    print("✗ thứ tự Hình 1..4 không theo xuất hiện", pos); sys.exit(1)
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
print(f"ok theory.html {len(h)} ký tự · 4 hình · {phut} phút")
