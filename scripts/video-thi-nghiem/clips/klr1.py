# Clip: tn-l10-klr-apsuat-01 - Do khoi luong rieng bon khoi nhom bang can va binh chia do (ban 2 cong moi, 27/11/2026)
# So lieu tu content/thi-nghiem/tn-l10-klr-apsuat-01.json:
#   so_lieu_mau (m g, V cm3, rho g/cm3): 21,1 8 2,64 ; 40,9 15 2,73 ; 67,2 25 2,69 ; 99,7 37 2,69
#   tham_so: rho nhom 2,7 g/cm3 ; V 5-60 cm3 ; doc binh chia do +-0,5 cm3 ; binh 100 cm3.
# Muc nuoc truoc khi tha chi la vi tri ve (khong ghi so) ; tren binh chi ghi vach 50, 100.
# Du doan (K10, khong nut): khoi nhom cang to, rho = m/V tinh ra doi the nao? (dap an: gan nhu khong doi).
# Bay = hien_tuong_hay_sai[1]: lay muc nuoc sau lam V (khoi 37 cm3, ngoac khong ghi so).
# Chot (tu suy, V = 60 cm3 trong tham_so, bai khong co): khoi nhom dac 60 cm3 nang bao nhieu? m = 2,7 . 60 = 162 g.
#   162 khong hien tren man ; buoc chua chieu: dao cong thuc rho = m/V.
from engine import *

ROWS = [(21.1, 8, 2.64), (40.9, 15, 2.73), (67.2, 25, 2.69), (99.7, 37, 2.69)]
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
AL_F, AL_T, AL_S = (178, 186, 200), (214, 220, 230), (138, 146, 164)
WATER = (150, 200, 245)
NOTE = (60, 64, 84); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128); DGREEN = (21, 110, 55)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

def side(V): return 40 * V ** (1 / 3)

CYL_X0, CYL_X1, CYL_B = 640, 820, 950
PX = 6
BASE = 40
def lvl(v): return CYL_B - v * PX

def cube(d, cx, by, s, alpha=1.0):
    o = 0.18 * s; x0, x1, y0 = cx - s / 2, cx + s / 2, by - s
    d.polygon([(x0, y0), (x0 + o, y0 - o), (x1 + o, y0 - o), (x1, y0)], fill=A(AL_T, alpha), outline=A(NAVY, alpha))
    d.polygon([(x1, y0), (x1 + o, y0 - o), (x1 + o, by - o), (x1, by)], fill=A(AL_S, alpha), outline=A(NAVY, alpha))
    d.rectangle([x0, y0, x1, by], fill=A(AL_F, alpha), outline=A(NAVY, alpha), width=3)

def balance(d, reading, block=None, ka=1.0):
    if block: cube(d, 260, 560, block, ka)
    d.rectangle([120, 560, 400, 578], fill=(200, 205, 215), outline=NAVY, width=3)
    d.rectangle([250, 578, 270, 596], fill=(120, 125, 140))
    card(d, (60, 596, 460, 820), fill=(70, 78, 100), r=22)
    card(d, (100, 630, 420, 740), fill=(220, 240, 225), r=12)
    text(d, (260, 685), reading, 62, (20, 60, 30))
    text(d, (260, 785), "cân điện tử", 55, WHITE)

