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
# Dung lai theo cong moi 27/11/2026 (Viec 4 L9 nhom C): chu >= 56, canh <= 180 tu/phut, khoi chu cach >= 2,5 s.
# Cau chot cu (60 mA: thang nao nhieu chu so nhat) trung Cau 2 ("nhieu chu so nhat") -> bo.
# Cau chot MOI: thang 200 mA hien 18.5 -> van sang thang 20 mA, man hinh hien gi? -> 18.50 (18,5 mA < 20 mA nen khong
#   qua thang; thang 20 mA buoc 0,01 mA). Clip chi chieu ca qua thang (153 > 20), chua chieu ca vua thang 20 mA.
# Bay: dung so khac Du doan (48.6 o thang 200 mA doc thanh 48,6 A), hien_tuong_hay_sai[2].
# Mach kin: nguon 3 V (+) -> K -> den -> que do -> dong ho -> COM -> que den -> (-) nguon. Dong ho noi tiep den.
import math
from engine import *

I_TRUE = 0.15318                                 # tham_so I mac_dinh (A)
I_HOI = 0.0185                                   # cau chot moi: 18,5 mA (khong hien dap so)
I_BAY = 0.0486                                   # bay: 48.6 o thang 200 mA
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
KNOB = (915, 520); KANG = {"20 mA": -150, "200 mA": -90, "10 A": -30}
JACK = {"10A": 625, "VΩmA": 790, "COM": 965}; JY = 660

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
    card(d, (560, 276, 1036, 770), fill=BODY, r=28)
    lcd(d, (590, 292, 1006, 392), s)
    text(d, (720, 520), scale.replace(" ", ""), 56, YELLOW)
    d.ellipse([KNOB[0] - 56, KNOB[1] - 56, KNOB[0] + 56, KNOB[1] + 56], fill=(90, 96, 120), outline=WHITE, width=4)
    def kang(nm): return math.radians(KANG[nm])
    ang_ = kang(scale) if prev is None else lerp(kang(prev), kang(scale), ease(knob_k))
    d.line([KNOB, (KNOB[0] + 50 * math.cos(ang_), KNOB[1] + 50 * math.sin(ang_))], fill=WHITE, width=8)
    for nm, x in JACK.items():
        d.ellipse([x - 18, JY - 18, x + 18, JY + 18], fill=NAVY, outline=RED if nm != "COM" else (200, 205, 220), width=4)
        text(d, (x, JY + 54), nm, 56, WHITE)
    # que do (tu den) vao lo dang chon, que den tu COM ve nguon
    jx = JACK[jack]
    d.line([(530, 370), (530, 600), (jx, JY - 18)], fill=RED, width=7, joint="curve")
    d.line([(JACK["COM"] + 18, JY), (1030, JY), (1030, 784), (60, 784), (60, 370), (90, 370)], fill=NAVY, width=6, joint="curve")

def circuit(d, closed):
    d.line([(250, 370), (290, 370)], fill=WIRE, width=6); d.line([(350, 370), (390, 370)], fill=WIRE, width=6)
    d.line([(470, 370), (530, 370)], fill=WIRE, width=6)
    card(d, (90, 330, 250, 410), fill=(245, 243, 255), outline=NAVY, r=16, w=4)
    text(d, (170, 370), "3V", 56, ORANGE)
    text(d, (232, 305), "+", 56, ORANGE); text(d, (108, 305), "−", 56, ORANGE)
    dot(d, 290, 370, 8, WIRE); dot(d, 350, 370, 8, WIRE)
    if closed: d.line([(290, 370), (350, 370)], fill=NAVY, width=7)
    else: d.line([(290, 370), (342, 326)], fill=NAVY, width=7)
    text(d, (320, 425), "K", 56, NAVY)
    lamp(d, 430, 370, 1.0 if closed else 0.0)

def top(d, scale, jack, closed, s, knob_k=1.0, prev=None):
    card(d, (40, 260, 1040, 800), fill=WHITE, outline=LIGHT, w=3)
    circuit(d, closed)
    meter(d, scale, jack, s if closed else "0.00" if jack == "10A" else ("0.0" if scale == "200 mA" else "0.00"), knob_k, prev)

