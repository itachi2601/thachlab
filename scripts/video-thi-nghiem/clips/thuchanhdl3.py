# Clip: tn-l10-thuchanhdl-03 - Bang dem khi nghieng nhe lam lech toc do do duoc (31/10/2026; dung lai 27/11/2026
# theo cong moi L10b: chu >= 55 px khi ve, nhip >= 2,5 s, K10 khong nut A-D, chot A-D o khung).
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-thuchanhdl-03.json (_kiem_so() doi chieu):
#   tham_so: L = 1,20 m ; v cong 1 = 0,505 m/s ; x = 0,300 m (dai 0,1-0,6) ; h = 2/4/6 mm (max 8)
#   so_lieu_mau: h 2/4/6 mm -> a 0,0163/0,0327/0,049 ; v_that 0,5146/0,524/0,5333 m/s ; ket_qua_ky_vong lech 1,9/3,8/5,6 %
# Doc bang ve DUNG ti le that (6 mm tren 1,20 m ~ 4,6 px) -> nhin nhu phang; do cao h hien qua kinh lup.
# Du doan (K10): ke 6 mm, cong 1 chi 0,505 m/s -> cong 2 (cach 0,30 m) chi khoang? Dap an 0,533 m/s.
#   Khung: A. Van 0,505 ; B. Khoang 0,51 ; C. Khoang 0,53 (DUNG) ; D. Khoang 0,60 m/s.
#   (Bai co vi du h = 2 mm -> ~2 % va dong "Nhin vao: lech bao nhieu %"; Du doan dung 6 mm, hoi so do.)
# Ket qua: cot lech 1,9/3,8/5,6 % theo h ; xuong doc nen nhanh dan.
# Bay = hien_tuong_hay_sai[0] o h = 2 mm (cap so khac Du doan): "khong dang ke" -> lech 1,9 % ; kem cach kiem
#   (hien_tuong_hay_sai[1]): tha xe dung yen, xe troi -> chinh chan vit. Chua noi duoc: ma sat, suc can (gia_thiet bo qua).
# Cau chot (ca tu suy theo mo_hinh kho, x trong dai 0,1-0,6): ke 4 mm, cong 2 doi xa x = 0,60 m ->
#   v = sqrt(0,505^2 + 2.0,0327.0,60) = 0,542 m/s -> lech ~ 7,4 % (gan gap doi 3,8 %). Khong hien tren man.
from engine import *

X0, X1 = 80, 1000
PXM = (X1 - X0) / 1.2                 # px / m doc bang ; mp4 x = 65 + 0,88 x
G1, G2, XE2 = 0.40, 0.70, 0.78
CW = 0.12
V1 = 0.505
DATA = {2: (0.0163, 0.5146, 1.9), 4: (0.0327, 0.524, 3.8), 6: (0.049, 0.5333, 5.6)}   # h: (a, v_that, lech %)
CHOT = (4, 0.60)                                                                     # h, x ; dap so lech ~ 7,4 %
RAIL = (148, 163, 184); RAIL_D = (100, 116, 139); LCD = (134, 239, 172)
NOTE = (60, 64, 84); DGREEN = (21, 110, 55); DRED = (185, 28, 28); EMPTY = (148, 140, 128)
def vn(x, n): return f"{x:.{n}f}".replace(".", ",")
def sx(s): return X0 + s * PXM

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l10-thuchanhdl-03.json")))
    for h, a, v, l in k["so_lieu_mau"]["hang"]:
        assert DATA[h][:2] == (a, v) and abs(DATA[h][2] - l) < 0.05, ("lech kho", h)
    assert "+1,9 %; +3,8 %; +5,6 %" in k["ket_qua_ky_vong"]
    ts = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert ts["v_cong"]["gia_tri"] == V1 and ts["L"]["gia_tri"] == 1.2 and ts["x"]["min"] <= CHOT[1] <= ts["x"]["max"]
    v = math.sqrt(V1 ** 2 + 2 * DATA[CHOT[0]][0] * CHOT[1]); assert round((v / V1 - 1) * 100, 1) == 7.4
_kiem_so()

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

def lift_px(h): return h / 1000 * PXM
def ty(yb, h, s): return yb - lift_px(h) * (1 - s / 1.2)          # dau trai ke cao

def cart(d, yb, h, s, col=ORANGE, flag=True):
    x = sx(s); y = ty(yb, h, s); w = CW * PXM / 2
    if flag: d.rectangle([x - 6, y - 110, x + 6, y - 70], fill=NAVY)
    d.rounded_rectangle([x - w, y - 74, x + w, y - 4], radius=12, fill=col, outline=NAVY, width=3)

