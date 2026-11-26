# Clip: tn-l12-antoanpx-02 - Giay, nhom, chi truoc chum gamma (ban 1, 14/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-antoanpx-02.json:
#   so_lieu_mau: khong chan 360 | giay 0,1 mm 355 (T 0,99) | nhom 3 mm 335 (T 0,93) | chi 5 mm 154 (T 0,43) | chi 10 mm 66 (T 0,18).
#   ghi_chu: sai so dem +-19 o muc 360 -> 360 va 355 coi nhu bang nhau. du_doan_neu_dung: moi 5 mm chi nhan ~0,43 (360 -> 154 -> 66).
#   cac_buoc: dau do cach nguon 1 m, moi lan dem 1 phut. khong_chung_minh: chua thay giay chan alpha; chua cho lieu co the.
# Khac antoanpx1 (lui xa, 1/r^2): clip nay ve vat lieu chan va quy luat ham mu theo be day.
# Du doan (khung ben canh, K10 khong ve nut; chum gamma 360 xung/phut, chen giay, nhom 3 mm, chi 5 mm):
#   A. Giay giam manh nhat (nham alpha/gamma)      B. Ba tam giam gan bang nhau
#   C. Chi chi giam ro  <- dung                    D. Tam nao cung chan het (hien_tuong_hay_sai #1)
# Cau chot (T7, sai so co chieu, ca moi khong trung Du doan): tam chi khong phu het mat dau do (sai_so_thuong_gap #1:
#   tia lot thang vao) -> so dem sau chi LON hon 154. Man hinh khong noi y nay.
# Dung lai 26/11/2026 (viec 4 lo 32): cong --do-chu, chu >= 56 px khi ve, <= 50 s, bo the goi y o canh chot; THU NGHI
#   = cau_chot (ca tu suy tu sai_so_thuong_gap: tia lot qua mep -> so dem LON hon 154).
from engine import *

ROWS = [("không", 360, "1"), ("giấy", 355, "0,99"), ("nhôm", 335, "0,93"), ("chì", 154, "0,43")]   # so_lieu_mau
PB10 = 66                                   # so_lieu_mau: chi 10 mm
N0, SAI = 360, 19                           # so_lieu_mau ghi_chu: +-19 o muc 360
NOTE = (70, 75, 95)
PAPER, AL, PB = (250, 250, 245), (196, 204, 214), (92, 96, 108)

# ---------------- dung cu: nguon gamma - tam chen - dau do ----------------
SX, SY = 170, 730
SLX = 520                                   # tam cua tam chen
DX0, DX1 = 840, 990                         # dau do (cua so o DX0)
SLAB = {"giấy": (8, PAPER), "nhôm": (26, AL), "chì": (44, PB), "chì 10": (88, PB)}   # be rong ve (khong theo ti le)
NRAY = 24

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
    d.rounded_rectangle([x - 36, y - 36, x + 36, y + 36], radius=12, fill=A(YELLOW, a), outline=A(NAVY, a), width=5)
    for k in range(3):
        g = 90 + 120 * k
        d.pieslice([x - 26, y - 26, x + 26, y + 26], g - 30, g + 30, fill=A(NAVY, a))
    dot(d, x, y, 6, A(YELLOW, a))

