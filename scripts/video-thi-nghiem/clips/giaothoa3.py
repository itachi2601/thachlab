# Clip: tn-l11-giaothoa-03 - Khe Young voi laser: doi khoang cach toi man D (lo 11, 19/11/2026;
# dung lai 27/11/2026 theo cong moi: chu ve >= 55 px (ra >= 48), moi nhip >= 2,5 s, Du doan khong nut A-D (K10),
# thanh dem day 70 px, Bay hai khung tu giai thich, Gioi han rieng, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-giaothoa-03.json (_kiem_so() doi chieu mo_hinh i = lam.D/a):
#   so_lieu_mau (lam um, a mm, D m, i mm): 0,65 0,2 2 -> 6,5 ; 0,65 0,2 3 -> 9,75. Hai hang a = 0,4 va lam = 0,45 KHONG chieu
#   (cau Thu PhET ngay sau hop hoi doi mau va doi a). Do 5 van sang lien tiep = 4 khoang: 26 mm / 39 mm ; bay chia 5 ra
#   5,2 mm ; cau chot a = 0,1 mm -> 13 mm: cac so nay ghi trong ghi_chu kho.
# Bai l11-giao-thoa-song (lesson 31): hop exp o muc II.4, sau cong thuc i = lam.D/a. Tranh trung: Cau 1 (tat mot nguon),
#   Cau 2, 3 (mat nuoc), Cau 4 (a = 1 mm, D = 2 m, 0,5 um, x = 2,5 mm: van toi) -> clip khong noi van toi o k + 1/2.
#   (Ra lai 27/11: dong Quan sat cua hop exp nay chi con "cach deu (co vai mm)", khong con lo dap an Du doan.)
# Du doan (K10): doi man tu 2 m ra 3 m, khoang van i se ra sao? Dap an: rong ra (6,5 -> 9,75 mm).
# Bay (hien_tuong_hay_sai[2]): dem 5 van sang roi chia 5 -> thuc ra 4 khoang van. Khung tren (de tuong) / khung duoi (that).
# Gioi han: moi doi D, chua doi a va mau laser.
# THU NGHI (= cau_chot khung web): man van 2 m, laser cu; muon i = 13 mm thi hai khe cach nhau bao nhieu? -> 0,1 mm.
#   Buoc suy luan chua chieu: i ti le nghich a (clip khong hien cong thuc, chi doi D). 0,1 mm KHONG hien tren man.
from engine import *

LAM, A0 = 0.65, 0.2
ROWS = [(2, 26, 6.5), (3, 39, 9.75)]                 # (D m, 4 khoang mm, i mm)
DGREEN, DPURPLE, DRED, DORANGE = (21, 110, 55), (91, 33, 182), (185, 28, 28), (176, 64, 8)

def vn(x, nd=None):
    s = f"{x:.{nd}f}" if nd is not None else f"{x:g}"
    return s.replace(".", ",")

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-giaothoa-03.json")))
    hang = k["so_lieu_mau"]["hang"]; g = k["so_lieu_mau"]["ghi_chu"]
    for D, s4, i in ROWS:
        assert any(r == [LAM, A0, D, i] for r in hang), (D, i)
        assert abs(LAM * D / A0 - i) < 1e-9 and abs(4 * i - s4) < 1e-9
        assert f"{s4} mm" in g
    assert "5,2 mm" in g and abs(26 / 5 - 5.2) < 1e-9
    assert "a = 0,1 mm" in g and abs(LAM * 2 / 0.1 - 13) < 1e-9 and "13 mm" in g
    assert any("chia 5" in s for s in k["hien_tuong_hay_sai"])
_kiem_so()

def pill(d, cx, cy, s, size, fg, bg, a=1.0):
    pw = tw(d, s, F(size)) + 56
    card(d, (cx - pw / 2, cy - size * 0.82, cx + pw / 2, cy + size * 0.82), fill=A(bg, a), r=int(size * 0.8))
    text(d, (cx, cy), s, size, fg, alpha=a)

