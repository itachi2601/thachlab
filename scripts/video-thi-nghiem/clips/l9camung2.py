# Clip: tn-l9-camung-02 - Nam cham dien: dong, giu dong, ngat cong tac (KHTN 9, bai 92, 18/11/2026)
# So lieu lay tu content/thi-nghiem/tn-l9-camung-02.json (dinh tinh, khong co so mA):
#   tham_so U = 6,0 V (dung_cu: bo pin 4 x 1,5 V). so_lieu_mau: mo -> 0 ; trong luc dong -> lech phai roi ve 0 ;
#   giu dong -> 0 ; trong luc ngat -> lech trai roi ve 0 ; sau khi ngat -> 0. ghi_chu: phia lech tuy cach noi dien ke.
#   rut_ra: chi khi dong trong A dang thay doi, tu truong qua B thay doi, B co dong cam ung.
#   Bay (cong B 18/11) = "luc ngat het dong nen kim khong lech" (bay cu "giu dong lech mai" = dap an Cau 2 bai). Chua noi duoc: do lon dong o B (chi quan sat dinh tinh,
#   kho khong co so) + ghi_chu (phia lech tuy cach noi). Kho KHONG co khong_chung_minh cho TN nay.
# Tranh tra loi san cau hoi cua bai:
#   - Cau 2 (Doan truoc, NAM TRUOC hop TN2): giu dong -> kim chi 0. Video dat sau Cau 2; Du doan clip hoi luc NGAT.
#   - Kiem tra nhanh cau 3 (kim lech khi nao?): Du doan khong hoi "khi nao", chi hoi luc ngat.
#   - Cau 3A + thu thach sao (keo cuon/nam cham ra xa): cau chot doi sang BIEN TRO (bai khong co bien tro).
#   - Tinh huong mau "dong, ngat lien tuc -> hai den thay nhau chop": khong dung lam cau chot.
# Du doan (K10): dong K mot luc roi ngat -> luc ngat, kim cua B the nao? -> lech sang trai (nguoc luc dong) roi ve 0.
# Cau chot: K van dong, van bien tro cho dong o A giam dan -> kim B co lech khong? -> co (dong A doi). The chot sau 4 s.
# Mo hinh (truc thoi gian so do, chieu cham): i_A tang muot 0 -> I0 trong [a,b], giam I0 -> 0 trong [c,e];
#   kim B ~ toc do doi cua i_A (ham sin) -> phai khi i_A tang, trai khi giam, 0 khi i_A khong doi. _kiem_vat_li() kiem.
import copy
from engine import *

U_PIN = 6.0                                  # tham_so U (4 x 1,5 V)
UA = (0.12, 0.26, 0.66, 0.80)                # bat dau tang, het tang, bat dau giam, het giam (truc so do)
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

def iA(u):                                   # 0..1 (ti le dong on dinh)
    a, b, c, e = UA
    if u < a: return 0.0
    if u < b: return (1 - math.cos(math.pi * (u - a) / (b - a))) / 2
    if u < c: return 1.0
    if u < e: return (1 + math.cos(math.pi * (u - c) / (e - c))) / 2
    return 0.0

def kim(u):                                  # -1..1, duong = lech phai
    a, b, c, e = UA
    if a <= u < b: return math.sin(math.pi * (u - a) / (b - a))
    if c <= u < e: return -math.sin(math.pi * (u - c) / (e - c))
    return 0.0

# ---------------- bo cuc (khung 1080x1920) ----------------
CY, CR, NT = 470, 92, 8
CA, CB = (120, 400), (540, 820)              # x dau - cuoi cuon A / cuon B (dat sat nhau, chung truc)
COLA, COLB = ORANGE, TEAL
GX, GY, GR, GANG = 800, 885, 150, 50         # dien ke cua B
BY = 690                                     # duong day mach A (pin + K)

LAB = [True, True]                                 # ve nhan chu cua bo dung cu (canh Bay tat)
def turns(c): return [c[0] + j * (c[1] - c[0]) / (NT - 1) for j in range(NT)]

def coil(d, c, col, front):
    for x in turns(c):
        if front: d.arc([x - 16, CY - CR, x + 16, CY + CR], 270, 90, fill=A(col, 0.95), width=9)
        else: d.arc([x - 16, CY - CR, x + 16, CY + CR], 90, 270, fill=mix(col, BG, 0.5), width=7)

