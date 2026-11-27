# Clip: tn-l10-biendang-02 - Treo qua nang vao lo xo, do do cung k (ban 2 cong moi, 27/11/2026)
# So lieu tu content/thi-nghiem/tn-l10-biendang-02.json:
#   l0 = 10,0 cm ; g = 9,8 ; so_lieu_mau (m g, F N, l cm, dl cm): 50 0,49 11,9 1,9 ; 100 0,98 13,9 3,9 ; 150 1,47 15,9 5,9 ;
#   200 1,96 17,9 7,9 ; 250 2,45 19,8 9,8. Lo xo ve dung ti le: 52 px moi cm, vach 0 thuoc ngang moc tren.
# KHONG hien cot F/dl va so k (bai giao HS tu tinh F/dl tung hang + "Bam xem nhan xet" co k ~ 25,1).
# Du doan (K10, khong nut A-D): them tung qua 50 g, moi lan lo xo dai them the nao?
#   A. them deu nhau moi lan (DUNG) ; B. them it dan, lo xo cung dan ; C. them nhieu dan, lo xo mem dan
#   (hien_tuong_hay_sai[2] "k tang khi treo them").
# Bay = hien_tuong_hay_sai[0] (lay F chia chieu dai l -> 4,1 ; 7,1 ; 9,2 N/m tang dan, tuong k tang): ngoac l do
#   va ngoac dl xanh tren cung lo xo 100 g.
# Chot (ca tu suy, ghi_chu kho): treo vat 120 g (trong khoang 50-250 g da do) -> F = 1,176 N, dl = 4,7 cm, l = 14,7 cm.
#   v2 (doi so tranh gan quiz bai): vat 80 g -> F = 0,784 N, dl = 3,1 cm, l = 13,1 cm (noi suy bang 11,9..13,9 cung ra 13,1).
#   So 80 g va 13,1 chua hien ; can >= 2 buoc (ti le tu bang hoac k, roi cong l0).
from engine import *

G, L0 = 9.8, 10.0
ROWS = [(50, 0.49, 11.9, 1.9), (100, 0.98, 13.9, 3.9), (150, 1.47, 15.9, 5.9), (200, 1.96, 17.9, 7.9), (250, 2.45, 19.8, 9.8)]
NOTE = (60, 64, 84); BRASS = (196, 150, 70); BRASS_D = (140, 100, 40); RULER = (255, 241, 205)
DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)

from PIL import ImageFont as _IF
_FL = {}
def FL(size):
    """l nghieng (Georgia Bold Italic) de khong lan voi I trong phong sans."""
    if size not in _FL: _FL[size] = _IF.truetype("/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf", size)
    return _FL[size]

def seq(d, x, y, parts, alpha=1.0, anchor="m"):
    """parts: (chu, size, mau, nghieng). anchor m: can giua tai x ; l: bat dau tai x ; r: ket thuc tai x."""
    fs = [FL(z) if it else F(z) for _, z, _, it in parts]
    ws = [tw(d, s_, f) + (6 if it else 0) for (s_, _, _, it), f in zip(parts, fs)]
    x -= sum(ws) / 2 if anchor == "m" else (sum(ws) if anchor == "r" else 0)
    for (s_, z, c, it), f, w in zip(parts, fs, ws):
        dtext(d, (x, y), s_, f, c, alpha, anchor="lm"); x += w

def lab_l(d, x, y, pre, post, size, col, alpha=1.0, anchor="m"):
    """Chu co mot chu l nghieng o giua: pre + l + post."""
    seq(d, x, y, [(pre, size, col, False), ("l", size + 2, col, True), (post, size, col, False)], alpha, anchor)

def vn(x, n=1): return f"{x:.{n}f}".replace(".", ",")

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- gia treo + lo xo + thuoc (ben phai) ----------------
SXX, TOP, PX = 790, 330, 52                       # truc lo xo, moc tren (= vach 0 thuoc), px moi cm
RX = 870                                         # mep trai thuoc
MW, MH = 110, 34                                 # qua 50 g
def yl(l): return TOP + l * PX

