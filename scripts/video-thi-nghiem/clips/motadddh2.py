# Clip: tn-l11-motadddh-02 - Nam lan doc li do tren do thi x-t (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-motadddh-02.json:
#   tham_so: A = 5 cm, T = 1 s, phi = 0 ; thuoc chia 1 mm, doc lam tron 0,1 cm (sai_so_do 0,1).
#   so_lieu_mau (t s, x tinh cm, x doc cm): 0 5,000 5,0 ; 0,10 4,045 4,0 ; 0,20 1,545 1,5 ; 0,30 -1,545 -1,5 ;
#     0,40 -4,045 -4,0.  x = 5.cos(2.pi.t) cm. |4,045 - 4,0| = 0,045 cm.
#   Muc giam moi 0,10 s (tru truc tiep cot x doc): 1,0 ; 2,5 ; 3,0 ; 2,5 cm.
#   Bay = hien_tuong_hay_sai[0]: lay so doc thuoc (4,0 cm o t = 0,10 s) lam bien do.
#   Cau hoi trong bai (sau hop) hoi sai so o t = 0,10 s -> Du doan KHONG hoi sai so; Du doan hoi li do giam
#   deu hay khong deu moi 0,10 s (dap an: khong deu, it o gan bien, nhieu khi qua VTCB).
#   Cau chot: cung 0,10 s gan bien di it, qua VTCB di nhieu. THU NGHI: t = 0,05 s (chua doc) -> 5cos(0,1.pi) = 4,755
#     -> doc khoang 4,8 cm (nguoc phan xa noi suy thang 4,5 cm).
# Bo cuc (khac cac clip lo xo khac cua lo): ray ngang + THUOC doc truc tiep o tren, DO THI x-t la truc chinh, bang
#   t / x doc nam ngang ben duoi; Rut ra phong to thuoc quanh 4,0 cm.
# Chuyen dong: x = 5cos(2.pi.tp), tp = thoi gian that; quay cham x10 (0,10 s that = 1,0 s video), dung hinh o moi
#   moc 0,10 s de doc. Vat, kim thuoc, vet do thi, cham, o bang, dong ho doi CUNG luc (kiem: _kiem_dong_bo()).
from engine import *

ROWS = [(0.0, 5.000, 5.0), (0.1, 4.045, 4.0), (0.2, 1.545, 1.5), (0.3, -1.545, -1.5), (0.4, -4.045, -4.0)]
AMP, PER = 5.0, 1.0
def xof(tp): return AMP * math.cos(2 * math.pi * tp / PER)
def vn(v, nd=1):
    s = f"{abs(v):.{nd}f}".replace(".", ",")
    return ("−" if v < -1e-9 else "") + s
def vt(tp): return "0" if tp == 0 else vn(tp, 2)
DGREEN = (21, 110, 55); HL = (255, 237, 213); DRED = (185, 28, 28); BLOCK = (59, 130, 246)

# ---------------- ray ngang + thuoc (khung nguon 1080x1920) ----------------
RX0, RS = 600, 70            # x = 0 (VTCB) o px 600 ; 70 px/cm
TRACK = 425
def rx(x): return RX0 + x * RS

def spring(d, x0, x1, y, n=11, amp=20, col=NAVY):
    pts = [(x0, y), (x0 + 16, y)]
    L = (x1 - 16) - (x0 + 16)
    for i in range(1, 2 * n):
        pts.append((x0 + 16 + L * i / (2 * n), y + (amp if i % 2 else -amp)))
    pts += [(x1 - 16, y), (x1, y)]
    d.line(pts, fill=col, width=4, joint="curve")

