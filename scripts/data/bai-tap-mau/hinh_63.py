"""Hình cho bài tập mẫu Bài 18 "Lực ma sát" (Vật lí 10), lesson_id 63.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Chuyển động tính từ công thức (mẫu theo thời gian, nội suy tuyến tính); vectơ lực vẽ bằng vec_luc (độ dài = k·độ lớn,
đầu mũi tên chữ V 30°, không dùng marker). Dạng 1 (đứng yên hay trượt) và dạng 5 (có tụt xuống không) KHÔNG cho mô phỏng
thấy kết quả: dạng 1 vẽ đồ thị của hộp mẫu khác đề, dạng 5 chỉ chạy tới lúc vật dừng lần đầu."""
import math, os, re as _re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
G = 9.8


def rich(s, size=13):
    """`F_ms` → F với chỉ số dưới ms."""
    parts = _re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
    return out


def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)


def R(x, y, w, h, c="currentColor", sw=2, fill="none", dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}"{d} opacity="{op}"/>')


def times(T, step=0.1, extra=()):
    """Mẫu thời gian CÁCH ĐỀU (N khoảng bằng nhau, N ≈ T/step): không dùng keyTimes vì Chrome bỏ qua animateTransform
    khi keyTimes không đều (gặp ở dạng 2)."""
    n = max(2, round(T / step))
    return [T * i / n for i in range(n + 1)]


def tr_anim(ts, pos, T, rot=None):
    """Nhóm tịnh tiến theo mẫu cách đều thời gian (t, (dx, dy)); chạy một lần khi bấm, dừng ở khung cuối."""
    vals = ";".join(f"{pos(t)[0]:.2f} {pos(t)[1]:.2f}" for t in ts)
    return (f'<animateTransform attributeName="transform" type="translate" values="{vals}" '
            f'dur="{T:.3f}s" begin="indefinite" fill="freeze"/>')


def fade_at(t0, T):
    """Ẩn nhóm kể từ thời điểm t0 (rời rạc). Dạng values="1;1;0;0" + keyTimes làm Chrome bỏ qua cả animateTransform
    của nhóm cha (gặp ở dạng 2), nên dùng calcMode="discrete" với hai giá trị."""
    return (f'<animate attributeName="opacity" values="1;0" keyTimes="0;{t0 / T:.4f}" calcMode="discrete" dur="{T:.3f}s" '
            f'begin="indefinite" fill="freeze"/>')


def crate(x, gy, w, h, label, sw=2.4):
    return R(x, gy - h, w, h, sw=sw) + txt(x + w / 2, gy - h / 2 + 4, label, "currentColor", 12, "middle")


def hatch(gy, x0=16, x1=410):
    out = ground(gy, x0, x1)
    for x in range(x0 + 8, x1 - 4, 22):
        out += seg(x, gy + 8, x - 8, gy + 17, "currentColor", 1.2, "", .55)
    return out


