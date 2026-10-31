# Clip: tn-l10-thuchanhdl-03 - Bang dem khi nghieng nhe lam lech toc do do duoc (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-thuchanhdl-03.json:
#   tham_so: L = 1,20 m ; v cong 1 = 0,505 m/s ; x = 0,300 m ; h = 2/4/6 mm (max 8)
#   so_lieu_mau: h 2/4/6 mm -> a 0,0163/0,0327/0,049 m/s2 ; v_that 0,5146/0,524/0,5333 m/s ; lech 1,9/3,77/5,61 %
# Doc bang ve DUNG ti le that (6 mm tren 1,20 m ~ 4,6 px) -> nhin nhu phang; do cao h hien qua kinh lup phong to.
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (3 lan h = 2, 4, 6 mm; cong 2 o cho va cham)
#       -> Dap an "khoang 6 %" + cot lech -> Rut ra (a = g.h/L, v^2 = v1^2 + 2ax, p bi doc thieu) + chua noi duoc
#       -> Bay (vai mm khong dang ke; kiem bang mat) -> Chot + cau hoi tu nho lai (xe di LEN doc: lon hay nho hon?).
from engine import *

X0, X1 = 80, 1000
PXM = (X1 - X0) / 1.2                 # px / m doc bang
G1, G2, XE2 = 0.40, 0.70, 0.78        # cong 1, cong 2 (cho va cham, cach cong 1 x = 0,30 m), mep trai xe 2
CW = 0.12                             # chieu dai xe (m)
V1 = 0.505
DATA = {2: (0.0163, 0.5146, 1.9), 4: (0.0327, 0.524, 3.77), 6: (0.049, 0.5333, 5.61)}   # h: (a, v_that, lech)
RAIL = (148, 163, 184); RAIL_D = (100, 116, 139); LCD = (134, 239, 172)
def vn(x, n): return f"{x:.{n}f}".replace(".", ",")
def sx(s): return X0 + s * PXM

def lift_px(h): return h / 1000 * PXM            # do cao that cua dau ke tren hinh (px)
def ty(yb, h, s, right=False):                    # y mat bang tai vi tri s (m); dau trai ke cao (right=True: dau phai)
    L = lift_px(h)
    return yb - L * (s / 1.2 if right else 1 - s / 1.2)

def cart(d, yb, h, s, col=ORANGE, flag=True, right=False):
    x = sx(s); y = ty(yb, h, s, right); w = CW * PXM / 2
    if flag: d.rectangle([x - 6, y - 92, x + 6, y - 46], fill=NAVY)
    d.rounded_rectangle([x - w, y - 50, x + w, y - 4], radius=10, fill=col, outline=NAVY, width=3)

def gate_back(d, yb, h, s):
    x = sx(s); y = ty(yb, h, s)
    d.line([(x - 30, y + 36), (x - 30, y - 124)], fill=NAVY, width=7)
    d.line([(x + 30, y + 36), (x + 30, y - 124)], fill=NAVY, width=7)
def gate_front(d, yb, h, s):
    x = sx(s); y = ty(yb, h, s)
    d.line([(x - 34, y - 124), (x + 34, y - 124)], fill=NAVY, width=9)
    dot(d, x - 30, y - 70, 7, RED); dot(d, x + 30, y - 70, 7, RED)

def track(d, yb, h, right=False):
    floor = yb + 92
    d.line([(50, floor), (1030, floor)], fill=INK, width=4)
    for s in (0.06, 1.14):                                  # chan bang; chan phia ke dung tren tam dem
        x = sx(s); yt = ty(yb, h, s, right) + 28
        raised = (s < 0.6) != right
        bot = floor - (lift_px(h) if raised else 0)
        d.rectangle([x - 14, yt, x + 14, bot], fill=RAIL_D)
        if raised and h > 0: d.rectangle([x - 26, bot, x + 26, floor], fill=ORANGE)
    top = [(X0, ty(yb, h, 0, right)), (X1, ty(yb, h, 1.2, right))]
    d.polygon(top + [(X1, top[1][1] + 28), (X0, top[0][1] + 28)], fill=RAIL, outline=NAVY)
    for i in range(1, 46):
        s = i * 1.2 / 46; dot(d, sx(s), ty(yb, h, s, right) + 9, 3, RAIL_D)

