"""Sinh 4 hình SVG cho bài "Bài 11. Thực hành đo độ lớn cảm ứng từ" (Vật lí 12)
và thay các mốc <!--FIGn--> trong theory.src.html -> theory.html.
Chạy từ thư mục này: python3 build_figs.py
"""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import *  # noqa: E402


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def rect(x, y, w, h, fill, stroke="currentColor", sw=2, rx=6):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def wrap(vb, label, body, cap, exp=""):
    e = f' data-exp="{exp}"' if exp else ""
    return (f'<figure class="fig" data-tl="1"{e}><svg viewBox="{vb}" role="img" aria-label="{label}">{body}</svg>'
            f'<figcaption>{cap}</figcaption></figure>')


RED_F, BLUE_F, GREY_F = "rgba(248,113,113,.28)", "rgba(56,189,248,.28)", "rgba(148,163,184,.16)"


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


# ======================================================= Hình 1: bố trí cân dòng điện (phối cảnh xiên)
# Chiều sâu vẽ xiên lên-phải. Khung dây nằm trong mặt phẳng (thẳng đứng, chiều sâu): cạnh dưới đi xuyên khe.
def poly(pts, fill, stroke="currentColor", sw=2, op=1):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" opacity="{op}"/>'


SD = (36, -24)                       # chiều sâu bệ cân
MD = (24, -16)                       # chiều sâu nam châm
add = lambda P, D, t=1: (P[0] + t * D[0], P[1] + t * D[1])
b = ""
b += line(10, 268, 370, 268, "currentColor", 2.5)                       # mặt bàn
# cân: mặt trên, mặt phải, mặt trước
b += poly([(30, 230), (250, 230), add((250, 230), SD), add((30, 230), SD)], "rgba(148,163,184,.30)")
b += poly([(250, 230), add((250, 230), SD), add((250, 268), SD), (250, 268)], "rgba(148,163,184,.42)")
b += rect(30, 230, 220, 38, GREY_F, "currentColor", 2, 2)
b += text(42, 255, "cân 0,01 g", "currentColor", 14, "start", "700")
b += rect(170, 238, 66, 22, "#d1fae5", "#047857", 1.5, 4)
b += text(203, 254, "? g", "#065f46", 15, "middle", "800")
# khung dây: cạnh dưới từ A (trước nam châm) tới Bk (sau nam châm), hai cạnh đứng lên tới A2, B2
C0 = (140, 160)                                                         # giao cạnh dưới với mặt trước nam châm (tâm khe)
A, Bk = add(C0, MD, -0.2), add(C0, MD, 1.2)        # cả cạnh dưới nằm gọn trong khe
A2, B2 = (A[0], 76), (Bk[0], 76 + MD[1] * 1.4)          # cạnh trên song song cạnh dưới
WIRE = ORG
b += line(*Bk, *add(C0, MD, 1), WIRE, 3.5) + line(*Bk, *B2, WIRE, 3.5)  # phần khung phía sau nam châm
# nam châm chữ U (mặt trước lệch (6,-4) so với mép trước bệ cân)
X0, YB = 76, 226
b += u_magnet(X0, 116, 136, 110, 36, 30, 52, MD)
# phần khung phía trước (cạnh dưới trong khe + cạnh đứng trước + cạnh trên)
b += line(*A, *add(C0, MD, 1), WIRE, 3.5) + line(*A, *A2, WIRE, 3.5) + line(*A2, *B2, WIRE, 3.5)
b += f'<text x="160" y="173" fill="#c2410c" font-size="20" font-weight="800" text-anchor="middle">ℓ</text>'
# giá đỡ riêng đứng trên bàn, ngoài cân
b += rect(312, 258, 56, 10, "rgba(148,163,184,.45)", "currentColor", 2, 2)
b += rect(335, 30, 10, 228, "rgba(148,163,184,.40)", "currentColor", 2, 2)
b += rect(130, 30, 215, 10, "rgba(148,163,184,.40)", "currentColor", 2, 2)
HX = (A2[0] + B2[0]) / 2
b += line(HX, 40, HX, (A2[1] + B2[1]) / 2, "currentColor", 2)
b += text(150, 22, "giá đỡ riêng, không chạm cân", "currentColor", 14, "start", "700")
b += text(14, 84, "khung dây", "#c2410c", 14, "start", "700") + line(88, 80, A2[0] - 4, 90, "#c2410c", 1.4)
b += text(262, 150, "nam châm", "currentColor", 14, "start", "600") + line(258, 158, 230, 176, "currentColor", 1.4)
b += text(262, 168, "chữ U", "currentColor", 14, "start", "600")
b += text(14, 292, "khung nối nguồn một chiều + ampe kế", "currentColor", 14, "start", "600")
fig1 = wrap("0 0 380 302", "Cân điện tử có nam châm chữ U trên đĩa; khung dây treo trên giá đứng riêng trên bàn, cạnh dưới dài ℓ xuyên qua khe nam châm",
            b, "Hình 1. Bố trí cân dòng điện: nam châm chữ U nằm trên đĩa cân, khung dây treo trên giá đứng riêng.<br>Cạnh dưới của khung (dài $\ell$, tức $l$ trong công thức) nằm trong khe nam châm.<br>Dây không chạm vào cân hay nam châm.")

