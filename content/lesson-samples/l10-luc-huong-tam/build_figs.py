"""Sinh 5 hình SVG cho bài 'Lực hướng tâm và gia tốc hướng tâm' (lesson 77), thay mốc <!--FIGn--> trong
theory.src.html -> theory.html. Chạy: python3 build_figs.py (từ thư mục bài hoặc gốc repo).
Mọi toạ độ tính từ hình học (tâm O, bán kính, góc); in kiểm: nhãn không chồng nhau, không vượt viewBox,
không bị nét đã đăng ký cắt xuyên; mũi tên gia tốc/lực hướng tâm phải chĩa đúng vào tâm."""
import math, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import RED, BLUE, ORG, GRN, wrap  # noqa: E402

COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}
LABELS = []   # (fig, x0, y0, x1, y1, text)
SEGS = []     # (fig, x1, y1, x2, y2, tên) — nét không được cắt xuyên nhãn
CHECKS = []   # lỗi kiểm hình học
CUR = {"fig": 0}
VB = {}


def defs(p):
    out = "<defs>"
    for n, c in COL.items():
        out += (f'<marker id="{p}-{n}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="12" markerHeight="12" '
                f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
    return out + "</defs>"


def arrow(p, c, x1, y1, x2, y2, w=3, name="", dash=""):
    if name:
        SEGS.append((CUR["fig"], x1, y1, x2, y2, name))
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{COL[c]}" stroke-width="{w}"{d} '
            f'marker-end="url(#{p}-{c})"/>')


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, name=""):
    if name:
        SEGS.append((CUR["fig"], x1, y1, x2, y2, name))
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def sub(base, s):
    return f'{base}<tspan baseline-shift="sub" font-size="13">{s}</tspan>'


def text(x, y, s, c="currentColor", size=17, anchor="start", weight="700", italic=False):
    plain = re.sub(r"<[^>]+>", "", s)
    w = 0.58 * size * len(plain)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    LABELS.append((CUR["fig"], x0, y - 0.75 * size, x0 + w, y + 0.25 * size, plain))
    st = ' font-style="italic" font-family="serif"' if italic else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}"{st}>{s}</text>')


def P(O, R, th):
    """Điểm trên đường tròn tâm O bán kính R, góc th (độ, chiều toán học, trục y SVG hướng xuống)."""
    t = math.radians(th)
    return O[0] + R * math.cos(t), O[1] - R * math.sin(t)


def tangent_cw(th):
    """Hướng vận tốc khi chạy theo chiều kim đồng hồ (góc giảm) tại góc th, toạ độ SVG."""
    t = math.radians(th)
    return math.sin(t), math.cos(t)


def arc(O, R, a0, a1, **kw):
    """Cung tròn từ góc a0 tới a1 (độ), vẽ bằng path nhiều đoạn (không phụ thuộc cờ sweep)."""
    n = max(8, int(abs(a1 - a0) / 3))
    pts = [P(O, R, a0 + (a1 - a0) * i / n) for i in range(n + 1)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    c = kw.get("c", "currentColor"); w = kw.get("w", 2); dash = kw.get("dash", ""); op = kw.get("op", 1)
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}"{ds} opacity="{op}"/>'


def points_to(fig, name, x1, y1, x2, y2, O, tol_deg=1.0):
    """Kiểm mũi tên (x1,y1)->(x2,y2) chĩa vào tâm O."""
    ax, ay = x2 - x1, y2 - y1
    bx, by = O[0] - x1, O[1] - y1
    ang = math.degrees(math.acos((ax * bx + ay * by) / (math.hypot(ax, ay) * math.hypot(bx, by))))
    if ang > tol_deg:
        CHECKS.append(f"Hình {fig}: '{name}' lệch {ang:.1f}° so với hướng vào tâm")


def perp_to_radius(fig, name, x1, y1, x2, y2, O, tol_deg=1.0):
    ax, ay = x2 - x1, y2 - y1
    bx, by = O[0] - x1, O[1] - y1
    ang = math.degrees(math.acos(abs(ax * bx + ay * by) / (math.hypot(ax, ay) * math.hypot(bx, by))))
    if abs(ang - 90) > tol_deg:
        CHECKS.append(f"Hình {fig}: '{name}' không vuông góc bán kính ({ang:.1f}°)")


def car(cx, cy, th, L=34, W=18):
    """Xe nhìn từ trên: hình chữ nhật xoay theo tiếp tuyến tại góc th."""
    ux, uy = tangent_cw(th)
    rot = math.degrees(math.atan2(uy, ux))
    return (f'<rect x="{cx - L/2:.1f}" y="{cy - W/2:.1f}" width="{L}" height="{W}" rx="4" '
            f'fill="rgba(56,189,248,.18)" stroke="currentColor" stroke-width="2" '
            f'transform="rotate({rot:.1f} {cx:.1f} {cy:.1f})"/>')


