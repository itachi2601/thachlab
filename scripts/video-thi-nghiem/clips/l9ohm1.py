# Clip: tn-l9-ohm-01 - Cung hieu dien the 3 V, hai day A, B cho hai dong dien khac nhau -> dien tro (KHTN 9, 05/11/2026)
# Dung lai 27/11/2026 theo cong moi (viec 4, L9 nhom A): chu than canh >= 56 (ra >= 49 px), nhan don le, khong nut A-D (K10),
#   thanh dem day 90 px, moi nhip >= 3 s co phu de, khoi chu cach >= 2,5 s, Bay = hai cot canh nhau (U.I sai / U:I dung).
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-ohm-01.json (_kiem_so()):
#   so_lieu_mau (Day, U V, I A, R Ohm): A 3,0 0,30 10 ; B 3,0 0,15 20 (ghi_chu: so lieu minh hoa).
#   tham_so: U 1,5..6 V buoc 1,5 (cau chot dung 1,5 V = min). bay = hien_tuong_hay_sai[1] (R = U.I):
#   U.I tu suy: A 0,9 ; B 0,45 (chi de cho thay "B nho hon A" nguoc voi "B can nhieu hon").
# Cau trong bai KHONG duoc giai trong clip: Cau 1 (6 V, 200 mA -> 30 Ohm), Cau 4 (15 Ohm, 3 V -> 6 V), Cau 5 (3 V: 0,3 / 0,1 A).
# Du doan (K10: chi cau hoi + hinh): van 3 V, thay day A bang day B -> ampe ke chi the nao? -> nho hon 0,30 A (0,15 A).
# THU NGHI = cau_chot khung web: day C dat 1,5 V (chua tung chieu) chi 0,15 A -> can nhu day A hay B?
#   dap an: nhu day A (1,5 : 0,15 = 10 Ohm), nguoc phan xa "cung 0,15 A nhu B". Can mot buoc chua chieu: U khac 3 V.
#   Man chot KHONG in 10 Ohm cua day C, khong in phep chia.
# Mach: nguon (+ ben trai) -> K -> ampe ke (+ ben trai) -> day; von ke SONG SONG voi day. K mo: 0,0 V ; 0,00 A.
import math
from engine import *

ROWS = [("A", 3.0, 0.30, 10.0), ("B", 3.0, 0.15, 20.0)]      # so_lieu_mau
U_C, I_C = 1.5, 0.15                                          # cau chot: tham_so U min ; I = U/R_A
I_MAX = 1.0                                                   # GHD ampe ke
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")


def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-ohm-01.json")))
    hang = k["so_lieu_mau"]["hang"]
    assert [tuple(h) for h in hang] == [(n, u, i, r) for n, u, i, r in ROWS], hang
    for n, u, i, r in ROWS: assert abs(u / i - r) < 1e-9
    tu = k["tham_so"][0]; assert tu["min"] == U_C and tu["ky_hieu"] == "U"
    assert abs(U_C / I_C - ROWS[0][3]) < 1e-9 and I_C == ROWS[1][2]        # C can nhu A, cung dong voi B (bay phan xa)
    assert [d["gia_tri"] for d in k["tham_so"][1:3]] == [10, 20]
_kiem_so()

WIRE = (60, 66, 92); BODY = (70, 78, 100); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30)
DGREEN = (21, 110, 55); DRED = (185, 28, 28); DPURP = (76, 29, 149)
CA, CB, CC = TEAL, ORANGE, PURPLE
COL = {"A": CA, "B": CB, "C": CC}
FS, FL = 56, 60     # chu nho nhat / chu chinh (ve) -> 49 / 53 px trong mp4

# ---------------- so do mach ----------------
TY, BY, XL, XR = 380, 690, 130, 950
AX, S0, S1, N1, N2, VX, VY, BX = 320, 560, 860, 525, 895, 710, 540, 540
KT, KB = 470, 590


def coil(d, cx, cy, name, a=1.0, w=250, h=78, lab=True, ly=None):
    col = COL[name]
    card(d, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), fill=A(mix(WHITE, col, 0.25), a), outline=A(col, a), r=16, w=5)
    for k in range(7):
        x = cx - w / 2 + 24 + k * (w - 48) / 6
        d.line([(x - 10, cy - h / 2 + 9), (x + 10, cy + h / 2 - 9)], fill=A(col, a), width=5)
    if lab: text(d, (cx, ly if ly is not None else cy - h / 2 - 44), "dây " + name, FS, mix(col, INK, 0.3), alpha=a)


