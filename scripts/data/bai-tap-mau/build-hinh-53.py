"""Bài 53 — "Bài 8. Chuyển động biến đổi. Gia tốc" (Vật lí 10, chương 2). 5 dạng + tự luận (ví dụ cũ chưa biên tập).
Mẫu: build-hinh-57.py. Chạy: python3 scripts/data/bai-tap-mau/build-hinh-53.py  → ghi scripts/data/bai-tap-mau/53.json"""
import json, math, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "53.json")
OLD = json.load(open(os.path.join(HERE, "old/53.json")))["questions"]
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
TOPIC = "Khái niệm gia tốc và đồ thị vận tốc – thời gian"


# ───────────── Hàm dùng chung của bài 53 ─────────────
def circ(x, y, r=5.5):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{GRN}" stroke="currentColor" stroke-width="1.5"/>'


def varrow(p, X, Y, L, dur):
    """Mũi tên vận tốc đỏ chạy cùng vật: đuôi ở X[i], dài L[i] px (âm = hướng trái). Mờ dần khi v → 0 để khỏi hiện mũi nhọn."""
    op = [min(1.0, abs(l) / 6) for l in L]
    return (f'<line x1="{X[0]:.1f}" y1="{Y:.1f}" x2="{X[0] + L[0]:.1f}" y2="{Y:.1f}" stroke="{RED}" stroke-width="3" marker-end="url(#{p}-r)">'
            + smil("x1", X, dur) + smil("x2", [x + l for x, l in zip(X, L)], dur) + smil("opacity", op, dur) + "</line>")


def ruler(x0, y, scale, vals, size=12):
    b = seg(16, y, 410, y, "currentColor", 2)
    for v in vals:
        x = x0 + scale * v
        b += seg(x, y, x, y + 8, "currentColor", 1.6) + lbl(x, y + 24, str(v), "currentColor", size, "middle", "400")
    return b


def axes_vt(p, ox, oy, sx, sy, tmax, vmax, xt, yt):
    b = arrow(p, "g", ox, oy, ox + sx * tmax + 28, oy, 2) + arrow(p, "g", ox, oy, ox, oy - sy * vmax - 28, 2)
    b += lbl(ox + sx * tmax + 28, oy - 10, "t (s)", GRN, 13, "end", "700") + lbl(ox + 8, oy - sy * vmax - 32, "v (m/s)", GRN, 13, "start", "700")
    for t in xt:
        b += seg(ox + sx * t, oy, ox + sx * t, oy + 5, "currentColor", 1.5) + lbl(ox + sx * t, oy + 19, str(t), "currentColor", 12, "middle", "400")
    for v in yt:
        b += seg(ox - 5, oy - sy * v, ox, oy - sy * v, "currentColor", 1.5) + lbl(ox - 9, oy - sy * v + 4, str(v), "currentColor", 12, "end", "400")
    return b


def graph_dash(ox, oy, sx, sy, verts):
    b = ""
    for t, v in verts:
        if v > 0:
            b += seg(ox, oy - sy * v, ox + sx * t, oy - sy * v, "currentColor", 1, "4 4", .45)
            if t > 0:
                b += seg(ox + sx * t, oy, ox + sx * t, oy - sy * v, "currentColor", 1, "4 4", .45)
    return b


def run_point(ox, oy, sx, sy, ts, vs, spi):
    """Điểm chạy trên đồ thị + vạch đứng xuống trục t (mẫu cách đều thời gian)."""
    X = [ox + sx * t for t in ts]; Y = [oy - sy * v for v in vs]; dur = spi * (len(ts) - 1)
    out = (f'<line x1="{X[0]:.1f}" y1="{Y[0]:.1f}" x2="{X[0]:.1f}" y2="{oy}" stroke="{ORG}" stroke-width="1.8" stroke-dasharray="4 3">'
           + smil("x1", X, dur) + smil("x2", X, dur) + smil("y1", Y, dur) + "</line>")
    out += (f'<circle cx="{X[0]:.1f}" cy="{Y[0]:.1f}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">'
            + smil("cx", X, dur) + smil("cy", Y, dur) + "</circle>")
    return out


def interp(pts, t):
    """Nội suy tuyến tính đồ thị v–t cho bởi các đỉnh (t, v)."""
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        if t0 <= t <= t1:
            return v0 + (v1 - v0) * (t - t0) / (t1 - t0)
    return pts[-1][1]


