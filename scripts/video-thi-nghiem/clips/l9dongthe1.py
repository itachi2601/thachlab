# Clip: tn-l9-dongthe-01 - Vien bi lan xuong mang nghieng va vao khuc go (KHTN 9, 5/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-dongthe-01.json:
#   so_lieu_mau (m g, h cm, s cm): 50 10 4,0 ; 50 20 8,0 ; 100 10 8,0   (ghi_chu: minh hoa, chua phai so do that)
#   tham_so: m 0,02-0,2 kg ; h 0,05-0,3 m (buoc 0,05) -> cau THU NGHI dung h = 15 cm (chua hien), bi 50 g.
#   mo_hinh.gia_thiet: chi dung de so sanh dinh tinh -> o "chua noi duoc": dong nang tang may lan chua do.
# Bo cuc (khac dongluong2 L10 = 2 mang nho + bang m,h,v,p): MOT mang dang ray tren chan do, cot thuoc do cao rieng,
#   thuoc cm duoi san do s, va BIEU DO COT NGANG s moi lan (thanh dai ra dong pha voi khuc go truot).
# Canh: Du doan (thay bi 50 g -> 100 g cung 10 cm; chi cau hoi + hinh, K10) -> Tien hanh (3 lan, ĐÁP ÁN · xa hon)
#   -> Vi sao (bi dang chay day duoc go = dong nang; nang hon, nhanh hon) -> Bay (chi toc do quan trong ✗)
#   + Chua noi duoc -> Chot + THU NGHI (50 g tha 15 cm: trong khoang 4,0-8,0 cm, khong ngoai suy).
# Lua chon Du doan (o khung web): A. Gan hon lan bi 50 g · B. Bang lan bi 50 g · C. Xa hon lan bi 50 g (dung)
#   · D. Khuc go khong nhuc nhich.  Lop 9: khong dung "dong luong", khong cong thuc dong nang (TN sau cua bai).
from engine import *

WOOD = (214, 170, 118); WOOD_D = (140, 96, 52); STEEL = (148, 163, 184); STEEL_D = (51, 65, 85)
RAIL = (203, 213, 225); RAIL_D = (71, 85, 105); RULER = (253, 246, 200); RULER_D = (170, 150, 60)
DRED = (185, 28, 28); OR_BG = (255, 237, 213)

# ---------------- hinh hoc (toa do khung 1080x1920) ----------------
Y0 = 820                         # mat san
PXH = 14                         # 1 cm do cao = 14 px
RB_X, RT_X, RT_H = 640, 330, 300  # chan mang, dau mang (x), do cao dau mang (px)
UX, UY = (RB_X - RT_X) / math.hypot(RB_X - RT_X, RT_H), RT_H / math.hypot(RB_X - RT_X, RT_H)   # huong xuong doc
NX, NY = UY, -UX                 # phap tuyen phia tren mat mang
POLE_X = 150                     # cot thuoc do cao
XB, BW, BH = 690, 92, 84         # mep sau khuc go luc dau, rong, cao
PXCM = 30                        # thuoc san: 1 cm = 30 px
ACC = 700.0                      # gia toc doc mang (px/s2): tha 20 cm mat ~1,1 s
SLIDE, HOLD = 0.9, 0.6
RUNS = [(50, 10, 4.0), (50, 20, 8.0), (100, 10, 8.0)]       # so_lieu_mau
def vn(x): return f"{x:.1f}".replace(".", ",")
def rad(g): return 21 if g == 50 else 27                     # bi thep: r ti le can bac 3 cua m

def surf(hcm):
    hp = hcm * PXH; return RB_X - hp * UX / UY, Y0 - hp

def ball_path(g, hcm, tau):
    """(x, y tam bi, da cham go, thoi diem cham) sau khi tha tau giay."""
    r = rad(g); sx, sy = surf(hcm); x0, y0 = sx + r * NX, sy + r * NY
    L = ((Y0 - r) - y0) / UY; t1 = math.sqrt(2 * L / ACC); v1 = ACC * t1
    x1 = x0 + L * UX; t2 = max(0.0, (XB - r) - x1) / v1; ti = t1 + t2
    if tau <= 0: return x0, y0, False, ti
    if tau < t1: s = 0.5 * ACC * tau * tau; return x0 + s * UX, y0 + s * UY, False, ti
    if tau < ti: return x1 + v1 * (tau - t1), Y0 - r, False, ti
    return XB - r, Y0 - r, True, ti

def run_len(i):
    g, h, _ = RUNS[i]; return ball_path(g, h, 0)[3] + SLIDE + HOLD

def slide(u, D): u = clamp(u / SLIDE); return D * (1 - (1 - u) ** 2)

