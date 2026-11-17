# Clip: tn-l11-do-sdd-pin-01 - Do E, r cua pin cu bang bien tro, von ke, ampe ke (16/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-do-sdd-pin-01.json -> so_lieu_mau (Rx Ohm, I A, U V):
#   100 0,014 1,48 ; 20 0,066 1,44 ; 10 0,117 1,40 ; 5 0,191 1,35 ; 2 0,311 1,25 ; 0 0,534 1,06.
#   Mo hinh E = 1,50 V, r = 0,80 Ohm, R0 = 2,0 Ohm. Duong ke qua (0; 1,50) va (0,500; 1,09) (ghi_chu kho).
#   Ho mach von ke chi E = 1,50 V (hien_tuong_hay_sai[0]). Kiem tung hang: _kiem_so().
# Du doan (KHAC sddpin2 - so duong pin moi/pin cu): giam Rx qua tung nac, von ke tut THE NAO?
#   Dap an: tut it luc dau, manh o may nac cuoi (hieu U tung nac: 0,04 0,04 0,05 0,10 0,19 - tinh tu bang).
#   Rut ra: tut theo I chu khong theo Rx -> U theo I la duong thang doc xuong; giao truc U = E ~ 1,50 V.
#   KHONG hien gia tri r (Tu kiem tra muc II: cau q2 tinh r = 0,8 Ohm, q4 chon hai diem xa nhat, q3 vai tro R0).
# Bay = hien_tuong_hay_sai[3]: mac ampe ke song song hai cuc pin (doan mach). (sddpin2 dung bay [0], nguondien2 dung [1].)
# Cau hoi chot (ca tu suy, ghi trong kho): giu pin cu, thay R0 = 2 Ohm bang 5 Ohm -> duong U-I TRUNG duong cu
#   (E, r cua pin khong doi), chi cac diem don ve I <= 1,5/5,8 = 0,26 A. So moi (5 Ohm) chua tung hien.
# Bo cuc (khac sddpin2 lay do thi lam truc chinh): Tien hanh = mach + 2 dong ho + BANG Rx-I-U them cot "U tut";
#   Rut ra moi ve do thi U-I.
# Mach: pin vach dai = (+) o tren; (+) -> K -> ampe ke -> R0 -> Rx -> (-), von ke SONG SONG hai cuc pin. Moi lan do:
#   doi Rx (K mo) -> dong K (so chi + hang bang hien cung luc) -> ngat K (0,000 A ; 1,50 V). Kiem: _kiem_dong_bo().
from engine import *

ROWS = [(100, 0.014, 1.48), (20, 0.066, 1.44), (10, 0.117, 1.40), (5, 0.191, 1.35), (2, 0.311, 1.25), (0, 0.534, 1.06)]
E0, R_IN, R0 = 1.50, 0.80, 2.0
LINE_P2 = (0.500, 1.09)                               # diem thu hai cua duong ke (kho)
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
DROPS = [round(ROWS[k - 1][2] - ROWS[k][2], 2) for k in range(1, 6)]   # 0,04 0,04 0,05 0,10 0,19

WIRE = (60, 66, 92); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30); BODY = (70, 78, 100)
PINC = ORANGE; DGREEN = (10, 80, 40); HL = (255, 237, 213)

# chu "E viet tay": SF khong co glyph -> STIX Bold Italic
_SX = "/System/Library/Fonts/Supplemental/STIXGeneralBolIta.otf"; _sc = {}
def FS(size):
    if size not in _sc: _sc[size] = ImageFont.truetype(_SX, int(size))
    return _sc[size]
def mt(d, xy, s, size, color=INK, alpha=1.0, anchor="m"):
    parts = [p for p in re.split(r"(ℰ)", s) if p]
    fs = [FS(size * 1.12) if p == "ℰ" else F(size) for p in parts]
    tot = sum(tw(d, p, f) for p, f in zip(parts, fs))
    x = xy[0] - tot / 2 if anchor == "m" else xy[0]; yb = xy[1] + size * 0.36
    for p, f in zip(parts, fs):
        dtext(d, (x, yb), p, f, color, alpha, "ls"); x += tw(d, p, f)

