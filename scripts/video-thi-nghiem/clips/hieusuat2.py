# Clip: tn-l10-hieu-suat-02 - Do hieu suat van nghieng o bon goc (ban 2 theo cong moi, 27/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-hieu-suat-02.json:
#   tham_so: mg = 4,0 N ; h = 20 cm ; mu = 0,25 ; alpha 10..60 do ; luc ke 0-5 N.
#   so_lieu_mau (alpha, s cm, F N, W_tp J, H %): 15 77,3 2,01 1,55 51,6 ; 25 47,3 2,58 1,22 65,6 ;
#   35 34,9 3,13 1,09 73,4 ; 45 28,3 3,52 1,00 80,0 ; W_ci = mgh = 0,80 J. Kiem: _kiem_so().
# Du doan (K10): van 15 do dai hon van 45 do; cong co ich o 15 do so voi 45 do? Dap an: bang nhau (mgh = 0,80 J).
#   Khong trung Bam xem cua bai (H tang theo goc, hao phi van thoai lon hon).
# Bay = hien_tuong_hay_sai[1] (lay W_tp chia W_ci -> H > 100 %). [0] (van thoai luc nho) da la moi cua Du doan.
# Cau chot (ca tu suy, ghi trong ghi_chu kho): van 60 do, luc ke 3,96 N, keo 23,1 cm
#   -> W_tp = 3,96 . 0,231 = 0,915 J ; H = 0,80/0,915 ~ 87 %. Chua hien tren man.
from engine import *
import math

ROWS = [(15, 77.3, 2.01, 1.55, 51.6), (25, 47.3, 2.58, 1.22, 65.6), (35, 34.9, 3.13, 1.09, 73.4), (45, 28.3, 3.52, 1.00, 80.0)]
MG, HCM, WCI = 4.0, 20, 0.80
def vn(x, n=1): return f"{x:.{n}f}".replace(".", ",")

def _kiem_so():
    bad = []
    for a, s, f, w, h in ROWS:
        if abs(HCM / math.sin(math.radians(a)) - s) > 0.06: bad.append(("s", a))
        if abs(round(f * s / 100, 2) - w) > 0.006: bad.append(("W_tp", a))
        if abs(round(WCI / w * 100, 1) - h) > 0.06: bad.append(("H", a))
    if abs(MG * HCM / 100 - WCI) > 1e-9: bad.append("W_ci")
    return bad

WOOD = (176, 124, 74); WOOD_D = (140, 96, 54); BOARD = (222, 184, 135); CART = (196, 140, 84)
SKIN = (240, 196, 160); DRED = (185, 28, 28); NOTE = (60, 64, 84); DGREEN = (21, 110, 55)

