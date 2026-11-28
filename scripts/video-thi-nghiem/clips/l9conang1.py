# Clip: tn-l9-conang-01 - Khoi truot tren mang dem khi nghieng: the nang luc tha va dong nang o chan doc (5/11/2026)
# Dung lai theo cong moi 27/11/2026 (Viec 4 L9 nhom C): chu >= 56 (ra >= 48 px), canh <= 180 tu/phut, khoi chu cach >= 2,5 s,
#   Du doan khong nut A/B/C (K10), thanh dem day >= 5 s; Bay hai thanh canh nhau, o ✓ >= 3 s; chot ca MOI.
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-conang-01.json:
#   tham_so: m = 0,20 kg ; f = 0,04 (phan co nang mat do luc can) ; h 0,05..0,50 m
#   so_lieu_mau (h m, v m/s, 10mh J, 1/2mv^2 J): 0,10 1,39 0,2 0,193 ; 0,20 1,96 0,4 0,384 ; 0,30 2,40 0,6 0,576 ; 0,40 2,77 0,8 0,767
#   quan_sat: hut khoang 3-4 % ; sai_so_thuong_gap: doc v toi 0,01 m/s -> 1/2mv^2 sai 0,4-0,7 %.
# Du doan: tha tu 0,20 m (10mh = 0,4 J) -> dong nang o chan doc? (gan bang 0,4 J, nho hon chut).
# Chot (ca moi, tu suy trong dai tham_so, theo mo hinh f = 0,04): chan doc do duoc 1/2mv^2 = 0,96 J -> tha tu do cao nao?
#   10mh = 0,96 / 0,96 = 1,0 J -> h = 1,0 / (10 . 0,20) = 0,50 m (bo qua hut -> 0,48 m; tru nguoc -> 0,46 m).
# Cau 3 sau hop trong bai hoi LY DO hut -> clip KHONG noi nguyen nhan (luc can/nhiet), chi ghi "chua noi duoc".
from engine import *

ROWS = [(0.10, 1.39, 0.2, 0.193), (0.20, 1.96, 0.4, 0.384), (0.30, 2.40, 0.6, 0.576), (0.40, 2.77, 0.8, 0.767)]
M_KG, F_LOSS = 0.20, 0.04
CHOT_WD = 0.96                              # J, chot: h = CHOT_WD / (1 - F_LOSS) / (10 m) = 0,50 m (khong hien tren man)
DRED = (185, 28, 28); DGREEN = (21, 110, 55)
def fm(x, n=2): return f"{x:.{n}f}".replace(".", ",")
def fj(x): return (f"{x:.3f}".rstrip("0").rstrip(",.") if x * 1000 % 100 else f"{x:.1f}").replace(".", ",")

# ---------------- mang dem khi + cong quang ----------------
FX, FY = 900, 900                  # chan doc
SY, SX = 1000, 1511                # px moi m do cao (doc), px ngang moi m do cao
HMAX = 0.45
EX, GATE_X, STOP_X = 1030, 925, 975
UX, UY = SX / math.hypot(SX, SY), SY / math.hypot(SX, SY)   # huong xuong doc
NX, NY = UY, -UX                                            # phap tuyen huong len
BL, BH = 50, 24

def track_pt(h): return FX - h * SX, FY - h * SY

