# Clip: tn-l12-mayphatdien-03 - Tu quan may bien ap: do dien ap thu cap theo so vong day
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-mayphatdien-03.json (so_lieu_mau, tham_so).
# Ban 1 (28/10/2026): mau boyle/phongxa2 (dung cu + bang + do thi), tieng bao cues.
# Lua chon trong hop Du doan (N2 = 400 vong) suy thang tu U1 = 12 V, N1 = 200 vong (tham_so):
#   A. 6 V  = U1.N1/N2 (lay nguoc ti so, nham voi I)   B. 12 V = U1 (nghi so vong khong quan trong, hien_tuong_hay_sai #2)
#   C. 24 V = U1.N2/N1 (dung; so do 23,5 V)             D. 48 V = U1.(N2/N1)^2 (nham binh phuong)
from engine import *

U1, N1 = 12, 200                                                         # tham_so
ROWS = [(100, "2,00", 5.9, "2,03"), (200, "1,00", 11.6, "1,03"),
        (400, "0,500", 23.5, "0,511"), (600, "0,333", 35.1, "0,342")]  # so_lieu_mau: N2, N1/N2, U2 do, U1/U2
def fmt(v): return f"{v:.1f}".replace(".", ",")

COPPER, COPPER_D = (196, 120, 52), (120, 66, 24)
CORE, CORE_L = (148, 158, 178), (190, 198, 214)

# ---------------- loi sat kin + cuon day ----------------
def core(d, x0, y0, x1, y1, w):
    d.rectangle([x0, y0, x1, y1], fill=CORE, outline=NAVY, width=5)
    d.rectangle([x0 + w, y0 + w, x1 - w, y1 - w], fill=BG, outline=NAVY, width=5)
    for k in (w * 0.25, w * 0.5, w * 0.75):              # cac la thep ghep (lop cach dien)
        d.rectangle([x0 + k, y0 + k, x1 - k, y1 - k], outline=CORE_L, width=2)

def coil(d, cx, yc, n, cw, pitch, flash=None):
    """n vong ve (moi vong ve = 25 vong that). flash(i) -> do sang 0..1 cua vong i (dem suat dien dong)."""
    hh = n * pitch; top = yc - hh / 2
    for i in range(n):
        y = top + i * pitch + pitch / 2
        d.rounded_rectangle([cx - cw / 2, y - pitch * 0.38, cx + cw / 2, y + pitch * 0.38], radius=int(pitch * 0.38),
                            fill=COPPER, outline=COPPER_D, width=2)
        if flash:
            f = flash(i)
            if f > 0: dot(d, cx + cw / 2 - 14, y, pitch * 0.32, A(YELLOW, f))
    return top + pitch / 2, top + hh - pitch / 2      # y dau day tren, duoi

def flux(d, t, x0, y0, x1, y1, col=BLUE, size=16, a=1.0):
    """Chevron chay quanh duong giua loi, doi chieu theo nhip xoay chieu (hinh cham)."""
    s = math.sin(2 * math.pi * 0.45 * t)
    if abs(s) < 0.15: return
    dirn = 1 if s > 0 else -1; al = a * clamp((abs(s) - 0.15) / 0.5)
    per = 2 * ((x1 - x0) + (y1 - y0)); step = per / 14
    off = (t * 70 * dirn) % step
    for k in range(14):
        p = (k * step + off) % per
        if p < x1 - x0: x, y, ang = x0 + p, y0, 0
        elif p < (x1 - x0) + (y1 - y0): x, y, ang = x1, y0 + p - (x1 - x0), 90
        elif p < 2 * (x1 - x0) + (y1 - y0): x, y, ang = x1 - (p - (x1 - x0) - (y1 - y0)), y1, 180
        else: x, y, ang = x0, y1 - (p - 2 * (x1 - x0) - (y1 - y0)), 270
        r = math.radians(ang + (0 if dirn > 0 else 180))
        for sg in (1, -1):
            b = r + math.pi - sg * math.radians(35)
            d.line([(x + size * 0.5 * math.cos(r), y + size * 0.5 * math.sin(r)),
                    (x + size * 0.5 * math.cos(r) + size * math.cos(b), y + size * 0.5 * math.sin(r) + size * math.sin(b))],
                   fill=A(col, al), width=5)

