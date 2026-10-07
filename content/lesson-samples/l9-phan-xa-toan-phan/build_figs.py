"""Sinh 4 hình SVG cho bài 'Phản xạ toàn phần' (KHTN 9, lesson_id 84) và thay mốc <!--FIGn--> trong theory.src.html -> theory.html.
Mọi tia sáng tính bằng định luật khúc xạ n1·sin i = n2·sin r; mũi tên tia sáng là chữ V 30° (chevron).
Chạy: python3 build_figs.py  (từ thư mục bài)."""
import math, re, pathlib
from svg_lib import RED, BLUE, ORG, GRN, chevron, wrap

HERE = pathlib.Path(__file__).resolve().parent
PHUT = "16"            # số phút đọc theo lint_do_dai.py (cập nhật sau mỗi lần sửa chữ)

FS, FSUB = 17, 13        # cỡ chữ SVG (viewBox ~420) và chỉ số dưới

def vn(x, d=1): return f"{x:.{d}f}".replace(".", "{,}")
def deg(a): return math.radians(a)
def asin_d(x): return math.degrees(math.asin(x))

def T(x, y, s, c="currentColor", size=FS, anchor="start", weight="600"):
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{s}</text>'

def sub(base, s, tail=""):
    return f'{base}<tspan baseline-shift="sub" font-size="{FSUB}">{s}</tspan>{tail}'

def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

def ray(x1, y1, x2, y2, c, w=2.6, op=1, at=0.55):
    """Tia sáng: đoạn thẳng + đầu V 30° đặt ở giữa đoạn, chỉ chiều truyền."""
    mx, my = x1 + (x2 - x1) * at, y1 + (y2 - y1) * at
    return (f'<g opacity="{op}">' + line(x1, y1, x2, y2, c, w)
            + chevron(mx, my, x2 - x1, y2 - y1, c, w, 12) + '</g>')

def normal(x, y1, y2):
    return line(x, y1, x, y2, "currentColor", 1.6, "6 5", .75)

def arc(cx, cy, r, a1, a2, c="currentColor", w=1.6):
    """Cung tròn; góc đo theo toạ độ màn hình (độ, 0 = sang phải, 90 = xuống dưới)."""
    p1 = (cx + r * math.cos(deg(a1)), cy + r * math.sin(deg(a1)))
    p2 = (cx + r * math.cos(deg(a2)), cy + r * math.sin(deg(a2)))
    large = 1 if abs(a2 - a1) > 180 else 0
    sweep = 1 if a2 > a1 else 0
    return f'<path d="M{p1[0]:.1f},{p1[1]:.1f} A{r},{r} 0 {large} {sweep} {p2[0]:.1f},{p2[1]:.1f}" fill="none" stroke="{c}" stroke-width="{w}"/>'

GLASS = 'fill="rgba(56,189,248,.12)" stroke="currentColor" stroke-width="2"'
WATER = 'fill="rgba(56,189,248,.12)"'

# ------------------------------------------------------------ Hình 1: khối bán trụ, i = 30°, n = 1,5
n_tt = 1.5
i1 = 30
r1 = asin_d(n_tt * math.sin(deg(i1)))          # 48,59°
Ix, Iy, R = 200, 150, 110
b = ""
# vòng chia độ: vòng nét đứt + vạch mỗi 10°
b += f'<circle cx="{Ix}" cy="{Iy}" r="128" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="3 5" opacity=".55"/>'
for k in range(36):
    a = deg(k * 10)
    L = 10 if k % 3 == 0 else 6
    b += line(Ix + 128 * math.cos(a), Iy + 128 * math.sin(a), Ix + (128 + L) * math.cos(a), Iy + (128 + L) * math.sin(a), "currentColor", 1.2, "", .55)
