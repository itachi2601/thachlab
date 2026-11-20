# Clip: tn-l12-thangnhietdo-01 - Tron nuoc nong voi nuoc lanh (ban 1, 28/10/2026; dung lai 21/11/2026 theo
# KE-HOACH-CAI-TIEN-CLIP viec 4 lo 20: cong --do-chu, chu >= 55 px khi ve, K10, Bay hinh tu giai thich).
# Quan niem sai can danh: HS lay trung binh cong hai nhiet do, bo qua khoi luong.
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-thangnhietdo-01.json -> so_lieu_mau (_kiem_so() doi chieu):
#   hang 2: 100 g 60 °C + 200 g 20 °C -> mo hinh 33,3 · do 32,9   (ca chinh cua clip, hop Du doan)
#   cau THU NGHI (= cau_chot khung web): 200 g 90 °C + 100 g 30 °C -> 70 °C (trong khoang tham_so; 46,7 hang 3 da co trong bang cua bai)
#   trung binh cong (60 + 20) : 2 = 40 = mo hinh hang 1 (chi dung o canh Bay).
# Du doan (K10: khong nut A-D, khong HOA goi y): "Nhiet ke dung o khoang bao nhieu?" -> dap an khoang 33 °C.
# Bay: don can tren thang nhiet do -- 100 g o vach 60, 200 g o vach 20. Diem tua o 40 (trung binh cong) -> nghieng;
#   doi diem tua toi 33,3 thi can (m1(t1 - t) = m2(t - t2) chinh la can bang momen). Nhip cuoi: chua noi duoc
#   (ca va khong khi nhan nhiet -> do 32,9 < tinh 33,3).
# Chot: hai phan deu la nuoc, bo qua nhiet ca nhan; hinh chi ve hai coc (khong ve thang, khong so gan 46,7).
from engine import *

M1, T1, M2, T2 = 100, 60, 200, 20        # so_lieu_mau hang 2
TCB_MH, TCB_DO = 33.3, 32.9               # hang 2: mo hinh, do
TBC = 40.0                                # (60 + 20) : 2 = mo hinh hang 1
CHOT = (200, 90, 100, 30, 70.0)           # cau chot (giai doan 2): trong khoang tham_so, dap so 70 khong co trong bai; khong hien


def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-thangnhietdo-01.json")))
    hang = [tuple(r) for r in k["so_lieu_mau"]["hang"]]
    assert (M1, T1, M2, T2, TCB_MH, TCB_DO) in hang
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    for key, v in zip(("m1", "t1", "m2", "t2"), CHOT[:4]): assert ts[key]["min"] <= v <= ts[key]["max"], key
    assert abs((CHOT[0] * CHOT[1] + CHOT[2] * CHOT[3]) / (CHOT[0] + CHOT[2]) - CHOT[4]) < 0.05
    assert any(h[0] == h[2] and h[4] == TBC == (h[1] + h[3]) / 2 for h in hang)
    assert abs((M1 * T1 + M2 * T2) / (M1 + M2) - TCB_MH) < 0.05
_kiem_so()


def f1(x): return f"{x:.1f}".replace(".", ",")


HOT_W = (253, 196, 160); COLD_W = (186, 216, 252)
DRED = (185, 28, 28); DBLUE = (29, 78, 216); DGREEN = (10, 110, 50); EMPTY = (148, 140, 128)
def wcol(tc): return mix(COLD_W, HOT_W, clamp((tc - 20) / 40))


# ---------------- hinh hoc: coc nghieng, mat nuoc luon nam ngang ----------------
def rot(p, c, a):
    ca, sa = math.cos(a), math.sin(a)
    return (c[0] + (p[0] - c[0]) * ca - (p[1] - c[1]) * sa, c[1] + (p[0] - c[0]) * sa + (p[1] - c[1]) * ca)


def clip_below(poly, ys):
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        pin, qin = p[1] >= ys, q[1] >= ys
        if pin: out.append(p)
        if pin != qin:
            k = (ys - p[1]) / (q[1] - p[1]); out.append((p[0] + (q[0] - p[0]) * k, ys))
    return out


