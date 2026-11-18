# Clip: tn-l9-conang-03 - Bong cao su nay thap dan: lan 2 nay len bao cao? (KHTN 9, lo 6, 18/11/2026)
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
FLOOR, SPX, RX, BX, BR = 1260, 860, 200, 330, 30
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
        if k % 2 == 0 and k > 0: text(d, (RX - 30, y), fm(k / 10, 1), 40, MUTED, bold=False, anchor="rm")

def ball(d, h, alpha=1.0):
    y = yh(h) - BR
    dot(d, BX, y, BR, A(BALL, alpha), outline=A(BALL_D, alpha))

def mark(d, h, label, col, alpha=1.0):
    y = yh(h)
    d.line([(RX + 16, y), (BX + 50, y)], fill=A(col, alpha), width=5)
    text(d, (BX + 64, y), label, 40, col, anchor="lm", alpha=alpha)

def table(d, shown, x0=560, x1=1040, y0=330, q_row=None, alpha=1.0):
    nrow = 4
    card(d, (x0, y0, x1, y0 + 100 + nrow * 84), fill=A(WHITE, alpha), outline=A(NAVY, alpha), w=4)
    cx = (x0 + 70, x0 + 210)
    text(d, (cx[0] - 10, y0 + 48), "Lần", 40, NAVY, alpha=alpha); text(d, (cx[1], y0 + 48), "h (m)", 40, ORANGE, alpha=alpha)
    d.line([(x0 + 20, y0 + 92), (x1 - 20, y0 + 92)], fill=A(LIGHT, alpha), width=4)
    for i, (n, h, w) in enumerate(ROWS):
        y = y0 + 138 + i * 84; a = shown[i] if i < len(shown) else 0
        if q_row == i:
            text(d, (cx[0] - 10, y), str(n), 42, INK, alpha=alpha); text(d, (cx[1], y), "?", 44, PURPLE, alpha=alpha); continue
        if a <= 0: continue
        text(d, (cx[0] - 10, y), "thả" if n == 0 else str(n), 42, INK, alpha=a * alpha)
        text(d, (cx[1], y), fm(h), 44, ORANGE, alpha=a * alpha)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    ruler(d); ball(d, H0)
    text(d, (BX + 50, yh(H0) - BR), "50 g", 40, BALL_D, anchor="lm")
    mark(d, 0.80, "lần 1", BLUE)
    table(d, [1, 1], q_row=2)
    k = appear(t, sc["M"][1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (60, 1310, 1020, 1660), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 1365), "Dự đoán", 46, PURPLE, alpha=k)
    ctext(d, 1450, "Lần 2 bóng nảy lên khoảng bao cao?", 44, INK, alpha=k)
    text(d, (W / 2, 1535), "Chọn đáp án ở khung câu hỏi", 40, MUTED, bold=False, alpha=appear(t, sc["M"][1] + 0.2))
    t1, t2 = sc["M"][1] + 0.6, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1606, 940, 1620], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1606, 140 + 800 * (1 - q), 1620], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh ----------------
RL = 0.6                                      # moc tha trong canh
def row_at(i): return 0.0 if i == 0 else RL + APEX[i - 1]
def s_do(img, d, t, sc):
    IMG_REF[0] = img
    tau = t - RL
    ruler(d)
    for i in (1, 2, 3):
        if t >= row_at(i): mark(d, ROWS[i][1], f"lần {i}", BLUE, alpha=appear(t, row_at(i), 0.2))
    ball(d, ball_h(tau))
    table(d, [appear(t, row_at(i), 0.3) if i else 1 for i in range(4)])
    if tau >= T_STOP:
        a = appear(t, RL + T_STOP, 0.3)
        card(d, (660, 800, 940, 870), fill=A(NAVY, a), r=30)
        text(d, (800, 835), "dừng hình", 40, WHITE, alpha=a)
    card(d, (60, 1340, 1020, 1440), fill=WHITE, outline=LIGHT, r=26, w=4)
    text(d, (W / 2, 1390), "Thả từ 1,00 m · quay chậm, đọc đỉnh", 42, INK)

