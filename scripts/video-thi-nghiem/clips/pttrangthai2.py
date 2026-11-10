# Clip: tn-l12-pttrangthai-02 - Binh kin ngam nuoc o nam nhiet do: p/T khong doi
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-pttrangthai-02.json (so_lieu_mau, mo_hinh).
# Ban 1 (28/10/2026): mau boyle (dung cu + bang + do thi) + cues nhu apsuat2, nhung goc nhin khac:
#   binh di qua 5 chau nuoc (0/25/50/75/100 C), hop Du doan hoi "dai luong nao khong doi", bay = chia cho do C.
import random
from engine import *

ROWS = [(0, 273, 100.0, 0.366), (25, 298, 108.9, 0.365), (50, 323, 118.4, 0.367),
        (75, 348, 126.9, 0.365), (100, 373, 136.3, 0.365)]      # so_lieu_mau: t (C), T (K), p (kPa), p/T (kPa/K)
K_PT = 100 / 273                                                 # mo_hinh: hang so p/T = 100/273 (chi de ve duong thang)
# Bay: p/t (do C) suy thang tu so_lieu_mau: 108,9/25 = 4,36; 118,4/50 = 2,37; 126,9/75 = 1,69; 136,3/100 = 1,36; 0 C -> chia cho 0
P_TC = [None] + [round(p / tc, 2) for tc, _, p, _ in ROWS[1:]]
def f1(v): return f"{v:.1f}".replace(".", ",")
def f2(v): return f"{v:.2f}".replace(".", ",")
def f3(v): return f"{v:.3f}".replace(".", ",")

# ---------------- dung cu: 5 chau nuoc + binh tam giac kin + nhiet ke + bang so ----------------
BXS = [150, 345, 540, 735, 930]          # tam 5 chau
BT0, BT1, WTOP = 720, 900, 748           # mieng chau, day chau, mat nuoc
R = random.Random(5)
PART = [(R.random(), R.random(), R.choice((-1, 1)) * R.uniform(0.3, 0.5), R.choice((-1, 1)) * R.uniform(0.3, 0.5))
        for _ in range(12)]
BUB = [(R.uniform(-60, 60), R.random()) for _ in range(7)]

def heat(tc): return clamp(tc / 100)
def water(tc): return mix((191, 219, 254), (254, 196, 160), heat(tc))

def bath(d, t, i):
    cx, tc = BXS[i], ROWS[i][0]
    d.rectangle([cx - 88, WTOP, cx + 88, BT1], fill=water(tc))
    if i == 0:                                     # nuoc da dang tan
        for dx, dy in ((-52, 6), (34, 2), (-8, 14)):
            d.rounded_rectangle([cx + dx, WTOP + dy, cx + dx + 26, WTOP + dy + 22], radius=5, fill=WHITE, outline=(140, 170, 210), width=3)
    if i == 4:                                     # nuoc dang soi: bot khi noi len
        for dx, ph in BUB:
            q = (ph + t * 0.8) % 1
            d.ellipse([cx + dx - 7, BT1 - 12 - q * 140 - 7, cx + dx + 7, BT1 - 12 - q * 140 + 7], outline=WHITE, width=3)
    d.line([(cx - 88, BT0), (cx - 88, BT1), (cx + 88, BT1), (cx + 88, BT0)], fill=NAVY, width=6, joint="curve")
    text(d, (cx, BT1 + 36), f"{tc} °C", 36, INK)

