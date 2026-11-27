# Clip: tn-l10-do-toc-do-02 - Bi chan mot cong quang F (MODE B, v = d/t); tia lech tam (10/11/2026; dung lai 27/11/2026
#   theo cong moi viec 4: --do-chu 0 LOI, chu ve >= 56 px, khong chi so duoi, Bay khong gach, THU NGHI khong goi y).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-do-toc-do-02.json (_kiem_so() doi chieu):
#   d = 20,0 mm; v_F that = 0,849 m/s; so_lieu_mau t = 0,024 / 0,023 / 0,024 s (tia qua tam), t trung binh 0,024 s;
#   v_F = 0,0200 m : 0,024 s ~ 0,83 m/s; ghi_chu: tia lech 6 mm -> day cung 16 mm, d/t lon hon that 25 %.
# Du doan MOI (khong trung Cau 4 cua bai "d/t lon hay nho hon"): tia cao hon tam 6 mm -> bi che tia tren doan dai bao nhieu
#   so voi 20 mm? (dap an: ngan hon, 16 mm). Hop exp truoc clip chi noi "chinh tia ngang tam", khong noi vi sao.
# Bay: lay ban kinh 10,0 mm lam d (hien_tuong_hay_sai cua kho) -> 0,42 m/s; dung: 0,0200 m -> 0,83 m/s.
# Chot (THU NGHI, chua chieu): tia cao hon tam 8 mm (lech 0..8 trong tham_so) -> day cung 2*sqrt(10^2 - 8^2) = 12 mm.
from engine import *

D_MM, VF, LECH = 20.0, 0.849, 6.0
READ = (0.024, 0.023, 0.024)
T_BLK = 0.0236
SLOW = 40.0
PXM = 12.0
RB = D_MM / 2 * PXM                                  # 120 px
BALL = (71, 85, 105); BALL_HI = (203, 213, 225); RAIL = (196, 200, 212); RAIL_D = (150, 155, 170); POST = (71, 85, 105)
DRED = (185, 28, 28); DGREEN = (10, 110, 50); DPURP = (91, 33, 182); DORANGE = (176, 64, 8); SUB = (60, 66, 92)
XB = 560

def vn(x, nd=3): return f"{x:.{nd}f}".replace(".", ",")
def chord(lech): return 2 * math.sqrt((D_MM / 2) ** 2 - lech ** 2)

def _kiem_so():
    import json, os
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-do-toc-do-02.json")))
    assert tuple(r[1] for r in k["so_lieu_mau"]["hang"]) == READ
    tp = {x["ky_hieu"]: x for x in k["tham_so"]}
    assert tp["d"]["mac_dinh"] == D_MM and tp["v_F"]["gia_tri"] == VF and tp["lech"]["max"] >= 8
    assert abs(chord(6) - 16) < 1e-9 and abs(chord(8) - 12) < 1e-9 and abs(D_MM / chord(6) - 1.25) < 1e-9
    assert round(0.0200 / 0.024, 2) == 0.83 and round(0.0100 / 0.024, 2) == 0.42
_kiem_so()

def cbar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0))
    d.rounded_rectangle([110, y, 970, y + 80], radius=40, fill=A((246, 244, 250), a))
    if p < 1: d.rounded_rectangle([110, y, 110 + max(80, 860 * (1 - p)), y + 80], radius=40, fill=A(col, a))

def pill(d, y, s, col, k):
    pw = tw(d, s, F(56)) + 60
    card(d, (W / 2 - pw / 2, y, W / 2 + pw / 2, y + 76), fill=A(col, k), r=36)
    text(d, (W / 2, y + 38), s, 56, WHITE, alpha=k)

