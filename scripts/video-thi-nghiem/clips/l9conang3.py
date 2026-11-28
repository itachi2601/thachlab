# Clip: tn-l9-conang-03 - Bong cao su nay thap dan: lan 2 nay len bao cao? (KHTN 9, lo 6, 18/11/2026)
# Dung lai theo cong moi 27/11/2026 (Viec 4 L9 nhom C): chu >= 56, canh <= 180 tu/phut, khoi chu cach >= 2,5 s, K10,
#   Bay = mot thanh (co nang + nhiet, am) tu giai thich, o ✓ >= 3 s; Chua noi = san khac thi sao (chua do).
#   Chot = ca tu suy ghi san trong kho so_lieu_mau.ghi_chu (tha 1,50 m, k = 0,8 -> lan 5 moi < 0,50 m; h0 1,50 trong dai tham_so).
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-conang-03.json:
#   tham_so: h0 = 1,00 m ; k = 0,8 ; m = 0,05 kg ; mo_hinh h_n = h0·k^n, W_n = 10·m·h_n
#   so_lieu_mau (lan, h m, W J): 0 1,00 0,5 ; 1 0,80 0,4 ; 2 0,64 0,32 ; 3 0,51 0,256 (ghi ≈ 0,26 vi 10·0,05·0,51 = 0,255)
# Chuyen dong: parabol roi tu do that (g = 9,8), chieu cham deu x2,5 (video quay cham), dung hinh o dinh lan nay 3
#   (khong chieu lan 4 de khoi lo ca cau chot).
# Canh: Du doan (bang da co lan 0, lan 1; lan 2 = ? ; K10) -> Tien hanh (tha, danh dau dinh, bang hien dung luc bong o dinh)
#   -> DAP AN · khoang 0,64 m (× 0,8 moi lan) -> Rut ra (cot co nang + phan thanh nhiet/am, tong 0,5 J)
#   -> Chua noi duoc + bay "nang luong mat di" ✗ -> Chot + THU NGHI (tha 1,50 m: lan 5 moi duoi 0,50 m, h5 ≈ 0,49 m).
# Lua chon Du doan (o khung web): A. 0,80 m (nhu lan 1) · B. 0,60 m (bot them 0,20 m) · C. Khoang 0,64 m (dung)
#   · D. 0,40 m (bang nua lan 1).
# Cau 5 (ngay truoc hop) hoi "bong nay thap dan, cau nao dung" -> HS da tra loi truoc khi xem; Cau 6 (goc the nang) khong dung toi.
from engine import *

G, H0, K, MKG, SLOW = 9.8, 1.0, 0.8, 0.05, 2.5
ROWS = [(0, 1.00, 0.5), (1, 0.80, 0.4), (2, 0.64, 0.32), (3, 0.51, 0.256)]
FLOOR, SPX, RX, BX, BR = 1180, 780, 200, 330, 30
BALL = (220, 38, 38); BALL_D = (140, 20, 20); RULER = (253, 246, 200); RULER_D = (170, 150, 60)
def fm(x, n=2): return f"{x:.{n}f}".replace(".", ",")
def yh(h): return FLOOR - h * SPX

# lich chuyen dong (giay video, tinh tu luc tha)
def _sched():
    ev = []; t = 0.0
    tf = math.sqrt(2 * H0 / G) * SLOW; ev.append(("fall", t, tf, H0)); t += tf
    for n in (1, 2, 3):
        h = H0 * K ** n; tu = math.sqrt(2 * h / G) * SLOW
        ev.append(("up", t, tu, h)); t += tu
        if n < 3: ev.append(("down", t, tu, h)); t += tu
    return ev
EV = _sched()
APEX = [e[1] + e[2] for e in EV if e[0] == "up"]          # moc dinh lan 1, 2, 3
T_STOP = APEX[2]                                          # dung hinh
def ball_h(tau):
    if tau <= 0: return H0
    if tau >= T_STOP: return H0 * K ** 3
    for kind, t0, d, h in EV:
        if t0 <= tau < t0 + d:
            s = (tau - t0) / SLOW
            if kind in ("fall", "down"): return max(0.0, h - 0.5 * G * s * s)
            return max(0.0, math.sqrt(2 * G * h) * s - 0.5 * G * s * s)
    return 0.0

