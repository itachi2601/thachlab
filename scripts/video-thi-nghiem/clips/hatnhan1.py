# Clip: tn-l12-hatnhan-01 - Mo hinh "ban bi mu": tim vat chan khuat bang chum bi bi lech (28/10/2026; dung lai 26/11/2026
# theo KE-HOACH-CAI-TIEN-CLIP viec 4 lo 32: cong --do-chu, chu >= 56 px khi ve, <= 50 s, Du doan khong nut A-D (K10)).
# Du doan (hien_tuong_hay_sai: "bay thang = ben trong khong co gi" / tuong lech deu): bi ra huong nao? -> da so thang, vai luot lech manh.
# Cau THU NGHI (= cau_chot khung web): dinh 4 mm, noi vung lan 20 -> 40 cm -> ti le lech giam con mot nua
#   (so_lieu_mau: 4 luot -> 2 luot / 60). Buoc suy luan chua chieu: dai bi chan giu nguyen, vung lan rong gap doi.
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-hatnhan-01.json:
#   tham_so: d_bia = 2 mm (mac dinh), d_bi = 10 mm, b = 20 cm, N = 60 luot
#   so_lieu_mau: dinh 2 mm, b 20 cm, 60 luot -> 3 luot lech manh, ti le 0,05 ; dinh 6 mm -> 6 luot ;
#                dinh 4 mm: b 20 cm -> 4 luot, b 40 cm -> 2 luot (chi dung trong cau hoi chot, khong lo ket qua)
#   57 = 60 - 3 (so luot di thang). ghi_chu: "dao dong them bot 2 luot".
# Hinh: nhin tu tren xuong, ty le that 2,6 px/mm (vung lan 200 mm). Bi va dinh = va cham cung: bi dung lai o vi tri
#   tiep xuc (tam cach tam dinh (d_bia + d_bi)/2 = 6 mm), van toc phan xa qua phap tuyen (goc toi = goc phan xa).
# Canh: Du doan -> Tien hanh (60 luot, 3 luot dau cham, con lai tua nhanh) -> Dap an C + keo dai vet lech + nhac tam che
#       -> Bay (ti le lech khong phu thuoc co dinh) + chua noi duoc -> Chot + cau hoi tu nho lai.
from engine import *

# ---------------- bo cuc (khung 1080x1920) ----------------
TBL = (50, 290, 1030, 1010)            # mat ban
S = 2.6                                # px / mm
LY0, B_MM = 390, 200                   # mep tren vung lan, be rong vung lan (mm)
COV = (300, 365, 780, 935)             # tam che (phu het be rong vung lan)
NX, YN = 560, 65                       # vi tri dinh: x (px), y trong vung lan (mm)
NY = LY0 + YN * S
RB, RN = 5 * S, 1 * S                  # ban kinh bi 10 mm / dinh 2 mm (px)
RC = RB + RN                           # khoang cach tam khi tiep xuc = 6 mm
XS = 150                               # bi bat dau lan
WOOD = (238, 224, 200); CARD = (205, 188, 160); STEEL = (112, 122, 142)

def yl(mm): return LY0 + mm * S

# ---------------- 60 luot lan ----------------
HITS = {1: 5.54, 22: -3.0, 46: 1.5}     # luot (0-based) -> do lech tam p (mm) so voi dinh; 3 luot = so_lieu_mau
def _lanes():
    R = random.Random(14); out = []
    for k in range(60):
        if k in HITS: out.append(YN + HITS[k]); continue
        while True:
            y = R.uniform(6, 194)
            if abs(y - YN) > 7.5: break
        out.append(y)
    return out

def _exit(p, v, box):
    """Tham so t > 0 khi tia p + t.v roi khoi hinh chu nhat box."""
    ts = []
    for i, (lo, hi) in enumerate(((box[0], box[2]), (box[1], box[3]))):
        if v[i] > 1e-9: ts.append((hi - p[i]) / v[i])
        elif v[i] < -1e-9: ts.append((lo - p[i]) / v[i])
    return min(ts)

