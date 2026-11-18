# Clip: tn-l10-biendang-02 - Treo qua nang vao lo xo, do do cung k (lo 8, 18/11/2026)
# So lieu tu content/thi-nghiem/tn-l10-biendang-02.json:
#   l0 = 10,0 cm ; g = 9,8 ; so_lieu_mau (m g, F N, l cm, dl cm): 50 0,49 11,9 1,9 ; 100 0,98 13,9 3,9 ; 150 1,47 15,9 5,9 ;
#   200 1,96 17,9 7,9 ; 250 2,45 19,8 9,8. Lo xo ve dung ti le: 52 px moi cm, vach 0 thuoc ngang moc tren.
# KHONG hien cot F/dl va so k (bai giao HS tu tinh F/dl tung hang + tim hang lech nhat - o "Doc so lieu").
# Du doan (K10, khong nut A-D): them tung qua 50 g, moi lan lo xo dai them the nao?
#   A. them deu nhau moi lan (DUNG) ; B. them it dan, lo xo cung dan ; C. them nhieu dan, lo xo mem dan.
# Bo cuc KHAC biendang3 (hai lo xo, the ben phai, cau so sanh): MOT lo xo ben PHAI, thuoc doc so chieu dai l (0 o moc),
#   bang m-F-l-dl ben trai, roi do thi F theo dl (chi trong khoang da do, khong ngoai suy).
# Bay = hien_tuong_hay_sai[0] (lay F chia chieu dai l -> 4,1 ; 7,1 ; 9,2 N/m tang dan, tuong k tang).
# Chot (ca tu suy, ghi ghi_chu kho): treo vat 120 g (trong khoang 50-250 g da do) -> F = 1,176 N, dl = 4,70 cm, l = 14,7 cm.
#   So 120 g chua hien ; can >= 2 buoc. Hop chot chi noi gioi han khoang do, khong ghi cong thuc.
# Dong bo so qua treo <-> chieu dai ve <-> so hang bang: _kiem_dong_bo() (moi 0,05 s).
from engine import *

G, L0 = 9.8, 10.0
ROWS = [(50, 0.49, 11.9, 1.9), (100, 0.98, 13.9, 3.9), (150, 1.47, 15.9, 5.9), (200, 1.96, 17.9, 7.9), (250, 2.45, 19.8, 9.8)]
NOTE = (60, 64, 84); BRASS = (196, 150, 70); BRASS_D = (140, 100, 40); RULER = (255, 241, 205)
def vn(x, n=1): return f"{x:.{n}f}".replace(".", ",")

# ---------------- gia treo + lo xo + thuoc (ben phai) ----------------
SXX, TOP, PX = 760, 330, 52                       # truc lo xo, moc tren (= vach 0 thuoc), px moi cm
RX = 840                                         # mep trai thuoc
MW, MH = 110, 34                                 # qua 50 g
def yl(l): return TOP + l * PX

def stand(d, a=1.0):
    d.rounded_rectangle([1000, 290, 1024, 1672], radius=6, fill=A((170, 175, 190), a))
    d.rounded_rectangle([660, 290, 1024, 318], radius=8, fill=A((150, 155, 172), a))
    d.rounded_rectangle([640, 1664, 1040, 1690], radius=10, fill=A((176, 124, 74), a))

def ruler(d, a=1.0):
    d.rectangle([RX, TOP - 14, RX + 50, yl(21) + 14], fill=A(RULER, a), outline=A(BRASS_D, a), width=3)
    for k in range(211):
        y = TOP + k * PX / 10; L = 30 if k % 10 == 0 else (18 if k % 5 == 0 else 8)
        d.line([(RX, y), (RX + L, y)], fill=A(NAVY, a), width=3 if k % 10 == 0 else 1)
    for c in range(0, 21, 2): text(d, (RX + 62, yl(c)), str(c), 44, INK, anchor="lm", alpha=a)
    text(d, (RX + 25, yl(21) + 60), "cm", 44, NOTE, alpha=a)

