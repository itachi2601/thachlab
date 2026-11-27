# Clip: tn-l10-tonghopluc-02 - Vat tren mat phang nghieng: luc ke keo doc van (30/10/2026; dung lai 27/11/2026 theo
# cong moi viec 4: --do-chu 0 LOI, chu ve >= 55 px, luc ke = engine.luc_ke(), khong nut A-D, Bay hai nhip, chot A-D o khung).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-tonghopluc-02.json (_kiem_so() doi chieu):
#   tham_so: P = 2,0 N, alpha 0-80 do; luc ke 0-5 N (vach 0,2 N);
#   so_lieu_mau: alpha 15/30/45/60 -> Px 0,52/1,0/1,41/1,73 ; Py 1,93/1,73/1,41/1,0 (quan_sat lam tron 0,5/1,0/1,4).
# Du doan (doi 27/11: ca 30 do -> 1,0 N cung kieu Cau 5 cua bai (thung 5 kg doc 30 do) nen doi sang du doan HUONG):
#   nang van 15 -> 45 do, so chi luc ke the nao so voi P = 2,0 N? -> tang dan nhung luon nho hon P.
# Bay = hien_tuong_hay_sai[0] "Px = P cos alpha": o 30 do P cos 30 = 1,73 ~ 1,7 N (so_lieu_mau Py) khac 1,0 N luc ke do;
#   nhip 2: goc alpha giua P va Py, Px doi dien goc -> sin.
# Chua noi duoc: gia_thiet "van tron" -> van nham.
# Chot (THU NGHI = cau_chot khung web): van 15 do, vat ep len van bao nhieu? -> Py = 1,93 ~ 1,9 N (so_lieu_mau hang 1).
#   Can mot buoc chua chieu (cos 15 do, hoac Pitago tu 0,5 N va 2,0 N). So 1,9 / 1,93 khong hien truoc do.
from engine import *

_GK = "/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf"; _gc = {}
def FG(size):                       # alpha cua SF de doc nham thanh "a" -> Times Bold Italic
    size = int(size)
    if size not in _gc: _gc[size] = ImageFont.truetype(_GK, size)
    return _gc[size]
def runs(s, size): return [(p, FG(size * 1.12) if p == "α" else F(size)) for p in re.split(r"(α)", s) if p]
def mwidth(d, s, size): return sum(tw(d, p, f) for p, f in runs(s, size))
def mtext(d, xy, s, size, color=INK, alpha=1.0):
    x = xy[0] - mwidth(d, s, size) / 2
    for p, f in runs(s, size):
        dtext(d, (x, xy[1]), p, f, color, alpha, "lm"); x += tw(d, p, f)

P_N = 2.0
ROWS = [(15, "0,5"), (30, "1,0"), (45, "1,4")]     # quan_sat (so_lieu_mau 0,52 / 1,0 / 1,41)
def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-tonghopluc-02.json")))
    assert {p["ky_hieu"]: p for p in k["tham_so"]}["P"]["gia_tri"] == P_N
    hang = {r[0]: r for r in k["so_lieu_mau"]["hang"]}
    for a, s in ROWS: assert abs(hang[a][1] - float(s.replace(",", "."))) < 0.06
    assert hang[15][2] == 1.93 and hang[30][2] == 1.73
    assert "0,5; 1,0; 1,4" in k["cac_buoc"]["quan_sat"][0]
_kiem_so()

# ---------------- bo cuc (khung nguon 1080x1920) ----------------
HX, HY = 90, 900                  # ban le van
LB = 760
S0, BW, BH = 170, 130, 100
ROPE, BODY = 70, 380
HOOK_H = BH / 2
FMAX = 5.0
LF = 270                          # px cho 2,0 N (vecto dung ti le, canh vecto bo luc ke cho rong)
WOOD = (176, 124, 74); WOOD_D = (140, 96, 54); SKIN = (240, 196, 160)
DRED = (185, 28, 28); DGREEN = (10, 110, 50); DTEAL = (15, 118, 110); DPURPLE = (91, 33, 182)

def frame_of(a):
    r = math.radians(a); c, s = math.cos(r), math.sin(r)
    u = (c, -s); n = (-s, -c)
    def Q(sx, h=0.0): return (HX + u[0] * sx + n[0] * h, HY + u[1] * sx + n[1] * h)
    return u, n, Q