# ---------------- mach (dich doc oy) ----------------
XL, XR = 260, 900
def circuit(d, closed, rx, oy=0, rx_q=False):
    YT, YB, YP, YN = 270 + oy, 540 + oy, 385 + oy, 425 + oy
    KX0, KX1, AX, R0X0, R0X1, VX, VY = 330, 410, 520, 640, 760, 110, 405 + oy
    NT, NB = 320 + oy, 490 + oy
    d.line([(XL, YP), (XL, YT), (KX0, YT)], fill=WIRE, width=6, joint="curve")
    d.line([(KX1, YT), (AX - 44, YT)], fill=WIRE, width=6)
    d.line([(AX + 44, YT), (R0X0, YT)], fill=WIRE, width=6)
    d.line([(R0X1, YT), (XR, YT), (XR, 335 + oy)], fill=WIRE, width=6, joint="curve")
    d.line([(XR, 475 + oy), (XR, YB), (XL, YB), (XL, YN)], fill=WIRE, width=6, joint="curve")
    d.line([(XL - 56, YP), (XL + 56, YP)], fill=PINC, width=7)                 # (+) vach dai
    d.line([(XL - 28, YN), (XL + 28, YN)], fill=PINC, width=16)                # (-) vach ngan
    text(d, (XL + 76, YP - 22), "+", 42, PINC); text(d, (XL + 76, YN + 24), "−", 42, PINC)
    text(d, (XL + 100, 405 + oy), "pin cũ", 40, MUTED, anchor="lm")
    dot(d, KX0, YT, 9, WIRE); dot(d, KX1, YT, 9, WIRE)
    if closed: d.line([(KX0, YT), (KX1, YT)], fill=NAVY, width=7)
    else: d.line([(KX0, YT), (KX0 + 80 * math.cos(math.radians(32)), YT - 80 * math.sin(math.radians(32)))], fill=NAVY, width=7)
    text(d, ((KX0 + KX1) / 2, YT + 42), "K", 40, NAVY)
    d.ellipse([AX - 44, YT - 44, AX + 44, YT + 44], fill=WHITE, outline=BLUE, width=6); text(d, (AX, YT + 2), "A", 42, BLUE)
    d.rectangle([R0X0, YT - 22, R0X1, YT + 22], fill=WHITE, outline=NAVY, width=5)
    rich(d, (R0X0 + R0X1) / 2, YT + 58, "R_{0} = 2 Ω", 50, NAVY)
    d.rectangle([XR - 24, 335 + oy, XR + 24, 475 + oy], fill=WHITE, outline=NAVY, width=5)
    arrow(d, (XR - 58, 480 + oy), (XR + 58, 330 + oy), NAVY, w=5, head=18)
    lab = "R_{x}" if rx_q else f"R_{{x}} = {rx} Ω"; dd = tw(d, "Rx" if rx_q else f"Rx = {rx} Ω", F(50))
    rich(d, XR - 60 - dd / 2, 405 + oy, lab, 50, NAVY)
    d.line([(XL, NT), (VX, NT), (VX, VY - 44)], fill=WIRE, width=5, joint="curve")
    d.line([(XL, NB), (VX, NB), (VX, VY + 44)], fill=WIRE, width=5, joint="curve")
    dot(d, XL, NT, 8, WIRE); dot(d, XL, NB, 8, WIRE)
    d.ellipse([VX - 44, VY - 44, VX + 44, VY + 44], fill=WHITE, outline=PURPLE, width=6); text(d, (VX, VY + 2), "V", 42, PURPLE)
    for p in ((XL, YT), (XR, YT), (XR, YB), (XL, YB)): dot(d, p[0], p[1], 7, WIRE)
    if closed:   # chieu dong quy uoc: (+) tren -> K -> A -> R0 -> Rx -> day duoi chay sang TRAI -> (-)
        arrow(d, (660, YB - 32), (580, YB - 32), RED, w=7, head=20)
        text(d, (680, YB - 32), "I", 40, RED, anchor="lm")

