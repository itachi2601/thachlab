# Clip: tn-l9-congsuat-03 - Hai bong X 6 V - 3 W va Y 6 V - 6 W, noi tiep roi song song vao nguon 6 V (KHTN 9, 05/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-congsuat-03.json:
#   so_lieu_mau (cach mac, den, U V, I A, P W): noi tiep X 4,0 0,33 1,33 ; Y 2,0 0,33 0,67 ;
#                                              song song X 6,0 0,5 3,0 ; Y 6,0 1,0 6,0 (ghi_chu: tinh tu mo hinh, chua do that).
#   tham_so: R_X = 12 Ohm, R_Y = 6 Ohm (coi khong doi). quan_sat: noi tiep X sang hon, Y chi do mo; song song ca hai sang
#   binh thuong, Y sang hon X. rut_ra: noi tiep cung I, P = I^2R, R lon sang hon; song song dung dinh muc, nhieu oat sang hon.
#   Bay = hien_tuong_hay_sai[0] ("nhieu oat luon sang hon"); chua noi duoc = so_lieu_mau.ghi_chu + mo_hinh.gia_thiet[0].
# Sau hop trong bai: PhET (hai bong giong nhau noi tiep/song song; 10 Ohm - 20 Ohm tinh P) + Tra bai cau 6 -> clip khong
#   so sang hai cach mac voi nhau, khong tinh P cho 10/20 Ohm, khong viet "it oat sang hon" (de cau THU NGHI con phai tinh R).
# Du doan (K10: chi cau hoi + hinh): noi tiep roi song song, moi lan den nao sang hon? -> noi tiep X, song song Y.
#   Khac tn-l9-congsuat-01 (mot den, U.I o 3 V).
# Cau hoi chot: den Z 6 V - 2 W (chua tung hien) noi tiep voi X vao 6 V: den nao sang hon? (Z: R = 18 Ohm > 12 Ohm).
# Mach noi tiep: nguon (+) -> K -> ampe ke (+ trai) -> X -> Y -> ve (-); hai von ke song song moi den (+ phia nguon +).
# Mach song song: nguon (+) -> K -> nut trai -> nhanh X (ampe ke A_X + den X), nhanh Y (A_Y + Y) -> nut phai -> (-);
#   mot von ke song song hai nut. K mo: so chi 0, den tat. Kiem bang ma moi 0,05 s: _kiem_dong_bo(); P = U.I: _kiem_so().
# Bo cuc (khac l9congsuat1): Tien hanh mot canh doi mach + o so chi + hai bong lon; Ket qua = bang 5 cot;
#   Rut ra = hai the (noi tiep / song song) kem bong nho.
import math
from engine import *

ROWS = [("nối tiếp", "X", 4.0, 0.33, 1.33), ("nối tiếp", "Y", 2.0, 0.33, 0.67),
        ("song song", "X", 6.0, 0.50, 3.0), ("song song", "Y", 6.0, 1.00, 6.0)]     # so_lieu_mau
R_X, R_Y, U0 = 12.0, 6.0, 6.0                                                           # tham_so
# do sang ve theo P that (quan_sat): (muc sang 0..1, mau day toc, nhan)
LOOK = {("nt", "X"): (0.45, (215, 90, 25), "sáng hơn Y"), ("nt", "Y"): (0.12, (160, 45, 30), "chỉ đỏ mờ"),
        ("ss", "X"): (0.72, (230, 140, 10), "sáng bình thường"), ("ss", "Y"): (1.0, (225, 160, 0), "sáng hơn X")}
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
def vp(p): return vn(p, 1) if abs(p - round(p)) < 1e-9 else vn(p, 2)

WIRE = (60, 66, 92); BODY = (70, 78, 100); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30)
DGREEN = (21, 110, 55); DRED = (185, 28, 28); GLOW = (255, 214, 80); DORANGE = (154, 52, 18)

