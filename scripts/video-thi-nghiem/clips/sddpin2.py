# Clip: tn-l11-do-sdd-pin-02 - Lap lai phep do voi pin moi cung loai: so sanh r pin moi va pin cu (31/10/2026)
# So lieu lay nguyen tu kho:
#   pin moi (tn-l11-do-sdd-pin-02.so_lieu_mau, Rx Ohm, I A, U V): 100 0,015 1,58 ; 20 0,073 1,56 ; 10 0,129 1,55 ;
#     5 0,217 1,53 ; 2 0,372 1,49 ; 0 0,701 1,40. Duong ke qua (0; 1,58) va (0,500; 1,45) -> E = 1,58 V, r = 0,26 Ohm.
#   pin cu (tn-l11-do-sdd-pin-01.so_lieu_mau): 100 0,014 1,48 ; 20 0,066 1,44 ; 10 0,117 1,40 ; 5 0,191 1,35 ;
#     2 0,311 1,25 ; 0 0,534 1,06. Duong qua (0; 1,50) va (0,500; 1,09) -> E = 1,50 V, r = 0,82 Ohm.
#   Kiem: U = E - I.r va I = E/(R0 + Rx + r), R0 = 2,0 Ohm, dung tung hang trong sai so nhieu (_kiem_so()).
#   KHONG hien gia tri r (0,26 / 0,82) va cac so o I = 0,5 A: hop "Dien buoc con thieu" ngay sau trong bai hoi dung
#   cac so do. Phan hut I.r o 0,5 A chi ve bang thanh do (ti le dung), khong ghi so.
#   Bay = hien_tuong_hay_sai[1]: do ho mach la du biet pin con tot (1,50 V vs 1,58 V gan nhau).
#   Cau hoi chot (sai_so_thuong_gap): tinh r pin moi chi tu 2 lan do Rx = 100 va 20 Ohm co tin duoc? -> khong:
#     U chi chenh 1,58 - 1,56 = 0,02 V, cung co sai so von ke +-0,01 V; can hai diem that xa nhau (chua tung hien).
# Bo cuc (khac nguondien2 dung bang R-I-U): DO THI U-I la truc chinh, truc CO DINH tu canh Du doan (I 0-0,8 A,
#   U 1,0-1,65 V co dau ngat truc), duong pin cu co san; Tien hanh: mach nho + 2 dong ho + chấm diem pin moi.
# Mach: pin vach dai = (+) o tren; (+) -> K -> ampe ke -> R0 -> Rx -> (-), von ke SONG SONG hai cuc pin. Moi lan do:
#   doi Rx (K mo) -> dong K (so chi + diem moi hien cung luc) -> ngat K (ampe ke 0,000 A, von ke chi E = 1,58 V).
#   Kiem bang ma moi 0,05 s: _kiem_dong_bo().
from engine import *

NEW = [(100, 0.015, 1.58), (20, 0.073, 1.56), (10, 0.129, 1.55), (5, 0.217, 1.53), (2, 0.372, 1.49), (0, 0.701, 1.40)]
OLD = [(100, 0.014, 1.48), (20, 0.066, 1.44), (10, 0.117, 1.40), (5, 0.191, 1.35), (2, 0.311, 1.25), (0, 0.534, 1.06)]
E_NEW, R_NEW, E_OLD, R_OLD, R0 = 1.58, 0.26, 1.50, 0.82, 2.0
I_CMP = 0.500                                                # diem thu hai cua ca hai duong (kho)
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")

WIRE = (60, 66, 92); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30); BODY = (70, 78, 100)
PINC = ORANGE; DGREEN = (10, 80, 40); OLDC = (120, 128, 150); NEWC = BLUE

# chu "E viet tay" (suat dien dong): SF khong co glyph -> ve bang STIX Bold Italic
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

# ---------------- do thi U-I (truc co dinh tu dau toi Rut ra) ----------------
GX0, GX1, GY0, GY1 = 200, 950, 1340, 790          # I 0-0,8 A ; U 1,0-1,65 V
UMIN, UMAX = 1.0, 1.65
def gx(i): return GX0 + i / 0.8 * (GX1 - GX0)
GU = GY0 - 70                                      # muc U = 1,0 V (tren dau ngat truc)
def gy(u): return GU - (u - UMIN) / (UMAX - UMIN) * (GU - GY1)

