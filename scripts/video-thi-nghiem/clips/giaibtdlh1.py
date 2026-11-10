# Clip: tn-l10-giaibt-dlh-01 - Hai hop but (rong / day) truot tren van nghieng (30/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-giaibt-dlh-01.json:
#   tham_so: alpha = 30 deg, mu = 0,3, L = 1 m ; so_lieu_mau: m = 0,05 / 0,1 / 0,2 / 0,4 kg -> a = 2,4 m/s2, t = 0,91 s.
#   Hop rong = 0,1 kg, hop day = 0,4 kg (hai hang cua so_lieu_mau).
# Canh: Du doan (K10: chi cau hoi + hinh, khong nut A/B/C) -> Tien hanh (hai van giong nhau, dong ho, chieu cham)
#       -> Dap an C + bang so lieu -> Rut ra (so do luc, dinh luat II, m gian uoc) -> Bay (N = mg) + chua noi duoc
#       -> Chot + cau hoi tu nho lai (bo ma sat: a = ?).
from engine import *

ALPHA = math.radians(30)
CA, SA = math.cos(ALPHA), math.sin(ALPHA)
U = (CA, SA)                       # doc theo doc, huong xuong
NRM = (SA, -CA)                    # phap tuyen huong ra khoi mat doc (len)
WOOD = (176, 124, 74); WOOD_D = (140, 96, 54)
T_SLIDE = 0.91                     # s (so_lieu_mau)
SLOW = 4.0                         # chieu cham 4 lan: 0,91 s that -> 3,64 s tren man
MASS = (("hộp rỗng", "0,1 kg", False), ("hộp đầy", "0,4 kg", True))

def P(p, v, k): return (p[0] + v[0] * k, p[1] + v[1] * k)

# Chu Hi Lap (alpha, mu) ve bang Times New Roman Bold Italic: alpha cua SF de doc nham thanh a (gia toc).
_GK = "/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf"; _gc = {}
def FG(size):
    size = int(size)
    if size not in _gc: _gc[size] = ImageFont.truetype(_GK, size)
    return _gc[size]
def runs(s, size):
    out = []
    for part in re.split(r"([αμ])", s):
        if part: out.append((part, FG(size * 1.12) if part in "αμ" else F(size)))
    return out
def mwidth(d, s, size): return sum(tw(d, p, f) for p, f in runs(s, size))
def mtext(d, xy, s, size, color=INK, alpha=1.0, anchor="mm"):
    x = xy[0] - (mwidth(d, s, size) / 2 if anchor == "mm" else 0)
    for p, f in runs(s, size):
        dtext(d, (x, xy[1]), p, f, color, alpha, "lm"); x += tw(d, p, f)

def ramp(d, x0, yb, Lp):
    """Nem go goc 30 do: dinh tren-trai (x0, yb-h), chan doc (x0+w, yb). Tra ve diem dinh."""
    w, h = Lp * CA, Lp * SA
    top = (x0, yb - h); bot = (x0 + w, yb); th = 0.035 * Lp           # tam van day th, ke tren mot cot
    d.line([(x0 - 20, yb), (x0 + w + 60, yb)], fill=INK, width=4)
    d.rectangle([x0 + 4, top[1] + th, x0 + 4 + 0.04 * Lp, yb], fill=WOOD_D)
    d.polygon([top, bot, P(bot, NRM, -th), P(top, NRM, -th)], fill=WOOD)
    d.line([top, bot], fill=WOOD_D, width=5)
    r = 0.24 * Lp
    d.arc([x0 + w - r, yb - r, x0 + w + r, yb + r], 180, 210, fill=INK, width=4)
    text(d, (x0 + w - r - 56, yb - 22), "30°", 38, INK)
    return top

def box(d, top, Lp, s, full, scale=1.0):
    """Hop but tren mat doc, s = 0 (dau van) .. 1 (chan van)."""
    bl, bh = 0.17 * Lp * scale, 0.1 * Lp * scale
    mg = 0.02 * Lp
    b0 = P(top, U, mg + s * (Lp - bl - 2 * mg))
    b1 = P(b0, U, bl); b2 = P(b1, NRM, bh); b3 = P(b0, NRM, bh)
    if full:
        d.polygon([b0, b1, b2, b3], fill=(52, 64, 110), outline=NAVY)
        for j, col in enumerate((ORANGE, YELLOW, (96, 165, 250))):
            a = P(P(b0, NRM, bh * (0.25 + 0.25 * j)), U, bl * 0.12)
            d.line([a, P(a, U, bl * 0.76)], fill=col, width=7)
    else:
        d.polygon([b0, b1, b2, b3], fill=WHITE, outline=NAVY)
        d.line([b0, b1, b2, b3, b0], fill=NAVY, width=5)
    return b0, b1, b2, b3