def bulb(d, cx, cy, r, look=None, alpha=1.0):
    """look = None (tat) hoac (muc sang, mau day toc, ...)."""
    if look is not None:
        b, fil = look[0], look[1]
        for i in range(4, 0, -1):
            rr = r + (12 * i * b + 10 * b) * r / 46
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=A(GLOW, (0.10 + 0.07 * b) * alpha))
        fill = mix(WHITE, (255, 226, 110), 0.15 + 0.85 * b); col = fil
    else:
        fill, col = WHITE, NAVY
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=A(fill, alpha), outline=A(NAVY, alpha), width=6)
    q = r * 0.68
    d.line([(cx - q, cy - q), (cx + q, cy + q)], fill=A(col, alpha), width=6)
    d.line([(cx - q, cy + q), (cx + q, cy - q)], fill=A(col, alpha), width=6)

# ---------------- so do mach (the 260-790) ----------------
XL, XR, TY, BY = 150, 990, 440, 740
KX0, KX1 = 240, 320

def source_k(d, closed):
    card(d, (40, 260, 1040, 790), fill=WHITE, outline=LIGHT, w=3)
    card(d, (95, 500, 205, 680), fill=BODY, r=16)
    text(d, (150, 590), "6 V", 40, WHITE)
    text(d, (70, 515), "+", 44, ORANGE); text(d, (70, 665), "−", 44, ORANGE)
    d.line([(XL, 500), (XL, TY), (KX0, TY)], fill=WIRE, width=6, joint="curve")
    d.line([(XL, 680), (XL, BY)], fill=WIRE, width=6)
    dot(d, KX0, TY, 9, WIRE); dot(d, KX1, TY, 9, WIRE)
    if closed: d.line([(KX0, TY), (KX1, TY)], fill=NAVY, width=7)
    else: d.line([(KX0, TY), (KX0 + 80 * math.cos(math.radians(32)), TY - 80 * math.sin(math.radians(32)))], fill=NAVY, width=7)
    text(d, ((KX0 + KX1) / 2, TY + 46), "K", 40, NAVY)

def meter(d, cx, cy, ch, col, r=42):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=col, width=6)
    text(d, (cx, cy + 2), ch, 42, col)

AX, NX, NY, VY = 430, 610, 840, 610
def circuit_nt(d, closed, on):
    source_k(d, closed)
    w = 6
    d.line([(KX1, TY), (AX - 42, TY)], fill=WIRE, width=w)
    d.line([(AX + 42, TY), (NX - 46, TY)], fill=WIRE, width=w)
    d.line([(NX + 46, TY), (NY - 46, TY)], fill=WIRE, width=w)
    d.line([(NY + 46, TY), (XR, TY), (XR, BY), (XL, BY)], fill=WIRE, width=w, joint="curve")
    for cx in (NX, NY):    # von ke song song moi den
        a, b = cx - 85, cx + 85
        d.line([(a, TY), (a, VY), (cx - 40, VY)], fill=WIRE, width=5, joint="curve")
        d.line([(cx + 40, VY), (b, VY), (b, TY)], fill=WIRE, width=5, joint="curve")
        dot(d, a, TY, 9, WIRE); dot(d, b, TY, 9, WIRE)
        meter(d, cx, VY, "V", PURPLE, 40); text(d, (cx - 60, VY - 44), "+", 40, PURPLE)
    meter(d, AX, TY, "A", BLUE); text(d, (AX - 64, TY + 40), "+", 40, BLUE)
    for cx, nm in ((NX, "X"), (NY, "Y")):
        bulb(d, cx, TY, 46, LOOK[("nt", nm)] if on else None)
        text(d, (cx, TY - 82), nm, 46, INK)
    if on:
        arrow(d, (600, BY + 26), (520, BY + 26), RED, w=5, head=16); text(d, (620, BY + 26), "I", 40, RED, anchor="lm")