# khối bán trụ: nửa dưới, mặt phẳng nằm ngang qua I
b += f'<path d="M{Ix-R},{Iy} A{R},{R} 0 0 0 {Ix+R},{Iy} Z" {GLASS}/>'
b += normal(Ix, Iy - 125, Iy + 125)
# tia tới: từ đèn laser (phía dưới bên trái), theo bán kính tới I
sx, sy = Ix - 170 * math.sin(deg(i1)), Iy + 170 * math.cos(deg(i1))
b += line(sx - 26 * math.sin(deg(i1)), sy + 26 * math.cos(deg(i1)), sx, sy, "currentColor", 9, "", .8)  # thân bút laser
b += ray(sx, sy, Ix, Iy, RED, 2.8)
# tia khúc xạ ra không khí (r tính từ định luật khúc xạ)
L = 125
b += ray(Ix, Iy, Ix + L * math.sin(deg(r1)), Iy - L * math.cos(deg(r1)), BLUE, 2.6)
# tia phản xạ mờ trong thủy tinh (góc phản xạ = góc tới)
b += ray(Ix, Iy, Ix + L * math.sin(deg(i1)), Iy + L * math.cos(deg(i1)), ORG, 2, .5)
# cung góc
b += arc(Ix, Iy, 42, 90, 90 + i1) + T(Ix - 58 * math.sin(deg(i1 / 2)), Iy + 58 * math.cos(deg(i1 / 2)) + 6, "i", anchor="middle")
b += arc(Ix, Iy, 42, -90, -90 + r1, BLUE) + T(Ix + 60 * math.sin(deg(r1 / 2)), Iy - 60 * math.cos(deg(r1 / 2)) + 6, "r", BLUE, anchor="middle")
b += T(Ix - 8, Iy - 8, "I", anchor="end", weight="700")
b += T(Ix + 8, Iy - 108, "N", weight="700")
b += T(12, 34, "không khí")
b += T(Ix + L * math.sin(deg(r1)) + 6, Iy - L * math.cos(deg(r1)) + 4, "tia khúc xạ", BLUE)
b += T(Ix + L * math.sin(deg(i1)) + 6, Iy + L * math.cos(deg(i1)) + 22, "tia phản xạ", ORG)
b += T(sx - 34, sy + 30, "laser", anchor="end")
b += line(Ix - 60, Iy + 60, 50, 228, "currentColor", 1.2, "", .7) + T(12, 248, "thủy tinh")
fig1 = wrap("0 0 420 330", f"Khối bán trụ thủy tinh trên vòng chia độ; tia laser tới tâm I với góc tới 30 độ, tia khúc xạ ló ra với góc 48,6 độ, tia phản xạ mờ",
            b, "Hình 1. Tia laser vào mặt cong theo bán kính nên đi thẳng tới tâm I, không bị gãy.<br>"
               f"Với $i = {i1}^\\circ$ ($n = 1{{,}}5$): tia khúc xạ ló ra với $r \\approx {vn(r1)}^\\circ$.<br>"
               + "Tia phản xạ còn mờ.")

# ------------------------------------------------------------ Hình 2: i = i_th và i = 60°
ith_tt = asin_d(1 / n_tt)                     # 41,81°
def panel(oy, i, grazing):
    Ix, Iy = 210, oy + 80
    g = f'<rect x="20" y="{Iy}" width="380" height="95" {WATER}/>' + line(20, Iy, 400, Iy, "currentColor", 2)
    g += normal(Ix, oy + 14, oy + 176)
    Ls = 90 / math.cos(deg(i))
    sx, sy = Ix - Ls * math.sin(deg(i)), Iy + Ls * math.cos(deg(i))
    g += ray(sx, sy, Ix, Iy, RED, 2.8)
    g += ray(Ix, Iy, Ix + Ls * math.sin(deg(i)), Iy + Ls * math.cos(deg(i)), ORG, 2.8, 1 if not grazing else .85)
    if grazing:
        g += ray(Ix, Iy - 3, 395, Iy - 3, BLUE, 1.8, .45, .7)
        g += T(395, Iy - 12, "r = 90°", BLUE, anchor="end")
    g += arc(Ix, Iy, 36, 90, 90 + i) + T(Ix - 52 * math.sin(deg(i / 2)), Iy + 52 * math.cos(deg(i / 2)) + 6, "i", anchor="middle")
    g += T(30, Iy + 26, "thủy tinh") + T(30, Iy - 14, "không khí")
    return g
b = panel(0, ith_tt, True)
b += T(20, 30, sub("i = i", "th", f" ≈ {ith_tt:.0f}°"), weight="700")
b += line(10, 190, 410, 190, "currentColor", 1, "2 4", .5)
b += panel(190, 60, False)
b += T(20, 220, sub("i = 60° &gt; i", "th"), weight="700")
b += T(400, 220, "chỉ còn tia phản xạ", ORG, anchor="end")
fig2 = wrap("0 0 420 380", "Hai trường hợp: góc tới bằng góc tới hạn, tia khúc xạ đi sát mặt phân cách; góc tới 60 độ, chỉ còn tia phản xạ",
            b, f"Hình 2. Trên: $i = i_{{th}} \\approx {vn(ith_tt)}^\\circ$" + ", tia khúc xạ rất mờ, đi sát mặt phân cách.<br>"
               "Dưới: $i = 60^\\circ$, chỉ còn tia phản xạ, sáng gần bằng tia tới.")

# ------------------------------------------------------------ Hình 3: sợi quang (chiết suất minh hoạ 1,50 / 1,20)
n_loi, n_vo = 1.50, 1.20
ith_q = asin_d(n_vo / n_loi)                 # 53,13°
iq = 65                                      # góc tới tại thành sợi
th = 90 - iq                                 # góc với trục sợi = 25°
top, bot = 100, 170
b = f'<rect x="20" y="75" width="380" height="120" rx="6" fill="rgba(148,163,184,.14)" stroke="currentColor" stroke-width="1.6"/>'
b += f'<rect x="20" y="{top}" width="380" height="{bot-top}" fill="rgba(56,189,248,.16)"/>'
b += line(20, top, 400, top, "currentColor", 1.6) + line(20, bot, 400, bot, "currentColor", 1.6)
# đường gấp khúc của tia: bắt đầu ở mặt đầu sợi (x=20, y=150), đi lên theo góc th với trục
k = math.tan(deg(th))
pts = [(20.0, 150.0)]
x, y, up = 20.0, 150.0, True
while True:
    yt = top if up else bot
    xn = x + abs(y - yt) / k
    if xn >= 400:
        pts.append((400.0, y - (400 - x) * k if up else y + (400 - x) * k)); break
    pts.append((xn, yt)); x, y, up = xn, yt, not up
