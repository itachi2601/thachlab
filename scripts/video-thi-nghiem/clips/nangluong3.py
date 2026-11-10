# Clip: tn-l11-nang-luong-dien-03 - Hieu suat cua hai pin AA theo dien tro mach ngoai (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-nang-luong-dien-03.json (E = 3,0 V, r = 1,0 Ohm):
#   so_lieu_mau (R Ohm, I A, U V, H %, P_R W): 1,0 1,50 1,50 50 2,25 ; 2,0 1,00 2,00 66,7 2,00 ;
#                                              4,0 0,60 2,40 80 1,44 ; 9,0 0,30 2,70 90 0,81
#   Kiem bang python: I = E/(R + r), U = IR, H = U/E = R/(R + r), P_R = UI -> khop ca 4 hang.
#   Bay = hien_tuong_hay_sai[0]: nghi H lon nhat khi R = r (do la P_R lon nhat 2,25 W, H chi 50 %).
#   Du doan: o R nao (1,0 / 2,0 / 4,0 / 9,0 Ohm) H lon nhat? Dap an: R = 9,0 Ohm (R lon nhat).
#   Cau hoi chot: hai pin moi r = 0,2 Ohm (tham_so r min), van R = 1,0 Ohm -> H = 1/1,2 = 83 % (chua tung hien;
#   phan xa sai: 50 % cua hang R = 1,0 Ohm).
# Khac clip nangluong2 (den xe may, BANG U-I-P): o day DO THI H theo R la truc chinh, khong bang; bay dung cot P_R.
# Mach (vat li): pin (+ o tren, vach dai = +) -> day tren -> AMPE KE NOI TIEP -> hop dien tro R -> day duoi -> khoa K
#   -> (-). VON KE SONG SONG voi R. K mo: hai dong ho chi 0. K dong: so chi + diem do thi + dong H doi CUNG luc
#   (kiem bang ma moi 0,05 s: _kiem_dong_bo()).
# Canh: Du doan (K10: chi cau hoi + hinh) -> Tien hanh (R = 1,0 lam cham; 2,0 / 4,0 / 9,0 tua nhanh, cham diem H)
#       -> Dap an + Rut ra (duong R/(R + r), vach 100 % khong cham; Chua noi duoc) -> Bay (cot P_R) -> Chot.
from engine import *

ROWS = [(1.0, 1.50, 1.50, 50.0, 2.25), (2.0, 1.00, 2.00, 66.7, 2.00),
        (4.0, 0.60, 2.40, 80.0, 1.44), (9.0, 0.30, 2.70, 90.0, 0.81)]      # so_lieu_mau
E_, R_IN = 3.0, 1.0
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
def hs(h): return (vn(h, 1) if abs(h - round(h)) > 1e-6 else str(int(round(h)))) + " %"
BODY = (70, 78, 100); SCR = (220, 240, 225); WIRE = (60, 66, 90); DRED = (185, 28, 28); DGREEN = (21, 110, 55)

# ---------------- dung cu (khung nguon 1080x1920) ----------------
XL, XR, YT, YB = 120, 760, 360, 760            # vong mach chinh
AMC = (440, YT)                                  # ampe ke tren day tren
RBX = (690, 470, 830, 650)                       # hop dien tro tren canh phai
XV, YJ1, YJ2 = 960, 420, 700                     # nhanh von ke song song voi R
VMC = (XV, 560)
KP, KC = (400, YB), (500, YB)                    # khoa K: chot xoay / tiep diem

def meter(d, c, reading, name):
    cx, cy = c
    card(d, (cx - 92, cy - 66, cx + 92, cy + 66), fill=BODY, r=18)
    card(d, (cx - 80, cy - 54, cx + 80, cy + 12), fill=SCR, r=10)
    text(d, (cx, cy - 21), reading, 42, (20, 60, 30))
    text(d, (cx, cy + 38), name, 40, WHITE, bold=False)

def cells(d):
    """Hai pin noi tiep tren canh trai, cuc + o tren: vach dai mong = +, vach ngan day = -."""
    for yc in (505, 615):
        d.line([(XL - 44, yc - 12), (XL + 44, yc - 12)], fill=NAVY, width=6)       # vach dai (+)
        d.line([(XL - 22, yc + 12), (XL + 22, yc + 12)], fill=NAVY, width=14)      # vach ngan (-)
    d.line([(XL, 517), (XL, 603)], fill=WIRE, width=7)
    text(d, (XL - 62, 482), "+", 44, RED); text(d, (XL - 62, 650), "−", 48, INK)

