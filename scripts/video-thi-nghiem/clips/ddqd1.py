# Clip: tn-l10-dd-qd-01 - Xe do choi chay tren ray uon: s do bang soi chi, d do bang thuoc (31/10/2026; dung lai
#   27/11/2026 theo cong moi viec 4: --do-chu 0 LOI, chu ve >= 56 px, Du doan khong nut A-D, THU NGHI cau chot A-D o web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-dd-qd-01.json -> so_lieu_mau (s do / d do, cm):
#   thang 30 cm: 30,2 / 30,0 ; nua vong r = 10 cm: 31,9 / 20,1 ; chu L 30 + 40 cm: 70,6 / 49,9 ;
#   tron vong r = 10 cm: 63,5 / 0,0.  Mo hinh d = 2r.sin(theta/2); tham_so: r 5-20 cm, theta 0-2pi.
# Video nam trong hop exp (bai co 'Doc bang' tinh d = 2r = 20; sau hop). Du doan: nua vong d ~ ? (la chinh thi nghiem).
# Chot (THU NGHI, chua chieu, khac bai: bai co 1,5 vong r = 50 m): 3/4 vong r = 10 cm -> d = r.can2 ~ 14 cm (theo mo hinh).
from engine import *

ROWS = [("thẳng 30 cm", "30,2", "30,0"), ("nửa vòng r = 10 cm", "31,9", "20,1"),
        ("chữ L 30 + 40 cm", "70,6", "49,9"), ("trọn vòng r = 10 cm", "63,5", "0,0")]   # so_lieu_mau
RAIL, RAIL_D = (214, 219, 228), (120, 130, 150)
CAR, TAPE = (220, 38, 38), (250, 204, 21)
DGREEN = (21, 128, 61); DRED = (185, 28, 28); BROWN = (154, 52, 18)

# ---------- hinh dang ray (cm, truc y huong xuong man hinh), u = 0..1 doc ray ----------
def pt(k, u):
    u = clamp(u)
    if k == 0: return (-15 + 30 * u, 0.0)                                   # thang 30 cm
    if k == 1:                                                              # nua vong r = 10, lom xuong
        a = math.pi - math.pi * u; return (10 * math.cos(a), 5 - 10 * math.sin(a))
    if k == 2:                                                              # chu L: len 30 roi sang phai 40
        L = 70 * u
        return (-20.0, 15 - L) if L <= 30 else (-20 + (L - 30), -15.0)
    a = math.pi / 2 - 2 * math.pi * u; return (10 * math.cos(a), 10 * math.sin(a))  # tron vong, xuat phat o day

def S(O, sc, p): return (O[0] + p[0] * sc, O[1] + p[1] * sc)

def rail(d, k, O, sc, alpha=1.0, w=26):
    pts = [S(O, sc, pt(k, i / 120)) for i in range(121)]
    d.line(pts, fill=A(RAIL_D, alpha), width=w, joint="curve")
    d.line(pts, fill=A(RAIL, alpha), width=w - 8, joint="curve")

def thread(d, k, O, sc, u, alpha=1.0, w=7):
    n = max(2, int(120 * u) + 1)
    pts = [S(O, sc, pt(k, u * i / (n - 1))) for i in range(n)]
    d.line(pts, fill=A(ORANGE, alpha), width=w, joint="curve")

def tape(d, k, O, sc, u, alpha=1.0):
    p = pt(k, u); q = pt(k, clamp(u + 0.01) if u < 0.99 else u - 0.01)
    ang = math.atan2(q[1] - p[1], q[0] - p[0]); c = S(O, sc, p)
    nx, ny = -math.sin(ang), math.cos(ang); tx, ty = math.cos(ang), math.sin(ang)
    hl, hw = 30, 9
    poly = [(c[0] + nx * hl + tx * hw, c[1] + ny * hl + ty * hw), (c[0] + nx * hl - tx * hw, c[1] + ny * hl - ty * hw),
            (c[0] - nx * hl - tx * hw, c[1] - ny * hl - ty * hw), (c[0] - nx * hl + tx * hw, c[1] - ny * hl + ty * hw)]
    d.polygon(poly, fill=A(TAPE, alpha), outline=A((161, 98, 7), alpha))

