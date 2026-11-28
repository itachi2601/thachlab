# Clip: tn-l10-trondeu-02 - Mot radian: quan soi chi dai bang ban kinh quanh nap noi (9/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-trondeu-02.json:
#   so_lieu_mau: r = s = 8,0 / 10,0 / 12,5 cm ; theta li thuyet 57,3 deg ; theta do 56 / 58 / 57 deg (minh hoa, lech +-1 deg).
#   tham_so: r 5-15 cm, s 1-30 cm ; rut_ra: theta = s/r ; ca vong 2.pi.r -> 2.pi rad ; 180 deg = pi rad.
# Hinh ve dung hinh hoc that: cung chi dai = r -> goc ve 1 rad = 57,3 deg; so doc tren thuoc do do la cot "theta do".
# Du doan (27/11, cong moi): o Quan sat hop exp ghi san "khoang 57 do, nap to hay nho deu vay" nen KHONG hoi co nap.
#   Hoi: quan noi tiep cac soi dai bang r, bao nhieu soi thi kin vanh? Dap an: hon 6 soi mot chut (2.pi ~ 6,28; kho rut_ra:
#   ca vong 2.pi.r -> 2.pi rad). Hinh ve dung: 6 soi = 6 rad, con ho 2.pi - 6 rad.
# Cau chot: r = 15 cm, s = 30 cm (trong mien tham_so) -> 2 rad ~ 115 do (2 x 57,3). Dap so khong hien tren man.
from engine import *

ROWS = [(8.0, 8.0, 56), (10.0, 10.0, 58), (12.5, 12.5, 57)]     # r (cm), s (cm), theta do (deg)
RAD = 1.0                                                     # goc ve that (rad) khi s = r
PXCM = 24.0
DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)
LID = (203, 213, 225); LID_D = (100, 116, 139); THREAD = ORANGE; PROT = (219, 234, 254)

def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

_TI = {}
def TI(size):                                   # Times Bold Italic cho theta, pi (de doc, khac chu thuong)
    size = int(size)
    if size not in _TI: _TI[size] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", size)
    return _TI[size]

