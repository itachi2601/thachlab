# Clip: tn-l11-dotocdoam-01 - Ong cong huong mot dau kin: tim hai lan am to nhat, tinh λ va v (lo 11, 19/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dotocdoam-01.json (_kiem_so() doi chieu ca mo_hinh):
#   f = 500 Hz ; ong dai 67 cm ; so_lieu_mau (lan, l1, l2, λ cm, v m/s): 1 16,8 50,8 68 340 | 2 16,7 50,9 68,4 342 |
#   3 16,8 50,9 68,2 341 | 4 16,6 50,8 68,4 342 | 5 16,7 51,0 68,6 343. mo_hinh l + e = (2k+1)λ/4, e = 0,5 cm.
# Clip KHONG dung ky hieu l1/l2 (l thuong de nham I): ghi "To lần 1/2" + so cm.
# Du doan (K10, khong nut A-D): lan to thu nhat cot khi 16,8 cm; ha tiep, lan to thu hai o dau? (gap doi / gap ba /
#   gap bon / khong con) -> dap an gap ba (50,8 ≈ 3·16,8). Ca goi y cua brief ("cach nhau bao nhieu so voi λ") TRUNG cau
#   Tu kiem tra Bay 2 (λ, λ/2, λ/4 o 1000 Hz) -> doi. Khong trung so 17/34/69/8,6 cua cau sau muc 3.
#   Luu y: dong "Quan sat" cua hop exp trong bai neu san "cỡ 17 cm và 51 cm" (truoc video) -> lo dap an, bao phien chinh.
# Bay = hien_tuong_hay_sai[3] (doc vach o mep binh). Khong dung [0] 4·l1 (= cau Bay 1), [1] λ vs λ/2 (= cau Bay 2),
#   [2] doi f (= cau Bay 3).
# Chua noi duoc: 5 lan lech vai m/s -> v dung toi dau? (muc 5 cua bai tinh Δv; clip KHONG tinh Δv, khong noi 339,6-343,6).
# Thu nghi: neu ong du dai, lan to thu ba o khoang bao nhieu cm? -> 50,8 + 34,0 = 84,8 cm (> 67 cm nen ong nay chi co 2
#   lan to). So 84,8 KHONG hien tren man, ghi trong ghi_chu kho.
from engine import *

F0, LONG = 500, 67
ROWS = [(1, 16.8, 50.8, 68.0, 340), (2, 16.7, 50.9, 68.4, 342), (3, 16.8, 50.9, 68.2, 341), (4, 16.6, 50.8, 68.4, 342),
        (5, 16.7, 51.0, 68.6, 343)]
L1, L2 = ROWS[0][1], ROWS[0][2]
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-dotocdoam-01.json")))
    hang = [tuple(r) for r in k["so_lieu_mau"]["hang"]]
    tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert tp["f"]["mac_dinh"] == F0 and tp["L"]["gia_tri"] == LONG
    for r in ROWS:
        assert any(all(abs(a - b) < 1e-9 for a, b in zip(r, h)) for h in hang), r
        assert abs(2 * (r[2] - r[1]) - r[3]) < 1e-6                      # λ = 2(l2 - l1)
        assert abs(r[3] / 100 * F0 - r[4]) < 0.6                         # v = λf
    lam, e = 343 / F0 * 100, 0.5                                         # mo hinh sinh so lieu
    assert abs(lam / 4 - e - L1) < 0.3 and abs(3 * lam / 4 - e - L2) < 0.3
    assert 5 * lam / 4 - e > LONG                                        # lan to thu ba ngoai ong 67 cm
    assert abs(L2 + (L2 - L1) - 84.8) < 1e-9 and "84,8" in k["so_lieu_mau"]["ghi_chu"]
    assert abs(L2 / L1 - 3) < 0.05                                       # dap an du doan: gap ba
_kiem_so()

