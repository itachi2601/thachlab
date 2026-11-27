# Clip: tn-l11-tudien-01 - Tu nap roi phong qua den LED (ban 2 cong moi, 27/11/2026)
# So lieu tu content/thi-nghiem/tn-l11-tudien-01.json (mo hinh, khong phai so do that):
#   U = 9 V, C = 1000 uF, R = 1 kOhm -> tau = RC = 1,0 s ; Q = CU = 9000 uC (hang 1 so_lieu_mau).
#   i(t) = (U/R).exp(-t/tau) khi nap ; khi phong dong nguoc chieu, cung dang exp.
# Du doan (khung ben canh, K10 khong ve nut): dong K, pin van noi mai, LED the nao?
#   A. sang deu ; B. loe roi tat han (DUNG) ; C. mo dan khong bao gio tat ; D. khong sang.
# Cau chot v4 (luot cuoi 27/11; bai khong day R.C nen bo cau "loe lau gap may lan"): giu tu 1000 uF, pin 9 V,
#   doi R 1 -> 2 kOhm, cho LED tat han -> tu giu Q = CU = 9000 uC, KHONG DOI (hang 1 so_lieu_mau; R chi doi
#   thoi gian nap). Clip KHONG chieu Q = 9000 uC, khong viet "tu day".
# KHONG LO QUIZ sau hop ("Vi sao LED tat han du pin van con noi?" - dap an: tu nap day nen dong ngung):
#   clip khong viet "tu day"/"het cho"; the "Chua noi duoc" day cau hoi do sang quiz.
# Bay (cac_buoc.lam buoc 2): phong ma quen dao LED -> LED chan dong, tu VAN con dien tich (hai mach canh nhau).
# Mach (vat li): pin + o tren -> K -> canh phai di xuong qua LED (anot tren) + R -> day duoi sang trai -> ban PHAI
#   cua tu (tich +) ; ban trai (tich -) -> pin -. Nap: chieu kim dong ho. Phong (thao pin, dao LED): ban + day dong
#   sang phai, len canh phai (LED anot duoi), sang trai, xuong ve ban - : nguoc chieu kim dong ho.
from engine import *

U, C_UF, R_K = 9, 1000, 1
TAU = R_K * 1e3 * C_UF * 1e-6
assert abs(TAU - 1.0) < 1e-9 and C_UF * U == 9000              # hang 1 so_lieu_mau
R_CHOT_K = 2
assert R_CHOT_K != R_K and C_UF * U == 9000                     # cau chot v4: Q khong phu thuoc R
DIR_NAP, DIR_PHONG = +1, -1
assert DIR_NAP == -DIR_PHONG

def ib(tp): return math.exp(-max(0.0, tp) / TAU)
def qf(tp): return 1 - math.exp(-max(0.0, tp) / TAU)

WIRE = NAVY; ARR = (194, 65, 12); BOXF = (70, 78, 100); DRED = (185, 28, 28); DGREEN = (21, 110, 55)
XL, XR, YT, YB = 190, 890, 300, 760
XC = 540
YLED, YRES = 450, 615

def wire(d, pts, w=6, col=WIRE): d.line(pts, fill=col, width=w, joint="curve")

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

EMPTY = (148, 140, 128)
def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

def led(d, cx, cy, b, up=False, a=1.0, r=56):
    """LED: quang sang ti le b; tam giac chi chieu cho dong qua (up = chi len)."""
    if b > 0.03:
        for k, rr in ((0.20, 2.0), (0.34, 1.5)):
            dot(d, cx, cy, r * rr * (0.6 + 0.4 * b), A((255, 90, 70), k * b * a))
    dot(d, cx, cy, r, A(mix((95, 40, 40), (255, 70, 60), b), a), outline=A(WIRE, a))
    s = -1 if up else 1; k = r / 56
    d.polygon([(cx - 26 * k, cy - 18 * s * k), (cx + 26 * k, cy - 18 * s * k), (cx, cy + 20 * s * k)], fill=A(WHITE, a))
    d.line([(cx - 26 * k, cy + 22 * s * k), (cx + 26 * k, cy + 22 * s * k)], fill=A(WHITE, a), width=6)

