"""Hình cho bài tập mẫu Bài 19 "Thế năng điện" (Vật lí 11), lesson_id 38.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mô phỏng chạy hạt MẪU với số liệu khác đề (không lộ đáp số), quỹ đạo tính từ công thức (mẫu cách đều thời gian,
nội suy tuyến tính). Quy ước: hai bản có dấu +/− ghi ngay trên bản; đường sức nét đứt, đầu V 30°.
Dạng 1, 2: chấm rỗng = hình chiếu của hạt lên đường sức. Dạng 3, 4: thanh W (thế năng, mốc ở bản âm) và K (động năng)."""
import math, os, re as _re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
MINUS = "−"


def rich(s, size=13):
    """`v_0` → v với chỉ số dưới 0 (tspan dy, không dùng ký tự Unicode chỉ số)."""
    parts = _re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
    return out


def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)


def plates(x0, x1, yt, yb, top_pos=True, step=30):
    """Hai bản phẳng nằm ngang; dấu +/− ghi ngay trên bản (phía ngoài)."""
    b = seg(x0, yt, x1, yt, "currentColor", 5) + seg(x0, yb, x1, yb, "currentColor", 5)
    st, sb = ("+", MINUS) if top_pos else (MINUS, "+")
    for x in range(int(x0 + 15), int(x1 - 6), step):
        b += txt(x, yt - 9, st, "currentColor", 15, "middle") + txt(x, yb + 22, sb, "currentColor", 15, "middle")
    return b


def elines_v(xs, yt, yb, down=True):
    """Đường sức thẳng đứng nét đứt, đầu V: xuống (bản trên dương) hoặc lên (bản trên âm)."""
    out = ""
    for x in xs:
        if down:
            out += field_line(x, yt + 8, x, yb - 8, "currentColor", 1.6, "6 4", 9)
        else:
            out += field_line(x, yb - 8, x, yt + 8, "currentColor", 1.6, "6 4", 9)
    return f'<g opacity=".5">{out}</g>'


def elines_h(ys, x0, x1):
    out = "".join(field_line(x0, y, x1, y, "currentColor", 1.6, "6 4", 9) for y in ys)
    return f'<g opacity=".45">{out}</g>'


def mover(pts, sec, r=5, c=GRN, fill=None):
    """Hạt chạy dọc pts (mẫu cách đều thời gian); một lần khi bấm, dừng ở khung cuối."""
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    f = fill or c
    return (f'<circle cx="{xs[0]:.1f}" cy="{ys[0]:.1f}" r="{r}" fill="{f}" stroke="currentColor" stroke-width="1.5">'
            f'{smil("cx", xs, sec)}{smil("cy", ys, sec)}</circle>')


def shadow(pts, y_line, sec, r=5):
    """Hình chiếu của hạt xuống đường sức nằm ngang y = y_line: chấm rỗng + đoạn thẳng đứng nối (chạy cùng hạt)."""
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    ln = (f'<line x1="{xs[0]:.1f}" y1="{ys[0]:.1f}" x2="{xs[0]:.1f}" y2="{y_line}" stroke="currentColor" stroke-width="1.2" stroke-dasharray="3 3" opacity=".6">'
          f'{smil("x1", xs, sec)}{smil("x2", xs, sec)}{smil("y1", ys, sec)}</line>')
    dt = (f'<circle cx="{xs[0]:.1f}" cy="{y_line}" r="{r}" fill="none" stroke="currentColor" stroke-width="2">{smil("cx", xs, sec)}</circle>')
    return ln + dt


def bar(x, y_bot, h_max, fracs, sec, c, label):
    """Thanh cột cao h_max·frac (frac theo từng mẫu), đáy ở y_bot; khung ngoài + nhãn dưới."""
    ys = [y_bot - h_max * f for f in fracs]; hs = [h_max * f for f in fracs]
    return (f'<rect x="{x}" y="{y_bot - h_max}" width="26" height="{h_max}" fill="none" stroke="currentColor" stroke-width="1.5" opacity=".6"/>'
            f'<rect x="{x}" y="{ys[0]:.1f}" width="26" height="{hs[0]:.1f}" fill="{c}" opacity=".85">{smil("y", ys, sec)}{smil("height", hs, sec)}</rect>'
            + txt(x + 13, y_bot + 20, label, c, 14, "middle"))


def charge(x, y, sign, r=8):
    s = "+" if sign > 0 else MINUS
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="currentColor" stroke-width="2"/>'
            + txt(x, y + 5, s, "currentColor", 14, "middle"))