# ---------------- ve dung cu ----------------
def ruler(d):
    y = Y0 + 12
    d.rectangle([XB - 14, y, XB + 10.6 * PXCM, y + 44], fill=RULER, outline=RULER_D, width=2)
    for k in range(11):
        x = XB + k * PXCM; L = 30 if k % 2 == 0 else 16
        d.line([(x, y), (x, y + L)], fill=NAVY, width=3 if L == 30 else 2)
        if k % 2 == 0: text(d, (x, y + 76), str(k), 40, INK)
    text(d, (XB - 40, y + 76), "cm", 40, MUTED, bold=False, anchor="rm")

def pole(d, hl=None):
    d.rectangle([POLE_X - 7, Y0 - 330, POLE_X + 7, Y0], fill=RULER, outline=RULER_D, width=2)
    for hcm in (10, 20):
        y = Y0 - hcm * PXH; on = hl == hcm
        d.line([(POLE_X - 16, y), (POLE_X + 16, y)], fill=NAVY, width=4)
        text(d, (POLE_X + 26, y - 30), f"{hcm} cm", 40, ORANGE if on else INK, anchor="lm")
        if on:   # net dut tu cot toi diem tha
            sx, _ = surf(hcm)
            for xx in range(POLE_X + 20, int(sx) - 6, 18):
                d.line([(xx, y), (min(xx + 9, sx), y)], fill=ORANGE, width=3)

def ramp(d):
    sx0, sy0 = RT_X, Y0 - RT_H
    d.line([(sx0 + 30, sy0 + 30), (sx0 + 30, Y0)], fill=RAIL_D, width=8)                 # chan do
    th = 20
    d.polygon([(sx0, sy0), (RB_X, Y0), (RB_X - th / UY, Y0), (sx0 - th * NX, sy0 - th * NY)], fill=RAIL, outline=RAIL_D)
    d.line([(sx0, sy0), (RB_X, Y0)], fill=RAIL_D, width=5)

def floor(d):
    d.line([(60, Y0), (1020, Y0)], fill=NAVY, width=6)

def block(d, dx, ghost=False):
    x0 = XB + dx
    if ghost:
        for yy in range(int(Y0 - BH), Y0, 16):
            d.line([(XB, yy), (XB, yy + 8)], fill=GRAY, width=3)
    d.rectangle([x0, Y0 - BH, x0 + BW, Y0], fill=WOOD, outline=WOOD_D, width=4)
    for k in (1, 2):
        d.line([(x0 + 10, Y0 - BH * k / 3), (x0 + BW - 10, Y0 - BH * k / 3)], fill=WOOD_D, width=2)

def ball(d, x, y, g, label=True):
    r = rad(g)
    d.ellipse([x - r, y - r, x + r, y + r], fill=STEEL, outline=STEEL_D, width=4)
    d.ellipse([x - r * 0.55, y - r * 0.6, x - r * 0.1, y - r * 0.15], fill=A(WHITE, 0.85))
    if label: text(d, (x, y - r - 34), f"{g} g", 40, NAVY)

def s_arrow(d, dx):
    if dx < 30: return
    ya = Y0 - BH - 34
    arrow(d, (XB + 4, ya), (XB + dx, ya), GREEN, w=5, head=16)
    text(d, (XB + dx / 2, ya - 32), "s", 42, GREEN)

