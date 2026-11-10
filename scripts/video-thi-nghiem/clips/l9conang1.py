# Clip: tn-l9-conang-01 - Khoi truot tren mang dem khi nghieng: the nang luc tha va dong nang o chan doc (5/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-conang-01.json:
#   tham_so: m = 0,20 kg ; f = 0,04 ; sai so doc v 0,005 m/s
#   so_lieu_mau (h m, v m/s, 10mh J, 1/2mv^2 J): 0,10 1,39 0,2 0,193 ; 0,20 1,96 0,4 0,384 ; 0,30 2,40 0,6 0,576 ; 0,40 2,77 0,8 0,767
#   quan_sat: hut khoang 3-4 % ; sai_so_thuong_gap: doc v toi 0,01 m/s -> 1/2mv^2 sai 0,4-0,7 %.
# Canh (khac conang1 = con lac + bang, conangdddh1 = lo xo + cot chong dung):
#   Du doan (tha tu 0,20 m, 10mh = 0,4 J: dong nang o chan doc khoang bao nhieu? chi cau hoi + hinh, K10)
#   -> Tien hanh (mang nghieng cheo man, cong quang o chan doc, bang h-v) -> So sanh bang COT NGANG ghep doi
#   + DAP AN · gan bang 0,4 J -> Rut ra (thanh nang luong ngang: cam thu lai, xanh dai ra) -> Chua noi duoc + bay
#   "hut do doc sai" (0,4-0,7 % << 3-4 %) -> Chot + THU NGHI: tha tu 0,25 m (chua hien, nam giua 2 lan do).
# Cau 3 sau hop trong bai hoi LY DO hut -> clip KHONG noi nguyen nhan (luc can/nhiet), chi ghi "chua tra loi".
from engine import *

ROWS = [(0.10, 1.39, 0.2, 0.193), (0.20, 1.96, 0.4, 0.384), (0.30, 2.40, 0.6, 0.576), (0.40, 2.77, 0.8, 0.767)]
M_KG = 0.20
def fm(x, n=2): return f"{x:.{n}f}".replace(".", ",")
def fj(x): return (f"{x:.3f}".rstrip("0").rstrip(",.") if x * 1000 % 100 else f"{x:.1f}").replace(".", ",")

# ---------------- mang dem khi + cong quang + dong ho ----------------
FX, FY = 900, 900                  # chan doc
SY, SX = 1000, 1511                # px moi m do cao (doc), px ngang moi m do cao
HMAX = 0.45
EX, GATE_X, STOP_X = 1030, 925, 975
UX, UY = SX / math.hypot(SX, SY), SY / math.hypot(SX, SY)   # huong xuong doc
NX, NY = UY, -UX                                            # phap tuyen huong len
BL, BH = 50, 24                                             # nua dai, nua cao khoi truot

def track_pt(h): return FX - h * SX, FY - h * SY

