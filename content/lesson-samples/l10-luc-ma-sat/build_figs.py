"""Sinh 4 hình SVG cho bài 'Lực ma sát' (lesson 63) và thay mốc <!--FIGn--> / __NHANXET__ / __PHUT__ trong
theory.src.html -> theory.html. Chạy: python3 build_figs.py (từ thư mục bài hoặc gốc repo).
Tự kiểm: nhãn không chồng nhau, không vượt viewBox, không bị nét/mũi tên cắt xuyên; độ dài mũi tên đúng tỉ lệ."""
import math, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import RED, BLUE, ORG, GRN, wrap  # noqa: E402

COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}
LABELS = []   # (fig, x0, y0, x1, y1, text)
SEGS = []     # (fig, x1, y1, x2, y2, tên) — nét để kiểm nhãn bị cắt xuyên
CUR = {"fig": 0}
VB = {}
bad = []


def defs(p):
    out = "<defs>"
    for n, c in COL.items():
        out += (f'<marker id="{p}-{n}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="12" markerHeight="12" '
                f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
    return out + "</defs>"


def arrow(p, c, x1, y1, x2, y2, w=3, dash="", name="mũi tên"):
    SEGS.append((CUR["fig"], x1, y1, x2, y2, name))
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{COL[c]}" stroke-width="{w}"{d} '
            f'marker-end="url(#{p}-{c})"/>')


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, name="nét", check=True):
    if check:
        SEGS.append((CUR["fig"], x1, y1, x2, y2, name))
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def sub(base, s):
    return f'{base}<tspan baseline-shift="sub" font-size="12">{s}</tspan>'


def text(x, y, s, c="currentColor", size=14, anchor="start", weight="700", italic=False):
    plain = re.sub(r"<[^>]+>", "", s)
    w = 0.58 * size * len(plain)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    LABELS.append((CUR["fig"], x0, y - 0.75 * size, x0 + w, y + 0.25 * size, plain))
    st = ' font-style="italic" font-family="serif"' if italic else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}"{st} '
            f'text-anchor="{anchor}">{s}</text>')


def seg_hits_box(x1, y1, x2, y2, bx0, by0, bx1, by1):
    """Đoạn thẳng có đi qua hộp không (lấy mẫu dày)."""
    for i in range(101):
        t = i / 100
        x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        if bx0 < x < bx1 and by0 < y < by1:
            return True
    return False


def num(v, d=1):
    return f"{v:.{d}f}".replace(".", ",")


g = 9.8

# ---------------- Hình 1: ma sát theo lực kéo (hàng 3 của bảng: N = 5,88 N) ----------------
CUR["fig"] = 1
VB[1] = (440, 250)
OX, OY, SX, SY = 60, 215, 110, 72          # px/N
FMAX, FTR, FEND = 2.1, 1.7, 3.0
b = defs("f1")
b += arrow("f1", "k", OX, OY, 420, OY, 2, name="trục F") + arrow("f1", "k", OX, OY, OX, 18, 2, name="trục Fms")
for F in (1, 2, 3):
    x = OX + SX * F
    b += line(x, OY - 4, x, OY + 4, "currentColor", 1.5, check=False) + text(x, OY + 20, str(F), "currentColor", 13, "middle", "500")
b += text(OX - 8, OY + 20, "0", "currentColor", 13, "end", "500")
for v in (1.0, FTR, FMAX):
    y = OY - SY * v
    b += line(OX - 4, y, OX + 4, y, "currentColor", 1.5, check=False) + text(OX - 8, y + 5, num(v), "currentColor", 13, "end", "500")
