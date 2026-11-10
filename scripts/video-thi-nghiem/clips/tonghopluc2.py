# Clip: tn-l10-tonghopluc-02 - Vat tren mat phang nghieng: luc ke keo doc van (30/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-tonghopluc-02.json:
#   tham_so: P = 2,0 N, alpha 0-80 do ; luc ke 0-5 N (dung_cu) ;
#   so_lieu_mau: alpha 15/30/45/60 -> Px 0,52/1,0/1,41/1,73 ; Py 1,93/1,73/1,41/1,0 (quan_sat lam tron 0,5/1,0/1,4).
#   Cau hoi chot dung alpha = 15 do, luc ep Py = 1,93 N (khoang 1,9 N; chua tung hien tren man).
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (nang van 15 -> 30 -> 45 trong MOT canh, bang so lieu)
#       -> Dap an B + phan tich P (vecto dung ti le) -> Bay (P cos alpha) roi Chua noi duoc (van nham)
#       -> Chot + cau hoi tu nho lai (60 do, luc ep len van).
from engine import *

# Chu alpha ve bang Times New Roman Bold Italic: alpha cua SF de doc nham thanh "a".
_GK = "/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf"; _gc = {}
def FG(size):
    size = int(size)
    if size not in _gc: _gc[size] = ImageFont.truetype(_GK, size)
    return _gc[size]
def runs(s, size):
    return [(p, FG(size * 1.12) if p == "α" else F(size)) for p in re.split(r"(α)", s) if p]
def mwidth(d, s, size): return sum(tw(d, p, f) for p, f in runs(s, size))
def mtext(d, xy, s, size, color=INK, alpha=1.0):
    x = xy[0] - mwidth(d, s, size) / 2
    for p, f in runs(s, size):
        dtext(d, (x, xy[1]), p, f, color, alpha, "lm"); x += tw(d, p, f)
def mlines(d, y, s, size, color=INK, alpha=1.0, lh=1.24):
    ls = s.split("\n"); y0 = y - (len(ls) - 1) * size * lh / 2
    for i, l in enumerate(ls): mtext(d, (W / 2, y0 + i * size * lh), l, size, color, alpha)

# ---------------- bo cuc (khung nguon 1080x1920) ----------------
HX, HY = 90, 900                  # ban le van (goc duoi trai)
LB = 760                          # chieu dai van
S0, BW, BH = 170, 130, 100        # vat: vi tri doc van, dai, cao (canh 45 do: thap de tay khong cham chip)
S0_HOOK_DO, S0_VEC = 170, 260      # canh co vecto P (30 do): vat cao hon de P khong cham dat
ROPE, BODY = 70, 320              # day tu vat toi moc luc ke ; than luc ke
HOOK_H = BH / 2                   # day/luc ke o do cao giua vat
FMAX = 5.0                        # luc ke 0-5 N
P_N = 2.0
LF = 180                          # px cho 2,0 N (vecto dung ti le)
WOOD = (176, 124, 74); WOOD_D = (140, 96, 54); SKIN = (240, 196, 160)
DRED = (185, 28, 28)
ROWS = [(15, "0,5"), (30, "1,0"), (45, "1,4")]     # quan_sat (so_lieu_mau 0,52 / 1,0 / 1,41)

def frame_of(a):
    r = math.radians(a); c, s = math.cos(r), math.sin(r)
    u = (c, -s); n = (-s, -c)                       # u: len doc ; n: phap tuyen ra khoi mat van
    def Q(sx, h=0.0): return (HX + u[0] * sx + n[0] * h, HY + u[1] * sx + n[1] * h)
    return u, n, Q

def dashed(d, p, q, color, w=4, seg=14, gap=10):
    L = math.dist(p, q); k = 0
    while k * (seg + gap) < L:
        a = k * (seg + gap) / L; b = min(1, (k * (seg + gap) + seg) / L)
        d.line([(lerp(p[0], q[0], a), lerp(p[1], q[1], a)), (lerp(p[0], q[0], b), lerp(p[1], q[1], b))], fill=color, width=w)
        k += 1

def board(d, a, label=True):
    u, n, Q = frame_of(a)
    d.line([(40, HY), (1040, HY)], fill=INK, width=5)
    for x in range(60, 1040, 40): d.line([(x, HY + 4), (x - 18, HY + 24)], fill=GRAY, width=3)
    th = 18
    top0, top1 = Q(0), Q(LB); bot1, bot0 = Q(LB, -th), Q(0, -th)
    px = Q(LB * 0.86, -th)                          # chan gia do
    d.rectangle([px[0] - 9, px[1], px[0] + 9, HY], fill=WOOD_D)
    d.polygon([top0, top1, bot1, bot0], fill=WOOD)
    d.line([top0, top1], fill=WOOD_D, width=5)
    dot(d, HX, HY, 10, NAVY)
    if a >= 5:
        r = 170
        d.arc([HX - r, HY - r, HX + r, HY + r], -a, 0, fill=ORANGE, width=5)
        if label:
            rr = 300; m = math.radians(a / 2)
            text(d, (HX + rr * math.cos(m) + 30, HY - rr * math.sin(m) + 4 + (20 if a < 20 else 0)), f"{a}°", 40, ORANGE)

