# Clip: tn-l9-taitao-02 - Pin mat troi mini duoi den ban: che bot, tat den (KHTN 9 Bai 17, lesson 95; 18/11/2026)
# So lieu lay nguyen tu content/thi-nghiem/tn-l9-taitao-02.json:
#   so_lieu_mau (f, E, P W): 1 1 1,0 ; 0,5 1 0,5 ; 1 0 0,0  (ghi_chu: minh hoa tu mo hinh P = P0.f.E, P0 = 1,0 W).
#   quan_sat: co den quat quay deu; che bot quat quay cham han; tat den quat dung. an_toan: den ban nong.
#   hien_tuong_hay_sai[1] = bay (pin can nhiet chu khong can anh sang); gia_thiet[1] = chua noi duoc.
#   "Vua tat den, tam pin con am" la suy luan dinh tinh (den ban nong), KHONG co trong kho -> bao phien chinh.
# Cau Tu kiem tra cua bai: Cau 3 (19 gio, nguon nao khong phat duoc) -> clip KHONG noi ban dem/buoi toi, khong dung
#   bay "pin tich san dien nen toi van chay" (hien_tuong_hay_sai[0]) vi qua sat Cau 3. Tra bai 3 (pin khac gio: khong
#   qua tua-bin) -> clip khong noi "khong qua tua-bin".
# Du doan (K10): che nua tam pin, quat nho se ra sao? -> quay cham han (P con 0,5 W theo mo hinh).
# Cau chot (cong B 18/11): khong che pin, van den toi con mot nua (E = 0,5) -> P = P0.f.E = 0,5 W, quat cham hon luc du sang.
#   Buoc moi (doi E thay vi f), khong trung Cau 1-7/Tra bai; da ghi vao ghi_chu kho.
import math
from engine import *

ROWS = [(1, 1, 1.0), (0.5, 1, 0.5), (1, 0, 0.0)]      # so_lieu_mau (f, E, P)
P0 = 1.0
def vn(x, nd=1): return f"{x:.{nd}f}".replace(".", ",")

PANEL = (30, 64, 140); CELL = (59, 106, 196); CARD_C = (180, 140, 90); GLOW = (255, 214, 80); METAL = (214, 218, 228)
BLADE = (96, 165, 250); DGREEN = (21, 110, 55); DRED = (185, 28, 28)

# ---------------- dung cu ----------------
PX0, PX1, PY0, PY1, SK = 170, 610, 640, 840, 60      # tam pin (hinh binh hanh nghieng), SK = do xien
LX, LY = 400, 360                                    # bong den
FCX, FCY = 850, 620                                  # quat nho
def panel_pts(a, b):   # phan tam pin tu ti le a toi b theo chieu ngang
    xa0, xb0 = PX0 + SK + (PX1 - PX0) * a, PX0 + SK + (PX1 - PX0) * b
    xa1, xb1 = PX0 + (PX1 - PX0) * a, PX0 + (PX1 - PX0) * b
    return [(xa0, PY0), (xb0, PY0), (xb1, PY1), (xa1, PY1)]

def lamp(d, on):
    d.line([(LX + 330, 930), (LX + 330, 300), (LX + 120, 290)], fill=NAVY, width=10, joint="curve")
    d.rectangle([LX + 270, 925, LX + 390, 945], fill=NAVY)
    d.polygon([(LX - 90, 330), (LX + 120, 270), (LX + 140, 330), (LX - 70, 390)], fill=(70, 78, 100))
    if on > 0:
        d.polygon([(LX - 70, 392), (LX + 140, 334), PANEL_TR, PANEL_BL], fill=A(GLOW, 0.22 * on))
        d.ellipse([LX - 10, 345, LX + 70, 380], fill=A(GLOW, on))
PANEL_TR, PANEL_BL = (PX1 + SK + 20, PY0 - 10), (PX0 - 20, PY1 - 60)

