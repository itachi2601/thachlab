"""Sinh 4 hình SVG cho bài Sóng dừng (Vật lí 11) và thay các mốc <!--FIGn--> trong theory.src.html.
Chạy: python3 build_figs.py   (từ thư mục bài)
"""
import math, pathlib, sys
# Thư viện chung (arrow đầu V 30°), không dùng bản svg_lib.py cũ trong thư mục bài
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *

def poly(pts, c, w=2.2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline fill="none" stroke="{c}" stroke-width="{w}"{d} opacity="{op}" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>'

def dot(x, y, r=4.5, c="currentColor"): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'

def seg(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

def sine(x0, x1, y0, amp, period, step=4):
    return [(x, y0 - amp * math.sin(2 * math.pi * (x - x0) / period)) for x in range(int(x0), int(x1) + 1, step)]

# ---------------- Hình 1: dây đàn buông (1 bó) và bấm phím giữa dây (vẫn 1 bó, đoạn rung còn nửa)
# Vẽ lại 30/10/2026: chữ 14 (trước 13), nhãn "đầu cố định" hai đầu, mỗi ý một dòng.
b = ""
# (a) dây buông, hai đầu cố định, 1 bó: đoạn rung 30→410 (380 px) = λ/2 → chu kì vẽ 760
b += text(20, 18, "Dây buông: đoạn rung dài, 1 bó → nốt thấp", "currentColor", 14, "start")
b += seg(30, 38, 30, 102, "currentColor", 3) + seg(410, 38, 410, 102, "currentColor", 3)
b += poly(sine(30, 410, 70, 30, 760), GRN, 2.6)
b += poly(sine(30, 410, 70, -30, 760), GRN, 1.6, "5 4", .5)
b += dot(30, 70, 4) + dot(410, 70, 4)
b += text(20, 122, "đầu cố định", "currentColor", 14, "start", "400")
b += text(420, 122, "đầu cố định", "currentColor", 14, "end", "400")
# (b) bấm đúng giữa dây (phím 12): đoạn rung 30→220 (190 px) = λ'/2 → chu kì vẽ 380 = 760/2
b += text(20, 154, "Bấm giữa dây (phím 12): đoạn rung còn nửa,", "currentColor", 14, "start")
b += text(20, 173, "vẫn 1 bó → nốt cao hơn", "currentColor", 14, "start")
b += seg(30, 186, 30, 250, "currentColor", 3)
b += seg(220, 186, 220, 250, "currentColor", 2.5)
b += poly(sine(30, 220, 218, 28, 380), GRN, 2.6)
b += poly(sine(30, 220, 218, -28, 380), GRN, 1.6, "5 4", .5)
b += seg(220, 218, 410, 218, "currentColor", 1.4, "3 3", .35)
b += dot(30, 218, 4) + dot(220, 218, 5, ORG)
b += text(230, 206, "ngón bấm ở giữa dây", ORG, 14, "start", "700")
b += text(320, 240, "đoạn không rung", "currentColor", 14, "middle", "400")
fig1 = wrap("0 0 440 256",
            "Dây đàn buông rung thành 1 bó; bấm phím ở giữa dây cho đoạn rung ngắn còn một nửa, vẫn 1 bó nên tần số gấp đôi",
            b,
            "Hình 1. Bấm phím ở giữa dây làm đoạn rung <strong>ngắn còn một nửa</strong>.<br>Vẫn một bó sóng nhưng bước sóng giảm một nửa, nên tần số tăng gấp đôi.<br>Nốt cao hơn một quãng tám.")
fig1 = fig1.replace('<figure class="fig" data-tl="1">',
                    '<figure class="fig" data-tl="1" data-exp="tn-l11-songdung-04">', 1)

# Ảnh OpenStax College Physics 2e (28/10/2026): thay SVG Hình 2, xem nguon.md
fig2 = (
    '<figure class="fig"><img src="/assets/openstax/l11-song-dung/hinh-song-dung-hai-song-nguoc-chieu.webp" alt="Hai sóng ngược chiều (Wave 1 sang trái, Wave 2 sang phải) và tổng của chúng ở năm thời điểm từ 0 đến T: tổng là sóng dừng, tại các nút luôn bằng 0" loading="lazy" width="975" height="395">'
    '<figcaption>Hình 2. Wave 1, 2 ngược chiều cộng thành sóng dừng (Resultant); t: thời điểm.<br>Nút–nút: λ/2; nút–bụng: λ/4.<br>'
    + '<small>Hình: OpenStax, College Physics 2e, Hình 16.36 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small>' + '</figcaption></figure>')

# ---------------- Hình 3: hai trường hợp điều kiện
# Vẽ lại 30/10/2026: chữ 14, tách tiêu đề thành 2 dòng (bỏ nối "·"), vòng đầu tự do nằm trên cọc.
b = ""
# (a) hai đầu cố định, l = 400 px = 3·λ/2 → λ = 266,7; nút cách 133,3; bụng xen kẽ trên/dưới
b += text(20, 18, "Hai đầu cố định: 3 bó", "currentColor", 14, "start")
b += text(20, 37, "4 nút (chấm đen), 3 bụng (chấm cam)", "currentColor", 14, "start", "400")
ya = 92
b += seg(20, ya - 40, 420, ya - 40, "currentColor", 1, "3 3", .3) + seg(20, ya + 40, 420, ya + 40, "currentColor", 1, "3 3", .3)
b += poly(sine(20, 420, ya, 40, 266.7), GRN, 2.4)
b += seg(20, ya - 25, 20, ya + 25, "currentColor", 3) + seg(420, ya - 25, 420, ya + 25, "currentColor", 3)
for k in range(4):
    b += dot(20 + k * 133.3, ya, 4.5)
for k in range(3):
    b += dot(20 + 66.7 + k * 133.3, ya - 40 if k % 2 == 0 else ya + 40, 5, ORG)
b += text(20, ya + 62, "l = 3·λ/2", GRN, 14, "start", "700")
# (b) một đầu cố định (x=20), đầu tự do (x=410) trên cọc: l = 390 px = 3·λ/4 → λ = 520
# nút: 20 và 20+λ/2 = 280; bụng: 20+λ/4 = 150 (trên) và 410 (dưới, đầu tự do)
yb = 262
b += text(20, 190, "Một đầu cố định, một đầu tự do:", "currentColor", 14, "start")
b += text(20, 209, "2 nút, 2 bụng", "currentColor", 14, "start", "400")
b += seg(20, yb - 40, 410, yb - 40, "currentColor", 1, "3 3", .3) + seg(20, yb + 40, 410, yb + 40, "currentColor", 1, "3 3", .3)
b += poly(sine(20, 410, yb, 40, 520, 2), RED, 2.4)
b += seg(20, yb - 25, 20, yb + 25, "currentColor", 3)
b += dot(20, yb, 4.5) + dot(280, yb, 4.5) + dot(150, yb - 40, 5, ORG)
b += seg(410, yb - 50, 410, yb + 52, "currentColor", 2.4, "", .6)
b += f'<circle cx="410" cy="{yb + 40}" r="8" fill="none" stroke="{ORG}" stroke-width="2.2"/>' + dot(410, yb + 40, 4, ORG)
b += text(398, yb + 70, "đầu tự do = bụng", ORG, 14, "end", "700")
b += text(20, yb + 70, "l = 3·λ/4", RED, 14, "start", "700")
fig3 = wrap("0 0 440 342",
            "Hai trường hợp sóng dừng: hai đầu cố định chiều dài bằng số nguyên lần λ/2; một đầu tự do chiều dài bằng số lẻ lần λ/4",
            b,
            "Hình 3. Trên: hai đầu cố định, dây có 3 bó (l = 3·λ/2).<br>Dưới: một đầu cố định, một đầu tự do, đầu tự do là bụng (l&nbsp;=&nbsp;3·λ/4).<br>Đây là k = 1 trong l = (2k+1)·λ/4.")

# ---------------- Hình 4: đường bao biên độ
# Vẽ lại 30/10/2026: chữ 14, mũi tên đầu V (bỏ marker tam giác), nhãn không đè đường, chú giải 2A/4A mỗi ý một dòng.
axis, amp, x0, x1, per = 100, 50, 20, 420, 200     # amp 50 px ≙ 2A; nút cách per/2 = 100 px ≙ λ/2
b = ""
b += text(20, 20, "Đường bao biên độ: lớn nhất ở bụng, bằng 0 ở nút", "currentColor", 14, "start")
b += poly(sine(x0, x1, axis, amp, per, 2), BLUE, 2.4)
b += poly(sine(x0, x1, axis, -amp, per, 2), BLUE, 1.6, "5 4", .55)
b += seg(x0, axis, x1, axis, "currentColor", 1.2, "", .45)
for k in range(5):
    b += dot(x0 + k * (per // 2), axis, 4.5)
b += dot(70, axis - amp, 5, ORG) + dot(170, axis + amp, 5, ORG)
b += arrow("f4", "o", 70, axis, 70, axis - amp + 3, 2.4)
b += text(78, axis - 8, "2A", ORG, 14, "start", "700")
b += arrow("f4", "o", 170, axis, 170, axis - amp + 2, 2.4)
b += arrow("f4", "o", 170, axis, 170, axis + amp - 3, 2.4)
b += text(177, axis - 12, "4A", ORG, 14, "start", "700")
b += text(426, axis + 5, "x", "currentColor", 14, "start", "700")
yl = 176
b += seg(x0, yl - 6, x0, yl + 6, "currentColor", 1.4) + seg(x0 + per // 2, yl - 6, x0 + per // 2, yl + 6, "currentColor", 1.4) + seg(x0, yl, x0 + per // 2, yl, "currentColor", 1.4)
b += text(x0 + per // 4, yl + 22, "λ/2", "currentColor", 14, "middle", "700")
b += text(200, yl + 2, "2A: biên độ tại bụng", ORG, 14, "start", "400")
b += text(200, yl + 22, "4A: bề rộng vùng dao động", ORG, 14, "start", "400")
fig4 = wrap("0 0 440 210",
            "Đường bao biên độ của sóng dừng: bằng 0 tại nút, lớn nhất 2A tại bụng; bụng vung từ +2A tới −2A nên bề rộng là 4A",
            b,
            "Hình 4. Đường bao biên độ: tại nút biên độ bằng 0, tại bụng biên độ bằng 2A.<br>Bụng vung từ +2A xuống −2A nên <strong>bề rộng</strong> vùng dao động của bụng là 4A.")

h = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, f"thiếu mốc FIG{n}"
    h = h.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(h)
print("ok", len(h), "bytes,", h.count('<figure class="fig"'), "hình")
