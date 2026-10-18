"""Thư viện vẽ hình SVG cho bài lý thuyết (import: from svg_lib import *).
Xem ../references/hinh-svg.md. Mỗi hình dùng một tiền tố marker riêng: defs("f1")."""
RED, BLUE, ORG, GRN = "#f87171", "#38bdf8", "#fb923c", "#34d399"

def defs(prefix):
    out = "<defs>"
    for n, c in (("r", RED), ("b", BLUE), ("o", ORG), ("g", GRN)):
        out += (f'<marker id="{prefix}-{n}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
    return out + "</defs>"

def arrow(p, c, x1, y1, x2, y2, w=3, dash=""):
    col = {"r": RED, "b": BLUE, "o": ORG, "g": GRN}[c]
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}"{d} marker-end="url(#{p}-{c})"/>'

def text(x, y, s, c="currentColor", size=13, anchor="start", weight="600"):
    return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{s}</text>'

def person(x, ground, s=1.0, arm_to=None, arm_y=None):
    """Người trượt băng dạng que: đầu, thân, chân, giày trượt (lưỡi dao)."""
    hy = ground - 100 * s; ty = ground - 62 * s; fy = ground - 6 * s
    g = f'<circle cx="{x}" cy="{hy:.0f}" r="{12*s:.0f}" fill="none" stroke="currentColor" stroke-width="2.5"/>'
    g += f'<line x1="{x}" y1="{hy+12*s:.0f}" x2="{x}" y2="{ty:.0f}" stroke="currentColor" stroke-width="2.5"/>'
    g += f'<line x1="{x}" y1="{ty:.0f}" x2="{x-12*s:.0f}" y2="{fy:.0f}" stroke="currentColor" stroke-width="2.5"/>'
    g += f'<line x1="{x}" y1="{ty:.0f}" x2="{x+12*s:.0f}" y2="{fy:.0f}" stroke="currentColor" stroke-width="2.5"/>'
    g += f'<line x1="{x-22*s:.0f}" y1="{ground-2}" x2="{x+22*s:.0f}" y2="{ground-2}" stroke="{BLUE}" stroke-width="3" stroke-linecap="round"/>'
    sh = hy + 22 * s
    if arm_to is not None:
        g += f'<line x1="{x}" y1="{sh:.0f}" x2="{arm_to}" y2="{arm_y}" stroke="currentColor" stroke-width="2.5"/>'
    return g

def wrap(vb, label, body, cap):
    return (f'<figure class="fig" data-tl="1"><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')

