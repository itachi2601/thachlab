# Clip: tn-l9-taitao-01 - Tua-bin gio mo hinh truoc quat ban (KHTN 9 Bai 17, lesson 95; 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-taitao-01.json:
#   so_lieu_mau (v m/s; U lan 1, 2, 3; U tb V; P W): 2,0 0,57 0,62 0,61 0,60 0,036 ; 3,0 1,18 1,23 1,19 1,20 0,144 ;
#   4,0 1,76 1,85 1,79 1,80 0,324.  tham_so: R = 10 Ω, v0 = 1,0 m/s (gio toi thieu de canh quay), k = 0,6.
#   an_toan: khong tho tay vao canh quat dang quay. hien_tuong_hay_sai[0] = Du doan, [2] = bay (doc mot lan).
# Cau Tu kiem tra cua bai: Cau 2 hoi P tang bao nhieu lan khi gio 2 -> 4 m/s (dap an 9) -> clip KHONG hien P o 4 m/s,
#   khong noi "gap 9" (kho rut_ra[1] + ket_qua_ky_vong noi dung dap an nay). Cau 3 (19 gio, nguon nao khong phat) ->
#   clip khong noi ban dem. Thu thach * (chuoi chuyen hoa dien gio) -> clip khong viet chuoi dong nang -> co nang -> dien.
# Du doan (K10): gio 2 -> 3 m/s (gap 1,5) thi U gap may lan? -> gap 2 (0,60 -> 1,20 V).
# Cau chot: gio 1 m/s, von ke chi khoang bao nhieu? -> 0 V (keo dai duong qua 3 diem; tham_so v0 = 1,0 m/s).
#   Do thi chi ve doan 2 -> 4 m/s, khong keo dai, khong ghi v0 tren man.
# Dung lai theo cong moi 27/11/2026 (Viec 4 L9 nhom C): chu >= 56, canh <= 180 tu/phut, khoi chu cach >= 2,5 s.
#   Bo goi y "Keo dai duong qua ba diem do" (neu san cach lam) va phu de "Duong thang khong qua goc" (goi san ca chot).
import math
from engine import *

ROWS = [(2.0, (0.57, 0.62, 0.61), 0.60, 0.036), (3.0, (1.18, 1.23, 1.19), 1.20, 0.144), (4.0, (1.76, 1.85, 1.79), 1.80, 0.324)]
R_TAI, V0, K_MP = 10.0, 1.0, 0.6
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

METAL = (214, 218, 228); BLADE = (96, 165, 250); AIR = (125, 211, 252); DGREEN = (21, 110, 55); DRED = (185, 28, 28)
SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30); BODY = (70, 78, 100)

# ---------------- dung cu ----------------
FX, FY, HX, HY = 190, 560, 560, 520          # tam quat ban ; truc tua-bin
def desk_fan(d, on):
    d.rectangle([FX - 14, FY + 120, FX + 14, 880], fill=METAL, outline=NAVY, width=3)
    d.ellipse([FX - 90, 870, FX + 90, 910], fill=METAL, outline=NAVY, width=4)
    d.ellipse([FX - 120, FY - 120, FX + 120, FY + 120], fill=A((226, 232, 240), 0.8), outline=NAVY, width=5)
    for r in (40, 80): d.ellipse([FX - r, FY - r, FX + r, FY + r], outline=GRAY, width=2)
    d.line([(FX - 120, FY), (FX + 120, FY)], fill=GRAY, width=2); d.line([(FX, FY - 120), (FX, FY + 120)], fill=GRAY, width=2)
    dot(d, FX, FY, 22, NAVY)

def wind(d, t, v, alpha=1.0):
    if v <= 0: return
    for j, dy in enumerate((-80, -20, 40, 100)):
        ph = (t * v * 0.35 + j * 0.27) % 1.0
        x0 = FX + 140 + ph * 140
        d.line([(x0, FY - 40 + dy), (x0 + 60, FY - 40 + dy)], fill=A(AIR, alpha * (1 - ph * 0.6)), width=6)

