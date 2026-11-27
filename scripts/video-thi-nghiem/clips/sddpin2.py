# Clip: tn-l11-do-sdd-pin-02 - Lap lai phep do voi pin moi cung loai: so sanh pin moi va pin cu.
# So lieu lay nguyen tu kho:
#   pin moi (tn-l11-do-sdd-pin-02.so_lieu_mau, Rx Ohm, I A, U V): 100 0,015 1,58 ; 20 0,073 1,56 ; 10 0,129 1,55 ;
#     5 0,217 1,53 ; 2 0,372 1,49 ; 0 0,701 1,40. Duong ke qua (0; 1,58) va (0,500; 1,45).
#   pin cu (tn-l11-do-sdd-pin-01.so_lieu_mau): 100 0,014 1,48 ; ... ; 0 0,534 1,06. Duong qua (0; 1,50) va (0,500; 1,09).
# Ban 1 (31/10/2026). Ban 2 (27/11/2026, cong moi lo L11b): chu ve >= 56 px, <= 180 tu/phut moi canh, nhip >= 2 s,
#   K10 (khong nut A-D, "Dung lai, tu doan."), dem 5 o, the CHUA NOI DUOC >= 4 s, nhip Bay >= 3 s.
# Du doan MOI (hop exp truoc video da ke 6 cap so + "duong thoai hon han" nen bo ca cu):
#   K mo: pin moi 1,58 V, pin cu 1,50 V (chenh 0,08 V). Dong K, Rx = 0: hai pin chenh hon hay kem 0,08 V?
#   -> hon han: 1,40 - 1,06 = 0,34 V. Hop exp khong neu phep so nay.
#   KHONG hien r (0,26 / 0,82) va cac so o I = 0,5 A: hop "Dien buoc con thieu" ngay sau video hoi dung cac so do.
# Bay = hien_tuong_hay_sai[1]: do ho mach la du biet pin con tot. Khong dung cap so cua Du doan.
# CHUA NOI DUOC: trong pin, dieu gi lam r tang? (bai muc VI)
# THU NGHI (= cau_chot khung, sai_so_thuong_gap kho): tinh r pin moi chi tu 2 lan do Rx = 100 va 20 Ohm co tin duoc?
#   -> khong: U chi chenh 0,02 V, co sai so von ke +-0,01 V. Man chot khong cong thuc, khong goi y.
from engine import *

NEW = [(100, 0.015, 1.58), (20, 0.073, 1.56), (10, 0.129, 1.55), (5, 0.217, 1.53), (2, 0.372, 1.49), (0, 0.701, 1.40)]
OLD = [(100, 0.014, 1.48), (20, 0.066, 1.44), (10, 0.117, 1.40), (5, 0.191, 1.35), (2, 0.311, 1.25), (0, 0.534, 1.06)]
E_NEW, R_NEW, E_OLD, R_OLD, R0 = 1.58, 0.26, 1.50, 0.82, 2.0
ROWS = NEW

def _kiem_so():
    import json, os
    base = os.path.join(HERE, "..", "..", "content", "thi-nghiem")
    k2 = json.load(open(os.path.join(base, "tn-l11-do-sdd-pin-02.json")))
    k1 = json.load(open(os.path.join(base, "tn-l11-do-sdd-pin-01.json")))
    assert [tuple(r) for r in k2["so_lieu_mau"]["hang"]] == NEW
    assert [tuple(r) for r in k1["so_lieu_mau"]["hang"]] == OLD
    assert round(E_NEW - E_OLD, 2) == 0.08 and round(NEW[-1][2] - OLD[-1][2], 2) == 0.34
    assert round(NEW[0][2] - NEW[1][2], 2) == 0.02
    for rx, i, u in NEW:
        assert abs(E_NEW / (R0 + rx + 0.25) - i) <= 0.003 and abs(E_NEW - i * 0.25 - u) <= 0.015, rx
_kiem_so()

def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
FS = 58
WIRE = (60, 66, 92); SCR = (220, 240, 225); SCR_INK = (20, 60, 30); BODY = (70, 78, 100)
DGREEN = (21, 110, 55); DRED = (185, 28, 28); DORANGE = (176, 64, 8); HL = (255, 237, 213)

_SX = "/System/Library/Fonts/Supplemental/STIXGeneralBolIta.otf"; _sc = {}
def FX(size):
    if size not in _sc: _sc[size] = ImageFont.truetype(_SX, int(size))
    return _sc[size]
