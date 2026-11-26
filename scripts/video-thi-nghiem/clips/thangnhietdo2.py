# Clip: tn-l12-thangnhietdo-02 - Kiem nhiet ke o hai moc: nuoc da dang tan va hoi nuoc dang soi.
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-thangnhietdo-02.json (so lieu minh hoa):
#   so_lieu_mau: lan 1: 0,2 / 99,6 · lan 2: 0,1 / 99,7 · lan 3: 0,3 / 100,1 (°C); sai_so_dc = ±0,5 °C; p_kq = 101,325 kPa
#   mo_hinh: t_s ≈ 100 + (p_kq − 101,325)/3,6 -> 80 kPa: ≈ 94 °C (ca tu suy cho THU NGHI, ghi trong so_lieu_mau.ghi_chu).
# Ban 1 (14/11/2026). Ban 2 (26/11/2026, KE-HOACH-CAI-TIEN-CLIP viec 4 lo 32): cong --do-chu (chu ve >= 58 px,
#   <= 180 tu/phut moi canh, nhip >= 2 s), <= 50 s, K10 (khong nut A-D), bo canh "chua noi duoc" (giu trong khung web),
#   Bay ve hai hinh canh nhau: hieu sai (so doc = nhiet do tan) / dung (so doc ± 0,5 chua 0 °C).
# KHONG hien trung binh hoi nuoc (bai ghi "em tu tinh") va KHONG neu co che chuyen the (dap an Cau 2 ngay sau hop).
# Du doan (khung web): nhiet ke ±0,5 °C trong nuoc da dang tan, doc 3 lan: A dung 0,0 ca ba / B quanh 0, lech duoi 0,5 (DUNG)
#   / C tang dan / D duoi 0 °C.  -> nham thang hien_tuong_hay_sai[0] (doc 0,2 -> "da tan o 0,2").
# THU NGHI (= cau_chot khung): tren nui 80 kPa, hoi nuoc soi doc 94 °C -> nhiet ke KHONG hong (moc 100 °C chi dung o 1 atm).
from engine import *

ICE_R = (0.2, 0.1, 0.3)
STM_R = (99.6, 99.7, 100.1)
ICE_S = ("0,2", "0,1", "0,3")
STM_S = ("99,6", "99,7", "100,1")

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-thangnhietdo-02.json")))
    h = k["so_lieu_mau"]["hang"]
    assert tuple(r[1] for r in h) == ICE_R and tuple(r[2] for r in h) == STM_R
    ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert ts["sai_so_dc"]["gia_tri"] == 0.5 and ts["p_kq"]["mac_dinh"] == 101.325
    assert round(100 + (80 - 101.325) / 3.6) == 94
_kiem_so()

DGREEN = (10, 110, 50); DRED = (185, 28, 28); DORANGE = (176, 64, 8)
FS = 58
NOTE = (70, 75, 95)
SCREEN = (24, 30, 40); LCD = (134, 239, 172)