def dashed(d, p, q, color, w=4, seg=14, gap=10):
    L = math.dist(p, q); k = 0
    while k * (seg + gap) < L:
        a = k * (seg + gap) / L; b = min(1, (k * (seg + gap) + seg) / L)
        d.line([(lerp(p[0], q[0], a), lerp(p[1], q[1], a)), (lerp(p[0], q[0], b), lerp(p[1], q[1], b))], fill=color, width=w)
        k += 1

def board(d, a, label=True, rough=False, leg=0.86, lab_txt=None):
    u, n, Q = frame_of(a)
    d.line([(40, HY), (1040, HY)], fill=INK, width=5)
    for x in range(60, 1040, 40): d.line([(x, HY + 4), (x - 18, HY + 24)], fill=GRAY, width=3)
    th = 18
    top0, top1 = Q(0), Q(LB); bot1, bot0 = Q(LB, -th), Q(0, -th)
    px = Q(LB * leg, -th)
    d.rectangle([px[0] - 9, px[1], px[0] + 9, HY], fill=WOOD_D)
    d.polygon([top0, top1, bot1, bot0], fill=WOOD)
    d.line([top0, top1], fill=WOOD_D, width=5)
    if rough:                                                    # van nham: rang cua tren mat
        for k in range(10, LB - 10, 26):
            d.polygon([Q(k), Q(k + 13, 12), Q(k + 26)], fill=WOOD_D)
    dot(d, HX, HY, 10, NAVY)
    if a >= 5:
        r = 170
        d.arc([HX - r, HY - r, HX + r, HY + r], -a, 0, fill=ORANGE, width=6)
        if label:
            if lab_txt: mtext(d, (HX + 300, HY + 62), lab_txt, 60, ORANGE)        # duoi mat dat, khong vecto nao di qua
            else:
                m = math.radians(a / 2); rr = 260
                text(d, (HX + rr * math.cos(m) + 40, HY + 64 if a < 20 else HY - rr * math.sin(m)), f"{a:.0f}°", 58, ORANGE)   # 15 do: duoi duong dat (kiem-v2)

def block(d, a):
    u, n, Q = frame_of(a)
    pts = [Q(S0), Q(S0 + BW), Q(S0 + BW, BH), Q(S0, BH)]
    d.polygon(pts, fill=(90, 98, 120)); d.line(pts + [pts[0]], fill=NAVY, width=4)
    dot(d, *Q(S0 + BW, HOOK_H), 7, NAVY)

def meter(d, a, f_read):
    """Day + luc ke engine.luc_ke() doc theo van + tay giu. f_read None: che thang do bang '?'."""
    u, n, Q = frame_of(a)
    Qm = lambda s, h=0.0: Q(s, HOOK_H + h)
    hk = S0 + BW + ROPE
    d.line([Qm(S0 + BW), Qm(hk - 13)], fill=NAVY, width=5)
    se = luc_ke(d, Qm, hk, hk + 20, hk + 20 + BODY, FMAX, f_read, nho=0.2, so=(0, 2, 4), hw=42, ben=1, co=56)
    d.line([Qm(se - 16), Qm(se + 12)], fill=NAVY, width=8)
    hx, hy = Qm(se + 40)
    dot(d, hx, hy, 30, SKIN, outline=(190, 140, 105))

def rig(d, a, f_read, label=True, rough=False):
    board(d, a, label, rough); block(d, a); meter(d, a, f_read)

def rig_vec(d, a=30):
    """Canh vecto: chi van + vat + doan day (bo luc ke de vecto to, khong lan chu N don vi voi luc phap tuyen)."""
    board(d, a, True, leg=0.98, lab_txt="α = 30°"); block(d, a)
    u, n, Q = frame_of(a); h = HOOK_H
    d.line([Q(S0 + BW, h), Q(S0 + BW + 150, h)], fill=NAVY, width=5)     # doan day toi luc ke (luc ke o canh Tien hanh)

def bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (190, y, 890, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (190, y, 190 + max(70, 700 * q), y + 70), fill=A(col, a), r=35)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    k = clamp((t - 0.6) / 2.6)                                   # van nang 15 -> 45 roi ve 15 (luc ke che "?")
    a = 15 + 30 * math.sin(math.pi * k)
    rig(d, a, None, label=True)
    kp = appear(t, M[1] - 0.2, 0.5)
    if kp <= 0: return
    y0 = 1000 + (1 - kp) * 30
    card(d, (50, y0, 1030, y0 + 590), fill=A(WHITE, kp), outline=A(PURPLE, kp), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 98), fill=A(PURPLE, kp), r=36)
    text(d, (W / 2, y0 + 60), "DỰ ĐOÁN", 56, WHITE, alpha=kp)
    text(d, (W / 2, y0 + 175), "Nâng ván từ 15° lên 45°:", 62, INK, alpha=kp)
    text(d, (W / 2, y0 + 260), "số chỉ lực kế thế nào", 62, INK, alpha=kp)
    text(d, (W / 2, y0 + 345), "so với P = 2,0 N?", 62, DPURPLE, alpha=kp)
    bar(d, y0 + 455, t, M[1] + 0.4, sc["T"] - 0.2, PURPLE, kp)

# ---------------- canh 2: Tien hanh (nang van trong MOT canh) ----------------
MOVE = 1.0
def ang_at(t, sc):
    M = sc["M"]
    if t < M[1]: return 15.0
    if t < M[2]: return lerp(15, 30, ease((t - M[1]) / MOVE))
    return lerp(30, 45, ease((t - M[2]) / MOVE))

