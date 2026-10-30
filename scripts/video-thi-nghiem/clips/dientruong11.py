# Clip: tn-l11-dien-truong-02 - Can dien tu "can" luc dien: E = F/q khong phu thuoc dien tich thu (30/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dien-truong-02.json:
#   so_lieu_mau (r cm, q nC, dm g, E do 10^5 V/m): 3 10 0,41 4,02 ; 4 10 0,23 2,25 ; 6 10 0,10 0,98 ; 4 5 0,12 2,35
#   tham_so: Q = 40 nC, g = 9,8 m/s2, can chia 0,01 g, q 2-20 nC (cau hoi chot dung q = 20 nC, chua tung hien tren man).
#   rut_ra: lan 2 va lan 4 lech 4 %, nam trong sai so doc can.
# Canh: Du doan (K10: chi cau hoi + hinh; q 10 -> 5 nC o r = 4 cm, E thay doi the nao?) -> Tien hanh (r = 3, 4, 6 cm
#       roi cham qua cau trung hoa, q con 5 nC, do lai o 4 cm; bang r - q - dm - E?) -> Dap an C (cot dm giam nua,
#       cot E gan bang; bang E; r gap doi E giam ~4 lan) -> Bay (2,25 khac 2,35 -> "E phu thuoc q") roi Chua noi duoc
#       -> Chot + cau hoi tu nho lai (q = 20 nC o 4 cm: can tang bao nhieu gam).
# Hai qua cau cung dau (+): Q o tren day q xuong -> luc dien tren q huong xuong, so chi can tang (dung vat li).
# Clip coulomb2 (luc theo r) lam song song: clip nay nhan E = F/q, khong ve do thi F theo r.
from engine import *

ROWS = [(3, 10, 0.41, 4.02), (4, 10, 0.23, 2.25), (6, 10, 0.10, 0.98), (4, 5, 0.12, 2.35)]   # so_lieu_mau
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
CHG = (220, 60, 60); NEU = (160, 165, 180); ROD = (214, 190, 140); DRED = (185, 28, 28)

# ---------------- dung cu (khung nguon 1080x1920) ----------------
BX, PAN_Y, PXCM = 380, 800, 55            # truc qua cau, mat dia can, px / cm
YQ = PAN_Y - 120                           # tam qua cau thu q (tren chan cach dien dat tren dia can)
STAND_X = 880                              # gia kep ben phai
def yQ(r): return YQ - r * PXCM            # tam qua cau Q o khoang cach r (cm) phia tren q

def ball(d, x, y, col, sign="+", R=30, alpha=1.0):
    d.ellipse([x - R, y - R, x + R, y + R], fill=A(col, alpha), outline=A(NAVY, alpha), width=3)
    d.ellipse([x - R * 0.55, y - R * 0.65, x - R * 0.05, y - R * 0.2], fill=A(WHITE, 0.45 * alpha))
    if sign: text(d, (x, y + 2), sign, 40, WHITE, alpha=alpha)

def rig(d, r, q, reading, dm=None, show_r=True, neu_x=None):
    """Can + qua cau q tren chan cach dien + qua cau Q treo tren gia kep, cach r (cm). dm: ve mui ten F ti le dm."""
    # can dien tu
    d.rectangle([BX - 150, PAN_Y, BX + 150, PAN_Y + 16], fill=(200, 205, 215), outline=NAVY, width=3)
    d.rectangle([BX - 10, PAN_Y + 16, BX + 10, PAN_Y + 34], fill=(120, 125, 140))
    card(d, (BX - 220, PAN_Y + 34, BX + 220, PAN_Y + 210), fill=(70, 78, 100), r=22)
    card(d, (BX - 160, PAN_Y + 58, BX + 160, PAN_Y + 148), fill=(220, 240, 225), r=12)
    text(d, (BX, PAN_Y + 103), reading, 50, (20, 60, 30))
    text(d, (BX, PAN_Y + 182), "cân điện tử", 36, WHITE, bold=False)
    # chan cach dien + q
    d.rectangle([BX - 7, YQ + 28, BX + 7, PAN_Y], fill=ROD, outline=NAVY, width=2)
    ball(d, BX, YQ, CHG)
    text(d, (BX + 48, YQ - 22), f"q = {q} nC", 40, INK, anchor="lm")
    # gia kep + Q
    y = yQ(r)
    d.rectangle([STAND_X - 8, 270, STAND_X + 8, PAN_Y + 210], fill=(110, 115, 130))
    d.rectangle([STAND_X - 90, PAN_Y + 200, STAND_X + 90, PAN_Y + 222], fill=NAVY)
    d.rectangle([BX - 7, y - 80, STAND_X, y - 66], fill=ROD, outline=NAVY, width=2)
    d.rectangle([STAND_X - 20, y - 96, STAND_X + 20, y - 50], fill=NAVY)
    d.rectangle([BX - 7, y - 80, BX + 7, y - 28], fill=ROD, outline=NAVY, width=2)
    ball(d, BX, y, CHG)
    text(d, (BX + 48, y + 6), "Q = 40 nC", 40, INK, anchor="lm")
    if show_r:
        xa = BX - 70
        arrow(d, ((xa, (y + YQ) / 2)), (xa, y + 4), MUTED, w=3, head=14)
        arrow(d, ((xa, (y + YQ) / 2)), (xa, YQ - 4), MUTED, w=3, head=14)
        text(d, (xa - 18, (y + YQ) / 2), f"r = {r} cm", 40, INK, anchor="rm")
    if dm:                                     # luc day cua Q len q: huong xuong
        L = 100 * dm / 0.41
        arrow(d, (BX + 48, YQ + 16), (BX + 48, YQ + 16 + max(L, 26)), RED, w=6, head=18)
        text(d, (BX + 74, YQ + 16 + max(L, 26) / 2 + 4), "F", 40, RED, anchor="lm")
    if neu_x is not None:                      # qua cau y het khong mang dien, cam bang thanh cach dien tu trai
        d.rectangle([-20, YQ - 7, max(-20, neu_x - 28), YQ + 7], fill=ROD, outline=NAVY, width=2)
        ball(d, neu_x, YQ, NEU, sign=None)

