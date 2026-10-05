"""Sinh 4 hình SVG cho bài 'Định luật 1 Newton' (lesson 59), thay mốc <!--FIGn--> trong theory.src.html -> theory.html.
Kèm lớp kiểm hộp nhãn: không vượt viewBox, không chồng nhau (ước lượng bề rộng chữ 0,58·cỡ chữ/ký tự)."""
import math, sys
from svg_lib import RED, BLUE, ORG, GRN, wrap

PHUT = "15"   # lấy từ lint_do_dai.py

LABELS = []   # (hình, x0, y0, x1, y1, nội dung) để kiểm chồng/vượt khung


def defs(p):
    """Marker cố định theo đơn vị viewBox (userSpaceOnUse) — nét dày không làm đầu mũi phình."""
    out = "<defs>"
    for n, c in (("r", RED), ("b", BLUE), ("o", ORG), ("g", GRN)):
        out += (f'<marker id="{p}-{n}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="12" markerHeight="12" '
                f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
    return out + "</defs>"


COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN}


def arrow(p, c, x1, y1, x2, y2, w=3, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{COL[c]}" stroke-width="{w}"{d} '
            f'marker-end="url(#{p}-{c})"/>')


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def text(fig, x, y, s, c="currentColor", size=14, anchor="start", weight="600", plain=None):
    n = len(plain if plain is not None else s)
    wdt = 0.58 * size * n
    x0 = x if anchor == "start" else (x - wdt / 2 if anchor == "middle" else x - wdt)
    LABELS.append((fig, x0, y - size * 0.8, x0 + wdt, y + size * 0.2, plain if plain is not None else s))
    return f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{s}</text>'


def sub(base, s):
    return f'{base}<tspan baseline-shift="sub" font-size="11">{s}</tspan>'


def ball(x, y, r=7, c=ORG):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}" stroke="currentColor" stroke-width="1.5"/>'


# ---------------------------------------------------------------- Hình 1: thí nghiệm Galilei
GY, TOP = 200, 70            # mặt đất, độ cao thả bi (h0 = 130 px)
A = (20, TOP); B = (130, GY)  # máng (1)
H_DOC, H_THOAI = 108, 96     # độ cao bi lên được (thấp hơn h0 = 130 vì ma sát; máng thoải mất nhiều hơn)
a_doc, a_thoai = 50, 22
E_doc = (B[0] + H_DOC / math.tan(math.radians(a_doc)), GY - H_DOC)
E_thoai = (B[0] + H_THOAI / math.tan(math.radians(a_thoai)), GY - H_THOAI)


def on_ramp(P0, P1, t, r=7):
    """Tâm bi nằm trên máng P0->P1 tại tham số t, nhấc lên theo pháp tuyến hướng lên."""
    x = P0[0] + t * (P1[0] - P0[0]); y = P0[1] + t * (P1[1] - P0[1])
    dx, dy = P1[0] - P0[0], P1[1] - P0[1]; L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L
    if ny > 0: nx, ny = -nx, -ny
    return x + nx * r, y + ny * r


b = defs("f1")
b += line(12, TOP, 430, TOP, "currentColor", 1.4, "6 5", .6)
b += text(1, 250, 62, "độ cao ban đầu", "currentColor", 14)
b += line(12, GY, 432, GY, "currentColor", 2.6)
b += line(*A, *B, "currentColor", 3)
b += line(*B, *E_doc, "currentColor", 2.6, "", .85)
b += line(*B, *E_thoai, "currentColor", 2.6, "", .85)
b += ball(*on_ramp(A, B, 0.06))
b += ball(*on_ramp(B, E_doc, 1.0))
b += ball(*on_ramp(B, E_thoai, 1.0))
b += ball(262, GY - 7)
b += arrow("f1", "g", 282, 186, 420, 186, 3)
b += text(1, 12, 175, "máng (1)", "currentColor", 14)
b += text(1, 236, 104, "(2) dốc", "currentColor", 14)
b += text(1, 350, 124, "(2) thoải", "currentColor", 14)
b += text(1, 282, 176, "nằm ngang: lăn mãi", GRN, 14, weight="700")
fig1 = wrap("0 0 440 214", "Thí nghiệm Galilei: bi lăn từ máng 1 lên máng 2; máng 2 càng thoải bi càng lăn xa; máng 2 nằm ngang thì bi lăn mãi",
            b, "Hình 1. Bi thả từ độ cao ban đầu trên máng (1). Máng (2) càng thoải, bi lăn càng xa nhưng lên hơi thấp hơn độ cao ban đầu; máng (2) nằm ngang, không ma sát thì bi lăn mãi. Sơ đồ minh hoạ, không theo tỉ lệ.")