def panel(d, cover, lit):
    d.polygon(panel_pts(0, 1), fill=PANEL, outline=NAVY)
    for i in range(1, 6):
        p = panel_pts(i / 6, i / 6); d.line([p[0], p[3]], fill=CELL, width=3)
    for j in (1, 2):
        y = PY0 + (PY1 - PY0) * j / 3; dx = SK * (1 - j / 3)
        d.line([(PX0 + dx, y), (PX1 + dx, y)], fill=CELL, width=3)
    if lit > 0:  # anh sang phan chieu tren mat pin
        d.polygon(panel_pts(0.55, 0.75), fill=A((255, 255, 255), 0.18 * lit))
    if cover > 0:  # tam bia truot vao tu trai, phu nua trai
        pts = panel_pts(0, 0.5); off = (1 - cover) * -320
        d.polygon([(x + off, y + (-8 if i < 2 else 8)) for i, (x, y) in enumerate(pts)], fill=CARD_C, outline=(120, 90, 50))
    d.line([(PX0 + 40, PY1), (PX0 + 40, 930)], fill=NAVY, width=6); d.line([(PX1 - 40, PY1), (PX1 - 40, 930)], fill=NAVY, width=6)

def small_fan(d, ang, spin):
    d.line([(PX1 + 10, 760), (FCX - 30, 760), (FCX - 30, FCY + 70)], fill=(60, 66, 92), width=4)
    d.rectangle([FCX - 10, FCY + 60, FCX + 10, 930], fill=METAL, outline=NAVY, width=3)
    d.rectangle([FCX - 60, 920, FCX + 60, 940], fill=METAL, outline=NAVY, width=3)
    if spin > 0.05:
        d.ellipse([FCX - 110, FCY - 110, FCX + 110, FCY + 110], fill=A((147, 197, 253), 0.35 * spin))
    for k in range(3):
        a = ang + k * 2 * math.pi / 3
        tip = (FCX + 105 * math.cos(a), FCY + 105 * math.sin(a)); sd = (-math.sin(a) * 30, math.cos(a) * 30)
        d.polygon([(FCX, FCY), (tip[0] + sd[0], tip[1] + sd[1]), tip], fill=A(BLADE, 1 - 0.6 * spin), outline=NAVY)
    d.rounded_rectangle([FCX - 26, FCY - 26, FCX + 26, FCY + 26], radius=8, fill=(70, 78, 100))

def pbar(d, p, y=980, alpha=1.0, label=True):
    x0, x1 = 300, 960
    if label: text(d, (60, y + 30), "P (mô hình)", 40, INK, anchor="lm", alpha=alpha)
    d.rounded_rectangle([x0, y, x1, y + 60], radius=14, fill=A(LIGHT, alpha))
    if p > 0.01: d.rounded_rectangle([x0, y, x0 + (x1 - x0 - 120) * p / P0, y + 60], radius=14, fill=A(ORANGE, alpha))
    text(d, (x1 - 10, y + 30), vn(p) + " W", 42, (154, 52, 18), anchor="rm", alpha=alpha)

def rig(d, t, ang, cover, lamp_on, p=None):
    card(d, (40, 262, 1040, 1080 if p is not None else 990), fill=WHITE, outline=LIGHT, w=3)
    d.line([(60, 940), (1020, 940)], fill=(180, 170, 150), width=4)
    lamp(d, lamp_on); panel(d, cover, lamp_on); small_fan(d, ang, clamp(spin_of(p if p is not None else lamp_on * P0)))
    if p is not None: pbar(d, p)
def spin_of(p): return p / P0

