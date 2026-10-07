"""Sinh 4 hình SVG cho bài 'Bài 7. Lăng kính' (KHTN 9, lesson_id 85) và thay mốc <!--FIGn--> trong theory.src.html -> theory.html.
Mọi tia sáng được dò bằng định luật khúc xạ (vectơ Snell), không vẽ ước lượng. Toạ độ SVG: y hướng xuống."""
import math, pathlib, re
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
FS, FSUB = 17, 13           # cỡ chữ tối thiểu, chỉ số dưới

# ---------- hình học + khúc xạ ----------
def norm(v):
    n = math.hypot(*v); return (v[0] / n, v[1] / n)
def dot(a, b): return a[0] * b[0] + a[1] * b[1]
def add(a, b, k=1.0): return (a[0] + k * b[0], a[1] + k * b[1])

def refract(d, nrm, n1, n2):
    """d: hướng tia (đơn vị); nrm: pháp tuyến đơn vị hướng VỀ phía tia tới. Trả hướng khúc xạ hoặc None (phản xạ toàn phần)."""
    ci = -dot(nrm, d)
    eta = n1 / n2
    k = 1 - eta * eta * (1 - ci * ci)
    if k < 0: return None
    return norm((eta * d[0] + (eta * ci - math.sqrt(k)) * nrm[0], eta * d[1] + (eta * ci - math.sqrt(k)) * nrm[1]))

def hit(p, d, a, b):
    """Giao điểm tia p + t·d (t>1e-6) với đoạn ab; trả (t, điểm) hoặc None."""
    ex, ey = b[0] - a[0], b[1] - a[1]
    den = d[0] * ey - d[1] * ex
    if abs(den) < 1e-12: return None
    t = ((a[0] - p[0]) * ey - (a[1] - p[1]) * ex) / den
    s = ((a[0] - p[0]) * d[1] - (a[1] - p[1]) * d[0]) / den
    if t > 1e-6 and -1e-9 <= s <= 1 + 1e-9: return t, (p[0] + t * d[0], p[1] + t * d[1])
    return None

def outward_normal(a, b, inside):
    e = norm((b[0] - a[0], b[1] - a[1])); n = (e[1], -e[0])
    mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    if dot(n, (inside[0] - mid[0], inside[1] - mid[1])) > 0: n = (-n[0], -n[1])
    return n

def trace(prism, S, d, n):
    """Dò tia qua lăng kính (đa giác lồi). Trả (I, J, d_trong, d_ra)."""
    cen = (sum(p[0] for p in prism) / len(prism), sum(p[1] for p in prism) / len(prism))
    edges = [(prism[k], prism[(k + 1) % len(prism)]) for k in range(len(prism))]
    best = min((h for h in (hit(S, d, a, b) + (a, b) if hit(S, d, a, b) else None for a, b in edges) if h), key=lambda h: h[0])
    _, I, a, b = best
    no = outward_normal(a, b, cen)
    d1 = refract(d, no, 1.0, n)
    best2 = min((h for h in (hit(I, d1, a2, b2) + (a2, b2) if hit(I, d1, a2, b2) else None for a2, b2 in edges) if h and h[0] > 1e-3), key=lambda h: h[0])
    _, J, a2, b2 = best2
    no2 = outward_normal(a2, b2, cen)
    d2 = refract(d1, (-no2[0], -no2[1]), n, 1.0)
    return I, J, d1, d2, no, no2

def ang_between(u, v): return math.degrees(math.acos(max(-1, min(1, dot(norm(u), norm(v))))))

# ---------- tiện ích vẽ ----------
def P(x, y): return f"{x:.1f},{y:.1f}"
def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}" stroke-linecap="round"/>'
def ray(p, q, c, w=2.6, mid=True):
    """Tia sáng p→q, đầu V 30° đặt giữa đoạn (chỉ chiều truyền)."""
    s = line(*p, *q, c, w)
    if mid:
        m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        s += chevron(m[0], m[1], q[0] - p[0], q[1] - p[1], c, w, 11)
    return s
def poly(pts, fill="rgba(56,189,248,.14)", w=2.4):
    return f'<polygon points="{" ".join(P(*p) for p in pts)}" fill="{fill}" stroke="currentColor" stroke-width="{w}" stroke-linejoin="round"/>'
