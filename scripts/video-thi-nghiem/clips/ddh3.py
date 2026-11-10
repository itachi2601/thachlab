# Clip: tn-l11-daodongdieuhoa-03 - Bong cua van xe dap: hinh chieu cua chuyen dong tron deu (vi_du, minh hoa)
#       (9/11/2026, L11 Ch.1)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-daodongdieuhoa-03.json (loai vi_du: hoat canh tinh tu mo hinh,
#   ghi_chu "khong phai so do that" -> tren man ghi "minh hoạ"):
#   tham_so: A = R = 10 cm, omega = 2 rad/s, phi = 0 ; mo_hinh x = A.cos(omega.t + phi) ; gia_thiet: M quay deu,
#   den chieu song song len duong kinh nam ngang.
#   so_lieu_mau (t s, x cm): 0 10 ; 1 -4,16 ; 2 -6,54 ; 3 9,60. Cham vet (cach deu thoi gian) KHONG ghi so.
#   hien_tuong_hay_sai[0] (bong chuyen dong deu) -> Du doan ; [1] (nham omega voi so vong/giay) -> Bay:
#     sau 3 s, x = 9,60 cm < 10 cm -> van CHUA quay het mot vong (khong neu so vong/giay, khong co trong kho).
#   Cau chot: R = 6 cm, omega = 4 rad/s (trong khoang tham_so, chua hien) -> bien do, tan so goc cua bong?
#     (6 cm, 4 rad/s; khong hien). Khong tra loi cau "Doan thu: Q o bien khi M o dau?" ngay sau hop trong bai.
# Bo cuc: banh xe dung, anh den song song tu tren xuong, man nam ngang ben duoi (bong Q), thuoc -10..+10 cm.
# Canh: Du doan (K10: chi cau hoi + hinh, man che "?") -> Tien hanh -> Dap an + Rut ra -> Bay roi Chua noi duoc
#       -> Chot + cau hoi tu nho lai (goi y tre 2,5 s).
from engine import *

AMP, OMG = 10.0, 2.0
ROWS = [(0, "10"), (1, "−4,16"), (2, "−6,54"), (3, "9,60")]      # so_lieu_mau
DGREEN = (21, 110, 55); DRED = (185, 28, 28); TIRE = (55, 60, 75); LAMP = (250, 204, 21)

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
CX, CY, PXC = 540, 560, 22          # tam banh; 22 px/cm -> R = 10 cm = 220 px
R = AMP * PXC
SY = 930                             # mat man hung bong
def mpos(th, cx=CX, cy=CY, r=R): return cx + r * math.cos(th), cy - r * math.sin(th)   # quay nguoc chieu kim dong ho
def qx(xcm, cx=CX, pxc=PXC): return cx + xcm * pxc

def light(d, a=1.0):
    for xx in range(250, 840, 60):
        y = 215
        while y < SY - 10:
            d.line([(xx, y), (xx, min(SY - 10, y + 22))], fill=A((240, 200, 60), 0.55 * a), width=3); y += 40
    card(d, (60, 215, 230, 275), fill=A(LAMP, a), r=20)
    text(d, (145, 245), "đèn ↓", 40, INK, alpha=a)

def wheel(d, th, a=1.0, cx=CX, cy=CY, r=R, sc=1.0):
    c = lambda col: A(col, a)
    d.ellipse([cx - r - 30 * sc, cy - r - 30 * sc, cx + r + 30 * sc, cy + r + 30 * sc], outline=c(TIRE), width=int(22 * sc))
    for k in range(8):                                 # 8 nan (12 nan lam mp4 nang ~2,5 MB)
        ang = th + k * math.pi / 4
        d.line([(cx, cy), (cx + (r + 18 * sc) * math.cos(ang), cy - (r + 18 * sc) * math.sin(ang))], fill=c(GRAY), width=max(2, int(3 * sc)))
    dot(d, cx, cy, 14 * sc, c(NAVY))
    mx, my = mpos(th, cx, cy, r)
    dot(d, mx, my, 16 * sc, c(ORANGE), outline=c(WHITE))
    if sc >= 1:                                       # nhan M phia trong vanh, canh cham cam
        text(d, mpos(th, cx, cy, r - 52), "M", 40, ORANGE, alpha=a)
    return mx, my

