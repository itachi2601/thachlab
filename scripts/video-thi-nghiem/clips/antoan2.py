# Clip: tn-l10-an-toan-02 - Nhiet do canh ngon den con theo khoang cach (1/11/2026; dung lai 27/11/2026 theo cong moi
#   viec 4: --do-chu 0 LOI, chu ve >= 56 px, Du doan khong nut A-D (K10), thanh dem lien, cau chot A-D o khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-an-toan-02.json (_kiem_so() doi chieu):
#   so_lieu_mau: d = 2; 5; 10; 20 cm -> T = 125; 41; 29; 26 C, nong them 100; 16; 4; 1 C ; T_phong 25 C ;
#   mo_hinh T = 25 + 400/d^2, tham_so d 2..40 cm.
# Bai 47: hop exp dung TRUOC video, Quan sat/Rut ra da cho du 4 so va "5 -> 10 cm: 16 -> 4" -> Du doan KHONG hoi kieu giam,
#   ma hoi ca ngoai bang: d = 40 cm (theo mo hinh 25,25 C -> "khoang 25 C", sat nhiet do phong).
# Chot (THU NGHI, chua chieu): o 4 cm nhiet ke chi khoang? -> theo mo hinh 25 + 400/16 = 50 C (buoc suy luan: gap doi khoang
#   cach thi phan nong them con 1/4, clip KHONG noi quy tac nay, chi chieu cot nong them).
# Canh: Du doan -> Tien hanh (5 vi tri, bang) + DAP AN -> Rut ra (cot nong them) -> Chua noi duoc -> Bay (2 khung) -> THU NGHI.
from engine import *

DS = (2, 5, 10, 20); TS = (125, 41, 29, 26); NT = (100, 16, 4, 1); T_PH = 25

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-an-toan-02.json")))
    hang = k["so_lieu_mau"]["hang"]
    assert [tuple(h) for h in hang] == list(zip(DS, TS, NT))
    for dd, tt in zip(DS, TS): assert round(T_PH + 400 / dd ** 2) == tt
    assert round(T_PH + 400 / 40 ** 2) == 25 and T_PH + 400 / 4 ** 2 == 50
_kiem_so()

DRED = (185, 28, 28); DGREEN = (10, 110, 50); DPURP = (91, 33, 182); DORANGE = (176, 64, 8); DTEAL = (15, 100, 90)
FL_O = (251, 146, 60); FL_I = (59, 130, 246); LAMP = (200, 225, 240); LAMP_D = (120, 140, 160)
FX, PX = 150, 20                     # truc ngon lua, px moi cm (thuoc 0..40 cm)
def xd(c): return FX + c * PX
def tmod(c): return T_PH + 400.0 / (c * c)

def lamp(d, t, x, yb, s=1.0, a=1.0):
    """den con, day o yb, ngon lua tai x."""
    d.rounded_rectangle([x - 80 * s, yb - 110 * s, x + 80 * s, yb], radius=int(40 * s), fill=A(LAMP, a), outline=A(LAMP_D, a), width=5)
    d.rectangle([x - 20 * s, yb - 140 * s, x + 20 * s, yb - 108 * s], fill=A((203, 213, 225), a), outline=A(LAMP_D, a), width=3)
    w = 1 + 0.08 * math.sin(t * 9); top = yb - 330 * s + 14 * s * math.sin(t * 7)
    def drop(hw, yt, col):
        pts = [(x - hw * w * math.cos(math.pi * i / 24), yb - 150 * s - hw * 0.9 * math.sin(math.pi * i / 24)) for i in range(25)]
        pts.append((x, yt)); d.polygon(pts, fill=A(col, a))
    drop(32 * s, top, FL_O); drop(17 * s, top + 70 * s, FL_I)
    return yb - 220 * s                                                   # do cao giua ngon lua