def stand(d, a=1.0):
    d.rounded_rectangle([1030, 290, 1054, 1672], radius=6, fill=A((170, 175, 190), a))
    d.rounded_rectangle([690, 290, 1054, 318], radius=8, fill=A((150, 155, 172), a))
    d.rounded_rectangle([670, 1664, 1060, 1690], radius=10, fill=A((176, 124, 74), a))

def ruler(d, a=1.0):
    d.rectangle([RX, TOP - 14, RX + 50, yl(21) + 14], fill=A(RULER, a), outline=A(BRASS_D, a), width=3)
    for k in range(211):
        y = TOP + k * PX / 10; L = 30 if k % 10 == 0 else (18 if k % 5 == 0 else 8)
        d.line([(RX, y), (RX + L, y)], fill=A(NAVY, a), width=3 if k % 10 == 0 else 1)
    for c in range(0, 21, 4): text(d, (RX + 60, yl(c)), str(c), 56, INK, anchor="lm", alpha=a)

def spring(d, yb, a=1.0, x=SXX, top=TOP, n=14, amp=26):
    lead = 22
    pts = [(x, top), (x, top + lead)]
    for i in range(1, 2 * n):
        pts.append((x + (amp if i % 2 else -amp), lerp(top + lead, yb - lead, i / (2 * n))))
    pts += [(x, yb - lead), (x, yb)]
    d.line(pts, fill=A(NAVY, a), width=5, joint="curve")
    d.ellipse([x - 9, yb - 4, x + 9, yb + 14], outline=A(NAVY, a), width=4)

def masses(d, n, yb, a=1.0, x=SXX):
    y = yb + 10
    for i in range(n):
        d.line([(x, y), (x, y + 8)], fill=A(NAVY, a), width=4)
        d.rounded_rectangle([x - MW / 2, y + 8, x + MW / 2, y + 8 + MH], radius=8, fill=A(BRASS, a), outline=A(BRASS_D, a), width=3)
        y += MH + 10
    return y

def pointer(d, l, a=1.0):
    y = yl(l)
    d.line([(SXX + 14, y), (RX + 34, y)], fill=A(RED, a), width=5)
    d.polygon([(RX + 2, y), (RX - 16, y - 9), (RX - 16, y + 9)], fill=A(RED, a))

def l0_line(d, a=1.0):
    y = yl(L0)
    for x in range(SXX - 60, RX, 22): d.line([(x, y), (x + 11, y)], fill=A(GRAY, a), width=4)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    k1 = appear(t, 0.6, 0.9)                     # mot qua 50 g treo vao, lo xo dan tu 10,0 toi 11,9 cm
    l = lerp(L0, ROWS[0][2], k1)
    stand(d); ruler(d); l0_line(d)
    spring(d, yl(l)); masses(d, 1 if t >= 0.6 else 0, yl(l)); pointer(d, l)
    text(d, (340, 360), "Chưa treo:", 58, NOTE)
    text(d, (340, 440), "10,0 cm", 64, NOTE)
    kb = appear(t, 1.6, 0.4)
    if kb > 0:
        text(d, (340, 560), "1 quả 50 g:", 58, INK, alpha=kb)
        text(d, (340, 640), "11,9 cm", 64, RED, alpha=kb)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1040 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 175), "Thêm từng quả 50 g.", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 270), "Mỗi lần dài thêm ra sao?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 400, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: tien hanh ----------------
ST0, PER, SLIDE, SETTLE = 0.5, 1.8, 0.6, 1.2
def osc(tt): return 1 - math.exp(-3.4 * tt) * math.cos(2 * math.pi * 1.4 * tt)
def masses_bottom(n, l): return yl(l) + 10 + n * (MH + 10)
def do_state(t):
    """-> (so qua dang treo, l ve (cm), so hang da ghi, qua dang truot (x, y) hoac None)."""
    n, l, rows, fly = 0, L0, 0, None
    for i in range(5):
        a = ST0 + i * PER
        if t < a: break
        lp = ROWS[i - 1][2] if i else L0; ln = ROWS[i][2]
        if t < a + SLIDE:                         # qua moi truot tu trai vao, treo duoi chum
            k = ease((t - a) / SLIDE); ybot = masses_bottom(i, lp)
            fly = (lerp(620, SXX, k), lerp(ybot + 60, ybot, k)); n, l = i, lp
        else:
            tt = t - a - SLIDE; n = i + 1; l = lp + (ln - lp) * osc(tt)
            if tt >= SETTLE: l = ln; rows = i + 1
            else: rows = i
    return n, l, rows, fly