def gate_back(d, yb, h, s):
    x = sx(s); y = ty(yb, h, s)
    for dx in (-30, 30): d.line([(x + dx, y + 36), (x + dx, y - 150)], fill=NAVY, width=7)
def gate_front(d, yb, h, s):
    x = sx(s); y = ty(yb, h, s)
    d.line([(x - 34, y - 150), (x + 34, y - 150)], fill=NAVY, width=9)
    dot(d, x - 30, y - 90, 8, RED); dot(d, x + 30, y - 90, 8, RED)

def track(d, yb, h, k=1.0):
    floor = yb + 92
    d.line([(50, floor), (1030, floor)], fill=A(INK, k), width=4)
    for s in (0.06, 1.14):
        x = sx(s); yt = ty(yb, h, s) + 28; raised = s < 0.6
        bot = floor - (lift_px(h) if raised else 0)
        d.rectangle([x - 14, yt, x + 14, bot], fill=A(RAIL_D, k))
        if raised and h > 0: d.rectangle([x - 26, bot, x + 26, floor], fill=A(ORANGE, k))
    top = [(X0, ty(yb, h, 0)), (X1, ty(yb, h, 1.2))]
    d.polygon(top + [(X1, top[1][1] + 28), (X0, top[0][1] + 28)], fill=A(RAIL, k), outline=A(NAVY, k))
    for i in range(1, 46):
        s = i * 1.2 / 46; dot(d, sx(s), ty(yb, h, s) + 9, 3, A(RAIL_D, k))

def display(d, x, y, lab, val, hi=False):
    text(d, (x, y - 80), lab, 56, INK)
    card(d, (x - 150, y - 44, x + 150, y + 44), fill=NAVY, r=14)
    text(d, (x, y), val + (" m/s" if val[0].isdigit() else ""), 56, YELLOW if hi else LCD)

def magnifier(d, cx, cy, h, yb):
    """Kinh lup phong to chan trai (12 px/mm): tam dem day h."""
    lx = sx(0.06)
    d.line([(lx, yb + 92), (cx + 40, cy - 104)], fill=NOTE, width=3)
    d.ellipse([cx - 115, cy - 115, cx + 115, cy + 115], fill=WHITE, outline=NOTE, width=5)
    fl = cy + 58; hp = h * 12
    d.line([(cx - 100, fl), (cx + 100, fl)], fill=INK, width=4)
    if hp > 0: d.rectangle([cx - 58, fl - hp, cx + 58, fl], fill=ORANGE)
    d.rectangle([cx - 26, cy - 92, cx + 26, fl - hp], fill=RAIL_D)
    text(d, (cx + 140, cy), f"h = {h} mm", 60, ORANGE, anchor="lm")

