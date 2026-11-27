# Clip: tn-l11-tatdan-01 - Quet tan so luc cuong buc, doc bien do on dinh
# (9/11/2026; dung lai 27/11/2026 theo cong moi: --do-chu 0 LOI, chu >= 56 px khi ve, K10, cau chot A-D ra khung web).
# So lieu lay nguyen tu content/thi-nghiem/tn-l11-tatdan-01.json (_kiem_so() doi chieu):
#   f0 = 2,0 Hz ; f 0,5-3,5 Hz buoc 0,5 ; b = 0,5 Hz ; Ar = 6,0 cm ; sai so doc 0,2 cm.
#   so_lieu_mau (f, A lam tron): 1,0 2,7 ; 1,5 4,2 ; 2,0 6,0 ; 2,5 4,2 ; 3,0 2,7 (so minh hoa).
#   mo_hinh A(f) = Ar.b / sqrt((f - f0)^2 + b^2): net dut CHI ve 1,0-3,0 Hz (khong lo cau chot).
# Du doan (giu, = dong "Nhin vao" cua hop thi nghiem): quet f 1,0 -> 3,0 Hz, A on dinh doi the nao? -> tang roi giam.
# Bay = hien_tuong_hay_sai[0] "luc manh la cong huong": cung mo-to, chi doi f 1,0 -> 2,0 Hz: 2,7 -> 6,0 cm.
# Thu nghi (= cau_chot khung web): f = 3,5 Hz (max tham_so, chua hien) -> A ~ 1,9 cm (xa f0 hon 3,0 Hz nen < 2,7;
#   nhieu 1,2 cm = ngoai suy thang 4,2 -> 2,7 -> 1,2, nhung duong cong thoai dan xa f0).
#   Dap so KHONG hien tren man.
from engine import *

F0, AR, B, ERR = 2.0, 6.0, 0.5, 0.2
ROWS = [(1.0, 2.7), (1.5, 4.2), (2.0, 6.0), (2.5, 4.2), (3.0, 2.7)]
def amp(f): return AR * B / math.sqrt((f - F0) ** 2 + B * B)
def vn(v): return f"{v:.1f}".replace(".", ",")

def _kiem_so():
    import json
    k = json.load(open(os.path.join(HERE, "..", "..", "content", "thi-nghiem", "tn-l11-tatdan-01.json")))
    tp = {p["ky_hieu"]: p for p in k["tham_so"]}
    assert tp["f0"]["gia_tri"] == F0 and tp["Ar"]["gia_tri"] == AR and tp["b"]["mac_dinh"] == B and tp["sai_so"]["gia_tri"] == ERR
    assert [(r[0], r[2]) for r in k["so_lieu_mau"]["hang"]] == ROWS
    assert tp["f"]["max"] == 3.5 and abs(amp(3.5) - 1.9) < 0.01                # cau chot
_kiem_so()

DBLUE = (29, 78, 216); DRED = (185, 28, 28); DGREEN = (21, 110, 55); DORANGE = (176, 64, 8); EMPTY = (148, 140, 128)

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

# ---------------- mo-to + lo xo + vat + thuoc ----------------
MX, MY, YEQ, PX = 260, 320, 640, 22             # truc mo-to; tam vat o VTCB; px/cm
def spring_v(d, x, y0, y1, n=11, amp_=24, w=5):
    lead = 14; pts = [(x, y0), (x, y0 + lead)]; L = (y1 - lead) - (y0 + lead)
    for i in range(1, 2 * n): pts.append((x + (amp_ if i % 2 else -amp_), y0 + lead + L * i / (2 * n)))
    pts += [(x, y1 - lead), (x, y1)]
    d.line(pts, fill=NAVY, width=w, joint="curve")

def rig(d, ycm, phase, f=None):
    d.rectangle([60, MY - 70, 520, MY - 50], fill=(190, 195, 210), outline=NAVY, width=3)
    card(d, (MX - 80, MY - 50, MX + 80, MY + 10), fill=(205, 200, 190), outline=NAVY, r=10, w=3)
    d.ellipse([MX - 34, MY - 34, MX + 34, MY + 26], outline=NAVY, width=4)
    dot(d, MX + 22 * math.cos(phase), MY - 4 - 22 * math.sin(phase), 10, ORANGE)
    yb = YEQ + ycm * PX
    spring_v(d, MX, MY + 10, yb - 45)
    card(d, (MX - 55, yb - 45, MX + 55, yb + 45), fill=BLUE, outline=NAVY, r=12, w=4)
    rx = MX + 120
    d.rectangle([rx, YEQ - 7 * PX, rx + 40, YEQ + 7 * PX], fill=(253, 246, 200), outline=NAVY, width=3)
    for k in range(-7, 8):
        d.line([(rx, YEQ + k * PX), (rx + (24 if k % 2 == 0 else 12), YEQ + k * PX)], fill=NAVY, width=3)
    text(d, (rx + 60, YEQ), "0", 56, INK, anchor="lm")
    text(d, (rx + 60, YEQ - 6 * PX), "6 cm", 56, INK, anchor="lm")
    d.line([(MX + 58, yb), (rx - 4, yb)], fill=ORANGE, width=3)
    if f is not None:
        card(d, (640, 300, 1040, 420), fill=WHITE, outline=NAVY, r=20, w=4)
        text(d, (840, 360), "f = " + vn(f) + " Hz", 60, NAVY)

