# Clip: tn-l10-klr-apsuat-01 - Do khoi luong rieng cua bon khoi nhom bang can va binh chia do (30/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-klr-apsuat-01.json:
#   so_lieu_mau (m g, V cm3, rho g/cm3): 21,1 8 2,64 ; 40,9 15 2,73 ; 67,2 25 2,69 ; 99,7 37 2,69
#   tham_so: rho nhom 2,7 g/cm3 ; V 5-60 cm3 (cau hoi chot dung 60 cm3, chua tung hien tren man) ;
#   sai so doc binh chia do 0,5 cm3 ; binh 100 cm3.
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (khoi nho: can, tha chim, V = sau - truoc; tua nhanh 3 khoi
#       con lai, bang m - V) -> Dap an B (do thi m theo V thang qua goc + cot rho, khoi 8 cm3 lech nhieu nhat do doc
#       vach) -> Bay (lay muc sau lam V) roi Chua noi duoc (chat khac, vat noi) -> Chot + cau hoi tu nho lai (60 cm3).
# Muc nuoc truoc khi tha (giua binh) chi la vi tri ve, khong ghi so; tren binh chi ghi vach 100 (dung_cu).
from engine import *

ROWS = [(21.1, 8, 2.64), (40.9, 15, 2.73), (67.2, 25, 2.69), (99.7, 37, 2.69)]   # so_lieu_mau
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
AL_F, AL_T, AL_S = (178, 186, 200), (214, 220, 230), (138, 146, 164)   # mat truoc / tren / ben cua khoi nhom
WATER = (150, 200, 245)
DRED = (185, 28, 28)

def side(V): return 40 * V ** (1 / 3)          # canh khoi (px) ti le can bac ba cua V: 80 .. 133

# ---------------- dung cu (khung nguon 1080x1920) ----------------
CYL_X0, CYL_X1, CYL_B = 610, 790, 950          # long binh chia do; day trong o y 950
PX = 6                                         # px / cm3 (100 cm3 = 600 px -> vach 100 o y 350)
BASE = 40                                      # muc nuoc truoc (vi tri ve giua hai vach, khong ghi so)
def lvl(v): return CYL_B - v * PX

def cube(d, cx, by, s, alpha=1.0):
    """Khoi nhom: mat truoc (cx - s/2 .. cx + s/2, by - s .. by) + mat tren / ben lech 0,18 s."""
    o = 0.18 * s; x0, x1, y0 = cx - s / 2, cx + s / 2, by - s
    d.polygon([(x0, y0), (x0 + o, y0 - o), (x1 + o, y0 - o), (x1, y0)], fill=A(AL_T, alpha), outline=A(NAVY, alpha))
    d.polygon([(x1, y0), (x1 + o, y0 - o), (x1 + o, by - o), (x1, by)], fill=A(AL_S, alpha), outline=A(NAVY, alpha))
    d.rectangle([x0, y0, x1, by], fill=A(AL_F, alpha), outline=A(NAVY, alpha), width=3)

def balance(d, reading, block=None, ka=1.0):
    """Can dien tu: dia can mat tren y 560; man hinh so. block = canh khoi dang dat tren dia."""
    if block: cube(d, 260, 560, block, ka)
    d.rectangle([120, 560, 400, 578], fill=(200, 205, 215), outline=NAVY, width=3)
    d.rectangle([250, 578, 270, 596], fill=(120, 125, 140))
    card(d, (60, 596, 460, 810), fill=(70, 78, 100), r=22)
    card(d, (110, 640, 410, 750), fill=(220, 240, 225), r=12)
    text(d, (260, 695), reading, 54, (20, 60, 30))
    text(d, (260, 780), "cân điện tử", 38, WHITE, bold=False)

def cylinder(d, v_water, block=None, by=900, ka=1.0, marks=False, v_after=None):
    """Binh chia do 100 cm3. block = canh khoi treo bang chi (day khoi o y by, cach day binh)."""
    top = lvl(100) - 40
    yw = lvl(v_water)
    d.rectangle([CYL_X0, yw, CYL_X1, CYL_B], fill=WATER)
    if block:
        cx = (CYL_X0 + CYL_X1) / 2 - 12
        d.line([(cx + 0.09 * block, 290), (cx + 0.09 * block, by - block - 0.09 * block)], fill=A(NAVY, ka), width=3)
        cube(d, cx, by, block, ka)
        # phan khoi duoi mat nuoc phu mau nuoc nhat (khoi o TRONG nuoc)
        y_in = max(yw, by - block - 0.18 * block)
        if y_in < by:
            d.rectangle([CYL_X0 + 3, y_in, CYL_X1 - 3, by + 2], fill=A(WATER, 0.45 * ka))
    d.line([(CYL_X0, yw), (CYL_X1, yw)], fill=(37, 99, 235), width=4)
    # thanh binh + vach
    d.line([(CYL_X0, top), (CYL_X0, CYL_B)], fill=NAVY, width=5)
    d.line([(CYL_X1, top), (CYL_X1, CYL_B)], fill=NAVY, width=5)
    d.rectangle([CYL_X0 - 40, CYL_B, CYL_X1 + 40, CYL_B + 22], fill=NAVY)
    for v in range(10, 101, 10):
        y = lvl(v); d.line([(CYL_X0, y), (CYL_X0 + (34 if v % 50 == 0 else 20), y)], fill=NAVY, width=3)
    text(d, (CYL_X0 - 14, lvl(100)), "100", 38, INK, anchor="rm")
    text(d, (CYL_X0 - 14, lvl(50)), "50", 38, INK, anchor="rm")       # thang cua binh 100 cm3 (dung_cu)
    text(d, (CYL_X0 - 14, lvl(100) + 46), "cm³", 38, MUTED, bold=False, anchor="rm")
    if marks:                                  # vach truoc / sau ben phai binh
        yb = lvl(BASE)
        for x in range(CYL_X1 + 6, CYL_X1 + 70, 16): d.line([(x, yb), (x + 9, yb)], fill=GRAY, width=4)
        text(d, (CYL_X1 + 80, yb + 6), "trước", 38, MUTED, anchor="lt")
        if v_after is not None:
            ya = lvl(v_after); d.line([(CYL_X1 + 6, ya), (CYL_X1 + 70, ya)], fill=BLUE, width=4)
            text(d, (CYL_X1 + 80, ya - 6), "sau", 38, BLUE, anchor="lb")

def vcard(d, s, alpha=1.0):
    card(d, (820, 790, 1040, 940), fill=A(WHITE, alpha), outline=A(BLUE, alpha), r=22, w=4)
    text(d, (930, 834), "V đo được", 38, INK, bold=False, alpha=alpha)
    text(d, (930, 896), s, 46, BLUE, alpha=alpha)

def table(d, n, rho=0, y=1010, hl=None, ka=1.0):
    """Bang m - V - rho; n hang da co; rho = so hang da hien cot rho (con lai '?')."""
    card(d, (40, y, 1040, y + 500), fill=WHITE, outline=NAVY, w=4)
    xs = (230, 530, 830)
    for x, c in zip(xs, ("m (g)", "V (cm³)", "ρ (g/cm³)")): text(d, (x, y + 52), c, 40, INK)
    d.line([(70, y + 92), (1010, y + 92)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 150 + i * 92; m, v, r = ROWS[i]
        if hl == i: d.rounded_rectangle([60, yy - 40, 1020, yy + 40], radius=18, fill=A((255, 237, 213), ka))
        text(d, (xs[0], yy), vn(m), 44, INK); text(d, (xs[1], yy), str(v), 44, INK)
        if i < rho: text(d, (xs[2], yy), vn(r, 2), 46, BLUE)
        else: text(d, (xs[2], yy), "?", 44, GRAY)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong ve nut lua chon) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    balance(d, "0,0 g"); cylinder(d, BASE)
    x = 50
    for j, (m, v, r) in enumerate(ROWS):                 # bon khoi xep hang, to dan (thu 0,85 cho vua, khong cham chan binh)
        s = 0.85 * side(v); k = appear(t, 0.3 + 0.25 * j, 0.4)
        cube(d, x + s / 2, 985, s, k); x += s + 0.18 * s + 14
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1040 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 520), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 240, "Khối nhôm càng to thì\nρ = m/V tính ra\nthay đổi thế nào?", 48, INK, maxw=900, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 470, 940, y0 + 482], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 470, 140 + 800 * (1 - p), y0 + 482], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
FF0, FFW = 0.2, 1.45     # tua nhanh: khoi 2..4 bat dau tu M[1] + FF0, moi khoi FFW giay

