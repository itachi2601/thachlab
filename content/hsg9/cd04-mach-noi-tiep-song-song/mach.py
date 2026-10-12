"""Vẽ sơ đồ mạch điện SVG (dùng chung cho build_figs.py và scripts/data/bai-tap-mau/build-hinh-157.py).
Quy ước: mỗi NHÁNH là một đoạn thẳng đứng/ngang nối hai nút, các phần tử đặt đều trên nhánh;
dây tự cắt ở hai đầu phần tử. Phần tử vẽ trong toạ độ cục bộ nằm ngang rồi xoay 90° nếu nhánh đứng,
nhãn đặt ngoài nhóm xoay nên luôn nằm ngang. Mô phỏng: chấm điện tích chạy một lần dọc mỗi nhánh,
tốc độ tỉ lệ cường độ dòng điện của nhánh (px/s = vA * I)."""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "soan-bai-ly-thuyet-tuong-tac", "scripts"))
from svg_lib import RED, BLUE, ORG, GRN, text  # noqa: E402

HL = {"R": 19, "Rb": 19, "A": 11, "V": 11, "E": 10, "K": 16, "RA": 14, "RV": 19}   # nửa chiều dài phần tử trên nhánh
GREY = "#94a3b8"


def rich(s, size=13):
    """`R_1` hoặc `R_{23}` -> chỉ số dưới (hạ dòng rồi trả lại)."""
    out, sub = "", False
    for p in re.split(r"(_\{[^}]+\}|_[A-Za-z0-9])", s):
        if p.startswith("_"):
            out += f'<tspan dy="4" font-size="{size - 3}">{p[2:-1] if p.startswith("_{") else p[1:]}</tspan>'
            sub = True
        elif p:
            out += f'<tspan dy="-4">{p}</tspan>' if sub else p
            sub = False
    return out


def lab(x, y, s, c="currentColor", size=15, anchor="middle", weight="700"):
    return text(round(x, 1), round(y, 1), rich(s, size), c, size, anchor, weight)


def line(x1, y1, x2, y2, c="currentColor", w=2.2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"'
            f'{d} opacity="{op}" stroke-linecap="round"/>')


def node(x, y, name="", dx=-9, dy=-8):
    b = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.8" fill="currentColor"/>'
    return b + (lab(x + dx, y + dy, name, "currentColor", 13) if name else "")


def _sym(kind, state, c, op):
    """Ký hiệu cục bộ, nằm ngang, tâm ở (0,0)."""
    a = f'stroke="{c}" stroke-width="2.2" fill="none" opacity="{op}" stroke-linecap="round" stroke-linejoin="round"'
    if kind in ("R", "RA", "RV"):
        w = {"R": 19, "RA": 14, "RV": 19}[kind]
        return f'<rect x="{-w}" y="-7" width="{2 * w}" height="14" {a}/>'
    if kind == "Rb":
        return (f'<rect x="-19" y="-7" width="38" height="14" {a}/>'
                f'<line x1="-13" y1="13" x2="13" y2="-13" {a}/><path d="M7,-14 L13,-13 L12,-7" {a}/>')
    if kind in ("A", "V"):
        return (f'<circle cx="0" cy="0" r="11" {a}/><text x="0" y="5" text-anchor="middle" font-size="13" font-weight="800" '
                f'fill="{c}" stroke="none" opacity="{op}">{kind}</text>')
    if kind == "E":                      # nguồn: vạch dài (+) ở bên trái, vạch ngắn (−) bên phải
        return (f'<line x1="-4" y1="-11" x2="-4" y2="11" {a}/><line x1="4" y1="-6" x2="4" y2="6" {a} stroke-width="3.2"/>')
    if kind == "K":
        if state == "closed":
            return (f'<line x1="-16" y1="0" x2="16" y2="0" {a}/><circle cx="-16" cy="0" r="2.6" fill="{c}"/>'
                    f'<circle cx="16" cy="0" r="2.6" fill="{c}"/>')
        return (f'<circle cx="-16" cy="0" r="2.6" fill="{c}"/><circle cx="16" cy="0" r="2.6" fill="{c}"/>'
                f'<line x1="-16" y1="0" x2="12" y2="-13" {a}/>')
    raise ValueError(kind)


