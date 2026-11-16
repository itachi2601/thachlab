# Clip: tn-l12-xoaychieu-02 - Hai LED mac song song nguoc chieu: dem so lan doi chieu (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-xoaychieu-02.json:
#   so_lieu_mau: f = 1 ; 5 ; 25 ; 50 Hz -> T = 1,0 ; 0,2 ; 0,04 ; 0,02 s -> doi chieu 2 ; 10 ; 50 ; 100 lan/s.
#   dung_cu: dien tro bao ve 330 ohm ; quan_sat: 1 Hz chop luan phien, 50 Hz trong nhu sang lien tuc.
#   tham_so f toi da 60 Hz -> ca cau chot (chua hien tren man): 60 Hz -> doi chieu 120 lan/s, LED do sang 60 lan/s.
# Du doan (khung ben canh, K10: mp4 khong ve nut A-D): f = 1 Hz, moi giay dong dien doi chieu may lan?
#   A. 1 lan (hien_tuong_hay_sai #1: f thay vi 2f)   B. 2 lan (dung)   C. 4 lan   D. 0,5 lan
#   Khong trung Cau 2 trong bai (100.pi -> 50 Hz -> 100 lan/s). Khac xoaychieu3 (mot chieu vs xoay chieu, cong suat).
# u = U0.cos(2.pi.f.t): tai t = 0 dong khac 0 -> giay dau du 2f lan doi chieu (tranh truong hop 2f - 1 trong bai).
from engine import *

ROWS = [(1, "1,0", "2"), (5, "0,2", "10"), (25, "0,04", "50"), (50, "0,02", "100")]
NOTE = (70, 75, 95)
LGREEN = (22, 163, 74)
THR = 0.15                                   # nguong sang cua LED (ti le U0), bo qua o mo hinh nhung de den tat gan u = 0

# ---------------- mach: may phat tin hieu - dien tro - hai LED nguoc chieu ----------------
def led(d, cx, cy, right, col, lit):
    """LED: tam giac chi chieu cho dong qua (right=True: trai -> phai) + vach; lit 0..1."""
    if lit > 0:
        for k in range(6, 0, -1):
            dot(d, cx, cy, 34 + k * 13, A(col, 0.08 * lit))
    s = 1 if right else -1
    tri = [(cx - s * 30, cy - 34), (cx - s * 30, cy + 34), (cx + s * 30, cy)]
    d.polygon(tri, fill=mix(WHITE, col, 0.25 + 0.75 * lit), outline=NAVY, width=4)
    d.line([(cx + s * 32, cy - 36), (cx + s * 32, cy + 36)], fill=NAVY, width=6)
    for j in (-1, 1):                                            # hai mui tia sang
        x0, y0 = cx + 6 + j * 14, cy - 44
        arrow(d, (x0, y0), (x0 + 22, y0 - 26), A(col, 0.35 + 0.65 * lit), w=4, head=10)

def resistor(d, x0, x1, y):
    d.rectangle([x0, y - 22, x1, y + 22], fill=WHITE, outline=NAVY, width=5)
    text(d, ((x0 + x1) / 2, y - 60), "330 Ω", 44, INK)

