"""Bài tập mẫu CĐ07 "Thấu kính mỏng và kính lúp" (lesson 156) — Dạng 1–3. Module được build-hinh-156.py import.
Dàn ý + số liệu đã tính: content/hsg9/cd07-thau-kinh-kinh-lup/nguon.md (mục "Bài tập mẫu", D1–D3 dùng nguyên số) + tinh.py.
Quy ước (nguon.md): d > 0 vật thật; d' > 0 ảnh thật, d' < 0 ảnh ảo; f > 0 hội tụ, f < 0 phân kì; 1/f = 1/d + 1/d'; h'/h = |d'|/d.
Hình: tia sáng nét liền có mũi tên giữa tia; đường kéo dài + ảnh ảo nét đứt; hình ĐỀ không vẽ sẵn ảnh. Dạng 1 có lưới ô ly mờ.
Mọi đáp số tính lại bằng Python trong kiem_so(); mọi lựa chọn sai được assert cho số khác đáp án đúng."""
import math
from fractions import Fraction as Fr
from dung import *   # sol, buoc, M/P/A, fig, seg, lbl, poly, arrow, chevron, ball, RED/BLUE/ORG/GRN

GREY = "#94a3b8"
TOPIC_DUNG = "Dựng ảnh của vật qua thấu kính"
TOPIC_CT = "Công thức thấu kính và số phóng đại"


def anh(f, d):
    """d' theo 1/f = 1/d + 1/d' (Fraction); None nếu ảnh ở vô cực."""
    f, d = Fr(f), Fr(d)
    inv = 1 / f - 1 / d
    return None if inv == 0 else 1 / inv


# ── số liệu D1 (1 ô = 2 cm ở hình a; 1 ô = 1 cm ở hình b) ──
F1, D1, H1 = 8, 12, 2
D1P = anh(F1, D1)                       # 24
H1P = abs(D1P) / D1 * H1                # 4
XB, YB, XBP, YBP = -24, 3, -8, 1        # hình b, cm, gốc tại O (HS không biết)
X_O = XB + (0 - YB) * (XBP - XB) / Fr(YBP - YB)        # giao BB' với trục
X_F = 0 + (0 - YB) * (XBP - 0) / Fr(YBP - YB)          # đường kéo dài IB' cắt trục, I(0; 3)
F1B = X_F - X_O                                         # F' cùng phía vật → f < 0
D1B = X_O - XB
# ── số liệu D2 ──
F2A, D2A, H2A = 20, 15, 1
D2AP = anh(F2A, D2A)                    # -60
H2AP = abs(D2AP) / D2A * H2A            # 4
L2A = abs(D2A + D2AP)                   # 45
F2B, D2B, H2B = -30, 15, Fr(3, 2)
D2BP = anh(F2B, D2B)                    # -10
H2BP = abs(D2BP) / D2B * H2B            # 1
L2B = abs(D2B + D2BP)                   # 5
# ── số liệu D3 ──
F3 = 12
D3_THAT = Fr(F3) * 4 / 3                # d' = 3d
D3_AO = Fr(F3) * 2 / 3                  # d' = -3d
L3 = 50


def roots(a, b, c):
    r = math.sqrt(b * b - 4 * a * c)
    return sorted([(-b - r) / (2 * a), (-b + r) / (2 * a)])


R3_THAT = roots(1, -L3, L3 * F3)        # d² − 50d + 600 = 0
R3_AO = roots(1, L3, -L3 * F3)          # d² + 50d − 600 = 0


def anim(attr, vals, dur, kt=None):
    k = f' keyTimes="{kt}"' if kt else ""
    return f'<animate attributeName="{attr}" values="{vals}"{k} dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'


# ═════════════ HÌNH: linh kiện quang ═════════════
def grid(X, Y, u0, u1, v0, v1):
    """Lưới ô ly mờ, mỗi ô 1 đơn vị lưới."""
    g = '<g opacity="0.5">'
    for u in range(u0, u1 + 1):
        g += f'<line x1="{X(u):.1f}" y1="{Y(v0):.1f}" x2="{X(u):.1f}" y2="{Y(v1):.1f}" stroke="{GREY}" stroke-width="0.7"/>'
    for v in range(v0, v1 + 1):
        g += f'<line x1="{X(u0):.1f}" y1="{Y(v):.1f}" x2="{X(u1):.1f}" y2="{Y(v):.1f}" stroke="{GREY}" stroke-width="0.7"/>'
    return g + "</g>"


def ray(x1, y1, x2, y2, c=ORG, w=2.2, at=0.55):
    """Tia sáng: nét liền + mũi tên chữ V giữa tia."""
    mx, my = x1 + (x2 - x1) * at, y1 + (y2 - y1) * at
    return seg(x1, y1, x2, y2, c, w) + chevron(mx, my, x2 - x1, y2 - y1, c, w, 9)


def ext(x1, y1, x2, y2, c=ORG, w=1.5):
    """Đường kéo dài (ảnh ảo): nét đứt, không mũi tên."""
    return seg(x1, y1, x2, y2, c, w, "5 4")


def lens(x, yt, yb, ht=True, c=BLUE):
    """TK hội tụ: hai mũi tên hướng ra; phân kì: hai đầu chữ V hướng vào."""
    s = seg(x, yt, x, yb, c, 2.6)
    if ht:
        return s + chevron(x, yt, 0, -1, c, 2.4, 10) + chevron(x, yb, 0, 1, c, 2.4, 10)
    return s + chevron(x, yt, 0, 1, c, 2.4, 10) + chevron(x, yb, 0, -1, c, 2.4, 10)


def vat(x, y0, y1, c=ORG, dash=False, w=2.6):
    """Mũi tên vật/ảnh từ chân (trên trục) lên đỉnh."""
    s = seg(x, y0, x, y1, c, w, "5 4" if dash else "")
    return s + chevron(x, y1, 0, y1 - y0, c, w, 9)


def tick(x, y, name, below=True, c="currentColor", dx=0):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{c}"/>'
            + lbl(x + dx, y + (17 if below else -8), name, c, 14, "middle", "700"))


def axis(x0, x1, y, lab=True):
    s = seg(x0, y, x1, y, "currentColor", 1.6)
    return s + (lbl(x1 - 2, y - 6, "Δ", "currentColor", 14, "end", "700") if lab else "")


def mk(ox, oy, sx, sy):
    return (lambda u: float(ox + sx * u)), (lambda v: float(oy - sy * v))


# ───────────── Dạng 1 · dựng ảnh trên giấy ô ly ─────────────
def pan1a(X, Y, mode):
    """Hình a: 1 ô = 2 cm. TK hội tụ f = 4 ô, vật cao 1 ô, cách TK 6 ô. mode: 'de' (không có ảnh) | 'giai'."""
    b = grid(X, Y, -8, 14, -3, 3) + axis(X(-8), X(14), Y(0))
    b += lens(X(0), Y(2.7), Y(-2.7), True)
    b += tick(X(-4), Y(0), "F") + tick(X(4), Y(0), "F′") + lbl(X(0) + 6, Y(0) + 17, "O", "currentColor", 14, "start", "700")
    b += vat(X(-6), Y(0), Y(1)) + lbl(X(-6), Y(0) + 17, "A", ORG, 14, "middle", "700") + lbl(X(-6) - 6, Y(1) - 2, "B", ORG, 14, "end", "700")
    if mode == "giai":
        b += ray(X(-6), Y(1), X(0), Y(1)) + ray(X(0), Y(1), X(13.6), Y(1 - 13.6 / 4), ORG, 2.2, 0.3)
        b += ray(X(-6), Y(1), X(13.6), Y(-13.6 / 6), GRN, 2.2, 0.25)
        b += ray(X(-6), Y(1), X(0), Y(-2), BLUE, 2, 0.4) + ray(X(0), Y(-2), X(13.6), Y(-2), BLUE, 2, 0.3)
        b += lbl(X(0) + 5, Y(1) - 5, "I", "currentColor", 14, "start", "700") + lbl(X(0) - 5, Y(-2) + 15, "K", "currentColor", 14, "end", "700")
        b += vat(X(12), Y(0), Y(-2), RED) + lbl(X(12) - 6, Y(0) - 6, "A′", RED, 14, "end", "700")
        b += lbl(X(12) + 6, Y(-2) + 16, "B′", RED, 14, "start", "700")
    return b


def pan1b(X, Y, mode):
    """Hình b: 1 ô = 1 cm. B(−24; 3), B'(−8; 1), O tại x = 0 (chưa vẽ ở đề)."""
    b = grid(X, Y, -28, 6, -2, 5) + axis(X(-28), X(6), Y(0))
    b += vat(X(XB), Y(0), Y(YB)) + lbl(X(XB), Y(0) + 16, "A", ORG, 14, "middle", "700") + lbl(X(XB) - 6, Y(YB) - 2, "B", ORG, 14, "end", "700")
    if mode == "de":
        b += vat(X(XBP), Y(0), Y(YBP), "currentColor", False, 2) + lbl(X(XBP), Y(0) + 16, "A′", "currentColor", 14, "middle", "700")
        b += lbl(X(XBP) + 6, Y(YBP) - 4, "B′", "currentColor", 14, "start", "700")
        return b
    b += lens(X(0), Y(4.7), Y(-1.8), False)
    b += ray(X(XB), Y(YB), X(0), Y(YB)) + ray(X(0), Y(YB), X(6), Y(YB + 6 * Fr(YB, 12)), ORG, 2.2, 0.6)
    b += ext(X(0), Y(YB), X(X_F), Y(0))
    b += ray(X(XB), Y(YB), X(6), Y(-6 * Fr(YB, D1B)), GRN, 2.2, 0.3)
    b += vat(X(XBP), Y(0), Y(YBP), RED, True, 2.2) + lbl(X(XBP), Y(0) + 16, "A′", RED, 14, "middle", "700")
    b += lbl(X(XBP) - 4, Y(YBP) + 2, "B′", RED, 14, "end", "700")
    b += tick(X(X_F), Y(0), "F′", True, BLUE) + lbl(X(0) + 6, Y(0) + 16, "O", "currentColor", 14, "start", "700")
    b += lbl(X(0) + 6, Y(YB) - 6, "I", "currentColor", 14, "start", "700")
    return b


