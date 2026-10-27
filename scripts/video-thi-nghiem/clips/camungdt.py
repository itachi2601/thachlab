# Clip: tn-l12-camungdt-01 - Nam cham va cuon day noi dien ke
from engine import *

OUT_X, IN_X, COIL_X, MY = 230, 590, 640, 600
PH = [  # (chi so phu de, v m/s, thoi luong s, x dau, x cuoi, i mA)
    (1, 0.4, 0.8, OUT_X, IN_X, 3.9), (2, 0.1, 3.2, OUT_X, IN_X, 1.0),
    (3, 0.0, 1.8, IN_X, IN_X, 0.0), (4, -0.2, 1.6, IN_X, OUT_X, -2.0)]

def state(t, sc):
    """vi tri nam cham, i (mA), nhan toc do, do hien."""
    x, i, lab, vis = OUT_X, 0.0, "", 1.0
    for k, v, dur, xa, xb, im in PH:
        t0 = sc["M"][k] + 0.4
        if t < t0 - 0.3: continue
        x = lerp(xa, xb, clamp((t - t0) / dur)); i = 0.0; lab = ""
        if k == 2: vis = clamp(abs(t - (t0 - 0.3)) / 0.15)
        else: vis = 1.0
        if v == 0: lab = "v = 0"
        elif t0 <= t <= t0 + dur + 0.3:
            i = im * ease((t - t0) / 0.2) * (1 - ease((t - t0 - dur) / 0.3)); lab = f"v = {abs(v):.1f} m/s".replace(".", ",")
    return x, i, lab, vis

def coil(d, cx, cy, n=9):
    for j in range(n):
        x = cx - 90 + j * 22
        d.ellipse([x - 20, cy - 120, x + 20, cy + 120], outline=ORANGE, width=8)
    return (cx - 90 - 20, cy + 120), (cx + 90 + 20, cy + 120)

def magnet(d, x, y, alpha=1.0):
    d.rectangle([x - 150, y - 45, x, y + 45], fill=A(BLUE, alpha)); d.rectangle([x, y - 45, x + 150, y + 45], fill=A(RED, alpha))
    text(d, (x - 75, y), "S", 44, WHITE, alpha=alpha); text(d, (x + 75, y), "N", 44, WHITE, alpha=alpha)

def gal(d, i, cx=540, cy=1330):
    d.pieslice([cx - 280, cy - 280, cx + 280, cy + 280], 180, 360, fill=WHITE, outline=NAVY, width=6)
    d.line([(cx - 280, cy), (cx + 280, cy)], fill=NAVY, width=6)
    for k in range(-5, 6):
        a = math.radians(k * 14); d.line([(cx + 230 * math.sin(a * 1), cy - 230 * math.cos(a)), (cx + 262 * math.sin(a), cy - 262 * math.cos(a))], fill=NAVY, width=4)
    ang = math.radians(clamp(i / 5, -1, 1) * 70)
    d.line([(cx, cy), (cx + 235 * math.sin(ang), cy - 235 * math.cos(ang))], fill=RED, width=9); dot(d, cx, cy, 14, NAVY)
    text(d, (cx, cy + 50), "điện kế", 32, MUTED)
    text(d, (cx - 230, cy - 30), "−", 40, BLUE); text(d, (cx + 230, cy - 30), "+", 40, RED)
    return cx, cy

def scene(d, x, i, lab, vis=1.0, pred=False):
    a, b = coil(d, COIL_X, MY)
    magnet(d, x, MY, vis)
    gx, gy = 540, 1330
    d.line([a, (a[0], 1000), (gx - 200, 1000), (gx - 200, gy - 5)], fill=NAVY, width=5)
    d.line([b, (b[0], 1060), (gx + 200, 1060), (gx + 200, gy - 5)], fill=NAVY, width=5)
    gal(d, i)
    text(d, (W / 2, 1000 - 2 + 0), "", 10)
    if lab: text(d, (240, 780), lab, 42, BLUE, anchor="lm")
    text(d, (785, 570), "600 vòng", 32, MUTED, bold=False, anchor="lm"); text(d, (785, 612), "không có pin", 32, MUTED, bold=False, anchor="lm")
    text(d, (540, 1470), "i = " + (f"{i:+.1f}".replace(".", ",").replace("+", "+") if abs(i) > 0.05 else "0") + " mA", 56, RED if abs(i) > 0.05 else MUTED)

