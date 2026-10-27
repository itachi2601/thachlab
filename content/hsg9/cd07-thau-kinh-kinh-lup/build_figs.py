"""CĐ07 Thấu kính (bài 156): sinh 5 hình SVG, thay <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Hình dựng ảnh vẽ trên lưới ô ly mờ (HS vẽ lại trên giấy ô ly). Mọi số liệu dùng trong bài được assert ở kiem_so().
Chạy: python3 content/hsg9/cd07-thau-kinh-kinh-lup/build_figs.py"""
import os, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "soan-bai-ly-thuyet-tuong-tac", "scripts"))
from svg_lib import text, wrap, chevron

PHUT = 18
# màu tầm trung: đọc được cả nền sáng (mặc định) lẫn nền tối
RAY, OBJ, IMG, AUX = "#dc2626", "#0284c7", "#059669", "#ea580c"
GRID = "rgba(148,163,184,.30)"


# ───────────────────────── kiểm số liệu (mọi số trong theory.src.html) ─────────────────────────
def anh(f, d):
    f, d = Fr(f), Fr(d)
    inv = 1 / f - 1 / d
    return None if inv == 0 else 1 / inv


def kiem_so():
    # ví dụ kiểm quy ước + hình 1, 2, 4 (đổi khỏi f = 12 để không lộ D3)
    assert anh(6, 10) == 15 and Fr(15, 10) == Fr(3, 2) and Fr(3, 2) * 4 == 6     # hình 1
    assert anh(6, 4) == -12 and Fr(12, 4) == 3                                   # hình 4
    assert anh(-6, 6) == -3 and Fr(3, 6) == Fr(1, 2)
    # hình 1: tia qua F từ B(-10,4) tới K(0,-6); tia F'B' kéo dài tới (16,5; -7)
    assert 4 + (-4 / 4) * 10 == -6 and abs(-6 + (-6 / 9) * 1.5 - (-7)) < 1e-9
    assert anh(-10, 15) == -6 and Fr(6, 15) * 5 == 2            # hình 2: h = 5, h' = 2
    assert anh(6, 15) == 10                                      # hình 3: điểm sáng S (f = 6, SO = 15)
    y1 = Fr(4, 15) * 6                                           # trục phụ cắt tiêu diện ảnh tại (6; 1,6)
    assert y1 == Fr(8, 5) and 0 + 4 * 6 / (4 - y1) == 10        # tia I(0;4) qua F1' cắt trục tại 10
    # q2: HT f = 10, d = 6
    assert anh(10, 6) == -15 and Fr(15, 6) == Fr(5, 2)
    assert 1 / (Fr(1, 10) + Fr(1, 6)) == Fr(15, 4)
    assert anh(-10, 6) == Fr(-15, 4)
    # bảng f = 10 (mục IV)
    bang = {110: 11, 60: 12, 35: 14, 20: 20, 14: 35, 11: 110}
    for d, dp in bang.items():
        assert anh(10, d) == dp
    assert [Fr(bang[d], d) for d in bang] == [Fr(1, 10), Fr(1, 5), Fr(2, 5), 1, Fr(5, 2), 10]
    assert [d + bang[d] for d in bang] == [121, 72, 49, 40, 49, 121]
    # bài toán mẫu hệ hai TK: f1 = 20, d1 = 10, f2 = 15, a = 10, h = 1
    d1p = anh(20, 10); assert d1p == -20
    d2 = 10 - d1p; assert d2 == 30
    d2p = anh(15, d2); assert d2p == 30 and 10 + d2p == 40
    assert 1 * Fr(20, 10) * Fr(30, 30) == 2
    assert anh(15, 10) == -30                                    # bẫy: lấy d2 = a
    # điền bước: a = 20
    d2 = 20 - d1p; assert d2 == 40
    d2p = anh(15, d2); assert d2p == 24 and Fr(24, 40) == Fr(3, 5) and 2 * Fr(3, 5) == Fr(6, 5)
    # thử thách ⭐: PK f = -20, d = 20, h = 4
    assert anh(-20, 20) == -10 and Fr(10, 20) * 4 == 2 and 20 - 10 == 10
    # ⭐⭐: HT f = 16, ảnh cao gấp 2
    assert anh(16, 24) == 48 and anh(16, 8) == -16
    # ⭐⭐⭐ ghép sát HT 20 + PK -30
    fs = 1 / (Fr(1, 20) + Fr(1, -30)); assert fs == 60
    assert anh(fs, 30) == -60
    d1p = anh(20, 30); assert d1p == 60
    assert anh(-30, -d1p) == -60                                 # vật ảo d2 = -60
    # kính lúp 10x, ví dụ 4x
    assert Fr(25, 10) == Fr(5, 2) and Fr(25, 4) == Fr(25, 4) and 25 / 4 == 6.25
    # Bessel q6: L = 96, l = 48
    L, l = 96, 48
    assert Fr(L * L - l * l, 4 * L) == 18 and L >= 4 * 18
    assert anh(18, 24) == 72 and Fr(L, 4) == 24 and Fr(l, 4) == 12 and Fr(L * L - l * l, 2 * L) == 36
    # thí nghiệm Bessel: L = 80, ba lần đo l
    L = 80
    ls = [39.6, 40.5, 40.2]
    fs_ = [(L * L - x * x) / (4 * L) for x in ls]
    assert [round(x, 2) for x in fs_] == [15.10, 14.87, 14.95]
    ftb = sum(fs_) / 3
    df = sum(abs(x - ftb) for x in fs_) / 3
    assert round(ftb, 2) == 14.97 and round(df, 2) == 0.08
    assert (L * L - 40 * 40) / (4 * L) == 15
    assert round(((L + 1) ** 2 - 1600) / (4 * (L + 1)), 2) == 15.31
    assert round((L * L - 41 ** 2) / (4 * L), 2) == 14.75
    # L >= 4f, hai vị trí đối xứng (ví dụ chữ, không số)
    print("kiem_so: ok")


