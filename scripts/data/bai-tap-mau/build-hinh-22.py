"""Bài 22 · Bài 3. Vận tốc, gia tốc trong dao động điều hoà (Vật lí 11, chương 1 Dao động) — dựng scripts/data/bai-tap-mau/22.json từ đầu.
Chạy: python3 scripts/data/bai-tap-mau/build-hinh-22.py        (mẫu cấu trúc: build-hinh-57.py, 33.py)
Quy ước theo lý thuyết bài 22: x = A cos(ωt+φ) · v = −Aω sin(ωt+φ) = Aω cos(ωt+φ+π/2) · a = −ω²x · v_max = Aω, a_max = Aω² ·
v sớm x góc π/2, a ngược pha x · hệ thức độc lập A² = x² + v²/ω² · từ O ra A/2, A√2/2, A√3/2, A: T/12, T/8, T/6, T/4.
Bước 0 quét dạng (từ lý thuyết bài + 3 YCCĐ con: 157 công thức v,a theo li độ · 158 quan hệ pha · 159 hệ thức độc lập), 5 dạng, cấp 1→4 không giảm:
  1 (cấp 1) viết v(t), a(t) từ phương trình x, v_max/a_max, v/a tại t, nhanh hay chậm dần       [157]
  2 (cấp 2) biết li độ tìm |v| và a bằng hệ thức độc lập, xét chiều; ngược lại biết tốc độ tìm |x| [157]
  3 (cấp 2) đọc đồ thị x–t: A, T, φ → pha của v, a → v(0), a(0)                                  [158]
  4 (cấp 3) tốc độ bằng nửa cực đại: li độ, thời gian ngắn nhất từ biên (vòng tròn lượng giác), |a| [159]
  5 (cấp 4) bài ngược: hai cặp (x, v) → ω, A, T, a_max                                           [159]
Ngân hàng câu hỏi bị RLS với anon nên không đếm được số câu; dạng bám lý thuyết + tên 3 chủ đề."""
import json, math, re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

HERE = os.path.dirname(os.path.abspath(__file__))
J = os.path.join(HERE, "22.json")
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
PI = math.pi


def fmt(x, nd=1):
    s = f"{x:.{nd}f}".replace(".", ",")
    return s.rstrip("0").rstrip(",") if "," in s else s


def bob(xs, y, dur, c=GRN, r=8):
    return (f'<circle cx="{xs[0]:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" stroke="currentColor" stroke-width="1.5">'
            f'{smil("cx", xs, dur)}</circle>')


def track(cx, y, s, half, ticks, unit="x (cm)"):
    """Trục Ox nằm ngang: gốc O ở cx, s px cho mỗi cm."""
    b = seg(cx - s * half, y, cx + s * half, y, "currentColor", 2)
    for t_, name in ticks:
        X = cx + s * t_
        b += seg(X, y - 6, X, y + 6, "currentColor", 1.6) + lbl(X, y + 26, name, "currentColor", 12, "middle", "400")
    b += lbl(cx - s * half, y - 12, unit, "currentColor", 12, "start", "700")
    return b


# ═════════════ Dạng 1 · x = 5cos(4πt + π/3) cm ═════════════
A1, W1, PH1 = 5.0, 4 * PI, PI / 3


def x1(t): return A1 * math.cos(W1 * t + PH1)


def d1(k):
    p = f"d1{k}"; VB = "0 0 420 150"; cx, y, s = 210, 100, 28
    ticks = [(-5, "−5"), (0, "O"), (5, "5")]
    b = defs(p) + track(cx, y, s, 5.8, ticks)
    if k == 0:
        n = 64; T = 2 * PI / W1; tot = 2 * T                       # 2 chu kì, chạy chậm 4 lần
        xs = [cx + s * x1(tot * i / n) for i in range(n + 1)]
        b += dim(p, "o", cx, 66, cx + s * A1, 66, "", 0, 0) + lbl(cx + s * A1 / 2, 58, "A = 5 cm", ORG, 13, "middle", "700")
        b += lbl(14, 24, "Cần tìm: v_max, a_max;  v, a lúc t = 1/12 s", "currentColor", 13, "start", "700")
        b += bob(xs, y - 18, 4 * tot)
        return fig("d1-0", VB, "Vật dao động quanh vị trí cân bằng O trên trục Ox với biên độ 5 cm", b,
                   "Mô phỏng: vật dao động đúng theo phương trình đề cho (chạy chậm 4 lần, 2 chu kì). Vị trí tính theo công thức.")
    b += dim(p, "o", cx, 66, cx + s * A1, 66, "", 0, 0) + lbl(cx + s * A1 / 2, 58, "A", ORG, 13, "middle", "700")
    b += lbl(14, 24, "x = A cos(ωt + φ)", "currentColor", 13, "start", "700")
    b += lbl(14, 42, "A, ω, φ đọc từ phương trình", ORG, 13, "start", "700")
    b += lbl(cx + s * 5.8, 140, "t = 1/12 s → pha ωt + φ = ?", "currentColor", 12, "end", "400")
    return fig("d1-2", VB, "Từ phương trình đọc biên độ, tần số góc và pha ban đầu", b, "Dữ kiện: A, ω, φ đọc thẳng từ phương trình. " + NOTE)


# ═════════════ Dạng 2 · A = 10 cm, ω = 4 rad/s, x = +6 cm chiều dương ═════════════
A2, W2 = 10.0, 4.0
PH2 = -math.acos(0.6)                                               # x(0) = 6, v(0) > 0


def d2(k):
    p = f"d2{k}"; VB = "0 0 420 156"; cx, y, s = 210, 104, 17
    ticks = [(-10, "−10"), (0, "O"), (10, "10")]
    b = defs(p) + track(cx, y, s, 11.5, ticks)
    X6 = cx + s * 6
    b += seg(X6, y - 52, X6, y + 8, ORG, 1.6, "5 4") + lbl(X6, y + 46, "x = 6 cm", ORG, 13, "middle", "700")
    if k == 0:
        n = 64; T = 2 * PI / W2; tot = 2 * T                         # 2 chu kì, đúng thời gian thật
        xs = [cx + s * A2 * math.cos(W2 * tot * i / n + PH2) for i in range(n + 1)]
        b += lbl(14, 22, "A = 10 cm,  ω = 4 rad/s", "currentColor", 13, "start", "700")
        b += lbl(14, 40, "Cần tìm: |v|, a tại x = 6 cm;  nhanh hay chậm dần", "currentColor", 12, "start", "700")
        b += bob(xs, y - 18, tot)
        return fig("d2-0", VB, "Vật dao động trên trục Ox, đang qua li độ 6 cm theo chiều dương", b,
                   "Mô phỏng: lúc bắt đầu vật qua x = 6 cm theo chiều dương (đúng thời gian thật, 2 chu kì). Vị trí tính theo công thức.")
    b += arrow(p, "b", X6 + 12, y - 30, X6 + 56, y - 30, 3) + lbl(X6 + 14, y - 45, "chiều chuyển động", BLUE, 12, "start", "700")
    b += dot(X6, y - 18, 8, GRN)
    b += lbl(14, 22, "|v| từ x:  A² = x² + v²/ω²", "currentColor", 13, "start", "700")
    return fig("d2-2", VB, "Vật ở li độ 6 cm, đang đi theo chiều dương của trục Ox", b, "Dữ kiện: biết x, A, ω và chiều chuyển động. " + NOTE)


# ═════════════ Dạng 3 · đồ thị x–t: A = 6 cm, T = 1,2 s, φ = π/3 ═════════════
A3, T3, PH3 = 6.0, 1.2, PI / 3
W3 = 2 * PI / T3
L3, R3, Y03, K3, TMAX = 66, 400, 118, 14, 1.8
PS3 = (R3 - L3) / TMAX


def tx3(t): return L3 + PS3 * t
def yx3(v): return Y03 - K3 * v
def x3(t): return A3 * math.cos(W3 * t + PH3)