def s_hook(img, d, t, sc):
    scene(d, 300, 0.0, "", 1.0)
    k = appear(t, sc["M"][1] - 0.1, 0.5)
    card(d, (80, 250, 1000, 440), fill=A(WHITE, k), outline=A(PURPLE, k), w=6)
    ctext(d, 345, "Dự đoán\nNam châm nằm yên TRONG cuộn dây:\nkim điện kế lệch hay không?", 40, PURPLE, alpha=k)

def s_do(img, d, t, sc):
    x, i, lab, vis = state(t, sc)
    # phase 3 bat dau voi nam cham dang o trong cuon
    scene(d, x, i, lab, vis)

def s_rut(img, d, t, sc):
    card(d, (80, 270, 1000, 800), fill=WHITE, outline=LIGHT, w=3)
    text(d, (W / 2, 320), "Độ lớn |i| theo tốc độ v", 40, MUTED)
    for j, (v, im) in enumerate(((0.0, 0.0), (0.1, 1.0), (0.2, 2.1), (0.4, 3.9))):
        x = 210 + j * 210; k = ease((t - sc["M"][1] - 0.2 * j) / 0.6) if t > sc["M"][1] else 0
        h = im / 4 * 330 * k
        d.rectangle([x - 55, 740 - h, x + 55, 740], fill=ORANGE)
        text(d, (x, 775), f"{v:.1f}".replace(".", ","), 32, MUTED); text(d, (x, 735 - h - 22), f"{im * k:.1f}".replace(".", ","), 34, INK)
    text(d, (880, 335), "v (m/s)", 28, MUTED, bold=False) if False else None
    keyword(d, "Chỉ khi từ thông BIẾN THIÊN mới có dòng cảm ứng", t, sc["M"][0], GREEN, y=930, size=42)
    keyword(d, "Biến thiên càng nhanh, dòng càng lớn: i tỉ lệ thuận với v", t, sc["M"][1], BLUE, y=1130, size=42)
    keyword(d, "Rút ra hoặc đổi cực nam châm → đổi chiều lệch (định luật Lenz)", t, sc["M"][2], PURPLE, y=1340, size=42)
    keyword(d, "Nam châm nằm yên trong cuộn: i = 0, dù từ trường vẫn còn", t, sc["M"][3], RED, y=1530, size=40)

CLIP = dict(id="tn-l12-camungdt-01", header="VẬT LÍ 12 · THÍ NGHIỆM", footer="Cảm ứng điện từ · thachlab.id.vn", scenes=[
 dict(key="hook", title="Nam châm và cuộn dây", draw=s_hook, caps=[
   "Cuộn dây 600 vòng chỉ nối với một điện kế nhạy, không có pin.",
   "Dự đoán trước: nam châm nằm yên trong cuộn thì kim điện kế có lệch không?"]),
 dict(key="do", title="Đưa nam châm vào – ra", draw=s_do, caps=[
   ("Đưa cực Bắc vào cuộn dây, rồi giữ yên, rồi rút ra.", 2.4),
   ("Đưa vào nhanh (0,4 m/s): kim lệch 3,9 mA.", 2.8),
   ("Đưa vào chậm (0,1 m/s): kim lệch ít hơn, 1,0 mA.", 4.6),
   ("Giữ nam châm yên trong cuộn: kim về 0.", 2.6),
   ("Rút ra: kim lệch ngược chiều, −2,0 mA.", 3.2)]),
 dict(key="rut", title="Rút ra", draw=s_rut, caps=[
   "Dòng cảm ứng chỉ có khi từ thông biến thiên.",
   "Độ lớn dòng phụ thuộc tốc độ biến thiên từ thông.",
   "Chiều dòng đổi khi từ thông tăng hay giảm, hoặc khi đổi cực.",
   "Bẫy: có từ trường mà không biến thiên thì không có dòng."]),
])