def table(d, n, e=0, y=1060, hl=(), ka=1.0):
    """Bang r - q - dm - E; n hang da co; e = so hang da hien cot E (con lai '?')."""
    card(d, (40, y, 1040, y + 460), fill=WHITE, outline=NAVY, w=4)
    xs = (165, 375, 590, 860)
    for x, c in zip(xs, ("r (cm)", "q (nC)", "Δm (g)", "E (×10⁵ V/m)")): text(d, (x, y + 50), c, 38, INK)
    d.line([(70, y + 88), (1010, y + 88)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 140 + i * 88; r, q, dm, E = ROWS[i]
        if i in hl: d.rounded_rectangle([60, yy - 38, 1020, yy + 38], radius=18, fill=A((255, 237, 213), ka))
        text(d, (xs[0], yy), str(r), 44, INK); text(d, (xs[1], yy), str(q), 44, INK)
        text(d, (xs[2], yy), vn(dm), 44, INK)
        if i < e: text(d, (xs[3], yy), vn(E), 46, BLUE)
        else: text(d, (xs[3], yy), "?", 44, GRAY)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong ve nut lua chon) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, 4, 10, "… g", show_r=True)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1050 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 520), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 250, "Giữ r = 4 cm, cho q từ\n10 nC còn 5 nC. E = F/q\nđo được thay đổi thế nào?", 46, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.6
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 470, 940, y0 + 482], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 470, 140 + 800 * (1 - p), y0 + 482], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
# ba vi tri r (moi vi tri: Q di chuyen 0,6 s, so can hien sau 0,1 s, hang bang them sau 0,4 s)
STEPS = [(0.4, 3), (2.5, 4), (4.6, 6)]
def s_do(img, d, t, sc):
    M = sc["M"]; tt = M[1]                     # moc cham qua cau trung hoa
    # r hien tai
    r, reading, dm, n = 8.0, "0,00 g", None, 0
    for i, (ts, rr) in enumerate(STEPS):
        if t >= ts:
            r0 = 8.0 if i == 0 else STEPS[i - 1][1]
            r = lerp(r0, rr, ease((t - ts) / 0.6))
            if t >= ts + 0.7: reading, dm = vn(ROWS[i][2]) + " g", ROWS[i][2]
            else: reading, dm = "… g", None
            if t >= ts + 1.0: n = i + 1
    q, neu = 10, None
    if t >= tt + 0.2:                          # qua cau trung hoa tien vao cham q roi lui ra
        u = t - tt - 0.2
        nx = lerp(-60, BX - 60, ease(u / 0.6)) if u < 1.3 else lerp(BX - 60, -60, ease((u - 1.3) / 0.6))
        if u < 2.0: neu = nx
        if u >= 0.65: q = 5
    if t >= tt + 2.2:                          # ha Q tu 6 cm xuong 4 cm
        r = lerp(6, 4, ease((t - tt - 2.2) / 0.6))
        reading, dm = ("… g", None) if t < tt + 2.9 else (vn(ROWS[3][2]) + " g", ROWS[3][2])
        if t >= tt + 3.2: n = 4
    elif t >= tt:
        reading, dm = "… g", None
    settled = abs(r - round(r)) < 0.02 and round(r) in (3, 4, 6)   # chi ghi nhan r khi Q da dung yen (3, 4, 6 cm)
    rig(d, round(r) if settled else r, q, reading, dm, show_r=settled, neu_x=neu)
    table(d, n)