def turbine(d, ang):
    d.rectangle([HX - 10, HY + 20, HX + 10, 880], fill=METAL, outline=NAVY, width=3)            # cot
    d.rectangle([HX - 70, 870, HX + 70, 900], fill=METAL, outline=NAVY, width=3)
    d.rounded_rectangle([HX - 28, HY - 26, HX + 60, HY + 26], radius=10, fill=BODY)              # dong co = may phat
    for k in range(3):
        a = ang + k * 2 * math.pi / 3
        tip = (HX + 170 * math.cos(a), HY + 170 * math.sin(a))
        sd = (-math.sin(a) * 26, math.cos(a) * 26)
        d.polygon([(HX + sd[0] * 0.4, HY + sd[1] * 0.4), (tip[0] + sd[0] * 0.5, tip[1] + sd[1] * 0.5), tip,
                   (HX - sd[0] * 0.4, HY - sd[1] * 0.4)], fill=BLADE, outline=NAVY)
    dot(d, HX, HY, 20, NAVY)

def meter(d, val, sub=None, alpha=1.0):
    # dien tro 10 Ω + von ke so mac song song (day tu chan tua-bin)
    d.line([(HX + 60, HY), (760, HY), (760, 700)], fill=(60, 66, 92), width=5)
    d.line([(HX + 70, 885), (980, 885), (980, 700)], fill=(60, 66, 92), width=5)
    d.rectangle([740, 700, 1000, 760], fill=WHITE, outline=NAVY, width=4)
    text(d, (870, 730), f"{int(R_TAI)} Ω", 56, NAVY)
    card(d, (720, 300, 1020, 520), fill=BODY, r=22)
    text(d, (870, 346), "vôn kế", 56, WHITE)
    card(d, (745, 395, 995, 495), fill=SCREEN, r=12)
    text(d, (870, 445), val, 56, SCR_INK)
    d.line([(760, 520), (760, 700)], fill=(60, 66, 92), width=4); d.line([(980, 520), (980, 700)], fill=(60, 66, 92), width=4)

def rig(d, t, ang, v, val, sub=None):
    card(d, (40, 262, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    d.line([(60, 910), (1020, 910)], fill=(180, 170, 150), width=4)
    desk_fan(d, v > 0); wind(d, t, v); turbine(d, ang); meter(d, val, sub)
    if v > 0:
        card(d, (60, 290, 420, 380), fill=(224, 242, 254), outline=BLUE, r=20, w=3)
        text(d, (240, 335), f"gió {vn(v)} m/s", 56, BLUE)

def pill(d, s, y, a, color, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, t, 2.2 * t, 2.0, vn(ROWS[0][2], 2) + " V")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1000 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 480), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    text(d, (W / 2, y0 + 165), "Gió tăng 2 → 3 m/s.", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 250), "U gấp mấy lần?", 58, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 340, 970, y0 + 430], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 340, 110 + max(90, 860 * (1 - p)), y0 + 430], radius=45, fill=A((76, 29, 149), a))

# ---------------- canh 2: Tien hanh ----------------
T_P = (0.6, 2.8, 5.0)            # bat dau moi muc gio
T_R = (0.35, 0.75, 1.15)         # ba lan doc trong moi muc
T_AVG = 1.55                     # hang bang (U trung binh) hien
def omega(u): return 1.5 + 6.0 * u            # toc do quay minh hoa, tang theo U (khong ghi so)
def do_state(t):
    """-> (muc j hoac -1, chuoi so chi, chu phu, so hang da ghi, goc canh)."""
    j = sum(1 for tp in T_P if t >= tp) - 1
    n = sum(1 for tp in T_P if t >= tp + T_AVG)
    ang = 0.0; prev = 0.0
    for i, tp in enumerate(T_P):                  # tich phan goc quay tung doan
        if t <= tp: break
        end = T_P[i + 1] if i + 1 < len(T_P) else 1e9
        ang += omega(ROWS[i][2]) * (min(t, end) - tp)
    if j < 0: return -1, "0,00 V", None, 0, 0.0
    dt = t - T_P[j]; reads = ROWS[j][1]
    r = sum(1 for x in T_R if dt >= x) - 1
    if r < 0: return j, "…", None, n, ang
    return j, vn(reads[r], 2) + " V", None, n, ang      # khong dem "lan 1/2/3" (de bay "doc mot lan" khong bi bac truoc)

