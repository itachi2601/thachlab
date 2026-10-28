# Clip: tn-l12-hatnhan-01 - Mo hinh "ban bi mu": tim vat chan khuat bang chum bi bi lech (28/10/2026)
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

def table(d):
    card(d, TBL, fill=WOOD, outline=LIGHT, r=28, w=3)
    # kich thuoc vung lan b = 20 cm
    x = 86
    d.line([(x, yl(0)), (x, yl(B_MM))], fill=NAVY, width=3)
    for yy, s in ((yl(0), -1), (yl(B_MM), 1)):
        chevron(d, x, yy, s * math.pi / 2, NAVY, s=14, w=3)
        d.line([(x - 14, yy), (x + 14, yy)], fill=NAVY, width=3)
    ym = yl(40)                                         # tranh nhan "bi 10 mm" (hook) va tia 3 (y 698-791)
    card(d, (x - 36, ym - 60, x + 36, ym + 60), fill=WHITE, r=16)
    text(d, (x, ym - 22), "20", 34, INK)
    text(d, (x, ym + 22), "cm", 34, INK, bold=False)

def cover(d, alpha=1.0, mark=False):
    if alpha <= 0.02: return
    card(d, COV, fill=A(CARD, alpha), outline=A(mix(CARD, NAVY, 0.4), alpha), r=18, w=4)
    text(d, ((COV[0] + COV[2]) / 2, COV[3] - 36), "tấm che", 36, mix(NAVY, CARD, 0.2), bold=False, alpha=alpha)
    if mark:
        text(d, ((COV[0] + COV[2]) / 2, (COV[1] + COV[3]) / 2 - 10), "?", 150, WHITE, alpha=alpha)
        text(d, ((COV[0] + COV[2]) / 2, (COV[1] + COV[3]) / 2 + 110), "đinh 2 mm ở đâu đó", 34, NAVY, alpha=alpha)

def ring6(d, alpha):                   # vong ban kinh 6 mm = noi tam bi nam khi cham dinh
    if alpha <= 0.02: return
    d.ellipse([NX - RC, NY - RC, NX + RC, NY + RC], outline=A(ORANGE, alpha), width=3)

def nail(d, alpha=1.0):
    if alpha <= 0.02: return
    d.ellipse([NX - RN - 1, NY - RN - 1, NX + RN + 1, NY + RN + 1], fill=A(NAVY, alpha))

# ---------------- canh 1: Du doan ----------------
OPTS = ("Lượt nào cũng lệch đi một chút", "Khoảng một nửa số lượt bị lệch",
        "Đa số đi thẳng, vài lượt lệch mạnh", "Không lượt nào lệch vì đinh nhỏ")

def s_hook(img, d, t, sc):
    table(d); cover(d, 1.0, mark=True)
    bx = XS + 40 * ease((t - 0.3) / 1.2)
    ball(d, bx, yl(150))
    arrow(d, (bx + RB + 10, yl(150)), (bx + RB + 90, yl(150)), NAVY, w=5, head=18)
    text(d, (bx, yl(150) + 46), "bi 10 mm", 34, NAVY, bold=False)
    M = sc["M"]; a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 590), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 86), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 55), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    text(d, (W / 2, y0 + 136), "Lăn 60 lượt bi qua vùng có tấm che.", 40, INK, alpha=a)
    text(d, (W / 2, y0 + 188), "Hướng bi đi ra sẽ thế nào?", 40, INK, alpha=a)
    for j, s in enumerate(OPTS):
        k = appear(t, M[1] + 0.15 * j, 0.4); yy = y0 + 264 + j * 76
        d.rounded_rectangle([90, yy - 30, 990, yy + 30], radius=30, outline=A(LIGHT, k), width=3)
        text(d, (120, yy), f"{'ABCD'[j]}.  {s}", 36, NAVY, bold=False, anchor="lm", alpha=k)
    tc, tend = M[1] + 0.8, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 560, 940, y0 + 572], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 560, 140 + 800 * (1 - p), y0 + 572], radius=6, fill=A(PURPLE, a))

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
        col = A(RED, 0.95) if r["hit"] else A((95, 92, 100), 0.45)
        trace(d, r, s, col, 5 if r["hit"] else 3)
        if s >= r["L"] - 0.5: n_done += 1
        if r["hit"] and t >= hit_time(r, st[k], du[k]): n_hit += 1
        if live and s < r["L"] - 0.5:
            x, y = _at(r["pts"], s)
            if not inside_cover(x, y, RB - 2): ball(d, x, y)
    return n_done, n_hit

