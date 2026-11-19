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

def source(d, x, y):
    d.rounded_rectangle([x - 36, y - 36, x + 36, y + 36], radius=12, fill=YELLOW, outline=NAVY, width=5)
    for k in range(3):
        g = 90 + 120 * k
        d.pieslice([x - 26, y - 26, x + 26, y + 26], g - 30, g + 30, fill=NAVY)
    dot(d, x, y, 6, YELLOW)

def rig(d, t, reading, sub, mat=None, mat_k=1.0, frac=1.0, beam=True, label=None):
    """mat: ten tam dang chen (None = khong chen); mat_k: 0..1 muc truot vao; frac: ti le tia qua (T)."""
    # may dem
    card(d, (60, 270, 560, 580), fill=WHITE, outline=LIGHT, r=28, w=4)
    d.rounded_rectangle([100, 320, 520, 450], radius=16, fill=NAVY)
    text(d, (310, 385), str(reading), 72, (134, 239, 172))
    text(d, (310, 515), sub, 44, NOTE, bold=False)
    # the vat lieu
    card(d, (600, 270, 1020, 580), fill=WHITE, outline=LIGHT, r=28, w=4)
    text(d, (810, 330), "Tấm chèn", 44, NOTE, bold=False)
    lb = label if label is not None else (mat or "không có")
    text(d, (810, 450), lb, 54, PB if mat and mat.startswith("chì") else INK)
    # ban
    d.line([(80, 900), (1000, 900)], fill=NAVY, width=6)
    d.rectangle([SX - 8, SY + 36, SX + 8, 896], fill=GRAY); d.rectangle([SX - 60, 882, SX + 60, 898], fill=NAVY)
    source(d, SX, SY); text(d, (SX, 960), "nguồn γ", 44, NOTE, bold=False)
    mx = (DX0 + DX1) / 2
    d.rectangle([mx - 8, SY + 40, mx + 8, 896], fill=GRAY); d.rectangle([mx - 60, 882, mx + 60, 898], fill=NAVY)
    d.rounded_rectangle([DX0, SY - 44, DX1, SY + 44], radius=30, fill=(214, 220, 232), outline=NAVY, width=5)
    d.rectangle([DX0 - 6, SY - 36, DX0 + 14, SY + 36], fill=(70, 78, 100))
    text(d, (mx, 960), "đầu dò", 44, NOTE, bold=False)
    # khoang cach 1 m
    for xx in (SX, DX0): d.line([(xx, 625), (xx, 655)], fill=NOTE, width=4)
    arrow(d, (SX + 4, 640), (DX0 - 4, 640), NOTE, w=4, head=14); arrow(d, (DX0 - 4, 640), (SX + 4, 640), NOTE, w=4, head=14)
    d.rectangle([290, 616, 380, 664], fill=BG); text(d, (335, 640), "1 m", 44, NOTE)
    # tia gamma: chum hep, cham cam; sau tam chen chi con ti le frac (tia dung o mat tam)
    wslab = SLAB[mat][0] if mat else 0
    sl_l, sl_r = SLX - wslab / 2, SLX + wslab / 2
    if beam:
        for j in range(NRAY):
            q = (j / NRAY + t * 0.8) % 1
            x = lerp(SX + 44, DX0 - 4, q); y = SY + ((j * 7) % 5 - 2) * 9
            passes = (j * 0.618) % 1 < frac
            if mat and mat_k >= 1 and x > sl_l and not passes: continue
            dot(d, x, y, 7, ORANGE)
    # tam chen truot tu tren xuong
    if mat:
        w, col = SLAB[mat]
        y0 = lerp(380, SY - 110, ease(mat_k))
        d.rectangle([SLX - w / 2, y0, SLX + w / 2, y0 + 220], fill=col, outline=NAVY, width=3)

