# Clip: tn-l12-udcamung-01 - Nam cham va cuon day noi loa qua bo khuech dai (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-udcamung-01.json (so lieu minh hoa tu mo hinh e = -N.dPhi/dt):
#   N = 500 vong, dPhi = 20 uWb ; vao cham dt = 0,4 s -> e = -0,025 V (keu rat khe) ; vao nhanh 0,05 s -> -0,2 V (keu ro) ;
#   rut ra nhanh 0,05 s -> +0,2 V (keu ro, xung nguoc chieu) ; giu yen -> 0 (im).
# Phien chinh 14/11: hop trong bai ghi "tai nghe (hoac loa nho qua bo khuech dai)" -> ve loa CO hop "khuếch đại" o giua.
# Bo cuc KHAC dttruong1 (ong dung + do thi e-v) va udcamung2 (hai cuon + dien ke): cuon NAM NGANG, nam cham vao tu phai,
#   loa + khuech dai ben trai, do thi e(t) chay theo thoi gian (xung rong/hep theo dt, ti le 0,4 : 0,05) + bang 4 hang.
# Hinh chay cham: ca hai lan vao/ra deu cham 6 lan (0,4 s -> 2,4 s ; 0,05 s -> 0,3 s) nen do rong xung dung ti le dt.
# Du doan (khung ben canh, K10 khong ve nut A-D trong mp4):
#   "Dua nam cham vao cuon roi giu yen trong do. Trong luc giu yen, loa the nao?"
#   A. Keu deu, khong dut   B. Im, khong keu (DUNG)   C. Keu to hon luc dua vao   D. Keu khe, deu deu
#   (A/C/D deu tu quan niem sai "nam cham manh dat trong cuon thi cuon co dong" - hien_tuong_hay_sai[0])
# Bay (hien_tuong_hay_sai[2]): "dua vao va rut ra cho dong cung chieu" -> sai: e = -0,2 V va +0,2 V, doi dau.
# Chua noi duoc (khong_chung_minh): loa khong cho biet chieu dong, khong do ra von (so trong bang tinh tu mo hinh).
# Ket noi pickup (cong B 14/11): chi "Ghi ta dien: day thep rung tren cuon day" + hinh day rung; KHONG noi tu hoa /
#   nam cham nho / cung tan so (de Cau 1 sau hop cho HS tu suy).
# Ca chot cho ghi_chu kho: "Cuon 1000 vong, dua cung nam cham vao trong 0,2 s -> |e| = 0,1 V".
# Cau chot THU NGHI (ca moi, so moi N = 1000, dt = 0,2 s chua hien; hai dai luong cung doi -> khong phai mot phep tinh):
#   "Cuon 1000 vong, dua cung nam cham vao trong 0,2 s. Do lon e khoang bao nhieu?"
#   -> |e| = 1000 . 2.10^-5 / 0,2 = 0,1 V. goi_y (du kien): "ΔΦ mỗi vòng vẫn 20 µWb".
from engine import *

NOTE = (70, 75, 95)
COP = (184, 115, 51)
N_TURN, DPHI = 500, 2e-5
# so trong bang = mo hinh (kiem)
for dt_, e_ in ((0.4, -0.025), (0.05, -0.2)): assert abs(-N_TURN * DPHI / dt_ - e_) < 1e-9
SLOW = 6.0                                     # hinh chay cham 6 lan

# ---------------- bo cuc ----------------
CX, CY, CR = 620, 520, 105                     # cuon nam ngang: tam, nua chieu cao vong
CL, CRR, NT = 480, 760, 10
ML, MH = 230, 76                               # nam cham ngang, N ben TRAI (quay vao cuon)
TIP_OUT, TIP_IN = 820, 510                     # dau N: ngoai cuon / trong cuon

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
    c = A(PURPLE, 0.5)
    for ln in FIELD:
        for sg in (1, -1):
            pts = [(tip - x, cy + sg * w) for x, w in ln]
            dashed_poly(d, pts, c)
            k = max(range(len(pts)), key=lambda n: abs(pts[n][1] - cy))      # dinh cung: mui ten N -> S (sang phai)
            (x0, y0), (x1, y1) = pts[max(0, k - 3)], pts[min(len(pts) - 1, k + 3)]
            chevron(d, pts[k][0], pts[k][1], math.atan2(y1 - y0, x1 - x0), c)
    d.line([(tip - 110, cy), (tip - 6, cy)], fill=c, width=4); chevron(d, tip - 110, cy, math.pi, c)   # ra khoi N (sang trai)

