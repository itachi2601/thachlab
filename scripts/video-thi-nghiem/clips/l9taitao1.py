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
    text(d, (870, 730), f"{int(R_TAI)} Ω", 40, NAVY)
    card(d, (720, 330, 1020, 520), fill=BODY, r=22)
    text(d, (870, 362), "vôn kế", 40, WHITE, bold=False)
    card(d, (745, 395, 995, 495), fill=SCREEN, r=12)
    text(d, (870, 445), val, 56, SCR_INK)
    d.line([(760, 520), (760, 700)], fill=(60, 66, 92), width=4); d.line([(980, 520), (980, 700)], fill=(60, 66, 92), width=4)
    if sub: text(d, (870, 565), sub, 38, MUTED, bold=False, alpha=alpha)

def rig(d, t, ang, v, val, sub=None):
    card(d, (40, 262, 1040, 960), fill=WHITE, outline=LIGHT, w=3)
    d.line([(60, 910), (1020, 910)], fill=(180, 170, 150), width=4)
    desk_fan(d, v > 0); wind(d, t, v); turbine(d, ang); meter(d, val, sub)
    if v > 0:
        card(d, (FX - 120, 300, FX + 190, 370), fill=(224, 242, 254), outline=BLUE, r=20, w=3)
        text(d, (FX + 35, 335), f"gió {vn(v)} m/s", 40, BLUE)

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.7
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, t, 2.2 * t, 2.0, vn(ROWS[0][2], 2) + " V")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 500), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 260, "Gió tăng từ 2 lên 3 m/s\n(gấp 1,5 lần).\nU gấp mấy lần?", 52, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 450, 940, y0 + 462], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 450, 140 + 800 * (1 - p), y0 + 462], radius=6, fill=A(PURPLE, a))

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
def table(d, n, y=1000, hl=None):
    card(d, (40, y, 1040, y + 420), fill=WHITE, outline=LIGHT, w=3)
    for x, h in zip(XS, ("gió (m/s)", "U (V)")): text(d, (x, y + 55), h, 42, INK)
    d.line([(70, y + 100), (1010, y + 100)], fill=LIGHT, width=3)
    for j, (v, _, u, _) in enumerate(ROWS):
        yy = y + 160 + j * 92
        if hl == j: d.rounded_rectangle([60, yy - 40, 1020, yy + 40], radius=20, fill=(255, 237, 213))
        if j < n:
            text(d, (XS[0], yy), vn(v), 46, BLUE); text(d, (XS[1], yy), vn(u, 2), 46, NAVY)
        else:
            for x in XS: text(d, (x, yy), "·", 44, GRAY)

