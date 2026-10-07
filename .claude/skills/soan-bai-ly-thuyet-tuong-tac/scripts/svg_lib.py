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



# ---- Đường sức: nét đứt + đầu mũi tên chữ V (hai vạch chéo 30° so với đường chính, đầu nhọn).
# Quy tắc chốt 7/10/2026 (xem references/hinh-svg.md). Không dùng marker: marker co theo bề dày nét làm đầu tù.
import math as _m

def chevron(x, y, dx, dy, c="currentColor", w=2, L=12, ang=30):
    """Đầu mũi tên chữ V tại (x, y) hướng (dx, dy): hai vạch dài L, mỗi vạch lệch `ang`° so với đường chính; góc nhọn (miter)."""
    n = _m.hypot(dx, dy) or 1
    ux, uy = dx / n, dy / n
    t = _m.radians(ang)
    pts = []
    for s in (1, -1):
        c_, s_ = _m.cos(t), _m.sin(s * t)
        bx, by = ux * c_ - uy * s_, ux * s_ + uy * c_      # hướng đường chính quay s·ang°
        pts.append((x - L * bx, y - L * by))
    (ax, ay), (bx, by) = pts
    return (f'<path d="M{ax:.1f},{ay:.1f} L{x:.1f},{y:.1f} L{bx:.1f},{by:.1f}" fill="none" stroke="{c}" stroke-width="{w}" '
            f'stroke-linejoin="miter" stroke-miterlimit="10" stroke-linecap="butt"/>')

def field_line(x1, y1, x2, y2, c="currentColor", w=1.8, dash="6 4", L=12):
    """Đường sức thẳng: nét đứt từ (x1,y1) tới đỉnh mũi tên (x2,y2) + đầu V."""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" stroke-dasharray="{dash}"/>'
            + chevron(x2, y2, x2 - x1, y2 - y1, c, w, L))

def field_path(d, tip, direction, c="currentColor", w=1.8, dash="6 4", L=12):
    """Đường sức cong: path nét đứt `d` + đầu V đặt tại điểm `tip`=(x,y) theo tiếp tuyến `direction`=(dx,dy)."""
    return (f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-dasharray="{dash}"/>'
            + chevron(tip[0], tip[1], direction[0], direction[1], c, w, L))


# ---- Hình 3D che khuất (dây thẳng, vòng dây, ống dây). Duyệt 7/10/2026.
# Quy ước: vật ở phía TRƯỚC thì nét liền đè lên; vật ở phía SAU bị che thì nét bị NGẮT một khe nhỏ chỗ vật trước đi qua.
# Đường tròn nhìn xiên = ellipse: tham số t (độ), x = cx + rx·cos t, y = cy + ry·sin t; t∈[0,180] là nửa TRƯỚC (thấp hơn trên hình), t∈[180,360] là nửa SAU.
def arc_pts(cx, cy, rx, ry, t0, t1, n=40):
    return [(cx + rx * _m.cos(_m.radians(t0 + (t1 - t0) * i / n)), cy + ry * _m.sin(_m.radians(t0 + (t1 - t0) * i / n))) for i in range(n + 1)]

def pts_path(pts, c="currentColor", w=2, dash=""):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}"{da} stroke-linecap="round" stroke-linejoin="round"/>'

def ell_tan(rx, ry, t, sgn=1):
    """Hướng tiếp tuyến của ellipse tại tham số t (sgn=+1: t tăng, -1: t giảm)."""
    r = _m.radians(t)
    return (-rx * _m.sin(r) * sgn, ry * _m.cos(r) * sgn)

def ell_pt(cx, cy, rx, ry, t):
    r = _m.radians(t)
    return cx + rx * _m.cos(r), cy + ry * _m.sin(r)

def cubic(p0, p1, p2, p3, n=60):
    out = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        out.append((u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0], u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]))
    return out

def chev_on(P, i, c, w=2.2, L=12):
    """Đầu V tại điểm thứ i của đường gấp khúc P, hướng theo chiều đi của P."""
    (x, y), (x2, y2) = P[i], P[i + 1]
    return chevron(x, y, x2 - x, y2 - y, c, w, L)
