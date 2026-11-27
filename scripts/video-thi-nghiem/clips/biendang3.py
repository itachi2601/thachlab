# Clip: tn-l10-biendang-03 - Hai lo xo, cung mot qua nang (ban 2 cong moi, 27/11/2026)
# So lieu tu content/thi-nghiem/tn-l10-biendang-03.json:
#   so_lieu_mau: day to k = 50 N/m, dl = 1,96 cm ; day manh k = 25 N/m, dl = 3,92 cm (qua 100 g, g = 9,8 -> P = 0,98 N)
#   tham_so: F 0-3 N. Hinh ve dung ti le: 90 px moi cm, vach 0 thuoc ngang dau duoi luc chua treo -> so doc = dl.
# Du doan (K10, khong nut A-D): cung qua 100 g, lo xo nao dan nhieu hon? (dap an: day manh).
# Bay = "dan nhieu hon thi bi keo manh hon" (khong lap cap so 1,96/3,92: ngoac khong ghi so, chi mui ten 0,98 N).
# Chot (tu suy, trong thang F <= 3 N, khong trung bai: bai co k=200/3 cm, 3 N/6 cm, 2 N/4 cm, k=100, k=80):
#   cung mot vat, day manh dan 5,0 cm -> F = 25 . 0,05 = 1,25 N -> day to dan 1,25 : 50 = 0,025 m = 2,5 cm.
#   1,25 va 2,5 khong hien tren man.
from engine import *
from PIL import ImageFont as _IF

DL = (1.96, 3.92)
NAME = ("dây to", "dây mảnh")
COIL = ((8, 30, 10), (13, 22, 4))                # (so vong, bien do, net): day to it vong net day
NOTE = (60, 64, 84); BRASS = (196, 150, 70); BRASS_D = (140, 100, 40); RULER = (255, 241, 205)
DORANGE = (176, 64, 8); EMPTY = (148, 140, 128); BAR = (150, 155, 172)
def vn(x, n=2): return f"{x:.{n}f}".replace(".", ",")

_FL = {}
def FL(size):
    if size not in _FL: _FL[size] = _IF.truetype("/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf", size)
    return _FL[size]

def seq(d, x, y, parts, alpha=1.0, anchor="m"):
    fs = [FL(z) if it else F(z) for _, z, _, it in parts]
    ws = [tw(d, s_, f) + (6 if it else 0) for (s_, _, _, it), f in zip(parts, fs)]
    x -= sum(ws) / 2 if anchor == "m" else (sum(ws) if anchor == "r" else 0)
    for (s_, z, c, it), f, w in zip(parts, fs, ws):
        dtext(d, (x, y), s_, f, c, alpha, anchor="lm"); x += w

def lab_l(d, x, y, pre, post, size, col, alpha=1.0, anchor="m"):
    seq(d, x, y, [(pre, size, col, False), ("l", size + 2, col, True), (post, size, col, False)], alpha, anchor)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 175 + i * 150
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- gia treo, hai lo xo, hai thuoc ----------------
SX = (140, 420)                                  # truc hai lo xo
RX = (225, 515)                                  # mep trai hai thuoc
TOP, Y0N, PX = 400, 630, 90                      # moc tren ; dau duoi luc chua treo ; px moi cm
MW, MH = 150, 84
BASE = 1150
FREE_X, FREE_Y = 820, BASE - 18 - MH - 4

def spring(d, x, top, yb, i, a=1.0):
    lead = 24; n, amp, w = COIL[i]
    pts = [(x, top), (x, top + lead)]
    for j in range(1, 2 * n):
        pts.append((x + (amp if j % 2 else -amp), lerp(top + lead, yb - lead, j / (2 * n))))
    pts += [(x, yb - lead), (x, yb)]
    d.line(pts, fill=A(NAVY, a), width=w, joint="curve")
    d.ellipse([x - 9, yb - 4, x + 9, yb + 14], outline=A(NAVY, a), width=4)

def mass(d, cx, ytop, a=1.0):
    d.arc([cx - 13, ytop, cx + 13, ytop + 24], 180, 360, fill=A(NAVY, a), width=5)
    d.line([(cx, ytop + 10), (cx, ytop + 20)], fill=A(NAVY, a), width=5)
    d.rounded_rectangle([cx - MW / 2, ytop + 18, cx + MW / 2, ytop + 18 + MH], radius=12,
                        fill=A(BRASS, a), outline=A(BRASS_D, a), width=3)
    text(d, (cx, ytop + 18 + MH / 2), "100 g", 55, WHITE, alpha=a)

