# Clip: tn-l10-do-g-02 - Do g bang do thi s theo t^2 tu nam do cao (31/10/2026; dung lai 27/11/2026 theo cong moi viec 4:
# --do-chu 0 LOI, chu >= 56 px khi ve, Du doan khong nut, chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-do-g-02.json (_kiem_so() doi chieu):
#   so_lieu_mau: s = 0,2..0,6 m -> t = 0,204 / 0,249 / 0,288 / 0,321 / 0,352 s ; t^2 = 0,0416 / 0,0620 / 0,0829 / 0,1030 / 0,1239 s^2.
#   ghi_chu: do doc hai diem xa = 0,400 / 0,0823 = 4,86 m/s^2 -> g = 9,72 m/s^2.
# Du doan (moi, vi Quan sat cua bai da noi "(t^2, s) gan nhu thang hang"): s gap 3 (0,200 -> 0,600 m), t gap may lan?
#   -> 0,352 / 0,204 = 1,7 lan (khong gap 3). Khung: A 1,7 / B 2 / C 3 / D 9 lan.
# Bay = hien_tuong_hay_sai thu 3: lay do doc theo hai diem sat (0,4 & 0,5 m): 0,100 / 0,0201 = 4,98 -> g 9,95, lech hon.
# Thu nghi (= cau_chot khung web, s = 0,250 m TRONG mien da do 0,2-0,6 vi Gioi han noi tren 0,6 m chua biet): do doc 4,86
#   -> t^2 = 0,250 / 4,86 = 0,0514 s^2 -> t = 0,23 s. Hai buoc; 0,23 khong hien. Nhieu: 0,05 (chua can) / 0,15 (t ti le s
#   tu 0,600 m) / 0,21 (t ti le s tu 0,300 m) -> C, D deu nam giua 0,204 va 0,249 nen khong doan bang noi suy. Bay "nhan 2"/"ve s theo t" khong dung (Rut ra da noi g = 2 . do doc).
from engine import *

ROWS = [(0.200, 0.204, 0.0416), (0.300, 0.249, 0.0620), (0.400, 0.288, 0.0829),
        (0.500, 0.321, 0.1030), (0.600, 0.352, 0.1239)]
K, G, CH_S = 4.86, 9.72, 0.250

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-do-g-02.json")))
    assert [tuple(r) for r in k["so_lieu_mau"]["hang"]] == ROWS
    for s, t, t2 in ROWS: assert abs(t * t - t2) < 6e-5
    kf = (ROWS[4][0] - ROWS[0][0]) / (ROWS[4][2] - ROWS[0][2]); assert f"{kf:.2f}" == "4.86" and f"{2 * K:.2f}" == "9.72"
    kc = (ROWS[3][0] - ROWS[2][0]) / (ROWS[3][2] - ROWS[2][2]); assert f"{kc:.2f}" == "4.98" and f"{2 * kc:.2f}" == "9.95"
    assert f"{ROWS[4][1] / ROWS[0][1]:.1f}" == "1.7"
    assert ROWS[0][0] < CH_S < ROWS[1][0]                            # trong mien da do (Gioi han: chua biet tren 0,600 m)
    assert f"{math.sqrt(CH_S / K):.2f}" == "0.23" and f"{math.sqrt(2 * CH_S / 9.8) + 0.002:.2f}" == "0.23"
    assert f"{CH_S / K:.2f}" == "0.05" and f"{ROWS[4][1] * CH_S / ROWS[4][0]:.2f}" == "0.15" and f"{ROWS[1][1] * CH_S / ROWS[1][0]:.2f}" == "0.21"
_kiem_so()

def vn(x, nd): return f"{x:.{nd}f}".replace(".", ",")
STEEL = (110, 120, 140); STEEL_L = (200, 205, 216); WOOD = (250, 236, 196); WOOD_D = (190, 160, 100)
POST = (71, 85, 105); HL = (255, 247, 237)
DRED = (185, 28, 28); DTEAL = (15, 118, 110); EMPTY = (148, 140, 128); C_S = (37, 99, 235); C_T = (176, 64, 8)
DGREEN = (21, 128, 61)

