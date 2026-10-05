"""Sinh 3 hình SVG + 2 bảng số liệu cho bài 'Thực hành: Đo gia tốc rơi tự do' (lesson 56),
thay mốc <!--FIGn-->, __BANG_TN1__, __BANG_TN2__, __PHUT__ trong theory.src.html -> theory.html,
và ghi 3 file thí nghiệm content/thi-nghiem/tn-l10-do-g-0{1,2,3}.json (số liệu tính từ cùng mô hình).
Có lớp kiểm hình học: nhãn không chồng nhau / không vượt viewBox / không bị nét cắt xuyên; mũi tên đúng chiều.
Chạy: python3 build_figs.py   (sau đó: python3 build_bundle.py)"""
import json, math, pathlib, re, subprocess, sys
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
            if a[5] < 14:
                errs.append(f"{self.name}: nhãn '{a[0]}' cỡ {a[5]} < 14")
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
G = 9.8
SYS = 0.002          # trễ hệ thống do từ dư (s)
DS, DT_DC = 0.001, 0.001


def ok(cond, msg):
    if not cond:
        ERR.append(msg)


# ================= Mô hình số liệu
# TN1: s = 0,500 m, 5 lần thả; t = sqrt(2s/g) + SYS + nhiễu cố định (không ngẫu nhiên, để tái lập)
S1 = 0.500
NOISE = [-0.002, 0.001, 0.000, 0.002, -0.001]
TM1 = math.sqrt(2 * S1 / G)
T1 = [round(TM1 + SYS + n, 3) for n in NOISE]
TB1 = round(sum(T1) / 5, 3)
D1 = [round(abs(t - TB1), 3) for t in T1]
DTB1 = round(sum(D1) / 5, 4)
DT1 = round(DTB1 + DT_DC, 4)
GB1 = 2 * S1 / TB1 ** 2
DEL1 = DS / S1 + 2 * DT1 / TB1
DG1 = DEL1 * GB1
ok(T1 == [0.319, 0.322, 0.321, 0.323, 0.320], T1)
ok(TB1 == 0.321 and D1 == [0.002, 0.001, 0.0, 0.002, 0.001] and DTB1 == 0.0012 and DT1 == 0.0022, (TB1, D1, DTB1, DT1))
ok(f"{GB1:.2f}" == "9.70" and f"{DEL1:.4f}" == "0.0157" and f"{DG1:.2f}" == "0.15", (GB1, DEL1, DG1))
ok(abs(GB1 - 9.70) < 0.005, GB1)
ok(f"{DS / S1 * 100:.1f}" == "0.2" and f"{2 * DT1 / TB1 * 100:.1f}" == "1.4", "phần đóng góp Δs/s, 2Δt/t")
ok(GB1 - DG1 < 9.8 < GB1 + DG1, "9,8 phải nằm trong khoảng g ± Δg của TN1")
ok(round(GB1 * DEL1, 2) == round(9.70 * 0.0157, 2), "Δg dùng 9,70 và 0,0157")

# TN2: nhiều độ cao
S2 = [0.200, 0.300, 0.400, 0.500, 0.600]
TB2 = [round(math.sqrt(2 * s / G) + SYS, 3) for s in S2]
T2SQ = [round(t * t, 4) for t in TB2]
ok(TB2 == [0.204, 0.249, 0.288, 0.321, 0.352], TB2)
ok(T2SQ == [0.0416, 0.0620, 0.0829, 0.1030, 0.1239], T2SQ)
ok(TB2[3] == TB1, "hàng s = 0,500 của TN2 phải khớp TN1")
SL = (S2[-1] - S2[0]) / (T2SQ[-1] - T2SQ[0])
ok(f"{SL:.2f}" == "4.86" and f"{2 * round(SL, 2):.2f}" == "9.72", SL)
SL2 = (S2[3] - S2[1]) / (T2SQ[3] - T2SQ[1])
ok(f"{SL2:.2f}" == "4.88" and f"{2 * SL2:.2f}" == "9.76", SL2)
ok(all(abs(s - 4.86 * t2) < 0.004 for s, t2 in zip(S2, T2SQ)), "điểm lệch đường thẳng")