def rig(d, g, hcm, bx, by, dx, ghost=False, hl=None, label=True):
    card(d, (40, 360, 1040, 930), fill=WHITE, outline=LIGHT, w=3)
    pole(d, hl); ramp(d); floor(d); ruler(d)
    block(d, dx, ghost); s_arrow(d, dx)
    ball(d, bx, by, g, label)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    x, y, _, _ = ball_path(50, 10, 0)
    rig(d, 50, 10, x, y, 0, hl=10)
    k0 = appear(t, 0.6, 0.4)                                  # mui ten chieu lan
    if k0 > 0:
        p, q = surf(16), surf(4)
        arrow(d, (p[0] + 70 * NX, p[1] + 70 * NY), (q[0] + 70 * NX, q[1] + 70 * NY), A(BLUE, k0), w=5, head=18)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 975 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "Dự đoán", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "Dự đoán", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 150), "Cùng thả từ 10 cm.", 46, NAVY, alpha=a)
    text(d, (W / 2, y0 + 212), "Thay bi 50 g bằng bi 100 g,", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 274), "khúc gỗ bị đẩy đi thế nào?", 46, INK, alpha=a)
    # hai vien bi phong to (cung mau, chi khac co theo khoi luong)
    for cx, g in ((380, 50), (700, 100)):
        r = rad(50) * 1.8; cy = y0 + 385
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=A(STEEL, a), outline=A(STEEL_D, a), width=4)
        text(d, (cx, cy + r + 34), f"{g} g", 40, NAVY, alpha=a)
    arrow(d, (470, y0 + 385), (600, y0 + 385), A(MUTED, a), w=5, head=18)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        q = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 522, 940, y0 + 536], radius=7, fill=A(LIGHT, a))
        if q < 1: d.rounded_rectangle([140, y0 + 522, 140 + 800 * (1 - q), y0 + 536], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
CAP_DO = [("Thả cao dần: 10 cm rồi 20 cm.", 5.5), ("Giữ 10 cm, thay bi nặng hơn.", 3.8)]
R0 = 0.8
def starts():
    s1 = R0; s2 = s1 + run_len(0)
    m1 = 0.4 + max(CAP_DO[0][1], cap_dur(CAP_DO[0][0]))
    s3 = max(s2 + run_len(1), m1 + 0.4)
    return [s1, s2, s3]
ST = starts()
STOP3 = ST[2] + ball_path(*RUNS[2][:2], 0)[3] + SLIDE
BADGE = STOP3 + 0.4

def state(i, t):
    """(bi x, y, go dx, da cham, da dung) cua lan i luc t."""
    g, h, s = RUNS[i]; tau = t - ST[i]
    x, y, hit, ti = ball_path(g, h, tau)
    dx = slide(tau - ti, s * PXCM) if hit else 0.0
    if hit: x += 0.3 * dx
    return x, y, dx, hit, tau >= ti + SLIDE

def cur_run(t):
    c = 0
    for i, s in enumerate(ST):
        if t >= s - 0.3: c = i
    return c

BX0, BSC = 400, 54                 # bieu do cot: goc x, px moi cm
def bars(d, t, y=965, hl=(), alpha=1.0, rows=(0, 1, 2), title=True, gap=115):
    top = y + (100 if title else 20); hh = top - y + gap * len(rows) + 20
    card(d, (40, y, 1040, y + hh), fill=A(WHITE, alpha), outline=A(NAVY, alpha), w=4)
    if title: text(d, (W / 2, y + 55), "s: quãng khúc gỗ bị đẩy đi", 42, INK, alpha=alpha)
    for j, i in enumerate(rows):
        g, h, s = RUNS[i]; yy = top + gap / 2 + gap * j
        if t < ST[i] - 0.3: continue
        hb = min(46, gap * 0.45)
        if i in hl: d.rounded_rectangle([60, yy - hb, 1020, yy + hb], radius=18, fill=A(OR_BG, alpha))
        text(d, (80, yy), f"{g} g · {h} cm", 40, NAVY, anchor="lm", alpha=alpha)
        _, _, dx, hit, done = state(i, t)
        L = dx / PXCM * BSC
        d.line([(BX0, yy - hb + 6), (BX0, yy + hb - 6)], fill=A(MUTED, alpha), width=3)
        if L > 2: d.rounded_rectangle([BX0, yy - 22, BX0 + L, yy + 22], radius=10, fill=A(GREEN, alpha))
        if done: text(d, (BX0 + L + 18, yy), f"{vn(s)} cm", 40, GREEN, anchor="lm", alpha=alpha)

def s_do(img, d, t, sc):
    i = cur_run(t); g, h, _ = RUNS[i]
    x, y, dx, hit, done = state(i, t)
    rig(d, g, h, x, y, dx, ghost=dx > 0, hl=h)
    ka = appear(t, BADGE, 0.4)
    bars(d, t, hl=(0, 2) if ka > 0.5 else ())
    if ka > 0:
        s_ = "ĐÁP ÁN · xa hơn bi 50 g"; pw = tw(d, s_, F(44)) + 70
        card(d, (W / 2 - pw / 2, 1435, W / 2 + pw / 2, 1530), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), r=26, w=4)
        text(d, (W / 2, 1483), s_, 44, GREEN, alpha=ka)

