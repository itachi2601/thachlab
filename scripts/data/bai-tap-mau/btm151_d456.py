"""Bài tập mẫu CĐ06 "Khúc xạ ánh sáng, phản xạ toàn phần, lăng kính và tán sắc" (khoá Vật lí HSG & chuyên KHTN 9) — lesson 151.
Phần Dạng 4–7 (module được build-hinh-151.py import). Dàn ý + số liệu: content/hsg9/cd06-khuc-xa-phan-xa-toan-phan/nguon.md
(số đã tính trong tinh.py cùng thư mục; dùng nguyên). Dạng sau dùng lại cách làm dạng trước:
  D4 bản mặt song song (định luật khúc xạ của D1 viết hai lần + hình học tam giác vuông)
  D5 lăng kính, tia tới vuông góc mặt bên: góc lệch và tán sắc (khúc xạ một lần ở mặt AC; điều kiện ló = PXTP của D3)
  D6 lăng kính phản xạ toàn phần (góc tới ở mặt bên + điều kiện PXTP; đổi môi trường ngoài)
  D7 sợi quang định lượng (PXTP ở thành + khúc xạ ở đầu sợi + v = c/n).
Lăng kính chỉ xét tia tới vuông góc mặt bên (không ra bài tia xiên).
Xuất DANG, BUILD, ANALYSIS, SOLS, STEPS (4 phần tử mỗi list) và kiem_so()."""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *  # noqa: F401,F403  (fig, seg, lbl, dot, arc, chevron, arrow, sol, M, P, A, buoc …)

T_KX = "Chiết suất và định luật khúc xạ ánh sáng"
T_PXTP = "Điều kiện xảy ra phản xạ toàn phần"
T_LK = "Đường truyền tia sáng qua lăng kính"
T_TS = "Tán sắc ánh sáng qua lăng kính"
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"
GLASS = "#38bdf8"
VIO = "#a78bfa"
YEL = "#facc15"


# ═════════════ SỐ LIỆU (mọi đáp số tính ở đây, kiem_so() kiểm lại) ═════════════
def sind(a): return math.sin(math.radians(a))
def cosd(a): return math.cos(math.radians(a))
def tand(a): return math.tan(math.radians(a))
def asind(x): return math.degrees(math.asin(x))

NW = 4 / 3
C0 = 3e8
# D4 · bản mặt song song e = 6 cm, n = 1,5, i = 60°
E4, N4, I4 = 6.0, 1.5, 60.0
def r_of(i, n=N4): return asind(sind(i) / n)
def d_of(i, e=E4, n=N4):
    r = r_of(i, n)
    return e * sind(i - r) / cosd(r)
R4 = r_of(I4)                                   # 35,26°
IJ4 = E4 / cosd(R4)                             # 7,35 cm
D4 = d_of(I4)                                   # 3,07 cm
D4_TAB = {30: d_of(30), 45: d_of(45), 60: D4, 75: d_of(75)}   # 1,16 · 1,97 · 3,07 · 4,49
DEL4 = E4 * (1 - 1 / N4)                        # 2 cm
# D5 · lăng kính A = 30°, tia ⊥ AB; n_đ = 1,50, n_t = 1,54
A5, ND, NT, L5 = 30.0, 1.50, 1.54, 1.2
R2D, R2T = asind(ND * sind(A5)), asind(NT * sind(A5))       # 48,59° · 50,35°
DD5, DT5 = R2D - A5, R2T - A5                               # 18,59° · 20,35°
MO5 = DT5 - DD5                                             # 1,76°
W5 = 100 * L5 * (tand(DT5) - tand(DD5))                      # 4,16 cm
A5B = 41.0
IGH_D, IGH_T = asind(1 / ND), asind(1 / NT)                 # 41,81° · 40,49°
R2D_B = asind(ND * sind(A5B))                               # 79,8°
NT_SIN_B = NT * sind(A5B)                                   # 1,010 > 1
# D6 · lăng kính vuông cân, n = 1,5, tia ⊥ mặt huyền
N6 = 1.5
I6 = 45.0
IGH6 = asind(1 / N6)                                        # 41,8°
NMIN6 = 1 / sind(I6)                                        # 1,414
NMIN6W = NW / sind(I6)                                      # 1,886
IGH6W = asind(NW / N6)                                      # 62,7°
R6W = asind(N6 * sind(I6) / NW)                             # 52,7°
LECH6 = R6W - I6                                            # 7,7°
# D7 · sợi quang lõi 1,60 / vỏ 1,50, dài 1 km
N1, N2, L7 = 1.60, 1.50, 1000.0
IGH7 = asind(N2 / N1)                                       # 69,64°
TH7 = 90 - IGH7                                             # 20,36°
SIN_IMAX = N1 * sind(TH7)                                   # 0,5568 = √(n1² − n2²)
IMAX7 = asind(SIN_IMAX)                                     # 33,8°
T0_7 = L7 * N1 / C0 * 1e6                                   # 5,333 µs
T1_7 = L7 / cosd(TH7) * N1 / C0 * 1e6                       # 5,689 µs
DT7 = (T1_7 - T0_7) * 1000                                  # 356 ns
IMAX7W = asind(SIN_IMAX / NW)                               # 24,7°


# ═════════════ HÌNH: helper ═════════════
def rich(s, size=14):
    """Nhãn SVG có chỉ số dưới: 'r_{2}' → tspan dy (chỉ số Unicode hiện như dấu phẩy ở một số máy)."""
    ms = list(re.finditer(r"_\{([^}]+)\}", s))
    if not ms:
        return s
    out = s[:ms[0].start()]
    for k, m in enumerate(ms):
        out += f'<tspan dy="4" font-size="{max(12, size - 2)}">{m.group(1)}</tspan>'
        nxt = ms[k + 1].start() if k + 1 < len(ms) else len(s)
        out += f'<tspan dy="-4">{s[m.end():nxt]}</tspan>' if s[m.end():nxt] else '<tspan dy="-4"></tspan>'
    return out

def txt(x, y, s, c="currentColor", size=14, anchor="start", weight="700", extra=""):
    size = max(size, 14)
    t = lbl(x, y, rich(s, size), c, size, anchor, weight)
    return t.replace("<text ", f"<text {extra} ", 1) if extra else t

def show_at(t, dur):
    k = max(0.001, min(0.999, t / dur))
    return (f'<animate attributeName="opacity" values="0;1" keyTimes="0;{k:.4f}" calcMode="discrete" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')

def timed(k, s, x, y, c="currentColor", size=14, anchor="start", weight="700", dur=6.0):
    return txt(x, y, s, c, size, anchor, weight, 'opacity="0"').replace("</text>", show_at(k * dur, dur) + "</text>", 1)

def later(k, svg, dur):
    """Nhóm hình hiện từ phân số k của mô phỏng."""
    return f'<g opacity="0">{svg}{show_at(k * dur, dur)}</g>'

def ray(x1, y1, x2, y2, c=RED, w=2.4, dash="", mid=True):
    """Tia sáng: nét liền + mũi tên chữ V ở giữa tia (đường kéo dài: dash, không mũi tên)."""
    b = seg(x1, y1, x2, y2, c, w, dash)
    if mid and not dash:
        b += chevron((x1 + x2) / 2 + (x2 - x1) * .06, (y1 + y2) / 2 + (y2 - y1) * .06, x2 - x1, y2 - y1, c, w, 10)
    return b

def normal(x, y, ux, uy, L1, L2):
    """Pháp tuyến nét đứt qua (x, y) theo hướng (ux, uy): L1 về một phía, L2 về phía kia."""
    n = math.hypot(ux, uy); ux, uy = ux / n, uy / n
    return seg(x - ux * L1, y - uy * L1, x + ux * L2, y + uy * L2, "currentColor", 1.4, "5 4", .8)

def path_anim(pts, speeds, k0, k1, dur, c=YEL, r=5):
    """Chấm sáng chạy dọc đường gấp khúc pts; speeds[j] = tốc độ trên đoạn j (đúng tỉ lệ c/n), trong [k0, k1] của dur."""
    lens = [math.hypot(pts[j + 1][0] - pts[j][0], pts[j + 1][1] - pts[j][1]) / speeds[j] for j in range(len(pts) - 1)]
    tot = sum(lens)
    kts, acc = [0.0, k0], 0.0
    for L in lens:
        acc += L
        kts.append(k0 + (k1 - k0) * acc / tot)
    kts.append(1.0)
    xs = [pts[0][0]] + [p[0] for p in pts] + [pts[-1][0]]
    ys = [pts[0][1]] + [p[1] for p in pts] + [pts[-1][1]]
    kt = ";".join(f"{k:.4f}" for k in kts)
    return (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="{r}" fill="{c}" stroke="currentColor" stroke-width="1.2">'
            f'<animate attributeName="cx" values="{";".join(f"{v:.1f}" for v in xs)}" keyTimes="{kt}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'
            f'<animate attributeName="cy" values="{";".join(f"{v:.1f}" for v in ys)}" keyTimes="{kt}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'
            '</circle>')

def angle_arc(cx, cy, r, a0, a1, c=ORG):
    """Cung góc (độ, Oy hướng lên), luôn vẽ cung nhỏ từ a0 tới a1 ngược chiều kim đồng hồ."""
    return arc(cx, cy, r, a0, a1, c, 1.8)


# ═════════════ HÌNH ═════════════
# ───────────── Dạng 4 · bản mặt song song ─────────────
Y4T, Y4B, X4I = 92, 172, 150
RD4 = 30.0                                   # góc khúc xạ VẼ (không đúng tỉ lệ, để không đo được đáp số)

def d4_geom():
    ux, uy = sind(I4), cosd(I4)              # hướng tia tới (y xuống)
    S = (X4I - 110 * ux, Y4T - 110 * uy)
    I = (X4I, Y4T)
    J = (X4I + (Y4B - Y4T) * tand(RD4), Y4B)
    K = (J[0] + 96 * ux, J[1] + 96 * uy)
    G = (X4I + 250 * ux, Y4T + 250 * uy)     # đường kéo dài tia tới
    return S, I, J, K, G, (ux, uy)

