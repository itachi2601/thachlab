# Clip: tn-l12-camungdt-03 - Tu thong qua khung quay trong tu truong deu (ban 1, 28/10/2026; dung lai 21/11/2026 theo
# KE-HOACH-CAI-TIEN-CLIP viec 4 lo 20: cong --do-chu, chu >= 55 px khi ve, K10 khong nut A-D, Bay hinh tu giai thich).
# Quan niem sai can danh (kho hien_tuong_hay_sai[0]): lay goc giua MAT khung va B thay vi goc giua PHAP TUYEN n va B.
# So lieu nguyen tu content/thi-nghiem/tn-l12-camungdt-03.json (_kiem_so() doi chieu):
#   tham_so B = 0,2 T, S = 0,05 m^2; so_lieu_mau (alpha, Phi): 0 0,01 | 30 0,00866 | 60 0,005 | 90 0 | 120 -0,005.
# Ca da co trong bai (KHONG dung lam Du doan/chot): Cau 1 (n hop B 60 do -> 5e-3; nhieu 8,7e-3 / 0 / 1e-2) va vi du
#   "mat khung hop duong suc 30 do -> alpha = 60 do".
# Du doan (khong nut, khung web hoi A-D): mat khung hop B goc 60 do -> Phi con bao nhieu phan Phi lon nhat?
#   -> C. Hon mot nua (alpha = 30 do, Phi = 0,00866 Wb). Bay "dung mot nua" = lay cos 60 do cua goc mat khung.
# Tien hanh: quay 0 -> 30 -> 60 -> 90 do (khong chieu 120 do: de danh cho cau chot), do thi truc 0..90 do.
# Bay (cap khac Du doan): mat khung song song B -> goc mat-B = 0 do, de tuong cos 0 = 1 (Phi lon nhat); that ra
#   alpha = 90 do, khong duong suc nao qua, Phi = 0. Hai buoc >= 3 s, hinh tu giai thich.
# Chot (khung web hoi A-D): quay tiep qua vi tri song song toi khi mat khung hop B goc 30 do -> alpha = 120 do,
#   Phi = -0,005 Wb (hang 5 cua kho; dap so khong hien tren man hinh, so am chua tung chieu).
from engine import *

ROWS = [(0, 0.01), (30, 0.00866), (60, 0.005), (90, 0.0)]        # so_lieu_mau hang 1-4 (chieu trong clip)
CHOT = (120, -0.005)                                             # so_lieu_mau hang 5 (cau chot, khong hien)
BB, SS = 0.2, 0.05


def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l12-camungdt-03.json")))
    hang = [tuple(r) for r in k["so_lieu_mau"]["hang"]]
    for r in ROWS + [CHOT]:
        assert any(abs(r[0] - h[0]) < 1e-9 and abs(r[1] - h[1]) < 1e-9 for h in hang), r
        assert abs(BB * SS * math.cos(math.radians(r[0])) - r[1]) < 6e-6, r
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["B"]["mac_dinh"] == BB and ts["S"]["mac_dinh"] == SS
_kiem_so()

# ---------------- bo cuc (khung 1080x1920, vung ve y 200..1690) ----------------
PX0, PY0, PX1, PY1 = 40, 236, 1040, 800           # khung hinh tu truong
CX, CY, HL = 540, 520, 190                        # tam truc quay, nua chieu dai khung (nhin canh)
LX0, LX1 = 132, 948                               # duong suc tu mat cuc N toi mat cuc S
LINES = [300 + i * 55 for i in range(9)]          # 9 duong suc cach deu (co duong y = 520 qua truc)
COPPER = (184, 115, 51); LINEC = (130, 150, 195); DGREEN = (10, 110, 50); DRED = (185, 28, 28)
DPURPLE = (109, 40, 217); EMPTY = (148, 140, 128)
PMAX = 0.0115


def fphi(p):
    if p == 0: return "0"
    return repr(p).replace(".", ",").replace("-", "−")


def phi_model(a): return BB * SS * math.cos(math.radians(a))


def chevron(d, x, y, ang, color, s=16, w=4):
    for sg in (1, -1):
        a = ang + math.pi - sg * math.radians(30)
        d.line([(x, y), (x + s * math.cos(a), y + s * math.sin(a))], fill=color, width=w)


