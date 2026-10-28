# Clip: tn-l12-thuchanh-02 - Mot lan dun da lien tuc: do nhiet nong chay rieng va nhiet hoa hoi rieng
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-thuchanh-02.json (so_lieu_mau, tham_so); JSON ghi "so lieu minh hoa".
#   m = 0,100 kg; P = 100 W; tau1 = 334 s, tau2 = 419 s, tau3 = 2 260 s; Q = 33 400 / 41 900 / 226 000 J;
#   lambda = 3,34.10^5 J/kg, c = 4 190 J/(kg.K), L = 2,26.10^6 J/kg; soi ~75% thoi gian, gap ~5,4 lan doan nong len.
# Cau hoi chot: 0,200 kg (trong khoang tham_so m 0,05-0,3) -> HS tu suy tau1 = 2 x 334 s (khong in dap so).
# Ban 1 (28/10/2026): mau chuyenthe (do thi theo thoi gian, truc co dinh tu dau) + boyle (bang so lieu) + cues.
import random
from engine import *

M_KG, P_W = "0,100", 100
STG = [("Đá tan ở 0 °C", 334, "33 400"), ("Nóng 0 → 100 °C", 419, "41 900"), ("Sôi ở 100 °C", 2260, "226 000")]
S1, S2, S3 = 334, 334 + 419, 334 + 419 + 2260          # cac moc dong ho (s) - tong cua so_lieu_mau
SHORT = ("Tan", "Nóng lên", "Sôi")
COL = (BLUE, ORANGE, RED)
def sp(n): return f"{n:,}".replace(",", " ")           # 2260 -> "2 260"
def T_of(tau):                                           # mo hinh: dung 0 °C, len deu, dung 100 °C
    if tau <= S1: return 0.0
    if tau <= S2: return 100.0 * (tau - S1) / (S2 - S1)
    return 100.0

def pill(d, cx, cy, s, size, fg, bg, alpha=1.0, padx=26):
    wdt = tw(d, s, F(size)) + 2 * padx
    card(d, (cx - wdt / 2, cy - size * 0.85, cx + wdt / 2, cy + size * 0.85), fill=A(bg, alpha), r=int(size * 0.85))
    text(d, (cx, cy), s, size, fg, alpha=alpha)

def dashed(d, p1, p2, color, w=3, dash=16, gap=12):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

# ---------------- binh + bep co oat ke + dau do ----------------
ICE = [(-90, 0), (-5, 0), (80, 0), (-50, 1), (40, 1), (-5, 2)]
R = random.Random(3)
BUB = [(R.uniform(-0.4, 0.4), R.random(), R.uniform(0.8, 1.3), R.uniform(5, 10)) for _ in range(14)]

