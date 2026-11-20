# Clip: tn-l12-pttrangthai-02 - Binh kin ngam nuoc o nam nhiet do: p/T khong doi
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-pttrangthai-02.json (so_lieu_mau, mo_hinh, hien_tuong_hay_sai).
# Ban 2 (21/11/2026, viec 4 lo 20, KE-HOACH-CAI-TIEN-CLIP): danh quan niem sai "chia p cho t (do C)".
#   Du doan: t 25 -> 100 C (gap 4), p tang gap may? -> dap an "chua toi 1,5 lan" (108,9 -> 136,3 kPa); khung web hoi A-D,
#   clip khong ve nut (K10). Ket qua: ba cap cot t / p / T -> cot p giong cot T, khong giong cot t. Bang p/T ~ 0,366.
#   Bay: hai bang ngang canh nhau, p/t (do C) giam 4,36 -> 1,36 (o 0 C chia cho 0) va p/T dung yen -> ket luan
#   "p khong ti le nhiet do" SAI. Chot (THU NGHI): nuoc 60 C, ap ke chi? (= 0,366 x 333 ~ 122 kPa, khong hien tren man).
#   Chu than canh >= 56 px (ra >= 49 px), khong chu xam, moi nhip >= 3 s mot phu de, dem nguoc 5 cham.
# Ban 1 (28/10/2026): mau boyle (dung cu + bang + do thi), Du doan "dai luong nao khong doi".
import random
from engine import *

ROWS = [(0, 273, 100.0, 0.366), (25, 298, 108.9, 0.365), (50, 323, 118.4, 0.367),
        (75, 348, 126.9, 0.365), (100, 373, 136.3, 0.365)]      # so_lieu_mau: t (C), T (K), p (kPa), p/T (kPa/K)
# Bay: p/t (do C) suy thang tu so_lieu_mau (kho hien_tuong_hay_sai: 4,36 -> 1,36); 0 C -> chia cho 0
P_TC = [None] + [round(p / tc, 2) for tc, _, p, _ in ROWS[1:]]
def f1(v): return f"{v:.1f}".replace(".", ",")
def f2(v): return f"{v:.2f}".replace(".", ",")
def f3(v): return f"{v:.3f}".replace(".", ",")
DARK_OR = (181, 71, 8)                   # chu cam tren nen sang >= 4,5:1

# ---------------- dung cu: 5 chau nuoc + binh tam giac kin + nhiet ke + dong ho ----------------
BXS = [135, 337, 540, 743, 945]          # tam 5 chau (mep ngoai 47..1033 -> mp4 106..974)
BT0, BT1, WTOP = 720, 900, 748           # mieng chau, day chau, mat nuoc
FY = 880                                 # day binh khi ngam
R = random.Random(5)
PART = [(R.random(), R.random(), R.choice((-1, 1)) * R.uniform(0.3, 0.5), R.choice((-1, 1)) * R.uniform(0.3, 0.5))
        for _ in range(12)]
BUB = [(R.uniform(-60, 60), R.random()) for _ in range(7)]

def heat(tc): return clamp(tc / 100)
def water(tc): return mix((191, 219, 254), (254, 196, 160), heat(tc))

def bath(d, t, cx, tc, label=True):
    d.rectangle([cx - 88, WTOP, cx + 88, BT1], fill=water(tc))
    if tc == 0:                                    # nuoc da dang tan
        for dx, dy in ((-52, 6), (34, 2), (-8, 14)):
            d.rounded_rectangle([cx + dx, WTOP + dy, cx + dx + 26, WTOP + dy + 22], radius=5, fill=WHITE, outline=(140, 170, 210), width=3)
    if tc == 100:                                  # nuoc dang soi: bot khi noi len
        for dx, ph in BUB:
            q = (ph + t * 0.8) % 1
            d.ellipse([cx + dx - 7, BT1 - 12 - q * 140 - 7, cx + dx + 7, BT1 - 12 - q * 140 + 7], outline=WHITE, width=3)
    d.line([(cx - 88, BT0), (cx - 88, BT1), (cx + 88, BT1), (cx + 88, BT0)], fill=NAVY, width=6, joint="curve")
    if label: text(d, (cx, BT1 + 46), f"{tc} °C", 56, INK)

