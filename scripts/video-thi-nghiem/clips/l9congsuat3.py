# Clip: tn-l9-congsuat-03 - Hai bong X 6 V - 3 W va Y 6 V - 6 W, noi tiep roi song song vao nguon 6 V (KHTN 9, 05/11/2026)
# Dung lai 27/11/2026 theo cong moi (viec 4, L9 nhom A): chu than canh >= 56, nhan den "X · 3 W" (khong them chu),
#   o so chi chi so, bang do sang 2x2 bang hinh bong (khong chu "sang hon"), khong nut A-D (K10), thanh dem 90 px,
#   khoi chu cach >= 2,5 s, Bay = hai the canh nhau (nghi Y sang hon ✗ / tinh P: X sang hon ✓), bo o "Goi y".
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-congsuat-03.json (_kiem_so()):
#   so_lieu_mau (cach mac, den, U V, I A, P W): noi tiep X 4,0 0,33 1,33 ; Y 2,0 0,33 0,67 ;
#                                              song song X 6,0 0,5 3,0 ; Y 6,0 1,0 6,0. R_X 12, R_Y 6 Ohm (coi khong doi).
#   bay = hien_tuong_hay_sai[0] ("nhieu oat luon sang hon"); chua noi duoc = mo_hinh.gia_thiet[0].
# Tra bai Cau 6 cua bai = hai den noi tiep, den nao sang hon (40 W / 100 W) -> THU NGHI KHONG hoi lai kieu do;
#   chot moi: X, Y song song vao 3 V, P cua Y? (R const: 3^2/6 = 1,5 W). CHUA co trong kho ghi_chu (kho khong co chot)
#   -> bao phien chinh. Man chot KHONG in 1,5.
# Du doan (K10): noi tiep roi song song vao 6 V, moi lan den nao sang hon? -> noi tiep X, song song Y.
import copy, json, math, os
from engine import *

ROWS = [("nối tiếp", "X", 4.0, 0.33, 1.33), ("nối tiếp", "Y", 2.0, 0.33, 0.67),
        ("song song", "X", 6.0, 0.50, 3.0), ("song song", "Y", 6.0, 1.00, 6.0)]
R_X, R_Y, U0 = 12.0, 6.0, 6.0
U_C = 3.0; P_C = U_C ** 2 / R_Y
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
def vp(p): return vn(p, 1) if abs(p - round(p)) < 1e-9 else vn(p, 2)


def _kiem_so():
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-congsuat-03.json")))
    assert [tuple(h) for h in k["so_lieu_mau"]["hang"]] == ROWS, k["so_lieu_mau"]["hang"]
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert (ts["R_X"]["gia_tri"], ts["R_Y"]["gia_tri"]) == (R_X, R_Y)
    assert R_X == 6 ** 2 / 3 and R_Y == 6 ** 2 / 6
    for _, _, u, i, p in ROWS: assert abs(u * i - p) < 0.02
    assert abs(ROWS[0][2] + ROWS[1][2] - U0) < 1e-9 and ROWS[0][3] == ROWS[1][3]
    assert abs(P_C - 1.5) < 1e-9
_kiem_so()

WIRE = (60, 66, 92); BODY = (70, 78, 100); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30)
DGREEN = (21, 110, 55); DRED = (185, 28, 28); GLOW = (255, 214, 80); DPURP = (76, 29, 149)
FS, FL = 56, 60
LOOK = {("nt", "X"): (0.45, (215, 90, 25)), ("nt", "Y"): (0.12, (160, 45, 30)),
        ("ss", "X"): (0.72, (230, 140, 10)), ("ss", "Y"): (1.0, (225, 160, 0))}
PDM = {"X": 3, "Y": 6}


def bulb(d, cx, cy, r, look=None, alpha=1.0):
    if look is not None:
        b, fil = look
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


# ---------------- so do mach (the 262-760) ----------------
XL, XR, TY, BY = 150, 990, 400, 700
KX0, KX1 = 240, 320


