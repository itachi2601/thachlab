"""Hình cho bài tập mẫu Bài 18 "Điện trường đều" (Vật lí 11), lesson_id 37.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mô phỏng KHÔNG chạy đúng số liệu của đề (tránh lộ đáp số): chạy hạt MẪU, số liệu khác đề, ghi rõ trong chú thích;
quỹ đạo tính từ công thức (mẫu cách đều thời gian, nội suy tuyến tính). Dạng 1, 2 dùng hạt mẫu mang điện trái dấu với hạt
của đề để không lộ chiều lực. Vectơ vẽ bằng vec_luc (độ dài = k·độ lớn, đầu V 30°, không dùng marker).
Quy ước: hình vẽ phẳng; bản trên/dưới mang dấu +/− ghi ngay trên bản; đường sức nét đứt, đầu V."""
import math, os, re as _re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
MINUS = "−"
E_CH, M_E = 1.6e-19, 9.1e-31


def rich(s, size=13):
    """`F_ms` → F với chỉ số dưới ms; `v_0` → v₀ dạng chỉ số dưới."""
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
    """Hai bản phẳng nằm ngang; dấu +/− ghi trên bản (trên bản trên phía ngoài, dưới bản dưới phía ngoài)."""
    b = seg(x0, yt, x1, yt, "currentColor", 5) + seg(x0, yb, x1, yb, "currentColor", 5)
    st, sb = ("+", MINUS) if top_pos else (MINUS, "+")
    for x in range(int(x0 + 15), int(x1 - 6), step):
        b += txt(x, yt - 9, st, "currentColor", 15, "middle") + txt(x, yb + 22, sb, "currentColor", 15, "middle")
    return b


def elines_v(xs, yt, yb, top_pos=True):
    """Đường sức thẳng đứng giữa hai bản: nét đứt, đầu V, từ bản dương sang bản âm."""
    out = ""
    for x in xs:
        if top_pos:
            out += field_line(x, yt + 8, x, yb - 8, "currentColor", 1.6, "6 4", 9)
        else:
            out += field_line(x, yb - 8, x, yt + 8, "currentColor", 1.6, "6 4", 9)
    return f'<g opacity=".5">{out}</g>'


def mover(pts, sec, r=5, c=GRN):
    """Hạt chạy dọc pts (mẫu cách đều thời gian); một lần khi bấm, dừng ở khung cuối."""
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return (f'<circle cx="{xs[0]:.1f}" cy="{ys[0]:.1f}" r="{r}" fill="{c}" stroke="currentColor" stroke-width="1.5">'
            f'{smil("cx", xs, sec)}{smil("cy", ys, sec)}</circle>')


def traj_plates(a, v0, L, x_total, N=60):
    """Hạt bay vào bản tại x=0 (m) với v0, gia tốc a (m/s², dọc trục y) trong 0 ≤ x ≤ L; ngoài bản đi thẳng tới x_total.
    Trả [(x, y)] (m) tại N+1 thời điểm cách đều. y cùng chiều gia tốc."""
    tL = L / v0; t_tot = x_total / v0; out = []
    for i in range(N + 1):
        t = t_tot * i / N
        y = 0.5 * a * t * t if t <= tL else 0.5 * a * tL * tL + a * tL * (t - tL)
        out.append((v0 * t, y))
    return out


def electron(x, y, r=7, label=MINUS):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="currentColor" stroke-width="2"/>'
            + txt(x, y + 5, label, "currentColor", 14, "middle"))


def dim_h(x1, x2, y, label, lx=None, ly=None, c="b"):
    lx = (x1 + x2) / 2 if lx is None else lx
    return dim("", c, x1, y, x2, y, "", 0, 0) + txt(lx, (y + 16) if ly is None else ly, label, {"b": BLUE, "o": ORG, "r": RED, "g": GRN}[c], 13, "middle")


def dim_v(x, y1, y2, label, lx, ly, anchor="start", c="o"):
    return dim("", c, x, y1, x, y2, label, lx, ly, anchor)


