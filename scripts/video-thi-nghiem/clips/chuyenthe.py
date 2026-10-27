# Clip: tn-l12-chuyenthe-01 - Dun nuoc da, moi phut ghi nhiet do mot lan
import numpy as np
from engine import *

ROWS = [(0, -6.0), (1, 0.2), (2, 0.2), (3, 0.2), (4, 0.3), (5, 17.8), (6, 38.0), (7, 58.1), (8, 78.0), (9, 98.1), (10, 100.2),
        (11, 100.3), (15, 100.3), (20, 100.3), (25, 100.3), (30, 100.3), (35, 100.2), (36, 100.2)]
TT = [r[0] for r in ROWS]; TV = [r[1] for r in ROWS]
def Tof(tau): return float(np.interp(tau, TT, TV))

def beaker(d, t, tau, cx=330, base=640):
    T = Tof(tau); w, h = 300, 300; x0, x1, y0 = cx - w // 2, cx + w // 2, base - h
    melt = clamp((tau - 0.4) / 3.7)                    # ty le da con lai ~ giam khi tau 0.4..4.1
    level = 0.30 + 0.45 * (1 - clamp((tau - 10) / 26) * 0.9)   # nuoc can dan khi soi
    wl = base - h * (level if tau > 4 else 0.55)
    d.rectangle([x0 + 6, wl, x1 - 6, base - 6], fill=(150, 200, 255, 150) if tau > 1 else (200, 225, 250, 120))
    if tau < 4.2:
        for i in range(6):
            sz = 46 * (1 - melt) + 6
            ix = x0 + 50 + (i % 3) * 80 + (i // 3) * 20; iy = wl + 18 + (i // 3) * 60 + (0 if tau < 4 else 40 * (tau - 4))
            d.rounded_rectangle([ix, iy, ix + sz, iy + sz], radius=8, fill=(240, 250, 255, 235), outline=(120, 170, 220), width=3)
    if T > 99:
        for i in range(9):
            bx = x0 + 30 + (i * 53) % (w - 60); by = base - 20 - ((t * 140 + i * 47) % (base - wl - 20))
            d.ellipse([bx - 8, by - 8, bx + 8, by + 8], outline=WHITE, width=3)
        for i in range(3):
            sx = cx - 70 + i * 70
            pts = [(sx + 18 * math.sin(t * 3 + i + k * 0.7), wl - 20 - k * 26) for k in range(5)]
            d.line(pts, fill=A(GRAY, 0.6), width=6)
    d.line([(x0, y0), (x0, base), (x1, base), (x1, y0)], fill=NAVY, width=8, joint="curve")
    d.rounded_rectangle([x0 - 30, base + 6, x1 + 30, base + 40], radius=12, fill=mix(GRAY, RED, clamp(0.25 + (T > -5) * 0.5)))
    d.line([(x1 - 80, y0 - 60), (x1 - 80, base - 40)], fill=RED, width=10)       # nhiet ke
    dot(d, x1 - 80, base - 36, 14, RED)
    # o doc nhiet do
    card(d, (560, 410, 1000, 620), fill=WHITE, outline=NAVY, w=5)
    text(d, (780, 450), f"t = {int(tau)} phút", 40, MUTED)
    text(d, (780, 540), f"{T:.1f}".replace(".", ",") + " °C", 76, RED if T > 50 else (BLUE if T < 5 else ORANGE))

def plot(d, x0, y0, x1, y1, tau, tmax=36, hl=0.0):
    X = lambda m: x0 + m / tmax * (x1 - x0); Y = lambda T: y0 + (T + 10) / 120 * (y1 - y0)
    d.line([(x0, y0), (x1 + 15, y0)], fill=NAVY, width=5); d.line([(x0, y0), (x0, y1 - 15)], fill=NAVY, width=5)
    text(d, (x1, y0 + 38), "t (phút)", 30, MUTED, anchor="rm"); text(d, (x0 + 12, y1 - 28), "T (°C)", 30, MUTED, anchor="lm")
    for T in (0, 50, 100):
        d.line([(x0 - 8, Y(T)), (x1, Y(T))], fill=LIGHT, width=2); text(d, (x0 - 14, Y(T)), str(T), 28, MUTED, bold=False, anchor="rm")
    for m in (10, 20, 30): text(d, (X(m), y0 + 30), str(m), 28, MUTED, bold=False)
    n = int(tau * 12) + 1; pts = [(X(i / 12), Y(Tof(i / 12))) for i in range(n)]
    if len(pts) > 1: d.line(pts, fill=BLUE, width=7)
    for r in ROWS:
        if r[0] <= tau and r[0] <= 11: dot(d, X(r[0]), Y(r[1]), 9, ORANGE)
    if hl > 0:
        for a, b, T, lab in ((1, 4.2, 0, "≈ 4 phút · nóng chảy"), (10, 36, 100, "≈ 27 phút · sôi")):
            d.line([(X(a), Y(T) + 24), (X(b), Y(T) + 24)], fill=A(GREEN, hl), width=10)
            text(d, ((X(a) + X(b)) / 2 + (110 if a == 1 else 0), Y(T) - 48), lab, 32, GREEN, alpha=hl)

def s_hook(img, d, t, sc):
    beaker(d, t, 0.0)
    card(d, (80, 740, 1000, 1010), fill=WHITE, outline=PURPLE, w=6)
    text(d, (W / 2, 790), "Dự đoán dạng đồ thị T – t", 42, PURPLE)
    a = appear(t, sc["M"][1] - 0.1, 0.5)
    for i, (lab, c, pts) in enumerate((("A", NAVY, [(0, 1), (1, 0)]), ("B", NAVY, [(0, 1), (.25, .55), (.45, .55), (.65, .2), (1, .2), (1, 0)]), ("C", NAVY, [(0, 1), (.4, .6), (.5, .8), (1, 0)]))):
        x = 130 + i * 290
        card(d, (x, 830, x + 230, 970), fill=A(WHITE, a), outline=A(c, a), r=20, w=4)
        text(d, (x + 24, 856), lab, 32, c, alpha=a, anchor="lm")
    # ba hinh phac: A thang dong, B co doan ngang, C lap lo
    def sk(x, pts, c):
        P = [(x + 40 + px * 150, 940 - (1 - py) * 80) for px, py in pts]
        d.line(P, fill=A(c, a), width=5)
    sk(130, [(0, 1), (1, 0)], NAVY); sk(420, [(0, 1), (.3, .45), (.5, .45), (1, 0)], NAVY); sk(710, [(0, 1), (.3, .85), (1, 0.7)], NAVY)
    text(d, (W / 2, 1130), "Đá −6 °C, 0,20 kg · bếp giữ một mức · ghi nhiệt độ mỗi phút", 36, MUTED, bold=False) if False else ctext(d, 1130, "Đá −6 °C, 0,20 kg · bếp giữ một mức · ghi nhiệt độ mỗi phút", 36, MUTED, bold=False)

def tau_of(t, sc):
    M = sc["M"]; return float(np.interp(t, [M[0], M[0] + 0.4, M[1], M[2], M[3], sc["T"] - 0.4], [-6, 0, 1, 4.4, 10, 36]))

def s_do(img, d, t, sc):
    tau = max(0.0, tau_of(t, sc)); beaker(d, t, tau)
    card(d, (50, 720, 1030, 1620), fill=WHITE, outline=LIGHT, w=3)
    plot(d, 160, 1470, 970, 820, tau)

def s_graph(img, d, t, sc):
    card(d, (50, 250, 1030, 1000), fill=WHITE, outline=LIGHT, w=3)
    plot(d, 160, 880, 970, 330, 36, hl=appear(t, sc["M"][0] + 0.3, 0.8))
    keyword(d, "Đang chuyển thể → nhiệt độ không đổi dù vẫn nhận nhiệt", t, sc["M"][1], GREEN, y=1120, size=42)
    keyword(d, "Nhiệt nhận vào phá liên kết giữa các phân tử, không làm tăng tốc độ trung bình", t, sc["M"][2], BLUE, y=1300, size=40)
    keyword(d, "Đọc 0,2 °C ≠ “nóng chảy ở 0,2 °C”: sai số nhiệt kế ±0,5 °C", t, sc["M"][3], RED, y=1470, size=40)

CLIP = dict(id="tn-l12-chuyenthe-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Sự chuyển thể · thachlab.id.vn", scenes=[
 dict(key="hook", title="Đun nước đá, ghi nhiệt độ", draw=s_hook, caps=[
   "Đun 0,20 kg nước đá ở −6 °C trên bếp giữ một mức, khuấy đều, mỗi phút đọc nhiệt kế một lần.",
   "Dự đoán trước: đồ thị nhiệt độ – thời gian trông như thế nào?"]),
 dict(key="do", title="Nhiệt kế nói gì?", draw=s_do, caps=[
   ("Bật bếp, bấm giờ, ghi nhiệt độ mỗi phút.", 3.0),
   ("Nhiệt kế lên 0 °C rồi đứng yên khoảng 4 phút, đá vẫn đang tan.", 5.5),
   ("Đá tan hết thì nhiệt độ mới tăng đều theo thời gian.", 5.0),
   ("Từ phút 10, nhiệt độ lại đứng yên gần 100 °C cho tới lúc nước cạn.", 6.5)]),
 dict(key="graph", title="Rút ra", draw=s_graph, caps=[
   "Hai đoạn nằm ngang: ở 0 °C khoảng 4 phút và ở 100 °C khoảng 27 phút.",
   "Chất đang chuyển thể thì nhiệt độ không đổi dù vẫn nhận nhiệt.",
   "Cơ chế: nhiệt nhận vào dùng để phá liên kết, không làm tăng tốc độ phân tử.",
   "Số đọc 0,2 °C nằm trong sai số ±0,5 °C của nhiệt kế."]),
])