def flask(d, t, fx, fy, tc):
    """fx: tam binh; fy: day binh. Binh tam giac day nut, ong mem len ap ke, nhiet ke gan ben phai."""
    body = [(fx - 54, fy), (fx + 54, fy), (fx + 24, fy - 112), (fx + 24, fy - 166), (fx - 24, fy - 166), (fx - 24, fy - 112)]
    d.polygon(body, fill=(236, 242, 252), outline=(70, 78, 100))
    d.line(body + [body[0]], fill=(70, 78, 100), width=6, joint="curve")
    sp = math.sqrt((tc + 273) / 273)               # v ti le can T
    for (ux, uy, vx, vy) in PART:
        yy = fy - 16 - refl(uy + vy * t * sp, 0, 1) * 88
        half = lerp(42, 18, (fy - 16 - yy) / 96)    # be ngang thu hep dan len vai binh
        x = fx + (refl(ux + vx * t * sp, 0, 1) * 2 - 1) * half
        dot(d, x, yy, 8, mix(BLUE, RED, heat(tc)))
    d.rounded_rectangle([fx - 30, fy - 190, fx + 30, fy - 162], radius=6, fill=NAVY)   # nut
    # ong noi len ap ke (cong bac hai)
    p0, p1, p2 = (fx, fy - 190), (fx, 470), (730, 432)
    pts = [((1 - s) ** 2 * p0[0] + 2 * (1 - s) * s * p1[0] + s * s * p2[0],
            (1 - s) ** 2 * p0[1] + 2 * (1 - s) * s * p1[1] + s * s * p2[1]) for s in [k / 24 for k in range(25)]]
    d.line(pts, fill=GRAY, width=12, joint="curve")
    # nhiet ke cam canh binh, bau khong cham day chau
    tx = fx + 62
    d.rounded_rectangle([tx - 8, fy - 230, tx + 8, fy - 30], radius=8, fill=WHITE, outline=NAVY, width=3)
    dot(d, tx, fy - 24, 10, RED, NAVY)
    d.rectangle([tx - 4, lerp(fy - 50, fy - 215, heat(tc)), tx + 4, fy - 30], fill=RED)

def readout(d, t_lbl, p_lbl):
    card(d, (150, 240, 930, 432), fill=WHITE, outline=LIGHT, r=28, w=4)
    text(d, (345, 275), "Nhiệt kế", 36, NAVY)
    text(d, (730, 275), "Áp kế", 36, NAVY)
    d.rounded_rectangle([185, 305, 505, 405], radius=16, fill=WHITE, outline=NAVY, width=4)
    text(d, (345, 355), t_lbl, 54, RED)
    d.rounded_rectangle([570, 305, 890, 405], radius=16, fill=NAVY)
    text(d, (730, 355), p_lbl, 54, (134, 239, 172))

def rig(d, t, fx, fy, tc, t_lbl, p_lbl):
    for i in range(5): bath(d, t, i)
    flask(d, t, fx, fy, tc)
    readout(d, t_lbl, p_lbl)

def lbl_t(i): return f"{ROWS[i][0]} °C"
def lbl_p(i): return f"{f1(ROWS[i][2])} kPa"

# ---------------- canh 1: mo bai + du doan ----------------
OPTS = ("A. p nhân T", "B. p chia t (°C)", "C. p chia T (K)", "D. p trừ T")
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    rig(d, t, BXS[0], 880, 0, lbl_t(0), lbl_p(0))
    k = appear(t, sc["M"][1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (60, 990, 1020, 1600), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 1040), "Dự đoán", 46, PURPLE, alpha=k)
    ctext(d, 1122, "Bình kín: 0 → 100 °C\np: 100,0 → 136,3 kPa", 44, INK, alpha=k)
    ctext(d, 1222, "Đại lượng nào không đổi?", 46, INK, alpha=k)
    for i, s in enumerate(OPTS):
        a = appear(t, sc["M"][1] + 0.2 + i * 0.15)
        x0 = 100 + (i % 2) * 450; y = 1325 + (i // 2) * 112
        card(d, (x0, y - 42, x0 + 430, y + 42), fill=A((245, 243, 255), a), outline=A(PURPLE, a), r=22, w=4)
        text(d, (x0 + 30, y), s, 40, INK, anchor="lm", alpha=a)
    t1, t2 = sc["M"][1] + 0.7, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1540, 940, 1554], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1540, 140 + 800 * (1 - q), 1554], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: ngam lan luot 5 chau, doc t va p ----------------
ROW_T = [0.5, 1.6, 2.7, 3.8, 4.9]      # moc (trong canh) hien tung hang
MOVE = 0.9                              # nhac binh sang chau ke trong 0,9 s truoc moi hang

