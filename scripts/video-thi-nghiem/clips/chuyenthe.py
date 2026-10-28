# Clip: tn-l12-chuyenthe-01 - Dun nuoc da, moi phut ghi nhiet do mot lan (ban 3, 27/10/2026: truc t co dinh,
# lo dap an C + phong to doan -6 -> 0 °C, tach hinh phan tu luc tan / luc soi, cau hoi chot, tieng bao thay nhac)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-chuyenthe-01.json -> so_lieu_mau (khong them diem).
# Canh: Du doan (4 lua chon cung kieu) -> Tien hanh (coc + dau do + dong ho, do thi ve dan, tua nhanh)
#       -> Dap an + vi sao nam ngang (tan: pha lien ket; soi: phan tu thoat ra) -> Gioi han (+-0,5 °C) + Bay
#       -> Chot + cau hoi tu nho lai (4 phut vs 27 phut, goi y lambda, L tu tham_so).
import random
import numpy as np
from engine import *

ROWS = [(0, -6.0), (1, 0.2), (2, 0.2), (3, 0.2), (4, 0.3), (5, 17.8), (6, 38.0), (7, 58.1), (8, 78.0), (9, 98.1),
        (10, 100.2), (11, 100.3), (15, 100.3), (20, 100.3), (25, 100.3), (30, 100.3), (35, 100.2)]
TT = [r[0] for r in ROWS]; TV = [r[1] for r in ROWS]
def Tline(tau): return float(np.interp(tau, TT, TV))          # duong noi cac diem do
def reading(tau):                                              # so doc gan nhat (doc moi phut / moi 5 phut)
    k = 0
    for i, r in enumerate(ROWS):
        if r[0] <= tau + 1e-6: k = i
    return ROWS[k]
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",").replace("-", "−")

ICE = [(-95, 0), (-15, 0), (65, 0), (-60, 1), (25, 1), (-20, 2), (90, 1)]   # (dx, tang) vien da
R = random.Random(5)
BUB = [(R.uniform(-0.42, 0.42), R.random(), R.uniform(0.8, 1.3), R.uniform(5, 10)) for _ in range(16)]

def dashed(d, p1, p2, color, w=3, dash=16, gap=12):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

def pill(d, cx, cy, s, size, fg, bg, alpha=1.0, padx=26):
    wdt = tw(d, s, F(size)) + 2 * padx
    card(d, (cx - wdt / 2, cy - size * 0.85, cx + wdt / 2, cy + size * 0.85), fill=A(bg, alpha), r=int(size * 0.85))
    text(d, (cx, cy), s, size, fg, alpha=alpha)
    return wdt

