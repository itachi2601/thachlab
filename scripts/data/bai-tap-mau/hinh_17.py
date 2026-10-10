"""Hình cho bài tập mẫu Bài 16 (Vật lí 12) "Phản ứng phân hạch, phản ứng nhiệt hạch và ứng dụng", lesson_id 17.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mô phỏng chỉ vẽ dữ kiện của đề; mọi đại lượng/hạt cần tìm ghi "?" (không lộ đáp số). Vẽ sơ đồ, không đúng tỉ lệ kích thước hạt nhân."""
import math, os, random, re as _re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Sơ đồ minh hoạ, kích thước hạt không đúng tỉ lệ."
GREY = "#94a3b8"
INK = "#0f172a"


def rich(s, size=13):
    """`m_X` → m với chỉ số dưới X."""
    parts = _re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
    return out

def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)

def kf(attr, vals, kts, dur, tr=False):
    """<animate> có keyTimes; tr=True → animateTransform translate (vals là cặp (x,y))."""
    kt = ";".join(f"{k:g}" for k in kts)
    if tr:
        v = ";".join(f"{a:.1f} {b:.1f}" for a, b in vals)
        return (f'<animateTransform attributeName="transform" type="translate" values="{v}" keyTimes="{kt}" dur="{dur}s" '
                f'begin="indefinite" fill="freeze"/>')
    v = ";".join(f"{a:g}" if isinstance(a, (int, float)) else str(a) for a in vals)
    return f'<animate attributeName="{attr}" values="{v}" keyTimes="{kt}" dur="{dur}s" begin="indefinite" fill="freeze"/>'

def part(x, y, r, fill, label, size=11, track=None, op=None, dur=4, dash=False, lc=INK, extra=""):
    """Hạt/hạt nhân là hình tròn bán kính r tại (x,y) có nhãn ở giữa. track = [(kt, x, y)…], op = [(kt, v)…] khi chạy mô phỏng."""
    st = f'stroke="currentColor" stroke-width="1.4"' + (' stroke-dasharray="4 3"' if dash else "")
    inner = (f'<circle r="{r}" fill="{fill}" {st}/>'
             + (f'<text y="{4 if size >= 11 else 3.5}" text-anchor="middle" font-size="{size}" font-weight="700" fill="{lc}">{label}</text>' if label else "") + extra)
    x0, y0 = (track[0][1], track[0][2]) if track else (x, y)
    o0 = op[0][1] if op else 1
    anim = ""
    if track and len(track) > 1:
        anim += kf("", [(p[1], p[2]) for p in track], [p[0] for p in track], dur, tr=True)
    if op and len(op) > 1:
        anim += kf("opacity", [p[1] for p in op], [p[0] for p in op], dur)
    return f'<g transform="translate({x0:.1f} {y0:.1f})" opacity="{o0}">{anim}{inner}</g>'

