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
# Cau chot cu (18/11): chi vang den con nua -> 0,5 W, quat cham hon: TRUNG so 0,5 W da chieu va trung dap an Du doan.
# Dung lai theo cong moi 27/11/2026 (Viec 4 L9 nhom C): cau chot moi = che nua pin VA den toi con nua
#   -> theo mo hinh P = P0.f.E = 0,25 W (ghep hai yeu to, so chua chieu). Kho ghi_chu con ghi cau chot cu -> bao phien chinh.
#   Chu >= 56, canh <= 180 tu/phut, khoi chu cach >= 2,5 s; Bay co o "✓" giu >= 3 s.
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
    x0, x1 = 150, 1010
    if label: text(d, (70, y + 30), "P", 56, INK, anchor="lm", alpha=alpha)
    d.rounded_rectangle([x0, y, x1, y + 60], radius=14, fill=A(LIGHT, alpha))
    if p > 0.01: d.rounded_rectangle([x0, y, x0 + (x1 - x0 - 120) * p / P0, y + 60], radius=14, fill=A(ORANGE, alpha))
    text(d, (x1 - 10, y + 30), vn(p) + " W", 56, (154, 52, 18), anchor="rm", alpha=alpha)

def rig(d, t, ang, cover, lamp_on, p=None):
    card(d, (40, 262, 1040, 1080 if p is not None else 990), fill=WHITE, outline=LIGHT, w=3)
    d.line([(60, 940), (1020, 940)], fill=(180, 170, 150), width=4)
    lamp(d, lamp_on); panel(d, cover, lamp_on); small_fan(d, ang, clamp(spin_of(p if p is not None else lamp_on * P0)))
    if p is not None: pbar(d, p)
def spin_of(p): return p / P0

def pill(d, s, y, a, color, size=56):
    pw = tw(d, s, F(size)) + 60
    card(d, (W / 2 - pw / 2, y - 40, W / 2 + pw / 2, y + 40), fill=A(color, a), r=38)
    text(d, (W / 2, y), s, size, WHITE, alpha=a)

def think_bar(d, t, tc, tend, y, a):
    if t <= tc: return
    p = clamp((t - tc) / (tend - tc))
    d.rounded_rectangle([110, y, 970, y + 90], radius=45, fill=A((237, 233, 254), a))
    if p < 1: d.rounded_rectangle([110, y, 110 + max(90, 860 * (1 - p)), y + 90], radius=45, fill=A((76, 29, 149), a))

# ---------------- canh 1: Du doan (K10: chi cau hoi + hinh) ----------------
def s_hook(img, d, t, sc):
    M = sc["M"]
    rig(d, t, 7.0 * t, 0.0, 1.0)
    text(d, (420, 745), "tấm pin", 56, WHITE)
    a = appear(t, M[1] - 0.2, 0.5)
    if a <= 0: return
    y0 = 1040 + (1 - a) * 40
    card(d, (40, y0, 1040, y0 + 480), fill=A(WHITE, a), outline=A(PURPLE, a), w=6)
    pill(d, "DỰ ĐOÁN", y0 + 62, a, PURPLE)
    text(d, (W / 2, y0 + 165), "Lấy bìa che nửa tấm pin.", 58, INK, alpha=a)
    text(d, (W / 2, y0 + 250), "Quạt nhỏ sẽ ra sao?", 58, INK, alpha=a)
    think_bar(d, t, M[1] + 0.3, sc["T"] - 0.1, y0 + 340, a)

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
    text(d, (W / 2, 1160), "Đèn nóng: không chạm bóng", 56, (154, 52, 18))
    text(d, (W / 2, 1270), "P: công suất điện của pin", 56, NAVY)      # GĐ2: goi ten P ngay khi hien

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
    pill(d, "ĐÁP ÁN: quay chậm hẳn", 320, 1.0, GREEN, 58)
    names = ("đủ sáng", "che nửa", "tắt đèn")
    card(d, (40, 400, 1040, 1290), fill=WHITE, outline=LIGHT, w=3)
    k = appear(t, 2.6, 0.4)
    if k > 0:                                     # o nhip quanh hang "che nua"
        ph = 0.5 + 0.5 * math.sin(2 * math.pi * t / 1.6)
        d.rounded_rectangle([56, 700, 1024, 900], radius=24, fill=A(mix((255, 237, 213), WHITE, 0.6 * ph), k))
    for j, (f, e, p) in enumerate(ROWS):
        g = ease((t - 0.5 - 0.8 * j) / 0.6)
        y = 520 + j * 270
        text(d, (80, y - 55), names[j], 56, INK, anchor="lm")
        d.rounded_rectangle([80, y, 800, y + 90], radius=16, fill=LIGHT)
        if p * g > 0.01: d.rounded_rectangle([80, y, 80 + 720 * p * g / P0, y + 90], radius=16, fill=ORANGE)
        text(d, (1000, y + 45), vn(p) + " W", 56, (154, 52, 18), anchor="rm")

