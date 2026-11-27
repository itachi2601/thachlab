# Clip: tn-l9-congsuat-01 - Do U, I cua bong den 6 V - 3 W, tinh tich U.I (KHTN 9, 05/11/2026)
# Dung lai 27/11/2026 theo cong moi (viec 4, L9 nhom A): chu than canh >= 56 (ra >= 49 px), o so chi ghi "U"/"I",
#   cot do sang ngan ("bình thường"), cac nac cach 2,6 s, khong nut A-D (K10), thanh dem 90 px, khoi chu cach >= 2,5 s,
#   Bay = hai bieu do cot canh nhau (nghi U.I x4 ✗ / do U.I x9 ✓), bo o "Goi y" o man chot.
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-congsuat-01.json (_kiem_so()):
#   so_lieu_mau (U V, I A, U.I W): 1,5 0,22 0,33 ; 3,0 0,33 0,99 ; 4,5 0,42 1,89 ; 6,0 0,50 3,0. U_dm 6 V, P_dm 3 W.
#   bay = hien_tuong_hay_sai[1] (U x4 thi U.I x4). chua noi duoc = mo_hinh.gia_thiet[1].
# Cau 1 cua bai (lam gi cho U.I dang tin hon) KHONG duoc goi y: khong noi do lap, do chia ampe ke.
# Du doan (K10): dat 3,0 V vao den -> tich U.I khoang? -> khoang 1 W (0,99).
# THU NGHI = cau_chot khung web (v2 theo kiem-v1 + phien chinh): dat 5,0 V, KHONG cho I. Buoc suy luan chua chieu:
#   0,42 A (4,5 V) < I < 0,50 A (6 V) -> 2,1 W < U.I < 2,5 W -> khoang 2,3 W (mo_hinh: I = 0,448 A, U.I = 2,24 W).
#   CHUA co trong kho ghi_chu (tinh tu mo_hinh) -> bao phien chinh. Man chot KHONG in 2,25.
import copy, json, math, os
from engine import *

ROWS = [(1.5, 0.22, 0.33), (3.0, 0.33, 0.99), (4.5, 0.42, 1.89), (6.0, 0.50, 3.0)]
SANG = ("đỏ mờ", "sáng yếu", "khá sáng", "bình thường")
LV = (0.25, 0.5, 0.75, 1.0)
FIL = ((160, 45, 30), (215, 90, 25), (230, 140, 10), (225, 160, 0))
U_DM, P_DM = 6.0, 3.0
U_C, I_C, P_C = 5.0, 0.45, 2.25
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")


def _kiem_so():
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-congsuat-01.json")))
    assert [tuple(h) for h in k["so_lieu_mau"]["hang"]] == ROWS, k["so_lieu_mau"]["hang"]
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert (ts["U_dm"]["gia_tri"], ts["P_dm"]["gia_tri"]) == (U_DM, P_DM)
    for u, i, p in ROWS: assert abs(u * i - p) < 0.006
    assert round(0.5 * (U_C / U_DM) ** 0.6, 2) == I_C and abs(U_C * I_C - P_C) < 1e-9
_kiem_so()

WIRE = (60, 66, 92); BODY = (70, 78, 100); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30)
DGREEN = (21, 110, 55); DRED = (185, 28, 28); GLOW = (255, 214, 80); DPURP = (76, 29, 149)
FS, FL = 56, 60

# ---------------- so do mach ----------------
TY, BY, XL, XR = 390, 690, 150, 990
KX0, KX1, AX, LX, L1, L2, VY = 250, 330, 450, 760, 640, 880, 570