def cbar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem day 70 px, rut tu phai sang trai theo 10 nac (moi nac la mot thay doi hinh ro)."""
    p = clamp((t - t0) / (t1 - t0)); q = math.floor(p * 10 + 1e-9) / 10
    d.rounded_rectangle([140, y, 940, y + 70], radius=35, fill=A(LIGHT, a))
    if q < 1: d.rounded_rectangle([140, y, 140 + 800 * (1 - q), y + 70], radius=35, fill=A(col, a))

# ---------------- hinh ----------------
SX = 250; PD = 190                                     # x tam khe ; px / m cho D
def scr_x(D): return SX + D * PD
GX0, GX1, PMM = 90, 990, 15.0                          # dai van: 60 mm, 15 px/mm, van trung tam o x = 540
GC = (GX0 + GX1) / 2
DARK = (28, 12, 16); LRED = (255, 70, 50)

def inten(xmm, i):
    return math.cos(math.pi * xmm / i) ** 2 * math.exp(-(xmm / (5.5 * i)) ** 2)

def _kiem_van():
    for D, s4, i in ROWS:
        for k in range(-2, 3): assert abs(inten(k * i, i) - math.exp(-(k / 5.5) ** 2)) < 1e-9   # van sang o k.i
        assert inten(0.5 * i, i) < 1e-9                                                       # van toi o giua
        assert abs(4 * i * PMM / 2) <= (GX1 - GX0) / 2                                         # 5 van sang nam trong dai
        assert inten(2 * i, i) > 0.85                                                          # van thu 5 con du sang de dem
_kiem_van()

def fringes(d, y0, y1, i, a=1.0):
    for x in range(GX0, GX1 + 1, 2):
        d.line([(x, y0), (x, y1)], fill=mix(DARK, LRED, inten((x - GC) / PMM, i)), width=2)
    d.rectangle([GX0, y0, GX1, y1], outline=NAVY, width=3)

def mmruler(d, y):
    d.line([(GX0, y), (GX1, y)], fill=NAVY, width=3)
    for k in range(13):
        x = GX0 + k * 5 * PMM; L = 18 if k % 2 == 0 else 10
        d.line([(x, y), (x, y + L)], fill=NAVY, width=3)
        if k % 2 == 0 and k != 12: text(d, (x, y + 52), str(k * 5), 56, INK)
    text(d, (GX1, y + 52), "mm", 56, INK, anchor="rm")

YB = 400                                               # truc chum laser
def schematic(d, D, t, show_d=True):
    sx = scr_x(D)
    d.polygon([(SX + 6, YB - 6), (sx, YB - 85), (sx, YB + 85), (SX + 6, YB + 6)], fill=(255, 205, 195))
    d.line([(200, YB), (SX, YB)], fill=LRED, width=5)
    d.rounded_rectangle([70, YB - 28, 200, YB + 28], radius=10, fill=(70, 78, 100))
    d.rectangle([SX - 6, YB - 100, SX + 6, YB - 14], fill=NAVY); d.rectangle([SX - 6, YB - 6, SX + 6, YB + 6], fill=NAVY)
    d.rectangle([SX - 6, YB + 14, SX + 6, YB + 100], fill=NAVY)
    d.rectangle([sx, YB - 95, sx + 14, YB + 95], fill=(225, 225, 232), outline=NAVY, width=3)
    text(d, (70, 268), "hai khe, a = 0,2 mm", 56, INK, anchor="lm")
    text(d, (135, YB + 72), "laser", 56, INK)
    text(d, (sx + 34, YB), "màn", 56, INK, anchor="lm")
    u = (t * 0.9) % 1.0                                # cham sang chay tu khe toi man (hinh khong dung yen)
    dot(d, SX + 10 + u * (sx - SX - 20), YB, 24, LRED, outline=NAVY)
    y = 545
    d.line([(SX, y), (sx, y)], fill=NAVY, width=3)
    for x in (SX, sx): d.line([(x, y - 14), (x, y + 14)], fill=NAVY, width=3)
    if show_d:
        s = f"D = {D:g} m"; pw = tw(d, s, F(56)) + 30
        card(d, ((SX + sx) / 2 - pw / 2, y - 34, (SX + sx) / 2 + pw / 2, y + 34), fill=WHITE, r=14)
        text(d, ((SX + sx) / 2, y), s, 56, INK)

FY0, FY1 = 690, 790
def stage(d, D, i, t, show_d=True):
    card(d, (40, 215, 1040, 900), fill=WHITE, outline=LIGHT, w=3)
    schematic(d, D, t, show_d)
    fringes(d, FY0, FY1, i); mmruler(d, FY1 + 10)

def brack(d, i, lab, y=668):
    xa, xb = GC - 2 * i * PMM, GC + 2 * i * PMM
    d.line([(xa, y), (xb, y)], fill=ORANGE, width=6)
    for x in (xa, xb): d.line([(x, y - 14), (x, y + 20)], fill=ORANGE, width=6)
    pw = tw(d, lab, F(56)) + 30
    card(d, (GC - pw / 2, y - 74, GC + pw / 2, y - 14), fill=WHITE, r=14)
    text(d, (GC, y - 44), lab, 56, DORANGE)

# ---------------- canh 1: Du doan (K10: chi cau hoi, khong nut) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    stage(d, 2, 6.5, t)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 75, "DỰ ĐOÁN", 58, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 210), "Dời màn từ 2 m ra 3 m:", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 320), "khoảng vân i ra sao?", 64, DPURPLE, alpha=a)
    cbar(d, y0 + 440, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
B1, MV0, MV1, B2 = 2.6, 4.0, 5.6, 6.4                  # do lan 1 (+ ghi hang) ; doi man ; do lan 2 (+ ghi hang)
def do_state(t):
    """-> (D dang ve, dang dich man?, chi so lan do dang hien (-1 neu khong), so hang)."""
    if t < MV0: D, moving = 2.0, False
    elif t < MV1: D, moving = 2.0 + ease((t - MV0) / (MV1 - MV0)), True
    else: D, moving = 3.0, False
    meas = 0 if B1 <= t < MV0 else (1 if t >= B2 else -1)
    rows = (1 if t >= B1 else 0) + (1 if t >= B2 else 0)
    return D, moving, meas, rows

def itable(d, y, n, hl=-1):
    card(d, (60, y, 1020, y + 104 + 2 * 82), fill=WHITE, outline=NAVY, w=4)
    for x, s in ((190, "D (m)"), (500, "4 khoảng (mm)"), (850, "i (mm)")): text(d, (x, y + 52), s, 56, INK)
    d.line([(90, y + 100), (990, y + 100)], fill=LIGHT, width=4)
    for j in range(n):
        yy = y + 144 + j * 82; D, s4, i = ROWS[j]
        if j == hl: d.rounded_rectangle([80, yy - 36, 1000, yy + 36], radius=16, fill=(255, 237, 213))
        text(d, (190, yy), str(D), 58, INK); text(d, (500, yy), str(s4), 58, INK); text(d, (850, yy), vn(i), 58, BLUE)

def s_do(img, d, t, sc):
    D, moving, meas, rows = do_state(t)
    i = LAM * D / A0
    stage(d, D, i, t, show_d=not moving)
    if meas >= 0: brack(d, ROWS[meas][2], f"5 vân sáng: {ROWS[meas][1]} mm")
    itable(d, 940, rows, hl=rows - 1)

def _kiem_dong_bo():
    """Moi 0,05 s: so D chi hien khi man dung yen ; khoang do khop D dang ve ; hang ghi cung luc do."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        D, moving, meas, rows = do_state(t)
        if not moving and D not in (2.0, 3.0): bad.append((round(t, 2), "D le khi dung yen"))
        if meas >= 0 and (moving or D != ROWS[meas][0]): bad.append((round(t, 2), "lan do lech D"))
        if rows >= 1 and t < B1: bad.append((round(t, 2), "hang 1 som"))
        if rows == 2 and (t < B2 or D != 3.0): bad.append((round(t, 2), "hang 2 som"))
        t += 0.05
    if do_state(sc["T"] - 0.05)[3] != 2: bad.append("chua du 2 hang cuoi canh")
    if sc["T"] < B2 + 1.5: bad.append("hang cuoi hien qua ngan")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    card(d, (60, 215, 1020, 420), fill=WHITE, outline=NAVY, r=26, w=5)
    pill(d, W / 2, 272, "ĐÁP ÁN", 56, WHITE, NAVY)
    text(d, (W / 2, 368), "Rộng ra", 64, NAVY)
    card(d, (40, 450, 1040, 1010), fill=WHITE, outline=LIGHT, w=3)
    for j, (D, s4, i) in enumerate(ROWS):
        y = 560 + j * 250
        text(d, (GX0, y - 55), f"D = {D} m", 56, INK, anchor="lm")
        fringes(d, y, y + 90, i)
        u = ((t * 0.35 + 0.5 * j) % 1.0)                 # dau do chay doc dai van (hinh khong dung yen)
        dot(d, GX0 + 20 + u * (GX1 - GX0 - 40), y + 45, 9, WHITE)
        xa, xb = GC, GC + i * PMM
        d.line([(xa, y + 120), (xb, y + 120)], fill=ORANGE, width=6)
        for x in (xa, xb): d.line([(x, y + 104), (x, y + 136)], fill=ORANGE, width=6)
        text(d, (xb + 16, y + 122), f"i = {vn(i)} mm", 56, DORANGE, anchor="lm")
    kr = appear(t, M[1] - 0.1, 0.45)
    if kr > 0:
        card(d, (60, 1050, 1020, 1190), fill=A((236, 253, 243), kr), outline=A(GREEN, kr), r=26, w=5)
        text(d, (W / 2, 1120), "D gấp 1,5 → i gấp 1,5", 62, DGREEN, alpha=kr)

