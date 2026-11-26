#!/usr/bin/env python3
"""Sinh hình SVG cho CNCTM 1 – Bài 5 (Độ chính xác gia công), thay <!--FIGn--> trong theory.src.html → theory.html.
Dùng: python3 build_figs.py  (chạy lại an toàn: luôn đọc từ theory.src.html)
Số hình trong chú thích = thứ tự xuất hiện trong bài (FIG1 → FIG7 đặt đúng thứ tự trong src).
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


# ---------------------------------------------------------------- Hình 1: bốn yếu tố
def fig1():
    o = [svg_open(420, 300, "Bốn yếu tố của độ chính xác gia công")]
    o.append('<line x1="210" y1="8" x2="210" y2="292" stroke="currentColor" stroke-opacity="0.3"/>')
    o.append('<line x1="8" y1="150" x2="412" y2="150" stroke="currentColor" stroke-opacity="0.3"/>')
    # 1. Cỡ – kích thước (ô trái trên)
    o.append(t(10, 20, "Cỡ – kích thước", 13, True, BLUE))
    o.append('<rect x="20" y="40" width="120" height="50" fill="none" stroke="currentColor" stroke-width="2"/>')
    o.append('<line x1="140" y1="40" x2="170" y2="40" stroke="currentColor" stroke-width="1"/>')
    o.append('<line x1="140" y1="90" x2="170" y2="90" stroke="currentColor" stroke-width="1"/>')
    o.append('<line x1="162" y1="40" x2="162" y2="90" stroke="currentColor" stroke-width="1.2"/>')
    o.append(arrow_head(162, 40, "up") + arrow_head(162, 90, "down"))
    o.append(t(10, 114, "Ø22 +0,021"))
    o.append(t(10, 132, "→ dung sai T = 0,021 mm"))
    # 2. Dáng – hình học (ô phải trên)
    o.append(t(220, 20, "Dáng – hình học", 13, True, BLUE))
    o.append('<rect x="232" y="45" width="150" height="40" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4"/>')
    o.append(f'<path d="M232 48 Q307 34 382 48 L382 82 Q307 96 232 82 Z" fill="none" stroke="{RED}" stroke-width="2"/>')
    o.append(t(220, 114, "nét đứt: dáng thiết kế"))
    o.append(t(220, 132, "nét đỏ: tang trống (phóng đại)", color=RED))
    # 3. Vị – vị trí tương quan (ô trái dưới)
    o.append(t(10, 170, "Vị – vị trí tương quan", 13, True, BLUE))
    o.append('<circle cx="62" cy="226" r="34" fill="none" stroke="currentColor" stroke-width="2"/>')
    o.append(f'<circle cx="72" cy="220" r="14" fill="none" stroke="{RED}" stroke-width="2"/>')
    o.append('<path d="M56 226 h12 M62 220 v12" stroke="currentColor" stroke-width="1.2"/>')
    o.append(f'<path d="M66 220 h12 M72 214 v12" stroke="{RED}" stroke-width="1.2"/>')
    o.append(t(110, 206, "độ đồng tâm"))
    o.append(t(110, 224, "độ song song"))
    o.append(t(110, 242, "độ vuông góc"))
    o.append(t(10, 284, "lỗ lệch tâm (phóng đại)", color=RED))
    # 4. Mặt – chất lượng bề mặt (ô phải dưới)
    o.append(t(220, 170, "Mặt – chất lượng bề mặt", 13, True, BLUE))
    pts = []
    for i in range(0, 37):
        x = 225 + i * 5
        y = 212 + (-6 if i % 2 else 6) + 6 * math.sin(i / 36 * 2 * math.pi)
        pts.append(f"{x},{y:.1f}")
    o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="currentColor" stroke-width="1.8"/>')
    o.append(f'<line x1="225" y1="232" x2="405" y2="232" stroke="{ORANGE}" stroke-width="5" stroke-opacity="0.45"/>')
    o.append(t(220, 256, "độ nhám, độ sóng"))
    o.append(t(220, 274, "lớp biến cứng, ứng suất dư", color=ORANGE))
    o.append('</svg>')
    return fig("".join(o), "Hình 1. Bốn yếu tố của độ chính xác gia công: Cỡ – Dáng – Vị – Mặt (hình minh hoạ, sai lệch vẽ phóng đại).")


# ---------------------------------------------------------------- Hình 2: nhám và sóng
def fig2():
    o = [svg_open(420, 190, "Độ sóng và độ nhám trên một profin bề mặt")]
    wave, prof = [], []
    for i in range(0, 153):
        x = 20 + i * 2.5
        yw = 100 + 18 * math.sin(2 * math.pi * (x - 20) / 190)
        saw = 5 * (1 - 2 * abs(((x - 20) / 10) % 2 - 1))
        wave.append(f"{x:.1f},{yw:.1f}")
        prof.append(f"{x:.1f},{yw + saw:.1f}")
    o.append(f'<polygon points="20,140 {" ".join(prof)} 400,140" fill="{BLUE}" fill-opacity="0.12"/>')
    o.append(f'<polyline points="{" ".join(prof)}" fill="none" stroke="currentColor" stroke-width="1.6"/>')
    o.append(f'<polyline points="{" ".join(wave)}" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="6 4"/>')
    o.append(f'<line x1="20" y1="20" x2="42" y2="20" stroke="{RED}" stroke-width="2" stroke-dasharray="6 4"/>')
    o.append(t(48, 24, "độ sóng: lượn dài, bước lớn", color=RED))
    o.append('<line x1="20" y1="42" x2="42" y2="42" stroke="currentColor" stroke-width="1.6"/>')
    o.append(t(48, 46, "độ nhám: nhấp nhô nhỏ, bước rất ngắn"))
    # chiều dài chuẩn
    o.append('<line x1="40" y1="158" x2="140" y2="158" stroke="currentColor" stroke-width="1.2"/>')
    o.append(arrow_head(40, 158, "left") + arrow_head(140, 158, "right"))
    o.append('<line x1="40" y1="148" x2="40" y2="166" stroke="currentColor"/><line x1="140" y1="148" x2="140" y2="166" stroke="currentColor"/>')
    o.append(t(40, 182, "l: chiều dài chuẩn để đo Ra, Rz"))
    o.append('</svg>')
    return fig("".join(o), "Hình 2. Một đường cắt qua bề mặt: độ sóng (đỏ, nét đứt) và độ nhám nằm chồng lên nhau.")


# ---------------------------------------------------------------- Hình 3: vết mũi dao tròn
def fig3():
    R, S, BOT = 70, 100, 140
    cy = BOT - R
    half = S / 2
    cusp = BOT - (R - math.sqrt(R * R - half * half))  # y của đỉnh nhấp nhô
    o = [svg_open(420, 200, "Vết mũi dao bán kính r để lại nhấp nhô cao Rz sau mỗi bước S")]
    cxs = [50, 150, 250, 350]
    d = f"M{cxs[0] - half} {cusp:.1f}"
    for cx in cxs:
        d += f" A{R} {R} 0 0 0 {cx + half} {cusp:.1f}"
    o.append(f'<path d="{d} L400 160 L0 160 Z" fill="{BLUE}" fill-opacity="0.12"/>')
    o.append(f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="2"/>')
    # mũi dao ở vị trí cuối
    o.append(f'<circle cx="350" cy="{cy}" r="{R}" fill="none" stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="6 4"/>')
    ex, ey = 350 + R * math.cos(math.radians(45)), cy - R * math.sin(math.radians(45))
    o.append(f'<line x1="350" y1="{cy}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{ORANGE}" stroke-width="1.6"/>')
    o.append(t(384, 58, "r", 14, True, ORANGE))
    o.append(t(274, 32, "mũi dao", color=ORANGE, anchor="end"))
    # công thức
    o.append(f'<text x="20" y="40" fill="currentColor" font-size="14" font-weight="700">Rz ≈ S<tspan baseline-shift="super" font-size="10">2</tspan> / (8r)</text>')
    o.append(t(20, 60, "(khi S &gt; 0,15 mm/vòng)"))
    # Rz tại đỉnh nhấp nhô x = 200
    o.append(f'<line x1="178" y1="{cusp:.1f}" x2="222" y2="{cusp:.1f}" stroke="{RED}" stroke-width="1" stroke-dasharray="3 3"/>')
    o.append(f'<line x1="120" y1="{BOT}" x2="280" y2="{BOT}" stroke="{RED}" stroke-width="1" stroke-dasharray="3 3"/>')
    o.append(f'<line x1="200" y1="{cusp:.1f}" x2="200" y2="{BOT}" stroke="{RED}" stroke-width="1.5"/>')
    o.append(t(204, 112, "Rz", 13, True, RED))
    # S giữa hai đáy
    o.append('<line x1="50" y1="140" x2="50" y2="178" stroke="currentColor" stroke-dasharray="3 3"/>')
    o.append('<line x1="150" y1="140" x2="150" y2="178" stroke="currentColor" stroke-dasharray="3 3"/>')
    o.append('<line x1="50" y1="172" x2="150" y2="172" stroke="currentColor" stroke-width="1.2"/>')
    o.append(arrow_head(50, 172, "left") + arrow_head(150, 172, "right"))
    o.append(t(100, 192, "S", 13, True, anchor="middle"))
    o.append(t(170, 192, "bước dao tiến mỗi vòng quay"))
    o.append('</svg>')
    return fig("".join(o), "Hình 3. Mũi dao tròn bán kính r tiến S mỗi vòng, để lại các nhấp nhô cao Rz. S nhỏ hoặc r lớn → nhấp nhô thấp.")


# ---------------------------------------------------------------- Hình 4: Rz theo tốc độ cắt
def fig4():
    X0, Y0 = 50, 170

    def vx(v):
        return X0 + v * 3.3

    o = [svg_open(420, 300, "Chiều cao nhấp nhô Rz thay đổi theo tốc độ cắt khi tiện thép cacbon")]
    o.append(f'<line x1="{X0}" y1="{Y0}" x2="400" y2="{Y0}" stroke="currentColor" stroke-width="1.5"/>')
    o.append(f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="28" stroke="currentColor" stroke-width="1.5"/>')
    o.append(arrow_head(400, Y0, "right") + arrow_head(X0, 28, "up"))
    o.append(t(58, 34, "Rz", 13, True))
    o.append(t(400, 202, "v (m/phút)", anchor="end"))
    for v in (30, 60):
        o.append(f'<line x1="{vx(v):.0f}" y1="{Y0}" x2="{vx(v):.0f}" y2="60" stroke="currentColor" stroke-opacity="0.5" stroke-dasharray="4 4"/>')
    for v in (20, 30, 60):
        o.append(t(f"{vx(v):.0f}", 186, str(v), anchor="middle"))
    o.append(f'<path d="M66 135 C90 135 100 62 116 62 C135 62 160 118 199 124 C250 132 320 142 380 146" fill="none" stroke="{RED}" stroke-width="2.5"/>')
    o.append(t(116, 50, "lẹo dao", 12, True, RED, "middle"))
    rows = ["v thấp: phoi dễ tách → Rz nhỏ",
            "v ≈ 15–20 m/phút: lẹo dao → Rz lớn nhất",
            "v ≈ 30–60 m/phút: lẹo dao bị phá huỷ",
            "v &gt; 60 m/phút: không còn lẹo dao → Rz giảm"]
    for i, s in enumerate(rows):
        o.append(t(20, 228 + i * 20, s))
    o.append('</svg>')
    return fig("".join(o), "Hình 4. Rz theo tốc độ cắt khi tiện thép cacbon (dạng đường cong, không theo tỉ lệ).")


# ---------------------------------------------------------------- Hình 5: mòn dao ba giai đoạn
def fig5():
    X0, Y0 = 50, 170
    o = [svg_open(420, 250, "Lượng mòn dao U theo chiều dài đường cắt L, ba giai đoạn")]
    o.append(f'<line x1="{X0}" y1="{Y0}" x2="400" y2="{Y0}" stroke="currentColor" stroke-width="1.5"/>')
    o.append(f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="24" stroke="currentColor" stroke-width="1.5"/>')
    o.append(arrow_head(400, Y0, "right") + arrow_head(X0, 24, "up"))
    o.append(t(58, 30, "U (µm)", 13, True))
    o.append(t(400, 188, "L (m)", anchor="end"))
    for x in (110, 310):
        o.append(f'<line x1="{x}" y1="{Y0}" x2="{x}" y2="40" stroke="currentColor" stroke-opacity="0.5" stroke-dasharray="4 4"/>')
    o.append(f'<path d="M50 170 C60 140 80 130 110 128 L310 95 C335 90 350 70 362 35" fill="none" stroke="{ORANGE}" stroke-width="2.5"/>')
    o.append(t(80, 158, "I", 14, True, anchor="middle"))
    o.append(t(210, 158, "II", 14, True, anchor="middle"))
    o.append(t(350, 158, "III", 14, True, anchor="middle"))
    o.append(f'<text x="170" y="92" fill="{ORANGE}" font-size="12">độ dốc ≈ U<tspan baseline-shift="sub" font-size="10">0</tspan></text>')
    rows = ["I: mòn ban đầu, rất nhanh",
            "II: mòn bình thường, U tăng đều theo L",
            "III: mòn khốc liệt → mài lại hoặc thay dao"]
    for i, s in enumerate(rows):
        o.append(t(20, 206 + i * 20, s))
    o.append('</svg>')
    return fig("".join(o), "Hình 5. Ba giai đoạn mòn dao. Tính sai số do mòn trong giai đoạn II, nơi U tỉ lệ với L.")


# ---------------------------------------------------------------- Hình 6: tang trống và loa kèn
def fig6():
    o = [svg_open(420, 256, "Chi tiết tiện chống tâm hai đầu thành tang trống, kẹp mâm cặp đầu tự do thành loa kèn")]
    # hàng 1: chống tâm hai đầu
    o.append(t(10, 18, "Chống tâm hai đầu (m = 48)", 13, True))
    o.append('<polygon points="26,60 48,70 26,80" fill="currentColor" fill-opacity="0.35" stroke="currentColor"/>')
    o.append('<polygon points="394,60 372,70 394,80" fill="currentColor" fill-opacity="0.35" stroke="currentColor"/>')
    o.append('<rect x="50" y="55" width="320" height="30" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4"/>')
    o.append(f'<path d="M50 57 Q210 43 370 57 L370 83 Q210 97 50 83 Z" fill="{BLUE}" fill-opacity="0.12" stroke="{BLUE}" stroke-width="2"/>')
    o.append(f'<line x1="260" y1="24" x2="260" y2="46" stroke="{RED}" stroke-width="2"/>' + arrow_head(260, 46, "down", RED))
    o.append(t(268, 38, "Py", 13, True, RED))
    o.append(t(10, 116, "→ giữa to, hai đầu nhỏ: TANG TRỐNG", color=BLUE))
    # hàng 2: mâm cặp, đầu tự do
    o.append(t(10, 146, "Kẹp mâm cặp, đầu kia tự do (m = 3)", 13, True))
    o.append('<rect x="20" y="164" width="30" height="62" fill="currentColor" fill-opacity="0.35" stroke="currentColor"/>')
    o.append('<rect x="50" y="180" width="320" height="30" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 4"/>')
    o.append(f'<path d="M50 181 Q250 182 370 172 L370 218 Q250 208 50 209 Z" fill="{ORANGE}" fill-opacity="0.12" stroke="{ORANGE}" stroke-width="2"/>')
    o.append(f'<line x1="340" y1="148" x2="340" y2="168" stroke="{RED}" stroke-width="2"/>' + arrow_head(340, 168, "down", RED))
    o.append(t(348, 162, "Py", 13, True, RED))
    o.append(t(10, 246, "→ đầu tự do to, đầu kẹp nhỏ: LOA KÈN", color=ORANGE))
    o.append('</svg>')
    return fig("".join(o), "Hình 6. Lực Py đẩy chi tiết lùi xa dao; chỗ chi tiết võng nhiều thì bị cắt ít, đường kính to hơn (nét đứt: hình đúng, nét màu: hình thực, phóng đại).")


# ---------------------------------------------------------------- Hình 7: phân bố 100 trục Ø50
FREQ = [2, 12, 18, 27, 23, 15, 3]


def fig7():
    X0, Y0, BW, K = 60, 190, 46, 5
    o = [svg_open(420, 262, "Biểu đồ số chi tiết theo khoảng đường kính của 100 trục và đường cong Gauss")]
    o.append(f'<line x1="40" y1="{Y0}" x2="405" y2="{Y0}" stroke="currentColor" stroke-width="1.5"/>')
    o.append(f'<line x1="40" y1="{Y0}" x2="40" y2="22" stroke="currentColor" stroke-width="1.5"/>')
    o.append(arrow_head(40, 22, "up"))
    o.append(t(48, 26, "số chi tiết", 12, True))
    for i, m in enumerate(FREQ):
        x = X0 + i * BW
        o.append(f'<rect x="{x}" y="{Y0 - m * K}" width="{BW}" height="{m * K}" fill="{BLUE}" fill-opacity="0.3" stroke="{BLUE}" stroke-width="1.2"/>')
        o.append(t(x + BW / 2, 208, str(m), 12, True, BLUE, "middle"))
    for i in range(8):
        o.append(t(X0 + i * BW, 228, f"50,{i * 5:02d}", 12, anchor="middle"))
    o.append(t(4, 208, "m", 12, True, BLUE))
    o.append(t(405, 250, "đường kính (mm)", anchor="end"))
    # đường cong Gauss: trung bình và độ lệch từ chính bảng số liệu
    mids = [50.025 + 0.05 * i for i in range(7)]
    n = sum(FREQ)
    mean = sum(f * m for f, m in zip(FREQ, mids)) / n
    sd = math.sqrt(sum(f * (m - mean) ** 2 for f, m in zip(FREQ, mids)) / n)
    pts = []
    for j in range(0, 161):
        dval = 49.99 + j * (0.37 / 160)
        y = n * 0.05 / (sd * math.sqrt(2 * math.pi)) * math.exp(-((dval - mean) / sd) ** 2 / 2)
        x = X0 + (dval - 50.0) / 0.05 * BW
        pts.append(f"{x:.1f},{Y0 - y * K:.1f}")
    o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{RED}" stroke-width="2"/>')
    o.append(t(300, 50, "đường cong Gauss", 12, True, RED))
    o.append('</svg>')
    return fig("".join(o), "Hình 7. Đường kính của 100 trục tiện trên một máy điều chỉnh sẵn: dồn ở giữa, thưa dần hai bên.")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
for tag, f in (("<!--FIG1-->", fig1), ("<!--FIG2-->", fig2), ("<!--FIG3-->", fig3), ("<!--FIG4-->", fig4),
               ("<!--FIG5-->", fig5), ("<!--FIG6-->", fig6), ("<!--FIG7-->", fig7)):
    assert src.count(tag) == 1, tag
    src = src.replace(tag, f())
pos = [src.find(f"Hình {i}.") for i in range(1, 8)]
assert pos == sorted(pos), "số hình không theo thứ tự xuất hiện"
(HERE / "theory.html").write_text(src, encoding="utf8")
print("đã ghi theory.html")
