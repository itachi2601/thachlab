# Clip: tn-l9-modau-02 - Von ke mac NOI TIEP voi bong den: den tat, von ke chi gan bang U nguon (KHTN 9, bai 128, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-modau-02.json:
#   tham_so: U_n 6,0 V (max 12 V), R_V = 10 000 000 Ohm, R_D = 12 Ohm. so_lieu_mau: U_n 6,0 V ; I 6e-7 A ; U_V 6,0 V.
#   ket_qua_ky_vong: dong khoang 0,6 uA, den tat, von ke chi 6,00 V. dung_cu: dong ho da nang thang DCV 20 V, den 6 V - 0,5 A,
#   bien ap nguon 6 V mot chieu, khoa K. bay = hien_tuong_hay_sai[0]; ve dung = rut_ra[2] (mac song song).
#   chua noi duoc = so_lieu_mau.ghi_chu (tinh tu mo hinh) + mo_hinh.gia_thiet[0] (bo qua dien tro day noi, nguon).
# Bai 128: Cau 4 (ngay TREN hop) hoi AMPE KE mac song song -> clip KHONG noi ampe ke mac nham, khong dung hien_tuong_hay_sai[1]
#   ("nguy hiem nhu ampe ke") lam bay. Cau 2, 5, 7 (chon thang dong) khong lien quan.
# Du doan (K10: chi cau hoi + hinh; vong 2): "Von ke chi gan 0 V, khoang 3 V hay khoang 6 V?" (bang truoc hop da noi den tat).
# Dung lai theo cong moi 27/11/2026 (Viec 4 L9 nhom C): chu >= 56, canh <= 180 tu/phut, thu tu chuan (Rut ra truoc Bay).
# Cau chot cu (nguon 3 V -> 3,00 V) la phep thay so tran -> bo. Cau chot MOI (tu suy): van noi tiep, nguon 12 V
#   (max tham_so), dong ho de thang 2 V -> U_V ~ 12 V > 2 V nen man hinh bao qua thang (so 1 ben trai).
#   Hai buoc chua chieu: U_V ~ U nguon (tu canh Rut ra) roi so voi gioi han thang 2 V.
# Mach kin: nguon (+) -> K -> den -> que do -> dong ho (lo VOmA) -> COM -> que den -> (-) nguon: von ke NOI TIEP den.
import math
from engine import *

U_N, U_HOI, THANG_HOI = 6.0, 12.0, 2.0   # tham_so U_n mac_dinh; cau chot: nguon 12 V (max), thang 2 V
R_V, R_D = 1.0e7, 12.0                  # tham_so
I_KHO, UV_KHO = 6e-7, 6.0               # so_lieu_mau
def I_of(u): return u / (R_V + R_D)     # mo_hinh
def UV_of(u): return I_of(u) * R_V
UV_STR = f"{UV_of(U_N):.2f}"            # dong ho 20 V: 3 1/2 chu so, buoc 0,01 V -> "6.00"

WIRE = (60, 66, 92); BODY = (52, 58, 78); SCREEN = (214, 236, 218); SCR_INK = (20, 55, 30)
DRED = (185, 28, 28); DGREEN = (21, 110, 55); GLOW = (253, 224, 71)
KNOB = (810, 545); JACK = {"10A": 690, "VΩmA": 820, "COM": 950}; JY = 660

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

KNOB = (915, 520); JACK = {"10A": 625, "VΩmA": 790, "COM": 965}; JY = 660
def meter(d, s, leads=1.0):
    card(d, (560, 276, 1036, 770), fill=BODY, r=28)
    lcd(d, (590, 292, 1006, 392), s)
    text(d, (720, 520), "20V", 56, YELLOW)
    d.ellipse([KNOB[0] - 56, KNOB[1] - 56, KNOB[0] + 56, KNOB[1] + 56], fill=(90, 96, 120), outline=WHITE, width=4)
    d.line([KNOB, (KNOB[0], KNOB[1] - 50)], fill=WHITE, width=8)
    for nm, x in JACK.items():
        d.ellipse([x - 18, JY - 18, x + 18, JY + 18], fill=NAVY, outline=RED if nm != "COM" else (200, 205, 220), width=4)
        text(d, (x, JY + 54), nm, 56, WHITE)
    if leads > 0:
        d.line([(530, 370), (530, 600), (JACK["VΩmA"], JY - 18)], fill=A(RED, leads), width=7, joint="curve")
        d.line([(JACK["COM"] + 18, JY), (1030, JY), (1030, 784), (60, 784), (60, 370), (90, 370)], fill=A(NAVY, leads), width=6, joint="curve")

