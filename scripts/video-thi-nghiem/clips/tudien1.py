# Clip: tn-l11-tudien-01 - Tu nap roi phong qua den LED (16/11/2026)
# So lieu tu content/thi-nghiem/tn-l11-tudien-01.json (mo hinh, khong phai so do that):
#   U = 9 V, C = 1000 uF, R = 1 kOhm -> tau = RC = 1,0 s ; Q = CU = 9000 uC (hang 1 so_lieu_mau).
#   i(t) = (U/R).exp(-t/tau) khi nap ; khi phong dong nguoc chieu, cung dang exp (bo qua nguong LED).
#   Cau chot THU NGHI: tu 2200 uF, pin 9 V (hang 2) -> tau = 2,2 s so voi 1,0 s -> LED sang lau hon ~2,2 lan.
# KHONG LO QUIZ ngay sau hop ("Vi sao LED tat han du pin van con noi?" - dap an: tu nap day nen dong ngung):
#   clip chi cho thay hien tuong (LED loe roi tat, do thi i giam ve 0), khong viet "tu day" / "het cho";
#   the "Chua noi duoc" chuyen cau hoi do sang quiz. Bay khong dung hien_tuong_hay_sai (trung phuong an quiz)
#   ma dung buoc "dao chieu LED" cua cac_buoc.lam.
# Mach (vat li): pin + o tren -> K -> canh phai di xuong qua LED (anot tren) + R -> day duoi sang trai -> ban PHAI
#   cua tu (tich +) ; ban trai (tich -) -> pin -. Nap: chieu kim dong ho. Phong (thao pin, dao LED): ban + day dong
#   sang phai, len canh phai (LED anot duoi), sang trai, xuong ve ban - : nguoc chieu kim dong ho.
from engine import *

U, C_UF, R_K = 9, 1000, 1
TAU = R_K * 1e3 * C_UF * 1e-6
Q_UC = C_UF * U
assert abs(TAU - 1.0) < 1e-9 and Q_UC == 9000           # khop hang 1 so_lieu_mau
assert abs(R_K * 1e3 * 2200e-6 - 2.2) < 1e-9 and 2200 * 9 == 19800   # hang 2 (cau chot)
DIR_NAP, DIR_PHONG = +1, -1                              # +1 = chieu kim dong ho tren so do
assert DIR_NAP == -DIR_PHONG                             # dong phong nguoc chieu dong nap

def ib(tp): return math.exp(-max(0.0, tp) / TAU)         # i/I0 (do sang LED ti le)
def qf(tp): return 1 - math.exp(-max(0.0, tp) / TAU)     # q/Q khi nap

WIRE = NAVY
ARR = (194, 65, 12)
BOXF = (70, 78, 100)
DRED = (185, 28, 28)
XL, XR, YT, YB = 190, 890, 380, 820                      # khung mach
XC = 540                                                 # truc tu (tren day duoi)
YLED, YRES = 520, 690

def wire(d, pts, w=5, col=WIRE): d.line(pts, fill=col, width=w, joint="curve")

def led(d, cx, cy, b, up=False, a=1.0):
    """Den LED: quang sang ti le b; ki hieu diot ben trong, mui tam giac theo chieu cho dong qua (up = chi len)."""
    if b > 0.03:
        for k, r in ((0.18, 110), (0.32, 84)):
            dot(d, cx, cy, r * (0.6 + 0.4 * b), A((255, 90, 70), k * b * a))
    core = mix((95, 40, 40), (255, 70, 60), b)
    dot(d, cx, cy, 56, A(core, a), outline=A(WIRE, a))
    s = -1 if up else 1                                  # tam giac: day o phia anot, dinh o phia catot
    d.polygon([(cx - 26, cy - 18 * s), (cx + 26, cy - 18 * s), (cx, cy + 20 * s)], fill=A(WHITE, a))
    d.line([(cx - 26, cy + 22 * s), (cx + 26, cy + 22 * s)], fill=A(WHITE, a), width=6)

