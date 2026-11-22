# Clip: tn-l9-modau-02 - Von ke mac NOI TIEP voi bong den: den tat, von ke chi gan bang U nguon (KHTN 9, bai 128, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-modau-02.json:
#   tham_so: U_n 6,0 V (max 12 V), R_V = 10 000 000 Ohm, R_D = 12 Ohm. so_lieu_mau: U_n 6,0 V ; I 6e-7 A ; U_V 6,0 V.
#   ket_qua_ky_vong: dong khoang 0,6 uA, den tat, von ke chi 6,00 V. dung_cu: dong ho da nang thang DCV 20 V, den 6 V - 0,5 A,
#   bien ap nguon 6 V mot chieu, khoa K. bay = hien_tuong_hay_sai[0]; ve dung = rut_ra[2] (mac song song).
#   chua noi duoc = so_lieu_mau.ghi_chu (tinh tu mo hinh) + mo_hinh.gia_thiet[0] (bo qua dien tro day noi, nguon).
# Bai 128: Cau 4 (ngay TREN hop) hoi AMPE KE mac song song -> clip KHONG noi ampe ke mac nham, khong dung hien_tuong_hay_sai[1]
#   ("nguy hiem nhu ampe ke") lam bay. Cau 2, 5, 7 (chon thang dong) khong lien quan.
# Du doan (K10: chi cau hoi + hinh; vong 2): "Von ke chi gan 0 V, khoang 3 V hay khoang 6 V?" (bang truoc hop da noi den tat).
# Thu tu vong 2: Bay dat TRUOC Rut ra. Cau chot: nguon 3 V (trong tham_so 0..12), von ke van noi tiep -> chi bao nhieu?
#   (3,00 V; kho them hang so_lieu_mau [3, 3e-7, 3] ghi "mo hinh"). Goi y khong neu cach lam.
# Mach kin: nguon (+) -> K -> den -> que do -> dong ho (lo VOmA) -> COM -> que den -> (-) nguon: von ke NOI TIEP den.
import math
from engine import *

U_N, U_HOI = 6.0, 3.0                   # tham_so U_n mac_dinh; U cau chot (trong 0..12, hang 2 so_lieu_mau)
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
    if s: text(d, (x1 - 30, (y0 + y1) / 2), s, size, SCR_INK, anchor="rm", alpha=a)

def meter(d, s, leads=1.0):
    card(d, (600, 280, 1020, 760), fill=BODY, r=28)
    lcd(d, (630, 305, 990, 420), s)
    text(d, (810, 458), "20V", 40, YELLOW); text(d, (680, 470), "DCV", 40, (200, 205, 220))
    d.ellipse([KNOB[0] - 56, KNOB[1] - 56, KNOB[0] + 56, KNOB[1] + 56], fill=(90, 96, 120), outline=WHITE, width=4)
    d.line([KNOB, (KNOB[0], KNOB[1] - 50)], fill=WHITE, width=8)
    for nm, x in JACK.items():
        d.ellipse([x - 18, JY - 18, x + 18, JY + 18], fill=NAVY, outline=RED if nm != "COM" else (200, 205, 220), width=4)
        text(d, (x, JY + 54), nm, 40, WHITE)
    if leads > 0:
        d.line([(560, 370), (560, 590), (JACK["VΩmA"], JY - 18)], fill=A(RED, leads), width=7, joint="curve")
        d.line([(JACK["COM"] + 18, JY), (1030, JY), (1030, 784), (60, 784), (60, 370), (90, 370)], fill=A(NAVY, leads), width=6, joint="curve")

