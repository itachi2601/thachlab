"""Hình cho bài tập mẫu Bài 21 "Tụ điện" (Vật lí 11), lesson_id 40. Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm
(đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích. Đường Q-U, vùng năng lượng, dòng nạp, điện tích hiện dần, góc kéo
bản đều TÍNH từ số liệu của đề. Trục chỉ ghi các số đề cho; đại lượng cần tìm ghi dấu "?"."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, chỉ ghi các số đề cho."
ORGT = ORG


def tx(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, s, c, size, anchor, weight)


def cs(base, i, rest=""):
    """Nhãn có chỉ số dưới thật bằng tspan: base_i rest."""
    return f'{base}<tspan dy="4" font-size="10">{i}</tspan><tspan dy="-4">{rest}</tspan>'


def an(attr, vals, dur, nd=1):
    return f'<animate attributeName="{attr}" values="{";".join(f"{v:.{nd}f}" if not isinstance(v, str) else v for v in vals)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


def runner(pts, dur):
    return (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">'
            f'{an("cx", [p[0] for p in pts], dur)}{an("cy", [p[1] for p in pts], dur)}</circle>')


def cap_h(x, y, h=13):
    """Kí hiệu tụ trên dây nằm ngang: hai vạch đứng tại x-4 và x+4."""
    return seg(x - 4, y - h, x - 4, y + h, "currentColor", 3) + seg(x + 4, y - h, x + 4, y + h, "currentColor", 3)


def batt_v(x, y):
    """Nguồn trên dây thẳng đứng, cực dương ở trên (vạch dài), tâm tại (x, y)."""
    return (seg(x - 13, y - 5, x + 13, y - 5, "currentColor", 2.4) + seg(x - 7, y + 5, x + 7, y + 5, "currentColor", 5)
            + tx(x + 17, y - 3, "+", ORG, 14))


def wire(pts, w=2.2):
    return poly(pts, "currentColor", w)


def axes_qu(ox, oy, wpx, hpx, xl, yl):
    b = arrow("", "g", ox - 8, oy, ox + wpx + 14, oy, 2) + arrow("", "g", ox, oy + 8, ox, oy - hpx - 14, 2)
    b += tx(ox + wpx + 12, oy + 17, xl, GRN, 13, "end") + tx(ox + 8, oy - hpx - 6, yl, GRN, 13)
    b += tx(ox - 6, oy + 16, "O", "currentColor", 13, "end")
    return b


# ───────────── Dạng 1 · tụ A: 9,0 V, 63 µC ─────────────
def d1(kk):
    ox, oy, ux, qy = 80, 160, 180, 110      # 9,0 V ↔ 180 px ; 63 µC ↔ 110 px
    px, py = ox + ux, oy - qy
    b = axes_qu(ox, oy, 290, 125, "U (V)", "Q (µC)")
    b += seg(ox, oy, px, py, BLUE, 2.8)
    b += seg(px, py, px, oy, "currentColor", 1.5, "4 4", .7) + seg(ox, py, px, py, "currentColor", 1.5, "4 4", .7)
    b += tx(px, oy + 18, "9,0 V", "currentColor", 13, "middle") + tx(ox - 8, py + 4, "63 µC", "currentColor", 13, "end")
    b += tx(px + 14, py + 40, "C = ?", ORG, 14) + dot(px, py, 4, "currentColor")
    if kk == 0:
        n = 24
        pts = [(ox + (px - ox) * i / n, oy - (oy - py) * i / n) for i in range(n + 1)]
        b += runner(pts, 3.5)
        return fig("d1-0", "0 0 420 196", "Đồ thị điện tích Q theo hiệu điện thế U của tụ A, điểm xanh chạy từ gốc tới điểm ứng với 9,0 V", b,
                   "Mô phỏng: điểm chạy trên đồ thị Q–U của tụ A (đường thẳng qua gốc) từ lúc chưa nạp tới 9,0 V; chạy chậm, không theo thời gian thật. " + NOTE)
    return fig("d1-2", "0 0 420 196", "Dữ kiện của tụ A: đường thẳng Q theo U qua gốc, điểm đo ứng với 9,0 V và 63 microculông", b,
               "Dữ kiện: một điểm đo của tụ A (9,0 V; 63 µC). Tụ B (4,7 nF – 25 V) không vẽ ở đây. " + NOTE)


# ───────────── Dạng 2 · C = 50 µF, U = 40 V : diện tích dưới đường Q-U ─────────────
def d2(kk):
    ox, oy, wpx, hpx = 70, 160, 240, 118      # 40 V ↔ 240 px ; 2,0 mC ↔ 118 px
    px, py = ox + wpx, oy - hpx
    b = axes_qu(ox, oy, 280, 130, "U (V)", "Q")
    if kk == 0:
        n = 20
        vals = ";".join(f"{ox},{oy} {ox + wpx * i / n:.1f},{oy} {ox + wpx * i / n:.1f},{oy - hpx * i / n:.1f}" for i in range(n + 1))
        b += (f'<polygon points="{ox},{oy} {ox},{oy} {ox},{oy}" fill="{ORG}" fill-opacity=".38" stroke="none">'
              f'<animate attributeName="points" values="{vals}" dur="4.00s" begin="indefinite" fill="freeze"/></polygon>')
    else:
        b += f'<polygon points="{ox},{oy} {px},{oy} {px},{py}" fill="{ORG}" fill-opacity=".38" stroke="none"/>'
    b += seg(ox, oy, px, py, BLUE, 2.8) + seg(px, py, px, oy, "currentColor", 1.5, "4 4", .7)
    b += tx(px, oy + 18, "40 V", "currentColor", 13, "middle") + tx(px - 40, oy - 24, "W = ?", ORG, 14, "middle")
    b += tx(130, 30, "C = 50 µF", "currentColor", 13) + dot(px, py, 4, "currentColor")
    if kk == 0:
        n = 24
        pts = [(ox + wpx * i / n, oy - hpx * i / n) for i in range(n + 1)]
        b += runner(pts, 4.0)
        return fig("d2-0", "0 0 420 196", "Đồ thị Q theo U của tụ 50 microfara, vùng tam giác dưới đường thẳng được tô dần khi hiệu điện thế tăng từ 0 tới 40 V", b,
                   "Mô phỏng: nạp tụ từ 0 tới 40 V, vùng tô cam là phần diện tích dưới đường Q–U được tạo ra dần (chạy chậm). " + NOTE)
    return fig("d2-2", "0 0 420 196", "Dữ kiện: tụ 50 microfara nạp tới 40 V, tam giác dưới đường Q theo U", b,
               "Dữ kiện: tụ 50 µF nạp tới 40 V; năng lượng cần tìm gắn với vùng tô cam. " + NOTE)


# ───────────── Dạng 3 · tụ phẳng không khí, 10 cm, 2,0 mm, 300 V ─────────────
def plates_fixed(extra=""):
    """Hai bản nằm ngang (nhìn từ cạnh) nối nguồn; trả về phần khung dùng chung."""
    b = wire([(118, 60), (118, 30), (84, 30), (84, 88)]) + wire([(84, 104), (84, 160), (118, 160), (118, 130)])
    b += batt_v(84, 96) + tx(14, 100, "300 V", "currentColor", 13)
    b += seg(120, 60, 300, 60, "currentColor", 6) + seg(120, 130, 300, 130, "currentColor", 6)
    b += dim("", "o", 328, 63, 328, 127, "d = 2,0 mm", 338, 100)
    b += dim("", "b", 126, 46, 300, 46, "cạnh 10 cm", 213, 38, "middle")
    return b


def d3(kk):
    b = plates_fixed()
    signs = "".join(tx(140 + 20 * k, 78, "+", ORG, 15, "middle", "800") + tx(140 + 20 * k, 124, "−", BLUE, 17, "middle", "800") for k in range(8))
    lines = "".join(field_line(x, 86, x, 112, GRN, 1.8, "5 4", 8) for x in (160, 200, 240, 280))
    if kk == 0:
        b += f'<g opacity=".18">{an("opacity", [0.18, 1], 3.0, 2)}{signs}{lines}</g>'
    else:
        b += signs + lines
    b += tx(318, 152, "C = ?", ORG, 13) + tx(318, 170, "E = ?", ORG, 13) + tx(318, 188, "U tối đa = ?", ORG, 13)
    if kk == 0:
        return fig("d3-0", "0 0 420 196", "Tụ phẳng nối nguồn 300 V, điện tích dương và âm hiện dần trên hai bản, đường sức điện hiện ra giữa hai bản", b,
                   "Mô phỏng: nối nguồn, điện tích hiện dần trên hai bản và điện trường xuất hiện giữa hai bản. Khoảng cách d vẽ to hơn thực tế, không theo tỉ lệ.")
    return fig("d3-2", "0 0 420 196", "Dữ kiện tụ phẳng không khí: bản vuông cạnh 10 cm, hai bản cách nhau 2,0 mm, nối nguồn 300 V", b,
               "Dữ kiện của tụ phẳng. Khoảng cách d vẽ to hơn thực tế, không theo tỉ lệ.")


# ───────────── Dạng 4 · (C1 nt C2) // C3, U = 60 V ─────────────
def cap_v(x, y, w=13):
    """Kí hiệu tụ trên dây thẳng đứng: hai vạch ngang tại y-4 và y+4."""
    return seg(x - w, y - 4, x + w, y - 4, "currentColor", 3) + seg(x - w, y + 4, x + w, y + 4, "currentColor", 3)


def d4(kk):
    b = wire([(24, 45), (235, 45)]) + wire([(24, 150), (235, 150)])
    b += wire([(24, 45), (24, 93)]) + wire([(24, 106), (24, 150)])
    b += wire([(150, 45), (150, 78)]) + wire([(150, 86), (150, 111)]) + wire([(150, 119), (150, 150)])
    b += wire([(235, 45), (235, 94)]) + wire([(235, 102), (235, 150)])
    b += batt_v(24, 98) + cap_v(150, 82) + cap_v(150, 115) + cap_v(235, 98)
    b += dot(150, 45, 3.5, "currentColor") + dot(150, 150, 3.5, "currentColor")
    b += tx(34, 130, "60 V", "currentColor", 13)
    b += tx(130, 80, cs("C", 1, " = 5 µF"), "currentColor", 12, "end") + tx(130, 119, cs("C", 2, " = 20 µF"), "currentColor", 12, "end")
    b += tx(254, 102, cs("C", 3, " = 6,0 µF"), "currentColor", 12)
    if kk == 2:
        b += tx(192, 70, cs("C", "b", " = ?"), ORG, 13, "middle") + tx(192, 135, cs("U", 1, " = ?"), ORG, 13, "middle")
    ox, oy, wpx, hpx = 346, 150, 60, 98
    gx = lambda f: [(ox + wpx * i / 40, oy - hpx * f(i / 40)) for i in range(41)]
    f = lambda u: math.exp(-4.2 * u)
    b += arrow("", "g", ox - 8, oy, ox + wpx + 12, oy, 2) + arrow("", "g", ox, oy + 6, ox, oy - hpx - 12, 2)
    b += tx(ox + wpx + 10, oy + 17, "t", GRN, 13, "end") + tx(ox + 8, oy - hpx - 6, "i", GRN, 13) + tx(ox - 6, oy + 16, "O", "currentColor", 13, "end")
    b += poly(gx(f), BLUE, 2.6) + tx(ox - 26, 24, "Dòng nạp", "currentColor", 12)
    if kk == 0:
        b += runner(gx(f)[::2], 4.0)
        return fig("d4-0", "0 0 420 196", "Mạch ba tụ nối nguồn 60 V và đồ thị dòng nạp theo thời gian, điểm xanh chạy dọc đồ thị", b,
                   "Mô phỏng: lúc đóng mạch dòng nạp lớn, giảm dần rồi về không khi các tụ nạp xong (chạy chậm). " + NOTE)
    return fig("d4-2", "0 0 420 196", "Dữ kiện: C1 nối tiếp C2 trên một nhánh, nhánh đó song song với C3, nối nguồn 60 V", b,
               "Dữ kiện: C₁ nối tiếp C₂ trên một nhánh; nhánh đó song song với C₃; cả bộ nối nguồn 60 V.")


# ───────────── Dạng 5 · tụ nạp 150 V, ngắt nguồn, kéo bản d → 3d ─────────────
def d5(kk):
    xs, xe, ybot, ytop = 170, 330, 170, 140          # khoảng cách ban đầu 30 px ; sau khi kéo 90 px (gấp ba)
    dy = -2 * (ybot - ytop)
    b = wire([(110, 40), (50, 40), (50, 90)]) + wire([(50, 100), (50, 190), (110, 190)])
    b += batt_v(50, 95) + dot(110, 40, 3.5, "currentColor") + dot(110, 190, 3.5, "currentColor") + tx(4, 112, "150 V", "currentColor", 12)
    b += tx(118, 54, "đã ngắt khỏi nguồn", "currentColor", 12)
    b += seg(xs, ybot, xe, ybot, "currentColor", 6)
    b += dim("", "o", 352, ytop + 3, 352, ybot - 3, "d", 360, 160)
    plate = seg(xs, ytop, xe, ytop, "currentColor", 6) + "".join(tx(xs + 14 + 22 * k, ytop - 8, "+", ORG, 15, "middle", "800") for k in range(7))
    b += "".join(tx(xs + 14 + 22 * k, ybot - 8, "−", BLUE, 17, "middle", "800") for k in range(7))
    ghost = f'<rect x="{xs}" y="{ytop + dy - 3}" width="{xe - xs}" height="6" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="5 4" opacity=".6"/>'
    b += tx(340, 40, "U′ = ?", ORG, 13) + tx(340, 58, "W′ = ?", ORG, 13)
    if kk == 0:
        b += ghost + (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 {dy}" dur="4.00s" begin="indefinite" fill="freeze"/>{plate}</g>')
        return fig("d5-0", "0 0 420 206", "Tụ phẳng đã ngắt khỏi nguồn, bản trên được kéo lên cho tới khi khoảng cách hai bản gấp ba", b,
                   "Mô phỏng: kéo bản trên lên cho tới khi khoảng cách hai bản gấp ba; nét đứt là vị trí cuối của bản trên (chạy chậm). Không theo tỉ lệ.")
    b += plate + ghost
    b += tx(272, 114, "kéo lên", GRN, 12) + arrow("", "g", 262, ytop - 12, 262, ytop + dy + 8, 2)
    return fig("d5-2", "0 0 420 206", "Dữ kiện: tụ phẳng đã ngắt khỏi nguồn, bản trên sẽ được kéo lên tới vị trí nét đứt (khoảng cách gấp ba)", b,
               "Dữ kiện: nét liền là vị trí ban đầu của bản trên, nét đứt là vị trí sau khi kéo (khoảng cách hai bản gấp ba). Không theo tỉ lệ.")
