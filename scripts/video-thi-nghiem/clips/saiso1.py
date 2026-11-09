# Clip: tn-l10-sai-so-01 - Bam gio 10 dao dong con lac don, 5 lan (9/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l10-sai-so-01.json:
#   so_lieu_mau: t = 20,19; 19,85; 20,14; 19,94; 20,23 s ; Δt_i = 0,12; 0,22; 0,07; 0,13; 0,16 s ; t̄ = 20,07 s.
#   tham_so: l = 1,000 m (min 0,5 m), DCNN dong ho 0,01 s ; buoc: lech khoang 5°.
# Cau 2 ngay SAU hop trong bai hoi Δt (dap an 0,15; nhieu 0,14 / 0,70 / 0,22) -> clip KHONG tinh Δt, de "= ?",
#   khong hien 0,14 / 0,15 / 0,75 %, khong neu "lay do lech lon nhat" (bay cua Cau 2).
# Khac saiso2 (thuoc + phong to + δA): o day con lac + dong ho + bang 5 lan + truc thoi gian cham diem.
# Canh: Du doan (5 so do lech nhau co bao nhieu, K10: chi cau hoi + hinh) -> Bam gio 5 lan (bang + cham tren truc)
#       -> Lay trung binh (t̄, cot Δt_i, Δt = ?) -> Chua noi duoc gi -> Bay (dong ho 0,01 s nen sai so 0,01 s)
#       -> Chot + cau hoi (day 0,5 m, chua tung hien).
from engine import *

