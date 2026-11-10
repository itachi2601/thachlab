# Clip: tn-l11-baitapdaodong-03 - Quay cham con lac lo xo: dem khung doan O -> 2 cm va 2 -> 4 cm
#       (31/10/2026, chang B L11 Dao dong)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-baitapdaodong-03.json:
#   tham_so: T = 0,8 s (0,4-2), A = 4,0 cm (2-8), fps = 240 khung/s ; mo_hinh x = A.sin(wt) tu luc qua O,
#   t(O->A/2) = T/12, t(A/2->A) = T/6, n = t.fps ; so_lieu_mau (lan, O->2, 2->4): 1 16 32 ; 2 17 31 ; 3 16 33.
#   goi_y_mo_phong: cung 30 do va 60 do tren vong tron pha ; hien_tuong_hay_sai[0]: "nua duong = nua thoi gian T/8".
#   Lan 1 = dung mo hinh (16 va 32 khung) nen hoat canh chay theo mo hinh: khung n -> x = 4 sin(pi n / 96).
#   Phat lai tung khung, moi khung 0,1 s video: 240 khung/s that -> 10 khung/s video = quay cham x24.
#   Cau chot: T = 1,0 s (trong khoang tham_so, chua tung hien), O -> 2 cm mat bao nhieu khung? (T/12 . 240 = 20 khung,
#   khong hien; phan xa sai: 16 nhu clip). Goi y khong noi cach giai.
# Dan canh (khac motadddh1: khong thuoc + vet cam + bang 4 moc): TRUC CHINH la hai thanh dem khung (bar chart song)
#   + vet chop (cham cach deu thoi gian) tren ray co bang dinh O / 2 cm / 4 cm ; Dap an dung vong tron pha 30/60 do.
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh -> Dap an + Rut ra + Chua noi duoc -> Bay -> Chot + cau hoi.
from engine import *

AMP, PER, FPSC = 4.0, 0.8, 240                      # tham_so A (cm), T (s), fps
ROWS = [(1, 16, 32), (2, 17, 31), (3, 16, 33)]       # so_lieu_mau
N1, N2 = 16, 32                                      # lan 1 (= mo hinh)
def xn(n): return AMP * math.sin(2 * math.pi * n / (PER * FPSC))    # li do o khung n (tinh tu luc qua O)

# ---------------- ray + lo xo + vat (khung nguon 1080x1920) ----------------
OX, S = 300, 120                      # O o x = 300 px ; 1 cm = 120 px -> 4 cm o 780 px
WALL = 70
BH, BW = 90, 100
YB = 560                              # day vat = mat ray
TAPE = YELLOW
def px(xcm): return OX + xcm * S

def spring(d, x0, x1, y, col, n=12, amp=22, w=5):
    lead = 18; pts = [(x0, y), (x0 + lead, y)]
    L = (x1 - lead) - (x0 + lead)
    for i in range(1, 2 * n):
        pts.append((x0 + lead + L * i / (2 * n), y + (amp if i % 2 else -amp)))
    pts += [(x1 - lead, y), (x1, y)]
    d.line(pts, fill=col, width=w, joint="curve")

def rig(d, yb, xcm, a=1.0, labs=True, hi=None):
    """Tuong trai, ray, 3 bang dinh (O, 2 cm, 4 cm), lo xo, vat tam o x cm. hi = chi so bang dinh dang loe sang."""
    c = lambda col: A(col, a)
    d.rectangle([WALL - 30, yb - 150, WALL, yb + 30], fill=c((205, 200, 190)), outline=c(NAVY), width=3)
    for k in range(7):
        yy = yb - 140 + k * 26; d.line([(WALL - 30, yy + 18), (WALL - 8, yy)], fill=c(NAVY), width=2)
    d.rectangle([WALL, yb, 1000, yb + 20], fill=c((190, 195, 210)), outline=c(NAVY), width=3)
    for i, (xc, lab) in enumerate(((0, "O"), (2, "2 cm"), (4, "4 cm"))):
        col = ORANGE if hi == i else TAPE
        d.rectangle([px(xc) - 9, yb - 2, px(xc) + 9, yb + 22], fill=c(col), outline=c(NAVY), width=2)
        if labs: text(d, (px(xc), yb + 62), lab, 42, INK, alpha=a)
    cx = px(xcm)
    spring(d, WALL, cx - BW / 2, yb - BH / 2, c(NAVY))
    card(d, (cx - BW / 2, yb - BH, cx + BW / 2, yb), fill=c(BLUE), outline=c(NAVY), r=12, w=4)
    d.line([(cx, yb - BH + 14), (cx, yb - 14)], fill=c(WHITE), width=4)          # vach giua vat (de doi bang dinh)