def rig(d, t, tau, cx=300, base=800):
    w, h = 320, 340; x0, x1, top = cx - w / 2, cx + w / 2, base - h
    f_ice = 1 - clamp(tau / S1)
    if tau <= S1: lvl = 0.06 + 0.40 * (1 - f_ice)            # 0,100 kg da tan thanh 0,100 kg nuoc
    else: lvl = 0.46 * (1 - clamp((tau - S2) / (S3 - S2)))    # soi: nuoc can dan toi het
    inner = h - 14; wl = base - 8 - inner * lvl
    Tc = T_of(tau)
    d.rounded_rectangle([x0, top, x1, base], radius=22, fill=(240, 246, 252), outline=(150, 175, 205), width=4)
    if lvl > 0.004:
        d.rounded_rectangle([x0 + 8, wl, x1 - 8, base - 8], radius=16, fill=mix((170, 210, 250), (200, 214, 236), Tc / 100))
        d.line([(x0 + 10, wl), (x1 - 10, wl)], fill=(110, 160, 220), width=4)
    if f_ice > 0.02:
        sz0 = 74; sz = sz0 * f_ice ** 0.55; al = clamp(f_ice / 0.12)
        for dx, lay in ICE:
            ytop = base - 10 - sz0 * (lay + 1) * 0.92 + (sz0 - sz)
            ix = cx + dx - sz / 2
            d.rounded_rectangle([ix, ytop, ix + sz, ytop + sz], radius=int(12 * max(0.4, f_ice)),
                                fill=A((248, 252, 255), al), outline=A((110, 160, 215), al), width=4)
    # nap he (khong day kin khi dun soi)
    d.rounded_rectangle([x0 - 14, top - 22, cx + 30, top - 6], radius=8, fill=(120, 126, 140))
    boil = clamp((tau - S2) / 60) * (1 if lvl > 0.03 else 0)
    if boil > 0:
        depth = base - 8 - wl
        for (u, ph, spd, r) in BUB:
            yy = base - 14 - ((t * 0.9 * spd + ph) % 1) * max(10, depth - 20)
            d.ellipse([cx + u * w - r, yy - r, cx + u * w + r, yy + r], outline=A(WHITE, boil), width=3)
    if tau > S2 and tau < S3 + 1:
        for i in range(3):
            sx = cx + 60 + i * 45
            pts = [(sx + 14 * math.sin(t * 2.6 + i * 1.7 + k * 0.8), top - 30 - k * 26) for k in range(6)]
            d.line(pts, fill=A(GRAY, 0.5), width=7, joint="curve")
    # dau do nhiet ke: ngap nhung khong cham day
    px = cx - 100
    d.line([(px, top - 110), (px, base - 70)], fill=(120, 126, 140), width=12)
    dot(d, px, base - 66, 9, NAVY)
    d.line([(px, top - 110), (px + 40, top - 150), (520, top - 150)], fill=(120, 126, 140), width=6, joint="curve")
    # bep + oat ke (cong suat giu 100 W)
    glow = 0.55 + 0.25 * math.sin(t * 5)
    d.rounded_rectangle([x0 - 30, base + 4, x1 + 30, base + 24], radius=8, fill=mix(ORANGE, RED, glow))
    d.rounded_rectangle([x0 - 40, base + 24, x1 + 40, base + 120], radius=14, fill=NAVY)
    d.rounded_rectangle([cx - 110, base + 40, cx + 110, base + 104], radius=10, fill=(20, 60, 40))
    text(d, (cx, base + 72), f"{P_W} W", 40, (134, 239, 172))
    text(d, (cx - 160, base + 72), "oát kế", 34, WHITE, anchor="lm")

def panel(d, tau, show_timers=True):
    card(d, (600, 270, 1020, 920), fill=WHITE, outline=NAVY, w=4)
    text(d, (810, 318), "Nhiệt kế", 38, INK)
    if tau < S1 + 0.5: text(d, (810, 395), "0 °C", 72, BLUE)
    elif tau < S2: text(d, (810, 395), "đang tăng ↑", 52, ORANGE)
    else: text(d, (810, 395), "100 °C", 72, RED)
    d.line([(630, 460), (990, 460)], fill=LIGHT, width=3)
    if not show_timers: return
    text(d, (810, 500), "Đồng hồ", 38, INK)
    starts = (0, S1, S2)
    for i, (lab, dur, _) in enumerate(STG):
        y = 580 + i * 112
        el = clamp(tau - starts[i], 0, dur)
        on = starts[i] <= tau < starts[i] + dur
        if on: card(d, (622, y - 46, 998, y + 46), fill=(255, 237, 213), r=20)
        text(d, (642, y), SHORT[i], 38, COL[i] if el > 0 else GRAY, anchor="lm")
        text(d, (980, y), f"{sp(int(round(el)))} s" if el > 0 else "–", 42, INK if el > 0 else GRAY, anchor="rm")