# ======================================================= Hình 2: lực và phản lực (mặt cắt khe nam châm)
b = text(20, 40, "⊙ dòng điện hướng ra khỏi trang", "currentColor", 14, "start", "700")
b += rect(20, 240, 230, 40, GREY_F)
b += text(135, 266, "cân điện tử", "currentColor", 14, "middle", "700")
b += u_magnet(30, 110, 210, 130, 50, 40, 60, (14, -10))
WX, WY, FL = 135, 148, 50                       # tâm dây; F và F′ cùng độ lớn → cùng dài FL px
b += field_line(98, WY, WX - 14, WY, GRN, 2.2) + field_line(WX + 14, WY, 184, WY, GRN, 2.2) + field_line(98, 164, 184, 164, GRN, 2.2)
b += text(102, WY - 12, "B", "#047857", 16, "start", "800")
b += f'<circle cx="{WX}" cy="{WY}" r="9" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="{WX}" cy="{WY}" r="3" fill="currentColor"/>'
b += arrow("", "r", WX, WY - 10, WX, WY - 10 - FL, 3)
b += text(WX, WY - FL - 18, "F lên dây", "#be123c", 15, "middle", "800")
b += line(215, 176, 215, 176 + FL, "#c2410c", 2.8) + chevron(215, 176 + FL, 0, 1, "#c2410c", 2.8, 11.5)               # đặt lên nam châm (cánh S + gông)
b += text(264, 200, "F′ lên", "#c2410c", 15, "start", "800")
b += text(264, 219, "nam châm", "#c2410c", 15, "start", "800")
fig2 = wrap("0 0 380 290", "Mặt cắt khe nam châm: dây có dòng hướng ra khỏi trang chịu lực từ hướng lên, nam châm chịu phản lực hướng xuống cùng độ lớn làm cân tăng",
            b, "Hình 2. Mặt cắt khe nam châm chữ U.<br>Đường sức từ đi từ cực N sang cực S.<br>Dây chịu lực $F$, nam châm chịu lực $F'$ cùng độ lớn và ngược chiều; cân chỉ cảm nhận $F'$.")