def circuit_A(d, closed, glow):
    w = 5
    d.line([(CA[0], CY + CR - 4), (CA[0], BY), (170, BY)], fill=NAVY, width=w)
    d.line([(170, BY - 40), (170, BY + 40)], fill=NAVY, width=6)          # ban cuc dai (+)
    d.line([(194, BY - 22), (194, BY + 22)], fill=NAVY, width=12)         # ban cuc ngan (-)
    d.line([(194, BY), (280, BY)], fill=NAVY, width=w)
    dot(d, 280, BY, 9, NAVY); dot(d, 360, BY, 9, NAVY)
    ang = 0 if closed else math.radians(-34)
    d.line([(280, BY), (280 + 80 * math.cos(ang), BY + 80 * math.sin(ang))], fill=NAVY, width=8)
    d.line([(360, BY), (CA[1], BY), (CA[1], CY + CR - 4)], fill=NAVY, width=w)
    if LAB[0]:
        text(d, (182, BY + 80), f"pin {U_PIN:g} V", 56, NAVY)
        text(d, (320, BY - 70 if not closed else BY - 54), "K", 58, INK)
    if glow > 0.02: arrow(d, (CA[1], BY - 10), (CA[1], CY + CR + 20), A(RED, glow), w=6, head=18)

def galvo(d, k):
    d.line([(CB[0], CY + CR - 4), (CB[0], 615), (700, 615), (700, 660)], fill=NAVY, width=5)
    d.line([(CB[1], CY + CR - 4), (CB[1], 600), (900, 600), (900, 660)], fill=NAVY, width=5)
    card(d, (580, 660, 1040, 930), fill=WHITE, outline=NAVY, r=26, w=4)
    for x in (700, 900): dot(d, x, 660, 10, NAVY)
    d.arc([GX - GR, GY - GR, GX + GR, GY + GR], 270 - GANG - 4, 270 + GANG + 4, fill=NAVY, width=4)
    for v in range(-4, 5):
        a = math.radians(v / 4 * GANG); big = v == 0
        r0 = GR - (26 if big else 14)
        d.line([(GX + r0 * math.sin(a), GY - r0 * math.cos(a)), (GX + GR * math.sin(a), GY - GR * math.cos(a))],
               fill=NAVY, width=5 if big else 3)
    a = math.radians(clamp(k, -1.05, 1.05) * GANG * 0.85)
    d.line([(GX, GY), (GX + (GR - 10) * math.sin(a), GY - (GR - 10) * math.cos(a))], fill=RED, width=8)
    dot(d, GX, GY, 14, NAVY)

def apparatus(d, closed, ia, k):
    coil(d, CA, COLA, False); coil(d, CB, COLB, False); coil(d, CA, COLA, True); coil(d, CB, COLB, True)
    if LAB[0] and LAB[1]:
        text(d, ((CA[0] + CA[1]) / 2, CY - CR - 50), "cuộn A", 58, COLA)
        text(d, ((CB[0] + CB[1]) / 2, CY - CR - 50), "cuộn B", 58, COLB)
    circuit_A(d, closed, ia)
    galvo(d, k)

# ---------------- do thi: dong o A va kim cua B theo thoi gian ----------------
PX0, PX1 = 250, 990
YA0, YA1 = 1170, 1030                        # dong A: 0 -> on dinh
YB0, YBS = 1370, 120                         # kim B: truc 0, bien do
def X(u): return PX0 + u * (PX1 - PX0)

