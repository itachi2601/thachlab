# Clip: tn-l9-ohm-01 - Cung hieu dien the 3 V, hai day A, B cho hai dong dien khac nhau -> dien tro (KHTN 9, 05/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-ohm-01.json:
#   so_lieu_mau (Day, U V, I A, R Ohm): A 3,0 0,30 10 ; B 3,0 0,15 20 (ghi_chu: so lieu minh hoa).
#   dung_cu: ampe ke GHD 1 A, von ke GHD 6 V. tham_so: U 1,5..6 V buoc 1,5 (cau chot dung 1,5 V).
#   rut_ra: cung U, day cho I nho hon can tro nhieu hon; R = U/I. bay = hien_tuong_hay_sai[1] (R = U.I).
#   chua noi duoc = so_lieu_mau.ghi_chu + mo_hinh.gia_thiet[0] (bo qua dien tro ampe ke, day noi, nguon).
# Cau hoi ngay sau hop trong bai (Cau 1: 6 V, 200 mA -> R) KHONG duoc giai trong clip: khong dung 6 V / 200 mA, khong doi mA.
# Du doan (K10: chi cau hoi + hinh): nguon van 3 V, thay day A bang day B -> so chi ampe ke? -> khac, tuy day.
# Cau hoi chot: day C dat 1,5 V (chua tung hien) chi 0,15 A -> can tro nhu day A hay B? (R = 10 Ohm nhu A, nguoc phan xa
#   "cung 0,15 A nhu B"). Chi can dinh nghia R = U/I clip da dung, khong ngoai suy dinh luat Ohm.
# Mach: nguon (+, ban cuc dai, trai) -> K (canh trai) -> ampe ke (+ ben trai) -> day R -> ve (-); von ke SONG SONG voi day
#   (+ o nut phia nguon +). K mo: 0,0 V ; 0,00 A. Kiem bang ma moi 0,05 s: _kiem_dong_bo(); R = U/I tung hang: _kiem_so().
# Bo cuc (khac l9congsuat1 / ohm3): so do mach + ampe ke KIM (dial) + von ke so + bang 3 cot; Ket qua = hai kim canh nhau.
import math
from engine import *

ROWS = [("A", 3.0, 0.30, 10.0), ("B", 3.0, 0.15, 20.0)]      # so_lieu_mau
U_C = 1.5                                                     # tham_so U min (cau chot)
I_MAX = 1.0                                                   # GHD ampe ke
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

WIRE = (60, 66, 92); BODY = (70, 78, 100); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30)
DGREEN = (21, 110, 55); DRED = (185, 28, 28)
CA, CB = TEAL, ORANGE
COL = {"A": CA, "B": CB, "C": PURPLE}

# ---------------- so do mach ----------------
TY, BY, XL, XR = 380, 700, 130, 950
AX, S0, S1, N1, N2, VX, VY, BX = 330, 580, 800, 520, 860, 690, 540, 540
KT, KB = 465, 575

def coil(d, cx, cy, name, a=1.0, w=210, h=70, lab=True, ls=40):
    col = COL[name]
    card(d, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), fill=A(mix(WHITE, col, 0.25), a), outline=A(col, a), r=16, w=5)
    for k in range(7):
        x = cx - w / 2 + 22 + k * (w - 44) / 6
        d.line([(x - 10, cy - h / 2 + 8), (x + 10, cy + h / 2 - 8)], fill=A(col, a), width=5)
    if lab: text(d, (cx, cy - h / 2 - ls * 0.85), "dây " + name, ls, mix(col, INK, 0.25), alpha=a)