def frame3():
    b = ""
    for i in range(0, 10):
        t = 0.2 * i
        b += seg(tx3(t), 32, tx3(t), 208, "currentColor", 1, "", .13) + seg(tx3(t), 208, tx3(t), 213, "currentColor", 1.4)
        b += lbl(tx3(t), 230, fmt(t), "currentColor", 12, "middle", "400")
    for u in (6, 3, 0, -3, -6):
        b += seg(L3, yx3(u), R3, yx3(u), "currentColor", 1, "" if u else "5 4", .3 if u else .55)
        b += lbl(L3 - 8, yx3(u) + 4, ("−" if u < 0 else "") + str(abs(u)), "currentColor", 12, "end", "400")
    b += seg(L3, 32, L3, 208, "currentColor", 1.6) + seg(L3, 208, R3, 208, "currentColor", 1.6)
    b += lbl(L3 + 6, 22, "x (cm)", "currentColor", 12, "start", "700") + lbl(L3 - 8, 230, "t (s)", "currentColor", 12, "end", "700")
    return b


def curve3():
    n = 90
    pts = [(tx3(TMAX * i / n), yx3(x3(TMAX * i / n))) for i in range(n + 1)]
    return poly(pts, GRN, 2.6)


def d3(k):
    p = f"d3{k}"; VB = "0 0 420 266"
    b = defs(p) + frame3() + curve3()
    if k == 0:
        n = 60; tot = TMAX                                          # chạy chậm 2 lần
        ts = [tot * i / n for i in range(n + 1)]
        yv = [yx3(x3(t)) for t in ts]; xv = [tx3(t) for t in ts]
        b += seg(22, 32, 22, 208, "currentColor", 1.2, "", .3)
        b += (f'<line x1="30" y1="{yv[0]:.1f}" x2="{xv[0]:.1f}" y2="{yv[0]:.1f}" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 4" opacity=".6">'
              f'{smil("x2", xv, 2 * tot)}{smil("y1", yv, 2 * tot)}{smil("y2", yv, 2 * tot)}</line>')
        b += (f'<circle cx="22" cy="{yv[0]:.1f}" r="8" fill="{GRN}" stroke="currentColor" stroke-width="1.5">{smil("cy", yv, 2 * tot)}</circle>')
        b += (f'<circle cx="{xv[0]:.1f}" cy="{yv[0]:.1f}" r="5.5" fill="{ORG}" stroke="currentColor" stroke-width="1.5">'
              f'{smil("cx", xv, 2 * tot)}{smil("cy", yv, 2 * tot)}</circle>')
        b += lbl(R3, 22, "Cần tìm: A, T, ω, φ;  v(0), a(0)", "currentColor", 12, "end", "700")
        return fig("d3-0", VB, "Đồ thị li độ theo thời gian của một vật dao động điều hoà từ 0 đến 1,8 giây, kèm vật chạy lên xuống theo đồ thị", b,
                   "Mô phỏng: vật (bên trái) dao động lên xuống, điểm cam chạy trên đồ thị x–t (chạy chậm 2 lần). Đồ thị tính theo công thức.")
    X0, Y0 = tx3(0), yx3(x3(0))
    b += dot(X0, Y0, 5.5, ORG) + lbl(X0 + 10, Y0 - 12, "x(0)", ORG, 13, "start", "700")
    dx = -A3 * W3 * math.sin(PH3)                                  # cm/s tại t=0 (dốc xuống)
    b += arrow(p, "o", X0, Y0, tx3(0.14), yx3(x3(0) + dx * 0.14), 3) + lbl(tx3(0.17), Y0 + 36, "đang đi xuống", ORG, 12, "start", "700")
    for tt in (0.4, 1.6):
        b += dot(tx3(tt), yx3(-A3), 5, BLUE) + seg(tx3(tt), 236, tx3(tt), 244, BLUE, 1.3, "4 4", .8)
    b += dim(p, "b", tx3(0.4), 242, tx3(1.6), 242, "", 0, 0) + lbl(tx3(1.0), 258, "T: giữa hai đáy liền nhau", BLUE, 12, "middle", "700")
    b += dot(tx3(1.0), yx3(A3), 5, RED) + dim(p, "r", tx3(1.0) + 14, Y03, tx3(1.0) + 14, yx3(A3), "", 0, 0) + lbl(tx3(1.0) + 22, yx3(A3 / 2) + 4, "A", RED, 13, "start", "700")
    return fig("d3-2", VB, "Đồ thị li độ: biên độ đo từ trục đến đỉnh, chu kì đo giữa hai đáy liền nhau, li độ ban đầu và hướng đi tại t bằng 0", b,
               "Dữ kiện: A ở đỉnh, T giữa hai đáy; x(0) và hướng đi cho pha ban đầu. " + NOTE)


# ═════════════ Dạng 4 · A = 8 cm, T = 1,2 s, t = 0 ở biên dương ═════════════
A4, T4 = 8.0, 1.2
W4 = 2 * PI / T4


def d4(k):
    p = f"d4{k}"; VB = "0 0 420 150"; cx, y, s = 210, 100, 22
    ticks = [(-8, "−8"), (0, "O"), (8, "8")]
    b = defs(p) + track(cx, y, s, 9.2, ticks)
    b += arrow(p, "g", cx + s * A4 + 2, y - 44, cx + s * A4 + 2, y - 22, 2) + lbl(cx + s * A4, y - 52, "t = 0", GRN, 12, "middle", "700")
    if k == 0:
        n = 64; tot = 2 * T4                                         # 2 chu kì, chạy chậm 2 lần
        xs = [cx + s * A4 * math.cos(W4 * tot * i / n) for i in range(n + 1)]
        b += lbl(14, 22, "A = 8 cm,  T = 1,2 s", "currentColor", 13, "start", "700")
        b += lbl(14, 40, "Cần tìm: v_max;  x, t, |a| khi |v| = v_max/2", "currentColor", 12, "start", "700")
        b += bob(xs, y - 18, 2 * tot)
        return fig("d4-0", VB, "Vật dao động trên trục Ox, bắt đầu từ biên dương", b,
                   "Mô phỏng: vật bắt đầu từ biên dương (chạy chậm 2 lần, 2 chu kì). Vị trí tính theo công thức.")
    X = cx + s * A4
    b += arrow(p, "o", X - 6, y - 30, cx + s * 2, y - 30, 3) + lbl(cx + s * 2, y - 45, "đi về O", ORG, 12, "start", "700")
    b += lbl(cx + s * 4, y + 46, "x = ?  khi |v| = v_max/2", "currentColor", 12, "middle", "700")
    b += lbl(14, 22, "(x/A)² + (v/v_max)² = 1", "currentColor", 13, "start", "700")
    return fig("d4-2", VB, "Từ biên dương đi về vị trí cân bằng; cần tìm li độ nơi tốc độ bằng một nửa tốc độ cực đại", b, "Dữ kiện: gốc thời gian ở biên dương. " + NOTE)


# ═════════════ Dạng 5 · (x₁=3 cm, 40 cm/s), (x₂=4 cm, 30 cm/s) ⇒ ω=10, A=5 ═════════════
def d5(k):
    p = f"d5{k}"; VB = "0 0 420 164"; cx, y = 210, 104
    X1, X2 = cx + 62, cx + 108
    b = defs(p) + seg(cx - 170, y, cx + 170, y, "currentColor", 2)
    for X, nm in ((cx, "O"), (X1, "x₁"), (X2, "x₂")):
        b += seg(X, y - 6, X, y + 6, "currentColor", 1.6) + lbl(X, y + 26, nm, "currentColor", 13, "middle", "700")
    b += lbl(cx + 170, y - 12, "x", "currentColor", 12, "end", "700")
    b += seg(X1, y - 46, X1, y + 6, ORG, 1.4, "5 4") + seg(X2, y - 46, X2, y + 6, BLUE, 1.4, "5 4")
    b += lbl(14, 22, "x₁ = 3 cm:  |v₁| = 40 cm/s", ORG, 13, "start", "700") + lbl(14, 42, "x₂ = 4 cm:  |v₂| = 30 cm/s", BLUE, 13, "start", "700")
    if k == 0:
        n = 64; tot = 2.0                                            # 2 chu kì minh hoạ, mỗi chu kì 2 s
        xs = [cx + 150 * math.cos(PI * tot * i / n) for i in range(n + 1)]
        b += lbl(cx + 170, 154, "Cần tìm: ω, T, A, a_max", "currentColor", 12, "end", "700")
        b += bob(xs, y - 18, 2 * tot)
        return fig("d5-0", VB, "Vật dao động trên trục Ox, hai vị trí x1 và x2 được đánh dấu, tại mỗi vị trí đo được một tốc độ", b,
                   "Mô phỏng một dao động minh hoạ (chạy chậm; không theo tỉ lệ, biên độ chưa phải đáp số): vật đi qua x₁ rồi x₂ với tốc độ nhỏ dần.")
    b += lbl(cx - 170, y + 26, "−A", "currentColor", 12, "start", "400") + lbl(cx + 170, y + 26, "+A", "currentColor", 12, "end", "400")
    b += lbl(cx + 170, 154, "Hai điểm cùng một dao động: cùng A, cùng ω", "currentColor", 12, "end", "700")
    return fig("d5-2", VB, "Hai vị trí x1 và x2 trên cùng một dao động với tốc độ tương ứng, biên độ và tần số góc chưa biết", b, "Dữ kiện: hai cặp (x, v); A và ω chưa biết. " + NOTE)


