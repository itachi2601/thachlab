# Clip: tn-l11-dotocdoam-01 - Ong cong huong mot dau kin: tim hai lan am to nhat, tinh λ va v (lo 11, 19/11/2026)
# Ban 2 (27/11/2026, cong moi lo L11b): chu ve >= 56 px, <= 180 tu/phut moi canh, nhip >= 2 s, K10 ("Dung lai, tu doan."),
#   dem 5 o, the CHUA NOI DUOC >= 4 s, nhip Bay >= 3 s, bo the goi y o man chot (goi y cu neu so = chi cach lam).
#   Hop exp trong bai (ban hien hanh) chi con "trong ong chi co hai cho nghe to nhat" - khong lo vi tri lan 2.
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dotocdoam-01.json (_kiem_so() doi chieu ca mo_hinh):
#   f = 500 Hz ; ong dai 67 cm ; so_lieu_mau (lan, l1, l2, λ cm, v m/s): 1 16,8 50,8 68 340 | 2 16,7 50,9 68,4 342 |
#   3 16,8 50,9 68,2 341 | 4 16,6 50,8 68,4 342 | 5 16,7 51,0 68,6 343. mo_hinh l + e = (2k+1)λ/4, e = 0,5 cm.
# Clip KHONG dung ky hieu l1/l2 (l thuong de nham I): ghi "To lần 1/2" + so cm.
# Du doan (K10, khong nut A-D): lan to thu nhat cot khi 16,8 cm; ha tiep, lan to thu hai o dau? (gap doi / gap ba /
#   gap bon / khong con) -> dap an gap ba (50,8 ≈ 3·16,8). Ca goi y cua brief ("cach nhau bao nhieu so voi λ") TRUNG cau
#   Tu kiem tra Bay 2 (λ, λ/2, λ/4 o 1000 Hz) -> doi. Khong trung so 17/34/69/8,6 cua cau sau muc 3.
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
TX, TW, YM, PX = 270, 60, 400, 8.4                   # tam ong x, be rong long ong, mieng ong y, px/cm
WATER = (147, 197, 253); WATER_D = (37, 99, 235); GLASS = (226, 232, 240); WALL = (70, 80, 105)
CURVE = (234, 88, 12); ENV = (124, 58, 237); DGREEN = (21, 110, 55); DRED = (185, 28, 28); DORANGE = (176, 64, 8)
HL = (255, 237, 213); FS = 58
GX0, GX1 = 620, 960                                  # vung do thi do to
def yl(lcm): return YM + lcm * PX

def loud(lcm, peaks=(L1, L2)):
    """Do to (0..1) khi cot khi dai lcm: chi cuc dai o hai vi tri cong huong da do."""
    return 0.07 + 0.93 * max(math.exp(-((lcm - p) / 1.3) ** 2) for p in peaks)

def _kiem_vat_li():
    xs = [i / 10 for i in range(0, 640)]
    pk = [x for i, x in enumerate(xs[1:-1], 1) if loud(x) > loud(xs[i - 1]) and loud(x) >= loud(xs[i + 1]) and loud(x) > 0.5]
    assert len(pk) == 2 and abs(pk[0] - L1) < 0.11 and abs(pk[1] - L2) < 0.11, pk
_kiem_vat_li()

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

def speaker(d, a=1.0):
    x, y = TX, YM - 70
    d.rectangle([x - 22, y - 34, x + 22, y - 6], fill=A(NAVY, a))
    d.polygon([(x - 22, y - 6), (x + 22, y - 6), (x + 44, y + 22), (x - 44, y + 22)], fill=A((90, 98, 120), a))
    text(d, (x + 70, y - 30), "loa 500 Hz", 56, INK, anchor="lm", alpha=a)

