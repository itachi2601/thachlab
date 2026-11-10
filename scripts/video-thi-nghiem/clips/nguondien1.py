# Clip: tn-l11-nguon-dien-01 - Tu dien "gia lam" nguon: von ke cua tu va cua pin theo thoi gian (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-nguon-dien-01.json -> so_lieu_mau:
#   t (s): 0, 20, 40, 60, 80, 100, 300 ; U tu (V): 2,70 2,21 1,81 1,48 1,21 0,99 0,13 ; U pin (V): 2,98 moi hang.
#   tham_so: C = 1,0 F, U0 = 2,7 V, R = 100 Ohm (dieu chinh 50-500), E_b = 3,0 V, r_b = 0,6 Ohm.
#   mo_hinh: U(t) = 2,7 exp(-t/100) (duong ve tren do thi), nhanh pin U = 3,0*100/100,6 = 2,98 V.
#   hien_tuong_hay_sai[1]: nghi tu tut DEU -> canh bay so 20 s dau (2,70 -> 2,21) voi 20 s cuoi (1,21 -> 0,99).
#   Cau hoi chot: R = 200 Ohm (trong tham_so, chua tung hien) -> sau 100 s U = 2,7 e^-0,5 = 1,64 V > 0,99 V.
# Bo cuc (khac nguondien2 dung bang U-I): DO THI U theo t la truc chinh, KHONG bang.
# Canh: Du doan (K10: chi cau hoi + hai mach, von ke "?") -> Tien hanh (hai von ke doc moi 20 s, do thi ve dan,
#       tua nhanh toi 300 s) + "DAP AN · ..." -> Rut ra (tu chua san dien tich / pin co luc la) + Chua noi duoc ->
#       Bay (tut deu?) -> Chot + cau hoi tu nho lai.
# Mach: von ke mac SONG SONG voi dien tro (cung la hai ban tu / hai cuc bo pin); pin: vach dai = cuc (+).
import numpy as np
from engine import *

ROWS = [(0, 2.70, 2.98), (20, 2.21, 2.98), (40, 1.81, 2.98), (60, 1.48, 2.98), (80, 1.21, 2.98), (100, 0.99, 2.98),
        (300, 0.13, 2.98)]
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
def Umod(tau): return 2.7 * math.exp(-tau / 100.0)          # mo hinh trong kho (chi de ve duong cong)

WIRE = (60, 66, 92); SCREEN = (220, 240, 225); SCR_INK = (20, 60, 30); BODY = (70, 78, 100)
CAPC = BLUE; PINC = ORANGE; DGREEN = (10, 80, 40)

