"""Bài tập mẫu CĐ14 "Gương phẳng, bóng tối và nửa tối" (lesson 158) — Dạng 4–7 (phần ảnh qua gương phẳng).
Module được build-hinh-158.py import. Dàn ý: content/hsg9/cd14-guong-phang-bong-toi/nguon.md mục "Bài tập mẫu" (số liệu dùng nguyên,
đã tính ở tinh.py cùng thư mục; kiem_so() tính lại bằng hình học véc-tơ).
Dạng sau dùng lại cách làm dạng trước:
  D4 ảnh khi vật/gương dịch chuyển (ảnh đối xứng qua gương tại mỗi thời điểm)
  D5 vùng nhìn thấy, gương thấy toàn thân (ảnh của mắt + hai mép gương; điểm tới là trung điểm theo phương ngang)
  D6 tia qua điểm cho trước, đường ngắn nhất (nối ảnh với điểm kia; hai gương: lấy ảnh hai lần)
  D7 hai gương hợp góc (chuỗi ảnh của D6, góc lệch mỗi lần phản xạ 180° − 2i của D1).
Sai sót docx đã tránh (nguon.md): góc giữa tia ló và tia tới = 2α chỉ khi α ≤ 90° (D7b chọn α = 72°); tia tới đi vào từ miệng góc
không bị G₂ chắn khi 90° − i₁ < α (D7b: 65° < 72°, D7c: 20° < 35°); α = 100° số ảnh phụ thuộc vị trí S (3 hoặc 4) → đề ghi S trên phân giác.
Xuất DANG, BUILD, ANALYSIS, SOLS, STEPS (4 phần tử mỗi list) và kiem_so()."""
import math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *  # noqa: F401,F403  (fig, seg, lbl, dot, poly, chevron, arrow, arc, sol, M, P, A, buoc …)

T_ANH = "Ảnh của vật tạo bởi gương phẳng"
NOTE = "Hình minh hoạ, không đúng tỉ lệ."
GREY = "#94a3b8"
d2r, r2d = math.radians, math.degrees

# ═════════════ SỐ LIỆU (mọi đáp số tính ở đây, kiem_so() kiểm lại) ═════════════
# D4
D4_d, D4_v, D4_t1 = 3.0, 1.2, 1.5
D4_vg, D4_t2 = 0.4, 2.0
D4_beta = 60.0
D4_delta = 15.0
D4_vgan = 2 * D4_v                                   # 2,4 m/s
D4_l1 = 2 * D4_d - 2 * D4_v * D4_t1                  # 2,4 m
D4_vanh = 2 * D4_vg                                  # 0,8 m/s
D4_l2 = 2 * (D4_d + D4_vg * D4_t2)                   # 7,6 m
D4_vx, D4_vy = D4_v * math.cos(d2r(D4_beta)), D4_v * math.sin(d2r(D4_beta))   # dọc gương 0,6 ; vuông góc 1,039
D4_vgan_c = 2 * D4_vy                                # 2,078 m/s
D4_phi = 2 * D4_delta                                # 30°
D4_s = 2 * D4_d * math.sin(d2r(D4_phi) / 2)          # 1,553 m
# D5
D5_h, D5_md = 1.70, 0.12
D5_hm = D5_h - D5_md                                 # 1,58 m
D5_Q = D5_hm / 2                                     # 0,79 m
D5_P = (D5_hm + D5_h) / 2                            # 1,64 m
D5_PQ = D5_P - D5_Q                                  # 0,85 m
D5_gc, D5_gd = 0.60, 0.95
D5_gt = D5_gd + D5_gc                                # 1,55 m
D5_ylo = 2 * D5_gd - D5_hm                           # 0,32 m
D5_yhi = 2 * D5_gt - D5_hm                           # 1,52 m
D5_w, D5_dm, D5_L, D5_dm2 = 0.40, 0.30, 2.0, 0.60
D5_band = D5_w * (D5_dm + D5_L) / D5_dm              # 3,067 m
D5_band2 = D5_w * (D5_dm2 + D5_L) / D5_dm2           # 1,733 m
D5_ex, D5_ey = 0.5, 0.5                              # mắt lệch: x = 0,5 m ; cách gương 0,5 m
D5_xA, D5_xB = -1.5, -3.4


def d5_cut(xs):
    """Giao của đoạn O'S (O' = ảnh của mắt) với mặt phẳng gương y = 0; S trên tường y = L."""
    t = D5_ey / (D5_L + D5_ey)
    return D5_ex + t * (xs - D5_ex)


def d5_wall(xg):
    """Điểm trên tường ứng với tia qua điểm xg của gương (đường O' → xg kéo dài tới y = L)."""
    return D5_ex + (xg - D5_ex) * (D5_L + D5_ey) / D5_ey


D5_x1, D5_x2 = d5_wall(-D5_w / 2), d5_wall(D5_w / 2)  # −3,0 ; −1,0 m
# D6
D6_a, D6_b, D6_s = 30.0, 50.0, 60.0
D6_xI = D6_s * D6_a / (D6_a + D6_b)                  # 22,5 cm
D6_i = r2d(math.atan(D6_xI / D6_a))                  # 36,87°
D6_L = math.hypot(D6_s, D6_a + D6_b)                 # 100 cm
D6_v = 1.25
D6_t = D6_L / D6_v                                   # 80 s
D6_A, D6_B = (40.0, 20.0), (10.0, 50.0)
D6_A1 = (D6_A[0], -D6_A[1])
D6_A12 = (-D6_A1[0], D6_A1[1])                       # (−40; −20)
D6_A2 = (-D6_A[0], D6_A[1])                          # ảnh qua G2 trước (sai thứ tự)
_tJ = (0 - D6_A12[0]) / (D6_B[0] - D6_A12[0])
D6_J = (0.0, D6_A12[1] + _tJ * (D6_B[1] - D6_A12[1]))   # y = 36,0
_tI = (0 - D6_A1[1]) / (D6_J[1] - D6_A1[1])
D6_I = (D6_A1[0] + _tI * (D6_J[0] - D6_A1[0]), 0.0)     # x = 25,71
D6_Lc = math.dist(D6_A12, D6_B)                      # 86,02 cm
# D7
D7_al_b, D7_i1_b = 72.0, 25.0
D7_i2_b = D7_al_b - D7_i1_b                          # 47°
D7_D_b = (180 - 2 * D7_i1_b) + (180 - 2 * D7_i2_b)   # 216°
D7_goc_b = 360 - D7_D_b                              # 144°
D7_i1_c = 70.0
D7_al_c = (90 - (90 - D7_i1_c)) / 2                  # 35°
D7_e, D7_sx = 20.0, 6.0
D7_S1, D7_S2 = -D7_sx, 2 * D7_e - D7_sx              # −6 ; 34
D7_S12 = 2 * D7_e - D7_S1                            # 46
D7_S1S2 = D7_S2 - D7_S1                              # 40


def count_images(alpha, theta):
    """Số ảnh của điểm ở góc theta trong góc alpha giữa G1 (phương 0°) và G2 (phương alpha). Hai chuỗi ảnh xen kẽ;
    dừng khi ảnh nằm sau cả hai gương (góc trong [180°, 180° + alpha])."""
    imgs = set()
    for first in (1, 2):
        th, which = theta, first
        for _ in range(60):
            th = (-th) % 360 if which == 1 else (2 * alpha - th) % 360
            imgs.add(round(th, 6))
            if 180 - 1e-9 <= th <= 180 + alpha + 1e-9:
                break
            which = 3 - which
    return len(imgs)


def _refl(v, deg):
    m = (math.cos(d2r(deg)), math.sin(d2r(deg)))
    k = v[0] * m[0] + v[1] * m[1]
    return (2 * k * m[0] - v[0], 2 * k * m[1] - v[1])


def _ang(u, v):
    c = (u[0] * v[0] + u[1] * v[1]) / (math.hypot(*u) * math.hypot(*v))
    return r2d(math.acos(max(-1, min(1, c))))


def trace_wedge(alpha, i1, r0=1.0):
    """Tia tới G1 (phương 0°, gốc O) tại I1 = (r0, 0) với góc tới i1, đi về phía O. Trả (điểm tới, góc tới, hướng vào, hướng ra)."""
    v_in = (-math.sin(d2r(i1)), -math.cos(d2r(i1)))
    p, v, cur = (r0, 0.0), _refl(v_in, 0), 1
    pts, inc = [p], [i1]
    cr = lambda a_, b_: a_[0] * b_[1] - a_[1] * b_[0]
    for _ in range(30):
        mdeg = alpha if cur == 1 else 0.0
        m = (math.cos(d2r(mdeg)), math.sin(d2r(mdeg)))
        den = cr(m, v)
        if abs(den) < 1e-12:
            break
        t = -cr(m, p) / den
        if t <= 1e-9:
            break
        q = (p[0] + t * v[0], p[1] + t * v[1])
        if q[0] * m[0] + q[1] * m[1] < 0:
            break
        ii = _ang((-v[0], -v[1]), (-m[1], m[0]))
        inc.append(min(ii, 180 - ii))
        v = _refl(v, mdeg)
        p, cur = q, 3 - cur
        pts.append(p)
    return pts, inc, v_in, v


# ═════════════ HÌNH: helper ═════════════
def rich(s, size=14):
    """Nhãn SVG có chỉ số dưới: 'G_{1}' → tspan dy (chỉ số Unicode hiện như dấu phẩy ở một số máy)."""
    ms = list(re.finditer(r"_\{([^}]+)\}", s))
    if not ms:
        return s
    out = s[:ms[0].start()]
    for k, m in enumerate(ms):
        out += f'<tspan dy="4" font-size="{max(12, size - 2)}">{m.group(1)}</tspan>'
        nxt = ms[k + 1].start() if k + 1 < len(ms) else len(s)
        out += f'<tspan dy="-4">{s[m.end():nxt]}</tspan>' if s[m.end():nxt] else '<tspan dy="-4"></tspan>'
    return out


TXT_DARK = {BLUE: "#0369a1", ORG: "#c2410c", RED: "#b91c1c", GRN: "#047857"}   # chữ trên nền sáng: màu đậm


def txt(x, y, s, c="currentColor", size=14, anchor="start", weight="700", extra=""):
    size = max(size, 14)
    c = TXT_DARK.get(c, c)
    t = lbl(x, y, rich(s, size), c, size, anchor, weight)
    return t.replace("<text ", f"<text {extra} ", 1) if extra else t


def show_at(t, dur):
    k = max(0.001, min(0.999, t / dur))
    return (f'<animate attributeName="opacity" values="0;1" keyTimes="0;{k:.4f}" calcMode="discrete" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')


