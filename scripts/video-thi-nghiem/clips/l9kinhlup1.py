# Clip: tn-l9-kinhlup-01 - Do tieu cu kinh lup ghi 5x bang anh bong den o xa (KHTN 9, lo 5, 18/11/2026)
# Dung lai 27/11/2026 theo cong moi (viec 4, L9 nhom D): chu than canh >= 55 (ra >= 48 px), K10 (khong nut A-D),
#   moi nhip >= 2,5 s, Bay hai o canh nhau, bo canh tinh cuoi (cau chot A-D o khung web).
# So lieu tu content/thi-nghiem/tn-l9-kinhlup-01.json:
#   tham_so: f = 5,0 cm ; D = 300 cm (den -> kinh) ; mo_hinh d' = D.f/(D - f) = 5,08 cm (vi tri anh ro nhat)
#   so_lieu_mau: 5 lan do kinh -> giay = 5,2 ; 5,0 ; 5,3 ; 5,1 ; 5,0 cm
# Du doan (doi 27/11): dich giay tu sat kinh (2 cm) ra xa (9 cm), vet sang tren giay doi the nao?
#   -> nho dan, ro net o mot cho, roi to ra. (Khong hoi "anh the nao" vi Cau 3 cua bai hoi dung bo phuong an
#   that/ao - cung/nguoc - lon/nho.)
# Cau hoi ngay sau hop trong bai: "Trung binh? G co khop 5x? Vi sao so do hoi lon hon 5 cm?" -> clip KHONG tinh trung
#   binh, KHONG tinh G, KHONG noi "den chua du xa". Bay dung hien_tuong_hay_sai[2] (giay o cho vet to nhat).
# Hinh: truc ngang dung ti le sau thau kinh (60 px/cm); den o 3 m ve sau dau ngat truc. Tia tu den (diem tren truc,
#   cach 300 cm) toi kinh roi hoi tu tai d' = 5,08 cm; vet sang tren giay = giao cua chum voi giay.
# THU NGHI = cau chot (kho ghi_chu): kinh ghi 2x, den van 3 m -> f = 25/2 = 12,5 cm, giay cach kinh khoang 12,5 cm
#   (mo hinh d' = 300.12,5/287,5 = 13,0 cm). Buoc suy luan chua chieu: tu so ghi 2x ra f. Man chot KHONG ghi G = 25/f.
from engine import *
from PIL import ImageFilter

AX, LX, LH, S = 560, 330, 170, 60            # truc chinh, thau kinh, nua cao kinh, px/cm
FCM, DCM = 5.0, 300.0
DPCM = DCM * FCM / (DCM - FCM)               # 5,0847 cm : anh ro nhat
X0 = LX - DCM * S                            # vi tri that cua den (ngoai khung)
LAMP_X = 110
ROWS = [5.2, 5.0, 5.3, 5.1, 5.0]             # so_lieu_mau
G2 = 2; F2 = 25 / G2                         # ca chot
DRED = (185, 28, 28); DGREEN = (21, 110, 55); LBLUE = (147, 197, 253); GLOW = (253, 224, 71); DINK = (60, 66, 90)
FS, FM = 58, 56                              # co chu than canh (ve) -> 51 / 49 px trong mp4


def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l9-kinhlup-01.json")))
    assert [h[1] for h in k["so_lieu_mau"]["hang"]] == ROWS
    assert k["tham_so"][0]["gia_tri"] == FCM and k["tham_so"][1]["mac_dinh"] == DCM
    assert abs(DPCM - 5.08) < 0.01
    assert F2 == 12.5 and "2x" in k["so_lieu_mau"]["ghi_chu"] and "12,5" in k["so_lieu_mau"]["ghi_chu"]
    assert abs(DCM * F2 / (DCM - F2) - 13.0) < 0.05
_kiem_so()


def xp_of(cm): return LX + cm * S


def vn(x): return f"{x:.1f}".replace(".", ",")


def chev(d, p, q, col, s=16, w=4):
    x, y = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2; ang = math.atan2(q[1] - p[1], q[0] - p[0])
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=col, width=w)


