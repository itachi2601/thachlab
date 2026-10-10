"""Hình cho bài tập mẫu Bài 14 "Máy phát điện xoay chiều. Máy biến áp" (Vật lí 12), lesson_id 125.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Đường cong, điểm chạy, độ sáng điện trở, góc quay rô-to/khung đều TÍNH từ công thức (lấy mẫu cách đều thời gian, nội suy tuyến tính).
Nhãn chỉ ghi dữ kiện đề cho và dấu "?" cho đại lượng cần tìm; không nhãn kết quả."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, không vẽ theo tỉ lệ số liệu."
TAU = 2 * math.pi


def tx(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, s, c, size, anchor, weight)


def smilf(attr, vals, dur, nd=1):
    return f'<animate attributeName="{attr}" values="{";".join(f"{v:.{nd}f}" for v in vals)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


def curve(f, ncyc, ox, oy, wpx, apx, per=40):
    """Điểm (X, Y) của đồ thị; f(x) nhận x = số chu kì kể từ t = 0, trả giá trị chuẩn hoá trong [-1, 1]."""
    n = int(round(per * ncyc))
    return [(ox + wpx * k / n, oy - apx * f(ncyc * k / n)) for k in range(n + 1)]


def axes_tv(ox, oy, wpx, apx, vlab, up=16):
    b = arrow("", "g", ox - 8, oy, ox + wpx + 14, oy, 2) + arrow("", "g", ox, oy + apx + 12, ox, oy - apx - up, 2)
    b += tx(ox + wpx + 12, oy + 17, "t", GRN, 13, "end") + tx(ox + 8, oy - apx - up + 8, vlab, GRN, 13)
    return b


def runner(pts, dur):
    return (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">'
            f'{smilf("cx", [p[0] for p in pts], dur)}{smilf("cy", [p[1] for p in pts], dur)}</circle>')


def rot(cx, cy, dphi, dur, inner):
    """Nhóm quay quanh (cx,cy) góc dphi độ (âm = ngược chiều kim đồng hồ), đều theo thời gian; chạy một lần khi bấm."""
    return (f'<g><animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};{dphi:.1f} {cx} {cy}" '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>{inner}</g>')


def zigzag(x0, x1, y, amp=8, teeth=6, c="currentColor", w=2.4):
    """Điện trở: dây thẳng – răng cưa – dây thẳng. Trả (svg, (xa, xb)) là đoạn răng cưa."""
    xa, xb = x0 + (x1 - x0) * 0.2, x1 - (x1 - x0) * 0.2
    pts = [(x0, y), (xa, y)]
    for k in range(teeth):
        pts.append((xa + (xb - xa) * (k + 0.5) / teeth, y + (amp if k % 2 == 0 else -amp)))
    pts += [(xb, y), (x1, y)]
    return poly(pts, c, w), (xa, xb)


def coil_v(x, y0, n, step=9, rx=11, ry=4.5, c="currentColor"):
    """Cuộn dây quấn quanh trụ đứng: n vòng elip xếp dọc, tâm x, bắt đầu từ y0."""
    return "".join(f'<ellipse cx="{x}" cy="{y0 + k * step}" rx="{rx}" ry="{ry}" fill="none" stroke="{c}" stroke-width="2"/>' for k in range(n))


def gen_circle(cx, cy, r=21):
    wave = [(cx - 11 + 22 * k / 20, cy - 6 * math.sin(TAU * k / 20)) for k in range(21)]
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="currentColor" stroke-width="2.4"/>' + poly(wave, "currentColor", 1.8)


def glow(cx0, cx1, y, amp, vals_fn, per, ncyc, dur):
    """Vùng sáng cam sau điện trở, độ trong suốt theo i² (tính thật)."""
    vals = [0.62 * vals_fn(ncyc * k / (per * ncyc)) ** 2 for k in range(per * ncyc + 1)]
    return (f'<rect x="{cx0:.1f}" y="{y - amp - 6}" width="{cx1 - cx0:.1f}" height="{2 * amp + 12}" rx="7" fill="{ORG}" opacity="{vals[0]:.2f}">'
            f'{smilf("opacity", vals, dur, 2)}</rect>')


def swing(x0, y, a, f, per, ncyc, dur, r=4.2):
    """Hạt tải dao động quanh x0 với biên độ a (dòng xoay chiều đổi chiều)."""
    vals = [x0 + a * f(ncyc * k / (per * ncyc)) for k in range(per * ncyc + 1)]
    return (f'<circle cx="{vals[0]:.1f}" cy="{y}" r="{r}" fill="{GRN}" stroke="currentColor" stroke-width="1.2">{smilf("cx", vals, dur)}</circle>')


# ───────────── Dạng 1 · rô-to 4 cặp cực, 750 vòng/phút ─────────────
def d1(kk):
    cx, cy, R = 84, 100, 56
    secs = ""
    for i in range(8):
        a0, a1 = math.radians(i * 45 - 22.5), math.radians(i * 45 + 22.5)
        col = RED if i % 2 == 0 else BLUE
        secs += (f'<path d="M{cx},{cy} L{cx + R * math.cos(a0):.1f},{cy - R * math.sin(a0):.1f} A{R},{R} 0 0 0 '
                 f'{cx + R * math.cos(a1):.1f},{cy - R * math.sin(a1):.1f} Z" fill="{col}" fill-opacity="0.28" stroke="currentColor" stroke-width="1.6"/>')
    rotor = secs + dot(cx, cy, 3.5, "currentColor")
    coil = coil_v(cx + R + 18, cy - 18, 5, 9, 11, 4.5)
    ox, oy, wpx, apx, ncyc = 234, 100, 160, 38, 4
    f = lambda x: math.sin(TAU * x)
    b = axes_tv(ox, oy, wpx, apx, "e") + poly(curve(f, ncyc, ox, oy, wpx, apx), BLUE, 2.4)
    b += coil + tx(cx + R + 18, cy + 40, "cuộn dây", "currentColor", 11, "middle", "400")
    b += tx(14, 20, "4 cặp cực ; n = 750 vòng/phút", "currentColor", 13)
    if kk == 0:
        b += rot(cx, cy, -360, 4.0, rotor) + runner(curve(f, ncyc, ox, oy, wpx, apx, 32), 4.0)
        b += tx(14, 186, "f = ?", ORG, 13)
        return fig("d1-0", "0 0 420 196", "Rô-to nam châm nhiều cặp cực quay trước một cuộn dây đứng yên, đồ thị suất điện động e theo thời gian có điểm chạy", b,
                   "Mô phỏng: rô-to (đỏ: cực N, xanh: cực S) quay đều ngược chiều kim đồng hồ trước cuộn dây đứng yên; điểm xanh chạy trên đồ thị e(t) tính theo số cặp cực; chạy chậm, một vòng quay ứng với 4 s. " + NOTE)
    b += rotor + tx(14, 186, "f = ? ; ω = ? ; p' = ? (câu c)", ORG, 13)
    return fig("d1-2", "0 0 420 196", "Dữ kiện: rô-to nhiều cặp cực quay đều trước cuộn dây, tốc độ cho bằng vòng trên phút", b,
               "Dữ kiện: rô-to 4 cặp cực (đỏ: cực N, xanh: cực S), tốc độ quay cho bằng vòng/phút. " + NOTE)


# ───────────── Dạng 2 · khung N = 400 vòng, S = 50 cm², B = 0,030 T, 1200 vòng/phút ─────────────
def d2(kk):
    cx, cy = 80, 106
    ox, oy, wpx, apx, ncyc = 230, 106, 150, 44, 2
    f = lambda x: math.sin(TAU * x)
    b = axes_tv(ox, oy, wpx, apx, "e") + poly(curve(f, ncyc, ox, oy, wpx, apx), BLUE, 2.4)
    for y in (58, 84, 128, 154):
        b += field_line(12, y, 150, y, BLUE, 1.8, "6 4", 11)
    b += tx(154, 62, "B", BLUE, 13)
    frame = (seg(cx, cy - 32, cx, cy + 32, "currentColor", 4.5) + dot(cx, cy - 32, 4, "currentColor") + dot(cx, cy + 32, 4, "currentColor")
             + arrow("", "r", cx, cy, cx + 30, cy, 2.4))
    b += tx(12, 20, "N = 400 vòng ; S = 50 cm²", "currentColor", 13) + tx(12, 38, "B = 0,030 T ; n = 1200 vòng/phút", "currentColor", 13)
    b += tx(cx, 186, "nhìn dọc trục quay", "currentColor", 11, "middle", "400")
    if kk == 0:
        b += rot(cx, cy, -720, 4.0, frame) + dot(cx, cy, 3.5, "currentColor") + runner(curve(f, ncyc, ox, oy, wpx, apx, 32), 4.0)
        return fig("d2-0", "0 0 420 198", "Khung dây quay đều trong từ trường đều, đồ thị suất điện động e theo thời gian có điểm chạy", b,
                   "Mô phỏng: khung (nhìn dọc trục quay, mũi tên đỏ là pháp tuyến) quay đều ngược chiều kim đồng hồ, điểm xanh chạy trên đồ thị e(t); chọn gốc thời gian lúc pháp tuyến cùng hướng B; chạy chậm, hai vòng quay ứng với 4 s. " + NOTE)
    ytop = oy - apx
    b += seg(ox, ytop, ox + wpx, ytop, ORG, 1.6, "6 4") + tx(ox + wpx, ytop - 6, "E₀ = ?", ORG, 12, "end")
    b += frame + dot(cx, cy, 3.5, "currentColor") + tx(cx + 34, cy - 8, "n", RED, 13)
    b += tx(12, 214, "ω, E₀, E = ? ; E₀ khi n mới = ?", ORG, 13)
    return fig("d2-2", "0 0 420 222", "Dữ kiện: khung dây quay quanh trục vuông góc với từ trường đều, đường nét đứt cam là biên độ suất điện động cần tìm", b,
               "Dữ kiện: trục quay vuông góc với B; mũi tên đỏ là pháp tuyến của khung. " + NOTE)


# ───────────── Dạng 3 · máy biến áp N1 = 1100, N2 = 60, U1 = 220 V, I2 = 2,5 A ─────────────
def d3(kk):
    b = (f'<rect x="130" y="30" width="160" height="118" fill="none" stroke="currentColor" stroke-width="2.6"/>'
         f'<rect x="162" y="58" width="96" height="62" fill="none" stroke="currentColor" stroke-width="2.2"/>')
    # đường sức: nét đứt, chạy theo đường tâm của lõi; chiều đổi liên tục nên không vẽ đầu mũi tên
    per, ncyc = 32, 2
    vals = [0.15 + 0.85 * abs(math.sin(TAU * ncyc * k / (per * ncyc))) for k in range(per * ncyc + 1)]
    op = vals[0] if kk == 0 else 0.7
    anim = smilf("stroke-opacity", vals, 4.0, 2) if kk == 0 else ""
    b += (f'<rect x="146" y="44" width="128" height="90" fill="none" stroke="{BLUE}" stroke-width="2" stroke-dasharray="6 4" stroke-opacity="{op:.2f}">{anim}</rect>')
    b += coil_v(146, 66, 6, 9, 14, 4.5) + coil_v(274, 80, 3, 9, 14, 4.5)
    b += seg(132, 66, 60, 66, "currentColor", 2.2) + seg(132, 111, 60, 111, "currentColor", 2.2)
    b += seg(288, 80, 360, 80, "currentColor", 2.2) + seg(288, 107, 360, 107, "currentColor", 2.2)
    b += gen_circle(60, 88) + seg(60, 67, 60, 66, "currentColor", 2.2) + seg(60, 109, 60, 111, "currentColor", 2.2)
    # tải ở bên thứ cấp: điện trở đặt đứng
    tai = poly([(360, 80), (360, 86)] + [(360 + (9 if k % 2 == 0 else -9), 88 + k * 3.2) for k in range(6)] + [(360, 107)], "currentColor", 2.4)
    b += tai
    b += tx(14, 26, "U₁ = 220 V", "currentColor", 13) + tx(14, 166, "N₁ = 1100 vòng", "currentColor", 13)
    b += tx(406, 26, "U₂ = ?", ORG, 13, "end") + tx(406, 166, "N₂ = 60 vòng", "currentColor", 13, "end") + tx(406, 126, "I₂ = 2,5 A", "currentColor", 13, "end")
    b += tx(210, 24, "lõi kín", "currentColor", 11, "middle", "400")
    if kk == 0:
        ox, oy, wpx, apx = 156, 196, 108, 11
        f = lambda x: math.sin(TAU * x)
        b += poly(curve(f, ncyc, ox, oy, wpx, apx), BLUE, 2.2) + tx(ox - 8, oy + 5, "u₁", BLUE, 12, "end") + runner(curve(f, ncyc, ox, oy, wpx, apx, 32), 4.0)
        return fig("d3-0", "0 0 420 214", "Máy biến áp lí tưởng nối nguồn xoay chiều; đường sức từ trong lõi mạnh yếu theo điện áp u1 và điểm chạy trên đồ thị u1", b,
                   "Mô phỏng: điểm xanh chạy trên đồ thị điện áp nguồn u₁(t); đường sức từ trong lõi (nét đứt) đậm nhạt theo |u₁|, chiều đổi liên tục nên không vẽ đầu mũi tên; chạy chậm. " + NOTE)
    return fig("d3-2", "0 0 420 182", "Dữ kiện: máy biến áp lí tưởng với số vòng hai cuộn, điện áp sơ cấp, cường độ thứ cấp; điện áp thứ cấp cần tìm", b,
               "Dữ kiện: hai cuộn dây trên cùng một lõi kín (số vòng ghi trên hình, không vẽ đủ số vòng). " + NOTE)


# ───────────── Dạng 4 · truyền tải P = 1,2 MW, U = 20 kV, R = 5 Ω ─────────────
def _line_scene(kk, with_mba, top_y, y_bot, x_r0, x_r1, x_load, per, ncyc, dur, dots):
    """Dây truyền tải: điện trở răng cưa trên dây trên; mô phỏng: điện trở sáng theo i², hạt tải dao động."""
    f = lambda x: math.sin(TAU * x)
    zz, (xa, xb) = zigzag(x_r0, x_r1, top_y, 8, 6)
    b = ""
    if kk == 0:
        b += glow(xa - 3, xb + 3, top_y, 8, f, per, ncyc, dur)
        for x0, a in dots:
            b += swing(x0, top_y, a, f, per, ncyc, dur)
    b += zz
    return b, (xa, xb)


def d4(kk):
    per, ncyc, dur = 32, 2, 4.0
    top, bot = 88, 144
    b = gen_circle(46, 116) + tx(46, 30, "P = 1,2 MW", "currentColor", 13, "middle") + tx(46, 48, "U = 20 kV", "currentColor", 13, "middle")
    b += seg(46, 95, 46, 88, "currentColor", 2.4) + seg(46, 88, 82, 88, "currentColor", 2.4)
    b += seg(46, 137, 46, bot, "currentColor", 2.4) + seg(46, bot, 366, bot, "currentColor", 2.4)
    sc, (xa, xb) = _line_scene(kk, False, top, bot, 150, 240, 330, per, ncyc, dur, [(112, 14), (288, 14)])
    b += seg(82, 88, 150, 88, "currentColor", 2.4) + sc + seg(240, 88, 330, 88, "currentColor", 2.4)
    b += f'<rect x="330" y="68" width="72" height="62" rx="6" fill="none" stroke="currentColor" stroke-width="2.4"/>' + tx(366, 104, "tải", "currentColor", 13, "middle")
    b += seg(366, 130, 366, bot, "currentColor", 2.4)
    b += tx(195, 66, "R = 5 Ω", "currentColor", 13, "middle") + tx(195, 116, "ΔP = ?", ORG, 13, "middle") + tx(112, 76, "I = ?", ORG, 12, "middle")
    b += tx(366, 160, "nơi tiêu thụ", "currentColor", 11, "middle", "400") + tx(46, 176, "nơi phát", "currentColor", 11, "middle", "400")
    if kk == 0:
        return fig("d4-0", "0 0 420 184", "Nhà máy truyền điện qua đường dây có điện trở R tới nơi tiêu thụ; điện trở sáng lên theo cường độ dòng điện", b,
                   "Mô phỏng: dòng xoay chiều đổi chiều (hạt xanh dao động), điện trở của dây sáng cam theo i²; chạy chậm. " + NOTE)
    return fig("d4-2", "0 0 420 184", "Dữ kiện: công suất và điện áp nơi phát, điện trở đường dây; cường độ dòng và hao phí cần tìm", b,
               "Dữ kiện: điện trở R là điện trở tổng cộng của đường dây. " + NOTE)


# ───────────── Dạng 5 · máy phát 400 kW, 2 kV → MBA tăng áp N1 = 1000, N2 = 5000 → dây R = 10 Ω ─────────────
def d5(kk):
    per, ncyc, dur = 32, 2, 4.0
    f = lambda x: math.sin(TAU * x)
    b = gen_circle(34, 85, 20)
    b += (f'<rect x="76" y="45" width="68" height="80" fill="none" stroke="currentColor" stroke-width="2.4"/>'
          f'<rect x="96" y="62" width="28" height="46" fill="none" stroke="currentColor" stroke-width="2"/>')
    vals = [0.15 + 0.85 * abs(math.sin(TAU * ncyc * k / (per * ncyc))) for k in range(per * ncyc + 1)]
    op = vals[0] if kk == 0 else 0.7
    anim = smilf("stroke-opacity", vals, dur, 2) if kk == 0 else ""
    b += f'<rect x="86" y="53" width="48" height="64" fill="none" stroke="{BLUE}" stroke-width="1.8" stroke-dasharray="5 4" stroke-opacity="{op:.2f}">{anim}</rect>'
    b += coil_v(86, 68, 4, 10, 10, 4) + coil_v(134, 68, 4, 10, 10, 4)
    b += seg(76, 70, 34, 70, "currentColor", 2.2) + seg(76, 104, 34, 104, "currentColor", 2.2) + seg(34, 70, 34, 65, "currentColor", 2.2) + seg(34, 104, 34, 105, "currentColor", 2.2)
    top, bot = 70, 104
    sc, (xa, xb) = _line_scene(kk, True, top, bot, 190, 270, 350, per, ncyc, dur, [(168, 10), (310, 10)])
    b += seg(144, top, 190, top, "currentColor", 2.2) + sc + seg(270, top, 350, top, "currentColor", 2.2) + seg(144, bot, 350, bot, "currentColor", 2.2)
    b += f'<rect x="350" y="58" width="58" height="58" rx="6" fill="none" stroke="currentColor" stroke-width="2.4"/>' + tx(379, 92, "tải", "currentColor", 13, "middle")
    b += tx(8, 148, "P = 400 kW", "currentColor", 13) + tx(8, 166, "U₁ = 2 kV", "currentColor", 13)
    b += tx(110, 34, "N₁ = 1000 ; N₂ = 5000", "currentColor", 13, "middle")
    b += tx(146, 60, "U₂ = ?", ORG, 12, "start")
    b += tx(230, 54, "R = 10 Ω", "currentColor", 13, "middle") + tx(230, 134, "I, ΔP = ?", ORG, 13, "middle") + tx(230, 154, "U, N₂ tối thiểu = ? (câu c)", ORG, 13, "middle")
    b += tx(118, 139, "máy tăng áp", "currentColor", 11, "middle", "400") + tx(379, 134, "nơi tiêu thụ", "currentColor", 11, "middle", "400")
    if kk == 0:
        return fig("d5-0", "0 0 420 176", "Máy phát, máy biến áp tăng áp, đường dây có điện trở R và tải; đường sức trong lõi và điện trở của dây sáng theo dòng xoay chiều", b,
                   "Mô phỏng: dòng xoay chiều đổi chiều (hạt xanh dao động), đường sức trong lõi máy biến áp đậm nhạt, điện trở của dây sáng cam theo i²; chạy chậm. " + NOTE)
    return fig("d5-2", "0 0 420 176", "Dữ kiện: máy phát, máy biến áp tăng áp với số vòng hai cuộn, đường dây có điện trở R; các đại lượng cần tìm in màu cam", b,
               "Dữ kiện: điện áp ở đầu đường dây là điện áp thứ cấp của máy biến áp. " + NOTE)