def dashed(d, p1, p2, color, w=3, dash=14, gap=10):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for k in range(n):
        a = k * (dash + gap) / L; b = min(1, (k * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

def axes(d):
    card(d, (40, 715, 1040, 1435), fill=WHITE, outline=LIGHT, w=3)
    for u in (1.0, 1.2, 1.4, 1.6):
        d.line([(GX0, gy(u)), (GX1, gy(u))], fill=LIGHT, width=3)
        text(d, (GX0 - 16, gy(u)), vn(u, 1), 40, MUTED, anchor="rm")
    d.line([(GX0, GY0), (GX1 + 10, GY0)], fill=NAVY, width=5)
    d.line([(GX0, GY0), (GX0, GY0 - 22)], fill=NAVY, width=5); d.line([(GX0, GY0 - 44), (GX0, GY1 - 10)], fill=NAVY, width=5)
    for yy in (GY0 - 18, GY0 - 40):                 # dau ngat truc U: hai gach cheo (truc U khong bat dau tu 0)
        d.line([(GX0 - 22, yy + 8), (GX0 + 22, yy - 8)], fill=NAVY, width=5)
    d.polygon([(GX1 + 26, GY0), (GX1 + 8, GY0 - 10), (GX1 + 8, GY0 + 10)], fill=NAVY)
    d.polygon([(GX0, GY1 - 26), (GX0 - 10, GY1 - 8), (GX0 + 10, GY1 - 8)], fill=NAVY)
    text(d, (GX0 + 22, GY1 - 14), "U (V)", 40, INK, anchor="lm")
    text(d, (GX0 - 16, GY0 + 34), "0", 40, MUTED, anchor="rm")
    for i in (0.2, 0.4, 0.6):
        d.line([(gx(i), GY0), (gx(i), GY0 + 12)], fill=NAVY, width=4)
        text(d, (gx(i), GY0 + 40), vn(i, 1), 40, MUTED)
    text(d, (GX1, GY0 + 40), "I (A)", 40, INK)

def old_line(d, a=1.0, label=True):
    i1 = (E_OLD - UMIN - 0.008) / R_OLD                       # dung truoc day truc 1,0 V
    d.line([(gx(0), gy(E_OLD)), (gx(i1), gy(E_OLD - R_OLD * i1))], fill=A(OLDC, 0.8 * a), width=5)
    for _, i, u in OLD: dot(d, gx(i), gy(u), 11, A(OLDC, a), outline=WHITE)
    if label: text(d, (gx(i1) + 10, gy(1.13)), "pin cũ", 40, OLDC, anchor="lm", alpha=a)

def new_line(d, k=1.0, a=1.0):
    i1 = 0.75 * k
    if i1 > 0: d.line([(gx(0), gy(E_NEW)), (gx(i1), gy(E_NEW - R_NEW * i1))], fill=A(NEWC, 0.8 * a), width=5)

def new_pts(d, n, pop=None):
    for j, (_, i, u) in enumerate(NEW[:n]):
        r = 12 + (6 * (1 - pop) if (pop is not None and j == n - 1) else 0)
        dot(d, gx(i), gy(u), r, NEWC, outline=WHITE)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong nut A-D) ----------------
Q_AT = 1.4
def s_hook(img, d, t, sc):
    axes(d); old_line(d)
    a = appear(t, Q_AT, 0.5)
    if a <= 0: return
    y0 = 250 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 440), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 38, WHITE, alpha=a)
    ctext(d, y0 + 235, "Thay pin mới cùng loại,\ngiữ nguyên mạch và 6 lần đo.\nĐường U–I của pin mới thế nào?",
          46, INK, maxw=920, alpha=a)
    tc, tend = Q_AT + 0.6, sc["T"] - 0.6
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 400, 940, y0 + 412], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 400, 140 + 800 * (1 - p), y0 + 412], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (mach nho + dong ho + cham diem pin moi) ----------------
XL, XR, YT, YB = 260, 900, 270, 540
YP, YN = 385, 425                    # vach dai (+), vach ngan (-)
KX0, KX1 = 330, 410; AX = 520; R0X0, R0X1 = 640, 760; VX, VY = 110, 405; NODE_T, NODE_B = 320, 490

