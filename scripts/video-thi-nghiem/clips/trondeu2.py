# Clip: tn-l10-trondeu-02 - Mot radian: quan soi chi dai bang ban kinh quanh nap noi (9/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-trondeu-02.json:
#   so_lieu_mau: r = s = 8,0 / 10,0 / 12,5 cm ; theta li thuyet 57,3 deg ; theta do 56 / 58 / 57 deg (minh hoa, lech +-1 deg).
#   tham_so: r 5-15 cm, s 1-30 cm ; rut_ra: theta = s/r ; ca vong 2.pi.r -> 2.pi rad ; 180 deg = pi rad.
# Hinh ve dung hinh hoc that: cung chi dai = r -> goc ve 1 rad = 57,3 deg; so doc tren thuoc do do la cot "theta do".
# Du doan (K10: chi cau hoi + hinh, khong nut): nap to hon thi goc AOB the nao? Dap an: gan nhu bang nhau.
#   Nhieu (khung): nap to -> goc lon hon ; nap to -> goc nho hon.
# Cau chot dung r = 15 cm, s = 30 cm (chua tung hien, trong mien tham_so): theta = 2 rad.
from engine import *

ROWS = [(8.0, 8.0, 56), (10.0, 10.0, 58), (12.5, 12.5, 57)]     # r (cm), s (cm), theta do (deg)
RAD = 1.0                                                     # goc ve that (rad) khi s = r
PXCM = 24.0
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

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    for (r, _, _), cx in ((ROWS[0], 270), (ROWS[2], 730)):
        R = r * 18; c = (cx, 640)
        lid(d, c, R)
        d.line([c, P(c, R, 0)], fill=NAVY, width=4)
        text(d, (cx, 920), f"r = {vn(r)} cm", 40, INK)
        thread(d, c, R, 0.0)                      # chi chua quan: thang dung tai A, dai = r
        text(d, (P(c, R, 0)[0] + 30, 640 + 26), "A", 40, NAVY, anchor="lm")
        text(d, (c[0] - 34, c[1] + 20), "O", 40, NAVY)
    text(d, (W / 2, 330), "sợi chỉ cam dài bằng r", 40, THREAD)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 86), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 55), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 160, "Quấn chỉ sát vành từ A, điểm cuối là B.", 46, INK, maxw=920, alpha=a)
    ctext(d, y0 + 290, "Nắp to hơn: góc AOB thế nào?", 50, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 1.4, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 450, 940, y0 + 464], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 450, 140 + 800 * (1 - p), y0 + 464], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (ba nap, mot canh lien mach) ----------------
C0 = (450, 650)
TS = [(0.5, 4.8), (5.5, 3.4), (9.1, 3.2)]          # (bat dau, do dai) moi lan do
def trial_at(t):
    j = 0
    for i, (a, _) in enumerate(TS):
        if t >= a: j = i
    a, D = TS[j]; return j, clamp((t - a) / D)

def table(d, n, hl=None, y0=1030, y1=1590, k=1.0, title=True):
    card(d, (40, y0, 1040, y1), fill=A(WHITE, k), outline=A(LIGHT, k), w=3)
    xs = (230, 540, 850); yh = y0 + 70
    for x, h in zip(xs, ("r (cm)", "s (cm)", "góc đo")):
        text(d, (x, yh), h, 40, MUTED, alpha=k)
    d.line([(90, yh + 42), (990, yh + 42)], fill=A(LIGHT, k), width=3)
    for i in range(3):
        y = yh + 120 + i * 110
        if hl == i: card(d, (80, y - 46, 1000, y + 46), fill=A((255, 247, 237), k), r=20)
        if i < n:
            r, s, g = ROWS[i]
            text(d, (xs[0], y), vn(r), 46, INK, alpha=k)
            text(d, (xs[1], y), vn(s), 46, THREAD, alpha=k)
            text(d, (xs[2], y), f"{g}°", 50, BLUE, alpha=k)