def source(d, x0, y0, x1, y1):
    card(d, (x0, y0, x1, y1), fill=WHITE, outline=NAVY, r=22, w=5)
    cx = (x0 + x1) / 2
    pts = [(cx - 55 + j * 110 / 40, y0 + 62 - 24 * math.sin(2 * math.pi * j / 40)) for j in range(41)]
    d.line(pts, fill=ORANGE, width=6, joint="curve")
    text(d, (cx, y0 + 138), f"{U1} V", 44, BLUE)
    text(d, (cx, y0 - 34), "nguồn ~", 36, INK)

def meter(d, x0, y0, x1, y1, reading, lbl="V~", title="vôn kế", col=(134, 239, 172)):
    card(d, (x0, y0, x1, y1), fill=(255, 236, 160), outline=NAVY, r=22, w=5)
    d.rounded_rectangle([x0 + 18, y0 + 30, x1 - 18, y0 + 130], radius=12, fill=NAVY)
    text(d, ((x0 + x1) / 2, y0 + 80), reading, 52, col)
    text(d, ((x0 + x1) / 2, y0 + 195), lbl, 44, INK)
    if title: text(d, ((x0 + x1) / 2, y0 - 34), title, 36, INK)

def n_draw(N): return int(round(N / 25))

def rig(d, t, n2, reading, power=True, note=None):
    cx1, cx2, yc = 340, 740, 660
    core(d, 300, 400, 780, 920, 80)
    text(d, (540, 360), "lõi sắt kín, ghép lá", 36, NAVY)
    if power: flux(d, t, 340, 440, 740, 880, size=18, a=0.9)
    a1, b1 = coil(d, cx1, yc, n_draw(N1), 140, 14)
    source(d, 60, 560, 230, 760)
    d.line([(270, a1), (250, a1), (250, 610), (230, 610)], fill=NAVY, width=5, joint="curve")
    d.line([(270, b1), (250, b1), (250, 710), (230, 710)], fill=NAVY, width=5, joint="curve")
    if n2 > 0:
        a2, b2 = coil(d, cx2, yc, n2, 140, 14)
        d.line([(810, a2), (832, a2), (832, 600), (850, 600)], fill=NAVY, width=5, joint="curve")
        d.line([(810, b2), (832, b2), (832, 720), (850, 720)], fill=NAVY, width=5, joint="curve")
    meter(d, 850, 520, 1040, 800, reading)
    text(d, (cx1, 968), f"N₁ = {N1} vòng", 40, INK)
    text(d, (cx2, 968), "N₂ = " + (f"{n2 * 25} vòng" if n2 > 0 else "?"), 40, BLUE)
    if note: note(d)

# ---------------- canh 1: mo bai + du doan ----------------
OPTS = ("A. 6 V", "B. 12 V", "C. 24 V", "D. 48 V")
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    rig(d, t, n_draw(400), "?")
    k = appear(t, sc["M"][1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (60, 1020, 1020, 1630), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 1075), "Dự đoán", 46, PURPLE, alpha=k)
    ctext(d, 1170, "Thứ cấp 400 vòng.\nVôn kế chỉ bao nhiêu?", 46, INK, alpha=k)
    for i, s in enumerate(OPTS):
        a = appear(t, sc["M"][1] + 0.2 + i * 0.12)
        x0 = 110 + (i % 2) * 440; y = 1320 + (i // 2) * 110
        card(d, (x0, y - 44, x0 + 420, y + 44), fill=A((245, 243, 255), a), outline=A(PURPLE, a), r=22, w=4)
        text(d, (x0 + 40, y), s, 44, INK, anchor="lm", alpha=a)
    t1, t2 = sc["M"][1] + 0.6, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1572, 940, 1586], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1572, 140 + 800 * (1 - q), 1586], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: quan them vong, do U2, ghi bang ----------------
WIND = 0.6
def row_at(i, sc): return sc["M"][i + 1] + 0.1 + WIND + 0.15