def counter(d, n, m, fast):
    card(d, (50, 1040, 1030, 1250), fill=WHITE, outline=LIGHT, w=3)
    text(d, (290, 1090), "Số lượt đã lăn", 36, MUTED, bold=False)
    text(d, (790, 1090), "Số lượt lệch mạnh", 36, MUTED, bold=False)
    text(d, (290, 1175), f"{n}/60", 72, INK)
    text(d, (790, 1175), str(m), 72, RED if m else INK)
    d.line([(540, 1070), (540, 1220)], fill=LIGHT, width=3)
    if fast:
        wdt = tw(d, "TUA NHANH", F(34)) + 44
        card(d, (1030 - wdt, 1260, 1030, 1310), fill=ORANGE, r=25); text(d, (1030 - wdt / 2, 1285), "TUA NHANH", 34, WHITE)

def s_do(img, d, t, sc):
    table(d)
    n, m = table_runs(d, t, sc)
    cover(d)
    st, du = schedule(sc)
    counter(d, n, m, t > st[3] - 0.05 and n < 60)
    k = appear(t, 0.5, 0.4)
    card(d, (50, 1330, 1030, 1590), fill=A(WHITE, k), outline=A(LIGHT, k), w=3)
    text(d, (100, 1395), "Ghi lại mỗi lượt:", 36, INK, anchor="lm", alpha=k)
    d.line([(110, 1470), (230, 1470)], fill=A((95, 92, 100), 0.6 * k), width=4)
    text(d, (260, 1470), "lăn thẳng qua (xám)", 38, INK, bold=False, anchor="lm", alpha=k)
    d.line([(110, 1540), (230, 1540)], fill=A(RED, k), width=6); chevron(d, 230, 1540, 0, A(RED, k), s=16, w=5)
    text(d, (260, 1540), "lệch mạnh, khác hướng trên 15° (đỏ)", 36, INK, bold=False, anchor="lm", alpha=k)