# ---------------- canh 1: Du doan ----------------
THINK_END = 0.7
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, t, 7.0 * t, 0.0, 1.0)
    text(d, (420, 745), "tấm pin", 42, WHITE)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1040 + (1 - a) * 40
    card(d, (50, y0, 1030, y0 + 470), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pw = tw(d, "DỰ ĐOÁN", F(40)) + 52
    card(d, (W / 2 - pw / 2, y0 + 26, W / 2 + pw / 2, y0 + 88), fill=A(PURPLE, a), r=31)
    text(d, (W / 2, y0 + 57), "DỰ ĐOÁN", 40, WHITE, alpha=a)
    ctext(d, y0 + 245, "Lấy bìa che nửa tấm pin.\nQuạt nhỏ sẽ ra sao?", 52, INK, maxw=920, alpha=a)
    tc, tend = M[1] + 0.6, sc["T"] - THINK_END
    if t > tc:
        p = clamp((t - tc) / (tend - tc))
        d.rounded_rectangle([140, y0 + 420, 940, y0 + 432], radius=6, fill=A(LIGHT, a))
        d.rounded_rectangle([140, y0 + 420, 140 + 800 * (1 - p), y0 + 432], radius=6, fill=A(PURPLE, a))

# ---------------- canh 2: Tien hanh (mot canh lien mach: che nua -> bo bia -> tat den) ----------------
T_CV0, T_CV1, T_UN0, T_UN1, T_OFF = 1.0, 1.6, 4.6, 5.1, 5.9
def do_state(t):
    """-> (do phu bia 0..1, den 0/1, P dang co theo so_lieu_mau)."""
    if t < T_CV0: cov = 0.0
    elif t < T_CV1: cov = ease((t - T_CV0) / (T_CV1 - T_CV0))
    elif t < T_UN0: cov = 1.0
    elif t < T_UN1: cov = 1 - ease((t - T_UN0) / (T_UN1 - T_UN0))
    else: cov = 0.0
    on = 0.0 if t >= T_OFF else 1.0
    f = 0.5 if cov >= 0.5 else 1.0          # so chi doi mot lan khi bia phu qua nua duong (khong hien so trung gian)
    return cov, on, P0 * f * on, f

def angle(t, dt=1 / 60):
    """tich phan goc quat, toc do bam theo P co quan tinh."""
    a = w = 0.0; s = 0.0
    while s < t:
        target = 9.0 * do_state(s)[2] / P0
        w += (target - w) * min(1, dt / 0.45); a += w * dt; s += dt
    return a, w / 9.0

def s_do(img, d, t, sc):
    cov, on, p, f = do_state(t)
    ang, spin = angle(t)
    card(d, (40, 262, 1040, 1080), fill=WHITE, outline=LIGHT, w=3)
    d.line([(60, 940), (1020, 940)], fill=(180, 170, 150), width=4)
    lamp(d, on); panel(d, cov, on); small_fan(d, ang, clamp(spin)); pbar(d, p)
    card(d, (40, 1120, 1040, 1200), fill=(255, 247, 237), outline=ORANGE, r=24, w=3)
    text(d, (W / 2, 1160), "An toàn: đèn nóng, không chạm bóng", 40, (154, 52, 18))

def _kiem_dong_bo():
    """P hien = P0.f.E dung hang kho moi 0,05 s: phu kin -> 0,5 ; tat den -> 0 ; con lai 1,0."""
    import copy; clip = copy.deepcopy(CLIP); build(clip)
    sc = [s for s in clip["scenes"] if s["key"] == "do"][0]; t = 0.0; bad = []
    while t < sc["T"]:
        cov, on, p, f = do_state(t)
        hop = [r[2] for r in ROWS if r[0] == f and r[1] == on]
        if not on: hop = [ROWS[2][2]]
        if not hop or abs(hop[0] - p) > 1e-9: bad.append((round(t, 2), cov, on, p))
        t += 0.05
    return bad

# ---------------- canh 3: Dap an ----------------
def s_dapan(img, d, t, sc):
    M = sc["M"]
    ka = appear(t, 0.15, 0.4)
    lab = "ĐÁP ÁN · quạt quay chậm hẳn"
    pw = tw(d, lab, F(46)) + 60
    card(d, (W / 2 - pw / 2, 270, W / 2 + pw / 2, 350), fill=A(NAVY, ka), r=38)
    text(d, (W / 2, 310), lab, 46, WHITE, alpha=ka)
    names = ("đủ sáng", "che nửa", "tắt đèn")
    card(d, (40, 400, 1040, 1290), fill=WHITE, outline=LIGHT, w=3)
    for j, (f, e, p) in enumerate(ROWS):
        kk = appear(t, 0.6 + 0.8 * j, 0.4)
        y = 520 + j * 270
        text(d, (80, y - 55), names[j], 46, INK, anchor="lm", alpha=kk)
        d.rounded_rectangle([80, y, 800, y + 90], radius=16, fill=A(LIGHT, kk))
        if p > 0: d.rounded_rectangle([80, y, 80 + 720 * p / P0, y + 90], radius=16, fill=A(ORANGE, kk))
        text(d, (1000, y + 45), vn(p) + " W", 48, (154, 52, 18), anchor="rm", alpha=kk)
    kn = appear(t, M[1] + 0.3, 0.4)
    card(d, (140, 1340, 940, 1440), fill=A((241, 245, 249), kn), r=24)
    text(d, (W / 2, 1390), "số minh hoạ theo mô hình", 40, MUTED, bold=False, alpha=kn)

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    k1 = appear(t, 0.3, 0.45)
    card(d, (40, 300, 1040, 740), fill=A((255, 251, 235), k1), outline=A((202, 138, 4), k1), w=5)
    text(d, (W / 2, 420), "năng lượng ánh sáng", 56, (161, 98, 7), alpha=k1)
    arrow(d, (W / 2, 480), (W / 2, 590), A(NAVY, k1), w=7, head=22)
    text(d, (W / 2, 650), "điện năng", 56, BLUE, alpha=k1)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        card(d, (40, 820, 1040, 1260), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 950), "Ít ánh sáng → ít điện", 54, DGREEN, alpha=k2)
        text(d, (W / 2, 1130), "Không ánh sáng → không điện", 54, DGREEN, alpha=k2 * appear(t, M[1] + 0.8, 0.4))