# ======================================================= Hình 3: đồ thị Δm–I
X0, Y0, KX, KY = 56, 215, 56, 62     # gốc, px mỗi A, px mỗi g
pts = [(1, .50), (2, .97), (3, 1.45), (4, 1.97), (5, 2.44)]
SLOPE = sum(i * m for i, m in pts) / sum(i * i for i, _ in pts)
b = text(60, 26, "Δm (g)", "currentColor", 14, "start", "700")
for g in (.5, 1, 1.5, 2, 2.5):
    y = Y0 - g * KY
    b += line(X0, y, 350, y, "currentColor", 1, "", .18)
    b += text(48, y + 5, str(g).replace(".", ",").rstrip("0").rstrip(",") if g != int(g) else str(int(g)), "currentColor", 14, "end", "500")
for i in range(1, 6):
    x = X0 + i * KX
    b += line(x, Y0, x, Y0 + 6, "currentColor", 2)
    b += text(x, Y0 + 24, str(i), "currentColor", 14, "middle", "500")
b += line(X0, Y0, 352, Y0, "currentColor", 2.5)
b += line(X0, Y0, X0, 36, "currentColor", 2.5)
b += text(352, Y0 + 44, "I (A)", "currentColor", 14, "end", "700")
b += line(X0, Y0, X0 + 5.1 * KX, Y0 - SLOPE * 5.1 * KY, GRN, 2.6)
for i, m in pts:
    b += f'<circle cx="{X0 + i * KX}" cy="{Y0 - m * KY:.1f}" r="5.5" fill="{ORG}" stroke="currentColor" stroke-width="1.2"/>'
b += text(78, 92, "độ dốc ≈ 0,489 g/A", GRN, 14, "start", "700")
b += text(78, 112, "→ B ≈ 0,12 T", GRN, 14, "start", "700")
fig3 = wrap("0 0 380 272", "Đồ thị khối lượng tăng theo cường độ dòng điện: năm điểm đo nằm gần đường thẳng qua gốc toạ độ có độ dốc khoảng 0,489 gam trên ampe",
            b, "Hình 3. Δm tăng gần tỉ lệ với $I$: năm điểm đo (số liệu minh hoạ) nằm sát đường thẳng qua gốc toạ độ.<br>Độ dốc đường thẳng bằng $Bl/g$.",
            "tn-l12-thuchanhtu-01")

# ======================================================= Hình 4: dây hợp góc với đường sức (ảnh OpenStax, chèn trực tiếp)
# Ảnh raster là ngoại lệ có chủ đích của quy tắc SVG tự vẽ. OpenStax, College Physics 2e, Hình 22.30 (CC BY-NC-SA 4.0).
fig4 = ('<figure class="fig" data-tl="1" data-exp="tn-l12-thuchanhtu-03">'
        '<img src="/assets/openstax/l12-thuc-hanh-cam-ung-tu/hinh-5.webp" '
        'alt="Bàn tay phải đặt trong mặt phẳng chứa dòng điện I và cảm ứng từ B hợp nhau góc theta; lực từ F hướng vuông góc với mặt phẳng đó" '
        'loading="lazy" width="750" height="784">'
        '<figcaption>Hình 4.<br>'
        '<em>RHR-1</em>: bàn tay phải.<br>'
        '<em>F ⊥ plane of I and B</em>: vuông góc mặt phẳng I, B.<br>'
        'Hình: OpenStax, College Physics 2e, Hình 22.30 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</figcaption></figure>')



# ======================================================= Mô phỏng (radio + CSS, không JS)
VAL = {1: (0.50, 4.91, 0.123), 2: (0.97, 9.52, 0.119), 3: (1.45, 14.22, 0.119), 4: (1.97, 19.33, 0.121), 5: (2.44, 23.94, 0.120)}
vn = lambda x, d: f"{x:.{d}f}".replace(".", ",")
vm = lambda x, d: f"{x:.{d}f}".replace(".", "{,}")