# ---------- can canh: bi lan qua tia cong F (ve len anh phu, cat theo khung) ----------
BOX = (40, 265, 1040, 800); RAIL1 = 740; CY = RAIL1 - RB; BEAM_C = CY
def closeup(img, d, bx, beam_y, blocked, show_chord=False, ghost=None):
    x0, y0, x1, y1 = BOX
    sub = Image.new("RGB", (x1 - x0, y1 - y0), WHITE); sd = ImageDraw.Draw(sub, "RGBA")
    old = IMG_REF[0]; IMG_REF[0] = sub
    sh = lambda y: y - y0; sx = lambda x: x - x0
    sd.rectangle([20, sh(RAIL1), 980, sh(RAIL1) + 22], fill=RAIL, outline=RAIL_D)
    sd.rectangle([sx(XB) - 11, sh(290), sx(XB) + 11, sh(beam_y) - 30], fill=POST)
    sd.rectangle([sx(XB) - 26, sh(beam_y) - 34, sx(XB) + 26, sh(beam_y) - 18], fill=POST)
    for b, al in ((ghost, 0.35), (bx, 1.0)):
        if b is None: continue
        x = sx(b)
        sd.ellipse([x - RB, sh(CY) - RB, x + RB, sh(CY) + RB], fill=BALL + (int(255 * al),), outline=NAVY + (int(255 * al),), width=3)
        if al > 0.9:
            sd.ellipse([x - 70, sh(CY) - 82, x - 30, sh(CY) - 42], fill=BALL_HI)
            th = (b - XB) / RB
            sd.line([(x, sh(CY)), (x + RB * 0.82 * math.sin(th), sh(CY) - RB * 0.82 * math.cos(th))], fill=(148, 163, 184), width=6)
    if show_chord:
        hc = math.sqrt(RB * RB - (beam_y - CY) ** 2)
        sd.line([(sx(XB) - hc, sh(beam_y)), (sx(XB) + hc, sh(beam_y))], fill=ORANGE, width=8)
    if blocked: sd.ellipse([sx(XB) - 13, sh(beam_y) - 13, sx(XB) + 13, sh(beam_y) + 13], outline=(254, 202, 202), width=4)
    else: dot(sd, sx(XB), sh(beam_y), 11, RED)
    IMG_REF[0] = old
    m = Image.new("L", sub.size, 0); ImageDraw.Draw(m).rounded_rectangle([3, 3, x1 - x0 - 4, y1 - y0 - 4], radius=30, fill=255)
    img.paste(sub, (x0, y0), m)
    d.rounded_rectangle(BOX, radius=34, outline=LIGHT, width=3)
    text(d, (XB + 200, 320), "cổng F", 56, INK)

def clock(d, y, val, hot=False):
    card(d, (40, y, 1040, y + 170), fill=WHITE, outline=LIGHT, w=3)
    card(d, (80, y + 20, 600, y + 150), fill=NAVY, r=18)
    text(d, (340, y + 85), vn(val) + " s", 80, YELLOW if (hot or val > 0) else GRAY)
    text(d, (820, y + 85), "MODE B", 60, NAVY)

def lech_mark(d, beam_y, col, lab, alpha=1.0, x=XB + 150, bg=False):
    d.line([(x, beam_y), (x, CY)], fill=A(col, alpha), width=5)
    for yy in (beam_y, CY): d.line([(x - 14, yy), (x + 14, yy)], fill=A(col, alpha), width=5)
    ym = (beam_y + CY) / 2 + 4
    if bg:
        wl = tw(d, lab, F(56))
        d.rounded_rectangle([x + 18, ym - 40, x + 42 + wl, ym + 40], radius=16, fill=A(WHITE, 0.92 * alpha), outline=A(col, alpha), width=3)
    text(d, (x + 30, ym), lab, 56, col, anchor="lm", alpha=alpha)