BUILD = [d1, d2, d3, d4, d5]

DANG = [
    dict(label="Dạng 1 · Dễ · Viết v(t), a(t) từ phương trình li độ; v_max, a_max; v và a tại một thời điểm",
         topic="Công thức vận tốc, gia tốc theo li độ",
         problem_html=r"<p>Một vật dao động điều hoà dọc trục Ox với phương trình $x=5\cos\left(4\pi t+\dfrac{\pi}{3}\right)$, trong đó $x$ tính bằng cm, $t$ tính bằng s.</p>"
                      r"<ol type=\"a\"><li>Tính tốc độ cực đại và độ lớn gia tốc cực đại của vật.</li><li>Viết phương trình vận tốc $v(t)$ và gia tốc $a(t)$.</li>"
                      r"<li>Tại $t=\dfrac{1}{12}\ \text{s}$, tính $v$ và $a$. Lúc đó vật đang đi về vị trí cân bằng hay ra biên?</li></ol>"),
    dict(label="Dạng 2 · Trung bình · Biết li độ tìm tốc độ và gia tốc, xét nhanh hay chậm dần; biết tốc độ tìm li độ",
         topic="Công thức vận tốc, gia tốc theo li độ",
         problem_html=r"<p>Một vật dao động điều hoà trên trục Ox với biên độ $A=10\ \text{cm}$ và tần số góc $\omega=4\ \text{rad/s}$. Vật đi qua li độ $x=+6\ \text{cm}$ theo chiều dương.</p>"
                      r"<ol type=\"a\"><li>Tính độ lớn vận tốc tại vị trí đó.</li><li>Tính gia tốc tại vị trí đó (kể cả dấu). Vật đang chuyển động nhanh dần hay chậm dần?</li>"
                      r"<li>Ở một thời điểm khác, tốc độ của vật là $24\ \text{cm/s}$. Li độ của vật khi đó có độ lớn bao nhiêu?</li></ol>"),
    dict(label="Dạng 3 · Trung bình · Đọc đồ thị x–t: biên độ, chu kì, pha ban đầu; suy ra v và a",
         topic="Quan hệ pha giữa x, v, a",
         problem_html=r"<p>Hình vẽ là đồ thị li độ $x$ theo thời gian $t$ của một vật dao động điều hoà ($x$ tính bằng cm, $t$ tính bằng s), vẽ từ $t=0$ đến $t=1{,}8\ \text{s}$.</p>"
                      r"<ol type=\"a\"><li>Đọc đồ thị để tìm $A$, $T$, $\omega$ và pha ban đầu $\varphi$ của li độ.</li>"
                      r"<li>Viết phương trình $v(t)$ và $a(t)$; nêu pha của $v$ và $a$ so với pha của $x$.</li><li>Tính $v$ và $a$ tại $t=0$.</li></ol>"),
    dict(label="Dạng 4 · Khó · Tốc độ bằng nửa cực đại: li độ, thời gian từ biên, độ lớn gia tốc",
         topic="Hệ thức độc lập với thời gian",
         problem_html=r"<p>Một vật dao động điều hoà trên trục Ox với biên độ $A=8\ \text{cm}$, chu kì $T=1{,}2\ \text{s}$. Chọn $t=0$ lúc vật ở biên dương.</p>"
                      r"<ol type=\"a\"><li>Tính tốc độ cực đại của vật.</li><li>Khi tốc độ của vật bằng một nửa tốc độ cực đại, li độ có độ lớn bao nhiêu?</li>"
                      r"<li>Tính khoảng thời gian ngắn nhất từ $t=0$ đến lúc tốc độ lần đầu bằng một nửa tốc độ cực đại.</li><li>Tính độ lớn gia tốc ở thời điểm đó.</li></ol>"),
    dict(label="Dạng 5 · Khó · Bài ngược: biết hai cặp (li độ, tốc độ), tìm tần số góc, biên độ, chu kì, gia tốc cực đại",
         topic="Hệ thức độc lập với thời gian",
         problem_html=r"<p>Một vật dao động điều hoà trên đoạn thẳng. Khi vật đi qua vị trí có li độ $x_1=3\ \text{cm}$ thì tốc độ là $40\ \text{cm/s}$; khi đi qua vị trí có li độ $x_2=4\ \text{cm}$ thì tốc độ là $30\ \text{cm/s}$.</p>"
                      r"<ol type=\"a\"><li>Tính tần số góc $\omega$ và chu kì $T$.</li><li>Tính biên độ $A$.</li><li>Tính tốc độ cực đại và độ lớn gia tốc cực đại.</li></ol>"),
]
for _d in DANG:
    _d["problem_html"] = _d["problem_html"].replace('\\"', '"')

