# Clip: tn-l12-udcamung-01 - Nam cham va cuon day noi loa qua bo khuech dai
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-udcamung-01.json (so lieu minh hoa tu mo hinh e = -N.dPhi/dt):
#   N = 500 vong, dPhi = 20 uWb ; vao cham dt = 0,4 s -> e = -0,025 V (keu rat khe) ; vao nhanh 0,05 s -> -0,2 V (keu ro) ;
#   rut ra nhanh 0,05 s -> +0,2 V (keu ro, xung nguoc chieu) ; giu yen -> 0 (im).
# Ban 2 (26/11/2026, viec 4 lo 32, cong --do-chu moi): canh hook / do / ans / bay / gioi / end nhu mau xoaychieu2.
#   Du doan (K10 khong ve nut; khung web hoi A-D): dua vao roi giu yen -> luc giu yen loa the nao? -> im
#     (hien_tuong_hay_sai[0] "nam cham manh dat trong cuon thi co dong"). Hop exp trong bai da neu "giu yen: loa im"
#     o dong Quan sat (lo dap an) -> bao phien chinh, khong sua bai.
#   Bay (hien_tuong_hay_sai[2]): "vao va ra cho dong cung chieu" -> hai xung -0,2 V / +0,2 V canh nhau.
#   Chot (khung web A-D, dap so KHONG hien; ca da ghi trong ghi_chu kho): cuon 1000 vong, dua vao trong 0,2 s
#     -> |e| = 1000 . 2.10^-5 / 0,2 = 0,1 V. Nhieu: 0,05 V (giu N = 500), 0,2 V (chep so do nhanh), 0,4 V (quen doi dt).
#   Bo canh pickup ghi ta (Cau 1 sau hop da hoi) de giu <= 50 s.
# Toa do mp4 = 65 + 0,88.x; chu than canh ve >= 56 px (ra >= 49 px).
from engine import *

COP = (184, 115, 51)
DARK_OR = (181, 71, 8)
DGREEN = (21, 128, 61)
N_TURN, DPHI = 500, 2e-5
for dt_, e_ in ((0.4, -0.025), (0.05, -0.2)): assert abs(-N_TURN * DPHI / dt_ - e_) < 1e-9
assert abs(1000 * DPHI / 0.2 - 0.1) < 1e-12                                   # ca chot
SLOW = 6.0                                     # hinh chay cham 6 lan

# ---------------- bo cuc ----------------
CX, CY, CR = 675, 520, 105                     # cuon nam ngang: tam, nua chieu cao vong
CL, CRR, NT = 540, 810, 10
ML, MH = 200, 72                               # nam cham ngang, N ben TRAI (quay vao cuon)
TIP_OUT, TIP_IN = 850, 570                     # dau N: ngoai cuon / trong cuon (duoi S toi 1050)
def _trace(ang, ml, inset=10):
    nx, sx = -inset, -ml + inset
    x, y = nx + 6 * math.cos(ang), -6 * math.sin(ang); pts = [(x, y)]
    for _ in range(4000):
        ex = ey = 0.0
        for px, q in ((nx, 1), (sx, -1)):
            dx, dy = x - px, y; r3 = (dx * dx + dy * dy) ** 1.5; ex += q * dx / r3; ey += q * dy / r3
        n = math.hypot(ex, ey); x += 3 * ex / n; y += 3 * ey / n; pts.append((x, y))
        if math.hypot(x - sx, y) < 8: break
    return pts
_RAW = [_trace(math.radians(a), ML) for a in (60, 82, 104)]
_SQ = 150 / max(-y for _, y in _RAW[0])
FIELD = [[(x, y * _SQ) for x, y in ln] for ln in _RAW]

def dashed_poly(d, pts, color, w=4, seg=10, gap=8):
    acc, on, cur = 0.0, True, [pts[0]]
    for p, q in zip(pts, pts[1:]):
        acc += math.dist(p, q); cur.append(q)
        if acc >= (seg if on else gap):
            if on and len(cur) > 1: d.line(cur, fill=color, width=w)
            on, acc, cur = not on, 0.0, [q]
    if on and len(cur) > 1: d.line(cur, fill=color, width=w)