# TN3: video 240 khung/s
FPS = [30, 60, 120, 240, 480]
T3TRUE = TM1 + SYS
V3 = [(f, round(T3TRUE * f), round(T3TRUE * f) / f, 1 / f) for f in FPS]
ok(V3[3][1] == 77 and f"{V3[3][2]:.3f}" == "0.321" and f"{1 / 240:.4f}" == "0.0042", V3[3])

# Câu quiz và bài toán mẫu
ok(f"{2 * 0.300 / 0.247 ** 2:.2f}" == "9.83" and f"{0.300 / 0.247 ** 2:.2f}" == "4.92" and
   f"{2 * 0.300 / 0.247:.2f}" == "2.43" and f"{2 * 0.300 * 0.247 ** 2:.4f}" == "0.0366" and f"{0.6:.3f}" and f"{0.247 ** 2:.4f}" == "0.0610", "Q2")
ok(f"{0.1 / 0.32 * 100:.0f}" == "31", "Q1")
ok(f"{2 * 0.51 / 0.319 ** 2:.2f}" == "10.02" and f"{2 * 0.5 / 0.319 ** 2:.2f}" == "9.83" and
   f"{(2 * 0.51 / 0.319 ** 2) / (2 * 0.5 / 0.319 ** 2) - 1:.2f}" == "0.02", "Q4")
ok(f"{9.68 - 0.13:.2f}" == "9.55" and f"{9.68 + 0.13:.2f}" == "9.81" and not (9.45 < 9.8 < 9.55) and not (9.90 < 9.8 < 10.50), "Q6")
ok(abs(math.sqrt(0.8 / 0.2) - 2) < 1e-9, "Q7")
# bài mẫu: s = 0,800; t = 0,403; 0,404; 0,405; 0,404
tm = [0.403, 0.404, 0.405, 0.404]
tbm = round(sum(tm) / 4, 3)
dm = [round(abs(t - tbm), 3) for t in tm]
dtbm = sum(dm) / 4
dtm = dtbm + DT_DC
gm = 2 * 0.8 / tbm ** 2
delm = DS / 0.8 + 2 * dtm / tbm
ok(tbm == 0.404 and dm == [0.001, 0.0, 0.001, 0.0] and abs(dtbm - 0.0005) < 1e-12 and abs(dtm - 0.0015) < 1e-12, (tbm, dm, dtbm, dtm))
ok(f"{gm:.2f}" == "9.80" and f"{delm:.4f}" == "0.0087" and f"{9.80 * 0.0087:.2f}" == "0.09" and 9.71 < 9.8 < 9.89, (gm, delm))
# điền bước: s = 0,450; t = 0,303; Δt = 0,0022
g3 = 2 * 0.45 / 0.303 ** 2
del3 = DS / 0.45 + 2 * 0.0022 / 0.303
ok(f"{g3:.2f}" == "9.80" and f"{del3:.4f}" == "0.0167" and f"{9.80 * 0.0167:.2f}" == "0.16", (g3, del3))
# thử sức: điện thoại 240 khung/s
dtv = dtbm + 1 / 240
delv = DS / 0.8 + 2 * round(dtv, 4) / tbm
ok(f"{round(dtv, 4):.4f}" == "0.0047" and f"{0.00125 + 2 * 0.0047 / 0.404:.4f}" == "0.0245" and f"{9.80 * 0.0245:.2f}" == "0.24", (dtv, delv))
# thử thách
ok(f"{2 * 1.0 / 0.452 ** 2:.2f}" == "9.79", "⭐")
ok(f"{0.5 * 9.8 * 0.4 ** 2:.2f}" == "0.78", "⭐⭐⭐")
# số trong lời văn mở bài / giải thích
ok(abs(TM1 - 0.3194) < 1e-4, "t lý thuyết 0,32 s")

