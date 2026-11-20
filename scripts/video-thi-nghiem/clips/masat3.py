# Clip: tn-l10-luc-ma-sat-03 - Tim he so ma sat bang goc nghieng tam van (lo 7, 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-luc-ma-sat-03.json: van dai L = 1,00 m ; so_lieu_mau:
#   bat dau truot h 0,34 m (19,9 do, tan 0,36) ; truot deu h 0,29 m (16,9 do, tan 0,30) ; ghi_chu: day = can(L2 - h2)
#   = 0,940 m (_kiem_so()). Them vao kho: hang "them gia trong" h 0,34 m SUY TU MO HINH (goc khong phu thuoc m:
#   tan = mu_n), khong phai so do -> tren man ghi "(theo mo hinh)".
# Hinh chinh KHAC masat1 (luc ke + do thi F-t) va masat2 (cot so sanh): van nghieng NANG DAN + thuoc do h dung dung,
#   ket qua la TAM GIAC van (dai 1,00 m ; h ; day 0,94 m) -> tan alpha. Khong co luc ke.
# Du doan (K10: chi cau hoi + hinh, khung ben canh co lua chon): nang dan van toi luc hop bat dau truot ; ha van, bung nhe
#   cho hop truot deu -> h luc truot deu so voi luc bat dau truot?  A. Cao hon ; B. Bang nhau ; C. Thap hon (DUNG).
# KHONG tra loi san: Cau 3 (tu dung yen: ma sat = luc day) -> clip khong co the "chua truot: ma sat nghi = ..." ;
#   Cau 4 (sach tren mat nghieng 30 do, tinh Fms) -> clip khong hien N = mg.cos, khong tinh luc nao bang so.
# Bay = hien_tuong_hay_sai[0] "vat nang hon truot o goc nho hon" -> them gia trong van bat dau truot o 0,34 m
#   (khong dung bay "ma sat nghi luon bang muN" cua masat1). Chua noi duoc: nang cao hon 0,34 m -> hop nhanh dan ra sao
#   (mo_hinh: a = g(sin - mu.cos)) -> Dinh luat 2 Newton.
# Cau chot (ghi trong ghi_chu kho): hop 0,20 kg (cung hop TN 01) dung yen tren van h = 0,20 m (tham_so mac_dinh)
#   -> ma sat nghi = P_x = m.g.h/L = 0,20.9,8.0,20 = 0,39 N (KHONG phai mu_n.N = 0,69 N). So 0,20 m / 0,39 N chua hien.
# Tu kiem: python clips/masat3.py --kiem-dong-bo
import math
from engine import *

L_M = 1.00
H_N, H_D = 0.34, 0.29                 # bat dau truot, truot deu (so_lieu_mau)
MU_N, MU = 0.36, 0.30
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
def base(h): return math.sqrt(L_M ** 2 - h ** 2)
def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-luc-ma-sat-03.json")))
    hang = k["so_lieu_mau"]["hang"]
    assert (hang[0][1], hang[0][3], hang[1][1], hang[1][3]) == (H_N, MU_N, H_D, MU)
    assert round(H_N / base(H_N), 2) == MU_N and round(H_D / base(H_D), 2) == MU and round(base(H_N), 2) == 0.94
    assert any(r[1] == H_N and "gia trọng" in r[0] for r in hang)
_kiem_so()

WOOD = (176, 124, 74); WOOD_D = (140, 96, 54); BOX = (214, 170, 110); BOX_D = (150, 104, 56)
BOARD = (196, 150, 98); RULER = (254, 243, 199); DGREEN = (21, 110, 55); DRED = (185, 28, 28); NOTE = (60, 64, 84)
WEIGHT = (90, 98, 120); SKIN = (240, 196, 160); SKIN_D = (190, 140, 105)

_TI = {}
def TI(size):
    size = int(size)
    if size not in _TI: _TI[size] = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf", size)
    return _TI[size]

def mrun(d, x, y, parts, size, color, alpha=1.0, anchor="m"):
    """parts: [(chu, kieu)] kieu 's' = SF dam, 'i' = Times Bold Italic (alpha, mu), 'b' = chi so duoi Times (>= 40 px)."""
    fs = {"s": F(size), "i": TI(size * 1.15), "b": TI(max(40, size * 0.8))}
    tot = sum(tw(d, p, fs[k]) for p, k in parts)
    x0 = x - tot / 2 if anchor == "m" else x
    for p, k in parts:
        dtext(d, (x0, y + (size * 0.28 if k == "b" else 0)), p, fs[k], color, alpha, "lm"); x0 += tw(d, p, fs[k])
    return tot