xp, yp = OX + SX * FMAX, OY - SY * FMAX
ytr = OY - SY * FTR
b += line(OX, yp, xp, yp, "currentColor", 1, "3 5", .4, check=False) + line(OX, ytr, xp, ytr, "currentColor", 1, "3 5", .4, check=False)
b += line(OX, OY, xp, yp, ORG, 3, name="đoạn nghỉ")
b += line(xp, yp, xp, ytr, "currentColor", 1.6, "4 4", name="tụt")
b += line(xp, ytr, OX + SX * FEND, ytr, RED, 3, name="đoạn trượt")
b += f'<circle cx="{xp:.1f}" cy="{yp:.1f}" r="4.5" fill="{ORG}"/>'
b += text(420, OY - 10, "F kéo (N)", "currentColor", 14, "end")
b += text(OX + 8, 26, sub("F", "ms") + " (N)", "currentColor", 14, "start")
b += text(xp, yp - 12, "nghỉ cực đại", ORG, 14, "middle")
b += text(xp + 20, ytr + 22, "trượt: μN", RED, 14, "start")
b += text(214, 172, "đứng yên:", ORG, 14, "start")
b += text(214, 190, sub("F", "ms") + " = F kéo", ORG, 14, "start")
fig1 = wrap(f"0 0 {VB[1][0]} {VB[1][1]}",
            "Đồ thị lực ma sát theo lực kéo: đứng yên thì ma sát bằng lực kéo, tăng tới 2,1 N; khi trượt ma sát tụt xuống 1,7 N và không đổi", b,
            "Hình 1. Kéo hộp gỗ 0,60 kg tăng dần (số đo ở mục 3). Còn đứng yên: ma sát nghỉ bằng đúng lực kéo, tăng tới cực đại 2,1 N. "
            "Bắt đầu trượt: ma sát tụt xuống 1,7 N và giữ nguyên dù kéo mạnh hơn.")
fig1 = fig1.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-luc-ma-sat-01"', 1)

# ---------------- Hình 2: kéo chếch lên — N = mg − F sinα (m = 3 kg, F = 20 N, μ = 0,5) ----------------
CUR["fig"] = 2
VB[2] = (440, 260)
K = 4.0                     # px/N
m2, F2, al2, mu2 = 3.0, 20.0, math.radians(30), 0.5
P2 = m2 * g
N2 = P2 - F2 * math.sin(al2)
Fms2 = mu2 * N2
CX, CY = 200, 110
FL = CY + 17                # mặt sàn = đáy hộp
b = defs("f2")
b += line(30, FL, 410, FL, "currentColor", 2, "", .6, check=False)
b += f'<rect x="{CX-20}" y="{CY-17}" width="40" height="34" rx="3" fill="rgba(251,146,60,.18)" stroke="currentColor" stroke-width="2"/>'
fx, fy = CX + K * F2 * math.cos(al2), CY - K * F2 * math.sin(al2)
b += line(CX, CY, fx, CY, RED, 1.4, "4 4", name="Fcos")
b += line(fx, CY, fx, fy, RED, 1.4, "4 4", name="Fsin")
b += arrow("f2", "r", CX, CY, fx, fy, 3, name="F")
b += arrow("f2", "k", CX, CY, CX, CY + K * P2, 2.6, name="P")
b += arrow("f2", "b", CX, CY, CX, CY - K * N2, 2.6, name="N")
b += arrow("f2", "o", CX, CY, CX - K * Fms2, CY, 3, name="Fms")
b += f'<circle cx="{CX}" cy="{CY}" r="3.5" fill="currentColor"/>'
ar = 26
b += (f'<path d="M{CX+ar},{CY} A{ar},{ar} 0 0 0 {CX+ar*math.cos(al2):.1f},{CY-ar*math.sin(al2):.1f}" '
      f'fill="none" stroke="currentColor" stroke-width="1.4"/>')
b += text(CX + 34, CY - 3, "α", "currentColor", 15, "start", "700", True)
b += text(fx + 6, fy - 4, "F", RED, 16, "start", "700", True)
b += text(fx + 8, CY - 10, "F sinα", RED, 14, "start")
b += text(CX + 8, CY + K * P2 - 4, "P", "currentColor", 16, "start", "700", True)
b += text(CX + 8, CY - K * N2 + 10, "N", BLUE, 16, "start", "700", True)
b += text(CX - K * Fms2 - 6, CY - 8, sub("F", "ms"), ORG, 16, "end", "700")
b += text(310, 250, "N + F sinα = P", "currentColor", 14, "middle")
fig2 = wrap(f"0 0 {VB[2][0]} {VB[2][1]}",
            "Vật trên sàn ngang bị kéo chếch lên góc alpha: các lực F, P, N, ma sát đặt ở trọng tâm; thành phần F sin alpha đỡ bớt vật", b,
            f"Hình 2. Kéo chếch lên góc α (vẽ theo tỉ lệ với $m$ = 3 kg, $F$ = 20 N, α = 30°, μ = 0,5). Các lực vẽ chung gốc ở trọng tâm. "
            f"Thành phần $F\\sin\\alpha$ đỡ bớt vật nên $N$ = {num(N2)} N, nhỏ hơn $P$ = {num(P2)} N.")