def circuit(d, wire, closed, wa=1.0):
    """wire = 'A' / 'B' (cho mac day); wa = alpha cuon day (luc thay day)."""
    card(d, (40, 262, 1040, 770), fill=WHITE, outline=LIGHT, w=3)
    w = 6
    d.line([(XL, KT), (XL, TY), (AX - 52, TY)], fill=WIRE, width=w, joint="curve")
    d.line([(AX + 52, TY), (S0, TY)], fill=WIRE, width=w)
    d.line([(S1, TY), (XR, TY), (XR, BY), (BX + 24, BY)], fill=WIRE, width=w, joint="curve")
    d.line([(BX - 24, BY), (XL, BY), (XL, KB)], fill=WIRE, width=w, joint="curve")
    # von ke song song voi day
    d.line([(N1, TY), (N1, VY + 30), (VX - 52, VY + 30)], fill=WIRE, width=5, joint="curve")
    d.line([(VX + 52, VY + 30), (N2, VY + 30), (N2, TY)], fill=WIRE, width=5, joint="curve")
    for x in (N1, N2): dot(d, x, TY, 9, WIRE)
    d.ellipse([VX - 52, VY - 22, VX + 52, VY + 82], fill=WHITE, outline=PURPLE, width=6); text(d, (VX, VY + 30), "V", FL, PURPLE)
    text(d, (VX - 90, VY - 10), "+", FL, PURPLE)
    # ampe ke noi tiep
    d.ellipse([AX - 52, TY - 52, AX + 52, TY + 52], fill=WHITE, outline=BLUE, width=6); text(d, (AX, TY + 2), "A", FL, BLUE)
    text(d, (AX - 82, TY + 50), "+", FL, BLUE)
    # cho mac day
    dot(d, S0, TY, 8, WIRE); dot(d, S1, TY, 8, WIRE)
    if wa < 1:
        for x in range(S0 + 10, S1 - 10, 26): d.line([(x, TY), (x + 12, TY)], fill=GRAY, width=4)
    if wa > 0: coil(d, (S0 + S1) / 2, TY, wire, a=wa)
    # khoa K (canh trai)
    dot(d, XL, KT, 9, WIRE); dot(d, XL, KB, 9, WIRE)
    if closed: d.line([(XL, KB), (XL, KT)], fill=NAVY, width=7)
    else: d.line([(XL, KB), (XL + 60, KT + 14)], fill=NAVY, width=7)
    text(d, (XL - 52, (KT + KB) / 2), "K", FL, NAVY)
    # nguon 3 V: ban dai (+) ben trai
    d.line([(BX - 20, BY - 50), (BX - 20, BY + 50)], fill=NAVY, width=6)
    d.line([(BX + 20, BY - 26), (BX + 20, BY + 26)], fill=NAVY, width=14)
    text(d, (BX - 66, BY - 40), "+", FL, ORANGE); text(d, (BX + 66, BY - 40), "−", FL, ORANGE)
    text(d, (BX + 210, BY + 38), "3 V", FL, ORANGE)
    if closed:
        arrow(d, (175, TY - 40), (245, TY - 40), RED, w=6, head=18)


def ang(v): return math.radians(200 + 140 * clamp(v / I_MAX))


def dial(d, cx, cy, r, v, txt, col=RED, alpha=1.0):
    d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=340, fill=A(NAVY, alpha), width=5)
    for k in range(21):
        a = ang(k * 0.05); L = 30 if k % 10 == 0 else (20 if k % 2 == 0 else 12)
        d.line([(cx + r * math.cos(a), cy + r * math.sin(a)), (cx + (r - L) * math.cos(a), cy + (r - L) * math.sin(a))],
               fill=A(NAVY, alpha), width=4 if k % 2 == 0 else 3)
    for lv, s in ((0, "0"), (0.5, "0,5"), (1, "1")):
        a = ang(lv)
        text(d, (cx + (r - 64) * math.cos(a), cy + (r - 64) * math.sin(a)), s, FS, NAVY, alpha=alpha)
    a = ang(v)
    d.line([(cx, cy), (cx + (r - 18) * math.cos(a), cy + (r - 18) * math.sin(a))], fill=A(col, alpha), width=7)
    dot(d, cx, cy, 13, A(NAVY, alpha))
    if txt: text(d, (cx, cy + 62), txt, FL, col, alpha=alpha)