# ================= Hình 1: bố trí thí nghiệm
c = Canvas("f1", 420, 330)
c.line(60, 26, 60, 290, "currentColor", 5)
c.line(20, 290, 120, 290, "currentColor", 6)
c.line(60, 53, 140, 53, "currentColor", 5)
c.add(f'<rect x="140" y="40" width="60" height="26" rx="3" fill="rgba(248,113,113,.25)" stroke="currentColor" stroke-width="2"/>')
c.add(f'<circle cx="170" cy="77" r="11" fill="{ORG}" stroke="currentColor" stroke-width="1.5"/>')
c.add('<rect x="146" y="232" width="10" height="40" fill="currentColor" opacity=".3" stroke="currentColor" stroke-width="1.5"/>'
      '<rect x="184" y="232" width="10" height="40" fill="currentColor" opacity=".3" stroke="currentColor" stroke-width="1.5"/>'
      '<rect x="146" y="262" width="48" height="10" fill="currentColor" opacity=".3" stroke="currentColor" stroke-width="1.5"/>')
c.line(140, 246, 200, 246, RED, 2.5, "6 4", obstacle=False)      # tia sáng
c.line(172, 88, 250, 88, "currentColor", 1.4, "4 4", .55, obstacle=False)
c.line(200, 246, 250, 246, "currentColor", 1.4, "4 4", .55, obstacle=False)
c.arr("s1", "k", 250, 167, 250, 88, 2.2, 10)
c.arr("s2", "k", 250, 167, 250, 246, 2.2, 10)
c.text(262, 171, "s", size=18, italic=True)
c.add(f'<rect x="290" y="70" width="114" height="56" rx="6" fill="none" stroke="currentColor" stroke-width="2"/>')
c.text(347, 94, "đồng hồ", anchor="middle", size=14)
c.text(347, 114, "hiện số", anchor="middle", size=14)
c.add('<polyline points="200,53 347,53 347,70" fill="none" stroke="currentColor" stroke-width="1.8"/>')
c.segs += [(200, 53, 347, 53), (347, 53, 347, 70)]
c.add('<polyline points="194,266 347,266 347,126" fill="none" stroke="currentColor" stroke-width="1.8"/>')
c.segs += [(194, 266, 347, 266), (347, 266, 347, 126)]
c.text(96, 30, "nam châm điện", size=14)
c.text(98, 84, "bi thép", size=14)
c.text(150, 300, "cổng quang", size=14)
c.text(20, 318, "giá đỡ", size=14)
x1_, y1_, x2_, y2_ = c.arrows["s1"]
ok(y2_ < y1_, "f1: mũi tên s1 phải hướng lên tới mép dưới bi")
ok(c.arrows["s2"][3] > c.arrows["s2"][1], "f1: mũi tên s2 phải hướng xuống tới tia sáng")
ok(abs(c.arrows["s1"][3] - 88) < 1e-9 and abs(c.arrows["s2"][3] - 246) < 1e-9, "f1: đầu mũi tên s phải tại mép dưới bi và tia sáng")
fig1 = c.svg("Sơ đồ bố trí đo gia tốc rơi tự do: giá đỡ thẳng đứng, nam châm điện giữ viên bi thép ở trên, cổng quang ở dưới với tia sáng nét đứt đỏ, hai dây nối tới đồng hồ hiện số; mũi tên hai đầu s đo từ mép dưới bi tới tia sáng",
             "Hình 1. Bố trí thí nghiệm. Ngắt điện nam châm: bi rơi và đồng hồ bắt đầu đếm; bi che tia sáng (nét đỏ đứt) thì đồng hồ dừng. <em>s</em> đo từ mép dưới bi (lúc còn ở nam châm) tới tia sáng.")
ERR += c.check()

# ================= Hình 2: đồ thị s theo t²
c = Canvas("f2", 420, 270)
OX, OY, KX, KY = 60, 220, 2400, 300
X = lambda t2: OX + KX * t2
Y = lambda s: OY - KY * s
c.arr("tx", "k", OX, OY, 408, OY, 1.8, 9)
c.arr("vy", "k", OX, OY, OX, 22, 1.8, 9)
c.text(68, 38, "s (m)", size=14)
c.text(350, 252, "t² (s²)", size=14)
c.text(38, 238, "O", size=14)
for sv in (0.2, 0.4, 0.6):
    c.line(OX - 4, Y(sv), OX + 4, Y(sv), "currentColor", 1.5, obstacle=False)
    c.text(OX - 8, Y(sv) + 5, vn(sv, 1), size=14, anchor="end", weight="600")
