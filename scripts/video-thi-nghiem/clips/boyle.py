# Clip: tn-l12-boylecharles-01 - Nen khi trong xilanh kin, nhiet do khong doi thi pV khong doi
import random
from engine import *

ROWS = [(8.0, 100), (6.0, 142), (5.0, 170), (4.0, 215), (3.0, 267)]
R = random.Random(3)
PART = [(R.random(), R.random(), R.uniform(-1, 1) * 0.9, R.uniform(-1, 1) * 0.9) for _ in range(26)]

def syringe(d, t, V, p, cx0=140, cy=620, show_p=True):
    L = 470 * V / 8.0; x1 = cx0 + 470; xh = x1 - L
    d.rounded_rectangle([cx0, cy - 110, x1, cy + 110], radius=18, fill=(236, 244, 255), outline=NAVY, width=6)
    d.rectangle([xh, cy - 104, x1 - 4, cy + 104], fill=(214, 232, 255))        # khoi khi
    d.rectangle([xh - 26, cy - 106, xh, cy + 106], fill=GRAY, outline=NAVY, width=4)  # piston
    d.line([(xh - 26, cy), (cx0 - 60, cy)], fill=NAVY, width=14)
    d.rounded_rectangle([cx0 - 90, cy - 70, cx0 - 50, cy + 70], radius=10, fill=NAVY)
    d.rectangle([x1, cy - 14, x1 + 150, cy + 14], fill=GRAY, outline=NAVY, width=3)
    for (ux, uy, vx, vy) in PART:
        px = refl(ux + vx * t * 0.45, 0, 1); py = refl(uy + vy * t * 0.45, 0, 1)
        dot(d, xh + 14 + px * (L - 28), cy - 90 + py * 180, 8, ORANGE)
    gx, gy = x1 + 150 + 110, cy
    d.ellipse([gx - 110, gy - 110, gx + 110, gy + 110], fill=WHITE, outline=NAVY, width=7)
    for k in range(0, 7):
        a = math.radians(-225 + k * 45 * 1.0 * 1.0)
        d.line([(gx + 90 * math.cos(a), gy + 90 * math.sin(a)), (gx + 104 * math.cos(a), gy + 104 * math.sin(a))], fill=NAVY, width=4)
    ang = math.radians(-225 + clamp(p / 300) * 270)
    d.line([(gx, gy), (gx + 84 * math.cos(ang), gy + 84 * math.sin(ang))], fill=RED, width=8); dot(d, gx, gy, 10, NAVY)
    text(d, (gx, gy + 70), "kPa", 28, MUTED)
    if show_p:
        text(d, (gx, gy + 168), f"p = {p:.0f} kPa", 44, RED)
    text(d, ((xh + x1) / 2, cy + 160), f"V = {V:.1f} ml", 44, BLUE)
    text(d, (cx0, cy - 150), "xilanh 20 ml, bịt kín", 30, MUTED, bold=False, anchor="lm")

def s_hook(img, d, t, sc):
    syringe(d, t, 8.0, 100)
    k = appear(t, sc["M"][2] - 0.1, 0.5)
    card(d, (80, 1000, 1000, 1330), fill=WHITE, outline=PURPLE, w=6)
    text(d, (W / 2, 1060), "Dự đoán", 44, PURPLE)
    ctext(d, 1180, "Ấn pít-tông cho V giảm còn một nửa (4 ml).\nÁp kế sẽ chỉ bao nhiêu?", 46, INK, alpha=k)
    for i, (s, c) in enumerate((("≈ 100 kPa", GRAY), ("≈ 150 kPa", BLUE), ("≈ 200 kPa", ORANGE))):
        a = appear(t, sc["M"][2] + 0.5 + i * 0.25)
        card(d, (110 + i * 295, 1260, 370 + i * 295, 1315), fill=A(c, 0.15 * a), outline=A(c, a), r=20, w=4)
        text(d, (240 + i * 295, 1288), s, 32, c, alpha=a)

