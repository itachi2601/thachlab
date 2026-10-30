"""Sinh 5 hình SVG cho bài 'Lực cản và lực nâng' (lesson 64) và thay mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy: python3 build_figs.py (từ thư mục bài hoặc gốc repo).
Kiểm toạ độ: nhãn không chồng nhau, không vượt viewBox, không bị mũi tên/đường cắt xuyên; đường v–t đúng phương trình."""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import math, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import RED, BLUE, ORG, GRN, wrap, chevron  # noqa: E402

COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}
LABELS = []   # (fig, x0, y0, x1, y1, text)
SEGS = []     # (fig, x1, y1, x2, y2) mũi tên / đường cần tránh nhãn
CUR = {"fig": 0}


def defs(p):
    """Không còn marker tam giác (đầu mũi V 30° vẽ bằng chevron của svg_lib)."""
    return ""


def arrow(p, c, x1, y1, x2, y2, w=3, dash=""):
    """Thân thẳng + đầu V 30° (svg_lib.chevron), thân ≤ 2,8."""
    SEGS.append((CUR["fig"], x1, y1, x2, y2))
    d = f' stroke-dasharray="{dash}"' if dash else ""
    ww = min(w, 2.8)
    n = math.hypot(x2 - x1, y2 - y1)
    L = max(5, min(3.4 * ww + 2, 0.6 * n))
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{COL[c]}" stroke-width="{ww}"{d}/>'
            + chevron(x2, y2, x2 - x1, y2 - y1, COL[c], ww, L))


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, track=True):
    if track:
        SEGS.append((CUR["fig"], x1, y1, x2, y2))
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def sub(base, s):
    return f'<tspan font-style="italic">{base}</tspan><tspan baseline-shift="sub" font-size="14">{s}</tspan>'


def it(s):
    return f'<tspan font-style="italic">{s}</tspan>'


def text(x, y, s, c="currentColor", size=14, anchor="start", weight="700"):
    plain = re.sub(r"<[^>]+>", "", s)
    w = 0.58 * size * len(plain)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    LABELS.append((CUR["fig"], x0, y - 0.75 * size, x0 + w, y + 0.25 * size, plain))
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}">{s}</text>')


def dot(x, y, r=4.5):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="currentColor"/>'


VB = {}

# ---------------- Hình 1: tờ giấy phẳng và viên giấy vo, cùng trọng lượng ----------------
CUR["fig"] = 1
VB[1] = (440, 256)
PL = 70                                    # cùng trọng lượng -> P dài bằng nhau
b = defs("f1")
b += line(12, 36, 428, 36, "currentColor", 1.4, "5 5", .6, track=False)
b += text(428, 26, "cùng độ cao thả", "currentColor", 14, "end", "600")
# tờ phẳng: rơi chậm, mới xuống ít
FX, FY = 120, 112
b += f'<rect x="{FX-45}" y="{FY-3}" width="90" height="6" rx="1" fill="rgba(148,163,184,.35)" stroke="currentColor" stroke-width="1.6"/>'
b += arrow("f1", "r", FX, FY, FX, FY + PL, 3)
b += arrow("f1", "b", FX, FY, FX, FY - 58, 3)
b += dot(FX, FY, 3.5)
b += text(FX + 10, FY + PL - 4, it("P"), RED, 15)
b += text(FX + 10, FY - 44, sub("F", "c") + " lớn", BLUE, 15)
b += text(FX, FY + PL + 30, "tờ giấy phẳng", "currentColor", 14, "middle", "600")
# viên giấy vo: rơi nhanh, đã xuống thấp hơn
BX, BY, BR = 320, 150, 10
b += f'<circle cx="{BX}" cy="{BY}" r="{BR}" fill="rgba(148,163,184,.35)" stroke="currentColor" stroke-width="1.6"/>'
b += arrow("f1", "r", BX, BY, BX, BY + PL, 3)
b += arrow("f1", "b", BX, BY, BX, BY - 24, 3)
b += dot(BX, BY, 3)
b += text(BX + 10, BY + PL - 4, it("P"), RED, 15)
b += text(BX + 14, BY - 16, sub("F", "c") + " nhỏ", BLUE, 15)
b += text(BX, BY + PL + 28, "viên giấy vo tròn", "currentColor", 14, "middle", "600")
fig1 = wrap(f"0 0 {VB[1][0]} {VB[1][1]}",
            "Tờ giấy phẳng và viên giấy vo tròn cùng trọng lượng P; lực cản lên tờ phẳng lớn hơn nhiều nên nó rơi chậm hơn", b,
            "Hình 1. Cùng trọng lượng <em>P</em> (mũi tên đỏ dài bằng nhau). Cùng một lúc sau khi thả, lực cản lên tờ phẳng (xanh) lớn hơn nhiều nên nó còn ở cao hơn.")