def ruler(d, rx, dl):
    d.rectangle([rx, Y0N - 20, rx + 44, Y0N + 4 * PX + 20], fill=RULER, outline=BRASS_D, width=3)
    for k in range(41):
        y = Y0N + k * PX / 10; L = 26 if k % 10 == 0 else (17 if k % 5 == 0 else 9)
        d.line([(rx, y), (rx + L, y)], fill=NAVY, width=3 if k % 10 == 0 else 2)
    for c in range(5): text(d, (rx + 56, Y0N + c * PX), str(c), 56, INK, anchor="lm")
    text(d, (rx + 75, Y0N - 62), "cm", 55, INK)
    y = Y0N + dl * PX                            # kim: ngang dau duoi lo xo
    d.line([(rx - 34, y), (rx + 30, y)], fill=RED, width=5)
    d.polygon([(rx + 2, y), (rx - 16, y - 9), (rx - 16, y + 9)], fill=RED)

def rig(d, dls, hung=(), free=None):
    d.rounded_rectangle([40, TOP - 30, 600, TOP], radius=8, fill=BAR)
    d.rounded_rectangle([14, BASE, 1060, BASE + 36], radius=10, fill=(176, 124, 74))
    for xx in range(60, 600, 30): d.line([(xx, Y0N), (xx + 16, Y0N)], fill=GRAY, width=3)
    for i in (0, 1):
        text(d, (SX[i] + 40, 335), NAME[i], 56, INK)
        ruler(d, RX[i], dls[i])
        yb = Y0N + dls[i] * PX
        spring(d, SX[i], TOP, yb, i)
        if i in hung: mass(d, SX[i], yb + 4)
    if free: mass(d, free[0], free[1])

def osc(D, tt):  return D * (1 - math.exp(-6.0 * tt) * math.cos(2 * math.pi * 1.4 * tt))
def back0(D, tt): return D * math.exp(-4.0 * tt) * math.cos(2 * math.pi * 1.4 * tt)
HANG, SETTLE, MOVE = 0.7, 1.6, 1.0

def state(t, a1, a2):
    """-> (dl, hung, free, doc). a1: bat dau dua qua len lo xo 1 ; a2: bat dau chuyen sang lo xo 2."""
    dl, hung, fr, doc = [0.0, 0.0], (), None, {}
    if t < a1: fr = (FREE_X, FREE_Y)
    elif t < a1 + HANG:
        k = ease((t - a1) / HANG); fr = (lerp(FREE_X, SX[0], k), lerp(FREE_Y, Y0N + 4, k) - 120 * math.sin(math.pi * k))
    elif t < a2:
        tt = t - a1 - HANG; dl[0] = osc(DL[0], tt); hung = (0,)
        if tt > SETTLE: dl[0] = DL[0]; doc[0] = DL[0]
    elif t < a2 + MOVE:
        tau = t - a2; k = ease(tau / MOVE); dl[0] = back0(DL[0], tau); doc[0] = DL[0]
        fr = (lerp(SX[0], SX[1], k), lerp(Y0N + DL[0] * PX + 4, Y0N + 4, k) - 110 * math.sin(math.pi * k))
    else:
        tau = t - a2; dl[0] = back0(DL[0], tau); tt = tau - MOVE; doc[0] = DL[0]
        dl[1] = osc(DL[1], tt); hung = (1,)
        if tt > SETTLE: dl[1] = DL[1]; doc[1] = DL[1]
    if abs(dl[0]) < 0.004: dl[0] = 0.0
    return dl, hung, fr, doc

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    rig(d, (0.0, 0.0), free=(FREE_X, FREE_Y))
    text(d, (FREE_X, 985), "Chưa treo", 58, NOTE)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1210 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 450), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 60, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 170), "Treo quả 100 g lần lượt.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 255), "Lò xo nào dãn nhiều hơn?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 340, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: tien hanh ----------------