# ---------------- hinh: ong dung, mieng o tren, thuoc ben trai, do thi "do to" thang hang ben phai ----------------
TX, TW, YM, PX = 250, 56, 400, 8.4                   # tam ong x, be rong long ong, mieng ong y, px/cm
WATER = (147, 197, 253); WATER_D = (37, 99, 235); GLASS = (226, 232, 240); WALL = (70, 80, 105)
CURVE = (234, 88, 12); ENV = (124, 58, 237); DGREEN = (10, 80, 40); DRED = (185, 28, 28)
GX0, GX1 = 600, 960                                  # vung do thi do to
def yl(lcm): return YM + lcm * PX

def loud(lcm, peaks=(L1, L2)):
    """Do to (0..1) khi cot khi dai lcm: chi cuc dai o hai vi tri cong huong da do."""
    return 0.07 + 0.93 * max(math.exp(-((lcm - p) / 1.3) ** 2) for p in peaks)

def _kiem_vat_li():
    xs = [i / 10 for i in range(0, 640)]
    pk = [x for i, x in enumerate(xs[1:-1], 1) if loud(x) > loud(xs[i - 1]) and loud(x) >= loud(xs[i + 1]) and loud(x) > 0.5]
    assert len(pk) == 2 and abs(pk[0] - L1) < 0.11 and abs(pk[1] - L2) < 0.11, pk
_kiem_vat_li()

def speaker(d, a=1.0):
    x, y = TX, YM - 70
    d.rectangle([x - 22, y - 34, x + 22, y - 6], fill=A(NAVY, a))
    d.polygon([(x - 22, y - 6), (x + 22, y - 6), (x + 44, y + 22), (x - 44, y + 22)], fill=A((90, 98, 120), a))
    text(d, (x + 70, y - 40), "loa 500 Hz", 40, INK, anchor="lm", alpha=a)

def rig(d, lcm, trace_to=None, marks=(), sound=0.0, t=0.0, bottle=True, env=None):
    top, bot = YM, yl(LONG)
    # thuoc: 0 o mieng ong
    for c in range(0, LONG + 1, 5):
        y = yl(c); L = 26 if c % 10 == 0 else 14
        d.line([(TX - TW / 2 - 8 - L, y), (TX - TW / 2 - 8, y)], fill=NAVY, width=3)
        if c % 10 == 0: text(d, (TX - TW / 2 - 44, y), str(c), 38, INK, anchor="rm")
    text(d, (TX - TW / 2 - 44, bot + 44), "cm", 38, MUTED, anchor="rm")
    # ong + nuoc
    d.rectangle([TX - TW / 2, top, TX + TW / 2, bot], fill=GLASS)
    d.rectangle([TX - TW / 2, yl(lcm), TX + TW / 2, bot], fill=WATER)
    d.line([(TX - TW / 2, yl(lcm)), (TX + TW / 2, yl(lcm))], fill=WATER_D, width=4)
    d.line([(TX - TW / 2, top), (TX - TW / 2, bot)], fill=WALL, width=6); d.line([(TX + TW / 2, top), (TX + TW / 2, bot)], fill=WALL, width=6)
    d.line([(TX - TW / 2, bot), (TX + TW / 2, bot)], fill=WALL, width=6)
    if env is not None:                                                    # bao bien do song dung (nut o mat nuoc)
        lam = 2 * (L2 - L1); sw = 0.6 + 0.4 * math.cos(2 * math.pi * 1.3 * t)
        for s in (1, -1):
            pts = [(TX + s * sw * (TW / 2 - 6) * abs(math.sin(2 * math.pi * (lcm - c / 10) / lam)), yl(c / 10))
                   for c in range(0, int(lcm * 10) + 1, 4)]
            d.line(pts, fill=A(ENV, env), width=4)
    if bottle:                                                             # binh nuoc noi ong mem, cung muc nuoc
        bx0, bx1 = 390, 480; y = yl(lcm)
        d.line([(TX, bot + 3), (TX, bot + 26), (435, bot + 26), (435, y + 90)], fill=(110, 118, 140), width=8)
        d.rectangle([bx0, y - 70, bx1, y + 90], fill=GLASS)
        d.rectangle([bx0, y, bx1, y + 90], fill=WATER); d.line([(bx0, y), (bx1, y)], fill=WATER_D, width=4)
        d.line([(bx0, y - 70), (bx0, y + 90), (bx1, y + 90), (bx1, y - 70)], fill=WALL, width=5)
        text(d, (bx1 + 12, y + 45), "bình", 38, MUTED, anchor="lm")
    speaker(d)
    if sound > 0:
        for k in range(3):
            r = 26 + ((t * 70 + k * 22) % 66)
            d.arc([TX - r, YM - 48 - r * 0.5, TX + r, YM - 48 + r * 0.5], 30, 150, fill=A(PURPLE, sound * (1 - (r - 26) / 66)), width=4)
    if trace_to is not None:                                               # do thi do to, truc doc thang hang voi thuoc
        d.line([(GX0, top), (GX0, bot)], fill=NAVY, width=3)
        text(d, (GX0 + 10, top - 40), "độ to →", 40, INK, anchor="lm")
        n = int(trace_to * 5)
        if n >= 1:
            pts = [(GX0 + (GX1 - GX0) * loud(c / 5), yl(c / 5)) for c in range(0, n + 1)]
            d.line(pts, fill=CURVE, width=5)
            dot(d, pts[-1][0], pts[-1][1], 9, CURVE)
        for p, lab in marks:
            d.line([(TX + TW / 2, yl(p)), (GX0 + (GX1 - GX0) * loud(p) + 12, yl(p))], fill=A(DGREEN, 0.55), width=3)
            card(d, (GX1 - 230, yl(p) + 14, GX1 + 50, yl(p) + 70), fill=(236, 253, 243), r=16)
            text(d, (GX1 - 90, yl(p) + 42), lab, 40, DGREEN)