def car(d, k, O, sc, u, alpha=1.0):
    p = pt(k, u); e = 0.004
    a, b = pt(k, u - e if u > e else 0), pt(k, u + e if u < 1 - e else 1)
    ang = math.atan2(b[1] - a[1], b[0] - a[0]); c = S(O, sc, p)
    tx, ty = math.cos(ang), math.sin(ang); nx, ny = -ty, tx
    def box(l, w, ox=0.0, oy=0.0):
        cx, cy = c[0] + tx * ox + nx * oy, c[1] + ty * ox + ny * oy
        return [(cx + tx * l + nx * w, cy + ty * l + ny * w), (cx - tx * l + nx * w, cy - ty * l + ny * w),
                (cx - tx * l - nx * w, cy - ty * l - ny * w), (cx + tx * l - nx * w, cy + ty * l - ny * w)]
    for ox in (-15, 15):
        for oy in (-17, 17): d.polygon(box(7, 5, ox, oy), fill=A(NAVY, alpha))
    d.polygon(box(26, 15), fill=A(CAR, alpha), outline=A(DRED, alpha))
    d.polygon(box(8, 10, 8), fill=A((254, 226, 226), alpha))

def d_arrow(d, k, O, sc, alpha=1.0, grow=1.0, lab="d"):
    p0, p1 = S(O, sc, pt(k, 0)), S(O, sc, pt(k, 1))
    if k == 3:                                                              # diem dau trung diem cuoi
        r = 40 * grow
        if r > 1: d.ellipse([p0[0] - r, p0[1] - r, p0[0] + r, p0[1] + r], outline=A(GREEN, alpha), width=6)
        if grow >= 1: text(d, (p0[0] + 56, p0[1] + 74), "d = 0", 56, DGREEN, anchor="lm", alpha=alpha)
        return
    off = 52 if k == 0 else 0
    a = (p0[0], p0[1] + off); b = (lerp(p0[0], p1[0], grow), lerp(p0[1], p1[1], grow) + off)
    if math.dist(a, b) < 4: return
    arrow(d, a, b, A(GREEN, alpha), w=8, head=32)
    if grow >= 1 and lab:
        ux, uy = (b[0] - a[0]) / math.dist(a, b), (b[1] - a[1]) / math.dist(a, b)
        nx, ny = -uy, ux
        if ny < 0: nx, ny = -nx, -ny                                        # nhan nam phia duoi mui ten
        text(d, ((a[0] + b[0]) / 2 + nx * 48, (a[1] + b[1]) / 2 + ny * 48), lab, 56, DGREEN, alpha=alpha)

ROWS2 = [("thẳng", "30,2", "30,0"), ("nửa vòng", "31,9", "20,1"), ("chữ L", "70,6", "49,9"), ("trọn vòng", "63,5", "0,0")]

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-dd-qd-01.json")))
    h = k["so_lieu_mau"]["hang"]
    for (_, s_, d_), r in zip(ROWS, h): assert (float(s_.replace(",", ".")), float(d_.replace(",", "."))) == (r[2], r[4]), r
    assert abs(2 * 10 * math.sin(math.radians(135)) - 14.14) < 0.01
_kiem_so()

def cbar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0))
    d.rounded_rectangle([110, y, 970, y + 80], radius=40, fill=A((246, 244, 250), a))
    if p < 1: d.rounded_rectangle([110, y, 110 + max(80, 860 * (1 - p)), y + 80], radius=40, fill=A(col, a))

def pill(d, y, s, col, k):
    pw = tw(d, s, F(56)) + 60
    card(d, (W / 2 - pw / 2, y, W / 2 + pw / 2, y + 76), fill=A(col, k), r=36)
    text(d, (W / 2, y + 38), s, 56, WHITE, alpha=k)

def legend(d, y, a=1.0, full=True):
    d.line([(120, y), (190, y)], fill=A(ORANGE, a), width=14)
    text(d, (210, y), "s: quãng đường" + (" (sợi chỉ)" if full else ""), 56, BROWN, anchor="lm", alpha=a)
    arrow(d, (115, y + 72), (195, y + 72), A(GREEN, a), w=8, head=26)
    text(d, (210, y + 72), "d: độ dịch chuyển" + (" (thước)" if full else ""), 56, DGREEN, anchor="lm", alpha=a)