def circuit(d, on, closed, lamp_on=0.0):
    d.line([(250, 370), (290, 370)], fill=WIRE, width=6); d.line([(350, 370), (390, 370)], fill=WIRE, width=6)
    d.line([(470, 370), (530, 370)], fill=WIRE, width=6)
    card(d, (90, 330, 250, 410), fill=(245, 243, 255) if on else (226, 226, 232), outline=NAVY, r=16, w=4)
    text(d, (170, 370), "6V", 56, ORANGE if on else GRAY)
    text(d, (232, 300), "+", 56, ORANGE); text(d, (108, 300), "−", 56, ORANGE)
    dot(d, 290, 370, 8, WIRE); dot(d, 350, 370, 8, WIRE)
    if closed: d.line([(290, 370), (350, 370)], fill=NAVY, width=7)
    else: d.line([(290, 370), (342, 326)], fill=NAVY, width=7)
    text(d, (320, 300), "K", 56, NAVY)
    lamp(d, 430, 370, lamp_on)
    text(d, (430, 455), "đèn", 56, INK)

def top(d, on, closed, s, leads=1.0, lab=True):
    card(d, (40, 260, 1040, 800), fill=WHITE, outline=LIGHT, w=3)
    circuit(d, on, closed)
    meter(d, s, leads)
    if lab: text(d, (290, 570), "vôn kế mắc", 56, PURPLE); text(d, (290, 650), "nối tiếp đèn", 56, PURPLE)

def table(d, n, hl=None, y=830):
    card(d, (40, y, 1040, y + 300), fill=WHITE, outline=LIGHT, w=3)
    rows = (("Đèn", "không sáng", INK), ("Vôn kế", UV_STR.replace(".", ",") + "V", PURPLE))
    for j, (a, b, c) in enumerate(rows):
        yy = y + 85 + j * 130
        if hl == j: d.rounded_rectangle([60, yy - 50, 1020, yy + 50], radius=20, fill=(255, 237, 213))
        text(d, (250, yy), a, 56, NAVY)
        if j < n: text(d, (700, yy), b, 56, c)

def pill(d, s, y, a, color, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    top(d, False, False, "", lab=False)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 860 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    text(d, (W / 2, y0 + 165), "Bật nguồn 6 V, đóng khoá.", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 250), "Vôn kế chỉ khoảng", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 335), "bao nhiêu vôn?", 58, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 420, 970, y0 + 510], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 420, 110 + max(90, 860 * (1 - p)), y0 + 510], radius=45, fill=A((76, 29, 149), a))

# ---------------- canh 2: Tien hanh ----------------
T_LEAD, T_ON, T_CL = 0.5, 3.2, 4.0
T_ROW1 = T_ROW2 = T_CL                  # bang hien cung luc so 6.00 tren man
def do_state(t):
    """-> (alpha day do, nguon bat?, K dong?, chu man hinh, so hang)."""
    leads = clamp((t - T_LEAD) / 0.6)
    on, closed = t >= T_ON, t >= T_CL
    s = (UV_STR if closed else "0.00") if on else ""
    n = (1 if t >= T_ROW1 else 0) + (1 if t >= T_ROW2 else 0)
    return leads, on, closed, s, n

def s_do(img, d, t, sc):
    leads, on, closed, s, n = do_state(t)
    top(d, on, closed, s, leads)
    table(d, n, hl=(n - 1 if n > 0 else None))

