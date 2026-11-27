# Clip: tn-l10-dongluong-01 - Xe tren ray dem khi bat vao dem lo xo gan cam bien luc (31/10/2026;
# dung lai 27/11/2026 theo cong moi L10b: chu >= 55 px khi ve, K10 khong nut A-D, chot A-D o khung).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-dongluong-01.json (_kiem_so() doi chieu):
#   tham_so: m = 0,250 kg (co dinh), v1 0,2..1,2 m/s, e 0..1 ; so_lieu_mau v1 / v2 / cam bien:
#   0,40/-0,32/0,176 ; 0,60/-0,49/0,268 ; 0,80/-0,63/0,352 ; 1,00/-0,81/0,445 ; rut_ra: lech 1,5-2,2 %.
# Du doan (DOI 27/11): ban cu hoi |dp| lan 1 = 0,18 -> trung "Bam xem nhan xet" (0,180 ; 0,2725 ...) cua bai.
#   Moi: luc nen va luc bat ra, dem day xe huong nao? (rut_ra[1] + hien_tuong_hay_sai[1]). Dap an: ca hai luc
#   deu nguoc chieu duong (chieu xe toi). Khung: A cung chieu ; B nguoc chieu (DUNG) ; C nen nguoc, bat ra cung ;
#   D bang 0 luc xe dung.
# Ket qua: bang 4 lan v1, v2, cam bien (KHONG ghi |dp|: hop bai de HS tinh, Bam xem co so) ; |dp| khop, lech 1,5-2,2 %.
# Bay = hien_tuong_hay_sai[0]: 0,250 . (0,40 - 0,32) = 0,02 -> dung 0,250 . (-0,32 - 0,40), |dp| = 0,180 (ghi_chu).
#   Chua noi duoc: ray co ma sat (gia_thiet mo hinh).
# Cau chot (tham_so trong mien: v1 = 0,50 m/s, e = 0 -> xe dinh vao dem): |dp| = 0,250 . 0,50 = 0,125 kg.m/s,
#   buoc "dinh vao dem -> v2 = 0" chua chieu ; 0,125 khong hien tren man.
from engine import *

M_XE = 0.250
ROWS = [(0.40, -0.32, 0.176), (0.60, -0.49, 0.268), (0.80, -0.63, 0.352), (1.00, -0.81, 0.445)]
CHOT_V = 0.50

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-dongluong-01.json")))
    for r, h in zip(ROWS, k["so_lieu_mau"]["hang"]): assert all(abs(a - b) < 1e-9 for a, b in zip(r, h)), ("lech kho", r)
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert abs(ts["m"]["gia_tri"] - M_XE) < 1e-9
    assert ts["v1"]["min"] <= CHOT_V <= ts["v1"]["max"] and ts["e"]["min"] == 0.0
    assert "0,180" in k["so_lieu_mau"]["ghi_chu"] and "1,5–2,2" in k["cac_buoc"]["rut_ra"][0]
    assert "0,40 − 0,32" in k["hien_tuong_hay_sai"][0]
    assert round(M_XE * (ROWS[0][0] - ROWS[0][1]), 3) == 0.180 and round(M_XE * CHOT_V, 3) == 0.125
_kiem_so()

CART = (59, 130, 246); CART_D = (30, 64, 175)
RAIL = (196, 200, 212); RAIL_D = (150, 155, 170)
NOTE = (60, 64, 84); DGREEN = (21, 110, 55); DRED = (185, 28, 28); LCD = (134, 239, 172); EMPTY = (148, 140, 128)
XFREE, XBLK = 760, 900          # dau tu do lo xo / mat cam bien
CW = 170                        # be rong xe
GX = 430                        # cong quang

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

