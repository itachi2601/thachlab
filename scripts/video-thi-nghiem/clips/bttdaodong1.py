# Clip: tn-l11-baitapdaodong-01 - Chum chia khoa treo day 36 cm: bam gio 10 dao dong bang dien thoai, lap 5 lan (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-baitapdaodong-01.json:
#   tham_so: L = 0,36 m (36 cm); A = 5 cm (5,0 cm); A max 8 cm (dung cho cau chot).
#   so_lieu_mau t10 (s): 12,12; 11,93; 12,18; 11,89; 12,03. ket_qua_ky_vong: mo hinh T = 1,204 s.
#   rut_ra: t10 TB 12,03 s; (12,18 - 11,89)/2 ~ 0,15 s -> Delta T ~ 0,015 s ~ 0,02 s; T = 1,20 +- 0,02 s;
#           omega = 2 pi / T ~ 5,22 rad/s; v_max = A omega ~ 26 cm/s.
#   mo_hinh.gia_thiet: sai lech bam tay ngau nhien co 0,1-0,2 s -> lua chon dung cua Du doan "chenh nhau co phan muoi giay".
#   hien_tuong_hay_sai[1]: bam bien nay sang bien kia roi goi la mot chu ki -> canh bay.
#   Cau chot: keo lech 8 cm (tham_so A max, chua hien) -> T khong doi (mo hinh T = 2 pi can(L/g)) -> v_max ~ 8 . 5,22
#             ~ 42 cm/s (KHONG hien tren man).
# Dan canh rieng (khac vantocdddh1 cung bam t10): con lac DON (chum chia khoa treo mep ban) + DIEN THOAI co danh sach
#   "lan bam" tren man hinh; Ket qua = truc so cham 5 diem t10 (do phan tan) roi chia 10.
# Chuyen dong: x = A cos(2 pi tau / T_MO), tau = thoi gian thi nghiem; lan 1: 2,6 s dau chieu that, sau do tua nhanh x6;
#   dong ho dien thoai = tau (bat dau dung luc tha) toi khi bam dung o 12,12 s; dem = so lan quay ve bien phai.
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (lan 1 day du, lan 2-5 ghi danh sach) -> Dap an (truc so, chia 10,
#       T, omega, v_max) + Chua noi duoc -> Bay (bien -> bien la nua chu ki) -> Chot + cau hoi tu nho lai.
from engine import *

T10 = [12.12, 11.93, 12.18, 11.89, 12.03]           # so_lieu_mau
T_MO = 1.204                                        # T mo hinh (ket_qua_ky_vong)
L_PX = 560; A_CM = 5.0; L_CM = 36.0
PXC = L_PX / L_CM                                   # px moi cm (dung ti le day 36 cm)
A_PX = A_CM * PXC
PIV = (300, 290)                                    # diem treo o mep ban
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
DGREEN = (21, 110, 55); DRED = (185, 28, 28); GOLD = (196, 150, 40); STEEL = (140, 150, 165)
PHONE = (40, 44, 60); SCREEN = (245, 247, 252)

_TI = {}
def TI(size):                                       # Times Bold Italic cho omega, pi (omega cua SF giong w)
    size = int(size)
    if size not in _TI: _TI[size] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", size)
    return _TI[size]

def eq(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """Cong thuc: 'ω', 'π' ve bang Times Bold Italic; _{..} chi so duoi (>= 36 px)."""
    fs = []
    for p in [p for p in re.split(r"(ω|π|_\{[^}]*\})", s) if p]:
        if p in ("ω", "π"): fs.append((p, TI(size * 1.12), 0))
        elif p.startswith("_{"): fs.append((p[2:-1], F(max(36, size * 0.62)), size * 0.26))
        else: fs.append((p, F(size), 0))
    tot = sum(tw(d, p, f) for p, f, _ in fs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for p, f, dy in fs:
        dtext(d, (x, cy + dy), p, f, color, alpha, "lm"); x += tw(d, p, f)
    return tot

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
    ang = math.atan2(x_off, by - py0)               # goc lech (rad), duong ve ben phai
    d.line([(px0, py0), (bx, by - 22 * scale)], fill=c(NAVY), width=3)
    dot(d, px0, py0, 7, c(NAVY))
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

def ruler(d, piv=PIV, bx=None, alpha=1.0):
    """Thuoc ke ngang duoi chum khoa (ve TRUOC con lac): 0 o duong thang dung qua diem treo, vach moi cm theo ti le
    day 36 cm; tam tam giac cam chi do lech ngang hien tai cua vong khoa (bx). Tra ve y mat tren thuoc."""
    c = lambda col: A(col, alpha); x0 = piv[0]; y = piv[1] + L_PX + 120
    for yy in range(int(piv[1]) + 20, int(y), 26):                 # duong thang dung qua diem treo (VTCB)
        d.line([(x0, yy), (x0, yy + 12)], fill=c(GRAY), width=2)
    d.rectangle([x0 - 2 * PXC - 20, y, x0 + 6 * PXC + 20, y + 30], fill=c((250, 240, 200)), outline=c(NAVY), width=2)
    for k in range(-2, 7):
        xx = x0 + k * PXC
        d.line([(xx, y), (xx, y + (20 if k in (0, 5) else 11))], fill=c(NAVY), width=3)
    text(d, (x0, y + 58), "0", 40, MUTED, bold=False, alpha=alpha)
    text(d, (x0 + 5 * PXC, y + 58), "5", 40, MUTED, bold=False, alpha=alpha)
    text(d, (x0 + 5 * PXC + 34, y + 58), "cm", 40, MUTED, bold=False, anchor="lm", alpha=alpha)
    if bx is not None:
        d.polygon([(bx, y), (bx - 11, y - 18), (bx + 11, y - 18)], fill=c(ORANGE))
    return y

# ---------------- dien thoai ----------------
def phone(d, box, big, sub, rows=0, avg=False, alpha=1.0, hi=None):
    x0, y0, x1, y1 = box; cx = (x0 + x1) / 2
    card(d, box, fill=A(PHONE, alpha), r=46)
    card(d, (x0 + 18, y0 + 50, x1 - 18, y1 - 40), fill=A(SCREEN, alpha), r=26)
    d.rounded_rectangle([cx - 50, y0 + 18, cx + 50, y0 + 32], radius=7, fill=A((90, 95, 115), alpha))
    text(d, (cx, y0 + 150), big, 92, INK, alpha=alpha)
    if sub: text(d, (cx, y0 + 235), sub, 40, MUTED, bold=False, alpha=alpha)
    if rows <= 0 and not avg: return
    yh = y0 + 310
    d.line([(x0 + 40, yh - 30), (x1 - 40, yh - 30)], fill=A(LIGHT, alpha), width=3)
    text(d, (cx, yh + 4), "10 dao động (s)", 40, MUTED, alpha=alpha)
    for i in range(rows):
        y = yh + 78 + i * 72
        col = ORANGE if hi == i else INK
        text(d, (x0 + 70, y), str(i + 1), 44, col, anchor="mm", alpha=alpha)
        text(d, (x1 - 50, y), vn(T10[i]), 44, col, anchor="rm", alpha=alpha)
    if avg:
        y = yh + 78 + 5 * 72 + 14
        d.line([(x0 + 40, y - 34), (x1 - 40, y - 34)], fill=A(LIGHT, alpha), width=3)
        text(d, (x0 + 50, y + 4), "TB", 44, DGREEN, anchor="lm", alpha=alpha)
        text(d, (x1 - 50, y + 4), vn(sum(T10) / 5), 44, DGREEN, anchor="rm", alpha=alpha)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong nut A-D) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    ruler(d, bx=PIV[0] + A_PX)
    pendulum(d, A_PX)                               # giu o bien phai, chua tha
    phone(d, (620, 300, 980, 860), "0,00", None)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1075 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 540), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 260, "Bấm giờ 10 dao động,\nlàm 5 lần.\nKết quả sẽ thế nào?", 52, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 480, 940, y0 + 492], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 480, 140 + 800 * (1 - p), y0 + 492], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