# ───────────── Dạng 1: xe tải tăng tốc, đổi km/h ─────────────
def d1(k):
    p = f"d1{k}"; sc = 0.75; x0 = 30; ty = 104
    x = lambda t: 5 * t + 0.125 * t * t           # a = 0,25 m/s², v₀ = 5 m/s
    b = defs(p)
    if k == 0:
        ts = list(range(41)); X = [x0 + sc * x(t) for t in ts]; L = [5 * (5 + 0.25 * t) for t in ts]; spi = 0.25
        b += ruler(x0, ty, sc, [0, 100, 200, 300, 400])
        b += lbl(410, ty + 42, "m", "currentColor", 12, "end", "400")
        for t, txt, row, anc in ((0, "v₀ = 18 km/h (lúc tăng ga)", 30, "start"), (20, "20 s: 36 km/h", 56, "middle"), (40, "40 s: v = ?", 30, "end")):
            px = x0 + sc * x(t)
            b += seg(px, row + 6, px, ty - 14, "currentColor", 1.2, "4 4", .6) + lbl(px if anc != "end" else px + 70, row, txt, "currentColor", 13, anc, "700")
        b += varrow(p, X, ty - 8, L, spi * 40) + ball(list(zip(X, [ty - 8] * 41)), 0, spi)
        b += lbl(16, 154, "mũi tên đỏ: vận tốc v", RED, 12, "start", "700")
        return fig("d1-0", "0 0 420 166", "Xe tải tăng tốc đều trên đường thẳng: ở giây 0 chạy 18 km/h, giây 20 chạy 36 km/h, cần tìm vận tốc ở giây 40", b,
                   "Mô phỏng: xe tải từ lúc tăng ga đến giây 40 (chạy nhanh 4 lần, bấm Chạy mô phỏng). Vị trí tính theo công thức; mũi tên đỏ dài tỉ lệ với vận tốc.")
    # k == 2: dữ kiện — bốn thời điểm
    xs = [50, 150, 250, 350]; y = 100
    arrs = [25, 50, None, None]
    b += seg(16, y + 12, 410, y + 12, "currentColor", 2)
    tops = ["18 km/h", "36 km/h", "v = ?", "72 km/h"]; bots = ["t = 0", "t = 20 s", "t = 40 s", "t = ?"]
    for i, px in enumerate(xs):
        b += circ(px, y)
        if arrs[i]: b += arrow(p, "r", px + 7, y, px + arrs[i], y, 3)
        b += lbl(px, y - 26, tops[i], RED if i < 2 else ORG, 13, "middle", "700") + lbl(px, y + 38, bots[i], "currentColor", 13, "middle", "700")
    b += dim(p, "b", xs[0], y + 54, xs[1], y + 54, "Δt = 20 s", (xs[0] + xs[1]) / 2 - 28, y + 74)
    b += lbl(210, 24, "Hai mốc đầu cho a; a không đổi nên dùng tiếp cho các mốc sau", "currentColor", 12, "middle", "400")
    return fig("d1-2", "0 0 420 190", "Bốn thời điểm của xe tải: giây 0 chạy 18 km/h, giây 20 chạy 36 km/h, giây 40 chưa biết, và một thời điểm chưa biết đạt 72 km/h", b,
               "Dữ kiện: hai mốc đầu cho tính gia tốc, hai mốc sau cần tìm. " + NOTE)


# ───────────── Dạng 2: xe máy phanh, đổi chiều dương ─────────────
def d2(k):
    p = f"d2{k}"; sc = 12; x0 = 30; ty = 102
    b = defs(p)
    if k == 0:
        ts = [i * 0.1 for i in range(41)]; xm = [10 * t - 1.25 * t * t for t in ts]; X = [x0 + sc * m for m in xm]
        L = [5.5 * (10 - 2.5 * t) for t in ts]; spi = 0.1
        b += ruler(x0, ty, sc, [0, 5, 10, 15, 20, 25]) + lbl(410, ty + 42, "m", "currentColor", 12, "end", "400")
        b += seg(x0, 52, x0, ty - 14, "currentColor", 1.2, "4 4", .6) + lbl(x0, 46, "v₀ = 36 km/h (lúc bắt đầu phanh)", "currentColor", 13, "start", "700")
        b += lbl(410, 24, "sau 4 s: dừng lại", "currentColor", 13, "end", "700")
        b += varrow(p, X, ty - 8, L, spi * 40) + ball(list(zip(X, [ty - 8] * 41)), 0, spi)
        b += lbl(16, 154, "mũi tên đỏ: vận tốc v", RED, 12, "start", "700")
        return fig("d2-0", "0 0 420 166", "Xe máy chạy 36 km/h phanh gấp, chậm dần đều và dừng sau 4 giây", b,
                   "Mô phỏng: xe máy phanh (đúng thời gian thật, 4 s; bấm Chạy mô phỏng). Mũi tên đỏ ngắn dần theo vận tốc.")
    y = 106
    b += seg(16, y + 12, 410, y + 12, "currentColor", 2) + circ(70, y) + arrow(p, "r", 77, y, 150, y, 3)
    b += lbl(70, y + 36, "v (chiều chuyển động)", RED, 13, "start", "700")
    b += arrow(p, "g", 120, 40, 200, 40, 2.4) + lbl(206, 45, "① chọn chiều dương →", GRN, 13, "start", "700")
    b += arrow(p, "g", 200, 72, 120, 72, 2.4) + lbl(206, 77, "② chọn chiều dương ←", GRN, 13, "start", "700")
    b += arrow(p, "b", 63, y, 20, y, 2.4) + lbl(16, y - 14, "a ngược chiều v (chậm dần)", BLUE, 12, "start", "700")
    return fig("d2-2", "0 0 420 170", "Xe máy chạy sang phải, vectơ gia tốc hướng ngược lại; hai cách chọn chiều dương: sang phải hoặc sang trái", b,
               "Dữ kiện: chậm dần thì gia tốc ngược chiều vận tốc; dấu của v và a còn phụ thuộc chiều dương chọn. " + NOTE)


# ───────────── Dạng 3: đọc đồ thị v–t (tàu điện) ─────────────
PT3 = [(0, 0), (6, 12), (16, 12), (24, 0)]
def d3(k):
    p = f"d3{k}"; ox, oy, sx, sy = 56, 205, 13, 10
    b = defs(p) + axes_vt(p, ox, oy, sx, sy, 24, 12, [0, 6, 16, 24], [12]) + graph_dash(ox, oy, sx, sy, PT3[1:])
    b += poly([(ox + sx * t, oy - sy * v) for t, v in PT3], GRN, 3)
    b += lbl(ox + 14, oy - 62, "①", ORG, 16, "middle", "700") + lbl(ox + sx * 11, oy - sy * 12 - 12, "②", ORG, 16, "middle", "700") + lbl(ox + sx * 20 + 16, oy - 62, "③", ORG, 16, "middle", "700")
    if k == 0:
        ts = [i * 0.5 for i in range(49)]; vs = [interp(PT3, t) for t in ts]
        b += run_point(ox, oy, sx, sy, ts, vs, 0.25)
        return fig("d3-0", "0 0 420 232", "Đồ thị v–t gồm ba đoạn thẳng ①②③", b,
                   "Mô phỏng: điểm chạy trên đồ thị v–t (chạy nhanh 2 lần, bấm Chạy mô phỏng); vạch cam đứng cho biết thời điểm hiện tại.")
    b += lbl(ox + 110, oy - sy * 12 - 50, "chiều dương: chiều chuyển động (v > 0)", "currentColor", 12, "start", "400")
    b += lbl(ox + sx * 3 + 34, oy - 20, "Δv / Δt ?", ORG, 13, "start", "700") + lbl(ox + sx * 11, oy - sy * 12 + 22, "nằm ngang", ORG, 12, "middle", "700") + lbl(ox + sx * 19.5, oy - 34, "Δv / Δt ?", ORG, 13, "end", "700")
    return fig("d3-2", "0 0 420 232", "Đồ thị gồm ba đoạn thẳng: đoạn một đi lên, đoạn hai nằm ngang, đoạn ba đi xuống; mỗi đoạn có một độ dốc riêng", b,
               "Dữ kiện: ba đoạn thẳng, mỗi đoạn một giai đoạn với gia tốc riêng. " + NOTE)