# ---------------- canh 1: Du doan ----------------
def hook_l(t):
    return L1 * ease((t - 0.6) / 3.0)

def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    lc = hook_l(t); done = t >= 3.6
    rig(d, lc, trace_to=lc, marks=[(L1, vn(L1) + " cm")] if done else (), sound=1.0, t=t)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1030 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 540), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 56), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    for j, s in enumerate(("To lần 1: cột khí 16,8 cm.", "Hạ tiếp: to lần 2 ở đâu?")):
        text(d, (W / 2, y0 + 180 + j * 80), s, 48, INK, alpha=a)
    text(d, (W / 2, y0 + 410), "Chọn đáp án ở khung câu hỏi", 40, MUTED, alpha=a)
    tc, tend = M[1] + 0.5, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 480, 940, y0 + 494], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 480, 140 + 800 * (1 - p), y0 + 494], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
T_L2, T_END, T_ROWS = 4.0, 6.0, 6.4             # toi to lan 2 ; ha tiep toi day ; cac lan lap
LOW = 64.0
def do_state(t):
    """-> (muc nuoc cm, da thay to lan 2, so hang bang)."""
    if t < T_L2: lc = lerp(L1, L2, ease((t - 0.4) / (T_L2 - 0.4)))
    elif t < T_L2 + 0.6: lc = L2
    else: lc = lerp(L2, LOW, ease((t - T_L2 - 0.6) / (T_END - T_L2 - 0.6)))
    got2 = t >= T_L2 - 0.1
    rows = 0 if not got2 else 1
    if t >= T_ROWS: rows = min(5, 2 + int((t - T_ROWS) / 0.55))
    return lc, got2, rows