# ---------------- dan thi nghiem: van nang mot dau, thuoc dung ----------------
PX0, PY0 = 60, 930                   # ban le (dau van tren san)
LPX = 800                             # px / m doc van
RX = 930                              # thuoc dung
BW, BH = 0.16 * LPX, 70               # hop
U0 = 0.72                             # tam hop ban dau (m tinh tu ban le)
UMIN = 0.06 + 0.08 + 0.01             # chan o chan van
def ang(h): return math.asin(h / L_M)
def along(u, h, n=0.0):
    a = ang(h); c, s = math.cos(a), math.sin(a)
    return (PX0 + u * LPX * c - n * s, PY0 - u * LPX * s - n * c)

def ruler(d, alpha=1.0):
    c = lambda col: A(col, alpha)
    d.rectangle([RX - 14, PY0 - 0.42 * LPX, RX + 14, PY0], fill=c(RULER), outline=c(NAVY), width=3)
    for k in range(0, 9):
        y = PY0 - k * 0.05 * LPX; L = 20 if k % 2 == 0 else 10
        d.line([(RX - 14, y), (RX - 14 + L, y)], fill=c(NAVY), width=3)
        if k % 2 == 0 and k > 0: text(d, (RX + 26, y), vn(k * 0.05, 1), 40, INK, anchor="lm", alpha=alpha)
    text(d, (RX + 26, PY0 - 0.42 * LPX - 40), "m", 40, INK, anchor="lm", alpha=alpha)

def rig(d, h, u, alpha_box=1.0, weight=False, flick=0.0, hlab=True):
    d.rectangle([40, PY0, 1040, PY0 + 30], fill=WOOD); d.line([(40, PY0), (1040, PY0)], fill=WOOD_D, width=4)
    ruler(d)
    e = along(L_M, h)
    d.line([(e[0], e[1] + 8), (e[0], PY0)], fill=NAVY, width=8)                        # thanh do dau van
    poly = [along(0, h), along(L_M, h), along(L_M, h, -16), along(0, h, -16)]
    d.polygon(poly, fill=BOARD); d.line([along(0, h), along(L_M, h)], fill=WOOD_D, width=4)
    st = [along(0.04, h), along(0.06, h), along(0.06, h, 30), along(0.04, h, 30)]     # chan chan
    d.polygon(st, fill=WOOD_D)
    for xx in range(int(e[0]) + 6, RX - 14, 22): d.line([(xx, e[1]), (min(xx + 12, RX - 14), e[1])], fill=ORANGE, width=4)
    if hlab:
        arrow(d, (RX - 40, PY0), (RX - 40, e[1] + 4), ORANGE, w=4, head=14) if e[0] < RX - 60 else None
    if alpha_box > 0.02:
        q = [along(u - 0.08, h, 0), along(u + 0.08, h, 0), along(u + 0.08, h, BH), along(u - 0.08, h, BH)]
        d.polygon(q, fill=A(BOX, alpha_box)); d.line(q + [q[0]], fill=A(BOX_D, alpha_box), width=4)
        if weight:
            w = [along(u - 0.05, h, BH), along(u + 0.05, h, BH), along(u + 0.05, h, BH + 44), along(u - 0.05, h, BH + 44)]
            d.polygon(w, fill=A(WEIGHT, alpha_box))
        if flick > 0:
            p0 = along(u + 0.08 + 0.02, h, BH / 2); p1 = along(u + 0.08 + 0.02 + 0.14 * flick, h, BH / 2)
            arrow(d, p1, p0, A(PURPLE, alpha_box), w=6, head=18)
            text(d, (p1[0] + 10, p1[1] - 50), "búng", 40, PURPLE, anchor="lm", alpha=alpha_box)

def readout(d, s, state=None, y=320):
    card(d, (60, y - 40, 470, y + 40), fill=(254, 242, 242), r=24)
    text(d, (265, y), s, 46, RED)
    if state:
        s, c = state; text(d, (1010, y), s, 40, c, anchor="rm")

