"""Hình cho bài tập mẫu Bài 34 "Khối lượng riêng. Áp suất chất lỏng" (Vật lí 10), lesson_id 79.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mô phỏng tính từ công thức (lật khối, đầu dò chìm, nước dâng, U-tube cân bằng áp suất, khối nổi dao động tắt dần).
KHÔNG vẽ đáp số: các hình đề chỉ ghi dữ kiện của đề, dấu "?" cho đại lượng cần tìm.
D4 mô phỏng dùng cột nước 13,6 cm (khác 20,4 cm của đề); D5 mô phỏng dùng khối 2,0 kg (khác 2,4 kg của đề)."""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from svg_lib import chevron

GREY = "#94a3b8"
WATER = f'fill="{BLUE}" fill-opacity="0.28"'
OIL = f'fill="{ORG}" fill-opacity="0.30"'
HG = 'fill="#94a3b8" fill-opacity="0.55"'
WOOD = 'fill="#ca8a04" fill-opacity="0.35"'


def ts(x, y, base, sb, tail="", c="currentColor", size=13, anchor="start", weight="700"):
    """Nhãn có chỉ số dưới: base_sb tail."""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{base}<tspan dy="4" font-size="{size - 3}">{sb}</tspan><tspan dy="-4">{tail}</tspan></text>')


def an(attr, vals, dur, nd=1, extra=""):
    return (f'<animate attributeName="{attr}" values="{";".join(f"{v:.{nd}f}" for v in vals)}" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"{extra}/>')


def fade_in(show, dur):
    """Nhóm hiện ra rời rạc: show[i] ∈ {0,1} theo mẫu."""
    return (f'<animate attributeName="opacity" values="{";".join(str(v) for v in show)}" dur="{dur:.2f}s" calcMode="discrete" '
            f'begin="indefinite" fill="freeze"/>')


def rad(a):
    return math.radians(a)


# ───────────── Dạng 1: khối hộp 3,0 × 4,0 × 15 cm, m = 1,26 kg ─────────────
def d1(kk):
    s = 8.0                      # px / cm
    gy = 170.0
    W, H = 15 * s, 3 * s         # tư thế nằm (hình chiếu: dài 15, cao 3; bề dày 4 vuông góc hình vẽ)
    b = ground(gy, 16, 410)
    if kk == 0:
        x0 = 60.0; pv = (x0 + W, gy)
        b += f'<rect x="{x0}" y="{gy - H}" width="{W}" height="{H}" fill="none" stroke="{GREY}" stroke-width="1.4" stroke-dasharray="5 4"/>'
        ths = [0] * 3 + [4.5 * i for i in range(1, 21)] + [90] * 6
        step = 0.12; dur = step * (len(ths) - 1)
        vals = ";".join(f"{t:.1f} {pv[0]:.1f} {pv[1]:.1f}" for t in ths)
        b += (f'<g><rect x="{x0}" y="{gy - H}" width="{W}" height="{H}" {WOOD} stroke="currentColor" stroke-width="2.4"/>'
              f'<animateTransform attributeName="transform" type="rotate" values="{vals}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></g>')
        b += dim("", "b", x0, gy - H - 14, x0 + W, gy - H - 14, "", 0, 0) + lbl(x0 + W / 2 - 22, gy - H - 20, "15 cm", BLUE, 13, "start", "700")
        b += dim("", "o", x0 - 12, gy - H, x0 - 12, gy, "", 0, 0) + lbl(x0 - 18, gy - H / 2 + 5, "3,0 cm", ORG, 13, "end", "700")
        b += lbl(14, 196, "nằm: chạm bàn bằng mặt 4,0 × 15 cm", "currentColor", 12, "start", "400")
        b += lbl(236, 60, "Hộp 3,0 × 4,0 × 15 cm", "currentColor", 13, "start", "700") + lbl(236, 82, "m = 1,26 kg", "currentColor", 13, "start", "700")
        b += lbl(236, 106, "ρ = ?", ORG, 13, "start", "700") + lbl(236, 128, "p = ?", ORG, 13, "start", "700")
        return fig("d1-0", "0 0 420 206", "Khối hộp kim loại nằm trên mặt bàn được lật sang tư thế đứng", b,
                   "Mô phỏng: khối được lật từ tư thế nằm sang tư thế đứng, quay quanh cạnh dưới (khoảng 3 s); đường nét đứt là vị trí lúc đầu. Tỉ lệ 1 cm ứng với 8 px, bề dày 4,0 cm vuông góc với hình.")
    # kk = 2: hai tư thế, ghi kích thước
    xa = 30.0; xb = 250.0
    b += f'<rect x="{xa}" y="{gy - H}" width="{W}" height="{H}" {WOOD} stroke="currentColor" stroke-width="2.4"/>'
    b += seg(xa, gy, xa + W, gy, GRN, 4.5)
    b += dim("", "b", xa, gy - H - 14, xa + W, gy - H - 14, "", 0, 0) + lbl(xa + W / 2 - 22, gy - H - 20, "15 cm", BLUE, 13, "start", "700")
    b += dim("", "o", xa + W + 12, gy - H, xa + W + 12, gy, "", 0, 0) + lbl(xa + W + 18, gy - H / 2 + 5, "3,0 cm", ORG, 13, "start", "700")
    Wb, Hb = 3 * s, 15 * s
    b += f'<rect x="{xb}" y="{gy - Hb}" width="{Wb}" height="{Hb}" {WOOD} stroke="currentColor" stroke-width="2.4"/>'
    b += seg(xb, gy, xb + Wb, gy, GRN, 4.5)
    b += dim("", "o", xb + Wb + 14, gy - Hb, xb + Wb + 14, gy, "", 0, 0) + lbl(xb + Wb + 20, gy - Hb / 2 + 5, "15 cm", ORG, 13, "start", "700")
    b += dim("", "b", xb, gy - Hb - 12, xb + Wb, gy - Hb - 12, "", 0, 0) + lbl(xb + Wb / 2, gy - Hb - 22, "3,0 cm", BLUE, 13, "middle", "700")
    b += lbl(14, 196, "nằm: mặt chạm bàn 4,0 × 15 cm", "currentColor", 12, "start", "400") + lbl(232, 196, "đứng: mặt chạm bàn 3,0 × 4,0 cm", "currentColor", 12, "start", "400")
    return fig("d1-2", "0 0 420 206", "Khối hộp ở hai tư thế: nằm và đứng, với các kích thước và mặt chạm bàn", b,
               "Dữ kiện: hai tư thế của cùng một khối (1 cm ứng với 8 px); nét xanh lá là mặt chạm bàn; bề dày 4,0 cm vuông góc với hình.")


