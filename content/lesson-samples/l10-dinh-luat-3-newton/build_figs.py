"""Sinh 4 hình SVG cho bài 'Định luật 3 Newton' (lesson 61) và thay mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy: python3 build_figs.py  (từ thư mục bài hoặc gốc repo). In kiểm toạ độ: nhãn không chồng nhau, không vượt viewBox,
mũi tên đúng chiều/độ dài tỉ lệ."""
import pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import RED, BLUE, ORG, GRN, wrap  # noqa: E402

COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}
LABELS = []   # (fig, x0, y0, x1, y1, text)
ARROWS = []   # (fig, tên, x1, y1, x2, y2)
CUR = {"fig": 0}


def defs(p):
    out = "<defs>"
    for n, c in COL.items():
        out += (f'<marker id="{p}-{n}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="12" markerHeight="12" '
                f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
    return out + "</defs>"


def arrow(p, c, x1, y1, x2, y2, w=3, name="", dash=""):
    ARROWS.append((CUR["fig"], name, x1, y1, x2, y2))
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{COL[c]}" stroke-width="{w}"{d} '
            f'marker-end="url(#{p}-{c})"/>')


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def sub(base, s):
    return f'{base}<tspan baseline-shift="sub" font-size="11">{s}</tspan>'


def text(x, y, s, c="currentColor", size=14, anchor="start", weight="700"):
    plain = re.sub(r"<[^>]+>", "", s)
    w = 0.58 * size * len(plain)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    LABELS.append((CUR["fig"], x0, y - 0.75 * size, x0 + w, y + 0.2 * size, plain))
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}">{s}</text>')


def person(x, ground, s=1.0, hand=None):
    """Người trượt băng dạng que; hand = (x, y) điểm bàn tay chạm vật, tay nối từ vai tới đó."""
    hy, ty, fy = ground - 100 * s, ground - 62 * s, ground - 6 * s
    r = 12 * s
    g = f'<circle cx="{x}" cy="{hy:.1f}" r="{r:.1f}" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    g += line(x, hy + r, x, ty, w=2.5) + line(x, ty, x - 12 * s, fy, w=2.5) + line(x, ty, x + 12 * s, fy, w=2.5)
    sh = hy + 24 * s
    if hand:
        g += line(x, sh, hand[0], hand[1], w=2.5)
    g += line(x - 24 * s, ground - 2, x + 24 * s, ground - 2, BLUE, 3)
    return g, sh


VB = {}

# ---------------- Hình 1: đẩy thành sân (mở bài, đặt SAU câu dự đoán) ----------------
CUR["fig"] = 1
VB[1] = (440, 262)
G = 196
b = defs("f1") + line(10, G, 430, G, BLUE, 2, "", .6)
WALL_R = 64
b += f'<rect x="10" y="50" width="{WALL_R-10}" height="{G-50}" fill="rgba(148,163,184,.3)" stroke="currentColor" stroke-width="2"/>'
b += text(10, 38, "Thành sân", "currentColor", 14, "start", "600")
PX = 200
hand = (WALL_R + 2, 108)
g, sh = person(PX, G, 1.0, hand)
b += g
b += arrow("f1", "r", WALL_R, 108, 18, 108, 3.2, "F1")                  # lên thành: gốc ở mặt tiếp xúc, hướng vào thành
b += text(20, 98, sub("F", "1"), RED, 15, "start")
b += arrow("f1", "b", PX + 14, 158, PX + 94, 158, 3.2, "F2")            # lên em: gốc ở thân, hướng ra xa thành
b += text(PX + 100, 163, sub("F", "2"), BLUE, 15, "start")
b += arrow("f1", "g", PX, 64, PX + 90, 64, 3.2, "a", "7 4")
b += text(PX, 50, "em trượt lùi", GRN, 14, "start")
b += text(10, 226, sub("F", "1") + " (đỏ): em đẩy thành, đặt lên thành", RED, 14, "start", "600")
b += text(10, 248, sub("F", "2") + " (xanh): thành đẩy em, đặt lên em", BLUE, 14, "start", "600")
fig1 = wrap(f"0 0 {VB[1][0]} {VB[1][1]}",
            "Em đẩy thành sân: lực F1 đặt lên thành hướng vào thành, phản lực F2 đặt lên em hướng ra xa thành, em trượt lùi", b,
            "Hình 1. <em>F</em><sub>1</sub> đặt lên <strong>thành</strong>, <em>F</em><sub>2</sub> đặt lên <strong>em</strong>: bằng nhau về độ lớn, ngược chiều, ở hai vật khác nhau.")

# ---------------- Hình 2: hai lực kế móc vào nhau ----------------
CUR["fig"] = 2
VB[2] = (440, 190)
b = defs("f2")
L0, L1, R0, R1, Y0, Y1 = 30, 150, 290, 410, 80, 122
for x0, x1 in ((L0, L1), (R0, R1)):
    b += f'<rect x="{x0}" y="{Y0}" width="{x1-x0}" height="{Y1-Y0}" rx="5" fill="rgba(148,163,184,.18)" stroke="currentColor" stroke-width="2"/>'