def rig(d, x, reading=None, ka=1.0):
    """Ray + lo xo + vat o li do x (cm) + thuoc -5..5 cm vach mm; reading = so doc ghi ben duoi thuoc."""
    d.rectangle([40, 300, 62, TRACK + 4], fill=GRAY, outline=NAVY, width=3)                  # tuong
    d.line([(40, TRACK + 4), (1040, TRACK + 4)], fill=NAVY, width=5)                        # ray
    cx = rx(x)
    spring(d, 62, cx - 40, 378)
    card(d, (cx - 40, 335, cx + 40, TRACK), fill=BLOCK, outline=NAVY, r=10, w=3)
    d.rectangle([rx(-5) - 14, 440, rx(5) + 14, 478], fill=(250, 240, 200), outline=NAVY, width=2)  # thuoc
    for k in range(-50, 51):
        X = rx(k / 10); L = 24 if k % 10 == 0 else (15 if k % 5 == 0 else 8)
        d.line([(X, 440), (X, 440 + L)], fill=NAVY, width=2 if L < 24 else 3)
    for c in range(-5, 6):
        text(d, (rx(c), 508), vn(c, 0), 38, MUTED, bold=False)
    text(d, (rx(5) + 36, 508), "cm", 38, MUTED, bold=False, anchor="lm")
    d.line([(cx, 360), (cx, 476)], fill=RED, width=4)                                       # kim chi tren vat
    if reading is not None:
        lab = f"đọc: {reading} cm"; pw = tw(d, lab, F(40)) + 40
        bx = 50
        card(d, (bx, 540, bx + pw, 604), fill=A(HL, ka), outline=A(ORANGE, ka), r=24, w=3)
        text(d, (bx + pw / 2, 572), lab, 40, ORANGE, alpha=ka)

# ---------------- do thi x-t ----------------
GX0, GSX, GSC = 200, 1800, 50          # t = 0 o px 200 ; 0,10 s = 180 px ; 50 px/cm
def gx(tp): return GX0 + tp * GSX
def gyf(gy): return lambda x: gy - x * GSC

def graph(d, gy, tp_end=None, ndots=0, ka=1.0, qmarks=False, hl=None):
    """Truc t 0..0,45 s, truc x -5..5 cm; vet x = 5cos(2.pi.t) tu 0 toi tp_end; ndots cham doc (cot x doc)."""
    Y = gyf(gy); top, bot = Y(5) - 50, Y(-5) + 30
    for k in range(1, 5):                                  # luoi doc o moc 0,10 s
        for yy in range(int(top + 30), int(bot), 26): d.line([(gx(k / 10), yy), (gx(k / 10), yy + 12)], fill=LIGHT, width=3)
    for xv in (5, -5):
        for xx in range(GX0, int(gx(0.42)), 26): d.line([(xx, Y(xv)), (xx + 12, Y(xv))], fill=LIGHT, width=3)
    arrow(d, (GX0, bot), (GX0, top), NAVY, w=4, head=18)
    arrow(d, (GX0, Y(0)), (gx(0.43), Y(0)), NAVY, w=4, head=18)
    text(d, (GX0 + 18, top - 4), "x (cm)", 38, INK, anchor="lm")
    text(d, (gx(0.43) - 8, Y(0) + 40), "t (s)", 38, INK, anchor="rm")
    for xv in (5, 0, -5):
        text(d, (GX0 - 18, Y(xv)), vn(xv, 0), 38, MUTED, bold=False, anchor="rm")
    for k in range(1, 5):
        text(d, (gx(k / 10), bot + 34), vn(k / 10, 2), 38, MUTED, bold=False)
    if qmarks:
        for k in range(1, 5): text(d, (gx(k / 10), top + 6), "?", 44, PURPLE)
    if tp_end is not None and tp_end > 0:
        n = max(2, int(tp_end * 400))
        pts = [(gx(tp_end * i / n), Y(xof(tp_end * i / n))) for i in range(n + 1)]
        d.line(pts, fill=A(TEAL, ka), width=6, joint="curve")
    for i in range(ndots):
        tp, _, xd = ROWS[i]
        c = ORANGE if hl == i else NAVY
        dot(d, gx(tp), Y(xd), 13, A(c, ka), outline=WHITE)