def meters(d, needle, itxt, utxt, closed):
    card(d, (40, 795, 620, 1255), fill=WHITE, outline=LIGHT, w=3)
    dial(d, 330, 1120, 240, needle, itxt)
    text(d, (330, 1000), "A", FL, BLUE)
    card(d, (660, 795, 1040, 1065), fill=BODY, r=22)
    text(d, (850, 850), "V", FL, WHITE)
    card(d, (690, 905, 1010, 1035), fill=SCREEN, r=12)
    text(d, (850, 970), utxt, 64, SCR_INK)
    card(d, (660, 1095, 1040, 1255), fill=WHITE, outline=LIGHT, w=3)
    text(d, (850, 1175), "K đóng" if closed else "K mở", FL, NAVY if closed else DPURP)


XS = (200, 520, 840)
def table(d, n, hl=None, y=1285):
    card(d, (40, y, 1040, y + 330), fill=WHITE, outline=LIGHT, w=3)
    for x, h in zip(XS, ("Dây", "U (V)", "I (A)")): text(d, (x, y + 55), h, FS, INK)
    d.line([(70, y + 102), (1010, y + 102)], fill=LIGHT, width=3)
    for j, (nm, u, i, r) in enumerate(ROWS):
        yy = y + 165 + j * 100
        if hl == j: d.rounded_rectangle([60, yy - 44, 1020, yy + 44], radius=20, fill=(255, 237, 213))
        if j < n:
            text(d, (XS[0], yy), nm, FL, mix(COL[nm], INK, 0.3)); text(d, (XS[1], yy), vn(u), FL, NAVY)
            text(d, (XS[2], yy), vn(i, 2), FL, BLUE)
        else:
            for x in XS: text(d, (x, yy), "…", FS, MUTED)


# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    nd = ROWS[0][2] * ease((t - 0.6) / 0.6)
    circuit(d, "A", True)
    meters(d, nd, vn(ROWS[0][2], 2) + " A" if t > 1.2 else "…", vn(ROWS[0][1]) + " V", True)
    table(d, 0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 800 + (1 - a) * 40
    card(d, (26, y0 - 20, 1054, y0 + 800), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(FS)) + 60
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 102), fill=A(PURPLE, a), r=38)
    text(d, (W / 2, y0 + 62), "DỰ ĐOÁN", FS, WHITE, alpha=a)
    coil(d, 290, y0 + 270, "A", a=a, ly=y0 + 180); coil(d, 790, y0 + 270, "B", a=a, ly=y0 + 180)
    arrow(d, (445, y0 + 270), (635, y0 + 270), A(NAVY, a), w=7, head=22)
    text(d, (W / 2, y0 + 430), "Vẫn 3 V, thay dây A bằng B.", FL, INK, alpha=a)
    text(d, (W / 2, y0 + 515), "Ampe kế chỉ thế nào?", FL, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:   # thanh dem nguoc day 90 px (doi du lon de khong tinh la hinh dung yen)
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 620, 970, y0 + 710], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 620, 110 + max(90, 860 * (1 - p)), y0 + 710], radius=45, fill=A(DPURP, a))


# ---------------- canh 2: Tien hanh ----------------
T_A, T_OPEN, T_OUT, T_IN, T_B = 0.9, 3.9, 4.1, 4.6, 5.2   # dong K voi A ; mo K ; thao A ; lap B ; dong K voi B
T_ROW, T_NEEDLE = 0.5, 0.35


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
    needle = needle_at(t)
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
        if n == 2 and not (wire == "B" and closed): bad.append((round(t, 2), "hang B truoc khi do"))
        nd = needle_at(t); tx = itxt(nd, i)
        if tx != "…" and (tx != vn(i, 2) + " A" or abs(nd - i) > 0.005): bad.append((round(t, 2), "chu ampe ke lech kim", tx))
        t += 0.05
    return bad


# ---------------- canh 3: Ket qua (hai kim canh nhau) ----------------
def pill(d, s, y, a, color=NAVY, size=FS):
    pw = tw(d, s, F(size)) + 64
    card(d, (W / 2 - pw / 2, y - 42, W / 2 + pw / 2, y + 42), fill=A(color, a), r=40)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


