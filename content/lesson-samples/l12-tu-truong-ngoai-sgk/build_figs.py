"""Sinh 4 hình SVG cho "Chủ đề thêm. Từ trường ngoài SGK hay gặp trong đề thi" (Vật lí 12, lesson 201)
và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html. Chạy từ thư mục này: python3 build_figs.py

Màu dùng chung (giống Bài 10): đỏ = lực · cam = dòng điện I · xanh dương = cảm ứng từ B · xanh lá = vận tốc v.
Hệ trục vật lí khi kiểm chiều: x sang phải, y lên trên, z hướng ra khỏi trang (⊙).
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from svg_lib import *  # noqa: E402,F403
from _margin_fig import margin_figs  # noqa: E402

BTXT = "#0284c7"   # chữ B xanh đậm hơn nét cho dễ đọc
OTXT = "#ea580c"


def line(x1, y1, x2, y2, c="currentColor", w=2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d}/>'


def ra(x, y, r=9, c=BLUE, w=2):
    """⊙ vectơ hướng ra khỏi trang."""
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{c}" stroke-width="{w}"/>'
            f'<circle cx="{x}" cy="{y}" r="{r * 0.28:.1f}" fill="{c}"/>')


def vao(x, y, r=6, c=BLUE, w=2):
    """× vectơ hướng vào trong trang (lưới đường sức)."""
    return (f'<line x1="{x - r}" y1="{y - r}" x2="{x + r}" y2="{y + r}" stroke="{c}" stroke-width="{w}"/>'
            f'<line x1="{x + r}" y1="{y - r}" x2="{x - r}" y2="{y + r}" stroke="{c}" stroke-width="{w}"/>')


def fig(vb, label, body, cap):
    return (f'<figure class="fig" data-tl="1"><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ------------------------------------------------- Hình 1: dây thẳng dài, dòng điện hướng ra khỏi trang
# I = +z ⇒ đường sức ngược chiều kim đồng hồ khi nhìn từ phía người xem. Tại M bên phải dây: B hướng lên (+y).
cx, cy = 170, 135
b = ""
for r in (40, 75, 110):
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BLUE}" stroke-width="1.8" stroke-dasharray="6 4"/>'
    b += chevron(cx - r, cy, 0, 1, BLUE, 1.8, 11)          # bên trái: đi xuống
    b += chevron(cx, cy - r, -1, 0, BLUE, 1.8, 11)         # trên: sang trái
b += f'<circle cx="{cx}" cy="{cy}" r="15" fill="rgba(251,146,60,.18)" stroke="{ORG}" stroke-width="2.5"/>'
b += f'<circle cx="{cx}" cy="{cy}" r="4.5" fill="{ORG}"/>'
b += text(cx - 22, cy + 30, "I", OTXT, 16, "end", "700")
mx = cx + 110
b += line(cx, cy, mx, cy, "currentColor", 1.5, "4 4")
b += text((cx + mx) / 2 + 12, cy + 20, "r", "currentColor", 16, "middle", "700")
b += f'<circle cx="{mx}" cy="{cy}" r="4.5" fill="currentColor"/>'
b += text(mx + 10, cy + 22, "M", "currentColor", 16, "start", "700")
b += arrow("f1", "b", mx, cy, mx, cy - 62, 3)
b += text(mx + 10, cy - 50, "B", BTXT, 17, "start", "700")
b += text(300, 236, "B = 2·10⁻⁷ I/r", "currentColor", 15, "middle", "700")
fig1 = fig("0 0 400 260",
           "Dây dẫn thẳng dài vuông góc trang, dòng điện hướng ra ngoài. Đường sức là các đường tròn đồng tâm nét đứt, "
           "đi ngược chiều kim đồng hồ. Tại điểm M cách dây khoảng r, vectơ cảm ứng từ tiếp tuyến với đường sức, hướng lên.",
           b, "Hình 1. Dây thẳng nhìn dọc dây, dòng điện hướng ra (⊙).<br>"
              "Đường sức: tròn đồng tâm, chiều theo nắm tay phải.<br>$\\vec B$ tại M tiếp tuyến đường sức.")

# ------------------------------------------------- Hình 2: hai dòng điện song song
# Trái: I1, I2 cùng lên. B1 tại dây 2 (bên phải dây 1, I lên) hướng vào trang; F2 = I2·ŷ × (−ẑ) = −x̂ → về phía dây 1: hút.
# Phải: I1 lên, I2 xuống ⇒ F2 = (−ŷ) × (−ẑ) = +x̂ → ra xa: đẩy.
def panel(x0, down2, title):
    g = text(x0 + 85, 26, title, "currentColor", 15, "middle", "700")
    x1, x2 = x0 + 45, x0 + 125
    g += line(x1, 48, x1, 222, ORG, 3) + line(x2, 48, x2, 222, ORG, 3)
    g += chevron(x1, 80, 0, -1, ORG, 3, 12)
    g += chevron(x2, 80 if not down2 else 196, 0, 1 if down2 else -1, ORG, 3, 12)
    g += text(x1 - 10, 66, "I₁", OTXT, 15, "end", "700")
    g += text(x2 + 10, 66, "I₂", OTXT, 15, "start", "700")
    s = -1 if not down2 else 1        # hướng lực lên dây 2 theo x
    g += arrow("f2", "r", x2, 140, x2 + 34 * s, 140, 3)
    g += arrow("f2", "r", x1, 140, x1 - 34 * s, 140, 3)
    g += text(x2 + 34 * s + (8 if s > 0 else -8), 136, "F", RED, 15, "start" if s > 0 else "end", "700")
    g += vao(x2 - 22, 190, 6)
    g += text(x2 - 32, 214, "B₁", BTXT, 14, "end", "700")
    g += text(x0 + 85, 250, "hút nhau" if not down2 else "đẩy nhau", RED, 15, "middle", "700")
    return g


b = panel(10, False, "Cùng chiều") + panel(210, True, "Ngược chiều")
b += line(200, 30, 200, 240, "currentColor", 1, "3 5")
fig2 = fig("0 0 400 262",
           "Hai cặp dây dẫn thẳng song song. Bên trái hai dòng điện cùng chiều đi lên, lực từ lên mỗi dây hướng về phía dây kia: hút nhau. "
           "Bên phải hai dòng điện ngược chiều, lực từ hướng ra xa nhau: đẩy nhau. Dấu nhân cạnh dây 2 là cảm ứng từ B1 do dây 1 gây ra, hướng vào trang.",
           b, "Hình 2. Dây 1 tạo $\\vec B_1$ (×, vào trang) tại dây 2.<br>"
              "Bàn tay trái cho dây 2 ra chiều lực F.")

# ------------------------------------------------- Hình 3: khối phổ kế — proton đi nửa vòng tròn
# B hướng ra khỏi trang (⊙). Proton vào khe đi lên (+y); ở đỉnh quỹ đạo v = +x, f = q v × B = x̂ × ẑ = −ŷ: về tâm ✓ (quay theo chiều kim đồng hồ).
R = 90
kx, py = 110, 220
ccx = kx + R
b = ""
for gx in range(80, 361, 56):
    for gy in range(62, 200, 46):
        if abs(((gx - ccx) ** 2 + (gy - py) ** 2) ** 0.5 - R) < 22 or (abs(gx - ccx) < 30 and abs(gy - py) < 40):
            continue
        b += ra(gx, gy, 7, BLUE, 1.6)
b += f'<rect x="60" y="40" width="310" height="180" fill="none" stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="3 4"/>'
b += text(352, 60, "B", BTXT, 16, "end", "700")
b += line(40, py, 380, py, "currentColor", 4)                        # phim
b += text(380, py + 22, "phim", "currentColor", 14, "end", "600")
b += f'<path d="M{kx},{py} A{R},{R} 0 0 1 {kx + 2 * R},{py}" fill="none" stroke="currentColor" stroke-width="2.2" stroke-dasharray="7 5"/>'
b += chevron(ccx, py - R, 1, 0, "currentColor", 2.2, 11)
b += f'<rect x="{kx - 9}" y="{py - 3}" width="18" height="7" fill="var(--surface, #fff)" stroke="none"/>'   # khe hở trên phim
b += line(kx, py + 50, kx, py + 4, ORG, 1.6, "4 3")
b += text(kx - 12, py + 44, "U", OTXT, 15, "end", "700")
b += f'<circle cx="{ccx}" cy="{py - R}" r="10" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2"/>'
b += text(ccx, py - R + 5, "+", "currentColor", 15, "middle", "800")
b += arrow("f3", "g", ccx + 12, py - R, ccx + 64, py - R, 3)
b += text(ccx + 70, py - R + 5, "v", GRN, 16, "start", "700")
b += arrow("f3", "r", ccx, py - R + 12, ccx, py - R + 56, 3)
b += text(ccx - 8, py - R + 50, "f", RED, 16, "end", "700")
b += line(kx, py + 26, kx + 2 * R, py + 26, "currentColor", 1.4)
b += line(kx, py + 18, kx, py + 34, "currentColor", 1.4) + line(kx + 2 * R, py + 18, kx + 2 * R, py + 34, "currentColor", 1.4)
b += text(ccx, py + 46, "d = 2R", "currentColor", 15, "middle", "700")
b += text(kx + 10, py - 8, "khe", "currentColor", 13, "start", "600")
fig3 = fig("0 0 400 280",
           "Khối phổ kế: proton được tăng tốc qua hiệu điện thế U, đi qua khe vào vùng từ trường đều hướng ra khỏi trang, "
           "chuyển động nửa vòng tròn rồi đập vào phim. Ở đỉnh quỹ đạo vận tốc hướng sang phải, lực Lorentz hướng xuống về tâm. "
           "Khoảng cách từ khe tới điểm đập bằng đường kính d = 2R.",
           b, "Hình 3. Khối phổ kế: $\\vec B$ hướng ra (⊙).<br>"
              "Lực Lorentz f luôn hướng về tâm, $\\vec v$ tiếp tuyến.<br>Điểm đập cách khe $d = 2R$.")

# ------------------------------------------------- Hình 4: thanh dẫn trượt trên hai ray
# B vào trang (−z), thanh đi sang phải ⇒ diện tích mạch tăng, từ thông (vào trang) tăng ⇒ dòng cảm ứng tạo B ra trang trong mạch
# ⇒ dòng ngược chiều kim đồng hồ ⇒ trong thanh (cạnh phải) I đi lên. Kiểm: F = I ŷ × (−ẑ) = −x̂, ngược chiều v ✓.
yt, yb, rx = 70, 200, 250
b = ""
for gx in range(95, 361, 52):
    for gy in (100, 135, 170):
        if abs(gx - rx) < 30:
            continue
        b += vao(gx, gy, 6, BLUE, 1.8)
b += text(372, 100, "B", BTXT, 16, "end", "700")
b += line(40, yt, 380, yt, "currentColor", 3) + line(40, yb, 380, yb, "currentColor", 3)
b += line(40, yt, 40, 110, "currentColor", 3) + line(40, 160, 40, yb, "currentColor", 3)
b += f'<rect x="30" y="110" width="20" height="50" rx="3" fill="var(--surface, #fff)" stroke="currentColor" stroke-width="2.5"/>'
b += text(58, 140, "R", "currentColor", 16, "start", "700")
b += f'<rect x="{rx - 6}" y="{yt - 12}" width="12" height="{yb - yt + 24}" rx="3" fill="#94a3b8" stroke="currentColor" stroke-width="2"/>'
b += arrow("f4", "o", rx + 22, 175, rx + 22, 95, 3)
b += text(rx + 30, 112, "I", OTXT, 16, "start", "700")
b += arrow("f4", "g", rx, yt - 30, rx + 60, yt - 30, 3)
b += text(rx + 66, yt - 25, "v", GRN, 16, "start", "700")
b += arrow("f4", "r", rx - 8, 135, rx - 62, 135, 3)
b += text(rx - 66, 130, "F", RED, 16, "end", "700")
b += line(rx - 36, yt, rx - 36, yb, "currentColor", 1.2, "3 3")
b += text(rx - 42, 182, "ℓ", "currentColor", 16, "end", "700")
b += arrow("f4", "o", 120, yt + 10, 90, yt + 10, 2)        # dòng chạy về R ở ray trên
b += arrow("f4", "o", 90, yb - 10, 120, yb - 10, 2)        # và trở lại ở ray dưới
fig4 = fig("0 0 400 230",
           "Thanh kim loại trượt sang phải trên hai ray song song nối với điện trở R, trong từ trường đều hướng vào trang. "
           "Dòng điện cảm ứng trong thanh đi lên, chạy ngược chiều kim đồng hồ quanh mạch. Lực từ F lên thanh hướng sang trái, ngược chiều vận tốc.",
           b, "Hình 4. Thanh trượt sang phải, $\\vec B$ vào trang (×).<br>"
              "Dòng cảm ứng I đi lên trong thanh.<br>Lực từ F ngược chiều $\\vec v$ (Lenz).")

src = open("theory.src.html", encoding="utf8").read()
for n, f in (("1", fig1), ("2", fig2), ("3", fig3), ("4", fig4)):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(margin_figs(src))
print("ok", len(src), "bytes")