DK_RAD = "⚠ Pha tính bằng rad: máy tính để chế độ radian"
ANALYSIS = [
    [("“$x=5\\cos(4\\pi t+\\pi/3)$ (cm, s)”", "$A=5$ cm; $\\omega=4\\pi$ rad/s; $\\varphi=\\pi/3$", "Dạng $x=A\\cos(\\omega t+\\varphi)$: đọc $A$, $\\omega$, $\\varphi$"),
     ("“tính … theo $t$”", "Pha $\\omega t+\\varphi$ tính bằng rad", DK_RAD),
     ("“tốc độ cực đại”", "Cần $v_{max}$", "$v=-A\\omega\\sin(\\omega t+\\varphi)$ nên $v_{max}=A\\omega$"),
     ("“gia tốc cực đại”", "Cần $a_{max}$", "$a=-\\omega^2x$ nên $a_{max}=A\\omega^2$"),
     ("“viết $v(t)$ và $a(t)$”", "Cần $v(t)$, $a(t)$", "Đạo hàm lần lượt: $v=x'$, $a=v'$"),
     ("“tại $t=1/12$ s, tính $v$ và $a$”", "$t=\\dfrac{1}{12}$ s", "Thế $t$ vào pha rồi vào $v(t)$, $a(t)$"),
     ("“về vị trí cân bằng hay ra biên”", "So dấu của $v$ và $a$", "⚠ $v$, $a$ cùng dấu: nhanh dần, về O; ngược dấu: chậm dần, ra biên")],
    [("“biên độ $A=10$ cm, $\\omega=4$ rad/s”", "$A=10$ cm; $\\omega=4$ rad/s", "$v_{max}=A\\omega$; $a_{max}=A\\omega^2$ là cực trị, chưa phải giá trị tại $x$"),
     ("“đi qua li độ $x=+6$ cm”", "$x=+6$ cm", "Hệ thức độc lập: $A^2=x^2+\\dfrac{v^2}{\\omega^2}$"),
     ("“theo chiều dương”", "$v\\gt0$", "⚠ Hệ thức chỉ cho $|v|$: dấu của $v$ lấy từ chiều chuyển động"),
     ("“tính độ lớn vận tốc”", "Cần $|v|$", "$|v|=\\omega\\sqrt{A^2-x^2}$"),
     ("“tính gia tốc (kể cả dấu)”", "Cần $a$", "$a=-\\omega^2x$ (luôn trái dấu $x$, hướng về O)"),
     ("“nhanh dần hay chậm dần”", "So dấu $v$ và $a$", "Cùng dấu: nhanh dần; ngược dấu: chậm dần; không có “đều”"),
     ("“tốc độ là 24 cm/s”", "$|v|=24$ cm/s", "Giải ngược: $x^2=A^2-\\dfrac{v^2}{\\omega^2}$")],
    [("“đồ thị li độ $x$ theo $t$”", "Đồ thị cho $x(t)$", "$x=A\\cos(\\omega t+\\varphi)$"),
     ("“đọc đồ thị … $A$, $T$”", "$A$ ở đỉnh; $T$ giữa hai đáy (hoặc hai đỉnh) liền nhau", "$\\omega=\\dfrac{2\\pi}{T}$"),
     ("“pha ban đầu $\\varphi$”", "$x(0)$ và hướng đi tại $t=0$", "⚠ $\\cos\\varphi=\\dfrac{x(0)}{A}$ cho hai góc đối nhau: chọn góc khớp hướng đi (độ dốc đồ thị là dấu của $v$)"),
     ("“pha của $v$ và $a$ so với pha của $x$”", "Cần độ lệch pha", "$v$ sớm $x$ góc $\\dfrac{\\pi}{2}$; $a$ sớm $x$ góc $\\pi$ (ngược pha)"),
     ("“viết $v(t)$ và $a(t)$”", "Cần $v(t)$, $a(t)$", "$v=-A\\omega\\sin(\\omega t+\\varphi)$; $a=-A\\omega^2\\cos(\\omega t+\\varphi)$"),
     ("“tính $v$ và $a$ tại $t=0$”", "$t=0$", "Thế $t=0$; kiểm bằng $A^2=x^2+\\dfrac{v^2}{\\omega^2}$ và $a=-\\omega^2x$")],
    [("“biên độ $A=8$ cm, chu kì $T=1{,}2$ s”", "$A=8$ cm; $T=1{,}2$ s", "$\\omega=\\dfrac{2\\pi}{T}$; $v_{max}=A\\omega$"),
     ("“chọn $t=0$ lúc vật ở biên dương”", "$\\varphi=0$", "⚠ $x=A\\cos(\\omega t)$: gốc thời gian ở biên dương"),
     ("“tốc độ bằng một nửa tốc độ cực đại”", "$|v|=\\dfrac{v_{max}}{2}$", "Hệ thức độc lập: $\\left(\\dfrac{x}{A}\\right)^2+\\left(\\dfrac{v}{v_{max}}\\right)^2=1$"),
     ("“li độ có độ lớn”", "Cần $|x|$", "Giải $|x|$ từ hệ thức trên"),
     ("“thời gian ngắn nhất từ $t=0$ đến lúc đó”", "Cần $t$", "Vòng tròn lượng giác: giải $\\cos\\omega t=\\dfrac{x}{A}$ rồi đổi góc sang thời gian"),
     ("“độ lớn gia tốc ở thời điểm đó”", "Cần $|a|$", "$|a|=\\omega^2|x|$")],
    [("“đi qua $x_1=3$ cm thì tốc độ 40 cm/s”", "$x_1=3$ cm; $|v_1|=40$ cm/s", "Hệ thức độc lập viết cho điểm 1: $A^2=x_1^2+\\dfrac{v_1^2}{\\omega^2}$"),
     ("“đi qua $x_2=4$ cm thì tốc độ 30 cm/s”", "$x_2=4$ cm; $|v_2|=30$ cm/s", "Viết cho điểm 2: $A^2=x_2^2+\\dfrac{v_2^2}{\\omega^2}$"),
     ("“một vật dao động điều hoà”", "Hai điểm thuộc một dao động", "⚠ Cùng $A$, cùng $\\omega$: hai phương trình, hai ẩn"),
     ("“tính $\\omega$ và chu kì”", "Cần $\\omega$, $T$", "Trừ vế để khử $A^2$; $T=\\dfrac{2\\pi}{\\omega}$"),
     ("“tính biên độ”", "Cần $A$", "Thế $\\omega$ vào một trong hai hệ thức"),
     ("“tốc độ cực đại, gia tốc cực đại”", "Cần $v_{max}$, $a_{max}$", "$v_{max}=A\\omega$; $a_{max}=A\\omega^2$")],
]

RC1 = [r"<strong>Khái niệm:</strong> $v$ là đạo hàm của $x$ theo $t$; $a$ là đạo hàm của $v$.",
      r"<strong>Công thức:</strong> $v=-A\omega\sin(\omega t+\varphi)$ · $a=-A\omega^2\cos(\omega t+\varphi)=-\omega^2x$",
      r"Cực đại: $v_{max}=A\omega$ · $a_{max}=A\omega^2$",
      r"⚠ <strong>Điều kiện:</strong> pha tính bằng rad (máy tính ở chế độ radian).",
      r"$v$, $a$ cùng dấu: nhanh dần · ngược dấu: chậm dần."]
RC2 = [r"<strong>Khái niệm:</strong> $v$ và $x$ vuông pha nên không cùng đạt cực đại.",
      r"<strong>Hệ thức độc lập:</strong> $A^2=x^2+\dfrac{v^2}{\omega^2}$, suy ra $|v|=\omega\sqrt{A^2-x^2}$",
      r"$a=-\omega^2x$ (trái dấu $x$, hướng về O)",
      r"⚠ <strong>Điều kiện:</strong> hệ thức chỉ cho $|v|$; dấu của $v$ lấy từ chiều chuyển động.",
      r"$v$, $a$ cùng dấu: nhanh dần · ngược dấu: chậm dần."]
RC3 = [r"<strong>Khái niệm:</strong> $v$ sớm $x$ góc $\dfrac{\pi}{2}$; $a$ ngược pha $x$ (sớm $x$ góc $\pi$).",
      r"<strong>Đọc đồ thị:</strong> $A$ ở đỉnh · $T$ giữa hai đáy liền nhau · $\omega=\dfrac{2\pi}{T}$",
      r"$x(0)=A\cos\varphi$; độ dốc đồ thị tại $t=0$ cùng dấu với $v(0)=-A\omega\sin\varphi$",
      r"⚠ <strong>Điều kiện:</strong> $\varphi$ phải khớp cả $x(0)$ lẫn hướng đi, không chỉ $x(0)$."]
RC4 = [r"<strong>Khái niệm:</strong> $|v|$ cực đại ở O, bằng 0 ở biên; $x$ và $v$ vuông pha.",
      r"<strong>Hệ thức độc lập:</strong> $\left(\dfrac{x}{A}\right)^2+\left(\dfrac{v}{v_{max}}\right)^2=1$ · $a=-\omega^2x$",
      r"Vòng tròn lượng giác: $x=A\cos\omega t$, góc quét $\omega t$ đổi sang $t=\dfrac{\omega t}{2\pi}T$.",
      r"⚠ <strong>Điều kiện:</strong> $t=0$ ở biên dương nên $\varphi=0$."]
RC5 = [r"<strong>Khái niệm:</strong> mọi điểm của cùng một dao động có chung $A$ và $\omega$.",
      r"<strong>Hệ thức độc lập:</strong> $A^2=x^2+\dfrac{v^2}{\omega^2}$ viết cho từng điểm",
      r"Trừ vế hai hệ thức để khử $A^2$, giải $\omega$ trước.",
      r"$T=\dfrac{2\pi}{\omega}$ · $v_{max}=A\omega$ · $a_{max}=A\omega^2$",
      r"⚠ <strong>Điều kiện:</strong> hai điểm phải thuộc cùng một dao động."]