def d1(kk):
    if kk == 0:
        DUR = 2.0
        X, Y = mk(159, 88, 17, 17)
        b = lbl(8, 22, "Hình a · mỗi ô 2 cm", "currentColor", 14, "start", "700") + pan1a(X, Y, "de")
        bx, by = X(-6), Y(1)
        b += seg(bx, by, X(0), Y(1), ORG, 1.4, "", 0.55) + seg(bx, by, X(0), Y(0), ORG, 1.4, "", 0.55)
        b += ball([(bx, by), (X(0), Y(1))], 0, DUR) + ball([(bx, by), (X(0), Y(0))], 0, DUR)
        b += (f'<g opacity="0">{anim("opacity", "0;0;1", DUR + 0.4, "0;0.85;1")}'
              f'{lbl(X(1.2), Y(1) - 6, "?", GRN, 16, "start", "700")}{lbl(X(1.2), Y(0) - 6, "?", GRN, 16, "start", "700")}'
              f'{lbl(X(13.8), Y(2.25), "tia ló đi tiếp thế nào?", GRN, 14, "end", "700")}</g>')
        X2, Y2 = mk(331, 235, 11, 11)
        b += lbl(8, 168, "Hình b · mỗi ô 1 cm · thấu kính chưa vẽ", "currentColor", 14, "start", "700") + pan1b(X2, Y2, "de")
        return fig("c07-1-0", "0 0 420 272",
                   "Hai lưới ô ly: hình a có thấu kính hội tụ, hai tiêu điểm và vật AB, hai chấm sáng đi từ B tới thấu kính; hình b chỉ có trục chính, vật AB và ảnh A phẩy B phẩy",
                   b, "Mô phỏng: hai chấm sáng đi từ B tới thấu kính theo hai tia đặc biệt rồi dừng — tia ló do em tự vẽ. "
                      "Hình đề không vẽ ảnh ở hình a, không vẽ thấu kính ở hình b.")
    # hình dữ kiện: mẫu ba tia đặc biệt (không theo số liệu đề)
    b = ""
    for k, (ox, ht, name) in enumerate(((110, True, "Thấu kính hội tụ"), (318, False, "Thấu kính phân kì"))):
        X, Y = mk(ox, 96, 1, 1)
        f = 38 if ht else -38
        d, h = (78, 30) if ht else (64, 30)
        dp = float(anh(f, d)); hp = h * abs(dp) / d
        b += lbl(ox, 20, name, BLUE, 14, "middle", "700") + axis(X(-100), X(98), Y(0), False) + lens(X(0), Y(44), Y(-44), ht)
        b += tick(X(-38), Y(0), "F" if ht else "F′", True, "currentColor", -4) + tick(X(38), Y(0), "F′" if ht else "F", True, "currentColor", 4)
        b += vat(X(-d), Y(0), Y(h))
        if ht:
            b += ray(X(-d), Y(h), X(0), Y(h)) + ray(X(0), Y(h), X(96), Y(h - 96 * h / 38), ORG, 2, 0.4)
            b += ray(X(-d), Y(h), X(96), Y(-96 * h / d), GRN, 2, 0.3)
            b += ray(X(-d), Y(h), X(0), Y(-hp), BLUE, 1.8, 0.4) + ray(X(0), Y(-hp), X(96), Y(-hp), BLUE, 1.8, 0.5)
            b += vat(X(dp), Y(0), Y(-hp), RED, False, 2.2)
        else:
            b += ray(X(-d), Y(h), X(0), Y(h)) + ray(X(0), Y(h), X(64), Y(h + 64 * h / 38), ORG, 2, 0.5) + ext(X(0), Y(h), X(-38), Y(0))
            b += ray(X(-d), Y(h), X(96), Y(-96 * h / d), GRN, 2, 0.3)
            b += ray(X(-d), Y(h), X(0), Y(hp), BLUE, 1.8, 0.5) + ray(X(0), Y(hp), X(96), Y(hp), BLUE, 1.8, 0.5) + ext(X(0), Y(hp), X(dp), Y(hp), BLUE)
            b += vat(X(dp), Y(0), Y(hp), RED, True, 2)
    b += lbl(12, 170, "Cam: song song trục → ló qua F′ (phân kì: kéo dài qua F′)", ORG, 14, "start", "400")
    b += lbl(12, 190, "Lục: qua quang tâm O → truyền thẳng", GRN, 14, "start", "400")
    b += lbl(12, 210, "Lam: qua F (phân kì: hướng tới F) → ló song song trục", BLUE, 14, "start", "400")
    return fig("c07-1-2", "0 0 420 222",
               "Hai hình mẫu ba tia đặc biệt: thấu kính hội tụ cho ảnh thật ngược chiều, thấu kính phân kì cho ảnh ảo nét đứt cùng chiều",
               b, "Hình mẫu quy tắc ba tia (không theo số liệu của đề). Ảnh ảo và đường kéo dài vẽ nét đứt.")


def fig1_giai_a():
    X, Y = mk(159, 72, 17, 17)
    return fig("c07-1-s1", "0 0 420 128", "Lời giải hình a: ba tia từ B gặp nhau tại B phẩy, ảnh thật ngược chiều cách thấu kính 12 ô",
               pan1a(X, Y, "giai"), "Ba tia từ B cùng đi qua B′; hạ vuông góc xuống trục được A′.")


def fig1_giai_b():
    X, Y = mk(331, 70, 11, 11)
    return fig("c07-1-s2", "0 0 420 104", "Lời giải hình b: quang tâm O là giao của BB phẩy với trục; đường kéo dài của tia ló qua B phẩy cắt trục tại F phẩy",
               pan1b(X, Y, "giai"), "Đường BB′ kéo dài cho O; đường kéo dài của tia ló IB′ cho F′ (nét đứt).")


# ───────────── Dạng 2 · công thức + tam giác đồng dạng ─────────────
def d2(kk):
    if kk == 0:
        DUR = 2.0
        b = ""
        for oy, ht, f, h, title in ((70, True, F2A, H2A, "a) Hội tụ, f = 20 cm"), (196, False, abs(F2B), H2B, "b) Phân kì, tiêu cự 30 cm")):
            X, Y = mk(214, oy, 5, 22)
            b += lbl(8, oy - (46 if ht else 62), title, BLUE, 14, "start", "700")   # b: vật cao hơn, đẩy tiêu đề lên khỏi nhãn B + axis(X(-40), X(40), Y(0)) + lens(X(0), Y(1.9), Y(-1.9), ht)
            b += tick(X(-f), Y(0), "F" if ht else "F′") + tick(X(f), Y(0), "F′" if ht else "F") + lbl(X(0) + 6, Y(0) + 17, "O", "currentColor", 14, "start", "700")
            b += vat(X(-D2A), Y(0), Y(h)) + lbl(X(-D2A) - 6, Y(h) - 2, "B", ORG, 14, "end", "700")
            b += seg(X(-D2A), Y(0) + 30, X(0), Y(0) + 30, "currentColor", 1.2) + lbl(X(-D2A / 2), Y(0) + 46, "15 cm", "currentColor", 14, "middle", "400")
            b += seg(X(-D2A), Y(0) + 25, X(-D2A), Y(0) + 35, "currentColor", 1.2) + seg(X(0), Y(0) + 25, X(0), Y(0) + 35, "currentColor", 1.2)
            bx, by = X(-D2A), Y(h)
            b += seg(bx, by, X(0), by, ORG, 1.4, "", 0.55) + seg(bx, by, X(0), Y(0), ORG, 1.4, "", 0.55)
            b += ball([(bx, by), (X(0), by)], 0, DUR) + ball([(bx, by), (X(0), Y(0))], 0, DUR)
            b += (f'<g opacity="0">{anim("opacity", "0;0;1", DUR + 0.4, "0;0.85;1")}'
                  f'{lbl(X(4), by - 6, "?", GRN, 16, "start", "700")}{lbl(X(4), Y(0) - 6, "?", GRN, 16, "start", "700")}</g>')
        return fig("c07-2-0", "0 0 420 262",
                   "Hai sơ đồ: thấu kính hội tụ tiêu cự 20 cm và thấu kính phân kì tiêu cự 30 cm, vật cách thấu kính 15 cm, hai chấm sáng đi từ đỉnh vật tới thấu kính",
                   b, "Mô phỏng: hai chấm sáng đi từ B tới thấu kính rồi dừng; em tự vẽ tia ló và ảnh. Trục ngang và trục đứng vẽ theo hai tỉ lệ khác nhau.")
    # hình mẫu chứng minh — trường hợp ẢNH THẬT (khác câu a)
    X, Y = mk(200, 70, 1, 1)
    f, d, h = 60, 100, 36
    dp = float(anh(f, d)); hp = h * dp / d
    b = (f'<polygon points="{X(0)},{Y(0)} {X(-d)},{Y(0)} {X(-d)},{Y(h)}" fill="{GRN}" fill-opacity="0.16" stroke="none"/>'
         f'<polygon points="{X(0)},{Y(0)} {X(dp)},{Y(0)} {X(dp)},{Y(-hp)}" fill="{GRN}" fill-opacity="0.16" stroke="none"/>'
         f'<polygon points="{X(f)},{Y(0)} {X(0)},{Y(0)} {X(0)},{Y(h)}" fill="{ORG}" fill-opacity="0.2" stroke="none"/>'
         f'<polygon points="{X(f)},{Y(0)} {X(dp)},{Y(0)} {X(dp)},{Y(-hp)}" fill="{ORG}" fill-opacity="0.2" stroke="none"/>')
    b += axis(X(-130), X(210), Y(0), False) + lens(X(0), Y(48), Y(-62), True)
    b += vat(X(-d), Y(0), Y(h)) + vat(X(dp), Y(0), Y(-hp), RED, False, 2.2)
    b += ray(X(-d), Y(h), X(0), Y(h)) + ray(X(0), Y(h), X(dp), Y(-hp), ORG, 2, 0.4)
    b += ray(X(-d), Y(h), X(dp), Y(-hp), GRN, 2, 0.3)
    b += tick(X(f), Y(0), "F′", False) + lbl(X(0) - 5, Y(0) + 17, "O", "currentColor", 14, "end", "700")
    b += lbl(X(-d), Y(0) + 17, "A", ORG, 14, "middle", "700") + lbl(X(-d) - 6, Y(h), "B", ORG, 14, "end", "700")
    b += lbl(X(0) + 6, Y(h) - 4, "I", "currentColor", 14, "start", "700")
    b += lbl(X(dp), Y(0) - 7, "A′", RED, 14, "middle", "700") + lbl(X(dp) + 6, Y(-hp) + 6, "B′", RED, 14, "start", "700")
    b += lbl(12, 156, "Lục: ΔOAB ∼ ΔOA′B′ (chung đỉnh O)", GRN, 14, "start", "700")
    b += lbl(12, 176, "Cam: ΔF′OI ∼ ΔF′A′B′ (chung đỉnh F′), OI = AB", ORG, 14, "start", "700")
    return fig("c07-2-2", "0 0 420 188",
               "Hình mẫu chứng minh công thức cho thấu kính hội tụ, ảnh thật: hai cặp tam giác đồng dạng tô màu, một cặp chung đỉnh O, một cặp chung đỉnh F phẩy",
               b, "Hình mẫu cách chứng minh, vẽ cho trường hợp ẢNH THẬT (không theo số liệu của đề). Câu a là ảnh khác loại: em tự chọn lại hai cặp tam giác trên hình của mình.")


