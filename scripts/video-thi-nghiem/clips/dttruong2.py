# Clip: tn-l12-dttruong-02 - Dong xoay chieu "di qua" tu dien: dien truong bien thien tuong duong dong dien dich
# Ban 2 (26/11/2026): khung mau xoaychieu2 (hook Du doan -> do -> ans co ĐÁP ÁN tu 0 s -> bay -> gioi -> end THU NGHI).
# So lieu nguyen tu content/thi-nghiem/tn-l12-dttruong-02.json: f = 50..800 Hz -> I = 3,6 ; 7,4 ; 14,8 ; 29,5 ; 58,0 mA;
#   mot chieu 0 mA; mo hinh I = U.2.pi.f.C = 0,0754.f (mA); I/f do duoc 0,072-0,074 mA/Hz.
# Du doan: hien_tuong_hay_sai[1] (tu can manh hon khi f cao). Bay: hien_tuong_hay_sai[0] (dien tich chay xuyen dien moi).
# Chot THU NGHI: f = 1 600 Hz -> I ≈ 2 . 58,0 ≈ 116 mA (mo hinh 120,6 mA; do thap hon ~3%).
# Hinh: dien tich chi dao dong trong DAY va tich tren hai ban; giua hai ban chi ve mui ten E (khong ve hat qua dien moi).
from engine import *

DGREEN = (21, 128, 61); DARK_OR = (181, 71, 8); NOTE = (70, 75, 95)
assert abs(12 * 2 * math.pi * 1e-6 * 1000 - 0.0754) < 1e-4
assert abs(2 * 58.0 - 116) < 1e-9 and abs(0.0754 * 1600 - 120.6) < 0.1
ROWS = [(50, "3,6"), (100, "7,4"), (200, "14,8"), (400, "29,5"), (800, "58,0")]   # so_lieu_mau: f (Hz), I do (mA)
IV = [3.6, 7.4, 14.8, 29.5, 58.0]
RATIO = ["0,072", "0,074", "0,074", "0,074", "0,073"]   # I/f (mA/Hz) = cot 2 / cot 1, lam tron 3 so le (nhu bang trong bai)
U, C_UF = 12, "1,0"                                      # tham_so: U = 12 V, C = 1,0 uF
K_MODEL = 0.0754                                         # mo_hinh: I = 0,0754*f (mA) voi U = 12 V, C = 1,0 uF

# ---------------- dung cu: may phat + tu + dong ho ----------------
WY = 880                              # do cao day duoi
PL, PR = 492, 588                     # mat trong ban trai / ban phai (giua: dien moi)
PT, PB = 790, 970                     # mep tren / duoi hai ban
GXW, AXW = 270, 810                   # day doc o may phat / dong ho
AMP = 22                              # bien do dich chuyen cua dien tich trong day (px)

LEFT = [(GXW, 600), (GXW, WY), (PL - 26, WY)]
RIGHT = [(PR + 26, WY), (AXW, WY), (AXW, 600)]
RY = 395                              # day hoi: cuc phai may phat (470) -> cuc trai dong ho (610), khep kin mach
BACK = [(610, RY), (470, RY)]         # cung chieu vong: may phat -> tu -> dong ho -> may phat
TERMS = [(GXW, 600), (470, RY), (AXW, 600), (610, RY)]   # hai cuc may phat + hai cuc dong ho

