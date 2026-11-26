# Clip: tn-l12-chuyenthe-03 - Hai dia nuoc 20 ml, mot dia truoc quat, can sau 1 gio.
# So lieu lay tu content/thi-nghiem/tn-l12-chuyenthe-03.json -> so_lieu_mau (MINH HOA tu mo hinh, phong 30 °C):
#   gio 0 m/s -> 18,4 g · 1 m/s -> 15,6 g · 3 m/s -> 11,2 g · 5 m/s -> 8,1 g (con lai sau 1 gio, ban dau 20 ml = 20 g).
#   Hang 40 °C (15,2 g; 7,6 g) KHONG hien: de danh cho cau chot.
# Ban 1 (14/11/2026). Ban 2 (26/11/2026, KE-HOACH-CAI-TIEN-CLIP viec 4 lo 32): cong --do-chu (chu ve >= 58 px,
#   <= 180 tu/phut moi canh, nhip >= 2 s), <= 50 s, K10 (khong nut A-D, khong "chon dap an"); bo canh "chua noi duoc"
#   (giu trong khung web), bay ve hai hinh canh nhau (tuong / that).
# Du doan (khung web): phong 30 °C, hai dia 20 ml, dia phai truoc quat 3 m/s. Sau 1 gio? A ca hai van 20 g vi chua soi
#   (hien_tuong_hay_sai[0]) / B voi bang nhau / C ca hai voi, dia truoc quat voi hon (dap an: 18,4 g va 11,2 g) / D chi dia quat voi.
# Bay (hien_tuong_hay_sai[1]): "gio hat nuoc ra" -> mat nuoc phang, khong giot van; gio cuon hoi (phan tu da thoat).
# Khong viet "mat thoang" / "soi o 100 °C" tren man: Cau Tu kiem tra sau hop hoi dung y nay.
# THU NGHI (= cau_chot khung, CA TU SUY ghi trong kho): phong 40 °C, gio 3 m/s -> con it hon 11,2 g (7,6 g). So 7,6 khong hien.
from engine import *

ROWS = [(0, 18.4), (1, 15.6), (3, 11.2), (5, 8.1)]   # (gio m/s, nuoc con lai g) o 30 °C - so_lieu_mau
M0 = 20.0
STILL, FAN = 18.4, 11.2

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-chuyenthe-03.json")))
    hang = [tuple(r) for r in k["so_lieu_mau"]["hang"]]
    for v, m in ROWS: assert (v, 30, m) in hang, (v, m)
    assert (3, 40, 7.6) in hang and 7.6 < FAN
    assert {x["ky_hieu"]: x for x in k["tham_so"]}["V0"]["gia_tri"] == M0
_kiem_so()

DGREEN = (10, 110, 50); DRED = (185, 28, 28); DORANGE = (176, 64, 8); DTEAL = (10, 110, 100)
FS = 58
WATER = (150, 200, 245); WATER_D = (90, 150, 220)
def vn(x): return f"{x:.1f}".replace(".", ",")

def pill(d, cx, cy, s, fill, alpha=1.0, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 38, cx + pw / 2, cy + 38), fill=A(fill, alpha), r=36)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (190, y, 890, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (190, y, 190 + max(70, 700 * q), y + 70), fill=A(col, a), r=35)

# ---------------- dung cu ----------------
DY = 660                                             # day dia
def dish(d, cx, m, alpha=1.0, dy=DY):
    """dia nong: mieng rong 300, sau 70; muc nuoc ti le khoi luong (20 g = day 56 px)"""
    w0, w1, h = 150, 120, 70
    d.polygon([(cx - w0, dy - h), (cx + w0, dy - h), (cx + w1, dy), (cx - w1, dy)], fill=A((225, 230, 238), alpha))
    lv = 56 * m / M0
    if lv > 2:
        k = lv / h; wl = w1 + (w0 - w1) * k
        d.polygon([(cx - wl + 6, dy - lv), (cx + wl - 6, dy - lv), (cx + w1 - 6, dy - 4), (cx - w1 + 6, dy - 4)], fill=A(WATER, alpha))
        d.line([(cx - wl + 6, dy - lv), (cx + wl - 6, dy - lv)], fill=A(WATER_D, alpha), width=4)
    d.line([(cx - w0, dy - h), (cx - w1, dy), (cx + w1, dy), (cx + w0, dy - h)], fill=A(NAVY, alpha), width=6)

