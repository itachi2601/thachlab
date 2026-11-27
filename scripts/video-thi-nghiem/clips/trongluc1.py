# Clip: tn-l10-trong-luc-luc-cang-01 - Tim trong tam tam bia phang bang day doi (lo 7, 18/11/2026)
# Kho content/thi-nghiem/tn-l10-trong-luc-luc-cang-01.json (dinh tinh, so_lieu_mau: lan 1-3 treo o A, B, C, duong ke
#   deu qua G): G tinh bang cong thuc mo_hinh (xG, yG theo dien tich da giac) cho tam bia ngu giac trong clip;
#   vat treo can bang <=> G nam tren duong thang dung qua diem treo (mo_hinh.phuong_trinh[3]) -> goc can bang tinh ra.
# Bo cuc KHAC trongluc2/trongluc3 (luc ke, qua nang dong thau, rong roc): bang ghim ban (nau nhat), tam bia xanh,
#   ba duong ke ba mau, khong co luc ke.
# Du doan (K10: chi cau hoi + hinh): bia treo o A da dung yen, da ke duong A -> G o dau? Dap an: tren duong vua ke.
# Bay = hien_tuong_hay_sai[1] (trong tam luon nam tren vat) + vong dem (cac_buoc.lam[3], quan_sat[2]).
# Chua noi duoc = mo_hinh.gia_thiet[0] (bia phang, dong chat, day deu).
# Chot: bia chu nhat dong chat 8 x 6 cm treo o mot goc -> day doi trung duong cheo 10 cm,
#   G o tam, cach diem treo 5 cm (so chua hien; can Pythagore + chia doi). Tu kiem: PYTHONPATH=. python3 clips/trongluc1.py --kiem
import math
from engine import *

CORK = (226, 196, 150); CORK_D = (186, 150, 100); CARD_C = (204, 236, 238); CARD_D = (60, 130, 140)
PIN = (90, 95, 110); BOB = (120, 125, 140); DGREEN = (21, 110, 55); DRED = (185, 28, 28)
LC = {"A": BLUE, "B": ORANGE, "C": PURPLE}

# Tam bia ngu giac loi (toa do rieng, px) va ba lo gan mep
V = [(0, 0), (260, -40), (340, 150), (190, 300), (-40, 210)]
HOLES = {"A": (22, 12), "B": (310, 140), "C": (180, 270)}

def centroid(P):
    A2 = sx = sy = 0.0
    for i in range(len(P)):
        x0, y0 = P[i]; x1, y1 = P[(i + 1) % len(P)]
        c = x0 * y1 - x1 * y0; A2 += c; sx += (x0 + x1) * c; sy += (y0 + y1) * c
    return sx / (3 * A2), sy / (3 * A2)
G = centroid(V)

def inside(p, P=V):
    s = None
    for i in range(len(P)):
        x0, y0 = P[i]; x1, y1 = P[(i + 1) % len(P)]
        c = (x1 - x0) * (p[1] - y0) - (y1 - y0) * (p[0] - x0)
        if s is None: s = c > 0
        elif (c > 0) != s: return False
    return True

def far_end(h):
    """Diem tren mep bia, theo tia tu lo h qua G (duong ke theo day doi)."""
    ux, uy = G[0] - h[0], G[1] - h[1]; L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
    lo, hi = L, 2000.0
    for _ in range(50):
        m = (lo + hi) / 2
        if inside((h[0] + ux * m, h[1] + uy * m)): lo = m
        else: hi = m
    return h[0] + ux * (lo - 6), h[1] + uy * (lo - 6)
ENDS = {k: far_end(h) for k, h in HOLES.items()}

def theta_eq(h):
    """Goc quay de G nam ngay duoi lo h (truc y huong xuong)."""
    return math.pi / 2 - math.atan2(G[1] - h[1], G[0] - h[0])

PX, PY = 540, 340           # dinh ghim
SC = 1.25
def to_screen(p, h, th, P0=(PX, PY), sc=SC):
    x, y = (p[0] - h[0]) * sc, (p[1] - h[1]) * sc; c, s = math.cos(th), math.sin(th)
    return (P0[0] + c * x - s * y, P0[1] + s * x + c * y)

