# Clip: tn-l10-an-toan-01 - Num bo nguon o vach 3, 6, 9, 12 V: von ke chi bao nhieu (1/11/2026; dung lai 27/11/2026 theo
#   cong moi viec 4: --do-chu 0 LOI, chu ve >= 56 px, Du doan khong nut A-D (K10), thanh dem lien, cau chot A-D o khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-an-toan-01.json (_kiem_so() doi chieu):
#   so_lieu_mau: vach 3; 6; 9; 12 V -> V doc 3,1; 6,2; 9,3; 12,4 V ; cot Lech 0,1; 0,2; 0,3; 0,4 V.
#   mo_hinh.gia_thiet: nguon khong mac tai (-> the "Chua noi duoc"); an_toan: giao vien cho phep, tat cong tac khi noi, dung cuc.
# Bai 47: hop exp dung TRUOC video va Quan sat da noi "so chi luon cao hon vach mot chut" -> Du doan KHONG hoi "cao hay thap",
#   ma hoi XU HUONG phan lech khi num tu 3 len 12 V (dap an: tang dan 0,1 -> 0,4 V). "Doc bang" sau video hoi "co phai do sai?"
#   -> clip khong noi "sai so cua bo nguon", khong noi %; Thu thach 2 sao (9 V -> 9,3 V) -> chot khong hoi so chi.
#   Cau mo bai (tat cong tac roi moi noi) -> chot ghep 2 buoc: kim lech nguoc khi nguon dang bat -> tat roi moi dao day.
# Canh: Du doan -> Tien hanh (noi khi tat, bat, xoay 4 vach, cot lech) + DAP AN -> Rut ra (song song, vach gan dung)
#       -> Chua noi duoc (co tai) -> Bay (hai khung: cam dao day / dung cuc) -> THU NGHI (kim lech nguoc, nguon dang bat).
from engine import *

VACH = (3, 6, 9, 12); DOC = (3.1, 6.2, 9.3, 12.4); LECH = (0.1, 0.2, 0.3, 0.4)
def fm(x): return f"{x:.1f}".replace(".", ",")

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-an-toan-01.json")))
    hang = k["so_lieu_mau"]["hang"]
    assert [h[0] for h in hang] == list(VACH) and [h[2] for h in hang] == list(DOC) and [h[3] for h in hang] == list(LECH)
    for v, dc, l in zip(VACH, DOC, LECH): assert abs(dc - v - l) < 1e-9
_kiem_so()

DARK = (40, 44, 56); DGREEN = (10, 110, 50); DRED = (185, 28, 28); DPURP = (91, 33, 182); DORANGE = (176, 64, 8)
PANEL = (60, 250, 1020, 690)
KN = (240, 470)
ANG = {3: -120, 6: -40, 9: 40, 12: 120}
SW = (520, 440)
TP, TM = (730, 480), (900, 480)
MB = (530, 740, 1030, 1190); PV, R = (780, 1120), 210
VP, VM = (610, 790), (950, 790)
VMAX = 15
def vang(v): return math.radians(140 - 100 * v / VMAX)        # 0 V -> 140 do, 15 V -> 40 do