def magnet(d, tip, cy=CY, s=1.0):
    ml, mh = ML * s, MH * s; xm, x1 = tip + ml / 2, tip + ml
    d.rounded_rectangle([tip, cy - mh / 2, xm, cy + mh / 2], radius=10, fill=RED)
    d.rounded_rectangle([xm, cy - mh / 2, x1, cy + mh / 2], radius=10, fill=BLUE)
    d.rectangle([xm - 10, cy - mh / 2, xm, cy + mh / 2], fill=RED)
    d.rectangle([xm, cy - mh / 2, xm + 10, cy + mh / 2], fill=BLUE)
    if s < 1: return                                   # nam cham thu nho: chi giu hai mau
    for xx, ch in ((tip + ml / 4, "N"), (x1 - ml / 4, "S")):
        if xx > CRR + 30: text(d, (xx, cy + 1), ch, 44, WHITE)     # trong cuon: bo chu (vong truoc che chu)

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
    if lab: text(d, (CX, 345), "cuộn 500 vòng", 44, NOTE)
    # day: hai dau cuon -> bo khuech dai -> loa
    d.line([(CL, CY + CR - 6), (CL, 700), (440, 700)], fill=NAVY, width=5)
    d.line([(CRR, CY + CR - 6), (CRR, 740), (440, 740)], fill=NAVY, width=5)
    card(d, (220, 672, 440, 768), fill=WHITE, outline=NAVY, r=14, w=5)
    text(d, (330, 720), "khuếch đại", 40, NAVY)
    d.line([(220, 720), (150, 720), (150, 604)], fill=NAVY, width=5)
    speaker(d, lvl)

# ---------------- do thi e(t) + bang ----------------
EX0, EX1, EY0, PXV = 110, 1010, 985, 600        # truc t, duong e = 0, px moi von
ROWS = [("Vào chậm", "0,4", "−0,025", "rất khẽ"), ("Giữ yên", "—", "0", "im"),
        ("Rút ra nhanh", "0,05", "+0,2", "rõ"), ("Vào nhanh", "0,05", "−0,2", "rõ")]

