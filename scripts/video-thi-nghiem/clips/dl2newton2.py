# Clip: tn-l10-dl2-newton-02 - Gia toc cua xe theo khoi luong, luc keo khong doi (lo 7, 18/11/2026; dung lai 27/11/2026
# theo viec 4: cong --do-chu, chu >= 55 px khi ve, K10, Bay hinh tu giai thich, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-dl2-newton-02.json (_kiem_so() doi chieu):
#   tham_so F = 0,40 N, m 0,5-1,5 kg buoc 0,25 ; so_lieu_mau (m kg, a m/s2, m.a N): 0,50 0,80 0,40 | 0,75 0,53 0,40 |
#   1,00 0,40 0,40 | 1,50 0,27 0,41. Kho khong co cot t: xe chay voi t = can(2s/a), s = 0,50 m (bo thi nghiem 01) chi de
#   ve -> xe nang chay cham hon that; so tren man chi la a.
# Bo cuc KHAC dl2newton1: hinh chinh la BANG m | a (| m.a) + gia trong chat len xe; ket qua la do thi a theo m (duong cong).
# Du doan (K10): giu F = 0,40 N, m 0,50 -> 1,50 kg, do thi a theo m dang nao? -> duong cong di xuong, thoai dan.
#   Khong trung clip 01 (a theo F), quiz mo bai (40/80 kg), Cau 2 (m gap 3 -> a?): clip khong tu noi phep so 0,50/1,50.
# Gia trong roi tu tren xuong (khong xep cho tren san), lan cuoi 2 khoi roi CUNG luc: tren xe chi co 0, 1, 2, 4 khoi
#   -> dap so chot "3 khoi" khong thoang hien.
# Bay = hien_tuong_hay_sai[0] "cung luc thi moi vat cung gia toc": hai xe 0,50 kg / 1,00 kg cung keo 0,40 N chay dua
#   (hinh tu giai thich), a = 0,80 / 0,40 m/s2 hien khi moi xe toi cong 2.
# Chua noi duoc: mang co ma sat thi m.a con bang luc keo?
# Cau chot (ghi_chu kho): F 0,40 N, xe rong 0,50 kg, muon a = 0,32 m/s2 -> m = 1,25 kg, them 0,75 kg = 3 gia trong 0,25 kg.
from engine import *

ROWS = [(0.50, 0.80, 0.40), (0.75, 0.53, 0.40), (1.00, 0.40, 0.40), (1.50, 0.27, 0.41)]   # so_lieu_mau
F_N, S_M, M0, GT = 0.40, 0.50, 0.50, 0.25
NB = [0, 1, 2, 4]                                  # so gia trong tren xe
CHOT = (0.32, 1.25, 3)
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-dl2-newton-02.json")))
    hang = [tuple(r) for r in k["so_lieu_mau"]["hang"]]
    assert all(any(all(abs(a - b) < 1e-9 for a, b in zip(r, h)) for h in hang) for r in ROWS)
    assert all(abs(M0 + n * GT - r[0]) < 1e-9 for n, r in zip(NB, ROWS))
    tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert tp["F"]["gia_tri"] == F_N and tp["m"]["min"] <= CHOT[1] <= tp["m"]["max"]
    assert abs(F_N / CHOT[0] - CHOT[1]) < 1e-9 and abs((CHOT[1] - M0) / GT - CHOT[2]) < 1e-9
    assert "0,32" in k["so_lieu_mau"]["ghi_chu"] and "3 gia trọng" in k["so_lieu_mau"]["ghi_chu"]
_kiem_so()
TRUN = [math.sqrt(2 * S_M / a) for _, a, _ in ROWS]   # chi de ve chuyen dong (khong hien so)

DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)
TRACK = (176, 184, 200); TRACK_D = (110, 118, 140); BODY = (70, 78, 100)
BLOCK = (120, 92, 60); BLOCK_D = (84, 62, 38); CART = (13, 148, 136); CART_D = (8, 90, 84)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- dung cu (mp4 x = 65 + 0,88x) ----------------
TY = 520; PPM = 720; X0 = 330                     # mep truoc xe khi tha ; di 0,50 m = 360 px
PUX, PUY, PUR = 985, TY + 6, 28; MY0 = 545
CW, CH = 250, 60

def track(d, ty=TY, gates=True, legs=True):
    d.rectangle([40, ty, 955, ty + 30], fill=TRACK); d.line([(40, ty), (955, ty)], fill=TRACK_D, width=4)
    if legs: d.rectangle([60, ty + 30, 84, ty + 120], fill=TRACK_D); d.rectangle([880, ty + 30, 904, ty + 120], fill=TRACK_D)
    d.line([(955, ty + 15), (PUX, ty + 6)], fill=TRACK_D, width=8)
    d.ellipse([PUX - PUR, ty + 6 - PUR, PUX + PUR, ty + 6 + PUR], fill=WHITE, outline=NAVY, width=5); dot(d, PUX, ty + 6, 6, NAVY)
    if gates:
        for x in (X0, X0 + S_M * PPM):
            d.rectangle([x - 8, ty - 150, x + 8, ty], fill=A(PURPLE, 0.6))

def block(d, cx, y, alpha=1.0):
    d.rectangle([cx - 52, y - 40, cx + 52, y], fill=A(BLOCK, alpha), outline=A(BLOCK_D, alpha), width=3)

