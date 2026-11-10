# Clip: tn-l12-dttruong-02 - Dong xoay chieu "di qua" tu dien: dien truong bien thien tuong duong dong dien dich
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-dttruong-02.json (so_lieu_mau, tham_so, mo_hinh).
# Ban 1 (28/10/2026): mau boyle (dung cu + bang + do thi), tieng bao cues nhu phongxa2.
# Hinh: dien tich chi dao dong trong DAY va tich tren hai ban; giua hai ban chi ve mui ten E (khong ve hat qua dien moi).
from engine import *

ROWS = [(50, "3,6"), (100, "7,4"), (200, "14,8"), (400, "29,5"), (800, "58,0")]   # so_lieu_mau: f (Hz), I do (mA)
IV = [3.6, 7.4, 14.8, 29.5, 58.0]
RATIO = ["0,072", "0,074", "0,074", "0,074", "0,073"]   # I/f (mA/Hz) = cot 2 / cot 1, lam tron 3 so le (nhu bang trong bai)
U, C_UF = 12, "1,0"                                      # tham_so: U = 12 V, C = 1,0 uF
K_MODEL = 0.0754                                         # mo_hinh: I = 0,0754*f (mA) voi U = 12 V, C = 1,0 uF

# ---------------- dung cu: may phat + tu + dong ho ----------------
WY = 880                              # do cao day duoi
PL, PR = 492, 588                     # mat trong ban trai / ban phai (giua: dien moi)
PT, PB = 790, 970                     # mep tren / duoi hai ban
GXW, AXW = 270, 810                   # day doc o may phat / dong ho
AMP = 22                              # bien do dich chuyen cua dien tich trong day (px)

LEFT = [(GXW, 600), (GXW, WY), (PL - 26, WY)]
RIGHT = [(PR + 26, WY), (AXW, WY), (AXW, 600)]