def circuit(d, on, closed, lamp_on=0.0):
    d.line([(250, 370), (290, 370)], fill=WIRE, width=6); d.line([(350, 370), (390, 370)], fill=WIRE, width=6)
    d.line([(470, 370), (560, 370)], fill=WIRE, width=6)
    card(d, (90, 330, 250, 410), fill=(245, 243, 255) if on else (232, 232, 236), outline=NAVY, r=16, w=4)
    text(d, (170, 370), "6 V", 44, ORANGE if on else GRAY)
    text(d, (232, 316), "+", 40, ORANGE); text(d, (108, 316), "−", 40, ORANGE)
    text(d, (170, 450), "nguồn bật" if on else "nguồn tắt", 40, INK if on else MUTED)
    dot(d, 290, 370, 8, WIRE); dot(d, 350, 370, 8, WIRE)
    if closed: d.line([(290, 370), (350, 370)], fill=NAVY, width=7)
    else: d.line([(290, 370), (342, 326)], fill=NAVY, width=7)
    text(d, (320, 300), "K", 40, NAVY)
    lamp(d, 430, 370, lamp_on)
    text(d, (430, 450), "đèn", 38, INK)

def top(d, on, closed, s, leads=1.0, lab=True):
    card(d, (40, 260, 1040, 800), fill=WHITE, outline=LIGHT, w=3)
    circuit(d, on, closed)
    meter(d, s, leads)
    if lab: text(d, (330, 560), "vôn kế mắc", 40, PURPLE); text(d, (330, 615), "nối tiếp đèn", 40, PURPLE)

def table(d, n, hl=None, y=830, alpha=1.0):
    card(d, (40, y, 1040, y + 300), fill=A(WHITE, alpha), outline=A(LIGHT, alpha), w=3)
    rows = (("Đèn", "không sáng", INK), ("Vôn kế", UV_STR.replace(".", ",") + " V", PURPLE))
    for j, (a, b, c) in enumerate(rows):
        yy = y + 85 + j * 130
        if hl == j: d.rounded_rectangle([60, yy - 50, 1020, yy + 50], radius=20, fill=A((255, 237, 213), alpha))
        text(d, (250, yy), a, 46, NAVY, alpha=alpha)
        text(d, (700, yy), b if j < n else "·", 48 if j < n else 44, c if j < n else GRAY, alpha=alpha)

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.7
def s_hook(img, d, t, sc):
    M = sc["M"]
    top(d, False, False, "", lab=False)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 830 + (1 - a) * 40
    card(d, (26, y0, 1054, y0 + 720), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 61), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 320, "Vôn kế chỉ gần 0 V,\nkhoảng 3 V hay khoảng 6 V?", 50, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 620, 940, y0 + 632], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 620, 140 + 800 * (1 - p), y0 + 632], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
