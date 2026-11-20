# Clip: tn-l10-newton3-05 - Hai xe day va lo xo nen, moi xe gan cam bien luc (20/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-newton3-05.json, so_lieu_mau (m1, m2 kg, F N, a1, a2 m/s2):
#   hang 2: 1 1 4 4,0 4,0 ; hang 3: 1 3 4 4,0 1,33 (ghi "≈ 1,33"). Hang 1 (1 kg / 2 kg) = Cau 6 ngay truoc hop -> KHONG hien.
#   Hang 4 (2 2 6) khong dung: de "2 kg" con moi cho cau chot.
# Hop trong bai (sau Cau 6): xe day tren ban nhan, lo xo nen giu bang chot, MOI XE gan cam bien luc o cho tiep xuc lo xo;
#   rut chot, do gia toc TRUNG BINH tung xe trong luc lo xo con day; lam lai sau khi chat gia trong len mot xe.
#   Cam bien doc 0 N truoc khi rut chot (chot giu lo xo) va sau khi lo xo roi xe 2; doc F trong luc day.
# Du doan (K10: chi cau hoi + hinh): xe 1 1 kg, xe 2 3 kg; rut chot, hai cam bien luc chi so the nao? Dap an: bang nhau (4 N).
#   Khong trung Cau 5 (ai toc do lon hon) / Cau 6 (1 kg, 2 kg -> a2).
# Bay = hien_tuong_hay_sai[0] "xe nang chiu luc lon hon" (hinh: mui ten khong bang nhau ✗ / bang nhau 4 N ✓).
# Chua noi duoc = mo_hinh.gia_thiet (luc lo xo coi khong doi; ma sat nho).
# Chot (ghi trong ghi_chu kho): xe 1 nang 2 kg co gia toc 2,5 m/s2, xe 2 nang 3 kg -> cam bien luc xe 2 chi 5 N
#   (F = 2·2,5 tren xe 1, roi dinh luat III). Clip KHONG hien m·a, khong hien a = F/m: buoc dinh luat II la buoc tu suy.
# Tu kiem: /usr/bin/python3 clips/newton3xe5.py --kiem
import math
from engine import *

RUNS = [(1, 1, 4, 4.0, 4.0), (1, 3, 4, 4.0, 1.33)]   # so_lieu_mau hang 2, 3
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
def a_str(a): return "≈ 1,33" if abs(a - 1.33) < 1e-9 else vn(a)

DRED = (185, 28, 28); DGREEN = (21, 110, 55); WOOD = (176, 124, 74); WOOD_D = (140, 96, 54)
WEIGHT = (96, 104, 124); SENS = (70, 78, 100)
C1, C2 = BLUE, ORANGE
GLOW = (214, 200, 255)
def pul(t, per=1.2): return 0.5 - 0.5 * math.cos(2 * math.pi * t / per)

# ---------------- dung cu ----------------
TRK = 668                      # mat ban (day banh xe)
CW, CHB = 220, 90              # than xe
SEN = 24                       # be day cam bien luc
X1, X2 = 366, 714              # tam xe khi lo xo nen (mat cam bien 500 va 580)
GAP0 = 80
K = 17.0                       # px cho 1 m/s2 · f
P, C, PIN = 1.2, 0.9, 0.3      # thoi gian day, troi, rut chot (quay cham)
FMAX = 1 + 2 * C / P