# ───────────── Dạng 2: bể dầu hoả sâu 2,5 m, M cách mặt thoáng 1,0 m, nắp van 20 cm² ─────────────
def tank_oil(b, with_valve=True):
    x0, x1, ys, yb = 70.0, 210.0, 40.0, 140.0       # 40 px / m
    b += f'<rect x="{x0}" y="{ys}" width="{x1 - x0}" height="{yb - ys}" {OIL}/>'
    b += f'<path d="M{x0},22 V{yb} H{x1} V22" fill="none" stroke="currentColor" stroke-width="2.6"/>'
    b += seg(x0, ys, x1, ys, "currentColor", 1.4, "5 4", .8) + lbl(x1 - 4, ys - 5, "mặt thoáng", "currentColor", 12, "end", "400")
    b += seg(222, ys, 222, yb, "currentColor", 1.2, "", .8)
    for i in range(6):
        y = ys + 20 * i
        b += seg(222, y, 228, y, "currentColor", 1.2, "", .8) + lbl(232, y + 4, ["0", "0,5", "1,0", "1,5", "2,0", "2,5 m"][i], "currentColor", 12, "start", "400")
    b += lbl(222, 16, "độ sâu", "currentColor", 12, "start", "400")
    b += dot(86, ys + 40, 4.5, "currentColor") + lbl(96, ys + 45, "M", "currentColor", 13, "start", "700")
    b += dim("", "o", 56, ys, 56, ys + 40, "", 0, 0) + lbl(50, ys + 24, "1,0 m", ORG, 13, "end", "700")
    if with_valve:
        b += f'<rect x="125" y="{yb - 4}" width="30" height="8" fill="{GRN}" fill-opacity="0.7" stroke="currentColor" stroke-width="1.6"/>' + lbl(140, yb + 22, "nắp van S = 20 cm²", "currentColor", 12, "middle", "400")
    return b, (x0, x1, ys, yb)