def d4(kk):
    S, I, J, K, G, (ux, uy) = d4_geom()
    b = f'<rect x="40" y="{Y4T}" width="340" height="{Y4B - Y4T}" fill="{GLASS}" fill-opacity=".14" stroke="currentColor" stroke-width="2"/>'
    b += normal(*I, 0, 1, 56, 96) + normal(*J, 0, 1, 40, 52)
    b += txt(372, Y4T + 26, "n = 1,5", "currentColor", 14, "end", "600")
    b += (seg(30, Y4T, 30, Y4B, "currentColor", 1.4) + chevron(30, Y4T, 0, -1, "currentColor", 1.4, 8)
          + chevron(30, Y4B, 0, 1, "currentColor", 1.4, 8) + txt(34, Y4B + 22, "e = 6 cm", ORG, 14, "start", "700"))
    # góc tới: giữa pháp tuyến hướng lên (90°) và tia tới đảo chiều (150°)
    b += angle_arc(I[0], I[1], 30, 90, 90 + I4) + txt(I[0] - 20, I[1] - 42, "60°", ORG, 14, "middle", "700")
    b += angle_arc(I[0], I[1], 34, 270, 270 + RD4, BLUE) + txt(I[0] + 6, I[1] + 48, "r", BLUE, 14, "start", "700")
    dur = 6.0
    if kk == 0:
        b += txt(16, 22, "Tia sáng qua tấm kính hai mặt song song", "currentColor", 14)
        b += ray(*S, *I) + later(.30, ray(*I, *J), dur) + later(.62, ray(*J, *K), dur)
        b += later(.86, seg(*I, *G, RED, 1.6, "6 5", .8), dur)
        b += path_anim([S, I, J, K], [1, 1 / N4, 1], 0, .86, dur)
        b += timed(.86, "đường kéo dài tia tới (nét đứt)", 16, 238, RED, 14, "start", "600", dur)
        b += timed(.86, "d = ?", 300, 214, RED, 14, "start", "700", dur)
        return fig("c06-4-0", "0 0 420 248", "Tia sáng đi qua tấm kính hai mặt song song: khúc xạ ở mặt trên, khúc xạ lần nữa ở mặt dưới rồi ló ra",
                   b, "Mô phỏng: chấm sáng đi chậm hơn trong kính (tốc độ giảm n lần). " + NOTE)
    b += txt(16, 22, "Dữ kiện và đại lượng cần tìm", "currentColor", 14)
    b += ray(*S, *I) + ray(*I, *J) + ray(*J, *K) + seg(*I, *G, RED, 1.6, "6 5", .8)
    b += dot(*I, 3.5) + txt(I[0] + 6, I[1] - 8, "I", "currentColor", 14) + dot(*J, 3.5) + txt(J[0] - 8, J[1] + 20, "J", "currentColor", 14, "end")
    b += txt(J[0] - 70, (I[1] + J[1]) / 2 + 30, "IJ = ?", RED, 14, "end", "700")
    b += txt(300, 214, "d = ?", RED, 14, "start", "700")
    b += txt(16, 238, "Tia ló có song song tia tới không?", "currentColor", 14, "start", "600")
    return fig("c06-4-2", "0 0 420 248", "Tấm kính dày e, tia tới tại I với góc tới 60 độ, khúc xạ tới J ở mặt dưới rồi ló ra; cần tìm r, IJ và độ dời ngang d",
               b, "Dữ kiện: góc đo so với pháp tuyến (nét đứt). " + NOTE)


# ───────────── Dạng 5 · lăng kính A = 30°, tán sắc ─────────────
PA, PB = (136, 34), (136, 214)
def d5_geom():
    t = (PB[1] - PA[1]) / cosd(A5)
    Cp = (PA[0] + t * sind(A5), PB[1])
    yr = 156
    J = (PA[0] + (yr - PA[1]) * tand(A5), yr)
    return Cp, yr, J

def d5(kk):
    Cp, yr, J = d5_geom()
    XS = 400
    DDR, DTR = 16.0, 27.0                     # góc lệch VẼ (phóng to góc tách màu, không đúng tỉ lệ)
    yd, yt = yr + (XS - J[0]) * tand(DDR), yr + (XS - J[0]) * tand(DTR)
    b = (f'<polygon points="{PA[0]},{PA[1]} {PB[0]},{PB[1]} {Cp[0]:.1f},{Cp[1]}" fill="{GLASS}" fill-opacity=".14" '
         f'stroke="currentColor" stroke-width="2.2"/>')
    b += txt(PA[0] - 8, PA[1] + 4, "A", "currentColor", 14, "end") + txt(PB[0] - 8, PB[1] + 4, "B", "currentColor", 14, "end")
    b += txt(Cp[0] + 6, Cp[1] + 4, "C", "currentColor", 14)
    b += angle_arc(PA[0], PA[1], 40, 270, 270 + A5) + txt(PA[0] + 10, PA[1] + 58, "30°", ORG, 14, "start", "700")
    b += seg(XS, 110, XS, 300, "currentColor", 3) + txt(XS - 4, 104, "màn", "currentColor", 14, "end", "600")
    grad = (f'<defs><linearGradient id="c06g{kk}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{RED}"/>'
            f'<stop offset=".35" stop-color="{YEL}"/><stop offset=".6" stop-color="{GRN}"/><stop offset="1" stop-color="{VIO}"/></linearGradient></defs>')
    fan = (grad + f'<polygon points="{J[0]:.1f},{yr} {XS},{yd:.1f} {XS},{yt:.1f}" fill="url(#c06g{kk})" fill-opacity=".45"/>'
           + ray(*J, XS, yd, RED, 2) + ray(*J, XS, yt, VIO, 2))
    ref = seg(J[0], yr, XS, yr, "currentColor", 1.4, "6 5", .7)
    dur = 6.0
    if kk == 0:
        b += txt(16, 22, "Chùm sáng trắng qua lăng kính", "currentColor", 14)
        b += ray(14, yr, PA[0], yr, "currentColor", 2.6) + later(.30, seg(PA[0], yr, *J, "currentColor", 2.6), dur)
        b += txt(16, yr - 10, "ánh sáng trắng", "currentColor", 14, "start", "600")
        b += path_anim([(14, yr), (PA[0], yr), J], [1, 1 / 1.52], 0, .55, dur, "#f8fafc")
        b += later(.55, fan + ref, dur)
        b += timed(.55, "vệt màu: ? cm", XS - 6, 316, RED, 14, "end", "700", dur)
        return fig("c06-5-0", "0 0 420 326", "Chùm sáng trắng tới vuông góc mặt AB, truyền thẳng tới mặt AC rồi ló ra tách thành dải màu từ đỏ tới tím trên màn",
                   b, "Mô phỏng: góc tách giữa các màu vẽ phóng to nhiều lần. " + NOTE)
    b += txt(16, 22, "Dữ kiện và đại lượng cần tìm", "currentColor", 14)
    b += ray(14, yr, PA[0], yr, "currentColor", 2.6) + seg(PA[0], yr, *J, "currentColor", 2.6) + fan + ref
    b += normal(*J, cosd(A5), -sind(A5), 50, 60)
    b += txt(J[0] + 10, J[1] - 40, "i_{2} = ?", BLUE, 14, "start", "700")
    b += angle_arc(J[0], yr, 78, -DDR, 0, RED) + angle_arc(J[0], yr, 60, -DTR, 0, VIO)
    b += txt(J[0] + 86, yr + 19, "D_{đ} = ?", RED, 14, "start", "700")
    b += txt(280, 244, "D_{t} = ?", VIO, 14, "end", "700")
    b += txt(16, 250, "n_{đ} = 1,50", RED, 14, "start", "700") + txt(16, 272, "n_{t} = 1,54", VIO, 14, "start", "700")
    b += txt(16, 300, "màn cách 1,2 m, vuông góc phương tia tới", "currentColor", 14, "start", "600")
    return fig("c06-5-2", "0 0 420 312", "Lăng kính góc chiết quang 30 độ; tia tới vuông góc AB; ở mặt AC cần tìm góc tới, góc lệch của tia đỏ và tia tím",
               b, "Dữ kiện: góc lệch D đo giữa tia ló và phương tia tới (nét đứt ngang). Góc tách màu vẽ phóng to. " + NOTE)


# ───────────── Dạng 6 · lăng kính phản xạ toàn phần ─────────────
QB, QC, QA = (80, 210), (340, 210), (210, 80)       # vuông tại A (đỉnh trên), mặt huyền BC nằm ngang
XR6 = 128

def d6(kk):
    K = (XR6, QB[1] - (XR6 - QB[0]))                  # điểm gặp mặt AB (y = 210 − (x − 80))
    b = (f'<polygon points="{QB[0]},{QB[1]} {QC[0]},{QC[1]} {QA[0]},{QA[1]}" fill="{GLASS}" fill-opacity=".14" '
         f'stroke="currentColor" stroke-width="2.2"/>')
    b += f'<path d="M{QA[0] - 11},{QA[1] + 11} L{QA[0]},{QA[1] + 22} L{QA[0] + 11},{QA[1] + 11}" fill="none" stroke="currentColor" stroke-width="1.6"/>'
    b += txt(QA[0], QA[1] - 8, "A", "currentColor", 14, "middle") + txt(QB[0] - 8, QB[1] + 6, "B", "currentColor", 14, "end")
    b += txt(QC[0] + 8, QC[1] + 6, "C", "currentColor", 14)
    b += txt(286, 196, "n = 1,5", "currentColor", 14, "middle", "600")
    S = (XR6, 296)
    dur = 5.0
    if kk == 0:
        b += txt(16, 22, "Tia sáng tới vuông góc mặt huyền BC", "currentColor", 14)
        b += ray(*S, XR6, QB[1]) + later(.42, ray(XR6, QB[1], *K), dur)
        b += path_anim([S, (XR6, QB[1]), K], [1, 1 / N6], 0, .8, dur)
        b += later(.8, normal(*K, -1, -1, 40, 40), dur)
        b += timed(.8, "tia đi tiếp thế nào?", 16, 60, RED, 14, "start", "700", dur)
        return fig("c06-6-0", "0 0 420 306", "Tia sáng đi lên, vuông góc mặt huyền BC của lăng kính vuông cân, truyền thẳng tới mặt bên AB",
                   b, "Mô phỏng: chạy tới lúc tia gặp mặt bên thứ nhất; đường đi sau đó là câu hỏi của bài. " + NOTE)
    b += txt(16, 22, "Dữ kiện và đại lượng cần tìm", "currentColor", 14)
    b += ray(*S, XR6, QB[1]) + ray(XR6, QB[1], *K) + normal(*K, -1, -1, 40, 40)
    b += dot(*K, 3.5) + txt(K[0] - 10, K[1] - 4, "K", "currentColor", 14, "end")
    b += txt(K[0] + 14, K[1] + 4, "i = ?", BLUE, 14, "start", "700")
    b += txt(160, 248, "a, b) ngoài là không khí", "currentColor", 14, "start", "600")
    b += txt(160, 270, "c) ngoài là nước, n = 4/3", "currentColor", 14, "start", "600")
    return fig("c06-6-2", "0 0 420 306", "Lăng kính tam giác vuông cân vuông tại A; tia vuông góc BC đi thẳng tới điểm K trên mặt AB; cần tìm góc tới tại K",
               b, "Dữ kiện: tia tới vuông góc mặt huyền nên đi thẳng vào lăng kính. Pháp tuyến tại K nét đứt. " + NOTE)


# ───────────── Dạng 7 · sợi quang ─────────────
Y7T, Y7B, Y7C, X70, X71 = 112, 172, 142, 70, 404
TH7D = 24.0                                    # góc với trục VẼ (không đúng tỉ lệ)

def zigzag(th=TH7D):
    pts, x, y, up = [(X70, Y7C)], X70, Y7C, True
    while True:
        ty = Y7T if up else Y7B
        nx = x + abs(ty - y) / tand(th)
        if nx >= X71:
            pts.append((X71, y + (ty - y) * (X71 - x) / (nx - x)))
            return pts
        pts.append((nx, ty)); x, y, up = nx, ty, not up