def cart(d, xc, yb, m, col, side, s=1.0, alpha=1.0, blk=1.0):
    """side +1: cam bien o mat phai (xe 1); -1: mat trai (xe 2). Tra ve (x mat cam bien, y lo xo)."""
    w, h, r = CW * s, CHB * s, 20 * s
    by1 = yb - 2 * r + 4; by0 = by1 - h
    nb = int(round(m)) - 1
    for k in range(nb):
        kk = clamp(blk * nb - k) if blk < 1 else 1.0
        if kk <= 0: continue
        yy0 = by0 - (k + 1) * 34 * s - (1 - kk) * 60
        d.rectangle([xc - 44 * s, yy0, xc + 44 * s, yy0 + 34 * s], fill=A(WEIGHT, alpha * kk), outline=A(NAVY, alpha * kk), width=3)
    d.rounded_rectangle([xc - w / 2, by0, xc + w / 2, by1], radius=int(12 * s), fill=A(col, alpha), outline=A(NAVY, alpha), width=4)
    for dx in (-0.3 * w, 0.3 * w):
        d.ellipse([xc + dx - r, yb - 2 * r, xc + dx + r, yb], fill=A(NAVY, alpha)); dot(d, xc + dx, yb - r, 5 * s, A(GRAY, alpha))
    text(d, (xc, (by0 + by1) / 2), f"{m:g} kg", 55, WHITE, alpha=alpha)
    xs = xc + side * w / 2
    d.rectangle([min(xs, xs + side * SEN * s), by0 + 18 * s, max(xs, xs + side * SEN * s), by1 - 14 * s], fill=A(SENS, alpha))
    return xs + side * SEN * s, (by0 + by1) / 2

def spring(d, xa, xb, y, amp=22, n=9, alpha=1.0):
    if xb - xa < 4: return
    pts = [(xa, y)] + [(lerp(xa, xb, (i + 0.5) / n), y + (amp if i % 2 else -amp)) for i in range(n)] + [(xb, y)]
    d.line(pts, fill=A(NAVY, alpha), width=5, joint="curve")

def display(d, xc, sx, sy, val, col, glow=0.0, alpha=1.0, lab=True, y0=300):
    hgt = 150 if lab else 100
    card(d, (xc - 150, y0, xc + 150, y0 + hgt), fill=A(mix(WHITE, GLOW, glow), alpha), outline=A(col, alpha), r=22, w=5)
    d.line([(xc, y0 + hgt), (sx, sy - 30)], fill=A(GRAY, alpha), width=4)
    if lab:
        text(d, (xc, y0 + 42), "lực lên xe " + ("1" if col == C1 else "2"), 55, col, alpha=alpha)
        text(d, (xc, y0 + 108), val, 60, INK, alpha=alpha)
    else:
        text(d, (xc, y0 + hgt / 2), val, 64, PURPLE if val == "?" else INK, alpha=alpha)

def rig(d, s1, s2, m1, m2, val1, val2, pin=0.0, lend=GAP0, glow=0.0, blk=1.0, top=260):
    card(d, (40, top, 1040, top + 460), fill=WHITE, outline=LIGHT, w=3)
    d.rectangle([56, TRK, 1024, TRK + 22], fill=WOOD); d.line([(56, TRK), (1024, TRK)], fill=WOOD_D, width=3)
    x1, x2 = X1 - s1, X2 + s2
    f1, y = cart(d, x1, TRK, m1, C1, +1)
    f2, _ = cart(d, x2, TRK, m2, C2, -1, blk=blk)
    spring(d, f1, f1 + min(f2 - f1, lend), y)
    if pin < 1:                                    # chot: thanh do xuyen qua lo xo, rut len roi mo
        a = 1 - pin; yy = y - 120 * pin
        d.line([(540, yy - 52), (540, yy + 40)], fill=A(RED, a), width=8); dot(d, 540, yy - 60, 13, A(RED, a))
    display(d, x1, f1 - 10, y, val1, C1, glow)
    display(d, x2, f2 + 10, y, val2, C2, glow)

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.7
def think_bar(d, t, t1, t2, y, a):
    q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, y, 940, y + 14], radius=7, fill=A(LIGHT, a))
    if q < 1: d.rounded_rectangle([140, y, 140 + 800 * (1 - q), y + 14], radius=7, fill=A(PURPLE, a))