def rig(d, t, reading, mat=None, mat_k=1.0, frac=1.0, label=None):
    card(d, (60, 270, 560, 580), fill=WHITE, outline=LIGHT, r=28, w=4)
    d.rounded_rectangle([100, 310, 520, 440], radius=16, fill=NAVY)
    text(d, (310, 375), str(reading), 76, (134, 239, 172))
    text(d, (310, 515), "xung/phút", 56, NOTE)
    card(d, (600, 270, 1020, 580), fill=WHITE, outline=LIGHT, r=28, w=4)
    text(d, (810, 340), "chèn", 56, NOTE)
    lb = label if label is not None else (mat or "không")
    text(d, (810, 460), lb, 58, PB if mat and mat.startswith("chì") else INK)
    d.line([(80, 900), (1000, 900)], fill=NAVY, width=6)
    d.rectangle([SX - 8, SY + 36, SX + 8, 896], fill=GRAY); d.rectangle([SX - 60, 882, SX + 60, 898], fill=NAVY)
    source(d, SX, SY); text(d, (SX, 960), "nguồn γ", 56, NOTE)
    mx = (DX0 + DX1) / 2
    d.rectangle([mx - 8, SY + 40, mx + 8, 896], fill=GRAY); d.rectangle([mx - 60, 882, mx + 60, 898], fill=NAVY)
    d.rounded_rectangle([DX0, SY - 44, DX1, SY + 44], radius=30, fill=(214, 220, 232), outline=NAVY, width=5)
    d.rectangle([DX0 - 6, SY - 36, DX0 + 14, SY + 36], fill=(70, 78, 100))
    text(d, (mx - 20, 960), "đầu dò", 56, NOTE)
    for xx in (SX, DX0): d.line([(xx, 625), (xx, 655)], fill=NOTE, width=4)
    arrow(d, (SX + 4, 640), (DX0 - 4, 640), NOTE, w=4, head=14); arrow(d, (DX0 - 4, 640), (SX + 4, 640), NOTE, w=4, head=14)
    d.rectangle([280, 606, 390, 674], fill=BG); text(d, (335, 640), "1 m", 56, NOTE)
    wslab = SLAB[mat][0] if mat else 0
    sl_l = SLX - wslab / 2
    for j in range(NRAY):
        q = (j / NRAY + t * 0.8) % 1
        x = lerp(SX + 44, DX0 - 4, q); y = SY + ((j * 7) % 5 - 2) * 9
        passes = (j * 0.618) % 1 < frac
        if mat and mat_k >= 1 and x > sl_l and not passes: continue
        dot(d, x, y, 7, ORANGE)
    if mat:
        w, col = SLAB[mat]
        y0 = lerp(380, SY - 110, ease(mat_k))
        d.rectangle([SLX - w / 2, y0, SLX + w / 2, y0 + 220], fill=col, outline=NAVY, width=3)

def bars(d, box, vals, alphas, xs, labs, err=0.0, ymax=400):
    x0b, y0b, x1b, y1b = box
    card(d, box, fill=WHITE, outline=LIGHT, w=3)
    yb, yt = y1b - 100, y0b + 110
    Y = lambda n: yb - n / ymax * (yb - yt)
    text(d, (x1b - 40, y0b + 50), "xung/phút", 56, NOTE, anchor="rm")
    for n in range(100, ymax + 1, 100): d.line([(200, Y(n)), (x1b - 30, Y(n))], fill=(240, 236, 228), width=2)
    d.line([(200, yb), (x1b - 30, yb)], fill=NAVY, width=5); d.line([(200, yb), (200, yt - 20)], fill=NAVY, width=5)
    for n in range(0, ymax + 1, 200): text(d, (180, Y(n)), str(n), 56, NOTE, anchor="rm")
    for i, (v, a) in enumerate(zip(vals, alphas)):
        x = xs[i]
        text(d, (x, yb + 50), labs[i], 56, NOTE)
        if a <= 0: continue
        top = yb - (yb - Y(v)) * ease(a)
        if yb - top > 2: d.rectangle([x - 55, top, x + 55, yb], fill=PB if labs[i] in ("chì", "5 mm", "10 mm") else BLUE)
        lab_y = top - 36 if not (err > 0 and i < 2) else Y(v + SAI) - 38
        text(d, (x, lab_y), str(v), 56, INK, alpha=clamp(a * 2 - 1))
        if err > 0 and i < 2:
            for yy in (Y(v - SAI), Y(v + SAI)): d.line([(x - 26, yy), (x + 26, yy)], fill=A(RED, err), width=6)
            d.line([(x, Y(v - SAI)), (x, Y(v + SAI))], fill=A(RED, err), width=6)
    return Y

BXS = [320, 500, 680, 860]

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, t, N0, label="?")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 66, "DỰ ĐOÁN", PURPLE, a)
    seg_bar(d, y0 + 130, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, a)
    text(d, (W / 2, y0 + 300), "Chèn giấy, nhôm, rồi chì.", 56, INK, alpha=a)
    text(d, (W / 2, y0 + 405), "Số đếm đổi thế nào?", 62, PURPLE, alpha=a)