# ───────────── Dạng 1 · hai bản, E = U/d, lực điện theo dấu q ─────────────
def d1(kk):
    x0, x1, yt, yb = 40, 300, 44, 156
    yc = (yt + yb) / 2
    b = defs("d1") + plates(x0, x1, yt, yb, True) + elines_v(range(70, 290, 40), yt, yb, True)
    b += dim_v(332, yt, yb, "d = 8,0 mm", 340, yc + 4) + txt(340, yc + 24, "U = 240 V", "currentColor", 13)
    if kk == 0:
        # hạt MẪU mang điện DƯƠNG (khác hạt trong đề), thả từ nghỉ ở giữa: s ∝ t² (a không đổi); bay xuống phía bản âm
        N = 40; pts = [(170, yc + 40 * (i / N) ** 2) for i in range(N + 1)]
        b += mover(pts, 3.0) + txt(40, 206, "● hạt mẫu q₀ > 0, thả từ nghỉ (khác hạt trong đề)", GRN, 12, "start", "600")
        return fig("d1-0", "0 0 420 222", "Hai bản kim loại song song nằm ngang, bản trên mang dấu cộng, bản dưới mang dấu trừ; một hạt mẫu mang điện dương được thả giữa hai bản",
                   b, "Mô phỏng: hạt mẫu mang điện dương (không phải hạt trong đề) được thả từ nghỉ giữa hai bản; chạy chậm hơn thật. " + NOTE)
    b += electron(170, yc) + txt(184, yc - 10, "q = −2,5 nC", "currentColor", 13)
    b += txt(40, 206, "Cần tìm: E, F, chiều của lực", ORG, 13)
    return fig("d1-2", "0 0 420 222", "Hai bản song song cách nhau 8,0 mm, hiệu điện thế 240 vôn, bản trên dương; hạt bụi mang điện âm ở giữa", b, "Dữ kiện: hai bản, U, d và hạt cần xét. " + NOTE)


# ───────────── Dạng 2 · bay dọc đường sức: a = |q|E/m, chậm dần rồi quay lại ─────────────
def d2(kk):
    ys = (56, 100, 144); yc = 100
    b = defs("d2")
    for y in ys:
        b += f'<g opacity=".5">{field_line(24, y, 200, y, "currentColor", 1.6, "6 4", 9)}{field_line(200, y, 380, y, "currentColor", 1.6, "6 4", 9)}</g>'
    b += txt(392, ys[0] + 5, "E", "currentColor", 15, "start")
    b += txt(60, yc + 24, "O (điểm vào)", "currentColor", 12, "middle", "600")
    if kk == 0:
        b += dot(60, yc, 3.5, "currentColor")
        # hạt MẪU = proton bay cùng chiều E (nhanh dần), số liệu khác đề: s(u) = 310·(0,25u + 0,75u²)
        N = 40; pts = [(60 + 310 * (0.25 * (i / N) + 0.75 * (i / N) ** 2), yc) for i in range(N + 1)]
        b += mover(pts, 3.0) + txt(24, 184, "● proton mẫu bay cùng chiều E (khác electron trong đề)", GRN, 12, "start", "600")
        return fig("d2-0", "0 0 420 198", "Điện trường đều có đường sức nằm ngang hướng sang phải; một proton mẫu bay dọc đường sức từ điểm O",
                   b, "Mô phỏng: proton mẫu (không phải electron của đề, số liệu khác) bay dọc đường sức; chạy chậm hơn thật. " + NOTE)
    v, tip = vec_luc("r", 74, yc, 1, 0, 8.0, 7, 3)
    b += electron(60, yc, 8) + v + txt(76, yc - 14, "v_0 = 8,0·10⁶ m/s", RED, 12, "start")
    b += txt(24, 28, "E = 1820 V/m", "currentColor", 13) + txt(24, 184, "Cần tìm: a, s, t", ORG, 13)
    return fig("d2-2", "0 0 420 198", "Electron ở điểm O bay cùng chiều đường sức với vận tốc 8,0 nhân 10 mũ 6 mét trên giây trong điện trường 1820 vôn trên mét", b,
               "Dữ kiện: electron ở O, vận tốc đầu cùng chiều đường sức. " + NOTE)


# ───────────── Dạng 3 · vào giữa hai bản: có ra khỏi bản không? ─────────────
S3 = 6.0           # px/mm: vẽ đúng tỉ lệ kích thước hai bản
L3, D3_ = 45.0, 10.0   # mm