def flask(d, t, fx, fy, tc, tube_to=(730, 466)):
    """fx: tam binh; fy: day binh. Binh tam giac day nut, ong mem len ap ke, nhiet ke gan ben phai."""
    body = [(fx - 54, fy), (fx + 54, fy), (fx + 24, fy - 112), (fx + 24, fy - 166), (fx - 24, fy - 166), (fx - 24, fy - 112)]
    d.polygon(body, fill=(236, 242, 252), outline=(70, 78, 100))
    d.line(body + [body[0]], fill=(70, 78, 100), width=6, joint="curve")
    sp = math.sqrt((tc + 273) / 273)               # v ti le can T
    for (ux, uy, vx, vy) in PART:
        yy = fy - 16 - refl(uy + vy * t * sp, 0, 1) * 88
        half = lerp(42, 18, (fy - 16 - yy) / 96)
        x = fx + (refl(ux + vx * t * sp, 0, 1) * 2 - 1) * half
        dot(d, x, yy, 8, mix(BLUE, RED, heat(tc)))
    d.rounded_rectangle([fx - 30, fy - 190, fx + 30, fy - 162], radius=6, fill=NAVY)   # nut
    p0, p2 = (fx, fy - 190), tube_to; p1 = (fx, (p0[1] + p2[1]) / 2)
    pts = [((1 - s) ** 2 * p0[0] + 2 * (1 - s) * s * p1[0] + s * s * p2[0],
            (1 - s) ** 2 * p0[1] + 2 * (1 - s) * s * p1[1] + s * s * p2[1]) for s in [k / 24 for k in range(25)]]
    d.line(pts, fill=GRAY, width=12, joint="curve")
    tx = fx + 62                                   # nhiet ke canh binh, bau khong cham day chau
    d.rounded_rectangle([tx - 8, fy - 230, tx + 8, fy - 30], radius=8, fill=WHITE, outline=NAVY, width=3)
    dot(d, tx, fy - 24, 10, RED, NAVY)
    d.rectangle([tx - 4, lerp(fy - 50, fy - 215, heat(tc)), tx + 4, fy - 30], fill=RED)

def readout(d, t_lbl, p_lbl, p_col=(134, 239, 172), nhan=True):
    card(d, (120, 240, 960, 470), fill=WHITE, outline=LIGHT, r=28, w=4)
    if nhan:
        text(d, (330, 284), "Nhiệt kế", 56, NAVY)
        text(d, (750, 284), "Áp kế", 56, NAVY)
    d.rounded_rectangle([160, 330, 500, 450], radius=16, fill=WHITE, outline=NAVY, width=4)
    text(d, (330, 390), t_lbl, 64, RED)
    d.rounded_rectangle([580, 330, 920, 450], radius=16, fill=NAVY)
    text(d, (750, 390), p_lbl, 64, p_col)

def rig(d, t, fx, fy, tc, t_lbl, p_lbl):
    for i in range(5): bath(d, t, BXS[i], ROWS[i][0])
    flask(d, t, fx, fy, tc)
    readout(d, t_lbl, p_lbl)

def lbl_t(i): return f"{ROWS[i][0]} °C"
def lbl_p(i): return f"{f1(ROWS[i][2])} kPa"

def pill(d, s, cx, cy, col, k, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(col, k), r=40)
    text(d, (cx, cy), s, size, WHITE, alpha=k)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, t, BXS[1], FY, 25, lbl_t(1), lbl_p(1))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 650), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", W / 2, y0 + 70, PURPLE, a)
    text(d, (W / 2, y0 + 190), "Nhiệt độ: 25 → 100 °C", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 280), "Số chỉ °C gấp 4.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 390), "Áp suất tăng gấp mấy?", 62, INK, alpha=a)   # K10: khong ve nut A-D
    tc, tend = M[1] + 0.3, sc["T"] - 0.1                   # dem nguoc 5 cham, moi cham tat sau ~1 s
    n_off = 0 if t < tc else min(5, int((t - tc) / ((tend - tc) / 5)) + 1)
    for j in range(5):
        dot(d, W / 2 + (j - 2) * 140, y0 + 505, 40, A(LIGHT, a) if j >= 5 - n_off else A(PURPLE, a))