def pill(d, cx, cy, s, size, fg, bg, a=1.0):
    pw = tw(d, s, F(size)) + 52
    card(d, (cx - pw / 2, cy - size * 0.85, cx + pw / 2, cy + size * 0.85), fill=A(bg, a), r=int(size * 0.85))
    text(d, (cx, cy), s, size, fg, alpha=a)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    k = ease((t - 1.0) / 1.4)                  # keo vat tu O ra +4 cm, giu yen
    rig(d, YB, AMP * k)
    kp = appear(t, 0.3, 0.4)
    pill(d, W / 2, 330, "điện thoại quay 240 khung/s", 40, WHITE, NAVY, kp)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 760 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 640), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 60, "DỰ ĐOÁN", 40, WHITE, PURPLE, a)
    ctext(d, y0 + 180, "Thả tay, bỏ qua ma sát.", 44, MUTED, maxw=920, alpha=a)
    ctext(d, y0 + 380, "Đoạn O → 2 cm và đoạn 2 → 4 cm:\nđoạn nào có nhiều khung hơn?", 52, INK, maxw=930, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 570, 940, y0 + 582], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 570, 140 + 800 * (1 - p), y0 + 582], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (phat lai tung khung) ----------------
REL, STEP = 1.2, 0.1                  # bat dau phat lai o giay 1,2 ; moi khung 0,1 s video (quay cham x24)
T_ROW = [REL + (N1 + N2) * STEP + 0.5, None, None]
T_ROW[1] = T_ROW[0] + 0.8; T_ROW[2] = T_ROW[1] + 0.8
PXF = 15                              # 1 khung = 15 px tren thanh dem
BX = 330                              # goc trai hai thanh dem
YTR = 690                             # duong vet chop

def nof(v):
    """So khung da phat (0..48) o giay v cua canh Tien hanh."""
    if v < REL: return 0
    return min(N1 + N2, int((v - REL) / STEP + 1e-9))

def strobe(d, n, a=1.0):
    """Vet chop: moi 4 khung mot cham o vi tri vat -> cham thua gan O, day gan bien. Khong ghi so."""
    d.line([(px(0), YTR), (px(AMP), YTR)], fill=A(GRAY, a), width=3)
    for m in range(0, n + 1, 4):
        dot(d, px(xn(m)), YTR, 11, A(PURPLE, a), outline=A(WHITE, a))

def bars(d, c1, c2, y1=1010, y2=1110, a=1.0, final=False):
    for y, lab, c, col, cmax in ((y1, "O → 2 cm", c1, GREEN, N1), (y2, "2 → 4 cm", c2, ORANGE, N2)):
        text(d, (60, y), lab, 42, INK, anchor="lm", alpha=a)
        d.rounded_rectangle([BX, y - 26, BX + PXF * cmax, y + 26], radius=10, outline=A(LIGHT, a), width=3)
        if c > 0: d.rounded_rectangle([BX, y - 26, BX + PXF * c, y + 26], radius=10, fill=A(col, a))
        if c > 0 or final: text(d, (BX + PXF * c + 18, y), f"{c} khung", 42, col, anchor="lm", alpha=a)

def table(d, rows, y0=1210, a=1.0):
    card(d, (60, y0, 1020, y0 + 330), fill=A(WHITE, a), outline=A(NAVY, a), r=24, w=4)
    xs = (190, 520, 850)
    for x, h in zip(xs, ("Lần", "O → 2 cm", "2 → 4 cm")): text(d, (x, y0 + 52), h, 42, NAVY, alpha=a)
    d.line([(80, y0 + 92), (1000, y0 + 92)], fill=A(NAVY, a), width=3)
    for i in range(rows):
        y = y0 + 140 + i * 72
        lan, a1, a2 = ROWS[i]
        text(d, (xs[0], y), str(lan), 44, INK, alpha=a)
        text(d, (xs[1], y), f"{a1} khung", 44, GREEN, alpha=a)
        text(d, (xs[2], y), f"{a2} khung", 44, ORANGE, alpha=a)

def s_do(img, d, t, sc):
    n = nof(t)
    hi = 1 if (N1 <= n < N1 + 4 and t >= REL) else (2 if n >= N1 + N2 else None)
    pill(d, W / 2, 330, "quay chậm 240 khung/s", 40, WHITE, ORANGE)
    rig(d, YB, xn(n), hi=hi)
    if t >= REL: strobe(d, n)
    text(d, (W / 2, 770), "chấm tím: cách đều thời gian", 40, PURPLE, alpha=appear(t, REL + 1.0, 0.4))
    bars(d, min(n, N1), max(0, n - N1))
    rows = sum(1 for tr in T_ROW if t >= tr)
    if rows: table(d, rows)