def d2(kk):
    b, (x0, x1, ys, yb) = tank_oil("")
    b += lbl(268, 62, "Dầu hoả", "currentColor", 13, "start", "700") + lbl(268, 82, "ρ = 0,80 g/cm³", "currentColor", 13, "start", "700") + lbl(268, 102, "Mực dầu cao 2,5 m", "currentColor", 13, "start", "700")
    if kk == 0:
        n = 25; step = 0.12; dur = step * (n - 1)
        ys_ = [ys + (yb - 5 - ys) * i / (n - 1) for i in range(n)]
        b += f'<circle cx="104" cy="{ys_[0]:.1f}" r="5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">{an("cy", ys_, dur)}</circle>'
        return fig("d2-0", "0 0 420 176", "Đầu dò áp suất chìm đều từ mặt thoáng xuống đáy bể dầu hoả", b,
                   "Mô phỏng: đầu dò chìm đều từ mặt thoáng xuống đáy bể (khoảng 3 s), thước độ sâu ghi bên phải. Không vẽ số đo áp suất.")
    b += ts(284, 124, "p", "đáy", " = ?", ORG) + ts(284, 144, "p", "M", " = ?", ORG) + lbl(284, 164, "F = ?", ORG, 13, "start", "700")
    return fig("d2-2", "0 0 420 176", "Bể dầu hoả cao 2,5 m, điểm M cách mặt thoáng 1,0 m, nắp van ở đáy", b,
               "Dữ kiện: độ sâu đo từ mặt thoáng xuống; 40 px ứng với 1 m. Chưa có số đo áp suất nào.")


# ───────────── Dạng 3: thùng trụ cao 1,8 m đầy nước, miệng hở; A cách đáy 0,50 m ─────────────
def d3(kk):
    sc = 70.0; yb = 182.0; x0, x1 = 70.0, 170.0; ytop = yb - 1.8 * sc
    yA = yb - 0.5 * sc; xA = 120.0
    b = ""
    if kk == 0:
        n = 27; step = 0.13; dur = step * (n - 1)
        lv = [1.8 * i / (n - 1) for i in range(n)]
        ysf = [yb - sc * v for v in lv]
        hs = [sc * v for v in lv]
        b += f'<rect x="{x0}" y="{ysf[0]:.1f}" width="{x1 - x0}" height="{hs[0]:.1f}" {WATER}>{an("y", ysf, dur)}{an("height", hs, dur)}</rect>'
    else:
        b += f'<rect x="{x0}" y="{ytop}" width="{x1 - x0}" height="{yb - ytop}" {WATER}/>'
    b += f'<path d="M{x0},{ytop} V{yb} H{x1} V{ytop}" fill="none" stroke="currentColor" stroke-width="2.6"/>'
    b += lbl(120, ytop - 12, "miệng hở", "currentColor", 12, "middle", "400")
    b += dot(xA, yA, 4.5, "currentColor") + lbl(xA + 9, yA + 4, "A", "currentColor", 13, "start", "700")
    b += dim("", "b", 50, ytop, 50, yb, "", 0, 0) + lbl(44, (ytop + yb) / 2 + 5, "1,8 m", BLUE, 13, "end", "700")
    b += dim("", "o", 192, yA, 192, yb, "", 0, 0) + lbl(198, (yA + yb) / 2 + 5, "0,50 m", ORG, 13, "start", "700")
    b += lbl(262, 66, "Nước: ρ = 1000 kg/m³", "currentColor", 13, "start", "700") + ts(262, 88, "p", "a", " = 1,0·10⁵ Pa", "currentColor") + lbl(262, 110, "g = 10 m/s²", "currentColor", 13, "start", "700")
    if kk == 0:
        # mũi tên độ sâu của A: từ mặt nước xuống A, chỉ hiện khi nước đã vượt A (đúng hình học)
        tipy = yA - 6
        tails = [min(y, tipy - 14) for y in ysf]
        show = [1 if lv[i] > 0.5 + 0.35 else 0 for i in range(n)]
        d_ch = [re.search(r'd="([^"]+)"', chevron(xA, tipy, 0, 1, ORG, 2.8, 9)).group(1)] * n
        ln = (f'<line x1="{xA}" y1="{tails[0]:.1f}" x2="{xA}" y2="{tipy:.1f}" stroke="{ORG}" stroke-width="2.8">{an("y1", tails, dur)}</line>'
              f'<path d="{d_ch[0]}" fill="none" stroke="{ORG}" stroke-width="2.8" stroke-linejoin="miter" stroke-miterlimit="10" stroke-linecap="butt"/>')
        b += f'<g opacity="0">{ln}{fade_in(show, dur)}</g>'
        b += dot(xA, yA, 4.5, "currentColor")
        return fig("d3-0", "0 0 420 206", "Nước dâng dần trong thùng trụ cao 1,8 m tới miệng thùng; điểm A cách đáy 0,50 m", b,
                   "Mô phỏng: thùng được đổ nước từ cạn đến đầy (khoảng 3 s). Mũi tên cam nối mặt nước với A, xuất hiện khi nước vượt qua A và dài dần theo mực nước. 70 px ứng với 1 m.")
    b += ts(262, 132, "p", "đáy", " = ?", ORG) + lbl(262, 152, "p tại A = ?", ORG, 13, "start", "700")
    return fig("d3-2", "0 0 420 206", "Thùng trụ cao 1,8 m đầy nước, miệng hở; điểm A cách đáy 0,50 m", b,
               "Dữ kiện: thùng đầy nước đến miệng; 70 px ứng với 1 m; A đánh dấu cách đáy 0,50 m. Chưa vẽ độ sâu của A.")


