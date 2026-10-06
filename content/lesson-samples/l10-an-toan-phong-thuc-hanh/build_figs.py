"""Sinh 4 hình SVG + bảng số liệu cho bài 'Các quy tắc an toàn trong phòng thực hành Vật lí' (lesson 47),
thay mốc <!--FIGn-->, __BANG_TN1__, __TILE__, __NHIET__, __PHUT__ trong theory.src.html -> theory.html,
và ghi 3 file thí nghiệm content/thi-nghiem/tn-l10-an-toan-0{1,2,3}.json (số liệu tính từ cùng mô hình).
Có lớp kiểm hình học: hộp nhãn không chồng nhau, không vượt viewBox.
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
YEL = "#facc15"
INK = "#111827"

# ================= Mô hình số liệu (dùng chung cho hình, bảng, lời văn và file thí nghiệm)
# TN1: núm bộ nguồn ở vạch; số chỉ vôn kế = 1,03 × vạch, làm tròn tới 0,1 V.
VACH = [3, 6, 9, 12]
VDO = [round(1.03 * v + 1e-9, 1) for v in VACH]
assert VDO == [3.1, 6.2, 9.3, 12.4], VDO
LECH = [round(d - v, 1) for d, v in zip(VDO, VACH)]
assert LECH == [0.1, 0.2, 0.3, 0.4], LECH
TILE = [100 * l / v for l, v in zip(LECH, VACH)]
assert all(abs(t - 3.3) < 0.1 for t in TILE), TILE          # "khoảng 3 %"
assert VDO[3] / 6 > 2                                       # "hơn gấp đôi định mức" bóng 6 V
# TN2: nhiệt độ cạnh ngọn đèn cồn theo khoảng cách d (cm): T = 25 + 400/d², làm tròn 1 °C.
DK = [2, 5, 10, 20]
TN = [round(25 + 400 / d ** 2) for d in DK]
assert TN == [125, 41, 29, 26], TN
assert (TN[1] - 25, TN[2] - 25) == (16, 4)                  # "gấp đôi khoảng cách thì còn 1/4 (16 → 4 °C)"
assert (TN[2] - 25) * 4 == TN[1] - 25

# ================= Hình 1: bàn thực hành, dây cuối cùng chưa nối (không lộ đáp án)
c = Canvas("f1", 420, 230)
GY = 190
c.line(10, GY, 410, GY, "currentColor", 2.5)
c.add(f'<rect x="20" y="100" width="110" height="90" rx="6" fill="none" stroke="currentColor" stroke-width="2.5"/>')
c.add(f'<circle cx="42" cy="124" r="7" fill="{RED}" stroke="currentColor" stroke-width="1.2"/>')
c.add('<rect x="72" y="116" width="34" height="16" rx="3" fill="none" stroke="currentColor" stroke-width="2"/>')
c.add(f'<rect x="90" y="119" width="13" height="10" rx="2" fill="{GRN}"/>')
c.text(26, 92, "Nguồn đang bật", size=14)
c.add(f'<circle cx="130" cy="148" r="6" fill="{RED}"/><circle cx="130" cy="172" r="6" fill="{BLUE}"/>')
# bóng đèn
c.add('<circle cx="340" cy="140" r="26" fill="none" stroke="currentColor" stroke-width="2.5"/>')
c.add(f'<path d="M328,150 Q334,128 340,140 Q346,152 352,130" fill="none" stroke="{ORG}" stroke-width="2.5"/>')
c.add('<rect x="328" y="166" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2.5"/>')
c.text(340, 214, "bóng đèn", size=14, anchor="middle")
# dây + (nối bóng), dây − (đầu tự do)
c.add(f'<polyline points="130,148 200,148 200,140 314,140" fill="none" stroke="{RED}" stroke-width="3"/>')
c.add(f'<polyline points="130,172 232,172 262,152" fill="none" stroke="{BLUE}" stroke-width="3"/>')
c.dot(262, 152, 5, BLUE)
c.line(262, 70, 262, 146, "currentColor", 1.5, "4 4")
c.text(176, 62, "đầu dây chưa nối", size=14)
fig1 = c.svg("Bàn thực hành: bộ nguồn đang bật có đèn báo sáng, cực dương đã nối với bóng đèn, dây từ cực âm còn một đầu tự do chưa nối vào bóng đèn.",
             "Hình 1. Bàn thực hành lúc còn một đầu dây chưa nối: bộ nguồn đã bật, bóng đèn đã nối một đầu.")
ERR += c.check()

# ================= Hình 2: nhãn bộ nguồn (Input, Output, DC/AC, cực +/−, núm vạch)
c = Canvas("f2", 420, 250)
c.add('<rect x="10" y="10" width="400" height="230" rx="10" fill="none" stroke="currentColor" stroke-width="2.5"/>')
c.line(215, 24, 215, 226, "currentColor", 1.5, op=.5)
c.text(28, 44, "INPUT", size=16)
c.text(28, 72, "220 V ~", size=16)
c.text(28, 98, "AC xoay chiều", size=14, weight="600")
c.text(232, 44, "OUTPUT", size=16)
c.text(232, 72, "3 – 12 V", size=16)
c.line(330, 60, 364, 60, "currentColor", 3)
c.line(330, 68, 364, 68, "currentColor", 3, "6 4")
c.text(232, 98, "DC một chiều", size=14, weight="600")
KC = (285, 172)
c.add(f'<circle cx="{KC[0]}" cy="{KC[1]}" r="24" fill="none" stroke="currentColor" stroke-width="2.5"/>')
c.line(KC[0], KC[1], KC[0] - 17, KC[1], ORG, 4)
c.dot(KC[0], KC[1], 3.5)
for ang, lab in ((180, "3"), (120, "6"), (60, "9"), (0, "12")):
    x = KC[0] + 42 * math.cos(math.radians(ang)); y = KC[1] - 42 * math.sin(math.radians(ang))
    c.text(x, y + 5, lab, size=14, anchor="middle")
c.text(KC[0], 226, "núm chọn vạch", size=14, anchor="middle", weight="600")
c.add(f'<circle cx="372" cy="128" r="13" fill="{RED}" stroke="currentColor" stroke-width="1.5"/>')
c.add(f'<circle cx="372" cy="186" r="13" fill="{BLUE}" stroke="currentColor" stroke-width="1.5"/>')
c.add('<text x="372" y="135" fill="#1f2937" font-size="20" font-weight="700" text-anchor="middle">+</text>')
c.add('<text x="372" y="193" fill="#1f2937" font-size="20" font-weight="700" text-anchor="middle">−</text>')
c.text(372, 163, "đỏ", size=14, anchor="middle", weight="600")
c.text(372, 216, "xanh", size=14, anchor="middle", weight="600")
fig2 = c.svg("Mặt nhãn bộ nguồn: bên trái Input 220 V xoay chiều; bên phải Output 3 đến 12 V một chiều, núm chọn các vạch 3, 6, 9, 12 V, cực dương màu đỏ, cực âm màu xanh.",
             "Hình 2. Nhãn bộ nguồn: Input nhận điện từ ổ cắm; Output cấp điện một chiều cho mạch, chọn vạch bằng núm.")
ERR += c.check()

# ================= Hình 3: tám kí hiệu cảnh báo vẽ lại bằng SVG
c = Canvas("f3", 420, 280)
CXS = [52, 157, 262, 367]
CYS = [48, 168]


def tri(cx, cy):
    return (f'<polygon points="{cx},{cy-34} {cx+38},{cy+30} {cx-38},{cy+30}" fill="{YEL}" stroke="currentColor" '
            f'stroke-width="3" stroke-linejoin="round"/>')


def flame(cx, cy, s=1.0, col=ORG):
    def P(x, y):
        return f"{cx+x*s:.1f},{cy+y*s:.1f}"
    d = (f"M{P(0,-18)} C{P(4,-8)} {P(14,-2)} {P(12,10)} C{P(10,20)} {P(-10,20)} {P(-12,10)} "
         f"C{P(-14,2)} {P(-6,-2)} {P(-6,-8)} C{P(-2,-6)} {P(-1,-12)} {P(0,-18)} Z")
    return f'<path d="{d}" fill="{col}" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>'


def sector(cx, cy, r, a1, a2):
    p = lambda a: (cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a)))
    (x1, y1), (x2, y2) = p(a1), p(a2)
    return f'<path d="M{cx},{cy} L{x1:.1f},{y1:.1f} A{r},{r} 0 0 0 {x2:.1f},{y2:.1f} Z" fill="currentColor"/>'


ICONS = []
# 1 điện
cx, cy = CXS[0], CYS[0]
ICONS.append(tri(cx, cy) + f'<polyline points="{cx+5},{cy-14} {cx-7},{cy+4} {cx+1},{cy+4} {cx-5},{cy+22}" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round"/>')
# 2 nhiệt
cx, cy = CXS[1], CYS[0]
waves = "".join(f'<path d="M{cx+dx},{cy+22} q5,-6 0,-12 t0,-12" fill="none" stroke="{RED}" stroke-width="3" stroke-linecap="round"/>' for dx in (-12, 0, 12))
ICONS.append(tri(cx, cy) + waves)
# 3 dễ cháy
cx, cy = CXS[2], CYS[0]
ICONS.append(tri(cx, cy) + flame(cx, cy + 6, 0.95))
# 4 phóng xạ
cx, cy = CXS[3], CYS[0]
ICONS.append(tri(cx, cy) + sector(cx, cy + 8, 19, 90 - 30 + 0, 90 + 30) + sector(cx, cy + 8, 19, 210 - 30, 210 + 30) + sector(cx, cy + 8, 19, 330 - 30, 330 + 30)
             + f'<circle cx="{cx}" cy="{cy+8}" r="4.5" fill="{YEL}" stroke="currentColor" stroke-width="1.5"/>')
# 5 laser
cx, cy = CXS[0], CYS[1]
ICONS.append(tri(cx, cy) + f'<circle cx="{cx-18}" cy="{cy+12}" r="5" fill="currentColor"/>'
             + f'<line x1="{cx-14}" y1="{cy+12}" x2="{cx+24}" y2="{cy+12}" stroke="{RED}" stroke-width="3"/>'
             + f'<line x1="{cx-14}" y1="{cy+12}" x2="{cx+24}" y2="{cy+3}" stroke="{RED}" stroke-width="2.5"/>'
             + f'<line x1="{cx-14}" y1="{cy+12}" x2="{cx+24}" y2="{cy+21}" stroke="{RED}" stroke-width="2.5"/>')
# 6 từ trường
cx, cy = CXS[1], CYS[1]
ICONS.append(tri(cx, cy)
             + f'<path d="M{cx-10},{cy+2} V{cy+8} A10,10 0 0 0 {cx+10},{cy+8} V{cy+2}" fill="none" stroke="currentColor" stroke-width="7"/>'
             + f'<line x1="{cx-10}" y1="{cy-6}" x2="{cx-10}" y2="{cy+2}" stroke="{RED}" stroke-width="7"/>'
             + f'<line x1="{cx+10}" y1="{cy-6}" x2="{cx+10}" y2="{cy+2}" stroke="{BLUE}" stroke-width="7"/>')
# 7 cấm lửa
cx, cy = CXS[2], CYS[1]
ICONS.append(f'<circle cx="{cx}" cy="{cy}" r="34" fill="none" stroke="#ef4444" stroke-width="5"/>' + flame(cx, cy + 2, 0.95)
             + f'<line x1="{cx-24}" y1="{cy-24}" x2="{cx+24}" y2="{cy+24}" stroke="#ef4444" stroke-width="5"/>')
# 8 đeo mặt nạ
cx, cy = CXS[3], CYS[1]
ICONS.append(f'<circle cx="{cx}" cy="{cy}" r="34" fill="#2563eb"/>'
             + f'<line x1="{cx-18}" y1="{cy+2}" x2="{cx-29}" y2="{cy-8}" stroke="#fff" stroke-width="3"/>'
             + f'<line x1="{cx+18}" y1="{cy+2}" x2="{cx+29}" y2="{cy-8}" stroke="#fff" stroke-width="3"/>'
             + f'<path d="M{cx-19},{cy-6} Q{cx},{cy-14} {cx+19},{cy-6} Q{cx+21},{cy+14} {cx},{cy+22} Q{cx-21},{cy+14} {cx-19},{cy-6} Z" fill="#fff"/>'
             + f'<circle cx="{cx-9}" cy="{cy+9}" r="6" fill="#2563eb" stroke="#fff" stroke-width="2"/>'
             + f'<circle cx="{cx+9}" cy="{cy+9}" r="6" fill="#2563eb" stroke="#fff" stroke-width="2"/>')
ICONS = [x.replace("currentColor", INK) for x in ICONS[:6]] + ICONS[6:]
c.add("".join(ICONS))
LABS = [("Nguy hiểm", "về điện"), ("Nhiệt độ", "cao"), ("Chất dễ", "cháy"), ("Chất", "phóng xạ"),
        ("Tia", "laser"), ("Từ", "trường"), ("Cấm", "lửa"), ("Đeo mặt nạ", "phòng độc")]
for i, (l1, l2) in enumerate(LABS):
    cx, cy = CXS[i % 4], CYS[i // 4]
    c.text(cx, cy + 52, l1, size=14, anchor="middle", weight="600")
    c.text(cx, cy + 70, l2, size=14, anchor="middle", weight="600")
ERR += c.check()
fig3 = c.svg("Tám kí hiệu cảnh báo vẽ lại: nguy hiểm về điện, nhiệt độ cao, chất dễ cháy, chất phóng xạ, tia laser, từ trường, cấm lửa, cần đeo mặt nạ phòng độc.",
             "Hình 3. Tám kí hiệu hay gặp (vẽ lại): sáu tam giác cảnh báo, một vòng tròn đỏ gạch chéo (cấm), một vòng tròn xanh (bắt buộc).")

# ================= Hình 4: bốn bước khi có sự cố
c = Canvas("f4", 420, 260)
STEPS = ["Dừng thí nghiệm, lùi ra", "Tắt nguồn điện nếu an toàn", "Báo ngay cho giáo viên", "Làm theo hướng dẫn của giáo viên"]
for i, s in enumerate(STEPS):
    cy = 36 + 60 * i
    c.add(f'<circle cx="40" cy="{cy}" r="18" fill="{ORG}"/>')
    c.add(f'<text x="40" y="{cy+6}" fill="#1f2937" font-size="16" font-weight="700" text-anchor="middle">{i+1}</text>')
    c.add(f'<rect x="72" y="{cy-24}" width="330" height="48" rx="8" fill="none" stroke="currentColor" stroke-width="2"/>')
    c.text(86, cy + 6, s, size=16)
    if i < 3:
        c.arr(f"s{i}", "o", 40, cy + 20, 40, cy + 40, 3, 9)
fig4 = c.svg("Bốn bước khi có sự cố: dừng thí nghiệm và lùi ra, tắt nguồn điện nếu an toàn, báo ngay cho giáo viên, làm theo hướng dẫn của giáo viên.",
             "Hình 4. Bốn bước khi có sự cố ở bàn thực hành: dừng, tắt nguồn nếu an toàn, báo giáo viên, làm theo hướng dẫn.")
ERR += c.check()

if ERR:
    print("\n".join("✗ " + e for e in ERR)); sys.exit(1)

# ================= Bảng số liệu TN1 (chèn vào bài)
f1 = lambda x: f"{x:.1f}".replace(".", ",")
rows = [f"<tr><td>{v}</td><td>{f1(d)}</td><td>{f1(l)}</td></tr>" for v, d, l in zip(VACH, VDO, LECH)]
bang = ('<div class="table-scroll">\n<table class="tl-table">\n<thead>\n'
        '<tr><th>Núm ở vạch (V)</th><th>Vôn kế chỉ (V)</th><th>Lệch (V)</th></tr>\n</thead>\n<tbody>\n'
        + "\n".join(rows) + "\n</tbody>\n</table>\n</div>")
nhiet = "nhiệt kế chỉ lần lượt " + "; ".join(str(t) for t in TN) + " °C"

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, fg in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
h = h.replace("__BANG_TN1__", bang).replace("__TILE__", "3").replace("__NHIET__", nhiet)
assert "__" not in h.replace("__PHUT__", "")
tmp = HERE / ".theory.tmp.html"
tmp.write_text(h.replace("__PHUT__", "15"), encoding="utf8")
lint = ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = subprocess.run([sys.executable, str(lint), str(tmp)], capture_output=True, text=True).stdout
tmp.unlink()
m = re.search(r"~?(\d+(?:[.,]\d+)?)\s*phút", out)
phut = -int(-float(m.group(1).replace(",", ".")) // 1) if m else None  # làm tròn LÊN (16,5 -> 17)
if phut is None:
    print("! không đọc được số phút từ lint_do_dai:\n" + out[:600]); sys.exit(1)
h = h.replace("__PHUT__", str(phut))
(HERE / "theory.html").write_text(h, encoding="utf8")

# ================= File thí nghiệm
BASE = {"mon": "vat-ly", "lop": 10, "bai": "Bài 2. Các quy tắc an toàn trong phòng thực hành Vật lí", "lesson_id": 47,
        "nguon_trong_bai": "content/lesson-samples/l10-an-toan-phong-thuc-hanh/theory.html"}
tn = [
    {**BASE,
     "id": "tn-l10-an-toan-01",
     "ten": "Núm bộ nguồn ở các vạch 3, 6, 9, 12 V: vôn kế chỉ bao nhiêu",
     "loai": "thi_nghiem", "muc_do": "co_ban",
     "kien_thuc": ["antoan.doc_nhan_thiet_bi", "antoan.hieu_dien_the_khop", "antoan.sai_so_nguon"],
     "muc_tieu": "Đọc nhãn Input/Output, DC/AC, cực +/−; so số chỉ vôn kế với vạch núm, nhận ra độ lệch vài phần trăm và vì sao phải chọn đúng vạch cho dụng cụ.",
     "dung_cu": [{"ten": "Bộ nguồn học đường (Input 220 V ~, Output 3–12 V DC)", "so_luong": 1},
                 {"ten": "Vôn kế một chiều, độ chia 0,1 V", "so_luong": 1},
                 {"ten": "Dây nối có đầu cắm", "so_luong": 2}],
     "cac_buoc": {"lam": ["Được giáo viên cho phép, đặt núm lần lượt ở các vạch 3; 6; 9; 12 V.",
                          "Mắc vôn kế một chiều vào hai cực Output (cực đỏ của vôn kế nối cực +), đọc số chỉ."],
                  "quan_sat": ["Số chỉ lần lượt " + "; ".join(f1(d) for d in VDO) + " V.",
                               "Số chỉ luôn cao hơn vạch 0,1–0,4 V, tức khoảng 3 % của vạch."],
                  "rut_ra": ["Vạch chỉ là giá trị gần đúng; độ lệch là sai số của bộ nguồn (và làm tròn tới 0,1 V của vôn kế).",
                             "Chọn vạch bằng định mức dụng cụ rồi đo lại bằng vôn kế; nhầm vạch 12 V cho bóng 6 V là hơn gấp đôi định mức."]},
     "tham_so": [{"ky_hieu": "vach", "ten": "Vạch núm bộ nguồn", "don_vi": "V", "kieu": "dieu_chinh", "min": 3, "max": 12, "mac_dinh": 6, "buoc": 3},
                 {"ky_hieu": "sai_so_nguon", "ten": "Độ lệch tương đối của nguồn so với vạch", "don_vi": "", "kieu": "co_dinh", "gia_tri": 0.03},
                 {"ky_hieu": "chia_do", "ten": "Độ chia của vôn kế", "don_vi": "V", "kieu": "co_dinh", "gia_tri": 0.1},
                 {"ky_hieu": "V", "ten": "Số chỉ vôn kế", "don_vi": "V", "kieu": "do_duoc", "sai_so_do": 0.05}],
     "mo_hinh": {"phuong_trinh": ["V_thực = 1,03 · vạch", "V_đọc = V_thực làm tròn tới 0,1 V", "lệch = V_đọc − vạch"],
                 "gia_thiet": ["nguồn ổn áp, không mắc tải", "độ lệch tỉ lệ với vạch (~3 %)"]},
     "so_lieu_mau": {"cot": ["Vạch (V)", "V thực (V)", "V đọc (V)", "Lệch (V)"],
                     "hang": [[v, round(1.03 * v, 3), d, l] for v, d, l in zip(VACH, VDO, LECH)],
                     "ghi_chu": "Số liệu minh hoạ tính từ mô hình V = 1,03·vạch, làm tròn tới 0,1 V."},
     "ket_qua_ky_vong": "Số chỉ 3,1; 6,2; 9,3; 12,4 V; lệch 0,1–0,4 V (≈ 3 %).",
     "hien_tuong_hay_sai": ["Cho rằng số chỉ khác vạch là đo sai hay nguồn hỏng.", "Bỏ qua vôn kế, tin tuyệt đối vào vạch núm.",
                            "Chọn vạch lớn hơn định mức cho dụng cụ 'sáng hơn'."],
     "sai_so_thuong_gap": "Sai số bộ nguồn, làm tròn của vôn kế, đọc nhầm thang đo.",
     "an_toan": "Chỉ làm khi giáo viên cho phép; tắt công tắc trước khi nối hoặc tháo dây; vôn kế mắc đúng cực.",
     "goi_y_mo_phong": {"loai": "so_do_luc+bang_so_lieu",
                        "y_tuong": "Bộ nguồn có núm xoay 3/6/9/12 V, vôn kế hiện số chỉ; kéo thêm bóng 6 V để thấy cháy khi ở vạch 12 V.",
                        "diem_nhan": "Nút 'nối bóng 6 V' ở vạch 12 V: bóng sáng chói rồi tắt, kèm cảnh báo quá áp."}},
    {**BASE,
     "id": "tn-l10-an-toan-02",
     "ten": "Nhiệt độ cạnh ngọn đèn cồn theo khoảng cách",
     "loai": "thi_nghiem", "muc_do": "trung_binh",
     "kien_thuc": ["antoan.khoang_cach_an_toan", "antoan.vat_nong"],
     "muc_tieu": "Thấy nhiệt độ giảm rất nhanh khi ra xa nguồn nóng (số chỉ minh hoạ, không phải quy luật 1/r²), từ đó hiểu quy tắc giữ khoảng cách an toàn.",
     "dung_cu": [{"ten": "Đèn cồn", "so_luong": 1}, {"ten": "Nhiệt kế đo tới 200 °C", "so_luong": 1},
                 {"ten": "Thước, giá đỡ nhiệt kế", "so_luong": 1}],
     "cac_buoc": {"lam": ["Giáo viên đặt nhiệt kế cạnh ngọn đèn cồn, cách lần lượt 2; 5; 10; 20 cm, đợi số chỉ ổn định.",
                          "Cả lớp đứng xa quan sát, ghi số chỉ."],
                  "quan_sat": ["Nhiệt kế chỉ lần lượt " + "; ".join(str(t) for t in TN) + " °C (nhiệt độ phòng 25 °C; nhiệt kế đo tới 200 °C; số chỉ minh hoạ, không phải quy luật 1/r²).",
                               "Từ 5 cm ra 10 cm, phần nóng thêm giảm từ 16 °C còn 4 °C."],
                  "rut_ra": ["Gần ngọn lửa nóng rất nhiều, ra xa thì nguội nhanh.", "Nhiều thí nghiệm nung nóng, laser, vật bắn ra cần giữ khoảng cách an toàn."]},
     "tham_so": [{"ky_hieu": "d", "ten": "Khoảng cách tới ngọn lửa", "don_vi": "cm", "kieu": "dieu_chinh", "min": 2, "max": 40, "mac_dinh": 10, "buoc": 1},
                 {"ky_hieu": "T_phong", "ten": "Nhiệt độ phòng", "don_vi": "°C", "kieu": "co_dinh", "gia_tri": 25},
                 {"ky_hieu": "K", "ten": "Hệ số nguồn nóng", "don_vi": "°C·cm²", "kieu": "co_dinh", "gia_tri": 400},
                 {"ky_hieu": "T", "ten": "Nhiệt độ nhiệt kế", "don_vi": "°C", "kieu": "do_duoc", "sai_so_do": 1}],
     "mo_hinh": {"phuong_trinh": ["T = T_phòng + K/d²", "T làm tròn tới 1 °C"],
                 "gia_thiet": ["mô hình đơn giản, số liệu minh hoạ", "nguồn nhỏ, đo cạnh ngọn lửa, bỏ qua gió"]},
     "so_lieu_mau": {"cot": ["d (cm)", "T (°C)", "T − 25 (°C)"],
                     "hang": [[d, t, t - 25] for d, t in zip(DK, TN)],
                     "ghi_chu": "Số liệu minh hoạ tính từ mô hình đơn giản T = 25 + 400/d² (chọn cho dễ tính, không phải quy luật 1/r² của ngọn lửa thật), làm tròn 1 °C; nhiệt kế đo tới 200 °C."},
     "ket_qua_ky_vong": "125; 41; 29; 26 °C; phần nóng thêm 100; 16; 4; 1 °C.",
     "hien_tuong_hay_sai": ["Tưởng càng xa thì nhiệt độ giảm đều từng cm.", "Tưởng ngoài 'vùng đỏ' của lửa thì không nóng."],
     "sai_so_thuong_gap": "Nhiệt kế đặt lệch ngọn lửa, gió thổi, chưa đợi ổn định.",
     "an_toan": "Giáo viên làm, học sinh đứng xa; không để đèn cồn gần thiết bị điện hay chất dễ cháy.",
     "goi_y_mo_phong": {"loai": "do_thi+bang_so_lieu",
                        "y_tuong": "Kéo nhiệt kế ra xa ngọn lửa, đồ thị T theo d vẽ dần.",
                        "diem_nhan": "Vùng màu đỏ thu nhỏ khi ra xa; đánh dấu khoảng cách an toàn."}},
    {**BASE,
     "id": "tn-l10-an-toan-03",
     "ten": "Rà phòng thực hành: xếp kí hiệu cảnh báo vào nhóm",
     "loai": "vi_du", "muc_do": "co_ban",
     "kien_thuc": ["antoan.ki_hieu_canh_bao", "antoan.nhom_ki_hieu"],
     "muc_tieu": "Nhận ra hình dạng và màu của kí hiệu (tam giác cảnh báo, tròn đỏ gạch chéo cấm, tròn xanh bắt buộc) rồi nói việc phải làm.",
     "dung_cu": [{"ten": "Điện thoại chụp ảnh", "so_luong": 1}, {"ten": "Phiếu ghi nhóm kí hiệu", "so_luong": 1}],
     "cac_buoc": {"lam": ["Đi một vòng phòng thực hành, tìm ít nhất 5 kí hiệu (bộ nguồn, tủ hoá chất, chai cồn, bình khí...), chụp ảnh."],
                  "quan_sat": ["Kí hiệu cùng nhóm thường cùng hình dạng, cùng màu viền."],
                  "rut_ra": ["Xếp từng kí hiệu vào nhóm cảnh báo, cấm hay bắt buộc rồi nêu việc phải làm."]},
     "tham_so": [{"ky_hieu": "so_ki_hieu", "ten": "Số kí hiệu tìm được", "don_vi": "", "kieu": "dieu_chinh", "min": 1, "max": 16, "mac_dinh": 5, "buoc": 1},
                 {"ky_hieu": "nhom", "ten": "Nhóm kí hiệu", "don_vi": "", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["nhóm = f(hình dạng, màu viền)"],
                 "gia_thiet": ["quy ước đa số: tam giác = cảnh báo, tròn đỏ gạch chéo = cấm, tròn xanh = bắt buộc"]},
     "so_lieu_mau": {"cot": ["Kí hiệu", "Hình dạng", "Nhóm"],
                     "hang": [["nguy hiểm về điện", "tam giác", "cảnh báo"], ["nhiệt độ cao", "tam giác", "cảnh báo"],
                              ["chất dễ cháy", "tam giác", "cảnh báo"], ["cấm lửa", "tròn đỏ gạch chéo", "cấm"],
                              ["đeo mặt nạ phòng độc", "tròn xanh", "bắt buộc"]],
                     "ghi_chu": "Bảng minh hoạ, không phải số đo."},
     "ket_qua_ky_vong": "Mỗi kí hiệu tìm được xếp đúng một nhóm và nêu được việc phải làm.",
     "hien_tuong_hay_sai": ["Chỉ nhìn hình bên trong, bỏ qua hình dạng và màu.", "Cho rằng kí hiệu cảnh báo chỉ để trang trí."],
     "goi_y_mo_phong": {"loai": "bang_so_lieu",
                        "y_tuong": "Kéo thả kí hiệu vào ba ô nhóm, đúng thì hiện việc phải làm.",
                        "diem_nhan": "Kí hiệu 'lạ' không có trong bài để học sinh suy luận từ hình dạng và màu."}},
]
for d in tn:
    (ROOT / "content/thi-nghiem" / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"ok theory.html {len(h)} ký tự · 4 hình · {phut} phút · 3 file thí nghiệm")
