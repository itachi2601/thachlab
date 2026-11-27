# Clip: tn-l9-ohm-02 - Doi U, doc I cua mot doan day constantan, ve do thi I theo U (KHTN 9, lo 6, 18/11/2026)
# Dung lai 27/11/2026 theo cong moi (viec 4, L9 nhom A): chu than canh >= 56 (ra >= 49 px), dong ho chi ghi V / A,
#   khong nut A-D (K10), thanh dem day 90 px, moi nhip >= 3 s co phu de, khoi chu cach >= 2,5 s,
#   Bay = hai do thi canh nhau (noi tung diem, khong qua goc / ke thang tu goc), bo o "Goi y" o man chot.
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-ohm-02.json (_kiem_so()):
#   so_lieu_mau (U V, I A, U/I Ohm): 1,5 0,08 18,75 ; 3,0 0,15 20,0 ; 4,5 0,22 20,45 ; 6,0 0,30 20,0. R = 20 Ohm (tham_so).
#   rut_ra: I ti le thuan U ; U/I quanh 20 Ohm ; do thi thang qua goc. bay = hien_tuong_hay_sai[1] (noi gap khuc).
#   KHONG nhan xet vi sao lan 1 lech (Cau 2 ngay sau hop hoi dung dieu nay) ; KHONG dung bay "tang U thi R tang" (Cau 4).
#   chua noi duoc = mo_hinh.gia_thiet[0] (moi thu day constantan, R gan nhu khong doi khi nong).
# Du doan (K10): cham 4 diem (U; I) -> duong qua cac diem co dang nao? -> thang qua goc (khac ohm-01: cung U, doi day).
# THU NGHI = cau_chot khung web (ghi o kho ghi_chu): day khac 2,0 V -> 0,05 A ; muon 0,12 A thi U? -> 4,8 V
#   (hai buoc: R = 40 Ohm roi U = I.R). Man chot KHONG in 40 Ohm, KHONG in 4,8 V.
import copy
from engine import *

ROWS = [(1.5, 0.08, 18.75), (3.0, 0.15, 20.0), (4.5, 0.22, 20.45), (6.0, 0.30, 20.0)]   # so_lieu_mau
R = 20.0
U_C0, I_C0, I_C, U_C = 2.0, 0.05, 0.12, 4.8   # cau chot: day khac 2,0 V -> 0,05 A (R = 40 Ohm); 0,12 A -> U = 4,8 V
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
def vq(x): return vn(x, 2) if abs(x * 10 - round(x * 10)) > 1e-6 else vn(x, 1)        # 18,75 ; 20,0 ; 20,45


def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-ohm-02.json")))
    assert [tuple(h) for h in k["so_lieu_mau"]["hang"]] == ROWS, k["so_lieu_mau"]["hang"]
    for u, i, q in ROWS: assert abs(u / i - q) < 0.01
    assert k["tham_so"][1]["gia_tri"] == R
    g = k["so_lieu_mau"]["ghi_chu"]
    assert "2,0 V" in g and "0,05 A" in g and "0,12 A" in g and "4,8 V" in g
    assert abs(U_C0 / I_C0 * I_C - U_C) < 1e-9 and U_C <= k["tham_so"][0]["max"]
_kiem_so()

WIRE = (60, 66, 92); BODY = (70, 78, 100); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30)
DGREEN = (21, 110, 55); DRED = (185, 28, 28); CON = (180, 83, 9); DPURP = (76, 29, 149); GRID = (232, 228, 218)
FS, FL = 56, 60

# ---------------- dai mach thu gon ----------------
XL, XR, TY, BY = 80, 680, 380, 560
AX, C0, C1, VX, VY = 190, 300, 580, 440, 475
SX, KX0, KX1 = 330, 460, 550
AR = 44


def coil(d, x0, x1, y, a=1.0):
    pts = [(x0, y)]; n = 9
    for k in range(n):
        pts.append((x0 + (k + 0.5) * (x1 - x0) / n, y + (-24 if k % 2 == 0 else 24)))
    pts.append((x1, y))
    d.line(pts, fill=A(CON, a), width=6, joint="curve")