# ---------------- canh 2: ngam lan luot 5 chau, doc t va p ----------------
ROW_T = [0.4, 1.4, 2.4, 3.4, 4.4]      # moc (trong canh) hien tung hang
MOVE = 0.9                              # nhac binh sang chau ke trong 0,9 s truoc moi hang

def pose(t):
    """(x binh, y day binh, nhiet do khi de ve, nhan nhiet ke, nhan ap ke). Dang chuyen thi hien '···'."""
    fx, fy, tc, tl, pl = BXS[0], FY, 0, lbl_t(0), lbl_p(0)
    for i in range(1, 5):
        s = ROW_T[i] - MOVE
        if t < s: break
        k = clamp((t - s) / (MOVE - 0.15))
        fx = lerp(BXS[i - 1], BXS[i], ease(clamp((k - 0.25) / 0.5)))
        fy = FY - 150 * math.sin(math.pi * k)
        tc = lerp(ROWS[i - 1][0], ROWS[i][0], ease(k))
        if t < ROW_T[i]: tl, pl = "···", "···"
        else: tl, pl = lbl_t(i), lbl_p(i)
    return fx, fy, tc, tl, pl

def s_do(img, d, t, sc):
    fx, fy, tc, tl, pl = pose(t)
    rig(d, t, fx, fy, tc, tl, pl)
    card(d, (60, 1005, 1020, 1680), fill=WHITE, outline=NAVY, w=4)
    xs = [330, 750]
    for x, c in zip(xs, ["t (°C)", "p (kPa)"]): text(d, (x, 1062), c, 58, NAVY)
    d.line([(100, 1105), (980, 1105)], fill=LIGHT, width=4)
    last = max([i for i in range(5) if t >= ROW_T[i]], default=-1)
    for i, (tt, _, p, _) in enumerate(ROWS):
        a = appear(t, ROW_T[i], 0.3); y = 1160 + i * 100
        if a <= 0: continue
        if i == last: d.rounded_rectangle([90, y - 42, 990, y + 42], radius=16, fill=A((225, 236, 255), a))
        text(d, (xs[0], y), str(tt), 60, RED, alpha=a)
        text(d, (xs[1], y), f1(p), 60, BLUE, alpha=a)

# ---------------- canh 3: Dap an - ba cap cot t / p / T ----------------
GX = [200, 540, 880]                    # tam nhom cot: t (C), p (kPa), T (K)
BASE, HB = 1130, 560                    # day cot, chieu cao cot lon nhat
def pair(d, gx, lo, hi, s_lo, s_hi, col, lab, k, grow=1.0):
    if k <= 0: return
    for dx, v, s in ((-75, lo, s_lo), (75, hi, s_hi)):
        h = HB * v / hi * grow
        d.rounded_rectangle([gx + dx - 40, BASE - h, gx + dx + 40, BASE], radius=10, fill=A(col, k))
        text(d, (gx + dx, BASE - h - 42), s, 56, col, alpha=k * clamp(grow * 3 - 2))
    text(d, (gx, BASE + 52), lab, 60, NAVY, alpha=k)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, M[0] + 0.1, 0.4)
    if ka > 0: pill(d, "ĐÁP ÁN: chưa tới 1,5 lần", W / 2, 292, NAVY, ka)
    card(d, (40, 360, 1040, 1230), fill=WHITE, outline=NAVY, w=3)
    pair(d, GX[0], 25, 100, "25", "100", RED, "t (°C)", 1.0)
    pair(d, GX[1], 108.9, 136.3, "108,9", "136,3", BLUE, "p (kPa)", 1.0)
    if ka > 0: text(d, (75, 425), "Số chỉ °C gấp 4", 56, RED, anchor="lm", alpha=ka)   # so chi, khong phai "nong gap 4"
    kT = appear(t, M[1] - 0.1, 0.4)
    pair(d, GX[2], 298, 373, "298", "373", TEAL, "T (K)", kT, grow=ease((t - M[1] + 0.1) / 0.8))
    if kT > 0:                                                  # vien cam om hai cap p va T giong nhau
        kk = appear(t, M[1] + 0.9, 0.4)
        d.rounded_rectangle([GX[1] - 125, 485, GX[2] + 150, 1215], radius=26, outline=A(ORANGE, kk), width=7)
        card(d, (40, 1270, 1040, 1440), fill=A((236, 253, 243), kT), outline=A(GREEN, kT), w=5)
        text(d, (W / 2, 1355), "T = t + 273", 68, INK, alpha=kT)