def spring(d, yb, a=1.0, x=SXX, top=TOP, n=14, amp=26):
    lead = 22
    pts = [(x, top), (x, top + lead)]
    for i in range(1, 2 * n):
        pts.append((x + (amp if i % 2 else -amp), lerp(top + lead, yb - lead, i / (2 * n))))
    pts += [(x, yb - lead), (x, yb)]
    d.line(pts, fill=A(NAVY, a), width=5, joint="curve")
    d.ellipse([x - 9, yb - 4, x + 9, yb + 14], outline=A(NAVY, a), width=4)

def masses(d, n, yb, a=1.0, x=SXX, lab=False):
    y = yb + 10
    for i in range(n):
        d.line([(x, y), (x, y + 8)], fill=A(NAVY, a), width=4)
        d.rounded_rectangle([x - MW / 2, y + 8, x + MW / 2, y + 8 + MH], radius=8, fill=A(BRASS, a), outline=A(BRASS_D, a), width=3)
        y += MH + 10
    if lab and n: text(d, (x - MW / 2 - 16, (yb + 18 + y) / 2), f"{50 * n} g", 44, INK, anchor="rm", alpha=a)
    return y

def pointer(d, l, a=1.0):
    y = yl(l)
    d.line([(SXX + 14, y), (RX + 34, y)], fill=A(RED, a), width=5)
    d.polygon([(RX + 2, y), (RX - 16, y - 9), (RX - 16, y + 9)], fill=A(RED, a))

def l0_line(d, a=1.0):
    y = yl(L0)
    for x in range(SXX - 60, RX, 22): d.line([(x, y), (x + 11, y)], fill=A(GRAY, a), width=4)