def mt(d, xy, s, size, color=INK, alpha=1.0, anchor="m"):
    parts = [p for p in re.split(r"(ℰ)", s) if p]
    fs = [FX(size * 1.12) if p == "ℰ" else F(size) for p in parts]
    tot = sum(tw(d, p, f) for p, f in zip(parts, fs))
    x = xy[0] - tot / 2 if anchor == "m" else xy[0]; yb = xy[1] + size * 0.36
    for p, f in zip(parts, fs):
        dtext(d, (x, yb), p, f, color, alpha, "ls"); x += tw(d, p, f)

def pill(d, cx, cy, s, fill, alpha=1.0, size=FS, fg=WHITE):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, fg, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(LIGHT, a), r=18, w=4)

# ---------------- mach: pin trai, ampe ke tren, Rx phai, R0 + K duoi, von ke o hai cuc pin ----------------
XL, XR, YT, YB = 150, 930, 330, 760
AM = (630, YT, 300)
VM = (370, 545, 270)
RB = (840, 430, 1020, 650)
R0B = (660, YB - 32, 800, YB + 32)
KP, KC = (430, YB), (540, YB)
LOOP = [(XL, 520), (XL, YT), (XR, YT), (XR, YB), (XL, YB), (XL, 580)]

def meter(d, c, reading):
    cx, cy, w = c
    card(d, (cx - w / 2, cy - 58, cx + w / 2, cy + 58), fill=BODY, r=18)
    card(d, (cx - w / 2 + 14, cy - 44, cx + w / 2 - 14, cy + 44), fill=SCR, r=10)
    text(d, (cx, cy), reading, FS, SCR_INK)

def _along(s):
    segs = list(zip(LOOP, LOOP[1:])); tot = sum(math.dist(a, b) for a, b in segs); s %= tot
    for a, b in segs:
        L = math.dist(a, b)
        if s <= L: return (a[0] + (b[0] - a[0]) * s / L, a[1] + (b[1] - a[1]) * s / L)
        s -= L
    return LOOP[-1]

def circuit(d, t, rx, closed, I=0.0, U=1.58):
    w = 8
    d.line([(XL, 520), (XL, YT), (AM[0] - AM[2] / 2, YT)], fill=WIRE, width=w, joint="curve")
    d.line([(AM[0] + AM[2] / 2, YT), (XR, YT), (XR, RB[1])], fill=WIRE, width=w, joint="curve")
    d.line([(XR, RB[3]), (XR, YB), (R0B[2], YB)], fill=WIRE, width=w, joint="curve")
    d.line([(R0B[0], YB), (KC[0], YB)], fill=WIRE, width=w)
    d.line([(KP[0], YB), (XL, YB), (XL, 580)], fill=WIRE, width=w, joint="curve")
    d.line([(VM[0], YT), (VM[0], VM[1] - 58)], fill=WIRE, width=w); d.line([(VM[0], VM[1] + 58), (VM[0], YB)], fill=WIRE, width=w)
    for y in (YT, YB): dot(d, VM[0], y, 13, WIRE)
    d.line([(XL - 52, 535), (XL + 52, 535)], fill=NAVY, width=7)
    d.line([(XL - 27, 567), (XL + 27, 567)], fill=NAVY, width=16)
    text(d, (XL - 82, 495), "+", 62, RED); text(d, (XL - 82, 610), "−", 66, INK)
    text(d, (XL + 10, YB + 62), "pin mới", FS, INK)
    card(d, RB, fill=BODY, r=16)
    card(d, (RB[0] + 10, 525, RB[2] - 10, 635), fill=SCR, r=10)
    text(d, ((RB[0] + RB[2]) / 2, 580), f"{rx} Ω", 56, SCR_INK)
    text(d, ((RB[0] + RB[2]) / 2, 476), "Rx", FS, WHITE)
    d.rectangle(R0B, fill=WHITE, outline=NAVY, width=5)
    text(d, ((R0B[0] + R0B[2]) / 2, YB + 80), "R0 = 2 Ω", 56, NAVY)
    dot(d, KP[0], KP[1], 12, WIRE); dot(d, KC[0], KC[1], 12, WHITE, outline=WIRE)
    ang = 0.0 if closed else math.radians(-32); L = KC[0] - KP[0]
    d.line([KP, (KP[0] + L * math.cos(ang), KP[1] + L * math.sin(ang))], fill=WIRE, width=9)
    text(d, (485, YB + 62), "K", FS, INK)
    meter(d, AM, vn(I, 3) + " A" if closed else "0,000 A")
    meter(d, VM, vn(U) + " V" if closed else vn(E_NEW) + " V")
    if closed:
        sp = 90 + 500 * I
        for k in range(22):
            x, y = _along(k * 105 + t * sp)
            if abs(x - AM[0]) < AM[2] / 2 + 8 and abs(y - YT) < 70: continue
            if RB[0] - 8 < x < RB[2] + 8 and RB[1] - 8 < y < RB[3] + 8: continue
            if XL - 60 < x < XL + 60 and 515 < y < 590: continue
            dot(d, x, y, 12, ORANGE)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    circuit(d, t, 0, False)
    k0 = 1.0
    card(d, (60, 880, 1020, 975), fill=A(HL, k0), r=20)
    text(d, (W / 2, 928), "Pin cũ, K mở: 1,50 V", 58, INK, alpha=k0)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1025 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 560), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, k)
    text(d, (W / 2, y0 + 185), "Đóng K, để Rx = 0 Ω.", 62, INK, alpha=k)
    text(d, (W / 2, y0 + 285), "Hai pin chênh nhau", 64, PURPLE, alpha=k)
    text(d, (W / 2, y0 + 370), "hơn hay kém 0,08 V?", 64, PURPLE, alpha=k)
    seg_bar(d, y0 + 450, t, M[1], sc["T"] - 0.2, PURPLE, k)