def source_k(d, closed, lab="6 V"):
    card(d, (40, 262, 1040, 760), fill=WHITE, outline=LIGHT, w=3)
    card(d, (80, 470, 220, 630), fill=BODY, r=16)
    text(d, (150, 550), lab, FS, WHITE)
    d.line([(XL, 470), (XL, TY), (KX0, TY)], fill=WIRE, width=6, joint="curve")
    d.line([(XL, 630), (XL, BY)], fill=WIRE, width=6)
    dot(d, KX0, TY, 9, WIRE); dot(d, KX1, TY, 9, WIRE)
    if closed: d.line([(KX0, TY), (KX1, TY)], fill=NAVY, width=7)
    else: d.line([(KX0, TY), (KX0 + 80 * math.cos(math.radians(32)), TY - 80 * math.sin(math.radians(32)))], fill=NAVY, width=7)
    text(d, ((KX0 + KX1) / 2, TY - 60), "K", FS, NAVY)


def meter(d, cx, cy, ch, col, r=42):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=col, width=6)
    text(d, (cx, cy + 2), ch, FS, col)


def lamp_lab(d, cx, cy, nm, look):
    text(d, (cx, cy), f"{nm} · {PDM[nm]} W", FS, INK)


AN, NX, NY = 420, 620, 840
def circuit_nt(d, closed, mode_alpha=1.0):
    source_k(d, closed)
    w = 6
    d.line([(KX1, TY), (AN - 42, TY)], fill=WIRE, width=w)
    d.line([(AN + 42, TY), (NX - 46, TY)], fill=WIRE, width=w)
    d.line([(NX + 46, TY), (NY - 46, TY)], fill=WIRE, width=w)
    d.line([(NY + 46, TY), (XR, TY), (XR, BY), (XL, BY)], fill=WIRE, width=w, joint="curve")
    meter(d, AN, TY, "A", BLUE)
    for cx, nm in ((NX, "X"), (NY, "Y")):
        bulb(d, cx, TY, 46, LOOK[("nt", nm)] if closed else None)
        lamp_lab(d, cx, TY + 110, nm, None)


NL, NR, YB = 480, 960, 590
BX = 720
def circuit_ss(d, closed):
    source_k(d, closed)
    w = 6
    d.line([(KX1, TY), (AN - 42, TY)], fill=WIRE, width=w)
    d.line([(AN + 42, TY), (BX - 46, TY)], fill=WIRE, width=w)
    d.line([(BX + 46, TY), (NR, TY), (NR, YB)], fill=WIRE, width=w, joint="curve")
    d.line([(NL, TY), (NL, YB), (BX - 46, YB)], fill=WIRE, width=w, joint="curve")
    d.line([(BX + 46, YB), (NR, YB)], fill=WIRE, width=w)
    d.line([(NR, YB), (NR, BY), (XL, BY)], fill=WIRE, width=w, joint="curve")
    dot(d, NL, TY, 10, WIRE); dot(d, NR, YB, 10, WIRE)
    meter(d, AN, TY, "A", BLUE)
    for y, nm in ((TY, "X"), (YB, "Y")):
        bulb(d, BX, y, 46, LOOK[("ss", nm)] if closed else None)
        text(d, (BX + 150, y + (-58 if nm == "X" else 58)), f"{nm} · {PDM[nm]} W", FS, INK, anchor="lm" if False else "mm")


def readouts(d, vals):
    """vals: 3 cap (nhan, gia tri) - nhan chi 1 chu cai/ky hieu."""
    for k, (lab, val, col) in enumerate(vals):
        x0 = 40 + k * 340
        card(d, (x0, 785, x0 + 320, 935), fill=BODY, r=22)
        text(d, (x0 + 58, 860), lab, FS, WHITE)
        card(d, (x0 + 110, 812, x0 + 300, 908), fill=SCREEN, r=12)
        text(d, (x0 + 205, 860), val, FS, SCR_INK)


