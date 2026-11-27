# Clip: tn-l10-dong-nang-the-nang-02 - Con lac vuong dinh (con lac Galilei) (ban 2 theo cong moi, 27/11/2026)
# So lieu lay tu content/thi-nghiem/tn-l10-dong-nang-the-nang-02.json:
#   tham_so: L = 1,0 m, h0 = 0,20 m, d 0 / 0,5 / 0,7 m; g = 10.  so_lieu_mau: h1 = 0,20 m ca ba; goc ben kia 36,9 / 53,1 /
#   70,5 do (hien 37°, 53°, 71°); goc tha 36,9°.
# Du doan (K10): chua dinh len lai vach 0,20 m; dinh o 0,7 m duoi diem treo -> ben kia qua nang len toi dau? Dap an: dung vach 0,20 m.
# Bay: hien_tuong_hay_sai[0] "vuong dinh thi len cao hon": con lac vuong dinh lac that lien tuc, hai dinh cung cham vach;
#   bong "nghi" cao hon bi gach. Chua noi duoc: dinh qua thap (L - d < h0, day chung) chua xet.
# Cau chot (tu suy): dinh 0,5 m duoi diem treo -> cao 0,50 m so day; dinh ben kia o 0,20 m -> thap hon dinh 0,30 m (KHONG hien).
import copy
from engine import *

G, LM, H0 = 10.0, 1.0, 0.20
DS = [0.0, 0.5, 0.7]
TH0 = math.acos(1 - H0 / LM)
def phimax(dd): return math.acos(1 - H0 / (LM - dd))
ANG = ["37°", "53°", "71°"]
DLAB = ["không", "0,5 m", "0,7 m"]

PX, PY, LPX = 540, 280, 620
YB = PY + LPX                  # 900
YH = YB - H0 * LPX             # 776
RB = 30
BOB = (70, 90, 160); BOB_D = (40, 52, 110); STEEL = (150, 155, 172); NAIL = (90, 90, 100)
EMPTY = (148, 140, 128); DORANGE = (176, 64, 8)
SLOW = 1.3

def ypos(dd): return PY + dd * LPX

def pill(d, cx, cy, s, fill, alpha=1.0, size=58):
    pw = tw(d, s, F(size)) + 60
    card(d, (cx - pw / 2, cy - 40, cx + pw / 2, cy + 40), fill=A(fill, alpha), r=38)
    text(d, (cx, cy), s, size, WHITE, alpha=alpha)

