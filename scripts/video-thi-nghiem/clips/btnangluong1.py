# Clip: tn-l11-baitapnangluong-01 - Do co nang con lac lo xo treo theo bien do
# (31/10/2026; dung lai 27/11/2026 theo cong moi: --do-chu 0 LOI, chu >= 56 px khi ve, K10, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-baitapnangluong-01.json (_kiem_so() doi chieu):
#   m = 0,25 kg ; dan 5,0 cm -> k = 49 N/m ; A 1..4 cm (buoc 0,5). so_lieu_mau (A cm, v_max cm/s, 1/2 m v^2 mJ, 1/2 k A^2 mJ):
#   1 13,5 2,3 2,45 ; 2 27,5 9,5 9,8 ; 3 41,5 21,5 22,05 ; 4 55,0 37,8 39,2 (clip dung 4 hang, bo 1,5 cm cho gon).
# Du doan (giu, = dong "Nhin vao" cua hop thi nghiem): A tang 1 -> 4 cm, W gap may lan? -> khoang 16 (37,8 / 2,3).
# Bay = hien_tuong_hay_sai[1]: the A bang cm vao 1/2 k A^2 roi ghi J (1/2*49*2^2 = 98 "J" thay vi 9,8 mJ).
# Thu nghi (= cau_chot khung web; DOI 27/11: ca cu "W gap doi -> A gap can 2" gan dap an D cua quiz mo bai):
#   DOI LAN 2 (cong B): khong ghi san W = 1/2 kA^2, khong lap canh Bay. The du kien "Do: A = 2,0 cm thi W = 9,5 mJ"; keo A = 2,5 cm
#   -> W ti le A^2: 9,5 . 1,25^2 = 14,8 ~ 15 mJ (mo hinh 15,3). Dap so KHONG hien tren man.
from engine import *

M_KG, K_, DL = 0.25, 49.0, 5.0
ROWS = [(1, "1", "13,5", "2,3"), (2, "2", "27,5", "9,5"), (3, "3", "41,5", "21,5"), (4, "4", "55,0", "37,8")]

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-baitapnangluong-01.json")))
    tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert tp["m"]["gia_tri"] == M_KG and abs(M_KG * 9.8 / (DL / 100) - K_) < 1e-9
    h = {r[0]: r for r in k["so_lieu_mau"]["hang"]}
    for a, _, v, w in ROWS:
        assert h[a][1] == float(v.replace(",", ".")) and h[a][2] == float(w.replace(",", ".")), a
    assert h[2][3] == 9.8 and tp["A"]["min"] <= 2.5 <= tp["A"]["max"]
    assert abs(0.5 * K_ * 0.025 ** 2 * 1000 - 15.3) < 0.02                       # cau chot (mo hinh)
    assert round(h[2][2] * (2.5 / 2) ** 2) == 15                                  # cau chot (tu so do 9,5 mJ)
    assert abs(0.5 * K_ * 2 ** 2 - 98) < 1e-9                                    # bay
_kiem_so()

DBLUE = (29, 78, 216); DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8)
CED = (37, 99, 235); BLOCK = (250, 204, 120); EMPTY = (148, 140, 128)

def eq(d, cx, cy, s, size, color=INK, alpha=1.0, anchor="m"):
    """Chuoi cong thuc: _{..} chi so duoi (>= 56 px)."""
    fs = []
    for p in [p for p in re.split(r"(_\{[^}]*\})", s) if p]:
        if p.startswith("_{"): fs.append((p[2:-1], F(max(56, size * 0.7)), size * 0.24))
        else: fs.append((p, F(size), 0))
    tot = sum(tw(d, p, f) for p, f, _ in fs)
    x = cx - tot / 2 if anchor == "m" else (cx - tot if anchor == "r" else cx)
    for p, f, dy in fs:
        dtext(d, (x, cy + dy), p, f, color, alpha, "lm"); x += tw(d, p, f)
    return tot