# ───────────── Dạng 1 · hộp mẫu: đồ thị lực ma sát theo lực kéo (khác số của đề) ─────────────
def d1(kk):
    if kk == 0:
        X0, Y0, SX, SY = 70, 174, 52, 24          # F: 52 px/N; F_ms: 24 px/N
        FMAX, TR, T = 6.0, 3.2, 6.0
        NG = 4.0
        fms = lambda F: F if F <= NG else TR
        b = arrow("", "g", X0, Y0, X0 + FMAX * SX + 18, Y0, 2) + arrow("", "g", X0, Y0, X0, Y0 - 5.2 * SY, 2)
        b += txt(X0 + FMAX * SX + 18, Y0 - 9, "F kéo (N)", GRN, 12, "end") + txt(X0 + 8, Y0 - 5.2 * SY - 2, "F ma sát (N)", GRN, 12)
        for v in (0, 2, 4, 6):
            b += seg(X0 + v * SX, Y0, X0 + v * SX, Y0 + 5, "currentColor", 1.5) + txt(X0 + v * SX, Y0 + 20, str(v), "currentColor", 12, "middle", "400")
        for v in (2, 4):
            b += seg(X0 - 5, Y0 - v * SY, X0, Y0 - v * SY, "currentColor", 1.5) + txt(X0 - 9, Y0 - v * SY + 4, str(v), "currentColor", 12, "end", "400")
        curve = [(0, 0), (NG, NG), (NG, TR), (FMAX, TR)]
        b += poly([(X0 + f * SX, Y0 - y * SY) for f, y in curve], "currentColor", 1.6, "5 4", .55)
        b += txt(X0 + 1.2 * SX, Y0 - 3.1 * SY, "đứng yên", ORG, 12, "end") + txt(X0 + 5.3 * SX, Y0 - 3.2 * SY - 8, "đang trượt", ORG, 12, "end")
        ts = times(T, 0.1, [NG / FMAX * T])
        pos = lambda t: (X0 + (FMAX * t / T) * SX, Y0 - fms(FMAX * t / T) * SY)
        x0_, y0_ = pos(0)
        b += (f'<circle cx="{x0_:.1f}" cy="{y0_:.1f}" r="5.5" fill="{RED}" stroke="currentColor" stroke-width="1.5">'
              f'<animate attributeName="cx" values="{";".join(f"{pos(t)[0]:.1f}" for t in ts)}" dur="{T}s" begin="indefinite" fill="freeze"/>'
              f'<animate attributeName="cy" values="{";".join(f"{pos(t)[1]:.1f}" for t in ts)}" dur="{T}s" begin="indefinite" fill="freeze"/></circle>')
        b += txt(16, 16, "hộp mẫu 1,0 kg, lực kéo ngang tăng đều từ 0", "currentColor", 12, "start", "400")
        return fig("d1-0", "0 0 420 206", "Đồ thị lực ma sát tác dụng lên một hộp mẫu theo lực kéo ngang tăng dần từ 0 đến 6 N", b,
                   "Mô phỏng một hộp mẫu khác số của đề (không phải tủ lạnh): lực kéo tăng đều từ 0 đến 6 N trong 6 s, chấm đỏ chỉ lực ma sát tại mỗi thời điểm.")
    gy, k = 112, 0.32
    b = ground(gy, 12, 410)
    for x0, F, tag in ((30, 140, "(a)"), (225, 200, "(b)")):
        b += R(x0, gy - 62, 44, 62, sw=2.4) + txt(x0 + 22, gy - 26, "50 kg", "currentColor", 12, "middle")
        v, tip = vec_luc("r", x0 + 44, gy - 31, 1, 0, F, k, 3)
        b += v + txt(x0 + 44, gy - 44, f"F = {F} N", RED, 13)
        b += txt(x0, gy - 72, tag, "currentColor", 13, "start", "700")
    b += txt(16, 146, "bắt đầu trượt khi kéo 160 N", "currentColor", 13, "start", "600")
    b += txt(16, 166, "trượt đều khi kéo 120 N", "currentColor", 13, "start", "600")
    return fig("d1-2", "0 0 420 180", "Hai lần kéo tủ lạnh 50 kilôgam trên sàn bằng lực ngang 140 niutơn và 200 niutơn, kèm hai mốc đo được",
               b, "Dữ kiện của đề: hai lực kéo và hai mốc đo (vectơ F vẽ tỉ lệ với độ lớn). " + NOTE)


# ───────────── Dạng 2 · thùng 40 kg: kéo 98 N trượt đều; kéo 150 N; buông dây sau 4 s ─────────────
def d2(kk):
    a1, T1 = 1.3, 4.0
    v1 = a1 * T1
    a2 = 0.25 * G
    T2 = v1 / a2
    T = T1 + T2
    S = 16
    def x_m(t):
        if t <= T1:
            return 0.5 * a1 * t * t
        tau = t - T1
        return 0.5 * a1 * T1 * T1 + v1 * tau - 0.5 * a2 * tau * tau
    if kk == 0:
        gy, X0, W, H = 118, 24, 56, 36
        k = 0.4
        b = hatch(gy)
        b += R(X0, gy - H, W, H, sw=1.4, dash="5 4", op=.45)
        v, tip = vec_luc("r", X0 + W, gy - H / 2, 1, 0, 150, k, 3)
        inner = crate(X0, gy, W, H, "40 kg") + f'<g>{v}{txt(X0 + W + 6, gy - H / 2 - 10, "F = 150 N", RED)}{fade_at(T1, T)}</g>'
        ts = times(T, 0.05)
        b += f'<g>{tr_anim(ts, lambda t: (S * x_m(t), 0), T)}{inner}</g>'
        b += txt(16, 22, "kéo 150 N trong 4,0 s rồi buông dây", "currentColor", 13, "start", "400")
        b += txt(16, 40, "μ = ?", ORG)
        return fig("d2-0", "0 0 420 150", "Thùng gỗ được kéo trượt nhanh dần trên sàn ngang trong 4 giây rồi dây được buông, thùng trượt chậm dần đến dừng",
                   b, "Mô phỏng đúng thời gian thật, tính từ số liệu của đề (hình minh hoạ, không có thước đo).")
    gy, k = 112, 0.5
    b = ground(gy, 12, 410)
    for x0, F, tag in ((30, 98, "thùng trượt đều"), (225, 150, "thùng bắt đầu từ trạng thái nghỉ")):
        b += R(x0, gy - 36, 56, 36, sw=2.4) + txt(x0 + 28, gy - 14, "40 kg", "currentColor", 12, "middle")
        v, tip = vec_luc("r", x0 + 56, gy - 18, 1, 0, F, k, 3)
        b += v + txt(x0 + 56, gy - 30, f"F = {F} N", RED, 13)
        b += txt(x0, gy - 48, tag, "currentColor", 12, "start", "400")
    b += txt(16, 150, "g = 9,8 m/s²", "currentColor", 13, "start", "600")
    return fig("d2-2", "0 0 420 166", "Hai lần kéo thùng 40 kilôgam trên sàn ngang: lực 98 niutơn làm thùng trượt đều, lực 150 niutơn kéo từ trạng thái nghỉ",
               b, "Dữ kiện của đề (vectơ F vẽ tỉ lệ với độ lớn). " + NOTE)