def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, 0, 0, 1, 3, "?", "?", glow=pul(t))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 800 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 520), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(55)) + 60
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 106), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 66), "DỰ ĐOÁN", 55, WHITE, alpha=a)
    ctext(d, y0 + 270, "Rút chốt. Hai cảm biến lực\nchỉ số thế nào?", 60, INK, maxw=900, alpha=a)
    if t > M[1] + 0.6: think_bar(d, t, M[1] + 0.6, sc["T"] - THINK_END, y0 + 450, a)

# ---------------- canh 2: Tien hanh ----------------
TS = (0.5, 4.6)            # bat dau moi lan (chot rut trong PIN giay, roi lo xo day P giay)
RESET = (2.9, 3.4)         # xe ve cho cu, nen lai lo xo
BLK = (3.9, 4.3)           # chat gia trong len xe 2
ROW_AT = PIN + 0.6         # m, F cua hang hien giua luc day (so cam bien con dang chi F)
A_AT = PIN + P + C         # o gia toc chi dien khi xe chay xong (cam bien chuyen dong tinh a trung binh luc day)

def fmot(tau):
    if tau <= 0: return 0.0
    if tau < P: return (tau / P) ** 2
    return min(1 + 2 * (tau - P) / P, FMAX)

def do_state(t):
    """-> dict: k (lan), s1, s2, chu cam bien, pin, lend, m2, blk, so hang da ghi."""
    k = 1 if t >= RESET[0] else 0
    m1, m2, Fk, a1, a2 = RUNS[k]
    st = dict(k=k, m1=m1, m2=m2, blk=1.0, n=sum(1 for j in range(2) if t >= TS[j] + ROW_AT - 1e-9),
              na=sum(1 for j in range(2) if t >= TS[j] + A_AT - 1e-9), roi=False)
    if k == 1:
        st["blk"] = clamp((t - BLK[0]) / (BLK[1] - BLK[0]))
        if t < BLK[0]: st["m2"] = 1
    ts = TS[k]; tau = t - ts - PIN
    if k == 1 and t < TS[1]:                     # dang dua xe cua lan 1 ve cho cu
        q = 1 - ease((t - RESET[0]) / (RESET[1] - RESET[0])); _, _, _, b1, b2 = RUNS[0]
        st.update(s1=K * b1 * FMAX * q, s2=K * b2 * FMAX * q, pin=1 - ease((t - RESET[0] - 0.3) / 0.3),
                  lend=GAP0 + K * (b1 + b2), val=0)
        return st
    f = fmot(tau)
    st.update(s1=K * a1 * f, s2=K * a2 * f, pin=clamp((t - ts) / PIN) if t >= ts else 0.0,
              lend=GAP0 + K * (a1 + a2) * min(f, 1.0), val=(Fk if 0 <= tau < P else 0), roi=tau >= P)
    return st