# bang do sang 2x2: hang noi tiep / song song, cot X / Y, o = hinh bong
GY0 = 965
def bright_table(d, n_on, hl=None, alpha=1.0, y0=GY0):
    card(d, (40, y0, 1040, y0 + 600), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    for x, nm in ((640, "X"), (880, "Y")): text(d, (x, y0 + 65), nm, FL, INK, alpha=alpha)
    d.line([(70, y0 + 115), (1010, y0 + 115)], fill=A(LIGHT, alpha), width=3)
    for j, (lab, key) in enumerate((("nối tiếp", "nt"), ("song song", "ss"))):
        yy = y0 + 240 + j * 220
        if hl == j: d.rounded_rectangle([56, yy - 95, 1024, yy + 95], radius=24, fill=A((255, 237, 213), alpha))
        text(d, (250, yy), lab, FL, INK, alpha=alpha)
        for x, nm in ((640, "X"), (880, "Y")):
            bulb(d, x, yy, 56, LOOK[(key, nm)] if j < n_on else None, alpha=alpha)


# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    circuit_nt(d, False)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 800 + (1 - a) * 40
    card(d, (26, y0, 1054, y0 + 680), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(FS)) + 60
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 102), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 62), "DỰ ĐOÁN", FS, WHITE, alpha=a)
    text(d, (W / 2, y0 + 185), "Nối tiếp, rồi song song", FL, INK, alpha=a)
    text(d, (W / 2, y0 + 270), "vào 6 V. Mỗi lần,", FL, INK, alpha=a)
    text(d, (W / 2, y0 + 355), "đèn nào sáng hơn?", FL, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 480, 970, y0 + 570], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 480, 110 + max(90, 860 * (1 - p)), y0 + 570], radius=45, fill=A(DPURP, a))


# ---------------- canh 2: Tien hanh ----------------
T_K1, T_SW, T_K2 = 1.0, 4.4, 6.0
def do_state(t):
    if t < T_SW: return "nt", t >= T_K1
    return "ss", t >= T_K2


def do_read(mode, closed):
    x, y = (ROWS[0], ROWS[1]) if mode == "nt" else (ROWS[2], ROWS[3])
    if mode == "nt":
        if not closed: return [("I", "0,00 A", BLUE), ("X", "0,0 V", PURPLE), ("Y", "0,0 V", PURPLE)]
        return [("I", vn(x[3], 2) + " A", BLUE), ("X", vn(x[2]) + " V", PURPLE), ("Y", vn(y[2]) + " V", PURPLE)]
    if not closed: return [("U", "0,0 V", PURPLE), ("X", "0,00 A", BLUE), ("Y", "0,00 A", BLUE)]
    return [("U", vn(x[2]) + " V", PURPLE), ("X", vn(x[3], 2) + " A", BLUE), ("Y", vn(y[3], 2) + " A", BLUE)]


def s_do(img, d, t, sc):
    mode, closed = do_state(t)
    if mode == "nt": circuit_nt(d, closed)
    else: circuit_ss(d, closed)
    if closed:   # cham dong dien chay tren day duoi (tu phai sang trai)
        for i in range(8):
            x = XR - ((t * 220 + i * 105) % (XR - XL))
            dot(d, x, BY, 18, A(BLUE, 0.8))
    readouts(d, do_read(mode, closed))
    n_on = (1 if t >= T_K1 else 0) + (1 if t >= T_K2 else 0)
    bright_table(d, n_on, hl=(0 if mode == "nt" else 1))


def _kiem_dong_bo():
    clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    if sc["T"] < T_K2 + 2.5: bad.append(("canh ngan", sc["T"]))
    while t < sc["T"]:
        mode, closed = do_state(t); r = do_read(mode, closed)
        zero = all(v.startswith("0,0") for _, v, _ in r)
        if closed == zero: bad.append((round(t, 2), mode, closed))
        if closed and mode == "nt" and (r[1][1], r[2][1]) != ("4,0 V", "2,0 V"): bad.append((round(t, 2), "U nt"))
        if closed and mode == "ss" and (r[1][1], r[2][1]) != ("0,50 A", "1,00 A"): bad.append((round(t, 2), "I ss"))
        t += 0.05
    return bad