def _run(y_mm, hit):
    y = yl(y_mm); P0 = (XS, y)
    if not hit:
        pts = [P0, (TBL[2] - 8, y)]
        vis = [(0, COV[0] - XS), (COV[2] - XS, TBL[2] - 8 - XS)]
        return dict(pts=pts, vis=vis, hit=False)
    pp = (y_mm - YN) * S
    dx = math.sqrt(RC * RC - pp * pp)
    C = (NX - dx, y)                                   # tam bi luc tiep xuc dinh
    nx, ny = -dx / RC, pp / RC                         # phap tuyen tai diem tiep xuc
    v = (1 - 2 * nx * nx, -2 * nx * ny)                # phan xa: v' = v - 2(v.n)n, v = (1, 0)
    tE = _exit(C, v, COV); E = (C[0] + tE * v[0], C[1] + tE * v[1])
    tT = _exit(C, v, (132, TBL[1] + 8, TBL[2] - 8, TBL[3] - 8)); Z = (C[0] + tT * v[0], C[1] + tT * v[1])
    L1 = C[0] - XS
    vis = [(0, COV[0] - XS), (L1 + tE, L1 + tT)]
    ang = math.degrees(math.atan2(v[1], v[0]))
    return dict(pts=[P0, C, Z], vis=vis, hit=True, C=C, E=E, v=v, ang=abs(ang))

LANES = _lanes()
RUNS = [_run(y, k in HITS) for k, y in enumerate(LANES)]

def _len(pts): return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
def _at(pts, s):
    for a, b in zip(pts, pts[1:]):
        L = math.dist(a, b)
        if s <= L: k = s / L if L else 0; return (lerp(a[0], b[0], k), lerp(a[1], b[1], k))
        s -= L
    return pts[-1]
for r in RUNS: r["L"] = _len(r["pts"])

# ---------------- hinh ve ----------------
def chevron(d, x, y, ang, color, s=14, w=4):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=color, width=w)

def dashed(d, p, q, color, w=4, seg=12, gap=9):
    L = math.dist(p, q); s = 0.0
    while s < L:
        e = min(L, s + seg); a, b = s / L, e / L
        d.line([(lerp(p[0], q[0], a), lerp(p[1], q[1], a)), (lerp(p[0], q[0], b), lerp(p[1], q[1], b))], fill=color, width=w)
        s += seg + gap

def trace(d, r, upto, color, w):
    pts = r["pts"]
    for a, b in r["vis"]:
        if upto <= a: continue
        d.line([_at(pts, a), _at(pts, min(b, upto))], fill=color, width=w)
    if r["hit"] and upto >= r["vis"][1][1] - 1:          # mui ten o dau ra
        Z = pts[-1]; v = r["v"]
        chevron(d, Z[0], Z[1], math.atan2(v[1], v[0]), color, s=26, w=w + 1)

def ball(d, x, y, alpha=1.0):
    d.ellipse([x - RB, y - RB, x + RB, y + RB], fill=A(STEEL, alpha), outline=A(NAVY, alpha), width=2)
    d.ellipse([x - RB * 0.55, y - RB * 0.6, x - RB * 0.1, y - RB * 0.15], fill=A(WHITE, 0.7 * alpha))

def inside_cover(x, y, m=0): return COV[0] - m < x < COV[2] + m and COV[1] - m < y < COV[3] + m

DORANGE = (154, 52, 18); DRED = (185, 28, 28); GOLD = (234, 179, 8)

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-hatnhan-01.json")))
    h = k["so_lieu_mau"]["hang"]
    assert h[0] == [2, 20, 60, 3, 0.05] and h[4][:4] == [6, 20, 60, 6] and h[2][:4] == [4, 20, 60, 4] and h[3][:4] == [4, 40, 60, 2]
    z = {p["ky_hieu"]: p for p in k["tham_so"]}; assert z["d_bi"]["gia_tri"] == 10 and z["d_bia"]["mac_dinh"] == 2