YM = (Y0 + Y1) / 2
b += line(L1, YM, R0, YM, w=2.5) + f'<circle cx="220" cy="{YM}" r="5" fill="none" stroke="currentColor" stroke-width="2"/>'
b += text((L0 + L1) / 2, YM + 6, "5 N", "currentColor", 17, "middle")
b += text((R0 + R1) / 2, YM + 6, "5 N", "currentColor", 17, "middle")
b += text(L0, 162, "Lực kế 1", "currentColor", 14, "start", "600")
b += text(R1, 162, "Lực kế 2", "currentColor", 14, "end", "600")
AY = 62
b += arrow("f2", "r", L1 + 2, AY, 206, AY, 3.2, "F21")          # lực kế 2 kéo lực kế 1: hướng sang phải (về phía 2), gốc ở móc lực kế 1
b += arrow("f2", "b", R0 - 2, AY, 234, AY, 3.2, "F12")          # lực kế 1 kéo lực kế 2: hướng sang trái, gốc ở móc lực kế 2
b += text(L0, 38, "Lên lực kế 1", RED, 14, "start", "600")
b += text(R1, 38, "Lên lực kế 2", BLUE, 14, "end", "600")
fig2 = wrap(f"0 0 {VB[2][0]} {VB[2][1]}",
            "Hai lực kế móc vào nhau cùng chỉ 5 N; lực kế 2 kéo lực kế 1 sang phải, lực kế 1 kéo lực kế 2 sang trái", b,
            "Hình 2. Kéo mạnh hay nhẹ, hai lực kế vẫn chỉ <strong>bằng nhau</strong>; mỗi lực kế đo lực đặt lên chính nó.")

# ---------------- Hình 3: sách trên bàn ----------------
CUR["fig"] = 3
VB[3] = (420, 290)
b = defs("f3")
BK = (140, 80, 280, 140)       # x0, y0, x1, y1 của quyển sách
TB = (90, 210, 330, 250)       # mặt bàn
b += f'<rect x="{BK[0]}" y="{BK[1]}" width="{BK[2]-BK[0]}" height="{BK[3]-BK[1]}" rx="3" fill="rgba(251,146,60,.15)" stroke="currentColor" stroke-width="2"/>'
b += text(BK[0] + 6, BK[1] - 8, "Quyển sách", "currentColor", 14, "start", "600")
b += f'<rect x="{TB[0]}" y="{TB[1]}" width="{TB[2]-TB[0]}" height="{TB[3]-TB[1]}" rx="3" fill="rgba(56,189,248,.12)" stroke="currentColor" stroke-width="2"/>'
b += line(110, TB[3], 110, 282) + line(310, TB[3], 310, 282)
b += text(TB[0] + 8, TB[1] + 26, "Mặt bàn", "currentColor", 14, "start", "600")
b += arrow("f3", "o", 180, 110, 180, 168, 3.2, "P")              # trọng lực: gốc ở trọng tâm sách, hướng xuống
b += text(170, 186, "P", ORG, 15, "end")
b += arrow("f3", "o", 245, BK[3], 245, 92, 3.2, "N")             # lực nâng lên sách, gốc ở mặt dưới sách, hướng lên
b += text(256, 108, "N", ORG, 15, "start")
b += arrow("f3", "b", 245, TB[1], 245, TB[1] + 34, 3.2, "N'")    # sách ép lên bàn, gốc ở mặt bàn, hướng xuống
b += text(256, TB[1] + 34, "N′", BLUE, 15, "start")
b += line(300, BK[3] + 4, 300, TB[1] - 4, "currentColor", 1.6, "4 4", .8)
b += text(308, 166, "N và N′:", "currentColor", 14, "start", "600")
b += text(308, 184, "lực–phản lực", "currentColor", 14, "start", "600")
b += text(10, 22, "● Cam: lực đặt lên SÁCH", ORG, 14, "start", "600")
b += text(10, 42, "● Xanh: lực đặt lên BÀN", BLUE, 14, "start", "600")
fig3 = wrap(f"0 0 {VB[3][0]} {VB[3][1]}",
            "Sách nằm yên trên bàn: P và N cùng đặt lên sách và cân bằng; N đặt lên sách và N phẩy đặt lên bàn là cặp lực phản lực", b,
            "Hình 3. <em>P</em> và <em>N</em> cùng đặt lên sách: <em>cân bằng</em>. <em>N</em> (lên sách) và <em>N</em>′ (lên bàn) mới là <em>lực – phản lực</em>.")