# ---------------- canh 2: Tien hanh (6 lan do pin moi) ----------------
T_S = [0.7, 2.1, 3.5, 4.9, 6.3, 7.7]
T_ON, T_RX = 0.9, 0.4
def do_state(t):
    n_rx = sum(1 for ts in T_S if t >= ts - T_RX - 1e-9)
    rx = ROWS[max(0, n_rx - 1)][0]
    n = sum(1 for ts in T_S if t >= ts - 1e-9)
    k = n - 1
    closed = k >= 0 and (t < T_S[k] + T_ON - 1e-9 or k == len(T_S) - 1)
    return closed, rx, n, k

TX = [150, 390, 630, 880]; TY0, RH = 930, 92
def table(d, n, k_on, kd):
    card(d, (40, 878, 1040, TY0 + 50 + 6 * RH + 14), fill=WHITE, outline=LIGHT, w=4)
    for x, s in zip(TX[:3], ("Rx (Ω)", "I (A)", "U mới")): text(d, (x, TY0), s, 56, INK)
    if kd > 0: text(d, (TX[3], TY0), "U cũ", 56, DRED, alpha=kd)
    d.line([(60, TY0 + 42), (1020, TY0 + 42)], fill=LIGHT, width=4)
    for j in range(n):
        y = TY0 + 50 + RH * j + RH / 2
        if j == k_on or (kd > 0 and j == 5): d.rounded_rectangle([60, y - 42, 1020, y + 42], radius=16, fill=HL)
        rx, i, u = ROWS[j]
        text(d, (TX[0], y), str(rx), 56, NAVY); text(d, (TX[1], y), vn(i, 3), 56, INK); text(d, (TX[2], y), vn(u), 56, BLUE)
        if kd > 0: text(d, (TX[3], y), vn(OLD[j][2]), 56, DRED, alpha=kd)

