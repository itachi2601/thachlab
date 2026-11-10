# Clip: tn-l10-dd-qd-01 - Xe do choi chay tren ray uon: s do bang soi chi, d do bang thuoc (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-dd-qd-01.json -> so_lieu_mau (s do / d do, cm):
#   thang 30 cm: 30,2 / 30,0 ; nua vong r = 10 cm: 31,9 / 20,1 ; chu L 30 + 40 cm: 70,6 / 49,9 ;
#   tron vong r = 10 cm: 63,5 / 0,0.  Mo hinh: 31,4 ; 20,0 ; 70 ; 50,0 ; 62,8.  tham_so: r 5-20 cm, theta 0-2pi.
# Canh: Du doan (nua vong r = 10 cm: d khoang bao nhieu? K10: chi cau hoi + hinh) -> Tien hanh (4 hinh ray, vet chi cam
#       = s, mui ten xanh la = d, bang dien dung luc do xong) -> Dap an (d = duong kinh) -> Rut ra (thanh s/d) ->
#       Chua noi duoc gi (huong cua d) -> Bay (30 + 40 = 70) -> Chot + cau hoi 3/4 vong r = 10 cm (theta = 3pi/2,
#       d = r.can2 ~ 14 cm: gia tri chua tung hien tren man, khac ca Du doan).
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
        if grow >= 1: text(d, (p0[0] + 56, p0[1] + 74), "d = 0", 40, DGREEN, anchor="lm", alpha=alpha)
        return
    off = 52 if k == 0 else 0
    a = (p0[0], p0[1] + off); b = (lerp(p0[0], p1[0], grow), lerp(p0[1], p1[1], grow) + off)
    if math.dist(a, b) < 4: return
    arrow(d, a, b, A(GREEN, alpha), w=8, head=32)
    if grow >= 1:
        ux, uy = (b[0] - a[0]) / math.dist(a, b), (b[1] - a[1]) / math.dist(a, b)
        nx, ny = -uy, ux
        if ny < 0: nx, ny = -nx, -ny                                        # nhan nam phia duoi mui ten
        text(d, ((a[0] + b[0]) / 2 + nx * 42, (a[1] + b[1]) / 2 + ny * 42), lab, 42, DGREEN, alpha=alpha)

# ---------------- canh 1: du doan ----------------
HO, HSC = (540, 600), 30
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k = appear(t, 0.1)
    rail(d, 1, HO, HSC, alpha=k, w=34)
    u = ease((t - 0.6) / 1.8)
    if t > 0.6: thread(d, 1, HO, HSC, u)
    tape(d, 1, HO, HSC, 0.0, alpha=k)
    if u >= 1: tape(d, 1, HO, HSC, 1.0)
    car(d, 1, HO, HSC, u, alpha=k)
    kc = appear(t, 0.5)
    ctr = S(HO, HSC, (0, 5)); top = S(HO, HSC, (0, -5))
    for j in range(9):                                                      # ban kinh net dut
        y0 = lerp(ctr[1], top[1] + 20, j / 9); y1 = lerp(ctr[1], top[1] + 20, (j + 0.55) / 9)
        d.line([(ctr[0], y0), (ctr[0], y1)], fill=A(NAVY, kc), width=4)
    dot(d, ctr[0], ctr[1], 7, A(NAVY, kc))
    text(d, (ctr[0] + 28, ctr[1] - 70), "r = 10 cm", 42, NAVY, anchor="lm", alpha=kc)
    kq = appear(t, M[1] - 0.4, 0.5)
    if kq <= 0: return
    y0 = 960 + (1 - kq) * 30
    card(d, (60, y0, 1020, y0 + 560), fill=A(WHITE, kq), outline=A(PURPLE, kq), w=6)
    pw = tw(d, "Dự đoán", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, kq), r=32)
    text(d, (W / 2, y0 + 60), "Dự đoán", 40, WHITE, alpha=kq)
    ctext(d, y0 + 175, "Độ lớn độ dịch chuyển d", 46, INK, alpha=kq)
    ctext(d, y0 + 240, "của xe khoảng bao nhiêu?", 46, INK, alpha=kq)
    card(d, (W / 2 - 80, y0 + 300, W / 2 + 80, y0 + 450), fill=A((245, 243, 255), kq), outline=A(PURPLE, kq), r=26, w=4)
    text(d, (W / 2, y0 + 375), "?", 90, PURPLE, alpha=kq)
    t1, t2 = M[1] - 0.2, sc["T"] - 0.2; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([200, y0 + 500, 880, y0 + 516], radius=8, fill=A(LIGHT, kq))
    if q < 1: d.rounded_rectangle([200, y0 + 500, 200 + 680 * (1 - q), y0 + 516], radius=8, fill=A(PURPLE, kq))