# ---------------- coc + bep + dau do ----------------
def beaker(d, t, tau, cx, base, s=1.0, probe_to=None):
    w, h = 330 * s, 360 * s; x0, x1, top = cx - w / 2, cx + w / 2, base - h
    inner = h - 14 * s
    f_ice = 1 - clamp((tau - 0.15) / 3.98)                     # da con lai (mo hinh: tan het o 248 s)
    if tau < 10: lvl = 0.62 * (1 - f_ice)
    else: lvl = 0.62 * (1 - clamp((tau - 10) / 26.0) * 0.97)  # nuoc can dan khi soi, can o ~phut 36
    wl = base - 8 * s - inner * lvl
    Tc = Tline(tau)
    wcol = mix((170, 210, 250), (196, 214, 236), clamp(Tc / 100))
    # than coc (kinh)
    d.rounded_rectangle([x0, top, x1, base], radius=int(22 * s), fill=(240, 246, 252))
    if lvl > 0.005:
        d.rounded_rectangle([x0 + 8 * s, wl, x1 - 8 * s, base - 8 * s], radius=int(16 * s), fill=wcol)
        d.line([(x0 + 10 * s, wl), (x1 - 10 * s, wl)], fill=(120, 170, 225), width=max(2, int(4 * s)))
    # vien da
    if f_ice > 0.02:
        sz0 = 78 * s; sz = sz0 * f_ice ** 0.55; al = clamp(f_ice / 0.12)
        for dx, lay in ICE:
            stack_top = base - 10 * s - sz0 * (lay + 1) * 0.92 + (sz0 - sz)
            ytop = min(stack_top, wl - 0.15 * sz) if lvl > 0.02 else stack_top
            ix = cx + dx * s - sz / 2
            d.rounded_rectangle([ix, ytop, ix + sz, ytop + sz], radius=int(12 * s * max(0.4, f_ice)),
                                fill=A((248, 252, 255), al), outline=A((110, 160, 215), al), width=max(2, int(4 * s)))
            d.line([(ix + sz * 0.2, ytop + sz * 0.25), (ix + sz * 0.45, ytop + sz * 0.25)], fill=A(WHITE, al), width=max(2, int(5 * s)))
    # bot khi va hoi khi soi (tu phut ~9,1)
    boil = clamp((tau - 9.1) / 0.6) * (1 if lvl > 0.08 else 0)
    if boil > 0:
        depth = base - 8 * s - wl
        for (u, ph, sp, r) in BUB:
            yy = base - 14 * s - ((t * 0.9 * sp + ph) % 1) * max(10, depth - 20 * s)
            d.ellipse([cx + u * w - r * s, yy - r * s, cx + u * w + r * s, yy + r * s], outline=A(WHITE, boil), width=max(2, int(3 * s)))
        for i in range(3):
            sx = cx + (-80 + i * 80) * s
            pts = [(sx + 16 * s * math.sin(t * 2.6 + i * 1.7 + k * 0.8), top - 20 * s - k * 30 * s) for k in range(6)]
            d.line(pts, fill=A(GRAY, 0.45 * boil), width=max(3, int(8 * s)), joint="curve")
    # que khuay (lac nhe)
    sw = math.sin(t * 3.2) * 18 * s
    d.line([(cx - 120 * s + sw, top - 70 * s), (cx - 30 * s + sw * 0.4, base - 40 * s)], fill=(176, 120, 70), width=max(4, int(12 * s)))
    # dau do nhiet ke dien tu: dau khong cham day
    px = cx + 105 * s
    d.line([(px, top - 90 * s), (px, base - 75 * s)], fill=(120, 126, 140), width=max(4, int(12 * s)))
    dot(d, px, base - 72 * s, 9 * s, NAVY)
    if probe_to:
        P0 = (px, top - 90 * s); P3 = probe_to; P1 = (px, top - 170 * s); P2 = (P3[0] - 90, P3[1])
        pts = [(((1 - u) ** 3) * P0[0] + 3 * u * (1 - u) ** 2 * P1[0] + 3 * u * u * (1 - u) * P2[0] + u ** 3 * P3[0],
                ((1 - u) ** 3) * P0[1] + 3 * u * (1 - u) ** 2 * P1[1] + 3 * u * u * (1 - u) * P2[1] + u ** 3 * P3[1]) for u in np.linspace(0, 1, 30)]
        d.line(pts, fill=(80, 86, 100), width=max(3, int(6 * s)), joint="curve")
    # vanh coc (ve sau de de len noi dung)
    d.line([(x0, top), (x0, base - 20 * s)], fill=NAVY, width=max(4, int(8 * s)))
    d.line([(x1, top), (x1, base - 20 * s)], fill=NAVY, width=max(4, int(8 * s)))
    d.arc([x0, base - 44 * s, x0 + 44 * s, base], 90, 180, fill=NAVY, width=max(4, int(8 * s)))
    d.arc([x1 - 44 * s, base - 44 * s, x1, base], 0, 90, fill=NAVY, width=max(4, int(8 * s)))
    d.line([(x0 + 20 * s, base), (x1 - 20 * s, base)], fill=NAVY, width=max(4, int(8 * s)))
    # bep dien: luon do (giu mot muc)
    glow = 0.75 + 0.25 * math.sin(t * 5)
    d.rounded_rectangle([x0 - 40 * s, base + 4 * s, x1 + 40 * s, base + 24 * s], radius=int(8 * s), fill=mix(ORANGE, RED, glow))
    d.rounded_rectangle([x0 - 50 * s, base + 24 * s, x1 + 50 * s, base + 84 * s], radius=int(14 * s), fill=NAVY)
    dot(d, x1 + 10 * s, base + 54 * s, 14 * s, (60, 66, 92), outline=GRAY)
    dot(d, x0 + 10 * s, base + 54 * s, 8 * s, mix(ORANGE, RED, glow))