AX, BX, Y1, Y2, YT, YB = 700, 980, 450, 610, 390, 710
def circuit(d, f_lab, lr, lg, cur, eye=0.0, lab=True):
    """lr, lg: do sang LED do/xanh; cur: +1 dong theo chieu do sang, -1 chieu xanh, 0 khong ve mui ten."""
    card(d, (40, 250, 1040, 790), fill=WHITE, outline=LIGHT, w=3)
    # may phat tin hieu
    card(d, (70, 330, 400, 760), fill=(241, 245, 249), outline=NAVY, r=22, w=5)
    if lab:
        text(d, (235, 380), "Máy phát", 44, NOTE, bold=False)
        text(d, (235, 430), "tín hiệu", 44, NOTE, bold=False)
    d.rounded_rectangle([100, 480, 370, 570], radius=12, fill=NAVY)
    text(d, (235, 525), f_lab, 50, (134, 239, 172))
    pts = [(165 + j * 140 / 40, 660 - 34 * math.sin(2 * math.pi * j / 40)) for j in range(41)]
    d.line(pts, fill=ORANGE, width=6, joint="curve")
    # day
    W_ = dict(fill=NAVY, width=6)
    d.line([(400, YT), (470, YT)], **W_); d.line([(610, YT), (AX, YT), (AX, Y2)], **W_)
    resistor(d, 470, 610, YT)
    d.line([(AX, Y1), (BX, Y1)], **W_); d.line([(AX, Y2), (BX, Y2)], **W_)
    d.line([(BX, Y1), (BX, YB), (400, YB)], **W_)
    for x, y in ((AX, Y1), (AX, Y2), (BX, Y1), (BX, Y2)): dot(d, x, y, 10, NAVY)
    d.rectangle([800, Y1 - 40, 880, Y1 + 40], fill=WHITE); d.rectangle([800, Y2 - 40, 880, Y2 + 40], fill=WHITE)
    led(d, 840, Y1, True, RED, lr)
    led(d, 840, Y2, False, LGREEN, lg)
    text(d, (750, Y1 - 50), "đỏ", 44, RED)
    text(d, (748, Y2 + 54), "xanh", 44, LGREEN)
    if cur:                                                      # chieu dong tren day duoi: do sang -> ve trai
        x0, x1 = (820, 560) if cur > 0 else (560, 820)
        arrow(d, (x0, YB), (x1, YB), BLUE, w=8, head=24)
        if lab: text(d, (690, YB + 46), "chiều dòng", 44, BLUE)
    if eye > 0:
        text(d, (690, YB + 46), "mắt thấy: sáng liên tục", 44, NOTE, alpha=eye)

def led_lit(u):
    return clamp((u - THR) / (1 - THR)), clamp((-u - THR) / (1 - THR))

# ---------------- do thi u(t) ----------------
GX0, GX1 = 150, 990
def graph(d, y0, y1, f, kx, cursor=None, shade=False, marks=False, a=1.0, tlab="1 s"):
    """Ve u = cos(2.pi.f.tau), tau 0..1 s (kx: phan da ve). cursor: tau cua con tro."""
    yc, amp = (y0 + y1) / 2, (y1 - y0) / 2 - 22
    X = lambda tau: GX0 + (GX1 - GX0) * tau
    d.line([(GX0, yc), (GX1 + 24, yc)], fill=A(NAVY, a), width=4)
    d.line([(GX0, y1 - 4), (GX0, y0 + 4)], fill=A(NAVY, a), width=4)
    text(d, (GX0 - 40, y0 + 22), "u", 44, INK, alpha=a)
    text(d, (GX0 - 30, yc + 36), "0", 44, MUTED, bold=False, alpha=a)
    text(d, (GX1, yc + 40), tlab, 44, MUTED, bold=False, alpha=a)
    n = max(120, int(24 * f)); m = int(n * kx)
    if shade and m > 0:
        for j in range(m):
            tau = j / n; u = math.cos(2 * math.pi * f * tau)
            d.line([(X(tau), yc), (X(tau), yc - amp * u)], fill=A(RED if u > 0 else LGREEN, 0.22 * a), width=max(2, int((GX1 - GX0) / n) + 1))
    if m > 1:
        pts = [(X(j / n), yc - amp * math.cos(2 * math.pi * f * j / n)) for j in range(m + 1)]
        d.line(pts, fill=A(ORANGE, a), width=5 if f < 20 else 3, joint="curve")
    if marks:
        for z in (0.25, 0.75):
            if kx >= z: dot(d, X(z), yc, 13, A(BLUE, a), outline=A(WHITE, a))
    if cursor is not None:
        d.line([(X(cursor), y0), (X(cursor), y1)], fill=A(PURPLE, a), width=4)
    return X, yc

