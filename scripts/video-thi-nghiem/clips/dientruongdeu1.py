# Clip: tn-l11-dien-truong-deu-01 - Hat bot trong dau giua hai la dong song song (lo 11, 19/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dien-truong-deu-01.json (_kiem_so()):
#   so_lieu_mau (d cm, U kV, E V/m): 4 15 375000 | 2 15 750000 | 4 30 750000. ghi_chu: "Tinh tu E = U/d; hinh duong suc
#   khong doi dang, chi hat xep nhanh hon khi E lon." Hop exp nam o muc II.1, TRUOC muc E = U/d -> clip KHONG viet cong
#   thuc E = U/d, cot E ghi "tính sẵn".
# Du doan (K10, khong nut A-D): giu U, dua hai la tu 4 cm lai 2 cm -> dien truong vung giua the nao?
#   (manh len, van deu / yeu di, van deu / khong doi / manh len nhung het deu) -> dap an: manh len, van deu.
#   Khong trung cau Tu kiem tra ngay sau hop (M sat ban duong vs N chinh giua), khong trung Bay 3 (4 mm, 12 V).
# Hinh: nhin tu tren khay; la (+) ben trai, la (-) ben phai. Duong suc tinh so bang hai doan tich dien deu +/- (mo hinh 2D),
#   lan theo E tu la (+) sang la (-) -> assert: duong giua thang (lech doc < 3 px), duong sat mep cong ra (> 12 px),
#   chieu E tai tam huong tu (+) sang (-).
# Bay = hien_tuong_hay_sai[1] (o mep duong suc cung thang deu). KHONG dung [0] (gan ban duong manh hon) vi trung cau Tu kiem tra.
# Chua noi duoc = gia_thiet "hat bot chi dinh huong": hat cho thay huong, khong do duoc E.
# Thu nghi (cong B v1, 27/11): giu 15 kV, dua hai la con 1 cm -> E vung giua? Dap an 1 500 000 V/m (khong hien tren man).
#   Mot buoc clip chua chieu: lai halve d lan nua (2 -> 1 cm) -> E gap doi tu 750 000. Clip chi doi d nen KHONG hoi doi U.
from engine import *

ROWS = [(4, 15, 375000), (2, 15, 750000)]           # hai hang chieu trong clip
ROW3 = (4, 30, 750000)                               # hang 3 kho (khong chieu)
CHOT = (1, 15, 1500000)                              # dap an cau chot (ghi_chu kho), khong hien tren man
def num(n): return f"{n:,}".replace(",", " ")

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-dien-truong-deu-01.json")))
    hang = [tuple(r) for r in k["so_lieu_mau"]["hang"]]
    for r in ROWS + [ROW3]:
        assert r in hang, r
        assert abs(r[1] * 1000 / (r[0] / 100) - r[2]) < 1e-6         # E = U/d
    assert "nhanh hơn" in k["so_lieu_mau"]["ghi_chu"] and "1 500 000 V/m" in k["so_lieu_mau"]["ghi_chu"]
    assert abs(CHOT[1] * 1000 / (CHOT[0] / 100) - CHOT[2]) < 1e-6
_kiem_so()

# ---------------- truong: hai la dong la hai doan tich dien deu +sigma / -sigma (2D) ----------------
CX, CY, HALF, PXCM = 540, 615, 250, 60                # tam khay, nua chieu dai la (px), px/cm
TRAY = (150, 300, 930, 990)
def plates(dcm):
    return CX - dcm * PXCM / 2, CX + dcm * PXCM / 2  # x la (+), x la (-)

def efield(x, y, dcm):
    xp, xm = plates(dcm); ex = ey = 0.0; n = 120
    for i in range(n):
        yy = CY - HALF + (i + 0.5) * 2 * HALF / n
        for xs, q in ((xp, 1), (xm, -1)):
            dx, dy = x - xs, y - yy; r2 = dx * dx + dy * dy + 4.0
            ex += q * dx / r2; ey += q * dy / r2
    return ex, ey

def trace(x, y, dcm, step=4.0, nmax=900):
    xp, xm = plates(dcm); pts = [(x, y)]
    for _ in range(nmax):
        ex, ey = efield(x, y, dcm); m = math.hypot(ex, ey) or 1e-9
        x2, y2 = x + step * ex / m / 2, y + step * ey / m / 2       # RK2
        ex, ey = efield(x2, y2, dcm); m = math.hypot(ex, ey) or 1e-9
        x, y = x + step * ex / m, y + step * ey / m; pts.append((x, y))
        if abs(x - xm) < 5 and abs(y - CY) <= HALF + 2: break
        if not (TRAY[0] + 10 < x < TRAY[2] - 10 and TRAY[1] + 10 < y < TRAY[3] - 10): break
    return pts

