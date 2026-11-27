# Clip: tn-l11-dien-truong-02 - Can dien tu "can" luc dien: E = F/q khong phu thuoc dien tich thu (ban 3 cong moi, 27/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-dien-truong-02.json:
#   so_lieu_mau (r cm, q nC, dm g, E do 10^5 V/m): 3 10 0,41 4,02 ; 4 10 0,23 2,25 ; 6 10 0,10 0,98 ; 4 5 0,12 2,35
#   tham_so: Q = 40 nC, g = 9,8 m/s2, can chia 0,01 g, q 2-20 nC (do lon).
#   rut_ra: lan 2 va lan 4 lech 4 %, nam trong sai so doc can. Thanh sai so o Bay (tu suy): 0,01/0,23 = 4 % ; 0,01/0,12 = 8 %.
# Canh: Du doan (K10: chi cau hoi + hinh; q 10 -> 5 nC o r = 4 cm, E?) -> Tien hanh (Q dat san o 3 cm; 3, 4, 6 cm roi cham
#   qua cau trung hoa, q con 5 nC, do lai o 4 cm; bang r - q - dm - E?) -> Ket qua (cot dm chia 2, cot E ~ bang; roi cot
#   E theo r: 3 -> 6 cm chia ~4) -> Bay (2,25 khac 2,35 -> "E phu thuoc q", bac bang thanh sai so chong nhau) + Chua noi
#   duoc -> THU NGHI: q = -10 nC (trai dau) o 4 cm -> can GIAM 0,23 g (tu suy: E giu nguyen, |F| = 0,23 g . g, luc hut len).
#   Cau chot hoi CHIEU (dau) - buoc clip chua chieu; khong trung Cau 4 cua bai (3q -> F x 3).
# Hai qua cau cung dau (+): Q o tren day q xuong -> luc dien tren q huong xuong, so chi can tang (dung vat li).
# Cong moi 27/11: chu than canh >= 56, moi canh <= 180 tu/phut, khoi chu cach >= 2 s, thanh dem 5 o 70 px.
from engine import *

ROWS = [(3, 10, 0.41, 4.02), (4, 10, 0.23, 2.25), (6, 10, 0.10, 0.98), (4, 5, 0.12, 2.35)]   # so_lieu_mau
def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-dien-truong-02.json")))
    assert [tuple(r[1:5]) for r in k["so_lieu_mau"]["hang"]] == ROWS
    for r, q, dm, E in ROWS: assert abs(dm * 1e-3 * 9.8 / (q * 1e-9) / 1e5 - E) < 0.03     # E = dm.g/q
_kiem_so()

def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
CHG = (220, 60, 60); NEU = (160, 165, 180); ROD = (214, 190, 140); DRED = (185, 28, 28); DORANGE = (176, 64, 8)
DGREEN = (20, 83, 45); EMPTY = (148, 140, 128); PEACH = (255, 237, 213)

def pill(d, s, y, a, color=NAVY, size=58, cx=W / 2):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, y - 40, cx + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (cx, y), s, size, WHITE, alpha=a)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- dung cu (khung nguon 1080x1920) ----------------
BX, PAN_Y, PXCM = 380, 800, 55            # truc qua cau, mat dia can, px / cm
YQ = PAN_Y - 120                           # tam qua cau thu q (tren chan cach dien dat tren dia can)
STAND_X = 900                              # gia kep ben phai
def yQ(r): return YQ - r * PXCM            # tam qua cau Q o khoang cach r (cm) phia tren q

def ball(d, x, y, col, sign="+", R=34, alpha=1.0):
    d.ellipse([x - R, y - R, x + R, y + R], fill=A(col, alpha), outline=A(NAVY, alpha), width=3)
    if sign: text(d, (x, y + 1), sign, 58, WHITE, alpha=alpha)