def s_do(img, d, t, sc):
    M = sc["M"]
    if t < M[1]:                                         # khoi nho nhat, lam cham
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
        if t >= 3.8: vcard(d, "8 cm³", appear(t, 3.8, 0.3))
        table(d, 1 if t >= 4.0 else 0)
        return
    # tua nhanh 3 khoi con lai
    card(d, (60, 280, 300, 340), fill=ORANGE, r=30); text(d, (180, 310), "tua nhanh", 38, WHITE)
    u = t - M[1] - FF0; j = 1 + max(0, min(2, int(u // FFW))) if u >= 0 else 0
    if u < 0:
        balance(d, "0,0 g"); cylinder(d, BASE + ROWS[0][1], side(ROWS[0][1]), 900, marks=True, v_after=BASE + ROWS[0][1])
        vcard(d, "8 cm³"); table(d, 1); return
    w = u - (j - 1) * FFW; m, v, r = ROWS[j]; s = side(v)
    if w < 0.6:
        balance(d, vn(m) + " g", s); cylinder(d, BASE)
    else:
        balance(d, "0,0 g"); cylinder(d, BASE + v, s, 900, marks=True, v_after=BASE + v); vcard(d, f"{v} cm³")
    table(d, j + (1 if w >= 0.95 else 0))

# ---------------- canh 3: Dap an + rut ra ----------------
GX0, GX1, GY0, GY1 = 170, 960, 860, 420         # truc do thi m theo V: V 0-40 cm3, m 0-110 g
def gx(v): return GX0 + v / 40 * (GX1 - GX0)
def gy(m): return GY0 - m / 110 * (GY0 - GY1)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    pw = tw(d, "ĐÁP ÁN B · gần như không đổi", F(38)) + 52
    card(d, (W - 60 - pw, 236, W - 60, 296), fill=A(NAVY, ka), r=30)
    text(d, (W - 60 - pw / 2, 266), "ĐÁP ÁN B · gần như không đổi", 38, WHITE, alpha=ka)
    card(d, (40, 320, 1040, 975), fill=WHITE, outline=LIGHT, w=3)
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=4)
    arrow(d, (GX0, GY1 - 10), (GX0, GY1 - 34), NAVY, w=4, head=16); arrow(d, (GX1 + 10, GY0), (GX1 + 34, GY0), NAVY, w=4, head=16)
    text(d, (GX0 + 20, GY1 - 50), "m (g)", 38, INK, anchor="lm")
    text(d, (GX1 + 34, GY0 - 40), "V (cm³)", 38, INK, anchor="rm")
    for v in (10, 20, 30, 40):
        d.line([(gx(v), GY0), (gx(v), GY0 + 12)], fill=NAVY, width=3); text(d, (gx(v), GY0 + 40), str(v), 38, MUTED, bold=False)
    for m in (50, 100):
        d.line([(GX0 - 12, gy(m)), (GX0, gy(m))], fill=NAVY, width=3); text(d, (GX0 - 20, gy(m)), str(m), 38, MUTED, bold=False, anchor="rm")
    kl = appear(t, M[0] + 0.6, 0.8)                     # duong thang qua goc, he so goc 2,7
    if kl > 0:
        v1 = 40 * kl
        d.line([(gx(0), gy(0)), (gx(v1), gy(2.7 * v1))], fill=A(GREEN, 0.9), width=5)
        if kl >= 1: text(d, (gx(29), gy(2.7 * 29) - 46), "đường thẳng qua gốc", 38, GREEN, anchor="rm")
    for i, (m, v, r) in enumerate(ROWS):
        k = appear(t, 0.2 + 0.15 * i, 0.3)
        if k > 0: dot(d, gx(v), gy(m), 13, A(ORANGE if (i == 0 and t >= M[1] - 0.1) else BLUE, k), outline=WHITE)
    hl = 0 if t >= M[1] - 0.1 else None
    table(d, 4, rho=sum(t >= 0.3 + 0.2 * i for i in range(4)), y=1000, hl=hl, ka=appear(t, M[1] - 0.1, 0.3))
    kn = appear(t, M[1] + 0.4, 0.4)
    if kn > 0:
        card(d, (40, 1515, 1040, 1605), fill=A((255, 237, 213), kn), outline=A(ORANGE, kn), r=20, w=3)
        text(d, (W / 2, 1560), "Lệch ≤ 0,06: do đọc vạch ±0,5 cm³", 42, (154, 52, 18), alpha=kn)

# ---------------- canh 4: Bay roi Chua noi duoc (khong hien cung luc) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    balance(d, "0,0 g")
    cylinder(d, BASE + ROWS[0][1], side(ROWS[0][1]), 900, marks=True, v_after=BASE + ROWS[0][1])
    if a1 > 0:
        y0 = 1040
        card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
        q = "“V = mực nước sau”"
        ks = clamp((t - 1.2) / 0.4); f = F(48); lw = tw(d, q, f); yy = y0 + 210
        text(d, (W / 2, yy), q, 48, DRED, alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=4)
        ctext(d, y0 + 380, "✓ V = mực sau − mực trước", 48, (21, 110, 55), maxw=900, alpha=a1 * appear(t, 1.7, 0.5))
    if k2 > 0:
        y0 = 1040 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Chất khác có ρ khác không?", "• Vật nổi (gỗ) đo V cách nào?")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (90, y0 + 220 + j * 140), l1, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: khoi nhom 60 cm3 nang bao nhieu (can buoc m = rho.V); goi y tre 2,5 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 390, "ρ là của chất, không của vật to hay nhỏ", 50, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.6, 0.5)
    if k1 <= 0: return
    card(d, (40, 580, 1040, 1310), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 610, W / 2 + pw / 2, 674), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 642), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 830, "Khối nhôm 60 cm³ có\nkhối lượng khoảng\nbao nhiêu gam?", 48, INK, maxw=920,
          alpha=appear(t, M[0] + 0.9, 0.5))
    kh = appear(t, M[0] + 0.9 + 2.5, 0.5)
    card(d, (110, 1010, 970, 1260), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1065, "Gợi ý", 38, INK, alpha=kh)
    ctext(d, 1170, "m = ρ · V", 46, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.3, "ding"),
           (do["t0"] + 2.4, "tap")]
    out += [(do["t0"] + M[1] + FF0 + j * FFW, "tick") for j in range(3)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.6, "open")]
    return out

CLIP = dict(id="tn-l10-klr-apsuat-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Khối lượng riêng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bốn khối nhôm to nhỏ", draw=s_hook, tail=0.8, caps=[
   ("Cân lấy m, nước dâng cho V.", 3.0),
   ("Tự đoán trước khi xem tiếp.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Cân khối nhỏ, rồi thả chìm hẳn.", 4.4),
   ("Lặp lại với ba khối còn lại.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Bốn khối đều gần 2,7 g/cm³.", 3.8),
   ("Khối nhỏ nhất lệch nhiều nhất.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy thường gặp.", 3.6),
   ("Thí nghiệm này mới đo nhôm.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Dừng video, tự trả lời.", 7.6)]),
])
