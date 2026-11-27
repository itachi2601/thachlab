# Clip: tn-l11-baitapdaodong-01 - Chum chia khoa treo day 36 cm: bam gio 10 dao dong bang dien thoai, lap 5 lan
# (31/10/2026; dung lai 27/11/2026 theo cong moi: --do-chu 0 LOI, chu ve >= 55 px, Du doan K10, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-baitapdaodong-01.json (_kiem_so() doi chieu):
#   tham_so: L = 0,36 m (36 cm); A = 5 cm (mac dinh), A max 8 cm (dung cho cau chot).
#   so_lieu_mau t10 (s): 12,12; 11,93; 12,18; 11,89; 12,03. rut_ra: TB 12,03 s, T = 1,203 s -> 1,20 s;
#   omega = 2 pi / T ~ 5,22 rad/s; v_max = A omega ~ 26 cm/s.
# Du doan (K10: khong nut A-D): bam 10 dao dong, 5 lan -> nam so do ra sao? -> chenh nhau co phan muoi giay.
# Bay = hien_tuong_hay_sai[1]: bam bien nay sang bien kia roi goi la mot chu ki (hinh: 2 mui ten nua/du dao dong).
# Chua noi duoc: goc lech vai chuc do (mo hinh chi goc nho), day khac.
# Thu nghi (= cau_chot khung web): keo lech 8 cm (tham_so A max, van goc nho ~13 do) -> T khong doi -> v_max = 8 . 5,22
#   ~ 42 cm/s. Buoc suy luan chua chieu: T khong phu thuoc A. So 42 KHONG hien tren man.
# Khong chieu T = 1,20 +- 0,02 s (dap an Cau 3 trong bai).
from engine import *

T10 = [12.12, 11.93, 12.18, 11.89, 12.03]           # so_lieu_mau
T_MO = 1.204                                        # T mo hinh (ket_qua_ky_vong)
L_PX = 560; A_CM = 5.0; L_CM = 36.0; A_CHOT = 8
PXC = L_PX / L_CM                                   # px moi cm (dung ti le day 36 cm)
A_PX = A_CM * PXC
PIV = (300, 290)
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
DGREEN = (21, 110, 55); DRED = (185, 28, 28); GOLD = (196, 150, 40); STEEL = (140, 150, 165); DORANGE = (176, 64, 8)
PHONE = (40, 44, 60); SCREEN = (245, 247, 252); EMPTY = (148, 140, 128)

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-baitapdaodong-01.json")))
    assert [r[1] for r in k["so_lieu_mau"]["hang"]] == T10
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["L"]["mac_dinh"] == 0.36 and ts["A"]["mac_dinh"] == A_CM and ts["A"]["max"] == A_CHOT
    assert abs(sum(T10) / 5 - 12.03) < 0.005 and "5,22 rad/s" in k["ket_qua_ky_vong"] and "26 cm/s" in k["ket_qua_ky_vong"]
_kiem_so()

_TI = {}
def TI(size):                                       # Times Bold Italic cho omega, pi (omega cua SF giong w)
    size = int(size)
    if size not in _TI: _TI[size] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", size)
    return _TI[size]