def pose(t):
    """(x binh, y day binh, nhiet do khi de ve, nhan nhiet ke, nhan ap ke). Dang chuyen thi hien '···'."""
    fx, fy, tc, tl, pl = BXS[0], 880, 0, lbl_t(0), lbl_p(0)
    for i in range(1, 5):
        s = ROW_T[i] - MOVE
        if t < s: break
        k = clamp((t - s) / (MOVE - 0.15))
        fx = lerp(BXS[i - 1], BXS[i], ease(clamp((k - 0.25) / 0.5)))
        fy = 880 - 150 * math.sin(math.pi * k)
        tc = lerp(ROWS[i - 1][0], ROWS[i][0], ease(k))
        if t < ROW_T[i]: tl, pl = "···", "···"
        else: tl, pl = lbl_t(i), lbl_p(i)
    return fx, fy, tc, tl, pl

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    fx, fy, tc, tl, pl = pose(t)
    rig(d, t, fx, fy, tc, tl, pl)
    card(d, (60, 990, 1020, 1600), fill=WHITE, outline=NAVY, w=4)
    xs = [330, 750]
    for x, c in zip(xs, ["t (°C)", "p (kPa)"]): text(d, (x, 1042), c, 40, NAVY)
    d.line([(100, 1080), (980, 1080)], fill=LIGHT, width=4)
    last = max([i for i in range(5) if t >= ROW_T[i]], default=-1)
    for i, (tt, _, p, _) in enumerate(ROWS):
        a = appear(t, ROW_T[i], 0.3); y = 1125 + i * 80
        if a <= 0: continue
        if i == last: d.rounded_rectangle([90, y - 34, 990, y + 34], radius=16, fill=A((225, 236, 255), a))
        text(d, (xs[0], y), str(tt), 46, RED, alpha=a)
        text(d, (xs[1], y), f1(p), 46, BLUE, alpha=a)
    text(d, (W / 2, 1560), "Số liệu minh hoạ", 36, NAVY)

# ---------------- canh 3: dap an + bang p/T ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k = back((t - 0.15) / 0.5) if t > 0.15 else 0
    card(d, (60, 245, 1020, 345), fill=(220, 252, 231), outline=GREEN, w=5)
    text(d, (W / 2, 295), "Đáp án C: p chia T (K)", int(48 * clamp(k, 0.3, 1.0)), GREEN)
    card(d, (60, 375, 1020, 1120), fill=WHITE, outline=NAVY, w=4)
    xs = [170, 385, 610, 865]
    band = appear(t, M[2] - 0.6, 0.4)
    if band > 0: d.rounded_rectangle([740, 398, 1000, 1040], radius=20, fill=A((187, 247, 208), band))
    for x, c in zip(xs, ["t (°C)", "T (K)", "p (kPa)", "p/T (kPa/K)"]): text(d, (x, 435), c, 36, NAVY)
    d.line([(90, 474), (990, 474)], fill=LIGHT, width=4)
    for i, (tt, TK, p, r) in enumerate(ROWS):
        y = 535 + i * 112
        text(d, (xs[0], y), str(tt), 52, RED)
        text(d, (xs[2], y), f1(p), 52, BLUE)
        text(d, (xs[1], y), str(TK), 52, INK, alpha=appear(t, 0.5 + i * 0.12, 0.3))
        text(d, (xs[3], y), f3(r), 52, GREEN, alpha=appear(t, M[1] + 0.3 + i * 0.25, 0.3))
    c = appear(t, 0.5)
    card(d, (60, 1160, 1020, 1600), fill=A((236, 253, 243), c), outline=A(GREEN, c), w=5)
    text(d, (W / 2, 1215), "Đổi: T = t + 273", 44, INK, alpha=c)
    text(d, (W / 2, 1300), "Chia p cho T", 44, INK, alpha=appear(t, M[1] - 0.2))
    text(d, (W / 2, 1415), "p/T ≈ 0,366 kPa/K", 60, GREEN, alpha=appear(t, M[2] - 0.4))
    ctext(d, 1530, "→ p tỉ lệ thuận với T", 44, GREEN, alpha=appear(t, M[2] + 0.6))

