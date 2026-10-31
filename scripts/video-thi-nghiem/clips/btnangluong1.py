# Clip: tn-l11-baitapnangluong-01 - Do co nang con lac lo xo treo theo bien do (31/10/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-baitapnangluong-01.json:
#   tham_so: m = 0,25 kg ; A 1..4 cm. cac_buoc.lam: dan 5,0 cm -> k = 49 N/m ; A = 1; 1,5; 2; 3; 4 cm ;
#     dien thoai 240 hinh/giay. so_lieu_mau (A cm, v_max do cm/s, 1/2 m v^2 mJ, 1/2 k A^2 mJ):
#     1 13,5 2,3 2,45 ; 1,5 20,5 5,3 5,51 ; 2 27,5 9,5 9,8 ; 3 41,5 21,5 22,05 ; 4 55,0 37,8 39,2.
#   quan_sat: W/A^2 ~ 2,3-2,4 mJ/cm^2. hien_tuong_hay_sai[1]: the A bang cm vao 1/2 k A^2, ghi J -> canh bay.
#   Du doan: A tang 1 -> 4 cm, W gap may lan? (dap an khoang 16: 37,8 / 2,3; khac cap 1 -> 3 cm cua kho va
#     khac Du doan dau bai (goc 5 -> 10 do, gap 4)). Lua chon (khung ben canh): 4 lan / 8 lan / khoang 16 lan / 64 lan.
#   Cau chot: muon W gap doi thi A gap may lan? -> can 2 ~ 1,4 lan (khong hien; nguoc phan xa "gap 2").
#   Khong giai cau hoi sai so ngay sau hop trong bai (hang nao kem tin cay, vi sao do thap hon mo hinh).
# Dan canh rieng (khac motadddh1/2, vantocdddh1, conangdddh1): lo xo TREO + thuoc dung (0 o VTCB) + dien thoai;
#   truc chinh = DO THI W theo A tich diem qua 5 lan tha + bang 5 hang; dap an them duong cong 1/2 k A^2 (net dut).
# Chuyen dong: x = A cos(omega tau) (x huong xuong, 0 o VTCB), omega = sqrt(k/m) = 14 rad/s; phat lai cham 8 lan
#   (240 hinh/giay chieu o 30 hinh/giay) -> omega tren video 1,75 rad/s, qua VTCB sau 0,898 s ke tu luc tha.
#   So v cua hang chi hien khi vat da qua VTCB; W va diem do thi hien sau do 0,1 s (mot nguon: meas_state()).
from engine import *

M_KG, K_NM = 0.25, 49.0
ROWS = [(1.0, "1", "13,5", "2,3", 2.3), (1.5, "1,5", "20,5", "5,3", 5.3), (2.0, "2", "27,5", "9,5", 9.5),
        (3.0, "3", "41,5", "21,5", 21.5), (4.0, "4", "55,0", "37,8", 37.8)]   # A, nhan A, v do, W nhan, W so
WV = math.sqrt(K_NM / M_KG) / 8                 # rad/s tren video (phat cham 8 lan)
QT = (math.pi / 2) / WV                         # 0,898 s: tu luc tha toi VTCB
DBLUE = (29, 78, 216); DRED = (185, 28, 28); DGREEN = (21, 110, 55)
BLOCK = (250, 204, 120); RULERC = (250, 240, 200)
CPT = (37, 99, 235)                             # mau diem do