T_LEAD, T_ON, T_CL = 0.5, 4.3, 5.1
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
    if closed:
        text(d, (440, 520), "I ≈ 0", 40, RED)
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
    if f"{UV_of(U_HOI):.2f}" != "3.00": bad.append(("U_V 3 V", UV_of(U_HOI)))
    if not (0 <= U_HOI <= 12): bad.append("U_HOI ngoai tham_so")
    if I_of(U_N) * R_D > 0.01: bad.append("U den khong ~ 0")
    return bad

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · khoảng 6 V"
    pw = tw(d, lab, F(42)) + 60
    card(d, (W / 2 - pw / 2, 272, W / 2 + pw / 2, 344), fill=A(NAVY, ka), r=34)
    text(d, (W / 2, 308), lab, 42, WHITE, alpha=ka)
    k = appear(t, 0.4, 0.4)
    card(d, (40, 390, 520, 900), fill=A(WHITE, k), outline=A(LIGHT, k), w=3)
    text(d, (280, 440), "đèn", 44, NAVY, alpha=k)
    lamp(d, 280, 640, 0.0, a=k, r=110)
    card(d, (560, 390, 1040, 900), fill=A(BODY, k), r=28)
    text(d, (800, 440), "vôn kế", 44, WHITE, alpha=k)
    lcd(d, (590, 560, 1010, 720), UV_STR, size=96, a=k)
    text(d, (800, 800), "thang 20 V", 40, (200, 205, 220), alpha=k)
    kb = appear(t, M[1] - 0.1, 0.4)
    if kb > 0:
        card(d, (40, 940, 1040, 1120), fill=A((245, 243, 255), kb), outline=A(PURPLE, kb), w=4)
        text(d, (W / 2, 1030), f"vôn kế ≈ U nguồn = {U_N:.0f} V", 50, PURPLE, alpha=kb)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k0 = appear(t, 0.2, 0.4)
    card(d, (40, 260, 1040, 760), fill=A(WHITE, k0), outline=A(LIGHT, k0), w=3)
    text(d, (W / 2, 320), "điện trở", 42, MUTED, alpha=k0)
    g = ease((t - 0.5) / 0.8)
    d.rounded_rectangle([90, 380, 90 + 900 * g, 450], radius=14, fill=A(PURPLE, k0))
    text(d, (110, 495), "vôn kế ≈ 10 000 000 Ω (thường)", 42, PURPLE, anchor="lm", alpha=k0)
    dot(d, 96, 575, 8, A(ORANGE, k0))
    text(d, (130, 575), "đèn 12 Ω", 42, ORANGE, anchor="lm", alpha=k0)
    k1 = appear(t, 1.6, 0.4)
    text(d, (W / 2, 680), "I ≈ 0,6 µA", 50, RED, alpha=k1)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 <= 0: return
    card(d, (40, 800, 1040, 1300), fill=A(WHITE, k2), outline=A(PURPLE, k2), w=4)
    text(d, (W / 2, 860), f"chia {U_N:.0f} V nguồn", 42, MUTED, alpha=k2)
    g2 = ease((t - M[1]) / 0.7)
    d.rounded_rectangle([90, 920, 90 + 900 * g2, 990], radius=14, fill=A(PURPLE, k2))
    text(d, (110, 1040), "vôn kế ≈ 6 V", 44, PURPLE, anchor="lm", alpha=k2)
    text(d, (110, 1110), "đèn ≈ 0 V", 44, ORANGE, anchor="lm", alpha=k2)
    text(d, (W / 2, 1210), "→ đo U nguồn, không đo U đèn", 44, INK, alpha=appear(t, M[1] + 1.0, 0.4))

# ---------------- canh 5: Bay roi Chua noi duoc ----------------
def sym(d, x, y, ch, col, a=1.0, r=40):
    d.ellipse([x - r, y - r, x + r, y + r], fill=A(WHITE, a), outline=A(col, a), width=6); text(d, (x, y + 2), ch, 42, col, alpha=a)

