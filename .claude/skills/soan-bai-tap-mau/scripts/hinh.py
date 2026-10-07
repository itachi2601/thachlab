"""Hình SVG cho gợi ý bài tập mẫu (dùng chung với soan-bai-ly-thuyet-tuong-tac/scripts/svg_lib.py).
Mỗi gợi ý = 1 hình + lời; hình dựng từ quỹ đạo TÍNH THẬT (không vẽ tay) để không lệch số liệu."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *  # RED, BLUE, ORG, GRN, defs, arrow, text

G = 9.8
W = 420

def poly(pts, c=GRN, w=2.4, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline fill="none" stroke="{c}" stroke-width="{w}"{d} opacity="{op}" points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>'

def seg(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'

def dot(x, y, r=4.5, c="currentColor"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'

def lbl(x, y, s, c="currentColor", size=13, anchor="start", weight="600"):
    return text(round(x, 1), round(y, 1), s, c, size, anchor, weight)

def arc(cx, cy, r, a0, a1, c=RED, w=1.8):
    """Cung tròn tâm (cx,cy) từ góc a0 đến a1 (độ, ngược chiều kim đồng hồ khi nhìn màn hình, Oy lên)."""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
    return f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 0 0 {x1:.1f},{y1:.1f}" fill="none" stroke="{c}" stroke-width="{w}"/>'

def ground(y, x0=16, x1=410):
    return f'<rect x="{x0}" y="{y:.1f}" width="{x1 - x0}" height="8" fill="none" stroke="currentColor" stroke-width="2"/>'

def axes(p, ox, oy, up=False, ln=70):
    """Hệ trục tại O: Ox sang phải; Oy hướng lên (up) hoặc xuống."""
    b = arrow(p, "g", ox, oy, ox + ln, oy, 2) + lbl(ox + ln + 4, oy + 5, "x", GRN, 13)
    y2 = oy - ln if up else oy + ln
    b += arrow(p, "g", ox, oy, ox, y2, 2) + lbl(ox + 6, y2 + (4 if up else 12), "y", GRN, 13)
    b += dot(ox, oy, 4, "currentColor") + lbl(ox - 14, oy - 6, "O", "currentColor", 13, "end", "700")
    return b

def dim(p, c, x1, y1, x2, y2, label, lx, ly, anchor="start"):
    """Kích thước hai đầu mũi tên + nhãn."""
    return arrow(p, c, x1, y1, x2, y2, 1.8) + arrow(p, c, x2, y2, x1, y1, 1.8) + lbl(lx, ly, label, {"o": ORG, "b": BLUE, "r": RED, "g": GRN}[c], 13, anchor, "700")

def fig(bt, vb, alt, body, cap):
    run = '<button type="button" class="bt-run" data-bt-run="1">▶ Chạy mô phỏng</button>' if "<animate" in body else ""
    return (f'<figure class="fig" data-tl="1" data-bt="{bt}"><svg viewBox="{vb}" role="img" aria-label="{alt}">{body}</svg>'
            f'{run}<figcaption>{cap}</figcaption></figure>')

def plane(x, y):
    """Máy bay nhìn nghiêng, mũi quay phải, đáy khoang tại y."""
    return (f'<rect x="{x - 46}" y="{y - 11}" width="46" height="11" rx="5" fill="none" stroke="currentColor" stroke-width="2.4"/>'
            f'<path d="M{x - 40},{y - 11} L{x - 46},{y - 21} L{x - 46},{y - 11} Z" fill="none" stroke="currentColor" stroke-width="2"/>'
            + seg(x - 20, y, x - 28, y + 9, "currentColor", 2))

def ngang_geom(h, v0, O, wmax, hpx):
    T = math.sqrt(2 * h / G); L = v0 * T
    s = min(wmax / L, hpx / h)
    pts = [(O[0] + s * v0 * T * u / 40, O[1] + s * 0.5 * G * (T * u / 40) ** 2) for u in range(41)]
    return dict(T=T, L=L, s=s, pts=pts, gy=O[1] + s * h, land=(O[0] + s * L, O[1] + s * h))

def xien_geom(v0, alpha, h0, O, s, T=None):
    """Ném xiên từ O, Oy lên; h0 = độ cao O so với đất. Trả quỹ đạo từ lúc ném tới lúc chạm đất (y = -h0)."""
    a = math.radians(alpha); vx, vy = v0 * math.cos(a), v0 * math.sin(a)
    if T is None:
        T = (vy + math.sqrt(vy * vy + 2 * G * h0)) / G
    pts = [(O[0] + s * vx * T * u / 60, O[1] - s * (vy * T * u / 60 - 0.5 * G * (T * u / 60) ** 2)) for u in range(61)]
    tu = vy / G
    top = (O[0] + s * vx * tu, O[1] - s * (vy * tu - 0.5 * G * tu * tu))
    return dict(vx=vx, vy=vy, T=T, tu=tu, pts=pts, top=top, L=vx * T, land=pts[-1])