def fig2_giai_a():
    X, Y = mk(282, 84, 4.3, 18)
    b = axis(X(-64), X(30), Y(0), False) + lens(X(0), Y(4.4), Y(-2.4), True)
    b += tick(X(-20), Y(0), "F") + tick(X(20), Y(0), "F′") + lbl(X(0) + 6, Y(0) + 17, "O", "currentColor", 14, "start", "700")
    b += vat(X(-D2A), Y(0), Y(H2A)) + lbl(X(-D2A), Y(0) + 17, "A", ORG, 14, "middle", "700") + lbl(X(-D2A) + 4, Y(H2A) - 6, "B", ORG, 14, "start", "700")
    b += ray(X(-D2A), Y(H2A), X(0), Y(H2A)) + ray(X(0), Y(H2A), X(30), Y(H2A - Fr(30, 20)), ORG, 2.2, 0.5)
    b += ext(X(0), Y(H2A), X(D2AP), Y(H2AP))
    b += ray(X(-D2A), Y(H2A), X(30), Y(-Fr(30, 15)), GRN, 2.2, 0.75) + ext(X(-D2A), Y(H2A), X(D2AP), Y(H2AP), GRN)
    b += vat(X(D2AP), Y(0), Y(H2AP), RED, True, 2.2) + lbl(X(D2AP), Y(0) + 17, "A′", RED, 14, "middle", "700")
    b += lbl(X(D2AP) + 7, Y(H2AP) + 4, "B′", RED, 14, "start", "700") + lbl(X(0) + 6, Y(H2A) - 5, "I", "currentColor", 14, "start", "700")
    return fig("c07-2-s1", "0 0 420 138", "Lời giải câu a: hai tia ló phân kì, đường kéo dài nét đứt cắt nhau tại B phẩy cùng phía vật, ảnh ảo cùng chiều lớn hơn vật",
               b, "Hai tia ló không cắt nhau; đường kéo dài của chúng (nét đứt) cắt nhau tại B′ — ảnh ảo. Trục đứng phóng to so với trục ngang.")


def fig2_giai_b():
    X, Y = mk(222, 70, 6, 20)
    b = axis(X(-34), X(30), Y(0), False) + lens(X(0), Y(3.1), Y(-3.1), False)
    b += tick(X(-30), Y(0), "F′") + tick(X(30), Y(0), "F") + lbl(X(0) + 6, Y(0) + 17, "O", "currentColor", 14, "start", "700")
    b += vat(X(-D2B), Y(0), Y(H2B)) + lbl(X(-D2B), Y(0) + 17, "A", ORG, 14, "middle", "700") + lbl(X(-D2B) - 6, Y(H2B) - 4, "B", ORG, 14, "end", "700")
    b += ray(X(-D2B), Y(H2B), X(0), Y(H2B), ORG, 2.2, 0.85) + ray(X(0), Y(H2B), X(30), Y(H2B + 30 * H2B / 30), ORG, 2.2, 0.5)
    b += ext(X(0), Y(H2B), X(-30), Y(0))
    b += ray(X(-D2B), Y(H2B), X(30), Y(-30 * H2B / D2B), GRN, 2.2, 0.75)
    b += vat(X(D2BP), Y(0), Y(H2BP), RED, True, 2.2) + lbl(X(D2BP), Y(0) + 17, "A′", RED, 14, "middle", "700")
    b += lbl(X(D2BP) + 3, Y(H2BP) - 8, "B′", RED, 14, "start", "700") + lbl(X(0) + 6, Y(H2B) - 5, "I", "currentColor", 14, "start", "700")
    return fig("c07-2-s2", "0 0 420 140", "Lời giải câu b: tia ló từ I có đường kéo dài qua F phẩy; giao với tia qua O là B phẩy, ảnh ảo nằm giữa F phẩy và thấu kính",
               b, "Ảnh qua thấu kính phân kì: B′ là giao của đường kéo dài F′I với tia BO. Trục đứng phóng to so với trục ngang.")


# ───────────── Dạng 3 · bài toán ngược nhiều trường hợp ─────────────
def d3(kk):
    X, Y = mk(300, 96, 7, 24)
    b = axis(X(-41), X(16), Y(0)) + lens(X(0), Y(2.2), Y(-2.2), True)
    b += tick(X(-12), Y(0), "F") + tick(X(12), Y(0), "F′") + tick(X(-24), Y(0), "2F") + lbl(X(0) + 6, Y(0) + 17, "O", "currentColor", 14, "start", "700")
    b += lbl(10, 22, "Thấu kính hội tụ, f = 12 cm", BLUE, 14, "start", "700")
    if kk == 0:
        DUR = 6.0
        x0 = X(-38)
        dx = X(-4) - x0
        b += (f'<g>{vat(x0, Y(0), Y(1.2))}{lbl(x0 - 6, Y(1.2) - 2, "B", ORG, 14, "end", "700")}'
              f'<animateTransform attributeName="transform" type="translate" values="0,0;{dx:.1f},0" dur="{DUR:.2f}s" begin="indefinite" fill="freeze"/></g>')
        b += lbl(X(-38), Y(0) + 40, "vật trượt dần lại gần thấu kính →", ORG, 14, "start", "400")
        b += (f'<g opacity="0">{anim("opacity", "0;0;1", DUR + 0.3, "0;0.9;1")}'
              f'{lbl(X(15), 46, "Ở đâu ảnh cao gấp 3 vật?", GRN, 14, "end", "700")}'
              f'{lbl(X(15), Y(0) + 62, "Ở đâu ảnh cách vật 50 cm?", GRN, 14, "end", "700")}</g>')
        return fig("c07-3-0", "0 0 420 166",
                   "Thấu kính hội tụ tiêu cự 12 cm, vật sáng trượt dọc trục chính từ xa lại gần thấu kính, cuối cùng hiện hai câu hỏi về vị trí vật",
                   b, "Mô phỏng: vật trượt từ xa lại sát thấu kính; ảnh không vẽ — vị trí cần tìm do em tính. Trục đứng phóng to so với trục ngang.")
    b += vat(X(-17), Y(0), Y(1.2)) + lbl(X(-17), Y(0) + 17, "A", ORG, 14, "middle", "700") + lbl(X(-17) - 6, Y(1.2) - 2, "B", ORG, 14, "end", "700")
    b += seg(X(-17), Y(0) + 32, X(0), Y(0) + 32, "currentColor", 1.2) + lbl(X(-8.5), Y(0) + 48, "d = ?", "currentColor", 14, "middle", "700")
    b += lbl(10, 150, "a) A′B′ = 3·AB", GRN, 14, "start", "700")
    b += lbl(10, 170, "b) khoảng cách vật – ảnh = 50 cm", GRN, 14, "start", "700")
    return fig("c07-3-2", "0 0 420 182", "Dữ kiện: thấu kính hội tụ tiêu cự 12 cm, vị trí vật d chưa biết, ảnh cao gấp 3 hoặc cách vật 50 cm",
               b, "Dữ kiện: chỉ biết f và một điều kiện về ảnh; vị trí vật vẽ tuỳ ý, không theo đáp số.")