def dashed(d, p1, p2, color, w=4, dash=16, gap=12):
    L = math.hypot(p2[0] - p1[0], p2[1] - p1[1]); n = int(L // (dash + gap)) + 1
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

def block(d, pos, alpha=1.0):
    if pos[0] == "doc":
        bx, by = track_pt(pos[1]); ux, uy, nx, ny = UX, UY, NX, NY
    else:
        bx, by = pos[1], FY; ux, uy, nx, ny = 1, 0, 0, -1
    cx, cy = bx + nx * (BH + 10), by + ny * (BH + 10)
    pts = [(cx + sx * BL * ux + sy * BH * nx, cy + sx * BL * uy + sy * BH * ny) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    d.polygon(pts, fill=A(BLUE, alpha), outline=A(NAVY, alpha), width=4)
    return bx, by

def rig(d, pos, h_show, v_show, balpha=1.0, cards=True):
    d.line([(60, 990), (1040, 990)], fill=NAVY, width=6)
    tx, ty = track_pt(HMAX)
    d.rectangle([tx + 10, ty + 20, tx + 26, 990], fill=GRAY)
    d.rectangle([FX - 8, FY + 18, FX + 8, 990], fill=GRAY); d.rectangle([EX - 30, FY + 18, EX - 14, 990], fill=GRAY)
    d.line([(tx, ty), (FX, FY), (EX, FY)], fill=(90, 98, 122), width=20, joint="curve")
    for k in range(1, 14):
        h = HMAX * k / 14; x, y = track_pt(h); dot(d, x + NX * 4, y + NY * 4, 3, WHITE)
    for x in range(FX + 20, EX - 20, 32): dot(d, x, FY - 4, 3, WHITE)
    d.rectangle([EX - 4, FY - 70, EX + 10, FY + 10], fill=NAVY)
    rx = 130                                                                # thuoc do do cao (vach, khong so)
    d.rectangle([rx - 14, FY - HMAX * SY - 10, rx + 14, FY], fill=(255, 244, 214), outline=NAVY, width=3)
    for k in range(0, 10):
        y = FY - k * 0.05 * SY; L = 22 if k % 2 == 0 else 12
        d.line([(rx + 14 - L, y), (rx + 14, y)], fill=NAVY, width=3)
    dashed(d, (rx + 14, FY), (FX, FY), GRAY, w=3)
    d.line([(GATE_X, FY - 116), (GATE_X, 470)], fill=GRAY, width=6)       # cong quang
    d.rectangle([GATE_X - 12, FY - 130, GATE_X + 12, FY - 34], fill=NAVY)
    d.rectangle([GATE_X - 12, FY + 12, GATE_X + 12, FY + 40], fill=NAVY)
    d.line([(GATE_X, FY - 34), (GATE_X, FY + 12)], fill=A(RED, 0.8), width=4)
    bx, by = block(d, pos, balpha)
    if pos[0] == "doc" and pos[1] > 0.005:
        dashed(d, (rx + 14, by), (bx, by), A(ORANGE, balpha), w=4)
        dot(d, rx, by, 10, A(ORANGE, balpha))
    if not cards: return
    card(d, (40, 255, 520, 440), fill=WHITE, outline=LIGHT, r=26, w=4)
    text(d, (280, 305), f"m = {fm(M_KG)} kg", 56, INK)
    text(d, (280, 390), "h = " + (fm(h_show) + " m" if h_show is not None else "?"), 56, ORANGE)
    card(d, (560, 255, 1040, 440), fill=(240, 246, 255), outline=BLUE, r=26, w=4)
    text(d, (800, 305), "v ở chân dốc", 56, NAVY)
    text(d, (800, 390), (v_show + " m/s") if v_show else "v = ?", 56, BLUE)

def slide(tau, h0, Ts):
    if tau <= 0: return ("doc", h0)
    if tau < Ts: return ("doc", h0 * (1 - (tau / Ts) ** 2))
    k = clamp((tau - Ts) / 0.3); return ("ngang", lerp(FX, STOP_X, 1 - (1 - k) ** 2))
def passed(tau, Ts): p = slide(tau, 1, Ts); return p[0] == "ngang" and p[1] >= GATE_X

def pill(d, s, y, a, color, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    rig(d, ("doc", 0.20), 0.20, None)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    text(d, (W / 2, y0 + 165), "Lúc thả: thế năng 0,4 J.", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 250), "Chân dốc: động năng?", 58, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 340, 970, y0 + 440], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 340, 110 + max(90, 860 * (1 - p)), y0 + 440], radius=45, fill=A((76, 29, 149), a))

# ---------------- canh 2: tien hanh ----------------
REL = [0.5, 2.5, 4.5, 6.5]
TS = [1.3 * math.sqrt(r[0] / 0.4) for r in ROWS]
def do_state(t):
    i = max([j for j in range(4) if t >= REL[j] - 0.35], default=0)
    tau = t - REL[i]; pos = slide(tau, ROWS[i][0], TS[i])
    if passed(tau, TS[i]): v = fm(ROWS[i][1])
    elif tau >= 0 or i == 0: v = None
    else: v = fm(ROWS[i - 1][1])
    ba = clamp((t - (REL[i] - 0.35)) / 0.25) if i > 0 or t < REL[0] else 1.0
    return i, pos, v, ba
def row_at(i): return REL[i] + TS[i] + 0.06

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    i, pos, v, ba = do_state(t)
    rig(d, pos, ROWS[i][0], v, balpha=ba)
    nshow = sum(1 for j in range(4) if t >= row_at(j))
    card(d, (140, 1030, 940, 1580), fill=WHITE, outline=NAVY, w=4)
    xs = (360, 720)
    text(d, (xs[0], 1100), "h (m)", 56, ORANGE); text(d, (xs[1], 1100), "v (m/s)", 56, BLUE)
    d.line([(180, 1145), (900, 1145)], fill=LIGHT, width=4)
    for j, r in enumerate(ROWS):
        a = appear(t, row_at(j), 0.35); y = 1192 + j * 78
        if a <= 0: continue
        if j == nshow - 1: d.rounded_rectangle([170, y - 36, 910, y + 36], radius=16, fill=A((225, 236, 255), a))
        text(d, (xs[0], y), fm(r[0]), 56, ORANGE, alpha=a); text(d, (xs[1], y), fm(r[1]), 56, BLUE, alpha=a)
    text(d, (W / 2, 1530), "(số liệu minh hoạ)", 56, NAVY)

