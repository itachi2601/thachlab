"""Bài 8. Thấu kính (KHTN 9, lesson_id 86).
Sinh 6 hình SVG + bảng số liệu thí nghiệm + 3 file content/thi-nghiem/tn-l9-thaukinh-0N.json,
thay mốc <!--FIGn--> / __...__ trong theory.src.html -> theory.html.
Mọi ảnh tính bằng 1/f = 1/d + 1/d' và tia đặc biệt (assert toạ độ ảnh = giao điểm tia). Chạy: cd <thư mục bài> && python3 build_figs.py
"""
import json, math, pathlib
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PHUT = 17          # số phút đọc: lấy từ lint_do_dai.py, làm tròn lên

def vn(x, nd=1):
    return f"{x:.{nd}f}".replace(".", "{,}")
def P(x, y): return f"{x:.1f},{y:.1f}"
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
def ray(x1, y1, x2, y2, c=RED, w=2.4, at=0.5, op=1):
    """Tia sáng: thân liền + đầu V 30° giữa đoạn, chỉ chiều truyền."""
    mx, my = x1 + (x2 - x1) * at, y1 + (y2 - y1) * at
    return (line(x1, y1, x2, y2, c, w, "", op) + f'<g opacity="{op}">'
            + chevron(mx, my, x2 - x1, y2 - y1, c, 2.2, 12) + "</g>")
def ext(x1, y1, x2, y2, c=RED):
    """Đường kéo dài của tia (nét đứt, không mũi tên)."""
    return line(x1, y1, x2, y2, c, 1.8, "6 5", .85)
def T(x, y, s, c="currentColor", size=18, anchor="start", weight="700"):
    return text(x, y, s, c, size, anchor, weight)
def lens(x, y1, y2, conv=True, c="currentColor", w=2.6):
    """Kí hiệu thấu kính: đoạn thẳng + đầu V (hội tụ: V hướng ra ngoài; phân kì: V hướng vào trong)."""
    g = line(x, y1, x, y2, c, w)
    if conv:
        g += chevron(x, y1, 0, -1, c, w, 13) + chevron(x, y2, 0, 1, c, w, 13)
    else:
        g += chevron(x, y1, 0, 1, c, w, 13) + chevron(x, y2, 0, -1, c, w, 13)
    return g
def axis(x1, x2, y):
    return line(x1, y, x2, y, "currentColor", 1.4, "", .7)
def dot(x, y, c="currentColor", r=3.5):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'
def obj(x, ay, by, c=ORG, w=3.4):
    """Vật/ảnh thật: mũi tên liền từ A (trên trục) tới B."""
    return line(x, ay, x, by, c, w) + chevron(x, by, 0, by - ay, c, w, 11)
def img(x, ay, by, real, c=BLUE):
    if real:
        return obj(x, ay, by, c, 3.4)
    return line(x, ay, x, by, c, 3, "5 4") + chevron(x, by, 0, by - ay, c, 2.6, 11)

def image(d, f, h):
    """d > 0; f > 0 hội tụ, f < 0 phân kì. Trả về d' (có dấu) và chiều cao ảnh có dấu (lên trên dương)."""
    dp = d * f / (d - f)
    return dp, -dp / d * h

def inter(p1, q1, p2, q2):
    """Giao điểm hai đường thẳng p1q1, p2q2."""
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, q1, p2, q2
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    a, b = x1 * y2 - y1 * x2, x3 * y4 - y3 * x4
    return ((a * (x3 - x4) - (x1 - x2) * b) / den, (a * (y3 - y4) - (y1 - y2) * b) / den)

def close(p, q, tol=0.05):
    return abs(p[0] - q[0]) < tol and abs(p[1] - q[1]) < tol

LENSFILL = "rgba(56,189,248,.18)"
def badge(cx, cy, n, c=RED):
    """Số thứ tự tia trong vòng tròn (tự vẽ, không dùng ký tự ①: font thiếu, vẽ nhỏ)."""
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="13" fill="none" stroke="{c}" stroke-width="1.8"/>'
            + text(cx, cy + 6, str(n), c, 17, "middle", "700"))

# ---------- Hình 1: cảnh mở bài (chỉ vẽ cái nhìn thấy, không vẽ tia, không nói tới tiêu cự)
b = ""
# (a) kính sát trang sách
b += f'<rect x="14" y="40" width="190" height="170" rx="6" fill="rgba(251,146,60,.07)" stroke="currentColor" stroke-width="1.4" opacity=".8"/>'
for k in range(7):
    yy = 62 + k * 22
    b += line(28, yy, 190, yy, "currentColor", 2.2, "", .28)
