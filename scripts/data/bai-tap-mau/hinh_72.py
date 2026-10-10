"""Hình cho bài tập mẫu Bài 27 "Hiệu suất" (Vật lí 10), lesson_id 72.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.

Mô phỏng là minh hoạ ĐỊNH TÍNH hiện tượng (không có thanh/độ dài/số hạt tỉ lệ với năng lượng nên không đo được đáp số):
  d1 máy khoan: mũi khoan quay, vỏ máy nóng dần, tiếng ồn · d2 máy bơm đẩy nước lên bể · d3 xe đạp điện chạy, moay-ơ nóng dần ·
  d4 tời kéo thùng vữa lên đều (quỹ đạo tuyến tính, đúng chuyển động đều) · d5 gói năng lượng đi qua ba khâu nối tiếp, mỗi khâu nóng dần.
Mọi nhãn chỉ ghi dữ kiện của đề; đại lượng cần tìm ghi dấu "?". Không dùng marker mũi tên (arrow() vẽ đầu V 30°)."""
import math, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

GREY = "#94a3b8"
N = 48                                     # số mẫu của mỗi hoạt hình


def L(x, y, s, c="currentColor", size=13, anchor="start", weight="600"):
    """Nhãn, hỗ trợ chỉ số dưới dạng X_{tp}."""
    k = len(re.findall(r"_\{[^}]*\}", s))
    s = re.sub(r"_\{([^}]*)\}", r'<tspan dy="3" font-size="%d">\1</tspan><tspan dy="-3">' % max(12, size - 1), s)
    return lbl(x, y, s + "</tspan>" * k, c, size, anchor, weight)


def rect(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0):
    r = f' rx="{rx}"' if rx else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"{r} fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'


def circ(x, y, r, c="currentColor", sw=2, fill="none", op=1):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}" opacity="{op}"/>'


def rot(content, ang_deg, cx, cy, dur):
    vals = ";".join(f"{a:.2f} {cx:.1f} {cy:.1f}" for a in ang_deg)
    return (f'<g><animateTransform attributeName="transform" type="rotate" values="{vals}" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>{content}</g>')


def shift(content, pts, dur):
    """Nhóm tịnh tiến theo danh sách (dx, dy) cách đều thời gian."""
    vals = ";".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return (f'<g><animateTransform attributeName="transform" type="translate" values="{vals}" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>{content}</g>')


def path_pt(pts, u):
    seg_len = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    d = u * sum(seg_len)
    for i, s in enumerate(seg_len):
        if d <= s or i == len(seg_len) - 1:
            f = 0 if s == 0 else min(1, d / s)
            return pts[i][0] + f * (pts[i + 1][0] - pts[i][0]), pts[i][1] + f * (pts[i + 1][1] - pts[i][1])
        d -= s


def run_dots(pts, c, dur, n=4, gap=0.14, r=4.5):
    """n gói năng lượng/giọt nước nối đuôi nhau chạy dọc đường gấp khúc pts (đều theo thời gian), rồi biến mất ở cuối."""
    span = 1 - (n - 1) * gap
    out = ""
    for k in range(n):
        xs, ys, op = [], [], []
        for i in range(N + 1):
            u = (i / N - k * gap) / span
            x, y = path_pt(pts, min(1, max(0, u)))
            xs.append(x); ys.append(y); op.append(1.0 if 0 < u < 1 else 0.0)
        out += (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="{r}" fill="{c}" opacity="0">'
                f'{smil("cx", xs, dur)}{smil("cy", ys, dur)}{smil("opacity", op, dur)}</circle>')
    return out


def glow(x, y, w, h, f, dur, peak=0.45, rx=8):
    """Lớp nóng dần màu cam bắt đầu ở thời điểm f (0..1 của thời gian chạy), tăng trong 25 % thời gian rồi giữ."""
    vals = [0.0 if i / N < f else min(peak, (i / N - f) / 0.25 * peak) for i in range(N + 1)]
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{ORG}" opacity="0">'
            f'{smil("opacity", vals, dur)}</rect>')


def glow_c(x, y, r, f, dur, peak=0.5):
    vals = [0.0 if i / N < f else min(peak, (i / N - f) / 0.25 * peak) for i in range(N + 1)]
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{ORG}" opacity="0">{smil("opacity", vals, dur)}</circle>'


def lin(a, b):
    return [a + (b - a) * i / N for i in range(N + 1)]