DA1, DA2 = 0.4, 4.9
def t_dapan(): return DA2 + MOVE + SETTLE + 0.6

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    dl, hung, fr, doc = state(t, DA1, DA2)
    rig(d, dl, hung, fr)
    card(d, (620, 290, 1045, 660), fill=WHITE, outline=NAVY, w=4)
    lab_l(d, 840, 350, "Δ", " (cm)", 56, NOTE)
    d.line([(640, 390), (1025, 390)], fill=LIGHT, width=4)
    for i in (0, 1):
        y = 460 + i * 120
        text(d, (752, y), NAME[i], 55, INK)
        if i in doc: text(d, (972, y), vn(doc[i]), 60, RED)
    k = appear(t, t_dapan(), 0.4)
    if k > 0:
        card(d, (640, 700, 1040, 900), fill=A(NAVY, k), r=30)
        text(d, (840, 760), "Dây mảnh dãn", 58, WHITE, alpha=k)
        text(d, (840, 840), "gấp đôi dây to", 58, (253, 224, 71), alpha=k)

def _kiem_dong_bo():
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; bad = []; t = 0.0
    while t < sc["T"]:
        dl, hung, fr, doc = state(t, DA1, DA2)
        for i, v in doc.items():
            if i in hung and abs(dl[i] - v) > 1e-9: bad.append(("lech", i, round(t, 2)))
        for i in (0, 1):
            if i in hung and Y0N + dl[i] * PX + 4 + 18 + MH > BASE - 4: bad.append(("cham de", round(t, 2)))
        t += 0.05
    if t_dapan() + 2.2 > sc["T"]: bad.append("dap an sat cuoi")
    return bad

