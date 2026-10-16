"""Sinh 3 hình SVG, thay <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Chạy: python3 content/hsg9/cd12-nhiet-hoc/build_figs.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "soan-bai-ly-thuyet-tuong-tac", "scripts"))
from svg_lib import RED, BLUE, ORG, GRN, text, wrap, chevron

PHUT = 13
GRAY = "rgba(148,163,184,.25)"


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def rect(x, y, w, h, fill="none", c="currentColor", sw=2, rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'


def path(pts, c="currentColor", w=2.6):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"/>'


def rich(x, y, parts, c="currentColor", size=15, anchor="start", weight="700"):
    """Chữ có chỉ số dưới: parts = [("Q", 0), ("max", 1), (" = 0", 0)] — 1 là chỉ số dưới (cỡ 12, hạ 4)."""
    s, low = "", False
    for t, is_sub in parts:
        if is_sub and not low:
            s += f'<tspan font-size="12" dy="4">{t}</tspan>'
            low = True
        elif not is_sub and low:
            s += f'<tspan dy="-4">{t}</tspan>'
            low = False
        else:
            fs = ' font-size="12"' if is_sub else ""
            s += f'<tspan{fs}>{t}</tspan>'
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{s}</text>'


# ═════════ Hình 1: nhiệt lượng kế (mặt cắt) ═════════
b = ""
b += rect(40, 74, 180, 196, GRAY, rx=4)                       # vỏ ngoài
for y in range(84, 262, 10):                                   # chấm biểu thị lớp không khí cách nhiệt
    b += f'<circle cx="55" cy="{y}" r="1.4" fill="currentColor" opacity=".45"/>'
    b += f'<circle cx="205" cy="{y}" r="1.4" fill="currentColor" opacity=".45"/>'
b += f'<rect x="71" y="132" width="118" height="122" fill="rgba(59,130,246,.18)" stroke="none"/>'   # nước
b += line(71, 132, 189, 132, BLUE, 1.6)
b += f'<path d="M70,96 L70,254 L190,254 L190,96" fill="none" stroke="currentColor" stroke-width="2.4"/>'   # cốc nhôm
b += f'<rect x="58" y="254" width="144" height="8" fill="currentColor" opacity=".35"/>'                 # đế kê cách nhiệt
b += rect(34, 62, 192, 12, "rgba(148,163,184,.45)", rx=2)    # nắp
b += rect(148, 218, 34, 26, "rgba(234,88,12,.35)", ORG, 2, 3)  # miếng kim loại
# nhiệt kế
b += rect(123, 22, 10, 208, "rgba(255,255,255,.04)", "currentColor", 1.6, 5)
b += f'<circle cx="128" cy="234" r="8" fill="{RED}" stroke="currentColor" stroke-width="1.6"/>'
b += line(128, 228, 128, 120, RED, 3)
# que khuấy: thanh đứng + vòng ngang ở đáy
b += line(92, 26, 92, 240, "currentColor", 2.4)
b += f'<ellipse cx="96" cy="240" rx="16" ry="5" fill="none" stroke="currentColor" stroke-width="2"/>'
b += text(92, 18, "que khuấy", "currentColor", 15, "middle", "700")
b += text(140, 18, "nhiệt kế", RED, 15, "start", "700")
# nhãn bên phải, mỗi nhãn một dòng, có đường dẫn
LX = 252
for ty, tx, tyy, lab, col in [
        (68, 226, 68, "nắp", "currentColor"),
        (108, 190, 108, "cốc nhôm", "currentColor"),
        (150, 206, 150, "lớp không khí", "currentColor"),
        (190, 176, 190, "nước", BLUE),
        (231, 182, 231, "miếng kim loại", ORG),
        (266, 220, 266, "vỏ ngoài", "currentColor")]:
    b += line(tx, tyy, LX - 4, ty, "currentColor", 1.2, "", .7)
    b += text(LX, ty + 5, lab, col, 15, "start", "700")
fig1 = wrap("0 0 400 284", "Mặt cắt nhiệt lượng kế: vỏ ngoài, lớp không khí, cốc nhôm chứa nước, nắp, nhiệt kế, que khuấy và miếng kim loại thả trong nước",
            b, "Hình 1. Nhiệt lượng kế. Cốc nhôm cũng thu nhiệt nên phải tính vào phương trình.<br>Lớp không khí và nắp giảm trao đổi nhiệt với bên ngoài.")

# ═════════ Hình 2: đồ thị T–τ đun nước đá từ −30 °C tới sôi ═════════
# Đơn vị thời gian u: thời gian đun nước lỏng 0→100 °C = 100u (cùng m, cùng P).
CN, CD, LAM, L = 4200, 2100, 3.4e5, 2.3e6
uAB = 100 * CD * 30 / (CN * 100)        # 15
uBC = 100 * LAM / (CN * 100)            # ≈ 81
uCD = 100.0
uDE = 100 * L / (CN * 100)              # ≈ 548 → vẽ cắt
assert abs(uAB - 15) < 1e-9 and 80 < uBC < 82 and uDE > 500
X0, XAX = 64, 384                        # gốc trục và mút trục τ
DE_PX = 74                              # đoạn DE vẽ cắt
S = (XAX - 12 - X0 - DE_PX) / (uAB + uBC + uCD)


def Y(T):
    return 196 - 1.4 * T


YAX = 252
A = (X0, Y(-30))
B = (A[0] + uAB * S, Y(0))
C = (B[0] + uBC * S, Y(0))
D = (C[0] + uCD * S, Y(100))
E = (D[0] + DE_PX, Y(100))
# kiểm tỉ lệ độ dốc: AB dốc gấp đôi CD (c đá = c nước / 2)
kAB = (A[1] - B[1]) / (B[0] - A[0])
kCD = (C[1] - D[1]) / (D[0] - C[0])
assert abs(kAB / kCD - CN / CD) < 1e-6, (kAB, kCD)
b = ""
b += line(X0, YAX, XAX, YAX, "currentColor", 1.8) + chevron(XAX, YAX, 1, 0, "currentColor", 1.8, 10)
b += line(X0, YAX, X0, 34, "currentColor", 1.8) + chevron(X0, 34, 0, -1, "currentColor", 1.8, 10)
b += text(X0 + 8, 38, "t (°C)", "currentColor", 15, "start", "700")
b += text(XAX, YAX + 22, "τ", "currentColor", 16, "end", "700")
for T in (-30, 0, 100):
    b += line(X0 - 5, Y(T), X0, Y(T), "currentColor", 1.6)
    b += text(X0 - 8, Y(T) + 5, "−30" if T < 0 else str(T), "currentColor", 15, "end", "600")
b += line(X0, Y(0), B[0], Y(0), "currentColor", 1.2, "4 4", .6)
b += line(X0, Y(100), D[0], Y(100), "currentColor", 1.2, "4 4", .6)
# đường đồ thị, DE có chỗ cắt
XB1 = D[0] + DE_PX * 0.45
b += path([A, B, C, D, (XB1 - 4, Y(100))], RED, 2.8)
b += line(XB1 + 4, Y(100), E[0], Y(100), RED, 2.8)
for dx in (-4, 4):                       # dấu cắt "//" trên đoạn DE và trên trục τ
    b += line(XB1 + dx - 4, Y(100) + 8, XB1 + dx + 4, Y(100) - 8, "currentColor", 1.6)
    b += line(XB1 + dx - 4, YAX + 8, XB1 + dx + 4, YAX - 8, "currentColor", 1.6)
for (px, py), lab, dx, dy in [(A, "A", 12, 4), (B, "B", -2, -10), (C, "C", 2, -10), (D, "D", -4, -10), (E, "E", 0, -10)]:
    b += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.4" fill="currentColor"/>'
    b += text(round(px + dx, 1), round(py + dy, 1), lab, "currentColor", 15, "middle", "700")
# chú giải dưới trục: mỗi đoạn một dòng
LY = YAX + 46
for i, s in enumerate(["AB: nước đá nóng lên", "BC: nước đá tan", "CD: nước nóng lên", "DE: nước sôi (vẽ cắt bớt)"]):
    b += text(X0 - 40, LY + 22 * i, s, "currentColor", 15, "start", "600")
b += text(XAX, 232, "nguồn cấp nhiệt đều", "currentColor", 15, "end", "600")
fig2 = wrap("0 14 400 368", "Đồ thị nhiệt độ theo thời gian khi đun nước đá từ âm 30 độ C tới sôi: đoạn dốc AB, đoạn ngang BC ở 0 độ, đoạn dốc CD, đoạn ngang DE ở 100 độ",
            b, "Hình 2. Đun đều một khối nước đá tới sôi.<br>Đoạn dốc: một thể, nhiệt độ tăng.<br>Đoạn ngang: đang chuyển thể, nhiệt độ đứng yên.")

# ═════════ Hình 3: thang biện luận 4 khả năng khi thả đá vào nước ═════════
AX = 112
YS = {"m1": 240, "q1": 172, "q2": 104}       # ba mốc, từ dưới lên
b = ""
b += line(AX, 306, AX, 30, "currentColor", 2) + chevron(AX, 30, 0, -1, "currentColor", 2, 10)
b += rich(AX + 8, 30, [("Q", 0), ("max", 1), (" tăng", 0)], "currentColor", 15)
b += rich(AX - 10, YS["q2"] + 5, [("Q", 0), ("2", 1)], ORG, 15, "end")
b += rich(AX - 10, YS["q1"] + 5, [("Q", 0), ("1", 1)], GRN, 15, "end")
b += rich(AX - 10, YS["m1"] + 5, [("Q", 0), ("1", 1), (" − λm", 0), ("n", 1)], BLUE, 15, "end")
for k, col in (("q2", ORG), ("q1", GRN), ("m1", BLUE)):
    b += line(AX - 6, YS[k], 392, YS[k], col, 1.6, "5 4")
bands = [(40, YS["q2"], "Đá tan hết", [("t", 0), ("cb", 1), (" &gt; 0 °C", 0)], RED),
         (YS["q2"], YS["q1"], "Đá tan một phần", [("t", 0), ("cb", 1), (" = 0 °C", 0)], ORG),
         (YS["q1"], YS["m1"], "Nước đông một phần", [("t", 0), ("cb", 1), (" = 0 °C", 0)], GRN),
         (YS["m1"], 306, "Nước đông hết", [("t", 0), ("cb", 1), (" &lt; 0 °C", 0)], BLUE)]
for y0, y1, t1, t2, col in bands:
    cy = (y0 + y1) / 2
    b += text(AX + 16, round(cy - 6, 1), t1, col, 16, "start", "700")
    b += rich(AX + 16, round(cy + 16, 1), t2, "currentColor", 15, "start", "600")
fig3 = wrap("0 12 400 304", "Thang so sánh nhiệt lượng Q max nước toả khi về 0 độ với ba mốc Q1 trừ lambda m nước, Q1 và Q2, chia thành bốn khả năng của trạng thái cuối",
            b, "Hình 3. So Q<sub>max</sub> với các mốc để biết trạng thái cuối.<br>Q<sub>max</sub>: nước nguội về 0 °C.<br>Q<sub>1</sub>: đá ấm lên tới 0 °C.<br>Q<sub>2</sub> = Q<sub>1</sub> + λm<sub>đ</sub>: đá tan hết (m<sub>đ</sub>: khối lượng đá).<br>Q<sub>1</sub> − λm<sub>n</sub>: dưới mốc này, nước đông hết (m<sub>n</sub>: khối lượng nước).")

# ═════════ ghi theory.html ═════════
src = open(os.path.join(HERE, "theory.src.html"), encoding="utf8").read()
for n, f in ((1, fig1), (2, fig2), (3, fig3)):
    assert f"<!--FIG{n}-->" in src, n
    src = src.replace(f"<!--FIG{n}-->", f)
src = src.replace("__PHUT__", str(PHUT))
open(os.path.join(HERE, "theory.html"), "w", encoding="utf8").write(src)
print("ok", len(src))
