# Clip: tn-l12-thangnhietdo-01 - Tron nuoc nong voi nuoc lanh: hai nhiet do tien ve mot gia tri (ban 1, 28/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-thangnhietdo-01.json -> so_lieu_mau (so lieu minh hoa):
#   hang 1: 100 g 60 °C + 100 g 20 °C -> mo hinh 40,0 · do 39,1
#   hang 2: 100 g 60 °C + 200 g 20 °C -> mo hinh 33,3 · do 32,9   (ca chinh cua clip)
#   hang 3: 200 g 60 °C + 100 g 20 °C -> mo hinh 46,7 (chi dung lam lua chon nhieu D)
# Lua chon nhieu (hop Du doan, ca hang 2): A 20,0 = t2 (nong nguoi tan xuong nhiet do nuoc lanh),
#   C 40,0 = trung binh cong (t1 + t2)/2 = mo hinh hang 1, D 46,7 = mo hinh hang 3 (lech nham ve phia nuoc nong).
# Canh: Du doan -> Tien hanh (do nong vao ca, khuay, hai nhiet do tien ve mot gia tri) -> Dap an B + Rut ra
#       (so hang 1 voi hang 2) -> Bay (trung binh cong) + sai so (32,9 < 33,3) + chua noi duoc -> Chot + cau hoi.
import random
from engine import *

M1, T1, M2, T2 = 100, 60, 200, 20        # so_lieu_mau hang 2
TCB_MH, TCB_DO = 33.3, 32.9               # hang 2: mo hinh, do
EQ_TCB, EQ_MH = 39.1, 40.0                # hang 1 (hai khoi luong bang nhau)


def f1(x): return f"{x:.1f}".replace(".", ",")


HOT_W = (253, 196, 160); COLD_W = (186, 216, 252)
def wcol(tc): return mix(COLD_W, HOT_W, clamp((tc - 20) / 40))


def tag(d, alpha=1.0, full=False):
    """Nhan 'So lieu minh hoa' duoi tieu de (JSON ghi so lieu minh hoa); chi canh do ghi day du, canh khac ghi 'Minh hoạ'."""
    s = "Số liệu minh hoạ" if full else "Minh hoạ"; wd = tw(d, s, F(36, False)) + 44
    card(d, (W / 2 - wd / 2, 226, W / 2 + wd / 2, 276), fill=A((241, 238, 230), alpha), r=25)
    text(d, (W / 2, 251), s, 36, MUTED, bold=False, alpha=alpha)


# ---------------- hinh hoc: coc nghieng, mat nuoc luon nam ngang ----------------
def rot(p, c, a):
    ca, sa = math.cos(a), math.sin(a)
    return (c[0] + (p[0] - c[0]) * ca - (p[1] - c[1]) * sa, c[1] + (p[0] - c[0]) * sa + (p[1] - c[1]) * ca)


def clip_below(poly, ys):
    """Phan da giac loi nam duoi duong y = ys (y lon hon)."""
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


def beaker(d, piv, w, h, ang, fill, col, steam_t=None):
    """Coc thuy tinh, goc tren-trai = piv, nghieng goc ang (am = do sang trai). fill = phan the tich nuoc."""
    x0, y0 = piv
    outer = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
    inner = [(x0 + 8, y0 + 4), (x0 + w - 8, y0 + 4), (x0 + w - 8, y0 + h - 8), (x0 + 8, y0 + h - 8)]
    O = [rot(p, piv, ang) for p in outer]; I = [rot(p, piv, ang) for p in inner]
    d.polygon(O, fill=(240, 246, 252))
    if fill > 0.005:
        target = fill * area(I)
        lo, hi = min(p[1] for p in I), max(p[1] for p in I)
        for _ in range(30):
            mid = (lo + hi) / 2
            if area(clip_below(I, mid)) > target: lo = mid
            else: hi = mid
        ys = max(lo, piv[1] + 2)            # khong cao hon mieng coc
        wp = clip_below(I, ys)
        if len(wp) > 2: d.polygon(wp, fill=col)
    d.line([O[0], O[3], O[2], O[1]], fill=(110, 125, 150), width=6, joint="curve")
    if steam_t is not None:
        cx = (O[0][0] + O[1][0]) / 2
        for j in range(3):
            q = (steam_t * 0.55 + j / 3) % 1
            y = y0 - 14 - q * 90; x = cx - 45 + j * 45
            pts = [(x + 9 * math.sin((y - k * 10) / 16 + j * 2), y - k * 10) for k in range(5)]
            d.line(pts, fill=A((175, 180, 195), 1 - q), width=5)


