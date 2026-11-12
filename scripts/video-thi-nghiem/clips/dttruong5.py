# Clip: tn-l12-dttruong-05 - Mo hinh song dien tu: E, B va phuong truyen tai diem M (ban 1, 12/11/2026)
# Kho loai "vi_du" (mo hinh): clip ghi ro "mo hinh · hinh ve li thuyet", khong phai anh chup.
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-dttruong-05.json:
#   so_lieu_mau tai M: t = 0 -> E/E0 = 1, B/B0 = 1 | T/4 -> 0, 0 | T/2 -> -1, -1 | 3T/4 -> 0, 0 | T -> 1, 1
#   tham_so: c = 3.10^8 m/s. mo_hinh: E = E0.cos(2pi.t/T - 2pi.x/lambda) theo Oy, B cung pha theo Oz, truyen theo Ox.
# Hinh phoi canh (it net): Ox nam ngang sang phai, Oy thang dung len, Oz xien xuong-trai (huong ra phia nguoi xem)
#   -> he thuan: y x z = x, nen E (Oy) va B (Oz) cung pha thi song truyen theo +Ox (dung chieu mui ten).
# Du doan (khung): Tai M, E dang cuc dai thi B ... A bang 0 / B cuc dai (dung) / C bang nua cuc dai / D tuy khoang cach toi nguon.
#   Trong mp4 KHONG ve nut A-D (K10).
# Bay chinh: E, B CUNG pha (khong lech T/4); E vuong goc B vuong goc phuong truyen; truyen duoc trong chan khong.
# Font SF khong co glyph "⊥" -> viet "vuong goc" bang chu.
from engine import *

NOTE = (70, 75, 95)
OX, OY = 220, 580                 # goc O tren man hinh (khung 1080 x 1920)
XEND = 1000                       # dau truc Ox
LAM = 380.0                       # buoc song tren hinh (px)
XM = 600                          # diem M
AE, AB = 165.0, 100.0             # bien do ve E (doc) va B (xien)
ZX, ZY = -0.5, 0.866               # huong +Oz tren man hinh (xuong-trai)

def wave(x, ph):
    """E/E0 = B/B0 tai x, pha ph = 2pi.t/T (M o pha 0 khi t = 0)."""
    return math.cos(ph - 2 * math.pi * (x - XM) / LAM)

def axes(d, show_lab=True):
    d.line([(OX, OY), (XEND, OY)], fill=NAVY, width=4); arrow(d, (XEND - 30, OY), (XEND + 20, OY), NAVY, w=4, head=20)
    d.line([(OX, OY), (OX, OY - 230)], fill=NAVY, width=4); arrow(d, (OX, OY - 200), (OX, OY - 250), NAVY, w=4, head=20)
    zx, zy = OX + ZX * 210, OY + ZY * 210
    d.line([(OX, OY), (zx, zy)], fill=NAVY, width=4); arrow(d, (OX + ZX * 180, OY + ZY * 180), (zx, zy), NAVY, w=4, head=20)
    if show_lab:
        text(d, (XEND + 24, OY + 46), "x", 44, NAVY)
        text(d, (OX + 34, OY - 262), "y", 44, NAVY)
        text(d, (zx - 26, zy + 30), "z", 44, NAVY)
        text(d, (OX - 30, OY - 26), "O", 40, NAVY)
    # mui ten phuong truyen phia tren hinh
    arrow(d, (780, 300), (1010, 300), GREEN, w=7, head=22)
    text(d, (760, 300), "phương truyền", 40, GREEN, anchor="rm")

def curves(d, ph, showB=True):
    xs = [OX + k * 6 for k in range(int((XEND - 40 - OX) / 6) + 1)]
    if showB:
        pts = [(x + ZX * AB * wave(x, ph), OY + ZY * AB * wave(x, ph)) for x in xs]
        d.line(pts, fill=BLUE, width=5, joint="curve")
    pts = [(x, OY - AE * wave(x, ph)) for x in xs]
    d.line(pts, fill=RED, width=5, joint="curve")

