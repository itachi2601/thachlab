"""Hình cho bài tập mẫu Bài 20 "Điện thế" (Vật lí 11), lesson_id 39.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Điện tích được dịch chuyển theo đoạn thẳng với tốc độ minh hoạ (mẫu cách đều thời gian, nội suy tuyến tính).
Hình D1, D4, D5 vẽ đúng góc và đúng tỉ lệ độ dài đã cho; đường sức chỉ để chỉ chiều (khoảng cách giữa chúng không có ý nghĩa).
KHÔNG vẽ sẵn lực, công, dấu của U hay điện thế cần tìm: chỉ dữ kiện đề cho và dấu «?»."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ."
MINUS = "−"


def eq(x, y, base, subs, rest, c="currentColor", size=13, anchor="start"):
    """Nhãn một dòng có chỉ số dưới: base + chỉ số + phần còn lại (vd. V_M = 140 V)."""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="700" text-anchor="{anchor}">'
            f'{base}<tspan dy="4" font-size="{size - 3}">{subs}</tspan><tspan dy="-4">{rest}</tspan></text>')


def charge(x, y, sign, c, r=9):
    """Điện tích: vòng tròn tô nhạt + dấu."""
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" fill-opacity=".22" stroke="{c}" stroke-width="2"/>'
            + text(f"{x:.1f}", f"{y + 5:.1f}", sign, c, 15, "middle", "800"))


def move(content, pts, T):
    """Nhóm tịnh tiến theo mẫu cách đều thời gian; nội dung vẽ tại pts[0]; chạy một lần khi bấm, dừng ở khung cuối."""
    x0, y0 = pts[0]
    vals = ";".join(f"{x - x0:.1f} {y - y0:.1f}" for x, y in pts)
    return (f'<g><animateTransform attributeName="transform" type="translate" values="{vals}" dur="{T:.2f}s" '
            f'begin="indefinite" fill="freeze"/>{content}</g>')


def flip(content, t0, T, to):
    """Đổi độ mờ của nhóm tại t0 (rời rạc): to=0 → ẩn từ t0; to=1 → hiện từ t0. Giá trị ban đầu (trước khi bấm) do thuộc tính opacity."""
    a, b = (1, 0) if to == 0 else (0, 1)
    return (f'<g opacity="{a}"><animate attributeName="opacity" values="{a};{b}" keyTimes="0;{t0 / T:.4f}" calcMode="discrete" '
            f'dur="{T:.2f}s" begin="indefinite" fill="freeze"/>{content}</g>')


def line_pts(P, Q, n, hold_start=0, hold_end=0):
    pts = [P] * hold_start + [(P[0] + (Q[0] - P[0]) * i / n, P[1] + (Q[1] - P[1]) * i / n) for i in range(n + 1)] + [Q] * hold_end
    return pts


def efield(ys, x0, x1, c="currentColor"):
    return "".join(field_line(x0, y, x1, y, c, 1.5, "6 5", 10) for y in ys)


# ───────────── Dạng 1 · điện tích q = −2 µC dịch chuyển M → N trong điện trường đều ─────────────
def d1(kk):
    p = f"d1{kk}"; s = 16.0
    M = (96.0, 196.0); a = math.radians(60)
    N = (M[0] + s * 8 * math.cos(a), M[1] - s * 8 * math.sin(a))
    ys = [M[1], M[1] - (M[1] - N[1]) / 2, N[1], N[1] - (M[1] - N[1]) / 2]
    b = efield(ys, 24, 402)
    b += seg(*M, *N, GRN, 2.2, "7 5")
    b += dot(*M, 3.5) + dot(*N, 3.5)
    b += lbl(M[0] - 14, M[1] + 20, "M", "currentColor", 14, "end", "700") + lbl(N[0] + 12, N[1] - 8, "N", "currentColor", 14, "start", "700")
    b += arc(M[0], M[1], 34, 0, 60, RED, 1.8) + lbl(M[0] + 40, M[1] - 8, "60°", RED, 13, "start", "700")
    b += lbl(102, 172, "MN = 8 cm", GRN, 13, "end", "700")
    b += lbl(24, 20, "E = 5000 V/m", ORG, 14, "start", "700")
    b += eq(250, 174, "A", "MN", " = ?", ORG, 14)
    if kk == 0:
        b += lbl(24, 184, "q = −2 μC", BLUE, 13, "start", "700")
        b += move(charge(*M, MINUS, BLUE), line_pts(M, N, 40), 3.0)
        return fig("d1-0", "0 0 420 240", "Điện tích âm được dịch chuyển từ điểm M đến điểm N trong điện trường đều có đường sức nằm ngang chiều từ trái sang phải", b,
                   "Mô phỏng: điện tích được dịch chuyển từ M đến N với tốc độ minh hoạ (3 s). Hình vẽ đúng góc 60° và đúng tỉ lệ độ dài MN; khoảng cách giữa các đường sức không có ý nghĩa.")
    b += lbl(24, 184, "q = −2 μC", BLUE, 13, "start", "700")
    b += charge(*M, MINUS, BLUE)
    return fig("d1-2", "0 0 420 240", "Dữ kiện: điện trường đều E, điểm M và N cách nhau 8 cm, đoạn MN hợp đường sức góc 60 độ, N lệch về phía chiều đường sức", b,
               "Dữ kiện đề cho. Hình vẽ đúng góc 60° và đúng tỉ lệ độ dài MN.")


# ───────────── Dạng 2 · ba điện tích lần lượt đặt vào đúng điểm M ─────────────
def d2(kk):
    M = (100.0, 104.0); T = 6.0; t1, t2 = 2.0, 4.0
    RB = "#38bdf8"; RR = "#f87171"
    b = dot(*M, 3.5) + lbl(M[0], M[1] + 36, "M", "currentColor", 14, "middle", "700")
    b += eq(M[0] - 24, M[1] - 38, "V", "M", " = ?", ORG, 15)
    # ba hàng thông tin bên phải (mặc định hiện; khi chạy thì hiện dần)
    r1 = (charge(178, 60, MINUS, RB, 8) + lbl(196, 58, "q₁ = −4 nC", "currentColor", 13, "start", "700") + eq(196, 78, "W", "1", " = −0,60 μJ"))
    r2 = (charge(178, 114, "+", RR, 8) + lbl(196, 112, "q₂ = +5 nC", "currentColor", 13, "start", "700") + eq(196, 132, "W", "2", " = ?", ORG))
    r3 = (charge(178, 168, MINUS, RB, 8) + lbl(196, 166, "electron (q = −e)", "currentColor", 13, "start", "700") + lbl(196, 186, "W = ? (eV)", ORG, 13, "start", "700"))
    b += r1
    b += (flip(r2, t1, T, 1) if kk == 0 else r2) + (flip(r3, t2, T, 1) if kk == 0 else r3)
    # điện tích đang đặt tại M
    q1 = charge(*M, MINUS, RB); q2 = charge(*M, "+", RR); q3 = charge(*M, MINUS, RB)
    if kk == 0:
        b += flip(q1, t1, T, 0)
        inner = flip(q2, t2, T, 0)
        b += f'<g opacity="0"><animate attributeName="opacity" values="0;1" keyTimes="0;{t1 / T:.4f}" calcMode="discrete" dur="{T:.2f}s" begin="indefinite" fill="freeze"/>{inner}</g>'
        b += f'<g opacity="0"><animate attributeName="opacity" values="0;1" keyTimes="0;{t2 / T:.4f}" calcMode="discrete" dur="{T:.2f}s" begin="indefinite" fill="freeze"/>{q3}</g>'
        return fig("d2-0", "0 0 420 210", "Lần lượt đặt ba điện tích khác nhau vào đúng cùng một điểm M của điện trường", b,
                   "Mô phỏng: ba điện tích lần lượt được đặt vào đúng điểm M, mỗi lần 2 s; điểm M không đổi.")
    b += q1
    return fig("d2-2", "0 0 420 210", "Dữ kiện: điện tích q1 đặt tại M có thế năng cho trước, sau đó đặt q2 và electron vào đúng M", b, "Dữ kiện đề cho; chọn mốc điện thế ở vô cực.")


# ───────────── Dạng 3 · proton rồi electron cùng đi từ M tới N ─────────────
def d3(kk):
    M = (100.0, 96.0); N = (320.0, 96.0); T = 5.0
    RB = "#38bdf8"; RR = "#f87171"
    b = seg(*M, *N, "currentColor", 1.4, "5 5", .5) + dot(*M, 3.5) + dot(*N, 3.5)
    b += lbl(M[0], M[1] + 28, "M", "currentColor", 14, "middle", "700") + lbl(N[0], N[1] + 28, "N", "currentColor", 14, "middle", "700")
    b += eq(M[0], M[1] - 34, "V", "M", " = 140 V", "currentColor", 14, "middle") + eq(N[0], N[1] - 34, "V", "N", " = 20 V", "currentColor", 14, "middle")
    b += charge(110, 158, "+", RR, 7) + lbl(124, 163, "proton: đi từ M đến N", "currentColor", 12, "start", "400")
    b += charge(110, 182, MINUS, RB, 7) + lbl(124, 187, "electron: đi từ M đến N", "currentColor", 12, "start", "400")
    pr = charge(*M, "+", RR); el = charge(*M, MINUS, RB)
    if kk == 0:
        b += flip(move(pr, line_pts(M, N, 20, 0, 20), T), T / 2, T, 0)
        b += f'<g opacity="0"><animate attributeName="opacity" values="0;1" keyTimes="0;0.5000" calcMode="discrete" dur="{T:.2f}s" begin="indefinite" fill="freeze"/>{move(el, line_pts(M, N, 20, 20, 0), T)}</g>'
        return fig("d3-0", "0 0 420 200", "Một proton rồi một electron lần lượt được đưa từ điểm M có điện thế 140 vôn đến điểm N có điện thế 20 vôn", b,
                   "Mô phỏng: proton đi từ M đến N (2,5 s), sau đó electron đi từ M đến N (2,5 s), tốc độ minh hoạ. Khoảng cách MN trên hình không ảnh hưởng đáp số.")
    b += pr
    return fig("d3-2", "0 0 420 200", "Dữ kiện: điện thế tại M là 140 vôn, tại N là 20 vôn; proton và electron đi từ M đến N", b, "Dữ kiện đề cho. Khoảng cách MN trên hình không ảnh hưởng đáp số.")


# ───────────── Dạng 4 · U = Ed: MN xiên 60°, điểm Q phía sau M ─────────────
def d4(kk):
    s = 12.0
    M = (136.0, 40.0); a = math.radians(60)
    N = (M[0] + s * 12 * math.cos(a), M[1] + s * 12 * math.sin(a))
    Q = (M[0] - s * 5, M[1])
    ys = [M[1], M[1] + (N[1] - M[1]) / 2, N[1], N[1] + (N[1] - M[1]) / 2]
    b = efield(ys, 24, 402)
    b += seg(*M, *N, GRN, 2.2, "7 5") + dot(*M, 3.5) + dot(*N, 3.5) + dot(*Q, 3.5)
    b += lbl(M[0] + 6, M[1] - 10, "M", "currentColor", 14, "start", "700") + lbl(Q[0], Q[1] - 12, "Q", "currentColor", 14, "middle", "700") + lbl(N[0] + 12, N[1] - 8, "N", "currentColor", 14, "start", "700")
    b += dim("", "b", Q[0], M[1] + 16, M[0], M[1] + 16, "", 0, 0) + lbl((Q[0] + M[0]) / 2, M[1] + 38, "5 cm", BLUE, 13, "middle", "700")
    b += arc(M[0], M[1], 34, -60, 0, RED, 1.8) + lbl(M[0] + 42, M[1] + 30, "60°", RED, 13, "start", "700")
    b += lbl(M[0] + 38 + 20, (M[1] + N[1]) / 2 + 22, "MN = 12 cm", GRN, 13, "start", "700")
    b += lbl(402, 20, "E = 2500 V/m", ORG, 14, "end", "700")
    b += eq(270, 92, "U", "MN", " = ?", ORG, 14) + eq(270, 202, "U", "MQ", " = ?", ORG, 14)
    if kk == 0:
        b += move(dot(*M, 6, GRN) + circ_ring(*M), line_pts(M, N, 40), 3.0)
        return fig("d4-0", "0 0 420 262", "Đầu dò chuyển từ điểm M đến điểm N trong điện trường đều; điểm Q nằm trên đường qua M song song với đường sức, phía sau M", b,
                   "Mô phỏng: đầu dò đi từ M đến N (3 s, tốc độ minh hoạ). Hình vẽ đúng góc 60° và đúng tỉ lệ các độ dài MN, MQ; khoảng cách giữa các đường sức không có ý nghĩa.")
    return fig("d4-2", "0 0 420 262", "Dữ kiện: điện trường đều E, đoạn MN hợp đường sức góc 60 độ, điểm Q cách M 5 cm trên đường qua M song song với đường sức", b,
               "Dữ kiện đề cho. Hình vẽ đúng góc 60° và đúng tỉ lệ các độ dài MN, MQ.")


def circ_ring(x, y, r=10, c=GRN):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="{c}" stroke-width="1.6"/>'


# ───────────── Dạng 5 · hai bản song song cách 5 cm: M, N, electron ─────────────
def d5(kk):
    s = 60.0; XL = 54.0; XR = XL + s * 5
    M = (XL + s * 1.5, 82.0); N = (XR - s * 1.0, 142.0)
    b = f'<rect x="{XL - 8}" y="28" width="8" height="160" fill="{RED}" fill-opacity=".3" stroke="{RED}" stroke-width="2"/>'
    b += f'<rect x="{XR}" y="28" width="8" height="160" fill="{BLUE}" fill-opacity=".3" stroke="{BLUE}" stroke-width="2"/>'
    b += efield([52, 112, 172], XL + 6, XR - 4)
    b += lbl(XL - 4, 18, "bản dương (+)", RED, 13, "middle", "700") + lbl(XR + 4, 18, "bản âm (−)", BLUE, 13, "middle", "700")
    b += lbl((XL + XR) / 2, 18, "U = 200 V", ORG, 14, "middle", "700")
    b += dot(*M, 3.5) + dot(*N, 3.5)
    b += lbl(M[0] + 8, M[1] - 8, "M", "currentColor", 14, "start", "700") + lbl(N[0] + 8, N[1] - 8, "N", "currentColor", 14, "start", "700")
    b += dim("", "b", XL, 208, M[0], 208, "", 0, 0) + lbl((XL + M[0]) / 2, 226, "1,5 cm", BLUE, 13, "middle", "700")
    b += dim("", "b", N[0], 208, XR, 208, "", 0, 0) + lbl((N[0] + XR) / 2, 226, "1 cm", BLUE, 13, "middle", "700")
    b += dim("", "o", XL, 244, XR, 244, "", 0, 0) + lbl((XL + XR) / 2, 262, "d = 5 cm", ORG, 13, "middle", "700")
    if kk == 0:
        b += lbl(XR - 90, 96, "electron", BLUE, 12, "end", "400")
        b += move(charge(*M, MINUS, BLUE), line_pts(M, N, 40), 3.0)
        return fig("d5-0", "0 0 420 272", "Electron được dịch chuyển từ điểm M đến điểm N trong điện trường đều giữa hai bản kim loại phẳng song song", b,
                   "Mô phỏng: electron được dịch chuyển từ M đến N với tốc độ minh hoạ (3 s). Hình vẽ đúng tỉ lệ khoảng cách giữa hai bản và các điểm M, N (60 px ứng 1 cm).")
    return fig("d5-2", "0 0 420 272", "Dữ kiện: hai bản song song cách nhau 5 cm, M cách bản dương 1,5 cm, N cách bản âm 1 cm", b,
               "Dữ kiện đề cho. Hình vẽ đúng tỉ lệ khoảng cách giữa hai bản và các điểm M, N.")