# ---------------- canh 1: mo bai + du doan ----------------
OPTS = ("A. 20 °C", "B. 33 °C", "C. 40 °C", "D. 60 °C")
BW, BH = 220, 300


def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    tag(d)
    beaker(d, (150, 450), BW, BH, 0, 0.4, wcol(60), steam_t=t)
    beaker(d, (710, 450), BW, BH, 0, 0.8, wcol(20))
    text(d, (540, 600), "+", 80, INK)
    text(d, (260, 800), "100 g · 60 °C", 42, RED); text(d, (260, 856), "nước nóng", 36, INK, bold=False)
    text(d, (820, 800), "200 g · 20 °C", 42, BLUE); text(d, (820, 856), "nước lạnh", 36, INK, bold=False)
    k = appear(t, sc["M"][1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (60, 940, 1020, 1600), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 995), "Dự đoán", 46, PURPLE, alpha=k)
    ctext(d, 1130, "Nhiệt kế dừng ở khoảng bao nhiêu?", 48, INK, alpha=k)
    for i, s in enumerate(OPTS):
        a = appear(t, sc["M"][1] + 0.2 + i * 0.15)
        x0 = 110 + (i % 2) * 440; y = 1290 + (i // 2) * 116
        card(d, (x0, y - 46, x0 + 420, y + 46), fill=A((245, 243, 255), a), outline=A(PURPLE, a), r=22, w=4)
        text(d, (x0 + 34, y), s, 42, INK, anchor="lm", alpha=a)
    t1, t2 = sc["M"][1] + 0.6, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1548, 940, 1562], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1548, 140 + 800 * (1 - q), 1562], radius=7, fill=A(PURPLE, k))


# ---------------- canh 2: do nuoc nong vao ca, khuay, doc nhiet ke ----------------
CX0, CX1, CY0, CY1 = 120, 480, 520, 900          # ca tron (thanh ngoai)
PRB_X = 170                                       # que do nhiet ke dien tu
SCR = (650, 590, 1010, 880)                       # man hinh nhiet ke
# moc trong canh (giay)
P_MOVE, P_TILT, P_END = 2.9, 3.6, 5.3              # nhac coc, nghieng, rot het
P_LID = 5.4                                        # day nap + bat dau khuay
P_READ = 8.2                                      # so dung yen (truoc phu de 4 doc 32,9)


def mix_k(t):
    """0 -> 1: muc do hai phan tien ve nhau (sau khi rot, khuay)."""
    return ease((t - 5.2) / (7.7 - 5.2))