# ---------------- bang so lieu ----------------
def table(d, nrows, y0=1180, a=1.0):
    card(d, (60, y0, 1020, y0 + 112 + 4 * 74), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    cols = (210, 480, 800)
    for cx, h in zip(cols, ("f (Hz)", "T (s)", "Đổi chiều/s")):
        text(d, (cx, y0 + 52), h, 46, NAVY, alpha=a)
    d.line([(90, y0 + 92), (990, y0 + 92)], fill=A(NAVY, a), width=3)
    for i in range(nrows):
        y = y0 + 130 + i * 74
        for j, cx in enumerate(cols):
            text(d, (cx, y), str(ROWS[i][j]), 46, INK if j < 2 else BLUE, alpha=a)

# ---------------- canh 1: mo bai + du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    circuit(d, "f = 1 Hz", 0, 0, 0)
    a = appear(t, M[1] - 0.4, 0.5)
    if a <= 0: return
    y0 = 880 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(44)) + 56
    card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 96), fill=A(PURPLE, a), r=34)
    text(d, (W / 2, y0 + 62), "DỰ ĐOÁN", 44, WHITE, alpha=a)
    text(d, (W / 2, y0 + 190), "Ở 1 Hz, mỗi giây dòng điện", 50, INK, alpha=a)
    text(d, (W / 2, y0 + 275), "đổi chiều mấy lần?", 50, INK, alpha=a)
    tc, te = M[1] + 0.4, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (te - tc))
        d.rounded_rectangle([140, y0 + 410, 940, y0 + 426], radius=8, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 410, 140 + 800 * (1 - p), y0 + 426], radius=8, fill=A(PURPLE, a))

# ---------------- canh 2: tien hanh ----------------
SLOW = 3.0                                   # 1 s that cua giai doan 1 Hz chieu trong 3 s
def stages(sc):
    a0 = sc["M"][0] + 0.4; return a0, a0 + SLOW, a0 + SLOW + 0.3, a0 + SLOW + 2.5, a0 + SLOW + 3.9

def do_state(t, sc):
    """Mot ham cho may phat, LED, chieu dong, do thi, bang (dong bo moc)."""
    a0, a1, b0, c0, d0 = stages(sc)
    if t < a0: return dict(f=1, lab="f = 1 Hz", u=None, rows=0, g=(1, 0.0, None), eye=0.0)
    if t < b0:
        tau = clamp((t - a0) / SLOW)
        return dict(f=1, lab="f = 1 Hz", u=math.cos(2 * math.pi * tau), rows=1 if t >= a1 else 0, g=(1, tau, tau), eye=0.0)
    if t < c0:
        tt = t - b0
        return dict(f=5, lab="f = 5 Hz", u=math.cos(2 * math.pi * 5 * tt), rows=2, g=(5, 1.0, tt % 1.0), eye=0.0)
    if t < d0: return dict(f=25, lab="f = 25 Hz", u=None, rows=3, g=(25, 1.0, None), eye=0.0, steady=0.75)
    return dict(f=50, lab="f = 50 Hz", u=None, rows=4, g=(50, 1.0, None), eye=appear(t, d0 + 0.3), steady=0.75)

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    s = do_state(t, sc)
    if s["u"] is not None:
        lr, lg = led_lit(s["u"]); cur = 1 if s["u"] > THR else (-1 if s["u"] < -THR else 0)
    else:
        lr = lg = s.get("steady", 0.0); cur = 0
    circuit(d, s["lab"], lr, lg, cur, eye=s["eye"])
    card(d, (60, 820, 1020, 1150), fill=WHITE, outline=LIGHT, w=3)
    f, kx, cu = s["g"]
    X, yc = graph(d, 850, 1110, f, kx, cursor=cu, marks=(f == 1))
    if f == 1 and kx > 0:
        k = sum(1 for z in (0.25, 0.75) if kx >= z)
        text(d, (990, 862), f"đổi chiều: {k}", 46, BLUE, anchor="rm")
    if f == 1 and kx < 1: text(d, (520, 860), "chiếu chậm", 44, NOTE, bold=False)
    table(d, s["rows"])