def d3(kk):
    yc = 100; hd = S3 * D3_ / 2
    yt, yb = yc - hd, yc + hd
    if kk == 0:
        x0 = 60; x1 = x0 + S3 * L3
        a_s = 3.2e14; v0 = 1.0e7                  # electron MẪU: gia tốc khác đề, bản trên DƯƠNG → lệch lên
        tr = traj_plates(a_s, v0, L3 * 1e-3, (400 - x0) / S3 * 1e-3)
        pts = [(x0 + S3 * x * 1e3, yc - S3 * y * 1e3) for x, y in tr]
        b = defs("d30") + plates(x0, x1, yt, yb, True) + elines_v(range(int(x0 + 30), int(x1 - 10), 45), yt, yb, True)
        b += poly(pts, GRN, 1.8, "6 4", .55) + mover(pts, 4.0, 4.5)
        b += dim_h(x0, x1, yb + 38, "L = 4,5 cm") + dim_v(x0 - 16, yt, yb, "d", x0 - 40, yc + 4, "start")
        b += txt(30, 200, "● electron mẫu (khác đề: bản trên +, U khác) bay vào mép bản", GRN, 12, "start", "600")
        return fig("d3-0", "0 0 420 212", "Electron bay vào mép hai bản phẳng nằm ngang, bản trên mang dấu cộng; quỹ đạo mẫu cong dần về phía bản trên",
                   b, "Mô phỏng: electron mẫu, vẽ đúng tỉ lệ kích thước hai bản; số liệu khác đề (bản trên dương, U khác); chạy chậm hàng tỉ lần.")
    x0 = 118; x1 = x0 + S3 * L3
    b = defs("d32") + plates(x0, x1, yt, yb, False) + elines_v(range(int(x0 + 30), int(x1 - 10), 45), yt, yb, False)
    v, tip = vec_luc("r", 30, yc, 1, 0, 10.0, 4, 3)
    b += electron(16, yc, 7) + v + txt(8, yc + 26, "v_0 = 1,0·10⁷ m/s", RED, 11, "start")
    b += dim_h(x0, x1, yb + 38, "L") + dim_v(x1 + 12, yt, yb, "d", x1 + 20, yc + 4)
    b += txt(8, 20, "L = 4,5 cm", "currentColor", 12) + txt(8, 38, "d = 1,0 cm", "currentColor", 12) + txt(8, 56, "U = 36,4 V", "currentColor", 12)
    b += txt(8, 74, "vào chính giữa", "currentColor", 12)
    return fig("d3-2", "0 0 420 196", "Electron bay vào chính giữa hai bản nằm ngang dài 4,5 cm cách nhau 1,0 cm, bản dưới mang điện dương", b,
               "Dữ kiện: kích thước hai bản vẽ đúng tỉ lệ; electron vào đúng chính giữa. ")


# ───────────── Dạng 4 · giọt mực: ra khỏi bản đi thẳng tới màn ─────────────
S4 = 10.0         # px/mm
L4, D4, DW4 = 10.0, 4.0, 20.0   # mm: dài bản, khoảng cách bản, quãng tới màn


def d4(kk):
    yc = 128; hd = S4 * D4 / 2
    yt, yb = yc - hd, yc + hd
    x0 = 60; x1 = x0 + S4 * L4; xs = x1 + S4 * DW4
    scr = seg(xs, 36, xs, 220, "currentColor", 3) + txt(xs + 6, 54, "màn", "currentColor", 13) + txt(xs + 6, 74, "Y = ?", ORG, 13)
    centre = seg(x1, yc, xs, yc, "currentColor", 1.3, "4 4", .6)
    b = defs("d4") + plates(x0, x1, yt, yb, True, 25) + elines_v(range(int(x0 + 20), int(x1 - 10), 30), yt, yb, True) + centre + scr
    if kk == 0:
        U_s, v0 = 1000.0, 20.0                      # giọt mực MẪU: U khác đề; âm, bản trên dương → lệch lên
        a_s = 2.0e-12 * U_s / (1.0e-10 * 4.0e-3)
        tr = traj_plates(a_s, v0, L4 * 1e-3, (L4 + DW4) * 1e-3)
        pts = [(x0 + S4 * x * 1e3, yc - S4 * y * 1e3) for x, y in tr]
        b += poly(pts, GRN, 1.8, "6 4", .55) + mover(pts, 4.0, 4.5)
        b += dim_h(x0, x1, yb + 40, "L") + dim_h(x1, xs, yb + 40, "D = 2,0 cm")
        b += txt(20, 238, "● giọt mực mẫu (khác đề: U khác) bay vào mép bản", GRN, 12, "start", "600")
        return fig("d4-0", "0 0 420 252", "Giọt mực tích điện âm bay vào hai bản nằm ngang, bản trên mang dấu cộng, rồi bay thẳng tới màn đặt cách mép ra 2,0 cm",
                   b, "Mô phỏng: giọt mực mẫu, vẽ đúng tỉ lệ kích thước hai bản và quãng tới màn; U khác đề; chạy chậm hàng nghìn lần.")
    v, tip = vec_luc("r", 30, yc, 1, 0, 20.0, 1.5, 3)
    b += electron(16, yc, 7) + v + txt(6, yc + 28, "v_0 = 20 m/s", RED, 11, "start")
    b += dim_h(x0, x1, yb + 40, "L") + dim_h(x1, xs, yb + 40, "D")
    b += txt(8, 18, "L = 1,0 cm", "currentColor", 12) + txt(8, 36, "d = 4,0 mm", "currentColor", 12) + txt(8, 54, "U = 1600 V", "currentColor", 12)
    b += txt(8, 72, "D = 2,0 cm", "currentColor", 12)
    return fig("d4-2", "0 0 420 252", "Giọt mực tích điện âm bay vào chính giữa hai bản dài 1,0 cm cách nhau 4,0 mm với vận tốc 20 mét trên giây, màn cách mép ra 2,0 cm", b,
               "Dữ kiện: kích thước hai bản và quãng tới màn vẽ đúng tỉ lệ; đường nét đứt là đường bay ban đầu.")