def circuit(d, rlab, closed, ra, rv, tag=True, cur=True):
    w = 7
    d.line([(XL, 493), (XL, YT), (AMC[0] - 92, YT)], fill=WIRE, width=w, joint="curve")
    d.line([(AMC[0] + 92, YT), (XR, YT), (XR, RBX[1])], fill=WIRE, width=w, joint="curve")
    d.line([(XR, RBX[3]), (XR, YB), (KC[0], YB)], fill=WIRE, width=w, joint="curve")
    d.line([(KP[0], YB), (XL, YB), (XL, 627)], fill=WIRE, width=w, joint="curve")
    d.line([(XR, YJ1), (XV, YJ1), (XV, VMC[1] - 66)], fill=WIRE, width=w, joint="curve")
    d.line([(XV, VMC[1] + 66), (XV, YJ2), (XR, YJ2)], fill=WIRE, width=w, joint="curve")
    for y in (YJ1, YJ2): dot(d, XR, y, 12, WIRE)
    cells(d)
    if tag:
        card(d, (175, 455, 410, 665), fill=WHITE, outline=ORANGE, r=18, w=4)
        text(d, (292, 500), "2 pin AA", 38, ORANGE)
        text(d, (292, 560), "E = 3,0 V", 38, INK)
        text(d, (292, 620), "r = 1,0 Ω", 38, INK)
    # hop dien tro
    card(d, RBX, fill=BODY, r=16)
    card(d, (RBX[0] + 10, 520, RBX[2] - 10, 600), fill=SCR, r=10)
    text(d, ((RBX[0] + RBX[2]) / 2, 560), rlab, 40, (20, 60, 30))
    text(d, ((RBX[0] + RBX[2]) / 2, 495), "R", 40, WHITE)
    # khoa K
    dot(d, KP[0], KP[1], 11, WIRE); dot(d, KC[0], KC[1], 11, WHITE, outline=WIRE)
    ang = 0.0 if closed else math.radians(-32)
    L = KC[0] - KP[0]
    d.line([KP, (KP[0] + L * math.cos(ang), KP[1] + L * math.sin(ang))], fill=WIRE, width=8)
    text(d, (330, YB - 40), "K", 40, INK)
    meter(d, AMC, ra, "ampe kế")
    meter(d, VMC, rv, "vôn kế")
    if cur and closed:      # chieu dong quy uoc: (+) -> day tren -> ampe ke -> R -> (-)
        arrow(d, (580, YT), (670, YT), RED, w=7, head=24)
        text(d, (625, YT - 40), "I", 40, RED)

# ---------------- do thi H theo R (truc co dinh tu canh Tien hanh) ----------------
GX0, GX1, GY0, GY1 = 200, 960, 1480, 1030       # R 0..10 Ohm ; H 0..100 %
def gx(R): return GX0 + R / 10 * (GX1 - GX0)
def gy(h): return GY0 - h / 100 * (GY0 - GY1)