def stage(t, sc):
    """V, p dang hien tai: piston chuyen sang moc moi sau phu de 1..4."""
    V = 8.0; p = 100.0
    for i in range(1, 5):
        k = ease((t - sc["M"][i] - 0.2) / 1.3)
        if k > 0:
            v0, p0 = ROWS[i - 1]; v1, p1 = ROWS[i]; V = lerp(v0, v1, k); p = lerp(p0, p1, k)
    return V, p

def s_do(img, d, t, sc):
    V, p = stage(t, sc); syringe(d, t, V, p, cy=520)
    card(d, (80, 860, 1000, 1560), fill=WHITE, outline=NAVY, w=4)
    cols = ["Lần", "V (ml)", "p (kPa)"]; xs = [200, 440, 740]
    for x, c in zip(xs, cols): text(d, (x, 920), c, 38, MUTED)
    d.line([(110, 960), (970, 960)], fill=LIGHT, width=4)
    for i, (v, pp) in enumerate(ROWS):
        a = appear(t, sc["M"][i] + 1.5 if i else sc["M"][0] + 0.2)
        y = 1020 + i * 100
        for x, s in zip(xs, [str(i + 1), f"{v:.1f}".replace(".", ","), str(pp)]):
            text(d, (x, y), s, 46, INK if i != 4 else ORANGE, alpha=a)

def s_graph(img, d, t, sc):
    x0, y0, x1, y1 = 170, 1050, 960, 370           # truc: V 2..9 ml, p 0..300 kPa
    X = lambda v: x0 + (v - 2) / 7 * (x1 - x0); Y = lambda p: y0 + p / 300 * (y1 - y0)
    card(d, (60, 280, 1020, 1100), fill=WHITE, outline=LIGHT, w=3)
    d.line([(x0, y0), (x1 + 20, y0)], fill=NAVY, width=5); d.line([(x0, y0), (x0, y1 - 20)], fill=NAVY, width=5)
    text(d, (x1 - 10, y0 + 40), "V (ml)", 34, MUTED); text(d, (x0 + 10, y1 - 40), "p (kPa)", 34, MUTED, anchor="lm")
    for v in range(3, 9): text(d, (X(v), y0 + 30), str(v), 28, MUTED, bold=False)
    for p_ in (100, 200, 300):
        d.line([(x0 - 8, Y(p_)), (x0, Y(p_))], fill=NAVY, width=4); text(d, (x0 - 50, Y(p_)), str(p_), 28, MUTED, bold=False)
    k = ease((t - sc["M"][0] - 0.3) / 3.0)
    if k > 0:
        pts = [(X(v), Y(800 / v)) for v in [2.6 + (9 - 2.6) * (1 - j / 60) for j in range(61)]]
        n = max(2, int(len(pts) * k)); d.line(pts[:n], fill=A(BLUE, 0.35), width=6)
    for i, (v, p_) in enumerate(ROWS):
        a = appear(t, sc["M"][0] + 0.5 + i * 0.5)
        dot(d, X(v), Y(p_), 15 * back(a), ORANGE, WHITE)
    a1 = appear(t, sc["M"][1])
    card(d, (80, 1160, 1000, 1560), fill=WHITE, outline=NAVY, w=4)
    text(d, (W / 2, 1210), "Tích p · V (kPa·ml)", 38, MUTED)
    for i, (v, p_) in enumerate(ROWS):
        x = 190 + i * 175; a = appear(t, sc["M"][1] + 0.2 + i * 0.3)
        text(d, (x, 1300), f"{v:.1f}".replace(".", ",") + "×" + str(p_), 28, MUTED, bold=False, alpha=a)
        text(d, (x, 1370), str(round(v * p_)), 50, ORANGE if a1 > 0 else INK, alpha=a)
    k3 = appear(t, sc["M"][2])
    text(d, (W / 2, 1480), "800 – 860  →  lệch ≤ 8 %", 52, GREEN, alpha=k3)