def circuit(d, closed, rx):
    d.line([(XL, YP), (XL, YT), (KX0, YT)], fill=WIRE, width=6, joint="curve")
    d.line([(KX1, YT), (AX - 44, YT)], fill=WIRE, width=6)
    d.line([(AX + 44, YT), (R0X0, YT)], fill=WIRE, width=6)
    d.line([(R0X1, YT), (XR, YT), (XR, 335)], fill=WIRE, width=6, joint="curve")
    d.line([(XR, 475), (XR, YB), (XL, YB), (XL, YN)], fill=WIRE, width=6, joint="curve")
    d.line([(XL - 56, YP), (XL + 56, YP)], fill=PINC, width=7)                 # (+) vach dai
    d.line([(XL - 28, YN), (XL + 28, YN)], fill=PINC, width=16)                # (-) vach ngan day
    text(d, (XL + 76, YP - 22), "+", 42, PINC); text(d, (XL + 76, YN + 24), "−", 42, PINC)
    text(d, (XL + 100, 405), "pin mới", 40, MUTED, anchor="lm")
    dot(d, KX0, YT, 9, WIRE); dot(d, KX1, YT, 9, WIRE)
    if closed: d.line([(KX0, YT), (KX1, YT)], fill=NAVY, width=7)
    else: d.line([(KX0, YT), (KX0 + 80 * math.cos(math.radians(32)), YT - 80 * math.sin(math.radians(32)))], fill=NAVY, width=7)
    text(d, ((KX0 + KX1) / 2, YT + 42), "K", 40, NAVY)
    d.ellipse([AX - 44, YT - 44, AX + 44, YT + 44], fill=WHITE, outline=BLUE, width=6); text(d, (AX, YT + 2), "A", 42, BLUE)
    d.rectangle([R0X0, YT - 22, R0X1, YT + 22], fill=WHITE, outline=NAVY, width=5)
    rich(d, (R0X0 + R0X1) / 2, YT + 54, "R_{0} = 2 Ω", 40, NAVY)
    d.rectangle([XR - 24, 335, XR + 24, 475], fill=WHITE, outline=NAVY, width=5)
    arrow(d, (XR - 58, 480), (XR + 58, 330), NAVY, w=5, head=18)
    lab = f"R_{{x}} = {rx} Ω"; dd = tw(d, f"Rx = {rx} Ω", F(40))
    rich(d, XR - 60 - dd / 2, 405, lab, 40, NAVY)
    d.line([(XL, NODE_T), (VX, NODE_T), (VX, VY - 44)], fill=WIRE, width=5, joint="curve")
    d.line([(XL, NODE_B), (VX, NODE_B), (VX, VY + 44)], fill=WIRE, width=5, joint="curve")
    dot(d, XL, NODE_T, 8, WIRE); dot(d, XL, NODE_B, 8, WIRE)
    d.ellipse([VX - 44, VY - 44, VX + 44, VY + 44], fill=WHITE, outline=PURPLE, width=6); text(d, (VX, VY + 2), "V", 42, PURPLE)
    for p in ((XL, YT), (XR, YT), (XR, YB), (XL, YB)): dot(d, p[0], p[1], 7, WIRE)
    if closed:                       # chieu dong quy uoc: (+) -> mach ngoai -> (-): day duoi chay sang trai
        arrow(d, (660, YB + 30), (580, YB + 30), RED, w=5, head=16)
        text(d, (680, YB + 30), "I", 40, RED, anchor="lm")

def readout(d, x0, label, reading):
    card(d, (x0, 586, x0 + 440, 712), fill=BODY, r=20)
    card(d, (x0 + 18, 602, x0 + 422, 664), fill=SCREEN, r=10)
    text(d, (x0 + 220, 633), reading, 46, SCR_INK)
    text(d, (x0 + 220, 686), label, 40, WHITE, bold=False)

T_S = [1.2, 2.6, 4.0, 5.4, 6.8, 8.2]   # dong K o lan do k ; doi Rx truoc 0,4 s (K mo) ; ngat K sau 0,9 s
T_ON, T_RX = 0.9, 0.4
T_LINE, T_ANS = 9.2, 10.2
def do_state(t):
    """-> (K dong?, Rx dang dat, so ampe ke, so von ke, so diem da cham, chi so lan do dang dong hoac -1)."""
    n_rx = sum(1 for ts in T_S if t >= ts - T_RX - 1e-9)
    rx = NEW[max(0, n_rx - 1)][0]
    n = sum(1 for ts in T_S if t >= ts - 1e-9)
    k = n - 1
    closed = k >= 0 and t < T_S[k] + T_ON - 1e-9
    if closed:
        _, i, u = NEW[k]; return True, rx, f"{i:.3f}".replace(".", ",") + " A", vn(u) + " V", n, k
    return False, rx, "0,000 A", vn(E_NEW) + " V", n, -1