def s_do(img, d, t, sc):
    j, p = trial_at(t)
    r, s, g = ROWS[j]; R = r * PXCM; c = C0
    lid(d, c, R)
    kr = appear(p, 0.0, 0.12)
    d.line([c, P(c, R, 0)], fill=A(NAVY, kr), width=5)
    text(d, (880, 600), f"r = {vn(r)} cm", 40, NAVY, alpha=kr)
    text(d, (P(c, R, 0)[0] + 26, c[1]), "A", 40, NAVY, anchor="lm", alpha=kr)
    text(d, (c[0] - 30, c[1] + 24), "O", 40, NAVY)
    kt = appear(p, 0.12, 0.08)
    w = RAD * ease((p - 0.22) / 0.38)
    if kt > 0: thread(d, c, R, w, k=kt)
    if p > 0.6:
        kb = appear(p, 0.6, 0.08); b = P(c, R, RAD)
        d.line([c, b], fill=A(NAVY, kb), width=5)
        text(d, (b[0] + 18, b[1] - 26), "B", 40, NAVY, anchor="lm", alpha=kb)
    if p > 0.7:
        kp = appear(p, 0.7, 0.08); rp = min(150, R * 0.62)
        protractor(d, c, rp, k=kp)
        d.arc([c[0] - 70, c[1] - 70, c[0] + 70, c[1] + 70], -math.degrees(RAD), 0, fill=A(BLUE, kp), width=6)
    if p > 0.82:
        kg = appear(p, 0.82, 0.08)
        lw = tw(d, f"≈ {g}°", F(56)) + 50
        card(d, (880 - lw / 2, 380, 880 + lw / 2, 470), fill=A(WHITE, kg), outline=A(BLUE, kg), r=24, w=4)
        text(d, (880, 425), f"≈ {g}°", 56, BLUE, alpha=kg)
        text(d, (880, 510), "thước đo độ", 40, BLUE, alpha=kg)
    text(d, (880, 320), f"Nắp {j + 1}", 44, INK)
    n = j + (1 if p > 0.84 else 0)
    table(d, n, hl=j)

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    ka = appear(t, 0.15, 0.5)
    lb = "ĐÁP ÁN · gần như bằng nhau"
    pw = tw(d, lb, F(40)) + 56
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 330), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 296), lb, 40, WHITE, alpha=ka)
    c = (430, 700)
    d.ellipse([c[0] - 9, c[1] - 9, c[0] + 9, c[1] + 9], fill=NAVY)
    cols = (TEAL, BLUE, PURPLE)
    for i, (r, _, _) in enumerate(ROWS):
        R = r * 24; k = appear(t, 0.6 + 0.6 * i, 0.4)
        d.arc([c[0] - R, c[1] - R, c[0] + R, c[1] + R], 0, 360, fill=A(LID_D, 0.5 * k), width=3)
        d.arc([c[0] - R, c[1] - R, c[0] + R, c[1] + R], -math.degrees(RAD), 0, fill=A(THREAD, k), width=10)
    Rm = ROWS[2][0] * 24 + 30
    d.line([c, P(c, Rm, 0)], fill=NAVY, width=5); d.line([c, P(c, Rm, RAD)], fill=NAVY, width=5)
    text(d, (P(c, Rm, 0)[0] + 20, c[1]), "A", 40, NAVY, anchor="lm")
    text(d, (P(c, Rm, RAD)[0] + 18, P(c, Rm, RAD)[1] - 10), "B", 40, NAVY, anchor="lm")
    kc = appear(t, 2.6, 0.4)
    text(d, (880, 760), "ba cung,", 40, THREAD, alpha=kc); text(d, (880, 815), "một góc", 40, THREAD, alpha=kc)
    table(d, 3, y0=1030, y1=1500)
    kn = appear(t, 3.4, 0.4)
    text(d, (W / 2, 1545), "lệch ±1°: quấn chỉ, đọc thước", 40, INK, alpha=kn)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]; c = (420, 650); R = 260
    lid(d, c, R)
    d.pieslice([c[0] - R, c[1] - R, c[0] + R, c[1] + R], -math.degrees(RAD), 0, fill=(254, 215, 170))
    d.arc([c[0] - R, c[1] - R, c[0] + R, c[1] + R], -math.degrees(RAD), 0, fill=THREAD, width=10)
    d.line([c, P(c, R, 0)], fill=NAVY, width=5); d.line([c, P(c, R, RAD)], fill=NAVY, width=5)
    text(d, (c[0] + R / 2, c[1] + 40), "r", 44, NAVY)
    m = P(c, R + 40, RAD / 2); text(d, (m[0] + 6, m[1]), "s = r", 44, THREAD, anchor="lm")
    q = P(c, 170, RAD / 2); text(d, q, "1 rad", 40, INK)
    if t < M[1] - 0.1:
        k1 = appear(t, 0.5, 0.45)
        card(d, (40, 1030, 1040, 1590), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
        eq(d, W / 2, 1150, "Góc ở tâm: θ = s/r (rad)", 50, PURPLE, alpha=k1)
        k3 = appear(t, 2.2, 0.45)
        eq(d, W / 2, 1320, "180° = π rad", 46, INK, alpha=k3)
        eq(d, W / 2, 1450, "1 rad = 180°/π ≈ 57,3°", 50, TEAL, alpha=k3)
    else:
        k2 = appear(t, M[1] - 0.1, 0.45)
        card(d, (40, 1030, 1040, 1590), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, 1100), "Chưa nói được", 46, NAVY, alpha=k2)
        kk = k2 * appear(t, M[1] + 0.3, 0.4)
        card(d, (80, 1160, 1000, 1540), fill=A((254, 242, 242), kk), r=24)
        text(d, (W / 2, 1270), "Thước chỉ đọc tới 1°", 46, RED, alpha=kk)
        text(d, (W / 2, 1420), "Số 57,3° có nhờ tính", 46, RED, alpha=kk)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.15, 0.4); y0 = 265
    card(d, (40, y0, 1040, 1420), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(RED, a1), r=32)
    text(d, (W / 2, y0 + 62), "BẪY", 40, WHITE, alpha=a1)
    text(d, (W / 2, y0 + 170), "✗ 1 rad = 1°", 52, RED, alpha=a1)
    tw_ = tw(d, "✗ 1 rad = 1°", F(52))
    d.line([(W / 2 - tw_ / 2 + 60, y0 + 172), (W / 2 + tw_ / 2, y0 + 172)], fill=A(RED, a1), width=5)
    c = (375, y0 + 640); R = 330
    d.pieslice([c[0] - R, c[1] - R, c[0] + R, c[1] + R], -math.degrees(RAD), 0, fill=A((219, 234, 254), a1), outline=A(BLUE, a1), width=4)
    d.pieslice([c[0] - R, c[1] - R, c[0] + R, c[1] + R], -1, 0, fill=A(RED, a1))
    d.line([c, P(c, R, 0)], fill=A(NAVY, a1), width=5)
    text(d, (P(c, R, 0)[0] + 20, c[1] + 4), "1°", 44, RED, anchor="lm", alpha=a1)
    m = P(c, R * 0.62, RAD * 0.6); text(d, m, "1 rad", 46, BLUE, alpha=a1)
    kk = appear(t, M[0] + 2.3, 0.5)
    card(d, (90, y0 + 790, 990, y0 + 1060), fill=A((236, 253, 243), kk), r=24)
    text(d, (W / 2, y0 + 870), "✓ 1 rad ≈ 57,3°", 50, GREEN, alpha=kk)
    text(d, (W / 2, y0 + 970), "gấp 57 lần góc 1°", 44, GREEN, alpha=kk)