def cylinder(d, v_water, block=None, by=900, ka=1.0, marks=False, v_after=None):
    top = lvl(100) - 40; yw = lvl(v_water)
    d.rectangle([CYL_X0, yw, CYL_X1, CYL_B], fill=WATER)
    if block:
        cx = (CYL_X0 + CYL_X1) / 2 - 12
        d.line([(cx + 0.09 * block, 290), (cx + 0.09 * block, by - block - 0.09 * block)], fill=A(NAVY, ka), width=3)
        cube(d, cx, by, block, ka)
        y_in = max(yw, by - block - 0.18 * block)
        if y_in < by: d.rectangle([CYL_X0 + 3, y_in, CYL_X1 - 3, by + 2], fill=A(WATER, 0.45 * ka))
    d.line([(CYL_X0, yw), (CYL_X1, yw)], fill=(37, 99, 235), width=4)
    d.line([(CYL_X0, top), (CYL_X0, CYL_B)], fill=NAVY, width=5)
    d.line([(CYL_X1, top), (CYL_X1, CYL_B)], fill=NAVY, width=5)
    d.rectangle([CYL_X0 - 40, CYL_B, CYL_X1 + 40, CYL_B + 22], fill=NAVY)
    for v in range(10, 101, 10):
        y = lvl(v); d.line([(CYL_X0, y), (CYL_X0 + (34 if v % 50 == 0 else 20), y)], fill=NAVY, width=3)
    text(d, (CYL_X0 - 14, lvl(100)), "100", 55, INK, anchor="rm")
    text(d, (CYL_X0 - 14, lvl(50)), "50", 55, INK, anchor="rm")
    text(d, (CYL_X0 - 14, lvl(100) - 58), "cm³", 55, INK, anchor="rm")
    if marks:
        yb = lvl(BASE)
        for x in range(CYL_X1 + 6, CYL_X1 + 60, 16): d.line([(x, yb), (x + 9, yb)], fill=GRAY, width=4)
        text(d, (CYL_X1 + 70, yb + 4), "trước", 55, NOTE, anchor="lt")
        if v_after is not None:
            ya = lvl(v_after); d.line([(CYL_X1 + 6, ya), (CYL_X1 + 60, ya)], fill=BLUE, width=4)
            text(d, (CYL_X1 + 70, ya - 4), "sau", 55, BLUE, anchor="lb")

def table(d, n, rho=0, y=1010, hl=None, ka=1.0):
    card(d, (40, y, 1040, y + 110 + 4 * 84), fill=WHITE, outline=NAVY, w=4)
    xs = (230, 530, 840)
    for x, c in zip(xs, ("m (g)", "V (cm³)", "ρ (g/cm³)")): text(d, (x, y + 52), c, 55, NOTE)
    d.line([(70, y + 96), (1010, y + 96)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 145 + i * 84; m, v, r = ROWS[i]
        if hl == i: d.rounded_rectangle([60, yy - 38, 1020, yy + 38], radius=18, fill=A((255, 237, 213), ka))
        text(d, (xs[0], yy), vn(m), 58, INK); text(d, (xs[1], yy), str(v), 58, INK)
        text(d, (xs[2], yy), vn(r, 2) if i < rho else "?", 60 if i < rho else 58, BLUE if i < rho else GRAY)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    balance(d, "0,0 g"); cylinder(d, BASE)
    x = 70
    for j, (m, v, r) in enumerate(ROWS):
        s = 0.85 * side(v); k = appear(t, 0.3 + 0.25 * j, 0.4)
        cube(d, x + s / 2, 985, s, k); x += s + 0.18 * s + 14
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1060 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 170), "Khối nhôm càng to,", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 255), "khối lượng riêng ρ = m/V", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 340), "đổi thế nào?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 440, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: tien hanh ----------------
FF0, FFW = 0.3, 1.45

