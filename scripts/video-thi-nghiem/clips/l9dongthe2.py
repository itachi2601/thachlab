# Clip: tn-l9-dongthe-02 - Xe lan tren mang ngang qua cong quang: do dong nang Wd = 1/2 m v^2 (KHTN 9, 5/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-dongthe-02.json:
#   tham_so: d = 0,02 m (tam chan 2,0 cm) ; m 0,2-0,6 kg ; dong ho do chia 0,0001 s
#   so_lieu_mau (m kg, dt s, v m/s, Wd J): 0,2 0,0198 1,01 0,102 ; 0,2 0,0101 1,98 0,392 ; 0,4 0,0202 0,99 0,196 ;
#                                          0,4 0,0099 2,02 0,816 ; ket_qua_ky_vong: 0,392 : 0,102 ~ 3,84 (gan 4)
# Bo cuc (khac l9conang1 = mang nghieng + bang h-v, dongnang1 L10 = go truot + bang): xe lan tren MANG NGANG,
#   dong ho so rieng, DO THI Wd theo v lam truc chinh (khong bang), truc co dinh tu canh do toi canh rut ra.
# Canh: Du doan (cung xe 0,20 kg, v gap doi -> Wd gap may; chi cau hoi + hinh, K10; khac l9dongthe1 = bi nang hon)
#   -> Tien hanh (4 lan day, diem hien khi xe qua cong) -> DAP AN · gan gap 4 -> Rut ra (duong cong 1/2 m v^2,
#   m gap doi -> Wd gap doi) -> Chua noi duoc + bay "3,84 chua dung 4 -> cong thuc sai" (v cung chua dung gap 2)
#   -> Chot + THU NGHI: xe 0,40 kg, dt = 0,020 s (ghi_chu) -> v = 1,00 m/s, Wd = 0,20 J (chua hien; gan 0,196).
# Lua chon Du doan (o khung web): A. Khong doi · B. Gan gap 2 · C. Gan gap 4 (dung) · D. Gan gap 8.
# Cau 1 sau hop trong bai hoi cach cho ket luan dang tin (do lap, lay trung binh) -> clip KHONG noi y do.
from engine import *

ROWS = [(0.20, 0.0198, 1.01, 0.102), (0.20, 0.0101, 1.98, 0.392), (0.40, 0.0202, 0.99, 0.196), (0.40, 0.0099, 2.02, 0.816)]
def fm(x, n=2): return f"{x:.{n}f}".replace(".", ",")

CART = (59, 130, 246); CART_D = (30, 64, 175); MASS = (120, 113, 108); FLAG = (24, 30, 56)
C02, C04 = BLUE, ORANGE                       # mau diem: xe 0,20 kg / xe 0,40 kg (goi theo khoi luong)

