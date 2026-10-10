"""Hình cho bài tập mẫu bài 3 (VL12): Nội năng. Định luật 1 của nhiệt động lực học — lesson_id 4.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mọi chuyển động tính từ số liệu của đề; không để lộ đáp số. Vectơ: đầu V 30°, độ dài = k·độ lớn (vec_luc)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"
CW, CA = ORG, RED       # công = cam, nhiệt = đỏ (chỉ trong bài này)


def R(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}"{d} opacity="{op}"/>')

def Rf(x, y, w, h, fill, op=.25, extra=""):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" opacity="{op}" stroke="none"{extra}>'

def circ(x, y, r, c="currentColor", sw=2, fill="none"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'

def anim(attr, vals, dur, kt=None, tag="animate", extra=""):
    k = f' keyTimes="{";".join(f"{v:.4f}" for v in kt)}"' if kt else ""
    vs = ";".join(v if isinstance(v, str) else f"{v:.1f}" for v in vals)
    return f'<{tag} attributeName="{attr}" values="{vs}"{k} dur="{dur:.2f}s" begin="indefinite" fill="freeze"{extra}/>'

def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, s, c, size, anchor, weight)


# ───────────── xilanh nằm ngang, mở bên phải ─────────────
def cyl_walls(x0, y0, w, h):
    return seg(x0, y0, x0 + w, y0, "currentColor", 3) + seg(x0, y0 + h, x0 + w, y0 + h, "currentColor", 3) + seg(x0, y0, x0, y0 + h, "currentColor", 3)

def piston_parts(head, y0, h, handle_dx=50):
    yc = y0 + h / 2
    return (R(head - 4, y0 + 3, 8, h - 6, sw=2.4, fill="currentColor", op=.9) + seg(head + 4, yc, head + handle_dx, yc, "currentColor", 3)
            + seg(head + handle_dx, yc - 14, head + handle_dx, yc + 14, "currentColor", 4))

def cyl_static(x0, y0, w, h, head, handle_dx=50, gas_op=.22):
    return (Rf(x0 + 1.5, y0 + 1.5, head - x0 - 5.5, h - 3, BLUE, gas_op) + "</rect>" + cyl_walls(x0, y0, w, h) + piston_parts(head, y0, h, handle_dx))

def cyl_anim(x0, y0, w, h, head0, dxs, dur, handle_dx=50, kt=None, gas_op=.22):
    """Xilanh với pit-tông tịnh tiến theo dãy dịch chuyển dxs (so với head0); khí co/giãn theo."""
    tr = anim("transform", [f"{d:.1f} 0" for d in [0] + list(dxs)], dur, kt, "animateTransform", ' type="translate"')
    gas = (Rf(x0 + 1.5, y0 + 1.5, head0 - x0 - 5.5, h - 3, BLUE, gas_op)
           + anim("width", [head0 - x0 - 5.5 + d for d in [0] + list(dxs)], dur, kt) + "</rect>")
    return gas + cyl_walls(x0, y0, w, h) + f"<g>{tr}{piston_parts(head0, y0, h, handle_dx)}</g>"


# ═════════════ DẠNG 1 · đĩa phanh nhôm ═════════════
def disc(cx, cy, r, rot_vals=None, dur=4):
    parts = circ(cx, cy, r, "currentColor", 3) + circ(cx, cy, 12, "currentColor", 2.4)
    for k in range(6):
        a = math.radians(30 + 60 * k)
        parts += circ(cx + 38 * math.cos(a), cy + 38 * math.sin(a), 7, GREY, 2)
    parts += seg(cx - r + 4, cy, cx - 14, cy, GREY, 2) + seg(cx + 14, cy, cx + r - 4, cy, GREY, 2)
    if rot_vals:
        tr = anim("transform", [f"{a} {cx} {cy}" for a in rot_vals], dur, None, "animateTransform", ' type="rotate"')
        return f"<g>{tr}{parts}</g>"
    return parts

def d1(kk):
    cx, cy, r = 100, 100, 60
    if kk == 0:
        b = disc(cx, cy, r, [0, 260, 460, 600, 690, 740, 760], 4)
        b += R(cx + r + 2, cy - 24, 16, 48, ORG, 2.4, ORG, 3, op=.9) + txt(cx + r - 14, cy - 32, "má phanh", ORG, 12)
        b += txt(210, 34, "m = 0,25 kg", "currentColor", 13, "start", "400") + txt(210, 54, "c = 880 J/(kg·K)", "currentColor", 13, "start", "400")
        b += txt(210, 84, "Phanh gấp: ma sát", "currentColor", 13, "start", "400") + txt(210, 102, "thực hiện công", "currentColor", 13, "start", "400") + txt(210, 122, "A = 4400 J", ORG)
        b += txt(210, 150, "25,0 → 45,0 → 25,0 °C", "currentColor", 13, "start", "400")
        b += txt(210, 176, "ΔU = ?", RED, 14)
        return fig("b4-1-0", "0 0 420 196", "Đĩa phanh nhôm quay chậm dần và dừng lại khi má phanh ép vào, kèm các dữ kiện của đề",
                   b, "Mô phỏng: đĩa quay chậm dần rồi dừng (minh hoạ, chạy 4 s).")
    # kk=2: dòng thời gian ba mốc nhiệt độ
    b = ""
    xs = [60, 210, 360]
    for x, t in zip(xs, ["25,0 °C", "45,0 °C", "25,0 °C"]):
        b += circ(x, 70, 30, GRN, 2.4) + txt(x, 75, t, "currentColor", 13, "middle")
    b += txt(60, 28, "trước phanh", "currentColor", 12, "middle", "400") + txt(210, 28, "sau phanh", "currentColor", 12, "middle", "400") + txt(360, 28, "nguội hẳn", "currentColor", 12, "middle", "400")
    b += arrow("", "o", 94, 70, 176, 70, 2.6) + arrow("", "r", 244, 70, 326, 70, 2.6)
    b += txt(135, 118, "Phanh", CW, 13, "middle") + txt(135, 138, "A = 4400 J", CW, 13, "middle") + txt(135, 158, "Q = 0", "currentColor", 13, "middle", "400")
    b += txt(285, 118, "Nguội", CA, 13, "middle") + txt(285, 138, "A = 0", "currentColor", 13, "middle", "400") + txt(285, 158, "Q = ?", CA, 13, "middle")
    return fig("b4-1-2", "0 0 420 176", "Dòng thời gian ba mốc nhiệt độ của đĩa phanh: trước phanh 25 độ, sau phanh 45 độ, nguội hẳn 25 độ",
               b, "Dữ kiện: hai giai đoạn, mỗi giai đoạn chỉ một cách tác động. " + NOTE)


# ═════════════ DẠNG 2 · nén rồi giãn khí trong bơm tay ═════════════
def d2(kk):
    if kk == 0:
        x0, y0, w, h, head0 = 50, 50, 230, 60, 230
        b = cyl_anim(x0, y0, w, h, head0, [-70, -25], 4, 50)
        b += txt(16, 24, "Khí trong xilanh của bơm tay", "currentColor", 13, "start", "400")
        b += txt(16, 150, "① nén: công vào 180 J, nhiệt ra 70 J", CW, 13) + txt(16, 172, "② giãn: nhiệt vào 130 J, công ra 150 J", CA, 13)
        b += txt(330, 90, "ΔU = ?", RED, 14)
        return fig("b4-2-0", "0 0 420 186", "Pit-tông nén khí trong xilanh rồi để khí giãn ra, kèm dữ kiện hai giai đoạn",
                   b, "Mô phỏng: pit-tông bị đẩy vào (nén) rồi lùi ra một phần (giãn), chạy 4 s.")
    K = 0.3
    b = txt(10, 22, "① Nén", "currentColor", 14) + txt(220, 22, "② Giãn", "currentColor", 14)
    # giai đoạn 1
    b += cyl_static(10, 70, 100, 50, 65, 50)
    v, _ = vec_luc("o", 169, 95, -1, 0, 180, K, 3); b += v + txt(122, 66, "công 180 J", CW, 12)
    v, _ = vec_luc("r", 40, 120, 0, 1, 70, K, 3); b += v + txt(50, 152, "nhiệt 70 J", CA, 12)
    # giai đoạn 2
    b += cyl_static(220, 70, 100, 50, 310, 50)
    v, _ = vec_luc("r", 270, 120 + K * 130, 0, -1, 130, K, 3); b += v + txt(220, 177, "nhiệt 130 J", CA, 12)
    v, _ = vec_luc("o", 360, 95, 1, 0, 150, K, 3); b += v + txt(335, 66, "công 150 J", CW, 12)
    b += txt(10, 195, "Độ dài mũi tên tỉ lệ độ lớn (k = 0,3 px/J)", "currentColor", 12, "start", "400")
    return fig("b4-2-2", "0 0 420 206", "Hai giai đoạn của khí trong xilanh: nén với công vào 180 J và nhiệt ra 70 J; giãn với nhiệt vào 130 J và công ra 150 J",
               b, "Dữ kiện: mũi tên chỉ chiều năng lượng đi vào hay ra khỏi khí. " + NOTE)


# ═════════════ DẠNG 3 · bài ngược ═════════════
def d3(kk):
    if kk == 0:
        x0, y0, w, h, head0 = 50, 50, 230, 60, 220
        b = cyl_anim(x0, y0, w, h, head0, [-70], 3, 50)
        b += txt(16, 24, "Quá trình 1: nén khí", "currentColor", 13, "start", "400")
        b += txt(16, 150, "① nén: công vào 25 J, nội năng giảm 35 J", CW, 13) + txt(16, 172, "② hơ nóng: nhiệt vào 100 J, nội năng tăng 20 J", CA, 13)
        b += txt(330, 90, "Q₁ = ?", RED, 14)
        return fig("b4-3-0", "0 0 420 186", "Pit-tông nén khí trong xilanh ở quá trình 1, kèm dữ kiện hai quá trình",
                   b, "Mô phỏng quá trình ①: pit-tông bị đẩy vào, chạy 3 s. Quá trình ② chỉ mô tả bằng số liệu.")
    K = 0.4
    b = txt(10, 22, "① Nén", "currentColor", 14) + txt(220, 22, "② Hơ nóng", "currentColor", 14)
    b += cyl_static(10, 70, 100, 50, 65, 50)
    v, _ = vec_luc("o", 156, 95, -1, 0, 25, K, 3); b += v + txt(110, 66, "công 25 J", CW, 12)
    b += txt(60, 152, "Q₁ = ?", RED, 13, "middle") + txt(60, 172, "ΔU₁ = −35 J", "currentColor", 13, "middle")
    b += cyl_static(220, 70, 100, 50, 275, 50)
    v, _ = vec_luc("r", 270, 120 + K * 100, 0, -1, 100, K, 3); b += v + txt(280, 150, "nhiệt 100 J", CA, 12)
    b += txt(340, 96, "A₂ = ?", ORG, 13) + txt(340, 116, "ΔU₂ = +20 J", "currentColor", 12)
    b += txt(10, 200, "Độ dài mũi tên tỉ lệ độ lớn (k = 0,4 px/J)", "currentColor", 12, "start", "400")
    return fig("b4-3-2", "0 0 420 210", "Quá trình 1: nén khí, công vào 25 J, nội năng giảm 35 J. Quá trình 2: hơ nóng, nhiệt vào 100 J, nội năng tăng 20 J",
               b, "Dữ kiện: mỗi quá trình cho ΔU và một trong hai đại lượng A, Q; đại lượng còn lại là ẩn. " + NOTE)


# ═════════════ DẠNG 4 · khoan khối đồng trong cốc nước ═════════════
def beaker(static):
    b = Rf(194, 96, 186, 86, BLUE, .22) + "</rect>"
    b += seg(190, 60, 190, 184, "currentColor", 3) + seg(384, 60, 384, 184, "currentColor", 3) + seg(190, 184, 384, 184, "currentColor", 3)
    b += R(232, 142, 110, 40, ORG, 2.4, ORG, 2, op=.8)
    b += txt(287, 168, "đồng 0,300 kg", "currentColor", 12, "middle")
    b += txt(194, 114, "nước 0,250 kg", "currentColor", 12, "start")
    return b

def thermo(ymerc_top, anim_vals=None, dur=4):
    b = R(46, 36, 14, 124, "currentColor", 2.4, rx=7) + circ(53, 168, 11, RED, 2.4, RED)
    top0 = 160 - 50
    if anim_vals:
        b += (f'<rect x="50" y="{top0:.1f}" width="6" height="{160 - top0:.1f}" fill="{RED}" stroke="none">'
              + anim("y", [160 - h for h in anim_vals], dur) + anim("height", anim_vals, dur) + "</rect>")
    else:
        b += f'<rect x="50" y="{ymerc_top:.1f}" width="6" height="{160 - ymerc_top:.1f}" fill="{RED}" stroke="none"/>'
    return b

def d4(kk):
    if kk == 0:
        hs = [50 + 40 * i / 5 for i in range(6)]   # cột thuỷ ngân cao 50 px (24,0 °C) → 90 px (27,0 °C): 13,33 px/K
        b = beaker(False)
        drill = (seg(287, 20, 287, 128, "currentColor", 4) + R(279, 14, 16, 12, "currentColor", 2.4)
                 + f'<line x1="287" y1="40" x2="287" y2="128" stroke="{ORG}" stroke-width="9" stroke-dasharray="3 5" opacity=".9">'
                 + anim("stroke-dashoffset", [0, -16, -32, -48, -64, -80], 4) + "</line>")
        tr = anim("transform", ["0 0", "0 8", "0 0", "0 8", "0 0", "0 8"], 4, None, "animateTransform", ' type="translate"')
        b += f"<g>{tr}{drill}</g>"
        b += thermo(0, hs, 4)
        b += txt(30, 22, "nhiệt kế (nước)", "currentColor", 12, "start", "400")
        b += txt(70, 114, "24,0 °C", "currentColor", 12, "start", "400") + txt(70, 74, "27,0 °C", "currentColor", 12, "start", "400")
        b += seg(60, 110, 66, 110, "currentColor", 1.6) + seg(60, 70, 66, 70, "currentColor", 1.6)
        b += txt(130, 52, "mũi khoan: A = 5400 J", CW, 13, "start", "700")
        b += txt(130, 202, "ΔU của khối đồng = ?", RED, 13)
        return fig("b4-4-0", "0 0 420 214", "Mũi khoan khoan khối đồng đặt trong cốc nước, nhiệt kế trong nước chỉ tăng từ 24 độ lên 27 độ",
                   b, "Mô phỏng: mũi khoan làm việc, nước nóng dần từ 24,0 °C đến 27,0 °C (chạy 4 s).")
    # kk=2: hai hệ
    b = txt(10, 22, "Hệ 1: khối đồng", "currentColor", 14) + txt(220, 22, "Hệ 2: nước", "currentColor", 14)
    b += R(40, 78, 150, 60, ORG, 2.4, ORG, 3, op=.8) + txt(115, 113, "đồng 0,300 kg", "currentColor", 13, "middle")
    K = 0.01
    v, _ = vec_luc("o", 115, 78 - K * 5400, 0, 1, 5400, K, 3); b += v + txt(124, 50, "công 5400 J", CW, 13)
    b += txt(115, 160, "A = 5400 J · Q = ?", "currentColor", 13, "middle")
    b += R(230, 78, 170, 60, BLUE, 2.4, BLUE, 3, op=.8) + txt(315, 113, "nước 0,250 kg", "currentColor", 13, "middle")
    b += txt(315, 160, "A = 0 · Q = ?", "currentColor", 13, "middle") + txt(315, 182, "24,0 °C → 27,0 °C", "currentColor", 12, "middle", "400")
    b += seg(190, 108, 230, 108, GREY, 2, "5 4") + txt(210, 98, "nhiệt", GREY, 12, "middle")
    b += txt(10, 205, "Mũi tên tỉ lệ độ lớn (k = 0,01 px/J). Nhiệt trao đổi chưa biết nên không vẽ.", "currentColor", 12, "start", "400")
    return fig("b4-4-2", "0 0 420 216", "Hai hệ: khối đồng nhận công 5400 J, nước nhận nhiệt từ khối đồng",
               b, "Dữ kiện: đặt dấu riêng cho từng hệ. " + NOTE)


# ═════════════ DẠNG 5 · chu trình gas của tủ lạnh ═════════════
def fridge(anim_dot):
    b = ""
    # đường ống
    pipe = [(110, 135, 110, 100), (110, 100, 165, 100), (275, 100, 330, 100), (330, 100, 330, 135), (330, 165, 330, 200),
            (330, 200, 275, 200), (165, 200, 110, 200), (110, 200, 110, 165)]
    for x1, y1, x2, y2 in pipe:
        b += seg(x1, y1, x2, y2, GREY, 3)
    for cxn, cyn, wn, hn, name in [(110, 150, 80, 30, "Máy nén"), (220, 100, 110, 26, "Dàn nóng"), (330, 150, 84, 30, "Van tiết lưu"), (220, 200, 110, 26, "Dàn lạnh")]:
        b += R(cxn - wn / 2, cyn - hn / 2, wn, hn, "currentColor", 2.4, "none", 4) + txt(cxn, cyn + 4.5, name, "currentColor", 12, "middle", "600")
    K = 0.15
    v, _ = vec_luc("o", 47.5, 150, 1, 0, 150, K, 3); b += v + txt(4, 128, "công 150 J", CW, 12)
    v, _ = vec_luc("r", 220, 87, 0, -1, 450, K, 3); b += v + txt(232, 50, "nhiệt toả 450 J", CA, 12)
    b += txt(220, 234, "nhiệt thu Q = ?", BLUE, 13, "middle")
    if anim_dot:
        pts = [(110, 118), (110, 100), (330, 100), (330, 200), (110, 200), (110, 118)]
        ls = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(5)]
        tot = sum(ls); kt = [0]
        for l in ls: kt.append(kt[-1] + l / tot)
        b += (f'<circle cx="110" cy="118" r="6" fill="{GRN}" stroke="currentColor" stroke-width="1.5">'
              + anim("cx", [p[0] for p in pts], 6, kt) + anim("cy", [p[1] for p in pts], 6, kt) + "</circle>")
    return b

def d5(kk):
    if kk == 0:
        return fig("b4-5-0", "0 0 420 244", "Gas tuần hoàn qua máy nén, dàn nóng, van tiết lưu, dàn lạnh rồi về đúng chỗ xuất phát",
                   fridge(True),
                   "Mô phỏng: một phân tử gas đi hết một chu trình rồi về chỗ cũ (chạy 6 s). Mũi tên tỉ lệ độ lớn (k = 0,15 px/J).")
    return fig("b4-5-2", "0 0 420 244", "Sơ đồ chu trình của gas: máy nén nhận công 150 J, dàn nóng toả 450 J, dàn lạnh thu nhiệt chưa biết",
               fridge(False), "Dữ kiện: trong một chu trình gas về đúng trạng thái đầu. " + NOTE)


BUILD = [d1, d2, d3, d4, d5]