def board(d, top=260, bot=1000):
    card(d, (40, top, 1040, bot), fill=CORK, outline=CORK_D, w=4, r=28)
    for i in range(70):   # vet ban
        x = 70 + (i * 137) % 940; y = top + 30 + (i * 89) % (bot - top - 60)
        d.ellipse([x, y, x + 6, y + 4], fill=CORK_D)

def bia(d, h_key, th, lines=(), part=None, show_g=False, P0=(PX, PY), sc=SC, labels=True, a=1.0):
    """Ve tam bia treo o lo h_key, goc th. lines: cac duong da ke; part: (key, ti le) duong dang ke do."""
    h = HOLES[h_key]; S = lambda p: to_screen(p, h, th, P0, sc)
    poly = [S(p) for p in V]
    d.polygon(poly, fill=A(CARD_C, a)); d.line(poly + [poly[0]], fill=A(CARD_D, a), width=5, joint="curve")
    for k in list(lines) + ([part[0]] if part else []):
        q = 1.0 if k in lines else part[1]
        if q <= 0: continue
        p0 = HOLES[k]; p1 = ENDS[k]; pe = (lerp(p0[0], p1[0], q), lerp(p0[1], p1[1], q))
        d.line([S(p0), S(pe)], fill=A(LC[k], a), width=6)
    for k, p in HOLES.items():
        x, y = S(p); d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=A(WHITE, a), outline=A(CARD_D, a), width=3)
        if labels:
            gx, gy = S(G); ux, uy = gx - x, gy - y; L = math.hypot(ux, uy)
            dtext(d, (x + ux / L * 56, y + uy / L * 56), k, F(58), LC[k], a)
    if show_g:
        gx, gy = S(G); dot(d, gx, gy, 12, RED, WHITE)
        dtext(d, (gx + 56, gy - 50), "G", F(62), RED, a)

def plumb(d, P0=(PX, PY), L=600, a=1.0):
    x, y = P0
    d.line([(x, y), (x, y + L)], fill=A(INK, a), width=3)
    d.polygon([(x - 18, y + L), (x + 18, y + L), (x, y + L + 46)], fill=A(BOB, a), outline=A(INK, a))
    dot(d, x, y, 11, PIN)

SWING = 2.0
def swing(tau, h):
    """Bia vua treo vao lo h: dao dong tat dan, tu SWING s tro di dung yen dung goc can bang."""
    te = theta_eq(h)
    if tau >= SWING: return te
    env = 0.5 * math.exp(-1.6 * tau) * (1 - ease((tau - SWING + 0.6) / 0.6))
    return te + env * math.cos(2 * math.pi * 0.9 * tau)

