# Clip: tn-l10-co-nang-bao-toan-01 - Con lac qua cong quang (ban 2 theo cong moi, 27/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-co-nang-bao-toan-01.json:
#   so_lieu_mau: h (cm) 5 / 10 / 15 / 20 ; v do (m/s) 0,98 / 1,39 / 1,70 / 1,97 ; v^2/(2gh) 96,0 / 96,6 / 96,3 / 97,0 %
#   tham_so: h 0,02-0,30 m; g = 10; k = 0,965 (mo hinh v ~ can h); day ~1 m -> chu ki ~2 s.
# Du doan (K10: chi cau hoi + hinh): tha 5 cm -> 0,98 m/s; tha 20 cm (cao gap 4) -> toc do gap may lan? Dap an: ~2 lan.
# Bay: hien_tuong_hay_sai[1] "luc cang day lam mat co nang" -> hinh: T luon vuong goc v khi con lac lac.
# Cau chot (tu suy, khac dang quiz bai): tha tu 18 cm, bo qua can; luc con cao 10 cm -> ha 8 cm,
#   v = can(2.10.0,08) = 1,26 m/s (trong dai tham_so 2-30 cm; KHONG hien tren man).
from engine import *

ROWS = [(5, "0,98"), (10, "1,39"), (15, "1,70"), (20, "1,97")]     # so_lieu_mau: h (cm), v do (m/s)
PCT = [96.0, 96.6, 96.3, 97.0]                                     # so_lieu_mau: v^2/(2gh) (%)
def fm(x, n=1): return f"{x:.{n}f}".replace(".", ",")

STEEL = (120, 128, 150); BOB = (70, 90, 160); BOB_D = (40, 52, 110)
EMPTY = (148, 140, 128); DORANGE = (176, 64, 8)
TP = 2.0                       # chu ki (day 1 m, g = 10 -> 1,99 s)
PX, PY, LPX = 540, 250, 620    # diem treo, day 1 m = 620 px
YB = PY + LPX                  # tam qua nang o day (y 870)
RB = 34

