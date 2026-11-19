# Clip: tn-l9-modau-01 - Do mot dong dien o ba thang cua dong ho da nang (KHTN 9, bai 128, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-modau-01.json:
#   tham_so: I that 0,15318 A; GHD 10 / 0,2 / 0,02 A. mo_hinh: buoc 10 A -> 0,01 A; 200 mA -> 0,1 mA; 20 mA -> 0,01 mA;
#   I > GHD -> hien "1" ben trai. so_lieu_mau: 10 A "0.15" (0,15 A); 200 mA "153.2" (153,2 mA); 20 mA "1 (ben trai)" (qua thang).
#   dung_cu: nguon 3 V, bong den nho, khoa K. quan_sat: den sang nhu nhau ca ba lan. bay = hien_tuong_hay_sai[2] (doc 153,2 A).
#   chua noi duoc = so_lieu_mau.ghi_chu + mo_hinh.gia_thiet[1] (bo qua dien tro dong ho).
# Bai 128: ngay sau hop la Cau 2 ("Nen ghi ket qua nao vao bao cao?" -> 153,2 mA vi nhieu chu so): clip KHONG noi thang nao
#   "chinh xac", "nhieu chu so nhat", "nen ghi", khong tinh sai so % (rut_ra[1] cua kho bo qua co y). Cau 5, Cau 7 (chon thang):
#   clip khong noi quy tac chon thang. Mo bai (so 1 ben trai = qua thang) da hoi o dau bai -> clip chi ghi "qua thang".
# Du doan (K10: chi cau hoi + hinh): "Thang 10 A: 0,15 A. Chuyen sang thang 200 mA, man hinh hien gi?" -> 153.2.
# Vong 2: bo cot "Doc ra" (trung phuong an Cau 2), Bay dat TRUOC Rut ra, bo "(khong phai 1 mA)" (Cau 2 C).
# Cau chot: dong khoang 60 mA (minh hoa, ghi vao kho) -> thang nao doc duoc nhieu chu so nhat? (200 mA: "60.0";
#   20 mA qua thang; 10 A "0.06"). Khong trung Cau 7 (15 mA -> 20 mA), khong trung Tra bai 4.
# Mach kin: nguon 3 V (+) -> K -> den -> que do -> dong ho -> COM -> que den -> (-) nguon. Dong ho noi tiep den.
import math
from engine import *

I_TRUE = 0.15318                                 # tham_so I mac_dinh (A)
I_HOI = 0.060                                    # cau chot (minh hoa, ghi trong so_lieu_mau.ghi_chu)
SCALES = [("10 A", 10.0), ("200 mA", 0.2), ("20 mA", 0.02)]   # tham_so GHD
ROWS = [("10 A", "0.15", "0,15 A"), ("200 mA", "153.2", "153,2 mA"), ("20 mA", "1 (bên trái)", "quá thang")]   # so_lieu_mau (cot "Doc ra" khong chieu)
def screen_str(I, ghd):
    """Dong ho 3 1/2 chu so theo mo_hinh: qua thang -> '1'; 10 A buoc 0,01 A; thang mA buoc GHD/2000 (hien theo mA)."""
    if I > ghd: return "1"
    if ghd == 10.0: return f"{round(I / 0.01) * 0.01:.2f}"
    st = ghd * 1000 / 2000; nd = 1 if st >= 0.1 - 1e-12 else 2
    return f"{round(I * 1000 / st) * st:.{nd}f}"

WIRE = (60, 66, 92); BODY = (52, 58, 78); SCREEN = (214, 236, 218); SCR_INK = (20, 55, 30)
DRED = (185, 28, 28); DGREEN = (21, 110, 55); GLOW = (253, 224, 71)
KNOB = (810, 545); KLAB = {"20 mA": (680, 470, "20m"), "200 mA": (810, 455, "200m"), "10 A": (940, 470, "10A")}
JACK = {"10A": 690, "VΩmA": 820, "COM": 950}; JY = 660

def lamp(d, x, y, on, a=1.0, r=40):
    if on > 0:
        for k in range(5, 0, -1):
            rr = r + k * 10 * on; d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=A(GLOW, a * on * 0.11))
    d.ellipse([x - r, y - r, x + r, y + r], fill=A(mix(WHITE, GLOW, on), a), outline=A(NAVY, a), width=5)
    d.line([(x - 18, y + 8), (x - 8, y - 10), (x, y + 8), (x + 8, y - 10), (x + 18, y + 8)], fill=A(ORANGE if on else MUTED, a), width=4)