def dashed(d, p1, p2, color, w=4, dash=16, gap=12):
    L = math.hypot(p2[0] - p1[0], p2[1] - p1[1]); n = int(L // (dash + gap)) + 1
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

def block(d, pos, alpha=1.0):
    """pos = ('doc', h) hoac ('ngang', x). Ve khoi truot, tra ve diem day giua (x, y)."""
    if pos[0] == "doc":
        bx, by = track_pt(pos[1]); ux, uy, nx, ny = UX, UY, NX, NY
    else:
        bx, by = pos[1], FY; ux, uy, nx, ny = 1, 0, 0, -1
    cx, cy = bx + nx * (BH + 10), by + ny * (BH + 10)
    pts = [(cx + sx * BL * ux + sy * BH * nx, cy + sx * BL * uy + sy * BH * ny) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    d.polygon(pts, fill=A(BLUE, alpha), outline=A(NAVY, alpha), width=4)
    return bx, by

def rig(d, t, pos, h_show, v_show, balpha=1.0, cards=True):
    # ban + chan do
    d.line([(60, 990), (1040, 990)], fill=NAVY, width=6)
    tx, ty = track_pt(HMAX)
    d.rectangle([tx + 10, ty + 20, tx + 26, 990], fill=GRAY)
    d.rectangle([FX - 8, FY + 18, FX + 8, 990], fill=GRAY); d.rectangle([EX - 30, FY + 18, EX - 14, 990], fill=GRAY)
    # mang (lo khi nho)
    d.line([(tx, ty), (FX, FY), (EX, FY)], fill=(90, 98, 122), width=20, joint="curve")
    for k in range(1, 14):
        h = HMAX * k / 14; x, y = track_pt(h); dot(d, x + NX * 4, y + NY * 4, 3, WHITE)
    for x in range(FX + 20, EX - 20, 32): dot(d, x, FY - 4, 3, WHITE)
    d.rectangle([EX - 4, FY - 70, EX + 10, FY + 10], fill=NAVY)            # tam chan mem
    # thuoc do do cao
    rx = 130
    d.rectangle([rx - 14, FY - HMAX * SY - 10, rx + 14, FY], fill=(255, 244, 214), outline=NAVY, width=3)
    for k in range(0, 10):
        y = FY - k * 0.05 * SY; L = 22 if k % 2 == 0 else 12
        d.line([(rx + 14 - L, y), (rx + 14, y)], fill=NAVY, width=3)
        if k % 2 == 0 and k > 0: text(d, (rx - 26, y), fm(k * 0.05, 1), 40, MUTED, bold=False, anchor="rm")
    dashed(d, (rx + 14, FY), (FX, FY), A(GRAY, 1.0), w=3)
    # cong quang + day noi dong ho
    d.line([(GATE_X, FY - 116), (GATE_X, 430)], fill=GRAY, width=6)
    d.rectangle([GATE_X - 12, FY - 130, GATE_X + 12, FY - 34], fill=NAVY)
    d.rectangle([GATE_X - 12, FY + 12, GATE_X + 12, FY + 40], fill=NAVY)
    d.line([(GATE_X, FY - 34), (GATE_X, FY + 12)], fill=A(RED, 0.8), width=4)
    # khoi truot + vach do cao
    bx, by = block(d, pos, balpha)
    if pos[0] == "doc" and pos[1] > 0.005:
        dashed(d, (rx + 14, by), (bx, by), A(ORANGE, balpha), w=4)
        dot(d, rx, by, 10, A(ORANGE, balpha))
    # the thong so + dong ho
    if not cards: return
    card(d, (60, 255, 570, 405), fill=WHITE, outline=LIGHT, r=26, w=4)
    text(d, (315, 297), f"khối lượng m = {fm(M_KG)} kg", 40, INK)
    text(d, (315, 363), "độ cao h = " + (fm(h_show) + " m" if h_show is not None else "?"), 40, ORANGE)
    card(d, (600, 255, 1020, 405), fill=(240, 246, 255), outline=BLUE, r=26, w=4)
    text(d, (810, 297), "vận tốc ở chân dốc", 40, MUTED)
    text(d, (810, 363), "v = " + (v_show if v_show else "?") + " m/s", 48, BLUE)

def slide(tau, h0, Ts):
    """Vi tri khoi sau tau giay ke tu luc tha tu h0 (xuong doc nhanh dan, roi chay ngang toi tam chan)."""
    if tau <= 0: return ("doc", h0)
    if tau < Ts: return ("doc", h0 * (1 - (tau / Ts) ** 2))
    k = clamp((tau - Ts) / 0.3); return ("ngang", lerp(FX, STOP_X, 1 - (1 - k) ** 2))
def passed(tau, Ts): p = slide(tau, 1, Ts); return p[0] == "ngang" and p[1] >= GATE_X   # tam khoi qua cong quang

# ---------------- canh 1: mo bai + du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    rig(d, t, ("doc", 0.20), 0.20, None)
    k = appear(t, sc["M"][1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (60, 1050, 1020, 1430), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 1110), "Dự đoán", 46, PURPLE, alpha=k)
    rich(d, W / 2, 1200, "Lúc thả: thế năng 10mh = 0,4 J", 44, INK, alpha=k)
    rich(d, W / 2, 1285, "Chân dốc: động năng ½mv² = ? J", 44, INK, alpha=k)
    t1, t2 = sc["M"][1] + 0.4, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1370, 940, 1384], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1370, 140 + 800 * (1 - q), 1384], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh, ghi bang ----------------