assert abs(K * N2 + K * F2 * math.sin(al2) - K * P2) < 1e-6

# ---------------- Hình 3: mặt nghiêng α = 30°, μ = 0,20 ----------------
CUR["fig"] = 3
VB[3] = (440, 320)
al = math.radians(30)
mu3 = 0.20
TOP = (30, 80)
L = 370
BOT = (TOP[0] + L, TOP[1] + L * math.tan(al))
d = (math.cos(al), math.sin(al))          # dọc dốc, hướng xuống (y hướng xuống)
n = (math.sin(al), -math.cos(al))         # pháp tuyến, hướng ra ngoài mặt dốc
SP = 140                                   # px cho P
b = defs("f3")
b += (f'<path d="M{TOP[0]},{TOP[1]} L{BOT[0]:.1f},{BOT[1]:.1f} L{TOP[0]},{BOT[1]:.1f} Z" fill="rgba(148,163,184,.15)" '
      f'stroke="currentColor" stroke-width="2"/>')
SEGS.append((3, TOP[0], TOP[1], BOT[0], BOT[1], "mặt dốc"))
SEGS.append((3, TOP[0], BOT[1], BOT[0], BOT[1], "đáy"))
s0 = 150
px0, py0 = TOP[0] + s0 * d[0], TOP[1] + s0 * d[1]
h = 18
CX, CY = px0 + h * n[0], py0 + h * n[1]
corners = [(px0 - h * d[0], py0 - h * d[1]), (px0 + h * d[0], py0 + h * d[1]),
           (px0 + h * d[0] + 2 * h * n[0], py0 + h * d[1] + 2 * h * n[1]), (px0 - h * d[0] + 2 * h * n[0], py0 - h * d[1] + 2 * h * n[1])]
b += '<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in corners) + ' Z" fill="rgba(251,146,60,.2)" stroke="currentColor" stroke-width="2"/>'
Px, Py = SP * math.sin(al), SP * math.cos(al)
Fm3 = mu3 * Py
b += arrow("f3", "k", CX, CY, CX, CY + SP, 2.6, name="P")
b += line(CX, CY, CX + Px * d[0], CY + Px * d[1], "currentColor", 1.6, "5 4", name="Px")
b += line(CX, CY, CX - Py * n[0], CY - Py * n[1], "currentColor", 1.6, "5 4", name="Py")
b += line(CX + Px * d[0], CY + Px * d[1], CX, CY + SP, "currentColor", 1, "2 4", .5, check=False)
b += line(CX - Py * n[0], CY - Py * n[1], CX, CY + SP, "currentColor", 1, "2 4", .5, check=False)
b += arrow("f3", "b", CX, CY, CX + Py * n[0], CY + Py * n[1], 2.6, name="N")
b += arrow("f3", "o", CX, CY, CX - Fm3 * d[0], CY - Fm3 * d[1], 3, name="Fms")
b += f'<circle cx="{CX:.1f}" cy="{CY:.1f}" r="3.5" fill="currentColor"/>'
b += text(CX + 8, CY + SP + 2, "P", "currentColor", 16, "start", "700", True)
b += text(CX + Py * n[0] + 8, CY + Py * n[1] + 10, "N", BLUE, 16, "start", "700", True)
b += text(CX + Px * d[0] + 6, CY + Px * d[1] - 8, sub("P", "x"), "currentColor", 16, "start", "700")
b += text(CX - Py * n[0] - 8, CY - Py * n[1] + 6, sub("P", "y"), "currentColor", 16, "end", "700")
b += text(CX - Fm3 * d[0] - 8, CY - Fm3 * d[1] - 8, sub("F", "ms"), ORG, 16, "end", "700")
ar = 40
b += (f'<path d="M{BOT[0]-ar:.1f},{BOT[1]:.1f} A{ar},{ar} 0 0 1 {BOT[0]-ar*math.cos(al):.1f},{BOT[1]-ar*math.sin(al):.1f}" '
      f'fill="none" stroke="currentColor" stroke-width="1.4"/>')