b += f'<circle cx="108" cy="122" r="62" fill="{LENSFILL}" stroke="currentColor" stroke-width="3"/>'
b += line(152, 166, 196, 214, "currentColor", 9)
b += f'<text x="108" y="140" fill="currentColor" font-size="50" font-weight="700" text-anchor="middle">Aa</text>'
b += T(16, 248, "(a) kính sát trang sách", "currentColor", 17)
b += T(16, 270, "chữ to, đứng thẳng", GRN, 17, "start", "600")
# (b) nhìn ngôi nhà ở xa qua kính
cx, cy = 320, 122
b += f'<circle cx="{cx}" cy="{cy}" r="62" fill="{LENSFILL}" stroke="currentColor" stroke-width="3"/>'
b += line(cx + 44, cy + 44, cx + 88, cy + 92, "currentColor", 9)
house = (f'<g transform="rotate(180 {cx} {cy})"><polygon points="{cx-18},{cy+16} {cx+18},{cy+16} {cx+18},{cy-6} {cx},{cy-22} {cx-18},{cy-6}" '
         f'fill="none" stroke="{ORG}" stroke-width="2.6" stroke-linejoin="round"/>'
         f'<rect x="{cx-5}" y="{cy+2}" width="10" height="14" fill="none" stroke="{ORG}" stroke-width="2"/></g>')
b += house
b += T(228, 248, "(b) nhìn ngôi nhà", "currentColor", 17)
b += T(228, 270, "nhỏ, lộn ngược", GRN, 17, "start", "600")
fig1 = wrap("0 0 420 284", "Hai lần nhìn qua cùng một kính lúp: chữ trên trang sách to và đứng thẳng; ngôi nhà ở xa nhỏ và lộn ngược", b,
            "Hình 1. Cùng một kính lúp: (a) đặt sát trang sách, chữ to và đứng thẳng; (b) duỗi tay nhìn ngôi nhà bên kia đường, ngôi nhà nhỏ và lộn ngược.")

# ---------- Hình 2: tiết diện thấu kính + kí hiệu
def S(d): return f'<path d="{d}" fill="{LENSFILL}" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>'
b = ""
y1 = 92
b += S(f"M50,{y1-45} Q78,{y1} 50,{y1+45} Q22,{y1} 50,{y1-45} Z")                 # hai mặt lồi
b += S(f"M118,{y1-45} L118,{y1+45} Q156,{y1} 118,{y1-45} Z")                       # phẳng - lồi
b += S(f"M190,{y1-45} Q226,{y1} 190,{y1+45} Q206,{y1} 190,{y1-45} Z")              # lõm - lồi (rìa mỏng)
y2 = 236
b += S(f"M32,{y2-45} L68,{y2-45} Q52,{y2} 68,{y2+45} L32,{y2+45} Q48,{y2} 32,{y2-45} Z")      # hai mặt lõm
b += S(f"M112,{y2-45} L144,{y2-45} Q124,{y2} 144,{y2+45} L112,{y2+45} Z")                       # phẳng - lõm
b += S(f"M178,{y2-45} L204,{y2-45} Q222,{y2} 204,{y2+45} L178,{y2+45} Q206,{y2} 178,{y2-45} Z")  # lồi - lõm (rìa dày)
b += line(250, 30, 250, 290, "currentColor", 1, "", .35)
b += lens(330, y1 - 45, y1 + 45, True) + lens(330, y2 - 45, y2 + 45, False)
b += T(14, 24, "Rìa mỏng: hội tụ", GRN, 18)
b += T(14, 170, "Rìa dày: phân kì", BLUE, 18)
b += T(330, 24, "kí hiệu", "currentColor", 17, "middle", "600")
b += T(330, 170, "kí hiệu", "currentColor", 17, "middle", "600")
fig2 = wrap("0 0 420 296", "Ba tiết diện thấu kính rìa mỏng và kí hiệu thấu kính hội tụ; ba tiết diện thấu kính rìa dày và kí hiệu thấu kính phân kì", b,
            "Hình 2. Hàng trên: thấu kính rìa mỏng (hội tụ), kí hiệu có hai đầu V hướng ra. Hàng dưới: thấu kính rìa dày (phân kì), kí hiệu có hai đầu V hướng vào.")

