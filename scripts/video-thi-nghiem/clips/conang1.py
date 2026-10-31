# Clip: tn-l10-co-nang-bao-toan-01 - Con lac qua cong quang: the nang thanh dong nang (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-co-nang-bao-toan-01.json:
#   so_lieu_mau: h (cm) 5 / 10 / 15 / 20 ; v do (m/s) 0,98 / 1,39 / 1,70 / 1,97 ; v^2/(2gh) 96,0 / 96,6 / 96,3 / 97,0 %
#   tham_so: g = 10 m/s2; day ~1 m (dung_cu) -> chu ki ve ~2 s; rut_ra: thieu 3-4 % do luc can, ma sat diem treo.
# Canh: Du doan (5 cm -> 0,98; keo len 20 cm thi toc do gap may lan? chi cau hoi + hinh, K10)
#       -> Tien hanh (4 lan tha, so cong quang chi hien khi qua nang da qua cong, bang ghi tung hang) + DAP AN · gap khoang 2 lan
#       -> Rut ra (the nang <-> dong nang, cot v^2/(2gh) dung ti le 0-100 %, thieu 3-4 %) + chua noi duoc (1 qua nang)
#       -> Bay (luc cang lam mat co nang? T vuong goc v) -> Chot + cau hoi: nhanh gap 3 lan luc 5 cm thi keo cao bao nhieu
#          (45 cm, chua hien; phan xa sai 15 cm -> goi y doi chieu hang 15 cm = 1,70 m/s).
from engine import *

ROWS = [(5, "0,98"), (10, "1,39"), (15, "1,70"), (20, "1,97")]     # so_lieu_mau: h (cm), v do (m/s)
PCT = [96.0, 96.6, 96.3, 97.0]                                     # so_lieu_mau: v^2/(2gh) (%)
def fm(x, n=1): return f"{x:.{n}f}".replace(".", ",")

STEEL = (120, 128, 150); BOB = (70, 90, 160); BOB_D = (40, 52, 110)
TP = 2.0                       # chu ki ve (day 1 m, g = 10 -> 1,99 s)

# ---------------- con lac + cong quang + dong ho ----------------
PX, PY, LPX = 540, 290, 620    # diem treo, chieu dai day (px) ung voi 1 m
YB = PY + LPX                  # tam qua nang o vi tri thap nhat (y 910)
RB = 34

def th(hcm):                   # goc lech ung voi do cao h (cm), day 1 m
    return math.acos(1 - hcm / 100.0)

def bob_xy(theta, px=PX, py=PY, L=LPX):
    return px + L * math.sin(theta), py + L * math.cos(theta)

def stand(d):
    d.rounded_rectangle([330, PY - 24, 750, PY], radius=8, fill=(150, 155, 172))
    d.polygon([(PX - 18, PY), (PX + 18, PY), (PX, PY + 16)], fill=NAVY)

def gate(d):
    d.rounded_rectangle([470, YB - 62, 610, YB + 54], radius=14, fill=(214, 218, 230), outline=STEEL, width=4)
    d.rectangle([470, YB + 54, 610, YB + 76], fill=STEEL)
    text(d, (W / 2, YB + 106), "cổng quang", 40, MUTED)

def pend(d, theta, ghost=False):
    x, y = bob_xy(theta)
    if ghost:
        n = 18
        for i in range(0, n, 2):
            a, b = i / n, (i + 1) / n
            d.line([(lerp(PX, x, a), lerp(PY, y, a)), (lerp(PX, x, b), lerp(PY, y, b))], fill=PURPLE, width=4)
        for k in range(0, 360, 30):
            d.arc([x - RB, y - RB, x + RB, y + RB], k, k + 18, fill=PURPLE, width=5)
        return
    d.line([(PX, PY), (x, y)], fill=NAVY, width=4)
    dot(d, x, y, RB, BOB, BOB_D)
    d.rectangle([x - 4, y + RB - 4, x + 4, y + RB + 16], fill=NAVY)         # tam chan sang nho