def chevron(d, x, y, ang, color, s=16, w=4):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=color, width=w)

def field(d, tip, cy=CY):
    """N o ben trai (dau N tai x = tip), S o ben phai. Cuc bo (x, w): x <= 0 ve phia S -> man hinh (tip - x, cy + w)."""
    c = A(PURPLE, 0.7)
    for ln in FIELD:
        for sg in (1, -1):
            pts = [(tip - x, cy + sg * w) for x, w in ln]
            dashed_poly(d, pts, c)
            k = max(range(len(pts)), key=lambda n: abs(pts[n][1] - cy))      # dinh cung: mui ten N -> S (sang phai)
            (x0, y0), (x1, y1) = pts[max(0, k - 3)], pts[min(len(pts) - 1, k + 3)]
            chevron(d, pts[k][0], pts[k][1], math.atan2(y1 - y0, x1 - x0), c)
    dashed_poly(d, [(tip - 6 - 4 * j, cy) for j in range(27)], c)   # duong suc truc (net dut)   # ra khoi N (sang trai)

def magnet(d, tip, cy=CY, s=1.0):
    ml, mh = ML * s, MH * s; xm, x1 = tip + ml / 2, tip + ml
    d.rounded_rectangle([tip, cy - mh / 2, xm, cy + mh / 2], radius=10, fill=RED)
    d.rounded_rectangle([xm, cy - mh / 2, x1, cy + mh / 2], radius=10, fill=BLUE)
    d.rectangle([xm - 10, cy - mh / 2, xm, cy + mh / 2], fill=RED)
    d.rectangle([xm, cy - mh / 2, xm + 10, cy + mh / 2], fill=BLUE)
    if s < 1: return                                   # nam cham thu nho: chi giu hai mau
    for xx, ch in ((tip + ml / 4, "N"), (x1 - ml / 4, "S")):
        if xx > CRR + 30: text(d, (xx, cy + 1), ch, 56, WHITE)     # trong cuon: bo chu (vong truoc che chu)

def turns(cl=CL, cr=CRR, nt=NT): return [cl + j * (cr - cl) / (nt - 1) for j in range(nt)]
def coil_back(d, cl=CL, cr=CRR, cy=CY, r=CR, nt=NT):
    for x in turns(cl, cr, nt): d.arc([x - 16, cy - r, x + 16, cy + r], 90, 270, fill=mix(COP, BG, 0.45), width=6)
def coil_front(d, cl=CL, cr=CRR, cy=CY, r=CR, nt=NT):
    for x in turns(cl, cr, nt): d.arc([x - 16, cy - r, x + 16, cy + r], 270, 90, fill=COP, width=8)

def speaker(d, lvl, x=150, y=560):
    """Loa nho, mieng huong len; lvl: 0 im, 1 rat khe, 3 ro (so vong song am + do dam)."""
    d.rectangle([x - 34, y, x + 34, y + 44], fill=NAVY)
    d.polygon([(x - 34, y), (x + 34, y), (x + 74, y - 70), (x - 74, y - 70)], fill=(70, 80, 120))
    d.line([(x - 74, y - 70), (x + 74, y - 70)], fill=NAVY, width=6)
    for j in range(lvl):
        r = 50 + 34 * j
        d.arc([x - r - 20, y - 110 - r, x + r + 20, y - 110 + r], 215, 325, fill=A(ORANGE, 1.0 - 0.18 * j), width=7 if lvl > 1 else 4)

def rig(d, tip, lvl, lab=True):
    field(d, tip)
    coil_back(d); magnet(d, tip); coil_front(d)
    if lab: text(d, (CX, 345), "cuộn 500 vòng", 56, INK)
    # day: hai dau cuon -> bo khuech dai -> loa
    d.line([(CL, CY + CR - 6), (CL, 700), (500, 700)], fill=NAVY, width=5)
    d.line([(CRR, CY + CR - 6), (CRR, 745), (500, 745)], fill=NAVY, width=5)
    card(d, (170, 662, 500, 782), fill=WHITE, outline=NAVY, r=14, w=5)
    text(d, (335, 722), "khuếch đại", 56, NAVY)
    d.line([(170, 722), (110, 722), (110, 604)], fill=NAVY, width=5)
    speaker(d, lvl, x=110)