BUILD = [d1, d2, d3]

# ═════════════ ĐỀ ═════════════
DANG = [
 dict(label="Dạng 1 · Dễ · Dựng ảnh trên giấy ô ly: cho vật tìm ảnh, cho vật và ảnh tìm thấu kính",
      topic=TOPIC_DUNG,
      problem_html=r"""<p>Chuẩn bị giấy ô ly, thước kẻ, bút chì. Ánh sáng truyền từ trái sang phải; vật sáng $AB$ vuông góc với trục chính, $A$ nằm trên trục chính.</p><ol type="a"><li>Hình a (mỗi ô $2\ \text{cm}$): thấu kính hội tụ tiêu cự $8\ \text{cm}$; vật $AB$ cao $2\ \text{cm}$, cách thấu kính $12\ \text{cm}$. Dựng ảnh $A'B'$ bằng hai tia đặc biệt, kiểm lại bằng tia thứ ba. Đọc trên lưới khoảng cách từ ảnh tới thấu kính và chiều cao ảnh; nêu tính chất của ảnh.</li><li>Hình b (mỗi ô $1\ \text{cm}$): $A'B'$ là ảnh của vật $AB$ qua một thấu kính chưa vẽ. $B$ cách trục chính $3\ \text{cm}$; $B'$ cách trục chính $1\ \text{cm}$, cùng phía trục với $B$; $A'$ ở bên phải $A$, $AA'=16\ \text{cm}$. Bằng cách vẽ, cho biết thấu kính loại gì, xác định quang tâm $O$, tiêu điểm ảnh $F'$, rồi tính tiêu cự $f$ (có dấu theo quy ước).</li></ol>"""),
 dict(label="Dạng 2 · Trung bình · Công thức thấu kính, quy ước dấu và chứng minh bằng tam giác đồng dạng",
      topic=TOPIC_CT,
      problem_html=r"""<p>Vật sáng $AB$ đặt vuông góc với trục chính của thấu kính, $A$ nằm trên trục chính. Dùng quy ước: $d'\gt0$ ảnh thật, $d'\lt0$ ảnh ảo; $f\gt0$ thấu kính hội tụ, $f\lt0$ thấu kính phân kì.</p><ol type="a"><li>Thấu kính hội tụ tiêu cự $20\ \text{cm}$; $AB$ cao $1\ \text{cm}$, cách thấu kính $15\ \text{cm}$. Dựng ảnh $A'B'$ (không cần đúng tỉ lệ) và nêu tính chất ảnh. Dùng hai cặp tam giác đồng dạng trên hình để tìm khoảng cách từ ảnh tới thấu kính; tìm chiều cao ảnh và khoảng cách giữa vật và ảnh. Kiểm lại bằng công thức $\dfrac1f=\dfrac1d+\dfrac1{d'}$.</li><li>Thay bằng thấu kính phân kì tiêu cự $30\ \text{cm}$ và một vật sáng khác cao $1{,}5\ \text{cm}$, vẫn cách thấu kính $15\ \text{cm}$. Tìm $d'$ (có dấu), chiều cao ảnh và khoảng cách giữa vật và ảnh.</li></ol>"""),
 dict(label="Dạng 3 · Trung bình · Bài toán ngược nhiều trường hợp: ảnh gấp n lần vật, ảnh cách vật một khoảng cho trước",
      topic=TOPIC_CT,
      problem_html=r"""<p>Một thấu kính hội tụ có tiêu cự $12\ \text{cm}$. Vật sáng $AB$ đặt vuông góc với trục chính, $A$ nằm trên trục chính.</p><ol type="a"><li>Tìm vị trí đặt vật để ảnh cao gấp $3$ lần vật. Với mỗi vị trí tìm được, ảnh cách vật bao nhiêu?</li><li>Tìm mọi vị trí đặt vật để ảnh cách vật $50\ \text{cm}$. Có bao nhiêu vị trí như vậy?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ ═════════════
ANALYSIS = [
 # Dạng 1
 [(r'"Ánh sáng truyền từ trái sang phải; vật sáng $AB$ vuông góc với trục chính"', r"Vật thật ở bên trái thấu kính",
   r"⚠ quy tắc ba tia chỉ dùng cho thấu kính mỏng, tia gần trục chính<br>⚠ mỗi hình một tỉ lệ ô: đổi số ô ra cm đúng tỉ lệ của hình đó"),
  (r'"Hình a (mỗi ô $2\ \text{cm}$): thấu kính hội tụ tiêu cự $8\ \text{cm}$"', r"$f=8\ \text{cm}=4$ ô",
   r"$F$ và $F'$ cách $O$ bằng $|f|$, ở hai bên thấu kính"),
  (r'"$AB$ cao $2\ \text{cm}$, cách thấu kính $12\ \text{cm}$"', r"$h=1$ ô; $d=6$ ô", r"Vật ở trong hay ngoài khoảng $OF$?"),
  (r'''"Dựng ảnh $A'B'$ bằng hai tia đặc biệt, kiểm lại bằng tia thứ ba"''', r"Cần $B'$ rồi $A'$",
   r"Tia song song trục → ló qua $F'$<br>Tia qua $O$ → truyền thẳng<br>Tia qua $F$ → ló song song trục"),
  (r'"Đọc trên lưới khoảng cách từ ảnh tới thấu kính và chiều cao ảnh"', r"Cần $OA'$, $A'B'$", r"Đếm số ô rồi đổi ra cm"),
  (r'''"$B$ cách trục chính $3\ \text{cm}$; $B'$ cách trục chính $1\ \text{cm}$, cùng phía trục với $B$"''', r"$h=3\ \text{cm}$; $h'=1\ \text{cm}$",
   r"Ảnh cùng chiều hay ngược chiều vật? Lớn hơn hay nhỏ hơn vật?"),
  (r'''"$A'$ ở bên phải $A$, $AA'=16\ \text{cm}$"''', r"$AA'=16\ \text{cm}$", r"Đây là khoảng cách vật – ảnh, chưa phải $d$ hay $d'$"),
  (r'''"cho biết thấu kính loại gì, xác định quang tâm $O$, tiêu điểm ảnh $F'$"''', r"Cần loại thấu kính, $O$, $F'$",
   r"Tia nào đi thẳng qua $O$?<br>Tia nào cho biết vị trí $F'$?"),
  (r'"tính tiêu cự $f$ (có dấu theo quy ước)"', r"Cần $f$", r"$f\gt0$: hội tụ; $f\lt0$: phân kì")],
 # Dạng 2
 [(r'''"Dùng quy ước: $d'\gt0$ ảnh thật, $d'\lt0$ ảnh ảo; $f\gt0$ … $f\lt0$ …"''', r"Quy ước dấu",
   r"⚠ $\dfrac1f=\dfrac1d+\dfrac1{d'}$ chỉ đúng khi $f$ và $d'$ mang dấu theo quy ước này<br>⚠ vật thật: $d\gt0$"),
  (r'"Thấu kính hội tụ tiêu cự $20\ \text{cm}$; $AB$ cao $1\ \text{cm}$, cách thấu kính $15\ \text{cm}$"',
   r"$f=20\ \text{cm}$; $h=1\ \text{cm}$; $d=15\ \text{cm}$", r"So $d$ với $f$: vật ở trong hay ngoài khoảng $OF$?"),
  (r'''"Dựng ảnh $A'B'$ (không cần đúng tỉ lệ) và nêu tính chất ảnh"''', r"—", r"Tia song song trục và tia qua $O$<br>Hai tia ló cắt nhau, hay đường kéo dài cắt nhau?"),
  (r'"Dùng hai cặp tam giác đồng dạng trên hình"', r"Cần $|d'|$", r"Một cặp chung đỉnh $O$, một cặp chung đỉnh $F'$<br>$OI=AB$"),
  (r'"tìm chiều cao ảnh và khoảng cách giữa vật và ảnh"', r"Cần $h'$ và $L$", r"$\dfrac{h'}{h}=\dfrac{|d'|}{d}$<br>Ảnh ở cùng phía hay khác phía vật?"),
  (r'"Thay bằng thấu kính phân kì tiêu cự $30\ \text{cm}$"', r"$f=-30\ \text{cm}$ (theo quy ước)", r"Ảnh của vật thật qua thấu kính phân kì có tính chất gì?"),
  (r'"vật sáng khác cao $1{,}5\ \text{cm}$, vẫn cách thấu kính $15\ \text{cm}$"', r"$h=1{,}5\ \text{cm}$; $d=15\ \text{cm}$", r"$d'=\dfrac{df}{d-f}$"),
  (r'''"Tìm $d'$ (có dấu), chiều cao ảnh và khoảng cách giữa vật và ảnh"''', r"Cần $d'$, $h'$, $L$", r"Ảnh nằm gần thấu kính hơn hay xa hơn vật?")],
 # Dạng 3
 [(r'"Một thấu kính hội tụ có tiêu cự $12\ \text{cm}$"', r"$f=12\ \text{cm}$",
   r"⚠ $d$, $d'$, $f$ mang dấu theo quy ước mới dùng được $\dfrac1f=\dfrac1d+\dfrac1{d'}$<br>⚠ vật thật: chỉ nhận nghiệm $d\gt0$"),
  (r'"Vật sáng $AB$ đặt vuông góc với trục chính"', r"Ẩn: $d$", r"$d'=\dfrac{df}{d-f}$"),
  (r'"ảnh cao gấp $3$ lần vật"', r"$\dfrac{|d'|}{d}=3$", r"$d'$ mang dấu gì?"),
  (r'"ảnh cách vật bao nhiêu?"', r"Cần $L$", r"Ảnh và vật ở cùng phía hay khác phía thấu kính?"),
  (r'"Tìm mọi vị trí đặt vật để ảnh cách vật $50\ \text{cm}$"', r"$L=50\ \text{cm}$", r"Viết $L$ theo $d$ và $d'$ rồi thế $d'=\dfrac{df}{d-f}$"),
  (r'"Có bao nhiêu vị trí như vậy?"', r"Cần số nghiệm hợp lệ", r"Mỗi nghiệm: $d\gt0$? Dấu của $d'$ có khớp loại ảnh đã giả sử?")],
]

# ═════════════ LỜI GIẢI ═════════════
R1 = [r"<strong>Khái niệm:</strong> trục chính, quang tâm $O$, tiêu điểm vật $F$, tiêu điểm ảnh $F'$, $OF=OF'=|f|$. Hội tụ: $F'$ khác phía vật; phân kì: $F'$ cùng phía vật.",
      r"<strong>Quy tắc ba tia:</strong> song song trục → ló qua $F'$ (phân kì: đường kéo dài qua $F'$); qua $O$ → truyền thẳng; qua $F$ (phân kì: hướng tới $F$) → ló song song trục.",
      r"<strong>Dựng ảnh:</strong> $B'$ là giao của hai tia ló (hoặc hai đường kéo dài); hạ vuông góc xuống trục được $A'$.",
      r"<strong>Điều kiện:</strong> thấu kính mỏng, tia gần trục; đếm ô đúng tỉ lệ của từng hình."]
R2 = [r"<strong>Quy ước:</strong> $d\gt0$; $d'\gt0$ ảnh thật, $d'\lt0$ ảnh ảo; $f\gt0$ hội tụ, $f\lt0$ phân kì.",
      r"<strong>Công thức:</strong> $\dfrac1f=\dfrac1d+\dfrac1{d'}$, suy ra $d'=\dfrac{df}{d-f}$; chiều cao $\dfrac{h'}{h}=\dfrac{|d'|}{d}$.",
      r"<strong>Chứng minh:</strong> $\triangle OAB\sim\triangle OA'B'$ (chung đỉnh $O$) và $\triangle F'OI\sim\triangle F'A'B'$ (chung đỉnh $F'$), với $OI=AB$.",
      r"<strong>Khoảng cách vật – ảnh:</strong> ảnh thật $L=d+d'$; ảnh ảo $L=\big|\,d-|d'|\,\big|$.",
      r"<strong>Điều kiện:</strong> thấu kính mỏng, vật vuông góc trục chính, $A$ trên trục."]
R3 = [r"<strong>Quy ước:</strong> $d\gt0$; $d'\gt0$ ảnh thật (khác phía vật), $d'\lt0$ ảnh ảo (cùng phía vật); hội tụ $f\gt0$.",
      r"<strong>Công thức:</strong> $\dfrac1f=\dfrac1d+\dfrac1{d'}$; ảnh cao gấp $n$ lần vật: $|d'|=nd$.",
      r"<strong>Hai loại ảnh của thấu kính hội tụ:</strong> $d\gt f$ cho ảnh thật; $d\lt f$ cho ảnh ảo, lớn hơn vật, xa thấu kính hơn vật.",
      r"<strong>Khoảng cách vật – ảnh:</strong> ảnh thật $L=d+d'$; ảnh ảo $L=|d'|-d$.",
      r"<strong>Điều kiện:</strong> đề không nói loại ảnh thì xét đủ hai loại; loại nghiệm $d\le0$."]


def with_figs(html, figs):
    for k, v in figs.items():
        html = html.replace(f"<p>@@{k}@@</p>", v)
    assert "@@" not in html
    return html


SOLS = [
 with_figs(sol(R1, [
  ("Dựng hai tia từ B (hình a)", [P(r"Vẽ trục chính, thấu kính tại $O$; đánh dấu $F$, $F'$ cách $O$ đúng $4$ ô ($8\ \text{cm}$) ở hai bên; dựng $AB$ cao $1$ ô, cách $O$ là $6$ ô."),
     P(r"Tia $BI$ song song trục chính → tia ló qua $F'$. Tia $BO$ qua quang tâm → truyền thẳng. Hai tia ló cắt nhau tại $B'$; hạ vuông góc được $A'$."),
     P("@@H1@@"),
     P(r"Đếm trên lưới: $A'$ cách $O$ là $12$ ô."), M(r"OA'=12\cdot2\ \text{cm}"), A(r"OA'=24\ \text{cm}")]),
  ("Chiều cao và tính chất ảnh", [P(r"$B'$ nằm dưới trục chính $2$ ô:"), M(r"A'B'=2\cdot2\ \text{cm}"), A(r"h'=4\ \text{cm}"),
     P(r"Ảnh ở khác phía vật, do chính tia ló cắt nhau tạo nên: <strong>ảnh thật, ngược chiều, cao gấp $2$ lần vật</strong>.")]),
  ("Kiểm bằng tia thứ ba", [P(r"Tia $BF$ qua tiêu điểm vật gặp thấu kính tại $K$ rồi ló song song trục. Tia ló này cũng đi qua $B'$ ✓ (hình trên, màu lam)."),
     P(r"Tính nhanh: $d'=\dfrac{df}{d-f}=\dfrac{12\cdot8}{12-8}=24\ \text{cm}$ ✓, khớp số đọc trên lưới.")]),
  ("Loại thấu kính (hình b)", [P(r"$B$ và $B'$ cùng phía trục chính: ảnh <strong>cùng chiều</strong> với vật. Vật thật cho ảnh cùng chiều thì đó là ảnh ảo."),
     P(r"Ảnh ảo nhỏ hơn vật ($1\ \text{cm}\lt3\ \text{cm}$). Ảnh ảo của thấu kính hội tụ luôn lớn hơn vật."), A(r"T:Thấu kính <strong>phân kì</strong>.")]),
  ("Tìm quang tâm O", [P(r"Tia qua quang tâm truyền thẳng nên $B$, $B'$, $O$ thẳng hàng: $O$ là giao của đường $BB'$ kéo dài với trục chính."),
     P(r"Đếm ô: từ $B$ sang $B'$ đường thẳng đi ngang $16$ ô thì hạ $2$ ô; còn $1$ ô nữa mới tới trục nên đi ngang thêm $8$ ô."),
     P("@@H2@@"),
     M(r"OA=16+8"), A(r"d=OA=24\ \text{cm}\ \ (OA'=8\ \text{cm})")]),
  ("Tìm F′ và tiêu cự", [P(r"Vẽ thấu kính phân kì tại $O$. Tia từ $B$ song song trục gặp thấu kính tại $I$, $OI=3$ ô. Tia ló có đường kéo dài đi qua $B'$."),
     P(r"Kéo dài $IB'$ tới trục chính: từ $I$ đi ngang $8$ ô hạ $2$ ô; hạ thêm $1$ ô nữa thì đi ngang thêm $4$ ô. Giao điểm là $F'$, cùng phía vật."),
     M(r"OF'=8+4=12\ \text{cm}"), A(r"f=-12\ \text{cm}")]),
  ("Kiểm tra", [P(r"Hình b theo công thức: $\dfrac1d+\dfrac1{d'}=\dfrac1{24}+\dfrac1{-8}=-\dfrac2{24}=-\dfrac1{12}=\dfrac1f$ ✓."),
     P(r"Tỉ số chiều cao: $\dfrac{|d'|}{d}=\dfrac8{24}=\dfrac13=\dfrac{h'}{h}$ ✓; ảnh ảo nằm trong khoảng $OF'$ ($8\lt12$) ✓."),
     P(r"Hình a: $\dfrac{h'}{h}=\dfrac{24}{12}=2$ ✓.")])],
  [r"a) Ảnh thật, ngược chiều; cách thấu kính $24\ \text{cm}$; cao $4\ \text{cm}$", r"b) Thấu kính phân kì; $O$ cách $A$ là $24\ \text{cm}$; $F'$ cùng phía vật; $f=-12\ \text{cm}$"],
  r"Nhận dạng: thấy <strong>giấy ô ly, dựng ảnh</strong> hoặc <strong>cho vật và ảnh, tìm thấu kính</strong> → dùng tia qua $O$ (thẳng) và tia song song trục (qua $F'$)."),
  dict(H1=fig1_giai_a(), H2=fig1_giai_b())),
 with_figs(sol(R2, [
  ("Dựng ảnh và nhận tính chất (câu a)", [P(r"$d=15\ \text{cm}\lt f=20\ \text{cm}$: vật nằm trong khoảng $OF$."),
     P(r"Tia $BI$ song song trục ló qua $F'$; tia $BO$ truyền thẳng. Hai tia ló đi ra xa nhau, chỉ đường kéo dài (nét đứt) cắt nhau tại $B'$ cùng phía vật."),
     P("@@H1@@"),
     A(r"T:Ảnh <strong>ảo, cùng chiều, lớn hơn vật</strong>.")]),
  ("Hai cặp tam giác đồng dạng", [P(r"$\triangle OAB\sim\triangle OA'B'$ (chung đỉnh $O$, $AB\parallel A'B'$):"), M(r"\frac{h'}{h}=\frac{OA'}{OA}=\frac{|d'|}{d}"),
     P(r"$\triangle F'OI\sim\triangle F'A'B'$ (chung đỉnh $F'$, $OI\parallel A'B'$, $OI=AB$). Ảnh ảo ở cùng phía vật nên $F'A'=F'O+OA'$:"),
     M(r"\frac{h'}{h}=\frac{F'A'}{F'O}=\frac{f+|d'|}{f}"), A(r"\frac{|d'|}{d}=\frac{f+|d'|}{f}")]),
  ("Giải tìm vị trí ảnh", [M(r"|d'|\,f=d\,f+d\,|d'|"), M(r"|d'|=\frac{df}{f-d}=\frac{15\cdot20}{20-15}"), A(r"|d'|=60\ \text{cm}\ \Rightarrow\ d'=-60\ \text{cm}"),
     P(r"Theo công thức: $\dfrac1{d'}=\dfrac1{20}-\dfrac1{15}=-\dfrac1{60}$ ✓, dấu âm đúng là ảnh ảo.")]),
  ("Chiều cao ảnh", [M(r"h'=h\cdot\frac{|d'|}{d}=1\cdot\frac{60}{15}"), A(r"h'=4\ \text{cm}")]),
  ("Khoảng cách vật – ảnh (câu a)", [P(r"Ảnh ảo cùng phía vật và xa thấu kính hơn vật:"), M(r"L=|d'|-d=60-15"), A(r"L=45\ \text{cm}")]),
  ("Ảnh qua thấu kính phân kì (câu b)", [P(r"Thấu kính phân kì: $f=-30\ \text{cm}$."), M(r"d'=\frac{df}{d-f}=\frac{15\cdot(-30)}{15-(-30)}=\frac{-450}{45}"), A(r"d'=-10\ \text{cm}")]),
  ("Khoảng cách vật – ảnh (câu b)", [M(r"h'=1{,}5\cdot\frac{10}{15}=1\ \text{cm}"),
     P(r"Ảnh ảo cùng phía vật, gần thấu kính hơn vật:"), M(r"L=d-|d'|=15-10"), A(r"L=5\ \text{cm}"),
     P("@@H2@@")]),
  ("Kiểm tra", [P(r"Câu a: $\dfrac1{15}+\dfrac1{-60}=\dfrac{4-1}{60}=\dfrac1{20}$ ✓; ảnh ảo của thấu kính hội tụ có $|d'|\gt d$ ($60\gt15$) ✓."),
     P(r"Câu b bằng tam giác: $\triangle F'OI\sim\triangle F'A'B'$ với $F'A'=|f|-|d'|$ cho $\dfrac{h'}{h}=\dfrac{30-10}{30}=\dfrac23$, khớp $\dfrac{|d'|}{d}=\dfrac{10}{15}=\dfrac23$ ✓."),
     P(r"Ảnh của thấu kính phân kì: $|d'|\lt|f|$ và $|d'|\lt d$ ✓.")])],
  [r"a) Ảnh ảo, cùng chiều; $d'=-60\ \text{cm}$; $h'=4\ \text{cm}$; ảnh cách vật $45\ \text{cm}$", r"b) $d'=-10\ \text{cm}$; $h'=1\ \text{cm}$; ảnh cách vật $5\ \text{cm}$"],
  r"Nhận dạng: thấy <strong>tìm vị trí, chiều cao ảnh</strong> hoặc <strong>chứng minh công thức</strong> → hai cặp tam giác đồng dạng, hoặc $\frac1f=\frac1d+\frac1{d'}$ có dấu."),
  dict(H1=fig2_giai_a(), H2=fig2_giai_b())),
 sol(R3, [
  ("Ảnh thật cao gấp 3 vật", [P(r"Ảnh thật: $d'=3d$."), M(r"\frac1{12}=\frac1d+\frac1{3d}=\frac4{3d}"), A(r"d=16\ \text{cm},\ d'=48\ \text{cm}"),
     P(r"$d=16\gt f$ ✓ đúng vùng cho ảnh thật.")]),
  ("Ảnh ảo cao gấp 3 vật", [P(r"Thấu kính hội tụ còn cho ảnh ảo lớn hơn vật khi $d\lt f$. Ảnh ảo: $d'=-3d$."),
     M(r"\frac1{12}=\frac1d-\frac1{3d}=\frac2{3d}"), A(r"d=8\ \text{cm},\ d'=-24\ \text{cm}"), P(r"$d=8\lt f$ ✓ đúng vùng cho ảnh ảo.")]),
  ("Khoảng cách vật – ảnh câu a", [M(r"\text{Ảnh thật: } L=d+d'=16+48=64\ \text{cm}"), P(r"Ảnh ảo cùng phía vật, xa thấu kính hơn vật:"),
     M(r"L=|d'|-d=24-8"), A(r"L=16\ \text{cm}")]),
  ("Ảnh thật cách vật 50 cm", [P(r"$d+d'=50$ với $d'=\dfrac{12d}{d-12}$:"), M(r"d+\frac{12d}{d-12}=50\ \Rightarrow\ d^2-50d+600=0"),
     M(r"\Delta=50^2-4\cdot600=100"), A(r"d=20\ \text{cm}\ (d'=30)\ \text{hoặc}\ d=30\ \text{cm}\ (d'=20)")]),
  ("Ảnh ảo cách vật 50 cm", [P(r"Ảnh ảo: $|d'|-d=50$, tức $d'=-(d+50)$:"), M(r"\frac1{12}=\frac1d-\frac1{d+50}=\frac{50}{d(d+50)}"),
     M(r"d^2+50d-600=0,\quad \Delta=50^2+4\cdot600=4900"), M(r"d=\frac{-50\pm70}{2}"), A(r"d=10\ \text{cm}\ (d'=-60\ \text{cm});\ \text{loại}\ d=-60"),
     P(r"$d=10\lt f$ ✓ đúng vùng cho ảnh ảo.")]),
  ("Kết luận số vị trí", [P(r"Hai vị trí cho ảnh thật ($d=20$ và $d=30\ \text{cm}$) và một vị trí cho ảnh ảo ($d=10\ \text{cm}$)."), A(r"T:Có <strong>3 vị trí</strong> đặt vật.")]),
  ("Kiểm tra", [P(r"$d=20$: $d'=\dfrac{240}{8}=30$, $L=50$ ✓. $d=30$: $d'=\dfrac{360}{18}=20$, $L=50$ ✓ (hai vị trí đối xứng: $d$ của vị trí này bằng $d'$ của vị trí kia)."),
     P(r"$d=10$: $d'=\dfrac{120}{-2}=-60$, $L=60-10=50$ ✓."),
     P(r"Ảnh thật cách vật $50\ \text{cm}\ge4f=48\ \text{cm}$ nên phương trình ảnh thật có nghiệm ✓. Câu a: $\dfrac{48}{16}=\dfrac{24}{8}=3$ ✓.")])],
  [r"a) Ảnh thật: $d=16\ \text{cm}$, ảnh cách vật $64\ \text{cm}$", r"a) Ảnh ảo: $d=8\ \text{cm}$, ảnh cách vật $16\ \text{cm}$",
   r"b) $d=20\ \text{cm}$ hoặc $30\ \text{cm}$ (ảnh thật); $d=10\ \text{cm}$ (ảnh ảo): $3$ vị trí"],
  r"Nhận dạng: thấy <strong>ảnh cao gấp n lần</strong> hoặc <strong>ảnh cách vật L</strong> mà đề không nói loại ảnh → xét cả ảnh thật lẫn ảnh ảo."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 1 ──
 dict(nhan_dang=r"Thấy <b>giấy ô ly, dựng ảnh</b> hoặc <b>cho vật và ảnh, tìm thấu kính</b> → dùng tia qua $O$ và tia song song trục.",
  cap_do=1, fading="mo_het", go_roi={"buoc_hay_sai": 5}, buoc=[
  buoc("Dựng hai tia từ B (hình a)", "Đọc trên lưới: ảnh A′B′ cách thấu kính bao nhiêu cm?", 24, "cm", 1,
       loi=r"Đếm được số ô nhưng quên nhân với $2\ \text{cm}$ mỗi ô; hoặc cho tia song song trục ló qua $F$ (phía vật) thay vì $F'$."),
  buoc("Chiều cao và tính chất ảnh", "Ảnh A′B′ cao bao nhiêu cm?", 4, "cm", 0.5,
       loi=r"Đọc chiều cao theo số ô mà không đổi ra cm, hoặc ghi chiều cao âm vì ảnh nằm dưới trục (chiều cao là độ dài, luôn dương).",
       ke=[(r"Đếm số ô từ $B'$ tới trục chính rồi đổi ra cm", True),
           (r"Lấy chiều cao ảnh bằng chiều cao vật vì tia qua $O$ truyền thẳng", r"Tia qua $O$ không song song trục; ảnh chỉ bằng vật khi vật đặt cách thấu kính $2f$."),
           (r"Tính $h'=h\cdot\dfrac{f}{d}$", r"Tỉ số chiều cao là $\dfrac{|d'|}{d}$, không phải $\dfrac fd$.")]),
  buoc("Kiểm bằng tia thứ ba"),
  buoc("Loại thấu kính (hình b)", "Thấu kính ở hình b là loại nào?",
       lua_chon=[(r"Phân kì: ảnh cùng chiều (ảnh ảo) mà nhỏ hơn vật", True),
                 (r"Hội tụ: thấu kính hội tụ cũng cho ảnh ảo cùng chiều", r"Ảnh ảo của thấu kính hội tụ luôn lớn hơn vật; ở đây ảnh nhỏ hơn vật."),
                 (r"Chưa biết được khi chưa vẽ thấu kính", r"Chiều và độ lớn của ảnh so với vật đã đủ để nhận loại thấu kính.")],
       loi=r"Thấy ảnh cùng chiều liền nghĩ tới kính lúp (hội tụ), quên so độ lớn của ảnh với vật.",
       ke=[(r"Dựa vào chiều và độ lớn của ảnh so với vật để nhận loại thấu kính", True),
           (r"Vẽ ngay tia song song trục ló qua $F'$ ở phía bên phải", r"Chưa biết thấu kính ở đâu, loại gì, nên chưa biết $F'$ ở phía nào."),
           (r"Thế $d=16\ \text{cm}$ vào công thức thấu kính", r"$16\ \text{cm}$ là khoảng cách vật – ảnh $AA'$, không phải khoảng cách từ vật tới thấu kính.")]),
  buoc("Tìm quang tâm O", "Quang tâm O cách A bao nhiêu cm?", 24, "cm", 1,
       loi=r"Đặt $O$ ở trung điểm $AA'$ hoặc ngay dưới $B'$; tia qua quang tâm truyền thẳng nên $O$ nằm trên đường $BB'$ kéo dài.",
       ke=[(r"Kéo dài đường $BB'$ cắt trục chính: giao điểm là $O$", True),
           (r"Lấy $O$ là trung điểm của $AA'$", r"Không có quy tắc trung điểm; điểm vật, điểm ảnh và quang tâm thẳng hàng."),
           (r"Lấy $O$ ngay dưới $B'$ (trùng $A'$)", r"Ảnh không nằm trên thấu kính; $O$ là giao của đường $BB'$ với trục.")]),
  buoc("Tìm F′ và tiêu cự", "Tiêu cự f của thấu kính (có dấu theo quy ước) bằng bao nhiêu cm?", -12, "cm", 0.5,
       loi=r"Kéo dài tia ló về phía sau thấu kính thay vì về phía vật, hoặc ghi $f$ dương cho thấu kính phân kì.",
       ke=[(r"Vẽ tia từ $B$ song song trục tới $I$; kéo dài đường $IB'$ cắt trục chính tại $F'$", True),
           (r"Vẽ thêm tia từ $B$ qua $O$", r"Tia này chỉ cho lại đường $BB'$ đã dùng để tìm $O$, không cho thêm điểm nào trên trục."),
           (r"Lấy $OF'$ bằng $OA'$", r"$A'$ là vị trí ảnh, không phải tiêu điểm; ảnh chỉ nằm ở $F'$ khi vật ở rất xa.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 2 ──
 dict(nhan_dang=r"Thấy <b>tìm vị trí, chiều cao ảnh</b> hoặc <b>chứng minh công thức</b> → hai cặp tam giác đồng dạng, hoặc $\frac1f=\frac1d+\frac1{d'}$ có dấu.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Dựng ảnh và nhận tính chất (câu a)", "Ảnh A′B′ ở câu a có tính chất gì?",
       lua_chon=[(r"Ảnh ảo, cùng chiều, lớn hơn vật", True),
                 (r"Ảnh thật, ngược chiều, lớn hơn vật", r"Vật nằm trong khoảng $OF$: hai tia ló đi ra xa nhau, không cắt nhau nên không có ảnh thật."),
                 (r"Ảnh ảo, cùng chiều, nhỏ hơn vật", r"Ảnh ảo nhỏ hơn vật là ảnh của thấu kính phân kì; ảnh ảo của thấu kính hội tụ lớn hơn vật.")],
       loi=r"Quen hình ảnh thật nên vẽ hai tia ló cắt nhau sau thấu kính, không so $d$ với $f$ trước."),
  buoc("Hai cặp tam giác đồng dạng", "Phương trình nào đúng cho trường hợp ảnh ảo này?",
       lua_chon=[(r"$\dfrac{|d'|}{d}=\dfrac{f+|d'|}{f}$", True),
                 (r"$\dfrac{|d'|}{d}=\dfrac{|d'|-f}{f}$", r"Đó là phương trình của ảnh thật, khi $A'$ nằm sau $F'$; ảnh ảo ở cùng phía vật nên $F'A'=f+|d'|$."),
                 (r"$\dfrac{|d'|}{d}=\dfrac{f}{f+|d'|}$", r"Vế phải bị đảo ngược: cả hai vế phải cùng bằng $\dfrac{A'B'}{AB}$.")],
       loi=r"Chép nguyên phương trình của trường hợp ảnh thật, không xét lại $F'A'$ bằng tổng hay hiệu.",
       ke=[(r"Viết $\dfrac{h'}{h}$ theo hai cặp tam giác, một cặp chung đỉnh $O$, một cặp chung đỉnh $F'$", True),
           (r"Thế số ngay vào $\dfrac1f=\dfrac1d+\dfrac1{d'}$ với $d'\gt0$", r"Đề yêu cầu tìm bằng tam giác đồng dạng; hơn nữa ảnh ảo thì $d'\lt0$."),
           (r"Dùng cặp tam giác chung đỉnh $F$ (tiêu điểm vật)", r"Tia song song trục ló qua $F'$, nên cặp tam giác chứa $I$ và $A'B'$ có đỉnh chung là $F'$.")]),
  buoc("Giải tìm vị trí ảnh", "Ảnh cách thấu kính bao nhiêu cm?", 60, "cm", 0.5,
       loi=r"Chuyển vế sai dấu khi gom các số hạng chứa $|d'|$, ra mẫu số $f+d$ thay vì $f-d$.",
       ke=[(r"Nhân chéo rồi gom các số hạng chứa $|d'|$ về một vế", True),
           (r"Dùng $|d'|=\dfrac{df}{d+f}$", r"Đó là kết quả khi chuyển vế sai dấu; nhân chéo cẩn thận sẽ ra mẫu $f-d$."),
           (r"Lấy $|d'|=f-d$", r"Không có phép trừ đơn giản như vậy; phải giải phương trình tỉ lệ.")]),
  buoc("Chiều cao ảnh", "Ảnh A′B′ cao bao nhiêu cm?", 4, "cm", 0.1,
       loi=r"Lấy tỉ số ngược $\dfrac{d}{|d'|}$ nên ra ảnh nhỏ hơn vật, trái với tính chất đã nhận ở bước 1.",
       ke=[(r"$h'=h\cdot\dfrac{|d'|}{d}$", True),
           (r"$h'=h\cdot\dfrac{d}{|d'|}$", r"Tỉ số bị đảo ngược; ảnh ảo của thấu kính hội tụ phải lớn hơn vật."),
           (r"$h'=h\cdot\dfrac{f}{d}$", r"$\dfrac fd$ không phải tỉ số chiều cao; tỉ số đó là $\dfrac{|d'|}{d}$.")]),
  buoc("Khoảng cách vật – ảnh (câu a)", "Ảnh cách vật bao nhiêu cm?", 45, "cm", 0.5,
       loi=r"Cộng $d+|d'|$ như với ảnh thật, quên ảnh ảo nằm cùng phía với vật.",
       ke=[(r"Ảnh cùng phía vật: lấy hiệu $|d'|-d$", True),
           (r"Cộng $d+|d'|$", r"Chỉ cộng khi ảnh và vật ở hai phía thấu kính (ảnh thật)."),
           (r"Lấy $|d'|-f$", r"Hiệu đó là khoảng cách từ ảnh tới $F$, không phải tới vật.")]),
  buoc("Ảnh qua thấu kính phân kì (câu b)", "d′ (có dấu) bằng bao nhiêu cm?", -10, "cm", 0.3,
       loi=r"Thế $f=+30\ \text{cm}$, quên thấu kính phân kì có $f\lt0$.",
       ke=[(r"Thế $f=-30\ \text{cm}$ vào $d'=\dfrac{df}{d-f}$", True),
           (r"Thế $f=+30\ \text{cm}$ vào $d'=\dfrac{df}{d-f}$", r"Thấu kính phân kì có $f\lt0$; thế $f$ dương là đang tính cho thấu kính hội tụ."),
           (r"Dùng $\dfrac1{d'}=\dfrac1f+\dfrac1d$", r"Chuyển vế sai dấu: đúng là $\dfrac1{d'}=\dfrac1f-\dfrac1d$.")]),
  buoc("Khoảng cách vật – ảnh (câu b)", "Ảnh cách vật bao nhiêu cm?", 5, "cm", 0.2,
       loi=r"Cộng $d+|d'|$, hoặc lấy khoảng cách từ ảnh tới tiêu điểm thay cho khoảng cách tới vật.",
       ke=[(r"Ảnh ảo cùng phía vật, gần thấu kính hơn vật: lấy $d-|d'|$", True),
           (r"Cộng $d+|d'|$", r"Ảnh ảo nằm cùng phía với vật nên khoảng cách là hiệu, không phải tổng."),
           (r"Lấy $|f|-|d'|$", r"Đó là khoảng cách từ ảnh tới $F'$, không phải tới vật.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 3 ──
 dict(nhan_dang=r"Thấy <b>ảnh cao gấp n lần</b> hoặc <b>ảnh cách vật L</b> mà đề không nói loại ảnh → xét cả ảnh thật lẫn ảnh ảo.",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 1}, buoc=[
  buoc("Ảnh thật cao gấp 3 vật", "Ảnh thật: vật đặt cách thấu kính bao nhiêu cm?", 16, "cm", 0.3,
       loi=r"Viết $d'=\dfrac d3$ (đảo tỉ số) thay vì $d'=3d$; ảnh cao gấp $3$ thì ảnh xa thấu kính gấp $3$ lần vật."),
  buoc("Ảnh ảo cao gấp 3 vật", "Ảnh ảo: vật đặt cách thấu kính bao nhiêu cm?", 8, "cm", 0.3,
       loi=r"Dừng lại sau trường hợp ảnh thật; hoặc xét ảnh ảo nhưng vẫn để $d'$ dương.",
       ke=[(r"Xét thêm ảnh ảo: $d'=-3d$, thấu kính vẫn có $f\gt0$", True),
           (r"Dừng: thấu kính hội tụ chỉ cho một vị trí ảnh gấp $3$ lần", r"Khi vật trong khoảng $OF$, thấu kính hội tụ cho ảnh ảo lớn hơn vật, cũng có thể gấp $3$ lần."),
           (r"Xét ảnh ảo bằng cách đổi dấu tiêu cự", r"Thấu kính không đổi, vẫn hội tụ nên $f\gt0$; ảnh ảo thể hiện ở dấu của $d'$.")]),
  buoc("Khoảng cách vật – ảnh câu a", "Trường hợp ảnh ảo: ảnh cách vật bao nhiêu cm?", 16, "cm", 0.3,
       loi=r"Cộng $d+|d'|$ cho cả trường hợp ảnh ảo.",
       ke=[(r"Ảnh ảo cùng phía vật, xa thấu kính hơn vật: lấy $|d'|-d$", True),
           (r"Cộng $d+|d'|$ như ảnh thật", r"Ảnh ảo nằm cùng phía với vật, khoảng cách là hiệu."),
           (r"Lấy luôn $|d'|$", r"$|d'|$ là khoảng cách từ ảnh tới thấu kính, chưa phải tới vật.")]),
  buoc("Ảnh thật cách vật 50 cm", "Nghiệm nhỏ hơn của d (ảnh thật) là bao nhiêu cm?", 20, "cm", 0.3,
       loi=r"Thế $d'=\dfrac{df}{d+f}$ (sai dấu) hoặc tính $\Delta$ sai, ra phương trình vô nghiệm.",
       ke=[(r"Đặt $d+d'=50$, thế $d'=\dfrac{12d}{d-12}$ được phương trình bậc hai theo $d$", True),
           (r"Đặt $d'-d=50$", r"Ảnh thật ở khác phía vật nên khoảng cách vật – ảnh là tổng $d+d'$."),
           (r"Lấy $d=d'=25\ \text{cm}$", r"$d=d'$ chỉ xảy ra khi vật ở $2f$; thế $d=25$ vào công thức thấy $d'\ne25$.")]),
  buoc("Ảnh ảo cách vật 50 cm", "Ảnh ảo: vật đặt cách thấu kính bao nhiêu cm?", 10, "cm", 0.3,
       loi=r"Bỏ qua trường hợp ảnh ảo vì ảnh ảo không hứng được trên màn; đề chỉ hỏi ảnh cách vật, không nói hứng trên màn.",
       ke=[(r"Ảnh ảo: $|d'|-d=50$, tức $d'=-(d+50)$, giải phương trình bậc hai", True),
           (r"Ảnh ảo: $d+|d'|=50$", r"Ảnh ảo cùng phía vật, khoảng cách vật – ảnh là hiệu $|d'|-d$."),
           (r"Bỏ qua ảnh ảo vì không hứng được trên màn", r"Đề hỏi ảnh cách vật, không yêu cầu hứng ảnh trên màn.")]),
  buoc("Kết luận số vị trí", "Có bao nhiêu vị trí đặt vật thoả mãn câu b?",
       lua_chon=[(r"Ba vị trí: hai cho ảnh thật, một cho ảnh ảo", True),
                 (r"Hai vị trí, đều cho ảnh thật", r"Bỏ sót trường hợp ảnh ảo: vật trong khoảng $OF$ cũng cho ảnh cách vật đúng khoảng đó."),
                 (r"Bốn vị trí: hai cho ảnh thật, hai cho ảnh ảo", r"Phương trình ảnh ảo có một nghiệm âm; vật thật nên $d\gt0$, loại nghiệm đó.")],
       loi=r"Giữ nghiệm âm của phương trình ảnh ảo, hoặc quên hẳn trường hợp ảnh ảo.",
       ke=[(r"Đếm các nghiệm $d\gt0$ của cả hai phương trình, kiểm dấu $d'$ khớp loại ảnh", True),
           (r"Chỉ đếm nghiệm của phương trình ảnh thật", r"Ảnh ảo cũng có thể cách vật đúng khoảng đó; phải đếm cả nghiệm hợp lệ của phương trình ảnh ảo."),
           (r"Đếm mọi nghiệm của hai phương trình, kể cả nghiệm âm", r"Vật thật nên $d\gt0$; nghiệm âm không ứng với vị trí đặt vật nào.")]),
  buoc("Kiểm tra")]),
]


def kiem_so():
    F = Fr
    # D1
    assert D1P == 24 and H1P == 4 and D1P / 2 == 12 and H1P / 2 == 2
    assert X_O == 0 and X_F == -12 and F1B == -12 and D1B == 24
    assert anh(F1B, D1B) == XBP - X_O and abs(anh(F1B, D1B)) / D1B * YB == YBP          # d' = −8, h' = 1
    assert XBP - XB == 16                                                                # AA' = 16 cm
    # ba tia hình a cùng qua B'(12; −2) (đơn vị ô): song song→F'(4,0); qua O; qua F(−4,0)→K(0,−2)
    assert 1 - F(12, 4) == -2 and F(-12, 6) == -2 and 1 + (0 + 6) * F(0 - 1, -4 + 6) == -2
    # cách sai D1 cho số khác đáp án
    assert H1 * F(F1, D1) != H1P and H1 != H1P and abs(-X_F) != abs(XBP - X_O)        # h·f/d; h' = h; OF' = OA'
    assert abs(XBP - X_O) != abs(X_F) and (XB + XBP) / 2 != X_O
    # D2
    assert D2AP == -60 and H2AP == 4 and L2A == 45
    assert F(abs(D2AP), D2A) == F(F2A + abs(D2AP), F2A)                                  # phương trình tam giác ảnh ảo
    assert F(abs(D2AP), D2A) != F(abs(D2AP) - F2A, F2A) and F(abs(D2AP), D2A) != F(F2A, F2A + abs(D2AP))
    assert F(D2A * F2A, D2A + F2A) != 60 and F2A - D2A != 60                             # cách giải sai
    assert H2A * F(D2A, abs(D2AP)) != 4 and H2A * F(F2A, D2A) != 4
    assert D2A + abs(D2AP) != 45 and abs(D2AP) - F2A != 45
    assert D2BP == -10 and H2BP == 1 and L2B == 5
    assert anh(30, 15) == -30 and anh(30, 15) != D2BP                                     # quên dấu f
    assert 1 / (F(1, F2B) + F(1, D2B)) == 30 and 30 != D2BP                               # chuyển vế sai
    assert D2B + abs(D2BP) != 5 and abs(F2B) - abs(D2BP) != 5
    assert F(abs(F2B) - abs(D2BP), abs(F2B)) == F(abs(D2BP), D2B) == F(2, 3)            # kiểm tam giác PK
    # D3
    assert D3_THAT == 16 and anh(F3, D3_THAT) == 3 * D3_THAT == 48
    assert D3_AO == 8 and anh(F3, D3_AO) == -3 * D3_AO == -24
    assert D3_THAT + 48 == 64 and 24 - D3_AO == 16 and D3_AO + 24 != 16 and 24 != 16
    assert R3_THAT == [20.0, 30.0] and anh(F3, 20) == 30 and anh(F3, 30) == 20
    assert R3_AO == [-60.0, 10.0] and anh(F3, 10) == -60 and abs(anh(F3, 10)) - 10 == L3
    assert L3 >= 4 * F3
    # cách sai D3 cho số khác đáp án
    assert anh(F3, 25) != 25                                                              # d = d' = 25
    d_sai = roots(1, 26, -600)[1]; assert abs(d_sai - 20) > 1                              # d' − d = 50 với ảnh thật
    d_sai2 = roots(1, -74, 600)[0]; assert abs(d_sai2 - 10) > 0.5                          # d + |d'| = 50 với ảnh ảo
    assert 1 / (F(1, F3) - F(1, 3) / F3) != D3_THAT                                       # đảo tỉ số d' = d/3 → d = 18
    assert 1 / (F(1, F3) - F(1, 3) / F3) == 18
    # không chuỗi nào chứa ký tự điều khiển (\t, \b, \f do quên r"…" trước \text, \beta, \frac)
    import ast
    src = ast.parse(open(__file__, encoding="utf-8").read())
    bad = [n.lineno for n in ast.walk(src) if isinstance(n, ast.Constant) and isinstance(n.value, str)
           and any(chr(k) in n.value for k in (7, 8, 9, 11, 12, 13))]
    assert not bad, f"chuỗi có ký tự điều khiển ở dòng {bad}"
    # không còn \' trong công thức (raw string r'…\'…' giữ cả dấu \ → KaTeX lỗi)
    import json as _j
    blob = _j.dumps([DANG, ANALYSIS, SOLS, STEPS], ensure_ascii=False)
    assert "\\\\'" not in blob, "còn \\' trong nội dung"
    print("kiểm số liệu D1–D3 (bài 156): đạt")