def dashed(d, p1, p2, color, w=3, dash=12, gap=9):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))],
               fill=color, width=w)


def tag(d, x, y, s, size, color, alpha=1.0, anchor="m"):
    wd = tw(d, s, F(size)) + 24
    x0 = x - wd / 2 if anchor == "m" else x
    d.rounded_rectangle([x0, y - size * 0.64, x0 + wd, y + size * 0.64], radius=12, fill=A(WHITE, 0.94 * alpha))
    text(d, (x0 + wd / 2, y), s, size, color, alpha=alpha)


def seg_bar(d, y, t, t0, t1, col, a=1.0):
    """Thanh dem 5 o cao 70 px, tat lan luot tu PHAI sang TRAI."""
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 190 + i * 145
        if i < on: card(d, (x, y, x + 120, y + 70), fill=A(col, a), r=16)
        else: card(d, (x, y, x + 120, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=16, w=4)


# ---------------- hinh tu truong + khung (nhin doc truc quay) ----------------
def field_panel(d, a, band=False, show_n=True, a_arc=False, a_lab=None, m_arc=False, m_lab=None, wires=False, alpha_k=1.0):
    """a = goc phap tuyen n voi B (do). band: to cac duong suc xuyen qua khung. a_arc: cung goc n-B (xanh);
    m_arc: cung goc giua MAT khung va B (tim)."""
    card(d, (PX0, PY0, PX1, PY1), fill=WHITE, outline=LIGHT, w=3)
    c = math.cos(math.radians(a)); s = math.sin(math.radians(a)); half = HL * abs(c)
    for y in LINES:
        inside = band and half > 1 and abs(y - CY) < half - 0.5
        col = ORANGE if inside else LINEC
        d.line([(LX0, y), (LX1, y)], fill=col, width=6 if inside else 3)
        for x in (290, 790): chevron(d, x, y, 0, col)
    d.rounded_rectangle([60, 284, LX0, 756], radius=10, fill=RED)
    d.rounded_rectangle([LX1, 284, 1020, 756], radius=10, fill=BLUE)
    text(d, (96, 520), "N", 58, WHITE); text(d, (984, 520), "S", 58, WHITE)
    arrow(d, (150, 262), (250, 262), BLUE, w=5, head=18)
    text(d, (268, 262), "B", 58, BLUE, anchor="lm")
    if wires:                                       # day noi tu truc khung xuong dien ke
        for dx in (0, 14):
            d.line([(CX + dx, CY), (CX + dx, 790), (860 + dx, 790), (860 + dx, 830)], fill=(90, 96, 112), width=3)
    p1 = (CX - HL * s, CY - HL * c); p2 = (CX + HL * s, CY + HL * c)
    d.line([p1, p2], fill=COPPER, width=16)
    for p in (p1, p2): dot(d, p[0], p[1], 10, COPPER)
    dot(d, CX, CY, 9, NAVY, outline=WHITE)
    if m_arc:                                       # goc giua mat khung (nua p2 hoac p1 nam gan +x) va B
        ang = math.degrees(math.atan2(p2[1] - CY, p2[0] - CX))       # goc ve (do, chieu kim dong ho)
        if p2[0] < CX: ang = math.degrees(math.atan2(p1[1] - CY, p1[0] - CX))
        lo, hi = (ang, 0) if ang < 0 else (0, ang)
        if abs(ang) > 1:
            d.arc([CX - 112, CY - 112, CX + 112, CY + 112], lo % 360 if lo < 0 else lo, hi, fill=DPURPLE, width=6)
        if m_lab:
            mid = math.radians(ang / 2)
            tag(d, CX + 262 * math.cos(mid), CY + 262 * math.sin(mid) + (8 if ang >= 0 else -8), m_lab, 56, DPURPLE,
                alpha=alpha_k)
    if show_n:
        tip = (CX + 150 * c, CY - 150 * s)
        arrow(d, (CX, CY), tip, GREEN, w=7, head=22)
        tag(d, CX + 192 * c - 36 * s, CY - 192 * s - 36 * c, "n", 56, DGREEN)
    if a_arc and a > 2:
        d.arc([CX - 70, CY - 70, CX + 70, CY + 70], 360 - a, 360, fill=GREEN, width=6)
        if a_lab:
            am = math.radians(min(a, 60) / 2 + (a - min(a, 60)) / 2)
            tag(d, CX + 150 * math.cos(am) + 70, CY - 150 * math.sin(am) - 20, a_lab, 56, DGREEN, alpha=alpha_k)


# ---------------- canh 1: Du doan ----------------
def hook_angle(t, sc):
    return 30 * ease((t - 2.0) / 1.0)


def s_hook(img, d, t, sc):
    M = sc["M"]; a = hook_angle(t, sc)
    field_panel(d, a, show_n=False, m_arc=a > 29.5, m_lab="60°")
    km = clamp(1 - (t - 1.9) / 0.3) * appear(t, 0.5, 0.4)
    if km > 0: tag(d, 600, 380, "Φ lớn nhất", 58, ORANGE, alpha=km, anchor="l")
    k = appear(t, M[1] - 0.15, 0.45)
    if k <= 0: return
    y0 = 830 + (1 - k) * 30
    card(d, (50, y0, 1030, y0 + 700), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 102), fill=A(PURPLE, k), r=36)
    text(d, (W / 2, y0 + 64), "DỰ ĐOÁN", 56, WHITE, alpha=k)
    text(d, (W / 2, y0 + 210), "Mặt khung hợp B góc 60°.", 62, INK, alpha=k)
    text(d, (W / 2, y0 + 330), "Φ còn bao nhiêu phần", 62, PURPLE, alpha=k)
    text(d, (W / 2, y0 + 415), "Φ lớn nhất?", 62, PURPLE, alpha=k)
    seg_bar(d, y0 + 540, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, k)


