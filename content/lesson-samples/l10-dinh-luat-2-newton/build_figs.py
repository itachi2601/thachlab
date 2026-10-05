"""Sinh 5 hình SVG cho bài 'Định luật 2 Newton' (lesson 60) và thay mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy: python3 build_figs.py  (từ thư mục bài hoặc gốc repo). In kiểm toạ độ: nhãn không chồng nhau, không vượt viewBox."""
import math, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import RED, BLUE, ORG, GRN, wrap  # noqa: E402

COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}
LABELS = []   # (fig, x0, y0, x1, y1, text) để kiểm chồng chữ


def defs(p):
    """Marker cỡ cố định theo đơn vị viewBox (markerUnits=userSpaceOnUse) để nét dày không phóng to đầu mũi."""
    out = "<defs>"
    for n, c in COL.items():
        out += (f'<marker id="{p}-{n}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="12" markerHeight="12" '
                f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
    return out + "</defs>"


def arrow(p, c, x1, y1, x2, y2, w=3, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{COL[c]}" stroke-width="{w}"{d} '
            f'marker-end="url(#{p}-{c})"/>')


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def sub(base, s):
    return f'{base}<tspan baseline-shift="sub" font-size="11">{s}</tspan>'


CUR = {"fig": 0}


def text(x, y, s, c="currentColor", size=14, anchor="start", weight="700"):
    plain = re.sub(r"<[^>]+>", "", s)
    w = 0.58 * size * len(plain)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    LABELS.append((CUR["fig"], x0, y - 0.75 * size, x0 + w, y + 0.2 * size, plain))
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}">{s}</text>')


def person(x, ground, s=1.0):
    """Người trượt băng dạng que (đầu, thân, hai chân, lưỡi giày); trả (svg, toạ độ y vai)."""
    hy, ty, fy = ground - 100 * s, ground - 62 * s, ground - 6 * s
    r = 12 * s
    g = f'<circle cx="{x}" cy="{hy:.1f}" r="{r:.1f}" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    g += line(x, hy + r, x, ty, w=2.5) + line(x, ty, x - 12 * s, fy, w=2.5) + line(x, ty, x + 12 * s, fy, w=2.5)
    sh = hy + 24 * s
    g += line(x, sh, x + 14 * s, sh + 22 * s, w=2.5)            # tay buông ra trước
    g += line(x - 24 * s, ground - 2, x + 24 * s, ground - 2, BLUE, 3)
    return g, hy, r


VB = {}

# ---------------- Hình 1: cùng lực đẩy 80 N, hai khối lượng ----------------
CUR["fig"] = 1
VB[1] = (440, 250)
G = 215
b = defs("f1") + line(10, G, 430, G, "currentColor", 2, "", .6)
F_LEN = 48                       # cùng lực 80 N -> cùng chiều dài
A_PX = 50                        # 50 px cho 1 m/s²
for x, s, m, name in ((100, 0.85, 40, "Bạn nhỏ"), (310, 1.15, 80, "Chú HLV")):
    g, hy, r = person(x, G, s)
    b += g
    back_y = G - 75 * s
    b += arrow("f1", "r", x - 5 - F_LEN - 3, back_y, x - 5 - 3, back_y, 3.2)
    b += text(x - 16, back_y + 22, "F = 80 N", RED, 14, "end")
    a = 80 / m
    b += arrow("f1", "g", x - 20, 72, x - 20 + a * A_PX, 72, 3.4)
    b += text(x - 20, 58, f"a = {a:g} m/s²".replace(".", ","), GRN, 14, "start")
    b += text(x, 238, f"{name} {m} kg", "currentColor", 14, "middle", "600")
fig1 = wrap(f"0 0 {VB[1][0]} {VB[1][1]}",
            "Cùng lực đẩy 80 N: bạn nhỏ 40 kg có gia tốc 2 m/s², người lớn 80 kg có gia tốc 1 m/s²", b,
            "Hình 1. Cùng lực đẩy (mũi tên đỏ dài bằng nhau), người có khối lượng gấp đôi chỉ có gia tốc bằng một nửa (mũi tên xanh lá).")

