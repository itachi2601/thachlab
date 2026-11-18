# Clip: tn-l10-biendang-01 - Lo xo but bi: bien dang dan hoi va bien dang deo (lo 8, 18/11/2026)
# So lieu tu content/thi-nghiem/tn-l10-biendang-01.json:
#   tham_so k = 200 N/m (0,5 cm moi N), F_gh = 4 N ; so_lieu_mau F = 1 / 3 N -> dl 0,5 / 1,5 cm, tha ve dung chieu dai cu ;
#   6 N: khong con ti le, dai han ra. Kho them (lo 8): l0 = 4,0 cm ; 6 N: dang keo dai 9,5 cm, tha ra dai 6,5 cm
#   (do lai dan hoi khi tha = 6 / 200 = 3 cm, nen 9,5 - 3 = 6,5 ; neu con ti le 6 N chi dai 7,0 cm).
# Du doan (K10, khong nut A-D): keo nhe tha ve 4,0 cm ; keo 6 N roi tha, lo xo dai bao nhieu?
#   A. ve dung 4,0 cm nhu lan keo nhe ; B. dai hon 4,0 cm, khong ve nhu cu (DUNG) ; C. ngan hon 4,0 cm vi co manh hon.
# Bo cuc KHAC biendang3 (treo doc, hai lo xo, the ben phai): lo xo NAM NGANG tren thuoc co so 0-10 cm,
#   luc ke ngang (luc_ke engine, so nguyen 0-8 N) moc dau phai ; bang 3 hang + the o duoi.
# Bay = hien_tuong_hay_sai[1] (chi vat mem nhu dat nan moi bien dang deo).
# Chot (ca tu suy, ghi ghi_chu kho): lo xo MOI cung loai, keo 2,5 N (trong khoang da do 1-3 N, deu ve) -> dang keo dai
#   4,0 + 2,5 . 0,5 = 5,25 cm ~ 5,3 cm. So 2,5 N chua hien ; can 2 buoc (do dan moi N, cong l0). Hop chot khong ghi cong thuc.
# Dong bo kim <-> chieu dai lo xo <-> hang bang: _kiem_dong_bo() (moi 0,05 s).
from engine import *

K_CM = 0.5                                       # cm moi N (k = 200 N/m)
L0, F_GH = 4.0, 4.0
ROWS = [(1, 4.5, 4.0), (3, 5.5, 4.0), (6, 9.5, 6.5)]   # (F N, dai khi dang keo cm, dai sau khi tha cm)
L_DU = 6.5                                        # chieu dai sau khi tha lan keo 6 N
FMAX = 8.0
NOTE = (60, 64, 84)
def vn(x, n=1): return f"{x:.{n}f}".replace(".", ",")

def l_model(f, peak, loading):
    """Chieu dai (cm) khi luc f, lan keo co luc lon nhat peak."""
    if peak <= F_GH: return L0 + K_CM * f
    if loading: return L0 + K_CM * f if f <= F_GH else L0 + K_CM * F_GH + (f - F_GH) * 1.75
    return L_DU + K_CM * f                       # tha: co lai dan hoi theo cung k

# ---------------- bo cuc ----------------
X0, SY, PX = 92, 540, 56                          # dau trai lo xo (vach 0), truc lo xo, px moi cm
RY = 620                                         # mep tren thuoc
def xl(l): return X0 + l * PX

def spring(d, xe, y=SY, alpha=1.0, n=13, amp=24, w=5, col=NAVY):
    lead = 14
    pts = [(X0 if xe > X0 else xe, y)]
    x0 = pts[0][0]
    pts = [(x0, y), (x0 + lead, y)]
    for i in range(1, 2 * n):
        pts.append((lerp(x0 + lead, xe - lead, i / (2 * n)), y + (amp if i % 2 else -amp)))
    pts += [(xe - lead, y), (xe, y)]
    d.line(pts, fill=A(col, alpha), width=w, joint="curve")