# ---------------- canh 4: Rut ra ----------------
def s_rutra(img, d, t, sc):
    M = sc["M"]
    card(d, (40, 300, 1040, 740), fill=(255, 251, 235), outline=(202, 138, 4), w=5)
    text(d, (W / 2, 420), "ánh sáng", 58, (161, 98, 7))
    g = ease(clamp(t / 1.2))
    arrow(d, (W / 2, 480), (W / 2, 480 + 110 * max(0.05, g)), NAVY, w=7, head=22)
    text(d, (W / 2, 650), "điện năng", 58, BLUE)
    k2 = appear(t, M[1] - 0.1, 0.45)
    if k2 > 0:
        card(d, (40, 820, 1040, 1260), fill=A((236, 253, 243), k2), outline=A(GREEN, k2), w=5)
        text(d, (W / 2, 960), "Ít ánh sáng → ít điện", 58, DGREEN, alpha=k2)
        text(d, (W / 2, 1120), "Tắt đèn → không điện", 58, DGREEN, alpha=k2)

# ---------------- canh 5: Bay (can nong) roi Chua noi duoc ----------------
BAY_ST = 2.2
def s_bay(img, d, t, sc):
    M = sc["M"]
    k2 = appear(t, M[2] - 0.1, 0.45); a1 = 1 - k2
    card(d, (40, 262, 1040, 990), fill=WHITE, outline=LIGHT, w=3)
    d.line([(60, 940), (1020, 940)], fill=(180, 170, 150), width=4)
    lamp(d, 0.0); panel(d, 0.0, 0.0); small_fan(d, 0.4, 0.0)
    for j, x0 in enumerate((260, 340, 420, 500)):
        pts = [(x0 + 18 * math.sin(2 * math.pi * (s / 40 - t * 0.9 + j * 0.3)), PY0 - 10 - s) for s in range(0, 80, 5)]
        d.line(pts, fill=A(ORANGE, 0.85), width=8)
    text(d, (390, 520), "pin ấm", 56, ORANGE)
    text(d, (FCX - 70, FCY - 175), "quạt dừng", 56, DRED)
    y0 = 1030
    if a1 > 0:
        card(d, (40, y0, 1040, y0 + 560), fill=A(WHITE, a1), outline=A(DRED, a1), w=6)
        pill(d, "BẪY", y0 + 62, a1, DRED)
        q = "“Pin mặt trời cần nóng”"; yy = y0 + 175; lw = tw(d, q, F(58))
        text(d, (W / 2, yy), q, 58, INK, alpha=a1)
        ks = clamp((t - BAY_ST) / 0.4)
        if ks > 0: d.line([(W / 2 - lw / 2 - 6, yy + 2), (W / 2 - lw / 2 - 6 + (lw + 12) * ks, yy + 2)], fill=A(DRED, a1), width=7)
        kk = a1 * appear(t, M[1] + 0.1, 0.4)
        card(d, (70, y0 + 280, 1010, y0 + 520), fill=A((236, 253, 243), kk), r=24)
        text(d, (W / 2, y0 + 355), "✓ Cần ánh sáng,", 58, DGREEN, alpha=kk)
        text(d, (W / 2, y0 + 445), "không cần nóng", 58, DGREEN, alpha=kk)
    if k2 > 0:
        card(d, (40, y0, 1040, y0 + 420), fill=A(WHITE, k2), outline=A(NAVY, k2), w=6)
        text(d, (W / 2, y0 + 110), "Chưa nói được:", 60, NAVY, alpha=k2)
        text(d, (W / 2, y0 + 220), "pin thật, nắng thật?", 58, INK, alpha=k2)
        text(d, (W / 2, y0 + 320), "(số minh hoạ)", 56, NAVY, alpha=k2)