b += text(BOT[0] - ar - 6, BOT[1] - 6, "α", "currentColor", 15, "end", "700", True)
fig3 = wrap(f"0 0 {VB[3][0]} {VB[3][1]}",
            "Vật trên mặt nghiêng góc alpha: trọng lực P tách thành Px dọc dốc và Py vuông góc dốc; phản lực N cân bằng Py; ma sát hướng lên dốc", b,
            "Hình 3. Vật trượt xuống mặt nghiêng (vẽ cho α = 30°, μ = 0,20). $P$ tách thành $P_x = P\\sin\\alpha$ kéo vật xuống dốc "
            "và $P_y = P\\cos\\alpha$ ép vào dốc (nét đứt). $N$ cân bằng $P_y$; $F_{\\text{ms}} = \\mu N$ hướng lên dốc, ngược chiều trượt.")
# kiểm tỉ lệ: N = Py, Px = P sinα, đỉnh mũi P nằm trên đường chéo hình chữ nhật Px–Py
assert abs(math.hypot(Px, Py) - SP) < 1e-6
for (x, y) in corners:
    if not (TOP[0] <= x <= BOT[0]):
        bad.append("Hình 3: hộp vượt khỏi mặt dốc")

# ---------------- Hình 4: bước đi — ma sát nghỉ đẩy chân tới trước ----------------
CUR["fig"] = 4
VB[4] = (440, 240)
GY = 188
b = defs("f4")
b += line(20, GY, 420, GY, "currentColor", 2, "", .6, check=False)
hx, hy = 210, 118
b += f'<circle cx="{hx}" cy="52" r="13" fill="none" stroke="currentColor" stroke-width="2.5"/>'
b += line(hx, 65, hx, hy, "currentColor", 2.5, name="thân")
b += line(hx, hy, 150, GY - 2, "currentColor", 2.5, name="chân sau")
b += line(hx, hy, 268, GY - 2, "currentColor", 2.5, name="chân trước")
b += line(hx, 80, 178, 112, "currentColor", 2.5, name="tay sau")
b += line(hx, 80, 240, 108, "currentColor", 2.5, name="tay trước")
b += arrow("f4", "r", 150, GY - 6, 214, GY - 6, 3.2, name="Fmsn")
b += arrow("f4", "b", 150, GY + 10, 86, GY + 10, 3.2, name="chân đẩy đất")
b += arrow("f4", "g", 300, 60, 380, 60, 3.2, name="hướng đi")
b += text(340, 46, "hướng đi", GRN, 14, "middle")
b += text(144, GY - 26, sub("F", "msn"), RED, 16, "end", "700")
b += text(144, GY - 6, "đất đẩy chân tới", RED, 14, "end")
b += text(86, GY + 32, "chân đẩy đất lùi", BLUE, 14, "start")
fig4 = wrap(f"0 0 {VB[4][0]} {VB[4][1]}",
            "Người bước đi: chân sau đẩy mặt đất ra sau, mặt đất tác dụng lên chân lực ma sát nghỉ hướng tới trước", b,
            "Hình 4. Chân sau có xu hướng trượt ra sau nên đất tác dụng lên chân ma sát nghỉ $F_{\\text{msn}}$ hướng tới trước (đỏ), "
            "cùng chiều em đi. Mũi xanh dương là lực chân đẩy đất (đặt lên mặt đất).")