# ---------------- canh 2: Tien hanh ----------------
def segs(sc):
    M = sc["M"]
    return [(M[1] + 0.3, M[1] + 1.2, 0, 30), (M[2] + 0.1, M[2] + 0.9, 30, 60), (M[3] + 0.1, M[3] + 0.9, 60, 90)]


def alpha_at(t, sc):
    a = 0.0
    for s0, s1, a0, a1 in segs(sc):
        if t >= s0: a = lerp(a0, a1, ease((t - s0) / (s1 - s0)))
    return a


def records(t, sc):
    times = [sc["M"][0] + 2.2] + [s1 + 0.05 for s0, s1, a0, a1 in segs(sc)]
    return [r for r, tm in zip(ROWS, times) if t >= tm]


def galvo(d, g):
    card(d, (680, 830, 1040, 1100), fill=WHITE, outline=NAVY, w=4, r=24)
    gx, gy, gr = 860, 1000, 110
    text(d, (860, 1058), "điện kế", 56, NAVY)
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 270 - 55, 270 + 55, fill=NAVY, width=4)
    d.line([(gx, gy - gr), (gx, gy - gr + 20)], fill=NAVY, width=5)
    for v in (-1, -0.5, 0.5, 1):
        an = math.radians(v * 50)
        d.line([(gx + (gr - 14) * math.sin(an), gy - (gr - 14) * math.cos(an)),
                (gx + gr * math.sin(an), gy - gr * math.cos(an))], fill=NAVY, width=4)
    an = math.radians(clamp(g, -1, 1) * 50)
    d.line([(gx, gy), (gx + (gr - 8) * math.sin(an), gy - (gr - 8) * math.cos(an))], fill=RED, width=8)
    dot(d, gx, gy, 11, NAVY)