def ruler(d, hmax=1.0):
    d.line([(90, FLOOR), (560, FLOOR)], fill=NAVY, width=8)
    for x in range(100, 560, 40): d.line([(x, FLOOR + 6), (x - 20, FLOOR + 26)], fill=GRAY, width=3)
    d.rectangle([RX - 16, yh(hmax) - 14, RX + 16, FLOOR], fill=RULER, outline=RULER_D, width=3)
    for k in range(0, int(round(hmax * 10)) + 1):
        y = yh(k / 10); L = 22 if k % 2 == 0 else 12
        d.line([(RX + 16 - L, y), (RX + 16, y)], fill=NAVY, width=3)
        if k % 5 == 0 and k > 0: text(d, (RX - 26, y), fm(k / 10, 1), 56, NAVY, anchor="rm")

def ball(d, h, alpha=1.0):
    y = yh(h) - BR
    dot(d, BX, y, BR, A(BALL, alpha), outline=A(BALL_D, alpha))

def mark(d, h, label, col, alpha=1.0):
    y = yh(h)
    d.line([(RX + 16, y), (BX + 50, y)], fill=A(col, alpha), width=5)
    text(d, (BX + 60, y), label, 56, col, anchor="lm", alpha=alpha)

def table(d, shown, x0=560, x1=1040, y0=330, q_row=None, alpha=1.0):
    nrow = 4
    card(d, (x0, y0, x1, y0 + 100 + nrow * 84), fill=A(WHITE, alpha), outline=A(NAVY, alpha), w=4)
    cx = (x0 + 80, x0 + 250)
    text(d, (cx[0] - 10, y0 + 48), "Lần", 56, NAVY, alpha=alpha); text(d, (cx[1], y0 + 48), "h (m)", 56, ORANGE, alpha=alpha)
    d.line([(x0 + 20, y0 + 92), (x1 - 20, y0 + 92)], fill=A(LIGHT, alpha), width=4)
    for i, (n, h, w) in enumerate(ROWS):
        y = y0 + 138 + i * 84; a = shown[i] if i < len(shown) else 0
        if q_row == i:
            text(d, (cx[0] - 10, y), str(n), 56, INK, alpha=alpha); text(d, (cx[1], y), "?", 60, PURPLE, alpha=alpha); continue
        if a <= 0: continue
        text(d, (cx[0] - 10, y), "thả" if n == 0 else str(n), 56, INK, alpha=a * alpha)
        text(d, (cx[1], y), fm(h), 56, ORANGE, alpha=a * alpha)

DRED = (185, 28, 28); DGREEN = (21, 110, 55); HEAT = (254, 202, 202)
def pill(d, s, y, a, color, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    ruler(d); ball(d, H0)
    mark(d, 0.80, "lần 1", BLUE)
    table(d, [1, 1], q_row=2)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1230 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 350), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    text(d, (W / 2, y0 + 160), "Lần 2 nảy lên bao cao?", 58, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p_ = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 230, 970, y0 + 315], radius=42, fill=A((237, 233, 254), a))
        if p_ < 1: d.rounded_rectangle([110, y0 + 230, 110 + max(85, 860 * (1 - p_)), y0 + 315], radius=42, fill=A((76, 29, 149), a))

# ---------------- canh 2: tien hanh ----------------
RL = 0.6
def row_at(i): return 0.0 if i == 0 else RL + APEX[i - 1]
def s_do(img, d, t, sc):
    IMG_REF[0] = img
    tau = t - RL
    ruler(d)
    for i in (1, 2, 3):
        if t >= row_at(i): mark(d, ROWS[i][1], f"lần {i}", BLUE, alpha=appear(t, row_at(i), 0.2))
    ball(d, ball_h(tau))
    table(d, [appear(t, row_at(i), 0.3) if i else 1 for i in range(4)])
    card(d, (60, 1270, 1020, 1380), fill=WHITE, outline=LIGHT, r=26, w=4)
    text(d, (W / 2, 1325), "quay chậm, đọc đỉnh", 56, INK)
    if tau >= T_STOP:
        a = appear(t, RL + T_STOP, 0.3)
        pill(d, "dừng hình", 1470, a, NAVY)