# ---------------- canh 5: Bay (can nong) roi Chua noi duoc ----------------
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[1] - 0.1, 0.45)
    a1 = appear(t, 0.1, 0.4) * (1 - k2)
    # hinh co ngay: vua tat den, tam pin con am (song nhiet), quat dung
    card(d, (40, 262, 1040, 990), fill=WHITE, outline=LIGHT, w=3)
    d.line([(60, 940), (1020, 940)], fill=(180, 170, 150), width=4)
    lamp(d, 0.0); panel(d, 0.0, 0.0); small_fan(d, 0.4, 0.0)
    for j, x0 in enumerate((300, 390, 480)):
        pts = [(x0 + 10 * math.sin(2 * math.pi * (s / 36 - t * 0.7 + j * 0.3)), PY0 - 10 - s) for s in range(0, 90, 6)]
        d.line(pts, fill=A(ORANGE, 0.8), width=5)
    kv = appear(t, M[0] + 1.4, 0.4)
    text(d, (390, 520), "pin còn ấm", 42, ORANGE, alpha=kv)
    text(d, (FCX, FCY - 150), "quạt dừng", 42, DRED, alpha=kv)
    if a1 > 0:
        y0 = 1040
        card(d, (40, y0, 1040, y0 + 330), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pw = tw(d, "BẪY", F(40)) + 52
        card(d, (W / 2 - pw / 2, y0 + 28, W / 2 + pw / 2, y0 + 92), fill=A(DRED, a1), r=32)
        text(d, (W / 2, y0 + 60), "BẪY", 40, WHITE, alpha=a1)
        q = "“Pin mặt trời cần nóng”"
        ks = clamp((t - M[0] - 1.4) / 0.4)
        f = F(48); lw = tw(d, q, f); yy = y0 + 200
        text(d, (W / 2, yy), q, 48, mix(INK, MUTED, ks), alpha=a1)
        if ks > 0:
            d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, 0.85 * a1), width=6)
            text(d, (W / 2 + lw / 2 + 40, yy), "✗", 48, DRED, alpha=a1 * ks)
    if k2 > 0:
        y0 = 1040 + (1 - k2) * 30
        card(d, (40, y0, 1040, y0 + 400), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 75), "Chưa nói được", 46, NAVY, alpha=k2)
        kk = k2 * appear(t, M[1] + 0.3, 0.4)
        text(d, (W / 2, y0 + 190), "Pin thật: che một phần", 46, INK, alpha=kk)
        text(d, (W / 2, y0 + 265), "giảm nhiều hơn nửa", 46, INK, alpha=kk)

