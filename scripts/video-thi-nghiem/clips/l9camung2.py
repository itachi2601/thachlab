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
    text(d, (182, BY + 76), f"pin {U_PIN:g} V", 38, MUTED, bold=False)
    text(d, (320, BY - 60 if not closed else BY - 44), "K", 40, INK)
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
    text(d, (612, 900), "điện kế", 36, MUTED, bold=False, anchor="lm")

def apparatus(d, closed, ia, k):
    coil(d, CA, COLA, False); coil(d, CB, COLB, False); coil(d, CA, COLA, True); coil(d, CB, COLB, True)
    text(d, ((CA[0] + CA[1]) / 2, CY - CR - 40), "cuộn A", 40, COLA)
    text(d, ((CB[0] + CB[1]) / 2, CY - CR - 40), "cuộn B", 40, COLB)
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
    for y0, y1, lab, col in ((ya0, ya1 - 40, "dòng ở A", COLA), (yb0 + YBS + 10, yb0 - YBS - 30, "kim B", COLB)):
        d.line([(PX0, y0), (PX0, y1)], fill=NAVY, width=4)
        d.polygon([(PX0, y1 - 14), (PX0 - 10, y1 + 6), (PX0 + 10, y1 + 6)], fill=NAVY)
        text(d, (PX0 - 16, y1 + 20), lab, 38, col, anchor="rm")
    d.line([(PX0, ya0), (PX1 + 10, ya0)], fill=NAVY, width=4)
    d.line([(PX0, yb0), (PX1 + 10, yb0)], fill=NAVY, width=4)
    text(d, (PX0 - 16, yb0 - 70), "phải", 36, MUTED, bold=False, anchor="rm")
    text(d, (PX0 - 16, yb0 + 70), "trái", 36, MUTED, bold=False, anchor="rm")
    text(d, (PX0 - 16, yb0), "0", 36, MUTED, bold=False, anchor="rm")
    for uu, lab in (((UA[0] + UA[1]) / 2, "đóng"), ((UA[1] + UA[2]) / 2, "giữ"), ((UA[2] + UA[3]) / 2, "ngắt")):
        text(d, (X(uu), yb0 + YBS + 50), lab, 38, INK)
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
THINK_END = 0.6
def s_hook(img, d, t, sc):
    M = sc["M"]
    apparatus(d, False, 0.0, 0.0)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1010 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    text(d, (W / 2, y0 + 145), "Lúc đóng K: kim lệch phải.", 44, INK, alpha=a)
    text(d, (W / 2, y0 + 215), "Giữ một lúc, rồi ngắt K.", 44, INK, alpha=a)
    text(d, (W / 2, y0 + 295), "Lúc ngắt, kim của B thế nào?", 48, PURPLE, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 370, 940, y0 + 382], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 370, 140 + 800 * (1 - p), y0 + 382], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (dong - giu - ngat lien mach, MOT canh) ----------------
def u_of(t, sc):
    M = sc["M"]
    return float(np.interp(t, [M[0] + 0.3, M[0] + 0.8, M[0] + 2.0, M[1] + 0.5, M[1] + 1.7, sc["T"] - 0.3],
                           [0, UA[0], UA[1], UA[2], UA[3], 1.0]))

def chips(d, cur):
    for j, s in enumerate(("Đóng", "Giữ", "Ngắt")):
        x0 = 60 + j * 330; box = (x0, 236, x0 + 300, 300)
        if j == cur: card(d, box, fill=ORANGE, r=32); text(d, (x0 + 150, 268), s, 40, WHITE)
        elif j < cur: card(d, box, fill=LIGHT, r=32); text(d, (x0 + 150, 268), s, 40, INK)
        else: card(d, box, fill=None, outline=LIGHT, r=32, w=3); text(d, (x0 + 150, 268), s, 40, GRAY)

def state(u):
    closed = UA[0] - 1e-6 <= u < UA[2] + 1e-6
    return closed, iA(u), kim(u)