def th(hcm): return math.acos(1 - hcm / 100.0)
def bob_xy(theta, px=PX, py=PY, L=LPX): return px + L * math.sin(theta), py + L * math.cos(theta)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0, n=6):
    """Thanh dem nhay tung o (moi o 130x70) de hinh doi that; n khong trung dap an."""
    p = clamp((t - t0) / (t1 - t0)); on = n - int(p * n + 1e-9); w = 780 / n
    for i in range(n):
        x = 150 + i * w
        if i < on: card(d, (x, y, x + w - 20, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + w - 20, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

def stand(d, px=PX, py=PY, hw=210):
    d.rounded_rectangle([px - hw, py - 24, px + hw, py], radius=8, fill=(150, 155, 172))
    d.polygon([(px - 18, py), (px + 18, py), (px, py + 16)], fill=NAVY)

def gate(d):
    d.rounded_rectangle([470, YB - 62, 610, YB + 54], radius=14, fill=(214, 218, 230), outline=STEEL, width=4)
    d.rectangle([470, YB + 54, 610, YB + 76], fill=STEEL)

def pend(d, theta, ghost=False):
    x, y = bob_xy(theta)
    if ghost:
        for i in range(0, 18, 2):
            a, b = i / 18, (i + 1) / 18
            d.line([(lerp(PX, x, a), lerp(PY, y, a)), (lerp(PX, x, b), lerp(PY, y, b))], fill=PURPLE, width=4)
        for k in range(0, 360, 30): d.arc([x - RB, y - RB, x + RB, y + RB], k, k + 18, fill=PURPLE, width=5)
        return
    d.line([(PX, PY), (x, y)], fill=NAVY, width=4)
    dot(d, x, y, RB, BOB, BOB_D)
    d.rectangle([x - 4, y + RB - 4, x + 4, y + RB + 16], fill=NAVY)

def bracket(d, hcm, color=INK, alpha=1.0, xb=1000, lab=None):
    """Do cao h: net dut o day + o cho tha, mui ten hai chieu, nhan duoi day (x phai <= 1010 -> mp4 954)."""
    yr = YB - hcm / 100.0 * LPX
    for y in (YB, yr):
        x0 = 640 if y == YB else int(bob_xy(th(hcm))[0]) + RB + 6
        for xx in range(x0, xb + 10, 26): d.line([(xx, y), (xx + 14, y)], fill=A(color, alpha), width=3)
    d.line([(xb, yr + 4), (xb, YB - 4)], fill=A(color, alpha), width=4)
    for y, s in ((yr, 1), (YB, -1)): d.polygon([(xb, y), (xb - 9, y + s * 14), (xb + 9, y + s * 14)], fill=A(color, alpha))
    text(d, (1010, YB + 60), lab or f"{hcm} cm", 58, color, anchor="rm", alpha=alpha)

def timer(d, vtxt, alpha=1.0):
    d.line([(470, YB + 65), (420, YB + 65), (420, 1000)], fill=A(STEEL, alpha), width=4)
    card(d, (60, 1000, 460, 1150), fill=A(NAVY, alpha), r=20)
    text(d, (260, 1040), "v (m/s)", 56, (205, 212, 236), alpha=alpha)
    text(d, (260, 1108), vtxt, 64, (120, 255, 160), alpha=alpha)

def swing(tau, hcm): return th(hcm) * math.cos(2 * math.pi * tau / TP)
def passed(tau): return tau >= TP / 4 - 1e-9

# ---------------- canh 1: du doan ----------------
REL0 = 0.9
def s_hook(img, d, t, sc):
    M = sc["M"]; tau = t - REL0
    theta = th(5) if (tau < 0 or tau >= TP) else swing(tau, 5)
    k = appear(t, M[1] - 0.2, 0.5)
    stand(d); gate(d)
    if k > 0: pend(d, th(20), ghost=True); bracket(d, 20, PURPLE, k)
    else: bracket(d, 5, INK)
    pend(d, theta)
    timer(d, ROWS[0][1] if passed(tau) else "—")
    if k <= 0: return
    y0 = 1190 + (1 - k) * 30
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, k)
    text(d, (W / 2, y0 + 170), "Thả từ 20 cm (cao gấp 4).", 62, INK, alpha=k)
    text(d, (W / 2, y0 + 260), "Tốc độ gấp mấy lần?", 62, PURPLE, alpha=k)
    seg_bar(d, y0 + 350, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: tien hanh + dap an ----------------
STEP, PULL, HOLD = 2.0, 0.45, 0.45
def trial_t0(i): return 0.3 + i * STEP
def state(t):
    i = max([j for j in range(4) if t >= trial_t0(j)], default=-1)
    if i < 0: return 0.0, -1, False
    tt = t - trial_t0(i); h = ROWS[i][0]
    prev = 0.0 if i == 0 else swing(STEP - PULL - HOLD, ROWS[i - 1][0])
    if tt < PULL: return lerp(prev, th(h), ease(tt / PULL)), i, False
    if tt < PULL + HOLD: return th(h), i, False
    tau = tt - PULL - HOLD
    if i == 3 and tau >= TP: return th(h), i, True
    return swing(tau, h), i, passed(tau)
def row_at(i): return trial_t0(i) + PULL + HOLD + TP / 4 + 0.15

def table(d, t, nshow, hl=0.0, cur=-1):
    card(d, (120, 1180, 960, 1640), fill=WHITE, outline=NAVY, w=4)
    xs = (330, 640)
    text(d, (xs[0], 1235), "h (cm)", 58, INK); text(d, (xs[1], 1235), "v (m/s)", 58, INK)
    d.line([(150, 1275), (930, 1275)], fill=LIGHT, width=4)
    for j, (h, v) in enumerate(ROWS):
        a = nshow(j)
        if a <= 0: continue
        y = 1330 + j * 85
        if j in (0, 3) and hl > 0: d.rounded_rectangle([250, y - 36, 760, y + 36], radius=16, fill=A((220, 252, 231), hl))
        elif j == cur and hl <= 0: d.rounded_rectangle([250, y - 36, 760, y + 36], radius=16, fill=A((225, 236, 255), a))
        text(d, (xs[0], y), str(h), 60, BLUE, alpha=a); text(d, (xs[1], y), v, 60, RED, alpha=a)
    if hl > 0:
        xa = 820
        d.line([(xa - 30, 1330), (xa, 1330), (xa, 1585), (xa - 30, 1585)], fill=A(GREEN, hl), width=5)
        d.polygon([(xa - 32, 1585), (xa - 16, 1575), (xa - 16, 1595)], fill=A(GREEN, hl))
        text(d, (xa + 14, 1458), "×2", 60, GREEN, anchor="lm", alpha=hl)
        xb = 225
        d.line([(xb + 22, 1330), (xb, 1330), (xb, 1585), (xb + 22, 1585)], fill=A(BLUE, hl), width=5)
        d.polygon([(xb + 24, 1585), (xb + 8, 1575), (xb + 8, 1595)], fill=A(BLUE, hl))
        text(d, (xb - 12, 1458), "×4", 60, BLUE, anchor="rm", alpha=hl)

def s_do(img, d, t, sc):
    M = sc["M"]; theta, i, ok = state(t)
    stand(d); gate(d)
    if i >= 0: bracket(d, ROWS[i][0], INK)
    pend(d, theta)
    ka = appear(t, M[2] + 0.2, 0.4)
    last = i if ok else i - 1                                      # dong ho giu so doc cu toi lan qua cong ke tiep
    if ka <= 0: timer(d, ROWS[last][1] if last >= 0 else "—")
    else:
        card(d, (60, 1000, 1020, 1150), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), r=28, w=5)
        text(d, (W / 2, 1075), "Đáp án: gấp khoảng 2 lần", 62, GREEN, alpha=ka)
    table(d, t, lambda j: appear(t, row_at(j), 0.3), hl=ka, cur=i)

# ---------------- canh 3: rut ra ----------------
def s_rut(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 230, 1040, 760), fill=WHITE, outline=LIGHT, w=3)
    px, py, L = 260, 270, 330; th0 = th(20)
    theta = th0 * math.cos(2 * math.pi * max(0.0, t - 0.4) / TP)
    bx, by = bob_xy(theta, px, py, L)
    d.rounded_rectangle([150, py - 16, 370, py], radius=6, fill=(150, 155, 172))
    d.line([(px, py), (bx, by)], fill=NAVY, width=4); dot(d, bx, by, 26, BOB, BOB_D)
    fr = (1 - math.cos(theta)) / (1 - math.cos(th0))
    base, hmax = 640, 250
    for cx, f, col, lab in ((585, fr, BLUE, "thế năng"), (895, 1 - fr, ORANGE, "động năng")):
        d.rectangle([cx - 60, base - hmax, cx + 60, base], outline=LIGHT, width=3)
        d.rectangle([cx - 60, base - hmax * f, cx + 60, base], fill=col)
        text(d, (cx, base + 62), lab, 56, col)
    ka = appear(t, 1.6, 0.45)
    if ka > 0:
        card(d, (440, 290, 1030, 370), fill=A((239, 246, 255), ka), r=20)
        text(d, (735, 330), "thế năng ≈ động năng", 56, INK, alpha=ka)
    kb = appear(t, M[1] - 0.1, 0.4)
    if kb > 0:
        card(d, (40, 800, 1040, 1300), fill=A(WHITE, kb), outline=A(LIGHT, kb), w=3)
        text(d, (W / 2, 860), "động năng : thế năng", 56, INK, alpha=kb)
        x0, x1 = 230, 860
        for j, ((h, _), p) in enumerate(zip(ROWS, PCT)):
            y = 950 + j * 85; g = ease((t - M[1]) / 0.6)
            text(d, (205, y), f"{h} cm", 56, INK, anchor="rm", alpha=kb)
            d.rectangle([x0, y - 32, x1, y + 32], fill=A((240, 236, 228), kb))
            if g > 0:
                d.rectangle([x0, y - 32, x0 + (x1 - x0) * p / 100 * g, y + 32], fill=ORANGE)
                text(d, (x0 + 20, y), fm(p) + " %", 56, WHITE, anchor="lm", alpha=clamp(g * 2 - 1))
        for yy in range(905, 1240, 24): d.line([(x1, yy), (x1, yy + 12)], fill=A(GREEN, kb), width=6)
        text(d, (x1 + 10, 1235), "100 %", 56, GREEN, anchor="lm", alpha=kb)
    kc = appear(t, M[1] + 2.6, 0.4)
    if kc > 0:
        card(d, (40, 1340, 1040, 1480), fill=A((254, 242, 242), kc), outline=A(RED, kc), w=4)
        text(d, (W / 2, 1410), "Thiếu 3–4 %: lực cản, ma sát", 58, RED, alpha=kc)

