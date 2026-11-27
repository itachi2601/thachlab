# Clip: tn-l11-daodongdieuhoa-03 - Bong cua van xe dap: hinh chieu cua chuyen dong tron deu (vi_du, minh hoa)
#       (9/11/2026, L11 Ch.1)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-daodongdieuhoa-03.json (loai vi_du: hoat canh tinh tu mo hinh,
#   ghi_chu "khong phai so do that" -> tren man ghi "minh hoạ"):
#   tham_so: A = R = 10 cm, omega = 2 rad/s, phi = 0 ; mo_hinh x = A.cos(omega.t + phi) ; gia_thiet: M quay deu,
#   den chieu song song len duong kinh nam ngang.
#   so_lieu_mau (t s, x cm): 0 10 ; 1 -4,16 ; 2 -6,54 ; 3 9,60. Cham vet (cach deu thoi gian) KHONG ghi so.
#   hien_tuong_hay_sai[0] (bong chuyen dong deu) -> Du doan ; [1] (nham omega voi so vong/giay) -> Bay:
#     sau 3 s, x = 9,60 cm < 10 cm -> van CHUA quay het mot vong (khong neu so vong/giay, khong co trong kho).
#   Dung lai 27/11/2026 theo cong moi (--do-chu 0 LOI, chu >= 55 px, Du doan K10 + thanh dem, cau chot A-D ra khung web).
#   Bay: khong hien "2.pi ~ 6,28" (tranh lo dap so cau chot); ly le = sau 3 s van chua ve cho cu.
#   Cau chot (THU NGHI): banh R = 6 cm quay deu 1 vong moi giay -> bong: A = ?, omega = ? -> 6 cm; 2.pi rad/s
#     (buoc chua chieu: 1 vong = 2.pi rad). Khong dung cau "1 vong het 2 s, bien nay sang bien kia" cua bai (dong 201).
# Bo cuc: banh xe dung, anh den song song tu tren xuong, man nam ngang ben duoi (bong Q), thuoc -10..+10 cm.
# Canh: Du doan (K10: chi cau hoi + hinh, man che "?") -> Tien hanh -> Dap an + Rut ra -> Bay roi Chua noi duoc
#       -> Chot + cau hoi tu nho lai (goi y tre 2,5 s).
from engine import *

AMP, OMG = 10.0, 2.0
ROWS = [(0, "10"), (1, "−4,16"), (2, "−6,54"), (3, "9,60")]      # so_lieu_mau
DGREEN = (21, 110, 55); DRED = (185, 28, 28); TIRE = (55, 60, 75); LAMP = (250, 204, 21)
DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)

_TI = {}
def TI(size):                                   # Times Bold Italic cho omega
    size = int(size)
    if size not in _TI: _TI[size] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", size)
    return _TI[size]

