# Clip: tn-l11-nguon-dien-02 - Do U hai cuc pin khi doi dien tro mach ngoai: U tut khi I tang (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-nguon-dien-02.json:
#   so_lieu_mau (R Ohm, I A, U V): 14 0,10 1,40 ; 9 0,15 1,35 ; 4 0,30 1,20 ; 2 0,50 1,00 ; 1,5 0,60 0,90.
#   cac_buoc.lam: K mo (ho mach) von ke chi E = 1,50 V, I = 0. tham_so: E = 1,5 V, r = 1,0 Ohm, R 0-20 Ohm buoc 0,5.
#   Kiem: I = 1,5/(R + 1,0), U = I.R = 1,5 - I.1,0 dung tung hang (_kiem_so()).
#   Bay = hien_tuong_hay_sai[1]: lay U/I cua mot hang goi la r (1,20/0,30 = 4 = R ; 1,40/0,10 = 14 = R).
#   KHONG hien gia tri r = 1,0 Ohm (cau hoi ngay sau hop trong bai hoi "r bang bao nhieu").
#   Cau hoi chot: R = 5 Ohm (trong tham_so, chua tung hien) -> I = 0,25 A, U = 1,25 V (chua tung hien).
# Bo cuc (khac nguondien1 dung hai mach + do thi U-t): MOT mach pin - K - ampe ke - hop dien tro (noi tiep),
#   von ke mac SONG SONG hai cuc pin; BANG R-I-U o Tien hanh, roi DIEM U-I o Rut ra.
# Mach: pin vach dai = cuc (+) o tren; dong quy uoc ra tu (+) -> K -> A -> R -> ve (-). So chi dong ho, nhan R,
#   trang thai K va hang bang doi CUNG luc (kiem bang ma moi 0,05 s: _kiem_dong_bo()).
from engine import *

ROWS = [(14, 0.10, 1.40), (9, 0.15, 1.35), (4, 0.30, 1.20), (2, 0.50, 1.00), (1.5, 0.60, 0.90)]   # so_lieu_mau
E0 = 1.50                                                                                          # ho mach
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
def vr(r): return vn(r, 1) if r != int(r) else str(int(r))

WIRE = (60, 66, 92); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30); BODY = (70, 78, 100)
PINC = ORANGE; DGREEN = (10, 80, 40); HL = (255, 237, 213)

# chu "E viet tay" (suat dien dong): SF khong co glyph -> ve bang STIX Bold Italic
_SX = "/System/Library/Fonts/Supplemental/STIXGeneralBolIta.otf"; _sc = {}
def FS(size):
    if size not in _sc: _sc[size] = ImageFont.truetype(_SX, int(size))
    return _sc[size]
def mt(d, xy, s, size, color=INK, alpha=1.0, anchor="m"):
    """Chu co 'ℰ' (ve bang STIX), con lai bang SF; anchor 'm' (giua) hoac 'l' (trai). Cung duong chan chu."""
    parts = [p for p in re.split(r"(ℰ)", s) if p]
    fs = [FS(size * 1.12) if p == "ℰ" else F(size) for p in parts]
    tot = sum(tw(d, p, f) for p, f in zip(parts, fs))
    x = xy[0] - tot / 2 if anchor == "m" else xy[0]; yb = xy[1] + size * 0.36
    for p, f in zip(parts, fs):
        dtext(d, (x, yb), p, f, color, alpha, "ls"); x += tw(d, p, f)

# ---------------- so do mach (toa do khung goc) ----------------
XL, XR, YT, YB = 330, 820, 330, 690
YP, YN = 486, 534                  # vach dai (+) va vach ngan (-) cua pin
KX0, KX1 = 420, 520                # khoa K tren day tren
AX, VX, VY = 660, 160, 510         # tam ampe ke (tren day tren) ; tam von ke (ben trai pin)
NODE_T, NODE_B = 400, 620          # hai nut noi von ke vao hai cuc pin

def meter_sym(d, x, y, ch, col):
    d.ellipse([x - 50, y - 50, x + 50, y + 50], fill=WHITE, outline=col, width=6)
    text(d, (x, y + 2), ch, 46, col)

