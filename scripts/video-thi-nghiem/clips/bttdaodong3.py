# Clip: tn-l11-baitapdaodong-03 - Quay cham con lac lo xo: dem khung doan O -> A/2
#       (31/10/2026, chang B L11 Dao dong; dung lai 27/11/2026 theo cong moi: --do-chu 0 LOI, chu >= 55 px,
#       Du doan K10, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-baitapdaodong-03.json (_kiem_so() doi chieu):
#   tham_so: T = 0,8 s (0,4-2), A = 4,0 cm (2-8), fps = 240 khung/s ; mo_hinh x = A.sin(wt) tu luc qua O,
#   t(O->A/2) = T/12, t(A/2->A) = T/6, n = t.fps ; so_lieu_mau lan 1: 16 / 32 khung (= mo hinh).
# DOI CA Du doan (27/11): ca cu "doan nao nhieu khung hon" da co dap so trong hop exp ngay tren video (16 / 32 khung).
#   Ca moi: tha tu 8 cm (A max tham_so, T giu 0,8 s) -> doan O -> 4 cm (nua duong) so khung so voi tha tu 4 cm
#   doan O -> 2 cm? Dap: BANG NHAU (T/12 khong phu thuoc A; so 16 khung cho A = 8 cm suy tu mo hinh, ghi "theo mo hinh").
# Bay = hien_tuong_hay_sai[0]: nua duong = nua thoi gian (T/8).
# Thu nghi (= cau_chot khung web): T = 1,0 s, A = 4 cm, 240 khung/s -> doan 2 -> 4 cm mat may khung?
#   T/6 . 240 = 40 khung (buoc chua chieu: goc 60 do = 90 - 30). Nhieu: 20 (T/12), 30 (T/8), 32 (chep so clip).
from engine import *

AMP, AMP2, PER, FPSC = 4.0, 8.0, 0.8, 240            # tham_so A (cm), A max, T (s), fps
N1, N2 = 16, 32                                      # so_lieu_mau lan 1 (= mo hinh)
DGREEN = (21, 110, 55); DRED = (185, 28, 28); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-baitapdaodong-03.json")))
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["T"]["mac_dinh"] == PER and ts["A"]["mac_dinh"] == AMP and ts["A"]["max"] == AMP2
    assert ts["fps"]["gia_tri"] == FPSC and ts["T"]["min"] <= 1.0 <= ts["T"]["max"]
    assert k["so_lieu_mau"]["hang"][0] == [1, N1, N2]
    assert round(PER / 12 * FPSC) == N1 and round(PER / 6 * FPSC) == N2
_kiem_so()

def xn(n, amp): return amp * math.sin(2 * math.pi * n / (PER * FPSC))    # li do o khung n (tinh tu luc qua O)

# ---------------- ray + lo xo + vat (khung nguon 1080x1920) ----------------
OX, S = 540, 52                       # O giua ray ; 1 cm = 52 px -> +-8 cm o 124..956 px
WALL = 70
BH, BW = 90, 90
def px(xcm): return OX + xcm * S

def spring(d, x0, x1, y, col, n=12, amp=22, w=5):
    lead = 18; pts = [(x0, y), (x0 + lead, y)]
    L = (x1 - lead) - (x0 + lead)
    for i in range(1, 2 * n):
        pts.append((x0 + lead + L * i / (2 * n), y + (amp if i % 2 else -amp)))
    pts += [(x1 - lead, y), (x1, y)]
    d.line(pts, fill=col, width=w, joint="curve")

