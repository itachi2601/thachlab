# Clip: tn-l12-thuchanh-02 - Mot lan dun da lien tuc: do nhiet nong chay rieng va nhiet hoa hoi rieng
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-thuchanh-02.json (so_lieu_mau, tham_so); JSON ghi "so lieu minh hoa".
#   m = 0,100 kg; P = 100 W; tau1 = 334 s, tau2 = 419 s, tau3 = 2 260 s; lambda = 3,34.10^5 = 334 000 J/kg,
#   L = 2,26.10^6 = 2 260 000 J/kg; soi gap ~5,4 lan doan nong len (rut_ra).
# Quan niem sai can danh (hien_tuong_hay_sai[0], KE-HOACH viec 4 dong 8): doan nam ngang = bep ngung cap nhiet.
#   -> Bay: hai binh "Luc dau"/"Luc sau" cung doan soi, oat ke van 100 W, muc nuoc tut -> van nhan nhiet de hoa hoi.
# Du doan (giu tu ban 1, khong trung quiz mo bai "nhiet ke khi da dang tan" va Cau 2 "doan ngang thu hai la gi"):
#   giai doan nao dai nhat -> Soi toi can (khung web hoi A-D, clip khong ve nut - K10).
# Cau chot moi (ban 2): dang soi thi tat bep, nhiet ke chi the nao? -> giam xuong duoi 100 °C (doan ngang can nhiet vao;
#   khong nhiet vao thi nuoc mat nhiet ra phong). Clip khong ve doan sau khi tat bep. Bo cau chot cu 0,200 kg -> 668 s
#   vi trung dap so bai Thu suc (0,400 kg, 200 W, 668 s).
# Ban 2 (21/11/2026, viec 4 lo 20): cong --do-chu moi (chu than canh >= 55 px ve, khoi chu cach >= 2,5 s, dem nguoc
#   5 cham), bo dong "Chon dap an o khung cau hoi", bo bay da uot (thay bang bay doan ngang = bep tat), <= 50 s.
# Ban 1 (28/10/2026): mau chuyenthe + boyle + cues.
import random
from engine import *

M_KG, P_W = "0,100", 100
STG = (334, 419, 2260)                                   # tau1, tau2, tau3 (s) - so_lieu_mau
S1, S2, S3 = 334, 334 + 419, 334 + 419 + 2260           # moc tren truc thoi gian (chi de ve)
SHORT = ("Tan", "Nóng lên", "Sôi")
COL = (BLUE, ORANGE, RED)
DARK_OR = (181, 71, 8)
def sp(n): return f"{n:,}".replace(",", " ")           # 2260 -> "2 260"
def T_of(tau):
    if tau <= S1: return 0.0
    if tau <= S2: return 100.0 * (tau - S1) / (S2 - S1)
    return 100.0

def pill(d, cx, cy, s, size, fg, bg, alpha=1.0, padx=30):
    wdt = tw(d, s, F(size)) + 2 * padx
    card(d, (cx - wdt / 2, cy - size * 0.75, cx + wdt / 2, cy + size * 0.75), fill=A(bg, alpha), r=int(size * 0.75))
    text(d, (cx, cy), s, size, fg, alpha=alpha)

def dashed(d, p1, p2, color, w=3, dash=16, gap=12):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

def dots5(d, t, tc, tend, y, col, a=1.0):
    """Dem nguoc 5 cham (r 40 = 70 px trong mp4), moi cham tat dan theo thoi gian nghi."""
    n_off = 0 if t < tc else min(5, int((t - tc) / ((tend - tc) / 5)) + 1)
    for j in range(5):
        dot(d, W / 2 + (j - 2) * 140, y, 40, A(LIGHT, a) if j >= 5 - n_off else A(col, a))

# ---------------- binh + bep co oat ke + dau do ----------------
ICE = [(-85, 0), (0, 0), (85, 0), (-45, 1), (45, 1), (0, 2)]
R = random.Random(3)
BUB = [(R.uniform(-0.4, 0.4), R.random(), R.uniform(0.8, 1.3), R.uniform(6, 11)) for _ in range(14)]