def supply(d, kang, on, glow=0.0, a=1.0):
    c = lambda col: A(col, a)
    card(d, PANEL, fill=c((214, 219, 230)), outline=c((120, 126, 145)), r=30, w=5)
    d.line([(PANEL[0], 640), (30, 648), (0, 680)], fill=c(DARK), width=12, joint="curve")
    text(d, (90, 640), "220 V ~", 56, INK, anchor="lm", alpha=a)
    for v, ag in ANG.items():
        r_ = math.radians(ag)
        d.line([(KN[0] + 86 * math.sin(r_), KN[1] - 86 * math.cos(r_)), (KN[0] + 102 * math.sin(r_), KN[1] - 102 * math.cos(r_))], fill=c(INK), width=5)
        text(d, (KN[0] + 140 * math.sin(r_), KN[1] - 140 * math.cos(r_)), str(v), 56, INK, alpha=a)
    dot(d, KN[0], KN[1], 74, c((60, 66, 84))); dot(d, KN[0], KN[1], 58, c((88, 95, 116)))
    r_ = math.radians(kang)
    d.line([(KN[0] + 14 * math.sin(r_), KN[1] - 14 * math.cos(r_)), (KN[0] + 66 * math.sin(r_), KN[1] - 66 * math.cos(r_))], fill=c(WHITE), width=10)
    d.rounded_rectangle([SW[0] - 76, SW[1] - 92, SW[0] + 76, SW[1] + 92], radius=16, fill=c(DARK))
    yk = SW[1] - 42 if on else SW[1] + 42
    d.rounded_rectangle([SW[0] - 66, yk - 40, SW[0] + 66, yk + 40], radius=12, fill=c((235, 238, 245)))
    text(d, (SW[0], yk), "BẬT" if on else "TẮT", 56, DGREEN if on else DRED, alpha=a)
    dot(d, SW[0], SW[1] + 140, 22, c((60, 220, 110) if on else (150, 155, 170)), outline=c(DARK))
    if glow > 0: d.rounded_rectangle([SW[0] - 92, SW[1] - 108, SW[0] + 92, SW[1] + 108], radius=22, outline=A(ORANGE, glow * a), width=8)
    text(d, (815, 318), "Output DC", 56, INK, alpha=a)
    for (x, y), col, s in ((TP, RED, "+"), (TM, DARK, "−")):
        dot(d, x, y, 40, c(col), outline=c((30, 30, 30))); dot(d, x, y, 14, c((200, 200, 200)))
        text(d, (x, y - 82), s, 64, col, alpha=a)

def wire(d, p1, p2, col, prog=1.0, sag=40, a=1.0):
    pts = [(lerp(p1[0], p2[0], i / 40) + sag * math.sin(math.pi * i / 40), lerp(p1[1], p2[1], i / 40)) for i in range(41)]
    n = max(2, int(41 * prog))
    d.line(pts[:n], fill=A(col, a), width=10, joint="curve")

def gauge(d, cx, cy, r, v=None, pinned=False, a=1.0, nums=True, tick=True):
    """Mat von ke: cung 40..140 do, kim do. pinned = kim dap vao chot trai (lech nguoc)."""
    c = lambda col: A(col, a)
    d.arc([cx - r, cy - r, cx + r, cy + r], 220, 320, fill=c(NAVY), width=4)
    if tick:
        for k in range(0, 2 * VMAX + 1):
            ag = vang(k / 2); L = 30 if k % 10 == 0 else (20 if k % 2 == 0 else 11)
            d.line([(cx + r * math.cos(ag), cy - r * math.sin(ag)), (cx + (r - L) * math.cos(ag), cy - (r - L) * math.sin(ag))], fill=c(NAVY), width=4 if L == 30 else 3)
    if nums:
        for v_ in (0, 5, 10, 15):
            ag = vang(v_); text(d, (cx + (r + 42) * math.cos(ag), cy - (r + 42) * math.sin(ag)), str(v_), 56, INK, alpha=a)
    if v is not None or pinned:
        ag = math.radians(152) if pinned else vang(v)
        d.line([(cx, cy), (cx + (r - 14) * math.cos(ag), cy - (r - 14) * math.sin(ag))], fill=c(RED), width=7)
    dot(d, cx, cy, 14, c(NAVY))

def meter(d, v, hide=False, read=None, a=1.0):
    card(d, MB, fill=A(WHITE, a), outline=A(NAVY, a), r=26, w=5)
    for (x, y), col, s in ((VP, RED, "+"), (VM, DARK, "−")):
        dot(d, x, y, 22, A(col, a), outline=A((30, 30, 30), a))
        text(d, (x + (52 if s == "+" else -52), y + 4), s, 60, col, alpha=a)
    gauge(d, PV[0], PV[1], R, None if hide else v, a=a)
    text(d, (PV[0], 1030), "V", 60, NAVY, alpha=a)
    if hide:
        d.rounded_rectangle([600, 930, 960, 1100], radius=24, fill=A((245, 243, 255), a), outline=A(PURPLE, a), width=4)
        text(d, (780, 1015), "?", 90, PURPLE, alpha=a)
    if read is not None: text(d, (640, 1145), read, 58, RED, alpha=a)