def circuit(d, wire, closed, wa=1.0):
    """wire = 'A' / 'B' / None (o trong); wa = alpha cuon day (luc thay day)."""
    card(d, (40, 260, 1040, 760), fill=WHITE, outline=LIGHT, w=3)
    w = 6
    d.line([(XL, KT), (XL, TY), (AX - 44, TY)], fill=WIRE, width=w, joint="curve")
    d.line([(AX + 44, TY), (S0, TY)], fill=WIRE, width=w)
    d.line([(S1, TY), (XR, TY), (XR, BY), (BX + 22, BY)], fill=WIRE, width=w, joint="curve")
    d.line([(BX - 22, BY), (XL, BY), (XL, KB)], fill=WIRE, width=w, joint="curve")
    # von ke song song voi day
    d.line([(N1, TY), (N1, VY), (VX - 44, VY)], fill=WIRE, width=5, joint="curve")
    d.line([(VX + 44, VY), (N2, VY), (N2, TY)], fill=WIRE, width=5, joint="curve")
    for x in (N1, N2): dot(d, x, TY, 9, WIRE)
    d.ellipse([VX - 44, VY - 44, VX + 44, VY + 44], fill=WHITE, outline=PURPLE, width=6); text(d, (VX, VY + 2), "V", 44, PURPLE)
    text(d, (VX - 66, VY - 40), "+", 40, PURPLE)
    # ampe ke noi tiep
    d.ellipse([AX - 44, TY - 44, AX + 44, TY + 44], fill=WHITE, outline=BLUE, width=6); text(d, (AX, TY + 2), "A", 44, BLUE)
    text(d, (AX - 66, TY + 40), "+", 40, BLUE)
    # cho mac day
    dot(d, S0, TY, 8, WIRE); dot(d, S1, TY, 8, WIRE)
    if wire is None or wa < 1:
        for x in range(S0 + 10, S1 - 10, 26): d.line([(x, TY), (x + 12, TY)], fill=GRAY, width=4)
    if wire is not None and wa > 0: coil(d, (S0 + S1) / 2, TY, wire, a=wa)
    # khoa K (canh trai, dung)
    dot(d, XL, KT, 9, WIRE); dot(d, XL, KB, 9, WIRE)
    if closed: d.line([(XL, KB), (XL, KT)], fill=NAVY, width=7)
    else: d.line([(XL, KB), (XL + 58, KT + 12)], fill=NAVY, width=7)
    text(d, (XL - 52, (KT + KB) / 2), "K", 40, NAVY)
    # nguon 3 V: ban dai (+) ben trai, ban ngan (-) ben phai
    d.line([(BX - 20, BY - 50), (BX - 20, BY + 50)], fill=NAVY, width=6)
    d.line([(BX + 20, BY - 26), (BX + 20, BY + 26)], fill=NAVY, width=14)
    text(d, (BX - 52, BY - 40), "+", 44, ORANGE); text(d, (BX + 54, BY - 40), "−", 44, ORANGE)
    text(d, (BX - 80, BY - 92), "nguồn 3 V", 40, INK, anchor="mm")
    if closed:
        arrow(d, (170, TY - 34), (250, TY - 34), RED, w=5, head=16)
        text(d, (150, TY - 34), "I", 40, RED)

def ang(v): return math.radians(200 + 140 * clamp(v / I_MAX))
def dial(d, cx, cy, r, v, txt, labels=(0, 0.5, 1.0), col=RED, alpha=1.0):
    d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=340, fill=A(NAVY, alpha), width=5)
    for k in range(21):
        a = ang(k * 0.05); L = 30 if k % 10 == 0 else (20 if k % 2 == 0 else 12)
        d.line([(cx + r * math.cos(a), cy + r * math.sin(a)), (cx + (r - L) * math.cos(a), cy + (r - L) * math.sin(a))],
               fill=A(NAVY, alpha), width=4 if k % 2 == 0 else 3)
    for lv in labels:
        a = ang(lv); s = "0" if lv == 0 else ("1" if lv == 1 else vn(lv))
        text(d, (cx + (r - 58) * math.cos(a), cy + (r - 58) * math.sin(a)), s, 40, NAVY, alpha=alpha)
    text(d, (cx + r * 0.25, cy - r * 0.06), "A", 44, BLUE, alpha=alpha)
    a = ang(v)
    d.line([(cx, cy), (cx + (r - 18) * math.cos(a), cy + (r - 18) * math.sin(a))], fill=A(col, alpha), width=7)
    dot(d, cx, cy, 13, A(NAVY, alpha))
    if txt: text(d, (cx, cy + 56), txt, 46, col if txt[0] != "?" else MUTED, alpha=alpha)

def meters(d, needle, itxt, utxt, closed):
    card(d, (40, 790, 620, 1210), fill=WHITE, outline=LIGHT, w=3)
    text(d, (330, 832), "ampe kế (A)", 40, BLUE)
    dial(d, 330, 1100, 220, needle, itxt)
    card(d, (660, 790, 1040, 1060), fill=BODY, r=22)
    text(d, (850, 840), "vôn kế (V)", 40, WHITE)
    card(d, (690, 885, 1010, 1020), fill=SCREEN, r=12)
    text(d, (850, 952), utxt, 58, SCR_INK)
    card(d, (660, 1090, 1040, 1210), fill=WHITE, outline=LIGHT, w=3)
    text(d, (850, 1150), "K đóng" if closed else "K mở", 44, NAVY if closed else MUTED)