def bulb(d, cx, cy, s, inv=False, alpha=1.0, glow=True):
    """bong den: bau tron o tren, de vit o duoi (inv = lat nguoc)"""
    sg = -1 if inv else 1
    gy = cy - sg * 0.18 * s; r = 0.42 * s
    if glow: d.ellipse([cx - r * 1.5, gy - r * 1.5, cx + r * 1.5, gy + r * 1.5], fill=A(GLOW, 0.35 * alpha))
    d.ellipse([cx - r, gy - r, cx + r, gy + r], fill=A((254, 240, 138), alpha), outline=A((161, 98, 7), alpha), width=max(2, int(s / 30)))
    by0, by1 = cy + sg * 0.2 * s, cy + sg * 0.5 * s
    d.rectangle([cx - 0.17 * s, min(by0, by1), cx + 0.17 * s, max(by0, by1)], fill=A(GRAY, alpha))
    for j in range(3):
        yy = by0 + sg * (0.07 + 0.09 * j) * s
        d.line([(cx - 0.17 * s, yy), (cx + 0.17 * s, yy)], fill=A(NAVY, 0.6 * alpha), width=max(2, int(s / 40)))


def lens(d, ax):
    pts = []
    for j in range(41):
        y = -LH + 2 * LH * j / 40; pts.append((LX + 3 + 15 * (1 - (y / LH) ** 2), ax + y))
    for j in range(41):
        y = LH - 2 * LH * j / 40; pts.append((LX - 3 - 15 * (1 - (y / LH) ** 2), ax + y))
    d.polygon(pts, fill=A(LBLUE, 0.75), outline=BLUE)


def bench(d, xp_cm, rays=1.0, ax=AX, fmark=False, ruler=True, lens_lab="kính lúp 5x", dpcm=DPCM, paper=True, grow=1.0):
    """den (sau dau ngat '3 m') - kinh - giay o xp_cm; chum tia tu den hoi tu tai dpcm"""
    xp = xp_of(xp_cm); xc = LX + dpcm * S
    d.line([(30, ax), (200, ax)], fill=A(NAVY, 0.6), width=3)
    d.line([(250, ax), (1060, ax)], fill=A(NAVY, 0.6), width=3)
    for x0 in (200, 226):                                                     # dau ngat truc
        d.line([(x0, ax + 22), (x0 + 24, ax - 22)], fill=NAVY, width=4)
    text(d, (245, ax - 105), "3 m", FM, NAVY)
    bulb(d, LAMP_X, ax, 130)
    text(d, (LAMP_X, ax + 125), "đèn", FM, INK)
    lens(d, ax)
    if lens_lab: text(d, (LX, ax + LH + 55), lens_lab, FM, BLUE)
    if rays > 0:
        c = A(ORANGE, 0.9 * rays)
        for yl in (-120, 0, 120):
            ys = yl * (250 - X0) / (LX - X0)
            d.line([(LAMP_X + 52, ax + 0.3 * yl), (198, ax + 0.85 * yl)], fill=c, width=4)   # doan tu den toi dau ngat
            d.line([(250, ax + ys), (LX, ax + yl)], fill=c, width=4)
            chev(d, (250, ax + ys), (LX, ax + yl), c)
            yp = yl * (1 - (xp - LX) / (xc - LX))
            d.line([(LX, ax + yl), (lerp(LX, xp, grow), ax + lerp(yl, yp, grow))], fill=c, width=6 if grow < 1 or ax != AX else 4)
        h = max(4, abs(120 * (1 - (xp - LX) / (xc - LX))))
        if paper and grow >= 1:
            d.ellipse([xp - 45, ax - 45, xp + 45, ax + 45], fill=A(GLOW, 0.8 * rays))
            d.rounded_rectangle([xp - 7, ax - h, xp + 7, ax + h], radius=6, fill=A(GLOW, 0.95 * rays))
    if fmark:
        dot(d, xp_of(FCM), ax, 10, NAVY)
        text(d, (xp_of(FCM) + 70, ax + 60), "F'", FS, NAVY)
    if paper:
        d.rounded_rectangle([xp - 8, ax - 210, xp + 8, ax + 210], radius=4, outline=NAVY, width=3, fill=A(WHITE, 0.0))
        text(d, (xp, ax - 250), "giấy", FM, NAVY)
    if ruler:
        ry = ax + 300
        d.rectangle([LX, ry, xp_of(10), ry + 34], fill=(254, 249, 195), outline=(161, 98, 7), width=2)
        for k in range(11):
            x = xp_of(k); d.line([(x, ry), (x, ry + (26 if k % 5 == 0 else 15))], fill=NAVY, width=3)
        for k in (0, 5, 10): text(d, (xp_of(k), ry + 75), str(k), FM, NAVY)
        text(d, (xp_of(10) + 100, ry + 75), "cm", FM, NAVY)
        if paper: d.line([(xp, ax + 210), (xp, ry)], fill=A(NAVY, 0.5), width=2)