def circuit(d, closed, rlab, flow=False, pin_note=None):
    # day mach chinh
    d.line([(XL, YP), (XL, YT), (KX0, YT)], fill=WIRE, width=6, joint="curve")
    d.line([(KX1, YT), (AX - 50, YT)], fill=WIRE, width=6)
    d.line([(AX + 50, YT), (XR, YT), (XR, 435)], fill=WIRE, width=6, joint="curve")
    d.line([(XR, 585), (XR, YB), (XL, YB), (XL, YN)], fill=WIRE, width=6, joint="curve")
    # pin: vach dai mong = (+) tren, vach ngan day = (-) duoi
    d.line([(XL - 62, YP), (XL + 62, YP)], fill=PINC, width=7)
    d.line([(XL - 32, YN), (XL + 32, YN)], fill=PINC, width=16)
    text(d, (XL + 84, YP - 22), "+", 44, PINC); text(d, (XL + 84, YN + 22), "−", 44, PINC)
    if pin_note: text(d, (XL + 112, 510), pin_note, 40, MUTED, bold=False, anchor="lm")
    # khoa K
    dot(d, KX0, YT, 10, WIRE); dot(d, KX1, YT, 10, WIRE)
    if closed: d.line([(KX0, YT), (KX1, YT)], fill=NAVY, width=7)
    else: d.line([(KX0, YT), (KX0 + 92 * math.cos(math.radians(32)), YT - 92 * math.sin(math.radians(32)))], fill=NAVY, width=7)
    text(d, ((KX0 + KX1) / 2, YT + 44), "K", 40, NAVY)
    # ampe ke noi tiep
    meter_sym(d, AX, YT, "A", BLUE)
    # hop dien tro (bien tro): hinh chu nhat + mui ten cheo
    d.rectangle([XR - 26, 435, XR + 26, 585], fill=WHITE, outline=NAVY, width=5)
    arrow(d, (XR - 62, 590), (XR + 62, 430), NAVY, w=5, head=20)
    text(d, (XR + 74, 510), rlab, 42, NAVY, anchor="lm")
    # von ke song song hai cuc pin
    d.line([(XL, NODE_T), (VX, NODE_T), (VX, VY - 50)], fill=WIRE, width=5, joint="curve")
    d.line([(XL, NODE_B), (VX, NODE_B), (VX, VY + 50)], fill=WIRE, width=5, joint="curve")
    dot(d, XL, NODE_T, 9, WIRE); dot(d, XL, NODE_B, 9, WIRE)
    meter_sym(d, VX, VY, "V", PURPLE)
    for p in ((XL, YT), (XR, YT), (XR, YB), (XL, YB)): dot(d, p[0], p[1], 7, WIRE)
    if flow:                         # chieu dong quy uoc: (+) -> mach ngoai -> (-)
        arrow(d, (560, YT - 34), (612, YT - 34), RED, w=5, head=16)
        text(d, (540, YT - 34), "I", 40, RED, anchor="rm")

def readout(d, x0, label, reading, col):
    card(d, (x0, 760, x0 + 420, 912), fill=BODY, r=20)
    card(d, (x0 + 18, 776, x0 + 402, 848), fill=SCREEN, r=10)
    text(d, (x0 + 210, 813), reading, 48 if reading != "?" else 52, PURPLE if reading == "?" else SCR_INK)
    text(d, (x0 + 210, 882), label, 40, WHITE, bold=False)

# ---------------- bang R - I - U ----------------
TY = 935; XS = (250, 540, 830)
def table(d, n_open, n, hl=None):
    card(d, (60, TY, 1020, TY + 482), fill=WHITE, outline=NAVY, w=4)
    for xx, c in zip(XS, ("R (Ω)", "I (A)", "U (V)")): text(d, (xx, TY + 44), c, 40, INK)
    d.line([(90, TY + 82), (990, TY + 82)], fill=LIGHT, width=4)
    rows = ([("K mở", "0", vn(E0))] if n_open else []) + [(vr(r), vn(i), vn(u)) for r, i, u in ROWS[:n]]
    for j, (a, b, c) in enumerate(rows):
        yy = TY + 122 + j * 60
        if hl == j: d.rounded_rectangle([78, yy - 28, 1002, yy + 28], radius=14, fill=HL)
        text(d, (XS[0], yy), a, 38 if a == "K mở" else 40, MUTED if a == "K mở" else NAVY)
        text(d, (XS[1], yy), b, 40, BLUE); text(d, (XS[2], yy), c, 40, PURPLE)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