def dim_v(x, y1, y2, label, lx, ly, anchor="start", c="o"):
    return dim("", c, x, y1, x, y2, label, lx, ly, anchor)


# ───────────── Dạng 1 · A = qEd: hình chiếu có dấu của MN lên đường sức ─────────────
def d1(kk):
    if kk == 0:
        N = 40
        pts = [(70 + 220 * i / N, 138 - 76 * i / N) for i in range(N + 1)]      # hạt mẫu đi xiên lên, sang phải
        b = elines_h((36, 90, 138), 20, 395) + txt(398, 41, "E", "currentColor", 15) + seg(60, 176, 310, 176, "currentColor", 1.2, "3 3", .5)
        b += shadow(pts, 176, 3.0) + mover(pts, 3.0)
        b += txt(20, 204, "● hạt mẫu q_0 &gt; 0 (khác đề)   ○ hình chiếu lên đường sức", GRN, 12, "start", "600")
        return fig("d1-0", "0 0 420 218", "Điện trường đều có đường sức nằm ngang hướng sang phải; một hạt mẫu đi xiên lên, chấm rỗng bên dưới là hình chiếu của hạt lên đường sức",
                   b, "Mô phỏng: hạt mẫu (không phải electron của đề, góc đi khác) đi xiên; chấm rỗng là hình chiếu của hạt lên đường sức. Chạy chậm hơn thật. " + NOTE)
    mx, my = 250, 150
    L = 105
    nx, ny = mx + L * math.cos(math.radians(120)), my - L * math.sin(math.radians(120))
    b = elines_h((40, 100, 150, 190), 20, 395) + txt(398, 45, "E", "currentColor", 15)
    b += arrow("", "r", mx, my, round(nx, 1), round(ny, 1), 2.6) + dot(mx, my, 4.5) + dot(nx, ny, 4.5)
    b += arc(mx, my, 30, 0, 120, ORG, 2) + txt(mx + 24, my - 34, "120°", ORG, 13)
    b += txt(mx + 8, my + 24, "M", "currentColor", 14) + txt(nx - 10, ny + 4, "N", "currentColor", 14, "end")
    b += txt((mx + nx) / 2 - 14, 128, "MN = 8,0 cm", RED, 13, "end")
    b += txt(20, 24, "E = 5000 V/m", "currentColor", 13) + txt(20, 212, "electron: q = −1,6·10⁻¹⁹ C", ORG, 13)
    return fig("d1-2", "0 0 420 224", "Điện trường đều nằm ngang hướng sang phải; electron đi từ M đến N lên trên chếch sang trái, đoạn MN dài 8,0 cm hợp với đường sức góc 120 độ",
               b, "Dữ kiện: đường sức nằm ngang sang phải; MN hợp với chiều đường sức góc 120° (đường đi thẳng). " + NOTE)


