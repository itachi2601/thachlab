# Clip: tn-l10-dong-nang-the-nang-01 - Khuc go truot sau cong quang (ban 2 theo cong moi, 27/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-dong-nang-the-nang-01.json:
#   so_lieu_mau: v = 1,00 / 1,50 / 2,00 / 2,50 m/s -> s = 0,21 / 0,44 / 0,82 / 1,22 m ; mu = 0,25, g = 10 -> s = v2/5.
# Du doan (K10; DOI CA vi quiz mo bai + bay trong bai da hoi "v gap doi -> quang gap 4"): lan 1 qua cong 1,00 m/s;
#   qua cong 2,50 m/s thi quang truot gap may lan? Dap an: khoang 6 lan (1,22 : 0,21 = 5,8; 2,5^2 = 6,25).
# Bay: hien_tuong_hay_sai[0] "v gap doi thi s gap doi": do thi s-v, duong thang qua goc (net dut do) lech 4 diem do,
#   diem do nam tren duong cong. Chua noi duoc: mot mat ban.
# Cau chot (ca khong co trong bai/kho): qua cong 1,25 m/s (bang nua 2,50) -> s = 1,22/4 ~ 0,31 m (mo hinh v2/5 = 0,3125).
#   Khong ve go truot toi cho dung o canh chot (tranh lo so tren thuoc).
from engine import *

WOOD = (176, 124, 74); WOOD_D = (128, 86, 46); STEEL = (90, 98, 120); DRED = (185, 28, 28)
EMPTY = (148, 140, 128); DORANGE = (176, 64, 8)
ROWS = [(1.00, 0.21), (1.50, 0.44), (2.00, 0.82), (2.50, 1.22)]   # so_lieu_mau
SLOW = 1.5
XG, Y0, PXM = 200, 600, 560
APPROACH_PX = 110
HOLD = 0.40
_TI = {}
def TI(size):
    size = int(size)
    if size not in _TI: _TI[size] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", size)
    return _TI[size]
def vn(x, n=2): return f"{x:.{n}f}".replace(".", ",")

