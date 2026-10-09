"""Bài 23 · Bài 4. Bài tập về dao động điều hoà (Vật lí 11, chương 1 Dao động) — dựng scripts/data/bai-tap-mau/23.json từ đầu.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-23.py        (mẫu cấu trúc: build-hinh-57.py, đồ thị/sóng: build-hinh-33.py)

Quét số dạng (bước 0, làm trong phiên chính từ lý thuyết bài 23 + ngân hàng chủ đề bài 21/22; bài 23 là bài tổng hợp nên chưa có chủ đề
riêng trong question-topics.json → topic lấy YCCĐ con của bài 21, 22, 132 — tên nguyên văn):
  4 họ của lý thuyết: đọc phương trình/đồ thị · x–v–a · viết phương trình từ t=0 · thời gian–quãng đường bằng vòng tròn pha.
  Ngoài phạm vi (lý thuyết bài không dạy): con lắc lò xo, con lắc đơn, năng lượng → KHÔNG đưa vào.
5 dạng, cấp không giảm:
  1 (cấp 1) đọc phương trình có sin/dấu trừ → dạng chuẩn, A, φ, T, f, v_max, a_max           [topic 154]
  2 (cấp 2) hệ thức độc lập: hai cặp (x, |v|) → ω, T, A, a_max                                 [topic 159]
  3 (cấp 2) đọc đồ thị x–t → A, T, ω, φ, viết phương trình                                      [topic 155]
  4 (cấp 3) thời gian bằng vòng tròn pha: lần đầu qua O, lần thứ n qua x = −A/2                 [topic 154]
  5 (cấp 4) quãng đường, tốc độ TB, vận tốc TB trong Δt = nT + phần dư xuất phát từ A/2         [topic 247]
Quy ước theo lý thuyết bài 23: dạng chuẩn x = A cos(ωt+φ), A>0, φ∈(−π;π] · −cos α = cos(α+π), sin α = cos(α−π/2) · v² = ω²(A²−x²), a = −ω²x
· đi chiều dương → φ<0 · mốc O↔A/2 mất T/12, A/2↔biên T/6, O↔biên T/4 · quãng đường T/2 → 2A, T → 4A."""
import json, math, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "23.json")
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
PI = math.pi
VB = "0 0 420 132"


def mn(v):
    """Số có dấu trừ Unicode, dùng cho nhãn trục."""
    return str(v).replace("-", "−").replace(".", ",")


def track(p, cx, s, y, ticks, numerals=True, half=5.6):
    """Trục Ox nằm ngang (chiều dương sang phải), vạch chia theo ticks (cm), gốc O."""
    b = arrow(p, "g", cx - s * half, y, cx + s * half, y, 2) + lbl(cx + s * half - 2, y - 10, "x (cm)", GRN, 12, "end", "700")
    for v in ticks:
        b += seg(cx + s * v, y - 5, cx + s * v, y + 5, "currentColor", 1.6)
        if v == 0:
            b += lbl(cx + s * v, y + 22, "O", "currentColor", 13, "middle", "700")
        elif numerals:
            b += lbl(cx + s * v, y + 22, mn(v), "currentColor", 12, "middle", "600")
    return b


def mark(cx, s, y, v, c, text, up=True, anchor="middle"):
    """Cột mốc gạch đứt tại li độ v (cm) kèm nhãn."""
    x = cx + s * v
    return seg(x, y - 44, x, y + 8, c, 1.8, "5 4") + lbl(x, y - 50, text, c, 12, anchor, "700")


# ═════════════ Dạng 1 · x = −4 sin(5πt) cm ═════════════
def d1(k):
    p = f"d1{k}"; cx, s, y = 210, 24, 84
    b = defs(p) + track(p, cx, s, y, [-4, -2, 0, 2, 4])
    if k == 0:
        n, tot = 40, 0.8                       # hai chu kì (T = 0,4 s)
        pts = [(cx + s * (-4 * math.sin(5 * PI * tot * i / n)), y) for i in range(n + 1)]
        b += lbl(18, 24, "x = −4 sin(5πt)  cm", "currentColor", 14, "start", "700")
        b += ball(pts, 0, tot * 5 / n)         # phát chậm 5 lần
        return fig("d1-0", VB, "Vật dao động trên trục Ox theo phương trình x bằng trừ 4 sin 5 pi t, bắt đầu từ vị trí cân bằng", b,
                   "Mô phỏng: vật dao động theo đúng phương trình đề cho (đã làm chậm để quan sát; bấm Chạy mô phỏng).")
    b += lbl(18, 24, "Dạng chuẩn: x = A cos(ωt + φ)", "currentColor", 13, "start", "700")
    b += lbl(18, 44, "A > 0 · φ trong (−π; π]", "currentColor", 12, "start", "400")
    b += dot(cx, y, 5.5, RED) + lbl(cx - 8, y - 14, "t = 0: x₀, chiều đi?", RED, 12, "end", "700")
    return fig("d1-2", VB, "Trục Ox với gốc O; cần đưa phương trình về dạng chuẩn rồi đọc A và phi, xét x0 và chiều đi lúc t bằng 0", b, "Dữ kiện: đọc sau khi đưa về dạng chuẩn. " + NOTE)


# ═════════════ Dạng 2 · hệ thức độc lập: (3 cm; 16π), (4 cm; 12π) → ω = 4π, A = 5 cm ═════════════
def d2(k):
    p = f"d2{k}"; cx, y, L = 210, 84, 128
    b = defs(p) + arrow(p, "g", cx - L - 14, y, cx + L + 14, y, 2) + lbl(cx + L + 14, y + 22, "x", GRN, 13, "end", "700")
    b += seg(cx, y - 6, cx, y + 6, "currentColor", 1.8) + lbl(cx, y + 24, "O", "currentColor", 13, "middle", "700")
    if k == 0:
        n, tot = 72, 1.125                     # hai chu kì rưỡi, dừng ở O (T = 0,5 s), phát chậm, không nêu hệ số
        X = [cx + L * math.cos(4 * PI * tot * i / n) for i in range(n + 1)]
        V = [60 * -math.sin(4 * PI * tot * i / n) for i in range(n + 1)]
        dt = tot * 5 / n; dur = dt * n
        b += lbl(18, 24, "Một vật dao động điều hoà", "currentColor", 13, "start", "700")
        b += lbl(18, 44, "Mũi tên xanh: vận tốc", BLUE, 12, "start", "700")
        b += (f'<line stroke="{BLUE}" stroke-width="3" marker-end="url(#{p}-b)" x1="{X[0]:.1f}" y1="{y - 18}" x2="{X[0] + V[0]:.1f}" y2="{y - 18}">'
              f'{smil("x1", X, dur)}{smil("x2", [a + c for a, c in zip(X, V)], dur)}</line>')
        b += ball([(a, y) for a in X], 0, dt)
        return fig("d2-0", VB, "Vật dao động quanh vị trí cân bằng O, mũi tên vận tốc ngắn dần khi vật ra gần biên và dài nhất khi qua O", b,
                   "Mô phỏng: một vật dao động điều hoà (đã làm chậm; không theo tỉ lệ với số liệu của đề). Mũi tên vận tốc tính từ công thức.")
    x1, x2 = cx + 0.45 * L, cx + 0.75 * L
    b += seg(x1, y - 40, x1, y + 8, ORG, 1.8, "5 4") + seg(x2, y - 40, x2, y + 8, ORG, 1.8, "5 4")
    b += arrow(p, "b", x1, y - 30, x1 + 56, y - 30, 3) + arrow(p, "b", x2, y - 12, x2 + 42, y - 12, 3)
    b += sub(x1 - 4, y - 46, "x", "1", ORG, 13, "end") + sub(x2 + 4, y - 46, "x", "2", ORG, 13, "start")
    b += sub(x1 + 62, y - 26, "v", "1", BLUE, 13) + sub(x2 + 48, y - 8, "v", "2", BLUE, 13)
    b += lbl(cx + L + 8, y + 42, "biên: x = A ?", "currentColor", 12, "end", "700")
    return fig("d2-2", VB, "Hai li độ x1 và x2 trên trục Ox, mỗi li độ có vận tốc tương ứng v1 và v2; vận tốc nhỏ hơn khi li độ lớn hơn", b, "Dữ kiện: hai cặp (li độ, tốc độ) của cùng một dao động. " + NOTE)