REL = 0.6            # tha chum khoa (tinh tu dau canh)
RT = 2.6             # 2,6 s dau chieu that
FAST = 6.0           # roi tua nhanh x6
U_STOP = REL + RT + (T10[0] - RT) / FAST       # luc bam dung (dong ho = 12,12 s)

def do_state(u, sc):
    """Trang thai canh Tien hanh tai giay u: tau (thoi gian thi nghiem), so dong ho, dem, so hang, lan dang hien."""
    M = sc["M"]
    if u < REL: tau = 0.0
    elif u < REL + RT: tau = u - REL
    elif u < U_STOP: tau = RT + (u - REL - RT) * FAST
    else: tau = T10[0] + (u - U_STOP)             # bam dung xong: con lac van dao dong (chieu that)
    st = dict(tau=tau, fast=(REL + RT <= u < U_STOP))
    if u < M[1] + 0.2:                           # lan 1
        sw = min(tau, T10[0]); st.update(sw=sw, count=min(10, int(sw / T_MO + 1e-9)), lan=1,
                                          rows=1 if u >= U_STOP + 0.3 else 0, running=REL <= u < U_STOP)
    else:                                         # lan 2-5: moi 0,5 s ghi them mot dong (tua nhanh)
        k = min(4, 1 + int((u - M[1] - 0.2) / 0.5))
        st.update(sw=T10[k], count=None, lan=k + 1, rows=k + 1, running=False, fast=False, ghi=True)
    st["avg"] = u >= M[1] + 0.2 + 4 * 0.5 + 0.4
    return st