def readout(d, x0, y0, label, reading):
    card(d, (x0, y0, x0 + 440, y0 + 126), fill=BODY, r=20)
    card(d, (x0 + 18, y0 + 16, x0 + 422, y0 + 78), fill=SCREEN, r=10)
    text(d, (x0 + 220, y0 + 47), reading, 46, SCR_INK)
    text(d, (x0 + 220, y0 + 100), label, 40, WHITE, bold=False)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
Q_AT = 1.2
def s_hook(img, d, t, sc):
    circuit(d, False, 100, oy=640, rx_q=True)
    a = appear(t, Q_AT, 0.5)
    if a <= 0: return
    y0 = 250 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 530), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 38, WHITE, alpha=a)
    ctext(d, y0 + 230, "Giảm Rx: 100, 20, 10, 5, 2, 0 Ω.\nSố chỉ vôn kế ở hai cực pin\nđổi thế nào qua từng nấc?",
          46, INK, maxw=920, alpha=a)
    text(d, (W / 2, y0 + 410), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=a)
    tc, tend = Q_AT + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 480, 940, y0 + 492], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 480, 140 + 800 * (1 - p), y0 + 492], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (mach + dong ho + bang Rx-I-U) ----------------
T_S = [1.0, 2.4, 3.8, 5.2, 6.6, 8.0]   # dong K o lan do k ; doi Rx truoc 0,4 s (K mo) ; ngat K sau 0,9 s
T_ON, T_RX = 0.9, 0.4
T_DU, T_ANS = 9.3, 10.6               # hien cot "U tut" ; dap an
def do_state(t):
    """-> (K dong?, Rx dang dat, so ampe ke, so von ke, so hang da ghi, chi so lan dang dong hoac -1)."""
    n_rx = sum(1 for ts in T_S if t >= ts - T_RX - 1e-9)
    rx = ROWS[max(0, n_rx - 1)][0]
    n = sum(1 for ts in T_S if t >= ts - 1e-9)
    k = n - 1
    closed = k >= 0 and (t < T_S[k] + T_ON - 1e-9 or k == len(T_S) - 1)   # lan cuoi giu K dong toi het canh (cong B)
    if closed:
        _, i, u = ROWS[k]; return True, rx, vn(i, 3) + " A", vn(u) + " V", n, k
    return False, rx, "0,000 A", vn(E0) + " V", n, -1

TX = [110, 330, 560, 820]; TY0, RH = 820, 92        # cot: Rx | I | U | U tut ; hang tieu de o TY0
def table(d, n, k_on, kd, hl_last=0.0):
    card(d, (40, 760, 1040, TY0 + 46 + 6 * RH + 20), fill=WHITE, outline=LIGHT, w=3)
    for x, s in zip(TX[:3], ("Rx (Ω)", "I (A)", "U (V)")): text(d, (x + 60 if x == 110 else x, TY0), s, 40, INK)
    if kd > 0: text(d, (TX[3], TY0), "Tụt so nấc trước", 40, RED, alpha=kd)
    d.line([(60, TY0 + 36), (1020, TY0 + 36)], fill=LIGHT, width=3)
    for j in range(n):
        y = TY0 + 46 + RH * j + RH / 2
        if j == k_on: d.rounded_rectangle([60, y - 38, 1020, y + 38], radius=14, fill=HL)
        rx, i, u = ROWS[j]
        text(d, (TX[0] + 60, y), str(rx), 44, NAVY); text(d, (TX[1], y), vn(i, 3), 44, INK); text(d, (TX[2], y), vn(u), 44, INK)
        if j >= 1 and kd > 0:
            big = j >= 4
            text(d, (TX[3], y - RH / 2), "−" + vn(DROPS[j - 1]), 44, RED if big else MUTED, alpha=kd)

def s_do(img, d, t, sc):
    closed, rx, ia, uv, n, k = do_state(t)
    circuit(d, closed, rx)
    readout(d, 70, 586, "ampe kế", ia); readout(d, 570, 586, "vôn kế", uv)
    table(d, n, k, appear(t, T_DU, 0.4))
    ka = appear(t, T_ANS, 0.15)
    if ka > 0:
        card(d, (60, 1490, 1020, 1600), fill=A((21, 110, 52), ka), r=30)
        text(d, (W / 2, 1545), "ĐÁP ÁN · tụt ít lúc đầu, mạnh ở cuối", 42, WHITE, alpha=ka)

