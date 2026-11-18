# Clip: tn-l9-kinhlup-01 - Do tieu cu kinh lup ghi 5x bang anh bong den o xa (KHTN 9, lo 5, 18/11/2026)
# So lieu tu content/thi-nghiem/tn-l9-kinhlup-01.json:
#   tham_so: f = 5,0 cm ; D = 300 cm (den -> kinh) ; mo_hinh d' = D.f/(D - f) = 5,08 cm (vi tri anh ro nhat)
#   so_lieu_mau: 5 lan do kinh -> giay = 5,2 ; 5,0 ; 5,3 ; 5,1 ; 5,0 cm
# Cau hoi ngay sau hop trong bai: "Trung binh? G co khop 5x? Vi sao so do hoi lon hon 5 cm?" -> clip KHONG tinh trung
#   binh, KHONG tinh G, KHONG noi "den chua du xa". Bay dung hien_tuong_hay_sai[2] (giay o cho anh to nhat).
# Hinh: truc ngang dung ti le sau thau kinh (60 px/cm, F' = 300 px); den o 3 m ve sau dau ngat truc. Tia tu den
#   (diem tren truc, cach 300 cm) toi kinh roi hoi tu tai d' = 5,08 cm; vet sang tren giay = giao cua chum voi giay.
# THU NGHI: kinh ghi 2x, den van 3 m -> giay cach kinh khoang 12,5 cm (f = 25/2; mo hinh d' = 300.12,5/287,5 = 13,0 cm).
from engine import *
from PIL import ImageFilter

AX, LX, LH, S = 560, 330, 170, 60            # truc chinh, thau kinh, nua cao kinh, px/cm
FCM, DCM = 5.0, 300.0
DPCM = DCM * FCM / (DCM - FCM)               # 5,0847 cm : anh ro nhat
XC = LX + DPCM * S
X0 = LX - DCM * S                            # vi tri that cua den (ngoai khung)
LAMP_X = 110
ROWS = [5.2, 5.0, 5.3, 5.1, 5.0]             # so_lieu_mau
DRED = (185, 28, 28); DGREEN = (21, 110, 55); LBLUE = (147, 197, 253); GLOW = (253, 224, 71)


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


def lens(d):
    pts = []
    for j in range(41):
        y = -LH + 2 * LH * j / 40; pts.append((LX + 3 + 15 * (1 - (y / LH) ** 2), AX + y))
    for j in range(41):
        y = LH - 2 * LH * j / 40; pts.append((LX - 3 - 15 * (1 - (y / LH) ** 2), AX + y))
    d.polygon(pts, fill=A(LBLUE, 0.75), outline=BLUE)


def bench(d, xp_cm, rays=1.0, fmark=False, ruler=True, lamp_lab=True, giay_duoi=False):
    """den (sau dau ngat '3 m') - kinh lup - giay o xp_cm; chum tia tu den hoi tu tai d' = 5,08 cm"""
    xp = xp_of(xp_cm)
    d.line([(30, AX), (200, AX)], fill=A(NAVY, 0.6), width=3)
    d.line([(250, AX), (1060, AX)], fill=A(NAVY, 0.6), width=3)
    for x0 in (200, 226):                                                     # dau ngat truc
        d.line([(x0, AX + 22), (x0 + 24, AX - 22)], fill=NAVY, width=4)
    text(d, (225, AX - 60), "3 m", 44, NAVY)
    bulb(d, LAMP_X, AX, 130)
    if lamp_lab: text(d, (LAMP_X, AX + 110), "bóng đèn", 40, INK)
    lens(d)
    text(d, (LX, AX - LH - 40), "kính lúp 5x", 42, BLUE)
    if rays > 0:
        c = A(ORANGE, 0.9 * rays)
        for yl in (-120, 0, 120):
            ys = yl * (250 - X0) / (LX - X0)
            d.line([(LAMP_X + 52, AX + 0.3 * yl), (198, AX + 0.85 * yl)], fill=c, width=4)   # doan tu den toi dau ngat (bo qua doan 3 m)
            d.line([(250, AX + ys), (LX, AX + yl)], fill=c, width=4)
            chev(d, (250, AX + ys), (LX, AX + yl), c)
            yp = yl * (1 - (xp - LX) / (XC - LX))
            d.line([(LX, AX + yl), (xp, AX + yp)], fill=c, width=4)
        h = max(4, abs(120 * (1 - (xp - LX) / (XC - LX))))
        d.rounded_rectangle([xp - 7, AX - h, xp + 7, AX + h], radius=6, fill=A(GLOW, 0.95 * rays))
    if fmark:
        dot(d, xp_of(FCM), AX, 9, NAVY)
        text(d, (xp_of(FCM) + 34, AX - 36), "F'", 42, NAVY)
    d.rounded_rectangle([xp - 8, AX - 210, xp + 8, AX + 210], radius=4, outline=NAVY, width=3, fill=A(WHITE, 0.0))
    text(d, (xp, AX + 240) if giay_duoi else (xp, AX - 240), "giấy", 42, NAVY)
    if ruler:
        ry = AX + 250
        d.rectangle([LX, ry, xp_of(10), ry + 30], fill=(254, 249, 195), outline=(161, 98, 7), width=2)
        for k in range(11):
            x = xp_of(k); d.line([(x, ry), (x, ry + (24 if k % 5 == 0 else 14))], fill=NAVY, width=3)
        for k in (0, 5, 10): text(d, (xp_of(k), ry + 62), str(k), 40, NAVY)
        text(d, (xp_of(10) + 60, ry + 62), "cm", 40, NAVY, bold=False)
        d.line([(xp, AX + 210), (xp, ry)], fill=A(NAVY, 0.5), width=2)


