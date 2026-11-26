# Clip: tn-l12-nllk-01 - Hai nam cham vong day nhau va chiec dai giu chung lai (28/10/2026)
# Dung lai 26/11/2026 theo KE-HOACH-CAI-TIEN-CLIP viec 4 lo 32: cong --do-chu, chu >= 56 px khi ve, <= 50 s,
#   Du doan khong nut A-D (K10), canh Bay + THU NGHI theo mau hatnhan3.
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-nllk-01.json:
#   so_lieu_mau: khong dai, tha tu do -> 18 mm (lo lung) ; khong dai, ep sat roi tha -> 18 mm (bat ve) ;
#                co dai siet -> 5 mm (ep sat, ca cum dung yen).
# Du doan (hien_tuong_hay_sai[0] "ep du manh thi tu dinh"): ep sat hai vong roi buong -> bat len, lo lung 18 mm.
# Bay (hien_tuong_hay_sai[2]): "luc hap dan giu proton" -> sai, hap dan qua nho (khong ghi so).
# Cau THU NGHI (= cau_chot khung web): thao dai khi hai vong dang cach 5 mm -> vong tren bat len, ve lo lung 18 mm
#   (cung so lieu hang 2: ep sat roi tha -> 18 mm). Lien he: bo luc giu thi cac phan day nhau tach ra.
# Hinh: hai vong cung cuc N quay vao nhau; cap F day la luc truc doi (cung do lon, nguoc chieu, dat vao hai vat).
from engine import *

DORANGE = (154, 52, 18); DG = (22, 120, 60)
S = 12                                # px / mm (d dung ti le)
RX, RW, RH = 400, 300, 130            # truc que, be rong vong, be day vong (ve)
BASE_Y = 900
LOW_TOP = BASE_Y - RH
D_EQ, D_BAND, D_LO = 18, 5, 1         # so_lieu_mau (mm); D_LO chi de ve luc ep sat
AX = 640

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-nllk-01.json")))
    h = k["so_lieu_mau"]["hang"]
    assert [r[1] for r in h] == [D_EQ, D_EQ, D_BAND]
_kiem_so()

def up_bot(dmm): return LOW_TOP - dmm * S

def pill(d, cx, cy, s, fill, alpha=1.0, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 38, cx + pw / 2, cy + 38), fill=A(fill, alpha), r=36)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); q = 1 - math.floor(p * 10 + 1e-9) / 10
    card(d, (190, y, 890, y + 70), fill=A(LIGHT, a), r=35)
    if q > 0: card(d, (190, y, 190 + max(70, 700 * q), y + 70), fill=A(col, a), r=35)