# ---------------- canh 3: Ket qua ----------------
def pill(d, s, y, a, color=NAVY, size=FS):
    pw = tw(d, s, F(size)) + 64
    card(d, (W / 2 - pw / 2, y - 42, W / 2 + pw / 2, y + 42), fill=A(color, a), r=40)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN: X, rồi Y", 310, 1.0)
    y0 = 390
    card(d, (40, y0, 1040, y0 + 600), fill=WHITE, outline=LIGHT, w=3)
    text(d, (250, y0 + 65), "P (W)", FL, ORANGE)
    for x, nm in ((640, "X"), (880, "Y")): text(d, (x, y0 + 65), nm, FL, INK)
    d.line([(70, y0 + 115), (1010, y0 + 115)], fill=LIGHT, width=3)
    for j, (lab, key) in enumerate((("nối tiếp", "nt"), ("song song", "ss"))):
        yy = y0 + 240 + j * 220
        text(d, (250, yy), lab, FL, INK)
        px, py = ROWS[2 * j][4], ROWS[2 * j + 1][4]
        for x, nm, p in ((640, "X", px), (880, "Y", py)):
            k = appear(t, 0.6 + 0.4 * (2 * j + (nm == "Y")), 0.35)
            big = p == max(px, py)
            if big and k > 0.9: d.rounded_rectangle([x - 105, yy - 60, x + 105, yy + 60], radius=24, fill=(255, 237, 213))
            if k > 0: text(d, (x, yy), vp(p), 68 if big else FL, ORANGE if big else GRAY, alpha=k)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        y1 = 1060 + (1 - k2) * 30
        card(d, (40, y1, 1040, y1 + 260), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, y1 + 85), "P = U·I", 72, DGREEN, alpha=k2)
        text(d, (W / 2, y1 + 185), "P lớn hơn → sáng hơn", FL, DGREEN, alpha=k2)


# ---------------- canh 4: Rut ra (hai the, chay dong dien o the noi tiep) ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, 0.2, 0.45)
    card(d, (40, 262, 1040, 860), fill=A((255, 247, 237), k1), outline=A(ORANGE, k1), w=5)
    text(d, (W / 2, 320), "Nối tiếp: cùng I", FL, (154, 52, 18), alpha=k1)
    # mach nho: hai bong noi tiep, cham dong dien chay vong
    x0, x1, y0, y1 = 140, 940, 480, 660
    d.rectangle([x0, y0, x1, y1], outline=A(WIRE, k1), width=6)
    pts_len = 2 * (x1 - x0) + 2 * (y1 - y0)
    for i in range(14):
        s = (t * 260 + i * pts_len / 14) % pts_len
        if s < x1 - x0: px, py = x0 + s, y0
        elif s < (x1 - x0) + (y1 - y0): px, py = x1, y0 + s - (x1 - x0)
        elif s < 2 * (x1 - x0) + (y1 - y0): px, py = x1 - (s - (x1 - x0) - (y1 - y0)), y1
        else: px, py = x0, y1 - (s - 2 * (x1 - x0) - (y1 - y0))
        dot(d, px, py, 14, A(BLUE, k1 * 0.8))
    for cx, nm, r in ((400, "X", R_X), (680, "Y", R_Y)):
        bulb(d, cx, y0, 50, LOOK[("nt", nm)], alpha=k1)
        text(d, (cx, y0 + 120), f"{vn(r, 0)} Ω", FL, INK, alpha=k1)
    text(d, (W / 2, 790), "R lớn → P lớn", FL, (154, 52, 18), alpha=k1)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        y2 = 900 + (1 - k2) * 30
        card(d, (40, y2, 1040, y2 + 340), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, y2 + 80), "Song song: đủ 6 V", FL, DGREEN, alpha=k2)
        text(d, (W / 2, y2 + 175), "P = số ghi trên đèn", FL, DGREEN, alpha=k2)
        for cx, nm in ((420, "X"), (660, "Y")):
            bulb(d, cx, y2 + 270, 40, LOOK[("ss", nm)], alpha=k2)