def ca(d, t, level, tc, lid, stir):
    ix0, ix1, ib = CX0 + 10, CX1 - 10, CY1 - 10
    d.rectangle([CX0, CY0, CX1, CY1], fill=(240, 246, 252))
    wy = ib - (ib - CY0 - 10) * level
    d.rectangle([ix0, wy, ix1, ib], fill=wcol(tc))
    d.line([(ix0, wy), (ix1, wy)], fill=(120, 160, 215), width=4)
    d.line([(CX0, CY0), (CX0, CY1), (CX1, CY1), (CX1, CY0)], fill=(110, 125, 150), width=8, joint="curve")
    text(d, ((CX0 + CX1) / 2, CY1 + 40), "ca trộn", 36, INK, bold=False)
    # que khuay
    if lid > 0:
        sx = 390 + 30 * math.sin(stir * 2 * math.pi * 1.4)
        d.line([(sx + 30, CY0 - 90), (sx, CY1 - 40)], fill=A((150, 155, 170), lid), width=10)
        y = CY0 - 22 * lid
        d.rounded_rectangle([CX0 - 18, y - 16, CX1 + 18, y + 10], radius=8, fill=A(NAVY, lid))
    # que do + day noi man hinh (ve truoc coc nuoc nong -> coc che len day)
    d.line([(PRB_X, CY0 - 60), (PRB_X, CY1 - 30)], fill=(120, 128, 145), width=10)
    dot(d, PRB_X, CY1 - 30, 9, NAVY)
    d.line([(PRB_X, CY0 - 100), (830, CY0 - 100), (830, SCR[1])], fill=NAVY, width=6, joint="curve")
    d.rounded_rectangle([PRB_X - 22, CY0 - 120, PRB_X + 22, CY0 - 60], radius=8, fill=NAVY)


def screen(d, s, sub=None):
    card(d, SCR, fill=WHITE, outline=LIGHT, r=28, w=4)
    text(d, ((SCR[0] + SCR[2]) / 2, SCR[1] + 46), "Nhiệt kế", 36, MUTED, bold=False)
    d.rounded_rectangle([SCR[0] + 30, SCR[1] + 84, SCR[2] - 30, SCR[1] + 200], radius=16, fill=NAVY)
    text(d, ((SCR[0] + SCR[2]) / 2, SCR[1] + 142), s, 64, (134, 239, 172))
    text(d, ((SCR[0] + SCR[2]) / 2, SCR[1] + 246), sub or "°C", 34, MUTED, bold=False)


SX0, SX1, SY = 140, 940, 1110                      # thang nhiet do ngang 10-70 °C
def SXv(tc): return SX0 + (tc - 10) / 60 * (SX1 - SX0)


def scale(d, y=SY, alpha=1.0):
    d.line([(SX0, y), (SX1, y)], fill=A(NAVY, alpha), width=5)
    for tc in range(10, 71, 10):
        d.line([(SXv(tc), y - 12), (SXv(tc), y + 12)], fill=A(NAVY, alpha), width=4)
        text(d, (SXv(tc), y + 44), str(tc), 34, INK, bold=False, alpha=alpha)
    text(d, (SX1 + 30, y + 44), "°C", 34, INK, bold=False, anchor="lm", alpha=alpha)


def marker(d, tc, y, col, lab, up=True, alpha=1.0, r=18):
    dot(d, SXv(tc), y, r, A(col, alpha), outline=WHITE)
    if lab: text(d, (SXv(tc), y - 70 if up else y + 96), lab, 36, col, alpha=alpha)


