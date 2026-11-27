# Clip: tn-l10-giaibt-dlh-02 - He xe lan va qua nang noi day qua rong roc (30/10/2026; cong moi 27/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-giaibt-dlh-02.json:
#   tham_so: m1 = 0,40 kg (0,1-1,0), m2 = 0,10 kg, s = 0,8 m, g = 10 (mo_hinh.gia_thiet), sai_so_do t = 0,02 s
#   so_lieu_mau: t = 0,93 / 0,95 / 0,92 / 0,94 / 0,93 s -> a = 1,85 / 1,77 / 1,89 / 1,81 / 1,85 m/s2;
#   du doan bo ma sat 2,0 m/s2; trung binh ~ 1,83 (ket_qua_ky_vong). mo_hinh: T = m2.(g - a).
# Du doan (27/11): bang duoi clip + Bam xem cua bai da tra loi "a do nho hon 2,0 ca 5 lan" -> KHONG hoi nua.
#   Hoi: giu xe dung yen thi day cang T = m2.g = 1,0 N; tha ra, T lon hon hay nho hon? Dap an: nho hon, T = m2(g - a)
#   ~ 0,1.(10 - 1,83) ~ 0,8 N (qua nang tang toc di xuong: hop luc huong xuong). Mui ten T : P2 ve ti le 0,8 : 1,0.
#   Loi kho: "cho rang luc cang day bang trong luong qua nang (T = m2.g)".
# Bay: "so do sai vi khong ra 2,0" (loi kho: quen ma sat roi cho rang so do 'sai').
# Cau chot: xe 0,90 kg (trong mien m1), qua nang 0,10 kg, bo ma sat -> a = 0,1.10/1,0 = 1,0 m/s2. Dap so khong hien.
from engine import *

DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)
WOOD = (176, 124, 74); WOOD_D = (140, 96, 54); STEEL = (90, 98, 120)
T_RUN = 0.93                       # s, lan 1 (so_lieu_mau)
SLOW = 3.0                         # chieu cham 3 lan
ROWS = [(1, 0.93, 1.85), (2, 0.95, 1.77), (3, 0.92, 1.89), (4, 0.94, 1.81), (5, 0.93, 1.85)]   # so_lieu_mau
def vn(x, n=2): return f"{x:.{n}f}".replace(".", ",")