def rig(d, yb, xcm, marks=(0, 2, 4, 8), a=1.0, hi=()):
    """Tuong trai, ray, bang dinh o cac moc (cm), lo xo, vat tam o x cm. hi = cac moc loe cam."""
    c = lambda col: A(col, a)
    d.rectangle([WALL - 30, yb - 150, WALL, yb + 30], fill=c((205, 200, 190)), outline=c(NAVY), width=3)
    for k in range(7):
        yy = yb - 140 + k * 26; d.line([(WALL - 30, yy + 18), (WALL - 8, yy)], fill=c(NAVY), width=2)
    d.rectangle([WALL, yb, 1010, yb + 20], fill=c((190, 195, 210)), outline=c(NAVY), width=3)
    for xc in marks:
        col = ORANGE if xc in hi else YELLOW
        d.rectangle([px(xc) - 10, yb - 2, px(xc) + 10, yb + 22], fill=c(col), outline=c(NAVY), width=2)
        text(d, (px(xc), yb + 66), "O" if xc == 0 else str(int(xc)), 56, INK, alpha=a)
    text(d, (1062, yb + 66), "cm", 56, INK, anchor="rm", alpha=a)
    cx = px(xcm)
    spring(d, WALL, cx - BW / 2, yb - BH / 2, c(NAVY))
    card(d, (cx - BW / 2, yb - BH, cx + BW / 2, yb), fill=c(BLUE), outline=c(NAVY), r=12, w=4)
    d.line([(cx, yb - BH + 14), (cx, yb - 14)], fill=c(WHITE), width=4)

def pill(d, cx, cy, s, size, fg, bg, a=1.0):
    pw = tw(d, s, F(size)) + 52
    card(d, (cx - pw / 2, cy - size * 0.8, cx + pw / 2, cy + size * 0.8), fill=A(bg, a), r=int(size * 0.8))
    text(d, (cx, cy), s, size, fg, alpha=a)

def seg_bar(d, y, t, t0, t1, col, a=1.0, n=6):
    """Thanh dem lien khoi, tat lan luot tu PHAI sang TRAI; cao 76 px."""
    p = clamp((t - t0) / (t1 - t0)); on = n - int(p * n + 1e-9); wseg = 820 / n
    for i in range(n):
        x = 130 + i * wseg
        if i < on: card(d, (x, y, x + wseg - 14, y + 76), fill=A(col, a), r=16)
        else: card(d, (x, y, x + wseg - 14, y + 76), fill=A(WHITE, a), outline=A(EMPTY, a), r=16, w=4)