def cart(d, xf, nb, drops=(), ty=TY, rope=True, lab=None):
    """Mep truoc xe xf, nb gia trong da nam tren xe ; drops = [(j, k 0..1)]: gia trong thu j dang roi tu tren xuong."""
    x0 = xf - CW; cx = xf - CW / 2
    d.rounded_rectangle([x0, ty - CH, xf, ty], radius=10, fill=CART, outline=CART_D, width=4)
    d.rectangle([xf - 4, ty - 50, xf + 26, ty - 18], fill=ORANGE, outline=NAVY, width=3)       # cam bien luc
    yb = ty - CH
    slot = lambda j: (cx + (-56 if j % 2 == 0 else 56), yb - (j // 2) * 42)
    for j in range(nb): block(d, *slot(j))
    for j, k in drops:
        tx, ty_ = slot(j); block(d, tx, lerp(ty_ - 160, ty_, ease(k)), alpha=clamp(k * 3))
    if lab: text(d, (cx, ty - CH / 2), lab, 56, WHITE)
    if rope:
        d.line([(xf + 26, ty - 34), (PUX, ty + 6 - PUR)], fill=NAVY, width=3)
        my = ty + 25 + (xf - X0) * 0.3
        d.line([(PUX + PUR, ty + 6), (PUX + PUR, my)], fill=NAVY, width=3)
        d.rectangle([PUX + PUR - 28, my, PUX + PUR + 22, my + 50], fill=BODY, outline=NAVY, width=3)

def readouts(d, a_s, flash=0.0, y=720):
    card(d, (40, y, 520, y + 100), fill=WHITE, outline=NAVY, w=4, r=20)
    text(d, (280, y + 50), "F = 0,40 N", 60, INK)
    card(d, (560, y, 1040, y + 100), fill=mix(WHITE, (255, 237, 160), flash), outline=BLUE, w=4, r=20)
    text(d, (800, y + 50), "a = " + a_s, 60, BLUE)

XS = (240, 540, 850)
def table(d, n, y=860, ma=0.0, hi=-1, alpha=1.0):
    card(d, (40, y, 1040, y + 140 + 4 * 92), fill=A(WHITE, alpha), outline=A(NAVY, alpha), w=4)
    text(d, (XS[0], y + 62), "m (kg)", 60, INK, alpha=alpha)
    text(d, (XS[1], y + 62), "a (m/s²)", 60, INK, alpha=alpha)
    text(d, (XS[2], y + 62), "m·a (N)", 60, DGREEN, alpha=alpha * ma)
    d.line([(70, y + 116), (1010, y + 116)], fill=A(LIGHT, alpha), width=4)
    for i in range(n):
        yy = y + 170 + i * 92
        if i == hi: card(d, (70, yy - 42, 1010, yy + 42), fill=A((255, 237, 213), alpha), r=18)
        text(d, (XS[0], yy), vn(ROWS[i][0]), 62, INK, alpha=alpha)
        text(d, (XS[1], yy), vn(ROWS[i][1]), 62, BLUE, alpha=alpha)
        text(d, (XS[2], yy), vn(ROWS[i][2]), 62, DGREEN, alpha=alpha * ma)

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    track(d); cart(d, X0, 0)
    yb = TY - CH - 190 + 22 * math.sin(t * 2.4)                       # gia trong cho chat len (lo lung tren xe)
    block(d, X0 - CW / 2, yb); text(d, (X0 - CW / 2 + 130, yb - 20), "0,25 kg", 58, BLOCK_D, anchor="lm")
    readouts(d, "?")
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 860 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 640), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 190), "Giữ F = 0,40 N.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 275), "Xe nặng dần 0,50 → 1,50 kg.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 385), "Đồ thị a theo m", 64, PURPLE, alpha=a)
    text(d, (W / 2, y0 + 465), "có dạng nào?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 535, t, M[1] + 0.2, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (chat gia trong, 4 lan) ----------------
DROP, GAP, BACK = 0.4, 0.3, 0.3
def run_starts():
    ts = [0.6]
    for k in range(3): ts.append(ts[-1] + TRUN[k] + GAP + BACK + DROP + 0.1)
    return ts
RS = run_starts()

def do_state(t):
    """-> (k lan, mep truoc xe, so gia trong tren xe, gia trong dang roi [(j, k)], so hang da do)."""
    k = max(0, sum(1 for r in RS if t >= r) - 1)
    if t < RS[0]: return 0, X0, 0, [], 0
    tau = t - RS[k]; tk = TRUN[k]
    if tau < tk: return k, X0 + S_M * PPM * (tau / tk) ** 2, NB[k], [], k
    if k == 3 or tau < tk + GAP: return k, X0 + S_M * PPM, NB[k], [], k + 1
    x = tau - tk - GAP
    if x < BACK: return k, lerp(X0 + S_M * PPM, X0, ease(x / BACK)), NB[k], [], k + 1
    kk = clamp((x - BACK) / DROP)                                     # cac khoi moi roi CUNG luc
    if kk >= 1: return k, X0, NB[k + 1], [], k + 1
    return k, X0, NB[k], [(j, kk) for j in range(NB[k], NB[k + 1])], k + 1

def s_do(img, d, t, sc):
    k, xf, nb, drops, n = do_state(t)
    track(d); cart(d, xf, nb, drops)
    done = n > k
    flash = 1 - clamp((t - RS[k] - TRUN[k]) / 0.6) if done else 0
    readouts(d, vn(ROWS[k][1]) + " m/s²" if done else "…", flash)
    table(d, n, hi=k if done else -1)

def _kiem_dong_bo():
    """Moi 0,05 s: so gia trong tren xe khi chay = NB[k] ; hang + so a hien CUNG luc xe toi cong 2 ; khong luc nao co 3 khoi."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        k, xf, nb, drops, n = do_state(t)
        tau = t - RS[k]
        if t >= RS[0] and tau < TRUN[k] and (nb != NB[k] or n != k or drops): bad.append(("chay", round(t, 2)))
        if t >= RS[0] and tau >= TRUN[k] and n != k + 1: bad.append(("hang", round(t, 2)))
        if nb == 3: bad.append(("3 khoi", round(t, 2)))
        t += 0.05
    if RS[-1] + TRUN[-1] + 0.8 > sc["T"]: bad.append("lan cuoi qua sat cuoi canh")
    return bad

# ---------------- canh 3: Ket qua (do thi a theo m) + Rut ra (cot m.a) ----------------
GX0, GX1, GY0, GY1 = 230, 940, 1580, 1170      # m 0-1,6 kg ; a 0-1,0
def gx(m): return GX0 + m / 1.6 * (GX1 - GX0)
def gy(a): return GY0 - a / 1.0 * (GY0 - GY1)

def axes(d, y_top=1040):
    card(d, (40, y_top, 1040, 1665), fill=WHITE, outline=LIGHT, w=3)
    for a in (0.2, 0.4, 0.6, 0.8, 1.0):
        d.line([(GX0, gy(a)), (GX1, gy(a))], fill=LIGHT, width=3)
    for a in (0.4, 0.8):
        text(d, (GX0 - 18, gy(a)), vn(a, 1), 56, NAVY, anchor="rm")
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=4)
    text(d, (GX0 + 24, GY1 - 60), "a (m/s²)", 56, INK, anchor="lm")
    text(d, (1020, GY0 - 50), "m (kg)", 56, INK, anchor="rm")
    text(d, (GX0 - 18, GY0 + 10), "0", 56, NAVY, anchor="rm")
    for m in (0.5, 1.0, 1.5):
        d.line([(gx(m), GY0), (gx(m), GY0 + 12)], fill=NAVY, width=3)
        text(d, (gx(m), GY0 + 48), vn(m, 1), 56, NAVY)

def curve(d, k):
    if k <= 0: return
    m1 = lerp(0.5, 1.5, k); pts_ = [(gx(m), gy(F_N / m)) for m in np.linspace(0.5, m1, 40)]
    d.line(pts_, fill=A(GREEN, 0.85), width=7, joint="curve")

def s_dapan(img, d, t, sc):
    M = sc["M"]
    kma = appear(t, M[1] + 0.1, 0.5)
    table(d, 4, y=240, ma=kma)
    kr = appear(t, M[1] + 2.2, 0.45)
    if kr > 0:
        card(d, (40, 870, 1040, 1000), fill=A((236, 253, 243), kr), outline=A(GREEN, kr), r=24, w=5)
        text(d, (W / 2, 935), "m·a gần bằng F = 0,40 N", 62, DGREEN, alpha=kr)
    axes(d); curve(d, appear(t, 0.4, 1.4))
    for m, a, _ in ROWS: dot(d, gx(m), gy(a), 16, BLUE, outline=WHITE)

# ---------------- canh 4: Bay - hai xe cung luc keo chay dua ----------------
SLOW = 1.6
LANE = (720, 1180)
RACE = ((0, ROWS[0]), (2, ROWS[2]))               # (so gia trong, hang): 0,50 kg / 1,00 kg
def s_bay(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.2, 0.45)
    card(d, (40, 230, 1040, 440), fill=A((254, 242, 242), ka), outline=A(DRED, ka), w=6, r=24)
    text(d, (W / 2, 295), "✗ Dễ tưởng: cùng lực kéo", 62, DRED, alpha=ka)
    text(d, (W / 2, 375), "thì cùng gia tốc", 62, DRED, alpha=ka)
    t0 = M[1] + 0.3
    if t < M[1] - 0.2: return
    kb = clamp((t - M[2]) / 0.8)
    for (nb, r), ty in zip(RACE, LANE):
        card(d, (40, ty - 250, 1040, ty + 160), fill=WHITE, outline=LIGHT, w=3)
        track(d, ty, legs=False)
        tk = math.sqrt(2 * S_M / r[1]); tau = clamp((t - t0) / SLOW, 0, tk)
        xf = X0 + S_M * PPM * (tau / tk) ** 2
        cart(d, xf, nb, ty=ty, rope=False)
        d.line([(xf + 26, ty - 34), (PUX, ty + 6 - PUR)], fill=NAVY, width=3)
        text(d, (60, ty + 70), vn(r[0]) + " kg", 60, INK, anchor="lm")
        text(d, (540, ty + 70), "F = 0,40 N", 60, DORANGE, anchor="lm")
        if kb > 0: d.rounded_rectangle([60, ty + 112, 60 + 500 * r[1] * ease(kb) + 8, ty + 146], radius=10, fill=BLUE)   # thanh a
        if tau >= tk - 1e-9:
            text(d, (X0 + S_M * PPM + 40, ty - 200), "a = " + vn(r[1]), 60, BLUE, anchor="lm")

# ---------------- canh 5: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    card(d, (40, 230, 1040, 520), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 310), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 430), "Có ma sát thì sao?", 64, INK)
    card(d, (40, 560, 1040, 1150), fill=WHITE, outline=LIGHT, w=3)
    ty = 950
    d.rectangle([80, ty, 1000, ty + 30], fill=(205, 196, 180))
    for x in range(90, 1000, 34): d.line([(x, ty + 30), (x + 18, ty + 4)], fill=(150, 140, 120), width=3)   # mat nham
    xf = 600 + 60 * ease(t / 2.0)
    cart(d, xf, 2, ty=ty, rope=False)
    k = appear(t, 1.0, 0.6)
    arrow(d, (xf - CW / 2 - 10, ty + 60), (xf - CW / 2 - 200, ty + 60), A(DRED, k), w=9, head=26)
    text(d, (xf - CW / 2 - 105, ty + 120), "?", 80, DRED, alpha=k)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1500), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, W / 2, 310, "THỬ NGHĨ", ORANGE, k1)
    ty = 700
    d.rectangle([90, ty, 990, ty + 26], fill=A(TRACK, k1))
    if k1 > 0.02:
        cart(d, 640, 0, ty=ty, rope=False); text(d, (640 - CW / 2, ty - CH / 2), "0,50 kg", 56, WHITE, alpha=k1)
        block(d, 200, ty - 20); text(d, (200, ty + 70), "0,25 kg", 58, BLOCK_D, alpha=k1)
        text(d, (640 - CW / 2, ty - 150), "+ ?", 80, PURPLE, alpha=k1)
    text(d, (W / 2, 900), "Vẫn F = 0,40 N.", 62, INK, alpha=k1)
    text(d, (W / 2, 1010), "Muốn a = 0,32 m/s²:", 62, DORANGE, alpha=k1)
    text(d, (W / 2, 1100), "thêm mấy khối?", 64, DORANGE, alpha=k1)
    seg_bar(d, 1240, t, 1.0, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = (sc[k] for k in ("hook", "do", "dapan", "bay", "end"))
    t0 = b["M"][1] + 0.3
    return ([(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
            + [(do["t0"] + r + TRUN[i], "tap") for i, r in enumerate(RS)]
            + [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz")]
            + [(b["t0"] + t0 + math.sqrt(2 * S_M / r[1]) * SLOW, "tap") for _, r in RACE]
            + [(e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l10-dl2-newton-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Định luật 2 Newton · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Chất thêm gia trọng", draw=s_hook, tail=0.3, caps=[
   ("Cảm biến giữ F không đổi.", 3.4),
   ("Dừng lại, tự đoán.", 5.1)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.9, caps=[
   ("Lần đầu: xe rỗng.", 3.0),
   ("Mỗi lần chất thêm gia trọng.", 3.4),
   ("Ghi a ở mỗi lần đo.", 3.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Bốn điểm trên một đường cong.", 3.4),
   ("Nhân m với a ở từng hàng.", 4.2)]),
 dict(key="bay", title="Bẫy: cùng lực kéo", draw=s_bay, tail=0.3, caps=[
   ("Đúng hay sai?", 3.0),
   ("Thả hai xe cùng lúc.", 3.2),
   ("Xe nặng gấp đôi, a còn một nửa.", 3.8)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.4, caps=[
   ("Ở đây bỏ qua ma sát.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Giữ F: a tỉ lệ nghịch với m.", 5.0)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
