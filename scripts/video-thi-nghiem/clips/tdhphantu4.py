# Clip: tn-l12-tdhphantu-04 - Qua bong bay trong nuoc nong va nuoc lanh: ap suat sinh ra tu va cham phan tu.
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-tdhphantu-04.json -> so_lieu_mau (vong quanh bong, cm):
#   27 °C (phong) 32,0 ; sau 1 phut trong nuoc 60 °C 32,9 ; sau 1 phut trong nuoc 5 °C 31,4. Kiem: _kiem_so().
# Ban 1 (27/11/2026, cong moi lo L11b; thay clip mo phong 16 s ngay 26/10): chu ve >= 56 px, <= 180 tu/phut moi canh,
#   nhip >= 2 s, K10 (khong nut A-D, "Dung lai, tu doan."), dem 5 o, the CHUA NOI DUOC >= 4 s, nhip Bay >= 3 s.
# Hop video trong bai (muc II.2, trong "Bam xem") ghi san "Rut ra: nong ... bong cang; lanh ... bong xep" -> KHONG hoi
#   chieu phong/xep. Du doan: nhung moi qua 1 phut (60 °C va 5 °C, bong o 27 °C), qua nao doi co NHIEU HON?
#   -> qua nong: +0,9 cm so voi -0,6 cm (chenh nhiet do 33 °C so voi 22 °C). Bai khong neu phep so nay.
# Hinh: do phong/xep cua bong VE PHONG TO x3 (32,9 vs 32,0 cm chi lech 3 %), co vong net dut co ban dau de so.
# Phan tu: cham trong bong, toc do ve ti le (nong 1,7 · phong 1,0 · lanh 0,55, chi dinh tinh); cham thanh thi loe cam.
# Bay = hien_tuong_hay_sai[0]: nuoc nong tham vao bong. Khong dung so cua Du doan.
# CHUA NOI DUOC: vo cao su gap nong co mem ra khong? (gia_thiet kho: bo qua doi do dan hoi cua vo).
# THU NGHI (= cau_chot khung, ca tu suy tu quan_sat[2] cua kho): lay qua nong ra, de o phong 27 °C vai phut ->
#   vong quanh tro ve gan 32,0 cm. Man chot khong cong thuc, khong goi y, khong hien 32,0 o man chot.
import random
from engine import *

ROWS = [("phong", 27, 32.0), ("nong", 60, 32.9), ("lanh", 5, 31.4)]
C0, C_HOT, C_COLD = 32.0, 32.9, 31.4

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-tdhphantu-04.json")))
    h = k["so_lieu_mau"]["hang"]
    assert [r[1] for r in h] == [C0, C_HOT, C_COLD]
    ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert ts["T_nong"]["mac_dinh"] == 60 and ts["T_lanh"]["mac_dinh"] == 5 and ts["T_p"]["gia_tri"] == 27
    assert round(C_HOT - C0, 1) == 0.9 and round(C0 - C_COLD, 1) == 0.6 and (60 - 27) > (27 - 5)
    assert "trở về ban đầu" in k["cac_buoc"]["quan_sat"][2]
_kiem_so()

def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
FS = 58
DGREEN = (21, 110, 55); DRED = (185, 28, 28); DORANGE = (176, 64, 8); DBLUE = (29, 78, 216)
BAL = (252, 207, 226); BAL_O = (190, 24, 93); HOTW = (254, 215, 170); COLDW = (191, 219, 254); BASIN = (90, 98, 120)

def pill(d, cx, cy, s, fill, alpha=1.0, size=FS, fg=WHITE):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, fg, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(LIGHT, a), r=18, w=4)

# ---------------- bong + phan tu ----------------
R0 = 150; KX = 3.0 * R0 / C0                      # px moi cm vong quanh, PHONG TO x3
def r_of(c): return R0 + (c - C0) * KX
_rng = random.Random(4)
MOLS = [(_rng.random() * 2, _rng.random() * 2, 0.8 + 0.6 * _rng.random(), 0.8 + 0.6 * _rng.random()) for _ in range(14)]
def tri(x): return 2 * abs((x % 2) - 1) - 1

def balloon(d, cx, cy, r, phase, a=1.0, ref=False, hits=True):
    if ref:                                        # vong net dut: co ban dau 32,0 cm
        for k in range(36):
            a0 = k * 10
            d.arc([cx - R0, cy - R0, cx + R0, cy + R0], a0, a0 + 5, fill=A(INK, a), width=4)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=A(BAL, a), outline=A(BAL_O, a), width=6)
    d.polygon([(cx - 16, cy + r + 18), (cx + 16, cy + r + 18), (cx, cy + r - 4)], fill=A(BAL_O, a))
    d.line([(cx, cy + r + 18), (cx + 10, cy + r + 70)], fill=A(INK, a), width=3)
    for ax, ay, fx, fy in MOLS:
        u, v = tri(ax + fx * phase), tri(ay + fy * phase)
        X, Y = u * math.sqrt(max(0, 1 - v * v / 2)), v * math.sqrt(max(0, 1 - u * u / 2))
        rr = r - 16
        dot(d, cx + X * rr, cy + Y * rr, 10, A(NAVY, a))
        if hits and (abs(u) > 0.93 or abs(v) > 0.93):
            n = math.hypot(X, Y) or 1
            hx, hy = cx + X / n * r, cy + Y / n * r
            d.ellipse([hx - 18, hy - 18, hx + 18, hy + 18], outline=A(ORANGE, a), width=5)