def _path_len(p): return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(p, p[1:]))
def _at(p, s):
    for a, b in zip(p, p[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if s <= L: return a[0] + (b[0] - a[0]) * s / L, a[1] + (b[1] - a[1]) * s / L
        s -= L
    return p[-1]

def charges(d, path, x, col=BLUE):
    L = _path_len(path); s = AMP + 8
    while s < L - AMP - 8:
        px, py = _at(path, s + x); dot(d, px, py, 9, col); s += 46

def viz_hz(f): return 0.45 * (f / 50) ** 0.35        # nhip nhin thay (dinh tinh): f lon -> dao dong nhanh hon

def plates(d, q, x0=PL, x1=PR, top=PT, bot=PB, th=26, sz=40, lbl_e=True, show_e=True):
    """q in [-1,1]: dien tich ban trai (ban phai trai dau). Mui ten E tu ban + sang ban -, chi o vung tren/duoi day."""
    d.rectangle([x0, top, x1, bot], fill=(255, 243, 214))               # dien moi
    for (a, b), qq in (((x0 - th, x0), q), ((x1, x1 + th), -q)):
        c = mix((205, 210, 222), RED if qq > 0 else BLUE, abs(qq))
        d.rectangle([a, top, b, bot], fill=c, outline=NAVY, width=3)
        n = int(round(abs(qq) * 3))
        for j in range(n):
            text(d, ((a + b) / 2, top + 30 + j * (bot - top - 60) / 2), "+" if qq > 0 else "−", sz, WHITE)
    if show_e and abs(q) > 0.08:
        gy = [top + (bot - top) * 0.2, bot - (bot - top) * 0.2]
        for y in gy:
            p1, p2 = (x0 + 10, y), (x1 - 10, y)
            if q < 0: p1, p2 = p2, p1
            arrow(d, p1, p2, A(ORANGE, clamp(abs(q) * 1.3)), w=5, head=14)
        if lbl_e: text(d, ((x0 + x1) / 2, (top + bot) / 2), "E", 36, A(ORANGE, clamp(abs(q) * 1.3)))

def rig(d, t, f, reading, phase=None, dc=False, label=True):
    """f: tan so dang dat; reading: chuoi so tren dong ho; phase: None = may phat chua bat."""
    # day
    d.line(LEFT, fill=GRAY, width=12, joint="curve"); d.line(RIGHT, fill=GRAY, width=12, joint="curve")
    if phase is None: x, q = 0.0, 0.0
    elif dc: x, q = AMP, -1.0
    else:
        s = math.sin(phase); x, q = AMP * s, -s          # e den ban trai -> ban trai am
    plates(d, q)
    charges(d, LEFT, x); charges(d, RIGHT, x)
    if label:
        text(d, ((PL + PR) / 2, 700), f"tụ {C_UF} μF", 40, NAVY)
        if phase is not None: text(d, ((PL + PR) / 2, 750), "mũi tên cam: E", 40, ORANGE)
    # may phat
    card(d, (70, 270, 470, 600), fill=WHITE, outline=NAVY, r=28, w=5)
    text(d, (270, 305), "Máy phát", 36, MUTED, bold=False)
    d.rounded_rectangle([100, 335, 440, 455], radius=14, fill=NAVY)
    if phase is not None:
        if dc: d.line([(120, 375), (420, 375)], fill=(134, 239, 172), width=5)
        else:
            cyc = 1 + math.log2(f / 50); pts = []
            for j in range(121):
                u = j / 120; pts.append((120 + 300 * u, 395 - 40 * math.sin(2 * math.pi * cyc * u + phase)))
            d.line(pts, fill=(134, 239, 172), width=5, joint="curve")
    text(d, (270, 505), "một chiều" if dc else f"{f} Hz", 52, BLUE)
    text(d, (270, 562), f"U = {U} V", 36, MUTED, bold=False)
    # dong ho
    card(d, (610, 270, 1010, 600), fill=WHITE, outline=NAVY, r=28, w=5)
    text(d, (810, 305), "Đồng hồ đo dòng", 36, MUTED, bold=False)
    d.rounded_rectangle([650, 335, 970, 455], radius=14, fill=NAVY)
    text(d, (810, 397), reading, 66, (134, 239, 172))
    text(d, (810, 505), "mA", 40, RED)

# ---------------- canh 1: mo bai + du doan ----------------
OPTS = ("A. Luôn bằng 0", "B. Giảm khi f tăng", "C. Tăng khi f tăng", "D. Không đổi theo f")
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    rig(d, t, 50, "?", phase=None)
    k = appear(t, sc["M"][1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (60, 990, 1020, 1600), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 1045), "Dự đoán", 46, PURPLE, alpha=k)
    ctext(d, 1135, "Tăng f: 50 → 800 Hz.\nDòng thay đổi thế nào?", 46, INK, alpha=k)
    for i, s in enumerate(OPTS):
        a = appear(t, sc["M"][1] + 0.2 + i * 0.15)
        x0 = 100 + (i % 2) * 450; y = 1290 + (i // 2) * 120
        card(d, (x0, y - 46, x0 + 430, y + 46), fill=A((245, 243, 255), a), outline=A(PURPLE, a), r=22, w=4)
        text(d, (x0 + 30, y), s, 38, INK, anchor="lm", alpha=a)
    t1, t2 = sc["M"][1] + 0.6, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1552, 940, 1566], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1552, 140 + 800 * (1 - q), 1566], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh, ghi bang ----------------
def row_at(i, sc):
    M = sc["M"]
    return [M[1] + 0.1, M[1] + 0.6, M[1] + 1.1, M[2] + 0.1, M[2] + 0.8, M[3] + 0.5][i]

def do_state(t, sc):
    """(tan so dang dat, so doc, mot chieu?, da bat may)"""
    if t < row_at(0, sc) - 0.6: return 50, "···", False, t > sc["M"][0] + 0.8
    last = max([i for i in range(6) if t >= row_at(i, sc)], default=-1)
    if last == 5: return 0, "0", True, True
    nxt = min(last + 1, 5)
    if t >= row_at(nxt, sc) - 0.2:                          # vua van num: so chua on dinh
        return (ROWS[nxt][0] if nxt < 5 else 0), "···", nxt == 5, True
    if last < 0: return 50, "···", False, True
    return ROWS[last][0], ROWS[last][1], False, True

def _phase(t, sc):
    # tich phan nhip nhin thay theo tung doan tan so de dao dong khong giat khi doi f
    ph, prev_t, prev_f = 0.0, 0.0, 50
    for i in range(5):
        a = row_at(i, sc)
        if t <= a: break
        ph += 2 * math.pi * viz_hz(prev_f) * (a - prev_t); prev_t, prev_f = a, ROWS[i][0]
    return ph + 2 * math.pi * viz_hz(prev_f) * (t - prev_t)

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    f, rd, dc, on = do_state(t, sc)
    rig(d, t, f if not dc else 50, rd, phase=_phase(t, sc) if on else None, dc=dc)
    card(d, (60, 995, 1020, 1590), fill=WHITE, outline=NAVY, w=4)
    text(d, (W / 2, 1040), f"Giữ U = {U} V", 44, PURPLE, alpha=appear(t, 0.6))
    xs = [330, 750]
    for x, c in zip(xs, ["f (Hz)", "I đo được (mA)"]): text(d, (x, 1105), c, 38, MUTED)
    d.line([(90, 1138), (990, 1138)], fill=LIGHT, width=4)
    last = max([i for i in range(6) if t >= row_at(i, sc)], default=-1)
    rows = [(str(f_), s) for f_, s in ROWS] + [("một chiều", "0")]
    for i, (a_, b_) in enumerate(rows):
        a = appear(t, row_at(i, sc), 0.35); y = 1180 + i * 66
        if a <= 0: continue
        if i == last: d.rounded_rectangle([80, y - 30, 1000, y + 30], radius=14, fill=A((225, 236, 255), a))
        text(d, (xs[0], y), a_, 42, BLUE, alpha=a)
        text(d, (xs[1], y), b_, 44, RED, alpha=a)

# ---------------- canh 3: dap an C + do thi I(f) + I/f ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k = back((t - 0.2) / 0.5) if t > 0.2 else 0
    card(d, (60, 250, 1020, 350), fill=(220, 252, 231), outline=GREEN, w=5)
    text(d, (W / 2, 300), "Đáp án C", int(48 * clamp(k, 0.3, 1.0)), GREEN)
    x0, x1, yb, yt = 190, 940, 900, 470
    X = lambda f: x0 + f / 850 * (x1 - x0); Y = lambda i: yb - i / 65 * (yb - yt)
    card(d, (60, 380, 1020, 1030), fill=WHITE, outline=LIGHT, w=3)
    for i in (30, 60): d.line([(x0, Y(i)), (x1, Y(i))], fill=(240, 236, 228), width=2)
    d.line([(x0, yb), (x1 + 30, yb)], fill=NAVY, width=5); d.line([(x0, yb), (x0, yt - 30)], fill=NAVY, width=5)
    text(d, (x0 + 18, yt - 40), "I (mA)", 36, MUTED, anchor="lm")
    text(d, (x1 + 30, yb + 80), "f (Hz)", 36, MUTED, anchor="rm")
    for f in (0, 400, 800):
        d.line([(X(f), yb), (X(f), yb + 10)], fill=NAVY, width=3); text(d, (X(f), yb + 36), str(f), 36, MUTED, bold=False)
    for i in (0, 30, 60):
        d.line([(x0 - 10, Y(i)), (x0, Y(i))], fill=NAVY, width=4); text(d, (x0 - 18, Y(i)), str(i), 36, MUTED, bold=False, anchor="rm")
    kc = ease((t - M[0] - 1.0) / 1.0)
    if kc > 0:                                           # duong mo hinh I = U*2*pi*f*C, qua goc toa do
        fe = 850 * kc
        for j in range(0, int(fe), 30):
            d.line([(X(j), Y(K_MODEL * j)), (X(min(j + 18, fe)), Y(K_MODEL * min(j + 18, fe)))], fill=A(BLUE, 0.7), width=5)
        km = appear(t, M[0] + 1.8)
        text(d, (x0 + 30, Y(57)), "nét đứt: mô hình", 36, BLUE, anchor="lm", alpha=km)
        text(d, (x0 + 30, Y(49)), "I = U·2πfC", 38, BLUE, anchor="lm", alpha=km)
    for i, (f, s) in enumerate(ROWS):
        a = appear(t, 0.5 + i * 0.2, 0.4)
        if a <= 0: continue
        dot(d, X(f), Y(IV[i]), 15 * back(a), ORANGE, WHITE)
        if i >= 2: text(d, (X(f) + 26, Y(IV[i]) + 36), s, 36, ORANGE, anchor="lm", alpha=a)
    dot(d, X(0), Y(0), 10, NAVY)
    text(d, (W / 2, 985), "Đo thấp hơn 2–5%", 36, MUTED, bold=False, alpha=appear(t, M[0] + 2.2))
    # cot I/f
    a1 = appear(t, M[1] - 0.2)
    if a1 <= 0: return
    card(d, (60, 1060, 1020, 1590), fill=A(WHITE, a1), outline=A(LIGHT, a1), w=3)
    text(d, (W / 2, 1110), "I / f (mA/Hz)", 38, MUTED, alpha=a1)
    vx = [160 + j * 190 for j in range(5)]
    for j, (f, s) in enumerate(ROWS):
        text(d, (vx[j], 1190), f"{f} Hz", 36, MUTED, bold=False, alpha=a1)
        text(d, (vx[j], 1250), s, 40, INK, alpha=a1)
        a = appear(t, M[1] + 0.3 + j * 0.25, 0.35)
        arrow(d, (vx[j], 1285), (vx[j], 1340), A(ORANGE, a), w=4, head=14)
        text(d, (vx[j], 1385), RATIO[j], 38, ORANGE, alpha=a)
    c = appear(t, M[1] + 1.8)
    card(d, (110, 1440, 970, 1550), fill=A((220, 252, 231), c), r=24)
    ctext(d, 1495, "I tỉ lệ thuận f", 44, GREEN, alpha=c)

# ---------------- canh 4: co che + chua noi duoc gi ----------------
def s_why(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    x0, x1, top, bot, wy = 410, 670, 330, 830, 580
    ph = 2 * math.pi * 0.45 * t; s = math.sin(ph); q = -s; x = 30 * s
    lp = [(80, wy), (x0 - 40, wy)]; rp = [(x1 + 40, wy), (1000, wy)]
    d.line(lp, fill=GRAY, width=14); d.line(rp, fill=GRAY, width=14)
    plates(d, q, x0, x1, top, bot, th=40, sz=48, lbl_e=False)
    L = _path_len(lp); u = 40
    while u < L - 40:
        for p in (lp, rp):
            px, py = _at(p, u + x); dot(d, px, py, 11, BLUE)
        u += 56
    text(d, ((x0 + x1) / 2, (top + bot) / 2), "E", 52, A(ORANGE, clamp(abs(q) * 1.3)))
    text(d, (200, wy - 50), "e trong dây:", 36, BLUE, bold=False)
    text(d, (200, wy + 50), "tới – lui", 36, BLUE, bold=False)
    # nhan dien moi
    a0 = appear(t, 0.4)
    card(d, (270, 850, 810, 930), fill=A(WHITE, a0), outline=A(NAVY, a0), r=20, w=3)
    text(d, (540, 890), "điện môi", 36, INK, alpha=a0)
    # tu truong khep kin quanh vung E bien thien (ket luan Maxwell)
    b = appear(t, M[1] + 0.3)
    if b > 0:
        cx = (x0 + x1) / 2
        for hw, hh in ((60, 190), (100, 240)):
            bb = [cx - hw, (top + bot) / 2 - hh, cx + hw, (top + bot) / 2 + hh]
            for a in range(0, 360, 24): d.arc(bb, a, a + 13, fill=A(TEAL, b), width=5)
        text(d, (cx + 200, top - 20), "từ trường", 36, TEAL, alpha=b)
    a = appear(t, M[0] + 0.6)
    card(d, (60, 960, 1020, 1210), fill=A(WHITE, a), outline=A(BLUE, a), w=5)
    ctext(d, 1035, "E biến thiên", 46, INK, alpha=a)
    ctext(d, 1135, "= dòng điện dịch", 50, BLUE, alpha=appear(t, M[1]))
    c = appear(t, M[2] - 0.2)
    card(d, (60, 1240, 1020, 1590), fill=A(WHITE, c), outline=A(PURPLE, c), w=5)
    text(d, (W / 2, 1300), "Chưa nói được gì?", 42, PURPLE, alpha=c)
    ctext(d, 1430, "Đồng hồ không thấy E\nvà từ trường.", 42, INK, alpha=c, lh=1.25)

# ---------------- canh 5: bay "f cao thi tu can manh hon" ----------------
def s_trap(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    card(d, (60, 250, 1020, 420), fill=(254, 226, 226), outline=RED, w=5)
    ctext(d, 335, "Bẫy: “f cao,\ntụ cản mạnh”", 48, RED, alpha=appear(t, 0.1))
    a = appear(t, 0.6)
    card(d, (60, 450, 1020, 1130), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    text(d, (W / 2, 500), "U = 12 V", 40, MUTED, alpha=a)
    base, top = 1040, 590
    bars = [("một chiều", 0.0, "0"), ("50 Hz", IV[0], ROWS[0][1]), ("800 Hz", IV[4], ROWS[4][1])]
    for j, (lb, v, s) in enumerate(bars):
        cx = 240 + j * 300; g = ease((t - 0.8 - j * 0.35) / 0.5)
        text(d, (cx, base + 46), lb, 36, MUTED, bold=False, alpha=a)
        h = (base - top - 60) * v / 60 * g
        if v > 0: d.rectangle([cx - 70, base - h, cx + 70, base], fill=ORANGE)
        text(d, (cx, base - h - 36), f"{s} mA", 40, INK, alpha=g)
    d.line([(110, base), (970, base)], fill=NAVY, width=4)
    c = appear(t, M[1] - 0.1)
    card(d, (60, 1160, 1020, 1590), fill=A((236, 253, 243), c), outline=A(GREEN, c), w=5)
    text(d, (W / 2, 1220), "Ngược lại:", 42, GREEN, alpha=c)
    rich(d, W / 2, 1320, "Z_{C} = 1/(2πfC)", 60, GREEN, alpha=c)
    ctext(d, 1440, "f tăng → dòng tăng\nmột chiều: 0 mA", 44, INK, alpha=appear(t, M[1] + 0.6), lh=1.3)

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    chot_hoi(d, t, sc, "Dòng điện dịch: I tỉ lệ thuận f",
             f"f = 1 600 Hz: đồng hồ chỉ?",
             "I/f có đổi không?")

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + row_at(5, do), "tap"), (an["t0"] + 0.2, "ding"),
            (tr["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l12-dttruong-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Dòng điện dịch · thachlab.id.vn", scenes=[
 dict(key="hook", title="Dòng xoay chiều qua tụ điện", draw=s_hook, tail=0.6, caps=[
   ("Tụ nối tiếp đồng hồ.", 2.4),
   ("Chọn đáp án.", 5.4)]),
 dict(key="do", title="Đổi tần số, đọc đồng hồ", draw=s_do, tail=0.8, caps=[
   ("Bật máy phát 12 V.", 2.3),
   ("50, 100, 200 Hz.", 2.8),
   ("400, 800 Hz.", 2.6),
   ("Một chiều: 0 mA.", 2.8)]),
 dict(key="ans", title="Dòng tỉ lệ thuận với tần số", draw=s_ans, tail=0.6, caps=[
   ("f gấp 16 lần, I gấp ≈ 16.", 3.0),
   ("I/f gần như không đổi.", 3.0)]),
 dict(key="why", title="Vì sao có dòng qua tụ?", draw=s_why, tail=0.6, caps=[
   ("Không hạt nào qua điện môi.", 2.8),
   ("Dòng điện dịch.", 2.8),
   ("Chưa thấy E, từ trường.", 2.6)]),
 dict(key="trap", title="Cái bẫy", draw=s_trap, tail=0.6, caps=[
   ("Bẫy hay gặp.", 2.6),
   ("Dung kháng giảm.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Thử nghĩ: bao nhiêu mA?", 5.0)]),
])