def bracket(d, hcm, color=INK, alpha=1.0, xb=1000, lab=None):
    """Do cao h: net dut o day + o cho tha, mui ten hai chieu, nhan ben duoi (khong de day)."""
    yr = YB - hcm / 100.0 * LPX
    for y in (YB, yr):
        for xx in range(640 if y == YB else int(bob_xy(th(hcm))[0]) + RB + 6, xb + 10, 26):
            d.line([(xx, y), (xx + 14, y)], fill=A(color, alpha), width=3)
    d.line([(xb, yr + 4), (xb, YB - 4)], fill=A(color, alpha), width=4)
    for y, s in ((yr, 1), (YB, -1)):
        d.polygon([(xb, y), (xb - 9, y + s * 14), (xb + 9, y + s * 14)], fill=A(color, alpha))
    text(d, (xb + 10, YB + 44), lab or f"h = {hcm} cm", 40, color, anchor="rm", alpha=alpha)

def timer(d, vtxt, alpha=1.0, head="v (m/s)"):
    d.line([(470, YB + 65), (400, YB + 65), (400, 1060), (380, 1060)], fill=A(STEEL, alpha), width=4)
    card(d, (40, 1000, 380, 1130), fill=A(NAVY, alpha), r=20)
    text(d, (210, 1036), head, 38, (190, 200, 228), alpha=alpha)
    text(d, (210, 1090), vtxt, 56, (120, 255, 160), alpha=alpha)

def swing(tau, hcm, decay=0.0):
    """Goc con lac tau giay sau khi tha tu h (cm), khong van toc dau. Qua cong (theta = 0) lan dau o tau = TP/4."""
    return th(hcm) * math.cos(2 * math.pi * tau / TP) * math.exp(-decay * tau)

def passed(tau): return tau >= TP / 4 - 1e-9

# ---------------- canh 1: du doan ----------------
REL0 = 1.0                     # giay tha qua nang o canh hook; lac mot chu ki roi tay giu lai o 5 cm (cung phia bong 20 cm)
def hook_theta(t):
    tau = t - REL0
    return th(5) if (tau < 0 or tau >= TP) else swing(tau, 5)