# ═════════════ Dạng 3 · đồ thị x = 4cos(5πt/3 + π/3): A = 4, T = 1,2, ω = 5π/3, φ = π/3 ═════════════
A3, W3, PH3 = 4.0, 5 * PI / 3, PI / 3
GX0, GSX, GYC, GSY = 48, 175, 106, 20


def gpx(t): return GX0 + GSX * t
def gpy(x): return GYC - GSY * x
def x3(t): return A3 * math.cos(W3 * t + PH3)


def graph_base(p, guides=True):
    b = defs(p)
    for i in range(0, 11):                                  # lưới thời gian mỗi 0,2 s
        t = 0.2 * i
        b += seg(gpx(t), gpy(4), gpx(t), gpy(-4), "currentColor", 1, "", .13) + seg(gpx(t), gpy(-4), gpx(t), gpy(-4) + 5, "currentColor", 1.4)
        b += lbl(gpx(t), gpy(-4) + 20, mn(round(t, 1)), "currentColor", 11, "middle", "600")
    for v in (-4, -2, 0, 2, 4):
        b += seg(GX0, gpy(v), gpx(2.0), gpy(v), "currentColor", 1, "", .13) + lbl(GX0 - 8, gpy(v) + 4, mn(v), "currentColor", 11, "end", "600")
    b += seg(GX0, GYC, gpx(2.0) + 6, GYC, "currentColor", 1.8) + seg(GX0, gpy(4) - 10, GX0, gpy(-4) + 4, "currentColor", 1.8)
    b += lbl(GX0 + 6, 14, "x (cm)", "currentColor", 12, "start", "700") + lbl(gpx(2.0) + 8, gpy(-4) + 38, "t (s)", "currentColor", 12, "end", "700")
    pts = [(gpx(0.02 * i), gpy(x3(0.02 * i))) for i in range(101)]
    b += poly(pts, GRN, 2.6)
    b += dot(gpx(0.4), gpy(-4), 4.5, ORG) + dot(gpx(1.0), gpy(4), 4.5, ORG) + dot(gpx(0), gpy(2), 5, RED)
    return b


def d3(k):
    p = f"d3{k}"; VB3 = "0 0 420 228"
    b = graph_base(p)
    if k == 0:
        n, tot = 50, 2.0; ts = [tot * i / n for i in range(n + 1)]
        X = [gpx(t) for t in ts]; Y = [gpy(x3(t)) for t in ts]; dur = tot * 2        # phát chậm 2 lần
        b += (f'<line stroke="{RED}" stroke-width="1.4" stroke-dasharray="4 3" opacity=".75" y1="{GYC}" x1="{X[0]:.1f}" x2="{X[0]:.1f}" y2="{Y[0]:.1f}">'
              f'{smil("x1", X, dur)}{smil("x2", X, dur)}{smil("y2", Y, dur)}</line>')
        b += dotanim3(X, Y, dur)
        return fig("d3-0", VB3, "Đồ thị li độ theo thời gian của một vật dao động điều hoà, một điểm chạy dọc đồ thị", b,
                   "Đồ thị đề cho: x tính bằng cm, t bằng giây. Điểm chạy dọc đồ thị theo thời gian (chạy chậm 2 lần).")
    b += lbl(gpx(1.3), gpy(3.4), "đỉnh–đáy = 2A", ORG, 12, "start", "700")
    b += lbl(gpx(1.3), gpy(2.5), "đỉnh–đỉnh = T", ORG, 12, "start", "700")
    b += lbl(gpx(1.3), gpy(1.6), "t = 0: x₀, chiều đi?", RED, 12, "start", "700")
    return fig("d3-2", VB3, "Đồ thị x theo t: điểm đỉnh và đáy màu cam, điểm lúc t bằng 0 màu đỏ cần xét vị trí và chiều đi", b, "Dữ kiện: đọc đỉnh, đáy, mốc thời gian và điểm lúc t = 0. " + NOTE)


def dotanim3(X, Y, dur):
    return (f'<circle cx="{X[0]:.1f}" cy="{Y[0]:.1f}" r="5.5" fill="{RED}" stroke="currentColor" stroke-width="1.5">'
            f'{smil("cx", X, dur)}{smil("cy", Y, dur)}</circle>')


# ═════════════ Dạng 4 · x = 6cos(4πt + π/3): qua O lần đầu 1/24 s; qua x = −3 lần thứ 5 → 13/12 s ═════════════
def d4(k):
    p = f"d4{k}"
    if k == 0:
        cx, s, y = 210, 24, 84
        b = defs(p) + track(p, cx, s, y, [-6, -3, 0, 3, 6])
        b += mark(cx, s, y, -3, ORG, "x = −3 cm") + mark(cx, s, y, 3, RED, "t = 0")
        n, tot = 72, 1.5                       # ba chu kì (T = 0,5 s)
        pts = [(cx + s * 6 * math.cos(4 * PI * tot * i / n + PI / 3), y) for i in range(n + 1)]
        b += lbl(18, 14, "x = 6 cos(4πt + π/3)  cm", "currentColor", 13, "start", "700")
        b += ball(pts, 0, tot * 4 / n)         # phát chậm 4 lần
        return fig("d4-0", VB, "Vật dao động từ li độ 3 cm, đi qua vị trí cân bằng và qua li độ trừ 3 cm nhiều lần", b,
                   "Mô phỏng: vật dao động theo phương trình đề cho, xuất phát từ li độ đánh dấu t = 0 (chạy chậm 4 lần).")
    cx, cy, R = 110, 104, 68
    b = defs(p) + f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="currentColor" stroke-width="1.6"/>'
    b += arrow(p, "g", cx - R - 14, cy, cx + R + 22, cy, 2) + lbl(cx + R + 22, cy + 16, "x", GRN, 13, "end", "700")
    b += seg(cx, cy - R - 12, cx, cy + R + 12, "currentColor", 1.2, "", .5) + lbl(cx - 8, cy + 16, "O", "currentColor", 13, "end", "700")
    mx, my = cx + R * math.cos(PI / 3), cy - R * math.sin(PI / 3)
    b += seg(cx, cy, mx, my, RED, 2.6) + dot(mx, my, 5.5, RED) + lbl(mx + 8, my - 6, "M₀ (t = 0)", RED, 12, "start", "700")
    b += seg(mx, my, mx, cy, RED, 1.2, "4 4") + dot(mx, cy, 3.5, GRN)
    xl = cx - R / 2
    b += seg(xl, cy - R + 4, xl, cy + R - 4, ORG, 1.8, "6 4")
    for sg in (-1, 1):
        b += dot(xl, cy + sg * R * math.sin(2 * PI / 3), 4.5, ORG)
    b += lbl(xl, cy + R + 22, "x = −3 cm", ORG, 12, "middle", "700")
    for i, t in enumerate(["M quay ngược chiều", "kim đồng hồ", "Góc 2π ứng với T", "x = −3 cm cắt vòng", "tròn tại hai điểm"]):
        b += lbl(246, 52 + i * 22, t, "currentColor" if i < 3 else ORG, 12, "start", "700")
    return fig("d4-2", "0 0 420 214", "Vòng tròn pha bán kính A: điểm M0 lúc t bằng 0 ở nửa trên, đường thẳng đứng x bằng trừ 3 cm cắt vòng tròn tại hai điểm", b,
               "Dữ kiện: vòng tròn pha, M quay đều, hình chiếu của M lên Ox là li độ. " + NOTE)