# ---------------- canh 3: dap an + rut ra + chua noi duoc ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    tau = ((t - 0.2) / SLOW) % 1.0 if t > 0.2 else 0.0
    u = math.cos(2 * math.pi * tau); lr, lg = led_lit(u)
    circuit(d, "f = 1 Hz", lr, lg, 1 if u > THR else (-1 if u < -THR else 0), lab=False)
    b = appear(t, 0.2)
    pw = tw(d, "ĐÁP ÁN · 2 lần", F(48)) + 70
    card(d, (W / 2 - pw / 2, 815, W / 2 + pw / 2, 895), fill=A((220, 252, 231), b), outline=A(GREEN, b), r=40, w=4)
    text(d, (W / 2, 855), "ĐÁP ÁN · 2 lần", 48, GREEN, alpha=b)
    card(d, (60, 920, 1020, 1250), fill=WHITE, outline=LIGHT, w=3)
    X, yc = graph(d, 950, 1220, 1, 1.0, cursor=tau, shade=True, marks=True, tlab="T")
    r = appear(t, M[0] + 1.0)
    if r > 0:
        card(d, (60, 1280, 1020, 1590), fill=A((236, 253, 243), r), outline=A(GREEN, r), w=5)
        text(d, (W / 2, 1360), "Mỗi LED sáng 1 lần", 48, INK, alpha=r)
        text(d, (W / 2, 1440), "Đổi chiều 2 lần", 48, BLUE, alpha=r)
        text(d, (W / 2, 1525), "→ 2f lần mỗi giây", 50, GREEN, alpha=appear(t, M[1] - 0.1))
    c = appear(t, M[2] - 0.1)
    if c > 0:
        card(d, (60, 920, 1020, 1590), fill=A(WHITE, c), outline=A(NAVY, c), w=5)
        text(d, (W / 2, 1010), "Chưa nói được gì?", 50, NAVY, alpha=c)
        for j, s in enumerate(("Tần số chính xác?", "Giá trị hiệu dụng?")):
            y = 1170 + j * 130
            dot(d, 130, y, 10, A(NAVY, c))
            text(d, (160, y), s, 46, INK, anchor="lm", alpha=c)

# ---------------- canh 4: hai bay ----------------
def xmark(d, x, y, a=1.0):
    d.line([(x - 22, y - 22), (x + 22, y + 22)], fill=A(RED, a), width=9); d.line([(x + 22, y - 22), (x - 22, y + 22)], fill=A(RED, a), width=9)
def vmark(d, x, y, a=1.0):
    d.line([(x - 24, y), (x - 6, y + 20), (x + 26, y - 22)], fill=A(GREEN, a), width=9, joint="curve")