# ---------------- canh 3: dap an - cot ngang ghep doi ----------------
BX0, BSC = 290, 720
GY0, GDY = 470, 168
def s_cmp(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    d.rectangle([110, 290, 160, 340], fill=ORANGE); text(d, (180, 315), "thế năng", 56, INK, anchor="lm")
    d.rectangle([560, 290, 610, 340], fill=BLUE); text(d, (630, 315), "động năng", 56, INK, anchor="lm")
    text(d, (1020, 315), "(J)", 56, NAVY, anchor="rm")
    hl = appear(t, M[1] - 0.1, 0.4)
    if hl > 0:
        y = GY0 + GDY
        d.rounded_rectangle([60, y - 34, 1040, y + 126], radius=20, fill=A((220, 252, 231), hl), outline=A(GREEN, hl), width=4)
    d.line([(BX0, GY0 - 40), (BX0, GY0 + 3 * GDY + 110)], fill=NAVY, width=5)
    for j, (h, v, wt, wd) in enumerate(ROWS):
        y = GY0 + j * GDY
        text(d, (BX0 - 22, y + 32), fm(h) + " m", 56, NAVY, anchor="rm")
        for k, (val, col, at) in enumerate(((wt, ORANGE, 0.2 + 0.25 * j), (wd, BLUE, 1.4 + 0.25 * j))):
            g = ease((t - at) / 0.5)
            if g <= 0: continue
            yy = y + k * 62; x1 = BX0 + val * BSC * g
            if x1 - BX0 > 2: d.rectangle([BX0, yy - 4, x1, yy + 44], fill=col)
            text(d, (x1 + 16, yy + 20), fj(val), 56, col, anchor="lm", alpha=clamp(g * 2 - 1))
    if hl > 0:
        pill(d, "ĐÁP ÁN: gần 0,4 J", 1240, hl, GREEN, 58)
    h2 = appear(t, M[1] + 2.5, 0.4)
    text(d, (W / 2, 1370), "hụt 3–4 % mỗi lần", 58, DRED, alpha=h2)

# ---------------- canh 4: rut ra, thanh nang luong ----------------
RH, RT0, RTS = 0.30, 0.6, 3.2
ESC, EX0 = 1300, 110
def s_rut(img, d, t, sc):
    IMG_REF[0] = img
    tau = t - RT0; pos = slide(tau, RH, RTS)
    hb = pos[1] if pos[0] == "doc" else 0.0
    rig(d, pos, RH, None, cards=False)
    fr = (RH - hb) / RH
    wt = 10 * M_KG * RH * (1 - fr); wd = ROWS[2][3] * fr
    card(d, (40, 1040, 1040, 1500), fill=WHITE, outline=LIGHT, w=4)
    yb0, yb1 = 1180, 1270
    xw = EX0 + wd * ESC
    if wd * ESC > 2: d.rectangle([EX0, yb0, xw, yb1], fill=BLUE)
    if wt * ESC > 2: d.rectangle([xw, yb0, xw + wt * ESC, yb1], fill=ORANGE)
    xm = EX0 + 0.6 * ESC
    dashed(d, (xm, yb0 - 30), (xm, yb1 + 20), NAVY, w=4, dash=10, gap=8)
    text(d, (xm - 10, yb0 - 70), "0,6 J lúc thả", 56, NAVY, anchor="rm")
    d.rectangle([110, 1360, 160, 1410], fill=ORANGE); text(d, (180, 1385), "thế năng", 56, INK, anchor="lm")
    d.rectangle([560, 1360, 610, 1410], fill=BLUE); text(d, (630, 1385), "động năng", 56, INK, anchor="lm")

# ---------------- canh 5: bay + chua noi duoc ----------------
SPC = 180                                        # px moi %
BAY_ST = 2.2
def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    a = appear(t, 0.2, 0.4)
    k2 = appear(t, M[2] - 0.1, 0.45)
    # hai thanh canh nhau (giu suot canh): sai so doc v nho, phan hut lon
    card(d, (40, 260, 1040, 700), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    for k, (lbl, lo, hi, col, s) in enumerate((("sai số động năng do đọc v", 0.4, 0.7, PURPLE, "0,4–0,7 %"),
                                                ("phần hụt", 3.0, 4.0, DRED, "3–4 %"))):
        y = 330 + k * 190
        text(d, (90, y), lbl, 56, col, anchor="lm", alpha=a)
        g = ease((t - 0.3 - 0.9 * k) / 0.8)                                # thanh moc lan luot
        if g > 0:
            d.rectangle([90, y + 45, 90 + lo * SPC * g, y + 115], fill=A(col, a))
            d.rectangle([90 + lo * SPC * g, y + 45, 90 + hi * SPC * g, y + 115], fill=A(mix(col, WHITE, 0.55), a))
        text(d, (90 + hi * SPC + 24, y + 80), s, 56, col, anchor="lm", alpha=a)
    a1 = a * (1 - k2); y0 = 760
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y0 + 62, a1, DRED)
        q = "“Hụt do đọc sai”"; yy = y0 + 190; lw = tw(d, q, F(60))
        text(d, (W / 2, yy), q, 60, INK, alpha=a1)
        ks = clamp((t - BAY_ST) / 0.4)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=7)
        kk = a1 * appear(t, M[1] + 0.1, 0.4)
        card(d, (70, y0 + 320, 1010, y0 + 480), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 400), "✓ Hụt lớn hơn nhiều", 60, DGREEN, alpha=kk)
    if k2 > 0:
        card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 110), "Chưa nói được:", 60, NAVY, alpha=k2)
        text(d, (W / 2, y0 + 220), "hụt thành dạng gì", 60, INK, alpha=k2)
        text(d, (W / 2, y0 + 320), "(chưa đo)", 56, NAVY, alpha=k2)