def s_do(img, d, t, sc):
    closed, rx, ia, uv, n, k = do_state(t)
    circuit(d, closed, rx)
    readout(d, 70, "ampe kế", ia); readout(d, 570, "vôn kế", uv)
    axes(d); old_line(d, a=0.75)
    kl = clamp((t - T_LINE) / 0.6)
    if kl > 0:
        new_line(d, ease(kl))
        text(d, (860, 900), "pin mới", 40, NEWC, alpha=appear(t, T_LINE + 0.5, 0.3))
    pop = clamp((t - T_S[n - 1]) / 0.25) if n > 0 else None
    new_pts(d, n, pop)
    ka = appear(t, T_ANS, 0.15)
    if ka > 0:
        card(d, (60, 1455, 1020, 1560), fill=A((21, 110, 52), ka), r=30)
        text(d, (W / 2, 1507), "ĐÁP ÁN · đường thoải hơn hẳn", 42, WHITE, alpha=ka)

def _kiem_so():
    """Moi hang: I = E/(R0 + Rx + r) trong 0,003 A va U = E - I.r trong 0,012 V (nhieu do kho: 0,002 A ; 0,01 V)."""
    bad = []
    for rows, E, r in ((NEW, E_NEW, R_NEW), (OLD, E_OLD, R_OLD)):
        for rx, i, u in rows:
            if abs(E / (R0 + rx + r) - i) > 0.003 or abs(E - i * r - u) > 0.012: bad.append((rx, i, u))
    if abs(E_NEW - R_NEW * I_CMP - 1.45) > 0.005 or abs(E_OLD - R_OLD * I_CMP - 1.09) > 0.005: bad.append("diem 0,5 A")
    return bad