# ---------------- bang t / x doc nam ngang ----------------
def table_row(d, y0, n, cur=None, qm=False):
    """Hai hang: t (s) va x doc (cm); 5 cot; n cot da co so; cur = cot dang doc (to nen)."""
    card(d, (40, y0, 1040, y0 + 190), fill=WHITE, outline=NAVY, r=20, w=3)
    d.line([(40, y0 + 95), (1040, y0 + 95)], fill=LIGHT, width=3)
    d.line([(270, y0 + 10), (270, y0 + 180)], fill=LIGHT, width=3)
    text(d, (155, y0 + 48), "t (s)", 38, INK)
    text(d, (155, y0 + 142), "x đọc (cm)", 38, INK)
    for i in range(5):
        cx = 270 + 77 + i * 154
        if cur == i: card(d, (cx - 72, y0 + 8, cx + 72, y0 + 182), fill=HL, r=14)
        text(d, (cx, y0 + 48), vt(ROWS[i][0]), 40, INK)
        if i < n: text(d, (cx, y0 + 142), vn(ROWS[i][2]), 42, ORANGE if cur == i else NAVY)
        elif qm: text(d, (cx, y0 + 142), "?", 42, PURPLE)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, 5.0)
    k = appear(t, 0.6, 0.4)
    if k > 0:                                               # tay tha o bien duong
        arrow(d, (rx(5) + 10, 290), (rx(5) - 70, 290), A(ORANGE, k), w=5, head=18)
        text(d, (rx(5) - 90, 290), "thả", 40, ORANGE, anchor="rm", alpha=k)
    graph(d, 940, ndots=1, qmarks=t > 1.0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1292 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 390), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 86), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 55), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 200, "Cứ mỗi 0,10 s, li độ giảm\nmột lượng như nhau không?", 50, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 336, 940, y0 + 348], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 336, 140 + 800 * (1 - p), y0 + 348], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (quay cham x10, dung o moi moc 0,10 s) ----------------
D0, HOLD, MOVE = 0.4, 0.8, 1.0     # moc doc dau o D0; moi moc dung HOLD; giua hai moc chay MOVE (0,10 s that)
def phase(t):
    """-> (tp, i_doc): tp thoi gian that; i_doc = chi so moc dang dung doc (None neu dang chay / chua bat dau)."""
    if t < D0: return 0.0, None
    u = t - D0
    for i in range(5):
        if u < HOLD: return ROWS[i][0], i
        u -= HOLD
        if i == 4: return ROWS[4][0], 4
        if u < MOVE: return ROWS[i][0] + 0.1 * u / MOVE, None
        u -= MOVE
    return ROWS[4][0], 4