# ---------------- canh 3: Vi sao ----------------
def s_rut(img, d, t, sc):
    M = sc["M"]
    x, y, _, _ = ball_path(50, 20, 99)
    rig(d, 50, 20, x, y, 0, label=False)
    k0 = appear(t, 0.5, 0.4)
    if k0 > 0:
        arrow(d, (XB + BW + 14, Y0 - BH / 2), (XB + BW + 180, Y0 - BH / 2), A(BLUE, k0), w=8, head=24)
        text(d, (XB + BW + 100, Y0 - BH / 2 - 44), "đẩy", 42, BLUE, alpha=k0)
    k1 = appear(t, M[0] + 0.9, 0.45)
    if k1 > 0:
        y1 = 955 + (1 - k1) * 30
        card(d, (40, y1, 1040, y1 + 170), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        text(d, (W / 2, y1 + 55), "Động năng", 54, GREEN, alpha=k1)
        text(d, (W / 2, y1 + 125), "năng lượng do chuyển động", 42, INK, alpha=k1)
    kb = appear(t, 0.3, 0.4)                                  # bieu do nho ca ba lan (giu so lieu tren man)
    hl = tuple(i for j, i in enumerate((1, 2)) if t >= M[1] + 0.2 + 0.6 * j)
    bars(d, 99, y=1150, hl=hl, title=False, gap=76, alpha=kb)
    for j, (lab, yy) in enumerate((("Lần 2: thả cao hơn", 1440), ("Lần 3: bi nặng hơn", 1510))):
        k = appear(t, M[1] + 0.2 + 0.6 * j, 0.4)
        text(d, (W / 2, yy), lab, 44, ORANGE, alpha=k)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a = appear(t, M[0] - 0.05, 0.4)
    if a > 0:
        card(d, (40, 300, 1040, 770), fill=A(WHITE, a), outline=A(DRED, a), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, 326, W / 2 + pw / 2, 390), fill=A(DRED, a), r=32)
        text(d, (W / 2, 358), "BẪY", 40, WHITE, alpha=a)
        q1, q2 = "“Chỉ tốc độ quan trọng,", "bi nặng nhẹ như nhau”"
        text(d, (W / 2, 470), q1, 48, INK, alpha=a); text(d, (W / 2, 534), q2, 48, INK, alpha=a)
        ks = clamp((t - (M[0] + 2.1)) / 0.4)
        if ks > 0:
            for yy, s in ((470, q1), (534, q2)):
                lw = tw(d, s, F(48)); xl = W / 2 - lw / 2 - 6
                d.line([(xl, yy + 2), (xl + (lw + 12) * ks, yy + 2)], fill=A(DRED, a), width=6)
            text(d, (960, 500), "✗", 80, DRED, alpha=a * ks)
        kv = appear(t, M[0] + 2.6, 0.4)
        ctext(d, 700, "✓ Cùng 10 cm: bi nặng đẩy xa hơn", 46, GREEN, maxw=900, alpha=a * kv)
        bars(d, 99, y=800, rows=(0, 2), title=False, alpha=a)      # hinh bay hien cung chu: lan 1 vs lan 3
    if k2 > 0:
        y1 = 1110 + (1 - k2) * 30
        card(d, (40, y1, 1040, y1 + 320), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y1 + 62), "Chưa nói được gì?", 46, NAVY, alpha=k2)
        for j, s in enumerate(("• Tăng mấy lần: chưa đo", "• Số liệu minh hoạ")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (90, y1 + 160 + j * 92), s, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 300, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 395), "Càng nặng, thả càng cao", 52, GREEN, alpha=k0)
    text(d, (W / 2, 470), "→ động năng càng lớn", 52, GREEN, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 620, 1040, 1240), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 682), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ka = appear(t, M[0] + 0.4, 0.5)
    text(d, (W / 2, 800), "Bi 50 g thả từ 15 cm.", 48, NAVY, alpha=ka)
    text(d, (W / 2, 870), "Khúc gỗ đi khoảng bao xa?", 48, INK, alpha=ka)
    kh = appear(t, M[0] + 2.5, 0.5)                                       # goi y tre 2,5 s
    if kh <= 0: return
    card(d, (110, 960, 970, 1200), fill=A((255, 247, 237), kh), r=24)
    text(d, (W / 2, 1022), "Gợi ý", 40, MUTED, bold=False, alpha=kh)
    text(d, (W / 2, 1110), "Trả lời dạng: từ … đến … cm", 46, ORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = (sc[k] for k in ("hook", "do", "rut", "bay", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding")]
    out += [(do["t0"] + ST[i] + ball_path(*RUNS[i][:2], 0)[3], "tap") for i in range(3)]   # bi cham khuc go
    out += [(do["t0"] + BADGE, "ding"), (r["t0"] + r["M"][0] + 0.9, "tap"),
            (b["t0"] + b["M"][0], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

DO_TAIL = max(0.6, BADGE + 2.4 - (0.4 + sum(max(dd, cap_dur(c)) for c, dd in CAP_DO)))

CLIP = dict(id="tn-l9-dongthe-01", header="KHTN 9 · THÍ NGHIỆM", footer="Động năng · thachlab.id.vn", cues=_cues, scenes=[
 dict(key="hook", title="Viên bi và khúc gỗ", draw=s_hook, tail=0.6, caps=[
   ("Bi lăn xuống máng, va khúc gỗ.", 3.8),
   ("Dừng video, tự đoán.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=DO_TAIL, caps=list(CAP_DO)),
 dict(key="rut", title="Vì sao khúc gỗ đi?", draw=s_rut, tail=1.8, caps=[
   ("Bi đang chạy đẩy được khúc gỗ.", 3.8),
   ("Vậy động năng lớn khi nào?", 3.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.9, caps=[
   ("Bi nặng hay nhẹ có quan trọng?", 4.4),
   ("Giới hạn của thí nghiệm.", 4.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự nghĩ.", 6.2)]),
])