def at_M(d, ph, showB=True, qB=False):
    e = wave(XM, ph)
    for y in range(OY + 18, OY + 196, 18): d.line([(XM, y), (XM, y + 8)], fill=GRAY, width=3)   # duong dan toi nhan M
    dot(d, XM, OY, 12, NAVY)
    text(d, (XM + 60, OY + 212), "M", 40, NAVY, anchor="lm")
    sg = 1 if e > 0 else -1
    if abs(e) > 0.06:
        arrow(d, (XM, OY), (XM, OY - AE * e), RED, w=10, head=26)
        if showB:
            bx, by = XM + ZX * AB * e, OY + ZY * AB * e
            arrow(d, (XM, OY), (bx, by), BLUE, w=10, head=26)
    if abs(e) > 0.35:                                 # nhan chi hien khi mui ten du dai (khong chong nhan M)
        text(d, (XM, OY - AE * e - 40 * sg), "E", 44, RED)
        if showB: text(d, (XM + ZX * AB * e + 20, OY + ZY * AB * e + 40 * sg), "B", 44, BLUE, anchor="lm")
    if qB:
        L = 46                                           # doan ngan chi phuong Oz, khong goi y do lon B
        bx, by = XM + ZX * L, OY + ZY * L
        d.line([(XM, OY), (bx, by)], fill=BLUE, width=5)
        card(d, (bx + 14, by - 4, bx + 98, by + 72), fill=WHITE, outline=BLUE, r=16, w=4)
        text(d, (bx + 56, by + 34), "B?", 40, BLUE)

def tag(d, y, alpha=1.0):
    text(d, (1030, y), "mô hình · hình vẽ lí thuyết", 40, NOTE, bold=False, anchor="rm", alpha=alpha)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    axes(d); curves(d, 0.0, showB=False); at_M(d, 0.0, showB=False, qB=True)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 900 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 235, "Tại M, E đang cực đại.\nLúc đó B tại M ra sao?", 56, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 410, 940, y0 + 422], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 410, 140 + 800 * (1 - p), y0 + 422], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
STOPS = [0.6, 1.5, 3.1, 4.7, 6.3]          # moc hien hang 0, T/4, T/2, 3T/4, T
MOVES = [(0.7, 1.4), (2.3, 3.0), (3.9, 4.6), (5.5, 6.2)]
RUN0 = 7.0                                  # sau do song chay lien tuc (cham)
ROWS = (("0", 1, 1), ("T/4", 0, 0), ("T/2", -1, -1), ("3T/4", 0, 0), ("T", 1, 1))

def ph_at(t):
    q = 0.0
    for a, b in MOVES:
        if t >= b: q += 1
        elif t > a: q += ease((t - a) / (b - a))
    if t > RUN0: q += (t - RUN0) * 0.55
    return q * math.pi / 2

def nv(v): return "0" if v == 0 else ("+1" if v > 0 else "−1")

def meters(d, ph, y0=850):
    card(d, (40, y0, 1040, y0 + 250), fill=WHITE, outline=LIGHT, w=3)
    e = wave(XM, ph)
    for j, (lab, col) in enumerate((("E/E₀", RED), ("B/B₀", BLUE))):
        yy = y0 + 60 + j * 84
        text(d, (90, yy), lab, 44, col, anchor="lm")
        d.rounded_rectangle([300, yy - 14, 900, yy + 14], radius=14, fill=LIGHT)
        x1 = 600 + 300 * e
        if abs(x1 - 600) > 3: d.rounded_rectangle([min(600, x1), yy - 14, max(600, x1), yy + 14], radius=14, fill=col)
        d.line([(600, yy - 24), (600, yy + 24)], fill=NAVY, width=3)
    for x, s in ((300, "−1"), (600, "0"), (900, "+1")):
        text(d, (x, y0 + 214), s, 40, NOTE, bold=False)

def table(d, y0, ks):
    rh = 66; h = 84 + rh * 5
    card(d, (40, y0, 1040, y0 + h), fill=WHITE, outline=LIGHT, w=3)
    for x, s, c in ((250, "t", NOTE), (560, "E/E₀", RED), (840, "B/B₀", BLUE)): text(d, (x, y0 + 44), s, 40, c)
    d.line([(70, y0 + 82), (1010, y0 + 82)], fill=LIGHT, width=3)
    for j, (r, k) in enumerate(zip(ROWS, ks)):
        if k <= 0: continue
        yy = y0 + 82 + rh * (j + 0.5) + 2
        text(d, (250, yy), r[0], 42, INK, alpha=k)
        text(d, (560, yy), nv(r[1]), 42, RED, alpha=k)
        text(d, (840, yy), nv(r[2]), 42, BLUE, alpha=k)
    return h