# ---------------- canh 1: Du doan ----------------
BEAM_L = BEAM_C - LECH * PXM
def s_hook(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    bx = XB - RB - 170 + 20 * math.sin(t * 1.5)
    closeup(img, d, bx, BEAM_L, False)
    d.line([(bx + 20, CY), (XB + 150, CY)], fill=A(GRAY, 1), width=3)
    dot(d, bx, CY, 9, WHITE)
    lech_mark(d, BEAM_L, DORANGE, "6 mm")
    a0, a1 = (bx - RB, CY - RB - 40), (bx + RB, CY - RB - 40)
    arrow(d, (bx, a0[1]), a0, A(BLUE, 1), w=4, head=16); arrow(d, (bx, a1[1]), a1, A(BLUE, 1), w=4, head=16)
    text(d, (230, 330), "d = 20,0 mm", 56, BLUE)
    k = appear(t, M[1] - 0.3, 0.45)
    if k <= 0: return
    y0 = 870 + (1 - k) * 30
    card(d, (50, y0, 1030, y0 + 640), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, y0 + 22, "DỰ ĐOÁN", PURPLE, k)
    cbar(d, y0 + 118, t, M[1] + 0.3, sc["T"] - 0.15, DPURP, k)
    text(d, (W / 2, y0 + 300), "Tia cao hơn tâm 6 mm.", 62, INK, alpha=k)
    text(d, (W / 2, y0 + 410), "Bi che tia đoạn dài bao nhiêu?", 60, PURPLE, alpha=k)
    text(d, (W / 2, y0 + 530 + 10 * math.sin(t * 3)), "?", 72, PURPLE, alpha=k)

# ---------------- canh 2: Tien hanh (tia qua tam, 3 lan, chieu cham 40 lan) ----------------
APP, EXIT, HOLD, RST = 0.55, 0.45, 0.6, 0.4
RUN0 = 0.5
VPX = VF * 1000 / SLOW * PXM                           # 255 px/s tren man
BLK = T_BLK * SLOW
def schedule():
    out = []; s = RUN0
    for _ in READ:
        L = RST + APP + BLK + EXIT + HOLD; out.append((s, L)); s += L
    return out
SCHED = schedule()

def run_state(t):
    if t < SCHED[0][0]: return 0, -9, None, 0.0, 0
    j = 0
    for i, (s, L) in enumerate(SCHED):
        if t >= s: j = i
    s, L = SCHED[j]; tk = READ[j]
    u = t - s - RST - APP
    if t - s < RST: return j, u, None, 0.0, j
    uc = min(u, BLK + EXIT)
    bx = XB - RB + uc * VPX
    clk = 0.0 if u < 0 else (tk if u >= BLK else min(tk, math.floor(u / SLOW * 1000) / 1000))
    return j, u, bx, clk, j + (1 if u >= BLK else 0)

def s_do(img, d, t, sc):
    IMG_REF[0] = img
    j, u, bx, clk, done = run_state(t)
    blocked = bx is not None and 0 <= u < BLK
    closeup(img, d, bx, BEAM_C, blocked)
    text(d, (230, 330), "chậm 40 lần", 56, SUB)
    text(d, (XB + 200, 400), "qua tâm", 56, RED)
    clock(d, 815, clk, hot=blocked)
    y = 1015
    card(d, (40, y, 1040, y + 430), fill=WHITE, outline=LIGHT, w=3)
    XS = (300, 700)
    text(d, (XS[0], y + 60), "Lần", 56, INK); text(d, (XS[1], y + 60), "t (s)", 56, INK)
    d.line([(90, y + 115), (990, y + 115)], fill=LIGHT, width=3)
    for i, tk in enumerate(READ):
        yy = y + 185 + i * 85
        if i == j and done <= i and t >= SCHED[0][0]:
            d.rounded_rectangle([80, yy - 40, 1000, yy + 40], radius=16, fill=(255, 247, 237))
        text(d, (XS[0], yy), str(i + 1), 56, MUTED)
        if i < done: text(d, (XS[1], yy), vn(tk), 60, NAVY)

# ---------------- canh 3: Dap an (tia cao hon tam 6 mm) ----------------
HC6 = math.sqrt(RB * RB - (LECH * PXM) ** 2)          # 96 px = 8 mm
BLK6 = 2 * HC6 / VPX
def s_dapan(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]
    per = APP + BLK6 + EXIT + 0.5
    u = ((t - 0.3) % per) - APP if t > 0.3 else -APP
    bx = XB - HC6 + clamp(u, -APP, BLK6 + EXIT) * VPX
    blocked = 0 <= u < BLK6
    kf = appear(t, M[1] - 0.05, 0.4)
    closeup(img, d, bx, BEAM_L, blocked, show_chord=blocked or kf > 0, ghost=XB if kf > 0 else None)
    lech_mark(d, BEAM_L, DORANGE, "6 mm", x=XB + 215, bg=True)
    ka = appear(t, 0.3, 0.4)                                            # hinh tinh hien som (chua co chu, chua dây cung)
    cx, cy, R = 420, 1165, 170; k = R / 10.0
    card(d, (40, 840, 1040, 1440), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=3)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=A((226, 232, 240), ka), outline=A(NAVY, ka), width=4)
    yb = cy - 6 * k; hx = 8 * k
    d.line([(cx - R, cy), (cx + R, cy)], fill=A(BLUE, ka), width=6)
    dot(d, cx, cy, 7, A(INK, ka))
    if kf <= 0: return
    d.line([(cx - hx, yb), (cx + hx, yb)], fill=A(ORANGE, kf), width=9)
    d.line([(cx, cy), (cx + hx, yb)], fill=A(INK, kf), width=3)
    d.line([(cx, cy), (cx, yb)], fill=A(INK, kf), width=3)
    dot(d, cx, cy, 7, A(INK, kf))
    text(d, (cx + R + 40, yb), "16 mm", 60, DORANGE, anchor="lm", alpha=kf)
    text(d, (cx, cy + R + 50), "20 mm", 60, BLUE, alpha=kf)
    d.line([(cx - 6, (cy + yb) / 2), (cx - R - 20, (cy + yb) / 2)], fill=A(INK, kf), width=3)
    text(d, (cx - R - 30, (cy + yb) / 2), "6 mm", 56, INK, anchor="rm", alpha=kf)
    mh = (cx + hx / 2, (cy + yb) / 2)
    d.line([mh, (cx + R + 30, cy + 40)], fill=A(INK, kf), width=3)
    text(d, (cx + R + 40, cy + 40), "10 mm", 56, INK, anchor="lm", alpha=kf)
    s_ = "ĐÁP ÁN: ngắn hơn, 16 mm"; pw = tw(d, s_, F(56)) + 60
    pu = 0.75 + 0.25 * math.sin(t * 4)
    card(d, (W / 2 - pw / 2, 1460, W / 2 + pw / 2, 1560), fill=A((220, 252, 231), kf), outline=A(GREEN, kf * pu), r=28, w=5)
    text(d, (W / 2, 1510), s_, 56, DGREEN, alpha=kf)
    k3 = appear(t, M[2] - 0.05, 0.4)
    if k3 > 0:
        card(d, (60, 852, 1020, 948), fill=A((254, 242, 242), k3), outline=A(DRED, k3), r=24, w=4)
        text(d, (W / 2, 900), "d : t lớn hơn thật 25 %", 58, DRED, alpha=k3)