# ───────────── Dạng 5 · bài ngược: U lớn nhất để electron còn ra khỏi bản ─────────────
S5 = 6.0          # px/mm
L5, D5_ = 40.0, 20.0   # mm


def d5(kk):
    yc = 110; hd = S5 * D5_ / 2
    yt, yb = yc - hd, yc + hd
    if kk == 0:
        x0 = 60; x1 = x0 + S5 * L5
        a_s = 2.2e15; v0 = 1.6e7                  # electron MẪU: gia tốc khác đề (ra khỏi bản), bản trên dương → lệch lên
        tr = traj_plates(a_s, v0, L5 * 1e-3, (400 - x0) / S5 * 1e-3)
        pts = [(x0 + S5 * x * 1e3, yc - S5 * y * 1e3) for x, y in tr]
        b = defs("d50") + plates(x0, x1, yt, yb, True) + elines_v(range(int(x0 + 30), int(x1 - 10), 45), yt, yb, True)
        b += poly(pts, GRN, 1.8, "6 4", .55) + mover(pts, 4.0, 4.5)
        b += dim_h(x0, x1, yb + 38, "L = 4,0 cm") + dim_v(x0 - 16, yt, yb, "d", x0 - 40, yc + 4, "start")
        b += txt(30, 248, "● electron mẫu (khác đề: U khác) bay vào mép bản", GRN, 12, "start", "600")
        return fig("d5-0", "0 0 420 258", "Electron bay vào mép hai bản phẳng nằm ngang, bản trên mang dấu cộng; quỹ đạo mẫu cong dần về phía bản trên rồi đi thẳng",
                   b, "Mô phỏng: electron mẫu, vẽ đúng tỉ lệ kích thước hai bản; U khác đề; chạy chậm hàng tỉ lần.")
    x0 = 130; x1 = x0 + S5 * L5
    b = defs("d52") + plates(x0, x1, yt, yb, True) + elines_v(range(int(x0 + 30), int(x1 - 10), 45), yt, yb, True)
    v, tip = vec_luc("r", 30, yc, 1, 0, 16.0, 2.5, 3)
    b += electron(16, yc, 7) + v + txt(8, yc + 26, "v_0 = 1,6·10⁷ m/s", RED, 11, "start")
    b += dim_h(x0, x1, yb + 38, "L") + dim_v(x1 + 16, yt, yb, "d", x1 + 24, yc + 4)
    b += txt(8, 20, "L = 4,0 cm", "currentColor", 12) + txt(8, 38, "d = 2,0 cm", "currentColor", 12) + txt(8, 56, "vào chính giữa", "currentColor", 12)
    b += txt(8, 248, "Cần tìm: U lớn nhất để còn bay ra", ORG, 13)
    return fig("d5-2", "0 0 420 258", "Electron bay vào chính giữa hai bản nằm ngang dài 4,0 cm cách nhau 2,0 cm, bản trên mang điện dương", b,
               "Dữ kiện: kích thước hai bản vẽ đúng tỉ lệ; electron vào đúng chính giữa. ")