NL, NR, YB, VT, BAX, BLX = 430, 930, 610, 330, 540, 740
def circuit_ss(d, closed, on):
    source_k(d, closed)
    w = 6
    d.line([(KX1, TY), (NL, TY), (NL, YB), (BAX - 42, YB)], fill=WIRE, width=w, joint="curve")
    d.line([(NL, TY), (BAX - 42, TY)], fill=WIRE, width=w)
    for y in (TY, YB):
        d.line([(BAX + 42, y), (BLX - 46, y)], fill=WIRE, width=w)
        d.line([(BLX + 46, y), (NR, y)], fill=WIRE, width=w)
    d.line([(NR, TY), (NR, BY), (XL, BY)], fill=WIRE, width=w, joint="curve")
    # von ke song song hai nut
    d.line([(NL, TY), (NL, VT), (680 - 38, VT)], fill=WIRE, width=5, joint="curve")
    d.line([(680 + 38, VT), (NR, VT), (NR, TY)], fill=WIRE, width=5, joint="curve")
    for p in ((NL, TY), (NR, TY), (NR, YB)): dot(d, p[0], p[1], 10, WIRE)
    meter(d, 680, VT, "V", PURPLE, 38); text(d, (625, VT - 38), "+", 40, PURPLE)
    for y, nm in ((TY, "X"), (YB, "Y")):
        meter(d, BAX, y, "A", BLUE); text(d, (BAX - 62, y + 40), "+", 40, BLUE)
        bulb(d, BLX, y, 46, LOOK[("ss", nm)] if on else None)
        text(d, (BLX + 92, y - 44), nm, 46, INK)
    if on:
        arrow(d, (600, BY + 26), (520, BY + 26), RED, w=5, head=16); text(d, (620, BY + 26), "I tổng", 40, RED, anchor="lm")

def readouts(d, items):
    for j, (lab, val) in enumerate(items):
        x0 = 50 + j * 340
        card(d, (x0, 820, x0 + 300, 990), fill=BODY, r=22)
        text(d, (x0 + 150, 860), lab, 40, WHITE, bold=False)
        card(d, (x0 + 24, 894, x0 + 276, 970), fill=SCREEN, r=12)
        text(d, (x0 + 150, 932), val, 52, SCR_INK)

def big_lamps(d, mode, on):
    card(d, (40, 1020, 1040, 1520), fill=WHITE, outline=LIGHT, w=3)
    for cx, nm, pdm in ((300, "X", 3), (780, "Y", 6)):
        lk = LOOK[(mode, nm)] if on else None
        bulb(d, cx, 1190, 80, lk)
        text(d, (cx, 1340), f"{nm} · 6 V – {pdm} W", 44, INK)
        if on: text(d, (cx, 1430), lk[2], 44, mix(lk[1], INK, 0.3))

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
THINK_END = 0.7
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 740), fill=WHITE, outline=LIGHT, w=3)
    for cx, nm, pdm in ((300, "X", 3), (780, "Y", 6)):
        bulb(d, cx, 440, 90)
        text(d, (cx, 600), f"{nm}: 6 V – {pdm} W", 46, INK)
    # hai so do nho: noi tiep / song song
    card(d, (40, 770, 520, 970), fill=WHITE, outline=LIGHT, w=3)
    text(d, (280, 808), "nối tiếp", 40, INK)
    d.line([(90, 905), (470, 905)], fill=WIRE, width=5)
    for cx in (215, 345): d.ellipse([cx - 28, 877, cx + 28, 933], fill=WHITE, outline=NAVY, width=5)
    card(d, (560, 770, 1040, 970), fill=WHITE, outline=LIGHT, w=3)
    text(d, (800, 808), "song song", 40, INK)
    d.line([(610, 900), (690, 900)], fill=WIRE, width=5); d.line([(910, 900), (990, 900)], fill=WIRE, width=5)
    d.line([(690, 860), (690, 940)], fill=WIRE, width=5); d.line([(910, 860), (910, 940)], fill=WIRE, width=5)
    for y in (860, 940):
        d.line([(690, y), (910, y)], fill=WIRE, width=5)
        d.ellipse([800 - 20, y - 20, 800 + 20, y + 20], fill=WHITE, outline=NAVY, width=5)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 245, "Nối tiếp, rồi song song\nvào 6 V: mỗi lần\nđèn nào sáng hơn?", 50, INK, maxw=900, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 420, 940, y0 + 432], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 420, 140 + 800 * (1 - p), y0 + 432], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (mot canh, doi mach o phu de 2) ----------------