def osc(t, amp, t0=0.0, slow=24.0):
    """Vat dao dong quay cham xN tu luc t0 (qua O theo chieu duong)."""
    if t < t0: return 0.0
    return amp * math.sin(2 * math.pi * (t - t0) / (PER * slow))

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
YB = 560
def s_hook(img, d, t, sc):
    M = sc["M"]
    k = ease((t - 0.8) / 1.4)                  # keo vat tu O ra +8 cm, giu yen
    rig(d, YB, AMP2 * k)
    pill(d, W / 2, 320, "quay chậm 240 khung/s", 56, WHITE, NAVY)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 780 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 690), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 64, "DỰ ĐOÁN", 56, WHITE, PURPLE, a)
    text(d, (W / 2, y0 + 180), "Thả từ 4 cm: đếm O → 2 cm.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 265), "Thả từ 8 cm: đếm O → 4 cm.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 370), "Số khung lần sau", 62, PURPLE, alpha=a)
    text(d, (W / 2, y0 + 450), "so với lần đầu?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 560, t, M[1] + 0.4, sc["T"] - 0.2, PURPLE, a)

# ---------------- canh 2: Tien hanh - hai lan tha, dem khung ----------------
STEP = 0.1                            # moi khung 0,1 s video (quay cham x24)
R1, R2 = 0.4, None                    # lan 1 bat dau ; lan 2 = M[1] + 0.2
PXF = 30; BX = 110
def s_do(img, d, t, sc):
    M = sc["M"]; r2 = M[1] + 0.2
    two = t >= r2 - 0.4
    amp = AMP2 if two else AMP
    tt0 = r2 if two else R1
    n = 0 if t < tt0 else min(N1, int((t - tt0) / STEP + 1e-9))
    if t < tt0: x = 0.0
    elif n < N1: x = xn((t - tt0) / STEP, amp)
    else: x = osc(t, amp, tt0, 24.0)                  # dem xong van chay cham (khong dung hinh)
    rig(d, YB, x, hi=((0, amp / 2) if n < N1 or t < tt0 else ()))
    pill(d, W / 2, 320, "thả từ 8 cm" if two else "thả từ 4 cm", 56, WHITE, ORANGE if two else TEAL)
    c1 = min(N1, max(0, int((t - R1) / STEP + 1e-9))) if t >= R1 else 0
    c2 = n if two else 0
    for y, lab, c, col in ((900, "Thả 4 cm · O → 2 cm", c1, TEAL), (1130, "Thả 8 cm · O → 4 cm", c2, ORANGE)):
        text(d, (BX, y), lab, 58, INK, anchor="lm")
        d.rounded_rectangle([BX, y + 50, BX + PXF * N1, y + 120], radius=12, outline=GRAY, width=3)
        if c > 0: d.rounded_rectangle([BX, y + 50, BX + PXF * c, y + 120], radius=12, fill=col)
        text(d, (BX + PXF * N1 + 30, y + 85), f"{c} khung", 58, col if c else INK, anchor="lm")
    kt = appear(t, r2 + N1 * STEP + 0.6, 0.4)
    if kt > 0:
        text(d, (W / 2, 1390), "lần 2: theo mô hình", 56, NAVY, alpha=kt)

# ---------------- canh 3: Ket qua (vong tron pha) + rut ra + chua noi duoc ----------------
CX, CY = 300, 640
def arc_pts(a0, a1, r, k=1.0):
    m = max(2, int(abs(a1 - a0) * k / 3) + 2)
    return [(CX + r * math.cos(math.radians(a0 + (a1 - a0) * k * i / (m - 1))),
             CY - r * math.sin(math.radians(a0 + (a1 - a0) * k * i / (m - 1)))) for i in range(m)]

def s_dapan(img, d, t, sc):
    M = sc["M"]
    for r, col in ((110, TEAL), (220, ORANGE)):
        d.ellipse([CX - r, CY - r, CX + r, CY + r], outline=GRAY, width=4)
    d.line([(CX - 250, CY), (CX + 260, CY)], fill=NAVY, width=3)
    k1 = clamp((t - 0.4) / 1.6)                         # M quay tu day vong (qua O) 30 do, lap lai cham
    loop = ((t - 0.4) % 3.2) / 3.2 if t > 2.0 else k1
    for r, col in ((110, TEAL), (220, ORANGE)):
        d.line(arc_pts(-90, -60, r, k1), fill=col, width=20, joint="curve")
        ang = -90 + 30 * loop
        mx, my = CX + r * math.cos(math.radians(ang)), CY - r * math.sin(math.radians(ang))
        d.line([(mx, my), (mx, CY)], fill=PURPLE, width=3)
        dot(d, mx, my, 14, col, outline=WHITE)
    for xc, lab in ((0, "O"), (55, "2"), (110, "4"), (220, "8")):
        d.line([(CX + xc, CY - 12), (CX + xc, CY + 12)], fill=NAVY, width=3)
    text(d, (CX + 285, CY - 48), "8 cm", 56, INK); text(d, (CX + 115, CY - 48), "4 cm", 56, INK)
    kg = appear(t, 1.8, 0.4)
    text(d, (800, 560), "cùng 30°", 60, PURPLE, alpha=kg)
    text(d, (800, 650), "16 khung", 60, TEAL, alpha=kg)
    text(d, (800, 730), "16 khung", 60, ORANGE, alpha=kg)
    kr = appear(t, M[1] - 0.05, 0.45)
    if kr > 0:
        card(d, (60, 920, 1020, 1090), fill=A((236, 253, 243), kr), outline=A(GREEN, kr), r=24, w=5)
        text(d, (W / 2, 1005), "Bằng nhau: đều T/12", 62, DGREEN, alpha=kr)
    kn = appear(t, M[2] - 0.05, 0.45)
    if kn > 0:
        card(d, (60, 1130, 1020, 1440), fill=A(WHITE, kn), outline=A(NAVY, kn), r=24, w=5)
        text(d, (W / 2, 1190), "Chưa nói được", 60, NAVY, alpha=kn)
        text(d, (100, 1280), "• Kéo 8 cm: lò xo còn tốt?", 58, INK, anchor="lm", alpha=kn)
        text(d, (100, 1370), "• Ma sát trên ray: bỏ qua", 58, INK, anchor="lm", alpha=appear(t, M[2] + 2.5, 0.4))

# ---------------- canh 4: Bay - nua duong = nua thoi gian ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    xr = osc(t, AMP, 0.0, 12.0)                          # vat chay cham x12 tren ray nho (khong dung hinh)
    rig(d, 470, xr, marks=(0, 2, 4))
    yN, yT = 760, 1060; half = PXF * (N1 + N2) / 2 * 0.62
    card(d, (40, yN - 90, 1040, yN + 170), fill=(254, 242, 242), outline=DRED, r=24, w=5)
    text(d, (80, yN - 30), "✗ Nửa đường, nửa thời gian", 58, DRED, anchor="lm")
    for i in range(2):
        x0 = 110 + i * half
        d.rounded_rectangle([x0, yN + 40, x0 + half - 8, yN + 120], radius=12, outline=DRED, width=5)
        text(d, (x0 + half / 2, yN + 80), "T/8", 58, DRED)
    kt = appear(t, M[1] - 0.1, 0.4)                      # nhip 2 cach nhip 1 >= 3 s
    if kt > 0:
        card(d, (40, yT - 90, 1040, yT + 230), fill=A((236, 253, 243), kt), outline=A(GREEN, kt), r=24, w=5)
        text(d, (80, yT - 30), "✓ Thật: gần biên đi chậm", 58, DGREEN, anchor="lm", alpha=kt)
        u = 2 * half / (N1 + N2)
        d.rounded_rectangle([110, yT + 40, 110 + u * N1 - 8, yT + 120], radius=12, fill=A(GREEN, kt))
        d.rounded_rectangle([110 + u * N1, yT + 40, 110 + u * (N1 + N2) - 8, yT + 120], radius=12, fill=A(ORANGE, kt))
        text(d, (110 + u * N1 / 2, yT + 175), "T/12", 58, DGREEN, alpha=kt)
        text(d, (110 + u * (N1 + N2 / 2), yT + 175), "lâu hơn", 58, DORANGE, alpha=kt)

# ---------------- canh 5: THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = 1.0 if t >= 0.15 else 0.0
    if k1 <= 0: return
    card(d, (40, 215, 1040, 1585), fill=WHITE, outline=ORANGE, w=6)
    pill(d, W / 2, 280, "THỬ NGHĨ", 56, WHITE, ORANGE)
    xr = osc(t, AMP, 0.3, 30.0)
    rig(d, 560, xr, marks=(0, 2, 4))
    d.rounded_rectangle([px(2), 700, px(4), 770], radius=12, outline=ORANGE, width=5)
    text(d, (px(3), 735), "?", 60, DORANGE)
    text(d, (W / 2, 900), "Con lắc khác: T = 1,0 s.", 60, INK)
    text(d, (W / 2, 985), "Thả từ 4 cm, 240 khung/s.", 60, INK)
    text(d, (W / 2, 1100), "Đoạn 2 → 4 cm", 64, DORANGE)
    text(d, (W / 2, 1185), "mất mấy khung?", 64, DORANGE)
    seg_bar(d, 1320, t, 0.8, sc["T"] - 0.2, ORANGE)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    r2 = do["M"][1] + 0.2
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
            (do["t0"] + R1, "tap"), (do["t0"] + R1 + N1 * STEP, "tick"),
            (do["t0"] + r2, "tap"), (do["t0"] + r2 + N1 * STEP, "tick"),
            (da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l11-baitapdaodong-03", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Bài tập dao động · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Quay chậm rồi đếm khung", draw=s_hook, tail=0.3, caps=[
   ("Đánh dấu O, 2, 4, 8 cm.", 4.4),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Thả từ 4 cm, đếm tới 2 cm.", 4.0),
   ("Thả từ 8 cm, đếm tới 4 cm.", 4.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Hai điểm cùng quay một góc.", 4.0),
   ("Biên độ gấp đôi, thời gian như cũ.", 4.4),
   ("Lần hai: số theo mô hình.", 4.6)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Bẫy: chia đôi đường, chia đôi giờ?", 3.6),
   ("Gần O nhanh, gần biên chậm.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự tính.", 6.4)]),
])