# ---------------- canh 3: dap an ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    ruler(d)
    for i in (1, 2, 3): mark(d, ROWS[i][1], f"lần {i}", BLUE)
    ball(d, ROWS[3][1], alpha=0.5)
    table(d, [1, 1, 1, 1])
    for i in (1, 2, 3):
        y = 330 + 138 + i * 84
        aa = appear(t, M[0] + 0.3 + 0.5 * (i - 1), 0.4)
        text(d, (960, y), "× 0,8", 56, DGREEN, alpha=aa)
    a2 = appear(t, M[1] - 0.1, 0.4)
    if a2 > 0:
        pill(d, "ĐÁP ÁN: khoảng 0,64 m", 1290, a2, GREEN, 58)
    text(d, (W / 2, 1420), "mỗi lần còn khoảng 80 %", 58, DGREEN, alpha=appear(t, M[1] + 2.5, 0.4))

# ---------------- canh 4: rut ra - cot co nang ----------------
CB0, CPX = 1050, 1300
def s_rut(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    d.line([(90, CB0), (1000, CB0)], fill=NAVY, width=5)
    ytop = CB0 - 0.5 * CPX
    for i, (n, h, w) in enumerate(ROWS):
        x = 130 + i * 215; g = ease((t - 0.3 - 0.35 * i) / 0.5)
        text(d, (x + 90, CB0 + 50), "thả" if n == 0 else f"lần {n}", 56, INK)
        if g <= 0: continue
        hb = w * CPX * g
        if hb > 2: d.rectangle([x, CB0 - hb, x + 180, CB0], fill=BLUE)
        lost = appear(t, M[1] - 0.1 + 0.3 * i, 0.5) if i else 0
        top = CB0 - w * CPX
        if lost > 0 and top - ytop > 2:
            d.rectangle([x, top - (top - ytop) * lost, x + 180, top], fill=HEAT, outline=RED, width=3)
        text(d, (x + 90, CB0 - hb + 40), ("≈ 0,26" if n == 3 else fm(w, 2 if n == 2 else 1)), 56, WHITE, alpha=clamp(g * 2 - 1))
    k = 1.0
    for xx in range(90, 1000, 30): d.line([(xx, ytop), (xx + 16, ytop)], fill=A(NAVY, k), width=4)
    text(d, (1000, ytop - 40), "0,5 J lúc thả", 56, NAVY, anchor="rm", alpha=k)
    kk = appear(t, M[1] - 0.1, 0.4)
    card(d, (40, 1170, 1040, 1420), fill=A(WHITE, k), outline=A(LIGHT, k), r=26, w=4)
    d.rectangle([100, 1220, 150, 1270], fill=A(BLUE, k)); text(d, (175, 1245), "cơ năng (J)", 56, INK, anchor="lm", alpha=k)
    d.rectangle([100, 1320, 150, 1370], fill=A(HEAT, kk), outline=A(RED, kk), width=3)
    text(d, (175, 1345), "thành nhiệt, âm thanh", 56, DRED, anchor="lm", alpha=kk)

# ---------------- canh 5: bay + chua noi duoc ----------------
BAY_ST = 2.2
def s_trap(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    a = appear(t, 0.2, 0.4)
    k2 = appear(t, M[2] - 0.1, 0.45)
    # hinh tu giai thich: thanh lan 3 = co nang 0,256 J + phan thanh nhiet, am; tong 0,5 J (thanh moc dan)
    card(d, (40, 260, 1040, 700), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    x0, x1, y0b, y1b = 90, 990, 360, 470
    g1 = ease((t - 0.3) / 0.8); g2 = ease((t - 1.1) / 0.8)
    xw = x0 + (x1 - x0) * 0.256 / 0.5
    if g1 > 0: d.rectangle([x0, y0b, x0 + (xw - x0) * g1, y1b], fill=A(BLUE, a))
    if g2 > 0: d.rectangle([xw, y0b, xw + (x1 - xw) * g2, y1b], fill=A(HEAT, a), outline=A(RED, a), width=3)
    text(d, ((x0 + xw) / 2, y0b - 50), "cơ năng", 56, BLUE, alpha=a)
    text(d, ((xw + x1) / 2, y0b - 50), "nhiệt, âm", 56, DRED, alpha=a)
    for xx in (x0, x1): d.line([(xx, y1b + 20), (xx, y1b + 60)], fill=A(NAVY, a), width=4)
    d.line([(x0, y1b + 40), (x1, y1b + 40)], fill=A(NAVY, a), width=4)
    text(d, (W / 2, y1b + 120), "sau lần nảy 3: tổng vẫn 0,5 J", 58, NAVY, alpha=a)
    a1 = a * (1 - k2); y0 = 760
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y0 + 62, a1, DRED)
        q = "“Năng lượng mất đi”"; yy = y0 + 190; lw = tw(d, q, F(60))
        text(d, (W / 2, yy), q, 60, INK, alpha=a1)
        ks = clamp((t - BAY_ST) / 0.4)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=7)
        kk = a1 * appear(t, M[1] + 0.1, 0.4)
        card(d, (70, y0 + 310, 1010, y0 + 470), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 390), "✓ Chỉ đổi dạng", 60, DGREEN, alpha=kk)
    if k2 > 0:
        card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 110), "Chưa nói được:", 60, NAVY, alpha=k2)
        text(d, (W / 2, y0 + 220), "sàn khác thì sao", 60, INK, alpha=k2)
        text(d, (W / 2, y0 + 320), "(chưa đo)", 56, NAVY, alpha=k2)

