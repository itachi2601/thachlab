# Clip: tn-l10-trong-luc-luc-cang-02 - Do trong luong cac qua nang bang luc ke (30/10/2026; dung lai 27/11/2026 theo
# cong moi viec 4: chu ve >= 55 px, luc ke = engine.luc_ke(), thanh dem lien, Bay hinh tu giai thich, chot A-D o khung).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-trong-luc-luc-cang-02.json (_kiem_so() doi chieu):
#   so_lieu_mau: m (kg) 0,05 / 0,10 / 0,15 / 0,20 ; P doc (N) 0,50 / 0,95 / 1,45 / 1,95 ; P/m 10,0 / 9,5 / 9,67 / 9,75
#   tham_so: g = 9,8 m/s2, sai_so_do 0,05 N (mot vach), m toi da 0,25 kg; dung_cu luc ke 0-2,5 N.
#   ket_qua_ky_vong: mot vach = 10 % so doc o hang dau, 2,6 % o hang cuoi.
# Du doan (K10: chi cau hoi + hinh truc trong): treo 1, 2, 3, 4 qua -> do thi P theo m dang gi? Dap an: thang, qua goc.
#   (Bai da co bang 4 hang ngay duoi clip -> khong hoi so chi 4 qua nhu ban cu.)
# Bay = hien_tuong_hay_sai[1]: P/m hang dau 10,0 lech -> tuong sai luat; hai thanh P canh nhau, cung o do "1 vach".
# Chua noi duoc: chi do o mot noi (P doi khi g doi chua thay) -> hai luc ke "o day" / "dinh nui ?".
# Chot (khung web A-D, kiem-v1 27/11): luc ke 0-2,5 N, toi da may qua 120 g (khoi luong CHUA chieu, m trong 0,05-0,25 kg kho)?
#   P = m.g: 1 qua 1,18 N, 2 qua 0,24 kg -> 2,35 N, 3 qua 3,53 N vuot -> 2 qua. Khong cong 0,50 N/qua tu bang duoc.
from engine import *

ROWS = [(0.05, 0.50, "10,0"), (0.10, 0.95, "9,5"), (0.15, 1.45, "9,67"), (0.20, 1.95, "9,75")]   # so_lieu_mau
G = 9.8; FMAX = 2.5; VACH = 0.05
def fm(x, n=2): return f"{x:.{n}f}".replace(".", ",")

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-trong-luc-luc-cang-02.json")))
    hang = k["so_lieu_mau"]["hang"]
    for (m, p, pm), h in zip(ROWS, hang):
        assert abs(m - h[0]) < 1e-9 and abs(p - h[2]) < 1e-9 and abs(float(pm.replace(",", ".")) - h[3]) < 0.01, (m, h)
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["g"]["gia_tri"] == G and ts["P"]["sai_so_do"] == VACH and ts["m"]["max"] == 0.25
    assert 2 * 0.12 * G <= FMAX < 3 * 0.12 * G and 2 * 0.12 <= ts["m"]["max"]   # dap so chot: 2 qua 120 g
_kiem_so()

BRASS = (226, 186, 110); BRASS_D = (150, 110, 50); DGREEN = (21, 110, 55); DRED = (185, 28, 28)
DPURPLE = (88, 28, 135); DORANGE = (176, 64, 8)