def n_read(t):
    """So moc da doc xong (cot bang / cham) tai t."""
    if t < D0: return 0
    return min(5, 1 + int((t - D0) // (HOLD + MOVE)))

def s_do(img, d, t, sc):
    tp, i = phase(t); n = n_read(t)
    rig(d, xof(tp), reading=vn(ROWS[i][2]) if i is not None else None)
    if i is not None:
        lab = f"t = {vt(ROWS[i][0])} s"
        card(d, (640, 540, 1030, 604), fill=NAVY, r=24); text(d, (835, 572), lab, 40, WHITE)
    elif t >= D0:
        card(d, (640, 540, 1030, 604), fill=ORANGE, r=24); text(d, (835, 572), "▶ quay chậm ×10", 38, WHITE)
    graph(d, 940, tp_end=tp, ndots=n, hl=i)
    table_row(d, 1300, n, cur=i)

# ---------------- canh 3: Dap an (giam khong deu) ----------------
GYA = 700
def s_dapan(img, d, t, sc):
    M = sc["M"]; ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · giảm không đều"
    pw = tw(d, lab, F(42)) + 56
    card(d, (W / 2 - pw / 2, 268, W / 2 + pw / 2, 332), fill=A(NAVY, ka), r=32)
    text(d, (W / 2, 300), lab, 42, WHITE, alpha=ka)
    graph(d, GYA, tp_end=0.4, ndots=5)
    Y = gyf(GYA)
    for j in range(1, 5):                                   # bac thang: ngang tu cham j-1, doc xuong cham j
        kj = appear(t, 0.5 + 0.35 * (j - 1), 0.35)
        if kj <= 0: continue
        (t0, _, a0), (t1, _, a1) = ROWS[j - 1], ROWS[j]
        for xx in range(int(gx(t0)) + 16, int(gx(t1)), 24): d.line([(xx, Y(a0)), (xx + 12, Y(a0))], fill=A(ORANGE, kj), width=4)
        d.line([(gx(t1), Y(a0)), (gx(t1), Y(a1) - 14)], fill=A(ORANGE, kj), width=7)
        ly = {1: Y(a0) - 26, 3: Y(0) + 42}.get(j, (Y(a0) + Y(a1)) / 2)
        text(d, (gx(t1) + 14, ly), vn(a0 - a1), 40, ORANGE, anchor="lm", alpha=kj)
    text(d, (W / 2, 1060), "bậc cam = hiệu hai số đọc", 38, ORANGE, alpha=appear(t, 0.5, 0.35))
    kb = appear(t, M[0] + 0.3, 0.4)                          # vat cham o bien, nhanh qua VTCB: hai the
    if kb > 0:
        card(d, (40, 1120, 1040, 1250), fill=A(WHITE, kb), outline=A(TEAL, kb), r=24, w=4)
        text(d, (90, 1185), "Gần biên: giảm 1,0 cm → chậm", 44, INK, anchor="lm", alpha=kb)
    kc = appear(t, M[1] + 0.3, 0.4)
    if kc > 0:
        card(d, (40, 1290, 1040, 1420), fill=A(WHITE, kc), outline=A(TEAL, kc), r=24, w=4)
        text(d, (90, 1355), "Qua VTCB: giảm 3,0 cm → nhanh", 44, INK, anchor="lm", alpha=kc)

# ---------------- canh 4: Rut ra (phong to thuoc) + Chua noi duoc ----------------
ZX0, ZS = 140, 2000                 # 3,85 cm o px 140 ; 1 cm = 2000 px (1 mm = 200 px)
def zx(x): return ZX0 + (x - 3.85) * ZS
def s_rutra(img, d, t, sc):
    M = sc["M"]
    text(d, (60, 270), "Phóng to thước lúc t = 0,10 s", 40, INK, anchor="lm")
    d.rectangle([60, 400, 1020, 480], fill=(250, 240, 200), outline=NAVY, width=3)
    for k in range(39, 43):                                 # vach mm 3,9 .. 4,2
        X = zx(k / 10); L = 60 if k == 40 else 34
        d.line([(X, 400), (X, 400 + L)], fill=NAVY, width=5 if k == 40 else 3)
    text(d, (zx(4.0), 520), "4,0", 44, NAVY)
    kp = appear(t, 0.3, 0.4)
    if kp > 0:
        X = zx(4.045)
        d.line([(X, 350), (X, 470)], fill=A(RED, kp), width=6)
        text(d, (X + 16, 340), "tính: 4,045", 42, RED, anchor="lm", alpha=kp)
        kr = appear(t, 1.0, 0.4)
        if kr > 0:
            arrow(d, (X - 10, 450), (zx(4.0) + 12, 450), A(ORANGE, kr), w=5, head=16)
            text(d, (zx(4.0) - 20, 590), "đọc: 4,0  → lệch 0,045 cm", 42, ORANGE, anchor="lm", alpha=kr)
    # bang ba hang: t, x tinh, x doc
    y0 = 660; kt = appear(t, M[0] + 0.6, 0.4)
    card(d, (40, y0, 1040, y0 + 300), fill=WHITE, outline=NAVY, r=20, w=3)
    for r_ in (1, 2): d.line([(40, y0 + r_ * 100), (1040, y0 + r_ * 100)], fill=LIGHT, width=3)
    d.line([(250, y0 + 10), (250, y0 + 290)], fill=LIGHT, width=3)
    for r_, lab in enumerate(("t (s)", "x tính", "x đọc")): text(d, (145, y0 + 50 + r_ * 100), lab, 38, INK)
    for i, (tp, xt, xd) in enumerate(ROWS):
        cx = 250 + 79 + i * 158
        text(d, (cx, y0 + 50), vt(tp), 40, INK)
        text(d, (cx, y0 + 150), vn(xt, 3), 38, RED)
        text(d, (cx, y0 + 250), vn(xd), 40, NAVY)
    if kt > 0:                                              # bon cot le: o cam
        for i in range(1, 5):
            cx = 250 + 79 + i * 158
            d.rounded_rectangle([cx - 76, y0 + 106, cx + 76, y0 + 294], radius=12, outline=A(ORANGE, kt), width=4)
    k2 = appear(t, M[0] + 2.0, 0.45)
    if k2 > 0:
        yb = 1030 + (1 - k2) * 30
        card(d, (40, yb, 1040, yb + 470), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, yb + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Sai số bấm giờ, đặt mắt", "• Mới đọc từ 0 tới 0,40 s")):
            kk = k2 * appear(t, M[0] + 2.4 + 0.5 * j, 0.4)
            text(d, (90, yb + 200 + j * 130), l1, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Bay (lay so doc lam bien do) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    graph(d, GYA, tp_end=0.4, ndots=5, hl=1)
    Y = gyf(GYA)
    text(d, (gx(0.1) - 22, Y(4.0) + 34), "4,0", 40, ORANGE, anchor="rm")
    kd = appear(t, M[1] - 0.1, 0.4)                         # do cao dinh: hien cung dau ✓
    if kd > 0:
        d.line([(gx(0) + 16, Y(5)), (gx(0.06), Y(5))], fill=A(GREEN, kd), width=6)
        arrow(d, (gx(0) - 60, Y(0)), (gx(0) - 60, Y(5) + 4), A(GREEN, kd), w=6, head=18)
        arrow(d, (gx(0) - 60, Y(5)), (gx(0) - 60, Y(0) - 4), A(GREEN, kd), w=6, head=18)
        text(d, (gx(0) - 78, (Y(0) + Y(5)) / 2), "A", 44, GREEN, anchor="rm", alpha=kd)
    a1 = appear(t, 0.0, 0.3)
    y0 = 1060
    card(d, (40, y0, 1040, y0 + 470), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
    text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
    q = "“Biên độ A = 4,0 cm”"
    ks = clamp((t - 1.4) / 0.4); f = F(50); lw = tw(d, q, f); yy = y0 + 200
    text(d, (W / 2, yy), q, 50, DRED, alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=(140, 15, 15), width=7)
    ctext(d, y0 + 360, "✓ A = 5,0 cm: li độ lớn nhất", 48, DGREEN, maxw=920, alpha=kd)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def _end_body(sc):
    M = sc["M"]
    def body(d, t, k1):
        kq = appear(t, M[0] + 0.4, 0.5)
        for j, (lab, val) in enumerate((("t (s)", "0,05"), ("x đọc (cm)", "?"))):
            x0 = 180 + j * 450
            card(d, (x0, 1010, x0 + 270, 1180), fill=A((245, 243, 255), kq), outline=A(PURPLE, kq), r=18, w=3)
            text(d, (x0 + 135, 1055), lab, 38, MUTED, bold=False, alpha=kq)
            text(d, (x0 + 135, 1125), val, 48, PURPLE if val == "?" else INK, alpha=kq)
        kh = appear(t, M[0] + 0.4 + 2.5, 0.5)                 # goi y tre 2,5 s sau cau hoi
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1360, "Gợi ý", 38, MUTED, bold=False, alpha=kh)
        ctext(d, 1445, "A = 5,0 cm, T = 1,00 s; thả từ biên", 42, ORANGE, maxw=820, alpha=kh)
    return body

def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Cùng 0,10 s: gần biên đi ít,\nqua VTCB đi nhiều",
             "Ở t = 0,05 s (chưa đọc),\nthước chỉ khoảng bao nhiêu?", body=_end_body(sc))

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, ru, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (do["t0"] + 0.1, "ding")]
    out += [(do["t0"] + D0 + i * (HOLD + MOVE), "tap") for i in range(1, 5)]
    out += [(da["t0"] + 0.1, "ding"), (ru["t0"] + 1.0, "tap"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-motadddh-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Mô tả dao động · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Đọc li độ trên thước", draw=s_hook, tail=0.6, caps=[
   ("A = 5,0 cm, T = 1,00 s.", 2.8),
   ("Tự đoán trước khi xem tiếp.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Dừng hình ở mỗi mốc 0,10 s để đọc.", 3.8),
   ("Mỗi số đọc là một chấm (t; x).", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=1.4, caps=[
   ("Chấm nằm trên đường côsin.", 3.0),
   ("Cùng 0,10 s, quãng đi khác nhau.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Thước chỉ chia tới 0,1 cm.", 3.4),
   ("Mới là sai số làm tròn.", 3.6)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Bẫy: số đọc thành biên độ.", 3.0),
   ("Số đọc chỉ là li độ.", 2.9)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 5.6)]),
])
