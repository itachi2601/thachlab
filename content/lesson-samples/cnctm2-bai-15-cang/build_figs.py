#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 2 – Bài 15 (Công nghệ gia công chi tiết dạng càng),
thay <!--FIGn--> và __PHUT__ trong theory.src.html → theory.html.
Dùng: python3 build_figs.py  (chạy lại an toàn: luôn đọc từ theory.src.html)
Mọi hình là sơ đồ nguyên lý tự vẽ, không theo tỉ lệ. Chữ ≥ 12 trong viewBox 420.
Nhãn được ghi hộp bao gần đúng và kiểm chồng nhau / vượt khung ngay khi build.
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
METAL = 'fill="#94a3b8" fill-opacity="0.30" stroke="currentColor" stroke-width="1.6"'
FIXT = 'fill="#64748b" fill-opacity="0.45" stroke="currentColor" stroke-width="1.4"'

BOXES = []   # (hình, x0, y0, x1, y1, chữ)
CUR = {"f": 0, "h": 0}


def T(x, y, s, size=12, anchor="start", w="400", c="currentColor"):
    n = len(re.sub(r"<[^>]+>", "", s))
    wd = n * size * 0.56
    x0 = x if anchor == "start" else (x - wd / 2 if anchor == "middle" else x - wd)
    BOXES.append((CUR["f"], x0, y - size * 0.8, x0 + wd, y + size * 0.2, s))
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{anchor}">{s}</text>'