def rig(d, lcm, trace_to=None, marks=(), sound=0.0, t=0.0, bottle=True, env=None, pulse=None):
    top, bot = YM, yl(LONG)
    for c in range(0, LONG + 1, 5):                                         # thuoc: 0 o mieng ong
        y = yl(c); L = 26 if c % 10 == 0 else 14
        d.line([(TX - TW / 2 - 8 - L, y), (TX - TW / 2 - 8, y)], fill=NAVY, width=3)
        if c % 20 == 0: text(d, (TX - TW / 2 - 44, y), str(c), 56, INK, anchor="rm")
    text(d, (TX - TW / 2 - 44, bot + 50), "cm", 56, INK, anchor="rm")
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
        bx0, bx1 = 410, 500; y = yl(lcm)
        d.line([(TX, bot + 3), (TX, bot + 26), (455, bot + 26), (455, y + 90)], fill=(110, 118, 140), width=8)
        d.rectangle([bx0, y - 70, bx1, y + 90], fill=GLASS)
        d.rectangle([bx0, y, bx1, y + 90], fill=WATER); d.line([(bx0, y), (bx1, y)], fill=WATER_D, width=4)
        d.line([(bx0, y - 70), (bx0, y + 90), (bx1, y + 90), (bx1, y - 70)], fill=WALL, width=5)
    speaker(d)
    if sound > 0:
        for k in range(3):
            r = 30 + ((t * 80 + k * 26) % 78)
            d.arc([TX - r, YM - 48 - r * 0.5, TX + r, YM - 48 + r * 0.5], 30, 150, fill=A(PURPLE, sound * (1 - (r - 30) / 78)), width=5)
    if pulse is not None:                                                  # vong nhip o mat nuoc (lan to)
        rr = 40 + 22 * math.sin(3.2 * t)
        d.ellipse([TX - rr, yl(pulse) - rr * 0.6, TX + rr, yl(pulse) + rr * 0.6], outline=CURVE, width=5)
    if trace_to is not None:                                               # do thi do to, truc doc thang hang voi thuoc
        d.line([(GX0, top), (GX0, bot)], fill=NAVY, width=3)
        text(d, (GX0 + 10, top - 34), "độ to →", 56, INK, anchor="lm")
        n = int(trace_to * 5)
        if n >= 1:
            pts = [(GX0 + (GX1 - GX0) * loud(c / 5), yl(c / 5)) for c in range(0, n + 1)]
            d.line(pts, fill=CURVE, width=5)
            dot(d, pts[-1][0], pts[-1][1], 10, CURVE)
        for p, lab in marks:
            d.line([(TX + TW / 2, yl(p)), (GX0 + (GX1 - GX0) * loud(p) + 12, yl(p))], fill=A(DGREEN, 0.55), width=3)
            card(d, (GX1 - 250, yl(p) + 14, GX1 + 70, yl(p) + 90), fill=(236, 253, 243), r=16)
            text(d, (GX1 - 90, yl(p) + 52), lab, 56, DGREEN)

# ---------------- canh 1: Du doan ----------------
def hook_l(t):
    return L1 * ease((t - 0.4) / 2.0)