def rig(d, r, q, reading, dm=None, show_r=True, neu_x=None):
    """Can + qua cau q tren chan cach dien + qua cau Q treo tren gia kep, cach r (cm). dm: ve mui ten F ti le dm."""
    d.rectangle([BX - 150, PAN_Y, BX + 150, PAN_Y + 16], fill=(200, 205, 215), outline=NAVY, width=3)
    d.rectangle([BX - 10, PAN_Y + 16, BX + 10, PAN_Y + 34], fill=(120, 125, 140))
    card(d, (BX - 220, PAN_Y + 34, BX + 220, PAN_Y + 200), fill=(70, 78, 100), r=22)
    card(d, (BX - 160, PAN_Y + 62, BX + 160, PAN_Y + 170), fill=(220, 240, 225), r=12)
    text(d, (BX, PAN_Y + 116), reading, 62, (20, 60, 30))
    d.rectangle([BX - 7, YQ + 30, BX + 7, PAN_Y], fill=ROD, outline=NAVY, width=2)
    ball(d, BX, YQ, CHG)
    text(d, (BX + 52, YQ - 26), f"q = {q} nC", 56, INK, anchor="lm")
    y = yQ(r)
    d.rectangle([STAND_X - 8, 270, STAND_X + 8, PAN_Y + 200], fill=(110, 115, 130))
    d.rectangle([STAND_X - 90, PAN_Y + 190, STAND_X + 90, PAN_Y + 212], fill=NAVY)
    d.rectangle([BX - 7, y - 84, STAND_X, y - 70], fill=ROD, outline=NAVY, width=2)
    d.rectangle([STAND_X - 20, y - 100, STAND_X + 20, y - 54], fill=NAVY)
    d.rectangle([BX - 7, y - 84, BX + 7, y - 32], fill=ROD, outline=NAVY, width=2)
    ball(d, BX, y, CHG)
    text(d, (BX + 52, y + 16), "Q = 40 nC", 56, INK, anchor="lm")
    if show_r:
        xa = BX - 70
        arrow(d, ((xa, (y + YQ) / 2)), (xa, y + 4), MUTED, w=4, head=16)
        arrow(d, ((xa, (y + YQ) / 2)), (xa, YQ - 4), MUTED, w=4, head=16)
        text(d, (xa - 18, (y + YQ) / 2), f"r = {r} cm", 56, INK, anchor="rm")
    if dm:                                     # luc day cua Q len q: huong xuong
        L = 100 * dm / 0.41
        arrow(d, (BX + 52, YQ + 20), (BX + 52, YQ + 20 + max(L, 28)), RED, w=7, head=20)
        text(d, (BX + 80, YQ + 20 + max(L, 28) / 2 + 6), "F", 58, RED, anchor="lm")
    if neu_x is not None:                      # qua cau y het khong mang dien, cam bang thanh cach dien tu trai
        d.rectangle([-20, YQ - 7, max(-20, neu_x - 32), YQ + 7], fill=ROD, outline=NAVY, width=2)
        ball(d, neu_x, YQ, NEU, sign=None)