# ───────────── Dạng 3 · thùng 6,0 kg kéo xiên 30° bằng 30 N, μ = 0,30 ─────────────
def d3(kk):
    m, F, al, mu = 6.0, 30.0, 30.0, 0.30
    ar = math.radians(al)
    N = m * G - F * math.sin(ar)
    a = (F * math.cos(ar) - mu * N) / m
    if kk == 0:
        T, S = 4.0, 11
        gy, X0, W, H = 128, 24, 60, 40
        k = 2.0
        ox, oy = X0 + W, gy - H / 2
        b = hatch(gy)
        b += R(X0, gy - H, W, H, sw=1.4, dash="5 4", op=.45)
        v, tip = vec_luc("r", ox, oy, math.cos(ar), -math.sin(ar), F, k, 3)
        ref = seg(ox, oy, ox + 74, oy, "currentColor", 1.2, "5 4", .6)
        arcp = arc(ox, oy, 40, 0, al, GRN, 1.8)
        inner = (crate(X0, gy, W, H, "6,0 kg") + v + ref + arcp + txt(ox + 44, oy - 4, "30°", GRN, 12, "start")
                 + txt(tip[0] - 4, tip[1] - 6, "F = 30 N", RED, 13, "end"))
        ts = times(T, 0.1)
        b += f'<g>{tr_anim(ts, lambda t: (S * 0.5 * a * t * t, 0), T)}{inner}</g>'
        b += txt(16, 22, "μ = 0,30", ORG) + txt(16, 40, "g = 9,8 m/s²", "currentColor", 13, "start", "400")
        return fig("d3-0", "0 0 420 160", "Thùng 6 kilôgam được kéo bằng dây chếch lên 30 độ so với phương ngang, trượt nhanh dần trên sàn nằm ngang trong 4 giây",
                   b, "Mô phỏng chạy đúng thời gian thật 4,0 s, tính từ số liệu của đề (hình minh hoạ, không có thước đo).")
    gy, k = 134, 1.2
    cx, cy, W, H = 150, gy - 22, 44, 44
    b = hatch(gy, 12, 410) + R(cx - W / 2, gy - H, W, H, sw=2.4)
    b += seg(cx, cy, cx + 120, cy, "currentColor", 1.2, "5 4", .6) + arc(cx, cy, 52, 0, al, GRN, 1.8) + txt(cx + 58, cy - 6, "30°", GRN, 12)
    v, tip = vec_luc("r", cx, cy, math.cos(ar), -math.sin(ar), F, k, 3)
    b += v + txt(tip[0] + 4, tip[1] - 8, "F = 30 N", RED, 13)
    v, tip = vec_luc("g", cx, cy, 0, 1, m * G, k, 3)
    b += v + txt(cx + 8, cy + m * G * k - 4, "P = mg", GRN, 13)
    b += txt(16, 24, "m = 6,0 kg · μ = 0,30", "currentColor", 13, "start", "600")
    b += txt(268, 62, "Cần: N, F_ms, a", ORG, 13, "start", "600")
    return fig("d3-2", "0 0 420 190", "Thùng chịu lực kéo chếch lên 30 độ và trọng lực; chưa vẽ phản lực và lực ma sát vì chưa biết độ lớn",
               b, "Dữ kiện của đề: lực kéo F và trọng lực P (vẽ tỉ lệ với độ lớn, gốc ở tâm thùng). N và F_ms chưa vẽ vì chưa tính. " + NOTE)