def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (40, 260, 1040, 1020), fill=WHITE, outline=LIGHT, w=3)
    lc = hook_l(t); done = t >= 2.4
    rig(d, lc, trace_to=lc, marks=[(L1, vn(L1) + " cm")] if done else (), sound=1.0, t=t, pulse=L1 if done else None)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1050 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 540), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 185), "To lần 1: cột khí 16,8 cm.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 285), "Hạ nước tiếp,", 64, PURPLE, alpha=a)
    text(d, (W / 2, y0 + 370), "to lần 2 ở đâu?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 440, t, M[1], sc["T"] - 0.2, PURPLE, a)

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

def dtable(d, y, n, hl=-1):
    card(d, (60, y, 1020, y + 96 + 5 * 76), fill=WHITE, outline=NAVY, w=4)
    xs = (170, 480, 820)
    for x, h in zip(xs, ("Lần", "To lần 1", "To lần 2")): text(d, (x, y + 48), h, 56, INK)
    d.line([(90, y + 88), (990, y + 88)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 132 + i * 76; r = ROWS[i]
        if i == hl: d.rounded_rectangle([80, yy - 34, 1000, yy + 34], radius=14, fill=HL)
        text(d, (xs[0], yy), str(r[0]), 56, INK)
        text(d, (xs[1], yy), vn(r[1]) + " cm", 56, BLUE); text(d, (xs[2], yy), vn(r[2]) + " cm", 56, BLUE)

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    lc, got2, rows = do_state(t)
    card(d, (40, 260, 1040, 1020), fill=WHITE, outline=LIGHT, w=3)
    mk = [(L1, vn(L1) + " cm")] + ([(L2, vn(L2) + " cm")] if got2 else [])
    rig(d, lc, trace_to=lc, marks=mk, sound=1.0, t=t, pulse=L2 if got2 else None)
    dtable(d, 1050, rows, hl=rows - 1 if rows <= 1 else -1)
    if t > T_END:                                       # cham chay doc duong do to: hai dinh 16,8 va 50,8
        c = ((t - T_END) * 22) % LOW
        dot(d, GX0 + (GX1 - GX0) * loud(c), yl(c), 20, CURVE, outline=WHITE)

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
    if do_state(9.0)[2] != 5: bad.append("chua du 5 hang")
    return bad

# ---------------- canh 3: Rut ra ----------------
PB = (L1 + L2) / 2                                                  # 33,8 cm: bung giua hai nut
assert abs(abs(math.sin(2 * math.pi * (L2 - PB) / (2 * (L2 - L1)))) - 1) < 1e-9   # bao bien cuc dai tai PB
def s_rut(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (40, 260, 1040, 1020), fill=WHITE, outline=LIGHT, w=3)
    ke = appear(t, 0.2, 0.5)
    rig(d, L2, marks=[], bottle=False, env=ke, t=t)
    for p, s in ((L2, "nút"), (L1, "nút"), (0, "bụng"), (PB, "bụng")):
        text(d, (TX + TW / 2 + 18, yl(p) + (22 if p == 0 else 0)), s, 56, ENV, anchor="lm", alpha=ke)
    kq = appear(t, M[1] - 0.1, 0.5)
    if kq > 0:
        card(d, (60, 1060, 1020, 1420), fill=A(WHITE, kq), outline=A(ENV, kq), w=5)
        for j, s in enumerate(("50,8 − 16,8 = 34,0 cm = λ/2", "λ = 68,0 cm", "v = λf = 340 m/s")):
            text(d, (W / 2, 1140 + j * 105), s, 58, (INK, ENV, DGREEN)[j], alpha=kq)

# ---------------- canh 4: Bay ; chua noi duoc ----------------
B2 = 3.4
def eye(d, x, y, col, a):
    d.ellipse([x - 30, y - 16, x + 30, y + 16], outline=A(col, a), width=5)
    dot(d, x - 6, y, 9, A(col, a))

def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    card(d, (40, 260, 1040, 1020), fill=WHITE, outline=LIGHT, w=3)
    rig(d, L2, bottle=True)
    yw = yl(L2); yb = yw - 70
    k3 = appear(t, M[2] - 0.2, 0.45); a1 = 1.0 - k3
    ks = clamp((t - B2) / 0.5); kg = appear(t, B2, 0.4)
    if a1 > 0:
        d.line([(500, yb), (TX + TW / 2, yb)], fill=A(DRED, a1), width=4)
        eye(d, 560, yb, DRED, a1); text(d, (610, yb), "mép bình", 56, DRED, anchor="lm", alpha=a1)
        if ks > 0:
            lw = tw(d, "mép bình", F(56))
            d.line([(606, yb + 4), (606 + (lw + 10) * ks, yb + 4)], fill=A(DRED, 0.85 * a1), width=5)
    if kg > 0 and a1 > 0:
        for x in range(TX + int(TW / 2), 526, 24): d.line([(x, yw), (x + 12, yw)], fill=A(DGREEN, kg * a1), width=4)
        d.line([(TX - TW / 2, yw), (TX + TW / 2, yw)], fill=A(DGREEN, kg * a1), width=6)
        eye(d, 560, yw + 4, DGREEN, kg * a1); text(d, (610, yw + 60), "mặt nước", 56, DGREEN, anchor="lm", alpha=kg * a1)
        rr = 38 + 20 * math.sin(3.2 * t)
        d.ellipse([TX - rr, yw - rr * 0.6, TX + rr, yw + rr * 0.6], outline=A(DGREEN, kg * a1), width=5)
    y = 1060
    if a1 > 0:
        card(d, (40, y, 1040, y + 360), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, W / 2, y + 70, "BẪY", DRED, a1)
        q = "Đọc vạch ở mép bình"; lw = tw(d, q, F(64)); yy = y + 200
        text(d, (W / 2, yy), q, 64, DRED, alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 4), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 4)], fill=A(DRED, 0.85 * a1), width=5)
    if k3 > 0:
        card(d, (40, y, 1040, y + 480), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, y + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, y + 200), "Năm lần lệch vài m/s:", 62, INK, alpha=k3)
        text(d, (W / 2, y + 300), "v đúng tới đâu?", 62, INK, alpha=k3)
        for j, v in enumerate((340, 342, 341, 342, 343)):          # 5 cham v nhay len xuong nhe
            x = 230 + j * 155; yy = y + 400 + 34 * math.sin(3.0 * t + j)
            dot(d, x, yy, 24, A(DGREEN, k3))

# ---------------- canh 5: THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1560), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 310, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 560), "Nếu ống đủ dài,", 64, INK, alpha=k)
    text(d, (W / 2, 650), "lần to thứ ba ở cột khí", 64, INK, alpha=k)
    text(d, (W / 2, 790), "khoảng bao nhiêu cm?", 66, DORANGE, alpha=k)
    seg_bar(d, 1000, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = (sc[x] for x in ("hook", "do", "rut", "bay", "end"))
    out = [(h["t0"] + 2.4, "tap"), (h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.7, "ding")]
    out += [(do["t0"] + T_L2, "tap"), (do["t0"] + do["M"][2], "ding"), (r["t0"] + r["M"][1], "tap")]
    out += [(b["t0"] + 0.3, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-dotocdoam-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Đo tốc độ truyền âm · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Ống cộng hưởng 500 Hz", draw=s_hook, tail=0.3, caps=[
   ("Hạ nước dần, nghe âm to nhất.", 3.8),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Hạ tiếp tới lần to thứ hai.", 4.2),
   ("Làm lại đủ năm lần.", 3.8),
   ("Đáp án: gần gấp ba lần 1.", 3.4)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.3, caps=[
   ("Mặt nước luôn là nút.", 3.4),
   ("Lấy hiệu hai lần to.", 4.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Mép bình không phải mặt nước.", 3.4),
   ("Mắt ngang mặt nước trong ống.", 3.4),
   ("Còn một chỗ chưa rõ.", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 6.5)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
