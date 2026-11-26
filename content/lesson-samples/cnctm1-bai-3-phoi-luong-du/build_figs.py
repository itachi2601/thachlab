#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 1 – Bài 3 (Phôi và lượng dư), thay <!--FIGn--> trong theory.src.html → theory.html.
Dùng: python3 build_figs.py  (chạy lại an toàn: luôn đọc từ theory.src.html)
Mọi hình là sơ đồ nguyên lý tự vẽ, không theo tỉ lệ.
"""
import math
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
FONT = 'font-family="system-ui, sans-serif" font-size="13"'
RED = "#dc2626"
ORANGE = "#ea580c"
BLUE = "#0284c7"
SAND = "#d6b98c"
GREY = "#94a3b8"
DEFS = ('<defs><marker id="b3{p}-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
        'orient="auto-start-reverse"><path d="M1 1 L9 5 L1 9" fill="none" stroke="currentColor" stroke-width="1.6"/>'
        '</marker></defs>')


def fig(svg, cap):
    return f'<figure class="fig" data-tl="1">{svg}<figcaption>{cap}</figcaption></figure>'


def svg_open(w, h, label, p):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" {FONT}>'
            + DEFS.format(p=p))


def t(x, y, s, extra=""):
    return f'<text x="{x}" y="{y}" fill="currentColor" font-size="12"{extra}>{s}</text>'


# Hình 1: sơ đồ cán — hai trục quay ngược chiều, phôi dày vào, sản phẩm mỏng ra
def fig1():
    o = [svg_open(420, 250, "Sơ đồ nguyên lý cán kim loại", "f1")]
    cx, cu, cl, r = 210, 70, 180, 48
    # phôi: dày 105–145 bên trái, mỏng 118–132 bên phải; cung tiếp xúc theo trục cán
    xc = cx - math.sqrt(r * r - 35 * 35)  # chỗ trục chạm mặt phôi dày
    o.append(f'<path d="M20 105 L{xc:.1f} 105 A{r} {r} 0 0 0 {cx} 118 L400 118 L400 132 L{cx} 132 '
             f'A{r} {r} 0 0 0 {xc:.1f} 145 L20 145 Z" fill="{ORANGE}" fill-opacity=".25" stroke="{ORANGE}" stroke-width="2"/>')
    for cy in (cu, cl):
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{GREY}" fill-opacity=".35" stroke="currentColor" stroke-width="2"/>')
        o.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="currentColor"/>')
    # chiều quay: trục trên ngược kim đồng hồ (đáy chạy sang phải), trục dưới thuận kim đồng hồ
    R = 58
    a = math.radians(30)
    x1, x2 = cx + R * math.sin(a), cx - R * math.sin(a)
    yu = cu - R * math.cos(a)
    yl = cl + R * math.cos(a)
    o.append(f'<path d="M{x1:.1f} {yu:.1f} A{R} {R} 0 0 0 {x2:.1f} {yu:.1f}" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#b3f1-ar)"/>')
    o.append(f'<path d="M{x1:.1f} {yl:.1f} A{R} {R} 0 0 1 {x2:.1f} {yl:.1f}" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#b3f1-ar)"/>')
    # nhãn, mỗi ý một dòng
    o.append(t(270, 60, "trục cán trên"))
    o.append(t(270, 200, "trục cán dưới"))
    o.append(t(20, 96, "phôi dày"))
    o.append(t(268, 110, "sản phẩm mỏng, dài"))
    o.append(f'<line x1="290" y1="152" x2="390" y2="152" stroke="currentColor" stroke-width="1.6" marker-end="url(#b3f1-ar)"/>')
    o.append(t(290, 170, "chiều cán"))
    o.append('</svg>')
    return fig("".join(o), "Hình 1. Cán: hai trục quay ngược chiều kéo phôi vào khe, phôi mỏng đi và dài ra (sơ đồ, không theo tỉ lệ).")


# Hình 2: rèn tự do và rèn khuôn hở
def fig2():
    o = [svg_open(420, 205, "Rèn tự do và rèn khuôn hở", "f2")]
    o.append('<text x="20" y="18" fill="currentColor" font-weight="700">Rèn tự do</text>')
    o.append('<text x="225" y="18" fill="currentColor" font-weight="700">Rèn khuôn hở</text>')
    # trái: búa – vật rèn – đe
    o.append('<line x1="75" y1="26" x2="75" y2="48" stroke="currentColor" stroke-width="1.8" marker-end="url(#b3f2-ar)"/>')
    o.append(f'<rect x="30" y="52" width="90" height="28" fill="{GREY}" fill-opacity=".45" stroke="currentColor" stroke-width="2"/>')
    o.append(f'<path d="M45 84 L105 84 Q115 103 105 122 L45 122 Q35 103 45 84 Z" fill="{ORANGE}" fill-opacity=".35" stroke="{ORANGE}" stroke-width="2"/>')
    o.append(f'<path d="M25 124 L125 124 L140 164 L10 164 Z" fill="{GREY}" fill-opacity=".45" stroke="currentColor" stroke-width="2"/>')
    o.append(t(128, 70, "búa"))
    o.append(t(122, 107, "vật rèn"))
    o.append(t(148, 152, "đe"))
    o.append(t(20, 190, "Mặt đe phẳng, kim loại tự do."))
    # phải: khuôn trên, khuôn dưới, vật rèn trong lòng khuôn, vành biên tràn ra mặt phân khuôn
    o.append(f'<path d="M225 46 L380 46 L380 96 L350 96 L350 71 L280 71 L280 96 L225 96 Z" fill="{GREY}" fill-opacity=".45" stroke="currentColor" stroke-width="2"/>')
    o.append(f'<path d="M225 104 L280 104 L280 129 L350 129 L350 104 L380 104 L380 154 L225 154 Z" fill="{GREY}" fill-opacity=".45" stroke="currentColor" stroke-width="2"/>')
    o.append(f'<path d="M280 71 L350 71 L350 97 L395 97 L395 103 L350 103 L350 129 L280 129 L280 103 L250 103 L250 97 L280 97 Z" fill="{ORANGE}" fill-opacity=".45" stroke="{ORANGE}" stroke-width="1.6"/>')
    o.append(t(225, 40, "khuôn trên"))
    o.append(t(225, 172, "khuôn dưới"))
    o.append('<line x1="395" y1="104" x2="395" y2="178" stroke="currentColor" stroke-width="1"/>')
    o.append(t(412, 192, "vành biên", ' text-anchor="end"'))
    o.append('</svg>')
    return fig("".join(o), "Hình 2. Rèn tự do chỉ có búa và đe; rèn khuôn ép kim loại đầy lòng khuôn, phần thừa tràn ra thành vành biên.")


# Hình 3: mặt cắt khuôn cát đúc bạc (ống lót)
def fig3():
    o = [svg_open(420, 205, "Mặt cắt khuôn cát", "f3")]
    # hai hòm khuôn
    o.append(f'<rect x="20" y="30" width="260" height="80" fill="{SAND}" fill-opacity=".4" stroke="currentColor" stroke-width="2"/>')
    o.append(f'<rect x="20" y="110" width="260" height="80" fill="{SAND}" fill-opacity=".4" stroke="currentColor" stroke-width="2"/>')
    # kim loại: lòng khuôn (trừ lõi), rãnh dẫn, đậu rót, đậu ngót
    m = f'fill="{RED}" fill-opacity=".75" stroke="{RED}" stroke-width="1"'
    o.append(f'<rect x="90" y="80" width="50" height="60" {m}/>')
    o.append(f'<rect x="180" y="80" width="50" height="60" {m}/>')
    o.append(f'<rect x="45" y="30" width="12" height="82" {m}/>')
    o.append(f'<rect x="45" y="104" width="45" height="8" {m}/>')
    o.append(f'<rect x="200" y="30" width="22" height="50" {m}/>')
    # cốc rót
    o.append('<path d="M33 16 L69 16 L57 30 L45 30 Z" fill="none" stroke="currentColor" stroke-width="2"/>')
    # lõi cát (có gối lõi cắm vào cát hai hòm)
    o.append('<rect x="140" y="62" width="40" height="96" fill="#78716c" fill-opacity=".55" stroke="currentColor" stroke-width="1.6"/>')
    # mặt phân khuôn (nét đứt)
    o.append('<line x1="10" y1="110" x2="285" y2="110" stroke="currentColor" stroke-width="1.4" stroke-dasharray="6 4"/>')
    # nhãn bên phải + đường dẫn
    L = [(44, 222, 44, "đậu ngót"), (66, 280, 66, "hòm khuôn trên"), (92, 230, 92, "vật đúc (kim loại)"),
         (114, 285, 110, "mặt phân khuôn"), (136, 180, 155, "lõi cát"), (176, 280, 176, "hòm khuôn dưới")]
    for ty, px, py, s in L:
        o.append(f'<line x1="{px}" y1="{py}" x2="286" y2="{ty - 4}" stroke="currentColor" stroke-width="1"/>')
        o.append(t(290, ty, s))
    o.append(t(74, 14, "đậu rót"))
    o.append('</svg>')
    return fig("".join(o), "Hình 3. Mặt cắt khuôn cát đúc một ống lót: kim loại rót qua đậu rót, điền đầy lòng khuôn quanh lõi cát; đậu ngót bù co ngót khi nguội.")


# Hình 4: lượng dư trung gian — mặt phẳng (một phía) và trục (đối xứng)
def fig4():
    o = [svg_open(420, 225, "Lượng dư trung gian mặt phẳng và trục", "f4")]
    o.append('<text x="20" y="20" fill="currentColor" font-weight="700">Mặt phẳng: Z = a − b</text>')
    o.append('<text x="232" y="20" fill="currentColor" font-weight="700">Trục: 2Z = d₁ − d₂</text>')
    # trái
    o.append(f'<rect x="40" y="60" width="110" height="25" fill="{ORANGE}" fill-opacity=".35" stroke="{ORANGE}" stroke-width="1.4" stroke-dasharray="5 3"/>')
    o.append(f'<rect x="40" y="85" width="110" height="95" fill="{GREY}" fill-opacity=".3" stroke="currentColor" stroke-width="2"/>')
    o.append('<line x1="25" y1="180" x2="205" y2="180" stroke="currentColor" stroke-width="1.6"/>')
    o.append(t(88, 78, "Z", ' font-weight="700"'))
    for x, y, s in ((170, 60, "a"), (192, 85, "b")):
        o.append(f'<line x1="{x}" y1="178" x2="{x}" y2="{y + 2}" stroke="currentColor" stroke-width="1.2" marker-start="url(#b3f4-ar)" marker-end="url(#b3f4-ar)"/>')
        o.append(f'<line x1="150" y1="{y}" x2="{x + 6}" y2="{y}" stroke="currentColor" stroke-width=".8"/>')
        o.append(t(x + 4, 140, s))
    o.append(t(20, 205, "a: trước · b: sau bước"))
    # phải: hai vòng tròn
    cx, cy = 310, 115
    o.append(f'<circle cx="{cx}" cy="{cy}" r="70" fill="{ORANGE}" fill-opacity=".35" stroke="{ORANGE}" stroke-width="1.4" stroke-dasharray="5 3"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="52" fill="{GREY}" fill-opacity=".45" stroke="currentColor" stroke-width="2"/>')
    o.append(f'<line x1="{cx - 52}" y1="{cy}" x2="{cx + 52}" y2="{cy}" stroke="currentColor" stroke-width="1.2" marker-start="url(#b3f4-ar)" marker-end="url(#b3f4-ar)"/>')
    o.append(t(cx - 6, cy - 8, "d₂"))
    o.append(t(cx - 66, cy + 5, "Z", ' font-weight="700"'))
    o.append(t(cx + 56, cy + 5, "Z", ' font-weight="700"'))
    o.append(f'<line x1="{cx - 70}" y1="200" x2="{cx + 70}" y2="200" stroke="currentColor" stroke-width="1.2" marker-start="url(#b3f4-ar)" marker-end="url(#b3f4-ar)"/>')
    for x in (cx - 70, cx + 70):
        o.append(f'<line x1="{x}" y1="{cy}" x2="{x}" y2="206" stroke="currentColor" stroke-width=".8"/>')
    o.append(t(cx - 6, 218, "d₁"))
    o.append('</svg>')
    return fig("".join(o), "Hình 4. Vùng tô cam là lượng dư Z của một bước. Mặt phẳng hớt một phía; trục hớt cả hai phía nên hiệu đường kính bằng 2Z.")


# Hình 5: lỗ tâm 60° ở đầu trục, mũi tâm máy tiện tì vào (mặt cắt)
def fig5():
    o = [svg_open(420, 210, "Lỗ tâm và mũi tâm", "f5")]
    k = math.tan(math.radians(30))
    ax, cy = 202, 120  # đỉnh côn 60°
    xp = 150 + (30 - 6) / k  # chỗ côn gặp lỗ dẫn r = 6
    # phôi trục (mặt cắt) trừ lỗ tâm
    o.append(f'<path d="M150 50 L400 50 L400 190 L150 190 L150 150 L{xp:.1f} {cy + 6} L215 {cy + 6} L215 {cy - 6} L{xp:.1f} {cy - 6} L150 90 Z" '
             f'fill="{GREY}" fill-opacity=".35" stroke="currentColor" stroke-width="2"/>')
    # mũi tâm: thân trụ + côn 60°, đầu cắt bằng tại x = 186
    xt = 186
    rt = (ax - xt) * k
    rb = (ax - 120) * k
    o.append(f'<path d="M40 {cy - rb:.1f} L120 {cy - rb:.1f} L{xt} {cy - rt:.1f} L{xt} {cy + rt:.1f} L120 {cy + rb:.1f} L40 {cy + rb:.1f} Z" '
             f'fill="{BLUE}" fill-opacity=".3" stroke="{BLUE}" stroke-width="2"/>')
    o.append(f'<line x1="20" y1="{cy}" x2="410" y2="{cy}" stroke="currentColor" stroke-width=".9" stroke-dasharray="10 3 2 3"/>')
    o.append(t(40, cy - rb - 8, "mũi tâm máy tiện"))
    o.append(t(300, 42, "đầu trục (mặt cắt)"))
    ys = cy - (ax - 180) * k
    o.append(f'<line x1="223" y1="92" x2="181" y2="{ys - 1:.1f}" stroke="currentColor" stroke-width="1"/>')
    o.append(t(226, 96, "lỗ tâm côn 60°"))
    o.append(t(226, 146, "lỗ dẫn nhỏ"))
    o.append(f'<line x1="224" y1="142" x2="212" y2="{cy + 6}" stroke="currentColor" stroke-width="1"/>')
    o.append('</svg>')
    return fig("".join(o), "Hình 5. Mũi tâm tì vào mặt côn 60° của lỗ tâm. Hai lỗ tâm ở hai đầu trục phải nằm trên cùng một đường tâm.")


# Hình 6: mặt cắt khối D — chi tiết (nét đậm) lồng trong phôi (nét mảnh), lượng dư phóng to
def fig6():
    o = [svg_open(420, 240, "Bản vẽ lồng phôi khối D", "f6")]
    o.append(f'<rect x="100" y="30" width="180" height="190" fill="{ORANGE}" fill-opacity=".3" stroke="{ORANGE}" stroke-width="1.4"/>')
    o.append(f'<rect x="120" y="60" width="140" height="140" fill="#cbd5e1" stroke="currentColor" stroke-width="3"/>')
    o.append(t(185, 50, "6", ' font-weight="700"'))
    o.append(t(185, 214, "4", ' font-weight="700"'))
    o.append(t(106, 135, "4", ' font-weight="700"'))
    o.append(t(266, 135, "4", ' font-weight="700"'))
    o.append(t(158, 125, "chi tiết"))
    o.append(t(150, 143, "100 × 100"))
    o.append(t(100, 20, "↑ mặt trên khi rót"))
    o.append('<line x1="292" y1="86" x2="316" y2="86" stroke="currentColor" stroke-width="3"/>')
    o.append(t(322, 90, "chi tiết"))
    o.append(f'<line x1="292" y1="110" x2="316" y2="110" stroke="{ORANGE}" stroke-width="1.4"/>')
    o.append(t(322, 114, "phôi đúc"))
    o.append(f'<rect x="292" y="128" width="24" height="12" fill="{ORANGE}" fill-opacity=".3"/>')
    o.append(t(322, 138, "lượng dư (mm)"))
    o.append('</svg>')
    return fig("".join(o), "Hình 6. Mặt cắt khối D: chi tiết lồng trong phôi đúc. Lượng dư vẽ phóng to để dễ đọc.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for i, f in enumerate((fig1, fig2, fig3, fig4, fig5, fig6), 1):
    tag = f"<!--FIG{i}-->"
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