# ---------------- Hình 2: bố trí thí nghiệm ----------------
CUR["fig"] = 2
VB[2] = (440, 230)
T = 140                                        # mặt máng
b = defs("f2")
b += f'<rect x="20" y="{T}" width="340" height="12" fill="rgba(148,163,184,.18)" stroke="currentColor" stroke-width="2"/>'
b += f'<rect x="92" y="114" width="68" height="24" rx="3" fill="rgba(251,146,60,.2)" stroke="currentColor" stroke-width="2.2"/>'
b += f'<rect x="160" y="119" width="12" height="12" rx="1" fill="rgba(248,113,113,.25)" stroke="{RED}" stroke-width="1.8"/>'   # cảm biến lực gắn đầu xe
PX, PY, PR = 372, 130, 10                       # ròng rọc
b += line(356, T, PX, PY, "currentColor", 2) + f'<circle cx="{PX}" cy="{PY}" r="{PR}" fill="none" stroke="currentColor" stroke-width="2"/>'
b += line(172, PY - PR + 5, 196, PY - PR + 5, "currentColor", 1.4)    # dây từ cảm biến
b += line(196, PY - PR + 5, PX - PR + 1, PY - PR + 5, "currentColor", 1.4)
b += line(PX + PR, PY, PX + PR, 186, "currentColor", 1.4)          # dây đứng, tiếp tuyến mép phải
b += f'<rect x="{PX+PR-11}" y="186" width="22" height="26" rx="2" fill="rgba(148,163,184,.3)" stroke="currentColor" stroke-width="2"/>'
b += arrow("f2", "r", 198, 125, 232, 125, 3)
b += text(215, 115, "F", RED, 15, "middle")
for gx, lab in ((178, "cổng 1"), (298, "cổng 2")):
    b += f'<path d="M{gx-8},{T} V92 H{gx+8} V{T}" fill="none" stroke="{BLUE}" stroke-width="2.4"/>'
    b += text(gx, 82, lab, BLUE, 13, "middle")
b += text(126, 131, "xe", "currentColor", 13, "middle")
b += text(164, 104, "cảm biến lực", RED, 13, "end", "600")
# kích thước s
b += line(178, 172, 298, 172, "currentColor", 1.4) + line(178, 165, 178, 179, "currentColor", 1.4) + line(298, 165, 298, 179, "currentColor", 1.4)
b += text(238, 194, "s = 0,50 m", "currentColor", 14, "middle")
b += text(PX - 2, 224, "quả nặng", "currentColor", 13, "end", "600")
fig2 = wrap(f"0 0 {VB[2][0]} {VB[2][1]}",
            "Xe trên máng đệm khí xuất phát tại cổng quang 1, dây qua cảm biến lực và ròng rọc treo quả nặng; hai cổng quang cách nhau s = 0,50 m", b,
            "Hình 2. Xe trên máng đệm khí xuất phát tại cổng 1; quả nặng kéo xe qua dây vắt ròng rọc, cảm biến ở đầu xe đo lực <em>F</em>, hai cổng quang đo thời gian <em>t</em> xe đi hết <em>s</em> = 0,50 m.")

# ---------------- Hình 3: đồ thị a theo F ----------------
CUR["fig"] = 3
VB[3] = (440, 230)
OX, OY, SX, SY = 64, 192, 600, 150          # px/N, px/(m/s²)
data = [(0.10, 0.19), (0.20, 0.41), (0.30, 0.58), (0.40, 0.81)]
b = defs("f3")
b += arrow("f3", "k", OX, OY, 400, OY, 2) + arrow("f3", "k", OX, OY, OX, 28, 2)
for F in (0.1, 0.2, 0.3, 0.4):
    x = OX + SX * F
    b += line(x, OY - 4, x, OY + 4, "currentColor", 1.5) + text(x, OY + 20, f"{F:.1f}".replace(".", ","), "currentColor", 13, "middle", "500")
