"""Hình cho bài tập mẫu Bài 23 "Điện trở. Định luật Ohm" (Vật lí 11), lesson_id 42.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mô phỏng chỉ dùng dữ kiện đề đã cho hoặc ví dụ không phải đáp số; hình dữ kiện có dấu "?" ở đại lượng cần tìm."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"
YEL = "#fde047"


def t(x, y, s, c="currentColor", size=13, anchor="start", weight="600"):
    return lbl(x, y, s, c, size, anchor, weight)

def circ(x, y, r, c="currentColor", w=2, fill="none", op=1):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{w}" opacity="{op}"/>'

def rect(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'

def anim(attr, vals, kts, T):
    v = ";".join(f"{x:.1f}" if isinstance(x, float) else str(x) for x in vals)
    k = ";".join(f"{q:.4f}" for q in kts)
    return f'<animate attributeName="{attr}" values="{v}" keyTimes="{k}" dur="{T:.2f}s" begin="indefinite" fill="freeze"/>'

def appear(inner, t0, t1, T):
    """Nhóm hiện dần: mặc định thấy (giảm chuyển động vẫn đủ hình), khi bấm chạy thì ẩn rồi hiện lần lượt."""
    return f'<g>{inner}{anim("opacity", [0, 0, 1, 1], [0, t0 / T, t1 / T, 1], T)}</g>'


# ───────────── mạch điện: nguồn – điện trở – ampe kế – vôn kế ─────────────
def circuit(box_label, a_label, v_label, src_label="nguồn điều chỉnh được"):
    b = seg(70, 50, 196, 50) + seg(224, 50, 350, 50)
    b += seg(70, 50, 70, 92) + seg(70, 108, 70, 160) + seg(70, 160, 350, 160)
    b += seg(350, 50, 350, 80) + seg(350, 130, 350, 160)
    b += seg(56, 92, 84, 92, "currentColor", 3) + seg(62, 108, 78, 108, "currentColor", 3)
    b += t(94, 92, "+", "currentColor", 14, "start", "700") + t(94, 117, "−", "currentColor", 14, "start", "700")
    b += rect(338, 80, 24, 50, "currentColor", 2.2)
    b += circ(210, 50, 14) + t(210, 55, "A", "currentColor", 14, "middle", "700")
    b += seg(350, 66, 388, 66) + seg(388, 66, 388, 91) + seg(388, 119, 388, 144) + seg(388, 144, 350, 144)
    b += dot(350, 66, 3) + dot(350, 144, 3)
    b += circ(388, 105, 14) + t(388, 110, "V", "currentColor", 14, "middle", "700")
    b += t(326, 110, box_label, ORG, 14, "end", "700")
    if a_label: b += t(210, 28, a_label, "currentColor", 14, "middle", "700")
    if v_label: b += t(388, 44, v_label, "currentColor", 14, "middle", "700")
    b += t(70, 182, src_label, "currentColor", 12, "middle", "400")
    return b

LOOP = 780
def loop_pos(s):
    s %= LOOP
    if s <= 280: return (70 + s, 160)
    s -= 280
    if s <= 110: return (350, 160 - s)
    s -= 110
    if s <= 280: return (350 - s, 50)
    s -= 280
    return (70, 50 + s)

def electrons(n=8, shift=195, T=5.0):
    """Êlectron (chấm xanh) đi ngược chiều kim đồng hồ: từ cực âm, qua điện trở, về cực dương. Chạy MỘT lần."""
    b = ""
    for i in range(n):
        s0 = LOOP / n * i
        pts = [s0] + [c for c in (280, 390, 670, 780, 1060, 1170, 1450, 1560) if s0 < c < s0 + shift] + [s0 + shift]
        kt = [(p_ - s0) / shift for p_ in pts]
        xy = [loop_pos(p_) for p_ in pts]
        b += (f'<circle cx="{xy[0][0]:.1f}" cy="{xy[0][1]:.1f}" r="3.8" fill="{BLUE}" stroke="currentColor" stroke-width="1">'
              + anim("cx", [q[0] for q in xy], kt, T) + anim("cy", [q[1] for q in xy], kt, T) + "</circle>")
    return b


# ───────────── Dạng 1 · R = U/I, đổi mA ─────────────
def d1(kk):
    if kk == 0:
        b = circuit("R ?", "", "")
        b += electrons()
        return fig("d1-0", "0 0 420 192", "Mạch gồm nguồn, điện trở và các êlectron tự do chuyển động qua điện trở", b,
                   "Mô phỏng: êlectron tự do (chấm xanh) đi từ cực âm của nguồn, qua điện trở, về cực dương; chạy chậm hơn nhiều lần so với thật. Chiều dòng điện quy ước ngược chiều êlectron. " + NOTE)
    b = circuit("R = ?", "24 mA", "6,0 V")
    b += t(16, 206, "Sau đó tăng hiệu điện thế của nguồn lên 15 V", "currentColor", 12, "start", "400")
    b += t(16, 224, "Cần tìm: R (ôm) ; I′ (mA)", ORG, 12, "start", "700")
    return fig("d1-2", "0 0 420 232", "Mạch có ampe kế chỉ 24 mA, vôn kế chỉ 6,0 V và điện trở chưa biết", b,
               "Dữ kiện: số chỉ của ampe kế và vôn kế; điện trở R và dòng điện I′ ở hiệu điện thế mới là ẩn. " + NOTE)


# ───────────── trục toạ độ I theo U ─────────────
def axes_iu(ox, oy, wpx, hpx, xl, yl, xticks, yticks):
    b = seg(ox, oy, ox + wpx, oy) + chevron(ox + wpx, oy, 1, 0, "currentColor", 2, 10)
    b += seg(ox, oy, ox, oy - hpx) + chevron(ox, oy - hpx, 0, -1, "currentColor", 2, 10)
    b += t(ox - 8, oy + 14, "O", "currentColor", 13, "end", "700")
    for x, s in xticks:
        b += seg(x, oy, x, oy + 5) + t(x, oy + 18, s, "currentColor", 12, "middle", "400")
    for y, s in yticks:
        b += seg(ox - 5, y, ox, y) + t(ox - 9, y + 4, s, "currentColor", 12, "end", "400")
    b += t(ox + wpx - 4, oy + 34, xl, "currentColor", 13, "end", "700") + t(ox + 8, oy - hpx + 4, yl, "currentColor", 13, "start", "700")
    return b

def mk_x(x, y, c=ORG):   # chấm tròn
    return circ(x, y, 5.5, c, 1.8, c)

def mk_y(x, y, c=BLUE):  # ô vuông
    return f'<rect x="{x - 5:.1f}" y="{y - 5:.1f}" width="10" height="10" fill="{c}" stroke="{c}" stroke-width="1.8"/>'


# ───────────── Dạng 2 · bảng đo của X (điện trở thuần) và Y (NTC) ─────────────
def d2(kk):
    ox, oy = 64, 190
    sx, sy = 50, 20
    X = [(2.0, 2.0), (4.0, 4.0), (6.0, 6.0)]
    Y = [(1.0, 0.5), (3.0, 2.0), (6.0, 6.6)]
    px = lambda u: ox + sx * u
    py = lambda i: oy - sy * i
    b = axes_iu(ox, oy, 340, 168, "U (V)", "I (mA)", [(px(u), str(u)) for u in (2, 4, 6)],
                [(py(i), str(i)) for i in (2, 4, 6, 8)])
    if kk == 0:
        order = [("y", 0), ("x", 0), ("y", 1), ("x", 1), ("x", 2), ("y", 2)]
        T = 6.0
        for n, (k_, j) in enumerate(order):
            u, i = (X if k_ == "x" else Y)[j]
            m = mk_x(px(u), py(i)) if k_ == "x" else mk_y(px(u), py(i))
            b += appear(m, 0.4 + n * 0.85, 0.9 + n * 0.85, T)
        b += mk_x(262, 26) + t(272, 30, "X", ORG, 13, "start", "700") + mk_y(318, 26) + t(328, 30, "Y", BLUE, 13, "start", "700")
        return fig("d2-0", "0 0 420 236", "Sáu điểm đo của hai linh kiện X và Y lần lượt hiện trên hệ trục I (mA) theo U (V)", b,
                   "Mô phỏng: các điểm đo (U; I) trong bảng của đề lần lượt hiện lên theo thứ tự U tăng dần, nhanh hơn nhiều so với lúc đo thật. " + NOTE)
    b += t(120, 60, "Cần xác định: dạng đường đi qua", ORG, 12, "start", "700") + t(120, 78, "các điểm đo của X và của Y", ORG, 12, "start", "700")
    return fig("d2-2", "0 0 420 236", "Hệ trục I (mA) theo U (V) để vẽ các điểm đo của X và Y", b,
               "Dữ kiện: hệ trục cho các điểm đo trong bảng của đề; dạng đường của mỗi linh kiện là điều cần xác định. " + NOTE)


# ───────────── Dạng 3 · hai đường qua gốc, trục I tính bằng mA ─────────────
def d3(kk):
    ox, oy = 64, 190
    sx, sy = 40, 40
    px = lambda u: ox + sx * u
    py = lambda i: oy - sy * i
    b = axes_iu(ox, oy, 336, 168, "U (V)", "I (mA)", [(px(u), str(u)) for u in (2, 4, 6, 8)],
                [(py(i), str(i)) for i in (1, 2, 3, 4)])
    x6 = px(6.0)
    if kk == 0:
        b += f'<line x1="{x6:.1f}" y1="{oy}" x2="{x6:.1f}" y2="{oy}" stroke="{GREY}" stroke-width="1.6" stroke-dasharray="5 4">' \
             + anim("y2", [oy, py(3.0)], [0, 1], 1.5) + "</line>"
    else:
        b += seg(x6, oy, x6, py(3.0), GREY, 1.6, "5 4")
    p1 = mk_x(x6, py(3.0)) + t(x6 + 12, py(3.0) + 4, "(1): 3,0 mA", ORG, 13, "start", "700")
    p2 = mk_y(x6, py(1.2)) + t(x6 + 12, py(1.2) + 4, "(2): 1,2 mA", BLUE, 13, "start", "700")
    if kk == 0:
        b += appear(p1, 1.6, 2.4, 4.0) + appear(p2, 2.4, 3.2, 4.0)
        return fig("d3-0", "0 0 420 236", "Hai điểm đo của hai điện trở tại hiệu điện thế 6,0 V trên hệ trục I (mA) theo U (V)", b,
                   "Mô phỏng: kẻ đường dóng tại U = 6,0 V rồi hai điểm của đường (1) và (2) hiện lên; đường (1), (2) đi qua gốc O và điểm tương ứng. " + NOTE)
    b += p1 + p2
    b += t(110, 52, "Cần tìm: R₁, R₂ (kΩ)", ORG, 12, "start", "700") + t(110, 70, "Đường nào dốc hơn?", ORG, 12, "start", "700")
    return fig("d3-2", "0 0 420 236", "Hai điểm đo của hai điện trở tại hiệu điện thế 6,0 V, cường độ dòng điện tính bằng mA", b,
               "Dữ kiện: mỗi đường đi qua gốc O và điểm đã cho; trục đứng tính bằng mA. " + NOTE)


# ───────────── Dạng 4 · dây platin: ion dao động mạnh dần ─────────────
def d4(kk):
    if kk == 0:
        T = 6.0; n = 30
        ion_x = [130 + 64 * k for k in range(4)]
        rows = [62, 128]
        b = ""
        for ri, y in enumerate(rows):
            for ci, x0 in enumerate(ion_x):
                ph = (ri * 4 + ci) * 0.9
                vals = [x0 + (1 + 6 * j / n) * math.sin(2 * math.pi * 4 * j / n + ph) for j in range(n + 1)]
                b += (f'<circle cx="{x0}" cy="{y}" r="9" fill="{RED}" fill-opacity=".55" stroke="{RED}" stroke-width="1.6">'
                      + smil("cx", vals, T) + "</circle>")
        m = 48
        ex = [96 + 268 * j / m for j in range(m + 1)]
        ey = [95 + 22 * math.sin(2 * math.pi * (2 * (j / m) + 5 * (j / m) ** 2)) for j in range(m + 1)]
        b += (f'<circle cx="{ex[0]:.1f}" cy="{ey[0]:.1f}" r="4.5" fill="{BLUE}" stroke="currentColor" stroke-width="1">'
              + smil("cx", ex, T) + smil("cy", ey, T) + "</circle>")
        b += rect(36, 30, 16, 130, "currentColor", 2, "none", 8)
        b += (f'<rect x="39" y="150" width="10" height="10" rx="4" fill="{ORG}">' + smil("y", [150, 52], T) + smil("height", [10, 108], T) + "</rect>")
        b += t(44, 22, "nhiệt độ", "currentColor", 12, "middle", "400") + t(44, 180, "nóng dần", ORG, 12, "middle", "700")
        b += circ(116, 196, 5, RED, 1.6, RED) + t(126, 200, "ion nút mạng", "currentColor", 12, "start", "400")
        b += circ(256, 196, 5, BLUE, 1.6, BLUE) + t(266, 200, "êlectron tự do", "currentColor", 12, "start", "400")
        return fig("d4-0", "0 0 420 208", "Kim loại nóng dần: các ion dao động mạnh dần và êlectron bị va chạm nhiều hơn", b,
                   "Mô phỏng: kim loại nóng dần (cột bên trái); ion dao động ngày càng mạnh, êlectron đi qua bị lệch nhiều hơn. Chạy chậm, vị trí và biên độ chỉ để minh hoạ. " + NOTE)
    b = circuit("R = ?", "5,0 mA", "0,89 V", "nguồn")
    b += t(16, 206, "Dây platin: R₀ = 100 Ω ở t₀ = 0 °C ; α = 3,9·10⁻³ K⁻¹", "currentColor", 12, "start", "400")
    b += t(16, 224, "Cần tìm: R ; nhiệt độ t của lò", ORG, 12, "start", "700")
    return fig("d4-2", "0 0 420 232", "Mạch đo điện trở dây platin trong lò: ampe kế chỉ 5,0 mA, vôn kế chỉ 0,89 V", b,
               "Dữ kiện: số chỉ hai đồng hồ, R₀ và α của platin; điện trở của dây và nhiệt độ lò là ẩn. " + NOTE)


# ───────────── Dạng 5 · dây nung nicrom của bàn là ─────────────
def d5(kk):
    if kk == 0:
        T = 5.0
        pts = [(110, 90)] + [(120 + 15 * k, 66 if k % 2 == 0 else 114) for k in range(13)] + [(310, 90)]
        b = (f'<polyline fill="none" stroke="{GREY}" stroke-width="3.2" stroke-linejoin="round" points="' + " ".join(f"{x},{y}" for x, y in pts) + '">'
             + anim("stroke", [GREY, ORG, ORG], [0, 0.6, 1], T) + "</polyline>")
        b += t(210, 40, "dây nung nicrom của bàn là", "currentColor", 13, "middle", "700")
        b += t(210, 150, "220 V", "currentColor", 14, "middle", "700")
        return fig("d5-0", "0 0 420 166", "Dây nung của bàn là nguội nóng dần lên", b,
                   "Mô phỏng: dây nung nguội (màu xám) nóng dần lên (màu cam) sau khi cắm điện; màu chỉ để minh hoạ, không phải thang nhiệt độ. " + NOTE)
    b = circuit("R = ?", "I = ?", "220 V", "mạng điện")
    b += t(16, 204, "Nicrom ở 20 °C: R₀ = 40,0 Ω ; ρ₀ = 1,10·10⁻⁶ Ω·m", "currentColor", 12, "start", "400")
    b += t(16, 222, "α = 0,40·10⁻³ K⁻¹ ; dây nóng ổn định ở 270 °C", "currentColor", 12, "start", "400")
    b += t(16, 240, "Cần tìm: R, I khi nóng ; I lúc vừa cắm ; ρ", ORG, 12, "start", "700")
    return fig("d5-2", "0 0 420 250", "Mạch bàn là: vôn kế chỉ 220 V, điện trở và cường độ dòng điện khi nóng chưa biết", b,
               "Dữ kiện: hiệu điện thế 220 V, các giá trị ở 20 °C và nhiệt độ khi nóng ổn định; điện trở, dòng điện và điện trở suất là ẩn. " + NOTE)


BUILD = [d1, d2, d3, d4, d5]