# ---------------- canh 4: Bang p/T ----------------
XS4 = [160, 385, 615, 870]
def s_pt(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 250, 1040, 1080), fill=WHITE, outline=NAVY, w=4)
    band = appear(t, M[0] + 0.1, 0.4)
    if band > 0: d.rounded_rectangle([745, 268, 1000, 1062], radius=20, fill=A((187, 247, 208), band))
    for x, c, u in zip(XS4, ["t", "T", "p", "p/T"], ["°C", "K", "kPa", "kPa/K"]):
        text(d, (x, 310), c, 62, NAVY); text(d, (x, 378), u, 56, NAVY)
    d.line([(70, 420), (1010, 420)], fill=LIGHT, width=4)
    for i, (tt, TK, p, r) in enumerate(ROWS):
        y = 480 + i * 130
        text(d, (XS4[0], y), str(tt), 60, RED)
        text(d, (XS4[1], y), str(TK), 60, TEAL)
        text(d, (XS4[2], y), f1(p), 60, BLUE)
        text(d, (XS4[3], y), f3(r), 60, GREEN, alpha=appear(t, M[0] + 0.3 + i * 0.3, 0.3))
    c = appear(t, M[1] - 0.1, 0.4)
    if c <= 0: return
    card(d, (40, 1120, 1040, 1440), fill=A((236, 253, 243), c), outline=A(GREEN, c), w=5)
    text(d, (W / 2, 1205), "p/T ≈ 0,366 kPa/K", 66, GREEN, alpha=c)
    text(d, (W / 2, 1335), "p tỉ lệ thuận với T (K)", 62, INK, alpha=c)

# ---------------- canh 5: Bay - p/t (do C) canh p/T (K) ----------------
def panel(d, x0, x1, head, unit, labs, vals, strs, vmax, col, k, grow, lmax=210):
    if k <= 0: return
    card(d, (x0, 380, x1, 1060), fill=A(WHITE, k), outline=A(col, k), w=5)
    text(d, ((x0 + x1) / 2, 440), head, 60, col, alpha=k)
    text(d, ((x0 + x1) / 2, 510), unit, 56, NAVY, alpha=k)
    for i, (lb, v, s) in enumerate(zip(labs, vals, strs)):
        y = 620 + i * 100
        text(d, (x0 + 65, y), lb, 56, NAVY, alpha=k)
        bx = x0 + 130
        if v is None:
            text(d, (bx + 10, y), s, 56, col, anchor="lm", alpha=k * clamp(grow * 3 - 2)); continue
        L = lmax * v / vmax * grow
        d.rounded_rectangle([bx, y - 24, bx + L, y + 24], radius=8, fill=A(col, k))
        text(d, (bx + L + 12, y), s, 56, col, anchor="lm", alpha=k * clamp(grow * 3 - 2))