# ---------- Hình 3: tiêu điểm của hai loại thấu kính (chùm tới song song trục chính)
b = ""
f3 = 105
for k, conv in enumerate((True, False)):
    Ay = 104 + k * 236
    Ox = 210
    b += axis(16, 404, Ay) + lens(Ox, Ay - 86, Ay + 86, conv)
    Fp = Ox + f3 if conv else Ox - f3        # F' : hội tụ phía sau, phân kì phía trước
    Fv = Ox - f3 if conv else Ox + f3
    for Y in (70, 40, -40, -70):
        y = Ay - Y
        b += ray(26, y, Ox, y, RED, 2.2, 0.45)
        if conv:
            # tia ló qua F': kéo tới x = 400
            t = (400 - Ox) / (Fp - Ox)
            b += ray(Ox, y, Ox + (Fp - Ox) * t, y + (Ay - y) * t, RED, 2.2, 0.3)
        else:
            # tia ló nằm trên đường F' -> (Ox, y), kéo tới x = 330
            dx, dy = Ox - Fp, y - Ay
            t = (280 - Ox) / dx
            b += ray(Ox, y, 280, y + dy * t, RED, 2.2, 0.55) + ext(Ox, y, Fp, Ay)
    b += dot(Fp, Ay) + dot(Fv, Ay) + dot(Ox, Ay)
    b += T(Fp, Ay + 32, "F'", "currentColor", 18, "middle")
    b += T(Fv, Ay + 32, "F", "currentColor", 18, "middle")
    b += T(Ox + 8, Ay + 26, "O", "currentColor", 18)
    b += T(16, Ay - 84, "(a) hội tụ" if conv else "(b) phân kì", GRN if conv else BLUE, 17)
b += T(404, 104 - 12, "Δ", "currentColor", 18, "end")
fig3 = wrap("0 0 420 470", "Chùm tia song song trục chính: qua thấu kính hội tụ gặp nhau tại tiêu điểm F' phía sau; qua thấu kính phân kì loe ra, đường kéo dài gặp nhau tại F' phía trước", b,
            "Hình 3. (a) Thấu kính hội tụ: tia ló gặp nhau thật tại F'. (b) Thấu kính phân kì: tia ló loe ra, đường kéo dài (nét đứt) gặp nhau tại F' ở phía trước kính. OF = OF' = f.")

# ---------- Hình 4: ba tia đặc biệt, thấu kính hội tụ, d = 2,5f (ảnh thật nhỏ)
f4, d4, h4 = 60, 150, 60
dp4, hp4 = image(d4, f4, h4)
assert abs(dp4 - 100) < 1e-9 and abs(hp4 + 40) < 1e-9
Ox, Ay = 205, 140
X = lambda u: Ox + u
Y = lambda v: Ay - v
Bx, By = X(-d4), Y(h4)
Bpx, Bpy = X(dp4), Y(hp4)
b = axis(14, 410, Ay) + lens(Ox, Y(84), Y(-84), True)
# tia 1: qua O
e1 = (X(dp4 + 45), Y(-h4 / d4 * (dp4 + 45)))
b += ray(Bx, By, Ox, Ay, RED, 2.4, 0.5) + ray(Ox, Ay, *e1, RED, 2.4, 0.4)
# tia 2: song song -> qua F'
e2 = (X(dp4 + 45), Y(h4 - h4 / f4 * (dp4 + 45)))
b += ray(Bx, By, Ox, By, RED, 2.4, 0.5) + ray(Ox, By, *e2, RED, 2.4, 0.3)
# tia 3: qua F -> song song
y3 = -h4 * f4 / (d4 - f4)
b += ray(Bx, By, Ox, Y(y3), RED, 2.4, 0.42) + ray(Ox, Y(y3), X(dp4 + 70), Y(y3), RED, 2.4, 0.3)
# kiểm: 3 tia gặp nhau đúng tại B'
assert close(inter((Bx, By), (Ox, Ay), (Ox, By), (X(f4), Ay)), (Bpx, Bpy))
assert close(inter((Bx, By), (Ox, Ay), (Ox, Y(y3)), (X(dp4), Y(y3))), (Bpx, Bpy))
assert abs(y3 - hp4) < 1e-9
b += obj(Bx, Ay, By) + img(Bpx, Ay, Bpy, True)
b += dot(X(-f4), Ay) + dot(X(f4), Ay)
b += T(X(-f4), Ay + 26, "F", "currentColor", 18, "middle") + T(X(f4) + 8, Ay - 10, "F'", "currentColor", 18)
b += T(Ox - 8, Ay - 8, "O", "currentColor", 18, "end")
b += T(Bx - 6, By - 4, "B", ORG, 18, "end") + T(Bx - 6, Ay + 22, "A", ORG, 18, "end")
b += T(Bpx - 8, Bpy + 26, "B'", BLUE, 18, "end") + T(Bpx + 8, Ay - 8, "A'", BLUE, 18)
b += badge(150, 99, 1) + badge(130, 62, 2) + badge(92, 122, 3)
b += T(412, Ay - 8, "Δ", "currentColor", 18, "end")
fig4 = wrap("0 0 420 252", "Ba tia đặc biệt từ đỉnh B qua thấu kính hội tụ: tia qua quang tâm đi thẳng, tia song song ló qua F', tia qua F ló song song; ba tia ló gặp nhau tại B'", b,
            "Hình 4. Ba tia đặc biệt từ B: ① qua O đi thẳng; ② song song trục chính, ló qua F'; ③ qua F, ló song song trục chính. Ba tia ló gặp nhau tại B'. Ở đây vật cách kính 2,5f.")