# ---------------- Hình 4: hai bạn đẩy nhau (bài toán mẫu) ----------------
CUR["fig"] = 4
VB[4] = (440, 238)
G = 190
b = defs("f4") + line(10, G, 430, G, BLUE, 2, "", .6)
HX, HY = 200, 104
gA, _ = person(110, G, 0.9, (HX, HY))
gB, _ = person(310, G, 1.1, (HX, HY))
b += gA + gB
b += text(110, 216, "A: 40 kg", "currentColor", 14, "middle", "600")
b += text(310, 216, "B: 60 kg", "currentColor", 14, "middle", "600")
F_PX = 56          # 120 N -> 56 px
b += arrow("f4", "r", 100, 150, 100 - F_PX, 150, 3.2, "F_BA")      # lực lên A, hướng ra xa B (sang trái)
b += text(24, 140, "120 N", RED, 14, "start")
b += arrow("f4", "r", 320, 150, 320 + F_PX, 150, 3.2, "F_AB")      # lực lên B, hướng ra xa A (sang phải)
b += text(334, 140, "120 N", RED, 14, "start")
A_A, A_B = 120, 80      # a_A = 3, a_B = 2 -> 40 px cho 1 m/s²
b += arrow("f4", "g", 192, 60, 192 - A_A, 60, 3.4, "aA")
b += text(132, 42, sub("a", "A") + " = 3 m/s²", GRN, 14, "middle")
b += arrow("f4", "g", 208, 60, 208 + A_B, 60, 3.4, "aB")
b += text(268, 42, sub("a", "B") + " = 2 m/s²", GRN, 14, "middle")
fig4 = wrap(f"0 0 {VB[4][0]} {VB[4][1]}",
            "Hai bạn đẩy nhau trên giày trượt: lực đỏ bằng nhau 120 N, gia tốc xanh của bạn A nhẹ hơn dài hơn", b,
            "Hình 4. Lực (đỏ) bằng nhau; gia tốc (xanh lá) của bạn A nhẹ hơn <em>dài hơn</em> (3 : 2).")

fig1 = fig1.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-newton3-02"', 1)
fig2 = fig2.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-newton3-01"', 1)
fig3 = fig3.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-newton3-03"', 1)
fig4 = fig4.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-newton3-04"', 1)

# ---------------- Kiểm toạ độ ----------------
bad = []
for i, (f, x0, y0, x1, y1, s) in enumerate(LABELS):
    W, H = VB[f]
    if x0 < 2 or y0 < 2 or x1 > W - 2 or y1 > H - 2:
        bad.append(f"Hình {f}: nhãn '{s}' vượt viewBox ({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f})")
    for g, a0, b0, a1, b1, t in LABELS[i + 1:]:
        if g == f and x0 < a1 and a0 < x1 and y0 < b1 and b0 < y1:
            bad.append(f"Hình {f}: nhãn '{s}' chồng '{t}'")
A = {(f, n): (x1, y1, x2, y2) for f, n, x1, y1, x2, y2 in ARROWS}
# chiều vật lí
def sgn(v): return (v > 0) - (v < 0)
chk = [
    ((1, "F1"), -1, "F1 lên thành, hướng vào thành (trái)"), ((1, "F2"), +1, "F2 lên em, hướng ra xa thành (phải)"),
    ((1, "a"), +1, "em trượt lùi (phải)"),
    ((2, "F21"), +1, "lực kế 2 kéo 1: về phía 2 (phải)"), ((2, "F12"), -1, "lực kế 1 kéo 2: về phía 1 (trái)"),
    ((4, "F_BA"), -1, "lực lên A hướng ra xa B (trái)"), ((4, "F_AB"), +1, "lực lên B hướng ra xa A (phải)"),
    ((4, "aA"), -1, "a_A hướng trái"), ((4, "aB"), +1, "a_B hướng phải"),
]
for k, d, why in chk:
    x1, y1, x2, y2 = A[k]
    if sgn(x2 - x1) != d:
        bad.append(f"Hình {k[0]}: mũi tên {k[1]} sai chiều ({why})")
for k, d, why in ((((3, "P")), -1, "P xuống"), ((3, "N"), +1, "N lên"), ((3, "N'"), -1, "N' xuống")):
    x1, y1, x2, y2 = A[k]
    if sgn(y1 - y2) != d * -1 and not (k[1] in ("P", "N'") and y2 > y1) and not (k[1] == "N" and y2 < y1):
        bad.append(f"Hình 3: mũi tên {k[1]} sai chiều ({why})")
# độ dài tỉ lệ
la = lambda k: abs(A[k][2] - A[k][0])
if abs(la((4, "F_BA")) - la((4, "F_AB"))) > 0.5: bad.append("Hình 4: hai lực không dài bằng nhau")
if abs(la((4, "aA")) / la((4, "aB")) - 1.5) > 0.01: bad.append("Hình 4: tỉ lệ gia tốc a_A : a_B khác 3 : 2")
if abs(la((2, "F21")) - la((2, "F12"))) > 0.5: bad.append("Hình 2: hai lực không dài bằng nhau")
print("\n".join(bad) if bad else "kiểm toạ độ: ok")

src = (HERE / "theory.src.html").read_text(encoding="utf8")
figs = [fig1, fig2, fig3, fig4]
order = [int(n) for n in re.findall(r"<!--FIG(\d)-->", src)]
assert order == sorted(order) == list(range(1, len(figs) + 1)), order
for n, f in enumerate(figs, 1):
    src = src.replace(f"<!--FIG{n}-->", f)

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
