# Clip: tn-l12-boylecharles-01 - Nen khi trong xilanh kin, nhiet do khong doi thi pV khong doi
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-boylecharles-01.json (so_lieu_mau, tham_so).
# Ban 2 (27/10/2026): ~46 s, xilanh dung + ap ke co vach so, du doan 3 lua chon cung kieu,
# bang so lieu, do thi p-V + cot p.V, co che va cham, gioi han + bay nen nhanh.
import random
from engine import *

# Pillow 11 bo qua kenh alpha khi ve chu (ImageDraw "RGBA" tren anh RGB) -> chu khong mo dan duoc.
# Viet lai text/ctext trong clip: alpha < 1 thi ve chu len mat na L roi dan mau qua mat na.
_IMG = [None]
def text(d, xy, s, size, color=INK, bold=True, anchor="mm", alpha=1.0):
    if alpha <= 0.02: return
    f = F(size, bold); col = tuple(color[:3])
    if alpha >= 0.98 or _IMG[0] is None:
        d.text(xy, s, font=f, fill=col, anchor=anchor); return
    l, t, r, b = d.textbbox(xy, s, font=f, anchor=anchor); l, t, r, b = int(l) - 3, int(t) - 3, int(r) + 3, int(b) + 3
    m = Image.new("L", (r - l, b - t), 0)
    ImageDraw.Draw(m).text((xy[0] - l, xy[1] - t), s, font=f, fill=int(255 * alpha), anchor=anchor)
    _IMG[0].paste(col, (l, t, r, b), m)
def ctext(d, y, s, size, color=INK, bold=True, maxw=940, alpha=1.0, lh=1.22):
    ls = wrap(d, s, F(size, bold), maxw); y0 = y - (len(ls) - 1) * size * lh / 2
    for i, l in enumerate(ls): text(d, (W / 2, y0 + i * size * lh), l, size, color, bold, alpha=alpha)

ROWS = [(8.0, 100), (6.0, 142), (5.0, 170), (4.0, 215), (3.0, 267)]   # so_lieu_mau: V (ml), p (kPa)
PV = [round(v * p) for v, p in ROWS]                                   # 800 852 850 860 801
T_PHONG, P0V0 = 25, 800                                                # tham_so: t = 25 C; p0*V0 = 100*8
def fmt(v): return f"{v:.1f}".replace(".", ",")

R = random.Random(11)
PART = [(R.random(), R.random(), R.choice((-1, 1)) * R.uniform(0.25, 0.5), R.choice((-1, 1)) * R.uniform(0.25, 0.5))
        for _ in range(30)]

# ---------------- xilanh dung + ap ke ----------------
BX0, BX1, Y0ML, PXML = 250, 450, 1000, 46       # thanh xilanh trong; y cua vach 0 ml; px moi ml
def ymL(v, y0=Y0ML, px=PXML): return y0 - v * px

def syringe(d, t, V, bx0=BX0, bx1=BX1, y0=Y0ML, px=PXML, scale_lbl=True, heat=0.0, push=False, vmin=3.0):
    top = ymL(10.4, y0, px); yh = ymL(V, y0, px); cx = (bx0 + bx1) / 2; s = px / PXML
    d.rounded_rectangle([bx0 - 10, top, bx1 + 10, y0 + 10], radius=int(16 * s), fill=(246, 249, 255))
    d.rectangle([bx0, yh, bx1, y0], fill=mix((214, 232, 255), (255, 214, 200), heat))       # khoi khi nhot kin
    # hat khi: cung so hat, vung chua nho lai -> day len
    for (ux, uy, vx, vy) in PART:
        sp = 1 + 1.6 * heat
        x = bx0 + 14 * s + refl(ux + vx * t * sp, 0, 1) * (bx1 - bx0 - 28 * s)
        y = yh + 14 * s + refl(uy + vy * t * sp, 0, 1) * (y0 - yh - 28 * s)
        dot(d, x, y, 9 * s, mix(ORANGE, RED, heat))
    d.rounded_rectangle([bx0 - 10, top, bx1 + 10, y0 + 10], radius=int(16 * s), outline=NAVY, width=max(3, int(6 * s)))
    # vach chia
    for v in range(0, 11):
        L = (24 if v % 2 == 0 else 14) * s
        d.line([(bx0 - 10, ymL(v, y0, px)), (bx0 - 10 + L, ymL(v, y0, px))], fill=NAVY, width=max(2, int(3 * s)))
        if scale_lbl and v % 2 == 0 and v > 0:
            text(d, (bx0 - 28, ymL(v, y0, px)), str(v), 36, MUTED, bold=False, anchor="rm")
    if scale_lbl: text(d, (bx0 - 28, y0), "ml", 36, MUTED, bold=False, anchor="rm")
    # pit-tong + can + tay nam
    hh = 26 * s; d.rectangle([bx0 + 2, yh - hh, bx1 - 2, yh], fill=(70, 78, 100))
    rod_top = yh - hh - ((10.4 - vmin) * px - hh + 18)   # tay nam luon nam tren mieng xilanh
    d.rectangle([cx - 11 * s, rod_top, cx + 11 * s, yh - hh], fill=GRAY, outline=NAVY, width=max(2, int(3 * s)))
    d.rounded_rectangle([cx - 130 * s, rod_top - 22 * s, cx + 130 * s, rod_top], radius=int(10 * s), fill=NAVY)
    if push:
        ax = cx + 130 * s + 44 * s
        arrow(d, (ax, rod_top - 70 * s), (ax, rod_top + 20 * s), ORANGE, w=max(5, int(9 * s)), head=int(24 * s))
    # dau ong
    d.rectangle([cx - 20 * s, y0 + 10, cx + 20 * s, y0 + 40 * s], fill=GRAY, outline=NAVY, width=max(2, int(3 * s)))
    return cx, y0 + 40 * s