for a in (0.2, 0.4, 0.6, 0.8):
    y = OY - SY * a
    b += line(OX - 4, y, OX + 4, y, "currentColor", 1.5) + text(OX - 8, y + 5, f"{a:.1f}".replace(".", ","), "currentColor", 13, "end", "500")
    b += line(OX, y, 400, y, "currentColor", 1, "3 5", .25)
b += text(OX - 8, OY + 20, "0", "currentColor", 13, "end", "500")
FM = 0.46
b += line(OX, OY, OX + SX * FM, OY - SY * FM / 0.50, GRN, 2.4)
pts = [(OX + SX * F, OY - SY * a) for F, a in data]
for x, y in pts:
    b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{ORG}" stroke="currentColor" stroke-width="1"/>'
b += text(430, OY + 20, "F (N)", "currentColor", 14, "end")
b += text(OX + 8, 30, "a (m/s²)", "currentColor", 14, "start")
b += text(200, 88, "a = F/0,50", GRN, 14, "middle")
fig3 = wrap(f"0 0 {VB[3][0]} {VB[3][1]}",
            "Đồ thị gia tốc theo lực: bốn điểm đo nằm sát đường thẳng qua gốc a = F/0,50", b,
            "Hình 3. Bốn điểm đo (cam) nằm sát đường thẳng qua gốc: gia tốc tỉ lệ thuận với lực.")

# ---------------- Hình 4: phanh xe — a ngược chiều v ----------------
CUR["fig"] = 4
VB[4] = (440, 205)
R = 165
b = defs("f4") + line(10, R, 430, R, "currentColor", 2, "", .6)
b += f'<rect x="150" y="112" width="140" height="38" rx="6" fill="rgba(56,189,248,.12)" stroke="currentColor" stroke-width="2.2"/>'
b += f'<path d="M178,112 L198,90 H250 L272,112" fill="none" stroke="currentColor" stroke-width="2.2"/>'
for wx in (182, 258):
    b += f'<circle cx="{wx}" cy="155" r="10" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2.4"/>'
b += arrow("f4", "b", 170, 40, 290, 40, 3.2)
b += text(170, 28, "v: xe vẫn chạy tới", BLUE, 14, "start")
b += arrow("f4", "g", 270, 72, 190, 72, 3.2)
b += text(182, 77, "a", GRN, 15, "end")
b += arrow("f4", "r", 262, 186, 182, 186, 3.2)
b += text(174, 191, sub("F", "hãm"), RED, 15, "end")
fig4 = wrap(f"0 0 {VB[4][0]} {VB[4][1]}",
            "Xe đang chạy sang phải thì phanh: vận tốc hướng phải, lực hãm và gia tốc hướng trái", b,
            "Hình 4. Khi phanh, lực hãm (đỏ) và gia tốc (xanh lá) cùng hướng ra sau, còn vận tốc (xanh dương) vẫn hướng tới.")

# ---------------- Hình 5: lực lên xe đẩy ----------------
CUR["fig"] = 5
VB[5] = (440, 240)
FL = 190
b = defs("f5") + line(10, FL, 430, FL, "currentColor", 2, "", .6)
b += f'<rect x="170" y="130" width="100" height="50" rx="3" fill="rgba(251,146,60,.18)" stroke="currentColor" stroke-width="2.2"/>'
for wx in (186, 254):
    b += f'<circle cx="{wx}" cy="185" r="5" fill="none" stroke="currentColor" stroke-width="2"/>'