def eq(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """Chuoi co 'ω' ve bang Times Bold Italic."""
    fs = [(p, TI(size * 1.12) if p == "ω" else F(size)) for p in re.split(r"(ω)", s) if p]
    tot = sum(tw(d, p, f) for p, f in fs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for p, f in fs:
        dtext(d, (x, cy), p, f, color, alpha, "lm"); x += tw(d, p, f)
    return tot

# ---------------- banh xe + man (khung nguon 1080x1920; vung thay y 200..1690) ----------------
CX, CY, PXC = 540, 590, 22          # tam banh; 22 px/cm -> R = 10 cm = 220 px
R = AMP * PXC
SY = 930                             # mat man hung bong
def mpos(th, cx=CX, cy=CY, r=R): return cx + r * math.cos(th), cy - r * math.sin(th)   # quay nguoc chieu kim dong ho
def qx(xcm, cx=CX, pxc=PXC): return cx + xcm * pxc

def light(d, a=1.0):
    for xx in range(250, 840, 60):
        y = 300
        while y < SY - 10:
            d.line([(xx, y), (xx, min(SY - 10, y + 22))], fill=A((240, 200, 60), 0.55 * a), width=3); y += 40
    card(d, (40, 215, 290, 295), fill=A(LAMP, a), r=20)
    text(d, (165, 255), "đèn ↓", 56, INK, alpha=a)

def wheel(d, th, a=1.0, cx=CX, cy=CY, r=R, sc=1.0, lab=True):
    c = lambda col: A(col, a)
    d.ellipse([cx - r - 30 * sc, cy - r - 30 * sc, cx + r + 30 * sc, cy + r + 30 * sc], outline=c(TIRE), width=int(22 * sc))
    for k in range(8):
        ang = th + k * math.pi / 4
        d.line([(cx, cy), (cx + (r + 18 * sc) * math.cos(ang), cy - (r + 18 * sc) * math.sin(ang))], fill=c(GRAY), width=max(2, int(3 * sc)))
    dot(d, cx, cy, 14 * sc, c(NAVY))
    mx, my = mpos(th, cx, cy, r)
    dot(d, mx, my, 18 * sc, c(ORANGE), outline=c(WHITE))
    if lab and sc >= 1:
        text(d, mpos(th, cx, cy, r - 62), "M", 56, DORANGE, alpha=a)
    return mx, my

def screen(d, a=1.0, ruler=True, labels=True, man=True):
    c = lambda col: A(col, a)
    d.rectangle([200, SY, 880, SY + 30], fill=c((215, 210, 200)), outline=c(NAVY), width=3)
    if man: text(d, (960, SY + 15), "màn", 56, INK, alpha=a)
    if ruler:
        for k in range(-10, 11, 2):
            L = 22 if k % 10 == 0 else 12
            d.line([(qx(k), SY + 30), (qx(k), SY + 30 + L)], fill=c(NAVY), width=3)
        if labels:
            for k, s in ((-10, "−10"), (0, "0"), (10, "+10")):
                text(d, (qx(k), SY + 90), s, 56, NAVY, alpha=a)
            text(d, (980, SY + 90), "x (cm)", 56, NAVY, alpha=a)

def shadow(d, xcm, mx, my, a=1.0):
    X = qx(xcm)
    y = my + 20
    while y < SY - 12:
        d.line([(X, y), (X, min(SY - 12, y + 14))], fill=A(NAVY, a), width=3); y += 24
    d.ellipse([X - 16, SY - 4, X + 16, SY + 26], fill=A(NAVY, a))

def pill(d, cx, cy, s, size, fg, bg, a=1.0):
    pw = tw(d, s, F(size)) + 52
    card(d, (cx - pw / 2, cy - size * 0.8, cx + pw / 2, cy + size * 0.8), fill=A(bg, a), r=int(size * 0.8))
    text(d, (cx, cy), s, size, fg, alpha=a)

def seg_bar(d, y, t, t0, t1, col, a=1.0, n=6):
    """Thanh dem lien khoi, tat lan luot tu PHAI sang TRAI; cao 76 px."""
    p = clamp((t - t0) / (t1 - t0)); on = n - int(p * n + 1e-9); wseg = 820 / n
    for i in range(n):
        x = 130 + i * wseg
        if i < on: card(d, (x, y, x + wseg - 14, y + 76), fill=A(col, a), r=16)
        else: card(d, (x, y, x + wseg - 14, y + 76), fill=A(WHITE, a), outline=A(EMPTY, a), r=16, w=4)

def tag_minh_hoa(d, a=1.0):
    pill(d, 880, 255, "minh hoạ", 56, WHITE, NAVY, a)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh; man chua co bong) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    light(d)
    wheel(d, OMG * max(0.0, t - 0.4))                       # van quay deu that, omega = 2 rad/s
    screen(d, ruler=False)
    if t > 1.0: text(d, (CX, SY - 60), "?", 72, PURPLE)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1100 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 66, "DỰ ĐOÁN", 56, WHITE, PURPLE, a)
    for j, l in enumerate(("Van quay đều, đèn chiếu", "song song. Bóng trên màn", "chạy nhanh, chậm thế nào?")):
        text(d, (W / 2, y0 + 170 + j * 80), l, 58, PURPLE if j == 2 else INK, alpha=a)
    seg_bar(d, y0 + 400, t, M[1] + 0.4, sc["T"] - 0.2, PURPLE, a)