# ---------------- canh 2: tien hanh (4 hinh ray) ----------------
DO_O, DSC = (540, 590), 15
R0, RUN = 0.6, 2.3
MV0, MV1, SAT, DG0, DG1, DAT = 0.25, 1.25, 1.30, 1.40, 1.75, 1.80     # moc trong moi lan (giay)
BADGE = R0 + 4 * RUN + 0.1
COLX = (100, 700, 900)

def run_state(i, t):
    """Lan i luc t: (u xe, da hien s, tien do mui ten d, da hien d)."""
    tau = t - (R0 + RUN * i)
    u = ease((tau - MV0) / (MV1 - MV0))
    return u, tau >= SAT, clamp((tau - DG0) / (DG1 - DG0)), tau >= DAT

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    if t < BADGE:
        i = max(0, min(3, int((t - R0) // RUN))) if t >= R0 else 0
        tau = t - (R0 + RUN * i); k = appear(tau, 0.0, 0.25) if i > 0 else appear(t, 0.1)
        u, s_on, g, d_on = run_state(i, t)
        rail(d, i, DO_O, DSC, alpha=k)
        if u > 0: thread(d, i, DO_O, DSC, u, alpha=k)
        tape(d, i, DO_O, DSC, 0.0, alpha=k)
        if u >= 1 and i != 3: tape(d, i, DO_O, DSC, 1.0)
        car(d, i, DO_O, DSC, u, alpha=k * (1 - 0.7 * g))                 # xe mo di khi dat thuoc: thay dau mui ten d
        if g > 0: d_arrow(d, i, DO_O, DSC, grow=g)                     # mui ten ve sau xe: dau mui ten khong bi che
    else:                                                                   # dap an: quay lai nua vong
        ka = appear(t, BADGE, 0.4)
        rail(d, 1, DO_O, DSC, alpha=ka); thread(d, 1, DO_O, DSC, 1.0, alpha=ka)
        tape(d, 1, DO_O, DSC, 0.0, alpha=ka); tape(d, 1, DO_O, DSC, 1.0, alpha=ka)
        d_arrow(d, 1, DO_O, DSC, alpha=ka, lab="2r = 20 cm")
    if t < BADGE:                                                           # nhac lai cau du doan
        cs = "Dự đoán: nửa vòng, d = ?"; pw = tw(d, cs, F(38)) + 56
        card(d, (W / 2 - pw / 2, 846, W / 2 + pw / 2, 896), fill=(245, 243, 255), outline=PURPLE, r=25, w=3)
        text(d, (W / 2, 871), cs, 38, PURPLE)
    # bang so lieu: s hien khi xe dung (chi dat xong), d hien khi mui ten thuoc ve xong
    card(d, (60, 905, 1020, 1250), fill=WHITE, outline=NAVY, w=4)
    text(d, (COLX[0], 950), "Hình ray", 40, INK, anchor="lm")
    text(d, (COLX[1], 950), "s đo (cm)", 40, BROWN); text(d, (COLX[2], 950), "d đo (cm)", 40, DGREEN)
    d.line([(90, 982), (990, 982)], fill=LIGHT, width=4)
    kb = appear(t, BADGE, 0.4)
    for i, (lab, sv, dv) in enumerate(ROWS):
        tau = t - (R0 + RUN * i)
        if tau < 0: continue
        yy = 1022 + i * 60; _, s_on, _, d_on = run_state(i, t)
        if kb > 0 and i == 1:
            d.rounded_rectangle([80, yy - 28, 1000, yy + 28], radius=14, fill=A((220, 252, 231), kb))
        elif t < BADGE and tau < RUN:
            d.rounded_rectangle([80, yy - 28, 1000, yy + 28], radius=14, fill=(239, 246, 255))
        text(d, (COLX[0], yy), lab, 40, NAVY, anchor="lm")
        if s_on: text(d, (COLX[1], yy), sv, 40, BROWN)
        if d_on: text(d, (COLX[2], yy), dv, 40, DGREEN)
    if kb > 0:
        s_ = "ĐÁP ÁN · khoảng 20 cm"; pw = tw(d, s_, F(46)) + 70
        card(d, (W / 2 - pw / 2, 1300, W / 2 + pw / 2, 1404), fill=A((220, 252, 231), kb), outline=A(GREEN, kb), r=26, w=4)
        text(d, (W / 2, 1352), s_, 46, GREEN, alpha=kb)

# ---------------- canh 3: rut ra (thanh s / d) ----------------
BX0, BPX = 380, 8.4                                                         # thanh bat dau x, px/cm (70,6 cm -> 593 px)
BARS = [("thẳng", 30.2, 30.0), ("nửa vòng", 31.9, 20.1), ("chữ L", 70.6, 49.9), ("trọn vòng", 63.5, 0.0)]
def s_rutra(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.1)
    card(d, (60, 270, 1020, 420), fill=A((239, 246, 255), a), r=30)
    text(d, (W / 2, 345), "Độ lớn d ≤ s", 64, BLUE, alpha=a)
    card(d, (60, 450, 1020, 1300), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    d.line([(BX0 - 34, 520), (BX0 + 10, 520)], fill=A(ORANGE, a), width=14)
    text(d, (BX0 + 30, 520), "s", 42, BROWN, anchor="lm", alpha=a)
    d.line([(BX0 + 160, 520), (BX0 + 204, 520)], fill=A(GREEN, a), width=14)
    text(d, (BX0 + 224, 520), "d", 42, DGREEN, anchor="lm", alpha=a)
    for i, (lab, sv, dv) in enumerate(BARS):
        y = 640 + i * 165; kr = appear(t, 0.3 + 0.25 * i, 0.4)
        hi = (i == 0 and t >= M[0] - 0.05) or (i > 0 and t >= M[1] - 0.05)
        if hi:
            col = (220, 252, 231) if i == 0 else (255, 237, 213)
            d.rounded_rectangle([80, y - 52, 1000, y + 72], radius=18, fill=col)
        text(d, (100, y + 10), lab, 40, INK, anchor="lm", alpha=kr)
        d.rectangle([BX0, y - 18, BX0 + sv * BPX * kr, y + 6], fill=A(ORANGE, kr))
        if dv > 0: d.rectangle([BX0, y + 18, BX0 + dv * BPX * kr, y + 42], fill=A(GREEN, kr))
        else: d.line([(BX0, y + 12), (BX0, y + 48)], fill=A(GREEN, kr), width=6)

# ---------------- canh 4: chua noi duoc gi ----------------
def s_gioihan(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.05, 0.35); y1 = 290
    card(d, (60, y1, 1020, y1 + 1150), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, y1 + 85), "Chưa nói được gì?", 54, NAVY, alpha=k)
    card(d, (110, y1 + 170, 970, y1 + 400), fill=A((239, 246, 255), k), r=24)
    ctext(d, y1 + 285, "Thước chỉ đo độ lớn d", 50, BLUE, alpha=k)
    yA = y1 + 640; xa, xb = 300, 780                                        # thuoc dat giua hai bang dinh
    d.rectangle([xa - 40, yA + 20, xb + 40, yA + 90], fill=A((254, 249, 195), k), outline=A((161, 98, 7), k), width=3)
    for j in range(0, 29):
        x = xa - 40 + j * (xb - xa + 80) / 28
        d.line([(x, yA + 20), (x, yA + (52 if j % 2 == 0 else 40))], fill=A((161, 98, 7), k), width=3)
    for x in (xa, xb):
        d.rectangle([x - 9, yA - 30, x + 9, yA + 30], fill=A(TAPE, k), outline=A((161, 98, 7), k))
    d.line([(xa, yA), (xb, yA)], fill=A(GREEN, k), width=8)
    ka = appear(t, 1.0)
    ctext(d, y1 + 880, "Hướng: đọc trên hình", 48, INK, alpha=ka)

# ---------------- canh 5: bay ----------------
BO, BSC = (560, 1180), 11
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    card(d, (60, 270, 1020, 620), fill=A(WHITE, a), outline=A(DRED, a), w=6)
    pw = tw(d, "Bẫy", F(40)) + 60
    card(d, (W / 2 - pw / 2, 300, W / 2 + pw / 2, 364), fill=A(DRED, a), r=32)
    text(d, (W / 2, 332), "Bẫy", 40, WHITE, alpha=a)
    q = "d = 30 + 40 = 70 cm"; lw = tw(d, q, F(54)); yy = 490
    text(d, (W / 2, yy), q, 54, DRED, alpha=a)
    ks = clamp((t - 0.9) / 0.4)
    if ks > 0: d.line([(W / 2 - lw / 2 - 10, yy + 2), (W / 2 - lw / 2 - 10 + (lw + 20) * ks, yy + 2)], fill=DRED, width=4)
    card(d, (60, 660, 1020, 1600), fill=WHITE, outline=GREEN, w=5)
    rail(d, 2, BO, BSC, w=22); thread(d, 2, BO, BSC, 1.0, w=6)
    tape(d, 2, BO, BSC, 0.0); tape(d, 2, BO, BSC, 1.0)
    p0, pc, p1 = S(BO, BSC, pt(2, 0)), S(BO, BSC, (-20, -15)), S(BO, BSC, pt(2, 1))
    text(d, (p0[0] - 30, (p0[1] + pc[1]) / 2), "30 cm", 40, BROWN, anchor="rm")
    text(d, ((pc[0] + p1[0]) / 2, pc[1] - 50), "40 cm", 40, BROWN)
    g = clamp((t - (M[1] - 0.3)) / 0.5)
    if g > 0:
        b = (lerp(p0[0], p1[0], g), lerp(p0[1], p1[1], g)); arrow(d, p0, b, GREEN, w=8, head=32)
    if g >= 1:
        text(d, ((p0[0] + p1[0]) / 2 + 40, (p0[1] + p1[1]) / 2 + 60), "d ≈ 50 cm", 44, DGREEN, anchor="lm")

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    def hint(d, t, k):
        ctext(d, 900, "Xe chạy 3/4 vòng tròn r = 10 cm.\nĐộ lớn d khoảng bao nhiêu?", 50, INK,
              maxw=900, alpha=appear(t, sc["M"][0] + 0.4, 0.5))
        kf = appear(t, sc["M"][0] + 0.6, 0.5)
        if kf > 0:
            O3, s3 = (540, 1083), 9.5
            pts = [S(O3, s3, pt(3, 0.75 * i / 90)) for i in range(91)]
            d.line(pts, fill=A(RAIL_D, kf), width=22, joint="curve"); d.line(pts, fill=A(RAIL, kf), width=14, joint="curve")
            tape(d, 3, O3, s3, 0.0, alpha=kf); tape(d, 3, O3, s3, 0.75, alpha=kf)
            for j in range(6):                                              # ban kinh net dut sang phai
                d.line([(O3[0] + j * 17, O3[1]), (O3[0] + j * 17 + 9, O3[1])], fill=A(NAVY, kf), width=4)
            dot(d, O3[0], O3[1], 6, A(NAVY, kf))
            text(d, (O3[0] + 140, O3[1]), "r = 10 cm", 40, NAVY, anchor="lm", alpha=kf)
        kh = appear(t, sc["M"][0] + 2.5, 0.5)
        if kh <= 0: return
        card(d, (110, 1230, 970, 1530), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=3)
        ctext(d, 1300, "Gợi ý", 44, INK, alpha=kh)
        ctext(d, 1420, "Nối điểm đầu với điểm cuối", 46, BROWN, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Độ lớn d không vượt quá s", "", body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, b, e = sc["hook"], sc["do"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + BADGE, "ding"), (b["t0"] + 0.9, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-dd-qd-01", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Độ dịch chuyển · thachlab.id.vn", scenes=[
 dict(key="hook", title="Xe chạy trên ray uốn", draw=s_hook, tail=0.5, caps=[
   ("Ray uốn nửa vòng tròn.", 3.0),
   ("Dừng video, tự đoán.", 6.5)]),
 dict(key="do", title="Bốn hình ray", draw=s_do, tail=0.4, caps=[
   ("Chỉ dọc ray đo s, thước đo d.", BADGE - 0.4),
   ("Nửa vòng: d bằng đường kính.", 3.2)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.4, caps=[
   ("Thẳng, không quay đầu: d = s.", 3.0),
   ("Cong hoặc quay về: d < s.", 3.0)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("Thước chưa cho biết hướng của d.", 4.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Cộng hai đoạn: đó là s.", 2.95),
   ("d nối thẳng đầu với cuối.", 2.95)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 6.0)]),
])
