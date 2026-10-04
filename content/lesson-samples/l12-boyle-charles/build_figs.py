"""Sinh 3 hình SVG cho bài "Bài 6. Định luật Boyle. Định luật Charles" (Vật lí 12)
và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy từ gốc repo: python3 content/lesson-samples/l12-boyle-charles/build_figs.py

LƯU Ý: trong <text> của SVG KHÔNG viết $...$ (KaTeX auto-render chèn span HTML vào SVG
làm chữ biến mất) — chỉ dùng chữ thường, Unicode và tspan cho chỉ số dưới.
"""
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"'
            f'{d} opacity="{op}"/>')


def dot(x, y, r=5, c="currentColor"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def rect(x, y, w, h, fill, stroke="currentColor", sw=2, rx=8):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>')


def sub(x, y, base, chi_so, c="currentColor", size=12, weight="700"):
    """Chữ có chỉ số dưới bằng tspan (không dùng KaTeX trong SVG)."""
    return (f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="start">'
            f'{base}<tspan dy="4" font-size="{size - 3}">{chi_so}</tspan></text>')


def polyline(pts, c, w=3):
    s = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline points="{s}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round"/>'


def hyperbola(x0, y0, K, x_cuoi, y_tren=42, buoc=3.0):
    """Nhánh (x−x0)(y0−y)=K từ chỗ chạm y_tren tới x_cuoi.

    Vẽ bằng polyline lấy đúng từ công thức p = k/V nên chấm dữ liệu đặt vào là trùng đường.
    """
    x, ra = x0 + K / (y0 - y_tren), []
    while x < x_cuoi:
        ra.append((x, y0 - K / (x - x0)))
        x += buoc
    ra.append((x_cuoi, y0 - K / (x_cuoi - x0)))
    return ra


def nhan_theo_duong(xc, yc, m, lech, c, noi_dung, size=11):
    """Nhãn xoay song song đường y = yc − m(x−xc), đặt lệch `lech` px theo pháp tuyến.

    `lech` > 0 là lệch lên phía trên-trái của đường, `lech` < 0 là xuống dưới-phải.
    """
    g = math.atan2(-m, 1.0)                     # góc nghiêng của đường (radian)
    nx, ny = math.sin(g), -math.cos(g)          # pháp tuyến hướng lên-trái
    x, y = xc + nx * lech, yc + ny * lech
    deg = math.degrees(g)
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="700" '
            f'text-anchor="middle" transform="rotate({deg:.2f} {x:.1f} {y:.1f})">{noi_dung}</text>')


def fig(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">'
            f'{body}</svg><figcaption>{cap}</figcaption></figure>')


# ---------------------------------------------------------------- Hình 1: nén khí trong bơm
b = defs("f1")
b += text(14, 22, "Nén khí trong bơm, nhiệt độ không đổi", "currentColor", 12.5, "start", "700")
b += rect(100, 40, 130, 196, "rgba(148,163,184,.10)", "currentColor", 2.5, 14)
b += line(100, 236, 230, 236, "currentColor", 2.5)
b += rect(104, 136, 122, 100, "rgba(52,211,153,.18)", GRN, 1.6, 8)
b += line(104, 136, 226, 136, GRN, 3)
b += rect(104, 210, 122, 26, "rgba(248,113,113,.20)", RED, 1.6, 8)
b += line(104, 210, 226, 210, RED, 3)
b += line(165, 118, 165, 136, "currentColor", 3)
b += rect(149, 106, 32, 12, "currentColor", "currentColor", 0, 3)
b += arrow("f1", "r", 165, 44, 165, 104, 2.6)
b += text(108, 190, "V", GRN, 12.5, "start", "700")
b += text(108, 228, "V/4", RED, 12.5, "start", "700")
b += text(240, 70, "Ấn pittông xuống:", "currentColor", 11, "start", "700")
b += text(240, 88, "thể tích khí nhỏ lại", "currentColor", 11, "start", "600")
b += text(240, 112, "ban đầu: V, p", GRN, 11.5, "start", "700")
b += text(240, 132, "bị nén: V/4, p′", RED, 11.5, "start", "700")
b += text(240, 152, "⇒ p′ = 4p (pV không đổi)", RED, 11, "start", "700")
b += text(240, 176, "vì nhiệt độ không đổi", "currentColor", 10.5, "start", "600")
b += text(240, 196, "nên tay em ấn nặng hơn", "currentColor", 10.5, "start", "600")
fig1 = fig("0 0 460 254",
           "Bơm xe: pittông đi xuống làm thể tích khí trong thân bơm nhỏ lại, áp suất tăng lên; thể tích còn một phần tư thì áp suất gấp bốn lần",
           b,
           "Hình 1. Bơm xe: cán bơm đi xuống làm thể tích khí nhỏ lại, áp suất tăng lên. Khi thể tích còn một phần tư thì áp suất gấp bốn lần — tích $pV$ không đổi vì nhiệt độ không đổi.",
           exp="tn-l12-boylecharles-04")