# ---------------- do thi t(tau), truc co dinh tu dau ----------------
XMAX, YLO, YHI = 3100, -20, 125
def plot(d, box, tau, hl=(0, 0, 0), pen=True):
    x0, ytop, x1, y0 = box
    X = lambda s: x0 + s / XMAX * (x1 - x0); Y = lambda T: y0 - (T - YLO) / (YHI - YLO) * (y0 - ytop)
    for T in (0, 100):
        d.line([(x0, Y(T)), (x1, Y(T))], fill=LIGHT, width=3)
        text(d, (x0 - 16, Y(T)), str(T), 36, INK, anchor="rm")
    dashed(d, (x0, Y(50)), (x1, Y(50)), LIGHT, 3)
    d.line([(x0, y0), (x1 + 10, y0)], fill=NAVY, width=5); d.line([(x0, y0), (x0, ytop - 10)], fill=NAVY, width=5)
    d.polygon([(x1 + 26, y0), (x1 + 8, y0 - 10), (x1 + 8, y0 + 10)], fill=NAVY)
    d.polygon([(x0, ytop - 26), (x0 - 10, ytop - 8), (x0 + 10, ytop - 8)], fill=NAVY)
    text(d, (x0 + 22, ytop - 8), "t (°C)", 36, INK, anchor="lm")
    text(d, (x1 + 20, y0 + 40), "τ (s)", 36, INK, anchor="rm")
    for s in (1000, 2000, 3000):
        d.line([(X(s), y0), (X(s), y0 + 12)], fill=NAVY, width=4)
        if s < 3000: text(d, (X(s), y0 + 40), sp(s), 36, INK)
    segs = ((0, S1, 0, 0), (S1, S2, 0, 100), (S2, S3, 100, 100))
    for (a, b, ta, tb), h, c in zip(segs, hl, COL):
        if h > 0:
            d.line([(X(a), Y(ta)), (X(b), Y(tb))], fill=A(mix(c, WHITE, 0.55), h), width=30)
    if tau > 0:
        pts = [(0, 0)] + [(s, T_of(s)) for s in (S1, S2, S3) if s < tau] + [(min(tau, S3), T_of(min(tau, S3)))]
        d.line([(X(s), Y(T)) for s, T in pts], fill=NAVY, width=7, joint="curve")
        for s in (0, S1, S2, S3):
            if s <= tau + 1e-6: dot(d, X(s), Y(T_of(s)), 11, ORANGE, outline=WHITE)
        if pen and tau < S3 - 1: dot(d, X(tau), Y(T_of(tau)), 13, RED, outline=WHITE)
    return X, Y

def minh_hoa(d, x, y, alpha=1.0, anchor="rm"):
    text(d, (x, y), "Số liệu minh hoạ", 34, PURPLE, anchor=anchor, alpha=alpha)

# ---------------- canh 1: Du doan ----------------
OPTS = ("A. Đá tan dần ở 0 °C tới hết", "B. Nước nóng từ 0 lên 100 °C",
        "C. Nước sôi ở 100 °C tới cạn", "D. Ba giai đoạn dài bằng nhau")

