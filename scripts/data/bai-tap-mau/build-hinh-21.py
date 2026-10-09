"""Bài 21 · Bài 2. Mô tả dao động điều hoà (Vật lí 11, chương 1 Dao động) — dựng file scripts/data/bai-tap-mau/21.json từ đầu.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-21.py        (mẫu cấu trúc: build-hinh-57.py, build-hinh-33.py)
Quy ước theo lý thuyết bài 21: x = A cos(ωt + φ), A > 0, ω > 0, φ ∈ (−π; π] · f = 1/T · ω = 2πf = 2π/T · lúc t = 0: x₀ = A cos φ, tăng t một chút để
biết đi chiều nào · độ lệch pha Δφ = φ₁ − φ₂, φ lớn hơn thì sớm pha, Δt = Δφ/ω · ngược pha φ₂ = φ₁ ± π · đổi mốc thời gian muộn τ: φ' = φ + ωτ ·
đồ thị x–t: đỉnh dương cho A, hai đỉnh dương liên tiếp cho T.

Quét dạng (bước 0, tự làm trong đầu 9/10/2026): lý thuyết bài + chủ đề ngân hàng 154 (Li độ, biên độ, chu kì, tần số, pha ban đầu), 155 (Viết phương trình
dao động điều hoà), 156 (Đọc đồ thị li độ – thời gian). Ngân hàng bị RLS với anon nên KHÔNG đếm được số câu từng chủ đề (xem báo cáo).
5 dạng, cấp 1–4 không giảm:
  1 (cấp 1 · topic 154) đọc phương trình: A, ω, φ, T, f, li độ tại một thời điểm
  2 (cấp 2 · topic 155) viết phương trình từ trạng thái lúc t = 0 (li độ + chiều) và thời gian tới biên dương
  3 (cấp 2 · topic 154) độ lệch pha hai dao động cùng ω: sớm/trễ, lệch thời gian, viết dao động ngược pha
  4 (cấp 3 · topic 156) đọc đồ thị x–t: A, T, ω, φ rồi viết phương trình
  5 (cấp 4 · topic 155) đổi mốc thời gian: pha ban đầu đổi, A, T, f, ω giữ nguyên
Bài chưa có dạng cũ trong DB → không có tu_luan."""
import json, math, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "21.json")
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
PI = math.pi
X0 = 210.0


def fmt(x, nd=2):
    s = f"{x:.{nd}f}".replace(".", ",")
    return s.rstrip("0").rstrip(",") if "," in s else s


def minus(s):
    return s.replace("-", "−")


def rail(y, A, sc, ticks=None, xlab="x (cm)"):
    """Trục Ox nằm ngang tại y, tâm X0, sc px/cm. ticks = [(giá trị, nhãn)]; mặc định −A, O, A."""
    ticks = ticks if ticks is not None else [(-A, minus(fmt(-A))), (0, "O"), (A, fmt(A))]
    h = (A + 1.7) * sc
    b = seg(X0 - h, y, X0 + h, y, "currentColor", 2)
    for v, nm in ticks:
        b += seg(X0 + v * sc, y - 6, X0 + v * sc, y + 6, "currentColor", 2) + lbl(X0 + v * sc, y + 24, nm, "currentColor", 13, "middle", "700")
    b += lbl(X0 + h, y - 12, xlab, "currentColor", 12, "end", "700")
    return b


def mover(y, sc, x_cm, dur, c=GRN, r=7):
    """Vật chạy trên trục: x_cm = danh sách li độ (cm) cách đều thời gian, nội suy tuyến tính."""
    return (f'<circle cx="{X0 + sc * x_cm[0]:.1f}" cy="{y}" r="{r}" fill="{c}" stroke="currentColor" stroke-width="1.5">'
            f'{smil("cx", [X0 + sc * v for v in x_cm], dur)}</circle>')


def samples(f, t1, n):
    return [f(t1 * i / n) for i in range(n + 1)]


# ═════════════ Dạng 1 · x = 8cos(5πt − π/3) cm ═════════════
A1, W1, PH1 = 8.0, 5 * PI, -PI / 3
SC1 = 21


def x1f(t):
    return A1 * math.cos(W1 * t + PH1)


def d1(k):
    p = f"d1{k}"; y = 78; VB = "0 0 420 172"
    b = defs(p) + rail(y, A1, SC1)
    if k == 0:
        T = 2 * PI / W1; slow = 5; t1 = 2 * T; dur = t1 * slow          # T thật 0,4 s, chạy chậm 5 lần, 2 chu kì
        b += mover(y, SC1, samples(x1f, t1, 80), dur)
        b += lbl(X0, 24, "x = 8 cos(5πt − π/3)  cm", "currentColor", 14, "middle", "700")
        return fig("d1-0", VB, "Vật dao động qua lại hai bên vị trí cân bằng O trên trục Ox, hai đầu ở −8 cm và 8 cm", b,
                   "Mô phỏng: li độ tính từ phương trình (chạy chậm 5 lần, 2 chu kì). Vị trí lúc t = 0,1 s không ghi trên hình.")
    b += seg(X0, y - 42, X0, y, "currentColor", 1.4, "4 4", .6)
    b += arrow(p, "o", X0 + 4, y - 30, X0 + A1 * SC1 - 2, y - 30, 2.4) + lbl(X0 + A1 * SC1 / 2 + 4, y - 38, "A = ?", ORG, 13, "middle", "700")
    b += (f'<text x="{X0}" y="{y + 56}" font-size="15" font-weight="700" text-anchor="middle" fill="currentColor">x = '
          f'<tspan fill="{ORG}">A</tspan> cos(<tspan fill="{BLUE}">ω</tspan>t + <tspan fill="{RED}">φ</tspan>)</text>')
    b += lbl(X0, y + 80, "so từng số hạng với phương trình của đề", "currentColor", 12, "middle", "600")
    return fig("d1-2", VB, "Dạng chuẩn x bằng A côsin của omega t cộng phi; A là khoảng từ O tới đầu mút của trục", b, "Dữ kiện: phương trình của đề so với dạng chuẩn. " + NOTE)


# ═════════════ Dạng 2 · A = 6 cm, T = 0,5 s, lúc t = 0: x = −3 cm, chiều dương → x = 6cos(4πt − 2π/3) ═════════════
A2, T2 = 6.0, 0.5
W2, PH2 = 2 * PI / T2, -2 * PI / 3
SC2 = 25


def x2f(t):
    return A2 * math.cos(W2 * t + PH2)


def d2(k):
    p = f"d2{k}"; y = 92; VB = "0 0 420 160"
    b = defs(p) + rail(y, A2, SC2)
    b += f'<circle cx="{X0 - 3 * SC2}" cy="{y}" r="8" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="3 3"/>'
    b += arrow(p, "r", X0 - 3 * SC2 + 11, y - 22, X0 - 3 * SC2 + 52, y - 22, 2.6) + lbl(X0 - 3 * SC2, y - 34, "t = 0: x = −3 cm", RED, 13, "middle", "700")
    if k == 0:
        slow = 5; t1 = 2 * T2; dur = t1 * slow                              # T thật 0,5 s, chạy chậm 5 lần, 2 chu kì
        b += mover(y, SC2, samples(x2f, t1, 80), dur)
        return fig("d2-0", VB, "Vật xuất phát từ li độ −3 cm, đi theo chiều dương của trục Ox, dao động giữa −6 cm và 6 cm", b,
                   "Mô phỏng: vật xuất phát từ vị trí đỏ, đi theo chiều dương (chạy chậm 5 lần, 2 chu kì). Thời gian tới biên dương không ghi trên hình.")
    b += lbl(X0, 138, "cos φ = x₀ / A  →  φ = ?", "currentColor", 13, "middle", "700")
    return fig("d2-2", VB, "Lúc t bằng 0 vật ở li độ âm 3 cm, chiều chuyển động là chiều dương; hai điều kiện này quyết định pha ban đầu", b, "Dữ kiện: A = 6 cm; li độ và chiều lúc t = 0. " + NOTE)


