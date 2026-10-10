"""Hình cho bài tập mẫu Bài 31 "Động học của chuyển động tròn đều" (Vật lí 10), lesson_id 76.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mọi vị trí tính thật từ công thức góc = ω·t (mẫu cách đều thời gian, nội suy tuyến tính); KHÔNG vẽ vectơ vận tốc,
KHÔNG ghi đáp số (chỉ dữ kiện của đề và dấu "?").
D1 xe quay ngược chiều kim đồng hồ từ A (đúng 5,0 s thật) · D2 vòng đu quay 5 vòng/120 s chạy nhanh 20 lần ·
D3 đĩa ổ cứng 7200 vòng/phút chạy chậm 1000 lần · D4 đĩa than 45 vòng/phút đúng thời gian thật (4 s) ·
D5 cánh quạt 480 vòng/phút chạy chậm 40 lần."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from svg_lib import chevron

GREY = "#94a3b8"
TAU = 2 * math.pi


def rad(a):
    return math.radians(a)


def circ(cx, cy, r, c=GRN, w=2.2, dash="", fill="none", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def on_circle(cx, cy, r, ang):
    """Điểm trên đường tròn tại góc ang (rad), ngược chiều kim đồng hồ trên màn hình, 0 = bên phải."""
    return (cx + r * math.cos(ang), cy - r * math.sin(ang))


def mover(pts, spi, fill=ORG, r=6):
    """Quả cầu chạy theo pts (mẫu cách đều thời gian, spi giây phát mỗi khoảng); dừng ở khung cuối."""
    dur = spi * (len(pts) - 1)
    return (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="{r}" fill="{fill}" stroke="currentColor" stroke-width="1.6">'
            f'{smil("cx", [p[0] for p in pts], dur)}{smil("cy", [p[1] for p in pts], dur)}</circle>')


def rod(o, pts, spi, c="currentColor", w=2.4, op=1):
    """Thanh từ O (cố định) tới điểm chạy theo pts."""
    dur = spi * (len(pts) - 1)
    return (f'<line x1="{o[0]:.1f}" y1="{o[1]:.1f}" x2="{pts[0][0]:.1f}" y2="{pts[0][1]:.1f}" stroke="{c}" stroke-width="{w}" opacity="{op}">'
            f'{smil("x2", [p[0] for p in pts], dur)}{smil("y2", [p[1] for p in pts], dur)}</line>')


def curved_arrow(cx, cy, r, a0, a1, c="currentColor", w=2):
    """Cung mũi tên chỉ chiều quay NGƯỢC chiều kim đồng hồ, từ góc a0 đến a1 (độ)."""
    x1, y1 = on_circle(cx, cy, r, rad(a1))
    tx, ty = -math.sin(rad(a1)), -math.cos(rad(a1))
    return arc(cx, cy, r, a0, a1, c, w) + chevron(x1, y1, tx, ty, c, w, 9)


def ts(x, y, base, sb, tail="", c="currentColor", size=13, anchor="start", weight="700"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{base}<tspan dy="4" font-size="{size - 3}">{sb}</tspan><tspan dy="-4">{tail}</tspan></text>')


def sam(w, t_end, dt, cx, cy, r, ph=0.0, sign=1):
    """Các điểm trên đường tròn bán kính r, góc = ph + sign·w·t, t = 0..t_end bước dt."""
    n = int(round(t_end / dt))
    return [on_circle(cx, cy, r, ph + sign * w * dt * i) for i in range(n + 1)]


# ───────────── Dạng 1: xe đồ chơi, r = 0,50 m, v = 0,40 m/s ngược chiều kim đồng hồ từ A ─────────────
def d1(kk):
    cx, cy, R = 135.0, 125.0, 95.0
    w = 0.40 / 0.50                                   # ω = v/r = 0,8 rad/s
    b = circ(cx, cy, R) + seg(cx, cy, cx + R, cy, GREY, 1.5, "4 4", .9)
    b += dot(cx, cy, 3.5) + lbl(cx - 8, cy + 20, "O", "currentColor", 13, "end", "700")
    b += dot(cx + R, cy, 4) + lbl(cx + R + 10, cy + 5, "A", "currentColor", 13, "start", "700")
    b += lbl(cx + R / 2, cy - 8, "r = 0,50 m", "currentColor", 12, "middle", "700")
    b += curved_arrow(cx, cy, R + 16, 108, 150, "currentColor", 2)
    b += lbl(272, 62, "Đồng hồ tốc độ", "currentColor", 13, "start", "600") + lbl(272, 82, "luôn chỉ 0,40 m/s", RED, 13, "start", "700")
    b += lbl(272, 118, "Xe chạy ngược chiều", "currentColor", 13, "start", "600") + lbl(272, 138, "kim đồng hồ", "currentColor", 13, "start", "600")
    b += lbl(272, 176, "t = 5,0 s:  s = ?", "currentColor", 13, "start", "700") + lbl(272, 196, "θ = ?", RED, 13, "start", "700")
    if kk == 0:
        pts = sam(w, 5.0, 0.1, cx, cy, R)              # đúng 5,0 s thật
        b += mover(pts, 0.1)
        return fig("d1-0", "0 0 420 250", "Xe đồ chơi chạy ngược chiều kim đồng hồ trên đường ray tròn bán kính 0,50 m, xuất phát từ điểm A bên phải tâm O", b,
                   "Mô phỏng: xe chạy từ A với tốc độ không đổi 0,40 m/s (chạy đúng thời gian thật, dừng ở t = 5,0 s). Chỉ vẽ quỹ đạo và chiều quay, không vẽ vectơ.")
    return fig("d1-2", "0 0 420 250", "Đường ray tròn tâm O bán kính 0,50 m; xe đi qua điểm A bên phải tâm, ngược chiều kim đồng hồ", b,
               "Dữ kiện: đường ray tròn tâm O, bán kính 0,50 m; xe đi qua A (xa nhất về bên phải) theo chiều ngược kim đồng hồ.")


# ───────────── Dạng 2: vòng đu quay 5 vòng trong 120 s ─────────────
def d2(kk):
    cx, cy, R = 135.0, 112.0, 85.0
    b = seg(cx, cy, cx - 42, 212, "currentColor", 3) + seg(cx, cy, cx + 42, 212, "currentColor", 3) + seg(cx - 72, 212, cx + 72, 212, "currentColor", 3)
    b += circ(cx, cy, R)
    b += dot(cx, cy, 5) + lbl(cx + 9, cy - 9, "O", "currentColor", 13, "start", "700")
    b += lbl(250, 62, "Vòng đu quay", "currentColor", 13, "start", "600") + lbl(250, 82, "5 vòng trong 2,0 phút", RED, 13, "start", "700")
    b += lbl(250, 118, "Cabin xuất phát từ", "currentColor", 13, "start", "600") + lbl(250, 138, "vị trí thấp nhất", "currentColor", 13, "start", "600")
    b += lbl(250, 176, "t = 10 s:  θ = ?", "currentColor", 13, "start", "700")
    w = TAU * 5 / 120.0                                 # chỉ để dựng hình; ω thật do học sinh tính
    if kk == 0:
        pts = sam(w, 120.0, 1.0, cx, cy, R, ph=-math.pi / 2)    # 120 s mô phỏng (5 vòng), phát trong 6 s
        b += rod((cx, cy), pts, 0.05, "currentColor", 2.2, .85) + mover(pts, 0.05)
        return fig("d2-0", "0 0 420 232", "Vòng đu quay quay đều 5 vòng; một cabin xuất phát từ vị trí thấp nhất, bán kính nối cabin quay quanh trục O", b,
                   "Mô phỏng: cabin đi đủ 5 vòng (chạy nhanh gấp 20 lần: 6 s thay cho 2,0 phút). Hình dừng ở vị trí xuất phát.")
    b += seg(cx, cy, cx, cy + R, "currentColor", 1.8, "5 4", .9) + dot(cx, cy + R, 5, ORG)
    return fig("d2-2", "0 0 420 232", "Vòng đu quay tâm O, cabin ở vị trí thấp nhất lúc bắt đầu tính thời gian", b,
               "Dữ kiện: vòng đu quay quay đều; cabin xuất phát từ vị trí thấp nhất. Hình không vẽ vị trí sau 10 s.")


# ───────────── Dạng 3: đĩa ổ cứng 7200 vòng/phút, chạy chậm 1000 lần ─────────────
def d3(kk):
    cx, cy, R = 135.0, 120.0, 88.0
    b = circ(cx, cy, R, "currentColor", 2.4) + circ(cx, cy, R - 22, GREY, 1.2, "", "none", .8) + circ(cx, cy, R - 44, GREY, 1.2, "", "none", .8)
    b += circ(cx, cy, 14, "currentColor", 2.0) + dot(cx, cy, 3)
    b += lbl(cx - 20, cy + 5, "O", "currentColor", 13, "end", "700")
    b += lbl(250, 62, "Đĩa của ổ cứng", "currentColor", 13, "start", "600") + lbl(250, 82, "7200 vòng/phút", RED, 13, "start", "700")
    b += lbl(250, 118, "f = ?   T = ? (ms)", "currentColor", 13, "start", "700") + lbl(250, 140, "ω = ?", "currentColor", 13, "start", "700")
    b += lbl(250, 178, "t = 1,0 ms:  θ = ?", RED, 13, "start", "700")
    w = TAU * 7200 / 60.0 / 1000.0                       # chạy chậm 1000 lần
    if kk == 0:
        pts = sam(w, 8.0, 0.1, cx, cy, R - 10, ph=rad(90))
        b += rod((cx, cy), pts, 0.1, "currentColor", 2.2, .85) + mover(pts, 0.1)
        return fig("d3-0", "0 0 420 240", "Đĩa ổ cứng quay đều quanh tâm O; một điểm đánh dấu gần mép đi theo đường tròn", b,
                   "Mô phỏng: đĩa thật quay quá nhanh để nhìn, nên hình chạy chậm 1000 lần (8 s ứng với 8 ms). Điểm đánh dấu xuất phát ở đỉnh đĩa.")
    p0 = on_circle(cx, cy, R - 10, rad(90))
    b += seg(cx, cy, p0[0], p0[1], "currentColor", 2.2, "", .9) + dot(p0[0], p0[1], 5, ORG)
    return fig("d3-2", "0 0 420 240", "Đĩa ổ cứng tâm O với một điểm đánh dấu gần mép, lúc bắt đầu tính thời gian", b,
               "Dữ kiện: đĩa quay đều 7200 vòng/phút; điểm đánh dấu ở đỉnh lúc t = 0. Hình không vẽ vị trí sau 1,0 ms.")


# ───────────── Dạng 4: đĩa than d = 30 cm, 45 vòng/phút, điểm M ở mép, N cách tâm 5,0 cm ─────────────
def d4(kk):
    cx, cy, R = 130.0, 118.0, 100.0
    rn = R * 5.0 / 15.0                                  # r_N = 5,0 cm trên đĩa bán kính 15 cm
    w = TAU * 45 / 60.0
    b = circ(cx, cy, R, "currentColor", 2.4) + circ(cx, cy, rn, GREY, 1.3, "4 4", "none", .9) + circ(cx, cy, 5, "currentColor", 1.6)
    b += lbl(cx - 10, cy - 8, "O", "currentColor", 13, "end", "700")
    b += dot(262, 74, 5, ORG) + lbl(274, 79, "M: mép đĩa", "currentColor", 13, "start", "600")
    b += dot(262, 100, 5, BLUE) + lbl(274, 105, "N: cách tâm", "currentColor", 13, "start", "600") + lbl(274, 123, "5,0 cm", "currentColor", 13, "start", "600")
    b += lbl(256, 160, "Đĩa than 45 vòng/phút", RED, 13, "start", "700")
    b += lbl(256, 184, "ω = ?", "currentColor", 13, "start", "700")
    b += ts(256, 206, "v", "M", " = ?") + ts(256, 228, "v", "N", " = ?")
    b += dim("", "b", cx - R, 238, cx + R, 238, "d = 30 cm", cx, 256, "middle")
    if kk == 0:
        pm = sam(w, 4.0, 0.05, cx, cy, R, ph=rad(35))
        pn = sam(w, 4.0, 0.05, cx, cy, rn, ph=rad(35))
        b += rod((cx, cy), pm, 0.05, "currentColor", 1.8, .6) + mover(pn, 0.05, BLUE, 5.5) + mover(pm, 0.05, ORG, 6)
        return fig("d4-0", "0 0 420 266", "Đĩa than đường kính 30 cm quay đều; điểm M ở mép và điểm N cách tâm 5,0 cm cùng nằm trên một bán kính và cùng quay", b,
                   "Mô phỏng: chạy đúng thời gian thật, 4 s (3 vòng). M và N nằm trên cùng một bán kính, xuất phát ở góc 35° so với phương ngang.")
    pm = on_circle(cx, cy, R, rad(35)); pn = on_circle(cx, cy, rn, rad(0))
    b += seg(cx, cy, pm[0], pm[1], "currentColor", 1.8, "", .9) + dot(pm[0], pm[1], 6, ORG)
    b += seg(cx, cy, pn[0], pn[1], BLUE, 2.2) + dot(pn[0], pn[1], 5.5, BLUE) + lbl(pn[0] + 5, pn[1] - 8, "N", BLUE, 13, "start", "700")
    b += lbl(pm[0] + 8, pm[1] - 4, "M", ORG, 13, "start", "700")
    b += lbl((cx + pn[0]) / 2, cy + 24, "5,0 cm", BLUE, 12, "middle", "700")
    return fig("d4-2", "0 0 420 266", "Đĩa than đường kính 30 cm; điểm M ở mép, điểm N cách tâm O 5,0 cm", b,
               "Dữ kiện: đường kính 30 cm; N cách tâm 5,0 cm; M ở mép. Hai điểm nằm trên hai bán kính khác nhau chỉ để dễ nhìn.")


# ───────────── Dạng 5: cánh quạt dài 0,40 m, 480 vòng/phút; cánh mới dài 0,60 m ─────────────
def d5(kk):
    cx, cy = 135.0, 130.0
    sc = 200.0                                           # px/m
    R1, R2 = 0.40 * sc, 0.60 * sc
    w = TAU * 480 / 60.0 / 40.0                          # chạy chậm 40 lần
    b = ""
    if kk == 0:
        b += circ(cx, cy, R1, GRN, 1.6, "5 4", "none", .9)
        starts = [rad(90), rad(90) + TAU / 3, rad(90) + 2 * TAU / 3]
        for s0 in starts:
            pts = sam(w, 8.0, 0.1, cx, cy, R1, ph=s0)
            b += rod((cx, cy), pts, 0.1, "currentColor", 4.0, 1)
        b += mover(sam(w, 8.0, 0.1, cx, cy, R1, ph=starts[0]), 0.1, ORG, 6)
        b += circ(cx, cy, 8, "currentColor", 2) + dot(cx, cy, 2.5)
    else:
        b += circ(cx, cy, R1, GREY, 1.4, "5 4", "none", .9)
        b += seg(cx, cy, cx + R1, cy, "currentColor", 4.0)
        b += circ(cx, cy, 8, "currentColor", 2) + dot(cx, cy, 2.5)
        b += dot(cx + R1, cy, 5.5, ORG)
        b += lbl(cx + R1 / 2, cy - 10, "0,40 m", "currentColor", 12, "middle", "700")
    if kk != 0:
        b += lbl(cx - 6, cy + 24, "O", "currentColor", 13, "end", "700")
    b += lbl(272, 62, "Cánh quạt dài 0,40 m", "currentColor", 13, "start", "600") + lbl(272, 82, "480 vòng/phút", RED, 13, "start", "700")
    b += lbl(272, 118, "Đầu cánh: v = ?", "currentColor", 13, "start", "700")
    b += lbl(272, 156, "Cánh mới, quay chậm", "currentColor", 13, "start", "600") + lbl(272, 176, "320 vòng/phút, giữ v:", "currentColor", 13, "start", "600") + lbl(272, 196, "r = ?", "currentColor", 13, "start", "700")
    if kk == 0:
        return fig("d5-0", "0 0 420 262", "Cánh quạt ba cánh dài 0,40 m quay đều quanh trục O; một đầu cánh được đánh dấu", b,
                   "Mô phỏng: quạt thật quay quá nhanh để nhìn, nên hình chạy chậm 40 lần (8 s ứng với 0,2 s). Đầu cánh được đánh dấu xuất phát ở đỉnh.")
    return fig("d5-2", "0 0 420 262", "Cánh quạt dài 0,40 m quay quanh trục O", b,
               "Dữ kiện: cánh cũ dài 0,40 m (vẽ đúng tỉ lệ độ dài); chưa vẽ cánh mới và vận tốc.")


BUILD = [d1, d2, d3, d4, d5]