def s_do(img, d, t, sc):
    ph = ph_at(t)
    axes(d); curves(d, ph); at_M(d, ph)
    meters(d, ph)
    ks = [appear(t, s, 0.35) for s in STOPS]
    table(d, 1135, ks)
    tag(d, 1660)

# ---------------- canh 3: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, M[0] + 0.1, 0.4)
    pw = tw(d, "ĐÁP ÁN B", F(40)) + 56
    card(d, (W / 2 - pw / 2, 270, W / 2 + pw / 2, 336), fill=A(NAVY, ka), r=33)
    text(d, (W / 2, 303), "ĐÁP ÁN B", 40, WHITE, alpha=ka)
    # hai do thi theo thoi gian tai M, cung truc t
    x0, x1 = 230, 980
    X = lambda u: x0 + u * (x1 - x0)                 # u = t/T tu 0 den 1
    kg = appear(t, 0.5, 0.5)
    for yc, lab, col in ((470, "E", RED), (660, "B", BLUE)):
        d.line([(x0, yc), (x1 + 10, yc)], fill=A(NAVY, kg), width=3)
        text(d, (x0 - 50, yc), lab, 44, col, alpha=kg)
        pts = [(X(u / 100), yc - 70 * math.cos(2 * math.pi * u / 100)) for u in range(101)]
        k = appear(t, 0.6 if lab == "E" else 1.0, 0.6)
        n = max(2, int(101 * k))
        d.line(pts[:n], fill=A(col, kg), width=6, joint="curve")
    kd = appear(t, 1.8, 0.4)
    if kd > 0:
        for u in (0, 0.5, 1.0):
            for y in range(380, 760, 26): d.line([(X(u), y), (X(u), y + 13)], fill=A(GREEN, kd), width=4)
        for u, s in ((0, "0"), (0.5, "T/2"), (1.0, "T")): text(d, (X(u), 790), s, 40, NOTE, bold=False, alpha=kd)
        text(d, (W / 2, 860), "Cùng cực đại, cùng bằng 0", 46, GREEN, alpha=kd)
    k2 = appear(t, M[1] + 0.2, 0.5)
    card(d, (40, 930, 1040, 1420), fill=A(WHITE, k2), outline=A(LIGHT, k2), w=3)
    if k2 > 0:
        cx, cy = 210, 1170                            # bieu tuong ba phuong vuong goc
        arrow(d, (cx, cy), (cx, cy - 150), A(RED, k2), w=8, head=22); text(d, (cx + 30, cy - 140), "E", 44, RED, anchor="lm", alpha=k2)
        arrow(d, (cx, cy), (cx + ZX * 140, cy + ZY * 140), A(BLUE, k2), w=8, head=22)
        text(d, (cx + ZX * 140 + 40, cy + ZY * 140 + 6), "B", 44, BLUE, anchor="lm", alpha=k2)
        arrow(d, (cx, cy), (cx + 170, cy), A(GREEN, k2), w=8, head=22)
        text(d, (cx + 26, cy - 44), "phương truyền", 40, GREEN, anchor="lm", alpha=k2)
        text(d, (540, 1030), "E vuông góc B", 44, INK, anchor="lm", alpha=k2)
        text(d, (540, 1110), "Cả hai vuông góc", 44, INK, anchor="lm", alpha=k2)
        text(d, (540, 1170), "phương truyền", 44, INK, anchor="lm", alpha=k2)
        text(d, (540, 1250), "→ sóng ngang", 44, GREEN, anchor="lm", alpha=k2)
        k3 = appear(t, M[1] + 1.6, 0.45)
        text(d, (W / 2, 1360), "Truyền cả trong chân không: c = 3·10⁸ m/s", 40, NAVY, alpha=k3)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def mini_plot(d, box, shift, alpha):
    x0, y0, x1, y1 = box; yc = (y0 + y1) / 2; amp = (y1 - y0) * 0.36
    d.line([(x0 + 16, yc), (x1 - 16, yc)], fill=A(NAVY, alpha), width=3)
    X = lambda u: x0 + 20 + u * (x1 - x0 - 40)
    e = [(X(u / 80), yc - amp * math.cos(2 * math.pi * u / 80)) for u in range(81)]
    b = [(X(u / 80), yc - amp * math.cos(2 * math.pi * u / 80 - shift)) for u in range(81)]
    d.line(e, fill=A(RED, alpha), width=6, joint="curve")
    for k in range(0, 80, 4): d.line(b[k:k + 3], fill=A(BLUE, alpha), width=6)