def plot(d, box, a_drawn, recs, pen=False):
    x0, yt, x1, yb = box
    X = lambda a: x0 + a / 90 * (x1 - x0)
    Y = lambda p: yb - p / PMAX * (yb - yt)
    for p in (0.01, 0.005):
        dashed(d, (x0, Y(p)), (x1, Y(p)), LIGHT, 3)
        text(d, (x0 - 16, Y(p)), fphi(p), 56, INK, bold=False, anchor="rm")
    for a in (30, 60, 90):
        dashed(d, (X(a), yt), (X(a), yb), LIGHT, 3)
    for a in (0, 30, 60, 90):
        text(d, (X(a), yb + 44), str(a), 56, INK, bold=False)
    d.line([(x0, yb), (x0, yt - 20)], fill=NAVY, width=5)
    d.polygon([(x0, yt - 38), (x0 - 11, yt - 18), (x0 + 11, yt - 18)], fill=NAVY)
    d.line([(x0, yb), (x1 + 30, yb)], fill=NAVY, width=5)
    d.polygon([(x1 + 48, yb), (x1 + 28, yb - 11), (x1 + 28, yb + 11)], fill=NAVY)
    text(d, (x0 + 24, yt - 30), "Φ (Wb)", 56, INK, anchor="lm")
    text(d, (x1 + 100, yb - 70), "α (°)", 56, INK, anchor="rm")
    if a_drawn > 0.2:
        n = max(2, int(a_drawn * 1.5))
        d.line([(X(a_drawn * k / (n - 1)), Y(phi_model(a_drawn * k / (n - 1)))) for k in range(n)],
               fill=BLUE, width=7, joint="curve")
    for a, p in recs: dot(d, X(a), Y(p), 13, ORANGE, outline=WHITE)
    if pen and 0.2 < a_drawn < 89.8: dot(d, X(a_drawn), Y(phi_model(a_drawn)), 13, RED, outline=WHITE)


def s_do(img, d, t, sc):
    a = alpha_at(t, sc)
    rot = any(s0 < t < s1 for s0, s1, a0, a1 in segs(sc))
    dadt = (alpha_at(t + 0.01, sc) - alpha_at(t - 0.01, sc)) / 0.02
    g = math.sin(math.radians(a)) * dadt / 45.0              # kim lech chi khi Phi dang bien thien (dang quay)
    field_panel(d, a, band=True, a_arc=True, a_lab="α", wires=True)
    recs = records(t, sc)
    card(d, (40, 830, 660, 1100), fill=WHITE, outline=NAVY, w=4, r=24)
    if recs:                                       # khi quay: giu so do cua lan dung truoc, mo di
        ra, rp = recs[-1]; al = 0.35 if rot else 1.0
        text(d, (80, 905), f"α = {ra}°", 62, DGREEN, anchor="lm", alpha=al)
        text(d, (80, 1020), f"Φ = {fphi(rp)} Wb", 62, ORANGE, anchor="lm", alpha=al)
    galvo(d, g)
    card(d, (40, 1120, 1040, 1680), fill=WHITE, outline=LIGHT, w=3)
    plot(d, (250, 1210, 930, 1560), a, recs, pen=True)


# ---------------- canh 3: Dap an + Rut ra ----------------
def kcard(d, y, lines, color, k, h=150):
    if k <= 0: return
    yy = y + (1 - k) * 30
    card(d, (40, yy, 1040, yy + h), fill=A(WHITE, k), outline=A(color, k), w=5, r=26)
    for i, (s, col) in enumerate(lines):
        text(d, (W / 2, yy + h / 2 + (i - (len(lines) - 1) / 2) * 80), s, 60, col, alpha=k)


def s_rut(img, d, t, sc):
    M = sc["M"]
    field_panel(d, 30, band=True, a_arc=True, a_lab="α = 30°", m_arc=True, m_lab="60°")
    ka = appear(t, M[0] - 0.1, 0.45)
    if ka > 0:                                      # the dap an: nhan + so do o alpha = 30 do (cung mot khoi chu)
        yy = 830 + (1 - ka) * 30
        card(d, (40, yy, 1040, yy + 230), fill=A(WHITE, ka), outline=A(GREEN, ka), w=5, r=26)
        pw = tw(d, "ĐÁP ÁN C", F(56)) + 52
        card(d, (W / 2 - pw / 2, yy + 24, W / 2 + pw / 2, yy + 96), fill=A(GREEN, ka), r=34)
        text(d, (W / 2, yy + 60), "ĐÁP ÁN C", 56, WHITE, alpha=ka)
        text(d, (W / 2, yy + 160), "Φ = 0,00866 Wb", 62, ORANGE, alpha=ka)
    kcard(d, 1090, [("Φ = BS cos α", DGREEN), ("α = 90° − 60° = 30°", DGREEN)], GREEN, appear(t, M[1] - 0.1, 0.45),
          h=230)
    kcard(d, 1350, [("Chưa nói được:", NAVY), ("chiều và độ lớn dòng", INK)], NAVY, appear(t, M[2] - 0.1, 0.45),
          h=230)