def block(d, a, label=True):
    u, n, Q = frame_of(a)
    pts = [Q(S0), Q(S0 + BW), Q(S0 + BW, BH), Q(S0, BH)]
    d.polygon(pts, fill=(90, 98, 120)); d.line(pts + [pts[0]], fill=NAVY, width=4)
    dot(d, *Q(S0 + BW, HOOK_H), 7, NAVY)

def meter(d, a, f_read):
    """Day + luc ke lo xo (mau trongluc2: 0-5 N, vach 0,2 N cho thua tren van ngan) + tay giu, doc theo van. f_read None: che thang do bang "?"."""
    u, n, Q = frame_of(a)
    Qm = lambda s, h=0.0: Q(s, HOOK_H + h)
    hk = S0 + BW + ROPE
    d.line([Qm(S0 + BW), Qm(hk - 13)], fill=NAVY, width=5)
    se = luc_ke(d, Qm, hk, hk + 20, hk + 20 + BODY, FMAX, f_read, nho=0.2, hw=40, ben=1)
    d.line([Qm(se - 16), Qm(se + 12)], fill=NAVY, width=8)
    hx, hy = Qm(se + 40)
    dot(d, hx, hy, 28, SKIN, outline=(190, 140, 105))

def readout(d, val, sub=None):
    card(d, (770, 300, 1040, 500), fill=WHITE, outline=LIGHT, r=26, w=3)     # goc phai tren: khong cham van/tay o 15-45 do
    text(d, (905, 348), "Lực kế chỉ", 38, INK, bold=False)
    text(d, (905, 428), val, 62, INK)

def rig(d, a, f_read, val, sub=None):
    board(d, a); block(d, a); meter(d, a, f_read); readout(d, val, sub)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    global S0; S0 = S0_HOOK_DO
    M = sc["M"]
    rig(d, 30, None, "?")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 570), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 280, "Ván trơn nghiêng 30°,\nquả nặng 2,0 N.\nLực kế kéo dọc ván\nchỉ bao nhiêu?", 46, INK,
          maxw=900, alpha=a)
    tc, tend = M[1] + 0.5, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 520, 940, y0 + 532], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 520, 140 + 800 * (1 - p), y0 + 532], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (nang van trong MOT canh) ----------------
MOVE = 1.0
def ang_at(t, sc):
    M = sc["M"]
    if t < M[1]: return 15.0
    if t < M[2]: return lerp(15, 30, ease((t - M[1]) / MOVE))
    return lerp(30, 45, ease((t - M[2]) / MOVE))

def chips(d, cur):
    for j, (a, _) in enumerate(ROWS):
        x0 = 150 + j * 270; box = (x0, 226, x0 + 240, 284); s = f"{a}°"
        if j == cur: card(d, box, fill=ORANGE, r=27); text(d, (x0 + 120, 255), s, 38, WHITE)
        elif j < cur: card(d, box, fill=LIGHT, r=27); text(d, (x0 + 120, 255), s, 38, INK)
        else: card(d, box, fill=None, outline=LIGHT, r=27, w=3); text(d, (x0 + 120, 255), s, 38, MUTED)

