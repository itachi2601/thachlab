# Clip: tn-l12-dttruong-05 - Mo hinh song dien tu: E, B va phuong truyen tai diem M (ban 1, 12/11/2026;
# dung lai 26/11/2026 theo KE-HOACH-CAI-TIEN-CLIP viec 4 lo 32: cong --do-chu, chu >= 56 px khi ve, <= 50 s, Du doan khong nut A-D (K10)).
# Kho loai "vi_du" (mo hinh): clip ghi ro "mo hinh · hinh ve li thuyet", khong phai anh chup.
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-dttruong-05.json:
#   so_lieu_mau tai M: t = 0 -> E/E0 = 1, B/B0 = 1 | T/4 -> 0, 0 | T/2 -> -1, -1 | 3T/4 -> 0, 0 | T -> 1, 1
#   tham_so: c = 3.10^8 m/s. mo_hinh: E = E0.cos(2pi.t/T - 2pi.x/lambda) theo Oy, B cung pha theo Oz, truyen theo Ox.
# Hinh phoi canh (it net): Ox nam ngang sang phai, Oy thang dung len, Oz xien xuong-trai (huong ra phia nguoi xem)
#   -> he thuan: y x z = x, nen E (Oy) va B (Oz) cung pha thi song truyen theo +Ox (dung chieu mui ten).
# Du doan (quan niem sai hien_tuong_hay_sai[0]): Tai M, E dang cuc dai thi B ... -> dap an: B cung cuc dai.
# Cau THU NGHI (= cau_chot khung web, ca tu suy ghi trong so_lieu_mau.ghi_chu): E = +0,5E0 dang tang -> B = +0,5B0, chieu +Oz.
#   Khac Cau 6 cua bai (E triet tieu -> B?) va Cau 4.
# Font SF khong co glyph "⊥" -> viet "vuong goc" bang chu.
from engine import *

NOTE = (70, 75, 95)
OX, OY = 230, 600                 # goc O tren man hinh (khung 1080 x 1920)
XEND = 990                        # dau truc Ox
LAM = 380.0                       # buoc song tren hinh (px)
XM = 610                          # diem M
AE, AB = 165.0, 115.0             # bien do ve E (doc) va B (xien)
ZX, ZY = -0.3, 0.954              # huong +Oz tren man hinh (xuong-trai, huong ra phia nguoi xem)

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-dttruong-05.json")))
    assert [r[1:] for r in k["so_lieu_mau"]["hang"]] == [[1, 1], [0, 0], [-1, -1], [0, 0], [1, 1]]
    assert {p["ky_hieu"]: p for p in k["tham_so"]}["c"]["gia_tri"] == 3e8
_kiem_so()

def wave(x, ph):
    """E/E0 = B/B0 tai x, pha ph = 2pi.t/T (M o pha 0 khi t = 0)."""
    return math.cos(ph - 2 * math.pi * (x - XM) / LAM)