def table(d, n_rows, hide=False, hl=-1, a=1.0):
    card(d, (50, 740, 500, 1190), fill=A(WHITE, a), outline=A(NAVY, a), r=26, w=4)
    xs = (160, 375)
    text(d, (xs[0], 790), "Vạch", 56, INK, alpha=a); text(d, (xs[1], 790), "Số chỉ", 56, INK, alpha=a)
    text(d, (xs[0], 850), "(V)", 56, INK, alpha=a); text(d, (xs[1], 850), "(V)", 56, INK, alpha=a)
    d.line([(70, 888), (480, 888)], fill=A(LIGHT, a), width=4); d.line([(265, 765), (265, 1170)], fill=A(LIGHT, a), width=3)
    for i, v in enumerate(VACH):
        y = 930 + i * 66
        if i == hl: d.rounded_rectangle([66, y - 32, 484, y + 32], radius=14, fill=A((255, 241, 222), a))
        text(d, (xs[0], y), str(v), 56, BLUE, alpha=a)
        if hide: text(d, (xs[1], y), "?", 56, PURPLE, alpha=a)
        elif i < n_rows: text(d, (xs[1], y), fm(DOC[i]), 56, DRED, alpha=a)

def cbar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0))
    d.rounded_rectangle([110, y, 970, y + 80], radius=40, fill=A((246, 244, 250), a))
    if p < 1: d.rounded_rectangle([110, y, 110 + max(80, 860 * (1 - p)), y + 80], radius=40, fill=A(col, a))

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    supply(d, ANG[3], False, a=a)
    pw = ease((t - 0.6) / 1.6)
    meter(d, 0, hide=True, a=a); table(d, 0, hide=True, a=a)
    if pw > 0:
        wire(d, (TP[0], TP[1] + 40), VP, RED, pw, sag=-40, a=a); wire(d, (TM[0], TM[1] + 40), VM, DARK, pw, sag=30, a=a)
    k = appear(t, M[1] - 0.3, 0.45)
    if k <= 0: return
    y0 = 1215 + (1 - k) * 30
    card(d, (50, y0, 1030, y0 + 465), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw_ = tw(d, "DỰ ĐOÁN", F(56)) + 60
    card(d, (W / 2 - pw_ / 2, y0 + 22, W / 2 + pw_ / 2, y0 + 98), fill=A(PURPLE, k), r=36)
    text(d, (W / 2, y0 + 60), "DỰ ĐOÁN", 56, WHITE, alpha=k)
    cbar(d, y0 + 118, t, M[1] + 0.3, sc["T"] - 0.15, DPURP, k)
    text(d, (W / 2, y0 + 270), "Núm từ 3 V lên 12 V:", 60, INK, alpha=k)
    text(d, (W / 2, y0 + 345), "số chỉ lệch khỏi vạch", 60, INK, alpha=k)
    text(d, (W / 2, y0 + 420), "thay đổi thế nào?", 60, PURPLE, alpha=k)

# ---------------- canh 2: Tien hanh ----------------
STEP, TURN = 1.4, 0.5
def state(t, sc):
    """-> (goc num, bat?, v kim, so chi dang hien, so hang bang, hang dang lam)."""
    M = sc["M"]; ton = M[1] + 0.2
    if t < ton: return ANG[3], False, 0.0, None, 0, -1
    for i in range(3, -1, -1):
        s = ton + i * STEP
        if t >= s: break
    k = ease((t - s) / TURN)
    if i == 0: kang = ANG[3]; v = lerp(0.0, DOC[0], k)
    else: kang = lerp(ANG[VACH[i - 1]], ANG[VACH[i]], k); v = lerp(DOC[i - 1], DOC[i], k)
    done = t >= s + TURN
    return kang, True, v, (fm(DOC[i]) + " V") if done else "…", i + 1 if done else i, i

def lech_bars(d, n, a=1.0):
    card(d, (50, 1215, 1030, 1680), fill=A(WHITE, a), outline=A(NAVY, a), w=4)
    text(d, (150, 1330), "Lệch", 56, DORANGE, alpha=a)
    yb = 1590
    d.line([(250, yb), (1000, yb)], fill=A(NAVY, a), width=4)
    for i in range(4):
        x = 330 + i * 190
        text(d, (x, 1635), f"{VACH[i]} V", 56, BLUE, alpha=a)
        if i < n:
            hgt = LECH[i] * 500
            d.rectangle([x - 55, yb - hgt, x + 55, yb], fill=A((253, 186, 116), a), outline=A(DORANGE, a), width=4)
            text(d, (x, yb - hgt - 38), fm(LECH[i]), 56, DORANGE, alpha=a)

def s_do(img, d, t, sc):
    M = sc["M"]
    kang, on, v, read, rows, cur = state(t, sc)
    glow = (0.5 + 0.5 * math.sin(2 * math.pi * 1.2 * t)) if t < M[1] else 0.0
    supply(d, kang, on, glow)
    wire(d, (TP[0], TP[1] + 40), VP, RED, sag=-40); wire(d, (TM[0], TM[1] + 40), VM, DARK, sag=30)
    meter(d, v, read=read if on else "0 V")
    table(d, rows, hl=cur)
    if t < M[1] + 0.2:
        a = 1.0                                                        # hien cung bo nguon (engine tu lam mo dau canh)
        card(d, (50, 1215, 1030, 1680), fill=A(WHITE, a), outline=A(GREEN, a), w=5)
        text(d, (W / 2, 1380), "✓ Giáo viên cho phép", 60, DGREEN, alpha=a)
        text(d, (W / 2, 1500), "Chưa nối tải", 60, INK, alpha=a)
        return
    lech_bars(d, rows)
    kc = appear(t, M[2] + 0.3, 0.4)
    if kc > 0:
        s_ = "ĐÁP ÁN: lệch tăng dần"; pw = tw(d, s_, F(58)) + 70
        card(d, (W / 2 - pw / 2, 1228, W / 2 + pw / 2, 1318), fill=A((220, 252, 231), kc), outline=A(GREEN, kc), r=28, w=5)
        text(d, (W / 2, 1273), s_, 58, DGREEN, alpha=kc)

# ---------------- canh 3: Rut ra ----------------
def s_rut(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.05, 0.35)
    card(d, (40, 240, 1040, 900), fill=A(WHITE, a), outline=A(LIGHT, a), w=3)
    bx0, by0, bx1, by1 = 100, 400, 440, 640
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=20, fill=A((214, 219, 230), a), outline=A(NAVY, a), width=4)
    text(d, ((bx0 + bx1) / 2, 470), "Bộ nguồn", 58, INK, alpha=a)
    text(d, ((bx0 + bx1) / 2, 565), "vạch 6 V", 58, BLUE, alpha=a)
    ptop, pbot = (440, 440), (440, 600)
    g = ease((t - 0.3) / 1.0); vx, vy = 800, 520
    d.line([ptop, (620, 440), (620, 330), (vx, 330), (vx, vy - 80)][:2 + int(3 * g)], fill=A(RED, a), width=7)
    d.line([pbot, (620, 600), (620, 710), (vx, 710), (vx, vy + 80)][:2 + int(3 * g)], fill=A(DARK, a), width=7)
    text(d, (480, 380), "+", 60, RED, alpha=a); text(d, (480, 660), "−", 60, DARK, alpha=a)
    d.ellipse([vx - 80, vy - 80, vx + 80, vy + 80], fill=A(WHITE, a), outline=A(NAVY, a), width=6)
    text(d, (vx, vy), "V", 70, NAVY, alpha=a)
    kb = appear(t, 1.4, 0.4)
    if kb > 0: text(d, (vx, 820), "6,2 V", 60, DRED, alpha=kb)
    kr = appear(t, M[1] + 0.2, 0.4)
    if kr > 0:
        card(d, (60, 960, 1020, 1100), fill=A((236, 253, 243), kr), outline=A(GREEN, kr), r=28, w=5)
        text(d, (W / 2, 1030), "Vạch núm chỉ gần đúng", 60, DGREEN, alpha=kr)
        x0 = 230 + 200 * ease((t - M[1] - 0.4) / 1.2)                 # vôn kế dời từ nguồn sang dụng cụ: do lai truoc khi noi
        d.ellipse([x0 - 60, 1250 - 60, x0 + 60, 1250 + 60], fill=A(WHITE, kr), outline=A(NAVY, kr), width=5)
        text(d, (x0, 1250), "V", 60, NAVY, alpha=kr)
        arrow(d, (x0 + 80, 1250), (680, 1250), A(INK, kr), w=6, head=22)
        d.ellipse([720, 1180, 860, 1320], fill=A((254, 249, 195), kr), outline=A(DORANGE, kr), width=5)
        d.line([(760, 1270), (790, 1220), (820, 1270)], fill=A(DORANGE, kr), width=4)