_kiem_so()

def pill(d, cx, cy, s, fill, alpha=1.0, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 38, cx + pw / 2, cy + 38), fill=A(fill, alpha), r=36)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem LIEN cao 70 px, ngan dan theo 10 nac (moi nac doi hinh du ro cho cong --do-chu)."""
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (190, y, 890, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (190, y, 190 + max(70, 700 * q), y + 70), fill=A(col, a), r=35)

def table(d):
    card(d, TBL, fill=WOOD, outline=LIGHT, r=28, w=3)
    x = 96                                              # kich thuoc vung lan b = 20 cm
    d.line([(x, yl(0)), (x, yl(B_MM))], fill=NAVY, width=3)
    for yy, s in ((yl(0), -1), (yl(B_MM), 1)):
        chevron(d, x, yy, s * math.pi / 2, NAVY, s=14, w=3)
        d.line([(x - 14, yy), (x + 14, yy)], fill=NAVY, width=3)
    ym = yl(40)
    card(d, (x - 46, ym - 70, x + 46, ym + 70), fill=WHITE, r=16)
    text(d, (x, ym - 30), "20", 56, INK)
    text(d, (x, ym + 30), "cm", 56, INK)

def cover(d, alpha=1.0, mark=False):
    if alpha <= 0.02: return
    card(d, COV, fill=A(CARD, alpha), outline=A(mix(CARD, NAVY, 0.4), alpha), r=18, w=4)
    if alpha > 0.95: text(d, ((COV[0] + COV[2]) / 2, COV[1] + 50), "tấm che", 56, mix(NAVY, CARD, 0.1), alpha=alpha)
    if mark:
        text(d, ((COV[0] + COV[2]) / 2, (COV[1] + COV[3]) / 2 - 30), "?", 160, WHITE, alpha=alpha)

def ring6(d, alpha):                   # vong ban kinh 6 mm = noi tam bi nam khi cham dinh
    if alpha <= 0.02: return
    d.ellipse([NX - RC, NY - RC, NX + RC, NY + RC], outline=A(ORANGE, alpha), width=3)

def nail(d, alpha=1.0):
    if alpha <= 0.02: return
    d.ellipse([NX - RN - 1, NY - RN - 1, NX + RN + 1, NY + RN + 1], fill=A(NAVY, alpha))


# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    table(d); cover(d, 1.0, mark=True)
    bx = XS + 40 * ease((t - 0.3) / 1.2)
    ball(d, bx, yl(150))
    arrow(d, (bx + RB + 10, yl(150)), (bx + RB + 90, yl(150)), NAVY, w=5, head=18)
    text(d, (70, 965), "bi 10 mm", 56, NAVY, anchor="lm")
    M = sc["M"]; a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1040 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 520), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    seg_bar(d, y0 + 140, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, a)
    text(d, (W / 2, y0 + 320), "Bi lăn 60 lượt qua tấm che.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 425), "Hướng bi đi ra thế nào?", 60, PURPLE, alpha=a)

# ---------------- canh 2: Tien hanh ----------------
SLOW, FAST_D = 1.15, 0.38              # 3 luot dau cham; con lai moi luot 0,38 s, xuat phat cach nhau deu
def schedule(sc):
    t0 = 0.6; fs = t0 + 3 * SLOW; fe = sc["T"] - 0.5 - FAST_D
    st = [t0 + k * SLOW for k in range(3)] + [fs + (k - 3) * (fe - fs) / 56 for k in range(3, 60)]
    du = [SLOW * 0.95] * 3 + [FAST_D] * 57
    return st, du

def hit_time(r, st, du):               # luc bi lech chui ra khoi tam che
    return st + du * r["vis"][1][0] / r["L"]

def table_runs(d, t, sc, live=True):
    st, du = schedule(sc); n_done = 0; n_hit = 0
    for k, r in enumerate(RUNS):
        if t < st[k]: continue
        s = clamp((t - st[k]) / du[k]) * r["L"]
        red = r["hit"] and t >= hit_time(r, st[k], du[k])           # do chi khi luot do da lech ra khoi tam che
        col = A(RED, 0.95) if red else A((95, 92, 100), 0.45)
        trace(d, r, s, col, 6 if red else 3)
        if s >= r["L"] - 0.5: n_done += 1
        if r["hit"] and t >= hit_time(r, st[k], du[k]): n_hit += 1
        if live and s < r["L"] - 0.5:
            x, y = _at(r["pts"], s)
            if not inside_cover(x, y, RB - 2): ball(d, x, y)
    return n_done, n_hit

def ff_icon(d, cx, cy, col):
    for dx in (-26, 18):
        d.polygon([(cx + dx - 22, cy - 28), (cx + dx + 22, cy), (cx + dx - 22, cy + 28)], fill=col)

def s_do(img, d, t, sc):
    table(d)
    n, m = table_runs(d, t, sc)
    cover(d)
    st, du = schedule(sc)
    if st[3] - 0.05 < t and n < 60:
        card(d, (900, 302, 1018, 374), fill=WHITE, r=20); ff_icon(d, 959, 338, ORANGE)
    card(d, (50, 1040, 1030, 1250), fill=WHITE, outline=LIGHT, w=3)
    text(d, (290, 1090), "Đã lăn", 56, INK)
    text(d, (790, 1090), "Lệch mạnh", 56, INK)
    text(d, (290, 1185), f"{n}/60", 76, INK)
    text(d, (790, 1185), str(m), 76, RED if m else INK)
    d.line([(540, 1065), (540, 1225)], fill=LIGHT, width=3)
    card(d, (50, 1280, 1030, 1500), fill=WHITE, outline=LIGHT, w=3)
    d.line([(110, 1345), (250, 1345)], fill=A((95, 92, 100), 0.6), width=5)
    text(d, (290, 1345), "đi thẳng (xám)", 56, INK, anchor="lm")
    d.line([(110, 1435), (250, 1435)], fill=RED, width=7); chevron(d, 250, 1435, 0, RED, s=18, w=6)
    text(d, (290, 1435), "lệch mạnh (đỏ)", 56, INK, anchor="lm")

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]; table(d)
    table_runs(d, 99, SC["do"], live=False)
    kc = appear(t, M[1] + 0.2, 0.8)                # nhac tam che + keo dai vet lech vao trong
    cover(d, 1 - 0.8 * kc)
    if kc > 0:
        for r in RUNS:
            if not r["hit"]: continue
            C, E = r["C"], r["E"]
            d.line([(COV[0], C[1]), C, E], fill=A(RED, kc), width=6)
            d.ellipse([C[0] - RB, C[1] - RB, C[0] + RB, C[1] + RB], outline=A(STEEL, kc), width=3)
        ring6(d, kc); nail(d, kc)
        ZC, ZR, Z = (905, 660), 105, 4.5                    # o phong to x4,5: dinh 2 mm va vong 6 mm (noi tam bi khi cham)
        d.line([(NX + 8, NY), (ZC[0] - ZR, ZC[1])], fill=A(NAVY, kc), width=3)
        d.ellipse([ZC[0] - ZR, ZC[1] - ZR, ZC[0] + ZR, ZC[1] + ZR], fill=A(WHITE, kc), outline=A(NAVY, kc), width=4)
        d.ellipse([ZC[0] - RC * Z, ZC[1] - RC * Z, ZC[0] + RC * Z, ZC[1] + RC * Z], outline=A(ORANGE, kc), width=5)
        d.ellipse([ZC[0] - RN * Z, ZC[1] - RN * Z, ZC[0] + RN * Z, ZC[1] + RN * Z], fill=A(NAVY, kc))
        text(d, (905, 510), "đinh 2 mm", 56, NAVY, alpha=kc)
    ka = appear(t, 0.3, 0.5)
    pill(d, W / 2, 1090, "ĐÁP ÁN: đa số đi thẳng", NAVY, ka)
    card(d, (50, 1170, 1030, 1400), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=3)
    for x, lab, val, col in ((210, "thẳng", "57", INK), (540, "lệch", "3", RED), (870, "tỉ lệ", "0,05", INK)):
        text(d, (x, 1225), lab, 56, INK, alpha=ka)
        text(d, (x, 1320), val, 76, col, alpha=ka)
    for x in (375, 705): d.line([(x, 1195), (x, 1375)], fill=A(LIGHT, ka), width=3)

# ---------------- canh 4: Rut ra (bi -> alpha) ----------------
def panel_bi(d, box, a):
    x0, y0, x1, y1 = box; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    card(d, box, fill=A(WOOD, a), outline=A(LIGHT, a), r=24, w=3)
    for yy in (y0 + 60, y0 + 120, y1 - 120, y1 - 60): d.line([(x0 + 30, yy), (x1 - 30, yy)], fill=A((95, 92, 100), 0.45 * a), width=4)
    d.line([(x0 + 30, cy - 6), (cx - 20, cy - 6), (x0 + 120, y0 + 40)], fill=A(RED, a), width=6)
    dot(d, cx, cy, 18, A(NAVY, a))

def panel_au(d, box, a):
    x0, y0, x1, y1 = box; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    card(d, box, fill=A((255, 244, 204), a), outline=A(GOLD, a), r=24, w=3)
    for yy in (y0 + 60, y0 + 120, y1 - 120, y1 - 60): d.line([(x0 + 30, yy), (x1 - 30, yy)], fill=A((95, 92, 100), 0.45 * a), width=4)
    P0, C, P2 = (x0 + 30, cy - 10), (cx + 30, cy - 10), (x0 + 40, cy - 110)     # quay dau truoc hat nhan, khong cham
    pts = [((1 - u) ** 2 * P0[0] + 2 * u * (1 - u) * C[0] + u * u * P2[0], (1 - u) ** 2 * P0[1] + 2 * u * (1 - u) * C[1] + u * u * P2[1])
           for u in [i / 40 for i in range(41)]]
    d.line(pts, fill=A(ORANGE, a), width=8, joint="curve")
    dot(d, cx, cy, 18, A(RED, a))

def s_rutra(img, d, t, sc):
    M = sc["M"]; k1 = appear(t, 0.3, 0.5); k2 = appear(t, M[1] + 0.2, 0.5)
    panel_bi(d, (50, 290, 520, 1040), k1)
    if k2 > 0: panel_au(d, (560, 290, 1030, 1040), k2)
    for j, (l, r, cl, cr) in enumerate((("đinh", "hạt nhân", NAVY, DRED), ("bi", "alpha", NAVY, DORANGE))):
        y = 1140 + j * 130
        text(d, (285, y), l, 62, cl, alpha=k1)
        if k2 > 0:
            arrow(d, (420, y), (640, y), A(INK, k2), w=8, head=26)
            text(d, (830, y), r, 62, cr, alpha=k2)

# ---------------- canh 5: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; k1 = appear(t, 0.3, 0.45)
    card(d, (40, 270, 1040, 1070), fill=A(WHITE, k1), outline=A(RED, k1), w=6)
    pill(d, W / 2, 345, "BẪY", RED, k1)
    text(d, (W / 2, 460), "“Cỡ đinh không ảnh hưởng”?", 60, INK, alpha=k1)
    text(d, (W / 2, 570), "lượt lệch / 60", 56, INK, alpha=k1)
    for j, (lab, n) in enumerate((("2 mm", 3), ("6 mm", 6))):
        yy = 680 + j * 130
        text(d, (80, yy), lab, 64, NAVY, anchor="lm", alpha=k1)
        for i in range(n):
            ki = k1 * appear(t, (0.6 + 0.3 * i) if j == 0 else (1.8 + 0.5 * i), 0.25)
            dot(d, 330 + i * 115, yy, 42, A(RED, ki))
    kv = appear(t, M[1] + 0.2, 0.4)
    if kv > 0:
        card(d, (340, 935, 740, 1045), fill=A((254, 226, 226), kv), outline=A(RED, kv), r=30, w=5)
        text(d, (W / 2, 990), "SAI", 72, RED, alpha=kv)
    k3 = appear(t, M[2] + 0.2, 0.45)
    if k3 > 0:
        card(d, (40, 1110, 1040, 1500), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, 1185), "Alpha bị đẩy từ xa", 62, NAVY, alpha=k3)
        hx, hy = 700, 1390                                   # hat nhan; alpha quay dau truoc khi cham
        P0, C, P2 = (120, hy), (1080, hy + 6), (160, 1250)
        pts = [((1 - u) ** 2 * P0[0] + 2 * u * (1 - u) * C[0] + u * u * P2[0],
                (1 - u) ** 2 * P0[1] + 2 * u * (1 - u) * C[1] + u * u * P2[1]) for u in [i / 40 for i in range(41)]]
        d.line(pts, fill=A(ORANGE, k3), width=8, joint="curve")
        arrow(d, pts[-4], P2, A(ORANGE, k3), w=8, head=24)
        dot(d, hx, hy, 20, A(RED, k3))

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def lane(d, cx, yc, w_cm, a):
    """Vung lan nhin tu tren: be rong theo ti le 20 cm = 280 px; dinh 4 mm o giua (cham)."""
    h = 280 * w_cm / 20
    card(d, (cx - 170, yc - h / 2, cx + 170, yc + h / 2), fill=A(WOOD, a), outline=A(LIGHT, a), r=16, w=3)
    dot(d, cx, yc, 15, A(NAVY, a))
    text(d, (cx, yc + 70), "đinh 4 mm", 56, NAVY, alpha=a)
    text(d, (cx, 1450), f"{w_cm} cm", 60, NAVY, alpha=a)

def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 260, 1040, 1530), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 340, "THỬ NGHĨ", ORANGE, k1)
    seg_bar(d, 420, t, 0.8, sc["T"] - 0.2, ORANGE, k1)
    text(d, (W / 2, 570), "Nới vùng lăn 20 → 40 cm:", 60, INK, alpha=k1)
    text(d, (W / 2, 665), "tỉ lệ lệch ra sao?", 60, DORANGE, alpha=k1)
    lane(d, 290, 1050, 20, k1); lane(d, 790, 1050, 40, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    st, du = schedule(do)
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    for k, r in enumerate(RUNS):
        if r["hit"]: out.append((do["t0"] + hit_time(r, st[k], du[k]), "tap"))
        elif k >= 3 and k % 3 == 0: out.append((do["t0"] + st[k], "tick"))
    out += [(da["t0"] + 0.3, "ding"), (b["t0"] + 0.3, "buzz"), (e["t0"] + 0.15, "open")]
    return sorted(out)

SCENES = [
 dict(key="hook", title="Tìm vật bị che khuất", draw=s_hook, tail=0.3, caps=[
   ("Có gì dưới tấm che?", 3.0),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Mỗi lượt: ghi hướng vào, ra.", 3.4),
   ("Tua nhanh đủ 60 lượt.", 5.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.2, caps=[
   ("Chỉ vài lượt lệch mạnh.", 3.2),
   ("Nhấc tấm che: một chiếc đinh.", 3.4)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.2, caps=[
   ("Chỉ 3/60 lệch: vật rất hẹp.", 3.6),
   ("Lá vàng: alpha cũng vậy.", 2.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.1, caps=[
   ("Đúng hay sai?", 2.8),
   ("Đinh to: dễ bị trúng hơn.", 2.9),
   ("Bi chạm đinh, alpha thì không.", 2.9)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=2.8, caps=[
   ("Bi lệch mạnh: có vật nhỏ, cứng.", 3.6)]),
]
SC = {s["key"]: s for s in SCENES}

CLIP = dict(id="tn-l12-hatnhan-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Hạt nhân và mô hình nguyên tử · thachlab.id.vn",
            cues=_cues, scenes=SCENES)