XS = (200, 520, 840)
def table(d, n, hl=None, y=1250):
    card(d, (40, y, 1040, y + 300), fill=WHITE, outline=LIGHT, w=3)
    for x, h in zip(XS, ("Dây", "U (V)", "I (A)")): text(d, (x, y + 55), h, 44, INK)
    d.line([(70, y + 100), (1010, y + 100)], fill=LIGHT, width=3)
    for j, (nm, u, i, r) in enumerate(ROWS):
        yy = y + 160 + j * 90
        if hl == j: d.rounded_rectangle([60, yy - 40, 1020, yy + 40], radius=20, fill=(255, 237, 213))
        if j < n:
            text(d, (XS[0], yy), nm, 48, COL[nm]); text(d, (XS[1], yy), vn(u), 48, NAVY); text(d, (XS[2], yy), vn(i, 2), 48, BLUE)
        else:
            for x in XS: text(d, (x, yy), "·", 44, GRAY)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
THINK_END = 0.7
def s_hook(img, d, t, sc):
    M = sc["M"]
    circuit(d, "A", True)
    meters(d, ROWS[0][2], vn(ROWS[0][2], 2) + " A", vn(ROWS[0][1]) + " V", True)
    table(d, 0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 800 + (1 - a) * 40
    card(d, (26, y0 - 26, 1054, y0 + 772), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)   # phu kin the dung cu + bang (40..1040, 790..1550)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    coil(d, 300, y0 + 200, "A", a=a); coil(d, 780, y0 + 200, "B", a=a)
    arrow(d, (440, y0 + 200), (640, y0 + 200), A(NAVY, a), w=6, head=20)
    ctext(d, y0 + 420, "Dây A: ampe kế chỉ 0,30 A.\nVẫn 3 V, thay bằng dây B.\nSố chỉ ampe kế thế nào?", 50, INK, maxw=900, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 640, 940, y0 + 652], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 640, 140 + 800 * (1 - p), y0 + 652], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
T_A, T_OPEN, T_OUT, T_IN, T_B = 0.9, 4.1, 4.3, 4.75, 5.4   # dong K voi A ; mo K ; thao A ; lap B ; dong K voi B
T_ROW, T_NEEDLE = 0.4, 0.35
def do_state(t):
    """-> (day trong cho mac, alpha day, K dong?, so hang da ghi)."""
    if t < T_OPEN: wire, closed = "A", t >= T_A
    elif t < T_B: wire, closed = ("A" if t < (T_OUT + T_IN) / 2 else "B"), False
    else: wire, closed = "B", True
    if T_OUT <= t < (T_OUT + T_IN) / 2: wa = 1 - (t - T_OUT) / ((T_IN - T_OUT) / 2)
    elif (T_OUT + T_IN) / 2 <= t < T_IN: wa = (t - (T_OUT + T_IN) / 2) / ((T_IN - T_OUT) / 2)
    else: wa = 1.0
    n = (1 if t >= T_A + T_ROW else 0) + (1 if t >= T_B + T_ROW else 0)
    return wire, wa, closed, n

def itxt(needle, i):
    """So tren mat ampe ke chi hien khi kim da dung dung so chi; kim dang chay -> '…'."""
    return vn(i, 2) + " A" if abs(needle - i) < 0.003 else "…"

def needle_at(t):
    ev = [(0.0, 0.0), (T_A, ROWS[0][2]), (T_OPEN, 0.0), (T_B, ROWS[1][2])]
    prev, tgt, ts = 0.0, 0.0, 0.0
    for k, (te, v) in enumerate(ev):
        if t >= te: prev, tgt, ts = (ev[k - 1][1] if k else 0.0), v, te
    return lerp(prev, tgt, ease((t - ts) / T_NEEDLE))

def reading(wire, closed):
    if not closed: return 0.0, 0.0
    r = [x for x in ROWS if x[0] == wire][0]; return r[1], r[2]

def s_do(img, d, t, sc):
    wire, wa, closed, n = do_state(t)
    u, i = reading(wire, closed)
    needle = needle_at(t)   # kim chay muot; chu so chi chi hien khi kim da dung
    circuit(d, wire, closed, wa)
    meters(d, needle, itxt(needle, i), vn(u) + " V", closed)
    table(d, n, hl=(n - 1 if n > 0 else None))