REL = [0.5, 2.5, 4.5, 6.5]                       # moc tha lan i
TS = [1.3 * math.sqrt(r[0] / 0.4) for r in ROWS]  # cung do doc: thoi gian xuong ti le sqrt(h)
def do_state(t):
    i = max([j for j in range(4) if t >= REL[j] - 0.35], default=0)
    tau = t - REL[i]; pos = slide(tau, ROWS[i][0], TS[i])
    if passed(tau, TS[i]): v = fm(ROWS[i][1])
    elif tau >= 0 or i == 0: v = None              # da tha lan moi: xoa so cu
    else: v = fm(ROWS[i - 1][1])
    ba = clamp((t - (REL[i] - 0.35)) / 0.25) if i > 0 or t < REL[0] else 1.0
    return i, pos, v, ba
def row_at(i): return REL[i] + TS[i] + 0.06       # hang hien cung luc so dong ho (khoi qua cong)

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    i, pos, v, ba = do_state(t)
    rig(d, t, pos, ROWS[i][0], v, balpha=ba)
    nshow = sum(1 for j in range(4) if t >= row_at(j))
    if nshow == 0 and t < REL[0] + TS[0]: pass
    card(d, (160, 1050, 920, 1530), fill=WHITE, outline=NAVY, w=4)
    text(d, (W / 2, 1488), "Số liệu minh hoạ", 40, MUTED, bold=False)
    xs = (370, 710)
    text(d, (xs[0], 1105), "h (m)", 40, ORANGE); text(d, (xs[1], 1105), "v (m/s)", 40, BLUE)
    d.line([(200, 1145), (880, 1145)], fill=LIGHT, width=4)
    for j, r in enumerate(ROWS):
        a = appear(t, row_at(j), 0.35); y = 1195 + j * 76
        if a <= 0: continue
        if j == nshow - 1: d.rounded_rectangle([190, y - 32, 890, y + 32], radius=16, fill=A((225, 236, 255), a))
        text(d, (xs[0], y), fm(r[0]), 44, ORANGE, alpha=a); text(d, (xs[1], y), fm(r[1]), 44, BLUE, alpha=a)

