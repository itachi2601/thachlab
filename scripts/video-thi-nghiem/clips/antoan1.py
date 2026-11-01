# Clip: tn-l10-an-toan-01 - Num bo nguon o vach 3, 6, 9, 12 V: von ke chi bao nhieu (1/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-an-toan-01.json:
#   so_lieu_mau: vach 3; 6; 9; 12 V -> von ke doc 3,1; 6,2; 9,3; 12,4 V (lam tron 0,1 V)
#   mo_hinh.gia_thiet: nguon khong mac tai (ghi len man); an_toan: giao vien cho phep, tat cong tac khi noi, dung cuc.
# Bai: sau hop co bang + cau "Doc bang: so chi cao hon vach 0,1-0,4 V, co phai do sai?" -> clip KHONG noi % lech,
#   KHONG noi "sai so cua bo nguon", khong co cot "Lech"; chi de cau do o the "Chua noi duoc gi".
# Bo cuc: bo nguon (num + cong tac + 2 cuc Output) tren, von ke kim ben phai mac SONG SONG 2 cuc (do vao +), bang trai.
#   Kim + so chi doi CUNG LUC voi num (cung 0,5 s); so chi chi hien khi kim dung (khong hien so noi suy).
# Canh: Du doan (K10, khong nut A-D) -> Tien hanh (tat nguon khi noi, bat, xoay 4 vach) + DAP AN
#       -> Rut ra (so do song song, vach gan dung, chua noi duoc) -> Bay (cam dao day: kim lech nguoc)
#       -> Chot + THU NGHI (thao day: viec dau tien? - chua tung hien tren man o canh chot).
from engine import *

VACH = (3, 6, 9, 12)                             # so_lieu_mau, cot "Vach (V)"
DOC = (3.1, 6.2, 9.3, 12.4)                      # so_lieu_mau, cot "V doc (V)"
def fm(x): return f"{x:.1f}".replace(".", ",")

PANEL = (60, 300, 1020, 720)
KN = (250, 500)                                  # tam num
ANG = {3: -120, 6: -40, 9: 40, 12: 120}          # goc vach (do, tinh tu dinh, chieu kim dong ho)
SW = (520, 470)                                  # cong tac
TP, TM = (720, 520), (900, 520)                  # cuc Output + va -
MB = (520, 820, 1020, 1290)                      # than von ke
PV, R = (770, 1210), 230                         # truc kim, ban kinh thang
VP, VM = (590, 840), (950, 840)                  # cuc + va - cua von ke
VMAX = 15
DARK = (40, 44, 56)

def vang(v): return math.radians(140 - 100 * v / VMAX)   # 0 V -> 140 do, 15 V -> 40 do

def knob_ang(vach): return ANG[vach]

def supply(d, kang, on, glow=0.0):
    card(d, PANEL, fill=(214, 219, 230), outline=(120, 126, 145), r=30, w=5)
    # day nguon Input ra mep trai
    d.line([(PANEL[0], 650), (30, 658), (0, 690)], fill=DARK, width=12, joint="curve")
    text(d, (100, 668), "Input 220 V ~", 40, INK, anchor="lm")
    # num
    text(d, (KN[0], 340), "Output (V)", 40, INK)
    for v, a in ANG.items():
        r_ = math.radians(a)
        x1, y1 = KN[0] + 92 * math.sin(r_), KN[1] - 92 * math.cos(r_)
        x2, y2 = KN[0] + 108 * math.sin(r_), KN[1] - 108 * math.cos(r_)
        d.line([(x1, y1), (x2, y2)], fill=INK, width=5)
        text(d, (KN[0] + 140 * math.sin(r_), KN[1] - 140 * math.cos(r_)), str(v), 40, INK)
    dot(d, KN[0], KN[1], 78, (60, 66, 84))
    dot(d, KN[0], KN[1], 62, (88, 95, 116))
    r_ = math.radians(kang)
    d.line([(KN[0] + 14 * math.sin(r_), KN[1] - 14 * math.cos(r_)),
            (KN[0] + 70 * math.sin(r_), KN[1] - 70 * math.cos(r_))], fill=WHITE, width=10)
    # cong tac + den bao
    d.rounded_rectangle([SW[0] - 60, SW[1] - 80, SW[0] + 60, SW[1] + 80], radius=16, fill=DARK)
    yk = SW[1] - 40 if on else SW[1] + 40
    d.rounded_rectangle([SW[0] - 46, yk - 34, SW[0] + 46, yk + 34], radius=12, fill=(235, 238, 245))
    text(d, (SW[0], yk), "BẬT" if on else "TẮT", 36, GREEN if on else RED)
    dot(d, SW[0], SW[1] + 130, 20, (60, 220, 110) if on else (150, 155, 170), outline=DARK)
    if glow > 0:
        d.rounded_rectangle([SW[0] - 76, SW[1] - 96, SW[0] + 76, SW[1] + 96], radius=22, outline=A(ORANGE, glow), width=7)
    # cuc Output
    text(d, ((TP[0] + TM[0]) / 2, 360), "Output DC", 40, INK)
    for (x, y), col, s in ((TP, RED, "+"), (TM, DARK, "−")):
        dot(d, x, y, 38, col, outline=(30, 30, 30)); dot(d, x, y, 14, (200, 200, 200))
        text(d, (x - 74 if s == "+" else x + 74, y), s, 56, col)