# ---------------- canh 2: Tien hanh (thoi gian that, dung o t = 1; 2; 3 s) ----------------
REL, HOLD = 0.6, 1.1
DT, TRAIL = 0.1, 1.5                # cham vet cach deu thoi gian, chi luot dau, khong ghi so
def tau_do(v):
    """-> (thoi gian that, so cot bang da co)"""
    if v < REL: return 0.0, 1
    u = v - REL; tau = 0.0
    for i in range(1, 4):
        if u < 1.0: return tau + u, i
        u -= 1.0; tau = float(i)
        if i < 3 and u < HOLD: return tau, i + 1
        if i < 3: u -= HOLD
    return 3.0, 4

def trails(d, tau, a=1.0):
    n = int(min(tau, TRAIL) / DT + 1e-6)
    for k in range(n + 1):
        th = OMG * k * DT
        mx, my = mpos(th)
        dot(d, mx, my, 8, A((251, 146, 60), a))
        dot(d, qx(AMP * math.cos(th)), SY - 26, 10, A(TEAL, a))

def table(d, cols, y0=1100):
    card(d, (40, y0, 1040, y0 + 200), fill=WHITE, outline=NAVY, r=20, w=3)
    d.line([(40, y0 + 100), (1040, y0 + 100)], fill=LIGHT, width=3)
    d.line([(250, y0 + 10), (250, y0 + 190)], fill=LIGHT, width=3)
    text(d, (145, y0 + 50), "t (s)", 56, INK); text(d, (145, y0 + 150), "x (cm)", 56, INK)
    for i, (tt, xs) in enumerate(ROWS):
        cx = 250 + 98 + i * 197
        text(d, (cx, y0 + 50), str(tt), 56, INK)
        if i < cols: text(d, (cx, y0 + 150), xs, 56, DORANGE)

def s_do(img, d, t, sc):
    tau, cols = tau_do(t)
    light(d); screen(d); tag_minh_hoa(d)
    trails(d, tau)
    mx, my = wheel(d, OMG * tau)
    xs = AMP * math.cos(OMG * tau)
    shadow(d, xs, mx, my)
    text(d, (qx(xs) + 24, SY - 70), "Q", 56, NAVY, anchor="lm")
    table(d, cols)
    card(d, (330, 1345, 750, 1445), fill=(70, 78, 100), r=22)
    text(d, (540, 1395), f"t = {tau:.1f} s".replace(".", ","), 56, WHITE)
    text(d, (W / 2, 1530), "t = 0: M ở bên phải", 56, INK)

# ---------------- canh 3: Dap an + Rut ra (banh van quay, bong van chay: khong dung hinh) ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    light(d, 0.6); screen(d, labels=False, man=False)
    trails(d, TRAIL)
    th = OMG * t
    mx, my = wheel(d, th, a=0.7, lab=False)
    shadow(d, AMP * math.cos(th), mx, my, a=0.7)
    for X in (qx(-8.5), qx(8.5)): text(d, (X, SY - 75), "dày", 56, TEAL)
    text(d, (CX, SY - 75), "thưa", 56, TEAL)
    pill(d, W / 2, 1110, "Nhanh ở giữa, chậm ở hai đầu", 56, WHITE, NAVY)
    k1 = appear(t, M[1] - 0.05, 0.45)
    if k1 > 0:
        card(d, (60, 1200, 1020, 1470), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), r=24, w=4)
        text(d, (W / 2, 1270), "A = bán kính = 10 cm", 58, INK, alpha=k1)
        eq(d, W / 2, 1390, "ω = tốc độ góc = 2 rad/s", 58, INK, alpha=k1)