# Nam châm chữ U: hai cánh 40×140 + gông 190×40; trọng tâm tính từ ba hình chữ nhật.
UP = "M40,112 H80 V252 H190 V112 H230 V292 H40 Z"
_parts = [(40 * 140, 60, 182), (40 * 140, 210, 182), (190 * 40, 135, 272)]
GX = sum(a * x for a, x, _ in _parts) / sum(a for a, _, _ in _parts)
GY = sum(a * y for a, _, y in _parts) / sum(a for a, _, _ in _parts)
GXr, GYr = round(GX), round(GY)

COL = {"F": RED, "Fp": ORG, "Q": "#a78bfa", "N": GRN, "P": "#94a3b8", "B": BLUE}


def arr(cx, cy, key, cls, w):
    """Mũi tên có độ dài/ chiều do CSS (--L, --sg) quyết định; đuôi ở đúng (cx, cy)."""
    c = COL[key]
    return (f'<g transform="translate({cx},{cy})">'
            f'<rect class="sim-sh {cls}" x="{-w/2}" y="-120" width="{w}" height="120" fill="{c}"/>'
            f'<polygon class="sim-hd {cls}" points="0,0 -7,13 7,13" fill="{c}"/></g>')


def wire(cx, cy):
    return (f'<circle cx="{cx}" cy="{cy}" r="9" fill="rgba(251,146,60,.25)" stroke="currentColor" stroke-width="2"/>'
            f'<circle class="sim-wp" cx="{cx}" cy="{cy}" r="3" fill="currentColor"/>'
            f'<path class="sim-wn" d="M{cx-5},{cy-5} L{cx+5},{cy+5} M{cx+5},{cy-5} L{cx-5},{cy+5}" stroke="currentColor" stroke-width="2"/>')


def hatch(x1, x2, y, n, c="currentColor"):
    step = (x2 - x1) / n
    return "".join(line(x1 + k * step, y, x1 + k * step - 9, y + 11, c, 1.6, "", .7) for k in range(n + 1))


