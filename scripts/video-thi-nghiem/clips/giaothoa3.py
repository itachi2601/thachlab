# Clip: tn-l11-giaothoa-03 - Khe Young voi laser: doi khoang cach toi man D (lo 11, 19/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-giaothoa-03.json (_kiem_so() doi chieu mo_hinh i = lam.D/a):
#   so_lieu_mau (lam um, a mm, D m, i mm): 0,65 0,2 2 -> 6,5 ; 0,65 0,2 3 -> 9,75. Hai hang a = 0,4 va lam = 0,45 KHONG chieu
#   (cau Thu PhET ngay sau hop hoi doi mau va doi a). Do 5 van sang lien tiep = 4 khoang: 26 mm / 39 mm ; bay chia 5 ra
#   5,2 mm ; THU NGHI a = 0,1 mm -> 13 mm: cac so nay ghi trong ghi_chu kho (them 19/11).
# Bai l11-giao-thoa-song (lesson 31): hop exp o muc II.4, sau cong thuc i = lam.D/a. Tranh trung: Cau 1 (tat mot nguon),
#   Cau 2, 3 (mat nuoc), Cau 4 (a = 1 mm, D = 2 m, 0,5 um, x = 2,5 mm: van toi) -> clip khong noi van toi o k + 1/2.
#   LUU Y: dong "Quan sat" cua hop exp da ghi "Dat man xa hon thi cac vach gian ra" = dap an Du doan (bao phien chinh).
# Du doan (K10): doi man tu 2 m ra 3 m, khoang van i se ra sao? Dap an: rong ra (6,5 -> 9,75 mm).
# Bay (them vao hien_tuong_hay_sai): dem 5 van sang roi chia 5 -> thuc ra 4 khoang van.
# Chua noi duoc: moi doi D, chua doi a va mau laser.
# Thu nghi: man van 2 m, laser cu; muon i = 13 mm thi tam khe a = ? (0,1 mm; can quan he i theo a chua chieu).
from engine import *

LAM, A0 = 0.65, 0.2
ROWS = [(2, 26, 6.5), (3, 39, 9.75)]                 # (D m, 4 khoang mm, i mm)

def vn(x, nd=None):
    s = f"{x:.{nd}f}" if nd is not None else f"{x:g}"
    return s.replace(".", ",")

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-giaothoa-03.json")))
    hang = k["so_lieu_mau"]["hang"]; g = k["so_lieu_mau"]["ghi_chu"]
    for D, s4, i in ROWS:
        assert any(r == [LAM, A0, D, i] for r in hang), (D, i)
        assert abs(LAM * D / A0 - i) < 1e-9 and abs(4 * i - s4) < 1e-9
        assert f"{s4} mm" in g
    assert "5,2 mm" in g and abs(26 / 5 - 5.2) < 1e-9
    assert "a = 0,1 mm" in g and abs(LAM * 2 / 0.1 - 13) < 1e-9 and "13 mm" in g
    assert any("chia 5" in s for s in k["hien_tuong_hay_sai"])
_kiem_so()

# ---------------- hinh ----------------
SX = 250; PD = 190                                     # x tam khe ; px / m cho D
def scr_x(D): return SX + D * PD
GX0, GX1, PMM = 90, 990, 15.0                          # dai van: 60 mm, 15 px/mm, van trung tam o x = 540
GC = (GX0 + GX1) / 2
DARK = (28, 12, 16); LRED = (255, 70, 50)

def inten(xmm, i):
    return math.cos(math.pi * xmm / i) ** 2 * math.exp(-(xmm / (5.5 * i)) ** 2)

def _kiem_van():
    for D, s4, i in ROWS:
        for k in range(-2, 3): assert abs(inten(k * i, i) - math.exp(-(k / 5.5) ** 2)) < 1e-9   # van sang o k.i
        assert inten(0.5 * i, i) < 1e-9                                                       # van toi o giua
        assert abs(4 * i * PMM / 2) <= (GX1 - GX0) / 2                                         # 5 van sang nam trong dai
        assert inten(2 * i, i) > 0.85                                                          # van thu 5 con du sang de dem
