# Clip: tn-l10-luc-ma-sat-02 - Doi mat tiep xuc, toc do, cho lan (ban 2 cong moi, 27/11/2026)
# So lieu tu content/thi-nghiem/tn-l10-luc-ma-sat-02.json (_kiem_so()): hop 0,40 kg ; so_lieu_mau: nam cham 1,2 N ;
#   dung dung 1,2 N ; nam nhanh hon 1,2 N ; lan tren but chi 0,08 N (luc ke chi doc "duoi 0,1 N").
# Du doan (K10, khong nut): ke hop len hai but chi cho lan, so voi luc truot so chi luc ke ra sao? (dap an: nho hon rat nhieu).
# KHONG tra loi san Cau 1 cua bai (dung dung, dien tich 1/3 -> ma sat?) bang quy tac chung: chi hien so do cua hop nay,
#   khong noi "1/3", khong phat bieu "khong phu thuoc dien tich". Khong hien mu.
# Bay = hien_tuong_hay_sai[1] "keo nhanh thi ma sat truot lon hon" -> hai cot cham / nhanh cung 1,2 N.
# Chua noi duoc: mat ban uot (bai: ma sat phu thuoc tinh trang hai mat).
# Chot (ghi_chu kho): them 0,10 kg (tong 0,50 kg), keo truot deu -> F = 0,30 . 0,50 . 9,8 = 1,47 ~ 1,5 N. Khong goi y.
import math
from engine import *

M_HOP = 0.40
CASES = [("nằm", 1.2, "flat", 22), ("đứng", 1.2, "tall", 22), ("kéo\nnhanh", 1.2, "flat", 60), ("lăn", 0.08, "roll", 22)]
FMAX = 5.0
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")
def rd(f): return "dưới 0,1 N" if f < 0.1 else vn(f) + " N"
def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-luc-ma-sat-02.json")))
    assert [h[1] for h in k["so_lieu_mau"]["hang"]] == [c[1] for c in CASES]
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["m"]["gia_tri"] == M_HOP and round(ts["μ"]["gia_tri"] * 0.50 * 9.8, 1) == 1.5
_kiem_so()

WOOD = (176, 124, 74); WOOD_D = (140, 96, 54); BOX = (232, 196, 140); BOX_D = (150, 104, 56)
SKIN = (240, 196, 160); SKIN_D = (190, 140, 105); DGREEN = (21, 110, 55); DRED = (185, 28, 28)
PENCIL = (250, 204, 21); PENCIL_D = (161, 98, 7); NOTE = (60, 64, 84); EMPTY = (148, 140, 128)
DORANGE = (176, 64, 8); WT = (120, 126, 140); DTEAL = (15, 110, 100)

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

# ---------------- dan thi nghiem (nhin ngang, keo sang PHAI) ----------------
SURF = 640; XR0 = 290; ROPE, BODY = 30, 340
DIMS = {"flat": (240, 100), "tall": (100, 220), "roll": (240, 100)}
PR = 16

def rig(d, xr, kind, f_read, alpha=1.0, lab=None, vlab=None, roll_dx=0.0, n_wt=0):
    c = lambda col: A(col, alpha)
    card(d, (40, 270, 1040, 720), fill=c(WHITE), outline=c(LIGHT), w=3)
    d.rectangle([40, SURF, 1040, SURF + 40], fill=c(WOOD)); d.line([(40, SURF), (1040, SURF)], fill=c(WOOD_D), width=4)
    bw, bh = DIMS[kind]; lift = 2 * PR if kind == "roll" else 0
    xl = xr - bw; yb = SURF - lift
    if kind == "roll":
        for px in (xl + 45, xr - 45):
            cx = px - roll_dx / 2; cy = SURF - PR
            d.ellipse([cx - PR, cy - PR, cx + PR, cy + PR], fill=c(PENCIL), outline=c(PENCIL_D), width=3)
            ang = -roll_dx / 2 / PR
            d.line([(cx, cy), (cx + PR * math.sin(ang), cy - PR * math.cos(ang))], fill=c(PENCIL_D), width=3)
    for j in range(n_wt):
        yy = yb - bh - (j + 1) * 46
        d.rounded_rectangle([xl + 60, yy, xr - 60, yy + 42], radius=8, fill=c(WT), outline=c(NAVY), width=3)
    d.rounded_rectangle([xl, yb - bh, xr, yb], radius=10, fill=c(BOX), outline=c(BOX_D), width=4)
    if lab: text(d, ((xl + xr) / 2, yb - bh / 2), lab, 56, INK, alpha=alpha)
    hy = yb - 45
    Q = lambda s, h=0.0: (xr + s, hy + h)
    d.line([Q(0), Q(ROPE - 13)], fill=c(NAVY), width=5)
    se = luc_ke(d, Q, ROPE, ROPE + 20, ROPE + 20 + BODY, FMAX, f_read, nho=0.1, so=(0, 1, 2, 3, 4), hw=44, ben=-1,
                co=55, alpha=alpha)
    d.line([Q(se - 16), Q(se + 12)], fill=c(NAVY), width=8)
    hx, hy2 = Q(se + 40); d.ellipse([hx - 28, hy2 - 28, hx + 28, hy2 + 28], fill=c(SKIN), outline=c(SKIN_D), width=3)
    if vlab:
        s, L = vlab; y = 330; x0 = xl
        arrow(d, (x0, y), (x0 + L, y), c(PURPLE), w=7, head=20)
        text(d, (x0 + L + 16, y), s, 55, PURPLE, anchor="lm", alpha=alpha)
    return hx + 28

