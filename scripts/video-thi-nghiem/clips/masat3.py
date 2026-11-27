# Clip: tn-l10-luc-ma-sat-03 - Nang dan tam van: do cao luc hop bat dau truot va luc truot deu (ban 2 cong moi, 27/11/2026)
# So lieu tu content/thi-nghiem/tn-l10-luc-ma-sat-03.json (_kiem_so()): van L = 1,00 m ; bat dau truot h 0,34 m ;
#   truot deu h 0,29 m ; hang "them gia trong" 0,34 m SUY TU MO HINH (ghi "theo mô hình" tren man).
# Du doan (K10, khong nut): nang dan toi luc hop bat dau truot ; ha bot, bung nhe cho truot deu -> h luc truot deu so voi
#   luc bat dau truot? (dap an: thap hon).
# KHONG tra loi san: muc 4 cua bai bat HS tinh sin = h/L, alpha, mu_n = tan, mu -> clip KHONG hien goc, tan, mu.
#   Cau 3 (tu yen: ma sat = luc day), Cau 4 (sach tren doc 30 do) -> clip khong tinh luc nao bang so.
# Bay = hien_tuong_hay_sai[0] "hop nang hon truot o doc thoai hon" -> hai van canh nhau, cung 0,34 m (theo mo hinh).
# Chua noi duoc: nang cao hon 0,34 m thi hop nhanh dan ra sao.
# Chot (ghi_chu kho): hop 0,20 kg nam yen tren van h = 0,20 m -> ma sat nghi = P_x = m.g.h/L = 0,39 N
#   (khong phai mu_n.N ~ 0,69 N). So 0,20 m / 0,39 N chua hien. Khong goi y.
import math
from engine import *

L_M = 1.00
H_N, H_D = 0.34, 0.29
def vn(x, nd=2): return f"{x:.{nd}f}".replace(".", ",")
def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-luc-ma-sat-03.json")))
    hang = k["so_lieu_mau"]["hang"]
    assert (hang[0][1], hang[1][1]) == (H_N, H_D) and hang[2][1] == H_N and "gia trọng" in hang[2][0]
    assert round(0.20 * 9.8 * 0.20 / L_M, 2) == 0.39
_kiem_so()