def wire(d, p1, p2, col, prog=1.0, sag=40):
    pts = []
    for i in range(41):
        u = i / 40
        x = lerp(p1[0], p2[0], u) + sag * math.sin(math.pi * u); y = lerp(p1[1], p2[1], u)   # cong ngang
        pts.append((x, y))
    n = max(2, int(41 * prog))
    d.line(pts[:n], fill=col, width=10, joint="curve")

def wires(d, swap=False):
    if not swap:
        wire(d, (TP[0], TP[1] + 30), VP, RED, sag=-30)
        wire(d, (TM[0], TM[1] + 30), VM, DARK, sag=30)
    else:                                        # day do cua von ke vao cuc -, day den vao cuc +
        wire(d, (TM[0], TM[1] + 30), VP, RED, sag=0)
        wire(d, (TP[0], TP[1] + 30), VM, DARK, sag=0)

def meter(d, v, hide=False, read=None, pinned=False):
    card(d, MB, fill=WHITE, outline=NAVY, r=26, w=5)
    for (x, y), col, s in ((VP, RED, "+"), (VM, DARK, "−")):
        dot(d, x, y, 20, col, outline=(30, 30, 30))
        text(d, (x, y + 46), s, 48, col)
    d.arc([PV[0] - R, PV[1] - R, PV[0] + R, PV[1] + R], 220, 320, fill=NAVY, width=4)
    for k in range(0, 2 * VMAX + 1):
        v_ = k / 2; a = vang(v_)
        L = 30 if k % 10 == 0 else (20 if k % 2 == 0 else 11)
        c, s_ = math.cos(a), math.sin(a)
        d.line([(PV[0] + R * c, PV[1] - R * s_), (PV[0] + (R - L) * c, PV[1] - (R - L) * s_)],
               fill=NAVY, width=4 if L == 30 else 3)
    for v_ in (0, 5, 10, 15):
        a = vang(v_); text(d, (PV[0] + (R + 38) * math.cos(a), PV[1] - (R + 38) * math.sin(a)), str(v_), 40, INK)
    text(d, (590, 1230), "V", 52, NAVY)
    if hide:
        d.rounded_rectangle([535, 922, 1005, 1190], radius=24, fill=(245, 243, 255), outline=PURPLE, width=4)
        text(d, (770, 1056), "?", 80, PURPLE)
    else:
        a = vang(v) if not pinned else math.radians(150)
        d.line([PV, (PV[0] + (R - 14) * math.cos(a), PV[1] - (R - 14) * math.sin(a))], fill=RED, width=6)
    dot(d, PV[0], PV[1], 14, NAVY)
    if read is not None:
        text(d, (PV[0], 1255), read, 40, RED if read[0].isdigit() else MUTED)