def do_state(t, sc):
    n2, rd = 0, "---"
    for i, (N, _, u, _) in enumerate(ROWS):
        s = sc["M"][i + 1] + 0.1
        if t < s: break
        k = clamp((t - s) / WIND); prev = ROWS[i - 1][0] if i else 0
        n2 = int(round(lerp(n_draw(prev), n_draw(N), k)))
        rd = fmt(u) if t >= row_at(i, sc) else "···"
    return n2, rd

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    n2, rd = do_state(t, sc)
    def note(d):
        a = appear(t, 0.3) * (1 - appear(t, sc["M"][1] - 0.2))
        if a > 0:
            ctext(d, 630, "không có", 36, RED, alpha=a); ctext(d, 680, "dây nối", 36, RED, alpha=a)
    rig(d, t, n2, rd, note=note)
    card(d, (60, 1020, 1020, 1495), fill=WHITE, outline=NAVY, w=4)
    xs = [230, 540, 840]
    for x, c in zip(xs, ["N₂ (vòng)", "N₁/N₂", "U₂ đo (V)"]): text(d, (x, 1068), c, 40, INK)
    d.line([(90, 1102), (990, 1102)], fill=LIGHT, width=4)
    last = max([i for i in range(4) if t >= row_at(i, sc)], default=-1)
    for i, (N, r, u, _) in enumerate(ROWS):
        a = appear(t, row_at(i, sc), 0.35); y = 1150 + i * 80
        if a <= 0: continue
        if i == last: d.rounded_rectangle([80, y - 34, 1000, y + 34], radius=16, fill=A((225, 236, 255), a))
        for x, s, col in zip(xs, [str(N), r, fmt(u)], [BLUE, INK, RED]):
            text(d, (x, y), s, 44, col, alpha=a)
    text(d, (W / 2, 1458), "Số liệu minh hoạ", 34, MUTED)
    c = appear(t, row_at(2, sc))
    if c > 0:
        card(d, (110, 1515, 970, 1615), fill=A((220, 252, 231), c), r=24)
        text(d, (W / 2, 1565), f"{fmt(ROWS[2][2])} ≈ 2 × {fmt(ROWS[1][2])}: gần gấp đôi", 42, GREEN, alpha=c)

# ---------------- canh 3: dap an C + do thi + so ti so ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k = back((t - 0.2) / 0.5) if t > 0.2 else 0
    card(d, (60, 250, 1020, 350), fill=(220, 252, 231), outline=GREEN, w=5)
    text(d, (W / 2, 300), "Đáp án C", int(48 * clamp(k, 0.3, 1.0)), GREEN)
    x0, x1, yb, yt = 200, 960, 920, 470
    X = lambda n: x0 + n / 700 * (x1 - x0); Y = lambda u: yb - u / 40 * (yb - yt)
    card(d, (60, 380, 1020, 1000), fill=WHITE, outline=LIGHT, w=3)
    for u in (10, 20, 30, 40): d.line([(x0, Y(u)), (x1, Y(u))], fill=(236, 232, 222), width=2)
    d.line([(x0, yb), (x1 + 25, yb)], fill=NAVY, width=5); d.line([(x0, yb), (x0, yt - 30)], fill=NAVY, width=5)
    text(d, (x0 + 18, yt - 36), "U₂ (V)", 38, INK, anchor="lm")
    text(d, (x1 - 175, yb - 40), "N₂ (vòng)", 38, INK, anchor="lm")
    text(d, (1000, yt - 36), "Số liệu minh hoạ", 34, MUTED, anchor="rm")
    for n in (0, 200, 400, 600):
        d.line([(X(n), yb), (X(n), yb + 10)], fill=NAVY, width=3); text(d, (X(n), yb + 38), str(n), 36, INK, bold=False)
    for u in (10, 20, 30, 40):
        d.line([(x0 - 10, Y(u)), (x0, Y(u))], fill=NAVY, width=4); text(d, (x0 - 20, Y(u)), str(u), 36, INK, bold=False, anchor="rm")
    text(d, (x0 - 20, yb), "0", 36, INK, bold=False, anchor="rm")
    # duong ly tuong U2 = U1.N2/N1 (net dut), hien o M[1]
    kl = ease((t - M[1]) / 1.0)
    if kl > 0:
        nmax = 40 * N1 / U1 * kl
        j = 0.0
        while j < nmax:
            j2 = min(j + 22, nmax)
            d.line([(X(j), Y(U1 * j / N1)), (X(j2), Y(U1 * j2 / N1))], fill=BLUE, width=6); j += 40
        text(d, (X(140), Y(27)), "U₂ = U₁·N₂/N₁", 40, BLUE, alpha=appear(t, M[1] + 0.8))
    # moc gap doi 200 -> 400
    g = appear(t, 0.6) * (1 - appear(t, M[1] - 0.2))
    for N, u in ((200, ROWS[1][2]), (400, ROWS[2][2])):
        if g > 0:
            d.line([(x0, Y(u)), (X(N), Y(u))], fill=A(GREEN, g), width=4)
            d.line([(X(N), Y(u)), (X(N), yb)], fill=A(GREEN, g), width=4)
    for i, (N, _, u, _) in enumerate(ROWS):
        a = appear(t, 0.3 + i * 0.15, 0.4)
        if a <= 0: continue
        dot(d, X(N), Y(u), 18 * back(a), ORANGE, WHITE)
        text(d, (X(N) + 30, Y(u) + 30), fmt(u), 36, ORANGE, anchor="lm", alpha=a)
    # bang so ti so
    a1 = appear(t, M[0] + 1.2)
    if a1 <= 0: return
    card(d, (60, 1030, 1020, 1630), fill=A(WHITE, a1), outline=A(LIGHT, a1), w=3)
    xs = [230, 540, 840]
    for x, c, col in zip(xs, ["N₂", "N₁/N₂", "U₁/U₂ đo"], [INK, INK, ORANGE]): text(d, (x, 1080), c, 42, col, alpha=a1)
    d.line([(90, 1116), (990, 1116)], fill=A(LIGHT, a1), width=4)
    for i, (N, r, _, q) in enumerate(ROWS):
        y = 1165 + i * 72
        text(d, (xs[0], y), str(N), 42, BLUE, alpha=a1)
        text(d, (xs[1], y), r, 42, INK, alpha=a1)
        text(d, (xs[2], y), q, 44, ORANGE, alpha=appear(t, M[2] + 0.2 + i * 0.2, 0.35))
    c = appear(t, M[2] + 1.2)
    ctext(d, 1530, "U₂ hơi thấp do hao phí", 44, INK, alpha=c, lh=1.25)