_kiem_van()

def fringes(d, y0, y1, i, a=1.0):
    for x in range(GX0, GX1 + 1, 2):
        c = mix(DARK, LRED, inten((x - GC) / PMM, i) * a + 0 * a)
        d.line([(x, y0), (x, y1)], fill=c, width=2)
    d.rectangle([GX0, y0, GX1, y1], outline=NAVY, width=3)

def mmruler(d, y):
    d.line([(GX0, y), (GX1, y)], fill=NAVY, width=3)
    for k in range(13):
        x = GX0 + k * 5 * PMM; L = 18 if k % 2 == 0 else 10
        d.line([(x, y), (x, y + L)], fill=NAVY, width=3)
        if k % 2 == 0 and k != 12: text(d, (x, y + 44), str(k * 5), 40, INK)
    text(d, (GX1, y + 44), "mm", 40, INK, anchor="rm")

def schematic(d, D, show_d=True):
    yc = 420; sx = scr_x(D)
    d.polygon([(SX + 6, yc - 6), (sx, 330), (sx, 510), (SX + 6, yc + 6)], fill=(255, 205, 195))
    d.line([(200, yc), (SX, yc)], fill=LRED, width=5)
    d.rounded_rectangle([70, yc - 28, 200, yc + 28], radius=10, fill=(70, 78, 100))
    d.rectangle([SX - 6, 330, SX + 6, yc - 14], fill=NAVY); d.rectangle([SX - 6, yc - 6, SX + 6, yc + 6], fill=NAVY)
    d.rectangle([SX - 6, yc + 14, SX + 6, 510], fill=NAVY)
    d.rectangle([sx, 320, sx + 14, 520], fill=(225, 225, 232), outline=NAVY, width=3)
    text(d, (135, yc + 70), "laser", 40, INK); text(d, (SX, 300), "hai khe, a = 0,2 mm", 40, INK)
    text(d, (sx + 7, 290), "màn", 40, INK)
    y = 560
    d.line([(SX, y), (sx, y)], fill=MUTED, width=3)
    for x in (SX, sx): d.line([(x, y - 14), (x, y + 14)], fill=MUTED, width=3)
    if show_d:
        s = f"D = {D:g} m"; pw = tw(d, s, F(42)) + 30
        card(d, ((SX + sx) / 2 - pw / 2, y - 26, (SX + sx) / 2 + pw / 2, y + 26), fill=WHITE, r=14)
        text(d, ((SX + sx) / 2, y), s, 42, INK)

def stage(d, D, i, show_d=True):
    card(d, (40, 260, 1040, 940), fill=WHITE, outline=LIGHT, w=3)
    schematic(d, D, show_d)
    fringes(d, 690, 790, i); mmruler(d, 800)

def brack(d, i, lab, a=1.0, y=670):
    xa, xb = GC - 2 * i * PMM, GC + 2 * i * PMM
    d.line([(xa, y), (xb, y)], fill=A(ORANGE, a), width=5)
    for x in (xa, xb): d.line([(x, y - 14), (x, y + 20)], fill=A(ORANGE, a), width=5)
    pw = tw(d, lab, F(42)) + 30
    card(d, (GC - pw / 2, y - 62, GC + pw / 2, y - 14), fill=A(WHITE, a), r=14)
    text(d, (GC, y - 38), lab, 42, (176, 64, 8), alpha=a)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    stage(d, 2, 6.5)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 980 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 580), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 56), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    for j, s in enumerate(("Dời màn từ 2 m ra 3 m.", "Khoảng vân i sẽ ra sao?")):
        text(d, (W / 2, y0 + 190 + j * 86), s, 50, INK, alpha=a)
    text(d, (W / 2, y0 + 450), "Chọn đáp án ở khung câu hỏi", 40, MUTED, alpha=a)
    tc, tend = M[1] + 0.5, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 520, 940, y0 + 534], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 520, 140 + 800 * (1 - p), y0 + 534], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
