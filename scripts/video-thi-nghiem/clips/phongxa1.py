# Clip: tn-l12-phongxa-01 - Nhip dem cua mot nguon phong xa: trung binh on dinh, tung phut ngau nhien (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-phongxa-01.json:
#   so_lieu_mau: 5 lan dem 1 phut = 512, 486, 531, 497, 505; phong nen 23 (ghi_chu: trung binh 506,2; tru phong con 483).
#   rut_ra: mot lan dem tan mat co +-20 xung/phut, trung binh 5 lan co +-10. ket_qua_ky_vong: 486-531, khoang +-4 %.
#   tham_so: d = 10 cm, t_dem = 60 s. khong_chung_minh: 5 phut qua ngan de thay giam; chua biet tia alpha, beta hay gamma.
# Khac phongxa2 (chu ki ban ra, bay = ti so khi chua tru phong): clip nay la bay T7 "quen tru phong -> tuong nguon manh hon".
# Du doan (khung ben canh, K10 khong ve nut; nguon khong doi, dem 5 lan x 1 phut, nam so dem se the nao?):
#   A. Bang nhau, vi nguon khong doi (hien_tuong_hay_sai #1)
#   B. Giam dan deu qua 5 lan (nham "nguon yeu dan" trong 5 phut; khong_chung_minh #1)
#   C. Khac nhau, dao dong quanh mot gia tri  <- dung
# Cau chot (ca moi, khong trung Du doan): dem moi lan 4 phut (t_dem trong khoang 30-300 s cua tham_so) -> do lech tuong doi
#   NHO hon (sai so tuong doi 1/sqrt(N), sai_so_thuong_gap #1 "muon giam phai dem lau hon"); man hinh khong ghi y nay.
# Dung lai 26/11/2026 (viec 4 lo 32): cong --do-chu, chu >= 56 px khi ve, <= 50 s; bo goi y 'sqrt(N), N ~ 2000' o canh chot
#   (lo dap an). Cau chot: N = 4 x 506 ~ 2000 -> sqrt(N) ~ 45 -> ~2,2 % (CA TU SUY tu rut_ra 1/sqrt(N)), nho hon 4 %.
import random
from engine import *

COUNTS = [512, 486, 531, 497, 505]      # so_lieu_mau
PHONG, MEAN, NET = 23, 506, 483         # so_lieu_mau (phong) + ghi_chu (506,2 -> 506; 483)
NOTE = (70, 75, 95)

# ---------------- dung cu: may dem + dong ho + nguon, ong dem tren ban ----------------
SX, SY = 300, 740          # tam nguon khi dat truoc ong
TX0, TX1, TY = 500, 900, 740
BOX = (110, 790)           # hop chi tren ban (goc trai)
RP = random.Random(5)
RAYS = [(RP.random(), RP.uniform(-1, 1)) for _ in range(16)]

DORANGE = (154, 52, 18)

def pill(d, cx, cy, s, fill, alpha=1.0, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 38, cx + pw / 2, cy + 38), fill=A(fill, alpha), r=36)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (190, y, 890, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (190, y, 190 + max(70, 700 * q), y + 70), fill=A(col, a), r=35)

def source(d, x, y, a=1.0):
    d.rounded_rectangle([x - 34, y - 34, x + 34, y + 34], radius=12, fill=A(YELLOW, a), outline=A(NAVY, a), width=5)
    for k in range(3):
        g = 90 + 120 * k
        d.pieslice([x - 24, y - 24, x + 24, y + 24], g - 30, g + 30, fill=A(NAVY, a))
    dot(d, x, y, 6, A(YELLOW, a))

def stopwatch(d, cx, cy, sec, run, r=92):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=NAVY, width=6)
    d.rectangle([cx - 14, cy - r - 24, cx + 14, cy - r], fill=NAVY)
    for k in range(12):
        a = math.radians(k * 30 - 90); L = 18 if k % 3 == 0 else 9
        d.line([(cx + (r - 6) * math.cos(a), cy + (r - 6) * math.sin(a)),
                (cx + (r - 6 - L) * math.cos(a), cy + (r - 6 - L) * math.sin(a))], fill=NAVY, width=4)
    a = math.radians(sec / 60 * 360 - 90)
    if sec > 0: d.pieslice([cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10], -90, sec / 60 * 360 - 90, fill=A(ORANGE, 0.22))
    d.line([(cx, cy), (cx + (r - 22) * math.cos(a), cy + (r - 22) * math.sin(a))], fill=RED if run else NAVY, width=6)
    dot(d, cx, cy, 8, NAVY)

