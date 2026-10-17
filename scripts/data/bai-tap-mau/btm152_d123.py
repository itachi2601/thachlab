"""Bài tập mẫu CĐ08 "Cảm ứng điện từ và dòng điện xoay chiều" (lesson 152) — Dạng 1–3. Module được build-hinh-152.py import.
Dàn ý + số liệu đã tính: content/hsg9/cd08-cam-ung-dien-tu/nguon.md (mục "Bài tập mẫu", D1–D3 dùng nguyên số; tinh.py cùng thư mục).
Quy ước: máy biến áp cuộn sơ cấp chỉ số 1, thứ cấp chỉ số 2; máy phát f = n·p (n vòng/s, p số CẶP cực); H_BA = P2/P1.
Đường sức từ nét đứt + đầu chevron 30° (field_line / field_path / chev_on của svg_lib).
Mọi đáp số tính lại bằng Python trong kiem_so(); mọi lựa chọn sai của chon_buoc_ke được assert cho số khác đáp án đúng."""
import math
from fractions import Fraction as Fr
from dung import *   # sol, buoc, M/P/A, fig, seg, lbl, poly, arrow, chevron, field_line, field_path, cubic, chev_on, RED/BLUE/ORG/GRN

GREY = "#94a3b8"
YEL = "#facc15"
FL = GRN                      # màu đường sức
TOPIC_D1 = "Điều kiện xuất hiện dòng điện cảm ứng"
TOPIC_D2 = "Nguyên tắc tạo ra dòng điện xoay chiều"
TOPIC_D3 = "Máy biến áp"

# số liệu D2
P_TD, F_LUOI = 6, 50
N_TD = Fr(F_LUOI, P_TD)                  # vòng/s
N_TD_PH = N_TD * 60                      # 500 vòng/phút
N_CHAM = 480
F_CHAM = Fr(N_CHAM, 60) * P_TD           # 48 Hz
V_XE = Fr(18 * 1000, 3600)               # 5 m/s
D_NUM = 0.02
N_NUM = float(V_XE) / (math.pi * D_NUM)  # ≈ 79,58 vòng/s
P_DYN = 2                                # 4 cực = 2 cặp
F_DYN = N_NUM * P_DYN                    # ≈ 159,2 Hz
DOI_CHIEU = 2 * F_LUOI                   # 100 lần/s
# số liệu D3
N1, U1, U2 = 1650, 220, 12
P_DEN, SO_DEN = 24, 2
N2 = Fr(N1 * U2, U1)                     # 90 vòng
P2 = P_DEN * SO_DEN                      # 48 W
I2 = Fr(P2, U2)                          # 4 A
I1 = Fr(P2, U1)                          # ≈ 0,218 A
H_BA = Fr(94, 100)
I1_H = Fr(P2, 1) / H_BA / U1             # ≈ 0,232 A
N_6V = Fr(N1 * 6, U1)                    # vòng thứ 45
U_NHAM = Fr(U1) * N1 / N2                # ≈ 4033 V


def anim(attr, vals, dur, kt=None):
    k = f' keyTimes="{kt}"' if kt else ""
    return f'<animate attributeName="{attr}" values="{vals}"{k} dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


def anim_tr(kind, vals, dur, kt=None):
    k = f' keyTimes="{kt}"' if kt else ""
    return (f'<animateTransform attributeName="transform" type="{kind}" values="{vals}"{k} dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')


def tsub(x, y, base, s, rest="", c="currentColor", size=15, anchor="start", weight="700"):
    """Nhãn có chỉ số dưới: base_s + rest (chữ 15, chỉ số 12)."""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{base}<tspan dy="4" font-size="12">{s}</tspan><tspan dy="-4">{rest}</tspan></text>')


def magnet(x, y, w=110, h=30):
    """Nam châm thẳng nằm ngang: nửa trái S (xanh), nửa phải N (đỏ)."""
    b = f'<rect x="{x}" y="{y - h / 2}" width="{w / 2}" height="{h}" fill="{BLUE}" fill-opacity="0.55" stroke="currentColor" stroke-width="2"/>'
    b += f'<rect x="{x + w / 2}" y="{y - h / 2}" width="{w / 2}" height="{h}" fill="{RED}" fill-opacity="0.6" stroke="currentColor" stroke-width="2"/>'
    b += lbl(x + w / 4, y + 6, "S", "currentColor", 16, "middle", "700") + lbl(x + 3 * w / 4, y + 6, "N", "currentColor", 16, "middle", "700")
    return b


def bar_field(x, y, w=110):
    """Đường sức ngoài nam châm thẳng (đi ra ở N bên phải, vào S bên trái), nét đứt + chevron."""
    xn, xs = x + w, x
    b = field_line(xn, y, xn + 62, y, FL, 1.8)
    for sgn in (-1, 1):
        for (dy0, up, ext) in ((9, 46, 28), (13, 80, 52)):
            P = cubic((xn - 6, y + sgn * dy0), (xn + ext, y + sgn * up), (xs - ext, y + sgn * up), (xs + 6, y + sgn * dy0))
            d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in P)
            b += f'<path d="{d}" fill="none" stroke="{FL}" stroke-width="1.8" stroke-dasharray="6 4"/>' + chev_on(P, 30, FL, 1.8, 11)
    return b


# ═════════════ HÌNH ═════════════
# ───────────── Dạng 1 · nam châm và cuộn dây ─────────────
def coil_side(x0, n, gap, cy, ry, c="currentColor"):
    b = ""
    for i in range(n):
        b += f'<ellipse cx="{x0 + gap * i}" cy="{cy}" rx="7" ry="{ry}" fill="none" stroke="{c}" stroke-width="2.4"/>'
    return b


def d1(kk):
    b = ""
    if kk == 0:
        DUR = 9.0
        CY = 104
        X0C, NC, GAP = 262, 6, 18
        # nam châm + đường sức gắn theo nam châm (vẽ trước để cuộn dây đè lên)
        g = magnet(14, CY) + bar_field(14, CY)
        kt = "0;0.333;0.556;0.889;1"
        b += f'<g>{anim_tr("translate", "0 0;190 0;190 0;0 0;0 0", DUR, kt)}{g}</g>'
        b += coil_side(X0C, NC, GAP, CY, 38)
        b += seg(X0C - 7, CY - 38, X0C + GAP * (NC - 1), CY - 38, "currentColor", 1.4, "3 3")
        b += lbl(X0C - 4, CY - 46, "A", "currentColor", 16, "middle", "700")
        # dây nối điện kế
        xa, xb = X0C, X0C + GAP * (NC - 1)
        b += (f'<path d="M{xa},{CY + 38} L{xa},{214} L{xa + 22},{214}" fill="none" stroke="currentColor" stroke-width="2"/>'
              f'<path d="M{xb},{CY + 38} L{xb},{214} L{xb - 22},{214}" fill="none" stroke="currentColor" stroke-width="2"/>')
        gx = (xa + xb) / 2
        b += f'<circle cx="{gx}" cy="214" r="21" fill="none" stroke="currentColor" stroke-width="2.2"/>'
        b += lbl(gx, 220, "G", "currentColor", 16, "middle", "700") + lbl(gx + 28, 198, "?", RED, 18, "start", "700")
        # nhãn giai đoạn
        b += f'<g>{anim("opacity", "1;1;0;0", DUR, "0;0.333;0.334;1")}{lbl(14, 24, "1. đưa nam châm lại gần A", ORG, 15, "start", "700")}</g>'
        b += (f'<g opacity="0">{anim("opacity", "0;0;1;1;0;0", DUR, "0;0.333;0.334;0.555;0.556;1")}'
              f'{lbl(14, 24, "2. giữ yên trong lòng cuộn dây", ORG, 15, "start", "700")}</g>')
        b += f'<g opacity="0">{anim("opacity", "0;0;1;1", DUR, "0;0.556;0.557;1")}{lbl(14, 24, "3. kéo nam châm ra xa", ORG, 15, "start", "700")}</g>'
        return fig("c08-1-0", "0 0 420 244",
                   "Nam châm thẳng cực Bắc hướng về đầu A của cuộn dây nối điện kế; nam châm tiến vào lòng cuộn dây, nằm yên, rồi kéo ra xa",
                   b, "Mô phỏng chạy chậm: nam châm lại gần, nằm yên trong lòng cuộn dây, rồi ra xa; đường sức (nét đứt) đi theo nam châm. "
                      "Kim điện kế không vẽ: tự dự đoán từ số đường sức xuyên qua cuộn dây.")
    # hình dữ kiện: mẹo nhìn đầu ống dây (hệ quả của quy tắc nắm tay phải) — kiến thức nền, không theo đề
    for cx, ccw, pole, col in ((105, True, "N", RED), (315, False, "S", BLUE)):
        cy, r = 84, 46
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
        ts = [math.radians(40 + 280 * i / 40) for i in range(41)]
        if not ccw:
            ts = ts[::-1]
        pts = [(cx + (r + 12) * math.cos(t), cy - (r + 12) * math.sin(t)) for t in ts]
        b += poly(pts, ORG, 2.4) + chevron(*pts[-1], pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1], ORG, 2.4, 11)
        b += lbl(cx, cy + 9, pole, col, 28, "middle", "700")
        b += lbl(cx, 172, "ngược chiều kim đồng hồ" if ccw else "cùng chiều kim đồng hồ", ORG, 14, "middle", "700")
        b += lbl(cx, 192, "→ đầu này là cực Bắc" if ccw else "→ đầu này là cực Nam", col, 14, "middle", "700")
    b += lbl(210, 214, "(mắt nhìn thẳng vào một đầu ống dây)", "currentColor", 14, "middle", "400")
    return fig("c08-1-2", "0 0 420 226",
               "Nhìn thẳng vào đầu ống dây: dòng ngược chiều kim đồng hồ thì đầu đó là cực Bắc, cùng chiều kim đồng hồ thì là cực Nam",
               b, "Kiến thức nền: mẹo nhìn đầu ống dây, rút từ quy tắc nắm tay phải. Hình không theo số liệu của đề.")