# ───────────── Dạng 4: quãng đường = diện tích dưới đồ thị ─────────────
PT4 = [(0, 0), (8, 12), (20, 12), (30, 0)]
def d4(k):
    p = f"d4{k}"; ox, oy, sx, sy = 56, 175, 10.5, 9
    b = defs(p) + axes_vt(p, ox, oy, sx, sy, 30, 12, [0, 8, 20, 30], [12]) + graph_dash(ox, oy, sx, sy, PT4[1:])
    poly_area = f'<polygon points="{ox},{oy} {ox + sx * 8},{oy - sy * 12} {ox + sx * 20},{oy - sy * 12} {ox + sx * 30},{oy}" fill="{GRN}" opacity=".3"/>'
    line = poly([(ox + sx * t, oy - sy * v) for t, v in PT4], GRN, 3)
    if k == 0:
        ts = [i * 0.5 for i in range(61)]; vs = [interp(PT4, t) for t in ts]; spi = 1 / 6; dur = spi * 60
        cum = [0.0]
        for i in range(1, len(ts)): cum.append(cum[-1] + 0.5 * (vs[i] + vs[i - 1]) * 0.5)
        clip = f'<clipPath id="{p}-clip"><rect x="{ox}" y="20" width="0" height="170">{smil("width", [sx * t for t in ts], dur)}</rect></clipPath>'
        b += clip + f'<g clip-path="url(#{p}-clip)">{poly_area}</g>' + line
        b += lbl(ox + sx * 14, oy - sy * 12 - 12, "t (s): 0 · 8 · 20 · 30", "currentColor", 12, "middle", "400")
        b += run_point(ox, oy, sx, sy, ts, vs, spi)
        ty = 252; px = [ox + 315 * c / cum[-1] for c in cum]
        b += seg(16, ty + 12, 410, ty + 12, "currentColor", 2) + lbl(ox, ty + 34, "vị trí xe trên đường (không ghi tỉ lệ)", "currentColor", 12, "start", "400")
        b += ball(list(zip(px, [ty] * 61)), 0, spi)
        return fig("d4-0", "0 0 420 290", "Đồ thị vận tốc theo thời gian của xe máy gồm ba đoạn thẳng, phần diện tích dưới đồ thị được tô dần và xe chạy trên đường phía dưới", b,
                   "Mô phỏng: diện tích dưới đồ thị tô dần theo thời gian, xe chạy trên đường bên dưới (chạy nhanh 3 lần, bấm Chạy mô phỏng).")
    b += poly_area + line
    b += seg(ox + sx * 8, oy, ox + sx * 8, oy - sy * 12, "currentColor", 1.2, "4 3", .8) + seg(ox + sx * 20, oy, ox + sx * 20, oy - sy * 12, "currentColor", 1.2, "4 3", .8)
    b += lbl(ox + sx * 3.2, oy - 22, "S₁", ORG, 14, "middle", "700") + lbl(ox + sx * 14, oy - 40, "S₂", ORG, 14, "middle", "700") + lbl(ox + sx * 25, oy - 22, "S₃", ORG, 14, "middle", "700")
    b += lbl(ox + sx * 14, oy - sy * 12 - 12, "s = S₁ + S₂ + S₃", ORG, 12, "middle", "700")
    return fig("d4-2", "0 0 420 232", "Diện tích dưới đồ thị chia thành ba phần S₁, S₂, S₃", b,
               "Dữ kiện: quãng đường bằng diện tích dưới đồ thị v–t. " + NOTE)