def table(d, n, y=1000):
    card(d, (40, y, 1040, y + 580), fill=WHITE, outline=NAVY, w=4)
    text(d, (W / 2, y + 56), "Quả nặng P = 2,0 N", 40, NAVY)
    xs = (330, 750)
    mtext(d, (xs[0], y + 140), "Góc α", 40, INK)
    text(d, (xs[1], y + 140), "Lực kế (N)", 40, INK)
    d.line([(70, y + 186), (1010, y + 186)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 260 + i * 105
        text(d, (xs[0], yy), f"{ROWS[i][0]}°", 44, INK)
        text(d, (xs[1], yy), ROWS[i][1], 46, BLUE)

def s_do(img, d, t, sc):
    global S0; S0 = S0_HOOK_DO
    M = sc["M"]; a = ang_at(t, sc); cur = max(0, cur_cap(sc, t))
    moving = any(M[i] <= t < M[i] + MOVE + 0.5 for i in (1, 2))
    chips(d, cur)
    ai = int(round(a))
    if moving: board(d, ai, label=False); block(d, ai); meter(d, ai, P_N * math.sin(math.radians(a))); readout(d, "···")
    else:
        v = ROWS[cur][1]
        rig(d, ai, float(v.replace(",", ".")), v + " N")
    table(d, sum(t >= M[i] + 1.6 for i in range(3)))

# ---------------- canh 3: Dap an + phan tich P (vecto dung ti le) ----------------
def harrow(d, p1, p2, color, alpha, w=9):
    arrow(d, p1, p2, A(WHITE, alpha), w=w + 7, head=26); arrow(d, p1, p2, A(color, alpha), w=w, head=24)

def sublab(d, x, y, main, sub, color, alpha=1.0):
    """Nhan vecto co chi so duoi du lon: chu chinh 46 px, chi so 38 px (sau thu x0,88 van >= 32 px)."""
    fm, fs = F(46), F(38); w = tw(d, main, fm) + tw(d, sub, fs); x0 = x - w / 2
    dtext(d, (x0, y), main, fm, color, alpha, "lm"); dtext(d, (x0 + tw(d, main, fm), y + 16), sub, fs, color, alpha, "lm")

def vecs(img, d, alpha, comp_alpha, a=30, px_col=None):
    """P (2,0 N = LF px), Px = P sin a doc van xuong, Py = P cos a vuong goc vao van, N = Py ra khoi van,
       F luc ke = Px len doc (ve song song phia tren day, chan F = mat vat). Dung ti le giua cac vecto.
       Mui ten + net chieu ve tren lop rieng; phan nam duoi mat van mo con 55% (khong 'xuyen' van)."""
    u, n, Q = frame_of(a); r = math.radians(a)
    c = Q(S0 + BW / 2, BH / 2)
    lx, ly = LF * math.sin(r), LF * math.cos(r)
    pe = (c[0], c[1] + LF)
    ex = (c[0] - u[0] * lx, c[1] - u[1] * lx)                     # Px xuong doc
    ey = (c[0] - n[0] * ly, c[1] - n[1] * ly)                     # Py vao van
    en = (c[0] + n[0] * ly, c[1] + n[1] * ly)                     # N ra khoi van, = Py
    f0 = Q(S0 + BW, BH - 2); f1 = (f0[0] + u[0] * lx, f0[1] + u[1] * lx)   # F = Px, len doc, tren day
    L = Image.new("RGBA", img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    if comp_alpha > 0:
        dashed(dl, ex, pe, A(MUTED, comp_alpha), w=3); dashed(dl, ey, pe, A(MUTED, comp_alpha), w=3)
        harrow(dl, c, ex, px_col or PURPLE, comp_alpha, w=7)
        harrow(dl, c, ey, TEAL, comp_alpha, w=7)
    if alpha > 0:
        harrow(dl, c, pe, BLUE, alpha); harrow(dl, c, en, GREEN, alpha, w=7); harrow(dl, f0, f1, RED, alpha, w=7)
    arr = np.array(L); ys, xs = np.mgrid[0:arr.shape[0], 0:arr.shape[1]]
    below = ys > HY - (xs - HX) * math.tan(r) + 2                 # duoi mat van
    arr[..., 3] = np.where(below, (arr[..., 3] * 0.55).astype(np.uint8), arr[..., 3])
    L = Image.fromarray(arr, "RGBA"); img.paste(L, (0, 0), L)
    dot(d, c[0], c[1], 9, NAVY, outline=WHITE)                   # diem dat tai tam vat
    if comp_alpha > 0:
        sublab(d, ex[0] - 66, ex[1] - 56, "P", "x", px_col or PURPLE, comp_alpha)
        sublab(d, ey[0] + 66, ey[1] + 14, "P", "y", TEAL, comp_alpha)
    text(d, (pe[0] - 40, pe[1] - 14), "P", 46, BLUE, alpha=alpha)
    text(d, (en[0] - 32, en[1] - 32), "N", 46, GREEN, alpha=alpha)
    text(d, (f0[0] + n[0] * 44, f0[1] + n[1] * 44), "F", 46, RED, alpha=alpha)   # o goc vat: dau mui ten sat than luc ke
    return c

def s_dapan(img, d, t, sc):
    global S0; S0 = S0_VEC
    M = sc["M"]
    board(d, 30, label=False); block(d, 30); meter(d, 30, 1.0)
    ka = appear(t, 0.1, 0.5)
    pw = tw(d, "ĐÁP ÁN B", F(36)) + 52
    card(d, (W - 60 - pw, 300, W - 60, 360), fill=A(NAVY, ka), r=30)
    text(d, (W - 60 - pw / 2, 330), "ĐÁP ÁN B", 36, WHITE, alpha=ka)
    vecs(img, d, appear(t, M[0] + 0.2, 0.5), appear(t, M[1] - 0.1, 0.5))
    k1 = appear(t, 0.3, 0.5)
    card(d, (40, 1060, 1040, 1270), fill=A(WHITE, k1), outline=A(BLUE, k1), w=5)
    ctext(d, 1165, "30°: lực kế chỉ 1,0 N", 48, INK, maxw=900, alpha=k1)
    k2 = appear(t, M[1] + 0.3, 0.5)
    card(d, (40, 1310, 1040, 1560), fill=A(WHITE, k2), outline=A(GREEN, k2), w=5)
    mtext(d, (W / 2, 1435), "F = P·sin α", 54, GREEN, alpha=k2)

# ---------------- canh 4: Bay roi Chua noi duoc (khong hien cung luc) ----------------
def s_bay(img, d, t, sc):
    global S0; S0 = S0_VEC
    M = sc["M"]
    board(d, 30, label=False); block(d, 30); meter(d, 30, 1.0)
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.15, 0.4) * (1 - k2)
    c = vecs(img, d, 1.0, 1.0, px_col=DRED if a1 > 0.5 else None)
    # goc alpha giua P (thang xuong) va Py (vao van): Px doi dien goc nay
    rr = 78
    d.arc([c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr], 60, 90, fill=ORANGE, width=5)
    m = math.radians(75)
    dtext(d, (c[0] + 112 * math.cos(m) + 6, c[1] + 112 * math.sin(m)), "α", FG(46), ORANGE)
    if a1 > 0:
        y0 = 1000
        card(d, (40, y0, 1040, y0 + 580), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
        q = "“Lực kéo = P·cos α”"
        ks = clamp((t - 0.9) / 0.4)
        lw = mwidth(d, q, 50); yy = y0 + 210
        mtext(d, (W / 2, yy), q, 50, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=5)
        kk = a1 * appear(t, 1.1, 0.35)
        mlines(d, y0 + 420, "Dọc ván: cạnh đối góc α\n→ sin", 48, DRED, alpha=kk, lh=1.55)
    if k2 > 0:
        y0 = 1000 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 580), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 48, NAVY, alpha=k2)
        kk = k2 * appear(t, M[1] + 0.2, 0.4)
        card(d, (70, y0 + 160, 1010, y0 + 480), fill=A((254, 242, 242), kk), outline=A(DRED, kk), r=24, w=4)
        ctext(d, y0 + 240, "Ván nhám:", 46, DRED, maxw=880, alpha=kk)
        ctext(d, y0 + 320, "lực kế chỉ bao nhiêu?", 46, INK, maxw=880, alpha=kk)
        ctext(d, y0 + 410, "→ xét ở bài Ma sát", 42, NAVY, maxw=880, alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    mtext(d, (W / 2, 400), "Lực kế dọc ván = P·sin α", 52, GREEN, alpha=k0)
    k1 = appear(t, M[0] + 0.6, 0.5)
    if k1 <= 0: return
    card(d, (40, 580, 1040, 1340), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 610, W / 2 + pw / 2, 674), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 642), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 840, "Ván nghiêng 15°, P = 2,0 N.\nVật ép lên ván\nmột lực khoảng bao nhiêu?", 48, INK, maxw=900,
          alpha=appear(t, M[0] + 0.9, 0.5))
    kh = appear(t, M[0] + 0.9 + 2.5, 0.5)
    card(d, (110, 1030, 970, 1290), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1085, "Gợi ý", 40, INK, alpha=kh)
    ctext(d, 1195, "Vẽ lại hai thành phần của P.", 44, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.3, "ding"),
            (do["t0"] + M[1], "tap"), (do["t0"] + M[2], "tap"),
            (da["t0"] + 0.1, "ding"), (b["t0"] + 0.15, "buzz"),
            (e["t0"] + e["M"][0] + 0.6, "open")]

CLIP = dict(id="tn-l10-tonghopluc-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Tổng hợp và phân tích lực · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Quả nặng trên ván nghiêng", draw=s_hook, tail=0.8, caps=[
   ("Quả nặng nằm yên trên ván nghiêng.", 3.8),
   ("Tự đoán trước khi xem tiếp.", 6.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Nghiêng 15°, đọc lực kế.", 3.0),
   ("Nâng ván lên 30°.", 2.6),
   ("Nâng tiếp tới 45°.", 2.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Phân tích trọng lực theo hai phương.", 4.6),
   ("Lực kế cân bằng thành phần dọc ván.", 4.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Bẫy thường gặp.", 3.4),
   ("Điều thí nghiệm chưa đo.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 7.6)]),
])
