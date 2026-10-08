"""Sinh 3 hình SVG + bảng thí nghiệm cho bài 'Độ dịch chuyển và quãng đường đi được' (lesson 49),
thay mốc <!--FIGn--> / <!--TABLE1--> trong theory.src.html -> theory.html.
Có lớp kiểm hình học: hộp nhãn không chồng nhau, không vượt viewBox, cỡ chữ >= 13; mũi tên đúng chiều; tỉ lệ độ dài đúng.
Chạy: python3 build_thi_nghiem.py (nếu đổi số liệu) -> python3 build_figs.py -> python3 build_bundle.py"""
import json, math, pathlib, re, subprocess, sys
from svg_lib import RED, BLUE, ORG, GRN, wrap

HERE = pathlib.Path(__file__).resolve().parent
COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN}


def sub(base, s, size=11):
    return f'{base}<tspan baseline-shift="sub" font-size="{size}">{s}</tspan>'


class Canvas:
    def __init__(self, name, w, h):
        self.name, self.w, self.h = name, w, h
        self.body, self.labels, self.markers, self.arrows, self.obst = "", [], set(), {}, []

    def add(self, s):
        self.body += s

    def line(self, x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, obstacle=True):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.body += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
        if obstacle:
            self.obst.append((x1, y1, x2, y2))

    def dot(self, x, y, r=4, c="currentColor"):
        self.body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'

    def arr(self, tag, c, x1, y1, x2, y2, w=3, head=12, dash=""):
        """Mũi tên có ĐỈNH đúng tại (x2,y2); marker cỡ cố định (userSpaceOnUse)."""
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        ex, ey = x2 - ux * head, y2 - uy * head
        self.markers.add((c, head))
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.body += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{COL[c]}" stroke-width="{w}"{d} '
                      f'marker-end="url(#{self.name}-{c}{head})"/>')
        self.arrows[tag] = (x1, y1, x2, y2)
        self.obst.append((x1, y1, x2, y2))

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

    @staticmethod
    def _seg_hits_box(seg, box, pad=1.5):
        x1, y1, x2, y2 = seg
        bx0, by0, bx1, by1 = box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad
        for k in range(41):                       # lấy mẫu dọc đoạn thẳng
            t = k / 40
            x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
            if bx0 < x < bx1 and by0 < y < by1:
                return True
        return False

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
            for s in self.obst:
                if self._seg_hits_box(s, a[1:5]):
                    errs.append(f"{self.name}: nhãn '{a[0]}' bị đường {tuple(round(v) for v in s)} cắt")
        return errs

    def svg(self, label, cap, exp=None):
        s = wrap(f"0 0 {self.w} {self.h}", label, self.defs() + self.body, cap)
        if exp:
            s = s.replace('<figure class="fig" data-tl="1">', f'<figure class="fig" data-tl="1" data-exp="{exp}">', 1)
        return s


ERR = []

# ---------------- Hình 1: một vòng sân băng (mở bài — KHÔNG ghi số liệu, không vẽ d)
c = Canvas("f1", 400, 250)
c.add('<rect x="30" y="30" width="340" height="160" rx="80" fill="rgba(56,189,248,.10)" stroke="currentColor" stroke-width="3"/>')
# đường trượt (cam), lùi vào trong 16 px so với rào
c.add(f'<rect x="46" y="46" width="308" height="128" rx="64" fill="none" stroke="{ORG}" stroke-width="2.6" stroke-dasharray="7 5"/>')
GX, GY = 200, 174                     # cửa vào trên đường trượt ở cạnh dưới
c.arr("duoi", "o", 230, GY, 290, GY, 3.2)        # cạnh dưới: sang phải
c.arr("tren", "o", 230, 46, 170, 46, 3.2)        # cạnh trên: sang trái  -> đi ngược chiều kim đồng hồ trên màn hình
c.add(f'<circle cx="{GX}" cy="{GY}" r="8" fill="none" stroke="currentColor" stroke-width="2.4"/>')
c.dot(GX, GY, 4)
c.line(GX, 190, GX, 200, "currentColor", 2, obstacle=False)
c.text(200, 104, "Sân băng", size=15, anchor="middle")
c.text(200, 130, "đường trượt (nét cam)", ORG, 13, "middle", "600")
c.text(200, 218, "Cửa vào: chỗ xuất phát", size=13, anchor="middle", weight="600")
c.text(200, 238, "và cũng là chỗ dừng", size=13, anchor="middle", weight="600")
# kiểm chiều đi: dưới sang phải, trên sang trái (một vòng ngược chiều kim đồng hồ trên màn hình)
x1, y1, x2, y2 = c.arrows["duoi"]; ERR += [] if x2 > x1 else ["f1: mũi dưới sai chiều"]
x1, y1, x2, y2 = c.arrows["tren"]; ERR += [] if x2 < x1 else ["f1: mũi trên sai chiều"]
fig1 = c.svg("Sân băng hình bầu dục, đường trượt một vòng sát rào, xuất phát và dừng ở cùng cửa vào",
             "Hình 1. Trượt một vòng sát rào chắn: chỗ xuất phát và chỗ dừng là cùng một điểm (cửa vào).",
             exp="tn-l10-dd-qd-03")