LINES = {}
def field_lines(dcm):
    if dcm in LINES: return LINES[dcm]
    xp, _ = plates(dcm); out = []
    for k in range(-4, 5):                                       # 9 duong tu mat trong la (+)
        out.append(trace(xp + 4, CY + k * HALF / 4.4, dcm))
    for s in (1, -1):                                            # 2 duong tu dau la vong ra ngoai
        out.append(trace(xp + 2, CY + s * (HALF + 3), dcm))
    LINES[dcm] = out
    return out

def e_mid(dcm, U):
    """Giu U: mo hinh tich dien deu, chuan hoa sao cho tich phan E doc duong giua tu la (+) sang la (-) bang U."""
    xp, xm = plates(dcm); n = 200; h = (xm - xp) / n
    s = sum(efield(xp + (i + 0.5) * h, CY, dcm)[0] for i in range(n)) * h
    return efield(CX, CY, dcm)[0] * U / s

def _kiem_vat_li():
    for dcm in (4, 2):
        L = field_lines(dcm); xp, xm = plates(dcm); gap = xm - xp
        mid = L[4]; assert max(abs(p[1] - CY) for p in mid) < 1, "duong giua khong thang"
        for k in (3, 5):                                         # hai duong ke giua: gan thang (lech < 3% khoang cach)
            assert max(p[1] for p in L[k]) - min(p[1] for p in L[k]) < 0.03 * gap, (dcm, k)
        assert max(abs(p[1] - L[0][0][1]) for p in L[0]) > 12, (dcm, "duong mep phai cong")
        ex, ey = efield(CX, CY, dcm); assert ex > 0 and abs(ey) < 1e-6 * abs(ex)   # E tu (+) trai sang (-) phai
        assert abs(mid[-1][0] - xm) < 6                          # duong giua ket thuc o la (-)
        e1, e2 = efield(CX - gap / 4, CY, dcm)[0], efield(CX + gap / 4, CY, dcm)[0]
        assert abs(e1 / ex - 1) < 0.06 and abs(e2 / ex - 1) < 0.06, (dcm, e1 / ex)     # vung giua deu
    r = e_mid(2, 15) / e_mid(4, 15)
    assert 1.8 < r < 2.2, r                                      # giu U, d giam mot nua -> E vung giua ~ gap doi
_kiem_vat_li()

# ---------------- hat bot: moi hat gan voi mot diem tren duong suc ----------------
import random
def grains(dcm, n=520, seed=5):
    R = random.Random(seed); L = field_lines(dcm); out = []
    lens = [len(l) for l in L]; tot = sum(lens)
    for _ in range(n):
        r = R.random() * tot; i = 0
        while r >= lens[i]: r -= lens[i]; i += 1
        j = int(r); l = L[i]; j = max(1, min(len(l) - 2, j))
        x, y = l[j]; tx, ty = l[j + 1][0] - l[j - 1][0], l[j + 1][1] - l[j - 1][1]
        ang = math.atan2(ty, tx)
        out.append((x, y, ang, R.uniform(-60, 60), R.uniform(-45, 45), R.uniform(0, math.pi)))
    return out
GR = {}
def grain_set(dcm):
    if dcm not in GR: GR[dcm] = grains(dcm)
    return GR[dcm]

OIL = (254, 243, 199); OIL_E = (217, 180, 90); GRAIN = (146, 64, 14); COPPER = (194, 120, 62); FL = (234, 88, 12)
DGREEN = (10, 80, 40); DRED = (185, 28, 28)

