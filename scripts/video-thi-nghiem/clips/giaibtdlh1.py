# Clip: tn-l10-giaibt-dlh-01 - Hai hop but (rong / day) truot tren van nghieng (30/10/2026; cong moi 27/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-giaibt-dlh-01.json:
#   tham_so: alpha = 30 deg, mu = 0,3, L = 1 m ; so_lieu_mau: m = 0,05 / 0,1 / 0,2 / 0,4 kg -> a = 2,4 m/s2, t = 0,91 s.
#   Hop rong = 0,1 kg, hop day = 0,4 kg (hai hang cua so_lieu_mau) -> nang gap 4.
#   mo_hinh: N = m.g.cos(alpha), Fms = mu.N ; P.sin(alpha) keo xuong doc, Fms huong LEN doc (hop truot xuong).
# Du doan (27/11): bai da hoi "ai toi truoc" o Mo bai, hop exp ghi Quan sat "toi gan nhu cung luc", Nhin vao hoi lai
#   -> KHONG hoi hop nao toi truoc. Hoi: hop day nang gap 4 -> ma sat van len no gap may lan? Dap an: gap 4 (Fms = mu.m.g.cos).
#   Cot luc ve ti le dung: P.sin = 0,5 / 2,0 N ; Fms = 0,26 / 1,04 N (khong in so len man).
# Cau chot: hop day 0,4 kg, mu = 0,3, doc 30 deg -> Fms = 0,3.0,4.10.cos30 ~ 1,0 N. Dap so khong hien.
from engine import *