def s_do(img, d, t, sc):
    IMG_REF[0] = img
    tag(d, full=True)
    # coc nuoc nong: nhac len, nghieng, rot het roi mo di
    mv = ease((t - P_MOVE) / (P_TILT - P_MOVE))
    tl = ease((t - P_TILT) / (P_END - P_TILT - 0.6))
    piv = (lerp(700, 330, mv), lerp(300, 455, mv))
    ang = math.radians(-95 * tl)
    pour = clamp((t - P_TILT - 0.4) / (P_END - P_TILT - 0.4))   # phan nuoc da rot sang ca
    hot_fill = 0.75 * (1 - pour)
    k_mix = mix_k(t)
    t_hot, t_cold = lerp(T1, TCB_DO, k_mix), lerp(T2, TCB_DO, k_mix)
    tc_ca = T2 if pour <= 0 else lerp(T2, lerp(T2 + 13.3, TCB_DO, k_mix), clamp(pour * 1.2))  # chi de to mau nuoc
    lid = appear(t, P_LID, 0.4)
    ca(d, t, 0.4 + 0.2 * pour, tc_ca, lid, max(0, t - P_LID))
    bh_a = 1 - appear(t, P_END + 0.1, 0.4)
    if bh_a > 0.02:
        if 0.02 < pour < 1:
            wy = CY1 - 10 - (CY1 - CY0 - 20) * (0.4 + 0.2 * pour)
            d.line([(piv[0] - 4, piv[1]), (piv[0] - 12, wy)], fill=A(HOT_W, bh_a), width=16)
        beaker(d, piv, 180, 210, ang, hot_fill, wcol(60), steam_t=None)
        if mv < 0.05: text(d, (790, 272), "100 g · 60 °C", 36, RED, alpha=bh_a)
    # man hinh nhiet ke: truoc khi rot do nuoc lanh, dang tron hien '···' (khong in so noi suy)
    if t < P_TILT + 0.4: screen(d, f1(T2))
    elif t < P_READ: screen(d, "···")
    else: screen(d, f1(TCB_DO))
    # thang nhiet do: hai phan tien ve nhau
    card(d, (60, 960, 1020, 1240), fill=WHITE, outline=LIGHT, w=3)
    text(d, (100, 1000), "Hai phần nước", 36, MUTED, anchor="lm")
    scale(d)
    if t >= P_READ:
        marker(d, TCB_DO, SY, GREEN, f1(TCB_DO), r=22)
    else:
        if k_mix > 0.04 and t_hot - t_cold > 6:
            arrow(d, (SXv(t_hot) - 28, SY - 34), (SXv(t_cold) + 28, SY - 34), ORANGE, w=5, head=16)
        marker(d, t_hot, SY, RED, "nóng" if k_mix < 0.45 else None)
        marker(d, t_cold, SY, BLUE, "lạnh" if k_mix < 0.45 else None)
    # bang so lieu
    card(d, (60, 1270, 1020, 1600), fill=WHITE, outline=NAVY, w=4)
    xs = [260, 610, 860]
    for x, c in zip(xs, ["", "m (g)", "t (°C)"]): text(d, (x, 1316), c, 36, MUTED)
    d.line([(90, 1346), (990, 1346)], fill=LIGHT, width=4)
    rows = [("Nước nóng", str(M1), f1(T1), RED, 0.2), ("Nước lạnh", str(M2), f1(T2), BLUE, 0.2),
            ("Hỗn hợp", "", f1(TCB_DO), GREEN, P_READ)]
    for i, (n, m, tt, col, at) in enumerate(rows):
        a = appear(t, at, 0.35); y = 1398 + i * 72
        if a <= 0: continue
        if i == 2: d.rounded_rectangle([80, y - 32, 1000, y + 32], radius=16, fill=A((220, 252, 231), a))
        text(d, (260, y), n, 40, INK, alpha=a)
        text(d, (610, y), m, 42, col, alpha=a)
        text(d, (860, y), tt, 42, col, alpha=a)
        if i == 2: text(d, (980, y), "→ B", 40, GREEN, anchor="rm", alpha=a)


# ---------------- canh 3: dap an + so hai hang ----------------
def panel(d, t, y0, title, tcb, mh, mc, hl, a):
    card(d, (60, y0, 1020, y0 + 340), fill=A(WHITE, a), outline=A(ORANGE if hl else LIGHT, a), w=5 if hl else 3)
    text(d, (W / 2, y0 + 46), title, 38, INK, alpha=a)
    y = y0 + 180
    d.line([(SX0, y), (SX1, y)], fill=A(NAVY, a), width=5)
    for tc in range(10, 71, 10):
        d.line([(SXv(tc), y - 12), (SXv(tc), y + 12)], fill=A(NAVY, a), width=4)
    for tc in (20, 40, 60):
        text(d, (SXv(tc), y + 42), str(tc), 34, INK, bold=False, alpha=a)
    # khoi luong o hai dau
    text(d, (SXv(60), y + 96), f"{mh} g", 36, RED, alpha=a)
    text(d, (SXv(20), y + 96), f"{mc} g", 36, BLUE, alpha=a)
    dot(d, SXv(60), y, 14, A(RED, a)); dot(d, SXv(20), y, 14, A(BLUE, a))
    dot(d, SXv(tcb), y, 20, A(GREEN, a), outline=WHITE)
    text(d, (SXv(tcb), y - 52), f1(tcb), 40, GREEN, alpha=a)