# ---------------- hinh: ray, xe, dem lo xo + cam bien, cong quang ----------------
def ray(d, yr, comp=0.0, gate=False, axis=True):
    d.rectangle([50, yr, XBLK, yr + 26], fill=RAIL, outline=RAIL_D, width=3)
    for x in range(80, XBLK - 20, 46): d.ellipse([x - 4, yr + 9, x + 4, yr + 17], fill=RAIL_D)
    d.rectangle([XBLK, yr - 150, 1030, yr + 40], fill=NAVY)                    # cam bien luc gan tuong
    d.rectangle([XBLK - 14, yr - 75, XBLK, yr - 20], fill=GRAY)
    x0 = XFREE - comp; n = 12; pts = []
    for i in range(n + 1):
        x = lerp(x0, XBLK - 14, i / n); pts.append((x, yr - 47 + (0 if i in (0, n) else (18 if i % 2 else -18))))
    d.line(pts, fill=INK, width=5)
    d.rectangle([x0 - 8, yr - 75, x0, yr - 18], fill=INK)
    text(d, (1030, yr - 190), "cảm biến lực", 56, INK, anchor="rm")
    if gate:
        d.rectangle([GX - 11, yr - 235, GX + 11, yr - 105], fill=(71, 85, 105))
        d.rectangle([GX - 22, yr - 145, GX + 22, yr - 108], fill=(71, 85, 105))
        dot(d, GX, yr - 126, 7, RED)
    if axis:
        arrow(d, (80, yr + 85), (250, yr + 85), INK, w=6, head=20)
        text(d, (275, yr + 85), "chiều dương", 56, INK, anchor="lm")

def xe(d, xr, yr):
    xl = xr - CW
    d.rounded_rectangle([xl, yr - 88, xr, yr - 2], radius=12, fill=CART, outline=NAVY, width=4)
    xm = xl + CW / 2
    d.rectangle([xm - 6, yr - 150, xm + 6, yr - 88], fill=INK)                 # tam chan sang

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; yr = 700
    card(d, (40, 265, 1040, 930), fill=WHITE, outline=LIGHT, w=3)
    g = ease((t - 0.5) / 2.2); xr = lerp(260, XFREE, g)
    ray(d, yr); xe(d, xr, yr)
    arrow(d, (xr - CW / 2 - 70, yr - 270), (xr - CW / 2 + 90, yr - 270), BLUE, w=8, head=24)
    text(d, (xr - CW / 2 + 10, yr - 330), "v₁", 60, BLUE)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 965 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 200), "Lúc nén và lúc bật ra,", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 290), "đệm đẩy xe hướng nào?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 410, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (lan 1, quay cham) ----------------
X_START, V_IN = 230, 360.0                # px/s luc toi ; luc ve 0,8 lan (0,32 / 0,40)
TA = (XFREE - X_START) / V_IN
TC = 1.5
V_OUT = V_IN * 0.32 / 0.40
X_END = 230
CMAX = 70
U0 = 0.5

def motion(u):
    if u <= 0: return X_START, 0.0, 0
    if u < TA: return X_START + V_IN * u, 0.0, 1
    u -= TA
    if u < TC:
        c = CMAX * math.sin(math.pi * u / TC); return XFREE - c, c, 2
    u -= TC
    return max(X_END, XFREE - V_OUT * u), 0.0, 3

def doc_cong(u):
    xr, _, ph = motion(u); xm = xr - CW / 2
    return (ph >= 2 or (ph == 1 and xm > GX + 10)), (ph == 3 and xm < GX - 10)

G_X0, G_X1, G_Y0, G_YT = 150, 960, 1420, 300
G_PAD = 0.5
def gx(u): return G_X0 + (u + G_PAD) / (TC + 2 * G_PAD) * (G_X1 - G_X0)
def gF(u): return G_YT * math.sin(math.pi * u / TC) if 0 <= u <= TC else 0.0