T_K = 0.8         # dong K sau khi mach hien 0,8 s
def do_state(t, sc):
    """-> (mach 'nt'|'ss', K dong?)."""
    t_sw = sc["M"][1] - 0.05
    if t < t_sw: return "nt", t >= T_K - 1e-9
    return "ss", t >= t_sw + T_K - 1e-9

def readings(mode, closed):
    if mode == "nt":
        x, y = ROWS[0], ROWS[1]
        if not closed: return [("U đèn X", "0,0 V"), ("U đèn Y", "0,0 V"), ("I (chung)", "0,00 A")]
        return [("U đèn X", vn(x[2]) + " V"), ("U đèn Y", vn(y[2]) + " V"), ("I (chung)", vn(x[3], 2) + " A")]
    x, y = ROWS[2], ROWS[3]
    if not closed: return [("U (chung)", "0,0 V"), ("I đèn X", "0,00 A"), ("I đèn Y", "0,00 A")]
    return [("U (chung)", vn(x[2]) + " V"), ("I đèn X", vn(x[3], 2) + " A"), ("I đèn Y", vn(y[3], 2) + " A")]

def s_do(img, d, t, sc):
    mode, closed = do_state(t, sc)
    (circuit_nt if mode == "nt" else circuit_ss)(d, closed, closed)
    readouts(d, readings(mode, closed))
    big_lamps(d, mode, closed)

