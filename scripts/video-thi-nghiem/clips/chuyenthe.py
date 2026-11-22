# Clip: tn-l12-chuyenthe-01 - Dun nuoc da, moi phut ghi nhiet do mot lan
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-chuyenthe-01.json -> so_lieu_mau (khong them diem); sai so +-0,5 °C
#   (tham_so T_do), ~4 phut / ~27 phut (ket_qua_ky_vong), nuoc can o phut 36.
# Ban 4 (21/11/2026, viec 4 lo 20 KE-HOACH-CAI-TIEN-CLIP): dung lai theo cong --do-chu moi (chu than canh >= 56 px,
#   <= 180 tu/phut moi canh, khoi chu cach >= 2,5 s, khong chu xam cho dieu quan trong).
#   Quan niem sai can danh: do thi T-t doc thang (nhan nhiet thi T phai tang).
#   Du doan (v2 sau kiem-code): nuoc da toi 100 °C, bep van bat -> nhiet ke sau do chi? (khung web A-D; dap an C:
#     dung gan 100 °C toi khi can). Cau mo bai da hoi luc da dang tan (0 °C) nen khong hoi lai doan do; khac Cau 2-6.
#     Clip khong ve nut A-D / nhan "DAP AN" (K10), dong "Dung lai, tu doan", dem nguoc 5 cham r 40.
#   Bay v2: nhip 1 chi truc + cau hoi; nhip 2 moi ve hai duong, SAI + chot sau 1,8 s. Goi y cau chot trung tinh.
#   Canh: hook -> do (tua nhanh, ve dan do thi, +-0,5 °C canh so doc) -> rutra (DAP AN D + co che tan / soi, moi co che
#     mot hinh) -> gioi (chua noi duoc gi) -> bay (2 nhip: "Q da nhan" doc thang canh "T" nam ngang, cung truc thoi gian;
#     chot "Dang chuyen the: T khong doi") -> end THU NGHI: gap doi da, cung bep -> doan ngang dau doi sao?
#     (dap an: van 0 °C, dai gap doi; khong hien tren man; goi y Q tan = m·λ hien tre).
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
DARK_OR = (181, 71, 8)                                         # cam dam: chu cam tren nen sang >= 4,5:1
DARK_GR = (21, 128, 61)

ICE = [(-95, 0), (-15, 0), (65, 0), (-60, 1), (25, 1), (-20, 2), (90, 1)]   # (dx, tang) vien da
R = random.Random(5)
BUB = [(R.uniform(-0.42, 0.42), R.random(), R.uniform(0.8, 1.3), R.uniform(5, 10)) for _ in range(16)]

def dashed(d, p1, p2, color, w=3, dash=16, gap=12):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

def pill(d, cx, cy, s, size, fg, bg, alpha=1.0, padx=30):
    wdt = tw(d, s, F(size)) + 2 * padx
    card(d, (cx - wdt / 2, cy - size * 0.78, cx + wdt / 2, cy + size * 0.78), fill=A(bg, alpha), r=int(size * 0.78))
    text(d, (cx, cy), s, size, fg, alpha=alpha)
    return wdt

def stove(d, t, x0, x1, base, s=1.0):
    glow = 0.75 + 0.25 * math.sin(t * 5)
    d.rounded_rectangle([x0 - 40 * s, base + 4 * s, x1 + 40 * s, base + 24 * s], radius=int(8 * s), fill=mix(ORANGE, RED, glow))
    d.rounded_rectangle([x0 - 50 * s, base + 24 * s, x1 + 50 * s, base + 84 * s], radius=int(14 * s), fill=NAVY)
    dot(d, x1 + 10 * s, base + 54 * s, 14 * s, (60, 66, 92), outline=GRAY)
    dot(d, x0 + 10 * s, base + 54 * s, 8 * s, mix(ORANGE, RED, glow))

def rim(d, x0, x1, top, base, s):
    d.line([(x0, top), (x0, base - 20 * s)], fill=NAVY, width=max(4, int(8 * s)))
    d.line([(x1, top), (x1, base - 20 * s)], fill=NAVY, width=max(4, int(8 * s)))
    d.arc([x0, base - 44 * s, x0 + 44 * s, base], 90, 180, fill=NAVY, width=max(4, int(8 * s)))
    d.arc([x1 - 44 * s, base - 44 * s, x1, base], 0, 90, fill=NAVY, width=max(4, int(8 * s)))
    d.line([(x0 + 20 * s, base), (x1 - 20 * s, base)], fill=NAVY, width=max(4, int(8 * s)))