def pill(d, cx, cy, s, fill, alpha=1.0, size=56, fg=WHITE):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 38, cx + pw / 2, cy + 38), fill=A(fill, alpha), r=36)
    text(d, (cx, cy), s, size, fg, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (190, y, 890, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (190, y, 190 + max(70, 700 * q), y + 70), fill=A(col, a), r=35)

# ---------------- dung cu: coc nuoc da (trai) + coc nuoc soi tren bep (phai) ----------------
def beaker(d, x0, x1, y0, y1, wy, wcol):
    d.rectangle([x0 + 6, wy, x1 - 6, y1 - 6], fill=wcol)
    d.line([(x0 + 6, wy), (x1 - 6, wy)], fill=(110, 160, 220), width=4)
    d.line([(x0, y0), (x0, y1), (x1, y1), (x1, y0)], fill=(90, 120, 160), width=6, joint="curve")

def rig(d, t, n_read, hl=0.0, labels=1.0):
    """n_read: so lan doc da xong - 1 (-1 = chua doc). Ve trong y 270..900."""
    beaker(d, 90, 430, 520, 820, 560, (205, 230, 252))
    for (x, y, a) in ((140, 590, 10), (215, 640, 40), (380, 600, -15), (150, 740, 25), (390, 730, 5), (230, 770, -20)):
        pts = [(x + 28 * math.cos(math.radians(a + 45 + 90 * k)), y + 28 * math.sin(math.radians(a + 45 + 90 * k))) for k in range(4)]
        d.polygon(pts, fill=(240, 248, 255), outline=(150, 190, 230))
    d.line([(300, 400), (300, 742)], fill=(90, 96, 110), width=9)
    dot(d, 300, 746, 10, NAVY)
    d.rounded_rectangle([660, 824, 980, 850], radius=8, fill=(234, 88, 12))
    beaker(d, 650, 990, 520, 820, 700, (190, 218, 248))
    for k in range(6):
        ph = (t * 0.9 + k * 0.31) % 1
        x = 690 + k * 50 + 6 * math.sin(t * 5 + k); y = lerp(805, 712, ph)
        d.ellipse([x - 7, y - 7, x + 7, y + 7], outline=WHITE, width=3)
    for k in range(4):
        ph = (t * 0.5 + k * 0.25) % 1
        cx = 700 + k * 75; cy = lerp(690, 540, ph)
        d.ellipse([cx - 34, cy - 18, cx + 34, cy + 18], fill=A((150, 160, 180), 0.6 * (1 - ph)))
    text(d, (960, 470), "hơi", FS, NOTE)
    d.line([(860, 400), (860, 628)], fill=(90, 96, 110), width=9)
    dot(d, 860, 632, 10, NAVY)
    if hl > 0: d.ellipse([820, 594, 900, 670], outline=A(ORANGE, hl), width=6)
    for cx, s in ((260, "—" if n_read < 0 else ICE_S[n_read]), (820, "—" if n_read < 0 else STM_S[n_read])):
        card(d, (cx - 160, 290, cx + 160, 400), fill=SCREEN, r=16)
        text(d, (cx - 20, 345), s, 62, LCD)
        text(d, (cx + 115, 345), "°C", FS, LCD)
    text(d, (260, 885), "nước đá tan", FS, NAVY, alpha=labels)
    text(d, (820, 905), "hơi nước sôi", FS, NAVY, alpha=labels)

# ---------------- dai sai so ----------------
def strip(d, y, lo, hi, ticks, col, title, ka=1.0, band=None, x0=130, x1=950):
    Xs = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    text(d, (x0 - 60, y - 110), title, FS, NOTE, anchor="lm", alpha=ka)
    if band: d.rounded_rectangle([Xs(band[0]), y - 34, Xs(band[1]), y + 34], radius=12, fill=mix(GREEN, WHITE, 0.72))
    d.line([(x0, y), (x1, y)], fill=INK, width=4)
    for v, s in ticks:
        d.line([(Xs(v), y - 14), (Xs(v), y + 14)], fill=INK, width=4)
        text(d, (Xs(v), y + 66), s, FS, NOTE, alpha=ka)
    return Xs

ICE_T = ((-0.5, "−0,5"), (0, "0"), (0.5, "0,5"))
STM_T = ((99.5, "99,5"), (100, "100"), (100.5, "100,5"))

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    rig(d, t, -1)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1000 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 520), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, k)
    text(d, (W / 2, y0 + 180), "Đọc 3 lần trong nước đá:", 64, INK, alpha=k)
    text(d, (W / 2, y0 + 285), "số đọc ra sao?", 66, PURPLE, alpha=k)
    seg_bar(d, y0 + 400, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: Tien hanh ----------------
READ = (1.0, 3.2, 5.4)
def s_do(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    n = -1
    for j, a in enumerate(READ):
        if t >= a: n = j
    rig(d, t, n, hl=appear(t, M[1], 0.4), labels=0.0)
    ka = appear(t, 0.3, 0.3)
    card(d, (40, 960, 1040, 1580), fill=WHITE, outline=LIGHT, w=3)
    for x, s in ((150, "Lần"), (450, "Nước đá"), (820, "Hơi nước")): text(d, (x, 1020), s, FS, NOTE, alpha=ka)
    d.line([(70, 1065), (1010, 1065)], fill=LIGHT, width=3)
    for j in range(n + 1):
        y = 1125 + 84 * j
        if j == n: d.rounded_rectangle([60, y - 38, 1020, y + 38], radius=14, fill=(255, 237, 213))
        text(d, (150, y), str(j + 1), FS, INK); text(d, (450, y), ICE_S[j], FS, BLUE); text(d, (820, y), STM_S[j], FS, DORANGE)
    text(d, (W / 2, 1520), "áp kế: 101,325 kPa", FS, NAVY, alpha=ka)

# ---------------- canh 3: Dap an ----------------
def s_ket(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]; ka = appear(t, 0.3, 0.3)
    card(d, (40, 250, 1040, 1300), fill=WHITE, outline=LIGHT, w=3)
    X1 = strip(d, 560, -1.0, 1.0, ICE_T, BLUE, "Nước đá (°C)", ka, band=(-0.5, 0.5))
    X2 = strip(d, 1040, 99.0, 101.0, STM_T, DORANGE, "Hơi nước (°C)", ka, band=(99.5, 100.5))
    for j in range(3):
        k1 = appear(t, 0.6 + 0.5 * j, 0.3); k2 = appear(t, 2.1 + 0.5 * j, 0.3)
        if k1 > 0.05: dot(d, X1(ICE_R[j]), 560, 20 * k1, BLUE, outline=WHITE)
        if k2 > 0.05: dot(d, X2(STM_R[j]), 1040, 20 * k2, ORANGE, outline=WHITE)
    # nhan nhay theo lan doc dang xet (giu hinh khong dung yen)
    for Xs, yy, x_lab in ((X1, 560, 0.5), (X2, 1040, 100.5)):
        text(d, (Xs(x_lab) + 10, yy - 70), "±0,5", FS, DGREEN, anchor="lm", alpha=ka)
    j = int(max(0, t - 3.6) / 1.0) % 3
    if t > 3.6:
        d.ellipse([X1(ICE_R[j]) - 34, 526, X1(ICE_R[j]) + 34, 594], outline=DGREEN, width=6)
        d.ellipse([X2(STM_R[j]) - 34, 1006, X2(STM_R[j]) + 34, 1074], outline=DGREEN, width=6)

# ---------------- canh 4: Rut ra (hai moc quy uoc) ----------------
def s_rut(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]; ka = appear(t, 0.3, 0.3)
    card(d, (40, 250, 1040, 1560), fill=WHITE, outline=LIGHT, w=3)
    tx, ty0, ty1 = 260, 400, 1340                          # nhiet ke dung: 100 °C o tren, 0 °C o duoi
    Y = lambda v: lerp(ty1 - 80, ty0 + 80, v / 100)
    d.rounded_rectangle([tx - 34, ty0, tx + 34, ty1], radius=34, fill=(236, 240, 246), outline=NAVY, width=4)
    dot(d, tx, ty1 + 30, 56, RED)
    v = 50 + 50 * math.sin(t * 1.5 - 1.2)
    d.rectangle([tx - 22, Y(v), tx + 22, ty1], fill=RED)
    for vv, lab, sub, col in ((100, "100 °C", "hơi nước sôi, 1 atm", DORANGE), (0, "0 °C", "nước đá tan", BLUE)):
        y = Y(vv)
        d.rounded_rectangle([tx - 70, y - 60, tx + 70, y + 60], radius=16, fill=mix(GREEN, WHITE, 0.72))
        d.line([(tx - 70, y), (tx + 90, y)], fill=INK, width=5)
        text(d, (tx + 120, y - 34), lab, 64, col, anchor="lm", alpha=ka)
        text(d, (tx - 90, y), "±0,5", FS, DGREEN, anchor="rm", alpha=appear(t, M[1], 0.4))
        text(d, (tx + 120, y + 40), sub, FS, NOTE, anchor="lm", alpha=ka)

# ---------------- canh 5: Bay (hai hinh canh nhau) ----------------
def vaxis(d, cx, y0, y1, k=1.0):
    Y = lambda v: lerp(y1, y0, (v + 1) / 2)
    d.line([(cx - 120, y0), (cx - 120, y1)], fill=INK, width=4)
    for v, s in ((0.5, "0,5"), (0, "0"), (-0.5, "−0,5")):
        d.line([(cx - 134, Y(v)), (cx - 106, Y(v))], fill=INK, width=4)
        text(d, (cx - 150, Y(v)), s, FS, NOTE, anchor="rm", alpha=k)
    return Y

def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]; ka = appear(t, 0.3, 0.3)
    j = 0 if t < M[1] else int((t - M[1]) / 1.3) % 3; r = ICE_R[j]
    for cx, lab, col in ((285, "Hiểu sai", DRED), (795, "Đúng", DGREEN)):
        card(d, (cx - 245, 250, cx + 245, 1330), fill=WHITE, outline=col, w=6)
        text(d, (cx, 320), lab, 62, col, alpha=ka)
        card(d, (cx - 150, 400, cx + 150, 500), fill=SCREEN, r=16)
        text(d, (cx, 450), ICE_S[j] + " °C", 62, LCD)
    Yl = vaxis(d, 330, 640, 1160, ka)
    dot(d, 330 - 120, Yl(r), 18, BLUE, outline=WHITE)
    for rr in ICE_R:
        if rr != r: dot(d, 330 - 120, Yl(rr), 12, A(BLUE, 0.35))
    d.line([(330 - 120, Yl(r)), (470, Yl(r))], fill=DRED, width=5)
    if t < M[1] + 0.3:
        text(d, (300, 590), "đá tan ở 0,2", FS, DRED, alpha=ka)
        cx_, cy_ = 450, Yl(r) + 60
        d.line([(cx_ - 22, cy_ - 22), (cx_ + 22, cy_ + 22)], fill=DRED, width=8); d.line([(cx_ - 22, cy_ + 22), (cx_ + 22, cy_ - 22)], fill=DRED, width=8)
    text(d, (285, 1250), "mỗi lần một số", FS, DRED, alpha=ka)
    Yr = vaxis(d, 840, 640, 1160, ka)
    kb = appear(t, M[1], 0.4)
    x = 840 - 120
    d.rounded_rectangle([x - 26, Yr(r + 0.5), x + 26, Yr(r - 0.5)], radius=12, fill=mix(GREEN, WHITE, 0.6))
    dot(d, x, Yr(r), 18, BLUE, outline=WHITE)
    if kb > 0:
        d.line([(x, Yr(0)), (x + 150, Yr(0))], fill=A(DGREEN, kb), width=6)
        text(d, (x + 170, Yr(0)), "0 °C", FS, DGREEN, anchor="lm", alpha=kb)
    text(d, (795, 1250), "vẫn chứa 0", FS, DGREEN, alpha=kb)

# ---------------- canh 6: chot + THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 285, "THỬ NGHĨ", ORANGE, k1)
    d.polygon([(130, 820), (330, 470), (530, 820)], fill=A((180, 190, 205), k1))
    d.polygon([(285, 549), (330, 470), (375, 549), (350, 538), (330, 560), (310, 538)], fill=A(WHITE, k1))
    pill(d, 330, 890, "80 kPa", NAVY, k1, size=FS)
    for k in range(4):                                    # hoi nuoc boc len (hinh khong dung yen)
        ph = (t * 0.5 + k * 0.25) % 1
        cx = 700 + k * 70; cy = lerp(800, 520, ph)
        d.ellipse([cx - 34, cy - 18, cx + 34, cy + 18], fill=A((150, 160, 180), 0.6 * (1 - ph) * k1))
    card(d, (640, 820, 960, 930), fill=A(SCREEN, k1), r=16)
    text(d, (800, 875), "94 °C", 64, LCD, alpha=k1)
    text(d, (W / 2, 1060), "Trên núi, hơi nước sôi", 64, INK, alpha=k1)
    text(d, (W / 2, 1150), "chỉ 94 °C:", 64, INK, alpha=k1)
    text(d, (W / 2, 1250), "nhiệt kế hỏng không?", 66, DORANGE, alpha=k1)
    seg_bar(d, 1370, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, k, r, b, e = (sc[x] for x in ("hook", "do", "ket", "rut", "bay", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding")]
    out += [(do["t0"] + a, "tap") for a in READ]
    out += [(k["t0"] + k["M"][0], "ding"), (r["t0"] + r["M"][1], "tap"), (b["t0"] + 0.4, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l12-thangnhietdo-02", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Thang nhiệt độ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Kiểm nhiệt kế ở hai mốc", draw=s_hook, tail=0.3, caps=[
   ("Nhiệt kế có sai số.", 3.4),
   ("Dừng lại, tự đoán.", 5.2)]),
 dict(key="do", title="Đọc ba lần", draw=s_do, tail=0.4, caps=[
   ("Đọc 3 lần, cách nhau 1 phút.", 3.8),
   ("Bầu nhiệt kế nằm trong hơi.", 3.8)]),
 dict(key="ket", title="Kết quả", draw=s_ket, tail=0.4, caps=[
   ("Đáp án: quanh 0 °C, lệch dưới 0,5.", 4.0),
   ("Cả sáu số nằm trong dải xanh.", 3.6)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.4, caps=[
   ("Hai mốc do Celsius quy ước.", 3.6),
   ("Lệch nhỏ nằm trong sai số dụng cụ.", 4.0)]),
 dict(key="bay", title="Bẫy: đá tan ở 0,2 °C?", draw=s_bay, tail=0.4, caps=[
   ("Đọc 0,2 rồi nói: đá tan ở 0,2 °C.", 3.8),
   ("Số đọc ±0,5 vẫn chứa 0 °C.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự nghĩ.", 5.8)]),
])