def s_do(img, d, t, sc):
    yr = 760; u = t - U0
    card(d, (40, 265, 1040, 900), fill=WHITE, outline=LIGHT, w=3)
    xr, comp, ph = motion(u)
    ray(d, yr, comp, gate=True); xe(d, xr, yr)
    v1, v2 = doc_cong(u)
    for x, lab, val, on in ((190, "v₁ (m/s)", "0,40", v1), (560, "v₂ (m/s)", "−0,32", v2)):
        text(d, (x, 320), lab, 56, INK)
        card(d, (x - 120, 360, x + 120, 440), fill=NAVY, r=14)
        text(d, (x, 400), val if on else "—", 56, YELLOW if on else GRAY)
    text(d, (880, 400), "m = 0,250 kg", 56, INK)
    # do thi F - t
    card(d, (40, 930, 1040, 1530), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 985), "diện tích = xung lượng (N·s)", 56, INK)
    arrow(d, (G_X0, G_Y0), (G_X1 + 30, G_Y0), INK, w=4, head=16)
    arrow(d, (G_X0, G_Y0), (G_X0, G_Y0 - G_YT - 60), INK, w=4, head=16)
    text(d, (G_X0 + 24, G_Y0 - G_YT - 50), "F (N)", 56, INK, anchor="lm")
    text(d, (G_X1 + 10, G_Y0 + 50), "t (s)", 56, INK, anchor="rm")
    uc = u - TA
    if uc > -G_PAD:
        ue = min(uc, TC + G_PAD)
        if uc >= TC:
            poly = [(gx(0), G_Y0)] + [(gx(TC * i / 60), G_Y0 - gF(TC * i / 60)) for i in range(61)] + [(gx(TC), G_Y0)]
            d.polygon(poly, fill=A((253, 186, 116), appear(uc, TC, 0.5)))
        n = 120; pts = [(gx(-G_PAD + (ue + G_PAD) * i / n), G_Y0 - gF(-G_PAD + (ue + G_PAD) * i / n)) for i in range(n + 1)]
        d.line(pts, fill=RED, width=6); dot(d, pts[-1][0], pts[-1][1], 9, RED)
        if uc >= TC: text(d, (gx(TC / 2), G_Y0 - 100), "0,176 N·s", 60, INK, alpha=appear(uc, TC + 0.2, 0.5))