# ---------------- canh 6: Chot ----------------
END_Q = 0.2
CH_F, CH_E = 0.5, 0.5                             # cau chot: che nua pin VA den con nua -> 0,25 W (khong hien)
def s_end(img, d, t, sc):
    k1 = appear(t, END_Q, 0.5)
    card(d, (40, 262, 1040, 990), fill=WHITE, outline=LIGHT, w=3)
    d.line([(60, 940), (1020, 940)], fill=(180, 170, 150), width=4)
    lamp(d, 0.5); panel(d, 1.0, 0.5)
    d.line([(PX1 + 10, 760), (FCX - 30, 760), (FCX - 30, FCY + 70)], fill=(60, 66, 92), width=4)
    rr = 70 + 30 * math.sin(2 * math.pi * t / 2.0)
    d.ellipse([FCX - rr, FCY - rr, FCX + rr, FCY + rr], fill=mix(ORANGE, WHITE, 0.45))
    text(d, (FCX, FCY), "?", 90, WHITE)
    if k1 <= 0: return
    y0 = 1040
    card(d, (40, y0, 1040, y0 + 440), fill=A(WHITE, k1), outline=A(ORANGE, k1), w=6)
    pill(d, "THỬ NGHĨ", y0 + 62, k1, ORANGE)
    text(d, (W / 2, y0 + 170), "Che nửa pin, đèn tối còn nửa.", 58, INK, alpha=k1)
    text(d, (W / 2, y0 + 255), "Theo mô hình, P khoảng?", 58, INK, alpha=k1)
    text(d, (W / 2, y0 + 350), "đủ sáng: 1,0 W", 56, NAVY, alpha=k1)

def _cues(clip):
    sc = {s["key"]: s for s in clip["scenes"]}
    h, do, da, r, b, e = sc["hook"], sc["do"], sc["dapan"], sc["rutra"], sc["bay"], sc["end"]
    return sorted([(h["t0"] + h["M"][1] - 0.2, "open"), (h["t0"] + h["T"] - 0.1, "ding"),
            (do["t0"] + T_CV0, "tap"), (do["t0"] + T_UN0, "tap"), (do["t0"] + T_OFF, "tap"),
            (da["t0"] + 0.2, "ding"), (r["t0"] + r["M"][1] - 0.1, "tap"), (b["t0"] + BAY_ST, "buzz"),
            (b["t0"] + b["M"][1] + 0.1, "tap"), (e["t0"] + END_Q + 0.1, "open")])

CLIP = dict(id="tn-l9-taitao-02", header="KHTN 9 · VẬT LÍ · THÍ NGHIỆM", footer="Năng lượng tái tạo · thachlab.id.vn",
            cues=_cues, scenes=[
 dict(key="hook", title="Pin mặt trời mini dưới đèn", draw=s_hook, tail=0.3, caps=[
   ("Đèn chiếu, quạt quay đều.", 2.5),
   ("Dừng lại, tự đoán.", 5.4)]),
 dict(key="do", title="Tiến hành", draw=s_do, tail=0.4, caps=[
   ("Che nửa tấm pin bằng bìa.", 4.2),
   ("Bỏ bìa ra, rồi tắt đèn.", 3.4)]),
 dict(key="dapan", title="Kết quả", draw=s_dapan, tail=0.4, caps=[
   ("Ba lần thử.", 3.0),
   ("Tắt đèn: quạt dừng hẳn.", 3.0)]),
 dict(key="rutra", title="Rút ra", draw=s_rutra, tail=0.4, caps=[
   ("Pin cần gì?", 3.0),
   ("Ánh sáng thành điện.", 3.0)]),
 dict(key="bay", title="Bẫy và giới hạn", draw=s_bay, tail=0.3, caps=[
   ("Đúng không?", 4.2),
   ("Nhìn quạt.", 3.4),
   ("Còn bỏ ngỏ.", 2.8)]),
 dict(key="end", title="Chốt lại", draw=s_end, tail=0.3, caps=[
   ("Tự nghĩ.", 6.2)]),
])

def _kiem_so():
    import json, os
    bad = []
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "content", "thi-nghiem", "tn-l9-taitao-02.json")
    k = json.load(open(p)); ts = {x["ky_hieu"]: x for x in k["tham_so"]}
    if [tuple(r) for r in k["so_lieu_mau"]["hang"]] != ROWS: bad.append("so_lieu_mau")
    if ts["P0"]["gia_tri"] != P0: bad.append("P0")
    if any(abs(P0 * f * e - p) > 1e-9 for f, e, p in ROWS): bad.append("mo hinh")
    if abs(P0 * CH_F * CH_E - 0.25) > 1e-9 or CH_F * CH_E in [f * e for f, e, _ in ROWS]: bad.append("cau chot")
    return bad

if __name__ == "__main__":
    import sys
    if "--kiem" in sys.argv:
        print("lệch kho/mô hình:", _kiem_so() or "không")
        print("lệch đồng bộ:", _kiem_dong_bo() or "không")