Q_AT = 1.4
def s_hook(img, d, t, sc):
    circuit(d, False, "R", pin_note="pin 1,5 V")
    readout(d, 90, "ampe kế", "?", BLUE); readout(d, 570, "vôn kế", "?", PURPLE)
    a = appear(t, Q_AT, 0.5)
    if a <= 0: return
    y0 = 945 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 38, WHITE, alpha=a)
    ctext(d, y0 + 240, "Đóng K rồi thay R nhỏ dần.\nSố chỉ vôn kế ở hai cực pin\nthay đổi thế nào?", 46,
          INK, maxw=920, alpha=a)
    tc, tend = Q_AT + 0.6, sc["T"] - 0.6
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 424, 940, y0 + 436], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 424, 140 + 800 * (1 - p), y0 + 436], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (bang R-I-U) ----------------
T_OPEN = 0.9                       # ghi hang "K mo" (ho mach)
T_S = [2.3, 3.8, 5.3, 6.8, 8.3]    # luc dong K / doi R: so chi + nhan R + hang moi doi cung luc
T_ANS = 9.8
def do_state(t):
    """-> (K dong?, nhan R, so ampe ke, so von ke, co hang ho mach?, so hang da ghi)."""
    k = sum(1 for ts in T_S if t >= ts - 1e-9)
    if k == 0: return False, vr(ROWS[0][0]) + " Ω", vn(0) + " A", vn(E0) + " V", t >= T_OPEN - 1e-9, 0
    r, i, u = ROWS[k - 1]
    return True, vr(r) + " Ω", vn(i) + " A", vn(u) + " V", True, k

def s_do(img, d, t, sc):
    closed, rlab, ia, uv, n_open, n = do_state(t)
    circuit(d, closed, rlab, flow=closed)
    readout(d, 90, "ampe kế", ia, BLUE); readout(d, 570, "vôn kế", uv, PURPLE)
    hl = (n if n_open else n - 1) if (n_open or n) else None
    table(d, n_open, n, hl=hl)
    ka = appear(t, T_ANS, 0.15)
    if ka > 0:
        card(d, (60, 1440, 1020, 1546), fill=A((21, 110, 52), ka), r=30)
        text(d, (W / 2, 1493), "ĐÁP ÁN · vôn kế tụt dần", 42, WHITE, alpha=ka)

def _kiem_so():
    """Moi hang: I = E/(R + r) va U = E - I.r (E = 1,5 V ; r = 1,0 Ohm) trong sai so 0,005."""
    return [(r, i, u) for r, i, u in ROWS if abs(1.5 / (r + 1.0) - i) > 0.005 or abs(1.5 - i * 1.0 - u) > 0.005
            or abs(i * r - u) > 0.005]