# ═════════════ Dạng 5 · A = 4 cm, T = 0,6 s, t = 0 ở x = 2 cm đi về biên âm; Δt = 1,4 s ═════════════
def d5(k):
    p = f"d5{k}"
    if k == 0:
        cx, s, y = 210, 24, 84
        b = defs(p) + track(p, cx, s, y, [-4, 0, 4], numerals=False)
        b += mark(cx, s, y, 2, RED, "t = 0")
        n, tot = 56, 1.4
        pts = [(cx + s * 4 * math.cos(2 * PI / 0.6 * tot * i / n + PI / 3), y) for i in range(n + 1)]
        b += ball(pts, 0, tot * 3 / n)         # phát chậm 3 lần
        return fig("d5-0", VB, "Vật dao động quanh vị trí cân bằng, xuất phát từ vị trí đánh dấu và đi về phía biên âm", b,
                   "Mô phỏng: vật xuất phát từ vị trí đánh dấu, đi về phía biên âm, chạy trong khoảng thời gian đề cho (chạy chậm 3 lần). Hình không có thang đo.")
    b = defs(p)
    X0, W = 24, 372; u = W / 1.4
    segs = [(0, 0.6, "T"), (0.6, 1.2, "T"), (1.2, 1.4, "?")]
    for a, c, t in segs:
        b += f'<rect x="{X0 + u * a:.1f}" y="76" width="{u * (c - a):.1f}" height="30" fill="none" stroke="currentColor" stroke-width="2"/>'
        b += lbl(X0 + u * (a + c) / 2, 96, t, ORG if t == "?" else "currentColor", 14, "middle", "700")
    b += dim(p, "g", X0, 62, X0 + W, 62, "Δt từ t = 0 đến lúc cần tính", X0 + 70, 52)
    b += lbl(X0 + u * 0.6, 128, "mỗi T đi được 4A", "currentColor", 12, "middle", "700")
    b += lbl(X0 + u * 1.3 - 6, 150, "phần dư: theo dõi vị trí", ORG, 12, "end", "700")
    b += lbl(18, 20, "t = 0: x₀ = A/2, đi về biên âm", RED, 12, "start", "700")
    return fig("d5-2", "0 0 420 160", "Khoảng thời gian chia thành hai chu kì đầy đủ và một phần dư chưa biết", b, "Dữ kiện: tách Δt thành nT và phần dư. " + NOTE)


BUILD = [d1, d2, d3, d4, d5]

# ───────────────────────── Đề ─────────────────────────
DANG = [
 dict(label="Dạng 1 · Dễ · Đọc phương trình có sin và dấu trừ: biên độ, pha ban đầu, chu kì, tốc độ cực đại",
      topic="Li độ, biên độ, chu kì, tần số, pha ban đầu",
      problem_html="<p>Một vật dao động điều hoà theo phương trình $x=-4\\sin(5\\pi t)$, trong đó $x$ tính bằng cm, $t$ tính bằng giây.</p>"
                   "<ol type=\"a\"><li>Đưa phương trình về dạng chuẩn; xác định biên độ và pha ban đầu.</li><li>Tính chu kì và tần số.</li>"
                   "<li>Tính tốc độ cực đại và gia tốc cực đại.</li><li>Lúc $t=0$ vật ở đâu và đang đi theo chiều nào?</li></ol>"),
 dict(label="Dạng 2 · Trung bình · Hệ thức độc lập: từ hai cặp (li độ, tốc độ) tìm tần số góc và biên độ",
      topic="Hệ thức độc lập với thời gian",
      problem_html="<p>Một vật dao động điều hoà. Khi vật ở li độ $x_1=3{,}0\\ \\text{cm}$ thì tốc độ của vật là $16\\pi\\ \\text{cm/s}$; "
                   "khi vật ở li độ $x_2=4{,}0\\ \\text{cm}$ thì tốc độ là $12\\pi\\ \\text{cm/s}$.</p>"
                   "<ol type=\"a\"><li>Tính tần số góc và chu kì.</li><li>Tính biên độ.</li><li>Tính gia tốc cực đại.</li></ol>"),
 dict(label="Dạng 3 · Trung bình · Đọc đồ thị li độ – thời gian rồi viết phương trình dao động",
      topic="Viết phương trình dao động điều hoà",
      problem_html="<p>Đồ thị li độ – thời gian của một vật dao động điều hoà được cho như hình ($x$ tính bằng cm, $t$ tính bằng giây).</p>"
                   "<ol type=\"a\"><li>Đọc đồ thị để tìm biên độ và chu kì.</li><li>Tính tần số góc.</li>"
                   "<li>Xác định pha ban đầu rồi viết phương trình dao động.</li></ol>"),
 dict(label="Dạng 4 · Khó · Vòng tròn pha: thời điểm vật qua một vị trí lần đầu và lần thứ n",
      topic="Li độ, biên độ, chu kì, tần số, pha ban đầu",
      problem_html="<p>Một vật dao động điều hoà theo phương trình $x=6\\cos\\left(4\\pi t+\\dfrac{\\pi}{3}\\right)$ cm, $t$ tính bằng giây.</p>"
                   "<ol type=\"a\"><li>Vật đi qua vị trí cân bằng lần đầu tiên vào thời điểm nào?</li>"
                   "<li>Vật đi qua li độ $x=-3\\ \\text{cm}$ lần thứ 5 vào thời điểm nào? (Mỗi lần đi qua tính một lần, kể cả hai chiều.)</li></ol>"),
 dict(label="Dạng 5 · Khó · Quãng đường, tốc độ trung bình và vận tốc trung bình trong khoảng thời gian dài",
      topic="Tính quãng đường vật đi được trong dao động điều hoà",
      problem_html="<p>Một vật dao động điều hoà với chu kì $T=0{,}6\\ \\text{s}$ và biên độ $A=4\\ \\text{cm}$. Lúc $t=0$ vật ở li độ $x=2\\ \\text{cm}$ "
                   "và đang đi về phía biên âm. Xét khoảng thời gian từ $t=0$ đến $t=1{,}4\\ \\text{s}$.</p>"
                   "<ol type=\"a\"><li>Tính quãng đường vật đi được.</li><li>Tính tốc độ trung bình và vận tốc trung bình trong khoảng thời gian đó.</li></ol>"),
]