def circuit(d, k_on=0.0, pin=1.0, flip=0.0, q=0.0, b=0.0, mode=None, ia=0.0, lbl=True, led_up=None):
    """k_on 0..1 khoa dong; pin 1 = co pin, 0 = da thao (thay day noi); flip 0 = LED nhu luc nap, 1 = da dao;
    q 0..1 dien tich tren hai ban; b do sang LED; mode 'nap'/'phong' ve mui ten chieu dong, do dam ia."""
    # day: canh trai (tru doan pin), tren (tru khoa), phai (tru LED, R), duoi (tru tu)
    wire(d, [(XL, 470), (XL, YT), (330, YT)])
    wire(d, [(450, YT), (XR, YT), (XR, YLED - 56)])
    wire(d, [(XR, YLED + 56), (XR, YRES - 55)])
    wire(d, [(XR, YRES + 55), (XR, YB), (XC + 16, YB)])
    wire(d, [(XC - 16, YB), (XL, YB), (XL, 690)])
    # khoa K
    dot(d, 330, YT, 11, WHITE, outline=WIRE); dot(d, 450, YT, 11, WHITE, outline=WIRE)
    ang = math.radians(-32 * (1 - ease(k_on)))
    d.line([(330, YT), (330 + 120 * math.cos(ang), YT + 120 * math.sin(ang))], fill=WIRE, width=8)
    text(d, (390, YT - 70), "K", 40, INK)
    # pin (hop) hoac day noi thay pin
    if pin > 0.02:
        card(d, (XL - 90, 470, XL + 90, 690), fill=A(BOXF, pin), r=20)
        text(d, (XL, 545), "pin", 38, WHITE, alpha=pin)
        text(d, (XL, 615), "9 V", 44, WHITE, alpha=pin)
        text(d, (XL + 120, 450), "+", 44, RED, alpha=pin)
        text(d, (XL + 120, 712), "−", 44, BLUE, alpha=pin)
    if pin < 0.98:
        wire(d, [(XL, 470), (XL, 690)], col=A(WIRE, 1 - pin))
    # LED + dien tro
    up = (flip >= 0.5) if led_up is None else led_up
    led(d, XR, YLED, b, up=up)
    d.rectangle([XR - 22, YRES - 55, XR + 22, YRES + 55], fill=WHITE, outline=WIRE, width=5)
    text(d, (XR - 50, YRES), "1 kΩ", 38, INK, anchor="rm")
    text(d, (XR - 80, YLED), "LED", 40, INK, anchor="rm")
    # tu: hai ban doc tren day duoi
    for x in (XC - 16, XC + 16):
        d.rectangle([x - 5, YB - 66, x + 5, YB + 66], fill=WIRE)
    text(d, (XC, YB + 120), "1000 μF", 40, INK)
    if q > 0.02:
        for yy in (YB - 44, YB, YB + 44):
            text(d, (XC + 44, yy), "+", 38, RED, alpha=q)
            text(d, (XC - 44, yy), "−", 38, BLUE, alpha=q)
    # chieu dong qui uoc (do dam theo cuong do)
    if mode and ia > 0.04:
        col = A(ARR, clamp(0.25 + 0.75 * ia))
        segs = [((XL, 455), (XL, 395)), ((560, YT), (680, YT)), ((XR, 755), (XR, 810)), ((800, YB), (690, YB))]
        if mode == "phong":
            segs = [(b2, a2) for a2, b2 in segs]                       # nguoc chieu nap
        for p1, p2 in segs:
            arrow(d, p1, p2, col, w=7, head=20)
        if lbl:
            text(d, (660, YT - 60), "dòng điện" if mode == "nap" else "dòng phóng",
                 40, ARR, alpha=clamp(0.4 + ia))