def table(d, y, rows, hl=-1, alpha=1.0, rowsel=(0, 1)):
    n = len(rowsel)
    card(d, (40, y, 1040, y + 130 + n * 90), fill=A(WHITE, alpha), outline=A(NAVY, alpha), w=4)
    text(d, (300, y + 60), "Trạng thái", 44, INK, alpha=alpha); text(d, (790, y + 60), "h (m)", 44, INK, alpha=alpha)
    d.line([(70, y + 105), (1010, y + 105)], fill=A(LIGHT, alpha), width=4)
    lab = ("bắt đầu trượt", "trượt đều")
    for j, i in enumerate(rowsel):
        yy = y + 160 + j * 90
        if i == hl: card(d, (70, yy - 40, 1010, yy + 40), fill=A((255, 237, 213), alpha), r=18)
        if i < rows:
            text(d, (300, yy), lab[i], 46, INK, alpha=alpha)
            text(d, (790, yy), vn((H_N, H_D)[i]), 46, BLUE, alpha=alpha)

# ---------------- canh 1: Du doan ----------------
H_HOOK = 0.10
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 260, 1040, 980), fill=WHITE, outline=LIGHT, w=3)
    rig(d, H_HOOK, U0)
    e = along(L_M, H_HOOK); text(d, (RX - 40, e[1] - 40), "h", 46, ORANGE)
    a = appear(t, M[1] - 0.3, 0.5)
    if a <= 0: return
    y0 = 1000 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 570), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 24, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=32)
    text(d, (W / 2, y0 + 56), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    for j, s in enumerate(("Nâng dần: hộp bắt đầu trượt.", "Hạ bớt, búng nhẹ: trượt đều.",
                           "Lúc trượt đều, h thế nào", "so với lúc bắt đầu trượt?")):
        text(d, (W / 2, y0 + 160 + j * 76), s, 46, INK, alpha=a)
    text(d, (W / 2, y0 + 470), "Chọn đáp án ở khung câu hỏi", 40, MUTED, alpha=a)
    tc, tend = M[1] + 0.3, sc["T"] - 0.2
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 525, 940, y0 + 539], radius=7, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 525, 140 + 800 * (1 - p), y0 + 539], radius=7, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh ----------------
RATE = 0.08                                   # m/s nang van
T_UP0 = 0.4; T_SLIP = T_UP0 + (H_N - H_HOOK) / RATE      # 3,4 s
A_SLIDE = 9.8 * (math.sin(ang(H_N)) - MU * math.cos(ang(H_N)))   # m/s2 khi da truot (van 0,34 m)
V_DEU = 0.16                                  # m/s sau khi bung
def do_state(t, M):
    """-> (h, u, alpha hop, flick, o so, trang thai, so hang bang)."""
    t2 = M[1]                                  # bat dau lan 2
    if t < t2:
        if t < T_UP0: h = H_HOOK
        else: h = min(H_N, H_HOOK + RATE * (t - T_UP0))
        if t < T_SLIP: u, st, rd = U0, ("đứng yên", MUTED), ("h tăng dần…" if t >= T_UP0 else "…")
        else:
            u = max(UMIN, U0 - 0.5 * A_SLIDE * (t - T_SLIP) ** 2); st = ("bắt đầu trượt", ORANGE); rd = "h = " + vn(H_N) + " m"
        rows = 1 if t >= T_SLIP + 0.3 else 0
        return h, u, 1.0, 0.0, rd, st, rows
    tk = t - t2
    T_LOW, T_FL = 0.9, 1.4
    al = 1.0 if tk > 0.3 else appear(tk, 0.0, 0.3)
    h = lerp(H_N, H_D, ease(tk / T_LOW)) if tk < T_LOW else H_D
    if tk < T_FL: u, st, rd, fl = U0, ("hạ ván", MUTED), "…", clamp((tk - T_LOW) / 0.4)
    else:
        u = max(UMIN, U0 - V_DEU * (tk - T_FL)); st = ("trượt đều", DGREEN); rd = "h = " + vn(H_D) + " m"; fl = 1 - clamp((tk - T_FL) / 0.3)
    rows = 2 if tk >= T_FL + 0.8 else 1
    return h, u, al, fl, rd, st, rows

def s_do(img, d, t, sc):
    M = sc["M"]; h, u, al, fl, rd, st, rows = do_state(t, M)
    card(d, (40, 260, 1040, 980), fill=WHITE, outline=LIGHT, w=3)
    rig(d, h, u, alpha_box=al, flick=fl)
    readout(d, rd, st)
    table(d, 1010, rows)

