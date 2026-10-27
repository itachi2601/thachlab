"""Sinh 4 hình SVG cho bài "Bài 10. Lực từ. Cảm ứng từ" (Vật lí 12) và thay các mốc
<!--FIGn--> trong theory.src.html -> theory.html. Chạy từ thư mục này: python3 build_figs.py

Quy ước màu dùng chung cả bài: đỏ = lực từ F · cam = dòng điện I · xanh dương = cảm ứng từ B
(chỉ dùng chữ và nét bằng currentColor cho vật thể).
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *  # noqa: E402


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def dot(x, y, r=5, c="currentColor"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def rect(x, y, w, h, fill, stroke="currentColor", sw=2, rx=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def vao(x, y, r=14, c=BLUE):
    """Kí hiệu ⊗: vectơ hướng vào trong mặt phẳng hình vẽ."""
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{c}" stroke-width="2.5"/>'
            f'<line x1="{x - r * 0.7:.0f}" y1="{y - r * 0.7:.0f}" x2="{x + r * 0.7:.0f}" y2="{y + r * 0.7:.0f}" stroke="{c}" stroke-width="2.5"/>'
            f'<line x1="{x + r * 0.7:.0f}" y1="{y - r * 0.7:.0f}" x2="{x - r * 0.7:.0f}" y2="{y + r * 0.7:.0f}" stroke="{c}" stroke-width="2.5"/>')


def ellipse(cx, cy, rx, ry, c=BLUE, w=2, fill="none"):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{c}" stroke-width="{w}"/>'


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


# ------------------------------------------------- Hình 1: dây dẫn trong khe nam châm chữ U
b = defs("f1")
b += rect(96, 30, 228, 30, "rgba(148,163,184,.16)", "currentColor", 2, 8)       # cực N
b += rect(96, 190, 228, 30, "rgba(148,163,184,.16)", "currentColor", 2, 8)      # cực S
b += text(210, 52, "N", "currentColor", 16, "middle", "700")
b += text(210, 212, "S", "currentColor", 16, "middle", "700")
b += field_line(150, 68, 150, 184, BLUE, 2.2)                                   # đường sức B
b += field_line(300, 68, 300, 184, BLUE, 2.2)
b += text(160, 88, "B", BLUE, 14, "start", "700")
b += line(30, 120, 390, 120, "currentColor", 3.5)                               # dây dẫn
b += arrow("f1", "o", 58, 120, 108, 120, 3)
b += text(78, 108, "I", ORG, 14, "middle", "700")
b += vao(210, 120, 14, RED)                                                     # lực từ F (vào trong)
b += text(232, 116, "F", RED, 14, "start", "700")
fig1 = wrap("0 0 420 260", "Đoạn dây mang dòng điện đặt giữa hai cực nam châm chữ U, đường sức từ hướng xuống, lực từ hướng vuông góc vào trong mặt phẳng hình vẽ",
            b, "Hình 1. Dây trong khe nam châm: B hướng xuống, F hướng vào mặt phẳng hình vẽ (⊗).")

# ------------------------------------------------- Hình 2: quy tắc bàn tay trái
# Lòng bàn tay hướng về người xem, bốn ngón sang phải, ngón cái thẳng lên (vuông góc 90°).
b = defs("f2")
b += (
    '<path d="M120,278'
    ' C78,276 46,250 46,214 L46,168'
    ' C46,148 78,136 100,128'
    ' C92,80 108,36 132,26'
    ' C156,16 170,40 160,72'
    ' C152,100 158,114 176,118'
    ' L332,118 A16,16 0 0 1 332,150'
    ' L200,150 L176,150 L176,164 L200,164'
    ' L364,164 A16,16 0 0 1 364,196'
    ' L200,196 L176,196 L176,210 L200,210'
    ' L326,210 A15,15 0 0 1 326,240'
    ' L200,240 L176,240 L176,252 L200,252'
    ' L300,252 A13,13 0 0 1 300,278'
    ' L120,278 Z"'
    ' fill="rgba(148,163,184,.16)" stroke="currentColor" stroke-width="2.5"'
    ' stroke-linejoin="round" stroke-linecap="round"/>'
)
b += vao(118, 208, 15, BLUE)                                                    # B xuyên vào lòng bàn tay
b += text(146, 214, "B", BLUE, 16, "start", "700")
b += arrow("f2", "r", 138, 108, 138, 18, 3.2)                                   # F: dọc ngón cái, hướng lên
b += text(196, 40, "F", RED, 16, "start", "700")
b += arrow("f2", "o", 46, 300, 386, 300, 3.2)                                   # I: cổ tay → đầu ngón
b += text(398, 306, "I", ORG, 16, "start", "700")
b += text(216, 324, "cổ tay → ngón tay", ORG, 15, "middle", "600")
fig2 = wrap("0 0 460 340", "Bàn tay trái duỗi thẳng, lòng bàn tay hướng về phía người xem: đường sức từ xuyên vào lòng bàn tay, chiều từ cổ tay đến ngón tay theo dòng điện, ngón cái chỉ chiều lực từ",
            b, "Hình 2. Quy tắc bàn tay trái.")

# ------------------------------------------------- Hình 3: cân dòng điện (bố trí đề 2025 câu II.2)
# Nhìn chính diện: cực N trái, cực S phải, B nằm ngang N → S; dây MN nhìn đầu, dòng M (sau) → N (trước) = ⊙.
# F lên dây hướng lên; phản lực F' dây đẩy nam châm hướng xuống → cân tăng.
b = defs("f3")
b += rect(100, 214, 240, 34, "rgba(148,163,184,.10)", "currentColor", 2, 6)     # cân
b += rect(190, 222, 60, 18, "none", "currentColor", 1.5, 3)
b += text(220, 236, "cân", "currentColor", 12, "middle", "700")
b += rect(130, 178, 180, 34, "rgba(148,163,184,.16)", "currentColor", 2, 6)     # đế nam châm chữ U
b += rect(130, 70, 52, 108, "rgba(148,163,184,.16)", "currentColor", 2, 6)      # cực N
b += rect(258, 70, 52, 108, "rgba(148,163,184,.16)", "currentColor", 2, 6)      # cực S
b += text(156, 128, "N", "currentColor", 18, "middle", "700")
b += text(284, 128, "S", "currentColor", 18, "middle", "700")
b += field_line(186, 88, 254, 88, BLUE, 2.2)                                    # đường sức nét đứt N → S
b += field_line(186, 164, 254, 164, BLUE, 2.2)
b += text(240, 106, "B", BLUE, 14, "middle", "700")
b += f'<circle cx="220" cy="126" r="11" fill="none" stroke="{ORG}" stroke-width="2.5"/>' + dot(220, 126, 3.5, ORG)   # ⊙ dòng ra
b += text(235, 132, "I", ORG, 14, "start", "700")
b += arrow("f3", "r", 220, 112, 220, 40, 3)                                     # F lên dây
b += text(230, 48, "F", RED, 15, "start", "700")
b += arrow("f3", "r", 220, 182, 220, 210, 3)                                    # F' dây đẩy nam châm
b += text(230, 204, "F′", RED, 15, "start", "700")
b += text(20, 30, "dây MN giữ cố định", "currentColor", 12, "start", "600")
b += text(20, 48, "dòng M → N: hướng ra (⊙)", ORG, 12, "start", "600")
fig3 = wrap("0 0 440 260", "Nam châm chữ U đặt trên cân, cực N bên trái, cực S bên phải, đường sức nằm ngang từ N sang S; dây MN giữ cố định nằm ngang trong khe, dòng điện hướng ra phía người xem; lực từ lên dây hướng lên, lực dây đẩy nam châm hướng xuống",
            b, "Hình 3. Cân dòng điện.")

# ------------------------------------------------- Hình 4a/4b/4c: dây thẳng, vòng dây, ống dây
# Vẽ lại theo OpenStax College Physics 2e, Hình 22.37-22.39 (CC BY-NC-SA 4.0). Đường sức của vòng dây và ống dây
# được TÍNH bằng numpy (Biot–Savart cho các vòng dây, tích phân Runge–Kutta theo hướng B) trong mặt phẳng chứa trục,
# rồi chiếu lên hình nhìn xiên. Quy ước che khuất: vật phía trước nét liền đè lên, vật phía sau bị ngắt một khe.
import numpy as np

W, GAP = 4, 14   # bề dày dây
VB4 = "0 0 440 260"
SRC = ('<br><span class="fig-src">Vẽ lại theo OpenStax, College Physics 2e, Hình {h} — CC BY‑NC‑SA 4.0 — '
       'openstax.org/books/college-physics-2e</span>')


def _nguon(vi_tri, kieu, R=1.0, M=120):
    """Các đoạn dòng điện của chuỗi vòng dây bán kính R. kieu='y': trục thẳng đứng (4b), 'x': trục nằm ngang (4c).
    Toạ độ (x phải, y lên, z hướng về phía người xem); chiều dòng chọn để B hướng +y (4b) / +x (4c)."""
    t = (np.arange(M) + 0.5) * 2 * np.pi / M
    dt = 2 * np.pi / M
    mid, dl = [], []
    for p in vi_tri:
        if kieu == "y":
            P = np.stack([R * np.cos(t), np.full(M, p), R * np.sin(t)], 1)
            D = -np.stack([-R * np.sin(t), np.zeros(M), R * np.cos(t)], 1) * dt
        else:
            P = np.stack([np.full(M, p), -R * np.sin(t), R * np.cos(t)], 1)
            D = np.stack([np.zeros(M), -R * np.cos(t), -R * np.sin(t)], 1) * dt
        mid.append(P)
        dl.append(D)
    return np.concatenate(mid), np.concatenate(dl)


def _B(q, mid, dl):
    r = q[None, :] - mid
    d = np.linalg.norm(r, axis=1)[:, None]
    return (np.cross(dl, r) / d ** 3).sum(0)


def _duong_suc(seed, nguon, h=0.03, hop=(14, 14), maxn=9000):
    """Đường sức qua seed=(x,y) trong mặt phẳng z=0: tích phân RK4 theo hướng B tới khi khép kín hoặc ra khỏi `hop`."""
    mid, dl = nguon

    def hd(q, sg):
        b = _B(np.r_[q, 0.0], mid, dl)[:2]
        return sg * b / np.linalg.norm(b)

    def theo(sg):
        p = np.array(seed, float)
        out = [p.copy()]
        for i in range(maxn):
            k1 = hd(p, sg); k2 = hd(p + k1 * h / 2, sg); k3 = hd(p + k2 * h / 2, sg); k4 = hd(p + k3 * h, sg)
            p = p + (k1 + 2 * k2 + 2 * k3 + k4) / 6 * h
            out.append(p.copy())
            if abs(p[0]) > hop[0] or abs(p[1]) > hop[1]:
                break
            if i > 40 and np.linalg.norm(p - out[0]) < h * 1.2:
                out[-1] = out[0].copy()
                return np.array(out), True
        return np.array(out), False
    f, kin = theo(1)
    if kin:
        return f
    b, _ = theo(-1)
    return np.vstack([b[::-1][:-1], f])


def _cach(P, occ, g):
    """True ở các điểm P cách mọi điểm của occ ít nhất g px."""
    if len(occ) == 0:
        return np.ones(len(P), bool)
    d = np.sqrt(((P[:, None, :] - occ[None, :, :]) ** 2).sum(2)).min(1)
    return d > g


def _ve(P, mask, c=BLUE, w=2.0, dash="6 4", chev=(), L=12):
    """Vẽ các đoạn liền mạch của P (mask=True) bằng nét đứt; chev = các điểm mục tiêu (x,y) đặt đầu V gần nhất."""
    s, i, n = "", 0, len(P)
    while i < n:
        if not mask[i]:
            i += 1
            continue
        j = i
        while j < n and mask[j]:
            j += 1
        if j - i >= 4:
            s += pts_path([tuple(p) for p in P[i:j]], c, w, dash)
        i = j
    for tx, ty in chev:
        d = np.hypot(P[:, 0] - tx, P[:, 1] - ty)
        d[~mask] = 1e9
        k = int(d.argmin())
        if d[k] < 30 and 2 <= k < n - 2 and mask[k - 2:k + 3].all():
            dx, dy = P[k + 2] - P[k - 2]
            s += chevron(P[k][0], P[k][1], dx, dy, c, w, L)
    return s


def _khung(P, vb_w, vb_h, m=8):
    return (P[:, 0] > m) & (P[:, 0] < vb_w - m) & (P[:, 1] > m) & (P[:, 1] < vb_h - m)


# 4a) dây thẳng: ba đường sức tròn đồng tâm, cách xa dây dần
b = defs("f4a")
cx, cy, k = 220, 138, 0.30
radii = [48, 96, 146]
wire = np.array([(cx, y) for y in np.arange(18, 248.01, 1.0)])
front = np.vstack([arc_pts(cx, cy, r, r * k, 0, 180, n=160) for r in radii])
wmask = _cach(wire, front, 6.0)
b += _ve(wire, wmask, "currentColor", W, "")
b += chevron(cx, 20, 0, -1, ORG, 3.4, 15)
b += text(cx + 12, 38, "I", ORG, 16, "start", "700")
wire_pts = wire
for r in radii:
    sau = np.array(arc_pts(cx, cy, r, r * k, 180, 360, n=240))
    b += _ve(sau, _cach(sau, wire_pts, 5.0), BLUE, 2.2, "6 4")
    b += pts_path(arc_pts(cx, cy, r, r * k, 0, 180, n=160), BLUE, 2.2, "6 4")
    x, y = ell_pt(cx, cy, r, r * k, 38)
    dx, dy = ell_tan(r, r * k, 38, -1)
    b += chevron(x, y, dx, dy, BLUE, 2.2)
b += text(cx + radii[2] + 6, cy + 4, "B", BLUE, 16, "start", "700")
fig4a = wrap(VB4, "Dây thẳng dài mang dòng điện hướng lên; đường sức từ là ba đường tròn đồng tâm quanh dây, cách xa dây dần, chiều ngược chiều kim đồng hồ nhìn từ trên xuống; nửa phía sau bị dây che, nửa phía trước đi đè lên dây",
             b, "Hình 4a. Dây thẳng: đường sức tròn đồng tâm." + SRC.format(h="22.37"),
             exp="")

# 4b) vòng dây: đường sức tính bằng Biot–Savart, chiếu lên hình nhìn xiên
b = defs("f4b")
cx, cy, s = 220, 130, 68
rx, ry = s, s * 0.36
ng = _nguon([0.0], "y")
dem = lambda p: np.column_stack([cx + s * p[:, 0], cy - s * p[:, 1]])
lines = [dem(_duong_suc((0.0, 0.0), ng, hop=(0.0001, 1.95)))]   # đường sức trên trục
for a in (0.4, 0.6, 0.78):    # 0.4: đường sức lớn hơn, bị khung hình cắt
    for sg in (1, -1):
        lines.append(dem(_duong_suc((sg * a, 0.0), ng, h=0.02, hop=(8, 8))))
front = np.array(arc_pts(cx, cy, rx, ry, 0, 180, n=200))
allL = np.vstack(lines)
b += _ve(lines[0], _khung(lines[0], 440, 260), BLUE, 2.2, "6 4", chev=[(cx, cy - 1.1 * s), (cx, cy + 1.3 * s)])
for P in lines[1:]:
    m = _cach(P, front, 5.5) & _khung(P, 440, 260)
    ytop = P[:, 1].argmin()
    ch = [tuple(P[ytop]), tuple(P[P[:, 1].argmax()])]
    if not _khung(P, 440, 260).all():       # đường lớn bị khung cắt: đầu V ngay phía trên và dưới vòng dây
        ch = []
        for yy in (cy - 1.25 * s, cy + 1.25 * s):
            idx = np.where(m)[0]
            j = idx[np.abs(P[idx, 1] - yy).argmin()]
            ch.append((P[j, 0], P[j, 1]))
    b += _ve(P, m, BLUE, 2.0, "6 4", chev=ch)
sau = np.array(arc_pts(cx, cy, rx, ry, 180, 360, n=200))
b += _ve(sau, _cach(sau, allL, 5.0), "currentColor", W, "")
b += pts_path(front, "currentColor", W)
for t in (100, 280):
    x, y = ell_pt(cx, cy, rx, ry, t)
    dx, dy = ell_tan(rx, ry, t, -1)
    b += chevron(x, y, dx, dy, ORG, 3.2, 12)
b += text(cx + 9, cy + ry + 24, "I", ORG, 16, "start", "700")
b += text(cx + 12, cy - 1.45 * s, "B", BLUE, 16, "start", "700")
fig4b = wrap(VB4, "Vòng dây tròn nhìn xiên với đường sức tính bằng mô hình Biot–Savart: đường sức trên trục thẳng đi qua tâm vuông góc mặt phẳng vòng dây; các đường sức khác là đường kín bao quanh từng đoạn dây, đi lên qua lòng vòng rồi vòng ra ngoài và đi xuống; chỗ vòng dây đi trước thì đường sức bị ngắt, chỗ đường sức đi trước thì vòng dây bị ngắt",
             b, "Hình 4b. Vòng dây: <strong>B</strong> xuyên qua tâm." + SRC.format(h="22.38"))

# 4c) ống dây dài (L = 10R): trong lòng ống các đường sức song song, cách đều; bên ngoài khép kín như nam châm thẳng
b = defs("f4c")
cx, cy, s = 220, 130, 22
rx, ry = 6, s
ng = _nguon(list(np.linspace(-5, 5, 41)), "x")
dem = lambda p: np.column_stack([cx + s * p[:, 0], cy - s * p[:, 1]])
rhos = [-0.85, -0.45, 0.0, 0.45, 0.85]
lines, chevs = [], []
for r_ in rhos:
    P = dem(_duong_suc((0.0, r_), ng, h=0.04, hop=(14, 14), maxn=6000))
    lines.append(P)
xs = [cx + s * (-4.5 + 9 * i / 8) for i in range(9)]       # 9 vòng vẽ (trường tính với 41 vòng sát nhau)
trước = np.vstack([arc_pts(x, cy, rx, ry, -90, 90, n=40) for x in xs])
allL = np.vstack(lines)
for r_, P in zip(rhos, lines):
    m = _cach(P, trước, 4.5) & _khung(P, 440, 260)
    ya = cy - s * r_
    xc = {-0.85: (-2.81, 1.69), -0.45: (-1.69, 2.81), 0.0: (-0.56, 3.94), 0.45: (-3.94, 0.56), 0.85: (-2.81, 1.69)}[r_]
    ch = [(cx + s * u, ya) for u in xc]
    if abs(r_) > 0.8:      # hai đường sát vách: thêm đầu V ở đỉnh vòng ngoài
        ch += [(cx, P[:, 1].min() if r_ > 0 else P[:, 1].max())]
    else:                  # các đường gần trục toả ra hai đầu: thêm đầu V ngoài ống
        ch += [(cx - 5.2 * s - 26, ya), (cx + 5.2 * s + 26, ya)]
    b += _ve(P, m, BLUE, 2.0, "6 4", chev=ch)
for x in xs:
    sau = np.array(arc_pts(x, cy, rx, ry, 90, 270, n=40))
    b += _ve(sau, _cach(sau, allL, 4.5), "currentColor", W, "")
    b += pts_path(arc_pts(x, cy, rx, ry, -90, 90, n=40), "currentColor", W)
for x in (xs[2], xs[6]):
    px, py = ell_pt(x, cy, rx, ry, 40)
    dx, dy = ell_tan(rx, ry, 40, 1)
    b += chevron(px, py, dx, dy, ORG, 3.2, 13)
b += text(xs[2] + rx + 6, cy + ry + 16, "I", ORG, 16, "start", "700")
b += text(cx + 6.2 * s, cy - 22, "B", BLUE, 16, "start", "700")
fig4c = wrap(VB4, "Ống dây dài nhìn xiên với đường sức tính bằng mô hình Biot–Savart: trong lòng ống năm đường sức song song với trục, cách đều nhau; hai đường sát vách khép kín bên ngoài, các đường ở gần trục toả ra ngoài hai đầu như nam châm thẳng; nửa vòng phía trước đè lên đường sức, nửa phía sau bị đường sức che",
             b, "Hình 4c. Ống dây: trong lòng ống <strong>B</strong> đều, bên ngoài như nam châm thẳng." + SRC.format(h="22.39"))

# ------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
for n, f in (("1", fig1), ("2", fig2), ("3", fig3), ("4A", fig4a), ("4B", fig4b), ("4C", fig4c)):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(src)
print("ok", len(src), "bytes")