ALPHA = math.radians(30)
CA, SA = math.cos(ALPHA), math.sin(ALPHA)
U = (CA, SA)                       # doc theo doc, huong xuong
NRM = (SA, -CA)                    # phap tuyen huong ra khoi mat doc (len)
WOOD = (176, 124, 74); WOOD_D = (140, 96, 54)
T_SLIDE = 0.91                     # s (so_lieu_mau)
SLOW = 4.0                         # chieu cham 4 lan: 0,91 s that -> 3,64 s tren man
MASS = (("hộp rỗng", "0,1 kg", False), ("hộp đầy", "0,4 kg", True))
MU, G = 0.3, 10.0
DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)

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
    text(d, (x0 + w - r - 62, yb - 26), "30°", 55, INK)
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
    text(d, (lx, box_xy[1] + 62), nm, 55, INK, anchor="lm")
    text(d, (lx, box_xy[1] + 130), kg, 55, NAVY, anchor="lm")
    if clock is not None:
        cy = box_xy[1] + 235
        card(d, (lx - 10, cy - 50, 1010, cy + 50), fill=(255, 247, 237) if not done else (236, 253, 243),
             outline=ORANGE if not done else GREEN, r=24, w=4)
        text(d, ((lx + 1000) / 2, cy), f"{clock:.2f} s".replace(".", ","), 58, INK if not done else GREEN)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0, x0=175, step=150, w=130):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = x0 + i * step
        if i < on: card(d, (x, y, x + w, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + w, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    panel(d, (40, 265, 1040, 615), 80, 585, 440, 0, 0.0)
    panel(d, (40, 640, 1040, 990), 80, 960, 440, 1, 0.0)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1085 + (1 - k) * 30
    card(d, (40, y0, 1040, y0 + 500), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, k)
    for j, s1 in enumerate(("Hộp đầy nặng gấp 4.", "Ma sát lên nó gấp mấy lần?")):
        text(d, (W / 2, y0 + 190 + j * 85), s1, 60, PURPLE if j == 1 else INK, alpha=k)
    seg_bar(d, y0 + 400, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, k)

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
        card(d, (330, 1510, 750, 1600), fill=A(ORANGE, k), r=40)
        text(d, (540, 1555), "Thả!", 58, WHITE, alpha=k)
    if t > run_start(sc) + 0.4:
        ka = appear(t, run_start(sc) + 0.4, 0.4)
        text(d, (540, 1555), "chiếu chậm 4 lần", 55, INK, bold=False, alpha=ka)

# ---------------- hinh doc lon + luc doc doc ----------------
def big_ramp_box(d, y1=1000):
    card(d, (40, 265, 1040, y1), fill=WHITE, outline=LIGHT, w=3)
    Lp, x0, yb = 900, 90, 935
    top = ramp(d, x0, yb, Lp)
    b0, b1, b2, b3 = box(d, top, Lp, 0.42, True, scale=1.0)
    c = ((b0[0] + b2[0]) / 2, (b0[1] + b2[1]) / 2)
    cm = P(b0, NRM, 6)                     # goc duoi-sau cua hop: Fms ve ra ngoai than hop, khong bi che
    return c, cm

LPF = 250
def along(d, c, cm, k=1.0):
    """Hai luc doc doc, ti le dung: P.sin30 = 0,5 P (xuong doc, cam) ; Fms = 0,3.0,87 P = 0,26 P (len doc, do)."""
    q = P(c, U, LPF * SA)
    arrow(d, c, q, A(ORANGE, k), w=7, head=20)
    mtext(d, (q[0] + 30, q[1] + 40), "P·sinα", 55, DORANGE, alpha=k, anchor="lm")
    pf = P(cm, U, -MU * LPF * CA)
    arrow(d, cm, pf, A(RED, k), w=7, head=18)
    lx, ly = pf[0] - 40, pf[1] - 120
    card(d, (lx - 70, ly - 40, lx + 70, ly + 40), fill=A(WHITE, 0.92 * k), outline=A(RED, k), r=18, w=3)
    text(d, (lx, ly), "Fms", 55, DRED, alpha=k)

def forces(d, c, cm, show_comp=False, alpha=1.0):
    LP = LPF
    arrow(d, c, (c[0], c[1] + LP), A(BLUE, alpha), w=7)
    text(d, (c[0] - 44, c[1] + LP - 14), "P", 58, BLUE, alpha=alpha)
    pn = P(c, NRM, LP * CA)
    arrow(d, c, pn, A(GREEN, alpha), w=7)
    text(d, (pn[0] + 40, pn[1] + 4), "N", 58, DGREEN, alpha=alpha)
    pf = P(cm, U, -MU * LP * CA)
    arrow(d, cm, pf, A(RED, alpha), w=7, head=18)
    lx, ly = pf[0] - 40, pf[1] - 120
    card(d, (lx - 70, ly - 40, lx + 70, ly + 40), fill=A(WHITE, 0.92 * alpha), outline=A(RED, alpha), r=18, w=3)
    text(d, (lx, ly), "Fms", 55, DRED, alpha=alpha)
    if show_comp:
        q = P(c, U, LP * SA)
        for k in range(8):                                   # net dut thanh phan P sin(alpha) doc doc
            a0, a1 = k / 8, (k + 0.55) / 8
            d.line([P(c, U, LP * SA * a0), P(c, U, LP * SA * a1)], fill=A(ORANGE, alpha), width=6)
        arrow(d, P(c, U, LP * SA * 0.9), q, A(ORANGE, alpha), w=6, head=18)

# ---------------- canh 3: Dap an (cot luc ti le) ----------------
BX0, BSC = 330, 320                       # cot bat dau x ; px moi N (2,0 N -> 640 px)
def bars(d, t, t0, kx):
    card(d, (40, 1030, 1040, 1590), fill=WHITE, outline=LIGHT, w=3)
    text(d, (300, 1075), "kéo xuống dốc", 55, DORANGE)
    text(d, (760, 1075), "ma sát", 55, DRED)
    mtext(d, (300, 1140), "P·sinα", 55, DORANGE)
    text(d, (760, 1140), "Fms", 55, DRED)
    d.line([(BX0, 1175), (BX0, 1560)], fill=NAVY, width=4)
    g = ease(clamp((t - t0) / 1.8))
    for i, (nm, kg, _) in enumerate(MASS):
        m = (0.1, 0.4)[i]; y = 1210 + i * 200
        text(d, (70, y + 32), nm, 55, INK, anchor="lm")
        ps, fm = m * G * SA, MU * m * G * CA
        d.rounded_rectangle([BX0, y - 10, BX0 + BSC * ps * g, y + 34], radius=10, fill=ORANGE)
        d.rounded_rectangle([BX0, y + 44, BX0 + BSC * fm * g, y + 88], radius=10, fill=RED)
        if i == 1 and kx > 0:
            text(d, (BX0 + BSC * fm + 70, y + 66), "×4", 58, DRED, alpha=kx)
            text(d, (BX0 + BSC * ps - 70, y - 50), "×4", 58, DORANGE, alpha=kx)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    c, cm = big_ramp_box(d)
    along(d, c, cm, appear(t, 0.3, 0.4))
    bars(d, t, 0.5, appear(t, M[1], 0.4))
    ka = appear(t, M[1], 0.45)
    if ka <= 0: return
    yk = 290 + (1 - ka) * 30                                                 # v2: goc tren-phai, khong che hop + Fms
    card(d, (580, yk, 1025, yk + 250), fill=A(WHITE, ka), outline=A(NAVY, ka), w=6)
    pill(d, 802, yk + 70, "ĐÁP ÁN", NAVY, ka)
    text(d, (802, yk + 175), "ma sát gấp 4", 58, BLUE, alpha=ka)

# ---------------- canh 4: Rut ra (so do luc + dinh luat II) ----------------
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
    forces(d, c, cm, show_comp=t > 0.6)
    if t > 0.6:
        q = P(c, U, LPF * SA)
        mtext(d, (q[0] + 30, q[1] + 40), "P·sinα", 55, DORANGE, alpha=appear(t, 0.6, 0.4), anchor="lm")
    k1 = appear(t, 0.6, 0.5)
    card(d, (40, 1030, 1040, 1590), fill=A(WHITE, k1), outline=A(GREEN, k1), w=6)
    pill(d, W / 2, 1100, "RÚT RA", GREEN, k1)
    mtext(d, (W / 2, 1210), "N = mg·cosα → Fms = μN", 58, INK, alpha=k1)
    k2 = appear(t, M[1], 0.5)
    st = clamp((t - M[1] - 0.6) / 0.8)
    pieces(d, 1320, [("m", RED, True), ("a = ", INK, False), ("m", RED, True), ("g·sinα − μ", INK, False),
                     ("m", RED, True), ("g·cosα", INK, False)], 58, alpha=k2, strike=st)
    k3 = appear(t, M[1], 0.5)
    mtext(d, (W / 2, 1440), "a = g(sinα − μ·cosα)", 60, DGREEN, alpha=k3 * st)
    text(d, (W / 2, 1525), "không còn m", 58, DGREEN, alpha=k3 * st)

# ---------------- canh 5: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    c, cm = big_ramp_box(d)
    LP = LPF
    arrow(d, c, (c[0], c[1] + LP), BLUE, w=7)
    text(d, (c[0] - 44, c[1] + LP - 14), "P", 58, BLUE)
    kn = appear(t, M[1], 0.4)
    gN = 0.3 + 0.7 * ease(clamp((t - M[1]) / 1.2))            # N moc dan tu tam hop, dai = P.cos30 (ti le dung)
    pn = P(c, NRM, LP * CA * gN)
    arrow(d, c, pn, GREEN, w=7)
    text(d, (pn[0] + 40, pn[1] + 4), "N", 58, DGREEN)
    text(d, (760, 340), "N ngắn hơn P", 55, DGREEN, alpha=kn)
    a1 = appear(t, 0.15, 0.4)
    y0 = 1030
    card(d, (40, y0, 1040, 1590), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
    pill(d, W / 2, y0 + 70, "BẪY", DRED, a1)
    q = "Áp lực N = mg"
    ks = clamp((t - M[1]) / 0.4); yy = y0 + 200
    lw = tw(d, q, F(60))
    text(d, (W / 2, yy), q, 60, mix(INK, GRAY, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
    mtext(d, (W / 2, yy + 110), "N = mg·cosα", 60, DGREEN, alpha=kn)
    k3 = appear(t, M[2] - 0.1, 0.4)
    if k3 > 0:
        yk = 1180 + (1 - k3) * 30
        card(d, (40, yk, 1040, yk + 400), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, yk + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, yk + 195), "Hai đáy cùng chất liệu", 58, INK, alpha=k3)
        mtext(d, (W / 2, yk + 295), "Đáy khác chất (μ khác)?", 58, INK, alpha=k3)

# ---------------- canh 6: Thu nghi ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    top = ramp(d, 120, 900, 640)
    sb = 0.1 + 0.25 * ease(clamp((t - 0.4) / 3.0))
    box(d, top, 640, sb, True)
    text(d, (820, 500), "0,4 kg", 58, NAVY, alpha=k)
    mtext(d, (820, 580), "hệ số μ = 0,3", 58, NAVY, alpha=k)
    text(d, (820, 660), "g = 10 m/s²", 58, NAVY, alpha=k)
    card(d, (40, 1030, 1040, 1585), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 1100, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 1215), "Hộp đang trượt xuống.", 60, INK, alpha=k)
    text(d, (W / 2, 1310), "Ma sát lên hộp bao nhiêu N?", 60, DORANGE, alpha=k)
    seg_bar(d, 1420, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"),
            (do["t0"] + run_start(do), "tap"), (do["t0"] + run_start(do) + T_SLIDE * SLOW, "tap"),
            (da["t0"] + da["M"][1], "ding"), (r["t0"] + r["M"][1] + 0.6, "tap"),
            (b["t0"] + b["M"][1], "buzz"), (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l10-giaibt-dlh-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Giải bài toán động lực học · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai hộp bút trên ván nghiêng", draw=s_hook, tail=0.2, caps=[
   ("Hai hộp bút, đáy như nhau.", 3.0),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Thả cùng lúc, chiếu chậm 4 lần.", 4.8),
   ("Hai đồng hồ dừng cùng số.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("So hai lực dọc dốc.", 3.0),
   ("Đáp án: ma sát gấp 4.", 3.4)]),
 dict(key="rutra", title="Vì sao?", draw=s_rutra, tail=0.3, caps=[
   ("Tính ma sát, rồi định luật II.", 3.8),
   ("Ba số hạng đều chứa m.", 3.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Áp lực N = mg?", 3.0),
   ("Không: N = mg·cosα.", 3.0),
   ("Đáy khác chất thì sao?", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 6.0)]),
])