# ───────────── Dạng 2 · máy phát: rôto nhiều cặp cực, dinamô ─────────────
def sector(cx, cy, r, a0, a1, fill):
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    return (f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{r},{r} 0 0 1 {x1:.1f},{y1:.1f} Z" fill="{fill}" fill-opacity="0.5" '
            f'stroke="currentColor" stroke-width="1.4"/>')


def rotor(cx, cy, r, npole, lab_r):
    b = ""
    step = 360 / npole
    for i in range(npole):
        a0 = -90 - step / 2 + i * step
        col = RED if i % 2 == 0 else BLUE
        b += sector(cx, cy, r, a0, a0 + step, col)
        am = math.radians(a0 + step / 2)
        b += lbl(cx + lab_r * math.cos(am), cy + lab_r * math.sin(am) + 5, "N" if i % 2 == 0 else "S", "currentColor", 14, "middle", "700")
    b += f'<circle cx="{cx}" cy="{cy}" r="7" fill="currentColor"/>'
    return b


def d2(kk):
    b = ""
    if kk == 0:
        DUR = 12.0
        CX, CY, R = 150, 146, 74
        g = rotor(CX, CY, R, 2 * P_TD, 56)
        b += f'<g>{anim_tr("rotate", f"0 {CX} {CY};360 {CX} {CY}", DUR)}{g}</g>'
        # stato: lõi + cuộn dây phía trên rôto
        b += f'<rect x="{CX - 16}" y="22" width="32" height="{CY - R - 28}" fill="{GREY}" fill-opacity="0.35" stroke="currentColor" stroke-width="1.8"/>'
        for k in range(5):
            yy = 30 + k * 9
            b += seg(CX - 24, yy, CX + 24, yy + 4, ORG, 2.6)
        b += (f'<path d="M{CX - 24},30 L{CX - 46},30 L{CX - 46},12" fill="none" stroke="{ORG}" stroke-width="2"/>'
              f'<path d="M{CX + 24},70 L{CX + 46},70 L{CX + 46},12" fill="none" stroke="{ORG}" stroke-width="2"/>')
        b += lbl(CX + 54, 34, "cuộn dây (stato, đứng yên)", ORG, 14, "start", "700")
        b += lbl(250, 120, "rôto nam châm:", "currentColor", 14, "start", "700")
        b += lbl(250, 140, "6 cặp cực (12 cực)", "currentColor", 14, "start", "400")
        b += lbl(250, 168, "f = 50 Hz", BLUE, 15, "start", "700")
        b += lbl(250, 192, "n = ?", GRN, 15, "start", "700")
        b += arrow("", "g", CX - R - 8, CY + 22, CX - R - 14, CY - 4, 2.2) + lbl(CX - R - 18, CY + 14, "quay", GRN, 14, "end", "700")
        return fig("c08-2-0", "0 0 420 236",
                   "Rôto nam châm có 12 cực Bắc Nam xen kẽ quay dưới một cuộn dây đứng yên của stato",
                   b, "Mô phỏng chạy chậm, không đúng tốc độ thật: rôto nam châm quay, các cực Bắc và Nam lần lượt đi qua dưới cuộn dây.")
    # hình dữ kiện: dinamô xe đạp (không theo tỉ lệ)
    TX, TY, TR = 120, 168, 104
    b += f'<path d="M{TX - TR},{TY} A{TR},{TR} 0 0 1 {TX + TR},{TY}" fill="none" stroke="currentColor" stroke-width="6" opacity="0.55"/>'
    b += lbl(TX, TY - 30, "lốp xe", "currentColor", 14, "middle", "400")
    a = math.radians(38)
    kr = 16
    kx, ky = TX + (TR + 3 + kr) * math.cos(a), TY - (TR + 3 + kr) * math.sin(a)
    b += f'<circle cx="{kx:.1f}" cy="{ky:.1f}" r="{kr}" fill="none" stroke="{ORG}" stroke-width="2.4"/>'
    b += seg(kx - kr, ky + 26, kx + kr, ky + 26, ORG, 1.6) + seg(kx - kr, ky + 20, kx - kr, ky + 32, ORG, 1.4) + seg(kx + kr, ky + 20, kx + kr, ky + 32, ORG, 1.4)
    b += lbl(kx + kr + 6, ky + 31, "d = 2 cm", ORG, 14, "start", "700")
    b += lbl(kx, ky - kr - 8, "núm dinamô", ORG, 14, "middle", "700")
    b += arrow("", "r", TX - 40, TY - TR - 12, TX + 30, TY - TR - 12, 2.6) + lbl(TX - 4, TY - TR - 20, "v = 18 km/h", RED, 14, "middle", "700")
    # nam châm 4 cực trong dinamô
    MX, MY = 340, 150
    b += rotor(MX, MY, 40, 4, 25)
    b += lbl(MX, MY + 62, "nam châm 4 cực", "currentColor", 14, "middle", "700")
    b += lbl(MX, 98, "n = ? ; f = ?", GRN, 15, "middle", "700")
    return fig("c08-2-2", "0 0 420 228",
               "Núm dinamô đường kính 2 cm tì vào mép lốp xe chạy 18 km/h; bên trong dinamô là nam châm 4 cực",
               b, "Dữ kiện câu c, hình không theo tỉ lệ. Núm lăn không trượt trên mép lốp.")


# ───────────── Dạng 3 · máy biến áp hạ áp ─────────────
def lamp(x, y, glow=""):
    return (f'<circle cx="{x}" cy="{y}" r="13" fill="{YEL}" fill-opacity="0" stroke="currentColor" stroke-width="2">{glow}</circle>'
            + seg(x - 9, y - 9, x + 9, y + 9, "currentColor", 1.6) + seg(x - 9, y + 9, x + 9, y - 9, "currentColor", 1.6))


def core(b_only=False):
    b = (f'<path d="M110,40 H300 V196 H110 Z M150,80 V156 H260 V80 Z" fill="{GREY}" fill-opacity="0.3" fill-rule="evenodd" '
         f'stroke="currentColor" stroke-width="1.8"/>')
    for k in range(9):                                     # cuộn sơ cấp (trái), vẽ không theo tỉ lệ số vòng
        yy = 62 + k * 12
        b += seg(102, yy, 158, yy + 5, ORG, 2.6)
    for k in range(4):                                     # cuộn thứ cấp (phải)
        yy = 88 + k * 16
        b += seg(252, yy, 308, yy + 5, BLUE, 2.6)
    return b