# ═════════════ Dạng 3 · x₁ = 3cos(4πt + π/6), x₂ = 5cos(4πt − π/3) (cm) ═════════════
A31, A32 = 3.0, 5.0
W3 = 4 * PI
SC3 = 22


def x31(t): return A31 * math.cos(W3 * t + PI / 6)
def x32(t): return A32 * math.cos(W3 * t - PI / 3)


def d3(k):
    p = f"d3{k}"; y1, y2 = 70, 160; VB = "0 0 420 214"
    b = defs(p) + rail(y1, A31, SC3, xlab="x₁ (cm)") + rail(y2, A32, SC3, xlab="x₂ (cm)")
    b += lbl(14, y1 - 30, "vật 1 · A = 3 cm", BLUE, 13, "start", "700") + lbl(14, y2 - 30, "vật 2 · A = 5 cm", ORG, 13, "start", "700")
    if k == 0:
        slow = 5; t1 = 1.0; dur = t1 * slow                                  # T thật 0,5 s, chạy chậm 5 lần, 2 chu kì
        b += mover(y1, SC3, samples(x31, t1, 80), dur, BLUE) + mover(y2, SC3, samples(x32, t1, 80), dur, ORG)
        return fig("d3-0", VB, "Hai vật dao động trên hai trục song song, cùng tần số, biên độ 3 cm và 5 cm", b,
                   "Mô phỏng: hai vật cùng ω (chạy chậm 5 lần, 2 chu kì). Pha và độ lệch pha không ghi trên hình.")
    b += lbl(X0, 204, "Δφ = φ₁ − φ₂ = ?   ·   Δt = Δφ / ω", "currentColor", 13, "middle", "700")
    return fig("d3-2", VB, "Hai dao động cùng tần số góc; cần so pha ban đầu của vật 1 và vật 2", b, "Dữ kiện: hai phương trình cùng ω. " + NOTE)


# ═════════════ Dạng 4 · đồ thị x = 4cos(4πt/3 + π/3) cm, T = 1,5 s ═════════════
A4, W4, PH4 = 4.0, 4 * PI / 3, PI / 3
GX, GS, GY, GC = 44.0, 118.0, 112.0, 22.0         # gốc t, px/s, trục t, px/cm


def x4f(t): return A4 * math.cos(W4 * t + PH4)
def gx(t): return GX + GS * t
def gy(x): return GY - GC * x


def graph_frame():
    b = ""
    for i in range(0, 13):
        t = i * 0.25
        b += seg(gx(t), gy(4.4), gx(t), gy(-4.4), "currentColor", 1, "", .14 if i % 2 else .26)
        b += seg(gx(t), GY - 4, gx(t), GY + 4, "currentColor", 1.4)
        if i % 2 == 0:
            b += lbl(gx(t), gy(-4.4) + 17, fmt(t), "currentColor", 12, "middle", "400")
    for v in (-4, -2, 0, 2, 4):
        b += seg(GX - 4, gy(v), GX + 4, gy(v), "currentColor", 1.4) + lbl(GX - 8, gy(v) + 4, minus(str(v)), "currentColor", 12, "end", "400")
        if v:
            b += seg(GX, gy(v), gx(3.0), gy(v), "currentColor", 1, "", .12)
    b += seg(GX, gy(4.6), GX, gy(-4.6), "currentColor", 1.6) + seg(GX, GY, gx(3.05), GY, "currentColor", 1.6)
    b += lbl(GX + 6, gy(4.6) - 2, "x (cm)", "currentColor", 12, "start", "700") + lbl(gx(3.05) + 6, GY + 20, "t (s)", "currentColor", 12, "end", "700")
    return b


def d4(k):
    p = f"d4{k}"; VB = "0 0 420 236"
    curve = [(gx(i * 0.025), gy(x4f(i * 0.025))) for i in range(0, 121)]
    b = defs(p) + graph_frame() + poly(curve, GRN, 2.6)
    if k == 0:
        n = 90; dur = 3.0                                                     # đúng thời gian thật, 3 s
        X = [gx(3.0 * i / n) for i in range(n + 1)]; Y = [gy(x4f(3.0 * i / n)) for i in range(n + 1)]
        b += (f'<line stroke="{ORG}" stroke-width="1.6" stroke-dasharray="4 3" x1="{X[0]:.1f}" x2="{X[0]:.1f}" y1="{GY}" y2="{Y[0]:.1f}">'
              f'{smil("x1", X, dur)}{smil("x2", X, dur)}{smil("y2", Y, dur)}</line>')
        b += (f'<circle cx="{X[0]:.1f}" cy="{Y[0]:.1f}" r="5.5" fill="{ORG}" stroke="currentColor" stroke-width="1.5">'
              f'{smil("cx", X, dur)}{smil("cy", Y, dur)}</circle>')
        return fig("d4-0", VB, "Đồ thị li độ theo thời gian của một dao động điều hoà trong 3 giây, có hai đỉnh dương", b,
                   "Mô phỏng: điểm chạy trên đồ thị đúng thời gian thật (3 s), vạch đứng chiếu xuống trục t. Đồ thị vẽ từ công thức.")
    for tt in (1.25, 2.75):
        b += seg(gx(tt), gy(4), gx(tt), GY, ORG, 1.4, "4 3") + f'<circle cx="{gx(tt):.1f}" cy="{gy(4):.1f}" r="5" fill="none" stroke="{ORG}" stroke-width="2"/>'
    b += lbl(gx(1.25), gy(4) - 8, "đỉnh dương 1", ORG, 12, "middle", "700") + lbl(gx(2.75), gy(4) - 8, "đỉnh dương 2", ORG, 12, "middle", "700")
    b += dim(p, "o", gx(1.25), gy(-3.1), gx(2.75), gy(-3.1), "T = ?", gx(2.0), gy(-3.1) - 6, "middle")
    b += f'<circle cx="{gx(0):.1f}" cy="{gy(x4f(0)):.1f}" r="5" fill="{RED}"/>' + lbl(gx(0) + 10, gy(x4f(0)) - 8, "t = 0", RED, 12, "start", "700")
    return fig("d4-2", VB, "Đồ thị li độ theo thời gian; hai đỉnh dương liên tiếp được đánh dấu để đo chu kì, điểm lúc t bằng 0 được đánh dấu", b,
               "Dữ kiện: hai đỉnh dương liên tiếp và điểm lúc t = 0. " + NOTE)


# ═════════════ Dạng 5 · đổi mốc thời gian: x = 8cos(2πt − 5π/6), Bình muộn 0,25 s → x = 8cos(2πt′ − π/3) ═════════════
A5, W5, PH5, TAU = 8.0, 2 * PI, -5 * PI / 6, 0.25
SC5 = 18


def x5f(t): return A5 * math.cos(W5 * t + PH5)


def d5(k):
    p = f"d5{k}"; VB = "0 0 420 190"
    if k == 0:
        y = 90
        b = defs(p) + rail(y, A5, SC5)
        slow = 4; t1 = 2.0; dur = t1 * slow                                   # T thật 1 s, chạy chậm 4 lần, 2 chu kì
        b += mover(y, SC5, samples(x5f, t1, 80), dur)
        b += lbl(X0, 30, "con lắc lò xo nằm ngang · đồng hồ của An", "currentColor", 13, "middle", "700")
        b += lbl(X0, 160, "Bình bấm giờ muộn hơn An 0,25 s", RED, 13, "middle", "700")
        return fig("d5-0", VB, "Con lắc lò xo ngang dao động quanh O trên trục Ox giữa −8 cm và 8 cm", b,
                   "Mô phỏng: chuyển động tính từ phương trình theo đồng hồ của An (chạy chậm 4 lần, 2 chu kì). Trạng thái lúc Bình bắt đầu không ghi trên hình.")
    # hình dữ kiện: hai đồng hồ lệch nhau τ
    b = defs(p)
    xa0, sx = 50.0, 280.0                                                     # px / s
    ya, yb = 62, 128
    b += arrow(p, "g", xa0 - 6, ya, xa0 + sx * 1.15, ya, 2.2) + arrow(p, "g", xa0 + sx * TAU - 6, yb, xa0 + sx * 1.15, yb, 2.2)
    b += lbl(xa0 - 8, ya - 10, "An", BLUE, 14, "end", "700") + lbl(xa0 + sx * TAU - 8, yb - 10, "Bình", ORG, 14, "end", "700")
    for t in (0, 0.25, 0.5, 0.75, 1.0):
        b += seg(xa0 + sx * t, ya - 5, xa0 + sx * t, ya + 5, "currentColor", 1.6) + lbl(xa0 + sx * t, ya + 22, fmt(t), "currentColor", 12, "middle", "400")
    b += seg(xa0 + sx * TAU, yb - 5, xa0 + sx * TAU, yb + 5, "currentColor", 1.6) + lbl(xa0 + sx * TAU, yb + 22, "0", ORG, 12, "middle", "700")
    b += seg(xa0 + sx * TAU, ya + 28, xa0 + sx * TAU, yb - 5, RED, 1.6, "4 3")
    b += lbl(xa0 + sx * 1.15, ya + 22, "t (s)", "currentColor", 12, "end", "700") + lbl(xa0 + sx * 1.15, yb + 22, "t′ (s)", ORG, 12, "end", "700")
    b += lbl(X0, 176, "t = t′ + τ  →  pha ban đầu mới = ?", "currentColor", 13, "middle", "700")
    return fig("d5-2", VB, "Hai trục thời gian của An và Bình; số 0 của đồng hồ Bình nằm ở 0,25 giây trên đồng hồ của An", b, "Dữ kiện: τ = 0,25 s. " + NOTE)