# ---------------- do thi A - f ----------------
GX0, GX1, GY0, GY1 = 210, 990, 960, 1400
def gx(f): return GX0 + (f - 0.5) / 3.25 * (GX1 - GX0)
def gy(a_): return GY1 - a_ / 7.0 * (GY1 - GY0)
def axes(d):
    d.line([(GX0, GY1), (GX1, GY1)], fill=INK, width=4)
    d.line([(GX0, GY1), (GX0, GY0 - 20)], fill=INK, width=4)
    for f in (1, 2, 3):
        d.line([(gx(f), GY1), (gx(f), GY1 + 14)], fill=INK, width=4)
        text(d, (gx(f), GY1 + 55), str(f), 56, INK)
    text(d, (GX1, GY1 + 120), "f (Hz)", 56, INK, anchor="rm")
    for a_ in (3, 6):
        d.line([(GX0 - 14, gy(a_)), (GX0, gy(a_))], fill=INK, width=4)
        text(d, (GX0 - 24, gy(a_)), str(a_), 56, INK, anchor="rm")
    text(d, (GX0 + 24, GY0 - 30), "A (cm)", 56, INK, anchor="lm")
def model(d, f1=1.0, f2=3.0, col=GRAY):
    pts = [(gx(f1 + (f2 - f1) * i / 80), gy(amp(f1 + (f2 - f1) * i / 80))) for i in range(81)]
    for p0, p1 in zip(pts[::2], pts[1::2]): d.line([p0, p1], fill=col, width=5)
def pt(d, f, a_, lab=False, a=1.0):
    dot(d, gx(f), gy(a_), 14, A(DORANGE, a))
    if lab: text(d, (gx(f), gy(a_) - 50), vn(a_), 56, DORANGE, alpha=a)

def osc(t, f, a_):                               # li do cm (quay cham x2), bien do lon dan toi on dinh
    return a_ * (1 - math.exp(-t / 0.5)) * math.sin(2 * math.pi * f * t / 2)

# ---------------- canh 1: Du doan ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, osc(t, 1.0, 2.7), 2 * math.pi * 1.0 * t / 2, f=None)
    card(d, (640, 300, 1040, 420), fill=WHITE, outline=NAVY, r=20, w=4)
    text(d, (840, 360), "f: 1,0 → 3,0 Hz", 56, NAVY)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 960 + (1 - a) * 30
    card(d, (50, y0, 1030, y0 + 600), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, y0 + 70, "DỰ ĐOÁN", PURPLE, a)
    text(d, (W / 2, y0 + 180), "Giữ lực, tăng f từ 1,0 lên 3,0 Hz.", 56, INK, alpha=a)
    text(d, (W / 2, y0 + 280), "Biên độ ổn định", 62, PURPLE, alpha=a)
    text(d, (W / 2, y0 + 360), "thay đổi thế nào?", 62, PURPLE, alpha=a)
    seg_bar(d, y0 + 470, t, M[1] + 0.4, sc["T"] - 0.3, PURPLE, a)