def plot(d, u, bands=0.0, pen=True, y_off=0):
    ya0, ya1, yb0 = YA0 + y_off, YA1 + y_off, YB0 + y_off
    if bands > 0:
        for (p, q), col in (((UA[0], UA[1]), RED), ((UA[2], UA[3]), BLUE)):
            d.rounded_rectangle([X(p) - 12, ya1 - 20, X(q) + 12, yb0 + YBS + 10], radius=14,
                                fill=A(mix(col, WHITE, 0.85), bands), outline=A(col, bands), width=3)
    xl = X((UA[1] + UA[2]) / 2)                  # nhan truc dat giua hai dai (khong de len dai mau)
    for y0, y1, lab, col, yl in ((ya0, ya1 - 40, "dòng ở A", COLA, (ya0 + ya1) / 2 + 10), (yb0 + YBS + 10, yb0 - YBS - 30, "kim B", COLB, yb0 - YBS + 10)):
        d.line([(PX0, y0), (PX0, y1)], fill=NAVY, width=4)
        d.polygon([(PX0, y1 - 14), (PX0 - 10, y1 + 6), (PX0 + 10, y1 + 6)], fill=NAVY)
        text(d, (xl, yl), lab, 56, col)
    d.line([(PX0, ya0), (PX1 + 10, ya0)], fill=NAVY, width=4)
    d.line([(PX0, yb0), (PX1 + 10, yb0)], fill=NAVY, width=4)
    text(d, (PX0 - 16, yb0 - 80), "phải", 56, NAVY, anchor="rm")
    text(d, (PX0 - 16, yb0 + 80), "trái", 56, NAVY, anchor="rm")
    text(d, (PX0 - 16, yb0), "0", 56, NAVY, anchor="rm")
    for uu, lab in (((UA[0] + UA[1]) / 2, "đóng"), ((UA[1] + UA[2]) / 2, "giữ"), ((UA[2] + UA[3]) / 2, "ngắt")):
        text(d, (X(uu), yb0 + YBS + 56), lab, 56, INK)
    if u > 0:
        us = sorted(set([k / 500 * u for k in range(501)] + [x for x in UA if x <= u]))
        d.line([(X(v), ya0 - iA(v) * (ya0 - ya1)) for v in us], fill=COLA, width=7, joint="curve")
        d.line([(X(v), yb0 - kim(v) * YBS) for v in us], fill=PURPLE, width=7, joint="curve")
        if pen and u < 0.999:
            dot(d, X(u), ya0 - iA(u) * (ya0 - ya1), 12, RED, outline=WHITE)
            dot(d, X(u), yb0 - kim(u) * YBS, 12, RED, outline=WHITE)

def plot_card(d, y0=940, y1=1625):
    card(d, (40, y0, 1040, y1), fill=WHITE, outline=LIGHT, w=3)

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.3
DGREEN, DRED = (10, 110, 50), (185, 28, 28)


def pill(d, s, y, a, color=NAVY, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)