def table(d, n_rows, hide=False, hl=-1):
    card(d, (50, 820, 490, 1290), fill=WHITE, outline=NAVY, r=26, w=4)
    xs = (160, 370)
    text(d, (xs[0], 868), "Vạch", 42, INK); text(d, (xs[1], 868), "Số chỉ", 42, INK)
    text(d, (xs[0], 916), "(V)", 40, MUTED); text(d, (xs[1], 916), "(V)", 40, MUTED)
    d.line([(70, 948), (470, 948)], fill=LIGHT, width=4); d.line([(265, 850), (265, 1270)], fill=LIGHT, width=3)
    for i, v in enumerate(VACH):
        y = 1000 + i * 72
        if i == hl: d.rounded_rectangle([66, y - 32, 474, y + 32], radius=14, fill=(255, 241, 222))
        text(d, (xs[0], y), str(v), 44, BLUE)
        if hide: text(d, (xs[1], y), "?", 44, PURPLE)
        elif i < n_rows: text(d, (xs[1], y), fm(DOC[i]), 44, RED)

# ---------------- trang thai tien hanh (dong bo num - kim - so - bang) ----------------
STEP, TURN = 1.5, 0.5
def state(t, sc):
    """-> (goc num, bat?, v kim, so chi dang hien hoac None, so hang bang, hang dang lam)"""
    M = sc["M"]; ton = M[1] + 0.2
    if t < ton: return knob_ang(3), False, 0.0, None, 0, -1
    for i in range(3, -1, -1):
        s = ton + i * STEP
        if t >= s: break
    k = ease((t - s) / TURN)
    if i == 0: kang = knob_ang(3); v = lerp(0.0, DOC[0], k)
    else:
        kang = lerp(knob_ang(VACH[i - 1]), knob_ang(VACH[i]), k); v = lerp(DOC[i - 1], DOC[i], k)
    done = t >= s + TURN
    rows = i + 1 if done else i
    return kang, True, v, (fm(DOC[i]) + " V") if done else "…", rows, i

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    supply(d, knob_ang(3), False); wires(d); meter(d, 0, hide=True); table(d, 0, hide=True)
    M = sc["M"]; k = appear(t, M[1] - 0.4, 0.5)
    if k <= 0: return
    y0 = 1320 + (1 - k) * 30
    card(d, (50, y0, 1030, y0 + 280), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "Dự đoán", F(40)) + 56
    card(d, (W / 2 - pw / 2, y0 + 22, W / 2 + pw / 2, y0 + 84), fill=A(PURPLE, k), r=30)
    text(d, (W / 2, y0 + 53), "Dự đoán", 40, WHITE, alpha=k)
    ctext(d, y0 + 160, "Số chỉ vôn kế so với vạch núm?", 46, INK, alpha=k)
    t1, t2 = M[1] - 0.2, sc["T"] - 0.2; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([200, y0 + 248, 880, y0 + 262], radius=7, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([200, y0 + 248, 200 + 680 * (1 - q), y0 + 262], radius=7, fill=A(PURPLE, k))

# ---------------- canh 2: tien hanh ----------------
def s_do(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    kang, on, v, read, rows, cur = state(t, sc)
    glow = 0.0
    if t < M[1]: glow = 0.5 + 0.5 * math.sin(2 * math.pi * 1.2 * t)
    supply(d, kang, on, glow)
    wires(d)
    meter(d, v, read=read if on else "0 V")
    table(d, rows, hl=cur)
    if t < M[1] + 0.2:                           # ghi chu an toan + gia thiet
        a = appear(t, M[0] + 0.2, 0.4)
        card(d, (50, 1330, 1030, 1570), fill=A(WHITE, a), outline=A(GREEN, a), w=5)
        ctext(d, 1400, "✓ Giáo viên cho phép", 44, GREEN, alpha=a)
        ctext(d, 1480, "Chỉ có vôn kế, chưa nối tải", 42, INK, alpha=a)
    if M[1] + 0.2 <= t < M[2]:                   # dai vach dang lam (khong them so moi)
        a = appear(t, M[1] + 0.2, 0.4)
        for i, v_ in enumerate(VACH):
            x = 230 + i * 207; on_ = i == cur
            card(d, (x - 85, 1380, x + 85, 1480), fill=A(BLUE if on_ else WHITE, a), outline=A(BLUE, a), r=24, w=4)
            text(d, (x, 1430), f"{v_} V", 44, WHITE if on_ else BLUE, alpha=a)
    kc = appear(t, M[2], 0.4)
    if kc > 0:
        card(d, (50, 1330, 1030, 1570), fill=A((220, 252, 231), kc), outline=A(GREEN, kc), w=5)
        text(d, (W / 2, 1395), "ĐÁP ÁN", 44, GREEN, alpha=kc)
        ctext(d, 1485, "Số chỉ luôn cao hơn vạch một chút", 44, INK, alpha=kc)

# ---------------- canh 3: rut ra ----------------
def s_rut(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.2)
    card(d, (40, 270, 1040, 820), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    # so do: nguon (hai cuc) + von ke mac song song
    bx0, by0, bx1, by1 = 120, 360, 420, 560
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=20, fill=A((214, 219, 230), a), outline=A(NAVY, a), width=4)
    text(d, ((bx0 + bx1) / 2, 410), "Bộ nguồn", 42, INK, alpha=a)
    text(d, ((bx0 + bx1) / 2, 480), "vạch 6 V", 40, BLUE, alpha=a)
    ptop, pbot = (420, 395), (420, 525)          # cuc + (tren), cuc - (duoi)
    vx, vy = 760, 460
    d.line([ptop, (620, 395), (620, 330), (vx, 330), (vx, vy - 62)], fill=A(RED, a), width=7)
    d.line([pbot, (620, 525), (620, 610), (vx, 610), (vx, vy + 62)], fill=A(DARK, a), width=7)
    dot(d, ptop[0], ptop[1], 12, A(RED, a)); dot(d, pbot[0], pbot[1], 12, A(DARK, a))
    text(d, (450, 360), "+", 48, RED, alpha=a); text(d, (450, 565), "−", 48, DARK, alpha=a)
    d.ellipse([vx - 62, vy - 62, vx + 62, vy + 62], fill=A(WHITE, a), outline=A(NAVY, a), width=6)
    text(d, (vx, vy), "V", 56, NAVY, alpha=a)
    text(d, (vx + 80, vy - 50), "+", 44, RED, alpha=a, anchor="lm")
    text(d, (vx + 80, vy + 50), "−", 44, DARK, alpha=a, anchor="lm")
    kb = appear(t, 0.9, 0.4)
    if kb > 0:
        text(d, (W / 2, 700), "Mắc song song hai cực", 42, INK, alpha=kb)
        text(d, (W / 2, 765), "6,2 V: điện áp giữa hai cực", 40, BLUE, alpha=kb)
    rows = [("Vạch núm chỉ gần đúng", INK)]
    for j, (s1, col) in enumerate(rows):         # moi dong mot nhip
        kr = appear(t, M[1] + 0.1 + j * 1.6, 0.4)
        if kr > 0: ctext(d, 990 + j * 90, s1, 46, col, alpha=kr)
    k3 = appear(t, M[2] - 0.1, 0.45)
    if k3 > 0:
        y1 = 1150 + (1 - k3) * 30
        card(d, (40, y1, 1040, y1 + 330), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y1 + 60), "Chưa nói được gì?", 44, NAVY, alpha=k3)
        ctext(d, y1 + 150, "Lệch vì đo sai hay vì nguồn?", 42, BLUE, alpha=k3)
        ctext(d, y1 + 240, "Nối dụng cụ vào: chưa đo", 42, BLUE, alpha=k3)

# ---------------- canh 4: bay ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    TON = M[1] + 2.5                             # cam xong day (nguon TAT) -> tu luc dap an moi bat nguon
    kon = ease((t - TON) / 0.3)
    supply(d, knob_ang(6), t >= TON)
    wires(d, swap=True)
    meter(d, lerp(0.0, -1.5, kon))               # -1,5 tren thang = kim dap vao chot trai (150 do)
    a = appear(t, 0.1, 0.4)
    card(d, (50, 820, 490, 1290), fill=A(WHITE, a), outline=A(RED, a), w=6)
    pw = tw(d, "Bẫy", F(40)) + 60
    card(d, (270 - pw / 2, 845, 270 + pw / 2, 905), fill=A(RED, a), r=30)
    text(d, (270, 875), "Bẫy", 40, WHITE, alpha=a)
    for j, s in enumerate(("Cắm đảo dây,", "vẫn đọc", "được?")):
        text(d, (270, 1010 + j * 72), s, 46, INK, alpha=a)
    kf = appear(t, TON + 0.3, 0.3)               # kim dap vao chot trai: chop do cung dong dap an
    if kf > 0:
        ap = math.radians(150)
        tip = (PV[0] + (R - 14) * math.cos(ap), PV[1] - (R - 14) * math.sin(ap))
        d.ellipse([tip[0] - 30, tip[1] - 30, tip[0] + 30, tip[1] + 30], outline=A(RED, kf), width=6)
    ok = appear(t, TON, 0.45)                    # dap an bay tre 2,5 s sau "Co dung khong?"
    if ok > 0:
        card(d, (50, 1330, 1030, 1570), fill=A((220, 252, 231), ok), outline=A(GREEN, ok), w=5)
        ctext(d, 1400, "✓ Không: kim lệch ngược", 44, GREEN, alpha=ok)
        ctext(d, 1485, "Đảo lại cực: đỏ vào +", 44, INK, alpha=ok)

# ---------------- canh 5: chot ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    def pic(d, t, k):                            # so do mach dang do (khong ve cong tac: khong goi y dap an)
        kg = appear(t, sc["M"][0] + 0.9, 0.5) * k
        if kg <= 0: return
        d.rounded_rectangle([250, 1030, 470, 1190], radius=18, fill=A((214, 219, 230), kg), outline=A(NAVY, kg), width=4)
        text(d, (360, 1110), "Bộ nguồn", 40, INK, alpha=kg)
        vx, vy = 760, 1110
        d.line([(470, 1060), (vx, 1060), (vx, vy - 50)], fill=A(RED, kg), width=7)
        d.line([(470, 1160), (vx, 1160), (vx, vy + 50)], fill=A(DARK, kg), width=7)
        d.ellipse([vx - 50, vy - 50, vx + 50, vy + 50], fill=A(WHITE, kg), outline=A(NAVY, kg), width=5)
        text(d, (vx, vy), "V", 48, NAVY, alpha=kg)
        text(d, (vx + 70, vy - 50), "6,2 V", 40, RED, alpha=kg, anchor="lm")
    chot_hoi(d, t, sc, "Số thật đọc ở vôn kế, không ở núm",
             "Muốn tháo vôn kế ra, làm gì trước?", goi_y="Nhớ lúc nối dây.", body=pic)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding"),
            (do["t0"] + do["M"][1] + 0.2, "tap"), (do["t0"] + do["M"][2], "ding"),
            (r["t0"] + r["M"][2] - 0.1, "tap"),
            (b["t0"] + 0.3, "buzz"), (b["t0"] + b["M"][1] + 2.5, "ding"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-an-toan-01", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="An toàn phòng thực hành · thachlab.id.vn", scenes=[
 dict(key="hook", title="Núm chỉ vạch, vôn kế chỉ?", draw=s_hook, tail=0.5, caps=[
   ("Vôn kế nối cực Output.", 3.0),
   ("Dừng video, tự đoán.", 5.0)]),
 dict(key="do", title="Xoay núm, đọc vôn kế", draw=s_do, tail=0.4, caps=[
   ("Dây nối lúc nguồn tắt.", 3.0),
   ("Bật nguồn, xoay núm từng vạch.", 6.6),
   ("So hai cột trong bảng.", 3.0)]),
 dict(key="rut", title="Vạch núm và số chỉ", draw=s_rut, tail=0.4, caps=[
   ("Đỏ vào +, đen vào −.", 2.6),
   ("Đo bằng vôn kế trước khi nối tải.", 3.0),
   ("Chưa nói được gì?", 4.2)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.5, caps=[
   ("Dây đỏ vào cực −.", 3.0),
   ("Có đúng không?", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Dừng video, tự trả lời.", 6.6)]),
])