def rig(d, x0, y0, k, s, gate=True, clock=None, done=False, labels=True, m1="0,40 kg"):
    """Ban + xe + rong roc + qua nang. (x0, y0) = mep trai mat ban; k = ti le; s = 0..1 phan quang duong 0,80 m."""
    D = 560 * k                                     # 0,80 m tren man
    xp, yp, rp = x0 + 830 * k, y0 - 30 * k, 30 * k  # rong roc kep mep ban
    d.rectangle([x0, y0, x0 + 820 * k, y0 + 30 * k], fill=WOOD, outline=WOOD_D, width=3)
    d.rectangle([x0 + 812 * k, y0 - 6 * k, x0 + 840 * k, y0 + 40 * k], fill=STEEL)          # kep
    d.line([(x0 + 826 * k, y0 - 4 * k), (xp, yp)], fill=STEEL, width=max(3, int(8 * k)))
    cx = x0 + 20 * k + D * s                         # mep sau xe
    cw, ch = 150 * k, 60 * k
    hook_y = y0 - 60 * k
    # day: xe -> dinh rong roc -> xuong qua nang
    my = y0 + 40 * k + D * s
    d.line([(cx + cw, hook_y), (xp, hook_y)], fill=INK, width=3)
    d.line([(xp + rp, yp), (xp + rp, my)], fill=INK, width=3)
    d.ellipse([xp - rp, yp - rp, xp + rp, yp + rp], fill=WHITE, outline=STEEL, width=max(3, int(6 * k)))
    dot(d, xp, yp, 5 * k + 2, STEEL)
    # xe lan
    card(d, (cx, y0 - 28 * k - ch, cx + cw, y0 - 28 * k), fill=BLUE, outline=NAVY, r=int(10 * k), w=3)
    for wx in (cx + 32 * k, cx + cw - 32 * k):
        dot(d, wx, y0 - 14 * k, 14 * k, NAVY); dot(d, wx, y0 - 14 * k, 5 * k, LIGHT)
    # qua nang
    mw, mh = 70 * k, 80 * k
    card(d, (xp + rp - mw / 2, my, xp + rp + mw / 2, my + mh), fill=ORANGE, outline=(160, 60, 10), r=int(10 * k), w=3)
    if labels:
        text(d, (cx + cw / 2, y0 + 30 * k + 45), m1, 55, BLUE)
        text(d, (xp + rp - mw / 2 - 18, my + mh / 2), "0,10 kg", 55, DORANGE, anchor="rm")
    if gate:
        g0, g1 = x0 + 170 * k, x0 + 170 * k + D          # vach xuat phat (mui xe) va cong quang o 0,80 m
        for yy in range(int(y0 - 120 * k), int(y0 - 4), 22):
            d.line([(g0, yy), (g0, yy + 11)], fill=GRAY, width=4)
        d.rectangle([g1 - 8, y0 - 150 * k, g1 + 8, y0 - 2], fill=RED)
        d.rectangle([g1 - 30, y0 - 160 * k, g1 + 30, y0 - 130 * k], fill=RED)
        ya = y0 - 190 * k
        arrow(d, (g0 + 40, ya), (g0 + 4, ya), INK, w=4, head=16); arrow(d, (g1 - 40, ya), (g1 - 4, ya), INK, w=4, head=16)
        d.line([(g0 + 40, ya), (g1 - 40, ya)], fill=INK, width=4)
        d.rectangle([(g0 + g1) / 2 - 110, ya - 34, (g0 + g1) / 2 + 110, ya + 34], fill=WHITE)
        text(d, ((g0 + g1) / 2, ya), "0,80 m", 55, INK)
    if clock is not None:
        bx = (180, y0 + 220 * k, 640, y0 + 340 * k)
        card(d, bx, fill=(236, 253, 243) if done else (255, 247, 237), outline=GREEN if done else ORANGE, r=24, w=4)
        text(d, ((bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2), f"t = {vn(clock)} s", 58, GREEN if done else INK)

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

def geo(x0, y0, k):
    xp, yp, rp = x0 + 830 * k, y0 - 30 * k, 30 * k
    return xp + rp, y0 + 40 * k, 80 * k          # x day treo, dinh qua nang, cao qua nang (s = 0)

# ---------------- canh 1: Du doan ----------------
HX, HY, HK = 90, 600, 0.95
def s_hook(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    rig(d, HX, HY, HK, 0.0, gate=False)
    cx = HX + 20 * HK
    card(d, (cx - 70, HY - 120, cx - 6, HY - 20), fill=(253, 230, 200), outline=DORANGE, r=20, w=4)   # tay giu xe
    text(d, (cx + 80, HY - 170), "Giữ xe", 55, DORANGE)
    mx, mt, mh = geo(HX, HY, HK)
    g = ease(clamp((t - 0.6) / 1.4)); L = 150 * g
    arrow(d, (mx, mt), (mx, mt - L - 1), TEAL, w=8, head=20)
    arrow(d, (mx, mt + mh), (mx, mt + mh + L + 1), BLUE, w=8, head=20)
    text(d, (mx - 40, mt - 190), "T = 1,0 N", 55, TEAL, anchor="rm")
    text(d, (mx - 40, mt + mh + 140), "P₂ = 1,0 N", 55, BLUE, anchor="rm")
    text(d, (300, 330), "T: lực căng dây", 55, TEAL)
    text(d, (300, 920), "P₂: trọng lực", 55, BLUE)
    k = appear(t, M[1] - 0.2, 0.5)
    if k <= 0: return
    y0 = 1085 + (1 - k) * 30
    card(d, (40, y0, 1040, y0 + 500), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pill(d, W / 2, y0 + 70, "DỰ ĐOÁN", PURPLE, k)
    for j, s1 in enumerate(("Thả ra:", "T lớn hơn hay nhỏ hơn 1,0 N?")):
        text(d, (W / 2, y0 + 190 + j * 85), s1, 60, PURPLE if j == 1 else INK, alpha=k)
    seg_bar(d, y0 + 400, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, k)

# ---------------- canh 2: Tien hanh ----------------
def run_start(sc): return sc["M"][0] + 0.6
def real_t(t, sc): return clamp((t - run_start(sc)) / SLOW, 0, T_RUN)

PY0, PY1 = 1150, 1590
def ya(v): return PY1 - 80 - (v - 1.70) / (2.05 - 1.70) * (PY1 - PY0 - 150)
def aplot(d, n, kl=1.0):
    card(d, (40, PY0, 1040, PY1), fill=WHITE, outline=LIGHT, w=3)
    text(d, (1010, PY0 + 45), "a (m/s²)", 55, INK, anchor="rm")
    d.line([(190, ya(1.70)), (190, ya(2.05))], fill=INK, width=3)
    d.line([(190, ya(1.70)), (900, ya(1.70))], fill=INK, width=3)
    for v in (1.7, 1.8, 1.9):
        d.line([(180, ya(v)), (200, ya(v))], fill=INK, width=3)
        text(d, (170, ya(v)), vn(v, 1), 55, INK, anchor="rm")
    y2 = ya(2.0)
    text(d, (170, y2), "2,0", 55, DRED, anchor="rm")
    for xx in range(200, 880, 36):
        d.line([(xx, y2), (xx + 20, y2)], fill=RED, width=5)
    text(d, (1010, y2), "tính", 55, DRED, anchor="rm")
    text(d, (1010, ya(1.70) + 45), "lần đo", 55, INK, anchor="rm")
    for j in range(n):
        x = 300 + j * 120; a = ROWS[j][2]
        dot(d, x, ya(a), 17, BLUE)
        text(d, (x, ya(1.70) + 45), str(j + 1), 55, INK)

def s_do(img, d, t, sc):
    M = sc["M"]
    tr = real_t(t, sc); s = (tr / T_RUN) ** 2                 # tu nghi: x = a t^2 / 2
    done = tr >= T_RUN - 1e-6; n = 1 if done else 0; clk = tr
    if t > M[1] + 0.1:                                       # lan 2-5 tua nhanh: moi lan 0,7 s
        j = min(3, int((t - M[1] - 0.1) / 0.7)); p = clamp((t - M[1] - 0.1 - 0.7 * j) / 0.55)
        s = p ** 2; clk = ROWS[j + 1][1] * p; done = p >= 1; n = 1 + j + (1 if done else 0)
    card(d, (40, 265, 1040, 1135), fill=WHITE, outline=LIGHT, w=3)
    rig(d, 80, 540, 0.88, s, clock=clk, done=done)
    k = 1 - appear(t, run_start(sc) + 0.4, 0.3)
    if k > 0:
        card(d, (400, 880, 720, 980), fill=A(ORANGE, k), r=40)
        text(d, (560, 930), "Thả!", 58, WHITE, alpha=k)
    text(d, (300, 1060), "chậm ×3" if t <= M[1] else "tua nhanh", 55, MUTED)
    aplot(d, n)

# ---------------- canh 3: Dap an (qua nang tach rieng) ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    mx, my = 420, 640                                     # tam qua nang
    d.line([(mx, 300), (mx, my - 70)], fill=INK, width=3)
    card(d, (mx - 60, my - 70, mx + 60, my + 70), fill=ORANGE, outline=(160, 60, 10), r=14, w=3)
    text(d, (mx, my), "m₂", 55, WHITE)
    g1 = ease(clamp((t - 0.4) / 1.2))
    arrow(d, (mx + 90, my + 70), (mx + 90, my + 70 + 260 * g1 + 1), BLUE, w=9, head=22)    # P2 = 1,0 N -> 260 px
    text(d, (mx + 130, my + 280), "P₂ = 1,0 N", 55, BLUE, anchor="lm", alpha=appear(t, 0.4, 0.4))
    arrow(d, (200, 560), (200, 560 + 200 * g1 + 1), PURPLE, w=7, head=20)
    text(d, (200, 820), "gia tốc a", 55, PURPLE, alpha=appear(t, 0.4, 0.4))
    kt = appear(t, M[1], 0.4); g2 = ease(clamp((t - M[1]) / 1.0))
    for yy in range(int(my - 70 - 260), int(my - 70), 24):                               # moc 1,0 N (net dut)
        d.line([(mx + 90, yy), (mx + 90, yy + 12)], fill=A(GRAY, kt), width=5)
    if g2 > 0:
        arrow(d, (mx + 90, my - 70), (mx + 90, my - 70 - 208 * g2 - 1), TEAL, w=9, head=22)  # T = 0,8 N -> 208 px
    text(d, (mx + 130, my - 250), "T ≈ 0,8 N", 55, TEAL, anchor="lm", alpha=kt)
    text(d, (mx + 130, my - 340), "1,0 N", 55, GRAY, anchor="lm", alpha=kt)
    ka = appear(t, M[1], 0.45)
    if ka <= 0: return
    yk = 1085 + (1 - ka) * 30
    card(d, (40, yk, 1040, yk + 400), fill=A(WHITE, ka), outline=A(NAVY, ka), w=6)
    pill(d, W / 2, yk + 70, "ĐÁP ÁN", NAVY, ka)
    text(d, (W / 2, yk + 195), "T nhỏ hơn, ≈ 0,8 N", 64, BLUE, alpha=ka)
    text(d, (W / 2, yk + 300), "T = m₂(g − a)", 58, DGREEN, alpha=ka)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 265, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    x0, y0, k = 90, 640, 0.95
    rig(d, x0, y0, k, 0.1, gate=False, labels=False)
    D = 560 * k; cx = x0 + 20 * k + D * 0.1; cw = 150 * k
    xp, yp, rp = x0 + 830 * k, y0 - 30 * k, 30 * k
    kf = appear(t, M[1], 0.4)
    for wx in (cx + 32 * k, cx + cw - 32 * k):                              # vong do o truc banh, rong roc
        d.ellipse([wx - 26, y0 - 14 * k - 26, wx + 26, y0 - 14 * k + 26], outline=A(RED, kf), width=6)
    d.ellipse([xp - rp - 14, yp - rp - 14, xp + rp + 14, yp + rp + 14], outline=A(RED, kf), width=6)
    arrow(d, (cx + 130, y0 + 100), (cx + 130 - 120 * ease(clamp((t - M[1]) / 0.8)) - 1, y0 + 100), A(RED, kf), w=7, head=18)
    text(d, (cx + 170, y0 + 100), "lực cản", 55, DRED, anchor="lm", alpha=kf)
    k1 = appear(t, 0.4, 0.45)
    card(d, (40, 1030, 1040, 1590), fill=A(WHITE, k1), outline=A(GREEN, k1), w=6)
    pill(d, W / 2, 1100, "RÚT RA", GREEN, k1)
    text(d, (W / 2, 1210), "T = m₁a ;  m₂g − T = m₂a", 58, INK, alpha=k1)
    text(d, (W / 2, 1310), "a = m₂g/(m₁ + m₂) = 2,0 m/s²", 58, DGREEN, alpha=k1)
    k2 = appear(t, M[1], 0.45)
    text(d, (W / 2, 1420), "a đo ≈ 1,83 m/s²", 60, DRED, alpha=k2)
    text(d, (W / 2, 1510), "đo nhỏ hơn: có lực cản", 55, DRED, alpha=k2)

# ---------------- canh 5: Bay + chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    a1 = appear(t, 0.15, 0.4); y0 = 265
    card(d, (40, y0, 1040, 1590), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
    pill(d, W / 2, y0 + 70, "BẪY", DRED, a1)
    q = "Số đo sai"
    ks = clamp((t - M[1]) / 0.4); yy = 450; lw = tw(d, q, F(60))
    text(d, (W / 2, yy), q, 60, mix(INK, GRAY, ks), alpha=a1)
    if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
    kk = appear(t, M[1], 0.4); g = ease(clamp((t - M[1]) / 1.2))
    BX, SCB = 330, 270                                   # 1 m/s2 -> 300 px
    for i, (lb, v, col) in enumerate((("tính", 2.0, GRAY), ("đo", 1.83, BLUE))):
        y = 640 + i * 150
        text(d, (90, y), lb, 58, col, anchor="lm", alpha=kk)
        d.rounded_rectangle([BX, y - 40, BX + SCB * v * g + 1, y + 40], radius=14, fill=A(col, kk))
        if g > 0.95: text(d, (BX + SCB * v + 20, y), vn(v, 2 if i else 1), 55, col, anchor="lm", alpha=kk)
    text(d, (W / 2, 960), "2,0 bỏ ma sát", 60, DGREEN, alpha=kk)
    k3 = appear(t, M[2] - 0.1, 0.4)
    if k3 > 0:
        yk = 1100 + (1 - k3) * 30
        card(d, (40, yk, 1040, yk + 440), fill=A(WHITE, k3), outline=A(NAVY, k3), w=6)
        pill(d, W / 2, yk + 70, "CHƯA NÓI ĐƯỢC", NAVY, k3)
        text(d, (W / 2, yk + 200), "Cản ở bánh xe", 58, INK, alpha=k3)
        text(d, (W / 2, yk + 300), "hay ở ròng rọc?", 58, INK, alpha=k3)

# ---------------- canh 6: Thu nghi ----------------
def s_end(img, d, t, sc):
    k = 1.0
    card(d, (40, 265, 1040, 1000), fill=WHITE, outline=LIGHT, w=3)
    s = 0.3 * ease(clamp((t - 0.4) / 3.5))
    rig(d, 90, 640, 0.95, s, gate=False, m1="0,90 kg")
    card(d, (40, 1030, 1040, 1585), fill=A(WHITE, k), outline=A(ORANGE, k), w=6)
    pill(d, W / 2, 1100, "THỬ NGHĨ", ORANGE, k)
    text(d, (W / 2, 1215), "Xe 0,90 kg, bỏ ma sát.", 58, INK, alpha=k)
    text(d, (W / 2, 1310), "Gia tốc a bao nhiêu?", 60, DORANGE, alpha=k)
    seg_bar(d, 1420, t, 1.0, sc["T"] - 0.2, ORANGE, k)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = (sc[k] for k in ("hook", "do", "dapan", "rutra", "bay", "end"))
    return [(h["t0"] + h["M"][1] - 0.2, "open"),
            (do["t0"] + run_start(do), "tap"), (do["t0"] + run_start(do) + T_RUN * SLOW, "tap"),
            (da["t0"] + da["M"][1], "ding"), (r["t0"] + r["M"][1], "tap"),
            (b["t0"] + b["M"][1], "buzz"), (e["t0"] + 0.15, "open")]

CLIP = dict(id="tn-l10-giaibt-dlh-02", header="VẬT LÍ 10 · THÍ NGHIỆM", footer="Giải bài toán động lực học · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Xe lăn và quả nặng", draw=s_hook, tail=0.2, caps=[
   ("Giữ xe đứng yên, dây căng.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Thả từ nghỉ, chiếu chậm 3 lần.", 4.0),
   ("Làm 5 lần, tính a = 2s/t².", 3.8)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.3, caps=[
   ("Quả nặng tăng tốc đi xuống.", 3.4),
   ("Đáp án: T nhỏ hơn, ≈ 0,8 N.", 3.8)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.3, caps=[
   ("Định luật II cho từng vật.", 3.4),
   ("Đo nhỏ hơn: có lực cản.", 3.4)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Số đo sai?", 3.0),
   ("Không, 2,0 bỏ ma sát.", 3.0),
   ("Cản ở đâu?", 3.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Dừng lại, tự trả lời.", 5.6)]),
])
