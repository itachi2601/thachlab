# Clip: tn-l11-do-sdd-pin-01 - Do E, r cua pin cu bang bien tro, von ke, ampe ke.
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-do-sdd-pin-01.json -> so_lieu_mau (Rx Ohm, I A, U V):
#   100 0,014 1,48 ; 20 0,066 1,44 ; 10 0,117 1,40 ; 5 0,191 1,35 ; 2 0,311 1,25 ; 0 0,534 1,06.
#   Mo hinh E = 1,50 V, r = 0,80 Ohm, R0 = 2,0 Ohm. Duong ke qua (0; 1,50) va (0,500; 1,09) (ghi_chu kho).
# Ban 1 (16/11/2026). Ban 2 (27/11/2026, cong moi lo L11b): chu ve >= 56 px, <= 180 tu/phut moi canh, nhip >= 2 s,
#   K10 (khong nut A-D, phu de "Dung lai, tu doan."), thanh dem 5 o, the CHUA NOI DUOC >= 4 s, nhip Bay >= 3 s.
# Du doan (giu ca cu): giam Rx qua tung nac, von ke tut the nao? -> it luc dau, manh o may nac cuoi
#   (hieu U tung nac 0,04 0,04 0,05 0,10 0,19 - tinh tu bang). Hop exp trong bai chi bao "so muc U tut", khong neu ket qua.
#   KHONG hien gia tri r (Tu kiem tra muc II hoi r = 0,8 Ohm tu duong thang).
# Bay = hien_tuong_hay_sai[3]: mac ampe ke song song hai cuc pin (doan mach).
# CHUA NOI DUOC: dong lon hon 0,53 A, cac diem con thang hang?
# THU NGHI (= cau_chot khung, ca tu suy ghi trong kho): giu pin cu, R0 = 2 -> 5 Ohm: duong U-I TRUNG duong cu
#   (E, r cua pin khong doi), chi cac diem don ve I <= 1,5/5,8 = 0,26 A. Man chot khong co cong thuc, khong goi y.
# Mach: (+) pin -> ampe ke -> Rx -> R0 -> K -> (-) pin; von ke SONG SONG hai cuc pin. Chieu dong quy uoc: tu (+) di len,
#   sang phai qua ampe ke, xuong qua Rx, sang trai o day duoi, ve (-).
from engine import *

ROWS = [(100, 0.014, 1.48), (20, 0.066, 1.44), (10, 0.117, 1.40), (5, 0.191, 1.35), (2, 0.311, 1.25), (0, 0.534, 1.06)]
E0, R_IN, R0 = 1.50, 0.80, 2.0
LINE_P2 = (0.500, 1.09)
DROPS = [round(ROWS[k - 1][2] - ROWS[k][2], 2) for k in range(1, 6)]   # 0,04 0,04 0,05 0,10 0,19
SLOPE = (E0 - LINE_P2[1]) / LINE_P2[0]                                # chi de ve, KHONG ghi so

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-do-sdd-pin-01.json")))
    assert [tuple(r) for r in k["so_lieu_mau"]["hang"]] == ROWS
    ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert ts["R0"]["gia_tri"] == R0 and ts["E"]["mac_dinh"] == E0
    for rx, i, u in ROWS:
        assert abs(E0 / (R0 + rx + R_IN) - i) <= 0.003 and abs(E0 - i * R_IN - u) <= 0.015, rx
    assert DROPS == [0.04, 0.04, 0.05, 0.10, 0.19] and all(DROPS[j + 1] >= DROPS[j] for j in range(4))
    assert abs(SLOPE - 0.82) < 0.005 and abs(E0 / (5.0 + R_IN) - 0.259) < 0.001
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

