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
    """Vectơ: thân thẳng + đầu V 30° (chevron) — KHÔNG dùng marker tam giác đặc (thầy chốt 7/10/2026).
    `p` giữ cho tương thích chữ ký cũ. Độ dài (x1,y1)→(x2,y2) PHẢI tỉ lệ độ lớn: dùng `vec_luc` cho lực."""
    col = {"r": RED, "b": BLUE, "o": ORG, "g": GRN}[c]
    d = f' stroke-dasharray="{dash}"' if dash else ""
    ww = min(w, 2.8)
    n = _m.hypot(x2 - x1, y2 - y1)
    L = max(5, min(3.4 * ww + 2, 0.6 * n))      # vectơ ngắn → đầu V nhỏ lại, thân vẫn đúng độ dài
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{ww}"{d}/>'
            + chevron(x2, y2, x2 - x1, y2 - y1, col, ww, L))

def vec_luc(c, x, y, dx, dy, F, k, w=3, dash="", min_len=8):
    """Vectơ lực/vận tốc từ gốc (x,y), hướng (dx,dy), độ dài = k·F (px) — cùng k cho MỌI vectơ cùng loại trong một hình
    (lực 2 N dài gấp đôi lực 1 N). Trả (svg, (x_ngọn, y_ngọn)). Ngắn hơn `min_len` thì báo lỗi: tăng k, đừng kéo dài giả."""
    n = _m.hypot(dx, dy) or 1
    L = k * F
    assert L >= min_len, f"vectơ F={F} dài {L:.1f}px < {min_len}: tăng k (tỉ lệ) rồi vẽ lại cả hình"
    x2, y2 = x + dx / n * L, y + dy / n * L
    return arrow("", c, x, y, round(x2, 1), round(y2, 1), w, dash), (x2, y2)

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


# ===== HÌNH CHUẨN (thầy duyệt 31/10/2026): nam châm chữ U. Từ nay mọi hình có nam châm chữ U dùng hàm này, không vẽ lại.
# ---- nam châm chữ U thật: thân bo góc, hai cánh, đầu cực tô màu, có chiều sâu xiên (dx, dy)
UM_BODY, UM_DARK, UM_EDGE = "#cbd5e1", "#94a3b8", "#334155"   # cùng bảng màu bài 9/10 (lực từ, khái niệm từ trường)
UM_N = ("#dc2626", "#f87171", "#b91c1c")      # mặt trước, mặt trên, mặt bên
UM_S = ("#2563eb", "#60a5fa", "#1e40af")


def u_path(x, y, w, h, arm, yoke, r, ri):
    yi = y + h - yoke
    return (f"M{x},{y} V{y+h-r} A{r},{r} 0 0 0 {x+r},{y+h} H{x+w-r} A{r},{r} 0 0 0 {x+w},{y+h-r} V{y} H{x+w-arm} "
            f"V{yi-ri} A{ri},{ri} 0 0 1 {x+w-arm-ri},{yi} H{x+arm+ri} A{ri},{ri} 0 0 1 {x+arm},{yi-ri} V{y} Z")


def u_magnet(x, y, w, h, arm, yoke, tip, d=(18, -12), r=None, ri=None, fs=17, sw=2):
    """Nam châm chữ U nhìn chính diện hơi xiên: mặt sau dời (dx, dy); trả SVG. Cực N bên trái, S bên phải."""
    dx, dy = d
    r = r if r is not None else min(arm, yoke) * 0.7
    ri = ri if ri is not None else min(arm, yoke) * 0.35
    P = lambda pts, f: f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="{f}" stroke="{UM_EDGE}" stroke-width="{sw}" stroke-linejoin="round"/>'
    o = f'<path d="{u_path(x + dx, y + dy, w, h, arm, yoke, r, ri)}" fill="{UM_DARK}" stroke="{UM_EDGE}" stroke-width="{sw}" stroke-linejoin="round"/>'
    xr = x + w
    o += P([(xr, y), (xr + dx, y + dy), (xr + dx, y + h - r + dy), (xr, y + h - r)], UM_DARK)          # mặt bên phải
    o += P([(xr, y), (xr + dx, y + dy), (xr + dx, y + tip + dy), (xr, y + tip)], UM_S[2])
    o += P([(x + arm, y), (x + arm + dx, y + dy), (x + arm + dx, y + tip + dy), (x + arm, y + tip)], UM_N[2])  # mặt trong cánh N
    o += P([(x, y), (x + arm, y), (x + arm + dx, y + dy), (x + dx, y + dy)], UM_N[1])                  # mặt trên hai cánh
    o += P([(xr - arm, y), (xr, y), (xr + dx, y + dy), (xr - arm + dx, y + dy)], UM_S[1])
    k = 0.2929 * r                                                                                       # đường viền góc bo
    o += f'<line x1="{xr - k:.1f}" y1="{y + h - k:.1f}" x2="{xr - k + dx:.1f}" y2="{y + h - k + dy:.1f}" stroke="{UM_EDGE}" stroke-width="{sw}"/>'
    o += f'<path d="{u_path(x, y, w, h, arm, yoke, r, ri)}" fill="{UM_BODY}" stroke="{UM_EDGE}" stroke-width="{sw}" stroke-linejoin="round"/>'
    o += (f'<rect x="{x}" y="{y}" width="{arm}" height="{tip}" fill="{UM_N[0]}" stroke="{UM_EDGE}" stroke-width="{sw}"/>'
          f'<rect x="{xr - arm}" y="{y}" width="{arm}" height="{tip}" fill="{UM_S[0]}" stroke="{UM_EDGE}" stroke-width="{sw}"/>')
    o += text(x + arm / 2, y + tip / 2 + fs * .36, "N", "#fff", fs, "middle", "800")
    o += text(xr - arm / 2, y + tip / 2 + fs * .36, "S", "#fff", fs, "middle", "800")
    return o