# ───────────── Dạng 5: bóng tennis đập tường, đổi hướng ─────────────
def d5(k):
    p = f"d5{k}"; b = defs(p)
    if k == 0:
        sc = 20; x0 = 40; dt = 0.0125; ts = [i * dt for i in range(69)]
        def xv(t):
            if t <= 0.4: return 25 * t, 25.0
            if t <= 0.45:
                tau = t - 0.4; return 10 + 25 * tau - 400 * tau * tau, 25 - 800 * tau
            return 10.25 - 15 * (t - 0.45), -15.0
        xm = [xv(t)[0] for t in ts]; vm = [xv(t)[1] for t in ts]; X = [x0 + sc * m for m in xm]; y = 115; spi = dt * 5; dur = spi * 68
        wx = x0 + sc * 10.25 + 5.5
        b += seg(16, y + 6, 410, y + 6, "currentColor", 2) + f'<rect x="{wx:.1f}" y="62" width="12" height="{y + 6 - 62}" fill="none" stroke="currentColor" stroke-width="2.2"/>' + lbl(wx + 6, 54, "tường", "currentColor", 13, "middle", "700")
        b += lbl(x0, 98, "25 m/s →", "currentColor", 13, "start", "700") + lbl(x0 + sc * 4.25 - 6, 98, "← 15 m/s", "currentColor", 13, "start", "700") + lbl(wx + 18, 98, "va chạm 0,05 s", ORG, 13, "start", "700")
        b += lbl(16, 24, "vận tốc v:", RED, 13, "start", "700") + lbl(410, 24, "chiều dương: đông →", GRN, 13, "end", "700")
        b += seg(230, 14, 230, 38, "currentColor", 1, "3 3", .5)
        b += varrow(p, [230.0] * 69, 31, [3 * v for v in vm], dur) + ball(list(zip(X, [y - 0.5] * 69)), 0, spi)
        return fig("d5-0", "0 0 420 150", "Quả bóng tennis bay sang phải với tốc độ 25 m/s, đập vào tường rồi bật lại sang trái với tốc độ 15 m/s, thời gian va chạm 0,05 s", b,
                   "Mô phỏng: bóng đập tường (chạy chậm 5 lần, bấm Chạy mô phỏng). Mũi tên đỏ ở trên là vận tốc v, đổi chiều khi bóng bật lại.")
    wx = 330
    b += f'<rect x="{wx}" y="56" width="12" height="118" fill="none" stroke="currentColor" stroke-width="2.2"/>' + lbl(wx + 6, 48, "tường", "currentColor", 13, "middle", "700")
    b += arrow(p, "g", 60, 30, 130, 30, 2.4) + lbl(136, 35, "chiều dương: đông", GRN, 13, "start", "700")
    b += lbl(16, 104, "trước", "currentColor", 13, "start", "700") + circ(100, 100) + arrow(p, "r", 108, 100, 188, 100, 3) + lbl(100, 80, "25 m/s, hướng đông", RED, 13, "start", "700")
    b += lbl(16, 154, "sau", "currentColor", 13, "start", "700") + circ(260, 150) + arrow(p, "r", 252, 150, 200, 150, 3) + lbl(260, 130, "15 m/s, hướng tây", RED, 13, "end", "700")
    b += lbl(wx - 8, 108, "Δt = 0,05 s", ORG, 13, "end", "700")
    return fig("d5-2", "0 0 420 190", "Trước va chạm bóng bay hướng đông 25 m/s, sau va chạm bay hướng tây 15 m/s, chiều dương chọn là hướng đông", b,
               "Dữ kiện: hai vận tốc ngược hướng; chiều dương chọn trước rồi mới lấy dấu. " + NOTE)


BUILD = [d1, d2, d3, d4, d5]

# ───────────── Phân tích đề ─────────────
ANALYSIS = [
 [("\"đang chạy … 18 km/h\"", "$v_1=18$ km/h", "Đổi $\\text{km/h}\\to\\text{m/s}$: chia $3{,}6$"),
  ("\"vận tốc tăng đều\"", "$a$ không đổi, $\\vec a$ cùng chiều $\\vec v$", "⚠ Nhanh dần đều: $a$ không đổi nên dùng được cho mọi mốc thời gian"),
  ("\"sau 20 s, vận tốc đạt 36 km/h\"", "$\\Delta t=20$ s; $v_2=36$ km/h", "$a=\\dfrac{\\Delta v}{\\Delta t}=\\dfrac{v_2-v_1}{\\Delta t}$"),
  ("\"Tính gia tốc của xe\"", "Cần $a$ (đơn vị $\\text{m/s}^2$)", "Công thức định nghĩa gia tốc"),
  ("\"vận tốc sau 40 s kể từ lúc tăng ga\"", "$\\Delta t=40$ s; cần $v$", "Rút từ định nghĩa: $v=v_1+a\\Delta t$"),
  ("\"sau bao lâu … đạt 72 km/h\"", "$v=72$ km/h; cần $\\Delta t$", "$\\Delta t=\\dfrac{v-v_1}{a}$")],
 [("\"đang chạy … 36 km/h\"", "$v_1=36$ km/h", "Đổi $\\text{km/h}\\to\\text{m/s}$: chia $3{,}6$"),
  ("\"phanh gấp … chậm dần đều\"", "$a$ không đổi; $\\vec a$ ngược chiều $\\vec v$", "⚠ Chậm dần: $a\\cdot v\\lt0$ (xét tích, không xét riêng dấu $a$)"),
  ("\"dừng lại sau 4 s\"", "$v_2=0$; $\\Delta t=4$ s", "$a=\\dfrac{v_2-v_1}{\\Delta t}$"),
  ("\"chọn chiều dương là chiều chuyển động\"", "$v_1\\gt0$", "$v$ lấy dấu theo chiều dương đã chọn"),
  ("\"chọn chiều dương ngược chiều chuyển động\"", "$v_1\\lt0$", "⚠ Dấu của $v$ và $a$ phụ thuộc chiều dương đã chọn"),
  ("\"vận tốc sau 2 s\"", "$\\Delta t=2$ s; cần $v$", "$v=v_1+a\\Delta t$ ($a$ không đổi)")],
 [("\"đồ thị vận tốc – thời gian\"", "Ba đoạn thẳng ①②③", "Mỗi đoạn thẳng là một giai đoạn có $a$ riêng"),
  ("\"chiều dương là chiều chuyển động\"", "$v\\gt0$ suốt quá trình", "⚠ Đồ thị đi lên: nhanh dần; nằm ngang: thẳng đều; đi xuống: chậm dần"),
  ("\"mô tả chuyển động từng giai đoạn\"", "Dạng của đoạn thẳng", "Độ dốc $\\gt0$, $=0$, $\\lt0$"),
  ("\"tính gia tốc từng giai đoạn\"", "Hai điểm đầu–cuối mỗi đoạn", "$a=\\dfrac{\\Delta v}{\\Delta t}=\\dfrac{v_2-v_1}{t_2-t_1}$ (độ dốc)"),
  ("\"giai đoạn nào gia tốc lớn nhất\"", "So sánh độ lớn $|a|$", "Dốc nhất thì $|a|$ lớn nhất"),
  ("\"lúc $t=18$ s nhanh hay chậm dần\"", "$t=18$ s thuộc đoạn nào", "Xét dấu $a\\cdot v$ trong đoạn đó")],
 [("\"vận tốc ghi tại các mốc 0; 8; 20; 30 s\"", "$(0;0)$, $(8;12)$, $(20;12)$, $(30;0)$", "Nối các mốc: đồ thị $v$–$t$ gồm ba đoạn thẳng"),
  ("\"giữa hai mốc … thay đổi đều\"", "Mỗi đoạn $a$ không đổi", "⚠ Chỉ dùng $a=\\dfrac{\\Delta v}{\\Delta t}$ cho từng đoạn, không cho cả 30 s"),
  ("\"tính chất chuyển động từng giai đoạn\"", "Dạng ba đoạn", "Lên: nhanh dần; ngang: đều; xuống: chậm dần"),
  ("\"gia tốc trong 8 s đầu và 10 s cuối\"", "$\\Delta v$ và $\\Delta t$ của hai đoạn", "$a=\\dfrac{\\Delta v}{\\Delta t}$"),
  ("\"quãng đường … bằng diện tích\"", "$v\\ge0$ suốt 30 s", "⚠ Xe không đổi chiều nên quãng đường $=$ diện tích dưới đồ thị"),
  ("\"tốc độ trung bình trong 30 s\"", "Cần $s$ và $t$", "$v_{tb}=\\dfrac{s}{t}$")],
 [("\"bay … 25 m/s về phía đông\"", "$|v_1|=25$ m/s, hướng đông", "Vận tốc là vectơ: có độ lớn và hướng"),
  ("\"bật lại … 15 m/s về phía tây\"", "$|v_2|=15$ m/s, hướng tây", "⚠ Đổi hướng: $v_1$ và $v_2$ trái dấu khi chọn một chiều dương"),
  ("\"thời gian va chạm 0,05 s\"", "$\\Delta t=0{,}05$ s", "$a=\\dfrac{\\Delta v}{\\Delta t}$ (gia tốc trung bình)"),
  ("\"sự thay đổi tốc độ\"", "Chỉ so hai độ lớn", "$\\Delta(\\text{tốc độ})=|v_2|-|v_1|$"),
  ("\"sự thay đổi vận tốc\"", "Chọn chiều dương, lấy dấu", "$\\Delta v=v_2-v_1$ (hiệu có dấu)"),
  ("\"gia tốc trong thời gian tiếp xúc\"", "Cần $a$ và hướng của nó", "$a$ cùng hướng với $\\Delta v$")],
]