# ---------------- mach: nguon (tu hoac bo pin) + R 100 Ohm + von ke song song ----------------
def circuit(d, cx, y0, kind, reading, label=True):
    """kind 'tu' / 'pin'. Vong mach: canh trai = nguon, canh phai = R. Von ke o ben phai, noi hai nut cua R."""
    xl, xr, yt, yb = cx - 190, cx - 10, y0 + 70, y0 + 330
    ym = (yt + yb) / 2
    col = CAPC if kind == "tu" else PINC
    if label: text(d, (cx, y0 + 14), "Tụ 1,0 F" if kind == "tu" else "2 pin nối tiếp", 40, col)
    # day
    gap = 46 if kind == "tu" else 70
    d.line([(xl, ym - gap), (xl, yt), (xr, yt), (xr, ym - 72)], fill=WIRE, width=6, joint="curve")
    d.line([(xl, ym + gap), (xl, yb), (xr, yb), (xr, ym + 72)], fill=WIRE, width=6, joint="curve")
    # R
    d.rectangle([xr - 24, ym - 72, xr + 24, ym + 72], fill=WHITE, outline=NAVY, width=5)
    text(d, (xr, yb + 40), "100 Ω", 36, INK)
    # nguon
    if kind == "tu":
        for yy in (ym - 18, ym + 18): d.line([(xl - 46, yy), (xl + 46, yy)], fill=CAPC, width=9)
        d.line([(xl, ym - gap), (xl, ym - 18)], fill=WIRE, width=6); d.line([(xl, ym + 18), (xl, ym + gap)], fill=WIRE, width=6)
        text(d, (xl + 56, ym - 44), "+", 40, CAPC, anchor="lm"); text(d, (xl + 56, ym + 44), "−", 40, CAPC, anchor="lm")
    else:
        for k, yy in enumerate((ym - 50, ym + 14)):           # hai pin noi tiep: vach dai (+) o tren moi pin
            d.line([(xl - 46, yy), (xl + 46, yy)], fill=PINC, width=7)
            d.line([(xl - 26, yy + 26), (xl + 26, yy + 26)], fill=PINC, width=13)
        d.line([(xl, ym - 24), (xl, ym + 14)], fill=WIRE, width=6)
        d.line([(xl, ym - gap), (xl, ym - 50)], fill=WIRE, width=6); d.line([(xl, ym + 40), (xl, ym + gap)], fill=WIRE, width=6)
        text(d, (xl + 56, ym - 54), "+", 40, PINC, anchor="lm"); text(d, (xl + 56, ym + 44), "−", 40, PINC, anchor="lm")
    for p in ((xl, yt), (xr, yt), (xl, yb), (xr, yb)): dot(d, p[0], p[1], 8, WIRE)
    # von ke so (song song voi R): day tu hai nut ben phai
    mx0, mx1, my0, my1 = cx + 30, cx + 225, ym - 70, ym + 70
    vx = (mx0 + mx1) / 2
    d.line([(xr, yt), (vx, yt), (vx, my0)], fill=WIRE, width=4)
    d.line([(xr, yb), (vx, yb), (vx, my1)], fill=WIRE, width=4)
    dot(d, xr, yt, 8, WIRE); dot(d, xr, yb, 8, WIRE)
    card(d, (mx0, my0, mx1, my1), fill=BODY, r=18)
    card(d, (mx0 + 14, my0 + 16, mx1 - 14, my1 - 46), fill=SCREEN, r=10)
    text(d, (vx, (my0 + 16 + my1 - 46) / 2), reading, 42 if reading != "?" else 48,
         PURPLE if reading == "?" else SCR_INK)
    if reading != "?": text(d, (vx, my1 - 24), "vôn kế", 37, WHITE, bold=False)   # canh Du doan: bo chu

CXL, CXR, CY = 290, 815, 330
def two_circuits(d, rt, rp, label=True):
    d.line([(547, CY + 40), (547, CY + 370)], fill=LIGHT, width=4)
    circuit(d, CXL, CY, "tu", rt, label); circuit(d, CXR, CY, "pin", rp, label)

# ---------------- do thi U theo t ----------------
def dashed(d, p1, p2, color, w=3, dash=14, gap=10):
    L = math.dist(p1, p2); n = max(1, int(L // (dash + gap)) + 1)
    for i in range(n):
        a = i * (dash + gap) / L; b = min(1, (i * (dash + gap) + dash) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))], fill=color, width=w)

def axes(d, box, xmax, xt, yt=(0, 1, 2, 3), ymax=3.4):
    x0, ytop, x1, y0 = box
    X = lambda s: x0 + s / xmax * (x1 - x0); Y = lambda u: y0 - u / ymax * (y0 - ytop)
    for u in yt:
        if u > 0: d.line([(x0, Y(u)), (x1, Y(u))], fill=LIGHT, width=3)
        text(d, (x0 - 16, Y(u)), str(u), 36, MUTED, anchor="rm")
    d.line([(x0, y0), (x1 + 10, y0)], fill=NAVY, width=5); d.line([(x0, y0), (x0, ytop - 10)], fill=NAVY, width=5)
    d.polygon([(x1 + 26, y0), (x1 + 8, y0 - 10), (x1 + 8, y0 + 10)], fill=NAVY)
    d.polygon([(x0, ytop - 26), (x0 - 10, ytop - 8), (x0 + 10, ytop - 8)], fill=NAVY)
    text(d, (x0 + 22, ytop - 8), "U (V)", 36, INK, anchor="lm")
    for s in xt:
        d.line([(X(s), y0), (X(s), y0 + 12)], fill=NAVY, width=4)
        text(d, (X(s), y0 + 38), str(s), 36, MUTED)
    text(d, (x1 + 24, y0 + 84), "t (s)", 36, INK, anchor="rm")
    return X, Y