# ---------------- canh 3: Dap an + Rut ra + Chua noi duoc ----------------
CX, CY, R = 300, 680, 200             # vong tron pha ; truc x di qua tam, O o CX, 2 cm o CX + R/2, 4 cm o CX + R
def arc_pts(a0, a1, r, k=1.0):
    """Cung tu goc a0 toi a0 + (a1 - a0) k (do, goc toan hoc, nguoc kim dong ho)."""
    m = max(2, int(abs(a1 - a0) * k / 3) + 2)
    return [(CX + r * math.cos(math.radians(a0 + (a1 - a0) * k * i / (m - 1))),
             CY - r * math.sin(math.radians(a0 + (a1 - a0) * k * i / (m - 1)))) for i in range(m)]

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    pill(d, W / 2, 330, "ĐÁP ÁN · đoạn 2 → 4 cm lâu hơn", 40, WHITE, NAVY, ka)
    # vong tron pha (M quay nguoc kim dong ho; qua O theo chieu duong: M o day vong, goc -90 do)
    d.ellipse([CX - R, CY - R, CX + R, CY + R], outline=GRAY, width=4)
    d.line([(CX - R - 30, CY), (CX + R + 40, CY)], fill=NAVY, width=3)
    for xc, lab in ((0, "O"), (R / 2, "2"), (R, "4 cm")):
        d.line([(CX + xc, CY - 12), (CX + xc, CY + 12)], fill=NAVY, width=3)
        text(d, (CX + xc + (70 if lab == "4 cm" else 0), CY - 46), lab, 44, INK)
    k1 = clamp((t - 0.6) / 0.9); k2 = clamp((t - 1.6) / 1.4)
    if k1 > 0: d.line(arc_pts(-90, -60, R, k1), fill=GREEN, width=12, joint="curve")
    if k2 > 0: d.line(arc_pts(-60, 0, R, k2), fill=ORANGE, width=12, joint="curve")
    ang = -90 + 30 * k1 + 60 * k2
    mx, my = CX + R * math.cos(math.radians(ang)), CY - R * math.sin(math.radians(ang))
    d.line([(mx, my), (mx, CY)], fill=A(PURPLE, 0.8), width=3)
    dot(d, mx, my, 13, PURPLE, outline=WHITE); dot(d, mx, CY, 9, BLUE)
    for a0, lab, col, at in ((-75, "30°", GREEN, 1.4), (-30, "60°", ORANGE, 3.0)):
        r2 = R + 56
        text(d, (CX + r2 * math.cos(math.radians(a0)), CY - r2 * math.sin(math.radians(a0))), lab, 44, col,
             alpha=appear(t, at, 0.4))
    # cot phai: so khung lan 1 va phan chu ki
    kg = appear(t, 1.4, 0.4); ko = appear(t, 3.0, 0.4)
    text(d, (820, 560), "16 khung", 46, GREEN, alpha=kg); text(d, (820, 620), "≈ T/12", 46, GREEN, alpha=kg)
    text(d, (820, 740), "32 khung", 46, ORANGE, alpha=ko); text(d, (820, 800), "≈ T/6", 46, ORANGE, alpha=ko)
    kr = appear(t, M[0] + 0.6, 0.45)
    if kr > 0:
        card(d, (60, 960, 1020, 1140), fill=A((236, 253, 243), kr), outline=A(GREEN, kr), r=24, w=4)
        ctext(d, 1050, "Gần biên, vật đi chậm", 52, (21, 110, 55), maxw=900, alpha=kr)
    kn = appear(t, M[1] - 0.05, 0.45)
    if kn > 0:
        card(d, (60, 1190, 1020, 1470), fill=A(WHITE, kn), outline=A(NAVY, kn), r=24, w=5)
        text(d, (W / 2, 1245), "Chưa nói được", 46, NAVY, alpha=kn)
        for j, l in enumerate(("• Biên độ lớn: lò xo còn đàn hồi?", "• Ray có ma sát?")):
            text(d, (100, 1325 + j * 80), l, 44, INK, anchor="lm", alpha=kn * appear(t, M[1] + 0.3 + 0.5 * j, 0.4))