# ---------- Hình 5: ba trường hợp (a) f < d < 2f; (b) d < f; (c) thấu kính phân kì
b = ""
CASES = (
    # (f, d, h, Ox, Ay_off, tiêu đề, xmax tia)
    (50, 80, 40, 130, 72, "(a) hội tụ, f < d < 2f", 330),
    (80, 48, 36, 250, 112, "(b) hội tụ, d < f", 360),
    (-80, 120, 84, 250, 130, "(c) phân kì", 300),
)
geo5 = []
py = 0
for idx, (f, d, h, Ox, ayo, title, xend) in enumerate(CASES):
    Ay = py + ayo
    X = lambda u, Ox=Ox: Ox + u
    Y = lambda v, Ay=Ay: Ay - v
    dp, hp = image(d, f, h)
    geo5.append((f, d, h, dp, hp))
    real = dp > 0
    Bx, By, Bpx, Bpy = X(-d), Y(h), X(dp), Y(hp)
    top = min(By, Bpy) - 18
    bot = max(Ay + 40, Bpy + 16)
    ext_l = 16 if idx == 2 else 22
    b += axis(14, 410, Ay) + lens(Ox, Y(max(h, 30) + ext_l), Y(-max(h, 30) - ext_l), f > 0)
    Fp = (X(f), Ay)                     # F' (hội tụ: phía sau; phân kì: f âm -> phía trước)
    Fv = (X(-f), Ay)
    # tia 1 qua O
    u1 = xend - Ox
    b += ray(Bx, By, Ox, Ay, RED, 2.4, 0.5) + ray(Ox, Ay, X(u1), Y(-h / d * u1), RED, 2.4, 0.5)
    # tia 2 song song -> (kéo dài) qua F'
    u2 = xend - Ox
    if f > 0:
        y2e = h - h / f * u2
    else:
        y2e = h + h / (-f) * u2
    if idx == 2:                          # giới hạn để không vượt khung trên
        u2 = 34; y2e = h + h / (-f) * u2
    b += ray(Bx, By, Ox, By, RED, 2.4, 0.5) + ray(Ox, By, X(u2), Y(y2e), RED, 2.4, 0.5)
    # giao điểm hai tia ló (hoặc đường kéo dài)
    q = inter((Bx, By), (Ox, Ay), (Ox, By), Fp)
    assert close(q, (Bpx, Bpy)), (idx, q, (Bpx, Bpy))
    if not real:
        b += ext(Ox, By, Bpx, Bpy)               # kéo dài ngược tia 2
        if f > 0:
            b += ext(Ox, Ay, Bpx, Bpy)           # kéo dài ngược tia 1 (b: B' nằm ngoài đoạn BO)
        if f < 0:
            b += ext(Bpx, Bpy, Fp[0], Fp[1])     # tiếp tới F'
    b += obj(Bx, Ay, By) + img(Bpx, Ay, Bpy, real)
    b += dot(*Fp) + dot(*Fv) + dot(Ox, Ay)
    if f > 0:
        b += T(Fp[0] + 8, Ay - 10, "F'", "currentColor", 18)
    else:
        b += T(Fp[0], Ay + 26, "F'", "currentColor", 18, "middle")
    b += T(Fv[0], Ay + 26, "F", "currentColor", 18, "middle")
    b += T(Ox - 7, Ay + 24, "O", "currentColor", 18, "end")
    b += T(Bx - 8, By + 20, "B", ORG, 18, "end")
    if idx == 0:
        b += T(Bpx - 8, Bpy + 26, "B'", BLUE, 18, "end")
    elif idx == 1:
        b += T(Bpx - 8, Bpy + 6, "B'", BLUE, 18, "end")
    else:   # nhãn trong tam giác B – (0,h) – B', có đường dẫn tới B'
        b += T(X(-55), Y(60), "B'", BLUE, 18, "middle") + line(X(-52), Y(56), X(-49), Y(hp + 5), BLUE, 1.2)
    b += T(406, py + 22, title.replace("<", "&lt;"), GRN if f > 0 else BLUE, 17, "end")
    if idx < 2:
        b += line(14, py + 214 if idx == 0 else py + 222, 406, py + 214 if idx == 0 else py + 222, "currentColor", 1, "", .3)
    py += 222 if idx == 0 else (232 if idx == 1 else 244)