# ---------------- canh 6: Chot + cau hoi ----------------
HINT_AT = 4.4
def s_end(img, d, t, sc):
    M = sc["M"]; k0 = appear(t, 0.2, 0.5)
    card(d, (60, 262, 1020, 520), fill=A((236, 253, 243), k0), outline=A(GREEN, k0), w=6)
    ctext(d, 391, "Pin quang điện: ánh sáng → điện", 50, GREEN, maxw=880, alpha=k0)
    k1 = appear(t, M[0] + 0.1, 0.5)
    if k1 <= 0: return
    card(d, (40, 580, 1040, 1300), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pw = tw(d, "THỬ NGHĨ", F(40)) + 52
    card(d, (W / 2 - pw / 2, 610, W / 2 + pw / 2, 676), fill=A(ORANGE, k1), r=32)
    text(d, (W / 2, 643), "THỬ NGHĨ", 40, WHITE, alpha=k1)
    kq = appear(t, M[0] + 0.4, 0.5)
    ctext(d, 830, "Không che pin, vặn đèn\ntối còn một nửa.\nQuạt quay thế nào?", 48, INK, maxw=900, alpha=kq)
    kh = appear(t, M[0] + HINT_AT, 0.5)
    if kh > 0:
        card(d, (110, 1060, 970, 1250), fill=A((255, 247, 237), kh), r=24)
        ctext(d, 1155, "Pin nhận bao nhiêu ánh sáng?", 44, ORANGE, maxw=840, alpha=kh)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    return [(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - THINK_END, "ding"),
            (do["t0"] + T_CV0, "tap"), (do["t0"] + T_UN0, "tap"), (do["t0"] + T_OFF, "tap"),
            (da["t0"] + 0.15, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + 0.1, "buzz"),
            (b["t0"] + b["M"][0] + 1.4, "tap"), (e["t0"] + e["M"][0] + 0.1, "open")]

CLIP = dict(id="tn-l9-taitao-02", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Năng lượng tái tạo · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Pin mặt trời mini dưới đèn", draw=s_hook, tail=0.8, caps=[
   ("Đèn chiếu, quạt nhỏ quay đều.", 3.2),
   ("Tự trả lời trước khi xem.", 5.6)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.6, caps=[
   ("Che nửa tấm pin bằng bìa.", 4.2),
   ("Bỏ bìa ra, rồi tắt đèn.", 3.6)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.6, caps=[
   ("Ba lần thử.", 3.4),
   ("Tắt đèn thì quạt dừng hẳn.", 3.4)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.5, caps=[
   ("Tấm pin cần thứ gì?", 3.0),
   ("Điện theo lượng ánh sáng.", 3.2)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.5, caps=[
   ("Vừa tắt đèn xong.", 4.2),
   ("Còn chưa nói được.", 3.6)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=1.0, caps=[
   ("Tự nghĩ, rồi xem gợi ý.", 5.8)]),
])

def _kiem_so():
    import json, os
    bad = []
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "content", "thi-nghiem", "tn-l9-taitao-02.json")
    k = json.load(open(p)); ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    if [tuple(r) for r in k["so_lieu_mau"]["hang"]] != ROWS: bad.append("so_lieu_mau")
    if ts["P0"]["gia_tri"] != P0: bad.append("P0")
    if any(abs(P0 * f * e - p) > 1e-9 for f, e, p in ROWS): bad.append("mo hinh")
    if abs(P0 * 1 * 0.5 - 0.5) > 1e-9 or "E = 0,5" not in k.get("ghi_chu", ""): bad.append("cau chot (ghi_chu kho)")
    return bad

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch kho/mô hình:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