# ---------------- canh 4: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    k = appear(t, 0.05, 0.35)
    card(d, (60, 240, 1020, 560), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, 325), "Chưa nói được", 62, NAVY, alpha=k)
    text(d, (W / 2, 455), "Có tải: số chỉ còn vậy?", 60, INK, alpha=k)
    d.rounded_rectangle([110, 700, 420, 940], radius=20, fill=A((214, 219, 230), k), outline=A(NAVY, k), width=4)
    text(d, (265, 820), "nguồn", 58, INK, alpha=k)
    d.line([(420, 760), (760, 760), (760, 800)], fill=A(RED, k), width=7); d.line([(420, 880), (760, 880), (760, 940)], fill=A(DARK, k), width=7)
    gl = 0.5 + 0.5 * math.sin(t * 4.0)                                 # bong den chop chop: chua biet sang the nao
    d.ellipse([680, 800 - 0, 840, 960], fill=A(mix((254, 249, 195), (250, 204, 21), gl), k), outline=A(DORANGE, k), width=5)
    text(d, (930, 860 + 40 * math.sin(t * 3.2)), "?", 120, NAVY, alpha=k)

# ---------------- canh 5: Bay (hai khung) ----------------
def mini(d, y0, wrong, k, t0, t):
    col = DRED if wrong else DGREEN
    card(d, (60, y0, 1020, y0 + 640), fill=A(WHITE, k), outline=A(col, k), w=6)
    text(d, (W / 2, y0 + 70), "✗ Đỏ vào −" if wrong else "✓ Đỏ vào +", 62, col, alpha=k)
    sx0, sy0 = 110, y0 + 190                                           # nguon: + tren, - duoi
    d.rounded_rectangle([sx0, sy0, sx0 + 230, sy0 + 300], radius=20, fill=A((214, 219, 230), k), outline=A(NAVY, k), width=4)
    pp, pm = (sx0 + 230, sy0 + 70), (sx0 + 230, sy0 + 230)
    text(d, (sx0 + 115, sy0 + 70), "+", 64, RED, alpha=k); text(d, (sx0 + 115, sy0 + 230), "−", 64, DARK, alpha=k)
    cx, cy, r = 760, y0 + 470, 170                                     # von ke: cuc do (+) tren trai, den (-) duoi trai
    top, bot = (560, y0 + 260), (560, y0 + 420)                        # ✗: cuc + von ke o duoi -> day khong cheo
    mp, mm = (bot, top) if wrong else (top, bot)
    for (x, y), c_, s in ((mp, RED, "+"), (mm, DARK, "−")):
        dot(d, x, y, 22, A(c_, k)); text(d, (x + 56, y), s, 76, c_, alpha=k)
    if wrong:
        d.line([pm, (470, pm[1]), (470, mp[1]), mp], fill=A(RED, k), width=11)       # day do: cuc - nguon -> + von ke
        d.line([pp, (470, pp[1]), (470, mm[1]), mm], fill=A(DARK, k), width=11)
    else:
        d.line([pp, (470, pp[1]), (470, mp[1]), mp], fill=A(RED, k), width=11)
        d.line([pm, (470, pm[1]), (470, mm[1]), mm], fill=A(DARK, k), width=11)
    kv = 1.0 if t >= t0 else 0.0                                       # kim dung ngay o vi tri cuoi (so khong noi suy)
    gauge(d, cx, cy, r, None if wrong else lerp(0, DOC[1], kv), pinned=wrong and kv > 0, a=k, nums=False, tick=True)
    if wrong and kv > 0:
        ag = math.radians(152); tip = (cx + (r - 14) * math.cos(ag), cy - (r - 14) * math.sin(ag))
        fl = 0.5 + 0.5 * math.sin((t - t0) * 9)
        d.ellipse([tip[0] - 34, tip[1] - 34, tip[0] + 34, tip[1] + 34], outline=A(RED, k * fl), width=7)
        text(d, (cx + 40, y0 + 560), "kim lệch ngược", 58, DRED, alpha=k)
    if not wrong and kv >= 1: text(d, (cx + 40, y0 + 560), "6,2 V", 60, DRED, alpha=k)

