"""Hình cho bài tập mẫu Bài 25 "Động năng, thế năng" (Vật lí 10), lesson_id 70.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mô phỏng tính thật từ công thức (mẫu cách đều thời gian, nội suy tuyến tính). Không vẽ/ghi động năng, thế năng, công hay vận tốc là đáp án.
D1 xe tải chạy 2 s đều 36 km/h rồi tăng tốc đều lên 90 km/h trong 5 s (a = 3 m/s², đúng thời gian thật)
D2 hai thùng được nâng từ nền kho lên giá (độ cao vẽ 40 px/m)
D3 mốc thế năng (nét đứt đỏ) dời lần lượt qua các sàn, chậu cây đứng yên (10 px/m)
D4 xe đạp chạy dọc đường đồi A → B → C với tốc độ không đổi (độ cao 4 px/m, khoảng cách ngang không theo tỉ lệ)
D5 thùng được kéo lên dốc nghiêng 30° với a = (150 − 25 − 100)/20 = 1,25 m/s² trong 4 s (đúng thời gian thật)."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from svg_lib import vec_luc, chevron, field_line

GREY = "#94a3b8"


def rad(a):
    return math.radians(a)


def an(attr, vals, dur, nd=1):
    return (f'<animate attributeName="{attr}" values="{";".join(f"{v:.{nd}f}" for v in vals)}" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')


def tr(vals, dur):
    """animateTransform translate: vals = [(x, y), …]."""
    return (f'<animateTransform attributeName="transform" type="translate" values="{";".join(f"{x:.1f} {y:.1f}" for x, y in vals)}" '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')


def ts(x, y, base, sb, tail="", c="currentColor", size=13, anchor="start", weight="700"):
    """Nhãn có chỉ số dưới: base_sb tail."""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{base}<tspan dy="4" font-size="{size - 3}">{sb}</tspan><tspan dy="-4">{tail}</tspan></text>')


def road(y, x0=16, x1=404):
    return seg(x0, y, x1, y, "currentColor", 2.4)


def wheel(x, y, r=6):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="currentColor" stroke-width="2"/>'


def truck(x, y):
    """Xe tải, đáy bánh chạm đường tại y; thân ở trái, cabin ở phải (hướng sang phải)."""
    return (f'<rect x="{x}" y="{y - 44}" width="46" height="34" fill="none" stroke="currentColor" stroke-width="2.2"/>'
            f'<rect x="{x + 46}" y="{y - 34}" width="18" height="24" fill="none" stroke="currentColor" stroke-width="2.2"/>'
            + wheel(x + 12, y - 6) + wheel(x + 36, y - 6) + wheel(x + 56, y - 6))


def car(x, y):
    return (f'<rect x="{x}" y="{y - 26}" width="56" height="16" fill="none" stroke="currentColor" stroke-width="2.2"/>'
            f'<rect x="{x + 12}" y="{y - 38}" width="30" height="12" fill="none" stroke="currentColor" stroke-width="2.2"/>'
            + wheel(x + 12, y - 8, 5) + wheel(x + 44, y - 8, 5))


# ───────────── Dạng 1: xe tải 4,0 tấn, 36 km/h → 90 km/h ─────────────
def x_truck(t):
    return 10 * t if t <= 2 else 20 + 10 * (t - 2) + 1.5 * (t - 2) ** 2


def d1(kk):
    yr = 168
    if kk == 0:
        k = 2.4; step = 0.25; n = 28
        ts_ = [i * step for i in range(n + 1)] + [7.0] * 4
        pos = [(k * x_truck(min(t, 7.0)), 0.0) for t in ts_]
        assert abs(x_truck(7.0) - 107.5) < 1e-9 and abs(10 + 3 * 5 - 25) < 1e-9
        dur = step * (len(ts_) - 1)
        b = road(yr) + f'<g>{truck(24, yr)}{tr(pos, dur)}</g>'
        b += lbl(24, 112, "36 km/h", BLUE, 13, "start", "700")
        xe = 24 + k * 107.5 + 64
        b += seg(xe, 120, xe, yr, GREY, 1.2, "4 4", .8) + lbl(xe - 4, 112, "90 km/h", ORG, 13, "end", "700")
        b += lbl(24, 196, "xe tải 4,0 tấn", "currentColor", 12, "start", "600")
        return fig("d1-0", "0 0 420 206", "Xe tải 4,0 tấn chạy với tốc độ 36 km/h rồi tăng tốc đến 90 km/h",
                   b, "Mô phỏng: xe chạy 2 s với 36 km/h rồi tăng tốc đều trong 5 s đến 90 km/h (đúng thời gian thật). Chưa tính động năng.")
    y1, y2 = 84, 170
    b = road(y1, 16, 100) + truck(24, y1) + road(y2, 16, 100) + car(24, y2)
    b += lbl(112, y1 - 36, "xe tải", "currentColor", 13, "start", "700")
    b += ts(112, y1 - 16, "m = 4,0 tấn · v", "1", " = 36 km/h", BLUE, 13, "start") + ts(112, y1 + 6, "W", "d1", " = ?", ORG, 13, "start")
    b += lbl(112, y2 - 36, "ô tô con", "currentColor", 13, "start", "700")
    b += lbl(112, y2 - 16, "m′ = 1,0 tấn · cùng động năng với xe tải", ORG, 13, "start", "700")
    b += lbl(112, y2 + 6, "v′ = ?", RED, 13, "start", "700")
    return fig("d1-2", "0 0 420 206", "Xe tải 4,0 tấn tốc độ 36 km/h và ô tô con 1,0 tấn có cùng động năng với xe tải", b,
               "Dữ kiện: hai xe cùng động năng; ô tô con chưa biết tốc độ. Hình không theo tỉ lệ.")


# ───────────── Dạng 2: thùng A 12 kg ở 1,5 m, thùng B 5,0 kg ở 3,6 m ─────────────
def d2(kk):
    yf = 196; k = 40.0
    hA, hB = 1.5, 3.6
    yA, yB = yf - k * hA, yf - k * hB
    ba = (44, 28); bb = (36, 24)
    xa, xb = 88, 252
    b = ground(yf, 16, 410)
    for x0, x1, ys in ((70, 150, yA), (230, 310, yB)):
        b += seg(x0, yf, x0, ys - 4, "currentColor", 2) + seg(x1, yf, x1, ys - 4, "currentColor", 2) + seg(x0, ys, x1, ys, "currentColor", 3)
    b += dim("", "o", 172, yf, 172, yA, "1,5 m", 178, (yf + yA) / 2 + 4) + dim("", "o", 334, yf, 334, yB, "3,6 m", 340, (yf + yB) / 2 + 4)
    b += lbl(110, yA - ba[1] - 8, "A · 12 kg", "currentColor", 13, "middle", "700") + lbl(270, yB - bb[1] - 8, "B · 5,0 kg", "currentColor", 13, "middle", "700")
    if kk == 0:
        n = 24; hold = 4
        def ease(u):
            return 0.5 - 0.5 * math.cos(math.pi * u)
        us = [ease(i / n) for i in range(n + 1)] + [1.0] * hold
        dur = 0.25 * (len(us) - 1)
        ya = [yf - ba[1] - (yf - yA - 0) * u for u in us]
        yb_ = [yf - bb[1] - (yf - yB) * u for u in us]
        assert abs(ya[-1] - (yA - ba[1])) < 1e-9 and abs(yb_[-1] - (yB - bb[1])) < 1e-9
        b += (f'<rect x="{xa}" y="{ya[0]:.1f}" width="{ba[0]}" height="{ba[1]}" fill="none" stroke="{BLUE}" stroke-width="2.4">{an("y", ya, dur)}</rect>'
              f'<rect x="{xb}" y="{yb_[0]:.1f}" width="{bb[0]}" height="{bb[1]}" fill="none" stroke="{ORG}" stroke-width="2.4">{an("y", yb_, dur)}</rect>')
        return fig("d2-0", "0 0 420 232", "Hai thùng hàng được nâng từ nền kho lên hai tầng giá ở độ cao khác nhau", b,
                   "Mô phỏng: hai thùng được nâng đồng thời từ nền kho lên giá (khoảng 6 s). Độ cao vẽ đúng tỉ lệ (1 m ứng với 40 px). Chưa tính thế năng.")
    b += (f'<rect x="{xa}" y="{yA - ba[1]}" width="{ba[0]}" height="{ba[1]}" fill="none" stroke="{BLUE}" stroke-width="2.4"/>'
          f'<rect x="{xb}" y="{yB - bb[1]}" width="{bb[0]}" height="{bb[1]}" fill="none" stroke="{ORG}" stroke-width="2.4"/>')
    b += ts(110, yA + 18, "W", "tA", " = ?", BLUE, 13, "middle") + ts(270, yB + 18, "W", "tB", " = ?", ORG, 13, "middle")
    b += ts(16, 224, "Thùng C: 8,0 kg · W", "t", " = 240 J · độ cao = ?", "currentColor", 13, "start")
    return fig("d2-2", "0 0 420 232", "Thùng A và thùng B trên giá, mốc thế năng ở nền kho; thùng C chỉ cho khối lượng và thế năng", b,
               "Dữ kiện: mốc thế năng ở nền kho; độ cao A, B vẽ đúng tỉ lệ (1 m ứng với 40 px). Thùng C không vẽ vì chưa biết độ cao.")


# ───────────── Dạng 3: toà nhà, mốc dời qua các sàn ─────────────
def y3(z):
    return 174 - 10.0 * z


def building3(with_labels=True):
    b = f'<rect x="150" y="{y3(15)}" width="100" height="{y3(-4) - y3(15):.1f}" fill="none" stroke="currentColor" stroke-width="2"/>'
    for z in (15, 6, -4):
        b += seg(150, y3(z), 250, y3(z), "currentColor", 3)
    b += seg(30, y3(0), 150, y3(0), "currentColor", 3) + seg(250, y3(0), 330, y3(0), "currentColor", 3)
    b += lbl(262, y3(15) + 4, "sàn tầng 6 · 15 m", "currentColor", 12, "start", "600")
    b += lbl(262, y3(6) + 4, "sàn tầng 3 · 6,0 m", "currentColor", 12, "start", "600")
    b += lbl(336, y3(0) + 4, "mặt đường", "currentColor", 12, "start", "600")
    b += lbl(262, y3(-4) + 4, "sàn hầm · −4,0 m", "currentColor", 12, "start", "600")
    b += f'<rect x="190" y="{y3(6) - 14}" width="20" height="14" fill="none" stroke="{GRN}" stroke-width="2.2"/><circle cx="200" cy="{y3(6) - 22}" r="8" fill="none" stroke="{GRN}" stroke-width="2"/>'
    b += lbl(158, y3(6) - 36, "chậu cây 2,0 kg", "currentColor", 12, "start", "600")
    return b


def d3(kk):
    b = building3()
    if kk == 0:
        zs = [0.0] * 4
        for target, hold in ((-4.0, 6), (15.0, 8)):
            z0 = zs[-1]; nst = int(round(abs(target - z0) / 0.5))
            zs += [z0 + (target - z0) * i / nst for i in range(1, nst + 1)] + [target] * hold
        ys = [y3(z) for z in zs]
        dur = 0.12 * (len(zs) - 1)
        b += (f'<line x1="24" y1="{ys[0]:.1f}" x2="250" y2="{ys[0]:.1f}" stroke="{RED}" stroke-width="2" stroke-dasharray="7 5">{an("y1", ys, dur)}{an("y2", ys, dur)}</line>'
              f'<text x="28" y="{ys[0] - 6:.1f}" fill="{RED}" font-size="13" font-weight="700">mốc{an("y", [y - 6 for y in ys], dur)}</text>')
        return fig("d3-0", "0 0 420 236", "Toà nhà có tầng hầm; mốc thế năng dời lần lượt qua các sàn, chậu cây đặt trên sàn tầng 3 đứng yên", b,
                   "Mô phỏng: mốc thế năng (nét đứt đỏ) dời lần lượt qua các sàn của đề (khoảng 7 s); chậu cây đứng yên. Độ cao vẽ đúng tỉ lệ (1 m ứng với 10 px).")
    b += ts(158, y3(6) + 24, "W", "t", " = ? (theo từng mốc)", ORG, 12, "start")
    return fig("d3-2", "0 0 420 236", "Toà nhà có tầng hầm, mặt đường, sàn tầng 3 có chậu cây và sàn tầng 6", b,
               "Dữ kiện: các sàn vẽ đúng tỉ lệ độ cao (1 m ứng với 10 px); mốc thế năng chưa chọn, đề lần lượt đặt mốc ở ba nơi.")


# ───────────── Dạng 4: xe đạp A (40 m) → B (12 m) → C (25 m) ─────────────
ZA, ZB, ZC = 40.0, 12.0, 25.0
XA, XB, XC = 46.0, 200.0, 366.0


def prof4(n=60):
    pts = []
    for (x0, z0, x1, z1) in ((XA, ZA, XB, ZB), (XB, ZB, XC, ZC)):
        for i in range(n + 1):
            if pts and i == 0:
                continue
            u = i / n
            e = 0.5 - 0.5 * math.cos(math.pi * u)
            pts.append((x0 + (x1 - x0) * u, 200 - 4.0 * (z0 + (z1 - z0) * e)))
    return pts


def d4(kk):
    pts = prof4()
    b = seg(16, 200, 410, 200, GREY, 1.2, "5 4", .8) + lbl(260, 216, "mức chuẩn (độ cao 0)", GREY, 12, "start", "600")
    b += poly(pts, GRN, 2.6)
    for (x, z, dy, anch) in ((XA, ZA, -10, "start"), (XB, ZB, 22, "middle"), (XC, ZC, -10, "middle")):
        y = 200 - 4.0 * z
        b += seg(x, y, x, 200, GREY, 1.2, "4 4", .7) + dot(x, y, 4.5)
    b += lbl(XA - 6, 200 - 4 * ZA - 22, "A · 40 m", "currentColor", 13, "start", "700")
    b += lbl(XB, 200 - 4 * ZB + 24, "B · 12 m", "currentColor", 13, "middle", "700")
    b += lbl(XC, 200 - 4 * ZC - 24, "C · 25 m", "currentColor", 13, "middle", "700")
    b += lbl(250, 28, "người + xe đạp: 60 kg", "currentColor", 13, "start", "700")
    if kk == 0:
        L = [0.0]
        for p, q in zip(pts, pts[1:]):
            L.append(L[-1] + math.hypot(q[0] - p[0], q[1] - p[1]))
        n = 40
        idx = []
        for i in range(n + 1):
            s = L[-1] * i / n
            j = max(m for m in range(len(L)) if L[m] <= s + 1e-9)
            j = min(j, len(L) - 2)
            u = (s - L[j]) / (L[j + 1] - L[j])
            idx.append((pts[j][0] + (pts[j + 1][0] - pts[j][0]) * u, pts[j][1] + (pts[j + 1][1] - pts[j][1]) * u))
        idx += [idx[-1]] * 4
        dur = 0.2 * (len(idx) - 1)
        b += (f'<circle cx="{idx[0][0]:.1f}" cy="{idx[0][1] - 7:.1f}" r="6.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">'
              f'{an("cx", [p[0] for p in idx], dur)}{an("cy", [p[1] - 7 for p in idx], dur)}</circle>')
        return fig("d4-0", "0 0 420 226", "Người đi xe đạp chạy từ đỉnh dốc A xuống chân dốc B rồi lên đồi C", b,
                   "Mô phỏng: xe chạy dọc đường từ A qua B tới C với tốc độ không đổi (khoảng 8 s). Độ cao vẽ đúng tỉ lệ (1 m ứng với 4 px), khoảng cách ngang thì không.")
    return fig("d4-2", "0 0 420 226", "Đường đồi đi qua ba điểm A, B, C ở các độ cao khác nhau so với mức chuẩn", b,
               "Dữ kiện: ba độ cao vẽ đúng tỉ lệ (1 m ứng với 4 px); khoảng cách ngang và độ dài đường đi không theo tỉ lệ.")


# ───────────── Dạng 5: thùng 20 kg kéo lên dốc dài 10 m, nghiêng 30° ─────────────
SL = 290.0
P0 = (36.0, 204.0)
TH = 30
S_PX = 244.0 / 10.0     # px mỗi mét (quãng đường thùng đi: 10 m ↔ 244 px, trừ bề dài thùng)


def d5(kk):
    top = (P0[0] + SL * math.cos(rad(TH)), P0[1] - SL * math.sin(rad(TH)))
    b = seg(P0[0], P0[1], top[0], top[1], "currentColor", 2.6) + seg(P0[0] - 10, P0[1], 330, P0[1], GREY, 1.2, "5 4", .7)
    b += arc(P0[0], P0[1], 56, 0, TH, RED) + lbl(P0[0] + 62, P0[1] - 10, "30°", RED, 13, "start", "700")
    b += lbl(18, 28, "m = 20 kg", "currentColor", 13, "start", "700") + lbl(18, 50, "lực kéo 150 N, song song dốc", BLUE, 13, "start", "700")
    b += lbl(18, 72, "lực ma sát 25 N", ORG, 13, "start", "700")
    b += lbl(240, 186, "dốc dài 10 m", "currentColor", 13, "start", "700")
    box = f'<rect x="0" y="-24" width="36" height="24" fill="none" stroke="currentColor" stroke-width="2.4"/>'
    if kk == 0:
        a = (150 - 25 - 20 * 10 * math.sin(rad(TH))) / 20.0
        assert abs(a - 1.25) < 1e-12 and abs(math.sqrt(2 * 10 / a) - 4.0) < 1e-12
        n = 16; step = 0.25
        ss = [0.5 * a * (i * step) ** 2 for i in range(n + 1)] + [10.0] * 3
        assert abs(ss[n] - 10.0) < 1e-9
        pos = [(P0[0] + S_PX * s * math.cos(rad(TH)), P0[1] - S_PX * s * math.sin(rad(TH))) for s in ss]
        dur = step * (len(ss) - 1)
        b += f'<g transform="translate({pos[0][0]:.1f} {pos[0][1]:.1f})">{tr(pos, dur)}<g transform="rotate({-TH})">{box}</g></g>'
        return fig("d5-0", "0 0 420 232", "Thùng 20 kg được kéo từ chân dốc lên đỉnh dốc dài 10 m nghiêng 30 độ", b,
                   "Mô phỏng: thùng được kéo từ nghỉ ở chân dốc lên đỉnh dốc (đúng thời gian thật, khoảng 4 s). Chưa vẽ các lực.")
    k = 0.34
    off = 130.0                      # vị trí đặt thùng dọc dốc (px)
    ox, oy = P0[0] + off * math.cos(rad(TH)), P0[1] - off * math.sin(rad(TH))
    c0 = (ox + 18 * math.cos(rad(TH)) - 12 * math.sin(rad(TH)), oy - 18 * math.sin(rad(TH)) - 12 * math.cos(rad(TH)))
    b += f'<g transform="translate({ox:.1f} {oy:.1f})"><g transform="rotate({-TH})">{box}</g></g>'
    ux, uy = math.cos(rad(TH)), -math.sin(rad(TH))
    cx, cy = c0
    sF, tF = vec_luc("b", cx, cy, ux, uy, 150.0, k)
    sf, tf = vec_luc("o", cx, cy, -ux, -uy, 25.0, k)
    sP, tP = vec_luc("r", cx, cy, 0, 1, 200.0, k)
    b += sF + sf + sP
    b += lbl(tF[0] + 6, tF[1] + 2, "F", BLUE, 13, "start", "700") + ts(tf[0] - 10, tf[1] + 20, "F", "ms", "", ORG, 13, "end") + lbl(tP[0] + 8, tP[1] + 4, "P = mg", RED, 13, "start", "700")
    return fig("d5-2", "0 0 420 232", "Thùng trên dốc nghiêng 30 độ chịu lực kéo song song dốc, lực ma sát và trọng lực", b,
               "Dữ kiện: ba lực vẽ cùng tỉ lệ (1 N ứng với 0,34 px), đặt tại tâm thùng. Chưa vẽ phản lực của mặt dốc.")


BUILD = [d1, d2, d3, d4, d5]