ERR += c.check()

# ---------------- Hình 2: xe điều khiển trên trục Ox: 20 -> 80 -> 50 cm
c = Canvas("f2", 420, 215)
AX_Y, X0, K = 130, 40, 3.4             # 1 cm = 3,4 px; x = 0 tại px 40
px = lambda cm: X0 + K * cm
c.line(24, AX_Y, 396, AX_Y, "currentColor", 2.2)
c.add(f'<path d="M408,{AX_Y} L396,{AX_Y-6} L396,{AX_Y+6} Z" fill="currentColor"/>')
for cm in range(0, 101, 10):
    c.line(px(cm), AX_Y - 5, px(cm), AX_Y + 5, "currentColor", 1.6, obstacle=False)
c.text(px(0), 152, "O", size=14, anchor="middle", italic=True)
for cm in (20, 50, 80, 100):
    c.text(px(cm), 152, str(cm), size=13, anchor="middle", weight="600")
c.text(404, 116, "x (cm)", size=14, anchor="end", italic=True)
x1, xq, x2 = 20, 80, 50
YA, YB = 70, 95
c.arr("toi", "o", px(x1), YA, px(xq), YA, 3.2)
c.line(px(xq), YA, px(xq), YB, ORG, 2, "3 3", 1)
c.arr("lui", "o", px(xq), YB, px(x2), YB, 3.2)
c.line(px(x1), YA, px(x1), AX_Y, "currentColor", 1.2, "3 4", .5)
c.text((px(x1) + px(xq)) / 2, YA - 10, "đi tới 60 cm", ORG, 13, "middle", "600")
c.text((px(xq) + px(x2)) / 2 + 30, YB + 18, "lùi 30 cm", ORG, 13, "middle", "600")
for cm in (x1, x2, xq):
    c.dot(px(cm), AX_Y, 4.5)
YD = 180
c.line(px(x1), 160, px(x1), YD, GRN, 1.2, "3 3", .7, obstacle=False)
c.line(px(x2), 160, px(x2), YD, GRN, 1.2, "3 3", .7, obstacle=False)
c.arr("d", "g", px(x1), YD, px(x2), YD, 3.4)
c.text(px(x1) - 8, YD + 5, sub("x", "1"), size=15, anchor="end", italic=True)
c.text(px(x2) + 8, YD + 5, sub("x", "2"), size=15, italic=True)
c.text((px(x1) + px(x2)) / 2, YD + 24, "d = 30 cm", GRN, 14, "middle")
c.text(16, 24, "Xe điều khiển chạy dọc thước, gốc O là đầu thước", size=13, weight="600")
# kiểm: d = x2 - x1 đúng tỉ lệ, cùng chiều trục; tổng hai đoạn cam = s
xa, _, xb, _ = c.arrows["d"]
ERR += [] if abs((xb - xa) / K - (x2 - x1)) < 1e-9 else ["f2: độ dài d sai tỉ lệ"]
ERR += [] if abs((c.arrows["toi"][2] - c.arrows["toi"][0]) / K - 60) < 1e-9 and abs((c.arrows["lui"][0] - c.arrows["lui"][2]) / K - 30) < 1e-9 else ["f2: đoạn cam sai"]
fig2 = c.svg("Trục Ox dọc thước: xe đi từ 20 cm tới 80 cm rồi lùi về 50 cm; mũi tên xanh lá d nối 20 cm tới 50 cm",
             "Hình 2. Đường cam: xe đi tới rồi lùi, tổng $90\\ \\text{cm}$. Mũi tên xanh lá: độ dịch chuyển chỉ nối điểm đầu với điểm cuối.",
             exp="tn-l10-dd-qd-02")
ERR += c.check()

# ---------------- Hình 3: nhà -> ngã tư (1,2 km Đông) -> trường (0,5 km Bắc). KHÔNG ghi độ lớn d (đề hỏi)
c = Canvas("f3", 400, 262)
S = 216.0                      # px / km
HX, HY = 62, 214
NX, NY = HX + 1.2 * S, HY
TX, TY = NX, HY - 0.5 * S
for x, y in ((HX, HY), (NX, NY), (TX, TY)):
    c.dot(x, y, 5)