# ---------------- canh 2: quet 5 tan so ----------------
def s_do(img, d, t, sc):
    i = min(4, int(t // 2.0))
    f, a_ = ROWS[i]; u = t - 2.0 * i
    rig(d, osc(u, f, a_), 2 * math.pi * f * u / 2, f=f)
    pw = tw(d, "quay chậm ×2", F(56)) + 56
    card(d, (1040 - pw, 450, 1040, 530), fill=ORANGE, r=40); text(d, (1040 - pw / 2, 490), "quay chậm ×2", 56, WHITE)
    axes(d)
    for j, (fj, aj) in enumerate(ROWS):
        if t >= 2.0 * j + 1.5: pt(d, fj, aj, lab=t >= 2.0 * (j + 1) or (j == 4 and t >= 10.0))

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    axes(d)
    km = appear(t, 0.0, 0.3)
    for f, a_ in ROWS: pt(d, f, a_, lab=True)
    k2 = appear(t, 2.3, 0.4)
    if k2 > 0:
        model(d)
        dashed(d, (gx(2.0), GY1), (gx(2.0), gy(6.0) + 20), DBLUE, w=4, on=10, off=8)
        card(d, (140, 300, 940, 420), fill=A((239, 246, 255), k2), r=20)
        text(d, (540, 360), "Đỉnh ở f₀ = 2,0 Hz", 62, DBLUE, alpha=k2)
    kp = appear(t, M[1] - 0.1, 0.4)
    if kp > 0: pill(d, 560, "ĐÁP ÁN · tăng rồi giảm", NAVY, kp, size=58)

# ---------------- canh 4: Bay (luc manh la cong huong?) ----------------
def s_bay(img, d, t, sc):
    kc = appear(t, 3.4, 0.5)
    f, a_ = (2.0, 6.0) if kc > 0.5 else (1.0, 2.7)
    u = t - (3.4 if kc > 0.5 else 0.0)
    rig(d, osc(u, f, a_), 2 * math.pi * f * u / 2, f=f)
    card(d, (640, 450, 1040, 530), fill=WHITE, outline=NAVY, r=20, w=3)
    text(d, (840, 490), "lực không đổi", 56, NAVY)
    y0 = 980
    card(d, (40, y0, 1040, y0 + 560), fill=WHITE, outline=DRED, w=6)
    pill(d, y0 + 70, "BẪY", DRED)
    s1 = "✗ Lực mạnh là cộng hưởng"
    lw = tw(d, s1, F(60))
    text(d, (W / 2, y0 + 200), s1, 60, DRED)
    if kc > 0:
        d.line([(W / 2 - lw / 2, y0 + 202), (W / 2 - lw / 2 + lw * kc, y0 + 202)], fill=(140, 15, 15), width=7)
        text(d, (W / 2, y0 + 320), "✓ Chỉ đổi f:", 60, DGREEN, alpha=kc)
        text(d, (W / 2, y0 + 430), "A: 2,7 cm → 6,0 cm", 60, DGREEN, alpha=kc)

# ---------------- canh 5: Chua noi duoc ----------------
def s_gioihan(img, d, t, sc):
    card(d, (40, 260, 1040, 600), fill=WHITE, outline=NAVY, w=6)
    text(d, (W / 2, 345), "Chưa nói được", 64, NAVY)
    text(d, (W / 2, 490), "Cản lớn thì đỉnh ra sao?", 60, INK)
    axes(d)
    model(d)
    fm = 1.0 + 2.0 * clamp(t / 4.4)
    text(d, (GX1, GY0 + 40), "f tăng →", 56, DORANGE, anchor="rm")
    d.rectangle([gx(fm) - 22, gy(amp(fm)), gx(fm) + 22, GY1], fill=A(ORANGE, 0.55))
    dot(d, gx(fm), gy(amp(fm)), 18, DORANGE)

# ---------------- canh 6: THU NGHI (= cau_chot khung web) ----------------
def s_end(img, d, t, sc):
    k1 = appear(t, 0.15, 0.4)
    card(d, (40, 215, 1040, 1560), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, 290, "THỬ NGHĨ", ORANGE, k1)
    card(d, (80, 380, 1000, 500), fill=A((239, 246, 255), k1), r=20)
    text(d, (W / 2, 440), "f = 3,0 Hz: A = 2,7 cm", 58, DBLUE, alpha=k1)
    kq = appear(t, 2.2, 0.45)
    if kq > 0:
        text(d, (W / 2, 700), "Cùng hệ, đặt f = 3,5 Hz.", 62, INK, alpha=kq)
        text(d, (W / 2, 810), "Biên độ ổn định khoảng bao nhiêu?", 58, DORANGE, alpha=kq)
        seg_bar(d, 960, t, 2.8, sc["T"] - 0.2, ORANGE, kq)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, b, e = sc["hook"], sc["do"], sc["dapan"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open")] + [(do["t0"] + 2.0 * j + 1.5, "tick") for j in range(5)] + [
            (da["t0"] + da["M"][1] - 0.1, "ding"), (b["t0"] + 0.3, "buzz"), (e["t0"] + 2.2, "open")]

CLIP = dict(id="tn-l11-tatdan-01", header="VẬT LÍ 11 · THÍ NGHIỆM", footer="Dao động cưỡng bức · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Mô-tơ lắc con lắc lò xo", draw=s_hook, tail=0.3, caps=[
   ("Mô-tơ lệch tâm lắc lò xo.", 3.4),
   ("Dừng lại, tự đoán.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.3, caps=[
   ("Mỗi tần số, chờ ổn định rồi đọc.", 5.0),
   ("Chấm từng số đọc lên đồ thị.", 5.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.2, caps=[
   ("Nối năm điểm đo.", 4.0),
   ("Đường đứt là mô hình.", 3.0)]),
 dict(key="bay", title="Bẫy hay gặp", draw=s_bay, tail=0.3, caps=[
   ("Lực mạnh là cộng hưởng?", 3.4),
   ("Chỉ đổi tần số.", 3.8)]),
 dict(key="gioihan", title="Giới hạn", draw=s_gioihan, tail=0.3, caps=[
   ("Mới thử một mức cản.", 4.0)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.2, caps=[
   ("Đổi tần số lực.", 3.0),
   ("Dừng lại, tự đoán.", 4.8)]),
])