def strip(d, closed, u_src, u_v, i_a):
    card(d, (40, 262, 1040, 620), fill=WHITE, outline=LIGHT, w=3)
    w = 6
    d.line([(XL, BY), (XL, TY), (AX - AR, TY)], fill=WIRE, width=w, joint="curve")
    d.line([(AX + AR, TY), (C0, TY)], fill=WIRE, width=w)
    d.line([(C1, TY), (XR, TY), (XR, BY), (KX1, BY)], fill=WIRE, width=w, joint="curve")
    d.line([(KX0, BY), (SX + 20, BY)], fill=WIRE, width=w)
    d.line([(SX - 20, BY), (XL, BY)], fill=WIRE, width=w)
    coil(d, C0, C1, TY)
    text(d, ((C0 + C1) / 2, 312), "dây constantan", FS, mix(CON, INK, 0.3))
    d.ellipse([AX - AR, TY - AR, AX + AR, TY + AR], fill=WHITE, outline=BLUE, width=6); text(d, (AX, TY + 2), "A", FS, BLUE)
    for x in (C0, C1): dot(d, x, TY, 8, WIRE)
    d.line([(C0, TY), (C0, VY), (VX - AR, VY)], fill=PURPLE, width=5, joint="curve")
    d.line([(C1, TY), (C1, VY), (VX + AR, VY)], fill=PURPLE, width=5, joint="curve")
    d.ellipse([VX - AR, VY - AR, VX + AR, VY + AR], fill=WHITE, outline=PURPLE, width=6); text(d, (VX, VY + 2), "V", FS, PURPLE)
    # nguon chinh duoc: ban dai (+) ben trai, mui ten cheo = chinh duoc
    d.line([(SX - 20, BY - 44), (SX - 20, BY + 44)], fill=NAVY, width=6)
    d.line([(SX + 20, BY - 22), (SX + 20, BY + 22)], fill=NAVY, width=14)
    arrow(d, (SX - 48, BY + 38), (SX + 48, BY - 38), ORANGE, w=4, head=16)
    text(d, (SX - 70, BY - 30), "+", FS, ORANGE)
    # khoa K
    dot(d, KX0, BY, 9, WIRE); dot(d, KX1, BY, 9, WIRE)
    if closed: d.line([(KX0, BY), (KX1, BY)], fill=NAVY, width=7)
    else: d.line([(KX0, BY), (KX1 - 12, BY - 44)], fill=NAVY, width=7)
    text(d, (KX1 + 50, BY - 30), "K", FS, NAVY)
    if closed:
        arrow(d, (XL, 520), (XL, 430), RED, w=7, head=20)
    # dong ho so
    for y, lab, val, col in ((276, "V", vn(u_v) + " V", PURPLE), (452, "A", vn(i_a, 2) + " A", BLUE)):
        card(d, (712, y, 1026, y + 158), fill=BODY, r=20)
        text(d, (752, y + 42), lab, FS, WHITE)
        card(d, (790, y + 14, 1010, y + 144), fill=SCREEN, r=12)
        text(d, (900, y + 79), val, 58, SCR_INK)


# ---------------- do thi I theo U ----------------
OX, OY, SU, SI = 215, 1240, 122.0, 1700.0
def P(u, i, ox=OX, oy=OY, su=SU, si=SI): return (ox + u * su, oy - i * si)