# ---------------- canh 6: Chot ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def hint(d, t, k):
        c = (250, 1110); R = 120                        # nap r = 15 cm, chi 30 cm de thang ben canh (chua quan)
        d.ellipse([c[0] - R - 10, c[1] - R - 10, c[0] + R + 10, c[1] + R + 10], fill=A(LID, k), outline=A(LID_D, k), width=4)
        d.ellipse([c[0] - R, c[1] - R, c[0] + R, c[1] + R], fill=A((241, 245, 249), k), outline=A(LID_D, k), width=3)
        d.line([c, P(c, R, 0)], fill=A(NAVY, k), width=4)
        d.ellipse([c[0] - 7, c[1] - 7, c[0] + 7, c[1] + 7], fill=A(NAVY, k))
        text(d, (c[0], c[1] + R + 45), "r = 15 cm", 40, NAVY, alpha=k)
        d.line([(450, c[1]), (450 + 2 * R, c[1])], fill=A(THREAD, k), width=8)
        text(d, (450 + R, c[1] - 50), "chỉ 30 cm", 40, THREAD, alpha=k)
        kh = appear(t, M[0] + 2.8, 0.5)
        if kh <= 0: return
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1360), "Gợi ý", 40, INK, alpha=kh)
        text(d, (W / 2, 1450), "Chỉ dài gấp mấy lần bán kính?", 40, ORANGE, alpha=kh)
    chot_hoi(d, t, sc, "1 rad: cung dài\nđúng bằng bán kính",
             "Nắp 15 cm, chỉ 30 cm:\ngóc ở tâm mấy rad?", None, body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open")]
    for a, D in TS: cs.append((do["t0"] + a + 0.82 * D, "tap"))
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1], "tap"),
           (b["t0"] + 0.15, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l10-trondeu-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Chuyển động tròn đều · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Sợi chỉ và nắp nồi", draw=s_hook, tail=0.5, caps=[
   ("Hai nắp: nhỏ và to.", 2.6),
   ("Dừng video, chọn câu trả lời.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Chỉ dài bằng r, quấn sát vành.", 5.0),
   ("Đo góc AOB, làm lại với nắp khác.", 6.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Nắp to hay nhỏ đều thế.", 5.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.4, caps=[
   ("Cung dài bằng bán kính: 1 rad.", 4.2),
   ("Còn điều chưa biết.", 3.8)]),
 dict(key="bay", title="Bẫy thường gặp", draw=s_bay, tail=0.4, caps=[
   ("1 rad có phải là 1°?", 4.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 6.4)]),
])