# ---------------- bieu do cot: truc tu 0 ----------------
def bars(d, box, vals, alphas, xs, labs, err=0.0, ymax=400):
    x0b, y0b, x1b, y1b = box
    card(d, box, fill=WHITE, outline=LIGHT, w=3)
    yb, yt = y1b - 100, y0b + 100
    Y = lambda n: yb - n / ymax * (yb - yt)
    text(d, (x1b - 40, y0b + 50), "xung/phút", 44, NOTE, bold=False, anchor="rm")
    for n in range(100, ymax + 1, 100): d.line([(190, Y(n)), (x1b - 30, Y(n))], fill=(240, 236, 228), width=2)
    d.line([(190, yb), (x1b - 30, yb)], fill=NAVY, width=5); d.line([(190, yb), (190, yt - 20)], fill=NAVY, width=5)
    for n in range(0, ymax + 1, 200): text(d, (172, Y(n)), str(n), 44, NOTE, bold=False, anchor="rm")
    for i, (v, a) in enumerate(zip(vals, alphas)):
        x = xs[i]
        text(d, (x, yb + 45), labs[i], 44, NOTE)
        if a <= 0: continue
        top = yb - (yb - Y(v)) * ease(a)
        if yb - top > 2: d.rectangle([x - 50, top, x + 50, yb], fill=PB if labs[i] in ("chì", "5 mm", "10 mm") else BLUE)
        lab_y = top - 32 if not (err > 0 and i < 2) else Y(v + SAI) - 34
        text(d, (x, lab_y), str(v), 44, INK, alpha=clamp(a * 2 - 1))
        if err > 0 and i < 2:                             # thanh sai so +-19
            for yy in (Y(v - SAI), Y(v + SAI)): d.line([(x - 24, yy), (x + 24, yy)], fill=A(RED, err), width=5)
            d.line([(x, Y(v - SAI)), (x, Y(v + SAI))], fill=A(RED, err), width=5)
    return Y

BXS = [300, 480, 660, 840]

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, t, N0, "xung/phút", label="?")
    a = appear(t, M[1] - 0.6, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 430), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 175), "Chèn giấy, nhôm 3 mm, chì 5 mm.", 46, INK, alpha=a)
    text(d, (W / 2, y0 + 290), "Số đếm đổi thế nào?", 50, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 370, 940, y0 + 384], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 370, 140 + 800 * (1 - p), y0 + 384], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: chen tung tam, dem 1 phut ----------------
SLIDE, CNT = 0.5, 0.7
def steps(sc):
    """moc bat dau chen tam i (1 giay, 2 nhom, 3 chi); i = 0 khong chen (doc ngay)."""
    M = sc["M"]
    return [0.0, M[0] + 0.5, M[0] + 2.2, M[1] + 0.1]

LABEL = {"giấy": "giấy 0,1 mm", "nhôm": "nhôm 3 mm", "chì": "chì 5 mm"}
def do_state(t, sc):
    """(so, nhan, tam, muc truot, ti le qua, so cot) -- mot nguon trang thai cho may dem, tam chen, the, cot."""
    st = steps(sc); n = 1; mat, mk, frac = None, 1.0, 1.0; reading, sub = N0, "xung/phút"
    for i in range(1, 4):
        s = st[i]
        if t < s: break
        mat = ROWS[i][0]; mk = clamp((t - s) / SLIDE); frac = ROWS[i][1] / N0
        if t < s + SLIDE + CNT: reading, sub = "···", "đang đếm 1 phút"
        else: reading, sub = ROWS[i][1], "xung/phút"; n = i + 1
    return reading, sub, mat, mk, frac, n

def s_do(img, d, t, sc):
    reading, sub, mat, mk, frac, n = do_state(t, sc)
    rig(d, t, reading, sub, mat, mk, frac, label=LABEL.get(mat))
    st = steps(sc)
    al = [appear(t, 0.3, 0.35)] + [appear(t, st[i] + SLIDE + CNT, 0.35) if i < n else 0 for i in range(1, 4)]
    bars(d, (60, 1010, 1020, 1600), [r[1] for r in ROWS], al, BXS, [r[0] for r in ROWS])