# ---------------- canh 3: Rut ra (do thi U-I) + Chua noi duoc ----------------
GX0, GX1, GY0, GY1 = 200, 950, 1360, 760          # I 0-0,6 A ; U 1,0-1,6 V (ngat truc)
UMIN, UMAX = 1.0, 1.6
def gx(i): return GX0 + i / 0.6 * (GX1 - GX0)
GU = GY0 - 70
def gy(u): return GU - (u - UMIN) / (UMAX - UMIN) * (GU - GY1)

def axes(d):
    card(d, (40, 700, 1040, 1450), fill=WHITE, outline=LIGHT, w=3)
    for u in (1.1, 1.3, 1.5):
        d.line([(GX0, gy(u)), (GX1, gy(u))], fill=LIGHT, width=3)
        text(d, (GX0 - 16, gy(u)), vn(u, 1), 40, MUTED, anchor="rm")
    d.line([(GX0, GY0), (GX1 + 10, GY0)], fill=NAVY, width=5)
    d.line([(GX0, GY0), (GX0, GY0 - 22)], fill=NAVY, width=5); d.line([(GX0, GY0 - 44), (GX0, GY1 - 10)], fill=NAVY, width=5)
    for yy in (GY0 - 18, GY0 - 40):
        d.line([(GX0 - 22, yy + 8), (GX0 + 22, yy - 8)], fill=NAVY, width=5)
    d.polygon([(GX1 + 26, GY0), (GX1 + 8, GY0 - 10), (GX1 + 8, GY0 + 10)], fill=NAVY)
    d.polygon([(GX0, GY1 - 26), (GX0 - 10, GY1 - 8), (GX0 + 10, GY1 - 8)], fill=NAVY)
    text(d, (GX0 + 22, GY1 - 14), "U (V)", 40, INK, anchor="lm")
    text(d, (GX0 - 16, GY0 + 34), "0", 40, MUTED, anchor="rm")
    for i in (0.2, 0.4):
        d.line([(gx(i), GY0), (gx(i), GY0 + 12)], fill=NAVY, width=4)
        text(d, (gx(i), GY0 + 40), vn(i, 1), 40, MUTED)
    text(d, (GX1 - 20, GY0 + 40), "I (A)", 40, INK)

SLOPE = (E0 - LINE_P2[1]) / LINE_P2[0]              # chi dung de ve, KHONG ghi so
def s_rut(img, d, t, sc):
    M = sc["M"]
    axes(d)
    kp = clamp(t / 1.2)
    for j, (_, i, u) in enumerate(ROWS):
        if kp * 6 > j: dot(d, gx(i), gy(u), 13, BLUE, outline=WHITE)
    kl = clamp((t - 1.4) / 0.7)
    if kl > 0:
        i1 = 0.58 * ease(kl)
        d.line([(gx(0), gy(E0)), (gx(i1), gy(E0 - SLOPE * i1))], fill=A(BLUE, 0.85), width=5)
    k1 = appear(t, 1.4, 0.45)
    if k1 > 0:
        y = 250 + (1 - k1) * 20
        card(d, (50, y, 1030, y + 200), fill=A(WHITE, k1), outline=A(BLUE, k1), w=6)
        text(d, (W / 2, y + 62), "Vẽ U theo I: 6 điểm thẳng hàng", 44, BLUE, alpha=k1)
        text(d, (W / 2, y + 140), "U tụt tỉ lệ với I tăng", 42, INK, alpha=k1)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        dot(d, GX0, gy(E0), 15, A(ORANGE, k2), outline=WHITE)
        mt(d, (GX0 + 200, gy(E0) - 45), "ℰ ≈ 1,50 V", 42, ORANGE, k2, anchor="l")
        y = 470 + (1 - k2) * 20
        card(d, (50, y, 1030, y + 200), fill=A(WHITE, k2), outline=A(ORANGE, k2), w=6)
        text(d, (W / 2, y + 62), "Giao trục U cho suất điện động", 44, ORANGE, alpha=k2)
        text(d, (W / 2, y + 140), "Độ dốc cho r", 42, INK, alpha=k2)
    k3 = appear(t, M[2] - 0.1, 0.45)
    if k3 > 0:
        y = 1440 + (1 - k3) * 20
        card(d, (50, y, 1030, y + 210), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 55), "Chưa nói được", 42, NAVY, alpha=k3)
        text(d, (W / 2, y + 145), "Dòng lớn hơn 0,534 A: còn thẳng?", 44, INK, alpha=k3 * appear(t, M[2] + 0.3, 0.4))