def road(O, r_in, r_out, a0, a1):
    g = arc(O, r_in, a0, a1, w=2.2) + arc(O, r_out, a0, a1, w=2.2)
    g += arc(O, (r_in + r_out) / 2, a0, a1, w=1.4, dash="8 8", op=.55)
    return g


# ---------------- Hình 1: ô tô qua khúc cua (mở bài, chỉ vận tốc) ----------------
CUR["fig"] = 1
VB[1] = (400, 250)
O1 = (200, 238)
b = defs("f1") + road(O1, 150, 190, 162, 18)
b += f'<circle cx="{O1[0]}" cy="{O1[1]}" r="3.5" fill="currentColor"/>' + text(O1[0] + 10, O1[1] + 4, "O", size=17)
for th, lab, dx, dy in ((132, "1", 10, -2), (52, "2", 8, 16)):
    cx, cy = P(O1, 170, th)
    b += line(O1[0], O1[1], cx, cy, "currentColor", 1.2, "4 5", .5)
    b += car(cx, cy, th)
    ux, uy = tangent_cw(th)
    x2, y2 = cx + 62 * ux, cy + 62 * uy
    b += arrow("f1", "b", cx, cy, x2, y2, 3.2, name=f"v{lab}")
    perp_to_radius(1, f"v{lab}", cx, cy, x2, y2, O1)
    b += text(x2 + dx, y2 + dy, sub('<tspan font-style="italic" font-family="serif">v</tspan>', lab), BLUE, 19)
b += text(12, 22, "nhìn từ trên xuống", size=17, weight="600")
b += text(388, 22, "tốc độ: 36 km/h", BLUE, 17, "end", "600")
fig1 = wrap(f"0 0 {VB[1][0]} {VB[1][1]}",
            "Ô tô qua khúc cua tròn tâm O nhìn từ trên xuống; vận tốc ở hai vị trí có cùng độ dài nhưng khác hướng",
            b, "Hình 1. Hai mũi tên vận tốc dài bằng nhau (cùng tốc độ) nhưng chĩa hai hướng khác nhau.")
fig1 = fig1.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-huongtam-01"', 1)

# ---------------- Hình 2: hiệu vận tốc chĩa vào tâm ----------------
CUR["fig"] = 2
VB[2] = (420, 250)
O2, R2 = (112, 222), 132
A1, A2 = 115, 65
b = defs("f2") + arc(O2, R2, 150, 30, w=2)
b += f'<circle cx="{O2[0]}" cy="{O2[1]}" r="3.5" fill="currentColor"/>' + text(O2[0] + 10, O2[1] + 4, "O", size=17)
VL = 56
for th, lab, dx, dy in ((A1, "1", -2, -10), (A2, "2", 8, 6)):
    x, y = P(O2, R2, th)
    b += line(O2[0], O2[1], x, y, "currentColor", 1.2, "4 5", .5)
    b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="currentColor"/>'
    ux, uy = tangent_cw(th)
    b += arrow("f2", "b", x, y, x + VL * ux, y + VL * uy, 3, name=f"v{lab}")
    perp_to_radius(2, f"v{lab}", x, y, x + VL * ux, y + VL * uy, O2)
    b += text(x + VL * ux + dx, y + VL * uy + dy, sub('<tspan font-style="italic" font-family="serif">v</tspan>', lab), BLUE, 19)
# gia tốc ở vị trí giữa (góc 90°), chĩa vào tâm
xm, ym = P(O2, R2, 90)
b += f'<circle cx="{xm:.1f}" cy="{ym:.1f}" r="4" fill="{GRN}"/>'
b += arrow("f2", "g", xm, ym, xm, ym + 52, 3.2, name="a")
points_to(2, "a_ht", xm, ym, xm, ym + 52, O2)
b += text(xm + 9, ym + 46, sub('<tspan font-style="italic" font-family="serif">a</tspan>', "ht"), GRN, 19)
# tam giác vectơ (bên phải): cùng gốc Q
Q, VT = (262, 128), 96
u1, u2 = tangent_cw(A1), tangent_cw(A2)
T1 = (Q[0] + VT * u1[0], Q[1] + VT * u1[1])
T2 = (Q[0] + VT * u2[0], Q[1] + VT * u2[1])
b += f'<circle cx="{Q[0]}" cy="{Q[1]}" r="3" fill="currentColor"/>'
b += arrow("f2", "b", Q[0], Q[1], *T1, 3, name="v1'") + arrow("f2", "b", Q[0], Q[1], *T2, 3, name="v2'")
b += arrow("f2", "g", *T1, *T2, 3.4, name="dv")
dvx, dvy = T2[0] - T1[0], T2[1] - T1[1]
if abs(dvx) > 0.5 or dvy <= 0:   # tâm O nằm phía dưới vị trí giữa -> Δv phải thẳng đứng, chĩa xuống
    CHECKS.append(f"Hình 2: Δv = ({dvx:.1f}, {dvy:.1f}) không chĩa xuống (vào tâm)")