def beaker(d, t, cx, base, w, h, lvl, f_ice=0.0, boil=0.0, Tc=0.0, steam=False):
    x0, x1, top = cx - w / 2, cx + w / 2, base - h
    d.rounded_rectangle([x0, top, x1, base], radius=22, fill=(240, 246, 252), outline=(150, 175, 205), width=5)
    inner = h - 14; wl = base - 8 - inner * lvl
    if lvl > 0.004:
        d.rounded_rectangle([x0 + 8, wl, x1 - 8, base - 8], radius=16, fill=mix((170, 210, 250), (200, 214, 236), Tc / 100))
        d.line([(x0 + 10, wl), (x1 - 10, wl)], fill=(70, 130, 210), width=6)
    if f_ice > 0.02:
        sz0 = w * 0.24; sz = sz0 * f_ice ** 0.55; al = clamp(f_ice / 0.12)
        for dx, lay in ICE:
            ytop = base - 10 - sz0 * (lay + 1) * 0.92 + (sz0 - sz)
            ix = cx + dx * w / 320 - sz / 2
            d.rounded_rectangle([ix, ytop, ix + sz, ytop + sz], radius=int(12 * max(0.4, f_ice)),
                                fill=A((248, 252, 255), al), outline=A((110, 160, 215), al), width=4)
    if boil > 0:
        depth = base - 8 - wl
        for (u, ph, spd, r) in BUB:
            yy = base - 14 - ((t * 0.9 * spd + ph) % 1) * max(10, depth - 20)
            d.ellipse([cx + u * w - r, yy - r, cx + u * w + r, yy + r], outline=A(WHITE, boil), width=3)
    if steam:
        for i in range(3):
            sx = cx - 40 + i * 45
            pts = [(sx + 14 * math.sin(t * 2.6 + i * 1.7 + k * 0.8), top - 20 - k * 22) for k in range(5)]
            d.line(pts, fill=A(GRAY, 0.55), width=7, joint="curve")
    return top

def stove(d, t, cx, base, half, watt="100 W", ring=0.0):
    glow = 0.55 + 0.25 * math.sin(t * 5)
    d.rounded_rectangle([cx - half - 30, base + 4, cx + half + 30, base + 24], radius=8, fill=mix(ORANGE, RED, glow))
    d.rounded_rectangle([cx - half - 40, base + 24, cx + half + 40, base + 130], radius=14, fill=NAVY)
    if ring > 0:
        d.rounded_rectangle([cx - 122, base + 32, cx + 122, base + 122], radius=16, outline=A(ORANGE, ring), width=8)
    d.rounded_rectangle([cx - 108, base + 44, cx + 108, base + 110], radius=10, fill=(20, 60, 40))
    text(d, (cx, base + 77), watt, 58, (134, 239, 172))

def rig(d, t, tau, cx=290, base=790, ring=0.0):
    f_ice = 1 - clamp(tau / S1)
    if tau <= S1: lvl = 0.06 + 0.40 * (1 - f_ice)            # 0,100 kg da tan thanh 0,100 kg nuoc
    else: lvl = 0.46 * (1 - clamp((tau - S2) / (S3 - S2)))    # soi: nuoc can dan
    boil = clamp((tau - S2) / 60) * (1 if lvl > 0.03 else 0)
    top = beaker(d, t, cx, base, 300, 330, lvl, f_ice, boil, T_of(tau), steam=S2 < tau < S3 + 1)
    d.rounded_rectangle([cx - 164, top - 22, cx + 30, top - 6], radius=8, fill=(120, 126, 140))   # nap he
    px = cx - 95                                                # dau do: ngap, khong cham day
    d.line([(px, top - 100), (px, base - 70)], fill=(120, 126, 140), width=12)
    dot(d, px, base - 66, 9, NAVY)
    d.line([(px, top - 100), (px + 40, top - 140), (548, top - 140)], fill=(120, 126, 140), width=6, joint="curve")
    stove(d, t, cx, base, 150, ring=ring)
    text(d, (cx, base + 190), "oát kế", 56, INK)

