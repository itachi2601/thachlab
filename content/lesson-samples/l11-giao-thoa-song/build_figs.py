"""Sinh 5 hình SVG và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html (chạy lại được)."""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import math, re
from svg_lib import *
import importlib.util as _ilu
_sp = _ilu.spec_from_file_location("_skill_svg", str(_pl.Path(__file__).resolve().parents[3] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/svg_lib.py"))
_sk = _ilu.module_from_spec(_sp); _sp.loader.exec_module(_sk)
chevron = _sk.chevron

def poly(pts, c, w=2, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline fill="none" stroke="{c}" stroke-width="{w}"{d} points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>'

def dot(x, y, r=5, c="currentColor"): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

# ---- Hình 1: hai loa, đi dọc nghe to nhỏ
b = ""
for x in (150, 290):
    b += f'<rect x="{x-12}" y="22" width="24" height="34" rx="3" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2"/>'
    b += f'<circle cx="{x}" cy="42" r="7" fill="none" stroke="currentColor" stroke-width="2"/>'
    for r in (40, 70, 100, 130, 160):
        b += f'<path d="M{x-r*.7:.0f},{56+r*.7:.0f} A{r},{r} 0 0 0 {x+r*.7:.0f},{56+r*.7:.0f}" fill="none" stroke="{BLUE}" stroke-width="1" opacity=".35"/>'
b += text(150, 18, "Loa 1", "currentColor", 12, "middle") + text(290, 18, "Loa 2", "currentColor", 12, "middle")
b += line(14, 188, 426, 188, "currentColor", 2, "", .6) + text(426, 208, "đường em đi", "currentColor", 11, "end", "400")
for x, lab in ((220, "TO"), (100, "TO"), (340, "TO")):
    b += dot(x, 188, 7, RED) + text(x, 172, lab, RED, 13, "middle", "700")
for x in (160, 280, 40, 400):
    b += dot(x, 188, 7, BLUE) + text(x, 172, "nhỏ", BLUE, 12, "middle", "700")
fig1 = wrap("0 0 440 215", "Hai loa phát cùng một âm: đi dọc trước hai loa nghe to rồi nhỏ xen kẽ",
            b, "Hình 1. Hai loa cùng phát một âm. Đi dọc đường, tiếng <strong>to – nhỏ xen kẽ</strong> và các vị trí đó cố định.")

# ---- Hình 2: vân giao thoa hypebol (AB = 4λ)
lam, c, cx, cy = 36, 72, 220, 125
b = ""
def hyp(a, sign, col, dash):
    bb = math.sqrt(c * c - a * a)
    pts = [(cx + sign * a * math.sqrt(1 + (y / bb) ** 2), cy + y) for y in range(-105, 106, 5)]
    return poly(pts, col, 2.2, dash)
b += line(cx, cy - 105, cx, cy + 105, RED, 2.4)
for k in (1, 2, 3):
    for s in (-1, 1): b += hyp(k * lam / 2, s, RED, "")
for k in range(4):
    for s in (-1, 1): b += hyp((k + .5) * lam / 2, s, BLUE, "6 4")
b += line(cx - c, cy, cx + c, cy, "currentColor", 1.2, "2 3", .5)
b += dot(cx - c, cy, 6, ORG) + dot(cx + c, cy, 6, ORG)
b += text(cx - c - 16, cy + 5, "A", "currentColor", 15, "middle", "700") + text(cx + c + 16, cy + 5, "B", "currentColor", 15, "middle", "700")
b += text(cx, 14, "k = 0", RED, 14, "middle", "700")
# chú giải: mỗi mục một mẫu nét riêng
b += line(16, 262, 40, 262, RED, 2.4) + text(46, 267, "cực đại", RED, 14, "start", "700")
b += line(160, 262, 184, 262, BLUE, 2.2, "6 4") + text(190, 267, "cực tiểu", BLUE, 14, "start", "700")
b += dot(312, 262, 6, ORG) + text(324, 267, "nguồn A, B", ORG, 14, "start", "700")
fig2 = wrap("0 0 440 278", "Hai nguồn cùng pha A, B: các đường cực đại (đỏ, liền) và cực tiểu (xanh, đứt) xen kẽ dạng hypebol",
            b, "Hình 2. AB = 4λ: có 7 đường cực đại và 8 đường cực tiểu.<br>Đường trung trực của AB là cực đại k = 0.")

# ---------------- Hình 3: ảnh OpenStax College Physics 2e, Hình 27.11 (28/10/2026) — thay SVG tự vẽ
fig3 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l11-giao-thoa-song/hinh-cung-pha-nguoc-pha.webp" '
        'alt="Hai sóng cộng lại: (a) cùng pha thì sóng tổng có biên độ 2X; (b) ngược pha thì sóng tổng bằng 0" loading="lazy" width="750" height="1025">'
        '<figcaption>Hình 3. Hai sóng cộng lại thành sóng tổng.<br>(a) Cùng pha: biên độ gấp đôi.<br>(b) Ngược pha: triệt tiêu.<br>Nhãn: Wave = sóng.<br>Resultant = sóng tổng.<br><small>Hình: OpenStax, College Physics 2e, Hình 27.11 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>')

# ---- Hình 4: khe Young (vẽ lại 30/10/2026: chữ ≥ 14, D hai đầu V, thêm nhãn màn)
XS, XM, YC, I = 140, 360, 112, 26          # x hai khe, x màn, y vân trung tâm, khoảng vân (px)
S1, S2 = YC - 20, YC + 20                  # hai khe đối xứng qua vân trung tâm
b = ""
for y0, y1 in ((28, S1 - 6), (S1 + 6, S2 - 6), (S2 + 6, 196)):
    b += line(XS, y0, XS, y1, "currentColor", 4)
b += text(XS, 18, "hai khe", "currentColor", 14, "middle")
b += line(XM, 28, XM, 196, "currentColor", 3) + text(XM, 18, "màn", "currentColor", 14, "middle")
b += dot(40, YC, 6, ORG) + text(40, YC + 26, "nguồn", ORG, 14, "middle")
b += line(46, YC, XS - 4, S1, ORG, 1.4, "", .7) + line(46, YC, XS - 4, S2, ORG, 1.4, "", .7)
b += line(XS, S1, XM, YC, "currentColor", 1.2, "3 3", .6) + line(XS, S2, XM, YC, "currentColor", 1.2, "3 3", .6)
for k in range(-3, 4):
    b += f'<rect x="{XM-7}" y="{YC + k*I - 5}" width="14" height="10" rx="2" fill="{ORG}"/>'
b += text(XM + 16, YC + 5, "k = 0", ORG, 14, "start", "700")
b += text(XM + 16, YC + I + 5, "k = 1", ORG, 14, "start", "700") + text(XM + 16, YC - I + 5, "k = −1", ORG, 14, "start", "700")
# khoảng vân i: từ vân k = 1 đến k = 2 (tránh chỗ hai tia đứt hội tụ ở vân 0)
Y1, Y2 = YC + I, YC + 2 * I
b += line(XM - 16, Y1, XM - 16, Y2, "currentColor", 1.6) + line(XM - 21, Y1, XM - 11, Y1, "currentColor", 1.6) + line(XM - 21, Y2, XM - 11, Y2, "currentColor", 1.6)
b += text(XM - 26, (Y1 + Y2) / 2 + 5, "i", "currentColor", 15, "end", "700")
# khoảng cách hai khe a
b += line(XS - 14, S1, XS - 14, S2, "currentColor", 1.6) + line(XS - 19, S1, XS - 9, S1, "currentColor", 1.6) + line(XS - 19, S2, XS - 9, S2, "currentColor", 1.6)
b += text(XS - 22, YC + 5, "a", "currentColor", 15, "end", "700")
# D: từ hai khe đến màn, hai đầu V
b += line(XS, 202, XS, 222, "currentColor", 1, "", .6) + line(XM, 202, XM, 222, "currentColor", 1, "", .6)
b += line(XS + 2, 216, XM - 2, 216, GRN, 2) + chevron(XS + 2, 216, -1, 0, GRN, 2) + chevron(XM - 2, 216, 1, 0, GRN, 2)
b += text((XS + XM) / 2, 210, "D", GRN, 15, "middle", "700")
fig4 = wrap("0 0 440 232", "Sơ đồ khe Young: hai khe cách nhau a, màn cách khe D, khoảng vân i",
            b, "Hình 4. a: khoảng cách hai khe.<br>D: từ hai khe đến màn.<br>i: khoảng cách hai vân sáng liên tiếp.<br>Ô cam: vân sáng.")

# ---- Hình 5: đếm cực trị trên AB (AB = 10 cm, λ = 1,5 cm)
x0, x1 = 20, 420
mid, step = 220, 30
b = line(x0, 70, x1, 70, "currentColor", 2.5)
b += dot(x0, 70, 6, ORG) + dot(x1, 70, 6, ORG) + text(x0, 124, "A", "currentColor", 15, "middle", "700") + text(x1, 124, "B", "currentColor", 15, "middle", "700")
for k in range(-6, 7):
    x = mid + k * step
    b += line(x, 40, x, 70, RED, 3)
for k in range(-7, 7):
    x = mid + (2 * k + 1) * step / 2
    b += line(x, 70, x, 98, BLUE, 3)
b += text(mid, 30, "k = 0", RED, 14, "middle", "700") + text(mid + 6 * step, 30, "k = 6", RED, 14, "middle", "700") + text(mid - 6 * step, 30, "k = −6", RED, 14, "middle", "700")
b += line(mid, 112, mid + step, 112, GRN, 2) + line(mid, 106, mid, 118, GRN, 2) + line(mid + step, 106, mid + step, 118, GRN, 2) + text(mid + step / 2, 134, "λ/2", GRN, 14, "middle", "700")
b += f'<rect x="20" y="158" width="5" height="16" fill="{RED}"/>' + text(32, 172, "13 cực đại", RED, 14, "start", "700")
b += f'<rect x="180" y="158" width="5" height="16" fill="{BLUE}"/>' + text(192, 172, "14 cực tiểu", BLUE, 14, "start", "700")
fig5 = wrap("0 0 440 184", "Trên đoạn AB = 10 cm, λ = 1,5 cm có 13 cực đại (đỏ) và 14 cực tiểu (xanh)",
            b, "Hình 6. AB = 10 cm, λ = 1,5 cm.<br>Cực đại (đỏ) và cực tiểu (xanh) xen kẽ, cách nhau λ/4.<br>Hai cực đại liên tiếp cách nhau λ/2.")

# ---- Ảnh OpenStax College Physics 2e đợt 2 (28/10/2026): Hình 16.41 thay Hình 1 (đặt sau câu dự đoán), Hình 27.15 thêm làm Hình 5
fig1 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l11-giao-thoa-song/hinh-hai-loa-cuc-dai.webp" '
        'alt="Hai loa trong phòng: vùng nén (nét liền) và vùng dãn (nét đứt) của hai sóng chồng lên nhau; các chấm đỏ là chỗ hai sóng cùng nhịp" '
        'loading="lazy" width="400" height="252" style="max-width:100%;height:auto">'
        '<figcaption>Hình 1. Hai loa trong phòng. Chấm đỏ: nghe to.<br>Nhãn: Compression = vùng nén.<br>Rarefaction = vùng dãn.<br>'
        '<small>Hình: OpenStax, College Physics 2e, Hình 16.41 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>')
fig4b = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l11-giao-thoa-song/hinh-khe-young-cuong-do.webp" '
         'alt="Hai khe cách nhau d, màn cách khe một đoạn x; đồ thị cường độ có các cực đại giảm dần ra xa vân giữa, bên phải là ảnh các vân sáng tối thật" '
         'loading="lazy" width="875" height="521" style="max-width:100%;height:auto">'
         '<figcaption>Hình 5. Vân thật (phải) và đồ thị cường độ (giữa).<br>Sách ghi d = a, x = D, y = toạ độ vân.<br>Vân càng xa vân giữa càng mờ.<br>'
         '<small>Hình: OpenStax, College Physics 2e, Hình 27.15 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>')

h = open("theory.src.html", encoding="utf8").read()
for n, f in enumerate((fig1, fig2, fig3, fig4, fig4b, fig5), 1):
    key = "<!--FIG4B-->" if n == 5 else f"<!--FIG{6 if n == 6 else n}-->"
    assert key in h, key
    h = h.replace(key, f)
out = margin_figs(h)
if 'tl-fn-h5' in out and 'href="#tl-fn-h5"' not in out:
    out = out.replace('<figure class="fig" data-tl="1"><img src="/assets/openstax/l11-giao-thoa-song/hinh-khe-young-cuong-do.webp"',
                      '<p class="tl-figlead">Quan sát Hình 5 dưới đây.<sup class="tl-fn"><a href="#tl-fn-h5">H5</a></sup></p>\n<figure class="fig" data-tl="1"><img src="/assets/openstax/l11-giao-thoa-song/hinh-khe-young-cuong-do.webp"', 1)
open("theory.html", "w", encoding="utf8").write(out)
print("ok", len(h))