def phase_of(t, speed_fn, dt=0.04):
    s, x = 0.0, 0.0
    while x < t: s += speed_fn(x) * dt; x += dt
    return s

def basin(d, cx, y0, hot, a=1.0, level=1.0):
    d.line([(cx - 200, y0), (cx - 180, y0 + 190), (cx + 180, y0 + 190), (cx + 200, y0)], fill=A(BASIN, a), width=7)
    d.polygon([(cx - 196, y0 + 30), (cx + 196, y0 + 30), (cx + 180, y0 + 186), (cx - 180, y0 + 186)],
              fill=A(HOTW if hot else COLDW, 0.75 * a * level))
    if not hot:
        for k, (dx, dy) in enumerate(((-110, 60), (-20, 90), (80, 55), (130, 110))):
            d.rectangle([cx + dx - 22, y0 + dy - 22, cx + dx + 22, y0 + dy + 22], fill=A(WHITE, a), outline=A(DBLUE, a), width=3)
    else:
        for k in range(3):                                  # hoi nuoc nong
            x = cx - 90 + k * 90; yy = y0 + 10 - ((k * 30) % 60) * 0.3
            d.line([(x, yy), (x + 12, yy - 30), (x, yy - 60)], fill=A(DORANGE, 0.6 * a), width=4)

# ---------------- canh 1: Du doan ----------------
BX = (290, 790)
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    ph = t * 1.0
    for cx in BX:
        balloon(d, cx, 470, R0, ph)
        text(d, (cx, 270), "27 °C", 56, INK)
    basin(d, BX[0], 800, True); basin(d, BX[1], 800, False)
    text(d, (BX[0], 1050), "nước 60 °C", 56, DORANGE); text(d, (BX[1], 1050), "nước đá 5 °C", 56, DBLUE)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1100 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 480), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 180), "Nhúng mỗi quả 1 phút.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 280), "Quả nào đổi cỡ nhiều hơn?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 370, t, M[1], sc["T"] - 0.2, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
T_IN, T_OUT, T_READ = 0.6, 5.2, 6.4               # nhung xuong ; nhac ra ; doc so do
def dip(t):                                        # 0 = tren, 1 = trong chau
    return ease((t - T_IN) / 0.8) * (1 - ease((t - T_OUT) / 0.8))
def warm(t):                                       # 0 -> 1: khi trong bong da doi nhiet do
    return ease((t - T_IN - 0.4) / 3.2)
def sp_hot(t): return 1.0 + 0.7 * warm(t)
def sp_cold(t): return 1.0 - 0.45 * warm(t)

def s_do(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    k = dip(t); w = warm(t)
    for cx, hot in ((BX[0], True), (BX[1], False)):
        c = lerp(C0, C_HOT if hot else C_COLD, w)
        cy = 470 + 300 * k
        balloon(d, cx, cy, r_of(c), phase_of(t, sp_hot if hot else sp_cold), ref=True)
        basin(d, cx, 800, hot)
        if k > 0.05:                                       # nuoc phu len phan duoi bong
            d.polygon([(cx - 196, 830), (cx + 196, 830), (cx + 180, 986), (cx - 180, 986)], fill=A(HOTW if hot else COLDW, 0.55 * k))
    text(d, (BX[0], 270), "60 °C", 56, DORANGE); text(d, (BX[1], 270), "5 °C", 56, DBLUE)
    if T_IN < t < T_OUT + 0.4:                             # dong ho 1 phut (hinh quat)
        p = clamp((t - T_IN) / (T_OUT - T_IN)); cx, cy, rr = W / 2, 520, 56
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=WHITE, outline=NAVY, width=5)
        d.pieslice([cx - rr + 8, cy - rr + 8, cx + rr - 8, cy + rr - 8], -90, -90 + 360 * p, fill=ORANGE)
    kr = appear(t, T_READ, 0.4)
    if kr > 0:
        card(d, (40, 1080, 1040, 1300), fill=A(WHITE, kr), outline=A(LIGHT, kr), w=4)
        text(d, (W / 2, 1130), "vòng quanh (cm)", 56, INK, alpha=kr)
        text(d, (BX[0], 1230), "32,0 → 32,9", 60, DORANGE, alpha=kr)
        text(d, (BX[1], 1230), "32,0 → 31,4", 60, DBLUE, alpha=kr)
    kd = appear(t, M[2], 0.45)
    if kd > 0:
        card(d, (BX[0] - 170, 1340, BX[0] + 170, 1450), fill=A(HOTW, kd), r=24)
        card(d, (BX[1] - 170, 1340, BX[1] + 170, 1450), fill=A(COLDW, kd), r=24)
        text(d, (BX[0], 1395), "+0,9 cm", 62, DORANGE, alpha=kd)
        text(d, (BX[1], 1395), "−0,6 cm", 62, DBLUE, alpha=kd)