def s_do(img, d, t, sc):
    j, val, sub, n, ang = do_state(t)
    rig(d, t, ang, ROWS[j][0] if j >= 0 else 0.0, val, sub)
    table(d, n, hl=(n - 1 if n > 0 else None))
    card(d, (40, 1450, 1040, 1530), fill=(255, 247, 237), outline=ORANGE, r=24, w=3)
    text(d, (W / 2, 1490), "An toàn: không thò tay vào cánh quay", 40, (154, 52, 18))

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
GX0, GX1, GY0, GY1 = 160, 980, 1180, 640        # truc: v 0..5 m/s ; U 0..2 V
def gx(v): return GX0 + (GX1 - GX0) * v / 5
def gy(u): return GY0 - (GY0 - GY1) * u / 2
def graph(d, k=1.0, seg=1.0):
    card(d, (40, 560, 1040, 1300), fill=WHITE, outline=LIGHT, w=3)
    d.line([(GX0, GY1 - 30), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 20, GY0)], fill=NAVY, width=4)
    text(d, (GX0 + 20, GY1 - 40), "U (V)", 40, NAVY, anchor="lm")
    text(d, (GX1, GY0 + 80), "gió (m/s)", 40, NAVY, anchor="rm")
    for v in range(0, 6):
        d.line([(gx(v), GY0), (gx(v), GY0 + 12)], fill=NAVY, width=3); text(d, (gx(v), GY0 + 40), str(v), 38, INK)
    for u in (1, 2):
        d.line([(GX0 - 12, gy(u)), (GX0, gy(u))], fill=NAVY, width=3); text(d, (GX0 - 24, gy(u)), str(u), 38, INK, anchor="rm")
    if seg > 0:
        v1 = 2 + 2 * seg
        d.line([(gx(2), gy(ROWS[0][2])), (gx(v1), gy(ROWS[0][2] + (ROWS[2][2] - ROWS[0][2]) * seg))], fill=A(BLUE, 0.6), width=5)
    for j, (v, _, u, _) in enumerate(ROWS):
        kk = clamp(k * 3 - j)
        if kk <= 0: continue
        dot(d, gx(v), gy(u), 13, A(ORANGE, kk))
        text(d, (gx(v) - 24, gy(u) - 40), vn(u, 2), 40, ORANGE, anchor="rm", alpha=kk)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · U gấp 2"
    pw = tw(d, lab, F(46)) + 60
    card(d, (W / 2 - pw / 2, 270, W / 2 + pw / 2, 350), fill=A(NAVY, ka), r=38)
    text(d, (W / 2, 310), lab, 46, WHITE, alpha=ka)
    k1 = appear(t, 0.5, 0.4)
    text(d, (W / 2, 420), f"{vn(ROWS[0][2], 2)} V  →  {vn(ROWS[1][2], 2)} V", 52, NAVY, alpha=k1)
    text(d, (W / 2, 495), "gió × 1,5   nhưng   U × 2", 46, ORANGE, alpha=appear(t, 1.2, 0.4))
    graph(d, k=appear(t, M[1] - 0.3, 0.9), seg=appear(t, M[1] + 0.6, 0.8))

# ---------------- canh 4: Rut ra (dinh tinh: P tang nhanh hon U; KHONG so P, KHONG cong thuc - tranh lo cach giai Cau 2) ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 270, 1040, 400), fill=(236, 253, 243), outline=GREEN, w=5)
    text(d, (W / 2, 335), f"gió {vn(ROWS[0][0])} → {vn(ROWS[1][0])} m/s", 50, DGREEN)
    base, unit = 1100, 140                              # chieu cao luc gio 2 m/s (U va P cung quy ve 1 don vi)
    for j in range(2):
        v, _, u, p = ROWS[j]
        cx = 300 + j * 480
        g = ease((t - 0.6 - 0.9 * j) / 0.7)
        for dx, val, ref, col, lab in ((-85, u, ROWS[0][2], NAVY, "U"), (85, p, ROWS[0][3], ORANGE, "P")):
            h = unit * val / ref * g
            if h > 2: d.rectangle([cx + dx - 60, base - h, cx + dx + 60, base], fill=col)
            text(d, (cx + dx, base + 45), lab, 44, col)
        text(d, (cx, base + 115), f"gió {vn(v)} m/s", 42, INK)
    d.line([(100, base), (980, base)], fill=NAVY, width=4)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        card(d, (40, 1290, 1040, 1440), fill=A((255, 247, 237), k2), outline=A(ORANGE, k2), w=5)
        text(d, (W / 2, 1365), "P tăng nhanh hơn U", 54, (154, 52, 18), alpha=k2)