# ---------------------------------------------------------------- Hình 2: đường đẳng nhiệt trên p–V
# Hai nhánh vẽ đúng từ p = k/V: (x−60)·(216−y) = K. Chấm ở x = 232 nằm CHÍNH XÁC trên đường.
b = defs("f2")
b += line(60, 216, 380, 216, "currentColor", 2)
b += line(60, 216, 60, 34, "currentColor", 2)
b += text(384, 220, "V", "currentColor", 13, "start", "700")
b += text(18, 40, "p", "currentColor", 13, "start", "700")
b += text(60, 236, "O", "currentColor", 12, "middle", "600")
XR = 232.0                                       # cùng một V để so hai nhiệt độ
K_BLUE, K_RED = 172 * 43.0, 172 * 62.0           # chấm xanh (232,173) · chấm đỏ (232,154)
b += polyline(hyperbola(60, 216, K_BLUE, 372), BLUE)
b += polyline(hyperbola(60, 216, K_RED, 372), RED)
Y_BLUE, Y_RED = 216 - K_BLUE / (XR - 60), 216 - K_RED / (XR - 60)
b += line(XR, 216, XR, Y_RED, "currentColor", 1.2, "6 5", .5)
b += dot(XR, Y_RED, 4, RED) + dot(XR, Y_BLUE, 4, BLUE)
b += text(240, 58, "cùng một V:", "currentColor", 10.5, "start", "600")
b += text(240, 74, "đường đỏ cho p lớn hơn", "currentColor", 10.5, "start", "600")
b += text(240, 92, "→ khí nóng hơn", RED, 10.5, "start", "700")
b += text(240, 122, "hai nhiệt độ khác nhau,", "currentColor", 10.5, "start", "600")
b += text(240, 138, "cùng một lượng khí", "currentColor", 10.5, "start", "600")
b += sub(344, 172, "T", "2", RED, 12)
b += sub(344, 210, "T", "1", BLUE, 12)
fig2 = fig("0 0 400 242",
           "Đồ thị áp suất theo thể tích ở nhiệt độ không đổi: hai nhánh hypebol, đường ứng với nhiệt độ cao hơn nằm xa gốc toạ độ hơn",
           b,
           "Hình 2. Đường đẳng nhiệt trên đồ thị $p$–$V$ là một nhánh hypebol. Cùng một lượng khí, đường ứng với nhiệt độ cao hơn ($T_2$) nằm xa gốc toạ độ hơn.",
           exp="tn-l12-boylecharles-03")

# ---------------------------------------------------------------- Hình 3: đường đẳng áp trên V–T
# Trục T chia TUYẾN TÍNH: O = 0 K tại x = 64, x = 372 ứng với 400 K (0,77 px/K).
# Chấm dữ liệu lấy y từ chính phương trình đường nên luôn nằm trên đường.
b = defs("f3")
b += line(64, 206, 372, 206, "currentColor", 2)
b += line(64, 206, 64, 30, "currentColor", 2)
b += text(376, 210, "T", "currentColor", 13, "start", "700")
b += text(16, 38, "V", "currentColor", 13, "start", "700")
b += text(64, 226, "O", "currentColor", 12, "middle", "600")
X0, Y0, X_END, T_MAX = 64.0, 206.0, 372.0, 400.0
M1, M2 = 140 / 266, 100 / 266                    # độ dốc hai đường đẳng áp (p1 < p2)
tx = lambda t: round(X0 + (X_END - X0) * t / T_MAX, 1)   # toạ độ x của nhiệt độ t (K)
vy = lambda x, m: round(Y0 - m * (x - X0), 1)
for t, neo in ((273, "end"), (300, "start"), (360, "middle")):
    b += line(tx(t), 206, tx(t), 211, "currentColor", 1.4)
    b += text(tx(t), 226, str(t), "currentColor", 10.5, neo, "600")
b += line(X0, Y0, X_END, vy(X_END, M1), ORG, 3)
b += line(X0, Y0, X_END, vy(X_END, M2), BLUE, 3)
for t in (300, 360):
    x = tx(t)
    b += line(x, 206, x, vy(x, M1), "currentColor", 1.2, "6 5", .5)
    b += dot(x, vy(x, M1), 4, ORG) + dot(x, vy(x, M2), 4, BLUE)
b += nhan_theo_duong(200, vy(200, M1), M1, 7, ORG,
                     'p<tspan dy="4" font-size="8">1</tspan><tspan dy="-4"> (nhỏ hơn)</tspan>')
b += nhan_theo_duong(255, vy(255, M2), M2, -12, BLUE,
                     'p<tspan dy="4" font-size="8">2</tspan><tspan dy="-4"> &gt; p</tspan>'
                     '<tspan dy="4" font-size="8">1</tspan>')
b += text(100, 44, "cùng một T: đường cam cho V lớn hơn", "currentColor", 10.5, "start", "600")
b += text(64, 244, "kéo dài: cả hai đường đi qua gốc O", "currentColor", 10.5, "start", "600")
fig3 = fig("0 0 400 252",
           "Đồ thị thể tích theo nhiệt độ tuyệt đối ở áp suất không đổi: hai đường thẳng kéo dài đều đi qua gốc toạ độ, đường ứng với áp suất nhỏ hơn nằm cao hơn",
           b,
           "Hình 3. Đường đẳng áp trên đồ thị $V$–$T$ là đoạn thẳng, kéo dài thì đi qua gốc $O$. Cùng một lượng khí, đường ứng với áp suất nhỏ hơn ($p_1$) nằm cao hơn.")

# ---------------------------------------------------------------- chèn vào theory.html
src = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, f in enumerate((fig1, fig2, fig3), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
(HERE / "theory.html").write_text(src, encoding="utf8")
print("ok", len(src), "bytes")
