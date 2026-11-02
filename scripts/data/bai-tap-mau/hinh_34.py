"""Hình cho bài tập mẫu Bài 15 "Thực hành: Đo tốc độ truyền âm" (Vật lí 11), lesson_id 34.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mô phỏng chạy SỐ LIỆU MẪU khác đề (ghi rõ trong chú thích) nên không lộ đáp số. Thuộc tính gốc của phần tử động = khung CUỐI
(giảm chuyển động chỉ thấy khung cuối). Hình đề không theo tỉ lệ (chú thích nói rõ)."""
import math, os, re as _re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, không theo tỉ lệ."


def rich(s, size=13):
    """`l_1` → chỉ số dưới; `10^{-12}` → số mũ."""
    s = _re.sub(r"\^\{([^}]*)\}", lambda m: f'<tspan dy="-5" font-size="{size - 3}">{m.group(1)}</tspan><tspan dy="5">​</tspan>', s)
    parts = _re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        out += f'<tspan dy="-4">{parts[i + 1]}</tspan>' if parts[i + 1] else '<tspan dy="-4">​</tspan>'
    return out


def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)


def spk(xc, y, size=1.0):
    """Loa nhìn nghiêng, miệng loa hướng xuống, đáy thân tại y."""
    return (f'<rect x="{xc - 9 * size:.1f}" y="{y - 22 * size:.1f}" width="{18 * size:.1f}" height="{12 * size:.1f}" fill="none" stroke="currentColor" stroke-width="2"/>'
            f'<path d="M{xc - 9 * size:.1f},{y - 10 * size:.1f} L{xc - 20 * size:.1f},{y:.1f} L{xc + 20 * size:.1f},{y:.1f} L{xc + 9 * size:.1f},{y - 10 * size:.1f} Z" fill="none" stroke="currentColor" stroke-width="2"/>')


def spk_r(x, y):
    """Loa nhìn nghiêng, miệng loa hướng sang phải, tâm miệng loa tại (x + 30, y)."""
    return (f'<rect x="{x}" y="{y - 9}" width="12" height="18" fill="none" stroke="currentColor" stroke-width="2"/>'
            f'<path d="M{x + 12},{y - 9} L{x + 30},{y - 22} L{x + 30},{y + 22} L{x + 12},{y + 9}" fill="none" stroke="currentColor" stroke-width="2"/>')


def brk(x, y1, y2, c=RED):
    """Dấu ngoặc đo đoạn ngắn (không đầu mũi tên)."""
    return seg(x, y1, x, y2, c, 2) + seg(x - 5, y1, x + 5, y1, c, 2) + seg(x - 5, y2, x + 5, y2, c, 2)


def tube(xc, ytop, ybot, w=44):
    return (seg(xc - w / 2, ytop, xc - w / 2, ybot, "currentColor", 2.6) + seg(xc + w / 2, ytop, xc + w / 2, ybot, "currentColor", 2.6)
            + seg(xc - w / 2, ybot, xc + w / 2, ybot, "currentColor", 2.6))


def water_static(xc, yw, ybot, w=44):
    return (f'<rect x="{xc - w / 2 + 1.3:.1f}" y="{yw:.1f}" width="{w - 2.6:.1f}" height="{ybot - yw - 1.3:.1f}" fill="{BLUE}" opacity=".35"/>'
            + seg(xc - w / 2 + 1.3, yw, xc + w / 2 - 1.3, yw, BLUE, 2.2))


def amp_curve(xc, y_ant, y_node, k, A=16, N=48):
    """Đường biên độ dao động của không khí (cam): bụng ở y_ant, nút ở y_node = y_ant + (2k+1)·λ/4."""
    Q = y_node - y_ant
    lam = 4 * Q / (2 * k + 1)
    pts_r = [(xc + A * abs(math.cos(2 * math.pi * (Q * i / N) / lam)), y_ant + Q * i / N) for i in range(N + 1)]
    pts_l = [(2 * xc - x, y) for x, y in pts_r]
    return poly(pts_r, ORG, 2, "", .95) + poly(pts_l, ORG, 2, "", .95)


