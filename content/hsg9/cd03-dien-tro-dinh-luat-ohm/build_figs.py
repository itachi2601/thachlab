"""Sinh 4 hình SVG, thay <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được).
Chạy: python3 content/hsg9/cd03-dien-tro-dinh-luat-ohm/build_figs.py
Số liệu hình tính từ phương trình (không gõ tay toạ độ). Linh kiện mạch điện: scripts/data/bai-tap-mau/hinh_159.py."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "scripts", "data", "bai-tap-mau"))
from hinh_159 import *

PHUT = 12   # điền theo lint_do_dai.py (làm tròn lên)

# ---------- Hình 1: kéo dãn dây, thể tích không đổi ----------
n = 2
l1, d1 = 110.0, 36.0
l2, d2 = n * l1, d1 / math.sqrt(n)             # S ∝ d²: S giảm n lần  =>  d giảm √n lần
assert abs((l1 * d1 ** 2) - (l2 * d2 ** 2)) < 1e-6   # V ∝ l·d² không đổi
X0 = 40
b = txt(X0, 20, "Ban đầu", "currentColor", 14)
y1 = 60
b += R(X0, y1 - d1 / 2, l1, d1, BLUE, 2.6, "rgba(56,189,248,.18)", 8)
b += seg(X0, y1 + 28, X0 + l1, y1 + 28, "currentColor", 1.6) + tick(X0, y1 + 28, 5) + tick(X0 + l1, y1 + 28, 5) + txt(X0 + l1 / 2, y1 + 46, "l", "currentColor", 14, "middle")
b += txt(X0 + l1 + 22, y1 - 2, "tiết diện S", "currentColor", 14) + txt(X0 + l1 + 22, y1 + 18, "R = 8 Ω", RED, 15)
b += txt(X0, 134, "Kéo dài gấp đôi (V không đổi)", "currentColor", 14)
y2 = 170
b += R(X0, y2 - d2 / 2, l2, d2, ORG, 2.6, "rgba(251,146,60,.18)", 8)
b += seg(X0, y2 + 28, X0 + l2, y2 + 28, "currentColor", 1.6) + tick(X0, y2 + 28, 5) + tick(X0 + l2, y2 + 28, 5) + txt(X0 + l2 / 2, y2 + 46, "2l", "currentColor", 14, "middle")
b += txt(X0 + l2 + 12, y2 - 2, "S/2", "currentColor", 14) + txt(X0 + l2 + 12, y2 + 18, "R = 32 Ω", RED, 15)
fig1 = wrap("0 0 380 232", "Dây đồng được kéo dài gấp đôi thì mảnh đi một nửa tiết diện, điện trở từ 8 ôm lên 32 ôm",
            b, "Hình 1. Dây dài gấp đôi, tiết diện giảm một nửa.<br>$R$ tăng $2\\cdot2=4$ lần: từ $8\\ \\Omega$ lên $32\\ \\Omega$.<br>Hình minh hoạ, không đúng tỉ lệ.")

# ---------- Hình 2: đồ thị U–I (trái) và I–U (phải) của hai vật dẫn 6 Ω và 9 Ω ----------
R1_, R2_ = 6.0, 9.0
b = txt(12, 18, "U–I: độ dốc = R", "currentColor", 14) + txt(206, 18, "I–U: độ dốc = 1/R", "currentColor", 14)
# trái: trục I (A) ngang 0..1,0 ; U (V) dọc 0..9
ox, oy, kx, ky = 40, 190, 120.0, 14.0
b += graph_axes(ox, oy, 130, 126, "I (A)", "U (V)", (0.5, 1.0), (3, 6, 9), kx, ky)
for Rv, col, nm in ((R1_, RED, "1"), (R2_, BLUE, "2")):
    b += poly([(ox, oy), (ox + kx * 1.0, oy - ky * Rv * 1.0)], col, 2.8)
    b += txt(ox + kx * 1.0 + 6, oy - ky * Rv + 5, nm, col, 15)
# phải: trục U (V) ngang 0..9 ; I (A) dọc 0..1,5
ox2, oy2, kx2, ky2 = 232, 190, 12.0, 84.0
b += graph_axes(ox2, oy2, 112, 126, "U (V)", "I (A)", (3, 6, 9), (0.5, 1.0, 1.5), kx2, ky2)
for Rv, col, nm in ((R1_, RED, "1"), (R2_, BLUE, "2")):
    b += poly([(ox2, oy2), (ox2 + kx2 * 9, oy2 - ky2 * 9 / Rv)], col, 2.8)
    b += txt(ox2 + kx2 * 9 + 6, oy2 - ky2 * 9 / Rv + 5, nm, col, 15)
fig2 = wrap("0 0 380 232", "Đồ thị U theo I và I theo U của hai vật dẫn có điện trở 6 ôm và 9 ôm",
            b, "Hình 2. Vật dẫn 1: $6\\ \\Omega$ (đỏ). Vật dẫn 2: $9\\ \\Omega$ (xanh).<br>Trái: $U$–$I$, đường 2 dốc hơn. Phải: $I$–$U$, đường 2 thoải hơn.")

# ---------- Hình 3: mạch biến trở ----------
fig3 = wrap("0 0 380 170", "Nguồn 24 vôn nối tiếp điện trở 30 ôm, biến trở 50 ôm và ampe kế",
            mach_bien_tro("U = 24 V", "R = 30 Ω", "biến trở 50 Ω"),
            "Hình 3. Biến trở (con chạy cam) nối tiếp với $R$.<br>Con chạy sang phải làm $R_b$ tăng, $I$ giảm.")

# ---------- Hình 4: ampe kế và vôn kế có điện trở ----------
fig4 = wrap("0 0 380 170", "Ampe kế có điện trở R_A nối tiếp, vôn kế có điện trở R_V mắc song song với R",
            mach_dung_cu(), "Hình 4. Ampe kế (đỏ) nối tiếp, vôn kế (xanh) song song với $R$.<br>Mỗi dụng cụ là một điện trở trong mạch.")

src = open(os.path.join(HERE, "theory.src.html"), encoding="utf8").read()
for k, f in ((1, fig1), (2, fig2), (3, fig3), (4, fig4)):
    assert f"<!--FIG{k}-->" in src
    src = src.replace(f"<!--FIG{k}-->", f)
src = src.replace("__PHUT__", str(PHUT))
open(os.path.join(HERE, "theory.html"), "w", encoding="utf8").write(src)
print("ok", len(src))