XS = (250, 760)
def table(d, n, hl=None, y=830, alpha=1.0):
    card(d, (40, y, 1040, y + 430), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    for x, h in zip(XS, ("Thang", "Màn hình")): text(d, (x, y + 50), h, 56, NAVY, alpha=alpha)
    d.line([(70, y + 92), (1010, y + 92)], fill=A(LIGHT, alpha), width=3)
    for j, (a, b, c) in enumerate(ROWS):
        yy = y + 150 + j * 95
        if hl == j: d.rounded_rectangle([60, yy - 42, 1020, yy + 42], radius=20, fill=A((255, 237, 213), alpha))
        if j < n:
            text(d, (XS[0], yy), a.replace(" ", ""), 56, NAVY, alpha=alpha); text(d, (XS[1], yy), b, 56, SCR_INK, alpha=alpha)

def pill(d, s, y, a, color, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    top(d, "10 A", "10A", True, ROWS[0][1])
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 860 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    text(d, (W / 2, y0 + 165), "Thang 10 A: 0,15 A.", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 250), "Vặn sang thang 200 mA,", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 335), "màn hình hiện gì?", 58, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 420, 970, y0 + 510], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 420, 110 + max(90, 860 * (1 - p)), y0 + 510], radius=45, fill=A((76, 29, 149), a))

# ---------------- canh 2: Tien hanh ----------------
# (dong K, mo K, doi thang/que luc K mo) cho 3 thang
STEPS = [(0.6, 2.4, None), (3.6, 5.0, 2.9), (5.9, None, 5.4)]   # (t dong, t mo, t bat dau doi thang)
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
    if [screen_str(I_HOI, g) for _, g in SCALES] != ["0.02", "18.5", "18.50"]: bad.append(("18,5 mA", [screen_str(I_HOI, g) for _, g in SCALES]))
    if screen_str(I_BAY, 0.2) != "48.6": bad.append(("bay", screen_str(I_BAY, 0.2)))
    return bad

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = 1.0
    pill(d, "ĐÁP ÁN: màn hiện 153.2", 320, ka, GREEN, 58)
    for j, (y, (sn, scr, doc)) in enumerate(zip((400, 610, 820), ROWS)):
        card(d, (40, y, 1040, y + 180), fill=WHITE, outline=LIGHT, w=3)
        text(d, (250, y + 90), sn.replace(" ", ""), 56, NAVY)
        k = appear(t, 0.4 + 0.3 * j, 0.4)
        lcd(d, (520, y + 25, 1000, y + 155), scr.split(" ")[0], size=80, a=max(0.2, k))
    kb = appear(t, M[1] - 0.1, 0.4)
    if kb > 0:
        card(d, (40, 1040, 1040, 1200), fill=A((255, 250, 225), kb), outline=A(ORANGE, kb), w=4)
        lamp(d, 150, 1120, 1.0, a=kb, r=36)
        text(d, (580, 1120), "đèn sáng như nhau", 58, INK, alpha=kb)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 720), fill=WHITE, outline=LIGHT, w=3)
    for j, (x, lab) in enumerate(zip((210, 540, 870), ("10A", "200mA", "20mA"))):
        k = appear(t, 0.2 + 0.25 * j, 0.4)
        lamp(d, x, 400, k, r=44)
        text(d, (x, 510), lab, 56, NAVY)
    d.line([(100, 400), (980, 400)], fill=A(WIRE, 0.25), width=4)
    k1 = 1.0
    text(d, (W / 2, 630), "dòng điện không đổi", 60, RED, alpha=k1)
    k2 = appear(t, M[1] + 0.1, 0.45)
    card(d, (40, 760, 1040, 1180), fill=A(WHITE, k2), outline=A(ORANGE, k2), w=4)
    lcd(d, (300, 800, 780, 960), "1", size=96, a=k2)
    text(d, (W / 2, 1080), "1 bên trái = quá thang", 58, DRED, alpha=k2)

