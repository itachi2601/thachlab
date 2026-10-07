#!/usr/bin/env python3
"""Dựng theory.html (hình SVG + số phút) và bundle.json cho CNC Bài 6 (Gia công tiện CNC). Chạy: python3 build.py"""
import json, pathlib, re, math, sys
from svg_lib import RED, BLUE, ORG, GRN, wrap

HERE = pathlib.Path(__file__).resolve().parent
PHUT = 15  # điền theo lint_do_dai.py (làm tròn lên)

# ---------- kiểm hộp nhãn (không đè nhau, không vượt viewBox) ----------
LABELS = []


def T(x, y, s, c="currentColor", size=15, anchor="middle", w="700", fig=None):
    plain = re.sub(r"<[^>]+>", "", s)
    wd = 0.58 * size * len(plain)
    x0 = x - wd / 2 if anchor == "middle" else (x if anchor == "start" else x - wd)
    LABELS.append((fig, plain, x0, y - size * 0.85, x0 + wd, y + size * 0.25))
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{anchor}">{s}</text>'


def check_labels(fig, vb_w, vb_h):
    L = [l for l in LABELS if l[0] == fig]
    bad = 0
    for i, a in enumerate(L):
        if a[2] < 0 or a[4] > vb_w or a[3] < 0 or a[5] > vb_h:
            print(f"[{fig}] VUOT viewBox: {a[1]} {a[2]:.0f}-{a[4]:.0f} / {a[3]:.0f}-{a[5]:.0f}"); bad += 1
        for b in L[i + 1:]:
            if a[2] < b[4] and b[2] < a[4] and a[3] < b[5] and b[3] < a[5]:
                print(f"[{fig}] DE NHAU: {a[1]} / {b[1]}"); bad += 1
    return bad