def eq(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """Cong thuc: 'ω', 'π' ve bang Times Bold Italic; _{..} chi so duoi (>= 55 px de ra >= 48 px trong mp4)."""
    fs = []
    for p in [p for p in re.split(r"(ω|π|_\{[^}]*\})", s) if p]:
        if p in ("ω", "π"): fs.append((p, TI(size * 1.12), 0))
        elif p.startswith("_{"): fs.append((p[2:-1], F(56), size * 0.3))
        else: fs.append((p, F(size), 0))
    tot = sum(tw(d, p, f) for p, f, _ in fs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for p, f, dy in fs:
        dtext(d, (x, cy + dy), p, f, color, alpha, "lm"); x += tw(d, p, f)
    return tot

def seg_bar(d, y, t, t0, t1, col, a=1.0, n=6):
    """Thanh dem lien khoi, tat lan luot tu PHAI sang TRAI; cao 76 px (cong --do-chu tinh la hinh doi)."""
    p = clamp((t - t0) / (t1 - t0)); on = n - int(p * n + 1e-9); wseg = 820 / n
    for i in range(n):
        x = 130 + i * wseg
        if i < on: card(d, (x, y, x + wseg - 14, y + 76), fill=A(col, a), r=16)
        else: card(d, (x, y, x + wseg - 14, y + 76), fill=A(WHITE, a), outline=A(EMPTY, a), r=16, w=4)

# ---------------- con lac chum chia khoa ----------------
def xpx(tau, a_px=A_PX): return a_px * math.cos(2 * math.pi * tau / T_MO)

def rot(pts, c, ang):
    ca, sa = math.cos(ang), math.sin(ang)
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa, c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]

def pendulum(d, x_off, piv=PIV, L=L_PX, alpha=1.0, desk=True, scale=1.0):
    """Day + chum chia khoa; x_off = do lech ngang (px) cua vong khoa so voi duong thang dung qua diem treo."""
    c = lambda col: A(col, alpha)
    px0, py0 = piv
    if desk:
        d.rectangle([px0 - 200, py0 - 40, px0 + 150, py0], fill=c((205, 170, 120)), outline=c(NAVY), width=3)
        for xx in range(int(px0 - 190), int(px0 + 150), 40): d.line([(xx, py0 - 40), (xx + 20, py0 - 20)], fill=c((180, 145, 95)), width=2)
    bx = px0 + x_off; by = py0 + math.sqrt(L * L - x_off * x_off)
    ang = math.atan2(x_off, by - py0)
    d.line([(px0, py0), (bx, by - 22 * scale)], fill=c(NAVY), width=4)
    dot(d, px0, py0, 8, c(NAVY))
    r = 22 * scale
    d.ellipse([bx - r, by - r, bx + r, by + r], outline=c(GOLD), width=max(3, int(7 * scale)))
    for dx, dl, col in ((-20, 70, STEEL), (2, 88, GOLD), (22, 64, STEEL)):   # 3 chia khoa treo duoi vong
        dx *= scale; dl *= scale
        top = (bx + dx * 0.5, by + r * 0.8)
        head = [(top[0] - 15 * scale, top[1]), (top[0] + 15 * scale, top[1]), (top[0] + 15 * scale, top[1] + 26 * scale), (top[0] - 15 * scale, top[1] + 26 * scale)]
        blade = [(top[0] - 5 * scale, top[1] + 26 * scale), (top[0] + 5 * scale, top[1] + 26 * scale), (top[0] + 5 * scale, top[1] + dl), (top[0] - 5 * scale, top[1] + dl)]
        tooth = [(top[0] + 5 * scale, top[1] + dl - 22 * scale), (top[0] + 14 * scale, top[1] + dl - 16 * scale), (top[0] + 5 * scale, top[1] + dl - 8 * scale)]
        o = (bx + dx * 0.4, by)
        dang = ang + math.radians(dx * 0.35)
        for poly in (blade, tooth, head):
            d.polygon(rot(poly, o, -dang), fill=c(col), outline=c(NAVY))
    return bx, by

def ruler(d, piv=PIV, bx=None, alpha=1.0, kmax=6, lab=5):
    """Thuoc ke ngang duoi chum khoa: 0 o duong thang dung qua diem treo, vach moi cm theo ti le day 36 cm;
    tam giac cam chi do lech ngang hien tai cua vong khoa (bx). lab = vach co ghi so (cm)."""
    c = lambda col: A(col, alpha); x0 = piv[0]; y = piv[1] + L_PX + 120
    for yy in range(int(piv[1]) + 20, int(y), 26):                 # duong thang dung qua diem treo (VTCB)
        d.line([(x0, yy), (x0, yy + 12)], fill=c(GRAY), width=3)
    d.rectangle([x0 - 2 * PXC - 20, y, x0 + kmax * PXC + 20, y + 30], fill=c((250, 240, 200)), outline=c(NAVY), width=2)
    for k in range(-2, kmax + 1):
        xx = x0 + k * PXC
        d.line([(xx, y), (xx, y + (22 if k in (0, lab) else 12))], fill=c(NAVY), width=3)
    text(d, (x0, y + 66), "0", 56, INK, alpha=alpha)
    text(d, (x0 + lab * PXC - 16, y + 66), f"{lab} cm", 56, INK, anchor="lm", alpha=alpha)
    if bx is not None:
        d.polygon([(bx, y), (bx - 13, y - 22), (bx + 13, y - 22)], fill=c(ORANGE))
    return y

# ---------------- dien thoai ----------------
def phone(d, box, big, sub, rows=0, avg=False, alpha=1.0, hi=None):
    x0, y0, x1, y1 = box; cx = (x0 + x1) / 2
    card(d, box, fill=A(PHONE, alpha), r=46)
    card(d, (x0 + 18, y0 + 50, x1 - 18, y1 - 40), fill=A(SCREEN, alpha), r=26)
    d.rounded_rectangle([cx - 50, y0 + 18, cx + 50, y0 + 32], radius=7, fill=A((90, 95, 115), alpha))
    text(d, (cx, y0 + 145), big, 96, INK, alpha=alpha)
    if sub: text(d, (cx, y0 + 240), sub, 56, TEAL, alpha=alpha)
    if rows <= 0 and not avg: return
    yh = y0 + 330
    d.line([(x0 + 40, yh - 40), (x1 - 40, yh - 40)], fill=A(LIGHT, alpha), width=3)
    text(d, (cx, yh + 4), "10 dao động (s)", 56, INK, alpha=alpha)
    for i in range(rows):
        y = yh + 86 + i * 76
        col = ORANGE if hi == i else INK
        text(d, (x0 + 66, y), str(i + 1), 56, col, alpha=alpha)
        text(d, (x1 - 50, y), vn(T10[i]), 56, col, anchor="rm", alpha=alpha)
    if avg:
        y = yh + 86 + 5 * 76 + 14
        d.line([(x0 + 40, y - 38), (x1 - 40, y - 38)], fill=A(LIGHT, alpha), width=3)
        text(d, (x0 + 46, y + 2), "TB", 56, DGREEN, anchor="lm", alpha=alpha)
        text(d, (x1 - 50, y + 2), vn(sum(T10) / 5), 56, DGREEN, anchor="rm", alpha=alpha)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong nut A-D) ----------------