def thermo(d, x, yc, T, s=1.0, a=1.0):
    """nhiet ke thuy tinh dung, bau o (x, yc); cot do 0..200 C."""
    top = yc - 260 * s
    d.rounded_rectangle([x - 13 * s, top, x + 13 * s, yc], radius=int(12 * s), fill=A((241, 245, 249), a), outline=A(NAVY, a), width=3)
    yl = yc - 18 * s - (yc - 18 * s - top - 8) * clamp(T / 200.0)
    d.rectangle([x - 5 * s, yl, x + 5 * s, yc - 10 * s], fill=A(RED, a))
    d.ellipse([x - 22 * s, yc - 22 * s, x + 22 * s, yc + 22 * s], fill=A(RED, a), outline=A(NAVY, a), width=3)

def bench(d, t, c, a=1.0, y0=240):
    """khung dung cu: den con + nhiet ke cach c cm + thuoc 0..40 cm (dung ti le)."""
    card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    yb = y0 + 420
    ym = lamp(d, t, FX, yb, a=a)
    d.line([(60, yb), (1020, yb)], fill=A((180, 170, 150), a), width=4)
    d.rectangle([FX - 20, yb + 4, xd(40) + 20, yb + 50], fill=A((254, 243, 199), a), outline=A((180, 150, 80), a), width=3)
    for k in range(0, 41, 5):
        d.line([(xd(k), yb + 4), (xd(k), yb + (26 if k % 10 == 0 else 16))], fill=A(NAVY, a), width=3)
    for k in (0, 10, 20, 30, 40):
        text(d, (xd(k), yb + 92), str(k), 56, INK, alpha=a)
    if c is not None:
        for yy in range(int(ym + 30), int(yb), 18):
            d.line([(xd(c), yy), (xd(c), min(yy + 9, yb))], fill=A(PURPLE, a), width=3)
        thermo(d, xd(c), ym, tmod(c), a=a)

def cbar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0))
    d.rounded_rectangle([110, y, 970, y + 80], radius=40, fill=A((246, 244, 250), a))
    if p < 1: d.rounded_rectangle([110, y, 110 + max(80, 860 * (1 - p)), y + 80], radius=40, fill=A(col, a))

def pill(d, y, s, col, k):
    pw = tw(d, s, F(56)) + 60
    card(d, (W / 2 - pw / 2, y, W / 2 + pw / 2, y + 76), fill=A(col, k), r=36)
    text(d, (W / 2, y + 38), s, 56, WHITE, alpha=k)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    k = appear(t, M[1] - 0.3, 0.45)
    c = lerp(20, 40, ease((t - M[1] + 0.3) / 1.2)) if k > 0 else 20
    bench(d, t, c, a)
    card(d, (40, 830, 1040, 970), fill=A(WHITE, a), outline=A(TEAL, a), w=4)
    text(d, (W / 2, 900), "20 cm: nhiệt kế 26 °C", 60, DRED, alpha=a)
    if k <= 0: return
    y0 = 1030 + (1 - k) * 30
    card(d, (50, y0, 1030, y0 + 520), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, y0 + 22, "DỰ ĐOÁN", PURPLE, k)
    cbar(d, y0 + 118, t, M[1] + 0.3, sc["T"] - 0.15, DPURP, k)
    text(d, (W / 2, y0 + 290), "Dời ra 40 cm:", 62, INK, alpha=k)
    text(d, (W / 2, y0 + 385), "nhiệt kế chỉ khoảng", 62, INK, alpha=k)
    text(d, (W / 2, y0 + 470), "bao nhiêu °C?", 62, PURPLE, alpha=k)