def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    tag(d)
    k = back((t - 0.15) / 0.5) if t > 0.15 else 0
    card(d, (60, 300, 1020, 396), fill=(220, 252, 231), outline=GREEN, w=5)
    text(d, (W / 2, 348), "Đáp án B: 32,9 °C", int(48 * clamp(k, 0.3, 1.0)), GREEN)
    hl1 = M[0] - 0.1 <= t < M[1] - 0.1
    panel(d, t, 420, "100 g + 100 g", EQ_TCB, 100, 100, hl1, appear(t, 0.3))
    panel(d, t, 780, "100 g + 200 g", TCB_DO, M1, M2, M[1] - 0.1 <= t < M[2] - 0.1, appear(t, 0.5))
    if t > M[0] - 0.1:   # vach trung binh cong o hang 1
        ka = appear(t, M[0] + 0.3)
        y = 600
        text(d, (SXv(EQ_MH) + 64, y - 52), "giữa: 40,0", 34, MUTED, anchor="lm", alpha=ka)
    for i, (s, col, at) in enumerate((("Lệch về phía nước nhiều", BLUE, M[1] - 0.1),
                                       ("Dừng khi cùng nhiệt độ", GREEN, M[2] - 0.1))):
        a = appear(t, at, 0.4); y0 = 1190 + i * 190
        if a <= 0: continue
        card(d, (60, y0, 1020, y0 + 130), fill=A(WHITE, a), outline=A(col, a), w=4, r=26)
        text(d, (W / 2, y0 + 65), s, 46, col, alpha=a)


# ---------------- canh 4: bay + sai so + chua noi duoc gi ----------------
def s_trap(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    tag(d)
    card(d, (60, 300, 1020, 396), fill=(254, 226, 226), outline=RED, w=5)
    text(d, (W / 2, 348), "Bẫy: trung bình cộng", 46, RED)
    # thang phong to 30-42 °C: 40,0 (gach), 33,3 tinh theo mo hinh, 32,9 do (cach nhau ~27 px)
    ZX = lambda tc: 150 + (tc - 30) / 12 * 780
    card(d, (60, 420, 1020, 724), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 458), "30–42 °C", 38, MUTED)
    y = 620
    d.line([(ZX(30), y), (ZX(42), y)], fill=NAVY, width=5)
    for tc in range(30, 43, 2):
        d.line([(ZX(tc), y - 12), (ZX(tc), y + 12)], fill=NAVY, width=4)
        text(d, (ZX(tc), y + 44), str(tc), 34, INK, bold=False)
    a0 = appear(t, 0.1, 0.3)
    dot(d, ZX(EQ_MH), y, 16, A(RED, a0), outline=WHITE)
    text(d, (ZX(EQ_MH), y - 66), "40,0", 38, RED, alpha=a0)
    ax = appear(t, 0.7, 0.3)
    if ax > 0:
        c = ZX(EQ_MH)
        d.line([(c - 26, y - 26), (c + 26, y + 26)], fill=A(RED, ax), width=7)
        d.line([(c - 26, y + 26), (c + 26, y - 26)], fill=A(RED, ax), width=7)
    a1 = appear(t, 1.0, 0.35)
    c = ZX(TCB_MH)
    dot(d, c, y, 12, A(BLUE, a1), outline=WHITE)
    d.line([(c, y - 14), (c + 30, y - 52)], fill=A(BLUE, a1), width=3)
    text(d, (c + 36, y - 66), "33,3 tính", 36, BLUE, anchor="lm", alpha=a1)
    a2 = appear(t, M[1] - 0.2, 0.35)
    if a2 > 0:
        c = ZX(TCB_DO)
        dot(d, c, y, 12, A(GREEN, a2), outline=WHITE)
        d.line([(c, y - 14), (c - 30, y - 52)], fill=A(GREEN, a2), width=3)
        text(d, (c - 36, y - 66), "32,9 đo", 36, GREEN, anchor="rm", alpha=a2)
    # vung duoi doi the: bay -> sai so -> chua noi duoc
    k1 = appear(t, 0.3, 0.4); k3 = appear(t, M[2] - 0.1, 0.4)
    b1 = k1 * (1 - k3)
    y0 = 780
    if b1 > 0:
        card(d, (60, y0, 1020, y0 + 520), fill=A(WHITE, b1), outline=A(RED, b1), w=5)
        ctext(d, y0 + 150, "(60 + 20) : 2 = 40,0 → SAI", 52, RED, alpha=b1)
        ctext(d, y0 + 340, "Nước nhiều kéo về phía nó", 52, GREEN, alpha=b1)
    if k3 > 0:
        card(d, (60, y0, 1020, y0 + 520), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 52, NAVY, alpha=k3)
        for j, h in enumerate(("Nhiệt ca nhận bao nhiêu?", "Chất khác thì sao?")):
            yy = y0 + 220 + j * 120
            text(d, (110, yy), "•", 50, NAVY, anchor="lm", alpha=k3)
            text(d, (160, yy), h, 48, INK, anchor="lm", alpha=k3)