def d3(kk):
    b = ""
    if kk == 0:
        DUR = 6.0
        b += core()
        # nguồn xoay chiều
        b += (f'<path d="M102,62 L56,62 L56,98" fill="none" stroke="{ORG}" stroke-width="2"/>'
              f'<path d="M102,163 L56,163 L56,138" fill="none" stroke="{ORG}" stroke-width="2"/>')
        b += f'<circle cx="56" cy="118" r="20" fill="none" stroke="currentColor" stroke-width="2.2"/>' + lbl(56, 125, "~", "currentColor", 22, "middle", "700")
        b += lbl(56, 214, "220 V", ORG, 15, "middle", "700")
        b += tsub(130, 30, "N", "1", " = 1650", ORG, anchor="middle")
        b += tsub(280, 30, "N", "2", " = ?", BLUE, anchor="middle")
        # tải: 2 đèn song song
        # thứ cấp: đầu trên → thanh trái x=346; đầu dưới → vòng xuống → thanh phải x=400; hai đèn nối giữa hai thanh
        b += f'<path d="M308,88 L346,88 L346,158" fill="none" stroke="{BLUE}" stroke-width="2"/>'
        b += f'<path d="M308,141 L326,141 L326,186 L400,186 L400,112" fill="none" stroke="{BLUE}" stroke-width="2"/>'
        glow = anim("fill-opacity", "0;0;0.85;0.85", DUR, "0;0.15;0.3;1")
        for ly in (112, 158):
            b += lamp(373, ly, glow) + seg(346, ly, 360, ly, BLUE, 2) + seg(386, ly, 400, ly, BLUE, 2)
        b += lbl(414, 210, "2 đèn 12 V – 24 W", BLUE, 14, "end", "700")
        # đường sức trong lõi: nét đứt, chiều đổi liên tục (hai nhóm chevron luân phiên)
        b += f'<rect x="130" y="60" width="150" height="116" fill="none" stroke="{FL}" stroke-width="1.8" stroke-dasharray="6 4"/>'
        cw = chevron(205, 60, 1, 0, FL, 2, 11) + chevron(205, 176, -1, 0, FL, 2, 11)
        ccw = chevron(205, 60, -1, 0, FL, 2, 11) + chevron(205, 176, 1, 0, FL, 2, 11)
        disc = 'calcMode="discrete" keyTimes="0;0.125;0.25;0.375;0.5;0.625;0.75;0.875;1"'
        b += (f'<g>{cw}<animate attributeName="opacity" values="1;0;1;0;1;0;1;0;1" {disc} dur="{DUR:.2f}s" begin="indefinite" fill="freeze"/></g>'
              f'<g opacity="0">{ccw}<animate attributeName="opacity" values="0;1;0;1;0;1;0;1;0" {disc} dur="{DUR:.2f}s" begin="indefinite" fill="freeze"/></g>')
        b += lbl(205, 120, "lõi thép", "currentColor", 14, "middle", "400")
        return fig("c08-3-0", "0 0 420 228",
                   "Máy biến áp: cuộn sơ cấp 1650 vòng nối nguồn xoay chiều 220 V, cuộn thứ cấp chưa biết số vòng nối hai đèn song song",
                   b, "Mô phỏng chạy chậm: đường sức trong lõi (nét đứt) đổi chiều liên tục theo dòng xoay chiều, hai đèn sáng. "
                      "Số vòng vẽ không theo tỉ lệ.")
    # hình dữ kiện: hai cuộn và các đại lượng
    b += f'<rect x="14" y="14" width="180" height="104" rx="8" fill="none" stroke="{ORG}" stroke-width="2.2"/>'
    b += lbl(104, 36, "Sơ cấp (nối nguồn)", ORG, 15, "middle", "700")
    b += tsub(30, 62, "N", "1", " = 1650 vòng", "currentColor", 14, weight="400")
    b += tsub(30, 84, "U", "1", " = 220 V", "currentColor", 14, weight="400")
    b += tsub(30, 106, "I", "1", " = ?", GRN, 14)
    b += f'<rect x="226" y="14" width="180" height="104" rx="8" fill="none" stroke="{BLUE}" stroke-width="2.2"/>'
    b += lbl(316, 36, "Thứ cấp (nối tải)", BLUE, 15, "middle", "700")
    b += tsub(242, 62, "N", "2", " = ?", GRN, 14)
    b += tsub(242, 84, "U", "2", " = 12 V", "currentColor", 14, weight="400")
    b += tsub(242, 106, "I", "2", " = ?", GRN, 14)
    b += arrow("", "o", 196, 66, 224, 66, 2.4)
    b += lbl(210, 140, "lõi thép: từ trường biến thiên", "currentColor", 14, "middle", "400")
    b += lbl(316, 162, "tải: 2 đèn 12 V – 24 W", BLUE, 14, "middle", "700")
    b += lbl(316, 180, "mắc song song", BLUE, 14, "middle", "400")
    b += lbl(104, 162, "đầu ra 6 V:", "currentColor", 14, "middle", "700")
    b += lbl(104, 180, "rút ở vòng thứ ?", GRN, 14, "middle", "700")
    return fig("c08-3-2", "0 0 420 194",
               "Sơ đồ đại lượng: sơ cấp 1650 vòng, 220 V, dòng chưa biết; thứ cấp 12 V, số vòng và dòng chưa biết; tải hai đèn song song",
               b, "Dữ kiện: chỉ số 1 là cuộn nối nguồn, chỉ số 2 là cuộn nối tải.")


BUILD = [d1, d2, d3]

