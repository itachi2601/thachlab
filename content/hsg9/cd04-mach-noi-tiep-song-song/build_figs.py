"""Sinh 3 hình SVG, thay <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Chạy: python3 content/hsg9/cd04-mach-noi-tiep-song-song/build_figs.py
Số liệu trong bài được kiểm lại bằng Fraction ở đầu file (assert); hình vẽ dùng mach.py."""
import os, sys
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mach import *

PHUT = 10   # điền theo lint_do_dai.py (làm tròn lên)

par = lambda *r: 1 / sum(F(1) / x for x in r)

# ---------- kiểm số liệu trong bài ----------
assert par(12, 4, 6) == 2 and par(12, 4) == 3                                  # q1
R23 = par(6, 3); assert (R23, 2 + R23, F(12) / (2 + R23)) == (2, 4, 3)           # bài toán mẫu
assert (F(12) / 4 * 2, 12 - F(12) / 4 * 2, 6 * 1 == 6) and F(6) / 6 == 1 and F(6) / 3 == 2
R23b = par(6, 12); Rb = 2 + R23b; Ib = F(12) / Rb; U23b = 12 - Ib * 2          # biến thể
assert (R23b, Rb, Ib, U23b / 6, U23b / 12) == (4, 6, 2, F(4, 3), F(2, 3))
Rt_open = 4 + par(12, 6); assert (Rt_open, F(12) / Rt_open, F(12) / 4, F(12) / (4 + 6)) == (8, F(3, 2), 3, F(6, 5))   # q3
assert 4 * 12 == 6 * 8 and par(4, 6) + par(8, 12) == F(36, 5) == F(12 * 18, 30)  # cầu ví dụ
assert F(6 * 5, 3) == 10 and F(3, 6) == F(5, 10)                                # q4
for rv, un, d in ((100, 4.00, 33.3), (1000, 5.71, 4.8), (10000, 5.97, 0.5)):     # bảng đo vôn kế
    rp = float(par(100, rv)); u = 12 * rp / (100 + rp)
    assert abs(u - un) < 0.006 and abs((6 - u) / 6 * 100 - d) < 0.06, (rv, u)
r = F(6); assert sorted({3 * r, 3 * r / 2, 2 * r / 3, r / 3}) == [2, 4, 9, 18]  # q6: bốn cách ghép
assert 2 * (2 + 4) == 12 == 1 * (2 + 10) and 12 / (2 + 4) == 2                  # thử thách


def tr(body, dx, dy):
    return f'<g transform="translate({dx} {dy})">{body}</g>'

R23c = par(6, 6); assert (R23c, 2 + R23c, F(12) / (2 + R23c), F(12) / 5 * 2, 12 - F(12) / 5 * 2, (12 - F(12) / 5 * 2) / 6) == (3, 5, F(12, 5), F(24, 5), F(36, 5), F(6, 5))   # biến thể R3=6
rp = par(100, 100000); assert (6 - 12 * rp / (100 + rp)) / 6 * 100 < F(1, 10) < (6 - 12 * par(100, 10000) / (100 + par(100, 10000))) / 6 * 100   # q5

# ---------- Hình 1: mạch hỗn hợp và mạch đã thu gọn ----------
b, _ = c_hh("R_1", "R_2", "R_3")
b += lab(105, 106, "Mạch ban đầu", "currentColor", 14, "start", "600")
red = branch((50, 40), (230, 40), [("R", "R_1")]) + branch((230, 40), (230, 160), [("R", "R_{23}")]) \
    + branch((50, 40), (50, 160), [("E", "U")]) + wire((50, 160), (230, 160))
red += lab(105, 106, "Sau khi thu gọn", "currentColor", 14, "start", "600")
fig1 = fig("", "0 0 440 380", "Mạch gồm R1 nối tiếp với R2 song song R3, có ampe kế và vôn kế, rồi mạch thu gọn còn R1 nối tiếp R23",
           b + tr(red, 0, 190), "Hình 1. Đoạn song song giữa hai nút M, N thu gọn thành $R_{23}=\\dfrac{R_2R_3}{R_2+R_3}$.<br>Sau đó chỉ còn hai điện trở nối tiếp: $R_{td}=R_1+R_{23}$.")

# ---------- Hình 2: khoá K song song R2, đóng ----------
b, _ = c_hh("R_1", "R_2", "R_3", A=True, V=False, shortK="open")
fig2 = fig("", "0 0 470 200", "Khoá K mắc song song với R2; ampe kế ở nhánh chính",
           b, "Hình 2. Khoá K mắc song song với $R_2$ (đang mở).<br>Ampe kế lí tưởng ở nhánh chính.")

# ---------- Hình 3: cầu ----------
b, g = c_bridge("R_1", "R_2", "R_3", "R_4", mid=("V", ""))
fig3 = fig("", "0 0 340 200", "Mạch cầu: hai nhánh M-P-N và M-Q-N, vôn kế lí tưởng nối giữa P và Q",
           b, "Hình 3. Nhánh trái: $R_1$ rồi $R_3$. Nhánh phải: $R_2$ rồi $R_4$.<br>Vôn kế lí tưởng nối hai điểm giữa P và Q.")

src = open(os.path.join(HERE, "theory.src.html"), encoding="utf8").read()
for n, f in ((1, fig1), (2, fig2), (3, fig3)):
    assert f"<!--FIG{n}-->" in src
    src = src.replace(f"<!--FIG{n}-->", f)
src = src.replace("__PHUT__", str(PHUT))
open(os.path.join(HERE, "theory.html"), "w", encoding="utf8").write(src)
print("ok", len(src))
