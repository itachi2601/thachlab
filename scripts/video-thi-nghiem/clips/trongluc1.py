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
#   G o tam, cach diem treo 5 cm (so chua hien; can Pythagore + chia doi). Tu kiem: python clips/trongluc1.py --kiem
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
            dtext(d, (x + ux / L * 48, y + uy / L * 48), k, F(44), LC[k], a)
    if show_g:
        gx, gy = S(G); dot(d, gx, gy, 12, RED, WHITE)
        dtext(d, (gx + 50, gy - 50), "G", F(48), RED, a)

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

def think_bar(d, t, t1, t2, y, a):
    q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, y, 940, y + 12], radius=6, fill=A(LIGHT, a))
    if q < 1: d.rounded_rectangle([140, y, 140 + 800 * (1 - q), y + 12], radius=6, fill=A(PURPLE, a))

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.7
DRAW = 0.8                 # thoi gian ke mot duong
def s_hook(img, d, t, sc):
    M = sc["M"]
    board(d)
    th = swing(t - 0.2, HOLES["A"])
    q = clamp((t - 0.2 - SWING - 0.2) / DRAW)
    bia(d, "A", th, part=("A", q))
    plumb(d)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 540), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 235, "Bìa treo ở A đã đứng yên,\nđã kẻ theo dây dọi.\nTrọng tâm G nằm ở đâu?", 52, INK,
          maxw=900, alpha=a)
    text(d, (W / 2, y0 + 425), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=a)
    if t > M[1] + 0.6: think_bar(d, t, M[1] + 0.6, sc["T"] - THINK_END, y0 + 495, a)

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
    # chu thich: lan treo va lo
    for j, k in enumerate(("A", "B", "C")):
        done = k == "A" or (k == "B" and t >= T_B + SWING + 0.1 + DRAW) or (k == "C" and t >= T_C + SWING + 0.1 + DRAW)
        x = 230 + j * 310; y = 1080
        card(d, (x - 130, y - 50, x + 130, y + 50), fill=WHITE, outline=LC[k], w=4, r=24)
        text(d, (x - 30, y), f"lỗ {k}", 44, LC[k])
        text(d, (x + 80, y), "✓" if done else "·", 46, DGREEN if done else GRAY)

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

# ---------------- canh 3: Dap an + rut ra ----------------
def pill(d, s, y, a, color=NAVY, size=42):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A(color, a), r=34)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

def pencil_balance(d, cx, cy, k):
    """Bia nam ngang (nhin xien, nen doc 0,35) dat tren dau but chi tai G."""
    S = lambda p: (cx + (p[0] - G[0]) * 0.8, cy + (p[1] - G[1]) * 0.8 * 0.33)
    d.polygon([(cx - 14, cy + 6), (cx + 14, cy + 6), (cx + 14, cy + 190), (cx - 14, cy + 190)], fill=A(YELLOW, k), outline=A(INK, k))
    d.polygon([(cx - 14, cy + 6), (cx + 14, cy + 6), (cx, cy - 4)], fill=A((60, 60, 60), k))
    poly = [S(p) for p in V]
    side = [(x, y + 12) for x, y in poly]                       # be day cua bia: bia nam ngang
    d.polygon(side, fill=A(CARD_D, k))
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        d.polygon([(x1, y1), (x2, y2), (x2, y2 + 12), (x1, y1 + 12)], fill=A(CARD_D, k))
    d.polygon(poly, fill=A(CARD_C, k)); d.line(poly + [poly[0]], fill=A(CARD_D, k), width=4, joint="curve")
    for key in HOLES:
        d.line([S(HOLES[key]), S(ENDS[key])], fill=A(LC[key], k), width=4)
    dot(d, cx, cy, 7, RED)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    board(d, bot=1000)
    ka = appear(t, 0.15, 0.4)
    bia(d, "A", 0.0, ("A", "B", "C"), show_g=True, P0=(150, 400), sc=1.0)
    k1 = appear(t, M[1] - 0.1, 0.5)
    if k1 > 0:
        card(d, (640, 330, 1020, 960), fill=A(WHITE, k1), r=26)
        pencil_balance(d, 830, 640, k1)
        text(d, (830, 880), "đặt G lên", 42, INK, alpha=k1)
        text(d, (830, 930), "đầu bút chì", 42, INK, alpha=k1)
    pill(d, "ĐÁP ÁN · Trên đường vừa kẻ", 1060, ka)
    k2 = appear(t, M[0] + 1.2, 0.45)
    if k2 > 0:
        y0 = 1130 + (1 - k2) * 20
        card(d, (40, y0, 1040, y0 + 200), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, y0 + 70), "Treo đứng yên: G ở", 46, DGREEN, alpha=k2)
        text(d, (W / 2, y0 + 140), "ngay dưới điểm treo", 46, DGREEN, alpha=k2)