def s_do(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    closed, rx, n, k = do_state(t)
    if closed:
        _, i, u = ROWS[k]; circuit(d, t, rx, True, i, u)
    else: circuit(d, t, rx, False)
    table(d, n, k if closed else -1, appear(t, M[2], 0.45))

# ---------------- canh 3: Rut ra (hai duong U-I) ----------------
GX0, GX1, GY0, GY1 = 230, 950, 1480, 880          # I 0-0,8 A ; U 1,0-1,6 V (ngat truc)
UMIN, UMAX = 1.0, 1.6
def gx(i): return GX0 + i / 0.8 * (GX1 - GX0)
GU = GY0 - 70
def gy(u): return GU - (u - UMIN) / (UMAX - UMIN) * (GU - GY1)
def u_new(i): return E_NEW - R_NEW * i
def u_old(i): return E_OLD - R_OLD * i

def axes(d):
    card(d, (40, 780, 1040, 1590), fill=WHITE, outline=LIGHT, w=4)
    for u in (1.1, 1.3, 1.5):
        d.line([(GX0, gy(u)), (GX1, gy(u))], fill=LIGHT, width=3)
        text(d, (GX0 - 18, gy(u)), vn(u, 1), 56, INK, anchor="rm")
    d.line([(GX0, GY0), (GX1 + 10, GY0)], fill=NAVY, width=5)
    d.line([(GX0, GY0), (GX0, GY0 - 22)], fill=NAVY, width=5); d.line([(GX0, GY0 - 44), (GX0, GY1 - 10)], fill=NAVY, width=5)
    for yy in (GY0 - 18, GY0 - 40):
        d.line([(GX0 - 22, yy + 8), (GX0 + 22, yy - 8)], fill=NAVY, width=5)
    d.polygon([(GX1 + 26, GY0), (GX1 + 8, GY0 - 10), (GX1 + 8, GY0 + 10)], fill=NAVY)
    d.polygon([(GX0, GY1 - 26), (GX0 - 10, GY1 - 8), (GX0 + 10, GY1 - 8)], fill=NAVY)
    text(d, (GX0 + 24, GY1 - 30), "U (V)", 56, INK, anchor="lm")
    for i in (0.2, 0.4, 0.6):
        d.line([(gx(i), GY0), (gx(i), GY0 + 12)], fill=NAVY, width=4)
        text(d, (gx(i), GY0 + 48), vn(i, 1), 56, INK)
    text(d, (GX1 - 20, GY0 - 40), "I (A)", 56, INK, anchor="rm")

def s_rut(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    axes(d)
    for _, i, u in OLD: dot(d, gx(i), gy(u), 12, DRED, outline=WHITE)
    d.line([(gx(0.014), gy(u_old(0.014))), (gx(0.55), gy(u_old(0.55)))], fill=A(DRED, 0.8), width=6)
    text(d, (gx(0.55) + 20, gy(u_old(0.55)) - 10), "pin cũ", 56, DRED, anchor="lm")
    kp = clamp((t - 0.3) / 1.5)
    for j, (_, i, u) in enumerate(NEW):
        if kp * 6 > j: dot(d, gx(i), gy(u), 14, BLUE, outline=WHITE)
    kl = clamp((t - 2.0) / 0.9)
    if kl > 0:
        i1 = 0.015 + (0.75 - 0.015) * ease(kl)
        d.line([(gx(0.015), gy(u_new(0.015))), (gx(i1), gy(u_new(i1)))], fill=A(BLUE, 0.85), width=6)
        pass
    k1 = appear(t, 0.2, 0.45)
    text(d, (gx(0.52), gy(u_new(0.52)) - 80), "pin mới", 56, BLUE, alpha=k1)
    card(d, (50, 260, 1030, 480), fill=A(WHITE, k1), outline=A(BLUE, k1), w=6)
    text(d, (W / 2, 330), "Cùng mạch, cùng 6 nấc", 62, INK, alpha=k1)
    text(d, (W / 2, 415), "pin mới thoải hơn hẳn", 62, BLUE, alpha=k1)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        ke = clamp((t - M[1] + 0.1) / 0.6)
        for f, i0 in ((u_new, 0.015), (u_old, 0.014)):
            d.line([(gx(i0 * (1 - ke)), gy(f(i0 * (1 - ke)))), (gx(i0), gy(f(i0)))], fill=ORANGE, width=8)
        rr = 40 + 22 * math.sin(3.0 * t)
        for u in (E_NEW, E_OLD):
            d.ellipse([GX0 - rr, gy(u) - rr, GX0 + rr, gy(u) + rr], outline=A(ORANGE, k2), width=5)
            dot(d, GX0, gy(u), 14, A(ORANGE, k2), outline=WHITE)
        card(d, (50, 540, 1030, 720), fill=A(WHITE, k2), outline=A(ORANGE, k2), w=6)
        mt(d, (W / 2, 630), "Cắt trục U: 1,58 V và 1,50 V", 60, DORANGE, k2)

# ---------------- canh 4: Bay - do ho mach la du + CHUA NOI DUOC ----------------
B2 = 3.4
def open_rig(d, t, a, kk):
    cx, y0 = 540, 760                                  # pin + von ke, K mo, khong dong
    d.line([(cx - 200, y0), (cx - 200, y0 + 110)], fill=A(WIRE, a), width=7)
    d.line([(cx - 200, y0 + 150), (cx - 200, y0 + 260)], fill=A(WIRE, a), width=7)
    d.line([(cx - 256, y0 + 110), (cx - 144, y0 + 110)], fill=A(NAVY, a), width=7)
    d.line([(cx - 228, y0 + 150), (cx - 172, y0 + 150)], fill=A(NAVY, a), width=16)
    d.line([(cx - 200, y0), (cx + 200, y0), (cx + 200, y0 + 70)], fill=A(WIRE, a), width=7, joint="curve")
    d.line([(cx + 200, y0 + 190), (cx + 200, y0 + 260), (cx - 200, y0 + 260)], fill=A(WIRE, a), width=7, joint="curve")
    d.ellipse([cx + 140, y0 + 70, cx + 260, y0 + 190], fill=A(WHITE, a), outline=A(NAVY, a), width=6)
    text(d, (cx + 200, y0 + 130), "V", 60, NAVY, alpha=a)
    text(d, (cx - 60, y0 + 130), "pin", FS, INK, alpha=a)
    if kk > 0:
        rr = 70 + 28 * math.sin(3.2 * t)
        d.ellipse([cx - 200 - rr, y0 + 130 - rr, cx - 200 + rr, y0 + 130 + rr], outline=A(DRED, kk), width=6)
        text(d, (W / 2, y0 + 360), "I = 0: chưa lộ r", 62, DRED, alpha=kk)

def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    k3 = appear(t, M[2] - 0.2, 0.45)
    a1 = appear(t, 0.0, 0.3) * (1 - k3)
    if a1 > 0:
        card(d, (40, 250, 1040, 1240), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, W / 2, 320, "BẪY", DRED, a1)
        q = ("Đo hở mạch là đủ", "biết pin còn tốt")
        for yy, s in zip((470, 560), q): text(d, (W / 2, yy), s, 64, DRED, alpha=a1)
        ks = clamp((t - B2) / 0.5)
        if ks > 0:
            for yy, s in zip((474, 564), q):
                lw = tw(d, s, F(64))
                d.line([(W / 2 - lw / 2 - 6, yy), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy)], fill=A(DRED, 0.85 * a1), width=5)
        open_rig(d, t, a1, appear(t, B2, 0.4) * a1)
    if k3 > 0:
        card(d, (40, 300, 1040, 840), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 380, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 540), "Trong pin, điều gì", 62, INK, alpha=k3)
        text(d, (W / 2, 640), "làm r tăng dần?", 62, INK, alpha=k3)
        # pin to + dau hoi nhip
        px, py = 540, 1150
        card(d, (px - 120, py - 220, px + 120, py + 220), fill=A(WHITE, k3), outline=A(NAVY, k3), r=30, w=8)
        card(d, (px - 50, py - 260, px + 50, py - 220), fill=A(NAVY, k3), r=10)
        rr = 70 + 26 * math.sin(3.0 * t)
        d.ellipse([px - rr, py - rr, px + rr, py + rr], outline=A(DRED, k3), width=6)
        text(d, (px, py), "?", 90, DRED, alpha=k3)