# ───────────── Dạng 1 · ba thế hệ nơtron 50 000; 50 100; 50 200 ─────────────
def d1(kk):
    anim = kk == 0
    N = [50000, 50200, 50400]; x0, WM = 118, 214
    b = txt(16, 22, "Ba thế hệ nơtron liên tiếp trong lò", "currentColor", 13)
    stage = [(0, 0.3), (0.3, 0.65), (0.65, 1.0)]
    for i, n in enumerate(N):
        y = 42 + i * 50; w = WM * n / N[-1]; s, e = stage[i]
        b += txt(16, y + 18, f"Thế hệ {i + 1}", "currentColor", 13)
        num = f"{n:,}".replace(",", " ")
        if anim:
            b += f'<rect x="{x0}" y="{y}" width="0" height="26" rx="3" fill="{BLUE}" opacity=".85">{kf("width", [0, 0, w, w], [0, s, e, 1], 4)}</rect>'
            b += f'<g opacity="0">{kf("opacity", [0, 0, 1, 1], [0, e, min(e + 0.05, 1), 1], 4)}{txt(x0 + w + 6, y + 18, num, "currentColor", 13)}</g>'
        else:
            b += f'<rect x="{x0}" y="{y}" width="{w:.1f}" height="26" rx="3" fill="{BLUE}" opacity=".85"/>' + txt(x0 + w + 6, y + 18, num, "currentColor", 13)
        if i < 2:
            if anim:
                b += f'<g opacity="0">{kf("opacity", [0, 0, 1, 1], [0, e, min(e + 0.05, 1), 1], 4)}{txt(x0, y + 44, "↓ nhân với k = ?", ORG, 12, "start", "700")}</g>'
            else:
                b += txt(x0, y + 44, "↓ nhân với k = ?", ORG, 12, "start", "700")
    cap = "Thanh vẽ đúng tỉ lệ với số nơtron (trục bắt đầu từ 0)."
    if anim:
        return fig("d1-0", "0 0 420 200", "Ba thế hệ nơtron liên tiếp hiện lần lượt thành ba thanh có số nơtron ghi bên phải", b,
                   "Mô phỏng: ba thế hệ nơtron hiện lần lượt trong 4 s. " + cap)
    return fig("d1-2", "0 0 420 200", "Dữ kiện: số nơtron của ba thế hệ liên tiếp, hệ số nhân cần tìm", b, "Dữ kiện: số nơtron ba thế hệ liên tiếp; hệ số nhân k chưa biết. " + cap)


# ───────────── Dạng 2 · phân hạch cho Xe-139 + Sr-95 + x n; D + D → He-3 + X ─────────────
def d2(kk):
    anim = kk == 0
    ya, yb = 62, 152
    b = txt(16, 20, "(1) n + U-235 → Xe-139 + Sr-95 + x n", "currentColor", 12) + txt(16, 108, "(2) D + D → He-3 + X", "currentColor", 12)
    D = 4
    if anim:
        b += part(0, 0, 5, BLUE, "", track=[(0, 30, ya), (0.38, 112, ya), (0.4, 112, ya), (1, 112, ya)], op=[(0, 1), (0.38, 1), (0.4, 0), (1, 0)])
        b += part(140, ya, 21, GREY, "U", 12, op=[(0, 1), (0.4, 1), (0.42, 0), (1, 0)])
        b += part(0, 0, 16, ORG, "Xe", 12, track=[(0, 140, ya), (0.42, 140, ya), (1, 250, ya - 22)], op=[(0, 0), (0.4, 0), (0.42, 1), (1, 1)])
        b += part(0, 0, 13, GRN, "Sr", 12, track=[(0, 140, ya), (0.42, 140, ya), (1, 250, ya + 24)], op=[(0, 0), (0.4, 0), (0.42, 1), (1, 1)])
        b += part(340, ya, 22, "none", "x n", 12, dash=True, lc="currentColor", op=[(0, 0), (0.6, 0), (1, 1)])
        b += part(0, 0, 10, RED, "D", 11, track=[(0, 50, yb), (0.38, 120, yb), (1, 120, yb)], op=[(0, 1), (0.38, 1), (0.4, 0), (1, 0)])
        b += part(0, 0, 10, RED, "D", 11, track=[(0, 190, yb), (0.38, 130, yb), (1, 130, yb)], op=[(0, 1), (0.38, 1), (0.4, 0), (1, 0)])
        b += part(0, 0, 14, ORG, "He", 11, track=[(0, 125, yb), (0.42, 125, yb), (1, 250, yb - 16)], op=[(0, 0), (0.4, 0), (0.42, 1), (1, 1)])
        b += part(0, 0, 14, "none", "X?", 12, dash=True, lc="currentColor", track=[(0, 125, yb), (0.42, 125, yb), (1, 335, yb + 6)], op=[(0, 0), (0.4, 0), (0.42, 1), (1, 1)])
        return fig("d2-0", "0 0 420 200", "Phản ứng phân hạch và phản ứng hai hạt đơteri: nơtron bắn vào urani, hai hạt đơteri va chạm, sản phẩm bay ra, số nơtron và hạt X chưa biết", b,
                   "Mô phỏng: hai phản ứng trong 4 s; số nơtron x ở (1) và hạt X ở (2) để dấu hỏi. " + NOTE)
    # hình dữ kiện: số khối A và số prôtôn Z đã cho của từng hạt
    def nuc(x, y, r, c, name, A, Z):
        s = part(x, y, r, c, name, 12)
        return s + txt(x, y + r + 14, f"A = {A}", "currentColor", 11, "middle", "400") + txt(x, y + r + 26, f"Z = {Z}", "currentColor", 11, "middle", "400")
    sa, sb = 48, 150
    b = txt(16, 20, "(1) n + U-235 → Xe-139 + Sr-95 + x n", "currentColor", 12) + txt(16, 116, "(2) D + D → He-3 + X", "currentColor", 12)
    b += part(36, sa, 5, BLUE, "") + txt(36, sa + 20, "A=1, Z=0", "currentColor", 11, "middle", "400")
    b += nuc(110, sa, 20, GREY, "U", 235, 92) + nuc(210, sa, 16, ORG, "Xe", 139, 54) + nuc(285, sa, 13, GRN, "Sr", 95, 38)
    b += part(358, sa, 20, "none", "x n", 12, dash=True, lc="currentColor") + txt(358, sa + 36, "x = ?", ORG, 12, "middle")
    b += nuc(60, sb, 10, RED, "D", 2, 1) + nuc(130, sb, 10, RED, "D", 2, 1) + nuc(240, sb, 14, ORG, "He", 3, 2)
    b += part(330, sb, 14, "none", "X?", 12, dash=True, lc="currentColor") + txt(330, sb + 36, "A = ?  Z = ?", ORG, 11, "middle")
    return fig("d2-2", "0 0 420 200", "Dữ kiện: số khối A và số prôtôn Z của các hạt đã biết; số nơtron x và hạt X chưa biết", b,
               "Dữ kiện: số khối A, số prôtôn Z của từng hạt đã cho; x và hạt X chưa biết. " + NOTE)