# ---------------- canh 3: so sanh bang cot ngang ----------------
BX0, BSC = 290, 760                 # goc truc, px moi J (0,8 J -> 608 px)
GY0, GDY = 470, 168
def s_cmp(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    d.rectangle([90, 290, 130, 330], fill=ORANGE); rich(d, 150, 310, "10mh: thế năng", 40, INK, anchor="l")
    d.rectangle([90, 362, 130, 402], fill=BLUE); rich(d, 150, 382, "½mv²: động năng", 40, INK, anchor="l")
    hl = appear(t, M[1], 0.4)
    if hl > 0:
        y = GY0 + GDY
        d.rounded_rectangle([70, y - 34, 1030, y + 98], radius=20, fill=A((220, 252, 231), hl), outline=A(GREEN, hl), width=4)
    d.line([(BX0, GY0 - 40), (BX0, GY0 + 3 * GDY + 110)], fill=NAVY, width=5)
    for j, (h, v, wt, wd) in enumerate(ROWS):
        y = GY0 + j * GDY
        text(d, (BX0 - 22, y + 32), fm(h) + " m", 40, MUTED, anchor="rm")
        for k, (val, col, at) in enumerate(((wt, ORANGE, M[0] + 0.2 + 0.25 * j), (wd, BLUE, M[0] + 1.6 + 0.25 * j))):
            g = ease((t - at) / 0.5)
            if g <= 0: continue
            yy = y + k * 62; x1 = BX0 + val * BSC * g
            if x1 - BX0 > 2: d.rectangle([BX0, yy - 4, x1, yy + 44], fill=col)
            text(d, (x1 + 16, yy + 20), fj(val), 40, col, anchor="lm", alpha=clamp(g * 2 - 1))
    if hl > 0:
        card(d, (150, 1210, 930, 1310), fill=A(GREEN, hl), r=50)
        text(d, (W / 2, 1260), "ĐÁP ÁN · gần bằng 0,4 J", 46, WHITE, alpha=hl)
    h2 = appear(t, M[1] + 1.2, 0.4)
    text(d, (W / 2, 1390), "lần nào cũng hụt 3–4 %", 44, RED, alpha=h2)

# ---------------- canh 4: rut ra, thanh nang luong ----------------
RH, RT0, RTS = 0.30, 0.7, 3.4                    # tha tu 0,30 m, chieu cham
ESC, EX0 = 1300, 110                             # px moi J, goc thanh
def s_rut(img, d, t, sc):
    IMG_REF[0] = img
    tau = t - RT0; pos = slide(tau, RH, RTS)
    hb = pos[1] if pos[0] == "doc" else 0.0
    rig(d, t, pos, RH, None, cards=False)
    fr = (RH - hb) / RH
    wt = 10 * M_KG * RH * (1 - fr); wd = ROWS[2][3] * fr         # cuoi: wd = 0,576 J (so lieu mau)
    card(d, (60, 1050, 1020, 1470), fill=WHITE, outline=LIGHT, w=4)
    text(d, (W / 2, 1105), "cơ năng = thế năng + động năng", 42, INK)
    yb0, yb1 = 1210, 1290
    xw = EX0 + wd * ESC
    if wd * ESC > 2: d.rectangle([EX0, yb0, xw, yb1], fill=BLUE)
    if wt * ESC > 2: d.rectangle([xw, yb0, xw + wt * ESC, yb1], fill=ORANGE)
    xm = EX0 + 0.6 * ESC
    dashed(d, (xm, yb0 - 40), (xm, yb1 + 20), NAVY, w=4, dash=10, gap=8)
    text(d, (xm, yb0 - 62), "0,6 J lúc thả", 40, NAVY, anchor="mm")
    d.rectangle([150, 1360, 190, 1400], fill=ORANGE); text(d, (205, 1380), "thế năng", 40, INK, anchor="lm")
    d.rectangle([470, 1360, 510, 1400], fill=BLUE); text(d, (525, 1380), "động năng", 40, INK, anchor="lm")
    text(d, (900, 1380), fj(ROWS[2][3]) + " J", 42, BLUE, alpha=appear(t, RT0 + RTS + 0.1))

# ---------------- canh 5: chua noi duoc + bay ----------------
SPC = 150                                        # px moi %
def s_trap(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    a = appear(t, 0.1)
    card(d, (60, 270, 1020, 520), fill=WHITE, outline=BLUE, w=6)
    text(d, (W / 2, 322), "Chưa nói được:", 46, BLUE, alpha=a)
    text(d, (W / 2, 404), "Chỉ một khối 0,20 kg.", 42, INK, alpha=a)
    text(d, (W / 2, 470), "Hụt đi đâu: chưa trả lời.", 42, INK, alpha=a)
    b = appear(t, M[1] - 0.05, 0.3)
    if b <= 0: return
    card(d, (60, 570, 1020, 1290), fill=A(WHITE, b), outline=A(RED, b), w=6)
    pre, q = "Bẫy: ", "“hụt do đọc sai”"
    pw, qw = tw(d, pre, F(44)), tw(d, q, F(44)); x0 = W / 2 - (pw + qw) / 2
    text(d, (x0, 640), pre, 44, RED, anchor="lm", alpha=b)
    text(d, (x0 + pw, 640), q, 44, INK, anchor="lm", alpha=b)
    x = appear(t, M[1] + 2.3, 0.3)
    if x > 0:
        d.line([(x0 + pw - 6, 642), (x0 + pw + qw + 6, 642)], fill=A(RED, x), width=6)
        text(d, (x0 + pw + qw + 24, 640), "✗", 48, RED, anchor="lm", alpha=x)
    for k, (lbl, lo, hi, col, s) in enumerate((("Sai số đọc v", 0.4, 0.7, PURPLE, "0,4–0,7 %"),
                                                ("Phần hụt", 3.0, 4.0, RED, "3–4 %"))):
        y = 720 + k * 170
        text(d, (110, y), lbl, 40, MUTED, anchor="lm", alpha=b)
        d.rectangle([110, y + 40, 110 + lo * SPC, y + 100], fill=A(col, b))
        d.rectangle([110 + lo * SPC, y + 40, 110 + hi * SPC, y + 100], fill=A(mix(col, WHITE, 0.55), b))
        text(d, (110 + hi * SPC + 20, y + 70), s, 42, col, anchor="lm", alpha=b)
    if x > 0:
        card(d, (100, 1080, 980, 1240), fill=A((220, 252, 231), x), r=26)
        text(d, (W / 2, 1160), "✓ Hụt lớn hơn nhiều: có thật", 44, GREEN, alpha=x)

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    def body(d, t, k1):
        # hinh nho: mang + khoi o h = 0,25 m (khong ghi so dap an)
        x0, y0, x1, y1 = 260, 1440, 820, 1180
        d.line([(160, y0 + 30), (920, y0 + 30)], fill=A(NAVY, k1), width=5)
        d.line([(x0, y1), (x1, y0), (900, y0)], fill=A((90, 98, 122), k1), width=14, joint="curve")
        u = ((x1 - x0) / math.hypot(x1 - x0, y0 - y1), (y0 - y1) / math.hypot(x1 - x0, y0 - y1)); n = (u[1], -u[0])
        bx, by = x0 + 0.12 * (x1 - x0), y1 + 0.12 * (y0 - y1); cx, cy = bx + n[0] * 30, by + n[1] * 30
        pts = [(cx + a * 44 * u[0] + b * 22 * n[0], cy + a * 44 * u[1] + b * 22 * n[1]) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        d.polygon(pts, fill=A(BLUE, k1), outline=A(NAVY, k1), width=3)
        dashed(d, (bx, by), (bx, y0), A(ORANGE, k1), w=4)
        arrow(d, (bx - 40, y0), (bx - 40, by + 6), A(ORANGE, k1), w=5, head=18)
        text(d, (bx - 60, (by + y0) / 2), "h = 0,25 m", 42, ORANGE, anchor="rm", alpha=k1)
        kh = appear(t, sc["M"][0] + 2.5, 0.5)
        if kh <= 0: return
        card(d, (110, 960, 970, 1080), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1020, "Gợi ý: xem lần thả 0,20 m và 0,30 m", 42, ORANGE, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Thế năng gần như thành hết động năng",
             "Thả từ 0,25 m: động năng ½mv² ở chân dốc khoảng bao nhiêu?", None, body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, cm, tr, e = sc["hook"], sc["do"], sc["cmp"], sc["trap"], sc["end"]
    out = [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + REL[i] + TS[i] + 0.06, "tap") for i in range(4)]
    out += [(cm["t0"] + cm["M"][1], "ding"), (tr["t0"] + tr["M"][1], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l9-conang-01", header="KHTN 9 · THÍ NGHIỆM", cues=_cues,
    footer="Cơ năng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Máng đệm khí nghiêng", draw=s_hook, tail=0.6, caps=[
   ("Khối trượt trên đệm khí.", 2.9),
   ("Dừng video, tự đoán.", 5.4)]),
 dict(key="do", title="Thả từ bốn độ cao", draw=s_do, tail=0.6, caps=[
   ("Thả nhẹ, cổng quang đo v.", 6.0),
   ("Thả càng cao, v càng lớn.", 2.6)]),
 dict(key="cmp", title="So thế năng và động năng", draw=s_cmp, tail=0.6, caps=[
   ("Tính cho cả bốn lần.", 3.0),
   ("Thanh động năng ngắn hơn chút.", 3.4)]),
 dict(key="rut", title="Thế năng thành động năng", draw=s_rut, tail=0.5, caps=[
   ("Thế năng giảm, động năng tăng.", 3.3),
   ("Tổng gần như không đổi.", 2.9)]),
 dict(key="trap", title="Giới hạn và cái bẫy", draw=s_trap, tail=0.5, caps=[
   ("Giới hạn của thí nghiệm.", 3.6),
   ("Đúng không? So hai thanh.", 4.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng lại, tự nghĩ.", 5.7)]),
])