def paper_face(img, d, box, dcm, ka=1.0, title="trên giấy"):
    """mat giay: anh bong den lat nguoc, nho; lech khoi cho ro nhat dcm (cm) -> nhoe thanh vet sang to"""
    x0, y0, x1, y1 = box
    card(d, box, fill=A(WHITE, ka), outline=A(LIGHT, ka), w=3)
    top = 10
    if title: text(d, ((x0 + x1) / 2, y0 + 48), title, FM, INK, alpha=ka); top = 90
    w, h = int(x1 - x0 - 20), int(y1 - y0 - top - 10)
    sub = Image.new("RGBA", (w, h), (255, 255, 255, 0)); sd = ImageDraw.Draw(sub, "RGBA")
    e = abs(dcm); R = min(18 + 60 * e, 0.45 * h)
    sd.ellipse([w / 2 - R, h / 2 - R, w / 2 + R, h / 2 + R], fill=(253, 224, 71, int(255 * clamp(0.9 - 0.18 * e, 0.3, 0.9))))
    kb = clamp(1 - e / 0.5)
    if kb > 0:
        bulb(sd, w / 2, h / 2, 84, inv=True, alpha=kb, glow=False)
    sub = sub.filter(ImageFilter.GaussianBlur(min(1 + 14 * e, 22)))
    if ka < 1:
        a = sub.split()[3].point(lambda v: int(v * ka)); sub.putalpha(a)
    img.paste(sub, (int(x0 + 10), int(y0 + top)), sub)


def table(d, n, y0):
    card(d, (60, y0, 1020, y0 + 240), fill=WHITE, outline=LIGHT, w=3)
    xs = [360 + 140 * j for j in range(5)]
    text(d, (190, y0 + 62), "Lần", FM, DINK)
    text(d, (190, y0 + 168), "cm", FM, DINK)
    d.line([(100, y0 + 112), (990, y0 + 112)], fill=LIGHT, width=3)
    for j in range(5):
        text(d, (xs[j], y0 + 62), str(j + 1), FM, DINK)
        if j < n: text(d, (xs[j], y0 + 168), vn(ROWS[j]), FS, INK)


# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    bench(d, 2.0, rays=0, ruler=False)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 930 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(FM)) + 56
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 96), fill=A(PURPLE, a), r=36)
    text(d, (W / 2, y0 + 59), "DỰ ĐOÁN", FM, WHITE, alpha=a)
    text(d, (W / 2, y0 + 165), "Dịch giấy ra xa kính dần.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 245), "Vệt sáng đổi thế nào?", 60, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1          # thanh dem nguoc lien, day 70 px
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 340, 970, y0 + 410], radius=35, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 340, 110 + max(70, 860 * (1 - p)), y0 + 410], radius=35, fill=A((76, 29, 149), a))


# ---------------- canh 2: Tien hanh ----------------
SWEEP = [(0.6, 3.6, 2.0, 9.0), (3.8, 5.0, 9.0, ROWS[0])]       # quet 2 -> 9 cm roi quay ve cho ro nhat
STOPS = [5.2]                                                   # luc dung o lan 1
for j in range(1, 5): STOPS.append(5.2 + 1.0 * j)              # lan 2..5: dich 0,5 s roi dung
MOVE = 0.5


def state_do(t):
    """(vi tri giay cm, so doc dang hien hoac None, so hang bang)"""
    if t < SWEEP[0][0]: return 2.0, None, 0
    for a, b, p0, p1 in SWEEP:
        if a <= t < b: return lerp(p0, p1, ease((t - a) / (b - a))), None, 0
    if t < SWEEP[1][1]: return 9.0, None, 0
    pos, rd, n = ROWS[0], None, 0
    for j, ts in enumerate(STOPS):
        if j > 0:
            ms = ts - MOVE
            if t < ms: break
            if t < ts: return lerp(ROWS[j - 1], ROWS[j], ease((t - ms) / MOVE)), None, n
        pos = ROWS[j]
        if t >= ts: rd, n = ROWS[j], j + 1
    return pos, rd, n