def seg_bar(d, y, t, t0, t1, col, a=1.0, x0=170, n=5):
    p = clamp((t - t0) / (t1 - t0)); on = n - int(p * n + 1e-9)
    for i in range(n):
        x = x0 + i * 152
        if i < on: card(d, (x, y, x + 130, y + 70), fill=A(col, a), r=16)
        else: card(d, (x, y, x + 130, y + 70), fill=A(WHITE, a), outline=A(EMPTY, a), r=16, w=4)

def pill(d, cy, s, col, a=1.0, size=56):
    pw = tw(d, s, F(size)) + 64
    card(d, (W / 2 - pw / 2, cy - 40, W / 2 + pw / 2, cy + 40), fill=A(col, a), r=40)
    text(d, (W / 2, cy), s, size, WHITE, alpha=a)

def dashed(d, p0, p1, col, w=4, on=16, off=12):
    L = math.dist(p0, p1)
    if L < 1: return
    n = int(L // (on + off)) + 1
    for i in range(n):
        a = i * (on + off) / L; b = min(1, (i * (on + off) + on) / L)
        if a >= 1: break
        d.line([(p0[0] + (p1[0] - p0[0]) * a, p0[1] + (p1[1] - p0[1]) * a),
                (p0[0] + (p1[0] - p0[0]) * b, p0[1] + (p1[1] - p0[1]) * b)], fill=col, width=w)

def coil(d, x, ya, yb, amp=24, n=11, col=NAVY, w=5):
    e = 14; pts = [(x, ya), (x, ya + e)]; L = (yb - e) - (ya + e)
    for i in range(1, 2 * n): pts.append((x + (amp if i % 2 else -amp), ya + e + L * i / (2 * n)))
    pts += [(x, yb - e), (x, yb)]
    d.line(pts, fill=col, width=w, joint="curve")

# ---------------- lo xo treo + thuoc (0 o VTCB, x huong xuong) ----------------
HX, TOPY, VY, PXC = 230, 290, 640, 40            # truc lo xo, moc treo, tam vat o VTCB, px/cm
def hanging(d, x_cm, amax=None):
    d.rectangle([90, TOPY - 24, 400, TOPY], fill=GRAY, outline=NAVY, width=3)
    yc = VY + x_cm * PXC
    coil(d, HX, TOPY, yc - 50)
    d.rounded_rectangle([HX - 60, yc - 50, HX + 60, yc + 50], radius=12, fill=BLOCK, outline=NAVY, width=4)
    rx = 340
    d.rectangle([rx, VY - 4 * PXC - 14, rx + 30, VY + 4 * PXC + 14], fill=(250, 240, 200), outline=NAVY, width=2)
    for k in range(-4, 5):
        d.line([(rx, VY + k * PXC), (rx + (26 if k % 2 == 0 else 14), VY + k * PXC)], fill=NAVY, width=3)
    dashed(d, (HX + 64, VY), (rx - 4, VY), GRAY, w=4, on=10, off=8)
    text(d, (rx + 50, VY), "0", 56, INK, anchor="lm")
    if amax:
        for s_ in (-1, 1):
            y = VY + s_ * amax * PXC
            d.line([(rx - 30, y), (rx + 40, y)], fill=ORANGE, width=6)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    hanging(d, 0.0)
    for j, (a_cm, col) in enumerate(((1, CED), (4, ORANGE))):
        x0 = 580 + j * 300
        d.line([(x0, VY), (x0, VY + a_cm * PXC)], fill=col, width=8)
        for yy in (VY, VY + a_cm * PXC): d.line([(x0 - 18, yy), (x0 + 18, yy)], fill=col, width=8)
        text(d, (x0, VY + 4 * PXC + 70), f"A = {a_cm} cm", 56, col)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1000 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 560), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 190), "Cùng lò xo, A từ 1 cm lên 4 cm.", 56, INK, alpha=a)
    text(d, (W / 2, y0 + 300), "Cơ năng gấp mấy lần?", 64, PURPLE, alpha=a)
    seg_bar(d, y0 + 430, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: bon lan tha, bang ----------------
RT = [2.0, 4.0, 6.0, 8.0]                       # luc hien tung hang (vat vua qua VTCB lan dau)
TX = [580, 780, 960]; TY0 = 500
def s_do(img, d, t, sc):
    i = min(3, int(t // 2.0)) if t < 8.0 else 3
    a_cm = ROWS[i][0]
    t0 = i * 2.0
    u = t - t0
    if u < 0.6: x = a_cm * ease(u / 0.6)                    # keo xuong toi A
    else: x = a_cm * math.cos(2 * math.pi * (u - 0.6) / 1.4)
    hanging(d, x, amax=a_cm)
    card(d, (470, 280, 1050, 500 + 3 * 90 + 50), fill=WHITE, outline=NAVY, r=20, w=3)
    eq(d, TX[0], 320, "A", 56, INK); eq(d, TX[1], 320, "v_{max}", 56, INK); eq(d, TX[2], 320, "W", 56, INK)
    for cx, u_ in zip(TX, ("cm", "cm/s", "mJ")): text(d, (cx, 395), u_, 56, INK)
    d.line([(480, 435), (1040, 435)], fill=NAVY, width=3)
    for r, (av, al, v, w) in enumerate(ROWS):
        if t < RT[r]: continue
        k = appear(t, RT[r], 0.3)
        for cx, s_, col in zip(TX, (al, v, w), (INK, DBLUE, DORANGE)): text(d, (cx, TY0 + r * 90), s_, 58, col, alpha=k)
    card(d, (60, 1000, 1020, 1260), fill=(240, 244, 255), r=22)
    text(d, (W / 2, 1065), "Dãn 5,0 cm: k = 49 N/m", 58, INK)
    eq(d, W / 2, 1190, "W = ½mv_{max}²", 62, DBLUE)
    pw = tw(d, "quay 240 hình/s", F(56)) + 56
    card(d, (60, 1330, 60 + pw, 1410), fill=ORANGE, r=40); text(d, (60 + pw / 2, 1370), "quay 240 hình/s", 56, WHITE)

# ---------------- canh 3: Dap an (do thi W theo A) ----------------
GX0, GY0, GSX, GSY = 200, 1000, 190, 16.0          # goc do thi; px/cm; px/mJ
def s_dapan(img, d, t, sc):
    M = sc["M"]
    d.line([(GX0, GY0), (GX0 + 4.4 * GSX, GY0)], fill=INK, width=4)
    d.line([(GX0, GY0), (GX0, GY0 - 42 * GSY)], fill=INK, width=4)
    for v in (0, 2, 4): text(d, (GX0 + v * GSX, GY0 + 50), str(v), 56, INK)
    for v in (20, 40): text(d, (GX0 - 20, GY0 - v * GSY), str(v), 56, INK, anchor="rm")
    text(d, (GX0 + 4.4 * GSX, GY0 + 130), "A (cm)", 56, INK, anchor="rm")
    text(d, (GX0 + 30, GY0 - 42 * GSY + 10), "W (mJ)", 56, INK, anchor="lm")
    pts = [(GX0 + a * GSX, GY0 - 0.5 * K_ * (a / 100) ** 2 * 1000 * GSY) for a in [i / 20 for i in range(0, 87)]]
    for p0, p1 in zip(pts[::2], pts[1::2]): d.line([p0, p1], fill=GRAY, width=4)
    for av, _, _, w in ROWS:
        wv = float(w.replace(",", "."))
        d.ellipse([GX0 + av * GSX - 14, GY0 - wv * GSY - 14, GX0 + av * GSX + 14, GY0 - wv * GSY + 14], fill=DORANGE)
    k2 = appear(t, 2.3, 0.4)
    if k2 > 0: text(d, (W / 2, 1150), "37,8 : 2,3 ≈ 16", 64, DBLUE, alpha=k2)
    kp = appear(t, M[1] - 0.1, 0.4)
    if kp > 0: pill(d, 1300, "ĐÁP ÁN · khoảng 16 lần", NAVY, kp, size=58)

# ---------------- canh 4: Bay (don vi) ----------------
def s_bay(img, d, t, sc):
    kc = appear(t, 3.4, 0.5)
    hanging(d, 2.0, amax=2.0)
    text(d, (560, VY + 40), "A = 2 cm", 60, DORANGE, anchor="lm")
    y0 = 980
    card(d, (40, y0, 1040, y0 + 560), fill=WHITE, outline=DRED, w=6)
    pill(d, y0 + 70, "BẪY", DRED)
    s1 = "✗ ½ · 49 · 2² = 98 J"
    lw = tw(d, s1, F(60))
    text(d, (W / 2, y0 + 200), s1, 60, DRED)
    if kc > 0:
        d.line([(W / 2 - lw / 2, y0 + 202), (W / 2 - lw / 2 + lw * kc, y0 + 202)], fill=(140, 15, 15), width=7)
        text(d, (W / 2, y0 + 320), "✓ A = 0,02 m", 60, DGREEN, alpha=kc)
        text(d, (W / 2, y0 + 420), "W = 0,0098 J = 9,8 mJ", 60, DGREEN, alpha=kc)
        text(d, (W / 2, y0 + 500), "(mô hình)", 56, MUTED, alpha=kc)

# ---------------- canh 5: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    hanging(d, 3.0 * math.exp(-0.35 * t) * math.cos(2 * math.pi * t / 1.4))
    card(d, (40, 1000, 1040, 1340), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 1085), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 1230), "Nếu có lực cản?", 62, INK)

# ---------------- canh 6: THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, 290, "THỬ NGHĨ", ORANGE, k1)
    card(d, (80, 380, 1000, 500), fill=A((239, 246, 255), k1), r=20)
    text(d, (W / 2, 440), "Đo: A = 2,0 cm thì W = 9,5 mJ", 56, DBLUE, alpha=k1)
    kq = appear(t, 2.2, 0.45)
    if kq > 0:
        text(d, (W / 2, 700), "Kéo tới A = 2,5 cm rồi thả.", 62, INK, alpha=kq)
        text(d, (W / 2, 810), "Cơ năng khoảng bao nhiêu mJ?", 62, DORANGE, alpha=kq)
        seg_bar(d, 960, t, 2.8, sc["T"] - 0.2, ORANGE, kq)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open")] + [(do["t0"] + r, "tick") for r in RT] + [
            (da["t0"] + da["M"][1] - 0.1, "ding"), (b["t0"] + 0.3, "buzz"), (e["t0"] + 2.2, "open")]

CLIP = dict(id="tn-l11-baitapnangluong-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Bài tập năng lượng · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Lò xo treo, hai biên độ", draw=s_hook, tail=0.3, caps=[
   ("Cùng lò xo, hai biên độ.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Bốn lần thả", draw=s_do, tail=0.3, caps=[
   ("Thả từ A, đo tốc độ qua VTCB.", 4.4),
   ("Mỗi lần một hàng.", 4.2)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.2, caps=[
   ("So hàng 4 cm với hàng 1 cm.", 4.0),
   ("Đường đứt là mô hình.", 3.0)]),
 dict(key="bay", title="Bẫy: đơn vị", draw=s_bay, tail=0.3, caps=[
   ("Để nguyên cm là sai.", 3.4),
   ("Đổi A ra mét trước.", 3.2)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("Số đo hơi thấp hơn mô hình.", 4.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.2, caps=[
   ("Đổi biên độ.", 3.0),
   ("Dừng lại, tự tính.", 4.8)]),
])
