# Clip: tn-l11-dien-truong-deu-02 - Do dien the tren giay dan dien giua hai dien cuc song song (30/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dien-truong-deu-02.json:
#   so_lieu_mau (x cm, V V, V/x V/m): 1 1,5 150 ; 2 3,0 150 ; 3 4,5 150 ; 4 6,0 150 ; 5 7,5 150
#   tham_so / dung_cu: U = 9,0 V (dieu chinh 3-12 V), d = 6,0 cm, von ke +-0,1 V.
#   ket_qua_ky_vong: dE = 10 V/m o x = 1 cm, 2 V/m o x = 5 cm. hien_tuong_hay_sai: de d bang cm -> 1,5.
#   Cau hoi chot: U = 12 V (max tham_so), d = 6,0 cm -> E = 200 V/m (chua tung hien tren man).
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (que duong do x = 1..5 cm, bang x - V) -> Dap an B (do thi V theo x
#       thang qua goc, cot V/x = 150 = U/d; hang x = 1 cm lech nhieu nhat) -> Bay (d de cm) roi Chua noi duoc ->
#       THU NGHI (12 V, khong hop chot, goi y 'doi d ra met', khong cong thuc).
# Cong moi 27/11: chu >= 56, bo nhip '+-0,1 V -> hang x nho kem tin cay' (la dap an cau Tu kiem tra q3 ngay sau video).
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

def setup(d, x=None, reading="– – –", show_d=False, pa=1.0, u="9,0", span=0.0, vk=True):
    d.line([(XN, 410), (XN, 300), (440, 300)], fill=NAVY, width=5)
    d.line([(bx(6), 410), (bx(6), 300), (480, 300)], fill=NAVY, width=5)
    d.line([(440, 278), (440, 322)], fill=NAVY, width=12)          # ban ngan, day: cuc am
    d.line([(480, 258), (480, 342)], fill=NAVY, width=5)           # ban dai: cuc duong
    text(d, (460, 240), f"U = {u} V", 56, INK)
    d.rectangle([110, 380, 810, 900], fill=PAPER)
    if span > 0: d.rectangle([bx(1), 390, bx(1) + 200 * span, 890], fill=A((255, 214, 110), 0.6))
    d.rectangle([XN + 12, 535, bx(6) - 12, 615], fill=RULER)       # thuoc nam TREN hang que do (y 640)
    for i in range(7):
        d.line([(bx(i), 535), (bx(i), 552)], fill=NAVY, width=3)
        if 1 <= i <= 5: text(d, (bx(i), 585), str(i), 56, INK)
    text(d, (XN + 60, 668), "cm", 56, WHITE, bold=False)
    for xc in (XN, bx(6)):
        d.rectangle([xc - 12, 410, xc + 12, 870], fill=COPPER, outline=NAVY, width=3)
    text(d, (XN + 46, 440), "−", 58, WHITE); text(d, (bx(6) - 46, 440), "+", 58, WHITE)
    if show_d:
        arrow(d, (460, 480), (XN + 16, 480), WHITE, w=4, head=18); arrow(d, (460, 480), (bx(6) - 16, 480), WHITE, w=4, head=18)
        card(d, (290, 410, 630, 470), fill=PAPER, r=10)
        text(d, (460, 440), "d = 6,0 cm", 56, WHITE)
    d.line([(420, 935), (420, 915), (XN, 915), (XN, 870)], fill=WIRE_NEG, width=6)
    card(d, (360, 935, 720, 1095), fill=(70, 78, 100), r=22)
    card(d, (390, 952, 690, 1075), fill=(220, 240, 225), r=12)
    text(d, (540, 1013), reading, 60, (20, 60, 30))
    if vk: text(d, (870, 1015), "vôn kế", 56, INK)
    dot(d, 420, 935, 11, WIRE_NEG); dot(d, 660, 935, 11, RED)
    if x is not None: probe(d, x, pa)

def table(d, n, vx=0, y=1130, hl=None, ka=1.0, col=0.0):
    """Bang x - V - V/x; n hang da co; vx = so hang da hien cot V/x (con lai '?')."""
    card(d, (40, y, 1040, y + 465), fill=WHITE, outline=NAVY, w=4)
    xs = (230, 520, 820)
    if col > 0: d.rounded_rectangle([660, y + 95, 1020, y + 455], radius=16, fill=A((255, 237, 213), col))
    for xx, c in zip(xs, ("x (cm)", "V (V)", "V/x (V/m)")): text(d, (xx, y + 50), c, 56, NAVY)
    d.line([(70, y + 92), (1010, y + 92)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 135 + i * 72; x, v, e = ROWS[i]
        if hl == i: d.rounded_rectangle([60, yy - 34, 1020, yy + 34], radius=16, fill=A((255, 237, 213), ka))
        text(d, (xs[0], yy), str(x), 56, INK); text(d, (xs[1], yy), vn(v), 56, INK)
        if i < vx: text(d, (xs[2], yy), str(e), 56, BLUE)
        else: text(d, (xs[2], yy), "?", 56, NAVY)

def pill(d, s, y, a, color=NAVY, size=58, cx=W / 2):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, y - 40, cx + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (cx, y), s, size, WHITE, alpha=a)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A((148, 140, 128), a), r=18, w=4)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong nut) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    e = (ease(clamp((t - 1.3) / 0.35)) + ease(clamp((t - 2.6) / 0.35))) / 2   # que nhay 1 -> 2 -> 3 cm (khong ghi so)
    x = 1 + 2 * e
    setup(d, x, show_d=True, pa=appear(t, 0.4, 0.4), span=e)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1130 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 450), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    text(d, (W / 2, y0 + 165), "Que dò dịch thêm từng 1 cm.", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 250), "Số chỉ vôn kế đổi thế nào?", 60, PURPLE, alpha=a)
    seg_bar(d, y0 + 330, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

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
GX0, GX1, GY0, GY1 = 190, 900, 980, 430        # truc do thi V theo x: x 0-6 cm, V 0-9 V (co dinh)
def gx(x): return GX0 + x / 6 * (GX1 - GX0)
def gy(v): return GY0 - v / 9 * (GY0 - GY1)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN: tăng đều", 290, 1.0)
    card(d, (40, 345, 1040, 1100), fill=WHITE, outline=LIGHT, w=3)
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=4)
    arrow(d, (GX0, GY1 - 10), (GX0, GY1 - 34), NAVY, w=4, head=16); arrow(d, (GX1 + 10, GY0), (GX1 + 34, GY0), NAVY, w=4, head=16)
    text(d, (GX0 + 24, GY1 - 30), "V (V)", 56, INK, anchor="lm")
    text(d, (GX1 + 40, GY0 - 45), "x (cm)", 56, INK, anchor="rm")
    for x in range(1, 6):
        d.line([(gx(x), GY0), (gx(x), GY0 + 12)], fill=NAVY, width=3); text(d, (gx(x), GY0 + 52), str(x), 56, INK, bold=False)
    for v in (3, 6, 9):
        d.line([(GX0 - 12, gy(v)), (GX0, gy(v))], fill=NAVY, width=3); text(d, (GX0 - 22, gy(v)), str(v), 56, INK, bold=False, anchor="rm")
    kl = appear(t, 0.9, 0.8)                         # duong thang qua goc qua 5 diem
    if kl > 0:
        x1 = 5 * kl
        d.line([(gx(0), gy(0)), (gx(x1), gy(1.5 * x1))], fill=A(GREEN, 0.9), width=6)
    kb = appear(t, 2.6, 0.4)                         # bac thang +1,5 V moi cm
    if kb > 0:
        for i in range(4):
            x, v = ROWS[i][0], ROWS[i][1]
            d.line([(gx(x), gy(v)), (gx(x + 1), gy(v))], fill=A(ORANGE, kb), width=6)
            d.line([(gx(x + 1), gy(v)), (gx(x + 1), gy(v + 1.5))], fill=A(ORANGE, kb), width=6)
        text(d, (gx(4.0) + 90, gy(6.0) + 70), "+1,5 V", 58, (176, 64, 8), alpha=kb, anchor="lm")
    for i, (x, v, e) in enumerate(ROWS):
        k = appear(t, 0.2 + 0.12 * i, 0.3)
        if k > 0: dot(d, gx(x), gy(v), 14, A(BLUE, k), outline=WHITE)
    km = appear(t, M[1] - 0.1, 0.4)
    if km > 0:
        card(d, (230, 470, 700, 560), fill=A(WHITE, km), outline=A(GREEN, km), r=20, w=4)
        text(d, (465, 515), "E đều: 150 V/m", 58, (10, 80, 40), alpha=km)
    table(d, 5, vx=5 if t >= M[1] - 0.1 else 0, y=1120, col=appear(t, M[1] + 2.6, 0.5))