H5 = py
(fa, da, ha, dpa, hpa), (fb, db, hb, dpb, hpb), (fc, dc, hc, dpc, hpc) = geo5
assert dpa > 2 * fa and -hpa > ha            # (a) ảnh thật, xa hơn 2f, lớn hơn
assert dpb < 0 and hpb > hb                  # (b) ảnh ảo, cùng chiều, lớn hơn
assert dpc < 0 and 0 < hpc < hc and -dpc < -fc   # (c) ảo, cùng chiều, nhỏ, trong OF'
fig5 = wrap(f"0 0 420 {H5}", "Dựng ảnh bằng hai tia: (a) thấu kính hội tụ, vật giữa F và 2F, ảnh thật ngược chiều lớn hơn; (b) vật trong tiêu cự, ảnh ảo cùng chiều lớn hơn; (c) thấu kính phân kì, ảnh ảo cùng chiều nhỏ hơn", b,
            "Hình 5. Dựng ảnh bằng tia ① và tia ②. (a) Ảnh thật, ngược chiều, lớn hơn vật. (b) Vật trong tiêu cự: tia ló loe ra, kéo dài ngược (nét đứt) mới gặp nhau, ảnh ảo cùng chiều, lớn hơn. (c) Thấu kính phân kì: ảnh ảo, cùng chiều, nhỏ hơn, nằm giữa O và F'.")

# ---------- Hình 6: che nửa dưới thấu kính, ảnh vẫn đủ
f6, d6, h6 = 60, 150, 50
dp6, hp6 = image(d6, f6, h6)
Ox, Ay = 205, 120
X = lambda u: Ox + u
Y = lambda v: Ay - v
Bx, By, Bpx, Bpy = X(-d6), Y(h6), X(dp6), Y(hp6)
Ax, Apx = X(-d6), X(dp6)
b = axis(14, 410, Ay) + lens(Ox, Y(80), Y(-80), True)
b += f'<rect x="{Ox-7}" y="{Ay+3}" width="14" height="78" fill="rgba(15,15,20,.9)" stroke="currentColor" stroke-width="1.5"/>'
def lens_out(src, Yp, f=f6):
    """Tia từ src=(u,v) tới điểm (0, Yp) của thấu kính mỏng: hệ số góc ló = hệ số góc tới - Yp/f."""
    m_in = (Yp - src[1]) / (0 - src[0])
    return m_in - Yp / f
for Yp in (70, 30):                # tia từ B qua nửa trên, hội tụ tại B'
    assert abs(Yp + lens_out((-d6, h6), Yp) * dp6 - hp6) < 1e-9
    b += ray(Bx, By, Ox, Y(Yp), RED, 2.2, 0.5) + ray(Ox, Y(Yp), Bpx, Bpy, RED, 2.2, 0.5)
for Yp in (50,):                   # tia từ A qua nửa trên, hội tụ tại A'
    assert abs(Yp + lens_out((-d6, 0), Yp) * dp6) < 1e-9
    b += ray(Ax, Ay, Ox, Y(Yp), ORG, 2, 0.5) + ray(Ox, Y(Yp), Apx, Ay, ORG, 2, 0.5)
for Yp in (-30, -65):              # tia từ B tới nửa dưới: bị chặn
    b += line(Bx, By, Ox - 7, Y(Yp) + 0.0, RED, 1.6, "3 4", .45)
b += obj(Bx, Ay, By) + img(Bpx, Ay, Bpy, True)
b += T(Bx - 8, By + 20, "B", ORG, 18, "end") + T(Ax - 8, Ay + 24, "A", ORG, 18, "end")
b += T(Bpx + 8, Bpy + 16, "B'", BLUE, 18) + T(Apx + 8, Ay - 8, "A'", BLUE, 18)
b += T(Ox + 20, Ay + 60, "giấy đen", "currentColor", 17)
b += T(Ox + 20, Ay + 80, "che nửa dưới", "currentColor", 17)
b += T(250, Ay + 116, "ảnh vẫn đủ A'B'", BLUE, 17, "start", "700")
# kiểm hình học: mọi tia qua thấu kính mỏng từ B ló tới B' <=> B' là giao tia 1 và tia 2
assert close(inter((Bx, By), (Ox, Ay), (Ox, By), (X(f6), Ay)), (Bpx, Bpy))
fig6 = wrap("0 0 420 252", "Nửa dưới thấu kính bị che; các tia từ B và từ A đi qua nửa trên vẫn hội tụ tại B' và A', ảnh đủ nhưng tối hơn", b,
            "Hình 6. Nửa dưới thấu kính bị che. Tia từ B và tia từ A qua nửa trên vẫn gặp nhau tại B' và A': ảnh đủ hình, chỉ tối hơn vì nhận ít ánh sáng.")

# ---------- Bảng số liệu thí nghiệm 3 (số liệu minh hoạ: d' mô hình f = 10 cm + độ lệch khi tìm ảnh rõ)
F3 = 10.0
D3 = (12, 16, 24, 36, 50)
LECH = (-3.0, 0.2, 0.1, -0.05, 0.05)          # độ lệch khi tìm chỗ ảnh rõ (cm), d gần f lệch nhiều nhất
rows = []
for d_, e in zip(D3, LECH):
    dp_true = d_ * F3 / (d_ - F3)
    dp_doc = round(dp_true + e, 1)
    rows.append((d_, dp_true, dp_doc, d_ * dp_doc / (d_ + dp_doc)))