def circuit(d, k_on=0.0, pin=1.0, flip=0.0, q=0.0, b=0.0, mode=None, ia=0.0):
    wire(d, [(XL, 400), (XL, YT), (330, YT)])
    wire(d, [(450, YT), (XR, YT), (XR, YLED - 56)])
    wire(d, [(XR, YLED + 56), (XR, YRES - 55)])
    wire(d, [(XR, YRES + 55), (XR, YB), (XC + 16, YB)])
    wire(d, [(XC - 16, YB), (XL, YB), (XL, 640)])
    dot(d, 330, YT, 12, WHITE, outline=WIRE); dot(d, 450, YT, 12, WHITE, outline=WIRE)
    ang = math.radians(-32 * (1 - ease(k_on)))
    d.line([(330, YT), (330 + 120 * math.cos(ang), YT + 120 * math.sin(ang))], fill=WIRE, width=9)
    text(d, (390, YT + 70), "K", 60, INK)
    if pin > 0.02:
        card(d, (XL - 100, 400, XL + 100, 640), fill=A(BOXF, pin), r=20)
        text(d, (XL, 480), "pin", 58, WHITE, alpha=pin)
        text(d, (XL, 565), "9 V", 58, WHITE, alpha=pin)
        text(d, (XL + 140, 420), "+", 64, RED, alpha=pin)
        text(d, (XL + 140, 620), "−", 64, BLUE, alpha=pin)
    if pin < 0.98: wire(d, [(XL, 400), (XL, 640)], col=A(WIRE, 1 - pin))
    led(d, XR, YLED, b, up=flip >= 0.5)
    d.rectangle([XR - 24, YRES - 55, XR + 24, YRES + 55], fill=WHITE, outline=WIRE, width=5)
    text(d, (XR - 50, YRES), "1 kΩ", 58, INK, anchor="rm")
    text(d, (XR - 90, YLED), "LED", 58, INK, anchor="rm")
    for x in (XC - 16, XC + 16): d.rectangle([x - 6, YB - 70, x + 6, YB + 70], fill=WIRE)
    text(d, (XC, YB + 125), "1000 μF", 58, INK)
    if q > 0.02:
        for yy in (YB - 36, YB + 36):
            text(d, (XC + 52, yy), "+", 60, RED, alpha=q)
            text(d, (XC - 52, yy), "−", 60, BLUE, alpha=q)
    if mode and ia > 0.04:
        col = A(ARR, clamp(0.25 + 0.75 * ia))
        segs = [((XL, 385), (XL, 325)), ((560, YT), (720, YT)), ((XR, 690), (XR, 745)), ((820, YB), (680, YB))]
        if mode == "phong": segs = [(q2, p2) for p2, q2 in segs]
        for p1, p2 in segs: arrow(d, p1, p2, col, w=9, head=26)

# ---------------- do thi i(t) ----------------
PW = 480
def panel(d, x0, y0, kind, tp, a=1.0, rev=0.0):
    """kind 'nap' (i > 0) / 'phong' (i < 0, truc t o tren). tp = thoi gian da ve (s, 0..4)."""
    card(d, (x0, y0, x0 + PW, y0 + 520), fill=A(WHITE, a), outline=A(LIGHT, a), r=24, w=3)
    ox = x0 + 80; xs = lambda t: ox + t / 4 * (PW - 140); hi = 250
    if kind == "nap": ax, sgn = y0 + 400, -1
    else: ax, sgn = y0 + 160, 1
    d.line([(ox, y0 + 110), (ox, y0 + 420)], fill=A(NAVY, a), width=4)
    d.line([(ox, ax), (ox + PW - 110, ax)], fill=A(NAVY, a), width=4)
    arrow(d, (ox + PW - 120, ax), (ox + PW - 100, ax), A(NAVY, a), w=4, head=16)
    text(d, (ox - 40, y0 + (120 if kind == "nap" else 400)), "i", 60, INK, alpha=a)
    text(d, (x0 + PW / 2 + 20, y0 + (55 if kind == "nap" else 470)), "nạp" if kind == "nap" else "phóng", 58, ARR if kind == "nap" else BLUE, alpha=a)
    if kind == "phong" and rev > 0: text(d, (x0 + PW / 2, y0 + 578), "i < 0: dòng ngược", 58, BLUE, alpha=a * rev)
    for t in (1, 2, 3, 4):
        d.line([(xs(t), ax - 9), (xs(t), ax + 9)], fill=A(NAVY, a), width=4)
        if t % 2 == 0: text(d, (xs(t), ax + (48 if kind == "nap" else -45)), str(t), 56, INK, alpha=a)
    text(d, (ox + PW - 140, ax + (110 if kind == "nap" else -105)), "t (s)", 56, INK, anchor="mm", alpha=a)
    if tp > 0:
        n = max(2, int(tp * 30)); pts = [(xs(0), ax)]
        for j in range(n + 1):
            t = tp * j / n; pts.append((xs(t), ax + sgn * hi * 0.92 * ib(t)))
        d.line(pts, fill=A(ARR if kind == "nap" else BLUE, a), width=8, joint="curve")

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    circuit(d)
    a = appear(t, M[1] - 0.2, 0.4)
    if a <= 0: return
    y0 = 960 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 190), "Đóng K, pin vẫn nối mãi.", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 290), "Đèn LED sẽ thế nào?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 410, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