# ---------------- do thi T - t ----------------
YLO, YHI = -30, 125
def plot(d, box, tau, xmax, t, hl=0.0, show_pen=True):
    x0, ytop, x1, y0 = box
    X = lambda m: x0 + m / xmax * (x1 - x0); Y = lambda T: y0 - (T - YLO) / (YHI - YLO) * (y0 - ytop)
    for T in (0, 50, 100):
        dashed(d, (x0, Y(T)), (x1, Y(T)), LIGHT, 3) if T == 50 else d.line([(x0, Y(T)), (x1, Y(T))], fill=LIGHT, width=3)
        text(d, (x0 - 16, Y(T)), str(T), 34, MUTED, bold=False, anchor="rm")
    d.line([(x0, y0), (x1 + 10, y0)], fill=NAVY, width=5); d.line([(x0, y0), (x0, ytop - 10)], fill=NAVY, width=5)
    d.polygon([(x1 + 26, y0), (x1 + 8, y0 - 10), (x1 + 8, y0 + 10)], fill=NAVY)
    d.polygon([(x0, ytop - 26), (x0 - 10, ytop - 8), (x0 + 10, ytop - 8)], fill=NAVY)
    text(d, (x0 + 22, ytop - 6), "T (°C)", 34, INK, anchor="lm")
    text(d, (x1 + 20, y0 + 50), "t (phút)", 34, INK, anchor="rm")
    am = clamp((20 - xmax) / 6)
    for m in range(0, int(xmax) + 1):
        if m % 5 == 0:
            d.line([(X(m), y0), (X(m), y0 + 12)], fill=NAVY, width=4)
            if X(m) < x1 - 150 or m == 0: text(d, (X(m), y0 + 34), str(m), 32, MUTED, bold=False)
        elif am > 0:
            d.line([(X(m), y0), (X(m), y0 + 8)], fill=A(NAVY, am), width=3)
    hls = hl if isinstance(hl, tuple) else (hl, hl)
    for (a, b, T), h in zip(((1, 4, 0), (10, 35, 100)), hls):
        if h > 0: d.rounded_rectangle([X(a) - 18, Y(T) - 20, X(b) + 18, Y(T) + 20], radius=20, fill=A((187, 247, 208), h), outline=A(GREEN, h), width=4)
    if tau > 0:
        ms = np.linspace(0, tau, max(2, int(tau * 30)))
        d.line([(X(m), Y(Tline(m))) for m in ms], fill=BLUE, width=7, joint="curve")
    for r in ROWS:
        if r[0] <= tau + 1e-6:
            k = back(clamp((tau - r[0]) / 0.5) if tau < 34.99 else 1.0)
            dot(d, X(r[0]), Y(r[1]), 10 * k + 0.1, ORANGE, outline=WHITE)
    if show_pen and 0 < tau < 34.99:
        dot(d, X(tau), Y(Tline(tau)), 13, RED, outline=WHITE)
    return X, Y

XMAX = 38   # truc t co dinh tu dau

# ---------------- canh 1: Du doan ----------------
OPTS = [("A", [(0, .06), (1, .94)]),
        ("B", [(0, .06), (.33, .5), (.62, .5), (1, .94)]),
        ("C", [(0, .06), (.06, .24), (.22, .24), (.42, .78), (1, .78)]),
        ("D", [(x, .06 + .88 * (1 - math.exp(-3.2 * x)) / (1 - math.exp(-3.2))) for x in np.linspace(0, 1, 24)])]