def s_hook(img, d, t, sc):
    M = sc["M"]
    apparatus(d, False, 0.0, 0.0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 990 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    text(d, (W / 2, y0 + 170), "Đóng K: kim lệch phải.", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 260), "Lúc ngắt K: kim B thế nào?", 60, INK, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.1
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([110, y0 + 350, 970, y0 + 450], radius=45, fill=A((237, 233, 254), a))
        if p < 1: d.rounded_rectangle([110, y0 + 350, 110 + max(90, 860 * (1 - p)), y0 + 450], radius=45, fill=A((76, 29, 149), a))


# ---------------- canh 2: Tien hanh (dong - giu - ngat lien mach, MOT canh) ----------------
def u_of(t, sc):
    M = sc["M"]
    return float(np.interp(t, [M[0] + 0.3, M[0] + 2.2, M[0] + 3.4, M[1] + 0.5, M[1] + 1.7, sc["T"] - 0.3],
                           [0, UA[0], UA[1], UA[2], UA[3], 1.0]))

def chips(d, cur):
    for j, s in enumerate(("Đóng", "Giữ", "Ngắt")):
        x0 = 60 + j * 330; box = (x0, 226, x0 + 300, 306)
        if j == cur: card(d, box, fill=ORANGE, r=40); text(d, (x0 + 150, 266), s, 56, WHITE)
        elif j < cur: card(d, box, fill=LIGHT, r=40); text(d, (x0 + 150, 266), s, 56, INK)
        else: card(d, box, fill=None, outline=LIGHT, r=40, w=3); text(d, (x0 + 150, 266), s, 56, NAVY)

def state(u):
    closed = UA[0] - 1e-6 <= u < UA[2] + 1e-6
    return closed, iA(u), kim(u)

def s_do(img, d, t, sc):
    u = u_of(t, sc); closed, ia, k = state(u)
    chips(d, 0 if u < UA[1] else (1 if u < UA[2] else 2))
    LAB[1] = False                               # chip Dong/Giu/Ngat nam cho nhan cuon day
    try: apparatus(d, closed, ia, k)
    finally: LAB[1] = True
    plot_card(d); plot(d, u)
    if (UA[0] <= u < UA[1]) or (UA[2] <= u < UA[3]):
        wd = tw(d, "CHIẾU CHẬM", F(56)) + 50
        card(d, (1020 - wd, 952, 1020, 1030), fill=ORANGE, r=39); text(d, (1020 - wd / 2, 991), "CHIẾU CHẬM", 56, WHITE)

def _kiem_vat_li():
    """Kim B chi lech khi dong A dang doi; phai khi tang, trai khi giam; K mo thi dong A = 0; giu dong thi kim 0."""
    bad = []
    for n in range(2001):
        u = n / 2000; closed, ia, k = state(u); da = (iA(min(1, u + 1e-6)) - iA(max(0, u - 1e-6)))
        if abs(da) < 1e-12 and abs(k) > 1e-6: bad.append((round(u, 3), "dong A khong doi ma kim lech"))
        if da > 1e-8 and not k > 0: bad.append((round(u, 3), "dong A tang ma kim khong lech phai"))
        if da < -1e-8 and not k < 0: bad.append((round(u, 3), "dong A giam ma kim khong lech trai"))
        if u < UA[0] and ia > 0: bad.append((round(u, 3), "K mo ma co dong"))
    # bang so_lieu_mau: (thoi diem, dau kim) tai giua moi doan
    exp = [((0 + UA[0]) / 2, 0), ((UA[0] + UA[1]) / 2, 1), ((UA[1] + UA[2]) / 2, 0), ((UA[2] + UA[3]) / 2, -1), ((UA[3] + 1) / 2, 0)]
    for u, s in exp:
        k = kim(u)
        if (s == 0 and abs(k) > 1e-9) or (s and (k > 0) != (s > 0)): bad.append((u, "lech so_lieu_mau"))
    clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]
    if u_of(sc["M"][1] - 0.05, sc) > UA[2]: bad.append("ngat truoc phu de Ngat")
    if u_of(sc["T"] - 0.3, sc) < 0.999: bad.append("do thi chua ve het")
    return bad

def _kiem_so():
    return [] if abs(U_PIN - 4 * 1.5) < 1e-9 else ["U pin khac 4 x 1,5 V"]

# ---------------- canh 3: Dap an + Rut ra ----------------
DA_K = 2.8
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    pill(d, "ĐÁP ÁN: lệch trái, rồi về 0", 290, ka)
    hb = appear(t, 0.6, 0.5)
    card(d, (40, 350, 1040, 1060), fill=WHITE, outline=LIGHT, w=3)
    plot(d, 1.0, bands=0.9 * hb, pen=False, y_off=-600)
    if t > DA_K:                                  # cham do chay lai doc hai duong (lap 3 s) cho hinh khong dung
        u = ((t - DA_K) % 3.0) / 3.0
        dot(d, X(u), YA0 - 600 - iA(u) * (YA0 - YA1), 12, RED, outline=WHITE)
        dot(d, X(u), YB0 - 600 - kim(u) * YBS, 12, RED, outline=WHITE)
    kr = appear(t, DA_K, 0.45)
    if kr > 0:
        card(d, (40, 1090, 1040, 1300), fill=A(WHITE, kr), outline=A(PURPLE, kr), w=5)
        text(d, (W / 2, 1150), "Đóng: dòng A tăng", 58, RED, alpha=kr)
        text(d, (W / 2, 1240), "Ngắt: dòng A giảm", 58, BLUE, alpha=kr)
    k1 = appear(t, M[1] + 0.3, 0.45)
    if k1 > 0:
        card(d, (40, 1330, 1040, 1470), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        text(d, (W / 2, 1400), "Dòng A đổi → B có dòng", 58, DGREEN, alpha=k1)


# ---------------- canh 4: Bay + Chua noi duoc ----------------
BAY_ST, BAY_OK = 2.2, 2.7
def s_bay(img, d, t, sc):
    M = sc["M"]
    ph = (t % 2.4) / 2.4                          # lap lai luc ngat: kim lech trai roi ve 0
    u = UA[2] + (UA[3] - UA[2]) * clamp(ph / 0.6) if ph < 0.85 else UA[2]
    closed, ia, kb = state(u)
    LAB[0] = False
    try: apparatus(d, closed, ia, kb)
    finally: LAB[0] = True
    k2 = appear(t, M[1] + 0.3, 0.45); a1 = appear(t, 0.2, 0.45) * (1 - k2)
    y0 = 990
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pill(d, "BẪY", y0 + 62, a1, DRED)
        ks = clamp((t - BAY_ST) / 0.4)
        for j, q in enumerate(("“Lúc ngắt hết dòng", "nên kim không lệch”")):
            yy = y0 + 170 + 85 * j
            text(d, (W / 2, yy), q, 58, INK, alpha=a1)
            if ks > 0:
                lw = tw(d, q, F(58))
                d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=7)
        text(d, (W / 2, y0 + 380), "✓ Đang giảm vẫn lệch", 58, DGREEN, alpha=a1 * appear(t, BAY_OK, 0.4))
    if k2 > 0:
        card(d, (40, y0, 1040, y0 + 540), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 80), "Chưa nói được:", 60, NAVY, alpha=k2)
        text(d, (90, y0 + 220), "• Dòng B lớn cỡ nào", 58, INK, anchor="lm", alpha=k2)
        text(d, (90, y0 + 330), "• Phía lệch tuỳ cách nối", 58, INK, anchor="lm", alpha=k2)