def eq(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """Cong thuc: _{..} chi so duoi, ^{..} so mu (>= 36 px)."""
    fs = []
    for p in [p for p in re.split(r"(_\{[^}]*\}|\^\{[^}]*\})", s) if p]:
        if p.startswith("_{"): fs.append((p[2:-1], F(max(36, size * 0.62)), size * 0.26))
        elif p.startswith("^{"): fs.append((p[2:-1], F(max(36, size * 0.62)), -size * 0.34))
        else: fs.append((p, F(size), 0))
    tot = sum(tw(d, p, f) for p, f, _ in fs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for p, f, dy in fs:
        dtext(d, (x, cy + dy), p, f, color, alpha, "lm"); x += tw(d, p, f)
    return tot

def dashed(d, p0, p1, col, w=4, on=16, off=12):
    L = math.dist(p0, p1); n = int(L // (on + off)) + 1
    for i in range(n):
        a = i * (on + off) / L; b = min(1, (i * (on + off) + on) / L)
        if a >= 1: break
        d.line([(lerp(p0[0], p1[0], a), lerp(p0[1], p1[1], a)), (lerp(p0[0], p1[0], b), lerp(p0[1], p1[1], b))], fill=col, width=w)

# ---------------- lo xo treo + thuoc (0 o VTCB) ----------------
PXC = 40                                        # px / cm
TOPY, YN, YV = 330, 430, 630                    # moc treo, dau lo xo chua treo, dau lo xo o VTCB (dan 5,0 cm)
def coil(d, x, ya, yb, amp=26, n=12, col=NAVY, w=5):
    e = 16; pts = [(x, ya), (x, ya + e)]; L = (yb - e) - (ya + e)
    for i in range(1, 2 * n): pts.append((x + (amp if i % 2 else -amp), ya + e + L * i / (2 * n)))
    pts += [(x, yb - e), (x, yb)]
    d.line(pts, fill=col, width=w, joint="curve")

def hanger(d, sx, x_cm, base=930, ruler=True, ml=True):
    """Gia treo: cot o sx-200, lo xo truc sx; x_cm > 0 la duoi VTCB. Tra ve y dau duoi lo xo."""
    px = sx - 200
    d.rectangle([px - 40, base, px + 230, base + 26], fill=GRAY, outline=NAVY, width=3)
    d.rectangle([px - 10, TOPY - 14, px + 10, base], fill=GRAY, outline=NAVY, width=3)
    d.rectangle([px - 10, TOPY - 18, sx + 20, TOPY + 4], fill=GRAY, outline=NAVY, width=3)
    ye = YV + x_cm * PXC
    coil(d, sx, TOPY + 4, ye)
    d.line([(sx, ye), (sx, ye + 20)], fill=NAVY, width=5)
    d.rounded_rectangle([sx - 60, ye + 20, sx + 60, ye + 100], radius=14, fill=BLOCK, outline=NAVY, width=4)
    if ml: text(d, (sx, ye + 60), "250 g", 36, INK)
    if ruler:                                   # thuoc dung: 0 o VTCB, -4..4 cm, vach mm
        rx = sx + 82
        d.rectangle([rx, YV - 4 * PXC - 14, rx + 34, YV + 4 * PXC + 14], fill=RULERC, outline=NAVY, width=2)
        for k in range(-40, 41):
            y = YV + k * PXC / 10
            L = 22 if k % 10 == 0 else (14 if k % 5 == 0 else 7)
            d.line([(rx, y), (rx + L, y)], fill=NAVY, width=3 if L == 22 else 2)
        for k in (-4, -2, 0, 2, 4): text(d, (rx + 46, YV + k * PXC), str(abs(k)), 36, INK, anchor="lm")
        d.line([(sx + 20, ye), (rx, ye)], fill=ORANGE, width=4)          # kim chi: dau duoi lo xo
    return ye

# ---------------- do thi W theo A (truc co dinh o canh do va dap an) ----------------
GX0, GY0, SXA, SYW = 220, 1560, 180, 12         # goc; px/cm; px/mJ
def GX(a): return GX0 + a * SXA
def GY(w): return GY0 - w * SYW
def axes(d):
    d.line([(GX0, GY0), (1000, GY0)], fill=INK, width=4)
    d.line([(GX0, GY0), (GX0, 1050)], fill=INK, width=4)
    d.polygon([(1012, GY0), (994, GY0 - 9), (994, GY0 + 9)], fill=INK)
    d.polygon([(GX0, 1038), (GX0 - 9, 1056), (GX0 + 9, 1056)], fill=INK)
    for a in (1, 2, 3, 4):
        d.line([(GX(a), GY0), (GX(a), GY0 + 12)], fill=INK, width=3)
        text(d, (GX(a), GY0 + 40), str(a), 36, INK)
    for w in (10, 20, 30, 40):
        d.line([(GX0 - 12, GY(w)), (GX0, GY(w))], fill=INK, width=3)
        dashed(d, (GX0 + 4, GY(w)), (990, GY(w)), LIGHT, w=2, on=8, off=10)
        text(d, (GX0 - 22, GY(w)), str(w), 36, INK, anchor="rm")
    text(d, (GX0 + 20, 1030), "W (mJ)", 38, INK, anchor="lm")
    text(d, (1040, GY0 + 86), "A (cm)", 38, INK, anchor="rm")

def model_curve(d, alpha=1.0, upto=1.0):
    pts = [(GX(a), GY(0.5 * K_NM * (a / 100) ** 2 * 1000)) for a in [i * 4.15 * upto / 80 for i in range(81)]]
    for i in range(0, len(pts) - 1, 2):
        d.line([pts[i], pts[i + 1]], fill=A(ORANGE, alpha), width=5)

# ---------------- canh: Du doan (K10: chi cau hoi + hinh) ----------------
def bracket(d, x, y0, y1, lab, col, alpha=1.0, side="r"):
    d.line([(x, y0), (x, y1)], fill=A(col, alpha), width=5)
    for yy in (y0, y1): d.line([(x - 12, yy), (x + 12, yy)], fill=A(col, alpha), width=5)
    if side == "r": text(d, (x + 20, (y0 + y1) / 2), lab, 40, col, anchor="lm", alpha=alpha)
    else: text(d, (x - 20, (y0 + y1) / 2), lab, 40, col, anchor="rm", alpha=alpha)

def s_hook(img, d, t, sc):
    M = sc["M"]
    k1 = ease((t - 0.5) / 0.8); k2 = ease((t - 1.0) / 0.8)
    for sx, a_cm, kk in ((330, 1.0, k1), (800, 4.0, k2)):
        hanger(d, sx, a_cm * kk, base=960, ruler=False)
        dashed(d, (sx - 110, YV), (sx + 110, YV), MUTED, w=4)
        if kk > 0.98: bracket(d, sx + 130, YV, YV + a_cm * PXC, f"{int(a_cm)} cm", ORANGE)
    kv = appear(t, 1.9, 0.4)
    if kv > 0:
        text(d, (215, YV - 34), "VTCB", 38, MUTED, alpha=kv)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1040 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 460), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(36)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 36, WHITE, alpha=a)
    ctext(d, y0 + 235, "Biên độ tăng từ 1 cm lên 4 cm.\nCơ năng gấp mấy lần?", 50, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - 0.3
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 400, 940, y0 + 412], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 400, 140 + 800 * (1 - p), y0 + 412], radius=6, fill=A(PURPLE, a))