# ---------------- canh 5: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]

    def body(d, t, k):                            # hai coc cua cau hoi (chi khoi luong, khong so dap an)
        if k <= 0.05: return
        beaker(d, (250, 1000), 150, 190, 0, 0.8, wcol(60))
        beaker(d, (680, 1000), 150, 190, 0, 0.4, wcol(20))
        text(d, (W / 2, 1095), "+", 64, INK, alpha=k)
        text(d, (325, 1236), "200 g", 40, RED, alpha=k)
        text(d, (755, 1236), "100 g", 40, BLUE, alpha=k)

    chot_hoi(d, t, sc, "Nóng truyền cho lạnh tới khi cân bằng nhiệt",
             "Trộn 200 g nước 60\u00a0°C với 100 g nước 20\u00a0°C. Nhiệt độ cuối gần mức nào?",
             body=body)
    kh = appear(t, M[0] + 2.5, 0.5)              # goi y tu ve, hien tre ~2,5 s
    if kh <= 0: return
    card(d, (110, 1300, 970, 1540), fill=A((255, 237, 213), kh), outline=A(ORANGE, kh), r=24, w=4)
    text(d, (W / 2, 1355), "Gợi ý", 40, ORANGE, alpha=kh)
    ctext(d, 1460, "Nhớ ca 100 g + 200 g.", 46, INK, maxw=820, alpha=kh)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + P_TILT + 0.4, "tap"), (do["t0"] + P_READ, "ding"),
            (an["t0"] + an["M"][2], "tap"), (tr["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]


CLIP = dict(id="tn-l12-thangnhietdo-01", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
            footer="Thang nhiệt độ · thachlab.id.vn", scenes=[
 dict(key="hook", title="Trộn nước nóng với nước lạnh", draw=s_hook, tail=0.6, caps=[
   ("Trộn, khuấy đều.", 2.5),
   ("Dừng video, chọn A–D.", 5.5)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Nước lạnh trong ca.", 2.5),
   ("Đổ nước nóng, khuấy đều.", 2.9),
   ("Nóng hạ, lạnh tăng.", 2.5),
   ("Đáp án B.", 2.5)]),
 dict(key="ans", title="Vì sao là 32,9 °C?", draw=s_ans, tail=0.6, caps=[
   ("Hai khối bằng nhau.", 2.8),
   ("Lạnh gấp đôi.", 2.8),
   ("Nóng sang lạnh.", 2.8)]),
 dict(key="trap", title="Bẫy và sai số", draw=s_trap, tail=0.6, caps=[
   ("Nhìn vạch 40,0.", 3.0),
   ("Đo thấp hơn tính.", 3.5),
   ("Giới hạn thí nghiệm.", 3.5)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video, tự trả lời.", 6.5)]),
])