# ---------------- canh 2: chen tung tam, dem 1 phut ----------------
SLIDE, CNT = 0.5, 0.7
def steps(sc):
    M = sc["M"]
    return [0.0, 2.0, 4.2, M[1] + 0.6]

LABEL = {"giấy": "giấy 0,1 mm", "nhôm": "nhôm 3 mm", "chì": "chì 5 mm"}
def do_state(t, sc):
    st = steps(sc); n = 1; mat, mk, frac = None, 1.0, 1.0; reading = N0
    for i in range(1, 4):
        s = st[i]
        if t < s: break
        mat = ROWS[i][0]; mk = clamp((t - s) / SLIDE); frac = ROWS[i][1] / N0
        if t < s + SLIDE + CNT: reading = "···"
        else: reading = ROWS[i][1]; n = i + 1
    return reading, mat, mk, frac, n

def s_do(img, d, t, sc):
    reading, mat, mk, frac, n = do_state(t, sc)
    rig(d, t, reading, mat, mk, frac, label=LABEL.get(mat))
    st = steps(sc)
    al = [1.0] + [appear(t, st[i] + SLIDE + CNT, 0.35) if i < n else 0 for i in range(1, 4)]
    bars(d, (40, 1030, 1040, 1600), [r[1] for r in ROWS], al, BXS, [r[0] for r in ROWS])

# ---------------- canh 3: Dap an + sai so ----------------
def s_ans(img, d, t, sc):
    M = sc["M"]
    pill(d, W / 2, 290, "ĐÁP ÁN: chỉ chì giảm rõ", NAVY)
    ke = appear(t, 2.3, 0.4)
    bars(d, (40, 360, 1040, 1000), [r[1] for r in ROWS], [1] * 4, BXS, [r[0] for r in ROWS], err=ke)
    if ke > 0: text(d, (W / 2, 1060), "±19: sai số đếm", 58, RED, alpha=ke)
    kt = appear(t, M[1] + 0.7, 0.4)
    if kt <= 0: return
    card(d, (40, 1120, 1040, 1420), fill=A(WHITE, kt), outline=A(LIGHT, kt), w=3)
    text(d, (150, 1270), "còn", 58, NOTE, alpha=kt)
    for i, (nm, _, tt) in enumerate(ROWS):
        if i == 0: continue
        x = BXS[i]
        text(d, (x, 1200), nm, 56, NOTE, alpha=kt)
        text(d, (x, 1300), tt, 62, PB if nm == "chì" else INK, alpha=kt)

# ---------------- canh 4: rut ra ----------------
def s_why(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 900), fill=WHITE, outline=BLUE, w=5)
    for j, (mats, x_end, line) in enumerate((((PAPER, AL), 960, "Giấy, nhôm 3 mm: cản ít"),
                                             ((PB,), 760, "Chì 5 mm: giảm rõ"))):
        y = 380 + j * 260; k = appear(t, 0.3 if j == 0 else M[1] + 0.2, 0.4)
        if k <= 0: continue
        dot(d, 130, y, 44, A(ORANGE, k)); text(d, (130, y), "γ", 60, WHITE, alpha=k)
        for i, col in enumerate(mats):
            xs = 380 + i * 170; ww = 18 if col is PAPER else (30 if col is AL else 60)
            d.rectangle([xs, y - 52, xs + ww, y + 52], fill=A(col, k), outline=A(NAVY, k), width=3)
        q = (t * 0.7) % 1                                # hat gamma chay doc theo tia
        if j == 0:
            arrow(d, (190, y), (x_end, y), A(ORANGE, k), w=7, head=22)
            dot(d, lerp(200, x_end - 30, q), y, 12, A(RED, k))
        else:
            d.line([(190, y), (375, y)], fill=A(ORANGE, k), width=7)
            arrow(d, (445, y), (x_end, y), A((253, 186, 116), k), w=4, head=16)
            dot(d, lerp(200, 370, q), y, 12, A(RED, k))
        text(d, (W / 2, y + 100), line, 58, INK, alpha=k)