def curves(d, X, Y, tau, upto_pts, pen=True):
    if tau > 0:
        ss = np.linspace(0, tau, max(2, int(tau * 1.5)))
        d.line([(X(s), Y(2.98)) for s in (0, tau)], fill=PINC, width=8)
        d.line([(X(s), Y(Umod(s))) for s in ss], fill=CAPC, width=8, joint="curve")
    for (s, ut, up) in ROWS:
        if s <= upto_pts + 1e-6:
            dot(d, X(s), Y(ut), 11, CAPC, outline=WHITE); dot(d, X(s), Y(up), 11, PINC, outline=WHITE)
    if pen and 0 < tau < 299.9:
        dot(d, X(tau), Y(Umod(tau)), 14, CAPC, outline=WHITE); dot(d, X(tau), Y(2.98), 14, PINC, outline=WHITE)

def legend(d, x, y):
    d.line([(x, y), (x + 60, y)], fill=PINC, width=8); text(d, (x + 76, y), "pin", 36, PINC, anchor="lm")
    d.line([(x, y + 56), (x + 60, y + 56)], fill=CAPC, width=8); text(d, (x + 76, y + 56), "tụ", 36, CAPC, anchor="lm")

# ---------------- canh 1: Du doan (K10) ----------------
Q_AT = 1.4
def s_hook(img, d, t, sc):
    two_circuits(d, "?", "?")
    text(d, (CXL, CY + 430), "nạp sẵn 2,7 V", 40, MUTED, bold=False)
    text(d, (CXR, CY + 430), "2 pin AA mới", 40, MUTED, bold=False)
    a = appear(t, Q_AT, 0.5)
    if a <= 0: return
    y0 = 860 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 38, WHITE, alpha=a)
    ctext(d, y0 + 240, "Mỗi nguồn nuôi một điện trở 100 Ω.\nTrong 100 s, hai vôn kế\nthay đổi thế nào?", 46,
          INK, maxw=920, alpha=a)
    tc, tend = Q_AT + 0.6, sc["T"] - 0.6
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 424, 940, y0 + 436], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 424, 140 + 800 * (1 - p), y0 + 436], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
T_R0, DT_R = 0.8, 1.4           # doc so t = 0 luc 0,8 s, moi 20 s cua thi nghiem = 1,4 s cua clip
T_FF0, T_FF1 = 8.8, 10.2        # dung o t = 100 s 1 s, roi tua nhanh 100 s -> 300 s
T_ANS = 10.7
def tau_of(t):                  # thoi gian thi nghiem tuong ung (de ve duong cong)
    return float(np.interp(t, [T_R0, T_R0 + 5 * DT_R, T_FF0, T_FF1], [0, 100, 100, 300]))
def read_k(t):                  # chi so hang da doc (-1 neu chua doc)
    k = -1
    for i in range(6):
        if t >= T_R0 + i * DT_R - 1e-6: k = i
    if t >= T_FF1 - 1e-6: k = 6
    return k

GB = (170, 900, 940, 1375)      # khung do thi (x0, ytop, x1, y0)
def s_do(img, d, t, sc):
    k = read_k(t)
    if k >= 0: rt, rp = vn(ROWS[k][1]) + " V", vn(ROWS[k][2]) + " V"
    else: rt = rp = "– – –"
    two_circuits(d, rt, rp)
    # o thoi gian doc so (dong pha voi von ke)
    ff = T_FF0 <= t < T_FF1
    if ff: s = "tua nhanh tới 300 s"; col = ORANGE
    elif k >= 0: s = f"đọc lúc t = {ROWS[k][0]} s"; col = INK
    else: s = "bấm giờ"; col = MUTED
    card(d, (290, 735, 790, 805), fill=(255, 237, 213) if ff else WHITE, outline=ORANGE if ff else LIGHT, r=38, w=4)
    text(d, (W / 2, 770), s, 40, col)
    # do thi (truc co dinh 0-300 s tu dau)
    card(d, (40, 830, 1040, 1490), fill=WHITE, outline=LIGHT, w=3)
    X, Y = axes(d, GB, 300, (0, 100, 200, 300))
    legend(d, X(200), Y(2.2))
    tau = max(0.0, tau_of(t))
    curves(d, X, Y, tau, ROWS[k][0] if k >= 0 else -1)
    ka = appear(t, T_ANS, 0.15)
    if ka > 0:
        card(d, (60, 1516, 1020, 1622), fill=A((21, 110, 52), ka), r=30)
        text(d, (W / 2, 1569), "ĐÁP ÁN · tụ tụt dần, pin gần như đứng yên", 40, WHITE, alpha=ka)