def s_hook(img, d, t, sc):
    beaker(d, t, 0.0, 330, 640, 0.95)
    card(d, (600, 300, 1010, 520), fill=WHITE, outline=NAVY, w=4)
    text(d, (805, 350), "Nhiệt độ đọc", 34, MUTED, bold=False)
    text(d, (805, 445), "−6,0 °C", 80, BLUE)
    a0 = appear(t, 0.5)
    pill(d, 805, 575, "0,20 kg nước đá", 34, INK, (232, 226, 214), a0)
    a = appear(t, sc["M"][1] - 0.2, 0.5)
    if a <= 0: return
    card(d, (50, 760, 1030, 1610), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, 815, "DỰ ĐOÁN", 36, WHITE, PURPLE, a)
    text(d, (W / 2, 892), "Đồ thị T theo t có dạng nào?", 46, INK, alpha=a)
    for i, (lab, pts) in enumerate(OPTS):
        k = appear(t, sc["M"][1] + 0.15 * i, 0.4)
        bx = 90 + (i % 2) * 460; by = 950 + (i // 2) * 315
        card(d, (bx, by, bx + 440, by + 290), fill=A((247, 248, 252), k), outline=A(NAVY, k), r=24, w=4)
        text(d, (bx + 40, by + 44), lab, 44, NAVY, alpha=k)
        gx0, gy0, gx1, gy1 = bx + 90, by + 250, bx + 410, by + 40       # truc nho
        d.line([(gx0, gy1), (gx0, gy0), (gx1, gy0)], fill=A(MUTED, k), width=4)
        text(d, (gx0 - 10, gy1 + 4), "T", 28, MUTED, anchor="rm", alpha=k)
        text(d, (gx1, gy0 + 22), "t", 28, MUTED, anchor="rm", alpha=k)
        P = [(gx0 + 10 + px * (gx1 - gx0 - 20), gy0 - 10 - py * (gy0 - gy1 - 20)) for px, py in pts]
        d.line(P, fill=A(NAVY, k), width=7, joint="curve")
    # thanh thoi gian "ngung lai chon"
    tc = sc["M"][1] + 0.8; tend = sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, 1580, 940, 1592], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, 1580, 140 + 800 * p, 1592], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
def tau_of(t, sc):
    M = sc["M"]
    return float(np.interp(t, [M[0] + 0.5, M[1], M[2], M[3], M[4], sc["T"] - 0.7], [0, 0.95, 4.2, 10, 20, 35]))

def s_do(img, d, t, sc):
    tau = max(0.0, tau_of(t, sc))
    beaker(d, t, tau, 300, 800, 1.0, probe_to=(620, 640))
    text(d, (300, 912), "bếp giữ một mức suốt thí nghiệm", 32, MUTED, bold=False)
    # o doc
    card(d, (600, 300, 1020, 860), fill=WHITE, outline=NAVY, w=4)
    blink = 0.65 + 0.35 * math.sin(t * 6)
    wdt = tw(d, "TUA NHANH", F(32)) + 90; cxp = 810
    card(d, (cxp - wdt / 2, 322, cxp + wdt / 2, 378), fill=ORANGE, r=28)
    for j in range(2):
        tx = cxp - wdt / 2 + 22 + j * 16
        d.polygon([(tx, 336), (tx, 364), (tx + 16, 350)], fill=A(WHITE, blink))
    text(d, (cxp + 22, 350), "TUA NHANH", 32, WHITE)
    text(d, (810, 430), "Đồng hồ", 34, MUTED, bold=False)
    text(d, (810, 500), f"phút {int(tau + 1e-6)}", 64, INK)
    d.line([(640, 560), (980, 560)], fill=LIGHT, width=3)
    rm, rv = reading(tau)
    text(d, (810, 610), "Nhiệt kế đọc", 34, MUTED, bold=False)
    fl = 1 - clamp((tau - rm) / 0.6) if rm > 0 else 0
    col = BLUE if rv < 5 else (RED if rv > 90 else ORANGE)
    if fl > 0: card(d, (630, 650, 990, 760), fill=A((255, 237, 213), fl), r=20)
    text(d, (810, 705), vn(rv) + " °C", 76, col)
    text(d, (810, 785 if rm >= 11 else 805), f"số ghi ở phút {rm}", 32, MUTED, bold=False)
    if rm >= 11: text(d, (810, 828), "sau đó 5 phút ghi 1 lần", 32, MUTED, bold=False)
    # do thi
    card(d, (40, 960, 1040, 1610), fill=WHITE, outline=LIGHT, w=3)
    plot(d, (160, 1010, 960, 1515), tau, XMAX, t)