# ---------------- canh 3: Rut ra ----------------
def s_rut(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (50, 250, 1030, 400), fill=WHITE, outline=BLUE, w=6)
    text(d, (W / 2, 325), "Phân tử đập vào vỏ bóng", 62, BLUE)
    for cx, c, sp, lab, col in ((BX[0], C_HOT, 1.7, "60 °C", DORANGE), (BX[1], C_COLD, 0.55, "5 °C", DBLUE)):
        balloon(d, cx, 760, r_of(c) * 1.25, t * sp)
        text(d, (cx, 510), lab, 60, col)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        card(d, (50, 1150, 1030, 1320), fill=A(WHITE, k2), outline=A(DGREEN, k2), w=6)
        text(d, (W / 2, 1235), "Tổng các cú đập = áp suất khí", 58, DGREEN, alpha=k2)

# ---------------- canh 4: Bay - nuoc tham vao bong + CHUA NOI DUOC ----------------
B2 = 3.4
def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    k3 = appear(t, M[2] - 0.7, 0.45); a1 = 1.0 - k3
    if a1 > 0:
        card(d, (40, 250, 1040, 1300), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, W / 2, 320, "BẪY", DRED, a1)
        q = "Nước nóng thấm vào bóng"; lw = tw(d, q, F(62))
        text(d, (W / 2, 450), q, 62, DRED, alpha=a1)
        ks = clamp((t - B2) / 0.5)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, 454), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, 454)], fill=A(DRED, 0.85 * a1), width=5)
        cx, cy, r = W / 2, 800, 170
        balloon(d, cx, cy, r, t * 1.6, a=a1)
        for k in range(8):                                         # giot nuoc bat ra o vo
            ang = k * 45 + 20; ph = (t * 1.2 + k * 0.13) % 1.0
            dist = r + 20 + 70 * abs(1 - 2 * ph)
            dot(d, cx + dist * math.cos(math.radians(ang)), cy + dist * math.sin(math.radians(ang)), 12, A(DBLUE, a1))
        kk = appear(t, B2, 0.4) * a1
        if kk > 0:
            for k in range(4):                                     # mui ten nhiet (cam) di qua vo
                ang = math.radians(45 + k * 90); s0 = r + 90 - ((t * 120) % 60)
                arrow(d, (cx + s0 * math.cos(ang), cy + s0 * math.sin(ang)),
                      (cx + (s0 - 110) * math.cos(ang), cy + (s0 - 110) * math.sin(ang)), A(ORANGE, kk), w=7, head=20)
    if k3 > 0:
        card(d, (40, 300, 1040, 840), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 380, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 540), "Vỏ cao su gặp nóng", 62, INK, alpha=k3)
        text(d, (W / 2, 640), "có mềm ra không?", 62, INK, alpha=k3)
        cx, cy = W / 2, 1150; rr = 150 + 14 * math.sin(2.6 * t)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=A(BAL, k3), outline=A(BAL_O, k3), width=8 + int(4 * math.sin(2.6 * t)))
        text(d, (cx, cy), "?", 100, DRED, alpha=k3)

# ---------------- canh 5: THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 310, "THỬ NGHĨ", ORANGE, k)
    balloon(d, 300, 560, r_of(C_HOT) * 0.8, t * 1.7, a=k)
    text(d, (300, 380), "32,9 cm", 56, DORANGE, alpha=k)
    arrow(d, (480, 560), (640, 560), A(INK, k), w=7, head=24)
    text(d, (790, 560), "27 °C", 64, INK, alpha=k)
    text(d, (W / 2, 850), "Lấy quả nóng ra,", 64, INK, alpha=k)
    text(d, (W / 2, 940), "để ở phòng vài phút.", 64, INK, alpha=k)
    text(d, (W / 2, 1070), "Vòng quanh thế nào?", 66, DORANGE, alpha=k)
    seg_bar(d, 1260, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = (sc[x] for x in ("hook", "do", "rut", "bay", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding")]
    out += [(do["t0"] + T_IN, "tap"), (do["t0"] + T_READ, "tick"), (do["t0"] + do["M"][2], "ding")]
    out += [(r["t0"] + r["M"][1], "tap"), (b["t0"] + 0.3, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l12-tdhphantu-04", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Thuyết động học phân tử · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hai quả bóng như nhau", draw=s_hook, tail=0.3, caps=[
   ("Vòng quanh mỗi quả 32,0 cm.", 3.6),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Nhúng 1 phút, lấy ra, đo ngay.", 4.6),
   ("Đo vòng quanh bằng dây.", 3.6),
   ("Đáp án: quả nóng đổi nhiều hơn.", 3.6)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.3, caps=[
   ("Lạnh: chạy chậm, đập yếu.", 3.6),
   ("Nóng: chạy nhanh, đập mạnh.", 4.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Vỏ bóng kín, nước không vào.", 3.4),
   ("Chỉ có nhiệt đi qua vỏ.", 3.4),
   ("Còn một chỗ chưa rõ.", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 6.1)]),
])