# ---------------- canh 1: Du doan ----------------
HO, HSC = (540, 560), 30
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k = appear(t, 0.1)
    rail(d, 1, HO, HSC, alpha=k, w=34)
    u = ease((t - 0.6) / 1.8)
    if t > 0.6: thread(d, 1, HO, HSC, u)
    tape(d, 1, HO, HSC, 0.0, alpha=k)
    if u >= 1: tape(d, 1, HO, HSC, 1.0)
    car(d, 1, HO, HSC, u, alpha=k)
    ctr = S(HO, HSC, (0, 5)); top = S(HO, HSC, (0, -5))
    for j in range(9):                                                      # ban kinh net dut
        y0 = lerp(ctr[1], top[1] + 20, j / 9); y1 = lerp(ctr[1], top[1] + 20, (j + 0.55) / 9)
        d.line([(ctr[0], y0), (ctr[0], y1)], fill=A(NAVY, k), width=4)
    dot(d, ctr[0], ctr[1], 7, A(NAVY, k))
    text(d, (ctr[0] + 24, ctr[1] - 80), "r = 10 cm", 56, NAVY, anchor="lm", alpha=k)
    kq = appear(t, M[1] - 0.3, 0.45)
    if kq <= 0: return
    y0 = 860 + (1 - kq) * 30
    card(d, (50, y0, 1030, y0 + 640), fill=A(WHITE, kq), outline=A(PURPLE, kq), w=6)
    pill(d, y0 + 22, "DỰ ĐOÁN", PURPLE, kq)
    cbar(d, y0 + 118, t, M[1] + 0.3, sc["T"] - 0.15, DPURP, kq)
    text(d, (W / 2, y0 + 330), "Hết nửa vòng, độ lớn d", 62, INK, alpha=kq)
    text(d, (W / 2, y0 + 440), "khoảng bao nhiêu cm?", 62, PURPLE, alpha=kq)

# ---------------- canh 2: Tien hanh (4 hinh ray) ----------------
DO_O, DSC = (540, 700), 13
R0, RUN = 0.6, 3.0
MV0, MV1, SAT, DG0, DG1, DAT = 0.25, 1.55, 1.60, 1.75, 2.15, 2.20     # moc trong moi lan (giay)
BADGE = R0 + 4 * RUN + 0.1
COLX = (100, 660, 890)
DIM = {0: [((0, -4), "30 cm", "mm")], 1: [((0, -9), "r = 10 cm", "mm")],
       2: [((-23, 0), "30 cm", "rm"), ((0, -19), "40 cm", "mm")], 3: [((11.5, 0), "r = 10 cm", "lm")]}

def run_state(i, t):
    tau = t - (R0 + RUN * i)
    u = ease((tau - MV0) / (MV1 - MV0))
    return u, tau >= SAT, clamp((tau - DG0) / (DG1 - DG0)), tau >= DAT