def lcd(d, box, s, size=80, a=1.0):
    x0, y0, x1, y1 = box
    card(d, box, fill=A(SCREEN, a), r=12)
    if s == "1": text(d, (x0 + 40, (y0 + y1) / 2), "1", size, SCR_INK, anchor="lm", alpha=a)
    elif s: text(d, (x1 - 30, (y0 + y1) / 2), s, size, SCR_INK, anchor="rm", alpha=a)

def meter(d, scale, jack, s, knob_k=1.0, prev=None):
    card(d, (600, 280, 1020, 760), fill=BODY, r=28)
    lcd(d, (630, 305, 990, 420), s)
    for nm, (x, y, lab) in KLAB.items():
        text(d, (x, y), lab, 40, YELLOW if nm == scale else (200, 205, 220))
    d.ellipse([KNOB[0] - 56, KNOB[1] - 56, KNOB[0] + 56, KNOB[1] + 56], fill=(90, 96, 120), outline=WHITE, width=4)
    def kang(nm): x, y, _ = KLAB[nm]; return math.atan2(y - KNOB[1], x - KNOB[0])
    ang_ = kang(scale) if prev is None else lerp(kang(prev), kang(scale), ease(knob_k))
    d.line([KNOB, (KNOB[0] + 50 * math.cos(ang_), KNOB[1] + 50 * math.sin(ang_))], fill=WHITE, width=8)
    for nm, x in JACK.items():
        d.ellipse([x - 18, JY - 18, x + 18, JY + 18], fill=NAVY, outline=RED if nm != "COM" else (200, 205, 220), width=4)
        text(d, (x, JY + 54), nm, 40, WHITE)
    # que do (tu den) vao lo dang chon, que den tu COM ve nguon
    jx = JACK[jack]
    d.line([(560, 370), (560, 590), (jx, JY - 18)], fill=RED, width=7, joint="curve")
    d.line([(JACK["COM"] + 18, JY), (1030, JY), (1030, 784), (60, 784), (60, 370), (90, 370)], fill=NAVY, width=6, joint="curve")

def circuit(d, closed):
    d.line([(250, 370), (290, 370)], fill=WIRE, width=6); d.line([(350, 370), (390, 370)], fill=WIRE, width=6)
    d.line([(470, 370), (560, 370)], fill=WIRE, width=6)
    card(d, (90, 330, 250, 410), fill=(245, 243, 255), outline=NAVY, r=16, w=4)
    text(d, (170, 370), "3 V", 44, ORANGE)
    text(d, (232, 316), "+", 40, ORANGE); text(d, (108, 316), "−", 40, ORANGE)
    dot(d, 290, 370, 8, WIRE); dot(d, 350, 370, 8, WIRE)
    if closed: d.line([(290, 370), (350, 370)], fill=NAVY, width=7)
    else: d.line([(290, 370), (342, 326)], fill=NAVY, width=7)
    text(d, (320, 420), "K", 40, NAVY)
    lamp(d, 430, 370, 1.0 if closed else 0.0)

def top(d, scale, jack, closed, s, knob_k=1.0, prev=None):
    card(d, (40, 260, 1040, 800), fill=WHITE, outline=LIGHT, w=3)
    circuit(d, closed)
    meter(d, scale, jack, s if closed else "0.00" if jack == "10A" else ("0.0" if scale == "200 mA" else "0.00"), knob_k, prev)

XS = (250, 760)
def table(d, n, hl=None, y=830, alpha=1.0):
    card(d, (40, y, 1040, y + 430), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    for x, h in zip(XS, ("Thang", "Màn hình")): text(d, (x, y + 50), h, 40, INK, alpha=alpha)
    d.line([(70, y + 92), (1010, y + 92)], fill=A(LIGHT, alpha), width=3)
    for j, (a, b, c) in enumerate(ROWS):
        yy = y + 150 + j * 95
        if hl == j: d.rounded_rectangle([60, yy - 42, 1020, yy + 42], radius=20, fill=A((255, 237, 213), alpha))
        if j < n:
            text(d, (XS[0], yy), a, 46, NAVY, alpha=alpha); text(d, (XS[1], yy), b, 46, SCR_INK, alpha=alpha)
        else:
            for x in XS: text(d, (x, yy), "·", 44, GRAY, alpha=alpha)

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.7
def s_hook(img, d, t, sc):
    M = sc["M"]
    top(d, "10 A", "10A", True, ROWS[0][1])
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 830 + (1 - a) * 40
    card(d, (26, y0, 1054, y0 + 720), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 61), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 320, "Thang 10 A: 0,15 A.\nChuyển sang thang 200 mA,\nmàn hình hiện gì?", 50, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 620, 940, y0 + 632], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 620, 140 + 800 * (1 - p), y0 + 632], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