def tl(M):
    """Moc: (do lan 1, ghi hang 1, bat dau doi man, het doi man, do lan 2, ghi hang 2)."""
    m0 = M[1] + 0.1
    return 1.0, 2.0, m0, m0 + 1.6, m0 + 2.0, m0 + 2.8

def do_state(t, M):
    """-> (D dang ve, dang dich man?, chi so lan do dang hien (-1 neu khong), so hang)."""
    b1, r1, mv0, mv1, b2, r2 = tl(M)
    if t < mv0: D, moving = 2.0, False
    elif t < mv1: D, moving = 2.0 + ease((t - mv0) / (mv1 - mv0)), True
    else: D, moving = 3.0, False
    meas = 0 if b1 <= t < mv0 else (1 if t >= b2 else -1)
    rows = (1 if t >= r1 else 0) + (1 if t >= r2 else 0)
    return D, moving, meas, rows

def itable(d, y, n, hl=-1):
    card(d, (80, y, 1000, y + 96 + 2 * 74), fill=WHITE, outline=NAVY, w=4)
    for x, s in ((230, "D (m)"), (530, "4 khoảng (mm)"), (850, "i (mm)")): text(d, (x, y + 48), s, 42, INK)
    d.line([(110, y + 90), (970, y + 90)], fill=LIGHT, width=4)
    for j in range(n):
        yy = y + 128 + j * 74; D, s4, i = ROWS[j]
        if j == hl: d.rounded_rectangle([100, yy - 31, 980, yy + 31], radius=16, fill=(255, 237, 213))
        text(d, (230, yy), str(D), 44, INK); text(d, (530, yy), str(s4), 44, INK); text(d, (850, yy), vn(i), 44, BLUE)

def s_do(img, d, t, sc):
    M = sc["M"]; D, moving, meas, rows = do_state(t, M)
    i = LAM * D / A0
    stage(d, D, i, show_d=not moving)
    if meas >= 0:
        b = tl(M)[0] if meas == 0 else tl(M)[4]
        brack(d, ROWS[meas][2], f"5 vân sáng: {ROWS[meas][1]} mm", appear(t, b, 0.3))
    itable(d, 990, rows, hl=rows - 1)