def bulb(d, cx, cy, r, lvl):
    if lvl >= 0:
        b = LV[lvl]
        for i in range(4, 0, -1):
            rr = r + (12 * i * b + 10 * b) * r / 46
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=A(GLOW, 0.10 + 0.07 * b))
    fill = WHITE if lvl < 0 else mix(WHITE, (255, 226, 110), 0.2 + 0.8 * LV[lvl])
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=NAVY, width=6)
    q = r * 0.68; col = NAVY if lvl < 0 else FIL[lvl]
    d.line([(cx - q, cy - q), (cx + q, cy + q)], fill=col, width=6)
    d.line([(cx - q, cy + q), (cx + q, cy - q)], fill=col, width=6)


def circuit(d, closed, lvl, u):
    card(d, (40, 262, 1040, 760), fill=WHITE, outline=LIGHT, w=3)
    w = 6
    d.line([(XL, 445), (XL, TY), (KX0, TY)], fill=WIRE, width=w, joint="curve")
    d.line([(KX1, TY), (AX - 46, TY)], fill=WIRE, width=w)
    d.line([(AX + 46, TY), (LX - 46, TY)], fill=WIRE, width=w)
    d.line([(LX + 46, TY), (XR, TY), (XR, BY), (XL, BY), (XL, 625)], fill=WIRE, width=w, joint="curve")
    d.line([(L1, TY), (L1, VY), (LX - 46, VY)], fill=WIRE, width=5, joint="curve")
    d.line([(LX + 46, VY), (L2, VY), (L2, TY)], fill=WIRE, width=5, joint="curve")
    for p in ((L1, TY), (L2, TY)): dot(d, p[0], p[1], 9, WIRE)
    card(d, (95, 445, 205, 625), fill=BODY, r=16)
    dot(d, 150, 535, 34, WHITE)
    ang = math.radians(-225 + 270 * u / U_DM)
    d.line([(150, 535), (150 + 26 * math.cos(ang), 535 + 26 * math.sin(ang))], fill=ORANGE, width=7)
    text(d, (232, 535), "nguồn", FS, INK, anchor="lm")
    dot(d, KX0, TY, 9, WIRE); dot(d, KX1, TY, 9, WIRE)
    if closed: d.line([(KX0, TY), (KX1, TY)], fill=NAVY, width=7)
    else: d.line([(KX0, TY), (KX0 + 80 * math.cos(math.radians(32)), TY - 80 * math.sin(math.radians(32)))], fill=NAVY, width=7)
    text(d, ((KX0 + KX1) / 2, TY + 58), "K", FS, NAVY)
    d.ellipse([AX - 46, TY - 46, AX + 46, TY + 46], fill=WHITE, outline=BLUE, width=6); text(d, (AX, TY + 2), "A", FS, BLUE)
    d.ellipse([LX - 46, VY - 46, LX + 46, VY + 46], fill=WHITE, outline=PURPLE, width=6); text(d, (LX, VY + 2), "V", FS, PURPLE)
    bulb(d, LX, TY, 46, lvl if closed else -1)
    text(d, (W / 2 + 80, 305), "đèn 6 V – 3 W", FS, INK)


def readouts(d, uv, ia, alpha=1.0):
    for x0, lab, val, col in ((40, "U", uv, PURPLE), (550, "I", ia, BLUE)):
        card(d, (x0, 785, x0 + 490, 945), fill=A(BODY, alpha), r=22)
        text(d, (x0 + 70, 865), lab, 64, WHITE, alpha=alpha)
        card(d, (x0 + 130, 815, x0 + 460, 915), fill=A(SCREEN, alpha), r=12)
        text(d, (x0 + 295, 865), val, 60, SCR_INK, alpha=alpha)