# ---------------- canh 3: Dap an + sai so ----------------
def s_ans(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.3, 0.4)
    s = "ĐÁP ÁN · chỉ chì giảm rõ"
    pw = tw(d, s, F(42)) + 56
    card(d, (W / 2 - pw / 2, 236, W / 2 + pw / 2, 304), fill=A(NAVY, ka), r=32)
    text(d, (W / 2, 270), s, 42, WHITE, alpha=ka)
    ke = appear(t, M[0] + 0.6, 0.4)
    Y = bars(d, (60, 330, 1020, 1000), [r[1] for r in ROWS], [1] * 4, BXS, [r[0] for r in ROWS], err=ke)
    if ke > 0:
        text(d, (390, 1060), "±19: sai số đếm", 44, RED, alpha=ke)
    # ti so N/N0
    kt = appear(t, M[1] - 0.1, 0.4)
    if kt <= 0: return
    card(d, (60, 1120, 1020, 1400), fill=A(WHITE, kt), outline=A(LIGHT, kt), w=3)
    text(d, (W / 2, 1175), "Phần còn lại", 44, NOTE, alpha=kt)
    for i, (nm, _, tt) in enumerate(ROWS):
        if i == 0: continue
        x = BXS[i]
        text(d, (x, 1255), nm, 44, NOTE, bold=False, alpha=kt)
        text(d, (x, 1330), tt, 52, PB if nm == "chì" else INK, alpha=kt)

# ---------------- canh 4: rut ra + chua noi duoc gi ----------------
def s_why(img, d, t, sc):
    M = sc["M"]
    a = appear(t, 0.2, 0.4)
    card(d, (60, 260, 1020, 760), fill=A(WHITE, a), outline=A(BLUE, a), w=5)
    # chi noi ve gamma (so_lieu_mau); alpha/beta chua thu trong thi nghiem nay (khong_chung_minh)
    for j, (mats, x_end, line) in enumerate((((PAPER, AL), 960, "Giấy, nhôm 3 mm: cản ít"),
                                             ((PB,), 760, "Chì: giảm rõ"))):
        y = 370 + j * 200; k = appear(t, 0.3 + j * 0.9, 0.4)
        if k <= 0: continue
        dot(d, 130, y, 40, A(ORANGE, k)); text(d, (130, y), "γ", 50, WHITE, alpha=k)
        for i, col in enumerate(mats):
            xs = 380 + i * 170; ww = 18 if col is PAPER else (30 if col is AL else 60)
            d.rectangle([xs, y - 48, xs + ww, y + 48], fill=A(col, k), outline=A(NAVY, k), width=3)
        if j == 0: arrow(d, (190, y), (x_end, y), A(ORANGE, k), w=7, head=20)
        else:
            d.line([(190, y), (375, y)], fill=A(ORANGE, k), width=7)
            arrow(d, (445, y), (x_end, y), A((253, 186, 116), k), w=4, head=16)
        text(d, (W / 2, y + 88), line, 44, INK, alpha=k)
    b = appear(t, M[1] - 0.1, 0.4)
    if b <= 0: return
    card(d, (60, 810, 1020, 1180), fill=A(WHITE, b), outline=A(PURPLE, b), w=5)
    text(d, (W / 2, 875), "Chưa nói được gì?", 48, PURPLE, alpha=b)
    text(d, (120, 990), "• Giấy có chặn α?", 46, INK, anchor="lm", alpha=b)
    text(d, (120, 1100), "• Liều cơ thể người?", 46, INK, anchor="lm", alpha=appear(t, M[1] + 1.4, 0.4))