# ───────────── Dạng 3 · D + T → He + n ; N + He → O + p, khối lượng cho trước ─────────────
def d3(kk):
    anim = kk == 0
    y = 100
    if anim:
        b = txt(16, 22, "(1) D + T → He + n", "currentColor", 13)
        b += part(0, 0, 11, RED, "D", 12, track=[(0, 50, y), (0.45, 175, y), (1, 175, y)], op=[(0, 1), (0.45, 1), (0.47, 0), (1, 0)])
        b += part(0, 0, 14, BLUE, "T", 12, track=[(0, 370, y), (0.45, 205, y), (1, 205, y)], op=[(0, 1), (0.45, 1), (0.47, 0), (1, 0)])
        b += part(0, 0, 14, ORG, "He", 12, track=[(0, 190, y), (0.47, 190, y), (1, 110, y - 52)], op=[(0, 0), (0.45, 0), (0.47, 1), (1, 1)])
        b += part(0, 0, 7, GRN, "n", 10, track=[(0, 190, y), (0.47, 190, y), (1, 330, y - 58)], op=[(0, 0), (0.45, 0), (0.47, 1), (1, 1)])
        b += f'<g opacity="0">{kf("opacity", [0, 0, 1], [0, 0.7, 1], 4)}{txt(210, 180, "Δm = ?    W = ?", ORG, 14, "middle")}</g>'
        return fig("d3-0", "0 0 420 200", "Hạt đơteri và hạt triti lao vào nhau rồi tạo ra hạt heli và nơtron bay đi, độ hụt khối và năng lượng chưa biết", b,
                   "Mô phỏng: phản ứng (1) trong 4 s; hai hạt sau phản ứng bay ra với động năng. " + NOTE)
    b = txt(16, 20, "(1) D + T → He + n", "currentColor", 12)
    xs = [(50, RED, "D", 11, "2,013553"), (150, BLUE, "T", 14, "3,015501"), (270, ORG, "He", 14, "4,001506"), (362, GRN, "n", 8, "1,008665")]
    for i, (x, c, nm, r, m) in enumerate(xs):
        b += part(x, 52, r, c, nm, 12) + txt(x, 86, m + " u", "currentColor", 11, "middle", "400")
    b += txt(100, 57, "+", "currentColor", 18, "middle") + txt(210, 57, "→", "currentColor", 20, "middle") + txt(316, 57, "+", "currentColor", 18, "middle")
    b += txt(16, 118, "(2) N + He → O + p", "currentColor", 12)
    ys = [(36, GREY, "N", 17, "13,999231"), (130, ORG, "He", 14, "4,001506"), (262, GRN, "O", 16, "16,994740"), (362, RED, "p", 10, "1,007276")]
    for i, (x, c, nm, r, m) in enumerate(ys):
        b += part(x, 152, r, c, nm, 12) + txt(x, 186, m + " u", "currentColor", 11, "middle", "400")
    b += txt(83, 157, "+", "currentColor", 18, "middle") + txt(196, 157, "→", "currentColor", 20, "middle") + txt(316, 157, "+", "currentColor", 18, "middle")
    return fig("d3-2", "0 0 420 200", "Dữ kiện: khối lượng các hạt nhân của hai phản ứng", b, "Dữ kiện: khối lượng hạt nhân (đơn vị u) của từng hạt. " + NOTE)