XS = (150, 340, 600, 900)
def table(d, n, y=970, ui=None, hl=None, alpha=1.0, sang=True):
    card(d, (40, y, 1040, y + 560), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    for x, h in zip(XS[:3], ("U (V)", "I (A)", "đèn" if sang else "")): text(d, (x, y + 60), h, FS, INK, alpha=alpha)
    if ui is not None: text(d, (XS[3], y + 60), "U·I (W)", FS, ORANGE, alpha=alpha * ui(-1))
    d.line([(70, y + 110), (1010, y + 110)], fill=A(LIGHT, alpha), width=3)
    for j, (u, i, p) in enumerate(ROWS):
        yy = y + 175 + j * 100
        if hl == j: d.rounded_rectangle([56, yy - 44, 1024, yy + 44], radius=20, fill=A((255, 237, 213), alpha))
        if j < n:
            text(d, (XS[0], yy), vn(u), FL, NAVY, alpha=alpha)
            text(d, (XS[1], yy), vn(i, 2), FL, BLUE, alpha=alpha)
            if sang: text(d, (XS[2], yy), SANG[j], FS, mix(FIL[j], INK, 0.3), alpha=alpha)
            else: bulb(d, XS[2], yy, 30, j)
        else:
            for x in XS[:3]: text(d, (x, yy), "·", FS, GRAY, alpha=alpha)
        if ui is not None:
            k = ui(j)
            if k > 0: text(d, (XS[3], yy), vn(p, 2 if p < 2.99 else 1), FL, ORANGE, alpha=alpha * k)


# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    circuit(d, False, -1, 0.0)
    readouts(d, "? V", "? A")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 975 + (1 - a) * 40
    card(d, (26, y0, 1054, y0 + 610), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(FS)) + 60
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 102), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 62), "DỰ ĐOÁN", FS, WHITE, alpha=a)
    text(d, (W / 2, y0 + 185), "Đặt U = 3,0 V vào đèn.", FL, INK, alpha=a)
    text(d, (W / 2, y0 + 270), "Tích U·I khoảng mấy oát?", FL, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 400, 970, y0 + 490], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 400, 110 + max(90, 860 * (1 - p)), y0 + 490], radius=45, fill=A(DPURP, a))


# ---------------- canh 2: Tien hanh ----------------
T_S = (2.2, 4.6, 7.0, 9.4)
T_ROW = 0.4
def do_state(t):
    k = sum(1 for ts in T_S if t >= ts - 1e-9) - 1
    n = sum(1 for ts in T_S if t >= ts + T_ROW - 1e-9)
    return k >= 0, k, n


def s_do(img, d, t, sc):
    closed, k, n = do_state(t)
    if closed:
        u, i, _ = ROWS[k]; circuit(d, True, k, u); readouts(d, vn(u) + " V", vn(i, 2) + " A")
    else:
        circuit(d, False, -1, 0.0); readouts(d, "0,0 V", "0,00 A")
    table(d, n, hl=(n - 1 if n > 0 else None))


def _kiem_dong_bo():
    clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    if sc["T"] < T_S[-1] + T_ROW + 0.5: bad.append(("canh ngan", sc["T"]))
    while t < sc["T"]:
        closed, k, n = do_state(t)
        if not closed and n != 0: bad.append((round(t, 2), "mo", k, n))
        if closed and n not in (k, k + 1): bad.append((round(t, 2), "dong", k, n))
        t += 0.05
    return bad


# ---------------- canh 3: Ket qua ----------------
def pill(d, s, y, a, color=NAVY, size=FS):
    pw = tw(d, s, F(size)) + 64
    card(d, (W / 2 - pw / 2, y - 42, W / 2 + pw / 2, y + 42), fill=A(color, a), r=40)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN: khoảng 1 W", 310, 1.0)
    ui = lambda j: 1.0 if j < 0 else appear(t, 0.6 + 0.35 * j, 0.35)
    table(d, 4, y=390, ui=ui, hl=1, sang=False)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        y0 = 1000 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 300), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, y0 + 95), "P = U·I", 72, DGREEN, alpha=k2)
        text(d, (W / 2, y0 + 210), "công suất điện (W)", FL, DGREEN, alpha=k2)