def d7(kk):
    b = f'<rect x="{X70}" y="{Y7T - 16}" width="{X71 - X70}" height="{Y7B - Y7T + 32}" fill="{GREY}" fill-opacity=".14" stroke="currentColor" stroke-width="1.6"/>'
    b += f'<rect x="{X70}" y="{Y7T}" width="{X71 - X70}" height="{Y7B - Y7T}" fill="{GLASS}" fill-opacity=".16" stroke="currentColor" stroke-width="1.6"/>'
    b += seg(X70 - 50, Y7C, X71, Y7C, "currentColor", 1.2, "8 5", .6)
    b += txt(X71 - 4, Y7T - 22, "vỏ n_{2} = 1,50", "currentColor", 14, "end", "600")
    b += txt(X71 - 4, Y7B + 36, "lõi n_{1} = 1,60", "currentColor", 14, "end", "600")
    th = TH7D if kk == 0 else 17.0
    zz = zigzag(th)
    ia = asind(N1 * sind(th))
    S = (X70 - 56, Y7C - 56 * tand(ia))
    dur = 7.0
    if kk == 0:
        b += txt(16, 22, "Hai tia cùng vào sợi một lúc: dọc trục và xiên", "currentColor", 14)
        b += ray(*S, X70, Y7C, RED, 2)
        for j in range(len(zz) - 1):
            b += seg(*zz[j], *zz[j + 1], RED, 1.8, "", .55)
        fx = 1 / cosd(TH7D)                     # tia xiên đi đường dài hơn, cùng tốc độ c/n₁
        b += path_anim([(X70, Y7C), (X71, Y7C)], [1], 0, .75 / fx, dur, YEL, 6)
        b += path_anim(zz, [1] * (len(zz) - 1), 0, .75, dur, ORG, 6)
        b += timed(.75 / fx, "tia dọc trục tới trước", 16, 236, YEL, 14, "start", "700", dur)
        b += timed(.75, "tia xiên tới sau: Δt = ?", 16, 258, ORG, 14, "start", "700", dur)
        return fig("c06-7-0", "0 0 420 270", "Trong lõi sợi quang, một chấm sáng đi dọc trục và một chấm sáng đi đường gấp khúc phản xạ ở thành; chấm đi dọc trục tới đầu kia trước",
                   b, "Mô phỏng: hai chấm sáng cùng tốc độ c/n<sub>1</sub> trong lõi; tia xiên phản xạ toàn phần ở thành nên đi đường dài hơn. " + NOTE)
    b += txt(16, 22, "Dữ kiện và đại lượng cần tìm", "currentColor", 14)
    b += ray(*S, X70, Y7C, RED, 2) + ray(X70, Y7C, *zz[1], RED, 2)
    b += seg(X70, Y7C - 64, X70, Y7C + 40, "currentColor", 1.4, "", .9)
    b += txt(S[0] - 2, S[1] - 8, "i_{max} = ?", RED, 14, "start", "700")
    b += angle_arc(X70, Y7C, 46, 0, th, BLUE) + txt(X70 + 50, Y7C + 2, "θ = ?", BLUE, 14, "start", "700")
    P1 = zz[1]
    b += normal(*P1, 0, 1, 34, 44) + txt(P1[0] + 8, P1[1] + 22, "i_{gh} = ?", ORG, 14, "start", "700")
    b += (txt(16, 236, "dài L = 1 km ; c = 3·10", "currentColor", 14, "start", "600")
          .replace("</text>", '<tspan dy="-6" font-size="12">8</tspan><tspan dy="6"> m/s</tspan></text>', 1))
    b += txt(16, 258, "c) đầu sợi đặt trong nước, n = 4/3", "currentColor", 14, "start", "600")
    return fig("c06-7-2", "0 0 420 270", "Đầu sợi quang: tia tới với góc i max, khúc xạ vào lõi hợp với trục góc theta, gặp thành lõi với góc tới giới hạn",
               b, "Dữ kiện: θ đo giữa tia trong lõi và trục sợi ; góc tới ở thành đo so với pháp tuyến của thành. " + NOTE)


BUILD = [d4, d5, d6, d7]


