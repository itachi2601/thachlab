# Clip: tn-l12-apsuatdongnang-02 - Do ap suat khi trong binh kin khi doi nhiet do
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-apsuatdongnang-02.json (so_lieu_mau, tham_so).
# Ban 1 (28/10/2026): mau boyle (dung cu + bang + do thi) + cues nhu phongxa2.
import random
from engine import *

ROWS = [(10, 283, 96.0, 0.3392), (30, 303, 102.8, 0.3393), (50, 323, 109.5, 0.3390),
        (70, 343, 116.4, 0.3394), (90, 363, 123.0, 0.3388)]          # so_lieu_mau: t (C), T (K), p (kPa), p/T
V_BINH, P0, T0 = "0,25", 96.0, 283                                    # tham_so: V binh (lit), p_0 o 283 K
def model(T): return P0 * T / T0                                      # chi de ve duong thang, khong in so
def f1(v): return f"{v:.1f}".replace(".", ",")
def f4(v): return f"{v:.4f}".replace(".", ",")

# ---------------- dung cu: noi nuoc tren bep + binh kin + nhiet ke + ap ke dien tu ----------------
R = random.Random(4)
PART = [(R.random(), R.random(), R.choice((-1, 1)) * R.uniform(0.25, 0.45), R.choice((-1, 1)) * R.uniform(0.25, 0.45))
        for _ in range(16)]
STEAM = [(R.uniform(170, 510), R.random()) for _ in range(6)]

PX0, PX1, PY0, PY1 = 130, 550, 560, 930      # noi
BX0, BX1, BY0, BY1 = 230, 410, 700, 890      # binh kim loai (ngap trong nuoc)
TX, TTOP, TBULB = 185, 440, 850              # nhiet ke ben trai binh (bau sat binh, khong cham day), ong ap ke khong cat qua

def heat_of(tc): return clamp((tc - 10) / 80)

def rig(d, t, tc, p_lbl, t_lbl, ph=0.0):
    """tc: nhiet do nuoc de ve (cot nhiet ke, mau nuoc, toc do hat); p_lbl/t_lbl: chu tren hai man hinh."""
    h = heat_of(tc)
    # bep dien
    d.rounded_rectangle([PX0 - 30, PY1 + 6, PX1 + 30, PY1 + 62], radius=14, fill=NAVY)
    d.rounded_rectangle([PX0 + 40, PY1 + 6, PX1 - 40, PY1 + 22], radius=6, fill=mix((120, 125, 140), (239, 68, 68), h))
    # noi + nuoc
    d.rectangle([PX0, PY0 + 50, PX1, PY1], fill=mix((191, 219, 254), (254, 205, 170), h))
    d.line([(PX0, PY0), (PX0, PY1), (PX1, PY1), (PX1, PY0)], fill=NAVY, width=8, joint="curve")
    d.line([(PX0 - 24, PY0), (PX0, PY0)], fill=NAVY, width=8); d.line([(PX1, PY0), (PX1 + 24, PY0)], fill=NAVY, width=8)
    # hoi nuoc khi nong
    if h > 0.6:
        sa = clamp((h - 0.6) / 0.4)
        for x, ph0 in STEAM:
            q = (ph0 + t * 0.5) % 1
            y = PY0 + 30 - q * 120
            pts = [(x + 10 * math.sin((y - k * 10) / 18 + ph0 * 6), y - k * 10) for k in range(5)]
            d.line(pts, fill=A((160, 165, 180), sa * (1 - q)), width=5)
    # binh kim loai kin + hat khi
    d.rounded_rectangle([BX0, BY0, BX1, BY1], radius=26, fill=mix((225, 232, 245), (255, 225, 210), h), outline=(70, 78, 100), width=8)
    sp = math.sqrt((tc + 273) / T0)                # v ∝ √T
    for (ux, uy, vx, vy) in PART:
        x = BX0 + 24 + refl(ux + vx * t * sp, 0, 1) * (BX1 - BX0 - 48)
        y = BY0 + 24 + refl(uy + vy * t * sp, 0, 1) * (BY1 - BY0 - 100)   # chua vung nhan the tich o day binh
        dot(d, x, y, 8, mix(BLUE, RED, h))
    text(d, ((BX0 + BX1) / 2, BY1 - 34), f"{V_BINH} lít", 30, NAVY)
    # ong noi binh -> ap ke
    cx = (BX0 + BX1) / 2
    d.line([(cx, BY0), (cx, 470), (640, 470)], fill=GRAY, width=14, joint="curve")
    # que khuay
    d.line([(500, 520), (460, 880)], fill=(160, 120, 80), width=10)
    # nhiet ke: cot chat long theo nhiet do (0-100 C)
    d.rounded_rectangle([TX - 14, TTOP, TX + 14, TBULB], radius=14, fill=WHITE, outline=NAVY, width=4)
    dot(d, TX, TBULB + 14, 24, RED, NAVY)
    lvl = lerp(TBULB - 40, TTOP + 30, tc / 100)
    d.rectangle([TX - 6, lvl, TX + 6, TBULB], fill=RED)
    # man hinh ap ke dien tu
    card(d, (640, 270, 1010, 560), fill=WHITE, outline=LIGHT, r=28, w=4)
    text(d, (825, 318), "Áp kế", 34, MUTED, bold=False)
    d.rounded_rectangle([670, 352, 980, 466], radius=16, fill=NAVY)
    text(d, (825, 410), p_lbl, 62, (134, 239, 172))
    text(d, (825, 512), "kPa", 34, MUTED, bold=False)
    # man hinh nhiet ke
    card(d, (640, 600, 1010, 890), fill=WHITE, outline=LIGHT, r=28, w=4)
    text(d, (825, 648), "Nhiệt kế", 34, MUTED, bold=False)
    d.rounded_rectangle([670, 682, 980, 796], radius=16, fill=WHITE, outline=NAVY, width=4)
    text(d, (825, 740), t_lbl, 62, RED)
    text(d, (825, 842), "°C", 34, MUTED, bold=False)