# ───────────── Dạng 4 · 1,0 g đơteri (M = 2,0 g/mol), mỗi hạt D tham gia một phản ứng D–T ─────────────
def d4(kk):
    anim = kk == 0
    rnd = random.Random(7)
    bx, by, bw, bh = 24, 52, 150, 100
    b = f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="none" stroke="currentColor" stroke-width="2.4"/>'
    b += txt(bx, 36, "1,0 g đơteri (D)", "currentColor", 13) + txt(bx, 176, "N phản ứng = ?", ORG, 13)
    for i in range(24):
        x = rnd.uniform(bx + 12, bx + bw - 12); yy = rnd.uniform(by + 12, by + bh - 12)
        if anim:
            t = round(rnd.uniform(0.15, 0.9), 2)
            b += (f'<circle cx="{x:.0f}" cy="{yy:.0f}" r="5.5" fill="{GREY}"><animate attributeName="fill" values="{GREY};{ORG};{ORG}" keyTimes="0;{t};1" '
                  f'calcMode="discrete" dur="4s" begin="indefinite" fill="freeze"/></circle>')
        else:
            b += f'<circle cx="{x:.0f}" cy="{yy:.0f}" r="5.5" fill="{GREY}"/>'
    ex, ey, eh = 250, 52, 100
    b += f'<rect x="{ex}" y="{ey}" width="40" height="{eh}" rx="4" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    if anim:
        b += f'<rect x="{ex + 2}" y="{ey + eh - 2}" width="36" height="1" fill="{ORG}">{smil("y", [ey + eh - 2, ey + 22], 4)}{smil("height", [1, eh - 24], 4)}</rect>'
    else:
        b += txt(ex + 20, ey + 56, "?", ORG, 22, "middle")
    b += txt(ex + 20, 36, "E toả ra = ?", ORG, 13, "middle") + txt(ex + 20, 176, "so với than đá", "currentColor", 12, "middle", "400")
    b += txt(304, 76, "D + T → He + n", "currentColor", 12, "start", "400") + txt(304, 94, "17,6 MeV", "currentColor", 12, "start", "400")
    b += txt(304, 110, "mỗi phản ứng", "currentColor", 12, "start", "400") + txt(304, 136, "than: 2,7·10⁷ J/kg", "currentColor", 12, "start", "400")
    if anim:
        return fig("d4-0", "0 0 420 200", "Các hạt nhân đơteri trong mẫu lần lượt tham gia phản ứng, thanh năng lượng toả ra dâng dần", b,
                   "Mô phỏng: từng hạt đơteri (rút gọn còn 24 chấm) lần lượt phản ứng trong 4 s, thanh năng lượng dâng lên. " + NOTE)
    return fig("d4-2", "0 0 420 200", "Dữ kiện: mẫu một gam đơteri, năng lượng mỗi phản ứng và năng suất toả nhiệt của than", b,
               "Dữ kiện: khối lượng đơteri, năng lượng mỗi phản ứng, năng suất toả nhiệt của than. " + NOTE)


