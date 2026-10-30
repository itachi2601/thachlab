# Clip: tn-l11-dien-truong-deu-02 - Do dien the tren giay dan dien giua hai dien cuc song song (30/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dien-truong-deu-02.json:
#   so_lieu_mau (x cm, V V, V/x V/m): 1 1,5 150 ; 2 3,0 150 ; 3 4,5 150 ; 4 6,0 150 ; 5 7,5 150
#   tham_so / dung_cu: U = 9,0 V (dieu chinh 3-12 V), d = 6,0 cm, von ke +-0,1 V.
#   ket_qua_ky_vong: dE = 10 V/m o x = 1 cm, 2 V/m o x = 5 cm. hien_tuong_hay_sai: de d bang cm -> 1,5.
#   Cau hoi chot: U = 12 V (max tham_so), d = 6,0 cm -> E = 200 V/m (chua tung hien tren man).
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (que duong do x = 1..5 cm, bang x - V) -> Dap an B (do thi V theo x
#       thang qua goc, cot V/x = 150 = U/d; hang x = 1 cm lech nhieu nhat) -> Bay (d de cm) roi Chua noi duoc ->
#       Chot + cau hoi tu nho lai (12 V).
# Chieu E: tu thanh + sang thanh - (dien the giam), khong ve duong suc o day de khoi roi hinh.
from engine import *

ROWS = [(1, 1.5, 150), (2, 3.0, 150), (3, 4.5, 150), (4, 6.0, 150), (5, 7.5, 150)]   # so_lieu_mau
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
PAPER = (92, 96, 108); COPPER = (200, 120, 62); RULER = (246, 236, 200); DRED = (185, 28, 28)
WIRE_NEG = (30, 30, 36)

# ---------------- dung cu (khung nguon 1080x1920) ----------------
XN, PXC = 160, 100                      # thanh am o x = 160 px; 100 px / cm -> thanh duong o 760 (d = 6,0 cm)
def bx(x): return XN + PXC * x
PY = 640                                # que do cham giay o giua to giay (thanh tu 410 den 870)

def probe(d, x, a=1.0):
    tx = bx(x)
    d.line([(tx + 56, 762), (660, 935)], fill=A(RED, a), width=5)                    # day do -> cuc + von ke (duoi thuoc)
    d.line([(tx + 4, PY + 6), (tx + 30, 700)], fill=A((60, 60, 70), a), width=6)      # dau kim
    d.line([(tx + 26, 692), (tx + 58, 764)], fill=A(RED, a), width=22)                # than que do (cheo xuong phai)
    dot(d, tx, PY, 9, A(YELLOW, a), outline=A(NAVY, a))

def setup(d, x=None, reading="– – –", show_d=False, pa=1.0, arrow_move=0.0):
    # nguon + day noi hai thanh
    d.line([(XN, 410), (XN, 300), (440, 300)], fill=NAVY, width=5)
    d.line([(bx(6), 410), (bx(6), 300), (480, 300)], fill=NAVY, width=5)
    d.line([(440, 278), (440, 322)], fill=NAVY, width=12)          # ban ngan, day: cuc am
    d.line([(480, 258), (480, 342)], fill=NAVY, width=5)           # ban dai: cuc duong
    text(d, (460, 238), "U = 9,0 V", 40, INK)
    # giay dan dien + thuoc
    d.rectangle([110, 380, 810, 900], fill=PAPER)
    d.rectangle([XN + 12, 540, bx(6) - 12, 610], fill=RULER)       # thuoc nam TREN hang que do (y 640)
    for i in range(7):
        d.line([(bx(i), 540), (bx(i), 560)], fill=NAVY, width=3)
        if 1 <= i <= 5: text(d, (bx(i), 586), str(i), 38, INK)
    text(d, (bx(5) + 50, 586), "cm", 38, INK, bold=False)
    # hai thanh dong
    for xc in (XN, bx(6)):
        d.rectangle([xc - 12, 410, xc + 12, 870], fill=COPPER, outline=NAVY, width=3)
    text(d, (XN + 46, 440), "−", 56, WHITE); text(d, (bx(6) - 46, 440), "+", 56, WHITE)
    if show_d:
        arrow(d, (460, 490), (XN + 16, 490), WHITE, w=4, head=18); arrow(d, (460, 490), (bx(6) - 16, 490), WHITE, w=4, head=18)
        text(d, (460, 450), "d = 6,0 cm", 40, WHITE)
    # von ke + day que am
    d.line([(420, 935), (420, 915), (XN, 915), (XN, 870)], fill=WIRE_NEG, width=6)
    card(d, (360, 935, 720, 1095), fill=(70, 78, 100), r=22)
    card(d, (390, 952, 690, 1040), fill=(220, 240, 225), r=12)
    text(d, (540, 996), reading, 52, (20, 60, 30))
    text(d, (540, 1068), "vôn kế", 38, WHITE)
    dot(d, 420, 935, 11, WIRE_NEG); dot(d, 660, 935, 11, RED)
    if x is not None: probe(d, x, pa)
    if arrow_move > 0:                                              # que dich sang phai tung cm (khong ghi so)
        arrow(d, (bx(1) + 24, 640), (bx(1) + 24 + 220 * arrow_move, 640), A(ORANGE, arrow_move), w=6, head=20)

def table(d, n, vx=0, y=1120, hl=None, ka=1.0):
    """Bang x - V - V/x; n hang da co; vx = so hang da hien cot V/x (con lai '?')."""
    card(d, (40, y, 1040, y + 470), fill=WHITE, outline=NAVY, w=4)
    xs = (230, 530, 830)
    for xx, c in zip(xs, ("x (cm)", "V (V)", "V/x (V/m)")): text(d, (xx, y + 50), c, 40, INK)
    d.line([(70, y + 88), (1010, y + 88)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 130 + i * 72; x, v, e = ROWS[i]
        if hl == i: d.rounded_rectangle([60, yy - 34, 1020, yy + 34], radius=16, fill=A((255, 237, 213), ka))
        text(d, (xs[0], yy), str(x), 42, INK); text(d, (xs[1], yy), vn(v), 42, INK)
        if i < vx: text(d, (xs[2], yy), str(e), 44, BLUE)
        else: text(d, (xs[2], yy), "?", 42, MUTED)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    setup(d, 1, show_d=True, pa=appear(t, 0.4, 0.4), arrow_move=appear(t, 1.0, 0.8))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1120 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 480), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 38, WHITE, alpha=a)
    ctext(d, y0 + 235, "Mỗi lần que dò dịch thêm\n1 cm, số chỉ vôn kế\nthay đổi thế nào?", 48, INK, maxw=900, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.6
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 430, 940, y0 + 442], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 430, 140 + 800 * (1 - p), y0 + 442], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
S0, SW = 1.0, 1.6          # que toi x = 1 o S0, moi vi tri tiep theo cach SW giay; truot 0,5 s