SOLS = [
    sol(RC1, [
        ("Tần số góc và tốc độ cực đại", [P(r"Đọc phương trình: $A=5$ cm, $\omega=4\pi$ rad/s, $\varphi=\dfrac{\pi}{3}$."), M(r"v_{max}=A\omega=5\cdot4\pi"), A(r"v_{max}=20\pi\approx62{,}8\ \text{cm/s}")]),
        ("Gia tốc cực đại", [M(r"a_{max}=A\omega^2=5\cdot(4\pi)^2=80\pi^2"), A(r"a_{max}\approx789{,}6\ \text{cm/s}^2")]),
        ("Phương trình $v(t)$ và $a(t)$", [P("Đạo hàm theo $t$:"),
                                           M(r"v=-A\omega\sin(\omega t+\varphi)=-20\pi\sin\left(4\pi t+\dfrac{\pi}{3}\right)\ \text{cm/s}"),
                                           M(r"a=-A\omega^2\cos(\omega t+\varphi)=-80\pi^2\cos\left(4\pi t+\dfrac{\pi}{3}\right)\ \text{cm/s}^2")]),
        ("Vận tốc tại $t=\\dfrac{1}{12}$ s", [P("Pha lúc đó:"), M(r"4\pi\cdot\dfrac{1}{12}+\dfrac{\pi}{3}=\dfrac{2\pi}{3}"),
                                              M(r"v=-20\pi\sin\dfrac{2\pi}{3}=-20\pi\cdot\dfrac{\sqrt3}{2}"), A(r"v\approx-54{,}4\ \text{cm/s}")]),
        ("Gia tốc tại $t=\\dfrac{1}{12}$ s", [M(r"a=-80\pi^2\cos\dfrac{2\pi}{3}=-80\pi^2\cdot\left(-\dfrac{1}{2}\right)"), A(r"a=40\pi^2\approx394{,}8\ \text{cm/s}^2")]),
        ("Chiều chuyển động", [P("$v\\lt0$ còn $a\\gt0$: hai đại lượng ngược dấu."),
                               P(r"Kiểm tra bằng li độ: $x=5\cos\dfrac{2\pi}{3}=-2{,}5$ cm, rồi $a=-\omega^2x=-16\pi^2\cdot(-2{,}5)=40\pi^2$ ✓."),
                               A("T:Vật đang <strong>ra biên</strong> (phía âm), chuyển động chậm dần.")])],
        ["a) $v_{max}\\approx62{,}8\\ \\text{cm/s}$ · $a_{max}\\approx789{,}6\\ \\text{cm/s}^2$",
         r"b) $v=-20\pi\sin\left(4\pi t+\dfrac{\pi}{3}\right)$ cm/s · $a=-80\pi^2\cos\left(4\pi t+\dfrac{\pi}{3}\right)$ cm/s²",
         "c) $v\\approx-54{,}4\\ \\text{cm/s}$ · $a\\approx394{,}8\\ \\text{cm/s}^2$ · vật đang ra biên, chậm dần"],
        "Nhận dạng: đề cho <strong>phương trình li độ</strong> rồi hỏi $v$, $a$ → đạo hàm; cực đại là $A\\omega$ và $A\\omega^2$."),
    sol(RC2, [
        ("Độ lớn vận tốc tại $x=6$ cm", [M(r"|v|=\omega\sqrt{A^2-x^2}=4\sqrt{10^2-6^2}=4\sqrt{64}"), A(r"|v|=32\ \text{cm/s}"),
                                         P("Chiều dương nên $v=+32$ cm/s.")]),
        ("Gia tốc tại $x=6$ cm", [M(r"a=-\omega^2x=-4^2\cdot6"), A(r"a=-96\ \text{cm/s}^2"), P("Dấu trừ: gia tốc hướng về O.")]),
        ("Nhanh dần hay chậm dần", [P("$v=+32$ còn $a=-96$: ngược dấu."), A("T:Vật <strong>chuyển động chậm dần</strong> (đang ra biên dương), không phải “đều”.")]),
        ("Tìm li độ khi tốc độ $24$ cm/s", [P("Từ hệ thức độc lập:"), M(r"x^2=A^2-\dfrac{v^2}{\omega^2}=10^2-\dfrac{24^2}{4^2}=100-36=64"), A(r"|x|=8\ \text{cm}")])],
        ["a) $|v|=32\\ \\text{cm/s}$", "b) $a=-96\\ \\text{cm/s}^2$ · chậm dần", "c) $|x|=8\\ \\text{cm}$"],
        "Nhận dạng: đề cho <strong>li độ</strong> mà hỏi <strong>tốc độ</strong> (hoặc ngược lại) → $A^2=x^2+v^2/\\omega^2$; $a=-\\omega^2x$; so dấu $v$, $a$."),
    sol(RC3, [
        ("Đọc $A$, $T$ và tính $\\omega$", [P("Đỉnh cao nhất ở $x=6$ cm nên $A=6$ cm. Hai đáy liền nhau ở $t=0{,}4$ s và $t=1{,}6$ s nên $T=1{,}2$ s."),
                                            M(r"\omega=\dfrac{2\pi}{T}=\dfrac{2\pi}{1{,}2}=\dfrac{5\pi}{3}"), A(r"\omega\approx5{,}24\ \text{rad/s}")]),
        ("Pha ban đầu của $x$", [P("Tại $t=0$: $x(0)=3$ cm."), M(r"\cos\varphi=\dfrac{x(0)}{A}=\dfrac{3}{6}=\dfrac{1}{2}\ \Rightarrow\ \varphi=\pm\dfrac{\pi}{3}"),
                                 P("Đồ thị đang đi xuống nên $v(0)\\lt0$, tức $\\sin\\varphi\\gt0$."), A(r"\varphi=\dfrac{\pi}{3}")]),
        ("Pha của $v$ và $a$", [P("$v$ sớm $x$ góc $\\dfrac{\\pi}{2}$, $a$ sớm $x$ góc $\\pi$:"),
                                M(r"v=A\omega\cos\left(\omega t+\varphi+\dfrac{\pi}{2}\right)=-10\pi\sin\left(\dfrac{5\pi}{3}t+\dfrac{\pi}{3}\right)\ \text{cm/s}"),
                                M(r"a=A\omega^2\cos\left(\omega t+\varphi+\pi\right)=-\dfrac{50\pi^2}{3}\cos\left(\dfrac{5\pi}{3}t+\dfrac{\pi}{3}\right)\ \text{cm/s}^2")]),
        ("Vận tốc tại $t=0$", [M(r"v(0)=-A\omega\sin\varphi=-10\pi\cdot\dfrac{\sqrt3}{2}"), A(r"v(0)\approx-27{,}2\ \text{cm/s}")]),
        ("Gia tốc tại $t=0$", [M(r"a(0)=-\omega^2x(0)=-\left(\dfrac{5\pi}{3}\right)^2\cdot3"), A(r"a(0)\approx-82{,}2\ \text{cm/s}^2")]),
        ("Kiểm tra", [P("Hệ thức độc lập:"), M(r"x^2+\dfrac{v^2}{\omega^2}=9+\dfrac{27{,}2^2}{5{,}24^2}\approx9+27=36=A^2\ \checkmark"),
                      P("$v(0)\\lt0$ khớp độ dốc xuống; $a(0)$ trái dấu $x(0)$ ✓.")])],
        ["a) $A=6\\ \\text{cm}$ · $T=1{,}2\\ \\text{s}$ · $\\omega\\approx5{,}24\\ \\text{rad/s}$ · $\\varphi=\\dfrac{\\pi}{3}$",
         r"b) $v=-10\pi\sin\left(\dfrac{5\pi}{3}t+\dfrac{\pi}{3}\right)$ cm/s · $a=-\dfrac{50\pi^2}{3}\cos\left(\dfrac{5\pi}{3}t+\dfrac{\pi}{3}\right)$ cm/s² · $v$ sớm $x$ góc $\dfrac{\pi}{2}$, $a$ sớm $x$ góc $\pi$",
         "c) $v(0)\\approx-27{,}2\\ \\text{cm/s}$ · $a(0)\\approx-82{,}2\\ \\text{cm/s}^2$"],
        "Nhận dạng: đề cho <strong>đồ thị $x$–$t$</strong> → đọc $A$, $T$; $x(0)$ cùng hướng đi cho $\\varphi$; rồi dùng quan hệ pha."),
    sol(RC4, [
        ("Tốc độ cực đại", [M(r"\omega=\dfrac{2\pi}{T}=\dfrac{2\pi}{1{,}2}=\dfrac{5\pi}{3}\ \text{rad/s}"), M(r"v_{max}=A\omega=8\cdot\dfrac{5\pi}{3}"), A(r"v_{max}=\dfrac{40\pi}{3}\approx41{,}9\ \text{cm/s}")]),
        ("Li độ khi $|v|=\\dfrac{v_{max}}{2}$", [P("Hệ thức độc lập với $\\dfrac{v}{v_{max}}=\\dfrac{1}{2}$:"),
                                                 M(r"\left(\dfrac{x}{A}\right)^2=1-\left(\dfrac{1}{2}\right)^2=\dfrac{3}{4}"), M(r"|x|=\dfrac{A\sqrt3}{2}=4\sqrt3"),
                                                 A(r"|x|\approx6{,}93\ \text{cm}")]),
        ("Thời gian ngắn nhất từ biên dương", [P("$x=A\\cos\\omega t$, cần $x=\\dfrac{A\\sqrt3}{2}$:"), M(r"\cos\omega t=\dfrac{\sqrt3}{2}\ \Rightarrow\ \omega t=\dfrac{\pi}{6}"),
                                               M(r"t=\dfrac{\pi/6}{2\pi}T=\dfrac{T}{12}=\dfrac{1{,}2}{12}"), A(r"t=0{,}1\ \text{s}")]),
        ("Độ lớn gia tốc", [M(r"|a|=\omega^2|x|=\left(\dfrac{5\pi}{3}\right)^2\cdot4\sqrt3"), A(r"|a|\approx190\ \text{cm/s}^2"),
                            P(r"Kiểm tra: $a_{max}=A\omega^2\approx219$ và $\dfrac{\sqrt3}{2}a_{max}\approx190$ ✓.")])],
        ["a) $v_{max}\\approx41{,}9\\ \\text{cm/s}$", "b) $|x|\\approx6{,}93\\ \\text{cm}$", "c) $t=0{,}1\\ \\text{s}\\ (=T/12)$", "d) $|a|\\approx190\\ \\text{cm/s}^2$"],
        "Nhận dạng: đề cho <strong>tốc độ bằng một phần của cực đại</strong> → hệ thức độc lập tìm $x$; vòng tròn lượng giác tìm thời gian."),
    sol(RC5, [
        ("Lập hai hệ thức độc lập rồi trừ vế", [P("Cùng $A$, $\\omega$ cho hai điểm:"), M(r"A^2=x_1^2+\dfrac{v_1^2}{\omega^2}\qquad A^2=x_2^2+\dfrac{v_2^2}{\omega^2}"),
                                                P("Trừ vế để khử $A^2$:"), M(r"x_2^2-x_1^2=\dfrac{v_1^2-v_2^2}{\omega^2}"),
                                                M(r"\omega^2=\dfrac{v_1^2-v_2^2}{x_2^2-x_1^2}=\dfrac{40^2-30^2}{4^2-3^2}=\dfrac{700}{7}=100"), A(r"\omega=10\ \text{rad/s}")]),
        ("Biên độ", [M(r"A^2=x_1^2+\dfrac{v_1^2}{\omega^2}=3^2+\dfrac{40^2}{10^2}=9+16=25"), A(r"A=5\ \text{cm}")]),
        ("Chu kì", [M(r"T=\dfrac{2\pi}{\omega}=\dfrac{2\pi}{10}"), A(r"T\approx0{,}628\ \text{s}")]),
        ("Cực đại của $v$ và $a$", [M(r"v_{max}=A\omega=5\cdot10=50\ \text{cm/s}"), M(r"a_{max}=A\omega^2=5\cdot10^2"), A(r"a_{max}=500\ \text{cm/s}^2")]),
        ("Kiểm tra", [P("Thử lại với điểm 2:"), M(r"|v_2|=\omega\sqrt{A^2-x_2^2}=10\sqrt{25-16}=30\ \text{cm/s}\ \checkmark"),
                      P("$v_{max}=50\\gt40$ và $\\gt30$: hợp lí vì hai điểm đều chưa phải O.")])],
        ["a) $\\omega=10\\ \\text{rad/s}$ · $T\\approx0{,}628\\ \\text{s}$", "b) $A=5\\ \\text{cm}$", "c) $v_{max}=50\\ \\text{cm/s}$ · $a_{max}=500\\ \\text{cm/s}^2$"],
        "Nhận dạng: đề cho <strong>hai cặp ($x$, $v$)</strong> rồi hỏi $A$, $\\omega$ → viết hệ thức độc lập hai lần, trừ vế khử $A^2$."),
]

