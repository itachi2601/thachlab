# Clip: tn-l12-xoaychieu-02 - Hai LED mac song song nguoc chieu: moi LED sang may lan moi giay?
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-xoaychieu-02.json:
#   so_lieu_mau: f = 1 ; 5 ; 25 ; 50 Hz -> T = 1,0 ; 0,2 ; 0,04 ; 0,02 s -> doi chieu 2 ; 10 ; 50 ; 100 lan/s.
#   dung_cu: dien tro bao ve 330 ohm; quan_sat: 50 Hz trong nhu sang lien tuc; rut_ra: moi chu ki moi LED sang 1 lan.
#   sai_so_thuong_gap: dem trong 10 s roi chia 10 -> ca cau chot dem 10 s.
# Ban 2 (21/11/2026, viec 4 lo 20, cong --do-chu moi): danh quan niem sai "doi chieu 2f lan/s nen MOI LED chop 2f lan"
#   (hoac "ca cap chop f lan"). Dung: moi LED sang f lan/s, ca cap 2f lan/s.
#   Du doan (K10 khong ve nut; khung web hoi A-D): f = 5 Hz, trong 1 s LED do sang may lan? -> 5 lan
#     (A 2,5 = "ca cap f lan"; C 10 = "moi LED 2f"; D 20). Bai chi neu ca 1 Hz (moi LED 1 lan) va doi chieu 2f; Cau 2
#     hoi 100.pi -> doi chieu 100 lan/s: khong trung.
#   Bay: bang so do f | doi chieu/s (kho: 1 Hz -> 2, 25 Hz -> 50) canh cot "Moi LED/s" (1, 25): khong lap cap 5 Hz/5 lan.
#   Chot (khung web hoi A-D, dap so KHONG hien tren man): trong 10 s ca hai LED chop tong cong 50 lan -> moi giay 5 lan
#     = 2f -> f = 2,5 Hz (tham_so f: 0,5..60 Hz buoc 0,5; CA TU SUY theo mo hinh N = 2f, khong phai hang do trong kho). Nhieu: 1,25 Hz (moi LED 2f), 5 Hz (tong = f), 25 Hz (quen chia 10 s).
# Pha u = U0.sin(2.pi.f.t): trong 1 s du f buou duong (do) + f buou am (xanh), khong buou cat doi o hai mep.
# Toa do mp4 = 65 + 0,88.x; chu than canh ve >= 56 px (ra >= 49 px).
from engine import *

LGREEN = (22, 163, 74)
DGREEN = (21, 128, 61)
THR = 0.15                                   # nguong sang cua LED (ti le U0)

# ---------------- mach: may phat tin hieu - dien tro - hai LED nguoc chieu ----------------
def led(d, cx, cy, right, col, lit):
    """LED: tam giac chi chieu cho dong qua (right=True: trai -> phai) + vach; lit 0..1."""
    if lit > 0:
        for k in range(6, 0, -1):
            dot(d, cx, cy, 34 + k * 13, A(col, 0.09 * lit))
    s = 1 if right else -1
    tri = [(cx - s * 32, cy - 36), (cx - s * 32, cy + 36), (cx + s * 32, cy)]
    d.polygon(tri, fill=mix(WHITE, col, 0.2 + 0.8 * lit), outline=NAVY, width=4)
    d.line([(cx + s * 34, cy - 38), (cx + s * 34, cy + 38)], fill=NAVY, width=7)

AX, BX, Y1, Y2, YT, YB, LX = 700, 1000, 480, 620, 390, 750, 850
def circuit(d, f_lab, lr, lg):
    card(d, (40, 250, 1040, 800), fill=WHITE, outline=LIGHT, w=3)
    card(d, (70, 300, 420, 780), fill=(241, 245, 249), outline=NAVY, r=22, w=5)       # may phat tin hieu
    text(d, (245, 352), "Máy phát", 56, INK)
    d.rounded_rectangle([95, 405, 395, 505], radius=14, fill=NAVY)
    text(d, (245, 455), f_lab, 60, (134, 239, 172))
    pts = [(160 + j * 170 / 40, 640 - 40 * math.sin(2 * math.pi * j / 40)) for j in range(41)]
    d.line(pts, fill=ORANGE, width=7, joint="curve")
    W_ = dict(fill=NAVY, width=7)
    d.line([(420, YT), (470, YT)], **W_); d.line([(620, YT), (AX, YT), (AX, Y2)], **W_)
    d.rectangle([470, YT - 24, 620, YT + 24], fill=WHITE, outline=NAVY, width=5)         # dien tro
    text(d, (545, 322), "330 Ω", 56, INK)
    d.line([(AX, Y1), (BX, Y1)], **W_); d.line([(AX, Y2), (BX, Y2)], **W_)
    d.line([(BX, Y1), (BX, YB), (420, YB)], **W_)
    for x, y in ((AX, Y1), (AX, Y2), (BX, Y1), (BX, Y2)): dot(d, x, y, 11, NAVY)
    d.rectangle([LX - 42, Y1 - 44, LX + 42, Y1 + 44], fill=WHITE); d.rectangle([LX - 42, Y2 - 44, LX + 42, Y2 + 44], fill=WHITE)
    led(d, LX, Y1, True, RED, lr)
    led(d, LX, Y2, False, LGREEN, lg)
    text(d, (760, Y1 - 58), "đỏ", 58, RED)
    text(d, (770, Y2 + 62), "xanh", 58, DGREEN)