T_HALF = 4.1
def s_dapan(img, d, t, sc):
    ka = appear(t, 0.15, 0.4)
    pill(d, "ĐÁP ÁN: nhỏ hơn 0,30 A", 310, ka)
    for x0, (nm, u, i, r) in zip((40, 560), ROWS):
        cx = x0 + 240
        card(d, (x0, 395, x0 + 480, 960), fill=A(WHITE, ka), outline=A(COL[nm], ka), w=5)
        text(d, (cx, 450), "dây " + nm, FL, mix(COL[nm], INK, 0.3), alpha=ka)
        dial(d, cx, 770, 200, i * appear(t, 0.5, 0.6), vn(i, 2) + " A", alpha=ka)
        text(d, (cx, 922), vn(u) + " V", FL, PURPLE, alpha=ka)
    # nua vach: kim B dung o dung nua kim A (cung thang do)
    k2 = appear(t, T_HALF, 0.45)
    if k2 > 0:
        card(d, (110, 1010, 970, 1130), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=26, w=4)
        text(d, (W / 2, 1070), "0,15 = 0,30 : 2", 64, DGREEN, alpha=k2)


# ---------------- canh 4: Rut ra ----------------
T_R, T_ROWR = None, None
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    card(d, (40, 262, 1040, 700), fill=A(WHITE, k0), outline=A(LIGHT, k0), w=3)
    for cx, (nm, u, i, r) in zip((290, 790), ROWS):
        coil(d, cx, 430, nm, a=k0)
        wd = int(30 * i / ROWS[0][2])
        ka = appear(t, 0.5, 0.4) * k0
        arrow(d, (cx - 110, 555), (cx + 110, 555), A(RED, ka), w=wd, head=26 + wd)
        # hat mang dien chay: day A nhanh gap doi day B
        if ka > 0:
            for q in range(4):
                x = cx - 110 + ((t * 140 * i / ROWS[1][2] + q * 55) % 220)
                dot(d, x, 610, 10, A(BLUE, ka))
        text(d, (cx, 660), vn(i, 2) + " A", FS, RED, alpha=ka)
    k1 = appear(t, M[1] - 0.1, 0.45)
    if k1 > 0:
        card(d, (40, 740, 1040, 1090), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        text(d, (450, 860), "R =", 72, GREEN, alpha=k1)
        text(d, (590, 815), "U", 66, GREEN, alpha=k1)
        d.line([(545, 862), (635, 862)], fill=A(GREEN, k1), width=6)
        text(d, (590, 910), "I", 66, GREEN, alpha=k1)
        text(d, (W / 2, 1025), "điện trở, đơn vị ôm (Ω)", FL, DGREEN, alpha=k1)
    kr = appear(t, M[1] + 2.5, 0.4)
    if kr > 0:
        card(d, (40, 1130, 1040, 1440), fill=A(WHITE, kr), outline=A(LIGHT, kr), w=3)
        for j, (nm, u, i, r) in enumerate(ROWS):
            text(d, (W / 2, 1215 + j * 130), f"Dây {nm}: {vn(u)} : {vn(i, 2)} = {r:.0f} Ω", FL, mix(COL[nm], INK, 0.3), alpha=kr)


# ---------------- canh 5: Bay (hai cot canh nhau) roi Chua noi duoc ----------------
BAY_R, BAY_C = 3.4, 6.4
def bars(d, x0, vals, top, col, k, ka, unit=""):
    """Hai cot A, B trong o rong 460 bat dau x0; top = gia tri lon nhat (cot cao 300)."""
    base = 1080
    d.line([(x0 + 30, base), (x0 + 430, base)], fill=A(INK, ka), width=4)
    for j, (nm, v, s) in enumerate(vals):
        cx = x0 + 130 + 200 * j; h = 300 * v / top * k
        if h > 0: d.rectangle([cx - 60, base - h, cx + 60, base], fill=A(COL[nm], ka))
        text(d, (cx, base - 300 * v / top - 45), s, FL, mix(COL[nm], INK, 0.3), alpha=ka * k)
        text(d, (cx, base + 50), nm, FL, mix(COL[nm], INK, 0.3), alpha=ka)


def s_bay(img, d, t, sc):
    a1 = appear(t, 0.3, 0.45)
    pw = tw(d, "BẪY", F(FS)) + 64
    card(d, (W / 2 - pw / 2, 268, W / 2 + pw / 2, 348), fill=A(DRED, a1), r=40)
    text(d, (W / 2, 308), "BẪY", FS, WHITE, alpha=a1)
    card(d, (40, 390, 530, 1260), fill=A(WHITE, a1), outline=A(DRED, a1), w=5)
    text(d, (285, 455), "R = U·I", 68, DRED, alpha=a1)
    text(d, (285, 535), "(V·A)", FS, DRED, alpha=a1)
    bars(d, 55, (("A", 0.9, "0,9"), ("B", 0.45, "0,45")), 0.9, DRED, appear(t, 0.6, 1.0), a1)
    text(d, (285, 1200), "✗ B nhỏ hơn A", FL, DRED, alpha=a1)
    a2 = appear(t, BAY_R, 0.45)
    if a2 > 0:
        card(d, (550, 390, 1040, 1260), fill=A(WHITE, a2), outline=A(DGREEN, a2), w=5)
        text(d, (795, 455), "R = U : I", 68, DGREEN, alpha=a2)
        text(d, (795, 535), "(Ω)", FS, DGREEN, alpha=a2)
        bars(d, 565, (("A", 10, "10"), ("B", 20, "20")), 20, DGREEN, appear(t, BAY_R, 0.9), a2)
        text(d, (795, 1200), "✓ B lớn hơn A", FL, DGREEN, alpha=a2)
    k3 = appear(t, BAY_C, 0.45)
    if k3 > 0:
        card(d, (40, 1300, 1040, 1560), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1370), "Chưa nói được:", FL, NAVY, alpha=k3)
        text(d, (W / 2, 1475), "số liệu minh hoạ, chưa đo thật", FL, INK, alpha=k3)