def show_between(k0, k1, dur):
    return (f'<animate attributeName="opacity" values="0;1;0" keyTimes="0;{k0:.4f};{k1:.4f}" calcMode="discrete" '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')


def anim_kt(attr, vals, kts, dur):
    return (f'<animate attributeName="{attr}" values="{";".join(f"{v:.1f}" for v in vals)}" '
            f'keyTimes="{";".join(f"{k:.4f}" for k in kts)}" dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')


def timed(t, s, x, y, c="currentColor", size=14, anchor="start", weight="700", k1=None, dur=None):
    a = show_between(t, k1, dur) if k1 is not None else show_at(t * dur, dur)
    return txt(x, y, s, c, size, anchor, weight, 'opacity="0"').replace("</text>", a + "</text>", 1)


def ray(x1, y1, x2, y2, c=ORG, w=2.2, dash="", head=True):
    """Tia sáng: nét liền, mũi tên chữ V ở giữa tia."""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    s = f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'
    if head:
        s += chevron((x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1, c, w, 10)
    return s


def mirror(x1, y1, x2, y2, side=None, c="currentColor", w=3, front=None):
    """Gương: nét đậm + gạch chéo ở MẶT SAU. `front` = một điểm ở phía mặt phản xạ (vật/mắt) — bắt buộc;
    phía gạch chéo tự chọn ngược phía `front` và được assert lại (tham số `side` cũ bị bỏ qua)."""
    assert front is not None, "mirror(): thiếu front (điểm phía mặt phản xạ)"
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    nx, ny = -uy, ux
    if nx * (front[0] - x1) + ny * (front[1] - y1) > 0:
        nx, ny = -nx, -ny
    assert nx * (front[0] - x1) + ny * (front[1] - y1) < 0, "gạch chéo cùng phía vật/mắt"
    s = f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"/>'
    k = 6.0
    while k < L - 2:
        px, py = x1 + ux * k, y1 + uy * k
        s += seg(px, py, px + nx * 7 - ux * 5, py + ny * 7 - uy * 5, c, 1.2, "", .7)
        k += 10
    return s


def dimh(x1, x2, y, label, c="currentColor", ly=None, size=14):
    s = seg(x1, y, x2, y, c, 1.4) + chevron(x1, y, -1, 0, c, 1.4, 7) + chevron(x2, y, 1, 0, c, 1.4, 7)
    s += seg(x1, y - 5, x1, y + 5, c, 1.2) + seg(x2, y - 5, x2, y + 5, c, 1.2)
    return s + txt((x1 + x2) / 2, ly if ly is not None else y - 6, label, c, size, "middle", "600")


def dimv(x, y1, y2, label, c="currentColor", lx=None, anchor="start", size=14):
    s = seg(x, y1, x, y2, c, 1.4) + chevron(x, y1, 0, -1, c, 1.4, 7) + chevron(x, y2, 0, 1, c, 1.4, 7)
    s += seg(x - 5, y1, x + 5, y1, c, 1.2) + seg(x - 5, y2, x + 5, y2, c, 1.2)
    return s + txt(lx if lx is not None else x + 6, (y1 + y2) / 2 + 5, label, c, size, anchor, "600")


def stick(x, floor, H, c="currentColor", dash="", eye=None):
    """Người dạng que, cao H px, đứng ở x trên sàn floor (đỉnh đầu ở floor − H). eye = độ cao mắt (px) → chấm mắt."""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    r = H * 0.075
    top = floor - H
    neck, hip = top + 2 * r, floor - H * 0.47
    s = f'<circle cx="{x:.1f}" cy="{top + r:.1f}" r="{r:.1f}" fill="none" stroke="{c}" stroke-width="2"{d}/>'
    s += f'<line x1="{x:.1f}" y1="{neck:.1f}" x2="{x:.1f}" y2="{hip:.1f}" stroke="{c}" stroke-width="2"{d}/>'
    s += f'<line x1="{x:.1f}" y1="{hip:.1f}" x2="{x - H * .09:.1f}" y2="{floor:.1f}" stroke="{c}" stroke-width="2"{d}/>'
    s += f'<line x1="{x:.1f}" y1="{hip:.1f}" x2="{x + H * .09:.1f}" y2="{floor:.1f}" stroke="{c}" stroke-width="2"{d}/>'
    s += f'<line x1="{x - H * .13:.1f}" y1="{neck + H * .12:.1f}" x2="{x + H * .13:.1f}" y2="{neck + H * .12:.1f}" stroke="{c}" stroke-width="2"{d}/>'
    if eye is not None:
        s += f'<circle cx="{x:.1f}" cy="{floor - eye:.1f}" r="2.6" fill="{RED}"/>'
    return s


def trail(pts, dur, k0, k1, c=ORG, w=2.4):
    """Đường tia hiện dần (stroke-dashoffset) từ phân số k0 tới k1 của dur, kèm chấm sáng chạy đều trên đường."""
    segs = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    tot = sum(segs)
    s = (f'<polyline fill="none" stroke="{c}" stroke-width="{w}" stroke-dasharray="{tot:.1f} {tot:.1f}" stroke-dashoffset="{tot:.1f}" points="'
         + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '">'
         + f'<animate attributeName="stroke-dashoffset" values="{tot:.1f};{tot:.1f};0;0" keyTimes="0;{k0:.4f};{k1:.4f};1" '
           f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/></polyline>')
    acc, kts = 0.0, [0.0, k0]
    for L in segs:
        acc += L
        kts.append(k0 + (k1 - k0) * acc / tot)
    kts.append(1.0)
    xs = [pts[0][0]] + [p[0] for p in pts] + [pts[-1][0]]
    ys = [pts[0][1]] + [p[1] for p in pts] + [pts[-1][1]]
    s += (f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="5" fill="{c}" stroke="currentColor" stroke-width="1.2">'
          f'{anim_kt("cx", xs, kts, dur)}{anim_kt("cy", ys, kts, dur)}</circle>')
    return s


# ═════════════ HÌNH ═════════════
# ───────────── Dạng 4 · ảnh khi người/gương dịch chuyển ─────────────
def d4(kk):
    b = ""
    if kk == 0:
        TT, T_REAL, k = 4.0, 1.8, 40.0                 # 40 px/m ; chạy chậm hơn thật 2,2 lần
        xm = 230
        b += mirror(xm, 20, xm, 212, front=(xm - 100, 100))
        b += txt(xm + 8, 36, "G", "currentColor", 14)
        x0, y0 = xm - k * D4_d, 180.0
        dx, dy = k * D4_vy * T_REAL, -k * D4_vx * T_REAL
        xs = [x0, x0 + dx]
        ys = [y0, y0 + dy]
        # vectơ v (1,2 m/s → 48 px) + góc 60° với phương song song gương
        b += seg(x0, y0, x0, y0 - 70, GREY, 1.4, "5 4")
        ux, uy = math.sin(d2r(D4_beta)), -math.cos(d2r(D4_beta))
        b += arrow("", "r", x0, y0, round(x0 + 48 * ux, 1), round(y0 + 48 * uy, 1), 2.4)
        b += arc(x0, y0, 30, 90 - D4_beta, 90, RED, 1.6) + txt(x0 + 6, y0 - 38, "60°", RED, 14)
        b += txt(x0 + 46, y0 - 26, "v", RED, 14)
        b += dimh(x0, xm, 204, "3,0 m", "currentColor", 222)
        # người và ảnh chạy đối xứng qua gương
        xi = [2 * xm - x for x in xs]
        b += (f'<line x1="{xs[0]:.1f}" y1="{ys[0]:.1f}" x2="{xi[0]:.1f}" y2="{ys[0]:.1f}" stroke="{GREY}" stroke-width="1.4" stroke-dasharray="4 4">'
              f'{anim_kt("x1", xs, [0, 1], TT)}{anim_kt("y1", ys, [0, 1], TT)}{anim_kt("x2", xi, [0, 1], TT)}{anim_kt("y2", ys, [0, 1], TT)}</line>')
        b += (f'<circle cx="{xs[0]:.1f}" cy="{ys[0]:.1f}" r="6" fill="{GRN}" stroke="currentColor" stroke-width="1.4">'
              f'{anim_kt("cx", xs, [0, 1], TT)}{anim_kt("cy", ys, [0, 1], TT)}</circle>')
        b += (f'<circle cx="{xi[0]:.1f}" cy="{ys[0]:.1f}" r="6" fill="none" stroke="{GRN}" stroke-width="2" stroke-dasharray="3 2">'
              f'{anim_kt("cx", xi, [0, 1], TT)}{anim_kt("cy", ys, [0, 1], TT)}</circle>')
        b += (txt(xs[0] - 10, ys[0] - 10, "P", "currentColor", 14, "end").replace("</text>", anim_kt("x", [xs[0] - 10, xs[1] - 10], [0, 1], TT) + anim_kt("y", [ys[0] - 10, ys[1] - 10], [0, 1], TT) + "</text>", 1))
        b += (txt(xi[0] + 10, ys[0] - 10, "P'", GRN, 14).replace("</text>", anim_kt("x", [xi[0] + 10, xi[1] + 10], [0, 1], TT) + anim_kt("y", [ys[0] - 10, ys[1] - 10], [0, 1], TT) + "</text>", 1))
        b += txt(16, 22, "Nhìn từ trên xuống: người đi xiên tới gương", "currentColor", 14)
        b += timed(.98, "ảnh đi hướng nào?", 248, 196, RED, 14, "start", "700", None, TT)
        b += timed(.98, "v' = ?", 248, 216, RED, 14, "start", "700", None, TT)
        return fig("c14-4-0", "0 0 420 232", "Nhìn từ trên xuống: người P đi xiên tới gương phẳng G với vận tốc hợp mặt gương 60 độ, ảnh P' chạy đối xứng phía sau gương",
                   b, "Mô phỏng: chạy chậm hơn thật khoảng 2 lần. Đoạn nét đứt nối người với ảnh luôn vuông góc với gương. Vận tốc của ảnh chưa vẽ.")
    # hình dữ kiện: (c) vận tốc xiên ; (d) gương quay quanh H
    xm = 150
    b += mirror(xm, 30, xm, 200, front=(50, 150)) + txt(xm + 8, 46, "G", "currentColor", 14)
    x0, y0 = 50.0, 150.0
    b += seg(x0, y0, x0, y0 - 80, GREY, 1.4, "5 4")
    ux, uy = math.sin(d2r(D4_beta)), -math.cos(d2r(D4_beta))
    b += arrow("", "r", x0, y0, round(x0 + 60 * ux, 1), round(y0 + 60 * uy, 1), 2.4)
    b += arc(x0, y0, 30, 90 - D4_beta, 90, RED, 1.6) + txt(x0 + 4, y0 - 36, "60°", RED, 14)
    b += dot(x0, y0, 4.5) + txt(x0 - 6, y0 + 20, "P", "currentColor", 14, "middle")
    b += txt(xm - 8, y0 - 56, "v = 1,2 m/s", RED, 14, "end", "700")
    b += dimh(x0, xm, 212, "3,0 m", "currentColor", 230)
    b += txt(16, 22, "c)", "currentColor", 14)
    # (d)
    Hx, Hy, R = 320.0, 120.0, 80.0
    b += txt(226, 22, "d)", "currentColor", 14)
    b += mirror(Hx - 80, Hy, Hx + 80, Hy, front=(Hx, Hy + R)) + txt(Hx + 84, Hy + 5, "G", "currentColor", 14)
    gx, gy = math.cos(d2r(D4_delta)), -math.sin(d2r(D4_delta))
    b += seg(Hx - 80 * gx, Hy - 80 * gy, Hx + 80 * gx, Hy + 80 * gy, BLUE, 2.4, "7 4")
    b += txt(Hx + 80 * gx + 4, Hy + 80 * gy - 2, "G'", BLUE, 14)
    b += arc(Hx, Hy, 46, 0, D4_delta, BLUE, 1.6) + txt(Hx + 52, Hy - 2, "15°", BLUE, 14)
    b += dot(Hx, Hy, 4) + txt(Hx - 8, Hy + 18, "H", "currentColor", 14, "end")
    b += dot(Hx, Hy + R, 4.5) + txt(Hx - 8, Hy + R + 6, "P", "currentColor", 14, "end")
    b += dimv(Hx + 12, Hy + 4, Hy + R, "3,0 m", "currentColor")
    b += f'<circle cx="{Hx:.1f}" cy="{Hy - R:.1f}" r="5" fill="none" stroke="{GRN}" stroke-width="2" stroke-dasharray="3 2"/>'
    b += txt(Hx - 10, Hy - R + 5, "P'", GRN, 14, "end")
    b += txt(Hx + 10, Hy - R + 5, "ảnh dời = ?", RED, 14)
    return fig("c14-4-2", "0 0 420 240", "Hai hình nhìn từ trên xuống: c) người P cách gương 3,0 m đi xiên với vận tốc 1,2 m/s hợp mặt gương 60 độ; d) gương G quay 15 độ quanh trục qua H thành G', người P cách H 3,0 m",
               b, "Dữ kiện câu c và câu d. Ảnh sau khi quay gương chưa vẽ. " + NOTE)


# ───────────── Dạng 5 · vùng nhìn thấy, gương toàn thân ─────────────
def d5(kk):
    b = ""
    if kk == 0:
        TT = 5.0
        floor, xw, H = 206, 210, 130
        eye = H * D5_hm / D5_h
        b += seg(16, floor, 404, floor, "currentColor", 2)
        b += seg(xw, 34, xw, floor, BLUE, 2.4, "8 5")
        b += txt(xw, 30, "tường có gương: cao ?, treo ở đâu ?", BLUE, 14, "middle")
        xp0, xp1 = 262, 372
        man = stick(0, floor, H, "currentColor", "", eye)
        img = stick(0, floor, H, GRN, "5 3", eye)
        b += (f'<g transform="translate({xp0} 0)">{man}<animateTransform attributeName="transform" type="translate" '
              f'values="{xp0} 0;{xp0} 0;{xp1} 0;{xp1} 0" keyTimes="0;.15;.85;1" dur="{TT:.2f}s" begin="indefinite" fill="freeze"/></g>')
        xi0, xi1 = 2 * xw - xp0, 2 * xw - xp1
        b += (f'<g transform="translate({xi0} 0)">{img}<animateTransform attributeName="transform" type="translate" '
              f'values="{xi0} 0;{xi0} 0;{xi1} 0;{xi1} 0" keyTimes="0;.15;.85;1" dur="{TT:.2f}s" begin="indefinite" fill="freeze"/></g>')
        b += txt(300, 226, "người", "currentColor", 14, "start", "600") + txt(120, 226, "ảnh (ảo)", GRN, 14, "end", "600")
        b += timed(.86, "lùi xa: thấy nhiều hơn, ít hơn hay như cũ?", 16, 56, RED, 14, "start", "700", None, TT)
        return fig("c14-5-0", "0 0 420 236", "Nhìn ngang: người đứng trước bức tường có gương rồi lùi ra xa; ảnh ảo phía sau gương lùi theo, luôn đối xứng với người qua mặt gương",
                   b, "Mô phỏng: người lùi ra xa gương, ảnh lùi theo. Không vẽ tia nhìn và vị trí gương. " + NOTE)
    # hình dữ kiện: người 1,70 m, mắt thấp hơn đỉnh 12 cm ; gương câu b
    floor, kpx = 226, 100.0
    xp, xw = 290, 130
    b += seg(16, floor, 404, floor, "currentColor", 2)
    b += seg(xw, 28, xw, floor, "currentColor", 1.6)
    b += stick(xp, floor, kpx * D5_h, "currentColor", "", kpx * D5_hm)
    yt, yb = floor - kpx * D5_gt, floor - kpx * D5_gd
    b += mirror(xw, yb, xw, yt, c=BLUE, w=4, front=(xp, 150))
    b += txt(xw + 8, yb + 20, "gương câu b", BLUE, 14)
    b += dimv(xw - 22, yt, yb, "0,60 m", BLUE, xw - 28, "end")
    b += dimv(xw - 22, yb + 2, floor, "0,95 m", BLUE, xw - 28, "end")
    b += dimv(xp + 64, floor - kpx * D5_h, floor, "1,70 m", "currentColor")
    ye = floor - kpx * D5_hm
    b += seg(xp + 6, ye, xp + 40, ye, RED, 1.2, "3 3") + seg(xp + 6, floor - kpx * D5_h, xp + 40, floor - kpx * D5_h, "currentColor", 1.2, "3 3")
    b += txt(xp + 66, floor - kpx * D5_h - 6, "mắt thấp hơn đỉnh 12 cm", "currentColor", 14, "end", "600")
    b += txt(xp - 22, ye + 5, "mắt", RED, 14, "end")
    return fig("c14-5-2", "0 0 420 240", "Nhìn ngang: người cao 1,70 m, mắt thấp hơn đỉnh đầu 12 cm, đứng trước tường; gương câu b cao 0,60 m, mép dưới cách sàn 0,95 m",
               b, "Dữ kiện câu a và câu b (nhìn ngang). Câu c, d xét nhìn từ trên xuống. " + NOTE)


# ───────────── Dạng 6 · tia qua điểm cho trước, đường ngắn nhất ─────────────
def d6(kk):
    b = ""
    if kk == 0:
        TT, k = 6.0, 3.0                                 # 3 px/m
        bank = 196
        xa, xb = 60.0, 60.0 + k * D6_s
        A_, B_ = (xa, bank - k * D6_a), (xb, bank - k * D6_b)
        Mx = (xa + xb) / 2
        b += f'<rect x="10" y="{bank}" width="400" height="26" fill="{BLUE}" fill-opacity=".22" stroke="none"/>'
        b += seg(10, bank, 410, bank, BLUE, 2.4) + txt(400, bank + 19, "sông", BLUE, 14, "end")
        b += seg(xa, A_[1], xa, bank, GREY, 1.2, "4 3") + seg(xb, B_[1], xb, bank, GREY, 1.2, "4 3")
        b += f'<polygon points="{xa - 14},{A_[1] + 8} {xa},{A_[1] - 10} {xa + 14},{A_[1] + 8}" fill="{ORG}" fill-opacity=".35" stroke="{ORG}" stroke-width="2"/>'
        b += f'<rect x="{xb - 13}" y="{B_[1] - 8}" width="26" height="18" fill="{GRN}" fill-opacity=".3" stroke="{GRN}" stroke-width="2"/>'
        b += f'<polygon points="{xb - 16},{B_[1] - 8} {xb},{B_[1] - 22} {xb + 16},{B_[1] - 8}" fill="none" stroke="{GRN}" stroke-width="2"/>'
        b += txt(xa - 18, A_[1] + 6, "lều", ORG, 14, "end") + txt(xb + 20, B_[1] + 6, "nhà", GRN, 14)
        b += txt(xa + 6, (A_[1] + bank) / 2 + 5, "30 m", "currentColor", 14, "start", "600")
        b += txt(xb + 6, (B_[1] + bank) / 2 + 5, "50 m", "currentColor", 14, "start", "600")
        b += dimh(xa, xb, bank + 40, "60 m", "currentColor", bank + 34 + 22)
        b += trail([A_, (Mx, bank), B_], TT, .05, .95, RED)
        b += txt(16, 22, "Đi thử: ra bờ sông ở giữa hai chân đường vuông góc", "currentColor", 14)
        b += timed(.96, "đường này đã", 404, 96, RED, 14, "end", "700", None, TT)
        b += timed(.96, "ngắn nhất chưa?", 404, 116, RED, 14, "end", "700", None, TT)
        return fig("c14-6-0", "0 0 420 262", "Bạn đi từ lều ra bờ sông, tới điểm giữa hai chân đường vuông góc, lấy nước rồi về nhà",
                   b, "Mô phỏng một đường đi thử (chưa phải đường ngắn nhất), chạy nhanh hơn thật khoảng 13 lần. " + NOTE)
    # hình dữ kiện: (a) A, B trước gương ; (c) hai gương vuông góc trên hệ trục
    k, ym, x0 = 2.0, 200.0, 40.0
    A_, B_ = (x0, ym - k * D6_a), (x0 + k * D6_s, ym - k * D6_b)
    b += txt(16, 22, "a)", "currentColor", 14)
    b += mirror(10, ym, 210, ym, front=(100, ym - 40)) + txt(206, ym - 6, "G", "currentColor", 14, "end")
    b += dot(*A_, 4.5) + txt(A_[0] - 8, A_[1] - 6, "A", "currentColor", 14, "end")
    b += dot(*B_, 4.5) + txt(B_[0] + 8, B_[1] - 6, "B", "currentColor", 14)
    b += dimv(A_[0], A_[1], ym, "30 cm", "currentColor", A_[0] + 8)
    b += dimv(B_[0], B_[1], ym, "50 cm", "currentColor", B_[0] - 8, "end")
    b += dimh(A_[0], B_[0], ym + 22, "60 cm", "currentColor", ym + 40)
    b += txt(A_[0] - 8, ym - 6, "H_{A}", "currentColor", 14, "end") + txt(B_[0] + 8, ym - 6, "H_{B}", "currentColor", 14)
    b += txt(108, ym - 10, "I = ?", RED, 14, "middle")
    # (c)
    ox, oy, kc = 250.0, 210.0, 2.6
    P_ = lambda p: (ox + kc * p[0], oy - kc * p[1])
    b += txt(226, 22, "c)", "currentColor", 14)
    b += mirror(ox, oy, 410, oy, front=(ox + 50, oy - 50)) + mirror(ox, oy, ox, 46, front=(ox + 50, oy - 50))
    b += txt(406, oy - 8, "G_{1}", "currentColor", 14, "end") + txt(ox + 8, 56, "G_{2}", "currentColor", 14)
    b += txt(ox - 6, oy + 18, "O", "currentColor", 14, "end")
    Ap, Bp = P_(D6_A), P_(D6_B)
    b += dot(*Ap, 4.5) + txt(Ap[0] + 6, Ap[1] - 8, "A(40;20)", "currentColor", 14)
    b += dot(*Bp, 4.5) + txt(Bp[0] + 8, Bp[1] - 6, "B(10;50)", "currentColor", 14)
    b += txt(300, 120, "A → G_{1} → G_{2} → B", ORG, 14)
    return fig("c14-6-2", "0 0 420 250", "a) Hai điểm A, B trước gương, cách gương 30 cm và 50 cm, chân đường vuông góc cách nhau 60 cm; c) hai gương vuông góc G1 trên Ox, G2 trên Oy, điểm A(40;20), B(10;50) cm",
               b, "Dữ kiện câu a và câu c (đơn vị cm). Điểm tới chưa vẽ. " + NOTE)


# ───────────── Dạng 7 · hai gương hợp góc ─────────────
def d7(kk):
    b = ""
    if kk == 0:
        TT = 7.0
        al, i1, ox, oy, r0, kpx = 40.0, D7_i1_c, 30.0, 214.0, 300.0, 1.0
        P_ = lambda p: (ox + kpx * p[0], oy - kpx * p[1])
        pts, inc, vin, vout = trace_wedge(al, i1, r0)
        g = (math.cos(d2r(90 - i1)), math.sin(d2r(90 - i1)))
        start = (r0 + 66 * g[0], 66 * g[1])
        end = (pts[-1][0] + 230 * vout[0] / math.hypot(*vout), pts[-1][1] + 230 * vout[1] / math.hypot(*vout))
        path = [P_(start)] + [P_(p) for p in pts] + [P_(end)]
        b += mirror(ox, oy, 410, oy, front=(ox + 150, oy - 30))
        b += mirror(ox, oy, ox + 270 * math.cos(d2r(al)), oy - 270 * math.sin(d2r(al)), front=(ox + 150, oy - 30))
        b += txt(220, oy - 8, "G_{1}", "currentColor", 14, "middle")
        b += txt(ox + 270 * math.cos(d2r(al)) - 8, oy - 270 * math.sin(d2r(al)) + 4, "G_{2}", "currentColor", 14, "end")
        b += arc(ox, oy, 40, 0, al, BLUE, 1.6) + txt(ox + 46, oy - 10, "40°", BLUE, 14)
        b += txt(ox - 6, oy + 18, "O", "currentColor", 14, "end")
        b += f'<g clip-path="none">{trail(path, TT, .04, .9, ORG)}</g>'
        b += txt(16, 22, "Bắn thử: góc tới đầu 70°, hai gương hợp 40°", "currentColor", 14)
        b += timed(.92, "tia không quay", 404, 56, RED, 14, "end", "700", None, TT)
        b += timed(.92, "ngược đường cũ", 404, 76, RED, 14, "end", "700", None, TT)
        return fig("c14-7-0", "0 0 420 236", "Tia sáng đi vào giữa hai gương hợp góc 40 độ, tới gương G1 với góc tới 70 độ, phản xạ nhiều lần rồi ra ngoài",
                   b, "Mô phỏng: bắn thử với góc giữa hai gương 40° (chưa phải đáp số câu c). Chạy chậm, không theo thời gian thật.")
    # hình dữ kiện: (b) α = 72°, i1 = 25° ; (d) hai gương song song
    ox, oy, al = 20.0, 212.0, D7_al_b
    b += txt(16, 22, "b)", "currentColor", 14)
    g2 = (math.cos(d2r(al)), -math.sin(d2r(al)))
    b += mirror(ox, oy, 214, oy, front=(ox + 100, oy - 30))
    b += mirror(ox, oy, ox + 190 * g2[0], oy + 190 * g2[1], front=(ox + 100, oy - 30))
    b += txt(210, oy - 8, "G_{1}", "currentColor", 14, "end") + txt(ox + 110 * g2[0] + 10, oy + 110 * g2[1], "G_{2}", "currentColor", 14)
    b += arc(ox, oy, 26, 0, al, BLUE, 1.6) + txt(ox + 30, oy - 24, "α = 72°", BLUE, 14)
    Ix = ox + 150
    gam = 90 - D7_i1_b
    S_ = (Ix + 70 * math.cos(d2r(gam)), oy - 70 * math.sin(d2r(gam)))
    b += ray(S_[0], S_[1], Ix, oy, ORG)
    b += seg(Ix, oy, Ix, oy - 80, GREY, 1.4, "5 4")
    b += arc(Ix, oy, 32, gam, 90, RED, 1.6) + txt(Ix + 4, oy - 88, "i_{1} = 25°", RED, 14, "middle")
    # tia phản xạ tới G2 (hướng 180° − γ)
    dvx, dvy = math.cos(d2r(180 - gam)), math.sin(d2r(180 - gam))
    cr = lambda a_, b_: a_[0] * b_[1] - a_[1] * b_[0]
    m = (math.cos(d2r(al)), math.sin(d2r(al)))
    pI = (150.0, 0.0)
    t = -cr(m, pI) / cr(m, (dvx, dvy))
    J = (pI[0] + t * dvx, pI[1] + t * dvy)
    Jx, Jy = ox + J[0], oy - J[1]
    b += ray(Ix, oy, Jx, Jy, ORG)
    nx, ny = math.sin(d2r(al)), math.cos(d2r(al))     # pháp tuyến G2 hướng vào trong góc (màn hình)
    b += seg(Jx, Jy, Jx + 60 * nx, Jy + 60 * ny, GREY, 1.4, "5 4")
    b += txt(Ix, oy + 18, "I", "currentColor", 14, "middle") + txt(Jx - 8, Jy - 4, "J", "currentColor", 14, "end")
    b += txt(Jx + 8, Jy - 10, "i_{2} = ?", RED, 14)
    # (d)
    x1, x2, kd = 256.0, 406.0, 7.5
    b += txt(226, 22, "d)", "currentColor", 14)
    b += mirror(x1, 48, x1, 196, front=(x1 + 50, 120)) + mirror(x2, 48, x2, 196, front=(x2 - 50, 120))
    b += txt(x1 + 6, 64, "G_{1}", "currentColor", 14) + txt(x2 - 6, 64, "G_{2}", "currentColor", 14, "end")
    xs_ = x1 + kd * D7_sx
    b += dot(xs_, 120, 4.5) + txt(xs_ + 8, 116, "S", "currentColor", 14)
    b += dimh(x1, xs_, 150, "6 cm", "currentColor", 170)
    b += dimh(x1, x2, 212, "20 cm", "currentColor", 232)
    return fig("c14-7-2", "0 0 420 240", "b) Hai gương G1, G2 hợp góc 72 độ, tia tới G1 tại I với góc tới 25 độ, phản xạ tới G2 tại J; d) hai gương song song cách 20 cm, điểm S cách G1 6 cm",
               b, "Dữ kiện câu b và câu d. Ảnh và tia ló chưa vẽ. " + NOTE)


BUILD = [d4, d5, d6, d7]

# ═════════════ ĐỀ ═════════════
DANG = [
dict(label="Dạng 4 · Vận dụng · Ảnh khi vật hoặc gương dịch chuyển",
     topic=T_ANH,
     problem_html=r"""<p>Một người đứng trước một gương phẳng lớn treo thẳng đứng, cách mặt gương $3{,}0\ \text{m}$. Coi người như một điểm, gương đủ rộng; mọi chuyển động đều nằm trong mặt phẳng ngang và tính so với mặt đất.</p><ol type="a"><li>Người đi thẳng tới gương (theo phương vuông góc với mặt gương) với tốc độ $1{,}2\ \text{m/s}$. Ảnh của người lại gần người với tốc độ bao nhiêu? Sau $1{,}5\ \text{s}$ người cách ảnh bao xa?</li><li>Người đứng yên ở chỗ cũ, còn gương được kéo ra xa người với tốc độ $0{,}4\ \text{m/s}$ theo phương vuông góc với mặt gương. Tính tốc độ của ảnh và khoảng cách giữa người và ảnh sau $2\ \text{s}$.</li><li>Gương đứng yên. Từ chỗ cũ, người đi với tốc độ $1{,}2\ \text{m/s}$ theo phương hợp với mặt gương góc $60^\circ$, hướng về phía gương. Tìm tốc độ của ảnh, góc giữa vận tốc của người và vận tốc của ảnh, và tốc độ người và ảnh lại gần nhau.</li><li>Người đứng yên cách gương $3{,}0\ \text{m}$. Gọi $H$ là chân đường vuông góc hạ từ người xuống mặt gương. Quay gương một góc $15^\circ$ quanh trục thẳng đứng đi qua $H$. Ảnh của người dời đi một đoạn bao nhiêu (khoảng cách giữa vị trí ảnh trước và sau khi quay)?</li></ol>"""),
dict(label="Dạng 5 · Nâng cao · Vùng nhìn thấy, gương thấy toàn thân",
     topic=T_ANH,
     problem_html=r"""<p>Một người cao $1{,}70\ \text{m}$, mắt ở thấp hơn đỉnh đầu $12\ \text{cm}$, đứng thẳng trước một bức tường thẳng đứng có treo gương phẳng (mặt gương thẳng đứng).</p><ol type="a"><li>Gương phải có chiều cao tối thiểu bao nhiêu, mép dưới và mép trên của gương cách sàn bao nhiêu, để người nhìn thấy toàn bộ ảnh của mình trong gương? Kết quả có phụ thuộc khoảng cách từ người tới gương không?</li><li>Trong nhà chỉ có một gương cao $0{,}60\ \text{m}$, treo với mép dưới cách sàn $0{,}95\ \text{m}$. Người đó nhìn thấy ảnh của phần cơ thể từ độ cao nào tới độ cao nào (so với sàn)?</li><li>Chỉ xét theo phương ngang (nhìn từ trên xuống): một gương phẳng rộng $40\ \text{cm}$ treo trên tường. Mắt người nằm trên đường vuông góc với gương đi qua tâm gương, cách gương $30\ \text{cm}$. Bức tường sau lưng người song song với gương, cách gương $2{,}0\ \text{m}$. Người nhìn thấy trong gương một dải tường sau lưng rộng bao nhiêu? Nếu lùi ra để mắt cách gương $60\ \text{cm}$ thì dải đó rộng bao nhiêu?</li><li>Vẫn gương và tường ở câu c. Mắt cách gương $0{,}5\ \text{m}$ nhưng lệch sang phải so với đường vuông góc qua tâm gương một đoạn $0{,}5\ \text{m}$. Trên tường sau lưng đặt trục $Ox$ nằm ngang, gốc $O$ là chân đường vuông góc hạ từ tâm gương, chiều dương sang phải khi nhìn từ phía người đứng trước gương (cùng phía mắt bị lệch). Có hai điểm $A$ ($x=-1{,}5\ \text{m}$) và $B$ ($x=-3{,}4\ \text{m}$). Mắt nhìn thấy ảnh của điểm nào trong gương? Dải tường thấy được nằm trong khoảng nào?</li></ol>"""),
dict(label="Dạng 6 · Nâng cao · Tia sáng qua điểm cho trước, đường đi ngắn nhất",
     topic=T_ANH,
     problem_html=r"""<ol type="a"><li>Hai điểm $A$, $B$ nằm cùng phía trước một gương phẳng: $A$ cách mặt gương $30\ \text{cm}$, $B$ cách mặt gương $50\ \text{cm}$. Chân các đường vuông góc hạ từ $A$ và $B$ xuống gương là $H_A$, $H_B$, với $H_AH_B = 60\ \text{cm}$. Một tia sáng đi từ $A$, phản xạ tại điểm $I$ trên gương rồi đi qua $B$. Tìm khoảng cách $H_AI$, góc tới tại $I$ và độ dài đường đi $A\to I\to B$. Chứng tỏ đó là đường ngắn nhất đi từ $A$ tới gương rồi tới $B$.</li><li>Một bạn ở lều cách bờ sông thẳng $30\ \text{m}$; nhà cách bờ sông $50\ \text{m}$, cùng phía bờ với lều; chân các đường vuông góc hạ từ lều và từ nhà xuống bờ cách nhau $60\ \text{m}$. Bạn đi từ lều ra bờ sông lấy nước rồi về nhà, luôn đi với tốc độ $1{,}25\ \text{m/s}$. Thời gian đi ngắn nhất là bao nhiêu?</li><li>Hai gương phẳng $G_1$, $G_2$ vuông góc với nhau, mặt phản xạ quay vào nhau, giao tuyến qua $O$. Trong mặt phẳng hình vẽ chọn hệ trục sao cho $G_1$ nằm trên tia $Ox$, $G_2$ nằm trên tia $Oy$ (đơn vị cm). Cho $A(40;20)$, $B(10;50)$. Một tia sáng đi từ $A$, phản xạ trên $G_1$ tại $I$, rồi phản xạ trên $G_2$ tại $J$ rồi đi qua $B$. Tìm toạ độ của $J$, của $I$ và độ dài đường đi $A\to I\to J\to B$. Tia ló $JB$ và tia tới $AI$ có quan hệ gì?</li></ol>"""),
dict(label="Dạng 7 · Vận dụng cao · Mở rộng HSG: Hai gương hợp góc — số ảnh, phản xạ nhiều lần",
     topic=T_ANH,
     problem_html=r"""<p>Hai gương phẳng $G_1$, $G_2$ có mặt phản xạ quay vào nhau, hợp với nhau góc $\alpha$, giao tuyến qua $O$. Coi các gương đủ dài; tia sáng xét trong mặt phẳng vuông góc với giao tuyến và đi vào từ miệng góc.</p><ol type="a"><li>Một điểm sáng $S$ đặt trong góc giữa hai gương. Đếm số ảnh của $S$ khi: $\alpha=72^\circ$ ($S$ nằm trên phân giác; $S$ lệch khỏi phân giác); $\alpha=60^\circ$; $\alpha=45^\circ$; $\alpha=100^\circ$ với $S$ nằm trên phân giác (dựng lần lượt các ảnh).</li><li>Cho $\alpha=72^\circ$. Một tia sáng tới $G_1$ với góc tới $i_1=25^\circ$, phản xạ rồi tới $G_2$. Tính góc tới $i_2$ trên $G_2$ và góc hợp bởi hướng truyền của tia ló (sau khi phản xạ trên $G_2$) với hướng truyền của tia tới ban đầu.</li><li>Một tia sáng tới $G_1$ với góc tới $70^\circ$. Tìm $\alpha$ để ở lần phản xạ thứ ba tia sáng tới vuông góc với mặt gương. Khi đó tia sáng phản xạ tất cả bao nhiêu lần trước khi ra khỏi hai gương?</li><li>Thay bằng hai gương phẳng song song, mặt phản xạ quay vào nhau, cách nhau $20\ \text{cm}$; điểm sáng $S$ ở giữa, cách $G_1$ $6\ \text{cm}$. Tính khoảng cách giữa ảnh $S_1$ (của $S$ qua $G_1$) và ảnh $S_2$ (của $S$ qua $G_2$). Ảnh $S_{12}$ (ảnh của $S_1$ qua $G_2$) cách $G_1$ bao nhiêu?</li></ol>"""),
]

# ═════════════ BẢNG PHÂN TÍCH ĐỀ (cột 1 nguyên văn đề ; cột 2 chỉ dữ liệu có trong đề ; cột 3 kiến thức nền + câu hỏi gợi) ═════════════
ANALYSIS = [
 # Dạng 4
 [(r'"cách mặt gương $3{,}0\ \text{m}$"', r"$d=3{,}0\ \text{m}$", r"Ảnh đối xứng với vật qua gương : ảnh cách gương bao xa, cách người bao xa ?"),
  (r'"Coi người như một điểm, gương đủ rộng"', r"người = điểm $P$", r"⚠ điều kiện : gương đủ rộng nên luôn có ảnh ; tại mỗi thời điểm ảnh đối xứng với người qua gương"),
  (r'"Người đi thẳng tới gương (theo phương vuông góc với mặt gương) với tốc độ $1{,}2\ \text{m/s}$"', r"$v=1{,}2\ \text{m/s}$ ; $t=1{,}5\ \text{s}$", r"Trong lúc người đi, ảnh đứng yên hay cũng chuyển động ?"),
  (r'"gương được kéo ra xa người với tốc độ $0{,}4\ \text{m/s}$"', r"$v_G=0{,}4\ \text{m/s}$ ; $t=2\ \text{s}$", r"⚠ người đứng yên nhưng mặt gương dời : viết lại khoảng người – gương và gương – ảnh sau thời gian $t$"),
  (r'"theo phương hợp với mặt gương góc $60^\circ$"', r"góc với mặt gương $60^\circ$", r"⚠ góc đo với mặt gương, không phải với pháp tuyến. Thành phần nào của vận tốc giữ nguyên, thành phần nào đổi chiều qua gương ?"),
  (r'"Quay gương một góc $15^\circ$ quanh trục thẳng đứng đi qua $H$"', r"$\delta=15^\circ$ ; $HP=3{,}0\ \text{m}$", r"$H$ nằm trên gương : khoảng cách từ $H$ tới ảnh có đổi không ?"),
  (r'"Ảnh của người dời đi một đoạn bao nhiêu"', r"độ dời $=?$", r"Hai vị trí ảnh nằm trên đường tròn nào ? Ảnh quay quanh tâm đó một góc bao nhiêu ?")],
 # Dạng 5
 [(r'"Một người cao $1{,}70\ \text{m}$, mắt ở thấp hơn đỉnh đầu $12\ \text{cm}$"', r"$h=1{,}70\ \text{m}$ ; mắt thấp hơn đỉnh $12\ \text{cm}$", r"Mắt cao bao nhiêu so với sàn ?"),
  (r'"đứng thẳng trước một bức tường thẳng đứng có treo gương phẳng (mặt gương thẳng đứng)"', r"người và gương song song", r"⚠ điều kiện : mặt gương cách đều người và ảnh của người ; mắt thấy một điểm khi tia từ điểm đó phản xạ trên gương rồi vào mắt"),
  (r'"để người nhìn thấy toàn bộ ảnh của mình trong gương"', r"thấy ảnh của chân và của đỉnh đầu", r"Tia từ chân, từ đỉnh đầu phải tới gương ở đâu rồi mới vào mắt ?"),
  (r'"Kết quả có phụ thuộc khoảng cách từ người tới gương không?"', r"—", r"Lùi xa thì người và ảnh cùng dời : điểm tới trên gương có đổi độ cao không ?"),
  (r'"gương cao $0{,}60\ \text{m}$, treo với mép dưới cách sàn $0{,}95\ \text{m}$"', r"mép dưới $0{,}95\ \text{m}$ ; mép trên $1{,}55\ \text{m}$", r"Mép gương là điểm tới của tia đi từ điểm nào trên người ?"),
  (r'"Bức tường sau lưng người song song với gương, cách gương $2{,}0\ \text{m}$"', r"tường cách gương $2{,}0\ \text{m}$ ; gương rộng $40\ \text{cm}$ ; mắt cách $30\ \text{cm}$", r"⚠ tường ở cùng phía với mắt : tia từ tường tới gương, phản xạ rồi vào mắt. Ảnh $O'$ của mắt nằm ở đâu ?"),
  (r'"Mắt nhìn thấy ảnh của điểm nào trong gương?"', r"$A$ : $x=-1{,}5\ \text{m}$ ; $B$ : $x=-3{,}4\ \text{m}$", r"Đoạn thẳng nối ảnh của mắt với điểm đó cắt mặt phẳng gương ở trong hay ngoài hai mép ?")],
 # Dạng 6
 [(r'"$A$ cách mặt gương $30\ \text{cm}$, $B$ cách mặt gương $50\ \text{cm}$"', r"$AH_A=30\ \text{cm}$ ; $BH_B=50\ \text{cm}$", r"Ảnh $A'$ của $A$ qua gương ở đâu ?"),
  (r'"$H_AH_B = 60\ \text{cm}$"', r"$H_AH_B=60\ \text{cm}$", r"Đặt toạ độ dọc mặt gương, gốc $H_A$"),
  (r'"Một tia sáng đi từ $A$, phản xạ tại điểm $I$ trên gương rồi đi qua $B$"', r"$I=?$", r"⚠ đường kéo dài của mọi tia phản xạ từ $A$ đi qua ảnh $A'$ ; $I$ phải nằm trên mặt gương thật"),
  (r'"Chứng tỏ đó là đường ngắn nhất"', r"—", r"So sánh $AM+MB$ với $A'B$ cho một điểm $M$ bất kì trên gương"),
  (r'"luôn đi với tốc độ $1{,}25\ \text{m/s}$"', r"$v=1{,}25\ \text{m/s}$ ; $30\ \text{m}$, $50\ \text{m}$, $60\ \text{m}$", r"Bờ sông thẳng đóng vai trò gì ? Hình này giống câu nào đã làm ?"),
  (r'"$G_1$ nằm trên tia $Ox$, $G_2$ nằm trên tia $Oy$"', r"$A(40;20)$ ; $B(10;50)$", r"Lấy đối xứng qua $Ox$, qua $Oy$ thì đổi dấu toạ độ nào ?"),
  (r'"phản xạ trên $G_1$ tại $I$, rồi phản xạ trên $G_2$ tại $J$ rồi đi qua $B$"', r"thứ tự gặp : $G_1$ rồi $G_2$", r"⚠ lấy ảnh theo đúng thứ tự gương tia gặp ; $I$, $J$ tìm được phải nằm trên tia $Ox$, $Oy$")],
 # Dạng 7
 [(r'"Coi các gương đủ dài; tia sáng xét trong mặt phẳng vuông góc với giao tuyến và đi vào từ miệng góc"', r"gương đủ dài", r"⚠ điều kiện : tia tới đi vào từ miệng góc mà không bị gương kia chắn ; mỗi ảnh qua gương này là vật cho gương kia nếu nằm trước gương kia"),
  (r'"Đếm số ảnh của $S$ khi"', r"$\alpha=72^\circ$ ; $60^\circ$ ; $45^\circ$ ; $100^\circ$", r"$360^\circ/\alpha$ có nguyên không, chẵn hay lẻ ? Các ảnh nằm trên đường tròn nào ?"),
  (r'"Cho $\alpha=72^\circ$. Một tia sáng tới $G_1$ với góc tới $i_1=25^\circ$"', r"$\alpha=72^\circ$ ; $i_1=25^\circ$", r"Hai pháp tuyến tại $I$ và $J$ hợp nhau góc bao nhiêu ? Tam giác nào chứa $i_1$, $i_2$ ?"),
  (r'"góc hợp bởi hướng truyền của tia ló (sau khi phản xạ trên $G_2$) với hướng truyền của tia tới ban đầu"', r"góc cần tìm $=?$", r"Mỗi lần phản xạ với góc tới $i$, hướng truyền quay $180^\circ-2i$"),
  (r'"Một tia sáng tới $G_1$ với góc tới $70^\circ$"', r"$i_1=70^\circ$", r"Góc giữa tia và mặt gương lúc đầu bằng bao nhiêu ? Sau mỗi lần phản xạ góc đó đổi thế nào ?"),
  (r'"ở lần phản xạ thứ ba tia sáng tới vuông góc với mặt gương"', r"lần 3 : vuông góc gương", r"⚠ tới vuông góc mặt gương nghĩa là góc tới bằng bao nhiêu ? Sau đó tia đi tiếp thế nào ?"),
  (r'"cách nhau $20\ \text{cm}$; điểm sáng $S$ ở giữa, cách $G_1$ $6\ \text{cm}$"', r"$e=20\ \text{cm}$ ; $SG_1=6\ \text{cm}$", r"Đặt trục vuông góc hai gương, gốc tại $G_1$ : toạ độ của $S$, của ảnh qua mỗi gương ?")],
]

# ═════════════ LỜI GIẢI ═════════════
R4 = [r"<strong>Ảnh qua gương phẳng:</strong> ảnh ảo, bằng vật, đối xứng với vật qua mặt gương.",
      r"<strong>Hệ quả:</strong> vật cách gương $d$ thì vật cách ảnh $2d$ ; mọi điểm trên mặt gương cách đều vật và ảnh.",
      r"<strong>Vận tốc của ảnh:</strong> thành phần dọc mặt gương giữ nguyên, thành phần vuông góc mặt gương đổi chiều.",
      r"<strong>Điều kiện:</strong> gương phẳng đủ rộng ; vận tốc tính so với mặt đất."]
R5 = [r"<strong>Mắt thấy ảnh của $S$</strong> khi tia từ $S$ phản xạ trên gương rồi vào mắt ; đường kéo dài của tia vào mắt đi qua ảnh $S'$.",
      r"<strong>Vùng nhìn thấy:</strong> dựng ảnh $O'$ của mắt ; điểm $S$ thấy được khi đoạn $O'S$ cắt mặt gương trong hai mép.",
      r"<strong>Đường trung bình:</strong> đoạn nối trung điểm hai cạnh tam giác bằng nửa cạnh thứ ba.",
      r"<strong>Điều kiện:</strong> gương phẳng ; người đứng thẳng, song song với gương."]
R6 = [r"<strong>Ảnh:</strong> $A'$ đối xứng $A$ qua gương ; đường kéo dài của mọi tia phản xạ từ $A$ đi qua $A'$.",
      r"<strong>Tia qua $B$:</strong> nối $A'B$ cắt gương tại $I$ ; $AI=A'I$ vì gương là trung trực của $AA'$.",
      r"<strong>Bất đẳng thức tam giác:</strong> $A'M+MB\ge A'B$, dấu bằng khi $M$ nằm trên đoạn $A'B$.",
      r"<strong>Nhiều gương:</strong> mỗi lần phản xạ lấy ảnh thêm một lần, theo đúng thứ tự gương tia gặp.",
      r"<strong>Điều kiện:</strong> điểm tới tìm được phải nằm trên phần gương thật."]
R7 = [r"<strong>Chuỗi ảnh:</strong> ảnh qua gương này là vật cho gương kia nếu nằm trước gương kia ; mọi ảnh nằm trên đường tròn tâm $O$ bán kính $OS$.",
      r"<strong>Đếm ảnh:</strong> $m=360^\circ/\alpha$ nguyên chẵn → $m-1$ ảnh ; nguyên lẻ → $m-1$ (vật trên phân giác) hoặc $m$ (lệch) ; không nguyên → dựng lần lượt.",
      r"<strong>Góc lệch:</strong> mỗi lần phản xạ với góc tới $i$, hướng truyền quay $180^\circ-2i$.",
      r"<strong>Góc với mặt gương:</strong> tia đang đi về phía $O$ thì góc giữa tia và mặt gương tăng thêm $\alpha$ sau mỗi lần phản xạ (góc ngoài tam giác).",
      r"<strong>Điều kiện:</strong> tia vào từ miệng góc không bị gương kia chắn ; gương đủ dài."]

SOLS = [
 sol(R4, [
  ("Ảnh lại gần người nhanh cỡ nào", [P(r"Lúc đầu ảnh ở sau gương $3{,}0\ \text{m}$ nên người cách ảnh :"), M(r"\ell_0=2d=2\cdot3{,}0=6{,}0\ \text{m}"),
     P(r"Người tiến về gương $v$ thì ảnh cũng tiến về gương $v$ (từ phía sau), hai bên cùng rút ngắn khoảng cách :"), M(r"v_{\text{gần}}=2v=2\cdot1{,}2"), A(r"v_{\text{gần}}=2{,}4\ \text{m/s}")]),
  (r"Khoảng cách người – ảnh sau $1{,}5\ \text{s}$", [M(r"\ell=2d-2vt"), M(r"\ell=6{,}0-2{,}4\cdot1{,}5"), A(r"\ell=2{,}4\ \text{m}")]),
  ("Tốc độ của ảnh khi gương lùi", [P(r"Sau thời gian $t$ gương lùi $v_Gt$ : người – gương thành $d+v_Gt$, gương – ảnh cũng $d+v_Gt$. Ảnh cách chỗ người đứng :"),
     M(r"x_{\text{ảnh}}=2(d+v_Gt)=2d+2v_Gt"), P(r"Người đứng yên nên ảnh đi được $2v_Gt$ so với đất :"), M(r"v_{\text{ảnh}}=2v_G=2\cdot0{,}4"), A(r"v_{\text{ảnh}}=0{,}8\ \text{m/s}")]),
  (r"Khoảng cách người – ảnh sau $2\ \text{s}$", [M(r"\ell'=2(d+v_Gt)=2\cdot(3{,}0+0{,}4\cdot2)"), A(r"\ell'=7{,}6\ \text{m}")]),
  ("Người và ảnh lại gần nhau khi đi xiên", [P(r"Tách vận tốc người : dọc mặt gương $v\cos60^\circ=0{,}6\ \text{m/s}$, vuông góc mặt gương $v\sin60^\circ\approx1{,}04\ \text{m/s}$."),
     P(r"Ảnh : thành phần dọc gương giữ nguyên, thành phần vuông góc đổi chiều. Ảnh cũng có tốc độ $1{,}2\ \text{m/s}$ ; hai vận tốc đối xứng qua mặt gương, mỗi cái hợp mặt gương $60^\circ$ về hai phía nên hợp nhau $120^\circ$."),
     P(r"Người và ảnh luôn nằm trên cùng một đường vuông góc với gương, khoảng cách bằng 2 lần khoảng người – gương :"),
     M(r"v_{\text{gần}}=2v\sin60^\circ=2\cdot1{,}2\cdot0{,}866"), A(r"v_{\text{gần}}\approx2{,}08\ \text{m/s}")]),
  ("Ảnh dời khi gương quay", [P(r"$H$ nằm trên gương nên $HP'=HP=3{,}0\ \text{m}$ : ảnh luôn ở trên đường tròn tâm $H$ bán kính $3{,}0\ \text{m}$."),
     P(r"Mặt gương là phân giác của góc $PHP'$. Lúc đầu $HP$ vuông góc gương, $\widehat{PHP'}=180^\circ$. Quay gương $15^\circ$ thì góc giữa $HP$ và gương còn $75^\circ$, nên $\widehat{PHP'}=150^\circ$ : ảnh quay quanh $H$ một góc"),
     M(r"\varphi=2\delta=30^\circ"), M(r"s=2R\sin\dfrac{\varphi}{2}=2\cdot3{,}0\cdot\sin15^\circ"), A(r"s\approx1{,}55\ \text{m}")]),
  ("Kiểm tra", [P(r"Câu a : sau $1{,}5\ \text{s}$ người cách gương $3{,}0-1{,}8=1{,}2\ \text{m}$, ảnh cũng cách gương $1{,}2\ \text{m}$ : tổng $2{,}4\ \text{m}$ ✓."),
     P(r"Câu c : đi vuông góc gương ($90^\circ$) thì $2v\sin90^\circ=2{,}4\ \text{m/s}$, trùng câu a ✓ ; đi dọc gương ($0^\circ$) thì không lại gần ✓."),
     P(r"Câu d : cung tròn dài $3{,}0\cdot\dfrac{\pi}{6}\approx1{,}57\ \text{m}$, dài hơn dây cung một chút ✓.")])],
  [r"a) ảnh lại gần người $2{,}4\ \text{m/s}$ ; sau $1{,}5\ \text{s}$ người cách ảnh $2{,}4\ \text{m}$",
   r"b) ảnh đi xa $0{,}8\ \text{m/s}$ ; sau $2\ \text{s}$ người cách ảnh $7{,}6\ \text{m}$",
   r"c) ảnh có tốc độ $1{,}2\ \text{m/s}$",
   r"c) hai vận tốc hợp nhau $120^\circ$",
   r"c) người và ảnh lại gần nhau khoảng $2{,}08\ \text{m/s}$",
   r"d) ảnh dời khoảng $1{,}55\ \text{m}$"],
  r"Nhận dạng: thấy <strong>người hoặc gương chuyển động</strong> → vẽ ảnh đối xứng qua gương <strong>tại từng thời điểm</strong>, rồi so khoảng cách hoặc tách vận tốc dọc và vuông góc mặt gương."),
 sol(R5, [
  ("Mép dưới gương", [P(r"Mắt cao $h_m=1{,}70-0{,}12=1{,}58\ \text{m}$. Ảnh $C'$ của chân ở sau gương ; tia từ chân vào mắt có đường kéo dài nối mắt $M$ với $C'$."),
     P(r"Gương cách đều người và ảnh nên đoạn $MC'$ cắt gương tại trung điểm theo phương ngang : điểm tới $Q$ có độ cao bằng trung bình độ cao của $M$ và $C'$ :"),
     M(r"h_Q=\dfrac{h_m+0}{2}=\dfrac{1{,}58}{2}"), A(r"h_Q=0{,}79\ \text{m}")]),
  ("Mép trên và chiều cao tối thiểu", [P(r"Tương tự, tia từ đỉnh đầu $D$ vào mắt cắt gương tại $P$ ở độ cao trung bình của $D$ và $M$ :"),
     M(r"h_P=\dfrac{h_m+h}{2}=\dfrac{1{,}58+1{,}70}{2}=1{,}64\ \text{m}"), M(r"PQ=h_P-h_Q=1{,}64-0{,}79"), A(r"PQ=0{,}85\ \text{m}=\dfrac{h}{2}"),
     P(r"$PQ$ là đường trung bình của tam giác $MC'D'$ ($D'$ là ảnh đỉnh đầu) nên luôn bằng $\dfrac{C'D'}{2}=\dfrac h2$ ; $h_P$, $h_Q$ không chứa khoảng cách người – gương : kết quả không phụ thuộc khoảng cách.")]),
  ("Điểm thấp nhất thấy được", [P(r"Điểm thấp nhất thấy được ở độ cao $y$ cho tia tới đúng mép dưới gương : mép dưới là trung bình độ cao của mắt và điểm đó :"),
     M(r"0{,}95=\dfrac{1{,}58+y}{2}\ \Rightarrow\ y=2\cdot0{,}95-1{,}58"), A(r"y_{\min}=0{,}32\ \text{m}")]),
  ("Điểm cao nhất thấy được", [P(r"Mép trên gương cao $0{,}95+0{,}60=1{,}55\ \text{m}$ :"), M(r"1{,}55=\dfrac{1{,}58+y}{2}\ \Rightarrow\ y=2\cdot1{,}55-1{,}58"), A(r"y_{\max}=1{,}52\ \text{m}"),
     A(r"T:Thấy ảnh phần cơ thể từ độ cao 0,32 m tới 1,52 m : không thấy chân, không thấy đỉnh đầu.")]),
  (r"Dải tường khi mắt cách gương $30\ \text{cm}$", [P(r"Ảnh $O'$ của mắt ở sau gương $0{,}30\ \text{m}$. Nối $O'$ với hai mép gương, kéo tới tường : hai tam giác đồng dạng chung đỉnh $O'$ :"),
     M(r"\dfrac{\ell}{0{,}40}=\dfrac{0{,}30+2{,}0}{0{,}30}"), M(r"\ell=0{,}40\cdot\dfrac{2{,}3}{0{,}3}"), A(r"\ell\approx3{,}07\ \text{m}")]),
  ("Dải tường khi lùi xa", [M(r"\ell'=0{,}40\cdot\dfrac{0{,}60+2{,}0}{0{,}60}"), A(r"\ell'\approx1{,}73\ \text{m}"),
     P(r"Lại gần gương thì thấy dải tường rộng hơn, như nhìn qua khung cửa sổ.")]),
  ("Mắt lệch khỏi trục", [P(r"Đặt toạ độ : trục $x$ dọc gương, gốc ở tâm gương ; mắt $M(0{,}5;\,0{,}5)$, ảnh $O'(0{,}5;\,-0{,}5)$ ; hai mép gương $x=\pm0{,}2$ ; tường ở $y=2{,}0$."),
     P(r"Đoạn $O'A$ cắt mặt gương ($y=0$) tại $x=0{,}5+\dfrac{0{,}5}{2{,}5}\cdot(-1{,}5-0{,}5)=0{,}1$ : nằm trong hai mép → thấy $A$."),
     P(r"Đoạn $O'B$ cắt mặt gương tại $x=0{,}5+0{,}2\cdot(-3{,}4-0{,}5)=-0{,}28$ : ngoài mép trái → không thấy $B$."),
     P(r"Hai mép của dải : đường $O'$ qua $x=\mp0{,}2$ kéo tới tường :"),
     M(r"x=0{,}5+(\mp0{,}2-0{,}5)\cdot\dfrac{2{,}5}{0{,}5}"), A(r"T:Thấy A, không thấy B ; dải thấy được từ x = −3,0 m đến x = −1,0 m.")]),
  ("Kiểm tra", [P(r"Câu a : mép dưới $0{,}79\ \text{m}$ thấp hơn $\dfrac h2=0{,}85\ \text{m}$ đúng $6\ \text{cm}$, bằng nửa khoảng mắt – đỉnh ✓."),
     P(r"Câu c : $O'$ cách tường $2{,}3\ \text{m}$, gấp $7{,}67$ lần $O'$ cách gương nên dải rộng gấp $7{,}67$ lần $0{,}40\ \text{m}$ ✓."),
     P(r"Câu d : dải dài $2{,}0\ \text{m}=0{,}40\cdot\dfrac{2{,}5}{0{,}5}$ ✓ và lệch sang trái vì mắt lệch sang phải ✓.")])],
  [r"a) gương cao tối thiểu $0{,}85\ \text{m}$", r"a) mép dưới cách sàn $0{,}79\ \text{m}$, mép trên $1{,}64\ \text{m}$", r"a) không phụ thuộc khoảng cách người – gương",
   r"b) thấy từ độ cao $0{,}32\ \text{m}$ tới $1{,}52\ \text{m}$", r"c) dải rộng khoảng $3{,}07\ \text{m}$", r"c) lùi ra $60\ \text{cm}$ : khoảng $1{,}73\ \text{m}$",
   r"d) thấy $A$, không thấy $B$", r"d) dải từ $x=-3{,}0\ \text{m}$ đến $x=-1{,}0\ \text{m}$"],
  r"Nhận dạng: thấy <strong>nhìn thấy toàn bộ ảnh</strong> hoặc <strong>vùng nhìn thấy</strong> → dựng <strong>ảnh của mắt</strong>, nối tới hai mép gương ; điểm tới là trung điểm theo phương ngang."),
 sol(R6, [
  ("Điểm tới $I$", [P(r"Ảnh $A'$ ở sau gương $30\ \text{cm}$. Nối $A'B$ cắt gương tại $I$. Hai tam giác vuông $A'H_AI$ và $BH_BI$ đồng dạng :"),
     M(r"\dfrac{H_AI}{H_BI}=\dfrac{A'H_A}{BH_B}=\dfrac{30}{50}"), M(r"H_AI=60\cdot\dfrac{30}{30+50}"), A(r"H_AI=22{,}5\ \text{cm}")]),
  ("Góc tới tại $I$", [P(r"Pháp tuyến tại $I$ song song với $AH_A$ nên góc tới là góc giữa $IA$ và $AH_A$ :"), M(r"\tan i=\dfrac{H_AI}{AH_A}=\dfrac{22{,}5}{30}=0{,}75"), A(r"i\approx36{,}9^\circ")]),
  ("Độ dài đường đi ngắn nhất", [P(r"$AI=A'I$ nên $AI+IB=A'I+IB=A'B$. Tam giác vuông có cạnh dọc gương $60\ \text{cm}$, cạnh vuông góc gương $30+50=80\ \text{cm}$ :"),
     M(r"A'B=\sqrt{60^2+80^2}"), A(r"AI+IB=100\ \text{cm}"),
     P(r"Với $M$ bất kì trên gương : $AM+MB=A'M+MB\ge A'B$, dấu bằng khi $M\equiv I$. Thử : $M$ ở trung điểm $H_AH_B$ thì đường dài $100{,}74\ \text{cm}$.")]),
  ("Thời gian ngắn nhất", [P(r"Bờ sông thẳng đóng vai mặt gương, số đo giống câu a (đổi cm thành m) : quãng ngắn nhất $100\ \text{m}$."),
     M(r"t=\dfrac{s}{v}=\dfrac{100}{1{,}25}"), A(r"t_{\min}=80\ \text{s}")]),
  ("Ảnh kép của $A$", [P(r"Tia gặp $G_1$ trước : ảnh của $A$ qua $G_1$ (trục $Ox$) đổi dấu tung độ :"), M(r"A_1(40;-20)"),
     P(r"Tia đi tiếp như phát ra từ $A_1$ tới $G_2$ : ảnh của $A_1$ qua $G_2$ (trục $Oy$) đổi dấu hoành độ :"), M(r"A_{12}(-40;-20)")]),
  ("Điểm tới $J$ trên $G_2$", [P(r"Tia ló cuối cùng đi qua $B$ và có đường kéo dài qua $A_{12}$ : $J$ là giao của $A_{12}B$ với $Oy$ ($x=0$) :"),
     M(r"y_J=-20+\dfrac{0-(-40)}{10-(-40)}\cdot(50-(-20))=-20+0{,}8\cdot70"), A(r"y_J=36{,}0\ \text{cm}")]),
  ("Điểm $I$ và độ dài đường đi", [P(r"$I$ là giao của $A_1J$ với $Ox$ ($y=0$) :"), M(r"x_I=40+\dfrac{20}{56}\cdot(0-40)\approx25{,}7\ \text{cm}"),
     P(r"Mỗi đoạn tia bằng đoạn tương ứng từ ảnh : $AI+IJ+JB=A_1I+IJ+JB=A_{12}J+JB=A_{12}B$ :"),
     M(r"A_{12}B=\sqrt{(10+40)^2+(50+20)^2}=\sqrt{50^2+70^2}"), A(r"AI+IJ+JB\approx86{,}0\ \text{cm}")]),
  ("Kiểm tra", [P(r"$I(25{,}7;0)$ và $J(0;36{,}0)$ có toạ độ dương : nằm trên phần gương thật ✓."),
     P(r"Câu c : hai gương vuông góc, qua hai lần phản xạ thành phần vận tốc theo $Ox$ và theo $Oy$ đều đổi dấu, nên tia ló $JB$ song song và ngược chiều tia tới $AI$ ✓ (nguyên lí gương phản quang)."),
     P(r"Câu a : $\tan i$ tính phía $B$ : $\dfrac{60-22{,}5}{50}=0{,}75$, cùng góc ✓ (góc tới bằng góc phản xạ).")])],
  [r"a) $H_AI=22{,}5\ \text{cm}$", r"a) góc tới $i\approx36{,}9^\circ$", r"a) đường ngắn nhất $100\ \text{cm}$",
   r"b) thời gian ngắn nhất $80\ \text{s}$",
   r"c) $J(0;\,36{,}0)$ ; $I(25{,}7;\,0)$ (cm)", r"c) đường đi dài khoảng $86{,}0\ \text{cm}$", r"c) tia ló $JB$ song song, ngược chiều tia tới $AI$"],
  r"Nhận dạng: thấy <strong>tia đi qua hai điểm cho trước</strong> hoặc <strong>đường ngắn nhất chạm một đường thẳng</strong> → nối <strong>ảnh của điểm đầu</strong> với điểm cuối ; nhiều gương thì lấy ảnh nhiều lần theo thứ tự."),
 sol(R7, [
  (r"Số ảnh khi $360^\circ/\alpha$ nguyên", [P(r"$\alpha=72^\circ$ : $m=5$ lẻ → $S$ trên phân giác có $4$ ảnh (hai ảnh cuối của hai chuỗi trùng nhau) ; $S$ lệch phân giác có $5$ ảnh."),
     P(r"$\alpha=60^\circ$ : $m=6$ chẵn → $5$ ảnh. $\alpha=45^\circ$ : $m=8$ chẵn → $7$ ảnh (với mọi vị trí $S$)."),
     A(r"T:α = 72°, S lệch phân giác : 5 ảnh.")]),
  (r"Số ảnh khi $360^\circ/\alpha$ không nguyên", [P(r"$\alpha=100^\circ$ : $360^\circ/100^\circ=3{,}6$ không nguyên → dựng lần lượt. Đo góc quanh $O$ từ $G_1$ ; $S$ trên phân giác ở góc $50^\circ$ ; vùng sau cả hai gương là từ $180^\circ$ tới $280^\circ$."),
     P(r"Chuỗi qua $G_1$ trước : $S_1$ ở $-50^\circ$ ($310^\circ$), còn trước $G_2$ → $S_{12}$ ở $200^\circ-(-50^\circ)=250^\circ$, đã sau cả hai gương → dừng."),
     P(r"Chuỗi qua $G_2$ trước : $S_2$ ở $200^\circ-50^\circ=150^\circ$, còn trước $G_1$ → $S_{21}$ ở $-150^\circ$ ($210^\circ$), sau cả hai gương → dừng."),
     A(r"T:α = 100°, S trên phân giác : 4 ảnh."),
     P(r"Ghi chú : với $\alpha=100^\circ$, nếu $S$ ở rất gần một gương (góc nhỏ hơn $20^\circ$ tính từ gương đó) thì chỉ còn $3$ ảnh — vì vậy đề phải cho vị trí $S$.")]),
  ("Góc tới $i_2$", [P(r"Pháp tuyến tại $I$ và $J$ cắt nhau tại $K$ ; tứ giác $OIKJ$ có hai góc vuông nên $\widehat{IKJ}=180^\circ-\alpha$. Trong tam giác $IKJ$ :"),
     M(r"i_1+i_2+(180^\circ-\alpha)=180^\circ\ \Rightarrow\ i_1+i_2=\alpha"), M(r"i_2=72^\circ-25^\circ"), A(r"i_2=47^\circ"),
     P(r"Dùng được vì $i_1\lt\alpha$ (tia sau lần 1 còn đi về phía $O$ rồi quay ra). Tia vào được từ miệng góc vì góc giữa tia tới và $G_1$ là $65^\circ\lt72^\circ$.")]),
  ("Góc giữa tia ló và tia tới", [P(r"Hướng truyền quay $180^\circ-2i$ ở mỗi lần phản xạ (cùng chiều quay) :"),
     M(r"D=(180^\circ-2\cdot25^\circ)+(180^\circ-2\cdot47^\circ)=130^\circ+86^\circ=216^\circ"),
     P(r"Góc giữa hai hướng truyền (từ $0^\circ$ tới $180^\circ$) :"), M(r"360^\circ-D=360^\circ-216^\circ"), A(r"144^\circ=2\alpha")]),
  ("Góc giữa hai gương", [P(r"Gọi $\gamma$ là góc giữa tia (đang đi về phía $O$) và mặt gương nó tới. Lần 1 : $\gamma_1=90^\circ-70^\circ=20^\circ$."),
     P(r"Tam giác tạo bởi $O$ và hai điểm tới liên tiếp : góc ngoài bằng tổng hai góc trong không kề, nên $\gamma_2=\gamma_1+\alpha$, $\gamma_3=\gamma_1+2\alpha$."),
     P(r"Lần 3 tới vuông góc mặt gương : $\gamma_3=90^\circ$ (góc tới $0^\circ$) :"), M(r"20^\circ+2\alpha=90^\circ"), A(r"\alpha=35^\circ"),
     P(r"Điều kiện vào được từ miệng góc : $\gamma_1=20^\circ\lt\alpha=35^\circ$ ✓.")]),
  ("Số lần phản xạ", [P(r"Góc tới lần lượt : $70^\circ$ ($G_1$), $35^\circ$ ($G_2$), $0^\circ$ ($G_1$). Tới vuông góc thì tia phản xạ ngược lại đúng đường cũ :"),
     P(r"đường về gặp lại $G_2$ với góc tới $35^\circ$, rồi $G_1$ với góc tới $70^\circ$, rồi ra khỏi miệng góc theo đúng đường tia tới."),
     A(r"T:Tổng cộng 5 lần phản xạ.")]),
  ("Hai ảnh đầu của hai gương song song", [P(r"Trục vuông góc hai gương, gốc tại $G_1$ ; $G_2$ ở $x=20$, $S$ ở $x=6$ (cm)."),
     M(r"S_1:\ x=-6 \qquad S_2:\ x=2\cdot20-6=34"), M(r"S_1S_2=34-(-6)"), A(r"S_1S_2=40\ \text{cm}=2\cdot20\ \text{cm}")]),
  ("Ảnh $S_{12}$", [P(r"$S_1$ ($x=-6$) nằm trước $G_2$, là vật cho $G_2$ :"), M(r"S_{12}:\ x=2\cdot20-(-6)"), A(r"S_{12}\ \text{cách}\ G_1\ 46\ \text{cm}"),
     P(r"Chuỗi tiếp tục mãi ($-46$ ; $86$ ; …) : hai gương song song cho vô số ảnh, ngày càng xa và mờ dần.")]),
  ("Kiểm tra", [P(r"Câu b : $144^\circ=2\alpha$ đúng với quy tắc khi $\alpha\le90^\circ$ ✓ (với $\alpha\gt90^\circ$ góc này là $360^\circ-2\alpha$)."),
     P(r"Câu c : sau lần tới vuông góc, đường về đi ngược đúng đường vào, nên tia ra trùng phương tia tới và ngược chiều ✓ ; điều kiện vào được từ miệng góc $20^\circ\lt35^\circ$ ✓."),
     P(r"Câu d : $S_1S_2=2\cdot20\ \text{cm}$ không phụ thuộc vị trí $S$ giữa hai gương ✓.")])],
  [r"a) $\alpha=72^\circ$ : 4 ảnh ($S$ trên phân giác) hoặc 5 ảnh ($S$ lệch)", r"a) $\alpha=60^\circ$ : 5 ảnh ; $\alpha=45^\circ$ : 7 ảnh", r"a) $\alpha=100^\circ$, $S$ trên phân giác : 4 ảnh",
   r"b) $i_2=47^\circ$", r"b) tia ló hợp tia tới $144^\circ$",
   r"c) $\alpha=35^\circ$ ; 5 lần phản xạ", r"d) $S_1S_2=40\ \text{cm}$ ; $S_{12}$ cách $G_1$ $46\ \text{cm}$"],
  r"Nhận dạng: thấy <strong>hai gương hợp góc</strong> → ảnh trên <strong>đường tròn tâm O</strong>, đếm theo $360^\circ/\alpha$ ; tia phản xạ nhiều lần thì theo dõi <strong>góc với mặt gương tăng α</strong> mỗi lần."),
]

# ═════════════ TỰ GIẢI TỪNG BƯỚC ═════════════
STEPS = [
 # ── Dạng 4 ──
 dict(nhan_dang=r"Thấy <b>người hoặc gương chuyển động</b> → vẽ <b>ảnh đối xứng qua gương</b> tại từng thời điểm",
  cap_do=2, fading="giau_buoc_cuoi", go_roi={"buoc_hay_sai": 2}, buoc=[
  buoc("Ảnh lại gần người nhanh cỡ nào", "Ở câu a, ảnh lại gần người với tốc độ bao nhiêu?", D4_vgan, "m/s", 0.05,
       loi=r"Lấy bằng tốc độ của người : quên rằng ảnh cũng tiến về phía gương cùng lúc với người."),
  buoc(r"Khoảng cách người – ảnh sau $1{,}5\ \text{s}$", "Sau 1,5 s, người cách ảnh bao nhiêu mét?", D4_l1, "m", 0.05,
       loi=r"Trừ quãng người đi vào khoảng cách người – gương rồi coi đó là khoảng cách người – ảnh.",
       ke=[(r"Lúc đầu cách $2d$, mỗi giây giảm $2v$ : $\ell=2d-2vt$", True),
           (r"$\ell=d-vt$", r"Đó là khoảng cách người – gương ; ảnh ở sau gương cùng khoảng ấy nên khoảng người – ảnh phải tính cả hai đoạn."),
           (r"$\ell=2d-vt$", r"Ảnh cũng tiến lại nên khoảng người – ảnh giảm theo cả hai bên, không chỉ theo quãng người đi.")]),
  buoc("Tốc độ của ảnh khi gương lùi", "Ở câu b, ảnh chuyển động với tốc độ bao nhiêu (so với mặt đất)?", D4_vanh, "m/s", 0.02,
       loi=r"Cho ảnh đi cùng tốc độ với gương, hoặc cho ảnh đứng yên vì người đứng yên.",
       ke=[(r"Viết vị trí ảnh theo vị trí gương : gương – ảnh luôn bằng người – gương", True),
           (r"Ảnh đi cùng tốc độ với gương", r"Gương dời thì cả khoảng người – gương lẫn khoảng gương – ảnh cùng thay đổi ; phải tính cả hai."),
           (r"Ảnh đứng yên vì người đứng yên", r"Vị trí ảnh phụ thuộc cả vị trí gương : mặt đối xứng dời thì ảnh dời theo.")]),
  buoc(r"Khoảng cách người – ảnh sau $2\ \text{s}$", "Sau 2 s, người cách ảnh bao nhiêu mét?", D4_l2, "m", 0.05,
       loi=r"Cộng quãng gương lùi vào khoảng cách người – ảnh ban đầu một lần, quên khoảng gương – ảnh cũng tăng theo.",
       ke=[(r"Người – gương sau $2\ \text{s}$ là $d+v_Gt$, rồi nhân đôi", True),
           (r"$2d+v_Gt$", r"Gương lùi thì khoảng gương – ảnh cũng dài thêm ; cộng quãng gương lùi một lần là thiếu."),
           (r"$d+2v_Gt$", r"Lúc đầu ảnh đã cách người $2d$ chứ không phải $d$ ; quãng ảnh đi phải cộng vào $2d$.")]),
  buoc("Người và ảnh lại gần nhau khi đi xiên", "Ở câu c, người và ảnh lại gần nhau với tốc độ bao nhiêu (lấy 2 chữ số sau dấu phẩy)?", D4_vgan_c, "m/s", 0.01,
       loi=r"Dùng $\cos60^\circ$ cho thành phần vuông góc gương : góc $60^\circ$ đo với mặt gương, không phải với pháp tuyến.",
       ke=[(r"Tách vận tốc thành phần dọc gương và vuông góc gương ; chỉ thành phần vuông góc làm khoảng cách thay đổi", True),
           (r"Lấy $2v$ như câu a", r"Người đi xiên nên chỉ một phần vận tốc hướng vào gương ; thành phần dọc gương không làm người và ảnh gần nhau."),
           (r"Bằng $0$ vì ảnh và người có cùng tốc độ", r"Cùng độ lớn nhưng khác hướng ; tốc độ lại gần phụ thuộc hướng của hai vận tốc, không chỉ độ lớn.")]),
  buoc("Ảnh dời khi gương quay", "Ở câu d, ảnh dời đi bao nhiêu mét (lấy 2 chữ số sau dấu phẩy)?", D4_s, "m", 0.01,
       loi=r"Cho ảnh quay quanh $H$ cùng góc với gương, hoặc tính độ dài cung tròn thay cho đoạn thẳng nối hai vị trí ảnh.",
       ke=[(r"Ảnh luôn cách $H$ bằng $HP$ ; tìm góc ảnh quay quanh $H$ rồi tính dây cung", True),
           (r"Ảnh quay quanh $H$ cùng góc gương quay", r"Gương là phân giác của góc $PHP'$ ; người đứng yên nên góc $PHP'$ đổi nhiều hơn góc quay của gương."),
           (r"Ảnh dời bằng độ dài cung tròn ảnh đi qua", r"Đề hỏi khoảng cách giữa hai vị trí ảnh (đoạn thẳng), không phải quãng đường đi trên cung.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 5 ──
 dict(nhan_dang=r"Thấy <b>nhìn thấy toàn bộ ảnh</b> hoặc <b>vùng nhìn thấy</b> → dựng <b>ảnh của mắt</b>, nối tới hai mép gương",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Mép dưới gương", "Mép dưới của gương phải cách sàn bao nhiêu mét?", D5_Q, "m", 0.005,
       loi=r"Lấy mép dưới bằng nửa chiều cao người : tia từ chân phản xạ rồi đi vào mắt, nên phải dùng độ cao của mắt chứ không phải đỉnh đầu."),
  buoc("Mép trên và chiều cao tối thiểu", "Chiều cao tối thiểu của gương là bao nhiêu mét?", D5_PQ, "m", 0.005,
       loi=r"Cho mép trên ngang đỉnh đầu hoặc ngang mắt ; hoặc nghĩ đứng càng xa thì gương cần càng nhỏ.",
       ke=[(r"Tia từ đỉnh đầu vào mắt : mép trên ở độ cao trung bình của đỉnh đầu và mắt ; lấy mép trên trừ mép dưới", True),
           (r"Mép trên ngang đỉnh đầu", r"Tia từ đỉnh đầu đi xuống tới gương rồi lên mắt ; điểm tới nằm giữa đỉnh đầu và mắt, thấp hơn đỉnh đầu."),
           (r"Mép trên ngang mắt", r"Mắt thấp hơn đỉnh đầu nên tia từ đỉnh đầu tới gương ở điểm cao hơn mắt ; gương chỉ tới ngang mắt sẽ mất phần trên của đầu.")]),
  buoc("Điểm thấp nhất thấy được", "Ở câu b, người thấy được ảnh từ độ cao thấp nhất bao nhiêu mét?", D5_ylo, "m", 0.005,
       loi=r"Lấy độ cao mép dưới chia đôi, hoặc cho điểm thấy được ngang mép dưới gương.",
       ke=[(r"Mép dưới gương ở độ cao trung bình của mắt và điểm thấp nhất thấy được", True),
           (r"Điểm thấp nhất ngang mép dưới gương", r"Tia từ điểm thấy được đi chéo tới mép gương rồi lên mắt ; điểm đó không nằm ngang mép gương."),
           (r"Lấy nửa độ cao mép dưới", r"Quy tắc trung điểm ghép mắt với điểm cần tìm ; mắt không ở sát sàn nên không chia đôi độ cao mép gương.")]),
  buoc("Điểm cao nhất thấy được", "Ở câu b, điểm cao nhất mà người thấy được ảnh cách sàn bao nhiêu mét?", D5_yhi, "m", 0.005,
       loi=r"Cho rằng thấy tới đỉnh đầu vì mép trên gương gần ngang mắt, hoặc lấy điểm cao nhất ngang mép trên.",
       ke=[(r"Mép trên gương ở độ cao trung bình của mắt và điểm cao nhất thấy được", True),
           (r"Thấy tới đỉnh đầu", r"Tia từ đỉnh đầu phải tới gương ở điểm giữa đỉnh đầu và mắt ; điểm đó cao hơn mép trên gương nên không có gương ở đó."),
           (r"Điểm cao nhất ngang mép trên gương", r"Điểm thấy được nằm đối xứng với mắt qua độ cao của mép gương, không nằm ngang mép gương.")]),
  buoc(r"Dải tường khi mắt cách gương $30\ \text{cm}$", "Ở câu c, dải tường thấy được rộng bao nhiêu mét (lấy 2 chữ số sau dấu phẩy)?", D5_band, "m", 0.01,
       loi=r"Dùng tỉ số khoảng gương – tường trên khoảng mắt – gương : quên ảnh của mắt ở sau gương, nên khoảng từ ảnh của mắt tới tường phải cộng thêm khoảng mắt – gương.",
       ke=[(r"Dựng ảnh $O'$ của mắt ; nối $O'$ với hai mép gương, kéo tới tường", True),
           (r"Nối mắt với hai mép gương rồi kéo thẳng tới tường", r"Tia vào mắt là tia phản xạ ; vùng thấy được xác định bằng ảnh của mắt sau gương, không phải tia đi thẳng từ mắt."),
           (r"Dải rộng bằng gương vì tường song song gương", r"Các tia từ tường qua hai mép gương tới mắt không song song nhau, nên dải trên tường không bằng bề rộng gương.")]),
  buoc("Dải tường khi lùi xa", "Mắt cách gương 60 cm thì dải tường thấy được rộng bao nhiêu mét (lấy 2 chữ số sau dấu phẩy)?", D5_band2, "m", 0.01,
       loi=r"Cho dải không đổi như chiều cao gương ở câu a, hoặc chia đôi dải cũ vì khoảng mắt – gương tăng gấp đôi.",
       ke=[(r"Giữ cách dựng, thay khoảng mắt – gương mới", True),
           (r"Dải không đổi như chiều cao gương ở câu a", r"Câu a không đổi vì người và ảnh cùng dời ; ở đây tường đứng yên còn mắt dời."),
           (r"Dải giảm một nửa vì khoảng mắt – gương tăng gấp đôi", r"Khoảng từ $O'$ tới tường không tăng gấp đôi, nên dải không giảm đúng một nửa.")]),
  buoc("Mắt lệch khỏi trục", "Ở câu d, mắt nhìn thấy ảnh của điểm nào?",
       loi=r"Nối thẳng mắt với điểm trên tường thay vì nối ảnh của mắt ; hoặc nghĩ mắt lệch phải thì thấy phần tường bên phải.",
       lua_chon=[(r"Chỉ thấy $A$", True),
                 (r"Chỉ thấy $B$", r"Nối $O'$ với $B$ : đoạn thẳng cắt mặt phẳng gương ở ngoài mép trái của gương."),
                 (r"Thấy cả $A$ và $B$", r"Một điểm chỉ thấy được khi đoạn nối nó với $O'$ cắt gương trong hai mép ; kiểm riêng từng điểm."),
                 (r"Không thấy điểm nào", r"Đoạn $O'A$ cắt mặt phẳng gương trong hai mép, nên điểm $A$ thấy được.")],
       ke=[(r"Nối ảnh $O'$ của mắt với từng điểm, xem giao với mặt gương", True),
           (r"Nối mắt với từng điểm, xem đoạn đó có chạm gương không", r"Mắt và tường ở cùng phía gương, đoạn mắt – tường không chạm gương ; phải dùng ảnh $O'$ của mắt."),
           (r"So khoảng cách từ mỗi điểm tới tâm tường với bề rộng gương", r"Vùng thấy được không đối xứng qua tâm khi mắt lệch ; phải dựng tia qua $O'$.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 6 ──
 dict(nhan_dang=r"Thấy <b>tia đi qua hai điểm cho trước</b> hoặc <b>đường ngắn nhất chạm một đường thẳng</b> → nối <b>ảnh của điểm đầu</b> với điểm cuối",
  cap_do=3, fading="giau_tu_buoc_2", go_roi={"buoc_hay_sai": 0}, buoc=[
  buoc("Điểm tới $I$", r"Khoảng cách $H_AI$ bằng bao nhiêu xentimét?", D6_xI, "cm", 0.2,
       loi=r"Lấy $I$ ở trung điểm $H_AH_B$ : chỉ đúng khi $A$ và $B$ cách gương bằng nhau."),
  buoc("Góc tới tại $I$", "Góc tới tại I bằng bao nhiêu độ (lấy 1 chữ số sau dấu phẩy)?", D6_i, "°", 0.1,
       loi=r"Lấy góc giữa tia $AI$ và mặt gương làm góc tới.",
       ke=[(r"$\tan i=\dfrac{H_AI}{AH_A}$ (pháp tuyến tại $I$ song song $AH_A$)", True),
           (r"$\tan i=\dfrac{AH_A}{H_AI}$", r"Đó là tan của góc giữa tia và mặt gương ; góc tới đo với pháp tuyến."),
           (r"$\sin i=\dfrac{H_AI}{AH_A}$", r"Trong tam giác vuông $AH_AI$, $H_AI$ và $AH_A$ là hai cạnh góc vuông nên dùng tan, không phải sin.")]),
  buoc("Độ dài đường đi ngắn nhất", "Đường A → I → B dài bao nhiêu xentimét?", D6_L, "cm", 0.5,
       loi=r"Tính $A'B$ với cạnh vuông góc gương là hiệu hai khoảng cách : $A'$ ở sau gương nên cạnh đó là tổng hai khoảng cách.",
       ke=[(r"$AI+IB=A'I+IB=A'B$, tính $A'B$ bằng định lí Py-ta-go", True),
           (r"Cộng $AH_A+H_AH_B+H_BB$", r"Đó là đường gấp khúc qua hai chân đường vuông góc, không phải đường tia sáng đi."),
           (r"Tính $AB$ bằng định lí Py-ta-go", r"$AB$ là đường thẳng không chạm gương ; tia phải tới gương rồi mới tới $B$.")]),
  buoc("Thời gian ngắn nhất", "Thời gian đi ngắn nhất là bao nhiêu giây?", D6_t, "s", 0.4,
       loi=r"Chọn điểm lấy nước ở giữa hai chân đường vuông góc, hoặc đi vuông góc ra bờ rồi men theo bờ.",
       ke=[(r"Bờ sông đóng vai mặt gương : quãng ngắn nhất tính như câu a, rồi $t=s/v$", True),
           (r"Đi vuông góc ra bờ, men theo bờ, rồi đi vuông góc lên nhà", r"Đường gấp khúc ấy là tổng ba cạnh, dài hơn một đường gãy duy nhất qua bờ."),
           (r"Lấy nước ở giữa hai chân đường vuông góc", r"Trung điểm chỉ là điểm tốt nhất khi lều và nhà cách sông bằng nhau.")]),
  buoc("Ảnh kép của $A$", "Để tia đi A → G₁ → G₂ → B, phải nối B với ảnh nào của A?",
       loi=r"Lấy ảnh một lần, hoặc lấy ảnh qua $G_2$ trước dù tia gặp $G_1$ trước.",
       lua_chon=[(r"$A_{12}$ : ảnh của $A_1$ qua $G_2$, với $A_1$ là ảnh của $A$ qua $G_1$", True),
                 (r"$A_1$ : ảnh của $A$ qua $G_1$", r"Tia còn phản xạ lần nữa trên $G_2$ trước khi tới $B$ ; mỗi lần phản xạ cần lấy ảnh thêm một lần."),
                 (r"Ảnh của $A$ qua $G_2$", r"Tia gặp $G_1$ trước ; ảnh đầu tiên phải lấy qua $G_1$, rồi mới qua $G_2$.")],
       ke=[(r"Lấy ảnh lần lượt theo thứ tự gương tia gặp", True),
           (r"Nối thẳng $A$ với $B$ rồi tìm chỗ cắt gương", r"Đường thẳng $AB$ không chạm gương nào ; tia phải đi qua hai lần phản xạ."),
           (r"Lấy ảnh của $B$ qua $G_1$ rồi nối với $A$", r"$B$ là điểm tia đi tới sau $G_2$ ; nếu lấy ảnh của $B$ thì phải qua $G_2$ trước, không phải $G_1$.")]),
  buoc("Điểm tới $J$ trên $G_2$", "Tung độ của J bằng bao nhiêu xentimét?", D6_J[1], "cm", 0.2,
       loi=r"Nối $B$ với ảnh qua một gương, hoặc nối $A$ với $B$ rồi tìm chỗ cắt $Oy$.",
       ke=[(r"$J$ là giao của đường $A_{12}B$ với $Oy$", True),
           (r"$J$ là giao của đường $A_1B$ với $Oy$", r"Từ $J$ tia ló đi như phát ra từ $A_{12}$ (ảnh sau hai lần phản xạ), không phải từ $A_1$."),
           (r"$J$ là giao của đường $AB$ với $Oy$", r"Đường $AB$ không phải đường tia sáng ; tia đã phản xạ trên $G_1$ trước khi tới $G_2$.")]),
  buoc("Điểm $I$ và độ dài đường đi", "Đường A → I → J → B dài bao nhiêu xentimét (lấy 1 chữ số sau dấu phẩy)?", D6_Lc, "cm", 0.1,
       loi=r"Tính khoảng cách từ $B$ tới ảnh chỉ qua một gương ; hoặc đổi dấu sai toạ độ khi lấy ảnh.",
       ke=[(r"Bằng $A_{12}B$", True),
           (r"Bằng $A_1B$", r"$A_1B$ chỉ thay được hai đoạn đầu khi tia phản xạ một lần ; ở đây có hai lần phản xạ."),
           (r"Bằng $A_2B$ với $A_2$ là ảnh của $A$ qua $G_2$", r"Ảnh qua $G_2$ trước chỉ dùng khi tia gặp $G_2$ trước ; ở đây tia gặp $G_1$ trước.")]),
  buoc("Kiểm tra")]),
 # ── Dạng 7 ──
 dict(nhan_dang=r"Thấy <b>hai gương hợp góc</b> → ảnh trên <b>đường tròn tâm O</b> ; phản xạ nhiều lần thì theo dõi <b>góc với mặt gương</b>",
  cap_do=4, fading="giau_het", go_roi={"buoc_hay_sai": 4}, buoc=[
  buoc(r"Số ảnh khi $360^\circ/\alpha$ nguyên", "Với α = 72° và S lệch khỏi phân giác, có bao nhiêu ảnh?", 5, "ảnh", 0,
       loi=r"Áp một công thức cho mọi trường hợp : với $360^\circ/\alpha$ lẻ, số ảnh còn tuỳ vật nằm trên hay lệch phân giác ; hoặc đếm cả vật."),
  buoc(r"Số ảnh khi $360^\circ/\alpha$ không nguyên", "Với α = 100° và S trên phân giác, có bao nhiêu ảnh?", 4, "ảnh", 0,
       loi=r"Làm tròn $360^\circ/\alpha$ rồi dùng công thức đếm, hoặc dựng tiếp cả ảnh đã nằm sau cả hai gương.",
       ke=[(r"Dựng lần lượt hai chuỗi ảnh (bắt đầu từ $G_1$ và từ $G_2$), dừng khi ảnh nằm sau cả hai gương", True),
           (r"Làm tròn $360^\circ/\alpha$ rồi trừ 1", r"Công thức đếm chỉ dùng khi $360^\circ/\alpha$ nguyên ; ở đây phải dựng từng ảnh."),
           (r"Lấy phần nguyên của $360^\circ/\alpha$ rồi trừ 1", r"Phần nguyên không cho số ảnh : phải xem từng ảnh còn nằm trước gương tiếp theo hay không.")]),
  buoc("Góc tới $i_2$", "Góc tới i₂ trên G₂ bằng bao nhiêu độ?", D7_i2_b, "°", 0.5,
       loi=r"Dùng góc giữa tia và mặt gương thay cho góc tới, hoặc coi góc tới không đổi sau khi phản xạ.",
       ke=[(r"Tam giác tạo bởi hai pháp tuyến và tia $IJ$ : $i_1+i_2=\alpha$ (vì $i_1\lt\alpha$)", True),
           (r"$i_2=i_1$", r"Hai gương không song song, pháp tuyến tại $I$ và $J$ lệch nhau nên góc tới thay đổi."),
           (r"$i_2=\alpha-(90^\circ-i_1)$", r"$90^\circ-i_1$ là góc giữa tia và mặt gương, không phải góc tới ; công thức trong tam giác pháp tuyến dùng góc tới.")]),
  buoc("Góc giữa tia ló và tia tới", "Hướng truyền của tia ló hợp với hướng truyền của tia tới một góc bao nhiêu độ?", D7_goc_b, "°", 0.5,
       loi=r"Lấy góc lệch tổng làm đáp số dù nó lớn hơn $180^\circ$, hoặc lấy thẳng góc giữa hai gương.",
       ke=[(r"Cộng góc lệch $180^\circ-2i$ của từng lần phản xạ, rồi đổi ra góc giữa hai hướng", True),
           (r"Góc giữa tia ló và tia tới bằng $\alpha$", r"Phải cộng hai góc lệch của hai lần phản xạ, không lấy thẳng góc giữa hai gương."),
           (r"Tổng $(180^\circ-2i_1)+(180^\circ-2i_2)$ chính là đáp số", r"Tổng đó lớn hơn $180^\circ$ ; góc giữa hai hướng truyền phải từ $0^\circ$ tới $180^\circ$ nên lấy phần bù tới $360^\circ$.")]),
  buoc("Góc giữa hai gương", "Ở câu c, góc α giữa hai gương bằng bao nhiêu độ?", D7_al_c, "°", 0.5,
       loi=r"Viết góc tới lần thứ ba bằng $90^\circ$ (tới vuông góc mặt gương là góc tới $0^\circ$), hoặc dùng $i_1+i_2=\alpha$ như câu b khi góc tới lớn.",
       ke=[(r"Theo dõi góc giữa tia và mặt gương : mỗi lần phản xạ tăng thêm $\alpha$, lần thứ ba bằng $90^\circ$", True),
           (r"Dùng $i_1+i_2=\alpha$ như câu b", r"Công thức ấy cần $i_1\lt\alpha$ ; với góc tới $70^\circ$ chưa biết điều đó có đúng không, theo dõi góc với mặt gương thì luôn dùng được."),
           (r"Cho góc tới ở lần thứ ba bằng $90^\circ$", r"Tới vuông góc mặt gương nghĩa là tia trùng pháp tuyến, góc tới bằng $0^\circ$.")]),
  buoc("Số lần phản xạ", "Tia sáng phản xạ tất cả bao nhiêu lần trước khi ra khỏi hai gương?", 5, "lần", 0,
       loi=r"Dừng đếm ở lần tới vuông góc, hoặc đếm lần quay đầu hai lần.",
       ke=[(r"Tới vuông góc thì tia quay ngược đường cũ, lặp lại các lần phản xạ theo thứ tự ngược", True),
           (r"Dừng ở lần tới vuông góc", r"Tới vuông góc thì tia phản xạ ngược lại, vẫn còn đi tiếp giữa hai gương."),
           (r"Quay ngược thì lặp lại đủ mọi lần trước, kể cả lần vuông góc", r"Lần phản xạ vuông góc là điểm quay đầu, chỉ tính một lần, không tính lại khi quay về.")]),
  buoc("Hai ảnh đầu của hai gương song song", "Khoảng cách S₁S₂ bằng bao nhiêu xentimét?", D7_S1S2, "cm", 0.2,
       loi=r"Cho $S$ cách $G_2$ cũng $6\ \text{cm}$, hoặc lấy $S_1S_2$ bằng khoảng cách hai gương.",
       ke=[(r"Đặt trục vuông góc hai gương, gốc tại $G_1$ ; ảnh qua mỗi gương đối xứng qua gương đó", True),
           (r"$S_1S_2$ bằng khoảng cách hai gương", r"$S_1$ ở sau $G_1$, $S_2$ ở sau $G_2$ ; cả hai nằm ngoài khoảng giữa hai gương."),
           (r"$S_1S_2=2\cdot6+2\cdot6$", r"$S$ cách $G_2$ không phải $6\ \text{cm}$ mà là phần còn lại của khoảng giữa hai gương.")]),
  buoc("Ảnh $S_{12}$", "Ảnh S₁₂ cách G₁ bao nhiêu xentimét?", D7_S12, "cm", 0.2,
       loi=r"Lấy $S$ làm vật cho $G_2$ (đó là $S_2$), hoặc đối xứng $S_1$ qua $G_1$ lần nữa.",
       ke=[(r"Lấy $S_1$ làm vật cho $G_2$ : khoảng $S_1$ tới $G_2$ rồi đối xứng", True),
           (r"Lấy $S$ làm vật cho $G_2$", r"Đó là ảnh $S_2$ ; ảnh $S_{12}$ là ảnh của ảnh $S_1$."),
           (r"Đối xứng $S_1$ qua $G_1$", r"Đối xứng qua $G_1$ lần nữa thì về lại $S$ ; ảnh tiếp theo của chuỗi phải qua gương kia.")]),
  buoc("Kiểm tra")]),
]


# KaTeX: chỉ số dưới có dấu tiếng Việt → \text{…}
_SUBVN = re.compile(r"_\{([^{}\\]*[^\x00-\x7f][^{}\\]*)\}")
_SUBVN1 = re.compile(r"_([^\x00-\x7f])")
def _tx(x):
    if isinstance(x, str):
        if x.lstrip().startswith("<figure"):
            return x
        x = _SUBVN.sub(lambda m: "_{\\text{" + m.group(1) + "}}", x)
        return _SUBVN1.sub(lambda m: "_{\\text{" + m.group(1) + "}}", x)
    if isinstance(x, list):
        return [_tx(v) for v in x]
    if isinstance(x, tuple):
        return tuple(_tx(v) for v in x)
    if isinstance(x, dict):
        return {k: _tx(v) for k, v in x.items()}
    return x
_RAW_DANG, _RAW_ANALYSIS = DANG, ANALYSIS
DANG, ANALYSIS, SOLS, STEPS = _tx(DANG), _tx(ANALYSIS), _tx(SOLS), _tx(STEPS)


def kiem_so():
    ok = lambda a, b, e=1e-9: abs(a - b) < e
    # ── D4 ──
    assert ok(D4_vgan, 2.4) and ok(D4_l1, 2.4) and ok(D4_vanh, 0.8) and ok(D4_l2, 7.6)
    assert ok(D4_vgan_c, 2.0785, 1e-3) and ok(D4_s, 1.5529, 1e-3) and round(D4_s, 2) == 1.55 and round(D4_vgan_c, 2) == 2.08
    # véc-tơ: ảnh của người (gương là trục Ox): vận tốc ảnh = (vx, −vy); tốc độ 1,2 ; góc 120°
    vel, img = (D4_vx, -D4_vy), (D4_vx, D4_vy)
    assert ok(math.hypot(*img), 1.2) and ok(_ang(vel, img), 120, 1e-6)
    # ảnh khi gương quay: ảnh của P(0, 3) qua đường qua gốc phương 0° và 15°
    def mp(p, deg):
        m = (math.cos(d2r(deg)), math.sin(d2r(deg))); k = p[0] * m[0] + p[1] * m[1]
        return (2 * k * m[0] - p[0], 2 * k * m[1] - p[1])
    assert ok(math.dist(mp((0, 3), 0), mp((0, 3), D4_delta)), D4_s)
    # các cách sai cho kết quả khác đáp số (ngoài sai số)
    assert abs(D4_v - D4_vgan) > 0.05                                                       # bước 1
    assert abs((D4_d - D4_v * D4_t1) - D4_l1) > 0.05 and abs((2 * D4_d - D4_v * D4_t1) - D4_l1) > 0.05   # bước 2
    assert abs(D4_vg - D4_vanh) > 0.02 and D4_vanh > 0.02                                    # bước 3
    assert abs((2 * D4_d + D4_vg * D4_t2) - D4_l2) > 0.05 and abs((D4_d + 2 * D4_vg * D4_t2) - D4_l2) > 0.05   # bước 4
    assert abs(2 * D4_v - D4_vgan_c) > 0.01 and abs(2 * D4_v * math.cos(d2r(D4_beta)) - D4_vgan_c) > 0.01     # bước 5
    assert abs(2 * D4_d * math.sin(d2r(D4_delta) / 2) - D4_s) > 0.01 and abs(D4_d * d2r(D4_phi) - D4_s) > 0.01  # bước 6: góc δ, cung
    # ── D5 ──
    assert ok(D5_hm, 1.58) and ok(D5_Q, 0.79) and ok(D5_P, 1.64) and ok(D5_PQ, 0.85) and ok(D5_PQ, D5_h / 2)
    assert ok(D5_ylo, 0.32) and ok(D5_yhi, 1.52) and D5_yhi < D5_h and D5_ylo > 0
    assert ok(D5_band, 3.0667, 1e-3) and ok(D5_band2, 1.7333, 1e-3)
    assert ok(D5_x1, -3.0) and ok(D5_x2, -1.0)
    assert abs(d5_cut(D5_xA)) <= D5_w / 2 and abs(d5_cut(D5_xB)) > D5_w / 2            # thấy A, không thấy B
    assert abs(D5_h / 2 - D5_Q) > 0.005                                                    # bước 1: mép dưới = h/2 sai
    assert abs((D5_h - D5_Q) - D5_PQ) > 0.005 and abs((D5_hm - D5_Q) - D5_PQ) > 0.005     # bước 2: mép trên ngang đỉnh / ngang mắt
    assert abs(D5_gd - D5_ylo) > 0.005 and abs(D5_gd / 2 - D5_ylo) > 0.005                 # bước 3
    assert abs(D5_gt - D5_yhi) > 0.005 and abs(D5_h - D5_yhi) > 0.005                      # bước 4
    assert abs(D5_w * D5_L / D5_dm - D5_band) > 0.01 and abs(D5_w - D5_band) > 0.01         # bước 5
    assert abs(D5_band / 2 - D5_band2) > 0.01 and abs(D5_band - D5_band2) > 0.01           # bước 6
    # định luật phản xạ trên gương thẳng đứng: tia chân → Q → mắt có độ dâng bằng nhau hai phía
    assert ok(D5_Q - 0, D5_hm - D5_Q) and ok(D5_P - D5_hm, D5_h - D5_P)
    # ── D6 ──
    assert ok(D6_xI, 22.5) and ok(D6_i, 36.8699, 1e-3) and ok(D6_L, 100) and ok(D6_t, 80)
    assert ok(D6_J[1], 36.0) and ok(D6_I[0], 25.714, 1e-3) and ok(D6_Lc, 86.023, 1e-3)
    f = lambda x_: math.hypot(x_, D6_a) + math.hypot(D6_s - x_, D6_b)
    assert all(f(D6_xI) < f(D6_xI + e) for e in (-5, -1, 1, 5)) and ok(f(D6_s / 2), 100.74, 0.01)
    v1 = (D6_I[0] - D6_A[0], D6_I[1] - D6_A[1]); v2 = (D6_J[0] - D6_I[0], D6_J[1] - D6_I[1]); v3 = (D6_B[0] - D6_J[0], D6_B[1] - D6_J[1])
    assert _ang(_refl(v1, 0), v2) < 1e-6 and _ang(_refl(v2, 90), v3) < 1e-6 and ok(_ang(v1, v3), 180, 1e-6)
    assert ok(math.dist(D6_A, D6_I) + math.dist(D6_I, D6_J) + math.dist(D6_J, D6_B), D6_Lc)
    assert abs(D6_s / 2 - D6_xI) > 0.2                                                     # bước 1
    assert abs(r2d(math.atan(D6_a / D6_xI)) - D6_i) > 0.1 and abs(r2d(math.asin(D6_xI / D6_a)) - D6_i) > 0.1   # bước 2
    assert abs(D6_a + D6_s + D6_b - D6_L) > 0.5 and abs(math.hypot(D6_s, D6_b - D6_a) - D6_L) > 0.5            # bước 3
    assert abs((D6_a + D6_s + D6_b) / D6_v - D6_t) > 0.4 and abs(f(D6_s / 2) / D6_v - D6_t) > 0.4              # bước 4
    yJ_A1B = D6_A1[1] + (0 - D6_A1[0]) / (D6_B[0] - D6_A1[0]) * (D6_B[1] - D6_A1[1])
    yJ_AB = D6_A[1] + (0 - D6_A[0]) / (D6_B[0] - D6_A[0]) * (D6_B[1] - D6_A[1])
    assert abs(yJ_A1B - D6_J[1]) > 0.2 and abs(yJ_AB - D6_J[1]) > 0.2                      # bước 6
    assert abs(math.dist(D6_A1, D6_B) - D6_Lc) > 0.1 and abs(math.dist(D6_A2, D6_B) - D6_Lc) > 0.1             # bước 7
    # ── D7 ──
    assert count_images(72, 36) == 4 and count_images(72, 24) == 5 and count_images(72, 10) == 5
    assert all(count_images(60, t) == 5 for t in (6, 20, 30, 50)) and all(count_images(45, t) == 7 for t in (5, 20, 22.5, 40))
    assert count_images(100, 50) == 4 and count_images(100, 10) == 3                        # 100°: phụ thuộc vị trí → đề cho S trên phân giác
    assert round(360 / 100) - 1 != 4 and math.floor(360 / 100) - 1 != 4                     # bước 2: hai cách sai
    pts, inc, vin, vout = trace_wedge(D7_al_b, D7_i1_b)
    assert len(inc) == 2 and ok(inc[1], D7_i2_b, 1e-6) and ok(_ang(vin, vout), D7_goc_b, 1e-6)
    assert ok(D7_D_b, 216) and ok(D7_goc_b, 2 * D7_al_b) and (90 - D7_i1_b) < D7_al_b         # 65° < 72°: không bị G2 chắn
    assert abs(D7_i1_b - D7_i2_b) > 0.5 and abs((D7_al_b - (90 - D7_i1_b)) - D7_i2_b) > 0.5  # bước 3
    assert abs(D7_al_b - D7_goc_b) > 0.5 and abs(D7_D_b - D7_goc_b) > 0.5                     # bước 4
    pts, inc, vin, vout = trace_wedge(D7_al_c, D7_i1_c)
    assert [round(x, 6) for x in inc] == [70, 35, 0, 35, 70] and ok(_ang(vin, vout), 180, 1e-6) and (90 - D7_i1_c) < D7_al_c
    assert ok(D7_al_c, 35)
    assert ok(D7_S1S2, 40) and ok(D7_S12, 46) and abs(D7_e - D7_S1S2) > 0.2 and abs(4 * D7_sx - D7_S1S2) > 0.2 and abs(D7_S2 - D7_S12) > 0.2
    # mô phỏng bắn thử α = 40° không phải đáp số câu c
    pts, inc, vin, vout = trace_wedge(40.0, D7_i1_c)
    assert abs(_ang(vin, vout) - 180) > 5 and all(i > 1 for i in inc)
    # ── bảng phân tích: cột 1 trích nguyên văn đề ──
    for n, rows in enumerate(_RAW_ANALYSIS):
        for r in rows:
            assert r[0].strip('"') in _RAW_DANG[n]["problem_html"], (n, r[0])
    # ── không lộ đáp số trong đề, hình, bảng phân tích, câu hỏi, lựa chọn, lỗi hay gặp ──
    lo = {0: ["2,4", "0,8", "7,6", "2,08", "2,078", "1,55", "1,553", "120", "30°"],
          1: ["0,79", "0,85", "1,64", "0,32", "1,52", "3,07", "1,73", "-3,0", "−3,0", "-1,0", "−1,0"],
          2: ["22,5", "36,9", "36,87", "100", "80 s", "36,0", "25,7", "86,0", "86,02", "-40", "−40"],
          3: ["47", "144", "216", "35", "40 cm", "46", "5 ảnh", "4 ảnh", "5 lần"]}
    for n in range(4):
        figs = re.sub(r"<[^>]+>", " ", BUILD[n](0) + BUILD[n](2))
        figs += " ".join(re.findall(r'aria-label="([^"]*)"', BUILD[n](0) + BUILD[n](2)))
        blob = DANG[n]["problem_html"] + figs + str(ANALYSIS[n]) + STEPS[n]["nhan_dang"]
        for s in STEPS[n]["buoc"]:
            blob += s.get("tieu_de", "") + s.get("hoi", "") + s.get("loi_hay_gap", "")
            for c in s.get("chon_buoc_ke", []) + s.get("lua_chon", []):
                blob += c["text"] + c.get("vi_sao", "")
        for x in lo[n]:
            assert x not in blob, (n, x)
    for n, s in enumerate(STEPS):
        assert len(s["buoc"]) == SOLS[n].count('class="bt-step"'), n
    assert [s["cap_do"] for s in STEPS] == [2, 3, 3, 4]
    # không có ký tự điều khiển (\t do quên r"…")
    for x in (str(DANG), str(ANALYSIS), "".join(SOLS), str(STEPS)):
        assert not re.search(r"[\x00-\x08\x0b-\x1f]", x)
    print("btm158_d456: kiểm số liệu đạt")


if __name__ == "__main__":
    kiem_so()