def circuit(d, t, rx, closed, I=0.0, U=E0):
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
    text(d, (XL + 10, YB + 62), "pin cũ", FS, INK)
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
    meter(d, VM, vn(U) + " V" if closed else vn(E0) + " V")
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
    circuit(d, t, 100, False)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1000 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 560), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, k)
    text(d, (W / 2, y0 + 185), "Giảm Rx từng nấc về 0 Ω.", 62, INK, alpha=k)
    text(d, (W / 2, y0 + 285), "Mỗi nấc vôn kế tụt", 64, PURPLE, alpha=k)
    text(d, (W / 2, y0 + 370), "đều hay không đều?", 64, PURPLE, alpha=k)
    seg_bar(d, y0 + 450, t, M[1], sc["T"] - 0.2, PURPLE, k)

# ---------------- canh 2: Tien hanh (6 lan do) ----------------
T_S = [0.7, 2.1, 3.5, 4.9, 6.3, 7.7]   # dong K o lan do k ; doi Rx truoc 0,4 s (K mo) ; ngat K sau 0,9 s
T_ON, T_RX = 0.9, 0.4
def do_state(t):
    n_rx = sum(1 for ts in T_S if t >= ts - T_RX - 1e-9)
    rx = ROWS[max(0, n_rx - 1)][0]
    n = sum(1 for ts in T_S if t >= ts - 1e-9)
    k = n - 1
    closed = k >= 0 and (t < T_S[k] + T_ON - 1e-9 or k == len(T_S) - 1)
    return closed, rx, n, k

TX = [170, 420, 650, 880]; TY0, RH = 930, 92
def table(d, n, k_on, kd):
    card(d, (40, 878, 1040, TY0 + 50 + 6 * RH + 14), fill=WHITE, outline=LIGHT, w=4)
    for x, s in zip(TX[:3], ("Rx (Ω)", "I (A)", "U (V)")): text(d, (x, TY0), s, 56, INK)
    if kd > 0: text(d, (TX[3], TY0), "U tụt", 56, DRED, alpha=kd)
    d.line([(60, TY0 + 42), (1020, TY0 + 42)], fill=LIGHT, width=4)
    for j in range(n):
        y = TY0 + 50 + RH * j + RH / 2
        if j == k_on: d.rounded_rectangle([60, y - 42, 1020, y + 42], radius=16, fill=HL)
        rx, i, u = ROWS[j]
        text(d, (TX[0], y), str(rx), 56, NAVY); text(d, (TX[1], y), vn(i, 3), 56, INK); text(d, (TX[2], y), vn(u), 56, INK)
        if j >= 1 and kd > 0:
            text(d, (TX[3], y - RH / 2), "−" + vn(DROPS[j - 1]), 56, DRED if j >= 4 else INK, alpha=kd)