def area(poly):
    return abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
                   for i in range(len(poly)))) / 2 if len(poly) > 2 else 0.0


def beaker(d, piv, w, h, ang, fill, col, steam_t=None, a=1.0):
    """Coc thuy tinh, goc tren-trai = piv, nghieng goc ang (am = do sang trai). fill = phan the tich nuoc."""
    x0, y0 = piv
    outer = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
    inner = [(x0 + 8, y0 + 4), (x0 + w - 8, y0 + 4), (x0 + w - 8, y0 + h - 8), (x0 + 8, y0 + h - 8)]
    O = [rot(p, piv, ang) for p in outer]; I = [rot(p, piv, ang) for p in inner]
    d.polygon(O, fill=A((240, 246, 252), a))
    if fill > 0.005:
        target = fill * area(I)
        lo, hi = min(p[1] for p in I), max(p[1] for p in I)
        for _ in range(30):
            mid = (lo + hi) / 2
            if area(clip_below(I, mid)) > target: lo = mid
            else: hi = mid
        ys = max(lo, piv[1] + 2)
        wp = clip_below(I, ys)
        if len(wp) > 2: d.polygon(wp, fill=A(col, a))
    d.line([O[0], O[3], O[2], O[1]], fill=A((110, 125, 150), a), width=6, joint="curve")
    if steam_t is not None:
        cx = (O[0][0] + O[1][0]) / 2
        for j in range(3):
            q = (steam_t * 0.55 + j / 3) % 1
            y = y0 - 14 - q * 90; x = cx - 45 + j * 45
            pts = [(x + 9 * math.sin((y - k * 10) / 16 + j * 2), y - k * 10) for k in range(5)]
            d.line(pts, fill=A((150, 158, 175), (1 - q) * a), width=7)


