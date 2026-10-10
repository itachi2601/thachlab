"""Hình cho bài tập mẫu Bài 32 "Lực hướng tâm và gia tốc hướng tâm" (Vật lí 10, chương 6), lesson_id 77.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mọi chuyển động tròn tính thật: vị trí theo góc θ = ω·t (SMIL lấy mẫu cách đều thời gian rồi nội suy; vật quay thì dùng animateTransform rotate
một vòng tuyến tính). KHÔNG vẽ vectơ gia tốc, lực hướng tâm hay lực căng; đại lượng cần tìm chỉ ghi "?" hoặc không ghi."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

GREY = "#94a3b8"


def rad(a):
    return math.radians(a)


def an(attr, vals, dur, nd=1):
    return (f'<animate attributeName="{attr}" values="{";".join(f"{v:.{nd}f}" for v in vals)}" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')


def circle_outline(cx, cy, R, c=GREY, w=1.4, dash="5 4"):
    return f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{c}" stroke-width="{w}" stroke-dasharray="{dash}"/>'


def ring(x, y, r=6):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="currentColor" stroke-width="2"/>'


def spin(inner, cx, cy, dur):
    """Nhóm quay đều một vòng quanh (cx, cy) (chiều kim đồng hồ trên màn hình), chạy MỘT lần khi bấm."""
    return (f'<g>{inner}<animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};360 {cx} {cy}" '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></g>')


def ts(x, y, base, sb, tail="", c="currentColor", size=13, anchor="start", weight="700"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{base}<tspan dy="4" font-size="{size - 3}">{sb}</tspan><tspan dy="-4">{tail}</tspan></text>')


# ───────────── Dạng 1: bi buộc dây, v = 2,0 m/s, r = 0,50 m ─────────────
def d1(kk):
    O = (125, 118); R = 80.0; v = 2.0; r_m = 0.50
    A = (O[0] + R, O[1]); B = (O[0] - R, O[1])
    b = circle_outline(O[0], O[1], R) + ring(*O, 5) + lbl(O[0] - 10, O[1] + 22, "O", "currentColor", 13, "end", "700")
    b += dot(*B, 3.5, "currentColor") + lbl(B[0] - 8, B[1] - 8, "B", "currentColor", 13, "end", "700")
    b += lbl(A[0] + 10, A[1] - 12, "A", "currentColor", 13, "start", "700")
    b += lbl(255, 96, "v = 2,0 m/s", BLUE, 13, "start", "700") + lbl(255, 120, "r = 0,50 m", "currentColor", 13, "start", "700")
    if kk == 0:
        T = 2 * math.pi * r_m / v                    # chu kì thật (s)
        slow = 2.0; n = 48; dur = T * slow
        pts = [(O[0] + R * math.cos(2 * math.pi * i / n), O[1] - R * math.sin(2 * math.pi * i / n)) for i in range(n + 1)]
        b += (f'<line x1="{O[0]}" y1="{O[1]}" x2="{pts[0][0]:.1f}" y2="{pts[0][1]:.1f}" stroke="currentColor" stroke-width="1.6">'
              f'{an("x2", [p[0] for p in pts], dur)}{an("y2", [p[1] for p in pts], dur)}</line>')
        b += (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="7" fill="{GRN}" stroke="currentColor" stroke-width="1.6">'
              f'{an("cx", [p[0] for p in pts], dur)}{an("cy", [p[1] for p in pts], dur)}</circle>')
        return fig("d1-0", "0 0 420 236", "Nhìn từ trên xuống: hòn bi buộc dây chuyển động tròn đều quanh O trên mặt bàn nhẵn, đi từ A đúng một vòng", b,
                   "Mô phỏng nhìn từ trên xuống: bi đi đúng một vòng từ A, tốc độ không đổi (chạy chậm 2 lần, khoảng 3 s). Không vẽ vectơ nào.")
    b += seg(O[0], O[1], A[0], A[1], "currentColor", 1.8) + f'<circle cx="{A[0]}" cy="{A[1]}" r="7" fill="{GRN}" stroke="currentColor" stroke-width="1.6"/>'
    b += lbl(A[0] + 14, A[1] + 22, "a = ?", RED, 13, "start", "700")
    return fig("d1-2", "0 0 420 236", "Hòn bi ở vị trí A trên quỹ đạo tròn tâm O, dây OA", b,
               "Dữ kiện: quỹ đạo tròn tâm O, bán kính 0,50 m; bi đang ở A. Chưa vẽ vectơ vận tốc hay gia tốc.")


# ───────────── Dạng 2: đu quay r = 15 m, T = 40 s ─────────────
def wheel_body(C, R, cabin_at_start=True):
    spokes = "".join(seg(C[0], C[1], C[0] + R * math.cos(rad(a)), C[1] - R * math.sin(rad(a)), GREY, 1.2) for a in range(0, 360, 45))
    rim = f'<circle cx="{C[0]}" cy="{C[1]}" r="{R}" fill="none" stroke="currentColor" stroke-width="2"/>'
    cabs = "".join(f'<circle cx="{C[0] + R * math.cos(rad(a)):.1f}" cy="{C[1] - R * math.sin(rad(a)):.1f}" r="4" fill="currentColor"/>' for a in range(45, 360, 45))
    guest = f'<circle cx="{C[0] + R}" cy="{C[1]}" r="7" fill="{GRN}" stroke="currentColor" stroke-width="1.6"/>'
    return spokes + rim + cabs + guest


def d2(kk):
    C = (130, 118); R = 85.0
    b = lbl(255, 92, "T = 40 s", "currentColor", 13, "start", "700") + lbl(255, 116, "r = 15 m", "currentColor", 13, "start", "700")
    b += lbl(255, 140, "khách ở mép vòng", GRN, 13, "start", "700")
    if kk == 0:
        T = 40.0; speed = 8.0
        b = spin(wheel_body(C, R), C[0], C[1], T / speed) + dot(C[0], C[1], 4.5, "currentColor") + b
        return fig("d2-0", "0 0 420 236", "Vòng quay công viên bán kính 15 m quay đều, mỗi vòng 40 giây; khách ngồi cabin ở mép vòng", b,
                   "Mô phỏng: vòng quay đúng một vòng (chạy nhanh 8 lần, khoảng 5 s). Cabin xanh là chỗ khách ngồi.")
    b = wheel_body(C, R) + dot(C[0], C[1], 4.5, "currentColor") + b
    b += seg(C[0], C[1], C[0] + R, C[1], BLUE, 2.4) + lbl(C[0] + R / 2, C[1] - 8, "r", BLUE, 13, "middle", "700")
    return fig("d2-2", "0 0 420 236", "Vòng quay bán kính r = 15 m; khách ngồi ở mép vòng, cách tâm đúng r", b,
               "Dữ kiện: khách ngồi ở mép vòng, cách trục quay đúng bán kính r. Chưa vẽ vectơ.")


# ───────────── Dạng 3: quạt trần ω = 20 rad/s, A cách 10 cm, B cách 30 cm ─────────────
def fan_body(C, k_px):
    """k_px = px/m. Ba cánh ở 0°, 120°, 240°; A (0,10 m) và B (0,30 m) trên cánh 0°."""
    out = ""
    for a in (0, 120, 240):
        ex, ey = C[0] + 0.40 * k_px * math.cos(rad(a)), C[1] - 0.40 * k_px * math.sin(rad(a))
        out += seg(C[0], C[1], ex, ey, "currentColor", 6, "", .55)
    out += f'<circle cx="{C[0] + 0.10 * k_px:.1f}" cy="{C[1]}" r="5.5" fill="{ORG}" stroke="currentColor" stroke-width="1.4"/>'
    out += f'<circle cx="{C[0] + 0.30 * k_px:.1f}" cy="{C[1]}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.4"/>'
    return out


def d3(kk):
    C = (120, 112); kp = 270.0                       # 0,40 m ứng với 108 px
    label = (lbl(C[0] + 0.10 * kp, C[1] - 12, "A", ORG, 13, "middle", "700") + lbl(C[0] + 0.30 * kp, C[1] - 12, "B", GRN, 13, "middle", "700")
             + dim("", "o", C[0], C[1] + 30, C[0] + 0.10 * kp, C[1] + 30, "", 0, 0) + lbl(C[0] + 0.10 * kp + 8, C[1] + 34, "10 cm", ORG, 12, "start", "700")
             + dim("", "g", C[0], C[1] + 54, C[0] + 0.30 * kp, C[1] + 54, "", 0, 0) + lbl(C[0] + 0.30 * kp + 8, C[1] + 58, "30 cm", GRN, 12, "start", "700"))
    legend = lbl(255, 30, "ω = 20 rad/s", BLUE, 13, "start", "700")
    if kk == 0:
        w = 20.0; T = 2 * math.pi / w; slow = 10.0
        b = spin(fan_body(C, kp), C[0], C[1], T * slow) + dot(C[0], C[1], 4.5, "currentColor") + label + legend
        return fig("d3-0", "0 0 420 236", "Quạt trần nhìn từ dưới lên quay đều quanh trục; điểm A cách trục 10 cm, điểm B cách trục 30 cm trên cùng một cánh", b,
                   "Mô phỏng: quạt quay đúng một vòng (chạy chậm 10 lần, khoảng 3 s). A, B ghi ở vị trí lúc đầu.")
    b = fan_body(C, kp) + dot(C[0], C[1], 4.5, "currentColor") + label + legend
    return fig("d3-2", "0 0 420 236", "Cánh quạt trần với hai điểm A (cách trục 10 cm) và B (cách trục 30 cm) trên cùng một cánh", b,
               "Dữ kiện: A và B nằm trên cùng một cánh quạt, cách trục lần lượt 10 cm và 30 cm.")


# ───────────── Dạng 4: vật 50 g trên đĩa, r = 20 cm, 60 vòng/phút ─────────────
def disc_body(C, kp):
    Rd = 0.33 * kp
    out = f'<circle cx="{C[0]}" cy="{C[1]}" r="{Rd:.1f}" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    out += seg(C[0], C[1], C[0] - Rd, C[1], GREY, 1.2, "4 4", .9)
    out += f'<rect x="{C[0] + 0.20 * kp - 7:.1f}" y="{C[1] - 7}" width="14" height="14" fill="{ORG}" stroke="currentColor" stroke-width="1.6"/>'
    return out


def d4(kk):
    C = (125, 118); kp = 300.0
    legend = lbl(255, 86, "m = 50 g", "currentColor", 13, "start", "700") + lbl(255, 110, "r = 20 cm", "currentColor", 13, "start", "700") + lbl(255, 134, "60 vòng/phút", BLUE, 13, "start", "700")
    ruler = dim("", "g", C[0], C[1] + 0.33 * kp + 16, C[0] + 0.20 * kp, C[1] + 0.33 * kp + 16, "", 0, 0)
    ruler = ""
    if kk == 0:
        T = 1.0; slow = 4.0
        b = spin(disc_body(C, kp), C[0], C[1], T * slow) + dot(C[0], C[1], 4.5, "currentColor") + legend
        b += lbl(C[0] + 0.20 * kp + 12, C[1] - 12, "vật", ORG, 13, "start", "700")
        return fig("d4-0", "0 0 420 236", "Nhìn từ trên xuống: đĩa nằm ngang quay đều 60 vòng/phút, vật nhỏ 50 g nằm yên trên đĩa cách trục 20 cm", b,
                   "Mô phỏng nhìn từ trên xuống: đĩa quay đúng một vòng (chạy chậm 4 lần, khoảng 4 s); vật nằm yên so với đĩa. Vạch xám trên đĩa chỉ để thấy đĩa quay.")
    b = disc_body(C, kp) + dot(C[0], C[1], 4.5, "currentColor") + legend
    b += seg(C[0], C[1], C[0] + 0.20 * kp, C[1], BLUE, 2) + lbl(C[0] + 0.10 * kp, C[1] - 9, "r", BLUE, 13, "middle", "700")
    b += lbl(C[0] + 0.20 * kp + 12, C[1] - 12, "vật", ORG, 13, "start", "700")
    return fig("d4-2", "0 0 420 236", "Vật nhỏ trên đĩa nằm ngang cách trục quay r = 20 cm", b,
               "Dữ kiện: vật cách trục quay r = 20 cm và nằm yên so với đĩa. Chưa vẽ lực nào.")


# ───────────── Dạng 5: mô tô 200 kg, 54 km/h vào đường vòng r = 50 m ─────────────
def d5(kk):
    C = (190.0, 218.0); R = 140.0; v = 15.0
    a0, a1 = 150.0, 60.0
    pt = lambda a, rr=R: (C[0] + rr * math.cos(rad(a)), C[1] - rr * math.sin(rad(a)))
    def arc_path(rr, dash=""):
        x0, y0 = pt(a0, rr); x1, y1 = pt(a1, rr)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<path d="M{x0:.1f},{y0:.1f} A{rr:.1f},{rr:.1f} 0 0 1 {x1:.1f},{y1:.1f}" fill="none" stroke="{"currentColor" if not dash else GREY}" stroke-width="{2.2 if not dash else 1.4}"{d}/>'
    b = arc_path(R + 14) + arc_path(R - 14) + arc_path(R, "6 5")
    top = pt(90.0)
    b += seg(C[0], C[1], top[0], top[1] + 14, GREY, 1.2, "4 4", .9) + dot(C[0], C[1], 4, "currentColor") + lbl(C[0] - 10, C[1] + 16, "O", "currentColor", 13, "end", "700")
    b += lbl(C[0] + 8, 150, "r = 50 m (ý a)", "currentColor", 13, "start", "700")
    b += lbl(285, 150, "v = 54 km/h", BLUE, 13, "start", "700") + lbl(285, 174, "m = 200 kg", "currentColor", 13, "start", "700")
    if kk == 0:
        arc_len = rad(a0 - a1) * 50.0                   # m, r thật = 50 m
        dur = arc_len / v                              # đúng thời gian thật (≈ 5,2 s)
        n = 45
        pts = [pt(a0 + (a1 - a0) * i / n) for i in range(n + 1)]
        b += (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="7" fill="{ORG}" stroke="currentColor" stroke-width="1.6">'
              f'{an("cx", [p[0] for p in pts], dur)}{an("cy", [p[1] for p in pts], dur)}</circle>')
        return fig("d5-0", "0 0 420 240", "Nhìn từ trên xuống: mô tô chạy đều 54 km/h qua đoạn đường vòng nằm ngang bán kính 50 m", b,
                   "Mô phỏng nhìn từ trên xuống: mô tô đi hết một phần tư đường vòng, tốc độ không đổi, đúng thời gian thật (khoảng 5 s). Không vẽ lực nào.")
    mid = pt(105.0)
    b += f'<circle cx="{mid[0]:.1f}" cy="{mid[1]:.1f}" r="7" fill="{ORG}" stroke="currentColor" stroke-width="1.6"/>'
    return fig("d5-2", "0 0 420 240", "Đoạn đường vòng nằm ngang tâm O, bán kính 50 m; mô tô chạy trên đường", b,
               "Dữ kiện: đường vòng nằm ngang, tâm O; ý a xét bán kính 50 m, ý b hỏi bán kính nhỏ nhất. Chưa vẽ lực nào.")


BUILD = [d1, d2, d3, d4, d5]