# ---------------- canh 4: Bay - nua duong = nua thoi gian ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    y0 = 300
    card(d, (40, y0, 1040, y0 + 420), fill=WHITE, outline=(185, 28, 28), w=6)
    pill(d, W / 2, y0 + 62, "BẪY", 40, WHITE, (185, 28, 28))
    q = "“Nửa đường thì nửa thời gian”"
    yy = y0 + 190; f = F(48); lw = tw(d, q, f)
    text(d, (W / 2, yy), q, 48, (185, 28, 28))
    ctext(d, y0 + 300, "→ mỗi đoạn T/8", 46, (185, 28, 28))
    ks = clamp((t - (M[1] + 2.0)) / 0.4)
    if ks > 0:
        for y_ in (yy + 2, y0 + 302):
            d.line([(W / 2 - lw / 2 - 6, y_), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, y_)], fill=(140, 15, 15), width=7)
    # hai cach chia: "nghi" (hai thanh bang nhau) va "that" (16 / 32 khung) - cung thang 15 px/khung, tong T/4
    yN, yT = 900, 1190
    text(d, (60, yN - 80), "Nghĩ:", 44, (185, 28, 28), anchor="lm")
    half = PXF * (N1 + N2) / 2
    for i, col in ((0, (185, 28, 28)), (1, (185, 28, 28))):
        x0 = 120 + i * half
        d.rounded_rectangle([x0, yN - 26, x0 + half - 6, yN + 26], radius=10, outline=col, width=4)
        text(d, (x0 + half / 2, yN), "T/8", 44, col)
    kt = appear(t, M[1] + 2.0, 0.4)
    text(d, (60, yT - 80), "✓ Thật:", 44, (21, 110, 55), anchor="lm", alpha=kt)
    if kt > 0:
        d.rounded_rectangle([120, yT - 26, 120 + PXF * N1 - 6, yT + 26], radius=10, fill=A(GREEN, kt))
        d.rounded_rectangle([120 + PXF * N1, yT - 26, 120 + PXF * (N1 + N2), yT + 26], radius=10, fill=A(ORANGE, kt))
        text(d, (120 + PXF * N1 / 2, yT + 66), "T/12", 44, GREEN, alpha=kt)
        text(d, (120 + PXF * (N1 + N2 / 2), yT + 66), "T/6", 44, ORANGE, alpha=kt)
    kc = appear(t, M[1] + 2.4, 0.5)
    ctext(d, 1430, "Gần O vật nhanh, gần biên vật chậm", 44, (21, 110, 55), maxw=940, alpha=kc)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 290, 1020, 510), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 400, "Thời gian theo góc quét,\nkhông theo quãng đường", 48, GREEN, maxw=900, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 570, 1040, 1520), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 600, W / 2 + pw / 2, 664), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 632), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 790, "Con lắc khác: T = 1,0 s, A = 4 cm,\nvẫn 240 khung/s. Đoạn O → 2 cm\nmất mấy khung?",
          46, INK, maxw=930, alpha=appear(t, M[0] + 0.4, 0.5))
    # hinh nho: ray voi bang dinh, thanh dem doan O -> 2 cm de trong "?"
    yb = 1060
    rig(d, yb, 0.0, a=k1)
    d.rounded_rectangle([px(0), yb + 110, px(2), yb + 160], radius=10, outline=A(GREEN, k1), width=4)
    text(d, (px(1), yb + 135), "? khung", 42, GREEN, alpha=k1)
    kh = appear(t, M[0] + 0.4 + 2.5, 0.5)
    if kh > 0:
        card(d, (110, 1300, 970, 1490), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1350), "Gợi ý", 40, INK, alpha=kh)
        text(d, (W / 2, 1430), "Nhìn lại vòng tròn pha", 44, ORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open")]            # K9: khong co tieng nao sat diem dung cuoi hook
    out += [(do["t0"] + REL, "tap"), (do["t0"] + REL + N1 * STEP, "tap"), (do["t0"] + REL + (N1 + N2) * STEP, "tap")]
    out += [(do["t0"] + tr, "tick") for tr in T_ROW]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-baitapdaodong-03", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Bài tập dao động · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Quay chậm rồi đếm khung", draw=s_hook, tail=0.6, caps=[
   ("Dán băng dính ở O, 2 cm, 4 cm.", 3.4),
   ("Tự đoán trước khi xem tiếp.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Tua tới lúc vật qua O, đếm khung.", 5.6),
   ("Làm ba lần, ghi vào bảng.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Cùng 2 cm, góc quét khác nhau.", 5.0),
   ("Mới thử một biên độ, một chu kì.", 5.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.6, caps=[
   ("Bẫy: chia đôi thời gian?", 3.0),
   ("Có đúng không?", 4.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.1, caps=[
   ("Dừng video, tự trả lời.", 7.2)]),
])