XS = (160, 365, 575, 860)
def table(d, n, e=0, y=1050, hl=()):
    """Bang r - q - dm - E; n hang da co; e = so hang da hien cot E (con lai '?')."""
    card(d, (40, y, 1040, y + 500), fill=WHITE, outline=NAVY, w=4)
    for x, c in zip(XS, ("r (cm)", "q (nC)", "Δm (g)", "E (×10⁵ V/m)")): text(d, (x, y + 52), c, 56, NAVY)
    d.line([(70, y + 95), (1010, y + 95)], fill=LIGHT, width=4)
    for i in range(n):
        yy = y + 150 + i * 88; r, q, dm, E = ROWS[i]
        if i in hl: d.rounded_rectangle([60, yy - 40, 1020, yy + 40], radius=18, fill=PEACH)
        text(d, (XS[0], yy), str(r), 58, INK); text(d, (XS[1], yy), str(q), 58, INK)
        text(d, (XS[2], yy), vn(dm), 58, INK)
        text(d, (XS[3], yy), vn(E) if i < e else "?", 58, BLUE if i < e else NAVY)

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, 4, 10, "… g", show_r=True)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1035 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 540), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    for j, s in enumerate(("q: 10 nC → 5 nC,", "giữ r = 4 cm.", "E = F/q sẽ thế nào?")):
        text(d, (W / 2, y0 + 170 + j * 85), s, 62, PURPLE if j == 2 else INK, alpha=a)
    seg_bar(d, y0 + 435, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
STEPS = [(0.4, 3), (2.3, 4), (4.2, 6)]     # Q dat san o 3 cm; moi vi tri: di 0,6 s, so can sau 0,7 s, hang bang sau 1,0 s
def s_do(img, d, t, sc):
    M = sc["M"]; tt = M[1]                     # moc cham qua cau trung hoa
    r, reading, dm, n = 3.0, "0,00 g", None, 0
    for i, (ts, rr) in enumerate(STEPS):
        if t >= ts:
            r0 = 3 if i == 0 else STEPS[i - 1][1]
            r = lerp(r0, rr, ease((t - ts) / 0.6))
            if t >= ts + 0.7: reading, dm = vn(ROWS[i][2]) + " g", ROWS[i][2]
            else: reading, dm = "… g", None
            if t >= ts + 1.0: n = i + 1
    q, neu = 10, None
    if t >= tt + 0.2:                          # qua cau trung hoa tien vao cham q roi lui ra
        u = t - tt - 0.2
        nx = lerp(-60, BX - 68, ease(u / 0.6)) if u < 1.3 else lerp(BX - 68, -60, ease((u - 1.3) / 0.6))
        if u < 2.0: neu = nx
        if u >= 0.65: q = 5
    if t >= tt + 2.2:                          # ha Q tu 6 cm xuong 4 cm
        r = lerp(6, 4, ease((t - tt - 2.2) / 0.6))
        reading, dm = ("… g", None) if t < tt + 2.9 else (vn(ROWS[3][2]) + " g", ROWS[3][2])
        if t >= tt + 3.2: n = 4
    elif t >= tt:
        reading, dm = "… g", None
    settled = abs(r - round(r)) < 0.02 and round(r) in (3, 4, 6)
    rig(d, round(r) if settled else r, q, reading, dm, show_r=settled, neu_x=neu)
    table(d, n)

# ---------------- canh 3: Ket qua + rut ra ----------------
BASE_Y, BAR_H = 880, 380
def bars(d, groups, t0, t, legend):
    card(d, (40, 340, 1040, 1010), fill=WHITE, outline=LIGHT, w=3)
    for x, col, s in legend:
        d.rounded_rectangle([x, 372, x + 40, 412], radius=8, fill=col)
        text(d, (x + 56, 392), s, 56, INK, anchor="lm")
    d.line([(90, BASE_Y), (990, BASE_Y)], fill=NAVY, width=4)
    for gi, (cx, name, vals, top) in enumerate(groups):
        if name: text(d, (cx, BASE_Y + 55), name, 56, NAVY)
        for j, (v, col) in enumerate(vals):
            k = appear(t, t0 + 0.3 * gi + 0.15 * j, 0.5)
            if k <= 0: continue
            h = BAR_H * v / top * k; x0 = cx - 130 + j * 145
            d.rectangle([x0, BASE_Y - h, x0 + 115, BASE_Y], fill=col)
            if k >= 1: text(d, (x0 + 58, BASE_Y - h - 34), vn(v), 56, INK)

def s_dapan(img, d, t, sc):
    M = sc["M"]
    pill(d, "ĐÁP ÁN: gần như không đổi", 290, 1.0)
    k2 = appear(t, M[1] - 0.1, 0.4)
    if k2 < 1:                                  # q = 10 vs 5 nC o r = 4 cm
        bars(d, ((300, "Δm (g)", ((ROWS[1][2], BLUE), (ROWS[3][2], ORANGE)), 0.30),
                 (760, "E (×10⁵ V/m)", ((ROWS[1][3], BLUE), (ROWS[3][3], ORANGE)), 3.0)), 0.3, t,
             ((130, BLUE, "q = 10 nC"), (580, ORANGE, "q = 5 nC")))
        kn = appear(t, 2.4, 0.4)
        if kn > 0:
            text(d, (300, 470), "÷ 2", 64, DORANGE, alpha=kn)
            text(d, (760, 470), "≈ bằng nhau", 60, DORANGE, alpha=kn)
    else:                                       # E theo r: 3 cm vs 6 cm (q = 10 nC)
        bars(d, ((530, "", ((ROWS[0][3], BLUE), (ROWS[2][3], PURPLE)), 4.5),), M[1] + 0.2, t,
             ((130, BLUE, "r = 3 cm"), (580, PURPLE, "r = 6 cm")))
        text(d, (830, 620), "E (×10⁵ V/m)", 56, NAVY)
        kp = appear(t, M[1] + 2.4, 0.4)
        if kp > 0:
            card(d, (730, 690, 930, 790), fill=A(ORANGE, kp), r=30)
            text(d, (830, 740), "≈ ÷ 4", 60, WHITE, alpha=kp)
    table(d, 4, e=4, hl=(1, 3) if t < M[1] - 0.1 else (0, 2))

# ---------------- canh 4: Bay (thanh sai so chong nhau) roi Chua noi duoc ----------------
EB = ((ROWS[1][3], 0.01 / ROWS[1][2], BLUE, "q = 10 nC"), (ROWS[3][3], 0.01 / ROWS[3][2], ORANGE, "q = 5 nC"))
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    card(d, (40, 240, 1040, 1010), fill=WHITE, outline=DRED, w=6)
    pill(d, "BẪY", 305, 1.0, DRED)
    q = "“Khác nhau: E phụ thuộc q”"
    ks = clamp((t - 0.3) / 0.4); f = F(60); lw = tw(d, q, f); yy = 410
    text(d, (W / 2, yy), q, 60, mix(DRED, GRAY, ks))
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=DRED, width=6)
    base, top, Hh = 850, 3.0, 300                   # hai cot E (x10^5 V/m) + thanh sai so doc can
    d.line([(120, base), (960, base)], fill=NAVY, width=4)
    ke = appear(t, 3.0, 0.45)
    for j, (E, rel, col, lab) in enumerate(EB):
        cx = 330 + j * 420; h = Hh * E / top
        d.rectangle([cx - 70, base - h, cx + 70, base], fill=col)
        text(d, (cx, base + 45), lab, 56, INK)
        if ke > 0:
            dh = Hh * E * rel / top
            for yv in (base - h - dh, base - h + dh): d.line([(cx - 40, yv), (cx + 40, yv)], fill=A(NAVY, ke), width=6)
            d.line([(cx, base - h - dh), (cx, base - h + dh)], fill=A(NAVY, ke), width=6)
        text(d, (cx + 130, base - h + 10), vn(E), 56, INK)
    text(d, (W / 2, base + 115), "E (×10⁵ V/m)", 56, NAVY)
    if ke > 0:
        d.rectangle([180, base - Hh * EB[1][0] * (1 + EB[1][1]) / top, 900, base - Hh * EB[0][0] * (1 - EB[0][1]) / top],
                    fill=A(GREEN, 0.18 * ke))
        text(d, (W / 2, 520), "✓ lệch trong sai số cân", 58, DGREEN, alpha=ke)
    if k2 > 0:
        y0 = 1050 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 500), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        pill(d, "CHƯA NÓI ĐƯỢC", y0 + 70, k2, NAVY)
        text(d, (W / 2, y0 + 210), "Đổi Q thì E ra sao?", 62, INK, alpha=k2)
        text(d, (W / 2, y0 + 340), "r quá nhỏ thì sao?", 62, INK, alpha=k2)