def dash(d, p1, p2, col, w=4, on=14, off=10):
    L = math.hypot(p2[0] - p1[0], p2[1] - p1[1]); n = int(L // (on + off)) + 1
    for i in range(n):
        a, b = i * (on + off) / L, min(1, (i * (on + off) + on) / L)
        if a >= 1: break
        d.line([(lerp(p1[0], p2[0], a), lerp(p1[1], p2[1], a)), (lerp(p1[0], p2[0], b), lerp(p1[1], p2[1], b))],
               fill=col, width=w)

LAB_OFF = [(24, 44), (24, 46), (26, 52), (0, 50)]   # nhan % duoi-phai diem (diem 9 Ohm: ngay duoi)
def graph(d, npts, curve=0.0, k100=0.0, hl=None):
    card(d, (40, 920, 1040, 1600), fill=WHITE, outline=LIGHT, w=3)
    d.line([(GX0, GY1 - 40), (GX0, GY0)], fill=NAVY, width=4); d.line([(GX0, GY0), (GX1 + 30, GY0)], fill=NAVY, width=4)
    arrow(d, (GX0, GY1 - 20), (GX0, GY1 - 44), NAVY, w=4, head=16)
    arrow(d, (GX1 + 10, GY0), (GX1 + 34, GY0), NAVY, w=4, head=16)
    text(d, (GX0 + 22, GY1 - 50), "H (%)", 38, INK, anchor="lm")
    text(d, (1010, GY0 - 40), "R (Ω)", 38, INK, anchor="rm")
    for h in (50, 100):
        d.line([(GX0 - 12, gy(h)), (GX0, gy(h))], fill=NAVY, width=3)
        text(d, (GX0 - 20, gy(h)), str(h), 38, MUTED, bold=False, anchor="rm")
    text(d, (GX0 - 20, GY0 + 4), "0", 38, MUTED, bold=False, anchor="rm")
    for R in (1, 2, 4, 9):
        d.line([(gx(R), GY0), (gx(R), GY0 + 12)], fill=NAVY, width=3)
        text(d, (gx(R), GY0 + 42), str(R), 38, MUTED, bold=False)
    if k100 > 0:
        dash(d, (GX0, gy(100)), (GX1 + 20, gy(100)), A(RED, k100))
        text(d, (GX1 + 20, gy(100) - 34), "100 %: không chạm", 38, RED, anchor="rm", alpha=k100)
    if curve > 0:
        pts = []; Rm = 10 * curve; n = 80
        for i in range(n + 1):
            R = Rm * i / n; pts.append((gx(R), gy(100 * R / (R + R_IN))))
        d.line(pts, fill=A(GREEN, 0.9), width=6, joint="curve")
    for i in range(npts):
        R, _, _, h, _ = ROWS[i]
        col = ORANGE if hl == i else BLUE
        dot(d, gx(R), gy(h), 14, col, outline=WHITE)
        ox, oy = LAB_OFF[i]
        text(d, (gx(R) + ox, gy(h) + oy), hs(h), 40, col, anchor="lm" if ox else "mm")

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh, khong nut A-D) ----------------
Q_AT = 1.4
def s_hook(img, d, t, sc):
    circuit(d, "– Ω", False, "0,00 A", "0,00 V")
    a = appear(t, Q_AT, 0.5)
    if a <= 0: return
    y0 = 930 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(38)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 38, WHITE, alpha=a)
    ctext(d, y0 + 280, "Lần lượt đặt R = 1,0; 2,0;\n4,0; 9,0 Ω. Ở R nào,\nhiệu suất H của pin lớn nhất?",
          48, INK, maxw=900, alpha=a)
    tc, tend = Q_AT + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 500, 940, y0 + 512], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 500, 140 + 800 * (1 - p), y0 + 512], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
SET0, CL0, OP0 = 0.4, 1.8, 3.9       # lan R = 1,0 Ohm (lam cham): dat R, dong K, mo K
FW, DCL, DOP = 1.7, 0.5, 1.35        # tua nhanh: moi lan FW giay; dong K sau DCL, mo K sau DOP
def plan(sc):
    """[(luc dat R, luc dong K, luc mo K)] cho 4 lan do (moc trong canh do)."""
    fs = sc["M"][1] + 0.3
    return [(SET0, CL0, OP0)] + [(fs + j * FW, fs + j * FW + DCL, fs + j * FW + DOP) for j in range(3)]

def state(sc, t):
    """-> (nhan hop R, K dong?, so chi ampe ke, so chi von ke, so diem da cham). Doi CUNG luc theo moc."""
    rl, closed, npts = "– Ω", False, 0
    for i, (ts, tc, to) in enumerate(plan(sc)):
        if t >= ts: rl = vn(ROWS[i][0]) + " Ω"
        if t >= tc: npts = i + 1
        if tc <= t < to: closed = True
    if closed:
        R, I, U, _, _ = ROWS[npts - 1]
        return rl, True, vn(I, 2) + " A", vn(U, 2) + " V", npts
    return rl, False, "0,00 A", "0,00 V", npts

def s_do(img, d, t, sc):
    rl, closed, ra, rv, npts = state(sc, t)
    circuit(d, rl, closed, ra, rv)
    if t >= sc["M"][1] + 0.3:
        card(d, (760, 214, 1000, 274), fill=ORANGE, r=30); text(d, (880, 244), "tua nhanh", 38, WHITE)
    graph(d, npts, hl=npts - 1 if npts else None)
    if closed:
        R, I, U, h, _ = ROWS[npts - 1]
        card(d, (150, 810, 930, 890), fill=(236, 242, 255), outline=BLUE, r=22, w=3)
        text(d, (W / 2, 850), f"H = U/E = {vn(U, 2)} / 3,0 = {hs(h)}", 42, BLUE)