def Ln(x1, y1, x2, y2, c="currentColor", w=1.5, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'


def Ar(x1, y1, x2, y2, c=RED, w=2.2, L=10):
    return Ln(x1, y1, x2, y2, c, w) + chevron(x2, y2, x2 - x1, y2 - y1, c, w, L=L)


def Dim(x1, y, x2, label, c="currentColor"):
    """Đường kích thước ngang hai đầu V."""
    return (Ln(x1, y, x2, y, c, 1.2) + chevron(x1, y, -1, 0, c, 1.2, L=7) + chevron(x2, y, 1, 0, c, 1.2, L=7)
            + T((x1 + x2) / 2, y - 6, label, 13, "middle", "700", c))


def P(pts, extra=METAL):
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" {extra}/>'


def R(x, y, w, h, extra=METAL):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" {extra}/>'


def circ_cw(cx, cy, r, cw=True):
    s = 1 if cw else 0
    return f"M{cx - r:.1f},{cy:.1f} A{r},{r} 0 1 {s} {cx + r:.1f},{cy:.1f} A{r},{r} 0 1 {s} {cx - r:.1f},{cy:.1f} Z "


def cang(cx1, R1, r1, cx2, R2, r2, cy, w1, w2, extra=METAL):
    """Càng nhìn từ trên: một đường bao (cung đầu to – thân – cung đầu nhỏ) + lỗ, không có nét thừa bên trong."""
    assert w1 < R1 and w2 < R2
    s1, s2 = math.sqrt(R1 ** 2 - w1 ** 2), math.sqrt(R2 ** 2 - w2 ** 2)
    assert cx1 + s1 < cx2 - s2
    d = (f"M{cx1 + s1:.1f},{cy - w1:.1f} L{cx2 - s2:.1f},{cy - w2:.1f} "
         f"A{R2},{R2} 0 1 1 {cx2 - s2:.1f},{cy + w2:.1f} L{cx1 + s1:.1f},{cy + w1:.1f} "
         f"A{R1},{R1} 0 1 1 {cx1 + s1:.1f},{cy - w1:.1f} Z ")
    if r1:
        d += circ_cw(cx1, cy, r1, False)
    if r2:
        d += circ_cw(cx2, cy, r2, False)
    return f'<path d="{d}" fill-rule="evenodd" {extra}/>'


def axis(x1, y1, x2, y2):
    return Ln(x1, y1, x2, y2, "currentColor", 0.8, "10 3 2 3")


def svg(h, label, body):
    return (f'<svg viewBox="0 0 420 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}" {FONT}>'
            + "".join(body) + "</svg>")


def fig(s, cap):
    return f'<figure class="fig" data-tl="1">{s}<figcaption>{cap}</figcaption></figure>'


def start(n, h):
    CUR["f"], CUR["h"] = n, h


def side_strip(y0, cx1, R1, cx2, R2, plate=True):
    """Nhìn ngang: hai đầu dày (mặt đầu lồi) + thân mỏng; tuỳ chọn phiến tì + ký hiệu 3 điểm tì."""
    o = [R(cx1 - R1, y0, 2 * R1, 30), R(cx1 + R1, y0 + 8, cx2 - R2 - cx1 - R1, 14), R(cx2 - R2, y0, 2 * R2, 30)]
    if plate:
        o.append(R(cx1 - R1 - 20, y0 + 44, cx2 + R2 - cx1 + R1 + 40, 12, FIXT))
        for x in (cx1 - R1 * 0.55, cx1 + R1 * 0.55, cx2):
            o.append(f'<path d="M{x:.1f} {y0 + 30:.1f} L{x - 7:.1f} {y0 + 44:.1f} L{x + 7:.1f} {y0 + 44:.1f} Z" fill="{BLUE}"/>')
    return o


# Hình 1: càng nối điển hình — nhìn từ trên + nhìn ngang
def fig1():
    start(1, 272)
    o = []
    cy, c1, c2 = 92, 110, 310
    o.append(cang(c1, 46, 24, c2, 30, 14, cy, 20, 13))
    for cx, Rr in ((c1, 46), (c2, 30)):
        o.append(axis(cx, cy - Rr - 8, cx, cy + Rr + 6))
        o.append(axis(cx - Rr - 6, cy, cx + Rr + 6, cy))
    o.append(Ln(c1, cy - 50, c1, 24, w=0.8))
    o.append(Ln(c2, cy - 34, c2, 24, w=0.8))
    o.append(Dim(c1, 30, c2, "A: khoảng cách tâm", BLUE))
    # lỗ ren kẹp chặt trên vành đầu to, giữa hai đường tròn r=24 và R=46
    hx, hy, hr = c1 - 35, cy, 4.5
    dist = c1 - hx
    assert dist - hr >= 24 + 4 and dist + hr <= 46 - 4
    o.append(f'<circle cx="{hx}" cy="{hy}" r="{hr}" fill="none" stroke="{RED}" stroke-width="2"/>')
    o.append(T(14, 50, "lỗ ren", 12, c=RED))
    o.append(T(14, 64, "kẹp chặt", 12, c=RED))
    o.append(Ln(40, 70, hx - 3, hy - 4, RED, 1))
    o.append(T(c1, 158, "lỗ cơ bản", 12, "middle", "700"))
    o.append(T(c2, 158, "lỗ cơ bản", 12, "middle", "700"))
    o.append(T(212, 96, "thân", 12, "middle"))
    # nhìn ngang
    y0 = 186
    o += side_strip(y0, c1, 46, c2, 30, plate=False)
    for x0, x1 in ((c1 - 46, c1 + 46), (c2 - 30, c2 + 30)):
        o.append(Ln(x0, y0, x1, y0, RED, 3.2))
        o.append(Ln(x0, y0 + 30, x1, y0 + 30, RED, 3.2))
    for cx, r in ((c1, 24), (c2, 14)):
        o.append(Ln(cx - r, y0, cx - r, y0 + 30, w=1, dash="4 3"))
        o.append(Ln(cx + r, y0, cx + r, y0 + 30, w=1, dash="4 3"))
        o.append(axis(cx, y0 - 8, cx, y0 + 38))
    o.append(T(212, 182, "mặt đầu lồi lên", 12, "middle", "700", RED))
    o.append(T(210, 262, "hai tâm lỗ song song, vuông góc mặt đầu", 12, "middle"))
    return fig(svg(272, "Càng nối điển hình nhìn từ trên và nhìn ngang", o),
               "Hình 1. Càng nối: trên nhìn từ trên, dưới nhìn ngang. Đỏ: mặt đầu cần gia công; nét đứt: thành lỗ.")


# Hình 2: phôi kép rèn từng cặp
def fig2():
    start(2, 196)
    o = []
    cy = 92
    ya = math.sqrt(22 ** 2 - 9 ** 2)
    o.append(R(182 + ya - 1, cy - 9, 238 - 182 - 2 * ya + 2, 18, 'fill="#94a3b8" fill-opacity="0.30" stroke="none"'))
    o.append(Ln(182 + ya, cy - 9, 238 - ya, cy - 9, w=1.6))
    o.append(Ln(182 + ya, cy + 9, 238 - ya, cy + 9, w=1.6))
    o.append(cang(70, 34, 0, 182, 22, 0, cy, 15, 10))
    o.append(cang(238, 22, 0, 350, 34, 0, cy, 10, 15))
    o.append(Ln(210, 44, 210, 140, RED, 2.2, "6 4"))
    o.append(T(70, 40, "càng 1", 13, "middle", "700"))
    o.append(T(350, 40, "càng 2", 13, "middle", "700"))
    o.append(T(210, 160, "cắt đôi sau khi gia công xong", 12, "middle", c=RED))
    o.append(T(210, 182, "rèn một lần được hai chi tiết, gá dễ hơn", 12, "middle"))
    return fig(svg(196, "Phôi kép rèn từng cặp càng", o),
               "Hình 2. Phôi kép rèn liền hai càng, cắt đôi theo nét đỏ.")


# Hình 3: gá đặt bằng chuẩn thô — mặt đầu + hai khối V
def fig3():
    start(3, 282)
    o = []
    cy, c1, R1, c2, R2 = 112, 120, 40, 320, 26
    o.append(cang(c1, R1, 0, c2, R2, 0, cy, 20, 13))
    s = math.sqrt(0.5)
    # khối V cố định (mở sang phải), mặt V tiếp xúc vành ngoài tại 135° và 225°
    vx = c1 - R1 / s
    ct = (c1 - R1 * s, cy - R1 * s)
    ext = (ct[0] + 8 * s, ct[1] - 8 * s)
    o.append(P([ext, (vx, cy), (ext[0], 2 * cy - ext[1]), (30, 2 * cy - ext[1]), (30, ext[1])], FIXT))
    # khối V di động (mở sang trái)
    vx2 = c2 + R2 / s
    ct2 = (c2 + R2 * s, cy - R2 * s)
    ext2 = (ct2[0] - 8 * s, ct2[1] - 8 * s)
    o.append(P([ext2, (vx2, cy), (ext2[0], 2 * cy - ext2[1]), (392, 2 * cy - ext2[1]), (392, ext2[1])], FIXT))
    o.append(Ar(418, cy, 400, cy, RED, 2.6, L=9))
    o.append(T(404, cy - 10, "W", 13, "start", "700", RED))
    o.append(T(24, 60, "khối V cố định: 2 bậc", 12, "start", "700", BLUE))
    o.append(T(410, 76, "khối V di động: 1 bậc", 12, "end", "700", BLUE))
    for cx, Rr in ((c1, R1), (c2, R2)):
        o.append(axis(cx - 8, cy, cx + 8, cy))
        o.append(axis(cx, cy - 8, cx, cy + 8))
    # nhìn ngang: mặt đầu dưới tì phiến tì (3 điểm), mặt trên sẽ gia công
    y0 = 196
    o += side_strip(y0, c1, R1, c2, R2)
    for x0, x1 in ((c1 - R1, c1 + R1), (c2 - R2, c2 + R2)):
        o.append(Ln(x0, y0, x1, y0, RED, 3.2))
    o.append(T(210, 188, "mặt đầu bên kia: gia công", 12, "middle", c=RED))
    o.append(T(210, 274, "mặt đầu dưới tì phiến tì: 3 bậc", 12, "middle", "700", BLUE))
    return fig(svg(282, "Gá đặt càng bằng chuẩn thô: mặt đầu và hai khối V", o),
               "Hình 3. Chuẩn thô. Trên: khối V ôm vành ngoài, kẹp W qua khối V di động. Dưới: tam giác xanh là điểm tì mặt đầu.")


# Hình 4: chuẩn tinh thống nhất — mặt đầu + chốt trụ ngắn + chốt trám
def fig4():
    start(4, 276)
    o = []
    cy, c1, R1, r1, c2, R2, r2 = 112, 120, 42, 22, 320, 31, 17
    o.append(cang(c1, R1, r1, c2, R2, r2, cy, 20, 13))
    o.append(axis(c1 - R1 - 8, cy, c2 + R2 + 8, cy))
    o.append(f'<circle cx="{c1}" cy="{cy}" r="{r1 - 1.5}" fill="{BLUE}" fill-opacity="0.55" stroke="{BLUE}" stroke-width="1.5"/>')
    # chốt trám: tròn ở trên/dưới, vát phẳng hai bên theo đường nối tâm (trái/phải)
    rp, fx = r2 - 1.5, (r2 - 1.5) * 0.45
    fy = math.sqrt(rp ** 2 - fx ** 2)
    d = (f"M{c2 - fx:.1f},{cy - fy:.1f} A{rp:.1f},{rp:.1f} 0 0 1 {c2 + fx:.1f},{cy - fy:.1f} "
         f"L{c2 + fx:.1f},{cy + fy:.1f} A{rp:.1f},{rp:.1f} 0 0 1 {c2 - fx:.1f},{cy + fy:.1f} Z")
    o.append(f'<path d="{d}" fill="{BLUE}" fill-opacity="0.55" stroke="{BLUE}" stroke-width="1.5"/>')
    o.append(T(24, 56, "chốt trụ ngắn: 2 bậc", 12, "start", "700", BLUE))
    o.append(T(410, 70, "chốt trám: 1 bậc", 12, "end", "700", BLUE))
    o.append(T(c2, 166, "vát hai bên theo", 12, "middle"))
    o.append(T(c2, 181, "đường nối tâm", 12, "middle"))
    # lỗ ren cần khoan ở vành đầu to
    hx = c1 - 33
    assert (c1 - hx) - 5 >= r1 + 4 and (c1 - hx) + 5 <= R1 - 3
    o.append(f'<circle cx="{hx}" cy="{cy}" r="5" fill="none" stroke="{RED}" stroke-width="2"/>')
    o.append(T(24, 176, "lỗ ren sẽ khoan", 12, c=RED))
    o.append(Ln(60, 166, hx - 2, cy + 6, RED, 1))
    y0 = 196
    o += side_strip(y0 - 4, c1, R1, c2, R2)
    o.append(T(210, 268, "mặt đầu tì phiến tì: 3 bậc", 12, "middle", "700", BLUE))
    return fig(svg(276, "Chuẩn tinh thống nhất của càng: mặt đầu, chốt trụ ngắn, chốt trám", o),
               "Hình 4. Chuẩn tinh thống nhất: mặt đầu 3 + chốt trụ ngắn 2 + chốt trám 1 = 6 bậc.")


# Hình 5: sơ đồ thứ tự nguyên công
def fig5():
    rows = [("Đầu: mặt đầu", "", "chuẩn thô: vành ngoài", "+ mặt đầu kia"),
            ("Vấu chuẩn phụ", "nếu có", "mặt đầu đã gia công", "(thông lệ)"),
            ("Lỗ chính: thô → tinh", "khoan – khoét – doa", "mặt đầu + vành ngoài,", "hoặc + lỗ đã làm"),
            ("Lỗ phụ: ren, dầu", "cân bằng nếu cần", "mặt đầu + chốt trụ", "+ chốt trám"),
            ("Kiểm tra", "", "khoảng cách tâm,", "song song, vuông góc")]
    bh, gap, y = 42, 26, 30
    h = y + len(rows) * bh + (len(rows) - 1) * gap + 12
    start(5, h)
    o = [T(16, 18, "Nguyên công", 12, "start", "700"), T(232, 18, "Chuẩn hay dùng", 12, "start", "700", BLUE)]
    for i, (a, a2, b, b2) in enumerate(rows):
        yt = y + i * (bh + gap)
        col = RED if i in (0, 2) else "currentColor"
        o.append(R(16, yt, 204, bh, f'fill="#94a3b8" fill-opacity="0.18" stroke="{col}" stroke-width="{2.2 if col == RED else 1.4}" rx="6"'))
        if a2:
            o.append(T(28, yt + 18, f"{i + 1}. {a}", 13, "start", "700"))
            o.append(T(28, yt + 35, a2, 12))
        else:
            o.append(T(28, yt + 26, f"{i + 1}. {a}", 13, "start", "700"))
        if b2:
            o.append(T(232, yt + 18, b, 12, c=BLUE))
            o.append(T(232, yt + 35, b2, 12, c=BLUE))
        else:
            o.append(T(232, yt + 26, b, 12, c=BLUE))
        if i < len(rows) - 1:
            o.append(Ar(118, yt + bh + 4, 118, yt + bh + gap - 8, "currentColor", 1.8, L=8))
    return fig(svg(h, "Sơ đồ thứ tự nguyên công gia công càng", o),
               "Hình 5. Đường lối chung. Viền đỏ: mặt đầu và lỗ cơ bản, hai bước quyết định độ chính xác.")


# Hình 6: kiểm độ song song và khoảng cách tâm hai lỗ
def fig6():
    start(6, 300)
    o = []
    o.append(R(40, 250, 340, 18, FIXT))
    o.append(T(348, 263, "đế", 12, "start", "700"))
    # chốt định vị (có vai đỡ càng)
    o.append(R(90, 200, 40, 50, f'fill="{BLUE}" fill-opacity="0.35" stroke="{BLUE}" stroke-width="1.4"'))
    o.append(R(101, 150, 18, 50, f'fill="{BLUE}" fill-opacity="0.55" stroke="{BLUE}" stroke-width="1.4"'))
    # càng kiểm (cắt ngang qua hai lỗ)
    o.append(R(66, 180, 35, 20))
    o.append(R(119, 180, 173, 20))
    o.append(R(308, 180, 36, 20))
    # trục kiểm qua lỗ 2
    o.append(R(292, 80, 16, 156, f'fill="{ORANGE}" fill-opacity="0.35" stroke="{ORANGE}" stroke-width="1.6"'))
    # hai đồng hồ so ở vị trí I (trên) và II (dưới)
    for yy, lab in ((100, "I"), (224, "II")):
        o.append(f'<circle cx="372" cy="{yy}" r="16" fill="none" stroke="currentColor" stroke-width="1.6"/>')
        o.append(Ln(372, yy, 380, yy - 9, RED, 1.6))
        o.append(Ln(356, yy, 309, yy, w=2))
        o.append(T(394, yy + 5, lab, 13, "start", "700", BLUE))
    o.append(axis(110, 146, 110, 270))
    o.append(axis(300, 70, 300, 244))
    o.append(Ln(110, 146, 110, 48, w=0.8))
    o.append(Ln(300, 76, 300, 48, w=0.8))
    o.append(Dim(110, 54, 300, "A", BLUE))
    o.append(T(128, 144, "chốt định vị (lỗ 1)", 12))
    o.append(T(130, 174, "càng cần kiểm", 12))
    o.append(T(286, 100, "trục kiểm", 12, "end"))
    o.append(T(286, 116, "(lỗ 2)", 12, "end"))
    o.append(T(14, 288, "Hiệu số đồng hồ I và II: độ không song song", 12, "start", "700"))
    return fig(svg(300, "Kiểm độ song song và khoảng cách tâm hai lỗ càng", o),
               "Hình 6. Nhìn ngang qua hai tâm lỗ: lỗ 1 trên chốt định vị, trục kiểm trong lỗ 2; đồng hồ ở I, II; A là khoảng cách tâm.")


FIGS = [fig1, fig2, fig3, fig4, fig5, fig6]
HS = {}
rendered = []
for i, f in enumerate(FIGS, 1):
    rendered.append(f())
    HS[i] = CUR["h"]

# kiểm nhãn: trong khung, không chồng nhau
bad = []
for i, (g, x0, y0, x1, y1, s) in enumerate(BOXES):
    if x0 < 2 or y0 < 2 or x1 > 418 or y1 > HS[g] - 1:
        bad.append(f"Hình {g}: nhãn '{s}' vượt khung ({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f})")
    for gg, a0, b0, a1, b1, t in BOXES[i + 1:]:
        if gg == g and x0 < a1 and a0 < x1 and y0 < b1 and b0 < y1:
            bad.append(f"Hình {g}: nhãn '{s}' chồng '{t}'")
print("\n".join(bad) if bad else "kiểm nhãn: ok")

src = (HERE / "theory.src.html").read_text(encoding="utf8")
order = [int(k) for k in re.findall(r"<!--FIG(\d)-->", src)]
assert order == list(range(1, len(FIGS) + 1)), order
for k, s in enumerate(rendered, 1):
    src = src.replace(f"<!--FIG{k}-->", s)
assert "<!--FIG" not in src

lint = ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = HERE / "theory.html"
out.write_text(src.replace("__PHUT__", "?"), encoding="utf8")
r = subprocess.run([sys.executable, str(lint), str(out), "--json"], capture_output=True, text=True)
mm = re.search(r'"phut"\s*:\s*([\d.]+)', r.stdout)
phut = math.ceil(float(mm.group(1))) if mm else "?"
out.write_text(src.replace("__PHUT__", str(phut)), encoding="utf8")
print("đã ghi theory.html,", len(FIGS), "hình; phút =", phut)