# ---------------- canh 4: Rut ra (cot U.I + 4 bong nho) ----------------
GX0, GBASE, GTOP = 150, 840, 420
def gy(p): return GBASE - p / 3.4 * (GBASE - GTOP)
BXS = (290, 480, 670, 860)
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 262, 1040, 1080), fill=WHITE, outline=LIGHT, w=3)
    d.line([(GX0, GTOP - 40), (GX0, GBASE)], fill=NAVY, width=4)
    d.line([(GX0, GBASE), (990, GBASE)], fill=NAVY, width=4)
    text(d, (GX0 + 20, 320), "U·I (W)", FS, ORANGE, anchor="lm")
    for j, (u, i, p) in enumerate(ROWS):
        g = ease((t - 0.3 - 0.3 * j) / 0.6)
        h = (GBASE - gy(p)) * g
        if h > 2: d.rectangle([BXS[j] - 60, GBASE - h, BXS[j] + 60, GBASE], fill=ORANGE)
        if g > 0.95: text(d, (BXS[j], gy(p) - 36), vn(p, 2 if p < 2.99 else 1), FS, ORANGE)
        text(d, (BXS[j], GBASE + 45), vn(u), FS, INK)
        bulb(d, BXS[j], 1000, 32, j if g > 0.95 else -1)
    text(d, (GX0 - 20, GBASE + 45), "U", FS, MUTED, anchor="rm")
    kd = appear(t, M[1] - 0.1, 0.4)
    if kd > 0:
        yd = gy(P_DM)
        for x in range(GX0, 990, 30): d.line([(x, yd), (x + 16, yd)], fill=A(DGREEN, kd), width=4)
    k1 = appear(t, 0.5, 0.45)
    card(d, (40, 1120, 1040, 1270), fill=A((255, 247, 237), k1), outline=A(ORANGE, k1), w=4)
    text(d, (W / 2, 1195), "U·I lớn hơn → đèn sáng hơn", FL, (154, 52, 18), alpha=k1)
    if kd > 0:
        card(d, (40, 1310, 1040, 1530), fill=A((236, 253, 243), kd), outline=A(GREEN, kd), w=5)
        text(d, (W / 2, 1375), "Đúng 6 V: U·I = 3 W", FL, DGREEN, alpha=kd)
        text(d, (W / 2, 1465), "= số ghi trên đèn", FL, DGREEN, alpha=kd)


# ---------------- canh 5: Bay (hai bieu do canh nhau) roi Chua noi duoc ----------------
BAY_R, BAY_C = 3.4, 6.4
def bars(d, x0, vals, col, k, ka):
    base = 1060
    d.line([(x0 + 40, base), (x0 + 430, base)], fill=A(INK, ka), width=4)
    for j, (nm, v) in enumerate(vals):
        cx = x0 + 145 + 190 * j; h = 330 * v / 3.0 * k
        if h > 0: d.rectangle([cx - 55, base - h, cx + 55, base], fill=A(col, ka))
        text(d, (cx, base - 330 * v / 3.0 - 42), vn(v, 2 if v < 2.99 else 1), FL, mix(col, INK, 0.3), alpha=ka * k)
        text(d, (cx, base + 50), nm, FL, INK, alpha=ka)