# ---------------- canh: Tien hanh - 5 lan tha ----------------
RS0, RD = 0.5, 2.4                              # lan dau bat dau; moi lan
PULL, HOLD = 0.45, 0.6                          # keo xong; tha luc 0,6 s
def meas_state(t):
    """-> (i lan, x cm, da tha, hien v, hien W). Mot nguon cho vat, kim thuoc, bang, diem do thi."""
    if t < RS0: return -1, 0.0, False, False, False
    i = min(4, int((t - RS0) // RD)); s = t - RS0 - i * RD
    a = ROWS[i][0]
    if s < HOLD:
        if i == 0: x0 = 0.0
        else: x0 = ROWS[i - 1][0] * math.cos(WV * (RD - HOLD))
        x = lerp(x0, a, ease(s / PULL)); return i, x, False, False, False
    tau = s - HOLD
    return i, a * math.cos(WV * tau), True, tau >= QT, tau >= QT + 0.1

TBX = [700, 840, 980]; TBY0 = 400; TBH = 54     # bang: cot A, v, W; hang
def s_do(img, d, t, sc):
    M = sc["M"]
    i, x, rel, sv, sw = meas_state(t)
    ye = hanger(d, 260, x)
    dashed(d, (150, YV), (330, YV), MUTED, w=3)
    # dien thoai
    card(d, (440, 430, 590, 700), fill=NAVY, r=22)
    d.rounded_rectangle([452, 446, 578, 684], radius=12, fill=(40, 52, 90))
    dot(d, 470, 470, 9, (90, 100, 130))
    if rel and int(t * 3) % 2 == 0: dot(d, 556, 470, 10, RED)
    text(d, (515, 600), "240", 40, WHITE)
    text(d, (515, 742), "hình/giây", 36, INK)
    text(d, (515, 790), "phát chậm", 36, ORANGE)
    # bang 5 hang
    card(d, (620, 330, 1050, 690), fill=WHITE, outline=NAVY, r=18, w=3)
    for cx, hd in zip(TBX, ("A", "v", "W")): text(d, (cx, 362), hd, 40, INK)
    d.line([(632, 392), (1038, 392)], fill=NAVY, width=3)
    for j in range(5):
        if j > i: break
        y = TBY0 + TBH * (j + 0.5) + 6
        if j == i: d.rounded_rectangle([628, y - 25, 1042, y + 25], radius=10, fill=(255, 237, 213))
        a_l, v_l, w_l = ROWS[j][1], ROWS[j][2], ROWS[j][3]
        if j < i or t - RS0 - j * RD >= PULL: text(d, (TBX[0], y), a_l, 38, INK)
        if j < i or sv: text(d, (TBX[1], y), v_l, 38, DGREEN)
        if j < i or sw: text(d, (TBX[2], y), w_l, 38, CPT)
    text(d, (835, 730), "đơn vị: cm · cm/s · mJ", 36, MUTED)
    eq(d, 835, 795, "W = ½mv^{2}", 40, INK)
    text(d, (835, 860), "dãn 5,0 cm → k = 49 N/m", 36, DBLUE)
    # do thi
    axes(d)
    for j in range(5):
        if j < i or (j == i and sw):
            a_c, _, _, _, w = ROWS[j]
            dot(d, GX(a_c), GY(w), 13 if j == i else 11, CPT, outline=NAVY)

# ---------------- canh: Dap an + rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.1, 0.5)
    lab = "ĐÁP ÁN · khoảng 16 lần"
    pw = tw(d, lab, F(42)) + 56
    card(d, (W / 2 - pw / 2, 290, W / 2 + pw / 2, 354), fill=A(NAVY, ka), r=32)
    text(d, (W / 2, 322), lab, 42, WHITE, alpha=ka)
    axes(d)
    km = appear(t, M[1] + 0.1, 0.6)
    if km > 0:
        model_curve(d, km, upto=km)
        kl = appear(t, M[1] + 0.6, 0.4)
        eq(d, GX(3.55), GY(28), "½kA^{2}", 40, ORANGE, alpha=kl, anchor="l")
    for j, (a_c, _, _, w_l, w) in enumerate(ROWS):
        hl = j in (0, 4)
        dot(d, GX(a_c), GY(w), 13, CPT, outline=NAVY)
        if hl:
            kh = appear(t, 0.6, 0.4)
            if kh > 0: d.ellipse([GX(a_c) - 26, GY(w) - 26, GX(a_c) + 26, GY(w) + 26], outline=A(DRED, kh), width=5)
    kh = appear(t, 0.6, 0.4)
    if kh > 0:
        text(d, (GX(1), GY(2.3) - 66), "2,3 mJ", 40, DRED, alpha=kh)
        text(d, (GX(4) - 40, GY(37.8) - 10), "37,8 mJ", 40, DRED, anchor="rm", alpha=kh)
    k1 = appear(t, M[0] + 0.6, 0.4)
    if k1 > 0:
        card(d, (60, 400, 1020, 560), fill=A((254, 242, 242), k1), outline=A(DRED, k1), r=20, w=3)
        eq(d, W / 2, 480, "37,8 : 2,3 ≈ 16 = 4^{2}", 52, DRED, alpha=k1)
    k2 = appear(t, M[1] + 0.8, 0.4)
    if k2 > 0:
        card(d, (60, 610, 1020, 780), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), r=20, w=3)
        eq(d, W / 2, 696, "W : A^{2} ≈ 2,3–2,4 mJ/cm^{2}", 48, DGREEN, alpha=k2)

# ---------------- canh: Bay roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.0, 0.3) * (1 - k2)
    kc = appear(t, M[0] + 2.2, 0.5)
    # thuoc 0..4 cm phong to (200 px/cm)
    x0, px = 140, 200
    d.rectangle([x0 - 20, 440, x0 + 4 * px + 20, 540], fill=RULERC, outline=NAVY, width=3)
    for k in range(0, 41):
        L = 40 if k % 10 == 0 else (26 if k % 5 == 0 else 14)
        d.line([(x0 + k * px / 10, 440), (x0 + k * px / 10, 440 + L)], fill=NAVY, width=3 if L == 40 else 2)
    for k in range(5): text(d, (x0 + k * px, 510), str(k), 38, INK)
    d.line([(x0, 400), (x0 + 4 * px, 400)], fill=ORANGE, width=5)
    for xx in (x0, x0 + 4 * px): d.line([(xx, 386), (xx, 414)], fill=ORANGE, width=5)
    text(d, (x0 + 2 * px, 360), "A = 4 cm", 42, ORANGE)
    kk = appear(t, M[0] + 2.2, 0.4)
    if kk > 0: text(d, (x0 + 2 * px, 600), "= 0,04 m", 46, DGREEN, alpha=kk)
    if a1 > 0:
        y0 = 700
        card(d, (40, y0, 1040, y0 + 520), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(38)) + 52
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 60), "BẪY", 38, WHITE, alpha=a1)
        yy = y0 + 180
        lw = eq(d, W / 2, yy, "½·49·4^{2} rồi ghi J", 48, DRED, alpha=a1)
        text(d, (W / 2 + lw / 2 + 40, yy), "✗", 48, DRED, alpha=a1)
        if kc > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 4), (W / 2 - lw / 2 - 6 + (lw + 12) * kc, yy + 4)], fill=A((140, 15, 15), a1), width=6)
            eq(d, W / 2, y0 + 310, "½·49·0,04^{2} = 0,0392 J", 48, DGREEN, alpha=a1 * kc)
            text(d, (W / 2, y0 + 420), "✓ = 39,2 mJ", 48, DGREEN, alpha=a1 * kc)
    if k2 > 0:
        y0 = 700 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 380), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 70), "Chưa nói được", 46, NAVY, alpha=k2)
        for j, l1 in enumerate(("• A từ 5 cm trở lên: chưa thử", "• Khối lượng lò xo: bỏ qua")):
            kk2 = k2 * appear(t, M[1] + 0.3 + 0.5 * j, 0.4)
            text(d, (90, y0 + 180 + j * 110), l1, 44, INK, anchor="lm", alpha=kk2)