fs = [r[3] for r in rows]
mean = sum(fs) / len(fs)
dev = [abs(x - F3) for x in fs]
mx = max(dev)
worst = [r for r, dv in zip(rows, dev) if abs(dv - mx) < 1e-6]
assert len(worst) == 1 and worst[0][0] == 12, worst
wd, wdt, wdd, wf = worst[0]
bang = "\n".join(f"<tr><td>$d = {d_};\\ d' = {vn(dd, 1)}$</td><td>${vn(fx, 2)}$</td></tr>" for d_, _, dd, fx in rows)
nx = (f"trung bình ${vn(mean, 2)}\\ \\text{{cm}},$ rất gần $10\\ \\text{{cm}}.$ Lệch nhiều nhất là lần $d = {wd}\\ \\text{{cm}}$ "
      f"($f \\approx {vn(wf, 2)}\\ \\text{{cm}}){{:}}$ ảnh ở xa, to và rõ trong một đoạn dài nên khó chọn đúng chỗ rõ nhất "
      f"(theo mô hình $d' = {vn(wdt, 0)}\\ \\text{{cm}},$ đọc được ${vn(wdd, 1)}\\ \\text{{cm}}).$ "
      f"Sai số chủ yếu do tìm ảnh rõ bằng mắt và đặt tâm thấu kính lệch vạch; đo nhiều lần rồi lấy trung bình.")
DTXT = ";\\ ".join(str(x) for x in D3) + "\\ \\text{cm}"

h = (HERE / "theory.src.html").read_text(encoding="utf8")
h = (h.replace("__D_TN3__", DTXT).replace("__BANG_TN3__", bang).replace("__NHAN_XET_TN3__", nx)
      .replace("__PHUT__", str(PHUT)))