def screen(d, a=1.0, ruler=True, cover=False):
    c = lambda col: A(col, a)
    d.rectangle([200, SY, 880, SY + 30], fill=c((215, 210, 200)), outline=c(NAVY), width=3)
    text(d, (940, SY + 15), "màn", 40, MUTED, alpha=a)
    if ruler:
        for k in range(-10, 11, 2):
            L = 22 if k % 10 == 0 else 12
            d.line([(qx(k), SY + 30), (qx(k), SY + 30 + L)], fill=c(NAVY), width=3)
        for k, s in ((-10, "−10"), (0, "0"), (10, "+10")):
            text(d, (qx(k), SY + 84), s, 40, NAVY, alpha=a)
        text(d, (qx(10) + 130, SY + 84), "x (cm)", 40, NAVY, alpha=a)
    if cover:
        text(d, (CX, SY - 50), "?", 64, PURPLE, alpha=a)

def shadow(d, xcm, mx, my, a=1.0):
    X = qx(xcm)
    y = my + 20
    while y < SY - 12:
        d.line([(X, y), (X, min(SY - 12, y + 14))], fill=A(NAVY, a), width=3); y += 24
    d.ellipse([X - 16, SY - 4, X + 16, SY + 26], fill=A(NAVY, a))

def pill(d, cx, cy, s, size, fg, bg, a=1.0):
    pw = tw(d, s, F(size)) + 52
    card(d, (cx - pw / 2, cy - size * 0.85, cx + pw / 2, cy + size * 0.85), fill=A(bg, a), r=int(size * 0.85))
    text(d, (cx, cy), s, size, fg, alpha=a)

def tag_minh_hoa(d, a=1.0):
    pill(d, 900, 245, "minh hoạ", 38, WHITE, MUTED, a)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh; man chua co bong) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    light(d, appear(t, 0.8, 0.5))
    th = OMG * max(0.0, t - 0.4)                            # van quay deu that, omega = 2 rad/s
    wheel(d, th)
    screen(d, ruler=False, cover=t > 1.0)
    tag_minh_hoa(d)
    ko = appear(t, 1.4, 0.4)
    if ko > 0:
        eq(d, 1050, 320, "ω = 2 rad/s", 42, NAVY, anchor="r", alpha=ko)
        text(d, (1050, 380), "van M quay đều", 40, ORANGE, anchor="rm", alpha=ko)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1100 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 60, "DỰ ĐOÁN", 40, WHITE, PURPLE, a)
    ctext(d, y0 + 250, "Van quay đều. Bóng của van\ntrên màn chạy nhanh, chậm\nthế nào?", 50, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 420, 940, y0 + 432], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 420, 140 + 800 * (1 - p), y0 + 432], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (thoi gian that, dung o t = 1; 2; 3 s) ----------------
REL, HOLD = 0.6, 1.3
DT, TRAIL = 0.1, 1.5                # cham vet cach deu thoi gian, chi luot dau (phai -> trai), khong ghi so
def tau_do(v):
    """-> (thoi gian that, so cot bang da co, dang dung?)"""
    if v < REL: return 0.0, 1, True
    u = v - REL; tau = 0.0
    for i in range(1, 4):
        if u < 1.0: return tau + u, i, False
        u -= 1.0; tau = float(i)
        if i < 3 and u < HOLD: return tau, i + 1, True
        if i < 3: u -= HOLD
    return 3.0, 4, True