BUILD = [d1, d2, d3, d4, d5]

# ───────────────────────── Đề + bảng phân tích ─────────────────────────
DANG = [
 dict(label="Dạng 1 · Dễ · Đọc phương trình: A, ω, φ, T, f và li độ tại một thời điểm",
      topic="Li độ, biên độ, chu kì, tần số, pha ban đầu",
      problem_html=r"<p>Một vật dao động điều hoà trên trục Ox với phương trình $x=8\cos\left(5\pi t-\dfrac{\pi}{3}\right)\ \text{cm}$, trong đó $t$ tính bằng giây.</p>"
                   r'<ol type="a"><li>Xác định biên độ, tần số góc và pha ban đầu.</li><li>Tính chu kì $T$ và tần số $f$.</li><li>Tính li độ của vật lúc $t=0{,}1\ \text{s}$.</li></ol>'),
 dict(label="Dạng 2 · Trung bình · Viết phương trình từ li độ và chiều chuyển động lúc t = 0",
      topic="Viết phương trình dao động điều hoà",
      problem_html=r"<p>Một vật dao động điều hoà trên trục Ox quanh vị trí cân bằng O với biên độ $A=6\ \text{cm}$ và chu kì $T=0{,}5\ \text{s}$. Chọn $t=0$ lúc vật ở li độ $x=-3\ \text{cm}$ và đang chuyển động theo chiều dương của trục Ox.</p>"
                   r'<ol type="a"><li>Viết phương trình dao động của vật.</li><li>Kể từ $t=0$, sau bao lâu vật lần đầu tới biên dương?</li></ol>'),
 dict(label="Dạng 3 · Trung bình · Độ lệch pha: sớm hay trễ, lệch bao lâu, viết dao động ngược pha",
      topic="Li độ, biên độ, chu kì, tần số, pha ban đầu",
      problem_html=r"<p>Hai vật dao động điều hoà trên hai trục song song, cùng chiều dương, cùng tần số góc: $x_1=3\cos\left(4\pi t+\dfrac{\pi}{6}\right)\ \text{cm}$ và $x_2=5\cos\left(4\pi t-\dfrac{\pi}{3}\right)\ \text{cm}$ ($t$ tính bằng giây).</p>"
                   r'<ol type="a"><li>Dao động nào sớm pha hơn, và lệch pha bao nhiêu?</li><li>Đỉnh dương của dao động sớm pha đến trước đỉnh dương của dao động kia bao lâu?</li><li>Viết phương trình dao động $x_3$ cùng biên độ với $x_1$ và ngược pha với $x_1$.</li></ol>'),
 dict(label="Dạng 4 · Khó · Đọc đồ thị li độ – thời gian rồi viết phương trình",
      topic="Đọc đồ thị li độ – thời gian",
      problem_html=r"<p>Đồ thị li độ – thời gian của một vật dao động điều hoà được vẽ ở hình dưới ($x$ tính bằng cm, $t$ tính bằng giây).</p>"
                   r'<ol type="a"><li>Đọc từ đồ thị biên độ $A$ và chu kì $T$.</li><li>Tính tần số góc $\omega$.</li><li>Xác định pha ban đầu $\varphi$ và viết phương trình dao động.</li></ol>'),
 dict(label="Dạng 5 · Khó · Đổi mốc thời gian: pha ban đầu đổi, nhịp dao động giữ nguyên",
      topic="Viết phương trình dao động điều hoà",
      problem_html=r"<p>Hai bạn cùng quan sát một con lắc lò xo nằm ngang. Theo đồng hồ của An, li độ của vật là $x=8\cos\left(2\pi t-\dfrac{5\pi}{6}\right)\ \text{cm}$ ($t$ tính bằng giây). Bình bấm đồng hồ muộn hơn An $0{,}25\ \text{s}$: khi đồng hồ của Bình chỉ $t'=0$ thì đồng hồ của An chỉ $t=0{,}25\ \text{s}$.</p>"
                   r'<ol type="a"><li>Viết phương trình li độ theo đồng hồ của Bình.</li><li>Lúc Bình bắt đầu bấm giờ, vật ở li độ nào và đang chuyển động theo chiều nào?</li><li>So hai phương trình: đại lượng nào đổi, đại lượng nào giữ nguyên?</li></ol>'),
]