for tv in (0.05, 0.10):
    c.line(X(tv), OY - 4, X(tv), OY + 4, "currentColor", 1.5, obstacle=False)
    c.text(X(tv), OY + 20, vn(tv, 2), size=14, anchor="middle", weight="600")
c.line(X(0), Y(0), X(0.130), Y(4.86 * 0.130), BLUE, 3)
P = [(X(t2), Y(s)) for s, t2 in zip(S2, T2SQ)]
c.line(P[0][0], P[0][1], P[-1][0], P[0][1], "currentColor", 1.6, "5 4", obstacle=False)
c.line(P[-1][0], P[0][1], P[-1][0], P[-1][1], "currentColor", 1.6, "5 4", obstacle=False)
for px, py in P:
    c.add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="{ORG}" stroke="currentColor" stroke-width="1.2"/>')
c.text((P[0][0] + P[-1][0]) / 2, P[0][1] + 20, "Δ(t²)", size=14, anchor="middle")
c.text(P[-1][0] + 9, (P[0][1] + P[-1][1]) / 2 + 5, "Δs", size=14)
ok(P[-1][0] < 408 and all(px < P[-1][0] + 1 for px, _ in P), "f2: điểm vượt trục")
ok(all(abs(py - (OY - KY * 4.86 * (px - OX) / KX)) < 2.5 for px, py in P), "f2: điểm lệch đường vẽ quá 2,5 đơn vị")
fig2 = c.svg("Đồ thị quãng đường s theo bình phương thời gian t²: năm điểm cam gần như nằm trên một đường thẳng xanh đi qua gốc toạ độ; tam giác nét đứt có cạnh ngang Δ(t²) và cạnh đứng Δs cho độ dốc",
             "Hình 2. Đồ thị <em>s</em> theo <em>t</em><sup>2</sup> (số liệu minh hoạ): các điểm gần thẳng hàng qua gốc. Độ dốc Δ<em>s</em>/Δ(<em>t</em><sup>2</sup>) bằng <em>g</em>/2.",
             exp="tn-l10-do-g-02")
ERR += c.check()

# ================= Hình 3: hai cách đo s — đúng và sai
c = Canvas("f3", 420, 250)
c.add('<rect x="130" y="14" width="100" height="32" rx="3" fill="rgba(248,113,113,.25)" stroke="currentColor" stroke-width="2"/>')
c.text(180, 36, "nam châm", anchor="middle", size=14)
c.add(f'<circle cx="180" cy="59" r="13" fill="{ORG}" stroke="currentColor" stroke-width="1.5"/>')
c.dot(180, 72, 2.5)
c.text(200, 64, "bi thép", size=14)
c.line(120, 205, 240, 205, RED, 2.5, "6 4", obstacle=False)
c.text(130, 232, "tia sáng cổng quang", size=14)
c.line(100, 72, 176, 72, "currentColor", 1.4, "4 4", .55, obstacle=False)
c.line(100, 205, 120, 205, "currentColor", 1.4, "4 4", .55, obstacle=False)
c.arr("d1", "g", 100, 138, 100, 72, 2.6, 10)
c.arr("d2", "g", 100, 138, 100, 205, 2.6, 10)
c.text(58, 146, "đúng", GRN, 14)
c.line(230, 46, 290, 46, "currentColor", 1.4, "4 4", .55, obstacle=False)
c.line(240, 205, 290, 205, "currentColor", 1.4, "4 4", .55, obstacle=False)
c.arr("e1", "r", 290, 125, 290, 46, 2.6, 10)
c.arr("e2", "r", 290, 125, 290, 205, 2.6, 10)
c.text(302, 130, "sai", RED, 14)
ok(c.arrows["d1"][3] == 72 and c.arrows["e1"][3] == 46 and c.arrows["d2"][3] == c.arrows["e2"][3] == 205, "f3: đầu mũi tên không đúng mốc")
ok(72 > 46, "f3: mép dưới bi phải thấp hơn mặt nam châm")
fig3 = c.svg("Hai cách đo độ cao s: mũi tên xanh lá đúng đo từ mép dưới viên bi tới tia sáng của cổng quang; mũi tên đỏ sai đo từ mặt dưới nam châm, dài hơn đoạn bi thật sự rơi một đường kính bi",
             "Hình 3. Đúng: <em>s</em> đo từ mép dưới bi tới tia sáng. Sai: đo từ mặt nam châm, dài hơn đoạn bi thật sự rơi một đường kính bi.")