# ---------------- do thi e(t) + bang ----------------
EX0, EX1, PXV = 110, 1010, 560                 # truc t, px moi von
ROWS = [("Vào chậm", "0,4", "−0,025", "khẽ"), ("Giữ yên", "—", "0", "im"),
        ("Rút nhanh", "0,05", "+0,2", "rõ"), ("Vào nhanh", "0,05", "−0,2", "rõ")]

def chart_frame(d, alpha=1.0, y0=810, y1=1150):
    card(d, (40, y0, 1040, y1), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    ey = (y0 + y1) / 2 + 10
    d.line([(EX0, ey), (EX1, ey)], fill=A(NAVY, alpha), width=4)
    d.line([(EX0, y0 + 30), (EX0, y1 - 20)], fill=A(NAVY, alpha), width=4)
    chevron(d, EX1, ey, 0, A(NAVY, alpha), 18, 4); chevron(d, EX0, y0 + 30, -math.pi / 2, A(NAVY, alpha), 18, 4)
    text(d, (EX0 + 22, y0 + 50), "e", 60, INK, anchor="lm", alpha=alpha)
    text(d, (EX1 - 4, ey + 44), "t", 60, INK, anchor="rm", alpha=alpha)
    return ey

def pulse(u):  # hinh xung tron (0..1 -> 0..1..0)
    return math.sin(math.pi * clamp(u)) ** 2 if 0 < u < 1 else 0.0

TB0 = 1170
def table(d, n, alpha=1.0):
    card(d, (40, TB0, 1040, TB0 + 420), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    cols = (220, 500, 710, 920)
    for x, s in zip(cols, ("(minh hoạ)", "Δt (s)", "e (V)", "Loa")): text(d, (x, TB0 + 46), s, 56, NAVY, alpha=alpha)
    d.line([(70, TB0 + 86), (1010, TB0 + 86)], fill=A(LIGHT, alpha), width=3)
    for j, r in enumerate(ROWS[:n]):
        yy = TB0 + 86 + 80 * (j + 0.5) + 2
        for x, s in zip(cols, r): text(d, (x, yy), s, 56, INK, alpha=alpha)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    rig(d, TIP_OUT, 0)
    a = appear(t, M[1] - 0.4, 0.5)
    if a <= 0: return
    y0 = 880 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 104), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 64), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    text(d, (W / 2, y0 + 185), "Đưa vào, rồi giữ yên.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 285), "Lúc giữ yên, loa thế nào?", 60, INK, alpha=a)
    tc, te = M[1] + 0.3, sc["T"] - 0.1                  # thanh dem lien, cao 120 px
    p = clamp((t - tc) / (te - tc))
    d.rounded_rectangle([110, y0 + 400, 970, y0 + 520], radius=24, fill=A(LIGHT, a))
    if p < 1: d.rounded_rectangle([110, y0 + 400, 110 + 860 * (1 - p), y0 + 520], radius=24, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
# su kien (bat dau, thoi gian hinh, tu, toi, e (V)); hinh = dt that x SLOW. Moi hang bang moi cach nhau >= 2 s.
def events(sc):
    s1 = sc["M"][0] + 0.6; s3 = sc["M"][1]
    return [(s1, 0.4 * SLOW, TIP_OUT, TIP_IN, -0.025),            # vao cham
            (s1 + 0.4 * SLOW, None, TIP_IN, TIP_IN, 0.0),        # giu yen (toi s3)
            (s3, 0.05 * SLOW, TIP_IN, TIP_OUT, 0.2),             # rut ra nhanh
            (s3 + 2.2, 0.05 * SLOW, TIP_OUT, TIP_IN, -0.2)]      # vao nhanh
CH_T0 = 0.5
def xs(sc): return (EX1 - 40 - EX0) / (sc["T"] - 0.3 - CH_T0)

def e_at(t, sc):
    for (s, dur, a, b, e) in events(sc):
        if dur and s <= t <= s + dur: return e * pulse((t - s) / dur)
    return 0.0

def state_do(t, sc):
    ev = events(sc); tip, lvl, n = TIP_OUT, 0, 0
    for j, (s, dur, a, b, e) in enumerate(ev):
        if t < s: break
        if dur is None:                       # giu yen: hang bang hien sau 2,0 s im
            tip = a; lvl = 0; n = 2 if t >= s + 2.0 else 1
            continue
        u = clamp((t - s) / dur); tip = lerp(a, b, ease(u))
        lvl = (1 if abs(e) < 0.1 else 3) if u < 1 else 0
        n = {0: 1, 2: 3, 3: 4}[j] if u >= 1 else n
    return tip, lvl, n

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    tip, lvl, n = state_do(t, sc)
    rig(d, tip, lvl)
    ey = chart_frame(d)
    text(d, (1010, 855), "chạy chậm", 56, INK, anchor="rm")
    if t > CH_T0:
        k = xs(sc); pts = []; tt = CH_T0
        while tt <= t:
            pts.append((EX0 + (tt - CH_T0) * k, ey - e_at(tt, sc) * PXV)); tt += 1 / 60
        if len(pts) > 1: d.line(pts, fill=ORANGE, width=7, joint="curve")
        x = pts[-1][0]; d.line([(x, ey - 130), (x, ey + 130)], fill=A(GRAY, 0.6), width=3)
    table(d, n)

# ---------------- canh 3: Dap an + Rut ra ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    rig(d, TIP_IN, 0, lab=False)
    s = "ĐÁP ÁN: loa im"; pw = tw(d, s, F(60)) + 70             # hien ngay tu 0 s (mot khoi chu)
    card(d, (W / 2 - pw / 2, 290, W / 2 + pw / 2, 370), fill=GREEN, r=40)
    text(d, (W / 2, 330), s, 60, WHITE)
    k = appear(t, 2.6, 0.45)
    if k <= 0: return
    card(d, (40, 840, 1040, 1560), fill=A(WHITE, k), outline=A(GREEN, k), w=5)
    text(d, (W / 2, 930), "Từ thông đổi → có dòng", 62, DGREEN, alpha=k)
    text(d, (W / 2, 1070), "e = −N·ΔΦ/Δt", 72, NAVY, alpha=k)
    k2 = appear(t, 4.8, 0.45)
    if k2 > 0:
        d.line([(100, 1170), (980, 1170)], fill=A(LIGHT, k2), width=3)
        text(d, (W / 2, 1260), "Giữ yên: ΔΦ = 0", 64, INK, alpha=k2)
        text(d, (W / 2, 1380), "→ e = 0", 72, DGREEN, alpha=k2)

# ---------------- canh 4: Bay ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    b1, b2, b3 = (m - 0.1 for m in sc["M"])
    k1, k2, k3 = appear(t, b1, 0.4), appear(t, b2, 0.4), appear(t, b3, 0.4)
    pw = tw(d, "BẪY", F(56)) + 60
    card(d, (W / 2 - pw / 2, 260, W / 2 + pw / 2, 336), fill=A(RED, k1), r=38)
    text(d, (W / 2, 298), "BẪY", 56, WHITE, alpha=k1)
    text(d, (W / 2, 420), "Vào và ra:", 64, INK, alpha=k1)
    text(d, (W / 2, 505), "dòng cùng chiều?", 64, RED, alpha=k1)
    card(d, (40, 580, 1040, 1180), fill=A(WHITE, k1), outline=A(NAVY, k1), w=4)
    ey = 880
    d.line([(90, ey), (1000, ey)], fill=A(NAVY, k1), width=4)
    for x0, sg, lab, sub, col in ((180, -1, "−0,2 V", "vào", BLUE), (640, 1, "+0,2 V", "ra", ORANGE)):
        text(d, (x0 + 110, 625), sub, 60, col, alpha=k1)
        if k2 > 0:
            pts = [(x0 + u * 220, ey - sg * 200 * pulse(u)) for u in [i / 50 for i in range(51)]]
            d.line(pts, fill=A(col, k2), width=8, joint="curve")
            text(d, (x0 + 110, (ey + 70) if sg > 0 else (ey - 70)), lab, 60, col, alpha=k2)
    if k3 > 0:
        pw2 = tw(d, "SAI", F(56)) + 50
        card(d, (1030 - pw2, 260, 1030, 336), fill=A((127, 29, 29), k3), r=38)
        text(d, (1030 - pw2 / 2, 298), "SAI", 56, WHITE, alpha=k3)
        card(d, (40, 1230, 1040, 1420), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
        text(d, (W / 2, 1325), "e đổi dấu: ngược chiều", 64, DGREEN, alpha=k3)

# ---------------- canh 5: Chua noi duoc gi ----------------
def s_gioi(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.2, 0.4); kb = appear(t, 2.4, 0.4)
    card(d, (40, 300, 1040, 1300), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    for j, s in enumerate(("• Chiều dòng: cần điện kế", "• Số vôn: cần đo")):
        text(d, (110, 600 + j * 260), s, 68, INK, anchor="lm", alpha=kb)
    text(d, (W / 2, 800), "?", 260, NAVY, alpha=k * (1 - kb))

# ---------------- canh 6: THU NGHI (cau_chot cua khung; dap so KHONG hien) ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.3, 0.5)
    card(d, (40, 260, 1040, 1180), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 285, W / 2 + pw / 2, 365), fill=A(DARK_OR, k), r=40)
    text(d, (W / 2, 325), "THỬ NGHĨ", 56, WHITE, alpha=k)
    text(d, (W / 2, 450), "Cuộn 1000 vòng, cùng nam châm,", 60, INK, alpha=k)
    text(d, (W / 2, 535), "đưa vào trong 0,2 s.", 60, INK, alpha=k)
    text(d, (W / 2, 640), "|e| = ?", 72, DARK_OR, alpha=k)
    # cuon nho + nam cham truot vao/ra cham (khong ve loa, khong so)
    cy = 900; u = 0.5 - 0.5 * math.cos(2 * math.pi * t / 3.0)
    coil_back(d, 330, 640, cy, 85, 12); magnet(d, lerp(800, 380, u), cy, 0.85); coil_front(d, 330, 640, cy, 85, 12)
    text(d, (485, 1050), "1000 vòng", 56, INK, alpha=k)
    arrow(d, (990, 1040), (850, 1040), A(ORANGE, k), w=8, head=26)          # chieu dua vao
    kh = appear(t, 3.3, 0.5)
    if kh > 0:
        card(d, (90, 1230, 990, 1380), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1305), "Gợi ý: ΔΦ mỗi vòng = 20 µWb", 60, DARK_OR, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, b, g, e = (sc[k] for k in ("hook", "do", "ans", "bay", "gioi", "end"))
    return ([(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + s, "tap") for s, dur, *_ in events(do) if dur]
            + [(an["t0"] + 0.1, "ding"), (b["t0"] + b["M"][0] - 0.1, "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"),
               (g["t0"] + 2.4, "tap"), (e["t0"] + 0.3, "open")])

CLIP = dict(id="tn-l12-udcamung-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Ứng dụng cảm ứng điện từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Cuộn dây nối loa", draw=s_hook, tail=0.3, caps=[
   ("Nam châm đặt ngoài cuộn.", 3.0),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Đưa vào chậm, rồi giữ yên.", 6.8),
   ("Rút ra nhanh, đưa vào nhanh.", 2.6)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.4, caps=[
   ("Nam châm nằm yên trong cuộn.", 3.0),
   ("Vì sao im?", 4.2)]),
 dict(key="bay", title="Bẫy", draw=s_bay, tail=0.3, caps=[
   ("Đúng hay sai?", 3.0),
   ("So hai xung đo được.", 3.0),
   ("Dòng đảo chiều.", 3.0)]),
 dict(key="gioi", title="Chưa nói được gì?", draw=s_gioi, tail=0.3, caps=[
   ("Loa chưa cho biết:", 4.0)]),
 dict(key="end", title="Tự kiểm tra", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự tính.", 6.4)]),
])