# ---------------- canh: Chot + cau hoi tu nho lai ----------------
def _end_body(d, t, k1):
    """Hai cot: W va 2W (dieu kien, khong phai dap so); goi y tre 2,5 s sau cau hoi."""
    kq = appear(t, END_M0 + 0.4, 0.5) * k1
    if kq > 0:
        base = 1230
        for bx, h, lab, sub in ((330, 110, "W", "A_{1}"), (600, 220, "2W", "?")):
            d.rectangle([bx, base - h, bx + 110, base], fill=A(CPT, kq), outline=A(NAVY, kq), width=3)
            text(d, (bx + 55, base - h - 34), lab, 44, CPT, alpha=kq)
            eq(d, bx + 55, base + 40, sub, 44, PURPLE if sub == "?" else INK, alpha=kq)
    kh = appear(t, END_M0 + 0.4 + 2.5, 0.5) * k1
    if kh > 0:
        card(d, (110, 1340, 970, 1520), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, 1385), "Gợi ý", 36, MUTED, bold=False, alpha=kh)
        text(d, (W / 2, 1462), "Thử A gấp 2: W gấp mấy?", 42, ORANGE, alpha=kh)

END_M0 = 0.4
def s_end(img, d, t, sc):
    chot_hoi(d, t, sc, "Cơ năng tỉ lệ với bình phương biên độ.", "Muốn cơ năng gấp đôi,\nbiên độ phải gấp mấy lần?",
             goi_y=None, body=_end_body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, dv, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (dv["t0"] + 0.1, "ding")] + [
            (dv["t0"] + RS0 + j * RD + HOLD, "tap") for j in range(5)] + [
            (da["t0"] + 0.1, "ding"), (b["t0"] + 0.2, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l11-baitapnangluong-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Năng lượng dao động · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Lò xo treo, hai biên độ", draw=s_hook, tail=0.9, caps=[
   "Cùng một con lắc, hai lần kéo.",
   ("Tự đoán trước khi xem tiếp.", 5.2)]),
 dict(key="do", title="Năm lần thả", draw=s_do, tail=0.9, caps=[
   ("Thả từ A, đo tốc độ qua VTCB.", 4.0),
   ("Năm biên độ, mỗi lần một điểm.", 7.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Gấp 4 lần biên, bình phương lên.", 3.8),
   ("Điểm đo bám đường cong mô hình.", 4.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Bẫy: thế A theo cm vào công thức.", 4.6),
   ("Số trong clip là số minh hoạ.", 4.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.4, caps=[
   ("Dừng video, tự trả lời.", 5.8)]),
])