def ln(x1, y1, x2, y2, c="currentColor", w=2.5, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'


def dot(x, y, c, r=5):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'


def marker(pid, c):
    return (f'<marker id="{pid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
            f'markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')


# ---------- hình học trục mẫu (Z,R) tính từ mặt đầu; 1 mm = S px ----------
S = 5.0
ZX0 = 388          # x của mặt đầu (Z0)
AX = 200           # y của trục quay


def px(z, r):
    return ZX0 + z * S, AX - r * S


# Điểm P1..P7 (X là đường kính)
PTS = [(10, 0), (12, -2), (12, -20), (15, -50), (15, -63), (17, -65), (20, -65)]  # (R, Z)


def profile_path():
    P = [px(z, r) for r, z in PTS]
    d = f"M {px(0, 0)[0]:.1f},{AX} L {P[0][0]:.1f},{P[0][1]:.1f} "
    d += f"L {P[1][0]:.1f},{P[1][1]:.1f} L {P[2][0]:.1f},{P[2][1]:.1f} L {P[3][0]:.1f},{P[3][1]:.1f} L {P[4][0]:.1f},{P[4][1]:.1f} "
    # bo cung lõm R2 giữa P5 và P6: điều khiển ở góc (Z-65, R15)
    cx, cy = px(-65, 15)
    d += f"Q {cx:.1f},{cy:.1f} {P[5][0]:.1f},{P[5][1]:.1f} L {P[6][0]:.1f},{P[6][1]:.1f} "
    d += f"L {px(-65, 0)[0]:.1f},{AX} Z"
    return d


def shaft_body(tag, with_stock=True):
    b = ""
    xl = px(-65, 0)[0]
    if with_stock:
        xs, ys = xl, AX - 20 * S
        b += (f'<rect x="{xs:.1f}" y="{ys:.1f}" width="{ZX0 + 2 * S - xs:.1f}" height="{20 * S:.1f}" '
              f'fill="rgba(251,146,60,0.22)" stroke="{ORG}" stroke-width="2" stroke-dasharray="6 5"/>')
    b += f'<path d="{profile_path()}" fill="rgba(52,211,153,0.28)" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/>'
    # mâm cặp
    b += f'<rect x="10" y="{AX - 22 * S:.1f}" width="{xl - 10:.1f}" height="{22 * S:.1f}" rx="4" fill="rgba(128,128,128,0.25)" stroke="currentColor" stroke-width="2.5"/>'
    b += ln(6, AX, 414, AX, "currentColor", 1.5, "10 4 2 4")
    return b


def fig1_svg():
    f = "f1"
    b = shaft_body(f)
    xl = px(-65, 0)[0]
    b += T(10, AX - 22 * S - 10, "Mâm cặp", "currentColor", 15, "start", fig=f)
    # lượng dư (giữa nét đứt và nét liền, phía trên bậc nhỏ)
    b += T(225, 116, "Lượng dư", ORG, 15, "middle", fig=f)
    # mặt đầu
    b += ln(392, 76, ZX0 + 1, AX - 40, "currentColor", 1.5)
    b += T(402, 70, "Mặt đầu", "currentColor", 15, "end", fig=f)
    # nhãn trong thân
    b += T(335, AX - 18, "Bậc", GRN, 15, fig=f)
    b += T(212, AX - 18, "Côn", GRN, 15, fig=f)
    # vai + bo cung (dưới trục)
    ax, ay = px(-64, 16)
    b += ln(110, 232, ax, ay + 2, "currentColor", 1.5)
    b += T(112, 250, "Vai, bo cung", "currentColor", 15, "start", fig=f)
    n = check_labels(f, 420, 262)
    return wrap("0 0 420 262", "Chi tiết trục bậc nằm trong phôi gá trên mâm cặp", b,
                "Hình 1. Chi tiết (nét liền) nằm trong phôi (nét đứt) gá trong mâm cặp; phần giữa hai nét là lượng dư phải tiện bỏ."), n


def fig2_svg():
    f = "f2"
    ay = 140
    R1, R2 = 66, 24           # nửa đường kính đầu to / đầu nhỏ (minh hoạ)
    xa, xb = 110, 320
    b = f'<defs>{marker("f2b", BLUE)}{marker("f2r", RED)}{marker("f2o", ORG)}</defs>'
    b += f'<path d="M {xa},{ay - R1} L {xb},{ay - R2} L {xb},{ay + R2} L {xa},{ay + R1} Z" fill="rgba(52,211,153,0.28)" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/>'
    b += ln(96, ay, 346, ay, "currentColor", 1.5, "10 4 2 4")
    # D (đầu to) và d (đầu nhỏ)
    b += f'<line x1="70" y1="{ay - R1}" x2="70" y2="{ay + R1}" stroke="{BLUE}" stroke-width="2.5" marker-end="url(#f2b)" marker-start="url(#f2b)"/>'
    b += ln(70, ay - R1, xa, ay - R1, BLUE, 1.2, "4 4") + ln(70, ay + R1, xa, ay + R1, BLUE, 1.2, "4 4")
    b += T(48, ay + 6, "D", BLUE, 18, fig=f)
    b += f'<line x1="365" y1="{ay - R2}" x2="365" y2="{ay + R2}" stroke="{RED}" stroke-width="2.5" marker-end="url(#f2r)" marker-start="url(#f2r)"/>'
    b += ln(xb, ay - R2, 365, ay - R2, RED, 1.2, "4 4") + ln(xb, ay + R2, 365, ay + R2, RED, 1.2, "4 4")
    b += T(388, ay + 6, "d", RED, 18, fig=f)
    # L
    yl = ay + R1 + 28
    b += f'<line x1="{xa}" y1="{yl}" x2="{xb}" y2="{yl}" stroke="{ORG}" stroke-width="2.5" marker-end="url(#f2o)" marker-start="url(#f2o)"/>'
    b += ln(xa, ay + R1, xa, yl + 6, ORG, 1.2, "4 4") + ln(xb, ay + R2, xb, yl + 6, ORG, 1.2, "4 4")
    b += T((xa + xb) / 2, yl - 8, "L", ORG, 18, fig=f)
    # nửa góc côn alpha: đường song song trục qua đầu nhỏ, kéo dài về đầu to
    b += ln(xa, ay - R2, xb, ay - R2, "currentColor", 1.2, "6 4")
    ang = math.atan2(R1 - R2, xb - xa)
    # cung góc tại đầu nhỏ
    r = 74
    x1, y1 = xb - r * math.cos(ang), ay - R2 - r * math.sin(ang)
    x2, y2 = xb - r, ay - R2
    b += f'<path d="M {x1:.1f},{y1:.1f} A {r},{r} 0 0 1 {x2:.1f},{y2:.1f}" fill="none" stroke="{GRN}" stroke-width="3"/>'
    mx, my = xb - r * math.cos(ang / 2), ay - R2 - r * math.sin(ang / 2)
    b += ln(mx - 2, my + 2, mx - 16, ay - R2 + 6, GRN, 1.5)
    b += T(mx - 22, ay - 8, "α", GRN, 18, "middle", fig=f)
    b += T(200, 22, "Máy tiện: X là đường kính", "currentColor", 15, fig=f)
    n = check_labels(f, 420, 256)
    return wrap("0 0 420 256", "Côn: đầu to D, đầu nhỏ d, chiều dài L, nửa góc côn alpha", b,
                "Hình 2. Côn: đầu to đường kính D, đầu nhỏ d, dài L; α là nửa góc côn."), n


def fig3_svg():
    f = "f3"
    b = shaft_body(f, with_stock=True)
    xl = px(-65, 0)[0]
    P = [px(z, r) for r, z in PTS]
    for (x, y) in P:
        b += dot(x, y, RED)
    # nhãn
    b += T(10, AX - 22 * S - 10, "Mâm cặp", "currentColor", 15, "start", fig=f)
    b += T(P[0][0] - 8, P[0][1] + 26, "P<tspan baseline-shift=\"sub\" font-size=\"14\">1</tspan>", RED, 16, "end", fig=f)
    b += T(P[1][0], P[1][1] - 12, "P<tspan baseline-shift=\"sub\" font-size=\"14\">2</tspan>", RED, 16, fig=f)
    b += T(P[2][0], P[2][1] - 12, "P<tspan baseline-shift=\"sub\" font-size=\"14\">3</tspan>", RED, 16, fig=f)
    b += T(P[3][0], P[3][1] - 12, "P<tspan baseline-shift=\"sub\" font-size=\"14\">4</tspan>", RED, 16, fig=f)
    # P5, P6, P7 gần nhau: nhãn có dây dẫn
    b += ln(P[4][0] + 2, P[4][1] + 3, P[4][0] + 22, P[4][1] + 26, RED, 1.2)
    b += T(P[4][0] + 24, P[4][1] + 42, "P<tspan baseline-shift=\"sub\" font-size=\"14\">5</tspan>", RED, 16, "start", fig=f)
    b += ln(P[5][0] + 2, P[5][1] - 2, P[5][0] + 34, P[5][1] - 18, RED, 1.2)
    b += T(P[5][0] + 36, P[5][1] - 14, "P<tspan baseline-shift=\"sub\" font-size=\"14\">6</tspan>", RED, 16, "start", fig=f)
    b += ln(P[6][0] + 2, P[6][1] - 2, P[6][0] + 34, P[6][1] - 34, RED, 1.2)
    b += T(P[6][0] + 36, P[6][1] - 32, "P<tspan baseline-shift=\"sub\" font-size=\"14\">7</tspan>", RED, 16, "start", fig=f)
    n = check_labels(f, 420, 232)
    return wrap("0 0 420 232", "Trục bậc có vát, côn, bậc và bo cung với các điểm P1 đến P7", b,
                "Hình 3. Nửa trên của trục (gốc W ở tâm mặt đầu bên phải, +Z hướng sang phải, ra xa mâm cặp). Nét đứt: phôi đường kính 40."), n


figs = {}
total_bad = 0
for k, fn in (("__FIG1__", fig1_svg), ("__FIG2__", fig2_svg), ("__FIG3__", fig3_svg)):
    svg, bad = fn()
    figs[k] = svg
    total_bad += bad
if total_bad:
    print("CO", total_bad, "LOI NHAN");

src = (HERE / "theory.src.html").read_text(encoding="utf8")
html = src
for k, v in figs.items():
    html = html.replace(k, v)
html = html.replace("__PHUT__", str(PHUT))
(HERE / "theory.html").write_text(html, encoding="utf8")

MC = "multiple_choice"
txt = lambda s: re.sub(r"<[^>]+>", "", s)
qs = []
for blk in re.findall(r'<div class="tl-quiz">(.*?)<div class="tl-fb tl-fb--no">', html, re.S):
    qm = re.search(r'<p>(.*?)</p>', blk, re.S)
    opts = re.findall(r'<label[^>]*class="tl-opt (tl-ok|tl-no)">[A-D]\. (.*?)</label>', blk, re.S)
    fb = re.search(r'<div class="tl-fb tl-fb--ok"><p>(.*?)</p></div>', blk, re.S)
    if len(opts) != 4:
        continue
    q = qm.group(1) if qm else "Chọn đáp án đúng."
    qs.append({"type": MC, "question": txt(q), "options": [txt(o[1]) for o in opts],
               "answer": [o[0] for o in opts].index("tl-ok"), "explanation": txt(fb.group(1)) if fb else ""})
if qs:  # câu dự đoán nằm ngoài tl-quiz: <p> đứng trước khối quiz
    qs[0]["question"] = "Vì sao quy trình chuẩn luôn tiện mặt đầu trước mọi bậc khác?"
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": html,
    "worked_examples": [],
    "exam": {"title": "Kiểm tra nhanh — Gia công tiện CNC", "duration_minutes": 10, "questions": qs},
}
(HERE / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("ok", len(html), "bytes;", len(qs), "cau")
