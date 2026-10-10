"""Hình cho bài tập mẫu Bài 5 (Thuyết động học phân tử chất khí, Vật lí 12), lesson_id 6.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Chuyển động phân tử TÍNH THẬT: mỗi phân tử bay thẳng đều giữa hai va chạm, đổi hướng đúng lúc va vào thành (hoặc hạt khói);
SMIL dùng keyTimes ở đúng thời điểm va chạm nên không cắt góc. Không để lộ đáp số."""
import math, os, random, re as _re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *

NOTE = "Hình minh hoạ, không đúng tỉ lệ; số chấm chỉ để minh hoạ."
GREY = "#94a3b8"


# ───────────── tiện ích vẽ ─────────────
def rich(s, size=13):
    """`F_ms` → F với chỉ số dưới ms."""
    parts = _re.split(r"_([A-Za-z0-9]+)", s)
    out = parts[0]
    for i in range(1, len(parts), 2):
        out += f'<tspan dy="4" font-size="{size - 3}">{parts[i]}</tspan>'
        if parts[i + 1]:
            out += f'<tspan dy="-4">{parts[i + 1]}</tspan>'
    return out

def txt(x, y, s, c="currentColor", size=13, anchor="start", weight="700"):
    return lbl(x, y, rich(s, size), c, size, anchor, weight)

def R(x, y, w, h, c="currentColor", sw=2, fill="none", rx=0, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" '
            f'stroke-width="{sw}"{d} opacity="{op}"/>')