def pill(d, cx, cy, s, fill, alpha=1.0, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 38, cx + pw / 2, cy + 38), fill=A(fill, alpha), r=36)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem LIEN cao 70 px, ngan dan theo 10 nac (moi nac doi hinh du ro cho cong --do-chu)."""
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (190, y, 890, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (190, y, 190 + max(70, 700 * q), y + 70), fill=A(col, a), r=35)

def axes(d):
    d.line([(OX, OY), (XEND, OY)], fill=NAVY, width=4); arrow(d, (XEND - 30, OY), (XEND + 20, OY), NAVY, w=4, head=20)
    d.line([(OX, OY), (OX, OY - 230)], fill=NAVY, width=4); arrow(d, (OX, OY - 200), (OX, OY - 250), NAVY, w=4, head=20)
    zx, zy = OX + ZX * 200, OY + ZY * 200
    d.line([(OX, OY), (zx, zy)], fill=NAVY, width=4); arrow(d, (OX + ZX * 170, OY + ZY * 170), (zx, zy), NAVY, w=4, head=20)
    text(d, (XEND + 4, OY + 52), "x", 58, NAVY)
    text(d, (OX - 52, OY - 240), "y", 58, NAVY)
    text(d, (zx - 46, zy + 10), "z", 58, NAVY)
    text(d, (OX - 44, OY - 34), "O", 56, NAVY)
    arrow(d, (800, 300), (1010, 300), GREEN, w=8, head=24)                 # phuong truyen phia tren hinh
    text(d, (780, 300), "phương truyền", 56, GREEN, anchor="rm")

def curves(d, ph, showB=True):
    xs = [OX + k * 3 for k in range(int((XEND - 40 - OX) / 3) + 1)]
    for x in range(OX + 19, XEND - 40, 19):          # vach noi truc Ox -> duong song (cung mat cat x)
        w = wave(x, ph)
        d.line([(x, OY), (x, OY - AE * w)], fill=A(RED, 0.35), width=2)
        if showB: d.line([(x, OY), (x + ZX * AB * w, OY + ZY * AB * w)], fill=A(BLUE, 0.35), width=2)
    if showB:
        pts = [(x + ZX * AB * wave(x, ph), OY + ZY * AB * wave(x, ph)) for x in xs]
        d.line(pts, fill=BLUE, width=5, joint="curve")
    pts = [(x, OY - AE * wave(x, ph)) for x in xs]
    d.line(pts, fill=RED, width=5, joint="curve")

def at_M(d, ph, showB=True, qB=False):
    e = wave(XM, ph)
    for y in range(OY + 18, OY + 180, 18): d.line([(XM, y), (XM, y + 8)], fill=GRAY, width=3)   # duong dan toi nhan M
    dot(d, XM, OY, 13, NAVY)
    text(d, (XM + 40, OY + 200), "M", 58, NAVY, anchor="lm")
    sg = 1 if e > 0 else -1
    if abs(e) > 0.06:
        arrow(d, (XM, OY), (XM, OY - AE * e), RED, w=10, head=26)
        if showB: arrow(d, (XM, OY), (XM + ZX * AB * e, OY + ZY * AB * e), BLUE, w=10, head=26)
    if abs(e) > 0.35:                                 # nhan chi hien khi mui ten du dai
        text(d, (XM + 46, OY - AE * e + 10 * sg), "E", 58, RED)
        if showB: text(d, (XM + ZX * AB * e + 46, OY + ZY * AB * e + 16 * sg), "B", 58, BLUE)
    if qB:
        L = 50                                           # doan ngan chi phuong Oz, khong goi y do lon B
        bx, by = XM + ZX * L, OY + ZY * L
        d.line([(XM, OY), (bx, by)], fill=BLUE, width=6)
        card(d, (bx - 150, by - 10, bx - 30, by + 76), fill=WHITE, outline=BLUE, r=18, w=4)
        text(d, (bx - 90, by + 33), "B?", 58, BLUE)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    axes(d); curves(d, 0.0, showB=False); at_M(d, 0.0, showB=False, qB=True)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    seg_bar(d, y0 + 140, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, a)
    text(d, (W / 2, y0 + 330), "Tại M, E đang cực đại.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 440), "Lúc đó B tại M ra sao?", 62, PURPLE, alpha=a)

# ---------------- canh 2: Tien hanh ----------------
STOPS = [1.0, 1.9, 3.3, 4.7, 6.1]          # moc hien hang 0, T/4, T/2, 3T/4, T
MOVES = [(1.2, 1.9), (2.6, 3.3), (4.0, 4.7), (5.4, 6.1)]
ROWS = (("0", 1, 1), ("T/4", 0, 0), ("T/2", -1, -1), ("3T/4", 0, 0), ("T", 1, 1))

def ph_at(t):
    q = 0.0
    for a, b in MOVES:
        if t >= b: q += 1
        elif t > a: q += ease((t - a) / (b - a))
    return q * math.pi / 2

def nv(v): return "0" if v == 0 else ("+1" if v > 0 else "−1")

def table(d, y0, ks, cur=-1):
    rh = 68; h = 90 + rh * 5
    card(d, (40, y0, 1040, y0 + h), fill=WHITE, outline=LIGHT, w=3)
    for x, s, c in ((250, "t", NOTE), (560, "E/E₀", RED), (840, "B/B₀", BLUE)): text(d, (x, y0 + 46), s, 58, c)
    d.line([(70, y0 + 88), (1010, y0 + 88)], fill=LIGHT, width=3)
    for j, (r, k) in enumerate(zip(ROWS, ks)):
        if k <= 0: continue
        yy = y0 + 88 + rh * (j + 0.5) + 2
        if j == cur: card(d, (60, yy - rh / 2 + 4, 1020, yy + rh / 2 - 4), fill=A((255, 247, 237), k), r=16)
        text(d, (250, yy), r[0], 58, INK, alpha=k)
        text(d, (560, yy), nv(r[1]), 58, RED, alpha=k)
        text(d, (840, yy), nv(r[2]), 58, BLUE, alpha=k)
    return h

def s_do(img, d, t, sc):
    ph = ph_at(t)
    axes(d); curves(d, ph); at_M(d, ph)
    text(d, (W / 2, 925), "mô hình · hình vẽ lí thuyết", 56, NOTE, bold=False)
    text(d, (W / 2, 1010), "E₀, B₀: giá trị cực đại", 56, INK)
    ks = [appear(t, s, 0.35) for s in STOPS]
    cur = max([i for i, s in enumerate(STOPS) if t >= s] or [-1])
    table(d, 1075, ks, cur)

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, W / 2, 320, "ĐÁP ÁN: B cũng cực đại", NAVY, appear(t, M[0] + 0.1, 0.4))
    x0, x1 = 230, 990
    X = lambda u: x0 + u * (x1 - x0)                 # u = t/T tu 0 den 1
    kg = appear(t, 0.5, 0.5)
    for yc, lab, col in ((560, "E", RED), (860, "B", BLUE)):
        d.line([(x0, yc), (x1 + 10, yc)], fill=A(NAVY, kg), width=3)
        text(d, (x0 - 70, yc), lab, 62, col, alpha=kg)
        pts = [(X(u / 100), yc - 95 * math.cos(2 * math.pi * u / 100)) for u in range(101)]
        k = appear(t, 0.6 if lab == "E" else 1.2, 1.2)
        n = max(2, int(101 * k))
        d.line(pts[:n], fill=A(col, kg), width=7, joint="curve")
    kd = appear(t, M[1] + 0.2, 0.4)
    if kd > 0:
        for u in (0, 0.25, 0.5, 0.75, 1.0):
            for y in range(440, 980, 26): d.line([(X(u), y), (X(u), y + 13)], fill=A(GREEN, kd), width=4)
        for u, s in ((0, "0"), (0.25, "T/4"), (0.5, "T/2"), (0.75, "3T/4"), (1.0, "T")): text(d, (X(u), 1030), s, 56, NOTE, alpha=kd)
        text(d, (1040, 905), "t", 60, NOTE, alpha=kd)
        card(d, (60, 1110, 1020, 1270), fill=A((236, 253, 243), kd), outline=A(GREEN, kd), r=28, w=5)
        text(d, (W / 2, 1190), "Cùng cực đại, cực tiểu, bằng 0", 60, GREEN, alpha=kd)

# ---------------- canh 4: Rut ra ----------------
def right_mark(d, c, u, v, s, col):
    """Dau goc vuong giua hai huong u, v (vecto don vi tren man hinh, da chieu phoi canh)."""
    p1 = (c[0] + u[0] * s, c[1] + u[1] * s); p3 = (c[0] + v[0] * s, c[1] + v[1] * s)
    p2 = (p1[0] + v[0] * s, p1[1] + v[1] * s)
    d.line([p1, p2, p3], fill=col, width=4)

def s_rutra(img, d, t, sc):
    M = sc["M"]; k = appear(t, 0.2, 0.5)
    card(d, (40, 270, 1040, 980), fill=A(WHITE, k), outline=A(LIGHT, k), w=3)
    cx, cy = 360, 680                                  # ba phuong vuong goc (phoi canh nhu hinh truc Oxyz)
    uE, uB, uX = (0, -1), (ZX, ZY), (1, 0)
    for u, v in ((uE, uX), (uE, uB), (uB, uX)): right_mark(d, (cx, cy), u, v, 40, A(NAVY, k))
    arrow(d, (cx, cy), (cx, cy - 300), A(RED, k), w=10, head=28); text(d, (cx + 50, cy - 280), "E", 64, RED, alpha=k)
    arrow(d, (cx, cy), (cx + ZX * 250, cy + ZY * 250), A(BLUE, k), w=10, head=28)
    text(d, (cx + ZX * 250 + 64, cy + ZY * 250 - 20), "B", 64, BLUE, alpha=k)
    arrow(d, (cx, cy), (cx + 420, cy), A(GREEN, k), w=10, head=28)
    text(d, (cx + 290, cy + 60), "phương truyền", 56, GREEN, alpha=k)
    ks = appear(t, 2.4, 0.45)
    if ks > 0:
        card(d, (140, 1030, 940, 1180), fill=A((236, 253, 243), ks), outline=A(GREEN, ks), r=28, w=5)
        text(d, (W / 2, 1105), "Sóng ngang", 64, GREEN, alpha=ks)
    kc = appear(t, M[1] + 1.9, 0.45)
    if kc > 0:
        card(d, (140, 1230, 940, 1380), fill=A(WHITE, kc), outline=A(NAVY, kc), r=28, w=5)
        text(d, (W / 2, 1305), "c = 3·10⁸ m/s", 64, NAVY, alpha=kc)

# ---------------- canh 5: Bay + chua noi duoc ----------------
def wide_plot(d, y0, y1, shift, alpha):
    """Hai duong E (do), B (xanh) trai rong khung; vach dut tai dinh E de thay dinh B trung hay lech."""
    x0, x1 = 150, 1000; yc = (y0 + y1) / 2; amp = (y1 - y0) * 0.40
    X = lambda u: x0 + u * (x1 - x0) / 1.25           # 1,25 chu ki
    d.line([(x0 - 10, yc), (x1 + 10, yc)], fill=A(NAVY, alpha), width=3)
    for u in (0.0, 1.0):
        for y in range(int(y0), int(y1), 24): d.line([(X(u), y), (X(u), y + 12)], fill=A(GRAY, alpha), width=4)
    e = [(X(u / 100), yc - amp * math.cos(2 * math.pi * u / 100)) for u in range(126)]
    b = [(X(u / 100), yc - amp * math.cos(2 * math.pi * u / 100 - shift)) for u in range(126)]
    d.line(b, fill=A(BLUE, alpha), width=8 if shift else 18, joint="curve")   # cung pha: B to hon, vien xanh quanh E
    d.line(e, fill=A(RED, alpha), width=8 if shift else 7, joint="curve")
    text(d, (95, yc - amp + 10), "E", 66, RED, alpha=alpha)
    text(d, (95, yc + (amp - 10 if shift else 70)), "B", 66, BLUE, alpha=alpha)

def s_bay(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, 0.2, 0.4)
    card(d, (40, 270, 1040, 1240), fill=A(WHITE, k1), outline=A(RED, k1), w=6)
    pill(d, W / 2, 340, "BẪY", RED, k1)
    text(d, (W / 2, 450), "“E cực đại thì B = 0”?", 60, INK, alpha=k1)
    ks = appear(t, M[1] + 0.2, 0.45)
    for j, (ya, sh, lab, verdict, col) in enumerate(((500, math.pi / 2, "lệch T/4", "SAI", RED),
                                                      (860, 0.0, "cùng pha", "ĐÚNG", GREEN))):
        kk = k1 if j == 0 else ks
        if kk <= 0: continue
        wide_plot(d, ya, ya + 270, sh, kk)
        text(d, (90, ya + 310), lab, 62, INK, anchor="lm", alpha=kk)
        if ks > 0: text(d, (990, ya + 310), verdict, 66, col, anchor="rm", alpha=ks)
    k3 = appear(t, M[2] + 0.2, 0.45)
    if k3 > 0:
        card(d, (40, 1270, 1040, 1440), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, 1355), "Vì sao tốc độ đúng bằng c?", 60, NAVY, alpha=k3)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
DORANGE = (154, 52, 18)
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 260, 1040, 1500), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 340, "THỬ NGHĨ", ORANGE, k1)
    seg_bar(d, 420, t, 0.8, sc["T"] - 0.2, ORANGE, k1)
    text(d, (W / 2, 580), "Tại M: E = +0,5E₀, đang tăng.", 60, INK, alpha=k1)
    text(d, (W / 2, 680), "B bằng bao nhiêu B₀, chiều nào?", 60, DORANGE, alpha=k1)
    ox, oy = 470, 1000                                 # truc nho: chua ve vecto B
    for (dx, dy), lab, lx, ly in (((0, -170), "y", -50, 15), ((250, 0), "x", 25, 45), ((ZX * 170, ZY * 170), "z", -55, -15)):
        arrow(d, (ox, oy), (ox + dx, oy + dy), A(NAVY, k1), w=6, head=24)
        text(d, (ox + dx + lx, oy + dy + ly), lab, 66, NAVY, alpha=k1)
    arrow(d, (ox, oy), (ox, oy - 100), A(RED, k1), w=12, head=28); text(d, (ox + 50, oy - 75), "E", 66, RED, alpha=k1)
    dot(d, ox, oy, 11, A(NAVY, k1))
    kh = appear(t, 3.2, 0.5)                         # goi y hien tre: chi du kien
    if kh > 0:
        card(d, (110, 1230, 970, 1400), fill=A((255, 237, 213), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1315), "Gợi ý: B nằm dọc trục Oz", 62, DORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
            + [(do["t0"] + s, "tick") for s in STOPS]
            + [(da["t0"] + da["M"][0] + 0.1, "ding"), (b["t0"] + b["M"][0], "buzz"),
               (e["t0"] + 0.15, "open")])

SCENES = [
 dict(key="hook", title="Sóng điện từ tại M", draw=s_hook, tail=0.3, caps=[
   ("Sóng truyền dọc trục Ox.", 3.0),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Ghi E, B tại M mỗi T/4.", 3.4),
   ("Đọc tiếp đến hết chu kì T.", 4.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.2, caps=[
   ("Tại M, B cũng đạt cực đại.", 3.4),
   ("E và B luôn cùng pha.", 3.2)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.4, caps=[
   ("Ba phương đôi một vuông góc.", 3.0),
   ("Truyền được cả trong chân không.", 3.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.2, caps=[
   ("Đúng hay sai?", 3.0),
   ("Sai: hai đỉnh trùng nhau.", 3.2),
   ("Mô hình chưa giải thích được.", 2.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=3.2, caps=[
   ("Sóng điện từ là sóng ngang.", 3.6)]),
]

CLIP = dict(id="tn-l12-dttruong-05", header="VẬT LÍ 12 · MÔ HÌNH", footer="Mô hình sóng điện từ · thachlab.id.vn",
            cues=_cues, scenes=SCENES)