# ───────────── Dạng 1 · mức cường độ âm L = 10 lg(I/I0); độ cao theo f, độ to theo L ─────────────
def d1(kk):
    b = defs("d1s" if kk == 2 else "d1") + spk_r(40, 95)
    # máy đo
    b += (f'<rect x="318" y="62" width="82" height="66" rx="8" fill="none" stroke="currentColor" stroke-width="2.4"/>'
          f'<rect x="328" y="72" width="62" height="26" rx="3" fill="none" stroke="{ORG}" stroke-width="1.8"/>')
    b += txt(359, 91, "L = ?", ORG, 15, "middle") + txt(359, 116, "dB", "currentColor", 13, "middle", "600")
    b += txt(359, 148, "máy đo", "currentColor", 13, "middle", "600") + txt(55, 140, "loa", "currentColor", 13, "middle", "600")
    if kk == 0:
        # sóng lan ra thẳng sang phải từ miệng loa: ba vòng cách đều, cùng tốc độ lan (R = c·(1 − s))
        cx, cy, c = 74, 95, 230.0
        clip = '<clipPath id="d1c"><rect x="74" y="10" width="334" height="150"/></clipPath>'
        rings = ""
        for s_ in (0.0, 0.25, 0.5):
            R = c * (1 - s_)
            rings += (f'<circle cx="{cx}" cy="{cy}" r="{R:.1f}" fill="none" stroke="{BLUE}" stroke-width="3" opacity=".75">'
                      f'<animate attributeName="r" values="0;0;{R:.1f}" keyTimes="0;{s_};1" dur="3.5s" begin="indefinite" fill="freeze"/></circle>')
        b += clip + f'<g clip-path="url(#d1c)">{rings}</g>'
        return fig("d1-0", "0 0 420 170", "Loa phát âm, các vòng sóng lan tới máy đo mức cường độ âm", b,
                   "Mô phỏng: loa phát âm, sóng âm lan tới máy đo (chạy chậm hơn thật nhiều lần). " + NOTE)
    b += txt(55, 156, "800 Hz", BLUE, 13, "middle") + txt(359, 36, "I = 4,0·10^{-7}", "currentColor", 13, "middle") + txt(359, 52, "W/m²", "currentColor", 13, "middle")
    b += txt(20, 14, "Cần tìm: L, L′, I, cảm giác của tai", ORG, 13)
    return fig("d1-2", "0 0 420 170", "Loa phát âm 800 hertz, máy đo ghi cường độ âm 4,0 nhân 10 mũ âm 7 oát trên mét vuông, cần tìm mức cường độ âm", b,
               "Dữ kiện: tần số của loa và cường độ âm đo được; chưa biết mức cường độ âm. " + NOTE)