def rig(d, n, l, a=1.0, lab=True):
    stand(d, a); ruler(d, a); l0_line(d, a)
    spring(d, yl(l), a); masses(d, n, yl(l), a, lab=lab); pointer(d, l, a)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    rig(d, 1, ROWS[0][2])
    text(d, (320, 330), "chưa treo: 10,0 cm", 44, NOTE)
    text(d, (320, 400), "1 quả 50 g: 11,9 cm", 46, INK)
    a = appear(t, M[1] - 0.4, 0.5)
    if a <= 0: return
    x0, x1 = 40, 570; cx = (x0 + x1) / 2; y0 = 480 + (1 - a) * 30
    card(d, (x0, y0, x1, y0 + 760), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "Dự đoán", F(42)) + 56
    card(d, (cx - pw / 2, y0 + 26, cx + pw / 2, y0 + 92), fill=A(PURPLE, a), r=32)
    text(d, (cx, y0 + 59), "Dự đoán", 42, WHITE, alpha=a)
    for j, s in enumerate(("Thêm từng quả 50 g.", "Mỗi lần dài", "thêm thế nào?")):
        text(d, (cx, y0 + 180 + j * 74 + (30 if j else 0)), s, 48, INK, alpha=a)
    text(d, (cx, y0 + 530), "Chọn đáp án ở", 40, MUTED, alpha=a)
    text(d, (cx, y0 + 580), "khung câu hỏi", 40, MUTED, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([x0 + 60, y0 + 680, x1 - 60, y0 + 696], radius=8, fill=A(LIGHT, a))
        d.rounded_rectangle([x0 + 60, y0 + 680, x0 + 60 + (x1 - x0 - 120) * (1 - p), y0 + 696], radius=8, fill=A(PURPLE, a))

# ---------------- canh 2: tien hanh ----------------
ST0, PER, SLIDE, SETTLE = 0.5, 2.1, 0.6, 1.3
def osc(tt): return 1 - math.exp(-3.4 * tt) * math.cos(2 * math.pi * 1.4 * tt)
def do_state(t):
    """-> (so qua dang treo, l ve (cm), so hang da ghi, qua dang truot (x, y) hoac None)."""
    n, l, rows, fly = 0, L0, 0, None
    for i in range(5):
        a = ST0 + i * PER
        if t < a: break
        lp = ROWS[i - 1][2] if i else L0; ln = ROWS[i][2]
        if t < a + SLIDE:                         # qua moi truot tu trai vao, treo duoi chum
            k = ease((t - a) / SLIDE); ybot = masses_bottom(i, lp)
            fly = (lerp(560, SXX, k), lerp(ybot + 60, ybot, k)); n, l = i, lp
        else:
            tt = t - a - SLIDE; n = i + 1; l = lp + (ln - lp) * osc(tt)
            if tt >= SETTLE: l = ln; rows = i + 1
            else: rows = i
    return n, l, rows, fly

def masses_bottom(n, l): return yl(l) + 10 + n * (MH + 10)
def t_dapan(): return ST0 + 4 * PER + SLIDE + SETTLE + 0.3

def table(d, rows, a=1.0, x0=40, x1=600, y0=380):
    card(d, (x0, y0, x1, y0 + 100 + 5 * 76), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    xs = (110, 245, 380, 520)
    for x, s in zip(xs, ("m (g)", "F (N)", "l (cm)", "Δl (cm)")): text(d, (x, y0 + 46), s, 40, NOTE, alpha=a)
    d.line([(x0 + 16, y0 + 84), (x1 - 16, y0 + 84)], fill=A(LIGHT, a), width=4)
    for i in range(rows):
        m, f, l, dl = ROWS[i]; y = y0 + 130 + i * 76
        text(d, (xs[0], y), str(m), 44, INK, alpha=a)
        text(d, (xs[1], y), vn(f, 2), 44, BLUE, alpha=a)
        text(d, (xs[2], y), vn(l), 44, INK, alpha=a)
        text(d, (xs[3], y), vn(dl), 44, RED, alpha=a)

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    n, l, rows, fly = do_state(t)
    stand(d); ruler(d); l0_line(d)
    spring(d, yl(l)); masses(d, n, yl(l), lab=True); pointer(d, l)
    if fly:
        x, y = fly
        d.rounded_rectangle([x - MW / 2, y + 8, x + MW / 2, y + 8 + MH], radius=8, fill=BRASS, outline=BRASS_D, width=3)
    text(d, (320, 460), "chưa treo: 10,0 cm", 44, NOTE)
    table(d, rows, y0=520)
    k = appear(t, t_dapan(), 0.4)
    if k > 0:
        card(d, (40, 1050, 600, 1290), fill=A(NAVY, k), r=30)
        text(d, (320, 1105), "ĐÁP ÁN ·", 44, WHITE, alpha=k)
        text(d, (320, 1170), "thêm đều nhau,", 44, WHITE, alpha=k)
        text(d, (320, 1230), "khoảng 2 cm mỗi quả", 44, (253, 224, 71), alpha=k)

def _kiem_dong_bo():
    """Moi 0,05 s: khi so hang = so qua va dung yen, chieu dai ve = l hang cuoi ; hang chi hien khi da on dinh ; kho khop."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; bad = []; t = 0.0
    while t < sc["T"]:
        n, l, rows, fly = do_state(t)
        if rows > n: bad.append(("hang>qua", round(t, 2)))
        if rows == n and n and abs(l - ROWS[n - 1][2]) > 1e-9: bad.append(("lech", round(t, 2)))
        if yl(l) + 10 + n * (MH + 10) > 1655: bad.append(("cham de", round(t, 2)))
        t += 0.05
    for m, f, l, dl in ROWS:
        if abs(m / 1000 * G - f) > 0.006 or abs(l - L0 - dl) > 1e-6 or abs(dl - f / 25 * 100) > 0.11: bad.append(("kho", m))
    if t_dapan() + 1.8 > sc["T"]: bad.append("dap an sat cuoi")
    return bad

# ---------------- canh 3: rut ra ----------------
GX0, GX1, GY0, GY1 = 170, 970, 1300, 840           # do thi: dl 0-10 cm, F 0-2,5 N
def gx(dl): return GX0 + (GX1 - GX0) * dl / 10
def gy(f): return GY0 - (GY0 - GY1) * f / 2.5

def s_rut(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    a = appear(t, 0.2)
    cx, top = 250, 400                           # chum 5 qua (vat dang xet), ve rieng
    bot = top - 18 + 10 + 5 * (MH + 10)
    ka = appear(t, 0.6, 0.4)
    if ka > 0:
        arrow(d, (cx - 80, top), (cx - 80, top - 120), A(GREEN, ka), w=8, head=26)
        arrow(d, (cx + 80, bot), (cx + 80, bot + 120), A(RED, ka), w=8, head=26)
    masses(d, 5, top - 18, a, x=cx)
    if ka > 0:
        text(d, (420, 330), "Lò xo kéo chùm quả lên", 44, GREEN, anchor="lm", alpha=ka)
        text(d, (420, bot + 60), "Trái Đất hút chùm quả xuống", 44, RED, anchor="lm", alpha=ka)
        text(d, (420, 500), "Đứng yên: F = m·g", 46, INK, anchor="lm", alpha=appear(t, 1.4, 0.4))
    # do thi
    kg = appear(t, 0.3, 0.4)
    if kg > 0:
        d.line([(GX0, GY0), (GX1 + 20, GY0)], fill=A(INK, kg), width=4)
        d.line([(GX0, GY0), (GX0, GY1 - 30)], fill=A(INK, kg), width=4)
        for v in (0, 2, 4, 6, 8, 10):
            d.line([(gx(v), GY0), (gx(v), GY0 + 12)], fill=A(INK, kg), width=3)
            text(d, (gx(v), GY0 + 44), str(v), 42, INK, alpha=kg)
        for v in (1, 2):
            d.line([(GX0 - 12, gy(v)), (GX0, gy(v))], fill=A(INK, kg), width=3)
            text(d, (GX0 - 24, gy(v)), str(v), 42, INK, anchor="rm", alpha=kg)
        text(d, (GX1 - 40, GY0 + 92), "Δl (cm)", 42, INK, alpha=kg)
        text(d, (GX0 + 20, GY1 - 50), "F (N)", 42, INK, anchor="lm", alpha=kg)
        for i, (m, f, l, dl) in enumerate(ROWS):
            kp = appear(t, M[1] + 0.3 + i * 0.45, 0.3)
            if kp > 0: dot(d, gx(dl), gy(f), 11, A(BLUE, kp))
        kl = appear(t, M[1] + 2.8, 0.5)
        if kl > 0:                                # chi noi cac diem da do (khong ngoai suy qua 9,8 cm)
            xe = lerp(gx(0), gx(9.8), kl); ye = lerp(gy(0), gy(0.25 * 9.8), kl)
            d.line([(gx(0), gy(0)), (xe, ye)], fill=A(ORANGE, 0.9), width=5)
    k3 = appear(t, M[2] - 0.1, 0.45)
    if k3 > 0:
        y1 = 1450 + (1 - k3) * 20
        card(d, (40, y1, 1040, y1 + 190), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y1 + 52), "Chưa nói được gì?", 44, NAVY, alpha=k3)
        text(d, (W / 2, y1 + 128), "Nặng hơn 250 g: còn thẳng không?", 44, BLUE, alpha=k3)

# ---------------- canh 4: bay ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    a = appear(t, 0.1, 0.4)
    card(d, (40, 280, 1040, 600), fill=A(WHITE, a), outline=A(RED, a), w=6)
    pw = tw(d, "Bẫy", F(42)) + 60
    card(d, (W / 2 - pw / 2, 300, W / 2 + pw / 2, 362), fill=A(RED, a), r=30)
    text(d, (W / 2, 331), "Bẫy", 42, WHITE, alpha=a)
    text(d, (W / 2, 420), "Lấy F chia chiều dài l:", 46, INK, alpha=a)
    text(d, (W / 2, 485), "4,1 → 7,1 → 9,2 N/m", 46, RED, alpha=a)
    text(d, (W / 2, 550), "Tưởng k tăng dần?", 46, INK, alpha=a)
    kx = appear(t, M[1] + 0.2, 0.35)
    if kx > 0:
        w_ = tw(d, "Tưởng k tăng dần?", F(46))
        d.line([(W / 2 - w_ / 2 - 10, 552), (W / 2 + w_ / 2 + 10, 552)], fill=A(RED, kx), width=7)
        text(d, (1010, 330), "✗", 64, RED, anchor="rm", alpha=kx)
    # lo xo 100 g, cung thang 52 px/cm: ngoac l (ca chieu dai) va ngoac dl (phan dai them)
    x, top = 420, 645
    ok = appear(t, M[1] + 1.2, 0.4)
    d.rounded_rectangle([x - 90, top - 22, x + 90, top], radius=6, fill=A((150, 155, 172), a))
    yb = top + ROWS[1][2] * PX
    spring(d, yb, a, x=x, top=top, n=12, amp=22); masses(d, 2, yb, a, x=x)
    y0 = top + L0 * PX
    for xx in range(x - 70, x + 300, 22): d.line([(xx, y0), (xx + 11, y0)], fill=A(GRAY, a), width=4)
    bx = x - 150                                  # ngoac l: tu moc toi dau duoi (hien cung cau sai)
    d.line([(bx, top), (bx, yb)], fill=A(RED, a), width=4)
    for y in (top, yb): d.line([(bx - 10, y), (bx + 10, y)], fill=A(RED, a), width=4)
    text(d, (bx - 18, (top + yb) / 2), "l = 13,9 cm", 44, RED, anchor="rm", alpha=a)
    if ok > 0:
        bx2 = x + 150
        d.line([(bx2, y0), (bx2, yb)], fill=A(GREEN, ok), width=5)
        for y in (y0, yb): d.line([(bx2 - 10, y), (bx2 + 10, y)], fill=A(GREEN, ok), width=5)
        text(d, (bx2 + 20, (y0 + yb) / 2), "Δl = 3,9 cm", 44, GREEN, anchor="lm", alpha=ok)
        card(d, (40, 1490, 1040, 1640), fill=A((220, 252, 231), ok), outline=A(GREEN, ok), w=5)
        text(d, (W / 2, 1565), "✓ Lực đi với phần dài thêm Δl", 46, GREEN, alpha=ok)

# ---------------- canh 5: chot ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    def body(d, t, k):
        kd = appear(t, M[0] + 0.9, 0.5) * k
        if kd > 0:
            x, top = 330, 960
            d.rounded_rectangle([x - 80, top - 22, x + 80, top], radius=6, fill=A((150, 155, 172), kd))
            spring(d, top + 190, kd, x=x, top=top, n=10, amp=20)
            text(d, (x + 70, top + 95), "chưa treo: 10,0 cm", 44, NOTE, anchor="lm", alpha=kd)
            d.rounded_rectangle([x - 60, top + 230, x + 60, top + 300], radius=10, fill=A(BRASS, kd), outline=A(BRASS_D, kd), width=3)
            text(d, (x, top + 265), "120 g", 40, WHITE, alpha=kd)
            arrow(d, (x + 100, top + 265), (x + 160, top + 265), A(PURPLE, kd), w=6, head=18)
            text(d, (x + 180, top + 265), "dài ? cm", 46, PURPLE, anchor="lm", alpha=kd)
        kh = appear(t, M[0] + 2.8, 0.5) * k
        if kh > 0:
            card(d, (110, 1320, 970, 1520), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
            text(d, (W / 2, 1365), "Gợi ý", 42, NOTE, alpha=kh)
            text(d, (W / 2, 1450), "g = 9,8 m/s²", 46, (176, 64, 8), alpha=kh)
    chot_hoi(d, t, sc, "Chỉ kết luận trong khoảng đã đo",
             "Treo vật 120 g vào lò xo này. Lò xo dài bao nhiêu?", body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding")]
            + [(do["t0"] + ST0 + i * PER + SLIDE, "tap") for i in range(5)]
            + [(do["t0"] + t_dapan(), "ding"), (r["t0"] + r["M"][2] - 0.1, "tap"),
               (b["t0"] + b["M"][1] + 0.2, "buzz"), (b["t0"] + b["M"][1] + 1.2, "ding"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l10-biendang-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Biến dạng của vật rắn · thachlab.id.vn", scenes=[
 dict(key="hook", title="Lò xo cạnh thước mm", draw=s_hook, tail=0.3, caps=[
   ("Thước đo chiều dài.", 2.5),
   ("Nghĩ trước khi xem tiếp.", 5.6)]),
 dict(key="do", title="Thêm từng quả nặng", draw=s_do, tail=1.3, caps=[
   ("Mỗi quả nặng 50 g.", 4.0),
   ("Đợi đứng yên mới đọc.", 4.0),
   ("So cột Δl.", 3.4)]),
 dict(key="rut", title="Lực và độ dãn", draw=s_rut, tail=0.3, caps=[
   ("Hai lực lên chùm quả.", 3.0),
   ("Chấm lên đồ thị.", 3.6),
   ("Còn bỏ ngỏ.", 3.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.6, caps=[
   ("Đúng hay sai?", 4.0),
   ("Đo từ đâu tới đâu?", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 7.6)]),
])