def table(d, n, y=1000, hl=-1):
    card(d, (40, y, 1040, y + 580), fill=WHITE, outline=NAVY, w=4)
    text(d, (W / 2, y + 62), "Quả nặng P = 2,0 N", 58, NAVY)
    xs = (330, 750)
    mtext(d, (xs[0], y + 160), "góc α", 58, INK)
    text(d, (xs[1], y + 160), "lực kế (N)", 58, INK)
    d.line([(70, y + 212), (1010, y + 212)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 285 + i * 98
        if i == hl: d.rounded_rectangle([60, yy - 42, 1020, yy + 42], radius=16, fill=(255, 237, 213))
        text(d, (xs[0], yy), f"{ROWS[i][0]}°", 62, INK)
        text(d, (xs[1], yy), ROWS[i][1], 62, BLUE)

def s_do(img, d, t, sc):
    M = sc["M"]; a = ang_at(t, sc); cur = max(0, cur_cap(sc, t))
    moving = any(M[i] <= t < M[i] + MOVE for i in (1, 2))
    if moving: rig(d, a, P_N * math.sin(math.radians(a)), label=False)
    else: rig(d, a, float(ROWS[cur][1].replace(",", ".")))
    n = sum(t >= M[i] + 1.4 for i in range(3))
    table(d, n, hl=n - 1)

# ---------------- canh 3: Dap an + phan tich P (vecto dung ti le) ----------------
S0_VEC = 400
def harrow(d, p1, p2, color, alpha, w=9):
    arrow(d, p1, p2, A(WHITE, alpha), w=w + 7, head=28); arrow(d, p1, p2, A(color, alpha), w=w, head=26)

def sublab(d, x, y, main, sub, color, alpha=1.0):
    fm, fs = F(62), F(56); w = tw(d, main, fm) + tw(d, sub, fs); x0 = x - w / 2
    dtext(d, (x0, y), main, fm, color, alpha, "lm"); dtext(d, (x0 + tw(d, main, fm), y + 18), sub, fs, color, alpha, "lm")

def vecs(img, d, alpha, comp_alpha, a=30, px_col=None, grow=1.0, show=("P", "Q", "F", "Px", "Py"), py_col=None):
    """P (2,0 N = LF px), Px = P sin a xuong doc, Py = P cos a vao van, N = Py ra khoi van, F luc ke = Px len doc.
       Phan nam duoi mat van mo con 55%."""
    u, n, Q = frame_of(a); r = math.radians(a)
    c = Q(S0 + BW / 2, BH / 2)
    lx, ly = LF * math.sin(r) * grow, LF * math.cos(r) * grow
    pe = (c[0], c[1] + LF)
    ex = (c[0] - u[0] * lx, c[1] - u[1] * lx)
    ey = (c[0] - n[0] * ly, c[1] - n[1] * ly)
    en = (c[0] + n[0] * LF * math.cos(r), c[1] + n[1] * LF * math.cos(r))
    f0 = Q(S0 + BW, BH - 2); f1 = (f0[0] + u[0] * LF * math.sin(r), f0[1] + u[1] * LF * math.sin(r))
    L = Image.new("RGBA", img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    if comp_alpha > 0:
        if grow > 0.98 and "Px" in show and "Py" in show:
            dashed(dl, ex, pe, A(MUTED, comp_alpha), w=4); dashed(dl, ey, pe, A(MUTED, comp_alpha), w=4)
        if "Px" in show: harrow(dl, c, ex, px_col or PURPLE, comp_alpha, w=9)
        if "Py" in show: harrow(dl, c, ey, py_col or TEAL, comp_alpha, w=9)
    if alpha > 0:
        harrow(dl, c, pe, BLUE, alpha)
        if "Q" in show: harrow(dl, c, en, GREEN, alpha, w=9)
        if "F" in show: harrow(dl, f0, f1, RED, alpha, w=9)
    arr = np.array(L); ys, xs = np.mgrid[0:arr.shape[0], 0:arr.shape[1]]
    below = ys > HY - (xs - HX) * math.tan(r) + 2
    arr[..., 3] = np.where(below, (arr[..., 3] * 0.55).astype(np.uint8), arr[..., 3])
    L = Image.fromarray(arr, "RGBA"); img.paste(L, (0, 0), L)
    dot(d, c[0], c[1], 10, NAVY, outline=WHITE)
    if comp_alpha > 0.6 and grow > 0.98:
        if "Px" in show: sublab(d, ex[0] - 68, ex[1] - 68, "P", "x", px_col or PURPLE, comp_alpha)
        if "Py" in show: sublab(d, ey[0] + 75, ey[1] + 5, "P", "y", py_col or DTEAL, comp_alpha)
    if alpha > 0.6:
        text(d, (pe[0] - 50, pe[1] - 22), "P", 62, BLUE)
        if "Q" in show: text(d, (en[0] - 46, en[1] - 30), "Q", 62, DGREEN)
        if "F" in show: text(d, (f1[0] + 10, f1[1] - 52), "F", 62, RED)
    return c

def s_dapan(img, d, t, sc):
    global S0; S0 = S0_VEC
    M = sc["M"]
    rig_vec(d)
    ka = appear(t, 0.0, 0.3)
    card(d, (40, 1010, 1040, 1190), fill=A((236, 253, 243), ka), outline=A(GREEN, ka), w=5)
    text(d, (W / 2, 1100), "0,5 → 1,0 → 1,4 N  <  P = 2,0 N", 60, DGREEN, alpha=ka)
    vecs(img, d, appear(t, 1.0, 0.5), appear(t, M[1] - 0.1, 0.5), show=("P", "F", "Px", "Py"), grow=ease((t - M[1] + 0.1) / 1.0))
    k2 = appear(t, M[1] + 1.0, 0.5)
    if k2 > 0:
        card(d, (40, 1240, 1040, 1420), fill=A(WHITE, k2), outline=A(RED, k2), w=5)
        mtext(d, (W / 2, 1330), "lực kế F = P·sin α", 62, RED, alpha=k2)
    S0 = 170

# ---------------- canh 4: Bay (P cos alpha) ----------------
def s_bay(img, d, t, sc):
    global S0; S0 = S0_VEC
    M = sc["M"]
    rig_vec(d)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 < 0.5: c = vecs(img, d, 1.0, 1.0, show=("P", "Py"), py_col=DRED)             # nhip 1: P.cos 30 la Py
    else: c = vecs(img, d, 1.0, 1.0, show=("P", "Px", "Py"))                             # nhip 2: Px doi dien goc alpha
    if k2 > 0:                                                    # goc alpha giua P (thang xuong) va Py (vao van)
        rr = 130
        d.arc([c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr], 60, 90, fill=A(ORANGE, k2), width=8)
        m = math.radians(76)
        dtext(d, (c[0] + 190 * math.cos(m), c[1] + 190 * math.sin(m)), "α", FG(74), ORANGE, k2)
    y0 = 1010
    k1 = 1 - k2
    if k1 > 0:
        card(d, (40, y0, 1040, y0 + 400), fill=A((254, 242, 242), k1), outline=A(DRED, k1), w=6)
        mtext(d, (W / 2, y0 + 85), "✗ lực kế = P·cos 30°", 62, DRED, alpha=k1)
        w1 = tw(d, "= P", F(62)) + tw(d, "y", F(56)); w2 = tw(d, " ≈ 1,7 N", F(62)); x0 = W / 2 - (w1 + w2) / 2
        sublab(d, x0 + w1 / 2, y0 + 190, "= P", "y", DRED, k1)
        text(d, (x0 + w1, y0 + 190), " ≈ 1,7 N", 62, DRED, anchor="lm", alpha=k1)
        text(d, (W / 2, y0 + 305), "lực kế đo: 1,0 N", 64, INK, alpha=k1)
    if k2 > 0:
        card(d, (40, y0, 1040, y0 + 400), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=6)
        mtext(d, (W / 2, y0 + 130), "✓ dọc ván: cạnh đối góc α", 62, DGREEN, alpha=k2)
        mtext(d, (W / 2, y0 + 270), "→ dùng sin", 64, DGREEN, alpha=k2)
    S0 = 170

# ---------------- canh 5: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    rig(d, 30, None, label=False, rough=True)
    k = appear(t, 0.0, 0.3)
    card(d, (40, 990, 1040, 1400), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, 1080), "Chưa nói được", 62, NAVY, alpha=k)
    kk = appear(t, 2.6, 0.5)
    card(d, (90, 1160, 990, 1340), fill=A((254, 242, 242), kk), outline=A(DRED, kk), r=24, w=4)
    text(d, (W / 2, 1250), "Ván nhám thì sao?", 64, DRED, alpha=kk)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    global S0; S0 = S0_VEC
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1590), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 238, W / 2 + pw / 2, 314), fill=A(ORANGE, k1), r=36)
    text(d, (W / 2, 276), "THỬ NGHĨ", 56, WHITE, alpha=k1)
    a = 15; board(d, a, label=False, leg=0.98); block(d, a)
    mtext(d, (HX + 300, HY + 62), "nghiêng 15°", 60, ORANGE, alpha=k1)
    u, n, Q = frame_of(a); c = Q(S0 + BW / 2, BH / 2)
    c = Q(S0 + BW * 0.25, BH / 2)                                 # P o nua trai, luc ep o mep phai: hai mui ten khong chong
    harrow(d, c, (c[0], c[1] + 170), BLUE, k1)
    text(d, (c[0] - 48, c[1] + 140), "P", 62, BLUE, alpha=k1)
    sp = Q(S0 + BW * 0.95, 0)                                     # luc ep: tai mat tiep xuc, vuong goc vao van (do dai an dap so)
    ep = (sp[0] - n[0] * 130, sp[1] - n[1] * 130)
    harrow(d, sp, ep, DTEAL, k1, w=8)
    text(d, (ep[0] + 60, ep[1] - 70), "?", 72, DTEAL, alpha=k1)
    text(d, (W / 2, 420), "P = 2,0 N", 62, BLUE, alpha=k1)
    text(d, (W / 2, 1150), "Lực ép lên ván bao nhiêu?", 64, DTEAL, alpha=appear(t, 2.3, 0.45))
    bar(d, 1330, t, 0.8, sc["T"] - 0.2, ORANGE, k1)
    S0 = 170

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
            (do["t0"] + M[1], "tap"), (do["t0"] + M[2], "tap"),
            (da["t0"] + 0.1, "ding"), (b["t0"] + 0.15, "buzz"), (b["t0"] + b["M"][1], "tap"),
            (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l10-tonghopluc-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Tổng hợp và phân tích lực · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Quả nặng trên ván nghiêng", draw=s_hook, tail=0.3, caps=[
   ("Lực kế giữ vật yên trên ván.", 3.8),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Ván 15°: đọc lực kế.", 3.0),
   ("Nâng ván lên 30°.", 3.4),
   ("Nâng tiếp tới 45°.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Đáp án: tăng, vẫn nhỏ hơn P.", 3.6),
   ("Tách P thành hai phần.", 4.2)]),
 dict(key="bay", title="Bẫy: dùng cos", draw=s_bay, tail=0.4, caps=[
   ("Dễ nhầm lấy P nhân cos.", 3.6),
   ("Nhìn góc α nằm ở đâu.", 3.4)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.6, caps=[
   ("Ở đây coi ván trơn.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Lực kế chỉ đỡ phần dọc ván.", 5.4)]),
])