def axes(d, a=1.0, y0=650, y1=1318):
    card(d, (40, y0, 1040, y1), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    for i in (0.1, 0.2, 0.3):
        y = OY - i * SI
        d.line([(OX, y), (OX + 6.3 * SU, y)], fill=A(GRID, a), width=2)
        text(d, (OX - 70, y), vn(i), FS, INK, alpha=a)
    for u in (1.5, 3.0, 4.5, 6.0):
        x = OX + u * SU
        d.line([(x, OY - 0.31 * SI), (x, OY)], fill=A(GRID, a), width=2)
        text(d, (x, OY + 48), vn(u), FS, INK, alpha=a)
    arrow(d, (OX, OY), (OX + 6.6 * SU, OY), A(NAVY, a), w=5, head=18)
    arrow(d, (OX, OY), (OX, OY - 0.33 * SI), A(NAVY, a), w=5, head=18)
    text(d, (OX - 60, OY + 48), "0", FS, INK, alpha=a)
    text(d, (OX + 110, OY - 0.33 * SI + 24), "I (A)", FS, NAVY, alpha=a)
    text(d, (955, OY - 56), "U (V)", FS, NAVY, alpha=a)


def pt(d, u, i, col=BLUE, a=1.0, r=15, **kw):
    x, y = P(u, i, **kw); d.ellipse([x - r, y - r, x + r, y + r], fill=A(col, a), outline=A(WHITE, a), width=3)


# ---------------- bang nam ngang ----------------
TXS = (450, 600, 750, 900)
def table(d, n, y=1334, ui=0.0, hl=None):
    hh = 200 + (95 if ui > 0 else 0)
    card(d, (40, y, 1040, y + hh), fill=WHITE, outline=LIGHT, w=3)
    labs = (("U (V)", NAVY), ("I (A)", BLUE)) + ((("U/I (Ω)", DGREEN),) if ui > 0 else ())
    for r, (lab, col) in enumerate(labs):
        yy = y + 55 + r * 92
        text(d, (75, yy), lab, FS, col, anchor="lm")
        if r < len(labs) - 1: d.line([(70, yy + 46), (1010, yy + 46)], fill=LIGHT, width=3)
    for k, (u, i, q) in enumerate(ROWS):
        x = TXS[k]
        if hl == k: d.rounded_rectangle([x - 72, y + 12, x + 72, y + 190], radius=18, fill=(255, 237, 213))
        if k < n:
            text(d, (x, y + 55), vn(u), FL, NAVY); text(d, (x, y + 147), vn(i, 2), FL, BLUE)
        else:
            text(d, (x, y + 55), "…", FS, MUTED); text(d, (x, y + 147), "…", FS, MUTED)
        if ui > 0: text(d, (x, y + 239), vq(q), 58 if len(vq(q)) < 5 else 56, DGREEN, alpha=appear(ui, 0.2 + 0.15 * k, 0.3))


# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    strip(d, False, None, 0.0, 0.0)
    axes(d); table(d, 0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 636 + (1 - a) * 40
    card(d, (26, y0, 1054, y0 + 950), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(FS)) + 60
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 104), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 64), "DỰ ĐOÁN", FS, WHITE, alpha=a)
    ax, ay = 400, y0 + 400   # do thi phac, chua co gi
    arrow(d, (ax, ay), (ax + 300, ay), A(NAVY, a), w=5, head=18); arrow(d, (ax, ay), (ax, ay - 230), A(NAVY, a), w=5, head=18)
    text(d, (ax + 340, ay - 30), "U", FL, NAVY, alpha=a); text(d, (ax - 45, ay - 215), "I", FL, NAVY, alpha=a)
    text(d, (ax + 150, ay - 110), "?", 80, DPURP, alpha=a)
    text(d, (W / 2, y0 + 520), "Chấm 4 điểm (U; I) lên đồ thị.", FL, INK, alpha=a)
    text(d, (W / 2, y0 + 605), "Đường qua các điểm dạng nào?", FL, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 720, 970, y0 + 810], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 720, 110 + max(90, 860 * (1 - p)), y0 + 810], radius=45, fill=A(DPURP, a))


# ---------------- canh 2: Tien hanh ----------------
T0, STEP, D_CLOSE, D_OPEN, T_PT = 0.5, 2.3, 0.5, 1.9, 0.35
def do_state(t):
    """-> (K dong?, U nguon dang dat, so diem da ghi, chi so lan dang do)."""
    k = int(clamp((t - T0) / STEP, 0, 3.999)) if t >= T0 else -1
    if k < 0: return False, 0.0, 0, -1
    ts = T0 + k * STEP
    closed = ts + D_CLOSE <= t < ts + D_OPEN
    n = sum(1 for j in range(4) if t >= T0 + j * STEP + D_CLOSE + T_PT)
    return closed, ROWS[k][0], n, k


def s_do(img, d, t, sc):
    closed, us, n, k = do_state(t)
    u, i = (ROWS[k][0], ROWS[k][1]) if closed else (0.0, 0.0)
    strip(d, closed, us, u, i)
    axes(d)
    for j in range(n): pt(d, ROWS[j][0], ROWS[j][1], a=appear(t, T0 + j * STEP + D_CLOSE + T_PT, 0.25))
    table(d, n, hl=k if k >= 0 else None)


def _kiem_dong_bo():
    clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        closed, us, n, k = do_state(t)
        if closed and n > k + 1: bad.append((round(t, 2), "cham truoc khi doc"))
        if not closed and k >= 0 and n not in (k, k + 1): bad.append((round(t, 2), "so cham lech lan do"))
        if closed and us != ROWS[k][0]: bad.append((round(t, 2), "U nguon lech hang"))
        t += 0.05
    if do_state(sc["T"] - 0.01)[2] != 4: bad.append("cuoi canh thieu diem")
    if T0 + 3 * STEP + D_OPEN > sc["T"]: bad.append("lan 4 chua mo K")
    return bad


