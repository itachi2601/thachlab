"""CĐ09 Năng lượng với cuộc sống (bài 163): kiểm số liệu trong theory.src.html, sinh 4 hình SVG,
thay <!--FIGn--> -> theory.html (chạy lại được).
Chạy: python3 content/hsg9/cd09-nang-luong-cuoc-song/build_figs.py"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "soan-bai-ly-thuyet-tuong-tac", "scripts"))
from svg_lib import RED, BLUE, ORG, GRN, text, wrap, chevron

PHUT = 18
GRAY = "rgba(148,163,184,.25)"
KWH = 3.6e6


def near(a, b, tol=0.005):
    return abs(a - b) <= tol * max(abs(b), 1e-12)


# ═════════ Kiểm số liệu dùng trong bài (mọi số trong theory.src.html) ═════════
# Mục II: ví dụ nhanh nhà máy than
assert near(0.88 * 0.40 * 0.95, 0.3344)
# q1: máy bơm 85/90/70
H = 0.85 * 0.9 * 0.7
assert near(H, 0.5355) and near((0.85 + 0.9 + 0.7) / 3, 0.8167, 0.001)
# Bài toán mẫu: diesel 38 % x 92 %, 46 kW x 10 h
H = 0.38 * 0.92
A = 46e3 * 10 * 3600
Atp = A / H
m = Atp / 4.4e7
assert near(H, 0.3496) and near(A, 1.656e9) and near(Atp, 4.74e9, 0.002)
assert near(m, 107.7, 0.001) and near(m / 0.84, 128, 0.002) and near(3.2 * m, 344, 0.003)
assert near(460 / (m / 0.84), 3.6, 0.01) and near(0.84 * 4.4e7 / KWH, 10.3, 0.005)
H2 = 0.42 * 0.92
m2 = A / H2 / 4.4e7
assert near(H2, 0.3864) and near(m2, 97.4, 0.001) and near(m - m2, 10.3, 0.005) and near((m - m2) / m, 0.095, 0.01)
# Mục III: công suất bức xạ tới Trái Đất
P = 1360 * math.pi * 6.4e6 ** 2
assert near(P, 1.75e17, 0.002) and 8500 < P / 2e13 < 9000
# q5: 20 L xăng
assert near(20 * 0.70, 14) and near(3.2 * 14, 44.8) and near(20 * 3.2, 64) and near(14 / 3.2, 4.375)
# q6: thuỷ điện 50 m, 40 m3/s, 90 %
Pn = 1e4 * 40 * 50
assert Pn == 2e7 and near(0.9 * Pn, 18e6) and near(0.9 * 1000 * 40 * 50, 1.8e6) and near(Pn / 0.9, 22.2e6, 0.002)
# Thí nghiệm pin mini: S = 0,006 m2, I = 800 W/m2
Pt = 800 * 0.10 * 0.06
assert near(Pt, 4.8)
Hs = [u * i / Pt for u, i in ((2.40, 0.37), (2.38, 0.36), (2.42, 0.38))]
assert all(abs(h * 100 - t) <= 0.051 for h, t in zip(Hs, (18.5, 17.9, 19.2))), Hs
assert near(sum(Hs) / 3, 0.185, 0.005) and near(max(Hs) - min(Hs), 0.013, 0.05)
# q7: hộ 7 kWh/ngày, tấm 1,6 m2, 21 %, 5 h
Pd = 0.21 * 1000 * 1.6
assert near(Pd, 336) and near(Pd * 5 / 1000, 1.68)
n = 7 / 1.68
assert 4 < n < 5 and math.ceil(n) == 5 and near(4 * 1.68, 6.72)
assert math.ceil(7 / (Pd * 12 / 1000)) == 2 and math.ceil(7 / (1.6 * 5)) == 1
# q8: 6 -> 9 m/s;  q9: 3 MW tại 12 m/s, gió 18 m/s
assert near((9 / 6) ** 3, 3.375) and near((9 / 6) ** 2, 2.25)
assert near(3 * (18 / 12) ** 3, 10.1, 0.003) and near(3 * 18 / 12, 4.5)
# Thử thách 1, 2, 3
assert near(0.8 * 1e4 * 2 * 20, 320e3)
p8 = 1.5 * (8 / 12) ** 3
assert near(p8, 0.444, 0.002) and near(10 * p8 + 6 * 1.5, 13.4, 0.005)
assert near(10 * p8 + 6 * 1.5 * (14 / 12) ** 3, 18.7, 0.005)
pin = 0.2 * 1000 * 1e4 * 4 / 1000            # kWh/ngày
sk = 0.25 * 2e4 * 1.6e7
assert near(pin, 8000) and near(pin * 365, 2.92e6) and near(sk, 8e10) and near(sk / KWH, 2.22e4, 0.002)
assert 125 < pin * 365 / (sk / KWH) < 135
nang = 1000 * 1e4 * 4 * 3600 * 365
assert near(nang, 5.3e13, 0.01) and near(2e4 * 1.6e7 / nang, 0.006, 0.05)
# Hạt nhân: 1 g U-235 ≈ 3 tấn than
assert 2900 < 8.2e10 / 2.7e7 < 3100


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def rect(x, y, w, h, fill="none", c="currentColor", sw=2, rx=0, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" stroke-width="{sw}"{d}/>'


def arr(x1, y1, x2, y2, c="currentColor", w=2, L=10):
    return line(x1, y1, x2, y2, c, w) + chevron(x2, y2, x2 - x1, y2 - y1, c, w, L)


def rich(x, y, parts, c="currentColor", size=15, anchor="start", weight="700"):
    """Chữ có chỉ số dưới: parts = [("v", 0), ("kđ", 1)] — 1 là chỉ số dưới (cỡ 12, hạ 4)."""
    s, low = "", False
    for t, is_sub in parts:
        if is_sub and not low:
            s += f'<tspan font-size="12" dy="4">{t}</tspan>'
            low = True
        elif not is_sub and low:
            s += f'<tspan dy="-4">{t}</tspan>'
            low = False
        else:
            fs = ' font-size="12"' if is_sub else ""
            s += f'<tspan{fs}>{t}</tspan>'
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{s}</text>'


def box(cx, y, w, lines, col="currentColor", fill=GRAY, dash="", h=None):
    """Hộp chữ căn giữa tại cx, đỉnh y; mỗi phần tử của lines là một dòng."""
    h = h or 10 + 19 * len(lines)
    g = rect(cx - w / 2, y, w, h, fill, col, 1.8, 6, dash)
    for i, s in enumerate(lines):
        g += text(cx, round(y + 20 + 19 * i, 1), s, col, 15 if i == 0 else 14, "middle", "700" if i == 0 else "600")
    return g, y + h


# ═════════ Hình 1: dòng năng lượng qua nhà máy nhiệt điện (độ rộng tỉ lệ công suất, không ghi số) ═════════
H1, H2_, H3 = 0.88, 0.40, 0.95
K = 1.0                                   # px trên một đơn vị (100 đơn vị nhiên liệu)
w0 = 100 * K
w1 = w0 * H1
w2 = w1 * H2_
w3 = w2 * H3
YT = 56                                   # mép trên dải chính
XS = [20, 120, 210, 300, 392]             # đầu, lò hơi, tuabin, máy phát, cuối
b = ""
fills = ["rgba(251,146,60,.35)", "rgba(248,113,113,.30)", "rgba(56,189,248,.30)", "rgba(52,211,153,.35)"]
widths = [w0, w1, w2, w3]
for i in range(4):
    x_end = XS[i + 1] if i < 3 else XS[4] - 14
    b += rect(XS[i], YT, x_end - XS[i], widths[i], fills[i], "none", 0)
# mũi tên đầu ra (điện)
b += f'<path d="M{XS[4]-14},{YT-6} L{XS[4]},{YT + w3/2:.1f} L{XS[4]-14},{YT + w3 + 6:.1f} z" fill="{fills[3]}"/>'
# vạch chia khâu
for x in XS[1:4]:
    b += line(x, YT - 6, x, YT + 104, "currentColor", 1.4, "4 3", .8)
# nhãn khâu (trên dải)
for x, s in ((XS[1], "lò hơi"), (XS[2], "tuabin"), (XS[3], "máy phát")):
    b += text(x, YT - 14, s, "currentColor", 15, "middle", "700")
b += text(XS[0], YT - 14, "nhiên liệu", ORG, 15, "start", "700")
b += text(XS[4], YT + w3 + 26, "điện", GRN, 15, "end", "700")
# hao phí: dải nhiệt rẽ xuống, bề rộng = phần mất ở khâu đó
YB = 236
losses = [(XS[1], w0 - w1, "khói thải", "middle", 0), (XS[2], w1 - w2, "nước làm mát", "end", 26),
          (XS[3], w2 - w3, "dây quấn", "start", -6)]
for x, wl, lab, anc, dx in losses:
    wl_draw = max(wl, 3)
    y0 = YT + (w0 if x == XS[1] else (w1 if x == XS[2] else w2)) - wl
    b += rect(x + 2, y0, wl_draw, YB - y0, "rgba(248,113,113,.35)", "none", 0)
    cx = x + 2 + wl_draw / 2
    b += chevron(cx, YB + 8, 0, 1, RED, 2.4, 10)
    b += text(round(cx + dx, 1), YB + 30, lab, RED, 14, anc, "700")
    b += text(round(cx + dx, 1), YB + 48, "(nhiệt)", RED, 14, anc, "600")
assert w0 - w1 + w1 - w2 + w2 - w3 + w3 == w0
fig1 = wrap("0 28 400 268",
            "Sơ đồ dòng năng lượng qua nhà máy nhiệt điện: dải nhiên liệu đi qua lò hơi, tuabin, máy phát, mỗi khâu rẽ ra một dải nhiệt hao phí; dải rẽ ra ở tuabin rộng nhất",
            b, "Hình 1. Dòng năng lượng qua nhà máy nhiệt điện. Độ rộng dải tỉ lệ công suất.<br>Dải đỏ rẽ xuống: hao phí, thành nhiệt toả ra môi trường.<br>Dải rẽ ra ở tuabin rộng nhất.")

# ═════════ Hình 2: vòng năng lượng trên Trái Đất ═════════
b = ""
g, yb = box(110, 14, 180, ["Mặt Trời", "nhiệt hạch ở lõi"], ORG, "rgba(251,146,60,.20)")
b += g
b += arr(110, yb, 110, 104, ORG, 2.4)
b += text(118, 92, "bức xạ", ORG, 14, "start", "700")
g, yE = box(200, 106, 360, ["Trái Đất hấp thụ khoảng 70 %"], "currentColor", GRAY, h=34)
b += g
# về vũ trụ
b += arr(300, 106, 300, 40, BLUE, 2.2)
b += arr(350, 106, 350, 40, RED, 2.2)
b += text(296, 26, "phản xạ", BLUE, 14, "end", "700")
b += text(354, 26, "hồng ngoại", RED, 14, "middle", "700")
b += text(325, 62, "về", "currentColor", 14, "middle", "600")
b += text(325, 80, "vũ trụ", "currentColor", 14, "middle", "600")
# bốn nhánh
COLS = [(52, ["làm nóng", "không đều"], ["gió"], ["sóng biển"]),
        (148, ["bốc hơi,", "mưa"], ["thế năng", "nước"], ["thuỷ điện"]),
        (250, ["quang hợp"], ["sinh khối"], ["than, dầu,", "khí"]),
        (346, ["pin, bình", "nước nóng"], [], [])]
for cx, *levels in COLS:
    y = yE + 30
    b += arr(cx, yE, cx, y - 2, "currentColor", 1.8, 9)
    for k, lv in enumerate([l for l in levels if l]):
        if k:
            b += arr(cx, y - 26, cx, y - 2, "currentColor", 1.8, 9)
        g, y2 = box(cx, y, 88, lv, GRN if k == 0 else "currentColor", "rgba(52,211,153,.12)")
        b += g
        y = y2 + 26
# ba ngoại lệ (nét đứt)
YX = 386
b += text(200, YX - 12, "Không từ bức xạ Mặt Trời:", "currentColor", 15, "middle", "700")
for cx, l1, l2 in ((70, "địa nhiệt", "lòng đất nóng"), (200, "hạt nhân", "urani trong vỏ"), (330, "thuỷ triều", "lực hút")):
    g, _ = box(cx, YX, 124, [l1, l2], RED, "none", "6 4")
    b += g
fig2 = wrap("0 6 400 440",
            "Sơ đồ vòng năng lượng: Mặt Trời bức xạ tới Trái Đất; một phần phản xạ và bức xạ hồng ngoại về vũ trụ; phần hấp thụ đi theo các nhánh gió và sóng biển, bốc hơi mưa thành thuỷ điện, quang hợp thành sinh khối rồi than dầu khí, pin Mặt Trời; ba ô nét đứt địa nhiệt, hạt nhân, thuỷ triều không từ bức xạ Mặt Trời",
            b, "Hình 2. Vòng năng lượng trên Trái Đất.<br>Ô xanh: các nhánh đi từ bức xạ Mặt Trời.<br>Ô nét đứt: ba nguồn không có gốc bức xạ Mặt Trời.")

# ═════════ Hình 3: hiệu ứng nhà kính ═════════
b = ""
YA0, YA1, YG = 92, 150, 250
b += rect(10, YA0, 380, YA1 - YA0, "rgba(148,163,184,.22)", "none", 0)
b += text(170, YA0 + 23, "khí quyển", "currentColor", 15, "middle", "700")
b += text(170, YA0 + 43, "CO₂, hơi nước, CH₄", "currentColor", 14, "middle", "600")
b += f'<rect x="10" y="{YG}" width="380" height="14" fill="rgba(52,211,153,.35)"/>'
b += line(10, YG, 390, YG, GRN, 2)
b += text(14, YG - 8, "mặt đất", GRN, 15, "start", "700")
# ánh sáng Mặt Trời: đi thẳng qua khí quyển
b += f'<circle cx="30" cy="30" r="16" fill="rgba(251,146,60,.45)" stroke="{ORG}" stroke-width="2"/>'
b += arr(46, 50, 96, YG - 4, ORG, 2.8, 12)
b += text(56, 26, "ánh sáng", ORG, 15, "start", "700")
b += text(56, 44, "đi qua", ORG, 14, "start", "600")
# hồng ngoại: một tia thoát ra, một tia bị giữ lại rồi toả về mặt đất
b += arr(250, YG - 4, 290, 20, RED, 2.4, 11)
b += text(298, 30, "một phần", RED, 14, "start", "700")
b += text(298, 48, "thoát ra", RED, 14, "start", "600")
b += arr(330, YG - 4, 346, YA1 - 8, RED, 2.4, 11)
b += f'<circle cx="349" cy="{YA1 - 20}" r="7" fill="{RED}" opacity=".7"/>'
b += line(354, YA1 - 10, 374, YG - 30, RED, 2.2, "6 4") + chevron(374, YG - 30, 20, YG - 30 - YA1 + 10, RED, 2.2, 10)
b += text(170, 186, "hồng ngoại", RED, 15, "middle", "700")
b += text(170, 204, "từ mặt đất", RED, 14, "middle", "600")
b += text(326, YA1 + 44, "bị giữ,", RED, 14, "end", "700")
b += text(326, YA1 + 62, "toả về", RED, 14, "end", "600")
fig3 = wrap("0 6 400 266",
            "Sơ đồ hiệu ứng nhà kính: ánh sáng Mặt Trời đi qua lớp khí quyển tới mặt đất; mặt đất phát hồng ngoại, một phần thoát ra vũ trụ, một phần bị khí CO2, hơi nước, CH4 hấp thụ rồi toả ngược về mặt đất",
            b, "Hình 3. Hiệu ứng nhà kính.<br>Ánh sáng Mặt Trời đi qua khí quyển.<br>Hồng ngoại từ mặt đất bị giữ lại một phần, toả về mặt đất.")

# ═════════ Hình 4: công suất tuabin gió theo tốc độ gió ═════════
VKD, VDM, VNG, VMAX = 3, 12, 25, 28
X0, XAX, YAX, YTOP = 52, 388, 236, 40


def X(v):
    return X0 + (XAX - 16 - X0) * v / VMAX


def Yp(p):                                 # p: phần của P_đm
    return YAX - 150 * p


b = ""
b += line(X0, YAX, XAX, YAX, "currentColor", 1.8) + chevron(XAX, YAX, 1, 0, "currentColor", 1.8, 10)
b += line(X0, YAX, X0, YTOP, "currentColor", 1.8) + chevron(X0, YTOP, 0, -1, "currentColor", 1.8, 10)
b += text(X0 + 10, YTOP + 6, "P", "currentColor", 16, "start", "700")
b += text(XAX, YAX + 22, "v", "currentColor", 16, "end", "700")
b += text(X0 - 8, YAX + 18, "0", "currentColor", 15, "end", "600")
b += rich(X0 - 6, Yp(1) + 5, [("P", 0), ("đm", 1)], "currentColor", 15, "end")
b += line(X0, Yp(1), X(VDM), Yp(1), "currentColor", 1.2, "4 4", .6)
for v, sub in ((VKD, "kđ"), (VDM, "đm"), (VNG, "ngắt")):
    b += line(X(v), YAX, X(v), YAX + 6, "currentColor", 1.6)
    b += rich(X(v), YAX + 24, [("v", 0), (sub, 1)], "currentColor", 15, "middle")
# đường P(v)
pts = [(X(0), YAX), (X(VKD), YAX)]
for i in range(0, 61):
    v = VKD + (VDM - VKD) * i / 60
    pts.append((X(v), Yp((v / VDM) ** 3)))
pts += [(X(VNG), Yp(1))]
d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
b += f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="2.8" stroke-linejoin="round"/>'
b += line(X(VNG), Yp(1), X(VNG), YAX, BLUE, 1.8, "5 4")
b += line(X(VNG), YAX, X(VMAX) - 4, YAX, BLUE, 2.8)
# kiểm toạ độ: đầu đoạn bậc ba ở v_kđ nằm trên trục (P rất nhỏ), cuối đoạn chạm đúng P_đm
assert abs(pts[2][1] - Yp((VKD / VDM) ** 3)) < 1e-9 and abs(pts[62][1] - Yp(1)) < 1e-9
b += rich(X(7.2) + 2, Yp(0.42), [("P ∼ v³", 0)], BLUE, 15, "end")
b += rich((X(VDM) + X(VNG)) / 2, Yp(1) - 12, [("P = P", 0), ("đm", 1)], BLUE, 15, "middle")
# chú giải dưới trục, mỗi vùng một dòng
LY = YAX + 54
for i, parts in enumerate([[("dưới v", 0), ("kđ", 1), (": gió yếu, P = 0", 0)],
                           [("v", 0), ("kđ", 1), (" tới v", 0), ("đm", 1), (": P tăng theo v³", 0)],
                           [("v", 0), ("đm", 1), (" tới v", 0), ("ngắt", 1), (": giữ định mức", 0)],
                           [("trên v", 0), ("ngắt", 1), (": dừng để an toàn", 0)]]):
    b += rich(12, LY + 22 * i, parts, "currentColor", 15, "start", "600")
fig4 = wrap("0 24 400 344",
            "Đồ thị công suất tuabin gió theo tốc độ gió: bằng 0 dưới tốc độ khởi động, tăng theo lập phương tới tốc độ định mức, nằm ngang ở công suất định mức tới tốc độ ngắt, rồi về 0",
            b, "Hình 4. Công suất tuabin gió theo tốc độ gió: ba vùng làm việc.")

# ═════════ ghi theory.html ═════════
src = open(os.path.join(HERE, "theory.src.html"), encoding="utf8").read()
for k, f in ((1, fig1), (2, fig2), (3, fig3), (4, fig4)):
    assert f"<!--FIG{k}-->" in src, k
    src = src.replace(f"<!--FIG{k}-->", f)
src = src.replace("__PHUT__", str(PHUT))
assert "$" not in "".join((fig1, fig2, fig3, fig4))
open(os.path.join(HERE, "theory.html"), "w", encoding="utf8").write(src)
print("ok", len(src))