# ---------------- canh 4: Bay - "dem 5 van sang roi chia 5" ----------------
I0 = 6.5
def bpanel(d, y0, lab, col, fill, k):
    card(d, (40, y0, 1040, y0 + 460), fill=fill, outline=col, w=6)
    text(d, (75, y0 + 62), lab, 58, col, anchor="lm")
    fy = y0 + 200
    fringes(d, fy, fy + 90, I0)
    return fy

def s_bay(img, d, t, sc):
    M = sc["M"]
    # khung tren: de tuong - dem 5 van, chia 5
    fy = bpanel(d, 215, "✗ Dễ tưởng: chia 5", DRED, (254, 242, 242), 1)
    n1 = min(5, int((t - 0.3) / 0.5) + 1) if t > 0.3 else 0
    for k in range(n1):
        x = GC + (k - 2) * I0 * PMM; text(d, (x, fy - 40), str(k + 1), 56, DRED)
    text(d, (W / 2, fy + 175), "26 : 5 = 5,2 mm", 60, DRED)
    # khung duoi: that - dem khoang giua hai van, 4 khoang
    k2 = appear(t, M[1], 0.45)
    if k2 > 0:
        fy2 = bpanel(d, 715, "Đếm khoảng giữa vân", BLUE, WHITE, k2)
        n2 = min(4, int((t - M[1] - 0.3) / 0.55) + 1) if t > M[1] + 0.3 else 0
        for k in range(n2):
            x0, x1 = GC + (k - 2) * I0 * PMM, GC + (k - 1) * I0 * PMM
            d.arc([x0 + 6, fy2 - 40, x1 - 6, fy2 + 10], 180, 360, fill=ORANGE, width=6)
            text(d, ((x0 + x1) / 2, fy2 - 62), str(k + 1), 56, DORANGE)
        text(d, (W / 2, fy2 + 175), "26 : 4 = 6,5 mm", 60, BLUE)
    kc = appear(t, M[2] - 0.1, 0.45)
    if kc > 0:
        card(d, (60, 1215, 1020, 1345), fill=A((236, 253, 243), kc), outline=A(GREEN, kc), r=26, w=5)
        text(d, (W / 2, 1280), "✓ 5 vân sáng = 4 khoảng", 60, DGREEN, alpha=kc)

