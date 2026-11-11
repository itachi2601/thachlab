#!/usr/bin/env python3
"""Dựng theory.html (hình SVG + số phút) và bundle.json cho CNC Bài 2. Chạy: python3 build.py"""
import json, pathlib, re
from svg_lib import RED, BLUE, ORG, GRN, wrap

HERE = pathlib.Path(__file__).resolve().parent
PHUT = 20  # điền theo lint_do_dai.py


def T(x, y, s, c="currentColor", size=15, anchor="middle", w="700", mono=False):
    f = ' font-family="ui-monospace,Menlo,Consolas,monospace"' if mono else ""
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{anchor}"{f}>{s}</text>'


def ln(x1, y1, x2, y2, c="currentColor", w=2.5, dash="", mk=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#{mk})"' if mk else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d}{m}/>'


def marker(i, c):
    return (f'<marker id="{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
            f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')


def fig1_svg():
    # 5 px/mm; trục y=125; mặt đầu phải x=380
    S, ax, x0 = 5, 125, 380
    zx = lambda z: x0 + z * S
    b = ln(20, ax, 410, ax, "currentColor", 1.5, "8 5")
    # mâm cặp
    b += f'<rect x="78" y="12" width="42" height="46" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    b += f'<rect x="78" y="192" width="42" height="46" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    b += T(99, 82, "Mâm", "currentColor", 14) + T(99, 99, "cặp", "currentColor", 14)
    # phần phôi kẹp Ø40 (x 120..205)
    b += f'<rect x="120" y="{ax-100}" width="{zx(-35)-120}" height="200" fill="none" stroke="currentColor" stroke-width="2"/>'
    # biên dạng trục bậc (đối xứng)
    r20, r30, ch = 10 * S, 15 * S, 1 * S
    top = [(zx(-35), ax - r30), (zx(-15), ax - r30), (zx(-15), ax - r20), (x0 - ch, ax - r20), (x0, ax - r20 + ch)]
    pts = top + [(x0, ax + r20 - ch), (x0 - ch, ax + r20), (zx(-15), ax + r20), (zx(-15), ax + r30), (zx(-35), ax + r30)]
    b += '<polyline points="' + " ".join(f"{x},{y}" for x, y in pts) + f'" fill="none" stroke="{BLUE}" stroke-width="3"/>'
    b += T(342, 113, "Ø20", BLUE, 16) + T(255, 113, "Ø30", BLUE, 16)
    b += T(415, 58, "vát 1×45°", "currentColor", 14, "end", "600") + ln(386, 62, 380, 76, "currentColor", 1.5)
    b += f'<circle cx="{x0}" cy="{ax}" r="6" fill="{RED}"/>' + T(396, 146, "W", RED, 17)
    # kích thước
    for x in (zx(-15), zx(-35), x0):
        b += ln(x, ax + r30 + 6 if x != x0 else ax + r20 + 6, x, 272, "currentColor", 1.2, "3 3")
    b += ln(zx(-15), 246, x0, 246, "currentColor", 1.5) + T((zx(-15) + x0) / 2, 240, "15", "currentColor", 15)
    b += ln(zx(-35), 270, x0, 270, "currentColor", 1.5) + T(250, 264, "35", "currentColor", 15)
    return wrap("0 0 420 282", "Bản vẽ trục bậc Ø20 và Ø30", b,
                "Hình 1. Trục bậc cần tiện: đoạn Ø20 dài 15 mm, đoạn Ø30 tới 35 mm tính từ mặt đầu, vát 1×45°. W ở tâm mặt đầu phải.")


def fig2_svg():
    rows = [("N50", "số thứ tự khối"), ("G01", "kiểu chuyển động: cắt thẳng"), ("X50.0", "đích theo phương đường kính"),
            ("Z-25.0", "đích dọc trục chính"), ("F0.2", "lượng chạy dao"), (";", "kết thúc khối")]
    cols = [ORG, BLUE, RED, RED, GRN, "currentColor"]
    b = T(210, 26, "N50 G01 X50.0 Z-25.0 F0.2 ;", "currentColor", 17, "middle", "700", True)
    for i, ((tok, mean), c) in enumerate(zip(rows, cols)):
        y = 46 + i * 38
        b += f'<rect x="16" y="{y}" width="104" height="30" rx="6" fill="none" stroke="{c}" stroke-width="2.5"/>'
        b += T(68, y + 21, tok, c, 16, "middle", "700", True)
        b += T(134, y + 21, mean, "currentColor", 15, "start", "600")
    return wrap("0 0 420 280", "Cấu trúc một khối lệnh", b,
                "Hình 2. Một khối lệnh FANUC 21T: mỗi chữ cái kèm con số là một từ lệnh, khối kết thúc bằng dấu chấm phẩy.")


def fig3_svg():
    S, ax, x0 = 8, 230, 370
    P = lambda X, Z: (x0 + Z * S, ax - X / 2 * S)
    b0 = ""
    S0 = P(30, 2)
    pts = {"S": P(18, 2), "A": P(18, 0), "B": P(20, -1), "C": P(20, -15), "D": P(30, -15), "E": P(30, -35), "F": P(42, -35)}
    b = "<defs>" + marker("g3", GRN) + marker("o3", ORG) + marker("k3", "currentColor") + "</defs>"
    b += ln(30, ax, 412, ax, "currentColor", 1.5, "8 5")
    # phôi Ø40 (nửa trên)
    y40 = ax - 20 * S
    b += ln(40, y40, x0, y40, "currentColor", 1.5, "5 4") + ln(x0, y40, x0, ax, "currentColor", 1.5, "5 4")
    b += T(150, y40 - 8, "phôi Ø40", "currentColor", 14, "middle", "600")
    k = list(pts)
    for a, c in zip(k, k[1:]):
        (x1, y1), (x2, y2) = pts[a], pts[c]
        b += ln(x1, y1, x2, y2, GRN, 3, mk="" if a in "SA" else "g3")
    b += ln(S0[0], S0[1], pts["S"][0], pts["S"][1], ORG, 2.5, "6 4", "o3") + f'<circle cx="{S0[0]}" cy="{S0[1]}" r="4.5" fill="{ORG}"/>'
    for n, (x, y) in pts.items():
        b += f'<circle cx="{x}" cy="{y}" r="4.5" fill="{ORG}"/>'
    lab = {"S": (S0[0] + 14, S0[1] - 4, "start"), "A": (370, 184, "middle"), "B": (356, 138, "middle"), "C": (250, 174, "middle"),
           "D": (240, 102, "end"), "E": (80, 128, "end"), "F": (80, 66, "end")}
    for n, (x, y, an) in lab.items():
        b += T(x, y, n, ORG, 16, an)
    b += f'<circle cx="{x0}" cy="{ax}" r="6" fill="{RED}"/>' + T(384, 254, "W", RED, 17)
    b += ln(40, ax, 40, ax - 60, "currentColor", 2.5, mk="k3") + T(50, ax - 46, "+X", "currentColor", 15, "start")
    b += T(150, 258, "Z âm: về phía mâm cặp", "currentColor", 14, "middle", "600")
    return wrap("0 0 420 270", "Đường tiện tinh trục bậc", b,
                "Hình 3. Đường dao tiện tinh (nửa trên trục): từ S chạy nhanh G00 (nét đứt) tới X18.0 Z2.0, rồi cắt: A–B vát, B–C đoạn Ø20, C–D lên bậc, D–E đoạn Ø30, E–F rút dao. Vẽ theo bán kính, chương trình ghi X theo đường kính.")


# ---- Hình 4–6: chu trình thô G73 / tinh G72 (nửa trên trục, chỉ vẽ phần bán kính 6..22 mm) ----
CS, CR, CX0, CY0, RB = 9, 13, 374, 30, 6.5   # Z: 9 px/mm, bán kính: 13 px/mm (phóng theo bán kính); ngắt ở r=7,5
cx = lambda z: CX0 + z * CS
cy = lambda r: CY0 + (22 - r) * CR
PROFILE = [(0, RB), (0, 9), (-1, 10), (-15, 10), (-15, 15), (-35, 15), (-35, 20)]  # (Z, bán kính) chi tiết Hình 1
GRAY = "#94a3b8"


def poly(pts, c, w, dash="", extra=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    s = " ".join(f"{cx(z):.1f},{cy(r):.1f}" for z, r in pts)
    return f'<polyline points="{s}" fill="none" stroke="{c}" stroke-width="{w}"{d}{extra}/>'


def dot(z, r, c, rad=4.5):
    return f'<circle cx="{cx(z):.1f}" cy="{cy(r):.1f}" r="{rad}" fill="{c}"/>'


def cycle_base(phoi=True):
    """Phôi Ø40 (nét đứt xám), đường cắt ngang ở bán kính 6 (không vẽ tới tâm), biên dạng chi tiết (xanh)."""
    b = ""
    if phoi:
        b += poly([(-37, 20), (0, 20), (0, RB)], GRAY, 2, "6 4")
        b += T(cx(-27), cy(20) - 8, "phôi Ø40", GRAY, 15, "middle", "600")
    # đường ngắt (răng cưa) ở bán kính 6
    zz = " ".join(f"{cx(-37) + i * 12:.0f},{cy(RB) + (4 if i % 2 else -4):.0f}" for i in range(0, 32))
    b += f'<polyline points="{zz}" fill="none" stroke="{GRAY}" stroke-width="1.2"/>'
    b += poly(PROFILE, BLUE, 3.5)
    b += T(cx(-8), cy(10) + 22, "Ø20", BLUE, 16) + T(cx(-25), cy(15) + 22, "Ø30", BLUE, 16)
    return b


def fig4_svg():
    """Trước: tự viết G00/G01 cho từng lát — 4 lát, mỗi lát 4 điểm phải tính."""
    b = "<defs>" + marker("g4", GRN) + marker("o4", ORG) + marker("k4", GRAY) + "</defs>" + cycle_base()
    lats = [(17.5, -34.9), (15.25, -34.9), (12.75, -14.9), (10.25, -14.9)]
    prev_r = 21  # S: X42 Z2
    b += dot(2, 21, ORG) + T(cx(2) + 9, cy(21) + 5, "S", ORG, 16, "start")
    for i, (r, zend) in enumerate(lats, 1):
        ret = r + 1
        b += ln(cx(2), cy(prev_r), cx(2), cy(r) - 4, ORG, 2.5, "5 3", "o4")            # ăn vào G00
        b += ln(cx(2), cy(r), cx(zend) + 4, cy(r), GRN, 3, mk="g4")                       # cắt G01
        b += ln(cx(zend), cy(r), cx(zend), cy(ret) + 3, GRAY, 2, "4 3", "k4")             # lùi
        b += ln(cx(zend), cy(ret), cx(2) - 4, cy(ret), GRAY, 2, "4 3", "k4")              # về
        b += dot(2, r, ORG, 4) + dot(zend, r, GRN, 4) + dot(zend, ret, GRAY, 3.5) + dot(2, ret, GRAY, 3.5)
        b += (f'<circle cx="{cx(2) + 14:.1f}" cy="{cy(r):.1f}" r="9" fill="none" stroke="{ORG}" stroke-width="2"/>'
              + T(cx(2) + 14, cy(r) + 5, str(i), ORG, 13))
        prev_r = ret
    lx = cx(-36)
    b += ln(lx, 261, lx + 22, 261, ORG, 2.5, "5 3") + T(lx + 28, 266, "ăn vào", "currentColor", 15, "start", "600")
    b += ln(lx + 92, 261, lx + 114, 261, GRN, 3) + T(lx + 120, 266, "cắt G01", "currentColor", 15, "start", "600")
    b += ln(lx + 190, 261, lx + 212, 261, GRAY, 2, "4 3") + T(lx + 218, 266, "lùi, về G00", "currentColor", 15, "start", "600")
    b += T(cx(-36), 292, "4 lát × 4 khối = 16 khối, 16 điểm tự tính", RED, 16, "start", "700")
    return wrap("0 0 420 304", "Tiện thô viết tay bằng G00 G01: bốn lát cắt",
                b, "Hình 4. Chưa dùng chu trình: em phải tự chọn từng lát và tính 4 điểm (chấm tròn) cho mỗi lát "
                   "(ăn vào → cắt → lùi → về), toạ độ ở bảng dưới. Hình phóng to theo bán kính. Hình lấy sâu khoảng 2,5 mm mỗi lát cho dễ nhìn; "
                   "với 1 mm như Bài tập 1 là 10 lát, 40 khối.")


def fig5_svg():
    """Sau: G73 — chỉ khai S và biên dạng A…F; máy tự sinh các lát (nét mờ)."""
    b = "<defs>" + marker("o5", ORG) + "</defs>" + cycle_base()
    # các lát máy tự tính (U1), nét mờ
    for r in (19, 18, 17, 16, 15.25):
        b += ln(cx(2), cy(r), cx(-34.9), cy(r), GRAY, 1.6, "", "")
    for r in (14.25, 13.25, 12.25, 11.25, 10.25):
        b += ln(cx(2), cy(r), cx(-14.9), cy(r), GRAY, 1.6, "", "")
    # biên dạng P–Q (cam) và các điểm em phải khai
    pq = [(2, 9), (0, 9), (-1, 10), (-15, 10), (-15, 15), (-35, 15), (-35, 21)]
    b += poly(pq, ORG, 3, "", ' stroke-linejoin="round"')
    b += ln(cx(2), cy(21), cx(2), cy(9) - 4, ORG, 2.5, "5 3", "o5")
    for z, r in [(2, 21)] + pq:
        b += dot(z, r, ORG)
    lab = [("S", cx(2) + 9, cy(21) + 5, "start"), ("A", cx(0) - 12, cy(9) + 12, "end"),
           ("B", cx(-1) - 6, cy(10) - 8, "end"), ("C", cx(-15) + 8, cy(10) + 18, "start"),
           ("D", cx(-15) + 8, cy(15) - 8, "start"), ("E", cx(-35) + 8, cy(15) + 18, "start"),
           ("F", cx(-35) - 8, cy(21) + 5, "end")]
    for n, x, y, an in lab:
        b += T(x, y, n, ORG, 16, an)
    b += T(cx(-36), 266, "Em khai: S + A…F · nét mờ: máy tự tính", "currentColor", 15, "start", "600")
    b += T(cx(-36), 292, "2 khối G73 + 7 khối biên dạng", GRN, 16, "start", "700")
    return wrap("0 0 420 304", "Chu trình G73: chỉ khai điểm bắt đầu và biên dạng",
                b, "Hình 5. Dùng G73: em chỉ cho máy điểm bắt đầu S (X42 Z2) và biên dạng A→F (khối P–Q). "
                   "Máy tự chia các lát mỗi lát sâu U1 (nét mờ, hình minh hoạ), cuối cùng chạy một lượt dọc biên dạng, chừa lớp dư.")


def fig6_svg():
    """G72: dao tinh chạy đúng biên dạng một lượt, bóc lớp dư (vẽ phóng to)."""
    b = "<defs>" + marker("g6", GRN) + "</defs>" + cycle_base(phoi=False)
    # lớp dư sau thô (phóng to ~1 mm cho thấy được)
    dz, dr = 0.7, 0.7
    off = [(0 + dz, RB), (0 + dz, 9 + dr), (-1 + dz, 10 + dr), (-15 + dz, 10 + dr), (-15 + dz, 15 + dr),
           (-35 + dz, 15 + dr), (-35 + dz, 20)]
    band = off + PROFILE[::-1]
    s = " ".join(f"{cx(z):.1f},{cy(r):.1f}" for z, r in band)
    b += f'<polygon points="{s}" fill="{GRAY}" fill-opacity="0.35" stroke="none"/>'
    b += poly(off, GRAY, 1.5, "4 3")
    b += T(cx(-25), cy(15) - 12, "lớp dư", GRAY, 15, "middle", "700")
    # đường dao tinh
    path = [(2, 21), (2, 9), (0, 9), (-1, 10), (-15, 10), (-15, 15), (-35, 15), (-35, 21)]
    for (z1, r1), (z2, r2) in zip(path, path[1:]):
        x1, y1, x2, y2 = cx(z1), cy(r1), cx(z2), cy(r2)
        dash = "5 3" if (z1, r1) == (2, 21) else ""
        b += ln(x1, y1, x2, y2, GRN, 3, dash, "g6" if abs(x2 - x1) + abs(y2 - y1) > 14 else "")
    b += dot(2, 21, ORG) + T(cx(2) + 9, cy(21) + 5, "S", ORG, 16, "start")
    b += T(cx(-36), 266, "Dao tinh T0404 · F0.1 · 1000 v/ph", "currentColor", 15, "start", "600")
    b += T(cx(-36), 292, "1 khối: G72 P80 Q140", GRN, 16, "start", "700")
    return wrap("0 0 420 304", "Chu trình G72: một lượt tinh theo biên dạng",
                b, "Hình 6. Dùng G72: dao tinh về lại S rồi chạy đúng biên dạng A→F một lượt, "
                   "bóc lớp dư mỏng và đều (lớp xám vẽ phóng to; thật chỉ 0,25 mm mỗi bên).")


src = (HERE / "theory.src.html").read_text(encoding="utf8")
html = (src.replace("__FIG1__", fig1_svg()).replace("__FIG2__", fig2_svg())
          .replace("__FIG3__", fig3_svg())
          .replace("__FIG4__", fig4_svg()).replace("__FIG5__", fig5_svg()).replace("__FIG6__", fig6_svg()).replace("__PHUT__", str(PHUT)))
(HERE / "theory.html").write_text(html, encoding="utf8")

MC = "multiple_choice"
qs = []
for blk in re.findall(r'<div class="tl-quiz">(.*?)<div class="tl-fb tl-fb--no">', html, re.S):
    qm = re.search(r'<p>(.*?)</p>', blk, re.S)
    opts = re.findall(r'<label[^>]*class="tl-opt (tl-ok|tl-no)">[A-D]\. (.*?)</label>', blk, re.S)
    fb = re.search(r'<div class="tl-fb tl-fb--ok"><p>(.*?)</p></div>', blk, re.S)
    if len(opts) != 4:
        continue
    q = qm.group(1) if qm else "Chọn đáp án đúng."
    txt = lambda s: re.sub(r"<[^>]+>", "", s)
    qs.append({"type": MC, "question": txt(q), "options": [txt(o[1]) for o in opts],
               "answer": [o[0] for o in opts].index("tl-ok"), "explanation": txt(fb.group(1)) if fb else ""})
if qs:  # câu dự đoán: đề nằm ngoài tl-quiz
    qs[0]["question"] = ("Bản vẽ ghi đoạn trục Ø20, chương trình ghi G01 X10.0 Z-15.0. "
                         "Vì sao chi tiết mô phỏng ra Ø10 thay vì Ø20?")
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": html,
    "worked_examples": [],
    "exam": {"title": "Kiểm tra nhanh — Lập trình tiện CNC với Win-NC32 / FANUC 21T", "duration_minutes": 10, "questions": qs},
}
(HERE / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("ok", len(html), "bytes;", len(qs), "cau")