# ---------------- canh 5: THU NGHI (cau chot o khung: q = -10 nC -> can giam 0,23 g) ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1570), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, "THỬ NGHĨ", 305, k, ORANGE)
    text(d, (W / 2, 470), "Đổi q thành −10 nC,", 62, INK, alpha=k)
    text(d, (W / 2, 570), "vẫn r = 4 cm.", 62, INK, alpha=k)
    text(d, (W / 2, 690), "Cân thay đổi ra sao?", 64, DORANGE, alpha=k)
    seg_bar(d, 820, t, 1.0, sc["T"] - 0.2, ORANGE, k)
    kh = appear(t, M[0] + 3.0, 0.5)
    if kh > 0:
        card(d, (90, 1000, 990, 1140), fill=A(PEACH, kh), outline=A(ORANGE, kh), r=24, w=4)
        text(d, (W / 2, 1070), "Gợi ý: lực điện giờ hướng nào?", 58, DORANGE, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    out += [(do["t0"] + ts, "tick") for ts, _ in STEPS]
    out += [(do["t0"] + do["M"][1] + 0.2, "tap"),
            (da["t0"] + 0.1, "ding"), (b["t0"] + 1.4, "buzz"), (e["t0"] + 0.15, "open")]
    return out

CLIP = dict(id="tn-l11-dien-truong-02", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Khái niệm điện trường · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Cân điện tử đo lực điện", draw=s_hook, tail=0.3, caps=[
   ("Q đẩy q xuống, số chỉ cân tăng.", 3.4),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Đổi r, ghi số cân tăng thêm.", 5.4),
   ("Chạm cầu trung hoà: q còn một nửa.", 4.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Lực giảm theo q, nên E giữ nguyên.", 4.2),
   ("Còn r gấp đôi thì E giảm khoảng 4 lần.", 4.6)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.4, caps=[
   ("Bẫy thường gặp.", 5.8),
   ("Q luôn là 40 nC.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng lại, tự trả lời.", 7.4)]),
])
