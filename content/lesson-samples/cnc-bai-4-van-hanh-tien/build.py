#!/usr/bin/env python3
"""Dựng theory.html (hình SVG + số phút) và bundle.json cho CNC Bài 4 (EMCO TURN 55). Chạy: python3 build.py"""
import json, pathlib, re
from svg_lib import RED, BLUE, ORG, GRN, wrap

HERE = pathlib.Path(__file__).resolve().parent
PHUT = 16  # điền theo lint_do_dai.py (làm tròn lên)


def T(x, y, s, c="currentColor", size=15, anchor="middle", w="700"):
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{w}" text-anchor="{anchor}">{s}</text>'


def box(x, y, w, h, c="currentColor", fill="none", sw=2.5):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'


def ln(x1, y1, x2, y2, c="currentColor", w=2.5, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d}/>'


def dot(x, y, c, r=6):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def arrow(pid, x1, y1, x2, y2, c, w=3):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" marker-end="url(#{pid})"/>'


def markers(pref, pairs):
    return ('<defs>' + ''.join(
        f'<marker id="{pref}{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" '
        f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
        for i, c in pairs) + '</defs>')


def fig1_svg():
    """Sơ đồ phần chấp hành máy tiện (nhìn ngang, đơn giản)."""
    b = markers("f1", (("x", RED), ("z", BLUE)))
    ax = 115  # tâm trục chính
    b += ln(10, ax, 410, ax, "currentColor", 1.5, "6 5")
    b += box(10, 60, 70, 110) + T(45, 50, "Trục chính", "currentColor", 15)
    b += box(80, 80, 24, 70) + T(92, 192, "Mâm cặp", "currentColor", 15) + ln(92, 152, 92, 176, "currentColor", 1.5)
    b += box(104, ax - 14, 130, 28) + T(170, ax + 34, "Phôi", "currentColor", 15)
    # ụ động + mũi tâm
    b += box(330, 92, 70, 46)
    b += f'<polygon points="330,{ax-10} 312,{ax} 330,{ax+10}" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    b += T(365, 82, "Ụ động", "currentColor", 15)
    # mâm dao + dao
    b += f'<circle cx="270" cy="45" r="26" fill="none" stroke="{ORG}" stroke-width="2.5"/>'
    b += ln(256, 67, 238, ax - 16, GRN, 4)
    b += T(304, 40, "Mâm dao", ORG, 15, "start")
    b += T(222, 78, "Dao", GRN, 15, "end")
    # băng máy
    b += box(10, 200, 400, 18) + T(210, 244, "Băng máy", "currentColor", 15)
    # trục toạ độ
    ox, oy = 290, 182
    b += arrow("f1z", ox, oy, ox + 62, oy, BLUE) + T(ox + 68, oy + 6, "+Z", BLUE, 16, "start")
    b += arrow("f1x", ox, oy, ox, oy - 34, RED) + T(ox - 8, oy - 22, "+X", RED, 16, "end")
    return wrap("0 0 420 256", "Sơ đồ phần chấp hành máy tiện CNC", b,
                "Hình 1. Phần chấp hành (sơ đồ). Z dọc trục chính, X theo đường kính.")


def fig2_svg():
    """Trình tự mở máy đến lúc chạy tay."""
    b = markers("f2", (("a", "currentColor"),))
    steps = [("1. Kiểm tra máy (chưa cấp điện)", "currentColor"),
             ("2. Đóng CP của máy tiện", "currentColor"),
             ("3. Nhấn Power máy tính", "currentColor"),
             ("4. Mở WinNC FANUC 21T", "currentColor"),
             ("5. Reference: về chuẩn", ORG),
             ("6. JOG / MDI: thao tác", BLUE)]
    y, h, gap = 8, 36, 14
    for i, (s, c) in enumerate(steps):
        b += box(60, y, 300, h, c) + T(210, y + 24, s, c, 15)
        if i < len(steps) - 1:
            b += arrow("f2a", 210, y + h, 210, y + h + gap - 1, "currentColor", 2.5)
        y += h + gap
    H = y - gap + 8
    return wrap(f"0 0 420 {H}", "Trình tự mở máy tiện CNC", b,
                "Hình 2. Trình tự mở máy: Reference luôn đứng trước JOG và MDI.")


def fig3_svg():
    """Cách 1 cài Z gốc phôi: MW = MA + AW."""
    b = ""
    ax = 120
    xM, xA, xW = 40, 110, 290
    b += ln(10, ax, 410, ax, "currentColor", 1.5, "6 5")
    b += box(xM, 70, xA - xM, 100) + T(75, 62, "Mâm cặp", "currentColor", 15)
    b += box(xA, ax - 25, xW - xA, 50) + T(200, ax + 19, "Phôi", "currentColor", 15)
    # dao chạm mặt đầu
    b += ln(xW + 3, ax - 22, 340, 40, GRN, 4) + dot(xW + 3, ax - 22, GRN, 5)
    b += T(350, 34, "Dao", GRN, 15, "start")
    # điểm M, A, W
    b += dot(xM, ax, BLUE) + T(xM - 10, ax - 8, "M", BLUE, 17, "end")
    b += dot(xA, ax - 25, "currentColor", 4) + T(xA + 8, ax - 32, "A", "currentColor", 16, "start")
    b += dot(xW, ax, RED) + T(xW + 12, ax + 22, "W", RED, 17, "start")
    # đường dóng
    b += ln(xM, 170, xM, 236, BLUE, 1.5, "4 4")
    b += ln(xA, 170, xA, 206, "currentColor", 1.5, "4 4")
    b += ln(xW, ax + 25, xW, 236, RED, 1.5, "4 4")

    def dim(x1, x2, y, lab, c="currentColor"):
        s = ln(x1, y, x2, y, c, 2)
        s += ln(x1, y - 6, x1, y + 6, c, 2) + ln(x2, y - 6, x2, y + 6, c, 2)
        return s + T((x1 + x2) / 2, y - 7, lab, c, 15)
    b += dim(xM, xA, 200, "MA")
    b += dim(xA, xW, 200, "AW")
    b += dim(xM, xW, 230, "MW = MA + AW", RED)
    return wrap("0 0 420 244", "Cài Z gốc phôi bằng cách đo trực tiếp", b,
                "Hình 4. Cách 1: MW = MA + AW. Vị trí M và dấu khi nhập theo sổ tay máy.")


def fig4_svg():
    """Sáu loại dao trên mâm dao: N (chuẩn dao) cùng một chỗ trên đài dao, P (mũi dao) mỗi dao một chỗ."""
    b = ""
    W, H = 210, 128
    tools = ["1. Tiện ngoài", "2. Cắt rãnh", "3. Ren ngoài", "4. Tiện lỗ", "5. Ren lỗ", "6. Mũi khoan"]
    pts = lambda L: " ".join(f"{x},{y}" for x, y in L)
    ins = lambda L: (f'<polygon points="{pts(L)}" fill="{GRN}" fill-opacity=".3" stroke="{GRN}" '
                     f'stroke-width="2.5" stroke-linejoin="round"/>')
    pho = lambda L: (f'<polygon points="{pts(L)}" fill="currentColor" fill-opacity=".12" stroke="currentColor" '
                     f'stroke-opacity=".55" stroke-width="1.5"/>')
    for k, name in enumerate(tools):
        g = f'<rect x="4" y="4" width="{W-8}" height="{H-8}" rx="8" fill="none" stroke="currentColor" stroke-opacity=".25" stroke-width="1.5"/>'
        g += T(14, 26, name, "currentColor", 15, "start")
        hy = 34 if k < 3 else 60          # đài dao: N = góc dưới bên trái
        N = (140, hy + 26)
        if k == 0:    # tiện ngoài: mảnh hình bình hành, mũi chĩa xuống-trái (−Z)
            g += pho([(8, 110), (108, 110), (108, 122), (8, 122)])
            g += box(146, 60, 28, 26) + ins([(146, 86), (174, 86), (152, 104), (110, 108)])
            P = (110, 108)
        elif k == 1:  # cắt rãnh: lưỡi mỏng trong rãnh, P = góc trái
            g += pho([(8, 100), (150, 100), (150, 114), (162, 114), (162, 100), (202, 100), (202, 122), (8, 122)])
            g += box(148, 60, 26, 18) + ins([(150, 78), (162, 78), (162, 114), (150, 114)])
            P = (150, 114)
        elif k == 2:  # ren ngoài: mũi chữ V 60° nằm trong rãnh ren
            zz = [(8, 122)] + [(x, 102 if (x - 153) % 14 == 0 else 114) for x in range(13, 202, 7)] + [(202, 122)]
            g += pho(zz)
            g += box(147, 60, 26, 30) + ins([(147, 90), (173, 90), (160, 114)])
            P = (160, 114)
        elif k in (3, 4):  # tiện lỗ / ren lỗ: cán dọc trục Z trong lỗ, mũi ở đầu trái chĩa lên (+X)
            g += pho([(8, 44), (108, 44), (108, 54), (8, 54)]) + pho([(8, 104), (108, 104), (108, 114), (8, 114)])
            g += T(58, 94, "lỗ", "currentColor", 15)
            g += box(36, 72, 106, 12)
            if k == 3:
                g += ins([(36, 72), (54, 72), (28, 56)])
                P = (28, 56)
            else:
                g += ins([(38, 72), (58, 72), (48, 56)])
                P = (48, 56)
        else:         # mũi khoan: dọc trục, mũi nhọn ở trái, sắp vào mặt đầu phôi
            g += pho([(8, 48), (30, 48), (30, 104), (8, 104)])
            g += box(54, 64, 88, 18)
            for x in (66, 84, 102, 120):
                g += ln(x, 64, x + 12, 82, "currentColor", 1.5)
            g += ins([(54, 64), (54, 82), (42, 73)])
            P = (42, 73)
        g += box(140, hy, 60, 26)
        g += ln(N[0], N[1], P[0], P[1], ORG, 2, "5 4")
        g += dot(N[0], N[1], BLUE, 5) + dot(P[0], P[1], RED, 5)
        b += f'<g transform="translate({(k % 2) * W},{(k // 2) * H})">{g}</g>'
    y = 3 * H + 22
    b += dot(18, y - 5, BLUE, 6) + T(32, y, "N: chuẩn dao, mọi dao cùng một chỗ", "currentColor", 15, "start")
    b += dot(18, y + 19, RED, 6) + T(32, y + 24, "P: mũi dao, mỗi dao một chỗ", "currentColor", 15, "start")
    b += ln(10, y + 43, 26, y + 43, ORG, 2.5, "5 4") + T(32, y + 48, "N → P: Geometry Offset của dao đó", ORG, 15, "start")
    return wrap(f"0 0 420 {y + 58}", "Sáu loại dao trên mâm dao, đánh dấu chuẩn dao N và mũi dao P", b,
                "Hình 3. Các dao trên mâm dao (sơ đồ). Cùng chuẩn N nhưng mũi P khác nhau, nên mỗi dao cần một hàng Geometry.")


# ---- Mô phỏng cài dao: 2 dao × 6 bước, chỉ radio + CSS (.tl-sim--buoc trong globals.css) ----
SC, AXY, CH, FACE, R0 = 3, 112, 70, 262, 45   # 3 px/mm; trục y=112; mâm cặp tới x=70; mặt đầu x=262; bán kính phôi Ø30
TOOLS = {  # số minh hoạ (không phải số máy thật); Z phôi (Work Shift) = 85,000 đã cài ở mục 8
    "v1": dict(t="T0202", ten="dao tiện ngoài", zm="132,450", zo="47,450", xm="118,300", xo="88,700"),
    "v2": dict(t="T0404", ten="dao cắt rãnh", zm="128,900", zo="43,900", xm="121,750", xo="92,150"),
}


def sim_tool(v, px, py):
    """Vẽ dao với mũi P tại (px, py), thân đi lên (+X)."""
    if v == "v1":
        pts = [(px, py), (px + 26, py - 8), (px + 34, py - 18), (px + 12, py - 18)]
        s = box(px + 12, py - 64, 22, 46)
    else:
        pts = [(px, py), (px + 8, py), (px + 8, py - 28), (px, py - 28)]
        s = box(px - 2, py - 64, 18, 36)
    s += (f'<polygon points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="{GRN}" fill-opacity=".3" '
          f'stroke="{GRN}" stroke-width="2.5" stroke-linejoin="round"/>')
    return s + dot(px, py, RED, 5)


def sim_scene(v, s):
    tl = TOOLS[v]
    g = ""
    yT = AXY - R0  # mặt trụ ngoài
    if s == 1:
        P = (372, 34)
    elif s in (2, 3):
        P = (FACE, AXY - 26)
    elif s in (4, 5):
        P = (FACE - 34, yT) if v == "v2" else (FACE + 26, yT)
    else:
        P = (FACE + 5 * SC, AXY - 10 * SC)
    g += sim_tool(v, *P)
    if s in (2, 4) or (s == 5 and v == "v2"):
        g += f'<circle cx="{P[0]}" cy="{P[1]}" r="11" fill="none" stroke="{ORG}" stroke-width="2.5"/>'
    if s == 3:
        g += ln(FACE, 26, FACE, AXY + 4, RED, 2, "5 4") + T(FACE - 6, 22, "W: Z0", RED, 15, "end")
    if v == "v1" and s in (4, 5):  # cắt thử một đoạn, rút +Z giữ X, đo đường kính
        g += ln(FACE - 40, yT, FACE + 18, yT, ORG, 2.5, "5 4")
        g += T(FACE + 4, yT - 30, "+Z, giữ X", ORG, 15, "end")
    if s in (4, 5):
        xd = FACE - 60
        g += ln(xd, yT, xd, AXY + R0, BLUE, 2) + ln(xd - 6, yT, xd + 6, yT, BLUE, 2) + ln(xd - 6, AXY + R0, xd + 6, AXY + R0, BLUE, 2)
        g += T(xd - 8, AXY + 32, "Ø29,60", BLUE, 15, "end")
    if s == 6:
        g += ln(FACE, AXY - 10 * SC - 4, FACE, AXY - 10 * SC + 4, "currentColor", 1.5) + ln(FACE, AXY - 10 * SC, FACE + 5 * SC, AXY - 10 * SC, "currentColor", 1.5)
        g += T(FACE + 4, AXY - 10 * SC + 20, "5 mm", "currentColor", 15, "start")
    # màn hình WinNC
    lines = {
        1: [f"MDI: {tl['t']} M6;", "M3 S500;"],
        2: ["POS (máy):", f"Z {tl['zm']}"],
        3: [f"Geometry hàng {tl['t'][1:3]}: Z0 → Measure", f"Z = {tl['zm']} − 85,000 = {tl['zo']}"],
        4: ["POS (máy):", f"X {tl['xm']}  · đo Ø29,60"],
        5: [f"Geometry hàng {tl['t'][1:3]}: X29.6 → Measure", f"X = {tl['xm']} − 29,600 = {tl['xo']}"],
        6: ["MDI: G0 X20 Z5;", "POS (phôi): X 20,000  Z 5,000"],
    }[s]
    g += box(10, 196, 400, 64, "currentColor", "none", 2)
    g += T(22, 222, lines[0], "currentColor", 15, "start") + T(22, 248, lines[1], BLUE if s != 6 else GRN, 15, "start")
    return f'<g class="sb-{v} sb-s{s}">{g}</g>'


def sim_dao():
    base = ln(10, AXY, 410, AXY, "currentColor", 1.5, "6 5")
    base += box(14, AXY - 70, CH - 14, 140) + T(14, AXY - 78, "Mâm cặp", "currentColor", 15, "start")
    base += box(CH, AXY - R0, FACE - CH, 2 * R0) + T(150, AXY - 14, "Phôi", "currentColor", 15)
    scenes = "".join(sim_scene(v, s) for v in TOOLS for s in range(1, 7))
    svg = (f'<svg viewBox="0 0 420 268" role="img" aria-label="Mô phỏng cài Geometry Offset cho dao tiện ngoài và dao cắt rãnh">'
           f'{base}{scenes}</svg>')
    chips_v = "".join(
        f'<input type="radio" name="cnc4-sim-v" id="cnc4-sim-{v}" class="tsb-{v}"{" checked" if v == "v1" else ""}>'
        f'<label for="cnc4-sim-{v}" class="tl-sim__chip">{tl["t"][:3]} {tl["ten"][4:]}</label>' for v, tl in TOOLS.items())
    steps = ["Gọi dao", "Chạm Z", "Đo Z", "Chạm X", "Đo X", "Thử"]
    chips_s = "".join(
        f'<input type="radio" name="cnc4-sim-s" id="cnc4-sim-s{i}" class="tsb-s{i}"{" checked" if i == 1 else ""}>'
        f'<label for="cnc4-sim-s{i}" class="tl-sim__chip">{i}. {n}</label>' for i, n in enumerate(steps, 1))
    txt = {
        (1, None): "MDI gọi dao rồi cho phôi quay. Dao ra vị trí làm việc, còn ở xa phôi.",
        (2, None): "JOG, % thấp: chạm nhẹ <strong>mặt đầu</strong> (vòng cam). Thấy phoi mỏng là dừng, không đi thêm.",
        (3, None): "Đúng hàng của dao, nhập <code>Z0</code> → <strong>Measure</strong>. Máy tự trừ Z phôi để ra độ dời của dao.",
        (4, "v1"): "Tiện thử một đoạn ngắn, rút dao theo +Z, <strong>giữ nguyên X</strong>. Dừng trục chính, đo đường kính bằng thước cặp.",
        (4, "v2"): "Chạm nhẹ đoạn <strong>Ø29,60</strong> mà dao 2 vừa tiện. Đường kính đã biết nên không cần cắt thử.",
        (5, None): "Nhập đường kính vừa đo (<code>X29.6</code>) → <strong>Measure</strong>. X đo theo đường kính.",
        (6, None): "Chạy thử <code>G0 X20 Z5;</code>: mũi P phải đứng trước mặt đầu đúng 5 mm. Lệch là dừng, kiểm lại hàng vừa đo.",
    }
    ps = ""
    for (s, v), t in txt.items():
        cls = f"sb-s{s}" + (f" sb-{v}" if v else "")
        ps += f'<p class="sb-txt {cls}"><strong>Bước {s}.</strong> {t}</p>'
    return (f'<div class="tl-sim tl-sim--buoc">'
            f'<p class="tl-label">🎛️ Mô phỏng: cài Geometry Offset từng bước</p>'
            f'<div class="tl-sim__row"><b>Chọn dao</b>{chips_v}</div>'
            f'<div class="tl-sim__row"><b>Chọn bước</b>{chips_s}</div>'
            f'{svg}{ps}'
            f'<p class="sb-txt">Số trên màn hình là số minh hoạ, không phải số của máy trong xưởng.</p></div>')


src = (HERE / "theory.src.html").read_text(encoding="utf8")
html = (src.replace("__FIG1__", fig1_svg()).replace("__FIG2__", fig2_svg())
          .replace("__FIG3__", fig3_svg())
          .replace("__FIG4__", fig4_svg()).replace("__SIM_DAO__", sim_dao()).replace("__PHUT__", str(PHUT)))
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
    qs[0]["question"] = "Sau khi mở WinNC FANUC 21T, việc nào phải làm trước khi di chuyển dao bằng tay?"
bundle = {
    "schema": "thachlab.lesson-bundle/v1",
    "theory_html": html,
    "worked_examples": [],
    "exam": {"title": "Kiểm tra nhanh — Vận hành và cài đặt máy tiện CNC EMCO TURN 55", "duration_minutes": 8, "questions": qs},
}
(HERE / "bundle.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=1), encoding="utf8")
print("ok", len(html), "bytes;", len(qs), "cau")