def s_rut(img, d, t, sc):
    k0 = back((t - sc["M"][0]) / 0.5) if t >= sc["M"][0] else 0
    card(d, (80, 290, 1000, 530), fill=WHITE, outline=GREEN, w=6)
    rich(d, W / 2, 380, "p_{1}V_{1} = p_{2}V_{2}", int(80 * clamp(k0, 0, 1.1)) + 1, GREEN)
    text(d, (W / 2, 480), "nhiệt độ không đổi", 38, MUTED, alpha=clamp(k0))
    a1 = appear(t, sc["M"][1])
    for j, (V, x0) in enumerate(((8.0, 80), (4.0, 560))):
        card(d, (x0, 600, x0 + 440, 860), fill=A(WHITE, a1), outline=A(NAVY, a1), r=24, w=4)
        text(d, (x0 + 220, 640), f"V = {V:.0f} ml", 34, BLUE, alpha=a1)
        n = 12 if j == 0 else 24
        for i in range(n):
            ux, uy, vx, vy = PART[i % 26]
            px = refl(ux + vx * t * 0.4 + 0.1 * i, 0, 1); py = refl(uy + vy * t * 0.4, 0, 1)
            dot(d, x0 + 20 + px * 400, 670 + py * 170, 8, A(ORANGE, a1))
    if t >= sc["M"][1]:
        arrow(d, (540 - 40, 730), (540 + 30, 730), ORANGE, w=8)
        text(d, (W / 2, 910), "mật độ phân tử tăng → va chạm thành bình nhiều hơn → p tăng", 34, ORANGE, alpha=a1) if False else None
        ctext(d, 925, "mật độ tăng → va chạm thành bình nhiều hơn → p tăng", 36, ORANGE, alpha=a1, maxw=900)
    keyword(d, "Chỉ khẳng định được pV không đổi trong sai số ≈ 5 %", t, sc["M"][2], BLUE, y=1130, size=44)
    keyword(d, "Ấn quá nhanh → khí nóng lên → KHÔNG còn đẳng nhiệt", t, sc["M"][3], RED, y=1380, size=44)

CLIP = dict(id="tn-l12-boylecharles-01", header="VẬT LÍ 12 · THÍ NGHIỆM",
    footer="Định luật Boyle · thachlab.id.vn", scenes=[
 dict(key="hook", title="Nén khí trong bơm tiêm", draw=s_hook, caps=[
   "Bịt kín đầu một xilanh có sẵn 8,0 ml không khí, nối với áp kế.",
   "Áp kế đang chỉ 100 kPa. Nhiệt độ phòng giữ nguyên suốt thí nghiệm.",
   "Dự đoán trước: V giảm còn một nửa thì áp suất thành bao nhiêu?"]),
 dict(key="do", title="Ấn từ từ, đọc áp kế", draw=s_do, caps=[
   "Ấn pít-tông từ từ để khí kịp trao đổi nhiệt, mỗi lần đợi 10 giây.",
   "6,0 ml: áp kế chỉ 142 kPa.", "5,0 ml: 170 kPa.", "4,0 ml: 215 kPa.",
   "3,0 ml: 267 kPa, gần trần thang đo nên số đọc kém tin cậy hơn."]),
 dict(key="graph", title="Đồ thị và tích p·V", draw=s_graph, caps=[
   "Áp suất tăng nhanh hơn tỉ lệ bậc nhất khi V giảm: các điểm nằm trên một đường cong.",
   "Tích p·V ở năm lần đo: 800, 852, 850, 860, 801 kPa·ml.",
   "Lệch nhau không quá 8 %: trong phạm vi sai số, p·V không đổi."]),
 dict(key="rut", title="Rút ra", draw=s_rut, caps=[
   "Nhiệt độ không đổi: áp suất tỉ lệ nghịch với thể tích.",
   "Cơ chế: V nhỏ đi thì mật độ phân tử tăng, va chạm lên thành bình nhiều hơn.",
   "Giới hạn: chỉ nói được p·V không đổi trong sai số, không phải bằng nhau tuyệt đối.",
   "Bẫy: ấn pít-tông quá nhanh làm khí nóng lên, quá trình không còn đẳng nhiệt."]),
])