ERR += c.check()

if ERR:
    print("\n".join("✗ " + str(e) for e in ERR)); sys.exit(1)

# ================= Bảng số liệu
def table(head, rows):
    return ('<div class="table-scroll">\n<table class="tl-table">\n<thead>\n<tr>' + "".join(f"<th>{h}</th>" for h in head)
            + "</tr>\n</thead>\n<tbody>\n" + "\n".join("<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in rows)
            + "\n</tbody>\n</table>\n</div>")


bang1 = table(["Lần đo", "$t$ (s)", "$\\Delta t_i$ (s)"],
              [[i + 1, vn(t, 3), vn(d, 3)] for i, (t, d) in enumerate(zip(T1, D1))])
bang2 = table(["$s$ (m)", "$\\bar t$ (s)", "$\\bar t^2$ (s²)"],
              [[vn(s, 3), vn(t, 3), vn(t2, 4)] for s, t, t2 in zip(S2, TB2, T2SQ)])

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, fg in enumerate((fig1, fig2, fig3), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
h = h.replace("__BANG_TN1__", bang1).replace("__BANG_TN2__", bang2)
assert "__" not in h.replace("__PHUT__", "")
tmp = HERE / ".theory.tmp.html"
tmp.write_text(h.replace("__PHUT__", "15"), encoding="utf8")
lint = ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = subprocess.run([sys.executable, str(lint), str(tmp)], capture_output=True, text=True).stdout
tmp.unlink()
m = re.search(r"~?(\d+(?:[.,]\d+)?)\s*phút", out)
if not m:
    print("! không đọc được số phút từ lint_do_dai:\n" + out[:600]); sys.exit(1)
phut = round(float(m.group(1).replace(",", ".")))
h = h.replace("__PHUT__", str(phut))
(HERE / "theory.html").write_text(h, encoding="utf8")

# ================= File thí nghiệm
BASE = {"mon": "vat-ly", "lop": 10, "bai": "Bài 11. Thực hành: Đo gia tốc rơi tự do", "lesson_id": 56,
        "nguon_trong_bai": "content/lesson-samples/l10-thuc-hanh-do-g/theory.html"}
r3 = lambda x: round(x, 4)
tn = [
    {**BASE, "id": "tn-l10-do-g-01",
     "ten": "Đo g bằng cổng quang: thả bi 5 lần từ s = 0,500 m, xử lí sai số",
     "loai": "thi_nghiem", "muc_do": "trung_binh",
     "kien_thuc": ["doig.cong_thuc_g", "doig.sai_so_tuyet_doi", "doig.sai_so_tuong_doi", "doig.sai_so_he_thong"],
     "muc_tieu": "Từ 5 lần đo thời gian rơi, tính t trung bình, sai số tuyệt đối từng lần, sai số của t, rồi g = ḡ ± Δg; nhận ra thời gian chi phối sai số và khoảng ḡ ± Δg chứa 9,8.",
     "dung_cu": [{"ten": "Giá đỡ thẳng đứng + dây dọi", "so_luong": 1}, {"ten": "Nam châm điện + hộp công tắc", "so_luong": 1},
                 {"ten": "Viên bi thép", "so_luong": 1}, {"ten": "Cổng quang điện", "so_luong": 1},
                 {"ten": "Đồng hồ đo thời gian hiện số, độ chia 0,001 s", "so_luong": 1}, {"ten": "Thước, độ chia 1 mm", "so_luong": 1}],
     "cac_buoc": {"lam": ["Dựng giá thẳng đứng bằng dây dọi; đặt cổng quang sao cho tia sáng cách mép dưới bi (lúc còn ở nam châm) s = 0,500 m.",
                          "Ngắt công tắc nam châm điện, ghi thời gian rơi t trên đồng hồ; lặp 5 lần."],
                  "quan_sat": ["t = " + "; ".join(vn(t, 3) for t in T1) + " s.", "Các lần chênh nhau vài phần nghìn giây."],
                  "rut_ra": [f"t̄ = {vn(TB1, 3)} s; Δt̄ = {vn(DTB1, 4)} s; Δt = {vn(DT1, 4)} s.",
                             f"ḡ = {vn(GB1)} m/s²; δ ≈ {vn(DEL1, 4)}; Δg ≈ {vn(DG1)} m/s²; g = {vn(GB1)} ± {vn(DG1)} m/s², khoảng chứa 9,8."]},
     "tham_so": [{"ky_hieu": "s", "ten": "Độ cao thả", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.2, "max": 1.0, "mac_dinh": S1, "buoc": 0.05},
                 {"ky_hieu": "tre_ht", "ten": "Độ trễ hệ thống (từ dư nam châm)", "don_vi": "s", "kieu": "dieu_chinh", "min": 0, "max": 0.006, "mac_dinh": SYS, "buoc": 0.001},
                 {"ky_hieu": "nhieu", "ten": "Biên độ nhiễu ngẫu nhiên mỗi lần thả", "don_vi": "s", "kieu": "dieu_chinh", "min": 0, "max": 0.004, "mac_dinh": 0.002, "buoc": 0.001},
                 {"ky_hieu": "g_that", "ten": "Gia tốc rơi tự do thật", "don_vi": "m/s²", "kieu": "co_dinh", "gia_tri": G},
                 {"ky_hieu": "dcnn_t", "ten": "Độ chia nhỏ nhất đồng hồ", "don_vi": "s", "kieu": "co_dinh", "gia_tri": DT_DC},
                 {"ky_hieu": "dcnn_s", "ten": "Độ chia nhỏ nhất thước", "don_vi": "m", "kieu": "co_dinh", "gia_tri": DS},
                 {"ky_hieu": "t", "ten": "Thời gian rơi đo được", "don_vi": "s", "kieu": "do_duoc", "sai_so_do": DT_DC},
                 {"ky_hieu": "g_do", "ten": "Gia tốc tính được", "don_vi": "m/s²", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["t_lần = sqrt(2s/g_thật) + tre_ht + nhiễu_lần, làm tròn 0,001 s", "t̄ = trung bình các lần", "Δt_i = |t_i − t̄|; Δt = trung bình(Δt_i) + dcnn_t",
                                  "ḡ = 2s/t̄²", "δ = dcnn_s/s + 2Δt/t̄; Δg = δ·ḡ"],
                 "gia_thiet": ["bỏ qua sức cản không khí", "độ trễ hệ thống không đổi mọi lần", "g thật = 9,8 m/s²", "nhiễu là dãy cố định để tái lập: −0,002; +0,001; 0; +0,002; −0,001 s"]},
     "so_lieu_mau": {"cot": ["Lần đo", "t (s)", "|t − t̄| (s)"], "hang": [[i + 1, t, d] for i, (t, d) in enumerate(zip(T1, D1))],
                     "ghi_chu": f"Số liệu minh hoạ tính từ mô hình (s = 0,500 m; trễ hệ thống 0,002 s), không phải đo thật. t̄ = {TB1}; ḡ = {GB1:.4f}; δ = {DEL1:.4f}; Δg = {DG1:.4f}."},
     "ket_qua_ky_vong": f"g = {vn(GB1)} ± {vn(DG1)} m/s²; Δs/s = 0,2 %, 2Δt/t̄ ≈ 1,4 %: thời gian chi phối; khoảng 9,55–9,85 chứa 9,8.",
     "hien_tuong_hay_sai": ["Quên hệ số 2 trước Δt/t̄.", "Cho rằng lấy trung bình là hết sai số.", "Thấy ḡ khác 9,8 liền kết luận thí nghiệm hỏng, không xét khoảng ± Δg."],
     "sai_so_thuong_gap": "Đo s sai gốc (từ mặt nam châm, dài hơn một đường kính bi); từ dư làm bi rời muộn; cổng quang đặt lệch tâm bi; giá đỡ không thẳng đứng.",
     "an_toan": "Đặt hộp mềm dưới cổng quang để bi không nảy ra sàn.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu",
                        "y_tuong": "Giá đỡ, nam châm, bi, cổng quang; nút thả; đồng hồ hiện t; bảng điền sau mỗi lần thả và tự tính t̄, Δt, ḡ, Δg.",
                        "diem_nhan": "Thanh trượt 'độ trễ hệ thống': kéo lên thì ḡ lệch hẳn khỏi 9,8 dù Δg vẫn nhỏ (chụm nhưng lệch)."}},
    {**BASE, "id": "tn-l10-do-g-02",
     "ten": "Đo g bằng đồ thị s theo t² từ năm độ cao",
     "loai": "thi_nghiem", "muc_do": "trung_binh",
     "kien_thuc": ["doig.do_thi_s_t2", "doig.do_doc_g_nua", "doig.cong_thuc_g"],
     "muc_tieu": "Vẽ điểm (t², s) cho năm độ cao, thấy chúng gần thẳng hàng qua gốc, tính độ dốc và g = 2·độ dốc.",
     "dung_cu": [{"ten": "Bộ nam châm điện, bi, cổng quang, đồng hồ hiện số như thí nghiệm 1", "so_luong": 1}, {"ten": "Thước 1 mm", "so_luong": 1}, {"ten": "Giấy kẻ ô", "so_luong": 1}],
     "cac_buoc": {"lam": ["Dời cổng quang để s = 0,200; 0,300; 0,400; 0,500; 0,600 m.", "Mỗi độ cao thả 5 lần, lấy t̄; tính t̄²; vẽ điểm (t̄², s)."],
                  "quan_sat": ["Các điểm gần như nằm trên một đường thẳng đi qua gốc toạ độ."],
                  "rut_ra": [f"Độ dốc ≈ {vn(SL)} m/s² (hai điểm xa nhau), g = 2·độ dốc ≈ {vn(2 * round(SL, 2))} m/s²."]},
     "tham_so": [{"ky_hieu": "s_max", "ten": "Độ cao lớn nhất", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.4, "max": 1.0, "mac_dinh": 0.6, "buoc": 0.1},
                 {"ky_hieu": "tre_ht", "ten": "Độ trễ hệ thống", "don_vi": "s", "kieu": "dieu_chinh", "min": 0, "max": 0.006, "mac_dinh": SYS, "buoc": 0.001},
                 {"ky_hieu": "g_that", "ten": "Gia tốc rơi tự do thật", "don_vi": "m/s²", "kieu": "co_dinh", "gia_tri": G},
                 {"ky_hieu": "t2", "ten": "Bình phương thời gian rơi", "don_vi": "s²", "kieu": "tinh_ra"},
                 {"ky_hieu": "do_doc", "ten": "Độ dốc đồ thị s theo t²", "don_vi": "m/s²", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["t̄ = sqrt(2s/g_thật) + tre_ht (đã trung bình, làm tròn 0,001 s)", "s = (g/2)·t² nên độ dốc = g/2", "g = 2·(s_cuối − s_đầu)/(t²_cuối − t²_đầu)"],
                 "gia_thiet": ["bỏ qua sức cản", "độ trễ hệ thống không đổi", "t̄ coi như đã trung bình bỏ nhiễu ngẫu nhiên"]},
     "so_lieu_mau": {"cot": ["s (m)", "t̄ (s)", "t̄² (s²)"], "hang": [[s, t, t2] for s, t, t2 in zip(S2, TB2, T2SQ)],
                     "ghi_chu": f"Số liệu minh hoạ tính từ mô hình (trễ 0,002 s). Hàng s = 0,500 khớp thí nghiệm 1. Độ dốc hai điểm xa = {SL:.4f}; hai điểm giữa = {SL2:.4f}."},
     "ket_qua_ky_vong": "Độ dốc ≈ 4,86 m/s² nên g ≈ 9,72 m/s²; năm điểm lệch đường thẳng dưới 0,004 m.",
     "hien_tuong_hay_sai": ["Vẽ s theo t (đường cong) rồi kẻ thẳng bừa.", "Quên nhân 2 sau khi tính độ dốc.", "Lấy độ dốc theo hai điểm sát nhau nên sai số lớn."],
     "sai_so_thuong_gap": "Điểm gần gốc nhạy với sai số t; độ trễ hệ thống làm đường thẳng không qua gốc chính xác.",
     "goi_y_mo_phong": {"loai": "do_thi+bang_so_lieu",
                        "y_tuong": "Bấm 'thả' ở từng độ cao, điểm (t², s) hiện dần trên đồ thị; kéo hai điểm chọn để vẽ tam giác độ dốc.",
                        "diem_nhan": "Nút 'thêm độ trễ hệ thống' làm đường thẳng lệch khỏi gốc."}},
    {**BASE, "id": "tn-l10-do-g-03",
     "ten": "Đếm khung hình: sai số dụng cụ khi dùng điện thoại quay chậm",
     "loai": "thi_nghiem", "muc_do": "co_ban",
     "kien_thuc": ["doig.sai_so_dung_cu", "doig.khung_hinh"],
     "muc_tieu": "Thấy thời gian đo bằng số khung hình bị làm tròn tới 1/fps, nên fps càng thấp thì sai số dụng cụ càng lớn.",
     "dung_cu": [{"ten": "Điện thoại quay chậm 240 khung/s", "so_luong": 1}, {"ten": "Thước dán thẳng đứng", "so_luong": 1}, {"ten": "Viên bi thép + nam châm điện", "so_luong": 1}],
     "cac_buoc": {"lam": ["Quay video chậm cảnh bi rơi từ độ cao s = 0,500 m cạnh thước.", "Đếm số khung từ lúc bi rời nam châm tới lúc bi chạm mốc s."],
                  "quan_sat": ["n = 77 khung ở 240 khung/s."],
                  "rut_ra": ["t = n/fps = 77/240 ≈ 0,321 s.", "Sai lệch 1 khung = 1/240 ≈ 0,0042 s, lớn hơn độ chia 0,001 s của đồng hồ hiện số."]},
     "tham_so": [{"ky_hieu": "fps", "ten": "Số khung hình mỗi giây", "don_vi": "khung/s", "kieu": "dieu_chinh", "min": 30, "max": 480, "mac_dinh": 240, "buoc": 30},
                 {"ky_hieu": "s", "ten": "Độ cao thả", "don_vi": "m", "kieu": "dieu_chinh", "min": 0.2, "max": 1.0, "mac_dinh": S1, "buoc": 0.05},
                 {"ky_hieu": "n", "ten": "Số khung đếm được", "don_vi": "khung", "kieu": "do_duoc", "sai_so_do": 1},
                 {"ky_hieu": "t", "ten": "Thời gian rơi", "don_vi": "s", "kieu": "tinh_ra"}],
     "mo_hinh": {"phuong_trinh": ["t_thật = sqrt(2s/9,8) + 0,002", "n = làm tròn(t_thật·fps)", "t = n/fps; sai số dụng cụ = 1/fps"],
                 "gia_thiet": ["bi rơi tự do", "độ trễ hệ thống 0,002 s như thí nghiệm 1"]},
     "so_lieu_mau": {"cot": ["fps (khung/s)", "n (khung)", "t (s)", "±1 khung (s)"], "hang": [[f, n, round(t, 4), round(e, 4)] for f, n, t, e in V3],
                     "ghi_chu": "Số liệu minh hoạ tính từ mô hình, s = 0,500 m."},
     "ket_qua_ky_vong": "Ở 240 khung/s: n = 77, t ≈ 0,321 s, sai số dụng cụ ≈ 0,0042 s; ở 30 khung/s sai số tới 0,033 s.",
     "hien_tuong_hay_sai": ["Tưởng quay chậm là hết sai số.", "Đếm khung từ lúc bi nằm sẵn trong nam châm thay vì lúc bắt đầu rời."],
     "sai_so_thuong_gap": "Khó xác định khung bi bắt đầu rời và khung chạm mốc; thước không thẳng đứng.",
     "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu",
                        "y_tuong": "Phát video giả lập từng khung, người dùng bấm khung bắt đầu và khung chạm; hiện t và ±1/fps.",
                        "diem_nhan": "Thanh trượt fps: thấy sai số dụng cụ giảm khi fps tăng."}},
]
for d in tn:
    (ROOT / "content/thi-nghiem" / f"{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
print(f"ok theory.html {len(h)} ký tự · 3 hình · {phut} phút · 3 file thí nghiệm · g1 = {GB1:.4f} ± {DG1:.4f}")
