#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 2 – Bài 19 (Công nghệ lắp ráp, phần 1), thay <!--FIGn--> và __PHUT__ trong
theory.src.html → theory.html.
Dùng: python3 build_figs.py  (chạy lại an toàn: luôn đọc từ theory.src.html)
Hình vẽ minh hoạ, không theo tỉ lệ. Chữ ≥ 12 trong viewBox 420 (đọc được ở 375px).
"""
import math
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import chevron  # noqa: E402

FONT = 'font-family="system-ui, sans-serif" font-size="13"'
RED, BLUE, GREEN, ORANGE = "#dc2626", "#0369a1", "#047857", "#ea580c"
METAL = 'fill="#94a3b8" fill-opacity="0.28"'
WORK = METAL + ' stroke="currentColor" stroke-width="1.5"'


def T(x, y, s, size=13, anchor="start", w="400", c="currentColor"):
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{anchor}">{s}</text>'


def sub(a, b):
    """Ký hiệu có chỉ số dưới, dùng trong T()."""
    return f'{a}<tspan dy="4" font-size="10">{b}</tspan><tspan dy="-4"></tspan>'


def Ln(x1, y1, x2, y2, c="currentColor", w=1.5, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'


def Ar(x1, y1, x2, y2, c=RED, w=2.2, L=10):
    """Mũi tên thẳng, đầu chữ V 30°."""
    return Ln(x1, y1, x2, y2, c, w) + chevron(x2, y2, x2 - x1, y2 - y1, c, w, L=L)


def R(x, y, w, h, extra=WORK, rx=0):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" {extra}/>'


def dim(x1, x2, y, c, label, ly=None, size=13):
    """Đường kích thước nằm ngang, hai đầu V hướng ra hai đường gióng, nhãn bên dưới."""
    L = 7 if x2 - x1 < 40 else 9
    o = [Ln(x1, y, x2, y, c, 1.6), chevron(x1, y, -1, 0, c, 1.6, L=L), chevron(x2, y, 1, 0, c, 1.6, L=L)]
    o.append(T((x1 + x2) / 2, ly if ly else y + 17, label, size, "middle", "700", c))
    return "".join(o)


def hatch(x, y, w, h, gap=8):
    """Gạch chéo 45° trong hình chữ nhật (mặt cắt thân hộp)."""
    o = [R(x, y, w, h, 'fill="#94a3b8" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"')]
    k = -h
    while k < w:
        x0 = x + k
        p0 = (x0, y + h)
        p1 = (x0 + h, y)
        # cắt vào khung
        if p0[0] < x:
            p0 = (x, y + h - (x - x0))
        if p1[0] > x + w:
            p1 = (x + w, y + (p1[0] - (x + w)))
        if p0[0] <= p1[0]:
            o.append(Ln(p0[0], p0[1], p1[0], p1[1], w=0.8))
        k += gap
    return "".join(o)


def svg(h, label, body):
    return (f'<svg viewBox="0 0 420 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" {FONT}>'
            + "".join(body) + "</svg>")


def fig(s, cap):
    return f'<figure class="fig" data-tl="1">{s}<figcaption>{cap}</figcaption></figure>'


def box(cx, cy, w, h, lines, c, bold=True, size=13):
    o = [R(cx - w / 2, cy - h / 2, w, h, f'fill="{c}" fill-opacity="0.12" stroke="{c}" stroke-width="1.6"', rx=6)]
    n = len(lines)
    for i, s in enumerate(lines):
        o.append(T(cx, cy + 4.5 + (i - (n - 1) / 2) * 16, s, size, "middle", "700" if bold else "400"))
    return "".join(o)


# Hình 1: phân loại mối lắp
def fig_moi_lap():
    o = [box(210, 24, 120, 30, ["Mối lắp"], "#64748b")]
    for cx, name, c in ((110, "Cố định", BLUE), (310, "Di động", ORANGE)):
        o.append(Ln(210, 39, cx, 66, w=1.4))
        o.append(box(cx, 82, 120, 30, [name], c))
        o.append(T(cx, 120, "vị trí tương đối không đổi" if cx < 200 else "chuyển động tương đối", 12, "middle", c=c))
        for dx, lines in ((-50, ["Tháo", "được"]), (50, ["Không", "tháo được"])):
            lx = cx + dx
            o.append(Ln(cx, 126, lx, 144, w=1.4))
            o.append(box(lx, 166, 90, 40, lines, c, bold=False, size=12))
    o.append(T(60, 204, "ren, then,", 12, "middle"))
    o.append(T(60, 220, "chốt, chêm", 12, "middle"))
    o.append(T(160, 204, "hàn, đinh tán,", 12, "middle"))
    o.append(T(160, 220, "ép, dán", 12, "middle"))
    return fig(svg(230, "Phân loại mối lắp cơ khí", o),
               "Hình 1. Phân loại mối lắp. Ví dụ dưới nhánh cố định lấy theo giáo trình.")


# Hình 2: chuỗi kích thước trong cụm thân hộp – bạc – bánh răng
def fig_chuoi():
    o = []
    WL, WR = 40, 380           # mặt trong hai thành hộp
    a1, a2, gap, a3 = 40, 230, 30, 40
    x1, x2, x3, x4 = WL + a1, WL + a1 + a2, WL + a1 + a2 + gap, WR
    assert x4 - x3 == a3
    # trục (vẽ trước)
    o.append(R(4, 88, 412, 16, 'fill="#94a3b8" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"'))
    o.append(Ln(2, 96, 418, 96, w=0.8, dash="8 3 2 3"))
    # thành hộp (mặt cắt)
    o.append(hatch(20, 30, 20, 58))
    o.append(hatch(20, 104, 20, 60))
    o.append(hatch(WR, 30, 20, 58))
    o.append(hatch(WR, 104, 20, 60))
    # bạc 1, bạc 2 (vai)
    o.append(R(WL, 64, a1, 64))
    o.append(R(x3, 64, a3, 64))
    # bánh răng + răng
    o.append(R(x1, 36, a2, 120, 'fill="#64748b" fill-opacity="0.30" stroke="currentColor" stroke-width="1.6"'))
    for yy in (44, 148):
        o.append(Ln(x1, yy, x2, yy, w=0.9, dash="5 3"))
    # nhãn chi tiết
    o.append(T(WL + a1 / 2, 58, "bạc", 12, "middle"))
    o.append(T(x3 + a3 / 2, 58, "bạc", 12, "middle"))
    o.append(T((x1 + x2) / 2, 74, "bánh răng", 13, "middle", "700"))
    o.append(T(14, 22, "thân hộp", 12))
    # đường gióng
    for x in (WL, x1, x2, x3, x4):
        o.append(Ln(x, 166 if x in (WL, x4) else 158, x, 236 if x in (WL, x4) else 194, w=0.8, dash="3 3"))
    o.append(Ln(x2, 158, x2, 194, w=0.8, dash="3 3"))
    # kích thước hàng 1
    o.append(dim(WL, x1, 186, "currentColor", sub("A", "1")))
    o.append(dim(x1, x2, 186, "currentColor", sub("A", "2")))
    o.append(dim(x2, x3, 186, RED, sub("A", "Δ")))
    o.append(dim(x3, x4, 186, "currentColor", sub("A", "3")))
    # kích thước hàng 2
    o.append(dim(WL, WR, 228, "currentColor", sub("A", "4"), ly=248))
    o.append(T(12, 268, "đỏ: khâu khép kín (khe hở)", 12, c=RED, w="700"))
    return fig(svg(276, "Chuỗi kích thước trong cụm thân hộp, bạc, bánh răng", o),
               "Hình 3. Cụm thân hộp – bạc – bánh răng (không theo tỉ lệ, khe hở vẽ phóng to). "
               "Khâu nào tăng, khâu nào giảm: em tự xác định ở Bài toán mẫu.")


# Hình 3: lắp cố định và lắp di động cưỡng bức
def fig_to_chuc():
    o = [T(12, 20, "a) Lắp cố định: sản phẩm đứng yên", 13, w="700")]
    # bàn lắp + sản phẩm
    o.append(R(160, 80, 100, 10, 'fill="currentColor" fill-opacity="0.5"'))
    o.append(R(180, 46, 60, 34))
    o.append(T(210, 108, "chỗ lắp", 12, "middle"))
    for (px, py, name) in ((40, 44, "chi tiết"), (40, 88, "cụm"), (340, 66, "bộ phận")):
        o.append(R(px - 26, py - 12, 52, 24, f'fill="{BLUE}" fill-opacity="0.12" stroke="{BLUE}" stroke-width="1.4"', rx=4))
        o.append(T(px, py + 4.5, name, 12, "middle"))
        if px < 200:
            o.append(Ar(px + 34, py, 168, 63 if py < 60 else 70, BLUE, 1.8, L=8))
        else:
            o.append(Ar(px - 34, py, 252, 63, BLUE, 1.8, L=8))
    # b) di động cưỡng bức
    y0 = 150
    o.append(T(12, y0, "b) Lắp di động cưỡng bức: băng chuyền theo nhịp", 13, w="700"))
    o.append(R(20, y0 + 62, 380, 8, 'fill="currentColor" fill-opacity="0.35"', rx=4))
    for k in range(9):
        o.append(f'<circle cx="{36 + 43.5 * k:.1f}" cy="{y0 + 78}" r="6" fill="none" stroke="currentColor" stroke-width="1.3"/>')
    for i, xs in enumerate((60, 180, 300)):
        h = 14 + 10 * i
        assert y0 + 62 - h - (y0 + 20) >= 8      # nhãn không chạm hộp
        o.append(R(xs, y0 + 62 - h, 50, h))
        o.append(T(xs + 25, y0 + 20, f"vị trí {i + 1}", 12, "middle"))
    o.append(Ar(150, y0 + 104, 270, y0 + 104, GREEN, 2.2))
    o.append(T(210, y0 + 124, "đối tượng lắp đi qua từng vị trí", 12, "middle", c=GREEN, w="700"))
    return fig(svg(284, "Lắp cố định và lắp di động cưỡng bức", o),
               "Hình 2. a) Lắp cố định: chi tiết, cụm, bộ phận được đưa tới chỗ lắp. "
               "b) Lắp di động cưỡng bức: mỗi vị trí làm một số nguyên công, sản phẩm lớn dần qua từng vị trí.")


# Hình 4: lắp chọn theo nhóm (lỗ Ø50 +0,03; trục 49,96 ÷ 49,99; 3 nhóm)
def fig_chon_nhom():
    o = []
    K = 2600.0                 # px / mm  (0,01 mm = 26 px)
    top = 50.03

    def y(v):
        return 26 + (top - v) * K

    colors = (BLUE, GREEN, ORANGE)
    names = ("I", "II", "III")
    HX, SX, W = 120, 260, 56
    for i in range(3):
        hl, hh = 50.00 + 0.01 * i, 50.01 + 0.01 * i
        sl, sh = 49.96 + 0.01 * i, 49.97 + 0.01 * i
        c = colors[i]
        o.append(R(HX, y(hh), W, y(hl) - y(hh), f'fill="{c}" fill-opacity="0.22" stroke="{c}" stroke-width="1.6"'))
        o.append(R(SX, y(sh), W, y(sl) - y(sh), f'fill="{c}" fill-opacity="0.22" stroke="{c}" stroke-width="1.6"'))
        o.append(T(HX + W / 2, (y(hh) + y(hl)) / 2 + 5, names[i], 13, "middle", "700", c))
        o.append(T(SX + W / 2, (y(sh) + y(sl)) / 2 + 5, names[i], 13, "middle", "700", c))
        o.append(Ln(HX + W, (y(hh) + y(hl)) / 2, SX, (y(sh) + y(sl)) / 2, c, 1.3, "5 4"))
    # đường danh nghĩa 50,00
    o.append(Ln(HX - 2, y(50.00), 400, y(50.00), w=1, dash="8 3 2 3"))
    o.append(T(398, y(50.00) - 5, "Ø50", 12, "end"))
    # cỡ ghi bên cạnh
    for v, s in ((50.03, "50,03"), (50.00, "50,00")):
        o.append(T(HX - 8, y(v) + 4.5, s, 12, "end"))
    for v, s in ((49.99, "49,99"), (49.96, "49,96")):
        o.append(T(SX + W + 8, y(v) + 4.5, s, 12))
    o.append(T(HX + W / 2, y(50.00) + 20, "lỗ", 13, "middle", "700"))
    o.append(T(SX + W / 2, y(49.96) + 22, "trục", 13, "middle", "700"))
    yb = y(49.96) + 46
    o.append(T(12, yb, "Không chọn: khe hở 0,01 ÷ 0,07 mm", 13))
    o.append(T(12, yb + 20, "Lắp cùng nhóm: khe hở 0,03 ÷ 0,05 mm", 13, w="700"))
    return fig(svg(int(yb + 32), "Sơ đồ lắp chọn theo ba nhóm", o),
               "Hình 4. Lắp chọn theo nhóm (ví dụ tự soạn): chia miền dung sai lỗ và trục thành 3 nhóm, "
               "lắp nhóm cùng tên với nhau. Dung sai lắp từ 0,06 còn 0,02 mm.")


# Hình 5: lắp điều chỉnh bằng vòng đệm
def fig_vong_dem():
    o = []
    # trục
    o.append(R(10, 100, 232, 20, 'fill="#94a3b8" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"'))
    o.append(Ln(6, 110, 330, 110, w=0.8, dash="8 3 2 3"))
    # thân hộp (mặt cắt) có lỗ lắp ổ
    o.append(hatch(200, 40, 90, 52))
    o.append(hatch(200, 128, 90, 52))
    # ổ lăn
    o.append(R(205, 92, 37, 36, 'fill="#64748b" fill-opacity="0.30" stroke="currentColor" stroke-width="1.4"'))
    o.append(f'<circle cx="223.5" cy="110" r="9" fill="none" stroke="currentColor" stroke-width="1.3"/>')
    # nắp ổ: gờ + mặt bích
    o.append(R(270, 94, 30, 32))
    o.append(R(300, 34, 20, 152))
    # vòng đệm (khâu bồi thường)
    o.append(R(290, 40, 10, 52, f'fill="{RED}" fill-opacity="0.45" stroke="{RED}" stroke-width="1.4"'))
    o.append(R(290, 128, 10, 52, f'fill="{RED}" fill-opacity="0.45" stroke="{RED}" stroke-width="1.4"'))
    # khe hở
    o.append(Ln(242, 102, 270, 102, RED, 1.4))
    o.append(chevron(242, 102, -1, 0, RED, 1.4, L=6))
    o.append(chevron(270, 102, 1, 0, RED, 1.4, L=6))
    o.append(T(256, 122, sub("A", "Δ"), 13, "middle", "700", RED))
    # nhãn
    o.append(T(200, 30, "thân hộp", 12, "end"))
    o.append(Ln(202, 26, 214, 40, w=0.8))
    o.append(T(330, 30, "nắp ổ", 12))
    o.append(T(30, 92, "trục", 12))
    o.append(T(150, 150, "ổ lăn", 12, "end"))
    o.append(Ln(152, 146, 205, 122, w=0.8))
    o.append(Ln(295, 180, 300, 204, RED, 1))
    o.append(T(300, 218, "vòng đệm s", 13, "middle", "700", RED))
    o.append(T(300, 234, "(khâu bồi thường)", 12, "middle", c=RED))
    o.append(T(12, 210, "Đệm dày hơn: khe hở tăng", 13))
    o.append(T(12, 230, "Đệm mỏng hơn: khe hở giảm", 13))
    o.append(T(12, 250, "Không cạo, mài chi tiết nào", 13, w="700"))
    return fig(svg(260, "Lắp điều chỉnh bằng vòng đệm", o),
               "Hình 5. Lắp điều chỉnh: đo khe hở rồi chọn vòng đệm có bề dày phù hợp. "
               "Lắp sửa thì ngược lại: cạo, mài bớt khâu bồi thường.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig_moi_lap), ("<!--FIG2-->", fig_to_chuc), ("<!--FIG3-->", fig_chuoi),
               ("<!--FIG4-->", fig_chon_nhom), ("<!--FIG5-->", fig_vong_dem)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())

lint = ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = HERE / "theory.html"
out.write_text(src.replace("__PHUT__", "?"), encoding="utf8")
r = subprocess.run([sys.executable, str(lint), str(out), "--json"], capture_output=True, text=True)
mm = re.search(r'"phut"\s*:\s*([\d.]+)', r.stdout)
phut = math.ceil(float(mm.group(1))) if mm else "?"
out.write_text(src.replace("__PHUT__", str(phut)), encoding="utf8")
print("đã ghi theory.html; phút =", phut)