def cube(d, ix, ytop, sz, s, al=1.0, f=1.0):
    d.rounded_rectangle([ix, ytop, ix + sz, ytop + sz], radius=int(12 * s * max(0.4, f)),
                        fill=A((248, 252, 255), al), outline=A((110, 160, 215), al), width=max(2, int(4 * s)))
    d.line([(ix + sz * 0.2, ytop + sz * 0.25), (ix + sz * 0.45, ytop + sz * 0.25)], fill=A(WHITE, al), width=max(2, int(5 * s)))

# ---------------- coc + bep + dau do ----------------
def beaker(d, t, tau, cx, base, s=1.0):
    w, h = 330 * s, 360 * s; x0, x1, top = cx - w / 2, cx + w / 2, base - h
    inner = h - 14 * s
    f_ice = 1 - clamp((tau - 0.15) / 3.98)                     # da con lai (mo hinh: tan het o 248 s)
    if tau < 10: lvl = 0.62 * (1 - f_ice)
    else: lvl = 0.62 * (1 - clamp((tau - 10) / 26.0) * 0.97)  # nuoc can dan khi soi, can o ~phut 36
    wl = base - 8 * s - inner * lvl
    Tc = Tline(tau)
    wcol = mix((170, 210, 250), (196, 214, 236), clamp(Tc / 100))
    d.rounded_rectangle([x0, top, x1, base], radius=int(22 * s), fill=(240, 246, 252))
    if lvl > 0.005:
        d.rounded_rectangle([x0 + 8 * s, wl, x1 - 8 * s, base - 8 * s], radius=int(16 * s), fill=wcol)
        d.line([(x0 + 10 * s, wl), (x1 - 10 * s, wl)], fill=(120, 170, 225), width=max(2, int(4 * s)))
    if f_ice > 0.02:
        sz0 = 78 * s; sz = sz0 * f_ice ** 0.55; al = clamp(f_ice / 0.12)
        for dx, lay in ICE:
            stack_top = base - 10 * s - sz0 * (lay + 1) * 0.92 + (sz0 - sz)
            ytop = min(stack_top, wl - 0.15 * sz) if lvl > 0.02 else stack_top
            cube(d, cx + dx * s - sz / 2, ytop, sz, s, al, f_ice)
    boil = clamp((tau - 9.1) / 0.6) * (1 if lvl > 0.08 else 0)
    if boil > 0:
        depth = base - 8 * s - wl
        for (u, ph, sp, r) in BUB:
            yy = base - 14 * s - ((t * 0.9 * sp + ph) % 1) * max(10, depth - 20 * s)
            d.ellipse([cx + u * w - r * s, yy - r * s, cx + u * w + r * s, yy + r * s], outline=A(WHITE, boil), width=max(2, int(3 * s)))
        for i in range(3):
            sx = cx + (-80 + i * 80) * s
            pts = [(sx + 16 * s * math.sin(t * 2.6 + i * 1.7 + k * 0.8), top - 20 * s - k * 26 * s) for k in range(5)]
            d.line(pts, fill=A(GRAY, 0.45 * boil), width=max(3, int(8 * s)), joint="curve")
    sw = math.sin(t * 3.2) * 18 * s                            # que khuay (lac nhe)
    d.line([(cx - 120 * s + sw, top - 60 * s), (cx - 30 * s + sw * 0.4, base - 40 * s)], fill=(176, 120, 70), width=max(4, int(12 * s)))
    px = cx + 105 * s                                          # dau do nhiet ke: khong cham day
    d.line([(px, top - 70 * s), (px, base - 75 * s)], fill=(120, 126, 140), width=max(4, int(12 * s)))
    dot(d, px, base - 72 * s, 9 * s, NAVY)
    rim(d, x0, x1, top, base, s)
    stove(d, t, x0, x1, base, s)