# (dong K, mo K, doi thang/que luc K mo) cho 3 thang
STEPS = [(0.8, 2.9, None), (4.4, 6.0, 3.6), (7.0, None, 6.4)]   # (t dong, t mo, t bat dau doi thang)
T_ROW = 0.5
def do_state(t):
    """-> (thang, lo que do, K dong?, chuoi man hinh, so hang, k quay num, thang truoc)."""
    j = 0
    for i, (tc, to, ts) in enumerate(STEPS):
        if ts is not None and t >= ts: j = i
    scale, jack = SCALES[j][0], ("10A" if j == 0 else "VΩmA")
    tc, to, ts = STEPS[j]
    closed = t >= tc and (to is None or t < to)
    s = screen_str(I_TRUE, SCALES[j][1]) if closed else None
    kk = clamp((t - ts) / 0.4) if ts is not None else 1.0
    prev = SCALES[j - 1][0] if j > 0 else None
    if j == 1 and t < ts + 0.4: jack = "10A" if t < ts + 0.2 else "VΩmA"
    n = sum(1 for (c, o, s_) in STEPS if t >= c + T_ROW)
    return scale, jack, closed, s, n, kk, prev

def s_do(img, d, t, sc):
    scale, jack, closed, s, n, kk, prev = do_state(t)
    top(d, scale, jack, closed, s, kk, prev)
    table(d, n, hl=(n - 1 if n > 0 else None))