def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    rig(d, t, 0.0)
    panel(d, 0.0, show_timers=False)
    text(d, (810, 520), "Cân nước đá", 38, INK, alpha=appear(t, 0.2))
    text(d, (810, 590), f"{M_KG} kg", 60, INK, alpha=appear(t, 0.2))
    text(d, (810, 680), "Bếp giữ", 38, INK, alpha=appear(t, 0.4))
    text(d, (810, 750), f"{P_W} W suốt", 60, INK, alpha=appear(t, 0.4))
    text(d, (810, 840), "tới khi nước cạn", 38, INK, alpha=appear(t, 0.4))
    a = appear(t, 1.0, 0.5)
    if a <= 0: return
    card(d, (50, 960, 1030, 1620), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, 1010, "DỰ ĐOÁN", 36, WHITE, PURPLE, a)
    ctext(d, 1092, "Đun liên tục, bếp giữ 100 W.\nGiai đoạn nào kéo dài nhất?", 42, INK, alpha=a)
    text(d, (W / 2, 1180), "Tra bảng: λ = 334 000 J/kg; L = 2 260 000 J/kg", 36, INK, alpha=a)
    text(d, (W / 2, 1226), "c = 4 190 J/(kg·K)", 36, INK, alpha=a)
    for i, s in enumerate(OPTS):
        k = appear(t, 1.3 + 0.15 * i, 0.4)
        y = 1300 + i * 72
        card(d, (110, y - 32, 970, y + 32), fill=A((245, 243, 255), k), outline=A(PURPLE, k), r=20, w=3)
        text(d, (140, y), s, 38, INK, anchor="lm", alpha=k)
    tc = 2.3; tend = sc["T"] - 0.1; q = clamp((t - tc) / (tend - tc))
    d.rounded_rectangle([140, 1580, 940, 1592], radius=6, fill=A(LIGHT, a))
    if q < 1: d.rounded_rectangle([140, 1580, 140 + 800 * (1 - q), 1592], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
def tau_of(t, sc):
    M = sc["M"]
    return float(np.interp(t, [M[0] + 1.0, M[1] + 2.2, M[2] + 0.1, M[2] + 2.3, M[3] + 0.1, M[3] + 2.8],
                           [0, S1, S1, S2, S2, S3]))

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; tau = tau_of(t, sc)
    rig(d, t, tau)
    panel(d, tau)
    if M[3] + 0.1 < t < M[3] + 2.8:
        blink = 0.65 + 0.35 * math.sin(t * 6)
        wdt = tw(d, "TUA NHANH", F(32)) + 90
    card(d, (40, 950, 1040, 1620), fill=WHITE, outline=LIGHT, w=3)
    if M[3] + 0.1 < t < M[3] + 2.8:
        cxp = 560
        card(d, (cxp - wdt / 2, 962, cxp + wdt / 2, 1018), fill=ORANGE, r=28)
        for j in range(2):
            tx = cxp - wdt / 2 + 22 + j * 16
            d.polygon([(tx, 976), (tx, 1004), (tx + 16, 990)], fill=A(WHITE, blink))
        text(d, (cxp + 22, 990), "TUA NHANH", 32, WHITE)
    minh_hoa(d, 1010, 990)
    plot(d, (170, 1040, 960, 1520), tau)

# ---------------- canh 3: Dap an + vi sao nam ngang ----------------
GR = [(c, r) for r in range(4) for c in range(5)]
BONDS = [(i, j) for i, (c, r) in enumerate(GR) for j, (c2, r2) in enumerate(GR) if (c2 == c + 1 and r2 == r) or (r2 == r + 1 and c2 == c)]
R2 = random.Random(11); BT = [R2.uniform(0.05, 0.95) for _ in BONDS]
PH = [(R2.uniform(0, 6.3), R2.uniform(0, 6.3), R2.uniform(0.5, 1.0)) for _ in GR]

def melt_panel(d, box, t, p):
    x0, y0, x1, y1 = box; sx = (x1 - x0 - 120) / 4; sy = (y1 - y0 - 120) / 3
    pos = []
    for i, (c, r) in enumerate(GR):
        a, b, s = PH[i]; free = clamp(p * 1.3 - 0.15)
        jx = 6 * math.sin(t * 14 * s + a); jy = 6 * math.cos(t * 13 * s + b)
        dx = free * 24 * math.sin(t * 1.1 * s + a); dy = free * 20 * math.cos(t * 0.9 * s + b)
        pos.append((x0 + 60 + c * sx + jx + dx, y0 + 60 + r * sy + jy + dy))
    for (i, j), bt in zip(BONDS, BT):
        al = 1 - clamp((p - bt) / 0.08)
        if al > 0: d.line([pos[i], pos[j]], fill=A(PURPLE, 0.8 * al), width=6)
    for (x, y) in pos: dot(d, x, y, 17, BLUE, outline=WHITE)

def boil_panel(d, box, t):
    x0, y0, x1, y1 = box; sy = y0 + 190
    d.rounded_rectangle([x0 + 12, sy, x1 - 12, y1 - 12], radius=18, fill=(214, 230, 250))
    d.line([(x0 + 16, sy), (x1 - 16, sy)], fill=(110, 160, 220), width=5)
    for i, (a, b, s) in enumerate(PH[:14]):
        x = refl(x0 + 50 + a * 60 + t * 70 * s, x0 + 40, x1 - 40)
        y = refl(sy + 40 + b * 40 + t * 55 * s, sy + 36, y1 - 40)
        dot(d, x, y, 17, BLUE, outline=WHITE)
    for i in range(4):
        u = (t * 0.45 + i / 4) % 1
        x = x0 + 90 + i * 100 + 18 * math.sin(t * 2 + i); y = sy - 10 - u * (sy - y0 - 40)
        al = clamp((1 - u) / 0.3)
        dot(d, x, y, 17, A(BLUE, al), outline=A(WHITE, al))
        if u < 0.5: arrow(d, (x, y - 26), (x, y - 70), A(ORANGE, al * (1 - u * 2)), w=5, head=14)

def heat_in(d, rx, y, t, a):
    text(d, (rx, y), "Nhiệt từ bếp", 36, INK, anchor="lm", alpha=a)
    for j in range(5):
        u = (t * 0.8 + j / 5) % 1; xx = rx + 10 + u * 380
        al = a * min(1, u / 0.15, (1 - u) / 0.15)
        d.line([(xx, y + 40), (xx + 18, y + 56), (xx, y + 72)], fill=A(ORANGE, al), width=7)
    text(d, (rx, y + 106), "vẫn vào đều", 34, ORANGE, anchor="lm", alpha=a)

def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; cur = cur_cap(sc, t)
    card(d, (40, 245, 1040, 905), fill=WHITE, outline=LIGHT, w=3)
    minh_hoa(d, 1010, 282)
    hA = appear(t, M[0] + 0.2, 0.5) * (1 - 0.7 * appear(t, M[1] - 0.1, 0.4))
    h1 = appear(t, M[1] - 0.1, 0.4) * (1 - appear(t, M[2] - 0.1, 0.4))
    h3 = max(hA, appear(t, M[2] - 0.1, 0.4))
    X, Y = plot(d, (170, 330, 960, 810), S3, hl=(h1, 0, h3), pen=False)
    text(d, (X(0) + 8, Y(0) - 95), "334 s", 34, BLUE, anchor="lm")
    d.line([(X(S1 / 2), Y(0) - 72), (X(S1 / 2), Y(0) - 20)], fill=BLUE, width=3)
    text(d, (X((S1 + S2) / 2) + 66, Y(50) + 14), "419 s", 34, ORANGE, anchor="lm")
    text(d, ((X(S2) + X(S3)) / 2, Y(100) - 48), "2 260 s ≈ 75% thời gian", 36, RED)
    ka = appear(t, M[0] + 0.1, 0.5)
    pill(d, 720, 600, "ĐÁP ÁN C", 40, WHITE, NAVY, ka)
    # khung duoi: so sanh 3 thoi gian -> co che tan -> co che soi
    card(d, (40, 935, 1040, 1620), fill=WHITE, outline=LIGHT, w=3)
    if cur <= 0:
        text(d, (W / 2, 990), f"Cùng bếp {P_W} W, cùng {M_KG} kg", 36, MUTED)
        for i, (lab, dur, _) in enumerate(STG):
            y = 1080 + i * 120; g = ease((t - 0.4 - 0.25 * i) / 0.7)
            text(d, (90, y), SHORT[i], 38, COL[i], anchor="lm")
            wmax = 520 * dur / 2260
            d.rounded_rectangle([290, y - 26, 290 + max(52, wmax * g), y + 26], radius=26, fill=COL[i])
            text(d, (290 + max(52, wmax * g) + 18, y), f"{sp(dur)} s", 38, INK, anchor="lm", alpha=g)
        k2 = appear(t, 0.2, 0.4)
        ctext(d, 1480, "Sôi lâu gấp ≈ 5,4 lần\nnóng lên 0 → 100 °C", 48, RED, maxw=900, alpha=k2)
        return
    soi = cur >= 2
    a = appear(t, (M[2] if soi else M[1]) - 0.1, 0.4)
    text(d, (W / 2, 985), "Trong bình, lúc nước đang sôi" if soi else "Trong bình, lúc đá đang tan", 38, INK, alpha=a)
    box = (70, 1030, 540, 1590)
    card(d, box, fill=A((244, 241, 255), a), r=24)
    if soi: boil_panel(d, box, t)
    else: melt_panel(d, box, t, clamp((t - M[1]) / (M[2] - M[1] - 0.3)))
    rx = 580
    heat_in(d, rx, 1080, t, a)
    a2 = appear(t, (M[2] if soi else M[1]) + 0.4, 0.5)
    if soi:
        text(d, (rx, 1290), "Phân tử thoát khỏi", 38, INK, anchor="lm", alpha=a2)
        text(d, (rx, 1340), "mặt nước thành hơi", 38, INK, anchor="lm", alpha=a2)
        text(d, (rx, 1450), "t đứng ở 100 °C", 40, RED, anchor="lm", alpha=a2)
    else:
        text(d, (rx, 1290), "Phá liên kết", 38, INK, anchor="lm", alpha=a2)
        text(d, (rx, 1340), "giữa các phân tử", 38, INK, anchor="lm", alpha=a2)
        text(d, (rx, 1450), "t đứng ở 0 °C", 40, BLUE, anchor="lm", alpha=a2)

# ---------------- canh 4: Tinh lambda, L + chua do duoc gi ----------------
def s_calc(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    card(d, (40, 245, 1040, 690), fill=WHITE, outline=NAVY, w=4)
    minh_hoa(d, 1010, 282)
    xs = (70, 640, 990)
    for x, c, an in zip(xs, ("Giai đoạn", "τ (s)", "Q = P·τ (J)"), ("lm", "rm", "rm")):
        text(d, (x, 330), c, 36, INK, anchor=an)
    d.line([(60, 366), (1020, 366)], fill=LIGHT, width=4)
    for i, (lab, dur, q) in enumerate(STG):
        k = appear(t, 0.1 + 0.2 * i, 0.35); y = 420 + i * 90
        hlr = appear(t, 0.9, 0.4) if i != 1 else 0
        if hlr > 0: d.rounded_rectangle([56, y - 36, 1024, y + 36], radius=16, fill=A((225, 236, 255), hlr * k))
        text(d, (xs[0], y), lab, 38, COL[i], anchor="lm", alpha=k)
        text(d, (xs[1], y), sp(dur), 40, INK, anchor="rm", alpha=k)
        text(d, (xs[2], y), q, 40, INK, anchor="rm", alpha=k)
    kf = appear(t, M[0] + 0.3, 0.5)
    card(d, (40, 720, 1040, 1230), fill=A(WHITE, kf), outline=A(BLUE, kf), w=5)
    text(d, (W / 2, 770), "Hai đoạn ngang: cùng công thức P·τ/m", 38, MUTED, alpha=kf)
    rich(d, W / 2, 860, "λ = P·τ_{1}/m = 3,34·10^{5} J/kg", 54, BLUE, alpha=kf)
    text(d, (W / 2, 930), "= 100 · 334 / 0,100", 40, INK, alpha=kf)
    kl = appear(t, M[0] + 0.9, 0.5)
    rich(d, W / 2, 1040, "L = P·τ_{3}/m = 2,26·10^{6} J/kg", 54, RED, alpha=kl)
    text(d, (W / 2, 1110), "= 100 · 2 260 / 0,100", 40, INK, alpha=kl)
    text(d, (W / 2, 1180), "L lớn hơn λ gần 7 lần", 38, PURPLE, alpha=appear(t, M[0] + 1.6, 0.5))
    kc = appear(t, M[1] - 0.3, 0.5)
    if kc <= 0: return
    y0 = 1270 + (1 - back((t - M[1] + 0.3) / 0.5)) * 30
    card(d, (60, y0, 1020, y0 + 340), fill=WHITE, outline=PURPLE, w=6)
    pill(d, W / 2, y0 + 56, "SAI SỐ: MẤT NHIỆT", 36, WHITE, PURPLE)
    ctext(d, y0 + 165, "λ, L đo được lớn hơn", 52, PURPLE)
    ctext(d, y0 + 262, "giá trị tra bảng", 44, INK, maxw=880)

# ---------------- canh 5: Bay - can da con uot ----------------
def s_trap(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    card(d, (60, 250, 1020, 340), fill=(254, 226, 226), outline=RED, w=5)
    text(d, (W / 2, 295), "Bẫy: cân đá khi còn ướt", 44, RED)
    # can dien tu + coc da uot (hinh co ngay tu dau canh)
    card(d, (60, 370, 1020, 1000), fill=WHITE, outline=LIGHT, w=3)
    cx = 400
    d.rounded_rectangle([cx - 230, 860, cx + 230, 950], radius=18, fill=NAVY)
    d.rounded_rectangle([cx - 110, 878, cx + 110, 932], radius=10, fill=(20, 60, 40))
    text(d, (cx, 905), "m cân", 34, (134, 239, 172))
    d.rounded_rectangle([cx - 200, 836, cx + 200, 860], radius=8, fill=(150, 155, 170))
    # coc
    d.polygon([(cx - 150, 560), (cx + 150, 560), (cx + 120, 836), (cx - 120, 836)], fill=(240, 246, 252), outline=(150, 175, 205))
    d.rectangle([cx - 126, 770, cx + 126, 832], fill=(170, 210, 250))            # nuoc dong day coc
    for dx, dy in ((-80, 690), (0, 680), (75, 695), (-40, 610), (45, 615)):
        d.rounded_rectangle([cx + dx - 40, dy - 40, cx + dx + 40, dy + 40], radius=12, fill=(248, 252, 255), outline=(110, 160, 215), width=4)
    for dx, dy in ((-80, 735), (5, 728), (70, 742), (-40, 655), (45, 660)):
        d.ellipse([cx + dx - 7, dy - 10, cx + dx + 7, dy + 10], fill=(90, 150, 230))
    # chu thich
    arrow(d, (720, 620), (470, 640), NAVY, w=5, head=18)
    text(d, (735, 620), "đá", 40, INK, anchor="lm")
    arrow(d, (720, 790), (520, 800), BLUE, w=5, head=18)
    text(d, (735, 775), "nước bám", 40, BLUE, anchor="lm")
    text(d, (735, 825), "và đọng đáy", 40, BLUE, anchor="lm")
    kr = appear(t, M[0] + 0.8, 0.4)
    text(d, (735, 905), "cân cả vào m", 38, RED, anchor="lm", alpha=kr)
    # cong thuc va chieu sai
    card(d, (60, 1040, 1020, 1610), fill=WHITE, outline=RED, w=5)
    ka = appear(t, M[0] + 0.3, 0.4)
    rich(d, W / 2, 1140, "λ = P·τ_{1}/m", 60, INK, alpha=ka)
    ctext(d, 1250, "m cân lớn hơn m đá thật", 42, INK, alpha=appear(t, M[0] + 0.7, 0.4))
    ctext(d, 1340, "→ λ tính ra NHỎ HƠN thật", 48, RED, alpha=appear(t, M[1], 0.3))
    card(d, (110, 1420, 970, 1570), fill=A((220, 252, 231), appear(t, M[1] + 0.8, 0.3)), r=24)
    ctext(d, 1495, "Làm đúng: để đá ráo nước rồi mới cân", 40, GREEN, maxw=820, alpha=appear(t, M[1] + 0.8, 0.3))

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def _body(d, t, k):
    for j, (lab, res, col) in enumerate(((f"{M_KG} kg", "334 s", BLUE), ("0,200 kg", "? s", ORANGE))):
        x = 290 + j * 500
        d.rounded_rectangle([x - 200, 1020, x + 200, 1240], radius=24, fill=A((247, 248, 252), k), outline=A(col, k), width=4)
        text(d, (x, 1070), lab, 40, INK, alpha=k)
        text(d, (x, 1130), "đoạn ngang 0 °C", 34, INK, alpha=k)
        text(d, (x, 1195), res, 46, col, alpha=k)

def s_end(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    chot_hoi(d, t, sc, "Đoạn nằm ngang: nhiệt vào để chuyển thể",
             "Cùng bếp 100 W, đun 0,200 kg đá đang tan. Đoạn ngang ở 0 °C dài bao lâu?", body=_body)
    kb = appear(t, M[0] + 0.4, 0.5)
    if kb <= 0: return
    card(d, (110, 1300, 970, 1560), fill=A((255, 237, 213), kb), outline=A(ORANGE, kb), r=24, w=4)
    text(d, (W / 2, 1355), "Gợi ý", 40, ORANGE, alpha=kb)
    kh = appear(t, M[0] + 2.5, 0.5)
    if kh <= 0:
        text(d, (W / 2, 1450), "tự nghĩ trước…", 38, MUTED, alpha=kb); return
    ctext(d, 1450, "λ = P·τ/m; P và λ giữ nguyên", 42, INK, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, ca, tr, e = sc["hook"], sc["do"], sc["ans"], sc["calc"], sc["trap"], sc["end"]
    out = [(h["t0"] + 1.0, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
           (do["t0"] + do["M"][0] + 1.0, "tap"), (do["t0"] + do["M"][2] + 0.1, "tap")]
    t = do["t0"] + do["M"][3] + 0.3
    while t < do["t0"] + do["M"][3] + 2.7: out.append((t, "tick")); t += 0.5
    out += [(an["t0"] + an["M"][0] + 0.1, "ding"), (ca["t0"] + ca["M"][1] - 0.3, "tap"),
            (tr["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l12-thuchanh-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Thực hành đo λ và L · thachlab.id.vn", scenes=[
 dict(key="hook", title="Đun đá liên tục tới cạn", draw=s_hook, tail=0.6, caps=[
   ("0,100 kg đá đang tan, bếp giữ 100 W.", 2.2),
   ("Chọn một đáp án trước khi xem tiếp.", 6.6)]),
 dict(key="do", title="Một lần đun, ba mốc giờ", draw=s_do, tail=0.4, caps=[
   ("Bật bếp và bấm đồng hồ cùng lúc.", 2.3),
   ("Nhiệt kế đứng ở 0 °C: đá đang tan.", 2.6),
   ("Đá tan hết: nhiệt độ leo đều lên 100 °C.", 2.7),
   ("Ở 100 °C lại đứng yên, sôi tới cạn.", 3.0)]),
 dict(key="ans", title="Vì sao có đoạn nằm ngang?", draw=s_ans, tail=0.3, caps=[
   ("Đoạn sôi dài nhất: đáp án C.", 3.4),
   ("Đá tan: nhiệt vào để phá liên kết.", 2.8),
   ("Sôi: nhiệt giúp phân tử thoát thành hơi.", 2.9)]),
 dict(key="calc", title="Tính λ và L", draw=s_calc, tail=0.4, caps=[
   ("λ và L: cùng công thức P·τ/m.", 2.8),
   ("Sai số: mất nhiệt → λ, L đo được lớn hơn.", 3.4)]),
 dict(key="trap", title="Cái bẫy khi cân", draw=s_trap, tail=0.3, caps=[
   ("Bẫy: cân đá khi còn ướt, chưa ráo.", 2.6),
   ("m cân lớn hơn → λ tính ra nhỏ hơn thật.", 2.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.4, caps=[
   ("Thử nghĩ: đá gấp đôi thì tan bao lâu?", 3.6)]),
])