# ---------------- do thi i(t) ----------------
PW, PH = 440, 400
def panel(d, x0, y0, kind, tp, a=1.0, lab=True):
    """kind 'nap' (i > 0, truc t o duoi) / 'phong' (i < 0, truc t o tren). tp = thoi gian da ve (s, 0..4)."""
    card(d, (x0, y0, x0 + PW + 20, y0 + PH + 80), fill=A(WHITE, a), outline=A(LIGHT, a), r=24, w=3)
    ox = x0 + 70; xs = lambda t: ox + t / 4 * (PW - 110)
    hi = 250
    if kind == "nap": ax, sgn = y0 + 120 + hi, -1
    else: ax, sgn = y0 + 120, 1
    d.line([(ox, y0 + 100), (ox, y0 + 120 + hi + 20)], fill=A(NAVY, a), width=4)
    arrow(d, (ox, y0 + 112), (ox, y0 + 90), A(NAVY, a), w=4, head=14)
    d.line([(ox, ax), (ox + PW - 70, ax)], fill=A(NAVY, a), width=4)
    arrow(d, (ox + PW - 80, ax), (ox + PW - 60, ax), A(NAVY, a), w=4, head=14)
    text(d, (ox - 30, y0 + 100), "i", 40, INK, alpha=a)
    title = "nạp" if kind == "nap" else "phóng"
    if lab: text(d, (ox + 30, y0 + 46), title, 40, ARR if kind == "nap" else BLUE, anchor="lm", alpha=a)
    for t in (1, 2, 3, 4):
        d.line([(xs(t), ax - 8), (xs(t), ax + 8)], fill=A(NAVY, a), width=3)
        text(d, (xs(t), ax + (44 if kind == "nap" else -42)), str(t), 44, INK, alpha=a)
    text(d, (x0 + PW - 10, ax + (92 if kind == "nap" else 50)), "t (s)", 44, INK, anchor="rm", alpha=a)
    if tp > 0:
        n = max(2, int(tp * 30)); pts = []
        for j in range(n + 1):
            t = tp * j / n; pts.append((xs(t), ax + sgn * hi * 0.92 * ib(t)))
        pts.insert(0, (xs(0), ax))
        d.line(pts, fill=A(ARR if kind == "nap" else BLUE, a), width=7, joint="curve")

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    circuit(d)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1000 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, a), r=33)
    text(d, (W / 2, y0 + 59), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 230, "Đóng khoá K, pin vẫn nối mãi.\nĐèn LED sẽ thế nào?", 50, INK, maxw=900, alpha=a)
    text(d, (W / 2, y0 + 400), "Chọn đáp án ở khung câu hỏi", 40, MUTED, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 490, 940, y0 + 502], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 490, 140 + 800 * (1 - p), y0 + 502], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (mot canh lien mach: nap -> thao pin, dao LED -> phong) ----------------
T_ON = 0.8           # dong khoa
T_RUN = 4.0          # moi giai doan chieu 4 s thoi gian thuc (= 4 tau)
SW0, SW1 = 0.0, 0.9  # tinh tu M[1]: thao pin + dao LED trong [SW0, SW1]
T_PH = 1.0           # tinh tu M[1]: noi lai, tu bat dau phong

def s_do(img, d, t, sc):
    M = sc["M"]; t2 = M[1]
    if t < t2:                                           # nap, pin van noi
        tp = t - T_ON; on = t >= T_ON
        circuit(d, k_on=appear(t, T_ON - 0.25, 0.25), q=qf(tp) if on else 0, b=ib(tp) if on else 0,
                mode="nap" if on else None, ia=ib(tp) if on else 0)
        panel(d, 60, 1000, "nap", clamp(tp, 0, T_RUN)); panel(d, 560, 1000, "phong", 0, a=0.45)
        if on and tp > 2.6:
            text(d, (XL + 150, 600), "pin vẫn nối", 38, ORANGE, anchor="lm", alpha=appear(tp, 2.6, 0.4))
        return
    u = t - t2
    pin = 1 - appear(u, SW0, 0.5); fl = appear(u, SW0 + 0.3, 0.5)
    tp = u - T_PH; on = u >= T_PH
    q = 1 - qf(tp) if on else qf(T_RUN)
    circuit(d, k_on=1, pin=pin, flip=fl, q=q, b=ib(tp) if on else 0, mode="phong" if on else None,
            ia=ib(tp) if on else 0)
    if u < SW1:
        text(d, (XL + 160, 580), "tháo pin", 40, ORANGE, anchor="lm", alpha=appear(u, 0.1, 0.3))
        text(d, (XR - 80, YLED + 90), "đảo LED", 40, ORANGE, anchor="rm", alpha=appear(u, 0.3, 0.3))
    panel(d, 60, 1000, "nap", T_RUN); panel(d, 560, 1000, "phong", clamp(tp, 0, T_RUN) if on else 0)