def eq(d, cx, cy, s, size, color=INK, alpha=1.0):
    """Chuoi co 'μ' (Times Bold Italic), con lai SF Bold; can giua."""
    parts = [p for p in re.split(r"(μ)", s) if p]
    fs = [(p, TI(size * 1.08) if p == "μ" else F(size)) for p in parts]
    x = cx - sum(tw(d, p, f) for p, f in fs) / 2
    for p, f in fs:
        dtext(d, (x, cy), p, f, color, alpha, "lm"); x += tw(d, p, f)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0, n=5):
    p = clamp((t - t0) / (t1 - t0)); on = n - int(p * n + 1e-9); w = 780 / n
    for i in range(n):
        x = 150 + i * w
        if i < on: card(d, (x, y, x + w - 20, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + w - 20, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

def runs():
    out = []; t = 0.0
    for i, (v, s) in enumerate(ROWS):
        ta = APPROACH_PX / (v * PXM) * SLOW; ts = 2 * s / v * SLOW
        out.append(dict(i=i, v=v, s=s, a0=t, g=t + ta, e=t + ta + ts, h=t + ta + ts + HOLD)); t += ta + ts + HOLD
    return out
RUNS = runs(); RUN_END = RUNS[-1]["h"]

def state(tr, only=None):
    rs = RUNS if only is None else [dict(RUNS[only], a0=0.0, g=RUNS[only]["g"] - RUNS[only]["a0"],
                                          e=RUNS[only]["e"] - RUNS[only]["a0"], h=RUNS[only]["h"] - RUNS[only]["a0"])]
    if tr < 0: return rs[0]["i"], -APPROACH_PX / PXM, False, False
    for r in rs:
        if tr < r["h"] or r is rs[-1]:
            if tr < r["g"]:
                k = (tr - r["a0"]) / (r["g"] - r["a0"]); return r["i"], -APPROACH_PX / PXM * (1 - k), False, False
            if tr < r["e"]:
                k = (tr - r["g"]) / (r["e"] - r["g"]); return r["i"], r["s"] * (1 - (1 - k) ** 2), True, False
            return r["i"], r["s"], True, True

def rig(d, xm, vtxt=None, done_s=None, a=1.0):
    """Ban + thuoc 0..1,4 m + khuc go (tam chan sang o giua) + cong quang + dong ho so. xm: m tu cong."""
    c = lambda col: A(col, a)
    d.rectangle([40, Y0, 1040, Y0 + 34], fill=c(WOOD), outline=c(WOOD_D), width=3)
    ry = Y0 + 34
    d.rectangle([XG, ry, XG + 1.4 * PXM, ry + 46], fill=c((253, 246, 200)), outline=c((170, 150, 60)), width=2)
    for k in range(29):
        x = XG + k * 0.05 * PXM; L = 30 if k % 4 == 0 else (18 if k % 2 == 0 else 10)
        d.line([(x, ry), (x, ry + L)], fill=c(NAVY), width=3 if L == 30 else 2)
    for k in range(0, 8, 2):
        text(d, (XG + k * 0.2 * PXM, ry + 90), vn(k * 0.2, 1) if k else "0", 56, INK, alpha=a)
    text(d, (XG - 80, ry + 90), "m", 56, INK, alpha=a)
    bx = XG + xm * PXM; bw, bh = 96, 70
    d.rectangle([bx - bw / 2, Y0 - bh, bx + bw / 2, Y0], fill=c(WOOD), outline=c(WOOD_D), width=4)
    d.rectangle([bx - 6, Y0 - bh - 64, bx + 6, Y0 - bh], fill=c(NAVY))
    gy0, gy1 = Y0 - 190, Y0
    d.rectangle([XG - 46, gy0, XG - 32, gy1], fill=c(RED)); d.rectangle([XG + 32, gy0, XG + 46, gy1], fill=c(RED))
    d.rectangle([XG - 46, gy0 - 16, XG + 46, gy0], fill=c(RED))
    by = Y0 - bh - 34
    for xx in range(int(XG - 30), int(XG + 30), 14): d.line([(xx, by), (xx + 7, by)], fill=c(ORANGE), width=4)
    d.line([(XG, gy0 - 16), (XG, gy0 - 40)], fill=c(STEEL), width=4)
    bxx = (60, gy0 - 140, 560, gy0 - 40)
    card(d, bxx, fill=c(NAVY), r=18)
    txt, col = (vtxt, YELLOW) if vtxt else ("v = –,– m/s", GRAY)
    text(d, ((bxx[0] + bxx[2]) / 2, (bxx[1] + bxx[3]) / 2), txt, 58, col, alpha=a)
    if done_s is not None and xm * PXM > 40:
        ya = Y0 + 190
        d.line([(XG, ya), (bx, ya)], fill=c(GREEN), width=5)
        for xe, sg in ((XG, 1), (bx, -1)):
            d.line([(xe, ya), (xe + sg * 18, ya - 12)], fill=c(GREEN), width=5); d.line([(xe, ya), (xe + sg * 18, ya + 12)], fill=c(GREEN), width=5)
        text(d, (max(XG + 20, bx - 10), ya + 58), f"s = {vn(done_s)} m", 58, GREEN, anchor="lm" if bx < 560 else "rm", alpha=a)

# ---------------- canh 1: Du doan ----------------
RUN_H = 0.6
def s_hook(img, d, t, sc):
    M = sc["M"]
    i, xm, passed, stopped = state(t - RUN_H, only=0)
    rig(d, xm, vtxt="v = 1,00 m/s" if passed else None, done_s=0.21 if stopped else None)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 180), "Qua cổng 2,50 m/s thì", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 275), "quãng trượt gấp mấy lần?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 400, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh + dap an ----------------
RUN0 = 0.6
def table(d, nrow, hi=-1, hl=0.0, y=1075):
    card(d, (40, y, 1040, y + 560), fill=WHITE, outline=NAVY, w=4)
    xs = (200, 520, 840)
    for x, s in zip(xs, ("Lần", "v (m/s)", "s (m)")): text(d, (x, y + 58), s, 58, INK)
    d.line([(80, y + 105), (1000, y + 105)], fill=LIGHT, width=4)
    for i in range(4):
        yy = y + 165 + i * 100
        if hl > 0 and i in (0, 3): d.rounded_rectangle([70, yy - 44, 1010, yy + 44], radius=18, fill=A((220, 252, 231), hl))
        elif i == hi: d.rounded_rectangle([70, yy - 44, 1010, yy + 44], radius=18, fill=(255, 237, 213))
        text(d, (xs[0], yy), str(i + 1), 58, INK)
        if i < nrow: text(d, (xs[1], yy), vn(ROWS[i][0]), 60, BLUE); text(d, (xs[2], yy), vn(ROWS[i][1]), 60, GREEN)