# ---------------- canh 2: Tien hanh ----------------
DD = DS + (40,); STEP, MOVE = 1.5, 0.7
ROWS = [(str(c), str(tt)) for c, tt in zip(DS, TS)] + [("40", "≈ 25")]
def s_do(img, d, t, sc):
    M = sc["M"]; ts = 0.4
    i = max(0, min(4, int((t - ts) // STEP)))
    s = ts + i * STEP
    c = DD[i] if i == 0 else lerp(DD[i - 1], DD[i], ease((t - s) / MOVE))
    bench(d, t, c)
    n = min(5, i + 1 if (t >= s + MOVE or i == 0) else i)
    card(d, (40, 960, 1040, 1590), fill=WHITE, outline=NAVY, w=4)
    text(d, (300, 1030), "Cách lửa", 58, BLUE); text(d, (760, 1030), "Nhiệt kế", 58, DRED)
    d.line([(80, 1075), (1000, 1075)], fill=NAVY, width=3)
    for j in range(n):
        y = 1130 + j * 85
        if j == n - 1: d.rounded_rectangle([70, y - 36, 1010, y + 36], radius=14, fill=(255, 241, 222))
        text(d, (300, y), ROWS[j][0] + " cm", 58, BLUE)
        text(d, (760, y), ROWS[j][1] + " °C", 58, DRED if j < 4 else DTEAL)
    kc = appear(t, M[2] + 0.3, 0.4)
    if kc > 0:
        s_ = "ĐÁP ÁN: khoảng 25 °C"; pw = tw(d, s_, F(58)) + 70
        card(d, (W / 2 - pw / 2, 810, W / 2 + pw / 2, 910), fill=A((220, 252, 231), kc), outline=A(GREEN, kc), r=28, w=5)
        text(d, (W / 2, 860), s_, 58, DGREEN, alpha=kc)

# ---------------- canh 3: Rut ra ----------------
def s_rut(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.05, 0.35)
    card(d, (40, 240, 1040, 1100), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    text(d, (W / 2, 310), "Nóng hơn phòng (°C)", 60, DORANGE, alpha=a)
    yb = 890; g = ease((t - 0.3) / 1.6)
    d.line([(90, yb), (1000, yb)], fill=A(NAVY, a), width=4)
    vals = NT + (0,)
    for j, v in enumerate(vals):
        x = 160 + j * 185; h = v * 4.8 * g
        if v > 0: d.rectangle([x - 55, yb - h, x + 55, yb], fill=A((253, 186, 116), a), outline=A(DORANGE, a), width=4)
        text(d, (x, yb - h - 40), str(v) if v else "≈ 0", 56, DORANGE, alpha=a)
        text(d, (x, yb + 48), str(DD[j]), 56, BLUE, alpha=a)
    text(d, (W / 2, 1040), "cách lửa (cm)", 56, BLUE, alpha=a)
    kr = appear(t, M[1] + 0.1, 0.4)
    if kr > 0:
        card(d, (60, 1160, 1020, 1300), fill=A((236, 253, 243), kr), outline=A(GREEN, kr), r=28, w=5)
        text(d, (W / 2, 1230), "Ra xa: nguội rất nhanh", 60, DGREEN, alpha=kr)
        lamp(d, t, 220, 1560, 0.7, kr)                                  # nguoi dung xa ngon lua
        xp = 640 + 180 * ease((t - M[1] - 0.3) / 1.2)                   # hinh nguoi lui ra xa den
        dot(d, xp, 1370, 36, A(NAVY, kr))
        d.line([(xp, 1406), (xp, 1490)], fill=A(NAVY, kr), width=14)
        d.line([(xp - 50, 1440), (xp + 50, 1440)], fill=A(NAVY, kr), width=12)
        for sx in (-34, 34): d.line([(xp, 1488), (xp + sx, 1560)], fill=A(NAVY, kr), width=12)
        arrow(d, (360, 1600), (xp - 20, 1600), A(DGREEN, kr), w=8, head=26)
        text(d, (W / 2 + 40, 1640), "đứng xa", 56, DGREEN, alpha=kr)

# ---------------- canh 4: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    k = appear(t, 0.05, 0.35)
    card(d, (60, 240, 1020, 640), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, 325), "Chưa nói được", 62, NAVY, alpha=k)
    text(d, (W / 2, 455), "Quy luật thật", 60, INK, alpha=k)
    text(d, (W / 2, 545), "của ngọn lửa", 60, INK, alpha=k)
    lamp(d, t * 2.2, 380, 1320, 1.3, k)
    text(d, (760, 1000 + 50 * math.sin(t * 3.2)), "?", 150, NAVY, alpha=k)

# ---------------- canh 5: Bay ----------------
def mini(d, t, y0, wrong, k):
    col = DRED if wrong else DGREEN
    card(d, (60, y0, 1020, y0 + 640), fill=A(WHITE, k), outline=A(col, k), w=6)
    text(d, (W / 2, y0 + 70), "✗ Ngoài lửa là mát" if wrong else "✓ 5 cm: 41 °C", 62, col, alpha=k)
    ym = lamp(d, t, 230, y0 + 590, 0.85, k)
    thermo(d, 230 + 5 * 40, ym, 41, 0.85, k)
    if wrong:
        fl = 0.5 + 0.5 * math.sin(t * 9)
        d.ellipse([400, ym - 70, 540, ym + 70], outline=A(RED, k * fl), width=8)
        text(d, (780, y0 + 380), "hết nóng?", 58, DRED, alpha=k)
    else:
        g = 0.5 + 0.5 * math.sin(t * 4)
        d.rounded_rectangle([600, y0 + 300, 960, y0 + 460], radius=24, fill=A(mix((255, 241, 222), (253, 186, 116), g), k))
        text(d, (780, y0 + 380), "> phòng 25 °C", 58, DRED, alpha=k)

def s_bay(img, d, t, sc):
    M = sc["M"]
    mini(d, t, 240, True, appear(t, 0.05, 0.3))
    kb = appear(t, M[1] - 0.05, 0.35)
    if kb > 0: mini(d, t, 930, False, kb)

# ---------------- canh 6: THU NGHI ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 220, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, 250, "THỬ NGHĨ", ORANGE, k1)
    ym = lamp(d, t, 300, 900, 1.0, k1)
    thermo(d, 300 + 4 * 40, ym, 0, 1.0, k1)
    for yy in range(int(ym + 30), 900, 18):
        d.line([(460, yy), (460, min(yy + 9, 900))], fill=A(PURPLE, k1), width=3)
    text(d, (780, 760), "4 cm", 62, PURPLE, alpha=k1)
    text(d, (780, 860 + 20 * math.sin(t * 3)), "?", 110, ORANGE, alpha=k1)
    text(d, (W / 2, 1040), "Ở 4 cm, nhiệt kế", 60, INK, alpha=k1)
    text(d, (W / 2, 1130), "chỉ khoảng bao nhiêu?", 60, ORANGE, alpha=k1)
    cbar(d, 1250, t, 1.0, sc["T"] - 0.2, DORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + 0.4 + i * STEP + MOVE, "tick") for i in range(5)]
    out += [(do["t0"] + do["M"][2] + 0.3, "ding"), (r["t0"] + r["M"][1] + 0.1, "tap"), (b["t0"] + 0.3, "buzz"),
            (b["t0"] + b["M"][1] + 0.1, "ding"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l10-an-toan-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="An toàn phòng thực hành · thachlab.id.vn", scenes=[
 dict(key="hook", title="Đèn cồn và nhiệt kế", draw=s_hook, tail=0.3, caps=[
   ("Lớp đứng xa quan sát.", 3.6),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Dời nhiệt kế ra xa", draw=s_do, tail=0.3, caps=[
   ("Đợi số chỉ ổn định.", 3.4),
   ("Điểm 40 cm theo mô hình.", 4.0),
   ("So với mức phòng.", 3.0)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.3, caps=[
   ("Gần lửa nóng hơn nhiều lần.", 3.6),
   ("Lùi ra, đỡ nóng hẳn.", 3.9)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.4, caps=[
   ("Số này là minh hoạ.", 4.6)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Dễ tưởng: ra khỏi lửa là hết nóng.", 3.6),
   ("Đo thật: vẫn nóng hơn phòng.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự trả lời.", 5.6)]),
])