COLS = (140, 300, 460, 620, 780, 940)
def table(d, y, n, hl=None, glow=0.0, a=1.0, na=None):
    na = n if na is None else na
    card(d, (40, y, 1040, y + 360), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    for x, s in ((220, "m (kg)"), (540, "F (N)"), (860, "a (m/s²)")):
        text(d, (x, y + 50), s, 55, INK, alpha=a)
    for j, x in enumerate(COLS):
        text(d, (x, y + 122), "xe " + ("1" if j % 2 == 0 else "2"), 58, C1 if j % 2 == 0 else C2, alpha=a)
    for x in (380, 700): d.line([(x, y + 20), (x, y + 340)], fill=A(LIGHT, a), width=3)
    d.line([(60, y + 162), (1020, y + 162)], fill=A(LIGHT, a), width=3)
    for j, (m1, m2, Fk, a1, a2) in enumerate(RUNS):
        yy = y + 215 + j * 92
        if hl == j: d.rounded_rectangle([56, yy - 42, 1024, yy + 42], radius=18, fill=A(mix((245, 243, 255), GLOW, glow), a))
        vals = (f"{m1:g}", f"{m2:g}", f"{Fk:g}", f"{Fk:g}", a_str(a1), a_str(a2))
        for i, (x, v) in enumerate(zip(COLS, vals)):
            if j < n and (i < 4 or j < na): text(d, (x, yy), v, 58, C1 if i % 2 == 0 else C2, alpha=a)
            elif j < n: text(d, (x, yy), "…", 58, GRAY, alpha=a)
            else: text(d, (x, yy), "·", 58, GRAY, alpha=a)

def s_do(img, d, t, sc):
    st = do_state(t)
    v = f"{st['val']:g} N"
    rig(d, st["s1"], st["s2"], st["m1"], st["m2"], v, v, pin=st["pin"], lend=st["lend"], blk=st["blk"])
    if st["roi"]:                                  # da roi lo xo: hai xe troi deu ra hai phia
        x1, x2 = X1 - st["s1"], X2 + st["s2"]
        arrow(d, (x1 - CW / 2 - 10, 585), (x1 - CW / 2 - 80, 585), C1, w=8, head=22)
        arrow(d, (x2 + CW / 2 + 10, 585), (x2 + CW / 2 + 80, 585), C2, w=8, head=22)
        text(d, (540, 752), "đã rời lò xo", 55, MUTED)
    table(d, 800, st["n"], hl=(st["n"] - 1 if st["n"] > 0 else None), na=st["na"])

def _kiem_dong_bo():
    """Moi 0,05 s: hai cam bien cung so; so != 0 chi khi lo xo dang day; hang j chi hien khi lan j dang day,
    va luc hang hien thi cam bien dang chi dung F cua hang; xe khong ra ngoai khung."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        st = do_state(t); k = st["k"]; tau = t - TS[k] - PIN
        if st["val"] and not (0 <= tau < P): bad.append((round(t, 2), "so khi khong day"))
        if st["n"] > k + 1: bad.append((round(t, 2), "hang som"))
        if st["na"] > st["n"] or (st["na"] == k + 1 and tau < P + C - 1e-9): bad.append((round(t, 2), "a dien som"))
        if st["roi"] and st["val"]: bad.append((round(t, 2), "roi lo xo ma con so"))
        if X1 - st["s1"] - 150 < 40 or X2 + st["s2"] + 150 > 1040: bad.append((round(t, 2), "ra khung", st["s1"], st["s2"]))
        t += 0.05
    for j in range(2):
        st = do_state(TS[j] + ROW_AT + 1e-3)
        if st["val"] != RUNS[j][2] or st["n"] != j + 1: bad.append(("hang", j, st["val"], st["n"]))
    if TS[1] + ROW_AT > sc["T"] - 0.6: bad.append("hang cuoi qua muon")
    if TS[1] < BLK[1]: bad.append("chot rut truoc khi chat xong gia trong")
    return bad

# ---------------- canh 3: Dap an + rut ra ----------------
def pill(d, s, y, a, color=NAVY, size=55):
    pw = tw(d, s, F(size)) + 70
    card(d, (W / 2 - pw / 2, y - 44, W / 2 + pw / 2, y + 44), fill=A(color, a), r=42)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    table(d, 330, 2, hl=1, glow=pul(t))
    ka = appear(t, 2.0, 0.4)
    if ka > 0: pill(d, "ĐÁP ÁN · 4 N = 4 N", 790, ka)
    k1 = appear(t, M[1] + 0.3, 0.45)
    if k1 > 0:
        y0 = 900 + (1 - k1) * 20
        card(d, (60, y0, 1020, y0 + 150), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        text(d, (W / 2, y0 + 75), "Xe nặng: gia tốc nhỏ hơn", 58, DGREEN, alpha=k1)
        if k1 >= 0.98:                             # lap lai lan 2: cung luc, xe 1 kg di xa gap ba xe 3 kg
            q = ((t - M[1] - 0.8) % 2.6) / 2.0; q = min(max(q, 0.0), 1.0) ** 2
            yb = 1330
            d.line([(80, yb), (1000, yb)], fill=WOOD_D, width=5)
            for x0, x1_, col in ((400 - 88, 400 - 150 - 88, C1), (680 + 88, 680 + 50 + 88, C2)):   # vach xuat phat (xam) + vach dich
                for yy in range(int(yb - 150), int(yb), 24): d.line([(x0, yy), (x0, yy + 12)], fill=GRAY, width=4)
                for yy in range(int(yb - 150), int(yb), 24): d.line([(x1_, yy), (x1_, yy + 12)], fill=col, width=6)
                arrow(d, (x0, yb + 30), (x1_, yb + 30), col, w=6, head=18)
            f1, y = cart(d, 400 - 150 * q, yb, 1, C1, +1, s=0.8)
            f2, _ = cart(d, 680 + 50 * q, yb, 3, C2, -1, s=0.8)
            spring(d, f1, f1 + min(f2 - f1, 60 + 200 * min(q * 4, 1)), y, amp=16, n=9)

# ---------------- canh 4: Bay roi Chua noi duoc ----------------
def mini(d, y_trk, l1, l2, k, lab=None):
    """Hai xe nho 1 kg / 3 kg, mui ten luc lo xo day len moi xe (dai l1, l2 px), nhan 'luc len xe' duoi ban."""
    d.line([(80, y_trk), (1000, y_trk)], fill=WOOD_D, width=5)
    f1, y = cart(d, 330, y_trk, 1, C1, +1, s=0.8)
    f2, _ = cart(d, 750, y_trk, 3, C2, -1, s=0.8)
    spring(d, f1, f2, y, amp=18, n=11)
    ya = y_trk - 165
    if k > 0:
        if l1 > 4: arrow(d, (330, ya), (330 - l1 * ease(k), ya), C1, w=9, head=26)
        if l2 > 4: arrow(d, (750, ya), (750 + l2 * ease(k), ya), C2, w=9, head=26)
        if lab:
            text(d, (330 - l1 - 20, ya), lab, 55, C1, anchor="rm", alpha=k)
            text(d, (750 + l2 + 20, ya), lab, 55, C2, anchor="lm", alpha=k)
    text(d, (330, y_trk + 45), "lực lên xe 1", 55, C1); text(d, (750, y_trk + 45), "lực lên xe 2", 55, C2)

QS, QX = 60, 500                                   # co chu va tam cau bay (con cho dau ✗ lon ben phai)
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.1, 0.4)
    card(d, (40, 270, 1040, 720), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
    pw = tw(d, "BẪY", F(55)) + 60
    card(d, (W / 2 - pw / 2, 290, W / 2 + pw / 2, 366), fill=A(DRED, a1), r=38)
    text(d, (W / 2, 328), "BẪY", 55, WHITE, alpha=a1)
    q = "“Xe nặng bị đẩy mạnh hơn”"
    ks = clamp((t - 2.0) / 0.4); lw = tw(d, q, F(QS)); yy = 425; xq = QX
    text(d, (xq, yy), q, QS, INK, alpha=a1)
    if ks > 0: text(d, (xq + lw / 2 + 60, yy), "✗", 90, DRED, alpha=ks)
    if a1 >= 0.98: mini(d, 640, 60, 180, a1)
    k2 = appear(t, 2.6, 0.5)
    if k2 > 0:
        card(d, (40, 750, 1040, 1170), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=6)
        text(d, (100, 800), "✓", 70, DGREEN, alpha=k2)
        if k2 >= 0.98: text(d, (W / 2 + 30, 800), "Lực bằng nhau: 4 N = 4 N", 58, DGREEN)
        if k2 >= 0.98: mini(d, 1090, 120, 120, appear(t, 2.8, 0.5), lab="4 N")
    k3 = appear(t, M[1] + 0.1, 0.45)
    if k3 > 0:
        y0 = 1200 + (1 - k3) * 20
        card(d, (40, y0, 1040, y0 + 330), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        hlq = ease((t - M[1] - 2.6) / 0.3)            # vach sang chuyen tu y 1 sang y 2
        for j, w_ in ((0, 1 - hlq), (1, hlq)):
            if t > M[1] + 0.6:
                yb = y0 + 165 + j * 95
                d.rounded_rectangle([70, yb - 44, 1010, yb + 44], radius=18, fill=A((255, 247, 205), k3 * w_))
        text(d, (W / 2, y0 + 70), "Chỉ đúng khi:", 60, NAVY, alpha=k3)
        text(d, (100, y0 + 165), "• Lực lò xo không đổi", 60, INK, anchor="lm", alpha=k3)
        text(d, (100, y0 + 260), "• Ma sát rất nhỏ", 60, INK, anchor="lm", alpha=k3)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, M[1] + 0.1, 0.5)
    k0 = appear(t, 0.2, 0.5) * (1 - k1)            # an the chot khi cau hoi hien (khong nhac nua loi giai)
    card(d, (50, 270, 1030, 480), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 375, "Lực bằng nhau,\nxe nặng tăng tốc chậm", 58, DGREEN, maxw=900, alpha=k0)
    if k1 <= 0: return
    card(d, (40, 520, 1040, 1420), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(55)) + 60
    card(d, (W / 2 - pw / 2, 545, W / 2 + pw / 2, 621), fill=A(ORANGE, k1), r=38)
    text(d, (W / 2, 583), "THỬ NGHĨ", 55, WHITE, alpha=k1)
    ctext(d, 712, "Cảm biến lực xe 2\nchỉ bao nhiêu?", 58, INK, maxw=900, alpha=k1)
    if k1 < 0.98: return
    yb = 1240
    d.line([(80, yb), (1000, yb)], fill=WOOD_D, width=5)
    f1, y = cart(d, 300, yb, 2, C1, +1, s=0.9, blk=1.0)
    f2, _ = cart(d, 760, yb, 3, C2, -1, s=0.9)
    spring(d, f1, f2, y, amp=18, n=12)
    display(d, 760, f2 + 8, y, "?", C2, glow=pul(t - M[1]), lab=False, y0=850)
    text(d, (300, 920), "xe 1: a = 2,5 m/s²", 58, C1)
    ab = 0.35 + 0.65 * pul(t - M[1], 1.0)          # mui ten gia toc xe 1 nhap nhay
    arrow(d, (360, 1000), (220, 1000), A(C1, ab), w=10, head=26)
    text(d, (540, yb + 55), "bàn nhẵn", 55, MUTED)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding")]
    out += [(do["t0"] + TS[0] + PIN, "tap"), (do["t0"] + BLK[0], "tick"), (do["t0"] + TS[1] + PIN, "tap")]
    out += [(da["t0"] + 2.0, "ding"), (b["t0"] + 2.0, "buzz"), (e["t0"] + e["M"][1] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l10-newton3-05", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Định luật III Newton · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai xe đẩy và lò xo nén", draw=s_hook, tail=0.8, caps=[
   ("Lò xo nén giữa hai xe.", 3.4),
   ("Tự trả lời trước khi xem.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Rút chốt: hai xe bật ra.", 3.6),
   ("Xe 2 chất thêm gia trọng.", 4.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=1.0, caps=[
   ("Cả hai cảm biến: 4 N.", 3.4),
   ("So hai cột gia tốc.", 3.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Đúng hay sai?", 4.6),
   ("Còn giả thiết gì?", 5.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Chốt lại.", 3.6),
   ("Tự tính trước khi đọc tiếp.", 7.0)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
        print("số trong kho:", RUNS)