STEPS = [
    dict(nhan_dang=r"Thấy <b>phương trình li độ</b> rồi hỏi $v$, $a$ → lấy đạo hàm: $v=-A\omega\sin(\cdot)$, $a=-\omega^2x$.",
         cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 3}, buoc=[
        buoc("Tần số góc và tốc độ cực đại", "Tốc độ cực đại $v_{max}$ bằng bao nhiêu?", 62.8, "cm/s", 0.3,
             loi=r"Hay lấy $v_{max}=A$ (quên $\omega$) hoặc $\omega=4$ thay vì $4\pi$; hệ số đứng trước $t$ mới là $\omega$."),
        buoc("Gia tốc cực đại", "Độ lớn gia tốc cực đại $a_{max}$ bằng bao nhiêu?", 789.6, "cm/s²", 4,
             loi=r"Dùng $A\omega$ (đó là $v_{max}$) hoặc quên bình phương $\omega$; gia tốc có $\omega^2$.",
             ke=[(r"$a_{max}=A\omega^2$ vì $a=-\omega^2x$ và $|x|_{max}=A$", True),
                 (r"$a_{max}=A\omega$", "Đó là tốc độ cực đại; gia tốc có thêm một thừa số $\\omega$ nữa."),
                 (r"$a_{max}=\omega^2x$ với $x=5\cos\dfrac{\pi}{3}$", "Cực đại phải lấy $|x|=A$, không lấy li độ ở thời điểm $t=0$.")]),
        buoc("Phương trình $v(t)$ và $a(t)$", "Chọn phương trình vận tốc đúng.",
             loi=r"Quên dấu trừ, hoặc quên nhân $\omega$ khi đạo hàm hàm hợp.",
             lua_chon=[(r"$v=-20\pi\sin\left(4\pi t+\dfrac{\pi}{3}\right)$", True),
                       (r"$v=20\pi\cos\left(4\pi t+\dfrac{\pi}{3}\right)$", "Đạo hàm của cos là −sin, không phải cos: $v$ không cùng dạng với $x$."),
                       (r"$v=-5\sin\left(4\pi t+\dfrac{\pi}{3}\right)$", "Thiếu thừa số $\\omega$ khi đạo hàm hàm hợp; hệ số ở đầu phải là $A\\omega$.")]),
        buoc("Vận tốc tại $t=\\dfrac{1}{12}$ s", "Vận tốc $v$ lúc $t=\\dfrac{1}{12}$ s bằng bao nhiêu (kể cả dấu)?", -54.4, "cm/s", 0.4,
             loi=r"Thế $t$ mà quên cộng $\varphi$ vào pha, hoặc để máy tính ở chế độ độ.",
             ke=[(r"Tính pha $\omega t+\varphi$ trước, rồi thế vào $v(t)$", True),
                 (r"Thế $t$ vào $x$ rồi lấy $v=\omega x$", "$v$ và $x$ vuông pha, không tỉ lệ nhau: $v$ lấy từ $v(t)$ hoặc $\\omega\\sqrt{A^2-x^2}$ kèm dấu."),
                 (r"Dùng $v_{max}$ vì $v$ cực đại", "Chỉ ở O thì $|v|$ mới cực đại; pha lúc này chưa tới đó.")]),
        buoc("Gia tốc tại $t=\\dfrac{1}{12}$ s", "Gia tốc $a$ lúc $t=\\dfrac{1}{12}$ s bằng bao nhiêu (kể cả dấu)?", 394.8, "cm/s²", 3,
             loi=r"Sai dấu: $a$ luôn trái dấu với $x$ lúc đó; xét dấu của $\cos$ ở pha vừa tính.",
             ke=[(r"Thế pha vào $a(t)$, hoặc dùng $a=-\omega^2x$ với $x$ lúc đó", True),
                 (r"Lấy $a=\dfrac{dv}{dt}$ bằng $v/t$", "$a$ là đạo hàm, không phải thương $v/t$ (chuyển động không đều)."),
                 (r"Dùng $a_{max}$ vì $a$ cực đại", "Cực đại chỉ ở biên; lúc này $|x|\\lt A$.")]),
        buoc("Chiều chuyển động", "Lúc đó vật đang ở trạng thái nào?",
             loi=r"Nhìn vào dấu của riêng $v$ hay $a$ mà không so với nhau.",
             lua_chon=[(r"Ra biên, chậm dần", True),
                       (r"Về O, nhanh dần", "Nhanh dần khi $v$, $a$ cùng dấu; ở đây $v\\lt0$ còn $a\\gt0$."),
                       (r"Chuyển động nhanh dần đều", "Trong dao động điều hoà không có “đều”: $a$ đổi theo vị trí.")],
             ke=[(r"So dấu của $v$ và $a$", True),
                 (r"Chỉ xét dấu của $a$", "$a\\gt0$ chỉ nói gia tốc hướng về phía dương, chưa nói vật nhanh hay chậm."),
                 (r"Chỉ xét độ lớn của $v$", "Độ lớn của một giá trị đơn lẻ không cho biết đang tăng hay giảm.")])]),
    dict(nhan_dang=r"Biết <b>li độ</b> hỏi <b>tốc độ</b> (hoặc ngược lại) → $A^2=x^2+\dfrac{v^2}{\omega^2}$; $a=-\omega^2x$; so dấu $v$, $a$.",
         cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
        buoc("Độ lớn vận tốc tại $x=6$ cm", "Độ lớn vận tốc $|v|$ tại li độ đó bằng bao nhiêu?", 32, "cm/s", 0.2,
             loi=r"Lấy $A\omega$ (chỉ đúng tại O) hoặc quên nhân $\omega$ sau khi khai căn."),
        buoc("Gia tốc tại $x=6$ cm", "Gia tốc $a$ (chiều dương là chiều Ox) bằng bao nhiêu?", -96, "cm/s²", 1,
             loi=r"Quên dấu trừ hoặc quên bình phương $\omega$.",
             ke=[(r"$a=-\omega^2x$ vì gia tốc luôn hướng về O", True),
                 (r"$a=-\omega x$", "Thiếu bình phương: đơn vị của $\\omega x$ là cm/s, không phải cm/s²."),
                 (r"$a=-\omega^2A$", "Đó là gia tốc ở biên; vật đang ở $x\\lt A$ nên phải dùng $x$ hiện tại.")]),
        buoc("Nhanh dần hay chậm dần", "Vật đang chuyển động thế nào?",
             loi=r"Cho rằng cứ đi theo chiều dương là nhanh dần, hoặc gọi là “nhanh dần đều”.",
             lua_chon=[(r"Chậm dần, vì $v$ và $a$ ngược dấu", True),
                       (r"Nhanh dần, vì $|a|$ khá lớn", "Nhanh hay chậm do $v$ và $a$ cùng hay ngược dấu, không do $|a|$ lớn hay nhỏ."),
                       (r"Nhanh dần đều, vì vật đi theo chiều dương", "Không có nhanh dần đều trong dao động điều hoà; chiều dương cũng không quyết định nhanh hay chậm.")],
             ke=[(r"So dấu của $v$ và $a$", True),
                 (r"So $|v|$ với $A\omega$", "Phép so đó chỉ cho biết vật gần O hay xa O, chưa cho biết đang nhanh hay chậm dần."),
                 (r"Chỉ nhìn chiều chuyển động", "Chiều chuyển động không đủ: phải so với chiều của gia tốc.")]),
        buoc("Tìm li độ khi tốc độ cho trước", "Khi tốc độ là 24 cm/s thì $|x|$ bằng bao nhiêu?", 8, "cm", 0.1,
             loi=r"Quên chia $v^2$ cho $\omega^2$ (đơn vị cm²/s² không cộng được với cm²).",
             ke=[(r"$x^2=A^2-\dfrac{v^2}{\omega^2}$", True),
                 (r"$x^2=A^2-v^2$", "Thiếu $\\omega^2$ ở mẫu: $v$ và $x$ khác đơn vị, không trừ trực tiếp được."),
                 (r"$x=\dfrac{v}{\omega}$", "$\\dfrac{v}{\\omega}$ cùng đơn vị với $x$ nhưng bằng $\\sqrt{A^2-x^2}$, không phải $x$.")])]),
    dict(nhan_dang=r"Cho <b>đồ thị $x$–$t$</b> → đọc $A$, $T$; $x(0)$ và hướng đi cho $\varphi$; $v$ sớm $\dfrac{\pi}{2}$, $a$ sớm $\pi$ so với $x$.",
         cap_do=2, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
        buoc("Đọc $A$, $T$ và tính $\\omega$", "Tần số góc $\\omega$ bằng bao nhiêu?", 5.24, "rad/s", 0.03,
             loi=r"Lấy $\omega=\dfrac{1}{T}$ (đó là $f$), hoặc đọc $T$ từ đỉnh đến đáy (chỉ là nửa chu kì)."),
        buoc("Pha ban đầu của $x$", "Pha ban đầu $\\varphi$ của li độ là bao nhiêu?",
             loi=r"Chỉ dùng $\cos\varphi=\dfrac{x(0)}{A}$ rồi lấy góc dương, quên xét đồ thị đi lên hay đi xuống.",
             lua_chon=[(r"$\varphi=\dfrac{\pi}{3}$, vì $x(0)=\dfrac{A}{2}$ và đồ thị đang đi xuống", True),
                       (r"$\varphi=-\dfrac{\pi}{3}$", "Cùng $x(0)=\\dfrac{A}{2}$ nhưng ứng với đồ thị đang đi lên ($v\\gt0$)."),
                       (r"$\varphi=\dfrac{\pi}{6}$", "$\\cos\\dfrac{\\pi}{6}=\\dfrac{\\sqrt3}{2}$, không phải $\\dfrac{1}{2}$.")],
             ke=[(r"Dùng $x(0)$ để tìm $|\varphi|$, rồi xét hướng đi để chọn dấu", True),
                 (r"Chọn $\varphi=0$ vì đồ thị bắt đầu ở $t=0$", "$\\varphi=0$ chỉ khi $t=0$ ở biên dương; ở đây $x(0)$ chưa phải đỉnh."),
                 (r"Chỉ dùng độ dốc đồ thị, bỏ qua $x(0)$", "Độ dốc chỉ cho dấu của $v(0)$; độ lớn của $\\varphi$ phải lấy từ $x(0)$.")]),
        buoc("Pha của $v$ và $a$", "Chọn pha đúng của $v$ và $a$.",
             loi=r"Nhớ ngược: cho rằng $v$ trễ $x$ góc $\dfrac{\pi}{2}$.",
             lua_chon=[(r"$v$ có pha $\omega t+\varphi+\dfrac{\pi}{2}$; $a$ có pha $\omega t+\varphi+\pi$", True),
                       (r"$v$ có pha $\omega t+\varphi-\dfrac{\pi}{2}$; $a$ có pha $\omega t+\varphi-\pi$", "$v$ là đạo hàm nên sớm pha hơn $x$ góc $\\dfrac{\\pi}{2}$, không trễ."),
                       (r"$v$ có pha $\omega t+\varphi$; $a$ có pha $\omega t+\varphi+\pi$", "$v$ vuông pha $x$, không cùng pha: $v=-A\\omega\\sin(\\cdot)$.")],
             ke=[(r"Viết $v=x'$ và $a=v'$ rồi đổi $-\sin$, $-\cos$ về dạng cos", True),
                 (r"Cho $v$ cùng pha $x$ vì cùng tần số", "Cùng tần số không có nghĩa cùng pha: $v$ lệch $x$ một góc $\\dfrac{\\pi}{2}$."),
                 (r"Lấy pha của $a$ bằng pha của $v$", "$a$ lệch $v$ thêm $\\dfrac{\\pi}{2}$ nữa, tổng cộng $\\pi$ so với $x$.")]),
        buoc("Vận tốc tại $t=0$", "Vận tốc $v(0)$ bằng bao nhiêu (kể cả dấu)?", -27.2, "cm/s", 0.3,
             loi=r"Dùng $v(0)=A\omega$ (cực đại) hoặc quên dấu: dấu của $v(0)$ phải khớp độ dốc của đồ thị tại $t=0$.",
             ke=[(r"$v(0)=-A\omega\sin\varphi$", True),
                 (r"$v(0)=A\omega\cos\varphi$", "Nhầm sin với cos: $v$ chứa $\\sin$, còn $\\cos$ là của $x$."),
                 (r"$v(0)=\omega x(0)$", "$v$ và $x$ vuông pha, không tỉ lệ nhau.")]),
        buoc("Gia tốc tại $t=0$", "Gia tốc $a(0)$ bằng bao nhiêu (kể cả dấu)?", -82.2, "cm/s²", 0.8,
             loi=r"Quên dấu trừ trong $a=-\omega^2x$; hoặc nhân $\omega$ thay vì $\omega^2$.",
             ke=[(r"$a(0)=-\omega^2x(0)$", True),
                 (r"$a(0)=-\omega^2A$", "Đó là gia tốc ở biên; $t=0$ vật chưa ở biên."),
                 (r"$a(0)=-\omega x(0)$", "Thiếu bình phương $\\omega$.")]),
        buoc("Kiểm tra")]),
    dict(nhan_dang=r"Hỏi <b>tốc độ bằng một phần của cực đại</b> → hệ thức độc lập tìm $x$; vòng tròn lượng giác tìm thời gian.",
         cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 1}, buoc=[
        buoc("Tốc độ cực đại", "Tốc độ cực đại $v_{max}$ bằng bao nhiêu?", 41.9, "cm/s", 0.2,
             loi=r"Lấy $\omega=\dfrac{1}{T}$ hoặc $2\pi T$; phải là $\omega=\dfrac{2\pi}{T}$."),
        buoc("Li độ khi $|v|=\\dfrac{v_{max}}{2}$", "Khi đó $|x|$ bằng bao nhiêu?", 6.93, "cm", 0.05,
             loi=r"Cho rằng tốc độ giảm một nửa thì li độ cũng bằng một nửa biên độ — $x$ và $v$ không tỉ lệ (quan hệ là elip).",
             ke=[(r"Dùng $\left(\dfrac{x}{A}\right)^2+\left(\dfrac{v}{v_{max}}\right)^2=1$", True),
                 (r"$|x|=\dfrac{A}{2}$ vì $|v|=\dfrac{v_{max}}{2}$", "$x$ và $v$ vuông pha, không tỉ lệ: quan hệ là elip."),
                 (r"$|x|=\dfrac{v}{\omega}$", "$\\dfrac{v}{\\omega}$ bằng $\\sqrt{A^2-x^2}$, không phải $x$.")]),
        buoc("Thời gian ngắn nhất từ biên dương", "Khoảng thời gian ngắn nhất đó bằng bao nhiêu?", 0.1, "s", 0.005,
             loi=r"Dùng nhầm mốc $\dfrac{A}{2}$ (ứng với $\dfrac{T}{6}$) hoặc $\dfrac{T}{4}$ (tới O).",
             ke=[(r"Giải $\cos\omega t=\dfrac{x}{A}$ rồi đổi góc sang thời gian", True),
                 (r"Lấy $t=\dfrac{T}{6}$ vì $x=\dfrac{A}{2}$", "Mốc $\\dfrac{T}{6}$ ứng với $x=\\dfrac{A}{2}$; ở đây $x=\\dfrac{A\\sqrt3}{2}$."),
                 (r"Lấy $t=\dfrac{T}{4}$ vì tốc độ cực đại ở O", "$\\dfrac{T}{4}$ là lúc tới O, tốc độ khi đó đã cực đại chứ chưa bằng một nửa.")]),
        buoc("Độ lớn gia tốc", "Độ lớn gia tốc $|a|$ lúc đó bằng bao nhiêu?", 190, "cm/s²", 1.5,
             loi=r"Cho rằng $v$ giảm một nửa thì $a$ cũng một nửa $a_{max}$; $a$ tỉ lệ với $x$, không với $v$.",
             ke=[(r"$|a|=\omega^2|x|$ với $|x|$ vừa tìm", True),
                 (r"$|a|=\dfrac{a_{max}}{2}$ vì $|v|=\dfrac{v_{max}}{2}$", "$a$ tỉ lệ với $x$ chứ không với $v$; tốc độ giảm thì $|a|$ lại tăng."),
                 (r"$|a|=\omega^2A$", "Đó là $a_{max}$ ở biên; lúc này $|x|\\lt A$.")])]),
    dict(nhan_dang=r"Cho <b>hai cặp ($x$, $v$)</b> rồi hỏi $A$, $\omega$ → viết hệ thức độc lập hai lần, trừ vế để khử $A^2$.",
         cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 0}, buoc=[
        buoc("Lập hai hệ thức độc lập rồi trừ vế", "Tần số góc $\\omega$ bằng bao nhiêu?", 10, "rad/s", 0.1,
             loi=r"Cố tìm $A$ trước. Hai hệ thức chung $A^2$, nên trừ vế để khử $A^2$ rồi rút $\omega^2$; chú ý thứ tự trừ ở tử và ở mẫu."),
        buoc("Biên độ", "Biên độ $A$ bằng bao nhiêu?", 5, "cm", 0.05,
             loi=r"Cộng hai li độ hoặc lấy li độ lớn hơn làm biên độ.",
             ke=[(r"Thế $\omega$ vào $A^2=x^2+\dfrac{v^2}{\omega^2}$", True),
                 (r"$A=x_1+x_2$", "Hai li độ thuộc hai thời điểm khác nhau, cộng lại không cho biên độ."),
                 (r"$A=x_2$ vì $x_2$ lớn hơn", "Tại $x_2$ tốc độ vẫn khác 0 nên vật còn đi tiếp tới biên.")]),
        buoc("Chu kì", "Chu kì $T$ bằng bao nhiêu?", 0.628, "s", 0.005,
             loi=r"Lấy $T=\dfrac{\omega}{2\pi}$ (đó là $f$) hoặc $T=\dfrac{1}{\omega}$.",
             ke=[(r"$T=\dfrac{2\pi}{\omega}$", True),
                 (r"$T=\dfrac{\omega}{2\pi}$", "Đó là tần số $f$ (Hz), không phải chu kì."),
                 (r"$T=\dfrac{1}{\omega}$", "Thiếu $2\\pi$: $\\omega$ đo bằng rad/s, một vòng ứng với $2\\pi$ rad.")]),
        buoc("Cực đại của $v$ và $a$", "Gia tốc cực đại $a_{max}$ bằng bao nhiêu?", 500, "cm/s²", 5,
             loi=r"Dùng $A\omega$ (đó là $v_{max}$) hoặc thế $x_2$ thay vì $A$.",
             ke=[(r"$a_{max}=A\omega^2$", True),
                 (r"$a_{max}=A\omega$", "Đó là tốc độ cực đại."),
                 (r"$a_{max}=\omega^2x_2$", "$x_2$ chưa phải biên; cực đại phải lấy $|x|=A$.")]),
        buoc("Kiểm tra")]),
]

d = {"lesson_id": 22, "lesson_title": "Bài 3. Vận tốc, gia tốc trong dao động điều hoà", "generated_at": "2026-10-09",
     "review": {"checked": True, "notes": "Kiểm chéo độc lập 9/10/2026: 5 dạng tự giải khớp, 23 bước buoc[] khớp; sửa nhãn đè ở hình dạng 2, 3, 4 và bỏ lộ dấu v(0) ở loi_hay_gap dạng 3."},
     "dang_bai": [dict(form="bai_tap", solution_html="", **x) for x in DANG]}
json.dump(d, open(J, "w"), ensure_ascii=False, indent=1)
inject(J, BUILD, ANALYSIS, SOLS, STEPS)