def tray(d, dcm, k, show_lines=0.0, arrows=0.0, d_lbl=True, edge_hl=0.0, mid_hl=0.0):
    x0, y0, x1, y1 = TRAY
    d.rounded_rectangle(TRAY, radius=40, fill=OIL, outline=OIL_E, width=6)
    xp, xm = plates(dcm)
    if mid_hl > 0:
        d.rectangle([xp + 10, CY - HALF * 0.75, xm - 10, CY + HALF * 0.75], fill=A(PURPLE, 0.22 * mid_hl))
    if show_lines > 0:
        for l in field_lines(dcm): d.line(l, fill=A(FL, 0.55 * show_lines), width=3)
    for (x, y, ang, ox, oy, a0) in grain_set(dcm):
        e = ease(k); gx, gy = x + ox * (1 - e), y + oy * (1 - e)
        da = ((ang - a0 + math.pi / 2) % math.pi) - math.pi / 2       # huong hat: mod pi
        th = a0 + da * e
        dx, dy = 9 * math.cos(th), 9 * math.sin(th)
        near = (abs(gx - xp) < 12 or abs(gx - xm) < 12) and abs(gy - CY) < HALF + 12
        if TRAY[0] + 14 < gx < TRAY[2] - 14 and TRAY[1] + 14 < gy < TRAY[3] - 14 and not near:
            d.line([(gx - dx, gy - dy), (gx + dx, gy + dy)], fill=GRAIN, width=4)
    for x, sg, col in ((xp, "+", BLUE), (xm, "−", DRED)):
        d.rectangle([x - 8, CY - HALF, x + 8, CY + HALF], fill=COPPER, outline=(120, 70, 30), width=2)
        for j in (-2, 0, 2):
            text(d, (x + (-40 if sg == "+" else 40), CY + j * 80), sg, 58, col)
    if arrows > 0:
        for j in (-1, 1):
            yy = CY + j * 28                                          # giua duong giua va duong ke (cach 57 px)
            arrow(d, (xp + 30, yy), (xm - 30, yy), A(PURPLE, arrows), w=6, head=20)
        card(d, (CX - 30, CY - 115, CX + 30, CY - 55), fill=A(OIL, arrows), r=12)   # nam giua hai duong suc -57 / -114 px
        text(d, (CX, CY - 85), "E", 56, PURPLE, alpha=arrows)
    if edge_hl > 0:
        for s in (1, -1):
            yy = CY + s * (HALF + 20)
            d.ellipse([CX - 250, yy - 75, CX + 250, yy + 75], outline=A(DGREEN, edge_hl), width=4)
    if d_lbl:                                   # ve sau vong elip: nhan "4 cm" nam tren, khong bi cat
        yy = CY + HALF + 30
        d.line([(xp, yy), (xm, yy)], fill=NAVY, width=3)
        for x in (xp, xm): d.line([(x, yy - 14), (x, yy + 14)], fill=NAVY, width=3)
        card(d, (CX - 110, yy + 8, CX + 110, yy + 74), fill=OIL, r=14)
        text(d, (CX, yy + 41), f"{dcm} cm", 56, INK)