# ---------------- canh 4: bay + gioi han ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; mk = M[1]
    px, py, L = 540, 250, 560; th0 = math.radians(34)
    th1 = th0 * math.cos(2 * math.pi * t / 2.4)                  # con lac lac that: T va v quay theo
    for i in range(-36, 37, 4):
        a1, a2 = math.radians(i), math.radians(i + 2)
        d.line([bob_xy(a1, px, py, L), bob_xy(a2, px, py, L)], fill=(200, 194, 180), width=4)
    d.rounded_rectangle([px - 120, py - 18, px + 120, py], radius=6, fill=(150, 155, 172))
    bx, by = bob_xy(th1, px, py, L)
    d.line([(px, py), (bx, by)], fill=NAVY, width=4)
    w_ = -math.sin(2 * math.pi * t / 2.4); sg = 1 if w_ >= 0 else -1   # chieu chuyen dong hien tai
    ut = (-math.sin(th1), -math.cos(th1)); uv = (sg * math.cos(th1), -sg * math.sin(th1))
    arrow(d, (bx, by), (bx + 190 * ut[0], by + 190 * ut[1]), PURPLE, w=8, head=26)
    tx, ty = bx + 120 * ut[0] - 55 * uv[0], by + 120 * ut[1] - 55 * uv[1]
    arrow(d, (bx, by), (bx + 190 * uv[0], by + 190 * uv[1]), BLUE, w=8, head=26)
    s = 34
    p1 = (bx + s * ut[0], by + s * ut[1]); p3 = (bx + s * uv[0], by + s * uv[1]); p2 = (p1[0] + s * uv[0], p1[1] + s * uv[1])
    d.line([p1, p2, p3], fill=INK, width=5)
    dot(d, bx, by, 30, BOB, BOB_D)
    card(d, (50, 280, 400, 450), fill=WHITE, outline=LIGHT, w=3)
    arrow(d, (75, 325), (140, 325), PURPLE, w=8, head=20); text(d, (160, 325), "T lực căng", 56, PURPLE, anchor="lm")
    arrow(d, (75, 405), (140, 405), BLUE, w=8, head=20); text(d, (160, 405), "v vận tốc", 56, BLUE, anchor="lm")
    k3 = appear(t, M[2] - 0.1, 0.45); a1 = 1 - k3; y = 1000
    if a1 > 0:
        card(d, (40, y, 1040, y + 420), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pill(d, W / 2, y + 70, "BẪY", RED, a1)
        q = "“Lực căng làm mất cơ năng”"
        ks = clamp((t - mk) / 0.4); lw = tw(d, q, F(62)); yy = y + 190
        text(d, (W / 2, yy), q, 62, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
        k2 = appear(t, mk + 0.2, 0.45)
        if k2 > 0: text(d, (W / 2, y + 320), "T không sinh công", 62, DORANGE, alpha=a1 * k2)
    if k3 > 0:
        card(d, (40, y, 1040, y + 330), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, y + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, y + 210), "Mới một quả nặng", 62, INK, alpha=k3)

# ---------------- canh 5: thu nghi (cau chot o khung: 1,26 m/s) ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1620), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 310, "THỬ NGHĨ", ORANGE, k)
    px, py, L = 540, 420, 400; th0 = th(18)
    theta = th0 * math.cos(2 * math.pi * max(0.0, t - 0.6) / TP)
    bx, by = bob_xy(theta, px, py, L)
    d.rounded_rectangle([px - 130, py - 18, px + 130, py], radius=6, fill=(150, 155, 172))
    d.line([(px, py), (bx, by)], fill=NAVY, width=4); dot(d, bx, by, 28, BOB, BOB_D)
    text(d, (W / 2, 980), "Thả từ 18 cm, bỏ qua cản,", 62, INK, alpha=k)
    text(d, (W / 2, 1070), "g = 10 m/s².", 62, INK, alpha=k)
    text(d, (W / 2, 1190), "Lúc cao 10 cm so cổng,", 64, DORANGE, alpha=k)
    text(d, (W / 2, 1280), "tốc độ bao nhiêu?", 64, DORANGE, alpha=k)
    seg_bar(d, 1420, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    return [(h["t0"] + REL0, "tap"), (h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.05, "ding"),
            (do["t0"] + do["M"][2] + 0.2, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"),
            (b["t0"] + b["M"][1], "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"), (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l10-co-nang-bao-toan-01", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Cơ năng và bảo toàn cơ năng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Con lắc qua cổng quang", draw=s_hook, tail=0.3, caps=[
   ("Thả từ 5 cm, đọc tốc độ.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Thả từ bốn độ cao", draw=s_do, tail=0.4, caps=[
   ("Kéo lên, thả nhẹ, không đẩy.", 3.6),
   ("Mỗi lần ghi một hàng.", 3.8),
   ("So hàng 5 cm với 20 cm.", 3.4)]),
 dict(key="rut", title="Thế năng thành động năng", draw=s_rut, tail=0.6, caps=[
   ("Xuống thấp, nhanh dần.", 4.0),
   ("Cả bốn lần dưới 100 %.", 4.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Đúng không?", 3.2),
   ("Sai: T vuông góc với v.", 3.4),
   ("Giới hạn của lần đo.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng lại, tự tính.", 6.4)]),
])