def panel(d, box_xy, x0, yb, Lp, idx, s, clock=None, done=False):
    card(d, box_xy, fill=WHITE, outline=LIGHT, w=3)
    top = ramp(d, x0, yb, Lp)
    xf = x0 + Lp * CA
    for yy in range(int(yb - 0.2 * Lp), int(yb) - 6, 22):          # vach dich o chan van
        d.line([(xf + 34, yy), (xf + 34, yy + 12)], fill=RED, width=4)
    box(d, top, Lp, s, MASS[idx][2])
    nm, kg, _ = MASS[idx]
    lx = xf + 70
    text(d, (lx, box_xy[1] + 62), nm, 42, INK, anchor="lm")
    text(d, (lx, box_xy[1] + 118), kg, 44, NAVY, anchor="lm")
    if clock is not None:
        cy = box_xy[1] + 220
        card(d, (lx - 10, cy - 50, 1010, cy + 50), fill=(255, 247, 237) if not done else (236, 253, 243),
             outline=ORANGE if not done else GREEN, r=24, w=4)
        text(d, ((lx + 1000) / 2, cy), f"{clock:.2f} s".replace(".", ","), 52, INK if not done else GREEN)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    panel(d, (40, 265, 1040, 615), 80, 585, 440, 0, 0.0)
    panel(d, (40, 640, 1040, 990), 80, 960, 440, 1, 0.0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 210, "Thả cùng lúc.", 50, INK, maxw=880, alpha=a)
    ctext(d, y0 + 320, "Hộp nào tới chân ván trước?", 50, INK, maxw=880, alpha=a)
    tc, tend = M[1] + 0.8, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 470, 940, y0 + 484], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 470, 140 + 800 * (1 - p), y0 + 484], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
def run_start(sc): return sc["M"][0] + 0.7
def real_t(t, sc): return clamp((t - run_start(sc)) / SLOW, 0, T_SLIDE)

def s_do(img, d, t, sc):
    tr = real_t(t, sc); s = (tr / T_SLIDE) ** 2           # x = a t^2 / 2 -> ti le quang duong = (t/T)^2
    done = tr >= T_SLIDE - 1e-6
    panel(d, (40, 265, 1040, 855), 80, 815, 680, 0, s, clock=tr, done=done)
    panel(d, (40, 885, 1040, 1475), 80, 1435, 680, 1, s, clock=tr, done=done)
    k = appear(t, run_start(sc) - 0.6, 0.4) * (1 - appear(t, run_start(sc) + 0.4, 0.3))
    if k > 0:
        card(d, (300, 1515, 780, 1600), fill=A(ORANGE, k), r=40)
        text(d, (540, 1557), "Thả!", 46, WHITE, alpha=k)
    if t > run_start(sc) + 0.4:
        ka = appear(t, run_start(sc) + 0.4, 0.4)
        text(d, (540, 1557), "chiếu chậm 4 lần", 44, INK, bold=False, alpha=ka)

# ---------------- canh 3: Dap an + bang so lieu ----------------
ROWS = [(0.05, 2.4, 0.91), (0.1, 2.4, 0.91), (0.2, 2.4, 0.91), (0.4, 2.4, 0.91)]   # so_lieu_mau
def vn(x): return f"{x:g}".replace(".", ",")

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.5)
    pw = tw(d, "ĐÁP ÁN C", F(38)) + 56
    card(d, (W / 2 - pw / 2, 250, W / 2 + pw / 2, 314), fill=A(NAVY, ka), r=32)
    text(d, (W / 2, 282), "ĐÁP ÁN C", 38, WHITE, alpha=ka)
    card(d, (40, 345, 1040, 560), fill=A((236, 253, 243), ka), outline=A(GREEN, ka), w=5)
    ctext(d, 452, "Hai hộp tới chân ván cùng lúc", 48, GREEN, maxw=900, alpha=ka)
    y = 600
    card(d, (40, y, 1040, y + 700), fill=WHITE, outline=LIGHT, w=3)
    XS = (230, 540, 850)
    for x, s in zip(XS, ("m (kg)", "a (m/s²)", "t (s)")): text(d, (x, y + 60), s, 44, INK)
    d.line([(70, y + 110), (1010, y + 110)], fill=LIGHT, width=3)
    for j, (m, a, tt) in enumerate(ROWS):
        k = appear(t, M[0] + 0.2 + 0.3 * j, 0.4); yy = y + 190 + j * 130
        if m in (0.1, 0.4) and k > 0:
            d.rounded_rectangle([60, yy - 46, 1020, yy + 46], radius=20, fill=A((255, 247, 237), k))
        text(d, (XS[0], yy), vn(m), 52, INK, alpha=k)
        text(d, (XS[1], yy), vn(a), 52, NAVY, alpha=k)
        text(d, (XS[2], yy), vn(tt), 52, NAVY, alpha=k)
    k2 = appear(t, M[0] + 1.6, 0.5)
    mtext(d, (W / 2, 1390), "α = 30°   ·   μ = 0,3   ·   ván 1 m", 44, INK, alpha=k2)