ANALYSIS = [
 [(r"“$x=8\cos(5\pi t-\pi/3)$ cm”", r"Hàm côsin của $t$ (s); $x$ (cm)", r"⚠ Dạng chuẩn $x=A\cos(\omega t+\varphi)$: so từng số hạng; dấu trừ trong ngoặc thuộc về $\varphi$"),
  (r"“xác định biên độ, tần số góc và pha ban đầu”", r"Cần $A$, $\omega$, $\varphi$", r"$A\gt0$ · $\omega\gt0$ · $\varphi\in(-\pi;\pi]$"),
  (r"“tính chu kì $T$ và tần số $f$”", r"Cần $T$, $f$", r"$T=\dfrac{2\pi}{\omega}$ · $f=\dfrac{1}{T}$"),
  (r"“li độ lúc $t=0{,}1$ s”", r"$t=0{,}1$ s", r"Thế $t$ vào cả pha $\omega t+\varphi$; máy tính ở chế độ radian")],
 [(r"“biên độ $A=6$ cm và chu kì $T=0{,}5$ s”", r"$A=6$ cm; $T=0{,}5$ s", r"$\omega=\dfrac{2\pi}{T}$"),
  (r"“chọn $t=0$ lúc vật ở li độ $x=-3$ cm”", r"$t=0$: $x_0=-3$ cm", r"⚠ $x_0=A\cos\varphi$ chỉ cho $\cos\varphi$, tức hai góc đối nhau: chưa đủ để chọn $\varphi$"),
  (r"“đang chuyển động theo chiều dương”", r"Chiều dương: $x$ tăng khi $t$ tăng", r"Tăng $t$ một chút, xem $x$ tăng hay giảm → chọn dấu của $\varphi$"),
  (r"“viết phương trình dao động”", r"Cần $x(t)$", r"$x=A\cos(\omega t+\varphi)$, $\varphi\in(-\pi;\pi]$"),
  (r"“sau bao lâu … lần đầu tới biên dương”", r"Cần $\Delta t$ tới $x=A$", r"Biên dương ứng với pha $0$; $\Delta t=\dfrac{\Delta\varphi}{\omega}$")],
 [(r"“cùng tần số góc … $x_1=3\cos(4\pi t+\pi/6)$, $x_2=5\cos(4\pi t-\pi/3)$”", r"Cùng $\omega$; cần $\varphi_1$, $\varphi_2$", r"⚠ Chỉ so pha khi cùng $\omega$ và cùng dạng côsin; khi đó độ lệch pha không đổi theo $t$"),
  (r"“dao động nào sớm pha hơn, lệch pha bao nhiêu”", r"Cần $\Delta\varphi$ và dấu", r"$\Delta\varphi=\varphi_1-\varphi_2$; $\varphi$ lớn hơn thì sớm pha"),
  (r"“đỉnh dương … đến trước … bao lâu”", r"Cần $\Delta t$", r"$\Delta t=\dfrac{\Delta\varphi}{\omega}$"),
  (r"“cùng biên độ với $x_1$ và ngược pha với $x_1$”", r"$A_3=A_1$; $\varphi_3$ chưa biết", r"Ngược pha: $\varphi_3=\varphi_1\pm\pi$, đưa về $(-\pi;\pi]$")],
 [(r"“đồ thị li độ – thời gian”", r"Trục ngang $t$ (s), trục đứng $x$ (cm)", r"⚠ Trục hoành là thời gian, không phải quãng đường; đọc đỉnh và chiều dốc"),
  (r"“đọc … biên độ $A$”", r"Cần $A$", r"Đỉnh dương: độ cao của đỉnh là $A$"),
  (r"“chu kì $T$”", r"Hai đỉnh dương liên tiếp (hình)", r"Hai đỉnh dương liên tiếp cách nhau $T$"),
  (r"“tần số góc $\omega$”", r"Cần $\omega$", r"$\omega=\dfrac{2\pi}{T}$"),
  (r"“pha ban đầu $\varphi$, viết phương trình”", r"Điểm của đồ thị lúc $t=0$ và chiều dốc", r"$x_0=A\cos\varphi$; dốc lên hay xuống cho dấu của $\varphi$")],
 [(r"“Theo đồng hồ của An … $x=8\cos(2\pi t-5\pi/6)$”", r"$A$, $\omega$, $\varphi$ theo An", r"$x=A\cos(\omega t+\varphi)$"),
  (r"“Bình bấm đồng hồ muộn hơn An $0{,}25$ s”", r"$\tau=0{,}25$ s; $t'=0$ ứng với $t=0{,}25$ s", r"⚠ Chỉ đổi gốc thời gian, vật vẫn là một vật: thế $t$ theo $t'$ vào pha"),
  (r"“viết phương trình theo đồng hồ của Bình”", r"Cần $\varphi'$", r"$\varphi'=\varphi+\omega\tau$, đưa về $(-\pi;\pi]$"),
  (r"“lúc Bình bắt đầu bấm giờ, vật ở … chiều nào”", r"$t'=0$", r"$x=A\cos\varphi'$; tăng $t'$ một chút xem $x$ tăng hay giảm"),
  (r"“đại lượng nào đổi, giữ nguyên”", r"So hai phương trình", r"$A,T,f,\omega$ theo cấu tạo hệ; $\varphi$ theo lúc bấm giờ")],
]

# ───────────────────────── Lời giải ─────────────────────────
R1 = [r"<strong>Khái niệm:</strong> dao động điều hoà $x=A\cos(\omega t+\varphi)$; $A\gt0$ là biên độ, $\omega\gt0$ là tần số góc, $\varphi\in(-\pi;\pi]$ là pha ban đầu.",
      r"<strong>Công thức:</strong> $T=\dfrac{2\pi}{\omega}$ · $f=\dfrac{1}{T}$",
      r"⚠ <strong>Điều kiện:</strong> so với dạng chuẩn hàm côsin; dấu trong ngoặc thuộc về $\varphi$; thế $t$ vào cả pha, máy tính ở chế độ radian."]
R2 = [r"<strong>Khái niệm:</strong> $\varphi$ là pha lúc $t=0$; cho biết lúc $t=0$ vật ở đâu và sắp đi đâu.",
      r"<strong>Công thức:</strong> $\omega=\dfrac{2\pi}{T}$ · $x_0=A\cos\varphi$ · $\Delta t=\dfrac{\Delta\varphi}{\omega}$",
      r"⚠ <strong>Điều kiện:</strong> $\cos\varphi$ cho hai góc đối nhau; chọn dấu theo chiều chuyển động (tăng $t$ một chút, xem $x$ tăng hay giảm) và đưa $\varphi$ về $(-\pi;\pi]$."]
R3 = [r"<strong>Khái niệm:</strong> độ lệch pha của hai dao động cùng $\omega$ là hiệu hai pha ban đầu, không đổi theo $t$; $\varphi$ lớn hơn thì sớm pha.",
      r"<strong>Công thức:</strong> $\Delta\varphi=\varphi_1-\varphi_2$ · $\Delta t=\dfrac{\Delta\varphi}{\omega}$ · ngược pha $\varphi_3=\varphi_1\pm\pi$",
      r"⚠ <strong>Điều kiện:</strong> chỉ so pha khi cùng $\omega$ và cùng dạng côsin; $\varphi$ ghi trong $(-\pi;\pi]$."]
R4 = [r"<strong>Khái niệm:</strong> đồ thị $x$–$t$: trục ngang là thời gian; đỉnh dương cao bằng $A$, hai đỉnh dương liên tiếp cách nhau $T$.",
      r"<strong>Công thức:</strong> $\omega=\dfrac{2\pi}{T}$ · $x_0=A\cos\varphi$",
      r"⚠ <strong>Điều kiện:</strong> cùng $x_0$ có hai giá trị $\varphi$ đối nhau; chiều dốc của đồ thị lúc $t=0$ quyết định dấu."]
R5 = [r"<strong>Khái niệm:</strong> đổi lúc bấm giờ chỉ đổi gốc thời gian; $A$, $T$, $f$, $\omega$ là của vật, $\varphi$ thì không.",
      r"<strong>Công thức:</strong> bấm muộn $\tau$ thì $t=t'+\tau$ và $\varphi'=\varphi+\omega\tau$",
      r"⚠ <strong>Điều kiện:</strong> $\varphi'$ phải đưa về $(-\pi;\pi]$; chiều của $\tau$ (bấm muộn hay sớm) quyết định dấu của $\omega\tau$."]