WOOD = (176, 124, 74); WOOD_D = (140, 96, 54); BOX = (232, 196, 140); BOX_D = (150, 104, 56)
BOARD = (196, 150, 98); RULER = (254, 243, 199); DGREEN = (21, 110, 55); DRED = (185, 28, 28); NOTE = (60, 64, 84)
WT = (120, 126, 140); EMPTY = (148, 140, 128); DORANGE = (176, 64, 8)

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0, x0=175, step=150, w=130):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = x0 + i * step
        if i < on: card(d, (x, y, x + w, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + w, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

# ---------------- van nghieng (ban le o (ox, oy), lpx px / m) ----------------
UMIN = 0.15
def ramp(d, ox, oy, lpx, h, u=None, a_box=1.0, n_wt=0, flick=0.0, a=1.0, bh=None):
    sa = h / L_M; ca = math.sqrt(1 - sa * sa)
    P = lambda uu, n=0.0: (ox + uu * lpx * ca - n * sa, oy - uu * lpx * sa - n * ca)
    e = P(L_M)
    d.line([(e[0], e[1] + 8), (e[0], oy)], fill=A(NAVY, a), width=8)                       # thanh do dau van
    poly = [P(0), P(L_M), P(L_M, -16), P(0, -16)]
    d.polygon(poly, fill=A(BOARD, a)); d.line([P(0), P(L_M)], fill=A(WOOD_D, a), width=4)
    d.polygon([P(0.04), P(0.06), P(0.06, 0.05 * lpx), P(0.04, 0.05 * lpx)], fill=A(WOOD_D, a))   # chan
    if u is not None and a_box > 0.02:
        BH = bh or 0.09 * lpx; ab = a_box * a
        for j in range(n_wt):
            w = [P(u - 0.05, BH + j * 0.055 * lpx), P(u + 0.05, BH + j * 0.055 * lpx),
                 P(u + 0.05, BH + (j + 1) * 0.055 * lpx - 4), P(u - 0.05, BH + (j + 1) * 0.055 * lpx - 4)]
            d.polygon(w, fill=A(WT, ab)); d.line(w + [w[0]], fill=A(NAVY, ab), width=3)
        q = [P(u - 0.08), P(u + 0.08), P(u + 0.08, BH), P(u - 0.08, BH)]
        d.polygon(q, fill=A(BOX, ab)); d.line(q + [q[0]], fill=A(BOX_D, ab), width=4)
        if flick > 0:
            p0 = P(u + 0.10, BH / 2); p1 = P(u + 0.10 + 0.14 * flick, BH / 2)
            arrow(d, p1, p0, A(PURPLE, ab), w=7, head=20)
    return e

# khung chinh
OX, OY, LPX = 70, 840, 760
RX = 870
def ruler(d):
    d.rectangle([RX - 14, OY - 0.42 * LPX, RX + 14, OY], fill=RULER, outline=NAVY, width=3)
    for k in range(0, 9):
        y = OY - k * 0.05 * LPX; L = 20 if k % 2 == 0 else 10
        d.line([(RX - 14, y), (RX - 14 + L, y)], fill=NAVY, width=3)
        if k % 2 == 0 and k > 0: text(d, (RX + 26, y), vn(k * 0.05, 1), 55, INK, anchor="lm")
    text(d, (RX + 26, OY - 0.42 * LPX - 46), "m", 55, INK, anchor="lm")

def scene_rig(d, h, u, a_box=1.0, flick=0.0, n_wt=0):
    card(d, (40, 270, 1040, 900), fill=WHITE, outline=LIGHT, w=3)
    d.rectangle([40, OY, 1040, OY + 30], fill=WOOD)
    ruler(d)
    e = ramp(d, OX, OY, LPX, h, u, a_box=a_box, flick=flick, n_wt=n_wt)
    for xx in range(int(e[0]) + 6, RX - 14, 22): d.line([(xx, e[1]), (min(xx + 12, RX - 14), e[1])], fill=ORANGE, width=4)
    text(d, (e[0] - 20, (e[1] + OY) / 2 + 10), "h", 62, ORANGE, anchor="rm")

def h_note(d, y):
    text(d, (W / 2, y), "h: độ cao đầu ván dài 1,00 m", 55, NOTE)

# ---------------- canh 1: Du doan ----------------
H_HOOK = 0.10; U0 = 0.72
def s_hook(img, d, t, sc):
    M = sc["M"]
    scene_rig(d, H_HOOK, U0)
    h_note(d, 960)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 900 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 660), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    for j, s1 in enumerate(("Lúc hộp trượt đều,", "h so với lúc hộp", "bắt đầu trượt?")):
        text(d, (W / 2, y0 + 200 + j * 95), s1, 62, PURPLE if j == 2 else INK, alpha=a)
    seg_bar(d, y0 + 520, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh ----------------
def do_state(t, M):
    """-> (h, u, a_box, flick, so dong bang)."""
    t1, t2, t3 = M[1], M[2], M[3]
    if t < t1:                                       # nang dan, hop yen
        h = lerp(H_HOOK, H_N, ease(clamp((t - M[0]) / (t1 - M[0] - 0.1)))); return h, U0, 1.0, 0.0, 0
    if t < t2:                                       # bat dau truot: nhanh dan xuong chan
        s = clamp((t - t1) / 1.6) ** 2; return H_N, lerp(U0, UMIN, s), 1.0, 0.0, 1
    if t < t2 + 1.2:                                 # ha van, hop dat lai dau
        k = ease((t - t2) / 1.2); return lerp(H_N, H_D, k), U0, k, 0.0, 1
    if t < t3 - 1.0:                                 # bung
        k = clamp((t - t2 - 1.2) / 0.5); return H_D, U0, 1.0, 1.0 - abs(1 - 2 * k), 1
    s = clamp((t - (t3 - 1.0)) / 3.6)                # truot deu (toc do khong doi)
    return H_D, lerp(U0, UMIN, s), 1.0, 0.0, 2 if t >= t3 else 1

TX = (330, 820)
def table(d, rows, hl=-1, y=930):
    card(d, (40, y, 1040, y + 330), fill=WHITE, outline=NAVY, w=4)
    text(d, (TX[0], y + 55), "Hộp", 55, INK); text(d, (TX[1], y + 55), "h (m)", 55, ORANGE)
    d.line([(60, y + 100), (1020, y + 100)], fill=LIGHT, width=4)
    for i, (lab, hv) in enumerate((("bắt đầu trượt", H_N), ("trượt đều", H_D))):
        yy = y + 160 + i * 100
        if i == hl: d.rounded_rectangle([60, yy - 42, 1020, yy + 42], radius=18, fill=(220, 252, 231))
        if i < rows:
            text(d, (TX[0], yy), lab, 58, INK); text(d, (TX[1], yy), vn(hv), 60, DORANGE)

def s_do(img, d, t, sc):
    M = sc["M"]; h, u, ab, fl, rows = do_state(t, M)
    scene_rig(d, h, u, a_box=ab, flick=fl)
    text(d, (90, 320), "h = " + vn(h) + " m", 58, DORANGE, anchor="lm")
    kr = appear(t, M[4], 0.45)
    table(d, rows, hl=1 if kr > 0.5 else -1)
    h_note(d, 1310)
    if kr > 0:
        y0 = 1270 + (1 - kr) * 20
        card(d, (40, y0, 1040, y0 + 290), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
        pill(d, W / 2, y0 + 60, "RÚT RA", GREEN, kr)
        text(d, (W / 2, y0 + 160), "Trượt đều: dốc thoải hơn.", 58, DGREEN, alpha=kr)
        text(d, (W / 2, y0 + 240), "Ma sát trượt < nghỉ cực đại.", 58, DGREEN, alpha=kr)

def _kiem_dong_bo():
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; M = sc["M"]; bad = []; t = 0.0
    while t < sc["T"]:
        h, u, ab, fl, rows = do_state(t, M)
        if rows >= 1 and t >= M[1] and abs(h - H_N) > 1e-9 and t < M[2]: bad.append((round(t, 2), "h dong 1"))
        if rows == 2 and abs(h - H_D) > 1e-9: bad.append((round(t, 2), "h dong 2"))
        if u < UMIN - 1e-9: bad.append((round(t, 2), "hop qua chan"))
        t += 0.05
    if abs(do_state(M[1] - 0.15, M)[0] - H_N) > 0.005: bad.append("chua toi 0,34 luc bat dau truot")
    if M[3] - 1.0 < M[2] + 1.7: bad.append("bung chong ha van")
    return bad

# ---------------- canh 3: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[2] - 0.1, 0.45); a1 = 1 - k3
    kv = appear(t, M[1], 0.4)
    card(d, (40, 860, 1040, 1560), fill=WHITE, outline=LIGHT, w=3)
    for cx, n, lab in ((70, 0, "hộp"), (570, 2, "hộp + gia trọng")):
        d.rectangle([cx - 20, 1330, cx + 450, 1350], fill=WOOD)
        e = ramp(d, cx, 1330, 400, H_N, 0.62, n_wt=n)
        text(d, (cx + 210, 1420), lab, 55, INK)
        if kv > 0:
            d.line([(e[0] + 22, e[1]), (e[0] + 22, 1330)], fill=A(ORANGE, kv), width=5)
            text(d, (e[0] - 10, e[1] - 50), "0,34 m", 55, DORANGE, alpha=kv)
    if kv > 0: text(d, (W / 2, 1500), "(theo mô hình)", 55, NOTE, alpha=kv)
    if a1 > 0:
        card(d, (40, 280, 1040, 800), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, W / 2, 350, "BẪY", DRED, a1)
        ks = clamp((t - M[0] - 1.2) / 0.4)
        for j, q in enumerate(("“Hộp nặng hơn trượt", "ở dốc thoải hơn”")):
            f = F(58); lw = tw(d, q, f); yy = 480 + j * 85
            text(d, (W / 2, yy), q, 58, mix(RED, GRAY, ks), alpha=a1)
            if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        if kv > 0: text(d, (W / 2, 710), "Cùng 0,34 m", 56, DGREEN, alpha=kv * a1)
    if k3 > 0:
        card(d, (40, 280, 1040, 800), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 350, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 500), "Dốc cao hơn:", 58, INK, alpha=k3)
        text(d, (W / 2, 590), "hộp nhanh dần ra sao?", 58, INK, alpha=k3)

# ---------------- canh 4: Thu nghi ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 300, 1040, 1400), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 375, "THỬ NGHĨ", ORANGE, k)
    oy = 880
    d.rectangle([80, oy, 1000, oy + 20], fill=A(WOOD, k))
    e = ramp(d, 110, oy, 700, 0.20, 0.55, a=k, bh=64)
    d.line([(e[0] + 24, e[1]), (e[0] + 24, oy)], fill=A(ORANGE, k), width=5)
    text(d, (e[0] + 40, (e[1] + oy) / 2), "0,20 m", 55, DORANGE, anchor="lm", alpha=k)
    sa = 0.20; ca = math.sqrt(1 - sa * sa); bx = 110 + 0.55 * 700 * ca; by = oy - 0.55 * 700 * sa
    text(d, (bx - 10, by - 130), "0,20 kg, nằm yên", 55, INK, anchor="mm", alpha=k)
    text(d, (420, oy + 70), "ván dài 1,00 m", 55, NOTE, alpha=k)
    text(d, (W / 2, 1060), "Ma sát ván tác dụng", 60, INK, alpha=k)
    text(d, (W / 2, 1150), "lên hộp bao nhiêu N?", 60, DORANGE, alpha=k)
    seg_bar(d, 1260, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, b, e = sc["hook"], sc["do"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding"), (do["t0"] + do["M"][1], "tap"),
             (do["t0"] + do["M"][3] - 0.85, "tap"), (do["t0"] + do["M"][4], "ding"), (b["t0"] + b["M"][0] + 1.2, "buzz"),
             (b["t0"] + b["M"][2] - 0.1, "tap"), (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l10-luc-ma-sat-03", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Lực ma sát · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Nâng dần tấm ván", draw=s_hook, tail=0.2, caps=[
   ("Hộp gỗ nằm yên trên ván.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Đo độ cao h", draw=s_do, tail=0.4, caps=[
   ("Nâng dần đầu ván.", 3.2),
   ("Hộp bắt đầu trượt.", 3.4),
   ("Hạ bớt, búng nhẹ hộp.", 3.4),
   ("Hộp trượt đều.", 3.2),
   ("Đáp án: h thấp hơn.", 3.8)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.4, caps=[
   ("Đúng không?", 3.6),
   ("Thêm gia trọng.", 3.6),
   ("Chưa nói được.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 6.4)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
