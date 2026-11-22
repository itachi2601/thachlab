# Clip: tn-l12-phongxa-02 - Theo doi do phong xa giam theo thoi gian de doc chu ki ban ra
# So lieu lay nguyen tu content/thi-nghiem/tn-l12-phongxa-02.json (_kiem_so() doi chieu so_lieu_mau, tham_so).
# Ban 1 (28/10/2026): mau boyle. Ban 2 (21/11/2026, KE-HOACH-CAI-TIEN-CLIP viec 4 lo 20): cong --do-chu
#   (chu ve >= 55 px, <= 180 tu/phut moi canh, nhip >= 2 s), <= 50 s, K10 (khong nut A-D).
# Quan niem sai can danh (hien_tuong_hay_sai[0]): so dem giam DEU theo duong thang (hieu hai lan doc la hang so).
# Du doan: da tru phong, phut 0 = 812, phut 5 = 398 -> phut 10 con khoang bao nhieu? Giam deu thi ~0; that ra 204.
# Thu tu: Du doan -> Tien hanh (do phong 23, dem 5 hang 0-20 phut) -> Dap an (do thi: duong thang "giam deu"
#   cat truc o ~phut 10, diem that 204 = mot nua) -> Vi sao (60 hat nhan, cung xac suat; chua noi duoc gi)
#   -> Bay "tru hai so lien nhau" (hieu nho dan, ti so ~2) -> Chot + THU NGHI.
#   Hang 25 phut (47 / 24, ti so 2,17) KHONG chieu: bai ly thuyet de hai o hang cuoi "em tu tinh";
#   ti so 1,60 khi quen tru phong cung khong chieu (bai co cau "Thu chia hai so chua tru phong o phut 20 va 25").
# Thu nghi (= cau_chot khung web): phut 0 -> 5 so dem giam 414; phut 20 -> 25 giam khoang bao nhieu?
#   -> hieu cung chia doi moi T: 414 / 16 ~ 26; so lieu that 52 - 24 = 28 -> "khoang 30". Dap so khong hien tren man.
import random
from engine import *

ROWS = [(0, 835, 812), (5, 421, 398), (10, 227, 204), (15, 120, 97), (20, 75, 52)]  # so_lieu_mau hang 1-5
PHONG, T_BR, H0 = 23, 5, 810                       # tham_so: phong nen, T mac dinh, H0 (mo hinh trong ghi_chu)
RATIOS = ["2,04", "1,95", "2,10", "1,87"]           # so_lieu_mau.ghi_chu: ti so hai lan lien tiep (da tru phong)
DROP0 = ROWS[0][2] - ROWS[1][2]                    # 414: giam trong 5 phut dau (cau THU NGHI)
def model(m): return H0 * 2 ** (-m / T_BR)          # chi dung de ve mat do hat / duong mo, khong in so

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-phongxa-02.json")))
    hang = [tuple(r) for r in k["so_lieu_mau"]["hang"]]
    for r in ROWS: assert r in hang, r
    for r in RATIOS: assert r in k["so_lieu_mau"]["ghi_chu"], r
    ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert ts["phong"]["mac_dinh"] == PHONG and ts["T"]["mac_dinh"] == T_BR and ts["H0"]["mac_dinh"] == H0
    assert all(h - d == PHONG for _, h, d in ROWS) and DROP0 == 414
_kiem_so()

DGREEN = (10, 110, 50); DRED = (185, 28, 28); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)
FS = 58                                            # chu phu nho nhat khi ve (x0,88 = 51 px trong mp4)

# ---------------- dung cu: nguon + ong dem Geiger + may dem + dong ho ----------------
RP = random.Random(3)
RAYS = [(RP.random(), RP.uniform(-1, 1)) for _ in range(28)]       # (pha, do lech) hat bay tu nguon vao cua so
BGR = [(RP.random(), RP.uniform(0, 2 * math.pi)) for _ in range(6)]  # hat phong nen tu moi phia

SX, SY = 300, 760          # tam nguon
TX0, TX1, TY = 430, 860, 760