def _kiem_dong_bo():
    """Moi 0,05 s: so D chi hien khi man dung yen ; khoang do khop D dang ve ; hang ghi sau khi do."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; M = sc["M"]; t = 0.0; bad = []
    b1, r1, mv0, mv1, b2, r2 = tl(M)
    while t < sc["T"]:
        D, moving, meas, rows = do_state(t, M)
        if not moving and D not in (2.0, 3.0): bad.append((round(t, 2), "D le khi dung yen"))
        if meas >= 0 and (moving or D != ROWS[meas][0]): bad.append((round(t, 2), "lan do lech D"))
        if rows >= 1 and t < b1 + 0.5: bad.append((round(t, 2), "hang 1 som"))
        if rows == 2 and (t < b2 + 0.5 or D != 3.0): bad.append((round(t, 2), "hang 2 som"))
        t += 0.05
    if do_state(sc["T"] - 0.05, M)[3] != 2: bad.append("chua du 2 hang cuoi canh")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def pill(d, s, y, a, color=NAVY, size=42):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A(color, a), r=34)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN: rộng ra", 310, appear(t, 0.15, 0.4))
    card(d, (40, 380, 1040, 900), fill=WHITE, outline=LIGHT, w=3)
    for j, (D, s4, i) in enumerate(ROWS):
        y = 470 + j * 230
        text(d, (GX0, y - 40), f"D = {D} m", 42, INK, anchor="lm")
        fringes(d, y, y + 90, i)
        xa, xb = GC, GC + i * PMM
        d.line([(xa, y + 120), (xb, y + 120)], fill=ORANGE, width=5)
        for x in (xa, xb): d.line([(x, y + 104), (x, y + 136)], fill=ORANGE, width=5)
        text(d, (xb + 16, y + 122), f"i = {vn(i)} mm", 42, (176, 64, 8), anchor="lm")
    k1 = appear(t, M[0] + 0.5, 0.45)
    if k1 > 0:
        card(d, (60, 950, 1020, 1090), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        text(d, (W / 2, 1020), "D gấp 1,5 → i gấp 1,5", 48, (21, 128, 61), alpha=k1)
    k2 = appear(t, M[1] - 0.05, 0.45)
    if k2 > 0:
        card(d, (60, 1130, 1020, 1270), fill=A(WHITE, k2), outline=A(NAVY, k2), w=5)
        text(d, (W / 2, 1200), "Vân sáng tối: dấu hiệu của sóng", 44, INK, alpha=k2)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; i = 6.5
    card(d, (40, 260, 1040, 940), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 330), "D = 2 m", 42, INK)
    fringes(d, 450, 570, i); mmruler(d, 580)
    for k in range(-2, 3):
        x = GC + k * i * PMM; text(d, (x, 410), str(k + 3), 42, NAVY)
    ka = appear(t, 2.2, 0.4)
    if ka > 0:
        for k in range(-2, 2):
            x0, x1 = GC + k * i * PMM, GC + (k + 1) * i * PMM
            d.arc([x0 + 6, 690, x1 - 6, 790], 180, 360, fill=A(ORANGE, ka), width=5)
        text(d, (W / 2, 830), "4 khoảng", 44, (176, 64, 8), alpha=ka)
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    y = 980
    if a1 > 0:
        card(d, (40, y, 1040, y + 400), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 26, W / 2 + pw / 2, y + 90), fill=A(RED, a1), r=32)
        text(d, (W / 2, y + 58), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - 1.4) / 0.4)
        q = "“5 vân: 26 : 5 = 5,2 mm”"
        f = F(48); lw = tw(d, q, f); yy = y + 175
        text(d, (W / 2, yy), q, 48, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
        text(d, (W / 2, y + 300), "✓ 26 : 4 = 6,5 mm", 48, (10, 80, 40), alpha=a1 * ka)
    if k3 > 0:
        card(d, (40, y, 1040, y + 300), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 75), "Chưa nói được", 48, NAVY, alpha=k3)
        kk = k3 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y + 170), "Mới đổi D.", 46, INK, alpha=kk)
        text(d, (W / 2, y + 240), "Đổi màu laser thì sao?", 46, INK, alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """THU NGHI: man van 2 m, laser cu ; muon i = 13 mm thi a = ? (0,1 mm)."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 370), "Màn càng xa,", 50, (21, 128, 61), alpha=k0)
    text(d, (W / 2, 450), "vân càng thưa", 50, (21, 128, 61), alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 1290), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    for j, s in enumerate(("Màn vẫn cách 2 m, laser cũ.", "Muốn i = 13 mm thì", "hai khe cách nhau bao nhiêu?")):
        text(d, (W / 2, 790 + j * 80), s, 48, INK, alpha=kq)
    kh = appear(t, M[0] + 3.2, 0.5)
    if kh > 0:
        card(d, (110, 1030, 970, 1260), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1080), "Gợi ý", 44, INK, alpha=kh)
        text(d, (W / 2, 1180), "a = 0,2 mm cho i = 6,5 mm", 46, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    T = tl(do["M"])
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + T[0], "tap"), (do["t0"] + T[4], "tap")]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 1.4, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-giaothoa-03", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Giao thoa sóng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Khe Young với laser", draw=s_hook, tail=0.3, caps=[
   ("Laser đỏ qua hai khe, chiếu lên màn.", 3.6),
   ("Tự trả lời trước khi xem.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.7, caps=[
   ("Đo nhiều vân, rồi chia ra i.", 3.8),
   ("Dời màn ra 3 m, đo lại.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Màn xa hơn, vân giãn đều ra.", 4.0),
   ("Giao thoa được: ánh sáng là sóng.", 4.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy thường gặp.", 4.8),
   ("Câu còn bỏ ngỏ.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Tự trả lời trước gợi ý.", 7.8)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