# ---------------- Hình 2: lực lên vật rơi ở ba giai đoạn ----------------
CUR["fig"] = 2
VB[2] = (440, 244)
CY, PL = 118, 70
b = defs("f2")
for x, n, fc, note in ((75, 1, 0, ("a ≈ g",)), (220, 2, 40, ("a giảm dần",)), (365, 3, 70, ("a = 0", "v không đổi"))):
    b += text(x, 22, f"Giai đoạn {n}", "currentColor", 14, "middle")
    b += arrow("f2", "r", x, CY, x, CY + PL, 3)
    b += text(x + 10, CY + PL - 6, it("P"), RED, 15)
    if fc:
        b += arrow("f2", "b", x, CY, x, CY - fc, 3)
        b += text(x + 10, CY - fc + 16, sub("F", "c"), BLUE, 15)
    else:
        b += text(x + 10, CY - 10, sub("F", "c") + " ≈ 0", BLUE, 15)
    b += dot(x, CY)
    for k, ln in enumerate(note):
        b += text(x, 214 + 18 * k, ln, GRN, 14, "middle", "600")
fig2 = wrap(f"0 0 {VB[2][0]} {VB[2][1]}",
            "Lực lên vật rơi trong không khí ở ba giai đoạn: lực cản tăng dần từ gần 0 đến bằng trọng lượng", b,
            "Hình 2. Trọng lượng <em>P</em> không đổi; lực cản <em>F</em><sub>c</sub> lớn dần theo tốc độ. Khi <em>F</em><sub>c</sub> = <em>P</em>, hợp lực bằng 0 và vật rơi đều.")

# ---------------- Hình 3: đồ thị v–t của người nhảy dù (chưa mở dù) ----------------
CUR["fig"] = 3
VB[3] = (440, 240)
OX, OY, ST, SV = 56, 200, 22, 2.6        # px/s, px/(m/s)
VT, G = 50.0, 9.8


def vt(t):
    return VT * math.tanh(G * t / VT)


b = defs("f3")
b += arrow("f3", "k", OX, OY, 424, OY, 2) + arrow("f3", "k", OX, OY, OX, 18, 2)
for t in (5, 10, 15):
    x = OX + ST * t
    b += line(x, OY - 4, x, OY + 4, "currentColor", 1.5, track=False) + text(x, OY + 20, str(t), "currentColor", 14, "middle", "500")
for v in (25, 50):
    y = OY - SV * v
    b += line(OX - 4, y, OX + 4, y, "currentColor", 1.5, track=False) + text(OX - 8, y + 5, str(v), "currentColor", 14, "end", "500")
b += text(OX - 8, OY + 20, "0", "currentColor", 14, "end", "500")
YA = OY - SV * VT
b += line(OX, YA, 410, YA, BLUE, 1.6, "6 5", .9, track=False)
b += text(410, YA - 6, "tốc độ giới hạn", BLUE, 14, "end", "600")
T1 = 4.0                                   # kéo dài đường v = gt để thấy rõ đồ thị tách khỏi nó
b += line(OX, OY, OX + ST * T1, OY - SV * G * T1, ORG, 1.8, "4 4", 1, track=False)
b += text(OX + ST * T1 + 6, OY - SV * G * T1 - 10, "v = gt", ORG, 14, "middle")
pts = [(OX + ST * t, OY - SV * vt(t)) for t in [i * 0.1 for i in range(0, 161)]]
b += '<polyline fill="none" stroke="' + GRN + '" stroke-width="3" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>'
for t in (2, 12):
    x = OX + ST * t
    b += line(x, YA + 2, x, OY, "currentColor", 1.2, "2 4", .5)