# ---------------- canh 4: Bay - mac ampe ke song song hai cuc pin ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.1, 0.4)
    card(d, (40, 260, 1040, 620), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, 290, W / 2 + pw / 2, 354), fill=A(RED, a1), r=32)
    text(d, (W / 2, 322), "BẪY", 38, WHITE, alpha=a1)
    q1, q2 = "Mắc ampe kế song song", "hai cực pin"
    text(d, (W / 2, 430), q1, 48, RED, alpha=a1); text(d, (W / 2, 520), q2, 48, RED, alpha=a1)
    ks = clamp((t - (M[1] + 0.6)) / 0.4)
    if ks > 0:
        for yy, s in ((432, q1), (522, q2)):
            lw = tw(d, s, F(48))
            d.line([(W / 2 - lw / 2 - 6, yy), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy)], fill=RED, width=6)
    # hinh: pin + ampe ke noi thang hai cuc (sai)
    a2 = appear(t, 0.3, 0.4)
    if a2 > 0:
        cx, y0 = 540, 720
        d.line([(cx - 260, y0 + 60), (cx - 260, y0 + 175)], fill=A(WIRE, a2), width=6)
        d.line([(cx - 260, y0 + 215), (cx - 260, y0 + 330)], fill=A(WIRE, a2), width=6)
        d.line([(cx - 260, y0 + 60), (cx + 220, y0 + 60), (cx + 220, y0 + 150)], fill=A(WIRE, a2), width=6, joint="curve")
        d.line([(cx + 220, y0 + 240), (cx + 220, y0 + 330), (cx - 260, y0 + 330)], fill=A(WIRE, a2), width=6, joint="curve")
        d.line([(cx - 316, y0 + 175), (cx - 204, y0 + 175)], fill=A(PINC, a2), width=7)
        d.line([(cx - 288, y0 + 215), (cx - 232, y0 + 215)], fill=A(PINC, a2), width=16)
        text(d, (cx - 180, y0 + 175), "+", 42, PINC, alpha=a2); text(d, (cx - 180, y0 + 222), "−", 42, PINC, alpha=a2)
        text(d, (cx - 100, y0 + 197), "pin", 40, MUTED, alpha=a2)
        d.ellipse([cx + 176, y0 + 151, cx + 264, y0 + 239], fill=A(WHITE, a2), outline=A(BLUE, a2), width=6)
        text(d, (cx + 220, y0 + 197), "A", 42, BLUE, alpha=a2)
        if t > M[1] + 0.6:   # dong vot: mui ten do dam tren day tren, chieu tu (+) sang phai
            kk = appear(t, M[1] + 0.6, 0.3)
            arrow(d, (cx - 60, y0 + 60), (cx + 80, y0 + 60), A(RED, kk), w=7, head=20)
            text(d, (cx + 10, y0 + 20), "dòng vọt", 40, RED, alpha=kk)
    ka = appear(t, M[1] + 1.4, 0.5)
    if ka > 0:
        card(d, (60, 1150, 1020, 1430), fill=A((236, 253, 243), ka), outline=A(GREEN, ka), w=5)
        text(d, (W / 2, 1230), "✓ Ampe kế mắc nối tiếp", 46, DGREEN, alpha=ka)
        text(d, (W / 2, 1350), "Song song = nối tắt pin", 44, INK, alpha=ka)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: R0 = 5 Ohm, duong U-I so voi lan truoc?"""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 300, 1020, 580), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 440), "Vẽ U theo I: đường thẳng", 52, GREEN, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 640, 1040, 1380), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 670, W / 2 + pw / 2, 734), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 702), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 880, "Vẫn pin cũ, đổi R0 từ 2 Ω lên 5 Ω.\nSo với đường lần trước,\nđường U–I mới thế nào?",
          44, INK, maxw=950, alpha=appear(t, M[0] + 0.4, 0.5))
    kh = appear(t, M[0] + 2.9, 0.5)
    if kh <= 0: return
    card(d, (110, 1090, 970, 1330), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1150, "Gợi ý", 40, (154, 52, 18), alpha=kh)
    ctext(d, 1250, "Chỉ đổi R0, pin giữ nguyên", 42, ORANGE, maxw=840, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    out = [(h["t0"] + Q_AT, "open"), (h["t0"] + h["T"] - 0.9, "ding")]
    out += [(do["t0"] + ts, "tick") for ts in T_S]
    out += [(do["t0"] + T_ANS, "ding"), (r["t0"] + 1.4, "tap"), (b["t0"] + 0.1, "buzz"),
            (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

# ---------------- kiem vat li ----------------
def _kiem_so():
    bad = []
    for rx, i, u in ROWS:   # I = E/(R0 + Rx + r) trong 0,003 A ; U = E - I.r trong 0,015 V (nhieu kho 0,01 V + lam tron 0,005)
        if abs(E0 / (R0 + rx + R_IN) - i) > 0.003 or abs(E0 - i * R_IN - u) > 0.015: bad.append((rx, i, u))
    if DROPS != [0.04, 0.04, 0.05, 0.10, 0.19]: bad.append(("hieu U", DROPS))
    if not all(DROPS[k + 1] >= DROPS[k] for k in range(4)): bad.append("U khong tut nhanh dan -> dap an sai")
    if not all(ROWS[k + 1][1] > ROWS[k][1] and ROWS[k + 1][2] < ROWS[k][2] for k in range(5)): bad.append("chieu I/U")
    if abs(SLOPE - 0.82) > 0.005: bad.append(("doc duong ke", SLOPE))
    i5 = E0 / (5.0 + R_IN)                                  # ca tu suy cau chot: R0 = 5 Ohm
    if not (abs(i5 - 0.259) < 0.001 and i5 < ROWS[-1][1]): bad.append(("R0 5 Ohm", i5))
    return bad

def _kiem_dong_bo():
    clip = dict(CLIP); clip["scenes"] = [dict(s) for s in CLIP["scenes"]]; build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        closed, rx, ia, uv, n, k = do_state(t)
        if closed:
            r, i, u = ROWS[k]
            if k != n - 1 or rx != r or ia != vn(i, 3) + " A" or uv != vn(u) + " V": bad.append((round(t, 2), "dong"))
        elif (ia, uv) != ("0,000 A", "1,50 V"): bad.append((round(t, 2), "mo", ia, uv))
        t += 0.05
    if T_S[-1] + T_ON > T_DU: bad.append("cot U tut hien truoc lan do cuoi")
    return bad

CLIP = dict(id="tn-l11-do-sdd-pin-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Đo suất điện động · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Pin cũ và biến trở", draw=s_hook, tail=0.4, caps=[
   ("Pin AA đã dùng.", 2.6),
   ("Nghĩ trước khi xem tiếp.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Đóng K, đọc hai số.", 5.6),
   ("So từng nấc với nấc trước.", 5.6)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.6, caps=[
   ("Rx nhỏ: I tăng vọt, U tụt theo.", 3.4),
   ("Kéo dài đường tới trục U.", 3.0),
   ("Còn bỏ ngỏ.", 4.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=1.0, caps=[
   ("Lỗi hay gặp.", 2.5),
   ("Ampe kế: điện trở rất nhỏ.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 7.0)]),
])

if __name__ == "__main__":
    import sys
    print("số lệch:", _kiem_so() or "không")
    print("lệch đồng bộ:", _kiem_dong_bo() or "không")
