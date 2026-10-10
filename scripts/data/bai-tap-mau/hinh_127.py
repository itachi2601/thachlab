"""Hình cho bài tập mẫu Bài 16 "Điện từ trường. Mô hình sóng điện từ" (Vật lí 12), lesson_id 127.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mọi đường cong, điểm chạy, góc kim điện kế, vị trí nam châm đều TÍNH từ công thức (lấy mẫu cách đều thời gian, nội suy tuyến tính).
Nhãn chỉ ghi dữ kiện đề cho và dấu "?" cho đại lượng cần tìm; không nhãn kết quả."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
MUTE = "#94a3b8"
TAU = 2 * math.pi
E_COL, B_COL = RED, BLUE          # đúng màu hình 3 trong bài lý thuyết: E đỏ, B xanh dương


def tx(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, s, c, size, anchor, weight)


def smilf(attr, vals, dur, nd=1):
    return f'<animate attributeName="{attr}" values="{";".join(f"{v:.{nd}f}" for v in vals)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


def sine(x0, x1, y0, A, lam, xc, step):
    """y = y0 − A·cos(2π(x − xc)/λ): đỉnh (lên trên màn hình) tại x = xc + kλ."""
    n = int((x1 - x0) / step) + 1
    return [(x0 + i * step, y0 - A * math.cos(TAU * (x0 + i * step - xc) / lam)) for i in range(n)]


def moving(pts, dx, dur, col, w=2.4, extra=""):
    """Nhóm dịch sang phải dx px trong dur giây, chạy một lần khi bấm."""
    return (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;{dx:.1f} 0" dur="{dur}s" begin="indefinite" fill="freeze"/>'
            + poly(pts, col, w) + extra + '</g>')


# ───────────────────────── Dạng 1: nam châm rơi vào ống dây ─────────────────────────
def coil(cx, cy, w=56, h=84):
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2
    b = f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="3" fill="none" stroke="currentColor" stroke-width="2.4"/>'
    for i in range(1, 7):
        y = y0 + i * h / 7
        b += f'<path d="M{x0},{y:.1f} Q{cx},{y + 7:.1f} {x1},{y:.1f}" fill="none" stroke="currentColor" stroke-width="1.4" opacity="0.55"/>'
    return b


def magnet(cx, my):
    """Nam châm thẳng, tâm (cx, my): nửa trên cực N, nửa dưới cực S."""
    return (f'<rect x="{cx - 9}" y="{my - 24}" width="18" height="24" fill="{RED}" fill-opacity="0.35" stroke="currentColor" stroke-width="2"/>'
            f'<rect x="{cx - 9}" y="{my}" width="18" height="24" fill="{BLUE}" fill-opacity="0.35" stroke="currentColor" stroke-width="2"/>'
            + tx(cx, my - 8, "N", "currentColor", 12, "middle") + tx(cx, my + 17, "S", "currentColor", 12, "middle"))


def galv(cx, cy, theta=0.0, animated=None):
    """Điện kế: vòng tròn + vạch 0 + kim (kim xoay quanh tâm). animated = (values, dur) → kim chạy một lần."""
    b = f'<circle cx="{cx}" cy="{cy}" r="22" fill="none" stroke="currentColor" stroke-width="2.4"/>' + seg(cx, cy - 22, cx, cy - 16, "currentColor", 1.6)
    t = math.radians(theta)
    needle = seg(cx, cy, cx + 15 * math.sin(t), cy - 15 * math.cos(t), ORG, 3)
    if animated:
        vals, dur = animated
        needle = (f'<g><animateTransform attributeName="transform" type="rotate" values="{";".join(f"{v:.1f} {cx} {cy}" for v in vals)}" '
                  f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>' + seg(cx, cy, cx, cy - 15, ORG, 3) + '</g>')
    return b + needle + dot(cx, cy, 3, "currentColor")


def scene1(cx, cy, my, theta, animated_magnet=None, animated_needle=None):
    gy = cy + 78
    b = coil(cx, cy)
    b += seg(cx - 28, cy + 42, cx - 28, gy, "currentColor", 2) + seg(cx - 28, gy, cx - 22, gy, "currentColor", 2)
    b += seg(cx + 28, cy + 42, cx + 28, gy, "currentColor", 2) + seg(cx + 28, gy, cx + 22, gy, "currentColor", 2)
    b += galv(cx, gy, theta, animated_needle)
    if animated_magnet:
        b += (f'<g><animateTransform attributeName="transform" type="translate" values="{";".join(f"0 {v:.1f}" for v in animated_magnet[0])}" '
              f'dur="{animated_magnet[1]:.2f}s" begin="indefinite" fill="freeze"/>' + magnet(cx, my) + '</g>')
    else:
        b += magnet(cx, my)
    return b


def d1(k):
    p = f"d1{k}"
    if k == 2:
        b = defs(p)
        b += scene1(105, 100, 80, 38) + arrow(p, "g", 152, 72, 152, 96, 2.4)
        b += scene1(315, 100, 100, 0)
        b += tx(105, 28, "Nam châm đang chuyển động", "currentColor", 13, "middle") + tx(105, 46, "kim điện kế lệch", ORG, 13, "middle")
        b += tx(315, 28, "Nam châm dừng lại trong ống", "currentColor", 13, "middle") + tx(315, 46, "kim điện kế ở vạch 0", ORG, 13, "middle")
        b += tx(160, 92, "v", GRN, 13)
        b += tx(210, 226, "Điện trường trong dây dẫn do đâu? Đường sức dạng nào?", "currentColor", 13, "middle")
        return fig("d1-2", "0 0 420 238", "Hai tình huống: nam châm chuyển động trong ống dây thì kim điện kế lệch, nam châm dừng lại thì kim về vạch 0", b,
                   "Dữ kiện: hai tình huống của đề. " + NOTE)
    # k = 0: nam châm rơi tự do từ z0 = 15 cm tới tâm ống rồi được giữ yên; kim ∝ dΦ/dt với từ thông qua một vòng dây (mô hình lưỡng cực)
    g, z0, R = 9.8, 0.15, 0.04
    Tf = math.sqrt(2 * z0 / g)
    nf, nh = 36, 20
    zs = [z0 - 0.5 * g * (Tf * i / nf) ** 2 for i in range(nf + 1)] + [0.0] * nh
    Phi = lambda z: 1 / (R * R + z * z) ** 1.5
    emf = []
    for i, z in enumerate(zs):
        if i >= nf: emf.append(0.0); continue
        t = Tf * i / nf; zdot = -g * t
        dPhi = (-3 * z / (R * R + z * z) ** 2.5) * zdot
        emf.append(dPhi)
    mx = max(abs(e) for e in emf)
    theta = [42 * e / mx for e in emf]
    cy = 130
    my0 = 40                                  # tâm nam châm lúc đầu (phía trên ống)
    cen = cy                                   # tâm ống
    pos = [cen - (cen - my0) * z / z0 for z in zs]   # tâm nam châm theo z
    dy = [pp - my0 for pp in pos]
    slow = 8
    dt = Tf / nf * slow
    dur = dt * (len(zs) - 1)
    b = defs(p) + scene1(210, cy, my0, 0, (dy, dur), (theta, dur))
    b += tx(300, 40, "Nam châm thẳng", "currentColor", 13) + tx(300, 58, "rơi vào lòng ống", "currentColor", 13)
    b += tx(300, 78, "rồi được giữ yên", "currentColor", 13)
    b += tx(262, 215, "kim điện kế: ?", ORG, 13)
    return fig("d1-0", "0 0 420 250", "Nam châm thẳng rơi vào lòng ống dây nối với điện kế rồi được giữ yên; kim điện kế quay rồi trở về vạch 0", b,
               "Mô phỏng: nam châm rơi vào lòng ống rồi được giữ yên, kim điện kế phản ứng theo (chạy chậm 8 lần). " + NOTE)


# ───────────────────────── Dạng 2: λ, T, f ─────────────────────────
def d2(k):
    p = f"d2{k}"
    lam, A, y0 = 110.0, 26.0, 106
    if k == 2:
        b = defs(p)
        b += poly(sine(30, 390, 64, 20, 150, 105, 3), E_COL, 2.4) + tx(30, 20, "Sóng FM: f = 91 MHz", "currentColor", 13)
        b += tx(300, 20, "λ = ?   T = ?", ORG, 13)
        b += poly(sine(30, 390, 150, 10, 15, 36, 1.2), B_COL, 2) + tx(30, 112, "Hồng ngoại của điều khiển từ xa: λ = 940 nm", "currentColor", 13)
        b += tx(300, 198, "f = ?", ORG, 13)
        b += tx(30, 220, "Coi như truyền trong chân không, tốc độ c", "currentColor", 12, "start", "400")
        return fig("d2-2", "0 0 420 232", "Hai sóng điện từ: sóng FM cho tần số, tia hồng ngoại cho bước sóng", b, "Dữ kiện: hai sóng cùng tốc độ c. " + NOTE)
    xc, px, dur = 60.0, 300.0, 4.0
    curve = sine(-60, 540, y0, A, lam, xc, 3)
    n = 41
    ys = [y0 - A * math.cos(TAU * (px - xc - lam * i / (n - 1)) / lam) for i in range(n)]
    b = defs(p) + '<clipPath id="c127a"><rect x="20" y="40" width="380" height="140"/></clipPath>'
    crest = f'<circle cx="{xc}" cy="{y0 - A}" r="5.5" fill="{ORG}" stroke="currentColor" stroke-width="1.5"/>'
    b += '<g clip-path="url(#c127a)">' + moving(curve, lam, dur, E_COL, 2.4, crest) + '</g>'
    b += seg(px, 46, px, 176, MUTE, 1.2, "4 4")
    b += (f'<circle cx="{px}" cy="{ys[0]:.1f}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">{smilf("cy", ys, dur)}</circle>')
    b += tx(px + 8, 58, "P", GRN, 13)
    b += dim(p, "b", xc, 48, xc + lam, 48, "", 0, 0) + tx(xc + lam / 2, 40, "λ = ?", BLUE, 13, "middle")
    b += tx(20, 20, "Sóng FM: f = 91 MHz", "currentColor", 13) + tx(px + 20, 160, "T = ?", ORG, 13)
    b += arrow(p, "g", 30, 198, 120, 198, 2.4) + tx(128, 203, "cùng tốc độ c", GRN, 13)
    return fig("d2-0", "0 0 420 214", "Sóng FM lan truyền sang phải qua điểm P", b,
               "Mô phỏng: sóng FM lan truyền sang phải, chấm cam đánh dấu một đỉnh sóng, điểm P cố định (chạy chậm hàng tỉ lần). " + NOTE)


# ───────────────────────── Dạng 3: E và B cùng pha ─────────────────────────
def graph(ox, oy, w, a, col, vlab, ncyc=2.0, ph=0.8, per=40):
    """Đồ thị v(t) = cos(2π·u + ph), u = số chu kì từ t = 0. Trả (svg, các điểm)."""
    n = int(per * ncyc)
    pts = [(ox + w * i / n, oy - a * math.cos(TAU * ncyc * i / n + ph)) for i in range(n + 1)]
    b = arrow("", "g", ox - 8, oy, ox + w + 14, oy, 2) + arrow("", "g", ox, oy + a + 12, ox, oy - a - 16, 2)
    b += tx(ox + w + 12, oy + 17, "t", GRN, 13, "end") + tx(ox + 8, oy - a - 8, vlab, col, 13)
    b += poly(pts, col, 2.4)
    return b, pts


def d3(k):
    p = f"d3{k}"
    ox, w, a = 50, 320, 32
    oyE, oyB = 66, 164
    gE, pE = graph(ox, oyE, w, a, E_COL, "E (V/m)")
    gB, pB = graph(ox, oyB, w, a, B_COL, "B (nT)")
    b = defs(p) + gE + gB
    b += tx(ox - 6, oyE - a + 4, "E₀", E_COL, 12, "end") + tx(ox - 6, oyB - a + 4, "B₀", B_COL, 12, "end")
    b += tx(300, 22, "E₀ = 18 V/m", E_COL, 13) + tx(300, 120, "B₀ = 60 nT", B_COL, 13)
    if k == 2:
        b += tx(30, 228, "Cùng một thời điểm:", "currentColor", 13) + tx(30, 248, "E = 6,0 V/m  →  B = ?", ORG, 13)
        b += tx(30, 268, "B = 45 nT  →  E = ?", ORG, 13) + tx(30, 288, "E = 0  →  B = ?", ORG, 13)
        return fig("d3-2", "0 0 420 296", "Đồ thị E và B theo thời gian tại điểm M cùng một trục thời gian", b, "Dữ kiện: giá trị cực đại của E, B và ba thời điểm cần xét. Trục thời gian không ghi số. " + NOTE)
    n = len(pE); dur = 6.0
    b += seg(pE[0][0], oyE - a - 12, pE[0][0], oyB + a + 12, MUTE, 1.2, "4 4").replace("/>", f'>{smilf("x1", [q[0] for q in pE], dur)}{smilf("x2", [q[0] for q in pE], dur)}</line>')
    for pts, col in ((pE, E_COL), (pB, B_COL)):
        b += (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="5.5" fill="{col}" stroke="currentColor" stroke-width="1.5">'
              f'{smilf("cx", [q[0] for q in pts], dur)}{smilf("cy", [q[1] for q in pts], dur)}</circle>')
    return fig("d3-0", "0 0 420 214", "Tại điểm M, cường độ điện trường E và cảm ứng từ B biến thiên điều hoà theo thời gian; hai điểm chạy dọc hai đồ thị", b,
               "Mô phỏng: hai điểm chạy dọc đồ thị E(t) và B(t) tại cùng một điểm M. Trục thời gian không ghi số. " + NOTE)


# ───────────────────────── Dạng 4: đổi môi trường ─────────────────────────
def d4(k):
    p = f"d4{k}"
    xb, A, y0 = 215.0, 26.0, 112
    lL, lR = 72.0, 43.0            # tỉ lệ hai bước sóng trong hình ≠ tỉ lệ thật của đề (hình minh hoạ)
    dur = 4.0
    b = defs(p) + f'<rect x="{xb}" y="46" width="195" height="140" fill="{BLUE}" fill-opacity="0.13"/>'
    b += seg(xb, 46, xb, 186, "currentColor", 1.6)
    left = sine(-80, xb, y0, A, lL, xb, 2)
    right = sine(xb - lR, xb + 200, y0, A, lR, xb, 2)
    b += tx(20, 22, "Chân không: λ₀ = 540 nm", "currentColor", 13) + tx(xb + 8, 40, "Nước: n = 4/3", "currentColor", 13)
    b += tx(20, 206, "f = ?", ORG, 13) + tx(xb + 8, 206, "v = ?", ORG, 13) + tx(xb + 90, 206, "λ' = ?", ORG, 13)
    if k == 2:
        b += poly(sine(20, xb, y0, A, lL, xb, 2), E_COL, 2.4) + poly(sine(xb, 410, y0, A, lR, xb, 2), E_COL, 2.4)
        b += dim(p, "b", xb - 2 * lL, 66, xb - lL, 66, "", 0, 0) + dim(p, "b", xb + lR, 66, xb + 2 * lR, 66, "", 0, 0)
        return fig("d4-2", "0 0 420 218", "Sóng điện từ đi từ chân không vào nước", b, "Dữ kiện: ánh sáng lục từ chân không vào nước. Hình minh hoạ: tỉ lệ hai bước sóng trong hình không đúng với đề.")
    gl = '<clipPath id="c127L"><rect x="20" y="46" width="195" height="140"/></clipPath><g clip-path="url(#c127L)">' + moving(left, lL, dur, E_COL) + '</g>'
    gr = '<clipPath id="c127R"><rect x="215" y="46" width="195" height="140"/></clipPath><g clip-path="url(#c127R)">' + moving(right, lR, dur, E_COL) + '</g>'
    b += gl + gr
    b += dim(p, "b", xb - 2 * lL, 66, xb - lL, 66, "", 0, 0) + dim(p, "b", xb + lR, 66, xb + 2 * lR, 66, "", 0, 0)
    return fig("d4-0", "0 0 420 218", "Sóng điện từ truyền từ chân không vào nước qua mặt phân cách", b,
               "Mô phỏng: sóng đi qua mặt phân cách (chạy chậm hàng tỉ lần). Hình minh hoạ: tỉ lệ hai bước sóng trong hình không đúng với đề.")


# ───────────────────────── Dạng 5: xung tới Mặt Trăng và về ─────────────────────────
def earth_moon(p, x_e=62, x_m=352, y=112):
    b = f'<circle cx="{x_e}" cy="{y}" r="24" fill="{GRN}" fill-opacity="0.2" stroke="currentColor" stroke-width="2.4"/>' + tx(x_e, y + 44, "Trái Đất", "currentColor", 13, "middle")
    b += f'<circle cx="{x_m}" cy="{y}" r="11" fill="{MUTE}" fill-opacity="0.35" stroke="currentColor" stroke-width="2.4"/>' + tx(x_m, y + 44, "Mặt Trăng", "currentColor", 13, "middle")
    b += seg(x_e + 24, y - 6, x_e + 38, y - 6, "currentColor", 2.4) + seg(x_e + 24, y + 6, x_e + 38, y + 6, "currentColor", 2.4)
    return b


def d5(k):
    p = f"d5{k}"
    xe, xm, y = 62, 352, 112
    b = defs(p) + earth_moon(p)
    b += dim(p, "g", xe, 50, xm, 50, "", 0, 0) + tx((xe + xm) / 2, 40, "d = 3,84·10⁸ m", GRN, 13, "middle")
    if k == 2:
        b += arrow(p, "o", xe + 44, y - 16, xm - 20, y - 16, 2.4)
        b += arrow(p, "b", xm - 20, y + 16, xe + 44, y + 16, 2.4)
        b += tx(30, 192, "Lần 1: t = ? (từ phát đến thu)", ORG, 13) + tx(30, 212, "Lần 2: t' = 2,50 s → d' = ?", ORG, 13)
        return fig("d5-2", "0 0 420 222", "Xung vô tuyến đi từ Trái Đất tới Mặt Trăng rồi phản xạ về, khoảng cách d một chiều", b, "Dữ kiện: khoảng cách Trái Đất - Mặt Trăng và thời gian lần đo thứ hai. " + NOTE)
    dur = 4.0
    b += (f'<circle cx="{xe + 46}" cy="{y - 8}" r="5.5" fill="{ORG}" stroke="currentColor" stroke-width="1.5">'
          f'<animate attributeName="cx" values="{xe + 46};{xm - 22};{xm - 22};{xe + 46}" keyTimes="0;0.5;0.5;1" dur="{dur}s" begin="indefinite" fill="freeze"/>'
          f'<animate attributeName="cy" values="{y - 8};{y - 8};{y + 8};{y + 8}" keyTimes="0;0.5;0.5;1" dur="{dur}s" begin="indefinite" fill="freeze"/></circle>')
    b += tx(30, 192, "Xung phát ra từ Trái Đất", "currentColor", 13) + tx(30, 212, "Từ phát đến thu xung phản xạ: t = ?", ORG, 13)
    return fig("d5-0", "0 0 420 222", "Xung vô tuyến đi từ Trái Đất tới Mặt Trăng, phản xạ rồi quay về Trái Đất", b,
               "Mô phỏng: xung đi tới Mặt Trăng rồi quay về (không đúng thời gian thật). " + NOTE)


# ───────────────────────── Dạng 6: thời điểm E = 0 hoặc cực đại ─────────────────────────
def d6(k):
    p = f"d6{k}"
    if k == 2:
        b = tx(24, 32, "B = B₀cos(2π·10⁸·t + π/3)", B_COL, 14)
        b += tx(24, 92, "Lúc t = 0, đối số của cos bằng π/3", "currentColor", 14, "start", "400")
        b += tx(24, 124, "Cần tìm:", "currentColor", 14) + tx(24, 146, "▸  chu kì T", ORG, 14) + tx(24, 168, "▸  thời điểm đầu tiên E = 0", ORG, 14) + tx(24, 190, "▸  thời điểm đầu tiên E cực đại", ORG, 14)
        return fig("d6-2", "0 0 420 204", "Phương trình của B đã cho và ba đại lượng cần tìm", b, "Dữ kiện của đề. " + NOTE)
    lam, A, y0, xM, nper, dur = 100.0, 30.0, 106, 300.0, 2, 8.0
    # E(x, t) = cos(ωt − k(x − xM) + π/3) → tại t = 0, tại M: cos(π/3); sóng đi sang phải
    pts = [(x, y0 - A * math.cos(-TAU * (x - xM) / lam + math.pi / 3)) for x in range(-int(lam * nper) - 40, 420, 4)]
    n = 41
    ys = [y0 - A * math.cos(TAU * nper * i / (n - 1) + math.pi / 3) for i in range(n)]
    b = defs(p) + '<clipPath id="c127b"><rect x="20" y="40" width="380" height="130"/></clipPath>'
    b += '<g clip-path="url(#c127b)">' + moving(pts, lam * nper, dur, E_COL) + '</g>'
    b += seg(xM, 44, xM, 168, MUTE, 1.2, "4 4") + tx(xM + 8, 58, "M", GRN, 13)
    b += (f'<circle cx="{xM}" cy="{ys[0]:.1f}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">{smilf("cy", ys, dur)}</circle>')
    b += tx(20, 22, "Sóng điện từ lan truyền qua điểm M", "currentColor", 13) + tx(20, 192, "B = B₀cos(2π·10⁸·t + π/3)", B_COL, 13)
    b += tx(300, 192, "E tại M: ?", E_COL, 13)
    return fig("d6-0", "0 0 420 204", "Sóng điện từ lan truyền sang phải qua điểm M; cường độ điện trường tại M dao động điều hoà", b,
               "Mô phỏng: đường cong là E dọc phương truyền; điểm M dao động khi sóng đi qua (chạy chậm hàng tỉ lần, không ghi mốc thời gian). " + NOTE)