def gang(p): return math.radians(-225 + clamp(p / 300) * 270)
def gauge(d, cx, cy, r, p, fs=36, mark=None, out=True):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=NAVY, width=7)
    a0, a1 = math.degrees(gang(270)), math.degrees(gang(300))
    d.arc([cx - r + 14, cy - r + 14, cx + r - 14, cy + r - 14], a0, a1, fill=(248, 180, 170), width=14)
    for k in range(0, 13):
        a = gang(k * 25); L = 26 if k % 2 == 0 else 13
        d.line([(cx + (r - 14 - L) * math.cos(a), cy + (r - 14 - L) * math.sin(a)),
                (cx + (r - 14) * math.cos(a), cy + (r - 14) * math.sin(a))], fill=NAVY, width=4 if k % 2 == 0 else 3)
    for v in (0, 100, 200, 300):
        a = gang(v); rr = r + 36 if out else r - 64
        text(d, (cx + rr * math.cos(a), cy + rr * math.sin(a)), str(v), fs, INK, bold=False)
    text(d, (cx, cy + r * 0.5), "kPa", fs - 4, MUTED, bold=False)
    if mark is not None:
        a = gang(mark)
        d.line([(cx + (r - 2) * math.cos(a), cy + (r - 2) * math.sin(a)), (cx + (r + 22) * math.cos(a), cy + (r + 22) * math.sin(a))],
               fill=GREEN, width=8)
        text(d, (cx + (r + 48) * math.cos(a), cy + (r + 48) * math.sin(a)), str(mark), fs, GREEN)
    a = gang(p)
    d.line([(cx - 22 * math.cos(a), cy - 22 * math.sin(a)), (cx + (r - 34) * math.cos(a), cy + (r - 34) * math.sin(a))], fill=RED, width=9)
    dot(d, cx, cy, 14, NAVY)

GX, GY, GR = 810, 830, 170
def rig(d, t, V, p, push=False):
    nx, ny = syringe(d, t, V, push=push)
    d.line([(nx, ny), (nx, 1062), (GX, 1062), (GX, GY + GR)], fill=GRAY, width=16, joint="curve")
    gauge(d, GX, GY, GR, p)
    card(d, (620, 280, 1000, 600), fill=WHITE, outline=LIGHT, r=28, w=4)
    text(d, (810, 360), f"V = {fmt(V)} ml", 54, BLUE)
    text(d, (810, 450), f"p = {p:.0f} kPa", 54, RED)
    text(d, (810, 535), f"t = {T_PHONG} °C", 40, MUTED, bold=False)

# ---------------- canh 1: mo bai + du doan ----------------
def s_hook(img, d, t, sc):
    _IMG[0] = img
    rig(d, t, 8.0, 100)
    k = appear(t, sc["M"][1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (80, 1110, 1000, 1590), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 1170), "Dự đoán", 46, PURPLE, alpha=k)
    ctext(d, 1270, "Ấn pít-tông tới 4,0 ml (một nửa).\nÁp kế chỉ khoảng bao nhiêu?", 44, INK, alpha=k)
    for i, s in enumerate(("A. 100 kPa", "B. 150 kPa", "C. 200 kPa")):
        a = appear(t, sc["M"][1] + 0.2 + i * 0.15)
        x0 = 100 + i * 300
        card(d, (x0, 1395, x0 + 280, 1490), fill=A((245, 243, 255), a), outline=A(PURPLE, a), r=22, w=4)
        text(d, (x0 + 140, 1443), s, 40, INK, alpha=a)
    # thanh dem nguoc thoi gian nghi
    t1, t2 = sc["M"][1] + 0.6, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1532, 940, 1546], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1532, 140 + 800 * (1 - q), 1546], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh, ghi bang ----------------