# ---------------- canh 4: Bay (3 nhip cach nhau >= 3 s) roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    light(d, 0.6); screen(d, labels=False, man=False)
    th3 = OMG * 3
    t2, t3 = M[1] - 0.1, M[2] - 0.1
    kc = appear(t, t2, 0.4)
    if kc > 0:                                              # phat lai 3 s quay that (lap), cung da quay + moc t = 3 s
        u = (t - t2) % 3.6
        th = OMG * min(u, 3.0)
        rr = R + 70
        d.arc([CX - rr, CY - rr, CX + rr, CY + rr], start=-math.degrees(th), end=0, fill=A(ORANGE, kc), width=8)
        gx, gy = mpos(th3)
        d.ellipse([gx - 26, gy - 26, gx + 26, gy + 26], outline=A(DGREEN, kc), width=5)
        mx, my = wheel(d, th, lab=False)
        shadow(d, AMP * math.cos(th), mx, my)
        text(d, (W / 2, SY + 95), "t = 3 s: chưa về chỗ cũ", 58, DGREEN, alpha=kc)
    else:
        mx, my = wheel(d, 0.0, lab=False)
        shadow(d, AMP, mx, my)
    y0 = 1100
    a1 = 1 - appear(t, t3, 0.25)
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 400), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, W / 2, y0 + 66, "BẪY", 56, WHITE, DRED, a1)
        q = "✗ “2 rad/s là 2 vòng/giây”"
        yy = y0 + 180; lw = tw(d, q, F(58))
        text(d, (W / 2, yy), q, 58, DRED, alpha=a1)
        ks = clamp((t - 1.4) / 0.4)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A((140, 15, 15), a1), width=5)
        if kc > 0: text(d, (W / 2, y0 + 300), "✓ 2 rad/s: mỗi giây quay 2 rad", 58, DGREEN, alpha=a1 * kc)
    k3 = appear(t, t3, 0.4)
    if k3 > 0:
        card(d, (40, y0, 1040, y0 + 400), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y0 + 75), "Chưa nói được", 58, NAVY, alpha=k3)
        text(d, (100, y0 + 200), "• Giả thiết: quay đều", 56, INK, anchor="lm", alpha=k3)
        text(d, (100, y0 + 310), "• Đèn chiếu song song", 56, INK, anchor="lm", alpha=k3)

# ---------------- canh 5: THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    if t < 0.15: return
    card(d, (40, 215, 1040, 1585), fill=WHITE, outline=ORANGE, w=6)
    pill(d, W / 2, 285, "THỬ NGHĨ", 56, WHITE, ORANGE)
    cx, cy, r = 300, 560, 130                                # hinh nho: banh R = 6 cm quay, khong ve bong
    th = 2 * math.pi * 0.5 * t                               # quay cham cho thay chuyen dong (khong phai toc do that)
    wheel(d, th, cx=cx, cy=cy, r=r, sc=0.55, lab=False)
    d.line([(cx, cy), mpos(th, cx, cy, r)], fill=DORANGE, width=5)
    text(d, (500, 560), "R = 6 cm", 64, DORANGE, anchor="lm")
    text(d, (W / 2, 830), "Bánh quay đều", 60, INK)
    text(d, (W / 2, 915), "1 vòng mỗi giây.", 60, INK)
    text(d, (W / 2, 1040), "Bóng của van:", 64, DORANGE)
    eq(d, W / 2, 1125, "A = ?   ω = ?", 64, DORANGE)
    seg_bar(d, 1270, t, 0.8, sc["T"] - 0.2, ORANGE)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"), (do["t0"] + REL, "tap")]
    out += [(do["t0"] + REL + i * 1.0 + (i - 1) * HOLD, "tick") for i in (1, 2, 3)]
    out += [(da["t0"] + 0.3, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-daodongdieuhoa-03", header="VẬT LÍ 11 · VÍ DỤ", footer="Dao động điều hoà · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bóng của van xe đạp", draw=s_hook, tail=0.3, caps=[
   ("Bóng van in lên màn.", 3.6),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Chấm cách đều thời gian.", 4.0),
   ("Dừng mỗi giây, đọc li độ.", 4.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Gần hai đầu, chấm dày.", 4.4),
   ("Bóng dao động điều hoà.", 5.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Bẫy hay gặp.", 3.3),
   ("Xem van sau 3 s.", 3.3),
   ("Còn giới hạn.", 4.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự tính.", 7.0)]),
])