# ───────────────────────── Bảng phân tích đề ─────────────────────────
ANALYSIS = [
 [("\"$x=-4\\sin(5\\pi t)$, $x$ tính bằng cm\"", "$x=-4\\sin(5\\pi t)\\ \\text{cm}$", "Khái niệm: dao động điều hoà. Dạng chuẩn $x=A\\cos(\\omega t+\\varphi)$"),
  ("\"biên độ, pha ban đầu\"", "Cần $A$, $\\varphi$", "⚠ Chỉ đọc $A$, $\\varphi$ sau khi đưa về dạng chuẩn: $\\sin$ đổi sang $\\cos$ lệch $\\dfrac{\\pi}{2}$; dấu trừ thêm $\\pi$; $A\\gt0$"),
  ("\"chu kì, tần số\"", "$\\omega$ là hệ số của $t$", "$T=\\dfrac{2\\pi}{\\omega}$; $f=\\dfrac{1}{T}$"),
  ("\"tốc độ cực đại, gia tốc cực đại\"", "Cần $|v|_{max}$, $|a|_{max}$", "$|v|_{max}=A\\omega$; $|a|_{max}=\\omega^2A$"),
  ("\"lúc $t=0$\" (ngầm)", "Thay $t=0$", "$x_0=A\\cos\\varphi$; $v_0=-A\\omega\\sin\\varphi$ → dấu của $v_0$ cho chiều đi")],
 [("\"khi ở li độ $x_1=3{,}0$ cm thì tốc độ $16\\pi$ cm/s\"", "$x_1=3{,}0$ cm; $|v_1|=16\\pi$ cm/s", "Hệ thức độc lập với thời gian: $v^2=\\omega^2(A^2-x^2)$"),
  ("\"khi ở li độ $x_2=4{,}0$ cm thì tốc độ $12\\pi$ cm/s\"", "$x_2=4{,}0$ cm; $|v_2|=12\\pi$ cm/s", "Cùng một dao động nên cùng $A$, cùng $\\omega$ → hai phương trình, hai ẩn"),
  ("\"tốc độ\" (không phải vận tốc)", "Chỉ biết độ lớn $|v|$", "⚠ $v^2$ không cần dấu của $v$; $x$ (cm) và $v$ (cm/s) phải cùng hệ đơn vị"),
  ("\"tần số góc và chu kì\"", "Cần $\\omega$, $T$", "Trừ vế hai hệ thức để mất $A$; $T=\\dfrac{2\\pi}{\\omega}$"),
  ("\"biên độ\"", "Cần $A$", "$A^2=x^2+\\dfrac{v^2}{\\omega^2}$"),
  ("\"gia tốc cực đại\"", "Cần $|a|_{max}$", "$|a|_{max}=\\omega^2A$")],
 [("\"đồ thị li độ – thời gian\"", "Đọc trên hình: đỉnh, đáy, các mốc thời gian", "Khái niệm: đồ thị $x$–$t$ là đường hình sin. Đỉnh–đáy $=2A$; hai đỉnh liền kề cách nhau $T$"),
  ("\"biên độ\"", "Giá trị của đỉnh và đáy trên trục $x$", "$A=\\dfrac{x_{max}-x_{min}}{2}$"),
  ("\"chu kì\"", "Hai mốc thời gian trên trục $t$", "⚠ Đỉnh và đáy liền kề cách nhau $\\dfrac{T}{2}$, không phải $T$"),
  ("\"tần số góc\"", "Cần $\\omega$", "$\\omega=\\dfrac{2\\pi}{T}$"),
  ("\"pha ban đầu\"", "$x_0$ lúc $t=0$ và chiều đi của đường cong", "$\\cos\\varphi=\\dfrac{x_0}{A}$; ⚠ đường cong đi xuống thì $\\varphi\\gt0$, đi lên thì $\\varphi\\lt0$"),
  ("\"viết phương trình\"", "Gộp $A$, $\\omega$, $\\varphi$", "$x=A\\cos(\\omega t+\\varphi)$")],
 [("\"$x=6\\cos(4\\pi t+\\frac{\\pi}{3})$\"", "$A=6$ cm; $\\omega=4\\pi$ rad/s; $\\varphi=\\dfrac{\\pi}{3}$", "Vòng tròn pha: M bán kính $A$, góc ban đầu $\\varphi$, quay ngược chiều kim đồng hồ với tốc độ góc $\\omega$"),
  ("lúc $t=0$ (ngầm)", "Góc ban đầu $\\varphi=\\dfrac{\\pi}{3}$ của M; cần biết chiều đi", "⚠ Chiều đi lúc $t=0$ đọc từ nửa của vòng tròn chứa M: nửa trên ứng với $v\\lt0$, nửa dưới ứng với $v\\gt0$"),
  ("\"qua vị trí cân bằng lần đầu\"", "$x=0$", "M ở góc $\\pm\\dfrac{\\pi}{2}$; tìm góc M quét $\\Delta\\varphi$ từ vị trí đầu"),
  ("\"qua li độ $x=-3$ cm lần thứ 5\"", "$x=-3\\ \\text{cm}$ ứng với đường thẳng đứng trên hình", "⚠ Mỗi vòng M cắt đường $x=-3$ cm hai lần; đếm các lần theo thứ tự M gặp đường đó"),
  ("\"vào thời điểm nào\"", "Cần $t$", "$\\Delta t=\\dfrac{\\Delta\\varphi}{\\omega}$ (góc $2\\pi$ ứng với $T$)")],
 [("\"chu kì $T=0{,}6$ s, biên độ $A=4$ cm\"", "$T=0{,}6$ s; $A=4$ cm", "Một chu kì đi $4A$; nửa chu kì đi $2A$"),
  ("\"lúc $t=0$ ở li độ 2 cm, đi về phía biên âm\"", "$x_0=2\\ \\text{cm}=\\dfrac{A}{2}$; $v_0\\lt0$", "⚠ Xuất phát từ $\\dfrac{A}{2}$, không phải O hay biên: phần dư $\\dfrac{T}{4}$ không cho đúng $A$"),
  ("\"từ $t=0$ đến $t=1{,}4$ s\"", "$\\Delta t=1{,}4$ s", "Tách $\\Delta t=nT+\\Delta t'$; $n$ chu kì đầy đủ đi $4nA$"),
  ("\"quãng đường\"", "Cần $s$", "Cộng từng đoạn: $s=4nA+s'$; $s'$ theo dõi bằng các mốc $\\dfrac{T}{12}$, $\\dfrac{T}{4}$ hoặc vòng tròn pha"),
  ("\"tốc độ trung bình\"", "Cần $\\dfrac{s}{\\Delta t}$", "Tốc độ TB $=\\dfrac{s}{\\Delta t}$, luôn dương"),
  ("\"vận tốc trung bình\"", "Cần $\\dfrac{x_2-x_1}{\\Delta t}$", "⚠ Vận tốc TB dùng độ dời (có dấu), không dùng quãng đường")],
]

# ───────────────────────── Lời giải ─────────────────────────
R1 = ["<strong>Khái niệm:</strong> dao động điều hoà, li độ biến thiên theo $\\cos$ (hoặc $\\sin$) của thời gian.",
      "<strong>Dạng chuẩn:</strong> $x=A\\cos(\\omega t+\\varphi)$, với $A\\gt0$ và $\\varphi\\in(-\\pi;\\pi]$.",
      "$T=\\dfrac{2\\pi}{\\omega}$ · $f=\\dfrac{1}{T}$ · $|v|_{max}=A\\omega$ · $|a|_{max}=\\omega^2A$",
      "⚠ <strong>Điều kiện:</strong> chỉ đọc $A$, $\\varphi$ sau khi đưa về dạng chuẩn: $\\sin\\alpha=\\cos\\left(\\alpha-\\dfrac{\\pi}{2}\\right)$ và $-\\cos\\alpha=\\cos(\\alpha+\\pi)$."]
R2 = ["<strong>Khái niệm:</strong> trong dao động điều hoà, $x$ và $v$ vuông pha nên có hệ thức không chứa $t$.",
      "<strong>Hệ thức độc lập:</strong> $v^2=\\omega^2(A^2-x^2)$, hay $A^2=x^2+\\dfrac{v^2}{\\omega^2}$",
      "$T=\\dfrac{2\\pi}{\\omega}$ · $|a|_{max}=\\omega^2A$",
      "⚠ <strong>Điều kiện:</strong> $x$ (cm) và $v$ (cm/s) cùng hệ đơn vị; hai lần đo là cùng một dao động (cùng $A$, cùng $\\omega$)."]
R3 = ["<strong>Khái niệm:</strong> đồ thị $x$–$t$ của dao động điều hoà là đường hình sin.",
      "<strong>Đọc đồ thị:</strong> đỉnh–đáy $=2A$ · đỉnh–đỉnh $=T$ · đỉnh–đáy liền kề $=\\dfrac{T}{2}$",
      "$\\omega=\\dfrac{2\\pi}{T}$ · $\\cos\\varphi=\\dfrac{x_0}{A}$",
      "⚠ <strong>Điều kiện:</strong> chọn dấu $\\varphi$ theo chiều đi lúc $t=0$: đi xuống thì $\\varphi\\gt0$, đi lên thì $\\varphi\\lt0$."]
R4 = ["<strong>Khái niệm:</strong> vòng tròn pha: M bán kính $A$, quay ngược chiều kim đồng hồ; hình chiếu của M lên $Ox$ là $x$.",
      "<strong>Định luật:</strong> M quay đều với tốc độ góc $\\omega$; góc $2\\pi$ ứng với $T$.",
      "$\\Delta t=\\dfrac{\\Delta\\varphi}{\\omega}$ · mốc: O ↔ $\\dfrac{A}{2}$ mất $\\dfrac{T}{12}$; $\\dfrac{A}{2}$ ↔ biên mất $\\dfrac{T}{6}$",
      "⚠ <strong>Điều kiện:</strong> M xuất phát ở góc $\\varphi$ (không phải $0$); nửa trên là $v\\lt0$; mỗi vòng M cắt một đường $x=\\text{const}$ hai lần."]
R5 = ["<strong>Khái niệm:</strong> quãng đường (cộng từng đoạn, luôn dương) khác độ dời (vị trí cuối trừ vị trí đầu, có dấu).",
      "<strong>Định luật:</strong> một chu kì đi $4A$; nửa chu kì đi $2A$ (xuất phát từ vị trí bất kì).",
      "Tốc độ TB $=\\dfrac{s}{\\Delta t}$ · vận tốc TB $=\\dfrac{x_2-x_1}{\\Delta t}$",
      "⚠ <strong>Điều kiện:</strong> phần dư $\\dfrac{T}{4}$ chỉ cho đúng $A$ khi xuất phát từ O hoặc biên; còn lại phải theo dõi vị trí (vòng tròn pha)."]