TOK2 = re.compile(r"(_\{[^}]*\})")
def rs(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """Chu co chi so duoi; chi so >= 40 px (brief lo 9)."""
    sub = max(56, int(size * 0.72)); segs = []
    for p in [p for p in TOK2.split(s) if p]:
        segs.append((p[2:-1], sub, size * 0.30) if p.startswith("_{") else (p, size, 0))
    tot = sum(tw(d, x, F(z)) for x, z, _ in segs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for s_, z, dy in segs:
        dtext(d, (x, cy + dy), s_, F(z), color, alpha, "lm"); x += tw(d, s_, F(z))
    return tot

def dash(d, p, q, color, w=4, seg=16, gap=12):
    L = math.dist(p, q); n = int(L // (seg + gap)) + 1
    for i in range(n):
        a = i * (seg + gap) / L; b = min(1, (i * (seg + gap) + seg) / L)
        if a >= 1: break
        d.line([(lerp(p[0], q[0], a), lerp(p[1], q[1], a)), (lerp(p[0], q[0], b), lerp(p[1], q[1], b))], fill=color, width=w)

# ---------------- khuon van nghieng ----------------
PXC = 6.0; TX, TY = 660, 740; YF = TY + HCM * PXC          # dinh van (mep be), mat san
CL, CH = 76, 40                                          # xe: dai, cao (px)
ROPE, BODY = 24, 230

def ramp_q(alpha):
    """-> (Q, L): Q(q, h) = diem cach chan van q px doc van, cao h px vuong goc mat van (h > 0 phia tren)."""
    a = math.radians(alpha); ux, uy = math.cos(a), -math.sin(a); nx, ny = -math.sin(a), -math.cos(a)
    L = HCM / math.sin(a) * PXC; fx, fy = TX - L * ux, TY - L * uy
    return (lambda q, h=0.0: (fx + q * ux + h * nx, fy + q * uy + h * ny)), L

def shelf(d):
    d.line([(50, YF), (1030, YF)], fill=INK, width=4)
    d.rectangle([TX, TY, 1010, YF], fill=WOOD, outline=WOOD_D, width=3)
    d.line([(990, TY + 8), (990, YF - 8)], fill=WHITE, width=3)
    for yy in (TY + 8, YF - 8): d.line([(978, yy), (1002, yy)], fill=WHITE, width=3)
    text(d, (835, (TY + YF) / 2), "cao 20 cm", 56, WHITE)

def ramp(d, alpha, ghost=False):
    Q, L = ramp_q(alpha)
    if ghost:
        dash(d, Q(0), Q(L), NAVY, w=5); return Q, L
    d.polygon([Q(0), Q(L), (TX, YF)], fill=(241, 245, 249))
    d.polygon([Q(0, 0), Q(L, 0), Q(L, -12), Q(0, -12)], fill=BOARD, outline=WOOD_D)
    fx, fy = Q(0); r = 80
    d.arc([fx - r, fy - r, fx + r, fy + r], 360 - alpha, 360, fill=NAVY, width=4)
    return Q, L

def cart(d, Q, q, alpha_k=1.0):
    c = lambda col: A(col, alpha_k)
    for dq in (-22, 22):
        x, y = Q(q + dq, 9); d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=c(NAVY))
    d.polygon([Q(q - CL / 2, 16), Q(q + CL / 2, 16), Q(q + CL / 2, 16 + CH), Q(q - CL / 2, 16 + CH)], fill=c(CART), outline=c(WOOD_D))

def meter(d, Q, q, f_read, fmax=5.0, alpha_k=1.0):
    """Luc ke song song van, moc vao dau tren cua xe; f_read None: che thang do bang "?"."""
    q0 = q + CL / 2
    Qk = lambda s, h=0.0: Q(q0 + s, 36 + h)
    d.line([Qk(0), Qk(ROPE - 13)], fill=A(NAVY, alpha_k), width=5)
    se = luc_ke(d, Qk, ROPE, ROPE + 16, ROPE + 16 + BODY, fmax, f_read, nho=0.5, so=(0, 2, 4), hw=30, ben=1,
                alpha=alpha_k, co=56)
    d.line([Qk(se - 16), Qk(se + 8)], fill=A(NAVY, alpha_k), width=8)
    hx, hy = Qk(se + 34); dot(d, hx, hy, 26, A(SKIN, alpha_k), outline=A((190, 140, 105), alpha_k))

def rig_card(d):
    card(d, (40, 265, 1040, 945), fill=WHITE, outline=LIGHT, w=3)

EMPTY = (148, 140, 128); DORANGE = (176, 64, 8)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0, n=6):
    p = clamp((t - t0) / (t1 - t0)); on = n - int(p * n + 1e-9); w = 780 / n
    for i in range(n):
        x = 150 + i * w
        if i < on: card(d, (x, y, x + w - 20, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + w - 20, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- canh 1: Du doan ----------------
def legend(d):
    card(d, (60, 290, 600, 480), fill=WHITE, outline=LIGHT, w=3)
    d.line([(90, 345), (170, 345)], fill=WOOD_D, width=10)
    text(d, (190, 345), "ván thoải 15°", 56, INK, anchor="lm")
    dash(d, (90, 425), (170, 425), NAVY, w=5)
    text(d, (190, 425), "ván dốc 45°", 56, INK, anchor="lm")

def s_hook(img, d, t, sc):
    M = sc["M"]
    rig_card(d); shelf(d)
    ramp(d, 45, ghost=True)
    Q, L = ramp(d, 15)
    qa, qb = CL / 2 + 8, L - CL / 2; p = clamp((t - 0.6) / 2.4); q = lerp(qa, qb, p)
    cart(d, Q, q); meter(d, Q, q, None)
    legend(d)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 990 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 175), "Ván 15° dài hơn ván 45°.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 265), "Công có ích ở 15° so với 45°?", 60, PURPLE, alpha=a)
    seg_bar(d, y0 + 370, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (4 goc) ----------------
R0, RUN, ROT, PULL = 0.6, 2.6, 0.5, 1.5

def do_state(t):
    """-> (lan i, goc dang ve, q tam xe (px), F dang chi hoac None, so hang da ghi, do mo xe)."""
    if t < R0:
        a = ROWS[0][0]; _, L = ramp_q(a); return 0, a, CL / 2 + 8, None, 0, 1.0
    i = min(3, int((t - R0) // RUN)); u = t - R0 - i * RUN
    a1 = ROWS[i][0]; a0 = ROWS[i - 1][0] if i > 0 else a1
    if u < ROT:
        a = lerp(a0, a1, ease(u / ROT)); q = CL / 2 + 8; f = None; rows = i
        k = appear(u, 0.0, 0.2) if i > 0 else 1.0
    else:
        a = a1; _, L = ramp_q(a); qa, qb = CL / 2 + 8, L - CL / 2
        p = clamp((u - ROT) / PULL); p = 1.0 if p > 1 - 1e-9 else p; q = qb if p >= 1 else lerp(qa, qb, p); f = ROWS[i][2]
        rows = i + (1 if p >= 1 else 0); k = 1.0 - (appear(u, RUN - 0.25, 0.2) if i < 3 else 0.0)
    return i, a, q, f, rows, k

XS = (150, 380, 620, 870)
def table(d, rows, hl=None, y=975):
    card(d, (40, y, 1040, y + 520), fill=WHITE, outline=LIGHT, w=3)
    text(d, (XS[0], y + 58), "góc", 56, INK)
    text(d, (XS[1], y + 58), "F (N)", 56, INK)
    text(d, (XS[2], y + 58), "s (cm)", 56, INK)
    rs(d, XS[3], y + 52, "W_{tp} (J)", 64, ORANGE)
    d.line([(70, y + 110), (1010, y + 110)], fill=LIGHT, width=3)
    for j in range(4):
        yy = y + 165 + j * 90
        if j == hl: d.rounded_rectangle([60, yy - 40, 1020, yy + 40], radius=20, fill=(255, 247, 237))
        text(d, (XS[0], yy), f"{ROWS[j][0]}°", 58, GRAY if j >= rows else INK)
        if j < rows:
            a, s, f, w, h = ROWS[j]
            text(d, (XS[1], yy), vn(f, 2), 58, NAVY); text(d, (XS[2], yy), vn(s), 58, BLUE)
            text(d, (XS[3], yy), vn(w, 2), 58, ORANGE)

def s_do(img, d, t, sc):
    i, a, q, f, rows, k = do_state(t)
    rig_card(d); shelf(d)
    Q, L = ramp(d, a)
    cart(d, Q, q, k); meter(d, Q, q, f if f is not None else 0.0, alpha_k=k)
    table(d, rows, hl=i if t >= R0 else None)

def _kiem_dong_bo():
    """Moi 0,05 s: so hang = so lan keo xong; luc ke chi F dung hang dang keo; xe o dinh <=> hang lan do da ghi."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        i, a, q, f, rows, k = do_state(t)
        _, L = ramp_q(a); at_top = abs(q - (L - CL / 2)) < 1e-6
        if t >= R0 and at_top != (rows == i + 1): bad.append(("dinh/hang", round(t, 2)))
        if f is not None and f != ROWS[i][2]: bad.append(("F", round(t, 2)))
        if rows not in (i, i + 1): bad.append(("hang", round(t, 2)))
        t += 0.05
    if R0 + 3 * RUN + ROT + PULL + 0.6 > sc["T"]: bad.append("hang cuoi qua sat cuoi canh")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
BX0, BX1, BY0, BY1, VMAX = 140, 1000, 560, 1150, 1.6
def yv(v): return BY1 - v / VMAX * (BY1 - BY0)
K_CH, K_H = 0.3, 2.9

def s_dapan(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 470, 1040, 1300), fill=WHITE, outline=LIGHT, w=3)
    d.line([(BX0, BY1), (BX1, BY1)], fill=INK, width=4)
    dash(d, (BX0, yv(WCI)), (BX1, yv(WCI)), DGREEN, w=5)
    for j, (a, s, f, w, h) in enumerate(ROWS):
        k = ease((t - K_CH) / 0.7); cx = 290 + j * 210
        text(d, (cx, BY1 + 55), f"{a}°", 58, INK)
        top = w * k
        d.rectangle([cx - 60, yv(min(top, WCI)), cx + 60, BY1], fill=GREEN)
        if top > WCI + 0.01:
            pu = 0.75 + 0.25 * math.sin(6.0 * max(0.0, t - K_H) + j) if t > K_H else 1.0
            d.rectangle([cx - 60, yv(top), cx + 60, yv(WCI)], fill=mix(WHITE, ORANGE, pu))
    rs(d, 70, 520, "có ích W_{ci} = 0,80 J", 64, DGREEN, anchor="l")
    ka = appear(t, M[1] + 0.3, 0.4)
    if ka > 0:
        card(d, (60, 1340, 1020, 1470), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), r=28, w=5)
        text(d, (W / 2, 1405), "Đáp án: bằng nhau, 0,80 J", 60, GREEN, alpha=ka)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; mk = M[1]
    # thanh so sanh: co ich nam TRONG toan phan (goc 15 do), hien tu dau
    card(d, (40, 260, 1040, 560), fill=WHITE, outline=LIGHT, w=3)
    x0, x1 = 90, 990; xc = x0 + (x1 - x0) * WCI / ROWS[0][3]
    d.rectangle([x0, 330, x1, 450], fill=(255, 237, 213), outline=ORANGE, width=4)
    d.rectangle([x0, 330, xc, 450], fill=GREEN)
    rs(d, (x0 + xc) / 2, 384, "W_{ci} 0,80 J", 64, WHITE)
    rs(d, (xc + x1) / 2, 384, "1,55 J", 64, DORANGE)
    rs(d, x0, 510, "góc 15°: toàn phần W_{tp}", 64, INK, anchor="l")
    k0 = appear(t, 0.2, 0.4); k3 = appear(t, M[2] - 0.1, 0.45); a1 = k0 * (1 - k3); y = 1000
    ks = clamp((t - mk) / 0.4)
    if a1 > 0:
        card(d, (40, y, 1040, y + 420), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pill(d, W / 2, y + 70, "BẪY", RED, a1)
        yy = y + 190
        lw = rs(d, W / 2, yy, "“H = W_{tp} ÷ W_{ci}”", 64, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 4), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 4)], fill=A(RED, 0.85 * a1), width=6)
        k2 = appear(t, mk + 0.2, 0.45)
        if k2 > 0: text(d, (W / 2, y + 320), "1,55 ÷ 0,80: quá 100 %", 60, DORANGE, alpha=a1 * k2)
    if k3 > 0:
        card(d, (40, y, 1040, y + 330), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, y + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, y + 210), "Chưa thử ván bôi trơn", 62, INK, alpha=k3)

# ---------------- canh 5: thu nghi (cau chot o khung: 87 %) ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1620), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 310, "THỬ NGHĨ", ORANGE, k)
    P0, P1, P2 = (330, 820), (515, 820), (515, 500)
    d.polygon([P0, P1, P2], fill=A(BOARD, k), outline=A(WOOD_D, k))
    d.line([P0, P2], fill=A(WOOD_D, k), width=8)
    u = (t * 0.3) % 1.0; ux, uy = (P2[0] - P0[0]) / 370, (P2[1] - P0[1]) / 370
    c0 = 40 + 280 * u; cx, cy = P0[0] + ux * c0, P0[1] + uy * c0; nx, ny = uy, -ux
    sq = [(cx - ux * 28, cy - uy * 28), (cx + ux * 28, cy + uy * 28),
          (cx + ux * 28 + nx * 50, cy + uy * 28 + ny * 50), (cx - ux * 28 + nx * 50, cy - uy * 28 + ny * 50)]
    d.polygon(sq, fill=A(CART, k), outline=A(WOOD_D, k))
    text(d, (268, 800), "60°", 56, INK, alpha=k)
    text(d, (545, 660), "h = 20 cm", 56, INK, alpha=k, anchor="lm")
    text(d, (395, 600), "s = 23,1 cm", 56, INK, alpha=k, anchor="rm")
    text(d, (W / 2, 900), "Ván 60°: lực kế 3,96 N,", 62, INK, alpha=k)
    text(d, (W / 2, 990), "trọng lượng xe 4,0 N.", 62, INK, alpha=k)
    text(d, (W / 2, 1130), "Hiệu suất H khoảng bao nhiêu?", 62, DORANGE, alpha=k)
    seg_bar(d, 1290, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.05, "ding")]
            + [(do["t0"] + R0 + i * RUN + ROT + PULL, "tap") for i in range(4)]
            + [(da["t0"] + da["M"][1] + 0.3, "ding"), (b["t0"] + b["M"][1], "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"),
               (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l10-hieu-suat-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Hiệu suất · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Ván nghiêng, nâng xe 20 cm", draw=s_hook, tail=0.3, caps=[
   ("Kéo đều xe lên ván thoải.", 3.4),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Bốn góc nghiêng", draw=s_do, tail=0.4, caps=[
   ("Lực kế luôn song song mặt ván.", 5.4),
   ("Mỗi góc ghi lực F, quãng s.", 5.8)]),
 dict(key="dapan", title="Có ích và hao phí", draw=s_dapan, tail=0.5, caps=[
   ("Mỗi cột: công kéo ở một góc.", 4.6),
   ("Phần cam: thắng ma sát.", 4.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Đúng không?", 3.2),
   ("Sai: có ích chia toàn phần.", 3.4),
   ("Giới hạn của lần đo.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng lại, tự tính.", 6.4)]),
])

if __name__ == "__main__" and "--kiem" in __import__("sys").argv:
    print("số:", _kiem_so() or "khớp kho"); print("đồng bộ:", _kiem_dong_bo() or "không lệch")