def paper_face(img, d, box, dcm, ka=1.0, title="trên giấy"):
    """mat giay: anh bong den lat nguoc, nho; lech khoi cho ro nhat dcm (cm) -> nhoe thanh vet sang to"""
    x0, y0, x1, y1 = box
    card(d, box, fill=A(WHITE, ka), outline=A(LIGHT, ka), w=3)
    if title: text(d, ((x0 + x1) / 2, y0 + 40), title, 40, MUTED, bold=False, alpha=ka)
    w, h = int(x1 - x0 - 20), int(y1 - y0 - 80)
    sub = Image.new("RGBA", (w, h), (255, 255, 255, 0)); sd = ImageDraw.Draw(sub, "RGBA")
    e = abs(dcm); R = min(18 + 60 * e, 0.45 * h)
    sd.ellipse([w / 2 - R, h / 2 - R, w / 2 + R, h / 2 + R], fill=(253, 224, 71, int(255 * clamp(0.9 - 0.18 * e, 0.3, 0.9))))
    kb = clamp(1 - e / 0.5)
    if kb > 0:
        bulb(sd, w / 2, h / 2, 84, inv=True, alpha=kb, glow=False)
    sub = sub.filter(ImageFilter.GaussianBlur(min(1 + 14 * e, 22)))
    if ka < 1:
        a = sub.split()[3].point(lambda v: int(v * ka)); sub.putalpha(a)
    img.paste(sub, (int(x0 + 10), int(y0 + 70)), sub)


def table(d, n, y0, ka=1.0):
    card(d, (60, y0, 1020, y0 + 230), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=3)
    xs = [330 + 140 * j for j in range(5)]
    text(d, (190, y0 + 60), "Lần", 42, MUTED, bold=False, alpha=ka)
    text(d, (190, y0 + 150), "cm", 42, MUTED, bold=False, alpha=ka)
    d.line([(100, y0 + 105), (990, y0 + 105)], fill=A(LIGHT, ka), width=3)
    for j in range(5):
        text(d, (xs[j], y0 + 60), str(j + 1), 42, MUTED, alpha=ka)
        if j < n: text(d, (xs[j], y0 + 150), vn(ROWS[j]), 46, INK, alpha=ka)
    text(d, (1010, y0 + 270), "số liệu minh hoạ", 40, MUTED, bold=False, anchor="rm", alpha=ka)


# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    bench(d, 8.0, rays=0, ruler=False)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 900 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 530), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(42)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 59), "DỰ ĐOÁN", 42, WHITE, alpha=a)
    ctext(d, y0 + 245, "Hứng ảnh bóng đèn cách 3 m\nlên tờ giấy sau kính.\nẢnh trên giấy thế nào?", 50, INK,
          maxw=920, alpha=a)
    text(d, (W / 2, y0 + 410), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 478, 940, y0 + 490], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 478, 140 + 800 * (1 - p), y0 + 490], radius=6, fill=A(PURPLE, a))


# ---------------- canh 2: Tien hanh ----------------
SWEEP = [(0.6, 3.4, 2.0, 9.0), (3.6, 5.2, 9.0, ROWS[0])]       # lan 1: quet qua cho ro roi quay ve
STOPS = [5.4]                                                  # luc dung o lan 1
for j in range(1, 5): STOPS.append(5.4 + 1.1 * j)              # lan 2..5: dich 0,55 s roi dung
MOVE = 0.55


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
    paper_face(img, d, (60, 920, 520, 1180), xp_cm - DPCM, title="trên giấy (phóng to)")
    card(d, (560, 920, 1020, 1180), fill=WHITE, outline=LIGHT, w=3)
    text(d, (790, 960), "kính → giấy", 40, MUTED, bold=False)
    text(d, (790, 1070), (vn(rd) + " cm") if rd is not None else "…", 64, INK if rd is not None else GRAY)
    if n > 0: table(d, n, 1230)