fig1 = fig1.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-dl1-newton-01"', 1)

# ---------------------------------------------------------------- Hình 2: ô tô chạy thẳng đều
C = (220, 148); LH, LV = 90, 70     # lực ngang bằng nhau, lực đứng bằng nhau
b = defs("f2")
b += line(20, 192, 420, 192, "currentColor", 2.4, "", .7)
b += '<rect x="150" y="125" width="140" height="45" rx="6" fill="rgba(148,163,184,.18)" stroke="currentColor" stroke-width="2.4"/>'
b += '<path d="M178,125 L192,100 L246,100 L262,125" fill="none" stroke="currentColor" stroke-width="2.4"/>'
b += '<circle cx="182" cy="178" r="13" fill="none" stroke="currentColor" stroke-width="2.4"/><circle cx="262" cy="178" r="13" fill="none" stroke="currentColor" stroke-width="2.4"/>'
b += arrow("f2", "r", C[0], C[1], 290 + LH, C[1], 3.4)
b += arrow("f2", "b", C[0], C[1], 150 - LH, C[1], 3.4)
b += arrow("f2", "o", C[0], C[1], C[0], C[1] - LV, 3.2)
b += arrow("f2", "o", C[0], C[1], C[0], C[1] + LV, 3.2)
b += f'<circle cx="{C[0]}" cy="{C[1]}" r="3.5" fill="currentColor"/>'
b += arrow("f2", "g", 40, 40, 140, 40, 3)
b += text(2, 40, 26, "v không đổi", GRN, 14, weight="700")
b += text(2, 335, 136, sub("F", "k"), RED, 16, "middle", "700", plain="Fk")
b += text(2, 105, 136, sub("F", "c"), BLUE, 16, "middle", "700", plain="Fc")
b += text(2, 230, 92, "N", ORG, 16, "start", "700")
b += text(2, 230, 214, "P", ORG, 16, "start", "700")
b += text(2, 290, 222, "hợp lực = 0", "currentColor", 14, weight="700")
fig2 = wrap("0 0 440 240", "Ô tô chạy thẳng đều: lực kéo Fk cân bằng lực cản Fc, lực đỡ N cân bằng trọng lực P, hợp lực bằng không",
            b, "Hình 2. Ô tô chạy thẳng đều: <em>F</em><sub>k</sub> = <em>F</em><sub>c</sub> và <em>N</em> = <em>P</em> (mũi tên dài bằng nhau từng cặp), hợp lực bằng 0 nên vận tốc không đổi.")

fig2 = fig2.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-dl1-newton-03"', 1)

# ---------------------------------------------------------------- Hình 3: đồng xu, tấm bìa, chiếc cốc
def glass(cx):
    return (f'<path d="M{cx-40},95 L{cx-30},195 L{cx+30},195 L{cx+40},95" fill="rgba(56,189,248,.10)" '
            f'stroke="currentColor" stroke-width="2.4"/>')


def coin(x, y, dash=""):
    d = f' stroke-dasharray="{dash}" fill="none"' if dash else f' fill="{ORG}"'
    return f'<ellipse cx="{x}" cy="{y}" rx="16" ry="5"{d} stroke="currentColor" stroke-width="1.6"/>'


b = defs("f3")
b += glass(110) + '<rect x="55" y="88" width="110" height="7" rx="1.5" fill="rgba(148,163,184,.45)" stroke="currentColor" stroke-width="1.6"/>'
b += coin(110, 82)
b += arrow("f3", "r", 14, 91.5, 50, 91.5, 3.4)
b += text(3, 12, 70, "búng nhanh", RED, 14, weight="700")
b += text(3, 110, 222, "Trước", "currentColor", 14, "middle", "700")
b += glass(320)
b += '<rect x="372" y="72" width="56" height="7" rx="1.5" fill="rgba(148,163,184,.45)" stroke="currentColor" stroke-width="1.6"/>'
b += arrow("f3", "g", 374, 90, 428, 90, 3)
b += text(3, 399, 60, "tấm bìa", "currentColor", 14, "middle")
b += coin(320, 82, "4 3")
b += arrow("f3", "b", 320, 90, 320, 178, 3, "6 4")
b += coin(320, 188)
b += text(3, 176, 140, "xu rơi thẳng", BLUE, 14, weight="700")
b += text(3, 176, 158, "vào cốc", BLUE, 14, weight="700")
b += text(3, 320, 222, "Sau", "currentColor", 14, "middle", "700")
fig3 = wrap("0 0 440 232", "Búng nhanh tấm bìa: bìa bay ra, đồng xu rơi thẳng vào cốc nhờ quán tính",
            b, "Hình 3. Búng nhanh: bìa bay ra, đồng xu giữ vận tốc ngang bằng 0 nên rơi thẳng vào cốc.")