RN1 = ["<strong>Khái niệm:</strong> gia tốc đặc trưng cho độ biến thiên của vận tốc theo thời gian.",
       "<strong>Công thức:</strong> $a=\\dfrac{\\Delta v}{\\Delta t}=\\dfrac{v_2-v_1}{\\Delta t}$ (đơn vị $\\text{m/s}^2$)",
       "Rút ra: $v_2=v_1+a\\Delta t$ · $\\Delta t=\\dfrac{v_2-v_1}{a}$",
       "⚠ <strong>Điều kiện:</strong> nhanh dần đều ($a$ không đổi); đổi $\\text{km/h}\\to\\text{m/s}$: chia $3{,}6$."]
RN2 = ["<strong>Khái niệm:</strong> nhanh dần: $\\vec a$ cùng chiều $\\vec v$ ($a\\cdot v\\gt0$); chậm dần: ngược chiều ($a\\cdot v\\lt0$).",
       "<strong>Công thức:</strong> $a=\\dfrac{v_2-v_1}{\\Delta t}$ · $v=v_1+a\\Delta t$",
       "⚠ <strong>Điều kiện:</strong> chọn chiều dương trước; $v$ và $a$ lấy dấu theo chiều dương đó.",
       "Tính chất chuyển động chỉ phụ thuộc dấu của tích $a\\cdot v$."]
RN3 = ["<strong>Khái niệm:</strong> đồ thị $v$–$t$ của chuyển động thẳng biến đổi đều là đoạn thẳng xiên.",
       "Ngang: thẳng đều ($a=0$) · lên: nhanh dần · xuống: chậm dần ($v\\gt0$).",
       "<strong>Công thức:</strong> $a=\\dfrac{\\Delta v}{\\Delta t}$ = độ dốc đoạn thẳng.",
       "⚠ <strong>Điều kiện:</strong> mỗi đoạn thẳng một giai đoạn, tính $a$ riêng từng đoạn."]
RN4 = ["<strong>Khái niệm:</strong> diện tích dưới đồ thị $v$–$t$ là độ dịch chuyển.",
       "Xe không đổi chiều: độ dịch chuyển $=$ quãng đường $s$.",
       "<strong>Công thức:</strong> tam giác $\\dfrac{1}{2}\\cdot$đáy$\\cdot$cao · hình thang $\\dfrac{1}{2}(a+b)h$ · $v_{tb}=\\dfrac{s}{t}$",
       "⚠ <strong>Điều kiện:</strong> $v\\ge0$ suốt thời gian xét (không đổi chiều)."]
RN5 = ["<strong>Khái niệm:</strong> vận tốc là vectơ; đổi hướng cũng là đổi vận tốc. Tốc độ chỉ là độ lớn.",
       "<strong>Công thức:</strong> $a=\\dfrac{\\Delta v}{\\Delta t}=\\dfrac{v_2-v_1}{\\Delta t}$",
       "⚠ <strong>Điều kiện:</strong> chọn chiều dương trước; bật ngược lại thì $v_2$ và $v_1$ trái dấu.",
       "$\\Delta v$ là hiệu có dấu, khác hiệu hai tốc độ."]