b += text(T1[0] - 50, T1[1] - 6, sub('<tspan font-style="italic" font-family="serif">v</tspan>', "1"), BLUE, 19)
b += text(T2[0] - 50, T2[1] + 22, sub('<tspan font-style="italic" font-family="serif">v</tspan>', "2"), BLUE, 19)
b += text(T1[0] + 10, (T1[1] + T2[1]) / 2 + 5, 'Δ<tspan font-style="italic" font-family="serif">v</tspan>', GRN, 19)
b += text(408, 232, "Δv chĩa vào tâm O", GRN, 17, "end", "600")
fig2 = wrap(f"0 0 {VB[2][0]} {VB[2][1]}",
            "Hai vận tốc v1, v2 ở hai vị trí gần nhau trên đường tròn; vẽ chung gốc thì hiệu Δv chĩa vào tâm O, cùng hướng gia tốc hướng tâm",
            b, "Hình 2. Trái: vận tốc tiếp tuyến ở hai vị trí, gia tốc (xanh lá) ở vị trí giữa chĩa vào O. "
               "Phải: đặt chung gốc, Δ<em>v</em> = <em>v</em><sub>2</sub> − <em>v</em><sub>1</sub> chĩa thẳng vào tâm.")

# ---------------- Hình 3: nút cao su quay trên đầu ống ----------------
CUR["fig"] = 3
VB[3] = (400, 250)
TX, TY, RR, RY = 190, 96, 140, 14      # đỉnh ống, bán kính quỹ đạo (px), bán trục nhỏ elip
SX = TX + RR                           # vị trí nút cao su
b = defs("f3")
b += (f'<ellipse cx="{TX}" cy="{TY}" rx="{RR}" ry="{RY}" fill="none" stroke="currentColor" '
      f'stroke-width="1.4" stroke-dasharray="6 6" opacity=".6"/>')
b += f'<rect x="{TX-6}" y="{TY}" width="12" height="80" rx="2" fill="rgba(148,163,184,.25)" stroke="currentColor" stroke-width="2"/>'
b += line(TX, TY, SX - 9, TY, "currentColor", 1.6)                       # dây ngang tới nút
b += f'<rect x="{SX-9}" y="{TY-9}" width="20" height="18" rx="4" fill="{ORG}" stroke="currentColor" stroke-width="2"/>'
b += line(TX, TY + 80, TX, 204, "currentColor", 1.6)                       # dây dưới ống
b += f'<rect x="{TX-4}" y="186" width="8" height="8" fill="{ORG}"/>'      # kẹp đánh dấu
b += f'<rect x="{TX-15}" y="204" width="30" height="28" rx="3" fill="rgba(148,163,184,.35)" stroke="currentColor" stroke-width="2"/>'
# lực căng dây lên nút: chĩa về trục ống (tâm quỹ đạo)
b += arrow("f3", "r", SX - 12, TY, SX - 70, TY, 3.2)
points_to(3, "lực căng", SX - 12, TY, SX - 70, TY, (TX, TY))
b += text(SX - 46, TY - 26, '<tspan font-style="italic" font-family="serif">T</tspan> = <tspan font-style="italic" font-family="serif">Mg</tspan>', RED, 17, "middle")
# kích thước r
b += line(TX, 42, SX, 42, "currentColor", 1.3) + line(TX, 36, TX, 48, "currentColor", 1.3) + line(SX, 36, SX, 48, "currentColor", 1.3)
b += text((TX + SX) / 2, 32, '<tspan font-style="italic" font-family="serif">r</tspan> = 0,50 m', size=17, anchor="middle")
b += text(SX + 2, 128, "nút cao su", ORG, 17, "middle", "600")
b += text(TX - 14, 150, "ống nhựa", size=17, anchor="end", weight="600")
b += text(TX + 12, 194, "kẹp", ORG, 17, "start", "600")
b += text(TX + 22, 224, 'quả nặng <tspan font-style="italic" font-family="serif">M</tspan>', size=17, weight="600")
fig3 = wrap(f"0 0 {VB[3][0]} {VB[3][1]}",
            "Nút cao su quay tròn nằm ngang bán kính r quanh đầu ống nhựa; dây luồn qua ống treo quả nặng M, lực căng dây bằng Mg kéo nút về tâm",
            b, "Hình 3. Lực căng dây (đỏ) bằng trọng lượng quả nặng <em>Mg</em>, kéo nút cao su về trục ống — đó là lực hướng tâm.")