# ---------------- canh 3: Rut ra + Chua noi duoc ----------------
def plates(d, cx, cy, n, k):
    for yy in (cy - 30, cy + 30): d.line([(cx - 110, yy), (cx + 110, yy)], fill=A(CAPC, k), width=10)
    for i in range(8):
        a = k * (1.0 if i < n else 0.12)
        x = cx - 92 + i * 26
        text(d, (x, cy - 66), "+", 36, RED, alpha=a); text(d, (x, cy + 66), "−", 36, BLUE, alpha=a)

def cell(d, cx, cy, t, k):
    d.line([(cx - 90, cy - 40), (cx + 90, cy - 40)], fill=A(PINC, k), width=8)       # vach dai = (+)
    d.line([(cx - 45, cy + 40), (cx + 45, cy + 40)], fill=A(PINC, k), width=16)      # vach ngan = (-)
    text(d, (cx - 104, cy - 40), "+", 40, PINC, anchor="rm", alpha=k)
    text(d, (cx - 104, cy + 40), "−", 40, PINC, anchor="rm", alpha=k)
    arrow(d, (cx + 125, cy + 60), (cx + 125, cy - 60), A(GREEN, k), w=9, head=24)    # luc la: (-) -> (+) trong nguon
    text(d, (cx + 152, cy), "lực lạ", 40, DGREEN, anchor="lm", alpha=k)

def s_rut(img, d, t, sc):
    M = sc["M"]
    k1, k2, k3 = appear(t, 0.3, 0.45), appear(t, M[1] - 0.1, 0.45), appear(t, M[2] - 0.1, 0.45)
    if k1 > 0:
        y = 470 + (1 - k1) * 30
        card(d, (60, y, 1020, y + 330), fill=A(WHITE, k1), outline=A(CAPC, k1), w=6)
        n = 8 - int(clamp((t - 0.9) / 3.0) * 7.999)            # dien tich tren ban tu hao dan khi xa
        plates(d, 250, y + 165, n, k1)
        text(d, (430, y + 120), "Tụ: chứa sẵn điện tích", 44, CAPC, anchor="lm", alpha=k1)
        text(d, (430, y + 200), "xả là hết", 44, INK, anchor="lm", alpha=k1)
    if k2 > 0:
        y = 840 + (1 - k2) * 30
        card(d, (60, y, 1020, y + 330), fill=A(WHITE, k2), outline=A(PINC, k2), w=6)
        cell(d, 240, y + 165, t, k2)
        text(d, (530, y + 120), "Pin: lực lạ bù", 44, PINC, anchor="lm", alpha=k2)
        text(d, (530, y + 200), "→ nguồn điện", 44, INK, anchor="lm", alpha=k2)
    if k3 > 0:
        y = 1210 + (1 - k3) * 30
        card(d, (60, y, 1020, y + 300), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 60), "Chưa nói được", 44, NAVY, alpha=k3)
        ctext(d, y + 180, "Vì sao pin chỉ 2,98 V,\nkhông đủ 3,0 V?", 48, INK, maxw=900, alpha=k3 * appear(t, M[2] + 0.3, 0.4))