# ---------------- canh 1: mo bai + du doan ----------------
OPTS = ("A. 96 kPa", "B. 123 kPa", "C. 192 kPa", "D. 864 kPa")
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    rig(d, t, 10, f1(ROWS[0][2]), str(ROWS[0][0]))
    k = appear(t, sc["M"][1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (60, 1000, 1020, 1600), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 1055), "Dự đoán", 46, PURPLE, alpha=k)
    ctext(d, 1155, "Đun từ 10 °C lên 90 °C.\nÁp kế chỉ bao nhiêu?", 42, INK, alpha=k)
    for i, s in enumerate(OPTS):
        a = appear(t, sc["M"][1] + 0.2 + i * 0.15)
        x0 = 110 + (i % 2) * 440; y = 1300 + (i // 2) * 110
        card(d, (x0, y - 44, x0 + 420, y + 44), fill=A((245, 243, 255), a), outline=A(PURPLE, a), r=22, w=4)
        text(d, (x0 + 40, y), s, 42, INK, anchor="lm", alpha=a)
    t1, t2 = sc["M"][1] + 0.6, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1552, 940, 1566], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1552, 140 + 800 * (1 - q), 1566], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: dun dan, doc p va t, ghi bang ----------------
ROW_T = [0.9, 2.3, 3.6, 4.9, 6.3]      # moc giay (trong canh) hien tung hang; dun 1,0 s truoc moi hang
HEAT = 1.0
def row_at(i): return ROW_T[i]

def do_state(t):
    """(nhiet do de ve, chu ap ke, chu nhiet ke): dang dun thi man hinh hien '···' (khong in so noi suy)."""
    tc, pl, tl = ROWS[0][0], f1(ROWS[0][2]), str(ROWS[0][0])
    for i in range(1, 5):
        s = ROW_T[i] - HEAT
        if t < s: break
        k = ease((t - s) / HEAT)
        tc = lerp(ROWS[i - 1][0], ROWS[i][0], k)
        if t < ROW_T[i]: pl, tl = "···", "···"
        else: pl, tl = f1(ROWS[i][2]), str(ROWS[i][0])
    return tc, pl, tl

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    tc, pl, tl = do_state(t)
    rig(d, t, tc, pl, tl)
    if pl == "···": text(d, (825, 950), "khuấy, đợi số đứng yên", 34, ORANGE)
    card(d, (60, 1010, 1020, 1600), fill=WHITE, outline=NAVY, w=4)
    xs = [200, 480, 760]
    for x, c in zip(xs, ["t (°C)", "T = t + 273 (K)", "p (kPa)"]): text(d, (x, 1060), c, 36, MUTED)
    d.line([(90, 1094), (990, 1094)], fill=LIGHT, width=4)
    last = max([i for i in range(5) if t >= row_at(i)], default=-1)
    for i, (tt, TK, p, _) in enumerate(ROWS):
        a = appear(t, row_at(i), 0.35); y = 1140 + i * 76
        if a <= 0: continue
        if i == last: d.rounded_rectangle([80, y - 32, 1000, y + 32], radius=16, fill=A((225, 236, 255), a))
        for x, s, col in zip(xs, [str(tt), str(TK), f1(p)], [RED, MUTED, BLUE]):
            text(d, (x, y), s, 44, col, alpha=a)
        if i == 4: text(d, (970, y), "→ B", 40, GREEN, anchor="rm", alpha=a)