# ---------------- canh 6: chot ----------------
END_Q = 0.2
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 280, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 350, k1, ORANGE)
    text(d, (W / 2, 470), "Cùng máng, cùng khối.", 58, INK, alpha=k1)
    text(d, (W / 2, 555), f"Chân dốc: động năng {fm(CHOT_WD)} J.", 58, INK, alpha=k1)
    text(d, (W / 2, 640), "Thả từ độ cao nào?", 58, INK, alpha=k1)
    if k1 <= 0: return
    # hinh nho: mang + khoi o do cao "?" (khong ghi so dap an, khong ve thuoc co vach so)
    x0, yb, x1, yt = 220, 1320, 860, 900
    d.line([(120, yb + 30), (980, yb + 30)], fill=A(NAVY, k1), width=5)
    d.line([(x0, yt), (x1, yb), (960, yb)], fill=A((90, 98, 122), k1), width=16, joint="curve")
    L = math.hypot(x1 - x0, yb - yt); u = ((x1 - x0) / L, (yb - yt) / L); n = (u[1], -u[0])
    bx, by = x0 + 0.1 * (x1 - x0), yt + 0.1 * (yb - yt); cx, cy = bx + n[0] * 32, by + n[1] * 32
    pts = [(cx + a * 46 * u[0] + b * 24 * n[0], cy + a * 46 * u[1] + b * 24 * n[1]) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    d.polygon(pts, fill=A(BLUE, k1), outline=A(NAVY, k1), width=3)
    xa = bx - 70
    dashed(d, (xa - 20, by), (bx - 30, by), A(ORANGE, k1), w=4)
    arrow(d, (xa, yb), (xa, by + 6), A(ORANGE, k1), w=6, head=20)
    rr = 66 + 34 * math.sin(2 * math.pi * t / 2.0)
    yc = (by + yb) / 2
    d.ellipse([xa - 60 - rr, yc - rr, xa - 60 + rr, yc + rr], fill=A(mix(ORANGE, WHITE, 0.45), k1))
    text(d, (xa - 60, yc), "?", 80, WHITE, alpha=k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, cm, b, e = sc["hook"], sc["do"], sc["cmp"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + row_at(i), "tap") for i in range(4)]
    out += [(cm["t0"] + cm["M"][1] - 0.1, "ding"), (b["t0"] + BAY_ST, "buzz"), (b["t0"] + b["M"][1] + 0.1, "tap"),
            (e["t0"] + END_Q + 0.1, "open")]
    return sorted(out)

CLIP = dict(id="tn-l9-conang-01", header="KHTN 9 · THÍ NGHIỆM", cues=_cues,
    footer="Cơ năng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Máng đệm khí nghiêng", draw=s_hook, tail=0.3, caps=[
   ("Máng đệm khí.", 2.5),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Thả từ bốn độ cao", draw=s_do, tail=0.2, caps=[
   ("Thả nhẹ, cổng quang đo v.", 3.0),
   ("Ghi v mỗi lần.", 2.6),
   ("Thả càng cao, v càng lớn.", 2.9)]),
 dict(key="cmp", title="So thế năng và động năng", draw=s_cmp, tail=0.8, caps=[
   ("Tính cho cả bốn lần.", 3.0),
   ("Động năng thấp hơn chút.", 3.4)]),
 dict(key="rut", title="Thế năng thành động năng", draw=s_rut, tail=0.3, caps=[
   ("Thế năng thành động năng.", 2.9),
   ("Tổng gần như không đổi.", 2.9)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 4.2),
   ("So hai thanh.", 3.4),
   ("Còn bỏ ngỏ.", 2.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Tự nghĩ.", 6.2)]),
])