def _kiem_dong_bo():
    """Moi 0,05 s: hop chi roi cho khi h dat dung 0,34 m (lan 1) / 0,29 m (lan 2) ; o so chi hien dung h dang co ;
    hang bang chi hien sau su kien ; lan 2 truot DEU (toc do khong doi) cho toi chan."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; M = sc["M"]; t = 0.0; bad = []; prev = None
    while t < sc["T"]:
        h, u, al, fl, rd, st, rows = do_state(t, M)
        if u < U0 - 1e-9 and t < M[1] and abs(h - H_N) > 1e-9: bad.append((round(t, 2), "truot truoc 0,34"))
        if u < U0 - 1e-9 and t >= M[1] and abs(h - H_D) > 1e-9: bad.append((round(t, 2), "truot khi chua ha xong"))
        if rd.startswith("h = ") and abs(float(rd[4:-2].replace(",", ".")) - h) > 1e-9: bad.append((round(t, 2), "o so != h"))
        if t < M[1] and h > H_N + 1e-9: bad.append((round(t, 2), "nang qua 0,34"))
        if rows >= 1 and not (t >= T_SLIP): bad.append((round(t, 2), "hang 1 som"))
        if rows == 2 and st[0] != "trượt đều": bad.append((round(t, 2), "hang 2 som"))
        if t >= M[1] and st[0] == "trượt đều" and prev is not None and prev > UMIN + 1e-6 and u > UMIN + 1e-6:
            if abs((prev - u) - V_DEU * 0.05) > 1e-6: bad.append((round(t, 2), "khong deu"))
        prev = u if t >= M[1] else None
        t += 0.05
    if T_SLIP + 0.3 > M[1]: bad.append("lan 1 qua ngan")
    if U0 - 0.5 * A_SLIDE * (M[1] - T_SLIP) ** 2 > U0 - 0.15: bad.append("lan 1 hop truot qua it")
    return bad

# ---------------- canh 3: Dap an + Rut ra (tam giac van) ----------------
def pill(d, s, y, a, color=NAVY, size=42):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 36, W / 2 + pw / 2, y + 36), fill=A(color, a), r=34)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

def triangle(d, y0, k, kf):
    ox, oy, Lp = 150, y0 + 420, 600
    b = base(H_N) * Lp; hh = H_N * Lp
    c = lambda col: A(col, k)
    d.line([(ox, oy), (ox + b, oy - hh)], fill=c(WOOD_D), width=8)
    d.line([(ox, oy), (ox + b, oy)], fill=c(NAVY), width=5)
    d.line([(ox + b, oy), (ox + b, oy - hh)], fill=c(ORANGE), width=6)
    d.rectangle([ox + b - 22, oy - 22, ox + b, oy], outline=c(NAVY), width=3)
    a = ang(H_N); d.arc([ox - 90, oy - 90, ox + 90, oy + 90], -math.degrees(a), 0, fill=c(NAVY), width=4)
    dtext(d, (ox + 112, oy - 22), "α", TI(46), INK, k, "lm")
    mx, my = ox + b / 2, oy - hh / 2
    text(d, (mx - 40, my - 50), "dài 1,00 m", 40, WOOD_D, alpha=k)
    text(d, (ox + b + 20, my), vn(H_N) + " m", 40, ORANGE, anchor="lm", alpha=k)
    text(d, (mx, oy + 44), vn(base(H_N)) + " m", 40, NAVY, alpha=k)
    if kf > 0:
        mrun(d, W / 2, y0 + 540, [("μ", "i"), ("n", "b"), (" = tan ", "s"), ("α", "i"),
                                  (" = 0,34 : 0,94 ≈ 0,36", "s")], 46, (154, 52, 18), kf)
    return ox, oy

def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    pill(d, "ĐÁP ÁN · Thấp hơn", 320, ka)
    table(d, 400, 2, hl=1 if appear(t, 0.6, 0.3) > 0.5 else -1)
    kr = appear(t, M[1] - 0.1, 0.45)
    if kr > 0:
        y0 = 770 + (1 - kr) * 20
        card(d, (40, y0, 1040, y0 + 770), fill=A((255, 247, 237), kr), outline=A(ORANGE, kr), w=5)
        pw = tw(d, "RÚT RA", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 90), fill=A(ORANGE, kr), r=32)
        text(d, (W / 2, y0 + 58), "RÚT RA", 40, WHITE, alpha=kr)
        triangle(d, y0, kr, appear(t, M[1] + 1.2, 0.45))
        k2 = appear(t, M[1] + 2.4, 0.45)
        mrun(d, W / 2, y0 + 640, [("Trượt đều (h = 0,29 m): ", "s"), ("μ", "i"), (" ≈ 0,30", "s")],
             46, DGREEN, k2)

# ---------------- canh 4: Bay + chua noi duoc ----------------
H_B0 = 0.24
def bay_state(t):
    """Them gia trong, nang lai tu 0,24 m: bat dau truot dung o 0,34 m."""
    tb0 = 0.4; ts = tb0 + (H_N - H_B0) / (RATE * 0.8)
    h = min(H_N, H_B0 + RATE * 0.8 * max(0.0, t - tb0))
    u = U0 if t < ts else max(UMIN, U0 - 0.5 * A_SLIDE * (t - ts) ** 2)
    return h, u, ts

def s_bay(img, d, t, sc):
    M = sc["M"]
    h, u, ts = bay_state(t)
    card(d, (40, 260, 1040, 980), fill=WHITE, outline=LIGHT, w=3)
    rig(d, h, u, weight=True)
    readout(d, ("h = " + vn(H_N) + " m") if t >= ts else "h tăng dần…", ("thêm gia trọng", NAVY))
    k3 = appear(t, M[1] - 0.1, 0.45); a1 = appear(t, 0.2, 0.4) * (1 - k3)
    y = 1000
    if a1 > 0:
        card(d, (40, y, 1040, y + 480), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y + 26, W / 2 + pw / 2, y + 90), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y + 58), "BẪY", 40, WHITE, alpha=a1)
        ks = clamp((t - ts - 0.3) / 0.4)
        for j, q in enumerate(("“Hộp nặng hơn thì", "trượt ở góc nhỏ hơn”")):
            f = F(48); lw = tw(d, q, f); yy = y + 170 + j * 76
            text(d, (W / 2, yy), q, 48, mix(INK, GRAY, ks), alpha=a1)
            if ks > 0:
                d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)],
                       fill=A(DRED, 0.85 * a1), width=6)
        if ks > 0: text(d, (W / 2 + tw(d, "trượt ở góc nhỏ hơn”", F(48)) / 2 + 40, y + 246), "✗", 48, DRED, alpha=a1 * ks)
        ke = a1 * appear(t, ts + 0.6, 0.4)
        text(d, (W / 2, y + 400), "Vẫn 0,34 m (theo mô hình)", 46, PURPLE, alpha=ke)
    if k3 > 0:
        card(d, (40, y, 1040, y + 340), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        text(d, (W / 2, y + 80), "Chưa nói được", 48, NAVY, alpha=k3)
        kk = k3 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y + 230), "Ván dốc hơn: hộp nhanh dần ra sao?", 46, INK, alpha=kk)

# ---------------- canh 5: Chot + cau hoi tu nho lai ----------------
def s_end(img, d, t, sc):
    """Chot (khong tra loi cau hoi) -> THU NGHI: hop 0,20 kg dung yen o h = 0,20 m -> ma sat ? (0,39 N) ; goi y tre 3 s."""
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 280, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    mrun(d, W / 2, 400, [("Trượt đều: ", "s"), ("μ", "i"), (" = tan ", "s"), ("α", "i")], 52, GREEN, k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 580, 1040, 1420), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 610, W / 2 + pw / 2, 674), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 642), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    for j, s in enumerate(("Hộp 0,20 kg nằm yên trên ván", "có đầu cao 0,20 m.", "Ma sát lên hộp bằng bao nhiêu?")):
        text(d, (W / 2, 790 + j * 80), s, 48, INK, alpha=kq)
    kh = appear(t, M[0] + 3.0, 0.5)
    if kh > 0:
        card(d, (110, 1100, 970, 1360), fill=A((255, 247, 237), kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1160), "Gợi ý", 44, INK, alpha=kh)
        text(d, (W / 2, 1270), "Ván dài 1,00 m; g = 9,8 m/s²", 48, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    _, _, ts = bay_state(0)
    return ([(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
            + [(do["t0"] + T_SLIP, "tap"), (do["t0"] + do["M"][1] + 1.4, "tap")]
            + [(da["t0"] + 0.1, "ding"), (b["t0"] + ts + 0.3, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")])

CLIP = dict(id="tn-l10-luc-ma-sat-03", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Lực ma sát · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Nâng dần tấm ván", draw=s_hook, tail=0.3, caps=[
   ("Hộp gỗ trên tấm ván dài 1,00 m.", 3.4),
   ("Nghĩ trước khi xem tiếp.", 6.0)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Nâng dần đầu ván, đo h.", 4.8),
   ("Hạ ván, búng nhẹ hộp.", 4.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("So hai độ cao h.", 3.0),
   ("Tam giác ván cho hệ số ma sát.", 5.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.6, caps=[
   ("Đúng hay sai?", 4.4),
   ("Câu còn bỏ ngỏ.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.7, caps=[
   ("Dừng video, tự trả lời.", 7.0)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
