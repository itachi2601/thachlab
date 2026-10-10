"""Hình cho bài tập mẫu Bài 13 "Đại cương về dòng điện xoay chiều" (Vật lí 12), lesson_id 14.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mọi đường cong, điểm chạy, độ sáng bóng đèn, góc quay của khung đều TÍNH từ biểu thức của đề (lấy mẫu cách đều thời gian,
nội suy tuyến tính). Trục không ghi số; nhãn chỉ ghi dữ kiện đề cho và dấu "?" cho đại lượng cần tìm."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, trục không ghi số."
TAU = 2 * math.pi


def tx(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, s, c, size, anchor, weight)


def smilf(attr, vals, dur, nd=1):
    return f'<animate attributeName="{attr}" values="{";".join(f"{v:.{nd}f}" for v in vals)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


def curve(f, ncyc, ox, oy, wpx, apx, per=40):
    """Các điểm (X, Y) của đồ thị; f(x) nhận x = số chu kì kể từ t = 0, trả giá trị chuẩn hoá trong [-1, 1]."""
    n = int(round(per * ncyc))
    return [(ox + wpx * k / n, oy - apx * f(ncyc * k / n)) for k in range(n + 1)]


def axes_tv(ox, oy, wpx, apx, vlab, up=18):
    b = arrow("", "g", ox - 8, oy, ox + wpx + 16, oy, 2) + arrow("", "g", ox, oy + apx + 14, ox, oy - apx - up, 2)
    b += tx(ox + wpx + 14, oy + 17, "t", GRN, 13, "end") + tx(ox + 8, oy - apx - up + 8, vlab, GRN, 13)
    b += tx(ox - 6, oy + 16, "O", "currentColor", 13, "end")
    return b


def runner(pts, dur):
    """Điểm chạy dọc đồ thị, một lần khi bấm."""
    return (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">'
            f'{smilf("cx", [p[0] for p in pts], dur)}{smilf("cy", [p[1] for p in pts], dur)}</circle>')


def rot(cx, cy, dphi, dur, inner):
    """Nhóm quay quanh (cx,cy) góc dphi độ (âm = ngược chiều kim đồng hồ), đều theo thời gian; chạy một lần khi bấm."""
    return (f'<g><animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};{dphi:.1f} {cx} {cy}" '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>{inner}</g>')


# ───────────── Dạng 1 · u = 20√2 cos(40πt + π/3) V ─────────────
def d1(kk):
    ox, oy, wpx, apx, ncyc = 140, 114, 240, 58, 2.5
    f = lambda x: math.cos(TAU * x + math.pi / 3)
    pts = curve(f, ncyc, ox, oy, wpx, apx)
    b = axes_tv(ox, oy, wpx, apx, "u") + poly(pts, BLUE, 2.6)
    b += tx(14, 22, "u = 20√2 cos(40πt + π/3) V", "currentColor", 13)
    b += dot(*pts[0], 4.5, ORG) + tx(ox - 10, pts[0][1] + 4, "u(0) = ?", ORG, 12, "end")
    if kk == 0:
        run = curve(f, ncyc, ox, oy, wpx, apx, 32)
        b += runner(run, 5.0)
        return fig("d1-0", "0 0 420 196", "Đồ thị điện áp u theo thời gian, điểm xanh chạy dọc đường cong từ thời điểm t bằng 0", b,
                   "Mô phỏng: điểm chạy trên đồ thị u(t) vẽ từ biểu thức của đề, chạy chậm 40 lần (một chu kì ứng với 2 s). " + NOTE)
    b += tx(14, 52, "U = ? ; φᵤ = ?", ORG, 13) + tx(14, 72, "ω, f, T = ?", ORG, 13)
    return fig("d1-2", "0 0 420 196", "Dữ kiện: biểu thức của điện áp u và đồ thị của nó, điểm cam là thời điểm t bằng 0", b,
               "Dữ kiện: biểu thức đã ở dạng chuẩn hàm cos; điểm cam là t = 0. " + NOTE)


# ───────────── Dạng 2 · i = 4cos(100πt − π/6) A qua R = 25 Ω ─────────────
def d2(kk):
    ox, oy, wpx, apx, ncyc = 214, 100, 170, 52, 2
    f = lambda x: math.cos(TAU * x - math.pi / 6)
    pts = curve(f, ncyc, ox, oy, wpx, apx)
    b = axes_tv(ox, oy, wpx, apx, "i") + poly(pts, BLUE, 2.6)
    zz = [(40, 100)]
    for k in range(7):
        zz.append((46 + k * 10, 100 + (12 if k % 2 == 0 else -12)))
    zz += [(116, 100), (136, 100)]
    gl = lambda v: 0.62 * v * v
    if kk == 0:
        vals = [gl(f(ncyc * k / (32 * ncyc))) for k in range(32 * ncyc + 1)]
        b += f'<rect x="38" y="80" width="80" height="40" rx="8" fill="{ORG}" opacity="{vals[0]:.2f}">{smilf("opacity", vals, 4.0, 2)}</rect>'
    b += seg(14, 100, 40, 100, "currentColor", 2.4) + poly(zz, "currentColor", 2.4) + seg(116, 100, 136, 100, "currentColor", 2.4)
    b += tx(77, 148, "R = 25 Ω", "currentColor", 13, "middle") + tx(14, 22, "i = 4cos(100πt − π/6) A", "currentColor", 13)
    if kk == 0:
        b += runner(curve(f, ncyc, ox, oy, wpx, apx, 32), 4.0)
        return fig("d2-0", "0 0 420 176", "Điện trở R nối với nguồn xoay chiều, đồ thị cường độ dòng điện i theo thời gian và điểm chạy trên đồ thị", b,
                   "Mô phỏng: điểm chạy trên đồ thị i(t) và điện trở sáng lên theo i², chạy chậm 100 lần (một chu kì ứng với 2 s). " + NOTE)
    b += tx(14, 168, "P = ? ; Q (2 phút) = ?", ORG, 13)
    return fig("d2-2", "0 0 420 176", "Dữ kiện: điện trở R và đồ thị cường độ dòng điện xoay chiều chạy qua nó", b,
               "Dữ kiện: dòng xoay chiều chạy qua R trong 2 phút. " + NOTE)


# ───────────── Dạng 3 · f = 50 Hz, I = 2 A, i(0) = −√2 A, đang tăng ─────────────
def d3(kk):
    ox, oy, wpx, apx, ncyc = 150, 112, 240, 58, 2.5
    f = lambda x: math.cos(TAU * x - 2 * math.pi / 3)
    pts = curve(f, ncyc, ox, oy, wpx, apx)
    b = axes_tv(ox, oy, wpx, apx, "i") + poly(pts, BLUE, 2.6)
    b += tx(14, 22, "f = 50 Hz ; I = 2 A", "currentColor", 13) + tx(14, 42, "t = 0: i = −√2 A", "currentColor", 12, "start", "600") + tx(14, 60, "và đang tăng", "currentColor", 12, "start", "600")
    x0, y0 = pts[0]
    slope = apx * TAU * math.sin(-2 * math.pi / 3) / (wpx / ncyc)       # dY/dX tại t = 0 (âm: đồ thị đi lên)
    ln = 34 / math.hypot(1, slope)
    b += arrow("", "o", round(x0, 1), round(y0, 1), round(x0 + ln, 1), round(y0 + slope * ln, 1), 2.4)
    b += dot(x0, y0, 4.5, ORG) + tx(ox - 10, y0 + 4, "i(0)", ORG, 12, "end")
    if kk == 0:
        b += runner(curve(f, ncyc, ox, oy, wpx, apx, 32), 5.0)
        return fig("d3-0", "0 0 420 200", "Đồ thị cường độ dòng điện i theo thời gian; điểm xanh chạy từ thời điểm t bằng 0, lúc đầu i âm và đang tăng", b,
                   "Mô phỏng: điểm chạy trên đồ thị i(t) theo dữ kiện của đề, chạy chậm 100 lần (một chu kì ứng với 2 s); mũi tên cam là chiều biến thiên lúc t = 0. " + NOTE)
    b += tx(14, 176, "i = ?   (φ = ?)", ORG, 13)
    return fig("d3-2", "0 0 420 200", "Dữ kiện: cường độ dòng điện lúc t bằng 0 và chiều biến thiên của nó", b,
               "Dữ kiện: i(0) âm và đang tăng; mũi tên cam là chiều biến thiên lúc t = 0. " + NOTE)


# ───────────── Dạng 4 · khung dây quay đều 1500 vòng/phút, pháp tuyến cùng hướng B lúc t = 0 ─────────────
def d4(kk):
    cx, cy = 88, 112
    ox, oy, wpx, apx, ncyc = 238, 112, 140, 48, 2
    f = lambda x: math.cos(TAU * x)                  # Φ/Φ₀ = cos(ωt)
    pts = curve(f, ncyc, ox, oy, wpx, apx)
    b = axes_tv(ox, oy, wpx, apx, "Φ") + poly(pts, BLUE, 2.6)
    for y in (58, 84, 140, 166):                      # đường sức từ: nét đứt, đầu V
        b += field_line(14, y, 170, y, BLUE, 1.8, "6 4", 11)
    b += tx(176, 62, "B", BLUE, 13)
    frame = (seg(cx, cy - 34, cx, cy + 34, "currentColor", 4.5) + dot(cx, cy - 34, 4, "currentColor") + dot(cx, cy + 34, 4, "currentColor")
             + arrow("", "r", cx, cy, cx + 30, cy, 2.6))
    if kk == 0:
        b += rot(cx, cy, -720, 4.0, frame) + dot(cx, cy, 3.5, "currentColor")
        b += runner(curve(f, ncyc, ox, oy, wpx, apx, 32), 4.0)
    else:
        b += frame + dot(cx, cy, 3.5, "currentColor") + tx(cx + 34, cy - 8, "n", RED, 13)
        b += tx(14, 206, "ω, Φ₀, E₀, E = ? ; e = ?", ORG, 13)
    b += tx(14, 22, "n = 1500 vòng/phút ; B = 0,04 T", "currentColor", 13)
    b += tx(cx, 192, "nhìn dọc trục quay", "currentColor", 11, "middle", "400")
    if kk == 0:
        return fig("d4-0", "0 0 420 210", "Khung dây quay đều trong từ trường đều, đồ thị từ thông Φ theo thời gian và điểm chạy trên đồ thị", b,
                   "Mô phỏng: khung (nhìn dọc trục quay, mũi tên đỏ là pháp tuyến) quay đều ngược chiều kim đồng hồ, điểm xanh chạy trên đồ thị Φ(t); chạy chậm 50 lần (một vòng ứng với 2 s). " + NOTE)
    return fig("d4-2", "0 0 420 210", "Dữ kiện: khung dây quay quanh trục vuông góc với từ trường đều, lúc t bằng 0 pháp tuyến cùng hướng với B", b,
               "Dữ kiện: lúc t = 0 pháp tuyến n cùng hướng với B; trục quay vuông góc với B. " + NOTE)


# ───────────── Dạng 5 · đèn sáng khi |u| ≥ 100√3 V, u = 200cos(100πt) V ─────────────
def d5(kk):
    ox, oy, wpx, apx, ncyc = 98, 134, 282, 62, 3
    thr = math.sqrt(3) / 2
    f = lambda x: math.cos(TAU * x)
    pts = curve(f, ncyc, ox, oy, wpx, apx)
    b = axes_tv(ox, oy, wpx, apx, "u", 10) + poly(pts, BLUE, 2.6)
    for s in (1, -1):
        y = oy - s * thr * apx
        b += seg(ox, y, ox + wpx, y, ORG, 1.6, "6 4") + tx(ox - 8, y + 4, ("+" if s > 0 else "−") + "100√3 V", ORG, 12, "end")
    # bóng đèn
    bx, by = 44, 40
    glow = lambda x: 0.8 if abs(f(x)) >= thr - 1e-9 else 0.06
    if kk == 0:
        per = 60
        vals = [glow(ncyc * k / (per * ncyc)) for k in range(per * ncyc + 1)]
        b += f'<circle cx="{bx}" cy="{by}" r="30" fill="{ORG}" opacity="{vals[0]:.2f}">{smilf("opacity", vals, 6.0, 2)}</circle>'
    b += (f'<circle cx="{bx}" cy="{by}" r="17" fill="none" stroke="currentColor" stroke-width="2.4"/>'
          + poly([(bx - 7, by + 9), (bx - 4, by - 3), (bx, by + 5), (bx + 4, by - 3), (bx + 7, by + 9)], "currentColor", 1.8)
          + f'<rect x="{bx - 8}" y="{by + 17}" width="16" height="9" fill="none" stroke="currentColor" stroke-width="2"/>')
    b += tx(390, 22, "u = 200cos(100πt) V", "currentColor", 13, "end") + tx(390, 42, "đèn sáng khi |u| ≥ 100√3 V", "currentColor", 12, "end", "600")
    if kk == 0:
        b += runner(curve(f, ncyc, ox, oy, wpx, apx, 32), 6.0)
        return fig("d5-0", "0 0 420 232", "Đồ thị điện áp u theo thời gian với hai đường ngưỡng cam; điểm xanh chạy dọc đồ thị và bóng đèn sáng, tối theo độ lớn của u", b,
                   "Mô phỏng: điểm chạy trên đồ thị u(t), bóng đèn sáng khi |u| không nhỏ hơn ngưỡng (hai đường nét đứt cam); chạy chậm 100 lần (một chu kì ứng với 2 s). " + NOTE)
    b += tx(14, 224, "a) ? ms ; b) ? s ; c) ? ms", ORG, 13)
    return fig("d5-2", "0 0 420 232", "Dữ kiện: đồ thị điện áp u theo thời gian và hai đường ngưỡng ứng với độ lớn điện áp mà đèn bắt đầu sáng", b,
               "Dữ kiện: đèn sáng khi đồ thị nằm ngoài dải giữa hai đường ngưỡng. " + NOTE)