# ---------------- canh 3: Dap an + rut ra + chua noi duoc ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · R = 9,0 Ω (R lớn nhất)"
    pw = tw(d, lab, F(40)) + 52
    card(d, (W / 2 - pw / 2, 234, W / 2 + pw / 2, 298), fill=A(NAVY, ka), r=32)
    text(d, (W / 2, 266), lab, 40, WHITE, alpha=ka)
    kc = appear(t, 0.6, 1.2)
    k100 = appear(t, 0.8, 0.5)
    graph(d, 4, curve=kc, k100=k100, hl=3)
    k2 = appear(t, M[1] - 0.1, 0.4)
    k1 = appear(t, 0.5, 0.45) * (1 - k2)
    if k1 > 0:
        card(d, (60, 330, 1020, 790), fill=A((236, 253, 243), k1), outline=A(GREEN, k1), w=5)
        rich(d, W / 2, 440, "H = U/E = R/(R + r)", 56, DGREEN, alpha=k1)
        text(d, (W / 2, 580), "r > 0 nên H < 100 %", 46, RED, alpha=k1 * appear(t, 0.8, 0.4))
        text(d, (W / 2, 690), "(còn hao phí I²r trong pin)", 40, INK, bold=False,
             alpha=k1 * appear(t, 1.1, 0.4))
    if k2 > 0:
        y0 = 330 + (1 - k2) * 30
        card(d, (60, y0, 1020, y0 + 460), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 75), "Chưa nói được", 48, NAVY, alpha=k2)
        for j, l1 in enumerate(("• r của pin đo bằng cách nào?", "• Pin dùng lâu: E, r có đổi?")):
            kk = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (110, y0 + 200 + j * 130), l1, 44, INK, anchor="lm", alpha=kk)

# ---------------- canh 4: Bay (cot cong suat mach ngoai) ----------------
BX = (230, 430, 630, 830); BW, BY0, BH = 130, 1400, 420     # cot P_R: 2,25 W cao BH
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.1, 0.4)
    card(d, (60, 300, 1020, 740), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
    pw = tw(d, "BẪY", F(38)) + 52
    card(d, (W / 2 - pw / 2, 330, W / 2 + pw / 2, 394), fill=A(DRED, a1), r=32)
    text(d, (W / 2, 362), "BẪY", 38, WHITE, alpha=a1)
    kx = appear(t, M[1] - 0.1, 0.4)
    q = "“R = r thì H lớn nhất”"
    text(d, (W / 2 + 30, 480), q, 48, mix(INK, WHITE, 0.55 * kx), alpha=a1)   # cau sai mo dan khi bi bac
    if kx > 0:       # dau X lon ben trai cau sai (khong che chu)
        cx = W / 2 + 30 - tw(d, q, F(48)) / 2 - 56; s = 26 * kx
        d.line([(cx - s, 480 - s), (cx + s, 480 + s)], fill=DRED, width=9)
        d.line([(cx - s, 480 + s), (cx + s, 480 - s)], fill=DRED, width=9)
        text(d, (W / 2, 590), "R = r: P = UI lớn nhất", 46, DGREEN, alpha=kx)
        text(d, (W / 2, 670), "nhưng H chỉ 50 %", 46, DRED, alpha=appear(t, M[1] + 0.8, 0.4))
    # cot P_R
    card(d, (40, 820, 1040, 1600), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 875), "Công suất mạch ngoài P = UI", 40, INK)
    d.line([(90, BY0), (990, BY0)], fill=NAVY, width=4)
    for i, (R, I, U, h, p) in enumerate(ROWS):
        kb = appear(t, 0.3 + 0.2 * i, 0.4)
        if kb <= 0: continue
        x = BX[i]; hh = BH * p / 2.25 * kb
        hot = i == 0 and kx > 0
        d.rectangle([x - BW / 2, BY0 - hh, x + BW / 2, BY0], fill=ORANGE if hot else (147, 180, 240),
                    outline=NAVY, width=3)
        text(d, (x, BY0 - hh - 30), vn(p, 2) + " W", 38, INK, alpha=kb)
        text(d, (x, BY0 + 40), vn(R) + " Ω", 38, INK, alpha=kb)
        text(d, (x, BY0 + 92), "H " + hs(h), 40, DRED if hot else MUTED, bold=hot, alpha=kb)