def s_bay(img, d, t, sc):
    M = sc["M"]
    mini(d, 240, True, appear(t, 0.05, 0.3), 0.0, t)
    kb = appear(t, M[1] - 0.05, 0.35)
    if kb > 0: mini(d, 930, False, kb, M[1] - 0.05, t)

# ---------------- canh 6: Chot (phu de) + THU NGHI ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 220, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(56)) + 60
    card(d, (W / 2 - pw / 2, 250, W / 2 + pw / 2, 326), fill=A(ORANGE, k1), r=36)
    text(d, (W / 2, 288), "THỬ NGHĨ", 56, WHITE, alpha=k1)
    d.ellipse([110, 470, 350, 710], fill=A((254, 249, 195), k1), outline=A(DORANGE, k1), width=6)   # dung cu dinh muc 12 V
    d.line([(180, 620), (230, 540), (280, 620)], fill=A(DORANGE, k1), width=6)
    text(d, (230, 790), "ghi 12 V", 58, INK, alpha=k1)
    cx, cy, r = 720, 700, 230
    gauge(d, cx, cy, r, DOC[3], a=k1, nums=False)
    text(d, (cx, cy + 110), "12,4 V", 60, DRED, alpha=k1)
    text(d, (W / 2, 1010), "Vạch 12 V, vôn kế 12,4 V.", 58, INK, alpha=k1)
    text(d, (W / 2, 1110), "Có cần hạ vạch?", 60, ORANGE, alpha=k1)
    cbar(d, 1230, t, 1.0, sc["T"] - 0.2, DORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.6, "ding"), (do["t0"] + do["M"][1] + 0.2, "tap")]
    out += [(do["t0"] + do["M"][1] + 0.2 + i * STEP + TURN, "tick") for i in range(4)]
    out += [(do["t0"] + do["M"][2] + 0.3, "ding"), (b["t0"] + 0.3, "buzz"), (b["t0"] + b["M"][1] + 0.1, "ding"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l10-an-toan-01", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="An toàn phòng thực hành · thachlab.id.vn", scenes=[
 dict(key="hook", title="Núm chỉ vạch, vôn kế chỉ?", draw=s_hook, tail=0.3, caps=[
   ("Vôn kế nối hai cực Output.", 3.8),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Xoay núm, đọc vôn kế", draw=s_do, tail=0.3, caps=[
   ("Nối dây khi nguồn tắt.", 3.2),
   ("Bật nguồn, xoay từng vạch.", 6.0),
   ("So từng hàng.", 3.0)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.3, caps=[
   ("Vôn kế mắc song song.", 3.4),
   ("Trước khi nối bóng, đo lại.", 3.8)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.4, caps=[
   ("Ở đây chưa nối tải.", 4.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Cắm đảo hai dây.", 3.4),
   ("Tắt nguồn, cắm lại đúng cực.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.4, caps=[
   ("So số chỉ với số ghi.", 5.6)]),
])