# ───────────── Dạng 4 · bao 12 kg trượt xuống ván dài 5,0 m nghiêng 35°, μ = 0,30 ─────────────
def d4(kk):
    m, L, al, mu = 12.0, 5.0, 35.0, 0.30
    ar = math.radians(al)
    a = G * (math.sin(ar) - mu * math.cos(ar))
    T = math.sqrt(2 * L / a)
    S = 56
    w, h = 34, 24
    ext = w / 2 + 8                                             # ván dài thêm mỗi đầu để vật nằm trọn trên ván
    tx, ty = 48, 30                                             # đầu trên của ván
    end = S * L + 2 * ext
    fx, fy = tx + end * math.cos(ar), ty + end * math.sin(ar)   # chân ván chạm đất
    gy = fy
    def scr(lx, ly):                                            # toạ độ cục bộ (dọc ván, vuông góc ván) → toạ độ hình
        return tx + lx * math.cos(ar) - ly * math.sin(ar), ty + lx * math.sin(ar) + ly * math.cos(ar)
    if kk == 0:
        b = ground(gy, 16, 410)
        b += f'<g transform="translate({tx} {ty}) rotate({al})">'
        b += seg(0, 0, end, 0, "currentColor", 3.2)
        b += R(ext - w / 2, -h, w, h, sw=1.4, dash="5 4", op=.45)
        ts = times(T, 0.05)
        inner = R(ext - w / 2, -h, w, h, sw=2.4) + txt(ext, -h / 2 + 4, "12 kg", "currentColor", 11, "middle")
        b += f'<g>{tr_anim(ts, lambda t: (S * 0.5 * a * t * t, 0), T)}{inner}</g></g>'
        b += arc(fx, fy, 46, 180 - al, 180, GRN, 1.8) + txt(fx - 76, fy - 9, "35°", GRN, 12, "end")
        b += txt(250, 40, "m = 12 kg", "currentColor", 13) + txt(250, 60, "μ = 0,30", ORG) + txt(250, 80, "L = 5,0 m", "currentColor", 13)
        b += txt(250, 100, "v₀ = 0", "currentColor", 13, "start", "400") + txt(250, 120, "g = 9,8 m/s²", "currentColor", 13, "start", "400")
        return fig("d4-0", "0 0 420 %d" % (gy + 22), "Bao hàng được thả ở đỉnh tấm ván dốc dài 5 mét nghiêng 35 độ và trượt xuống chân ván",
                   b, "Mô phỏng đúng thời gian thật, tính từ số liệu của đề; góc nghiêng và quãng đường trượt L vẽ đúng tỉ lệ.")
    K = 0.45
    b = ground(gy, 16, 410) + seg(tx, ty, fx, fy, "currentColor", 3.2)
    lc = ext + 0.5 * S * L
    b += f'<g transform="translate({tx} {ty}) rotate({al})">{R(lc - w / 2, -h, w, h, sw=2.4)}</g>'
    cx, cy = scr(lc, -h / 2)
    b += arc(fx, fy, 46, 180 - al, 180, GRN, 1.8) + txt(fx - 76, fy - 9, "35°", GRN, 12, "end")
    v, tip = vec_luc("g", cx, cy, 0, 1, m * G, K, 3)
    b += v + txt(cx - 8, cy + m * G * K - 2, "P = mg", GRN, 13, "end")
    ux, uy = math.cos(ar), math.sin(ar)
    b += seg(cx, cy, cx + 90 * ux, cy + 90 * uy, "currentColor", 1.2, "5 4", .6) + txt(cx + 94 * ux, cy + 94 * uy, "x", "currentColor", 12)
    nx, ny = -math.sin(ar), -math.cos(ar)
    b += seg(cx, cy, cx + 70 * nx, cy + 70 * ny, "currentColor", 1.2, "5 4", .6) + txt(cx + 74 * nx - 14, cy + 74 * ny + 4, "y", "currentColor", 12)
    b += txt(250, 40, "m = 12 kg · μ = 0,30", "currentColor", 13, "start", "600") + txt(250, 60, "L = 5,0 m · v₀ = 0", "currentColor", 13, "start", "600")
    b += txt(250, 84, "Cần: N, F_ms, a, v", ORG, 13, "start", "600")
    return fig("d4-2", "0 0 420 %d" % (gy + 22), "Bao hàng trên ván nghiêng 35 độ chịu trọng lực P; trục x dọc ván hướng xuống, trục y vuông góc ván",
               b, "Dữ kiện của đề: trọng lực P (vẽ tỉ lệ với độ lớn), trục x dọc ván hướng xuống, trục y vuông góc ván. N và F_ms chưa vẽ vì chưa tính.")