# ───────────── Dạng 2 · dự đoán vị trí cộng hưởng: l + e = (2k+1)λ/4 ─────────────
def d2(kk):
    if kk == 0:
        # số liệu MẪU: f = 500 Hz, 20 °C (v = 343 m/s, λ = 68,6 cm), e = 0,5 cm; hạ nước 10 cm/s
        xc, yt, sc, yb = 190, 60, 2.8, 250
        L1 = 68.6 / 4 - 0.5; L2 = 3 * 68.6 / 4 - 0.5
        y1, y2, yend = yt + L1 * sc, yt + L2 * sc, yt + 58 * sc
        dur = 5.8
        b = defs("d2") + spk(xc, 40) + tube(xc, yt, yb)
        b += (f'<rect x="{xc - 22 + 1.3:.1f}" y="{yend:.1f}" width="{44 - 2.6:.1f}" height="{yb - yend - 1.3:.1f}" fill="{BLUE}" opacity=".35">'
              f'<animate attributeName="y" values="{yt};{yend:.1f}" dur="{dur}s" begin="indefinite" fill="freeze"/>'
              f'<animate attributeName="height" values="{yb - yt - 1.3:.1f};{yb - yend - 1.3:.1f}" dur="{dur}s" begin="indefinite" fill="freeze"/></rect>')
        for n, (yy, tt) in enumerate(((y1, L1 / 58), (y2, L2 / 58)), 1):
            b += (f'<g opacity="1"><animate attributeName="opacity" values="0;1" keyTimes="0;{tt:.3f}" calcMode="discrete" dur="{dur}s" begin="indefinite" fill="freeze"/>'
                  + seg(xc + 22, yy, xc + 38, yy, ORG, 2.2) + txt(xc + 44, yy + 5, f"nghe to nhất lần {n}", ORG, 13) + '</g>')
        b += arrow("", "b", 80, 100, 80, 170, 2) + txt(80, 190, "hạ nước", BLUE, 13, "middle") + txt(xc - 30, 30, "loa", "currentColor", 13, "end", "600")
        return fig("d2-0", "0 0 420 262", "Ống thẳng đứng đáy có nước, loa đặt trên miệng ống; mặt nước hạ dần và hai lần nghe to nhất được đánh dấu", b,
                   "Mô phỏng: hạ nước dần, đánh dấu hai lần nghe to nhất đầu tiên. Số liệu mẫu (500 Hz, 20 °C), không phải số của đề. " + NOTE)
    xc, yt, yw, yb = 150, 70, 170, 235
    ya = yt - 14                                # bụng cao hơn miệng ống đoạn e (vẽ phóng to)
    b = defs("d2s") + spk(xc, 44) + tube(xc, yt, yb) + water_static(xc, yw, yb) + amp_curve(xc, ya, yw, 0)
    b += seg(xc - 26, ya, xc + 26, ya, RED, 1.6, "5 4")
    b += dim_v(214, yt, yw, "l_1 = ?", 222, (yt + yw) / 2 + 5) + brk(262, ya, yt) + txt(272, ya + 11, "e", RED, 13)
    b += dim_v(100, ya, yw, "", 0, 0) + txt(94, (ya + yw) / 2 + 5, "λ/4", GRN, 13, "end")
    b += txt(xc + 32, ya + 4, "bụng", RED, 13) + txt(xc + 28, yw + 22, "nút (mặt nước)", BLUE, 13)
    b += txt(xc - 30, 30, "loa", "currentColor", 13, "end", "600") + txt(300, 30, "f = 600 Hz", "currentColor", 13) + txt(300, 48, "t = 15 °C", "currentColor", 13)
    b += txt(20, 256, "Cần tìm: v, λ, l_1, l_2, lần thứ ba?", ORG, 13)
    return fig("d2-2", "0 0 420 266", "Ống thẳng đứng đáy có nước, mặt nước là nút, bụng cao hơn miệng ống đoạn e; chiều dài cột khí l một và một phần tư bước sóng", b,
               "Lần cộng hưởng đầu tiên: từ nút (mặt nước) tới bụng là một đoạn ngắn nhất; bụng cao hơn miệng ống đoạn e (vẽ phóng to). " + NOTE)


def dim_v(x, y1, y2, label, lx, ly, anchor="start", c="o"):
    out = arrow("", c, x, y1, x, y2, 1.8) + arrow("", c, x, y2, x, y1, 1.8)
    return out + (txt(lx, ly, label, {"b": BLUE, "o": ORG, "r": RED, "g": GRN}[c], 13, anchor) if label else "")