def row_on(i, t): return t >= (0.0 if i == 0 else R0 + RUN * i)

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    legend(d, 300)
    if t < BADGE:
        i = max(0, min(3, int((t - R0) // RUN))) if t >= R0 else 0
        tau = t - (R0 + RUN * i)
        u, s_on, g, d_on = run_state(i, t)
        rail(d, i, DO_O, DSC)
        for p, lab, an in DIM[i]: text(d, S(DO_O, DSC, p), lab, 56, NAVY, anchor=an)
        if u > 0: thread(d, i, DO_O, DSC, u)
        tape(d, i, DO_O, DSC, 0.0)
        if u >= 1 and i != 3: tape(d, i, DO_O, DSC, 1.0)
        car(d, i, DO_O, DSC, u, alpha=1 - 0.7 * g)
        if g > 0: d_arrow(d, i, DO_O, DSC, grow=g, lab="d" if d_on else "")
    else:                                                                   # dap an: quay lai nua vong
        rail(d, 1, DO_O, DSC); thread(d, 1, DO_O, DSC, 1.0)
        tape(d, 1, DO_O, DSC, 0.0); tape(d, 1, DO_O, DSC, 1.0)
        text(d, S(DO_O, DSC, (0, -9)), "r = 10 cm", 56, NAVY)
        d_arrow(d, 1, DO_O, DSC, lab="d = 2r")
    card(d, (60, 915, 1020, 1330), fill=WHITE, outline=NAVY, w=4)
    text(d, (COLX[0], 975), "Ray", 56, INK, anchor="lm")
    text(d, (COLX[1], 975), "s (cm)", 56, BROWN); text(d, (COLX[2], 975), "d (cm)", 56, DGREEN)
    d.line([(90, 1012), (990, 1012)], fill=LIGHT, width=4)
    kb = appear(t, BADGE, 0.4)
    for i, (lab, sv, dv) in enumerate(ROWS2):
        if not row_on(i, t): continue
        yy = 1050 + i * 74; _, s_on, _, d_on = run_state(i, t)
        if kb > 0 and i == 1:
            d.rounded_rectangle([80, yy - 33, 1000, yy + 33], radius=14, fill=A((220, 252, 231), kb))
        elif t < BADGE and t - (R0 + RUN * i) < RUN:
            d.rounded_rectangle([80, yy - 33, 1000, yy + 33], radius=14, fill=(239, 246, 255))
        text(d, (COLX[0], yy), lab, 56, NAVY, anchor="lm")
        if s_on: text(d, (COLX[1], yy), sv, 56, BROWN)
        if d_on: text(d, (COLX[2], yy), dv, 56, DGREEN)
    if kb > 0:
        s_ = "ĐÁP ÁN: khoảng 20 cm"; pw = tw(d, s_, F(58)) + 70
        card(d, (W / 2 - pw / 2, 1365, W / 2 + pw / 2, 1465), fill=A((220, 252, 231), kb), outline=A(GREEN, kb), r=28, w=5)
        text(d, (W / 2, 1415), s_, 58, DGREEN, alpha=kb)

# ---------------- canh 3: Rut ra ----------------
BX0, BPX = 400, 8.0
BARS = [("thẳng", 30.2, 30.0), ("nửa vòng", 31.9, 20.1), ("chữ L", 70.6, 49.9), ("trọn vòng", 63.5, 0.0)]
def s_rutra(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.1)
    card(d, (60, 260, 1020, 410), fill=A((239, 246, 255), a), r=30)
    text(d, (W / 2, 335), "Độ lớn d ≤ s", 64, BLUE, alpha=a)
    card(d, (60, 440, 1020, 1300), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    legend(d, 500, a, full=False)
    g = ease((t - 0.3) / 1.4)
    for i, (lab, sv, dv) in enumerate(BARS):
        y = 700 + i * 148
        hi = (i == 0 and t >= M[0] - 0.05 and t < M[1] - 0.05) or (i > 0 and t >= M[1] - 0.05)
        if hi:
            col = (220, 252, 231) if i == 0 else (255, 237, 213)
            pa = 0.75 + 0.25 * math.sin(t * 4 + i)
            d.rounded_rectangle([80, y - 52, 1000, y + 72], radius=18, fill=A(col, a * pa))
        text(d, (100, y + 10), lab, 56, INK, anchor="lm", alpha=a)
        d.rectangle([BX0, y - 18, BX0 + sv * BPX * g, y + 6], fill=A(ORANGE, a))
        if dv > 0: d.rectangle([BX0, y + 18, BX0 + dv * BPX * g, y + 42], fill=A(GREEN, a))
        else: d.line([(BX0, y + 12), (BX0, y + 48)], fill=A(GREEN, a), width=6)

# ---------------- canh 4: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.05, 0.35)
    card(d, (60, 260, 1020, 1300), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, 350), "Chưa nói được", 62, NAVY, alpha=k)
    text(d, (W / 2, 470), "Hướng của d?", 62, BLUE, alpha=k)
    yA = 800; xa, xb = 300, 780                                            # thuoc dat giua hai bang dinh
    d.rectangle([xa - 40, yA + 20, xb + 40, yA + 90], fill=A((254, 249, 195), k), outline=A((161, 98, 7), k), width=3)
    for j in range(0, 29):
        x = xa - 40 + j * (xb - xa + 80) / 28
        d.line([(x, yA + 20), (x, yA + (52 if j % 2 == 0 else 40))], fill=A((161, 98, 7), k), width=3)
    for x in (xa, xb):
        d.rectangle([x - 9, yA - 30, x + 9, yA + 30], fill=A(TAPE, k), outline=A((161, 98, 7), k))
    d.line([(xa, yA), (xb, yA)], fill=A(GREEN, k), width=8)
    ang = math.radians(180 * (0.5 + 0.5 * math.sin(t * 2.2)))               # mui ten quay: huong chua biet
    cx, cy, L = W / 2, 1080, 150
    arrow(d, (cx - L * math.cos(ang), cy - L * math.sin(ang) * 0.3), (cx + L * math.cos(ang), cy + L * math.sin(ang) * 0.3),
          A(GREEN, k), w=8, head=30)

# ---------------- canh 5: Bay ----------------
BO, BSC = (560, 1150), 11
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    card(d, (60, 260, 1020, 520), fill=A(WHITE, a), outline=A(DRED, a), w=6)
    text(d, (W / 2, 390), "✗ d = 30 + 40 = 70 cm", 60, DRED, alpha=a)
    card(d, (60, 560, 1020, 1560), fill=A(WHITE, a), outline=A(GREEN if t >= M[1] - 0.05 else NAVY, a), w=5)
    rail(d, 2, BO, BSC, w=22, alpha=a); thread(d, 2, BO, BSC, 1.0, w=6, alpha=a)
    tape(d, 2, BO, BSC, 0.0, alpha=a); tape(d, 2, BO, BSC, 1.0, alpha=a)
    p0, pc, p1 = S(BO, BSC, pt(2, 0)), S(BO, BSC, (-20, -15)), S(BO, BSC, pt(2, 1))
    text(d, (p0[0] - 30, (p0[1] + pc[1]) / 2), "30 cm", 56, BROWN, anchor="rm", alpha=a)
    text(d, ((pc[0] + p1[0]) / 2, pc[1] - 56), "40 cm", 56, BROWN, alpha=a)
    if t < M[1] - 0.05:
        car(d, 2, BO, BSC, (t * 0.35) % 1.0, alpha=a)                       # xe chay lai doan L
        return
    g = clamp((t - (M[1] - 0.05)) / 0.5)
    b = (lerp(p0[0], p1[0], g), lerp(p0[1], p1[1], g)); arrow(d, p0, b, GREEN, w=8, head=32)
    text(d, (W / 2, 640), "✓ d ≈ 50 cm", 60, DGREEN)
    if g >= 1: text(d, ((p0[0] + p1[0]) / 2 + 50, (p0[1] + p1[1]) / 2 + 50), "d", 60, DGREEN)

# ---------------- canh 6: THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 220, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, 250, "THỬ NGHĨ", ORANGE, k1)
    O3, s3 = (480, 610), 13
    pts = [S(O3, s3, pt(3, 0.75 * i / 90)) for i in range(91)]
    d.line(pts, fill=A(RAIL_D, k1), width=24, joint="curve"); d.line(pts, fill=A(RAIL, k1), width=16, joint="curve")
    tape(d, 3, O3, s3, 0.0, alpha=k1); tape(d, 3, O3, s3, 0.75, alpha=k1)
    for j in range(7):                                                      # ban kinh net dut sang phai
        d.line([(O3[0] + j * 19, O3[1]), (O3[0] + j * 19 + 10, O3[1])], fill=A(NAVY, k1), width=4)
    dot(d, O3[0], O3[1], 6, A(NAVY, k1))
    text(d, (O3[0] + 170, O3[1]), "r = 10 cm", 56, NAVY, anchor="lm", alpha=k1)
    car(d, 3, O3, s3, 0.75 * ((t * 0.3) % 1.0), alpha=k1)
    text(d, (W / 2, 960), "Xe chạy 3/4 vòng tròn.", 60, INK, alpha=k1)
    text(d, (W / 2, 1060), "Độ lớn d khoảng", 60, ORANGE, alpha=k1)
    text(d, (W / 2, 1150), "bao nhiêu cm?", 60, ORANGE, alpha=k1)
    cbar(d, 1300, t, 1.0, sc["T"] - 0.2, DORANGE, k1)

DPURP = (91, 33, 182); DORANGE = (176, 64, 8)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, b, e = sc["hook"], sc["do"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
            (do["t0"] + BADGE, "ding"), (b["t0"] + 0.3, "buzz"), (b["t0"] + b["M"][1], "ding"),
            (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l10-dd-qd-01", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Độ dịch chuyển · thachlab.id.vn", scenes=[
 dict(key="hook", title="Xe chạy trên ray uốn", draw=s_hook, tail=0.3, caps=[
   ("Ray uốn nửa vòng tròn.", 3.0),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Bốn hình ray", draw=s_do, tail=0.4, caps=[
   ("Chỉ dọc ray đo s, thước đo d.", BADGE - 0.4),
   ("Nửa vòng: d bằng đường kính.", 3.2)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.4, caps=[
   ("Thẳng, không quay đầu: d = s.", 3.0),
   ("Cong hoặc quay về: d < s.", 3.0)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("Thước chỉ cho độ lớn.", 3.6)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Cộng hai đoạn: đó là s.", 3.4),
   ("d nối thẳng đầu với cuối.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự trả lời.", 5.2)]),
])