def s_do(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    closed, rx, n, k = do_state(t)
    if closed:
        _, i, u = ROWS[k]; circuit(d, t, rx, True, i, u)
    else: circuit(d, t, rx, False)
    table(d, n, k if closed else -1, appear(t, M[2], 0.45))

# ---------------- canh 3: Rut ra (do thi U-I) ----------------
GX0, GX1, GY0, GY1 = 230, 950, 1480, 880          # I 0-0,6 A ; U 1,0-1,6 V (ngat truc)
UMIN, UMAX = 1.0, 1.6
def gx(i): return GX0 + i / 0.6 * (GX1 - GX0)
GU = GY0 - 70
def gy(u): return GU - (u - UMIN) / (UMAX - UMIN) * (GU - GY1)

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
    for i in (0.2, 0.4):
        d.line([(gx(i), GY0), (gx(i), GY0 + 12)], fill=NAVY, width=4)
        text(d, (gx(i), GY0 + 48), vn(i, 1), 56, INK)
    text(d, (GX1 - 40, GY0 + 48), "I (A)", 56, INK)

def s_rut(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    axes(d)
    kp = clamp(t / 1.5)
    for j, (_, i, u) in enumerate(ROWS):
        if kp * 6 > j: dot(d, gx(i), gy(u), 14, BLUE, outline=WHITE)
    kl = clamp((t - 1.8) / 0.9)
    if kl > 0:
        i1 = 0.58 * ease(kl)
        d.line([(gx(0.014), gy(E0 - SLOPE * 0.014)), (gx(i1), gy(E0 - SLOPE * i1))], fill=A(BLUE, 0.85), width=6)
    k1 = appear(t, 0.2, 0.45)
    card(d, (50, 260, 1030, 480), fill=A(WHITE, k1), outline=A(BLUE, k1), w=6)
    text(d, (W / 2, 330), "U theo I: sáu điểm", 62, BLUE, alpha=k1)
    text(d, (W / 2, 415), "gần một đường thẳng", 62, BLUE, alpha=k1)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        ke = clamp((t - M[1] + 0.1) / 0.6)
        i_a = 0.014 * (1 - ke)
        d.line([(gx(i_a), gy(E0 - SLOPE * i_a)), (gx(0.014), gy(E0 - SLOPE * 0.014))], fill=ORANGE, width=8)
        ii = 0.55 * (1 - ((t - M[1]) * 0.35) % 1.0)          # cham cam chay doc duong ve phia truc U
        if t > M[1]: dot(d, gx(ii), gy(E0 - SLOPE * ii), 20, ORANGE, outline=WHITE)
        rr = 45 + 25 * math.sin(3.0 * t)
        d.ellipse([GX0 - rr, gy(E0) - rr, GX0 + rr, gy(E0) + rr], outline=A(ORANGE, k2), width=5)
        dot(d, GX0, gy(E0), 16, A(ORANGE, k2), outline=WHITE)
        card(d, (50, 540, 1030, 720), fill=A(WHITE, k2), outline=A(ORANGE, k2), w=6)
        mt(d, (W / 2, 630), "Cắt trục U: ℰ ≈ 1,50 V", 62, DORANGE, k2)

# ---------------- canh 4: Bay - mac ampe ke song song hai cuc pin + CHUA NOI DUOC ----------------
B2 = 3.4
def wrong(d, t, a2, kk):
    cx, y0 = 540, 640
    d.line([(cx - 260, y0 + 60), (cx - 260, y0 + 175)], fill=A(WIRE, a2), width=7)
    d.line([(cx - 260, y0 + 215), (cx - 260, y0 + 330)], fill=A(WIRE, a2), width=7)
    d.line([(cx - 260, y0 + 60), (cx + 220, y0 + 60), (cx + 220, y0 + 135)], fill=A(WIRE, a2), width=7, joint="curve")
    d.line([(cx + 220, y0 + 255), (cx + 220, y0 + 330), (cx - 260, y0 + 330)], fill=A(WIRE, a2), width=7, joint="curve")
    d.line([(cx - 316, y0 + 175), (cx - 204, y0 + 175)], fill=A(NAVY, a2), width=7)
    d.line([(cx - 288, y0 + 215), (cx - 232, y0 + 215)], fill=A(NAVY, a2), width=16)
    text(d, (cx - 120, y0 + 195), "pin", FS, INK, alpha=a2)
    d.ellipse([cx + 160, y0 + 135, cx + 280, y0 + 255], fill=A(WHITE, a2), outline=A(BLUE, a2), width=6)
    text(d, (cx + 220, y0 + 197), "A", 60, BLUE, alpha=a2)
    if kk > 0:
        for k in range(10):                                   # dong vot: hat chay nhanh vong pin - ampe ke
            s = (k * 130 + t * 900) % 1300
            pts = [(cx - 260, y0 + 175), (cx - 260, y0 + 60), (cx + 220, y0 + 60), (cx + 220, y0 + 330),
                   (cx - 260, y0 + 330), (cx - 260, y0 + 215)]
            rem = s
            for p, q in zip(pts, pts[1:]):
                L = math.dist(p, q)
                if rem <= L: dot(d, p[0] + (q[0] - p[0]) * rem / L, p[1] + (q[1] - p[1]) * rem / L, 13, A(RED, kk)); break
                rem -= L
        text(d, (cx - 20, y0 + 400), "dòng vọt", FS, DRED, alpha=kk)

def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    k3 = appear(t, M[2] - 0.2, 0.45)
    a1 = appear(t, 0.0, 0.3) * (1 - k3)
    if a1 > 0:
        card(d, (40, 250, 1040, 1240), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, W / 2, 320, "BẪY", DRED, a1)
        q1 = "Ampe kế song song pin"
        text(d, (W / 2, 470), q1, 64, DRED, alpha=a1)
        kk = appear(t, B2, 0.4) * a1
        ks = clamp((t - B2) / 0.5)
        if ks > 0:
            for yy, s in ((474, q1),):
                lw = tw(d, s, F(64))
                d.line([(W / 2 - lw / 2 - 6, yy), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy)], fill=A(DRED, 0.85 * a1), width=5)
        wrong(d, t, a1, kk)
    if k3 > 0:
        card(d, (40, 300, 1040, 840), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 380, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 540), "Dòng lớn hơn 0,53 A,", 62, INK, alpha=k3)
        text(d, (W / 2, 640), "điểm còn thẳng hàng?", 62, INK, alpha=k3)
        # do thi mo: 6 diem + dau hoi o phia I lon (chuyen dong nhe)
        bx0, by0 = 160, 1450
        d.line([(bx0, by0), (940, by0)], fill=A(NAVY, k3), width=5); d.line([(bx0, by0), (bx0, 960)], fill=A(NAVY, k3), width=5)
        for j, (_, i, u) in enumerate(ROWS):
            dot(d, bx0 + i * 900, by0 - (u - 0.9) * 700, 13, A(BLUE, k3))
        qx, qy = bx0 + 0.70 * 900, by0 - 0.05 * 700 - 120
        rr = 80 + 30 * math.sin(3.0 * t)
        d.ellipse([qx - rr, qy - rr, qx + rr, qy + rr], outline=A(DRED, k3), width=6)
        text(d, (qx, qy), "?", 90, DRED, alpha=k3)