def s_trap(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    # bay 1: f lan hay 2f lan (hinh mot chu ki co hai diem doi chieu, hien ngay)
    card(d, (40, 300, 1040, 920), fill=WHITE, outline=RED, w=4)
    xmark(d, 110, 360); text(d, (150, 360), "Đổi chiều f lần/giây", 46, RED, anchor="lm")
    graph(d, 430, 760, 1, 1.0, shade=True, marks=True, tlab="T")
    a1 = appear(t, M[0] + 2.2)
    vmark(d, 110, 860, a1); text(d, (150, 860), "Mỗi chu kì: 2 lần", 46, GREEN, anchor="lm", alpha=a1)
    # bay 2: sang deu = mot chieu?
    a2 = appear(t, M[1] - 0.2)
    if a2 <= 0: return
    card(d, (40, 950, 1040, 1600), fill=A(WHITE, a2), outline=A(RED, a2), w=4)
    xmark(d, 110, 1000, a2); text(d, (150, 1000), "Sáng đều → không đổi chiều", 46, RED, anchor="lm", alpha=a2)
    for cx, col in ((300, RED), (780, LGREEN)):
        for k in range(5, 0, -1): dot(d, cx, 1110, 30 + k * 12, A(col, 0.1 * a2))
        dot(d, cx, 1110, 34, A(mix(WHITE, col, 0.8), a2), outline=A(NAVY, a2))
    text(d, (W / 2, 1110), "50 Hz", 46, INK, alpha=a2)
    a3 = appear(t, M[1] + 2.0)
    if a3 > 0:
        X = lambda tau: 150 + 840 * tau
        pts = [(X(j / 1200), 1300 - 70 * math.cos(2 * math.pi * 50 * j / 1200)) for j in range(1201)]
        d.line(pts, fill=A(ORANGE, a3), width=2)
        d.line([(150, 1300), (1000, 1300)], fill=A(NAVY, a3), width=3)
        text(d, (995, 1395), "1 s", 44, MUTED, bold=False, alpha=a3)
        vmark(d, 110, 1520, a3); text(d, (150, 1520), "Vẫn đổi chiều, mắt không kịp", 46, GREEN, anchor="lm", alpha=a3)

# ---------------- canh 5: chot + cau hoi ----------------
# Chot + THU NGHI: nhu chot_hoi cua engine nhung hop cau hoi thu theo noi dung, goi y hien tre (cong B 14/11).
def chot_hoi_gon(d, t, sc, chot, hoi, goi_y=None, tre=2.5):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 410, chot, 52, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    hq = len(wrap(d, hoi, F(48), 880)) * 48 * 1.22
    y1 = int(760 + hq + 40)
    card(d, (40, 620, 1040, y1), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(44)) + 56
    card(d, (W / 2 - pw / 2, 646, W / 2 + pw / 2, 718), fill=A(ORANGE, k1), r=36)
    text(d, (W / 2, 682), "THỬ NGHĨ", 44, WHITE, alpha=k1)
    ctext(d, 760 + hq / 2 - 10, hoi, 48, INK, maxw=880, alpha=appear(t, M[0] + 0.4, 0.5))
    if goi_y:
        kh = appear(t, M[0] + tre, 0.5)
        if kh > 0:
            card(d, (110, y1 + 40, 970, y1 + 250), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
            text(d, (W / 2, y1 + 95), "Gợi ý", 44, MUTED, alpha=kh)
            ctext(d, y1 + 180, goi_y, 48, ORANGE, maxw=820, alpha=kh)

def s_end(img, d, t, sc):
    IMG_REF[0] = img
    chot_hoi_gon(d, t, sc, "Mỗi chu kì, dòng điện\nđổi chiều 2 lần",
                 "f = 60 Hz: mỗi giây đổi chiều mấy lần? Đèn đỏ sáng mấy lần?",
                 "1 giây có mấy chu kì?", tre=2.8)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    a0, a1, b0, c0, d0 = stages(do)
    out = [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding"),
           (do["t0"] + a0, "tap"), (do["t0"] + a1, "tap"), (do["t0"] + b0, "tap"), (do["t0"] + c0, "tap"), (do["t0"] + d0, "tap"),
           (an["t0"] + 0.2, "ding"), (an["t0"] + an["M"][2] - 0.1, "tap"),
           (tr["t0"] + 0.1, "buzz"), (tr["t0"] + tr["M"][1] - 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l12-xoaychieu-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Dòng điện xoay chiều · thachlab.id.vn", scenes=[
 dict(key="hook", title="Hai LED mắc ngược chiều", draw=s_hook, tail=0.3, caps=[
   ("Nhìn hai đèn LED.", 2.5),
   ("Chọn đáp án ở khung câu hỏi.", 6.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("1 Hz: đếm số lần đổi lượt.", 3.6),
   ("Tăng f: 5, 25 rồi 50 Hz.", 4.6)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.9, caps=[
   ("Nhìn một chu kì.", 3.6),
   ("Mỗi giây có f chu kì.", 3.0),
   ("Giới hạn của thí nghiệm.", 4.0)]),
 dict(key="trap", title="Cái bẫy", draw=s_trap, tail=0.8, caps=[
   ("Bẫy 1: f hay 2f lần?", 3.8),
   ("Bẫy 2: sáng đều là một chiều?", 4.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video và trả lời.", 7.8)]),
])