def s_do(img, d, t, sc):
    M = sc["M"]
    i, xm, passed, stopped = state(t - RUN0)
    rig(d, xm, vtxt=f"v = {vn(ROWS[i][0])} m/s" if passed else None, done_s=ROWS[i][1] if stopped else None)
    ka = appear(t, M[2] + 0.1, 0.4); kb = appear(t, M[2] + 2.6, 0.4)
    table(d, i + (1 if stopped else 0), hi=i if stopped else -1, hl=ka)
    if ka > 0:
        y = 935
        card(d, (60, y - 20, 1020, y + 130), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), r=28, w=5)
        if kb <= 0: text(d, (W / 2, y + 55), "Đáp án: khoảng 6 lần", 62, GREEN, alpha=ka)
        else:
            text(d, (W / 2, y + 55), "1,22 : 0,21 ≈ 5,8", 62, GREEN, alpha=kb)

# ---------------- canh 3: vi sao ----------------
def s_rut(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 230, 1040, 820), fill=WHITE, outline=LIGHT, w=3)
    d.rectangle([60, 600, 1020, 634], fill=WOOD, outline=WOOD_D, width=3)
    T0 = 2.4; ph = (t % T0) / T0; v0 = 1.0
    u = clamp(ph / 0.8)                                   # truot cham dan deu trong 80 % chu ki, roi dung
    xpos = 140 + 560 * (1 - (1 - u) ** 2); v = v0 * (1 - u)
    bx = xpos
    d.rectangle([bx - 60, 510, bx + 60, 600], fill=WOOD, outline=WOOD_D, width=4)
    if v > 0.05:
        arrow(d, (bx + 70, 460), (bx + 70 + 230 * v, 460), BLUE, w=8, head=24)
        text(d, (bx + 95 + 230 * v, 455), "v", 60, BLUE, anchor="lm")
        arrow(d, (bx - 10, 590), (bx - 170, 590), RED, w=8, head=24)
        text(d, (bx - 90, 680), "ma sát", 56, RED)
    # cot dong nang
    d.rectangle([870, 270, 950, 520], outline=LIGHT, width=4)
    d.rectangle([870, 520 - 250 * v * v, 950, 520], fill=ORANGE)
    text(d, (850, 300), "động năng", 56, ORANGE, anchor="rm")
    k1 = appear(t, 2.0, 0.45)
    if k1 > 0:
        card(d, (60, 860, 1020, 990), fill=A(WHITE, k1), outline=A(NAVY, k1), r=26, w=4)
        eq(d, W / 2, 925, "μmg·s = ½mv²", 64, INK, alpha=k1)
    k2 = appear(t, M[1] + 0.6, 0.45)
    if k2 > 0:
        card(d, (60, 1030, 1020, 1160), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=26, w=5)
        text(d, (W / 2, 1095), "s tỉ lệ với v²", 64, GREEN, alpha=k2)
    k3 = appear(t, M[1] + 3.1, 0.45)
    if k3 > 0:
        card(d, (60, 1200, 1020, 1330), fill=A((255, 247, 237), k3), outline=A(ORANGE, k3), r=26, w=4)
        text(d, (W / 2, 1265), "2,5² = 6,25 ≈ 6", 64, DORANGE, alpha=k3)

# ---------------- canh 4: Bay + chua noi duoc ----------------
GX0, GY0, GX1, GY1 = 230, 1120, 960, 580          # do thi s theo v: v 0..2,5 ; s 0..1,4
def gx(v): return GX0 + v / 2.5 * (GX1 - GX0)
def gy(s): return GY0 - s / 1.4 * (GY0 - GY1)