for n, fg in enumerate((fig1, fig2, fig3, fig4, fig5, fig6), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", fg)
assert "__" not in h.replace("___", "")
(HERE / "theory.html").write_text(h, encoding="utf8")

# ---------- Kho thí nghiệm
BAI = "Bài 8. Thấu kính"
SRC = "content/lesson-samples/l9-thau-kinh/theory.html"
base = {"mon": "vat-ly", "lop": 9, "bai": BAI, "lesson_id": 86, "nguon_trong_bai": SRC}
tn = []
tn.append({**base,
  "id": "tn-l9-thaukinh-01", "ten": "Ba vệt sáng song song qua thấu kính rìa mỏng và rìa dày", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["thaukinh.nhan_biet", "thaukinh.tieu_diem"],
  "muc_tieu": "Thấy chùm sáng song song hội tụ sau thấu kính rìa mỏng và loe ra sau thấu kính rìa dày.",
  "dung_cu": [{"ten": "Hộp đèn ba khe (hoặc đèn pin + tấm bìa có ba khe hẹp)", "so_luong": 1},
              {"ten": "Thấu kính rìa mỏng (tiết diện phẳng, đặt đứng trên giấy)", "so_luong": 1},
              {"ten": "Thấu kính rìa dày (tiết diện phẳng)", "so_luong": 1},
              {"ten": "Tờ giấy trắng khổ A4", "so_luong": 1}],
  "cac_buoc": {"lam": ["Đặt hộp đèn trên giấy trắng để có ba vệt sáng song song.",
                       "Đặt thấu kính rìa mỏng chắn ngang ba vệt, vuông góc với vệt giữa.",
                       "Thay bằng thấu kính rìa dày, giữ nguyên vị trí."],
               "quan_sat": ["Sau kính rìa mỏng, ba vệt gặp nhau tại một điểm.",
                            "Sau kính rìa dày, ba vệt toả rộng ra, không gặp nhau.",
                            "Vệt giữa (đi qua tâm kính) không đổi hướng."],
               "rut_ra": ["Thấu kính rìa mỏng là thấu kính hội tụ; điểm gặp nhau là tiêu điểm F'.",
                          "Thấu kính rìa dày là thấu kính phân kì; đường kéo dài của các tia ló gặp nhau tại F' phía trước kính.",
                          "Tia qua quang tâm đi thẳng."]},
  "tham_so": [{"ky_hieu": "f", "ten": "Tiêu cự (có dấu: hội tụ dương, phân kì âm)", "don_vi": "cm", "kieu": "dieu_chinh", "min": -20, "max": 20, "mac_dinh": 10, "buoc": 1},
              {"ky_hieu": "y", "ten": "Khoảng cách từ vệt sáng tới trục chính", "don_vi": "cm", "kieu": "dieu_chinh", "min": -3, "max": 3, "mac_dinh": 2, "buoc": 0.5},
              {"ky_hieu": "goc", "ten": "Góc lệch của tia ló so với trục chính", "don_vi": "độ", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["tia ló (hoặc đường kéo dài) đi qua F' = (f, 0)", "tan(goc) = y / f"],
              "gia_thiet": ["thấu kính mỏng", "tia gần trục chính", "ánh sáng đơn sắc"]},
  "so_lieu_mau": {"cot": ["y (cm)", "góc lệch với f = 10 cm (độ)", "góc lệch với f = -10 cm (độ)"],
                  "hang": [[y, round(math.degrees(math.atan(y / 10)), 1), round(-math.degrees(math.atan(y / 10)), 1) + 0.0] for y in (-2, 0, 2)],
                  "ghi_chu": "Số liệu minh hoạ tính từ mô hình thấu kính mỏng; thí nghiệm này chỉ quan sát định tính. Góc dương: tia ló đi về phía trục chính."},
  "ket_qua_ky_vong": "Rìa mỏng: ba tia gặp nhau tại F' sau kính. Rìa dày: ba tia loe ra, kéo dài ngược gặp nhau tại F' trước kính.",
  "hien_tuong_hay_sai": ["Tưởng thấu kính phân kì cũng có điểm sáng thật phía sau.",
                         "Tưởng tia qua tâm thấu kính cũng bị bẻ cong.",
                         "Nhận biết thấu kính theo độ to nhỏ thay vì theo rìa mỏng/rìa dày."],
  "an_toan": "Không nhìn thẳng vào đèn khe; hộp đèn có thể nóng.",
  "goi_y_mo_phong": {"loai": "2d_dong_hoc", "y_tuong": "Kéo thanh trượt f từ âm sang dương, ba tia song song qua kính cập nhật; đổi kí hiệu kính tương ứng.",
                     "diem_nhan": "Với f âm, vẽ đường kéo dài nét đứt gặp nhau tại F' phía trước."}})
D_XA = 400.0
F_KL = 10.0
tn.append({**base,
  "id": "tn-l9-thaukinh-02", "ten": "Hứng ảnh cửa sổ lên tờ giấy bằng kính lúp", "loai": "thi_nghiem", "muc_do": "co_ban",
  "kien_thuc": ["thaukinh.anh_that", "thaukinh.do_tieu_cu_nhanh"],
  "muc_tieu": "Thấy ảnh thật, ngược chiều, nhỏ của vật ở xa hứng được trên giấy, và đo nhanh tiêu cự.",
  "dung_cu": [{"ten": "Kính lúp (thấu kính hội tụ)", "so_luong": 1},
              {"ten": "Tờ giấy trắng hoặc bìa cứng", "so_luong": 1},
              {"ten": "Thước kẻ", "so_luong": 1}],
  "cac_buoc": {"lam": ["Đứng cách cửa sổ vài mét, quay mặt về phía cửa sổ; cầm tờ giấy trắng phía sau kính lúp (xa cửa sổ hơn).",
                       "Dịch tờ giấy tới lui đến khi thấy hình cửa sổ rõ nét.",
                       "Đo khoảng cách từ kính tới giấy."],
               "quan_sat": ["Hình cửa sổ nhỏ, lộn ngược, rõ nét trên giấy.",
                            "Khoảng cách kính – giấy gần bằng tiêu cự ghi trên kính."],
               "rut_ra": ["Vật rất xa cho ảnh thật, ngược chiều, nhỏ hơn vật, nằm gần tiêu điểm F'.",
                          "Ảnh thật hứng được trên màn."]},
  "tham_so": [{"ky_hieu": "d", "ten": "Khoảng cách cửa sổ tới kính", "don_vi": "cm", "kieu": "dieu_chinh", "min": 100, "max": 1000, "mac_dinh": D_XA, "buoc": 50},
              {"ky_hieu": "f", "ten": "Tiêu cự kính lúp", "don_vi": "cm", "kieu": "co_dinh", "gia_tri": F_KL},
              {"ky_hieu": "d'", "ten": "Khoảng cách giấy tới kính khi ảnh rõ", "don_vi": "cm", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["1/f = 1/d + 1/d'", "h'/h = d'/d"],
              "gia_thiet": ["thấu kính mỏng", "cửa sổ coi như vật phẳng vuông góc trục chính"]},
  "so_lieu_mau": {"cot": ["d (cm)", "d' (cm)", "d' - f (cm)"],
                  "hang": [[d_, round(d_ * F_KL / (d_ - F_KL), 2), round(d_ * F_KL / (d_ - F_KL) - F_KL, 2)] for d_ in (200, 400, 800)],
                  "ghi_chu": "Số liệu minh hoạ tính từ mô hình f = 10 cm: vật càng xa, ảnh càng sát F'."},
  "ket_qua_ky_vong": "Ảnh cửa sổ lộn ngược, nhỏ, rõ nét khi giấy cách kính khoảng f.",
  "hien_tuong_hay_sai": ["Tưởng ảnh hứng trên giấy là bóng của kính.", "Tưởng ảnh qua kính lúp lúc nào cũng to và cùng chiều."],
  "an_toan": "Không hướng kính lúp về phía Mặt Trời khi đang nhìn qua kính.",
  "goi_y_mo_phong": {"loai": "2d_dong_hoc", "y_tuong": "Kéo vị trí tờ giấy, ảnh nhoè thành vệt khi lệch khỏi d', rõ nét tại d'.",
                     "diem_nhan": "Vật càng xa, chỗ ảnh rõ càng tiến sát F'."}})
tn.append({**base,
  "id": "tn-l9-thaukinh-03", "ten": "Đo d, d' trên thước quang học và tính tiêu cự", "loai": "thi_nghiem", "muc_do": "trung_binh",
  "kien_thuc": ["thaukinh.cong_thuc", "thaukinh.anh_that"],
  "muc_tieu": "Từ các cặp d, d' đo được, thấy f = d·d'/(d + d') gần như không đổi.",
  "dung_cu": [{"ten": "Thước quang học dài 1 m, chia 1 mm", "so_luong": 1},
              {"ten": "Đèn LED hình chữ F", "so_luong": 1},
              {"ten": "Thấu kính hội tụ ghi f = 10 cm", "so_luong": 1},
              {"ten": "Màn ảnh", "so_luong": 1}],
  "cac_buoc": {"lam": ["Đặt đèn chữ F, thấu kính, màn trên thước.",
                       "Đặt vật lần lượt cách thấu kính d = " + ", ".join(f"{x}" for x in D3) + " cm.",
                       "Mỗi lần dịch màn tới chỗ ảnh rõ nhất, đọc d'."],
               "quan_sat": ["d giảm thì d' tăng, ảnh to dần.", "Khi d gần f, ảnh rõ trong một đoạn dài."],
               "rut_ra": ["f = d·d'/(d + d') gần như không đổi, xấp xỉ 10 cm.",
                          "Sai lệch lớn nhất khi d gần f vì khó chọn chỗ ảnh rõ nhất."]},
  "tham_so": [{"ky_hieu": "d", "ten": "Khoảng cách vật tới thấu kính", "don_vi": "cm", "kieu": "dieu_chinh", "min": 11, "max": 50, "mac_dinh": 20, "buoc": 1},
              {"ky_hieu": "f", "ten": "Tiêu cự", "don_vi": "cm", "kieu": "co_dinh", "gia_tri": F3},
              {"ky_hieu": "d'", "ten": "Khoảng cách ảnh tới thấu kính", "don_vi": "cm", "kieu": "do_duoc", "sai_so_do": 0.1},
              {"ky_hieu": "f_tn", "ten": "Tiêu cự tính từ số đo", "don_vi": "cm", "kieu": "tinh_ra"}],
  "mo_hinh": {"phuong_trinh": ["1/f = 1/d + 1/d'", "d' = d·f/(d - f)", "d'_doc = lam_tron(d' + lech, 0,1 cm)", "f_tn = d·d'_doc/(d + d'_doc)"],
              "gia_thiet": ["thấu kính mỏng", "lech là độ lệch khi tìm chỗ ảnh rõ: " + ", ".join(str(e) for e in LECH) + " cm"]},
  "so_lieu_mau": {"cot": ["d (cm)", "d' đọc (cm)", "f tính ra (cm)"],
                  "hang": [[d_, dd, round(fx, 2)] for d_, _, dd, fx in rows],
                  "ghi_chu": f"Số liệu minh hoạ: d' tính từ f = 10 cm cộng độ lệch tìm ảnh rõ, chưa phải số đo thật. Trung bình f = {mean:.2f} cm."},
  "ket_qua_ky_vong": f"f trung bình khoảng {mean:.2f} cm; lệch nhiều nhất ở d = {wd} cm.",
  "hien_tuong_hay_sai": ["Tính f = d + d' hoặc f = (d + d')/2.", "Dịch màn đến chỗ ảnh to nhất thay vì rõ nhất."],
  "sai_so_thuong_gap": "Tìm chỗ ảnh rõ bằng mắt (nhất là khi d gần f), tâm thấu kính không trùng vạch đọc.",
  "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu", "y_tuong": "Kéo vị trí vật và màn; ảnh nhoè theo độ lệch khỏi d'; bảng tự tính f.",
                     "diem_nhan": "d gần f thì vùng ảnh rõ kéo dài, sai số lớn."}})
for dct in tn:
    p = ROOT / "content" / "thi-nghiem" / f"{dct['id']}.json"
    p.write_text(json.dumps(dct, ensure_ascii=False, indent=1), encoding="utf8")

print("ok", len(h), "| H5 =", H5, "| geo5:", [(round(a[3], 2), round(a[4], 2)) for a in geo5],
      "| tn3 mean=%.3f worst d=%d" % (mean, wd), "| f:", [round(x, 3) for x in fs])