# ---------------- canh 4: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = 1.0 - k2
    ke = ease(clamp((t - M[1] + 0.1) / 0.8))                       # que dich sat thanh duong: chua do
    setup(d, 3 + 2.7 * ke, "4,5 V" if ke == 0 else "? V", show_d=True)
    y0 = 1130
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 450), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y0 + 65, a1, DRED)
        q = "E = 9,0 : 6,0 = 1,5 V/m"
        ks = clamp((t - 0.3) / 0.4); f = F(58); lw = tw(d, q, f); yy = y0 + 200
        text(d, (W / 2, yy), q, 58, mix(DRED, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=6)
        text(d, (W / 2, y0 + 330), "✓ 9,0 : 0,060 = 150 V/m", 58, (10, 80, 40), alpha=a1 * appear(t, 3.0, 0.4))
    if k2 > 0:
        card(d, (40, y0, 1040, y0 + 450), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        pill(d, "CHƯA NÓI ĐƯỢC", y0 + 65, k2, NAVY)
        text(d, (W / 2, y0 + 200), "Sát mép thanh, E còn đều?", 58, INK, alpha=k2)

# ---------------- canh 5: THU NGHI (cau chot o khung: 12 V, 6,0 cm -> 200 V/m, khong hien) ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k = appear(t, 0.15, 0.4)
    setup(d, None, "– – –", u="12", vk=False)
    y0 = 1110
    card(d, (40, y0, 1040, 1590), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, "THỬ NGHĨ", y0 + 60, k, ORANGE)
    text(d, (W / 2, y0 + 155), "Nguồn 12 V, vẫn d = 6,0 cm.", 58, INK, alpha=k)
    text(d, (W / 2, y0 + 240), "E giữa hai thanh bao nhiêu?", 60, (176, 64, 8), alpha=k)
    seg_bar(d, y0 + 290, t, 1.0, sc["T"] - 0.2, ORANGE, k)
    kh = appear(t, M[0] + 3.0, 0.5)
    if kh > 0:
        card(d, (90, y0 + 380, 990, y0 + 470), fill=A((255, 237, 213), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, y0 + 425), "Gợi ý: U và d giờ là bao nhiêu?", 58, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
           (do["t0"] + S0, "tap")]
    out += [(do["t0"] + S0 + j * SW, "tick") for j in range(1, 5)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 1.4, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-dien-truong-deu-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Điện trường đều · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Dò điện thế trên giấy", draw=s_hook, tail=0.3, caps=[
   ("Que dò dịch xa thanh âm từng cm.", 3.2),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Que âm chạm thanh âm, que dương dò.", 4.4),
   ("Đọc vôn kế ở năm vị trí.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("Mỗi cm, số chỉ thêm 1,5 V.", 4.0),
   ("Chia V cho x ở từng hàng.", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Bẫy thường gặp.", 5.8),
   ("Mới đo ở giữa tờ giấy.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng lại, tự tính.", 7.4)]),
])