MOVE = 1.0
def state(t, sc):
    V, c, extra, moving = ROWS[0][0], PV[0], 0.0, False
    for i in range(1, 5):
        s = sc["M"][i] + 0.1
        if t < s: break
        k = ease((t - s) / MOVE); V = lerp(ROWS[i - 1][0], ROWS[i][0], k); c = lerp(PV[i - 1], PV[i], k)
        tau = t - s; moving = tau < MOVE
        # so chi nhay len vai kPa ngay sau khi an roi tut ve gia tri on dinh (quan_sat trong kho)
        extra = 6 * ease(tau / MOVE) if tau < MOVE else 6 * (1 - ease((tau - MOVE) / 0.6))
    return V, c / V + extra, moving

def row_at(i, sc): return sc["M"][0] + 0.7 if i == 0 else sc["M"][i] + 0.1 + MOVE + 0.6

def s_do(img, d, t, sc):
    _IMG[0] = img
    V, p, mv = state(t, sc); rig(d, t, V, p, push=mv)
    card(d, (80, 1100, 1000, 1590), fill=WHITE, outline=NAVY, w=4)
    xs = [190, 420, 670]
    for x, c in zip(xs, ["Lần", "V (ml)", "p (kPa)"]): text(d, (x, 1148), c, 38, MUTED)
    d.line([(110, 1182), (970, 1182)], fill=LIGHT, width=4)
    last = max([i for i in range(5) if t >= row_at(i, sc)], default=-1)
    for i, (v, pp) in enumerate(ROWS):
        a = appear(t, row_at(i, sc), 0.35); y = 1225 + i * 72
        if a <= 0: continue
        if i == last: d.rounded_rectangle([100, y - 32, 980, y + 32], radius=16, fill=A((225, 236, 255), a))
        for x, s, col in zip(xs, [str(i + 1), fmt(v), str(pp)], [MUTED, BLUE, RED]):
            text(d, (x, y), s, 44, col, alpha=a)
        if i == 3: text(d, (880, y), "≈ gấp đôi", 36, GREEN, alpha=a)

# ---------------- canh 3: do thi p-V + tich pV ----------------
def s_graph(img, d, t, sc):
    _IMG[0] = img
    x0, x1, yb, yt = 190, 960, 930, 330
    X = lambda v: x0 + v / 9 * (x1 - x0); Y = lambda p: yb - p / 300 * (yb - yt)
    card(d, (60, 250, 1020, 1010), fill=WHITE, outline=LIGHT, w=3)
    for p_ in (100, 200, 300): d.line([(x0, Y(p_)), (x1, Y(p_))], fill=(240, 236, 228), width=2)
    d.line([(x0, yb), (x1 + 20, yb)], fill=NAVY, width=5); d.line([(x0, yb), (x0, yt - 25)], fill=NAVY, width=5)
    text(d, (x1 + 20, yb - 34), "V (ml)", 36, MUTED, anchor="rm"); text(d, (x0 + 18, yt - 22), "p (kPa)", 36, MUTED, anchor="lm")
    for v in range(1, 10):
        d.line([(X(v), yb), (X(v), yb + 10)], fill=NAVY, width=3); text(d, (X(v), yb + 36), str(v), 36, MUTED, bold=False)
    for p_ in (0, 100, 200, 300):
        d.line([(x0 - 10, Y(p_)), (x0, Y(p_))], fill=NAVY, width=4); text(d, (x0 - 18, Y(p_)), str(p_), 36, MUTED, bold=False, anchor="rm")
    k = ease((t - sc["M"][0] - 1.6) / 1.2)
    if k > 0:
        vs = [800 / 300 + (9 - 800 / 300) * j / 80 for j in range(81)]
        pts = [(X(v), Y(P0V0 / v)) for v in vs]; n = max(2, int(len(pts) * k))
        d.line(pts[:n], fill=A(BLUE, 0.55), width=7, joint="curve")
        text(d, (X(6.6), Y(212)), f"p = {P0V0}/V", 40, BLUE, alpha=appear(t, sc["M"][0] + 2.6))
    for i, (v, p_) in enumerate(ROWS):
        a = appear(t, sc["M"][0] + 0.2 + i * 0.25, 0.4)
        if a > 0: dot(d, X(v), Y(p_), 16 * back(a), ORANGE, WHITE)
    # cot p.V
    a1 = appear(t, sc["M"][1] - 0.2)
    if a1 <= 0: return
    card(d, (60, 1050, 1020, 1590), fill=A(WHITE, a1), outline=A(LIGHT, a1), w=3)
    base, sc_ = 1480, 0.33; band = appear(t, sc["M"][2], 0.4)
    if band > 0:
        d.rectangle([90, base - 860 * sc_, 990, base - 800 * sc_], fill=A((187, 247, 208), band))
    title = "Tích p·V (kPa·ml)" if band < 0.5 else "p·V ≈ 800 – 860 kPa·ml"
    text(d, (W / 2, 1095), title, 40, GREEN if band >= 0.5 else MUTED, alpha=a1)
    d.line([(90, base), (990, base)], fill=NAVY, width=4)
    for i, ((v, p_), pv) in enumerate(zip(ROWS, PV)):
        cx = 180 + i * 180; g = ease((t - sc["M"][1] - 0.3 - i * 0.3) / 0.5)
        text(d, (cx, 1522), f"{fmt(v)} ml", 36, MUTED, bold=False, alpha=a1)
        if g <= 0: continue
        top = base - pv * sc_ * g
        d.rectangle([cx - 55, top, cx + 55, base], fill=ORANGE)
        text(d, (cx, top - 32), str(pv), 42, INK, alpha=clamp(g * 2 - 1))

