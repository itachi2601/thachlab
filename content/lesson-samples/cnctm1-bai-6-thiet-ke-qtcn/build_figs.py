#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 1 – Bài 6 (Thiết kế quy trình công nghệ), thay <!--FIGn--> trong theory.src.html → theory.html.
Dùng: python3 build_figs.py  (chạy lại an toàn: luôn đọc từ theory.src.html)
Số hình trong chú thích = thứ tự xuất hiện trong bài (FIG1 → FIG6 đặt đúng thứ tự trong src).
"""
import math
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
FONT = 'font-family="system-ui, sans-serif" font-size="13"'
RED, GREEN, BLUE, ORANGE = "#dc2626", "#059669", "#0284c7", "#ea580c"


def fig(svg, cap):
    return f'<figure class="fig" data-tl="1">{svg}<figcaption>{cap}</figcaption></figure>'


def svg_open(w, h, label):
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" {FONT}>'


def t(x, y, s, size=12, bold=False, color="currentColor", anchor="start"):
    fw = ' font-weight="700"' if bold else ""
    an = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}"{fw}{an}>{s}</text>'


def arrow_head(x, y, direction, color="currentColor", size=6):
    """Đầu mũi tên chevron 30° tại (x, y), hướng 'up'/'down'/'left'/'right'."""
    d = size
    w = d * math.tan(math.radians(30))
    if direction == "up":
        pts = f"M{x - w:.1f} {y + d} L{x} {y} L{x + w:.1f} {y + d}"
    elif direction == "down":
        pts = f"M{x - w:.1f} {y - d} L{x} {y} L{x + w:.1f} {y - d}"
    elif direction == "left":
        pts = f"M{x + d} {y - w:.1f} L{x} {y} L{x + d} {y + w:.1f}"
    else:
        pts = f"M{x - d} {y - w:.1f} L{x} {y} L{x - d} {y + w:.1f}"
    return f'<path d="{pts}" fill="none" stroke="{color}" stroke-width="1.5"/>'


def box(x, y, w, h, color="currentColor", fill="none", sw=1.4, rx=6):
    fo = ' fill-opacity="0.12"' if fill != "none" else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{fo} stroke="{color}" stroke-width="{sw}"/>'


# ---------------------------------------------------------------- Hình 1: tài liệu ban đầu
def fig1():
    docs = ["Bản vẽ chi tiết ★", "Bản vẽ lắp, bộ phận", "Sản lượng", "Bản vẽ phôi",
            "Thuyết minh máy", "Atlas đồ gá, catalog dao", "Sổ tay công nghệ"]
    o = [svg_open(420, 268, "Bảy tài liệu ban đầu dẫn vào quy trình công nghệ")]
    hx, hy = 290, 134  # điểm vào của khối QTCN
    for i, name in enumerate(docs):
        y = 8 + i * 36
        first = i == 0
        o.append(box(8, y, 190, 28, ORANGE if first else "currentColor", ORANGE if first else "none", 2 if first else 1.2))
        o.append(t(18, y + 19, name, 12, first, ORANGE if first else "currentColor"))
        o.append(f'<line x1="198" y1="{y + 14}" x2="{hx - 8}" y2="{hy}" stroke="currentColor" stroke-opacity="0.55" stroke-width="1.1"/>')
    o.append(arrow_head(hx - 2, hy, "right"))
    o.append(box(hx, hy - 34, 122, 68, BLUE, BLUE, 2))
    o.append(t(hx + 61, hy - 6, "Quy trình", 14, True, BLUE, "middle"))
    o.append(t(hx + 61, hy + 14, "công nghệ", 14, True, BLUE, "middle"))
    o.append(t(hx + 61, hy + 60, "★ không thể thiếu", 12, True, ORANGE, "middle"))
    o.append('</svg>')
    return fig("".join(o), "Hình 1. Bảy tài liệu ban đầu để thiết kế quy trình công nghệ. Thiếu tài liệu khác còn xoay xở được; thiếu bản vẽ chi tiết thì không.")


# ---------------------------------------------------------------- Hình 2: 12 bước
def fig2():
    phases = [("Chuẩn bị", ["1. Dạng", "sản xuất"], ["2. Phân tích", "bản vẽ"], ["3. Chọn", "phôi"]),
              ("Vạch đường", ["4. Thứ tự", "nguyên công"], ["5. Chọn", "máy"], ["6. Lượng", "dư"]),
              ("Trang bị", ["7. Dao, dụng", "cụ đo"], ["8. Chế độ", "cắt"], ["9. Đồ gá", ""]),
              ("Định mức,|ghi phiếu", ["10. Thời", "gian"], ["11. Bậc", "thợ"], ["12. Viết", "phiếu"])]
    o = [svg_open(420, 282, "Mười hai bước thiết kế quy trình công nghệ chia bốn chặng")]
    for r, (ph, *steps) in enumerate(phases):
        y = 8 + r * 68
        if "|" in ph:
            a, b = ph.split("|")
            o.append(t(8, y + 23, a, 12, True, BLUE))
            o.append(t(8, y + 41, b, 12, True, BLUE))
        else:
            o.append(t(8, y + 32, ph, 12, True, BLUE))
        for c, (l1, l2) in enumerate(steps):
            x = 108 + c * 104
            key = (r, c) == (1, 0)
            col = ORANGE if key else "currentColor"
            o.append(box(x, y, 88, 52, col, ORANGE if key else "none", 2 if key else 1.3))
            if l2:
                o.append(t(x + 44, y + 22, l1, 12, key, col, "middle"))
                o.append(t(x + 44, y + 40, l2, 12, key, col, "middle"))
            else:
                o.append(t(x + 44, y + 31, l1, 12, key, col, "middle"))
            if c < 2:
                o.append(f'<line x1="{x + 88}" y1="{y + 26}" x2="{x + 103}" y2="{y + 26}" stroke="currentColor" stroke-width="1.3"/>')
                o.append(arrow_head(x + 103, y + 26, "right", size=5))
        if r < 3:
            o.append(f'<line x1="360" y1="{y + 52}" x2="360" y2="{y + 60}" stroke="currentColor" stroke-opacity="0.5"/>')
            o.append(f'<line x1="360" y1="{y + 60}" x2="152" y2="{y + 60}" stroke="currentColor" stroke-opacity="0.5"/>')
            o.append(f'<line x1="152" y1="{y + 60}" x2="152" y2="{y + 65}" stroke="currentColor" stroke-opacity="0.5"/>')
            o.append(arrow_head(152, y + 66, "down", size=5))
    o.append('</svg>')
    return fig("".join(o), "Hình 2. Mười hai bước thiết kế quy trình công nghệ, gom thành bốn chặng. Bước 4 (thứ tự nguyên công) quyết định chất lượng của cả quy trình.")


# ---------------------------------------------------------------- Hình 3: tập trung vs phân tán
def fig3():
    steps = ["Khoả mặt", "Tiện trụ", "Khoan lỗ", "Vát mép"]
    o = [svg_open(420, 236, "Tập trung nguyên công so với phân tán nguyên công")]
    # Tập trung
    o.append(t(8, 62, "Tập trung", 13, True, BLUE))
    o.append(t(8, 80, "đơn chiếc", 12))
    o.append(t(110, 22, "1 máy, 1 nguyên công, 4 bước"))
    o.append(box(104, 32, 308, 64, BLUE, BLUE, 1.8))
    for i, s in enumerate(steps):
        x = 112 + i * 75
        o.append(box(x, 46, 66, 36, "currentColor", "none", 1.1, 4))
        o.append(t(x + 33, 68, s, 12, False, "currentColor", "middle"))
    # Phân tán
    o.append(t(8, 172, "Phân tán", 13, True, ORANGE))
    o.append(t(8, 190, "hàng loạt", 12))
    o.append(t(110, 132, "4 máy, 4 nguyên công, mỗi nguyên công 1 bước"))
    for i, s in enumerate(steps):
        x = 104 + i * 78
        o.append(box(x, 142, 66, 64, ORANGE, ORANGE, 1.6))
        o.append(t(x + 33, 164, f"Máy {i + 1}", 12, True, ORANGE, "middle"))
        o.append(t(x + 33, 190, s, 12, False, "currentColor", "middle"))
        if i < 3:
            o.append(f'<line x1="{x + 66}" y1="174" x2="{x + 77}" y2="174" stroke="currentColor" stroke-width="1.3"/>')
            o.append(arrow_head(x + 77, 174, "right", size=5))
    o.append(t(104, 228, "Chi tiết đi lần lượt qua từng máy."))
    o.append('</svg>')
    return fig("".join(o), "Hình 3. Cùng bốn bước gia công: tập trung dồn cả vào một nguyên công trên một máy; phân tán chia mỗi máy một bước.")


# ---------------------------------------------------------------- Hình 4: ba cách gá nhiều chi tiết
def fig4():
    o = [svg_open(420, 212, "Ba cách gá nhiều chi tiết: tuần tự, song song, song song – tuần tự (nhìn từ trên xuống)")]
    titles = ["Tuần tự", "Song song", "Song song–tuần tự"]
    caps = [("dao đi qua", "lần lượt từng chiếc"), ("các chiếc xong", "cùng một lúc"), ("từng cột,", "mỗi cột 3 chiếc")]
    for p in range(3):
        x0 = p * 140
        if p:
            o.append(f'<line x1="{x0}" y1="6" x2="{x0}" y2="206" stroke="currentColor" stroke-opacity="0.3"/>')
        o.append(t(x0 + 70, 20, titles[p], 12, True, BLUE, "middle"))
        parts = []
        if p == 0:
            parts = [(x0 + 40, 80), (x0 + 68, 80), (x0 + 96, 80)]
            o.append(f'<circle cx="{x0 + 18}" cy="91" r="13" fill="{ORANGE}" fill-opacity="0.2" stroke="{ORANGE}" stroke-width="1.8"/>')
        else:
            cols = [x0 + 60] if p == 1 else [x0 + 54, x0 + 90]
            parts = [(cx, cy) for cx in cols for cy in (44, 76, 108)]
            o.append(f'<rect x="{x0 + 20}" y="38" width="18" height="100" rx="8" fill="{ORANGE}" fill-opacity="0.2" stroke="{ORANGE}" stroke-width="1.8"/>')
        for (px, py) in parts:
            o.append(f'<rect x="{px}" y="{py}" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6"/>')
        o.append(f'<line x1="{x0 + 16}" y1="152" x2="{x0 + 128}" y2="152" stroke="currentColor" stroke-width="1.3"/>')
        o.append(arrow_head(x0 + 128, 152, "right"))
        o.append(t(x0 + 70, 178, caps[p][0], 12, False, "currentColor", "middle"))
        o.append(t(x0 + 70, 196, caps[p][1], 12, False, "currentColor", "middle"))
    o.append('</svg>')
    return fig("".join(o), "Hình 4. Ba cách gá nhiều chi tiết nhỏ trên một máy lớn (nhìn từ trên xuống). Ô vuông: chi tiết; màu cam: dao phay; mũi tên: hướng chạy dao.")


# ---------------------------------------------------------------- Hình 5: ba loại phiếu
def fig5():
    o = [svg_open(420, 236, "Ba loại phiếu công nghệ: tiến trình, quy trình, chỉ dẫn nguyên công")]
    cards = [("Biểu 1", "Tiến trình"), ("Biểu 2", "Quy trình"), ("Biểu 3", "Chỉ dẫn NC")]
    for i, (b, n) in enumerate(cards):
        x = 8 + i * 140
        o.append(box(x, 8, 124, 172, "currentColor", "none", 1.4, 4))
        o.append(t(x + 62, 28, b, 13, True, BLUE, "middle"))
        o.append(t(x + 62, 46, n, 12, False, "currentColor", "middle"))
        o.append(f'<line x1="{x}" y1="56" x2="{x + 124}" y2="56" stroke="currentColor" stroke-width="1"/>')
    # Biểu 1: chỉ tên nguyên công
    for j in range(4):
        y = 76 + j * 24
        o.append(t(16, y, f"NC {j + 1}", 12, True))
        o.append(f'<line x1="56" y1="{y - 4}" x2="122" y2="{y - 4}" stroke="currentColor" stroke-opacity="0.4" stroke-width="3"/>')
    # Biểu 2: nguyên công + bước
    y = 76
    for j in range(2):
        o.append(t(156, y, f"NC {j + 1}", 12, True))
        o.append(f'<line x1="196" y1="{y - 4}" x2="262" y2="{y - 4}" stroke="currentColor" stroke-opacity="0.4" stroke-width="3"/>')
        y += 20
        for k in range(2):
            o.append(t(170, y, f"bước {k + 1}", 12, False, ORANGE))
            o.append(f'<line x1="220" y1="{y - 4}" x2="262" y2="{y - 4}" stroke="{ORANGE}" stroke-opacity="0.5" stroke-width="2"/>')
            y += 18
    # Biểu 3: một nguyên công, có ô sơ đồ
    o.append(t(296, 76, "NC 3", 12, True))
    o.append(f'<rect x="296" y="86" width="108" height="54" fill="none" stroke="{RED}" stroke-width="1.6" stroke-dasharray="5 3"/>')
    o.append(t(350, 118, "sơ đồ NC", 12, True, RED, "middle"))
    for j in range(2):
        o.append(f'<line x1="296" y1="{154 + j * 14}" x2="404" y2="{154 + j * 14}" stroke="currentColor" stroke-opacity="0.4" stroke-width="3"/>')
    caps = ["khái quát", "tỉ mỉ từng bước", "mỗi NC một tờ"]
    for i, c in enumerate(caps):
        o.append(t(8 + i * 140 + 62, 202, c, 12, True, "currentColor", "middle"))
    o.append(t(8 + 0 * 140 + 62, 222, "đơn giản, ít kiểm soát", 12, False, "currentColor", "middle"))
    o.append(t(8 + 1 * 140 + 62, 222, "hàng loạt", 12, False, "currentColor", "middle"))
    o.append(t(8 + 2 * 140 + 62, 222, "loạt lớn, máy tự động", 12, False, "currentColor", "middle"))
    o.append('</svg>')
    return fig("".join(o), "Hình 5. Ba loại phiếu công nghệ: càng sang phải càng tỉ mỉ. NC: nguyên công.")


# ---------------------------------------------------------------- Hình 6: sơ đồ nguyên công
def locate(x, y, direction, n):
    """Ký hiệu định vị đơn giản hoá: chữ V có đỉnh chạm mặt chuẩn + số bậc tự do khống chế."""
    if direction == "left":   # mặt chuẩn quay sang trái, ký hiệu nằm bên trái
        p = f"M{x - 14} {y - 8} L{x} {y} L{x - 14} {y + 8}"
        lab = t(x - 26, y + 5, n, 13, True, GREEN, "middle")
    else:                     # mặt chuẩn quay lên, ký hiệu nằm phía trên
        p = f"M{x - 8} {y - 14} L{x} {y} L{x + 8} {y - 14}"
        lab = t(x, y - 20, n, 13, True, GREEN, "middle")
    return f'<path d="{p}" fill="none" stroke="{GREEN}" stroke-width="2"/>' + lab


def fig6():
    o = [svg_open(420, 262, "Sơ đồ nguyên công khoét – doa lỗ Ø22 của bạc trượt")]
    o.append('<defs><pattern id="c6-gach" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
             '<line x1="0" y1="0" x2="0" y2="7" stroke="currentColor" stroke-width="1"/></pattern></defs>')
    o.append(t(8, 20, "NC 2: khoét – doa lỗ Ø22", 13, True))
    # bạc trượt cắt dọc: thành trên và thành dưới
    for (y1, y2) in ((86, 104), (146, 164)):
        o.append(f'<rect x="150" y="{y1}" width="62" height="{y2 - y1}" fill="url(#c6-gach)" stroke="currentColor" stroke-width="1.8"/>')
    # mặt lỗ đang gia công: nét đỏ đậm
    o.append(f'<line x1="150" y1="104" x2="212" y2="104" stroke="{RED}" stroke-width="3.5"/>')
    o.append(f'<line x1="150" y1="146" x2="212" y2="146" stroke="{RED}" stroke-width="3.5"/>')
    o.append('<line x1="130" y1="125" x2="350" y2="125" stroke="currentColor" stroke-width="0.8" stroke-dasharray="10 3 2 3"/>')
    # định vị: mặt đầu 3 bậc, mặt trụ ngắn 2 bậc
    o.append(locate(150, 155, "left", "3"))
    o.append(locate(166, 86, "up", "2"))
    # kẹp chặt
    o.append(f'<line x1="196" y1="48" x2="196" y2="84" stroke="{BLUE}" stroke-width="2"/>' + arrow_head(196, 85, "down", BLUE, 7))
    o.append(t(204, 56, "W", 13, True, BLUE))
    o.append(f'<line x1="196" y1="202" x2="196" y2="166" stroke="{BLUE}" stroke-width="2"/>' + arrow_head(196, 165, "up", BLUE, 7))
    o.append(t(204, 200, "W", 13, True, BLUE))
    # dao doa đi vào từ bên phải
    o.append(f'<rect x="222" y="105" width="124" height="40" rx="3" fill="{ORANGE}" fill-opacity="0.2" stroke="{ORANGE}" stroke-width="1.8"/>')
    o.append(t(300, 98, "mũi doa", 12, True, ORANGE, "middle"))
    o.append(f'<line x1="330" y1="172" x2="262" y2="172" stroke="currentColor" stroke-width="1.4"/>' + arrow_head(262, 172, "left"))
    o.append(t(300, 190, "chạy dao S", 12, False, "currentColor", "middle"))
    # kích thước cần đạt
    o.append(f'<line x1="206" y1="104" x2="250" y2="64" stroke="{RED}" stroke-width="1"/>')
    o.append(t(252, 62, "Ø22 +0,021; Ra 1,25", 12, True, RED))
    # chú giải
    o.append(f'<path d="M14 218 L28 226 L14 234" fill="none" stroke="{GREEN}" stroke-width="2"/>')
    o.append(t(36, 230, "định vị (số: bậc tự do khống chế)"))
    o.append(f'<line x1="260" y1="226" x2="290" y2="226" stroke="{RED}" stroke-width="3.5"/>')
    o.append(t(298, 230, "mặt gia công"))
    o.append(f'<line x1="14" y1="250" x2="30" y2="250" stroke="{BLUE}" stroke-width="2"/>' + arrow_head(30, 250, "right", BLUE))
    o.append(t(36, 254, "W: lực kẹp"))
    o.append('</svg>')
    return fig("".join(o), "Hình 6. Sơ đồ nguyên công khoét – doa lỗ bạc trượt (ký hiệu đơn giản hoá; ký hiệu chuẩn tra bảng ký hiệu định vị – kẹp chặt). Thợ nhìn sơ đồ là biết gá thế nào, dao ở đâu, cần đạt gì.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
FIGS = (fig1, fig2, fig3, fig4, fig5, fig6)
for i, f in enumerate(FIGS, 1):
    tag = f"<!--FIG{i}-->"
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
pos = [src.find(f"Hình {i}.") for i in range(1, len(FIGS) + 1)]
assert pos == sorted(pos), "số hình không theo thứ tự xuất hiện"
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