fig3 = fig3.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-huongtam-03"', 1)

# ---------------- Hình 4: viên bi trong vòng có chỗ hở ----------------
CUR["fig"] = 4
VB[4] = (400, 260)
O4, RW, RB = (160, 150), 88, 80      # tâm, bán kính thành vòng, bán kính đường đi của tâm bi
GAP0, GAP1 = 0, 60                   # chỗ hở từ 0° tới 60°; bi chạy ngược kim đồng hồ (góc tăng)
b = defs("f4") + arc(O4, RW, GAP1, 360, w=4)
b += f'<circle cx="{O4[0]}" cy="{O4[1]}" r="3.5" fill="currentColor"/>' + text(O4[0] - 10, O4[1] + 5, "O", size=17, anchor="end")
# đường bi đã đi (bên trong thành), xanh dương
b += arc(O4, RB, 200, 352, c=BLUE, w=2, dash="5 5", op=.9)
# bi tại điểm rời thành (góc 0°)
BX, BY = P(O4, RB, 0)
b += f'<circle cx="{BX:.1f}" cy="{BY:.1f}" r="7" fill="rgba(56,189,248,.45)" stroke="currentColor" stroke-width="1.8"/>'
# lực của thành lên bi ở góc 315°, chĩa vào tâm
fx, fy = P(O4, RB, 315)
f2x, f2y = fx + 38 * (O4[0] - fx) / RB, fy + 38 * (O4[1] - fy) / RB
b += f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="7" fill="rgba(56,189,248,.45)" stroke="currentColor" stroke-width="1.8"/>'
b += arrow("f4", "r", fx - 6 * (fx - O4[0]) / RB, fy - 6 * (fy - O4[1]) / RB, f2x, f2y, 3, name="F")
points_to(4, "lực của thành", fx, fy, f2x, f2y, O4)
b += text(fx + 30, fy + 26, "lực của thành", RED, 17, "start", "600")
# đường thật: theo tiếp tuyến (góc tăng -> hướng (−sin, −cos) = lên trên tại 0°)
ty_end = 30
b += arrow("f4", "g", BX, BY - 9, BX, ty_end, 3, name="tiep tuyen", dash="7 5")
tx_, ty_ = -math.sin(0), -math.cos(0)
if abs(tx_) > 1e-9 or ty_ >= 0:
    CHECKS.append("Hình 4: đường tiếp tuyến sai hướng")
# kiểm: đường tiếp tuyến đi qua chỗ hở (cắt vòng thành ở góc nằm trong khoảng hở)
cut = math.degrees(math.asin(math.sqrt(RW**2 - RB**2) / RW))
if not (GAP0 < cut < GAP1):
    CHECKS.append(f"Hình 4: đường đi thẳng cắt thành ở {cut:.0f}°, không lọt chỗ hở")
b += text(BX + 10, 44, "✓ đi thẳng", GRN, 17)
b += text(BX + 10, 62, "theo tiếp tuyến", GRN, 17)
# đường sai: theo bán kính
b += arrow("f4", "r", BX + 9, BY, BX + 98, BY, 2.4, name="ban kinh", dash="3 5")
b += text(BX + 12, BY + 26, "✗ không bật ra", RED, 17, weight="600")
b += text(BX + 12, BY + 43, "theo bán kính", RED, 17, weight="600")
b += text(BX + 12, 108, "chỗ hở", size=17, weight="600")
wx, wy = P(O4, RW + 14, 240)
b += text(wx, wy, "thành vòng", size=17, anchor="end", weight="600")
fig4 = wrap(f"0 0 {VB[4][0]} {VB[4][1]}",
            "Viên bi chạy sát thành vòng nhìn từ trên; thành đẩy bi vào tâm; tới chỗ hở bi đi thẳng theo tiếp tuyến chứ không bật ra theo bán kính",
            b, "Hình 4. Còn thành vòng: lực của thành (đỏ) đẩy bi đi vòng. Tới chỗ hở: bi đi thẳng theo tiếp tuyến (xanh lá), không bật ra theo bán kính.")
fig4 = fig4.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-huongtam-04"', 1)