# ---------------- canh 4: co che ----------------
def hits(u0, s, L, t):  # so lan dap vao hai thanh trai/phai trong [0, t]
    return abs(math.floor((u0 + s * t) / L) - math.floor(u0 / L))

RB = random.Random(5)
MOL = [(RB.random(), RB.random(), RB.choice((-1, 1)) * RB.uniform(110, 210), RB.choice((-1, 1)) * RB.uniform(110, 210)) for _ in range(20)]
def box(d, t, t0, x0, x1, y0, y1, lbl, p_, a):
    d.rectangle([x0, y0, x1, y1], fill=A((236, 244, 255), a))
    d.line([(x0, y0), (x1, y0)], fill=A(NAVY, a), width=4); d.line([(x0, y1), (x1, y1)], fill=A(NAVY, a), width=4)
    L, Hh = x1 - x0 - 24, y1 - y0 - 24; n = 0
    flashL, flashR = [], []
    for (ux, uy, vx, vy) in MOL:
        x = x0 + 12 + refl(ux * L + vx * t, 0, L); y = y0 + 12 + refl(uy * Hh + vy * t, 0, Hh)
        dot(d, x, y, 10, A(ORANGE, a))
        if t > t0: n += hits(ux * L, vx, L, t) - hits(ux * L, vx, L, t0)
        if x - x0 < 26: flashL.append(y)
        if x1 - x < 26: flashR.append(y)
    for xx, fl in ((x0, flashL), (x1, flashR)):
        d.line([(xx, y0), (xx, y1)], fill=A(ORANGE, a), width=10)
        for y in fl: d.line([(xx, y - 26), (xx, y + 26)], fill=A(YELLOW, a), width=18)
    text(d, ((x0 + x1) / 2, y0 - 36), lbl, 40, BLUE, alpha=a)
    if t > t0:
        text(d, ((x0 + x1) / 2, y1 + 48), f"{n} va chạm", 40, ORANGE, alpha=a)
        text(d, ((x0 + x1) / 2, y1 + 108), f"p = {p_} kPa", 44, RED, alpha=appear(t, t0 + 1.2))

def s_why(img, d, t, sc):
    _IMG[0] = img
    a = appear(t, 0.1, 0.4); t0 = sc["M"][0] + 0.6
    box(d, t, t0, 110, 510, 330, 880, "8,0 ml", ROWS[0][1], a)
    box(d, t, t0, 680, 880, 330, 880, "4,0 ml", ROWS[3][1], a)
    k = back((t - sc["M"][1] - 0.6) / 0.5) if t >= sc["M"][1] + 0.6 else 0
    if k > 0:
        card(d, (80, 1110, 1000, 1450), fill=WHITE, outline=GREEN, w=6)
        rich(d, W / 2, 1235, "p_{1}V_{1} = p_{2}V_{2}", int(88 * clamp(k, 0.2, 1.08)), GREEN)
        text(d, (W / 2, 1370), "khi nhiệt độ không đổi", 40, MUTED, alpha=clamp(k))