# ───────────── Dạng 4: ống chữ U, thuỷ ngân + nước ─────────────
def d4_tube(b, ox, y0=None):
    """Khung ống chữ U: nhánh trái trong x∈[ox, ox+36], nhánh phải x∈[ox+76, ox+112]; đáy trong y=170."""
    b += f'<path d="M{ox},24 V200 H{ox + 112} V24" fill="none" stroke="currentColor" stroke-width="2.6"/>'
    b += f'<path d="M{ox + 36},24 V170 H{ox + 76} V24" fill="none" stroke="currentColor" stroke-width="2.6"/>'
    b += lbl(ox + 18, 17, "pₐ", "currentColor", 12, "middle", "400") + lbl(ox + 94, 17, "pₐ", "currentColor", 12, "middle", "400")
    return b


def hg_path(ox, yL, yR):
    pts = [(ox, yL), (ox + 36, yL), (ox + 36, 170), (ox + 76, 170), (ox + 76, yR), (ox + 112, yR), (ox + 112, 200), (ox, 200)]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def d4(kk):
    ox = 100.0
    rho1, rho2 = 1000.0, 13600.0
    legend = (lbl(300, 70, "Nước", BLUE, 13, "start", "700") + lbl(300, 90, "ρ₁ = 1000 kg/m³", "currentColor", 12, "start", "700")
              + lbl(300, 120, "Thuỷ ngân", GREY, 13, "start", "700") + lbl(300, 140, "ρ₂ = 13 600 kg/m³", "currentColor", 12, "start", "700"))
    b = ""
    if kk == 0:
        s = 6.0; y0 = 128.0; h1m = 16.0                      # cột nước minh hoạ 16 cm (khác 20,4 cm của đề)
        n = 28; step = 0.12; dur = step * (n - 1)
        h1 = [h1m * min(i, n - 5) / (n - 5) for i in range(n)]
        h2 = [rho1 * h / rho2 for h in h1]                   # cân bằng áp suất tại hai điểm cùng mức ngang
        yL = [y0 + s * h / 2 for h in h2]                    # mặt phân cách tụt xuống h2/2 (tiết diện đều → thể tích Hg bảo toàn)
        yR = [y0 - s * h / 2 for h in h2]
        top = [yl - s * h for yl, h in zip(yL, h1)]
        assert abs((yL[-1] - yR[-1]) / s - h2[-1]) < 1e-9
        b += (f'<path d="{hg_path(ox, yL[0], yR[0])}" {HG}>'
              f'<animate attributeName="d" values="{";".join(hg_path(ox, a, c) for a, c in zip(yL, yR))}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></path>')
        b += f'<rect x="{ox}" y="{top[0]:.1f}" width="36" height="{yL[0] - top[0]:.1f}" {WATER}>{an("y", top, dur)}{an("height", [a - c for a, c in zip(yL, top)], dur)}</rect>'
        b = d4_tube(b, ox)
        b += f'<line x1="{ox}" y1="{yL[0]:.1f}" x2="{ox + 112}" y2="{yL[0]:.1f}" stroke="{GREY}" stroke-width="1.2" stroke-dasharray="4 4">{an("y1", yL, dur)}{an("y2", yL, dur)}</line>'
        b += f'<circle cx="{ox + 18}" cy="{yL[0]:.1f}" r="4" fill="currentColor">{an("cy", yL, dur)}</circle>'
        b += f'<circle cx="{ox + 94}" cy="{yL[0]:.1f}" r="4" fill="currentColor">{an("cy", yL, dur)}</circle>'
        b += f'<text x="{ox + 24}" y="{yL[0] + 16:.1f}" fill="currentColor" font-size="13" font-weight="700" text-anchor="start">A{an("y", [v + 16 for v in yL], dur)}</text>'
        b += f'<text x="{ox + 99}" y="{yL[0] + 16:.1f}" fill="currentColor" font-size="13" font-weight="700" text-anchor="start">B{an("y", [v + 16 for v in yL], dur)}</text>'
        show = [0] * (n - 3) + [1, 1, 1]
        g = (seg(ox - 14, top[-1], ox - 14, yL[-1], "currentColor", 1.4) + seg(ox - 19, top[-1], ox - 9, top[-1], "currentColor", 1.4) + seg(ox - 19, yL[-1], ox - 9, yL[-1], "currentColor", 1.4)
             + lbl(ox - 22, (top[-1] + yL[-1]) / 2 + 5, "h₁", BLUE, 13, "end", "700")
             + seg(ox + 126, yR[-1], ox + 126, yL[-1], "currentColor", 1.4) + seg(ox + 121, yR[-1], ox + 131, yR[-1], "currentColor", 1.4) + seg(ox + 121, yL[-1], ox + 131, yL[-1], "currentColor", 1.4)
             + lbl(ox + 136, yR[-1] + 12, "h₂", ORG, 13, "start", "700"))
        b += f'<g opacity="0">{g}{fade_in(show, dur)}</g>'
        b += legend + lbl(300, 170, "Minh hoạ:", "currentColor", 12, "start", "400") + lbl(300, 186, "cột nước 16 cm", "currentColor", 12, "start", "400")
        return fig("d4-0", "0 0 420 214", "Rót nước vào nhánh trái ống chữ U chứa thuỷ ngân: thuỷ ngân nhánh trái tụt xuống, nhánh phải dâng lên", b,
                   "Mô phỏng: rót nước vào nhánh trái (khoảng 3 s). Cột nước trong hình là 16 cm, khác số liệu của đề; 1 cm ứng với 6 px. Hai điểm A, B luôn cùng mức ngang.")
    # kk = 2: số liệu của đề; độ chênh h₂ vẽ phóng to
    s = 5.0; yL = 150.0; yR = yL - 14.0; top = yL - s * 20.4
    b += f'<path d="{hg_path(ox, yL, yR)}" {HG}/>'
    b += f'<rect x="{ox}" y="{top:.1f}" width="36" height="{yL - top:.1f}" {WATER}/>'
    b = d4_tube(b, ox)
    b += seg(ox, yL, ox + 112, yL, GREY, 1.2, "4 4") + dot(ox + 18, yL, 4, "currentColor") + dot(ox + 94, yL, 4, "currentColor")
    b += lbl(ox + 24, yL + 16, "A", "currentColor", 13, "start", "700") + lbl(ox + 99, yL + 16, "B", "currentColor", 13, "start", "700")
    b += (seg(ox - 14, top, ox - 14, yL, "currentColor", 1.4) + seg(ox - 19, top, ox - 9, top, "currentColor", 1.4) + seg(ox - 19, yL, ox - 9, yL, "currentColor", 1.4)
          + lbl(ox - 22, (top + yL) / 2 + 5, "h₁ = 20,4 cm", BLUE, 12, "end", "700"))
    b += (seg(ox + 126, yR, ox + 126, yL, "currentColor", 1.4) + seg(ox + 121, yR, ox + 131, yR, "currentColor", 1.4) + seg(ox + 121, yL, ox + 131, yL, "currentColor", 1.4)
          + lbl(ox + 136, (yR + yL) / 2 + 5, "h₂ = ?", ORG, 13, "start", "700"))
    b += legend
    return fig("d4-2", "0 0 420 214", "Ống chữ U: cột nước 20,4 cm ở nhánh trái, thuỷ ngân ở nhánh phải; A ở mặt phân cách, B cùng mức ngang với A", b,
               "Dữ kiện: cột nước vẽ đúng tỉ lệ (1 cm ứng với 5 px); độ chênh h₂ vẽ phóng to cho dễ thấy, không đúng tỉ lệ.")