# ---------------- canh 5: Bay roi Chua noi duoc ----------------
BAY_ST = 2.2
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 560), fill=WHITE, outline=LIGHT, w=3)
    pu = 0.5 + 0.5 * math.sin(2 * math.pi * t / 1.6)
    d.rounded_rectangle([70, 350, 350, 470], radius=30, fill=mix(WHITE, (253, 186, 116), pu))
    text(d, (210, 410), "200mA", 60, NAVY)
    lcd(d, (420, 340, 980, 480), screen_str(I_BAY, 0.2), size=88)
    k2 = appear(t, M[2] - 0.1, 0.45)
    a1 = 1 - k2; y0 = 600
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 640), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y0 + 62, a1, DRED)
        q = "“Dòng điện 48,6 A”"; yy = y0 + 190; lw = tw(d, q, F(58))
        text(d, (W / 2, yy), q, 58, INK, alpha=a1)
        ks = clamp((t - BAY_ST) / 0.4)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=7)
        kk = a1 * appear(t, M[1] + 0.1, 0.4)
        card(d, (70, y0 + 300, 1010, y0 + 560), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 380), "✓ Thang mA", 58, DGREEN, alpha=kk)
        text(d, (W / 2, y0 + 470), "→ đọc 48,6 mA", 58, DGREEN, alpha=kk)
    if k2 > 0:
        card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 110), "Chưa nói được:", 60, NAVY, alpha=k2)
        text(d, (W / 2, y0 + 220), "điện trở đồng hồ", 58, INK, alpha=k2)
        text(d, (W / 2, y0 + 320), "(bỏ qua, chưa đo)", 56, NAVY, alpha=k2)

# ---------------- canh 6: Chot ----------------
END_Q = 0.2
def s_end(img, d, t, sc):
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 280, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 350, k1, ORANGE)
    text(d, (W / 2, 465), "Thang 200 mA hiện 18.5.", 58, INK, alpha=k1)
    text(d, (W / 2, 550), "Vặn sang thang 20 mA,", 58, INK, alpha=k1)
    text(d, (W / 2, 635), "màn hình hiện gì?", 58, INK, alpha=k1)
    if k1 <= 0: return
    for x, lab, s in ((280, "200mA", "18.5"), (800, "20mA", None)):
        text(d, (x, 800), lab, 56, NAVY, alpha=k1)
        lcd(d, (x - 210, 860, x + 210, 1000), s, size=80, a=k1)
    arrow(d, (510, 930), (570, 930), A(NAVY, k1), w=8, head=24)
    rr = 60 + 30 * math.sin(2 * math.pi * t / 2.0)
    xc, yc = 800, 1240
    d.ellipse([xc - rr, yc - rr, xc + rr, yc + rr], fill=A(mix(ORANGE, WHITE, 0.45), k1))
    text(d, (xc, yc), "?", 80, WHITE, alpha=k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    cs += [(do["t0"] + c, "tap") for c, o, s_ in STEPS]
    cs += [(da["t0"] + 0.2, "ding"), (r["t0"] + r["M"][1] + 0.1, "tap"), (b["t0"] + BAY_ST, "buzz"),
           (b["t0"] + b["M"][1] + 0.1, "tap"), (e["t0"] + END_Q + 0.1, "open")]
    return sorted(cs)

CLIP = dict(id="tn-l9-modau-01", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Dụng cụ đo điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Một dòng điện, ba thang", draw=s_hook, tail=0.3, caps=[
   ("Đồng hồ nối tiếp đèn.", 2.5),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Thang 10 A: que đỏ lỗ 10A.", 3.4),
   ("Ngắt khoá rồi mới đổi thang.", 4.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Ba thang, ba màn hình.", 3.0),
   ("Còn đèn thì sao?", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.4, caps=[
   ("Đổi thang, đèn vẫn vậy.", 3.0),
   ("Thang quá nhỏ thì sao?", 3.4)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 4.2),
   ("Nhìn đơn vị thang.", 3.4),
   ("Còn bỏ ngỏ.", 2.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Tự nghĩ.", 6.2)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch số:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