def trails(d, tau, a=1.0):
    n = int(min(tau, TRAIL) / DT + 1e-6)
    for k in range(n + 1):
        th = OMG * k * DT
        mx, my = mpos(th)
        dot(d, mx, my, 8, A((251, 146, 60), a))
        dot(d, qx(AMP * math.cos(th)), SY - 26, 9, A(TEAL, a))

def table(d, cols, y0=1080):
    card(d, (40, y0, 1040, y0 + 200), fill=WHITE, outline=NAVY, r=20, w=3)
    d.line([(40, y0 + 100), (1040, y0 + 100)], fill=LIGHT, width=3)
    d.line([(250, y0 + 10), (250, y0 + 190)], fill=LIGHT, width=3)
    text(d, (145, y0 + 50), "t (s)", 40, INK); text(d, (145, y0 + 150), "x (cm)", 40, INK)
    for i, (tt, xs) in enumerate(ROWS):
        cx = 250 + 98 + i * 197
        text(d, (cx, y0 + 50), str(tt), 42, INK)
        if i < cols: text(d, (cx, y0 + 150), xs, 42, ORANGE)

def s_do(img, d, t, sc):
    tau, cols, hold = tau_do(t)
    light(d); screen(d); tag_minh_hoa(d)
    trails(d, tau)
    mx, my = wheel(d, OMG * tau)
    shadow(d, AMP * math.cos(OMG * tau), mx, my)
    text(d, (qx(AMP * math.cos(OMG * tau)) + 22, SY - 70), "Q", 42, NAVY, anchor="lm")
    table(d, cols)
    card(d, (300, 1330, 780, 1430), fill=(70, 78, 100), r=22)
    text(d, (540, 1380), (f"t = {int(round(tau))} s" if hold else "▶ đang quay"), 44, WHITE)
    eq(d, W / 2, 1490, "φ = 0: lúc t = 0, M ở bên phải", 40, INK)

# ---------------- canh 3: Dap an + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    light(d, 0.6); screen(d); tag_minh_hoa(d)
    trails(d, TRAIL)
    wheel(d, OMG * TRAIL, a=0.5)
    ka = appear(t, 0.1, 0.5)
    pill(d, W / 2, 1090, "ĐÁP ÁN · nhanh ở giữa, chậm ở hai đầu", 40, WHITE, NAVY, ka)
    kd = appear(t, 0.8, 0.4)
    if kd > 0:
        for X in (qx(-9), qx(9)): text(d, (X, SY - 68), "dày", 40, TEAL, alpha=kd)
        text(d, (CX, SY - 68), "thưa", 40, TEAL, alpha=kd)
    k1 = appear(t, M[1] - 0.05, 0.45)
    if k1 > 0:
        card(d, (60, 1160, 1020, 1530), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), r=24, w=4)
        eq(d, W / 2, 1230, "x = A cos(ωt + φ)", 50, DGREEN, alpha=k1)
        k2 = appear(t, M[1] + 0.8, 0.45)
        text(d, (W / 2, 1335), "A = bán kính = 10 cm", 44, INK, alpha=k2)
        eq(d, W / 2, 1430, "ω = tốc độ góc = 2 rad/s", 44, INK, alpha=k2)