# ───────────────────────── công cụ vẽ ─────────────────────────
class Scene:
    """Hệ toạ độ cm: thấu kính tại x = 0, trục chính y = 0. s = px/cm, cell = số cm của 1 ô."""

    def __init__(self, x0, x1, y0, y1, s, cell, ox, oy):
        self.x0, self.x1, self.y0, self.y1, self.s, self.cell, self.ox, self.oy = x0, x1, y0, y1, s, cell, ox, oy
        self.b = ""

    def X(self, x):
        return self.ox + x * self.s

    def Y(self, y):
        return self.oy - y * self.s

    def P(self, x, y):
        return self.X(x), self.Y(y)

    def grid(self):
        c = self.cell
        k = -(-self.x0 // c) * c if self.x0 % c else self.x0
        x = self.x0
        while x <= self.x1 + 1e-9:
            self.b += f'<line x1="{self.X(x):.1f}" y1="{self.Y(self.y1):.1f}" x2="{self.X(x):.1f}" y2="{self.Y(self.y0):.1f}" stroke="{GRID}" stroke-width="0.8"/>'
            x += c
        y = self.y0
        while y <= self.y1 + 1e-9:
            self.b += f'<line x1="{self.X(self.x0):.1f}" y1="{self.Y(y):.1f}" x2="{self.X(self.x1):.1f}" y2="{self.Y(y):.1f}" stroke="{GRID}" stroke-width="0.8"/>'
            y += c

    def line(self, p, q, c="currentColor", w=2, dash=""):
        (x1, y1), (x2, y2) = self.P(*p), self.P(*q)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.b += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'

    def ray(self, p, q, c=RAY, mid=True):
        """Tia sáng nét liền, mũi tên giữa tia (chiều p -> q)."""
        self.line(p, q, c, 2)
        if mid:
            (x1, y1), (x2, y2) = self.P(*p), self.P(*q)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.b += chevron(mx, my, x2 - x1, y2 - y1, c, 2, 9)

    def ext(self, p, q, c=RAY):
        """Đường kéo dài (ảo) nét đứt."""
        self.line(p, q, c, 1.5, "5 4")

    def axis(self):
        self.line((self.x0 - 0.6 * self.cell, 0), (self.x1 + 0.6 * self.cell, 0), "currentColor", 1.6)
        x, y = self.P(self.x1 + 0.6 * self.cell, 0)
        self.b += text(round(x - 2, 1), round(y - 8, 1), "Δ", "currentColor", 15, "end", "700")

    def lens(self, kind, top, bot):
        (x, yt), (_, yb) = self.P(0, top), self.P(0, bot)
        self.b += f'<line x1="{x:.1f}" y1="{yt:.1f}" x2="{x:.1f}" y2="{yb:.1f}" stroke="currentColor" stroke-width="2.6"/>'
        if kind == "HT":       # hai mũi tên hướng ra
            self.b += chevron(x, yt, 0, -1, "currentColor", 2.4, 11) + chevron(x, yb, 0, 1, "currentColor", 2.4, 11)
        else:                  # chữ V hướng vào
            self.b += chevron(x, yt, 0, 1, "currentColor", 2.4, 11) + chevron(x, yb, 0, -1, "currentColor", 2.4, 11)

    def arrow_obj(self, x, h, c, dash=""):
        """Mũi tên vật/ảnh vuông góc trục tại x, cao h (âm = dưới trục)."""
        self.line((x, 0), (x, h), c, 3 if not dash else 2.4, dash)
        X, Y = self.P(x, h)
        self.b += chevron(X, Y, 0, -1 if h > 0 else 1, c, 2.6, 10)

    def dot(self, x, y, c="currentColor", r=3.2):
        X, Y = self.P(x, y)
        self.b += f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{r}" fill="{c}"/>'

    def lab(self, x, y, s, c="currentColor", dx=0, dy=0, anchor="middle", size=15):
        X, Y = self.P(x, y)
        self.b += text(round(X + dx, 1), round(Y + dy, 1), s, c, size, anchor, "700")


def sub(a, b, tail=""):
    """'F' + chỉ số dưới + phần đuôi (về lại dòng chính)."""
    return f'{a}<tspan font-size="12" dy="4">{b}</tspan><tspan dy="-4">{tail}</tspan>'


# ═════════ Hình 1: TK hội tụ, ba tia đặc biệt, ảnh thật (f = 6, d = 10, h = 4 -> d' = 15, h' = 6), 1 ô = 1 cm ═════════
S = Scene(-12, 18, -7, 5, 13, 1, 178, 86)
S.grid(); S.axis(); S.lens("HT", 5.6, -7.6)
B, Bp = (-10, 4), (15, -6)
S.ray(B, (0, 4)); S.ray((0, 4), (6, 0)); S.ray((6, 0), Bp); S.line(Bp, (16.5, -7), RAY, 2)
S.ray(B, (-6, 0)); S.ray((-6, 0), (0, -6)); S.ray((0, -6), Bp)
S.ray(B, (0, 0)); S.ray((0, 0), Bp)
S.arrow_obj(-10, 4, OBJ); S.arrow_obj(15, -6, IMG)
for x in (-6, 6):
    S.dot(x, 0)
S.lab(-10, 0, "A", OBJ, 0, 18); S.lab(-10, 4, "B", OBJ, -12, 2)
S.lab(15, 0, "A'", IMG, 0, -8); S.lab(15, -6, "B'", IMG, -14, 18)
S.lab(-6, 0, "F", "currentColor", 0, 18); S.lab(6, 0, "F'", "currentColor", 0, -9)
S.lab(0, 0, "O", "currentColor", -9, 18); S.lab(0, 4, "I", "currentColor", 10, -6, "start")
S.lab(0, -6, "K", "currentColor", 9, 16, "start")
fig1 = wrap("0 0 440 196",
            "Thấu kính hội tụ trên lưới ô ly: ba tia đặc biệt từ đỉnh B của vật AB gặp nhau tại B' phía sau thấu kính, ảnh thật A'B' ngược chiều",
            S.b, "Hình 1. Ba tia đặc biệt qua thấu kính hội tụ, ảnh thật.<br>Lưới: 1 ô = 1 cm.")

# ═════════ Hình 2: TK phân kì (f = -10, d = 15, h = 5 -> d' = -6, h' = 2), 1 ô = 1 cm ═════════
S = Scene(-18, 12, -4, 10, 12.2, 1, 242, 142)
S.grid(); S.axis(); S.lens("PK", 10.6, -4.4)
B, Bp = (-15, 5), (-6, 2)
S.ray(B, (0, 5)); S.ray((0, 5), (9, 9.5)); S.ext((0, 5), (-10, 0))
S.ray(B, (0, 2)); S.ray((0, 2), (11, 2)); S.ext((0, 2), Bp); S.ext((0, 2), (10, 0), AUX)
S.ray(B, (0, 0)); S.ray((0, 0), (10, -10 / 3))
S.arrow_obj(-15, 5, OBJ); S.arrow_obj(-6, 2, IMG, "5 3")
for x in (-10, 10):
    S.dot(x, 0)
S.lab(-15, 0, "A", OBJ, 0, 18); S.lab(-15, 5, "B", OBJ, -12, 0)
S.lab(-6, 0, "A'", IMG, 0, 18); S.line((-5.6, 2.4), (-3.9, 3.5), IMG, 1.2)
S.lab(-3.7, 3.6, "B'", IMG, 0, 0, "start")
S.lab(-10, 0, "F'", "currentColor", 0, 18); S.lab(10, 0, "F", "currentColor", 0, 18)
S.lab(0, 0, "O", "currentColor", 10, 18, "start"); S.lab(0, 5, "I", "currentColor", 9, -6, "start")
S.lab(0, 2, "K", "currentColor", 9, -6, "start")
fig2 = wrap("0 0 440 210",
            "Thấu kính phân kì trên lưới ô ly: tia song song ló ra loe rộng, đường kéo dài đi qua F' cùng phía vật; ảnh ảo A'B' cùng chiều, nhỏ hơn vật, vẽ nét đứt",
            S.b, "Hình 2. Thấu kính phân kì: F' cùng phía vật.<br>Nét đứt đỏ: đường kéo dài. Nét đứt cam: tia tới hướng về F.<br>Lưới: 1 ô = 1 cm.")

# ═════════ Hình 3: điểm sáng S trên trục chính (HT f = 6, SO = 15 -> S' tại 10), 1 ô = 1 cm: tia bất kì + trục phụ ═════════
S = Scene(-17, 13, -2, 5, 13, 1, 240, 86)
S.grid(); S.axis(); S.lens("HT", 5.4, -2.6)
S.line((6, 5.4), (6, -2.4), "currentColor", 1.4, "3 3")
S.line((-7, -28 / 15), (13, 52 / 15), AUX, 1.6, "6 4")                    # trục phụ y = (4/15)x qua O
S.ray((-15, 0), (0, 4)); S.ray((0, 4), (10, 0)); S.line((10, 0), (12.5, -1), RAY, 2)
S.dot(-15, 0, OBJ, 4); S.dot(6, 1.6, AUX); S.dot(10, 0, IMG, 4); S.dot(-6, 0); S.dot(6, 0)
S.lab(-15, 0, "S", OBJ, 0, 20); S.lab(10, 0, "S'", IMG, 2, 20)
S.lab(-6, 0, "F", "currentColor", 0, -8); S.lab(6, 0, "F'", "currentColor", -12, 18)
S.lab(6, 1.6, sub("F", "1", "'"), AUX, 10, -14, "start")
S.lab(0, 0, "O", "currentColor", -10, 18); S.lab(0, 4, "I", "currentColor", -10, -4)
S.lab(-7, -28 / 15, "trục phụ", AUX, -6, 5, "end", 14)
S.lab(6, 5.4, "tiêu diện ảnh", "currentColor", 6, 4, "start", 14)
fig3 = wrap("0 0 440 132",
            "Dựng ảnh điểm sáng S trên trục chính thấu kính hội tụ: tia bất kì SI, trục phụ qua O song song SI cắt tiêu diện ảnh tại F1', tia ló qua F1' cắt trục chính tại S'",
            S.b, "Hình 3. Dựng ảnh điểm sáng S trên trục chính.<br>Lưới: 1 ô = 1 cm.")

# ═════════ Hình 4: TK hội tụ, vật trong OF -> ảnh ảo (f = 6, d = 4, h = 2 -> d' = -12, h' = 6), 1 ô = 1 cm ═════════
S = Scene(-14, 12, -5, 7, 13, 1, 204, 110)
S.grid(); S.axis(); S.lens("HT", 7.4, -5.4)
B, Bp = (-4, 2), (-12, 6)
S.ray(B, (0, 2)); S.ray((0, 2), (6, 0)); S.ray((6, 0), (11, -5 / 3)); S.ext((0, 2), Bp)
S.ray(B, (0, 0)); S.ray((0, 0), (10, -5)); S.ext(B, Bp)
S.arrow_obj(-4, 2, OBJ); S.arrow_obj(-12, 6, IMG, "5 3")
for x in (-6, 6):
    S.dot(x, 0)
S.lab(-4, 0, "A", OBJ, 0, 18); S.lab(-4, 2, "B", OBJ, -8, 12, "end")
S.lab(-12, 0, "A'", IMG, 0, 18); S.lab(-12, 6, "B'", IMG, -14, 4)
S.lab(-6, 0, "F", "currentColor", 0, 18); S.lab(6, 0, "F'", "currentColor", 0, -9)
S.lab(0, 0, "O", "currentColor", 10, 18, "start"); S.lab(0, 2, "I", "currentColor", 9, -7, "start")
fig4 = wrap("0 0 440 196",
            "Thấu kính hội tụ, vật AB đặt trong khoảng OF: hai tia ló loe ra, đường kéo dài gặp nhau tại B' cùng phía vật; ảnh ảo A'B' cùng chiều, lớn hơn vật",
            S.b, "Hình 4. Vật trong OF (kính lúp): đường kéo dài gặp nhau tại B'.<br>Lưới: 1 ô = 1 cm.")

# ═════════ Hình 5: sơ đồ Bessel (không số) ═════════
b = ""
XA, XM, Y0 = 34, 404, 120
X1, X2 = 120, 318                       # hai vị trí thấu kính, đối xứng: X1 - XA = XM - X2
assert abs((X1 - XA) - (XM - X2)) < 1e-9


def ln(x1, y1, x2, y2, c="currentColor", w=2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d}/>'


def dim(x1, x2, y, lab, c="currentColor"):
    s = ln(x1, y, x2, y, c, 1.4) + chevron(x1, y, -1, 0, c, 1.4, 8) + chevron(x2, y, 1, 0, c, 1.4, 8)
    s += ln(x1, y - 6, x1, y + 6, c, 1.2) + ln(x2, y - 6, x2, y + 6, c, 1.2)
    return s + text((x1 + x2) / 2, y - 8, lab, c, 15, "middle", "700")


b += ln(XA - 14, Y0, XM + 14, Y0, "currentColor", 1.4)
b += ln(XA, Y0, XA, Y0 - 34, OBJ, 3) + chevron(XA, Y0 - 34, 0, -1, OBJ, 2.6, 10)
b += text(XA, Y0 + 20, "vật", OBJ, 15, "middle", "700")
b += f'<rect x="{XM - 3}" y="{Y0 - 70}" width="6" height="110" fill="rgba(148,163,184,.45)" stroke="currentColor" stroke-width="1.4"/>'
b += text(XM - 10, Y0 - 76, "màn", "currentColor", 15, "end", "700")
for x, dash, lab in ((X1, "", "(1)"), (X2, "6 4", "(2)")):
    b += ln(x, Y0 - 52, x, Y0 + 40, "currentColor", 2.6, dash)
    b += chevron(x, Y0 - 52, 0, -1, "currentColor", 2.2, 10) + chevron(x, Y0 + 40, 0, 1, "currentColor", 2.2, 10)
    b += text(x, Y0 - 60, lab, "currentColor", 15, "middle", "700")
b += dim(XA, XM, 206, "L (giữ cố định)")
b += dim(X1, X2, 176, "ℓ", AUX)
b += dim(XA, X1, 22, "d", "currentColor")
b += dim(X2, XM, 22, "d", "currentColor")
fig5 = wrap("0 0 440 220",
            "Sơ đồ phương pháp Bessel: vật và màn cách nhau L cố định, thấu kính ở hai vị trí 1 và 2 cách nhau l đều cho ảnh rõ; khoảng từ vật tới vị trí 1 bằng khoảng từ vị trí 2 tới màn",
            b, "Hình 5. Phương pháp Bessel: L cố định.<br>Hai vị trí cho ảnh rõ cách nhau ℓ, đối xứng.")

# ═════════ ghi theory.html ═════════
if __name__ == "__main__":
    kiem_so()
    src = open(os.path.join(HERE, "theory.src.html"), encoding="utf8").read()
    for n, f in enumerate((fig1, fig2, fig3, fig4, fig5), 1):
        assert src.count(f"<!--FIG{n}-->") == 1, n
        src = src.replace(f"<!--FIG{n}-->", f)
    src = src.replace("__PHUT__", str(PHUT))
    open(os.path.join(HERE, "theory.html"), "w", encoding="utf8").write(src)
    print("ok", len(src))