SOLS = [
 sol(R1, [
  ("Đưa về dạng chuẩn", [P("Đổi $\\sin$ sang $\\cos$:"), M(r"-\sin\alpha=-\cos\left(\alpha-\dfrac{\pi}{2}\right)"),
                         P("Dấu trừ thêm $\\pi$ vào pha:"), M(r"-\cos\left(\alpha-\dfrac{\pi}{2}\right)=\cos\left(\alpha-\dfrac{\pi}{2}+\pi\right)=\cos\left(\alpha+\dfrac{\pi}{2}\right)"),
                         A(r"x=4\cos\left(5\pi t+\dfrac{\pi}{2}\right)\ \text{cm}"), P("Đọc: $A=4\\ \\text{cm}$, $\\varphi=\\dfrac{\\pi}{2}\\ \\text{rad}$, $\\omega=5\\pi\\ \\text{rad/s}$.")]),
  ("Chu kì và tần số", [M(r"T=\dfrac{2\pi}{\omega}=\dfrac{2\pi}{5\pi}"), A(r"T=0{,}4\ \text{s}"), M(r"f=\dfrac{1}{T}=\dfrac{1}{0{,}4}"), A(r"f=2{,}5\ \text{Hz}")]),
  ("Tốc độ cực đại và gia tốc cực đại", [M(r"|v|_{max}=A\omega=4\cdot5\pi"), A(r"|v|_{max}=20\pi\approx62{,}8\ \text{cm/s}"),
                                         M(r"|a|_{max}=\omega^2A=(5\pi)^2\cdot4=100\pi^2"), A(r"|a|_{max}\approx987\ \text{cm/s}^2")]),
  ("Lúc $t=0$", [M(r"x_0=4\cos\dfrac{\pi}{2}=0"), M(r"v_0=-A\omega\sin\varphi=-20\pi\sin\dfrac{\pi}{2}=-20\pi\ \text{cm/s}\ \lt0"),
                 A("T:Vật ở <strong>O</strong>, đang đi theo <strong>chiều âm</strong>."),
                 P("Kiểm tra trực tiếp: $x=-4\\sin(5\\pi t)$ nhận giá trị âm ngay sau $t=0$ ✓. Đơn vị: cm/s và cm/s² ✓.")])],
  ["a) $A=4\\ \\text{cm}$ · $\\varphi=\\dfrac{\\pi}{2}\\ \\text{rad}$", "b) $T=0{,}4\\ \\text{s}$ · $f=2{,}5\\ \\text{Hz}$",
   "c) $|v|_{max}\\approx62{,}8\\ \\text{cm/s}$ · $|a|_{max}\\approx987\\ \\text{cm/s}^2$", "d) Lúc $t=0$ vật ở O, đi theo chiều âm"],
  "Nhận dạng: đề cho <strong>phương trình có $\\sin$ hoặc dấu trừ</strong> → đưa về $A\\cos(\\omega t+\\varphi)$ rồi mới đọc."),
 sol(R2, [
  ("Tần số góc", [P("Viết hệ thức độc lập cho hai vị trí:"), M(r"v_1^2=\omega^2(A^2-x_1^2)"), M(r"v_2^2=\omega^2(A^2-x_2^2)"),
                  P("Trừ vế theo vế để mất $A$:"), M(r"v_1^2-v_2^2=\omega^2(x_2^2-x_1^2)"),
                  M(r"\omega^2=\dfrac{(16\pi)^2-(12\pi)^2}{4^2-3^2}=\dfrac{112\pi^2}{7}=16\pi^2"), A(r"\omega=4\pi\approx12{,}6\ \text{rad/s}")]),
  ("Chu kì", [M(r"T=\dfrac{2\pi}{\omega}=\dfrac{2\pi}{4\pi}"), A(r"T=0{,}5\ \text{s}")]),
  ("Biên độ", [M(r"A^2=x_1^2+\dfrac{v_1^2}{\omega^2}=3^2+\dfrac{(16\pi)^2}{(4\pi)^2}=9+16=25"), A(r"A=5\ \text{cm}")]),
  ("Gia tốc cực đại", [M(r"|a|_{max}=\omega^2A=16\pi^2\cdot5=80\pi^2"), A(r"|a|_{max}\approx790\ \text{cm/s}^2\ \ (\approx7{,}9\ \text{m/s}^2)")]),
  ("Kiểm tra", [P("Thử với $x_2$: $v_2=\\omega\\sqrt{A^2-x_2^2}=4\\pi\\sqrt{25-16}=12\\pi\\ \\text{cm/s}$ ✓ khớp đề."),
                P("$A=5\\ \\text{cm}\\gt4\\ \\text{cm}=x_2$ nên $x_2$ nằm trong đoạn dao động ✓. Đơn vị: rad/s · cm = cm/s ✓.")])],
  ["a) $\\omega=4\\pi\\approx12{,}6\\ \\text{rad/s}$ · $T=0{,}5\\ \\text{s}$", "b) $A=5\\ \\text{cm}$", "c) $|a|_{max}\\approx790\\ \\text{cm/s}^2$"],
  "Nhận dạng: đề cho <strong>hai cặp (li độ, tốc độ)</strong> hoặc một cặp và hỏi biên độ → hệ thức độc lập, trừ vế để mất $A$."),
 sol(R3, [
  ("Đọc biên độ", [P("Đỉnh ở $x=+4\\ \\text{cm}$, đáy ở $x=-4\\ \\text{cm}$:"), M(r"A=\dfrac{4-(-4)}{2}"), A(r"A=4\ \text{cm}")]),
  ("Đọc chu kì", [P("Đáy ở $t=0{,}4\\ \\text{s}$, đỉnh liền sau ở $t=1{,}0\\ \\text{s}$:"), M(r"\dfrac{T}{2}=1{,}0-0{,}4=0{,}6\ \text{s}"), A(r"T=1{,}2\ \text{s}")]),
  ("Tần số góc", [M(r"\omega=\dfrac{2\pi}{T}=\dfrac{2\pi}{1{,}2}"), A(r"\omega=\dfrac{5\pi}{3}\approx5{,}24\ \text{rad/s}")]),
  ("Pha ban đầu", [P("Đồ thị cắt trục $x$ ở $x_0=2\\ \\text{cm}$ lúc $t=0$:"), M(r"\cos\varphi=\dfrac{x_0}{A}=\dfrac{2}{4}=\dfrac12"), M(r"\varphi=\pm\dfrac{\pi}{3}"),
                   P("Đường cong đang đi xuống ($v_0\\lt0$) nên chọn dấu dương:"), A(r"\varphi=\dfrac{\pi}{3}\ \text{rad}")]),
  ("Phương trình và kiểm tra", [A(r"x=4\cos\left(\dfrac{5\pi}{3}t+\dfrac{\pi}{3}\right)\ \text{cm}"),
                                P("Kiểm tra $t=0$: $x=4\\cos\\dfrac{\\pi}{3}=2\\ \\text{cm}$ ✓."),
                                P("Kiểm tra $t=0{,}4\\ \\text{s}$: pha $=\\pi$, $x=-4\\ \\text{cm}$ (đáy) ✓."),
                                P("Kiểm tra $t=1{,}0\\ \\text{s}$: pha $=2\\pi$, $x=4\\ \\text{cm}$ (đỉnh) ✓.")])],
  ["a) $A=4\\ \\text{cm}$ · $T=1{,}2\\ \\text{s}$", "b) $\\omega=\\dfrac{5\\pi}{3}\\approx5{,}24\\ \\text{rad/s}$",
   "c) $\\varphi=\\dfrac{\\pi}{3}$ · $x=4\\cos\\left(\\dfrac{5\\pi}{3}t+\\dfrac{\\pi}{3}\\right)\\ \\text{cm}$"],
  "Nhận dạng: đề cho <strong>đồ thị $x$–$t$</strong> → đỉnh–đáy cho $A$, đỉnh–đỉnh cho $T$, điểm lúc $t=0$ và chiều đi cho $\\varphi$."),
 sol(R4, [
  ("Đặt M lúc $t=0$", [M(r"x_0=6\cos\dfrac{\pi}{3}=3\ \text{cm}"),
                       A("T:M xuất phát ở góc $\\dfrac{\\pi}{3}$, thuộc <strong>nửa trên</strong>: vật đang đi về biên âm.")]),
  ("Lần đầu qua vị trí cân bằng", [P("Vật qua O khi M tới góc $\\dfrac{\\pi}{2}$:"), M(r"\Delta\varphi=\dfrac{\pi}{2}-\dfrac{\pi}{3}=\dfrac{\pi}{6}"),
                                   M(r"t_1=\dfrac{\Delta\varphi}{\omega}=\dfrac{\pi/6}{4\pi}=\dfrac{1}{24}"), A(r"t_1\approx0{,}0417\ \text{s}"),
                                   P("Kiểm tra mốc: $\\dfrac{T}{12}=\\dfrac{0{,}5}{12}=\\dfrac{1}{24}\\ \\text{s}$ ✓ (từ $\\dfrac{A}{2}$ về O).")]),
  ("Góc M quét tới lần thứ 5", [P("$x=-3\\ \\text{cm}=-\\dfrac{A}{2}$ ứng với M ở góc $\\dfrac{2\\pi}{3}$ hoặc $\\dfrac{4\\pi}{3}$ (cộng thêm $2\\pi$ mỗi vòng). Các lần theo thứ tự:"),
                                M(r"\dfrac{2\pi}{3}\ ;\ \dfrac{4\pi}{3}\ ;\ \dfrac{2\pi}{3}+2\pi\ ;\ \dfrac{4\pi}{3}+2\pi\ ;\ \dfrac{2\pi}{3}+4\pi"),
                                P("Lần thứ 5 ở góc $\\dfrac{2\\pi}{3}+4\\pi$. Góc M quét kể từ $\\dfrac{\\pi}{3}$:"),
                                M(r"\Delta\varphi=\dfrac{2\pi}{3}+4\pi-\dfrac{\pi}{3}=\dfrac{13\pi}{3}"), A(r"\Delta\varphi=\dfrac{13\pi}{3}\approx4{,}33\pi\ \text{rad}")]),
  ("Thời điểm lần thứ 5", [M(r"t_5=\dfrac{\Delta\varphi}{\omega}=\dfrac{13\pi/3}{4\pi}=\dfrac{13}{12}"), A(r"t_5\approx1{,}08\ \text{s}")]),
  ("Kiểm tra", [P("Cách khác: $T=\\dfrac{2\\pi}{4\\pi}=0{,}5\\ \\text{s}$. Hai chu kì đầy đủ đi qua $x=-3$ đúng 4 lần; lần thứ 5 cần thêm $\\dfrac{T}{6}$ (từ $\\dfrac{A}{2}$ qua O tới $-\\dfrac{A}{2}$)."),
                M(r"2T+\dfrac{T}{6}=1{,}0+\dfrac{1}{12}=\dfrac{13}{12}\ \text{s}\ \ ✓")])],
  ["a) $t_1=\\dfrac{1}{24}\\ \\text{s}\\approx0{,}0417\\ \\text{s}$", "b) $t_5=\\dfrac{13}{12}\\ \\text{s}\\approx1{,}08\\ \\text{s}$"],
  "Nhận dạng: đề hỏi <strong>thời điểm, lần thứ n</strong> → vẽ vòng tròn pha, tính góc M quét rồi chia cho $\\omega$."),
 sol(R5, [
  ("Tách khoảng thời gian", [M(r"\dfrac{\Delta t}{T}=\dfrac{1{,}4}{0{,}6}=2+\dfrac{1}{3}"), A(r"\Delta t=2T+\dfrac{T}{3}")]),
  ("Quãng đường của hai chu kì đầy đủ", [M(r"s_1=2\cdot4A=8\cdot4"), A(r"s_1=32\ \text{cm}"),
                                         P("Sau $2T$ vật về đúng $x=2\\ \\text{cm}$, vẫn đang đi về biên âm (như lúc đầu).")]),
  ("Quãng đường của phần dư $\\dfrac{T}{3}$", [P("Phần dư ứng với M quét $120^\\circ$, từ $60^\\circ$ tới $180^\\circ$: vật đi từ $x=\\dfrac{A}{2}$ qua O tới biên âm."),
                                              M(r"s'=\dfrac{A}{2}+A=2+4"), A(r"s'=6\ \text{cm}"),
                                              P("Kiểm tra mốc: $\\dfrac{A}{2}\\to O$ mất $\\dfrac{T}{12}$, $O\\to$ biên mất $\\dfrac{T}{4}$; tổng $\\dfrac{T}{3}$ ✓.")]),
  ("Tốc độ trung bình", [M(r"s=s_1+s'=32+6=38\ \text{cm}"), M(r"v_{tb}=\dfrac{s}{\Delta t}=\dfrac{38}{1{,}4}"), A(r"v_{tb}\approx27{,}1\ \text{cm/s}")]),
  ("Vận tốc trung bình", [P("Vị trí đầu $x_1=2\\ \\text{cm}$; sau $\\Delta t$ vật ở biên âm, $x_2=-4\\ \\text{cm}$."),
                          M(r"\Delta x=x_2-x_1=-4-2=-6\ \text{cm}"), M(r"\overline{v}=\dfrac{\Delta x}{\Delta t}=\dfrac{-6}{1{,}4}"), A(r"\overline{v}\approx-4{,}29\ \text{cm/s}"),
                          P("Kiểm tra: $27{,}1\\lt v_{max}=A\\omega=4\\cdot\\dfrac{2\\pi}{0{,}6}\\approx41{,}9\\ \\text{cm/s}$ ✓; độ lớn vận tốc TB nhỏ hơn tốc độ TB ✓.")])],
  ["a) $s=38\\ \\text{cm}$", "b) tốc độ TB $\\approx27{,}1\\ \\text{cm/s}$ · vận tốc TB $\\approx-4{,}29\\ \\text{cm/s}$"],
  "Nhận dạng: quãng đường trong <strong>khoảng thời gian dài</strong> → tách $nT$ cộng phần dư; phần dư theo dõi vị trí, không đoán theo $T/4$."),
]