# ---------------- canh 5: Bay (doc mot lan) roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.1, 0.4) * (1 - k2)
    v, reads, u, _ = ROWS[2]
    card(d, (40, 262, 1040, 760), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 330), f"gió {vn(v)} m/s, đọc ba lần", 44, BLUE)
    for i, r in enumerate(reads):
        kk = appear(t, 0.3 + 0.35 * i, 0.3)
        x = 230 + i * 310
        card(d, (x - 120, 400, x + 120, 500), fill=A(SCREEN, kk), r=14)
        text(d, (x, 450), vn(r, 2), 52, SCR_INK, alpha=kk)
    kv = appear(t, M[0] + 2.2, 0.4)
    text(d, (W / 2, 580), f"lệch nhau tới {vn(max(reads) - min(reads), 2)} V", 44, DRED, alpha=kv)
    text(d, (W / 2, 670), f"trung bình {vn(u, 2)} V", 48, DGREEN, alpha=kv)
    if a1 > 0:
        y0 = 820
        card(d, (40, y0, 1040, y0 + 320), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 60), "BẪY", 40, WHITE, alpha=a1)
        q = "“Đọc vôn kế một lần là đủ”"
        ks = clamp((t - M[0] - 2.2) / 0.4)
        f = F(46); lw = tw(d, q, f); yy = y0 + 200
        text(d, (W / 2, yy), q, 46, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
            text(d, (W / 2 + lw / 2 + 40, yy), "✗", 46, DRED, alpha=a1 * ks)
    if k2 > 0:
        y0 = 820 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 320), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 75), "Chưa nói được", 46, NAVY, alpha=k2)
        kk = k2 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y0 + 190), "Tua-bin đồ chơi, số minh hoạ", 46, INK, alpha=kk)

# ---------------- canh 6: Chot + cau hoi ----------------
HINT_AT = 4.4
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 262, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 391, "Điện gió phụ thuộc mạnh vào gió", 50, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 580, 1040, 1420), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 610, W / 2 + pw / 2, 676), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 643), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    # ve lai 3 diem do (KHONG ve duong noi / doan keo dai)
    x0, x1, yb, yt = 200, 860, 1000, 720                 # v 0..5 m/s ; U 0..2 V
    px = lambda v: x0 + (x1 - x0) * v / 5
    py = lambda u: yb - (yb - yt) * u / 2
    d.line([(x0, yt - 20), (x0, yb)], fill=A(NAVY, kq), width=4); d.line([(x0, yb), (x1 + 20, yb)], fill=A(NAVY, kq), width=4)
    text(d, (x0 + 18, yt - 20), "U (V)", 40, NAVY, anchor="lm", alpha=kq)
    text(d, (x1 + 40, yb), "m/s", 40, NAVY, anchor="lm", alpha=kq)
    for v in range(0, 6):
        d.line([(px(v), yb), (px(v), yb + 10)], fill=A(NAVY, kq), width=3); text(d, (px(v), yb + 36), str(v), 38, INK, alpha=kq)
    for v, _, u, _ in ROWS:
        dot(d, px(v), py(u), 12, A(ORANGE, kq))
        text(d, (px(v) - 22, py(u) - 34), vn(u, 2), 40, ORANGE, anchor="rm", alpha=kq)
    ctext(d, 1120, "Gió chỉ còn 1 m/s.\nVôn kế chỉ khoảng bao nhiêu?", 48, INK, maxw=920, alpha=kq)
    kh = appear(t, M[0] + HINT_AT, 0.5)
    if kh > 0:
        card(d, (110, 1230, 970, 1390), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1310, "Kéo dài đường qua ba điểm đo", 44, ORANGE, maxw=840, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding")]
    out += [(do["t0"] + tp, "tap") for tp in T_P]
    out += [(do["t0"] + tp + x, "tick") for tp in T_P for x in T_R]
    out += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + 0.1, "buzz"),
            (b["t0"] + b["M"][0] + 2.2, "tap"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l9-taitao-01", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Năng lượng tái tạo · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Tua-bin gió trước quạt bàn", draw=s_hook, tail=0.8, caps=[
   ("Cánh quay máy phát nhỏ.", 3.0),
   ("Tự trả lời trước khi xem.", 5.7)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Đo gió ngay trước cánh.", 3.4),
   ("Đọc vôn kế ở mỗi mức gió.", 4.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("So hai số trung bình.", 3.0),
   ("Đường thẳng không qua gốc.", 3.8)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Công suất điện trên điện trở.", 3.2),
   ("Còn tăng nhanh hơn U.", 3.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Kim vôn kế dao động.", 3.8),
   ("Còn chưa nói được.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Tự nghĩ, rồi xem gợi ý.", 6.4)]),
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
    if max(0.0, K_MP * (1.0 - V0)) != 0: bad.append("cau chot")
    return bad

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch kho/mô hình:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