SOLS = [
 sol(R1, [
  ("Đọc $A$, $\\omega$, $\\varphi$", [P(r"So với $x=A\cos(\omega t+\varphi)$:"), M(r"A=8\ \text{cm}\ ;\ \ \omega=5\pi\ \text{rad/s}\ ;\ \ \varphi=-\dfrac{\pi}{3}\ \text{rad}"), P(r"Dấu trừ trong ngoặc thuộc về $\varphi$; $\varphi$ đã nằm trong $(-\pi;\pi]$.")]),
  ("Chu kì", [M(r"T=\dfrac{2\pi}{\omega}=\dfrac{2\pi}{5\pi}"), A(r"T=0{,}4\ \text{s}")]),
  ("Tần số", [M(r"f=\dfrac{1}{T}=\dfrac{1}{0{,}4}"), A(r"f=2{,}5\ \text{Hz}")]),
  ("Li độ lúc $t=0{,}1$ s", [P(r"Thế $t$ vào cả pha (máy tính ở chế độ radian):"), M(r"x=8\cos\left(5\pi\cdot0{,}1-\dfrac{\pi}{3}\right)=8\cos\dfrac{\pi}{6}"), A(r"x\approx6{,}93\ \text{cm}")]),
  ("Kiểm tra", [P(r"$|x|\le A$: $6{,}93\lt8$ ✓."), P(r"$T\cdot f=0{,}4\cdot2{,}5=1$ ✓ và $\omega=2\pi f=5\pi$ rad/s ✓.")])],
  [r"a) $A=8\ \text{cm}$ · $\omega=5\pi\ \text{rad/s}$ · $\varphi=-\dfrac{\pi}{3}\ \text{rad}$", r"b) $T=0{,}4\ \text{s}$ · $f=2{,}5\ \text{Hz}$", r"c) $x\approx6{,}93\ \text{cm}$"],
  r"Nhận dạng: đề cho <strong>phương trình dạng côsin</strong> → so từng số hạng với $A\cos(\omega t+\varphi)$ trước, rồi mới tính $T$, $f$."),
 sol(R2, [
  ("Tần số góc", [M(r"\omega=\dfrac{2\pi}{T}=\dfrac{2\pi}{0{,}5}"), A(r"\omega=4\pi\ \text{rad/s}")]),
  ("Giá trị của $\\cos\\varphi$", [P(r"Lúc $t=0$:"), M(r"x_0=A\cos\varphi"), M(r"\cos\varphi=\dfrac{x_0}{A}=\dfrac{-3}{6}"), A(r"\cos\varphi=-0{,}5")]),
  ("Chọn $\\varphi$ theo chiều chuyển động", [P(r"$\cos\varphi=-0{,}5$ cho $\varphi=\dfrac{2\pi}{3}$ hoặc $\varphi=-\dfrac{2\pi}{3}$."),
                                               P(r"Chiều dương nghĩa là $x$ tăng khi pha tăng. Trong $(-\pi;0)$ côsin tăng theo góc; trong $(0;\pi)$ côsin giảm."),
                                               A(r"\varphi=-\dfrac{2\pi}{3}\ \text{rad}")]),
  ("Viết phương trình và kiểm tra", [M(r"x=6\cos\left(4\pi t-\dfrac{2\pi}{3}\right)\ \text{cm}"), P(r"Lúc $t=0$: $x=6\cos\left(-\dfrac{2\pi}{3}\right)=-3$ cm ✓."), P(r"Pha tăng từ $-\dfrac{2\pi}{3}$ nên côsin tăng, $x$ tăng: chiều dương ✓.")]),
  ("Lần đầu tới biên dương", [P(r"Biên dương ứng với pha $0$. Pha đi từ $-\dfrac{2\pi}{3}$ tới $0$:"), M(r"\Delta\varphi=0-\left(-\dfrac{2\pi}{3}\right)=\dfrac{2\pi}{3}"),
                              M(r"\Delta t=\dfrac{\Delta\varphi}{\omega}=\dfrac{2\pi/3}{4\pi}"), A(r"\Delta t=\dfrac{1}{6}\ \text{s}\approx0{,}167\ \text{s}"),
                              P(r"Kiểm tra: $\Delta t=\dfrac{T}{3}=\dfrac{0{,}5}{3}$ ✓ (từ $-\dfrac{A}{2}$ về O mất $\dfrac{T}{12}$, từ O ra biên mất $\dfrac{T}{4}$).")])],
  [r"a) $x=6\cos\left(4\pi t-\dfrac{2\pi}{3}\right)\ \text{cm}$", r"b) $\Delta t=\dfrac{1}{6}\ \text{s}\approx0{,}167\ \text{s}$"],
  r"Nhận dạng: đề cho <strong>li độ và chiều chuyển động lúc $t=0$</strong> → $\cos\varphi=\dfrac{x_0}{A}$ rồi chọn dấu $\varphi$ theo chiều."),
 sol(R3, [
  ("Hiệu hai pha ban đầu", [P(r"$\varphi_1=\dfrac{\pi}{6}$, $\varphi_2=-\dfrac{\pi}{3}$:"), M(r"\Delta\varphi=\varphi_1-\varphi_2=\dfrac{\pi}{6}+\dfrac{\pi}{3}"), A(r"\Delta\varphi=\dfrac{\pi}{2}\ \text{rad}")]),
  ("Sớm pha hay trễ pha", [P(r"$\varphi_1\gt\varphi_2$ nên:"), A(r"T:Dao động 1 <strong>sớm pha</strong> hơn dao động 2 một góc $\dfrac{\pi}{2}$ (không đồng pha, không ngược pha).")]),
  ("Thời gian lệch", [M(r"\Delta t=\dfrac{\Delta\varphi}{\omega}=\dfrac{\pi/2}{4\pi}"), A(r"\Delta t=0{,}125\ \text{s}")]),
  ("Dao động ngược pha với $x_1$", [P(r"Ngược pha: $\varphi_3=\varphi_1\pm\pi$. Chọn dấu để $\varphi_3\in(-\pi;\pi]$:"), M(r"\varphi_3=\dfrac{\pi}{6}-\pi=-\dfrac{5\pi}{6}"), A(r"x_3=3\cos\left(4\pi t-\dfrac{5\pi}{6}\right)\ \text{cm}")]),
  ("Kiểm tra", [P(r"$T=\dfrac{2\pi}{\omega}=0{,}5$ s nên $\Delta t=0{,}125\ \text{s}=\dfrac{T}{4}$ ứng với $\dfrac{\pi}{2}$ ✓."), P(r"$\varphi_1-\varphi_3=\dfrac{\pi}{6}+\dfrac{5\pi}{6}=\pi$ ✓ ngược pha.")])],
  [r"a) $x_1$ sớm pha hơn $x_2$ một góc $\dfrac{\pi}{2}$", r"b) $\Delta t=0{,}125\ \text{s}$", r"c) $x_3=3\cos\left(4\pi t-\dfrac{5\pi}{6}\right)\ \text{cm}$"],
  r"Nhận dạng: đề hỏi <strong>sớm, trễ, lệch pha hay ngược pha</strong> của hai dao động cùng $\omega$ → lấy $\Delta\varphi=\varphi_1-\varphi_2$, dấu cho biết ai sớm."),
 sol(R4, [
  ("Biên độ", [P(r"Đỉnh dương cao tới $4$ trên trục $x$:"), A(r"A=4\ \text{cm}")]),
  ("Chu kì", [P(r"Hai đỉnh dương liên tiếp ở $t=1{,}25$ s và $t=2{,}75$ s:"), M(r"T=2{,}75-1{,}25"), A(r"T=1{,}5\ \text{s}")]),
  ("Tần số góc", [M(r"\omega=\dfrac{2\pi}{T}=\dfrac{2\pi}{1{,}5}"), A(r"\omega=\dfrac{4\pi}{3}\ \text{rad/s}\approx4{,}19\ \text{rad/s}")]),
  ("Pha ban đầu", [P(r"Lúc $t=0$ đồ thị ở $x_0=2$ cm và đi xuống:"), M(r"\cos\varphi=\dfrac{x_0}{A}=\dfrac{2}{4}=0{,}5"),
                   P(r"$\varphi=\pm\dfrac{\pi}{3}$. Đồ thị đi xuống nghĩa là $x$ giảm khi pha tăng; côsin giảm theo góc trong $(0;\pi)$:"), A(r"\varphi=\dfrac{\pi}{3}\ \text{rad}")]),
  ("Viết phương trình và kiểm tra", [M(r"x=4\cos\left(\dfrac{4\pi}{3}t+\dfrac{\pi}{3}\right)\ \text{cm}"), P(r"Lúc $t=1{,}25$ s: pha $=\dfrac{4\pi}{3}\cdot1{,}25+\dfrac{\pi}{3}=2\pi$ nên $x=4$ cm, đúng đỉnh dương trên đồ thị ✓."),
                                   P(r"Lúc $t=0$: $x=4\cos\dfrac{\pi}{3}=2$ cm ✓.")])],
  [r"a) $A=4\ \text{cm}$ · $T=1{,}5\ \text{s}$", r"b) $\omega=\dfrac{4\pi}{3}\ \text{rad/s}$", r"c) $\varphi=\dfrac{\pi}{3}\ \text{rad}$ · $x=4\cos\left(\dfrac{4\pi}{3}t+\dfrac{\pi}{3}\right)\ \text{cm}$"],
  r"Nhận dạng: đề cho <strong>đồ thị $x$–$t$</strong> → đỉnh cho $A$, hai đỉnh dương cho $T$, điểm $t=0$ cùng chiều dốc cho $\varphi$."),
 sol(R5, [
  ("Liên hệ hai đồng hồ", [P(r"Khi đồng hồ Bình chỉ $t'=0$ thì đồng hồ An chỉ $0{,}25$ s, nên An luôn chỉ lớn hơn Bình $0{,}25$ s:"), M(r"t=t'+\tau\ ,\quad \tau=0{,}25\ \text{s}")]),
  ("Phần pha cộng thêm", [M(r"\omega\tau=2\pi\cdot0{,}25"), A(r"\omega\tau=\dfrac{\pi}{2}\ \text{rad}")]),
  ("Pha ban đầu theo Bình", [P(r"Thế $t=t'+\tau$ vào pha $2\pi t-\dfrac{5\pi}{6}$:"), M(r"\varphi'=\varphi+\omega\tau=-\dfrac{5\pi}{6}+\dfrac{\pi}{2}"), A(r"\varphi'=-\dfrac{\pi}{3}\ \text{rad}"), P(r"$\varphi'$ đã nằm trong $(-\pi;\pi]$."), A(r"x=8\cos\left(2\pi t'-\dfrac{\pi}{3}\right)\ \text{cm}")]),
  ("Trạng thái lúc Bình bắt đầu", [M(r"x=8\cos\left(-\dfrac{\pi}{3}\right)=8\cdot0{,}5=4\ \text{cm}"), P(r"Pha tăng từ $-\dfrac{\pi}{3}$; trong $(-\pi;0)$ côsin tăng nên $x$ tăng."), A("T:Vật ở $x=4$ cm, đang đi theo <strong>chiều dương</strong> (về biên dương).")]),
  ("Đại lượng đổi và không đổi", [P(r"Hai phương trình cùng $A=8$ cm, cùng $\omega=2\pi$ rad/s (nên cùng $T=1$ s, $f=1$ Hz)."), A("T:Chỉ <strong>pha ban đầu</strong> đổi: từ $-\\dfrac{5\\pi}{6}$ thành $-\\dfrac{\\pi}{3}$.")]),
  ("Kiểm tra", [P(r"Thế $t=0{,}25$ s vào phương trình của An: $8\cos\left(2\pi\cdot0{,}25-\dfrac{5\pi}{6}\right)=8\cos\left(-\dfrac{\pi}{3}\right)=4$ cm, khớp với li độ của Bình lúc $t'=0$ ✓.")])],
  [r"a) $x=8\cos\left(2\pi t'-\dfrac{\pi}{3}\right)\ \text{cm}$", r"b) $x=4\ \text{cm}$, đang đi theo chiều dương", r"c) $\varphi$ đổi; $A$, $T$, $f$, $\omega$ giữ nguyên"],
  r"Nhận dạng: đề cho <strong>đồng hồ bấm muộn $\tau$</strong> → $t=t'+\tau$, $\varphi'=\varphi+\omega\tau$; $A$, $T$, $f$, $\omega$ không đổi."),
]