# ---------------- canh 3: rut ra ----------------
def s_rut(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    a = appear(t, 0.2)
    cx, ytop, ybot = 240, 520, 630
    d.rounded_rectangle([cx - 100, ytop, cx + 100, ybot], radius=16, fill=A(BRASS, a), outline=A(BRASS_D, a), width=4)
    text(d, (cx, (ytop + ybot) / 2), "100 g", 58, WHITE, alpha=a)
    ka = appear(t, 0.6, 0.4)
    if ka > 0:
        L = 170
        arrow(d, (cx, ytop), (cx, ytop - L), A(GREEN, ka), w=9, head=28)
        arrow(d, (cx, ybot), (cx, ybot + L), A(RED, ka), w=9, head=28)
        dot(d, cx, ytop, 9, A(GREEN, ka)); dot(d, cx, ybot, 9, A(RED, ka))
        text(d, (cx + 40, ytop - 120), "F", 64, GREEN, anchor="lm", alpha=ka)
        text(d, (cx + 40, ybot + 120), "P", 64, RED, anchor="lm", alpha=ka)
        text(d, (700, 440), "F: lực lò xo", 58, GREEN, alpha=ka)
        text(d, (700, 520), "P: trọng lực", 58, RED, alpha=ka)
        text(d, (700, 620), "F = P = 0,98 N", 62, INK, alpha=ka)
    kb = appear(t, M[1] - 0.1, 0.4)
    if kb > 0:
        card(d, (40, 900, 1040, 1530), fill=A(WHITE, kb), outline=A(NAVY, kb), w=4)
        lab_l(d, W / 2, 990, "k = F : Δ", "", 64, BLUE, kb)
        for i, kk in enumerate((50, 25)):
            y = 1110 + i * 120
            text(d, (300, y), NAME[i], 60, INK, alpha=kb)
            text(d, (720, y), f"{kk} N/m", 64, RED, alpha=kb)
        kc = appear(t, M[1] + 2.6, 0.4)
        if kc > 0: text(d, (W / 2, 1450), "Cùng lực, k khác nhau", 58, NAVY, alpha=kc)

# ---------------- canh 4: bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img; M = sc["M"]
    k0 = appear(t, 0.2, 0.4); k3 = appear(t, M[2] - 0.1, 0.45); a1 = k0 * (1 - k3)
    if a1 > 0:
        card(d, (40, 290, 1040, 520), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pill(d, W / 2, 355, "BẪY", RED, a1)
        q = "“Dãn nhiều: bị kéo mạnh”"
        ks = clamp((t - M[1]) / 0.4); f = F(60); lw = tw(d, q, f); yy = 455
        text(d, (W / 2, yy), q, 60, mix(RED, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
        BT, BN, BP = 640, 820, 70                # moc ; dau duoi luc chua treo ; px moi cm
        ok = appear(t, M[1], 0.4) * a1
        for i in (0, 1):
            x = (300, 760)[i]; yb = BN + DL[i] * BP
            text(d, (x, 585), NAME[i], 56, INK, alpha=a1)
            d.rounded_rectangle([x - 80, BT - 22, x + 80, BT], radius=6, fill=A(BAR, a1))
            spring(d, x, BT, yb, i, a1); mass(d, x, yb + 4, a1)
            for xx in range(x - 110, x + 130, 28): d.line([(xx, BN), (xx + 14, BN)], fill=A(GRAY, a1), width=3)
            bx = x + 115
            d.line([(bx, BN), (bx, yb)], fill=A(RED, a1), width=5)
            for y in (BN, yb): d.line([(bx - 10, y), (bx + 10, y)], fill=A(RED, a1), width=5)
            lab_l(d, bx + 16, (BN + yb) / 2, "Δ", "", 56, RED, a1, anchor="l")
            if ok > 0:                           # luc lo xo len qua nang: bang nhau
                xa = x - 115; y1 = yb + 4 + 18 + MH / 2
                arrow(d, (xa, y1), (xa, y1 - 170), A(GREEN, ok), w=8, head=24)
                text(d, (x, yb + 4 + 18 + MH + 50), "0,98 N", 55, GREEN, alpha=ok)
        text(d, (530, BN - 42), "chưa treo", 55, NOTE, alpha=a1)
        k2 = appear(t, M[1] + 3.0, 0.45) * a1
        if k2 > 0:
            card(d, (40, 1380, 1040, 1520), fill=A((220, 252, 231), k2), outline=A(GREEN, k2), w=5)
            text(d, (W / 2, 1450), "Cùng lực, khác lò xo", 60, GREEN, alpha=k2)
    if k3 > 0:
        card(d, (40, 290, 1040, 1100), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 360, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 480), "Mới thử một lực.", 60, INK, alpha=k3)
        text(d, (W / 2, 580), "Đổi lực, k có đổi?", 60, INK, alpha=k3)
        x, top = W / 2, 690                      # lo xo day to + qua nang mo, dau ?
        d.rounded_rectangle([x - 80, top - 22, x + 80, top], radius=6, fill=A(BAR, k3))
        spring(d, x, top, top + 200, 0, k3)
        d.rounded_rectangle([x - 70, top + 230, x + 70, top + 310], radius=10, fill=A(BRASS, 0.55 * k3), outline=A(BRASS_D, k3), width=3)
        d.line([(x, top + 210), (x, top + 230)], fill=A(NAVY, k3), width=4)
        text(d, (x, top + 270), "?", 64, WHITE, alpha=k3)

# ---------------- canh 5: thu nghi ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1180), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 305, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 450), "Coi k không đổi.", 60, NOTE, alpha=k)
    text(d, (W / 2, 620), "Vật X: dây mảnh dãn 5,0 cm.", 62, INK, alpha=k)
    text(d, (W / 2, 800), "Dây to dãn bao nhiêu cm?", 64, DORANGE, alpha=k)
    seg_bar(d, 1000, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"),
            (do["t0"] + DA1 + HANG, "tap"), (do["t0"] + DA2 + MOVE, "tap"), (do["t0"] + t_dapan(), "ding"),
            (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + b["M"][1], "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"),
            (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l10-biendang-03", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Biến dạng của vật rắn · thachlab.id.vn", scenes=[
 dict(key="hook", title="Hai lò xo, một quả nặng", draw=s_hook, tail=0.3, caps=[
   ("Hai lò xo dài bằng nhau.", 3.0),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Treo lần lượt, đọc thước", draw=s_do, tail=0.2, caps=[
   ("Vạch 0 ngang đầu dưới lò xo.", 3.8),
   ("Chuyển quả sang lò xo kia.", 3.4),
   ("So hai số đọc.", 2.5)]),
 dict(key="rut", title="Cùng một lực kéo", draw=s_rut, tail=0.6, caps=[
   ("Đứng yên: hai lực cân bằng.", 3.6),
   ("Chia lực cho độ dãn.", 4.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Đúng không?", 3.0),
   ("Cùng một quả 100 g.", 6.1),
   ("Chưa nói được.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự tính.", 6.8)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