def branch(p1, p2, elems, name_pos="auto", wc="currentColor", grey=False):
    """elems = [(kind, label, state)] hoặc (kind, label). Nhãn đặt trên (nhánh ngang) / bên phải (nhánh đứng)."""
    (x1, y1), (x2, y2) = p1, p2
    vert = abs(x1 - x2) < 1e-6
    L = abs(y2 - y1) if vert else abs(x2 - x1)
    sgn = (1 if y2 >= y1 else -1) if vert else (1 if x2 >= x1 else -1)
    hls = [HL[e[0]] for e in elems]
    free = L - 2 * sum(hls)
    assert free >= 8 * (len(elems) + 1) - 1e-6 or not elems, f"nhánh quá ngắn: L={L}, hl={hls}"
    gap = free / (len(elems) + 1) if elems else L
    op = .38 if grey else 1
    c = GREY if grey else wc
    out, pos = "", 0.0
    def at(s):  # toạ độ dọc nhánh
        return (x1, y1 + sgn * s) if vert else (x1 + sgn * s, y1)
    for i, e in enumerate(elems):
        kind, label = e[0], e[1]
        state = e[2] if len(e) > 2 else None
        start = pos + gap
        cen = start + hls[i]
        a, b = at(pos), at(start)
        out += line(*a, *b, c, 2.2, "", op)
        cx, cy = at(cen)
        rot = ' rotate(90)' if vert and kind not in ("A", "V") else ""
        if kind == "E" and vert:                      # nguồn đứng: + ở phía trên (p1 nếu đi xuống)
            rot = ' rotate(90)' if sgn > 0 else ' rotate(-90)'
        out += f'<g transform="translate({cx:.1f} {cy:.1f}){rot}">{_sym(kind, state, c, op)}</g>'
        if label:
            col = c if grey else "currentColor"
            parts = label.split("|")
            if vert:
                for j, t in enumerate(parts):
                    out += lab(cx + (16 if kind in ("R", "Rb", "RA", "RV") else 18), cy + 5 + (j - (len(parts) - 1) / 2) * 16 * (1 if len(parts) > 1 else 0), t, col, 15, "start")
            else:
                base = cy - (14 if kind in ("R", "Rb", "RA", "RV", "K") else 17)
                for j, t in enumerate(parts):
                    out += lab(cx, base - (len(parts) - 1 - j) * 15, t, col, 15)
        pos = start + 2 * hls[i]
    out += line(*at(pos), x2, y2, c, 2.2, "", op) if elems else line(x1, y1, x2, y2, c, 2.2, "", op)
    return out


def wire(*pts, c="currentColor", w=2.2, dash="", op=1):
    return "".join(line(*pts[i], *pts[i + 1], c, w, dash, op) for i in range(len(pts) - 1))


def sim(branches, vA=40.0, r=5.5):
    """branches = [((x1,y1),(x2,y2), I)] — chấm chạy từ p1 đến p2 (I < 0: ngược lại), một lần, khi bấm nút."""
    b = ""
    for (p1, p2, I) in branches:
        if I == 0:
            continue
        if I < 0:
            p1, p2, I = p2, p1, -I
        d = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** .5
        dur = d / (vA * I)
        b += (f'<circle cx="{p1[0]:.1f}" cy="{p1[1]:.1f}" r="{r}" fill="{GRN}" stroke="currentColor" stroke-width="1.4">'
              f'<animate attributeName="cx" values="{p1[0]:.1f};{p2[0]:.1f}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>'
              f'<animate attributeName="cy" values="{p1[1]:.1f};{p2[1]:.1f}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></circle>')
    return b