# ---------------- do thi T - t (chu truc 56 px) ----------------
YLO, YHI = -30, 125
XMAX = 38   # truc t co dinh tu dau
def plot(d, box, tau, t, hl=(0.0, 0.0), show_pen=True, alpha=1.0):
    x0, ytop, x1, y0 = box
    X = lambda m: x0 + m / XMAX * (x1 - x0); Y = lambda T: y0 - (T - YLO) / (YHI - YLO) * (y0 - ytop)
    for T in (0, 100):
        d.line([(x0, Y(T)), (x1, Y(T))], fill=A(LIGHT, alpha), width=3)
        text(d, (x0 - 16, Y(T)), str(T), 56, INK, anchor="rm", alpha=alpha)
    d.line([(x0, y0), (x1 + 10, y0)], fill=A(NAVY, alpha), width=5); d.line([(x0, y0), (x0, ytop - 10)], fill=A(NAVY, alpha), width=5)
    d.polygon([(x1 + 26, y0), (x1 + 8, y0 - 10), (x1 + 8, y0 + 10)], fill=A(NAVY, alpha))
    d.polygon([(x0, ytop - 26), (x0 - 10, ytop - 8), (x0 + 10, ytop - 8)], fill=A(NAVY, alpha))
    text(d, (x0 + 24, ytop - 4), "T (°C)", 56, INK, anchor="lm", alpha=alpha)
    text(d, (x1 + 26, y0 - 44), "t (phút)", 56, INK, anchor="rm", alpha=alpha)
    for m in (0, 10, 20, 30):
        d.line([(X(m), y0), (X(m), y0 + 12)], fill=A(NAVY, alpha), width=4)
        text(d, (X(m), y0 + 46), str(m), 56, INK, alpha=alpha)
    for (a, b, T), h in zip(((1, 4, 0), (10, 35, 100)), hl):
        if h > 0: d.rounded_rectangle([X(a) - 18, Y(T) - 22, X(b) + 18, Y(T) + 22], radius=22, fill=A((187, 247, 208), h), outline=A(GREEN, h), width=5)
    if tau > 0:
        ms = np.linspace(0, tau, max(2, int(tau * 30)))
        d.line([(X(m), Y(Tline(m))) for m in ms], fill=A(BLUE, alpha), width=8, joint="curve")
    for r in ROWS:
        if r[0] <= tau + 1e-6:
            k = back(clamp((tau - r[0]) / 0.5) if tau < 34.99 else 1.0)
            dot(d, X(r[0]), Y(r[1]), 11 * k + 0.1, A(ORANGE, alpha), outline=A(WHITE, alpha))
    if show_pen and 0 < tau < 34.99:
        dot(d, X(tau), Y(Tline(tau)), 14, RED, outline=WHITE)
    return X, Y

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    beaker(d, t, 0.0, 300, 700, 1.0)
    card(d, (600, 300, 1030, 560), fill=WHITE, outline=NAVY, w=4)
    text(d, (815, 430), "−6,0 °C", 96, BLUE)
    pill(d, 815, 640, "0,20 kg đá", 56, INK, (232, 226, 214))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1000 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 590), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)      # K10: khong ve nut A-D
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", 56, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 195), "Đun đá −6 °C tới khi nước 100 °C.", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 295), "Bếp vẫn bật. Sau đó nhiệt kế?", 58, INK, alpha=a)
    # dem nguoc 5 cham (r 40 = 80 px), moi cham tat sau ~1 s
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    n_off = 0 if t < tc else min(5, int((t - tc) / ((tend - tc) / 5)) + 1)
    for j in range(5):
        dot(d, W / 2 + (j - 2) * 140, y0 + 455, 40, A(LIGHT, a) if j >= 5 - n_off else A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
def tau_of(t, sc):
    M = sc["M"]
    return float(np.interp(t, [M[0] + 0.3, M[1], M[2], M[3], sc["T"] - 0.3], [0, 1.0, 4.3, 10, 35]))

def s_do(img, d, t, sc):
    tau = max(0.0, tau_of(t, sc))
    beaker(d, t, tau, 290, 660, 0.85)
    card(d, (560, 260, 1030, 740), fill=WHITE, outline=NAVY, w=4)
    blink = 0.65 + 0.35 * math.sin(t * 6)
    wdt = tw(d, "TUA NHANH", F(56)) + 100; cxp = 795
    card(d, (cxp - wdt / 2, 290, cxp + wdt / 2, 370), fill=ORANGE, r=40)
    for j in range(2):
        tx = cxp - wdt / 2 + 22 + j * 18
        d.polygon([(tx, 312), (tx, 348), (tx + 20, 330)], fill=A(WHITE, blink))
    text(d, (cxp + 26, 330), "TUA NHANH", 56, WHITE)
    rm, rv = reading(tau)
    text(d, (795, 445), f"phút {rm}", 66, INK)
    fl = 1 - clamp((tau - rm) / 0.6) if rm > 0 else 0
    col = BLUE if rv < 5 else (RED if rv > 90 else DARK_OR)
    if fl > 0: card(d, (585, 495, 1005, 615), fill=A((255, 237, 213), fl), r=24)
    text(d, (795, 555), vn(rv) + " °C", 86, col)
    ke = appear(tau, 0.95, 0.15) * (1 - appear(tau, 4.6, 0.3))  # sai so canh so doc, chi luc dung o ~0 °C
    if ke > 0: text(d, (795, 680), "sai số ±0,5 °C", 56, NAVY, alpha=ke)
    card(d, (40, 770, 1040, 1600), fill=WHITE, outline=LIGHT, w=3)
    plot(d, (210, 860, 960, 1470), tau, t)

# ---------------- canh 3: Dap an + vi sao nam ngang ----------------
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
        if al > 0: d.line([pos[i], pos[j]], fill=A(PURPLE, 0.85 * al), width=7)
    for (x, y) in pos: dot(d, x, y, 18, BLUE, outline=WHITE)

def boil_panel(d, box, t):
    # luc soi: phan tu trong nuoc chay tu do, mot so thoat qua mat nuoc thanh hoi
    x0, y0, x1, y1 = box; sy = y0 + 190
    d.rounded_rectangle([x0 + 12, sy, x1 - 12, y1 - 12], radius=18, fill=(214, 230, 250))
    d.line([(x0 + 16, sy), (x1 - 16, sy)], fill=(120, 170, 225), width=5)
    P = [[refl(x0 + 50 + a * 60 + t * 70 * sp, x0 + 40, x1 - 40), refl(sy + 40 + b * 40 + t * 55 * sp, sy + 36, y1 - 40)]
         for (a, b, sp) in PH[:14]]
    for _ in range(6):                                         # tach cac cham chong nhau (khoang cach >= 44 px)
        for i in range(len(P)):
            for j in range(i + 1, len(P)):
                dx, dy = P[j][0] - P[i][0], P[j][1] - P[i][1]; dd = math.hypot(dx, dy) or 0.01
                if dd < 44:
                    k = (44 - dd) / 2 / dd
                    P[i][0] -= dx * k; P[i][1] -= dy * k; P[j][0] += dx * k; P[j][1] += dy * k
        for q in P: q[0] = clamp(q[0], x0 + 40, x1 - 40); q[1] = clamp(q[1], sy + 36, y1 - 40)
    for x, y in P: dot(d, x, y, 18, BLUE, outline=WHITE)
    for i in range(4):
        u = (t * 0.45 + i / 4) % 1
        x = x0 + 90 + i * 100 + 18 * math.sin(t * 2 + i)
        y = sy - 10 - u * (sy - y0 - 40)
        al = clamp((1 - u) / 0.3)
        dot(d, x, y, 18, A(BLUE, al), outline=A(WHITE, al))
        if u < 0.5: arrow(d, (x, y - 26), (x, y - 70), A(ORANGE, al * (1 - u * 2)), w=5, head=14)
    text(d, (x1 - 40, y0 + 60), "hơi", 56, NAVY, anchor="rm")

def bar(d, x, y, wdt, frac, color, a=1.0):
    d.rounded_rectangle([x, y - 16, x + wdt, y + 16], radius=16, fill=A(LIGHT, a))
    if frac > 0.01: d.rounded_rectangle([x, y - 16, x + wdt * frac, y + 16], radius=16, fill=A(color, a))

def heat_in(d, t, box, a):
    """Bep duoi khung phan tu + chevron cam di len: nhiet van vao suot (khong can chu)."""
    x0, y0, x1, y1 = box
    glow = 0.75 + 0.25 * math.sin(t * 5)
    d.rounded_rectangle([x0 + 20, y1 + 8, x1 - 20, y1 + 30], radius=10, fill=A(mix(ORANGE, RED, glow), a))
    for j in range(3):
        u = (t * 0.9 + j / 3) % 1; xx = x0 + 110 + j * 125; yy = y1 - 10 - u * 70
        al = a * min(1, u / 0.2, (1 - u) / 0.2)
        d.line([(xx - 18, yy + 14), (xx, yy), (xx + 18, yy + 14)], fill=A(ORANGE, al), width=7)

def s_rutra(img, d, t, sc):
    M = sc["M"]; cur = cur_cap(sc, t)
    card(d, (40, 250, 1040, 975), fill=WHITE, outline=LIGHT, w=3)
    h_tan = appear(t, M[0] + 0.1, 0.4) * (1 - 0.7 * appear(t, M[2] - 0.1, 0.4))
    h_soi = appear(t, M[0] + 0.1, 0.4) * (1 - 0.7 * (appear(t, M[1] - 0.1, 0.4) - appear(t, M[2] - 0.1, 0.4)))
    X, Y = plot(d, (210, 340, 960, 870), 35, t, hl=(h_tan, h_soi), show_pen=False)
    ka = appear(t, M[0] + 0.1, 0.4)
    if ka > 0:
        text(d, (X(1) + 4, Y(0) + 66), "≈ 4 phút", 56, DARK_GR, anchor="lm", alpha=ka)
        text(d, ((X(10) + X(35)) / 2, Y(100) + 66), "≈ 27 phút", 56, DARK_GR, alpha=ka)
    a = appear(t, M[1] - 0.15, 0.4)
    if a <= 0: return
    soi = cur >= 2
    card(d, (40, 1000, 1040, 1600), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    box = (70, 1025, 540, 1530)
    card(d, box, fill=A((244, 241, 255), a), r=24)
    if soi: boil_panel(d, box, t)
    else: particles(d, box, t, clamp((t - M[1]) / (M[2] - M[1] - 0.3)))
    heat_in(d, t, box, a)
    rx = 580
    text(d, (rx, 1150), "Động năng TB", 56, INK, anchor="lm", alpha=a)
    bar(d, rx, 1240, 420, 0.8 if soi else 0.45, BLUE, a)
    text(d, (rx, 1330), "không đổi", 60, DARK_GR, anchor="lm", alpha=a)

# ---------------- canh 4: Chua noi duoc gi ----------------
def s_gioi(img, d, t, sc):
    k = appear(t, 0.2, 0.4); kb = appear(t, 2.2, 0.4)
    card(d, (40, 300, 1040, 1300), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    for j, s in enumerate(("• Nhiệt mất ra ngoài?", "• Áp suất khác?")):
        text(d, (110, 640 + j * 260), s, 64, INK, anchor="lm", alpha=kb)
    pul = 1 + 0.06 * math.sin(t * 4)
    text(d, (W / 2, 800), "?", int(260 * pul), NAVY, alpha=k * (1 - kb))

# ---------------- canh 5: Bay (2 nhip >= 3 s) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; k1 = appear(t, M[0] - 0.1, 0.4); k2 = appear(t, M[1] - 0.1, 0.4)
    text(d, (W / 2, 300), "“Nhận nhiệt thì T phải tăng”", 58, INK, alpha=k1)
    k3 = appear(t, M[1] + 1.8, 0.4)                             # SAI + chot sau khi hai duong ve xong
    if k3 > 0: pill(d, W / 2, 400, "SAI", 56, WHITE, RED, k3)
    card(d, (40, 460, 1040, 1300), fill=A(WHITE, k1), outline=A(RED, k1), w=5)
    p = ease((t - M[1] + 0.1) / 1.6)                            # nhip 1 chi truc + cau hoi; nhip 2 moi ve hai duong
    gx0, gx1 = 230, 880
    # do thi tren: nhiet da nhan (Q = P·τ, doc thang)
    text(d, (gx0, 520), "Nhiệt đã nhận", 56, DARK_OR, anchor="lm", alpha=k1)
    d.line([(gx0, 570), (gx0, 820)], fill=A(NAVY, k1), width=5); d.line([(gx0, 820), (gx1, 820)], fill=A(NAVY, k1), width=4)
    if p > 0: d.line([(gx0, 810), (lerp(gx0, gx1, p), lerp(810, 590, p))], fill=A(ORANGE, k1), width=9)
    # do thi duoi: nhiet do T nam ngang o 0 °C
    text(d, (gx0, 880), "T (°C)", 56, INK, anchor="lm", alpha=k1)
    d.line([(gx0, 930), (gx0, 1180)], fill=A(NAVY, k1), width=5); d.line([(gx0, 1180), (gx1, 1180)], fill=A(NAVY, k1), width=5)
    text(d, (gx0 - 16, 1090), "0", 56, INK, anchor="rm", alpha=k1)
    if k3 > 0: d.rounded_rectangle([gx0 - 6, 1066, gx1 + 6, 1114], radius=24, fill=A((187, 247, 208), k3), outline=A(GREEN, k3), width=4)
    if p > 0: d.line([(gx0, 1090), (lerp(gx0, gx1, p), 1090)], fill=A(BLUE, k1), width=9)
    kq = k1 * (1 - appear(t, M[1] - 0.1, 0.4))                  # nhip 1: dau ? nhip nhay o hai truc (hinh khong dung yen)
    if kq > 0:
        for yy in (700, 1060):
            text(d, (W / 2 + 40, yy), "?", int(130 * (1 + 0.12 * math.sin(t * 5))), NAVY, alpha=kq)
    for m, x in ((1, gx0), (4, gx1)):
        d.line([(x, 1180), (x, 1194)], fill=A(NAVY, k1), width=4)
        text(d, (x, 1236), f"phút {m}", 56, INK, alpha=k1)
    if k3 > 0:
        card(d, (40, 1330, 1040, 1590), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
        text(d, (W / 2, 1405), "Đang chuyển thể:", 60, DARK_GR, alpha=k3)
        text(d, (W / 2, 1510), "T không đổi", 66, DARK_GR, alpha=k3)

# ---------------- canh 6: THU NGHI (gap doi da) ----------------
def mini(d, t, cx, base, n_lay, lab, s=0.62):
    w, h = 330 * s, 330 * s; x0, x1, top = cx - w / 2, cx + w / 2, base - h
    d.rounded_rectangle([x0, top, x1, base], radius=int(22 * s), fill=(240, 246, 252))
    sz = 78 * s
    for lay in range(n_lay):
        for dx in (-95, -15, 65):
            cube(d, cx + dx * s - sz / 2, base - 10 * s - sz * (lay + 1) * 0.95, sz, s)
    sw = math.sin(t * 3.2 + cx) * 14 * s
    d.line([(cx - 110 * s + sw, top - 50 * s), (cx - 40 * s + sw * 0.4, base - 40 * s)], fill=(176, 120, 70), width=8)
    rim(d, x0, x1, top, base, s)
    stove(d, t, x0, x1, base, s)
    text(d, (cx, top - 70), lab, 66, NAVY)

def s_end(img, d, t, sc):
    k0 = appear(t, 0.2, 0.4)
    if k0 > 0:
        mini(d, t, 290, 860, 1, "×1"); mini(d, t, 790, 860, 2, "×2")
    k = appear(t, 0.3, 0.5)
    if k <= 0: return
    card(d, (50, 990, 1030, 1600), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    text(d, (W / 2, 1075), "Gấp đôi đá −6 °C, cùng bếp:", 58, INK, alpha=k)
    text(d, (W / 2, 1180), "đoạn ngang đầu đổi sao?", 62, DARK_OR, alpha=k)
    kh = appear(t, 2.9, 0.5)
    if kh > 0:
        card(d, (110, 1290, 970, 1540), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1415), "Gợi ý: nhiệt vào đều", 60, DARK_OR, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}; out = []
    h = sc["hook"]; out += [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    do = sc["do"]; t = do["t0"] + do["M"][0] + 0.5
    while t < do["t0"] + do["T"] - 0.4: out.append((t, "tick")); t += 0.5
    out += [(do["t0"] + do["M"][1], "tap"), (do["t0"] + do["M"][3], "tap")]
    r = sc["rutra"]; b = sc["bay"]; e = sc["end"]
    out += [(r["t0"] + r["M"][0] + 0.1, "ding"), (sc["gioi"]["t0"] + 2.2, "tap"),
            (b["t0"] + b["M"][0] - 0.1, "buzz"), (b["t0"] + b["M"][1] - 0.1, "tap"), (e["t0"] + 0.3, "open")]
    return out

CLIP = dict(id="tn-l12-chuyenthe-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Sự chuyển thể · thachlab.id.vn", cues=_cues, scenes=[
 dict(key="hook", title="Đun nước đá, ghi nhiệt độ", draw=s_hook, tail=0.3, caps=[
   "Đá −6 °C, bếp giữ một mức.",
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Bật bếp, khuấy đều.", 2.6),
   ("Đá tan: đứng gần 0 °C.", 3.0),
   ("Tan hết: tăng đều.", 2.6),
   ("Sôi: đứng gần 100 °C.", 3.0)]),
 dict(key="rutra", title="Kết quả", draw=s_rutra, tail=0.3, caps=[
   ("Hai đoạn nằm ngang.", 2.8),
   "Đá tan: nhiệt phá liên kết.",
   ("Sôi: phân tử thoát ra.", 3.2)]),
 dict(key="gioi", title="Giới hạn", draw=s_gioi, tail=0.3, caps=[
   ("Còn chưa biết gì?", 3.7)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Đúng hay sai?", 3.3),
   ("Bếp vẫn cấp nhiệt suốt.", 4.0)]),
 dict(key="end", title="Thử nghĩ", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự đoán.", 5.4)]),
])