def etable(d, y, n, hl=-1, ratio=0.0, fade=0.0):
    card(d, (40, y, 1040, y + 120 + 2 * 90), fill=WHITE, outline=NAVY, w=4)
    xs = (190, 420, 760)
    for x, h in zip(xs, ("d (cm)", "U (kV)", "E (V/m)")): text(d, (x, y + 55), h, 56, NAVY)
    d.line([(70, y + 100), (1010, y + 100)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 155 + i * 90; dc, U, E = ROWS[i]
        if i == hl or ratio > 0:
            d.rounded_rectangle([60, yy - 40, 1020, yy + 40], radius=16, fill=A((255, 237, 213), 1.0 if i == hl else ratio * (1 - fade)))
        text(d, (xs[0], yy), str(dc), 58, INK); text(d, (xs[1], yy), str(U), 58, INK); text(d, (xs[2], yy), num(E), 58, BLUE)
    if ratio > 0:
        yy = y + 200
        text(d, (xs[0] - 80, yy), "÷2", 58, ORANGE, alpha=ratio); text(d, (xs[2] + 205, yy), "×2", 58, ORANGE, alpha=ratio)

def pill(d, s, y, a, color=NAVY, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A((148, 140, 128), a), r=18, w=4)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong nut) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    tray(d, 4, clamp((t - 0.6) / 2.0))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1060 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 520), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    for j, s in enumerate(("Giữ U = 15 kV,", "hai lá còn 2 cm.", "Điện trường vùng giữa?")):
        text(d, (W / 2, y0 + 170 + j * 82), s, 60, PURPLE if j == 2 else INK, alpha=a)
    seg_bar(d, y0 + 410, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
S1, S2, MOVE = 0.5, 4.6, 0.8          # quay may o 4 cm ; khuay lai + dua la ve 2 cm ; thoi gian dua la
TAU = {4: 2.0, 2: 1.0}                # E gap doi -> hat xep nhanh gap doi (ghi_chu kho: chi xep nhanh hon)
def do_state(t):
    """-> (d dang ve, muc xep hang 0..1, so hang bang)."""
    if t < S2:
        k = clamp((t - S1) / TAU[4]); return 4, k, (1 if k >= 1 else 0)
    if t < S2 + MOVE: return 2, 0.0, 1
    k = clamp((t - S2 - MOVE) / TAU[2]); return 2, k, (2 if k >= 1 else 1)

def s_do(img, d, t, sc):
    dc, k, rows = do_state(t)
    if t >= S2 and t < S2 + MOVE:                                  # dua la lai gan: ve la o vi tri trung gian
        dm = lerp(4, 2, ease((t - S2) / MOVE)); tray_move(d, dm)
    else:
        tray(d, dc, k)
    etable(d, 1060, rows, hl=rows - 1)

def tray_move(d, dm):
    d.rounded_rectangle(TRAY, radius=40, fill=OIL, outline=OIL_E, width=6)
    R = random.Random(9)
    for _ in range(420):
        x, y = R.uniform(TRAY[0] + 20, TRAY[2] - 20), R.uniform(TRAY[1] + 20, TRAY[3] - 20); a = R.uniform(0, math.pi)
        d.line([(x - 9 * math.cos(a), y - 9 * math.sin(a)), (x + 9 * math.cos(a), y + 9 * math.sin(a))], fill=GRAIN, width=4)
    xp, xm = CX - dm * PXCM / 2, CX + dm * PXCM / 2
    for x in (xp, xm): d.rectangle([x - 8, CY - HALF, x + 8, CY + HALF], fill=COPPER, outline=(120, 70, 30), width=2)

def _kiem_dong_bo():
    """Moi 0,05 s: hang bang chi hien khi hat da xep xong o dung khoang cach cua hang do."""
    bad = []; t = 0.0
    while t < 9.5:
        dc, k, rows = do_state(t)
        if rows >= 1 and t < S2 and (dc != 4 or k < 1): bad.append((round(t, 2), "hang 1 som"))
        if rows == 2 and (dc != 2 or k < 1): bad.append((round(t, 2), "hang 2 som"))
        t += 0.05
    if do_state(9.0)[2] != 2: bad.append("chua du 2 hang")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    kl = appear(t, M[1] - 0.1, 0.6)
    tray(d, 2, 1.0, show_lines=kl, arrows=appear(t, M[1] + 0.8, 0.5), mid_hl=kl)
    pill(d, "ĐÁP ÁN: Mạnh lên, vẫn đều", 1045, 1.0)
    etable(d, 1120, 2, ratio=appear(t, 2.6, 0.4), fade=appear(t, M[1] + 2.6, 0.5))

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = 1.0 - k3
    tray(d, 4, 1.0, show_lines=1.0, edge_hl=a1 * appear(t, 3.0, 0.4))
    y = 1040
    if a1 > 0:
        card(d, (40, y, 1040, y + 400), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y + 65, a1, DRED)
        ks = clamp((t - 0.3) / 0.4)
        q = "“Ở mép, đường cũng thẳng đều”"; f = F(58); lw = tw(d, q, f); yy = y + 190
        text(d, (W / 2, yy), q, 58, DRED, alpha=a1)
        if ks > 0:                              # gach cheo manh, chu van doc ro
            x0 = W / 2 - lw / 2 - 6; d.line([(x0, yy + 30), (x0 + (lw + 12) * ks, yy + 30 - 64 * ks)], fill=A(DRED, 0.8 * a1), width=4)
        text(d, (W / 2, y + 310), "✓ Gần mép: đường cong ra", 58, DGREEN, alpha=a1 * appear(t, 3.0, 0.4))
    if k3 > 0:
        card(d, (40, y, 1040, y + 400), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, "CHƯA NÓI ĐƯỢC", y + 65, k3, NAVY)
        text(d, (W / 2, y + 190), "Hạt chỉ cho thấy hướng,", 58, INK, alpha=k3)
        text(d, (W / 2, y + 300), "chưa đo được E.", 58, INK, alpha=k3)

# ---------------- canh 5: THU NGHI (cau chot o khung: 1 cm, 15 kV -> 1 500 000 V/m, khong hien) ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k = appear(t, 0.15, 0.4)
    tray(d, 2, 1.0, d_lbl=False)
    card(d, (40, 1020, 1040, 1580), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, "THỬ NGHĨ", 1085, k, ORANGE)
    text(d, (W / 2, 1190), "Giữ 15 kV, hai lá còn 1 cm.", 60, INK, alpha=k)
    text(d, (W / 2, 1280), "E vùng giữa bao nhiêu?", 62, (176, 64, 8), alpha=k)
    seg_bar(d, 1360, t, 1.0, sc["T"] - 0.2, ORANGE, k)
    kh = appear(t, M[0] + 3.0, 0.5)
    if kh > 0:
        card(d, (60, 1450, 1020, 1560), fill=A((255, 237, 213), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1505), "Gợi ý: 2 cm, 15 kV được bao nhiêu?", 56, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + S1, "tap"), (do["t0"] + S2 + MOVE, "tap")]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 1.6, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-dien-truong-deu-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Điện trường đều · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hạt bột trong dầu", draw=s_hook, tail=0.3, caps=[
   ("Hai lá đồng cách 4 cm, quay máy.", 3.6),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Khuấy bột, quay máy ở 4 cm.", 4.2),
   ("Đưa hai lá còn 2 cm.", 4.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Hai lá gần hơn, E tính sẵn gấp đôi.", 4.0),
   ("Đường sức vẫn thẳng, song song.", 4.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy thường gặp.", 5.8),
   ("Hạt bột cho biết gì?", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng lại, tự tính.", 7.4)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