PULL = (0.7, 2.4)                                   # keo lech tu 0 ra 5 cm
def s_hook(img, d, t, sc):
    M = sc["M"]
    x_off = A_PX * ease((t - PULL[0]) / (PULL[1] - PULL[0]))
    ruler(d, bx=PIV[0] + x_off)
    pendulum(d, x_off)
    text(d, (282, 600), "36 cm", 58, NAVY, anchor="rm")
    phone(d, (620, 300, 980, 840), "0,00", None)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 590), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 100), fill=A(PURPLE, a), r=36)
    text(d, (W / 2, y0 + 62), "DỰ ĐOÁN", 56, WHITE, alpha=a)
    text(d, (W / 2, y0 + 170), "Lúc thả đếm “một”,", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 248), "về chỗ thả: đếm tiếp,", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 326), "tới “mười” thì dừng.", 60, INK, alpha=a)
    text(d, (W / 2, y0 + 410), "Mấy dao động?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 480, t, M[1] + 0.4, sc["T"] - 0.2, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
REL = 0.0            # tha chum khoa ngay dau canh (noi tiep canh Du doan dang giu o 5 cm)
RT = 1.6             # 1,6 s dau chieu that
FAST = 6.0           # roi tua nhanh x6 (nhan "×6" + bieu tuong ve tay: khong tinh la khoi chu)
U_STOP = REL + RT + (T10[0] - RT) / FAST       # luc bam dung (dong ho = 12,12 s)

def do_state(u, sc):
    M = sc["M"]
    if u < REL: tau = 0.0
    elif u < REL + RT: tau = u - REL
    elif u < U_STOP: tau = RT + (u - REL - RT) * FAST
    else: tau = T10[0] + (u - U_STOP)             # bam dung xong: con lac van dao dong (chieu that)
    st = dict(tau=tau, fast=(REL + RT <= u < U_STOP))
    if u < M[1] + 0.2:                           # lan 1
        sw = min(tau, T10[0]); st.update(sw=sw, count=min(10, int(sw / T_MO + 1e-9)), lan=1,
                                          rows=1 if u >= U_STOP else 0, running=REL <= u < U_STOP)
    else:                                         # lan 2-5: moi 0,6 s ghi them mot dong
        k = min(4, 1 + int((u - M[1] - 0.2) / 0.5))
        st.update(sw=T10[k], count=None, lan=k + 1, rows=k + 1, running=False, fast=False)
    st["avg"] = u >= M[1] + 0.2 + 4 * 0.5 + 0.4
    return st

DP = (300, 450)
def s_do(img, d, t, sc):
    st = do_state(t, sc)
    ruler(d, piv=DP, bx=DP[0] + xpx(st["tau"]))
    pendulum(d, xpx(st["tau"]), piv=DP)
    if st["running"]: sub = "đang chạy"
    elif t < REL: sub = None
    else: sub = f"lần {st['lan']}"
    phone(d, (560, 440, 1020, 1420), vn(st["sw"]), sub, rows=st["rows"], avg=st["avg"],
          hi=st["rows"] - 1 if st["rows"] and not st["avg"] else None)
    if st["count"] is not None and t >= REL:
        card(d, (60, 1260, 520, 1380), fill=WHITE, outline=ORANGE, r=24, w=5)
        text(d, (290, 1320), f"đếm: {st['count']}/10", 62, ORANGE)
    if st["fast"]:
        card(d, (60, 1410, 320, 1500), fill=ORANGE, r=40)                       # bieu tuong tua nhanh (ve tay) + "×6"
        for dx in (0, 34): d.polygon([(100 + dx, 1430), (100 + dx, 1480), (136 + dx, 1455)], fill=WHITE)
        text(d, (245, 1455), "×6", 60, WHITE)

# ---------------- canh 3: Dap an Du doan - dem "mot" luc tha thi chi 9 dao dong ----------------
CX0, CDX = 100, 88                                  # truc dem: vach k o x = CX0 + k*CDX (k = 0..10)
def count_row(d, y, t, t0, start, col, n_lab):
    """Hang vach: vach 0 = luc tha; nhan so hien lan luot tu t0 (moi 0,2 s); start = so dem luc tha (1 hoac 0)."""
    d.line([(CX0 - 20, y), (CX0 + 10 * CDX + 20, y)], fill=col, width=5)
    d.polygon([(CX0, y - 24), (CX0 - 16, y - 54), (CX0 + 16, y - 54)], fill=TEAL)      # vach 0 = luc tha
    for k in range(11):
        x = CX0 + k * CDX
        d.line([(x, y - 18), (x, y + 18)], fill=col, width=5 if k == 0 else 4)
        v = start + k
        if v <= 10 and t >= t0 + 0.15 * k: text(d, (x, y + 62), str(v), 56, col)
    return CX0 + (10 - start) * CDX                 # x cua vach dem "muoi"

def s_dapan(img, d, t, sc):
    M = sc["M"]
    # hang 1: dem "mot" luc tha
    card(d, (40, 250, 1040, 640), fill=(254, 242, 242), outline=DRED, r=24, w=5)
    text(d, (W / 2, 300), "✗ Lúc thả đếm “một”", 60, DRED)
    x10 = count_row(d, 400, t, 0.1, 1, DRED, 10)
    kb = appear(t, 1.8, 0.4)
    if kb > 0:
        d.line([(CX0, 520), (CX0, 540), (x10, 540), (x10, 520)], fill=A(DRED, kb), width=6)
        text(d, ((CX0 + x10) / 2, 590), "chỉ 9 dao động", 60, DRED, alpha=kb)
    # hang 2: dem 0 luc tha
    k2 = appear(t, M[1] - 0.05, 0.4)
    if k2 > 0:
        card(d, (40, 680, 1040, 1070), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=24, w=5)
        text(d, (W / 2, 730), "✓ Lúc thả đếm 0", 60, DGREEN, alpha=k2)
        x10 = count_row(d, 830, t, M[1] + 0.1, 0, DGREEN, 10)
        kc = appear(t, M[1] + 2.2, 0.4)
        if kc > 0:
            d.line([(CX0, 950), (CX0, 970), (x10, 970), (x10, 950)], fill=A(DGREEN, kc), width=6)
            text(d, ((CX0 + x10) / 2, 1020), "đủ 10 dao động", 60, DGREEN, alpha=kc)

# ---------------- canh 4: Rut ra + chua noi duoc ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.45)
    card(d, (60, 300, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), r=24, w=5)
    text(d, (W / 2, 360), "TB 5 lần: 12,03 s", 60, DGREEN, alpha=k0)
    eq(d, W / 2, 455, "T = 12,03 : 10 ≈ 1,20 s", 62, DGREEN, alpha=k0)
    k2 = appear(t, 2.6, 0.45)
    if k2 > 0:
        card(d, (60, 560, 1020, 780), fill=A(WHITE, k2), outline=A(BLUE, k2), r=24, w=5)
        eq(d, W / 2, 620, "ω = 2π/T ≈ 5,22 rad/s", 60, INK, alpha=k2)
        eq(d, W / 2, 712, "v_{max} = A·ω ≈ 26 cm/s", 60, INK, alpha=k2)
    k3 = appear(t, M[1] - 0.05, 0.4)
    if k3 > 0:
        card(d, (60, 830, 1020, 1140), fill=A(WHITE, k3), outline=A(NAVY, k3), r=24, w=5)
        text(d, (W / 2, 890), "Chưa nói được", 60, NAVY, alpha=k3)
        text(d, (100, 980), "• Góc lệch lớn: chưa thử", 58, INK, anchor="lm", alpha=k3)
        text(d, (100, 1070), "• Dây khác: chưa đo", 58, INK, anchor="lm", alpha=appear(t, M[1] + 2.5, 0.4))
    tau = t                                           # con lac nho van dao dong (hinh khong dung yen)
    pendulum(d, xpx(tau) * 0.9, piv=(540, 1215), L=300, scale=0.8)

# ---------------- canh 5: Bay - bien nay sang bien kia ----------------
BP = (540, 330); BA = 190                         # bien do ve phong to (so do, khong theo ti le) cho de thay
SLOW = 2.0                                        # quay cham x2
B1 = 0.85
def bay_tau(t, sc):
    M = sc["M"]; h = T_MO / 2; b2 = M[1] + 0.05         # 2 nhip cach 3,0 s, nhip 2 hien >= 3,2 s
    if t < B1: return 0.0
    if t < B1 + h * SLOW: return (t - B1) / SLOW
    if t < b2: return h
    if t < b2 + h * SLOW: return h + (t - b2) / SLOW
    return T_MO

def s_bay(img, d, t, sc):
    M = sc["M"]; h = T_MO / 2; b2 = M[1] + 0.05
    tau = bay_tau(t, sc)
    ybob = BP[1] + math.sqrt(L_PX ** 2 - BA ** 2)
    for s in (-1, 1):                              # vach bien trai/phai (net dut)
        for yy in range(int(ybob) - 60, int(ybob) + 160, 24):
            d.line([(BP[0] + s * BA, yy), (BP[0] + s * BA, yy + 12)], fill=GRAY, width=4)
    text(d, (BP[0] - BA - 20, ybob + 130), "biên", 58, INK, anchor="rm")
    text(d, (BP[0] + BA + 20, ybob + 130), "biên", 58, INK, anchor="lm")
    xr = BP[0] + BA                                # cho tha
    d.polygon([(xr, ybob - 150), (xr - 18, ybob - 186), (xr + 18, ybob - 186)], fill=TEAL)
    text(d, (xr + 30, ybob - 180), "thả", 58, TEAL, anchor="lm")
    pendulum(d, BA * math.cos(2 * math.pi * tau / T_MO), piv=BP)
    card(d, (40, 380, 400, 466), fill=TEAL, r=40); text(d, (220, 423), "chậm ×2", 56, WHITE)
    y1, y2 = 1110, 1330
    if t >= B1 + h * SLOW:                         # nua chu ki dau xong
        card(d, (60, y1 - 70, 1020, y1 + 130), fill=(255, 247, 237), outline=ORANGE, r=24, w=5)
        arrow(d, (BP[0] + BA, y1 - 10), (BP[0] - BA, y1 - 10), ORANGE, w=8, head=26)
        text(d, (W / 2, y1 + 70), "✗ mới nửa dao động", 60, DRED)
    if t >= b2 + h * SLOW:
        card(d, (60, y2 - 70, 1020, y2 + 130), fill=(236, 253, 243), outline=GREEN, r=24, w=5)
        arrow(d, (BP[0] - BA, y2 - 10), (BP[0] + BA, y2 - 10), DGREEN, w=8, head=26)
        text(d, (W / 2, y2 + 70), "✓ về chỗ thả: 1 dao động", 60, DGREEN)

# ---------------- canh 6: Chot (phu de) + THU NGHI (= cau_chot khung web) ----------------
EP = (300, 400)
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 1585), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 240, W / 2 + pw / 2, 316), fill=A(ORANGE, k1), r=36)
    text(d, (W / 2, 278), "THỬ NGHĨ", 56, WHITE, alpha=k1)
    xo = A_CHOT * PXC
    ruler(d, piv=EP, bx=EP[0] + xo, alpha=k1, kmax=9, lab=A_CHOT)
    pendulum(d, xo, piv=EP, alpha=k1)
    text(d, (W / 2, 1230), "Kéo lệch 8 cm, thả.", 62, INK, alpha=k1)
    eq(d, W / 2, 1320, "v_{max} = ?", 66, DORANGE, alpha=k1)
    seg_bar(d, 1420, t, 0.8, sc["T"] - 0.2, ORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"), (do["t0"] + REL, "tap")]
    out += [(do["t0"] + REL + RT + 0.4 * j, "tick") for j in range(4)]
    out += [(do["t0"] + U_STOP, "tap")]
    out += [(do["t0"] + do["M"][1] + 0.2 + 0.5 * k, "tick") for k in range(4)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + b["M"][0] + 0.1, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-baitapdaodong-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Dao động điều hoà · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Chùm chìa khoá treo dây", draw=s_hook, tail=0.3, caps=[
   ("Dây 36 cm, lệch 5 cm.", 3.4),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.2, caps=[
   ("Thả là 0, đếm tới 10.", 3.8),
   ("Lặp thêm 4 lần, ghi lại.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Vạch đầu là lúc thả.", 4.0),
   ("Lúc thả chưa có dao động nào.", 4.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.2, caps=[
   ("Lấy trung bình rồi chia 10.", 4.6),
   ("Mới thử một dây, góc nhỏ.", 4.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.2, caps=[
   ("Bẫy: biên này sang biên kia.", 3.4),
   ("Phải quay về đúng chỗ thả.", 4.3)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự tính.", 4.6)]),
])