def think_bar(d, t, t1, t2, y, a, col=DPURPLE, x0=80, x1=1000, h=92):
    """Thanh dem LIEN (khong chia o: so o khong goi dap an), cao 92 px, mau dam -> --do-chu thay hinh doi."""
    q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([x0, y, x1, y + h], radius=h // 2, fill=A(WHITE, a), outline=A((148, 140, 128), a), width=4)
    if q < 1: d.rounded_rectangle([x0, y, x0 + max(h, (x1 - x0) * (1 - q)), y + h], radius=h // 2, fill=A(col, a))

def pill(d, s, y, a, color=NAVY, size=56, cx=W / 2):
    pw = tw(d, s, F(size)) + 64
    card(d, (cx - pw / 2, y - 40, cx + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (cx, y), s, size, WHITE, alpha=a)

# ---------------- gia treo + luc ke (engine.luc_ke) + qua nang ----------------
LX = 300                       # truc luc ke
BODY = 440
YH = 282 + BODY + 36 + 14      # y moc luc ke (vong treo sat thanh ngang gia y 282)
UNIT = 92                      # chieu cao mot qua (moc + than)
Q0 = lambda s, h=0.0: (LX + h, YH - s)
def needle_y(f, yh=YH):
    b0, b1 = 20, 20 + BODY; z0, zf = b1 - 58, b0 + 40
    return yh - (z0 - (z0 - zf) * f / FMAX)

def stand(d):
    d.rounded_rectangle([96, 262, 124, 1560], radius=8, fill=(170, 175, 190))
    d.rounded_rectangle([96, 256, 420, 282], radius=8, fill=(150, 155, 172))
    d.rounded_rectangle([50, 1560, 470, 1600], radius=10, fill=(176, 124, 74))
    d.line([(LX, 282), (LX, 300)], fill=NAVY, width=5)

def mass(d, cx, ytop, alpha=1.0, lbl=True, ten="50 g"):
    """Mot qua nang 50 g co moc: vong moc tren, than tru dong thau, moc duoi."""
    d.arc([cx - 12, ytop, cx + 12, ytop + 22], 180, 360, fill=A(NAVY, alpha), width=4)
    d.line([(cx, ytop + 10), (cx, ytop + 18)], fill=A(NAVY, alpha), width=4)
    d.rounded_rectangle([cx - 76, ytop + 18, cx + 76, ytop + 84], radius=12, fill=A(BRASS, alpha), outline=A(BRASS_D, alpha), width=3)
    if lbl: text(d, (cx, ytop + 51), ten, 56, INK, alpha=alpha)
    d.line([(cx, ytop + 84), (cx, ytop + UNIT)], fill=A(NAVY, alpha), width=4)

def scale(d, f_read, n, extra=None, ex_a=0.0, tag=None, yh=YH, lx=LX, an=False, alpha=1.0, so=(0, 1, 2)):
    """Luc ke 0-2,5 N vach 0,05 N treo thang (luc_ke, moc o duoi); n qua treo duoi moc; tag: so doc canh kim."""
    Q = lambda s, h=0.0: (lx + h, yh - s)
    luc_ke(d, Q, 0, 20, 20 + BODY, FMAX, None if an else f_read, nho=VACH, so=so, hw=48, ben=-1, co=56, alpha=alpha, an=an)
    for i in range(n): mass(d, lx, yh + 12 + i * UNIT, alpha=alpha)
    if extra is not None and ex_a > 0: mass(d, extra[0], extra[1], alpha=ex_a)
    if tag:
        y = needle_y(f_read, yh)
        d.polygon([(lx + 56, y), (lx + 76, y - 14), (lx + 76, y + 14)], fill=A(RED, alpha))
        text(d, (lx + 84, y), tag, 60, RED, anchor="lm", alpha=alpha)

def axes(d, box, k, lab=True):
    """Truc P-m (khung Du doan: trong; canh do thi: co diem)."""
    x0, y0, x1, y1 = box
    d.line([(x0, y1), (x1, y1)], fill=A(NAVY, k), width=5); d.line([(x0, y1), (x0, y0)], fill=A(NAVY, k), width=5)
    arrow(d, (x1 - 30, y1), (x1, y1), A(NAVY, k), w=5, head=20); arrow(d, (x0, y0 + 30), (x0, y0), A(NAVY, k), w=5, head=20)
    if lab:
        text(d, (x0 + 24, y0 + 10), "P", 60, INK, anchor="lm", alpha=k)
        text(d, (x1 - 10, y1 - 50), "m", 60, INK, anchor="rm", alpha=k)
        text(d, (x0 - 34, y1 + 30), "O", 56, INK, alpha=k)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    stand(d)
    f = ROWS[0][1] + (0 - ROWS[0][1]) * math.exp(-3.0 * max(0, t - 0.6)) * math.cos(2 * math.pi * 1.4 * max(0, t - 0.6)) \
        if t > 0.6 else 0.0
    settled = t > 2.4
    scale(d, f, 1 if t > 0.3 else 0, tag=fm(ROWS[0][1]) + " N" if settled else None)
    if t <= 0.3: mass(d, LX + 200, YH + 12 - 40, alpha=1 - clamp(t / 0.3))
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    card(d, (595, 300, 1040, 960), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    axes(d, (680, 360, 1010, 860), a)
    text(d, (845, 620), "?", 110, DPURPLE, alpha=a)
    y0 = 1010 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 70, a, PURPLE)
    text(d, (W / 2, y0 + 190), "Treo 1, 2, 3, 4 quả.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 290), "Đồ thị P theo m dạng gì?", 62, DPURPLE, alpha=a)
    think_bar(d, t, M[1] + 0.4, sc["T"] - 0.2, y0 + 410, a)

# ---------------- canh 2: Tien hanh ----------------
ADD = [0.5, 3.0, 5.5]            # moc giay (tinh tu M[0]) treo them qua thu 2, 3, 4
HANG = 0.7                       # thoi gian dua qua vao moc
def p_at(t, sc):
    """So chi: dao dong tat dan quanh so doc moi roi dung yen (doi dung yen roi doc)."""
    P, n, extra, ex_a, settled = ROWS[0][1], 1, None, 0.0, True
    for i, a in enumerate(ADD):
        s = sc["M"][0] + a
        if t < s: break
        tau = t - s
        if tau < HANG:
            k = ease(tau / HANG)
            extra = (lerp(480, LX, k), YH + 12 + (i + 1) * UNIT - (1 - k) * 60); ex_a = clamp(k * 3)
            P, n, settled = ROWS[i][1], i + 1, False
        else:
            tt = tau - HANG; p0, p1 = ROWS[i][1], ROWS[i + 1][1]
            P = p1 + (p0 - p1) * math.exp(-3.2 * tt) * math.cos(2 * math.pi * 1.6 * tt)
            n, extra, ex_a, settled = i + 2, None, 0.0, tt > 1.2
    return P, n, extra, ex_a, settled

def row_at(i, sc): return 0.2 if i == 0 else sc["M"][0] + ADD[i - 1] + HANG + 1.2

def s_do(img, d, t, sc):
    stand(d)
    P, n, extra, ex_a, settled = p_at(t, sc)
    scale(d, P, n, extra, ex_a, tag=fm(ROWS[n - 1][1]) + " N" if settled else None)
    card(d, (600, 300, 1040, 860), fill=WHITE, outline=NAVY, w=4)
    xs = (720, 930)
    text(d, (xs[0], 360), "m (kg)", 56, INK); text(d, (xs[1], 360), "P (N)", 56, INK)
    d.line([(620, 405), (1020, 405)], fill=LIGHT, width=4)
    last = max([i for i in range(4) if t >= row_at(i, sc)], default=-1)
    for i, (m, p, _) in enumerate(ROWS):
        a = appear(t, row_at(i, sc), 0.35); y = 470 + i * 100
        if a <= 0: continue
        if i == last: d.rounded_rectangle([615, y - 42, 1025, y + 42], radius=16, fill=A((225, 236, 255), a))
        text(d, (xs[0], y), fm(m), 60, BLUE, alpha=a); text(d, (xs[1], y), fm(p), 60, RED, alpha=a)

def _kiem_dong_bo():
    """Hang bang chi hien khi kim da dung yen dung so doc cua hang do; kim khong vuot thang."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; bad = []; t = 0.0
    while t < sc["T"]:
        P, n, extra, ex_a, settled = p_at(t, sc)
        if not 0 <= P <= FMAX: bad.append((round(t, 2), "kim ngoai thang"))
        for i in range(4):
            if t >= row_at(i, sc) and n < i + 1: bad.append((round(t, 2), "hang som", i))
        t += 0.05
    for i in range(1, 4):                                  # luc hang hien: kim da yen o dung so doc
        P = p_at(row_at(i, sc) + 0.05, sc)[0]
        if abs(P - ROWS[i][1]) > 0.02: bad.append(("kim chua yen khi ghi hang", i, round(P, 3)))
    if row_at(3, sc) > sc["T"] - 1.0: bad.append("hang 4 qua muon")
    return bad

# ---------------- canh 3: do thi P theo m -> dap an ----------------
GX0, GX1, GYB, GYT = 200, 980, 960, 340
def gX(m): return GX0 + m / 0.25 * (GX1 - GX0)
def gY(p): return GYB - p / 2.5 * (GYB - GYT)
def s_graph(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 1050), fill=WHITE, outline=LIGHT, w=3)
    for p_ in (1, 2): d.line([(GX0, gY(p_)), (GX1, gY(p_))], fill=(236, 230, 220), width=3)
    axes(d, (GX0, GYT - 40, GX1 + 30, GYB), 1.0)
    for m in (0.1, 0.2):
        d.line([(gX(m), GYB), (gX(m), GYB + 12)], fill=NAVY, width=4); text(d, (gX(m), GYB + 50), fm(m, 1), 56, INK)
    for p_ in (1, 2):
        d.line([(GX0 - 12, gY(p_)), (GX0, gY(p_))], fill=NAVY, width=4); text(d, (GX0 - 24, gY(p_)), str(p_), 56, INK, anchor="rm")
    k = ease((t - M[0] - 1.4) / 1.2)          # duong thang tu goc toa do (do doc = g)
    if k > 0:
        me = 0.23 * k
        d.line([(gX(0), gY(0)), (gX(me), gY(G * me))], fill=A(BLUE, 0.75), width=7)
    for i, (m, p, _) in enumerate(ROWS):
        a = appear(t, 0.2 + i * 0.3, 0.4)
        if a > 0: dot(d, gX(m), gY(p), 18 * back(a), ORANGE, WHITE)
    pill(d, "Đáp án: thẳng, qua gốc O", 1110, appear(t, M[1] - 0.1, 0.45), GREEN)
    kc = appear(t, M[1] + 2.5, 0.45)
    if kc > 0:
        card(d, (60, 1200, 1020, 1330), fill=A((239, 246, 255), kc), outline=A(BLUE, kc), r=24, w=5)
        text(d, (W / 2, 1265), "P/m ≈ 9,8 N/kg ≈ g", 60, BLUE, alpha=kc)

# ---------------- canh 4: Bay - hang dau lech 10,0 -> tuong sai luat; cung o "1 vach" tren hai thanh ----------------
BX0, PXN = 130, 400               # x goc thanh, px moi N
def s_bay(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, M[0] + 1.7, 0.45)
    card(d, (60, 270, 1020, 380), fill=A((254, 242, 242), k1), outline=A(DRED, k1), r=24, w=6)
    text(d, (W / 2, 325), "✗ Dễ tưởng: P không tỉ lệ m", 58, DRED, alpha=k1)
    text(d, (W / 2, 1300), "1 vạch = 0,05 N", 58, INK, alpha=k1)            # kiem-v1: noi vach truoc ngoac do
    kb = appear(t, M[1] - 0.1, 0.45)
    for j, (i, pct, y) in enumerate(((0, "10%", 560), (3, "2,6%", 900))):
        m, p, pm = ROWS[i]
        card(d, (40, y - 140, 1040, y + 160), fill=WHITE, outline=LIGHT, w=3)
        text(d, (BX0 - 50, y - 85), f"{fm(m)} kg", 58, INK, anchor="lm")
        text(d, (1010, y - 85), "P/m = " + pm, 58, DORANGE, anchor="rm")
        d.rounded_rectangle([BX0, y - 28, BX0 + p * PXN, y + 28], radius=12, fill=ORANGE)
        text(d, (BX0 + p * PXN + 44 if i == 0 else BX0 + p * PXN - 24, y), fm(p) + " N", 58, INK if i == 0 else WHITE,
             anchor="lm" if i == 0 else "rm")
        if kb > 0:
            e0, e1 = BX0 + (p - VACH) * PXN, BX0 + (p + VACH) * PXN
            d.rectangle([e0, y - 44, e1, y + 44], outline=A(RED, kb), width=6)
            text(d, (e0 - 10 if i else BX0, y + 100), "1 vạch ≈ " + pct + " số đọc", 56, RED, anchor="rm" if i else "lm",
                 alpha=kb * appear(t, M[1] + 0.4 + j * 0.25, 0.4))
    k3 = appear(t, M[2] + 0.3, 0.45)
    if k3 > 0:
        card(d, (60, 1110, 1020, 1220), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), r=24, w=6)
        text(d, (W / 2, 1165), "✓ Lệch nằm trong sai số đọc", 58, DGREEN, alpha=k3)

# ---------------- canh 5: Chua noi duoc - chi do o mot noi ----------------
def s_gioihan(img, d, t, sc):
    card(d, (40, 260, 1040, 380), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 320), "Chưa nói được", 60, NAVY)
    yh = 430 + BODY + 36 + 14
    for cx, lab, an in ((300, "ở đây", False), (780, "đỉnh núi", True)):
        d.rounded_rectangle([cx - 160, 404, cx + 160, 430], radius=8, fill=(150, 155, 172))
        d.line([(cx, 430), (cx, 448)], fill=NAVY, width=5)
        tau = max(0.0, t - 0.3)
        f = ROWS[0][1] * (1 - math.exp(-3.0 * tau) * math.cos(2 * math.pi * 1.4 * tau))
        scale(d, f, 1, yh=yh, lx=cx, an=an, so=(0, 1, 2))
        text(d, (cx, yh + 150), lab, 60, INK)
        if an:                                              # dau hoi nhip nhe canh kim (hinh khong dung yen)
            pz = 1 + 0.2 * math.sin(2 * math.pi * 0.9 * t)
            dot(d, cx + 170, needle_y(ROWS[0][1], yh), 52 * pz, DPURPLE); text(d, (cx + 170, needle_y(ROWS[0][1], yh) + 2), "?", int(70 * pz), WHITE)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1590), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 300, k1, ORANGE)
    yh = 380 + BODY + 36 + 14
    d.rounded_rectangle([140, 354, 460, 380], radius=8, fill=A((150, 155, 172), k1))
    d.line([(LX, 380), (LX, 398)], fill=A(NAVY, k1), width=5)
    scale(d, 0.0, 0, yh=yh, alpha=k1, so=(0, 1, 2))                   # kiem-v1: bo so 2,5 chong chu N
    for i in range(2): mass(d, LX, yh + 12 + i * UNIT, alpha=0.45 * k1, lbl=i == 0, ten="120 g")
    text(d, (LX + 130, yh + 12 + UNIT), "?", 96, DORANGE, alpha=k1)
    text(d, (760, 560), "Lực kế chỉ", 60, INK, alpha=k1)
    text(d, (760, 650), "tới 2,5 N.", 60, INK, alpha=k1)
    text(d, (W / 2, 1180), "Treo tối đa mấy quả 120 g?", 64, DORANGE, alpha=k1)
    think_bar(d, t, 1.0, sc["T"] - 0.2, 1330, k1, col=DORANGE)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, g, b, e = sc["hook"], sc["do"], sc["graph"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 1.0, "ding"),
            (do["t0"] + do["M"][0] + ADD[0], "tap"), (g["t0"] + g["M"][1] - 0.1, "ding"),
            (b["t0"] + b["M"][0] + 1.7, "buzz"), (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l10-trong-luc-luc-cang-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Trọng lực và lực căng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Treo quả nặng vào lực kế", draw=s_hook, tail=0.3, caps=[
   ("Kim ở 0, treo một quả 50 g.", 3.4),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Thêm từng quả, đọc số chỉ", draw=s_do, tail=0.5, caps=[
   ("Thêm từng quả, đợi kim đứng yên.", 4.4),
   ("Đọc số chỉ, ghi vào bảng.", 4.6)]),
 dict(key="graph", title="Đồ thị P theo m", draw=s_graph, tail=0.4, caps=[
   ("Bốn điểm gần một đường thẳng.", 3.4),
   ("Khối lượng gấp đôi, P gấp đôi.", 4.0)]),
 dict(key="bay", title="Bẫy: hàng đầu lệch", draw=s_bay, tail=0.4, caps=[
   ("Hàng đầu lệch xa nhất.", 3.6),
   ("Cùng sai một vạch.", 3.2),
   ("Vật nặng hơn, tin cậy hơn.", 3.2)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.6, caps=[
   ("Chỉ đo ở một nơi.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Thử tính, rồi chọn đáp án.", 5.8)]),
])

_b = _kiem_dong_bo(); assert not _b, _b