def _kiem_dong_bo():
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [x for x in clip["scenes"] if x["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        leads, on, closed, s, n = do_state(t)
        if on and leads < 1: bad.append((round(t, 2), "bat nguon khi chua mac xong"))
        if n and not closed: bad.append((round(t, 2), "ghi bang truoc khi dong K"))
        if s not in ("", "0.00", UV_STR) or (s == UV_STR) != (on and closed): bad.append((round(t, 2), "man hinh lech"))
        t += 0.05
    return bad

def _kiem_so():
    bad = []
    if abs(I_of(U_N) - I_KHO) / I_KHO > 0.01: bad.append(("I", I_of(U_N), I_KHO))
    if abs(UV_of(U_N) - UV_KHO) > 0.005: bad.append(("U_V", UV_of(U_N)))
    if UV_STR != "6.00": bad.append(("man hinh", UV_STR))
    if not UV_of(U_HOI) > THANG_HOI: bad.append(("chot khong qua thang", UV_of(U_HOI)))
    if not (0 <= U_HOI <= 12): bad.append("U_HOI ngoai tham_so")
    if I_of(U_N) * R_D > 0.01: bad.append("U den khong ~ 0")
    return bad

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN: khoảng 6 V", 320, 1.0, GREEN, 58)
    card(d, (40, 400, 520, 900), fill=WHITE, outline=LIGHT, w=3)
    text(d, (280, 460), "đèn", 56, NAVY)
    lamp(d, 280, 660, 0.0, r=110)
    card(d, (560, 400, 1040, 900), fill=BODY, r=28)
    text(d, (800, 460), "vôn kế", 56, WHITE)
    k = appear(t, 0.5, 0.4)
    lcd(d, (590, 580, 1010, 740), UV_STR if k > 0.5 else "", size=96)
    text(d, (800, 830), "20V", 56, YELLOW)
    kb = appear(t, M[1] - 0.1, 0.4)
    if kb > 0:
        card(d, (40, 940, 1040, 1120), fill=A((245, 243, 255), kb), outline=A(PURPLE, kb), w=4)
        text(d, (W / 2, 1030), "vôn kế ≈ U nguồn", 60, PURPLE, alpha=kb)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 760), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 330), "điện trở", 58, MUTED)
    g = ease((t - 0.3) / 1.2)
    text(d, (90, 440), "vôn kế", 56, PURPLE, anchor="lm")
    d.rounded_rectangle([300, 410, 300 + max(14, 690 * g), 470], radius=14, fill=PURPLE)
    text(d, (90, 590), "đèn", 56, ORANGE, anchor="lm")
    d.rounded_rectangle([300, 560, 314, 620], radius=6, fill=ORANGE)
    k2 = appear(t, M[1] + 0.1, 0.45)
    card(d, (40, 800, 1040, 1180), fill=A(WHITE, k2), outline=A(PURPLE, k2), w=4)
    text(d, (W / 2, 900), "U vôn kế ≈ 6 V", 60, PURPLE, alpha=k2)
    text(d, (W / 2, 1060), "U đèn ≈ 0", 60, ORANGE, alpha=k2)

# ---------------- canh 5: Bay roi Chua noi duoc ----------------
BAY_ST = 2.2
def sym(d, x, y, ch, col, a=1.0, r=44):
    d.ellipse([x - r, y - r, x + r, y + r], fill=A(WHITE, a), outline=A(col, a), width=6); text(d, (x, y + 2), ch, 56, col, alpha=a)