DP = (300, 450)                                   # diem treo canh Tien hanh (thap hon canh Du doan)
def s_do(img, d, t, sc):
    st = do_state(t, sc)
    ruler(d, piv=DP, bx=DP[0] + xpx(st["tau"]))
    pendulum(d, xpx(st["tau"]), piv=DP)
    if st["running"]: sub = "đang chạy"
    elif st["lan"] == 1 and t < REL: sub = "sẵn sàng"
    else: sub = f"lần {st['lan']}: đã dừng"
    phone(d, (560, 450, 1020, 1330), vn(st["sw"]), sub, rows=st["rows"], avg=st["avg"], hi=st["rows"] - 1 if st["rows"] and not st["avg"] else None)
    if st["count"] is not None and t >= REL:
        card(d, (60, 1250, 520, 1410), fill=WHITE, outline=ORANGE, r=24, w=4)
        text(d, (290, 1295), "đã đếm", 40, MUTED, bold=False)
        text(d, (290, 1365), f"{st['count']} / 10", 60, ORANGE)
    if st["fast"]:
        card(d, (60, 1440, 400, 1506), fill=ORANGE, r=33); text(d, (230, 1473), "tua nhanh ×6", 40, WHITE)
    elif st.get("ghi"):
        card(d, (60, 1280, 520, 1380), fill=WHITE, outline=TEAL, r=24, w=4)
        text(d, (290, 1330), "con lắc vẫn đưa", 44, TEAL)