XS = (300, 760)
def table(d, n, y=990, hl=None):
    card(d, (40, y, 1040, y + 420), fill=WHITE, outline=LIGHT, w=3)
    for x, h in zip(XS, ("gió (m/s)", "U (V)")): text(d, (x, y + 55), h, 56, NAVY)
    d.line([(70, y + 100), (1010, y + 100)], fill=LIGHT, width=3)
    for j, (v, _, u, _) in enumerate(ROWS):
        yy = y + 160 + j * 92
        if hl == j: d.rounded_rectangle([60, yy - 40, 1020, yy + 40], radius=20, fill=(255, 237, 213))
        if j < n:
            text(d, (XS[0], yy), vn(v), 56, BLUE); text(d, (XS[1], yy), vn(u, 2), 56, NAVY)

def s_do(img, d, t, sc):
    j, val, sub, n, ang = do_state(t)
    rig(d, t, ang, ROWS[j][0] if j >= 0 else 0.0, val, sub)
    if j < 0:                                     # nhan gio hien du tu t=0 (khoi chu dau canh)
        card(d, (60, 290, 420, 380), fill=(224, 242, 254), outline=BLUE, r=20, w=3)
        text(d, (240, 335), f"gió {vn(ROWS[0][0])} m/s", 56, BLUE)
    table(d, n, hl=(n - 1 if n > 0 else None))
    card(d, (40, 1450, 1040, 1530), fill=(255, 247, 237), outline=ORANGE, r=24, w=3)
    text(d, (W / 2, 1490), "Không thò tay vào cánh quay", 56, (154, 52, 18))