# ---------------- canh 4: Bay - mat khung song song B ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    field_panel(d, 90, band=True, a_arc=appear(t, M[2] - 0.1, 0.3) > 0, a_lab="α = 90°", m_lab=None)
    km = appear(t, 0.3, 0.4)
    if km > 0:                                      # chu thich: mat khung nam doc duong suc, goc mat-B = 0
        tag(d, CX + 40, CY + 92, "mặt khung dọc B", 56, DPURPLE, alpha=km)
    k1 = appear(t, M[1] - 0.1, 0.45)
    if k1 > 0:
        card(d, (40, 840, 1040, 1150), fill=A((254, 242, 242), k1), outline=A(DRED, k1), r=26, w=6)
        text(d, (W / 2, 925), "✗ Lấy góc mặt khung = 0°", 60, DRED, alpha=k1)
        text(d, (W / 2, 1050), "cos 0° = 1: Φ lớn nhất? (sai)", 60, DRED, alpha=k1)
    k2 = appear(t, M[2] - 0.1, 0.45)
    if k2 > 0:
        card(d, (40, 1190, 1040, 1500), fill=A((236, 253, 243), k2), outline=A(DGREEN, k2), r=26, w=6)
        text(d, (W / 2, 1275), "✓ Không đường nào qua", 60, DGREEN, alpha=k2)
        text(d, (W / 2, 1400), "Φ = 0", 64, DGREEN, alpha=k2)


# ---------------- canh 5: Chot + THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    M = sc["M"]
    field_panel(d, CHOT[0], show_n=True, m_arc=True, m_lab="30°")
    k1 = appear(t, 0.5, 0.45)
    card(d, (40, 830, 1040, 1520), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    text(d, (W / 2, 1000), "Quay quá vị trí song song,", 58, INK, alpha=k1)
    text(d, (W / 2, 1085), "mặt khung hợp B góc 30°.", 58, INK, alpha=k1)
    text(d, (W / 2, 1175), "B = 0,2 T · S = 0,05 m²", 58, INK, alpha=k1)
    text(d, (W / 2, 1265), "Φ = ?", 64, ORANGE, alpha=k1)
    kh = appear(t, 3.0, 0.5)
    if kh > 0:
        card(d, (110, 1335, 970, 1495), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1415), "Gợi ý: α đo từ đâu tới đâu?", 58, ORANGE, alpha=kh)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.15, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + s1, "tap") for s0, s1, a0, a1 in segs(do)]
    out += [(r["t0"] + r["M"][0] - 0.1, "ding"), (b["t0"] + b["M"][1] - 0.1, "buzz"), (e["t0"] + 0.5, "open")]
    return out


CLIP = dict(id="tn-l12-camungdt-03", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Cảm ứng điện từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Khung quay giữa hai cực", draw=s_hook, tail=0.3, caps=[
   ("Lúc đầu mặt khung vuông góc B.", 3.2),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Bắt đầu: α = 0°.", 2.5),
   ("Quay: kim lệch. Dừng: kim về 0.", 3.6),
   ("Tới α = 60°.", 2.5),
   ("Tới 90°: Φ = 0.", 2.5)]),
 dict(key="rut", title="Kết quả", draw=s_rut, tail=0.3, caps=[
   ("Hơn một nửa.", 3.0),
   ("α đo từ pháp tuyến n.", 3.0),
   ("Cần thêm Lenz và Faraday.", 3.6)]),
 dict(key="bay", title="Bẫy: lấy góc mặt khung", draw=s_bay, tail=0.3, caps=[
   ("Khung song song đường sức.", 3.4),
   ("Đừng vội thay vào cos.", 3.4),
   ("Góc của n với B mới là α.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("α: góc của n với B.", 6.6)]),
])