def fig(bt, vb, alt, body, cap, run=False):
    btn = '<button type="button" class="bt-run" data-bt-run="1">▶ Chạy mô phỏng</button>' if run else ""
    dbt = f' data-bt="{bt}"' if bt else ""
    return (f'<figure class="fig" data-tl="1"{dbt}><svg viewBox="{vb}" role="img" aria-label="{alt}">{body}</svg>'
            f'{btn}<figcaption>{cap}</figcaption></figure>')


# ═════════════ CÁC MẠCH DÙNG CHUNG (trả về (svg, hình học)) ═════════════
def c_hh(l1="R_1", l2="R_2", l3="R_3", A=True, V=True, Akind="A", Alabel="", Vkind="V", Vlabel="", kind2="R",
         grey=(), shortK=None, U="U", x0=50, xv=None, nodes=True):
    """R1 nối tiếp (R2 // R3); l3=None: chỉ R1 nối tiếp R2. A: ampe kế ở nhánh chính; V: vôn kế song song đoạn đo.
    shortK: None | "open" | "closed" — khoá K song song với R2 (nằm giữa R2 và R3)."""
    xm = 230
    xk = 285
    xr3 = None if l3 is None else (310 if shortK is None else 345)
    top, bot = 40, 160
    xv = xv or (xr3 + 80 if xr3 else xm + 100)
    b = branch((x0, top), (x0, bot), [("E", U)])
    b += branch((x0, top), (xm, top), ([(Akind, Alabel)] if A else []) + [("R", l1)])
    b += branch((xm, top), (xm, bot), [(kind2, l2)], grey=("R2" in grey))
    if shortK:
        b += branch((xk, top), (xk, bot), [("K", "K", shortK)])
    if xr3:
        b += branch((xr3, top), (xr3, bot), [("R", l3)], grey=("R3" in grey))
    end = xv if V else (xr3 or xm)
    b += wire((xm, top), (end, top)) + wire((x0, bot), (end, bot))
    if V:
        b += branch((xv, top), (xv, bot), [(Vkind, Vlabel)])
    if nodes:
        b += node(xm, top, "M", -2, -10) + node(xm, bot, "N", -2, 20)
        if shortK:
            b += node(xk, top, "", 0, 0) + node(xk, bot, "", 0, 0)
        if xr3:
            b += node(xr3, top, "", 0, 0) + node(xr3, bot, "", 0, 0)
        if V:
            b += node(xv, top, "", 0, 0) + node(xv, bot, "", 0, 0)
    geom = dict(src=((x0, top), (x0, bot)), r1=((x0, top), (xm, top)), r2=((xm, top), (xm, bot)),
                r3=((xr3, top), (xr3, bot)) if xr3 else None, k=((xk, top), (xk, bot)), v=((xv, top), (xv, bot)),
                bot=((xm, bot), (x0, bot)), xv=xv, width=xv + 40)
    return b, geom


def c_red(l1="R_1", l2="R_{23}", x0=50, xm=230, note=()):
    """Mạch thu gọn: nguồn, R1 trên, một điện trở ở bên phải; `note` = các dòng chữ ghi bên phải."""
    b = branch((x0, 40), (xm, 40), [("R", l1)]) + branch((xm, 40), (xm, 160), [("R", l2)]) \
        + branch((x0, 40), (x0, 160), [("E", "U")]) + wire((x0, 160), (xm, 160))
    for j, t in enumerate(note):
        b += lab(xm + 62, 92 + 26 * j, t, "currentColor", 13, "start", "700")
    return b


def sim_hh(g, I, I2, I3=None, Ik=None, vA=40.0):
    """Mô phỏng cho c_hh: dòng đi từ cực + của nguồn (nguồn đứng, + ở trên) ra, qua các nhánh, về cực −."""
    br = [(g["src"][1], g["src"][0], I), (g["r1"][0], g["r1"][1], I), (g["r2"][0], g["r2"][1], I2), (g["bot"][0], g["bot"][1], I)]
    if g["r3"] and I3 is not None:
        br.append((g["r3"][0], g["r3"][1], I3))
    return sim(br, vA)