def rig(d, t, reading, sub, sec=0.0, run=False, src=0.0):
    card(d, (60, 270, 650, 580), fill=WHITE, outline=LIGHT, r=28, w=4)
    d.rounded_rectangle([110, 330, 600, 460], radius=16, fill=NAVY)
    text(d, (355, 395), str(reading), 76, (134, 239, 172))
    if sub: text(d, (355, 520), sub, 56, NOTE)
    card(d, (690, 270, 1020, 580), fill=WHITE, outline=LIGHT, r=28, w=4)
    stopwatch(d, 855, 440, sec, run)
    d.line([(90, 900), (990, 900)], fill=NAVY, width=6)
    mx = (TX0 + TX1) / 2
    d.rectangle([mx - 8, TY + 40, mx + 8, 896], fill=GRAY); d.rectangle([mx - 70, 882, mx + 70, 898], fill=NAVY)
    d.rounded_rectangle([TX0, TY - 44, TX1, TY + 44], radius=40, fill=(214, 220, 232), outline=NAVY, width=5)
    d.rectangle([TX0 - 6, TY - 38, TX0 + 14, TY + 38], fill=(70, 78, 100))
    text(d, (mx + 10, TY), "ống đếm", 56, NAVY)
    d.line([(TX1, TY), (960, TY), (960, 590)], fill=GRAY, width=12, joint="curve")
    bx, by = BOX
    if src > 0:
        d.rectangle([bx - 70, by, bx + 70, 896], fill=(110, 115, 128), outline=NAVY, width=4)
        text(d, (bx + 20, 960), "hộp chì", 56, NOTE)
    k = ease(src)
    x = lerp(SX, bx, k); y = lerp(SY, by + 52, k) if k < 1 else by + 52
    if k < 0.98:
        if k < 0.05: d.rectangle([x - 8, y + 34, x + 8, 896], fill=GRAY)
        source(d, x, y)
    if src <= 0:
        for xx in (SX, TX0): d.line([(xx, 640), (xx, 670)], fill=NOTE, width=4)
        arrow(d, (SX + 4, 655), (TX0 - 4, 655), NOTE, w=4, head=14); arrow(d, (TX0 - 4, 655), (SX + 4, 655), NOTE, w=4, head=14)
        text(d, ((SX + TX0) / 2, 610), "10 cm", 56, NOTE)
        text(d, (SX, 960), "nguồn", 56, NOTE)
        if run:
            for ph, dy in RAYS:
                q = (ph + t * 1.7) % 1
                dot(d, lerp(SX + 40, TX0, q), SY + dy * 30 * q, 7, ORANGE)