# ───────────── Dạng 5 · vật 3,0 kg, v₀ = 6,0 m/s lên dốc 25°, μ = 0,20 ─────────────
def d5(kk):
    m, v0, al, mu = 3.0, 6.0, 25.0, 0.20
    ar = math.radians(al)
    a_up = G * (math.sin(ar) + mu * math.cos(ar))
    T = v0 / a_up
    s_max = v0 * v0 / (2 * a_up)
    S = 66
    fx, fy = 36, 196                                           # chân dốc
    gy = fy
    w, h = 34, 24
    x0 = w / 2 + 10                                             # tâm vật cách chân dốc một đoạn để vật nằm trọn trên dốc
    if kk == 0:
        b = ground(gy, 16, 410)
        b += f'<g transform="translate({fx} {fy}) rotate({-al})">'
        b += seg(0, 0, 4.3 * S, 0, "currentColor", 3.2)
        b += R(x0 - w / 2, -h, w, h, sw=1.4, dash="5 4", op=.45)
        ts = times(T, 0.025)
        inner = R(x0 - w / 2, -h, w, h, sw=2.4) + txt(x0, -h / 2 + 4, "3,0 kg", "currentColor", 11, "middle")
        b += f'<g>{tr_anim(ts, lambda t: (S * (v0 * t - 0.5 * a_up * t * t), 0), T)}{inner}</g></g>'
        b += arc(fx, fy, 56, 0, al, GRN, 1.8) + txt(fx + 62, fy - 5, "25°", GRN, 12)
        b += txt(250, 190, "μ = 0,20", ORG) + txt(250, 168, "v₀ = 6,0 m/s dọc dốc", "currentColor", 13) + txt(250, 146, "g = 9,8 m/s²", "currentColor", 13, "start", "400")
        return fig("d5-0", "0 0 420 216", "Vật được truyền vận tốc đầu dọc mặt dốc hướng lên từ chân dốc nghiêng 25 độ; mô phỏng dừng ở lúc vật lên tới điểm cao nhất",
                   b, "Mô phỏng đúng thời gian thật, chỉ chạy tới lúc vật lên tới điểm cao nhất (tính từ số liệu của đề).")
    K = 1.6
    b = ground(gy, 16, 410) + seg(fx, fy, fx + 4.3 * S * math.cos(ar), fy - 4.3 * S * math.sin(ar), "currentColor", 3.2)
    b += f'<g transform="translate({fx} {fy}) rotate({-al})">{R(x0 + 120 - w / 2, -h, w, h, sw=2.4)}</g>'
    cx = fx + (x0 + 120) * math.cos(ar) - math.sin(ar) * (h / 2)
    cy = fy - (x0 + 120) * math.sin(ar) - math.cos(ar) * (h / 2)
    b += arc(fx, fy, 56, 0, al, GRN, 1.8) + txt(fx + 62, fy - 5, "25°", GRN, 12)
    ux, uy = math.cos(ar), -math.sin(ar)
    v, tip = vec_luc("b", cx, cy, ux, uy, v0, 12, 3)
    b += v + txt(tip[0] + 4, tip[1] - 6, "v₀", BLUE, 13)
    v, tip = vec_luc("g", cx, cy, 0, 1, m * G, 1.0, 3)
    b += v + txt(cx + 8, cy + m * G * 1.0 + 2, "P = mg", GRN, 13)
    b += txt(16, 24, "m = 3,0 kg · μ = 0,20", "currentColor", 13, "start", "600")
    b += txt(16, 44, "coi F_msn max = F_mst", "currentColor", 13, "start", "400")
    b += txt(16, 68, "Cần: a, s, trượt lại?, v", ORG, 13, "start", "600")
    return fig("d5-2", "0 0 420 216", "Vật ở chân dốc nghiêng 25 độ với vận tốc đầu hướng lên dốc và trọng lực P",
               b, "Dữ kiện của đề: vận tốc đầu v₀ và trọng lực P (mỗi loại vectơ vẽ tỉ lệ với độ lớn của nó, v₀ và P khác tỉ lệ). N và F_ms chưa vẽ vì chưa tính.")
