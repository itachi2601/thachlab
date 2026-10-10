"""Hình cho bài tập mẫu Bài 7 (Vật lí 12) "Phương trình trạng thái của khí lí tưởng", lesson_id 8.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mọi chuyển động tính từ số liệu của đề (kim áp kế quay tuyến tính theo p ∝ T, pit-tông theo V, đường đẳng tích thẳng qua O,
phân tử phản xạ đàn hồi ở thành bình), không để lộ đáp số."""
import math, os, random, re as _re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"


# ───────────── tiện ích ─────────────
def R(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}"{d} opacity="{op}"/>')

def circ(x, y, r, c="currentColor", sw=2, fill="none"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'

def rich(s, size=13):
    """`p_N` → p với chỉ số dưới N (tspan hạ dòng rồi trả lại)."""
    parts = _re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
    return out

def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)

def rot(cx, cy, dphi, dur, inner):
    """Nhóm quay quanh (cx,cy) góc dphi độ (dương = cùng chiều kim đồng hồ), đều theo thời gian; chạy một lần khi bấm."""
    return (f'<g><animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};{dphi:.1f} {cx} {cy}" '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>{inner}</g>')

def phi(p, pmax):
    """Góc kim (độ, cùng chiều kim đồng hồ tính từ phương thẳng đứng hướng lên): 0 → −135°, pmax → +135°."""
    return -135 + 270 * p / pmax

def dial(cx, cy, r, ticks=12, labels=None, needles=(), dur=4):
    """Đồng hồ áp suất. labels = {chỉ số vạch: chữ}. needles = [(phi, màu, nét đứt, dphi hoặc None)]: dphi ≠ None → quay (mô phỏng)."""
    out = circ(cx, cy, r, "currentColor", 2.2)
    for i in range(ticks + 1):
        a = math.radians(-135 + 270 * i / ticks); s, c = math.sin(a), -math.cos(a)
        r0 = r - (9 if i % 2 == 0 else 6)
        out += seg(cx + r0 * s, cy + r0 * c, cx + (r - 2) * s, cy + (r - 2) * c, "currentColor", 1.4)
    for i, t in (labels or {}).items():
        a = math.radians(-135 + 270 * i / ticks)
        out += lbl(cx + (r - 22) * math.sin(a), cy - (r - 22) * math.cos(a) + 4, t, "currentColor", 11, "middle", "600")
    for ph, col, dash, dphi in needles:
        a = math.radians(ph); L = r - 12
        ln = seg(cx, cy, cx + L * math.sin(a), cy - L * math.cos(a), col, 2.6, dash)
        out += rot(cx, cy, dphi, dur, ln) if dphi is not None else ln
    return out + dot(cx, cy, 4, "currentColor")

def thermo(x, ytop, h, t_low, t_high, t0, t1, anim, dur=4, labels=True):
    """Nhiệt kế: cột chất lỏng dâng tuyến tính theo nhiệt độ từ t0 đến t1 (chia độ t_low..t_high)."""
    yb = ytop + h; l0 = h * (t0 - t_low) / (t_high - t_low); l1 = h * (t1 - t_low) / (t_high - t_low)
    out = R(x - 6, ytop, 12, h, sw=2, rx=6) + circ(x, yb + 10, 10, RED, 2, RED)
    if anim:
        out += (f'<rect x="{x - 3}" y="{yb - l0:.1f}" width="6" height="{l0:.1f}" fill="{RED}">'
                f'{smil("y", [yb - l0, yb - l1], dur)}{smil("height", [l0, l1], dur)}</rect>')
    else:
        out += f'<rect x="{x - 3}" y="{yb - l1:.1f}" width="6" height="{l1:.1f}" fill="{RED}"/>'
    if labels:
        for lv, t in ((l0, t0), (l1, t1)):
            out += seg(x + 6, yb - lv, x + 14, yb - lv, "currentColor", 1.4) + txt(x + 18, yb - lv + 4, f"{t} °C", "currentColor", 12, "start", "700")
    return out

def flame(x, y):
    return f'<path d="M{x},{y} C{x - 11},{y - 10} {x - 7},{y - 17} {x},{y - 27} C{x + 7},{y - 17} {x + 11},{y - 10} {x},{y} Z" fill="{ORG}" opacity=".85"/>'

def smil0(attr, vals, dur):
    return f'<animate attributeName="{attr}" values="{";".join(f"{v:.0f}" for v in vals)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'

def refl(u, lo, hi):
    """Toạ độ sau khi phản xạ đàn hồi ở hai thành lo, hi (đường đi gấp khúc)."""
    w = hi - lo; u = (u - lo) % (2 * w)
    return lo + (u if u <= w else 2 * w - u)

def dots(xa, ya, xb, yb, n, seed, dur, speed, samples=60, r=3.6, c=BLUE):
    """n phân tử chuyển động trong hộp [xa,xb]×[ya,yb]; vận tốc đầu cho trước, phản xạ đàn hồi ở thành (lấy mẫu cách đều thời gian)."""
    rnd = random.Random(seed); out = ""; static = ""
    for _ in range(n):
        x0 = rnd.uniform(xa + r, xb - r); y0 = rnd.uniform(ya + r, yb - r)
        th = rnd.uniform(0, 2 * math.pi); v = speed * rnd.uniform(0.6, 1.2)
        vx, vy = v * math.cos(th), v * math.sin(th)
        X = [refl(x0 + vx * dur * k / samples, xa + r, xb - r) for k in range(samples + 1)]
        Y = [refl(y0 + vy * dur * k / samples, ya + r, yb - r) for k in range(samples + 1)]
        out += f'<circle cx="{X[0]:.0f}" cy="{Y[0]:.0f}" r="{r}" fill="{c}" opacity=".9">{smil0("cx", X, dur)}{smil0("cy", Y, dur)}</circle>'
        static += f'<circle cx="{x0:.0f}" cy="{y0:.0f}" r="{r}" fill="{c}" opacity=".9"/>'
    return out, static


# ───────────── Dạng 1 · bình kín nung nóng: 27 °C → 117 °C, p₁ = 2,4·10⁵ Pa ─────────────
def d1(kk):
    p = f"d1{kk}"; anim = kk == 0; PM = 5.0
    ph0, ph1 = phi(2.4, PM), phi(3.12, PM)
    b = R(36, 56, 100, 90, sw=2.4, rx=14) + txt(86, 96, "khí kín", "currentColor", 13, "middle", "600") + txt(86, 114, "V không đổi", "currentColor", 12, "middle", "400")
    for x in (58, 86, 114):
        b += flame(x, 178)
    b += seg(136, 100, 208, 100, "currentColor", 3)
    ndl = [(ph0, RED, "", ph1 - ph0 if anim else None)] if anim else [(ph0, GREY, "5 4", None)]
    b += dial(254, 100, 46, 12, None, ndl, 4)
    b += txt(254, 170, "p₁ = 2,4·10⁵ Pa", "currentColor", 12, "middle", "700") + txt(254, 188, "p₂ = ?", ORG, 13, "middle", "700")
    b += thermo(352, 44, 108, 0, 130, 27, 117, anim)
    if kk == 0:
        return fig("d1-0", "0 0 420 210", "Bình thép kín được đốt nóng từ 27 độ C lên 117 độ C, kim áp kế quay dần", b,
                   "Mô phỏng: nhiệt độ tăng đều từ 27 °C lên 117 °C trong 4 s; kim áp kế quay theo công thức, thang đo không ghi số. " + NOTE)
    b += txt(16, 24, "Đẳng tích: p/T không đổi", GRN, 13, "start", "700") + txt(16, 42, "T phải là Kelvin", "currentColor", 12, "start", "400")
    return fig("d1-2", "0 0 420 210", "Dữ kiện: bình kín thể tích không đổi, áp suất và nhiệt độ ban đầu, nhiệt độ sau khi nóng lên", b,
               "Dữ kiện: V không đổi, lượng khí không đổi; kim xám là vị trí ban đầu. " + NOTE)


# ───────────── Dạng 2 · nén xi lanh: 2,4 → 0,20 dm³, 1,0 → 18 atm, 27 °C → ? ─────────────
def d2(kk):
    p = f"d2{kk}"; anim = kk == 0
    X0, S1, S2 = 56, 300, 25          # px: V₁ = 2,4 dm³ ↔ 300 px; V₂ = 0,20 dm³ ↔ 25 px (đúng tỉ lệ 12 : 1)
    b = seg(50, 62, 372, 62, "currentColor", 2.4) + seg(50, 118, 372, 118, "currentColor", 2.4) + seg(50, 62, 50, 118, "currentColor", 3)
    if anim:
        b += f'<rect x="{X0}" y="64" width="{S1}" height="52" fill="{GRN}" opacity=".25">{smil("width", [S1, S2], 5)}</rect>'
    else:
        b += f'<rect x="{X0}" y="64" width="{S2}" height="52" fill="{GRN}" opacity=".25"/>'
    pist = R(X0 + S1, 66, 10, 48, sw=2.2, fill="currentColor", op=.35) + seg(X0 + S1 + 10, 90, X0 + S1 + 46, 90, "currentColor", 3) + seg(X0 + S1 + 46, 74, X0 + S1 + 46, 106, "currentColor", 4)
    if anim:
        b += f'<g><animateTransform attributeName="transform" type="translate" values="0 0;{-(S1 - S2)} 0" dur="5s" begin="indefinite" fill="freeze"/>{pist}</g>'
    else:
        b += f'<g transform="translate({-(S1 - S2)} 0)">{pist}</g>' + R(X0 + S1, 66, 10, 48, sw=1.4, dash="5 4", op=.5)
    b += seg(X0, 140, X0 + S1, 140, "currentColor", 1.6) + seg(X0, 134, X0, 146, "currentColor", 1.6) + seg(X0 + S1, 134, X0 + S1, 146, "currentColor", 1.6)
    b += txt(X0 + S1 / 2 + 70, 160, "V₁ = 2,4 dm³", "currentColor", 13, "middle")
    b += seg(X0, 172, X0 + S2, 172, ORG, 1.8) + seg(X0, 166, X0, 178, ORG, 1.8) + seg(X0 + S2, 166, X0 + S2, 178, ORG, 1.8)
    b += txt(X0 + S2 + 8, 176, "V₂ = 0,20 dm³", ORG, 13)
    b += txt(16, 24, "Trước nén: p₁ = 1,0 atm ; T₁ = 27 °C", "currentColor", 12, "start", "700")
    b += txt(16, 44, "Sau nén: p₂ = 18 atm ; T₂ = ?", ORG, 12, "start", "700")
    if kk == 0:
        return fig("d2-0", "0 0 420 190", "Pit-tông nén khí trong xi lanh từ 2,4 xuống 0,20 đềximét khối", b,
                   "Mô phỏng: pit-tông nén đều trong 5 s, thể tích khí tính từ số liệu của đề. " + NOTE.replace("Hình minh hoạ, không đúng tỉ lệ.", "Chiều dài đúng tỉ lệ thể tích."))
    b += txt(16, 206, "p₁V₁/T₁ = p₂V₂/T₂", GRN, 13, "start", "700") + txt(410, 54, "nét đứt: vị trí pit-tông lúc đầu", "currentColor", 11, "end", "400")
    return fig("d2-2", "0 0 420 216", "Dữ kiện: thể tích, áp suất, nhiệt độ ban đầu và áp suất cuối", b, "Dữ kiện: cả ba thông số cùng đổi, lượng khí không đổi. Chiều dài đúng tỉ lệ thể tích.")


# ───────────── Dạng 3 · đồ thị p–T: đường (1) qua M(300 K; 3,0) và N(500 K); đường (2) qua Q(300 K; 1,5) ─────────────
def d3(kk):
    p = f"d3{kk}"; anim = kk == 0
    O = (60, 190); kx, ky = 0.5, 30      # 0,5 px/K ; 30 px / 10⁵ Pa
    X = lambda T: O[0] + kx * T
    Y = lambda pp: O[1] - ky * pp
    b = arrow(p, "g", O[0], O[1], 392, O[1], 2) + arrow(p, "g", O[0], O[1], O[0], 24, 2)
    b += txt(388, O[1] + 18, "T (K)", GRN, 12, "end") + txt(O[0] - 10, 34, "p", GRN, 13, "end") + txt(O[0] - 8, O[1] + 14, "O", "currentColor", 13, "end")
    b += seg(*O, X(540), Y(5.4), ORG, 2.6) + seg(*O, X(540), Y(2.7), BLUE, 2.6)
    b += txt(X(540) + 6, Y(5.4) + 3, "(1)", ORG, 13) + txt(X(540) + 6, Y(2.7) + 4, "(2)", BLUE, 13)
    b += seg(X(300), O[1], X(300), Y(3.0), "currentColor", 1.2, "4 4", .6) + seg(X(500), O[1], X(500), Y(5.0), "currentColor", 1.2, "4 4", .6)
    for T in (300, 500):
        b += seg(X(T), O[1] - 4, X(T), O[1] + 4, "currentColor", 1.6) + txt(X(T), O[1] + 18, str(T), "currentColor", 12, "middle", "400")
    b += dot(X(300), Y(3.0), 4.5, ORG) + dot(X(300), Y(1.5), 4.5, BLUE)
    b += txt(X(300) - 8, Y(3.0) - 16, "T_M = 300 K", ORG, 12, "end") + txt(X(300) - 8, Y(3.0) - 1, "p_M = 3,0·10⁵ Pa", ORG, 12, "end")
    b += txt(X(300) + 10, Y(1.5) + 18, "T_Q = 300 K", BLUE, 12) + txt(X(300) + 10, Y(1.5) + 32, "p_Q = 1,5·10⁵ Pa", BLUE, 12)
    b += txt(84, 22, "(1): V₁ = 4,0 lít", ORG, 12) + txt(84, 38, "(2): V₂ = ?", BLUE, 12)
    nx, ny = X(500), Y(5.0)
    b += txt(nx + 12, ny + 24, "T_N = 500 K", ORG, 12) + txt(nx + 12, ny + 40, "p_N = ?", ORG, 13)
    if kk == 0:
        b += (f'<circle cx="{X(300):.1f}" cy="{Y(3.0):.1f}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">'
              f'{smil("cx", [X(300), nx], 4)}{smil("cy", [Y(3.0), ny], 4)}</circle>')
        return fig("d3-0", "0 0 420 230", "Đồ thị p theo T của một lượng khí: điểm M chạy dọc đường thẳng qua gốc toạ độ tới điểm N, đường thứ hai qua Q", b,
                   "Mô phỏng: điểm biểu diễn trạng thái chạy từ M tới N dọc đường thẳng (1) (nung nóng đều 4 s). " + "Hình vẽ theo tỉ lệ, trục không ghi số.")
    b += dot(nx, ny, 4.5, ORG)
    return fig("d3-2", "0 0 420 230", "Dữ kiện: hai đường thẳng qua gốc toạ độ trên đồ thị p–T, các điểm M, N, Q và nhiệt độ tương ứng", b,
               "Dữ kiện: hai đường đẳng tích của cùng một lượng khí; M và Q cùng nhiệt độ. " + "Hình vẽ theo tỉ lệ, trục không ghi số.")


# ───────────── Dạng 4 · bình thép 12 lít, N₂, 27 °C, 2,0·10⁶ Pa ─────────────
def d4(kk):
    p = f"d4{kk}"; anim = kk == 0
    xa, ya, xb, yb = 44, 46, 204, 136
    box = R(xa - 4, ya - 4, xb - xa + 8, yb - ya + 8, sw=2.6, rx=16) + seg(100, ya - 4, 100, ya - 16, "currentColor", 3) + seg(88, ya - 16, 112, ya - 16, "currentColor", 4)
    mov, sta = dots(xa + 6, ya + 6, xb - 6, yb - 6, 11, 8, 6, 55)
    b = box + (mov if anim else sta)
    b += txt(124, 166, "khí nitrogen N₂", "currentColor", 12, "middle", "400")
    b += txt(232, 46, "V = 12 lít", "currentColor", 13) + txt(232, 64, "t = 27 °C", "currentColor", 13) + txt(232, 82, "p = 2,0·10⁶ Pa", "currentColor", 13)
    b += txt(232, 100, "M = 28 g/mol", "currentColor", 13) + txt(232, 118, "R = 8,31 J/(mol·K)", "currentColor", 12, "start", "400")
    if kk == 0:
        b += txt(232, 142, "n = ?", ORG, 13) + txt(232, 160, "m = ?", ORG, 13) + txt(232, 178, "V₀ = ?", ORG, 13)
        return fig("d4-0", "0 0 420 192", "Bình thép chứa khí nitrogen, các phân tử chuyển động hỗn loạn va chạm vào thành bình", b,
                   "Mô phỏng: chuyển động nhiệt của phân tử khí trong bình trong 6 s (phản xạ đàn hồi ở thành). " + NOTE)
    b += txt(232, 142, "n = pV/(RT)", GRN, 13) + txt(232, 160, "m = n·M", GRN, 13) + txt(232, 178, "V₀ = n·22,4 lít", GRN, 13)
    return fig("d4-2", "0 0 420 192", "Dữ kiện: thể tích, nhiệt độ, áp suất, khối lượng mol của khí trong bình", b,
               "Dữ kiện: một trạng thái của khí, cần số mol rồi khối lượng. " + NOTE)


# ───────────── Dạng 5 · xả bớt oxygen: 4,5·10⁶ Pa (27 °C) → 1,5·10⁶ Pa (17 °C), V = 8,0 lít ─────────────
def d5(kk):
    p = f"d5{kk}"; anim = kk == 0; PM = 6.0
    ph0, ph1 = phi(4.5, PM), phi(1.5, PM)
    b = R(30, 80, 100, 100, sw=2.4, rx=16) + seg(80, 80, 80, 62, "currentColor", 3) + R(68, 50, 24, 12, sw=2.2, rx=3) + txt(80, 138, "O₂", "currentColor", 14, "middle", "700")
    b += seg(130, 130, 206, 130, "currentColor", 3)
    if anim:
        nd = [(ph0, RED, "", ph1 - ph0)]
    else:
        nd = [(ph0, GREY, "5 4", None), (ph1, RED, "", None)]
    b += dial(258, 130, 52, 12, {0: "0", 4: "2", 8: "4", 12: "6"}, nd, 4)
    b += txt(258, 198, "×10⁶ Pa", "currentColor", 11, "middle", "400")
    b += txt(16, 20, "Lúc mới nạp: 27 °C ; 4,5·10⁶ Pa", "currentColor", 12, "start", "700")
    b += txt(16, 38, "Lúc còn lại: 17 °C ; 1,5·10⁶ Pa", "currentColor", 12, "start", "700")
    b += txt(330, 90, "V = 8,0 lít", "currentColor", 12, "start", "700") + txt(330, 108, "M = 32 g/mol", "currentColor", 12, "start", "400")
    b += txt(330, 150, "Δm = ?", ORG, 13, "start", "700")
    if kk == 0:
        return fig("d5-0", "0 0 420 214", "Oxygen trong bình thép được dùng bớt, kim áp kế quay từ 4,5 về 1,5 nhân 10 mũ 6 pascal", b,
                   "Mô phỏng: khí được dùng dần, kim áp kế quay đều từ 4,5·10⁶ Pa về 1,5·10⁶ Pa trong 4 s. " + NOTE)
    b += txt(16, 206, "pV = nRT cho từng trạng thái", GRN, 12, "start", "700")
    return fig("d5-2", "0 0 420 214", "Dữ kiện: hai trạng thái của bình oxygen trước và sau khi dùng, kim xám là lúc mới nạp", b,
               "Dữ kiện: lượng khí giảm, tính số mol riêng cho từng trạng thái; kim xám là lúc mới nạp. " + NOTE)