def t_dapan(): return ST0 + 4 * PER + SLIDE + SETTLE + 0.3

def table(d, rows, a=1.0, x0=40, x1=660, y0=330):
    card(d, (x0, y0, x1, y0 + 110 + 5 * 82), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    xs = (130, 330, 535)
    text(d, (xs[0], y0 + 52), "m (g)", 55, NOTE, alpha=a)
    lab_l(d, xs[1], y0 + 52, "", " (cm)", 55, NOTE, a); lab_l(d, xs[2], y0 + 52, "Δ", " (cm)", 55, NOTE, a)
    d.line([(x0 + 16, y0 + 96), (x1 - 16, y0 + 96)], fill=A(LIGHT, a), width=4)
    for i in range(rows):
        m, f, l, dl = ROWS[i]; y = y0 + 145 + i * 82
        text(d, (xs[0], y), str(m), 58, INK, alpha=a)
        text(d, (xs[1], y), vn(l), 58, INK, alpha=a)
        text(d, (xs[2], y), vn(dl), 58, RED, alpha=a)

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    n, l, rows, fly = do_state(t)
    stand(d); ruler(d); l0_line(d)
    spring(d, yl(l)); masses(d, n, yl(l)); pointer(d, l)
    if fly:
        x, y = fly
        d.rounded_rectangle([x - MW / 2, y + 8, x + MW / 2, y + 8 + MH], radius=8, fill=BRASS, outline=BRASS_D, width=3)
    table(d, rows)
    k = appear(t, t_dapan(), 0.4)
    if k > 0:
        card(d, (40, 920, 660, 1120), fill=A(NAVY, k), r=30)
        text(d, (350, 980), "Dài thêm đều,", 60, WHITE, alpha=k)
        text(d, (350, 1060), "khoảng 2 cm mỗi quả", 56, (253, 224, 71), alpha=k)

def _kiem_dong_bo():
    """Moi 0,05 s: khi so hang = so qua va dung yen, chieu dai ve = l hang cuoi ; hang chi hien khi da on dinh ; kho khop."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; bad = []; t = 0.0
    while t < sc["T"]:
        n, l, rows, fly = do_state(t)
        if rows > n: bad.append(("hang>qua", round(t, 2)))
        if rows == n and n and abs(l - ROWS[n - 1][2]) > 1e-9: bad.append(("lech", round(t, 2)))
        if yl(l) + 10 + n * (MH + 10) > 1655: bad.append(("cham de", round(t, 2)))
        t += 0.05
    for m, f, l, dl in ROWS:
        if abs(m / 1000 * G - f) > 0.006 or abs(l - L0 - dl) > 1e-6 or abs(dl - f / 25 * 100) > 0.11: bad.append(("kho", m))
    if t_dapan() + 2.1 > sc["T"]: bad.append("dap an sat cuoi")
    return bad

# ---------------- canh 3: luc va do dan ----------------
GX0, GX1, GY0, GY1 = 200, 940, 1430, 960           # do thi: dl 0-10 cm, F 0-2,5 N
def gx(dl): return GX0 + (GX1 - GX0) * dl / 10
def gy(f): return GY0 - (GY0 - GY1) * f / 2.5

def s_rut(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    a = appear(t, 0.2)
    cx, top = 230, 360                           # chum 5 qua (vat dang xet)
    bot = masses(d, 5, top - 18, a, x=cx)
    ka = appear(t, 0.6, 0.4)
    if ka > 0:
        arrow(d, (cx, top - 10), (cx, top - 140 * ka - 10 + 40), A(GREEN, ka), w=9, head=28)
        arrow(d, (cx, bot + 4), (cx, bot + 104 * ka + 4), A(RED, ka), w=9, head=28)
        text(d, (cx + 70, top - 80), "F", 64, GREEN, anchor="lm", alpha=ka)
        text(d, (cx + 70, bot + 60), "P", 64, RED, anchor="lm", alpha=ka)
        text(d, (680, 450), "F: lực lò xo", 58, GREEN, alpha=ka)
        text(d, (680, 530), "P: trọng lực", 58, RED, alpha=ka)
        text(d, (680, 630), "F = P = m·g", 64, INK, alpha=ka)
    kg = appear(t, M[1] - 0.1, 0.4)
    if kg > 0:
        d.line([(GX0, GY0), (GX1 + 20, GY0)], fill=A(INK, kg), width=5)
        d.line([(GX0, GY0), (GX0, GY1 - 40)], fill=A(INK, kg), width=5)
        for v in (0, 5):
            d.line([(gx(v), GY0), (gx(v), GY0 + 14)], fill=A(INK, kg), width=3)
            text(d, (gx(v), GY0 + 52), str(v), 56, INK, alpha=kg)
        for v in (1, 2):
            d.line([(GX0 - 14, gy(v)), (GX0, gy(v))], fill=A(INK, kg), width=3)
            text(d, (GX0 - 28, gy(v)), str(v), 56, INK, anchor="rm", alpha=kg)
        lab_l(d, GX1 + 20, GY0 + 52, "Δ", " (cm)", 56, INK, kg, anchor="r")
        text(d, (GX0 + 26, GY1 - 40), "F (N)", 56, INK, anchor="lm", alpha=kg)
        for i, (m, f, l, dl) in enumerate(ROWS):
            kp = appear(t, M[1] + 0.3 + i * 0.4, 0.3)
            if kp > 0: dot(d, gx(dl), gy(f), 13, A(BLUE, kp))
        kl = appear(t, M[1] + 2.5, 0.6)
        if kl > 0:                                # chi noi cac diem da do (khong ngoai suy qua 9,8 cm)
            xe = lerp(gx(0), gx(9.8), kl); ye = lerp(gy(0), gy(0.25 * 9.8), kl)
            d.line([(gx(0), gy(0)), (xe, ye)], fill=A(ORANGE, 0.9), width=6)
        kt = appear(t, M[1] + 3.0, 0.4)
        if kt > 0: text(d, (gx(7.0), gy(0.33)), "đường thẳng qua gốc", 55, DORANGE, alpha=kt)

# ---------------- canh 4: bay + chua noi duoc ----------------
BPX = 40                                         # thang ve o canh bay (px moi cm)
def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    k0 = appear(t, 0.2, 0.4); k3 = appear(t, M[2] - 0.1, 0.45); a1 = k0 * (1 - k3)
    if a1 > 0:
        card(d, (40, 290, 1040, 600), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pill(d, W / 2, 355, "BẪY", RED, a1)
        lab_l(d, W / 2, 450, "F chia ", " (N/m): 4,1 → 7,1 → 9,2", 58, INK, a1)
        q = "“k tăng dần”"
        ks = clamp((t - M[1]) / 0.4); f = F(60); lw = tw(d, q, f); yy = 540
        text(d, (W / 2, yy), q, 60, mix(RED, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
        # lo xo 100 g: ngoac l (ca chieu dai, do) hien cung cau sai ; ngoac dl (xanh) o M[1]
        x, top = 540, 660
        d.rounded_rectangle([x - 90, top - 22, x + 90, top], radius=6, fill=A((150, 155, 172), a1))
        yb = top + ROWS[1][2] * BPX; y0 = top + L0 * BPX
        spring(d, yb, a1, x=x, top=top, n=12, amp=22); masses(d, 2, yb, a1, x=x)
        for xx in range(x - 70, x + 140, 22): d.line([(xx, y0), (xx + 11, y0)], fill=A(GRAY, a1), width=4)
        text(d, (x + 160, y0 - 6), "chưa treo", 55, NOTE, anchor="lm", alpha=a1)
        bx = x - 130
        d.line([(bx, top), (bx, yb)], fill=A(RED, a1), width=5)
        for y in (top, yb): d.line([(bx - 12, y), (bx + 12, y)], fill=A(RED, a1), width=5)
        lab_l(d, bx - 20, (top + yb) / 2, "", " = 13,9 cm", 56, RED, a1, anchor="r")
        ok = appear(t, M[1], 0.4) * a1
        if ok > 0:
            bx2 = x + 130
            d.line([(bx2, y0), (bx2, yb)], fill=A(GREEN, ok), width=6)
            for y in (y0, yb): d.line([(bx2 - 12, y), (bx2 + 12, y)], fill=A(GREEN, ok), width=6)
            lab_l(d, bx2 + 20, (y0 + yb) / 2, "Δ", " = 3,9 cm", 56, GREEN, ok, anchor="l")
        k2 = appear(t, M[1] + 3.0, 0.45) * a1
        if k2 > 0:
            card(d, (40, 1340, 1040, 1470), fill=A((220, 252, 231), k2), outline=A(GREEN, k2), w=5)
            seq(d, W / 2, 1405, [("F đi với Δ", 60, GREEN, False), ("l", 62, GREEN, True), (", không với ", 60, GREEN, False), ("l", 62, GREEN, True)], k2)
    if k3 > 0:
        card(d, (40, 290, 1040, 640), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 360, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 470), "Treo nặng hơn 250 g:", 60, INK, alpha=k3)
        text(d, (W / 2, 560), "còn dài thêm đều?", 60, INK, alpha=k3)
        # do thi thu nho: 5 diem da do, khoang sau 9,8 cm de trong co dau ?
        x0, x1, yA, yB = 200, 900, 1180, 760
        d.line([(x0, yA), (x1, yA)], fill=A(INK, k3), width=5); d.line([(x0, yA), (x0, yB)], fill=A(INK, k3), width=5)
        for i, (m, f, l, dl) in enumerate(ROWS):
            dot(d, x0 + 40 * dl, yA - 140 * f, 12, A(BLUE, k3))
        d.line([(x0, yA), (x0 + 40 * 9.8, yA - 140 * 2.45)], fill=A(ORANGE, 0.9 * k3), width=6)
        text(d, (x0 + 40 * 9.8 + 150, yA - 140 * 2.45 - 40), "?", 80, PURPLE, alpha=k3)
        lab_l(d, x1 - 60, yA + 52, "Δ", "", 56, INK, k3); text(d, (x0 + 50, yB - 10), "F", 56, INK, alpha=k3)

# ---------------- canh 5: thu nghi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 305, "THỬ NGHĨ", ORANGE, k)
    x, top = 300, 420
    d.rounded_rectangle([x - 80, top - 22, x + 80, top], radius=6, fill=A((150, 155, 172), k))
    spring(d, top + 230, k, x=x, top=top, n=10, amp=22)
    d.rounded_rectangle([x - 70, top + 260, x + 70, top + 340], radius=10, fill=A(BRASS, k), outline=A(BRASS_D, k), width=3)
    d.line([(x, top + 240), (x, top + 260)], fill=A(NAVY, k), width=4)
    text(d, (x, top + 300), "80 g", 56, WHITE, alpha=k)
    text(d, (690, 520), "Lò xo này,", 60, INK, alpha=k)
    text(d, (690, 600), "chưa treo 10,0 cm", 58, NOTE, alpha=k)
    text(d, (W / 2, 900), "Treo 80 g, đứng yên.", 64, INK, alpha=k)
    text(d, (W / 2, 1020), "Lò xo dài bao nhiêu cm?", 64, DORANGE, alpha=k)
    text(d, (W / 2, 1120), "Lấy g = 9,8 m/s².", 58, NOTE, alpha=k)
    seg_bar(d, 1200, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
            + [(do["t0"] + ST0 + i * PER + SLIDE, "tap") for i in range(5)]
            + [(do["t0"] + t_dapan(), "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"),
               (b["t0"] + b["M"][1], "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"), (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l10-biendang-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Biến dạng của vật rắn · thachlab.id.vn", scenes=[
 dict(key="hook", title="Lò xo cạnh thước mm", draw=s_hook, tail=0.3, caps=[
   ("Treo vào móc lò xo.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Thêm từng quả nặng", draw=s_do, tail=1.1, caps=[
   ("Mỗi quả nặng 50 g.", 3.6),
   ("Đợi đứng yên mới đọc.", 3.6),
   ("So cột độ dãn.", 3.3)]),
 dict(key="rut", title="Lực và độ dãn", draw=s_rut, tail=0.2, caps=[
   ("Đứng yên: hai lực cân bằng.", 3.8),
   ("Chấm năm hàng lên đồ thị.", 3.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Đúng không?", 3.0),
   ("Đo từ vạch 10,0 cm.", 6.1),
   ("Chưa nói được.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Dừng lại, tự tính.", 6.6)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