# ───────────── Dạng 1 · máy khoan: nhận 150 kJ, có ích 105 kJ ─────────────
def d1(kk):
    dur = 6.0
    body = rect(150, 80, 100, 50, "currentColor", 2.4, "none", 10)
    grip = '<path d="M172,130 L164,188 L206,188 L214,130" fill="none" stroke="currentColor" stroke-width="2.4"/>'
    chuck_c = (268, 105)
    spokes = "".join(seg(chuck_c[0], chuck_c[1], chuck_c[0] + 13 * math.cos(math.radians(a)), chuck_c[1] + 13 * math.sin(math.radians(a)), "currentColor", 2) for a in (0, 90, 180, 270))
    chuck = circ(*chuck_c, 14, "currentColor", 2.2)
    bit = seg(282, 105, 348, 105, "currentColor", 3)
    flutes = "".join(seg(290 + 12 * k, 100, 298 + 12 * k, 110, "currentColor", 1.4) for k in range(5))
    wood = rect(346, 72, 52, 66, "currentColor", 2)
    st = body + grip + chuck + wood + L(8, 76, "điện năng nhận vào", "currentColor", 12, "start", "400") + L(8, 92, "W_{tp} = 150 kJ", BLUE, 13, "start", "700")
    st += arrow("d1", "b", 8, 106, 148, 106, 2.4)
    st += L(222, 62, "cơ năng quay mũi khoan", "currentColor", 12, "start", "400") + L(222, 48, "W_{ci} = 105 kJ", GRN, 13, "start", "700")
    st += L(234, 168, "hao phí: W_{hp} = ?", ORG, 13, "start", "700") + L(234, 186, "(nhiệt, tiếng ồn, rung)", "currentColor", 12, "start", "400")
    vb = "0 0 420 210"
    if kk == 0:
        b = glow(150, 80, 100, 50, 0.1, dur, 0.4, 10) + glow(164, 130, 50, 58, 0.2, dur, 0.25, 6)
        # tiếng ồn: hai cung nhấp nháy bên phải tay cầm
        for rr, ph in ((10, 0), (18, 1)):
            vals = [1.0 if (int(i / N * 6) + ph) % 2 == 0 else 0.15 for i in range(N + 1)]
            b += (f'<path d="M{220 + rr * 0.3:.1f},{160 - rr} A{rr},{rr} 0 0 1 {220 + rr * 0.3:.1f},{160 + rr}" fill="none" stroke="{ORG}" stroke-width="2" opacity="0">'
                  f'{smil("opacity", vals, dur)}</path>')
        b += st
        b += rot(spokes, lin(0, 1440), *chuck_c, dur)
        b += shift(bit + flutes, [(x, 0) for x in lin(0, 14)], dur)
        return fig("d1-0", vb, "Máy khoan cầm tay chạy điện nhận 150 kJ điện năng, 105 kJ thành cơ năng quay mũi khoan, phần còn lại làm vỏ máy nóng lên và phát tiếng ồn", b,
                   "Mô phỏng minh hoạ định tính, chạy 6 s: mũi khoan quay và ăn vào gỗ, vỏ máy nóng dần (cam), phát tiếng ồn. Không vẽ theo tỉ lệ năng lượng.")
    b = st + spokes + bit + flutes
    return fig("d1-2", vb, "Dữ kiện: máy khoan nhận 150 kJ, có ích 105 kJ, hao phí chưa biết", b,
               "Dữ kiện câu a: điện năng nhận vào 150 kJ; cơ năng có ích 105 kJ; hao phí cần tìm. Hình không vẽ theo tỉ lệ năng lượng.")