def eq(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    fs = [(p, TI(size * 1.12) if p in ("θ", "π") else F(size)) for p in re.split(r"(θ|π)", s) if p]
    tot = sum(tw(d, p, f) for p, f in fs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for p, f in fs:
        dtext(d, (x, cy), p, f, color, alpha, "lm"); x += tw(d, p, f)
    return tot

def P(c, R, u): return (c[0] + R * math.cos(u), c[1] - R * math.sin(u))     # u nguoc chieu kim dong ho tu huong dong

def lid(d, c, R, k=1.0):
    d.ellipse([c[0] - R - 14, c[1] - R - 14, c[0] + R + 14, c[1] + R + 14], fill=A(LID, k), outline=A(LID_D, k), width=5)
    d.ellipse([c[0] - R, c[1] - R, c[0] + R, c[1] + R], fill=A((241, 245, 249), k), outline=A(LID_D, k), width=4)
    d.ellipse([c[0] - 9, c[1] - 9, c[0] + 9, c[1] + 9], fill=A(NAVY, k))

def thread(d, c, R, w, col=THREAD, k=1.0, width=9):
    """chi dai R (px), da quan w (rad) theo vanh tu A (u = 0); phan con lai thang theo tiep tuyen."""
    if w > 0.01:
        pts = [P(c, R, w * i / 40) for i in range(41)]
        d.line(pts, fill=A(col, k), width=width, joint="curve")
    p = P(c, R, w); L = R * (RAD - w)
    if L > 2:
        tx, ty = -math.sin(w), -math.cos(w)
        d.line([p, (p[0] + L * tx, p[1] + L * ty)], fill=A(col, k), width=width)

def protractor(d, c, rp, reading=None, k=1.0):
    d.pieslice([c[0] - rp, c[1] - rp, c[0] + rp, c[1] + rp], 180, 360, fill=A(PROT, 0.75 * k), outline=A(BLUE, k), width=3)
    for g in range(0, 181, 10):
        u = math.radians(g); L = 26 if g % 30 == 0 else 14
        d.line([P(c, rp, u), P(c, rp - L, u)], fill=A(BLUE, k), width=3)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0, x0=175, step=150, w=130):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = x0 + i * step
        if i < on: card(d, (x, y, x + w, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + w, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

def arc_pts(c, R, u0, u1, n=40): return [P(c, R, u0 + (u1 - u0) * i / n) for i in range(n + 1)]

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    c, R = (540, 640), 10.0 * PXCM
    lid(d, c, R)
    w = RAD * ease(clamp((t - 0.4) / 1.8))
    thread(d, c, R, w)
    d.line([c, P(c, R, 0)], fill=NAVY, width=4)
    text(d, (c[0] + R / 2, c[1] + 40), "r", 58, NAVY)
    text(d, (P(c, R, 0)[0] + 30, c[1] + 10), "A", 55, NAVY, anchor="lm")
    text(d, (c[0] - 40, c[1] + 30), "O", 55, NAVY)
    text(d, (W / 2, 330), "sợi chỉ dài bằng r", 55, DORANGE)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1085 + (1 - k) * 30
    card(d, (40, y0, 1040, y0 + 500), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, k)
    for j, s1 in enumerate(("Quấn nối tiếp từng sợi.", "Bao nhiêu sợi thì kín vành?")):
        text(d, (W / 2, y0 + 190 + j * 85), s1, 60, PURPLE if j == 1 else INK, alpha=k)
    seg_bar(d, y0 + 400, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: Tien hanh (ba nap) ----------------
C0 = (430, 650)
TS = [(0.5, 3.4), (4.0, 2.4), (6.5, 2.4)]          # (bat dau, do dai) moi lan do
def trial_at(t):
    j = 0
    for i, (a, _) in enumerate(TS):
        if t >= a: j = i
    a, D = TS[j]; return j, clamp((t - a) / D)

def table(d, n, hl=None, y0=1030, y1=1590, k=1.0):
    card(d, (40, y0, 1040, y1), fill=A(WHITE, k), outline=A(LIGHT, k), w=3)
    xs = (230, 540, 850); yh = y0 + 75
    for x, h, col in zip(xs, ("r (cm)", "s (cm)", "góc đo (°)"), (NAVY, DORANGE, BLUE)):
        text(d, (x, yh), h, 58, col, alpha=k)
    d.line([(90, yh + 48), (990, yh + 48)], fill=A(LIGHT, k), width=3)
    for i in range(3):
        y = yh + 140 + i * 110
        if hl == i: card(d, (80, y - 48, 1000, y + 48), fill=A((255, 247, 237), k), r=20)
        if i < n:
            r, s_, g = ROWS[i]
            text(d, (xs[0], y), vn(r), 58, INK, alpha=k)
            text(d, (xs[1], y), vn(s_), 58, DORANGE, alpha=k)
            text(d, (xs[2], y), f"{g}°", 58, BLUE, alpha=k)

def s_do(img, d, t, sc):
    j, p = trial_at(t)
    r, s_, g = ROWS[j]; R = r * PXCM; c = C0
    lid(d, c, R)
    d.line([c, P(c, R, 0)], fill=NAVY, width=5)
    text(d, (P(c, R, 0)[0] + 26, c[1] + 10), "A", 55, NAVY, anchor="lm")
    text(d, (c[0] - 34, c[1] + 30), "O", 55, NAVY)
    w = RAD * ease((p - 0.1) / 0.45)
    thread(d, c, R, w)
    if p > 0.55:
        b = P(c, R, RAD); d.line([c, b], fill=NAVY, width=5)
        text(d, (b[0] + 18, b[1] - 30), "B", 55, NAVY, anchor="lm")
    if p > 0.65:
        rp = min(150, R * 0.62)
        protractor(d, c, rp)
        d.arc([c[0] - 70, c[1] - 70, c[0] + 70, c[1] + 70], -math.degrees(RAD), 0, fill=BLUE, width=6)
    if p > 0.78:
        lw = tw(d, f"≈ {g}°", F(60)) + 50
        card(d, (880 - lw / 2, 400, 880 + lw / 2, 490), fill=WHITE, outline=BLUE, r=24, w=4)
        text(d, (880, 445), f"≈ {g}°", 60, BLUE)
    text(d, (880, 320), f"Nắp {j + 1}", 58, INK)
    table(d, j + (1 if p > 0.8 else 0), hl=j)

# ---------------- canh 3: Dap an (quan noi tiep 6 soi) ----------------
NS, T1, DT = 6, 0.5, 0.5
def s_dapan(img, d, t, sc):
    M = sc["M"]
    c, R = (540, 650), 10.0 * PXCM
    lid(d, c, R)
    d.line([c, P(c, R, 0)], fill=NAVY, width=4)
    text(d, (P(c, R, 0)[0] + 30, c[1] + 10), "A", 55, NAVY, anchor="lm")
    for i in range(NS):
        g = clamp((t - T1 - i * DT) / DT)
        if g <= 0: continue
        col = THREAD if i % 2 == 0 else TEAL
        d.line(arc_pts(c, R, i * RAD, i * RAD + RAD * g), fill=col, width=11, joint="curve")
        if g >= 1: text(d, P(c, R - 55, i * RAD + RAD / 2), str(i + 1), 58, col)
    kg = appear(t, M[1], 0.45)
    if kg > 0:                                   # phan ho con lai: 2.pi - 6 rad
        d.line(arc_pts(c, R + 26, NS * RAD, 2 * math.pi, 12), fill=A(DRED, kg), width=8)
        q = P(c, R + 70, (NS * RAD + 2 * math.pi) / 2)
        text(d, (q[0] + 10, q[1] + 30), "còn hở", 55, DRED, anchor="lm", alpha=kg)
    ka = appear(t, M[1], 0.45)
    if ka <= 0: return
    yk = 1085 + (1 - ka) * 30
    card(d, (40, yk, 1040, yk + 420), fill=A(WHITE, ka), outline=A(NAVY, ka), w=6)
    pill(d, W / 2, yk + 70, "ĐÁP ÁN", NAVY, ka)
    text(d, (W / 2, yk + 200), "hơn 6 sợi một chút", 64, BLUE, alpha=ka)
    eq(d, W / 2, yk + 310, "cả vành = 2πr ≈ 6,28 r", 58, DGREEN, alpha=ka)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]; c = (420, 650); R = 260
    lid(d, c, R)
    g = ease(clamp((t - 0.4) / 1.6))
    d.pieslice([c[0] - R, c[1] - R, c[0] + R, c[1] + R], -math.degrees(RAD * g), 0, fill=(254, 215, 170))
    d.line(arc_pts(c, R, 0, RAD * g), fill=THREAD, width=10, joint="curve")
    d.line([c, P(c, R, 0)], fill=NAVY, width=5); d.line([c, P(c, R, RAD * g)], fill=NAVY, width=5)
    text(d, (c[0] + R / 2, c[1] + 45), "r", 58, NAVY)
    m = P(c, R + 40, RAD / 2); text(d, (m[0] + 6, m[1]), "s = r", 58, DORANGE, anchor="lm")
    q = P(c, 165, RAD / 2); text(d, q, "1 rad", 55, INK)
    k1 = appear(t, 0.4, 0.4)
    card(d, (40, 1085, 1040, 1585), fill=A(WHITE, k1), outline=A(GREEN, k1), w=6)
    pill(d, W / 2, 1155, "RÚT RA", GREEN, k1)
    eq(d, W / 2, 1255, "θ = s/r (rad)", 64, PURPLE, alpha=k1)
    eq(d, W / 2, 1340, "θ: góc ở tâm, s: độ dài cung", 55, MUTED, alpha=k1)
    k2 = appear(t, M[1], 0.4)
    eq(d, W / 2, 1430, "cả vòng: 2π rad = 360°", 60, INK, alpha=k2)
    eq(d, W / 2, 1515, "1 rad ≈ 57,3°", 60, TEAL, alpha=k2)

# ---------------- canh 5: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.15, 0.4); y0 = 265
    card(d, (40, y0, 1040, 1590), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
    pill(d, W / 2, y0 + 70, "BẪY", DRED, a1)
    q = "1 rad = 1°"
    ks = clamp((t - M[1]) / 0.4); lw = tw(d, q, F(60)); yy = 450
    text(d, (W / 2, yy), q, 60, mix(INK, GRAY, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
    c = (330, 950); R = 340
    g = 0.02 + 0.98 * ease(clamp((t - M[1]) / 1.4))
    d.pieslice([c[0] - R, c[1] - R, c[0] + R, c[1] + R], -math.degrees(RAD * g), 0, fill=A((219, 234, 254), a1), outline=A(BLUE, a1), width=4)
    d.pieslice([c[0] - R, c[1] - R, c[0] + R, c[1] + R], -1, 0, fill=A(RED, a1))
    d.line([c, P(c, R, 0)], fill=A(NAVY, a1), width=5)
    text(d, (P(c, R, 0)[0] + 20, c[1] + 4), "1°", 58, DRED, anchor="lm", alpha=a1)
    kk = appear(t, M[1], 0.4)
    m = P(c, R * 0.62, RAD * 0.55); text(d, m, "1 rad", 58, BLUE, alpha=kk)
    text(d, (W / 2, 1060), "1 rad ≈ 57,3°", 60, DGREEN, alpha=kk)
    k3 = appear(t, M[2] - 0.1, 0.4)
    if k3 > 0:
        yk = 1160 + (1 - k3) * 30
        card(d, (40, yk, 1040, yk + 420), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, yk + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, yk + 200), "Thước chỉ đọc tới 1°", 58, INK, alpha=k3)
        text(d, (W / 2, yk + 300), "57,3° có nhờ tính", 58, INK, alpha=k3)

# ---------------- canh 6: Thu nghi ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    c = (330, 640); R = 15.0 * 16                         # hinh rieng: 1 cm = 16 px
    lid(d, c, R, k=k)
    d.line([c, P(c, R, 0)], fill=A(NAVY, k), width=5)
    text(d, (c[0], c[1] + R + 60), "r = 15 cm", 58, NAVY, alpha=k)
    text(d, (P(c, R, 0)[0] + 24, c[1] + 10), "A", 55, NAVY, anchor="lm", alpha=k)
    L = 30.0 * 16 * (0.4 + 0.6 * ease(clamp((t - 0.4) / 1.6)))          # chi 30 cm keo ra doc canh phai
    x0 = 950; d.line([(x0, 900), (x0, 900 - min(L, 600))], fill=A(THREAD, k), width=9)
    text(d, (x0 - 30, 900 - min(L, 600) / 2), "chỉ", 55, DORANGE, anchor="rm", alpha=k)
    text(d, (x0 - 30, 900 - min(L, 600) / 2 + 65), "30 cm", 55, DORANGE, anchor="rm", alpha=k)
    card(d, (40, 1030, 1040, 1585), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 1100, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 1215), "Quấn sát vành từ A.", 60, INK, alpha=k)
    text(d, (W / 2, 1310), "Góc AOB khoảng mấy độ?", 60, DORANGE, alpha=k)
    seg_bar(d, 1420, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open")]
    for a, D in TS: cs.append((do["t0"] + a + 0.78 * D, "tap"))
    cs += [(da["t0"] + T1 + i * DT + DT, "tick") for i in range(NS)]
    cs += [(da["t0"] + da["M"][1], "ding"), (r["t0"] + r["M"][1], "tap"),
           (b["t0"] + b["M"][1], "buzz"), (e["t0"] + 0.15, "open")]
    return cs

CLIP = dict(id="tn-l10-trondeu-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Chuyển động tròn đều · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Sợi chỉ và nắp nồi", draw=s_hook, tail=0.2, caps=[
   ("Quấn sát vành từ A.", 2.6),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Chỉ dài bằng r, quấn sát vành.", 4.0),
   ("Đo góc AOB, đổi nắp khác.", 5.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Quấn nối tiếp từng sợi.", 3.1),
   ("Đáp án: hơn 6 sợi một chút.", 3.4)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Cung dài bằng r: góc 1 rad.", 3.8),
   ("Cả vòng: 2π rad.", 3.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("1 rad có phải 1°?", 3.2),
   ("Không: 1 rad ≈ 57,3°.", 3.0),
   ("Thước chỉ đọc tới 1°.", 2.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 5.6)]),
])