# ---------------- canh 3: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN B · loé rồi tắt hẳn"
    pw = tw(d, lab, F(40)) + 52
    card(d, (W - 60 - pw, 300, W - 60, 364), fill=A(NAVY, ka), r=32)
    text(d, (W - 60 - pw / 2, 332), lab, 40, WHITE, alpha=ka)
    panel(d, 60, 400, "nap", T_RUN); panel(d, 560, 400, "phong", T_RUN)
    kn = appear(t, M[1] - 0.1, 0.4)
    if kn > 0:
        text(d, (800, 830), "ngược chiều nạp", 38, BLUE, alpha=kn)
    k1 = appear(t, M[1] + 0.3, 0.45)
    if k1 > 0:
        card(d, (40, 1000, 1040, 1230), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), r=24, w=4)
        ctext(d, 1115, "Không còn pin, LED vẫn loé:\ntụ đã giữ điện tích", 46, (21, 110, 55), maxw=920, alpha=k1)

# ---------------- canh 4: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    circuit(d, k_on=1, pin=0, flip=0, q=1, b=0, led_up=False)       # phong ma KHONG dao LED: LED chan dong
    ax = appear(t, 0.3, 0.3)
    if ax > 0:                                                       # dau X do canh LED
        c = A(DRED, ax)
        d.line([(XR + 70, YLED - 40), (XR + 130, YLED + 40)], fill=c, width=10)
        d.line([(XR + 130, YLED - 40), (XR + 70, YLED + 40)], fill=c, width=10)
    if a1 > 0:
        y0 = 1000
        card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 96), fill=A(DRED, a1), r=33)
        text(d, (W / 2, y0 + 63), "BẪY", 40, WHITE, alpha=a1)
        k3 = a1 * appear(t, 0.5, 0.5); k4 = a1 * appear(t, 1.8, 0.5)
        ctext(d, y0 + 210, "LED tối:\ntưởng tụ rỗng", 46, INK, maxw=920, alpha=k3)
        ctext(d, y0 + 420, "Thật ra LED\nchặn dòng phóng", 46, (21, 110, 55), maxw=920, alpha=k4)
    if k2 > 0:
        y0 = 1000 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Vì sao dòng về 0 dù pin còn?", "• Tụ giữ bao nhiêu điện tích?")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (80, y0 + 220 + j * 150), l1, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi quiz) -> THU NGHI: tu 2200 uF, pin 9 V nhu cu: LED loe lau gap bao nhieu lan so voi
    lan dung tu 1000 uF? Goi y = du kien thay doi, hien tre 2,5 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 400, "Tụ tích điện, giữ lại,\nrồi phóng ra", 50, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.6, 0.5)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 1590), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 696), fill=A(ORANGE, k1), r=33)
    text(d, (W / 2, 663), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    ctext(d, 880, "Thay tụ 2200 μF, pin vẫn 9 V.\nLED loé lâu gấp bao nhiêu lần\nso với lần tụ 1000 μF?",
          48, INK, maxw=940, alpha=appear(t, M[0] + 0.9, 0.5))
    th = M[0] + 0.9; kh = appear(t, th + 2.5, 0.5)
    card(d, (110, 1140, 970, 1480), fill=A((255, 247, 237), k1), r=24)
    ctext(d, 1215, "Gợi ý", 40, INK, alpha=k1)
    if t > th and kh < 1:
        p = clamp((t - th) / 2.5); kb = k1 * (1 - kh)
        d.rounded_rectangle([200, 1334, 880, 1346], radius=6, fill=A(LIGHT, kb))
        d.rounded_rectangle([200, 1334, 200 + 680 * (1 - p), 1346], radius=6, fill=A(ORANGE, kb))
    ctext(d, 1350, "Chỉ đổi tụ,\npin như cũ", 48, (154, 52, 18), maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + T_ON, "tap"), (do["t0"] + do["M"][1] + T_PH, "tap"),
            (da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.6, "open")]

CLIP = dict(id="tn-l11-tudien-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Tụ điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Tụ, pin và đèn LED", draw=s_hook, tail=0.3, caps=[
   ("Pin 9 V, tụ 1000 μF, đèn LED.", 2.8),
   ("Nghĩ kỹ trước khi xem tiếp.", 6.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Đóng khoá K, pin vẫn nối.", 5.2),
   ("Tháo pin, đảo LED, nối lại.", 5.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Dòng qua LED giảm dần, LED tối.", 3.6),
   ("Lúc phóng, dòng đổi chiều.", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.8, caps=[
   ("Bẫy: phóng mà quên đảo LED.", 4.2),
   ("Hai câu còn bỏ ngỏ.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Dừng video, tự trả lời.", 7.4)]),
])