# ───────────── Dạng 5 · lò 900 MW chạy 30 ngày: diện tích dưới đường P(t) là năng lượng ─────────────
def d5(kk):
    anim = kk == 0
    X0, X1, Y0, Y1 = 62, 322, 150, 52              # trục t: 0–30 ngày; trục P: 0–900 MW
    px = lambda t: X0 + (X1 - X0) * t / 30
    py = lambda p: Y0 - (Y0 - Y1) * p / 900
    b = seg(X0, Y0, X1 + 10, Y0, "currentColor", 2) + seg(X0, Y0, X0, 36, "currentColor", 2)
    for t in (0, 10, 20, 30):
        b += seg(px(t), Y0, px(t), Y0 + 5, "currentColor", 1.6) + txt(px(t), Y0 + 20, str(t), "currentColor", 12, "middle", "400")
    for p in (0, 300, 600, 900):
        b += seg(X0 - 5, py(p), X0, py(p), "currentColor", 1.6) + txt(X0 - 8, py(p) + 4, str(p), "currentColor", 12, "end", "400")
    b += txt(X1 + 10, Y0 + 38, "t (ngày)", "currentColor", 12, "end", "400") + txt(X0 + 6, 32, "P (MW)", "currentColor", 12, "start", "400")
    w = X1 - X0
    if anim:
        b += f'<rect x="{X0}" y="{py(900):.1f}" width="1" height="{Y0 - py(900):.1f}" fill="{ORG}" opacity=".35">{smil("width", [1, w], 4)}</rect>'
    else:
        b += f'<rect x="{X0}" y="{py(900):.1f}" width="{w}" height="{Y0 - py(900):.1f}" fill="{ORG}" opacity=".35"/>'
    b += seg(X0, py(900), X1, py(900), BLUE, 2.4)
    b += f'<g opacity="{0 if anim else 1}">' + (kf("opacity", [0, 0, 1], [0, 0.8, 1], 4) if anim else "") + txt((X0 + X1) / 2, 108, "E = ?", "currentColor", 16, "middle") + "</g>"
    b += txt(X1 + 20, py(900) + 4, "P = 900 MW", BLUE, 12, "start") + txt(X1 + 20, 110, "200 MeV", "currentColor", 12, "start", "400") + txt(X1 + 20, 126, "mỗi phân hạch", "currentColor", 12, "start", "400")
    b += txt(16, 188, "than đá: 2,7·10⁷ J/kg", "currentColor", 12, "start", "400")
    if anim:
        return fig("d5-0", "0 0 420 200", "Đồ thị công suất không đổi theo thời gian, phần tô màu dưới đồ thị lớn dần theo ngày chạy của lò", b,
                   "Mô phỏng: lò chạy liên tục 30 ngày trong 4 s; phần tô màu dưới đường công suất lớn dần theo thời gian. " + NOTE)
    return fig("d5-2", "0 0 420 200", "Dữ kiện: công suất nhiệt không đổi 900 MW trong 30 ngày, năng lượng mỗi phân hạch, năng suất toả nhiệt của than", b,
               "Dữ kiện: công suất, thời gian chạy, năng lượng mỗi phân hạch, năng suất toả nhiệt của than. " + NOTE)