# ---------------- canh 5: gioi han + bay ----------------
def s_trap(img, d, t, sc):
    _IMG[0] = img
    a = appear(t, 0.1)
    card(d, (80, 250, 1000, 560), fill=WHITE, outline=BLUE, w=6)
    text(d, (W / 2, 305), "Chưa nói được gì?", 44, BLUE, alpha=a)
    ctext(d, 395, "p·V chỉ không đổi trong sai số ≈ 5%,\nkhông bằng nhau tuyệt đối.", 40, INK, alpha=a, lh=1.25)
    text(d, (W / 2, 505), "Chưa cho biết p phụ thuộc nhiệt độ ra sao.", 36, MUTED, bold=False, alpha=a)
    b = appear(t, sc["M"][1] - 0.3)
    if b <= 0: return
    card(d, (80, 600, 1000, 1590), fill=A(WHITE, b), outline=A(RED, b), w=6)
    text(d, (W / 2, 655), "Bẫy: ấn thật nhanh", 46, RED, alpha=b)
    ts = sc["M"][1] + 0.4
    kc = ease((t - ts) / 0.3)                     # nen nhanh 8 -> 4 ml trong 0,3 s
    heat = ease((t - ts) / 1.2)
    V = lerp(8.0, 4.0, kc)
    syringe(d, t, V, bx0=190, bx1=310, y0=1230, px=34, scale_lbl=False, heat=heat, push=0 < t - ts < 0.4, vmin=4.0)
    # nhiet ke
    tx, tb, tt = 455, 1220, 770
    d.rounded_rectangle([tx - 16, tt, tx + 16, tb], radius=16, fill=WHITE, outline=NAVY, width=4)
    dot(d, tx, tb + 18, 30, RED, NAVY)
    lvl = lerp(tb - 150, tb - 360, heat)
    d.rectangle([tx - 8, lvl, tx + 8, tb], fill=RED)
    text(d, (tx, tt - 34), "t tăng", 36, RED, alpha=heat)
    # ap ke: moc 215 kPa (dang nhiet, so lieu mau) va kim vot qua
    p_iso = PV[0] / V
    p_show = p_iso * (1 + 0.16 * heat)
    gauge(d, 760, 990, 150, p_show, fs=36, mark=ROWS[3][1], out=False)
    c2 = appear(t, sc["M"][1] + 1.4)
    text(d, (W / 2, 1345), f"p lớn hơn {ROWS[3][1]} kPa, p·V lớn dần", 40, RED, alpha=c2)
    c3 = appear(t, sc["M"][2])
    card(d, (130, 1410, 950, 1550), fill=A((220, 252, 231), c3), r=24)
    ctext(d, 1480, "Làm đúng: ấn từ từ, đợi 10 giây\nrồi mới đọc áp kế", 38, GREEN, alpha=c3, lh=1.25)

CLIP = dict(id="tn-l12-boylecharles-01", header="VẬT LÍ 12 · THÍ NGHIỆM",
    footer="Định luật Boyle · thachlab.id.vn", scenes=[
 dict(key="hook", title="Nén khí trong xilanh kín", draw=s_hook, tail=0.6, caps=[
   ("8,0 ml khí nhốt kín, nối với áp kế.", 2.8),
   ("Chọn một đáp án trước khi xem tiếp.", 4.2)]),
 dict(key="do", title="Ấn từ từ, đọc áp kế", draw=s_do, tail=0.8, caps=[
   ("Ấn từ từ, đợi số chỉ ổn định rồi ghi.", 2.4),
   ("6,0 ml → 142 kPa", 2.2), ("5,0 ml → 170 kPa", 2.2),
   ("4,0 ml → 215 kPa: gần gấp đôi!", 2.6),
   ("3,0 ml → 267 kPa, gần trần thang đo.", 2.6)]),
 dict(key="graph", title="Đồ thị p–V và tích p·V", draw=s_graph, tail=0.8, caps=[
   ("V giảm, p tăng theo đường cong.", 3.0),
   ("Nhân p với V ở mỗi lần đo.", 2.8),
   ("800 đến 860: gần như không đổi.", 2.8)]),
 dict(key="why", title="Vì sao p tăng?", draw=s_why, tail=0.8, caps=[
   ("Cùng số phân tử, mật độ gấp đôi.", 3.0),
   ("Va chạm lên thành nhiều hơn → p tăng.", 3.2)]),
 dict(key="trap", title="Giới hạn và cái bẫy", draw=s_trap, tail=1.0, caps=[
   ("Kết quả chỉ đúng trong sai số đo.", 2.6),
   ("Ấn nhanh: khí nóng lên, p vọt cao.", 3.0),
   ("Không còn đẳng nhiệt nữa!", 2.6)]),
])