def segs(d, x, y, parts, size, alpha=1.0):
    """Chu nhieu mau mot dong (giua x). parts = [(chu, mau)] hoac [(chu, mau, True)] -> gach ngang tren (t trung binh)."""
    f = F(size); tot = sum(tw(d, p[0], f) for p in parts); xx = x - tot / 2
    for p in parts:
        s, c = p[0], p[1]; w = tw(d, s, f)
        dtext(d, (xx, y), s, f, c, alpha, "lm")
        if len(p) > 2 and p[2]:
            yb = y - size * 0.6
            d.line([(xx + w * 0.1, yb), (xx + w * 0.9, yb)], fill=A(c, alpha), width=max(4, size // 14))
        xx += w
    return tot

def seg_bar(d, y, t, t0, t1, col, a=1.0):
    p = clamp((t - t0) / (t1 - t0)); on = 5 - int(p * 5 + 1e-9)
    for i in range(5):
        x = 190 + i * 145
        if i < on: card(d, (x, y, x + 120, y + 70), fill=A(col, a), r=18)
        else: card(d, (x, y, x + 120, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=18, w=4)

def badge(d, y, s, col, a=1.0):
    pw = tw(d, s, F(58)) + 64
    card(d, (W / 2 - pw / 2, y, W / 2 + pw / 2, y + 82), fill=A(col, a), r=40)
    text(d, (W / 2, y + 41), s, 58, WHITE, alpha=a)

# ---------------- gia do (ben trai) ----------------
SY0, SPX = 330, 1400.0
def SYp(s): return SY0 + SPX * s
BX, BR = 285, 20
def rig(d, gate_s, ball_s=None, ball_a=1.0, ghosts=False):
    card(d, (40, 215, 420, 1290), fill=WHITE, outline=LIGHT, w=3)
    d.rectangle([150, SY0 - 6, 180, SYp(0.6) + 10], fill=WOOD, outline=WOOD_D, width=3)
    for i in range(7):
        y = SYp(i / 10); d.line([(150, y), (176, y)], fill=INK, width=3)
    for v in (0, 0.2, 0.4, 0.6): text(d, (140, SYp(v)), "0" if v == 0 else vn(v, 1), 56, C_S, anchor="rm")
    text(d, (75, 250), "s (m)", 56, C_S, anchor="lm")
    d.rectangle([240, 230, 330, SY0 - 2 * BR], fill=NAVY)
    if ghosts:
        for s, *_r in ROWS:
            y = SYp(s)
            for x0 in range(222, 350, 22): d.line([(x0, y), (x0 + 12, y)], fill=GRAY, width=4)
    yg = SYp(gate_s)
    d.line([(250, yg), (320, yg)], fill=RED, width=5)
    d.rectangle([222, yg - 22, 250, yg + 22], fill=POST); d.rectangle([320, yg - 22, 348, yg + 22], fill=POST)
    if ball_s is not None and ball_a > 0.02:
        y = SYp(ball_s) - BR
        d.ellipse([BX - BR, y - BR, BX + BR, y + BR], fill=A(STEEL, ball_a), outline=A(NAVY, ball_a), width=2)
        d.ellipse([BX - 9, y - 10, BX - 2, y - 3], fill=A(STEEL_L, ball_a))

def clock(d, val, lit=True):
    card(d, (440, 215, 1040, 365), fill=NAVY, r=26)
    text(d, (740, 290), "t = " + vn(val, 3) + " s", 64, YELLOW if lit else GRAY)

def table(d, n, cur=None, ring=(), box=(440, 385, 1040, 1290)):
    card(d, box, fill=WHITE, outline=LIGHT, w=3)
    cx = (box[0] + box[2]) / 2; xs, xt = cx - 140, cx + 140
    text(d, (xs, box[1] + 65), "s (m)", 56, C_S); segs(d, xt, box[1] + 65, [("t", C_T, True), (" (s)", C_T)], 56)
    d.line([(box[0] + 20, box[1] + 115), (box[2] - 20, box[1] + 115)], fill=LIGHT, width=3)
    step = min(125, (box[3] - box[1] - 215) / 5)
    for i in range(5):
        y = box[1] + 175 + step * 0.16 + i * step
        if cur == i: d.rounded_rectangle([box[0] + 15, y - 50, box[2] - 15, y + 50], radius=16, fill=HL)
        if i in ring: d.rounded_rectangle([box[0] + 15, y - 50, box[2] - 15, y + 50], radius=16, outline=ORANGE, width=6)
        text(d, (xs, y), vn(ROWS[i][0], 3), 60, C_S)
        if i < n: text(d, (xt, y), vn(ROWS[i][1], 3), 60, C_T)

# ---------------- do thi s theo t^2 ----------------
def graph(d, box, n=5, line=0.0, tri=None, tri_k=0.0, tri_col=DGREEN, ext=0.0):
    card(d, box, fill=WHITE, outline=LIGHT, w=3)
    OX, OY = box[0] + 170, box[3] - 100
    XS = (box[2] - 120 - OX) / 0.14; YS = (OY - box[1] - 110) / 0.7
    P = lambda t2, s: (OX + XS * t2, OY - YS * s)
    for v in (0.2, 0.4, 0.6): d.line([P(0, v), P(0.14, v)], fill=(240, 236, 228), width=2)
    arrow(d, (OX, OY), (box[2] - 40, OY), NAVY, w=5, head=18); arrow(d, (OX, OY), (OX, box[1] + 50), NAVY, w=5, head=18)
    for v in (0.04, 0.08, 0.12):
        x = P(v, 0)[0]; d.line([(x, OY), (x, OY + 12)], fill=NAVY, width=4); text(d, (x, OY + 50), vn(v, 2), 56, C_T)
    for v in (0.2, 0.4, 0.6):
        y = P(0, v)[1]; d.line([(OX - 12, y), (OX, y)], fill=NAVY, width=4); text(d, (OX - 22, y), vn(v, 1), 56, C_S, anchor="rm")
    text(d, (OX + 30, box[1] + 55), "s (m)", 58, C_S, anchor="lm")
    segs(d, box[2] - 130, OY - 50, [("t", C_T, True), ("² (s²)", C_T)], 58)
    if line > 0:
        e = 0.13 * line; d.line([P(0, 0), P(e, K * e)], fill=DGREEN, width=7)
    if ext > 0:                                                 # sau diem cuoi: net dut xam (chua do)
        for k in range(4):
            u0 = 0.130 + 0.004 * k
            if (u0 - 0.130) / 0.016 > ext: break
            d.line([P(u0, K * u0), P(u0 + 0.002, K * (u0 + 0.002))], fill=GRAY, width=7)
    if tri is not None and tri_k > 0:
        i, j = tri; a, b = P(ROWS[i][2], ROWS[i][0]), P(ROWS[j][2], ROWS[j][0])
        c = A(tri_col, tri_k)
        d.line([a, (b[0], a[1])], fill=c, width=6); d.line([(b[0], a[1]), b], fill=c, width=6)
        ds, dt2 = ROWS[j][0] - ROWS[i][0], ROWS[j][2] - ROWS[i][2]
        text(d, (a[0] + 25, a[1] + 45), vn(dt2, 4) + " s²", 56, tri_col, anchor="lm", alpha=tri_k)
        lab = vn(ds, 3) + " m"; right = b[0] + 15 + tw(d, lab, F(56)) < box[2] - 20
        text(d, (b[0] + 15, (a[1] + b[1]) / 2) if right else (b[0] - 15, a[1] - 50), lab, 56, tri_col, anchor="lm" if right else "rm", alpha=tri_k)
    for i in range(n):
        x, y = P(ROWS[i][2], ROWS[i][0]); dot(d, x, y, 15, NAVY, WHITE)
    return P

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, 0.2 + 0.4 * ease((t - 1.0) / 1.2), ball_s=0.0, ghosts=True); clock(d, 0.0, lit=False)
    card(d, (440, 385, 1040, 1290), fill=WHITE, outline=LIGHT, w=3)
    text(d, (740, 520), "Đổi độ cao s:", 60, INK); text(d, (740, 610), "0,200 → 0,600 m", 60, C_S)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 760 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    badge(d, y0 + 26, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 175), "s gấp 3: 0,200 → 0,600 m.", 62, INK, alpha=a)
    text(d, (W / 2, y0 + 265), "t gấp mấy lần?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 350, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (5 do cao, chieu cham 2 lan) ----------------
SLOW, MOVE, HOLD, RUN0 = 2.0, 0.35, 0.3, 0.3
def schedule():
    out = []; s = RUN0
    for i in range(5):
        f0 = s + MOVE; f1 = f0 + ROWS[i][1] * SLOW
        out.append((s, f0, f1)); s = f1 + HOLD
    return out
SCHED = schedule()

def run_state(t):
    j = 0
    for i, (s0, *_r) in enumerate(SCHED):
        if t >= s0: j = i
    s0, f0, f1 = SCHED[j]
    gprev = ROWS[j - 1][0] if j > 0 else ROWS[0][0]
    if t < f0:
        g = gprev + (ROWS[j][0] - gprev) * ease((t - s0) / MOVE)
        return g, 0.0, 1.0, ROWS[j - 1][1] if j > 0 else 0.0, j > 0, j, j
    u = clamp((t - f0) / (f1 - f0)); g = ROWS[j][0]
    if t < f1: return g, g * u * u, 1.0, round(ROWS[j][1] * u, 3), True, j, j
    return g, g, 1 - clamp((t - f1) / 0.25), ROWS[j][1], True, j + 1, j

def s_do(img, d, t, sc):
    g, bs, ba, cv, lit, done, j = run_state(t)
    rig(d, g, bs, ba); clock(d, cv, lit); table(d, done, cur=j if done <= j else None)
    card(d, (40, 1310, 1040, 1430), fill=NAVY, r=30)
    text(d, (W / 2, 1370), "chiếu chậm ×2", 58, YELLOW)

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]; ka = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 560), fill=A((236, 253, 243), ka), outline=A(GREEN, ka), w=6)
    badge(d, 240, "ĐÁP ÁN", DTEAL, ka)
    text(d, (W / 2, 400), "t chỉ gấp ≈ 1,7 lần,", 64, DTEAL, alpha=ka)
    text(d, (W / 2, 485), "không gấp 3", 64, DTEAL, alpha=ka)
    table(d, 5, ring=(0, 4), box=(40, 580, 1040, 1290))
    k2 = appear(t, M[1] + 0.1, 0.45)
    card(d, (40, 1310, 1040, 1590), fill=A(WHITE, k2), outline=A(C_T, k2), w=5)
    text(d, (W / 2, 1390), "0,352 s : 0,204 s ≈ 1,7", 60, C_T, alpha=k2)
    text(d, (W / 2, 1500), "0,600 m : 0,200 m = 3", 60, C_S, alpha=k2)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    n = sum(1 for i in range(5) if t >= 0.4 + 0.25 * i)
    graph(d, (40, 215, 1040, 1100), n=n, line=ease(clamp((t - 1.8) / 1.0)) if t > 1.82 else 0.0, tri=(0, 4), tri_k=appear(t, M[1] - 0.1, 0.4))
    k2 = appear(t, M[1] - 0.1, 0.45)
    card(d, (40, 1120, 1040, 1590), fill=A(WHITE, k2), outline=A(GREEN, k2), w=5)
    text(d, (W / 2, 1200), "độ dốc = 0,400 m : 0,0823 s²", 58, INK, alpha=k2)
    text(d, (W / 2, 1300), "≈ 4,86 m/s²", 60, DGREEN, alpha=k2)
    text(d, (W / 2, 1450), "g = 2 · 4,86 ≈ 9,72 m/s²", 64, DTEAL, alpha=appear(t, M[1] + 2.2, 0.4))

