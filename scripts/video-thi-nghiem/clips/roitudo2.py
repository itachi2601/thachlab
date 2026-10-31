# Clip: tn-l10-roi-tu-do-02 - Day doi va video quay cham: vi tri bi roi sau moi 0,1 s (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-roi-tu-do-02.json:
#   tham_so: T = 0,1 s (mien 0,05..0,2), g = 9,8 m/s2; s do tu diem tha (cm).
#   so_lieu_mau: t = 0..0,5 s -> s = 0; 4,9; 19,6; 44,1; 78,4; 122,5 cm; khoang 4,9; 14,7; 24,5; 34,3; 44,1 cm.
#   mo_hinh: ds_(n+1) - ds_n = g.T^2 = 9,8 cm (T = 0,1 s).
#   Cau chot dung T = 0,2 s (trong mien tham_so): khoang 19,6 va 58,8 cm -> hieu 39,2 cm, chua tung hien.
# Truc chinh: hinh nhieu anh bi chong theo moc 0,1 s, khoang cach tang dan (khac dog2: do thi s-t^2).
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (bi roi cham, de lai bong moi 0,1 s, bang t-s)
#       -> Dap an (khoang + hieu 9,8) -> Rut ra (phuong/chieu, toc do TB tang deu, chua noi duoc) -> Bay -> Chot.
# Mau: vi tri s = BLUE, khoang = ORANGE, hieu 9,8 = GREEN, toc do TB = TEAL, bi = xam thep.
from engine import *

G_CM = 490.0                                             # g/2 = 4,9 m/s2 = 490 cm/s2
ROWS = [(0.0, 0.0), (0.1, 4.9), (0.2, 19.6), (0.3, 44.1), (0.4, 78.4), (0.5, 122.5)]   # so_lieu_mau (t s, s cm)
GAPS = [4.9, 14.7, 24.5, 34.3, 44.1]                     # so_lieu_mau: khoang toi vi tri sau (cm)
SPEED = (8, 145, 178)                                    # toc do TB: xanh cyan (khac xanh la cua +9,8)
STEEL = (110, 120, 140); STEEL_L = (200, 205, 216); GHOST = (196, 202, 214); WOOD = (250, 236, 196); WOOD_D = (190, 160, 100)

def vn(x, nd=1):
    return f"{x:.{nd}f}".replace(".", ",")

# ---------------- dung cu dung chung (thuoc + day doi + bi) ----------------
Y0, PXC = 360, 10.0                                      # y cua vach 0 ; px / cm
def Y(scm): return Y0 + PXC * scm
RX0, RX1 = 150, 215                                      # than thuoc
PX = 268                                                 # day doi
BX, BR = 298, 14                                         # tam bi (sat day), ban kinh

def ruler(d):
    d.rectangle([RX0, Y0 - 30, RX1, 1690], fill=WOOD, outline=WOOD_D, width=3)
    for c in range(0, 134, 2):
        y = Y(c)
        L = 34 if c % 20 == 0 else (22 if c % 10 == 0 else 10)
        d.line([(RX1 - L, y), (RX1, y)], fill=INK, width=3 if c % 10 == 0 else 2)
        if c % 20 == 0:
            text(d, (RX0 - 12, y), str(c), 38, INK, anchor="rm")
    text(d, (RX0 - 40, Y0 - 62), "s (cm)", 38, BLUE, anchor="lm")

def plumb(d):
    d.line([(PX - 30, 292), (PX + 60, 292)], fill=NAVY, width=8)                 # gia treo
    d.line([(PX, 292), (PX, 1630)], fill=NAVY, width=3)
    d.polygon([(PX - 16, 1630), (PX + 16, 1630), (PX, 1670)], fill=NAVY)          # qua doi

def ball(d, s, ghost=False, alpha=1.0):
    y = Y(s)
    if ghost:
        d.ellipse([BX - BR, y - BR, BX + BR, y + BR], fill=A(GHOST, alpha), outline=A(STEEL, alpha), width=3)
    else:
        d.ellipse([BX - BR, y - BR, BX + BR, y + BR], fill=A(STEEL, alpha), outline=A(NAVY, alpha), width=2)
        d.ellipse([BX - 7, y - 8, BX - 1, y - 2], fill=A(STEEL_L, alpha))

def holder(d):
    d.rectangle([BX - 9, 300, BX + 9, Y0 - BR - 2], fill=NAVY)                     # kep tha bi