def circ(x, y, r, c="currentColor", sw=2, fill="none"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'


# ───────────── mô phỏng: chuyển động theo các điểm gãy (keyTimes) ─────────────
def _fmt(v):
    return f"{v:.1f}"

def path_g(pts, T, inner):
    """Nhóm tịnh tiến theo đường gấp khúc pts=[(t,x,y)…], t từ 0 đến T. Chạy một lần khi bấm, dừng ở khung cuối."""
    kt = ";".join(f"{min(1.0, p[0] / T):.4f}" for p in pts)
    vals = ";".join(f"{_fmt(p[1])} {_fmt(p[2])}" for p in pts)
    return (f'<g transform="translate({_fmt(pts[0][1])} {_fmt(pts[0][2])})"><animateTransform attributeName="transform" type="translate" '
            f'values="{vals}" keyTimes="{kt}" dur="{T:.2f}s" begin="indefinite" fill="freeze"/>{inner}</g>')

def sim_rect(n, box, speed, T, seed, pad=5):
    """n phân tử bay thẳng đều trong hộp chữ nhật, phản xạ đàn hồi ở thành; trả danh sách đường đi."""
    rnd = random.Random(seed); x0, y0, x1, y1 = box
    out = []
    for _ in range(n):
        x = rnd.uniform(x0 + pad, x1 - pad); y = rnd.uniform(y0 + pad, y1 - pad)
        a = rnd.uniform(0, 2 * math.pi); s = speed * rnd.uniform(.6, 1.4)
        vx, vy = s * math.cos(a), s * math.sin(a)
        pts = [(0.0, x, y)]; t = 0.0
        while t < T - 1e-9:
            tx = ((x1 - pad) - x) / vx if vx > 1e-9 else (((x0 + pad) - x) / vx if vx < -1e-9 else 1e9)
            ty = ((y1 - pad) - y) / vy if vy > 1e-9 else (((y0 + pad) - y) / vy if vy < -1e-9 else 1e9)
            dt = min(tx, ty, T - t)
            x += vx * dt; y += vy * dt; t += dt
            pts.append((t, x, y))
            if abs(dt - tx) < 1e-9: vx = -vx
            if abs(dt - ty) < 1e-9: vy = -vy
        out.append(pts)
    return out

def sim_circle(n, c, Rr, speed, T, seed, pad=5):
    """n phân tử trong vùng tròn bán kính Rr tâm c; phản xạ đàn hồi ở mặt tròn."""
    rnd = random.Random(seed); cx, cy = c; Re = Rr - pad
    out = []
    for _ in range(n):
        rr = Re * math.sqrt(rnd.uniform(0, .9)); th = rnd.uniform(0, 2 * math.pi)
        x, y = cx + rr * math.cos(th), cy + rr * math.sin(th)
        a = rnd.uniform(0, 2 * math.pi); s = speed * rnd.uniform(.6, 1.4)
        vx, vy = s * math.cos(a), s * math.sin(a)
        pts = [(0.0, x, y)]; t = 0.0
        while t < T - 1e-9:
            px, py = x - cx, y - cy
            A = vx * vx + vy * vy; B = 2 * (px * vx + py * vy); C = px * px + py * py - Re * Re
            tt = (-B + math.sqrt(max(B * B - 4 * A * C, 0))) / (2 * A)
            dt = min(tt, T - t)
            x += vx * dt; y += vy * dt; t += dt
            pts.append((t, x, y))
            if dt == tt:
                nx, ny = (x - cx) / Re, (y - cy) / Re
                d = vx * nx + vy * ny
                vx, vy = vx - 2 * d * nx, vy - 2 * d * ny
        out.append(pts)
    return out

def sim_brown(box, n, speed, Rb, mu, T, seed, r=3.0, dt=1 / 400):
    """Hạt khói (bán kính Rb, khối lượng gấp mu lần phân tử) bị n phân tử khí va đập đàn hồi. Trả (đường đi hạt khói, các phân tử)."""
    rnd = random.Random(seed); x0, y0, x1, y1 = box
    bx, by = (x0 + x1) / 2, (y0 + y1) / 2; bvx = bvy = 0.0
    mol = []
    while len(mol) < n:
        x = rnd.uniform(x0 + r, x1 - r); y = rnd.uniform(y0 + r, y1 - r)
        if math.hypot(x - bx, y - by) < Rb + r + 6: continue
        a = rnd.uniform(0, 2 * math.pi); s = speed * rnd.uniform(.6, 1.4)
        mol.append([x, y, s * math.cos(a), s * math.sin(a), [(0.0, x, y)]])
    bpts = [(0.0, bx, by)]
    steps = int(T / dt); ncol = 0
    for k in range(1, steps + 1):
        t = k * dt
        bx += bvx * dt; by += bvy * dt
        ev = False
        if bx < x0 + Rb: bx = x0 + Rb; bvx = abs(bvx); ev = True
        if bx > x1 - Rb: bx = x1 - Rb; bvx = -abs(bvx); ev = True
        if by < y0 + Rb: by = y0 + Rb; bvy = abs(bvy); ev = True
        if by > y1 - Rb: by = y1 - Rb; bvy = -abs(bvy); ev = True
        for m in mol:
            m[0] += m[2] * dt; m[1] += m[3] * dt; hit = False
            if m[0] < x0 + r: m[0] = x0 + r; m[2] = abs(m[2]); hit = True
            if m[0] > x1 - r: m[0] = x1 - r; m[2] = -abs(m[2]); hit = True
            if m[1] < y0 + r: m[1] = y0 + r; m[3] = abs(m[3]); hit = True
            if m[1] > y1 - r: m[1] = y1 - r; m[3] = -abs(m[3]); hit = True
            dx, dy = m[0] - bx, m[1] - by; dist = math.hypot(dx, dy)
            if dist < Rb + r:
                nx, ny = dx / dist, dy / dist
                dot = (m[2] - bvx) * nx + (m[3] - bvy) * ny
                if dot < 0:
                    m[2] -= 2 * mu / (1 + mu) * dot * nx; m[3] -= 2 * mu / (1 + mu) * dot * ny
                    bvx += 2 / (1 + mu) * dot * nx; bvy += 2 / (1 + mu) * dot * ny
                    m[0] = bx + nx * (Rb + r); m[1] = by + ny * (Rb + r)
                    hit = True; ev = True; ncol += 1
            if hit: m[4].append((t, m[0], m[1]))
        if ev: bpts.append((t, bx, by))
    bpts.append((T, bx, by))
    for m in mol: m[4].append((T, m[0] + 0.0, m[1] + 0.0))
    # điểm cuối của phân tử: vị trí tại T (đã cập nhật đến bước cuối)
    return bpts, [m[4] for m in mol], ncol


# ───────────── sơ đồ chuỗi (hình dữ kiện) ─────────────
def box_t(x, y, w, h, lines, c="currentColor", size=13):
    b = R(x, y, w, h, c, 2, rx=6)
    n = len(lines)
    for i, s in enumerate(lines):
        yy = y + h / 2 + 5 - (n - 1) * 8 + i * 16
        b += txt(x + w / 2, yy, s, c, size, "middle")
    return b


# ───────────── Dạng 1 · hạt khói trong hộp kín (chuyển động Brown) ─────────────
BOX1 = (30, 34, 390, 186)

def d1(kk):
    p = f"d1{kk}"
    if kk == 0:
        T = 8.0
        bpts, mols, _ = sim_brown(BOX1, 15, 120, 15, 12, T, 11)
        b = defs(p) + R(BOX1[0] - 3, BOX1[1] - 3, BOX1[2] - BOX1[0] + 6, BOX1[3] - BOX1[1] + 6, sw=3)
        for pts in mols:
            b += path_g(pts, T, circ(0, 0, 3, BLUE, 1.2, BLUE))
        b += path_g(bpts, T, circ(0, 0, 15, GRN, 2.4, "none"))
        b += txt(30, 22, "hộp kín", "currentColor", 13) + txt(300, 22, "chùm sáng rọi ngang", ORG, 12, "start", "400")
        b += circ(40, 212, 6, GRN, 2.4) + txt(52, 217, "hạt khói", GRN, 12) + circ(150, 212, 3, BLUE, 1.2, BLUE) + txt(160, 217, "phân tử khí", BLUE, 12)
        return fig("d1-0", "0 0 420 226", "Hạt khói trong hộp kín bị các phân tử khí va đập, đi theo đường gấp khúc", b,
                   "Mô phỏng: hạt khói (phóng to) và phân tử khí bay thẳng, đổi hướng đúng lúc va chạm; chạy chậm hàng tỉ lần. " + NOTE)
    b = defs(p) + R(BOX1[0] - 3, BOX1[1] - 3, BOX1[2] - BOX1[0] + 6, BOX1[3] - BOX1[1] + 6, sw=3)
    b += circ(210, 110, 15, GRN, 2.4)
    spec = [(120, 70, 80, 10), (320, 80, -70, 40), (90, 150, 60, -50), (340, 160, -90, -30), (260, 48, 30, 60), (270, 150, 10, -80)]
    for x, y, vx, vy in spec:
        b += circ(x, y, 3, BLUE, 1.2, BLUE) + vec_luc("b", x, y, vx, vy, math.hypot(vx, vy), 0.5, 2, "", 8)[0]
    b += txt(210, 144, "hạt khói", GRN, 12, "middle") + txt(30, 22, "mũi tên: tốc độ phân tử (dài tỉ lệ với tốc độ)", BLUE, 12, "start", "400")
    b += txt(100, 212, "va đập từ nhiều phía, không bao giờ cân bằng tuyệt đối", "currentColor", 12, "start", "400")
    return fig("d1-2", "0 0 420 226", "Hạt khói bị phân tử khí va đập từ nhiều hướng với tốc độ khác nhau", b,
               "Dữ kiện: hạt khói to, phân tử khí nhỏ và đi theo mọi hướng. " + NOTE)


# ───────────── Dạng 2 · 0,16 kg O₂ → n, N ─────────────
BOX2 = (30, 52, 250, 176)

def d2(kk):
    p = f"d2{kk}"
    if kk == 0:
        T = 8.0
        mols = sim_rect(12, BOX2, 80, T, 21)
        b = defs(p) + R(BOX2[0] - 3, BOX2[1] - 3, BOX2[2] - BOX2[0] + 6, BOX2[3] - BOX2[1] + 6, sw=3)
        for pts in mols:
            b += path_g(pts, T, circ(0, 0, 3.6, BLUE, 1.2, BLUE))
        b += txt(30, 24, "bình kín đựng khí O₂", "currentColor", 13) + txt(30, 42, "m = 0,16 kg", "currentColor", 13)
        b += txt(290, 70, "M = 32 g/mol", "currentColor", 13) + txt(290, 94, "N_A = 6,02·10²³ mol⁻¹", "currentColor", 13, "start", "400")
        b += txt(290, 130, "n = ?", ORG, 14) + txt(290, 154, "N = ?", ORG, 14)
        return fig("d2-0", "0 0 420 196", "Bình kín đựng khí oxygen, các phân tử khí bay thẳng và va vào thành bình", b,
                   "Mô phỏng: phân tử khí bay thẳng đều giữa hai va chạm, phản xạ ở thành bình; chạy chậm hàng tỉ lần. " + NOTE)
    b = defs(p)
    b += box_t(10, 30, 112, 50, ["m = 0,16 kg", "khí O₂"], "currentColor", 13)
    b += box_t(154, 30, 112, 50, ["n = ?"], ORG, 14)
    b += box_t(298, 30, 112, 50, ["N = ?"], ORG, 14)
    b += arrow(p, "b", 122, 55, 154, 55, 2.4) + arrow(p, "b", 266, 55, 298, 55, 2.4)
    b += txt(138, 44, "÷ M", BLUE, 12, "middle") + txt(282, 44, "× N_A", BLUE, 12, "middle")
    b += txt(10, 112, "M = 32 g/mol  (đơn vị gam trên mol)", "currentColor", 13, "start", "400")
    b += txt(10, 136, "N_A = 6,02·10²³ mol⁻¹", "currentColor", 13, "start", "400")
    b += txt(10, 168, "Đơn vị phải khớp: M tính bằng g/mol thì m tính bằng g", ORG, 13)
    return fig("d2-2", "0 0 420 186", "Sơ đồ từ khối lượng khí đến số mol rồi đến số phân tử", b,
               "Dữ kiện: khối lượng đã biết; số mol và số phân tử là hai đại lượng cần tìm, nối bằng M và N_A. " + NOTE)


# ───────────── Dạng 3 · 1,505·10²³ nguyên tử He ở đktc ─────────────
BOX3 = (30, 52, 250, 176)

def d3(kk):
    p = f"d3{kk}"
    if kk == 0:
        T = 8.0
        mols = sim_rect(11, BOX3, 95, T, 33)
        b = defs(p) + R(BOX3[0] - 3, BOX3[1] - 3, BOX3[2] - BOX3[0] + 6, BOX3[3] - BOX3[1] + 6, sw=3)
        for pts in mols:
            b += path_g(pts, T, circ(0, 0, 4, GRN, 1.2, GRN))
        b += txt(30, 24, "bình kín đựng khí He", "currentColor", 13) + txt(30, 42, "0 °C · 1 atm", "currentColor", 13, "start", "400")
        b += txt(290, 66, "N = 1,505·10²³", "currentColor", 13) + txt(290, 84, "nguyên tử He", "currentColor", 12, "start", "400") + txt(290, 108, "M = 4 g/mol", "currentColor", 13, "start", "400")
        b += txt(290, 130, "m = ?", ORG, 14) + txt(290, 154, "V = ?", ORG, 14)
        return fig("d3-0", "0 0 420 196", "Bình kín đựng khí helium ở điều kiện tiêu chuẩn, các nguyên tử bay thẳng và va vào thành bình", b,
                   "Mô phỏng: nguyên tử He bay thẳng đều giữa hai va chạm; chạy chậm hàng tỉ lần. " + NOTE)
    b = defs(p)
    b += box_t(8, 20, 130, 44, ["N = 1,505·10²³", "nguyên tử He"], "currentColor", 12)
    b += box_t(178, 20, 80, 44, ["n = ?"], ORG, 14)
    b += box_t(60, 116, 100, 44, ["m = ?"], ORG, 14)
    b += box_t(280, 116, 100, 44, ["V = ?"], ORG, 14)
    b += arrow(p, "b", 138, 42, 178, 42, 2.4) + txt(158, 33, "÷ N_A", BLUE, 12, "middle")
    b += arrow(p, "b", 200, 64, 130, 116, 2.4) + txt(134, 84, "× M", BLUE, 12, "end")
    b += arrow(p, "b", 238, 64, 306, 116, 2.4) + txt(276, 84, "× 22,4 L/mol", BLUE, 12, "start")
    b += txt(8, 188, "Bình thứ hai (H₂): cùng V, cùng đktc → số mol so với bình He?", ORG, 13)
    return fig("d3-2", "0 0 420 202", "Sơ đồ từ số nguyên tử He đến số mol, khối lượng và thể tích ở điều kiện tiêu chuẩn", b,
               "Dữ kiện: số nguyên tử cho trước; khối lượng và thể tích cần tìm đều đi qua số mol. " + NOTE)


# ───────────── Dạng 4 · giọt nước hình cầu d = 4,0 mm ─────────────
DROP = (130, 100, 66)    # tâm x, y, bán kính

def d4(kk):
    p = f"d4{kk}"
    cx, cy, Rr = DROP
    if kk == 0:
        T = 8.0
        mols = sim_circle(14, (cx, cy), Rr, 55, T, 44)
        b = defs(p) + circ(cx, cy, Rr, "currentColor", 3)
        for pts in mols:
            b += path_g(pts, T, circ(0, 0, 3.6, BLUE, 1.2, BLUE))
        b += dim(p, "o", cx - Rr, cy + Rr + 22, cx + Rr, cy + Rr + 22, "", 0, 0) + txt(cx, cy + Rr + 42, "d = 4,0 mm", ORG, 13, "middle")
        b += txt(250, 56, "giọt nước hình cầu", "currentColor", 13) + txt(250, 80, "ρ = 1,0 g/cm³", "currentColor", 13, "start", "400")
        b += txt(250, 100, "M = 18 g/mol", "currentColor", 13, "start", "400") + txt(250, 124, "N = ?", ORG, 14)
        return fig("d4-0", "0 0 420 214", "Giọt nước hình cầu phóng to, các phân tử nước chuyển động bên trong", b,
                   "Mô phỏng: phân tử nước (phóng to rất nhiều) chuyển động trong giọt; chạy chậm hàng tỉ lần. " + NOTE)
    b = defs(p) + circ(70, 80, 40, "currentColor", 3)
    b += dim(p, "o", 30, 140, 110, 140, "", 0, 0) + txt(70, 160, "d = 4,0 mm", ORG, 13, "middle")
    ys = (8, 64, 120, 176)
    for y, l in zip(ys, ("V = ?", "m = ?", "n = ?", "N = ?")):
        b += box_t(190, y, 100, 32, [l], ORG, 14)
    for y, op in zip(ys[:3], ("× ρ  (1,0 g/cm³)", "÷ M  (18 g/mol)", "× N_A")):
        b += arrow(p, "b", 240, y + 32, 240, y + 56, 2.4) + txt(252, y + 50, op, BLUE, 12)
    b += txt(8, 196, "Hình cầu: V = π·d³/6", "currentColor", 13, "start", "400")
    return fig("d4-2", "0 0 420 226", "Sơ đồ từ đường kính giọt nước đến thể tích, khối lượng, số mol và số phân tử", b,
               "Dữ kiện: chỉ biết đường kính; mỗi đại lượng đi qua đại lượng đứng trước nó. " + NOTE)


# ───────────── Dạng 5 · khoảng cách giữa các phân tử khí ở đktc ─────────────
def d5(kk):
    p = f"d5{kk}"
    if kk == 0:
        T = 5.0; cols, rows, S = 6, 3, 40; ox, oy = 20, 44
        b = defs(p)
        n = cols * rows
        for j in range(rows):
            for i in range(cols):
                idx = j * cols + i; a = 0.04 + 0.86 * idx / n
                x, y = ox + i * S, oy + j * S
                b += (f'<rect x="{x}" y="{y}" width="{S}" height="{S}" fill="{GRN}" fill-opacity="0" stroke="currentColor" stroke-width="1.6">'
                      f'<animate attributeName="fill-opacity" values="0;0;0.3;0.3" keyTimes="0;{a:.3f};{min(a + .04, .99):.3f};1" dur="{T:.2f}s" begin="indefinite" fill="freeze"/></rect>')
                b += circ(x + S / 2, y + S / 2, 5, BLUE, 1.2, BLUE)
        b += txt(20, 24, "khí N₂ ở đktc: mỗi phân tử ở tâm một ô", "currentColor", 13)
        b += txt(20, oy + rows * S + 24, "22,4 L khí ↔ N_A ô (xếp khít)", "currentColor", 13, "start", "400")
        b += txt(282, 74, "d = ?", ORG, 14) + txt(282, 98, "cạnh ô = khoảng cách", ORG, 12, "start", "400") + txt(282, 114, "hai phân tử kề nhau", ORG, 12, "start", "400")
        b += txt(282, 148, "D = 3,0·10⁻¹⁰ m", "currentColor", 13) + txt(282, 166, "đường kính phân tử", "currentColor", 12, "start", "400")
        return fig("d5-0", "0 0 420 212", "Khí nitrogen ở điều kiện tiêu chuẩn: mỗi phân tử nằm ở tâm một hình lập phương nhỏ, các hình xếp khít nhau", b,
                   "Mô phỏng: lần lượt từng ô được tô, mỗi ô chứa một phân tử (mặt cắt phẳng của hình lập phương). " + NOTE)
    S = 120; ox, oy = 30, 24
    b = defs(p) + R(ox, oy, S, S, "currentColor", 2.4) + circ(ox + S / 2, oy + S / 2, 12, BLUE, 1.6, BLUE)
    b += dim(p, "o", ox, oy + S + 20, ox + S, oy + S + 20, "", 0, 0) + txt(ox + S / 2, oy + S + 42, "d = ?", ORG, 14, "middle")
    b += dim(p, "g", ox + S / 2 - 12, oy + S / 2 - 24, ox + S / 2 + 12, oy + S / 2 - 24, "", 0, 0) + txt(ox + S / 2 + 18, oy + S / 2 - 26, "D", GRN, 13)
    b += txt(200, 50, "Một ô = thể tích V₁ cho một phân tử", "currentColor", 13) + txt(200, 78, "V_mol = 22,4 L = N_A ô", "currentColor", 13, "start", "400")
    b += txt(200, 106, "D = 3,0·10⁻¹⁰ m", GRN, 13, "start", "700") + txt(200, 134, "Cần: d và tỉ số d / D", ORG, 13)
    return fig("d5-2", "0 0 420 216", "Một ô vuông là mặt cắt của hình lập phương chứa một phân tử, với cạnh d cần tìm và đường kính phân tử D", b,
               "Dữ kiện: cạnh ô là khoảng cách hai phân tử kề nhau; hình vẽ không đúng tỉ lệ giữa D và d. " + NOTE)


BUILD = [d1, d2, d3, d4, d5]