# ---------------- canh 3: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]; table(d)
    sc_do = SC["do"]
    table_runs(d, 99, sc_do, live=False)
    kx = appear(t, M[1] + 0.1, 0.6)                # keo dai vet lech vao trong
    kc = appear(t, M[2] + 0.1, 0.7)                # nhac tam che
    cover(d, 1 - 0.75 * kc)
    if kx > 0:
        for r in RUNS:
            if not r["hit"]: continue
            C, E = r["C"], r["E"]; P = (COV[0], C[1])
            c = A(ORANGE, kx * (1 - kc))
            dashed(d, P, (lerp(P[0], C[0], kx), C[1]), c, w=3, seg=10, gap=8)
            dashed(d, E, (lerp(E[0], C[0], kx), lerp(E[1], C[1], kx)), c, w=4)
        ka6 = appear(t, M[1] + 0.7, 0.4)
        ring6(d, ka6)
        text(d, (NX + 30, NY - 82), "tâm bi khi", 34, NAVY, anchor="lm", alpha=ka6)          # goc tren-phai tam che: trong
        text(d, (NX + 30, NY - 40), "chạm đinh", 34, NAVY, anchor="lm", alpha=ka6)
        d.line([(NX + 24, NY - 30), (NX + RC * 0.75, NY - RC * 0.75)], fill=A(NAVY, ka6), width=3)
    for j, r in enumerate([r for r in RUNS if r["hit"]]):      # danh so 3 tia ra
        Z, v = r["pts"][-1], r["v"]; bx, by = Z[0] - 62 * v[0], Z[1] - 62 * v[1]
        sg = -1 if v[0] < -0.9 else 1                           # tia bat nguoc: so nam phia xa duong vao
        bx += sg * 28 * -v[1]; by += sg * 28 * v[0]
        ko = appear(t, M[0] + 0.3, 0.4)
        dot(d, bx, by, 21, A(RED, ko)); text(d, (bx, by), str(j + 1), 32, WHITE, alpha=ko)
    if kc > 0:
        for r in RUNS:
            if not r["hit"]: continue
            C, E = r["C"], r["E"]
            d.line([(COV[0], C[1]), C, E], fill=A(RED, kc), width=5)
            d.ellipse([C[0] - RB, C[1] - RB, C[0] + RB, C[1] + RB], outline=A(STEEL, kc), width=3)
        ring6(d, 1.0); nail(d, kc)
        text(d, (NX + 30, NY - 150), "đinh 2 mm", 34, NAVY, anchor="lm", alpha=kc)
        d.line([(NX + 22, NY - 148), (NX + 2, NY - 6)], fill=A(NAVY, kc), width=3)
    ka = appear(t, M[0] + 0.1, 0.5)
    pw = tw(d, "ĐÁP ÁN C", F(36)) + 52
    card(d, (1012 - pw, 302, 1012, 360), fill=A(NAVY, ka), r=29)
    text(d, (1012 - pw / 2, 331), "ĐÁP ÁN C", 36, WHITE, alpha=ka)
    # so lieu
    card(d, (50, 1040, 1030, 1220), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=3)
    for x, lab, val, col in ((210, "Đi thẳng", "57", INK), (540, "Lệch mạnh", "3", RED), (870, "Tỉ lệ lệch", "0,05", INK)):
        text(d, (x, 1085), lab, 34, MUTED, bold=False, alpha=ka)
        text(d, (x, 1160), val, 64, col, alpha=ka)
    for x in (375, 705): d.line([(x, 1070), (x, 1190)], fill=A(LIGHT, ka), width=3)
    # rut ra
    k1 = appear(t, M[2] + 0.4, 0.5); k2 = appear(t, M[3] + 0.1, 0.5)
    card(d, (50, 1245, 1030, 1600), fill=A(WHITE, k1), outline=A(GREEN, k1), w=5)
    text(d, (W / 2, 1292), "Rút ra", 38, GREEN, alpha=k1)
    lines = (("• Bi lệch mạnh → có vật nhỏ, cứng chắn đường.", k1),
             ("• 3/60 lượt lệch → vật chắn chỉ chắn", k1), ("   một phần nhỏ bề rộng vùng lăn.", k1),
             ("• Lá vàng: alpha bật ngược → hạt nhân", k2), ("   rất nhỏ, rất nặng, mang điện dương.", k2))
    for j, (s, kk) in enumerate(lines):
        text(d, (80, 1352 + j * 52), s, 36, INK, bold=False, anchor="lm", alpha=kk)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, 0.3, 0.45)
    y0 = 255 + (1 - k1) * 30
    card(d, (40, y0, 1040, y0 + 640), fill=A(WHITE, k1), outline=A(RED, k1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 88), fill=A(RED, k1), r=32)
    text(d, (W / 2, y0 + 56), "BẪY", 38, WHITE, alpha=k1)
    q = "“Tỉ lệ lệch không phụ thuộc cỡ đinh”"
    ks = clamp((t - 1.2) / 0.4)
    lw = tw(d, q, F(40)); yy = y0 + 150
    text(d, (W / 2, yy), q, 40, mix(INK, GRAY, ks), alpha=k1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.8 * k1), width=4)
    text(d, (W / 2, y0 + 235), "Cùng 60 lượt, vùng lăn 20 cm:", 38, INK, alpha=k1)
    for j, (lab, n) in enumerate((("đinh 2 mm", 3), ("đinh 6 mm", 6))):
        yy = y0 + 325 + j * 95
        text(d, (80, yy), lab, 38, INK, anchor="lm", alpha=k1)
        d.rounded_rectangle([290, yy - 26, 770, yy + 26], radius=26, fill=A(LIGHT, k1))
        d.rounded_rectangle([290, yy - 26, 290 + 480 * n / 6 * ease((t - 0.4) / 0.7), yy + 26], radius=26, fill=A(RED, k1))
        text(d, (800, yy), f"{n}/60 lượt", 38, RED, anchor="lm", alpha=k1)
    ctext(d, y0 + 560, "Sai: đinh to hơn chắn dải rộng hơn → tỉ lệ lệch lớn hơn.", 40, RED, maxw=900, alpha=appear(t, 1.6, 0.5))
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        y0 = 925 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 500), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 58), "Thí nghiệm chưa nói được", 42, NAVY, alpha=k2)
        ka = k2 * appear(t, M[1] + 0.3, 0.4); kb = k2 * appear(t, M[2] + 0.1, 0.4)
        text(d, (80, y0 + 145), "• Mô hình bi chỉ lệch khi chạm cứng vào đinh;", 38, INK, bold=False, anchor="lm", alpha=ka)
        text(d, (80, y0 + 199), "  hạt alpha không chạm hạt nhân, mà lệch do", 38, INK, bold=False, anchor="lm", alpha=ka)
        text(d, (W / 2, y0 + 290), "LỰC ĐIỆN ĐẨY", 56, PURPLE, alpha=kb)
        text(d, (W / 2, y0 + 370), "của hạt nhân mang điện dương.", 40, INK, alpha=kb)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def _hint(d, t, k):                    # goi y tu ve, hien sau ~2,8 s (khong lo tang/giam)
    sc = SC["end"]; kh = appear(t, sc["M"][0] + 2.8, 0.5)
    if kh <= 0: return
    card(d, (110, 1290, 970, 1560), fill=A((255, 237, 213), kh), outline=A(ORANGE, kh), r=24, w=4)
    ctext(d, 1345, "Gợi ý", 38, ORANGE, alpha=kh)
    ctext(d, 1450, "Đinh chắn một dải hẹp cố định. Dải đó chiếm bao nhiêu phần bề rộng vùng lăn?", 40, INK, maxw=800, alpha=kh)