# ---------------- canh 4: co che + chua noi duoc gi ----------------
def s_why(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    core(d, 220, 270, 860, 900, 90)
    flux(d, t, 265, 315, 815, 855, size=24)
    text(d, (540, 470), "Φ biến thiên", 44, BLUE, alpha=appear(t, 0.3))
    ctext(d, 610, "không có", 36, RED, alpha=appear(t, 0.5)); ctext(d, 660, "dây nối", 36, RED, alpha=appear(t, 0.5))
    ts = M[1] + 0.2
    def fl(i, n):                                       # lan luot sang tung vong: moi vong cung mot e
        return clamp(1 - abs((t - ts) * 8 - i) / 2) if t > ts else 0
    nL, nR = n_draw(N1), n_draw(400)
    coil(d, 265, 585, nL, 150, 22, flash=lambda i: fl(i, nL))
    coil(d, 815, 585, nR, 150, 22, flash=lambda i: fl(i, nR))
    text(d, (110, 585), f"{U1} V ~", 40, INK)
    text(d, (265, 945), f"{N1} vòng", 38, INK); text(d, (815, 945), "400 vòng", 38, BLUE)
    e = appear(t, M[1] + 0.4)
    text(d, (265, 1000), "U₁ = 200·e", 42, ORANGE, alpha=e); text(d, (815, 1000), "U₂ = 400·e", 42, ORANGE, alpha=e)
    a = appear(t, 0.2)
    card(d, (60, 1040, 1020, 1300), fill=A(WHITE, a), outline=A(BLUE, a), w=5)
    ctext(d, 1095, "Cùng lõi: cùng từ thông", 44, INK, alpha=a)
    text(d, (W / 2, 1165), "e: suất điện động mỗi vòng", 40, ORANGE, alpha=e)
    text(d, (W / 2, 1240), "→ U₁/U₂ = N₁/N₂", 50, BLUE, alpha=appear(t, M[1] + 0.8))
    b = appear(t, M[2] - 0.3)
    if b <= 0: return
    card(d, (60, 1330, 1020, 1580), fill=A(WHITE, b), outline=A(PURPLE, b), w=5)
    text(d, (W / 2, 1390), "Chưa nói được gì?", 44, PURPLE, alpha=b)
    text(d, (W / 2, 1495), "Chưa đo dòng I", 46, INK, alpha=b)

# ---------------- canh 5: bay thang DC ----------------
def multimeter(d, x0, y0, x1, y1, ac, reading, a, kn=None):
    cx = (x0 + x1) / 2
    card(d, (x0, y0, x1, y1), fill=A((255, 236, 160), a), outline=A(NAVY, a), r=26, w=5)
    d.rounded_rectangle([x0 + 30, y0 + 40, x1 - 30, y0 + 170], radius=14, fill=A(NAVY, a))
    text(d, (cx, y0 + 105), reading, 72, (134, 239, 172) if ac else (252, 165, 165), alpha=a)
    r, cy = 110, y0 + 340
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=A(WHITE, a), outline=A(NAVY, a), width=5)
    text(d, (cx - 92, cy - 150), "DC", 40, INK, alpha=a); text(d, (cx + 92, cy - 150), "V~", 40, INK, alpha=a)
    ang = math.radians(lerp(-125, -55, ac if kn is None else kn))
    d.line([(cx, cy), (cx + (r - 14) * math.cos(ang), cy + (r - 14) * math.sin(ang))], fill=A(RED, a), width=12)
    dot(d, cx, cy, 16, A(NAVY, a))
    text(d, (cx, y1 - 50), "thang AC" if ac else "thang DC", 40, GREEN if ac else RED, alpha=a)