# ---------------- canh 4: Rut ra (so do luc + dinh luat II) ----------------
def big_ramp_box(d):
    card(d, (40, 265, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    Lp, x0, yb = 900, 90, 935
    top = ramp(d, x0, yb, Lp)
    b0, b1, b2, b3 = box(d, top, Lp, 0.42, True, scale=1.0)
    c = ((b0[0] + b2[0]) / 2, (b0[1] + b2[1]) / 2)
    cm = P(b0, NRM, 6)                     # goc duoi-sau cua hop: Fms ve ra ngoai than hop, khong bi che
    return c, cm

LPF = 250
def forces(d, c, cm, show_comp=False, alpha=1.0):
    # P, N dat o tam hop (chat diem); N = P cos30 = 0,87 P; Fms = 0,3 N o mat tiep xuc; P sin30 doc doc (ti le dung)
    LP = LPF
    arrow(d, c, (c[0], c[1] + LP), A(BLUE, alpha), w=7)
    rich(d, c[0] - 44, c[1] + LP - 14, "P", 48, BLUE, alpha=alpha)
    pn = P(c, NRM, LP * CA)
    arrow(d, c, pn, A(GREEN, alpha), w=7)
    rich(d, pn[0] + 36, pn[1] + 4, "N", 48, GREEN, alpha=alpha)
    pf = P(cm, U, -0.3 * LP * CA)
    arrow(d, cm, pf, A(RED, alpha), w=7, head=18)
    lx, ly = pf[0] - 150, pf[1] - 70
    d.rounded_rectangle([lx - 12, ly - 40, lx + 112, ly + 44], radius=16, fill=A(WHITE, 0.92 * alpha), outline=A(RED, alpha), width=3)
    rich(d, lx, ly - 4, "F_{ms}", 58, RED, alpha=alpha, anchor="l")
    if show_comp:
        q = P(c, U, LP * SA)
        for k in range(8):                                   # net dut thanh phan P sin(alpha) doc doc
            a0, a1 = k / 8, (k + 0.55) / 8
            d.line([P(c, U, LP * SA * a0), P(c, U, LP * SA * a1)], fill=A(ORANGE, alpha), width=6)
        arrow(d, P(c, U, LP * SA * 0.9), q, A(ORANGE, alpha), w=6, head=18)

def pieces(d, cy, parts, size, alpha=1.0, strike=0.0):
    """parts: [(chu, mau, gach)] ve can giua; gach=True -> ve gach cheo theo strike (0..1)."""
    tot = sum(mwidth(d, s, size) for s, _, _ in parts); x = W / 2 - tot / 2
    for s, col, g in parts:
        wd = mwidth(d, s, size)
        mtext(d, (x, cy), s, size, col, alpha, "lm")
        if g and strike > 0:
            d.line([(x - 4, cy + size * 0.35), (x - 4 + (wd + 8) * strike, cy - size * 0.35)], fill=A(RED, alpha), width=6)
        x += wd

def s_rutra(img, d, t, sc):
    M = sc["M"]
    c, cm = big_ramp_box(d)
    forces(d, c, cm, show_comp=t > M[0] + 0.3)
    if t > M[0] + 0.3:
        q = P(c, U, LPF * SA)
        mtext(d, (q[0] + 34, q[1] + 34), "P·sinα", 44, ORANGE, alpha=appear(t, M[0] + 0.3, 0.4), anchor="lm")
    k1 = appear(t, M[0] + 0.4, 0.5)
    card(d, (40, 1000, 1040, 1620), fill=A(WHITE, k1), outline=A(NAVY, k1), w=5)
    mtext(d, (W / 2, 1075), "N = mg·cosα   →   Fms = μN", 46, INK, alpha=k1)
    k15 = appear(t, M[0] + 2.0, 0.5)
    d.line([(90, 1125), (990, 1125)], fill=A(LIGHT, k15), width=3)
    st = clamp((t - M[1] - 0.4) / 0.8)
    pieces(d, 1185, [("m", RED, True), ("a = ", INK, False), ("m", RED, True), ("g·sinα − μ", INK, False),
                     ("m", RED, True), ("g·cosα", INK, False)], 52, alpha=k15, strike=st)
    k3 = appear(t, M[1] + 1.4, 0.5)
    if k3 > 0:
        arrow(d, (W / 2, 1240), (W / 2, 1310), A(MUTED, k3), w=6, head=18)
        card(d, (110, 1335, 970, 1475), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
        mtext(d, (W / 2, 1405), "a = g(sinα − μ·cosα)", 56, GREEN, alpha=k3)
        text(d, (W / 2, 1550), "không còn m", 44, GREEN, alpha=k3)

# ---------------- canh 5: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    c, cm = big_ramp_box(d)
    LP = LPF
    arrow(d, c, (c[0], c[1] + LP), BLUE, w=7)
    rich(d, c[0] - 44, c[1] + LP - 14, "P", 48, BLUE)
    pn = P(c, NRM, LP * CA)
    arrow(d, c, pn, GREEN, w=7)
    rich(d, pn[0] + 36, pn[1] + 4, "N", 48, GREEN)
    text(d, (W / 2 + 230, 340), "N ngắn hơn P", 42, GREEN)
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if a1 > 0:
        y0 = 1000
        card(d, (40, y0, 1040, y0 + 600), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(RED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
        q = "“Áp lực N = mg”"
        ks = clamp((t - 1.0) / 0.4)
        f = F(48); lw = tw(d, q, f); yy = y0 + 200
        text(d, (W / 2, yy), q, 48, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.8 * a1), width=5)
        kk = a1 * appear(t, 1.5, 0.5)
        card(d, (110, y0 + 300, 970, y0 + 450), fill=A((236, 253, 243), kk), r=24)
        mtext(d, (W / 2, y0 + 375), "N = mg·cosα", 56, GREEN, alpha=kk)
    if k2 > 0:
        y0 = 1000 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 600), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Thí nghiệm chưa nói được", 46, NAVY, alpha=k2)
        kk = k2 * appear(t, M[1] + 0.2, 0.4)
        card(d, (70, y0 + 160, 1010, y0 + 460), fill=A((254, 242, 242), kk), outline=A(RED, kk), r=24, w=4)
        text(d, (W / 2, y0 + 230), "Chưa biết:", 44, RED, alpha=kk)
        ctext(d, y0 + 300, "hai đáy khác chất liệu", 48, RED, alpha=kk)
        mtext(d, (W / 2, y0 + 380), "(μ khác) thì sao?", 48, RED, alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def hint(d, t, k):                       # goi y tu ve (chu >= 40 px), hien tre 1,2 s nhu chot_hoi
        if k > 0.02:                         # hinh minh hoa: van nghieng, khong ma sat
            top = ramp(d, 250, 1245, 380); box(d, top, 380, 0.35, True)
            mtext(d, (720, 1150), "μ = 0", 50, NAVY, alpha=k)
        kh = appear(t, M[0] + 1.2, 0.5)
        if kh <= 0: return
        card(d, (110, 1290, 970, 1540), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1345), "Gợi ý", 40, INK, alpha=kh)
        text(d, (W / 2, 1420), "g = 10 m/s²", 46, ORANGE, alpha=kh)
        text(d, (W / 2, 1485), "sin 30° = 0,5", 46, ORANGE, alpha=kh)
    chot_hoi(d, t, sc, "Cùng dốc, cùng μ: gia tốc không phụ thuộc m",
             "Bỏ hẳn ma sát, dốc vẫn 30°. Gia tốc bằng bao nhiêu?", None, body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.3, "ding"),
            (do["t0"] + run_start(do), "tap"), (do["t0"] + run_start(do) + T_SLIDE * SLOW, "tap"),
            (da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] + 0.4, "tap"),
            (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-giaibt-dlh-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Giải bài toán động lực học · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai hộp bút trên ván nghiêng", draw=s_hook, tail=0.8, caps=[
   ("Hai hộp bút, hai ván như nhau.", 3.0),
   ("Dừng video, chọn câu trả lời.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Nhìn hai đồng hồ.", 4.8),
   ("Hai đồng hồ dừng cùng số.", 3.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Nặng gấp bốn, thời gian vẫn vậy.", 4.0)]),
 dict(key="rutra", title="Vì sao?", draw=s_rutra, tail=0.6, caps=[
   ("Tính ma sát, rồi định luật II.", 4.4),
   ("Cả ba số hạng đều chứa m.", 3.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Bẫy thường gặp.", 3.0),
   ("Giới hạn thí nghiệm.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 5.4)]),
])