def panel(d, tau, show_timers=True):
    card(d, (560, 260, 1040, 1010), fill=WHITE, outline=NAVY, w=4)
    if show_timers: text(d, (800, 310), "Nhiệt kế", 56, INK)
    else: text(d, (800, 310), "t (°C)", 60, INK)            # hook: bot chu cho cau hoi neu ten 3 giai doan
    if tau < S1 + 0.5: text(d, (800, 405), "0 °C", 80, BLUE)
    elif tau < S2: text(d, (800, 405), "tăng ↑", 72, ORANGE)
    else: text(d, (800, 405), "100 °C", 80, RED)
    d.line([(590, 470), (1010, 470)], fill=LIGHT, width=4)
    if not show_timers: return
    text(d, (800, 520), "Đồng hồ", 56, INK)
    starts = (0, S1, S2)
    for i, dur in enumerate(STG):
        y = 625 + i * 115
        el = clamp(tau - starts[i], 0, dur)
        if starts[i] <= tau < starts[i] + dur: card(d, (576, y - 50, 1024, y + 50), fill=(255, 237, 213), r=22)
        text(d, (592, y), SHORT[i], 56, COL[i] if el > 0 else GRAY, anchor="lm")
        text(d, (1010, y), f"{sp(int(round(el)))} s" if el > 0 else "–", 56, INK if el > 0 else GRAY, anchor="rm")
    text(d, (800, 960), "Minh hoạ", 56, PURPLE)