# ───────────── Dạng 2 · công không phụ thuộc đường đi ─────────────
def d2(kk):
    if kk == 0:
        N = 48
        pts = []
        for i in range(N + 1):
            u = i / N
            pts.append((60 + 250 * u, 150 - 80 * u - 34 * math.sin(2 * math.pi * u)))   # đường cong lượn, x tăng dần
        b = elines_h((30, 78, 126), 20, 395) + txt(398, 35, "E", "currentColor", 15) + seg(50, 180, 330, 180, "currentColor", 1.2, "3 3", .5)
        b += poly(pts, GRN, 1.6, "5 4", .5) + shadow(pts, 180, 3.5) + mover(pts, 3.5)
        b += txt(20, 208, "● hạt mẫu đi theo đường cong   ○ hình chiếu lên đường sức", GRN, 12, "start", "600")
        return fig("d2-0", "0 0 420 222", "Điện trường đều có đường sức nằm ngang hướng sang phải; một hạt mẫu đi theo đường cong lượn từ trái sang phải, chấm rỗng bên dưới là hình chiếu của hạt lên đường sức",
                   b, "Mô phỏng: hạt mẫu (số liệu khác đề) đi theo một đường cong; chấm rỗng là hình chiếu của hạt lên đường sức. Chạy chậm hơn thật. " + NOTE)
    ax, ay = 46, 168
    bx, by = 150, 168
    cx_, cy_ = bx + 60 * math.cos(math.radians(60)) * 1.4, by - 60 * 1.4 * math.sin(math.radians(60))
    b = elines_h((36, 112, 206), 20, 395) + txt(398, 41, "E", "currentColor", 15)
    b += arrow("", "b", ax, ay, bx, by, 2.4) + arrow("", "r", bx, by, round(cx_, 1), round(cy_, 1), 2.4)
    dxp, dyp = cx_, cy_ + 42
    b += f'<path d="M{ax},{ay} C{ax - 10},{ay - 80} {bx - 10},{cy_ - 40} {cx_:.1f},{cy_:.1f} S{dxp + 20:.1f},{dyp - 20:.1f} {dxp:.1f},{dyp:.1f}" fill="none" stroke="{GRN}" stroke-width="2" stroke-dasharray="6 4"/>'
    b += seg(cx_, cy_, dxp, dyp, "currentColor", 1.5, "2 3", .8) + txt(dxp + 10, dyp + 4, "D", "currentColor", 14)
    b += dot(ax, ay, 4.5) + dot(bx, by, 4.5) + dot(cx_, cy_, 4.5) + dot(dxp, dyp, 4.5)
    b += txt(ax - 4, ay + 22, "A", "currentColor", 14, "middle") + txt(bx, by + 22, "B", "currentColor", 14, "middle") + txt(cx_ + 12, cy_ - 8, "C", "currentColor", 14)
    b += arc(bx, by, 26, 0, 60, ORG, 2) + txt(bx + 30, by - 10, "60°", ORG, 13)
    b += txt((ax + bx) / 2, ay + 22, "6,0 cm", BLUE, 13, "middle") + txt(bx + 1, (by + cy_) / 2 + 8, "BC = 10 cm", RED, 13, "end")
    b += txt(262, 74, "đường cong", GRN, 13) + txt(262, 92, "dài 25 cm", GRN, 13)
    b += txt(270, 24, "E = 3000 V/m", "currentColor", 13) + txt(270, 170, "q = −2,0 µC", ORG, 13)
    return fig("d2-2", "0 0 420 224", "Điện trường đều nằm ngang hướng sang phải; đoạn AB dọc đường sức dài 6,0 cm, đoạn BC dài 10 cm hợp với đường sức góc 60 độ, đường cong nét đứt dài 25 cm nối A với D nằm dưới C",
               b, "Dữ kiện: A→B→C (xanh dương, đỏ) và đường cong nét đứt từ A tới D; CD vuông góc đường sức. " + NOTE)


# ───────────── Dạng 3 · thế năng, mốc, A = W_M − W_N ─────────────
def d3(kk):
    x0, x1, yt, yb = 40, 270, 44, 184
    if kk == 0:
        N = 40
        ys = [yb - 24 - (yb - yt - 48) * (i / N) for i in range(N + 1)]            # hạt mẫu q>0 đi lên về phía bản âm (trên)
        fr = [(y - yt) / (yb - yt) for y in ys]                                    # d tới bản âm / khoảng cách hai bản
        b = plates(x0, x1, yt, yb, False) + elines_v(range(80, 262, 45), yt, yb, False)
        b += mover([(150, y) for y in ys], 3.0) + bar(330, 176, 120, fr, 3.0, ORG, "W")
        b += txt(300, 214, "mốc ở bản âm", "currentColor", 12, "start", "600") + txt(20, 232, "● hạt mẫu q_0 &gt; 0 (khác hạt bụi của đề)", GRN, 12, "start", "600")
        return fig("d3-0", "0 0 420 244", "Hai bản phẳng nằm ngang, bản trên âm, bản dưới dương; hạt mẫu mang điện dương đi lên về phía bản âm, thanh W bên phải thấp dần",
                   b, "Mô phỏng: hạt mẫu mang điện dương (khác hạt bụi của đề) đi về phía bản âm; thanh W là thế năng của nó với mốc ở bản âm. Chạy chậm hơn thật. " + NOTE)
    mx, my, nx, ny = 130, 74, 205, 130
    b = plates(x0, x1, yt, yb, False) + elines_v((175,), yt, yb, False) + txt(12, 24, "bản trên (−)", "currentColor", 12, "start", "600") + txt(12, 236, "bản dưới (+)", "currentColor", 12, "start", "600")
    b += f'<path d="M{mx},{my} C{mx + 70},{my - 10} {nx - 80},{ny + 10} {nx},{ny}" fill="none" stroke="{GRN}" stroke-width="2" stroke-dasharray="6 4"/>'
    b += dot(mx, my, 4.5) + dot(nx, ny, 4.5) + txt(mx - 10, my - 8, "M", "currentColor", 14, "end") + txt(nx + 10, ny + 4, "N", "currentColor", 14)
    b += dim_v(mx - 40, yt, my, "1,0 cm", mx - 46, (yt + my) / 2 + 4, "end", "o")
    b += txt(nx + 12, ny + 18, "?", ORG, 14)
    b += txt(290, 40, "q = −5,0 nC", ORG, 13) + txt(290, 66, "mốc: bản trên", "currentColor", 12, "start", "600") + txt(290, 92, "W_M = −2,0·10⁻⁷ J", "currentColor", 13) + txt(290, 118, "A_MN = +6,0·10⁻⁷ J", RED, 13)
    b += txt(290, 150, "hai bản cách", "currentColor", 12, "start", "600") + txt(290, 166, "nhau 5,0 cm", "currentColor", 12, "start", "600")
    return fig("d3-2", "0 0 420 246", "Hai bản phẳng nằm ngang cách nhau 5,0 cm, bản trên âm, bản dưới dương; điểm M cách bản trên 1,0 cm, điểm N nằm dưới M, hạt bụi đi theo đường nét đứt từ M tới N",
               b, "Dữ kiện: hai bản, điểm M, điểm N (chưa biết vị trí), thế năng tại M và công của lực điện. " + NOTE)