def display(d, x, y, lab, val, hi=False):
    text(d, (x, y - 72), lab, 38, INK)
    card(d, (x - 108, y - 44, x + 108, y + 44), fill=NAVY, r=14)
    text(d, (x, y), val, 44, YELLOW if hi else LCD)

def magnifier(d, cx, cy, h, yb, alpha=1.0):
    """Kinh lup phong to chan trai (12 px/mm): tam dem day h."""
    lx = sx(0.06)
    d.line([(lx, yb + 92), (cx + 40, cy - 104)], fill=A(MUTED, alpha), width=3)
    d.ellipse([cx - 115, cy - 115, cx + 115, cy + 115], fill=A(WHITE, alpha), outline=A(MUTED, alpha), width=5)
    fl = cy + 58; hp = h * 12
    d.line([(cx - 100, fl), (cx + 100, fl)], fill=A(INK, alpha), width=4)
    if hp > 0: d.rectangle([cx - 58, fl - hp, cx + 58, fl], fill=A(ORANGE, alpha))
    d.rectangle([cx - 26, cy - 92, cx + 26, fl - hp], fill=A(RAIL_D, alpha))
    text(d, (cx + 140, cy - 4), f"h = {h} mm", 44, ORANGE, anchor="lm", alpha=alpha)
    text(d, (cx + 140, cy + 48), "(phóng to)", 38, MUTED, bold=False, anchor="lm", alpha=alpha)

def rig(d, h, s, r1, r2, hi2=False, dims=True):
    """Hinh chinh trong the y 265-1000: bang that ti le, hai cong, hai dong ho, kinh lup."""
    card(d, (40, 265, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    yb = 590
    display(d, sx(G1), 400, "cổng 1", r1)
    display(d, sx(G2), 400, "cổng 2", r2, hi=hi2)
    track(d, yb, h)
    gate_back(d, yb, h, G1); gate_back(d, yb, h, G2)
    cart(d, yb, h, XE2 + CW / 2, col=GRAY, flag=False)
    text(d, (sx(XE2) - 20, yb - 90), "xe đứng yên", 38, MUTED, anchor="lm")
    cart(d, yb, h, s)
    gate_front(d, yb, h, G1); gate_front(d, yb, h, G2)
    if dims:
        y = 735
        d.line([(sx(G1), y), (sx(G2), y)], fill=INK, width=3)
        for xx in (sx(G1), sx(G2)): d.line([(xx, y - 14), (xx, y + 14)], fill=INK, width=3)
        text(d, ((sx(G1) + sx(G2)) / 2, y + 40), "x = 0,30 m", 40, INK)
        text(d, (1010, 950), "băng dài 1,20 m", 40, INK, anchor="rm")
    magnifier(d, 215, 862, h, yb)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, 6, 0.55, "0,505", "?")
    arrow(d, (395, 650), (510, 650), NAVY, w=6, head=18)          # duoi bang: khong de cong
    text(d, (382, 650), "v", 40, NAVY, anchor="rm")
    text(d, (528, 650), "xuống dốc", 38, NAVY, anchor="lm")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1035 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 270, "Tốc độ ở cổng 2 lệch bao nhiêu % so với cổng 1?", 48, INK, maxw=880, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 480, 940, y0 + 494], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 480, 140 + 800 * (1 - p), y0 + 494], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (3 lan chay) ----------------
R0, RUN, SLOW, S0, SEND = 0.8, 2.6, 1.5, 0.10, XE2 - CW / 2
HS = (2, 4, 6)
def kin(h):
    """u: thoi gian that tinh tu luc qua cong 1. Tra ve (u0, u2, uend) ung voi s = S0, G2, SEND."""
    a = DATA[h][0]
    def u_at(s):   # s = G1 + V1 u + a u^2 / 2
        dd = s - G1
        return (-V1 + math.sqrt(V1 * V1 + 2 * a * dd)) / a
    return u_at(S0), u_at(G2), u_at(SEND)