def chart_frame(d, alpha=1.0, y0=800, y1=1160):
    card(d, (40, y0, 1040, y1), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    ey = (y0 + y1) / 2 + 5
    d.line([(EX0, ey), (EX1, ey)], fill=A(NAVY, alpha), width=3)
    d.line([(EX0, y0 + 30), (EX0, y1 - 20)], fill=A(NAVY, alpha), width=3)
    chevron(d, EX1, ey, 0, A(NAVY, alpha), 16, 3); chevron(d, EX0, y0 + 30, -math.pi / 2, A(NAVY, alpha), 16, 3)
    text(d, (EX0 + 18, y0 + 44), "e", 44, INK, anchor="lm", alpha=alpha)
    text(d, (EX1 - 4, ey + 36), "t", 44, INK, anchor="rm", alpha=alpha)
    return ey

def pulse(u):  # hinh xung tron (0..1 -> 0..1..0)
    return math.sin(math.pi * clamp(u)) ** 2 if 0 < u < 1 else 0.0

def table(d, n, y0=1190, alpha=1.0):
    card(d, (40, y0, 1040, y0 + 400), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    cols = (230, 520, 715, 915)
    for x, s in zip(cols, ("Thao tác", "Δt (s)", "e (V)", "Loa")): text(d, (x, y0 + 44), s, 42, NOTE, bold=False, alpha=alpha)
    d.line([(70, y0 + 80), (1010, y0 + 80)], fill=A(LIGHT, alpha), width=3)
    for j, r in enumerate(ROWS[:n]):
        yy = y0 + 80 + 72 * (j + 0.5) + 4
        for x, s in zip(cols, r): text(d, (x, yy), s, 42, INK, alpha=alpha)
    text(d, (1020, y0 + 440), "số liệu minh hoạ", 40, NOTE, bold=False, anchor="rm", alpha=alpha)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, TIP_OUT, 0)
    a = appear(t, M[0] + 1.6, 0.5)
    if a <= 0: return
    y0 = 880 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(42)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 59), "DỰ ĐOÁN", 42, WHITE, alpha=a)
    text(d, (W / 2, y0 + 170), "Đưa nam châm vào cuộn,", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 235), "rồi giữ yên.", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 320), "Lúc giữ yên, loa thế nào?", 48, INK, alpha=a)
    text(d, (W / 2, y0 + 410), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=a)
    tc, tend = M[0] + 2.0, sc["T"] - 0.15
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 490, 940, y0 + 504], radius=7, fill=A(LIGHT, a))
        if p < 1: d.rounded_rectangle([140, y0 + 490, 140 + 800 * (1 - p), y0 + 504], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
# su kien (bat dau, thoi gian hinh, tu, toi, e (V), so hang bang khi xong); hinh = dt that x SLOW
def events(sc):
    s1 = sc["M"][0] + 0.8; s3 = sc["M"][1] + 0.6
    return [(s1, 0.4 * SLOW, TIP_OUT, TIP_IN, -0.025),            # vao cham
            (s1 + 0.4 * SLOW, None, TIP_IN, TIP_IN, 0.0),        # giu yen (toi s3)
            (s3, 0.05 * SLOW, TIP_IN, TIP_OUT, 0.2),             # rut ra nhanh
            (s3 + 1.5, 0.05 * SLOW, TIP_OUT, TIP_IN, -0.2)]      # vao nhanh
CH_T0 = 0.6                                                      # moc t tren do thi = luc bat dau ve
def xs(sc):  # px/s cua truc t (hinh): het do thi luc canh gan het
    return (EX1 - 40 - EX0) / (sc["T"] - 0.6 - CH_T0)

def e_at(t, sc):
    for (s, dur, a, b, e) in events(sc):
        if dur and s <= t <= s + dur: return e * pulse((t - s) / dur) * 1.0
    return 0.0

def state_do(t, sc):
    """(dau N, muc loa, so hang bang) dong bo tu events()."""
    ev = events(sc); tip, lvl, n = TIP_OUT, 0, 0
    for j, (s, dur, a, b, e) in enumerate(ev):
        if t < s: break
        if dur is None:                       # giu yen: hang bang hien sau 1,2 s im
            tip = a; lvl = 0; n = 2 if t >= s + 1.2 else 1
            continue
        u = clamp((t - s) / dur); tip = lerp(a, b, ease(u))
        lvl = (1 if abs(e) < 0.1 else 3) if u < 1 else 0
        n = {0: 1, 2: 3, 3: 4}[j] if u >= 1 else n
    return tip, lvl, n

def s_do(img, d, t, sc):
    tip, lvl, n = state_do(t, sc)
    rig(d, tip, lvl)
    text(d, (1030, 300), "chạy chậm", 40, NOTE, bold=False, anchor="rm")
    ey = chart_frame(d)
    if t > CH_T0:
        k = xs(sc); pts = []; tt = CH_T0
        while tt <= t:
            pts.append((EX0 + (tt - CH_T0) * k, ey - e_at(tt, sc) * PXV)); tt += 1 / 60
        if len(pts) > 1: d.line(pts, fill=ORANGE, width=6, joint="curve")
        x = pts[-1][0]; d.line([(x, ey - 140), (x, ey + 140)], fill=A(GRAY, 0.6), width=3)
        s1, dur1 = events(sc)[0][:2]
        if t > s1 + dur1:                                             # nhan xung nho (vao cham) sau khi ve xong
            text(d, (EX0 + (s1 + dur1 / 2 - CH_T0) * k, ey + 48), "−0,025 V", 40, BLUE)
    table(d, n)

def full_chart(d, alpha):
    if alpha <= 0: return
    sc = [x for x in CLIP["scenes"] if x["key"] == "do"][0]
    if "T" not in sc:                                    # CLIP chua build (vd. ban sao cua script kiem) -> build mot ban sao
        import copy; c = copy.deepcopy(CLIP); build(c); sc = [x for x in c["scenes"] if x["key"] == "do"][0]
    ey = chart_frame(d, alpha); k = xs(sc); pts = []; tt = CH_T0
    while tt <= sc["T"] - 0.6:
        pts.append((EX0 + (tt - CH_T0) * k, ey - e_at(tt, sc) * PXV)); tt += 1 / 60
    d.line(pts, fill=A(ORANGE, alpha), width=6, joint="curve")
    table(d, 4, alpha=alpha)

# ---------------- canh 3: Dap an + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    rig(d, TIP_IN, 0, lab=False)
    full_chart(d, 0.35 if appear(t, M[1] + 0.3, 0.5) <= 0.9 else 0.0)                                               # do thi + bang mo o duoi cho toi khi the Rut ra phu len
    kb = appear(t, M[0] + 0.8, 0.4)
    if kb > 0:
        s = "ĐÁP ÁN · loa im"; pw = tw(d, s, F(44)) + 60
        card(d, (W / 2 - pw / 2, 800, W / 2 + pw / 2, 872), fill=A(NAVY, kb), r=36)
        text(d, (W / 2, 836), s, 44, WHITE, alpha=kb)
    k = appear(t, M[0] + 1.4, 0.5)
    if k <= 0: return
    k3 = appear(t, M[1] + 0.3, 0.5)
    card(d, (40, 910, 1040, 1250 + 350 * k3), fill=A(WHITE, k), outline=A(GREEN, k), w=5)   # the co theo noi dung
    text(d, (W / 2, 985), "Từ thông đổi → có dòng", 46, GREEN, alpha=k)
    text(d, (W / 2, 1085), "e = −N·ΔΦ/Δt", 56, NAVY, alpha=appear(t, M[0] + 2.0, 0.4))
    text(d, (W / 2, 1185), "Giữ yên: ΔΦ = 0 nên e = 0", 46, INK, alpha=appear(t, M[0] + 2.6, 0.4))
    if k3 > 0.9:
        d.line([(100, 1250), (980, 1250)], fill=A(LIGHT, k3), width=3)
        # day thep rung tren cuon day (pickup) - KHONG noi "tu hoa"/"nam cham nho" (de Cau 1 sau hop cho HS tu suy)
        yy = 1340 + 14 * math.sin(2 * math.pi * 3 * t) * k3
        d.line([(110, yy), (500, yy)], fill=A(GRAY, k3), width=6)
        for j in range(5): d.arc([248, 1400 + 26 * j, 362, 1424 + 26 * j], 0, 180, fill=A(COP, k3), width=6)
        text(d, (540, 1360), "Ghi ta điện:", 44, ORANGE, anchor="lm", alpha=k3)
        text(d, (540, 1430), "dây thép rung", 44, ORANGE, anchor="lm", alpha=k3)
        text(d, (540, 1500), "trên cuộn dây", 44, ORANGE, anchor="lm", alpha=k3)

# ---------------- canh 4: Bay + Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.4)
    mk = M[0] + 2.4; ks = clamp((t - mk) / 0.4); kc = appear(t, mk + 0.25, 0.45)
    y = 300; h = 270 + 400 * kc
    card(d, (40, y, 1040, y + h), fill=A(WHITE, k0), outline=A(RED, k0), w=6)
    pw = tw(d, "BẪY", F(42)) + 52
    card(d, (W / 2 - pw / 2, y + 28, W / 2 + pw / 2, y + 94), fill=A(RED, k0), r=32)
    text(d, (W / 2, y + 61), "BẪY", 42, WHITE, alpha=k0)
    q = "“Đưa vào và rút ra: dòng cùng chiều”"; yy = y + 180; lw = tw(d, q, F(46))
    text(d, (W / 2, yy), q, 46, mix(INK, GRAY, ks), alpha=k0)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85), width=5)
    if ks > 0.99: text(d, (W / 2, yy + 66), "✗ sai", 46, RED)
    if kc > 0.9:
        ey = 700
        d.line([(110, ey), (980, ey)], fill=A(NAVY, kc), width=3)
        for x0, sg, lab in ((260, -1, "vào: −0,2 V"), (680, 1, "ra: +0,2 V")):
            pts = [(x0 + u * 70, ey - sg * 150 * pulse(u)) for u in [i / 40 for i in range(41)]]
            d.line(pts, fill=ORANGE, width=6, joint="curve")
            text(d, (x0 + 35 + 60, ey - sg * 110), lab, 44, ORANGE if sg > 0 else BLUE, anchor="lm")
        text(d, (W / 2, 900), "e đổi dấu: dòng ngược chiều", 46, NAVY, alpha=appear(t, mk + 0.6, 0.4))
    k1 = appear(t, M[1], 0.45)
    if k1 > 0:
        yb = 1060
        card(d, (40, yb, 1040, yb + 330), fill=A(WHITE, k1), outline=A(NOTE, k1), w=5)
        pw = tw(d, "CHƯA NÓI ĐƯỢC", F(42)) + 52
        card(d, (W / 2 - pw / 2, yb + 28, W / 2 + pw / 2, yb + 94), fill=A(NOTE, k1), r=32)
        text(d, (W / 2, yb + 61), "CHƯA NÓI ĐƯỢC", 42, WHITE, alpha=k1)
        text(d, (W / 2, yb + 170), "Loa không cho biết chiều dòng", 44, INK, alpha=k1)
        text(d, (W / 2, yb + 250), "lẫn số vôn", 44, INK, alpha=k1)