def spring_at(d, x0, xe, y, alpha=1.0, n=13, amp=20, w=5):
    lead = 12
    pts = [(x0, y), (x0 + lead, y)]
    for i in range(1, 2 * n):
        pts.append((lerp(x0 + lead, xe - lead, i / (2 * n)), y + (amp if i % 2 else -amp)))
    pts += [(xe - lead, y), (xe, y)]
    d.line(pts, fill=A(NAVY, alpha), width=w, joint="curve")

def clamp_wall(d, alpha=1.0):
    d.rounded_rectangle([40, SY - 90, X0 - 4, SY + 90], radius=8, fill=A((150, 155, 172), alpha))
    for y in range(SY - 80, SY + 90, 26): d.line([(40, y + 18), (X0 - 8, y)], fill=A((120, 125, 140), alpha), width=3)

def ruler(d, alpha=1.0):
    d.rectangle([X0 - 14, RY, xl(10) + 14, RY + 64], fill=A((255, 241, 205), alpha), outline=A((140, 100, 40), alpha), width=3)
    for k in range(101):
        x = X0 + k * PX / 10; L = 30 if k % 10 == 0 else (20 if k % 5 == 0 else 10)
        d.line([(x, RY), (x, RY + L)], fill=A(NAVY, alpha), width=3 if k % 10 == 0 else 2)
    for c in range(11): text(d, (xl(c), RY + 98), str(c), 44, INK, alpha=alpha)
    text(d, (xl(10) + 4, RY + 150), "cm", 44, NOTE, alpha=alpha)

def marker(d, l, col=RED, alpha=1.0):
    x = xl(l)
    for y in range(SY + 30, RY, 16): d.line([(x, y), (x, y + 8)], fill=A(col, alpha), width=4)
    d.polygon([(x, RY + 2), (x - 11, RY - 16), (x + 11, RY - 16)], fill=A(col, alpha))

def rig(d, l, f_read, alpha=1.0, dyn=True):
    clamp_wall(d, alpha); ruler(d, alpha)
    xe = xl(l); spring(d, xe, alpha=alpha)
    if dyn:
        Q = lambda s, h: (xe + s, SY + h)
        luc_ke(d, Q, 0, 22, 372, FMAX, f_read, nho=0.5, so=(0, 2, 4, 6, 8), hw=40, ben=-1, alpha=alpha, co=44)
    marker(d, l, alpha=alpha)

def readout(d, s, col, a=1.0):
    card(d, (40, 820, 1040, 925), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    text(d, (W / 2, 872), s, 46, col, alpha=a)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    text(d, (W / 2, 310), "Lò xo bút bi, dài 4,0 cm", 48, INK)
    text(d, (W / 2, 390), "Lực kế kéo lò xo", 44, NOTE)
    rig(d, L0, None)
    a = appear(t, M[1] - 0.4, 0.5)
    if a <= 0: return
    y0 = 860 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "Dự đoán", F(42)) + 56
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 59), "Dự đoán", 42, WHITE, alpha=a)
    text(d, (W / 2, y0 + 190), "Kéo 6 N rồi thả.", 52, INK, alpha=a)
    text(d, (W / 2, y0 + 270), "Lò xo dài bao nhiêu?", 52, INK, alpha=a)
    text(d, (W / 2, y0 + 410), "Chọn đáp án ở khung câu hỏi", 40, MUTED, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 520, 940, y0 + 536], radius=8, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 520, 140 + 800 * (1 - p), y0 + 536], radius=8, fill=A(PURPLE, a))

# ---------------- canh 2: tien hanh ----------------
UP = (1.0, 1.0, 1.5)                              # thoi gian keo len moi lan
HOLD, DOWN, SET = 1.0, 0.7, 0.15
def plan(sc):
    """-> [(bat dau, het keo, het giu, het tha)] theo moc phu de."""
    out = []
    for i in range(3):
        a = sc["M"][i] + 0.15; b = a + UP[i]; c = b + HOLD; e = c + DOWN
        out.append((a, b, c, e))
    return out

