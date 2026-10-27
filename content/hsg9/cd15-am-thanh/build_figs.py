"""Sinh 4 hình SVG, thay <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Chạy: python3 content/hsg9/cd15-am-thanh/build_figs.py"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "soan-bai-ly-thuyet-tuong-tac", "scripts"))
from svg_lib import RED, BLUE, ORG, GRN, text, wrap, chevron, arrow

PHUT = 16


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def path(pts, c="currentColor", w=2.4):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"/>'


def dim(x1, x2, y, c, label, ly):
    """Đường kích thước hai đầu mũi tên + nhãn giữa."""
    b = line(x1, y, x2, y, c, 1.8)
    b += chevron(x1, y, -1, 0, c, 1.8, 9) + chevron(x2, y, 1, 0, c, 1.8, 9)
    b += line(x1, y - 7, x1, y + 7, c, 1.6) + line(x2, y - 7, x2, y + 7, c, 1.6)
    return b + text((x1 + x2) / 2, ly, label, c, 15, "middle", "700")


# ═════════ Hình 1: loa và các lớp khí nén – dãn (sóng dọc) ═════════
LAM, X0, X1 = 120, 84, 424           # bước sóng 120 px; vùng khí từ 84 đến 424
AK = 0.75                            # a·k: độ nén lớn nhất
A = AK * LAM / (2 * math.pi)
b = ""
# loa: hộp + màng
b += f'<rect x="16" y="66" width="34" height="72" rx="3" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2"/>'
b += f'<path d="M50,78 L74,56 L74,148 L50,126 Z" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2"/>'
b += text(14, 164, "loa", "currentColor", 16, "start", "700")
xs = []
x0 = X0
while x0 <= X1:
    xs.append(x0 + A * math.sin(2 * math.pi * (x0 - X0) / LAM))
    x0 += 6
for x in xs:
    if X0 - 2 <= x <= X1 + 2:
        b += line(x, 62, x, 142, BLUE, 2)
# chỗ nén: x0 - X0 = λ/2 + nλ (dx/dx0 nhỏ nhất); chỗ dãn: x0 - X0 = nλ
nen = [X0 + LAM / 2 + n * LAM for n in range(3)]
for xc in nen:
    i = min(range(len(xs)), key=lambda j: abs(xs[j] - xc))
    assert abs(xs[i] - xc) < 0.01   # vạch giữa chỗ nén nằm đúng tâm
d_nen = min(abs(xs[i + 1] - xs[i]) for i in range(len(xs) - 1))
d_dan = max(abs(xs[i + 1] - xs[i]) for i in range(len(xs) - 1))
assert d_nen < 2 and d_dan > 10, (d_nen, d_dan)
b += text(nen[0], 52, "nén", ORG, 15, "middle", "700")
b += text(X0 + LAM, 52, "dãn", GRN, 15, "middle", "700")
b += text(nen[1], 52, "nén", ORG, 15, "middle", "700")
b += text(X0 + 2 * LAM, 52, "dãn", GRN, 15, "middle", "700")
b += dim(nen[0], nen[1], 166, RED, "λ", 186)
# phương truyền + phương dao động của lớp khí
b += arrow("", "o", 300, 214, 400, 214, 2.4)
b += text(296, 219, "phương truyền", "currentColor", 16, "end", "600")
b += line(342, 242, 382, 242, BLUE, 2.4) + chevron(382, 242, 1, 0, BLUE, 2.4, 9) + chevron(342, 242, -1, 0, BLUE, 2.4, 9)
b += text(296, 247, "lớp khí dao động", "currentColor", 16, "end", "600")
fig1 = wrap("0 30 440 228", "Loa đẩy các lớp khí thành chỗ nén và chỗ dãn xen kẽ, bước sóng là khoảng cách hai chỗ nén liền nhau, lớp khí dao động dọc theo phương truyền",
            b, "Hình 1. Chỗ nén và chỗ dãn nối tiếp nhau đi ra xa loa. Lớp khí dao động dọc theo phương truyền: sóng dọc.")

# ═════════ Hình 2: đồ thị dao động hai âm, trục thời gian 0–4 ms ═════════
PX0, PX1, TMAX = 64, 424, 4.0
SX = (PX1 - PX0) / TMAX              # 90 px / ms
U = 16                               # 1 ô li độ = 16 px
panels = [(76, 2, 2.0, RED, "Âm 1"), (196, 1, 1.0, BLUE, "Âm 2")]   # (tâm y, biên độ ô, T ms, màu, tên)
b = ""
for cy, amp, T, col, name in panels:
    top, bot = cy - 2 * U - 8, cy + 2 * U + 8
    for k in range(9):                                   # vạch dọc mỗi 0,5 ms
        x = PX0 + k * 0.5 * SX
        b += line(x, top, x, bot, "currentColor", 1, "", .28 if k % 2 else .45)
    for j in (-2, -1, 1, 2):                             # vạch ngang mỗi 1 ô
        b += line(PX0, cy + j * U, PX1, cy + j * U, "currentColor", 1, "", .28)
    b += line(PX0, cy, PX1 + 6, cy, "currentColor", 1.6)          # trục t
    b += line(PX0, top, PX0, bot, "currentColor", 1.6)             # trục li độ
    pts = [(PX0 + t * SX, cy - amp * U * math.sin(2 * math.pi * t / T)) for t in [i * TMAX / 400 for i in range(401)]]
    b += path(pts, col, 2.6)
    # kiểm: đỉnh đầu tiên tại t = T/4, cao đúng amp ô
    tp = T / 4
    assert abs(min(p[1] for p in pts) - (cy - amp * U)) < 0.5
    b += text(12, cy + 5, name, col, 15, "start", "700")
    b += text(PX0 - 6, cy - 2 * U + 4, "+2", "currentColor", 15, "end", "600")
    b += text(PX0 - 6, cy + 2 * U + 4, "−2", "currentColor", 15, "end", "600")
for k in range(5):
    x = PX0 + k * SX
    b += text(x, 262, str(k), "currentColor", 15, "middle", "600")
b += text(PX1, 282, "t (ms)", "currentColor", 15, "end", "600")
b += text(PX0, 282, "1 ô ngang = 0,5 ms", "currentColor", 15, "start", "600")
fig2 = wrap("0 28 440 262", "Đồ thị dao động của hai âm trong 4 mili giây: âm 1 biên độ 2 ô, chu kì 2 ms; âm 2 biên độ 1 ô, chu kì 1 ms",
            b, "Hình 2. Đồ thị dao động của hai âm, cùng trục thời gian. Mỗi ô ngang 0,5 ms, mỗi ô dọc là một đơn vị li độ.")

# ═════════ Hình 3: tàu đo độ sâu bằng tiếng vang ═════════
SEA, FLOOR = 74, 236
b = ""
b += line(10, SEA, 430, SEA, BLUE, 2)
b += text(424, SEA - 8, "mặt biển", BLUE, 15, "end", "600")
# thân tàu
b += f'<path d="M70,{SEA-18} L190,{SEA-18} L176,{SEA+8} L84,{SEA+8} Z" fill="rgba(148,163,184,.3)" stroke="currentColor" stroke-width="2"/>'
b += f'<rect x="110" y="{SEA-38}" width="42" height="20" rx="2" fill="rgba(148,163,184,.3)" stroke="currentColor" stroke-width="2"/>'
# đáy biển + gạch
b += line(10, FLOOR, 430, FLOOR, "currentColor", 2.6)
for x in range(14, 430, 16):
    b += line(x, FLOOR, x - 9, FLOOR + 10, "currentColor", 1.3, "", .55)
b += text(12, FLOOR + 30, "đáy biển", "currentColor", 15, "start", "600")
# tia phát (đỏ, đi xuống) và tia phản xạ (xanh lá, đi lên)
b += arrow("", "r", 116, SEA + 12, 116, FLOOR - 4, 2.6)
b += arrow("", "g", 146, FLOOR - 4, 146, SEA + 12, 2.6)
b += text(108, 150, "phát", RED, 16, "end", "700")
b += text(156, 150, "thu", GRN, 16, "start", "700")
# kích thước d
b += line(250, SEA, 250, FLOOR, ORG, 1.8) + chevron(250, SEA, 0, -1, ORG, 1.8, 9) + chevron(250, FLOOR, 0, 1, ORG, 1.8, 9)
b += text(262, 150, "d = ?", ORG, 16, "start", "700")
b += text(262, 120, "nước: v = 1500 m/s", "currentColor", 15, "start", "600")
b += text(262, 182, "t: thời gian đi và về", "currentColor", 15, "start", "600")
b += text(262, 202, "d = v·t / 2", ORG, 16, "start", "700")
fig3 = wrap("0 28 440 248", "Tàu phát siêu âm xuống đáy biển và thu âm phản xạ, độ sâu bằng tốc độ nhân thời gian chia hai",
            b, "Hình 3. Âm đi xuống rồi dội lên, đi hai lần độ sâu d. Nên d = vt/2.")

# ═════════ Hình 4: xe bóp còi tiến về vách (đúng tỉ lệ bài toán mẫu) ═════════
V, VX, T4 = 340, 20, 4
D = (V + VX) * T4 / 2                 # 720 m
D2 = D - VX * T4                      # 640 m
assert (D, D2) == (720, 640)
K = 0.45                              # px / m
XW = 412                              # mặt vách
XA, XB = XW - K * D, XW - K * D2
GROUND = 196


def car(x, op=1.0):
    """Ô tô nhỏ, tâm x; op < 1 là vị trí lúc sau (vẽ mờ)."""
    s = f'<g opacity="{op}">'
    s += f'<rect x="{x-14:.1f}" y="{GROUND-18}" width="28" height="11" rx="2" fill="rgba(148,163,184,.35)" stroke="currentColor" stroke-width="1.8"/>'
    s += f'<path d="M{x-8:.1f},{GROUND-18} L{x-4:.1f},{GROUND-25} L{x+6:.1f},{GROUND-25} L{x+10:.1f},{GROUND-18}" fill="none" stroke="currentColor" stroke-width="1.8"/>'
    s += f'<circle cx="{x-8:.1f}" cy="{GROUND-5}" r="4" fill="currentColor"/><circle cx="{x+8:.1f}" cy="{GROUND-5}" r="4" fill="currentColor"/>'
    return s + "</g>"


b = line(10, GROUND, XW, GROUND, "currentColor", 2)
b += f'<rect x="{XW}" y="40" width="20" height="{GROUND-40}" fill="rgba(148,163,184,.3)" stroke="currentColor" stroke-width="2"/>'
for y in range(48, GROUND, 14):
    b += line(XW + 2, y + 8, XW + 18, y, "currentColor", 1.2, "", .5)
b += text(XW - 4, 34, "vách núi", "currentColor", 15, "end", "700")
b += car(XA) + car(XB, .5)
b += text(XA, GROUND - 32, "A", "currentColor", 16, "middle", "700")
b += text(XB + 2, GROUND - 32, "B", "currentColor", 16, "middle", "700")
# âm đi tới vách và âm dội về B
YA, YR = 84, 124
b += arrow("", "r", XA, YA, XW - 2, YA, 2.4)
b += text((XA + XW) / 2, YA - 9, "âm đi tới vách", RED, 16, "middle", "700")
b += line(XW - 2, YA, XW - 2, YR, "currentColor", 1.2, "4 3", .6)
b += arrow("", "g", XW - 2, YR, XB, YR, 2.4)
b += text((XB + XW) / 2, YR - 9, "âm dội về gặp xe", GRN, 16, "middle", "700")
b += line(XA, YA, XA, GROUND - 50, "currentColor", 1, "4 3", .5) + line(XB, YR, XB, GROUND - 50, "currentColor", 1, "4 3", .5)
# kích thước dưới mặt đất
b += dim(XA, XB, 214, ORG, "", 0)
b += text(XB + 12, 219, "xe đi: s = vₓt", ORG, 16, "start", "700")
b += dim(XA, XW, 240, "currentColor", "", 0)
b += text((XA + XW) / 2, 258, "d: lúc bóp còi (xe ở A)", "currentColor", 16, "middle", "600")
b += dim(XB, XW, 272, BLUE, "", 0)
b += text((XB + XW) / 2, 290, "d′: lúc nghe (xe ở B)", BLUE, 16, "middle", "600")
fig4 = wrap("0 22 440 276", "Xe bóp còi ở A, âm đi tới vách rồi dội về gặp xe ở B; quãng âm đi cộng quãng xe đi bằng hai lần khoảng cách d",
            b, "Hình 4. Vẽ đúng tỉ lệ số liệu bài toán mẫu.<br>Âm đi + xe đi = 2d.")

# ═════════ ghi theory.html ═════════
src = open(os.path.join(HERE, "theory.src.html"), encoding="utf8").read()
for n, f in ((1, fig1), (2, fig2), (3, fig3), (4, fig4)):
    assert f"<!--FIG{n}-->" in src, n
    src = src.replace(f"<!--FIG{n}-->", f)
src = src.replace("__PHUT__", str(PHUT))
open(os.path.join(HERE, "theory.html"), "w", encoding="utf8").write(src)
print("ok", len(src))