# ---------------- Hình 5: bài toán mẫu — lực lên xe ở khúc cua ----------------
CUR["fig"] = 5
VB[5] = (400, 250)
O5 = (200, 236)
b = defs("f5") + road(O5, 150, 190, 160, 20)
b += f'<circle cx="{O5[0]}" cy="{O5[1]}" r="3.5" fill="currentColor"/>' + text(O5[0] - 10, O5[1] + 4, "O", size=17, anchor="end")
cx, cy = P(O5, 170, 90)
b += line(O5[0], O5[1], cx, cy + 66, "currentColor", 1.2, "4 5", .5)
b += car(cx, cy, 90)
b += arrow("f5", "b", cx + 18, cy, cx + 86, cy, 3.2, name="v")
perp_to_radius(5, "v", cx, cy, cx + 86, cy, O5)
b += text(cx + 98, cy + 6, '<tspan font-style="italic" font-family="serif">v</tspan>', BLUE, 19)
b += arrow("f5", "r", cx, cy + 10, cx, cy + 66, 3.2, name="Fms")
points_to(5, "F_ms", cx, cy + 10, cx, cy + 66, O5)
b += text(cx - 8, cy + 58, sub('<tspan font-style="italic" font-family="serif">F</tspan>', "ms nghỉ"), RED, 18, "end")
b += arrow("f5", "g", cx + 26, cy + 14, cx + 26, cy + 60, 3.2, name="a")
points_to(5, "a_ht", cx + 26, cy + 14, cx + 26, cy + 60, (O5[0] + 26, O5[1]))
b += text(cx + 34, cy + 52, sub('<tspan font-style="italic" font-family="serif">a</tspan>', "ht"), GRN, 19)
b += text(cx + 8, 186, '<tspan font-style="italic" font-family="serif">r</tspan>', size=18)
b += text(12, 22, "nhìn từ trên xuống", size=17, weight="600")
fig5 = wrap(f"0 0 {VB[5][0]} {VB[5][1]}",
            "Ô tô ở giữa khúc cua nhìn từ trên: vận tốc tiếp tuyến, lực ma sát nghỉ và gia tốc hướng tâm cùng chĩa vào tâm O",
            b, "Hình 5. Đường nằm ngang: trọng lực và phản lực (vuông góc mặt đường) triệt tiêu; ma sát nghỉ (đỏ) là lực hướng tâm, cùng hướng gia tốc (xanh lá).")
fig5 = fig5.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-huongtam-01"', 1)


# ---------------- Kiểm toạ độ nhãn ----------------
def seg_hits_box(x1, y1, x2, y2, bx0, by0, bx1, by1):
    for i in range(41):
        t = i / 40
        x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        if bx0 + 1 < x < bx1 - 1 and by0 + 1 < y < by1 - 1:
            return True
    return False


bad = list(CHECKS)
for i, (f, x0, y0, x1, y1, s) in enumerate(LABELS):
    W, H = VB[f]
    if x0 < 2 or y0 < 2 or x1 > W - 2 or y1 > H - 2:
        bad.append(f"Hình {f}: nhãn '{s}' vượt viewBox ({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f})")
    for g, a0, b0, a1, b1, t in LABELS[i + 1:]:
        if g == f and x0 < a1 and a0 < x1 and y0 < b1 and b0 < y1:
            bad.append(f"Hình {f}: nhãn '{s}' chồng '{t}'")
    for g, sx1, sy1, sx2, sy2, nm in SEGS:
        if g == f and seg_hits_box(sx1, sy1, sx2, sy2, x0, y0, x1, y1):
            bad.append(f"Hình {f}: nét '{nm}' cắt nhãn '{s}'")
print("\n".join(bad) if bad else "kiểm toạ độ: ok")

src = (HERE / "theory.src.html").read_text(encoding="utf8")
figs = (fig1, fig2, fig3, fig4, fig5)
order = [int(n) for n in re.findall(r"<!--FIG(\d)-->", src)]
assert order == list(range(1, len(figs) + 1)), order
for n, f in enumerate(figs, 1):
    assert f"<figcaption>Hình {n}." in f, n
    src = src.replace(f"<!--FIG{n}-->", f)

lint = HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = HERE / "theory.html"
out.write_text(src.replace("__PHUT__", "?"), encoding="utf8")
r = subprocess.run([sys.executable, str(lint), str(out), "--json"], capture_output=True, text=True)
m = re.search(r'"phut"\s*:\s*([\d.]+)', r.stdout)
phut = int(float(m.group(1)) + 0.5) if m else "?"
out.write_text(src.replace("__PHUT__", str(phut)), encoding="utf8")
print("ok", len(src), "ký tự; phút =", phut)