# ---------------- canh 6: Chot + THU NGHI (cau chot A-D o khung web) ----------------
END_Q, END_C = 0.2, 3.0
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 415), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 340), "Điện trở: R = U : I", FL, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 450, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(FS)) + 60
    card(d, (W / 2 - pw / 2, 478, W / 2 + pw / 2, 558), fill=A(ORANGE, k1), r=40)
    text(d, (W / 2, 518), "THỬ NGHĨ", FS, WHITE, alpha=k1)
    text(d, (W / 2, 640), f"Dây C: đặt {vn(U_C)} V,", 62, INK, alpha=k1)
    text(d, (W / 2, 725), f"ampe kế chỉ {vn(I_C, 2)} A.", 62, INK, alpha=k1)
    text(d, (W / 2, 810), "Cản như dây A hay B?", 62, INK, alpha=k1)
    coil(d, 540, 1000, "C", a=k1, w=420, h=120, ly=905)
    # hai so do cua day C (khong in R)
    card(d, (120, 1150, 500, 1300), fill=A(BODY, k1), r=22)
    card(d, (145, 1170, 475, 1280), fill=A(SCREEN, k1), r=12)
    text(d, (310, 1225), vn(U_C) + " V", 64, SCR_INK, alpha=k1)
    card(d, (580, 1150, 960, 1300), fill=A(WHITE, k1), outline=A(BLUE, k1), r=22, w=5)
    text(d, (770, 1225), vn(I_C, 2) + " A", 64, BLUE, alpha=k1)
    text(d, (310, 1360), "V", FL, PURPLE, alpha=k1); text(d, (770, 1360), "A", FL, BLUE, alpha=k1)
    text(d, (540, 1225), "?", 72, ORANGE, alpha=k1)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + T_A, "tap"), (do["t0"] + T_B, "tap"),
            (da["t0"] + 0.15, "ding"), (da["t0"] + T_HALF, "tap"), (r["t0"] + r["M"][1] - 0.1, "tap"),
            (b["t0"] + 0.3, "buzz"), (b["t0"] + BAY_R, "tap"), (e["t0"] + END_Q + 0.1, "open")]


CLIP = dict(id="tn-l9-ohm-01", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Điện trở · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai cuộn dây A và B", draw=s_hook, tail=0.3, caps=[
   ("Mạch đo U, I của dây A.", 2.9),
   ("Dừng lại, tự đoán.", 5.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Mắc dây A, đóng khoá K.", 3.4),
   ("Mở K, thay dây B, đóng lại.", 3.9)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Vôn kế giống, ampe kế khác.", 3.4),
   ("Dây B: dòng chỉ một nửa.", 2.9)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.4, caps=[
   ("Dòng nhỏ: dây cản trở nhiều.", 3.4),
   ("Mức cản đó là điện trở.", 4.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.2, caps=[
   ("Nhân U với I thì sao?", 3.0),
   ("Chia U cho I mới đúng.", 3.0),
   ("Còn bỏ ngỏ.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.2, caps=[
   ("Dừng lại, tự tính.", 6.1)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