# ---------------- canh 4: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    IMG_REF[0] = img
    k = appear(t, 0.05, 0.35)
    card(d, (40, 265, 1040, 760), fill=A(WHITE, k), outline=A(LIGHT, k), w=3)
    for i, x in enumerate((200, 540, 880)):                                 # ba cho tren mang, chi F co cong
        d.rectangle([x - 70, 600, x + 70, 620], fill=A(RAIL, k))
        if i == 2:
            d.rectangle([x - 8, 360, x + 8, 560], fill=A(POST, k)); text(d, (x, 320), "F", 60, INK, alpha=k)
        else:
            text(d, (x, 500 + 12 * math.sin(t * 3 + i)), "?", 72, PURPLE, alpha=k)
    card(d, (60, 840, 1020, 1240), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, 950), "Chưa nói được", 62, NAVY, alpha=k)
    text(d, (W / 2, 1090), "Tốc độ ở chỗ khác?", 62, BLUE, alpha=k)

# ---------------- canh 5: Bay ----------------
def s_bay(img, d, t, sc):
    IMG_REF[0] = img
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    ok = appear(t, M[1] - 0.05, 0.4)
    card(d, (60, 260, 1020, 520), fill=A(WHITE, a), outline=A(DRED, a), w=6)
    text(d, (W / 2, 340), "✗ d = 10,0 mm (bán kính)", 60, DRED, alpha=a)
    text(d, (W / 2, 440), "v ≈ 0,42 m/s", 60, DRED, alpha=a)
    card(d, (60, 560, 1020, 1500), fill=A(WHITE, a), outline=A(GREEN if ok > 0 else NAVY, a), w=5)
    cx, cy, R = 540, 900, 200
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=A((226, 232, 240), a), outline=A(NAVY, a), width=4)
    dot(d, cx, cy, 7, A(INK, a))
    if ok <= 0:
        pu = 0.6 + 0.4 * math.sin(t * 4)
        arrow(d, (cx, cy), (cx + R, cy), A(DRED, a), w=8, head=24)
        d.rounded_rectangle([cx - 20, cy - 40, cx + R + 20, cy + 40], radius=16, outline=A(DRED, a * pu), width=5)
        return
    arrow(d, (cx, cy), (cx - R, cy), A(GREEN, ok), w=8, head=24); arrow(d, (cx, cy), (cx + R, cy), A(GREEN, ok), w=8, head=24)
    text(d, (W / 2, 1180), "✓ d = 20,0 mm = 0,0200 m", 60, DGREEN, alpha=ok)
    text(d, (W / 2, 1290), "(đường kính)", 56, DGREEN, alpha=ok)
    text(d, (W / 2, 1400), "v ≈ 0,83 m/s", 60, DGREEN, alpha=ok)