def s_do(img, d, t, sc):
    xp_cm, rd, n = state_do(t)
    bench(d, xp_cm)
    paper_face(img, d, (60, 1010, 520, 1290), xp_cm - DPCM)
    card(d, (560, 1010, 1020, 1290), fill=WHITE, outline=LIGHT, w=3)
    text(d, (790, 1058), "kính → giấy", FM, INK)
    if rd is not None: text(d, (790, 1185), vn(rd) + " cm", 66, INK)
    else: text(d, (790, 1185), "…", 66, DINK)
    if n > 0: table(d, n, 1325)


def _kiem_dong_bo():
    bad = []; t = 0.0
    while t < 10.0:
        pos, rd, n = state_do(t)
        if rd is not None and abs(pos - rd) > 1e-9: bad.append((round(t, 2), "so doc khi giay chua dung"))
        t += 0.05
    if state_do(9.5)[2] != 5: bad.append("chua du 5 hang")
    return bad


# ---------------- canh 3: Dap an + rut ra ----------------
DA_CMP, DA_RULE = 0.15, 5.4
def s_dapan(img, d, t, sc):
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN: nhỏ dần, rõ, rồi to"
    pw = tw(d, lab, F(FM)) + 60
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 342), fill=A(NAVY, ka), r=38)
    text(d, (W / 2, 302), lab, FM, WHITE, alpha=ka)
    k1 = appear(t, DA_CMP, 0.45)
    if k1 > 0:
        card(d, (60, 390, 1020, 800), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
        bulb(d, 280, 560, 190, alpha=k1)
        text(d, (280, 740), "đèn", FM, INK, alpha=k1)
        foc = lerp(1.2, ROWS[4] - DPCM, appear(t, 0.6, 2.0))     # giay dich toi cho ro: vet to -> anh net
        paper_face(img, d, (580, 410, 980, 690), foc, ka=k1, title="")
        text(d, (780, 740), "ảnh", FM, INK, alpha=k1)
        ko = appear(t, DA_CMP + 2.6, 0.8)          # mui ten chieu: den dung len, anh lat xuong
        if ko > 0:
            arrow(d, (125, 660), (125, 660 - 220 * ko), A(BLUE, ko), w=18, head=40)
            arrow(d, (935, 460), (935, 460 + 220 * ko), A(DRED, ko), w=18, head=40)
    k2 = appear(t, DA_RULE, 0.45)
    if k2 > 0:
        bench(d, ROWS[4], rays=k2, ax=1085, fmark=True, ruler=False, lens_lab=None,
              grow=appear(t, DA_RULE + 0.2, 2.2))
        card(d, (60, 1350, 1020, 1570), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=26, w=4)
        text(d, (W / 2, 1410), "Đèn ở xa → ảnh rõ gần F'", FS, DGREEN, alpha=k2)
        text(d, (W / 2, 1505), "kính → giấy ≈ f", FS, DGREEN, alpha=k2)


# ---------------- canh 4: Bay roi Chua noi duoc ----------------
BAY_R, BAY_E = 3.4, 6.6
def s_bay(img, d, t, sc):
    a1 = appear(t, 0.3, 0.45)
    pw = tw(d, "BẪY", F(FM)) + 60
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 338), fill=A(DRED, a1), r=38)
    text(d, (W / 2, 300), "BẪY", FM, WHITE, alpha=a1)
    text(d, (W / 2, 405), "“Giấy ở chỗ vệt sáng to nhất”", FS, INK, alpha=a1)
    # o trai: giay lech 3 cm khoi cho ro -> vet to, nhoe; vet "tho" nhe de hinh khong dung yen
    if a1 > 0:
        card(d, (50, 470, 530, 1300), fill=A(WHITE, a1), outline=A(DRED, a1), w=5)
        paper_face(img, d, (80, 500, 500, 1000), 8.0 - DPCM + 0.15 * math.sin(2.2 * t), ka=a1, title="")
        text(d, (290, 1080), "vệt to, nhoè", FS, DRED, alpha=a1)
        text(d, (290, 1190), "✗", 80, DRED, alpha=a1)
    a2 = appear(t, BAY_R, 0.45)
    if a2 > 0:
        card(d, (550, 470, 1030, 1300), fill=A(WHITE, a2), outline=A(DGREEN, a2), w=5)
        paper_face(img, d, (580, 500, 1000, 1000), ROWS[4] - DPCM, ka=a2, title="")
        text(d, (790, 1080), "ảnh nhỏ, rõ nét", FS, DGREEN, alpha=a2)
        text(d, (790, 1190), "✓", 80, DGREEN, alpha=a2)
    k3 = appear(t, BAY_E, 0.45)
    if k3 > 0:
        card(d, (50, 1345, 1030, 1560), fill=A(WHITE, k3), outline=A(NAVY, k3), w=5)
        text(d, (W / 2, 1405), "Chưa nói được:", FS, NAVY, alpha=k3)
        text(d, (W / 2, 1495), "số liệu minh hoạ", FM, INK, alpha=k3)