def scale(d, cx, s, alpha=1.0, hl=0.0):
    d.rounded_rectangle([cx - 160, DY + 6, cx + 160, DY + 40], radius=8, fill=A((120, 126, 140), alpha))
    d.rounded_rectangle([cx - 150, DY + 40, cx + 150, DY + 170], radius=14, fill=A((60, 66, 84), alpha))
    d.rounded_rectangle([cx - 125, DY + 60, cx + 125, DY + 150], radius=10, fill=A((205, 230, 200) if s else (90, 100, 90), alpha))
    if hl > 0: d.rounded_rectangle([cx - 131, DY + 54, cx + 131, DY + 156], radius=12, outline=A(ORANGE, hl), width=8)
    if s: text(d, (cx, DY + 105), s, 64, NAVY, alpha=alpha)

def fan(d, t, cx, cy, on=1.0, base=True):
    if base:
        d.line([(cx + 20, cy), (cx + 40, DY + 150)], fill=(90, 96, 110), width=14)
        d.rounded_rectangle([cx - 30, DY + 140, cx + 110, DY + 160], radius=8, fill=(90, 96, 110))
    d.ellipse([cx - 90, cy - 120, cx + 50, cy + 120], outline=NAVY, width=7, fill=(240, 244, 250))
    for k in range(3):
        a = t * 14 * on + k * 2 * math.pi / 3
        d.ellipse([cx - 20 - 55 * abs(math.cos(a)) * 0.5, cy + 95 * math.sin(a) - 22, cx - 20 + 55 * abs(math.cos(a)) * 0.5,
                   cy + 95 * math.sin(a) + 22], fill=A(BLUE, 0.35 + 0.4 * (1 - on)))
    dot(d, cx - 20, cy, 16, NAVY)

def wind(d, t, x0, x1, ys, alpha=1.0):
    for j, y in enumerate(ys):
        u = (t * 1.3 + j * 0.37) % 1
        xa = x1 - u * (x1 - x0); al = alpha * min(1, u / 0.15, (1 - u) / 0.15)
        d.line([(xa, y), (xa - 90, y)], fill=A(TEAL, al), width=6)
        d.line([(xa - 90, y), (xa - 74, y - 12)], fill=A(TEAL, al), width=6)

def therm_card(d, s="30 °C"):
    card(d, (40, 255, 340, 420), fill=WHITE, outline=NAVY, w=4, r=22)
    text(d, (190, 300), "Phòng", FS, INK)
    text(d, (190, 372), s, 62, RED)