# ───────────── Dạng 4 · từ nghỉ, chỉ có lực điện: thế năng giảm = động năng tăng ─────────────
def d4(kk):
    x0, x1, yt, yb = 40, 270, 44, 184
    if kk == 0:
        N = 40
        ys = [yt + 14 + (yb - yt - 28) * (i / N) ** 2 for i in range(N + 1)]       # từ nghỉ: quãng đường ∝ t²
        w = [(yb - y) / (yb - yt - 14) for y in ys]                                # W ∝ khoảng cách tới bản âm
        k = [1 - v for v in w]
        b = plates(x0, x1, yt, yb, True) + elines_v(range(80, 262, 45), yt, yb, True)
        b += mover([(150, y) for y in ys], 3.0) + bar(300, 176, 120, w, 3.0, ORG, "W") + bar(350, 176, 120, k, 3.0, BLUE, "K")
        b += txt(20, 232, "● hạt mẫu q_0 &gt; 0, thả từ nghỉ (khác đề)", GRN, 12, "start", "600")
        return fig("d4-0", "0 0 420 244", "Hai bản phẳng nằm ngang, bản trên dương, bản dưới âm; hạt mẫu mang điện dương thả từ nghỉ rơi dần về bản âm, thanh W thấp dần, thanh K cao dần",
                   b, "Mô phỏng: hạt mẫu thả từ nghỉ (khác hạt của đề); W là thế năng điện của hạt mẫu, K là động năng. Chạy chậm hơn thật. " + NOTE)
    mx, my, px, py = 150, 62, 150, 130
    b = plates(x0, x1, yt, yb, True) + elines_v((190,), yt, yb, True) + txt(12, 24, "bản trên (+)", "currentColor", 12, "start", "600") + txt(12, 236, "bản dưới (−)", "currentColor", 12, "start", "600")
    b += dot(mx, my, 5) + dot(px, py, 5) + txt(mx + 12, my + 4, "M", "currentColor", 14) + txt(px + 12, py + 4, "P", "currentColor", 14)
    b += dim_v(mx - 50, my, yb, "5,0 cm", mx - 56, (my + yb) / 2 + 4, "end", "o") + dim_v(px + 70, py, yb, "2,0 cm", px + 76, (py + yb) / 2 + 4, "start", "b")
    b += txt(300, 30, "q = +4,0 nC", ORG, 13) + txt(296, 52, "m = 2,0·10⁻⁸ kg", ORG, 13) + txt(296, 84, "thả từ nghỉ ở M", "currentColor", 12, "start", "600")
    b += txt(296, 150, "tới bản âm:", "currentColor", 12, "start", "600") + txt(296, 168, "v = 10 m/s", RED, 13)
    return fig("d4-2", "0 0 420 246", "Hai bản phẳng nằm ngang, bản trên dương, bản dưới âm; hạt bụi thả từ nghỉ ở M cách bản âm 5,0 cm, điểm P cách bản âm 2,0 cm; tới bản âm hạt có tốc độ 10 mét trên giây",
               b, "Dữ kiện: hạt thả từ nghỉ ở M, đi thẳng xuống theo đường sức. " + NOTE)