# ═════════════ ĐỀ ═════════════
DANG = [
dict(label="Dạng 4 · Nâng cao · Bản mặt song song: tia ló song song tia tới, độ dời ngang",
     topic=T_KX,
     problem_html=r"""<p>Một tấm kính phẳng có hai mặt song song, dày $e=6\ \text{cm}$, chiết suất $n=1{,}5$, đặt trong không khí. Chiếu một tia sáng hẹp tới mặt trên của tấm kính với góc tới $i=60^\circ$. Dùng máy tính cầm tay để tính sin, cos, tan.</p><ol type="a"><li>Tính góc khúc xạ $r$ trong kính và quãng đường tia sáng đi trong kính. Tia ló ra ở mặt dưới có phương thế nào so với tia tới?</li><li>Tính độ dời ngang $d$ của tia ló, tức là khoảng cách giữa đường kéo dài của tia tới và tia ló.</li><li>Tính $d$ khi góc tới lần lượt là $30^\circ$, $45^\circ$, $75^\circ$. Nhận xét $d$ thay đổi thế nào khi $i$ tăng.</li><li>Đặt tấm kính nằm ngang lên một trang sách rồi nhìn gần vuông góc từ trên xuống. Dòng chữ trông gần mắt hơn bao nhiêu so với khi không có tấm kính?</li></ol>"""),
dict(label="Dạng 5 · Nâng cao · Lăng kính: góc lệch, tán sắc và màu sắc",
     topic=T_TS,
     problem_html=r"""<p>Một lăng kính thuỷ tinh có tiết diện thẳng là tam giác $ABC$, góc chiết quang $A=30^\circ$, đặt trong không khí. Chiếu một chùm sáng trắng hẹp tới mặt bên $AB$ theo phương vuông góc với mặt đó. Chiết suất của thuỷ tinh với ánh sáng đỏ là $n_đ=1{,}50$, với ánh sáng tím là $n_t=1{,}54$. Dùng máy tính cầm tay để tính sin, tan.</p><ol type="a"><li>Tính góc ló và góc lệch $D$ (góc giữa tia ló và phương tia tới) của tia đỏ và của tia tím. Tính góc hợp bởi tia đỏ và tia tím ló ra.</li><li>Đặt một màn ảnh vuông góc với phương tia tới, cách lăng kính $1{,}2\ \text{m}$. Coi các tia ló cùng xuất phát từ một điểm trên mặt $AC$, khoảng cách tới màn tính từ điểm đó theo phương tia tới. Tính bề rộng vệt màu trên màn (theo cm).</li><li>Đặt một tấm lọc màu đỏ trước màn, rồi chồng thêm một tấm lọc màu lục. Mỗi lần trên màn thấy gì? Bỏ hai tấm lọc, thay màn trắng bằng một tờ giấy màu xanh lục: dải màu trông thế nào?</li><li>Thay bằng một lăng kính cùng loại thuỷ tinh nhưng góc chiết quang $A=41^\circ$, chùm sáng vẫn tới vuông góc mặt $AB$. Ánh sáng đỏ và ánh sáng tím có ló ra khỏi mặt $AC$ không?</li></ol>"""),
dict(label="Dạng 6 · Nâng cao · Lăng kính phản xạ toàn phần: đổi môi trường bên ngoài",
     topic=T_PXTP,
     problem_html=r"""<p>Một lăng kính thuỷ tinh có tiết diện thẳng là tam giác $ABC$ vuông cân tại $A$, chiết suất $n=1{,}5$, đặt trong không khí. Chiếu một tia sáng hẹp tới mặt huyền $BC$ theo phương vuông góc với mặt đó, ở gần đầu $B$. Chiết suất của nước là $\dfrac43$. Dùng máy tính cầm tay.</p><ol type="a"><li>Vẽ đường truyền của tia sáng qua lăng kính. Tia ló ra khỏi lăng kính có phương và chiều thế nào so với tia tới?</li><li>Chiết suất của lăng kính phải thoả điều kiện gì để đường truyền ở câu a xảy ra khi lăng kính đặt trong không khí?</li><li>Nhúng cả lăng kính vào nước. Lăng kính phải có chiết suất tối thiểu bằng bao nhiêu để tia sáng vẫn đi như câu a? Với lăng kính thuỷ tinh đã cho (vẫn nhúng trong nước), tia sáng có ló ra ở mặt bên thứ nhất không? Nếu có, tính góc khúc xạ và góc hợp bởi tia ló với phương tia tới.</li></ol>"""),
dict(label="Dạng 7 · Vận dụng cao · Mở rộng HSG: Sợi quang định lượng",
     topic=T_PXTP,
     problem_html=r"""<p>Một sợi quang đặt thẳng, dài $L=1\ \text{km}$, gồm lõi có chiết suất $n_1=1{,}60$ và lớp vỏ có chiết suất $n_2=1{,}50$. Hai đầu sợi được cắt phẳng, vuông góc với trục sợi. Chiếu ánh sáng từ không khí vào tâm một đầu sợi. Lấy $c=3\cdot10^8\ \text{m/s}$; chiết suất của nước là $\dfrac43$. Dùng máy tính cầm tay.</p><ol type="a"><li>Tính góc giới hạn ở mặt phân cách lõi – vỏ. Tia sáng trong lõi phải hợp với trục sợi một góc tối đa bằng bao nhiêu để bị phản xạ toàn phần ở thành lõi? Suy ra góc tới lớn nhất $i_{max}$ ở đầu sợi để ánh sáng được giữ trong lõi.</li><li>Tính thời gian ánh sáng truyền hết sợi theo tia đi dọc trục và theo tia xiên nhất còn được giữ trong lõi. Hai tia chênh nhau bao nhiêu nano giây? Vì sao một xung sáng rất ngắn đi qua sợi thì bị "nhoè" ra?</li><li>Nếu đầu sợi đặt trong nước, góc tới lớn nhất $i_{max}$ bằng bao nhiêu?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (cột 1 nguyên văn đề ; cột 2 chỉ dữ liệu đề cho ; cột 3 kiến thức nền + câu hỏi gợi) ═════════════
ANALYSIS = [
 # Dạng 4
 [(r'"Một tấm kính phẳng có hai mặt song song, dày $e=6\ \text{cm}$, chiết suất $n=1{,}5$, đặt trong không khí"', r"$e=6\ \text{cm}$ ; $n=1{,}5$ ; ngoài là không khí", r"Bản mặt song song : hai mặt phân cách song song, cùng pháp tuyến"),
  (r'"Chiếu một tia sáng hẹp tới mặt trên của tấm kính với góc tới $i=60^\circ$"', r"$i=60^\circ$", r"⚠ góc đo so với pháp tuyến. Định luật khúc xạ : $n_1\sin i=n_2\sin r$"),
  (r'"quãng đường tia sáng đi trong kính"', r"$IJ=?$", r"Tam giác vuông nào có cạnh huyền $IJ$ và cạnh góc vuông $e$ ?"),
  (r'"Tia ló ra ở mặt dưới có phương thế nào so với tia tới?"', r"phương tia ló", r"Ở mặt dưới, góc tới trong kính bằng góc nào ở mặt trên ? Áp dụng định luật khúc xạ lần hai"),
  (r'"khoảng cách giữa đường kéo dài của tia tới và tia ló"', r"$d=?$", r"⚠ khoảng cách giữa hai đường song song đo theo phương vuông góc với chúng. Góc giữa $IJ$ và đường kéo dài tia tới là bao nhiêu ?"),
  (r'"Tính $d$ khi góc tới lần lượt là $30^\circ$, $45^\circ$, $75^\circ$"', r"ba góc tới", r"Góc tới đổi thì đại lượng nào đổi theo ?"),
  (r'"nhìn gần vuông góc từ trên xuống"', r"nhìn gần vuông góc", r"⚠ chỉ khi nhìn gần vuông góc mới dùng độ sâu biểu kiến $h'=\dfrac hn$. Ảnh của dòng chữ qua lớp kính nằm ở đâu ?")],
 # Dạng 5
 [(r'"tam giác $ABC$, góc chiết quang $A=30^\circ$, đặt trong không khí"', r"$A=30^\circ$ ; ngoài là không khí", r"Góc chiết quang : góc giữa hai mặt bên $AB$, $AC$"),
  (r'"theo phương vuông góc với mặt đó"', r"tia tới ⊥ $AB$", r"⚠ góc tới bằng $0$ ⇒ tia truyền thẳng vào lăng kính. Góc tới ở $AC$ bằng góc nào của lăng kính ?"),
  (r'"Chiết suất của thuỷ tinh với ánh sáng đỏ là $n_đ=1{,}50$, với ánh sáng tím là $n_t=1{,}54$"', r"$n_đ=1{,}50$ ; $n_t=1{,}54$", r"Tán sắc : chiết suất phụ thuộc màu. Ra không khí ở $AC$ : $n\sin i_2=\sin r_2$"),
  (r'"góc lệch $D$ (góc giữa tia ló và phương tia tới)"', r"$D_đ=?$ ; $D_t=?$", r"Pháp tuyến của $AC$ nghiêng bao nhiêu so với phương tia tới ? Tia ló lệch về phía nào của pháp tuyến ?"),
  (r'"Đặt một màn ảnh vuông góc với phương tia tới, cách lăng kính $1{,}2\ \text{m}$"', r"$L=1{,}2\ \text{m}$", r"Một tia lệch góc $D$ thì cắt màn cách phương tia tới bao xa ?"),
  (r'"Đặt một tấm lọc màu đỏ trước màn, rồi chồng thêm một tấm lọc màu lục"', r"lọc đỏ ; lọc đỏ + lọc lục", r"Tấm lọc màu cho qua màu của nó, hấp thụ các màu khác"),
  (r'"thay màn trắng bằng một tờ giấy màu xanh lục"', r"giấy lục", r"Màu của vật : màu ánh sáng chiếu tới mà vật hắt lại"),
  (r'"góc chiết quang $A=41^\circ$"', r"$A=41^\circ$", r"⚠ muốn ló ra ở $AC$ : góc tới ở $AC$ phải nhỏ hơn góc giới hạn. Mỗi màu có góc giới hạn riêng không ?")],
 # Dạng 6
 [(r'"tam giác $ABC$ vuông cân tại $A$, chiết suất $n=1{,}5$, đặt trong không khí"', r"vuông cân tại $A$ ; $n=1{,}5$", r"Hai góc ở $B$, $C$ bằng bao nhiêu ?"),
  (r'"Chiếu một tia sáng hẹp tới mặt huyền $BC$ theo phương vuông góc với mặt đó"', r"tia tới ⊥ $BC$", r"Góc tới bằng $0$ ⇒ truyền thẳng. Góc tới ở mặt bên bằng góc giữa mặt tia đi vào và mặt tia gặp tiếp theo"),
  (r'"Tia ló ra khỏi lăng kính có phương và chiều thế nào so với tia tới?"', r"đường truyền", r"⚠ phản xạ toàn phần khi : đi từ môi trường chiết quang hơn sang kém hơn VÀ góc tới $\ge i_{gh}$, $\sin i_{gh}=\dfrac{n_2}{n_1}$"),
  (r'"Chiết suất của lăng kính phải thoả điều kiện gì"', r"$n_{min}=?$", r"Viết điều kiện góc tới $\ge i_{gh}$ thành bất đẳng thức của $n$"),
  (r'"Nhúng cả lăng kính vào nước"', r"$n_{\text{nước}}=\dfrac43$", r"⚠ môi trường ngoài đổi ⇒ $i_{gh}$ đổi : $\sin i_{gh}=\dfrac{n_{\text{nước}}}{n}$"),
  (r'"tính góc khúc xạ và góc hợp bởi tia ló với phương tia tới"', r"$r=?$ ; góc lệch $=?$", r"Định luật khúc xạ, môi trường 1 chứa tia tới : $n_1\sin i=n_2\sin r$")],
 # Dạng 7
 [(r'"gồm lõi có chiết suất $n_1=1{,}60$ và lớp vỏ có chiết suất $n_2=1{,}50$"', r"$n_1=1{,}60$ ; $n_2=1{,}50$", r"⚠ $n_1\gt n_2$ nên ở thành lõi có thể phản xạ toàn phần : $\sin i_{gh}=\dfrac{n_2}{n_1}$"),
  (r'"Hai đầu sợi được cắt phẳng, vuông góc với trục sợi"', r"đầu sợi ⊥ trục", r"Pháp tuyến của đầu sợi trùng phương nào ? Pháp tuyến của thành lõi vuông góc với phương nào ?"),
  (r'"Tia sáng trong lõi phải hợp với trục sợi một góc tối đa bằng bao nhiêu"', r"$\theta_{max}=?$", r"Góc với trục và góc tới ở thành liên hệ thế nào ? Tia càng nghiêng thì góc tới ở thành lớn hay nhỏ ?"),
  (r'"Suy ra góc tới lớn nhất $i_{max}$ ở đầu sợi"', r"$i_{max}=?$", r"Định luật khúc xạ ở đầu sợi, từ không khí vào lõi"),
  (r'"dài $L=1\ \text{km}$"', r"$L=1000\ \text{m}$ ; $c=3\cdot10^8\ \text{m/s}$", r"Tốc độ trong lõi : $v=\dfrac{c}{n_1}$ ; $t=\dfrac{s}{v}$"),
  (r'"theo tia xiên nhất còn được giữ trong lõi"', r"$\Delta t=?$", r"Tia gấp khúc đi quãng đường dài bao nhiêu so với trục ? Mỗi đoạn là cạnh huyền của tam giác vuông nào ?"),
  (r'"Nếu đầu sợi đặt trong nước"', r"$n_{\text{nước}}=\dfrac43$", r"⚠ điều kiện ở thành lõi không đổi ; chỉ khúc xạ ở đầu sợi đổi")],
]

# ═════════════ LỜI GIẢI ═════════════
RC4 = [r"<strong>Định luật khúc xạ:</strong> $n_1\sin i=n_2\sin r$, góc đo so với pháp tuyến.",
       r"<strong>Bản mặt song song:</strong> hai mặt song song nên góc khúc xạ ở mặt trên bằng góc tới ở mặt dưới.",
       r"<strong>Hình học:</strong> tam giác vuông $\cos r=\dfrac{e}{IJ}$ ; khoảng cách từ $J$ tới một đường $= IJ\cdot\sin(\text{góc giữa chúng})$.",
       r"<strong>Nhìn gần vuông góc:</strong> lớp dày $e$ chiết suất $n$ trông dày $\dfrac en$."]
RC5 = [r"<strong>Góc chiết quang $A$:</strong> góc giữa hai mặt bên ; tia tới vuông góc $AB$ thì góc tới ở $AC$ là $i_2=A$ (hai góc có cạnh tương ứng vuông góc).",
       r"<strong>Ló ra không khí:</strong> $n\sin i_2=\sin r_2$ ; góc lệch $D=r_2-A$, lệch về phía đáy.",
       r"<strong>Tán sắc:</strong> $n_đ\lt n_t$ nên tia tím lệch nhiều nhất.",
       r"<strong>Màu sắc:</strong> tấm lọc cho qua màu của nó ; vật hắt lại màu của nó, hấp thụ màu khác.",
       r"<strong>Điều kiện ló:</strong> $i_2\lt i_{gh}$, $\sin i_{gh}=\dfrac1n$ ; ngược lại phản xạ toàn phần."]
RC6 = [r"<strong>Góc tới ở mặt bên:</strong> bằng góc giữa mặt tia đi vào và mặt tia gặp tiếp theo.",
       r"<strong>Phản xạ toàn phần:</strong> đi từ $n_1$ sang $n_2\lt n_1$ VÀ $i\ge i_{gh}$, $\sin i_{gh}=\dfrac{n_2}{n_1}$.",
       r"<strong>Phản xạ:</strong> góc phản xạ bằng góc tới.",
       r"<strong>Khúc xạ:</strong> $n_1\sin i=n_2\sin r$, môi trường 1 chứa tia tới."]
RC7 = [r"<strong>Phản xạ toàn phần ở thành lõi:</strong> $n_1\gt n_2$ và góc tới $\ge i_{gh}$, $\sin i_{gh}=\dfrac{n_2}{n_1}$.",
       r"<strong>Hình học:</strong> pháp tuyến của thành vuông góc với trục ⇒ góc với trục $\theta=90^\circ-$ góc tới ở thành.",
       r"<strong>Đầu sợi:</strong> $n_{ngoài}\sin i=n_1\sin\theta$.",
       r"<strong>Tốc độ trong lõi:</strong> $v=\dfrac{c}{n_1}$ ; $t=\dfrac sv$."]

SOLS = [
 sol(RC4, [
  ("Góc khúc xạ trong kính", [P(r"Ở mặt trên, ánh sáng từ không khí vào kính :"),
     M(r"\sin i=n\sin r\ \Rightarrow\ \sin r=\dfrac{\sin60^\circ}{1{,}5}\approx0{,}5774"), A(r"r\approx35{,}3^\circ")]),
  ("Quãng đường trong kính", [P(r"Tam giác vuông có cạnh góc vuông $e$ (theo pháp tuyến) và cạnh huyền $IJ$ :"),
     M(r"IJ=\dfrac{e}{\cos r}=\dfrac{6}{\cos35{,}3^\circ}"), A(r"IJ\approx7{,}35\ \text{cm}")]),
  ("Phương của tia ló", [P(r"Hai mặt song song nên góc tới ở mặt dưới bằng $r$. Từ kính ra không khí :"),
     M(r"n\sin r=\sin i'\ \Rightarrow\ \sin i'=\sin i\ \Rightarrow\ i'=i=60^\circ"),
     A(r"T:Tia ló song song với tia tới, chỉ bị dời sang một bên.")]),
  ("Độ dời ngang $d$", [P(r"Tia $IJ$ hợp với đường kéo dài của tia tới góc $i-r$ ; $d$ là khoảng cách từ $J$ tới đường đó :"),
     M(r"d=IJ\sin(i-r)=\dfrac{e\sin(i-r)}{\cos r}"), M(r"d=\dfrac{6\sin24{,}7^\circ}{\cos35{,}3^\circ}"), A(r"d\approx3{,}07\ \text{cm}")]),
  ("Bảng $i$ – $d$", [P(r"Lặp lại hai bước : tìm $r$ từ $\sin r=\dfrac{\sin i}{n}$, rồi $d=\dfrac{e\sin(i-r)}{\cos r}$ :"),
     M(r"i=30^\circ:\ r\approx19{,}5^\circ,\ d\approx1{,}16\ \text{cm}"), M(r"i=45^\circ:\ r\approx28{,}1^\circ,\ d\approx1{,}97\ \text{cm}"),
     M(r"i=75^\circ:\ r\approx40{,}1^\circ,\ d\approx4{,}49\ \text{cm}"),
     A(r"T:$i$ càng lớn thì $d$ càng lớn ; $i=0$ thì tia đi thẳng, không dời.")]),
  ("Nhìn vuông góc xuống trang sách", [P(r"Lớp kính dày $e$ trông chỉ dày $\dfrac en$, nên dòng chữ (ở mặt dưới) trông được nâng lên :"),
     M(r"\Delta=e-\dfrac en=e\left(1-\dfrac1n\right)=6\left(1-\dfrac1{1{,}5}\right)"), A(r"\Delta=2\ \text{cm}")]),
  ("Kiểm tra", [P(r"Vào kính (chiết quang hơn) ra $r\lt i$ ✓ ; $IJ\gt e$ vì là cạnh huyền ✓."),
     P(r"$d\lt IJ$ ✓ ; $d$ tăng theo $i$ đúng như bảng ✓."),
     P(r"Ảnh dịch về phía môi trường chiết quang kém (lên phía mắt) ✓.")])],
  [r"a) $r\approx35{,}3^\circ$ ; $IJ\approx7{,}35\ \text{cm}$ ; tia ló song song tia tới",
   r"b) $d\approx3{,}07\ \text{cm}$",
   r"c) $1{,}16\ \text{cm}$ ; $1{,}97\ \text{cm}$ ; $4{,}49\ \text{cm}$ : $i$ tăng thì $d$ tăng",
   r"d) chữ trông gần hơn $2\ \text{cm}$"],
  r"Nhận dạng: thấy <strong>tấm kính hai mặt song song</strong> → khúc xạ hai lần, tia ló song song tia tới ; độ dời $d=\dfrac{e\sin(i-r)}{\cos r}$."),
 sol(RC5, [
  ("Góc ló của tia đỏ", [P(r"Tia vuông góc $AB$ đi thẳng tới $AC$ với góc tới $i_2=A=30^\circ$. Ra không khí :"),
     M(r"\sin r_{2đ}=n_đ\sin A=1{,}50\cdot0{,}5=0{,}75"), A(r"r_{2đ}\approx48{,}6^\circ")]),
  ("Góc lệch của tia đỏ", [P(r"Pháp tuyến của $AC$ hợp với phương tia tới góc $A$ ; tia ló lệch thêm về phía đáy :"),
     M(r"D_đ=r_{2đ}-A=48{,}6^\circ-30^\circ"), A(r"D_đ\approx18{,}6^\circ")]),
  ("Góc lệch của tia tím", [M(r"\sin r_{2t}=1{,}54\cdot0{,}5=0{,}77\ \Rightarrow\ r_{2t}\approx50{,}4^\circ"),
     M(r"D_t=r_{2t}-A"), A(r"D_t\approx20{,}4^\circ"),
     P(r"Góc giữa tia đỏ và tia tím ló ra : $D_t-D_đ\approx1{,}76^\circ$. Tia tím lệch nhiều hơn, nằm gần đáy hơn.")]),
  ("Bề rộng vệt màu", [P(r"Tia lệch góc $D$ cắt màn cách phương tia tới $L\tan D$ :"),
     M(r"\ell=L(\tan D_t-\tan D_đ)=1{,}2\cdot(0{,}3710-0{,}3364)"), A(r"\ell\approx0{,}042\ \text{m}\approx4{,}2\ \text{cm}")]),
  ("Tấm lọc màu", [P(r"Lọc đỏ chỉ cho ánh sáng đỏ đi qua : trên màn chỉ còn vệt đỏ."),
     P(r"Chồng thêm lọc lục : ánh sáng đỏ qua được lọc đỏ nhưng bị lọc lục hấp thụ."),
     A(r"T:Màn tối, không còn vệt màu nào.")]),
  ("Màn giấy xanh lục", [P(r"Giấy lục hắt lại chủ yếu ánh sáng lục, hấp thụ phần lớn các màu khác."),
     A(r"T:Chỉ vùng lục sáng rõ ; vùng đỏ (và tím) gần như đen.")]),
  ("Lăng kính $A=41^\circ$", [P(r"Góc tới ở $AC$ là $i_2=41^\circ$. So với góc giới hạn của từng màu :"),
     M(r"\sin i_{gh,đ}=\dfrac1{1{,}50}\ \Rightarrow\ i_{gh,đ}\approx41{,}8^\circ\gt41^\circ"),
     M(r"\sin i_{gh,t}=\dfrac1{1{,}54}\ \Rightarrow\ i_{gh,t}\approx40{,}5^\circ\lt41^\circ"),
     P(r"Tia đỏ ló ra với $\sin r_2=1{,}5\sin41^\circ\approx0{,}984$, $r_2\approx79{,}8^\circ$ (gần sát mặt $AC$). Tia tím : $1{,}54\sin41^\circ\approx1{,}010\gt1$, không có góc ló."),
     A(r"T:Đỏ ló ra ; tím phản xạ toàn phần ở $AC$.")]),
  ("Kiểm tra", [P(r"$r_2\gt i_2$ khi ra không khí ✓ ; $D_t\gt D_đ$ vì $n_t\gt n_đ$ ✓."),
     P(r"Vệt màu vài xentimét trên màn cách hơn một mét : hợp lí với góc tách chưa tới $2^\circ$ ✓.")])],
  [r"a) $D_đ\approx18{,}6^\circ$ ($r_2\approx48{,}6^\circ$) ; $D_t\approx20{,}4^\circ$ ($r_2\approx50{,}4^\circ$) ; góc tách $\approx1{,}76^\circ$",
   r"b) vệt màu rộng khoảng $4{,}2\ \text{cm}$, tím ở phía đáy",
   r"c) lọc đỏ : chỉ còn vệt đỏ",
   r"c) chồng lọc lục : màn tối",
   r"c) giấy lục : chỉ vùng lục sáng, vùng đỏ gần như đen",
   r"d) đỏ ló ra, tím phản xạ toàn phần"],
  r"Nhận dạng: thấy <strong>tia tới vuông góc mặt bên</strong> lăng kính → $i_2=A$, $\sin r_2=n\sin A$, $D=r_2-A$ ; mỗi màu một $n$, kiểm $n\sin A\lt1$ trước."),
 sol(RC6, [
  ("Góc tới ở mặt bên thứ nhất", [P(r"Tia vuông góc $BC$ đi thẳng tới mặt $AB$. Góc tới tại $K$ bằng góc giữa mặt $BC$ và mặt $AB$, tức góc $B$ :"),
     A(r"i=\widehat B=45^\circ")]),
  ("Đường đi tiếp của tia sáng", [M(r"\sin i_{gh}=\dfrac1{1{,}5}\ \Rightarrow\ i_{gh}\approx41{,}8^\circ\lt45^\circ"),
     P(r"Tại $K$ phản xạ toàn phần ; tia phản xạ quay $90^\circ$, đi song song $BC$, gặp mặt $AC$ cũng với góc tới $45^\circ$ nên lại phản xạ toàn phần."),
     P(r"Tia đi xuống vuông góc $BC$, ló ra không đổi phương."),
     A(r"T:Tia ló song song, ngược chiều tia tới (quay $180^\circ$), dời sang một bên.")]),
  ("Chiết suất tối thiểu trong không khí", [M(r"i\ge i_{gh}\ \Leftrightarrow\ \sin45^\circ\ge\dfrac1n"), M(r"n\ge\dfrac1{\sin45^\circ}=\sqrt2"), A(r"n_{min}\approx1{,}414")]),
  ("Chiết suất tối thiểu khi nhúng trong nước", [M(r"\sin45^\circ\ge\dfrac{n_{\text{nước}}}{n}\ \Rightarrow\ n\ge\dfrac43\sqrt2"), A(r"n_{min}\approx1{,}886")]),
  ("Góc giới hạn thuỷ tinh – nước", [M(r"\sin i_{gh}=\dfrac{4/3}{1{,}5}\approx0{,}889"), A(r"i_{gh}\approx62{,}7^\circ"),
     P(r"Góc tới $45^\circ\lt62{,}7^\circ$ : không còn phản xạ toàn phần, tia ló vào nước ngay ở mặt bên thứ nhất.")]),
  ("Góc khúc xạ vào nước", [M(r"1{,}5\sin45^\circ=\dfrac43\sin r\ \Rightarrow\ \sin r\approx0{,}796"), A(r"r\approx52{,}7^\circ")]),
  ("Góc giữa tia ló và phương tia tới", [P(r"Tia tới và tia ló nằm cùng phía pháp tuyến tại $K$ (tia ló lệch xa pháp tuyến hơn) :"),
     M(r"\delta=r-i=52{,}7^\circ-45^\circ"), A(r"\delta\approx7{,}7^\circ")]),
  ("Kiểm tra", [P(r"$1{,}414\lt1{,}5\lt1{,}886$ : thuỷ tinh dùng được trong không khí, không dùng được trong nước ✓."),
     P(r"Từ thuỷ tinh ra nước (chiết quang kém hơn) ra $r\gt i$ ✓ ; trong nước góc giới hạn lớn hơn trong không khí ✓.")])],
  [r"a) phản xạ toàn phần hai lần ; tia ló song song, ngược chiều tia tới",
   r"b) $n\ge\sqrt2\approx1{,}414$",
   r"c) cần $n\ge\dfrac43\sqrt2\approx1{,}886$",
   r"c) thuỷ tinh $1{,}5$ : tia ló vào nước ở mặt bên thứ nhất, $r\approx52{,}7^\circ$, lệch $\approx7{,}7^\circ$"],
  r"Nhận dạng: thấy <strong>lăng kính vuông cân</strong>, tia <strong>vuông góc mặt huyền</strong> → góc tới mặt bên bằng góc đáy ; so với $i_{gh}$ của đúng môi trường bên ngoài."),
 sol(RC7, [
  ("Góc giới hạn lõi – vỏ", [M(r"\sin i_{gh}=\dfrac{n_2}{n_1}=\dfrac{1{,}50}{1{,}60}=0{,}9375"), A(r"i_{gh}\approx69{,}6^\circ")]),
  ("Góc lớn nhất giữa tia và trục", [P(r"Pháp tuyến của thành vuông góc với trục nên góc với trục và góc tới ở thành phụ nhau. Cần góc tới $\ge i_{gh}$ :"),
     M(r"\theta\le\theta_{max}=90^\circ-i_{gh}"), A(r"\theta_{max}\approx20{,}4^\circ")]),
  ("Góc tới lớn nhất ở đầu sợi", [P(r"Pháp tuyến của đầu sợi là trục. Từ không khí vào lõi :"),
     M(r"\sin i_{max}=n_1\sin\theta_{max}=n_1\cos i_{gh}=\sqrt{n_1^2-n_2^2}"), M(r"\sin i_{max}=\sqrt{1{,}6^2-1{,}5^2}\approx0{,}557"),
     A(r"i_{max}\approx33{,}8^\circ")]),
  ("Thời gian theo tia dọc trục", [M(r"t_0=\dfrac{L}{v}=\dfrac{n_1L}{c}=\dfrac{1{,}6\cdot1000}{3\cdot10^8}"), A(r"t_0\approx5{,}333\cdot10^{-6}\ \text{s}=5{,}333\ \mu\text{s}")]),
  ("Chênh lệch thời gian", [P(r"Tia xiên nhất hợp với trục $\theta_{max}$ ; mỗi đoạn gấp khúc là cạnh huyền, tổng quãng đường $\dfrac{L}{\cos\theta_{max}}=\dfrac{L}{\sin i_{gh}}$ :"),
     M(r"t_1=\dfrac{t_0}{\sin i_{gh}}=\dfrac{5{,}333}{0{,}9375}\approx5{,}689\ \mu\text{s}"),
     M(r"\Delta t=t_1-t_0"), A(r"\Delta t\approx0{,}356\ \mu\text{s}=356\ \text{ns}"),
     P(r"Xung sáng ngắn gồm nhiều tia đi các đường khác nhau, tới đầu kia lệch nhau tới hàng trăm nano giây nên xung bị kéo dài ra.")]),
  ("Đầu sợi đặt trong nước", [P(r"Điều kiện ở thành lõi không đổi ($\theta_{max}$ như cũ) ; chỉ khúc xạ ở đầu sợi đổi :"),
     M(r"n_{\text{nước}}\sin i_{max}=n_1\sin\theta_{max}\ \Rightarrow\ \sin i_{max}=\dfrac{0{,}557}{4/3}\approx0{,}418"), A(r"i_{max}\approx24{,}7^\circ")]),
  ("Kiểm tra", [P(r"$\sin i_{max}\lt1$ ✓ ; trong nước $i_{max}$ nhỏ hơn trong không khí vì môi trường ngoài chiết quang hơn ✓."),
     P(r"$t_1\gt t_0$ ✓ ; chênh $\dfrac{1}{0{,}9375}-1\approx6{,}7\,\%$ của $t_0$ ✓.")])],
  [r"a) $i_{gh}\approx69{,}6^\circ$ ; $\theta_{max}\approx20{,}4^\circ$ ; $i_{max}\approx33{,}8^\circ$",
   r"b) $t_0\approx5{,}333\ \mu\text{s}$ ; $t_1\approx5{,}689\ \mu\text{s}$ ; chênh $\approx356\ \text{ns}$",
   r"c) $i_{max}\approx24{,}7^\circ$"],
  r"Nhận dạng: thấy <strong>lõi – vỏ, sợi quang</strong> → $\sin i_{gh}=n_2/n_1$ ở thành, $\theta=90^\circ-i_{gh}$ với trục, rồi khúc xạ ở đầu sợi ra $i_{max}$."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>tấm kính hai mặt song song</b> → <b>khúc xạ hai lần</b>, tia ló song song tia tới",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Góc khúc xạ trong kính", "Góc khúc xạ r trong kính bằng bao nhiêu độ?", round(R4, 2), "°", 0.2,
       loi=r"Viết ngược tỉ số $\sin r=n\sin i$ (ra số lớn hơn 1, vô lí), hoặc đo góc tới so với mặt kính thay vì pháp tuyến."),
  buoc("Quãng đường trong kính", "Tia sáng đi trong kính một quãng IJ bằng bao nhiêu cm?", round(IJ4, 2), "cm", 0.05,
       loi=r"Nhân $e$ với $\cos r$ : kết quả ngắn hơn bề dày, vô lí vì $IJ$ là cạnh huyền.",
       ke=[(r"$IJ=\dfrac{e}{\cos r}$", True),
           (r"$IJ=e\cos r$", r"$IJ$ là cạnh huyền nên phải dài hơn $e$ ; $e\cos r$ lại ngắn hơn $e$."),
           (r"$IJ=\dfrac{e}{\cos i}$", r"Trong kính tia đi theo góc $r$, không phải góc tới $i$ ở ngoài không khí.")]),
  buoc("Phương của tia ló", "Tia ló ra ở mặt dưới có phương thế nào so với tia tới?",
       lua_chon=[(r"Song song với tia tới, chỉ dời sang một bên", True),
                 (r"Lệch gần pháp tuyến hơn tia tới", r"Ra không khí, định luật khúc xạ cho lại đúng góc $i$ ; hai mặt song song nên hai lần lệch bù nhau."),
                 (r"Đi tiếp theo phương tia khúc xạ trong kính", r"Ở mặt dưới tia lại khúc xạ lần nữa khi ra không khí, lệch xa pháp tuyến.")],
       loi=r"Quên rằng ở mặt dưới tia khúc xạ lần thứ hai ; hai mặt song song nên góc tới ở mặt dưới bằng $r$.",
       ke=[(r"Viết định luật khúc xạ ở mặt dưới với góc tới bằng $r$", True),
           (r"Coi tia đi thẳng qua mặt dưới", r"Mặt dưới cũng là mặt phân cách kính – không khí ; tia khúc xạ ở đó."),
           (r"Lấy góc tới ở mặt dưới bằng $i$", r"Trong kính tia hợp với pháp tuyến góc $r$ ; hai mặt song song nên góc tới ở mặt dưới là $r$.")]),
  buoc("Độ dời ngang $d$", "Độ dời ngang d bằng bao nhiêu cm?", round(D4, 2), "cm", 0.03,
       loi=r"Lấy khoảng cách giữa hai điểm trên mặt kính thay cho khoảng cách vuông góc giữa hai tia, hoặc dùng góc $r$ thay cho góc $i-r$.",
       ke=[(r"$d=IJ\sin(i-r)$", True),
           (r"$d=e\tan i-e\tan r$", r"Đó là khoảng cách dọc mặt kính giữa hai điểm, không phải khoảng cách vuông góc giữa hai tia song song."),
           (r"$d=IJ\sin r$", r"Góc giữa $IJ$ và đường kéo dài của tia tới là $i-r$, không phải $r$.")]),
  buoc("Bảng $i$ – $d$", "Với góc tới 75°, độ dời ngang d bằng bao nhiêu cm?", round(D4_TAB[75], 2), "cm", 0.03,
       loi=r"Giữ nguyên góc khúc xạ của câu b, hoặc coi $d$ tỉ lệ thuận với $i$.",
       ke=[(r"Tìm lại $r$ từ $\sin r=\dfrac{\sin i}{n}$, rồi $d=\dfrac{e\sin(i-r)}{\cos r}$", True),
           (r"Lấy $d$ của câu b nhân với $\dfrac{75}{60}$", r"$d$ không tỉ lệ thuận với $i$ ; công thức có sin và cos."),
           (r"Giữ $r$ như câu b, chỉ đổi $i$", r"Góc tới đổi thì góc khúc xạ đổi theo định luật khúc xạ.")]),
  buoc("Nhìn vuông góc xuống trang sách", "Dòng chữ trông gần mắt hơn bao nhiêu cm?", round(DEL4, 2), "cm", 0.05,
       loi=r"Trả lời bằng bề dày biểu kiến $\dfrac en$ thay cho độ dịch, hoặc nhân với $n$ thay vì chia.",
       ke=[(r"$\Delta=e-\dfrac en$", True),
           (r"$\Delta=\dfrac en$", r"$\dfrac en$ là bề dày lớp kính trông thấy ; độ dịch là phần chênh với bề dày thật."),
           (r"$\Delta=e(n-1)$", r"Nhân thay vì chia : nhìn qua lớp chiết quang hơn, lớp đó trông mỏng đi $n$ lần.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>tia tới vuông góc mặt bên</b> lăng kính → <b>góc tới mặt kia bằng A</b>, mỗi màu một n",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Góc ló của tia đỏ", "Góc ló r₂ của tia đỏ ở mặt AC bằng bao nhiêu độ?", round(R2D, 2), "°", 0.2,
       loi=r"Lấy góc tới ở $AC$ là góc giữa tia và mặt $AC$ (phần bù), hoặc viết ngược $\sin r_2=\dfrac{\sin i_2}{n}$ trong khi ánh sáng đi từ thuỷ tinh ra không khí."),
  buoc("Góc lệch của tia đỏ", "Góc lệch D của tia đỏ so với phương tia tới bằng bao nhiêu độ?", round(DD5, 2), "°", 0.2,
       loi=r"Trả lời bằng góc ló $r_2$ : góc này đo so với pháp tuyến của $AC$, mà pháp tuyến đó đã nghiêng so với phương tia tới.",
       ke=[(r"$D=r_2-A$", True),
           (r"$D=r_2$", r"$r_2$ đo so với pháp tuyến $AC$ ; pháp tuyến này nghiêng góc $A$ so với phương tia tới."),
           (r"$D=r_2+A$", r"Pháp tuyến $AC$ nghiêng về phía đỉnh, tia ló lệch về phía đáy so với pháp tuyến : hai góc ngược phía nên phải trừ.")]),
  buoc("Góc lệch của tia tím", "Góc lệch D của tia tím bằng bao nhiêu độ?", round(DT5, 2), "°", 0.2,
       loi=r"Lấy góc lệch của tia tím bằng tia đỏ vì cùng góc tới, hoặc nhân góc lệch với tỉ số chiết suất.",
       ke=[(r"Làm lại với $n_t$ : $\sin r_2=n_t\sin A$, rồi $D_t=r_2-A$", True),
           (r"$D_t=D_đ\cdot\dfrac{n_t}{n_đ}$", r"Góc lệch không tỉ lệ với chiết suất ; chỉ $\sin r_2$ tỉ lệ với $n$."),
           (r"$D_t=D_đ$ vì cùng góc tới", r"Cùng góc tới nhưng chiết suất khác nên góc ló khác : đó chính là tán sắc.")]),
  buoc("Bề rộng vệt màu", "Vệt màu trên màn rộng bao nhiêu cm?", round(W5, 2), "cm", 0.15,
       loi=r"Nhân khoảng cách với hiệu hai góc tính bằng độ, hoặc dùng góc ló $r_2$ thay cho góc lệch $D$.",
       ke=[(r"$\ell=L(\tan D_t-\tan D_đ)$", True),
           (r"$\ell=L(D_t-D_đ)$ với góc tính bằng độ", r"Số đo độ không phải độ dài ; vị trí trên màn là $L\tan D$."),
           (r"$\ell=L(\sin r_{2t}-\sin r_{2đ})$", r"Màn vuông góc với phương tia tới nên phải dùng góc lệch $D$ (so với phương tia tới) và tan.")]),
  buoc("Tấm lọc màu", "Chồng tấm lọc đỏ và tấm lọc lục trước màn thì màn thế nào?",
       lua_chon=[(r"Màn tối, không còn vệt màu", True),
                 (r"Thấy vệt vàng vì đỏ cộng lục ra vàng", r"Đỏ + lục ra vàng khi hai chùm sáng cùng chiếu lên màn ; ở đây ánh sáng đi lần lượt qua hai tấm lọc."),
                 (r"Vẫn còn vệt đỏ", r"Ánh sáng đỏ qua được lọc đỏ nhưng bị lọc lục hấp thụ.")],
       loi=r"Nhầm lọc màu với trộn ánh sáng màu : mỗi tấm lọc chỉ bớt đi các màu khác màu của nó.",
       ke=[(r"Theo dõi ánh sáng qua lần lượt từng tấm lọc", True),
           (r"Cộng màu hai tấm lọc như trộn hai chùm sáng", r"Hai tấm lọc chồng nhau : ánh sáng phải qua cả hai, không phải hai chùm cùng chiếu."),
           (r"Coi tấm lọc nhuộm màu cho ánh sáng", r"Tấm lọc không biến màu này thành màu khác, chỉ hấp thụ bớt.")]),
  buoc("Màn giấy xanh lục", "Trên tờ giấy xanh lục, dải màu trông thế nào?",
       lua_chon=[(r"Chỉ vùng lục sáng rõ, vùng đỏ gần như đen", True),
                 (r"Dải màu vẫn đủ như trên màn trắng", r"Giấy lục hắt lại chủ yếu ánh sáng lục, hấp thụ phần lớn các màu khác."),
                 (r"Cả dải đều thành màu lục", r"Chỗ chỉ có ánh sáng đỏ chiếu tới, giấy không có ánh sáng lục để hắt lại nên chỗ đó tối.")],
       loi=r"Nghĩ vật màu lục luôn trông lục : vật chỉ hắt lại được màu có trong ánh sáng chiếu tới nó.",
       ke=[(r"Màu của vật là màu ánh sáng chiếu tới mà vật hắt lại", True),
           (r"Vật màu lục luôn trông lục dưới mọi ánh sáng", r"Dưới ánh sáng không có màu lục, vật lục không hắt lại gì nên trông tối."),
           (r"Giấy màu hắt lại mọi màu như giấy trắng, chỉ nhạt hơn", r"Giấy màu hấp thụ phần lớn các màu khác màu của nó.")]),
  buoc("Lăng kính $A=41^\circ$", "Với góc chiết quang 41°, ánh sáng nào ló ra khỏi mặt AC?",
       lua_chon=[(r"Chỉ ánh sáng đỏ ló ra, ánh sáng tím phản xạ toàn phần", True),
                 (r"Cả hai đều ló ra, tím lệch nhiều hơn", r"Tính $n_t\sin A$ : lớn hơn 1 nên tia tím không có góc ló."),
                 (r"Cả hai đều phản xạ toàn phần", r"Góc giới hạn của ánh sáng đỏ còn lớn hơn góc tới ở $AC$.")],
       loi=r"Dùng một góc giới hạn chung cho mọi màu, hoặc tính ngay góc lệch mà không kiểm tra điều kiện ló.",
       ke=[(r"So góc tới ở $AC$ với góc giới hạn của từng màu, $\sin i_{gh}=\dfrac1n$", True),
           (r"So với góc giới hạn tính theo chiết suất trung bình", r"Hai màu có chiết suất khác nhau nên góc giới hạn khác nhau ; phải xét riêng."),
           (r"Tính ngay $D=r_2-A$ cho cả hai màu", r"Phải kiểm điều kiện ló trước ; nếu $n\sin A\gt1$ thì không có $r_2$.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 6 ──
 dict(nhan_dang=r"Thấy <b>lăng kính vuông cân</b>, tia <b>vuông góc mặt huyền</b> → so góc tới mặt bên với <b>i_gh của môi trường ngoài</b>",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Góc tới ở mặt bên thứ nhất", "Góc tới của tia sáng ở mặt bên AB bằng bao nhiêu độ?", I6, "°", 0.5,
       loi=r"Lấy góc vuông của lăng kính làm góc tới. Góc tới ở mặt bên bằng góc giữa mặt tia đi vào và mặt tia gặp tiếp theo, không phải góc ở đỉnh vuông."),
  buoc("Đường đi tiếp của tia sáng", "Sau khi gặp mặt bên thứ nhất, tia sáng đi thế nào?",
       lua_chon=[(r"Phản xạ toàn phần ở cả hai mặt bên, ló ra qua mặt huyền, ngược chiều tia tới", True),
                 (r"Khúc xạ ló ra ngoài ngay ở mặt bên thứ nhất", r"Góc tới lớn hơn góc giới hạn thuỷ tinh – không khí nên không có tia khúc xạ."),
                 (r"Phản xạ toàn phần một lần rồi ló ra ở mặt bên thứ hai", r"Sau lần phản xạ thứ nhất, tia gặp mặt bên thứ hai với góc tới bằng lần đầu nên lại phản xạ toàn phần.")],
       loi=r"Không so góc tới với góc giới hạn mà cho tia khúc xạ ra ngoài như bình thường.",
       ke=[(r"So góc tới với $i_{gh}$ của thuỷ tinh – không khí", True),
           (r"So góc tới với $90^\circ$", r"Mọi góc tới đều nhỏ hơn $90^\circ$ ; điều kiện là góc tới $\ge i_{gh}$."),
           (r"Áp dụng ngay $n\sin i=\sin r$ để tìm góc ló", r"Phải kiểm điều kiện phản xạ toàn phần trước ; nếu $n\sin i\gt1$ thì không có góc ló.")]),
  buoc("Chiết suất tối thiểu trong không khí", "Chiết suất của lăng kính tối thiểu bằng bao nhiêu?", round(NMIN6, 3), "", 0.015,
       loi=r"Viết ngược $\sin i_{gh}=n$, hoặc lấy góc tới là $90^\circ$ thay cho góc tìm ở bước 1.",
       ke=[(r"$\sin i\ge\sin i_{gh}=\dfrac1n$, với $i$ là góc tìm ở bước 1", True),
           (r"$\sin i_{gh}=n$ rồi cho $i_{gh}\le i$", r"Viết ngược : $\sin i_{gh}=\dfrac{n_2}{n_1}=\dfrac1n$, luôn nhỏ hơn 1."),
           (r"$n\ge\dfrac1{\sin90^\circ}$", r"Góc tới là góc ở bước 1, không phải góc vuông của lăng kính.")]),
  buoc("Chiết suất tối thiểu khi nhúng trong nước", "Nhúng trong nước, chiết suất tối thiểu của lăng kính bằng bao nhiêu?", round(NMIN6W, 3), "", 0.015,
       loi=r"Giữ điều kiện như trong không khí, hoặc viết ngược tỉ số chiết suất thuỷ tinh – nước.",
       ke=[(r"$\sin i\ge\dfrac{n_{\text{nước}}}{n}$", True),
           (r"$\sin i\ge\dfrac{n}{n_{\text{nước}}}$", r"Ngược tỉ số : $\sin i_{gh}=\dfrac{n_2}{n_1}$, $n_1$ là môi trường chứa tia tới (lăng kính)."),
           (r"Giữ kết quả bước 3 vì nước không ảnh hưởng", r"Góc giới hạn phụ thuộc cả môi trường bên ngoài ; ra nước thì góc giới hạn lớn hơn.")]),
  buoc("Góc giới hạn thuỷ tinh – nước", "Góc giới hạn của thuỷ tinh 1,5 với nước bằng bao nhiêu độ?", round(IGH6W, 2), "°", 0.2,
       loi=r"Dùng $\sin i_{gh}=\dfrac1n$ như khi ra không khí, quên môi trường ngoài đã là nước.",
       ke=[(r"$\sin i_{gh}=\dfrac{4/3}{1{,}5}$", True),
           (r"$\sin i_{gh}=\dfrac1{1{,}5}$", r"Đó là góc giới hạn với không khí ; bên ngoài bây giờ là nước."),
           (r"$\sin i_{gh}=\dfrac{1{,}5}{4/3}$", r"Ra số lớn hơn 1 : viết ngược tỉ số.")]),
  buoc("Góc khúc xạ vào nước", "Tia ló vào nước với góc khúc xạ bằng bao nhiêu độ?", round(R6W, 2), "°", 0.2,
       loi=r"Đổi chỗ hai chiết suất (vế chứa tia tới phải là thuỷ tinh), hoặc coi bên ngoài vẫn là không khí.",
       ke=[(r"$1{,}5\sin i=\dfrac43\sin r$", True),
           (r"$\dfrac43\sin i=1{,}5\sin r$", r"Tia tới nằm trong thuỷ tinh nên vế có góc tới phải là chiết suất thuỷ tinh."),
           (r"$1{,}5\sin i=\sin r$", r"Bên ngoài là nước, không phải không khí ; viết vậy còn ra $\sin r\gt1$.")]),
  buoc("Góc giữa tia ló và phương tia tới", "Tia ló vào nước hợp với phương tia tới một góc bao nhiêu độ?", round(LECH6, 2), "°", 0.2,
       loi=r"Cộng góc tới với góc khúc xạ, hoặc lấy phần bù của góc khúc xạ : cả hai góc đều đo từ cùng một pháp tuyến, cùng một phía.",
       ke=[(r"Lấy hiệu góc khúc xạ và góc tới, $\delta=r-i$", True),
           (r"$\delta=r+i$", r"Tia tới và tia ló ở cùng phía pháp tuyến nên góc giữa chúng là hiệu, không phải tổng."),
           (r"$\delta=90^\circ-r$", r"Đó là góc giữa tia ló và mặt bên, không phải góc giữa tia ló và phương tia tới.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 7 ──
 dict(nhan_dang=r"Thấy <b>lõi – vỏ</b>, <b>sợi quang</b> → <b>i_gh ở thành</b>, góc với trục phụ với nó, rồi khúc xạ ở đầu sợi",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Góc giới hạn lõi – vỏ", "Góc giới hạn ở mặt phân cách lõi – vỏ bằng bao nhiêu độ?", round(IGH7, 2), "°", 0.2,
       loi=r"Viết ngược $\sin i_{gh}=\dfrac{n_1}{n_2}$ (ra số lớn hơn 1), hoặc dùng $\dfrac1{n_1}$ như khi lõi tiếp xúc không khí."),
  buoc("Góc lớn nhất giữa tia và trục", "Tia trong lõi hợp với trục góc tối đa bao nhiêu độ?", round(TH7, 2), "°", 0.2,
       loi=r"Lấy luôn góc giới hạn làm góc với trục : góc giới hạn đo so với pháp tuyến của thành, mà pháp tuyến này vuông góc với trục.",
       ke=[(r"$\theta_{max}=90^\circ-i_{gh}$, tia càng gần trục thì góc tới ở thành càng lớn", True),
           (r"$\theta_{max}=i_{gh}$", r"$i_{gh}$ đo so với pháp tuyến của thành ; pháp tuyến vuông góc với trục nên hai góc phụ nhau."),
           (r"$90^\circ-i_{gh}$ là góc tối thiểu với trục", r"Tia càng nghiêng so với trục thì góc tới ở thành càng nhỏ ; điều kiện góc tới $\ge i_{gh}$ cho giới hạn trên của góc với trục.")]),
  buoc("Góc tới lớn nhất ở đầu sợi", "Góc tới lớn nhất ở đầu sợi (trong không khí) bằng bao nhiêu độ?", round(IMAX7, 2), "°", 0.2,
       loi=r"Viết ngược định luật khúc xạ ở đầu sợi (chia cho $n_1$), hoặc quên ánh sáng bị khúc xạ khi vào lõi.",
       ke=[(r"$\sin i_{max}=n_1\sin\theta_{max}$", True),
           (r"$\sin i_{max}=\dfrac{\sin\theta_{max}}{n_1}$", r"Ánh sáng đi từ không khí vào lõi : $1\cdot\sin i=n_1\sin\theta$ ; chia cho $n_1$ là viết ngược."),
           (r"$i_{max}=\theta_{max}$", r"Ánh sáng khúc xạ ở đầu sợi ; góc trong không khí lớn hơn góc trong lõi.")]),
  buoc("Thời gian theo tia dọc trục", "Ánh sáng đi dọc trục hết sợi mất bao nhiêu micrô giây?", round(T0_7, 3), "µs", 0.01,
       loi=r"Dùng tốc độ $c$ của chân không, hoặc nhân $c$ với $n_1$.",
       ke=[(r"$t_0=\dfrac{L}{v}=\dfrac{n_1L}{c}$", True),
           (r"$t_0=\dfrac{L}{c}$", r"Trong lõi ánh sáng đi chậm hơn : $v=\dfrac{c}{n_1}$."),
           (r"$t_0=\dfrac{L}{n_1c}$", r"Nhân thay vì chia : tốc độ trong lõi là $\dfrac{c}{n_1}$, nhỏ hơn $c$.")]),
  buoc("Chênh lệch thời gian", "Tia xiên nhất tới chậm hơn tia dọc trục bao nhiêu nano giây?", round(DT7, 1), "ns", 5,
       loi=r"Lấy quãng đường tia xiên là $L\cos\theta$ (ngắn hơn trục), hoặc cho tia xiên đi trong vỏ với tốc độ $\dfrac{c}{n_2}$.",
       ke=[(r"Tia xiên đi quãng $\dfrac{L}{\cos\theta_{max}}$, cùng tốc độ $\dfrac{c}{n_1}$", True),
           (r"Tia xiên đi trong vỏ với tốc độ $\dfrac{c}{n_2}$", r"Tia vẫn ở trong lõi, chỉ chạm thành rồi phản xạ toàn phần."),
           (r"Quãng đường tia xiên là $L\cos\theta_{max}$", r"Đường gấp khúc dài hơn trục ; mỗi đoạn là cạnh huyền.")]),
  buoc("Đầu sợi đặt trong nước", "Đầu sợi đặt trong nước thì góc tới lớn nhất bằng bao nhiêu độ?", round(IMAX7W, 2), "°", 0.2,
       loi=r"Giữ nguyên $i_{max}$ như trong không khí, hoặc ghép chiết suất nước với góc trong lõi.",
       ke=[(r"$n_{\text{nước}}\sin i_{max}=n_1\sin\theta_{max}$", True),
           (r"Giữ $i_{max}$ như trong không khí", r"$\theta_{max}$ không đổi nhưng khúc xạ ở đầu sợi đổi vì môi trường ngoài đổi."),
           (r"$\sin i_{max}=n_{\text{nước}}\sin\theta_{max}$", r"Đặt nhầm chỗ : $\theta_{max}$ là góc trong lõi nên đi với $n_1$ ; nước ở phía ngoài, đi với $i_{max}$.")]),
  buoc("Kiểm tra")]),
]


# KaTeX: chỉ số dưới có dấu tiếng Việt → \text{…} (n_đ → n_{\text{đ}}, r_{2đ} → r_{\text{2đ}})
_SUBVN = re.compile(r"_\{([^{}\\]*[^\x00-\x7f][^{}\\]*)\}")
_SUBVN1 = re.compile(r"_([^\x00-\x7f])")
def _tx(x):
    if isinstance(x, str):
        if x.lstrip().startswith("<figure"):
            return x
        x = _SUBVN.sub(lambda m: "_{\\text{" + m.group(1) + "}}", x)
        return _SUBVN1.sub(lambda m: "_{\\text{" + m.group(1) + "}}", x)
    if isinstance(x, list):
        return [_tx(v) for v in x]
    if isinstance(x, tuple):
        return tuple(_tx(v) for v in x)
    if isinstance(x, dict):
        return {k: _tx(v) for k, v in x.items()}
    return x
_RAW_DANG, _RAW_ANALYSIS = DANG, ANALYSIS
DANG, ANALYSIS, SOLS, STEPS = _tx(DANG), _tx(ANALYSIS), _tx(SOLS), _tx(STEPS)


def kiem_so():
    # số liệu khớp nguon.md / tinh.py
    assert round(R4, 1) == 35.3 and round(IJ4, 2) == 7.35 and round(D4, 2) == 3.07 and abs(DEL4 - 2) < 1e-9
    assert [round(D4_TAB[k], 2) for k in (30, 45, 75)] == [1.16, 1.97, 4.49]
    assert all(D4_TAB[a] < D4_TAB[b] for a, b in ((30, 45), (45, 60), (60, 75)))
    assert round(R2D, 1) == 48.6 and round(DD5, 1) == 18.6 and round(R2T, 1) == 50.4 and round(DT5, 1) == 20.4
    assert round(MO5, 2) == 1.76 and round(W5, 1) == 4.2 and round(tand(DD5), 4) == 0.3364 and round(tand(DT5), 4) == 0.3710
    assert IGH_D > A5B > IGH_T and round(IGH_D, 1) == 41.8 and round(IGH_T, 1) == 40.5 and round(R2D_B, 1) == 79.8 and NT_SIN_B > 1
    assert IGH6 < I6 and round(NMIN6, 3) == 1.414 and round(NMIN6W, 3) == 1.886 and NMIN6 < N6 < NMIN6W
    assert round(IGH6W, 1) == 62.7 and I6 < IGH6W and round(R6W, 1) == 52.7 and round(LECH6, 1) == 7.7
    assert round(IGH7, 1) == 69.6 and round(TH7, 1) == 20.4 and abs(SIN_IMAX - math.sqrt(N1**2 - N2**2)) < 1e-12
    assert round(IMAX7, 1) == 33.8 and round(T0_7, 3) == 5.333 and round(T1_7, 3) == 5.689 and round(DT7) == 356 and round(IMAX7W, 1) == 24.7
    # mỗi cách sai cho số khác đáp án đúng (ngoài sai số của bước)
    assert abs(E4 * cosd(R4) - IJ4) > .05 and abs(E4 / cosd(I4) - IJ4) > .05                                       # D4 b2
    assert abs(E4 * (tand(I4) - tand(R4)) - D4) > .03 and abs(IJ4 * sind(R4) - D4) > .03                             # D4 b4
    assert abs(D4 * 75 / 60 - D4_TAB[75]) > .03 and abs(E4 * sind(75 - R4) / cosd(R4) - D4_TAB[75]) > .03             # D4 b5
    assert abs(E4 / N4 - DEL4) > .05 and abs(E4 * (N4 - 1) - DEL4) > .05                                            # D4 b6
    assert abs(R2D - DD5) > .2 and abs(R2D + A5 - DD5) > .2                                                            # D5 b2
    assert abs(DD5 * NT / ND - DT5) > .2 and abs(DD5 - DT5) > .2                                                       # D5 b3
    assert abs(L5 * MO5 * 100 - W5) > .15 and abs(L5 * (NT - ND) * sind(A5) * 100 - W5) > .15                           # D5 b4
    assert abs(1 / sind(90) - NMIN6) > .015 and abs(NMIN6 - NMIN6W) > .015 and N6 * sind(I6) / NW < 1             # D6 b3, b4
    assert abs(asind(1 / N6) - IGH6W) > .2 and NW / N6 < 1 < N6 / NW                                                   # D6 b5
    assert abs(asind(NW * sind(I6) / N6) - R6W) > .2 and N6 * sind(I6) > 1 and abs(R6W + I6 - LECH6) > .2 and abs(90 - R6W - LECH6) > .2                                             # D6 b6
    assert abs(IGH7 - TH7) > .2 and N1 / N2 > 1                                                                        # D7 b1, b2
    assert abs(asind(sind(TH7) / N1) - IMAX7) > .2 and abs(TH7 - IMAX7) > .2                                          # D7 b3
    assert abs(L7 / C0 * 1e6 - T0_7) > .01 and abs(L7 / (N1 * C0) * 1e6 - T0_7) > .01                                # D7 b4
    assert abs((L7 / cosd(TH7) * N2 / C0 * 1e6 - T0_7) * 1000 - DT7) > 5 and abs((L7 * cosd(TH7) * N1 / C0 * 1e6 - T0_7) * 1000 - DT7) > 5 and abs(360 - DT7) <= 5
    assert abs(IMAX7 - IMAX7W) > .2 and abs(asind(NW * sind(TH7)) - IMAX7W) > .2                                                            # D7 b6
    # bảng phân tích: cột 1 trích nguyên văn đề
    for n, rows in enumerate(_RAW_ANALYSIS):
        for r in rows:
            assert r[0].strip('"') in _RAW_DANG[n]["problem_html"], (n, r[0])
    # không lộ đáp số trong đề, hình, bảng phân tích, nhãn, câu hỏi, lựa chọn, lỗi hay gặp
    lo = {0: ["35,3", "35,2", "7,35", "3,07", "1,16", "1,97", "4,49", "19,5", "28,1", "40,1", "24,7", "2 cm"],
          1: ["48,6", "18,6", "50,4", "20,4", "1,76", "4,2", "79,8", "0,75", "0,77", "0,33", "0,37"],
          2: ["45", "1,414", "1,886", "62,7", "52,7", "7,7", "√2", "sqrt", "180", "0,889", "0,796"],
          3: ["69,6", "20,4", "33,8", "5,333", "5,689", "356", "24,7", "0,9375", "0,557", "0,418"]}
    for n in range(4):
        figs = re.sub(r"<[^>]+>", " ", BUILD[n](0) + BUILD[n](2))       # chỉ chữ hiện trên hình, bỏ toạ độ
        blob = DANG[n]["problem_html"] + figs + str(ANALYSIS[n]) + STEPS[n]["nhan_dang"]
        for s in STEPS[n]["buoc"]:
            blob += s.get("tieu_de", "") + s.get("hoi", "") + s.get("loi_hay_gap", "")
            for c in s.get("chon_buoc_ke", []) + s.get("lua_chon", []):
                blob += c["text"] + c.get("vi_sao", "")
        for x in lo[n]:
            assert x not in blob, (n, x)
    for n, s in enumerate(STEPS):
        assert s["cap_do"] in (3, 4) and len(s["buoc"]) == SOLS[n].count('class="bt-step"'), n
        for k, b_ in enumerate(s["buoc"][:-1]):
            assert "hoi" in b_ and "loi_hay_gap" in b_, (n, k)
            assert ("dap_so" in b_) != ("lua_chon" in b_), (n, k)
            if k:
                assert len(b_["chon_buoc_ke"]) == 3 and sum(c["dung"] for c in b_["chon_buoc_ke"]) == 1, (n, k)
        assert "hoi" not in s["buoc"][-1]
    # chuỗi không có ký tự điều khiển (\t lọt vào do quên r"")
    for x in (DANG, ANALYSIS, SOLS, STEPS):
        assert not re.search(r"[\x00-\x08\x0b-\x1f]", str(x).replace("\\n", "")), "ký tự điều khiển"
    print("btm151_d456: kiểm số liệu đạt")


if __name__ == "__main__":
    kiem_so()