# ---------------- canh 4: Bay - "tu tut deu" ----------------
GZ = (190, 400, 940, 980)       # do thi phong to 0-100 s
def s_bay(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 300, 1040, 1080), fill=WHITE, outline=LIGHT, w=3)
    text(d, (1000, 340), "phóng to 0–100 s", 36, MUTED, bold=False, anchor="rm")
    X, Y = axes(d, GZ, 100, (0, 20, 40, 60, 80, 100))
    curves(d, X, Y, 100, 100, pen=False)
    kb = appear(t, M[1] + 0.2, 0.4)
    for (sa, ua, sb, ub, lab, dv) in ((0, 2.70, 20, 2.21, "20 s đầu", "2,70 → 2,21 V"),
                                      (80, 1.21, 100, 0.99, "20 s cuối", "1,21 → 0,99 V")):
        if kb <= 0: break
        d.line([(X(sa), Y(ua)), (X(sb), Y(ua))], fill=A(RED, kb), width=7)
        d.line([(X(sb), Y(ua)), (X(sb), Y(ub))], fill=A(RED, kb), width=12)         # do tut: vach do day
        d.polygon([(X(sb), Y(ub) + 4), (X(sb) - 14, Y(ub) - 18), (X(sb) + 14, Y(ub) - 18)], fill=A(RED, kb))
        if sa == 0:
            text(d, (X(sb) + 26, Y((ua + ub) / 2) - 24), lab, 38, RED, anchor="lm", alpha=kb)
            text(d, (X(sb) + 26, Y((ua + ub) / 2) + 24), dv, 38, RED, anchor="lm", alpha=kb)
        else:
            text(d, (X(sb) - 10, Y(ub) + 48), lab, 38, RED, anchor="rm", alpha=kb)
            text(d, (X(sb) - 10, Y(ub) + 94), dv, 38, RED, anchor="rm", alpha=kb)
    a1 = appear(t, 0.1, 0.4)
    y0 = 1120
    card(d, (40, y0, 1040, y0 + 450), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 30, W / 2 + pw / 2, y0 + 94), fill=A(RED, a1), r=32)
    text(d, (W / 2, y0 + 62), "BẪY", 38, WHITE, alpha=a1)
    q = "Tụ tụt đều theo thời gian"
    ks = clamp((t - (M[1] + 0.6)) / 0.4); f = F(46); lw = tw(d, q, f); yy = y0 + 190
    text(d, (W / 2, yy), q, 46, RED, alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=RED, width=4)
    ka = appear(t, M[1] + 1.1, 0.5)
    text(d, (W / 2, y0 + 310), "✓ Tụt nhanh lúc đầu,", 46, DGREEN, alpha=ka)
    text(d, (W / 2, y0 + 380), "chậm dần về sau", 46, DGREEN, alpha=ka)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: R = 200 Ohm, sau 100 s von ke cua tu hon hay kem 0,99 V? (1,64 V)."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 400, 1020, 680), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 540, "Nguồn điện duy trì\nhiệu điện thế", 52, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 740, 1040, 1420), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 770, W / 2 + pw / 2, 834), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 802), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 980, "Vẫn nạp 2,7 V, xả qua 200 Ω.\nSau 100 s, vôn kế của tụ\nhơn hay kém 0,99 V?", 46, INK,
          maxw=930, alpha=appear(t, M[0] + 0.4, 0.5))
    kh = appear(t, M[0] + 2.9, 0.5)
    if kh <= 0: return
    card(d, (110, 1170, 970, 1380), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1220, "Gợi ý", 40, (154, 52, 18), alpha=kh)
    ctext(d, 1305, "R lớn hơn: dòng xả lớn hay nhỏ?", 44, ORANGE, maxw=820, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    out = [(h["t0"] + Q_AT, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + T_R0 + i * DT_R, "tick") for i in range(6)] + [(do["t0"] + T_FF1, "tick")]
    out += [(do["t0"] + T_ANS, "ding"), (r["t0"] + 0.3, "tap"), (b["t0"] + 0.1, "buzz"),
            (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

CLIP = dict(id="tn-l11-nguon-dien-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Nguồn điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Tụ điện và pin", draw=s_hook, tail=0.8, caps=[
   ("Bấm giờ cùng lúc.", 2.5),
   ("Tự đoán trước khi xem tiếp.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.9, caps=[
   ("Đọc hai vôn kế mỗi 20 s.", 8.4),
   ("Rồi đọc lại sau 5 phút.", 3.6)]),
 dict(key="rut", title="Rút ra", draw=s_rut, tail=0.6, caps=[
   ("Tụ cạn dần điện tích.", 2.9),
   ("Pin thì giữ được.", 2.5),
   ("Còn bỏ ngỏ.", 4.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.6, caps=[
   ("Bẫy thường gặp.", 2.6),
   ("Cùng 20 s, tụt bao nhiêu V?", 3.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 7.0)]),
])