# ───────────── Dạng 2 · máy bơm: nhận 540 kJ, 405 kJ truyền cho nước, 5 phút ─────────────
def d2(kk):
    dur = 6.0
    pump = rect(150, 172, 74, 44, "currentColor", 2.4, "none", 6) + L(187, 199, "máy bơm", "currentColor", 12, "middle", "700")
    pipe_pts = [(172, 172), (172, 62), (292, 62)]
    pipe = poly(pipe_pts, GREY, 6, "", 0.9)
    intake = poly([(100, 205), (150, 205)], GREY, 6, "", 0.9)
    pond = rect(10, 168, 92, 62, "currentColor", 2) + seg(14, 182, 98, 182, BLUE, 2.4, "", 0.8)
    tank = rect(292, 30, 116, 70, "currentColor", 2)
    ground_ = seg(10, 232, 410, 232, "currentColor", 2)
    elec = arrow("d2", "b", 330, 195, 226, 195, 2.4)
    st = pond + intake + pipe + pump + tank + ground_ + elec
    st += L(246, 170, "điện năng nhận vào", "currentColor", 12, "start", "400") + L(246, 186, "W_{tp} = 540 kJ", BLUE, 13, "start", "700")
    st += L(14, 28, "cơ năng truyền cho nước", "currentColor", 12, "start", "400") + L(14, 44, "W_{ci} = 405 kJ", GRN, 13, "start", "700")
    st += L(246, 224, "thời gian bơm: 5 phút", "currentColor", 12, "start", "400")
    vb = "0 0 420 244"
    if kk == 0:
        fill_vals = lin(100, 62)
        water = (f'<rect x="293" y="100" width="114" height="0" fill="{BLUE}" opacity="0.45"><animate attributeName="height" values="{";".join(f"{100 - y:.1f}" for y in fill_vals)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'
                 f'<animate attributeName="y" values="{";".join(f"{y:.1f}" for y in fill_vals)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></rect>')
        b = glow(150, 172, 74, 44, 0.15, dur, 0.5, 6) + water + st + run_dots(pipe_pts, BLUE, dur, 5, 0.12)
        return fig("d2-0", vb, "Máy bơm nhận điện năng 540 kJ trong 5 phút và đẩy nước từ ao lên bể cao; cơ năng truyền cho nước là 405 kJ", b,
                   "Mô phỏng minh hoạ định tính, 5 phút ứng với 6 s: nước (xanh) được bơm lên bể, vỏ máy nóng dần (cam). Số giọt và mực nước không vẽ theo tỉ lệ năng lượng.")
    b = st
    b += L(14, 120, "H = ?", ORG, 13, "start", "700")
    return fig("d2-2", vb, "Dữ kiện: máy bơm nhận 540 kJ trong 5 phút, truyền cho nước 405 kJ", b,
               "Dữ kiện: điện năng nhận vào 540 kJ, cơ năng truyền cho nước 405 kJ, bơm trong 5 phút. Hình không vẽ theo tỉ lệ năng lượng.")


# ───────────── Dạng 3 · xe đạp điện: H = 80 %, P_tp = 250 W, W_ci = 144 kJ ─────────────
def d3(kk):
    dur = 6.0
    R = 24
    def wheel(cx, cy, spin):
        rim = circ(cx, cy, R, "currentColor", 2.4)
        sp = "".join(seg(cx, cy, cx + (R - 3) * math.cos(math.radians(a)), cy + (R - 3) * math.sin(math.radians(a)), GREY, 1.4) for a in (0, 60, 120, 180, 240, 300))
        return rim + (rot(sp, lin(0, 400), cx, cy, dur) if spin else sp)
    def bike(spin):
        rear, front = (50, 150), (122, 150)
        bb, seat, head = (84, 150), (76, 108), (112, 108)
        fr = (seg(*rear, *seat, "currentColor", 2.4) + seg(*bb, *seat, "currentColor", 2.4) + seg(*bb, *head, "currentColor", 2.4)
              + seg(*seat, *head, "currentColor", 2.4) + seg(*head, *front, "currentColor", 2.4) + seg(*head, 116, 96, "currentColor", 2.4))
        fr += seg(66, 106, 88, 106, "currentColor", 3.2)                         # yên
        fr += rect(77, 118, 11, 22, GRN, 2, "none", 2)                              # pin
        rider = seg(80, 104, 90, 72, "currentColor", 2.4) + circ(93, 62, 8, "currentColor", 2.2) + seg(90, 78, 116, 96, "currentColor", 2.2) + seg(84, 104, 94, 128, "currentColor", 2.2) + seg(94, 128, 86, 150, "currentColor", 2.2)
        return wheel(*rear, spin) + wheel(*front, spin) + fr + rider
    ground_ = seg(10, 176, 410, 176, "currentColor", 2)
    legend = L(10, 18, "hiệu suất động cơ: H = 80 %", ORG, 13, "start", "700") + L(10, 36, "a) điện động cơ nhận: P_{tp} = 250 W", "currentColor", 13, "start", "600") \
        + L(10, 54, "b) công có ích cần: W_{ci} = 144 kJ", "currentColor", 13, "start", "600")
    vb = "0 0 420 196"
    if kk == 0:
        mv = [(x, 0) for x in lin(0, 240)]
        b = ground_ + legend + shift(bike(True) + glow_c(50, 150, 12, 0.1, dur, 0.55), mv, dur)
        return fig("d3-0", vb, "Xe đạp điện chạy trên đường; động cơ đặt ở moay-ơ bánh sau, hiệu suất 80 %", b,
                   "Mô phỏng minh hoạ định tính, chạy 6 s: xe chạy, bánh quay, moay-ơ có động cơ (cam) nóng dần. Quãng đường vẽ không dùng khi giải.")
    b = ground_ + legend + bike(False) + glow_c(50, 150, 12, 0.0, dur, 0.0)
    return fig("d3-2", vb, "Dữ kiện: hiệu suất động cơ 80 %, điện động cơ nhận 250 W, công có ích cần 144 kJ", b,
               "Dữ kiện: H = 80 %; câu a cho công suất điện, câu b cho công có ích. Hình không dùng để đo.")