def _kiem_dong_bo():
    """Moi 0,05 s: K mo <=> 0 V, 0 A; K dong <=> so chi dung hang cua day dang mac; hang bang chi co sau khi da do day do."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        wire, wa, closed, n = do_state(t); u, i = reading(wire, closed)
        if not closed and (u, i) != (0.0, 0.0): bad.append((round(t, 2), "mo ma co so"))
        if closed and (wa < 1 or (wire, u, i) not in [(r[0], r[1], r[2]) for r in ROWS]): bad.append((round(t, 2), "dong sai so"))
        if closed and wire == "A" and n != (1 if t >= T_A + T_ROW else 0): bad.append((round(t, 2), "hang A"))
        if wire == "B" and closed and n not in (1, 2): bad.append((round(t, 2), "hang B"))
        if n == 2 and not (wire == "B" and closed): bad.append((round(t, 2), "hang B truoc khi do"))
        nd = needle_at(t); tx = itxt(nd, i)
        if tx != "…" and (tx != vn(i, 2) + " A" or abs(nd - i) > 0.005): bad.append((round(t, 2), "chu ampe ke lech kim", tx, round(nd, 3)))
        t += 0.05
    return bad

def _kiem_so():
    return [r for r in ROWS if abs(r[1] / r[2] - r[3]) > 0.01]

# ---------------- canh 3: Ket qua (hai kim canh nhau) ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · nhỏ hơn 0,30 A"
    pw = tw(d, lab, F(42)) + 60
    card(d, (W / 2 - pw / 2, 272, W / 2 + pw / 2, 344), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 308), lab, 42, WHITE, alpha=ka)
    for x0, (nm, u, i, r) in zip((40, 560), ROWS):
        cx = x0 + 240
        card(d, (x0, 390, x0 + 480, 890), fill=WHITE, outline=COL[nm], w=5)
        text(d, (cx, 432), "dây " + nm, 42, mix(COL[nm], INK, 0.25))
        dial(d, cx, 730, 195, i * appear(t, 0.4, 0.5), vn(i, 2) + " A")
        text(d, (cx, 848), "vôn kế " + vn(u) + " V", 40, PURPLE)
    kb = appear(t, 0.9, 0.4)
    if kb > 0:
        card(d, (40, 930, 1040, 1450), fill=A(WHITE, kb), outline=A(LIGHT, kb), w=3)
        L = 620
        for j, (nm, u, i, r) in enumerate(ROWS):
            yy = 1040 + j * 140
            text(d, (90, yy), nm, 46, COL[nm], alpha=kb)
            g = ease((t - 1.0 - 0.3 * j) / 0.5); wbar = L * i / ROWS[0][2] * g
            if wbar > 2: d.rounded_rectangle([140, yy - 38, 140 + wbar, yy + 38], radius=14, fill=A(COL[nm], kb))
            if g > 0.95: text(d, (140 + L * i / ROWS[0][2] + 30, yy), vn(i, 2) + " A", 44, COL[nm], anchor="lm", alpha=kb)
        k2 = appear(t, M[1] + 0.2, 0.4)
        if k2 > 0:
            xm = 140 + L / 2
            for y in range(985, 1220, 22): d.line([(xm, y), (xm, y + 12)], fill=A(DGREEN, k2), width=4)
            text(d, (W / 2, 1370), "0,15 = 0,30 : 2", 50, DGREEN, alpha=k2)

# ---------------- canh 4: Rut ra (dong manh / yeu -> R = U/I) ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    card(d, (40, 260, 1040, 700), fill=A(WHITE, k0), outline=A(LIGHT, k0), w=3)
    for cx, (nm, u, i, r) in zip((290, 790), ROWS):
        coil(d, cx, 420, nm, a=k0)
        wd = int(28 * i / ROWS[0][2])
        ka = appear(t, 0.6, 0.4) * k0
        arrow(d, (cx - 100, 540), (cx + 100, 540), A(RED, ka), w=wd, head=24 + wd)
        text(d, (cx, 630), "I = " + vn(i, 2) + " A", 44, RED, alpha=ka)
    k1 = appear(t, M[1] - 0.1, 0.45)
    if k1 > 0:
        card(d, (40, 740, 1040, 1070), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        text(d, (470, 850), "R =", 64, GREEN, alpha=k1)
        text(d, (600, 808), "U", 60, GREEN, alpha=k1)
        d.line([(560, 852), (640, 852)], fill=A(GREEN, k1), width=6)
        text(d, (600, 900), "I", 60, GREEN, alpha=k1)
        text(d, (W / 2, 1010), "R: điện trở, đơn vị ôm (Ω)", 42, DGREEN, alpha=k1)
    for j, (nm, u, i, r) in enumerate(ROWS):
        kr = appear(t, M[1] + 0.5 + 0.5 * j, 0.4)
        if kr <= 0: continue
        if j == 0: card(d, (40, 1110, 1040, 1420), fill=A(WHITE, kr), outline=A(LIGHT, kr), w=3)
        text(d, (W / 2, 1195 + j * 130), f"Dây {nm}: R = {vn(u)} : {vn(i, 2)} = {r:.0f} Ω", 46, mix(COL[nm], INK, 0.2), alpha=kr)

# ---------------- canh 5: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 560), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 320), "Cùng U = 3,0 V", 44, PURPLE)
    for cx, (nm, u, i, r) in zip((290, 790), ROWS):
        text(d, (cx, 410), "dây " + nm, 44, mix(COL[nm], INK, 0.25))
        text(d, (cx, 490), vn(i, 2) + " A", 48, BLUE)
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if a1 > 0:
        y0 = 600
        card(d, (40, y0, 1040, y0 + 860), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 40, WHITE, alpha=a1)
        q = "“Điện trở R = U · I”"
        ks = clamp((t - M[0] - 1.6) / 0.4)
        f = F(56); lw = tw(d, q, f); yy = y0 + 250
        text(d, (W / 2, yy), q, 56, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
            text(d, (W / 2 + lw / 2 + 40, yy), "✗", 56, DRED, alpha=a1 * ks)
        kk = a1 * appear(t, M[0] + 2.0, 0.4)
        card(d, (70, y0 + 420, 1010, y0 + 800), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 520), "✓ Phải chia: R = U : I", 48, DGREEN, alpha=kk)
        ctext(d, y0 + 670, "cùng U = 3 V:\nI nhỏ hơn → R lớn hơn", 46, DGREEN, alpha=kk)
    if k2 > 0:
        y0 = 600 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 780), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 95), "Chưa nói được", 52, NAVY, alpha=k2)
        for j, (l1, l2) in enumerate((("• Số liệu minh hoạ,", "chưa đo thật"),
                                      ("• Bỏ qua điện trở", "ampe kế, dây nối"))):
            kk = k2 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4)
            text(d, (90, y0 + 300 + j * 300), l1, 50, INK, anchor="lm", alpha=kk)
            text(d, (132, y0 + 375 + j * 300), l2, 50, INK, anchor="lm", alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
T_CHOT = 4.0   # o chot hien sau ~3,5 s nghi (canh dai 7,2 s)
def s_end(img, d, t, sc):
    M = sc["M"]
    # Khong dung chot_hoi: o chot "R = U : I" chi hien SAU thoi gian nghi (hien cung cau hoi = noi san cach lam).
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 > 0:
        card(d, (40, 620, 1040, 1600), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
        pw = tw(d, "THỬ NGHĨ", F(38)) + 52
        card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
        text(d, (W / 2, 682), "THỬ NGHĨ", 38, WHITE, alpha=k1)
        ctext(d, 820, f"Dây C: đặt {vn(U_C)} V, ampe kế chỉ 0,15 A.\nCản trở như dây A hay dây B?", 46, INK, maxw=880,
              alpha=appear(t, M[0] + 0.4, 0.5))
        coil(d, 540, 1110, "C", a=appear(t, M[0] + 0.6, 0.5) * k1, w=380, h=120, ls=46)
        kh = appear(t, M[0] + 2.9, 0.5)
        card(d, (110, 1270, 970, 1500), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1325, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1420, "Tự trả lời trước khi xem", 44, ORANGE, maxw=820, alpha=kh)
    k0 = appear(t, M[0] + T_CHOT, 0.5)   # sau thoi gian nghi
    if k0 > 0:
        card(d, (60, 260, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
        ctext(d, 410, "Điện trở: R = U : I", 52, GREEN, maxw=860, alpha=k0)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding"),
            (do["t0"] + T_A, "tap"), (do["t0"] + T_B, "tap"),
            (da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + 0.2, "buzz"),
            (b["t0"] + b["M"][0] + 2.0, "tap"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l9-ohm-01", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Điện trở · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai cuộn dây A và B", draw=s_hook, tail=0.8, caps=[
   ("Mạch đo U, I của từng dây.", 2.9),
   ("Dừng video, chọn câu trả lời.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Mắc dây A, đóng khoá K.", 3.7),
   ("Mở K, thay dây B, đóng lại.", 4.3)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Vôn kế giống, ampe kế khác.", 3.4),
   ("Dây B: dòng chỉ một nửa.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.6, caps=[
   ("Dòng nhỏ: dây cản trở nhiều.", 3.4),
   ("Đó là điện trở.", 3.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Có đúng không?", 4.4),
   ("Còn chưa nói được.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Dừng video, tự trả lời.", 6.0)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch R = U/I:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