# ---------------- canh 5: Chot + THU NGHI ----------------
END_Q, END_C = 0.2, 3.0
def s_end(img, d, t, sc):
    k0 = appear(t, END_C, 0.5)
    card(d, (50, 265, 1030, 425), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    text(d, (W / 2, 345), "Dòng A đổi → B có dòng", 58, DGREEN, alpha=k0)
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 455, 1040, 1580), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", 518, k1, ORANGE)
    text(d, (W / 2, 625), "K vẫn đóng. Vặn biến trở", 60, INK, alpha=k1)
    text(d, (W / 2, 705), "cho dòng ở A giảm dần.", 60, INK, alpha=k1)
    text(d, (W / 2, 785), "Kim B thế nào?", 60, INK, alpha=k1)
    if k1 > 0:
        cy = 1060
        for x0, x1, col in ((230, 430, COLA), (620, 820, COLB)):
            for j in range(6):
                x = x0 + j * (x1 - x0) / 5
                d.arc([x - 14, cy - 70, x + 14, cy + 70], 0, 360, fill=A(col, k1), width=7)
        sx = 200 + 640 * (0.5 - 0.5 * math.cos(2 * math.pi * t / 3.0))              # bien tro dai, con chay chay qua lai
        d.rounded_rectangle([200, cy + 150, 880, cy + 230], radius=14, fill=A((254, 243, 199), k1), outline=A(INK, k1), width=6)
        d.rounded_rectangle([200, cy + 150, max(214, sx), cy + 230], radius=14, fill=A(ORANGE, k1))
        d.polygon([(sx, cy + 150), (sx - 26, cy + 105), (sx + 26, cy + 105)], fill=A(PURPLE, k1))
        text(d, (W / 2, 1420), "kim B = ?", 62, ORANGE, alpha=k1)


def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + M[0] + 2.2, "tap"), (do["t0"] + M[1] + 0.5, "tap"),
            (da["t0"] + 0.15, "ding"), (b["t0"] + BAY_ST, "buzz"), (e["t0"] + END_Q + 0.1, "open")]

CLIP = dict(id="tn-l9-camung-02", header="KHTN 9 · THÍ NGHIỆM", footer="Cảm ứng điện từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Nam châm điện và cuộn dây", draw=s_hook, tail=THINK_END, caps=[
   ("A nối pin, B nối điện kế.", 3.0),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Đóng K rồi giữ đóng.", 5.4),
   ("Bây giờ ngắt K.", 4.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.8, caps=[
   ("Ngược phía lúc đóng.", 5.2),
   ("Nam châm điện cũng tạo dòng.", 4.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Đúng không?", 4.8),
   ("Còn bỏ ngỏ.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự nghĩ.", 7.6)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch số:", _kiem_so() or "không")
        print("lệch vật lí:", _kiem_vat_li() or "không")