# ---------------- canh 5: Gioi han ----------------
def s_gioi(img, d, t, sc):
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 300), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 440), "Đổi màu laser thì sao?", 62, INK)
    card(d, (40, 600, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    fringes(d, 700, 800, I0)
    u = (t * 0.35) % 1.0
    dot(d, GX0 + 20 + u * (GX1 - GX0 - 40), 750, 18, WHITE, outline=NAVY)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 1300), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 290, "THỬ NGHĨ", 58, WHITE, ORANGE, k1)
    text(d, (W / 2, 480), "Màn vẫn 2 m, laser cũ.", 64, INK, alpha=k1)
    text(d, (W / 2, 600), "Muốn i = 13 mm, hai khe", 64, INK, alpha=k1)
    text(d, (W / 2, 720), "cách nhau bao nhiêu?", 64, DORANGE, alpha=k1)
    cbar(d, 1100, t, 1.2, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open")]
    out += [(do["t0"] + B1, "tap"), (do["t0"] + B2, "tap")]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.3, "buzz"), (b["t0"] + b["M"][2], "ding"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-giaothoa-03", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Giao thoa sóng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Khe Young với laser", draw=s_hook, tail=0.3, caps=[
   ("Laser đỏ qua hai khe, chiếu lên màn.", 3.6),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Đo năm vân sáng liền nhau.", 3.8),
   ("Dời màn ra 3 m, đo lại.", 4.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Màn xa hơn, vân giãn đều ra.", 3.6),
   ("Giao thoa được: ánh sáng là sóng.", 3.8)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Năm vân thì chia năm?", 3.2),
   ("Đếm khoảng, không đếm vân.", 3.2),
   ("Luôn ít hơn một.", 3.0)]),
 dict(key="gioi", title="Giới hạn", draw=s_gioi, tail=0.3, caps=[
   ("Chỉ mới đổi D.", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự tính.", 6.4)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