def s_bay(img, d, t, sc):
    a1 = appear(t, 0.3, 0.45)
    pw = tw(d, "BẪY", F(FS)) + 64
    card(d, (W / 2 - pw / 2, 268, W / 2 + pw / 2, 348), fill=A(DRED, a1), r=40)
    text(d, (W / 2, 308), "BẪY", FS, WHITE, alpha=a1)
    text(d, (W / 2, 410), "“U gấp 4 thì U·I gấp 4”", FL, INK, alpha=a1)
    card(d, (40, 470, 530, 1260), fill=A(WHITE, a1), outline=A(DRED, a1), w=5)
    text(d, (285, 540), "U·I (W) nghĩ", FS, DRED, alpha=a1)
    bars(d, 50, (("1,5", 0.33), ("6", 1.32)), DRED, appear(t, 0.6, 1.0), a1)
    text(d, (285, 1195), "✗ gấp 4", FS, DRED, alpha=a1)
    a2 = appear(t, BAY_R, 0.45)
    if a2 > 0:
        card(d, (550, 470, 1040, 1260), fill=A(WHITE, a2), outline=A(DGREEN, a2), w=5)
        text(d, (795, 540), "U·I (W) đo", FS, DGREEN, alpha=a2)
        text(d, (795, 615), f"I: {vn(ROWS[0][1], 2)} → {vn(ROWS[3][1], 2)}", FS, BLUE, alpha=a2)
        bars(d, 560, (("1,5", ROWS[0][2]), ("6", ROWS[3][2])), DGREEN, appear(t, BAY_R, 0.9), a2)
        text(d, (795, 1195), "✓ gấp khoảng 9", FS, DGREEN, alpha=a2)
    k3 = appear(t, BAY_C, 0.45)
    if k3 > 0:
        card(d, (40, 1300, 1040, 1560), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1370), "Chưa nói được:", FL, NAVY, alpha=k3)
        text(d, (W / 2, 1475), "bỏ qua điện trở ampe kế", FL, INK, alpha=k3)


# ---------------- canh 6: Chot + THU NGHI ----------------
END_Q, END_C = 0.2, 3.0
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 415), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 340), "P = U·I là công suất điện", FS, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 450, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(FS)) + 60
    card(d, (W / 2 - pw / 2, 478, W / 2 + pw / 2, 558), fill=A(ORANGE, k1), r=40)
    text(d, (W / 2, 518), "THỬ NGHĨ", FS, WHITE, alpha=k1)
    text(d, (W / 2, 650), "Đặt 5,0 V vào đèn.", FL, INK, alpha=k1)
    text(d, (W / 2, 735), "Tích U·I khoảng bao nhiêu?", FL, INK, alpha=k1)
    if k1 > 0.5: bulb(d, W / 2, 920, 70, 2)
    for x0, lab, val, col in ((40, "U", "5,0 V", PURPLE), (550, "I", "? A", BLUE)):
        card(d, (x0 + 30, 1070, x0 + 460, 1210), fill=A(BODY, k1), r=22)
        text(d, (x0 + 95, 1140), lab, 64, WHITE, alpha=k1)
        card(d, (x0 + 150, 1095, x0 + 440, 1185), fill=A(SCREEN, k1), r=12)
        text(d, (x0 + 295, 1140), val, FL, SCR_INK, alpha=k1)
    card(d, (290, 1300, 790, 1430), fill=A(SCREEN, k1), r=20)
    text(d, (540, 1365), "U·I = ? W", 64, ORANGE, alpha=k1)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"), (do["t0"] + T_S[0], "tap")]
    out += [(do["t0"] + ts, "tick") for ts in T_S[1:]]
    out += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + 0.3, "buzz"),
            (b["t0"] + BAY_R, "tap"), (e["t0"] + END_Q + 0.1, "open")]
    return out


CLIP = dict(id="tn-l9-congsuat-01", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Công suất điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bóng đèn ghi 6 V – 3 W", draw=s_hook, tail=0.3, caps=[
   ("Mạch đo U và I của đèn.", 2.9),
   ("Dừng lại, tự đoán.", 5.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Đóng K, tăng U từng nấc.", 3.4),
   ("Mỗi nấc: đọc I, xem đèn.", 3.4),
   ("Tăng tiếp lên 6 V.", 3.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Nhân U với I mỗi lần.", 3.0),
   ("Tích U·I là công suất.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("So độ sáng với cột.", 3.0),
   ("Đó là công suất định mức.", 3.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.2, caps=[
   ("U gấp 4 lần.", 3.0),
   ("I cũng tăng theo.", 3.0),
   ("Còn bỏ ngỏ.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.2, caps=[
   ("Dừng lại, tự tính.", 6.1)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