def rig(d, t, minute, reading, src=1.0, clock_lbl=None, ff=False):
    # ban + gia do
    d.line([(110, 960), (990, 960)], fill=NAVY, width=6)
    d.rectangle([(TX0 + TX1) / 2 - 8, TY + 44, (TX0 + TX1) / 2 + 8, 956], fill=GRAY)
    d.rectangle([(TX0 + TX1) / 2 - 70, 940, (TX0 + TX1) / 2 + 70, 958], fill=NAVY)
    # ong dem Geiger (cua so o dau trai, quay ve phia nguon)
    d.rounded_rectangle([TX0, TY - 44, TX1, TY + 44], radius=40, fill=(214, 220, 232), outline=NAVY, width=5)
    d.rectangle([TX0 - 6, TY - 38, TX0 + 14, TY + 38], fill=(70, 78, 100))
    text(d, ((TX0 + TX1) / 2 + 10, TY), "ống Geiger", FS, NAVY)
    # cap noi may dem
    d.line([(TX1, TY), (950, TY), (950, 562)], fill=GRAY, width=12, joint="curve")
    # nguon tren gia (truot vao khi dat nguon)
    sx = lerp(-120, SX, ease(src))
    if src > 0:
        d.rectangle([sx - 8, SY + 30, sx + 8, 956], fill=GRAY)
        d.rectangle([sx - 60, 940, sx + 60, 958], fill=NAVY)
        d.rounded_rectangle([sx - 34, SY - 34, sx + 34, SY + 34], radius=12, fill=YELLOW, outline=NAVY, width=5)
        for k in range(3):
            a = math.radians(90 + 120 * k)
            d.pieslice([sx - 24, SY - 24, sx + 24, SY + 24], math.degrees(a) - 30, math.degrees(a) + 30, fill=NAVY)
        dot(d, sx, SY, 6, YELLOW)
        text(d, (sx - 50, SY), "nguồn", FS, INK, anchor="rm")
    # hat phong xa: mat do theo nhip dem mo hinh
    if src >= 1:
        n = int(len(RAYS) * clamp(model(minute) / model(0) + 0.04))
        for ph, dy in RAYS[:n]:
            q = (ph + t * 1.6) % 1
            x = lerp(SX + 40, TX0, q); y = SY + dy * 32 * q
            dot(d, x, y, 7, ORANGE)
    for ph, ang in BGR[:2]:                       # phong nen: vai hat le tu ngoai vao
        q = (ph + t * 0.7) % 1
        if q > 0.5: continue
        r = lerp(240, 50, q / 0.5)
        dot(d, 645 + r * math.cos(ang), TY + 0.7 * r * math.sin(ang), 7, PURPLE)
    # dong ho
    card(d, (70, 270, 520, 560), fill=WHITE, outline=LIGHT, r=28, w=4)
    text(d, (295, 390 if ff else 415), clock_lbl or f"phút {minute:.0f}", 68, BLUE)
    if ff:                                        # dau tua nhanh (khong chu)
        for j in range(2): d.polygon([(250 + j * 40, 466), (250 + j * 40, 522), (286 + j * 40, 494)], fill=DORANGE)
    # may dem
    card(d, (580, 270, 1010, 560), fill=WHITE, outline=LIGHT, r=28, w=4)
    d.rounded_rectangle([620, 300, 970, 420], radius=16, fill=NAVY)
    text(d, (795, 360), str(reading), 70, (134, 239, 172))
    text(d, (795, 495), "xung/phút", FS, INK)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem 5 o cao 70 px, tat lan luot tu PHAI sang TRAI; o da tat: nen trang, vien dam."""
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    rig(d, t, 0, "···")
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1000 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 580), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 20, W / 2 + pw / 2, y0 + 96), fill=A(PURPLE, k), r=36)
    text(d, (W / 2, y0 + 58), "DỰ ĐOÁN", 56, WHITE, alpha=k)
    text(d, (W / 2, y0 + 148), "Số đếm đã trừ phông", 60, INK, alpha=k)
    xs = [380, 610, 840]
    text(d, (110, y0 + 235), "phút", FS, BLUE, anchor="lm", alpha=k)
    for x, s in zip(xs, ("0", "5", "10")): text(d, (x, y0 + 235), s, 62, BLUE, alpha=k)
    d.line([(100, y0 + 280), (980, y0 + 280)], fill=A(LIGHT, k), width=4)
    for x, s in zip(xs, (str(ROWS[0][2]), str(ROWS[1][2]), "?")): text(d, (x, y0 + 330), s, 68, INK, alpha=k)
    text(d, (W / 2, y0 + 425), "Còn khoảng bao nhiêu?", 62, PURPLE, alpha=k)
    seg_bar(d, y0 + 480, t, M[1] + 0.3, sc["T"] - 0.25, PURPLE, k)

# ---------------- canh 2: do phong, dem moi 5 phut, ghi bang ----------------
def row_at(i, sc): return sc["M"][1] + 0.9 + 1.15 * i

def do_state(t, sc):
    """(phut tren dong ho, so tren may dem, nhan dong ho, dang tua nhanh)"""
    M = sc["M"]
    if t < M[1]: return 0, PHONG, "– –", False
    if t < row_at(0, sc): return 0, "···", None, False
    for i in range(4):
        a, b = row_at(i, sc), row_at(i + 1, sc)
        if t < b:
            k = clamp((t - a - 0.15) / (b - a - 0.45))
            if k <= 0: return ROWS[i][0], ROWS[i][1], None, False
            if k >= 1: return ROWS[i + 1][0], "···", None, False
            return ROWS[i][0] + 5 * k, "···", None, True
    return ROWS[4][0], ROWS[4][1], None, False

XS = [200, 520, 830]
def s_do(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    m, rd, lbl, ff = do_state(t, sc)
    rig(d, t, m, rd, src=clamp((t - M[1]) / 0.6), clock_lbl=lbl, ff=ff)
    a0 = 1.0
    if a0 > 0:
        card(d, (300, 588, 780, 650), fill=A((237, 233, 254), a0), r=30)
        text(d, (W / 2, 619), f"Phông nền: {PHONG}", FS, PURPLE, alpha=a0)
    card(d, (60, 995, 1020, 1590), fill=WHITE, outline=NAVY, w=4)
    for x, c, col in zip(XS, ["phút", "đo được", "trừ phông"], [BLUE, INK, DGREEN]): text(d, (x, 1050), c, FS, col)
    d.line([(90, 1092), (990, 1092)], fill=LIGHT, width=4)
    last = max([i for i in range(5) if t >= row_at(i, sc)], default=-1)
    for i, (tm, hd, hs) in enumerate(ROWS):
        a = appear(t, row_at(i, sc), 0.35); y = 1146 + i * 88
        if a <= 0: continue
        if i == last: d.rounded_rectangle([80, y - 38, 1000, y + 38], radius=14, fill=A((225, 236, 255), a))
        text(d, (XS[0], y), str(tm), 62, BLUE, alpha=a)
        text(d, (XS[1], y), str(hd), 62, INK, alpha=a)
        text(d, (XS[2], y), str(hs), 64, DGREEN, alpha=appear(t, row_at(i, sc) + 0.3, 0.35))

# ---------------- canh 3: dap an - do thi, duong "giam deu" vs diem that ----------------
GX0, GX1, GYB, GYT = 210, 950, 1110, 470
def GX(m): return GX0 + m / 20 * (GX1 - GX0)
def GY(h): return GYB - h / 850 * (GYB - GYT)
T_ZERO = ROWS[0][2] / DROP0 * 5                      # duong thang qua 2 diem dau cat truc: ~9,8 phut
def s_ans(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (60, 280, 1020, 1300), fill=WHITE, outline=LIGHT, w=3)
    for h in (400, 800): d.line([(GX0, GY(h)), (GX1, GY(h))], fill=(240, 236, 228), width=2)
    d.line([(GX0, GYB), (GX1 + 20, GYB)], fill=NAVY, width=5); d.line([(GX0, GYB), (GX0, GYT - 60)], fill=NAVY, width=5)
    text(d, (GX0 + 20, GYT - 110), "số đếm (trừ phông)", FS, INK, anchor="lm")
    text(d, (GX1 + 20, GYB + 110), "phút", FS, INK, anchor="rm")
    for m in range(0, 21, 5):
        d.line([(GX(m), GYB), (GX(m), GYB + 12)], fill=NAVY, width=3)
        text(d, (GX(m), GYB + 50), str(m), FS, INK)
    for h in (0, 400, 800):
        d.line([(GX0 - 12, GY(h)), (GX0, GY(h))], fill=NAVY, width=4); text(d, (GX0 - 20, GY(h)), str(h), FS, INK, anchor="rm")
    # 1) duong "giam deu": thang qua 2 diem dau, ve dan toi truc hoanh
    kl = ease((t - 0.6) / 1.4)
    if kl > 0:
        mend = T_ZERO * kl; n = int(mend / 0.4)
        for j in range(n + 1):
            m0, m1 = j * 0.4, min(j * 0.4 + 0.25, mend)
            if m1 > m0: d.line([(GX(m0), GY(ROWS[0][2] * (1 - m0 / T_ZERO))), (GX(m1), GY(ROWS[0][2] * (1 - m1 / T_ZERO)))], fill=RED, width=7)
    ag = appear(t, 2.3, 0.4)
    if ag > 0:
        text(d, (370, GYB - 45), "giảm đều?", 60, RED, alpha=ag)          # duoi duong thang, khong de diem phut 15
        dot(d, GX(T_ZERO), GYB, 14 * ag, RED, WHITE)
    # 2) diem that (2 diem dau co tu dau, 3 diem sau hien o phu de 2) + duong cong
    kc = ease((t - M[1] - 0.2) / 1.2)
    if kc > 0:
        pts = [(GX(20 * j / 100), GY(model(20 * j / 100))) for j in range(101)]
        d.line(pts[:max(2, int(len(pts) * kc))], fill=A(BLUE, 0.5), width=7, joint="curve")
    for i, (tm, _, hs) in enumerate(ROWS):
        a = 1.0 if i < 2 else appear(t, M[1] + 0.2 + (i - 2) * 0.35, 0.4)
        if a <= 0: continue
        dot(d, GX(tm), GY(hs), 17 * back(a), ORANGE, WHITE)
        if i < 3: text(d, (GX(tm) + 34, GY(hs) - 40), str(hs), 62 if i == 2 else FS, ORANGE if i == 2 else INK, anchor="lm", alpha=a)
    kt = appear(t, M[1] + 1.6)
    if kt > 0:                                   # T: tu 812 xuong ~ mot nua mat 5 phut
        y_t = GYB + 130
        d.line([(GX(0), y_t), (GX(5), y_t)], fill=A(DGREEN, kt), width=6)
        for x in (GX(0), GX(5)): d.line([(x, y_t - 16), (x, y_t + 16)], fill=A(DGREEN, kt), width=6)
        text(d, (GX(5) + 24, y_t), "T ≈ 5 phút", 60, DGREEN, anchor="lm", alpha=kt)

# ---------------- canh 4: co che + chua noi duoc gi ----------------
NC, NR = 10, 6
RN = random.Random(8)
_q = [(k + 0.5) / (NC * NR) for k in range(NC * NR)]; RN.shuffle(_q)
DEC = [-T_BR * math.log(u) / math.log(2) for u in _q]      # phut phan ra cua tung hat nhan (phan bo mu, T = 5)
STEPS = [0.6, 2.1, 3.6]                                    # dong ho mo phong: 0 -> 5 -> 10 -> 15 phut
def s_why(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    m = 5 * sum(clamp((t - a) / 0.8) for a in STEPS)
    card(d, (60, 280, 1020, 370), fill=WHITE, outline=LIGHT, r=24, w=3)
    FR = {0: "đủ", 5: "½", 10: "¼", 15: "⅛"}
    mm = 5 * round(m / 5)
    text(d, (W / 2 - 40, 325), f"phút {5 * math.ceil(m / 5 - 1e-6)}", 60, BLUE)
    if abs(m - mm) < 0.05 and mm: text(d, (W / 2 + 150, 325), FR[mm], 64, DORANGE)   # phan con lai (ve rieng)
    for i in range(NC * NR):
        cx = 150 + (i % NC) * 87; cy = 440 + (i // NC) * 88
        if DEC[i] <= m:
            dot(d, cx, cy, 22, LIGHT)
            fl = 1 - clamp((m - DEC[i]) / 2.5)
            if fl > 0:
                arrow(d, (cx + 18, cy - 18), (cx + 18 + 40 * (1 - fl) + 10, cy - 18 - 40 * (1 - fl) - 10), A(ORANGE, fl), w=5, head=12)
        else:
            dot(d, cx, cy, 22, ORANGE, NAVY)
    for j, (c, s) in enumerate([(ORANGE, "còn"), (LIGHT, "đã rã")]):
        dot(d, 250 + j * 380, 1000, 22, c, NAVY if c == ORANGE else EMPTY)
        text(d, (285 + j * 380, 1000), s, FS, INK, anchor="lm")
    b = appear(t, M[1] + 0.2)
    if b > 0:
        card(d, (60, 1080, 1020, 1400), fill=A(WHITE, b), outline=A(PURPLE, b), w=5)
        text(d, (W / 2, 1180), "Không đoán được", 64, PURPLE, alpha=b)
        text(d, (W / 2, 1290), "hạt nào rã trước.", 64, INK, alpha=b)

# ---------------- canh 5: bay "tru hai so lien nhau" ----------------
BX = [190 + 170 * i for i in range(5)]
def s_trap(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    # tren: cot so dem + doan do = phan giam trong moi 5 phut (khong in so: hinh tu noi "nho dan")
    a = appear(t, 0.2, 0.4)
    card(d, (60, 280, 1020, 900), fill=A(WHITE, a), outline=A(RED, a), w=5)
    text(d, (W / 2, 340), "Lấy trước − sau", 60, DRED, alpha=a)
    base, k = 860, 0.53
    for i, (tm, _, hs) in enumerate(ROWS):
        x = BX[i]
        d.rectangle([x - 42, base - hs * k, x + 42, base], fill=A((191, 219, 254), a), outline=A(BLUE, a), width=3)
    for i in range(4):
        g = ease((t - 0.7 - 0.55 * i) / 0.45)
        if g <= 0: continue
        x = BX[i] + 85; y1, y2 = base - ROWS[i][2] * k, base - ROWS[i + 1][2] * k
        d.line([(BX[i] + 42, y1), (x + 24, y1)], fill=RED, width=6)
        ye = lerp(y1, y2, g)                      # doan giam: khoi do day 30 px + dau tam giac rieng (thay ca doan ngan)
        d.rectangle([x - 15, y1, x + 15, ye], fill=RED)
        d.polygon([(x - 30, ye), (x + 30, ye), (x, ye + 30)], fill=RED)
    # duoi: chia hai so lien nhau -> gan bang 2
    b = appear(t, M[1] - 0.1, 0.4)
    if b <= 0: return
    card(d, (60, 950, 1020, 1560), fill=A(WHITE, b), outline=A(DGREEN, b), w=5)
    text(d, (W / 2, 1010), "Lấy trước : sau", 60, DGREEN, alpha=b)
    for i, r in enumerate(RATIOS):
        c = appear(t, M[1] + 0.2 + 0.35 * i, 0.35)
        x = (BX[i] + BX[i + 1]) / 2 + 0
        y = 1140 + (i % 2) * 110
        card(d, (x - 95, y - 46, x + 95, y + 46), fill=A((220, 252, 231), c), outline=A(DGREEN, c), r=22, w=3)
        text(d, (x, y), r, 62, DGREEN, alpha=c)
    ce = appear(t, M[1] + 1.9, 0.4)
    text(d, (W / 2, 1440), "≈ 2", 80, DGREEN, alpha=ce)

# ---------------- canh 6: chot (phu de) + THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 258, W / 2 + pw / 2, 334), fill=A(ORANGE, k1), r=36)
    text(d, (W / 2, 296), "THỬ NGHĨ", 56, WHITE, alpha=k1)
    text(d, (W / 2, 560), "Phút 0 → 5:", 66, INK, alpha=k1)
    text(d, (W / 2, 660), f"số đếm giảm {DROP0}", 66, INK, alpha=k1)
    k2 = appear(t, 2.3, 0.45)
    text(d, (W / 2, 860), "Phút 20 → 25:", 66, INK, alpha=k2)
    text(d, (W / 2, 960), "giảm khoảng bao nhiêu?", 66, DORANGE, alpha=k2)
    seg_bar(d, 1110, t, 2.5, sc["T"] - 0.2, ORANGE, k2)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, an, w, tr, e = (sc[k] for k in ("hook", "do", "ans", "why", "trap", "end"))
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding")]
    for i in range(4):                                   # tich tac khi dong ho tua nhanh 5 phut
        a, b = row_at(i, do) + 0.15, row_at(i + 1, do) - 0.3
        x = a
        while x < b: out.append((do["t0"] + x, "tick")); x += 0.25
    out += [(an["t0"] + an["M"][1] + 0.2, "ding"), (w["t0"] + w["M"][1] + 0.2, "tap"),
            (tr["t0"] + 0.2, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l12-phongxa-02", header="VẬT LÍ 12 · THÍ NGHIỆM", cues=_cues,
    footer="Chu kì bán rã · thachlab.id.vn", scenes=[
 dict(key="hook", title="Đếm xung theo thời gian", draw=s_hook, tail=0.3, caps=[
   ("Nguồn đặt trước ống Geiger.", 2.9),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Đo phông, rồi đếm mỗi 5 phút", draw=s_do, tail=0.3, caps=[
   ("Không nguồn: vẫn đếm được.", 2.9),
   ("Đặt nguồn, ghi số mỗi lần.", 3.4),
   ("Bớt 23 ở mỗi số đo.", 3.0)]),
 dict(key="ans", title="Phút 10 thật ra ra sao?", draw=s_ans, tail=0.3, caps=[
   ("Giảm đều: phút 10 về 0.", 3.4),
   ("Thật ra: 5 phút còn một nửa.", 3.8)]),
 dict(key="why", title="Vì sao còn một nửa?", draw=s_why, tail=0.4, caps=[
   ("Mỗi hạt: cùng một xác suất rã.", 3.8),
   ("Còn ít hạt, số đếm ít đi.", 3.8)]),
 dict(key="trap", title="Bẫy: trừ hai số liền nhau", draw=s_trap, tail=0.3, caps=[
   ("Giảm đều? Hiệu phải bằng nhau.", 3.4),
   ("Tỉ số mới gần như không đổi.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Cứ sau mỗi T, còn một nửa.", 5.4)]),
])