# ───────────── Dạng 4 · tời kéo thùng vữa: 350 kg, 12 m, 24 s, điện 2,5 kW ─────────────
def d4(kk):
    dur = 8.0                                # 24 s thật, phát nhanh gấp 3
    px, py = 250, 52
    pul_r = 10
    ground_y = 270
    S = 14.5                                  # px / m
    top0 = ground_y - 24                       # đỉnh thùng lúc đầu (thùng cao 24 px)
    beam = seg(200, 40, 316, 40, "currentColor", 3) + seg(316, 40, 316, ground_y, "currentColor", 3)
    pulley_c = circ(px, py, pul_r, "currentColor", 2.4)
    spokes = seg(px - 8, py, px + 8, py, GREY, 1.6) + seg(px, py - 8, px, py + 8, GREY, 1.6)
    winch = rect(268, 238, 40, 32, "currentColor", 2.4, "none", 4) + L(288, 258, "tời", "currentColor", 12, "middle", "700")
    rope_r = seg(px + pul_r, py, px + pul_r, 238, "currentColor", 1.8)
    ground_ = seg(10, ground_y, 410, ground_y, "currentColor", 2)
    hfin = 12 * S                              # quãng đường thùng đi
    ytop_f = top0 - hfin
    st = beam + pulley_c + winch + rope_r + ground_
    # thước chiều cao h bên trái
    ruler = dim("d4", "o", 180, ground_y - 6, 180, ytop_f + 12, "", 0, 0)
    leg_ = L(188, (ground_y + ytop_f) / 2 + 40, "h = 12 m", ORG, 13, "start", "700")
    info = L(10, 100, "m = 350 kg", "currentColor", 13, "start", "700") + L(10, 120, "nâng đều", "currentColor", 12, "start", "400") + L(10, 140, "trong t = 24 s", "currentColor", 13, "start", "700")
    info2 = L(322, 224, "P_{tp} = 2,5 kW", BLUE, 13, "start", "700")
    vb = "0 0 420 290"
    box = lambda y: rect(px - pul_r - 14, y, 28, 24, "currentColor", 2.4, "none", 3) + L(px - pul_r, y + 17, "m", "currentColor", 13, "middle", "700")
    if kk == 0:
        ys = lin(top0, ytop_f)
        thung = (f'<g><animateTransform attributeName="transform" type="translate" values="{";".join(f"0 {y - top0:.1f}" for y in ys)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'
                 f'{box(top0)}</g>')
        rope_l = (f'<line x1="{px - pul_r}" y1="{py}" x2="{px - pul_r}" y2="{top0}" stroke="currentColor" stroke-width="1.8">'
                  f'<animate attributeName="y2" values="{";".join(f"{y:.1f}" for y in ys)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></line>')
        b = st + info + info2 + ruler + leg_ + rope_l + thung + rot(spokes, lin(0, -720), px, py, dur)
        b += glow(268, 238, 40, 32, 0.1, dur, 0.5, 4)
        return fig("d4-0", vb, "Tời điện kéo đều thùng vữa 350 kg lên cao 12 m trong 24 s qua ròng rọc cố định; động cơ tời tiêu thụ điện 2,5 kW", b,
                   "Mô phỏng chạy nhanh gấp 3 lần (8 s ứng với 24 s thật): thùng lên đều, ròng rọc quay, động cơ tời nóng dần (cam). Thùng và dây không vẽ theo tỉ lệ đề.")
    b = st + info + info2 + ruler + leg_ + seg(px - pul_r, py, px - pul_r, top0, "currentColor", 1.8) + box(top0)
    b += L(10, 160, "W_{ci} = ?   H = ?", ORG, 13, "start", "700")
    return fig("d4-2", vb, "Dữ kiện: thùng 350 kg nâng đều lên 12 m trong 24 s, tời tiêu thụ 2,5 kW", b,
               "Dữ kiện: nâng đều thùng 350 kg lên 12 m trong 24 s; công suất điện tiêu thụ 2,5 kW. Hình không vẽ theo tỉ lệ.")