# ---------------- canh 3: dap an + do thi p-T + ti so p/T ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k = back((t - 0.2) / 0.5) if t > 0.2 else 0
    card(d, (60, 250, 1020, 350), fill=(220, 252, 231), outline=GREEN, w=5)
    text(d, (W / 2, 300), f"Đáp án B: {f1(ROWS[0][2])} → {f1(ROWS[4][2])} kPa", int(44 * clamp(k, 0.3, 1.0)), GREEN)
    x0, x1, yb, yt = 190, 950, 960, 470
    X = lambda T: x0 + T / 400 * (x1 - x0); Y = lambda p: yb - p / 140 * (yb - yt)
    card(d, (60, 380, 1020, 1060), fill=WHITE, outline=LIGHT, w=3)
    for p in (40, 80, 120): d.line([(x0, Y(p)), (x1, Y(p))], fill=(240, 236, 228), width=2)
    d.line([(x0, yb), (x1 + 25, yb)], fill=NAVY, width=5); d.line([(x0, yb), (x0, yt - 40)], fill=NAVY, width=5)
    text(d, (x0 + 18, yt - 50), "p (kPa)", 36, MUTED, anchor="lm")
    text(d, (x1 + 25, yb + 76), "T (K)", 36, MUTED, anchor="rm")
    text(d, (x0 - 26, yb + 30), "O", 36, MUTED)
    for T in (100, 200, 300, 400):
        d.line([(X(T), yb), (X(T), yb + 10)], fill=NAVY, width=3)
        text(d, (X(T), yb + 36), str(T), 34, MUTED, bold=False)
    for p in (40, 80, 120):
        d.line([(x0 - 10, Y(p)), (x0, Y(p))], fill=NAVY, width=4); text(d, (x0 - 18, Y(p)), str(p), 34, MUTED, bold=False, anchor="rm")
    # duong thang qua goc (ve sau khi co diem)
    kl = ease((t - M[1] - 0.2) / 1.2)
    if kl > 0:
        Te = 400 * kl
        for j in range(0, 40):
            a_, b_ = Te * j / 40, Te * (j + 0.55) / 40
            d.line([(X(a_), Y(model(a_))), (X(b_), Y(model(b_)))], fill=A(BLUE, 0.6), width=6)
        dot(d, X(0), Y(0), 10, BLUE)
    for i, (_, TK, p, _) in enumerate(ROWS):
        a = appear(t, 0.5 + i * 0.2, 0.4)
        if a > 0: dot(d, X(TK), Y(p), 15 * back(a), ORANGE, WHITE)
    # bang ti so p/T
    a1 = appear(t, M[1] + 1.2)
    if a1 <= 0: return
    card(d, (60, 1090, 1020, 1600), fill=A(WHITE, a1), outline=A(LIGHT, a1), w=3)
    text(d, (W / 2, 1140), "p/T mỗi mốc", 38, MUTED, alpha=a1)
    xs = [260 + i * 160 for i in range(5)]
    text(d, (150, 1225), "T (K)", 34, MUTED, alpha=a1)
    text(d, (150, 1320), "p/T", 34, MUTED, alpha=a1)
    band = appear(t, M[1] + 3.2, 0.4)
    if band > 0: d.rounded_rectangle([190, 1280, 1000, 1360], radius=20, fill=A((187, 247, 208), band))
    for i, (_, TK, _, r) in enumerate(ROWS):
        text(d, (xs[i], 1225), str(TK), 38, INK, alpha=a1)
        text(d, (xs[i], 1320), f4(r), 36, GREEN, alpha=appear(t, M[1] + 1.5 + i * 0.2, 0.3))
    ctext(d, 1460, "p/T ≈ 0,339 kPa/K\n→ p tỉ lệ thuận T", 40, GREEN, alpha=band, lh=1.3)