# ---------------- Kiểm toạ độ nhãn ----------------
for i, (f, x0, y0, x1, y1, s) in enumerate(LABELS):
    W, H = VB[f]
    if x0 < 2 or y0 < 2 or x1 > W - 2 or y1 > H - 2:
        bad.append(f"Hình {f}: nhãn '{s}' vượt viewBox ({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f})")
    for gg, a0, b0, a1, b1, t in LABELS[i + 1:]:
        if gg == f and x0 < a1 and a0 < x1 and y0 < b1 and b0 < y1:
            bad.append(f"Hình {f}: nhãn '{s}' chồng '{t}'")
    for gg, sx1, sy1, sx2, sy2, nm in SEGS:
        if gg == f and seg_hits_box(sx1, sy1, sx2, sy2, x0 + 1, y0 + 1, x1 - 1, y1 - 1):
            bad.append(f"Hình {f}: nét '{nm}' cắt nhãn '{s}'")
print("\n".join(bad) if bad else "kiểm toạ độ: ok")

# ---------------- Nhận xét bảng số liệu: tính lại từ chính bảng ----------------
src = (HERE / "theory.src.html").read_text(encoding="utf8")
tbl = re.search(r"<th>\$N\$ \(N\)</th>.*?<tbody>(.*?)</tbody>", src, re.S).group(1)
rows = [[float(c.replace(",", ".")) for c in re.findall(r"<td>([\d,]+)</td>", r)] for r in re.findall(r"<tr>(.*?)</tr>", tbl)]
assert len(rows) == 4 and all(len(r) == 3 for r in rows), rows
for Nn, _, _ in rows:
    pass
ratios = [t / Nn for Nn, _, t in rows]
rn = [nm / Nn for Nn, nm, _ in rows]
mu_tb = sum(ratios) / len(ratios)
assert all(nm > t for _, nm, t in rows)
rel = [0.05 / t for _, _, t in rows]
worst = rel.index(max(rel))
assert worst == 0
NX = (f"$F_{{\\text{{trượt}}}}/N \\approx$ {'; '.join(num(r, 2) for r in ratios)}, trung bình $\\mu \\approx {num(mu_tb, 2).replace(',', '{,}')}$. "
      f"Trong cả 4 lần đo, nghỉ cực đại đều lớn hơn trượt; $F_{{\\text{{nghỉ max}}}}/N \\approx$ {num(min(rn), 2)}–{num(max(rn), 2)} (đó là $\\mu_n$). "
      f"</p><p>Lần đo đầu ($N = 1{{,}}96$ N) kém tin cậy nhất: lực kế đọc sai cỡ $\\pm 0{{,}}05$ N (nửa vạch chia), "
      f"so với $0{{,}}6$ N đã là ${round(100 * rel[0])}\\,\\%$; ở lần cuối chỉ còn ${round(100 * rel[-1])}\\,\\%$. "
      f"Lần 3 có tỉ số thấp nhất ({num(min(ratios), 2)}) nhưng sai số tương đối chỉ $\\approx {round(100 * rel[2])}\\,\\%$, nên vẫn tin cậy hơn lần đầu. "
      f"Kéo không thật đều hoặc dây lực kế hơi chếch cũng làm số chỉ dao động.")
print("tỉ số trượt:", [round(r, 3) for r in ratios], "μ tb", round(mu_tb, 3), "nghỉ:", [round(r, 3) for r in rn])
src = src.replace("__NHANXET__", NX)

# ---------------- Ghép hình ----------------
figs = [re.sub(r"<figcaption>Hình \d\.", f"<figcaption>Hình {k}.", f) for k, f in enumerate((fig1, fig2, fig3, fig4), 1)]
order = [int(k) for k in re.findall(r"<!--FIG(\d)-->", src)]
assert order == sorted(order) == list(range(1, len(figs) + 1)), order
for k, f in enumerate(figs, 1):
    src = src.replace(f"<!--FIG{k}-->", f)

lint = HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = HERE / "theory.html"
out.write_text(src.replace("__PHUT__", "?"), encoding="utf8")
r = subprocess.run([sys.executable, str(lint), str(out), "--json"], capture_output=True, text=True)
mm = re.search(r'"phut"\s*:\s*([\d.]+)', r.stdout)
phut = round(float(mm.group(1))) if mm else "?"
out.write_text(src.replace("__PHUT__", str(phut)), encoding="utf8")
print("ok", len(src), "ký tự; phút =", phut)
if bad:
    sys.exit(1)