def seg_bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem 5 o cao 70 px, tat lan luot tu PHAI sang TRAI; o da tat: nen trang, vien dam."""
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 125, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 125, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=5)


def pill(d, y, s, col, a=1.0):
    pw = tw(d, s, F(56)) + 60
    card(d, (W / 2 - pw / 2, y, W / 2 + pw / 2, y + 76), fill=A(col, a), r=36)
    text(d, (W / 2, y + 38), s, 56, WHITE, alpha=a)


# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 215, 1040, 780), fill=WHITE, outline=LIGHT, w=3)
    beaker(d, (170, 300), 210, 280, 0, 0.4, wcol(60), steam_t=t)
    beaker(d, (700, 300), 210, 280, 0, 0.8, wcol(20))
    text(d, (W / 2, 440), "+", 90, INK)
    text(d, (275, 650), "100 g", 62, RED); text(d, (275, 722), "60 °C", 62, RED)
    text(d, (805, 650), "200 g", 62, BLUE); text(d, (805, 722), "20 °C", 62, BLUE)
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 820 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 610), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, y0 + 24, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 175), "Khuấy đều xong,", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 275), "Nhiệt kế dừng", 62, PURPLE, alpha=a)
    text(d, (W / 2, y0 + 355), "ở khoảng bao nhiêu?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 460, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, a)


# ---------------- canh 2: Tien hanh ----------------
CX0, CX1, CY0, CY1 = 120, 480, 520, 900          # ca tron
PRB_X = 170                                       # que do nhiet ke dien tu
SCR = (640, 590, 1010, 900)                       # man hinh nhiet ke
P_MOVE, P_TILT, P_END = 0.6, 1.2, 2.9             # nhac coc, nghieng, rot het
P_LID = 3.3                                       # day nap + khuay (truoc phu de 2)
MIX0, MIX1 = 3.4, 6.0                             # hai phan tien ve nhau
P_READ = 6.3                                      # so dung yen (ngay truoc phu de 3)


def ca(d, level, tc, lid, stir):
    ix0, ix1, ib = CX0 + 10, CX1 - 10, CY1 - 10
    d.rectangle([CX0, CY0, CX1, CY1], fill=(240, 246, 252))
    wy = ib - (ib - CY0 - 10) * level
    d.rectangle([ix0, wy, ix1, ib], fill=wcol(tc))
    d.line([(ix0, wy), (ix1, wy)], fill=(120, 160, 215), width=4)
    d.line([(CX0, CY0), (CX0, CY1), (CX1, CY1), (CX1, CY0)], fill=(110, 125, 150), width=8, joint="curve")
    if lid > 0:
        sx = 390 + 30 * math.sin(stir * 2 * math.pi * 1.4)
        d.line([(sx + 30, CY0 - 90), (sx, CY1 - 40)], fill=A((150, 155, 170), lid), width=10)
        y = CY0 - 22 * lid
        d.rounded_rectangle([CX0 - 18, y - 16, CX1 + 18, y + 10], radius=8, fill=A(NAVY, lid))
    d.line([(PRB_X, CY0 - 60), (PRB_X, CY1 - 30)], fill=(120, 128, 145), width=10)
    dot(d, PRB_X, CY1 - 30, 9, NAVY)
    d.line([(PRB_X, CY0 - 100), (825, CY0 - 100), (825, SCR[1])], fill=NAVY, width=6, joint="curve")
    d.rounded_rectangle([PRB_X - 22, CY0 - 120, PRB_X + 22, CY0 - 60], radius=8, fill=NAVY)


def screen(d, s):
    card(d, SCR, fill=WHITE, outline=NAVY, r=28, w=4)
    cx = (SCR[0] + SCR[2]) / 2
    text(d, (cx, SCR[1] + 50), "Nhiệt kế", 56, INK)
    d.rounded_rectangle([SCR[0] + 30, SCR[1] + 96, SCR[2] - 30, SCR[1] + 216], radius=16, fill=NAVY)
    text(d, (cx, SCR[1] + 156), s, 72, (134, 239, 172))
    text(d, (cx, SCR[1] + 264), "°C", 56, INK)


SX0, SX1 = 160, 920                                # thang nhiet do 20-60 °C
def XT(tc): return SX0 + (tc - 20) / 40 * (SX1 - SX0)


def axis(d, y, a=1.0, step=20):
    d.line([(XT(20) - 20, y), (XT(60) + 20, y)], fill=A(NAVY, a), width=6)
    for tc in range(20, 61, 10):
        d.line([(XT(tc), y - 14), (XT(tc), y + 14)], fill=A(NAVY, a), width=5)
        if (tc - 20) % step == 0: text(d, (XT(tc), y + 56), str(tc), 58, INK, alpha=a)


def s_do(img, d, t, sc):
    text(d, (60, 250), "Số liệu minh hoạ", 56, INK, bold=False, anchor="lm")
    mv = ease((t - P_MOVE) / (P_TILT - P_MOVE))
    tl = ease((t - P_TILT) / (P_END - P_TILT - 0.6))
    piv = (lerp(720, 330, mv), lerp(330, 455, mv))
    ang = math.radians(-95 * tl)
    pour = clamp((t - P_TILT - 0.4) / (P_END - P_TILT - 0.4))
    k_mix = ease((t - MIX0) / (MIX1 - MIX0))
    t_hot, t_cold = lerp(T1, TCB_DO, k_mix), lerp(T2, TCB_DO, k_mix)
    tc_ca = T2 if pour <= 0 else lerp(T2, lerp(T2 + 13.3, TCB_DO, k_mix), clamp(pour * 1.2))  # chi to mau nuoc
    lid = appear(t, P_LID, 0.4)
    ca(d, 0.4 + 0.2 * pour, tc_ca, lid, max(0, t - P_LID))
    bh_a = 1 - appear(t, P_END + 0.1, 0.4)
    if bh_a > 0.02:
        if 0.02 < pour < 1:
            wy = CY1 - 10 - (CY1 - CY0 - 20) * (0.4 + 0.2 * pour)
            d.line([(piv[0] - 4, piv[1]), (piv[0] - 12, wy)], fill=A(HOT_W, bh_a), width=16)
        beaker(d, piv, 180, 210, ang, 0.75 * (1 - pour), wcol(60), a=bh_a)
        la = 1 - appear(t, P_MOVE, 0.3)
        if la > 0: text(d, (810, 290), "100 g · 60 °C", 56, RED, alpha=la)
    if t < P_TILT + 0.4: screen(d, f1(T2))
    elif t < P_READ: screen(d, "···")
    else: screen(d, f1(TCB_DO))
    # thang: hai phan tien ve nhau
    card(d, (60, 960, 1020, 1210), fill=WHITE, outline=LIGHT, w=3)
    y = 1080
    axis(d, y)
    if t >= P_READ:
        dot(d, XT(TCB_DO), y, 24, GREEN, outline=WHITE)
    else:
        if k_mix > 0.04 and t_hot - t_cold > 6:
            arrow(d, (XT(t_hot) - 30, y - 40), (XT(t_cold) + 30, y - 40), ORANGE, w=6, head=18)
        for tc, col, lab in ((t_hot, RED, "nóng"), (t_cold, BLUE, "lạnh")):
            dot(d, XT(tc), y, 20, col, outline=WHITE)
            if k_mix < 0.3: text(d, (XT(tc), y - 70), lab, 56, col)
    # bang so lieu
    card(d, (60, 1240, 1020, 1660), fill=WHITE, outline=NAVY, w=4)
    xs = [270, 640, 870]
    text(d, (xs[1], 1295), "m (g)", 56, INK); text(d, (xs[2], 1295), "t (°C)", 56, INK)
    d.line([(90, 1335), (990, 1335)], fill=LIGHT, width=4)
    rows = [("Nước nóng", str(M1), str(T1), RED), ("Nước lạnh", str(M2), str(T2), BLUE), ("Hỗn hợp", "", f1(TCB_DO), GREEN)]
    for i, (n, m, tt, col) in enumerate(rows):
        yy = 1400 + i * 85
        if i == 2:
            a = appear(t, P_READ, 0.35)
            if a > 0: d.rounded_rectangle([80, yy - 38, 1000, yy + 38], radius=16, fill=A((220, 252, 231), a))
            text(d, (xs[0], yy), n, 58, INK)
            text(d, (xs[2], yy), tt, 60, DGREEN, alpha=a)
            continue
        text(d, (xs[0], yy), n, 58, INK)
        text(d, (xs[1], yy), m, 60, col); text(d, (xs[2], yy), tt, 60, col)


# ---------------- canh 3: Ket qua + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    k = appear(t, 0.15, 0.4)
    y0 = 220 + (1 - k) * 25
    card(d, (60, y0, 1020, y0 + 120), fill=A((220, 252, 231), k), outline=A(GREEN, k), w=5)
    text(d, (W / 2, y0 + 60), "Đáp án: khoảng 33 °C", 62, DGREEN, alpha=k)
    card(d, (40, 380, 1040, 900), fill=WHITE, outline=LIGHT, w=3)
    y = 640
    axis(d, y, step=10)
    text(d, (XT(20), 470), "200 g", 60, BLUE); text(d, (XT(60), 470), "100 g", 60, RED)
    dot(d, XT(20), y, 20, BLUE, outline=WHITE); dot(d, XT(60), y, 20, RED, outline=WHITE)
    dot(d, XT(TCB_DO), y, 24, GREEN, outline=WHITE)
    text(d, (XT(TCB_DO) + 30, 560), "32,9", 60, DGREEN, anchor="lm")
    # nhip 2: nong ha nhieu (mui ten dai), lanh tang it (mui ten ngan)
    g = ease((t - (M[1] - 0.1)) / 1.0)
    if g > 0:
        yr, yb = 790, 850
        arrow(d, (XT(60), yr), (lerp(XT(60), XT(TCB_DO) + 6, g), yr), RED, w=9, head=26)
        arrow(d, (XT(20), yb), (lerp(XT(20), XT(TCB_DO) - 6, g), yb), BLUE, w=9, head=26)
    # nhip 3: nhiet nang nong -> lanh, toi khi cung nhiet do (can bang nhiet)
    a = appear(t, M[2] - 0.1, 0.45)
    if a <= 0: return
    card(d, (60, 940, 1020, 1560), fill=A(WHITE, a), outline=A(GREEN, a), w=5)
    text(d, (W / 2, 1020), "Nhiệt năng: nóng → lạnh", 62, ORANGE, alpha=a)
    q = ease((t - (M[2] + 0.4)) / 1.8)
    ch = mix(HOT_W, wcol(TCB_DO), q); cc = mix(COLD_W, wcol(TCB_DO), q)
    card(d, (170, 1120, 450, 1330), fill=A(ch, a), outline=A((110, 125, 150), a), r=24, w=5)
    card(d, (630, 1120, 910, 1330), fill=A(cc, a), outline=A((110, 125, 150), a), r=24, w=5)
    if q < 0.98:
        off = 40 * ((t * 1.2) % 1)
        arrow(d, (470 + off, 1225), (560 + off, 1225), A(ORANGE, a * (1 - q)), w=10, head=26)
    else:
        text(d, (W / 2, 1225), "=", 80, DGREEN, alpha=a)
    text(d, (W / 2, 1455), "Cân bằng nhiệt", 64, DGREEN, alpha=a)


# ---------------- canh 4: Bay - don can tren thang nhiet do; chua noi duoc ----------------
BY, AY = 700, 900                                  # beam (khi nam ngang), truc thang
def lever(d, pv, ang, mood):
    """Thanh can = thang 20-60 °C; diem tua o nhiet do pv; ang < 0 la nghieng xuong phia 20 °C."""
    P = (XT(pv), BY)
    e1, e2 = rot((XT(20) - 40, BY), P, ang), rot((XT(60) + 40, BY), P, ang)
    d.line([e1, e2], fill=NAVY, width=14)
    for tc in range(20, 61, 10):                                       # vach tren thanh can
        a1, a2 = rot((XT(tc), BY - 14), P, ang), rot((XT(tc), BY + 14), P, ang)
        d.line([a1, a2], fill=WHITE, width=4)
    d.polygon([(P[0], BY + 8), (P[0] - 55, AY - 14), (P[0] + 55, AY - 14)], fill=mood)  # diem tua
    for tc, h, col, lab in ((20, 190, BLUE, "200 g"), (60, 95, RED, "100 g")):
        cx, cy = rot((XT(tc), BY - 7), P, ang)
        card(d, (cx - 100, cy - h, cx + 100, cy), fill=col, r=14)
        text(d, (cx, cy - h / 2), lab, 56, WHITE)


def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (60, 215, 1020, 335), fill=(254, 242, 242), outline=RED, w=5)
    text(d, (W / 2, 275), "Hay nghĩ: (60 + 20) : 2 = 40", 58, DRED)
    card(d, (40, 360, 1040, 1010), fill=WHITE, outline=LIGHT, w=3)
    axis(d, AY, step=10)
    tip = ease((t - (M[1] - 0.1)) / 0.9)                               # nhip 2: tha tay -> nghieng
    sl = ease((t - (M[2] - 0.1)) / 1.2)                                # nhip 3: doi diem tua toi 33,3
    pv = lerp(TBC, TCB_MH, sl)
    ang = math.radians(-9) * tip * (1 - sl)
    lever(d, pv, ang, DRED if sl < 0.5 else DGREEN)
    kl = appear(t, M[2] + 1.0, 0.4)                                    # cung luc the "Cân bằng" (mot khoi chu)
    if kl > 0: text(d, (XT(TCB_MH) + 70, AY - 70), "t cuối 33,3 °C", 58, DGREEN, anchor="lm", alpha=kl)
    k4 = appear(t, M[3] - 0.1, 0.45)
    kx = appear(t, M[1] + 0.5, 0.4) * (1 - appear(t, M[2] - 0.1, 0.3))
    if kx > 0 and k4 < 0.05:
        card(d, (60, 1050, 1020, 1170), fill=A((254, 242, 242), kx), outline=A(RED, kx), r=24, w=5)
        text(d, (W / 2, 1110), "✗ Không cân", 62, DRED, alpha=kx)
    kv = appear(t, M[2] + 1.0, 0.4) * (1 - k4)
    if kv > 0:
        card(d, (60, 1050, 1020, 1170), fill=A((236, 253, 243), kv), outline=A(GREEN, kv), r=24, w=5)
        text(d, (W / 2, 1110), "✓ Cân bằng", 62, DGREEN, alpha=kv)
    if k4 <= 0: return
    card(d, (60, 1050, 1020, 1640), fill=A(WHITE, k4), outline=A(NAVY, k4), w=6)
    text(d, (W / 2, 1125), "Chưa nói được", 62, NAVY, alpha=k4)
    x0, x1, y0, y1 = 120, 400, 1240, 1520                             # ca nho, nhiet thoat ra thanh va khong khi
    d.rectangle([x0, y0, x1, y1], fill=A((240, 246, 252), k4))
    d.rectangle([x0 + 10, y0 + 90, x1 - 10, y1 - 10], fill=A(wcol(TCB_DO), k4))
    d.line([(x0, y0), (x0, y1), (x1, y1), (x1, y0)], fill=A((110, 125, 150), k4), width=8)
    ph = (t * 0.8) % 1
    for (ax, ay, dx, dy) in ((x0 + 40, y0 + 190, -1, 0), (x1 - 40, y0 + 190, 1, 0), ((x0 + x1) / 2, y0 + 70, 0, -1)):
        s = 30 + 40 * ph
        arrow(d, (ax + dx * s, ay + dy * s), (ax + dx * (s + 60), ay + dy * (s + 60)), A(ORANGE, k4 * (1 - 0.6 * ph)), w=8, head=20)
    text(d, ((x0 + x1) / 2 + 14, 1576), "nhiệt thoát ra", 56, (176, 64, 8), alpha=k4)
    text(d, (750, 1340), "Đo: 32,9 °C", 62, DGREEN, alpha=k4)
    text(d, (750, 1460), "Tính: 33,3 °C", 62, NAVY, alpha=k4)


# ---------------- canh 5: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1500), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, 238, "THỬ NGHĨ", ORANGE, k1)
    beaker(d, (180, 380), 200, 270, 0, 0.8, wcol(90), a=k1)
    beaker(d, (700, 380), 200, 270, 0, 0.4, wcol(30), a=k1)
    text(d, (W / 2, 515), "+", 90, INK, alpha=k1)
    text(d, (280, 720), "200 g", 62, RED, alpha=k1); text(d, (280, 792), "90 °C", 62, RED, alpha=k1)
    text(d, (800, 720), "100 g", 62, BLUE, alpha=k1); text(d, (800, 792), "30 °C", 62, BLUE, alpha=k1)
    text(d, (W / 2, 935), "Nhiệt kế dừng gần mức nào?", 62, ORANGE, alpha=k1)
    text(d, (W / 2, 1045), "Bỏ qua nhiệt ca nhận.", 62, INK, alpha=k1)
    seg_bar(d, 1170, t, 1.0, sc["T"] - 0.2, ORANGE, k1)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = (sc[k] for k in ("hook", "do", "dapan", "bay", "end"))
    return [(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
            (do["t0"] + P_TILT + 0.4, "tap"), (do["t0"] + P_READ, "ding"),
            (da["t0"] + 0.15, "ding"), (b["t0"] + b["M"][1] - 0.1, "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"),
            (e["t0"] + 0.15, "open")]


CLIP = dict(id="tn-l12-thangnhietdo-01", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
            footer="Thang nhiệt độ · thachlab.id.vn", scenes=[
 dict(key="hook", title="Trộn hai phần nước", draw=s_hook, tail=0.3, caps=[
   ("Đổ chung hai cốc nước.", 3.0),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Đổ nước nóng vào ca.", 3.0),
   ("Đậy nắp, khuấy đều.", 3.0),
   ("Số đứng yên thì ghi.", 3.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Gần phía nước lạnh hơn.", 3.0),
   ("Nóng hạ nhiều, lạnh tăng ít.", 3.4),
   ("Tới khi cùng nhiệt độ.", 3.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Chỉ lấy trung bình cộng?", 3.0),
   ("Bỏ quên khối lượng.", 3.0),
   ("Điểm tựa là nhiệt độ cuối.", 3.6),
   ("Ca cũng nhận ít nhiệt.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 6.2)]),
])