# ---------------- canh 4: do thi p-T qua 0 K + chua noi duoc gi ----------------
def s_why(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    x0, x1, yb, yt = 190, 960, 830, 340
    X = lambda T: x0 + T / 400 * (x1 - x0); Y = lambda p: yb - p / 150 * (yb - yt)
    card(d, (60, 245, 1020, 940), fill=WHITE, outline=LIGHT, w=3)
    for p in (50, 100, 150): d.line([(x0, Y(p)), (x1, Y(p))], fill=(240, 236, 228), width=2)
    d.line([(x0, yb), (x1 + 20, yb)], fill=NAVY, width=5); d.line([(x0, yb), (x0, yt - 30)], fill=NAVY, width=5)
    text(d, (x0 + 18, yt - 40), "p (kPa)", 36, NAVY, anchor="lm")
    text(d, (x1 + 20, yb + 78), "T (K)", 36, NAVY, anchor="rm")
    for T in (100, 200, 300, 400):
        d.line([(X(T), yb), (X(T), yb + 10)], fill=NAVY, width=3)
        text(d, (X(T), yb + 36), str(T), 34, NAVY, bold=False)
    for p in (50, 100, 150):
        d.line([(x0 - 10, Y(p)), (x0, Y(p))], fill=NAVY, width=4)
        text(d, (x0 - 18, Y(p)), str(p), 34, NAVY, bold=False, anchor="rm")
    # duong thang p = (100/273)T, ve tu diem do keo dai ve goc 0 K
    kl = ease((t - 0.3) / 1.0)
    if kl > 0:
        lo = lerp(373, 0, kl)
        for j in range(44):
            a_, b_ = lerp(400, lo, j / 44), lerp(400, lo, (j + 0.55) / 44)
            if a_ < lo and b_ < lo: break
            d.line([(X(a_), Y(K_PT * a_)), (X(b_), Y(K_PT * b_))], fill=A(BLUE, 0.7), width=6)
    for i, (_, TK, p, _) in enumerate(ROWS):
        a = appear(t, 0.1 + i * 0.1, 0.3)
        if a > 0: dot(d, X(TK), Y(p), 14 * back(a), ORANGE, WHITE)
    g = appear(t, 0.9, 0.4)
    if g > 0:
        d.ellipse([x0 - 24, yb - 24, x0 + 24, yb + 24], outline=A(BLUE, g), width=6)
        text(d, (x0 + 30, 560), "qua gốc 0 K", 38, BLUE, anchor="lm", alpha=g)
        arrow(d, (x0 + 70, 595), (x0 + 22, yb - 34), A(BLUE, g), w=5, head=20)
        for yy in range(int(Y(150)), yb, 22):         # vach 273 K = 0 C
            d.line([(X(273), yy), (X(273), yy + 11)], fill=A(RED, g), width=4)
        text(d, (X(273) - 14, Y(140)), "0 °C = 273 K", 36, RED, anchor="rm", alpha=g)
    b = appear(t, M[1] - 0.3)
    card(d, (60, 975, 1020, 1130), fill=A(WHITE, b), outline=A(BLUE, b), w=5)
    rich(d, W / 2, 1040, "p_{1}/T_{1} = p_{2}/T_{2}", 58, BLUE, alpha=b)
    c = appear(t, M[2] - 0.3)
    card(d, (60, 1170, 1020, 1520), fill=A((245, 243, 255), c), outline=A(PURPLE, c), w=5)
    text(d, (W / 2, 1245), "Chưa nói được gì?", 48, PURPLE, alpha=c)
    ctext(d, 1345, "• áp suất rất cao", 46, INK, alpha=c)
    ctext(d, 1440, "• đổi lượng khí", 46, INK, alpha=appear(t, M[2] + 0.3))

# ---------------- canh 5: bay chia cho do C ----------------
def s_trap(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    card(d, (60, 245, 1020, 340), fill=(254, 226, 226), outline=RED, w=5)
    text(d, (W / 2, 292), "Bẫy: chia p cho t (°C)", 46, RED)
    card(d, (60, 375, 1020, 960), fill=WHITE, outline=NAVY, w=4)
    xs = [230, 520, 820]
    for x, c in zip(xs, ["t (°C)", "p (kPa)", "p/t"]): text(d, (x, 428), c, 38, NAVY)
    d.line([(90, 462), (990, 462)], fill=LIGHT, width=4)
    for i, (tt, _, p, _) in enumerate(ROWS):
        y = 515 + i * 88
        text(d, (xs[0], y), str(tt), 44, INK)
        text(d, (xs[1], y), f1(p), 44, BLUE)
        a = appear(t, 0.15 + i * 0.15, 0.3)
        text(d, (xs[2], y), "÷ 0 ?" if P_TC[i] is None else f2(P_TC[i]), 44, RED, alpha=a)
    c = appear(t, M[1] - 0.3)
    if c > 0:
        arrow(d, (930, 600), (930, 870), A(RED, c), w=7, head=24)
    card(d, (60, 1000, 1020, 1270), fill=A((254, 242, 242), c), outline=A(RED, c), w=4)
    ctext(d, 1075, "p/t: 4,36 → 1,36", 48, RED, alpha=c)
    ctext(d, 1180, "ở 0 °C: chia cho 0", 46, INK, alpha=c)
    e = appear(t, M[2] - 0.2)
    card(d, (60, 1310, 1020, 1600), fill=A((220, 252, 231), e), outline=A(GREEN, e), w=4)
    ctext(d, 1400, "Làm đúng: T = t + 273", 46, GREEN, alpha=e)
    ctext(d, 1505, "rồi chia p cho T", 46, INK, alpha=e)

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    chot_hoi(d, t, sc, "Thể tích không đổi: p/T không đổi (kelvin)",
             "Ngâm bình vào nước 60 °C. Áp kế chỉ bao nhiêu?")
    kb = appear(t, M[0] + 0.6, 0.5)            # hai o so: nhiet ke 60 C, ap ke chua biet
    if kb > 0:
        for x0, lb, val, col in ((130, "Nhiệt kế", "60 °C", RED), (570, "Áp kế", "? kPa", ORANGE)):
            d.rounded_rectangle([x0, 1045, x0 + 380, 1165], radius=18, fill=A(WHITE, kb), outline=A(NAVY, kb), width=4)
            text(d, (x0 + 190, 1105), val, 60, col, alpha=kb)
    kh = appear(t, M[0] + 2.5, 0.5)            # goi y tu ve, hien tre ~2,5 s
    if kh <= 0: return
    card(d, (100, 1220, 980, 1560), fill=A((255, 237, 213), kh), outline=A(ORANGE, kh), r=24, w=4)
    text(d, (W / 2, 1285), "Gợi ý", 42, ORANGE, alpha=kh)
    ctext(d, 1420, "Đổi sang kelvin trước.", 48, INK, maxw=840, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (an["t0"] + 0.15, "ding"), (an["t0"] + an["M"][2] - 0.6, "tap"),
            (tr["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l12-pttrangthai-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Phương trình trạng thái khí lí tưởng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Bình kín qua năm chậu nước", draw=s_hook, tail=0.6, caps=[
   ("Năm chậu nước.", 2.5),
   ("Dừng video, chọn A–D.", 5.0)]),
 dict(key="do", title="Ngâm từng chậu, đọc t và p", draw=s_do, tail=0.6, caps=[
   ("Chờ 2–3 phút mỗi chậu.", 3.0),
   ("Càng nóng, p càng lớn.", 2.5)]),
 dict(key="ans", title="Chia p cho T", draw=s_ans, tail=0.6, caps=[
   ("Đổi sang kelvin.", 2.5),
   ("Chia p cho T.", 2.6),
   ("p/T gần như nhau.", 2.5)]),
 dict(key="why", title="Rút ra", draw=s_why, tail=0.6, caps=[
   ("Kéo dài đường thẳng.", 2.5),
   ("Mọi cặp: p/T như nhau.", 2.5),
   ("Hai giới hạn.", 3.0)]),
 dict(key="trap", title="Cái bẫy", draw=s_trap, tail=0.6, caps=[
   ("Nhìn cột p/t.", 2.5),
   ("Tỉ số đổi mạnh.", 2.5),
   ("Dùng kelvin.", 2.5)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 6.0)]),
])