# ---------------- canh 3: Dap an (duong thang qua goc) ----------------
def pill(d, s, y, a, color=NAVY, size=FS):
    pw = tw(d, s, F(size)) + 64
    card(d, (W / 2 - pw / 2, y - 42, W / 2 + pw / 2, y + 42), fill=A(color, a), r=40)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    pill(d, "ĐÁP ÁN: thẳng, qua gốc", 330, ka)
    axes(d, y0=430)
    g = ease((t - 0.6) / 1.2)
    if g > 0:   # ke thuoc: duong I = U/R tu goc, ve dan
        u1 = 6.3 * g; d.line([P(0, 0), P(u1, u1 / R)], fill=DGREEN, width=7)
    for u, i, q in ROWS: pt(d, u, i)
    gd = ease((t - M[1] + 0.1) / 1.6)   # nhip 2: cham truot doc duong ve goc (U giam ve 0 thi I ve 0)
    if 0 < gd < 1:
        uu = 6.3 * (1 - gd); x, y = P(uu, uu / R)
        d.line([(x, y), (x, OY)], fill=ORANGE, width=4); d.line([(OX, y), (x, y)], fill=ORANGE, width=4)
        dot(d, x, y, 28, ORANGE)
    k0 = appear(t, M[1] + 1.5, 0.4)
    if k0 > 0:
        r = 26 + 8 * (1 - k0)
        d.ellipse([OX - r, OY - r, OX + r, OY + r], outline=A(ORANGE, k0), width=7)
        text(d, (OX - 85, OY - 75), "gốc", FL, ORANGE, alpha=k0)


# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    card(d, (40, 268, 1040, 420), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=5)
    text(d, (W / 2, 344), "I tỉ lệ thuận với U", 64, DGREEN, alpha=k0)
    table(d, 4, y=470, ui=clamp((t - 1.0) / 1.6))
    k2 = appear(t, M[1] - 0.1, 0.4)
    if k2 > 0:
        card(d, (40, 830, 1040, 1160), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 925), "Định luật Ohm", FL, DGREEN, alpha=k2)
        text(d, (430, 1060), "I =", 76, DGREEN, alpha=k2)
        text(d, (560, 1015), "U", 66, DGREEN, alpha=k2)
        d.line([(515, 1062), (605, 1062)], fill=A(DGREEN, k2), width=6)
        text(d, (560, 1110), "R", 66, DGREEN, alpha=k2)


# ---------------- canh 5: Bay (hai do thi canh nhau) roi Chua noi duoc ----------------
BAY_R, BAY_C = 3.4, 6.4
MS = dict(su=58.0, si=1000.0)
def mini(d, x0, a, col):
    ox, oy = x0 + 70, 1000
    arrow(d, (ox, oy), (ox + 400, oy), A(NAVY, a), w=4, head=16)
    arrow(d, (ox, oy), (ox, oy - 380), A(NAVY, a), w=4, head=16)
    text(d, (ox - 35, oy + 40), "0", FS, INK, alpha=a)
    text(d, (ox + 372, oy + 44), "U", FS, NAVY, alpha=a); text(d, (ox - 38, oy - 350), "I", FS, NAVY, alpha=a)
    d.ellipse([ox - 22, oy - 22, ox + 22, oy + 22], outline=A(ORANGE, a), width=5)
    return ox, oy