# ---------------- canh 3: Dap an + rut ra + chua noi duoc ----------------
NX0, NX1, NV0, NV1 = 120, 960, 11.85, 12.25        # truc so t10
def nx(v): return NX0 + (v - NV0) / (NV1 - NV0) * (NX1 - NX0)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · chênh cỡ phần mười giây"
    pw = tw(d, lab, F(40)) + 56
    card(d, (W / 2 - pw / 2, 270, W / 2 + pw / 2, 334), fill=A(NAVY, ka), r=32)
    text(d, (W / 2, 302), lab, 40, WHITE, alpha=ka)
    text(d, (W / 2, 400), "10 dao động (s)", 40, MUTED, bold=False, alpha=ka)
    yl = 620
    d.line([(NX0 - 20, yl), (NX1 + 20, yl)], fill=A(NAVY, ka), width=4)
    for v in (11.9, 12.0, 12.1, 12.2):
        d.line([(nx(v), yl - 12), (nx(v), yl + 12)], fill=A(NAVY, ka), width=3)
        text(d, (nx(v), yl + 50), vn(v, 1), 40, MUTED, bold=False, alpha=ka)
    order = sorted(range(5), key=lambda i: T10[i])
    for r, i in enumerate(order):                  # 5 diem, nhan so xen ke hai tang
        k = appear(t, 0.3 + 0.2 * i, 0.3)
        if k <= 0: continue
        v = T10[i]; col = ORANGE if v in (max(T10), min(T10)) else BLUE
        dot(d, nx(v), yl - 30, 14, A(col, k), outline=WHITE)
        yt = 545 if r % 2 == 0 else 480
        d.line([(nx(v), yl - 46), (nx(v), yt + 24)], fill=A(LIGHT, k), width=2)
        text(d, (nx(v), yt), vn(v), 40, col, alpha=k)
    kb = appear(t, 1.6, 0.4)                       # ngoac tu min toi max: do tan (khong tinh so, de khong lo Cau 3)
    if kb > 0:
        x0, x1, yb = nx(min(T10)), nx(max(T10)), 720
        d.line([(x0, yb - 14), (x0, yb), (x1, yb), (x1, yb - 14)], fill=A(ORANGE, kb), width=4)
    k1 = appear(t, M[0] + 0.3, 0.45)               # chia 10 (phu de 1): chi dinh tinh
    if k1 > 0:
        card(d, (60, 770, 1020, 990), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), r=24, w=4)
        ctext(d, 830, "Sai số cũng chia 10", 46, DGREEN, maxw=900, alpha=k1)
        eq(d, W / 2, 940, "T ≈ 1,20 s", 52, DGREEN, alpha=appear(t, M[0] + 0.8, 0.45))
    k2 = appear(t, M[1] + 0.2, 0.45)               # omega, v_max (phu de 2)
    if k2 > 0:
        card(d, (60, 1020, 1020, 1200), fill=A(WHITE, k2), outline=A(BLUE, k2), r=24, w=4)
        eq(d, W / 2, 1070, "ω = 2π/T ≈ 5,22 rad/s", 46, INK, alpha=k2)
        eq(d, W / 2, 1150, "v_{max} = A·ω ≈ 26 cm/s", 46, INK, alpha=appear(t, M[1] + 0.6, 0.45))
    k3 = appear(t, M[2] - 0.05, 0.4)               # chua noi duoc (phu de 3, >= 4 s)
    if k3 > 0:
        card(d, (60, 1240, 1020, 1540), fill=A(WHITE, k3), outline=A(NAVY, k3), r=24, w=4)
        text(d, (W / 2, 1295), "Chưa nói được", 44, NAVY, alpha=k3)
        for j, l1 in enumerate(("• Góc lớn: chưa thử", "• Dây khác: chưa đo")):
            text(d, (110, 1380 + j * 80), l1, 44, INK, anchor="lm", alpha=k3 * appear(t, M[2] + 0.2 + 0.4 * j, 0.4))

# ---------------- canh 4: Bay - bien nay sang bien kia ----------------
BP = (540, 330)                                   # diem treo canh bay (giua man)
SLOW = 2.0                                        # quay cham x2
B1, B2 = 0.4, None
def bay_tau(t, sc):
    M = sc["M"]; h = T_MO / 2
    if t < B1: return 0.0
    if t < B1 + h * SLOW: return (t - B1) / SLOW
    if t < M[1]: return h
    if t < M[1] + h * SLOW: return h + (t - M[1]) / SLOW
    return T_MO

