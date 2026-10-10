"""Hình cho bài tập mẫu bài 7 (Bài 6. Định luật Boyle. Định luật Charles, Vật lí 12).
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Dạng hỏi thể tích/chiều dài là đáp số thì mô phỏng dùng SỐ MẪU KHÁC đề (ghi rõ ở chú thích) để không lộ đáp số."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import chevron

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"
import re as _re


def rich(s, size=13):
    parts = _re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
    return out


def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)


def R(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}"{d} opacity="{op}"/>')


def anim(attr, vals, dur, keytimes=None):
    kt = f' keyTimes="{";".join(f"{k:.3f}" for k in keytimes)}"' if keytimes else ""
    return (f'<animate attributeName="{attr}" values="{";".join(f"{v:.1f}" for v in vals)}"{kt} dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')


def gdot(x, y, r=3):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{GRN}" opacity=".9"/>'


def fdots(n):
    """Toạ độ tương đối (0..1, 0..1) của n phân tử khí, rải đều giả ngẫu nhiên nhưng cố định."""
    return [(((i * 37 + 11) % 97) / 97, ((i * 53 + 29) % 89) / 89) for i in range(n)]


# ───────────── Dạng 1 · bơm xe: 240 cm³ → 80 cm³ (đúng tỉ lệ, V₂ là dữ kiện) ─────────────
def _tube_h(yt, yb, x0, length):
    return (seg(x0, yt, x0, yb, "currentColor", 4) + seg(x0, yt, x0 + length, yt, "currentColor", 2.4)
            + seg(x0, yb, x0 + length, yb, "currentColor", 2.4))


def d1(kk):
    p = f"d1{kk}"; X0, YT, YB, S = 40, 62, 122, 0.8
    xp0, xp1 = X0 + 240 * S, X0 + 80 * S
    dots = fdots(16)
    if kk == 0:
        b = defs(p) + _tube_h(YT, YB, X0, 270)
        b += seg(xp1, YT - 8, xp1, YB + 8, "currentColor", 1.4, "5 4", .6)
        for fx, fy in dots:
            x = X0 + 8 + fx * (240 * S - 16); y = YT + 9 + fy * (YB - YT - 18)
            xe = X0 + (x - X0) / 3
            b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{GRN}" opacity=".9">{smil("cx", [x, xe], 4)}</circle>'
        pist = (R(xp0 - 4, YT + 2, 8, YB - YT - 4, fill="currentColor") + seg(xp0 + 4, 92, xp0 + 50, 92, "currentColor", 4)
                + seg(xp0 + 50, 74, xp0 + 50, 110, "currentColor", 5))
        b += (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;{xp1 - xp0:.1f} 0" dur="4s" '
              f'begin="indefinite" fill="freeze"/>{pist}</g>')
        b += txt(X0 - 6, YB + 22, "đầu ra bịt kín", "currentColor", 12, "start", "400")
        b += dim(p, "o", X0 + 2, YB + 40, xp1, YB + 40, "", 0, 0) + txt((X0 + xp1) / 2, YB + 58, "V₂ = 80 cm³", ORG, 13, "middle")
        b += dim(p, "b", X0 + 2, YB + 74, xp0, YB + 74, "", 0, 0) + txt((X0 + xp0) / 2, YB + 92, "V₁ = 240 cm³", BLUE, 13, "middle")
        b += txt(16, 24, "p₁ = 1,0·10⁵ Pa", "currentColor", 13) + txt(16, 44, "nhiệt độ không đổi", "currentColor", 13, "start", "400")
        b += txt(250, 24, "p₂ = ?", RED) + txt(250, 44, "ấn cán bơm thật chậm", "currentColor", 12, "start", "400")
        return fig("c1-0", "0 0 420 216", "Bơm xe đạp bịt kín đầu ra, ấn cán bơm làm thể tích khí giảm từ 240 xuống 80 centimét khối",
                   b, "Mô phỏng: pittông ấn từ V₁ = 240 cm³ xuống V₂ = 80 cm³ (đúng tỉ lệ), các phân tử khí dồn lại; chạy 4 s.")
    b = defs(p)
    for k, (Vv, y0, nm) in enumerate(((240, 40, "Trạng thái 1"), (80, 140, "Trạng thái 2"))):
        yt, yb = y0 + 14, y0 + 66; xp = X0 + Vv * S
        b += txt(16, y0 + 4, nm, "currentColor", 13, "start", "700")
        b += _tube_h(yt, yb, X0, 270)
        for fx, fy in dots:
            x = X0 + 8 + fx * (240 * S - 16); y = yt + 9 + fy * (yb - yt - 18)
            b += gdot(X0 + (x - X0) * Vv / 240, y)
        b += R(xp - 4, yt + 2, 8, yb - yt - 4, fill="currentColor") + seg(xp + 4, (yt + yb) / 2, xp + 50, (yt + yb) / 2, "currentColor", 4)
        b += seg(xp + 50, yt + 12, xp + 50, yb - 12, "currentColor", 5)
    b += txt(318, 70, "V₁ = 240 cm³", BLUE) + txt(318, 90, "p₁ = 1,0·10⁵ Pa", "currentColor")
    b += txt(318, 170, "V₂ = 80 cm³", BLUE) + txt(318, 190, "p₂ = ?", RED)
    b += txt(16, 232, "T không đổi · lượng khí không đổi", "currentColor", 13, "start", "400")
    return fig("c1-2", "0 0 420 244", "Hai trạng thái của khí trong bơm xe: thể tích 240 centimét khối rồi 80 centimét khối, nhiệt độ không đổi",
               b, "Dữ kiện: hai trạng thái cùng nhiệt độ, cùng lượng khí. " + NOTE)


# ───────────── Dạng 2 · xilanh đứng, nung đẳng áp (mô phỏng dùng số mẫu: 300 K → 450 K) ─────────────
def _tube_v(xl, xr, yt, yb):
    return seg(xl, yt, xl, yb, "currentColor", 2.4) + seg(xr, yt, xr, yb, "currentColor", 2.4) + seg(xl, yb, xr, yb, "currentColor", 4)


def d2(kk):
    p = f"d2{kk}"; XL, XR, YT, YB = 80, 150, 60, 200
    dots = fdots(12)
    if kk == 0:
        h1, h2 = 60, 90      # số mẫu: T tăng 1,5 lần nên V tăng 1,5 lần (không phải số của đề)
        b = defs(p) + _tube_v(XL, XR, YT, YB)
        for fx, fy in dots:
            x = XL + 6 + fx * (XR - XL - 12); y = YB - 8 - fy * (h1 - 16)
            ye = YB - (YB - y) * h2 / h1
            b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{GRN}" opacity=".9">{anim("cy", [y, ye], 5)}</circle>'
        pist = R(XL + 1.5, YB - h1 - 8, XR - XL - 3, 8, fill="currentColor")
        b += (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 {-(h2 - h1)}" dur="5s" '
              f'begin="indefinite" fill="freeze"/>{pist}</g>')
        for fx0 in (96, 116, 134):
            b += f'<path d="M{fx0},{YB + 8} q-7,9 0,18 q3,-5 7,-4 q5,-6 -1,-14 z" fill="{ORG}" opacity=".85"/>'
        b += txt((XL + XR) / 2, 46, "khí trời", "currentColor", 12, "middle", "400")
        yf = YB - h2 - 4
        b += seg(XR + 4, yf, XR + 40, yf, ORG, 1.6, "5 4") + txt(XR + 46, yf + 4, "V₂ = ?", ORG)
        b += txt(220, 160, "pittông tự do, nhẹ", "currentColor", 12, "start", "400") + txt(220, 180, "áp suất khí không đổi", "currentColor", 12, "start", "400")
        b += txt(16, 24, "V₁ = 450 cm³ · t₁ = 17 °C", "currentColor", 13) + txt(250, 24, "nung tới t₂ = 75 °C", ORG)
        return fig("c2-0", "0 0 420 236", "Xilanh đặt thẳng đứng miệng hướng lên, pittông nhẹ trượt tự do, khí được nung nóng nên pittông nâng lên",
                   b, "Mô phỏng minh hoạ với số mẫu khác đề (nung từ 300 K lên 450 K: thể tích tăng 1,5 lần); pittông tự do nên áp suất không đổi. "
                      "Thể tích V₂ của đề tính ở lời giải; chạy 5 s.")
    b = defs(p)
    for (xl, h, tt, vv, nm) in ((50, 60, "t₁ = 17 °C", "V₁ = 450 cm³", "Trạng thái 1"), (250, 84, "t₂ = 75 °C", "V₂ = ?", "Trạng thái 2")):
        xr = xl + 70
        b += _tube_v(xl, xr, YT, YB)
        b += R(xl + 1.5, YB - h - 8, 67, 8, fill="currentColor")
        for fx, fy in dots:
            b += gdot(xl + 6 + fx * 58, YB - 8 - fy * (h - 16))
        b += txt(xl + 35, 44, nm, "currentColor", 13, "middle") + txt(xl + 35, YB + 24, tt, "currentColor", 13, "middle")
        b += txt(xr + 6, YB - h - 4, vv, BLUE if "450" in vv else RED, 12, "start")
    b += arrow(p, "o", 160, 90, 232, 90, 3) + txt(196, 78, "nung nóng", ORG, 12, "middle")
    b += txt(196, 112, "p không đổi", "currentColor", 12, "middle", "400")
    return fig("c2-2", "0 0 420 240", "Hai trạng thái của khối khí trong xilanh ở áp suất không đổi: 17 độ C rồi 75 độ C",
               b, "Dữ kiện: cùng lượng khí, cùng áp suất, hai nhiệt độ khác nhau. " + NOTE)


# ───────────── Dạng 3 · đồ thị V–T hai đường đẳng áp (đúng tỉ lệ; số trên hình là dữ kiện) ─────────────
def d3(kk):
    p = f"d3{kk}"; OX, OY = 60, 210; KT, KV = 0.8, 18          # px/K, px/lít
    X = lambda T: OX + KT * T
    Y = lambda V: OY - KV * V
    b = defs(p)
    b += arrow(p, "g", OX, OY, 398, OY, 2) + arrow(p, "g", OX, OY, OX, 22, 2)
    b += txt(412, OY - 8, "T (K)", GRN, 13, "end") + txt(OX + 8, 20, "V (lít)", GRN, 13, "start")
    for T in (100, 200, 300, 400):
        b += seg(X(T), OY - 3, X(T), OY + 3, "currentColor", 1.6) + txt(X(T), OY + 18, str(T), "currentColor", 12, "middle", "400")
    for V in (2, 4, 6, 8, 10):
        b += seg(OX - 3, Y(V), OX + 3, Y(V), "currentColor", 1.6) + txt(OX - 8, Y(V) + 4, str(V), "currentColor", 12, "end", "400")
    b += txt(OX - 8, OY + 18, "O", "currentColor", 13, "end")
    s1, s2 = 4 / 300, 6 / 300
    b += seg(X(0), Y(0), X(400), Y(400 * s1), ORG, 2.6) + seg(X(0), Y(0), X(400), Y(400 * s2), BLUE, 2.6)
    b += txt(X(400) + 6, Y(400 * s1) + 4, "(1)", ORG, 13) + txt(X(400) + 6, Y(400 * s2) + 4, "(2)", BLUE, 13)
    b += seg(X(300), OY, X(300), Y(6), "currentColor", 1.3, "5 4", .6)
    b += seg(OX, Y(4), X(300), Y(4), ORG, 1.3, "5 4", .7) + seg(OX, Y(6), X(300), Y(6), BLUE, 1.3, "5 4", .7)
    b += dot(X(300), Y(4), 4.5, ORG) + dot(X(300), Y(6), 4.5, BLUE)
    b += txt(X(300) + 8, Y(4) + 18, "A: V = 4 lít", ORG, 12) + txt(X(300) - 8, Y(6) - 8, "B: V = 6 lít", BLUE, 12, "end")
    b += txt(X(300), OY + 34, "T = 300 K", "currentColor", 12, "middle", "400")
    if kk == 0:
        for sl, c in ((s1, ORG), (s2, BLUE)):
            T0, T1 = 20, 400
            b += (f'<circle cx="{X(T0):.1f}" cy="{Y(T0 * sl):.1f}" r="5" fill="{c}" stroke="currentColor" stroke-width="1.5">'
                  f'{smil("cx", [X(T0), X(T1)], 5)}{smil("cy", [Y(T0 * sl), Y(T1 * sl)], 5)}</circle>')
        return fig("c3-0", "0 0 420 252", "Đồ thị V theo T của một lượng khí: hai đường thẳng kéo dài qua gốc toạ độ, điểm trạng thái chạy dọc mỗi đường",
                   b, "Mô phỏng: điểm trạng thái chạy dọc từng đường từ gần gốc O tới 400 K (đồ thị đúng tỉ lệ); chạy 5 s.")
    return fig("c3-2", "0 0 420 252", "Đồ thị V theo T của một lượng khí: hai đường thẳng kéo dài qua gốc toạ độ, tại 300 kenvin thể tích lần lượt là 4 lít và 6 lít",
               b, "Dữ kiện: hai điểm A, B cùng nhiệt độ 300 K nhưng nằm trên hai đường khác nhau, mỗi đường kéo dài đi qua O. Hình vẽ đúng tỉ lệ.")


# ───────────── Dạng 4 · hai giai đoạn: đẳng nhiệt rồi đẳng áp (mô phỏng dùng số mẫu) ─────────────
def d4(kk):
    p = f"d4{kk}"
    if kk == 0:
        XL, XR, YT, YB = 80, 150, 30, 190
        H0, H1, H2 = 100, 50, 75       # mẫu: nén còn 1/2 (p tăng 2 lần), rồi nung T tăng 1,5 lần (V tăng 1,5 lần)
        dots = fdots(12)
        b = defs(p) + _tube_v(XL, XR, YT, YB) + seg(XL, YT, XR, YT, "currentColor", 2.4)
        D = 6
        kt = [0, .45, 1]
        for fx, fy in dots:
            x = XL + 6 + fx * (XR - XL - 12); y0 = YB - 8 - fy * (H0 - 16)
            ys = [y0, YB - (YB - y0) * H1 / H0, YB - (YB - y0) * H2 / H0]
            b += f'<circle cx="{x:.1f}" cy="{y0:.1f}" r="3" fill="{GRN}" opacity=".9">{anim("cy", ys, D, kt)}</circle>'
        top0 = YB - H0
        pist = (R(XL + 1.5, top0 - 8, XR - XL - 3, 8, fill="currentColor") + seg((XL + XR) / 2, top0 - 8, (XL + XR) / 2, top0 - 34, "currentColor", 4)
                + seg((XL + XR) / 2 - 16, top0 - 34, (XL + XR) / 2 + 16, top0 - 34, "currentColor", 5))
        b += (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 {H0 - H1};0 {H0 - H2}" keyTimes="0;.45;1" '
              f'dur="{D}s" begin="indefinite" fill="freeze"/>{pist}</g>')
        for fx0 in (96, 116, 134):
            b += (f'<path d="M{fx0},{YB + 8} q-7,9 0,18 q3,-5 7,-4 q5,-6 -1,-14 z" fill="{ORG}" opacity="0">'
                  f'{anim("opacity", [0, 0, .85, .85], D, [0, .45, .5, 1])}</path>')
        b += txt((XL + XR) / 2, YB + 50, "giai đoạn 1: đẩy chậm · giai đoạn 2: nung", "currentColor", 12, "middle", "400")
        b += txt(210, 60, "lúc đầu: 3,0 lít · 1,0 atm · 27 °C", "currentColor", 13)
        b += txt(210, 84, "giai đoạn 1: T không đổi", BLUE, 13) + txt(210, 104, "tới p = 2,5 atm", BLUE, 13, "start", "400")
        b += txt(210, 128, "giai đoạn 2: p = 2,5 atm", ORG, 13) + txt(210, 148, "nung tới t = 127 °C", ORG, 13, "start", "400")
        b += txt(210, 176, "thể tích cuối V = ?", RED)
        return fig("c4-0", "0 0 420 250", "Khí trong xilanh có pittông: trước hết đẩy pittông chậm, sau đó nung nóng ở áp suất không đổi",
                   b, "Mô phỏng minh hoạ trình tự với số mẫu khác đề (nén còn một nửa, rồi nung làm thể tích tăng 1,5 lần); không đúng với số của đề. Chạy 6 s.")
    OX, OY = 60, 240
    X = lambda v: OX + v; Y = lambda v: OY - v
    c = 13000.0
    x1, x2, x3 = 260, 70, 170
    y1, y2 = c / x1, c / x2
    b = defs(p) + arrow(p, "g", OX, OY, 400, OY, 2) + arrow(p, "g", OX, OY, OX, 26, 2)
    b += txt(400, OY + 18, "V", GRN, 13, "end") + txt(OX + 8, 24, "p", GRN, 13, "start") + txt(OX - 8, OY + 16, "O", "currentColor", 13, "end")
    pts = [(X(v), Y(c / v)) for v in [x2 + (x1 - x2) * i / 40 for i in range(41)]]
    b += poly(pts, BLUE, 2.6)
    b += seg(X(x2), Y(y2), X(x3), Y(y2), ORG, 2.6)
    for (xx, yy, nm, col) in ((x1, y1, "1", "currentColor"), (x2, y2, "2", "currentColor"), (x3, y2, "3", "currentColor")):
        b += dot(X(xx), Y(yy), 4.5, col)
    b += txt(X(x1) + 8, Y(y1) - 8, "1", "currentColor", 14) + txt(X(x2) - 14, Y(y2) - 8, "2", "currentColor", 14) + txt(X(x3) + 4, Y(y2) - 10, "3", "currentColor", 14)
    mx, my = pts[22]; nx, ny = pts[23]
    b += chevron(pts[12][0], pts[12][1], pts[11][0] - pts[12][0], pts[11][1] - pts[12][1], BLUE, 2.6, 11)
    b += chevron(X(x3), Y(y2), 1, 0, ORG, 2.6, 11)
    b += txt(X(x2) + 50, Y(y2) - 10, "đẳng áp", ORG, 12, "middle") + txt(X(150) + 20, Y(c / 150) + 30, "đẳng nhiệt", BLUE, 12, "start")
    b += txt(250, 100, "1: 1,0 atm · 3,0 lít · 27 °C", "currentColor", 12, "start", "400")
    b += txt(250, 120, "2: 2,5 atm · V₂ = ? · 27 °C", "currentColor", 12, "start", "400")
    b += txt(250, 140, "3: 2,5 atm · V₃ = ? · 127 °C", "currentColor", 12, "start", "400")
    return fig("c4-2", "0 0 420 266", "Đồ thị p theo V: từ trạng thái 1 sang 2 theo đường đẳng nhiệt, từ 2 sang 3 theo đường nằm ngang (đẳng áp)",
               b, "Dữ kiện: hai quá trình nối tiếp, thể tích cuối của quá trình trước là thể tích đầu của quá trình sau. " + NOTE)


# ───────────── Dạng 5 · ống thuỷ ngân: lật ống (số của đề cho l₁, h; l₂ là đáp số) ─────────────
def _tube5(cx, ytop, scale, sealed_bottom, gas_cm, hg_cm, Ltot=80, w=22, with_hg=True):
    """Ống thẳng đứng dài Ltot cm; sealed_bottom: đầu kín ở dưới. Khí dài gas_cm tính từ đầu kín, Hg hg_cm ngay sau khí."""
    H = Ltot * scale; yb = ytop + H
    out = (seg(cx - w / 2, ytop, cx - w / 2, yb, "currentColor", 2.4) + seg(cx + w / 2, ytop, cx + w / 2, yb, "currentColor", 2.4))
    out += seg(cx - w / 2, yb if sealed_bottom else ytop, cx + w / 2, yb if sealed_bottom else ytop, "currentColor", 4)
    if sealed_bottom:
        g0, g1 = yb - gas_cm * scale, yb
        h0, h1 = g0 - hg_cm * scale, g0
    else:
        g0, g1 = ytop, ytop + gas_cm * scale
        h0, h1 = g1, g1 + hg_cm * scale
    out += R(cx - w / 2 + 1.5, g0, w - 3, g1 - g0, GRN, 0, GRN, 0, "", .22)
    if with_hg:
        out += R(cx - w / 2 + 1.5, h0, w - 3, h1 - h0, GREY, 0, GREY, 0, "", .85)
    return out


def d5(kk):
    p = f"d5{kk}"; SC = 2.5; YT = 24; L = 80
    if kk == 0:
        cx1, cx2 = 100, 300
        b = defs(p)
        b += _tube5(cx1, YT, SC, True, 28, 20)
        # ống bên phải: quay 180° quanh tâm ống (vật rắn: lúc vừa lật cột Hg còn nguyên vị trí tương đối)
        cyc = YT + L * SC / 2
        inner = _tube5(cx2, YT, SC, True, 28, 20)
        b += (f'<g><animateTransform attributeName="transform" type="rotate" values="0 {cx2} {cyc:.1f};180 {cx2} {cyc:.1f}" dur="3s" '
              f'begin="indefinite" fill="freeze"/>{inner}</g>')
        yb = YT + L * SC
        b += dim(p, "b", cx1 - 26, yb - 28 * SC, cx1 - 26, yb, "", 0, 0) + txt(cx1 - 32, yb - 28 * SC / 2 + 4, "l₁ = 28 cm", BLUE, 12, "end")
        b += dim(p, "o", cx1 + 26, yb - 48 * SC, cx1 + 26, yb - 28 * SC, "", 0, 0) + txt(cx1 + 32, yb - 38 * SC + 4, "h = 20 cm", ORG, 12, "start")
        b += txt(cx1, YT - 6, "miệng hướng lên", "currentColor", 12, "middle", "400") + txt(cx2, YT - 6, "lật 180°", "currentColor", 12, "middle", "400")
        b += txt(cx1 + 30, yb - 4 - 0, "", "currentColor")
        b += txt(196, 60, "p₀ = 760 mmHg", "currentColor", 13, "middle") + txt(196, 80, "ống dài 80 cm", "currentColor", 12, "middle", "400")
        b += txt(cx2 + 30, yb - 60, "l₂ = ?", RED, 13, "start")
        return fig("c5-0", "0 0 420 236", "Ống thuỷ tinh một đầu kín, cột thuỷ ngân giam một cột khí; bên phải là ống đó được lật 180 độ",
                   b, "Mô phỏng: lật ống 180° (ống bên trái giữ nguyên làm mốc). Đây là lúc VỪA lật, cột Hg chưa kịp dịch; "
                      "vị trí cân bằng mới (chiều dài cột khí l₂) là điều cần tìm. Chạy 3 s.")
    b = defs(p)
    cx1, cx2 = 100, 300
    b += _tube5(cx1, YT, SC, True, 28, 20)
    yb = YT + L * SC
    b += dim(p, "b", cx1 - 26, yb - 28 * SC, cx1 - 26, yb, "", 0, 0) + txt(cx1 - 32, yb - 28 * SC / 2 + 4, "l₁ = 28 cm", BLUE, 12, "end")
    b += dim(p, "o", cx1 + 26, yb - 48 * SC, cx1 + 26, yb - 28 * SC, "", 0, 0) + txt(cx1 + 32, yb - 38 * SC + 4, "h = 20 cm", ORG, 12, "start")
    b += txt(cx1, YT - 6, "miệng hướng lên", "currentColor", 12, "middle", "400")
    b += txt(cx1 + 14, YT + 12, "p₀", RED, 13, "start")
    # ống phải: vị trí cột Hg chưa biết → vẽ đứt đoạn (dấu gãy) và không theo tỉ lệ
    w = 22; ytp = YT; ybt = YT + 150
    b += seg(cx2 - w / 2, ytp, cx2 - w / 2, ybt, "currentColor", 2.4) + seg(cx2 + w / 2, ytp, cx2 + w / 2, ybt, "currentColor", 2.4) + seg(cx2 - w / 2, ytp, cx2 + w / 2, ytp, "currentColor", 4)
    b += R(cx2 - w / 2 + 1.5, ytp, w - 3, 50, GRN, 0, GRN, 0, "", .22) + R(cx2 - w / 2 + 1.5, ytp + 50, w - 3, 50, GREY, 0, GREY, 0, "", .85)
    for zy in (ytp + 36,):
        b += seg(cx2 - w / 2 - 6, zy + 4, cx2 + w / 2 + 6, zy - 4, "currentColor", 2, "", 1)
    b += txt(cx2 + 18, ytp + 28, "l₂ = ?", RED, 13, "start") + txt(cx2 + 18, ytp + 80, "h = 20 cm", ORG, 12, "start")
    b += txt(cx2, ybt + 18, "miệng hướng xuống", "currentColor", 12, "middle", "400") + txt(cx2 + 14, ybt + 34, "p₀", RED, 13, "start")
    b += txt(196, 60, "p₀ = 760 mmHg", "currentColor", 13, "middle") + txt(196, 80, "ống dài 80 cm", "currentColor", 12, "middle", "400")
    return fig("c5-2", "0 0 420 236", "Hai trạng thái của khí bị giam: miệng ống hướng lên và miệng ống hướng xuống, cột thuỷ ngân cao 20 xentimét",
               b, "Dữ kiện: ống bên trái vẽ đúng tỉ lệ; ống bên phải vẽ sơ lược, dấu gãy cho biết chiều dài cột khí l₂ chưa biết. " + NOTE)


BUILD = [d1, d2, d3, d4, d5]