def dtable(d, y, n, vcol=0.0, hl=-1):
    card(d, (60, y, 1020, y + 100 + 5 * 66), fill=WHITE, outline=NAVY, w=4)
    xs = (150, 380, 610, 860)
    for x, h in zip(xs, ("Lần", "To lần 1", "To lần 2", "v (m/s)")):
        if h != "v (m/s)" or vcol > 0: text(d, (x, y + 50), h, 40, INK, alpha=1.0 if h != "v (m/s)" else vcol)
    d.line([(90, y + 88), (990, y + 88)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 124 + i * 66; r = ROWS[i]
        if i == hl: d.rounded_rectangle([80, yy - 30, 1000, yy + 30], radius=14, fill=(255, 237, 213))
        text(d, (xs[0], yy), str(r[0]), 42, INK)
        text(d, (xs[1], yy), vn(r[1]), 42, BLUE); text(d, (xs[2], yy), vn(r[2]), 42, BLUE)
        if vcol > 0: text(d, (xs[3], yy), str(r[4]), 42, DGREEN, alpha=vcol)

def s_do(img, d, t, sc):
    lc, got2, rows = do_state(t)
    card(d, (40, 260, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    mk = [(L1, vn(L1) + " cm")] + ([(L2, vn(L2) + " cm")] if got2 else [])
    rig(d, lc, trace_to=lc, marks=mk, sound=1.0, t=t)
    dtable(d, 1030, rows, hl=rows - 1 if rows <= 1 else -1)
    text(d, (W / 2, 1030 + 100 + 5 * 66 + 50), "số đo theo cm", 38, MUTED)

def _kiem_dong_bo():
    """Moi 0,05 s: nhan 50,8 cm chi hien khi muc nuoc da toi 50,8 ; hang 1 chi hien cung luc ; hang 2-5 sau khi ha xong."""
    bad = []; t = 0.0
    while t < 11.0:
        lc, got2, rows = do_state(t)
        if got2 and lc < L2 - 0.15: bad.append((round(t, 2), "nhan l2 truoc khi nuoc toi"))
        if not got2 and abs(lc - L2) < 0.05: bad.append((round(t, 2), "nuoc o l2 ma chua co nhan"))
        if rows >= 1 and not got2: bad.append((round(t, 2), "hang 1 som"))
        if rows >= 2 and t < T_ROWS: bad.append((round(t, 2), "hang lap som"))
        t += 0.05
    if do_state(10.4)[2] != 5: bad.append("chua du 5 hang")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def pill(d, s, y, a, color=NAVY, size=42):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A(color, a), r=34)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

PB = (L1 + L2) / 2                                                  # 33,8 cm: bung giua hai nut
assert abs(abs(math.sin(2 * math.pi * (L2 - PB) / (2 * (L2 - L1)))) - 1) < 1e-9   # bao bien cuc dai tai PB
def s_dapan(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    ke = appear(t, M[0] + 0.6, 0.5)
    rig(d, L2, marks=[], bottle=False, env=ke, t=t)
    if ke > 0:
        for p, s in ((L2, "nút"), (L1, "nút")):
            text(d, (TX + TW / 2 + 14, yl(p)), s, 42, ENV, anchor="lm", alpha=ke)
        text(d, (TX + TW / 2 + 14, YM + 18), "bụng", 42, ENV, anchor="lm", alpha=ke)
        text(d, (TX + TW / 2 + 14, yl(PB)), "bụng", 42, ENV, anchor="lm", alpha=ke)   # bung giua hai nut
    pill(d, "ĐÁP ÁN: gần gấp ba lần 1", 1060, appear(t, 0.15, 0.4))
    kq = appear(t, M[1] - 0.1, 0.5)
    lines = ("50,8 − 16,8 = 34,0 cm = λ/2", "λ = 68,0 cm", "v = λf = 340 m/s")
    for j, s in enumerate(lines):
        text(d, (W / 2, 1170 + j * 80), s, 48, (INK, ENV, DGREEN)[j], alpha=appear(t, M[1] + 0.2 + j * 1.0, 0.5))
    kr = appear(t, M[2] - 0.1, 0.5)
    if kr > 0:
        card(d, (60, 1410, 1020, 1530), fill=A((236, 253, 243), kr), outline=A(GREEN, kr), r=24, w=4)
        text(d, (W / 2, 1470), "5 lần đo: v từ 340 đến 343 m/s", 46, DGREEN, alpha=kr)

# ---------------- canh 4: Bay ; chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    rig(d, L2, bottle=True)
    yw = yl(L2); ks = clamp((t - 1.6) / 0.4); kg = appear(t, 2.4, 0.4)
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    # mat sai: ngang mep binh ; mat dung: ngang mat nuoc trong ong
    yb = yw - 70
    if a1 > 0:
        d.line([(500, yb), (TX + TW / 2, yb)], fill=A(DRED, a1), width=4)
        eye(d, 540, yb, DRED, a1); text(d, (590, yb), "✗ mép bình", 42, DRED, anchor="lm", alpha=a1)
    if kg > 0 and a1 > 0:
        for x in range(TX + int(TW / 2), 506, 24): d.line([(x, yw), (x + 12, yw)], fill=A(DGREEN, kg * a1), width=4)
        d.line([(TX - TW / 2, yw), (TX + TW / 2, yw)], fill=A(DGREEN, kg * a1), width=6)
        eye(d, 540, yw, DGREEN, kg * a1); text(d, (590, yw), "✓ mặt nước", 42, DGREEN, anchor="lm", alpha=kg * a1)
    y = 1030
    if a1 > 0:
        card(d, (40, y, 1040, y + 330), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 26, W / 2 + pw / 2, y + 90), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 58), "BẪY", 40, WHITE, alpha=a1)
        q = "Đọc vạch ở mép bình"; f = F(48); lw = tw(d, q, f); yy = y + 165
        text(d, (W / 2, yy), q, 48, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        text(d, (W / 2, y + 255), "✓ Mắt ngang mặt nước trong ống", 46, DGREEN, alpha=a1 * kg)
    if k3 > 0:
        card(d, (40, y, 1040, y + 300), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 75), "Chưa nói được", 48, NAVY, alpha=k3)
        kk = k3 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y + 200), "Năm lần lệch nhau: v đúng tới đâu?", 46, INK, alpha=kk)