def dashed(d, p1, p2, color, w=4, dash=16, gap=12):
    L = math.hypot(p2[0] - p1[0], p2[1] - p1[1]); n = int(L // (dash + gap)) + 1
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

# ---------------- mang ngang + xe + cong quang + dong ho ----------------
TY = 590                      # mat mang
GATE = 560                    # x cong quang
X0, XSTOP = 190, 900          # tam xe luc day / luc cham vat chan
FW = 24                       # be rong tam chan tren hinh

def cart(d, x, heavy, alpha=1.0):
    c = lambda col: A(col, alpha)
    d.rounded_rectangle([x - 90, TY - 92, x + 90, TY - 30], radius=12, fill=c(CART), outline=c(CART_D), width=4)
    for wx in (x - 55, x + 55):
        d.ellipse([wx - 20, TY - 40, wx + 20, TY], fill=c(NAVY)); d.ellipse([wx - 7, TY - 27, wx + 7, TY - 13], fill=c(GRAY))
    d.rectangle([x - FW / 2, TY - 200, x + FW / 2, TY - 92], fill=c(FLAG))          # tam chan sang
    if heavy > 0:
        k = alpha * heavy
        d.rounded_rectangle([x - 78, TY - 150, x - 20, TY - 94], radius=8, fill=A(MASS, k), outline=A(NAVY, k), width=3)
        d.rounded_rectangle([x + 20, TY - 150, x + 78, TY - 94], radius=8, fill=A(MASS, k), outline=A(NAVY, k), width=3)

def rig(d, t, x, heavy, blocked, m_txt, dt_txt, ca=1.0, flag_lbl=False):
    # ban, mang, vat chan
    d.rectangle([70, TY, 1010, TY + 26], fill=(90, 98, 122))
    for lx in (120, 960): d.rectangle([lx - 10, TY + 26, lx + 10, TY + 70], fill=GRAY)
    d.line([(60, TY + 70), (1020, TY + 70)], fill=NAVY, width=6)
    d.rectangle([996, TY - 70, 1012, TY], fill=NAVY)
    # cong quang (chan + dau cam bien): tia sang o do cao tam chan
    d.rectangle([GATE - 9, TY - 165, GATE + 9, TY + 26], fill=GRAY)
    d.rounded_rectangle([GATE - 34, TY - 190, GATE + 34, TY - 130], radius=10, fill=NAVY)
    dot(d, GATE, TY - 160, 11, (70, 70, 80) if blocked else RED)
    # day noi toi dong ho
    d.line([(GATE + 9, TY + 42), (760, TY + 42), (760, 690)], fill=GRAY, width=5)
    cart(d, x, heavy, ca)
    if flag_lbl:
        a = appear(t, 1.0)
        arrow(d, (x + 150, TY - 250), (x + 20, TY - 180), A(INK, a), w=5, head=18)
        text(d, (x + 160, TY - 262), "tấm chắn d = 2,0 cm", 40, INK, anchor="lm", alpha=a)
    # the khoi luong + dong ho so
    card(d, (60, 690, 470, 830), fill=WHITE, outline=LIGHT, r=24, w=4)
    text(d, (265, 728), "khối lượng xe", 40, MUTED, bold=False)
    text(d, (265, 790), "m = " + m_txt + " kg", 46, INK)
    card(d, (500, 690, 1020, 830), fill=NAVY, r=24)
    text(d, (760, 728), "Δt: thời gian chắn sáng", 40, (190, 200, 225), bold=False)
    text(d, (760, 790), "Δt = " + dt_txt + " s", 50, (110, 231, 160))

# ---------------- do thi Wd theo v (truc co dinh) ----------------
GX0, GY0, PXV, PYJ = 220, 1500, 330, 560
def gp(v, w): return GX0 + v * PXV, GY0 - w * PYJ
def axes(d, a=1.0):
    d.line([(GX0, GY0), (GX0 + 2.45 * PXV, GY0)], fill=A(NAVY, a), width=5)
    d.line([(GX0, GY0), (GX0, GY0 - 0.93 * PYJ)], fill=A(NAVY, a), width=5)
    for v in (1, 2):
        x, _ = gp(v, 0); d.line([(x, GY0), (x, GY0 + 14)], fill=A(NAVY, a), width=4)
        text(d, (x, GY0 + 44), str(v), 40, MUTED, alpha=a)
    text(d, (GX0, GY0 + 44), "0", 40, MUTED, alpha=a)
    for w in (0.2, 0.4, 0.6, 0.8):
        _, y = gp(0, w); d.line([(GX0 - 14, y), (GX0, y)], fill=A(NAVY, a), width=4)
        d.line([(GX0 + 4, y), (GX0 + 2.4 * PXV, y)], fill=A((236, 230, 220), a), width=2)
        text(d, (GX0 - 24, y), fm(w, 1), 40, MUTED, anchor="rm", alpha=a)
    text(d, (GX0 + 2.45 * PXV, GY0 - 34), "v (m/s)", 40, INK, anchor="rm", alpha=a)
    text(d, (GX0 + 14, GY0 - 0.93 * PYJ - 4), "Wđ (J)", 40, INK, anchor="lm", alpha=a)
    for k, (lbl, col) in enumerate((("xe 0,20 kg", C02), ("xe 0,40 kg", C04))):
        y = GY0 - 0.72 * PYJ + k * 58
        dot(d, GX0 + 50, y, 13, A(col, a)); text(d, (GX0 + 76, y), lbl, 40, INK, anchor="lm", alpha=a)

LBL = [("l", 1), ("l", 1), ("r", -1), ("r", -1)]   # nhan so: ben phai (lm) cho xe 0,20, ben trai (rm) cho xe 0,40
def point(d, j, a, big=False, lbl=True):
    if a <= 0: return
    m, dt, v, w = ROWS[j]; x, y = gp(v, w); col = C02 if m < 0.3 else C04
    r = 17 if big else 14
    dot(d, x, y, r, A(col, a), outline=A(WHITE, a))
    if lbl:
        an, s = LBL[j]
        text(d, (x + s * 28, y), fm(w, 3), 40, col, anchor=an + "m", alpha=a)

# ---------------- canh 1: mo bai + du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    rig(d, t, X0, 0, False, "0,20", "?", flag_lbl=True)
    k = appear(t, sc["M"][1] - 0.5, 0.5)
    if k <= 0: return
    card(d, (60, 890, 1020, 1330), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    text(d, (W / 2, 950), "Dự đoán", 46, PURPLE, alpha=k)
    text(d, (W / 2, 1060), "Cùng xe, tốc độ v gấp đôi.", 46, INK, alpha=k)
    text(d, (W / 2, 1160), "Động năng Wđ gấp mấy lần?", 46, INK, alpha=k)
    t1, t2 = sc["M"][1] + 0.4, sc["T"] - 0.1; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([140, 1268, 940, 1282], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([140, 1268, 140 + 800 * (1 - q), 1282], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh, 4 lan day ----------------
REL = [0.5, 2.8, 5.4, 7.6]                     # moc day lan i
SPD = [410, 820, 410, 820]                     # px/s tren hinh: lan manh nhanh gap doi
def cart_x(tau, i): return min(XSTOP, X0 + SPD[i] * max(0.0, tau))
def pass_t(i): return REL[i] + (GATE + FW / 2 - X0) / SPD[i]      # tam chan vua ra khoi tia sang
HEAVY_AT = REL[2] - 0.4                        # them gia trong (luc xe ve dau mang)

def do_state(t):
    i = max([j for j in range(4) if t >= REL[j] - 0.4], default=0)
    x = cart_x(t - REL[i], i)
    blocked = abs(x - GATE) < FW / 2
    if t >= pass_t(i): dt = fm(ROWS[i][1], 4); shown = i
    elif t >= REL[i]: dt = "0,0000"; shown = i - 1 if i != 2 else -1
    elif i == 2: dt = fm(ROWS[1][1], 4); shown = -1   # vua them gia trong: giu so dong ho cu, an dong tinh cua xe 0,20 kg
    else: dt = fm(ROWS[i - 1][1], 4) if i > 0 else "?"; shown = i - 1   # giu so cu toi luc day lan moi
    ca = clamp((t - (REL[i] - 0.4)) / 0.25) if i > 0 else 1.0
    heavy = appear(t, HEAVY_AT, 0.2)
    m_txt = "0,40" if t >= HEAVY_AT + 0.1 else "0,20"
    return i, x, blocked, dt, shown, ca, heavy, m_txt

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    i, x, blocked, dt, shown, ca, heavy, m_txt = do_state(t)
    rig(d, t, x, heavy, blocked, m_txt, dt, ca=ca)
    axes(d)
    for j in range(4):
        point(d, j, appear(t, pass_t(j), 0.3))
    if shown >= 0:
        m, dtv, v, w = ROWS[shown]
        rich(d, W / 2, 860, f"v = 0,020 m : Δt = {fm(v)} m/s", 42, INK)
        rich(d, W / 2, 914, f"Wđ = ½·m·v² = {fm(w, 3)} J", 42, INK)

# ---------------- canh 3: dap an ----------------
def s_ans(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    a0 = appear(t, 0.3); a1 = appear(t, M[0] + 1.2); a2 = appear(t, M[1], 0.4)
    card(d, (60, 290, 1020, 670), fill=WHITE, outline=LIGHT, w=4)
    text(d, (110, 365), "v:", 46, INK, anchor="lm", alpha=a0)
    text(d, (230, 365), "1,01 → 1,98 m/s", 46, C02, anchor="lm", alpha=a0)
    text(d, (970, 365), "gần gấp 2", 42, MUTED, anchor="rm", alpha=a1)
    text(d, (110, 465), "Wđ:", 46, INK, anchor="lm", alpha=a0)
    text(d, (230, 465), "0,102 → 0,392 J", 46, C02, anchor="lm", alpha=a0)
    text(d, (970, 465), "gấp 3,84", 42, MUTED, anchor="rm", alpha=a2)
    if a2 > 0:
        card(d, (150, 540, 930, 630), fill=A(GREEN, a2), r=45)
        text(d, (W / 2, 585), "ĐÁP ÁN · gần gấp 4", 46, WHITE, alpha=a2)
    axes(d)
    for j in (2, 3): point(d, j, 0.35, lbl=False)
    for j in (0, 1):
        _, _, v, w = ROWS[j]; x, y = gp(v, w)
        g = appear(t, 0.5 + 0.4 * j)
        dashed(d, (x, y), (x, GY0), A(C02, g), w=3); dashed(d, (x, y), (GX0, y), A(C02, g), w=3)
        point(d, j, 1.0, big=True)

# ---------------- canh 4: rut ra ----------------
def s_rut(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (60, 290, 1020, 540), fill=WHITE, outline=GREEN, w=5)
    rich(d, W / 2, 360, "Wđ = ½·m·v²", 54, GREEN)
    rich(d, W / 2, 470, "v gấp 2 thì v² gấp 4", 46, INK, alpha=appear(t, M[0] + 1.0))
    axes(d)
    g = ease((t - 0.5) / 1.6)
    for m, col in ((0.20, C02), (0.40, C04)):
        vmax = (2.15 if m < 0.3 else 2.1) * g; pts = []
        n = 40
        for k in range(n + 1):
            v = vmax * k / n; pts.append(gp(v, 0.5 * m * v * v))
        for k in range(0, n, 2): d.line([pts[k], pts[k + 1]], fill=A(col, 0.8), width=4)
    hl = appear(t, M[1], 0.4)
    for j in range(4): point(d, j, 1.0, big=(j in (0, 2) and hl > 0), lbl=True)
    if hl > 0:
        card(d, (60, 600, 1020, 820), fill=A((255, 247, 237), hl), outline=A(ORANGE, hl), w=4)
        text(d, (W / 2, 655), "m: 0,20 → 0,40 kg", 42, INK, alpha=hl)
        text(d, (W / 2, 750), "Wđ: 0,102 → 0,196 J · gần gấp 2", 44, ORANGE, alpha=hl)
        x1, y1 = gp(ROWS[0][2], ROWS[0][3]); x2, y2 = gp(ROWS[2][2], ROWS[2][3])
        d.ellipse([min(x1, x2) - 40, y2 - 40, max(x1, x2) + 40, y1 + 40], outline=A(ORANGE, hl), width=5)

# ---------------- canh 5: chua noi duoc + bay ----------------
NX0, NPX = 1.90, 5200                           # truc so phong to: tu 1,90 m/s, px moi m/s
def nx(v): return 140 + (v - NX0) * NPX
def s_trap(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    a = appear(t, 0.1)
    card(d, (60, 270, 1020, 500), fill=WHITE, outline=BLUE, w=6)
    text(d, (W / 2, 330), "Chưa nói được:", 46, BLUE, alpha=a)
    text(d, (W / 2, 425), "Số minh hoạ, chưa đo thật.", 42, INK, alpha=a)
    b = appear(t, M[1] - 0.05, 0.3)
    if b <= 0: return
    card(d, (60, 570, 1020, 1320), fill=A(WHITE, b), outline=A(RED, b), w=6)
    text(d, (W / 2, 630), "Bẫy:", 44, RED, alpha=b)
    q = "“Không đúng 4: sai công thức”"
    qw = tw(d, q, F(44)); x0 = W / 2 - qw / 2
    text(d, (x0, 700), q, 44, INK, anchor="lm", alpha=b)
    x = appear(t, M[1] + 2.3, 0.3)
    if x > 0:
        d.line([(x0 - 6, 702), (x0 + qw + 6, 702)], fill=A(RED, x), width=6)
        text(d, (x0 + qw + 14, 700), "✗", 48, RED, anchor="lm", alpha=x)
    # truc so v phong to (xe 0,20 kg, lan 2)
    text(d, (130, 790), "phóng to", 40, MUTED, bold=False, anchor="lm", alpha=b)
    y = 900
    d.line([(110, y), (970, y)], fill=A(NAVY, b), width=5)
    xm = nx(2 * ROWS[0][2])
    dashed(d, (xm, y - 70), (xm, y + 10), A(GREEN, b), w=5, dash=12, gap=8)
    text(d, (xm - 20, y - 98), "gấp đúng 2: 2,02", 40, GREEN, anchor="mm", alpha=b)
    xo = nx(ROWS[1][2]); dot(d, xo, y, 16, A(C02, b), outline=A(WHITE, b))
    text(d, (xo - 20, y + 100), "đo: 1,98", 42, C02, anchor="rm", alpha=b)
    if x > 0:
        card(d, (100, 1070, 980, 1290), fill=A((220, 252, 231), x), r=26)
        text(d, (W / 2, 1135), "✓ Vì v chưa gấp đúng 2", 46, GREEN, alpha=x)
        text(d, (W / 2, 1220), "v gấp 1,96 → Wđ gấp 3,84", 44, GREEN, alpha=x)

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    def body(d, t, k1):
        # hinh nho: xe co gia trong ghi 0,60 kg, cong quang (khong ghi so dap an)
        bx, by = 540, 1110
        d.rectangle([200, by + 40, 880, by + 56], fill=A((90, 98, 122), k1))
        d.rectangle([700 - 7, by - 110, 700 + 7, by + 40], fill=A(GRAY, k1))
        d.rounded_rectangle([700 - 26, by - 130, 700 + 26, by - 86], radius=8, fill=A(NAVY, k1))
        dot(d, 700, by - 108, 8, A(RED, k1))
        x = 420
        d.rounded_rectangle([x - 80, by - 30, x + 80, by + 20], radius=10, fill=A(CART, k1), outline=A(CART_D, k1), width=3)
        for wx in (x - 48, x + 48): dot(d, wx, by + 24, 16, A(NAVY, k1))
        d.rectangle([x - 9, by - 115, x + 9, by - 30], fill=A(FLAG, k1))
        for gx in (x - 64, x + 18): d.rounded_rectangle([gx, by - 72, gx + 46, by - 32], radius=6, fill=A(MASS, k1), outline=A(NAVY, k1), width=3)
        text(d, (x - 150, by - 10), "0,40 kg", 42, INK, anchor="rm", alpha=k1)
        kh = appear(t, sc["M"][0] + 2.5, 0.5)
        if kh <= 0: return
        card(d, (110, 1330, 970, 1450), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1390, "Gợi ý: Wđ = ½·m·v²; d = 0,020 m", 42, ORANGE, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "v gấp đôi → Wđ gấp 4; m gấp đôi → Wđ gấp 2",
             "Xe 0,40 kg, Δt = 0,020 s. Wđ khoảng bao nhiêu?", None, body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, tr, e = sc["hook"], sc["do"], sc["ans"], sc["trap"], sc["end"]
    out = [(h["t0"] + h["M"][1], "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + pass_t(i), "tap") for i in range(4)]
    out += [(an["t0"] + an["M"][1], "ding"), (tr["t0"] + tr["M"][1], "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l9-dongthe-02", header="KHTN 9 · THÍ NGHIỆM", cues=_cues,
    footer="Động năng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Xe lăn qua cổng quang", draw=s_hook, tail=0.4, caps=[
   ("Tấm chắn che tia sáng.", 3.4),
   ("Dừng video, tự đoán.", 5.4)]),
 dict(key="do", title="Đẩy xe bốn lần", draw=s_do, tail=0.4, caps=[
   ("Đẩy nhẹ, rồi đẩy mạnh hơn.", 4.5),
   ("Thêm gia trọng, lặp lại.", 4.1)]),
 dict(key="ans", title="So hai lần đẩy", draw=s_ans, tail=0.4, caps=[
   "Cùng xe, so hai lần đẩy.",
   "Động năng tăng nhanh hơn tốc độ."]),
 dict(key="rut", title="Đồ thị là đường cong", draw=s_rut, tail=0.4, caps=[
   "Bình phương nên cong lên.",
   "Cùng tốc độ, xe nặng gấp đôi."]),
 dict(key="trap", title="Giới hạn và cái bẫy", draw=s_trap, tail=0.4, caps=[
   ("Còn giới hạn.", 3.0),
   ("Lệch khỏi 4 có phải sai?", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Dừng lại, tự nghĩ.", 6.2)]),
])