# ---------------- canh 4: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    light(d, 0.6); screen(d); tag_minh_hoa(d)
    th3 = OMG * 3
    kc = appear(t, 1.8, 0.4)                                 # cung da quay + x(3 s) hien CUNG luc chu ✓
    if kc > 0:
        rr = R + 70
        d.arc([CX - rr, CY - rr, CX + rr, CY + rr], start=-math.degrees(th3), end=0, fill=A(ORANGE, kc), width=8)
        arrow(d, (CX + 50, CY - rr), (CX - 50, CY - rr), A(ORANGE, kc), w=8, head=26)     # chieu quay: nguoc kim dong ho
        text(d, (CX - 70, CY - rr - 4), "chiều quay", 40, ORANGE, anchor="rm", alpha=kc)
    mx, my = wheel(d, th3)
    shadow(d, AMP * math.cos(th3), mx, my)
    if kc > 0:
        text(d, (qx(9.6) - 30, SY - 60), "t = 3 s: x = 9,60 cm", 40, NAVY, anchor="rm", alpha=kc)
    a1 = appear(t, 0.0, 0.3) * (1 - appear(t, M[1] - 0.3, 0.2))
    if a1 > 0:
        y0 = 1090
        card(d, (40, y0, 1040, y0 + 500), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, W / 2, y0 + 62, "BẪY", 40, WHITE, DRED, a1)
        q = "“ω = 2 rad/s là 2 vòng mỗi giây”"
        yy = y0 + 200; lw = eq(d, W / 2, yy, q, 46, DRED, alpha=a1)
        ks = clamp((t - 1.4) / 0.4)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A((140, 15, 15), a1), width=4)
        ctext(d, y0 + 320, "✓ Sau 3 s: chưa hết một vòng", 46, DGREEN, maxw=940, alpha=a1 * kc)
        eq(d, W / 2, y0 + 415, "ωt = 2·3 = 6 rad < 2π ≈ 6,28 rad", 42, INK, alpha=a1 * kc)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        y0 = 1090 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 450), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Bánh quay đều: giả thiết", "• Đèn chiếu song song")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (90, y0 + 190 + j * 120), l1, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def _end_body(sc):
    M = sc["M"]
    def body(d, t, k1):
        kq = appear(t, M[0] + 0.4, 0.5)
        cx, cy, r = 330, 1060, 6 * 14                       # hinh nho: banh R = 6 cm (14 px/cm), khong ve bong
        wheel(d, 0.7, a=kq, cx=cx, cy=cy, r=r, sc=0.5)
        d.line([(cx, cy), mpos(0.7, cx, cy, r)], fill=A(ORANGE, kq), width=4)
        text(d, (cx + r + 60, cy - 60), "R = 6 cm", 40, ORANGE, anchor="lm", alpha=kq)
        eq(d, cx + r + 60, cy + 10, "ω = 4 rad/s", 40, NAVY, anchor="l", alpha=kq)
        d.rectangle([cx - 140, 1210, cx + 140, 1230], fill=A((215, 210, 200), kq), outline=A(NAVY, kq), width=2)
        eq(d, cx + 200, 1220, "bóng: A = ?   ω = ?", 40, PURPLE, anchor="l", alpha=kq)
        kh = appear(t, M[0] + 0.4 + 2.5, 0.5)                # goi y tre 2,5 s sau cau hoi
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1360, "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1450, "Bóng = hình chiếu của van", 42, ORANGE, maxw=820, alpha=kh)
    return body

def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Hình chiếu của chuyển động\ntròn đều: dao động điều hoà",
             "Bánh R = 6 cm, quay 4 rad/s.\nBiên độ, tần số góc của bóng?", body=_end_body(sc))

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (do["t0"] + REL, "tap")]
    out += [(do["t0"] + REL + i * 1.0 + (i - 1) * HOLD, "tick") for i in (1, 2, 3)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-daodongdieuhoa-03", header="VẬT LÍ 11 · VÍ DỤ", footer="Dao động điều hoà · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bóng của van xe đạp", draw=s_hook, tail=0.6, caps=[
   ("Đèn chiếu song song, bóng in lên màn.", 3.8),
   ("Tự đoán trước khi xem tiếp.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Chấm cách đều nhau về thời gian.", 4.4),
   ("Dừng ở mỗi giây, đọc li độ bóng.", 4.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.8, caps=[
   ("Cùng thời gian, gần đầu đi ít hơn.", 4.2),
   ("Bóng dao động điều hoà.", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=1.0, caps=[
   ("Bẫy: nhầm rad/s với vòng/giây.", 4.4),
   ("Kết quả này còn giới hạn.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.4, caps=[
   ("Dừng video, tự trả lời.", 7.6)]),
])