# ═════════════ ĐỀ ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Điều kiện xuất hiện và chiều của dòng điện cảm ứng (định tính)",
      topic=TOPIC_D1,
      problem_html=r"""<p>Một cuộn dây dẫn có hai đầu nối kín với một điện kế G (kim lệch sang trái hay sang phải tuỳ chiều dòng điện). Một nam châm thẳng đặt trên trục của cuộn dây, cực Bắc (N) hướng về đầu A của cuộn dây (hình dưới).</p><ol type="a"><li>Đưa nam châm lại gần đầu A. Trong cuộn dây có dòng điện cảm ứng không? Đầu A trở thành cực từ gì? Nhìn từ phía nam châm vào đầu A, dòng điện chạy cùng hay ngược chiều kim đồng hồ?</li><li>Giữ nam châm nằm yên trong lòng cuộn dây. Có dòng điện cảm ứng không?</li><li>Kéo nam châm ra xa đầu A. Trả lời các câu hỏi như câu a.</li><li>Đặt nam châm gần đầu A rồi quay nam châm quanh chính trục dọc của nó (trục này trùng trục cuộn dây). Có dòng điện cảm ứng không?</li><li>Thay nam châm thẳng bằng một nam châm điện đặt yên ở chỗ cũ, nối với pin qua khoá K. Điện kế cho thấy gì khi đóng K, khi giữ K đóng, và khi ngắt K?</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Máy phát điện xoay chiều: tần số, tốc độ quay và số cặp cực",
      topic=TOPIC_D2,
      problem_html=r"""<p>Tần số dòng điện của máy phát có rôto là nam châm: $f=np$, trong đó $n$ là số vòng quay mỗi giây, $p$ là số cặp cực.</p><ol type="a"><li>Rôto của một máy phát ở nhà máy thuỷ điện là nam châm có $6$ cặp cực. Máy phát ra dòng điện tần số $50\ \text{Hz}$. Rôto quay bao nhiêu vòng mỗi phút?</li><li>Lưu lượng nước giảm, rôto chỉ còn quay $480$ vòng/phút. Tần số dòng điện phát ra lúc này bằng bao nhiêu?</li><li>Một dinamô xe đạp có núm quay đường kính $2\ \text{cm}$ tì vào mép ngoài của lốp và lăn không trượt; nam châm trong dinamô có $4$ cực (Bắc, Nam xen kẽ). Xe chạy đều với tốc độ $18\ \text{km/h}$; coi tốc độ dài của mép lốp bằng tốc độ của xe. Núm quay bao nhiêu vòng mỗi giây, và dòng điện dinamô phát ra có tần số bao nhiêu?</li><li>Dòng điện lưới ở Việt Nam có tần số $50\ \text{Hz}$. Mỗi giây dòng điện này đổi chiều bao nhiêu lần?</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Máy biến áp: số vòng, cường độ dòng điện và khi lắp nhầm cuộn",
      topic=TOPIC_D3,
      problem_html=r"""<p>Cần một máy biến áp hạ áp để thắp sáng bình thường hai bóng đèn loại $12\ \text{V} - 24\ \text{W}$ mắc song song. Cuộn sơ cấp có $1650$ vòng, nối vào nguồn điện xoay chiều $220\ \text{V}$. Coi máy biến áp là lí tưởng (bỏ qua mọi hao phí) trừ chỗ đề nói khác.</p><ol type="a"><li>Tính số vòng của cuộn thứ cấp.</li><li>Tính cường độ dòng điện chạy qua cuộn thứ cấp và qua cuộn sơ cấp. Nếu máy thực có hiệu suất $H_{\text{BA}}=94\%$ (hai đèn vẫn sáng bình thường) thì dòng điện qua cuộn sơ cấp bằng bao nhiêu?</li><li>Muốn có thêm một đầu ra $6\ \text{V}$ trên cuộn thứ cấp thì phải rút đầu dây ở vòng thứ bao nhiêu, tính từ một đầu của cuộn thứ cấp?</li><li>Một bạn lắp nhầm, nối nguồn $220\ \text{V}$ vào cuộn thứ cấp. Khi đó hiệu điện thế giữa hai đầu cuộn $1650$ vòng bằng bao nhiêu? Nhận xét.</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 # Dạng 1
 [(r'"cuộn dây dẫn có hai đầu nối kín với một điện kế"', r"Mạch kín có điện kế",
   r"⚠ chỉ trong mạch KÍN dòng cảm ứng mới chạy được<br>Điện kế lệch hai phía: biết cả có dòng lẫn chiều dòng"),
  (r'"nam châm thẳng đặt trên trục của cuộn dây, cực Bắc (N) hướng về đầu A"', r"Cực N đối diện đầu A",
   r"Ngoài nam châm, đường sức đi ra từ cực Bắc, đi vào cực Nam"),
  (r'"Đưa nam châm lại gần đầu A"', r"Khoảng cách giảm", r"Số đường sức xuyên qua tiết diện cuộn dây thay đổi thế nào?"),
  (r'"Đầu A trở thành cực từ gì?"', r"Cần: cực của A",
   r"Định luật Lenz: dòng cảm ứng chống lại sự biến thiên của số đường sức<br>Cùng tên đẩy nhau, khác tên hút nhau"),
  (r'"Nhìn từ phía nam châm vào đầu A … chiều kim đồng hồ"', r"Cần: chiều dòng", r"Quy tắc nắm tay phải (mẹo nhìn đầu ống dây)"),
  (r'"Giữ nam châm nằm yên trong lòng cuộn dây"', r"Không còn chuyển động tương đối", r"Số đường sức qua cuộn dây có thay đổi không?"),
  (r'"quay nam châm quanh chính trục dọc của nó"', r"Nam châm có chuyển động",
   r"⚠ điều kiện là số đường sức BIẾN THIÊN, không phải chỉ cần có chuyển động<br>Khi quay như vậy, đường sức quanh trục có đổi chỗ không?"),
  (r'"nam châm điện đặt yên … đóng K, giữ K đóng, ngắt K"', r"Dòng qua nam châm điện ở từng giai đoạn",
   r"Từ trường nam châm điện mạnh, yếu theo dòng điện chạy qua nó")],
 # Dạng 2
 [(r'"$f=np$ … $n$ là số vòng quay mỗi giây, $p$ là số cặp cực"', r"Công thức đề cho",
   r"⚠ $n$ tính bằng vòng/s<br>⚠ $p$ là số CẶP cực, không phải số cực"),
  (r'"nam châm có $6$ cặp cực … tần số $50\ \text{Hz}$"', r"$p=6$; $f=50\ \text{Hz}$", r"Rút $n$ từ $f=np$"),
  (r'"Rôto quay bao nhiêu vòng mỗi phút?"', r"Cần $n$ theo vòng/phút", r"$1$ vòng/s $=60$ vòng/phút"),
  (r'"rôto chỉ còn quay $480$ vòng/phút"', r"$n'=480$ vòng/phút", r"Đơn vị này đã dùng thẳng trong $f=np$ được chưa?"),
  (r'"núm quay đường kính $2\ \text{cm}$ … lăn không trượt"', r"$d=0{,}02\ \text{m}$",
   r"Lăn không trượt: chỗ tiếp xúc của núm và lốp có cùng tốc độ dài<br>Mỗi vòng núm lăn được một chu vi $\pi d$"),
  (r'"Xe chạy đều với tốc độ $18\ \text{km/h}$; coi tốc độ dài của mép lốp bằng tốc độ của xe"', r"$v=18\ \text{km/h}$",
   r"Đổi: $1\ \text{km/h}=\dfrac{1}{3{,}6}\ \text{m/s}$"),
  (r'"nam châm trong dinamô có $4$ cực"', r"$4$ cực", r"Một cặp cực gồm những cực nào?"),
  (r'"Mỗi giây dòng điện này đổi chiều bao nhiêu lần?"', r"$f=50\ \text{Hz}$", r"Trong một chu kì, dòng xoay chiều đổi chiều mấy lần?")],
 # Dạng 3
 [(r'"Coi máy biến áp là lí tưởng (bỏ qua mọi hao phí)"', r"Không hao phí",
   r"⚠ chỉ máy lí tưởng mới có $U_1I_1=U_2I_2$<br>⚠ máy biến áp chỉ làm việc với dòng xoay chiều"),
  (r'"Cuộn sơ cấp có $1650$ vòng, nối vào nguồn … $220\ \text{V}$"', r"$N_1=1650$; $U_1=220\ \text{V}$",
   r"Cuộn nối nguồn là cuộn sơ cấp (chỉ số 1)"),
  (r'"thắp sáng bình thường hai bóng đèn loại $12\ \text{V} - 24\ \text{W}$ mắc song song"', r"$U_2=12\ \text{V}$; mỗi đèn $24\ \text{W}$",
   r"Đèn sáng bình thường: hiệu điện thế đúng định mức<br>Mạch song song: công suất toàn mạch bằng tổng công suất các đèn"),
  (r'"Tính số vòng của cuộn thứ cấp"', r"Cần $N_2$", r"$\dfrac{U_1}{U_2}=\dfrac{N_1}{N_2}$"),
  (r'"cường độ dòng điện chạy qua cuộn thứ cấp và qua cuộn sơ cấp"', r"Cần $I_2$; $I_1$", r"$P=UI$ cho từng cuộn"),
  (r'"hiệu suất $H_{\text{BA}}=94\%$ (hai đèn vẫn sáng bình thường)"', r"$H_{\text{BA}}=0{,}94$; $P_2$ không đổi",
   r"$H_{\text{BA}}=\dfrac{P_2}{P_1}$: công suất phía nào lớn hơn?"),
  (r'"đầu ra $6\ \text{V}$ … rút đầu dây ở vòng thứ bao nhiêu"', r"$U=6\ \text{V}$", r"Hiệu điện thế ra tỉ lệ với số vòng dùng tới"),
  (r'"nối nguồn $220\ \text{V}$ vào cuộn thứ cấp"', r"Nguồn đổi sang cuộn kia", r"Cuộn nào bây giờ là sơ cấp?")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = [r"<strong>Khái niệm:</strong> số đường sức từ xuyên qua tiết diện cuộn dây (còn gọi là từ thông).",
      r"<strong>Điều kiện:</strong> cuộn dây kín và số đường sức xuyên qua tiết diện của nó biến thiên thì có dòng điện cảm ứng.",
      r"<strong>Định luật Lenz (mở rộng HSG):</strong> dòng cảm ứng sinh ra từ trường chống lại sự biến thiên của số đường sức.",
      r"<strong>Quy tắc nắm tay phải:</strong> nhìn thẳng vào một đầu ống dây, thấy dòng ngược chiều kim đồng hồ thì đầu đó là cực Bắc."]
R2 = [r"<strong>Khái niệm:</strong> máy phát có rôto nam châm quay trước cuộn dây đứng yên (stato); mỗi cặp cực đi qua cuộn dây cho một chu kì.",
      r"<strong>Công thức:</strong> $f=np$ với $n$ (vòng/s), $p$ (số cặp cực).",
      r"<strong>Lăn không trượt:</strong> mỗi vòng núm lăn được một chu vi $\pi d$, nên $n=\dfrac{v}{\pi d}$.",
      r"<strong>Đổi đơn vị:</strong> $1$ vòng/s $=60$ vòng/phút; $1\ \text{km/h}=\dfrac{1}{3{,}6}\ \text{m/s}$.",
      r"<strong>Chiều dòng:</strong> trong mỗi chu kì, dòng xoay chiều đổi chiều $2$ lần."]
R3 = [r"<strong>Khái niệm:</strong> cuộn nối nguồn là sơ cấp (chỉ số 1), cuộn nối tải là thứ cấp (chỉ số 2).",
      r"<strong>Định luật:</strong> $\dfrac{U_1}{U_2}=\dfrac{N_1}{N_2}$.",
      r"<strong>Máy lí tưởng:</strong> $U_1I_1=U_2I_2$ nên $\dfrac{I_1}{I_2}=\dfrac{N_2}{N_1}$.",
      r"<strong>Máy thực:</strong> $H_{\text{BA}}=\dfrac{P_2}{P_1}$, với $P=UI$ (CĐ05).",
      r"<strong>Điều kiện:</strong> chỉ dùng với dòng xoay chiều."]

SOLS = [
 sol(R1, [
  ("Câu a: có dòng cảm ứng không", [P(r"Nam châm lại gần thì từ trường ở chỗ cuộn dây mạnh lên: số đường sức xuyên qua tiết diện cuộn dây <strong>tăng</strong>."),
     P(r"Cuộn dây kín, số đường sức biến thiên:"), A(r"T:Có dòng điện cảm ứng, kim điện kế lệch.")]),
  ("Câu a: đầu A là cực gì", [P(r"Theo định luật Lenz, dòng cảm ứng chống lại sự tăng, tức là cản nam châm tiến lại."),
     P(r"Muốn đẩy cực Bắc đang tiến tới thì đầu A phải cùng tên:"), A(r"T:Đầu A là cực Bắc (đẩy nam châm).")]),
  ("Câu a: chiều dòng điện", [P(r"Nhìn thẳng vào đầu A (từ phía nam châm), đầu A là cực Bắc nên theo quy tắc nắm tay phải:"),
     A(r"T:Dòng chạy ngược chiều kim đồng hồ.")]),
  ("Câu b: nam châm nằm yên", [P(r"Nam châm và cuộn dây đứng yên với nhau: số đường sức qua cuộn dây lớn nhưng <strong>không đổi</strong>."),
     A(r"T:Không có dòng cảm ứng, kim điện kế về số 0.")]),
  ("Câu c: kéo nam châm ra xa", [P(r"Số đường sức qua cuộn dây <strong>giảm</strong>: có dòng cảm ứng, ngược chiều với câu a."),
     P(r"Dòng cảm ứng chống lại sự giảm, tức là giữ nam châm lại: đầu A hút cực Bắc nên là cực Nam."),
     A(r"T:Có dòng; đầu A là cực Nam; nhìn từ nam châm, dòng chạy cùng chiều kim đồng hồ.")]),
  ("Câu d: quay quanh trục dọc", [P(r"Đường sức của nam châm thẳng phân bố đều quanh trục dọc của nó. Quay quanh trục đó, hình đường sức không đổi chỗ, cực Bắc vẫn hướng về A."),
     P(r"Số đường sức qua cuộn dây không đổi dù nam châm đang chuyển động:"), A(r"T:Không có dòng cảm ứng.")]),
  ("Câu e: nam châm điện", [P(r"Đóng K: dòng qua nam châm điện tăng từ $0$, từ trường mạnh dần, số đường sức qua cuộn dây tăng: có dòng cảm ứng trong thời gian ngắn."),
     P(r"Giữ K đóng: dòng không đổi, số đường sức không đổi: không có dòng."),
     P(r"Ngắt K: từ trường mất đi, số đường sức giảm: có dòng thoáng qua, ngược chiều lúc đóng."),
     A(r"T:Kim lệch rồi về 0; đứng ở 0; lệch về phía ngược lại rồi về 0.")]),
  ("Kiểm tra", [P(r"Mọi trường hợp có dòng đều có số đường sức biến thiên; mọi trường hợp không có dòng (b, d, giữ K) đều có số đường sức không đổi ✓."),
     P(r"Câu a và c: một lần đẩy, một lần hút, luôn cản chuyển động của nam châm. Muốn di chuyển nam châm phải tốn công, công đó chuyển thành điện năng: đúng bảo toàn năng lượng ✓.")])],
  [r"a) Có dòng; A là cực Bắc; dòng ngược chiều kim đồng hồ (nhìn từ nam châm)", r"b) Không có dòng",
   r"c) Có dòng; A là cực Nam; dòng cùng chiều kim đồng hồ (nhìn từ nam châm)", r"d) Không có dòng",
   r"e) Đóng K: dòng thoáng qua", r"Giữ K đóng: không có dòng", r"Ngắt K: dòng thoáng qua, ngược chiều lúc đóng"],
  r"Nhận dạng: thấy <strong>nam châm, cuộn dây kín, hỏi có dòng không</strong> → xét số đường sức qua cuộn dây có biến thiên không, rồi dùng Lenz tìm chiều."),
 sol(R2, [
  ("Tốc độ quay của rôto thuỷ điện", [M(r"n=\dfrac{f}{p}=\dfrac{50}{6}\approx8{,}33\ \text{vòng/s}"), M(r"n=\dfrac{50}{6}\cdot60"),
     A(r"n=500\ \text{vòng/phút}")]),
  ("Tần số khi rôto chậm lại", [P(r"Đổi ra vòng/s trước:"), M(r"n'=\dfrac{480}{60}=8\ \text{vòng/s}"), M(r"f'=n'p=8\cdot6"), A(r"f'=48\ \text{Hz}"),
     P(r"Tần số lệch khỏi $50\ \text{Hz}$ của lưới, nhà máy phải tăng lưu lượng nước để rôto quay lại đủ nhanh.")]),
  ("Tốc độ quay của núm", [P(r"Đổi $v=18\ \text{km/h}=\dfrac{18}{3{,}6}=5\ \text{m/s}$. Mỗi vòng núm lăn được $\pi d$:"),
     M(r"n=\dfrac{v}{\pi d}=\dfrac{5}{\pi\cdot0{,}02}"), A(r"n\approx79{,}6\ \text{vòng/s}")]),
  ("Tần số dòng điện của dinamô", [P(r"Nam châm $4$ cực gồm $2$ cặp (mỗi cặp một N và một S): $p=2$."),
     M(r"f=np=79{,}58\cdot2"), A(r"f\approx159\ \text{Hz}")]),
  ("Số lần đổi chiều mỗi giây", [P(r"Mỗi chu kì dòng đổi chiều $2$ lần; mỗi giây có $50$ chu kì:"), M(r"2f=2\cdot50"), A(r"100\ \text{lần}")]),
  ("Kiểm tra", [P(r"Câu a: máy nhiều cặp cực quay chậm ($500$ vòng/phút) vẫn cho đủ $50\ \text{Hz}$, hợp với tuabin nước quay chậm ✓."),
     P(r"Câu c: núm rất nhỏ nên quay rất nhanh, tần số lớn hơn $50\ \text{Hz}$ là hợp lí. Lấy nhầm $p=4$ sẽ ra khoảng $318\ \text{Hz}$, gấp đôi giá trị đúng."),
     P(r"Đơn vị: $\dfrac{\text{vòng}}{\text{s}}\cdot(\text{số cặp cực})=\dfrac{1}{\text{s}}=\text{Hz}$ ✓.")])],
  [r"a) $n=500$ vòng/phút", r"b) $f'=48\ \text{Hz}$", r"c) Núm quay khoảng $79{,}6$ vòng/s", r"Tần số khoảng $159\ \text{Hz}$", r"d) $100$ lần mỗi giây"],
  r"Nhận dạng: thấy <strong>số cặp cực, vòng/phút, tần số</strong> → $f=np$, đổi $n$ ra vòng/s, $p$ là số CẶP cực."),
 sol(R3, [
  ("Số vòng cuộn thứ cấp", [M(r"\dfrac{U_1}{U_2}=\dfrac{N_1}{N_2}\ \Rightarrow\ N_2=N_1\dfrac{U_2}{U_1}"), M(r"N_2=1650\cdot\dfrac{12}{220}"), A(r"N_2=90\ \text{vòng}")]),
  ("Dòng điện qua cuộn thứ cấp", [P(r"Hai đèn song song sáng bình thường: $P_2=2\cdot24=48\ \text{W}$ ở $U_2=12\ \text{V}$."),
     M(r"I_2=\dfrac{P_2}{U_2}=\dfrac{48}{12}"), A(r"I_2=4\ \text{A}")]),
  ("Dòng điện qua cuộn sơ cấp (lí tưởng)", [M(r"U_1I_1=U_2I_2=48\ \text{W}"), M(r"I_1=\dfrac{48}{220}"), A(r"I_1\approx0{,}218\ \text{A}"),
     P(r"Cách khác: $\dfrac{I_1}{I_2}=\dfrac{N_2}{N_1}=\dfrac{90}{1650}$, cho cùng kết quả.")]),
  ("Dòng sơ cấp khi hiệu suất 94 %", [P(r"Tải vẫn dùng $P_2=48\ \text{W}$, máy hao phí nên nguồn phải cấp nhiều hơn:"),
     M(r"P_1=\dfrac{P_2}{H_{\text{BA}}}=\dfrac{48}{0{,}94}\approx51{,}1\ \text{W}"), M(r"I_1'=\dfrac{P_1}{U_1}=\dfrac{51{,}06}{220}"), A(r"I_1'\approx0{,}232\ \text{A}")]),
  ("Vị trí đầu ra 6 V", [P(r"Hiệu điện thế lấy ra tỉ lệ với số vòng dùng tới:"), M(r"N_x=N_2\cdot\dfrac{6}{12}=N_1\cdot\dfrac{6}{220}=\dfrac{1650\cdot6}{220}"),
     A(r"N_x=45\ \text{vòng}"), P(r"Rút đầu dây ở vòng thứ $45$; giữa đầu đó và đầu đầu tiên của cuộn thứ cấp có $6\ \text{V}$.")]),
  ("Lắp nhầm cuộn", [P(r"Cuộn nối nguồn (cuộn $90$ vòng) giờ là sơ cấp:"), M(r"U'=220\cdot\dfrac{1650}{90}"), A(r"U'\approx4033\ \text{V}"),
     P(r"Máy thành máy tăng áp: đầu cuộn $1650$ vòng có hơn $4000\ \text{V}$, chạm vào rất nguy hiểm. Cuộn $90$ vòng chỉ chịu được khoảng $12\ \text{V}$, nên máy còn bị quá tải, nóng và có thể cháy.")]),
  ("Kiểm tra", [P(r"Máy hạ áp: $N_2\lt N_1$ ✓ và $I_2\gt I_1$ ✓ (hạ áp bao nhiêu lần thì dòng tăng bấy nhiêu lần: $\dfrac{220}{12}\approx18{,}3$, $\dfrac{4}{0{,}218}\approx18{,}3$ ✓)."),
     P(r"Máy thực: $I_1'\gt I_1$ vì nguồn phải bù phần hao phí ✓."),
     P(r"Đơn vị: $\dfrac{\text{W}}{\text{V}}=\text{A}$ ✓.")])],
  [r"a) $N_2=90$ vòng", r"b) $I_2=4\ \text{A}$; $I_1\approx0{,}218\ \text{A}$", r"Với $H_{\text{BA}}=94\%$: $I_1'\approx0{,}232\ \text{A}$",
   r"c) Rút ở vòng thứ $45$", r"d) $U'\approx4033\ \text{V}$: máy thành tăng áp, rất nguy hiểm"],
  r"Nhận dạng: thấy <strong>số vòng sơ cấp, thứ cấp, hiệu điện thế vào, ra</strong> → $\dfrac{U_1}{U_2}=\dfrac{N_1}{N_2}$; dòng điện qua $U_1I_1=U_2I_2$ (lí tưởng)."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>nam châm lại gần, ra xa cuộn dây kín</b> → xét số đường sức có biến thiên không, dùng Lenz tìm chiều.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Câu a: có dòng cảm ứng không", "Khi đưa nam châm lại gần đầu A, trong cuộn dây có dòng điện cảm ứng không?",
       lua_chon=[(r"Có, vì số đường sức từ xuyên qua tiết diện cuộn dây tăng", True),
                 (r"Không, vì nam châm không chạm vào cuộn dây", r"Dòng cảm ứng không cần tiếp xúc; chỉ cần số đường sức qua cuộn dây biến thiên."),
                 (r"Có, vì cuộn dây nằm trong từ trường của nam châm", r"Kết luận đúng nhưng lí do sai: chỉ nằm trong từ trường chưa đủ, điều kiện là số đường sức qua cuộn dây biến thiên.")],
       loi=r"Nghĩ rằng cứ có nam châm ở gần cuộn dây là có dòng cảm ứng."),
  buoc("Câu a: đầu A là cực gì", "Khi nam châm lại gần, đầu A của cuộn dây trở thành cực gì?",
       lua_chon=[(r"Cực Bắc, để đẩy cực Bắc của nam châm đang tiến lại", True),
                 (r"Cực Nam, để hút nam châm", r"Hút thì nam châm càng tới gần, số đường sức càng tăng: dòng cảm ứng tiếp tay cho sự biến thiên, trái định luật Lenz và bảo toàn năng lượng."),
                 (r"Không thành cực nào vì dòng cảm ứng rất nhỏ", r"Có dòng chạy trong ống dây thì ống dây là một nam châm, dù yếu.")],
       loi=r"Đọc định luật Lenz thành &quot;chống lại từ trường của nam châm&quot; thay cho &quot;chống lại sự biến thiên&quot;.",
       ke=[(r"Dùng định luật Lenz: dòng cảm ứng chống lại sự tăng số đường sức", True),
           (r"Dùng ngay quy tắc nắm tay phải", r"Chưa biết chiều dòng điện thì chưa nắm tay phải được; cực của A phải tìm trước bằng định luật Lenz."),
           (r"Dựa vào đường sức của nam châm: đường sức đi vào đầu A nên A là cực Nam", r"Đó là từ trường của nam châm; cực của A do từ trường của chính dòng cảm ứng quyết định.")]),
  buoc("Câu a: chiều dòng điện", "Nhìn từ phía nam châm vào đầu A, dòng điện cảm ứng chạy theo chiều nào?",
       lua_chon=[(r"Ngược chiều kim đồng hồ", True),
                 (r"Cùng chiều kim đồng hồ", r"Nhìn vào một đầu ống mà thấy dòng cùng chiều kim đồng hồ thì đầu đó là cực Nam, trái với cực vừa tìm.")],
       loi=r"Đặt mắt sai chỗ: nhìn từ phía trong ống ra thì chiều quay thấy được bị đảo ngược.",
       ke=[(r"Từ cực của đầu A, dùng quy tắc nắm tay phải (mẹo nhìn đầu ống) suy ra chiều dòng", True),
           (r"Lấy chiều theo đường sức của nam châm đi vào đầu A", r"Đường sức là đường thẳng đi dọc trục, không cho biết dòng quay chiều nào quanh trục."),
           (r"Kết luận không xác định được vì chưa biết chiều quấn dây", r"Khi nhìn thẳng vào đầu A thì không cần chiều quấn: chỉ cần biết A là cực gì.")]),
  buoc("Câu b: nam châm nằm yên", "Giữ nam châm nằm yên trong lòng cuộn dây: có dòng điện cảm ứng không?",
       lua_chon=[(r"Không, vì số đường sức qua cuộn dây không đổi", True),
                 (r"Có, vì từ trường trong lòng cuộn dây lúc này mạnh nhất", r"Từ trường mạnh nhưng không đổi; dòng cảm ứng cần số đường sức biến thiên."),
                 (r"Có, và dòng giữ nguyên như lúc nam châm đang tiến vào", r"Nam châm vừa dừng thì số đường sức thôi biến thiên, dòng cảm ứng mất ngay.")],
       loi=r"Nhầm &quot;nhiều đường sức&quot; với &quot;số đường sức biến thiên&quot;.",
       ke=[(r"So số đường sức qua cuộn dây ở hai thời điểm khác nhau trong lúc nam châm nằm yên", True),
           (r"Xét từ trường trong cuộn dây mạnh hay yếu", r"Điều kiện không phụ thuộc từ trường mạnh hay yếu mà phụ thuộc nó có thay đổi hay không."),
           (r"Xét nam châm có nằm bên trong cuộn dây hay không", r"Vị trí không quyết định; điều quyết định là số đường sức có biến thiên không.")]),
  buoc("Câu c: kéo nam châm ra xa", "Kéo nam châm ra xa: đầu A là cực gì và (nhìn từ nam châm) dòng chạy chiều nào?",
       lua_chon=[(r"Cực Nam; dòng cùng chiều kim đồng hồ", True),
                 (r"Cực Bắc; dòng ngược chiều kim đồng hồ", r"Đó là kết quả khi nam châm lại gần; lúc ra xa số đường sức biến thiên theo chiều ngược lại."),
                 (r"Cực Nam; dòng ngược chiều kim đồng hồ", r"Nhìn vào đầu A thấy dòng ngược chiều kim đồng hồ thì A là cực Bắc, mâu thuẫn với cực Nam.")],
       loi=r"Hiểu định luật Lenz là &quot;dòng cảm ứng luôn đẩy nam châm ra&quot;.",
       ke=[(r"Xét số đường sức đang tăng hay giảm, dùng định luật Lenz rồi suy ra chiều dòng", True),
           (r"Giữ nguyên kết quả câu a vì vẫn là nam châm và cuộn dây đó", r"Chiều dòng cảm ứng phụ thuộc số đường sức đang tăng hay đang giảm, không chỉ phụ thuộc nam châm và cuộn dây."),
           (r"Lấy A luôn là cực cùng tên để đẩy nam châm", r"Định luật Lenz nói chống lại sự biến thiên, không nói lúc nào cũng đẩy.")]),
  buoc("Câu d: quay quanh trục dọc", "Quay nam châm quanh chính trục dọc của nó: có dòng điện cảm ứng không?",
       lua_chon=[(r"Không, vì đường sức phân bố đều quanh trục nên số đường sức qua cuộn dây không đổi", True),
                 (r"Có, vì nam châm đang chuyển động", r"Có chuyển động chưa đủ; điều kiện là số đường sức qua cuộn dây biến thiên."),
                 (r"Có, và là dòng xoay chiều vì nam châm quay", r"Máy phát cần các cực lần lượt đi qua cuộn dây; ở đây cực Bắc luôn hướng về đầu A.")],
       loi=r"Nghĩ rằng hễ nam châm chuyển động là có dòng cảm ứng.",
       ke=[(r"Xét khi nam châm quay, số đường sức xuyên qua tiết diện cuộn dây có thay đổi không", True),
           (r"Xét nam châm có chuyển động hay không", r"Chuyển động không phải điều kiện; nhiều chuyển động không làm số đường sức thay đổi."),
           (r"Xét nam châm quay nhanh hay chậm", r"Tốc độ chỉ quyết định độ lớn của dòng khi đã có biến thiên; trước hết phải xét có biến thiên không.")]),
  buoc("Câu e: nam châm điện", "Đóng K, giữ K đóng, rồi ngắt K: điện kế cho thấy gì?",
       lua_chon=[(r"Đóng K: dòng thoáng qua; giữ K: không có dòng; ngắt K: dòng thoáng qua ngược chiều lúc đóng", True),
                 (r"Đóng K: có dòng suốt thời gian giữ K; ngắt K: hết dòng", r"Giữ K đóng thì dòng qua nam châm điện không đổi, số đường sức qua cuộn dây không đổi."),
                 (r"Đóng K và ngắt K đều cho dòng thoáng qua cùng một chiều", r"Đóng K số đường sức tăng, ngắt K số đường sức giảm: hai biến thiên ngược nhau cho hai dòng ngược chiều.")],
       loi=r"Nghĩ nam châm điện đặt yên thì không thể sinh dòng cảm ứng.",
       ke=[(r"Xét dòng qua nam châm điện tăng, không đổi hay giảm ở từng giai đoạn", True),
           (r"Xét nam châm điện có dịch chuyển không", r"Nam châm điện đặt yên; từ trường của nó vẫn thay đổi được khi dòng qua nó thay đổi."),
           (r"Coi nam châm điện như nam châm vĩnh cửu đặt yên", r"Khác nam châm vĩnh cửu, từ trường nam châm điện xuất hiện khi đóng khoá và mất đi khi ngắt khoá.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>số cặp cực, vòng/phút, tần số</b> → $f=np$, đổi $n$ ra vòng/s, $p$ là số cặp cực.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Tốc độ quay của rôto thuỷ điện", "Rôto quay bao nhiêu vòng mỗi phút?", float(N_TD_PH), "vòng/phút", 1,
       loi=r"Tính $n=f/p$ theo vòng/s rồi ghi luôn đơn vị vòng/phút; hoặc lấy $p$ bằng số cực thay cho số cặp cực."),
  buoc("Tần số khi rôto chậm lại", "Tần số dòng điện lúc này là bao nhiêu Hz?", float(F_CHAM), "Hz", 0.1,
       loi=r"Nhân thẳng số vòng/phút với số cặp cực, quên đổi ra vòng/s.",
       ke=[(r"Đổi số vòng/phút ra vòng/s rồi nhân với số cặp cực", True),
           (r"Nhân thẳng số vòng/phút với số cặp cực", r"Đề cho vòng/phút; $f=np$ dùng $n$ theo vòng/s, để nguyên thì kết quả lớn gấp $60$ lần."),
           (r"Đổi ra vòng/s rồi chia cho số cặp cực", r"Tần số tăng theo số cặp cực vì mỗi vòng quay cho $p$ chu kì; phải nhân với $p$.")]),
  buoc("Tốc độ quay của núm", "Núm dinamô quay bao nhiêu vòng mỗi giây?", round(N_NUM, 1), "vòng/s", 0.5,
       loi=r"Chia tốc độ cho đường kính thay cho chu vi $\pi d$, hoặc để tốc độ theo km/h.",
       ke=[(r"Đổi $v$ ra m/s rồi chia cho chu vi núm $\pi d$", True),
           (r"Đổi $v$ ra m/s rồi chia cho đường kính $d$", r"Mỗi vòng núm lăn được một chu vi $\pi d$, không phải một đường kính."),
           (r"Lấy số vòng của núm bằng số vòng của bánh xe", r"Hai bên chỉ cùng tốc độ dài ở chỗ tiếp xúc; núm nhỏ hơn bánh rất nhiều nên quay nhanh hơn.")]),
  buoc("Tần số dòng điện của dinamô", "Dòng điện dinamô phát ra có tần số bao nhiêu Hz?", round(F_DYN), "Hz", 1.5,
       loi=r"Lấy $p$ bằng số cực của nam châm thay cho số cặp cực.",
       ke=[(r"Đếm số cặp cực của nam châm $4$ cực rồi dùng $f=np$", True),
           (r"Lấy $p=4$ rồi dùng $f=np$", r"$4$ là số cực; một cực Bắc với một cực Nam mới tạo thành một cặp."),
           (r"Lấy $f$ bằng số vòng quay mỗi giây của núm", r"Chỉ đúng khi nam châm có đúng một cặp cực; nam châm này có nhiều cực hơn.")]),
  buoc("Số lần đổi chiều mỗi giây", "Dòng điện lưới đổi chiều bao nhiêu lần mỗi giây?", DOI_CHIEU, "lần", 0,
       loi=r"Đồng nhất số chu kì mỗi giây với số lần đổi chiều mỗi giây.",
       ke=[(r"Đếm số lần đổi chiều trong một chu kì rồi nhân với số chu kì mỗi giây", True),
           (r"Lấy đúng bằng tần số", r"Tần số là số chu kì mỗi giây; trong một chu kì dòng đổi chiều nhiều hơn một lần."),
           (r"Lấy một nửa tần số", r"Mỗi chu kì có ít nhất một lần đổi chiều, nên số lần đổi chiều không thể ít hơn số chu kì.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>số vòng sơ cấp, thứ cấp, hiệu điện thế vào, ra</b> → $U_1/U_2=N_1/N_2$; dòng điện tính qua $U_1I_1=U_2I_2$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Số vòng cuộn thứ cấp", "Cuộn thứ cấp có bao nhiêu vòng?", float(N2), "vòng", 0,
       loi=r"Viết ngược tỉ số thành $U_1/U_2=N_2/N_1$, ra số vòng thứ cấp lớn hơn cả sơ cấp dù là máy hạ áp."),
  buoc("Dòng điện qua cuộn thứ cấp", "Cường độ dòng điện qua cuộn thứ cấp là bao nhiêu A?", float(I2), "A", 0.02,
       loi=r"Chỉ tính dòng qua một đèn, quên cuộn thứ cấp cấp dòng cho cả hai đèn song song.",
       ke=[(r"Cộng công suất hai đèn rồi chia cho $U_2$", True),
           (r"Chia công suất một đèn cho $U_2$", r"Đó là dòng qua một đèn; cuộn thứ cấp cấp dòng cho cả hai đèn song song."),
           (r"Chia tổng công suất cho $U_1$", r"Đó là cách tính dòng phía sơ cấp; phía thứ cấp dùng hiệu điện thế ra $U_2$.")]),
  buoc("Dòng điện qua cuộn sơ cấp (lí tưởng)", "Dòng điện qua cuộn sơ cấp khi máy lí tưởng là bao nhiêu A?", round(float(I1), 3), "A", 0.003,
       loi=r"Dùng $I_1/I_2=N_1/N_2$ (sai chiều tỉ lệ) nên ra dòng sơ cấp lớn hơn dòng thứ cấp.",
       ke=[(r"Dùng $U_1I_1=U_2I_2$", True),
           (r"Dùng $\dfrac{I_1}{I_2}=\dfrac{N_1}{N_2}$", r"Dòng điện tỉ lệ NGHỊCH với số vòng: máy hạ áp thì dòng phía thứ cấp lớn hơn."),
           (r"Lấy $I_1=I_2$ vì hai cuộn nối với nhau qua lõi", r"Hai cuộn cách điện với nhau, chỉ liên hệ qua từ trường trong lõi; dòng hai cuộn khác nhau.")]),
  buoc("Dòng sơ cấp khi hiệu suất 94 %", "Với hiệu suất 94 %, dòng điện qua cuộn sơ cấp là bao nhiêu A?", round(float(I1_H), 3), "A", 0.003,
       loi=r"Nhân dòng lí tưởng với $0{,}94$: máy có hao phí thì phải lấy từ nguồn nhiều hơn chứ không ít hơn.",
       ke=[(r"Tính $P_1=\dfrac{P_2}{H_{\text{BA}}}$ rồi $I_1'=\dfrac{P_1}{U_1}$", True),
           (r"Tính $P_1=H_{\text{BA}}\cdot P_2$ rồi $I_1'=\dfrac{P_1}{U_1}$", r"$H_{\text{BA}}=P_2/P_1$ nên $P_1=P_2/H_{\text{BA}}$; nhân với $H_{\text{BA}}$ thì nguồn cấp ít hơn tải dùng, vô lí."),
           (r"Tính $I_1'=\dfrac{P_2}{H_{\text{BA}}\,U_2}$", r"Chia cho $U_2$ là tính dòng phía thứ cấp; cuộn sơ cấp nối với $U_1=220\ \text{V}$.")]),
  buoc("Vị trí đầu ra 6 V", "Phải rút đầu dây ở vòng thứ bao nhiêu của cuộn thứ cấp?", float(N_6V), "vòng", 0,
       loi=r"Lấy một nửa số vòng của cuộn sơ cấp vì $6\ \text{V}$ bằng nửa $12\ \text{V}$.",
       ke=[(r"Số vòng tỉ lệ với hiệu điện thế: $\dfrac{N_x}{N_1}=\dfrac{6}{U_1}$", True),
           (r"Lấy $N_x=\dfrac{N_1}{2}$ vì $6\ \text{V}$ bằng nửa $12\ \text{V}$", r"Nửa của $12\ \text{V}$ ứng với nửa cuộn THỨ CẤP; cuộn sơ cấp ứng với $220\ \text{V}$."),
           (r"Lấy $N_x=N_2\cdot\dfrac{12}{6}$", r"Hiệu điện thế ra tỉ lệ THUẬN với số vòng: dùng ít vòng hơn thì hiệu điện thế nhỏ hơn.")]),
  buoc("Lắp nhầm cuộn", "Hiệu điện thế giữa hai đầu cuộn 1650 vòng khi lắp nhầm là bao nhiêu V?", round(float(U_NHAM)), "V", 5,
       loi=r"Vẫn coi cuộn $1650$ vòng là sơ cấp khi lập tỉ số, nên tưởng máy vẫn hạ áp như cũ.",
       ke=[(r"Coi cuộn đang nối nguồn là sơ cấp rồi lập lại tỉ số", True),
           (r"Giữ tỉ số cũ $\dfrac{U_1}{U_2}=\dfrac{1650}{N_2}$ với $U_1=220\ \text{V}$", r"Cuộn nối nguồn luôn là sơ cấp; đổi cuộn nối nguồn thì tỉ số đảo lại."),
           (r"Kết luận máy không hoạt động vì nối ngược", r"Máy biến áp làm việc theo cả hai chiều; nối ngược thì thành máy tăng áp.")]),
  buoc("Kiểm tra")]),
]


def kiem_so():
    F = Fr
    # D2
    assert N_TD_PH == 500 and abs(float(N_TD) - 8.333) < 1e-3
    assert F_CHAM == 48
    assert V_XE == 5 and abs(N_NUM - 79.577) < 1e-3 and abs(F_DYN - 159.15) < 0.01 and round(F_DYN) == 159
    assert DOI_CHIEU == 100
    # cách sai D2 cho số khác đáp án
    assert abs(float(N_TD) - 500) > 1 and float(F(50, 12) * 60) != 500           # để vòng/s; dùng p = 12
    assert N_CHAM * P_TD != 48 and abs(N_CHAM / 60 / P_TD - 48) > 0.1           # nhân 480·6; chia cho p
    assert abs(80 - N_NUM) < 0.5 and abs(5 / D_NUM - 79.6) > 1 and abs(18 / (math.pi * D_NUM) - 79.6) > 1   # chia d; để km/h
    assert abs(N_NUM * 4 - 159) > 2 and abs(N_NUM - 159) > 2                    # p = 4; f = n
    assert F_LUOI != 100 and F_LUOI / 2 != 100
    # D3
    assert N2 == 90 and P2 == 48 and I2 == 4 and abs(float(I1) - 0.21818) < 1e-4
    assert abs(float(I1_H) - 0.23211) < 1e-4 and abs(float(P2 / H_BA) - 51.06) < 0.01
    assert N_6V == 45 and N2 * F(6, 12) == 45 and abs(float(U_NHAM) - 4033.3) < 0.1
    assert abs(float(I2 / I1) - float(F(U1, U2))) < 1e-9                            # dòng tăng bao nhiêu lần
    # cách sai D3 cho số khác đáp án
    assert N1 * F(U1, U2) != 90                                                    # tỉ số ngược
    assert F(P_DEN, U2) != 4 and F(P2, U1) != 4                                    # một đèn; chia U1
    assert abs(float(I2 * F(N1) / N2) - 0.218) > 0.01 and float(I2) != 0.218      # tỉ lệ thuận; I1 = I2
    assert abs(float(I1 * H_BA) - 0.232) > 0.005 and abs(48 / (220 * 0.94) - 0.232) < 0.001
    assert abs(float(F(P2) / (H_BA * U2)) - 0.232) > 1                             # chia cho U2
    assert F(N1, 2) != 45 and N2 * F(12, 6) != 45                                  # nửa cuộn sơ cấp; tỉ lệ nghịch
    assert abs(220 * float(N2) / N1 - 4033) > 100                                  # giữ tỉ số cũ ra 12 V
    print("kiểm số liệu D1–D3 (bài 152): đạt")