# ---------------- canh 4: co che + chua noi duoc gi ----------------
RB = random.Random(9)
MOL = [(RB.random(), RB.random(), RB.uniform(0, 2 * math.pi)) for _ in range(14)]
def box(d, t, x0, x1, y0, y1, TK, p, col, a):
    sp = 170 * math.sqrt(TK / T0)                 # toc do ti le can T (v ∝ √T)
    d.rectangle([x0, y0, x1, y1], fill=A((246, 249, 255), a), outline=A(NAVY, a), width=5)
    L, Hh = x1 - x0 - 24, y1 - y0 - 24
    for (ux, uy, ang) in MOL:
        vx, vy = sp * math.cos(ang), sp * math.sin(ang)
        x = x0 + 12 + refl(ux * L + vx * t, 0, L); y = y0 + 12 + refl(uy * Hh + vy * t, 0, Hh)
        dot(d, x, y, 10, A(col, a))
        if x - x0 < 22 or x1 - x < 22 or y - y0 < 22 or y1 - y < 22:
            dot(d, x, y, 18, A(YELLOW, 0.6 * a))
            dot(d, x, y, 10, A(col, a))
    text(d, ((x0 + x1) / 2, y0 - 36), f"{TK} K", 42, col, alpha=a)
    text(d, ((x0 + x1) / 2, y1 + 44), f"p = {f1(p)} kPa", 40, col, alpha=a)

def s_why(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.1, 0.4)
    box(d, t, 90, 510, 330, 720, ROWS[0][1], ROWS[0][2], BLUE, a)
    box(d, t, 570, 990, 330, 720, ROWS[4][1], ROWS[4][2], RED, a)
    text(d, (W / 2, 830), "cùng N, cùng V", 36, MUTED, bold=False, alpha=a)
    b = appear(t, M[1] - 0.2)
    card(d, (60, 880, 1020, 1160), fill=A(WHITE, b), outline=A(BLUE, b), w=5)
    rich(d, W / 2, 960, "p = (2/3)·μ·E_{d}, μ không đổi", 42, INK, alpha=b)
    rich(d, W / 2, 1075, "→ E_{d} = (3/2)kT, tỉ lệ T", 46, BLUE, alpha=appear(t, M[1] + 0.8))
    c = appear(t, M[1] + 2.6)
    card(d, (60, 1200, 1020, 1600), fill=A(WHITE, c), outline=A(PURPLE, c), w=5)
    text(d, (W / 2, 1260), "Chưa nói được gì?", 42, PURPLE, alpha=c)
    ctext(d, 1375, "Chỉ đo p và t.", 38, INK, alpha=c)
    ctext(d, 1480, "Tốc độ, động năng: chỉ suy ra.", 38, MUTED, bold=False, alpha=c, lh=1.25)