# ---------------- canh 3: dap an ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    ruler(d)
    for i in (1, 2, 3): mark(d, ROWS[i][1], f"lần {i}", BLUE)
    ball(d, ROWS[3][1], alpha=0.5)
    table(d, [1, 1, 1, 1])
    a = appear(t, M[0] + 0.3, 0.4)
    for i in (1, 2, 3):
        y = 330 + 138 + i * 84
        aa = appear(t, M[0] + 0.3 + 0.5 * (i - 1), 0.4)
        text(d, (940, y), "× 0,8", 40, GREEN, alpha=aa)
    a2 = appear(t, M[1] - 0.1, 0.4)
    if a2 > 0:
        card(d, (110, 1340, 970, 1450), fill=A(GREEN, a2), r=50)
        text(d, (W / 2, 1395), "ĐÁP ÁN · khoảng 0,64 m", 46, WHITE, alpha=a2)
        text(d, (W / 2, 1530), "mỗi lần còn khoảng 80 % lần trước", 42, GREEN, alpha=appear(t, M[1] + 0.6, 0.4))

# ---------------- canh 4: rut ra - cot co nang ----------------
CB0, CPX = 1100, 1300                         # day cot, px moi J (0,5 J -> 650 px)
def s_rut(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    text(d, (W / 2, 300), "Cơ năng W = 10mh  (m = 0,05 kg)", 42, INK)
    d.line([(90, CB0), (1000, CB0)], fill=NAVY, width=5)
    ytop = CB0 - 0.5 * CPX
    for i, (n, h, w) in enumerate(ROWS):
        x = 160 + i * 215; g = ease((t - 0.3 - 0.35 * i) / 0.5)
        if g <= 0: continue
        hb = w * CPX * g
        if hb > 2: d.rectangle([x, CB0 - hb, x + 130, CB0], fill=BLUE)
        lost = appear(t, M[1] - 0.1 + 0.3 * i, 0.5) if i else 0
        top = CB0 - w * CPX
        if lost > 0 and top - ytop > 2:
            d.rectangle([x, top - (top - ytop) * lost, x + 130, top], fill=(254, 202, 202), outline=RED, width=3)
        lab = "thả" if n == 0 else f"lần {n}"
        text(d, (x + 65, CB0 + 40), lab, 40, INK, alpha=g)
        text(d, (x + 65, CB0 - hb + 34), ("≈ 0,26" if n == 3 else fm(w, 2 if n == 2 else 1)), 40, WHITE, alpha=clamp(g * 2 - 1))
    k = appear(t, 0.3, 0.5)
    for xx in range(90, 1000, 30): d.line([(xx, ytop), (xx + 16, ytop)], fill=A(NAVY, k), width=4)
    text(d, (1000, ytop - 34), "0,5 J lúc thả", 40, NAVY, anchor="rm", alpha=k)
    kk = appear(t, M[1] - 0.1, 0.4)
    card(d, (60, 1190, 1020, 1400), fill=A(WHITE, k), outline=A(LIGHT, k), r=26, w=4)
    d.rectangle([110, 1240, 150, 1280], fill=A(BLUE, k)); text(d, (170, 1260), "cơ năng của bóng (J)", 40, INK, anchor="lm", alpha=k)
    d.rectangle([110, 1320, 150, 1360], fill=A((254, 202, 202), kk), outline=A(RED, kk), width=3)
    text(d, (170, 1340), "thành nhiệt năng, âm thanh", 40, RED, anchor="lm", alpha=kk)

# ---------------- canh 5: chua noi duoc + bay ----------------
def s_trap(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    a = appear(t, 0.1)
    card(d, (60, 270, 1020, 470), fill=WHITE, outline=BLUE, w=6)
    text(d, (W / 2, 325), "Chưa nói được:", 46, BLUE, alpha=a)
    text(d, (W / 2, 405), "Số liệu minh hoạ.", 42, INK, alpha=a)
    b = appear(t, M[1] - 0.05, 0.3)
    if b <= 0: return
    x = appear(t, M[1] + 2.3, 0.3)
    card(d, (60, 590, 1020, 1160 if x > 0 else 760), fill=A(WHITE, b), outline=A(RED, b), w=6)
    text(d, (W / 2, 650), "Bẫy:", 44, RED, alpha=b)
    q = "“Năng lượng của bóng mất đi”"; qw = tw(d, q, F(44))
    text(d, (W / 2, 715), q, 44, INK, alpha=b)
    if x <= 0: return
    d.line([(W / 2 - qw / 2 - 6, 717), (W / 2 + qw / 2 + 6, 717)], fill=A(RED, x), width=6)
    text(d, (W / 2 + qw / 2 + 30, 715), "✗", 48, RED, anchor="lm", alpha=x)
    # thanh: lan 3 = co nang 0,256 + phan da thanh nhiet = 0,5 J
    x0, x1, y0, y1 = 120, 960, 800, 880
    xw = x0 + (x1 - x0) * 0.256 / 0.5
    d.rectangle([x0, y0, xw, y1], fill=A(BLUE, x))
    d.rectangle([xw, y0, x1, y1], fill=A((254, 202, 202), x), outline=A(RED, x), width=3)
    text(d, ((x0 + xw) / 2, y0 + 40), "cơ năng", 40, WHITE, alpha=x)
    text(d, ((xw + x1) / 2, y0 + 40), "nhiệt, âm", 40, RED, alpha=x)
    text(d, (W / 2, 950), "cộng lại vẫn 0,5 J", 42, NAVY, alpha=x)
    text(d, (W / 2, 1060), "✓ Chỉ đổi sang dạng khác", 44, GREEN, alpha=x)

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    def body(d, t, k1):
        # hinh nho: thuoc + bong o 1,50 m + vach 0,50 m (khong ve lan nay nao)
        fl, sp, rx, bx = 1280, 210, 330, 420
        d.line([(230, fl), (700, fl)], fill=A(NAVY, k1), width=6)
        d.rectangle([rx - 12, fl - 1.5 * sp - 10, rx + 12, fl], fill=A(RULER, k1), outline=A(RULER_D, k1), width=3)
        dot(d, bx, fl - 1.5 * sp - 24, 24, A(BALL, k1), outline=A(BALL_D, k1))
        text(d, (bx + 40, fl - 1.5 * sp - 24), "thả từ 1,50 m", 40, BALL_D, anchor="lm", alpha=k1)
        for xx in range(rx + 12, 760, 26): d.line([(xx, fl - 0.5 * sp), (xx + 14, fl - 0.5 * sp)], fill=A(BLUE, k1), width=4)
        text(d, (790, fl - 0.5 * sp), "0,50 m", 40, BLUE, anchor="lm", alpha=k1)
        kh = appear(t, sc["M"][0] + 2.6, 0.5)
        if kh <= 0: return
        card(d, (110, 1300, 970, 1470), fill=A((255, 237, 213), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1345), "Gợi ý", 40, ORANGE, alpha=kh)
        ctext(d, 1415, "Bóng, sàn như cũ", 42, INK, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Cơ năng giảm, năng lượng vẫn bảo toàn",
             "Lần nảy thứ mấy bóng lên thấp hơn 0,50 m?", None, body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.5, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + row_at(i), "tap") for i in (1, 2, 3)]
    out += [(an["t0"] + an["M"][1] - 0.1, "ding"), (tr["t0"] + tr["M"][1], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l9-conang-03", header="KHTN 9 · THÍ NGHIỆM", cues=_cues,
    footer="Cơ năng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Bóng cao su nảy trên sàn", draw=s_hook, tail=0.6, caps=[
   ("Bóng 50 g cạnh thước dựng đứng.", 2.6),
   ("Nghĩ kĩ rồi mới xem tiếp.", 5.6)]),
 dict(key="do", title="Thả rồi đọc độ cao đỉnh", draw=s_do, tail=0.6, caps=[
   ("Đánh dấu đỉnh mỗi lần nảy.", 3.6),
   ("Ba lần nảy đầu.", 3.8)]),
 dict(key="ans", title="So mỗi lần với lần trước", draw=s_ans, tail=0.6, caps=[
   ("Chia lần sau cho lần trước.", 2.8),
   ("Không bớt đều mà còn 80 %.", 3.4)]),
 dict(key="rut", title="Cơ năng đi đâu?", draw=s_rut, tail=0.5, caps=[
   ("Mỗi lần chạm sàn, cơ năng giảm.", 3.2),
   ("Phần giảm không biến mất.", 3.2)]),
 dict(key="trap", title="Giới hạn và cái bẫy", draw=s_trap, tail=0.5, caps=[
   ("Giới hạn của thí nghiệm.", 3.2),
   ("Đúng không? Nhìn thanh dưới.", 4.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Tự trả lời trước khi xem.", 6.0)]),
])