def s_bay(img, d, t, sc):
    a1 = appear(t, 0.3, 0.45)
    pw = tw(d, "BẪY", F(FS)) + 64
    card(d, (W / 2 - pw / 2, 268, W / 2 + pw / 2, 348), fill=A(DRED, a1), r=40)
    text(d, (W / 2, 308), "BẪY", FS, WHITE, alpha=a1)
    card(d, (40, 390, 530, 1260), fill=A(WHITE, a1), outline=A(DRED, a1), w=5)
    ox, oy = mini(d, 40, a1, DRED)
    g = clamp((t - 0.7) / 1.2)
    pts = [P(u, i, ox, oy, **MS) for u, i, q in ROWS]
    seg = g * (len(pts) - 1)
    for j in range(len(pts) - 1):
        f = clamp(seg - j)
        if f > 0: d.line([pts[j], (lerp(pts[j][0], pts[j + 1][0], f), lerp(pts[j][1], pts[j + 1][1], f))], fill=A(DRED, a1), width=6)
    for u, i, q in ROWS: pt(d, u, i, a=a1, r=13, ox=ox, oy=oy, **MS)
    text(d, (285, 1110), "✗ nối từng điểm,", FS, DRED, alpha=a1)
    text(d, (285, 1190), "hở ở gốc", FS, DRED, alpha=a1)
    a2 = appear(t, BAY_R, 0.45)
    if a2 > 0:
        card(d, (550, 390, 1040, 1260), fill=A(WHITE, a2), outline=A(DGREEN, a2), w=5)
        ox, oy = mini(d, 550, a2, DGREEN)
        g2 = ease((t - BAY_R - 0.2) / 1.0)
        if g2 > 0: d.line([(ox, oy), P(6.4 * g2, 6.4 * g2 / R, ox, oy, **MS)], fill=A(DGREEN, a2), width=6)
        for u, i, q in ROWS: pt(d, u, i, a=a2, r=13, ox=ox, oy=oy, **MS)
        text(d, (795, 1110), "✓ kẻ thẳng", FS, DGREEN, alpha=a2)
        text(d, (795, 1190), "từ gốc", FS, DGREEN, alpha=a2)
    k3 = appear(t, BAY_C, 0.45)
    if k3 > 0:
        card(d, (40, 1300, 1040, 1560), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1370), "Chưa nói được:", FL, NAVY, alpha=k3)
        text(d, (W / 2, 1475), "mới thử một dây constantan", FL, INK, alpha=k3)


# ---------------- canh 6: Chot + THU NGHI (cau chot A-D o khung web) ----------------
END_Q, END_C = 0.2, 3.0
def chip(d, x0, y0, val, lab, col, a):
    card(d, (x0, y0, x0 + 330, y0 + 140), fill=A(BODY, a), r=20)
    text(d, (x0 + 42, y0 + 70), lab, FS, WHITE, alpha=a)
    card(d, (x0 + 80, y0 + 14, x0 + 316, y0 + 126), fill=A(SCREEN, a), r=12)
    text(d, (x0 + 198, y0 + 70), val, 60, col, alpha=a)


def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 415), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 340), "Cùng dây: I tỉ lệ thuận với U", FS, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 450, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(FS)) + 60
    card(d, (W / 2 - pw / 2, 478, W / 2 + pw / 2, 558), fill=A(ORANGE, k1), r=40)
    text(d, (W / 2, 518), "THỬ NGHĨ", FS, WHITE, alpha=k1)
    text(d, (W / 2, 650), "Một dây khác.", 62, INK, alpha=k1)
    text(d, (W / 2, 735), f"Muốn {vn(I_C, 2)} A, đặt U bao nhiêu?", 62, INK, alpha=k1)
    coil(d, 300, 780, 870, a=k1)
    for j, (u, i) in enumerate(((vn(U_C0) + " V", vn(I_C0, 2) + " A"), ("? V", vn(I_C, 2) + " A"))):
        y = 1000 + j * 220
        chip(d, 90, y, u, "V", SCR_INK if u[0] != "?" else ORANGE, k1)
        arrow(d, (450, y + 70), (600, y + 70), A(NAVY, k1), w=6, head=20)
        chip(d, 660, y, i, "A", SCR_INK, k1)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    cs += [(do["t0"] + T0 + j * STEP + D_CLOSE, "tap") for j in range(4)]
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + 0.3, "buzz"),
           (b["t0"] + BAY_R, "tap"), (e["t0"] + END_Q + 0.1, "open")]
    return cs


CLIP = dict(id="tn-l9-ohm-02", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Định luật Ohm · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đổi U, đọc I", draw=s_hook, tail=0.3, caps=[
   ("Một đoạn dây constantan.", 2.9),
   ("Dừng lại, tự đoán.", 5.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Mỗi lần: đặt U, đóng K, đọc I.", 3.3),
   ("Ngắt K giữa các lần đo.", 2.9),
   ("Chấm từng điểm lên đồ thị.", 3.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Kẻ thẳng sát các điểm.", 2.9),
   ("U bằng 0 thì I bằng 0.", 2.9)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Tính U chia I mỗi lần.", 3.0),
   ("Đó là định luật Ohm.", 3.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.2, caps=[
   ("Nối gấp khúc có đúng?", 3.0),
   ("Thẳng, qua gốc.", 3.0),
   ("Còn bỏ ngỏ.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.2, caps=[
   ("Dừng lại, tự tính.", 6.4)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