def s_do(img, d, t, sc):
    k = max(0, min(4, int((t - S0) // SW))) if t >= S0 else -1
    if k < 0:
        setup(d, 1, "– – –"); table(d, 0); return
    w = t - S0 - k * SW
    if k > 0 and w < 0.5:                                          # dang truot tu x = k sang x = k + 1
        x = k + ease(w / 0.5); setup(d, x, "– – –")
        table(d, k); return
    x, v, e = ROWS[k]
    shown = w >= (0.5 if k > 0 else 0.0) + 0.05                     # so von ke va hang bang hien CUNG luc
    setup(d, x, vn(v) + " V" if shown else "– – –")
    table(d, k + (1 if shown else 0))

# ---------------- canh 3: Dap an + rut ra ----------------
GX0, GX1, GY0, GY1 = 170, 920, 980, 400        # truc do thi V theo x: x 0-6 cm, V 0-9 V (co dinh)
def gx(x): return GX0 + x / 6 * (GX1 - GX0)
def gy(v): return GY0 - v / 9 * (GY0 - GY1)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    pw = tw(d, "ĐÁP ÁN · tăng đều", F(38)) + 52
    card(d, (W - 60 - pw, 236, W - 60, 296), fill=A(NAVY, ka), r=30)
    text(d, (W - 60 - pw / 2, 266), "ĐÁP ÁN · tăng đều", 38, WHITE, alpha=ka)
    card(d, (40, 316, 1040, 1080), fill=WHITE, outline=LIGHT, w=3)
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=4)
    arrow(d, (GX0, GY1 - 10), (GX0, GY1 - 34), NAVY, w=4, head=16); arrow(d, (GX1 + 10, GY0), (GX1 + 34, GY0), NAVY, w=4, head=16)
    text(d, (GX0 + 20, GY1 - 50), "V (V)", 38, INK, anchor="lm")
    text(d, (GX1 + 34, GY0 - 40), "x (cm)", 38, INK, anchor="rm")
    for x in range(1, 7):
        d.line([(gx(x), GY0), (gx(x), GY0 + 12)], fill=NAVY, width=3); text(d, (gx(x), GY0 + 42), str(x), 38, MUTED, bold=False)
    for v in (3, 6, 9):
        d.line([(GX0 - 12, gy(v)), (GX0, gy(v))], fill=NAVY, width=3); text(d, (GX0 - 22, gy(v)), str(v), 38, MUTED, bold=False, anchor="rm")
    kl = appear(t, 0.9, 0.8)                         # duong thang qua goc qua 5 diem
    if kl > 0:
        x1 = 5 * kl
        d.line([(gx(0), gy(0)), (gx(x1), gy(1.5 * x1))], fill=A(GREEN, 0.9), width=5)
        if kl >= 1: text(d, (gx(3.4), gy(4.5) + 20), "đường thẳng qua gốc", 38, GREEN, anchor="lt")
    for i, (x, v, e) in enumerate(ROWS):
        k = appear(t, 0.2 + 0.12 * i, 0.3)
        if k > 0: dot(d, gx(x), gy(v), 13, A(ORANGE if (i == 0 and t >= M[1] - 0.1) else BLUE, k), outline=WHITE)
    hl = 0 if t >= M[1] - 0.1 else None
    table(d, 5, vx=sum(t >= 0.4 + 0.2 * i for i in range(5)), hl=hl, ka=appear(t, M[1] - 0.1, 0.3))
    # the ghi chu o vung trong tren-trai cua do thi (duoi nhan truc V, ben trai duong thang)
    k1 = appear(t, 1.8, 0.4) * (1 - appear(t, M[1] - 0.1, 0.3))
    k2 = appear(t, M[1] + 0.3, 0.4)
    if k1 > 0:
        card(d, (215, 450, 705, 540), fill=A(WHITE, k1), outline=A(GREEN, k1), r=20, w=4)
        text(d, (460, 495), "V/x = 150 V/m mọi hàng", 40, (10, 80, 40), alpha=k1)
    if k2 > 0:
        card(d, (215, 450, 705, 540), fill=A((255, 237, 213), k2), outline=A(ORANGE, k2), r=20, w=3)
        text(d, (460, 495), "±0,1 V : 0,010 m = ±10 V/m", 38, (130, 40, 10), alpha=k2)

# ---------------- canh 4: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    setup(d, 3, "4,5 V", show_d=True)
    if a1 > 0:
        y0 = 1120
        card(d, (40, y0, 1040, y0 + 470), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
        q = "E = 9,0 : 6,0 = 1,5 V/m"
        ks = clamp((t - 1.2) / 0.4); f = F(48); lw = tw(d, q, f); yy = y0 + 200
        text(d, (W / 2, yy), q, 48, DRED, alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=4)
        ctext(d, y0 + 340, "✓ E = 9,0 : 0,060 = 150 V/m", 48, (10, 80, 40), maxw=900, alpha=a1 * appear(t, 1.7, 0.5))
    if k2 > 0:
        y0 = 1120 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 470), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        ctext(d, y0 + 250, "Sát mép thanh, E còn đều?", 48, INK, maxw=900, alpha=k2 * appear(t, M[1] + 0.3, 0.4))

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: nguon 12 V, d giu 6,0 cm, E bao nhieu (HS tu doi d ra m); goi y tre 4,5 s, khong lam ho buoc doi."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 260, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 390, "Giữa hai thanh song song,\nđiện trường là đều", 50, (10, 80, 40), maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.6, 0.5)
    if k1 <= 0: return
    card(d, (40, 580, 1040, 1200), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 610, W / 2 + pw / 2, 674), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 642), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 830, "Nguồn 12 V, hai thanh vẫn\ncách 6,0 cm. E giữa hai\nthanh khoảng bao nhiêu V/m?", 46, INK, maxw=920,
          alpha=appear(t, M[0] + 0.9, 0.5))
    kh = appear(t, M[0] + 0.9 + 4.5, 0.5)
    card(d, (110, 955, 970, 1165), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1005, "Gợi ý", 40, (154, 52, 18), alpha=kh)
    ctext(d, 1100, "E = U/d — nhớ cảnh bẫy", 46, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
           (do["t0"] + S0, "tap")]
    out += [(do["t0"] + S0 + j * SW, "tick") for j in range(1, 5)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.6, "open")]
    return out

CLIP = dict(id="tn-l11-dien-truong-deu-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Điện trường đều · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Dò điện thế trên giấy", draw=s_hook, tail=0.8, caps=[
   ("Que dò dịch xa thanh âm từng cm.", 3.2),
   ("Tự đoán trước khi xem tiếp.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Que âm chạm thanh âm, que dương dò.", 4.4),
   ("Đọc vôn kế ở năm vị trí.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Mỗi cm, số chỉ thêm 1,5 V.", 3.8),
   ("Hàng x nhỏ kém tin cậy nhất.", 4.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy thường gặp.", 3.6),
   ("Mới đo ở giữa tờ giấy.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Dừng video, tự trả lời.", 8.4)]),
])