# ---------------- canh 5: bay "them 5 mm chi la chan het" ----------------
TX = [340, 570, 800]
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.2, 0.4)
    card(d, (40, 250, 1040, 520), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pill(d, W / 2, 320, "BẪY", RED, a1)
    text(d, (W / 2, 440), "“Thêm 5 mm chì là chặn hết”?", 60, INK, alpha=a1)
    kb = appear(t, 2.6, 0.45)
    if kb <= 0: return
    Y = bars(d, (40, 560, 1040, 1260), [N0, ROWS[3][1], PB10], [kb, kb, kb], TX, ["0 mm", "5 mm", "10 mm"])
    for i in range(2):
        k = appear(t, 3.2 + i * 0.6, 0.4)
        if k <= 0: continue
        xa, xb = TX[i] + 60, TX[i + 1] - 60; ya = Y([N0, ROWS[3][1]][i]) + 20
        arrow(d, (xa, ya), (xb, ya + 50), A(ORANGE, k), w=6, head=18)
        text(d, ((xa + xb) / 2 + 50, ya - 30), "× 0,43", 56, ORANGE, alpha=k)
    kv = appear(t, M[1] + 2.4, 0.45)
    if kv > 0:
        card(d, (40, 1310, 1040, 1480), fill=A((254, 242, 242), kv), outline=A(RED, kv), w=4)
        text(d, (W / 2, 1395), "Giảm mãi, không về 0", 62, RED, alpha=kv)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 260, 1040, 1450), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 340, "THỬ NGHĨ", ORANGE, k1)
    seg_bar(d, 420, t, 0.8, sc["T"] - 0.2, ORANGE, k1)
    text(d, (W / 2, 570), "Chì hẹp, tia lọt qua mép:", 60, INK, alpha=k1)
    text(d, (W / 2, 665), "số đếm hơn hay kém 154?", 60, DORANGE, alpha=k1)
    y = 1000
    if k1 > 0.5: source(d, 200, y)
    for j in range(5):                                   # chum tia rong hon tam chi
        yy = y + (j - 2) * 55
        d.line([(250, yy), (520 if abs(j - 2) < 2 else 800, yy)], fill=A(ORANGE, k1), width=6)
    d.rectangle([520, y - 70, 570, y + 70], fill=A(PB, k1), outline=A(NAVY, k1), width=3)
    d.rounded_rectangle([800, y - 150, 920, y + 150], radius=24, fill=A((214, 220, 232), k1), outline=A(NAVY, k1), width=5)
    text(d, (545, y + 140), "chì", 56, NOTE, alpha=k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, b, e = sc["hook"], sc["do"], sc["ans"], sc["bay"], sc["end"]
    st = steps(do)
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + st[i] + SLIDE + CNT, "tap") for i in range(1, 4)]
    out += [(an["t0"] + 0.2, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + 0.15, "open")]
    return out

SCENES = [
 dict(key="hook", title="Ba tấm chắn trước chùm gamma", draw=s_hook, tail=0.2, caps=[
   ("Đầu dò cách nguồn 1 m.", 3.4),
   ("Dừng lại, tự đoán.", 4.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Chèn giấy, rồi nhôm 3 mm.", 5.6),
   ("Thay bằng chì 5 mm.", 3.2)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.4, caps=[
   ("Giấy: lệch nằm trong sai số.", 3.6),
   ("Nhôm giảm ít, chì giảm rõ.", 3.6)]),
 dict(key="why", title="Rút ra", draw=s_why, tail=0.2, caps=[
   ("Gamma xuyên giấy, nhôm mỏng.", 3.4),
   ("Chưa thử với tia alpha.", 3.2)]),
 dict(key="bay", title="Cái bẫy", draw=s_bay, tail=0.4, caps=[
   ("Đúng hay sai?", 2.8),
   ("Sai: 10 mm vẫn còn 66.", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=2.8, caps=[
   ("Chắn gamma: cần chì đủ dày.", 3.8)]),
]

CLIP = dict(id="tn-l12-antoanpx-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="An toàn phóng xạ · thachlab.id.vn", scenes=SCENES)