def _kiem_dong_bo():
    """Moi 0,05 s: K dong <=> so chi = hang vua cham ; K mo <=> 0,000 A va 1,58 V ; Rx = Rx cua hang dang do."""
    clip = dict(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        closed, rx, ia, uv, n, k = do_state(t)
        if closed:
            r, i, u = NEW[k]
            if k != n - 1 or rx != r or ia != f"{i:.3f}".replace(".", ",") + " A" or uv != vn(u) + " V":
                bad.append((round(t, 2), "dong", rx, ia, uv, n))
        elif (ia, uv) != ("0,000 A", "1,58 V"): bad.append((round(t, 2), "mo", ia, uv))
        t += 0.05
    return bad

# ---------------- canh 3: Rut ra (hai duong cung truc) + Chua noi duoc ----------------
def s_rut(img, d, t, sc):
    M = sc["M"]
    axes(d); old_line(d); new_line(d); new_pts(d, 6)
    text(d, (860, 900), "pin mới", 40, NEWC)
    k1 = appear(t, 0.3, 0.45)                      # giao truc U
    if k1 > 0:
        for E, c in ((E_NEW, NEWC), (E_OLD, OLDC)): dot(d, GX0, gy(E), 13, A(ORANGE, k1), outline=WHITE)
        y = 250 + (1 - k1) * 20
        card(d, (50, y, 1030, y + 200), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
        mt(d, (W / 2, y + 62), "Giao trục U = ℰ", 44, ORANGE, k1)
        text(d, (W / 2, y + 140), "1,58 V và 1,50 V: gần nhau", 44, INK, alpha=k1)
    k2 = appear(t, 1.9, 0.45)                      # phan hut I.r o cung dong (khong ghi so)
    if k2 > 0:
        xb = gx(I_CMP)
        for E, r, dx in ((E_NEW, R_NEW, 16), (E_OLD, R_OLD, -16)):
            dashed(d, (GX0, gy(E)), (xb + dx, gy(E)), A(ORANGE, k2), w=3)
            d.line([(xb + dx, gy(E)), (xb + dx, gy(E - r * I_CMP))], fill=A(RED, k2), width=10)
        text(d, (xb + 44, gy(1.30)), "phần hụt I·r", 40, RED, anchor="lm", alpha=k2)
        y = 480 + (1 - k2) * 20
        card(d, (50, y, 1030, y + 200), fill=A(WHITE, k2), outline=A(RED, k2), w=6)
        text(d, (W / 2, y + 62), "Càng dốc xuống, r càng lớn", 44, RED, alpha=k2)
        text(d, (W / 2, y + 140), "pin mới: r nhỏ hơn hẳn", 44, INK, alpha=k2)
    k3 = appear(t, M[1] - 0.1, 0.45)
    if k3 > 0:
        y = 1450 + (1 - k3) * 20
        card(d, (50, y, 1030, y + 225), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 55), "Chưa nói được", 42, NAVY, alpha=k3)
        text(d, (W / 2, y + 150), "Trong pin, điều gì làm r tăng?", 44, INK, alpha=k3 * appear(t, M[1] + 0.3, 0.4))

# ---------------- canh 4: Bay - "do ho mach la du biet pin con tot" ----------------
def pin_meter(d, cx, y, name, reading, a, col=INK):
    d.rounded_rectangle([cx - 92, y, cx + 92, y + 260], radius=22, fill=A((255, 237, 213), a), outline=A(PINC, a), width=5)
    d.rounded_rectangle([cx - 26, y - 22, cx + 26, y + 2], radius=6, fill=A(PINC, a))
    text(d, (cx, y + 60), "+", 46, PINC, alpha=a); text(d, (cx, y + 205), "−", 46, PINC, alpha=a)
    text(d, (cx, y + 132), name, 40, col, alpha=a)
    card(d, (cx + 130, y + 56, cx + 450, y + 208), fill=A(BODY, a), r=18)
    card(d, (cx + 146, y + 74, cx + 434, y + 148), fill=A(SCREEN, a), r=10)
    text(d, (cx + 290, y + 111), reading, 46, SCR_INK, alpha=a)
    text(d, (cx + 290, y + 178), "hở mạch", 40, WHITE, bold=False, alpha=a)

def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.1, 0.4)
    card(d, (40, 260, 1040, 640), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, 290, W / 2 + pw / 2, 354), fill=A(RED, a1), r=32)
    text(d, (W / 2, 322), "BẪY", 38, WHITE, alpha=a1)
    q = "Hở mạch gần như nhau"; q2 = "→ pin cũ vẫn tốt"
    text(d, (W / 2, 440), q, 48, RED, alpha=a1); text(d, (W / 2, 530), q2, 48, RED, alpha=a1)
    ks = clamp((t - (M[1] + 1.4)) / 0.4)
    if ks > 0:
        lw = tw(d, q2, F(48))
        d.line([(W / 2 - lw / 2 - 6, 532), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, 532)], fill=RED, width=6)
    pin_meter(d, 360, 740, "pin cũ", vn(E_OLD) + " V", appear(t, 0.3, 0.4), OLDC)
    pin_meter(d, 360, 1060, "pin mới", vn(E_NEW) + " V", appear(t, 0.8, 0.4), NEWC)
    ka = appear(t, M[1] + 2.2, 0.5)
    if ka > 0:
        mt(d, (W / 2, 1420), "✓ Vôn kế hở mạch chỉ cho ℰ", 44, DGREEN, ka)
        text(d, (W / 2, 1510), "r chỉ lộ ra khi có dòng", 44, DGREEN, alpha=ka)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: cung 0,5 A, U hai cuc chenh nhieu hay it hon luc ho mach?"""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 300, 1020, 580), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 395), "Pin “hết” vì r tăng,", 50, GREEN, alpha=k0)
    mt(d, (W / 2, 480), "không phải vì mất ℰ", 50, GREEN, k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 640, 1040, 1340), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 670, W / 2 + pw / 2, 734), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 702), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 860, "Tính r pin mới chỉ từ hai lần đo\nRx = 100 Ω và 20 Ω: có đáng tin?",
          44, INK, maxw=940, alpha=appear(t, M[0] + 0.4, 0.5))
    kh = appear(t, M[0] + 2.9, 0.5)
    if kh <= 0: return
    card(d, (110, 1070, 970, 1300), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1125, "Gợi ý", 40, (154, 52, 18), alpha=kh)
    ctext(d, 1220, "Vôn kế đọc tới 0,01 V", 48, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    out = [(h["t0"] + Q_AT, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + ts, "tick") for ts in T_S]
    out += [(do["t0"] + T_ANS, "ding"), (r["t0"] + 0.3, "tap"), (b["t0"] + 0.1, "buzz"),
            (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-do-sdd-pin-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Đo suất điện động · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Pin cũ và pin mới", draw=s_hook, tail=0.8, caps=[
   ("Đường của pin cũ đã có.", 3.0),
   ("Tự đoán trước khi xem tiếp.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Đóng K ngắn, đọc, rồi ngắt.", 5.0),
   ("Chấm lên cùng hệ trục.", 6.3)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.6, caps=[
   ("So chỗ cắt trục U và độ dốc.", 4.8),
   ("Còn bỏ ngỏ.", 4.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.8, caps=[
   ("Thử pin bằng vôn kế hở mạch.", 3.0),
   ("Có đúng không?", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 7.0)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("số lệch U = E − Ir:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