def led_lit(u):
    return clamp((u - THR) / (1 - THR)), clamp((-u - THR) / (1 - THR))

# ---------------- do thi u(t) trong 1 s (hoac 1 chu ki) ----------------
GX0, GX1 = 140, 960
def graph(d, y0, y1, f, kx, tlab="1 s", nums=None):
    """u = sin(2.pi.f.tau), tau 0..1 (kx: phan da ve); buou duong to do, buou am to xanh.
    nums = (k_do, k_xanh): so thu tu tren buou do (tren) / xanh (duoi), hien toi buou thu k."""
    yc, amp = (y0 + y1) / 2, (y1 - y0) / 2 - 20
    X = lambda tau: GX0 + (GX1 - GX0) * tau
    n = max(160, int(30 * f)); m = int(n * kx)
    for j in range(m):
        tau = j / n; u = math.sin(2 * math.pi * f * tau)
        if abs(u) > THR:
            d.line([(X(tau), yc), (X(tau), yc - amp * u)], fill=A(RED if u > 0 else LGREEN, 0.3), width=max(2, int((GX1 - GX0) / n) + 1))
    d.line([(GX0, yc), (GX1 + 26, yc)], fill=NAVY, width=5)
    d.line([(GX0, y1), (GX0, y0)], fill=NAVY, width=5)
    text(d, (GX0 - 42, y0 + 26), "u", 58, INK)
    d.line([(X(1), yc - 14), (X(1), yc + 14)], fill=NAVY, width=5)
    text(d, (GX1 + 8, yc - 12), tlab, 56, INK, anchor="lb")     # tren truc, ben phai moc 1 s: khong de buou
    if m > 1:
        pts = [(X(j / n), yc - amp * math.sin(2 * math.pi * f * j / n)) for j in range(m + 1)]
        d.line(pts, fill=ORANGE, width=6 if f < 20 else 3, joint="curve")
    if nums:
        for i in range(int(f)):
            if i < nums[0]: text(d, (X((i + 0.25) / f), yc - amp - 6), str(i + 1), 56, RED, anchor="mb")
            if i < nums[1]: text(d, (X((i + 0.75) / f), yc + amp + 6), str(i + 1), 56, DGREEN, anchor="mt")
    return X, yc

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    circuit(d, "5 Hz", 0, 0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 850 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 104), fill=A(PURPLE, a), r=40)
    text(d, (W / 2, y0 + 64), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    text(d, (W / 2, y0 + 200), "Trong 1 s, LED đỏ", 64, INK, alpha=a)        # K10: khong ve nut A-D
    text(d, (W / 2, y0 + 300), "sáng mấy lần?", 64, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1          # thanh dem lien (khong chia 5 phan: cong B v1, 5 cham goi "5 lan")
    p = clamp((t - tc) / (tend - tc))
    d.rounded_rectangle([110, y0 + 400, 970, y0 + 530], radius=24, fill=A(LIGHT, a))
    if p < 1: d.rounded_rectangle([110, y0 + 400, 110 + 860 * (1 - p), y0 + 530], radius=24, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
SLOW = 4.6                                   # 1 s that o 5 Hz chieu cham trong 4,6 s
def stages(sc):
    M = sc["M"]; a0 = M[0] + 0.3
    return a0, a0 + SLOW, M[1] - 0.1          # bat dau cham, het 1 s, chuyen 50 Hz

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    a0, a1, b0 = stages(sc)
    if t < b0:
        tau = clamp((t - a0) / SLOW)
        u = math.sin(2 * math.pi * 5 * tau) if a0 <= t < a1 else 0.0
        lr, lg = led_lit(u)
        circuit(d, "5 Hz", lr, lg)
        card(d, (40, 830, 1040, 1230), fill=WHITE, outline=LIGHT, w=3)
        graph(d, 880, 1180, 5, tau)
        # bo dem: buou do thu i bat dau tai tau = i/5, buou xanh tai (i + 0,5)/5
        n_r = min(5, int(tau * 5 + 1e-6) + (1 if t >= a0 else 0)) if tau < 1 else 5
        n_g = min(5, int(tau * 5 + 0.5 + 1e-6)) if tau < 1 else 5
        card(d, (40, 1260, 1040, 1440), fill=WHITE, outline=NAVY, w=4)
        text(d, (290, 1350), f"đỏ: {n_r}", 72, RED)
        text(d, (790, 1350), f"xanh: {n_g}", 72, DGREEN)
        return
    k = appear(t, b0, 0.4)
    circuit(d, "50 Hz", 0.7 * k, 0.7 * k)
    card(d, (40, 830, 1040, 1230), fill=WHITE, outline=LIGHT, w=3)
    graph(d, 880, 1180, 50, clamp((t - b0) / 1.8))
    ke = appear(t, b0 + 0.6, 0.4)
    if ke > 0:
        card(d, (40, 1260, 1040, 1440), fill=A(WHITE, ke), outline=A(NAVY, ke), w=4)
        text(d, (W / 2, 1350), "Mắt thấy: sáng đều", 68, INK, alpha=ke)

# ---------------- canh 3: Dap an + rut ra ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    b = appear(t, 0.3, 0.4)
    pw = tw(d, "ĐÁP ÁN: 5 lần", F(60)) + 70
    card(d, (W / 2 - pw / 2, 270, W / 2 + pw / 2, 350), fill=A(GREEN, b), r=40)
    text(d, (W / 2, 310), "ĐÁP ÁN: 5 lần", 60, WHITE, alpha=b)
    card(d, (40, 380, 1040, 880), fill=WHITE, outline=LIGHT, w=3)
    sw = clamp((t - 0.5) / 3.0)                                   # danh so lan luot tung buou
    graph(d, 470, 790, 5, 1.0, nums=(int(sw * 5 + 0.75), int(sw * 5 + 0.25)))
    r = appear(t, M[1] - 0.1, 0.45)
    if r > 0:
        card(d, (40, 920, 1040, 1300), fill=A((236, 253, 243), r), outline=A(GREEN, r), w=5)
        text(d, (W / 2, 1030), "Mỗi chu kì:", 64, INK, alpha=r)
        text(d, (W / 2, 1160), "mỗi LED sáng 1 lần", 64, DGREEN, alpha=r)
        # LED nho chop luan phien (giu hinh khong dung yen)
        ph = (t - M[1]) % 1.2 < 0.6
        for cx, col, on in ((180, RED, ph), (900, LGREEN, not ph)):
            dot(d, cx, 1400, 46, A(col, r * (1.0 if on else 0.18)), outline=A(NAVY, r))
        text(d, (180, 1500), "đỏ", 58, RED, alpha=r); text(d, (900, 1500), "xanh", 58, DGREEN, alpha=r)

# ---------------- canh 4: Bay (3 nhip, moi nhip mot phu de) ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    b1, b2, b3 = (m - 0.1 for m in sc["M"])
    k1, k2, k3 = appear(t, b1, 0.4), appear(t, b2, 0.4), appear(t, b3, 0.4)
    pw = tw(d, "BẪY", F(56)) + 60
    card(d, (W / 2 - pw / 2, 260, W / 2 + pw / 2, 336), fill=A(RED, k1), r=38)
    text(d, (W / 2, 298), "BẪY", 56, WHITE, alpha=k1)
    text(d, (W / 2, 420), "Đổi chiều 2f lần/s", 64, INK, alpha=k1)
    text(d, (W / 2, 515), "→ mỗi LED 2f lần/s?", 64, RED, alpha=k1)
    if k3 > 0:
        pw2 = tw(d, "SAI", F(56)) + 50
        card(d, (1030 - pw2, 260, 1030, 336), fill=A(RED, k3), r=38)
        text(d, (1030 - pw2 / 2, 298), "SAI", 56, WHITE, alpha=k3)
    # bang so do: khung + tieu de hien tu nhip 1 (cong B v1: bot nua man trong); so lieu nhip 2; cot moi LED nhip 3
    card(d, (40, 590, 1040, 1080), fill=A(WHITE, k1), outline=A(NAVY, k1), w=4)
    cols = (170, 480, 830)
    text(d, (cols[0], 670), "f (Hz)", 58, NAVY, alpha=k1)
    text(d, (cols[1], 650), "Đổi", 58, BLUE, alpha=k1); text(d, (cols[1], 712), "chiều/s", 58, BLUE, alpha=k1)
    text(d, (cols[2], 650), "Mỗi", 58, DGREEN, alpha=k1); text(d, (cols[2], 712), "LED/s", 58, DGREEN, alpha=k1)
    d.line([(70, 765), (1010, 765)], fill=A(NAVY, k1), width=4)
    if k2 <= 0: return
    for j, (f, n2, n1) in enumerate(((1, 2, 1), (25, 50, 25))):
        y = 860 + j * 130
        text(d, (cols[0], y), str(f), 66, INK, alpha=k2)
        text(d, (cols[1], y), str(n2), 66, BLUE, alpha=k2)
        if k3 > 0:
            d.rounded_rectangle([cols[2] - 110, y - 50, cols[2] + 110, y + 50], radius=16, fill=A((220, 252, 231), k3))
            text(d, (cols[2], y), str(n1), 66, DGREEN, alpha=k3)
        else:
            text(d, (cols[2], y), "?", 66, GRAY, alpha=k2)
    if k3 > 0:
        card(d, (40, 1120, 1040, 1300), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), w=5)
        text(d, (W / 2, 1210), "Hai LED thay phiên", 66, DGREEN, alpha=k3)

# ---------------- canh 5: Chua noi duoc gi ----------------
def s_gioi(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.2, 0.4); kb = appear(t, 2.4, 0.4)
    card(d, (40, 300, 1040, 1300), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    for j, s in enumerate(("• Tần số chính xác", "• Giá trị hiệu dụng")):
        text(d, (100, 600 + j * 260), s, 64, INK, anchor="lm", alpha=kb)
    text(d, (W / 2, 800), "?", 260, NAVY, alpha=k * (1 - kb))

# ---------------- canh 6: THU NGHI (cau_chot cua khung; dap so khong hien) ----------------
DARK_OR = (181, 71, 8)
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    k = appear(t, 0.3, 0.5)
    card(d, (40, 260, 1040, 1000), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 285, W / 2 + pw / 2, 365), fill=A(DARK_OR, k), r=40)
    text(d, (W / 2, 325), "THỬ NGHĨ", 56, WHITE, alpha=k)
    text(d, (W / 2, 450), "Trong 10 s, hai LED", 62, INK, alpha=k)
    text(d, (W / 2, 535), "chớp tổng cộng 50 lần.", 62, INK, alpha=k)
    text(d, (W / 2, 620), "f = ?", 66, DARK_OR, alpha=k)
    # thanh 10 s day dan, 50 vach (giu hinh khong dung yen)
    x0, x1, yb0, yb1 = 110, 970, 730, 840
    d.rounded_rectangle([x0, yb0, x1, yb1], radius=14, fill=A(LIGHT, k))
    p = clamp((t - 0.8) / 5.6)
    if p > 0:
        d.rounded_rectangle([x0, yb0, x0 + (x1 - x0) * p, yb1], radius=14, fill=A(ORANGE, k))
        for i in range(int(50 * p)):
            x = x0 + (x1 - x0) * (i + 0.5) / 50
            d.line([(x, yb0 + 18), (x, yb1 - 18)], fill=WHITE, width=4)
    text(d, (x0, 905), "0", 58, INK, alpha=k)
    text(d, (x1, 905), "10 s", 58, INK, alpha=k)
    kh = appear(t, 3.3, 0.5)
    if kh > 0:
        card(d, (90, 1050, 990, 1290), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1120), "Gợi ý: một chu kì", 58, DARK_OR, alpha=kh)
        text(d, (W / 2, 1210), "có mấy lần chớp?", 58, DARK_OR, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, b, g, e = (sc[k] for k in ("hook", "do", "ans", "bay", "gioi", "end"))
    a0, a1, b0 = stages(do)
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + a0, "tap"), (do["t0"] + b0, "tap"),
            (an["t0"] + 0.3, "ding"),
            (b["t0"] + b["M"][0] - 0.1, "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"),
            (g["t0"] + 2.4, "tap"), (e["t0"] + 0.3, "open")]

CLIP = dict(id="tn-l12-xoaychieu-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Dòng điện xoay chiều · thachlab.id.vn", scenes=[
 dict(key="hook", title="Hai LED ngược chiều", draw=s_hook, tail=0.3, caps=[
   "Máy phát đặt 5 Hz.",
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Chiếu chậm đúng 1 s.", 5.4),
   ("Tăng lên 50 Hz.", 3.2)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.4, caps=[
   ("Đỏ: u dương. Xanh: u âm.", 3.4),
   ("1 s có 5 chu kì.", 3.4)]),
 dict(key="bay", title="Bẫy", draw=s_bay, tail=0.3, caps=[
   ("Đúng hay sai?", 3.1),
   ("Đọc bảng số đo.", 3.1),
   ("Mỗi LED chỉ một nửa.", 3.4)]),
 dict(key="gioi", title="Chưa nói được gì?", draw=s_gioi, tail=0.3, caps=[
   ("Còn chưa đo được gì?", 4.6)]),
 dict(key="end", title="Tự kiểm tra", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự tính.", 6.8)]),
])