# ---------------- canh 6: THU NGHI ----------------
def s_end(img, d, t, sc):
    IMG_REF[0] = img
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 220, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, 250, "THỬ NGHĨ", ORANGE, k1)
    cx, cy, R = 420, 640, 200; k = R / 10.0
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=A((226, 232, 240), k1), outline=A(NAVY, k1), width=4)
    dot(d, cx, cy, 7, A(INK, k1))
    yb = cy - 8 * k
    for i in range(22):
        x0 = 120 + i * 40; d.line([(x0, yb), (x0 + 22, yb)], fill=A(RED, k1 * (0.7 + 0.3 * math.sin(t * 4 - i * 0.4))), width=5)
    xm = cx + R + 60
    d.line([(xm, cy), (xm, yb)], fill=A(ORANGE, k1), width=5)
    for yy in (cy, yb): d.line([(xm - 14, yy), (xm + 14, yy)], fill=A(ORANGE, k1), width=5)
    text(d, (xm + 30, (cy + yb) / 2), "8 mm", 56, DORANGE, anchor="lm", alpha=k1)
    text(d, (cx, cy + R + 50), "d = 20,0 mm", 56, BLUE, alpha=k1)
    text(d, (W / 2, 1020), "Tia cao hơn tâm 8 mm.", 60, INK, alpha=k1)
    text(d, (W / 2, 1120), "Bi che tia bao nhiêu mm?", 60, ORANGE, alpha=k1)
    cbar(d, 1300, t, 1.0, sc["T"] - 0.2, DORANGE, k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    cs = [(h["t0"] + h["M"][1] - 0.3, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    for s, L in SCHED: cs.append((do["t0"] + s + RST + APP, "tap"))
    cs += [(da["t0"] + da["M"][1], "ding"), (b["t0"] + 0.3, "buzz"), (b["t0"] + b["M"][1], "ding"), (e["t0"] + 0.15, "open")]
    return cs

CLIP = dict(id="tn-l10-do-toc-do-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Đo tốc độ của vật · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Tia sáng ở đâu trên bi?", draw=s_hook, tail=0.3, caps=[
   ("Bi lăn qua cổng F.", 2.8),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tia qua tâm, ba lần", draw=s_do, tail=0.3, caps=[
   ("MODE B: đếm lúc bi che tia.", 4.4),
   ("Ba lần gần như nhau.", 4.6)]),
 dict(key="dapan", title="Tia cao hơn tâm", draw=s_dapan, tail=0.3, caps=[
   ("Cùng bi, tia cao hơn tâm.", 3.0),
   ("Bi che tia ít hơn.", 3.4),
   ("t ngắn lại, d vẫn 20 mm.", 3.4)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("Chỉ biết tốc độ tại F.", 3.5)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Lấy bán kính làm d?", 3.4),
   ("d là đường kính.", 3.4)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.4, caps=[
   ("Dừng lại, tự trả lời.", 6.2)]),
])