SOLS = [
 sol(RN1, [
  ("Đổi đơn vị", [P("Chia cho $3{,}6$:"), M(r"v_1=\dfrac{18}{3{,}6}=5\ \text{m/s}"), M(r"v_2=\dfrac{36}{3{,}6}=10\ \text{m/s}"), M(r"v_3=\dfrac{72}{3{,}6}=20\ \text{m/s}")]),
  ("Gia tốc", [P("Chọn chiều dương là chiều chuyển động:"), M(r"a=\dfrac{v_2-v_1}{\Delta t}=\dfrac{10-5}{20}"), A(r"a=0{,}25\ \text{m/s}^2")]),
  ("Vận tốc sau 40 s", [P("$a$ không đổi, $\\Delta t=40$ s tính từ lúc tăng ga:"), M(r"v=v_1+a\Delta t=5+0{,}25\cdot40"), A(r"v=15\ \text{m/s}"), M(r"15\cdot3{,}6=54\ \text{km/h}")]),
  ("Thời gian đạt 72 km/h", [M(r"\Delta t=\dfrac{v_3-v_1}{a}=\dfrac{20-5}{0{,}25}"), A(r"\Delta t=60\ \text{s}")]),
  ("Kiểm tra", [P("Mỗi giây vận tốc tăng $0{,}25\\ \\text{m/s}$: sau 20 s tăng $5$ (5 → 10 ✓), sau 60 s tăng $15$ (5 → 20 ✓)."), P("Đơn vị: $\\text{m/s}^2\\cdot\\text{s}=\\text{m/s}$ ✓")])],
  ["a) $a=0{,}25\\ \\text{m/s}^2$", "b) $v=15\\ \\text{m/s}$ (54 km/h)", "c) $\\Delta t=60\\ \\text{s}$"],
  "Nhận dạng: đề cho <strong>hai vận tốc và khoảng thời gian</strong> (có km/h) → đổi sang m/s, tính $a$ từ định nghĩa rồi dùng lại $a$ cho các mốc khác."),
 sol(RN2, [
  ("Đổi đơn vị", [M(r"v=\dfrac{36}{3{,}6}=10\ \text{m/s}")]),
  ("Chiều dương cùng chiều chuyển động", [P("$v_1=+10$ m/s; dừng lại nên $v_2=0$:"), M(r"a=\dfrac{v_2-v_1}{\Delta t}=\dfrac{0-10}{4}"), A(r"a=-2{,}5\ \text{m/s}^2"), P("$v\\gt0$, $a\\lt0$ nên $a\\cdot v\\lt0$: chậm dần ✓")]),
  ("Chiều dương ngược chiều chuyển động", [P("Bây giờ $v_1=-10$ m/s, $v_2=0$:"), M(r"a=\dfrac{0-(-10)}{4}"), A(r"a=+2{,}5\ \text{m/s}^2"), P("$v\\lt0$, $a\\gt0$ nên $a\\cdot v\\lt0$: vẫn chậm dần."), P("Hai cách cùng $|a|=2{,}5\\ \\text{m/s}^2$, chỉ khác dấu.")]),
  ("Vận tốc sau 2 s phanh", [P("$a$ không đổi, $\\Delta t=2$ s. Cách 1:"), M(r"v=v_1+a\Delta t=10+(-2{,}5)\cdot2"), A(r"v=5\ \text{m/s}"), P("Cách 2 cho $v=-10+2{,}5\\cdot2=-5$ m/s: cùng độ lớn, dấu âm chỉ nói xe đi ngược chiều dương đã chọn.")]),
  ("Kiểm tra", [P("Phanh 4 s mất $10$ m/s thì 2 s mất một nửa, còn $5$ m/s ✓.")])],
  ["a) $a=-2{,}5\\ \\text{m/s}^2$ ($v\\gt0$, $a\\lt0$)", "b) $a=+2{,}5\\ \\text{m/s}^2$ ($v\\lt0$, $a\\gt0$), vẫn chậm dần", "c) $v=+5\\ \\text{m/s}$"],
  "Nhận dạng: đề hỏi <strong>dấu của $a$</strong> khi xe hãm hoặc đổi chiều dương → xét tích $a\\cdot v$, không gán \"$a$ âm là chậm dần\"."),
 sol(RN3, [
  ("Chia giai đoạn theo đoạn thẳng", [P("① từ 0 đến 6 s: $v$ từ $0$ lên $12$ m/s."), P("② từ 6 đến 16 s: $v$ giữ $12$ m/s."), P("③ từ 16 đến 24 s: $v$ từ $12$ xuống $0$.")]),
  ("Giai đoạn ①", [M(r"a_1=\dfrac{12-0}{6-0}"), A(r"a_1=2\ \text{m/s}^2"), P("Đồ thị đi lên: nhanh dần đều.")]),
  ("Giai đoạn ②", [M(r"a_2=\dfrac{12-12}{16-6}"), A(r"a_2=0"), P("Đồ thị nằm ngang: thẳng đều với $v=12$ m/s.")]),
  ("Giai đoạn ③", [M(r"a_3=\dfrac{0-12}{24-16}"), A(r"a_3=-1{,}5\ \text{m/s}^2"), P("Đồ thị đi xuống: chậm dần đều, tàu dừng lại.")]),
  ("So sánh và xét $t=18$ s", [P("$|a_1|=2\\gt|a_3|=1{,}5$: đoạn ① dốc nhất, tàu tăng tốc mạnh hơn hãm."), P("$t=18$ s thuộc ③:"), M(r"v=12+a_3\cdot(18-16)=12-1{,}5\cdot2=9\ \text{m/s}"), P("$v\\gt0$, $a\\lt0$ nên $a\\cdot v\\lt0$: chậm dần.")]),
  ("Kiểm tra", [P("Đơn vị: $\\dfrac{\\text{m/s}}{\\text{s}}=\\text{m/s}^2$ ✓. Đi xuống ↔ $a$ âm ✓.")])],
  ["a) ① nhanh dần đều · ② thẳng đều · ③ chậm dần đều rồi dừng", "b) $a_1=2$ · $a_2=0$ · $a_3=-1{,}5\\ \\text{m/s}^2$", "c) ① có $|a|$ lớn nhất; lúc $t=18$ s: chậm dần"],
  "Nhận dạng: đề cho <strong>đồ thị $v$–$t$ gồm nhiều đoạn thẳng</strong> → tách giai đoạn, tính độ dốc từng đoạn, xét dấu $a\\cdot v$."),
 sol(RN4, [
  ("Dựng đồ thị từ các mốc", [P("Ba đoạn thẳng: ① $0\\to8$ s, $v$: $0\\to12$; ② $8\\to20$ s, $v=12$; ③ $20\\to30$ s, $v$: $12\\to0$."), P("① nhanh dần đều, ② thẳng đều, ③ chậm dần đều rồi dừng.")]),
  ("Gia tốc hai đoạn", [M(r"a_1=\dfrac{12-0}{8}"), A(r"a_1=1{,}5\ \text{m/s}^2"), M(r"a_3=\dfrac{0-12}{30-20}"), A(r"a_3=-1{,}2\ \text{m/s}^2")]),
  ("Quãng đường: ba phần diện tích", [M(r"S_1=\dfrac{1}{2}\cdot8\cdot12=48\ \text{m}"), M(r"S_2=(20-8)\cdot12=144\ \text{m}"), M(r"S_3=\dfrac{1}{2}\cdot10\cdot12=60\ \text{m}"), M(r"s=S_1+S_2+S_3=48+144+60"), A(r"s=252\ \text{m}")]),
  ("Kiểm tra bằng hình thang", [P("Đáy lớn $30$ (cả thời gian), đáy nhỏ $12$ (giai đoạn đều), cao $12$:"), M(r"s=\dfrac{1}{2}(30+12)\cdot12=252\ \text{m}"), P("Hai cách cùng kết quả ✓")]),
  ("Tốc độ trung bình", [M(r"v_{tb}=\dfrac{s}{t}=\dfrac{252}{30}"), A(r"v_{tb}=8{,}4\ \text{m/s}"), P("Nhỏ hơn $12$ m/s (tốc độ lớn nhất) ✓")])],
  ["a) ① nhanh dần đều · ② thẳng đều · ③ chậm dần đều", "b) $a_1=1{,}5$ · $a_3=-1{,}2\\ \\text{m/s}^2$", "c) $s=252\\ \\text{m}$", "d) $v_{tb}=8{,}4\\ \\text{m/s}$"],
  "Nhận dạng: đề hỏi <strong>quãng đường</strong> khi cho đồ thị hoặc bảng $v$–$t$ → chia diện tích thành tam giác, chữ nhật, hình thang."),
 sol(RN5, [
  ("Độ biến thiên tốc độ", [P("Chỉ so hai độ lớn:"), M(r"|v_2|-|v_1|=15-25"), A(r"-10\ \text{m/s}"), P("Tốc độ giảm $10$ m/s.")]),
  ("Độ biến thiên vận tốc", [P("Chọn chiều dương hướng đông: $v_1=+25$ m/s, $v_2=-15$ m/s."), M(r"\Delta v=v_2-v_1=-15-25"), A(r"\Delta v=-40\ \text{m/s}"), P("Độ lớn $40$ m/s, hướng tây.")]),
  ("Gia tốc", [M(r"a=\dfrac{\Delta v}{\Delta t}=\dfrac{-40}{0{,}05}"), A(r"a=-800\ \text{m/s}^2"), P("Dấu âm: $\\vec a$ hướng tây, cùng hướng với $\\Delta\\vec v$, ra xa tường.")]),
  ("Kiểm tra", [P("Nếu lấy nhầm $\\Delta v=-10$ thì $a=-200\\ \\text{m/s}^2$: sai, vì bỏ qua việc đổi hướng."), P("$800\\ \\text{m/s}^2\\approx82g$: rất lớn vì $\\Delta t$ chỉ $0{,}05$ s ✓")])],
  ["a) tốc độ giảm $10\\ \\text{m/s}$", "b) $\\Delta v=-40\\ \\text{m/s}$ (hướng tây)", "c) $a=-800\\ \\text{m/s}^2$ (hướng tây)"],
  "Nhận dạng: vật <strong>bật lại hoặc quay đầu</strong> → chọn chiều dương trước, $v_1$ và $v_2$ trái dấu, $\\Delta v$ là hiệu có dấu."),
]