def _kiem_dong_bo():
    """Moi 0,05 s: so von ke/ampe ke = hang cuoi cua bang; nhan R = R cua hang do; K dong <=> co hang R."""
    clip = dict(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        closed, rlab, ia, uv, n_open, n = do_state(t)
        if closed != (n > 0): bad.append((round(t, 2), "K", closed, n))
        if n > 0:
            r, i, u = ROWS[n - 1]
            if (ia, uv, rlab) != (vn(i) + " A", vn(u) + " V", vr(r) + " Ω"): bad.append((round(t, 2), "so", ia, uv, rlab))
        elif n_open and (ia, uv) != ("0,00 A", "1,50 V"): bad.append((round(t, 2), "ho", ia, uv))
        t += 0.05
    return bad

# ---------------- canh 3: Rut ra (diem U-I) + Chua noi duoc ----------------
GX0, GX1, GY0, GY1 = 220, 930, 970, 390          # I 0-0,8 A ; U 0-1,6 V (truc co dinh)
def gx(i): return GX0 + i / 0.8 * (GX1 - GX0)
def gy(u): return GY0 - u / 1.6 * (GY0 - GY1)
PTS = [(0.0, E0)] + [(i, u) for _, i, u in ROWS]

def dashed(d, p1, p2, color, w=3, dash=14, gap=10):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for k in range(n):
        a = k * (dash + gap) / L; b = min(1, (k * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

def graph_axes(d):
    card(d, (40, 300, 1040, 1062), fill=WHITE, outline=LIGHT, w=3)
    for u in (0.5, 1.0, 1.5):
        d.line([(GX0, gy(u)), (GX1, gy(u))], fill=LIGHT, width=3)
        text(d, (GX0 - 16, gy(u)), vn(u, 1), 40, MUTED, anchor="rm")
    text(d, (GX0 - 16, GY0), "0", 40, MUTED, anchor="rm")
    d.line([(GX0, GY0), (GX1 + 10, GY0)], fill=NAVY, width=5); d.line([(GX0, GY0), (GX0, GY1 - 10)], fill=NAVY, width=5)
    d.polygon([(GX1 + 26, GY0), (GX1 + 8, GY0 - 10), (GX1 + 8, GY0 + 10)], fill=NAVY)
    d.polygon([(GX0, GY1 - 26), (GX0 - 10, GY1 - 8), (GX0 + 10, GY1 - 8)], fill=NAVY)
    text(d, (GX0 + 22, GY1 - 14), "U (V)", 38, INK, anchor="lm")
    for i in (0.2, 0.4, 0.6, 0.8):
        d.line([(gx(i), GY0), (gx(i), GY0 + 12)], fill=NAVY, width=4)
        text(d, (gx(i), GY0 + 38), vn(i, 1), 40, MUTED)
    text(d, (GX1 + 20, GY0 - 40), "I (A)", 38, INK, anchor="rm")

def s_rut(img, d, t, sc):
    M = sc["M"]
    graph_axes(d)
    kE = appear(t, 0.3, 0.4)                        # muc ho mach 1,50 V
    if kE > 0:
        dashed(d, (GX0, gy(E0)), (GX1, gy(E0)), A(ORANGE, kE), w=4)
        mt(d, (GX1 - 200, gy(E0) - 34), "ℰ = 1,50 V", 38, ORANGE, kE, anchor="l")
    kl = appear(t, 2.0, 0.4)
    if kl > 0: d.line([(gx(0), gy(E0)), (gx(0.7), gy(E0 - 0.7))], fill=A(PURPLE, 0.55 * kl), width=4)
    for j, (i, u) in enumerate(PTS):
        kp = appear(t, 0.5 + j * 0.25, 0.25)
        if kp <= 0: continue
        kg = clamp((t - (2.3 + 0.25 * j)) / 0.6)    # thanh do moc dan tu muc 1,50 V xuong diem (2,3-3,8 s)
        if j > 0 and kg > 0:
            d.line([(gx(i), gy(E0)), (gx(i), lerp(gy(E0), gy(u), ease(kg)))], fill=RED, width=8)
        dot(d, gx(i), gy(u), 12, A(PURPLE, kp), outline=WHITE)
    kf = appear(t, 4.1, 0.45)                       # cong thuc: sau khi cac thanh do da moc xong
    if kf > 0:
        y = 1085 + (1 - kf) * 30
        card(d, (60, y, 1020, y + 250), fill=A(WHITE, kf), outline=A(RED, kf), w=6)
        mt(d, (W / 2, y + 55), "Phần hụt  ℰ − U = I·r", 46, RED, kf)
        text(d, (W / 2, y + 120), "r: điện trở trong của pin", 40, INK, alpha=kf)
        ku = appear(t, 5.2, 0.45)
        mt(d, (W / 2, y + 195), "U = ℰ − I·r", 52, INK, ku)
    k3 = appear(t, M[1] - 0.1, 0.45)
    if k3 > 0:
        y = 1355 + (1 - k3) * 20
        card(d, (60, y, 1020, y + 300), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 55), "Chưa nói được", 44, NAVY, alpha=k3)
        ctext(d, y + 180, "Pin nóng lên hay cũ thêm,\nr có giữ nguyên?", 46, INK, maxw=900,
              alpha=k3 * appear(t, M[1] + 0.3, 0.4))

# ---------------- canh 4: Bay - "U/I cua mot hang la r" ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.1, 0.4)
    y0 = 320
    card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(RED, a1), r=32)
    text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
    q = "r = U / I của một hàng"
    yy = y0 + 190; lw = tw(d, q, F(48))
    text(d, (W / 2, yy), q, 48, RED, alpha=a1)
    ks = clamp((t - (M[1] + 1.6)) / 0.4)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=RED, width=5)
    text(d, (W / 2, y0 + 320), "r: điện trở trong của pin", 40, INK, alpha=a1)
    # hai hang thu
    for j, (r, i, u, at) in enumerate(((4, 0.30, 1.20, 0.6), (14, 0.10, 1.40, M[1] + 0.2))):
        kr = appear(t, at, 0.4)
        if kr <= 0: continue
        y = 800 + j * 200
        card(d, (60, y, 1020, y + 160), fill=A(HL, kr), r=24)
        text(d, (240, y + 80), f"{vn(u)} / {vn(i)}", 48, INK, alpha=kr)
        text(d, (440, y + 80), "=", 48, INK, alpha=kr)
        kv = appear(t, at + 0.8, 0.35)
        text(d, (540, y + 80), f"{r} Ω", 52, BLUE, alpha=kv)
        text(d, (630, y + 80), "= R trên hộp", 46, BLUE, alpha=kv, anchor="lm")
    ka = appear(t, M[1] + 1.9, 0.5)
    if ka > 0:
        text(d, (W / 2, 1270), "✓ U/I là điện trở mạch ngoài", 44, DGREEN, alpha=ka)
        mt(d, (W / 2, 1350), "r nằm ở phần hụt  ℰ − U", 44, DGREEN, ka)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: R = 5 Ohm, von ke chi bao nhieu? (I = 0,25 A ; U = 1,25 V)."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 400, 1020, 680), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 540, "Dòng càng lớn,\nU hai cực càng tụt", 52, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 740, 1040, 1420), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 770, W / 2 + pw / 2, 834), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 802), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 980, "Cùng pin đó, đặt R = 5 Ω.\nVôn kế ở hai cực pin\nchỉ khoảng bao nhiêu?", 46, INK,
          maxw=930, alpha=appear(t, M[0] + 0.4, 0.5))
    kh = appear(t, M[0] + 2.9, 0.5)
    if kh <= 0: return
    card(d, (110, 1170, 970, 1380), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1220, "Gợi ý", 40, (154, 52, 18), alpha=kh)
    mt(d, (W / 2, 1305), "ℰ = 1,50 V; r tìm từ phần hụt", 44, ORANGE, kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    out = [(h["t0"] + Q_AT, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + T_OPEN, "tick")] + [(do["t0"] + ts, "tick") for ts in T_S]
    out += [(do["t0"] + T_ANS, "ding"), (r["t0"] + 0.3, "tap"), (b["t0"] + 0.1, "buzz"),
            (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-nguon-dien-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Nguồn điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Pin và hộp điện trở", draw=s_hook, tail=0.8, caps=[
   ("Vôn kế mắc ở hai cực pin.", 3.0),
   ("Tự đoán trước khi xem tiếp.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=1.4, caps=[
   ("Hở mạch trước, rồi đóng K.", 4.4),
   ("Giảm R, ghi từng cặp số.", 6.0)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.6, caps=[
   ("Mỗi hàng của bảng là một điểm.", 6.0),
   ("Còn bỏ ngỏ.", 4.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.8, caps=[
   ("Lấy một hàng để tìm r.", 3.0),
   ("Thử thêm hàng 14 Ω.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 7.0)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("số lệch U = E − Ir:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