def s_trap(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    card(d, (60, 250, 1020, 350), fill=(254, 226, 226), outline=RED, w=5)
    text(d, (W / 2, 300), "Bẫy: thang DC", 48, RED, alpha=appear(t, 0.05, 0.2))
    text(d, (W / 2, 410), "Đo thứ cấp 400 vòng", 40, INK, alpha=appear(t, 0.05, 0.2))
    # MOT dong ho, hai trang thai: thang DC chi 0 -> van nup sang V~ chi 23,5
    a = appear(t, 0.05, 0.25); kn = ease((t - M[1] + 0.3) / 0.5); ac = kn >= 1
    multimeter(d, 300, 470, 780, 1070, ac, fmt(ROWS[2][2]) if ac else ("0" if kn <= 0 else "···"), a, kn=kn)
    if not ac and kn <= 0:                               # dau X do
        d.line([(830, 700), (930, 800)], fill=A(RED, a), width=14); d.line([(930, 700), (830, 800)], fill=A(RED, a), width=14)
    b = appear(t, M[1] + 0.25)
    if b > 0:                                            # dau tich xanh
        d.line([(830, 760), (865, 800)], fill=A(GREEN, b), width=14); d.line([(865, 800), (940, 710)], fill=A(GREEN, b), width=14)
    c = appear(t, M[1] + 0.6)
    card(d, (90, 1150, 990, 1290), fill=A((220, 252, 231), c), r=24)
    ctext(d, 1220, "Vặn về thang AC (V~)", 48, GREEN, alpha=c)

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    chot_hoi(d, t, sc, "U₁/U₂ = N₁/N₂",
             "Muốn thứ cấp ra 6 V: hơn hay kém 100 vòng?")
    kh = appear(t, sc["M"][0] + 2.5, 0.4)                # goi y hien sau 2,5 s cho HS tu nghi truoc
    if kh > 0:
        card(d, (110, 1110, 970, 1330), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1165), "Gợi ý", 38, INK, alpha=kh)
        text(d, (W / 2, 1255), "100 vòng cho ra mấy vôn?", 46, ORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    out = [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + row_at(2, do), "tap"), (an["t0"] + 0.2, "ding"),
            (tr["t0"] + 0.05, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l12-mayphatdien-03", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Máy biến áp · thachlab.id.vn", scenes=[
 dict(key="hook", title="Tự quấn máy biến áp", draw=s_hook, tail=0.6, caps=[
   ("Sơ cấp 200 vòng, nguồn 12 V.", 2.3),
   ("Chọn đáp án.", 5.7)]),
 dict(key="do", title="Quấn thêm vòng, đo U₂", draw=s_do, tail=0.4, caps=[
   ("Hai cuộn chung lõi.", 2.1),
   ("100 vòng → 5,9 V", 1.9), ("200 vòng → 11,6 V", 1.9),
   ("400 vòng → 23,5 V", 2.6),
   ("600 vòng → 35,1 V", 2.0)]),
 dict(key="ans", title="Đồ thị U₂ theo N₂", draw=s_ans, tail=0.5, caps=[
   ("N₂ gấp đôi, U₂ gấp đôi.", 2.8),
   ("Điểm bám đường thẳng.", 2.6),
   ("Hao phí nhỏ.", 2.4)]),
 dict(key="why", title="Vì sao tỉ lệ số vòng?", draw=s_why, tail=0.5, caps=[
   ("Cùng lõi kín.", 2.6),
   ("Mỗi vòng cùng e.", 2.6),
   ("Chưa biết hiệu suất.", 3.0)]),
 dict(key="trap", title="Cái bẫy khi đo", draw=s_trap, tail=0.6, caps=[
   ("Thang DC: chỉ 0.", 2.6),
   ("Đúng: thang AC.", 2.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Thử nghĩ: hơn hay kém?", 4.6)]),
])