c.arr("dong", "o", HX, HY, NX, NY, 3.2)
c.arr("bac", "o", NX, NY, TX, TY, 3.2)
c.arr("d", "g", HX, HY, TX, TY, 3.2, dash="8 5")
c.add(f'<path d="M{NX-20:.1f},{NY:.1f} L{NX-20:.1f},{NY-20:.1f} L{NX:.1f},{NY-20:.1f}" fill="none" stroke="currentColor" stroke-width="1.4"/>')
alpha = math.atan2(HY - TY, TX - HX)
R = 46
ax_, ay_ = HX + R * math.cos(alpha), HY - R * math.sin(alpha)
c.add(f'<path d="M{HX+R:.1f},{HY:.1f} A{R},{R} 0 0 0 {ax_:.1f},{ay_:.1f}" fill="none" stroke="{GRN}" stroke-width="2"/>')
c.text(HX + R + 8, HY - 7, "α", GRN, 16, italic=True)
c.text(HX, HY + 26, "Nhà", size=14, anchor="middle")
c.text(NX, HY + 26, "Ngã tư", size=14, anchor="middle")
c.text(TX, TY - 14, "Trường", size=14, anchor="middle")
c.text((HX + NX) / 2, HY + 26, "1,2 km", ORG, 14, "middle")
c.text(NX + 10, (NY + TY) / 2 + 5, "0,5 km", ORG, 14)
c.text(150, 140, "d = ?", GRN, 16, "end", italic=True)
# la bàn
CX, CY = 44, 92
c.arr("N", "b", CX, CY, CX, CY - 46, 2.4, 10)
c.arr("E", "b", CX, CY, CX + 46, CY, 2.4, 10)
c.text(CX, CY - 54, "Bắc", BLUE, 13, "middle", "600")
c.text(CX + 52, CY + 5, "Đông", BLUE, 13, "start", "600")
# kiểm: tỉ lệ 1,2 : 0,5; d nối nhà -> trường; góc ~22,6°
ERR += [] if abs((NX - HX) / (NY - TY) - 1.2 / 0.5) < 1e-9 else ["f3: tỉ lệ hai cạnh sai"]
ERR += [] if abs(math.degrees(alpha) - math.degrees(math.atan(0.5 / 1.2))) < 1e-9 else ["f3: góc sai"]
ERR += [] if abs(math.hypot(TX - HX, HY - TY) / S - 1.3) < 1e-9 else ["f3: d sai"]
fig3 = c.svg("Đường đạp xe: từ nhà đi về phía Đông tới ngã tư, rẽ trái đi về phía Bắc tới trường; mũi tên nét đứt xanh lá nối nhà tới trường là độ dịch chuyển",
             "Hình 3. Đường cam: đường đạp xe thật. Mũi tên nét đứt xanh lá: độ dịch chuyển $\\vec d$ từ nhà tới trường, hợp với hướng Đông góc α.")
ERR += c.check()

if ERR:
    print("\n".join("✗ " + e for e in ERR)); sys.exit(1)

# ---------------- Bảng thí nghiệm 01: đọc từ file JSON (số liệu tính trong build_thi_nghiem.py)
tn = json.loads((HERE.parents[1] / "thi-nghiem" / "tn-l10-dd-qd-01.json").read_text(encoding="utf8"))
vn = lambda v: f"{v:.1f}".replace(".", ",")
rows = "".join(f"<tr><td>{h[0]}</td><td>{vn(h[2])}</td><td>{vn(h[4])}</td></tr>\n" for h in tn["so_lieu_mau"]["hang"])
table1 = ('<div class="table-scroll">\n<table class="tl-table">\n<thead>\n<tr><th>Hình ray</th><th>$s$ đo (cm)</th><th>$d$ đo (cm)</th></tr>\n'
          f'</thead>\n<tbody>\n{rows}</tbody>\n</table>\n</div>')

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, fg in enumerate((fig1, fig2, fig3), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
assert "<!--TABLE1-->" in h
h = h.replace("<!--TABLE1-->", table1)
# số phút: điền từ lint_do_dai (đo trên chính bản đã chèn hình)
tmp = HERE / ".theory.tmp.html"
tmp.write_text(h.replace("__PHUT__", "15"), encoding="utf8")
lint = HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = subprocess.run([sys.executable, str(lint), str(tmp)], capture_output=True, text=True).stdout
tmp.unlink()
m = re.search(r"~?(\d+(?:[.,]\d+)?)\s*phút", out)
phut = round(float(m.group(1).replace(",", "."))) if m else None
if phut is None:
    print("! không đọc được số phút từ lint_do_dai:\n" + out[:600]); sys.exit(1)
h = h.replace("__PHUT__", str(phut))
(HERE / "theory.html").write_text(h, encoding="utf8")
print(f"ok theory.html {len(h)} ký tự · 3 hình · {phut} phút")