def strike_q(d, y, q, ks, alpha):
    f = F(44); ls = wrap(d, q, f, 900)
    for i, l in enumerate(ls):
        yy = y + i * 56
        text(d, (W / 2, yy), l, 44, mix(INK, GRAY, ks), alpha=alpha)
        if ks > 0:
            lw = tw(d, l, f)
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * alpha), width=5)

def s_bay(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, 0.2, 0.4); mk = 3.2
    card(d, (40, 270, 1040, 1010), fill=A(WHITE, k1), outline=A(RED, k1), w=6)
    pw = tw(d, "BẪY", F(40)) + 52
    card(d, (W / 2 - pw / 2, 298, W / 2 + pw / 2, 362), fill=A(RED, k1), r=32)
    text(d, (W / 2, 330), "BẪY", 40, WHITE, alpha=k1)
    strike_q(d, 430, "“E cực đại thì B = 0 (lệch T/4)”", clamp((t - mk) / 0.4), k1)
    k0 = k1 * appear(t, 0.5, 0.45)                    # hinh co ngay khi phu de len
    for j, (x0, sh, lab, col) in enumerate(((60, math.pi / 2, "lệch T/4: sai", RED), (560, 0.0, "cùng pha: đúng", GREEN))):
        kk = k0 if j == 0 else k1 * appear(t, mk - 1.0, 0.45)
        card(d, (x0, 500, x0 + 460, 860), fill=A(WHITE, kk), outline=A(col, kk), r=24, w=4)
        mini_plot(d, (x0 + 10, 520, x0 + 450, 780), sh, kk)
        text(d, (x0 + 230, 820), lab, 40, col, alpha=kk)
    text(d, (W / 2, 940), "E đỏ liền · B xanh đứt", 40, NOTE, bold=False, alpha=k0)
    k3 = appear(t, M[1] - 0.1, 0.45)
    if k3 > 0:
        card(d, (40, 1060, 1040, 1560), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, 1120), "Chưa nói được", 48, NAVY, alpha=k3)
        lines = (("• Hình vẽ, không phải ảnh chụp",), ("• Không ai nhìn thấy E, B",),
                 ("• Vì sao tốc độ trong chân không", "  đúng bằng c"))
        for j, ls in enumerate(lines):
            kk = k3 * appear(t, M[1] + 0.2 + 0.4 * j, 0.4)
            for i, l in enumerate(ls): text(d, (90, 1225 + j * 100 + i * 56), l, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    chot_hoi(d, t, sc, "E, B cùng pha, vuông góc nhau\nvà vuông góc phương truyền",
             "Tại M, E = +0,5E₀ và đang tăng. B/B₀ lúc đó bằng bao nhiêu, chiều nào?", None)
    kh = appear(t, M[0] + 3.0, 0.5)                 # goi y hien tre: chi du kien
    if kh > 0:
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1350, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1440, "B dọc trục Oz", 46, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + s, "tick") for s in STOPS]
            + [(da["t0"] + da["M"][0] + 0.1, "ding"), (b["t0"] + b["M"][0], "buzz"),
               (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l12-dttruong-05", header="VẬT LÍ 12 · MÔ HÌNH", footer="Mô hình sóng điện từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Sóng điện từ tại M", draw=s_hook, tail=0.3, caps=[
   ("Sóng điện từ truyền dọc trục Ox.", 3.2),
   ("Dừng lại, tự đoán.", 6.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Ghi E, B tại M mỗi T/4.", 3.8),
   ("Sóng chạy tiếp theo phương Ox.", 5.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("B cũng cực đại. Đáp án B.", 3.6),
   ("Tại mỗi điểm, E và B luôn cùng pha.", 5.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Đúng hay sai?", 5.4),
   ("Chưa nói được gì?", 4.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video, trả lời.", 6.4)]),
])