def T(x, y, s, c="currentColor", size=FS, anchor="start", weight="600"): return text(round(x, 1), round(y, 1), s, c, size, anchor, weight)
def sub(base, s): return f'{base}<tspan baseline-shift="sub" font-size="{FSUB}">{s}</tspan>'
def arc_dir(c, r, u, v, col="currentColor", w=1.8):
    """Cung tròn tâm c bán kính r, từ hướng u tới hướng v (góc nhỏ)."""
    u, v = norm(u), norm(v)
    p1, p2 = add(c, u, r), add(c, v, r)
    cross = u[0] * v[1] - u[1] * v[0]
    return f'<path d="M{P(*p1)} A{r},{r} 0 0 {1 if cross > 0 else 0} {P(*p2)}" fill="none" stroke="{col}" stroke-width="{w}"/>'

# ---------- Hình 1: cấu tạo lăng kính ----------
def fig1():
    # mặt trước (tiết diện) + mặt sau lệch (dx, dy) để gợi khối
    A, B, C = (130, 40), (40, 196), (220, 196)
    dx, dy = 150, -14
    A2, B2, C2 = add(A, (dx, dy)), add(B, (dx, dy)), add(C, (dx, dy))
    b = ""
    b += poly([A, A2, C2, C], "rgba(56,189,248,.10)")           # mặt bên phải
    b += line(*B, *B2, "currentColor", 1.6, "5 4", .7)          # cạnh đáy khuất
    b += line(*A2, *B2, "currentColor", 1.6, "5 4", .7)         # cạnh khuất
    b += poly([A, B, C], "rgba(251,146,60,.18)")                # tiết diện (mặt trước)
    b += line(*A, *A2, "currentColor", 2.4)
    # góc chiết quang A
    b += arc_dir(A, 34, (B[0] - A[0], B[1] - A[1]), (C[0] - A[0], C[1] - A[1]), RED, 2.2)
    b += T(A[0] - 6, A[1] + 58, "A", RED, 18, "middle", "700")
    # nhãn
    b += T(A2[0] + 8, A2[1] - 6, "Cạnh", "currentColor", FS, "start", "700")
    b += T(46, 62, "Mặt bên", "currentColor", FS, "start", "600")
    b += line(78, 70, 92, 108, "currentColor", 1.4, "", .8)
    b += T(252, 152, "Mặt bên", "currentColor", FS, "start", "600")
    b += T(224, 226, "Đáy (mặt dưới)", "currentColor", FS, "middle", "700")
    b += T(130, 178, "Tiết diện", ORG, FS, "middle", "700")
    return wrap("0 0 420 248", "Lăng kính tam giác: hai mặt bên, cạnh, đáy, góc chiết quang A ở đỉnh tiết diện",
                b, "Hình 1. Lăng kính: hai mặt bên gặp nhau ở cạnh; mặt đối diện là đáy. Góc <em>A</em> giữa hai mặt bên là góc chiết quang. Trên tiết diện (tam giác), mỗi mặt bên chỉ hiện ra là một cạnh của tam giác.")

# ---------- lăng kính đều A = 60° dùng cho hình 2, 3 ----------
def prism60(apex, side):
    h = side * math.sin(math.radians(60))
    return [apex, (apex[0] - side / 2, apex[1] + h), (apex[0] + side / 2, apex[1] + h)]

def incident_dir(prism, i_deg):
    """Hướng tia tới mặt trái với góc tới i, tia đi lên-phải (quay từ pháp tuyến hướng vào trong về phía đỉnh)."""
    a, b = prism[0], prism[1]
    cen = (sum(p[0] for p in prism) / 3, sum(p[1] for p in prism) / 3)
    no = outward_normal(a, b, cen); ni = (-no[0], -no[1])
    t = math.radians(-i_deg)                    # quay ngược chiều kim đồng hồ trên màn hình (y xuống) = ngả lên
    return norm((ni[0] * math.cos(t) - ni[1] * math.sin(t), ni[0] * math.sin(t) + ni[1] * math.cos(t)))