# ---------------- canh 4: Bay (vong dem) roi Chua noi duoc ----------------
RO, RI = 150, 72            # vong dem: ban kinh ngoai, trong (px)
def washer(d, k, show):
    px, py = 540, 330                       # ghim cham mep trong cua lo
    cx, cy = px, py + RI                    # can bang: tam ngay duoi ghim
    if show: plumb(d, (px, py), L=480, a=k)
    ring = Image.new("L", (2 * RO + 4, 2 * RO + 4), 0); dr = ImageDraw.Draw(ring)
    dr.ellipse([2, 2, 2 * RO + 2, 2 * RO + 2], fill=255); dr.ellipse([RO + 2 - RI, RO + 2 - RI, RO + 2 + RI, RO + 2 + RI], fill=0)
    IMG_REF[0].paste((170, 176, 190), (int(cx - RO - 2), int(cy - RO - 2)), ring)
    d.ellipse([cx - RO, cy - RO, cx + RO, cy + RO], outline=INK, width=4)
    d.ellipse([cx - RI, cy - RI, cx + RI, cy + RI], outline=INK, width=4)
    if show:
        d.line([(px, py), (px, py + 480)], fill=INK, width=3)
        dot(d, cx, cy, 12, RED, WHITE)
        d.line([(cx + 16, cy), (cx + RO + 40, cy)], fill=RED, width=3)
        text(d, (cx + RO + 56, cy), "G", 48, RED, anchor="lm")
    dot(d, px, py, 11, PIN)

def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    board(d, bot=900)
    ks = clamp((t - M[0] - 1.6) / 0.4)
    kk = appear(t, M[0] + 1.9, 0.4)
    washer(d, kk, kk > 0)
    text(d, (70, 330), "vòng đệm", 44, INK, anchor="lm")
    text(d, (70, 390), "(như đĩa CD)", 40, INK, anchor="lm")
    a1 = appear(t, 0.1, 0.4) * (1 - k2)
    if a1 > 0:
        y0 = 930
        card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 40, WHITE, alpha=a1)
        q = "“Trọng tâm luôn nằm trên vật”"
        lw = tw(d, q, F(48)); yy = y0 + 200
        text(d, (W / 2 - 24, yy), q, 48, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0:
            xa = W / 2 - 24 - lw / 2 - 6
            d.line([(xa, yy + 2), (xa + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
            text(d, (W / 2 - 24 + lw / 2 + 34, yy), "✗", 48, DRED, alpha=a1 * ks)
        k3 = a1 * kk
        card(d, (70, y0 + 300, 1010, y0 + 520), fill=A((236, 253, 243), k3), r=24)
        text(d, (W / 2, y0 + 370), "✓ Vòng đệm: G ở tâm lỗ,", 46, DGREEN, alpha=k3)
        text(d, (W / 2, y0 + 450), "chỗ không có vật chất", 46, DGREEN, alpha=k3)
    if k2 > 0:
        y0 = 930 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 400), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 75), "Chưa nói được", 46, NAVY, alpha=k2)
        kq = k2 * appear(t, M[1] + 0.3, 0.4)
        text(d, (90, y0 + 180), "• Đã coi bìa phẳng, đồng chất", 44, INK, anchor="lm", alpha=kq)
        text(d, (90, y0 + 270), "• Vật dày, ghép nhiều chất:", 44, INK, anchor="lm", alpha=kq)
        text(d, (128, y0 + 345), "chưa thử", 44, INK, anchor="lm", alpha=kq)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def body(d, t, k):
        # bia chu nhat 8 cm x 6 cm treo o mot goc, 25 px/cm (khong ve G, khong ve duong cheo)
        vx, vy = 540, 930
        u, v = (-120, 160), (120, 90)                          # canh 8 cm, canh 6 cm
        rect = [(vx, vy), (vx + u[0], vy + u[1]), (vx + u[0] + v[0], vy + u[1] + v[1]), (vx + v[0], vy + v[1])]
        d.polygon(rect, fill=A(CARD_C, k)); d.line(rect + [rect[0]], fill=A(CARD_D, k), width=5, joint="curve")
        d.line([(vx, vy), (vx, vy + 300)], fill=A(INK, k), width=3)
        d.polygon([(vx - 14, vy + 300), (vx + 14, vy + 300), (vx, vy + 336)], fill=A(BOB, k))
        dot(d, vx, vy, 10, PIN)
        text(d, (vx + u[0] / 2 - 30, vy + u[1] / 2), "8 cm", 44, BLUE, anchor="rm", alpha=k)
        text(d, (vx + v[0] / 2 + 30, vy + v[1] / 2 - 10), "6 cm", 44, BLUE, anchor="lm", alpha=k)
        kh = appear(t, M[0] + 0.4 + 2.5, 0.5)
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1355, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1450, "Bìa đồng chất, dày đều", 44, ORANGE, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Treo đứng yên:\nG ngay dưới điểm treo",
             "Bìa chữ nhật 8 cm × 6 cm, treo\nở một góc. G cách điểm treo mấy cm?", body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding"), (do["t0"] + T_B, "tap"),
            (do["t0"] + T_C, "tap"), (da["t0"] + 0.15, "ding"), (b["t0"] + b["M"][0] + 1.6, "buzz"),
            (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-trong-luc-luc-cang-01", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
            footer="Trọng lực và lực căng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Treo tấm bìa có ba lỗ", draw=s_hook, tail=0.8, caps=[
   ("Treo ở A, kẻ theo dây dọi.", 3.4),
   ("Dừng video, chọn đáp án.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Treo ở B, đợi bìa đứng yên.", 3.7),
   ("Treo ở C, kẻ thêm đường thứ ba.", 3.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Ba đường cắt nhau tại một điểm.", 3.8),
   ("Đặt G lên bút chì: bìa thăng bằng.", 4.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Treo vòng đệm ở mép.", 4.9),
   ("Chưa nói được gì?", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Dừng video, tự trả lời.", 7.0)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("G =", tuple(round(v, 1) for v in G), "| goc can bang:",
              {k: round(math.degrees(theta_eq(h)), 1) for k, h in HOLES.items()})
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