# ---------------- canh 5: Chot + THU NGHI (cau chot A-D o khung web) ----------------
END_Q, END_C = 0.2, 3.0
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 425), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 345), "Đèn ở xa: ảnh rõ gần tiêu điểm", FM, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 455, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(FM)) + 56
    card(d, (W / 2 - pw / 2, 480, W / 2 + pw / 2, 556), fill=A(ORANGE, k1), r=38)
    text(d, (W / 2, 518), "THỬ NGHĨ", FM, WHITE, alpha=k1)
    text(d, (W / 2, 625), "Kính lúp ghi 2x, đèn vẫn 3 m.", FS, INK, alpha=k1)
    text(d, (W / 2, 705), "Giấy cách kính bao nhiêu?", FS, INK, alpha=k1)
    if k1 > 0:   # hinh: den - kinh 2x - giay o cho chua biet (khong ve tia, khong ve thuoc)
        ax = 1110
        d.line([(30, ax), (200, ax)], fill=A(NAVY, 0.6 * k1), width=3)
        d.line([(250, ax), (1020, ax)], fill=A(NAVY, 0.6 * k1), width=3)
        for x0 in (200, 226): d.line([(x0, ax + 22), (x0 + 24, ax - 22)], fill=A(NAVY, k1), width=4)
        text(d, (245, ax - 105), "3 m", FM, NAVY, alpha=k1)
        bulb(d, LAMP_X, ax, 130, alpha=k1)
        lens(d, ax)
        text(d, (LX, ax + LH + 55), "kính 2x", FM, BLUE, alpha=k1)
        xp = 840 + 120 * math.sin(0.9 * t)     # giay dich qua lai: dang tim cho ro, khong dung o so nao
        d.rounded_rectangle([xp - 8, ax - 210, xp + 8, ax + 210], radius=4, outline=A(NAVY, k1), width=3)
        text(d, (xp, ax - 250), "giấy", FM, NAVY, alpha=k1)
        y = ax + 300
        arrow(d, (LX + 40, y), (xp - 6, y), A(ORANGE, k1), w=5, head=20)
        arrow(d, (xp - 40, y), (LX + 6, y), A(ORANGE, k1), w=5, head=20)
        text(d, ((LX + xp) / 2, y + 62), "? cm", FS, ORANGE, alpha=k1)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"), (do["t0"] + SWEEP[0][0], "tap")]
    cs += [(do["t0"] + ts, "tick") for ts in STOPS]
    cs += [(da["t0"] + 0.1, "ding"), (da["t0"] + DA_RULE, "tap"), (b["t0"] + 0.3, "buzz"), (e["t0"] + END_Q + 0.1, "open")]
    return cs


CLIP = dict(id="tn-l9-kinhlup-01", header="KHTN 9 · THÍ NGHIỆM", footer="Đo tiêu cự kính lúp · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Ảnh bóng đèn trên giấy", draw=s_hook, tail=0.3, caps=[
   ("Kính lúp 5x, đèn ở cuối lớp.", 3.0),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Dịch giấy từ sát kính ra xa.", 4.2),
   ("Dừng ở chỗ rõ nhất, đo 5 lần.", 5.5)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Ảnh ngược chiều, nhỏ hơn đèn.", 5.0),
   ("Ảnh thật: hứng được trên giấy.", 3.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.3, caps=[
   ("So hai chỗ đặt giấy.", BAY_E - 0.4),
   ("Còn bỏ ngỏ.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự tính.", 8.2)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