def fig2():
    N = 1.5; I_DEG = 45
    pr = prism60((190, 34), 250)
    d0 = incident_dir(pr, I_DEG)
    I_on = (pr[0][0] + 0.52 * (pr[1][0] - pr[0][0]), pr[0][1] + 0.52 * (pr[1][1] - pr[0][1]))
    S = add(I_on, d0, -110)
    I, J, d1, d2, no, no2 = trace(pr, S, d0, N)
    R = add(J, d2, 150)
    ext = add(J, d0, 150)                        # phương tia tới vẽ lại qua J
    D = ang_between(d0, d2)
    global FIG2_INFO
    FIG2_INFO = dict(r1=ang_between(d1, (-no[0], -no[1])), i2=ang_between(d2, no2), D=D)
    b = poly(pr)
    b += line(*add(I, no, 46), *add(I, no, -46), "currentColor", 1.5, "5 4", .75)
    b += line(*add(J, no2, 46), *add(J, no2, -46), "currentColor", 1.5, "5 4", .75)
    b += line(*J, *ext, "currentColor", 1.5, "3 5", .6)
    b += ray(S, I, RED) + ray(I, J, RED) + ray(J, R, RED)
    b += arc_dir(J, 66, d0, d2, GRN, 2.2)
    # nhãn D đặt trên đường phân giác góc lệch
    bis = norm(add(d0, d2))
    lp = add(J, bis, 84)
    b += T(lp[0] + 4, lp[1] + 6, "D", GRN, 18, "start", "700")
    b += T(12, S[1] + 26, "Tia tới", RED, FS, "start", "700")
    b += T(R[0] - 4, R[1] + 22, "Tia ló", RED, FS, "end", "700")
    b += T(pr[0][0], pr[1][1] + 24, "Đáy", "currentColor", FS, "middle", "700")
    b += T(pr[0][0] + 12, pr[0][1] + 4, "Cạnh", "currentColor", FS, "start", "600")
    b += T(I[0] + 8, I[1] + 30, "I", "currentColor", FS, "start", "700")
    b += T(J[0] - 10, J[1] + 30, "J", "currentColor", FS, "end", "700")
    return wrap("0 0 420 290", "Tia sáng đỏ đơn sắc khúc xạ hai lần qua lăng kính tại I và J, tia ló lệch về phía đáy một góc D",
                b, "Hình 2. Tia đơn sắc khúc xạ ở <em>I</em> và <em>J</em> (nét đứt: pháp tuyến), tia ló lệch về phía đáy. Góc lệch <em>D</em> là góc giữa phương tia tới (chấm mờ, vẽ lại qua <em>J</em>) và tia ló. Vẽ với chiết suất giả định $n = 1{,}5,$ góc tới $45^\\circ.$")

# ---------- Hình 3: tán sắc ánh sáng trắng ----------
COLORS = [("đỏ", "#f87171", 1.50), ("cam", "#fb923c", 1.52), ("vàng", "#eab308", 1.54), ("lục", "#22c55e", 1.56),
          ("lam", "#38bdf8", 1.58), ("chàm", "#818cf8", 1.60), ("tím", "#c084fc", 1.62)]
def fig3():
    pr = prism60((196, 30), 230)
    d0 = incident_dir(pr, 48)
    I_on = (pr[0][0] + 0.5 * (pr[1][0] - pr[0][0]), pr[0][1] + 0.5 * (pr[1][1] - pr[0][1]))
    S = add(I_on, d0, -120)
    screen_x = 384
    b = poly(pr)
    info = []
    ends = []
    for name, col, n in COLORS:
        I, J, d1, d2, no, no2 = trace(pr, S, d0, n)
        t = (screen_x - J[0]) / d2[0]
        E = add(J, d2, t)
        b += line(*I, *J, col, 1.8, "", .95) + line(*J, *E, col, 2.6)
        ends.append(E)
        info.append((name, ang_between(d0, d2), E[1]))
    b += ray(S, I, "currentColor", 3)
    b += line(screen_x, ends[0][1] - 40, screen_x, ends[-1][1] + 40, "currentColor", 3)
    b += T(screen_x, ends[-1][1] + 62, "Màn", "currentColor", FS, "middle", "700")
    b += T(screen_x + 8, ends[0][1] - 4, "đỏ", "currentColor", FS, "start", "700")
    b += T(screen_x + 8, ends[-1][1] + 14, "tím", "currentColor", FS, "start", "700")
    b += T(8, S[1] + 28, "Ánh sáng", "currentColor", FS, "start", "700") + T(8, S[1] + 50, "trắng", "currentColor", FS, "start", "700")
    b += T(pr[0][0], pr[1][1] + 24, "Đáy", "currentColor", FS, "middle", "700")
    global FIG3_INFO
    FIG3_INFO = info
    # thứ tự trên màn phải đúng: đỏ cao nhất (y nhỏ nhất), tím thấp nhất
    ys = [e[1] for e in ends]
    assert ys == sorted(ys), ys
    return wrap("0 0 420 300", "Chùm sáng trắng qua lăng kính tách thành dải màu từ đỏ (trên, lệch ít) đến tím (dưới, lệch nhiều)",
                b, "Hình 3. Ánh sáng trắng tách thành dải màu trên màn: đỏ lệch ít nhất (trên cùng), tím lệch nhiều nhất (sát phía đáy). Trên màn, từ trên xuống: đỏ, cam, vàng, lục, lam, chàm, tím. Chiết suất giả định từ $1{,}50$ (đỏ) đến $1{,}62$ (tím), phóng đại để dễ nhìn; thuỷ tinh thật chỉ khoảng $1{,}51$ đến $1{,}53.$")