# ---------------- canh 5: Chot + cau hoi tu nho lai (goi y tre ~2,5 s) ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: pin moi r = 0,2 Ohm, R = 1,0 Ohm -> H = 83 %."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 330, 1020, 610), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 470, "R càng lớn so với r,\nH càng gần 100 %", 52, GREEN, maxw=900, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 680, 1040, 1420), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(38)) + 52
    card(d, (W / 2 - pw / 2, 710, W / 2 + pw / 2, 774), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 742), "THỬ NGHĨ", 38, WHITE, alpha=k1)
    ctext(d, 930, "Thay hai pin mới, r = 0,2 Ω,\nvẫn đặt R = 1,0 Ω.\nH khoảng bao nhiêu %?", 48, INK,
          maxw=920, alpha=appear(t, M[0] + 0.4, 0.5))
    kh = appear(t, M[0] + 2.9, 0.5)
    if kh <= 0: return
    card(d, (110, 1150, 970, 1380), fill=A((255, 247, 237), kh), r=24)
    ctext(d, 1205, "Gợi ý", 40, (154, 52, 18), alpha=kh)
    ctext(d, 1300, "Đồ thị lúc nãy vẽ với r = 1,0 Ω", 46, INK, maxw=840, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    pl = plan(do)
    out = [(h["t0"] + Q_AT, "open"), (h["t0"] + h["T"] - 0.6, "ding"), (do["t0"] + pl[0][1], "tap")]
    out += [(do["t0"] + tc, "tick") for _, tc, _ in pl[1:]]
    out += [(da["t0"] + 0.1, "ding"), (b["t0"] + 0.1, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]
    return out

def _kiem_dong_bo(clip):
    """Moi 0,05 s canh Tien hanh: K dong <=> dong ho khac 0; so chi khop dung hang so diem; U = IR, H = U/E."""
    build(clip); sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; loi = 0
    while t < sc["T"]:
        rl, closed, ra, rv, n = state(sc, t)
        if closed:
            R, I, U, h, p = ROWS[n - 1]
            ok = (ra == vn(I, 2) + " A" and rv == vn(U, 2) + " V" and rl == vn(R) + " Ω"
                  and abs(I * R - U) < 1e-9 and abs(100 * U / E_ - h) < 0.05 and abs(E_ / (R + R_IN) - I) < 1e-9
                  and abs(U * I - p) < 1e-9)
        else:
            ok = ra == "0,00 A" and rv == "0,00 V"
        seen = []; orig = ImageDraw.ImageDraw.text           # dong "H = U/E" tren khung chi khi K dong
        ImageDraw.ImageDraw.text = lambda self, xy, s_, *a, **k: (seen.append(s_), orig(self, xy, s_, *a, **k))[1]
        try:
            im = Image.new("RGB", (W, H), BG); IMG_REF[0] = im; s_do(im, ImageDraw.Draw(im, "RGBA"), t, sc)
        finally:
            ImageDraw.ImageDraw.text = orig
        if any(x.startswith("H = U/E") for x in seen) != closed: ok = False
        if not ok: loi += 1; print("lệch", round(t, 2), rl, closed, ra, rv, n)
        t += 0.05
    # dong H (s_do) ve khi va chi khi closed -> cung dieu kien voi so chi dong ho
    print("đồng bộ dụng cụ:", "OK" if loi == 0 else f"{loi} lỗi")

CLIP = dict(id="tn-l11-nang-luong-dien-03", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Năng lượng điện · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Hiệu suất của pin", draw=s_hook, tail=0.7, caps=[
   ("Hai pin AA nối với hộp điện trở.", 3.0),
   ("Tự đoán trước khi xem tiếp.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.8, caps=[
   ("Đặt R = 1,0 Ω, đóng K, đọc nhanh.", 4.6),
   ("Lặp lại, nghỉ 30 s giữa các lần.", 5.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.7, caps=[
   ("H tăng dần khi R tăng.", 4.0),
   ("Thí nghiệm mới đo một cặp pin.", 4.6)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.8, caps=[
   ("Bẫy: nhầm H với công suất ra.", 3.4),
   ("Cột cao nhất lại có H thấp nhất.", 4.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Dừng video, tự trả lời.", 7.4)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in sys.argv:
    _kiem_dong_bo(CLIP)