# ---------------- canh 3: Ket qua ----------------
XS = (170, 420, 670, 900)
def s_kq(img, d, t, sc):
    M = sc["M"]; yr = 560
    card(d, (40, 265, 1040, 760), fill=WHITE, outline=LIGHT, w=3)
    ray(d, yr, 55, axis=False); xe(d, XFREE - 55, yr)
    arrow(d, (XFREE - 55 - 30, yr - 45), (XFREE - 55 - 260, yr - 45), RED, w=10, head=28)
    text(d, (250, yr - 140), "lực đệm", 60, RED)
    text(d, (W / 2, yr + 90), "ngược chiều dương", 60, DRED)
    text(d, (W / 2, yr + 165), "lúc nén lẫn lúc bật ra", 56, NOTE)
    ka = appear(t, M[1] - 0.1, 0.45)
    if ka > 0:
        y = 790
        card(d, (40, y, 1040, y + 560), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=3)
        for x, lab, unit, col in ((XS[0], "Lần", "", INK), (XS[1], "v₁", "m/s", BLUE), (XS[2], "v₂", "m/s", GREEN),
                                  (XS[3], "cảm biến", "N·s", ORANGE)):
            text(d, (x, y + 55), lab, 58, col, alpha=ka)
            if unit: text(d, (x, y + 118), unit, 56, col, bold=False, alpha=ka)
        d.line([(70, y + 160), (1010, y + 160)], fill=A(LIGHT, ka), width=3)
        for j, (v1, v2, J) in enumerate(ROWS):
            k = appear(t, M[1] + 0.2 + 0.35 * j, 0.4); yy = y + 220 + j * 90
            text(d, (XS[0], yy), str(j + 1), 58, INK, alpha=k)
            text(d, (XS[1], yy), f"{v1:.2f}".replace(".", ","), 58, BLUE, alpha=k)
            text(d, (XS[2], yy), f"−{-v2:.2f}".replace(".", ","), 58, DRED, alpha=k)
            text(d, (XS[3], yy), f"{J:.3f}".replace(".", ","), 58, ORANGE, alpha=k)
    kb = appear(t, M[2] - 0.1, 0.45)
    if kb > 0:
        card(d, (40, 1380, 1040, 1640), fill=A((236, 253, 243), kb), outline=A(GREEN, kb), w=5)
        text(d, (W / 2, 1460), "|Δp| = m·|v₂ − v₁|", 60, INK, alpha=kb)
        text(d, (W / 2, 1560), "Δp: biến thiên động lượng", 56, DGREEN, alpha=kb)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.3, 0.45)
    card(d, (40, 265, 1040, 600), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pill(d, W / 2, 335, "BẪY", RED, a1)
    q = "Δp = 0,250 · (0,40 − 0,32)"
    ks = clamp((t - M[1]) / 0.4); lw = tw(d, q, F(62)); yy = 470
    text(d, (W / 2, yy), q, 62, mix(INK, DRED, ks), alpha=a1)
    text(d, (W / 2, yy + 75), "m (kg) · tốc độ (m/s)", 56, NOTE, alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
    kk = appear(t, M[1] + 0.1, 0.45)
    if kk > 0:
        card(d, (40, 640, 1040, 1230), fill=A(WHITE, kk), outline=A(NAVY, kk), w=5)
        arrow(d, (120, 730), (300, 730), A(INK, kk), w=6, head=20)
        text(d, (325, 730), "chiều dương", 56, INK, anchor="lm", alpha=kk)
        arrow(d, (140, 840), (340, 840), A(BLUE, kk), w=9, head=24)
        text(d, (380, 840), "v₁ = +0,40 m/s", 60, BLUE, anchor="lm", alpha=kk)
        arrow(d, (300, 945), (140, 945), A(GREEN, kk), w=9, head=24)
        text(d, (380, 945), "v₂ = −0,32 m/s", 60, DGREEN, anchor="lm", alpha=kk)
        text(d, (W / 2, 1060), "Δp = 0,250 · (−0,32 − 0,40)", 60, DGREEN, alpha=kk)
        text(d, (W / 2, 1160), "|Δp| = 0,180 kg·m/s ✓", 62, DGREEN, alpha=kk)
    k5 = appear(t, M[2] + 0.1, 0.45)
    if k5 > 0:
        y0 = 1270 + (1 - k5) * 30
        card(d, (40, y0, 1040, y0 + 290), fill=A(WHITE, k5), outline=A(NAVY, k5), w=6)
        pill(d, W / 2, y0 + 70, "CHƯA NÓI ĐƯỢC", NAVY, k5)
        text(d, (W / 2, y0 + 200), "ray có ma sát thì sao", 60, INK, alpha=k5)

# ---------------- canh 5: THU NGHI (cau chot o khung web: |dp| = 0,125) ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; yr = 720
    card(d, (40, 265, 1040, 930), fill=WHITE, outline=LIGHT, w=3)
    ray(d, yr); xe(d, 560, yr)
    arrow(d, (300, yr - 290), (500, yr - 290), BLUE, w=8, head=24)
    text(d, (520, yr - 290), "0,50 m/s", 60, BLUE, anchor="lm")
    y0 = 965
    card(d, (40, y0, 1040, 1665), fill=WHITE, outline=ORANGE, w=6)
    pill(d, W / 2, y0 + 70, "THỬ NGHĨ", ORANGE)
    k1 = appear(t, 2.6, 0.45)
    text(d, (W / 2, y0 + 195), "Xe 0,250 kg dính đệm, dừng hẳn.", 60, INK, alpha=k1)
    k2 = appear(t, 5.0, 0.45)
    text(d, (W / 2, y0 + 300), "|Δp| của xe bằng bao nhiêu?", 62, ORANGE, alpha=k2)
    seg_bar(d, y0 + 370, t, 5.2, sc["T"] - 0.2, ORANGE, k2)
    kh = appear(t, 7.5, 0.45)
    if kh > 0:
        card(d, (90, y0 + 475, 990, y0 + 680), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, y0 + 530), "Gợi ý", 56, INK, alpha=kh)
        text(d, (W / 2, y0 + 620), "viết v₁, v₂ trước khi tính", 58, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, kq, b, e = sc["hook"], sc["do"], sc["kq"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + U0 + TA, "tap"), (do["t0"] + U0 + TA + TC, "tap"),
            (kq["t0"] + 0.4, "ding"), (b["t0"] + b["M"][1], "buzz"), (e["t0"] + 5.0, "open")]

CLIP = dict(id="tn-l10-dongluong-01", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Động lượng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Xe bật vào đệm lò xo", draw=s_hook, tail=0.3, caps=[
   ("Xe chạy tới nén đệm.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Cổng quang đo v₁ và v₂.", 3.4),
   ("Cảm biến vẽ đồ thị lực.", 3.4)]),
 dict(key="kq", title="Kết quả", draw=s_kq, tail=0.5, caps=[
   ("Đáp án: đệm đẩy ngược lại.", 3.4),
   ("Bốn lần, v₂ đều âm.", 3.4),
   ("|Δp| khớp cảm biến.", 3.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 3.0),
   ("Sai: v₂ ngược chiều, mang dấu trừ.", 4.0),
   ("Thí nghiệm này còn thiếu gì?", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Lần đo mới.", 4.6),
   ("Dừng lại, tự tính.", 4.8)]),
])