BX = [290, 410, 530, 650, 770, 910]
def bar_chart(d, box, vals, alphas, mean_k=0.0, labels=True):
    x0b, y0b, x1b, y1b = box
    card(d, box, fill=WHITE, outline=LIGHT, w=3)
    yb, yt = y1b - 100, y0b + 110
    Y = lambda n: yb - n / 600 * (yb - yt)
    text(d, (x0b + 40, y0b + 50), "xung/phút", 56, NOTE, anchor="lm")
    for n in (200, 400, 600): d.line([(210, Y(n)), (x1b - 30, Y(n))], fill=(240, 236, 228), width=2)
    d.line([(210, yb), (x1b - 30, yb)], fill=NAVY, width=5); d.line([(210, yb), (210, yt - 20)], fill=NAVY, width=5)
    for n in (0, 200, 400, 600): text(d, (190, Y(n)), str(n), 56, NOTE, anchor="rm")
    labs = ["1", "2", "3", "4", "5", "phông"]
    for i, (v, a) in enumerate(zip(vals, alphas)):
        x = BX[i]
        if v is None: continue
        text(d, (x, yb + 50), labs[i], 56, PURPLE if i == 5 else NOTE)
        if a <= 0: continue
        col = PURPLE if i == 5 else BLUE
        top = yb - (yb - Y(v)) * ease(a)
        if yb - top > 2: d.rectangle([x - 44, top, x + 44, yb], fill=col)
        if labels: text(d, (x, top - 36), str(v), 56, INK, alpha=clamp(a * 2 - 1))
    if mean_k > 0:
        y = Y(MEAN)
        for xx in range(210, x1b - 40, 26): d.line([(xx, y), (min(xx + 14, x1b - 40), y)], fill=A(GREEN, mean_k), width=6)
    return Y

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, t, "?", "")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 66, "DỰ ĐOÁN", PURPLE, a)
    seg_bar(d, y0 + 130, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, a)
    text(d, (W / 2, y0 + 300), "Đếm 5 lần, mỗi lần 1 phút.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 405), "Năm số đếm sẽ thế nào?", 62, PURPLE, alpha=a)

# ---------------- canh 2: dem 5 lan, roi do phong ----------------
SWEEP = 0.8
def count_at(i, sc):
    M = sc["M"]
    return M[0] + 0.25 + i * 1.0 if i < 5 else M[1] + 0.9

def do_state(t, sc):
    M = sc["M"]; src = clamp((t - M[1] - 0.1) / 0.6)
    n = 0; reading, sec, run = "?", 0.0, False
    for i in range(6):
        s = count_at(i, sc)
        if t < s: break
        if t < s + SWEEP: reading, sec, run = "···", 60 * (t - s) / SWEEP, True
        else: n = i + 1; reading = (COUNTS + [PHONG])[i]; sec, run = 60, False
    if n == 5 and t >= M[1] and t < count_at(5, sc): reading, sec, run = COUNTS[4], 60, False
    return reading, sec, run, src, n

def s_do(img, d, t, sc):
    reading, sec, run, src, n = do_state(t, sc)
    rig(d, t, reading, "xung/phút", sec, run, src)
    bar_chart(d, (40, 1010, 1040, 1600), COUNTS + [PHONG],
              [appear(t, count_at(i, sc) + SWEEP, 0.35) if i < n else 0 for i in range(6)])

# ---------------- canh 3: Dap an (phong to quanh 506) ----------------
ZX0, ZX1, ZV0, ZV1 = 150, 930, 470, 540
def Xz(v): return ZX0 + (v - ZV0) / (ZV1 - ZV0) * (ZX1 - ZX0)

def s_ans(img, d, t, sc):
    M = sc["M"]
    pill(d, W / 2, 290, "ĐÁP ÁN: khác nhau", NAVY)
    Y = bar_chart(d, (40, 360, 1040, 930), COUNTS + [None], [1] * 5 + [0], mean_k=1.0, labels=False)
    text(d, (1010, Y(MEAN) - 40), "≈ 506", 56, GREEN, anchor="rm")
    kz = appear(t, 1.8, 0.45)
    if kz <= 0: return
    card(d, (40, 960, 1040, 1600), fill=A(WHITE, kz), outline=A(LIGHT, kz), w=3)
    yl = 1100
    d.line([(ZX0 - 20, yl), (ZX1 + 20, yl)], fill=A(NAVY, kz), width=5)
    for yy in range(yl - 30, yl + 30, 14): d.line([(Xz(MEAN), yy), (Xz(MEAN), yy + 7)], fill=A(GREEN, kz), width=4)
    up = {486: True, 497: False, 505: True, 512: False, 531: True}
    for v in COUNTS:
        dot(d, Xz(v), yl, 16, A(BLUE, kz), A(WHITE, kz))
        text(d, (Xz(v), yl - 56 if up[v] else yl + 56), str(v), 56, BLUE, alpha=kz)
    y1 = 1270                                           # mot lan: +-20 (rut_ra)
    d.line([(Xz(486), y1), (Xz(526), y1)], fill=A(ORANGE, kz), width=10)
    for v in (486, 526): d.line([(Xz(v), y1 - 22), (Xz(v), y1 + 22)], fill=A(ORANGE, kz), width=6)
    text(d, (W / 2, y1 + 64), "một lần: ±20", 58, ORANGE, alpha=kz)
    k2 = appear(t, M[1] + 0.8, 0.4)                     # trung binh 5 lan: +-10
    y2 = 1440
    if k2 > 0:
        d.line([(Xz(496), y2), (Xz(516), y2)], fill=A(GREEN, k2), width=10)
        for v in (496, 516): d.line([(Xz(v), y2 - 22), (Xz(v), y2 + 22)], fill=A(GREEN, k2), width=6)
        dot(d, Xz(MEAN), y2, 16, A(GREEN, k2), A(WHITE, k2))
        text(d, (W / 2, y2 + 64), "trung bình 5 lần: ±10", 58, GREEN, alpha=k2)

# ---------------- canh 4: vi sao + chua noi ----------------
def s_why(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 1100), fill=WHITE, outline=BLUE, w=5)
    rr = random.Random(int(t / 0.3))
    fire = set(rr.sample(range(48), rr.randint(2, 7)))
    for i in range(48):
        cx, cy = 150 + (i % 12) * 71, 360 + (i // 12) * 90
        dot(d, cx, cy, 26, ORANGE if i in fire else (226, 214, 196), NAVY)
    text(d, (W / 2, 800), "Mỗi phút rã ngẫu nhiên", 60, INK)
    k2 = appear(t, M[1] + 0.2, 0.4)
    text(d, (W / 2, 930), "Trung bình: đặc trưng nguồn", 60, BLUE, alpha=k2)

# ---------------- canh 5: bay quen tru phong ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.2, 0.4)
    card(d, (40, 250, 1040, 520), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pill(d, W / 2, 320, "BẪY", RED, a1)
    text(d, (W / 2, 440), "“Nguồn cho 506 xung/phút”?", 60, INK, alpha=a1)
    kb = appear(t, M[1] - 0.9, 0.45)
    if kb > 0:
        card(d, (40, 560, 1040, 1200), fill=A(WHITE, kb), outline=A(LIGHT, kb), w=3)
        yb, yt = 1120, 680; Y = lambda n: yb - n / 600 * (yb - yt)
        d.line([(210, yb), (900, yb)], fill=A(NAVY, kb), width=5); d.line([(210, yb), (210, yt - 20)], fill=A(NAVY, kb), width=5)
        for n in (0, 200, 400, 600): text(d, (190, Y(n)), str(n), 56, NOTE, anchor="rm", alpha=kb)
        x = 360
        d.rectangle([x - 80, Y(NET), x + 80, yb], fill=A(GREEN, kb))
        d.rectangle([x - 80, Y(MEAN), x + 80, Y(NET)], fill=A(PURPLE, kb))
        text(d, (x, Y(MEAN) - 40), f"đo {MEAN}", 56, INK, alpha=kb)
        d.line([(x + 86, (Y(MEAN) + Y(NET)) / 2), (520, 770)], fill=A(PURPLE, kb), width=4)
        text(d, (530, 770), f"phông {PHONG}", 58, PURPLE, anchor="lm", alpha=kb)
        text(d, (x + 110, Y(NET / 2)), f"nguồn {NET}", 58, GREEN, anchor="lm", alpha=kb)
    kv = appear(t, M[1] + 2.0, 0.45)
    if kv > 0:
        card(d, (40, 1250, 1040, 1440), fill=A((240, 253, 244), kv), outline=A(GREEN, kv), w=5)
        text(d, (W / 2, 1345), "Phải trừ phông nền", 62, GREEN, alpha=kv)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 260, 1040, 1450), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 340, "THỬ NGHĨ", ORANGE, k1)
    seg_bar(d, 420, t, 0.8, sc["T"] - 0.2, ORANGE, k1)
    text(d, (W / 2, 570), "Đếm mỗi lần 4 phút:", 60, INK, alpha=k1)
    text(d, (W / 2, 665), "độ lệch (%) đổi thế nào?", 60, DORANGE, alpha=k1)
    for cx, sec in ((330, 15), (750, 60)):
        stopwatch(d, cx, 980, sec, False, r=120)
    text(d, (330, 1180), "1 phút", 58, NOTE, alpha=k1)
    text(d, (750, 1180), "4 phút", 58, ORANGE, alpha=k1)
    arrow(d, (470, 980), (610, 980), A(GRAY, k1), w=8, head=24)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, b, e = sc["hook"], sc["do"], sc["ans"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    for i in range(6):
        s = count_at(i, do); x = s
        while x < s + SWEEP: out.append((do["t0"] + x, "tick")); x += 0.2
        out.append((do["t0"] + s + SWEEP, "tap"))
    out += [(an["t0"] + 0.2, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + 0.15, "open")]
    return out

SCENES = [
 dict(key="hook", title="Đếm xung từng phút", draw=s_hook, tail=0.2, caps=[
   ("Nguồn cách ống 10 cm.", 3.0),
   ("Dừng lại, tự đoán.", 4.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Đếm 1 phút, ghi số; 5 lần.", 5.4),
   ("Cất nguồn, đếm phông nền.", 2.9)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.4, caps=[
   ("Năm số khác nhau, quanh 506.", 3.0),
   ("Trung bình 5 lần ít lệch hơn.", 4.0)]),
 dict(key="why", title="Vì sao?", draw=s_why, tail=0.2, caps=[
   ("Phân rã là ngẫu nhiên.", 3.0),
   ("Chưa biết nguồn có yếu dần.", 3.4)]),
 dict(key="bay", title="Cái bẫy", draw=s_bay, tail=0.4, caps=[
   ("Đúng hay sai?", 2.8),
   ("Sai: 506 còn lẫn phông 23.", 5.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=2.8, caps=[
   ("Từng phút ngẫu nhiên, trung bình ổn định.", 4.0)]),
]

CLIP = dict(id="tn-l12-phongxa-01", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Hiện tượng phóng xạ · thachlab.id.vn", scenes=SCENES)