# ---------------- canh 3: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · ngược chiều, nhỏ hơn đèn"
    pw = tw(d, lab, F(42)) + 56
    card(d, (W / 2 - pw / 2, 226, W / 2 + pw / 2, 292), fill=A(NAVY, ka), r=33)
    text(d, (W / 2, 259), lab, 42, WHITE, alpha=ka)
    bench(d, ROWS[4], fmark=t > M[1], ruler=False, lamp_lab=False, giay_duoi=True)
    k1 = appear(t, M[0] + 0.3, 0.4)
    if k1 > 0:
        card(d, (60, 860, 1020, 1200), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
        bulb(d, 250, 1030, 170, alpha=k1)
        text(d, (250, 1160), "bóng đèn", 42, INK, alpha=k1)
        paper_face(img, d, (560, 880, 980, 1130), ROWS[4] - DPCM, ka=k1, title="trên giấy")
        text(d, (770, 1160), "(vẽ phóng to)", 40, MUTED, bold=False, alpha=k1)
    k3 = appear(t, M[1] + 0.2, 0.4)
    if k3 > 0:
        card(d, (60, 1240, 1020, 1500), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), r=22, w=3)
        text(d, (W / 2, 1310), "Đèn ở xa → ảnh rõ ở gần F'", 46, DGREEN, alpha=k3)
        text(d, (W / 2, 1400), "kính → giấy ≈ tiêu cự f", 46, DGREEN, alpha=appear(t, M[1] + 1.2, 0.4))


# ---------------- canh 4: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    bench(d, 8.0 if t < 2.3 else ROWS[4], rays=0.6, ruler=False, lamp_lab=False)
    if a1 > 0:
        k3 = a1 * appear(t, 0.3, 0.5); k4 = a1 * appear(t, 2.3, 0.5)          # ✓ tre 2 s, con >= 3 s truoc the sau
        y0 = 860
        card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(42)) + 52
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 61), "BẪY", 42, WHITE, alpha=a1)
        if k3 > 0:
            paper_face(img, d, (80, y0 + 120, 520, y0 + 380), 8.0 - DPCM, ka=k3, title="")
            text(d, (300, y0 + 440), "Vệt sáng to, nhoè", 42, DRED, alpha=k3)
            text(d, (300, y0 + 505), "✗", 70, DRED, alpha=k3)
        if k4 > 0:
            paper_face(img, d, (560, y0 + 120, 1000, y0 + 380), ROWS[4] - DPCM, ka=k4, title="")
            text(d, (780, y0 + 440), "Ảnh nhỏ, rõ nhất", 42, DGREEN, alpha=k4)
            text(d, (780, y0 + 505), "✓", 70, DGREEN, alpha=k4)
    if k2 > 0:
        y0 = 900 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 330), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Số liệu minh hoạ", "• Ảnh khi vật gần kính hơn f")):
            kk = k2 * appear(t, M[1] + 0.1 + 0.3 * j, 0.4)
            text(d, (90, y0 + 170 + j * 95), l1, 44, INK, anchor="lm", alpha=kk)


# ---------------- canh 5: Chot + THU NGHI ----------------
def s_end(img, d, t, sc):
    """Chot (khong neu G = 25/f) -> THU NGHI: kinh 2x, den van 3 m -> giay cach kinh ? (khoang 12,5 cm); goi y tre 2,5 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 400, "Đèn ở xa: ảnh rõ nhất\nhiện gần tiêu điểm F'", 52, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.6, 0.5)
    if k1 <= 0: return
    kh = appear(t, M[0] + 0.9 + 2.5, 0.5)
    card(d, (40, 600, 1040, lerp(1060, 1340, kh)), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(42)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 696), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 663), "THỬ NGHĨ", 42, WHITE, alpha=k1)
    ctext(d, 870, "Kính lúp ghi 2x, đèn vẫn\ncách 3 m. Giấy cách kính\nbao nhiêu cm?",
          48, INK, maxw=940, alpha=appear(t, M[0] + 0.9, 0.5))
    if kh > 0:
        card(d, (110, 1040, 970, 1310), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1095, "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1205, "G = 25/f", 46, ORANGE, maxw=820, alpha=kh)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"), (do["t0"] + SWEEP[0][0], "tap")]
    cs += [(do["t0"] + ts, "tick") for ts in STOPS]
    cs += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.5, "buzz"), (e["t0"] + e["M"][0] + 0.6, "open")]
    return cs


CLIP = dict(id="tn-l9-kinhlup-01", header="KHTN 9 · THÍ NGHIỆM", footer="Đo tiêu cự kính lúp · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Ảnh bóng đèn trên giấy", draw=s_hook, tail=0.8, caps=[
   ("Kính lúp 5x, đèn ở cuối lớp.", 3.0),
   ("Tự đoán trước khi xem tiếp.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.7, caps=[
   ("Dịch giấy tới khi ảnh rõ nhất.", 5.0),
   ("Đo từ kính tới giấy, làm 5 lần.", 4.9)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.8, caps=[
   ("Ảnh thật: hứng được trên giấy.", 3.6),
   ("Đo khoảng này để tìm f.", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.8, caps=[
   ("Giấy đặt chỗ nào mới đúng?", 5.0),
   ("Chưa nói được điều gì?", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.3, caps=[
   ("Dừng video, tự trả lời.", 6.6)]),
])