# ---------------- canh 3: Vi sao nam ngang ----------------
GR = [(c, r) for r in range(4) for c in range(5)]
BONDS = [(i, j) for i, (c, r) in enumerate(GR) for j, (c2, r2) in enumerate(GR) if (c2 == c + 1 and r2 == r) or (r2 == r + 1 and c2 == c)]
R2 = random.Random(11); BT = [R2.uniform(0.05, 0.95) for _ in BONDS]
PH = [(R2.uniform(0, 6.3), R2.uniform(0, 6.3), R2.uniform(0.5, 1.0)) for _ in GR]

def particles(d, box, t, p):
    x0, y0, x1, y1 = box; sx = (x1 - x0 - 120) / 4; sy = (y1 - y0 - 120) / 3
    pos = []
    for i, (c, r) in enumerate(GR):
        a, b, sp = PH[i]
        free = clamp(p * 1.3 - 0.15)
        jx = 6 * math.sin(t * 14 * sp + a); jy = 6 * math.cos(t * 13 * sp + b)    # rung: bien do khong doi
        dx = free * 26 * math.sin(t * 1.1 * sp + a); dy = free * 22 * math.cos(t * 0.9 * sp + b)
        pos.append((x0 + 60 + c * sx + jx + dx, y0 + 60 + r * sy + jy + dy))
    for (i, j), bt in zip(BONDS, BT):
        al = 1 - clamp((p - bt) / 0.08)
        if al > 0: d.line([pos[i], pos[j]], fill=A(PURPLE, 0.8 * al), width=6)
    for (x, y) in pos: dot(d, x, y, 17, BLUE, outline=WHITE)

def bar(d, x, y, wdt, frac, color):
    d.rounded_rectangle([x, y - 13, x + wdt, y + 13], radius=13, fill=LIGHT)
    if frac > 0.01: d.rounded_rectangle([x, y - 13, x + wdt * frac, y + 13], radius=13, fill=color)

def boil_panel(d, box, t):
    # luc soi: phan tu trong nuoc chay tu do, mot so thoat qua mat nuoc thanh hoi
    x0, y0, x1, y1 = box; sy = y0 + 190
    d.rounded_rectangle([x0 + 12, sy, x1 - 12, y1 - 12], radius=18, fill=(214, 230, 250))
    d.line([(x0 + 16, sy), (x1 - 16, sy)], fill=(120, 170, 225), width=5)
    for i, (a, b, sp) in enumerate(PH[:14]):
        x = refl(x0 + 50 + a * 60 + t * 70 * sp, x0 + 40, x1 - 40)
        y = refl(sy + 40 + b * 40 + t * 55 * sp, sy + 36, y1 - 40)
        dot(d, x, y, 17, BLUE, outline=WHITE)
    for i in range(4):
        u = (t * 0.45 + i / 4) % 1
        x = x0 + 90 + i * 100 + 18 * math.sin(t * 2 + i)
        y = sy - 10 - u * (sy - y0 - 40)
        al = clamp((1 - u) / 0.3)
        dot(d, x, y, 17, A(BLUE, al), outline=A(WHITE, al))
        if u < 0.5: arrow(d, (x, y - 26), (x, y - 70), A(ORANGE, al * (1 - u * 2)), w=5, head=14)