for t0, t1, n in ((0, 2, 1), (2, 12, 2), (12, 16, 3)):
    b += text(OX + ST * (t0 + t1) / 2, 43, f"GĐ {n}", "currentColor", 14, "middle", "600")
b += text(424, OY - 10, "t (s)", "currentColor", 14, "end")
b += text(OX + 8, 26, "v (m/s)", "currentColor", 14, "start")
fig3 = wrap(f"0 0 {VB[3][0]} {VB[3][1]}",
            "Đồ thị tốc độ theo thời gian của người nhảy dù chưa mở dù: lúc đầu tăng gần như đều, sau chậm lại, rồi đi ngang ở tốc độ giới hạn khoảng 50 m/s", b,
            "Hình 3. Tốc độ người nhảy dù chưa mở dù (giả định tốc độ giới hạn 50 m/s). Đầu tiên đồ thị bám đường <em>v</em> = <em>gt</em> (cam), sau cong dần, cuối cùng nằm ngang.")
fig3 = fig3.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-luc-can-luc-nang-04"', 1)

# ---------------- Hình 4: ảnh OpenStax College Physics 2e, Hình 11.18 (đợt 28/10/2026) ----------------
fig4 = ('<figure class="fig" data-tl="1"><img src="/assets/openstax/l10-luc-can-luc-nang/hinh-ap-luc-mat-tren-duoi.webp" '
        'alt="Khối trụ chìm trong chất lỏng: mặt dưới ở sâu h2 bị ép lên bởi lực F2 lớn hơn lực F1 ép xuống mặt trên ở độ sâu h1; hiệu hai lực là lực đẩy Archimedes" '
        'loading="lazy" width="725" height="768">'
        '<figcaption>Hình 4. Mặt dưới sâu hơn nên áp lực <em>F</em><sub>2</sub> lớn hơn <em>F</em><sub>1</sub>:<br>'
        '<em>F</em><sub>2</sub> − <em>F</em><sub>1</sub> = lực đẩy Archimedes (sách kí hiệu <em>F</em><sub>B</sub>).<br>'
        'Nhãn: fluid = chất lỏng · <em>A</em> = diện tích mặt.<br>'
        '<small>Hình: OpenStax, College Physics 2e, Hình 11.18 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small>'
        '</figcaption></figure>')

# ---------------- Hình 5: bài toán mẫu — lực kế ngoài không khí và khi nhúng ----------------
CUR["fig"] = 5
VB[5] = (440, 262)
b = defs("f5")
b += line(20, 12, 420, 12, "currentColor", 3, track=False)


def scale(x, obj_top, reading):
    g = line(x, 12, x, 22, "currentColor", 2, track=False)
    g += f'<rect x="{x-13}" y="22" width="26" height="62" rx="4" fill="rgba(148,163,184,.2)" stroke="currentColor" stroke-width="2"/>'
    for yy in range(32, 80, 8):
        g += line(x - 6, yy, x + 6, yy, "currentColor", 1, op=.6, track=False)
    g += line(x, 84, x, obj_top, "currentColor", 1.6, track=False)
    g += text(x + 22, 58, reading, RED, 15)
    return g