CX, CY = 220, 155
b += f'<circle cx="{CX}" cy="{CY}" r="3.5" fill="currentColor"/>'
b += arrow("f5", "r", 80, 150, 80 + 90 - 2.6, 150, 3.2)            # F = 90 N -> 90 px, đầu mũi chạm thành xe
b += text(120, 140, "F = 90 N", RED, 14, "middle")
b += arrow("f5", "o", 262, 200, 262 - 30, 200, 3.2)                # Fms = 30 N -> 30 px, đặt ở chỗ tiếp xúc
b += text(268, 205, sub("F", "ms") + " = 30 N", ORG, 14, "start")
b += arrow("f5", "k", CX, CY, CX, CY + 60, 2.6)
b += text(CX - 8, CY + 66, "P", "currentColor", 15, "end")
b += arrow("f5", "k", CX, CY, CX, CY - 60, 2.6)            # N cùng điểm đặt với P (trọng tâm)
b += text(CX + 8, CY - 50, "N", "currentColor", 15, "start")
b += arrow("f5", "g", 300, 100, 360, 100, 3.4)
b += text(366, 105, "a", GRN, 15, "start")
b += text(244, 172, "60 kg", "currentColor", 13, "middle", "600")
b += arrow("f5", "k", 30, 226, 90, 226, 2)
b += text(96, 231, "chiều +", "currentColor", 13, "start", "600")
fig5 = wrap(f"0 0 {VB[5][0]} {VB[5][1]}",
            "Bốn lực lên xe đẩy: lực đẩy F 90 N, ma sát 30 N, trọng lực P và phản lực N; gia tốc a hướng theo chiều đẩy", b,
            "Hình 5. Lực lên xe đẩy. <em>F</em> và <em>F</em><sub>ms</sub> vẽ đúng tỉ lệ 3 : 1; <em>P</em>, <em>N</em> vẽ thu nhỏ, triệt tiêu nhau.")

fig3 = fig3.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-dl2-newton-01"', 1)
fig2 = fig2.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-dl2-newton-01"', 1)

# ---------------- Kiểm toạ độ nhãn ----------------
bad = []
for i, (f, x0, y0, x1, y1, s) in enumerate(LABELS):
    W, H = VB[f]
    if x0 < 2 or y0 < 2 or x1 > W - 2 or y1 > H - 2:
        bad.append(f"Hình {f}: nhãn '{s}' vượt viewBox ({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f})")
    for g, a0, b0, a1, b1, t in LABELS[i + 1:]:
        if g == f and x0 < a1 and a0 < x1 and y0 < b1 and b0 < y1:
            bad.append(f"Hình {f}: nhãn '{s}' chồng '{t}'")
# điểm đo của hình 3 phải nằm sát đường a = F/0,50 (lệch ≤ 0,03 m/s² = 4,5 px)
for F, a in data:
    dev = abs(a - F / 0.50) * SY
    if dev > 4.5:
        bad.append(f"Hình 3: điểm F={F} lệch {dev:.1f}px khỏi đường")
print("\n".join(bad) if bad else "kiểm toạ độ: ok")

src = (HERE / "theory.src.html").read_text(encoding="utf8")
# thứ tự xuất hiện trong bài: sơ đồ thí nghiệm, đồ thị, sân băng, phanh xe, xe đẩy; số "Hình n." đánh lại theo thứ tự này
figs = [re.sub(r"<figcaption>Hình \d\.", f"<figcaption>Hình {n}.", f) for n, f in enumerate((fig2, fig3, fig1, fig4, fig5), 1)]
order = [int(n) for n in re.findall(r"<!--FIG(\d)-->", src)]
assert order == sorted(order) == list(range(1, len(figs) + 1)), order
for n, f in enumerate(figs, 1):
    src = src.replace(f"<!--FIG{n}-->", f)

# số phút ở khung Mục tiêu lấy từ lint_do_dai (chạy 2 lượt: lượt 1 đo, lượt 2 ghi)
lint = HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = HERE / "theory.html"
out.write_text(src.replace("__PHUT__", "?"), encoding="utf8")
r = subprocess.run([sys.executable, str(lint), str(out), "--json"], capture_output=True, text=True)
m = re.search(r'"phut"\s*:\s*([\d.]+)', r.stdout) or re.search(r'"minutes"\s*:\s*([\d.]+)', r.stdout)
phut = round(float(m.group(1))) if m else None
if phut is None:
    print("KHÔNG đọc được số phút từ lint_do_dai:", r.stdout[:300])
    phut = "?"
out.write_text(src.replace("__PHUT__", str(phut)), encoding="utf8")
print("ok", len(src), "ký tự; phút =", phut)