def s_bay(img, d, t, sc):
    M = sc["M"]; b1, b2, b3 = (m - 0.1 for m in M)
    k1 = appear(t, b1, 0.4)
    pill(d, "BẪY", W / 2, 292, RED, k1)
    panel(d, 40, 610, "p/t (kPa/°C)", "(t tính °C)", [str(r[0]) for r in ROWS], [None] + P_TC[1:],
          ["÷ 0: không chia"] + [f2(v) for v in P_TC[1:]], max(P_TC[1:]), RED, k1, ease((t - b1) / 1.2))
    k2 = appear(t, b2, 0.4)
    if k2 > 0:
        card(d, (40, 1085, 1040, 1345), fill=A((254, 242, 242), k2), outline=A(RED, k2), w=5)
        text(d, (90, 1150), "Từ cột p/t, suy ra:", 58, INK, anchor="lm", alpha=k2)
        text(d, (90, 1270), "“p không tỉ lệ nhiệt độ”", 58, INK, anchor="lm", alpha=k2)
        pill(d, "SAI", 945, 1270, RED, k2)
    k3 = appear(t, b3, 0.4)
    panel(d, 630, 1040, "p/T (kPa/K)", "(T tính K)", [str(r[1]) for r in ROWS], [r[3] for r in ROWS],
          [f3(r[3]) for r in ROWS], 0.367, GREEN, k3, ease((t - b3) / 1.0), lmax=100)
    if k3 > 0:
        card(d, (40, 1380, 1040, 1560), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
        text(d, (W / 2, 1470), "Cột p/T: các thanh bằng nhau", 58, GREEN, alpha=k3)

# ---------------- canh 6: Chua noi duoc gi ----------------
def s_gioi(img, d, t, sc):
    M = sc["M"]; k = appear(t, 0.0, 0.3)
    card(d, (40, 300, 1040, 1300), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    for j, s in enumerate(("• Chưa đo ngoài 0–100 °C", "• Chưa thử đổi lượng khí")):   # hien lan luot, moi gach mot nhip
        text(d, (100, 560 + j * 300), s, 60, INK, anchor="lm", alpha=appear(t, M[j] - 0.1, 0.4))
    text(d, (W / 2, 1150), "?", 160, NAVY, alpha=k * (1 - appear(t, M[1] - 0.1, 0.4)))

# ---------------- canh 7: THU NGHI ----------------
def s_end(img, d, t, sc):
    bath(d, t, W / 2, 60, label=False)
    flask(d, t, W / 2, FY, 60, tube_to=(750, 466))
    readout(d, "60 °C", "? kPa", p_col=(253, 186, 116), nhan=False)
    k = 1.0
    card(d, (50, 1000, 1030, 1400), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, "CÂU HỎI", W / 2, 1070, DARK_OR, k)
    text(d, (W / 2, 1200), "Ngâm vào nước 60 °C,", 62, INK, alpha=k)
    text(d, (W / 2, 1310), "áp kế chỉ khoảng?", 62, DARK_OR, alpha=k)
    kh = appear(t, 2.9, 0.5)                                  # goi y hien tre ~2,6 s
    if kh <= 0: return
    card(d, (50, 1440, 1030, 1640), fill=A((255, 237, 213), kh), outline=A(ORANGE, kh), r=24, w=4)
    text(d, (W / 2, 1540), "Gợi ý: °C hay K?", 60, INK, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, pt, b, g, e = (sc[k] for k in ("hook", "do", "dapan", "pt", "bay", "gioi", "end"))
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + s, "tick") for s in ROW_T]
            + [(da["t0"] + da["M"][0] + 0.1, "ding"), (pt["t0"] + pt["M"][1] - 0.1, "tap"),
               (b["t0"] + b["M"][0] - 0.1, "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"), (g["t0"] + g["M"][1] - 0.1, "tap"),
               (e["t0"] + 0.1, "open")])

CLIP = dict(id="tn-l12-pttrangthai-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Phương trình trạng thái khí lí tưởng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Bình kín qua năm chậu nước", draw=s_hook, tail=0.3, caps=[
   ("Bình kín.", 2.5),
   ("Dừng lại, tự đoán.", 5.1)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Đo ở năm mức nhiệt độ.", 3.0),
   ("Càng nóng, p càng lớn.", 2.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Số °C gấp 4, p thì không.", 3.0),
   ("Đổi kelvin: cột T giống cột p.", 3.2)]),
 dict(key="pt", title="Chia p cho T", draw=s_pt, tail=0.3, caps=[
   ("Chia p cho T từng dòng.", 2.6),
   ("Cột p/T gần như yên.", 2.6)]),
 dict(key="bay", title="Bẫy", draw=s_bay, tail=0.3, caps=[
   ("Chia p cho t (°C) thì sao?", 3.0),
   ("Kết luận chung này sai.", 3.0),
   ("Phải chia cho T (K).", 3.0)]),
 dict(key="gioi", title="Chưa nói được gì?", draw=s_gioi, tail=0.3, caps=[
   ("Còn hai chỗ hở.", 2.6),
   ("Cần thí nghiệm khác.", 3.0)]),
 dict(key="end", title="Tự kiểm tra", draw=s_end, tail=0.5, caps=[
   ("Dừng lại, tự trả lời.", 5.3)]),
])