# ---------------- canh 5: THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 310, "THỬ NGHĨ", ORANGE, k)
    for cx, lab, col in ((330, "2 Ω", INK), (750, "5 Ω", DORANGE)):
        d.rectangle([cx - 90, 470, cx + 90, 540], fill=A(WHITE, k), outline=A(NAVY, k), width=5)
        text(d, (cx, 505), lab, 58, col, alpha=k)
    text(d, (540, 505), "→", 62, INK, alpha=k)
    text(d, (W / 2, 640), "R0", 62, NAVY, alpha=k)
    text(d, (W / 2, 820), "Vẫn pin cũ, đổi R0", 64, INK, alpha=k)
    text(d, (W / 2, 910), "từ 2 Ω lên 5 Ω, đo lại.", 64, INK, alpha=k)
    text(d, (W / 2, 1040), "Đường U–I đổi ra sao?", 66, DORANGE, alpha=k)
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

CLIP = dict(id="tn-l11-do-sdd-pin-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Đo suất điện động · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Pin cũ và biến trở", draw=s_hook, tail=0.3, caps=[
   ("K mở: vôn kế chỉ 1,50 V.", 3.6),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Mỗi nấc: đóng K, đọc nhanh, ngắt.", 4.4),
   ("Ghi I và U từng nấc.", 4.2),
   ("Đáp án: ít lúc đầu, mạnh ở cuối.", 3.8)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.3, caps=[
   ("Vẽ U theo I.", 3.4),
   ("Kéo dài tới trục U.", 4.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Ampe kế: điện trở rất nhỏ.", 3.2),
   ("Song song là nối tắt pin.", 3.2),
   ("Còn một chỗ chưa rõ.", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 5.8)]),
])

if __name__ == "__main__":
    print("lệch đồng bộ:", _kiem_dong_bo() or "không")