XL, XR, XF = 230, 600, 930                            # dia trai, dia phai, quat

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    therm_card(d)
    dish(d, XL, M0); dish(d, XR, M0); fan(d, t, XF, 480)
    wind(d, t, XR - 120, XF - 110, (490, 530, 570))
    pill(d, 680, 320, "gió 3 m/s", TEAL, size=FS)
    text(d, (XL, DY + 60), "để yên", FS, INK)
    text(d, (XR, DY + 60), "trước quạt", FS, DTEAL)
    text(d, (W / 2, DY + 150), "mỗi đĩa 20 ml", FS, BLUE)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1010 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 430), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, k)
    text(d, (W / 2, y0 + 180), "Sau 1 giờ,", 64, INK, alpha=k)
    text(d, (W / 2, y0 + 265), "hai đĩa ra sao?", 64, PURPLE, alpha=k)
    seg_bar(d, y0 + 335, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: Tien hanh (tua nhanh 1 gio, can lai) ----------------
def tau_of(t, sc):                                    # phut da troi
    a, b = sc["M"][0] + 0.3, sc["M"][1] - 0.3
    return 60.0 * clamp((t - a) / (b - a))

def readings(tau):
    """so can hien tren man: chi luc 0 phut va 60 phut (khong noi suy)"""
    if tau <= 1e-6: return vn(M0) + " g", vn(M0) + " g"
    if tau >= 60 - 1e-6: return vn(STILL) + " g", vn(FAN) + " g"
    return "…", "…"

def s_do(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    tau = tau_of(t, sc)
    therm_card(d)
    mL = M0 - (M0 - STILL) * tau / 60; mR = M0 - (M0 - FAN) * tau / 60
    dish(d, XL, mL); dish(d, XR, mR); fan(d, t, XF, 480)
    wind(d, t, XR - 120, XF - 110, (490, 530, 570))
    rl, rr = readings(tau); hl = appear(t, M[1] + 0.1, 0.4) * (0.6 + 0.4 * math.cos((t - M[1]) * 6))
    scale(d, XL, rl, hl=hl); scale(d, XR, rr, hl=hl)
    card(d, (370, 255, 700, 420), fill=WHITE, outline=NAVY, w=4, r=22)
    text(d, (535, 300), "Đồng hồ", FS, INK)
    text(d, (535, 372), f"{int(tau + 1e-6)} phút", 62, NAVY)
    if tau < 60:
        wdt = tw(d, "TUA NHANH", F(FS)) + 100
        card(d, (W / 2 - wdt / 2, 900, W / 2 + wdt / 2, 980), fill=ORANGE, r=38)
        text(d, (W / 2 + 24, 940), "TUA NHANH", FS, WHITE)
        for kk in range(2):
            tx = W / 2 - wdt / 2 + 26 + kk * 18; d.polygon([(tx, 922), (tx, 958), (tx + 18, 940)], fill=WHITE)
    k2 = appear(t, M[1] + 0.6, 0.4)
    if k2 > 0:
        card(d, (60, 1040, 1020, 1200), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 1120), "Chưa sôi: còn xa 100 °C", 62, DGREEN, alpha=k2)

# ---------------- canh 3: Dap an + bieu do ----------------
def s_ket(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    ka = appear(t, 0.3, 0.4)
    card(d, (40, 260, 1040, 1340), fill=WHITE, outline=LIGHT, w=4)
    text(d, (80, 330), "Còn sau 1 giờ (g)", FS, INK, anchor="lm", alpha=ka)
    text(d, (1000, 330), "minh hoạ", FS, PURPLE, anchor="rm", alpha=ka)
    X0, KX = 330, 620 / 20                            # truc tu 0 g, 20 g = 620 px
    yb = 1150
    d.line([(X0, 420), (X0, yb)], fill=INK, width=5); d.line([(X0, yb), (X0 + KX * 20 + 20, yb)], fill=INK, width=5)
    for v in (0, 10, 20):
        x = X0 + KX * v; d.line([(x, yb), (x, yb + 16)], fill=INK, width=5)
        text(d, (x, yb + 56), str(v), FS, INK)
    xs = X0 + KX * 20
    for yy in range(425, yb, 30): d.line([(xs, yy), (xs, yy + 15)], fill=GREEN, width=5)
    text(d, (1000, yb + 120), "lúc đầu", FS, DGREEN, anchor="rm", alpha=ka)
    order = (0, 2, 1, 3)                              # hai dia vua can hien truoc, roi hai lan lap
    for n, j in enumerate(order):
        v, m = ROWS[j]; y = 480 + 180 * j
        at = 0.3 if n < 2 else M[1] - 0.1 + 0.4 * (n - 2)
        k = appear(t, at, 0.4)
        if k <= 0: continue
        text(d, (X0 - 20, y), f"gió {v} m/s", FS, INK, anchor="rm", alpha=k)
        L = KX * m * ease((t - at) / 0.6)
        if L > 2: d.rounded_rectangle([X0, y - 42, X0 + L, y + 42], radius=12, fill=A(BLUE if v == 0 else TEAL, k))
        if L > 200: text(d, (X0 + L - 16, y), vn(m), 60, WHITE, anchor="rm", alpha=appear(t, at + 0.5, 0.3))

# ---------------- canh 4: co che ----------------
def panel(d, t, x0, x1, windy, alpha=1.0, y0=420, ys=700, y1=900, back_arrow=True):
    d.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=A((247, 248, 252), alpha))
    d.rectangle([x0 + 4, ys, x1 - 4, y1 - 4], fill=A((214, 230, 250), alpha))
    d.line([(x0 + 4, ys), (x1 - 4, ys)], fill=A(WATER_D, alpha), width=6)
    for i in range(10):                                  # phan tu trong nuoc: rung tai cho
        px = x0 + 40 + (i % 5) * (x1 - x0 - 80) / 4 + 8 * math.sin(t * 9 + i)
        py = ys + 45 + (i // 5) * 85 + 8 * math.cos(t * 8 + 2 * i)
        dot(d, px, py, 16, A(BLUE, alpha), outline=A(WHITE, alpha))
    for i in range(4):                                   # phan tu nhanh thoat len thanh hoi
        u = (t * 0.55 + i / 4) % 1
        bx = x0 + 60 + i * (x1 - x0 - 120) / 3
        if windy:
            x = bx + u * u * 420; y = ys - 20 - u * (ys - y0 - 60)
            al = alpha * clamp((1 - u) / 0.2) * clamp((x1 - 20 - x) / 40)
        else:
            up = 1 - abs(1 - 2 * u)                       # len roi roi lai mat nuoc
            x = bx + 18 * math.sin(t * 2 + i); y = ys - 20 - up * (ys - y0 - 90)
            al = alpha
        if al > 0.02:
            for q in range(1, 4):                       # vet: phan tu nhanh
                dot(d, x - (8 * q if windy else 0), y + 14 * q, 16 - 3 * q, A(BLUE, al * (0.45 - 0.12 * q)))
            dot(d, x, y, 16, A(BLUE, al), outline=A(WHITE, al))
    if windy: wind(d, t, x0 + 120, x1 - 20, (y0 + 60, y0 + 125), alpha)

def s_coche(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (40, 250, 1040, 1200), fill=WHITE, outline=LIGHT, w=4)
    text(d, (290, 330), "Không gió", FS, INK); text(d, (790, 330), "Có gió", FS, DTEAL)
    panel(d, t, 70, 510, False, y0=400, ys=760, y1=980); panel(d, t, 570, 1010, True, y0=400, ys=760, y1=980)
    kq = appear(t, 2.0, 0.4)
    if kq > 0: arrow(d, (455, 470), (455, 690), A(ORANGE, kq), w=8, head=24)
    text(d, (290, 1045), "quay lại", FS, DORANGE, alpha=kq)
    if kq > 0: arrow(d, (390, 1045), (440, 760), A(ORANGE, kq * 0.6), w=5, head=16)
    dot(d, 300, 1135, 16, BLUE, outline=WHITE); text(d, (330, 1135), "phân tử nước", FS, INK, anchor="lm")
    text(d, (790, 1045), "bị cuốn đi", FS, DTEAL, alpha=appear(t, M[1], 0.4))

# ---------------- canh 5: bay "gio hat nuoc ra" (hai hinh canh nhau) ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    for j, (cx, lab, col) in enumerate(((285, "Hiểu lầm", DRED), (795, "Thật ra", DGREEN))):
        card(d, (cx - 245, 260, cx + 245, 1300), fill=WHITE, outline=col, w=6)
        text(d, (cx, 330), lab, 62, col)
        dish(d, cx, 16, dy=900)
        fan(d, t, cx + 150, 560, base=False)
        wind(d, t, cx - 200, cx + 40, (520, 580), 1.0)
    # trai: giot van ra khoi dia (dieu KHONG xay ra)
    for i in range(5):
        u = (t * 0.8 + i / 5) % 1
        x = 285 - 30 - u * 190; y = 835 - 160 * math.sin(math.pi * u) + 40 * u
        d.ellipse([x - 22, y - 30, x + 22, y + 26], fill=WATER_D)
    for i in range(3):                                   # mat nuoc gon song
        x = 210 + i * 70; d.arc([x - 30, 820, x + 30, 850], 180, 360, fill=WATER_D, width=6)
    text(d, (285, 1050), "giọt văng?", 62, DRED)
    kx = appear(t, 0.6, 0.3)
    if kx > 0:
        d.line([(110, 1120), (460, 1220)], fill=A(DRED, kx), width=10); d.line([(110, 1220), (460, 1120)], fill=A(DRED, kx), width=10)
    # phai: mat nuoc phang, chi phan tu hoi (da thoat) bi cuon
    for i in range(4):
        u = (t * 0.55 + i / 4) % 1
        x = 700 + i * 40 - u * 220; y = 820 - 40 - u * 260
        dot(d, x, y, 9, A(BLUE, clamp((1 - u) / 0.25)), outline=WHITE)
    ka = appear(t, M[1], 0.4)
    text(d, (795, 1050), "mặt nước phẳng", FS, DGREEN, alpha=ka)
    if ka > 0:
        d.line([(730, 1180), (780, 1230), (880, 1120)], fill=A(DGREEN, ka), width=12, joint="curve")

# ---------------- canh 6: chot (phu de) + THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 285, "THỬ NGHĨ", ORANGE, k1)
    if k1 > 0.5:
        d.rounded_rectangle([170, 420, 210, 720], radius=20, outline=NAVY, width=6, fill=WHITE)
        d.rectangle([181, 500, 199, 712], fill=RED); dot(d, 190, 750, 36, RED)
        dish(d, 520, M0, dy=760)
        fan(d, t, 860, 560, base=False)
        wind(d, t, 560, 760, (540, 600), 1.0)
    text(d, (190, 860), "40 °C", 66, RED, alpha=k1)
    text(d, (790, 760), "3 m/s", 66, DTEAL, alpha=k1)
    text(d, (W / 2, 1040), "Phòng 40 °C, gió 3 m/s:", 64, INK, alpha=k1)
    text(d, (W / 2, 1130), "sau 1 giờ còn nhiều hơn", 64, DORANGE, alpha=k1)
    text(d, (W / 2, 1220), "hay ít hơn 11,2 g?", 64, DORANGE, alpha=k1)
    text(d, (W / 2, 1310), "(ở 30 °C: còn 11,2 g)", FS, INK, alpha=k1)
    seg_bar(d, 1420, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, k, c, b, e = (sc[x] for x in ("hook", "do", "ket", "coche", "bay", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding")]
    tt = do["M"][0] + 0.3
    while tt < do["M"][1] - 0.3: out.append((do["t0"] + tt, "tick")); tt += 0.5
    out += [(do["t0"] + do["M"][1] + 0.1, "tap"), (k["t0"] + 0.3, "ding"), (c["t0"] + c["M"][1], "tap"),
            (b["t0"] + 0.6, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l12-chuyenthe-03", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Sự chuyển thể · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai đĩa nước, một chiếc quạt", draw=s_hook, tail=0.3, caps=[
   ("Hai đĩa nước, một đĩa trước quạt.", 3.0),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Chờ 1 giờ rồi cân", draw=s_do, tail=0.4, caps=[
   ("Bật quạt, giữ nguyên 1 giờ.", 3.4),
   ("Cân lại hai đĩa.", 3.6)]),
 dict(key="ket", title="Kết quả", draw=s_ket, tail=0.4, caps=[
   ("Đáp án: cả hai vơi, gió vơi hơn.", 4.2),
   ("Gió càng mạnh, còn càng ít.", 3.4)]),
 dict(key="coche", title="Vì sao gió làm khô nhanh?", draw=s_coche, tail=0.4, caps=[
   ("Phân tử nhanh thoát khỏi nước.", 3.8),
   ("Gió cuốn hơi đi.", 3.4)]),
 dict(key="bay", title="Bẫy: gió hất nước ra?", draw=s_bay, tail=0.4, caps=[
   ("Gió không hất giọt nước ra.", 3.4),
   ("Gió chỉ cuốn hơi đã thoát.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Chưa sôi, nước vẫn bay hơi.", 6.4)]),
])