# ───────────── Dạng 3 · từ l1, l2 tính λ, v, e; so với v theo nhiệt độ ─────────────
def d3(kk):
    if kk == 0:
        # mô phỏng: độ to nghe được theo l (số liệu mẫu 500 Hz, 20 °C: cộng hưởng ở 16,7 và 51,0 cm)
        x0, y0, sx, H = 40, 170, 5.0, 100
        def g(l):
            h = lambda c: 1 / (1 + ((l - c) / 2.2) ** 2)
            return 0.07 + 0.93 * min(1.0, h(16.7) + h(51.0))
        pts = [(x0 + sx * l, y0 - H * g(l)) for l in [i * 70 / 140 for i in range(141)]]
        run = [(x0 + sx * l, y0 - H * g(l)) for l in [i * 68 / 100 for i in range(101)]]
        b = defs("d3") + seg(x0, y0, 400, y0, "currentColor", 2) + seg(x0, y0, x0, 40, "currentColor", 2)
        for l in (0, 20, 40, 60):
            b += seg(x0 + sx * l, y0, x0 + sx * l, y0 + 6, "currentColor", 2) + txt(x0 + sx * l, y0 + 22, str(l), "currentColor", 12, "middle", "600")
        b += txt(400, y0 + 40, "l (cm)", "currentColor", 13, "end") + txt(x0 + 8, 40, "độ to nghe được", ORG, 13)
        b += poly(pts, GRN, 2.4)
        xs = [p[0] for p in run]; ys = [p[1] for p in run]
        b += (f'<circle cx="{xs[-1]:.1f}" cy="{ys[-1]:.1f}" r="6" fill="{ORG}" stroke="currentColor" stroke-width="1.5">'
              f'{smil("cx", xs, 5.0)}{smil("cy", ys, 5.0)}</circle>')
        return fig("d3-0", "0 0 420 214", "Đồ thị độ to nghe được theo chiều dài cột khí, có hai đỉnh, một chấm chạy dọc đường cong", b,
                   "Mô phỏng: hạ nước dần (l tăng), độ to nghe được thay đổi. Số liệu mẫu (500 Hz, 20 °C), không phải số của đề. " + NOTE)
    # hình dữ kiện: hai lần cộng hưởng k = 0 và k = 1 (tỉ lệ λ/4 : 3λ/4 theo lý thuyết, e vẽ phóng to)
    yt, yb = 52, 244
    ya = yt - 12
    Q1, Q2 = 56, 168
    b = defs("d3s")
    for xc, Q, k, nm, lab in ((100, Q1, 0, "lần 1 (k = 0)", "l_1 = 13,0 cm"), (270, Q2, 1, "lần 2 (k = 1)", "l_2 = 39,9 cm")):
        yw = ya + Q
        b += tube(xc, yt, yb) + water_static(xc, yw, yb) + amp_curve(xc, ya, yw, k) + seg(xc - 26, ya, xc + 26, ya, RED, 1.6, "5 4")
        b += dim_v(xc + 40, yt, yw, "", 0, 0) + txt(xc + 48, (yt + yw) / 2 + 5, lab, ORG, 13) + txt(xc, 22, nm, "currentColor", 13, "middle")
    b += txt(100 - 30, ya + 4, "e", RED, 13, "end") + txt(14, 262, "Cần tìm: λ, v, e, độ lệch so với v theo nhiệt độ", ORG, 13)
    return fig("d3-2", "0 0 420 270", "Hai ống: lần cộng hưởng thứ nhất ứng với một phần tư bước sóng, lần thứ hai ứng với ba phần tư bước sóng", b,
               "Dữ kiện: l₁ và l₂ của hai lần nghe to nhất liên tiếp; bụng cao hơn miệng ống đoạn e (vẽ phóng to). " + NOTE)