# ---------------- canh 5: bay "them chi la chan het" ----------------
TX = [330, 560, 790]
def s_bay(img, d, t, sc):
    M = sc["M"]; mk = M[1]
    a1 = appear(t, 0.2, 0.4)
    card(d, (40, 250, 1040, 520), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(40)) + 52
    card(d, (W / 2 - pw / 2, 276, W / 2 + pw / 2, 340), fill=A(RED, a1), r=32)
    text(d, (W / 2, 308), "BẪY", 40, WHITE, alpha=a1)
    q = "“Thêm 5 mm chì là chặn hết”"
    ks = clamp((t - mk) / 0.4); f = F(48); lw = tw(d, q, f); yy = 440
    text(d, (W / 2, yy), q, 48, mix(INK, GRAY, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85), width=6)
    kb = appear(t, mk - 1.4, 0.45)
    if kb <= 0: return
    Y = bars(d, (40, 560, 1040, 1260), [N0, ROWS[3][1], PB10], [kb, kb, kb], TX, ["0 mm", "5 mm", "10 mm"])
    for i in range(2):
        k = appear(t, mk - 0.8 + i * 0.5, 0.4)
        if k <= 0: continue
        xa, xb = TX[i] + 56, TX[i + 1] - 56; ya = Y([N0, ROWS[3][1]][i]) + 20
        arrow(d, (xa, ya), (xb, ya + 50), A(ORANGE, k), w=6, head=18)
        text(d, ((xa + xb) / 2 + 6, ya - 30), "× 0,43", 44, ORANGE, alpha=k)
    kv = appear(t, mk + 1.0, 0.45)
    if kv > 0:
        card(d, (40, 1310, 1040, 1470), fill=A((254, 242, 242), kv), outline=A(RED, kv), w=4)
        text(d, (W / 2, 1390), "Giảm mãi, không về 0", 52, RED, alpha=kv)

# ---------------- canh 6: chot + cau hoi tu nho lai ----------------
def _end_body(d, t, k):
    if k > 0.5: source(d, 300, 1080)
    d.rectangle([560, 1020, 604, 1140], fill=A(PB, k), outline=A(NAVY, k), width=3)
    d.rounded_rectangle([760, 990, 880, 1170], radius=24, fill=A((214, 220, 232), k), outline=A(NAVY, k), width=5)
    text(d, (582, 1200), "chì", 44, NOTE, alpha=k)

def s_end(img, d, t, sc):
    M = sc["M"]
    chot_hoi(d, t, sc, "Chắn gamma: chì, đủ dày",
             "Chì nhỏ hơn chùm tia, tia lọt qua mép: số đếm lớn hơn hay nhỏ hơn 154?", None, body=_end_body)
    kh = appear(t, M[0] + 2.6, 0.5)
    if kh > 0:
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        ctext(d, 1360, "Gợi ý", 44, INK, alpha=kh)
        ctext(d, 1450, "Tia còn đường nào khác?", 46, (176, 64, 8), maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, wy, b, e = sc["hook"], sc["do"], sc["ans"], sc["why"], sc["bay"], sc["end"]
    st = steps(do)
    out = [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + st[i] + SLIDE + CNT, "tap") for i in range(1, 4)]
    out += [(an["t0"] + 0.3, "ding"), (wy["t0"] + wy["M"][1] - 0.1, "tap"),
            (b["t0"] + b["M"][1], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l12-antoanpx-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="An toàn phóng xạ · thachlab.id.vn", scenes=[
 dict(key="hook", title="Ba tấm chắn trước chùm gamma", draw=s_hook, tail=0.3, caps=[
   ("Đầu dò cách nguồn gamma 1 m.", 3.4),
   ("Chọn đáp án ở khung câu hỏi.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Chèn giấy, rồi nhôm 3 mm.", 4.0),
   ("Thay bằng chì 5 mm.", 2.9)]),
 dict(key="ans", title="Kết quả", draw=s_ans, tail=0.5, caps=[
   ("Giấy: lệch nằm trong sai số.", 3.4),
   ("Nhôm giảm ít, chì giảm rõ.", 3.4)]),
 dict(key="why", title="Rút ra", draw=s_why, tail=0.4, caps=[
   ("Gamma xuyên giấy, nhôm mỏng.", 3.4),
   ("Chưa trả lời được.", 4.0)]),
 dict(key="bay", title="Cái bẫy", draw=s_bay, tail=0.4, caps=[
   ("Đúng hay sai?", 2.5),
   ("Sai: 10 mm vẫn còn 66.", 5.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Dừng video và trả lời.", 6.2)]),
])