def s_graph(img, d, t, sc):
    M = sc["M"]; cur = cur_cap(sc, t)
    card(d, (40, 245, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    a0 = appear(t, M[0] + 0.2, 0.6)
    b2 = appear(t, M[2] - 0.1, 0.4)
    h0 = a0 * (1 - 0.75 * b2); h1 = a0 * (1 - 0.75 * (appear(t, M[1] - 0.1, 0.4) - b2))
    X, Y = plot(d, (160, 300, 960, 870), 35, XMAX, t, hl=(h0, h1), show_pen=False)
    text(d, ((X(10) + X(35)) / 2, Y(100) - 52), "100 °C · 27 phút", 36, GREEN, alpha=max(0.3, h1))
    text(d, (X(1) - 10, Y(0) + 56), "0 °C · 4 phút", 36, GREEN, anchor="lm", alpha=max(0.3, h0))
    # dap an C + o phong to doan da nong len -6 -> 0 °C
    ka = appear(t, M[0] + 0.1, 0.5)
    if ka > 0:
        pill(d, 755, 470, "ĐÁP ÁN C", 36, WHITE, NAVY, ka)
        P = [(885 + px * 105, 495 - py * 55) for px, py in OPTS[2][1]]
        d.line(P, fill=A(NAVY, ka), width=6, joint="curve")
        bx0, by0, bx1, by1 = 640, 540, 1010, 840
        card(d, (bx0, by0, bx1, by1), fill=A((247, 248, 252), ka), outline=A(LIGHT, ka), r=20, w=3)
        text(d, ((bx0 + bx1) / 2, by0 + 34), "Phóng to", 36, INK, alpha=ka)
        ix = lambda m: bx0 + 70 + m / 2 * (bx1 - bx0 - 110); iy = lambda T: by1 - 50 - (T + 8) / 10 * (by1 - by0 - 130)
        dashed(d, (ix(0), iy(0)), (ix(2), iy(0)), A(GREEN, ka), 3)
        text(d, (ix(0) - 14, iy(0)), "0", 32, GREEN, anchor="rm", alpha=ka)
        text(d, (ix(0) - 14, iy(-6)), "−6", 32, MUTED, bold=False, anchor="rm", alpha=ka)
        d.line([(ix(m), iy(Tline(m))) for m in np.linspace(0, 2, 40)], fill=A(BLUE, ka), width=6, joint="curve")
        for m in (0, 1, 2): dot(d, ix(m), iy(Tline(m)), 9, A(ORANGE, ka), outline=A(WHITE, ka))
        d.rectangle([X(0) - 10, Y(2) - 8, X(2) + 10, Y(-8) + 6], outline=A(NAVY, ka), width=3)
        dashed(d, (X(2) + 10, Y(-3)), (bx0, iy(-3)), A(NAVY, 0.6 * ka), 3, 10, 8)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    soi = cur >= 2
    card(d, (40, 990, 1040, 1610), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    text(d, (W / 2, 1036), "Nước sôi" if soi else "Đá tan", 40, MUTED, alpha=a)
    box = (70, 1075, 540, 1585)
    card(d, box, fill=A((244, 241, 255), a), r=24)
    if soi: boil_panel(d, box, t)
    else: particles(d, box, t, clamp((t - M[1]) / (M[2] - M[1] - 0.3)))
    # cot phai: 3 hang
    rx = 580
    text(d, (rx, 1110), "Nhiệt từ bếp", 36, INK, anchor="lm", alpha=a)
    for j in range(5):
        u = ((t * 0.8 + j / 5) % 1)
        xx = rx + 10 + u * 380
        al = a * min(1, u / 0.15, (1 - u) / 0.15)
        d.line([(xx, 1150), (xx + 18, 1166), (xx, 1182)], fill=A(ORANGE, al), width=7)
    a2 = appear(t, (M[2] if soi else M[1]) + 0.4, 0.5)
    if soi:
        text(d, (rx, 1290), "Phân tử thoát ra", 40, INK, anchor="lm", alpha=a2)
        text(d, (rx, 1338), "thành hơi", 40, INK, anchor="lm", alpha=a2)
    else:
        text(d, (rx, 1290), "Liên kết giữa phân tử", 40, INK, anchor="lm", alpha=a2)
        if a2 > 0: bar(d, rx, 1342, 400, 1 - clamp((t - M[1]) / (M[2] - M[1] - 0.3)), PURPLE)
        text(d, (rx, 1392), "bị phá dần", 40, PURPLE, anchor="lm", alpha=a2)
    a3 = appear(t, (M[2] if soi else M[1]) + 1.2, 0.5)
    text(d, (rx, 1466), "Động năng", 40, INK, anchor="lm", alpha=a3)
    if a3 > 0: bar(d, rx, 1518, 400, 0.45 if not soi else 0.8, BLUE)
    text(d, (rx, 1566), "không tăng", 40, GREEN, anchor="lm", alpha=a3)

# ---------------- canh 4: Gioi han + bay ----------------
def s_limit(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 245, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 296), "Phóng to", 40, INK)
    x0, x1, yt, yb = 200, 960, 370, 790
    X = lambda m: x0 + (m - 0.3) / 4.4 * (x1 - x0); Y = lambda T: yb - (T + 1) / 2 * (yb - yt)
    for T, lab in ((1, "1"), (0.5, "0,5"), (0, "0"), (-0.5, "−0,5"), (-1, "−1")):
        if T != 0: d.line([(x0, Y(T)), (x1, Y(T))], fill=LIGHT, width=2)
        text(d, (x0 - 16, Y(T)), lab, 32, MUTED, bold=False, anchor="rm")
    d.line([(x0, yt - 10), (x0, yb)], fill=NAVY, width=5)
    text(d, (x0 + 18, yt - 22), "T (°C)", 32, INK, anchor="lm")
    dashed(d, (x0, Y(0)), (x1, Y(0)), GREEN, 5, 22, 12)
    text(d, (x0 + 18, Y(0) + 30), "0 °C", 34, GREEN, anchor="lm")
    for m in (1, 2, 3, 4):
        text(d, (X(m), yb + 34), f"{m}", 32, MUTED, bold=False)
    for i, m in enumerate((1, 2, 3, 4)):
        v = dict(ROWS)[m]; k = appear(t, M[0] + 0.25 * i, 0.4)
        if k <= 0: continue
        e = 0.5 * ease((t - M[0] - 0.8 - 0.2 * i) / 0.5)
        if e > 0:
            d.line([(X(m), Y(v - e)), (X(m), Y(v + e))], fill=NAVY, width=5)
            for yy in (Y(v - e), Y(v + e)): d.line([(X(m) - 18, yy), (X(m) + 18, yy)], fill=NAVY, width=5)
        dot(d, X(m), Y(v), 13 * k, ORANGE, outline=WHITE)
        text(d, (X(m) + 26, Y(v) - 4), vn(v), 32, ORANGE, anchor="lm", alpha=k)
    ka = appear(t, M[0] + 1.6, 0.5)
    text(d, (W / 2, 870), "Thanh dọc: ±0,5 °C", 40, NAVY, alpha=ka)
    # bay
    kb = appear(t, M[1] - 0.15, 0.5)
    if kb <= 0: return
    y0 = 1000 + (1 - back((t - M[1] + 0.15) / 0.5)) * 40
    card(d, (40, y0, 1040, y0 + 600), fill=WHITE, outline=RED, w=6)
    pill(d, W / 2, y0 + 62, "BẪY", 38, WHITE, RED)
    q = "“Nằm ngang = bếp tắt”"; ls = wrap(d, q, F(44), 860)
    ks = clamp((t - M[1] - 0.7) / 0.4)
    for j, l in enumerate(ls):
        yy = y0 + 170 + (j - (len(ls) - 1) / 2) * 54; lw = tw(d, l, F(44))
        text(d, (W / 2, yy), l, 44, mix(INK, GRAY, ks))
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.8), width=4)
    kc = appear(t, M[1] + 1.1, 0.5)
    ctext(d, y0 + 330, "Sai: bếp vẫn bật suốt.", 50, RED, alpha=kc)
    ctext(d, y0 + 450, "Nhiệt dùng để phá liên kết.", 46, INK, maxw=860, alpha=appear(t, M[1] + 1.6, 0.5))

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 360, "Nhiệt vào → T đứng yên", 52, GREEN, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 620, 1040, 1600), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 682, "THỬ NGHĨ", 38, WHITE, ORANGE, k1)
    for j, (lab, mins, col) in enumerate((("đá tan", 4, BLUE), ("sôi tới cạn", 27, RED))):
        y = 820 + j * 130; g = ease((t - M[0] - 0.3 - 0.3 * j) / 0.8)
        text(d, (100, y), lab, 38, INK, anchor="lm", alpha=k1)
        wmax = 430 * mins / 27
        d.rounded_rectangle([340, y - 24, 340 + max(48, wmax * g), y + 24], radius=24, fill=A(col, k1))
        text(d, (340 + max(48, wmax * g) + 20, y), f"{mins} phút", 38, col, anchor="lm", alpha=g)
    ctext(d, 1130, "Vì sao sôi lâu gấp gần 7 lần?", 48, INK, maxw=880, alpha=appear(t, M[0] + 1.0, 0.5))
    kh = appear(t, M[0] + 2.2, 0.5)
    card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1445, "λ = 334 · L = 2 260 kJ/kg", 46, ORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}; out = []
    h = sc["hook"]; out += [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.3, "ding")]
    do = sc["do"]; t = do["t0"] + do["M"][0] + 0.5
    while t < do["t0"] + do["T"] - 0.7: out.append((t, "tick")); t += 0.5
    out += [(do["t0"] + do["M"][1], "tap"), (do["t0"] + do["M"][3], "tap")]
    out += [(sc["graph"]["t0"] + sc["graph"]["M"][0] + 0.1, "ding"), (sc["limit"]["t0"] + sc["limit"]["M"][1], "buzz"),
            (sc["end"]["t0"] + sc["end"]["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l12-chuyenthe-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Sự chuyển thể · thachlab.id.vn", cues=_cues, scenes=[
 dict(key="hook", title="Đun nước đá, ghi nhiệt độ", draw=s_hook, tail=0.6, caps=[
   ("Nước đá −6 °C, bếp giữ một mức.", 2.9),
   ("Dự đoán: đồ thị T theo t dạng nào?", 3.4)]),
 dict(key="do", title="Mỗi phút đọc nhiệt kế", draw=s_do, tail=0.8, caps=[
   ("Bật bếp, khuấy, ghi mỗi phút.", 2.4),
   ("Phút 1–4: đứng ở 0 °C.", 3.0),
   ("Đá tan hết: tăng đều.", 2.8),
   ("Từ phút 10: đứng ở 100 °C.", 2.6),
   ("Nước cạn dần.", 2.4)]),
 dict(key="graph", title="Vì sao có đoạn nằm ngang?", draw=s_graph, tail=0.6, caps=[
   ("Lên – ngang – lên – ngang.", 3.4),
   ("Đá tan: nhiệt phá liên kết.", 3.6),
   ("Đang sôi: phân tử thoát ra.", 3.6)]),
 dict(key="limit", title="Giới hạn và cái bẫy", draw=s_limit, tail=0.7, caps=[
   ("0,2–0,3 °C vẫn khớp 0 °C.", 3.4),
   ("Bẫy hay gặp.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Nhìn hai thanh, nghĩ vì sao.", 5.0)]),
])