# ───────────────────────── Tự giải từng bước (9/10/2026) ─────────────────────────
STEPS = [
 dict(nhan_dang=r"Thấy <b>phương trình dạng côsin</b> → so từng số hạng với $A\cos(\omega t+\varphi)$, rồi mới tính $T$, $f$.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Đọc $A$, $\\omega$, $\\varphi$", r"Pha ban đầu $\varphi$ là số nào?",
       loi=r"Lấy $\varphi=+\dfrac{\pi}{3}$ vì bỏ dấu trừ; hoặc lấy $5\pi$ làm $\varphi$ — đó là $\omega$, hệ số của $t$.",
       lua_chon=[(r"$\varphi=-\dfrac{\pi}{3}$ rad", True),
                 (r"$\varphi=\dfrac{\pi}{3}$ rad", r"Dấu trừ trong ngoặc là dấu của $\varphi$: $\omega t-\dfrac{\pi}{3}=\omega t+\left(-\dfrac{\pi}{3}\right)$."),
                 (r"$\varphi=5\pi$ rad", r"$5\pi$ là hệ số của $t$, tức tần số góc $\omega$, không phải pha ban đầu.")]),
  buoc("Chu kì", r"Chu kì $T$ bằng bao nhiêu giây?", 0.4, "s", 0.01,
       loi=r"Đảo ngược công thức $T=\dfrac{\omega}{2\pi}$ (kết quả đó là tần số $f$); hoặc $T=\dfrac{1}{\omega}$ quên $2\pi$.",
       ke=[(r"$T=\dfrac{2\pi}{\omega}$", True),
           (r"$T=\dfrac{\omega}{2\pi}$", r"Công thức này cho tần số $f$ ($\omega=2\pi f$), không phải chu kì."),
           (r"$T=\dfrac{1}{\omega}$", r"Thiếu $2\pi$: một chu kì ứng với pha tăng $2\pi$, nên $T=\dfrac{2\pi}{\omega}$.")]),
  buoc("Tần số", r"Tần số $f$ bằng bao nhiêu hertz?", 2.5, "Hz", 0.05,
       loi=r"Lấy $f=\omega=5\pi$ (nhầm tần số với tần số góc), hoặc $f=T$.",
       ke=[(r"$f=\dfrac{1}{T}$", True),
           (r"$f=\omega$", r"Tần số góc $\omega=2\pi f$, không bằng $f$."),
           (r"$f=2\pi T$", r"Tần số là nghịch đảo của chu kì, không nhân với $2\pi$.")]),
  buoc("Li độ lúc $t=0{,}1$ s", r"Li độ của vật lúc $t=0{,}1$ s bằng bao nhiêu cm?", 6.93, "cm", 0.05,
       loi=r"Máy tính để chế độ độ: $\dfrac{\pi}{6}$ bị hiểu là $0{,}52^\circ$, cho kết quả gần $8$; hoặc bỏ $\varphi$ trong pha rồi lấy $8\cos\dfrac{\pi}{2}=0$.",
       ke=[(r"Thế $t$ vào cả pha $5\pi t-\dfrac{\pi}{3}$ rồi lấy côsin (radian)", True),
           (r"Chỉ thế vào $\omega t$, bỏ $\varphi$", r"$\varphi$ có mặt trong pha ở mọi thời điểm, không chỉ lúc $t=0$."),
           (r"Lấy $x=A\cos\varphi$", r"Công thức đó chỉ đúng lúc $t=0$; ở $t=0{,}1$ s phải thế $t$ vào pha.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Đề cho <b>li độ và chiều chuyển động lúc $t=0$</b> → $\cos\varphi=\dfrac{x_0}{A}$, rồi chọn dấu $\varphi$ theo chiều.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Tần số góc", r"Tần số góc $\omega$ bằng bao nhiêu rad/s?", 12.57, "rad/s", 0.1,
       loi=r"Lấy $\omega=\dfrac{2\pi}{T}$ nhưng thế $T=0{,}5$ nhầm thành $f=0{,}5$ nên ra $\pi$; hoặc $\omega=\dfrac{1}{T}=2$."),
  buoc("Giá trị của $\\cos\\varphi$", r"$\cos\varphi$ bằng bao nhiêu?", -0.5, None, 0.01,
       loi=r"Chia ngược $\dfrac{A}{x_0}=-2$ (côsin không vượt $[-1;1]$); hoặc bỏ dấu âm của $x_0$.",
       ke=[(r"Lúc $t=0$: $x_0=A\cos\varphi$, nên $\cos\varphi=\dfrac{x_0}{A}$", True),
           (r"Dùng $x_0=A\cos(\omega\cdot0)$ để tìm $\omega$ trước", r"Lúc $t=0$ phần $\omega t$ bằng $0$, chỉ còn $\varphi$; $\omega$ đã tính từ chu kì."),
           (r"Dùng ngay $\Delta t=\dfrac{\Delta\varphi}{\omega}$", r"Chưa biết $\varphi$ nên chưa có $\Delta\varphi$; cần $\cos\varphi$ từ $x_0$ trước.")]),
  buoc("Chọn $\\varphi$ theo chiều chuyển động", r"$\varphi$ bằng giá trị nào?",
       loi=r"Bấm máy $\arccos(-0{,}5)$ rồi dừng, bỏ qua chiều chuyển động lúc $t=0$.",
       lua_chon=[(r"$\varphi=-\dfrac{2\pi}{3}$ rad", True),
                 (r"$\varphi=\dfrac{2\pi}{3}$ rad", r"$\cos\dfrac{2\pi}{3}=-0{,}5$ đúng li độ, nhưng pha tăng từ $\dfrac{2\pi}{3}$ thì côsin giảm, $x$ giảm: vật đi chiều âm, trái đề."),
                 (r"$\varphi=-\dfrac{\pi}{3}$ rad", r"$\cos\left(-\dfrac{\pi}{3}\right)=+0{,}5$: li độ dương, không khớp $x_0=-3$ cm.")],
       ke=[(r"$\cos\varphi=-0{,}5$ cho hai góc đối nhau; chọn dấu theo chiều chuyển động", True),
           (r"Lấy $\varphi=\arccos(-0{,}5)$ bằng máy tính là xong", r"Máy chỉ cho một nghiệm trong $[0;\pi]$ và không xét chiều chuyển động."),
           (r"Lấy $\varphi=0$ vì chọn $t=0$ làm gốc", r"$\varphi=0$ chỉ khi lúc $t=0$ vật ở biên dương; ở đây $x_0=-3$ cm.")]),
  buoc("Viết phương trình và kiểm tra"),
  buoc("Lần đầu tới biên dương", r"Kể từ $t=0$, sau bao lâu vật lần đầu tới biên dương (s)?", 0.167, "s", 0.005,
       loi=r"Dùng $\omega=2\pi$ thay vì $4\pi$ nên ra $\dfrac{1}{3}$ s; hoặc lấy $\Delta\varphi=-\dfrac{2\pi}{3}$ (âm) ra thời gian âm.",
       ke=[(r"Pha đi từ $\varphi$ tới $0$ (biên dương): $\Delta t=\dfrac{\Delta\varphi}{\omega}$", True),
           (r"Từ $-3$ cm tới biên dương mất $\dfrac{T}{2}$", r"$\dfrac{T}{2}$ là đi từ biên này sang biên kia ($-A$ tới $A$); đây xuất phát từ $-\dfrac{A}{2}$ nên ngắn hơn."),
           (r"Từ gần O tới biên dương mất $\dfrac{T}{4}$", r"$\dfrac{T}{4}$ chỉ đúng khi xuất phát đúng từ O; vật xuất phát từ $-3$ cm, trước đó còn đoạn về O.")])]),
 dict(nhan_dang=r"Đề hỏi <b>sớm, trễ, lệch pha, ngược pha</b> của hai dao động cùng $\omega$ → lấy $\Delta\varphi=\varphi_1-\varphi_2$, dấu cho biết ai sớm.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Hiệu hai pha ban đầu", r"$\Delta\varphi=\varphi_1-\varphi_2$ bằng bao nhiêu (tính theo đơn vị $\pi$ rad)?", 0.5, "π rad", 0.01,
       loi=r"Bỏ dấu trừ của $\varphi_2$: $\dfrac{1}{6}-\dfrac{1}{3}=-\dfrac{1}{6}$; hoặc lấy $\varphi_2-\varphi_1$ nên ra dấu âm."),
  buoc("Sớm pha hay trễ pha", r"Kết luận nào đúng?",
       loi=r"Lấy dao động có biên độ lớn hơn làm dao động sớm pha; sớm hay trễ chỉ xét theo pha.",
       lua_chon=[(r"Dao động 1 sớm pha $\dfrac{\pi}{2}$ so với dao động 2", True),
                 (r"Dao động 2 sớm pha $\dfrac{\pi}{2}$ so với dao động 1", r"$\varphi_1=\dfrac{\pi}{6}$ lớn hơn $\varphi_2=-\dfrac{\pi}{3}$ nên dao động 1 mới là sớm pha."),
                 (r"Hai dao động đồng pha vì cùng $\omega$", r"Cùng $\omega$ chỉ cho độ lệch pha không đổi; $\Delta\varphi=\dfrac{\pi}{2}\neq0$ nên không đồng pha.")],
       ke=[(r"Lấy $\varphi_1-\varphi_2$; dấu dương thì dao động 1 sớm pha", True),
           (r"So hai biên độ $A_1$ và $A_2$", r"Biên độ không quyết định sớm hay trễ; chỉ so pha ban đầu."),
           (r"So hai chu kì", r"Hai vật cùng $\omega$ nên cùng chu kì; hiệu pha mới khác nhau.")]),
  buoc("Thời gian lệch", r"Đỉnh dương của dao động sớm pha đến trước bao lâu (s)?", 0.125, "s", 0.005,
       loi=r"Chia $\dfrac{\Delta\varphi}{2\pi}=0{,}25$ rồi quên nhân với $T$; hoặc chia cho $\omega=2\pi$ thay vì $4\pi$.",
       ke=[(r"$\Delta t=\dfrac{\Delta\varphi}{\omega}$", True),
           (r"$\Delta t=\Delta\varphi\cdot\omega$", r"Nhân sai: đơn vị rad nhân rad/s không ra giây; phải chia."),
           (r"$\Delta t=\Delta\varphi$", r"$\Delta\varphi$ đo bằng rad, không phải giây; phải chia cho $\omega$.")]),
  buoc("Dao động ngược pha với $x_1$", r"Phương trình nào là dao động $x_3$ ngược pha $x_1$, cùng biên độ?",
       loi=r"Cộng thêm $\dfrac{\pi}{2}$ (nhầm với lệch vuông góc) hoặc đảo dấu $\varphi_1$ thành $-\dfrac{\pi}{6}$; ngược pha là lệch $\pi$.",
       lua_chon=[(r"$x_3=3\cos\left(4\pi t-\dfrac{5\pi}{6}\right)$ cm", True),
                 (r"$x_3=3\cos\left(4\pi t+\dfrac{2\pi}{3}\right)$ cm", r"$\dfrac{\pi}{6}+\dfrac{\pi}{2}=\dfrac{2\pi}{3}$: mới lệch $\dfrac{\pi}{2}$, chưa phải $\pi$."),
                 (r"$x_3=3\cos\left(4\pi t-\dfrac{\pi}{6}\right)$ cm", r"Đổi dấu $\varphi_1$ chỉ cho độ lệch $\dfrac{\pi}{3}$; ngược pha phải lệch đúng $\pi$.")],
       ke=[(r"Ngược pha: $\varphi_3=\varphi_1\pm\pi$, chọn dấu để $\varphi_3\in(-\pi;\pi]$", True),
           (r"Đổi dấu $\varphi_1$", r"Đổi dấu chỉ là đối xứng của pha, không phải lệch $\pi$."),
           (r"Đổi dấu biên độ $A_3=-3$ cm", r"Biên độ luôn dương ($A\gt0$); muốn đảo dấu li độ thì đổi pha thêm $\pi$.")]),
  buoc("Kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>đồ thị $x$–$t$</b> → đỉnh cho $A$, hai đỉnh dương cho $T$, điểm lúc $t=0$ cùng chiều dốc cho $\varphi$.",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 3}, buoc=[
  buoc("Biên độ", r"Biên độ $A$ đọc từ đồ thị bằng bao nhiêu cm?", 4, "cm", 0.1,
       loi=r"Lấy khoảng từ đỉnh âm tới đỉnh dương ($8$ cm) — đó là $2A$."),
  buoc("Chu kì", r"Chu kì $T$ bằng bao nhiêu giây?", 1.5, "s", 0.03,
       loi=r"Lấy thời điểm đỉnh dương đầu tiên ($1{,}25$ s) làm chu kì; hoặc đo từ đỉnh âm tới đỉnh dương kế (chỉ nửa chu kì).",
       ke=[(r"Hai đỉnh dương liên tiếp cách nhau $T$", True),
           (r"Thời điểm đỉnh dương đầu tiên chính là $T$", r"Đồ thị không bắt đầu ở đỉnh; khoảng từ gốc $t=0$ tới đỉnh đầu chưa phải một chu kì."),
           (r"Từ đỉnh âm tới đỉnh dương kế tiếp là $T$", r"Đó mới chỉ là nửa chu kì.")]),
  buoc("Tần số góc", r"Tần số góc $\omega$ bằng bao nhiêu rad/s?", 4.19, "rad/s", 0.05,
       loi=r"Lấy $\omega=\dfrac{1}{T}=0{,}67$ (đó là $f$, quên $2\pi$); hoặc thế $T=1{,}25$.",
       ke=[(r"$\omega=\dfrac{2\pi}{T}$", True),
           (r"$\omega=\dfrac{1}{T}$", r"Đó là tần số $f$; $\omega=2\pi f$."),
           (r"$\omega=\dfrac{T}{2\pi}$", r"Ngược rồi: $T=\dfrac{2\pi}{\omega}$ nên $\omega=\dfrac{2\pi}{T}$.")]),
  buoc("Pha ban đầu", r"Pha ban đầu $\varphi$ là giá trị nào?",
       loi=r"Từ $\cos\varphi=0{,}5$ lấy ngay một nghiệm mà không nhìn chiều dốc đồ thị lúc $t=0$.",
       lua_chon=[(r"$\varphi=\dfrac{\pi}{3}$ rad", True),
                 (r"$\varphi=-\dfrac{\pi}{3}$ rad", r"Cùng $x_0=2$ cm, nhưng $\varphi=-\dfrac{\pi}{3}$ cho đồ thị đi lên lúc $t=0$; đồ thị trong đề đi xuống."),
                 (r"$\varphi=\dfrac{2\pi}{3}$ rad", r"$\cos\dfrac{2\pi}{3}=-0{,}5$ cho $x_0=-2$ cm, không phải $+2$ cm.")],
       ke=[(r"Lấy $\cos\varphi=\dfrac{x_0}{A}$ rồi chọn dấu theo chiều dốc đồ thị", True),
           (r"Lấy $\varphi=0$ vì đồ thị bắt đầu ở trục $x$", r"$\varphi=0$ chỉ khi lúc $t=0$ đồ thị ở đỉnh dương; ở đây $x_0=2$ cm, chưa phải đỉnh."),
           (r"Bấm $\arccos$ rồi dừng, không xét chiều dốc", r"Máy chỉ cho một nghiệm; nghiệm đối nhau cho đồ thị đi theo chiều ngược lại.")]),
  buoc("Viết phương trình và kiểm tra")]),
 dict(nhan_dang=r"Thấy <b>đồng hồ bấm muộn $\tau$</b> → $t=t'+\tau$, $\varphi'=\varphi+\omega\tau$; $A$, $T$, $f$, $\omega$ không đổi.",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Liên hệ hai đồng hồ", r"Liên hệ nào giữa $t$ (An) và $t'$ (Bình) là đúng?",
       loi=r"Đảo chiều: coi Bình chạy trước An, nên cộng và trừ $\tau$ ngược lại.",
       lua_chon=[(r"$t=t'+0{,}25$", True),
                 (r"$t'=t+0{,}25$", r"Bình bấm muộn nên khi Bình chỉ $0$, An đã chỉ $0{,}25$ s: An lớn hơn Bình, $t=t'+0{,}25$."),
                 (r"$t=t'$", r"Hai đồng hồ lệch nhau $0{,}25$ s, không trùng.")]),
  buoc("Phần pha cộng thêm", r"Phần pha cộng thêm $\omega\tau$ bằng bao nhiêu (theo đơn vị $\pi$ rad)?", 0.5, "π rad", 0.01,
       loi=r"Lấy $\omega\tau=2\pi\cdot0{,}25$ nhưng ghi $0{,}25$ (thiếu một nửa); hoặc thế $\tau=0{,}5$.",
       ke=[(r"Thế $t=t'+\tau$ vào pha, phần thêm là $\omega\tau$", True),
           (r"Trừ $\omega\tau$ vào pha", r"$t=t'+\tau$ nên pha là $\omega t'+\omega\tau+\varphi$: phải cộng."),
           (r"Chỉ đổi biên độ $A$", r"Đổi gốc thời gian không làm vật dao động mạnh hơn hay yếu hơn; $A$ giữ nguyên.")]),
  buoc("Pha ban đầu theo Bình", r"Pha ban đầu $\varphi'$ theo đồng hồ Bình là giá trị nào?",
       loi=r"Trừ thay vì cộng ($-\dfrac{5\pi}{6}-\dfrac{\pi}{2}=-\dfrac{4\pi}{3}$, ngoài khoảng quy ước); hoặc cộng $\pi$ vì lấy nhầm $\tau=0{,}5$ s.",
       lua_chon=[(r"$\varphi'=-\dfrac{\pi}{3}$ rad", True),
                 (r"$\varphi'=\dfrac{\pi}{6}$ rad", r"Đó là $-\dfrac{5\pi}{6}+\pi$, ứng với $\tau=0{,}5$ s; đề cho $\tau=0{,}25$ s nên chỉ cộng $\dfrac{\pi}{2}$."),
                 (r"$\varphi'=-\dfrac{5\pi}{6}$ rad", r"Đó là pha ban đầu theo An; đổi gốc thời gian thì pha ban đầu đổi.")],
       ke=[(r"$\varphi'=\varphi+\omega\tau$ rồi đưa về $(-\pi;\pi]$", True),
           (r"Giữ $\varphi'=\varphi$ vì cùng một vật", r"Cùng một vật nhưng gốc thời gian khác, nên pha lúc $t'=0$ khác."),
           (r"$\varphi'=\varphi-\omega\tau$", r"Dấu cộng: Bình bấm muộn nên lúc $t'=0$ vật đã đi được thêm pha $\omega\tau$.")]),
  buoc("Trạng thái lúc Bình bắt đầu", r"Lúc Bình bắt đầu bấm giờ, vật ở đâu và sắp đi đâu?",
       loi=r"Chỉ tính $8\cos\varphi'$ rồi đoán chiều theo dấu của $\varphi'$; phải xem pha tăng một chút thì $x$ tăng hay giảm.",
       lua_chon=[(r"$x=4$ cm, đang đi theo chiều dương (về biên dương)", True),
                 (r"$x=4$ cm, đang đi theo chiều âm (về O)", r"Pha $-\dfrac{\pi}{3}$ tăng lên thì côsin tăng (trong $(-\pi;0)$), nên $x$ tăng: chiều dương."),
                 (r"$x=-4$ cm, đang đi theo chiều dương", r"$\cos\left(-\dfrac{\pi}{3}\right)=+0{,}5$ nên $x=+4$ cm, không phải $-4$ cm.")],
       ke=[(r"Tính $x=A\cos\varphi'$ rồi xem pha tăng thì $x$ tăng hay giảm", True),
           (r"Dùng phương trình của An với $t=0$", r"Lúc Bình bắt đầu, đồng hồ An chỉ $0{,}25$ s, không phải $0$."),
           (r"Lấy $x=A$ vì lúc bắt đầu vật ở biên", r"Chỉ khi $\varphi'=0$ vật mới ở biên dương; ở đây $\varphi'=-\dfrac{\pi}{3}$.")]),
  buoc("Đại lượng đổi và không đổi", r"Đại lượng nào của dao động thay đổi giữa hai phương trình?",
       loi=r"Cho rằng đổi gốc thời gian thì cả chu kì, tần số cũng đổi vì phương trình trông khác.",
       lua_chon=[(r"Chỉ pha ban đầu $\varphi$; $A$, $T$, $f$, $\omega$ giữ nguyên", True),
                 (r"Cả $A$, $T$, $f$, $\omega$ và $\varphi$ đều đổi", r"Đổi gốc thời gian không làm vật dao động khác đi; $A$, $T$, $f$, $\omega$ là của vật."),
                 (r"Chỉ tần số góc $\omega$ đổi", r"Hai phương trình cùng $2\pi t$: $\omega$ như nhau.")],
       ke=[(r"So từng số hạng của hai phương trình", True),
           (r"Coi hai phương trình mô tả hai vật khác nhau", r"Cùng một con lắc, chỉ khác lúc bấm giờ."),
           (r"Chỉ so li độ lúc $t=0$ của hai phương trình", r"Li độ lúc $t=0$ chỉ là một giá trị; phải so $A$, $\omega$, $\varphi$.")]),
  buoc("Kiểm tra")]),
]

d = {"lesson_id": 21, "lesson_title": "Bài 2. Mô tả dao động điều hoà", "generated_at": "2026-10-09",
     "review": {"checked": True, "notes": "kiểm chéo 9/10: 5 dạng đáp số đúng, đã chỉnh loi_hay_gap"},
     "dang_bai": [dict(form="bai_tap", solution_html="", **x) for x in DANG]}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