def _kiem_dong_bo():
    """moi 0,05 s: so chi dang hien phai la mot lan doc cua muc dang dat; hang bang khong vuot muc dang dat."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        j, val, sub, n, ang = do_state(t)
        if n > j + 1: bad.append((round(t, 2), "hang vuot", j, n))
        if j >= 0 and val not in ("…",) + tuple(vn(x, 2) + " V" for x in ROWS[j][1]): bad.append((round(t, 2), val))
        t += 0.05
    return bad

# ---------------- canh 3: Dap an + do thi U theo v ----------------
GX0, GX1, GY0, GY1 = 180, 960, 1200, 700        # truc: v 0..5 m/s ; U 0..2 V
def gx(v): return GX0 + (GX1 - GX0) * v / 5
def gy(u): return GY0 - (GY0 - GY1) * u / 2
def axes(d, a=1.0, y0=580, y1=1330, x0=40, x1=1040):
    card(d, (x0, y0, x1, y1), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    d.line([(GX0, GY1 - 50), (GX0, GY0)], fill=A(NAVY, a), width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=A(NAVY, a), width=4)
    text(d, (GX0 + 24, GY1 - 60), "U (V)", 56, NAVY, anchor="lm", alpha=a)
    text(d, (GX1 + 40, GY0 - 50), "m/s", 56, NAVY, anchor="rm", alpha=a)
    for v in range(0, 6):
        d.line([(gx(v), GY0), (gx(v), GY0 + 12)], fill=A(NAVY, a), width=3); text(d, (gx(v), GY0 + 50), str(v), 56, INK, alpha=a)
    for u in (1, 2):
        d.line([(GX0 - 12, gy(u)), (GX0, gy(u))], fill=A(NAVY, a), width=3); text(d, (GX0 - 26, gy(u)), str(u), 56, INK, anchor="rm", alpha=a)
def points(d, k=1.0):
    for j, (v, _, u, _) in enumerate(ROWS):
        kk = clamp(k * 3 - j)
        if kk <= 0: continue
        dot(d, gx(v), gy(u), 14, A(ORANGE, kk))
        text(d, (gx(v) - 26, gy(u) - 44), vn(u, 2), 56, ORANGE, anchor="rm", alpha=kk)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN: U gấp 2", 320, 1.0, GREEN, 58)
    text(d, (W / 2, 420), f"{vn(ROWS[0][2], 2)} V  →  {vn(ROWS[1][2], 2)} V", 58, NAVY)
    text(d, (W / 2, 505), "gió × 1,5  nhưng  U × 2", 56, ORANGE)
    axes(d)
    seg = appear(t, M[1] + 0.6, 0.8)
    if seg > 0:
        v1 = 2 + 2 * seg
        d.line([(gx(2), gy(ROWS[0][2])), (gx(v1), gy(ROWS[0][2] + (ROWS[2][2] - ROWS[0][2]) * seg))], fill=A(BLUE, 0.6), width=5)
    k = appear(t, 1.8, 0.4)
    if k > 0:                                     # vong nhip quanh hai diem dang so
        for v, _, u, _ in ROWS[:2]:
            rr = 34 + 26 * (0.5 + 0.5 * math.sin(2 * math.pi * t / 1.6))
            d.ellipse([gx(v) - rr, gy(u) - rr, gx(v) + rr, gy(u) + rr], outline=A(ORANGE, k), width=8)
    points(d, appear(t, 0.6, 1.2))

# ---------------- canh 4: Rut ra (dinh tinh: P tang nhanh hon U; KHONG so P, KHONG cong thuc - tranh lo cach giai Cau 2) ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 270, 1040, 400), fill=(236, 253, 243), outline=GREEN, w=5)
    text(d, (W / 2, 335), f"gió {vn(ROWS[0][0])} → {vn(ROWS[1][0])} m/s", 58, DGREEN)
    base, unit = 1060, 140
    for j in range(2):
        v, _, u, p = ROWS[j]
        cx = 300 + j * 480
        g = ease((t - 0.4 - 0.9 * j) / 0.7)
        for dx, val, ref, col, lab in ((-85, u, ROWS[0][2], NAVY, "U"), (85, p, ROWS[0][3], ORANGE, "P")):
            h = unit * val / ref * g
            if h > 2: d.rectangle([cx + dx - 60, base - h, cx + dx + 60, base], fill=col)
            text(d, (cx + dx, base + 50), lab, 56, col)
        text(d, (cx, base + 130), f"gió {vn(v)} m/s", 56, INK)
    d.line([(100, base), (980, base)], fill=NAVY, width=4)
    k2 = appear(t, M[1] + 0.1, 0.45)
    card(d, (40, 1260, 1040, 1410), fill=A((255, 247, 237), k2), outline=A(ORANGE, k2), w=5)
    text(d, (W / 2, 1335), "P tăng nhanh hơn U", 58, (154, 52, 18), alpha=k2)

# ---------------- canh 5: Bay (doc mot lan) roi Chua noi duoc ----------------
BAY_ST = 2.2
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[2] - 0.1, 0.45); a1 = 1 - k2
    v, reads, u, _ = ROWS[2]
    card(d, (40, 262, 1040, 600), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 330), f"gió {vn(v)} m/s", 58, BLUE)
    for i, r in enumerate(reads):
        kk = appear(t, 0.3 + 1.0 * i, 0.3)
        x = 230 + i * 310
        card(d, (x - 130, 410, x + 130, 530), fill=A(SCREEN, max(0.25, kk)), r=14)
        text(d, (x, 470), vn(r, 2), 64, SCR_INK, alpha=kk)
    y0 = 640
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 640), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y0 + 62, a1, DRED)
        for j, q in enumerate(("“Đọc vôn kế", "một lần là đủ”")):
            yy = y0 + 170 + j * 80; lw = tw(d, q, F(58))
            text(d, (W / 2, yy), q, 58, INK, alpha=a1)
            ks = clamp((t - BAY_ST) / 0.4)
            if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=7)
        kk = a1 * appear(t, M[1] + 0.1, 0.4)
        card(d, (70, y0 + 320, 1010, y0 + 580), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 400), f"✓ Lệch tới {vn(max(reads) - min(reads), 2)} V:", 58, DGREEN, alpha=kk)
        text(d, (W / 2, y0 + 490), f"lấy trung bình {vn(u, 2)} V", 58, DGREEN, alpha=kk)
    if k2 > 0:
        card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 110), "Chưa nói được:", 60, NAVY, alpha=k2)
        text(d, (W / 2, y0 + 220), "tua-bin thật?", 58, INK, alpha=k2)
        text(d, (W / 2, y0 + 320), "(số minh hoạ)", 56, NAVY, alpha=k2)

# ---------------- canh 6: Chot ----------------
END_Q = 0.2
CH_V = 1.0                                        # cau chot: gio 1 m/s (dap so 0 V khong hien)
def s_end(img, d, t, sc):
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 280, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 340, k1, ORANGE)
    text(d, (W / 2, 425), "Gió chỉ còn " + vn(CH_V, 0) + " m/s.", 58, INK, alpha=k1)
    text(d, (W / 2, 505), "Vôn kế chỉ khoảng bao nhiêu?", 58, INK, alpha=k1)
    if k1 <= 0: return
    axes(d, k1, y0=600, x0=70, x1=1010)            # GĐ2: khung do thi khong cham vien cam
    points(d, k1)
    rr = 62 + 32 * math.sin(2 * math.pi * t / 2.0)
    xc, yc = 820, 1400
    d.ellipse([xc - rr, yc - rr, xc + rr, yc + rr], fill=A(mix(ORANGE, WHITE, 0.45), k1))
    text(d, (xc, yc), "?", 80, WHITE, alpha=k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    out += [(do["t0"] + tp, "tap") for tp in T_P]
    out += [(da["t0"] + 0.2, "ding"), (r["t0"] + r["M"][1] + 0.1, "tap"), (b["t0"] + BAY_ST, "buzz"),
            (b["t0"] + b["M"][1] + 0.1, "tap"), (e["t0"] + END_Q + 0.1, "open")]
    return sorted(out)

CLIP = dict(id="tn-l9-taitao-01", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Năng lượng tái tạo · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Tua-bin gió trước quạt bàn", draw=s_hook, tail=0.3, caps=[
   ("Cánh quay máy phát nhỏ.", 2.5),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Đo gió ngay trước cánh.", 3.4),
   ("Đọc vôn kế ở mỗi mức gió.", 3.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("So hai số trung bình.", 3.0),
   ("Ba điểm thẳng hàng.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.4, caps=[
   ("Công suất điện trên điện trở.", 3.2),
   ("Còn tăng nhanh hơn U.", 3.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 4.2),
   ("Nhìn ba số đọc.", 3.4),
   ("Còn bỏ ngỏ.", 2.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Tự nghĩ.", 6.2)]),
])

def _kiem_so():
    import json, os
    bad = []
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "content", "thi-nghiem", "tn-l9-taitao-01.json")
    k = json.load(open(p)); ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    kho = [(r[0], tuple(r[1:4]), r[4], r[5]) for r in k["so_lieu_mau"]["hang"]]
    if kho != ROWS: bad.append("so_lieu_mau")
    if (ts["R"]["gia_tri"], ts["v0"]["gia_tri"], ts["k"]["gia_tri"]) != (R_TAI, V0, K_MP): bad.append("tham_so")
    for v, rd, u, pw in ROWS:
        if abs(sum(rd) / 3 - u) > 1e-9: bad.append(("tb", v))
        if abs(u * u / R_TAI - pw) > 1e-9: bad.append(("P", v))
        if abs(K_MP * (v - V0) - u) > 1e-9: bad.append(("mo hinh", v))
    if round(ROWS[1][2] / ROWS[0][2], 6) != 2 or round(ROWS[1][3] / ROWS[0][3], 6) != 4: bad.append("ti le 2->3")
    if abs(max(ROWS[2][1]) - min(ROWS[2][1]) - 0.09) > 1e-9: bad.append("lech 0,09")
    if max(0.0, K_MP * (CH_V - V0)) != 0: bad.append("cau chot")
    return bad

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch kho/mô hình:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
