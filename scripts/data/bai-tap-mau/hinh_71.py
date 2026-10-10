"""Hình cho bài tập mẫu Bài 26 "Cơ năng và định luật bảo toàn cơ năng" (Vật lí 10), lesson_id 71.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mọi chuyển động TÍNH THẬT: ném thẳng đứng theo z = z0 + v0·t − g·t²/2; máng cong giải phương trình chuyển động bằng tích phân số
(kiểm tra bảo toàn cơ năng); dốc có lực cản: gia tốc đều a = v²/(2L) ứng với đúng công cản của đề. Ảnh đứng yên không ghi đáp số."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from svg_lib import vec_luc

GREY = "#94a3b8"
G = 10.0


def zt(z0, v0, t):
    return z0 + v0 * t - 0.5 * G * t * t


def vert_pts(z0, v0, x, y0, s, n=None, dt=0.1):
    """Mẫu cách đều thời gian dt của vật ném thẳng đứng, dừng khi chạm đất (z=0). y0 = pixel của z=0, s = px/m."""
    T = (v0 + math.sqrt(v0 * v0 + 2 * G * z0)) / G
    n = n or int(math.ceil(T / dt))
    dtt = T / n
    pts = [(x, y0 - s * max(0.0, zt(z0, v0, i * dtt))) for i in range(n + 1)]
    return pts, dtt, T


def ts(x, y, base, sb, tail="", c="currentColor", size=13, anchor="start", weight="700"):
    """Nhãn có chỉ số dưới: base_sb tail."""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{base}<tspan dy="4" font-size="{size - 3}">{sb}</tspan><tspan dy="-4">{tail}</tspan></text>')


def guide(x0, x1, y, label, lx, anchor="start", c=GREY, dash="4 4"):
    return seg(x0, y, x1, y, c, 1.2, dash, .85) + lbl(lx, y + 4, label, "currentColor", 13, anchor, "600")


def building(x0, x1, ytop, ybot):
    return f'<rect x="{x0}" y="{ytop}" width="{x1 - x0}" height="{ybot - ytop}" fill="none" stroke="currentColor" stroke-width="2.4"/>'


# ───────────── Dạng 1: đá ném lên từ cửa sổ 6 m, qua P (8 m) với v = 3 m/s; mốc đất / cửa sổ / mái 10 m ─────────────
def d1(kk):
    y0, s, X = 250, 20.0, 170
    b = ground(y0, 16, 410) + building(40, 150, y0 - 200, y0)
    b += f'<rect x="128" y="{y0 - 6 * s - 12:.0f}" width="22" height="24" fill="none" stroke="currentColor" stroke-width="1.8"/>'
    b += guide(150, 262, y0 - 10 * s, "mái sân thượng: 10 m", 270)
    b += guide(150, 262, y0 - 8 * s, "P: 8,0 m", 270)
    b += guide(150, 262, y0 - 6 * s, "cửa sổ: 6,0 m", 270)
    b += ts(270, y0 - 8 * s + 22, "v", "P", " = 3,0 m/s", RED)
    b += lbl(270, y0 + 28, "mặt đất", "currentColor", 13, "start", "600")
    pP = (X, y0 - 8 * s)
    b += f'<circle cx="{pP[0]}" cy="{pP[1]:.0f}" r="9" fill="none" stroke="currentColor" stroke-width="1.6"/>'
    if kk == 0:
        pts, dtt, T = vert_pts(6.0, 7.0, X, y0, s, dt=0.1)
        assert abs(T - 2.0) < 1e-9 and abs(zt(6.0, 7.0, 0.4) - 8.0) < 1e-9 and abs(7.0 - G * 0.4 - 3.0) < 1e-9     # qua P (8 m) lúc 0,4 s với v = 3 m/s
        b += ball(pts, 0, dtt)
        return fig("d1-0", "0 0 420 284", "Hòn đá ném thẳng đứng lên từ cửa sổ, qua điểm P rồi rơi xuống đất", b,
                   "Mô phỏng: ném thẳng đứng lên từ cửa sổ, chạy đúng thời gian thật (khoảng 2 s). Độ cao vẽ đúng tỉ lệ. Tốc độ tại P ghi trên hình.")
    b += f'<circle cx="{X}" cy="{pP[1]:.0f}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5"/>'
    v, _ = vec_luc("b", X, pP[1] - 7, 0, -1, 3.0, 8.0)
    b += v
    return fig("d1-2", "0 0 420 284", "Hòn đá đang đi lên qua điểm P cách mặt đất 8 mét", b,
               "Dữ kiện: ba mốc có thể chọn — mặt đất, cửa sổ, mái sân thượng. Độ cao vẽ đúng tỉ lệ. Mũi tên là vận tốc tại P (đi lên).")


# ───────────── Dạng 2: máng cong nhẵn, A cao 2,45 m, M cao 1,2 m ─────────────
HA, AW = 2.45, 2.8          # độ cao A, bề ngang đoạn máng cong (m)


def chute_z(x):
    return HA * (1 - x / AW) ** 2 if x < AW else 0.0


def chute_dz(x):
    return -2 * HA * (1 - x / AW) / AW if x < AW else 0.0


def chute_run(dt_s=0.05, x_end=3.9):
    """Tích phân số chuyển động trượt không ma sát trên máng; trả các mẫu cách đều dt_s: (x, z, v). Kiểm tra bảo toàn cơ năng."""
    x, v, t, h = 0.0, 0.0, 0.0, 1e-4
    out = [(0.0, chute_z(0), 0.0)]
    nxt = dt_s
    while x < x_end:
        dz = chute_dz(x)
        a = G * (-dz) / math.sqrt(1 + dz * dz)
        v += a * h
        x += v * h / math.sqrt(1 + dz * dz)
        t += h
        if t >= nxt - 1e-12:
            out.append((x, chute_z(x), v))
            nxt += dt_s
        if x >= AW and len(out) > 1 and out[-1][0] >= x_end:
            break
    for (xx, zz, vv) in out[1:]:
        assert abs(vv * vv / 2 + G * zz - G * HA) < 0.02 * G * HA, ("bảo toàn cơ năng lệch", xx, zz, vv)
    return out


def d2(kk):
    yf, s, x0 = 170, 40.0, 130
    b = ground(yf, 16, 410)
    curve = [(x0 + s * u * AW / 60, yf - s * chute_z(u * AW / 60)) for u in range(61)]
    b += poly(curve, "currentColor", 2.6) + seg(curve[-1][0], yf, 400, yf, "currentColor", 2.6)
    b += seg(x0, yf, x0, curve[0][1], "currentColor", 1.6, "", .5)
    xm = AW * (1 - math.sqrt(1.2 / HA))
    pm = (x0 + s * xm, yf - s * chute_z(xm))
    assert abs(chute_z(xm) - 1.2) < 1e-9
    b += seg(100, 100, 100, yf, "currentColor", 1.4) + seg(94, 100, 106, 100, "currentColor", 1.4)
    b += seg(94, yf, 106, yf, "currentColor", 1.4)
    yA, yM = yf - s * HA, yf - s * 1.2
    b += seg(94, yA, 106, yA, "currentColor", 1.4) + seg(94, yM, 106, yM, "currentColor", 1.4) + seg(100, yA, 100, yf, "currentColor", 1.4)
    b += seg(106, yA, x0, yA, GREY, 1.2, "4 4", .9) + seg(106, yM, pm[0], yM, GREY, 1.2, "4 4", .9)
    b += lbl(92, yA + 4, "A: 2,45 m", "currentColor", 13, "end", "700") + lbl(92, yM + 4, "M: 1,2 m", "currentColor", 13, "end", "700")
    b += lbl(92, yf + 26, "chân máng O", "currentColor", 13, "end", "700")
    b += dot(x0, yA, 4.5, RED) + dot(pm[0], pm[1], 4.5, RED)
    b += lbl(x0 + 10, yA - 6, "A", RED, 14, "start", "700") + lbl(pm[0] + 10, pm[1] - 8, "M", RED, 14, "start", "700")
    if kk == 0:
        run = chute_run(0.05)
        pts = []
        for (xx, zz, vv) in run:
            dz = chute_dz(xx); m = -dz
            nx, ny = (m, -1.0) if xx < AW else (0.0, -1.0)
            nn = math.hypot(nx, ny)
            pts.append((x0 + s * xx + 6.5 * nx / nn, yf - s * zz + 6.5 * ny / nn))
        assert abs(run[-1][2] - 7.0) < 0.15       # trên sàn ngang tốc độ = √(2gH) = 7 m/s
        b += ball(pts, 0, 0.10)
        return fig("d2-0", "0 0 420 200", "Hòn bi trượt từ đỉnh A xuống chân máng cong nhẵn rồi chạy tiếp trên sàn ngang", b,
                   "Mô phỏng: bi thả nhẹ tại A, trượt không ma sát; chạy chậm 2 lần so với thực tế. Độ cao vẽ đúng tỉ lệ.")
    b += dot(x0 + 7, yA - 7, 5.5, GRN)
    return fig("d2-2", "0 0 420 200", "Máng cong nhẵn: A cao 2,45 m, M cao 1,2 m so với chân máng O", b,
               "Dữ kiện: độ cao của A và M so với chân máng O (mốc thế năng). Điểm N ở ý c chưa được đánh dấu.")


# ───────────── Dạng 3: ném thẳng đứng từ mặt đất, v0 = 12 m/s ─────────────
def d3(kk):
    y0, s, X = 220, 20.0, 130
    b = ground(y0 + 5.5, 16, 410) + lbl(150, y0 + 28, "mặt đất (mốc thế năng)", "currentColor", 13, "start", "600")
    b += guide(X + 14, 300, y0 - 5 * s, "độ cao 5,0 m", 308)
    v, _ = vec_luc("b", X, y0 - 8, 0, -1, 12.0, 3.0)
    b += v + ts(X + 10, y0 - 22, "v", "0", " = 12 m/s", BLUE)
    if kk == 0:
        T = 2 * 12.0 / G
        n = 24
        pts = [(X, y0 - s * max(0.0, zt(0.0, 12.0, T * i / n))) for i in range(n + 1)]
        assert abs(zt(0.0, 12.0, T)) < 1e-9
        b += ball(pts, 0, T / n)
        return fig("d3-0", "0 0 420 250", "Hòn đá ném thẳng đứng lên từ mặt đất rồi rơi xuống", b,
                   "Mô phỏng: ném thẳng đứng lên từ mặt đất, chạy đúng thời gian thật (khoảng 2,4 s). Không ghi thang độ cao.")
    b += dot(X, y0 - 5 * s, 5.5, GRN)
    return fig("d3-2", "0 0 420 250", "Hòn đá ném lên từ mặt đất; mốc thế năng ở mặt đất; xét độ cao 5,0 mét", b,
               "Dữ kiện: tốc độ ném và độ cao 5,0 m ở ý d. Độ cao ở ý c chưa được đánh dấu.")


# ───────────── Dạng 4: ném lên từ sân thượng 3 m, đạt 8 m ─────────────
def d4(kk):
    y0, s, X = 250, 20.0, 175
    b = ground(y0, 16, 410) + building(40, 150, y0 - 3 * s, y0)
    b += guide(150, 290, y0 - 3 * s, "sân thượng: 3,0 m", 298)
    b += guide(150, 290, y0 - 8 * s, "cực đại: 8,0 m", 298)
    b += lbl(298, y0 + 28, "mặt đất", "currentColor", 13, "start", "600")
    if kk == 0:
        pts, dtt, T = vert_pts(3.0, 10.0, X, y0, s, n=24)
        assert abs(zt(3.0, 10.0, 1.0) - 8.0) < 1e-9 and max((y0 - p[1]) / s for p in pts) < 8.0 + 0.2
        b += ball(pts, 0, dtt)
        return fig("d4-0", "0 0 420 284", "Hòn sỏi ném thẳng đứng lên từ mép sân thượng, lên tới độ cao cực đại rồi rơi xuống đất", b,
                   "Mô phỏng: ném lên từ mép sân thượng, chạy đúng thời gian thật (khoảng 2,3 s). Độ cao vẽ đúng tỉ lệ.")
    b += dot(X, y0 - 8 * s, 5.5, GRN) + lbl(X + 12, y0 - 8 * s - 8, "v = 0", RED, 13, "start", "700")
    return fig("d4-2", "0 0 420 284", "Hòn sỏi ở điểm cao nhất, cách mặt đất 8 mét; sân thượng cao 3 mét", b,
               "Dữ kiện: sân thượng 3,0 m; điểm cao nhất 8,0 m so với mặt đất. Độ cao vẽ đúng tỉ lệ.")


# ───────────── Dạng 5: trượt tuyết, dốc A cao 10 m, tới B với 12 m/s (có lực cản) ─────────────
def d5(kk):
    ang = math.radians(30)
    s = 12.0
    A = (60.0, 40.0)
    L = 20.0                                   # độ dài dốc (m) = 10 m / sin 30°
    B = (A[0] + s * L * math.cos(ang), A[1] + s * L * math.sin(ang))
    yf = B[1]
    b = ground(yf, 16, 410) + seg(A[0], A[1], B[0], B[1], "currentColor", 2.6) + seg(B[0], yf, 400, yf, "currentColor", 2.6)
    b += seg(A[0], A[1], A[0], yf, "currentColor", 1.6, "", .5)
    b += seg(40, A[1], 40, yf, "currentColor", 1.4) + seg(34, A[1], 46, A[1], "currentColor", 1.4) + seg(34, yf, 46, yf, "currentColor", 1.4)
    b += lbl(32, (A[1] + yf) / 2 + 4, "10 m", "currentColor", 13, "end", "700")
    b += dot(A[0], A[1], 4.5, RED) + dot(B[0], B[1], 4.5, RED)
    b += lbl(A[0] + 8, A[1] - 8, "A", RED, 14, "start", "700") + lbl(B[0] - 4, yf + 24, "B", RED, 14, "middle", "700")
    b += lbl(B[0] + 12, yf - 12, "tại B: 12 m/s", "currentColor", 13, "start", "700")
    nrm = (math.sin(ang), -math.cos(ang))
    if kk == 0:
        a = 12.0 ** 2 / (2 * L)                 # a = 3,6 m/s² (lực cản không đổi 70 N ứng với công cản −1400 J)
        assert abs(50 * (G * 0.5 - a) * L - 1400) < 1e-6
        T = 12.0 / a
        n = 20
        pts = []
        for i in range(n + 1):
            d = 0.5 * a * (T * i / n) ** 2
            pts.append((A[0] + s * d * math.cos(ang) + 6.5 * nrm[0], A[1] + s * d * math.sin(ang) + 6.5 * nrm[1]))
        b += ball(pts, 0, T / n)
        return fig("d5-0", "0 0 420 210", "Vận động viên trượt tuyết từ nghỉ ở đỉnh dốc A xuống chân dốc B", b,
                   "Mô phỏng: trượt từ nghỉ ở A xuống B, chạy đúng thời gian thật (khoảng 3,3 s). Độ cao vẽ đúng tỉ lệ.")
    b += dot(A[0] + 6.5 * nrm[0], A[1] + 6.5 * nrm[1], 5.5, GRN)
    b += lbl(A[0] + 70, A[1] + 4, "lượt 2: qua A với 5,0 m/s", "currentColor", 13, "start", "600")
    return fig("d5-2", "0 0 420 210", "Dốc cao 10 mét: lượt đầu xuất phát từ nghỉ, lượt hai qua A với 5,0 mét trên giây", b,
               "Dữ kiện: độ cao dốc và tốc độ tại B của lượt đầu; tốc độ tại A của lượt hai. Độ cao vẽ đúng tỉ lệ.")


BUILD = [d1, d2, d3, d4, d5]