def s_do(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    if t < M[1]:
        s = side(ROWS[0][1])
        on_bal = 0.5 <= t < 2.3
        kb = appear(t, 0.5, 0.35) * (1 - appear(t, 2.1, 0.2))
        balance(d, ("21,1 g" if t >= 1.1 else "0,0 g") if on_bal else "0,0 g", s if kb > 0 else None, kb)
        if t >= 2.4:
            by = lerp(560, 900, ease((t - 2.4) / 1.2))
            sub = clamp((by - lvl(BASE)) / s)
            cylinder(d, BASE + ROWS[0][1] * sub, s, by, appear(t, 2.4, 0.3), marks=t >= 3.7,
                     v_after=BASE + ROWS[0][1] if t >= 3.7 else None)
        else:
            cylinder(d, BASE)
        table(d, 1 if t >= 4.0 else 0)
        return
    u = t - M[1] - FF0
    if u < 0:
        balance(d, "0,0 g"); cylinder(d, BASE + ROWS[0][1], side(ROWS[0][1]), 900, marks=True, v_after=BASE + ROWS[0][1])
        table(d, 1); return
    j = 1 + max(0, min(2, int(u // FFW)))
    w = u - (j - 1) * FFW; m, v, r = ROWS[j]; s = side(v)
    if w < 0.6:
        balance(d, vn(m) + " g", s); cylinder(d, BASE)
    else:
        balance(d, "0,0 g"); cylinder(d, BASE + v, s, 900, marks=True, v_after=BASE + v)
    table(d, j + (1 if w >= 0.95 else 0))

# ---------------- canh 3: ket qua ----------------
GX0, GX1, GY0, GY1 = 200, 960, 820, 420
def gx(v): return GX0 + v / 40 * (GX1 - GX0)
def gy(m): return GY0 - m / 110 * (GY0 - GY1)

def s_dapan(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    d.line([(GX0, GY1 - 40), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=4)
    text(d, (GX0 + 24, GY1 - 60), "m (g)", 55, INK, anchor="lm")
    text(d, (GX1 + 40, GY0 + 56), "V (cm³)", 55, INK, anchor="rm")
    for v in (20,):
        d.line([(gx(v), GY0), (gx(v), GY0 + 12)], fill=NAVY, width=3); text(d, (gx(v), GY0 + 56), str(v), 55, INK)
    for m in (50, 100):
        d.line([(GX0 - 12, gy(m)), (GX0, gy(m))], fill=NAVY, width=3); text(d, (GX0 - 22, gy(m)), str(m), 55, INK, anchor="rm")
    kl = appear(t, 0.8, 0.8)
    if kl > 0:
        v1 = 40 * kl
        d.line([(gx(0), gy(0)), (gx(v1), gy(2.7 * v1))], fill=A(GREEN, 0.9), width=6)
    kt = appear(t, 2.2, 0.4)
    if kt > 0: text(d, (gx(40), gy(18)), "thẳng, qua gốc", 55, DGREEN, anchor="rm", alpha=kt)
    for i, (m, v, r) in enumerate(ROWS):
        dot(d, gx(v), gy(m), 14, ORANGE if (i == 0 and t >= M[1] + 0.8) else BLUE, outline=WHITE)
    hl = 0 if t >= M[1] + 0.8 else None
    table(d, 4, rho=sum(t >= 0.3 + 0.2 * i for i in range(4)), y=930, hl=hl, ka=appear(t, M[1] + 0.8, 0.3))
    ka = appear(t, 2.2, 0.4)
    if ka > 0 and t < M[1] + 0.8:
        card(d, (40, 1400, 1040, 1600), fill=A(NAVY, ka), r=30)
        text(d, (W / 2, 1460), "ρ gần như không đổi,", 60, WHITE, alpha=ka)
        text(d, (W / 2, 1545), "quanh 2,7 g/cm³", 60, (253, 224, 71), alpha=ka)
    kn = appear(t, M[1] + 0.8, 0.4)
    if kn > 0:
        card(d, (40, 1400, 1040, 1600), fill=A((255, 237, 213), kn), outline=A(ORANGE, kn), r=24, w=4)
        text(d, (W / 2, 1460), "V nhỏ: đọc vạch lệch", 58, (154, 52, 18), alpha=kn)
        text(d, (W / 2, 1545), "0,5 cm³ là đáng kể", 58, (154, 52, 18), alpha=kn)

# ---------------- canh 4: bay + chua noi duoc ----------------
VB = ROWS[3][1]
def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    k3 = appear(t, M[2] - 0.1, 0.45)
    cylinder(d, BASE + VB, side(VB), 900, marks=True, v_after=BASE + VB)
    a1 = appear(t, 0.2, 0.45) * (1 - k3)
    if a1 > 0:
        ya, yb, y0 = lvl(BASE + VB), lvl(BASE), CYL_B
        bx = CYL_X0 - 150                         # ngoac sai: tu day binh toi muc sau
        d.line([(bx, ya), (bx, y0)], fill=A(RED, a1), width=5)
        for y in (ya, y0): d.line([(bx - 12, y), (bx + 12, y)], fill=A(RED, a1), width=5)
        text(d, (bx - 20, (ya + y0) / 2 + 60), "mực sau", 55, RED, anchor="rm", alpha=a1)
        card(d, (40, 1060, 1040, 1290), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pill(d, W / 2, 1125, "BẪY", RED, a1)
        q = "“V = mực nước sau”"
        ks = clamp((t - M[1]) / 0.4); f = F(60); lw = tw(d, q, f); yy = 1225
        text(d, (W / 2, yy), q, 60, mix(RED, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
        ok = appear(t, M[1], 0.4) * a1          # ngoac dung: giua muc truoc va muc sau
        if ok > 0:
            gxb = CYL_X1 + 200
            d.line([(gxb, ya), (gxb, yb)], fill=A(GREEN, ok), width=6)
            for y in (ya, yb): d.line([(gxb - 12, y), (gxb + 12, y)], fill=A(GREEN, ok), width=6)
            text(d, (gxb + 22, (ya + yb) / 2), "V", 64, GREEN, anchor="lm", alpha=ok)
        k2 = appear(t, M[1] + 3.0, 0.45) * a1
        if k2 > 0:
            card(d, (40, 1330, 1040, 1470), fill=A((220, 252, 231), k2), outline=A(GREEN, k2), w=5)
            text(d, (W / 2, 1400), "V = mực sau − mực trước", 60, DGREEN, alpha=k2)
    if k3 > 0:
        card(d, (40, 1060, 1040, 1480), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 1130, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 1260), "Mới đo nhôm.", 60, INK, alpha=k3)
        text(d, (W / 2, 1360), "Chất khác, ρ ra sao?", 60, INK, alpha=k3)

# ---------------- canh 5: thu nghi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1250), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 305, "THỬ NGHĨ", ORANGE, k)
    cube(d, W / 2 - 20, 640, 1.0 * side(60), k)
    text(d, (W / 2, 750), "Khối nhôm đặc khác,", 62, INK, alpha=k)
    text(d, (W / 2, 840), "thể tích 60 cm³.", 62, INK, alpha=k)
    text(d, (W / 2, 970), "Nặng bao nhiêu gam?", 64, DORANGE, alpha=k)
    seg_bar(d, 1100, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"), (do["t0"] + 2.4, "tap")]
    out += [(do["t0"] + M[1] + FF0 + j * FFW, "tick") for j in range(3)]
    out += [(da["t0"] + 2.2, "ding"), (da["t0"] + da["M"][1] + 0.8, "tap"),
            (b["t0"] + b["M"][1], "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l10-klr-apsuat-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Khối lượng riêng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bốn khối nhôm to nhỏ", draw=s_hook, tail=0.3, caps=[
   ("Cân lấy m, nước dâng cho V.", 3.8),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Cân, rồi thả chìm", draw=s_do, tail=0.4, caps=[
   ("Cân khối nhỏ, rồi thả chìm hẳn.", 4.4),
   ("Tua nhanh ba khối còn lại.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=1.0, caps=[
   ("Chia m cho V.", 3.8),
   ("Khối nhỏ nhất lệch nhiều nhất.", 4.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Đúng không?", 3.0),
   ("Nước dâng bao nhiêu?", 6.1),
   ("Chưa nói được.", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Dừng lại, tự tính.", 6.6)]),
])