# ---------------- canh 3: Dap an + rut ra ----------------
BASE_Y, BAR_H = 860, 400                       # cot: dm thang 0-0,30 g ; E thang 0-3,0 (x10^5 V/m)
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · gần như không đổi"
    pw = tw(d, lab, F(38)) + 52
    card(d, (W - 60 - pw, 236, W - 60, 296), fill=A(NAVY, ka), r=30)
    text(d, (W - 60 - pw / 2, 266), lab, 38, WHITE, alpha=ka)
    card(d, (40, 320, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    # chu giai mau
    for x, col, s in ((130, BLUE, "q = 10 nC"), (560, ORANGE, "q = 5 nC")):
        d.rounded_rectangle([x, 346, x + 34, 380], radius=6, fill=col)
        text(d, (x + 50, 363), s, 38, INK, anchor="lm")
    d.line([(90, BASE_Y), (990, BASE_Y)], fill=NAVY, width=4)
    groups = ((300, "Δm (g)", ROWS[1][2], ROWS[3][2], 0.30, "÷ 2"),
              (760, "E (×10⁵ V/m)", ROWS[1][3], ROWS[3][3], 3.0, "≈ bằng nhau"))
    for gi, (cx, name, v10, v5, top, ann) in enumerate(groups):
        text(d, (cx, BASE_Y + 46), name, 38, INK)
        for j, (v, col) in enumerate(((v10, BLUE), (v5, ORANGE))):
            k = appear(t, 0.3 + 0.5 * gi + 0.2 * j, 0.5)
            if k <= 0: continue
            h = BAR_H * v / top * k; x0 = cx - 125 + j * 135
            d.rectangle([x0, BASE_Y - h, x0 + 110, BASE_Y], fill=col)
            if k >= 1: text(d, (x0 + 55, BASE_Y - h - 28), vn(v), 38, INK)
        kn = appear(t, 1.4 + 0.4 * gi, 0.4)
        if kn > 0: text(d, (cx, 430), ann, 42, (154, 52, 18), alpha=kn)
    text(d, (W / 2, 1012), "E = F/q = Δm·g/q", 44, NAVY, alpha=appear(t, 0.2, 0.4))
    hl = (1, 3) if t < M[1] - 0.1 else (0, 2)
    table(d, 4, e=4, y=1060, hl=hl)

# ---------------- canh 4: Bay roi Chua noi duoc (khong hien cung luc) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.0, 0.3) * (1 - k2)
    rig(d, 4, 5, vn(ROWS[3][2]) + " g", ROWS[3][2], show_r=False)
    if a1 > 0:
        y0 = 1050
        card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
        text(d, (W / 2, y0 + 170), "2,25 ≠ 2,35", 46, DRED, alpha=a1)
        q = "“E phụ thuộc q”"            # chi gach dong ket luan sai (khong gach qua dau khac)
        ks = clamp((t - 1.2) / 0.4); f = F(46); lw = tw(d, q, f); yy = y0 + 250
        text(d, (W / 2, yy), q, 46, DRED, alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=4)
        ctext(d, y0 + 390, "✓ Lệch 4 %: sai số đọc cân", 46, (20, 83, 45), maxw=920, alpha=a1 * appear(t, 1.5, 0.3))
    if k2 > 0:
        y0 = 1050 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 440), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• Q khác thì E ra sao?", "• r quá nhỏ: không coi là điện tích điểm")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (90, y0 + 200 + j * 130), l1, 42, INK, anchor="lm", alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
HINT_LAG = 4.0                                 # goi y hien tre ~4 s sau cau hoi de HS tu nghi truoc
def s_end(img, d, t, sc):
    M = sc["M"]
    def hint(d, t, k):
        kh = appear(t, M[0] + 0.4 + HINT_LAG, 0.5)
        if kh <= 0: return
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1360, "Gợi ý", 36, MUTED, bold=False, alpha=kh)
        ctext(d, 1445, "F = q·E, mà E giữ nguyên", 42, ORANGE, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "E do Q và r quyết định,\nkhông do điện tích thử",
             "Vẫn r = 4 cm, đổi q = 20 nC.\nSố chỉ cân tăng thêm\nkhoảng bao nhiêu gam?", body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + ts, "tick") for ts, _ in STEPS]
    out += [(do["t0"] + do["M"][1] + 0.2, "tap"),
            (da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-dien-truong-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Khái niệm điện trường · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Cân điện tử đo lực điện", draw=s_hook, tail=0.8, caps=[
   ("Q đẩy q xuống, số chỉ cân tăng.", 2.8),
   ("Tự đoán trước khi xem tiếp.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Đổi r, ghi số cân tăng thêm.", 6.6),
   ("Chạm cầu trung hoà: q còn một nửa.", 4.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Lực giảm theo q, nên E giữ nguyên.", 4.2),
   ("Còn r gấp đôi thì E giảm khoảng 4 lần.", 4.3)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy thường gặp.", 3.8),
   ("Thí nghiệm này giữ Q cố định.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Dừng video, tự trả lời.", 7.0)]),
])