T_DO = [20.19, 19.85, 20.14, 19.94, 20.23]
D_I = ["0,12", "0,22", "0,07", "0,13", "0,16"]
TBAR = 20.07
DRED = (185, 28, 28)
BOB = (234, 88, 12)
def vn(x): return f"{x:.2f}".replace(".", ",")
def tbar_text(d, cx, cy, s, size, color, alpha=1.0, anchor="mm"):
    """Ve chuoi bat dau bang 't' roi ke gach ngang tren chu t (dau macron ghep cua font SF lech trai)."""
    f = F(size); text(d, (cx, cy), s, size, color, anchor=anchor, alpha=alpha)
    l, tp, r, b = d.textbbox((cx, cy), s, font=f, anchor=anchor)
    tl, tt, tr, tb_ = d.textbbox((l, tp), "t", font=f, anchor="lt")
    d.line([(tl + 1, tt - size * 0.12), (tr + 2, tt - size * 0.12)], fill=A(color, alpha), width=max(3, size // 14))
def rich(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """Nhu engine.rich nhung chi so duoi 0,8 co (>= 36 px) de con doc duoc sau thu x0,88."""
    segs = []
    for p in [p for p in TOK.split(s) if p]:
        if p.startswith("_{"): segs.append((p[2:-1], max(36, int(size * 0.8)), size * 0.22))
        else: segs.append((p, size, 0))
    tot = sum(tw(d, t, F(sz)) for t, sz, _ in segs)
    x = cx - tot / 2 if anchor == "m" else cx
    for t, sz, dy in segs:
        dtext(d, (x, cy + dy), t, F(sz), color, alpha, "lm"); x += tw(d, t, F(sz))

# ---------- hinh dung chung ----------
def pendulum(d, px, py, L, ang_deg, alpha=1.0, lab=True):
    """Con lac don: diem treo (px, py), day L px, goc lech ang_deg (do)."""
    c = lambda col: A(col, alpha)
    d.rectangle([px - 90, py - 16, px + 90, py], fill=c(GRAY))
    a = math.radians(ang_deg); bx, by = px + L * math.sin(a), py + L * math.cos(a)
    yy = py                                              # duong thang dung net dut
    while yy < py + L:
        d.line([(px, yy), (px, min(yy + 14, py + L))], fill=c(LIGHT), width=3); yy += 26
    d.line([(px, py), (bx, by)], fill=c(NAVY), width=4)
    dot(d, bx, by, 26, c(BOB), outline=c((154, 52, 18)))
    if lab: text(d, (px - 30, py + L * 0.5), "1,000 m", 40, INK, anchor="rm", alpha=alpha)

def stopwatch(d, box, s, alpha=1.0, sub=None):
    x0, y0, x1, y1 = box; c = lambda col: A(col, alpha)
    card(d, box, fill=c(NAVY), r=30)
    card(d, (x0 + 24, y0 + 24, x1 - 24, y1 - (70 if sub else 24)), fill=c((222, 247, 236)), r=18)
    cy = (y0 + 24 + y1 - (70 if sub else 24)) / 2
    text(d, ((x0 + x1) / 2, cy), s, 84, NAVY, alpha=alpha)
    if sub: text(d, ((x0 + x1) / 2, y1 - 38), sub, 40, (200, 210, 235), alpha=alpha)

# truc thoi gian 19,8 .. 20,4 s
AX0, AX1, V0, V1 = 120, 960, 19.8, 20.4
def ax(v): return AX0 + (v - V0) / (V1 - V0) * (AX1 - AX0)
def axis(d, y, alpha=1.0):
    c = lambda col: A(col, alpha)
    d.line([(AX0 - 30, y), (AX1 + 30, y)], fill=c(INK), width=4)
    for v in (19.8, 20.0, 20.2, 20.4):
        d.line([(ax(v), y - 12), (ax(v), y + 12)], fill=c(INK), width=4)
        text(d, (ax(v), y + 50), vn(v)[:-1], 40, INK, alpha=alpha)
    text(d, (AX1 + 30, y - 46), "t (s)", 40, INK, anchor="rm", alpha=alpha)

def dots(d, y, ks, hl=None):
    """ks[i]: do hien cham lan i. hl: tap lan duoc to dam."""
    for i, k in enumerate(ks):
        if k <= 0: continue
        x = ax(T_DO[i]); col = DRED if (hl and i in hl) else BOB
        dot(d, x, y, 17, A(col, k))
        text(d, (x, y - 48), str(i + 1), 40, col, alpha=k)

# bang: cot Lan | t (s) | Δt_i (s)
TX = (190, 470, 800)
def table(d, y0, krow, kcol3=None, alpha=1.0):
    c = lambda col: A(col, alpha)
    rh = 66; h = 84 + rh * 5
    card(d, (60, y0, 1020, y0 + h), fill=c(WHITE), outline=c(NAVY), w=4, r=24)
    text(d, (TX[0], y0 + 44), "Lần", 40, MUTED, alpha=alpha)
    text(d, (TX[1], y0 + 44), "t (s)", 40, MUTED, alpha=alpha)
    if kcol3 is not None: rich(d, TX[2], y0 + 44, "Δt_{i} (s)", 40, MUTED, alpha=alpha * max(kcol3[0], 0))
    d.line([(90, y0 + 82), (990, y0 + 82)], fill=c(LIGHT), width=3)
    for i in range(5):
        yy = y0 + 84 + rh * i + rh / 2; k = krow[i]
        if k <= 0: continue
        text(d, (TX[0], yy), str(i + 1), 44, INK, alpha=k * alpha)
        text(d, (TX[1], yy), vn(T_DO[i]), 46, INK, alpha=k * alpha)
        if kcol3 is not None and kcol3[i + 1] > 0:
            text(d, (TX[2], yy), D_I[i], 46, PURPLE, alpha=kcol3[i + 1] * alpha)

# ---------------- canh 1: du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.1)
    sw = 6 * math.sin(2 * math.pi * t / 2.0) if t < M[1] - 0.4 else 5.0
    pendulum(d, 250, 300, 430, sw, alpha=a)
    stopwatch(d, (480, 380, 1010, 640), "?", alpha=appear(t, 0.5), sub="chia 0,01 s")
    k = appear(t, M[1] - 0.4, 0.5)
    if k <= 0: return
    y0 = 830 + (1 - k) * 30
    card(d, (60, y0, 1020, y0 + 560), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    pw = tw(d, "Dự đoán", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(PURPLE, k), r=32)
    text(d, (W / 2, y0 + 60), "Dự đoán", 40, WHITE, alpha=k)
    ctext(d, y0 + 170, "Bấm giờ 10 dao động, đo 5 lần.", 46, INK, alpha=k)
    ctext(d, y0 + 300, "5 số đo lệch nhau", 50, INK, alpha=k)
    ctext(d, y0 + 370, "cỡ bao nhiêu giây?", 50, INK, alpha=k)
    t1, t2 = M[1] - 0.2, sc["T"] - 0.2; q = clamp((t - t1) / (t2 - t1))
    d.rounded_rectangle([200, y0 + 480, 880, y0 + 496], radius=8, fill=A(LIGHT, k))
    if q < 1: d.rounded_rectangle([200, y0 + 480, 200 + 680 * (1 - q), y0 + 496], radius=8, fill=A(PURPLE, k))

# ---------------- canh 2: bam gio 5 lan ----------------
RUN0, RUND, RUNC = 0.9, 1.4, 1.0      # lan i bat dau RUN0 + i*RUND, dong ho chay RUNC s
AXY_DO = 1330
def run_state(t):
    """(lan dang/da bam, so dong ho, do hien tung hang)."""
    ks = [appear(t, RUN0 + i * RUND + RUNC, 0.3) for i in range(5)]
    i = int(clamp((t - RUN0) / RUND, 0, 4.999)) if t >= RUN0 else -1
    if i < 0: return -1, 0.0, ks
    q = clamp((t - (RUN0 + i * RUND)) / RUNC)
    return i, T_DO[i] * q, ks

def s_do(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.1)
    pendulum(d, 210, 290, 250, 6 * math.sin(2 * math.pi * t / 0.9), alpha=a, lab=False)
    i, v, ks = run_state(t)
    stopwatch(d, (400, 290, 1010, 560), vn(v) + " s" if i >= 0 else "0,00 s", alpha=a,
              sub=(f"lần {i + 1} · tua nhanh" if i >= 0 else "tua nhanh"))
    table(d, 610, ks)
    axis(d, AXY_DO, alpha=appear(t, 0.5))
    kh = appear(t, M[2] + 0.3, 0.4)
    dots(d, AXY_DO - 70, ks, hl=({1, 4} if kh > 0 else None))
    if kh > 0:                                          # ngoac tu lan 2 (nho nhat) toi lan 5 (lon nhat)
        xa, xb, yb = ax(T_DO[1]), ax(T_DO[4]), AXY_DO + 110
        d.line([(xa, yb), (xb, yb)], fill=A(DRED, kh), width=5)
        for x in (xa, xb): d.line([(x, yb - 14), (x, yb + 14)], fill=A(DRED, kh), width=5)
    kb = appear(t, M[2] + 1.6, 0.4)
    if kb > 0:
        s_ = "ĐÁP ÁN · lệch vài phần mười giây"; pw = tw(d, s_, F(42)) + 70
        card(d, (W / 2 - pw / 2, 1500, W / 2 + pw / 2, 1596), fill=A((220, 252, 231), kb), outline=A(GREEN, kb), r=26, w=4)
        text(d, (W / 2, 1548), s_, 42, GREEN, alpha=kb)

# ---------------- canh 3: lay trung binh ----------------
def s_tb(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.1)
    card(d, (60, 270, 1020, 450), fill=A(WHITE, a), outline=A(BLUE, a), w=4)
    tbar_text(d, W / 2, 335, "t = 100,35 : 5 = 20,07 s", 52, BLUE, alpha=a)
    text(d, (W / 2, 405), "100,35 s: tổng 5 lần", 40, MUTED, alpha=a)
    yax = 670
    axis(d, yax, alpha=a)
    dots(d, yax - 70, [a] * 5)
    kl = appear(t, 0.6, 0.4)
    if kl > 0:                                          # vach trung binh net dut
        x = ax(TBAR); yy = yax - 160
        while yy < yax + 10:
            d.line([(x, yy), (x, min(yy + 16, yax + 10))], fill=A(BLUE, kl), width=5); yy += 28
        tbar_text(d, x + 14, yax - 180, "t", 44, BLUE, anchor="lm", alpha=kl)
    kc = [appear(t, M[1] - 0.1, 0.3)] + [appear(t, M[1] + 0.3 + 0.45 * i, 0.3) for i in range(5)]
    for i in range(5):                                  # doan lech tu cham toi vach t̄
        if kc[i + 1] <= 0: continue
        x0_, x1_ = sorted((ax(T_DO[i]), ax(TBAR)))
        d.line([(x0_, yax - 12 - 9 * i), (x1_, yax - 12 - 9 * i)], fill=A(PURPLE, kc[i + 1]), width=4)
    table(d, 790, [1] * 5, kcol3=kc, alpha=a)
    k3 = appear(t, M[2] - 0.05, 0.4)
    if k3 > 0:
        card(d, (260, 1260, 820, 1420), fill=A(WHITE, k3), outline=A(GREEN, k3), w=5)
        text(d, (W / 2 - 40, 1340), "Δt =", 54, GREEN, anchor="rm", alpha=k3)
        card(d, (W / 2 - 20, 1298, W / 2 + 80, 1382), fill=A((245, 243, 255), k3), outline=A(PURPLE, k3), r=18, w=3)
        text(d, (W / 2 + 30, 1340), "?", 54, PURPLE, alpha=k3)

# ---------------- canh 4: chua noi duoc gi ----------------
def s_gioihan(img, d, t, sc):
    k = appear(t, 0.05, 0.35); y1 = 290
    card(d, (60, y1, 1020, y1 + 900), fill=A(WHITE, k), outline=A(NAVY, k), w=6)
    text(d, (W / 2, y1 + 85), "Chưa nói được gì?", 54, NAVY, alpha=k)
    card(d, (110, y1 + 170, 970, y1 + 400), fill=A((239, 246, 255), k), r=24)
    ctext(d, y1 + 285, "Đếm nhầm dao động", 50, BLUE, alpha=k)
    card(d, (110, y1 + 440, 970, y1 + 670), fill=A((239, 246, 255), k), r=24)
    ctext(d, y1 + 555, "Góc lệch lớn", 50, BLUE, alpha=k)
    ctext(d, y1 + 790, "số liệu minh hoạ", 42, MUTED, bold=False, alpha=k)

# ---------------- canh 5: bay ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]; a = appear(t, 0.05, 0.3)
    card(d, (60, 270, 1020, 640), fill=A(WHITE, a), outline=A(DRED, a), w=6)
    pw = tw(d, "Bẫy", F(40)) + 60
    card(d, (W / 2 - pw / 2, 300, W / 2 + pw / 2, 364), fill=A(DRED, a), r=32)
    text(d, (W / 2, 332), "Bẫy", 40, WHITE, alpha=a)
    for j, q in enumerate(("Đồng hồ chia 0,01 s", "nên sai số cỡ 0,01 s")):
        yy = 450 + j * 80; f = F(50); lw = tw(d, q, f)
        text(d, (W / 2, yy), q, 50, DRED, alpha=a)
        ks = clamp((t - 0.9 - 0.25 * j) / 0.4)
        if ks > 0: d.line([(W / 2 - lw / 2 - 10, yy + 2), (W / 2 - lw / 2 - 10 + (lw + 20) * ks, yy + 2)], fill=DRED, width=7)
    text(d, (W / 2 + 400, 490), "✗", 70, DRED, alpha=appear(t, 1.3, 0.3))
    # thanh so sanh cung ti le: 1 s = 2800 px
    kb = appear(t, M[1] - 0.05, 0.4); S_ = 2800; x0 = 360
    if kb > 0:
        text(d, (90, 730), "ĐCNN đồng hồ", 40, INK, anchor="lm", alpha=kb)
        d.rectangle([x0, 790, x0 + 0.01 * S_, 840], fill=A(TEAL, kb))
        text(d, (x0 + 0.01 * S_ + 20, 815), "0,01 s", 42, TEAL, anchor="lm", alpha=kb)
        rich(d, 90, 920, "Độ lệch Δt_{i} của 5 lần", 40, INK, alpha=kb, anchor="l")
        for i in range(5):
            v = float(D_I[i].replace(",", ".")); yy = 980 + i * 64
            text(d, (x0 - 30, yy + 22), f"lần {i + 1}", 40, MUTED, anchor="rm", alpha=kb)
            d.rectangle([x0, yy, x0 + v * S_, yy + 44], fill=A(PURPLE, kb))
    kc = appear(t, M[1] + 2.0, 0.4)
    if kc > 0:
        ctext(d, 1400, "✓ Tay bấm lệch lớn hơn nhiều", 46, GREEN, alpha=kc)

# ---------------- canh 6: chot + cau hoi ----------------
def s_end(img, d, t, sc):
    def body(d, t, k):
        ka = appear(t, sc["M"][0] + 0.4, 0.5)
        ctext(d, 830, "Dây 0,5 m. Độ lệch do tay bấm\ncó nhỏ đi không?", 46, INK, maxw=900, alpha=ka)
        pendulum(d, 540, 1010, 200, 5 * math.sin(2 * math.pi * t / 1.4), alpha=ka, lab=False)
        text(d, (510, 1110), "0,5 m", 40, INK, anchor="rm", alpha=ka)
        kh = appear(t, sc["M"][0] + 2.9, 0.5)
        card(d, (110, 1300, 970, 1500), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1350, "Gợi ý", 40, MUTED, bold=False, alpha=kh)
        ctext(d, 1430, "Vì sao 5 số lệch nhau?", 42, ORANGE, maxw=820, alpha=kh)
    chot_hoi(d, t, sc, "Đo nhiều lần, lấy trung bình", "", body=body)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, b, e = sc["hook"], sc["do"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.4, "open"), (h["t0"] + h["T"] - 0.7, "ding")] + \
           [(do["t0"] + RUN0 + i * RUND + RUNC, "tap") for i in range(5)] + \
           [(do["t0"] + do["M"][2] + 1.6, "ding"), (b["t0"] + 0.9, "buzz"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l10-sai-so-01", header="VẬT LÍ 10 · THÍ NGHIỆM", cues=_cues,
    footer="Sai số phép đo · thachlab.id.vn", scenes=[
 dict(key="hook", title="Bấm giờ con lắc đơn", draw=s_hook, tail=0.4, caps=[
   ("Lệch 5° rồi thả.", 2.5),
   ("Dừng video, tự đoán.", 5.6)]),
 dict(key="do", title="Đo 5 lần", draw=s_do, tail=0.3, caps=[
   ("Đếm đủ 10 dao động.", 3.6),
   ("Tay bấm lúc sớm, lúc muộn.", 3.9),
   ("Nhỏ nhất 19,85; lớn nhất 20,23.", 3.5)]),
 dict(key="tb", title="Lấy trung bình", draw=s_tb, tail=0.3, caps=[
   ("Các số tản quanh trung bình.", 2.5),
   ("Mỗi lần lệch bao nhiêu?", 3.4),
   ("Em tự tính Δt.", 2.5)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.4, caps=[
   ("Hai nguồn sai chưa xét.", 4.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Có đúng không?", 2.5),
   ("So cùng tỉ lệ.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.6, caps=[
   ("Dừng video, tự trả lời.", 6.4)]),
])