# ---------------- canh 5: bay dung do C ----------------
def s_trap(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    card(d, (60, 250, 1020, 340), fill=(254, 226, 226), outline=RED, w=5)
    text(d, (W / 2, 295), "Bẫy: xét tỉ lệ theo độ C", 44, RED, alpha=appear(t, 0.1))
    x0, x1, yb, yt = 190, 950, 960, 470
    X = lambda tc: x0 + tc / 100 * (x1 - x0); Y = lambda p: yb - p / 140 * (yb - yt)
    card(d, (60, 380, 1020, 1060), fill=WHITE, outline=LIGHT, w=3)
    for p in (40, 80, 120): d.line([(x0, Y(p)), (x1, Y(p))], fill=(240, 236, 228), width=2)
    d.line([(x0, yb), (x1 + 25, yb)], fill=NAVY, width=5); d.line([(x0, yb), (x0, yt - 40)], fill=NAVY, width=5)
    text(d, (x0 + 18, yt - 50), "p (kPa)", 36, MUTED, anchor="lm")
    text(d, (x1 + 25, yb + 76), "t (°C)", 36, MUTED, anchor="rm")
    text(d, (x0 - 26, yb + 30), "O", 36, MUTED)
    for tc in (20, 40, 60, 80, 100):
        d.line([(X(tc), yb), (X(tc), yb + 10)], fill=NAVY, width=3)
        text(d, (X(tc), yb + 36), str(tc), 34, MUTED, bold=False)
    for p in (40, 80, 120):
        d.line([(x0 - 10, Y(p)), (x0, Y(p))], fill=NAVY, width=4); text(d, (x0 - 18, Y(p)), str(p), 34, MUTED, bold=False, anchor="rm")
    for i, (tc, _, p, _) in enumerate(ROWS):
        a = appear(t, 0.4 + i * 0.15, 0.4)
        if a > 0: dot(d, X(tc), Y(p), 15 * back(a), ORANGE, WHITE)
    kl = ease((t - M[1]) / 1.0)                    # keo dai duong thang ve t = 0 C
    if kl > 0:
        te = lerp(100, 0, kl)
        for j in range(40):
            a_ = lerp(100, te, j / 40); b_ = lerp(100, te, (j + 0.55) / 40)
            d.line([(X(a_), Y(model(a_ + 273))), (X(b_), Y(model(b_ + 273)))], fill=A(RED, 0.7), width=6)
    ci = appear(t, M[1] + 0.9, 0.3)
    if ci > 0:
        yi = Y(model(273))
        d.ellipse([x0 - 26, yi - 26, x0 + 26, yi + 26], outline=A(RED, ci), width=6)
        text(d, (x0 + 40, yi + 70), "t = 0 °C, p chưa về 0", 38, RED, anchor="lm", alpha=ci)
    c = appear(t, M[1] + 0.15, 0.3)
    card(d, (60, 1100, 1020, 1330), fill=A((254, 242, 242), c), r=28)
    ctext(d, 1215, "p KHÔNG tỉ lệ thuận với t", 46, RED, alpha=c)
    e = appear(t, M[1] + 2.2)
    card(d, (60, 1370, 1020, 1600), fill=A((220, 252, 231), e), r=28)
    ctext(d, 1485, "Đúng: T = t + 273", 40, GREEN, alpha=e, lh=1.25)

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    chot_hoi(d, t, sc, "V không đổi: p tỉ lệ thuận T",
             "Đun bình kín từ 0 °C lên 100 °C. Áp suất tăng gấp đôi không?")
    kh = appear(t, M[0] + 1.2, 0.5)            # o goi y tu ve: chu "Gợi ý" to, dam hon ban trong engine
    if kh <= 0: return
    card(d, (110, 1060, 970, 1270), fill=A((255, 237, 213), kh), outline=A(ORANGE, kh), r=24, w=4)
    text(d, (W / 2, 1115), "Gợi ý", 40, ORANGE, alpha=kh)
    ctext(d, 1198, "Đổi hai nhiệt độ sang kelvin rồi so", 42, INK, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + row_at(4), "ding"), (an["t0"] + an["M"][1] + 3.2, "tap"),
            (tr["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l12-apsuatdongnang-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Áp suất – động năng phân tử khí · thachlab.id.vn", scenes=[
 dict(key="hook", title="Đun nóng bình khí kín", draw=s_hook, tail=0.6, caps=[
   ("Bình kín ngâm trong nước.", 2.4),
   ("Chọn một đáp án.", 5.0)]),
 dict(key="do", title="Đun dần, đọc t và p", draw=s_do, tail=0.6, caps=[
   ("Nước nóng dần.", 5.5),
   ("90 °C: 123,0 kPa.", 3.2)]),
 dict(key="ans", title="Đồ thị p–T và tỉ số p/T", draw=s_ans, tail=0.6, caps=[
   ("Thẳng hàng, qua gốc O.", 2.8),
   ("p/T gần như không đổi.", 5.4)]),
 dict(key="why", title="Vì sao p tăng?", draw=s_why, tail=0.6, caps=[
   ("Nóng hơn: phân tử nhanh hơn.", 2.8),
   ("Va chạm mạnh hơn → p tăng.", 5.4)]),
 dict(key="trap", title="Cái bẫy", draw=s_trap, tail=0.6, caps=[
   ("Thử lập tỉ lệ theo °C.", 2.8),
   ("Đường thẳng không qua O.", 5.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Áp suất ra sao?", 5.0)]),
])