# ---------------- canh 6: chot ----------------
END_Q = 0.2
CH_H0, CH_LIM = 1.50, 0.55          # h1..h5 = 1,20; 0,96; 0,77; 0,61; 0,49 -> lan 5 (khong hien). GĐ2: nguong 0,55 (cach lan 4 va lan 5 ro, kiem-code 27/11)
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 280, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 350, k1, ORANGE)
    text(d, (W / 2, 465), "Bóng, sàn như cũ.", 58, INK, alpha=k1)
    text(d, (W / 2, 550), "Lần nảy thứ mấy", 58, INK, alpha=k1)
    text(d, (W / 2, 635), "mới thấp hơn " + fm(CH_LIM) + " m?", 58, INK, alpha=k1)
    if k1 <= 0: return
    fl, sp, rx, bx = 1480, 480, 250, 360
    d.line([(150, fl), (950, fl)], fill=A(NAVY, k1), width=6)
    d.rectangle([rx - 14, fl - CH_H0 * sp - 10, rx + 14, fl], fill=A(RULER, k1), outline=A(RULER_D, k1), width=3)
    dot(d, bx, fl - CH_H0 * sp - 26, 26, A(BALL, k1), outline=A(BALL_D, k1))
    text(d, (bx + 46, fl - CH_H0 * sp - 26), "thả từ " + fm(CH_H0) + " m", 56, BALL_D, anchor="lm", alpha=k1)
    for xx in range(rx + 14, 700, 26): d.line([(xx, fl - CH_LIM * sp), (xx + 14, fl - CH_LIM * sp)], fill=A(BLUE, k1), width=5)
    text(d, (720, fl - CH_LIM * sp), fm(CH_LIM) + " m", 56, BLUE, anchor="lm", alpha=k1)
    rr = 60 + 30 * math.sin(2 * math.pi * t / 2.0)
    xc, yc = 560, fl - 1.0 * sp
    d.ellipse([xc - rr, yc - rr, xc + rr, yc + rr], fill=A(mix(ORANGE, WHITE, 0.45), k1))
    text(d, (xc, yc), "?", 80, WHITE, alpha=k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + row_at(i), "tap") for i in (1, 2, 3)]
    out += [(an["t0"] + an["M"][1] - 0.1, "ding"), (tr["t0"] + BAY_ST, "buzz"), (tr["t0"] + tr["M"][1] + 0.1, "tap"),
            (e["t0"] + END_Q + 0.1, "open")]
    return sorted(out)

CLIP = dict(id="tn-l9-conang-03", header="KHTN 9 · THÍ NGHIỆM", cues=_cues,
    footer="Cơ năng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Bóng cao su nảy trên sàn", draw=s_hook, tail=0.3, caps=[
   ("Bóng 50 g cạnh thước.", 2.5),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Thả từ 1,00 m", draw=s_do, tail=0.3, caps=[
   ("Đánh dấu đỉnh mỗi lần nảy.", 3.6),
   ("Ba lần nảy đầu.", 3.0)]),
 dict(key="ans", title="So mỗi lần với lần trước", draw=s_ans, tail=0.8, caps=[
   ("Chia lần sau cho lần trước.", 3.0),
   ("Không bớt đều.", 3.4)]),
 dict(key="rut", title="Cơ năng đi đâu?", draw=s_rut, tail=0.4, caps=[
   ("Chạm sàn: cơ năng giảm.", 2.9),
   ("Phần giảm không biến mất.", 2.9)]),
 dict(key="trap", title="Bẫy và giới hạn", draw=s_trap, tail=0.3, caps=[
   ("Đúng không?", 4.4),
   ("Nhìn cả thanh.", 3.4),
   ("Còn bỏ ngỏ.", 2.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Tự nghĩ.", 6.2)]),
])