def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; k = appear(t, M[1] - 0.4, 0.5)
    stand(d); gate(d)
    tau = t - REL0
    if k > 0: pend(d, th(20), ghost=True); bracket(d, 20, PURPLE, k, lab="kéo lên: 20 cm")
    else: bracket(d, 5, INK)
    pend(d, hook_theta(t))
    timer(d, ROWS[0][1] if passed(tau) else "—", head="thả 5 cm · m/s" if k > 0 else "v (m/s)")
    if k <= 0: return
    y0 = 1170 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 420), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "Dự đoán", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, k), r=32)
    text(d, (W / 2, y0 + 58), "Dự đoán", 40, WHITE, alpha=k)
    ctext(d, y0 + 160, "Kéo lên 20 cm, cao gấp 4.", 46, INK, maxw=880, alpha=k)
    ctext(d, y0 + 240, "Tốc độ qua cổng gấp mấy lần?", 46, INK, maxw=880, alpha=k)
    t1, t2 = M[1] - 0.2, sc["T"] - 0.2; q = clamp((t - t1) / (t2 - t1))           # thanh dem thoi gian nghi
    d.rounded_rectangle([200, y0 + 340, 880, y0 + 356], radius=8, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([200, y0 + 340, 200 + 680 * (1 - q), y0 + 356], radius=8, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh ----------------
STEP = 1.9                     # moi lan: keo 0,45 s, dung yen dung vach h 0,45 s, tha (qua cong sau 0,5 s), lac tiep
PULL, HOLD = 0.45, 0.45
def trial_t0(i, sc): return 0.3 + i * STEP

def state(t, sc):
    """(goc, chi so lan dang do, da qua cong chua) - so cong quang va hang bang theo cung ham nay."""
    i = max([j for j in range(4) if t >= trial_t0(j, sc)], default=-1)
    if i < 0: return 0.0, -1, False
    tt = t - trial_t0(i, sc); h = ROWS[i][0]
    if i == 0: prev = 0.0
    else: prev = swing(STEP - PULL - HOLD, ROWS[i - 1][0])     # goc luc tay bat lai qua truoc
    if tt < PULL: return lerp(prev, th(h), ease(tt / PULL)), i, False
    if tt < PULL + HOLD: return th(h), i, False
    tau = tt - PULL - HOLD
    if i == 3 and tau >= TP: return th(h), i, True             # lan cuoi: lac ve lai dung 20 cm, tay giu
    return swing(tau, h), i, passed(tau)

def row_at(i, sc): return trial_t0(i, sc) + PULL + HOLD + TP / 4 + 0.15

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; theta, i, ok = state(t, sc)
    stand(d); gate(d)
    if i >= 0: bracket(d, ROWS[i][0], INK)
    pend(d, theta)
    ka = appear(t, M[1], 0.4)
    if ka <= 0: timer(d, ROWS[i][1] if (i >= 0 and ok) else "—")
    else:
        card(d, (100, 1048, 980, 1148), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), r=28, w=5)
        text(d, (W / 2, 1098), "ĐÁP ÁN · gấp khoảng 2 lần", 44, GREEN, alpha=ka)
    card(d, (120, 1165, 960, 1595), fill=WHITE, outline=NAVY, w=4)
    xs = (330, 620)
    text(d, (xs[0], 1215), "h (cm)", 42, INK); text(d, (xs[1], 1215), "v (m/s)", 42, INK)
    d.line([(150, 1250), (930, 1250)], fill=LIGHT, width=4)
    for j, (h, v) in enumerate(ROWS):
        a = appear(t, row_at(j, sc), 0.3); y = 1300 + j * 80
        if a <= 0: continue
        hl = (j in (0, 3)) and ka > 0
        if hl: d.rounded_rectangle([270, y - 32, 720, y + 32], radius=16, fill=A((220, 252, 231), ka))
        elif j == i and not ka: d.rounded_rectangle([270, y - 32, 720, y + 32], radius=16, fill=A((225, 236, 255), a))
        text(d, (xs[0], y), str(h), 44, BLUE, alpha=a); text(d, (xs[1], y), v, 44, RED, alpha=a)
    if ka > 0:                                  # 0,98 -> 1,97: mui ten noi hang 1 va hang 4
        xa = 800
        d.line([(xa - 30, 1300), (xa, 1300), (xa, 1540), (xa - 30, 1540)], fill=A(GREEN, ka), width=5)
        d.polygon([(xa - 32, 1540), (xa - 16, 1530), (xa - 16, 1550)], fill=A(GREEN, ka))
        text(d, (xa + 18, 1420), "×2", 48, GREEN, anchor="lm", alpha=ka)
        xb = 245                                # 5 -> 20 cm: mui ten noi cot h
        d.line([(xb + 22, 1300), (xb, 1300), (xb, 1540), (xb + 22, 1540)], fill=A(BLUE, ka), width=5)
        d.polygon([(xb + 24, 1540), (xb + 8, 1530), (xb + 8, 1550)], fill=A(BLUE, ka))
        text(d, (xb - 14, 1420), "×4", 48, BLUE, anchor="rm", alpha=ka)

# ---------------- canh 3: rut ra ----------------
def s_rut(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    # (a) the nang <-> dong nang: con lac nho + hai cot (khong so)
    card(d, (40, 262, 1040, 740), fill=WHITE, outline=LIGHT, w=3)
    px, py, L = 280, 300, 330; th0 = th(20)
    theta = th0 * math.cos(2 * math.pi * max(0.0, t - 0.4) / TP)
    bx, by = bob_xy(theta, px, py, L)
    d.rounded_rectangle([170, py - 16, 390, py], radius=6, fill=(150, 155, 172))
    d.line([(px, py), (bx, by)], fill=NAVY, width=4); dot(d, bx, by, 24, BOB, BOB_D)
    d.line([(px - 30, py + L + 26), (px + 30, py + L + 26)], fill=STEEL, width=4)
    fr = (1 - math.cos(theta)) / (1 - math.cos(th0))          # phan the nang so voi luc tha
    base, hmax = 640, 260
    for cx, f, col, lab in ((640, fr, BLUE, "thế năng"), (860, 1 - fr, ORANGE, "động năng")):
        d.rectangle([cx - 60, base - hmax, cx + 60, base], outline=LIGHT, width=3)
        d.rectangle([cx - 60, base - hmax * f, cx + 60, base], fill=col)
        text(d, (cx, base + 40), lab, 40, col)
    ka = appear(t, M[0] + 1.2, 0.5)
    text(d, (750, 330), "mgh ≈ ½mv²", 46, INK, alpha=ka)
    # (b) v^2/(2gh) dung ti le 0-100 %
    kb = appear(t, M[0] + 2.2, 0.4)
    if kb > 0:
        card(d, (40, 770, 1040, 1260), fill=A(WHITE, kb), outline=A(LIGHT, kb), w=3)
        text(d, (W / 2, 820), "½mv² ở đáy so với mgh lúc thả", 42, INK, alpha=kb)
        x0, x1 = 230, 850
        for j, ((h, _), p) in enumerate(zip(ROWS, PCT)):
            y = 900 + j * 75; g = ease((t - M[0] - 2.4 - j * 0.2) / 0.5)
            text(d, (200, y), f"{h} cm", 40, INK, anchor="rm", alpha=kb)
            d.rectangle([x0, y - 24, x1, y + 24], fill=A((240, 236, 228), kb))
            if g > 0:
                d.rectangle([x0, y - 24, x0 + (x1 - x0) * p / 100 * g, y + 24], fill=ORANGE)
                text(d, (x0 + 20, y), fm(p) + " %", 40, WHITE, anchor="lm", alpha=clamp(g * 2 - 1))
        for yy in range(860, 1140, 24): d.line([(x1, yy), (x1, yy + 12)], fill=A(GREEN, kb), width=5)
        text(d, (x1 + 16, 900), "100 %", 40, GREEN, anchor="lm", alpha=kb)
        kc = appear(t, M[1] + 1.8, 0.4)
        ctext(d, 1205, "Thiếu 3–4 %: lực cản, ma sát ở điểm treo", 40, RED, maxw=920, alpha=kc)
    # (c) chua noi duoc gi
    k3 = appear(t, M[2] - 0.1, 0.45)
    if k3 > 0:
        y1 = 1290 + (1 - k3) * 20
        card(d, (40, y1, 1040, y1 + 300), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y1 + 55), "Chưa nói được gì?", 44, NAVY, alpha=k3)
        card(d, (100, y1 + 105, 980, y1 + 270), fill=A((239, 246, 255), k3), r=24)
        ctext(d, y1 + 150, "Chỉ dùng một quả nặng:", 42, INK, alpha=k3)
        ctext(d, y1 + 225, "chưa đo v theo khối lượng", 42, BLUE, alpha=k3)

# ---------------- canh 4: bay ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.1, 0.4); y0 = 270
    card(d, (60, y0, 1020, y0 + 330), fill=A(WHITE, a), outline=A(RED, a), w=6)
    pw = tw(d, "Bẫy", F(40)) + 60
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(RED, a), r=32)
    text(d, (W / 2, y0 + 58), "Bẫy", 40, WHITE, alpha=a)
    q = "Lực căng T sinh công âm"; f = F(46); lw = tw(d, q, f); yy = y0 + 180
    ks = clamp((t - 1.0) / 0.4)
    text(d, (W / 2, yy), q, 46, mix(INK, MUTED, ks), alpha=a)
    if ks > 0: d.line([(W / 2 - lw / 2 - 8, yy + 2), (W / 2 - lw / 2 - 8 + (lw + 16) * ks, yy + 2)], fill=A(RED, 0.85 * a), width=6)
    k2 = appear(t, 1.5, 0.45)
    text(d, (W / 2, y0 + 270), "Sai: lực căng không sinh công", 44, GREEN, alpha=a * k2)
    # hinh: con lac dang di xuong, T huong ve diem treo, v tiep tuyen, P thang dung
    px, py, L = 540, 680, 520; th1 = math.radians(28)
    for i in range(-40, 41, 4):                               # quy dao (net dut)
        a1, a2 = math.radians(i), math.radians(i + 2)
        d.line([bob_xy(a1, px, py, L), bob_xy(a2, px, py, L)], fill=(200, 194, 180), width=4)
    d.rounded_rectangle([px - 120, py - 18, px + 120, py], radius=6, fill=(150, 155, 172))
    bx, by = bob_xy(th1, px, py, L)
    d.line([(px, py), (bx, by)], fill=NAVY, width=4)
    ut = (-math.sin(th1), -math.cos(th1)); uv = (-math.cos(th1), math.sin(th1))
    kf = appear(t, 0.3, 0.4)
    if kf > 0:
        arrow(d, (bx, by), (bx + 200 * ut[0], by + 200 * ut[1]), A(PURPLE, kf), w=7, head=24)
        text(d, (bx + 200 * ut[0] + 40, by + 200 * ut[1] + 10), "T", 48, PURPLE, alpha=kf)
        arrow(d, (bx, by), (bx + 210 * uv[0], by + 210 * uv[1]), A(BLUE, kf), w=7, head=24)
        text(d, (bx + 210 * uv[0] - 10, by + 210 * uv[1] + 46), "v", 48, BLUE, alpha=kf)
        arrow(d, (bx, by), (bx, by + 190), A(INK, kf), w=7, head=24)
        text(d, (bx + 36, by + 170), "P", 48, INK, alpha=kf)
        s = 30                                                   # dau goc vuong T-v
        p1 = (bx + s * ut[0], by + s * ut[1]); p3 = (bx + s * uv[0], by + s * uv[1])
        p2 = (p1[0] + s * uv[0], p1[1] + s * uv[1])
        d.line([p1, p2, p3], fill=A(INK, kf), width=4)
    dot(d, bx, by, 30, BOB, BOB_D)
    k4 = appear(t, M[1] - 0.1, 0.45)
    if k4 > 0:
        card(d, (60, 1380, 1020, 1580), fill=A((220, 252, 231), k4), outline=A(GREEN, k4), w=5)
        ctext(d, 1440, "T vuông góc với v", 46, PURPLE, alpha=k4)
        ctext(d, 1520, "→ công của T bằng 0", 44, INK, alpha=k4)