# ---------------- canh 5: Bay roi Chua noi duoc ----------------
BAY_R, BAY_C = 3.4, 6.4
def s_bay(img, d, t, sc):
    a1 = appear(t, 0.3, 0.45)
    pw = tw(d, "BẪY", F(FS)) + 64
    card(d, (W / 2 - pw / 2, 268, W / 2 + pw / 2, 348), fill=A(DRED, a1), r=40)
    text(d, (W / 2, 308), "BẪY", FS, WHITE, alpha=a1)
    text(d, (W / 2, 410), "“Nhiều oát luôn sáng hơn”", FL, INK, alpha=a1)
    card(d, (40, 470, 530, 1240), fill=A(WHITE, a1), outline=A(DRED, a1), w=5)
    text(d, (285, 540), "nghĩ", FS, DRED, alpha=a1)
    for cy, nm, look in ((720, "X", LOOK[("nt", "Y")]), (950, "Y", LOOK[("ss", "Y")])):
        bulb(d, 200, cy, 56, look, alpha=a1)
        text(d, (370, cy), f"{nm} · {PDM[nm]} W", FS, INK, alpha=a1)
    text(d, (285, 1170), "✗ Y sáng hơn", FS, DRED, alpha=a1)
    a2 = appear(t, BAY_R, 0.45)
    if a2 > 0:
        card(d, (550, 470, 1040, 1240), fill=A(WHITE, a2), outline=A(DGREEN, a2), w=5)
        text(d, (795, 540), "tính P", FS, DGREEN, alpha=a2)
        for cy, nm in ((720, "X"), (950, "Y")):
            bulb(d, 710, cy, 56, LOOK[("nt", nm)], alpha=a2)
            p = ROWS[0][4] if nm == "X" else ROWS[1][4]
            text(d, (900, cy), vp(p) + " W", FS, ORANGE, alpha=a2)
        text(d, (795, 1170), "✓ X sáng hơn", FS, DGREEN, alpha=a2)
    k3 = appear(t, BAY_C, 0.45)
    if k3 > 0:
        card(d, (40, 1290, 1040, 1560), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1360), "Chưa nói được:", FL, NAVY, alpha=k3)
        text(d, (W / 2, 1465), "coi điện trở đèn không đổi", FL, INK, alpha=k3)


# ---------------- canh 6: Chot + THU NGHI ----------------
END_Q, END_C = 0.2, 3.0
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 415), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 340), "Số oát đúng khi đủ 6 V", FS, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 450, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(FS)) + 60
    card(d, (W / 2 - pw / 2, 478, W / 2 + pw / 2, 558), fill=A(ORANGE, k1), r=40)
    text(d, (W / 2, 518), "THỬ NGHĨ", FS, WHITE, alpha=k1)
    text(d, (W / 2, 650), "X, Y song song vào 3 V.", FL, INK, alpha=k1)
    text(d, (W / 2, 735), "Đèn Y tiêu thụ mấy oát?", FL, INK, alpha=k1)
    # so do nho: nguon 3 V, hai nhanh
    if k1 > 0.5:
        xl, xr, yt, yb = 200, 880, 900, 1250
        card(d, (100, 1010, 240, 1140), fill=BODY, r=16)
        text(d, (170, 1075), "3 V", FS, WHITE)
        d.line([(170, 1010), (170, yt), (xr, yt), (xr, yb), (170, yb), (170, 1140)], fill=WIRE, width=6, joint="curve")
        d.line([(420, yt), (420, 1080), (xr, 1080)], fill=WIRE, width=6, joint="curve")
        for cy, nm in ((yt, "X"), (1080, "Y")):
            bulb(d, 600, cy, 46, None)
            text(d, (760, cy - 60 if nm == "X" else cy + 70), f"{nm} · {PDM[nm]} W", FS, INK)
    card(d, (290, 1320, 790, 1450), fill=A(SCREEN, k1), r=20)
    text(d, (540, 1385), "P(Y) = ? W", 64, ORANGE, alpha=k1)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
           (do["t0"] + T_K1, "tap"), (do["t0"] + T_SW, "tick"), (do["t0"] + T_K2, "tap")]
    out += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + 0.3, "buzz"),
            (b["t0"] + BAY_R, "tap"), (e["t0"] + END_Q + 0.1, "open")]
    return out


CLIP = dict(id="tn-l9-congsuat-03", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Công suất điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai đèn 6 V khác số oát", draw=s_hook, tail=0.3, caps=[
   ("Đèn X 3 W, đèn Y 6 W.", 2.9),
   ("Dừng lại, tự đoán.", 5.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Nối tiếp: đóng K, nhìn đèn.", 3.4),
   ("Đổi sang mắc song song.", 3.2),
   ("So độ sáng hai lần.", 3.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Tính P = U·I từng đèn.", 3.0),
   ("Thứ tự sáng đổi ngược.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Vì sao X sáng hơn?", 3.0),
   ("Còn song song?", 3.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.2, caps=[
   ("Nghe hợp lí?", 3.0),
   ("Tính P mới biết.", 3.0),
   ("Còn bỏ ngỏ.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.2, caps=[
   ("Dừng lại, tự tính.", 6.1)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