def s_do(img, d, t, sc):
    u = u_of(t, sc); closed, ia, k = state(u)
    chips(d, 0 if u < UA[1] else (1 if u < UA[2] else 2))
    apparatus(d, closed, ia, k)
    plot_card(d); plot(d, u)
    if (UA[0] <= u < UA[1]) or (UA[2] <= u < UA[3]):
        wd = tw(d, "CHIẾU CHẬM", F(38)) + 44
        card(d, (1020 - wd, 956, 1020, 1002), fill=ORANGE, r=23); text(d, (1020 - wd / 2, 979), "CHIẾU CHẬM", 38, WHITE)

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
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · ngược phía lúc đóng, rồi về 0"
    fs = 44 if tw(d, lab, F(44)) <= 940 else 40
    pw = tw(d, lab, F(fs)) + 60
    card(d, (W / 2 - pw / 2, 262, W / 2 + pw / 2, 338), fill=A(NAVY, ka), r=36)
    text(d, (W / 2, 300), lab, fs, WHITE, alpha=ka)
    hb = appear(t, 0.6, 0.5)
    card(d, (40, 350, 1040, 1040), fill=WHITE, outline=LIGHT, w=3)
    plot(d, 1.0, bands=0.9 * hb, pen=False, y_off=-610)
    kr = appear(t, 1.2, 0.45)
    if kr > 0:
        card(d, (40, 1080, 1040, 1300), fill=A(WHITE, kr), outline=A(PURPLE, kr), w=5)
        text(d, (90, 1145), "Đóng: dòng A tăng → lệch phải", 46, RED, anchor="lm", alpha=kr)
        text(d, (90, 1235), "Ngắt: dòng A giảm → lệch trái", 46, BLUE, anchor="lm", alpha=kr)
    k1 = appear(t, M[1] - 0.1, 0.45)
    if k1 > 0:
        card(d, (40, 1340, 1040, 1580), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        text(d, (W / 2, 1410), "Dòng ở A đang đổi", 50, GREEN, alpha=k1)
        text(d, (W / 2, 1505), "→ cuộn B có dòng", 50, GREEN, alpha=k1)

# ---------------- canh 4: Bay + Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    closed, ia, kb = state((UA[2] + UA[3]) / 2)
    apparatus(d, closed, ia, kb)
    k2 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.45) * (1 - k2)
    if a1 > 0:
        y0 = 1010
        card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(RED, a1), r=31)
        text(d, (W / 2, y0 + 57), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - M[0] - 1.6) / 0.4)
        q = "“Lúc ngắt hết dòng nên kim không lệch”"
        lw = tw(d, q, F(44)); yy = y0 + 180
        text(d, (W / 2, yy), q, 44, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
        text(d, (W / 2, y0 + 300), "✓ Dòng đang giảm: kim lệch", 46, GREEN, alpha=a1 * appear(t, M[0] + 2.2, 0.4))
    if k2 > 0:
        y0 = 1010
        card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 48, NAVY, alpha=k2)
        for j, s in enumerate(("• Dòng ở B lớn bao nhiêu", "• Phía lệch tuỳ cách nối")):
            text(d, (90, y0 + 190 + j * 110), s, 44, INK, bold=False, anchor="lm", alpha=k2 * appear(t, M[1] + 0.3 + 0.6 * j, 0.4))

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
T_CHOT = 4.0
def s_end(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 > 0:
        card(d, (40, 620, 1040, 1600), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
        pw = tw(d, "THỬ NGHĨ", F(38)) + 52
        card(d, (W / 2 - pw / 2, 650, W / 2 + pw / 2, 714), fill=A(ORANGE, k1), r=32)
        text(d, (W / 2, 682), "THỬ NGHĨ", 38, WHITE, alpha=k1)
        ctext(d, 820, "K vẫn đóng. Vặn biến trở cho\ndòng ở A giảm dần. Kim B có lệch?", 46, INK, maxw=940,
              alpha=appear(t, M[0] + 0.4, 0.5))
        ka = appear(t, M[0] + 0.6, 0.5) * k1
        cy = 1070
        for x0, x1, col in ((260, 440, COLA), (620, 800, COLB)):
            for j in range(6):
                x = x0 + j * (x1 - x0) / 5
                d.arc([x - 12, cy - 60, x + 12, cy + 60], 0, 360, fill=A(col, ka), width=6)
        d.rectangle([250, cy + 100, 450, cy + 140], outline=A(INK, ka), width=5)   # bien tro: hop + mui ten cheo
        arrow(d, (230, cy + 170), (470, cy + 70), A(PURPLE, ka), w=5, head=18)
        text(d, (910, cy), "?", 72, PURPLE, alpha=ka)
        kh = appear(t, M[0] + 2.9, 0.5)
        card(d, (110, 1260, 970, 1500), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1380, "Dòng ở A có đổi không?", 44, ORANGE, maxw=820, alpha=kh)
    k0 = appear(t, M[0] + T_CHOT, 0.5)
    if k0 > 0:
        card(d, (60, 260, 1020, 560), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
        ctext(d, 410, "Dòng ở A thay đổi → B có dòng cảm ứng", 50, GREEN, maxw=880, alpha=k0)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    M = do["M"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding"),
            (do["t0"] + M[0] + 0.8, "tap"), (do["t0"] + M[1] + 0.5, "tap"),
            (da["t0"] + 0.15, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l9-camung-02", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Cảm ứng điện từ · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Nam châm điện và cuộn dây", draw=s_hook, tail=THINK_END, caps=[
   ("Cuộn A nối pin, cuộn B nối điện kế.", 3.6),
   ("Tự trả lời trước khi xem.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Đóng K rồi giữ đóng.", 5.4),
   ("Bây giờ ngắt K.", 4.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.8, caps=[
   ("Ngược phía với lúc đóng.", 3.8),
   ("Nam châm điện cũng tạo được dòng.", 4.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Có đúng không?", 4.4),
   ("Chưa nói được.", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.2, caps=[
   ("Tự trả lời trước khi xem.", 6.4)]),
])

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch số:", _kiem_so() or "không")
        print("lệch vật lí:", _kiem_vat_li() or "không")