def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[2] - 0.1, 0.45)
    a1 = 1 - k2
    card(d, (40, 260, 1040, 600), fill=WHITE, outline=LIGHT, w=3)
    kk = appear(t, M[1] + 0.1, 0.4)
    y = 400
    lamp(d, 540, y, 0.0, r=40)
    if kk < 1:
        a = 1 - kk
        d.line([(120, y), (500, y)], fill=A(WIRE, a), width=6); d.line([(580, y), (960, y)], fill=A(WIRE, a), width=6)
        d.rectangle([730, y - 8, 850, y + 8], fill=WHITE)
        pu = 0.5 + 0.5 * math.sin(2 * math.pi * t / 1.6); rr = 62 + 14 * pu
        d.ellipse([790 - rr, y - rr, 790 + rr, y + rr], fill=A(mix(WHITE, (253, 186, 116), pu), a))
        sym(d, 790, y, "V", PURPLE, a)
    if kk > 0:
        d.line([(120, y), (500, y)], fill=A(WIRE, kk), width=6); d.line([(580, y), (960, y)], fill=A(WIRE, kk), width=6)
        d.line([(430, y), (430, y + 110), (494, y + 110)], fill=A(PURPLE, kk), width=5)
        d.line([(586, y + 110), (650, y + 110), (650, y)], fill=A(PURPLE, kk), width=5)
        sym(d, 540, y + 110, "V", PURPLE, kk)
        for x in (430, 650): dot(d, x, y, 9, A(WIRE, kk))
    y0 = 640
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 640), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y0 + 62, a1, DRED)
        for j, q in enumerate(("“Nối tiếp vẫn đo", "đúng U đèn”")):
            yy = y0 + 170 + j * 80; lw = tw(d, q, F(58))
            text(d, (W / 2, yy), q, 58, INK, alpha=a1)
            ks = clamp((t - BAY_ST) / 0.4)
            if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=7)
        ka = a1 * kk
        card(d, (70, y0 + 320, 1010, y0 + 580), fill=A((236, 253, 243), ka), r=24)
        text(d, (W / 2, y0 + 400), "✓ Song song", 58, DGREEN, alpha=ka)
        text(d, (W / 2, y0 + 490), "với đèn", 58, DGREEN, alpha=ka)
    if k2 > 0:
        card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 110), "Chưa nói được:", 60, NAVY, alpha=k2)
        text(d, (W / 2, y0 + 220), "điện trở dây, nguồn", 58, INK, alpha=k2)
        text(d, (W / 2, y0 + 320), "(bỏ qua, chưa đo)", 56, NAVY, alpha=k2)

# ---------------- canh 6: Chot ----------------
END_Q = 0.2
def s_end(img, d, t, sc):
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 280, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 350, k1, ORANGE)
    text(d, (W / 2, 465), "Vẫn mắc nối tiếp,", 58, INK, alpha=k1)
    text(d, (W / 2, 550), f"nguồn {U_HOI:.0f} V, thang {THANG_HOI:.0f} V.", 58, INK, alpha=k1)
    text(d, (W / 2, 635), "Màn hình hiện gì?", 58, INK, alpha=k1)
    if k1 <= 0: return
    y = 820
    d.line([(140, y), (500, y)], fill=A(WIRE, k1), width=6); d.line([(580, y), (940, y)], fill=A(WIRE, k1), width=6)
    lamp(d, 540, y, 0.0, a=k1, r=40)
    sym(d, 790, y, "V", PURPLE, k1)
    card(d, (140, y - 50, 300, y + 50), fill=A((245, 243, 255), k1), outline=A(NAVY, k1), r=16, w=4)
    text(d, (220, y), f"{U_HOI:.0f}V", 56, ORANGE, alpha=k1)
    card(d, (330, 1000, 750, 1140), fill=A(BODY, k1), r=20)
    lcd(d, (350, 1015, 730, 1125), "", a=k1)
    text(d, (870, 1070), f"{THANG_HOI:.0f}V", 56, NAVY, alpha=k1)
    rr = 60 + 30 * math.sin(2 * math.pi * t / 2.0)
    xc, yc = 540, 1340
    d.ellipse([xc - rr, yc - rr, xc + rr, yc + rr], fill=A(mix(ORANGE, WHITE, 0.45), k1))
    text(d, (xc, yc), "?", 80, WHITE, alpha=k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
          (do["t0"] + T_ON, "tap"), (do["t0"] + T_CL, "tap")]
    cs += [(da["t0"] + 0.5, "ding"), (r["t0"] + r["M"][1] + 0.1, "tap"), (b["t0"] + BAY_ST, "buzz"),
           (b["t0"] + b["M"][1] + 0.1, "tap"), (e["t0"] + END_Q + 0.1, "open")]
    return sorted(cs)

CLIP = dict(id="tn-l9-modau-02", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Dụng cụ đo điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Vôn kế mắc nối tiếp", draw=s_hook, tail=0.3, caps=[
   ("Đồng hồ để thang 20 V.", 2.5),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Tắt nguồn rồi mới mắc.", 3.0),
   ("Bật nguồn, đóng khoá.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Đèn không sáng chút nào.", 3.0),
   ("So với nguồn 6 V.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.4, caps=[
   ("Vôn kế cản dòng rất mạnh.", 3.0),
   ("Còn đèn?", 3.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 4.2),
   ("Nhìn sơ đồ trên.", 3.4),
   ("Còn bỏ ngỏ.", 2.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Tự nghĩ.", 6.2)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch số:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