def seg_bar(d, y, t, t0, t1, col, a=1.0, n=6):
    p = clamp((t - t0) / (t1 - t0)); on = n - int(p * n + 1e-9); w = 780 / n
    for i in range(n):
        x = 150 + i * w
        if i < on: card(d, (x, y, x + w - 20, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + w - 20, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

def stand(d):
    d.rounded_rectangle([340, PY - 26, 740, PY], radius=8, fill=STEEL)
    d.polygon([(PX - 18, PY), (PX + 18, PY), (PX, PY + 16)], fill=NAVY)

def nail(d, dd, alpha=1.0, lab=True):
    if dd <= 0 or alpha <= 0: return
    y = ypos(dd)
    d.ellipse([PX - 14, y - 14, PX + 14, y + 14], fill=A(NAIL, alpha), outline=A(NAVY, alpha), width=3)
    if lab: text(d, (PX - 30, y), "đinh", 56, NAIL, anchor="rm", alpha=alpha)

def marks(d, alpha=1.0):
    for y, c in ((YH, ORANGE), (YB, GRAY)):
        for xx in range(110, 1010, 26): d.line([(xx, y), (xx + 14, y)], fill=A(c, alpha), width=4)
    xb = 80
    d.line([(xb, YH + 4), (xb, YB - 4)], fill=A(INK, alpha), width=4)
    for y, s in ((YH, 1), (YB, -1)): d.polygon([(xb, y), (xb - 9, y + s * 14), (xb + 9, y + s * 14)], fill=A(INK, alpha))
    text(d, (50, YB + 55), "0,20 m", 56, ORANGE, anchor="lm", alpha=alpha)

def bob_left(theta): return PX - LPX * math.sin(theta), PY + LPX * math.cos(theta)
def bob_right(phi, dd):
    r = (LM - dd) * LPX; cy = ypos(dd)
    return PX + r * math.sin(phi), cy + r * math.cos(phi)

def draw_pend(d, pos, side, dd, alpha=1.0):
    x, y = pos
    if side == "R" and dd > 0:
        d.line([(PX, PY), (PX, ypos(dd))], fill=A(NAVY, alpha), width=4)
        d.line([(PX, ypos(dd)), (x, y)], fill=A(NAVY, alpha), width=4)
    else: d.line([(PX, PY), (x, y)], fill=A(NAVY, alpha), width=4)
    d.ellipse([x - RB, y - RB, x + RB, y + RB], fill=A(BOB, alpha), outline=A(BOB_D, alpha), width=3)

def ghost(d, pos, color=PURPLE, alpha=1.0):
    x, y = pos
    for k in range(0, 360, 30): d.arc([x - RB, y - RB, x + RB, y + RB], k, k + 18, fill=A(color, alpha), width=5)

APP, HOLD = 0.25, 0.3
def ql(): return math.pi / 2 / math.sqrt(G / LM) * SLOW
def qr(dd): return math.pi / 2 / math.sqrt(G / (LM - dd)) * SLOW
def run_len(dd): return APP + HOLD + ql() + qr(dd) + 0.5
def peak_t(dd): return APP + HOLD + ql() + qr(dd)

def run_state(tau, dd):
    if tau < APP + HOLD: return bob_left(TH0), "L", clamp(tau / APP), False
    s = tau - APP - HOLD
    if s < ql(): return bob_left(TH0 * math.cos(math.pi / 2 * s / ql())), "L", 1.0, False
    s -= ql()
    if s < qr(dd): return bob_right(phimax(dd) * math.sin(math.pi / 2 * s / qr(dd)), dd), "R", 1.0, False
    return bob_right(phimax(dd), dd), "R", 1.0, True

def swing_pos(t, dd):
    """Lac lien tuc (khong can) trai 37° <-> phai phimax(dd), moi nua chu ki theo tam quay tuong ung."""
    per = 2 * (ql() + qr(dd)); s = t % per
    if s < ql(): return bob_left(TH0 * math.cos(math.pi / 2 * s / ql())), "L", 1
    s -= ql()
    if s < qr(dd): return bob_right(phimax(dd) * math.sin(math.pi / 2 * s / qr(dd)), dd), "R", 1
    s -= qr(dd)
    if s < qr(dd): return bob_right(phimax(dd) * math.cos(math.pi / 2 * s / qr(dd)), dd), "R", -1
    s -= qr(dd)
    return bob_left(TH0 * math.sin(math.pi / 2 * s / ql())), "L", -1

# ---------------- canh 1: du doan ----------------
REL0 = 0.4
def s_hook(img, d, t, sc):
    M = sc["M"]; tau = t - REL0
    marks(d); stand(d)
    for yy in range(PY + 20, PY + 220, 24): d.line([(PX, yy), (PX, yy + 12)], fill=GRAY, width=3)
    d.arc([PX - 110, PY - 110, PX + 110, PY + 110], 90, 90 + math.degrees(TH0), fill=INK, width=4)
    text(d, (PX - 175, PY + 120), "37°", 56, INK)
    kq = appear(t, M[1] - 0.2, 0.5)
    if tau < run_len(0.0):
        pos, side, al, ok = run_state(tau, 0.0)
        if ok: ghost(d, pos, BLUE)
        draw_pend(d, pos, side, 0.0, al)
    else:
        nail(d, 0.7, kq)
        draw_pend(d, bob_left(TH0), "L", 0.7, clamp((tau - run_len(0.0)) / 0.3))
    if kq <= 0: return
    y0 = 1100 + (1 - kq) * 30
    card(d, (50, y0, 1030, y0 + 540), fill=A(WHITE, kq), outline=A(PURPLE, kq), w=6)
    pill(d, W / 2, y0 + 62, "DỰ ĐOÁN", PURPLE, kq)
    text(d, (W / 2, y0 + 175), "Đinh ở 0,7 m dưới điểm treo.", 62, INK, alpha=kq)
    text(d, (W / 2, y0 + 265), "Bên kia, quả nặng lên tới đâu?", 62, PURPLE, alpha=kq)
    seg_bar(d, y0 + 380, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, kq)

# ---------------- canh 2: tien hanh + dap an ----------------
T0S = [0.3]
for _dd in DS[:-1]: T0S.append(T0S[-1] + run_len(_dd))
def row_t(j): return T0S[j] + peak_t(DS[j])
def which(t): return max([i for i in range(3) if t >= T0S[i]], default=-1)

def s_do(img, d, t, sc):
    M = sc["M"]; j = which(t)
    marks(d); stand(d)
    for i in range(3):
        if t >= row_t(i):
            a = appear(t, row_t(i), 0.25); p = bob_right(phimax(DS[i]), DS[i])
            ghost(d, p, BLUE, a)
    if j >= 0:
        dd = DS[j]; nail(d, dd)
        pos, side, al, ok = run_state(t - T0S[j], dd)
        draw_pend(d, pos, side, dd, al)
    ka = appear(t, M[1] + 0.1, 0.4); kc = appear(t, M[1] + 2.6, 0.4)
    if ka > 0:
        card(d, (60, 1010, 1020, 1120), fill=A((220, 252, 231), ka), outline=A(GREEN, ka), r=28, w=5)
        text(d, (W / 2, 1065), "Đáp án: lên đúng 0,20 m", 62, GREEN, alpha=ka)
    nr = sum(1 for i in range(3) if t >= row_t(i))
    if nr == 0: return
    card(d, (60, 1150, 1020, 1310 + (nr - 1) * 100 + 60), fill=WHITE, outline=NAVY, w=4)
    xs = (230, 545, 840)
    for x, s in zip(xs, ("đinh", "lên tới", "góc lệch")): text(d, (x, 1205), s, 58, INK)
    d.line([(90, 1250), (990, 1250)], fill=LIGHT, width=4)
    for i in range(3):
        a = appear(t, row_t(i), 0.3); yy = 1315 + i * 100
        if a <= 0: continue
        if kc > 0: d.rounded_rectangle([420, yy - 42, 670, yy + 42], radius=16, fill=A((220, 252, 231), kc))
        text(d, (xs[0], yy), DLAB[i], 58, NAIL if i else INK, alpha=a)
        text(d, (xs[1], yy), "0,20 m", 58, ORANGE, alpha=a); text(d, (xs[2], yy), ANG[i], 58, BLUE, alpha=a)

# ---------------- canh 3: vi sao ----------------
def tv_arrows(d, te, dd, alpha=1.0):
    """T huong ve tam quay hien tai; v lay theo chieu chuyen dong that (sai phan), dai ti le toc do, an o dinh."""
    (x, y), side, _ = swing_pos(te, dd); (x2, y2), _, _ = swing_pos(te + 0.004, dd)
    cx, cy = (PX, ypos(dd)) if side == "R" else (PX, PY)
    L = math.hypot(x - cx, y - cy); ut = ((cx - x) / L, (cy - y) / L)
    sp = math.hypot(x2 - x, y2 - y); vmax = math.sqrt(2 * G * H0) * LPX * 0.004
    arrow(d, (x, y), (x + 150 * ut[0], y + 150 * ut[1]), A(PURPLE, alpha), w=8, head=24)
    if sp < 0.4 * vmax:
        text(d, (x + 90 * ut[0] + 60, y + 90 * ut[1]), "T", 60, PURPLE, alpha=alpha); return
    uv = ((x2 - x) / sp, (y2 - y) / sp); ln = 60 + 120 * min(1, sp / vmax)
    text(d, (x + 100 * ut[0] - 50 * uv[0], y + 100 * ut[1] - 50 * uv[1]), "T", 60, PURPLE, alpha=alpha)
    arrow(d, (x, y), (x + ln * uv[0], y + ln * uv[1]), A(BLUE, alpha), w=8, head=24)
    text(d, (x + (ln + 35) * uv[0], y + (ln + 35) * uv[1] + 10), "v", 60, BLUE, alpha=alpha)
    s = 30
    p1 = (x + s * ut[0], y + s * ut[1]); p3 = (x + s * uv[0], y + s * uv[1]); p2 = (p1[0] + s * uv[0], p1[1] + s * uv[1])
    d.line([p1, p2, p3], fill=A(INK, alpha), width=5)

def s_rut(img, d, t, sc):
    M = sc["M"]; dd = 0.7
    marks(d); stand(d); nail(d, dd, lab=False)
    pos, side, sg = swing_pos(t * 0.75, dd)
    draw_pend(d, pos, side, dd)
    tv_arrows(d, t * 0.75, dd)
    k1 = appear(t, 0.3, 0.4)
    card(d, (50, 270, 400, 440), fill=A(WHITE, k1), outline=A(LIGHT, k1), w=3)
    arrow(d, (75, 315), (140, 315), A(PURPLE, k1), w=8, head=20); text(d, (160, 315), "T lực căng", 56, PURPLE, anchor="lm", alpha=k1)
    arrow(d, (75, 395), (140, 395), A(BLUE, k1), w=8, head=20); text(d, (160, 395), "v vận tốc", 56, BLUE, anchor="lm", alpha=k1)
    card(d, (60, 1010, 1020, 1130), fill=A((243, 238, 255), k1), outline=A(PURPLE, k1), r=28, w=4)
    text(d, (W / 2, 1070), "T vuông góc v: không sinh công", 60, PURPLE, alpha=k1)
    k2 = appear(t, M[1] - 0.1, 0.4)
    if k2 > 0:
        card(d, (60, 1170, 1020, 1290), fill=A(WHITE, k2), outline=A(ORANGE, k2), r=28, w=4)
        text(d, (W / 2, 1230), "Hai đỉnh đều có v = 0", 60, INK, alpha=k2)
    k3 = appear(t, M[1] + 2.5, 0.4)
    if k3 > 0:
        card(d, (60, 1330, 1020, 1450), fill=A((236, 253, 243), k3), outline=A(GREEN, k3), r=28, w=5)
        text(d, (W / 2, 1390), "Công trọng lực: xuống = lên", 60, GREEN, alpha=k3)

# ---------------- canh 4: bay + gioi han ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; mk = M[1]; dd = 0.5
    marks(d); stand(d); nail(d, dd)
    ks = clamp((t - mk) / 0.4)
    gx, gy = bob_right(phimax(dd), dd)                             # dinh that: dung vach
    rise = clamp((t - 0.5) / 1.5)                                  # bong "nghi" bay len tu vach toi cao hon
    wx, wy = bob_right(phimax(dd) + rise * (math.radians(85) - phimax(dd)), dd)
    ghost(d, (wx, wy), RED, 1 - 0.5 * ks)
    text(d, (wx + 45, wy - 10), "nghĩ", 56, RED, anchor="lm", alpha=1 - 0.5 * ks)
    if ks > 0:
        for s in (1, -1): d.line([(wx - 40, wy - 40 * s), (wx - 40 + 80 * ks, wy - 40 * s + 80 * s * ks)], fill=RED, width=7)
        ghost(d, (gx, gy), GREEN, ks); text(d, (gx + 45, gy + 45), "thật", 56, GREEN, anchor="lm", alpha=ks)
    pos, side, sg = swing_pos(t * 0.75, dd)
    draw_pend(d, pos, side, dd)
    k0 = appear(t, 0.2, 0.4); k3 = appear(t, M[2] - 0.1, 0.45); a1 = k0 * (1 - k3); y = 1015
    if a1 > 0:
        card(d, (40, y, 1040, y + 420), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
        pill(d, W / 2, y + 70, "BẪY", RED, a1)
        q = "“Dây ngắn, lên cao hơn”"; lw = tw(d, q, F(62)); yy = y + 190
        text(d, (W / 2, yy), q, 62, mix(INK, GRAY, ks), alpha=a1)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
        k2 = appear(t, mk + 0.2, 0.45)
        if k2 > 0: text(d, (W / 2, y + 320), "Vẫn tới vạch cũ", 62, DORANGE, alpha=a1 * k2)
    if k3 > 0:
        card(d, (40, y, 1040, y + 330), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, y + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, y + 210), "Đinh dưới vạch 0,20 m: chưa thử", 60, INK, alpha=k3)
        yn = ypos(0.9); xn = PX + 150                              # dinh "thu" thap hon vach, chua lam
        d.ellipse([xn - 14, yn - 14, xn + 14, yn + 14], outline=A(NAVY, k3), width=4)
        text(d, (xn + 30, yn), "?", 60, NAVY, anchor="lm", alpha=k3)

# ---------------- canh 5: thu nghi (cau chot o khung: 0,30 m) ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 230, 1040, 1620), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 310, "THỬ NGHĨ", ORANGE, k)
    # con lac nho vuong dinh lac lien tuc (minh hoa, khong ghi so)
    px, py, Lp, dn = 540, 400, 420, 0.5
    th0 = math.acos(1 - H0); ph0 = math.acos(1 - H0 / (1 - dn))
    per = 2.4; s = (t % per) / per
    if s < 0.5:
        a = th0 * math.cos(math.pi * s / 0.5) if s < 0.25 else 0
        if s < 0.25: x, y = px - Lp * math.sin(th0 * math.cos(math.pi / 2 * s / 0.25)), py + Lp * math.cos(th0 * math.cos(math.pi / 2 * s / 0.25)); side = "L"
        else:
            ph = ph0 * math.sin(math.pi / 2 * (s - 0.25) / 0.25); r = (1 - dn) * Lp; side = "R"
            x, y = px + r * math.sin(ph), py + dn * Lp + r * math.cos(ph)
    else:
        if s < 0.75:
            ph = ph0 * math.cos(math.pi / 2 * (s - 0.5) / 0.25); r = (1 - dn) * Lp; side = "R"
            x, y = px + r * math.sin(ph), py + dn * Lp + r * math.cos(ph)
        else:
            th = th0 * math.sin(math.pi / 2 * (s - 0.75) / 0.25); side = "L"
            x, y = px - Lp * math.sin(th), py + Lp * math.cos(th)
    d.rounded_rectangle([px - 130, py - 18, px + 130, py], radius=6, fill=A(STEEL, k))
    yn = py + dn * Lp
    if side == "R": d.line([(px, py), (px, yn), (x, y)], fill=A(NAVY, k), width=4)
    else: d.line([(px, py), (x, y)], fill=A(NAVY, k), width=4)
    d.ellipse([px - 11, yn - 11, px + 11, yn + 11], fill=A(NAIL, k))
    d.ellipse([x - 24, y - 24, x + 24, y + 24], fill=A(BOB, k), outline=A(BOB_D, k), width=3)
    text(d, (W / 2, 950), "Dây 1,0 m, đinh 0,5 m dưới", 62, INK, alpha=k)
    text(d, (W / 2, 1040), "điểm treo, thả từ 0,20 m.", 62, INK, alpha=k)
    text(d, (W / 2, 1160), "Lên cao nhất bên kia,", 64, DORANGE, alpha=k)
    text(d, (W / 2, 1250), "thấp hơn đinh bao nhiêu?", 64, DORANGE, alpha=k)
    seg_bar(d, 1400, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, r, b, e = sc["hook"], sc["do"], sc["rut"], sc["bay"], sc["end"]
    return [(h["t0"] + REL0 + APP, "tap"), (h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.05, "ding"),
            (do["t0"] + do["M"][1] + 0.1, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"),
            (b["t0"] + b["M"][1], "buzz"), (b["t0"] + b["M"][2] - 0.1, "tap"), (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l10-dong-nang-the-nang-02", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Động năng, thế năng · thachlab.id.vn", scenes=[
 dict(key="hook", title="Con lắc dây 1,0 m", draw=s_hook, tail=0.3, caps=[
   ("Thả từ vạch 0,20 m, chưa có đinh.", 3.8),
   ("Dừng lại, tự đoán.", 5.8)]),
 dict(key="do", title="Dời đinh, thả lại", draw=s_do, tail=0.5, caps=[
   ("Thả nhẹ từ vạch cũ, không đẩy.", 6.4),
   ("Góc khác nhau, độ cao như nhau.", 3.8)]),
 dict(key="rut", title="Vì sao cùng độ cao?", draw=s_rut, tail=0.6, caps=[
   ("Nhìn góc giữa T và v.", 3.6),
   ("Từ đỉnh này sang đỉnh kia.", 4.8)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Đúng không?", 3.2),
   ("Sai: hai bên cùng một vạch.", 3.4),
   ("Giới hạn của lần đo.", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng lại, tự tính.", 7.3)]),
])

def _kiem_dong_bo():
    """Canh Tien hanh: so hang bang = so lan da toi dinh; luc hang hien qua nang o dung vach 0,20 m; khong vuot vach."""
    c = copy.deepcopy(CLIP); build(c); sc = c["scenes"][1]; t = 0.0; loi = 0
    while t < sc["T"]:
        j = which(t); rows = sum(1 for i in range(3) if t >= row_t(i))
        if j >= 0:
            pos, side, al, ok = run_state(t - T0S[j], DS[j])
            if rows != j + (1 if ok else 0): loi += 1
            if pos[1] < YH - 0.5: loi += 1
            if ok and abs(pos[1] - YH) > 0.5: loi += 1
        t += 0.05
    return loi