# ---------------- canh 5: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    # nhu chot_hoi() cua engine nhung o THU NGHI thu vua noi dung (cau hoi 2 dong + goi y)
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 410, "Thế năng đầu ≈ động năng đáy", 52, GREEN, maxw=860, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 620, 1040, 1250), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 682), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 840, "Muốn v gấp 3 lần lúc thả 5 cm, kéo lên cao bao nhiêu?", 46, INK, maxw=880, alpha=appear(t, M[0] + 0.4, 0.5))
    kh = appear(t, M[0] + 2.5, 0.5)                                 # goi y hien tre ~2,5 s
    if kh > 0:
        card(d, (110, 1000, 970, 1200), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1050, "Gợi ý", 38, MUTED, alpha=kh)
        ctext(d, 1130, "15 cm chỉ được 1,70 m/s", 46, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + do["M"][1], "ding"), (r["t0"] + r["M"][2] - 0.1, "tap"),
            (b["t0"] + 1.0, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-co-nang-bao-toan-01", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Cơ năng và bảo toàn cơ năng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Con lắc qua cổng quang", draw=s_hook, tail=0.6, caps=[
   ("Thả từ 5 cm, đọc tốc độ.", 3.4),
   ("Dừng video, tự đoán.", 4.4)]),
 dict(key="do", title="Thả từ bốn độ cao", draw=s_do, tail=0.6, caps=[
   ("Kéo lên, thả nhẹ, không đẩy.", 7.4),
   ("Cao gấp 4, nhanh gấp 2.", 3.4)]),
 dict(key="rut", title="Thế năng thành động năng", draw=s_rut, tail=0.6, caps=[
   ("Xuống thấp: thế năng thành động năng.", 3.8),
   ("Lần nào cũng thiếu một chút.", 3.8),
   ("Giới hạn của thí nghiệm.", 5.1)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.6, caps=[
   ("Nhiều bạn nghĩ dây làm mất cơ năng.", 3.0),
   ("Dây chỉ đổi hướng chuyển động.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 5.6)]),
])