# ---------------- cot so sanh ----------------
CX = [190, 420, 650, 880]; BASE = 1380; SP = 300
def chart(d, hs, hl=(), top=840):
    card(d, (40, top, 1040, 1560), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, top + 60), "Số chỉ lực kế (N)", 55, INK, anchor="lm")
    d.line([(90, BASE), (1010, BASE)], fill=NAVY, width=4)
    for i, (lab, f, kind, v) in enumerate(CASES):
        g = hs[i]; h = f * SP * g; cx = CX[i]
        col = ORANGE if i < 3 else TEAL
        if i in hl:
            x0, x1 = (740, 1030) if i == 3 else (cx - 100, cx + 100)
            d.rounded_rectangle([x0, BASE - f * SP - 100, x1, BASE + 8], radius=18, outline=DRED, width=6)
        if h > 2: d.rectangle([cx - 60, BASE - h, cx + 60, BASE], fill=col)
        if g > 0.97:
            if i == 3: text(d, (1022, BASE - h - 46), rd(f), 55, DTEAL, anchor="rm")
            else: text(d, (cx, BASE - h - 46), rd(f), 55, DORANGE)
        for j, ln in enumerate(lab.split("\n")): text(d, (cx, BASE + 60 + 58 * j), ln, 55, INK)

def readout(d, s, y=780, alpha=1.0):
    card(d, (W / 2 - 200, y - 46, W / 2 + 200, y + 46), fill=A((254, 242, 242), alpha), outline=A(RED, alpha), r=24, w=4)
    text(d, (W / 2, y), s, 60, RED, alpha=alpha)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, XR0, "roll", None, lab="0,40 kg")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 790 + (1 - a) * 30
    card(d, (40, y0, 1040, y0 + 760), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    for j, s1 in enumerate(("Hộp lăn trên bút chì.", "So với lúc trượt,", "số chỉ lực kế ra sao?")):
        text(d, (W / 2, y0 + 220 + j * 100), s1, 62, PURPLE if j == 2 else INK, alpha=a)
    seg_bar(d, y0 + 600, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (4 lan keo deu) ----------------
FADE, T_READ, T_BAR, BAR_D = 0.3, 0.6, 1.4, 0.5
def do_state(t, M):
    k = max(0, sum(1 for m in M if t >= m) - 1); tk = t - M[k]
    lab, f, kind, v = CASES[k]
    xr = XR0 + v * max(0.0, tk)
    al = appear(tk, 0.0, FADE) if k > 0 else 1.0
    read = rd(f) if tk >= T_READ else "…"
    hs = [1.0 if i < k else (ease((tk - T_BAR) / BAR_D) if i == k else 0.0) for i in range(4)]
    return k, xr, f, al, read, hs

def s_do(img, d, t, sc):
    M = sc["M"]; k, xr, f, al, read, hs = do_state(t, M)
    lab, _, kind, v = CASES[k]
    vl = ("nhanh hơn", 200) if v > 30 else ("chậm", 80)
    rig(d, xr, kind, f, alpha=al, vlab=vl, roll_dx=xr - XR0)
    readout(d, read, alpha=al)
    chart(d, hs)

def _kiem_dong_bo():
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; M = sc["M"]; t = 0.0; bad = []
    while t < sc["T"]:
        k, xr, f, al, read, hs = do_state(t, M)
        if read != "…" and read != rd(f): bad.append((round(t, 2), "o so != kim"))
        if hs[k] > 0 and read == "…": bad.append((round(t, 2), "cot truoc so"))
        hx = xr + ROPE + 20 + BODY + 30 + 40 + 28
        if 65 + 0.88 * hx > 1045: bad.append((round(t, 2), "tay sat mep", round(hx)))
        t += 0.05
    if T_BAR + BAR_D + 0.3 > sc["T"] - M[3]: bad.append("cot lan chua moc xong")
    return bad

# ---------------- canh 3: Dap an + Rut ra ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    chart(d, [1, 1, 1, 1], hl=(3,))
    card(d, (40, 280, 1040, 400), fill=(220, 252, 231), outline=GREEN, w=5)
    text(d, (W / 2, 340), "Lăn: nhỏ hơn rất nhiều", 60, DGREEN)
    kr = appear(t, M[1], 0.45)
    if kr > 0:
        y0 = 440 + (1 - kr) * 20
        card(d, (40, y0, 1040, y0 + 360), fill=A(WHITE, kr), outline=A(GREEN, kr), w=6)
        pill(d, W / 2, y0 + 62, "RÚT RA", GREEN, kr)
        text(d, (W / 2, y0 + 170), "Trượt: cùng 1,2 N.", 58, DORANGE, alpha=kr)
        text(d, (W / 2, y0 + 270), "Lăn: dưới 0,1 N.", 58, DTEAL, alpha=kr)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k3 = appear(t, M[2] - 0.1, 0.45); a1 = 1 - k3
    kv = appear(t, M[1], 0.4)
    chart(d, [1, 1, 1, 1], hl=(0, 2) if kv > 0.5 and k3 < 0.5 else ())
    if a1 > 0:
        card(d, (40, 280, 1040, 760), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, W / 2, 350, "BẪY", DRED, a1)
        ks = clamp((t - M[0] - 1.2) / 0.4)
        for j, q in enumerate(("“Kéo nhanh thì ma sát lớn hơn”",)):
            f = F(58); lw = tw(d, q, f); yy = 490 + j * 85
            text(d, (W / 2, yy), q, 58, mix(RED, GRAY, ks), alpha=a1)
            if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
        if kv > 0:
            text(d, (W / 2, 640), "Cùng 1,2 N", 58, DGREEN, alpha=kv * a1)
    if k3 > 0:
        card(d, (40, 280, 1040, 640), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, 350, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, 520), "Mặt bàn ướt thì sao?", 58, INK, alpha=k3)

# ---------------- canh 5: Thu nghi ----------------
def s_end(img, d, t, sc):
    k = appear(t, 0.15, 0.4)
    card(d, (40, 300, 1040, 1300), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 375, "THỬ NGHĨ", ORANGE, k)
    d.rectangle([90, 760, 990, 790], fill=A(WOOD, k))
    d.rounded_rectangle([200, 640, 440, 760], radius=10, fill=A(BOX, k), outline=A(BOX_D, k), width=4)
    d.rounded_rectangle([260, 594, 380, 636], radius=8, fill=A(WT, k), outline=A(NAVY, k), width=3)
    text(d, (320, 700), "0,50 kg", 56, INK, alpha=k)
    arrow(d, (450, 700), (620, 700), A(RED, k), w=8, head=24)
    text(d, (650, 700), "?", 72, RED, anchor="lm", alpha=k)
    text(d, (W / 2, 890), "Thêm 0,10 kg, cùng mặt bàn.", 60, INK, alpha=k)
    text(d, (W / 2, 985), "Trượt đều: lực kế", 60, INK, alpha=k)
    text(d, (W / 2, 1075), "chỉ khoảng bao nhiêu?", 60, DORANGE, alpha=k)
    seg_bar(d, 1170, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return ([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.6, "ding")]
            + [(do["t0"] + m, "tap") for m in do["M"]]
            + [(da["t0"] + 0.1, "ding"), (da["t0"] + da["M"][1], "tap"), (b["t0"] + b["M"][0] + 1.2, "buzz"),
               (b["t0"] + b["M"][2] - 0.1, "tap"), (e["t0"] + 0.15, "open")])

CLIP = dict(id="tn-l10-luc-ma-sat-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Lực ma sát · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Trượt hay lăn?", draw=s_hook, tail=0.2, caps=[
   ("Hộp gỗ trên hai bút chì.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Kéo đều bốn lần", draw=s_do, tail=0.4, caps=[
   ("Hộp nằm, kéo chậm.", 3.0),
   ("Dựng đứng hộp.", 3.0),
   ("Hộp nằm, kéo nhanh hơn.", 3.0),
   ("Kê lên hai bút chì.", 3.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.5, caps=[
   ("Kim gần như không nhích.", 3.8),
   ("So bốn cột.", 3.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 3.4),
   ("Hai cột như nhau.", 3.4),
   ("Chưa nói được.", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 6.4)]),
])

if __name__ == "__main__" and "--kiem-dong-bo" in __import__("sys").argv:
    print("lệch:", _kiem_dong_bo() or "không")