def s_bay(img, d, t, sc):
    M = sc["M"]; h = T_MO / 2
    tau = bay_tau(t, sc)
    ybob = BP[1] + math.sqrt(L_PX ** 2 - A_PX ** 2)
    for s in (-1, 1):                              # vach bien trai/phai (net dut)
        for yy in range(int(ybob) - 60, int(ybob) + 150, 24):
            d.line([(BP[0] + s * A_PX, yy), (BP[0] + s * A_PX, yy + 12)], fill=GRAY, width=3)
    text(d, (BP[0] - A_PX - 18, ybob + 120), "biên", 46, MUTED, anchor="rm")
    text(d, (BP[0] + A_PX + 18, ybob + 120), "biên", 46, MUTED, anchor="lm")
    pendulum(d, xpx(tau), piv=BP)
    card(d, (40, 960, 336, 1026), fill=TEAL, r=33); text(d, (188, 993), "quay chậm ×2", 40, WHITE)
    ya = 410                                       # mui ten hai nua chu ki, hien cung luc nhan
    if t >= B1 + h * SLOW:
        arrow(d, (BP[0] + A_PX + 10, ya), (BP[0] - A_PX - 10, ya), ORANGE, w=5, head=18)
        text(d, (BP[0] - A_PX - 30, ya), "nửa chu kì", 46, ORANGE, anchor="rm")
    if t >= M[1] + h * SLOW:
        arrow(d, (BP[0] - A_PX - 10, ya + 70), (BP[0] + A_PX + 10, ya + 70), BLUE, w=5, head=18)
        text(d, (BP[0] + A_PX + 30, ya + 70), "nửa chu kì", 46, BLUE, anchor="lm")
    a1 = appear(t, 0.0, 0.3); y0 = 1110
    card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(DRED, a1), r=32)
    text(d, (W / 2, y0 + 60), "BẪY", 38, WHITE, alpha=a1)
    q = "“Biên → biên là 1 dao động”"
    f = F(48); lw = tw(d, q, f); yy = y0 + 180
    text(d, (W / 2, yy), q, 48, DRED, alpha=a1)
    ks = clamp((t - (B1 + h * SLOW)) / 0.4)        # gach khi nua chu ki dau xong
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=(140, 15, 15), width=7)
    kc = appear(t, M[1] + h * SLOW, 0.4)           # ket luan hien cung luc mui ten nua chu ki thu hai
    ctext(d, y0 + 330, "✓ 1 dao động: về chỗ thả", 46, DGREEN, maxw=940, alpha=kc)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
EP = (540, 1000); EL = 200
def end_body(d, t, k1):
    sc = END[0]; M = sc["M"]
    kq = appear(t, M[0] + 0.4, 0.5)
    if kq > 0:                                     # hinh: 2 hang x 10 cham = 20 dao dong, so 10 / 20 o cuoi hang
        for r, (col, lab) in enumerate(((ORANGE, "10"), (BLUE, "20"))):
            y = 1060 + r * 100
            for k in range(10): dot(d, 230 + k * 56, y, 17, A(col, kq))
            text(d, (790, y), lab, 48, col, anchor="lm", alpha=kq)
    kh = appear(t, M[0] + 0.4 + 2.5, 0.5)
    if kh > 0:
        card(d, (110, 1330, 970, 1560), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1385, "Gợi ý", 40, INK, alpha=kh)
        ctext(d, 1480, "Bấm tay mấy lần mỗi lượt?", 44, ORANGE, maxw=820, alpha=kh)

END = []
def s_end(img, d, t, sc):
    END[:] = [sc]
    chot_hoi(d, t, sc, "Đếm nhiều dao động,\nsai số nhỏ", "Bấm 20 dao động thay vì 10.\nSai số T đổi thế nào?", None, end_body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (do["t0"] + 0.15, "ding"), (do["t0"] + REL, "tap")]
    out += [(do["t0"] + REL + RT + 0.3 * j, "tick") for j in range(5)]
    out += [(do["t0"] + U_STOP, "tap")]
    out += [(do["t0"] + do["M"][1] + 0.2 + 0.5 * k, "tick") for k in range(4)]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-baitapdaodong-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Dao động điều hoà · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Chùm chìa khoá treo dây", draw=s_hook, tail=0.8, caps=[
   ("Dây 36 cm, kéo lệch 5 cm.", 3.4),
   ("Tự đoán trước khi xem tiếp.", 5.2)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.7, caps=[
   ("Lần 1: đếm đủ 10 dao động.", 4.8),
   ("Lặp thêm 4 lần, ghi lại.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Lệch do tay bấm, không do dây.", 3.8),
   ("Từ T tính tiếp tốc độ cực đại.", 3.8),
   ("Mới thử một dây, góc nhỏ.", 4.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.6, caps=[
   ("Bẫy: biên này sang biên kia.", 3.4),
   ("Phải quay về đúng chỗ thả.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 6.6)]),
])