def run_state(t):
    """-> (lan i, h, s xe, so cong 1, so cong 2, so hang da hien)."""
    i = int(clamp((t - R0) // RUN, 0, 2)) if t >= R0 else 0
    h = HS[i]; a = DATA[h][0]
    u0, u2, ue = kin(h)
    u = u0 + clamp(t - R0 - i * RUN, 0, 99) / SLOW
    u = min(u, ue)
    s = G1 + V1 * u + a * u * u / 2
    r1 = "0,505" if u >= 0 else "– – –"
    r2 = vn(DATA[h][1], 3) if u >= u2 else "– – –"
    rows = i + (1 if u >= u2 else 0) if t >= R0 else 0
    return i, h, s, r1, r2, rows

def table(d, rows, y0=1035, hl=None, alpha=1.0):
    card(d, (40, y0, 1040, y0 + 565), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    XS = (165, 405, 645, 900)
    for x, a_, b_ in zip(XS, ("h", "cổng 1", "cổng 2", "lệch"), ("(mm)", "(m/s)", "(m/s)", "(%)")):
        text(d, (x, y0 + 60), a_, 42, INK, alpha=alpha); text(d, (x, y0 + 110), b_, 38, MUTED, bold=False, alpha=alpha)
    d.line([(70, y0 + 150), (1010, y0 + 150)], fill=A(LIGHT, alpha), width=3)
    for j in range(rows):
        h = HS[j]; yy = y0 + 225 + j * 112
        if hl == j: d.rounded_rectangle([60, yy - 46, 1020, yy + 46], radius=20, fill=A((255, 247, 237), alpha))
        text(d, (XS[0], yy), str(h), 50, INK, alpha=alpha)
        text(d, (XS[1], yy), "0,505", 50, NAVY, alpha=alpha)
        text(d, (XS[2], yy), vn(DATA[h][1], 3), 50, NAVY, alpha=alpha)
        text(d, (XS[3], yy), vn(DATA[h][2], 1), 50, ORANGE, alpha=alpha)

def s_do(img, d, t, sc):
    i, h, s, r1, r2, rows = run_state(t)
    rig(d, h, s, r1, r2, hi2=r2[0] != "–")
    table(d, rows)

# ---------------- canh 3: Dap an + cot lech ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]; ka = appear(t, 0.15, 0.5)
    lab = "ĐÁP ÁN · khoảng 6 %"
    pw = tw(d, lab, F(38)) + 56
    card(d, (W / 2 - pw / 2, 250, W / 2 + pw / 2, 314), fill=A(NAVY, ka), r=32)
    text(d, (W / 2, 282), lab, 38, WHITE, alpha=ka)
    card(d, (40, 345, 1040, 520), fill=A((236, 253, 243), ka), outline=A(GREEN, ka), w=5)
    ctext(d, 432, "Kê 6 mm: cổng 2 nhanh hơn 5,6 %", 48, GREEN, maxw=920, alpha=ka)
    card(d, (40, 560, 1040, 1460), fill=WHITE, outline=LIGHT, w=3)
    bx0, bx1, by0, by1 = 210, 980, 650, 1300            # truc co dinh 0-6 %
    def yv(v): return by1 - v / 6 * (by1 - by0)
    d.line([(bx0, by0 - 20), (bx0, by1)], fill=INK, width=4); d.line([(bx0, by1), (bx1, by1)], fill=INK, width=4)
    for v in (0, 2, 4, 6):
        d.line([(bx0 - 12, yv(v)), (bx0, yv(v))], fill=INK, width=3)
        text(d, (bx0 - 24, yv(v)), str(v), 38, INK, anchor="rm")
    text(d, (bx0 - 24, by0 - 52), "lệch (%)", 38, MUTED, bold=False, anchor="lm")
    for j, h in enumerate(HS):
        k = ease((t - M[0] - 0.2 - 0.45 * j) / 0.6); cx = 360 + j * 240
        if k <= 0: continue
        v = DATA[h][2]
        d.rectangle([cx - 60, yv(v * k), cx + 60, by1], fill=ORANGE if h == 6 else (253, 186, 116))
        if k > 0.95: text(d, (cx, yv(v) - 34), vn(v, 1), 42, INK)
        text(d, (cx, by1 + 44), f"{h} mm", 40, INK)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 690), fill=WHITE, outline=LIGHT, w=3)
    A_, B_, C_ = (170, 400), (170, 600), (930, 600)        # tam giac phong to do doc
    d.polygon([A_, B_, C_], fill=(241, 245, 249)); d.line([A_, C_], fill=NAVY, width=7)
    d.line([A_, B_], fill=ORANGE, width=6); d.line([B_, C_], fill=GRAY, width=3)
    text(d, (150, 500), "h", 44, ORANGE, anchor="rm")
    text(d, (800, 515), "L", 44, NAVY)
    text(d, (550, 645), "độ dốc vẽ phóng to", 38, MUTED, bold=False)
    ka = appear(t, M[0] + 0.3, 0.4)
    if ka > 0:
        ux, uy = C_[0] - A_[0], C_[1] - A_[1]; n = math.hypot(ux, uy); ux, uy = ux / n, uy / n
        nx, ny = uy, -ux                                     # phap tuyen huong len, mui ten nam sat tren mat doc
        p0 = (380 + 30 * nx, 400 + 210 * 200 / 760 + 30 * ny); p1 = (p0[0] + 220 * ux, p0[1] + 220 * uy)
        arrow(d, p0, p1, A(RED, ka), w=7)
        text(d, (p1[0] + 10, p1[1] - 48), "a", 46, RED, alpha=ka)
    card(d, (40, 720, 1040, 1290), fill=WHITE, outline=NAVY, w=5)
    k1 = appear(t, M[0] + 0.6, 0.5)
    rich(d, W / 2, 785, "a = g·h/L = 9,8·0,006/1,20", 48, INK, alpha=k1)
    rich(d, W / 2, 865, "a ≈ 0,049 m/s^{2}", 48, INK, alpha=appear(t, M[0] + 1.1, 0.5))
    k2 = appear(t, M[0] + 1.7, 0.5)
    rich(d, W / 2, 955, "v^{2} = 0,505^{2} + 2a·0,30", 48, INK, alpha=k2)
    k3 = appear(t, M[0] + 2.4, 0.5)
    rich(d, W / 2, 1040, "v ≈ 0,533 m/s", 52, GREEN, alpha=k3)
    k4 = appear(t, M[0] + 3.0, 0.5)
    ctext(d, 1185, "p = m·v tính từ v cổng 1 sẽ thiếu ≈ 5,6 %", 42, ORANGE, maxw=900, alpha=k4)
    k5 = appear(t, M[1] + 2.4, 0.45)
    if k5 > 0:
        y0 = 1320 + (1 - k5) * 30
        card(d, (40, y0, 1040, y0 + 290), fill=A((254, 242, 242), k5), outline=A(RED, k5), w=5)
        text(d, (W / 2, y0 + 62), "Thí nghiệm chưa nói được", 44, NAVY, alpha=k5)
        ctext(d, y0 + 150, "ma sát, sức cản,", 46, RED, alpha=k5)
        ctext(d, y0 + 215, "băng võng ở giữa", 46, RED, alpha=k5)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.2, 0.45)
    card(d, (40, 265, 1040, 760), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, 290, W / 2 + pw / 2, 354), fill=A(RED, a1), r=32)
    text(d, (W / 2, 322), "BẪY", 38, WHITE, alpha=a1)
    q = "“Nghiêng vài mm, không đáng kể”"
    ks = clamp((t - 0.7) / 0.4); f = F(46); lw = tw(d, q, f); yy = 460
    text(d, (W / 2, yy), q, 46, mix(INK, MUTED, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.8 * a1), width=5)
    kk = appear(t, 1.1, 0.5)
    card(d, (110, 560, 970, 700), fill=A((236, 253, 243), kk), r=24)
    text(d, (W / 2, 630), "6 mm → lệch 5,6 %", 52, GREEN, alpha=kk)
    # kiem bang ngang: xe dung yen giua bang (h = 4 mm, that ti le) tu troi xuong
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 <= 0: return
    card(d, (40, 800, 1040, 1600), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
    yb = 1120; h = 4; a = DATA[h][0]
    tt = clamp(t - M[1] - 0.3, 0, 99); s = 0.45 + a * tt * tt / 2
    track(d, yb, h); cart(d, yb, h, s, flag=False)
    if tt > 0.6:
        x = sx(s) + CW * PXM / 2 + 14; y = ty(yb, h, s) - 26
        arrow(d, (x, y), (x + 90, y), A(GREEN, appear(t, M[1] + 1.0, 0.3)), w=6, head=18)
    k3 = appear(t, M[1] + 1.0, 0.3)
    ctext(d, 1340, "Xe tự trôi → băng nghiêng", 48, GREEN, alpha=k3)
    k4 = appear(t, M[1] + 1.8, 0.4)
    if k4 > 0:                                                # chan vit duoi chan trai bang
        vx, vy = sx(0.06), yb + 92 - lift_px(h)
        d.rectangle([vx - 30, vy - 4, vx + 30, vy + 8], fill=A(NAVY, k4))
        for dx in (-18, -6, 6, 18): d.line([(vx + dx, vy - 4), (vx + dx, vy + 8)], fill=A(GRAY, k4), width=3)
        arrow(d, (330, 1425), (vx + 16, vy + 22), A(ORANGE, k4), w=5, head=18)
        ctext(d, 1450, "chỉnh chân vít", 46, ORANGE, alpha=k4)

# ---------------- canh 6: Chot ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def body(d, t, k):
        if k < 0.02: return
        yb = 1110
        track(d, yb, 6, right=True); cart(d, yb, 6, 0.30, right=True)
        x = sx(0.30) + CW * PXM / 2 + 14; y = ty(yb, 6, 0.30, True) - 26
        arrow(d, (x, y), (x + 110, y), A(NAVY, k), w=6, head=18)
        text(d, (x + 140, y), "v", 44, NAVY, anchor="lm", alpha=k)
        cx, cy = 760, 1000                                    # kinh lup nho: dau PHAI ke cao
        d.line([(sx(1.14), yb + 92 - lift_px(6)), (cx + 40, cy + 48)], fill=A(MUTED, k), width=3)
        d.ellipse([cx - 62, cy - 62, cx + 62, cy + 62], fill=A(WHITE, k), outline=A(MUTED, k), width=4)
        d.line([(cx - 52, cy + 35), (cx + 52, cy + 35)], fill=A(INK, k), width=3)
        d.rectangle([cx - 34, cy - 7, cx + 34, cy + 35], fill=A(ORANGE, k))
        d.rectangle([cx - 15, cy - 54, cx + 15, cy - 7], fill=A(RAIL_D, k))
        text(d, (cx - 84, cy + 14), "h", 44, ORANGE, anchor="rm", alpha=k)
        kh = appear(t, M[0] + 2.5, 0.5)
        if kh <= 0: return
        card(d, (110, 1290, 970, 1540), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1345), "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1450, "Xe đứng yên trôi về đâu?", 42, ORANGE, maxw=800, alpha=kh)
    chot_hoi(d, t, sc, "Chỉnh băng thật ngang trước khi đo",
             "Xe đi lên dốc. Cổng 2 đọc lớn hay nhỏ hơn 0,505?", None, body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    for i in range(3):
        u0, u2, _ = kin(HS[i])
        out.append((do["t0"] + R0 + i * RUN + (u2 - u0) * SLOW, "tap"))      # cong 2 hien so
    out += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] + 2.4, "tap"),
            (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l10-thuchanhdl-03", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Thực hành động lượng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Băng đệm khí kê một đầu", draw=s_hook, tail=0.6, caps=[
   ("Băng kê cao 6 mm.", 3.4),
   ("Dừng video, chọn câu trả lời.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Thêm cổng 2 ngay chỗ va chạm.", 3.4),
   ("Kê cao dần: 2, 4, 6 mm.", 4.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Kê càng cao, lệch càng lớn.", 4.4)]),
 dict(key="rutra", title="Vì sao?", draw=s_rutra, tail=0.5, caps=[
   ("Xe xuống dốc nên nhanh dần.", 3.8),
   ("Mô hình đã bỏ qua gì?", 6.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Vài milimét cũng đủ lệch.", 3.4),
   ("Kiểm băng ngang: thả xe đứng yên.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Dừng video, tự trả lời.", 6.0)]),
])