# ───────────────────────── Tự giải từng bước ─────────────────────────
STEPS = [
 dict(nhan_dang="Thấy <b>phương trình có sin hoặc dấu trừ</b> → đưa về <b>A cos(ωt + φ)</b> rồi mới đọc A, φ.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Đưa về dạng chuẩn", "Pha ban đầu $\\varphi$ bằng bao nhiêu rad (lấy trong $(-\\pi;\\pi]$)?", 1.571, "rad", 0.01,
       loi="Đổi $\\sin$ sang $\\cos$ thành $\\cos\\left(\\alpha-\\dfrac{\\pi}{2}\\right)$ rồi bỏ dấu trừ ngoài cùng, ra $\\varphi=-\\dfrac{\\pi}{2}$; dấu trừ trước hàm phải thêm $\\pi$ vào pha."),
  buoc("Chu kì và tần số", "Chu kì $T$ bằng bao nhiêu giây?", 0.4, "s", 0.01,
       loi="Lấy $T=\\dfrac{\\omega}{2\\pi}$ (đảo ngược) hoặc $T=\\dfrac{1}{\\omega}$ (thiếu $2\\pi$); $\\omega$ là hệ số đứng trước $t$.",
       ke=[("$T=\\dfrac{2\\pi}{\\omega}$ với $\\omega$ là hệ số của $t$", True),
           ("$T=\\dfrac{\\omega}{2\\pi}$", "Đảo ngược: $\\omega=\\dfrac{2\\pi}{T}$ nên $T=\\dfrac{2\\pi}{\\omega}$."),
           ("$T=\\dfrac{1}{\\omega}$", "Thiếu $2\\pi$: $\\dfrac{1}{T}$ là tần số $f$, còn $\\omega=2\\pi f$.")]),
  buoc("Tốc độ cực đại và gia tốc cực đại", "Tốc độ cực đại bằng bao nhiêu cm/s?", 62.8, "cm/s", 0.5,
       loi="Dùng $\\omega^2A$ (đó là gia tốc cực đại) hoặc chia $\\dfrac{A}{\\omega}$ thay vì nhân.",
       ke=[("$|v|_{max}=A\\omega$ với $A$ đã ở dạng chuẩn ($A\\gt0$)", True),
           ("$|v|_{max}=\\omega^2A$", "Đó là gia tốc cực đại; tốc độ cực đại là $A\\omega$."),
           ("$|v|_{max}=\\dfrac{A}{\\omega}$", "Chia thay vì nhân: $v=-A\\omega\\sin(\\omega t+\\varphi)$ nên biên độ của $v$ là $A\\omega$.")]),
  buoc("Lúc $t=0$", "Lúc $t=0$ vật ở đâu và đi theo chiều nào?",
       loi="Thấy $\\varphi\\gt0$ rồi kết luận 'đi chiều dương'; quy tắc ngược lại: $v_0=-A\\omega\\sin\\varphi$ nên $\\varphi\\gt0$ cho $v_0\\lt0$.",
       lua_chon=[("Ở O, đi theo chiều âm", True),
                 ("Ở O, đi theo chiều dương", "Với $\\varphi\\gt0$ thì $v_0=-A\\omega\\sin\\varphi\\lt0$. Cũng có thể nhìn thẳng: $x=-4\\sin(5\\pi t)$ nhận giá trị âm ngay sau $t=0$."),
                 ("Ở biên âm, đang tạm dừng", "Thay $t=0$: $x_0=A\\cos\\varphi=0$, không phải biên (ở biên thì $|x|=A$).")],
       ke=[("Thay $t=0$ vào $x$ và $v$ rồi xét dấu của $v_0$", True),
           ("Dùng $\\varphi=0$ vì phương trình đề cho dùng $\\sin$", "$\\varphi$ chỉ đọc được sau khi đưa về $\\cos$; đề cho $\\sin$ nên chưa thể đọc thẳng."),
           ("Từ tốc độ cực đại suy ra chiều đi", "Tốc độ cực đại chỉ cho độ lớn, không cho chiều.")])]),
 dict(nhan_dang="Thấy <b>li độ và tốc độ tại cùng lúc</b>, không có $t$ → nghĩ tới <b>$v^2=\\omega^2(A^2-x^2)$</b>.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Tần số góc", "Tần số góc $\\omega$ bằng bao nhiêu rad/s?", 12.57, "rad/s", 0.1,
       loi="Chỉ dùng một hệ thức: một phương trình có hai ẩn $\\omega$ và $A$ nên không giải được; phải viết cả hai rồi trừ vế để mất $A$."),
  buoc("Chu kì", "Chu kì $T$ bằng bao nhiêu giây?", 0.5, "s", 0.01,
       loi="Lấy $T=2\\pi\\omega$ hoặc $T=\\dfrac{\\omega}{2\\pi}$ thay vì $T=\\dfrac{2\\pi}{\\omega}$.",
       ke=[("$T=\\dfrac{2\\pi}{\\omega}$", True),
           ("$T=2\\pi\\omega$", "Nhân thay vì chia: $\\omega$ lớn thì dao động nhanh, chu kì phải nhỏ."),
           ("$T=\\dfrac{\\omega}{2\\pi}$", "Đảo ngược: đó là tần số $f$, không phải chu kì.")]),
  buoc("Biên độ", "Biên độ $A$ bằng bao nhiêu cm?", 5, "cm", 0.05,
       loi="Cộng thẳng $A=x_1+\\dfrac{v_1}{\\omega}$; hai đại lượng này vuông pha nên phải bình phương rồi cộng.",
       ke=[("$A^2=x_1^2+\\dfrac{v_1^2}{\\omega^2}$", True),
           ("$A=x_1+\\dfrac{v_1}{\\omega}$", "Cộng thẳng sai: $x$ và $\\dfrac{v}{\\omega}$ vuông pha, cộng bình phương."),
           ("$A=\\dfrac{v_1}{\\omega}$", "Chỉ đúng khi vật qua O ($x=0$); ở li độ $x_1\\neq0$ còn thiếu phần $x_1^2$.")]),
  buoc("Gia tốc cực đại", "Gia tốc cực đại bằng bao nhiêu cm/s²?", 789.6, "cm/s²", 4,
       loi="Dùng $\\omega A$ (đó là tốc độ cực đại) hoặc lấy gia tốc tại $x_2$ thay vì tại biên.",
       ke=[("$|a|_{max}=\\omega^2A$", True),
           ("$|a|_{max}=\\omega A$", "Đó là tốc độ cực đại $|v|_{max}$."),
           ("$|a|=\\omega^2x_2$", "Đó chỉ là độ lớn gia tốc tại $x_2$; gia tốc cực đại ở biên, $x=\\pm A$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>đồ thị x–t</b> → đọc <b>A (đỉnh–đáy), T (đỉnh–đỉnh)</b>, rồi chiều đi lúc $t=0$ cho dấu của $\\varphi$.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Đọc biên độ", "Biên độ $A$ đọc được bằng bao nhiêu cm?", 4, "cm", 0.1,
       loi="Lấy khoảng từ đáy tới đỉnh làm $A$; khoảng đó là $2A$."),
  buoc("Đọc chu kì", "Chu kì $T$ đọc được bằng bao nhiêu giây?", 1.2, "s", 0.03,
       loi="Lấy khoảng thời gian từ đáy tới đỉnh liền sau làm $T$; khoảng đó chỉ là $\\dfrac{T}{2}$.",
       ke=[("Chu kì gấp đôi khoảng thời gian từ đáy tới đỉnh liền sau", True),
           ("Chu kì bằng khoảng thời gian từ đáy tới đỉnh liền sau", "Đáy tới đỉnh mới là nửa dao động, $\\dfrac{T}{2}$."),
           ("Chu kì là thời điểm đồ thị cắt trục $t$ lần đầu", "Đồ thị cắt trục $t$ hai lần mỗi chu kì, và lần đầu phụ thuộc pha ban đầu; mốc đó không phải $T$.")]),
  buoc("Tần số góc", "Tần số góc $\\omega$ bằng bao nhiêu rad/s?", 5.236, "rad/s", 0.05,
       loi="Quên $2\\pi$ (lấy $\\dfrac{1}{T}$) hoặc nhân thay vì chia.",
       ke=[("$\\omega=\\dfrac{2\\pi}{T}$", True),
           ("$\\omega=\\dfrac{1}{T}$", "Đó là tần số $f$; $\\omega=2\\pi f$."),
           ("$\\omega=2\\pi T$", "Nhân thay vì chia: $T$ lớn thì dao động chậm, $\\omega$ phải nhỏ.")]),
  buoc("Pha ban đầu", "Pha ban đầu $\\varphi$ bằng bao nhiêu rad (lấy trong $(-\\pi;\\pi]$)?", 1.047, "rad", 0.02,
       loi="Chọn $\\varphi\\lt0$ vì nhớ nhầm 'đi xuống thì âm'; đường cong đang đi xuống tức $v_0\\lt0$, nên $\\varphi\\gt0$.",
       ke=[("$\\cos\\varphi=\\dfrac{x_0}{A}$, rồi chọn dấu theo chiều đi của đường cong", True),
           ("$\\varphi=\\dfrac{x_0}{A}$ (rad)", "$\\dfrac{x_0}{A}$ là giá trị của $\\cos\\varphi$, không phải bản thân góc $\\varphi$."),
           ("$\\varphi=0$ vì đồ thị có dạng $\\cos$", "$\\varphi=0$ chỉ khi lúc $t=0$ vật ở biên dương; ở đây $x_0$ khác $A$.")]),
  buoc("Phương trình và kiểm tra", "Phương trình dao động của vật là:",
       loi="Ghi $\\omega=T$ (lấy chu kì làm tần số góc) hoặc ghi $\\varphi$ sai dấu.",
       lua_chon=[("$x=4\\cos\\left(\\dfrac{5\\pi}{3}t+\\dfrac{\\pi}{3}\\right)\\ \\text{cm}$", True),
                 ("$x=4\\cos\\left(\\dfrac{5\\pi}{3}t-\\dfrac{\\pi}{3}\\right)\\ \\text{cm}$", "Pha ban đầu âm ứng với vật đi theo chiều dương lúc $t=0$; đồ thị đang đi xuống."),
                 ("$x=4\\cos\\left(1{,}2t+\\dfrac{\\pi}{3}\\right)\\ \\text{cm}$", "Đã lấy chu kì $T$ làm $\\omega$; phải dùng $\\omega=\\dfrac{2\\pi}{T}$.")],
       ke=[("Gộp $A$, $\\omega$, $\\varphi$ vừa tìm vào $x=A\\cos(\\omega t+\\varphi)$", True),
           ("Đổi $\\varphi$ sang độ rồi ghi vào", "Trong $\\cos(\\omega t+\\varphi)$ với $\\omega$ tính bằng rad/s thì $\\varphi$ phải tính bằng rad."),
           ("Thay $t=0$ để tính lại $A$", "$A$ đã đọc được ở bước đầu; bước này chỉ ghép các đại lượng đã có.")])]),
 dict(nhan_dang="Thấy <b>thời điểm, lần thứ n</b> qua một li độ → nghĩ tới <b>vòng tròn pha</b>: $\\Delta t=\\dfrac{\\Delta\\varphi}{\\omega}$.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Đặt M lúc $t=0$", "Lúc $t=0$ vật đi theo chiều nào?",
       loi="Thấy $\\varphi\\gt0$ rồi kết luận 'đi chiều dương'; ngược lại, $\\varphi\\gt0$ ứng với M ở nửa trên, tức vật đi về biên âm.",
       lua_chon=[("Chiều âm: M ở nửa trên vòng tròn", True),
                 ("Chiều dương, vì $\\varphi\\gt0$", "Quy tắc đúng ngược lại: $v_0=-A\\omega\\sin\\varphi$, nên $\\varphi\\gt0$ cho $v_0\\lt0$."),
                 ("Đứng yên, vì vật ở li độ $\\dfrac{A}{2}$", "Vật chỉ đứng yên tạm thời ở biên; $\\dfrac{A}{2}$ chưa phải biên.")]),
  buoc("Lần đầu qua vị trí cân bằng", "Vật qua vị trí cân bằng lần đầu tiên ở thời điểm nào (s)?", 0.0417, "s", 0.002,
       loi="Tính góc từ $0$ tới $\\dfrac{\\pi}{2}$ trong khi M xuất phát ở $\\dfrac{\\pi}{3}$ nên thừa; hoặc lấy $\\dfrac{T}{4}$ như từ biên về O.",
       ke=[("$\\Delta\\varphi$ từ góc xuất phát tới $\\dfrac{\\pi}{2}$, rồi $\\Delta t=\\dfrac{\\Delta\\varphi}{\\omega}$", True),
           ("$\\Delta\\varphi=\\dfrac{\\pi}{2}$ (tính từ góc $0$)", "M không xuất phát từ góc $0$ mà từ góc $\\varphi$; chỉ quét phần còn lại."),
           ("$\\Delta t=\\dfrac{T}{4}$ vì từ biên về O", "Vật không xuất phát từ biên (lúc $t=0$ vật ở li độ $x_0=A\\cos\\varphi$).")]),
  buoc("Góc M quét tới lần thứ 5", "Góc M phải quét tới lần thứ 5 qua $x=-3$ cm là bao nhiêu (đơn vị $\\pi$ rad)?", 4.333, "π rad", 0.02,
       loi="Cộng $4\\cdot2\\pi$ (như mỗi lần là một vòng) hoặc dùng góc của lần thứ nhất; mỗi vòng M cắt đường $x=-3$ cm hai lần.",
       ke=[("Liệt kê các lần M cắt đường $x=-3$ cm theo thứ tự, lấy lần thứ 5", True),
           ("Mỗi lần ứng với một vòng đầy đủ: lấy $5\\cdot2\\pi$", "Mỗi vòng M cắt đường $x=-3$ cm hai lần (hai chiều), nên 5 lần chưa tới 3 vòng."),
           ("Góc M quét tới lần thứ 5 bằng góc quét tới lần thứ nhất", "Hai lần cùng vị trí trên vòng tròn nhưng M đã quay thêm hai vòng; góc quét phải cộng thêm $4\\pi$.")]),
  buoc("Thời điểm lần thứ 5", "Vật qua $x=-3$ cm lần thứ 5 ở thời điểm nào (s)?", 1.083, "s", 0.01,
       loi="Lấy $\\Delta t=\\Delta\\varphi\\cdot\\omega$ (nhân thay vì chia) hoặc chia cho $2\\pi$ rồi quên nhân với $T$.",
       ke=[("$\\Delta t=\\dfrac{\\Delta\\varphi}{\\omega}$", True),
           ("$\\Delta t=\\Delta\\varphi\\cdot\\omega$", "Nhân thay vì chia: $\\omega=\\dfrac{\\Delta\\varphi}{\\Delta t}$."),
           ("$\\Delta t=\\dfrac{\\Delta\\varphi}{2\\pi}$", "Đó là số chu kì; phải nhân với $T$ mới ra thời gian.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang="Thấy <b>quãng đường trong khoảng thời gian dài</b> → tách $nT$ cộng phần dư; phần dư theo dõi vị trí, không đoán theo $T/4$.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Tách khoảng thời gian", "$\\Delta t$ bằng bao nhiêu lần chu kì $T$?", 2.33, None, 0.01,
       loi="Làm tròn thành 2 hoặc 3 chu kì rồi bỏ phần lẻ; phần lẻ vẫn đi thêm quãng đường."),
  buoc("Quãng đường của hai chu kì đầy đủ", "Hai chu kì đầy đủ đi được bao nhiêu cm?", 32, "cm", 0.1,
       loi="Lấy $2A$ cho mỗi chu kì (đó là nửa chu kì) hoặc quên nhân với số chu kì.",
       ke=[("Mỗi chu kì đi $4A$, nhân với số chu kì đầy đủ", True),
           ("Mỗi chu kì đi $2A$", "$2A$ là quãng đường của nửa chu kì."),
           ("Mỗi chu kì đi $A$", "$A$ chỉ là quãng đường của $\\dfrac{T}{4}$ khi xuất phát từ O hoặc biên.")]),
  buoc("Quãng đường của phần dư", "Phần dư $\\dfrac{T}{3}$ đi được bao nhiêu cm?", 6, "cm", 0.1,
       loi="Cho quãng đường tỉ lệ với thời gian ($\\dfrac{4A}{3}\\approx5{,}33$ cm) hoặc coi $\\dfrac{T}{3}$ là $\\dfrac{T}{4}$ nên đi đúng $A$.",
       ke=[("Dùng vòng tròn pha để xác định vị trí cuối của phần dư, rồi cộng các đoạn đi qua", True),
           ("Quãng đường tỉ lệ với thời gian: $s'=\\dfrac{4A}{3}$", "Vật đi nhanh gần O, chậm gần biên; quãng đường không tỉ lệ thời gian."),
           ("Lấy phần dư bằng $\\dfrac{T}{4}$ nên đi đúng $A$", "Quãng đường đúng $A$ trong $\\dfrac{T}{4}$ chỉ khi xuất phát từ O hoặc biên.")]),
  buoc("Tốc độ trung bình", "Tốc độ trung bình bằng bao nhiêu cm/s?", 27.1, "cm/s", 0.2,
       loi="Chia độ dời cho $\\Delta t$ (đó là vận tốc trung bình) hoặc chỉ lấy quãng đường của $2T$.",
       ke=[("Cộng quãng đường hai phần rồi chia cho $\\Delta t$", True),
           ("Chia độ dời $x_2-x_1$ cho $\\Delta t$", "Đó là vận tốc trung bình (có dấu), không phải tốc độ trung bình."),
           ("Lấy $\\dfrac{v_{max}}{2}$", "Tốc độ trung bình là quãng đường chia thời gian, không phải nửa tốc độ cực đại.")]),
  buoc("Vận tốc trung bình", "Vận tốc trung bình bằng bao nhiêu cm/s (có dấu)?", -4.286, "cm/s", 0.05,
       loi="Dùng quãng đường thay độ dời, hoặc cho rằng vật về chỗ cũ nên bằng 0; sau $\\Delta t$ vật ở biên âm, không phải vị trí đầu.",
       ke=[("Lấy vị trí cuối trừ vị trí đầu rồi chia cho $\\Delta t$", True),
           ("Dùng quãng đường chia cho $\\Delta t$", "Quãng đường cho tốc độ trung bình; vận tốc trung bình dùng độ dời có dấu."),
           ("Bằng 0 vì sau $2T$ vật về chỗ cũ", "Còn phần dư $\\dfrac{T}{3}$ nữa, vị trí cuối khác vị trí đầu.")])]),
]

d = {"lesson_id": 23, "lesson_title": "Bài 4. Bài tập về dao động điều hoà", "generated_at": "2026-10-09",
     "review": {"checked": True, "notes": "Kiểm chéo 9/10: tự giải 5 dạng + từng bước khớp (D4 lần 5 = 13/12 s; D5 s=38 cm, vtb≈27,1 cm/s, v̄≈−4,29 cm/s). Sửa: hình phân tích D5 lộ T/3, bảng D4 lộ nửa trên, lựa chọn sai D4 bước 3 thực ra đúng vị trí, loi_hay_gap D5 bước 1 lộ T/3."},
     "dang_bai": [dict(form="bai_tap", solution_html="", **x) for x in DANG]}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