# ---------------- canh 5: Bay (hai diem sat) ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; ok = t >= M[1] - 0.1
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=DRED, w=6)
    text(d, (W / 2, 300), "✗ Hai điểm sát nhau:", 62, DRED)
    text(d, (W / 2, 420), "0,100 m : 0,0201 s² ≈ 4,98 m/s²", 56, DRED)
    graph(d, (40, 580, 1040, 1290), line=1.0, tri=(0, 4) if ok else (2, 3), tri_k=1.0, tri_col=DGREEN if ok else DRED)
    if ok:
        card(d, (40, 1310, 1040, 1590), fill=WHITE, outline=DTEAL, w=6)
        text(d, (W / 2, 1395), "✓ Hai điểm xa nhau:", 60, DTEAL)
        text(d, (W / 2, 1500), "độ dốc 4,86 m/s²", 60, DTEAL)

# ---------------- canh 6: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    card(d, (40, 215, 1040, 560), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 300), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 450), "Cao hơn 0,600 m: còn thẳng?", 60, INK)
    graph(d, (40, 580, 1040, 1290), line=1.0, ext=clamp((t - 0.5) / 1.5))
    text(d, (960, 690), "?", 72, GRAY, alpha=appear(t, 2.0, 0.4))

# ---------------- canh 7: THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 210, 1040, 1585), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    badge(d, 235, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 400), "Cùng bộ dụng cụ, s = 0,250 m.", 60, INK, alpha=k)
    text(d, (W / 2, 495), "Độ dốc 4,86 m/s².", 60, DGREEN, alpha=k)
    segs(d, W / 2, 620, [("t", C_T, True), (" đọc được bao nhiêu (s)?", C_T)], 62, alpha=k)
    x = 540; yt, yb = 760, 1180
    d.rectangle([x - 45, yt - 10, x + 45, yt + 50], fill=A(NAVY, k))
    d.line([(x + 110, yt + 60), (x + 110, yb)], fill=A(C_S, k), width=5)
    arrow(d, (x + 110, yt + 100), (x + 110, yt + 60), A(C_S, k), w=5, head=18); arrow(d, (x + 110, yb - 40), (x + 110, yb), A(C_S, k), w=5, head=18)
    text(d, (x + 140, (yt + yb) / 2), "0,250 m", 58, C_S, anchor="lm", alpha=k)
    d.line([(x - 35, yb), (x + 35, yb)], fill=A(RED, k), width=5)
    d.rectangle([x - 63, yb - 22, x - 35, yb + 22], fill=A(POST, k)); d.rectangle([x + 35, yb - 22, x + 63, yb + 22], fill=A(POST, k))
    bs = (t * 0.6) % 1.0; by = yt + 70 + (yb - yt - 90) * bs * bs
    d.ellipse([x - 20, by - 20, x + 20, by + 20], fill=A(STEEL, k), outline=A(NAVY, k), width=2)
    seg_bar(d, 1290, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = (sc[k] for k in ("hook", "do", "dapan", "bay", "end"))
    cs = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
    cs += [(do["t0"] + f1, "tap") for s0, f0, f1 in SCHED]
    cs += [(da["t0"] + 0.15, "ding"), (b["t0"] + 0.4, "buzz"), (e["t0"] + 0.15, "open")]
    return cs

CLIP = dict(id="tn-l10-do-g-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Thực hành đo gia tốc rơi tự do · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Năm độ cao", draw=s_hook, tail=0.3, caps=[
   ("Năm độ cao, đo t.", 3.0),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Mỗi độ cao: trung bình 5 lần.", 3.6),
   ("Cao hơn, rơi lâu hơn.", 3.0)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("So độ cao đầu và cuối.", 3.2),
   ("t tăng chậm hơn s.", 3.4)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Vẽ s theo t bình phương.", 3.2),
   ("g bằng hai lần độ dốc.", 3.6)]),
 dict(key="bay", title="Bẫy: hai điểm sát nhau", draw=s_bay, tail=0.3, caps=[
   ("Lấy hai điểm sát nhau?", 3.4),
   ("Hai điểm xa: ít lệch hơn.", 3.4)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("Mới đo tới 0,600 m.", 3.5)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Thử tính, rồi chọn đáp án.", 6.0)]),
])