def do_state(t, sc):
    """-> (f, l, o bang da ghi [(hang, cot)], on dinh?, lan keo hien tai)."""
    P = plan(sc); f, l, cells, steady, cur = 0.0, L0, [], True, -1
    for i, (a, b, c, e) in enumerate(P):
        F0 = ROWS[i][0]
        if t < a: break
        cur = i
        if t < b:   f = F0 * ease((t - a) / (b - a)); l = l_model(f, F0, True); steady = False
        elif t < c: f = F0; l = l_model(f, F0, True); steady = t >= b + SET
        elif t < e: f = F0 * (1 - ease((t - c) / (e - c))); l = l_model(f, F0, False); steady = False
        else:       f = 0.0; l = l_model(0.0, F0, False); steady = t >= e + SET
        if t >= b + SET: cells.append((i, 1))
        if t >= e + SET: cells.append((i, 2))
    return f, l, cells, steady, cur

def table(d, cells, hl=None, a=1.0, y0=830):
    card(d, (40, y0, 1040, y0 + 470), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    xs = (190, 520, 860)
    for x, s in zip(xs, ("lực", "đang kéo", "đã thả")): text(d, (x, y0 + 50), s, 44, NOTE, alpha=a)
    d.line([(60, y0 + 88), (1020, y0 + 88)], fill=A(LIGHT, a), width=4)
    for i, (f, l1, l2) in enumerate(ROWS):
        y = y0 + 160 + i * 110
        if hl == i: d.rounded_rectangle([56, y - 46, 1024, y + 46], radius=16, fill=A((254, 226, 226), a))
        if any(r == i for r, _ in cells): text(d, (xs[0], y), f"{f} N", 50, BLUE, alpha=a)
        if (i, 1) in cells: text(d, (xs[1], y), f"dài {vn(l1)} cm", 50, INK, alpha=a)
        if (i, 2) in cells: text(d, (xs[2], y), f"dài {vn(l2)} cm", 50, RED if l2 != L0 else INK, alpha=a)

def t_dapan(sc): return plan(sc)[2][3] + SET + 0.3

def s_do(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    f, l, cells, steady, cur = do_state(t, sc)
    text(d, (W / 2, 390), "Lực kế kéo lò xo", 44, NOTE)
    rig(d, l, f)
    ta = t_dapan(sc)
    table(d, cells, hl=2 if t >= ta else None)
    k = appear(t, ta, 0.4)
    if k > 0:
        card(d, (40, 1350, 1040, 1490), fill=A(NAVY, k), r=30)
        text(d, (W / 2, 1420), "ĐÁP ÁN · dài hơn 4,0 cm, không về", 46, WHITE, alpha=k)

def _kiem_dong_bo():
    """Moi 0,05 s: lo xo on dinh = mo hinh = hang bang ; o bang chi hien khi on dinh ; kho khop k."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; bad = []; t = 0.0
    while t < sc["T"]:
        f, l, cells, steady, cur = do_state(t, sc)
        if steady and cur >= 0:
            want = ROWS[cur][1] if f > 0 else ROWS[cur][2]
            if abs(l - want) > 1e-6: bad.append(("lech", round(t, 2)))
            if f > 0 and (cur, 1) not in cells: bad.append(("chua ghi", round(t, 2)))
            if abs(f - (ROWS[cur][0] if (cur, 2) not in cells else 0.0)) > 1e-9: bad.append(("kim", round(t, 2)))
        for i, c in cells:
            if c == 1 and abs(l_model(ROWS[i][0], ROWS[i][0], True) - ROWS[i][1]) > 1e-6: bad.append(("hang", i))
            if c == 2 and abs(l_model(0, ROWS[i][0], False) - ROWS[i][2]) > 1e-6: bad.append(("tha", i))
        t += 0.05
    P = plan(sc)
    for i, (a, b, c, e) in enumerate(P):
        if e + SET > (sc["M"][i + 1] if i + 1 < len(sc["M"]) else sc["T"]): bad.append(("tran", i))
    if t_dapan(sc) + 1.5 > sc["T"]: bad.append("dap an sat cuoi")
    for f, l1, _ in ROWS[:2]:
        if abs(L0 + f * 100 / 200 - l1) > 1e-6: bad.append(("k", f))
    if abs(l_model(6, 6, True) - l_model(6, 6, False)) > 1e-6: bad.append("noi 6N")
    return bad

# ---------------- canh 3: rut ra ----------------
def mini(d, x0, y, l, alpha, ghost=None):
    """Lo xo nho dung ti le PX/cm (cung thang canh do) + vach chieu dai cu (net dut)."""
    d.rounded_rectangle([x0 - 26, y - 46, x0 - 2, y + 46], radius=6, fill=A((150, 155, 172), alpha))
    spring_at(d, x0, x0 + l * PX, y, alpha=alpha)
    if ghost is not None:
        xg = x0 + ghost * PX
        for yy in range(y - 60, y + 64, 18): d.line([(xg, yy), (xg, yy + 9)], fill=A(GRAY, alpha), width=4)

def s_rut(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    a = appear(t, 0.2)
    card(d, (40, 290, 1040, 590), fill=A(WHITE, a), outline=A(GREEN, a), w=5)
    text(d, (W / 2, 345), "1 N, 3 N: về 4,0 cm", 46, INK, alpha=a)
    mini(d, 120, 450, L0, a)
    text(d, (120 + L0 * PX + 60, 450), "Đàn hồi", 50, GREEN, anchor="lm", alpha=a)
    b = appear(t, M[0] + 1.6, 0.4)
    if b > 0:
        card(d, (40, 620, 1040, 940), fill=A(WHITE, b), outline=A(RED, b), w=5)
        text(d, (W / 2, 675), "6 N: còn dài 6,5 cm", 46, INK, alpha=b)
        mini(d, 120, 780, L_DU, b, ghost=L0)
        xg, xe = 120 + L0 * PX, 120 + L_DU * PX
        d.line([(xg, 852), (xe, 852)], fill=A(RED, b), width=4)
        for x in (xg, xe): d.line([(x, 840), (x, 864)], fill=A(RED, b), width=4)
        text(d, (xe + 30, 852), "dư 2,5 cm", 44, RED, anchor="lm", alpha=b)
        text(d, (xe + 30, 772), "Dẻo, hỏng", 50, RED, anchor="lm", alpha=b)
    k3 = appear(t, M[1] - 0.1, 0.45)
    if k3 > 0:
        y1 = 1010 + (1 - k3) * 30
        card(d, (40, y1, 1040, y1 + 280), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y1 + 60), "Chưa nói được gì?", 46, NAVY, alpha=k3)
        ctext(d, y1 + 170, "Giới hạn ở đâu giữa 3 N và 6 N?", 46, BLUE, alpha=k3)

# ---------------- canh 4: bay ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    a = appear(t, 0.1, 0.4)
    card(d, (40, 280, 1040, 500), fill=A(WHITE, a), outline=A(RED, a), w=6)
    pw = tw(d, "Bẫy", F(42)) + 60
    card(d, (W / 2 - pw / 2, 300, W / 2 + pw / 2, 362), fill=A(RED, a), r=30)
    text(d, (W / 2, 331), "Bẫy", 42, WHITE, alpha=a)
    ctext(d, 435, "Chỉ vật mềm mới biến dạng dẻo?", 48, INK, alpha=a)
    cx, cy = W / 2, 650                          # dat nan (vat mem) hien cung cau sai
    d.ellipse([cx - 130, cy - 70, cx + 130, cy + 70], fill=A((248, 180, 120), a), outline=A((190, 110, 50), a), width=4)
    d.ellipse([cx - 50, cy - 34, cx + 4, cy - 4], fill=A((252, 205, 160), a))
    text(d, (cx, cy + 115), "đất nặn", 44, NOTE, alpha=a)
    kx = appear(t, M[1] + 0.2, 0.35)
    if kx > 0:
        w_ = tw(d, "Chỉ vật mềm mới biến dạng dẻo?", F(48))
        d.line([(W / 2 - w_ / 2 - 10, 437), (W / 2 + w_ / 2 + 10, 437)], fill=A(RED, kx), width=7)
        text(d, (1020, 330), "✗", 64, RED, anchor="rm", alpha=kx)
    ok = appear(t, M[1] + 1.4, 0.45)
    if ok > 0:
        card(d, (40, 880, 1040, 1260), fill=A((220, 252, 231), ok), outline=A(GREEN, ok), w=5)
        text(d, (W / 2, 950), "✓ Thép cũng dẻo khi quá giới hạn", 46, GREEN, alpha=ok)
        mini(d, 150, 1100, L_DU, ok, ghost=L0)
        text(d, (150 + L_DU * PX + 30, 1100), "dư 2,5 cm", 44, RED, anchor="lm", alpha=ok)

# ---------------- canh 5: chot ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    def body(d, t, k):
        kd = appear(t, M[0] + 0.9, 0.5) * k
        if kd > 0:
            x0, y = 200, 1060
            text(d, (W / 2, 955), "chưa kéo: 4,0 cm", 44, NOTE, alpha=kd)
            d.rounded_rectangle([x0 - 28, y - 50, x0 - 2, y + 50], radius=6, fill=A((150, 155, 172), kd))
            spring_at(d, x0, x0 + L0 * PX, y, alpha=kd)
            xe = x0 + L0 * PX
            arrow(d, (xe, y), (xe + 230, y), A(RED, kd), w=8, head=26)
            text(d, (xe + 250, y), "2,5 N", 46, RED, anchor="lm", alpha=kd)
        kh = appear(t, M[0] + 2.8, 0.5) * k
        if kh > 0:
            card(d, (110, 1180, 970, 1400), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
            text(d, (W / 2, 1230), "Gợi ý", 42, NOTE, alpha=kh)
            ctext(d, 1320, "Còn trong giới hạn đàn hồi?", 46, (176, 64, 8), maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Quá giới hạn: thôi lực không về",
             "Lò xo mới cùng loại, kéo 2,5 N: dài bao nhiêu?", body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    P = plan(do)
    return ([(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding")]
            + [(do["t0"] + c, "tap") for a_, b_, c, e_ in P]
            + [(do["t0"] + t_dapan(do), "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"),
               (b["t0"] + b["M"][1] + 0.2, "buzz"), (b["t0"] + b["M"][1] + 1.4, "ding"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l10-biendang-01", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Biến dạng của vật rắn · thachlab.id.vn", scenes=[
 dict(key="hook", title="Lò xo bút bi trên thước", draw=s_hook, tail=0.3, caps=[
   ("Đọc trên thước.", 2.8),
   ("Nghĩ trước khi xem tiếp.", 5.4)]),
 dict(key="do", title="Kéo rồi thả", draw=s_do, tail=2.0, caps=[
   ("Kéo nhẹ 1 N rồi thả.", 3.2),
   ("Kéo 3 N rồi thả.", 3.2),
   ("Kéo mạnh 6 N rồi thả.", 3.9)]),
 dict(key="rut", title="Hai kết cục", draw=s_rut, tail=0.5, caps=[
   ("So với chiều dài lúc đầu.", 4.0),
   ("Còn bỏ ngỏ.", 4.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.6, caps=[
   ("Đúng hay sai?", 4.0),
   ("Nhìn lại lò xo thép.", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 8.2)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