# ───────────── Dạng 4 · xử lý bảng số liệu, sai số, so với giá trị tham khảo ─────────────
def d4(kk):
    if kk == 0:
        # mô phỏng: 5 lần đo hiện dần trên trục v, rồi khoảng v ± Δv, giá trị tham khảo (số mẫu)
        x0, y0, s = 30, 126, 12.0
        px = lambda v: x0 + (v - 330) * s
        b = defs("d4") + seg(x0, y0, 400, y0, "currentColor", 2)
        for v in (330, 340, 350, 360):
            b += seg(px(v), y0, px(v), y0 + 6, "currentColor", 2) + txt(px(v), y0 + 22, str(v), "currentColor", 12, "middle", "600")
        b += txt(400, y0 + 40, "v (m/s)", "currentColor", 13, "end")
        dots = (338, 341, 343, 339, 340)
        mean = sum(dots) / 5; half = 3.0
        bx0, bw = px(mean - half), 2 * half * s
        b += (f'<rect x="{bx0:.1f}" y="64" width="{bw:.1f}" height="12" fill="{ORG}" opacity=".85">'
              f'<animate attributeName="x" values="{px(mean):.1f};{px(mean):.1f};{bx0:.1f}" keyTimes="0;0.6;1" dur="5s" begin="indefinite" fill="freeze"/>'
              f'<animate attributeName="width" values="0;0;{bw:.1f}" keyTimes="0;0.6;1" dur="5s" begin="indefinite" fill="freeze"/></rect>')
        b += txt(px(mean - half) - 8, 75, "v ± Δv", ORG, 13, "end")
        for n, v in enumerate(dots):
            t = 0.1 + 0.1 * n
            b += (f'<circle cx="{px(v):.1f}" cy="104" r="5.5" fill="{GRN}" stroke="currentColor" stroke-width="1.5">'
                  f'<animate attributeName="opacity" values="0;1" keyTimes="0;{t:.2f}" calcMode="discrete" dur="5s" begin="indefinite" fill="freeze"/></circle>')
        b += seg(px(342), 40, px(342), y0, RED, 2, "6 4") + txt(px(342) + 6, 36, "v tham khảo", RED, 13)
        b += txt(x0, 98, "5 lần đo", GRN, 13)
        return fig("d4-0", "0 0 420 176", "Trục tốc độ âm: năm lần đo hiện dần, rồi khoảng giá trị trung bình cộng trừ sai số, và vạch giá trị tham khảo", b,
                   "Mô phỏng: các lần đo hiện dần, rồi khoảng v ± Δv, so với vạch tham khảo. Số liệu mẫu, không phải số của đề. " + NOTE)
    b = defs("d4s")
    BW, BH = 112, 46
    xs = (10, 150, 290)
    rows = ((14, BLUE, (("Trung bình", "l_1 và l_2"), ("Bước sóng", "λ"), ("Tốc độ", "v = λ f"))),
            (84, ORG, (("Sai số mỗi l", "Δl_1, Δl_2"), ("Sai số của λ", "Δλ"), ("Sai số của v", "Δv"))))
    for y, c, cells in rows:
        for i, (a, bb) in enumerate(cells):
            x = xs[i]
            b += f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" fill="none" stroke="{c}" stroke-width="2"/>'
            b += txt(x + BW / 2, y + 19, a, "currentColor", 13, "middle", "600") + txt(x + BW / 2, y + 37, bb, c, 13, "middle")
            if i < 2:
                b += arrow("", "b" if c == BLUE else "o", x + BW + 3, y + BH / 2, xs[i + 1] - 3, y + BH / 2, 2)
    b += f'<rect x="40" y="170" width="340" height="46" rx="6" fill="none" stroke="{GRN}" stroke-width="2"/>'
    b += txt(210, 189, "Kết quả v = v̄ ± Δv", "currentColor", 13, "middle", "600") + txt(210, 207, "so với giá trị tham khảo ở nhiệt độ phòng", GRN, 13, "middle")
    b += arrow("", "b", 346, 14 + BH + 2, 346, 82, 2) + arrow("", "o", 346, 84 + BH + 2, 346, 168, 2)
    b += txt(14, 240, "Cần tìm: v̄, Δv, kết luận", ORG, 13)
    return fig("d4-2", "0 0 420 250", "Sơ đồ xử lý số liệu: trung bình hai vị trí, bước sóng, tốc độ, rồi sai số từng bước và so với giá trị tham khảo", b,
               "Dữ kiện: thứ tự xử lý số liệu; chưa có số nào của kết quả. " + NOTE)