# ───────────── Đề chữ (hình mô phỏng do BUILD chèn dưới đề) ─────────────
DANG = [
 dict(label="Dạng 1 · Dễ · Tính gia tốc từ hai vận tốc, đổi km/h", topic=TOPIC,
      problem_html="<p>Một ô tô tải đang chạy thẳng trên đường với vận tốc $18\\ \\text{km/h}$ thì tăng ga, vận tốc tăng đều. Sau $20\\ \\text{s}$ kể từ lúc tăng ga, vận tốc đạt $36\\ \\text{km/h}$.</p>"
                   "<ol type=\"a\"><li>Tính gia tốc của xe.</li><li>Tính vận tốc của xe sau $40\\ \\text{s}$ kể từ lúc tăng ga.</li><li>Kể từ lúc tăng ga, sau bao lâu xe đạt $72\\ \\text{km/h}$?</li></ol>"),
 dict(label="Dạng 2 · Trung bình · Xe phanh: dấu của gia tốc và chiều dương", topic=TOPIC,
      problem_html="<p>Một xe máy đang chạy thẳng với vận tốc $36\\ \\text{km/h}$ thì người lái phanh gấp. Xe chuyển động chậm dần đều và dừng lại sau $4\\ \\text{s}$.</p>"
                   "<ol type=\"a\"><li>Chọn chiều dương là chiều chuyển động của xe. Tính gia tốc và cho biết dấu của $v$, $a$.</li>"
                   "<li>Chọn chiều dương ngược chiều chuyển động của xe. Tính lại gia tốc và dấu của $v$, $a$. Xe có còn chậm dần không?</li>"
                   "<li>Giả sử gia tốc không đổi, vận tốc của xe sau $2\\ \\text{s}$ kể từ lúc bắt đầu phanh là bao nhiêu (chọn chiều dương như câu a)?</li></ol>"),
 dict(label="Dạng 3 · Trung bình · Đọc đồ thị v–t: gia tốc từng giai đoạn", topic=TOPIC,
      problem_html="<p>Một đoàn tàu điện chạy trên đường thẳng, đồ thị vận tốc – thời gian của tàu gồm ba đoạn thẳng ①, ②, ③ như hình dưới. Chọn chiều dương là chiều chuyển động của tàu.</p>"
                   "<ol type=\"a\"><li>Mô tả chuyển động của tàu trong từng giai đoạn.</li><li>Tính gia tốc của tàu trong từng giai đoạn.</li>"
                   "<li>Giai đoạn nào gia tốc có độ lớn lớn nhất? Lúc $t=18\\ \\text{s}$ tàu chuyển động nhanh dần hay chậm dần?</li></ol>"),
 dict(label="Dạng 4 · Trung bình · Quãng đường từ diện tích dưới đồ thị v–t", topic=TOPIC,
      problem_html="<p>Vận tốc của một xe máy trên đường thẳng được ghi tại các mốc: $t=0$: $v=0$; $t=8\\ \\text{s}$: $v=12\\ \\text{m/s}$; $t=20\\ \\text{s}$: $v=12\\ \\text{m/s}$; $t=30\\ \\text{s}$: $v=0$. Giữa hai mốc liên tiếp vận tốc thay đổi đều theo thời gian.</p>"
                   "<ol type=\"a\"><li>Nhận xét tính chất chuyển động của xe trong từng giai đoạn.</li><li>Tính gia tốc của xe trong $8\\ \\text{s}$ đầu và trong $10\\ \\text{s}$ cuối.</li>"
                   "<li>Dùng diện tích dưới đồ thị, tính quãng đường xe đi được trong $30\\ \\text{s}$.</li><li>Tính tốc độ trung bình của xe trong $30\\ \\text{s}$.</li></ol>"),
 dict(label="Dạng 5 · Khó · Vật đổi hướng: độ biến thiên vận tốc và gia tốc", topic=TOPIC,
      problem_html="<p>Một quả bóng tennis đang bay ngang với tốc độ $25\\ \\text{m/s}$ theo hướng đông thì đập vuông góc vào tường và bật lại với tốc độ $15\\ \\text{m/s}$ theo hướng tây. Thời gian va chạm giữa bóng và tường là $0{,}05\\ \\text{s}$ (số liệu minh hoạ).</p>"
                   "<ol type=\"a\"><li>Tính độ biến thiên tốc độ của quả bóng.</li><li>Chọn chiều dương hướng đông, tính độ biến thiên vận tốc của quả bóng.</li>"
                   "<li>Tính gia tốc trung bình của bóng trong thời gian va chạm và cho biết hướng của gia tốc.</li></ol>"),
]