# ───────────── Dạng 5: khối gỗ 20 × 20 × 10 cm thả vào nước ─────────────
def d5(kk):
    s = 5.0; yw = 90.0; yb = 200.0; x0, x1 = 30.0, 250.0
    bx0, bx1 = 90.0, 190.0
    Hb = 10 * s
    b = f'<rect x="{x0}" y="{yw}" width="{x1 - x0}" height="{yb - yw}" {WATER}/>'
    b += lbl(x1 + 8, yw + 4, "mặt nước", "currentColor", 12, "start", "400")
    b += seg(x0, yw, x1, yw, "currentColor", 1.2, "5 4", .8)
    if kk == 0:
        rho_w, S, g_, msim = 1000.0, 0.04, 10.0, 1.8
        w0 = math.sqrt(rho_w * g_ * S / msim); gam = 2.2; wd = math.sqrt(w0 * w0 - gam * gam)
        deq = msim / (rho_w * S)
        n = 71; step = 0.04; dur = step * (n - 1)
        d = [deq * (1 - math.exp(-gam * i * step) * (math.cos(wd * i * step) + gam / wd * math.sin(wd * i * step))) for i in range(n)]
        d[-1] = deq
        assert min(d) >= -1e-9 and max(d) < 0.10                # luôn chìm một phần (chưa ngập hẳn)
        ybot = [yw + 100 * v * s for v in d]
        ytop = [v - Hb for v in ybot]
        b += f'<rect x="{bx0}" y="{ytop[0]:.1f}" width="{bx1 - bx0}" height="{Hb}" {WOOD} stroke="currentColor" stroke-width="2.4">{an("y", ytop, dur)}</rect>'
        b += f'<path d="M{x0},{yw - 40} V{yb} H{x1} V{yw - 40}" fill="none" stroke="currentColor" stroke-width="2.6"/>'
        b += lbl(266, 56, "Nước: 1000 kg/m³", "currentColor", 13, "start", "700") + lbl(266, 76, "Khối gỗ 20 × 20 × 10 cm", "currentColor", 13, "start", "700")
        b += lbl(266, 126, "Minh hoạ: m = 1,8 kg", "currentColor", 12, "start", "400") + lbl(266, 142, "(khác khối của đề)", "currentColor", 12, "start", "400")
        return fig("d5-0", "0 0 420 214", "Khối gỗ được thả chạm mặt nước, chìm xuống, dao động tắt dần rồi nổi yên", b,
                   "Mô phỏng: khối gỗ cùng kích thước nhưng m = 1,8 kg (khác đề) được thả khi vừa chạm nước; dao động tắt dần theo đúng thời gian thật (khoảng 3 s). 1 cm ứng với 5 px, coi mực nước không đổi.")
    ytop = 34.0
    b += f'<rect x="{bx0}" y="{ytop}" width="{bx1 - bx0}" height="{Hb}" {WOOD} stroke="currentColor" stroke-width="2.4"/>'
    b += f'<path d="M{x0},{yw - 40} V{yb} H{x1} V{yw - 40}" fill="none" stroke="currentColor" stroke-width="2.6"/>'
    b += dim("", "b", bx0, ytop - 8, bx1, ytop - 8, "", 0, 0) + lbl((bx0 + bx1) / 2 - 22, ytop - 14, "20 cm", BLUE, 13, "start", "700")
    b += dim("", "o", bx1 + 12, ytop, bx1 + 12, ytop + Hb, "", 0, 0) + lbl(bx1 + 18, ytop + Hb / 2 + 5, "10 cm", ORG, 13, "start", "700")
    b += lbl((bx0 + bx1) / 2, ytop + Hb / 2 + 5, "2,4 kg", "currentColor", 13, "middle", "700")
    b += lbl(266, 126, "Nước: 1000 kg/m³", "currentColor", 13, "start", "700") + lbl(266, 150, "Đáy khối 20 × 20 cm", "currentColor", 13, "start", "700") + lbl(266, 174, "g = 10 m/s²", "currentColor", 13, "start", "700")
    return fig("d5-2", "0 0 420 214", "Khối gỗ 20 × 20 × 10 cm, khối lượng 2,4 kg, đặt phía trên mặt nước trước khi thả", b,
               "Dữ kiện: khối trước khi thả (1 cm ứng với 5 px). Chưa vẽ mức chìm của khối.")


BUILD = [d1, d2, d3, d4, d5]