# ---------------- do thi t(tau), truc co dinh ----------------
XMAX, YLO, YHI = 3100, -20, 125
def plot(d, box, tau, hl=(0, 0, 0), pen=True, ticks=True):
    x0, ytop, x1, y0 = box
    X = lambda s: x0 + s / XMAX * (x1 - x0); Y = lambda T: y0 - (T - YLO) / (YHI - YLO) * (y0 - ytop)
    for T in (0, 100):
        d.line([(x0, Y(T)), (x1, Y(T))], fill=LIGHT, width=3)
        text(d, (x0 - 16, Y(T)), str(T), 56, INK, anchor="rm")
    d.line([(x0, y0), (x1 + 10, y0)], fill=NAVY, width=5); d.line([(x0, y0), (x0, ytop - 10)], fill=NAVY, width=5)
    d.polygon([(x1 + 26, y0), (x1 + 8, y0 - 10), (x1 + 8, y0 + 10)], fill=NAVY)
    d.polygon([(x0, ytop - 26), (x0 - 10, ytop - 8), (x0 + 10, ytop - 8)], fill=NAVY)
    text(d, (x0 + 24, ytop - 4), "t (°C)", 56, INK, anchor="lm")
    text(d, (x1 + 34, y0 + 52), "τ (s)", 56, INK, anchor="rm")
    if ticks:
        for s in (1000, 2000):
            d.line([(X(s), y0), (X(s), y0 + 12)], fill=NAVY, width=4)
            text(d, (X(s), y0 + 52), sp(s), 56, INK)
    segs = ((0, S1, 0, 0), (S1, S2, 0, 100), (S2, S3, 100, 100))
    for (a, b, ta, tb), h, c in zip(segs, hl, COL):
        if h > 0:
            d.line([(X(a), Y(ta)), (X(min(b, max(tau, a))), Y(ta + (tb - ta) * clamp((min(b, tau) - a) / (b - a))))],
                   fill=A(mix(c, WHITE, 0.45), h), width=34)
    if tau > 0:
        pts = [(0, 0)] + [(s, T_of(s)) for s in (S1, S2, S3) if s < tau] + [(min(tau, S3), T_of(min(tau, S3)))]
        d.line([(X(s), Y(T)) for s, T in pts], fill=NAVY, width=8, joint="curve")
        if pen and tau < S3 - 1: dot(d, X(tau), Y(T_of(tau)), 14, RED, outline=WHITE)
    return X, Y

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, t, 0.0)
    panel(d, 0.0, show_timers=False)
    text(d, (800, 640), f"{M_KG} kg đá", 64, INK)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1060 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 590), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", 56, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 195), "Tan, nóng lên, sôi:", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 295), "Giai đoạn nào dài nhất?", 62, INK, alpha=a)   # K10: khong ve nut A-D
    dots5(d, t, M[1] + 0.3, sc["T"] - 0.1, y0 + 470, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
def tau_of(t, sc):
    M = sc["M"]
    # doan soi tua deu, xong som ~1,2 s truoc het canh de so 2 260 s dung lai doc duoc
    return float(np.interp(t, [M[0] + 0.3, M[1] - 0.2, M[1] + 0.2, M[2] - 0.3, M[2] + 2.6],
                           [0, S1, S1, S2, S3]))

def s_do(img, d, t, sc):
    M = sc["M"]; tau = tau_of(t, sc)
    flat = tau <= S1 or tau >= S2
    rig(d, t, tau, ring=(0.6 + 0.4 * math.sin(t * 6)) if flat and t > M[0] + 0.3 else 0.0)
    panel(d, tau)
    card(d, (40, 1060, 1040, 1680), fill=WHITE, outline=LIGHT, w=3)
    if t < M[2] + 2.6:                           # ca thi nghiem chieu tua nhanh
        blink = 0.65 + 0.35 * math.sin(t * 6)
        wdt = tw(d, "TUA NHANH", F(56)) + 100; cxp = 700
        card(d, (cxp - wdt / 2, 1076, cxp + wdt / 2, 1150), fill=ORANGE, r=36)
        for j in range(2):
            tx = cxp - wdt / 2 + 24 + j * 18
            d.polygon([(tx, 1096), (tx, 1130), (tx + 18, 1113)], fill=A(WHITE, blink))
        text(d, (cxp + 24, 1113), "TUA NHANH", 56, WHITE)
    plot(d, (210, 1180, 950, 1560), tau)

# ---------------- canh 3: Dap an ----------------
def s_ans(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 250, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    h3 = 0.5 + 0.5 * appear(t, M[0], 0.4)
    plot(d, (210, 360, 950, 870), S3, hl=(0.5, 0.5, h3), pen=False, ticks=False)
    ka = appear(t, M[0] + 0.1, 0.4)
    if ka > 0: pill(d, W / 2, 1065, "ĐÁP ÁN: SÔI TỚI CẠN", 56, WHITE, NAVY, ka)
    kb = appear(t, M[1] - 0.1, 0.4)
    if kb <= 0: return
    card(d, (40, 1130, 1040, 1680), fill=A(WHITE, kb), outline=A(NAVY, kb), w=3)
    for i, dur in enumerate(STG):
        y = 1225 + i * 135; g = ease((t - M[1] + 0.1 - 0.2 * i) / 0.8)
        text(d, (80, y), SHORT[i], 58, COL[i], anchor="lm", alpha=kb)
        wmax = 540 * dur / 2260; ww = max(40, wmax * g)
        d.rounded_rectangle([340, y - 30, 340 + ww, y + 30], radius=30, fill=A(COL[i], kb))
        vx = min(340 + ww + 20, 1020 - tw(d, f"{sp(dur)} s", F(58)))
        vy = y if 340 + ww + 20 + tw(d, f"{sp(dur)} s", F(58)) < 1020 else y + 68
        text(d, (vx, vy), f"{sp(dur)} s", 58, INK, anchor="lm", alpha=kb)
    # (dong Soi: so 2 260 s nam duoi thanh, ben phai)

# ---------------- canh 4: Bay - doan ngang = bep tat? ----------------
def s_trap(img, d, t, sc):
    M = sc["M"]; k1 = appear(t, M[0] - 0.1, 0.4); k2 = appear(t, M[1] - 0.1, 0.4); k3 = appear(t, M[2] - 0.1, 0.4)
    pill(d, W / 2, 290, "BẪY", 56, WHITE, RED, k1)
    if k3 > 0:
        wdt = tw(d, "SAI", F(56)) + 60
        card(d, (1030 - wdt, 248, 1030, 332), fill=A(RED, k3), r=40)
        text(d, (1030 - wdt / 2, 290), "SAI", 56, WHITE, alpha=k3)
    # nhip 1: do thi, doan ngang 100 °C to do + cau hoi
    card(d, (40, 350, 1040, 930), fill=WHITE, outline=RED, w=4)
    if k3 < 1:
        text(d, (W / 2, 420), "Đoạn ngang: bếp đã tắt?", 62, INK, alpha=k1 * (1 - k3))
        if k3 <= 0:
            plot(d, (210, 520, 950, 820), S3, hl=(0, 0, 0.5 + 0.5 * math.sin(t * 4) ** 2), pen=False, ticks=False)
    if k3 > 0:                                 # nhip 3: thay do thi bang the chot co che
        y = 460
        text(d, (W / 2, y + 40), "Bếp vẫn cấp nhiệt", 66, GREEN, alpha=k3)
        # nuoc -> hoi: phan tu thoat len
        for i in range(5):
            u = (t * 0.5 + i / 5) % 1
            x = 300 + i * 120 + 14 * math.sin(t * 2 + i); yy = 870 - u * 190
            al = k3 * clamp((1 - u) / 0.3)
            dot(d, x, yy, 18, A(BLUE, al), outline=A(WHITE, al))
            if u < 0.6: arrow(d, (x, yy - 28), (x, yy - 72), A(ORANGE, al * (1 - u / 0.6)), w=5, head=14)
        text(d, (W / 2, y + 150), "nước → hơi, t không đổi", 60, INK, alpha=k3)
    # nhip 2: hai binh cung doan soi, oat ke van 100 W, muc nuoc tut
    if k2 <= 0: return
    card(d, (40, 950, 1040, 1680), fill=A(WHITE, k2), outline=A(NAVY, k2), w=3)
    for cx, lab, lvl in ((280, "Lúc đầu", 0.46), (800, "Lúc sau", 0.46 * (1 - 0.55 * clamp((t - M[1]) / 2.5)))):
        text(d, (cx, 1010), lab, 58, INK, alpha=k2)
        text(d, (cx, 1600), "100 °C", 58, RED, alpha=k2)
        beaker(d, t, cx, 1400, 250, 250, lvl, boil=1.0, Tc=100, steam=True)
        stove(d, t, cx, 1400, 120)
    arrow(d, (480, 1270), (600, 1270), A(NAVY, k2), w=8, head=26)

# ---------------- canh 5: Tinh lambda, L + chua noi duoc ----------------
def s_calc(img, d, t, sc):
    M = sc["M"]; k = appear(t, 0.2, 0.4)
    card(d, (40, 250, 1040, 1080), fill=A(WHITE, k), outline=A(NAVY, k), w=4)
    text(d, (W / 2, 360), "λ = P·τ₁ / m", 80, BLUE, alpha=k)
    text(d, (W / 2, 490), "τ₁ = 334 s", 64, BLUE, alpha=k)
    text(d, (W / 2, 740), "L = P·τ₃ / m", 80, RED, alpha=k)
    text(d, (W / 2, 870), "τ₃ = 2 260 s", 64, RED, alpha=k)
    d.line([(90, 615), (990, 615)], fill=A(LIGHT, k), width=4)
    text(d, (W / 2, 1000), f"P = {P_W} W · m = {M_KG} kg", 58, INK, alpha=k)
    kc = appear(t, M[1] - 0.2, 0.5)
    if kc <= 0: return
    y0 = 1120 + (1 - back((t - M[1] + 0.2) / 0.5)) * 30
    card(d, (40, y0, 1040, y0 + 520), fill=WHITE, outline=PURPLE, w=6)
    pill(d, W / 2, y0 + 80, "CHƯA NÓI ĐƯỢC", 56, WHITE, PURPLE)
    text(d, (W / 2, y0 + 290), "λ, L đo > giá trị bảng", 64, INK)

# ---------------- canh 6: Thu nghi ----------------
TOFF = S2 + 900                                           # luc tat bep (giua doan soi) - chi de ve, khong co so
def s_end(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 250, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    X, Y = plot(d, (210, 360, 950, 870), TOFF, pen=False, ticks=False)
    dashed(d, (X(TOFF), Y(125)), (X(TOFF), Y(-20)), DARK_OR, w=5)
    text(d, (X(TOFF) - 26, Y(30)), "100 W", 56, INK, anchor="rm")       # oat ke truoc / sau luc tat bep
    text(d, (X(TOFF) + 26, Y(30)), "0 W", 56, DARK_OR, anchor="lm")
    kq = appear(t, 2.6, 0.4)
    if kq > 0: text(d, (X(TOFF) + 150, Y(100) + 10), "?", 130, DARK_OR, alpha=kq)
    k = appear(t, 0.3, 0.5)
    if k <= 0: return
    card(d, (50, 1040, 1030, 1680), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 1115, "THỬ NGHĨ", 56, WHITE, DARK_OR, k)
    text(d, (W / 2, 1255), "Đang sôi, tắt bếp.", 64, INK, alpha=k)
    text(d, (W / 2, 1365), "Nhiệt kế chỉ thế nào?", 64, DARK_OR, alpha=k)
    dots5(d, t, M[0] + 0.5, sc["T"] - 0.1, 1540, DARK_OR, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, ca, e = (sc[k] for k in ("hook", "do", "ans", "trap", "calc", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
           (do["t0"] + do["M"][0] + 0.3, "tap"), (do["t0"] + do["M"][1] + 0.2, "tap")]
    t = do["t0"] + do["M"][2] - 0.3
    while t < do["t0"] + do["M"][2] + 2.6: out.append((t, "tick")); t += 0.5
    out += [(an["t0"] + an["M"][0] + 0.1, "ding"), (tr["t0"] + tr["M"][0] - 0.1, "buzz"),
            (tr["t0"] + tr["M"][2] - 0.1, "tap"), (ca["t0"] + ca["M"][1] - 0.2, "tap"), (e["t0"] + 0.3, "open")]
    return out

CLIP = dict(id="tn-l12-thuchanh-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Thực hành đo λ và L · thachlab.id.vn", scenes=[
 dict(key="hook", title="Đun đá tới cạn", draw=s_hook, tail=0.3, caps=[
   ("Bếp giữ 100 W suốt.", 2.6),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   "Đá tan: nhiệt kế đứng ở 0 °C.",
   "Hết đá: nhiệt độ tăng đều.",
   "Sôi: lại đứng yên, nước cạn dần."]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.3, caps=[
   ("Đoạn ngang 100 °C dài nhất.", 3.0),
   ("Gấp khoảng 5,4 lần nóng lên.", 3.2)]),
 dict(key="trap", title="Bẫy", draw=s_trap, tail=0.3, caps=[
   ("Đúng hay sai?", 3.1),
   ("Oát kế vẫn chỉ 100 W.", 3.4),
   ("Nhiệt dùng để đổi thể.", 3.2)]),
 dict(key="calc", title="Tính λ và L", draw=s_calc, tail=0.3, caps=[
   ("Cùng công thức P·τ/m.", 3.0),
   ("Thực tế còn mất nhiệt.", 3.0)]),
 dict(key="end", title="Thử nghĩ", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự trả lời.", 5.0)]),
])