# ───────────── Tự luận: ví dụ cũ chưa biên tập (idx 0-based trong old/53.json), xếp dễ → khó ─────────────
# Đã biên tập thành dạng: VD11(idx10)→D1, VD10(idx9)→D2, VD6(idx5)→D3, VD18(idx17)→D4, VD9(idx8)→D5.
ORDER = [2, 7, 0, 6, 1, 13, 15, 11, 14, 18, 3, 4, 16]   # bỏ idx12 (VD13: đáp án không đối chiếu được với hình)
MUC = {2: "Dễ", 7: "Dễ", 0: "Dễ", 6: "Dễ", 1: "Trung bình", 13: "Trung bình", 12: "Trung bình", 15: "Trung bình", 11: "Trung bình",
       14: "Trung bình", 3: "Trung bình", 18: "Trung bình", 4: "Khó", 16: "Nâng cao"}
import re
def _math(m):
    t = re.sub(r"(?<=\d),(?=\d)", "{,}", m.group(0))
    t = re.sub(r"(\d)\s*(c?m|km)/(s|h)\^\{?2\}?", r"\1\\ \\text{\2/\3}^{2}", t)
    t = re.sub(r"(\d)\s*(c?m|km)/(s|h)(?![\w^])", r"\1\\ \\text{\2/\3}", t)
    return t
for _q in OLD:
    _q["body_html"] = re.sub(r"\$[^$]*\$", _math, _q["body_html"])
# VD5: a_C = (3-4)/(3,5-3) khó theo dõi → (2-4)/(4-3) (đồ thị: v = 4 tại t = 3, v = 2 tại t = 4)
assert "\\frac{3-4}{3{,}5-3}" in OLD[4]["body_html"]
OLD[4]["body_html"] = OLD[4]["body_html"].replace("\\frac{3-4}{3{,}5-3}", "\\frac{2-4}{4-3}")
# VD17: đề hỏi độ dịch chuyển (III), lời giải a = (0-4)/20 → t = 20 s
assert "d_{3}=v_{03}t+\\frac{1}{2}a_{3}t^{2}=4t-0{,}1t^{2}$" in OLD[16]["body_html"]
OLD[16]["body_html"] = OLD[16]["body_html"].replace("d_{3}=v_{03}t+\\frac{1}{2}a_{3}t^{2}=4t-0{,}1t^{2}$", "d_{3}=v_{03}t+\\frac{1}{2}a_{3}t^{2}=4t-0{,}1t^{2}$; tại $t=20\\ \\text{s}$: $d_{3}=4\\cdot20-0{,}1\\cdot20^{2}=40\\ \\text{m}$")
TU_LUAN = tu_luan_tu(OLD, ORDER, MUC)

write(J, 53, "Bài 8. Chuyển động biến đổi. Gia tốc", DANG, BUILD, ANALYSIS, SOLS, TU_LUAN)