def dashed(d, p, q, color, w=3, seg=12, gap=9):
    L = math.dist(p, q); n = int(L // (seg + gap)) + 1
    for k in range(n):
        a = k * (seg + gap) / L; b = min(1, (k * (seg + gap) + seg) / L)
        if a >= 1: break
        d.line([(lerp(p[0], q[0], a), lerp(p[1], q[1], a)), (lerp(p[0], q[0], b), lerp(p[1], q[1], b))], fill=color, width=w)

# ---------------- thiet bi ----------------
def ring(d, ybot, top_pole, oy=0):
    x0, x1, ym = RX - RW // 2, RX + RW // 2, ybot - RH // 2
    ct, cb = (RED, BLUE) if top_pole == "N" else (BLUE, RED)
    lt, lb = (("N", "S") if top_pole == "N" else ("S", "N"))
    d.rounded_rectangle([x0, ybot - RH, x1, ym + 6], radius=12, fill=ct)
    d.rounded_rectangle([x0, ym - 6, x1, ybot], radius=12, fill=cb)
    d.rectangle([x0, ym - 6, x1, ym], fill=ct); d.rectangle([x0, ym, x1, ym + 6], fill=cb)
    for xx in (x0 + 60, x1 - 60):
        text(d, (xx, ybot - RH * 3 // 4), lt, 56, WHITE); text(d, (xx, ybot - RH // 4), lb, 56, WHITE)

def strap(d, dmm, alpha, dash=False):
    if alpha <= 0.02: return
    c = A(DG, alpha); top = up_bot(dmm) - RH - 12
    x0, x1 = RX - RW // 2 - 18, RX + RW // 2 + 18
    if dash:
        for xx in (x0, x1): dashed(d, (xx, top), (xx, BASE_Y), c, w=10, seg=22, gap=16)
        dashed(d, (x0, top + 4), (x1, top + 4), c, w=10, seg=22, gap=16); return
    for xx in (x0, x1): d.rounded_rectangle([xx - 8, top, xx + 8, BASE_Y - 2], radius=6, fill=c)
    d.line([(x0, top + 4), (x1, top + 4)], fill=c, width=14)

def apparatus(d, dmm, band=0.0, push=False, dash=False):
    d.rounded_rectangle([RX - 7, max(300, BASE_Y - 560), RX + 7, BASE_Y], radius=6, fill=(170, 175, 190))
    d.rounded_rectangle([190, BASE_Y, 610, BASE_Y + 46], radius=10, fill=(176, 124, 74))
    ring(d, BASE_Y, "N")
    ring(d, up_bot(dmm), "S")
    strap(d, dmm, band, dash)
    if push:
        yt = up_bot(dmm) - RH
        arrow(d, (RX, yt - 110), (RX, yt - 10), MUTED, w=10, head=28)
        text(d, (RX + 50, yt - 75), "tay ép", 56, INK, anchor="lm")

def bracket(d, dmm, a=1.0):
    ya, yb = up_bot(dmm), LOW_TOP
    x = 210
    d.line([(x, ya), (x, yb)], fill=A(INK, a), width=5)
    for yy in (ya, yb): d.line([(x - 16, yy), (x + 16, yy)], fill=A(INK, a), width=5)
    text(d, (x - 24, (ya + yb) / 2), f"{dmm} mm", 56, INK, anchor="rm", alpha=a)

def forces(d, dmm, mode, a=1.0):
    if a <= 0.02: return
    yb_u = up_bot(dmm); yt_u = yb_u - RH; yU = yb_u - RH / 2
    L = 120 if mode == "free" else 170
    arrow(d, (AX, yb_u), (AX, yb_u - L), A(RED, a), w=8, head=26)
    arrow(d, (AX, LOW_TOP), (AX, LOW_TOP + L), A(RED, a), w=8, head=26)
    text(d, (AX + 24, LOW_TOP + L - 20), "F đẩy", 56, RED, anchor="lm", alpha=a)
    if mode == "free":
        arrow(d, (AX + 200, yU), (AX + 200, yU + L), A(BLUE, a), w=8, head=26)
        text(d, (AX + 230, yU + L - 20), "P", 56, BLUE, anchor="lm", alpha=a)
    else:
        arrow(d, (AX + 200, yt_u), (AX + 200, yt_u + L), A(DG, a), w=8, head=26)
        text(d, (AX + 230, yt_u + 50), "đai", 56, DG, anchor="lm", alpha=a)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    apparatus(d, D_LO, push=True)
    M = sc["M"]; a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 66, "DỰ ĐOÁN", PURPLE, a)
    seg_bar(d, y0 + 130, t, M[1] + 0.3, sc["T"] - 0.3, PURPLE, a)
    text(d, (W / 2, y0 + 300), "Ép sát hai vòng rồi buông.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 405), "Vòng trên sẽ làm gì?", 62, PURPLE, alpha=a)

# ---------------- canh 2: Tien hanh ----------------
def d_at(t, sc):
    """buong tay luc 0,3 s -> dao dong tat dan ve 18 mm; siet dai tu M[1]+0.8 den M[1]+1.8 -> 5 mm."""
    M = sc["M"]; tb0, tb1 = M[1] + 0.8, M[1] + 1.8
    if t < 0.3: return D_LO
    if t < tb0:
        s = t - 0.3
        return D_EQ + (D_LO - D_EQ) * math.exp(-2.2 * s) * math.cos(2 * math.pi * 0.9 * s)
    if t < tb1: return lerp(D_EQ, D_BAND, ease((t - tb0) / (tb1 - tb0)))
    return D_BAND

def plot(d, box, t, sc):
    x0, y0, x1, y1 = box
    X = lambda tt: x0 + tt / sc["T"] * (x1 - x0)
    yb, yt = y1 - 50, y0 + 40
    Y = lambda v: yb - v / 22 * (yb - yt)
    d.line([(x0, yt - 10), (x0, yb)], fill=NAVY, width=4)
    d.line([(x0, yb), (x1 + 14, yb)], fill=NAVY, width=4)
    text(d, (x1 + 10, yb - 40), "t", 56, INK, anchor="rm")
    text(d, (x0 + 20, yt + 4), "d", 56, INK, anchor="lm")
    for v, col in ((D_EQ, GREEN), (D_BAND, DG)):
        dashed(d, (x0, Y(v)), (x1, Y(v)), A(col, 0.6), w=3)
        text(d, (x0 - 16, Y(v)), str(v), 56, col, anchor="rm")
    ts = [k / 300 * t for k in range(301)]
    if t > 0.05:
        d.line([(X(v), Y(d_at(v, sc))) for v in ts], fill=ORANGE, width=7, joint="curve")
        dot(d, X(t), Y(d_at(t, sc)), 13, RED, WHITE)

def s_do(img, d, t, sc):
    M = sc["M"]; dm = d_at(t, sc)
    band = clamp((t - M[1] - 0.6) / 0.3)
    apparatus(d, dm, band=band)
    k_eq = appear(t, 2.6, 0.4) * (1 - appear(t, M[1] + 0.7, 0.2))
    k_bd = appear(t, M[1] + 2.0, 0.4)
    if k_eq > 0:
        bracket(d, D_EQ, k_eq); forces(d, D_EQ, "free", k_eq)
        text(d, (W / 2, 1000), "lơ lửng", 60, GREEN, alpha=k_eq)
    if k_bd > 0:
        bracket(d, D_BAND, k_bd); forces(d, D_BAND, "band", k_bd)
        text(d, (W / 2, 1000), "đứng yên", 60, DG, alpha=k_bd)
    card(d, (40, 1060, 1040, 1560), fill=WHITE, outline=LIGHT, w=3)
    plot(d, (200, 1080, 960, 1550), t, sc)

# ---------------- canh 3: Dap an ----------------
ROWS = [("Thả", D_EQ), ("Ép rồi thả", D_EQ), ("Có đai", D_BAND)]   # so_lieu_mau

def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, W / 2, 310, "ĐÁP ÁN: bật lên", NAVY)
    card(d, (40, 390, 1040, 860), fill=WHITE, outline=LIGHT, w=3)
    text(d, (760, 450), "d (mm)", 56, NOTE)
    d.line([(70, 500), (1010, 500)], fill=LIGHT, width=3)
    for j, (nm, dm) in enumerate(ROWS):
        yy = 580 + j * 100
        if j == 1:
            pz = 0.5 + 0.5 * math.sin(t * 2 * math.pi / 1.2)
            d.rounded_rectangle([60, yy - 44, 1020, yy + 44], radius=16, fill=mix((255, 255, 255), (221, 214, 254), 0.3 + 0.7 * pz))
        col = DG if dm == D_BAND else INK
        text(d, (90, yy), nm, 60, INK, anchor="lm")
        text(d, (760, yy), str(dm), 62, col)
    k1 = appear(t, M[1] + 0.2, 0.45)
    if k1 > 0:
        card(d, (40, 920, 1040, 1150), fill=A((240, 253, 244), k1), outline=A(GREEN, k1), w=5)
        text(d, (W / 2, 1035), "Phải có lực giữ", 64, DG, alpha=k1)
        apparatus_mini(d, k1)

def apparatus_mini(d, a):
    for x in (360, 720):
        y = 1320
        d.rounded_rectangle([x - 110, y + 40, x + 110, y + 90], radius=10, fill=A(RED, a))
        dy = 120 if x == 360 else 40
        d.rounded_rectangle([x - 110, y - dy - 10, x + 110, y - dy + 40], radius=10, fill=A(BLUE, a))
        if x == 720:
            for xx in (x - 126, x + 126): d.rounded_rectangle([xx - 6, y - dy - 20, xx + 6, y + 90], radius=4, fill=A(DG, a))

NOTE = (70, 75, 95)

# ---------------- canh 4: Rut ra (hat nhan) ----------------
def proton(d, x, y, r, a=1.0):
    dot(d, x, y, r, A(RED, a), outline=A(WHITE, a))
    text(d, (x, y), "p", 60, WHITE, alpha=a)

def s_rutra(img, d, t, sc):
    M = sc["M"]; cx, cy = W / 2, 620
    k1 = appear(t, 0.3, 0.45); k2 = appear(t, M[1] + 0.3, 0.45)
    card(d, (40, 260, 1040, 1000), fill=A(WHITE, k1), outline=A(NAVY, k1), w=5)
    xl, xr = cx - 170, cx + 170
    proton(d, xl, cy, 62, k1); proton(d, xr, cy, 62, k1)
    for x, sg in ((xl, -1), (xr, 1)):
        arrow(d, (x, cy - 100), (x + sg * 150, cy - 100), A(RED, k1), w=9, head=28)
        if k2 > 0: arrow(d, (x, cy + 100), (x - sg * 200, cy + 100), A(GREEN, k2), w=9, head=28)
    text(d, (W / 2, 390), "điện: đẩy", 60, RED, alpha=k1)
    text(d, (W / 2, 850), "lực hạt nhân: hút", 60, GREEN, alpha=k2)
    if k2 > 0:
        for j, (l, r) in enumerate((("đai", "lực hạt nhân"),)):
            y = 1120
            text(d, (230, y), l, 62, DG, alpha=k2)
            arrow(d, (330, y), (500, y), A(INK, k2), w=8, head=26)
            text(d, (760, y), r, 62, GREEN, alpha=k2)

# ---------------- canh 5: Bay + chua noi ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; k1 = appear(t, 0.2, 0.4)
    card(d, (40, 260, 1040, 1100), fill=A(WHITE, k1), outline=A(RED, k1), w=6)
    pill(d, W / 2, 330, "BẪY", RED, k1)
    text(d, (W / 2, 445), "“Hấp dẫn giữ các prôtôn”?", 60, INK, alpha=k1)
    cy = 700; xl, xr = W / 2 - 170, W / 2 + 170
    proton(d, xl, cy, 58, k1); proton(d, xr, cy, 58, k1)
    gr = k1
    for x, sg in ((xl, -1), (xr, 1)):
        arrow(d, (x, cy - 95), (x + sg * 170, cy - 95), A(RED, k1), w=9, head=28)
        if gr > 0: arrow(d, (x, cy + 95), (x - sg * 34, cy + 95), A(MUTED, gr), w=6, head=16)
    text(d, (W / 2, 590), "điện", 56, RED, alpha=k1)
    text(d, (W / 2, 830), "hấp dẫn", 56, MUTED, alpha=gr)
    kv = appear(t, M[1] + 0.2, 0.4)
    if kv > 0:
        card(d, (340, 930, 740, 1040), fill=A((254, 226, 226), kv), outline=A(RED, kv), r=30, w=5)
        text(d, (W / 2, 985), "SAI", 72, RED, alpha=kv)
    k3 = appear(t, M[2] + 0.2, 0.45)
    if k3 > 0:
        card(d, (40, 1150, 1040, 1520), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, 1220), "Đai bó bên ngoài", 60, NAVY, alpha=k3)
        x, y = W / 2, 1400
        d.rounded_rectangle([x - 150, y + 10, x + 150, y + 60], radius=10, fill=A(RED, k3))
        d.rounded_rectangle([x - 150, y - 60, x + 150, y - 10], radius=10, fill=A(BLUE, k3))
        for xx in (x - 168, x + 168): d.rounded_rectangle([xx - 7, y - 75, xx + 7, y + 60], radius=4, fill=A(DG, k3))
        d.line([(x - 168, y - 72), (x + 168, y - 72)], fill=A(DG, k3), width=12)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 260, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 340, "THỬ NGHĨ", ORANGE, k1)
    seg_bar(d, 420, t, 0.8, sc["T"] - 0.2, ORANGE, k1)
    text(d, (W / 2, 570), "Đang cách 5 mm, tháo đai.", 60, INK, alpha=k1)
    text(d, (W / 2, 665), "Vòng trên sẽ làm gì?", 60, DORANGE, alpha=k1)
    global BASE_Y, LOW_TOP
    b0 = BASE_Y; BASE_Y = 1440; LOW_TOP = BASE_Y - RH
    try:
        if k1 > 0.5:
            apparatus(d, D_BAND, band=k1, dash=True)
    finally:
        BASE_Y = b0; LOW_TOP = BASE_Y - RH

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
            (do["t0"] + do["M"][1] + 1.8, "tap"), (da["t0"] + 0.2, "ding"),
            (b["t0"] + 0.2, "buzz"), (e["t0"] + 0.15, "open")]

SCENES = [
 dict(key="hook", title="Hai nam châm vòng trên một que", draw=s_hook, tail=0.2, caps=[
   ("Hai mặt N quay vào nhau.", 3.0),
   ("Dừng lại, tự đoán.", 4.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.2, caps=[
   ("Buông tay, đo khoảng cách d.", 3.6),
   ("Siết đai quanh hai vòng.", 4.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Ép sát vẫn bật về 18 mm.", 3.6),
   ("Có đai mới đứng yên.", 3.6)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.2, caps=[
   ("Hai prôtôn cũng đẩy nhau.", 3.4),
   ("Lực hạt nhân giữ chúng lại.", 3.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Đúng hay sai?", 2.8),
   ("Hấp dẫn quá nhỏ, không giữ nổi.", 3.2),
   ("Đai chỉ là mô hình.", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=2.4, caps=[
   ("Đẩy nhau mà đứng yên: cần lực giữ.", 3.8)]),
]

CLIP = dict(id="tn-l12-nllk-01", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Năng lượng liên kết hạt nhân · thachlab.id.vn", scenes=SCENES)