# ---------- Hình 4: bài toán mẫu, lăng kính vuông tại B, A = 30° ----------
def fig4():
    N = 1.5
    Ap, Bp = (110, 34), (110, 274)
    Cp = (Bp[0] + (Bp[1] - Ap[1]) * math.tan(math.radians(30)), Bp[1])
    pr = [Ap, Bp, Cp]
    S = (20, 168); d0 = (1.0, 0.0)
    I, J, d1, d2, no, no2 = trace(pr, S, d0, N)
    R = add(J, d2, 175)
    global FIG4_INFO
    FIG4_INFO = dict(i2=ang_between(d1, no2), r=ang_between(d2, no2), D=ang_between(d0, d2))
    b = poly(pr)
    b += line(*add(J, no2, 70), *add(J, no2, -40), "currentColor", 1.5, "5 4", .75)
    b += line(*J, *add(J, d0, 175), "currentColor", 1.5, "3 5", .6)
    b += ray(S, I, RED) + ray(I, J, RED) + ray(J, R, RED)
    # góc vuông ở I
    b += f'<path d="M{I[0]-12:.1f},{I[1]:.1f} L{I[0]-12:.1f},{I[1]-12:.1f} L{I[0]:.1f},{I[1]-12:.1f}" fill="none" stroke="currentColor" stroke-width="1.5"/>'
    # góc A
    b += arc_dir(Ap, 50, (Bp[0] - Ap[0], Bp[1] - Ap[1]), (Cp[0] - Ap[0], Cp[1] - Ap[1]), "currentColor", 1.8)
    b += T(Ap[0] + 3, Ap[1] + 84, "30°", "currentColor", FS, "start", "700")
    b += arc_dir(J, 58, d0, d2, GRN, 2.2)
    b += T(J[0] + 66, J[1] + 17, "D", GRN, FS, "start", "700")
    b += T(Ap[0] - 8, Ap[1] + 6, "A", "currentColor", 18, "end", "700")
    b += T(Bp[0] - 8, Bp[1] + 6, "B", "currentColor", 18, "end", "700")
    b += T(Cp[0] + 8, Cp[1] + 6, "C", "currentColor", 18, "start", "700")
    b += T(I[0] - 8, I[1] + 22, "I", "currentColor", FS, "end", "700")
    b += T(J[0] - 6, J[1] + 26, "J", "currentColor", FS, "end", "700")
    nt = add(J, no2, 70)
    b += T(nt[0] + 6, nt[1] + 2, "pháp tuyến", "currentColor", FS, "start", "600")
    b += T(R[0] - 2, R[1] + 22, "tia ló", RED, FS, "end", "700")
    b += T(S[0], S[1] - 12, "tia tới", RED, FS, "start", "700")
    b += T((Bp[0] + Cp[0]) / 2, Bp[1] + 22, "đáy BC", "currentColor", FS, "middle", "600")
    return wrap("0 0 420 300", "Lăng kính vuông tại B, góc A 30 độ; tia đỏ vuông góc mặt AB đi thẳng tới J trên AC, ló ra lệch về đáy BC một góc D",
                b, "Hình 4. Tia vuông góc <em>AB</em> đi thẳng tới <em>J</em>, khúc xạ ở mặt <em>AC</em>, lệch về đáy <em>BC</em> một góc <em>D</em> (so với phương tia tới kéo dài).")

figs = [fig1(), fig2(), fig3(), fig4()]

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, f in enumerate(figs, 1):
    assert f"<!--FIG{n}-->" in h, n
    h = h.replace(f"<!--FIG{n}-->", f)
(HERE / "theory.html").write_text(h, encoding="utf8")
print("ok", len(h))
print("Hình 2:", {k: round(v, 2) for k, v in FIG2_INFO.items()})
print("Hình 3:", [(n, round(D, 2)) for n, D, _ in FIG3_INFO])
print("Hình 4:", {k: round(v, 2) for k, v in FIG4_INFO.items()})