def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.2, 0.45) * (1 - k2)
    card(d, (40, 260, 1040, 560), fill=WHITE, outline=LIGHT, w=3)
    kk = appear(t, M[0] + 2.2, 0.4) if k2 <= 0 else 1.0
    # tren: so do noi tiep (sai) -> doi sang song song (dung) khi hien dau tick
    y = 430
    lamp(d, 540, y, 0.0, r=36)
    if kk < 1:
        a = 1 - kk
        d.line([(120, y), (504, y)], fill=A(WIRE, a), width=6); d.line([(576, y), (960, y)], fill=A(WIRE, a), width=6)
        d.rectangle([680, y - 6, 740, y + 6], fill=WHITE)
        sym(d, 790, y, "V", PURPLE, a)
    if kk > 0:
        d.line([(120, y), (504, y)], fill=A(WIRE, kk), width=6); d.line([(576, y), (960, y)], fill=A(WIRE, kk), width=6)
        d.line([(440, y), (440, y + 90), (500, y + 90)], fill=A(PURPLE, kk), width=5)
        d.line([(580, y + 90), (640, y + 90), (640, y)], fill=A(PURPLE, kk), width=5)
        sym(d, 540, y + 90, "V", PURPLE, kk, r=36)
        for x in (440, 640): dot(d, x, y, 8, A(WIRE, kk))
    if a1 > 0:
        y0 = 600
        card(d, (40, y0, 1040, y0 + 820), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 62), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - M[0] - 1.6) / 0.4)
        for j, q in enumerate(("“Nối tiếp vẫn đo", "đúng U đèn”")):
            yy = y0 + 210 + j * 72; lw = tw(d, q, F(50))
            text(d, (W / 2, yy), q, 50, mix(INK, MUTED, ks), alpha=a1)
            if ks > 0:
                d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        text(d, (W / 2, y0 + 360), "✗", 56, DRED, alpha=a1 * ks)
        ka = a1 * appear(t, M[0] + 2.2, 0.4)
        card(d, (70, y0 + 440, 1010, y0 + 760), fill=A((236, 253, 243), ka), r=24)
        text(d, (W / 2, y0 + 600), "✓ Mắc song song với đèn", 50, DGREEN, alpha=ka)
    if k2 > 0:
        y0 = 600 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 700), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 95), "Chưa nói được", 52, NAVY, alpha=k2)
        for j, (l1, l2) in enumerate((("• Số liệu", "theo mô hình"),
                                      ("• Bỏ qua điện trở", "dây, nguồn"))):
            kj = k2 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4)
            text(d, (90, y0 + 270 + j * 250), l1, 50, INK, anchor="lm", alpha=kj)
            text(d, (132, y0 + 345 + j * 250), l2, 50, INK, anchor="lm", alpha=kj)

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
        ctext(d, 450, f"Vẫn mắc nối tiếp, nguồn {U_HOI:.0f} V.\nVôn kế chỉ bao nhiêu?", 48, INK, maxw=900,
              alpha=appear(t, M[0] + 0.4, 0.5))
        ka = appear(t, M[0] + 0.6, 0.5) * k1
        y = 640
        d.line([(160, y), (504, y)], fill=A(WIRE, ka), width=6); d.line([(576, y), (920, y)], fill=A(WIRE, ka), width=6)
        lamp(d, 540, y, 0.0, a=ka, r=36)
        sym(d, 780, y, "V", PURPLE, ka)
        text(d, (280, y + 80), f"{U_HOI:.0f} V", 46, ORANGE, alpha=ka)
        text(d, (780, y - 90), "?", 60, PURPLE, alpha=ka)
        kh = appear(t, M[0] + 2.4, 0.5)
        card(d, (110, 800, 970, 1020), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 910, "Xem lại cảnh Rút ra", 44, ORANGE, maxw=820, alpha=kh)
    k0 = appear(t, M[0] + T_CHOT, 0.5)
    if k0 > 0:
        card(d, (60, 1110, 1020, 1420), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
        ctext(d, 1265, "Vôn kế nối tiếp:\nmạch gần như hở", 52, GREEN, maxw=880, alpha=k0)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding"),
          (do["t0"] + T_ON, "tap"), (do["t0"] + T_CL, "tap")]
    cs += [(da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + 0.2, "buzz"),
           (b["t0"] + b["M"][0] + 2.2, "tap"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return sorted(cs)

CLIP = dict(id="tn-l9-modau-02", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Dụng cụ đo điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Vôn kế mắc nối tiếp", draw=s_hook, tail=0.7, caps=[
   ("Đồng hồ để thang 20 V.", 3.0),
   ("Tự trả lời trước khi xem.", 4.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Tắt nguồn rồi mới mắc mạch.", 3.9),
   ("Bật nguồn 6 V, đóng khoá.", 4.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Đèn không sáng chút nào.", 3.0),
   ("So với nguồn 6 V.", 3.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Có đúng không?", 3.6),
   ("Còn chưa nói được.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Vôn kế cản dòng rất mạnh.", 3.4),
   ("Gần như cả 6 V nằm trên vôn kế.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.8, caps=[
   ("Tự trả lời trước khi xem.", 6.2)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch số:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