def _kiem_dong_bo():
    """Moi 0,05 s: man hinh dung so cua thang dang chon; doi thang/que chi luc K mo; hang bang chi sau lan do do."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [x for x in clip["scenes"] if x["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        scale, jack, closed, s, n, kk, prev = do_state(t)
        if closed and (kk < 1 or s != ROWS[[r[0] for r in ROWS].index(scale)][1].split(" ")[0]): bad.append((round(t, 2), "so lech", scale, s))
        if closed and jack != ("10A" if scale == "10 A" else "VΩmA"): bad.append((round(t, 2), "que sai lo"))
        if n and ROWS[n - 1][0] != [SCALES[i][0] for i, (c, o, s_) in enumerate(STEPS) if t >= c + T_ROW][-1]: bad.append((round(t, 2), "hang"))
        t += 0.05
    return bad

def _kiem_so():
    bad = []
    for (nm, ghd), (nm2, scr, doc) in zip(SCALES, ROWS):
        if screen_str(I_TRUE, ghd) != scr.split(" ")[0]: bad.append((nm, screen_str(I_TRUE, ghd), scr))
    if not (abs(153.2 / 1000 - 0.15) < 0.005): bad.append("153,2 mA khong xap xi 0,15 A")
    if not (0.2 < 10 and I_TRUE < 0.2 and I_TRUE > 0.02): bad.append("thu tu thang")
    if [screen_str(I_HOI, g) for _, g in SCALES] != ["0.06", "60.0", "1"]: bad.append(("60 mA", [screen_str(I_HOI, g) for _, g in SCALES]))
    return bad

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · màn hiện 153.2"
    pw = tw(d, lab, F(42)) + 60
    card(d, (W / 2 - pw / 2, 272, W / 2 + pw / 2, 344), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 308), lab, 42, WHITE, alpha=ka)
    for j, (y, (sn, scr, doc)) in enumerate(zip((420, 640, 860), ROWS)):
        k = appear(t, 0.4 + 0.3 * j, 0.4)
        card(d, (40, y, 1040, y + 190), fill=A(WHITE, k), outline=A(LIGHT, k), w=3)
        text(d, (250, y + 95), sn, 48, NAVY, alpha=k)
        lcd(d, (520, y + 30, 1000, y + 160), scr.split(" ")[0], size=80, a=k)
    kb = appear(t, M[1] - 0.1, 0.4)
    if kb > 0:
        card(d, (40, 1090, 1040, 1250), fill=A((255, 250, 225), kb), outline=A(ORANGE, kb), w=4)
        lamp(d, 150, 1170, 1.0, a=kb, r=36)
        text(d, (580, 1170), "đèn sáng như nhau", 46, INK, alpha=kb)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    card(d, (40, 260, 1040, 700), fill=A(WHITE, k0), outline=A(LIGHT, k0), w=3)
    text(d, (W / 2, 330), "dòng điện trong mạch", 44, MUTED, alpha=k0)
    arrow(d, (160, 450), (920, 450), A(RED, k0), w=16, head=40)
    k1 = appear(t, 1.0, 0.4)
    text(d, (W / 2, 570), "cùng một dòng điện", 56, RED, alpha=k1)
    text(d, (W / 2, 645), "không đổi khi đổi thang", 46, INK, alpha=k1)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 <= 0: return
    card(d, (40, 740, 1040, 1300), fill=A(WHITE, k2), outline=A(ORANGE, k2), w=4)
    text(d, (W / 2, 805), "thang 20 mA nhỏ hơn dòng đo", 46, INK, alpha=k2)
    lcd(d, (300, 860, 780, 1020), "1", size=96, a=k2)
    text(d, (W / 2, 1150), "1 bên trái = quá thang", 50, DRED, alpha=k2)

# ---------------- canh 5: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 560), fill=WHITE, outline=LIGHT, w=3)
    text(d, (220, 410), "thang", 44, MUTED); text(d, (220, 470), "200 mA", 48, NAVY)
    lcd(d, (420, 340, 900, 480), "153.2", size=80)
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if a1 > 0:
        y0 = 600
        card(d, (40, y0, 1040, y0 + 820), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - M[0] - 1.6) / 0.4)
        q = "“Dòng điện 153,2 A”"; yy = y0 + 230; lw = tw(d, q, F(56))
        text(d, (W / 2, yy), q, 56, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
            text(d, (W / 2 + lw / 2 + 40, yy), "✗", 56, DRED, alpha=a1 * ks)
        kk = a1 * appear(t, M[0] + 2.2, 0.4)
        card(d, (70, y0 + 420, 1010, y0 + 760), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 540), "✓ Đơn vị theo", 54, DGREEN, alpha=kk)
        text(d, (W / 2, y0 + 640), "thang đang chọn", 54, DGREEN, alpha=kk)
    if k2 > 0:
        y0 = 600 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 700), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 95), "Chưa nói được", 52, NAVY, alpha=k2)
        for j, (l1, l2) in enumerate((("• Số liệu minh hoạ", ""),
                                      ("• Bỏ qua điện trở", "của đồng hồ"))):
            kk = k2 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4)
            text(d, (90, y0 + 270 + j * 250), l1, 50, INK, anchor="lm", alpha=kk)
            if l2: text(d, (132, y0 + 345 + j * 250), l2, 50, INK, anchor="lm", alpha=kk)

# ---------------- canh 6: Chot + cau hoi tu nho lai ----------------
T_CHOT = 4.0
def s_end(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 > 0:
        card(d, (40, 260, 1040, 1060), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
        pw = tw(d, "THỬ NGHĨ", F(40)) + 52
        card(d, (W / 2 - pw / 2, 290, W / 2 + pw / 2, 354), fill=A(ORANGE, k1), r=32)
        text(d, (W / 2, 322), "THỬ NGHĨ", 40, WHITE, alpha=k1)
        ctext(d, 480, f"Dòng khoảng {I_HOI * 1000:.0f} mA. Thang nào\nđọc được nhiều chữ số nhất?", 48, INK, maxw=900,
              alpha=appear(t, M[0] + 0.4, 0.5))
        ka = appear(t, M[0] + 0.6, 0.5) * k1
        for x, lab in zip((210, 540, 870), ("20 mA", "200 mA", "10 A")):
            card(d, (x - 140, 620, x + 140, 720), fill=A((245, 243, 255), ka), outline=A(PURPLE, ka), r=20, w=3)
            text(d, (x, 670), lab, 46, PURPLE, alpha=ka)
        kh = appear(t, M[0] + 2.4, 0.5)
        card(d, (110, 790, 970, 1020), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 905, f"Thử {I_HOI * 1000:.0f} mA với từng thang", 44, ORANGE, maxw=820, alpha=kh)
    k0 = appear(t, M[0] + T_CHOT, 0.5)
    if k0 > 0:
        card(d, (60, 1110, 1020, 1420), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
        ctext(d, 1265, "Đổi thang:\ndòng điện không đổi", 52, GREEN, maxw=880, alpha=k0)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding")]
    cs += [(do["t0"] + c, "tap") for c, o, s_ in STEPS]
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + 0.2, "buzz"),
           (b["t0"] + b["M"][0] + 2.2, "tap"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return sorted(cs)

CLIP = dict(id="tn-l9-modau-01", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Dụng cụ đo điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Một dòng điện, ba thang", draw=s_hook, tail=0.7, caps=[
   ("Đồng hồ nối tiếp với đèn.", 3.4),
   ("Tự trả lời trước khi xem.", 5.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.5, caps=[
   ("Thang 10 A: que đỏ lỗ 10A.", 3.4),
   ("Ngắt khoá rồi mới đổi thang.", 5.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Ba thang, ba màn hình.", 3.0),
   ("Còn đèn thì sao?", 3.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Có đúng không?", 3.8),
   ("Còn chưa nói được.", 3.2)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Cùng một dòng điện.", 3.4),
   ("Thang quá nhỏ thì sao?", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Tự trả lời trước khi xem.", 6.6)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch số:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