T_ON = 0.8; T_RUN = 4.0; T_PH = 1.0
def s_do(img, d, t, sc):
    M = sc["M"]; t2 = M[1]
    if t < t2:
        tp = t - T_ON; on = t >= T_ON
        circuit(d, k_on=appear(t, T_ON - 0.25, 0.25), q=qf(tp) if on else 0, b=ib(tp) if on else 0,
                mode="nap" if on else None, ia=ib(tp) if on else 0)
        panel(d, 50, 960, "nap", clamp(tp, 0, T_RUN)); panel(d, 550, 960, "phong", 0, a=0.4)
        ka = appear(t, 3.6, 0.3)
        if ka > 0: pill(d, 500, 520, "pin vẫn nối", ORANGE, ka, size=56)
        return
    u = t - t2
    pin = 1 - appear(u, 0.0, 0.5); fl = appear(u, 0.3, 0.4)
    tp = u - T_PH; on = u >= T_PH
    q = 1 - qf(tp) if on else qf(T_RUN)
    circuit(d, k_on=1, pin=pin, flip=fl, q=q, b=ib(tp) if on else 0, mode="phong" if on else None, ia=ib(tp) if on else 0)
    ka = appear(u, 0.05, 0.3) * (1 - appear(u, 2.6, 0.4))
    if ka > 0:
        pill(d, 480, 460, "tháo pin", ORANGE, ka, size=56)
        pill(d, 520, 600, "đảo LED", ORANGE, ka, size=56)
    panel(d, 50, 960, "nap", T_RUN); panel(d, 550, 960, "phong", clamp(tp, 0, T_RUN) if on else 0)