# ---------------- canh 5: THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 310, "THỬ NGHĨ", ORANGE, k)
    for x, s in zip(TX[:3], ("Rx (Ω)", "I (A)", "U (V)")): text(d, (x, 450), s, 56, INK, alpha=k)
    for j in (0, 1):
        y = 545 + 92 * j; rx, i, u = NEW[j]
        text(d, (TX[0], y), str(rx), 56, NAVY, alpha=k); text(d, (TX[1], y), vn(i, 3), 56, INK, alpha=k)
        text(d, (TX[2], y), vn(u), 56, BLUE, alpha=k)
    text(d, (W / 2, 820), "Tính r pin mới chỉ từ", 64, INK, alpha=k)
    text(d, (W / 2, 910), "hai lần đo này.", 64, INK, alpha=k)
    text(d, (W / 2, 1040), "Có tin được không?", 66, DORANGE, alpha=k)
    seg_bar(d, 1250, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = (sc[x] for x in ("hook", "do", "rut", "bay", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding")]
    out += [(do["t0"] + ts, "tick") for ts in T_S] + [(do["t0"] + do["M"][2], "ding")]
    out += [(r["t0"] + r["M"][1], "tap"), (b["t0"] + 0.3, "buzz"), (e["t0"] + 0.15, "open")]
    return out

def _kiem_dong_bo():
    bad = []; t = 0.0
    while t < 12.0:
        closed, rx, n, k = do_state(t)
        if closed and (k != n - 1 or rx != ROWS[k][0]): bad.append((round(t, 2), "dong"))
        t += 0.05
    return bad

CLIP = dict(id="tn-l11-do-sdd-pin-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Đo suất điện động · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Pin mới, cùng mạch", draw=s_hook, tail=0.3, caps=[
   ("Thay pin mới, giữ nguyên mạch.", 3.6),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Sáu nấc Rx như lần trước.", 4.2),
   ("Ghi I và U từng nấc.", 4.0),
   ("Đáp án: chênh 0,34 V, hơn hẳn.", 3.8)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.3, caps=[
   ("Chấm cạnh đường pin cũ.", 3.4),
   ("Kéo dài tới trục U.", 4.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Hở mạch: không có dòng.", 3.2),
   ("Vôn kế chưa thấy r.", 3.2),
   ("Còn một chỗ chưa rõ.", 4.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 6.5)]),
])

if __name__ == "__main__":
    print("lệch đồng bộ:", _kiem_dong_bo() or "không")