def rig(d, h, s, r1, r2, hi2=False, g2=G2, xlab="x = 0,30 m", xe2=True):
    """Hinh trong the y 265-1000: bang that ti le, hai cong, hai dong ho, kinh lup."""
    card(d, (40, 265, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    yb = 600
    display(d, sx(G1) - 40, 420, "cổng 1", r1)
    display(d, min(sx(g2) + 40, 870), 420, "cổng 2", r2, hi=hi2)
    track(d, yb, h)
    gate_back(d, yb, h, G1); gate_back(d, yb, h, g2)
    if xe2: cart(d, yb, h, XE2 + CW / 2, col=GRAY, flag=False)
    cart(d, yb, h, s)
    gate_front(d, yb, h, G1); gate_front(d, yb, h, g2)
    y = 745
    d.line([(sx(G1), y), (sx(g2), y)], fill=INK, width=3)
    for xx in (sx(G1), sx(g2)): d.line([(xx, y - 14), (xx, y + 14)], fill=INK, width=3)
    text(d, ((sx(G1) + sx(g2)) / 2 + 40, y + 50), xlab, 56, INK)
    text(d, (1010, 955), "băng dài 1,20 m", 56, NOTE, bold=False, anchor="rm")
    magnifier(d, 170, 870, h, yb)

# ---------------- canh 1: Du doan (K10) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    s = lerp(0.12, 0.52, ease((t - 0.5) / 1.8))
    rig(d, 6, s, "0,505" if s >= G1 else "– – –", "?")
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1035 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 200), "Cổng 2 chỉ khoảng", 64, INK, alpha=a)
    text(d, (W / 2, y0 + 290), "bao nhiêu m/s?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 410, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: Tien hanh (3 lan chay) ----------------
R0, RUN, SLOW, S0, SEND = 0.5, 2.5, 1.5, 0.10, XE2 - CW / 2
HS = (2, 4, 6)
def kin(h):
    """u: thoi gian that tu luc qua cong 1. -> (u0, u2, uend) ung s = S0, G2, SEND."""
    a = DATA[h][0]
    def u_at(s): return (-V1 + math.sqrt(V1 * V1 + 2 * a * (s - G1))) / a
    return u_at(S0), u_at(G2), u_at(SEND)
def run_state(t):
    i = int(clamp((t - R0) // RUN, 0, 2)) if t >= R0 else 0
    h = HS[i]; a = DATA[h][0]
    u0, u2, ue = kin(h)
    u = min(u0 + clamp(t - R0 - i * RUN, 0, 99) / SLOW, ue)
    s = G1 + V1 * u + a * u * u / 2
    r1 = "0,505" if u >= 0 else "– – –"
    r2 = vn(DATA[h][1], 3) if u >= u2 else "– – –"
    rows = i + (1 if u >= u2 else 0) if t >= R0 else 0
    return i, h, s, r1, r2, rows

XS = (200, 540, 870)
def table(d, rows, y0=1035, hl=None):
    card(d, (40, y0, 1040, y0 + 545), fill=WHITE, outline=LIGHT, w=3)
    for x, a_, b_ in zip(XS, ("h", "cổng 1", "cổng 2"), ("mm", "m/s", "m/s")):
        text(d, (x, y0 + 60), a_, 60, INK); text(d, (x, y0 + 125), b_, 56, NOTE, bold=False)
    d.line([(70, y0 + 170), (1010, y0 + 170)], fill=LIGHT, width=3)
    for j in range(rows):
        h = HS[j]; yy = y0 + 245 + j * 100
        if hl == j: d.rounded_rectangle([60, yy - 46, 1020, yy + 46], radius=20, fill=(255, 247, 237))
        text(d, (XS[0], yy), str(h), 60, ORANGE)
        text(d, (XS[1], yy), "0,505", 60, NAVY)
        text(d, (XS[2], yy), vn(DATA[h][1], 3), 60, NAVY)

def s_do(img, d, t, sc):
    i, h, s, r1, r2, rows = run_state(t)
    rig(d, h, s, r1, r2, hi2=r2[0] != "–")
    table(d, rows, hl=i if t >= R0 else None)

def _kiem_dong_bo():
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; bad = []
    for h in HS:
        u0, u2, ue = kin(h)
        if (ue - u0) * SLOW > RUN - 0.3: bad.append(("luot dai", h))
    if R0 + 3 * RUN > sc["T"] + 0.3: bad.append("lan cuoi sat cuoi canh")
    return bad

# ---------------- canh 3: Ket qua ----------------
def s_kq(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 620), fill=WHITE, outline=LIGHT, w=3)
    text(d, (80, 325), "Kê 6 mm", 56, ORANGE, anchor="lm")
    display(d, 290, 500, "cổng 1", "0,505")
    display(d, 790, 500, "cổng 2", vn(DATA[6][1], 3), hi=True)
    ka = appear(t, M[1] - 0.1, 0.45)
    if ka > 0:
        card(d, (40, 660, 1040, 1300), fill=A(WHITE, ka), outline=A(LIGHT, ka), w=3)
        text(d, (W / 2, 725), "độ lệch", 56, INK, alpha=ka)
        by0, by1 = 840, 1160
        def yv(v): return by1 - v / 6 * (by1 - by0)
        d.line([(120, by1), (960, by1)], fill=A(INK, ka), width=4)
        for j, h in enumerate(HS):
            g = ease((t - M[1] - 0.2 - 0.4 * j) / 0.5); cx = 280 + j * 260; v = DATA[h][2]
            if g > 0: d.rectangle([cx - 65, yv(v * g), cx + 65, by1], fill=ORANGE if h == 6 else (253, 186, 116))
            if g > 0.95: text(d, (cx, yv(v) - 40), f"{vn(v, 1)} %", 56, INK)
            text(d, (cx, by1 + 60), f"{h} mm", 56, ORANGE, alpha=ka)
    kb = appear(t, M[2] - 0.1, 0.45)
    if kb > 0:
        card(d, (40, 1340, 1040, 1560), fill=A((236, 253, 243), kb), outline=A(GREEN, kb), w=5)
        text(d, (W / 2, 1450), "xuống dốc: xe nhanh dần", 62, DGREEN, alpha=kb)

# ---------------- canh 4: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.3, 0.45)
    card(d, (40, 265, 1040, 600), fill=A(WHITE, a1), outline=A(RED, a1), w=6)
    pill(d, W / 2, 335, "BẪY", RED, a1)
    q = "“Kê 2 mm, không đáng kể”"
    ks = clamp((t - M[1]) / 0.4); lw = tw(d, q, F(62)); yy = 470
    text(d, (W / 2, yy), q, 62, mix(INK, DRED, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(RED, 0.85 * a1), width=6)
    kk = appear(t, M[1] + 0.1, 0.45)
    if kk > 0:
        card(d, (40, 640, 1040, 1230), fill=A(WHITE, kk), outline=A(NAVY, kk), w=5)
        text(d, (W / 2, 715), f"2 mm → lệch {vn(DATA[2][2], 1)} %", 62, DRED, alpha=kk)
        text(d, (W / 2, 815), "thả xe đứng yên", 58, INK, alpha=kk)
        yb = 1030; h = 2; a = DATA[h][0]
        tt = clamp(t - M[1] - 0.5, 0, 99); s = min(0.40 + 16 * a * tt * tt / 2, 0.66)     # tua nhanh
        track(d, yb, h, kk); cart(d, yb, h, s, flag=False)
        if tt > 0.8:
            x = sx(s) - 50; y = ty(yb, h, s) - 120
            arrow(d, (x, y), (x + 100, y), DGREEN, w=7, head=20)
            text(d, (x + 120, y), "trôi", 56, DGREEN, anchor="lm")
    k5 = appear(t, M[2] + 0.1, 0.45)
    if k5 > 0:
        y0 = 1270 + (1 - k5) * 30
        card(d, (40, y0, 1040, y0 + 290), fill=A(WHITE, k5), outline=A(NAVY, k5), w=6)
        pill(d, W / 2, y0 + 70, "CHƯA NÓI ĐƯỢC", NAVY, k5)
        text(d, (W / 2, y0 + 200), "ma sát, sức cản", 60, INK, alpha=k5)

# ---------------- canh 5: THU NGHI (cau chot o khung web: lech ~ 7,4 %) ----------------
def s_end(img, d, t, sc):
    M = sc["M"]; h, x = CHOT
    rig(d, h, 0.30, "– – –", "?", g2=G1 + x, xlab="x = 0,60 m", xe2=False)
    y0 = 1035
    card(d, (40, y0, 1040, 1670), fill=WHITE, outline=ORANGE, w=6)
    pill(d, W / 2, y0 + 70, "THỬ NGHĨ", ORANGE)
    k1 = appear(t, 2.6, 0.45)
    text(d, (W / 2, y0 + 185), "Cổng 1 vẫn 0,505 m/s.", 60, INK, alpha=k1)
    k2 = appear(t, 5.0, 0.45)
    text(d, (W / 2, y0 + 285), "Cổng 2 lệch khoảng mấy %?", 62, ORANGE, alpha=k2)
    seg_bar(d, y0 + 350, t, 5.2, sc["T"] - 0.2, ORANGE, k2)
    kh = appear(t, 7.5, 0.45)
    if kh > 0:
        card(d, (90, y0 + 445, 990, y0 + 620), fill=A((255, 247, 237), kh), r=24)
        text(d, (W / 2, y0 + 490), "Gợi ý", 56, INK, alpha=kh)
        text(d, (W / 2, y0 + 570), "tìm gia tốc xe trước", 58, (176, 64, 8), alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, kq, b, e = sc["hook"], sc["do"], sc["kq"], sc["bay"], sc["end"]
    out = [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding")]
    for i in range(3):
        u0, u2, _ = kin(HS[i])
        out.append((do["t0"] + R0 + i * RUN + (u2 - u0) * SLOW, "tap"))
    return out + [(kq["t0"] + 0.4, "ding"), (b["t0"] + b["M"][1], "buzz"), (e["t0"] + 5.0, "open")]

CLIP = dict(id="tn-l10-thuchanhdl-03", header="VẬT LÍ 10 · THỰC HÀNH", footer="Thực hành động lượng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Băng đệm khí kê một đầu", draw=s_hook, tail=0.3, caps=[
   ("Kê một đầu cao 6 mm.", 3.4),
   ("Dừng lại, tự đoán.", 5.5)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Cổng 2 đặt ở chỗ va chạm.", 3.4),
   ("Kê cao dần: 2, 4, 6 mm.", 3.6)]),
 dict(key="kq", title="Kết quả", draw=s_kq, tail=0.3, caps=[
   ("Đáp án: cổng 2 chỉ 0,533 m/s.", 3.2),
   ("Kê càng cao, lệch càng lớn.", 3.4),
   ("Vì sao cổng 2 nhanh hơn?", 3.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 3.0),
   ("Sai: cỡ sai số đo.", 4.0),
   ("Thí nghiệm này còn thiếu gì?", 3.2)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.5, caps=[
   ("Dời cổng 2 ra xa.", 2.8),
   ("Dừng lại, tự tính.", 6.6)]),
])

if __name__ == "__main__" and "--kiem" in __import__("sys").argv:
    print("đồng bộ:", _kiem_dong_bo() or "không lệch")