LX, RX = 110, 320
b += scale(LX, 150, "5,4 N")
b += f'<rect x="{LX-17}" y="150" width="34" height="40" rx="3" fill="rgba(251,146,60,.25)" stroke="currentColor" stroke-width="2"/>'
b += text(LX, 228, "ngoài không khí", "currentColor", 14, "middle", "600")
b += f'<rect x="250" y="126" width="140" height="108" fill="rgba(56,189,248,.14)"/>'
b += f'<path d="M250,112 V234 H390 V112" fill="none" stroke="currentColor" stroke-width="2"/>'
b += line(250, 126, 390, 126, BLUE, 2, track=False)
b += scale(RX, 144, "? N")
b += f'<rect x="{RX-17}" y="144" width="34" height="40" rx="3" fill="rgba(251,146,60,.25)" stroke="currentColor" stroke-width="2"/>'
b += text(384, 228, "nước", BLUE, 14, "end", "600")
b += text(RX, 254, "chìm hoàn toàn", "currentColor", 14, "middle", "600")
fig5 = wrap(f"0 0 {VB[5][0]} {VB[5][1]}",
            "Khối nhôm treo vào lực kế: ngoài không khí lực kế chỉ 5,4 N; nhúng chìm hoàn toàn trong nước thì số chỉ cần tìm", b,
            "Hình 5. Cùng một khối nhôm: treo ngoài không khí lực kế chỉ 5,4&nbsp;N; nhúng chìm hoàn toàn trong nước thì lực kế chỉ bao nhiêu?")

fig1 = fig1.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-luc-can-luc-nang-01"', 1)

# ---------------- Kiểm toạ độ ----------------
bad = []


def seg_hits_box(x1, y1, x2, y2, bx0, by0, bx1, by1):
    for i in range(41):
        t = i / 40
        x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        if bx0 + 1 < x < bx1 - 1 and by0 + 1 < y < by1 - 1:
            return True
    return False


for i, (f, x0, y0, x1, y1, s) in enumerate(LABELS):
    W, H = VB[f]
    if x0 < 2 or y0 < 2 or x1 > W - 2 or y1 > H - 2:
        bad.append(f"Hình {f}: nhãn '{s}' vượt viewBox ({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f})")
    for g, a0, b0, a1, b1, t in LABELS[i + 1:]:
        if g == f and x0 < a1 and a0 < x1 and y0 < b1 and b0 < y1:
            bad.append(f"Hình {f}: nhãn '{s}' chồng '{t}'")
    for g, sx1, sy1, sx2, sy2 in SEGS:
        if g == f and seg_hits_box(sx1, sy1, sx2, sy2, x0, y0, x1, y1):
            bad.append(f"Hình {f}: nhãn '{s}' bị đường ({sx1:.0f},{sy1:.0f})-({sx2:.0f},{sy2:.0f}) cắt")
# Hình 3: nhãn không nằm trên đường cong v–t
for f, x0, y0, x1, y1, s in LABELS:
    if f == 3 and any(x0 < x < x1 and y0 < y < y1 for x, y in pts):
        bad.append(f"Hình 3: nhãn '{s}' đè đường cong")
# Hình 3: đường cong đúng phương trình, tiệm cận tốc độ giới hạn
assert abs(vt(16) - VT) / VT < 0.01 and abs(vt(0.1) - G * 0.1) < 0.05
print("\n".join(bad) if bad else "kiểm toạ độ: ok")

src = (HERE / "theory.src.html").read_text(encoding="utf8")
figs = [fig1, fig2, fig3, fig4, fig5]
order = [int(n) for n in re.findall(r"<!--FIG(\d)-->", src)]
assert order == sorted(order) == list(range(1, len(figs) + 1)), order
for n, f in enumerate(figs, 1):
    assert f"<figcaption>Hình {n}." in f, n
    src = src.replace(f"<!--FIG{n}-->", f)

# số phút ở khung Mục tiêu lấy từ lint_do_dai (lượt 1 đo, lượt 2 ghi)
lint = HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = HERE / "theory.html"
out.write_text(margin_figs(src.replace("__PHUT__", "?")), encoding="utf8")
r = subprocess.run([sys.executable, str(lint), str(out), "--json"], capture_output=True, text=True)
m = re.search(r'"phut"\s*:\s*([\d.]+)', r.stdout) or re.search(r'"minutes"\s*:\s*([\d.]+)', r.stdout)
phut = round(float(m.group(1))) if m else None
if phut is None:
    print("KHÔNG đọc được số phút từ lint_do_dai:", r.stdout[:300])
    phut = "?"
out.write_text(margin_figs(src.replace("__PHUT__", str(phut))), encoding="utf8")
print("ok", len(src), "ký tự; phút =", phut)