def eye(d, x, y, col, a):
    d.ellipse([x - 26, y - 14, x + 26, y + 14], outline=A(col, a), width=4)
    dot(d, x - 6, y, 8, A(col, a))

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 540), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 410), "Hai lần to, đọc ở mặt nước", 50, DGREEN, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 600, 1040, 1290), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 630, W / 2 + pw / 2, 694), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 662), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    for j, s in enumerate(("Nếu ống đủ dài, lần to thứ ba", "ở cột khí khoảng bao nhiêu cm?")):
        text(d, (W / 2, 800 + j * 78), s, 48, INK, alpha=kq)
    kh = appear(t, M[0] + 3.2, 0.5)
    if kh > 0:
        card(d, (90, 1030, 990, 1260), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1080), "Gợi ý", 44, INK, alpha=kh)
        text(d, (W / 2, 1180), "Lần 1: 16,8 cm · lần 2: 50,8 cm", 44, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + 3.6, "tap"), (h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + T_L2, "tap"), (da["t0"] + 0.1, "ding"), (b["t0"] + 1.6, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-dotocdoam-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Đo tốc độ truyền âm · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Ống cộng hưởng 500 Hz", draw=s_hook, tail=0.3, caps=[
   ("Hạ nước dần, nghe âm to nhất.", 3.8),
   ("Tự trả lời trước khi xem.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Hạ tiếp tới lần to thứ hai.", 4.8),
   ("Làm lại đủ năm lần.", 4.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.8, caps=[
   ("Mặt nước luôn là nút.", 3.6),
   ("Lấy hiệu hai lần to.", 4.4),
   ("Làm lại, v gần như nhau.", 2.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy khi đọc thước.", 4.4),
   ("Câu còn bỏ ngỏ.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Tự trả lời trước gợi ý.", 7.4)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