def s_bay(img, d, t, sc):
    M = sc["M"]; mk = M[1]
    # do thi
    d.line([(GX0, GY0), (GX1 + 20, GY0)], fill=INK, width=4); d.line([(GX0, GY0), (GX0, GY1 - 20)], fill=INK, width=4)
    for v in (1.0, 2.0):
        d.line([(gx(v), GY0), (gx(v), GY0 + 12)], fill=INK, width=3); text(d, (gx(v), GY0 + 50), vn(v, 1), 56, INK)
    for s in (0.4, 0.8, 1.2):
        d.line([(GX0 - 12, gy(s)), (GX0, gy(s))], fill=INK, width=3); text(d, (GX0 - 20, gy(s)), vn(s, 1), 56, INK, anchor="rm")
    text(d, (1030, GY0 + 50), "v", 60, INK, anchor="rm"); text(d, (GX0 - 20, GY1 - 10), "s", 60, INK, anchor="rm")
    kp = appear(t, 0.2, 0.4)
    # duong "s ti le v" (bay): qua goc va diem lan 1, net dut do; ve dan theo thoi gian
    gr = clamp((t - 0.4) / 2.0)
    pts = [(gx(v), gy(0.21 * v)) for v in np.linspace(0, 2.5 * gr, 26)]
    for j in range(0, len(pts) - 1, 2): d.line([pts[j], pts[j + 1]], fill=RED, width=7)
    kc = appear(t, mk + 0.2, 0.6)
    if kc > 0:
        cur = [(gx(v), gy(v * v / 5)) for v in np.linspace(0, 2.5 * kc, 60)]
        d.line(cur, fill=GREEN, width=7, joint="curve")
    for v, s in ROWS: dot(d, gx(v), gy(s), 18, A(BLUE, kp))
    # the bay o tren
    k3 = appear(t, M[2] - 0.1, 0.45)
    ks = clamp((t - mk) / 0.4)
    card(d, (40, 230, 1040, 470), fill=WHITE, outline=RED, w=6)
    pill(d, W / 2, 300, "BẪY", RED)
    q = "“v gấp đôi thì s gấp đôi”"; lw = tw(d, q, F(60)); yy = 405
    text(d, (W / 2, yy), q, 60, mix(RED, GRAY, ks))
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85), width=6)
    if k3 > 0:
        y = 1250 + (1 - k3) * 30
        card(d, (40, y, 1040, y + 330), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, y + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, y + 210), "Mới thử một mặt bàn", 62, INK, alpha=k3)

# ---------------- canh 5: Thu nghi (cau chot o khung: ~0,31 m) ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1620), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 310, "THỬ NGHĨ", ORANGE, k)
    # khuc go dang lao toi cong (khong ve cho dung)
    y0 = 720; gxx = 640
    d.rectangle([90, y0, 990, y0 + 30], fill=A(WOOD, k), outline=A(WOOD_D, k), width=3)
    xb = 200 + 220 * ((t * 0.6) % 1.0)
    d.rectangle([xb - 48, y0 - 70, xb + 48, y0], fill=A(WOOD, k), outline=A(WOOD_D, k), width=4)
    d.rectangle([gxx - 46, y0 - 190, gxx - 32, y0], fill=A(RED, k)); d.rectangle([gxx + 32, y0 - 190, gxx + 46, y0], fill=A(RED, k))
    d.rectangle([gxx - 46, y0 - 206, gxx + 46, y0 - 190], fill=A(RED, k))
    text(d, (W / 2, 900), "Qua cổng 1,25 m/s", 64, INK, alpha=k)
    text(d, (W / 2, 990), "(bằng nửa 2,50 m/s).", 62, INK, alpha=k)
    text(d, (W / 2, 1140), "Gỗ trượt khoảng bao xa?", 64, DORANGE, alpha=k)
    seg_bar(d, 1330, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = (sc[k] for k in ("hook", "do", "rut", "bay", "end"))
    out = [(h["t0"] + RUN_H + RUNS[0]["g"], "tap"), (h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.05, "ding")]
    out += [(do["t0"] + RUN0 + R["g"], "tap") for R in RUNS]
    out += [(do["t0"] + do["M"][2] + 0.1, "ding"), (b["t0"] + b["M"][1], "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"),
            (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l10-dong-nang-the-nang-01", header="VẬT LÍ 10 · THÍ NGHIỆM",
            footer="Động năng, thế năng · thachlab.id.vn", cues=_cues, scenes=[
 dict(key="hook", title="Khúc gỗ qua cổng quang", draw=s_hook, tail=0.3, caps=[
   ("Lần 1: qua cổng 1,00 m/s.", 3.4),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Bốn tốc độ", draw=s_do, tail=0.4, caps=[
   ("Đẩy gỗ, buông trước cổng.", 3.0),
   ("Đo s từ cổng tới chỗ dừng.", 4.0),
   ("So lần 1 với lần 4.", 3.6)]),
 dict(key="rut", title="Vì sao như vậy?", draw=s_rut, tail=0.6, caps=[
   ("Ma sát lấy dần động năng.", 3.6),
   ("Hết động năng thì gỗ dừng.", 4.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Đúng không?", 2.8),
   ("Sai: điểm đo nằm trên đường cong.", 3.8),
   ("Giới hạn của lần đo.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng lại, tự tính.", 6.6)]),
])