def sim_html():
    WY = 150  # tâm dây
    sv = defs("sm")
    sv += text(20, 22, "B đi từ N sang S →", GRN, 14, "start", "700")
    # mặt bàn + cân
    sv += line(8, 336, 372, 336, "currentColor", 3) + hatch(14, 366, 337, 26)
    sv += rect(20, 292, 230, 44, GREY_F)
    sv += text(135, 311, "cân điện tử", "currentColor", 14, "middle", "700")
    sv += rect(40, 318, 190, 10, "none", "currentColor", 1, 3)
    sv += '<rect class="sim-bar" x="135" y="318" width="95" height="10" rx="3" fill="#fb923c"/>'
    sv += text(28, 327, "−", "currentColor", 14, "middle", "700") + text(242, 327, "+", "currentColor", 14, "middle", "700")
    # nam châm chữ U: cực N, S ở đầu cánh
    sv += u_magnet(40, 112, 190, 180, 40, 40, 64, (10, -7))
    # đường sức B
    sv += field_line(94, 122, 122, 122, GRN, 2.2, "5 3", 10) + field_line(148, 122, 182, 122, GRN, 2.2, "5 3", 10)
    # giá gá cứng: đế bắt xuống bàn, trụ, tay đỡ, thanh treo, ngàm ôm dây, bu lông
    sv += rect(284, 326, 60, 10, "rgba(148,163,184,.45)", "currentColor", 2, 2) + hatch(286, 342, 337, 6)
    sv += rect(306, 50, 16, 278, "rgba(148,163,184,.4)", "currentColor", 2, 2)
    sv += rect(135, 50, 187, 14, "rgba(148,163,184,.4)", "currentColor", 2, 2)
    sv += rect(130, 64, 10, 70, "rgba(148,163,184,.4)", "currentColor", 2, 2)
    sv += f'<path d="M118,128 H152 V{WY} a17,17 0 0 1 -34,0 Z" fill="rgba(148,163,184,.55)" stroke="currentColor" stroke-width="2"/>'
    for (bx, by) in ((314, 58), (314, 100), (314, 300), (135, 98), (135, 124)):
        sv += f'<circle cx="{bx}" cy="{by}" r="3.2" fill="currentColor"/>'
    sv += text(150, 42, "giá gá cứng xuống bàn", "currentColor", 14, "start", "700")
    sv += wire(135, WY)
    sv += f'<circle cx="{GXr}" cy="{GYr}" r="4" fill="currentColor"/>' + text(GXr + 9, GYr - 6, "G", "currentColor", 14, "start", "700")
    sv += arr(135, WY, "F", "a-F", 4) + arr(GXr, GYr, "Fp", "a-Fp", 4)
    sv += text(160, 150, "F", RED, 15, "start", "700") + text(GXr + 22, GYr + 20, "F′", ORG, 15, "start", "700")
    scene = (f'<svg viewBox="0 0 380 346" role="img" aria-label="Mô phỏng cân dòng điện: nam châm chữ U đặt trên cân, dây gá cứng trên giá, chọn dòng điện để đổi lực và số cân">{sv}</svg>')

    # biểu đồ lực: ba vật, đuôi mũi tên đặt đúng trọng tâm
    CY = 180
    fb = ""
    for k, (cx, ten) in enumerate(((63, "Dây điện"), (190, "Nam châm"), (317, "Cân"))):
        fb += text(cx, 20, ten, "currentColor", 14, "middle", "700")
    fb += wire(63, CY)
    ux, uy, us = 190, CY, .55
    fb += f'<g transform="translate({ux - GX * us:.2f},{uy - GY * us:.2f}) scale({us})">{u_magnet(40, 112, 190, 180, 40, 40, 64, (10, -7), fs=26, sw=3.5)}</g>'
    fb += rect(262, CY - 22, 110, 44, GREY_F)
    # mũi tên dày (trọng lực, phản lực pháp tuyến) vẽ trước, mũi tên mảnh (lực từ, lực giữ) đè lên
    fb += arr(190, CY, "P", "a-Pm", 6) + arr(190, CY, "N", "a-N", 6)
    fb += arr(317, CY, "P", "a-Pc", 6) + arr(317, CY, "N", "a-Np", 6) + arr(317, CY, "B", "a-Qb", 6)
    fb += arr(63, CY, "F", "a-F", 3.6) + arr(63, CY, "Q", "a-Q", 3.6) + arr(190, CY, "Fp", "a-Fp", 3.6)
    for cx in (63, 190, 317):
        fb += f'<circle cx="{cx}" cy="{CY}" r="4" fill="currentColor"/>'
    fb += text(76, CY - 8, "G", "currentColor", 14, "start", "700") + text(203, CY - 8, "G", "currentColor", 14, "start", "700") + text(330, CY - 8, "G", "currentColor", 14, "start", "700")
    fbd = (f'<div class="tl-sim__fbd"><svg viewBox="0 0 380 300" role="img" aria-label="Biểu đồ lực tác dụng lên dây, nam châm và cân; đuôi mũi tên đặt tại trọng tâm G của từng vật">{fb}</svg>'
           '<details class="tl-details tl-more"><summary>Chú giải các lực</summary><ul class="tl-sim__leg">'
           '<li><strong>Dây:</strong> <span class="lg lg-F">●</span> F lực từ</li>'
           '<li><strong>Dây:</strong> <span class="lg lg-Q">●</span> Q lực giữ của giá, ngược F nên dây đứng yên</li>'
           '<li><strong>Nam châm:</strong> <span class="lg lg-P">●</span> P trọng lực</li>'
           '<li><strong>Nam châm:</strong> <span class="lg lg-Fp">●</span> F′ phản lực của F</li>'
           '<li><strong>Nam châm:</strong> <span class="lg lg-N">●</span> N phản lực của cân (N = P + F′)</li>'
           '<li><strong>Cân:</strong> <span class="lg lg-P">●</span> P trọng lực</li>'
           '<li><strong>Cân:</strong> <span class="lg lg-N">●</span> N′ áp lực của nam châm, bằng N</li>'
           '<li><strong>Cân:</strong> <span class="lg lg-B">●</span> phản lực của mặt bàn</li>'
           '<li><strong>Dây:</strong> trọng lực rất nhỏ nên bỏ qua.</li>'
           '</ul>'
           '<p>G là trọng tâm của từng vật.</p>'
           '<p>Dây: G ở tâm tiết diện.</p>'
           '<p>Cân: G ở tâm bệ cân.</p>'
           '<p>Nam châm chữ U: G nằm <em>trong khe</em>, trên gông.</p>'
           '<p>Mũi tên F, F′ phóng to cho dễ thấy.</p>'
           '<p>Các mũi tên còn lại không vẽ theo tỉ lệ.</p></details></div>')

    h = '<div class="tl-box tl-box--exp tl-sim" data-exp="tn-l12-thuchanhtu-04">\n<p class="tl-label">🎛️ Mô phỏng: tự chỉnh dòng điện, quan sát cân</p>\n'
    h += '<div class="tl-sim__row"><b>Cường độ dòng điện</b>'
    for i in range(6):
        h += f'<input type="radio" name="tls12-i" class="tls-i{i}" id="tls12-i{i}"' + (" checked" if i == 0 else "") + ">"
        h += f'<label for="tls12-i{i}" class="tl-sim__chip">{i} A</label>'
    h += '</div>\n<div class="tl-sim__row"><b>Chiều dòng điện</b>'
    h += '<input type="radio" name="tls12-d" class="tls-dir-f" id="tls12-df" checked><label for="tls12-df" class="tl-sim__chip">⊙ ra khỏi trang</label>'
    h += '<input type="radio" name="tls12-d" class="tls-dir-r" id="tls12-dr"><label for="tls12-dr" class="tl-sim__chip">⊗ vào trong trang</label></div>\n'
    h += '<div class="tl-sim__row"><input type="checkbox" class="tls-force" id="tls12-force"><label for="tls12-force" class="tl-sim__chip">Hiện các lực</label></div>\n'
    h += scene + '\n<div aria-live="polite">\n'
    h += '<div class="tl-sim__st st-0"><p>Cân: <strong>0,00 g</strong></p><p>Không có dòng điện nên không có lực từ.</p></div>\n'
    for i, (m, f, bb) in VAL.items():
        for sg, sc in (("p", "+"), ("n", "−")):
            h += (f'<div class="tl-sim__st st-{i}{sg}"><p>Cân: <strong>{sc}{vn(m, 2)} g</strong></p>'
                  f'<p>$F = \\Delta m\\, g \\approx {vm(f, 2)}\\ \\text{{mN}}$</p><p>$B = \\dfrac{{F}}{{Il}} \\approx {vm(bb, 3)}\\ \\text{{T}}$</p></div>\n')
    h += '</div>\n' + fbd + '\n<p>Thử:</p>\n<p>1. Tăng $I$ từng nấc: số cân và mũi tên đổi thế nào?</p>\n<p>2. Đảo chiều ở cùng $I$.</p>\n<p>3. Bật <em>Hiện các lực</em>, so độ dài $N$ với $P$ của nam châm.</p>\n<p>Số liệu minh hoạ, khớp bảng ở mục II.3 ($l = 4{,}0\\ \\text{cm}$).</p>\n</div>'
    return h

# ------------------------------------------------------- thay vào theory.html
src = open("theory.src.html", encoding="utf8").read()
assert "<!--SIM-->" in src
src = src.replace("<!--SIM-->", sim_html())
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in src, f"thiếu mốc FIG{n}"
    src = src.replace(f"<!--FIG{n}-->", f)
open("theory.html", "w", encoding="utf8").write(margin_figs(src))
print("ok", len(src), "bytes; slope", round(SLOPE, 4))