def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Bi lệch mạnh chỉ ra một vật nhỏ, cứng nằm khuất",
             "Giữ nguyên chiếc đinh, nới vùng lăn từ 20 cm lên 40 cm. Tỉ lệ lượt lệch tăng hay giảm? Vì sao?",
             None, body=_hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    st, du = schedule(do)
    out = [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.3, "ding")]
    for k, r in enumerate(RUNS):
        if r["hit"]: out.append((do["t0"] + hit_time(r, st[k], du[k]), "tap"))
        elif k >= 3 and k % 3 == 0: out.append((do["t0"] + st[k], "tick"))
    out += [(da["t0"] + da["M"][0] + 0.1, "ding"), (b["t0"] + 0.3, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return sorted(out)

SCENES = [
 dict(key="hook", title="Tìm vật bị che khuất", draw=s_hook, tail=0.6, caps=[
   ("Một chiếc đinh 2 mm giấu dưới tấm che.", 2.8),
   ("Lăn 60 lượt bi qua: bi ra sao?", 2.8),
   ("Dừng lại, chọn A, B, C hay D.", 4.1)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Bi lăn vào, lọt dưới tấm che.", 2.8),
   ("Chỉ ghi hướng bi vào và hướng bi ra.", 2.8),
   ("Tua nhanh cho đủ 60 lượt.", 2.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("57 lượt thẳng, 3 lượt lệch: đáp án C.", 2.9),
   ("Kéo dài 3 vệt lệch: dồn về một chỗ.", 2.8),
   ("Nhấc tấm che: chiếc đinh nằm đúng đó.", 2.8),
   ("Lá vàng tương tự: alpha chỉ ra hạt nhân.", 3.1)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Bẫy: tỉ lệ lệch không phụ thuộc cỡ đinh?", 3.0),
   ("Thí nghiệm này chưa nói được gì?", 3.2),
   ("Bi va cứng; alpha lệch do lực điện đẩy.", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=2.5, caps=[
   ("Nới vùng lăn 20→40 cm: tỉ lệ lệch ra sao?", 4.6)]),
]
SC = {s["key"]: s for s in SCENES}

CLIP = dict(id="tn-l12-hatnhan-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Hạt nhân và mô hình nguyên tử · thachlab.id.vn",
            cues=_cues, scenes=SCENES)