def think_bar(d, t, t1, t2, y, a, col=(88, 28, 135), x0=80, x1=1000, h=92):
    """Thanh dem LIEN (khong chia o, lo 20: so o = dap an), cao 92 px, mau dam trong vung y 200-1580 de --do-chu thay hinh doi."""
    q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([x0, y, x1, y + h], radius=h // 2, fill=A(WHITE, a), outline=A((148, 140, 128), a), width=4)
    if q < 1: d.rounded_rectangle([x0, y, x0 + max(h, (x1 - x0) * (1 - q)), y + h], radius=h // 2, fill=A(col, a))

# ---------------- canh 1: Du doan (K10: khong nut A-D, chi cau hoi + hinh; thanh dem lien) ----------------
THINK_END = 0.3
DRAW = 0.8                 # thoi gian ke mot duong
def pill(d, s, y, a, color=NAVY, size=56):
    pw = tw(d, s, F(size)) + 64
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

def s_hook(img, d, t, sc):
    M = sc["M"]
    board(d)
    th = swing(t - 0.2, HOLES["A"])
    q = clamp((t - 0.2 - SWING - 0.2) / DRAW)
    bia(d, "A", th, part=("A", q))
    plumb(d)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1040 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 530), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 70, a, PURPLE)
    text(d, (W / 2, y0 + 195), "Bìa đã đứng yên.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 295), "Trọng tâm G ở đâu?", 64, PURPLE, alpha=a)
    think_bar(d, t, M[1] + 0.4, sc["T"] - THINK_END, y0 + 400, a)

# ---------------- canh 2: Tien hanh (treo B roi C trong MOT canh) ----------------
T_B, T_C = 0.2, 3.9        # luc treo vao lo B, lo C
def do_state(t):
    """-> (lo dang treo, goc, cac duong da ke, duong dang ke (key, ti le), hien G)."""
    if t < T_C:
        tau = t - T_B; q = clamp((tau - SWING - 0.1) / DRAW)
        return "B", swing(tau, HOLES["B"]), ("A",), ("B", q), q >= 1
    tau = t - T_C; q = clamp((tau - SWING - 0.1) / DRAW)
    return "C", swing(tau, HOLES["C"]), ("A", "B"), ("C", q), True

def s_do(img, d, t, sc):
    board(d)
    hk, th, lines, part, g = do_state(max(t, T_B))
    bia(d, hk, th, lines, part, show_g=g)
    plumb(d)
    for j, k in enumerate(("A", "B", "C")):            # chu thich: lo da treo + ke xong
        done = k == "A" or (k == "B" and t >= T_B + SWING + 0.1 + DRAW) or (k == "C" and t >= T_C + SWING + 0.1 + DRAW)
        x = 210 + j * 330; y = 1090
        card(d, (x - 150, y - 56, x + 150, y + 56), fill=WHITE, outline=LC[k], w=5, r=26)
        text(d, (x - 30, y), f"lỗ {k}", 60, LC[k])
        text(d, (x + 95, y), "✓" if done else "·", 62, DGREEN if done else GRAY)

def _kiem_dong_bo():
    """Moi 0,05 s: duong chi duoc ke khi bia da dung yen (goc = goc can bang); G chi hien khi du 2 duong;
    moi duong ke (tren bia) phai trung day doi (thang dung qua ghim) va di qua G."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        hk, th, lines, part, g = do_state(max(t, T_B))
        if part[1] > 0 and abs(th - theta_eq(HOLES[hk])) > 1e-9: bad.append((round(t, 2), "ke khi bia chua yen", hk))
        if g and len(lines) + (part[1] >= 1) < 2: bad.append((round(t, 2), "G som"))
        t += 0.05
    for k, h in HOLES.items():
        gx, gy = to_screen(G, h, theta_eq(h)); ex, ey = to_screen(ENDS[k], h, theta_eq(h))
        if abs(gx - PX) > 1e-6 or abs(ex - PX) > 1e-6 or gy <= PY: bad.append(("duong khong thang dung", k))
    if T_C + SWING + 0.1 + DRAW > sc["T"] - 0.5: bad.append("duong C ke qua muon")
    return bad

# ---------------- canh 3: Dap an + rut ra (moi khoi chu cach >= 2,5 s) ----------------
def pencil_balance(d, cx, cy, k, tilt=0.0):
    """Bia nam ngang (nhin xien, nen doc 0,33) dat tren dau but chi tai G; tilt: nghieng nhe luc moi dat (tat dan)."""
    S = lambda p: (cx + (p[0] - G[0]) * 0.8, cy + (p[1] - G[1]) * 0.8 * 0.33 + (p[0] - G[0]) * 0.8 * tilt)
    d.polygon([(cx - 14, cy + 6), (cx + 14, cy + 6), (cx + 14, cy + 190), (cx - 14, cy + 190)], fill=A(YELLOW, k), outline=A(INK, k))
    d.polygon([(cx - 14, cy + 6), (cx + 14, cy + 6), (cx, cy - 4)], fill=A((60, 60, 60), k))
    poly = [S(p) for p in V]
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        d.polygon([(x1, y1), (x2, y2), (x2, y2 + 12), (x1, y1 + 12)], fill=A(CARD_D, k))
    d.polygon(poly, fill=A(CARD_C, k)); d.line(poly + [poly[0]], fill=A(CARD_D, k), width=4, joint="curve")
    for key in HOLES:
        d.line([S(HOLES[key]), S(ENDS[key])], fill=A(LC[key], k), width=4)
    dot(d, cx, cy, 8, RED)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    board(d, bot=1000)
    bia(d, "A", 0.0, ("A", "B", "C"), show_g=True, P0=(150, 400), sc=1.0)
    k1 = appear(t, M[1] - 0.1, 0.5)
    if k1 > 0:
        card(d, (640, 330, 1020, 960), fill=A(WHITE, k1), r=26)
        tau = max(0.0, t - M[1] + 0.1)
        pencil_balance(d, 830, 680, k1, tilt=0.12 * math.exp(-1.4 * tau) * math.cos(2 * math.pi * 1.1 * tau))
    pill(d, "Đáp án: trên đường kẻ", 1075, appear(t, 0.2, 0.45))
    k2 = appear(t, M[0] + 2.6, 0.45)
    if k2 > 0:
        y0 = 1160 + (1 - k2) * 20
        card(d, (40, y0, 1040, y0 + 220), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, y0 + 70), "Treo đứng yên: G ở", 60, DGREEN, alpha=k2)
        text(d, (W / 2, y0 + 155), "ngay dưới điểm treo", 60, DGREEN, alpha=k2)

# ---------------- canh 4: Bay - hai truong hop canh nhau: bia (G tren vat) | vong dem (G o cho trong) ----------------
RO, RI = 140, 66            # vong dem: ban kinh ngoai, trong (px)
WP = (795, 340)             # ghim treo vong dem
def washer(d, phi, show_g, k=1.0):
    px, py = WP
    cx, cy = px + RI * math.sin(phi), py + RI * math.cos(phi)     # ghim cham mep trong lo; can bang: tam ngay duoi ghim
    ring = Image.new("L", (2 * RO + 4, 2 * RO + 4), 0); dr = ImageDraw.Draw(ring)
    dr.ellipse([2, 2, 2 * RO + 2, 2 * RO + 2], fill=255); dr.ellipse([RO + 2 - RI, RO + 2 - RI, RO + 2 + RI, RO + 2 + RI], fill=0)
    IMG_REF[0].paste((170, 176, 190), (int(cx - RO - 2), int(cy - RO - 2)), ring)
    d.ellipse([cx - RO, cy - RO, cx + RO, cy + RO], outline=INK, width=4)
    d.ellipse([cx - RI, cy - RI, cx + RI, cy + RI], outline=INK, width=4)
    if show_g:
        d.line([(px, py), (px, py + 440)], fill=INK, width=3)
        d.polygon([(px - 16, py + 440), (px + 16, py + 440), (px, py + 482)], fill=BOB, outline=INK)
        dot(d, cx, cy, 13, RED, WHITE)
        text(d, (cx + 40, cy - 34), "G", 62, RED, anchor="lm")
    dot(d, px, py, 11, PIN)

def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 530, 1010), fill=CORK, outline=CORK_D, w=4, r=26)
    card(d, (550, 260, 1040, 1010), fill=CORK, outline=CORK_D, w=4, r=26)
    bia(d, "A", theta_eq(HOLES["A"]), ("A",), show_g=True, P0=(285, 330), sc=0.7, labels=False)
    plumb(d, (285, 330), L=520)
    kw = appear(t, M[1] - 0.1, 0.4)
    if kw > 0:
        tau = t - M[1] + 0.1
        phi = 0.55 * math.exp(-1.3 * tau) * math.cos(2 * math.pi * 0.8 * tau) if tau < 2.4 else 0.0
        washer(d, phi, t >= M[2] - 0.1)
        text(d, (795, 940), "vòng đệm", 58, INK)
    k1 = appear(t, M[0] + 0.3, 0.45)
    card(d, (60, 1050, 1020, 1160), fill=A((254, 242, 242), k1), outline=A(DRED, k1), r=24, w=6)
    text(d, (W / 2, 1105), "✗ Dễ tưởng: G luôn ở trên vật", 58, DRED, alpha=k1)
    k3 = appear(t, M[2] + 0.4, 0.45)
    if k3 > 0:
        card(d, (60, 1200, 1020, 1310), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), r=24, w=6)
        text(d, (W / 2, 1255), "✓ G ở chỗ không có vật chất", 58, DGREEN, alpha=k3)

# ---------------- canh 5: Chua noi duoc (hinh: khoi day ghep go + sat, G = ?) ----------------
def s_gioihan(img, d, t, sc):
    card(d, (40, 260, 1040, 470), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 320), "Chưa nói được", 60, NAVY)
    text(d, (W / 2, 410), "Vật dày, hai chất?", 60, INK)
    k = appear(t, 0.3, 0.6)
    card(d, (40, 500, 1040, 1250), fill=A(WHITE, k), outline=A(LIGHT, k), w=3)
    x0, x1, y0, y1, dz = 230, 850, 720, 1060, 90               # khoi hop nhin xien
    xm = (x0 + x1) / 2
    for (a, b, col) in ((x0, xm, (222, 184, 135)), (xm, x1, (150, 158, 172))):
        d.polygon([(a, y0), (b, y0), (b + dz, y0 - dz), (a + dz, y0 - dz)], fill=A(mix(col, WHITE, 0.25), k), outline=A(INK, k))
        d.rectangle([a, y0, b, y1], fill=A(col, k), outline=A(INK, k), width=3)
    d.polygon([(x1, y0), (x1 + dz, y0 - dz), (x1 + dz, y1 - dz), (x1, y1)], fill=A((120, 128, 142), k), outline=A(INK, k))
    text(d, ((x0 + xm) / 2, (y0 + y1) / 2), "gỗ", 62, INK, alpha=k)
    text(d, ((xm + x1) / 2, (y0 + y1) / 2), "sắt", 62, WHITE, alpha=k)
    p = 1 + 0.18 * math.sin(2 * math.pi * 0.9 * max(0.0, t - 0.6))            # dau hoi nhip nhe (hinh khong dung yen)
    dot(d, xm, 1150, 50 * p, A(PURPLE, k)); text(d, (xm, 1152), "?", int(72 * p), WHITE, alpha=k)
    d.line([(xm, 1100 - 50 * (p - 1)), (xm, y1 + 8)], fill=A(PURPLE, k), width=4)

# ---------------- canh 6: Chot (phu de) + THU NGHI: bia chu nhat 8 x 6 cm treo o mot goc ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1570), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 300, k1, ORANGE)
    vx, vy = 540, 430                                     # 25 px/cm; khong ve G, khong ve duong cheo
    u, v = (-160, 213), (160, 120)                        # canh 8 cm (dai 266 px... ti le 8:6 = 266:200)
    rect = [(vx, vy), (vx + u[0], vy + u[1]), (vx + u[0] + v[0], vy + u[1] + v[1]), (vx + v[0], vy + v[1])]
    d.polygon(rect, fill=A(CARD_C, k1)); d.line(rect + [rect[0]], fill=A(CARD_D, k1), width=5, joint="curve")
    d.line([(vx, vy), (vx, vy + 400)], fill=A(INK, k1), width=3)
    d.polygon([(vx - 16, vy + 400), (vx + 16, vy + 400), (vx, vy + 442)], fill=A(BOB, k1))
    dot(d, vx, vy, 11, PIN)
    text(d, (vx + u[0] / 2 - 30, vy + u[1] / 2 - 10), "8 cm", 60, BLUE, anchor="rm", alpha=k1)
    text(d, (vx + v[0] / 2 + 34, vy + v[1] / 2 - 20), "6 cm", 60, BLUE, anchor="lm", alpha=k1)
    text(d, (W / 2, 1010), "Bìa đồng chất, treo ở góc.", 58, INK, alpha=k1)
    text(d, (W / 2, 1150), "G cách điểm treo bao xa?", 64, DORANGE, alpha=k1)
    think_bar(d, t, 1.0, sc["T"] - 0.2, 1300, k1, col=DORANGE)

DORANGE = (176, 64, 8)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.9, "ding"), (do["t0"] + T_B, "tap"),
            (do["t0"] + T_C, "tap"), (da["t0"] + 0.2, "ding"), (b["t0"] + b["M"][0] + 0.3, "buzz"),
            (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l10-trong-luc-luc-cang-01", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
            footer="Trọng lực và lực căng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Treo tấm bìa có ba lỗ", draw=s_hook, tail=0.3, caps=[
   ("Treo ở A, kẻ theo dây dọi.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Treo ở B, đợi bìa đứng yên.", 3.7),
   ("Treo ở C, kẻ đường thứ ba.", 3.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Ba đường cắt nhau tại một điểm.", 3.8),
   ("Đặt G lên bút chì: thăng bằng.", 3.8)]),
 dict(key="bay", title="Bẫy: trọng tâm ở đâu?", draw=s_bay, tail=0.4, caps=[
   ("Đây là bẫy hay gặp.", 3.1),
   ("Treo vòng đệm ở mép.", 3.3),
   ("Dây dọi đi qua tâm lỗ.", 3.5)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.6, caps=[
   ("Ở đây coi bìa phẳng, đồng chất.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Hai dây dọi cắt nhau tại G.", 6.2)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("G =", tuple(round(v, 1) for v in G), "| goc can bang:",
              {k: round(math.degrees(theta_eq(h)), 1) for k, h in HOLES.items()})
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