# ---------------- canh 5: Chot ----------------
def _end_body(d, t, k):
    cy = 1110
    coil_back(d, 380, 600, cy, 70, 7); magnet(d, 640, cy, 0.7); coil_front(d, 380, 600, cy, 70, 7)

def s_end(img, d, t, sc):
    M = sc["M"]
    chot2(d, t, sc, "Từ thông đổi mới có dòng cảm ứng",
          "Cuộn 1000 vòng, đưa cùng nam châm vào trong 0,2 s. Độ lớn e?", "ΔΦ mỗi vòng vẫn 20 µWb", _end_body, 4.0)

def chot2(d, t, sc, chot, hoi, goi_y, body, at_goi):
    """Nhu chot_hoi cua engine nhung the THU NGHI co theo noi dung: day o 1290 truoc goi y, gian toi 1600 khi goi y hien."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 410, chot, 52, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    kh = appear(t, M[0] + at_goi, 0.5)
    card(d, (40, 620, 1040, 1290 + 310 * kh), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 682), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ctext(d, 820, hoi, 46, INK, maxw=880, alpha=appear(t, M[0] + 0.4, 0.5))
    body(d, t, k1)
    if kh > 0:
        card(d, (110, 1320, 970, 1540), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1368, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1460, goi_y, 44, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][0] + 1.6, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + s, "tap") for s, dur, *_ in events(do) if dur]
            + [(da["t0"] + da["M"][0] + 1.6, "ding"), (b["t0"] + b["M"][0], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l12-udcamung-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Ứng dụng cảm ứng điện từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Cuộn dây nối loa", draw=s_hook, tail=0.3, caps=[
   ("Nam châm đặt ngoài cuộn.", 3.0),
   ("Nghĩ trước khi xem tiếp.", 6.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Đưa vào chậm, rồi giữ yên.", 6.4),
   ("Rút ra nhanh, đưa vào nhanh.", 3.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Lúc giữ yên.", 4.6),
   ("Ứng dụng thực tế.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.7, caps=[
   ("Đúng hay sai?", 4.8),
   ("Giới hạn của loa.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Tự trả lời.", 7.6)]),
])