def setup(d, ghosts=(), cur=None, hold=False):
    ruler(d); plumb(d)
    if hold: holder(d)
    for s in ghosts: ball(d, s, ghost=True)
    if cur is not None: ball(d, cur)

def text_cx(d, cx, y, s, size, color=INK, bold=True, maxw=600, alpha=1.0, lh=1.22):
    """Nhu ctext nhung can giua quanh cx (cot phai)."""
    f = F(size, bold); ls = wrap(d, s, f, maxw)
    y0 = y - (len(ls) - 1) * size * lh / 2
    for i, l in enumerate(ls):
        dtext(d, (cx, y0 + i * size * lh), l, f, color, alpha)

# ---------------- canh 1: Du doan ----------------
QX0, QX1 = 380, 1040
QC = (QX0 + QX1) / 2
def phone(d):
    card(d, (850, 290, 975, 520), fill=NAVY, r=20)
    card(d, (862, 312, 963, 498), fill=(60, 72, 110), r=10)
    dot(d, 912, 405, 26, (30, 36, 60), outline=STEEL_L)
    text(d, (825, 405), "quay chậm", 40, INK, anchor="rm")

def s_hook(img, d, t, sc):
    M = sc["M"]
    setup(d, cur=0.0, hold=True)
    text(d, (PX + 50, 1650), "dây dọi", 40, NAVY, anchor="lm")
    phone(d)
    a = appear(t, M[0] + 0.3, 0.5)
    if a <= 0: return
    y0 = 570 + (1 - a) * 40
    card(d, (QX0, y0, QX1, y0 + 790), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (QC - pw / 2, y0 + 30, QC + pw / 2, y0 + 92), fill=A(PURPLE, a), r=31)
    text(d, (QC, y0 + 61), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    text_cx(d, QC, y0 + 190, "Thả nhẹ, bỏ qua lực cản.", 42, INK, bold=False, maxw=580, alpha=a)
    text_cx(d, QC, y0 + 305, "Đánh dấu vị trí bi mỗi 0,1 s.", 42, INK, bold=False, maxw=580, alpha=a)
    text_cx(d, QC, y0 + 510, "Khoảng giữa hai vị trí liền nhau đổi thế nào?", 50, INK, maxw=580, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.8
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([QX0 + 60, y0 + 690, QX1 - 60, y0 + 704], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([QX0 + 60, y0 + 690, QX0 + 60 + (QX1 - QX0 - 120) * (1 - p), y0 + 704], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (bi roi cham, bong moi 0,1 s) ----------------
SLOW = 16.0
RUN0 = 0.8
def run_state(t):
    """-> (tau that (s), s bi (cm), so bong da danh dau). Bong n = vi tri luc t = n.0,1 s (n = 0..5)."""
    if t < RUN0: return -1.0, 0.0, 0
    tau = min((t - RUN0) / SLOW, 0.5)
    n = min(5, int(tau * 10 + 1e-9)) + 1
    return tau, G_CM * tau * tau, n

def chip(d, y=290):
    card(d, (QX0, y, QX1, y + 74), fill=(245, 243, 255), outline=PURPLE, r=37, w=3)
    text(d, (QC, y + 37), "Khoảng liền nhau đổi thế nào?", 38, PURPLE)

def s_do(img, d, t, sc):
    tau, s, n = run_state(t)
    setup(d, ghosts=[ROWS[i][1] for i in range(n)], cur=s, hold=(tau < 0))
    text(d, (PX + 50, 1650), "dây dọi", 40, NAVY, anchor="lm")
    if n > 0:                                            # vong nhan manh bong vua danh dau
        tn = RUN0 + (n - 1) * 0.1 * SLOW
        k = 1 - clamp((t - tn) / 0.6)
        if k > 0:
            yy = Y(ROWS[n - 1][1]); r = BR + 8 + 14 * (1 - k)
            d.ellipse([BX - r, yy - r, BX + r, yy + r], outline=A(BLUE, k), width=5)
    chip(d)
    card(d, (QX0, 395, QX1, 480), fill=NAVY, r=18)
    text(d, (QC, 437), "chiếu chậm", 40, YELLOW)
    # bang t - s
    y = 520
    card(d, (QX0, y, QX1, y + 740), fill=WHITE, outline=LIGHT, w=3)
    XS = (QX0 + 170, QX0 + 470)
    text(d, (XS[0], y + 60), "t (s)", 44, INK)
    text(d, (XS[1], y + 60), "s (cm)", 44, BLUE)
    d.line([(QX0 + 30, y + 108), (QX1 - 30, y + 108)], fill=LIGHT, width=3)
    for i, (ti, si) in enumerate(ROWS):
        yy = y + 170 + i * 98
        if i == n - 1 and t - (RUN0 + i * 0.1 * SLOW) < 0.9:
            d.rounded_rectangle([QX0 + 20, yy - 42, QX1 - 20, yy + 42], radius=18, fill=(239, 246, 255))
        if i < n:
            text(d, (XS[0], yy), vn(ti, 1), 48, INK)
            text(d, (XS[1], yy), vn(si, 1), 48, BLUE)

# ---------------- canh 3: Dap an (khoang + hieu) ----------------
LX = BX + 52                                             # cot nhan khoang
DX = 640                                                 # cot "dai them"
def gap_y(i): return (Y(ROWS[i][1]) + Y(ROWS[i + 1][1])) / 2

def brackets(d, k_of):
    for i in range(5):
        k = k_of(i)
        if k <= 0: continue
        ya, yb = Y(ROWS[i][1]) + 3, Y(ROWS[i + 1][1]) - 3
        x = BX + 24
        d.line([(x, ya), (x + 12, ya), (x + 12, yb), (x, yb)], fill=A(ORANGE, k), width=4)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    setup(d, ghosts=[r[1] for r in ROWS])
    ka = appear(t, 0.15, 0.5)
    lb = "ĐÁP ÁN · dài dần, thêm đều"
    pw = tw(d, lb, F(38)) + 56
    card(d, (QX1 - pw, 268, QX1, 332), fill=A(NAVY, ka), r=32)
    text(d, (QX1 - pw / 2, 300), lb, 38, WHITE, alpha=ka)
    brackets(d, lambda i: appear(t, 0.5 + 0.3 * i, 0.35))
    for i, g in enumerate(GAPS):
        k = appear(t, 0.5 + 0.3 * i, 0.35)
        yy = gap_y(i)
        text(d, (LX, yy), vn(g) + " cm", 40, ORANGE, anchor="lm", alpha=k)
    for i in range(4):
        k = appear(t, M[0] + 0.4 + 0.45 * i, 0.35)
        ya = gap_y(i)
        yb = gap_y(i + 1)
        ym = (ya + yb) / 2
        if k > 0:
            d.line([(DX - 20, ya), (DX - 8, ya), (DX - 8, yb), (DX - 20, yb)], fill=A(GREEN, k), width=3)
        text(d, (DX + 6, ym), "+9,8 cm", 40, GREEN, anchor="lm", alpha=k)
    kb = appear(t, M[0] + 3.0, 0.5)
    card(d, (600, 1290, QX1, 1590), fill=A((236, 253, 243), kb), outline=A(GREEN, kb), w=5)
    text(d, (820, 1370), "Mỗi khoảng dài hơn", 40, INK, alpha=kb)
    text(d, (820, 1430), "khoảng trước", 40, INK, alpha=kb)
    text(d, (820, 1515), "9,8 cm", 56, GREEN, alpha=kb)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    setup(d, ghosts=[r[1] for r in ROWS])
    # A: phuong + chieu
    card(d, (QX0, 270, QX1, 590), fill=WHITE, outline=LIGHT, w=3)
    arrow(d, (450, 330), (450, 540), NAVY, w=8, head=24)
    text(d, (500, 380), "Phương thẳng đứng", 44, INK, anchor="lm")
    text(d, (500, 480), "Chiều từ trên xuống", 44, INK, anchor="lm")
    # B: toc do trung binh = khoang / 0,1 s, tang deu
    k1 = appear(t, M[1] - 0.1, 0.45)
    if k1 > 0:
        card(d, (QX0, 615, QX1, 1150), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
        text(d, (QC, 670), "tốc độ TB = khoảng ÷ 0,1 s", 40, SPEED, alpha=k1)
        sc_ = 380 / GAPS[-1]
        for i, g in enumerate(GAPS):
            kb = appear(t, M[1] + 0.2 + 0.25 * i, 0.3) * k1
            yy = 730 + i * 62
            x1 = QX0 + 60 + g * sc_ * kb
            d.rounded_rectangle([QX0 + 60, yy, x1, yy + 40], radius=8, fill=A(SPEED, kb))
            text(d, (QX0 + 60 + g * sc_ + 16, yy + 20), vn(g * 10, 0) + " cm/s", 38, SPEED, anchor="lm", alpha=kb)
        k2 = appear(t, M[1] + 1.8, 0.45) * k1
        text(d, (QC, 1105), "tăng đều: nhanh dần đều", 44, INK, alpha=k2)
    # C: chua noi duoc
    k3 = appear(t, M[2] - 0.1, 0.45)
    if k3 > 0:
        y0 = 1175 + (1 - k3) * 30
        card(d, (QX0, y0, QX1, y0 + 410), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (QC, y0 + 60), "Chưa nói được", 44, NAVY, alpha=k3)
        kk = k3 * appear(t, M[2] + 0.3, 0.4)
        card(d, (QX0 + 30, y0 + 125, QX1 - 30, y0 + 370), fill=A((254, 242, 242), kk), outline=A(RED, kk), r=24, w=4)
        text(d, (QC, y0 + 247), "Bi nặng hơn rơi khác?", 46, RED, alpha=kk)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    card(d, (40, 265, 1040, 815), fill=WHITE, outline=LIGHT, w=3)
    ytop, H5 = 330, 392.0                                 # hai cot cham cung tong chieu dai
    xa, xb = 330, 750
    for i in range(6):                                    # cot A: neu la chuyen dong deu (sai)
        y = ytop + H5 * i / 5
        d.ellipse([xa - 6, y - 6, xa + 6, y + 6], fill=GHOST, outline=STEEL, width=2)
    for si in (r[1] for r in ROWS):                       # cot B: quay cham (thuc)
        y = ytop + H5 * si / ROWS[-1][1]
        d.ellipse([xb - 6, y - 6, xb + 6, y + 6], fill=GHOST, outline=STEEL, width=2)
    text(d, (xa, 775), "đều?", 40, INK)
    text(d, (xb, 775), "thật", 40, INK)
    kx = appear(t, 1.0, 0.3)
    if kx > 0:
        d.line([(xa - 70, 380), (xa + 70, 680)], fill=A(RED, kx), width=8)
        d.line([(xa + 70, 380), (xa - 70, 680)], fill=A(RED, kx), width=8)
    a1 = appear(t, 0.2, 0.45); y0 = 840
    card(d, (40, y0, 1040, y0 + 750), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(RED, a1), r=32)
    text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
    q = "“Rơi nhanh quá, chắc là đều”"
    ks = clamp((t - 1.0) / 0.4); f = F(50); lw = tw(d, q, f); yy = y0 + 210
    text(d, (W / 2, yy), q, 50, mix(INK, MUTED, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=5)
    kk = a1 * appear(t, 1.5, 0.5)
    card(d, (90, y0 + 330, 990, y0 + 700), fill=A((239, 246, 255), kk), r=24)
    text(d, (W / 2, y0 + 515), "Thật: khoảng dài dần", 56, NAVY, alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    def hint(d, t, k):                                   # goi y tu ve, hien tre ~3,6 s
        kh = appear(t, M[0] + 3.6, 0.5)
        if kh <= 0: return
        card(d, (110, 1300, 970, 1530), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1360), "Gợi ý", 40, INK, alpha=kh)
        text(d, (W / 2, 1450), "Khoảng đầu: 0 → 0,2 s", 42, INK, alpha=kh)
    chot_hoi(d, t, sc, "Rơi tự do: thẳng đứng, xuống,\nnhanh dần đều",
             "Cùng cách thả, đánh dấu mỗi 0,2 s. Khoảng thứ hai dài hơn khoảng đầu bao nhiêu cm?",
             None, body=hint)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][0] + 0.3, "open"), (h["t0"] + h["T"] - 0.8, "ding")]
    for n in range(6): cs.append((do["t0"] + RUN0 + n * 0.1 * SLOW, "tap"))    # moi lan danh dau bong
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] + 1.8, "tap"),
           (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return cs

CLIP = dict(id="tn-l10-roi-tu-do-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Sự rơi tự do · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Bi rơi sau mỗi 0,1 s?", draw=s_hook, tail=0.6, caps=[
   ("Bi thép cạnh dây dọi.", 3.0),
   ("Dừng video, chọn câu trả lời.", 6.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.7, caps=[
   ("Quay chậm, dừng hình mỗi 0,1 s.", 4.4),
   ("Đọc vị trí tâm bi.", 3.9)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Trừ hai khoảng liền nhau.", 6.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.6, caps=[
   ("Bi luôn sát dây dọi.", 3.0),
   ("Chia mỗi khoảng cho 0,1 s.", 3.4),
   ("Mới thử một bi.", 3.4)]),
 dict(key="bay", title="Bẫy thường gặp", draw=s_bay, tail=0.4, caps=[
   ("Mắt thường không kịp thấy.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.5, caps=[
   ("Tự trả lời.", 5.6)]),
])