# ───────────── Dạng 5 · xe điện: pin → bộ điều khiển (95 %) → động cơ (80 %) → hộp số (75 %) → bánh xe ─────────────
def d5(kk):
    dur = 6.0
    xs = [(6, 52), (84, 76), (180, 76), (276, 76)]            # (x, w) pin + ba khâu
    y0, h = 70, 62
    mid = y0 + h / 2
    names = [("Pin", None), ("Bộ điều", "khiển"), ("Động", "cơ"), ("Hộp", "số")]
    parts = ""
    for (x, w), (a, b_) in zip(xs, names):
        parts += rect(x, y0, w, h, "currentColor", 2.4, "none", 8)
        if b_:
            parts += L(x + w / 2, mid - 3, a, "currentColor", 13, "middle", "700") + L(x + w / 2, mid + 14, b_, "currentColor", 13, "middle", "700")
        else:
            parts += L(x + w / 2, mid + 5, a, "currentColor", 13, "middle", "700")
    wx = 398
    parts += circ(wx, mid, 22, "currentColor", 2.4) + circ(wx, mid, 4, "currentColor", 2, "currentColor") + L(wx, y0 + h + 34, "bánh xe", "currentColor", 12, "middle", "400")
    arrows = (arrow("d5", "b", 58, mid, 82, mid, 2.2) + arrow("d5", "b", 160, mid, 178, mid, 2.2)
              + arrow("d5", "b", 256, mid, 274, mid, 2.2) + arrow("d5", "b", 352, mid, 374, mid, 2.2))
    hs = L(xs[1][0] + 38, y0 - 10, "H₁ = 95 %", GRN, 13, "middle", "700") + L(xs[2][0] + 38, y0 - 10, "H₂ = 80 %", GRN, 13, "middle", "700") + L(xs[3][0] + 38, y0 - 10, "H₃ = 75 %", GRN, 13, "middle", "700")
    ends = L(6, y0 + h + 34, "W_{tp} = ?", ORG, 13, "start", "700") + L(424, y0 - 30, "W_{ci} = 5,7 kJ", GRN, 13, "end", "700")
    ends += L(210, 20, "ba khâu nối tiếp", "currentColor", 12, "middle", "400")
    st = parts + arrows + hs + ends
    vb = "0 0 430 200"
    if kk == 0:
        pts = [(32, mid), (398, mid)]
        b = glow(*[xs[1][0], y0, xs[1][1], h], 0.25, dur, 0.45, 8) + glow(*[xs[2][0], y0, xs[2][1], h], 0.45, dur, 0.45, 8) + glow(*[xs[3][0], y0, xs[3][1], h], 0.65, dur, 0.45, 8)
        b += st + run_dots(pts, BLUE, dur, 5, 0.12, 5)
        return fig("d5-0", vb, "Hệ truyền động xe điện: pin, bộ điều khiển hiệu suất 95 %, động cơ 80 %, hộp số 75 %, rồi tới bánh xe", b,
                   "Mô phỏng minh hoạ định tính, chạy 6 s: gói năng lượng (xanh dương) đi lần lượt qua từng khâu, mỗi khâu nóng dần (cam) khi năng lượng đi qua. Hình chỉ minh hoạ, không vẽ theo tỉ lệ năng lượng.")
    return fig("d5-2", vb, "Dữ kiện: ba khâu nối tiếp hiệu suất 95 %, 80 %, 75 %; bánh xe nhận 5,7 kJ", st,
               "Dữ kiện: hiệu suất ba khâu và cơ năng có ích 5,7 kJ ở bánh xe; điện năng pin cấp cần tìm.")


BUILD = [d1, d2, d3, d4, d5]