def _kiem_dong_bo():
    """Moi 0,05 s: K mo <=> so chi 0 va den tat; K dong <=> so chi dung hang kho cua mach dang ve."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        mode, closed = do_state(t, sc); r = readings(mode, closed)
        zero = all(v.startswith("0,0") for _, v in r)
        if closed == zero: bad.append((round(t, 2), mode, closed))
        if closed and mode == "nt" and (r[0][1], r[1][1]) != ("4,0 V", "2,0 V"): bad.append((round(t, 2), "U nt"))
        if closed and mode == "ss" and (r[1][1], r[2][1]) != ("0,50 A", "1,00 A"): bad.append((round(t, 2), "I ss"))
        t += 0.05
    return bad

def _kiem_so():
    bad = [r for r in ROWS if abs(r[2] * r[3] - r[4]) > 0.02]                       # P = U.I
    bad += [r for r in ROWS if abs(r[3] * (R_X if r[1] == "X" else R_Y) - r[2]) > 0.05]  # U = I.R
    if abs(ROWS[0][2] + ROWS[1][2] - U0) > 1e-9: bad.append("U nt cong lai")
    if ROWS[0][3] != ROWS[1][3]: bad.append("I nt khac nhau")
    rz = 6.0 ** 2 / 2.0
    if not rz > R_X: bad.append("cau chot")
    return bad

# ---------------- canh 3: Ket qua (bang 5 cot) ----------------
TX = (180, 390, 555, 735, 920)
RY = (555, 650, 770, 865)
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · nối tiếp X, song song Y"
    pw = tw(d, lab, F(42)) + 60
    card(d, (W / 2 - pw / 2, 272, W / 2 + pw / 2, 344), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 308), lab, 42, WHITE, alpha=ka)
    card(d, (40, 380, 1040, 930), fill=WHITE, outline=LIGHT, w=3)
    kh = appear(t, M[1] - 0.1, 0.45)
    for j in (0, 3):     # den sang hon moi cach mac
        if kh > 0: d.rounded_rectangle([300, RY[j] - 42, 1020, RY[j] + 42], radius=20, fill=A((255, 237, 213), kh))
    kp = appear(t, M[0] + 0.3, 0.4)
    for x, h, c in zip(TX, ("Cách mắc", "Đèn", "U (V)", "I (A)", "P (W)"), (INK, INK, NAVY, BLUE, ORANGE)):
        text(d, (x, 440), h, 42, c, alpha=(kp if h.startswith("P") else 1.0))
    d.line([(70, 490), (1010, 490)], fill=LIGHT, width=3)
    d.line([(70, 712), (1010, 712)], fill=LIGHT, width=3)
    text(d, (TX[0], (RY[0] + RY[1]) / 2), "nối tiếp", 42, INK)
    text(d, (TX[0], (RY[2] + RY[3]) / 2), "song song", 42, INK)
    for j, (_, nm, u, i, p) in enumerate(ROWS):
        yy = RY[j]
        text(d, (TX[1], yy), nm, 48, INK)
        text(d, (TX[2], yy), vn(u), 48, NAVY)
        text(d, (TX[3], yy), ("≈ " if j < 2 else "") + vn(i, 2), 48, BLUE)
        k = appear(t, M[0] + 0.6 + 0.35 * j, 0.35)
        if k > 0: text(d, (TX[4], yy), vp(p), 48, ORANGE, alpha=k)
    k2 = appear(t, M[0] + 0.3, 0.45)
    if k2 > 0:
        y0 = 970 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 270), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, y0 + 85), "P = U·I", 60, GREEN, alpha=k2)
        text(d, (W / 2, y0 + 185), "P: công suất (oát, W)", 42, DGREEN, alpha=k2)

# ---------------- canh 4: Rut ra (hai the) ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, M[0] + 0.2, 0.45)
    if k1 > 0:
        card(d, (40, 290, 1040, 800), fill=A((255, 247, 237), k1), outline=A(ORANGE, k1), w=5)
        text(d, (W / 2, 355), "Nối tiếp: cùng I", 52, DORANGE, alpha=k1)
        kb = k1 * appear(t, M[0] + 0.9, 0.4)
        for cx, nm, r, lk in ((300, "X", R_X, LOOK[("nt", "X")]), (780, "Y", R_Y, LOOK[("nt", "Y")])):
            bulb(d, cx, 500, 56, lk, alpha=kb)
            text(d, (cx, 625), f"{nm}: R = {int(r)} Ω", 44, INK, alpha=kb)
        kc = k1 * appear(t, M[0] + 1.8, 0.4)
        text(d, (W / 2, 735), "P = I²R, cùng I", 44, DORANGE, alpha=kc)
        text(d, (W / 2, 420), "(R: điện trở)", 40, MUTED, bold=False, alpha=kb)
    k2 = appear(t, M[1] + 0.1, 0.45)
    if k2 > 0:
        y0 = 850 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 500), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, y0 + 65), "Song song: cùng U = 6 V", 52, DGREEN, alpha=k2)
        kb = k2 * appear(t, M[1] + 0.7, 0.4)
        for cx, nm, pdm, lk in ((300, "X", 3, LOOK[("ss", "X")]), (780, "Y", 6, LOOK[("ss", "Y")])):
            bulb(d, cx, y0 + 215, 56, lk, alpha=kb)
            text(d, (cx, y0 + 335), f"{nm}: {pdm} W", 44, INK, alpha=kb)
        kc = k2 * appear(t, M[1] + 1.4, 0.4)
        text(d, (W / 2, y0 + 440), "Đúng định mức: P = số ghi", 44, DGREEN, alpha=kc)

# ---------------- canh 5: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a0 = appear(t, 0.2, 0.45)
    card(d, (40, 280, 1040, 720), fill=A(WHITE, a0), outline=A(LIGHT, a0), w=3)
    for cx, nm, pdm in ((300, "X", 3), (780, "Y", 6)):
        lk = LOOK[("nt", nm)]
        bulb(d, cx, 500, 72, lk, alpha=a0)
        text(d, (cx, 640), f"{nm} · {pdm} W" + (": đỏ mờ" if nm == "Y" else ""), 42, mix(lk[1], INK, 0.3), alpha=a0)
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if a1 > 0:
        y0 = 770
        kk0 = appear(t, M[0] + 2.4, 0.4)
        card(d, (40, y0, 1040, y0 + 250 + 190 * kk0), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 40, WHITE, alpha=a1)
        q = "“Đèn nhiều oát luôn sáng hơn”"
        ks = clamp((t - M[0] - 2.2) / 0.4)
        f = F(48); lw = tw(d, q, f); yy = y0 + 170
        text(d, (W / 2 - 20, yy), q, 48, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0:
            x0 = W / 2 - 20 - lw / 2 - 6
            d.line([(x0, yy + 2), (x0 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
            text(d, (W / 2 - 20 + lw / 2 + 40, yy), "✗", 48, DRED, alpha=a1 * ks)
        kk = a1 * kk0
        if kk > 0: card(d, (70, y0 + 270, 1010, y0 + 400), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 335), "✓ Chỉ đúng khi cùng U định mức", 44, DGREEN, alpha=kk)
    if k2 > 0:
        y0 = 770 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 380), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 75), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Số liệu tính, chưa đo thật", "• Coi điện trở đèn không đổi")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4)
            text(d, (80, y0 + 190 + j * 110), l1, 46, INK, anchor="lm", alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def fig(d, t, k):
        kf = appear(t, M[0] + 0.4, 0.5)
        x0, x1, yt, yb, bx = 150, 930, 1040, 1190, 540
        d.line([(bx - 14, yb), (x0, yb), (x0, yt), (x1, yt), (x1, yb), (bx + 14, yb)], fill=A(WIRE, kf), width=5, joint="curve")
        d.line([(bx - 14, yb - 34), (bx - 14, yb + 34)], fill=A(NAVY, kf), width=5)    # cuc + (vach dai)
        d.line([(bx + 14, yb - 18), (bx + 14, yb + 18)], fill=A(NAVY, kf), width=11)   # cuc - (vach ngan)
        text(d, (bx - 50, yb - 34), "+", 40, ORANGE, alpha=kf); text(d, (bx + 50, yb - 34), "−", 40, ORANGE, alpha=kf)
        text(d, (bx + 90, yb + 4), "6 V", 40, INK, anchor="lm", alpha=kf)
        for cx, lab in ((390, "Z · 6 V – 2 W"), (690, "X · 6 V – 3 W")):
            d.ellipse([cx - 46, yt - 46, cx + 46, yt + 46], fill=A(WHITE, kf), outline=A(NAVY, kf), width=6)
            text(d, (cx, yt), "?", 46, NAVY, alpha=kf)
            text(d, (cx, yt - 88), lab, 40, INK, alpha=kf)
        card(d, (110, 1280, 970, 1520), fill=A((255, 247, 237), kf), r=24)
        ctext(d, 1335, "Gợi ý", 40, MUTED, bold=False, alpha=kf)
        kh = appear(t, M[0] + 0.4 + 2.5, 0.5)
        ctext(d, 1435, "Nối tiếp thì cùng I", 44, ORANGE, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Sáng theo P thật, không theo số ghi",
             "Z nối tiếp X vào 6 V: đèn nào sáng hơn?", body=fig)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    t_sw = do["M"][1] - 0.05
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding"),
            (do["t0"] + T_K, "tap"), (do["t0"] + t_sw + T_K, "tap"),
            (da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] + 0.1, "tap"), (b["t0"] + 0.2, "buzz"),
            (b["t0"] + b["M"][0] + 2.4, "tap"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l9-congsuat-03", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Công suất điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai bóng đèn, một nguồn 6 V", draw=s_hook, tail=0.8, caps=[
   ("Hai đèn khác số oát.", 3.0),
   ("Dừng video, chọn câu trả lời.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Nối tiếp trước: đóng K, nhìn đèn.", 3.9),
   ("Rồi đổi sang mắc song song.", 3.9)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Nhân U với I cho từng đèn.", 3.0),
   ("Thứ tự sáng đổi ngược.", 3.2)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Vì sao đèn X sáng hơn lúc đầu?", 3.8),
   ("Còn song song thì sao?", 3.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Đúng không?", 4.4),
   ("Còn giới hạn gì?", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 5.6)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch số:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