def _path_len(p): return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(p, p[1:]))
def _at(p, s):
    for a, b in zip(p, p[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if s <= L: return a[0] + (b[0] - a[0]) * s / L, a[1] + (b[1] - a[1]) * s / L
        s -= L
    return p[-1]

def charges(d, path, x, col=BLUE):
    L = _path_len(path); s = AMP + 8
    while s < L - AMP - 8:
        px, py = _at(path, s + x); dot(d, px, py, 9, col); s += 46

def viz_hz(f): return 0.45 * (f / 50) ** 0.35        # nhip nhin thay (dinh tinh): f lon -> dao dong nhanh hon

def plates(d, q, x0=PL, x1=PR, top=PT, bot=PB, th=26, sz=64, lbl_e=True, show_e=True):
    """q in [-1,1]: dien tich ban trai (ban phai trai dau). Mui ten E tu ban + sang ban -, chi o vung tren/duoi day."""
    d.rectangle([x0, top, x1, bot], fill=(255, 243, 214))               # dien moi
    for (a, b), qq in (((x0 - th, x0), q), ((x1, x1 + th), -q)):
        c = mix((205, 210, 222), RED if qq > 0 else BLUE, abs(qq))
        d.rectangle([a, top, b, bot], fill=c, outline=NAVY, width=3)
        n = int(round(abs(qq) * 3))
        for j in range(n):
            text(d, ((a + b) / 2, top + 30 + j * (bot - top - 60) / 2), "+" if qq > 0 else "−", sz, WHITE)
    if show_e and abs(q) > 0.08:
        gy = [top + (bot - top) * 0.2, bot - (bot - top) * 0.2]
        for y in gy:
            p1, p2 = (x0 + 10, y), (x1 - 10, y)
            if q < 0: p1, p2 = p2, p1
            arrow(d, p1, p2, A(ORANGE, clamp(abs(q) * 1.3)), w=5, head=14)
        if lbl_e: text(d, ((x0 + x1) / 2, (top + bot) / 2), "E", 56, A(ORANGE, clamp(abs(q) * 1.3)))

def rig(d, t, f, reading, phase=None, dc=False, label=True):
    """f: tan so dang dat; reading: chuoi so tren dong ho; phase: None = may phat chua bat."""
    # day
    d.line(LEFT, fill=GRAY, width=12, joint="curve"); d.line(RIGHT, fill=GRAY, width=12, joint="curve")
    if phase is None: x, q = 0.0, 0.0
    elif dc: x, q = AMP, -1.0
    else:
        s = math.sin(phase); x, q = AMP * s, -s          # e den ban trai -> ban trai am
    plates(d, q)
    charges(d, LEFT, x); charges(d, RIGHT, x)
    if label:
        text(d, ((PL + PR) / 2, 720), f"tụ {C_UF} μF", 56, NAVY)
    # may phat
    card(d, (70, 258, 470, 612), fill=WHITE, outline=NAVY, r=28, w=5)
    text(d, (270, 306), "máy phát", 56, NOTE, bold=False)
    d.rounded_rectangle([100, 350, 440, 455], radius=14, fill=NAVY)
    if phase is not None:
        if dc: d.line([(120, 375), (420, 375)], fill=(134, 239, 172), width=5)
        else:
            cyc = 1 + math.log2(f / 50); pts = []
            for j in range(121):
                u = j / 120; pts.append((120 + 300 * u, 395 - 40 * math.sin(2 * math.pi * cyc * u + phase)))
            d.line(pts, fill=(134, 239, 172), width=5, joint="curve")
    text(d, (270, 498), "một chiều" if dc else f"{f} Hz", 56, BLUE)
    text(d, (270, 563), f"U = {U} V", 56, NOTE, bold=False)
    # dong ho
    card(d, (610, 258, 1010, 612), fill=WHITE, outline=NAVY, r=28, w=5)
    text(d, (810, 306), "đồng hồ", 56, NOTE, bold=False)
    d.rounded_rectangle([650, 350, 970, 455], radius=14, fill=NAVY)
    text(d, (810, 403), reading, 66, (134, 239, 172))
    text(d, (810, 515), "mA", 56, RED)
    d.line(BACK, fill=GRAY, width=12)                                  # day hoi giua hai the
    if phase is not None: charges(d, BACK, x)
    for tx, ty in TERMS: dot(d, tx, ty, 17, NAVY, WHITE); dot(d, tx, ty, 6, WHITE)   # cuc noi day

for (f_, _), i_, r_ in zip(ROWS, IV, RATIO): assert f"{i_ / f_ + 1e-9:.3f}".replace(".", ",") == r_

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    rig(d, t, 50, "?", phase=None)
    M = sc["M"]; a = appear(t, M[1] - 0.4, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 104), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 64), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    text(d, (W / 2, y0 + 185), "Tăng f: 50 → 800 Hz.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 270), "Dòng qua tụ thế nào?", 60, PURPLE, alpha=a)
    tc, te = M[1] + 0.3, sc["T"] - 0.1
    p = clamp((t - tc) / (te - tc))
    d.rounded_rectangle([110, y0 + 350, 970, y0 + 450], radius=24, fill=A(LIGHT, a))
    if p < 1: d.rounded_rectangle([110, y0 + 350, 110 + 860 * (1 - p), y0 + 450], radius=24, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
def row_at(i, sc):
    M = sc["M"]
    return [M[0] + 0.6, M[0] + 1.3, M[0] + 2.0, M[0] + 2.7, M[0] + 3.4, M[1] + 0.4][i]

def do_state(t, sc):
    if t < row_at(0, sc) - 0.4: return 50, "···", False, t > 0.3
    last = max([i for i in range(6) if t >= row_at(i, sc)], default=-1)
    if last == 5: return 0, "0", True, True
    nxt = min(last + 1, 5)
    if t >= row_at(nxt, sc) - 0.2:
        return (ROWS[nxt][0] if nxt < 5 else 0), "···", nxt == 5, True
    if last < 0: return 50, "···", False, True
    return ROWS[last][0], ROWS[last][1], False, True

def _phase(t, sc):
    ph, prev_t, prev_f = 0.0, 0.0, 50
    for i in range(5):
        a = row_at(i, sc)
        if t <= a: break
        ph += 2 * math.pi * viz_hz(prev_f) * (a - prev_t); prev_t, prev_f = a, ROWS[i][0]
    return ph + 2 * math.pi * viz_hz(prev_f) * (t - prev_t)

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    f, rd, dc, on = do_state(t, sc)
    rig(d, t, f if not dc else 50, rd, phase=_phase(t, sc) if on else None, dc=dc)
    card(d, (40, 1000, 1040, 1588), fill=WHITE, outline=NAVY, w=4)
    xs = [300, 760]
    for x, c in zip(xs, ["f (Hz)", "I (mA)"]): text(d, (x, 1050), c, 56, NOTE)
    d.line([(80, 1088), (1000, 1088)], fill=LIGHT, width=4)
    last = max([i for i in range(6) if t >= row_at(i, sc)], default=-1)
    rows = [(str(f_), s) for f_, s in ROWS] + [("một chiều", "0")]
    for i, (a_, b_) in enumerate(rows):
        a = appear(t, row_at(i, sc), 0.3); y = 1120 + i * 70
        if a <= 0: continue
        if i == last: d.rounded_rectangle([70, y - 34, 1010, y + 34], radius=14, fill=A((225, 236, 255), a))
        text(d, (xs[0], y), a_, 56, BLUE, alpha=a)
        text(d, (xs[1], y), b_, 56, RED, alpha=a)
    text(d, (1010, 1552), "số liệu minh hoạ", 56, NOTE, bold=False, anchor="rm")

# ---------------- canh 3: Ket qua ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    s = "ĐÁP ÁN: tăng theo f"; pw = tw(d, s, F(56)) + 70                  # hien ngay tu 0 s
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 340), fill=GREEN, r=39)
    text(d, (W / 2, 301), s, 56, WHITE)
    x0, x1, yb, yt = 200, 940, 860, 470
    X = lambda f: x0 + f / 850 * (x1 - x0); Y = lambda i: yb - i / 65 * (yb - yt)
    card(d, (40, 370, 1040, 970), fill=WHITE, outline=LIGHT, w=3)
    d.line([(x0, yb), (x1 + 30, yb)], fill=NAVY, width=5); d.line([(x0, yb), (x0, yt - 40)], fill=NAVY, width=5)
    text(d, (x0 + 20, yt - 40), "I (mA)", 56, INK, anchor="lm")
    text(d, (1010, yb - 44), "f (Hz)", 56, INK, anchor="rm")
    text(d, (1010, 760), "minh hoạ", 56, NOTE, bold=False, anchor="rm")
    for f in (400, 800):
        d.line([(X(f), yb), (X(f), yb + 10)], fill=NAVY, width=3); text(d, (X(f), yb + 46), str(f), 56, NOTE, bold=False)
    for i in (30, 60):
        d.line([(x0 - 10, Y(i)), (x0, Y(i))], fill=NAVY, width=4); text(d, (x0 - 18, Y(i)), str(i), 56, NOTE, bold=False, anchor="rm")
    kc = ease((t - 0.3) / 1.2)
    fe = 850 * kc
    for j in range(0, int(fe), 30):
        d.line([(X(j), Y(K_MODEL * j)), (X(min(j + 18, fe)), Y(K_MODEL * min(j + 18, fe)))], fill=A(BLUE, 0.6), width=5)
    for i, (f, s) in enumerate(ROWS):
        dot(d, X(f), Y(IV[i]), 15, ORANGE, WHITE)
    for i in (0, 4):
        text(d, (X(ROWS[i][0]) + (30 if i == 0 else -30), Y(IV[i]) - 50), ROWS[i][1], 56, ORANGE, anchor="lm" if i == 0 else "rm")
    k1 = appear(t, M[1] - 0.1, 0.4)
    if k1 > 0:
        card(d, (40, 995, 1040, 1085), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=4)
        text(d, (W / 2, 1040), "I/f ≈ 0,073 mA/Hz", 56, DGREEN, alpha=k1)
    k = appear(t, M[2] - 0.1, 0.5)
    card(d, (40, 1105, 1040, 1588), fill=A(WHITE, k), outline=A(BLUE, k), w=5)
    if k <= 0: return
    ph = 2 * math.pi * 0.5 * t; q = -math.sin(ph); x = 26 * math.sin(ph)
    lp = [(80, 1330), (230, 1330)]; rp = [(410, 1330), (560, 1330)]
    d.line(lp, fill=GRAY, width=12); d.line(rp, fill=GRAY, width=12)
    plates(d, q, 270, 370, 1150, 1490, th=30, sz=64, lbl_e=False)
    for p in (lp, rp):
        for u in (30, 80, 130):
            px, py = _at(p, u + x); dot(d, px, py, 10, BLUE)
    text(d, (320, 1540), "điện môi", 56, NOTE, alpha=k)
    text(d, (600, 1190), "E biến thiên", 56, ORANGE, anchor="lm", alpha=k)
    text(d, (600, 1270), "giữa hai bản", 56, ORANGE, anchor="lm", alpha=k)
    text(d, (600, 1380), "→ như dòng", 60, BLUE, anchor="lm", alpha=k)
    text(d, (600, 1460), "điện dịch", 60, BLUE, anchor="lm", alpha=k)

# ---------------- canh 4: Bay ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    b1, b2, b3 = (m - 0.1 for m in sc["M"])
    k2, k3 = appear(t, b2, 0.4), appear(t, b3, 0.4)
    card(d, (40, 262, 1040, 620), outline=RED, w=5)
    pw = tw(d, "BẪY", F(56)) + 60
    card(d, (W / 2 - pw / 2, 282, W / 2 + pw / 2, 358), fill=RED, r=38)
    text(d, (W / 2, 320), "BẪY", 56, WHITE)
    ks = clamp((t - b3) / 0.4)
    for j, q in enumerate(("“Điện tích chạy xuyên", "qua điện môi”")):
        yy = 445 + 85 * j
        text(d, (W / 2, yy), q, 60, mix(INK, GRAY, 0.45 * ks))
        if ks > 0:
            lw = tw(d, q, F(60))
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85), width=6)
    if k3 > 0:
        pw2 = tw(d, "SAI", F(56)) + 50
        card(d, (1020 - pw2, 282, 1020, 358), fill=A((127, 29, 29), k3), r=38)
        text(d, (1020 - pw2 / 2, 320), "SAI", 56, WHITE, alpha=k3)
    card(d, (40, 650, 1040, 1380), fill=A(WHITE, k2), outline=A(LIGHT, k2), w=3)
    if k2 > 0:
        text(d, (W / 2, 720), "nguồn một chiều 12 V", 56, NOTE, alpha=k2)
        lp = [(100, 1000), (480, 1000)]; rp = [(600, 1000), (980, 1000)]
        d.line(lp, fill=GRAY, width=12); d.line(rp, fill=GRAY, width=12)
        qd = ease((t - b2) / 0.8)
        plates(d, -qd, 506, 574, 820, 1180, th=26, sz=64, lbl_e=False)
        for p in (lp, rp):
            for u in (60, 150, 240, 330):
                px, py = _at(p, u + 26 * qd); dot(d, px, py, 10, BLUE)
        d.rounded_rectangle([340, 1220, 740, 1340], radius=14, fill=NAVY)
        text(d, (540, 1280), "0 mA", 64, (134, 239, 172))
    if k3 > 0:
        card(d, (40, 1410, 1040, 1588), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
        text(d, (W / 2, 1499), "electron chỉ tới – lui", 60, DGREEN, alpha=k3)

# ---------------- canh 5: Chua noi duoc gi ----------------
def s_gioi(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.2, 0.4); kb = appear(t, 2.4, 0.4)
    card(d, (40, 300, 1040, 1000), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    for j, s in enumerate(("• E giữa hai bản: chưa đo", "• Từ trường của dòng dịch?")):
        text(d, (90, 520 + j * 240), s, 62, INK, anchor="lm", alpha=kb)
    text(d, (W / 2, 650), "?", 180, NAVY, alpha=k * (1 - kb))

# ---------------- canh 6: THU NGHI (cau_chot; dap an KHONG hien) ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.3, 0.5)
    card(d, (40, 260, 1040, 1200), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 285, W / 2 + pw / 2, 365), fill=A(DARK_OR, k), r=40)
    text(d, (W / 2, 325), "THỬ NGHĨ", 56, WHITE, alpha=k)
    text(d, (W / 2, 450), "Cùng tụ, cùng 12 V.", 60, INK, alpha=k)
    text(d, (W / 2, 540), "f = 1 600 Hz: I ≈ ? mA", 60, DARK_OR, alpha=k)
    ph = 2 * math.pi * 1.2 * t; q = -math.sin(ph); x = 22 * math.sin(ph)
    lp = [(120, 850), (480, 850)]; rp = [(600, 850), (960, 850)]
    d.line(lp, fill=GRAY, width=12); d.line(rp, fill=GRAY, width=12)
    plates(d, q, 506, 574, 700, 1000, th=26, sz=64, lbl_e=False)
    for p in (lp, rp):
        for u in (60, 150, 240, 330):
            px, py = _at(p, u + x); dot(d, px, py, 10, BLUE)
    d.rounded_rectangle([340, 1040, 740, 1150], radius=14, fill=A(NAVY, k))
    text(d, (540, 1095), "? mA", 64, (134, 239, 172), alpha=k)
    kh = appear(t, 3.3, 0.5)
    if kh > 0:
        card(d, (90, 1240, 990, 1390), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1315), "Gợi ý: so với 800 Hz", 60, DARK_OR, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, b, g, e = (sc[k] for k in ("hook", "do", "ans", "bay", "gioi", "end"))
    return ([(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + row_at(i, do), "tap") for i in (0, 5)]
            + [(an["t0"] + 0.1, "ding"), (an["t0"] + an["M"][2] - 0.1, "tap"),
               (b["t0"] + b["M"][0] - 0.1, "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"),
               (g["t0"] + 2.4, "tap"), (e["t0"] + 0.3, "open")])

CLIP = dict(id="tn-l12-dttruong-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Dòng điện dịch · thachlab.id.vn", scenes=[
 dict(key="hook", title="Dòng xoay chiều qua tụ", draw=s_hook, tail=0.3, caps=[
   ("Tụ nối tiếp đồng hồ.", 3.0),
   ("Dừng lại, tự đoán.", 5.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Giữ 12 V, tăng dần f.", 4.4),
   ("Rồi đổi sang một chiều.", 3.6)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.4, caps=[
   ("f gấp 16, I gấp ≈ 16.", 3.0),
   ("I/f gần như không đổi.", 3.0),
   ("E đổi: dòng điện dịch.", 3.2)]),
 dict(key="bay", title="Bẫy", draw=s_bay, tail=0.3, caps=[
   ("Đúng hay sai?", 3.0),
   ("Nguồn một chiều: 0 mA.", 3.0),
   ("Không hạt nào qua điện môi.", 3.0)]),
 dict(key="gioi", title="Chưa nói được gì?", draw=s_gioi, tail=0.3, caps=[
   ("Chưa trả lời được:", 4.0)]),
 dict(key="end", title="Tự kiểm tra", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự trả lời.", 6.6)]),
])