# ---------------------------------------------------------------- Hình 4: xe buýt phanh gấp
b = defs("f4")
b += '<rect x="30" y="60" width="390" height="130" rx="12" fill="none" stroke="currentColor" stroke-width="2.4"/>'
b += line(10, 214, 432, 214, "currentColor", 2.2, "", .7)
b += '<circle cx="100" cy="200" r="14" fill="none" stroke="currentColor" stroke-width="2.4"/><circle cx="350" cy="200" r="14" fill="none" stroke="currentColor" stroke-width="2.4"/>'
FOOT1, FOOT2, HIP, NECK, HEAD = (205, 188), (221, 188), (222, 146), (250, 106), (258, 93)
st = 'stroke="currentColor" stroke-width="2.6" stroke-linecap="round"'
b += f'<line x1="{FOOT1[0]}" y1="{FOOT1[1]}" x2="{HIP[0]}" y2="{HIP[1]}" {st}/><line x1="{FOOT2[0]}" y1="{FOOT2[1]}" x2="{HIP[0]}" y2="{HIP[1]}" {st}/>'
b += f'<line x1="{HIP[0]}" y1="{HIP[1]}" x2="{NECK[0]}" y2="{NECK[1]}" {st}/>'
b += f'<line x1="246" y1="114" x2="272" y2="134" {st}/>'
b += f'<circle cx="{HEAD[0]}" cy="{HEAD[1]}" r="11" fill="none" {st}/>'
b += arrow("f4", "g", 50, 36, 150, 36, 3)
b += text(4, 160, 41, "xe phanh: v giảm", GRN, 14, weight="700")
b += arrow("f4", "b", 213, 182, 150, 182, 3.2)
b += text(4, 44, 170, "sàn giữ chân lại", BLUE, 14, weight="700")
b += arrow("f4", "o", 273, 93, 350, 93, 3, "6 4")
b += text(4, 262, 80, "thân giữ vận tốc cũ", ORG, 14, weight="700")
fig4 = wrap("0 0 440 224", "Xe buýt phanh gấp: sàn giữ chân hành khách chậm lại, thân người giữ vận tốc cũ nên chúi về phía trước",
            b, "Hình 4. Phanh gấp: sàn chỉ giữ <em>chân</em> chậm lại cùng xe; phần thân trên (không có gì giữ riêng) có xu hướng giữ vận tốc cũ nên vẫn đi tới. Không có \"lực quán tính\" nào đẩy người.")


# ---------------------------------------------------------------- kiểm nhãn
VB = {1: (440, 214), 2: (440, 240), 3: (440, 232), 4: (440, 224)}
bad = []
for i, (f, x0, y0, x1, y1, s) in enumerate(LABELS):
    W, H = VB[f]
    if x0 < 2 or x1 > W - 2 or y0 < 2 or y1 > H - 2:
        bad.append(f"hình {f}: nhãn '{s}' vượt khung ({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f})")
    for g, a0, b0, a1, b1, t in LABELS[i + 1:]:
        if g == f and x0 < a1 and a0 < x1 and y0 < b1 and b0 < y1:
            bad.append(f"hình {f}: '{s}' chồng '{t}'")
# nhãn hình 1 không bị máng cắt: kiểm điểm trên máng (2) thoải dưới hộp nhãn
for f, x0, y0, x1, y1, s in LABELS:
    if f != 1: continue
    for X in (x0, x1):
        for (P0, P1) in ((A, B), (B, E_doc), (B, E_thoai)):
            if min(P0[0], P1[0]) <= X <= max(P0[0], P1[0]):
                Y = P0[1] + (X - P0[0]) * (P1[1] - P0[1]) / (P1[0] - P0[0])
                if y0 - 1 <= Y <= y1 + 1:
                    bad.append(f"hình 1: máng cắt nhãn '{s}' tại x={X:.0f}")
print("E_doc", tuple(round(v, 1) for v in E_doc), "E_thoai", tuple(round(v, 1) for v in E_thoai))
if bad:
    print("\n".join(bad)); sys.exit(1)

h = open("theory.src.html", encoding="utf8").read().replace("__PHUT__", PHUT)
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(h)
print("ok", len(h), "nhãn", len(LABELS))