def c_bridge(l1="R_1", l2="R_2", l3="R_3", l4="R_4", mid=("V", ""), x0=50, xl=170, xr=300, U="U"):
    """Cầu: nhánh trái M-R1-P-R3-N, nhánh phải M-R2-Q-R4-N, giữa P-Q có phần tử `mid` (None = dây trần)."""
    top, bot, ym = 30, 170, 100
    b = branch((x0, top), (x0, bot), [("E", U)])
    b += wire((x0, top), (xr, top)) + wire((x0, bot), (xr, bot))
    b += branch((xl, top), (xl, bot), [("R", l1), ("R", l3)])
    b += branch((xr, top), (xr, bot), [("R", l2), ("R", l4)])
    b += branch((xl, ym), (xr, ym), [mid] if mid else [])
    b += node(xl, top, "", 0, 0) + node(xr, top, "", 0, 0) + node(xl, bot, "", 0, 0) + node(xr, bot, "", 0, 0)
    b += node(xl, ym, "P", -13, 4) + node(xr, ym, "Q", 12, 4)
    b += lab((x0 + xr) / 2, top - 9, "M") + lab((x0 + xr) / 2, bot + 20, "N")
    geom = dict(top=top, bot=bot, ym=ym, xl=xl, xr=xr, x0=x0)
    return b, geom


def c_3tier(l1, l2, l3, l4, l5, U="U", boxes=False):
    """R1 nối tiếp [R2 // (R3 nối tiếp (R4 // R5))]; ampe kế A2 ở nhánh chính, ampe kế A1 nối tiếp R4."""
    x0, xm, x2, x3, x4, x5 = 50, 170, 215, 280, 345, 410
    top, bot, ys = 54, 214, 124
    b = branch((x0, top), (x0, bot), [("E", U)])
    b += branch((x0, top), (xm, top), [("A", "A_2"), ("R", l1)])
    b += wire((xm, top), (x3, top)) + wire((x0, bot), (x5, bot))
    b += branch((x2, top), (x2, bot), [("R", l2)])
    b += branch((x3, top), (x3, ys), [("R", l3)])
    b += wire((x3, ys), (x5, ys))
    b += branch((x4, ys), (x4, bot), [("A", "A_1"), ("R", l4)])
    b += branch((x5, ys), (x5, bot), [("R", l5)])
    b += node(xm, top, "M", -2, -10) + node(x2, top, "", 0, 0) + node(x3, ys, "S", -12, 4) + node(x4, ys, "", 0, 0) \
        + node(x2, bot, "N", 0, 20) + node(x4, bot, "", 0, 0) + node(x5, bot, "", 0, 0)
    if boxes:
        b += (f'<rect x="{x4 - 24}" y="{ys - 14}" width="{x5 - x4 + 76}" height="{bot - ys + 30}" rx="8" fill="none" stroke="{ORG}" '
              f'stroke-width="1.8" stroke-dasharray="5 4"/>' + lab(x4 - 4, ys - 20, "R_{45}", ORG, 13))
        b += (f'<rect x="{x3 - 40}" y="{top - 20}" width="{x5 - x3 + 120}" height="{bot - top + 48}" rx="10" fill="none" stroke="{BLUE}" '
              f'stroke-width="1.8" stroke-dasharray="5 4"/>' + lab(x3 - 24, top - 26, "Y", BLUE, 14))
    geom = dict(src=((x0, top), (x0, bot)), r1=((x0, top), (xm, top)), r2=((x2, top), (x2, bot)), r3=((x3, top), (x3, ys)),
                r4=((x4, ys), (x4, bot)), r5=((x5, ys), (x5, bot)), bot=((x2, bot), (x0, bot)), M=(xm, top))
    return b, geom
