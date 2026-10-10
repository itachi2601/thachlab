"""Hình cho bài tập mẫu Bài 14 "Hạt nhân và mô hình nguyên tử" (Vật lí 12), lesson_id 15.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Mô phỏng dùng hạt nhân/nguyên tố MẪU khác đề (ghi rõ trong chú thích) và số liệu tính thật từ công thức của bài;
không để lộ đáp số: hình dữ kiện chỉ có dữ kiện đề cho và dấu "?" ở đại lượng cần tìm."""
import math, os, random, re as _re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"


# ───────────── tiện ích vẽ ─────────────
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

def circ(x, y, r, c="currentColor", sw=2, fill="none"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'

def box_t(x, y, w, h, lines, c="currentColor", size=13):
    b = R(x, y, w, h, c, 2, rx=6)
    n = len(lines)
    for i, s in enumerate(lines):
        yy = y + h / 2 + 5 - (n - 1) * 8 + i * 16
        b += txt(x + w / 2, yy, s, c, size, "middle")
    return b

def nuc(x, y, A, Z, sym, c="currentColor", size=20):
    """Kí hiệu hạt nhân: A ở trên, Z ở dưới, kí hiệu nguyên tố bên phải; (x, y) = góc trái, đường cơ sở của kí hiệu."""
    fi = round(size * 0.55)
    wi = max(len(str(A)), len(str(Z))) * fi * 0.6
    b = lbl(x + wi, y - size * 0.55, str(A), c, fi, "end", "700") + lbl(x + wi, y + size * 0.05 + fi * 0.5, str(Z), c, fi, "end", "700")
    b += lbl(x + wi + 2, y + size * 0.3, sym, c, size, "start", "700")
    return b, wi + 2 + len(sym) * size * 0.62

def anim(attr, vals, kts, T):
    v = ";".join(f"{x:.1f}" if isinstance(x, float) else str(x) for x in vals)
    k = ";".join(f"{t:.4f}" for t in kts)
    return f'<animate attributeName="{attr}" values="{v}" keyTimes="{k}" dur="{T:.2f}s" begin="indefinite" fill="freeze"/>'

def nucleon(kind, x, y, r, animx="", animy=""):
    if kind == "p":
        return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{RED}" fill-opacity=".55" stroke="{RED}" stroke-width="1.6">{animx}{animy}</circle>')
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{GREY}" fill-opacity=".45" stroke="{GREY}" stroke-width="1.6">{animx}{animy}</circle>')


# ───────────── Dạng 1 · đọc kí hiệu, đếm hạt (mô phỏng: lắp hạt nhân lithi-7 MẪU) ─────────────
def d1(kk):
    p = f"d1{kk}"
    if kk == 0:
        r = 7.4; cx, cy = 300, 100
        ring = [(0, 0)] + [(15.2 * math.cos(math.radians(60 * k + 30)), 15.2 * math.sin(math.radians(60 * k + 30))) for k in range(6)]
        kinds = ["n", "p", "n", "p", "n", "p", "n"]          # 3 prôtôn + 4 nơtron
        T = 7.4
        starts = {"p": [(34, 52), (34, 88), (34, 124)], "n": [(86, 52), (86, 88), (86, 124), (86, 160)]}
        cnt = {"p": 0, "n": 0}
        b = ""
        for i, (kd, (ox, oy)) in enumerate(zip(kinds, ring)):
            sx, sy = starts[kd][cnt[kd]]; cnt[kd] += 1
            ex, ey = cx + ox, cy + oy
            t0 = 0.4 + i * 0.95; t1 = t0 + 0.8
            kt = [0, t0 / T, t1 / T, 1]
            b += nucleon(kd, sx, sy, r, anim("cx", [sx, sx, ex, ex], kt, T), anim("cy", [sy, sy, ey, ey], kt, T))
        b += txt(34, 28, "prôtôn", RED, 12, "middle", "400") + txt(86, 28, "nơtron", GREY, 12, "middle", "400")
        b += circ(20, 190, 6, RED, 1.6, RED) + txt(32, 195, "prôtôn (+e)", RED, 12) + circ(150, 190, 6, GREY, 1.6, GREY) + txt(162, 195, "nơtron (không mang điện)", GREY, 12)
        b += txt(300, 160, "hạt nhân mẫu: lithi-7", "currentColor", 13, "middle") + txt(300, 178, "(không phải hạt nhân trong đề)", "currentColor", 12, "middle", "400")
        b += arrow(p, "b", 135, 100, 262, 100, 2)
        return fig("d1-0", "0 0 420 206", "Các prôtôn và nơtron lần lượt vào một hạt nhân lithi-7 mẫu", b,
                   "Mô phỏng: từng nuclôn (prôtôn hoặc nơtron) tiến vào tụ lại thành một hạt nhân mẫu. " + NOTE)
    b = ""
    sy, wd = nuc(120, 104, 63, 29, "Cu", "currentColor", 44)
    b += sy
    b += arrow(p, "o", 78, 36, 112, 62, 2) + txt(10, 30, "chỉ số trên", ORG, 13)
    b += arrow(p, "o", 78, 174, 112, 120, 2) + txt(10, 190, "chỉ số dưới", ORG, 13)
    b += txt(250, 52, "Cần tìm:", "currentColor", 13) + txt(250, 76, "số prôtôn ?", ORG, 13) + txt(250, 98, "số nuclôn ?", ORG, 13)
    b += txt(250, 120, "số nơtron ?", ORG, 13) + txt(250, 142, "số êlectron ?", ORG, 13) + txt(250, 164, "điện tích hạt nhân ?", ORG, 13)
    return fig("d1-2", "0 0 420 208", "Kí hiệu hạt nhân của đồng với hai chỉ số cần đọc và các đại lượng cần tìm", b,
               "Dữ kiện: kí hiệu hạt nhân của đồng đã cho; các đại lượng cần tìm ghi bên phải. " + NOTE)


# ───────────── Dạng 2 · đồng vị (mô phỏng: ba đồng vị của hiđrô MẪU) ─────────────
def d2(kk):
    p = f"d2{kk}"
    if kk == 0:
        T = 8.0; xs = [80, 210, 340]; cy = 100; r = 11
        b = ""
        names = ["hiđrô-1", "hiđrô-2 (đơteri)", "hiđrô-3 (triti)"]
        for j, x in enumerate(xs):
            b += nucleon("p", x, cy, r)
            b += txt(x, 150, names[j], "currentColor", 12, "middle")
            b += txt(x, 168, "1 prôtôn", RED, 12, "middle", "400")
        # nơtron thêm lần lượt: hiđrô-2 nhận 1, hiđrô-3 nhận 2
        spec = [(xs[1], 1.0, 2.2, (xs[1] + 22, cy)), (xs[2], 3.0, 4.2, (xs[2] + 22, cy)), (xs[2], 4.8, 6.0, (xs[2] + 11, cy - 19))]
        for x, t0, t1, (ex, ey) in spec:
            kt = [0, t0 / T, t1 / T, 1]
            b += nucleon("n", x, 28, r, anim("cx", [x, x, ex, ex], kt, T), anim("cy", [28.0, 28.0, ey, ey], kt, T))
        b += txt(210, 188, "thêm nơtron: vẫn là hiđrô", "currentColor", 12, "middle", "400")
        return fig("d2-0", "0 0 420 200", "Thêm nơtron vào hạt nhân hiđrô thì số prôtôn không đổi", b,
                   "Mô phỏng: hạt nhân hiđrô mẫu nhận thêm nơtron lần lượt; hiđrô là ví dụ khác đề. " + NOTE)
    b = ""
    items = [(12, 6, "C"), (14, 6, "C"), (14, 7, "N"), (15, 7, "N"), (16, 8, "O"), (17, 8, "O")]
    for k, (A, Z, s) in enumerate(items):
        col, row = k % 3, k // 3
        x0, y0 = 20 + col * 130, 20 + row * 74
        b += R(x0, y0, 110, 58, "currentColor", 2, rx=8)
        sy, wd = nuc(x0 + 16, y0 + 40, A, Z, s, "currentColor", 26)
        b += sy
    b += txt(20, 190, "Cần tìm:  số nơtron mỗi hạt nhân · số cặp đồng vị", ORG, 13)
    return fig("d2-2", "0 0 420 206", "Sáu hạt nhân cho bởi kí hiệu, cần tìm số nơtron và các cặp đồng vị", b,
               "Dữ kiện: sáu kí hiệu hạt nhân; chưa nhóm hay đánh dấu cặp nào. " + NOTE)


# ───────────── Dạng 3 · bán kính hạt nhân (mô phỏng: ba hạt nhân MẪU A = 8, 27, 125) ─────────────
def d3(kk):
    p = f"d3{kk}"
    if kk == 0:
        T = 7.5; k = 10.0                                   # px trên 10⁻¹⁵ m
        spec = [(8, 70), (27, 190), (125, 330)]
        cy = 104
        b = ""
        for i, (A, x) in enumerate(spec):
            Rm = 1.2 * A ** (1 / 3); rr = k * Rm
            t0 = 0.4 + i * 2.2; t1 = t0 + 1.6
            kt = [0, t0 / T, t1 / T, 1]
            b += (f'<circle cx="{x}" cy="{cy}" r="0" fill="{BLUE}" fill-opacity=".18" stroke="{BLUE}" stroke-width="2">'
                  f'{anim("r", [0.0, 0.0, rr, rr], kt, T)}</circle>')
            b += txt(x, 196, f"A = {A}", "currentColor", 13, "middle")
            kt2 = [0, t1 / T, min(1.0, (t1 + 0.3) / T), 1]
            b += (f'<g opacity="0">{anim("opacity", [0, 0, 1, 1], kt2, T)}'
                  + txt(x, 176, f"R = {Rm:.1f}·10⁻¹⁵ m".replace(".", ","), BLUE, 12, "middle") + "</g>")
        b += R(24, 20, k, 5, "currentColor", 1.6) + txt(24 + k + 8, 27, "= 1·10⁻¹⁵ m (thước)", "currentColor", 12, "start", "400")
        return fig("d3-0", "0 0 420 206", "Ba hạt nhân mẫu lớn dần theo số khối, bán kính ghi dưới mỗi hạt nhân", b,
                   "Mô phỏng: bán kính tính từ công thức R = 1,2·10⁻¹⁵·∛A cho ba hạt nhân mẫu A = 8, 27, 125 (khác hạt nhân trong đề); bán kính vẽ đúng tỉ lệ với thước 10⁻¹⁵ m.")
    b = ""
    b += circ(95, 96, 46, BLUE, 2.2) + arrow(p, "o", 95, 96, 141, 96, 1.8) + txt(118, 88, "R", ORG, 13, "middle")
    sy, _ = nuc(55, 168, 64, 30, "Zn", "currentColor", 20); b += sy + txt(130, 168, "R = ?", ORG, 13)
    b += circ(300, 96, 58, BLUE, 2.2) + arrow(p, "o", 300, 96, 358, 96, 1.8) + txt(330, 88, "R", ORG, 13, "middle")
    sy, _ = nuc(250, 190, 238, 92, "U", "currentColor", 20); b += sy + txt(335, 190, "R = ?", ORG, 13)
    b += txt(10, 22, "R = 1,2·10⁻¹⁵·∛A (m), hạt nhân hình cầu", "currentColor", 12, "start", "400")
    return fig("d3-2", "0 0 420 214", "Hai hạt nhân hình cầu với số khối đã cho và bán kính cần tìm", b,
               "Dữ kiện: số khối của hai hạt nhân; bán kính, tỉ số bán kính và tỉ số thể tích cần tìm. Hình không đúng tỉ lệ. ")


# ───────────── Dạng 4 · đếm hạt trong m gam (mô phỏng: mạng nguyên tử rung nhiệt, mẫu kim loại) ─────────────
def d4(kk):
    p = f"d4{kk}"
    if kk == 0:
        T = 6.0; rnd = random.Random(15)
        b = R(24, 34, 214, 150, "currentColor", 2.4, rx=6)
        for i in range(5):
            for j in range(3):
                x, y = 56 + 40 * i, 66 + 40 * j
                ph, ph2 = rnd.uniform(0, 6.28), rnd.uniform(0, 6.28)
                f1, f2 = rnd.uniform(1.5, 2.5), rnd.uniform(1.5, 2.5)
                vals = ";".join(f"{x + 3.4 * math.sin(ph + 2 * math.pi * f1 * u / 14):.1f} {y + 3.4 * math.sin(ph2 + 2 * math.pi * f2 * u / 14):.1f}" for u in range(15))
                b += (f'<g transform="translate({x} {y})"><animateTransform attributeName="transform" type="translate" values="{vals}" dur="{T:.1f}s" begin="indefinite" fill="freeze"/>'
                      f'<circle r="14" fill="{BLUE}" fill-opacity=".12" stroke="{BLUE}" stroke-width="1.4"/><circle r="3.4" fill="{RED}"/></g>')
        b += txt(24, 22, "mẫu kim loại phóng to", "currentColor", 13)
        b += txt(256, 62, "mẫu sắt Fe", "currentColor", 13) + txt(256, 84, "m = 14 g", "currentColor", 13, "start", "400") + txt(256, 106, "M ≈ 56 g/mol", "currentColor", 13, "start", "400")
        b += txt(256, 128, "N_A = 6,022·10²³ mol⁻¹", "currentColor", 12, "start", "400")
        b += txt(256, 154, "số hạt nhân = ?", ORG, 13) + txt(256, 174, "số nơtron = ?", ORG, 13)
        return fig("d4-0", "0 0 420 196", "Các nguyên tử trong mẫu kim loại dao động quanh vị trí cân bằng, mỗi chấm đỏ là một hạt nhân", b,
                   "Mô phỏng: mỗi vòng xanh là một nguyên tử, chấm đỏ là hạt nhân; số nguyên tử trong hình chỉ để minh hoạ, thực tế rất nhiều hơn. " + NOTE)
    b = ""
    b += box_t(10, 14, 120, 40, ["m = 14 g"], "currentColor", 13) + box_t(160, 14, 100, 40, ["n = ?"], ORG, 14)
    b += box_t(290, 14, 120, 40, ["số hạt nhân = ?"], ORG, 13)
    b += arrow(p, "b", 130, 34, 160, 34, 2.2) + arrow(p, "b", 260, 34, 290, 34, 2.2)
    b += box_t(10, 96, 150, 40, ["nơtron mỗi hạt nhân = ?"], ORG, 12) + box_t(190, 96, 220, 40, ["số nơtron cả mẫu = ?"], ORG, 13)
    b += box_t(190, 152, 220, 40, ["điện tích các prôtôn = ?"], ORG, 13)
    b += txt(10, 76, "M ≈ 56 g/mol · N_A = 6,022·10²³ mol⁻¹ · e = 1,6·10⁻¹⁹ C", "currentColor", 12, "start", "400")
    b += txt(10, 166, "kí hiệu: Fe, số khối 56,", "currentColor", 12, "start", "400") + txt(10, 184, "chỉ số dưới 26", "currentColor", 12, "start", "400")
    return fig("d4-2", "0 0 420 204", "Các đại lượng cần tìm của mẫu sắt và dữ kiện cho trước", b,
               "Dữ kiện: khối lượng mẫu, khối lượng mol, N_A, e và kí hiệu hạt nhân; bốn đại lượng cần tìm. " + NOTE)


# ───────────── Dạng 5 · khối lượng nguyên tử trung bình (mô phỏng: liti tự nhiên MẪU, lấy ngẫu nhiên từng nguyên tử) ─────────────
def d5(kk):
    p = f"d5{kk}"
    if kk == 0:
        N = 40; m6, m7, f6 = 6.015, 7.016, 0.075
        rnd = random.Random(23)
        draws = [m6 if rnd.random() < f6 else m7 for _ in range(N)]
        x0, x1 = 50, 390; dx = (x1 - x0) / N
        ytop, ybot = 120, 214                                # trục tung: 7,2 (trên) → 6,0 (dưới)
        def yv(v): return ybot - (v - 6.0) / 1.2 * (ybot - ytop)
        run = 0.0; pts = []
        for i, m in enumerate(draws):
            run += m; pts.append((x0 + dx * (i + 0.5), yv(run / (i + 1))))
        T = 8.0
        b = f'<clipPath id="{p}c"><rect x="{x0 - 2}" y="20" width="0" height="210"><animate attributeName="width" from="0" to="{x1 - x0 + 4}" dur="{T}s" begin="indefinite" fill="freeze"/></rect></clipPath>'
        b += R(x0, ytop, x1 - x0, ybot - ytop, "currentColor", 1.6, op=.6)
        for v in (6.0, 6.5, 7.0):
            b += seg(x0 - 4, yv(v), x0, yv(v), "currentColor", 1.6) + txt(x0 - 7, yv(v) + 4, f"{v:.1f}".replace(".", ","), "currentColor", 11, "end", "400")
        b += txt(x0 - 7, ytop - 8, "u", "currentColor", 11, "end", "400")
        b += '<g clip-path="url(#' + p + 'c)">'
        for i, m in enumerate(draws):
            b += f'<circle cx="{x0 + dx * (i + .5):.1f}" cy="62" r="3.3" fill="{ORG if m == m6 else BLUE}"/>'
        b += poly(pts, GRN, 2.2) + "</g>"
        b += circ(60, 28, 4, ORG, 1.2, ORG) + txt(70, 32, "⁶Li (6,015 u)", ORG, 12, "start", "400") + circ(180, 28, 4, BLUE, 1.2, BLUE) + txt(190, 32, "⁷Li (7,016 u)", BLUE, 12, "start", "400")
        b += txt(x0, 90, "mỗi chấm: một nguyên tử được lấy ngẫu nhiên", "currentColor", 12, "start", "400")
        b += txt(x0 + 6, 111, "khối lượng trung bình các nguyên tử đã lấy", GRN, 12, "start", "400")
        b += txt((x0 + x1) / 2, 232, "số nguyên tử đã lấy (từ trái sang phải)", "currentColor", 12, "middle", "400")
        return fig("d5-0", "0 0 420 240", "Khối lượng trung bình của các nguyên tử liti lấy ngẫu nhiên dần ổn định theo tỉ lệ đồng vị", b,
                   "Mô phỏng: liti tự nhiên mẫu (7,5 % ⁶Li, 92,5 % ⁷Li), khác bo trong đề; lấy ngẫu nhiên 40 nguyên tử, đường xanh là khối lượng trung bình các nguyên tử đã lấy. " + NOTE)
    b = R(10, 14, 190, 54, "currentColor", 2, rx=6) + R(220, 14, 190, 54, "currentColor", 2, rx=6)
    sy, _ = nuc(34, 46, 10, 5, "B", "currentColor", 22); b += sy + txt(98, 46, "10,013 u", "currentColor", 14, "start")
    sy, _ = nuc(244, 46, 11, 5, "B", "currentColor", 22); b += sy + txt(308, 46, "11,009 u", "currentColor", 14, "start")
    b += txt(105, 90, "tỉ lệ ?", ORG, 13, "middle") + txt(315, 90, "tỉ lệ ?", ORG, 13, "middle")
    b += box_t(60, 106, 300, 40, ["bo tự nhiên: khối lượng trung bình 10,811 u"], "currentColor", 13)
    b += txt(10, 170, "1 u ≈ 1,66054·10⁻²⁷ kg ≈ 931,5 MeV/c²", "currentColor", 12, "start", "400")
    b += txt(10, 192, "Cần tìm: tỉ lệ hai đồng vị", ORG, 12) + txt(10, 210, "khối lượng một nguyên tử ¹¹B ra kg và ra MeV/c²", ORG, 12)
    return fig("d5-2", "0 0 420 220", "Hai đồng vị của bo với khối lượng nguyên tử đã cho và khối lượng trung bình của bo tự nhiên", b,
               "Dữ kiện: khối lượng nguyên tử hai đồng vị và khối lượng trung bình; tỉ lệ mỗi đồng vị là ẩn. Hình không đúng tỉ lệ. ")


BUILD = [d1, d2, d3, d4, d5]