for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
    b += ray(x1, y1, x2, y2, RED, 2.6)
bx, by = pts[1]
b += normal(bx, by, by + 52)
b += arc(bx, by, 30, 90, 90 + iq) + T(bx - 46 * math.sin(deg(iq / 2)), by + 46 * math.cos(deg(iq / 2)) + 6, "i", anchor="middle")
b += line(300, 88, 318, 50, "currentColor", 1.2, "", .7) + T(318, 44, sub("vỏ n", "2", " = 1,20"), anchor="middle")
b += line(330, 160, 318, 216, "currentColor", 1.2, "", .7) + T(318, 236, sub("lõi n", "1", " = 1,50"), anchor="middle")
b += T(24, 214, "ánh sáng vào") + line(40, 196, 26, 156, "currentColor", 1.2, "", .7)
fig3 = wrap("0 0 420 250", "Sợi quang: tia sáng trong lõi phản xạ toàn phần liên tiếp tại mặt lõi và vỏ",
            b, "Hình 3. Chiết suất minh hoạ: lõi 1,50, vỏ 1,20 (sợi thật chỉ chênh vài phần trăm).<br>"
               f"Mỗi lần chạm thành: $i = {iq}^\\circ \\gt i_{{th}} \\approx {vn(ith_q)}^\\circ$" + ", nên phản xạ toàn phần.")

# ------------------------------------------------------------ Hình 4: đèn đáy bể, tia 40° và 60° (lời giải bài toán mẫu)
n_nuoc = 1.33
ith_n = asin_d(1 / n_nuoc)                    # 48,75°
Sy, lx, ly = 110, 40, 270
b = f'<rect x="0" y="{Sy}" width="420" height="190" {WATER}/>' + line(0, Sy, 420, Sy, "currentColor", 2)
b += f'<circle cx="{lx}" cy="{ly}" r="7" fill="{ORG}"/>' + T(lx + 14, ly + 22, "đèn")
# tia 40°
ia = 40; ra = asin_d(n_nuoc * math.sin(deg(ia)))   # 58,75°
ha = lx + (ly - Sy) * math.tan(deg(ia))
b += normal(ha, 30, 205)
b += ray(lx, ly, ha, Sy, RED, 2.6)
b += ray(ha, Sy, ha + 90 * math.tan(deg(ra)), Sy - 90, BLUE, 2.6)
b += ray(ha, Sy, ha + 42 * math.tan(deg(ia)), Sy + 42, ORG, 1.8, .45, .5)
b += arc(ha, Sy, 34, 90, 90 + ia) + T(ha - 62 * math.sin(deg(ia / 2)), Sy + 62 * math.cos(deg(ia / 2)) + 6, "40°", anchor="middle")
b += arc(ha, Sy, 34, -90, -90 + ra, BLUE) + T(ha + 58 * math.sin(deg(ra / 2)), Sy - 58 * math.cos(deg(ra / 2)) + 6, f"{ra:.1f}°".replace(".", ","), BLUE, anchor="middle")
b += T(ha + 90 * math.tan(deg(ra)) + 6, Sy - 80, "ló ra", BLUE)
# tia 60°
ib = 60
hb = lx + (ly - Sy) * math.tan(deg(ib))
b += normal(hb, 50, 172)
b += ray(lx, ly, hb, Sy, RED, 2.6)
ex = 412; b += ray(hb, Sy, ex, Sy + (ex - hb) / math.tan(deg(ib)), ORG, 2.6)
b += arc(hb, Sy, 34, 90, 90 + ib) + T(hb - 62 * math.sin(deg(ib / 2)), Sy + 62 * math.cos(deg(ib / 2)) + 6, "60°", anchor="middle")
b += T(412, 200, "phản xạ toàn phần", ORG, anchor="end")
b += T(12, 40, "không khí") + T(12, 146, "nước") + T(12, 168, "n = 1,33")
fig4 = wrap("0 0 420 300", "Đèn dưới đáy bể: tia tới 40 độ ló ra với góc 58,7 độ; tia tới 60 độ phản xạ toàn phần",
            b, f"Hình 4. Tia $40^\\circ$ ló ra với $r \\approx {vn(ra)}^\\circ$" + " (kèm tia phản xạ mờ).<br>"
               "Tia $60^\\circ$ phản xạ toàn phần.")

# ------------------------------------------------------------ ghép
h = (HERE / "theory.src.html").read_text(encoding="utf8")
assert "__PHUT__" in h
h = h.replace("__PHUT__", PHUT)
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", f)
(HERE / "theory.html").write_text(h, encoding="utf8")
print("ok", len(h), f"r1={r1:.2f} ith_tt={ith_tt:.2f} ith_q={ith_q:.2f} ith_n={ith_n:.2f} ra={ra:.2f}")