# ---------------- canh 3: Ket qua ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    panel(d, 50, 290, "nap", T_RUN); panel(d, 550, 290, "phong", T_RUN, rev=appear(t, sc["M"][1] + 0.3, 0.4))
    ka = appear(t, 0.4, 0.4)
    card(d, (40, 920, 1040, 1080), fill=A(NAVY, ka), r=40)
    text(d, (W / 2, 1000), "ĐÁP ÁN · loé rồi tắt hẳn", 62, WHITE, alpha=ka)
    k1 = appear(t, M[1] + 0.3, 0.4)
    if k1 > 0:
        card(d, (40, 1130, 1040, 1310), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        text(d, (W / 2, 1220), "Tụ giữ điện tích, phóng lại", 62, DGREEN, alpha=k1)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def mini(d, ox, oy, ok, b, a=1.0):
    """Tu da nap noi voi LED. ok = LED da dao (cho dong phong qua)."""
    x0, x1, y0, y1, cx = ox, ox + 400, oy, oy + 360, ox + 170
    c = A(WIRE, a)
    d.line([(cx - 14, y1), (x0, y1), (x0, y0), (x1, y0), (x1, oy + 120)], fill=c, width=6, joint="curve")
    d.line([(x1, oy + 240), (x1, y1), (cx + 14, y1)], fill=c, width=6, joint="curve")
    for x in (cx - 14, cx + 14): d.rectangle([x - 6, y1 - 60, x + 6, y1 + 60], fill=c)
    text(d, (cx + 56, y1 - 32), "+", 58, RED, alpha=a); text(d, (cx - 56, y1 - 32), "−", 58, BLUE, alpha=a)
    led(d, x1, oy + 180, b, up=ok, a=a, r=50)
    if ok and b > 0.1:
        col = A(ARR, a * clamp(0.3 + b))
        arrow(d, (cx + 70, y1), (cx + 190, y1), col, w=8, head=24)
        arrow(d, (x1 - 100, y0), (x0 + 120, y0), col, w=8, head=24)

def s_bay(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    pill(d, W / 2, 290, "BẪY", DRED, k0)
    lit = appear(t, M[1], 0.4)
    bl = lit * (0.75 + 0.25 * math.cos((t - M[1]) * 3)) if lit > 0 else 0
    mini(d, 50, 430, True, bl, a=k0); mini(d, 590, 430, False, 0, a=k0)
    text(d, (270, 900), "đảo LED", 60, DGREEN, alpha=k0)
    text(d, (810, 900), "quên đảo", 60, DRED, alpha=k0)
    if lit > 0:
        text(d, (270, 1000), "sáng", 60, DGREEN, alpha=lit)
        text(d, (810, 1000), "tối", 60, DRED, alpha=lit)
        c = A(DRED, lit)
        d.line([(1010, 560), (1060, 660)], fill=c, width=10); d.line([(1060, 560), (1010, 660)], fill=c, width=10)
    k3 = appear(t, M[2] - 0.7, 0.4)
    if k3 > 0:
        card(d, (40, 1100, 1040, 1440), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 1170, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 1320), "Vì sao dòng về 0 dù còn pin?", 60, INK, alpha=k3)

# ---------------- canh 5: THU NGHI ----------------
def cap_icon(d, cx, cy, h, a):
    d.line([(cx - 140, cy), (cx - 20, cy)], fill=A(WIRE, a), width=6); d.line([(cx + 20, cy), (cx + 140, cy)], fill=A(WIRE, a), width=6)
    for x in (cx - 18, cx + 18): d.rectangle([x - 7, cy - h, x + 7, cy + h], fill=A(WIRE, a))

def res_icon(d, cx, cy, col, a):
    d.line([(cx - 150, cy), (cx - 70, cy)], fill=A(WIRE, a), width=6); d.line([(cx + 70, cy), (cx + 150, cy)], fill=A(WIRE, a), width=6)
    d.rectangle([cx - 70, cy - 28, cx + 70, cy + 28], outline=A(col, a), width=7)

def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 305, "THỬ NGHĨ", ORANGE, k)
    res_icon(d, 290, 520, INK, k); res_icon(d, 790, 520, ORANGE, k)
    arrow(d, (480, 520), (600, 520), A(ORANGE, k))
    text(d, (290, 640), "1 kΩ", 62, INK, alpha=k); text(d, (790, 640), "2 kΩ", 62, ORANGE, alpha=k)
    text(d, (W / 2, 820), "Vẫn tụ 1000 μF, pin 9 V,", 62, INK, alpha=k)
    text(d, (W / 2, 905), "điện trở đổi thành 2 kΩ.", 62, INK, alpha=k)
    text(d, (W / 2, 1060), "LED tắt hẳn: Q = ? μC", 64, DRED, alpha=k)
    seg_bar(d, 1260, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + T_ON, "tap"), (do["t0"] + do["M"][1] + T_PH, "tap"),
            (da["t0"] + 0.4, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l11-tudien-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Tụ điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Tụ, pin và đèn LED", draw=s_hook, tail=0.3, caps=[
   ("Pin 9 V, tụ, đèn LED.", 3.4),
   ("Dừng lại, tự đoán.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Đóng khoá K, nhìn đèn LED.", 6.0),
   ("Tháo pin, đảo LED, nối lại.", 5.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Dòng giảm dần về 0.", 3.6),
   ("Lúc phóng, dòng đổi chiều.", 4.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Bẫy: phóng mà quên đảo LED.", 3.6),
   ("LED tối, tụ vẫn còn điện.", 3.6),
   ("Câu hỏi còn bỏ ngỏ.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng lại, tự trả lời.", 7.2)]),
])
