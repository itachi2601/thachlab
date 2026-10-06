"""Sinh 4 hình SVG cho bài 'Động lượng' (lesson 73) và thay mốc <!--FIGn--> / __BANG__ / __NHANXET__ / __PHUT__ /
thử thách ⭐⭐⭐ trong theory.src.html -> theory.html. Chạy: python3 build_figs.py (sau build_thi_nghiem.py).
Tự kiểm: nhãn không chồng nhau, không vượt viewBox, không bị nét cắt xuyên; mũi tên đúng tỉ lệ, đúng chiều."""
import json, math, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1].parent
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import RED, BLUE, ORG, GRN, wrap, person  # noqa: E402

COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}
LABELS, SEGS, VB, bad = [], [], {}, []
CUR = {"fig": 0}
G = 9.8


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
    return f'{base}<tspan baseline-shift="sub" font-size="13">{s}</tspan>'


def text(x, y, s, c="currentColor", size=14, anchor="start", weight="700", italic=False):
    plain = re.sub(r"<[^>]+>", "", s)
    w = 0.58 * size * len(plain)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    LABELS.append((CUR["fig"], x0, y - 0.75 * size, x0 + w, y + 0.25 * size, plain))
    st = ' font-style="italic" font-family="serif"' if italic else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}"{st} '
            f'text-anchor="{anchor}">{s}</text>')


def seg_hits_box(x1, y1, x2, y2, bx0, by0, bx1, by1):
    for i in range(101):
        t = i / 100
        x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        if bx0 < x < bx1 and by0 < y < by1:
            return True
    return False


def num(v, d=1):
    return f"{v:.{d}f}".replace(".", ",")


def knum(v, d=1):
    """Số thập phân trong $…$: dấu phẩy phải là {,}."""
    return num(v, d).replace(",", "{,}")


# ---------------- Hình 1: hai người trượt băng (mở bài — chỉ vẽ cảnh, không ghi số) ----------------
CUR["fig"] = 1
VB[1] = (440, 250)
b = defs("f1")
V_NHO, V_LON, KV = 4.0, 2.0, 30.0       # m/s, px/(m/s): mũi tên vận tốc tỉ lệ 4 : 2
for (x, gr, s, v, ten, mo_ta) in ((70, 115, 0.75, V_NHO, "bạn nhỏ", "nhẹ, lướt nhanh"),
                                  (70, 235, 1.0, V_LON, "người lớn", "nặng, lướt chậm")):
    b += line(20, gr, 420, gr, "currentColor", 1.5, "", .45, check=False)
    b += person(x, gr, s)
    ya = gr - 62 * s
    x1, x2 = x + 34, x + 34 + KV * v
    b += arrow("f1", "g", x1, ya, x2, ya, 3.2, name=f"v {ten}")
    b += text(x2 + 12, ya + 5, mo_ta, GRN, 14, "start")
    b += text(x + 22, gr - 100 * s + 5, ten, "currentColor", 14, "start")
    b += text(x1 + 4, ya + 22, "v", GRN, 16, "start", "700", True)
assert abs(KV * V_NHO / (KV * V_LON) - 2) < 1e-9
fig1 = wrap(f"0 0 {VB[1][0]} {VB[1][1]}",
            "Hai người trượt băng lướt cùng chiều: bạn nhỏ nhẹ lướt nhanh, người lớn nặng lướt chậm; mũi tên vận tốc dài gấp đôi nhau", b,
            "Hình 1. Bạn nhỏ nhẹ nhưng nhanh, người lớn nặng nhưng chậm (mũi tên xanh lá dài theo tỉ lệ tốc độ). Ai khó dừng hơn?")

# ---------------- Hình 2: cộng hai vector động lượng theo quy tắc hình bình hành ----------------
CUR["fig"] = 2
VB[2] = (440, 190)
b = defs("f2")
O = (60, 150)
P1, P2, AL = 150.0, 110.0, math.radians(60)      # px (vẽ theo tỉ lệ), góc giữa hai vector
e1 = (O[0] + P1, O[1])
e2 = (O[0] + P2 * math.cos(AL), O[1] - P2 * math.sin(AL))
es = (e1[0] + e2[0] - O[0], e1[1] + e2[1] - O[1])
b += line(e1[0], e1[1], es[0], es[1], "currentColor", 1.4, "5 4", .7, name="song song p2")
b += line(e2[0], e2[1], es[0], es[1], "currentColor", 1.4, "5 4", .7, name="song song p1")
b += arrow("f2", "r", *O, *e1, 3, name="p1")
b += arrow("f2", "b", *O, *e2, 3, name="p2")
b += arrow("f2", "g", *O, *es, 3.2, name="p hệ")
ar = 30
b += (f'<path d="M{O[0]+ar},{O[1]} A{ar},{ar} 0 0 0 {O[0]+ar*math.cos(AL):.1f},{O[1]-ar*math.sin(AL):.1f}" '
      f'fill="none" stroke="currentColor" stroke-width="1.4"/>')
b += text(O[0] + 45 * math.cos(math.radians(42)), O[1] - 45 * math.sin(math.radians(42)) + 5, "α", "currentColor", 15, "start", "700", True)
b += text(O[0] + P1 / 2, O[1] + 24, sub("p", "1"), RED, 16, "middle", "700")
b += text((O[0] + e2[0]) / 2 - 10, (O[1] + e2[1]) / 2, sub("p", "2"), BLUE, 16, "end", "700")
b += text(es[0] + 8, es[1] - 4, sub("p", "hệ"), GRN, 16, "start", "700")
# kiểm: đường chéo đúng định lí hàm cos
assert abs(math.dist(O, es) ** 2 - (P1 ** 2 + P2 ** 2 + 2 * P1 * P2 * math.cos(AL))) < 1e-6
fig2 = wrap(f"0 0 {VB[2][0]} {VB[2][1]}",
            "Hai vector động lượng p1 và p2 hợp góc alpha, động lượng của hệ là đường chéo hình bình hành", b,
            "Hình 2. Động lượng của hệ là đường chéo hình bình hành dựng trên $\\vec p_1$, $\\vec p_2$ (xanh lá). "
            "Góc $\\alpha$ giữa hai vector quyết định công thức tính độ lớn.")

# ---------------- Hình 3: đồ thị F–t, mặt cứng và đệm mềm, cùng diện tích Δp ----------------
CUR["fig"] = 3
VB[3] = (440, 250)
b = defs("f3")
DP, T_C, T_M = 0.45, 0.010, 0.040             # khớp tn-l10-dongluong-03
OX, OY, ST, SF = 60, 210, 6800.0, 2.1          # px/s, px/N
FC, FM = math.pi * DP / (2 * T_C), math.pi * DP / (2 * T_M)
b += arrow("f3", "k", OX, OY, 420, OY, 2, name="trục t") + arrow("f3", "k", OX, OY, OX, 20, 2, name="trục F")


def xung(T, Fm, col, op):
    pts = [(OX + ST * T * i / 60, OY - SF * Fm * math.sin(math.pi * i / 60)) for i in range(61)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        SEGS.append((3, xa, ya, xb, yb, "xung"))
    return f'<path d="{d}" fill="{col}" fill-opacity="{op}" stroke="{col}" stroke-width="2.4"/>'


b += xung(T_M, FM, BLUE, .25) + xung(T_C, FC, RED, .3)
for T in (T_C, T_M):
    x = OX + ST * T
    b += line(x, OY - 4, x, OY + 4, "currentColor", 1.5, check=False)
b += text(OX + ST * T_C, OY + 22, "0,01", "currentColor", 14, "middle", "500")
b += text(OX + ST * T_M, OY + 22, "0,04", "currentColor", 14, "middle", "500")
b += text(OX - 8, OY + 22, "0", "currentColor", 14, "end", "500")
b += text(420, OY - 10, "t (s)", "currentColor", 14, "end")
b += text(OX + 8, 30, "F", "currentColor", 16, "start", "700", True)
b += text(OX + ST * T_C / 2 + 26, OY - SF * FC + 14, "mặt cứng", RED, 14, "start")
b += text(OX + ST * T_M / 2, OY - SF * FM - 12, "đệm mềm", BLUE, 14, "middle")
b += text(290, 90, "hai diện tích", "currentColor", 14, "middle")
b += text(290, 108, "bằng nhau = Δp", "currentColor", 14, "middle")
# kiểm: diện tích hai xung bằng nhau và bằng Δp (tích phân số)
for T, Fm in ((T_C, FC), (T_M, FM)):
    S = sum(Fm * math.sin(math.pi * (i + .5) / 4000) * T / 4000 for i in range(4000))
    assert abs(S - DP) < 1e-4, (T, S)
fig3 = wrap(f"0 0 {VB[3][0]} {VB[3][1]}",
            "Đồ thị lực theo thời gian: xung hẹp và cao trên mặt cứng, xung thấp và rộng trên đệm mềm, hai diện tích bằng nhau", b,
            "Hình 3. Cùng một vật dừng lại với cùng $\\Delta p$ (vẽ cho $0{,}45\\ \\text{kg}\\cdot\\text{m/s}$). Mặt cứng: $\\Delta t$ ngắn, lực cao (đỏ). "
            "Đệm mềm: $\\Delta t$ dài gấp 4, lực thấp gấp 4 (xanh). Diện tích dưới đồ thị là xung lượng.")
fig3 = fig3.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-dongluong-03"', 1)

# ---------------- Hình 4: vector p trước, p sau, Δp của bài toán mẫu ----------------
CUR["fig"] = 4
VB[4] = (440, 250)
b = defs("f4")
m4, v1, v2 = 0.45, 12.0, -8.0
p1, p2 = m4 * v1, m4 * v2
dp4 = p2 - p1
K = 25.0                                    # px/(kg·m/s)
WX = 405
b += line(WX, 15, WX, 125, "currentColor", 3, name="tường")
for yy in range(20, 125, 14):
    b += line(WX, yy, WX + 14, yy - 10, "currentColor", 1.2, "", .6, check=False)
b += f'<circle cx="{WX-11}" cy="45" r="10" fill="rgba(251,146,60,.25)" stroke="currentColor" stroke-width="2"/>'
x_end = WX - 24
b += arrow("f4", "r", x_end - K * p1, 45, x_end, 45, 3, name="p1")
b += text(x_end - K * p1 - 10, 50, "trước: " + sub("p", "1"), RED, 14, "end")
b += arrow("f4", "b", x_end, 100, x_end + K * p2, 100, 3, name="p2")       # p2 < 0: hướng sang trái
b += text(x_end + K * p2 - 10, 105, "sau: " + sub("p", "2"), BLUE, 14, "end")
b += arrow("f4", "g", x_end, 170, x_end + K * dp4, 170, 3.4, name="Δp")
b += text(x_end + K * dp4 - 8, 175, "Δp", GRN, 16, "end", "700")
b += text(x_end, 198, "Δp = p₂ − p₁: ra xa tường", GRN, 14, "end")
b += arrow("f4", "k", 30, 232, 90, 232, 2, name="trục +")
b += text(98, 237, "chiều dương", "currentColor", 14, "start", "500")
assert p2 < 0 < p1 and dp4 < 0 and abs(K * abs(dp4) - (K * p1 + K * abs(p2))) < 1e-9
fig4 = wrap(f"0 0 {VB[4][0]} {VB[4][1]}",
            "Bóng đập tường: vector động lượng trước hướng vào tường, sau hướng ra; vector delta p hướng ra xa tường, dài bằng tổng hai vector", b,
            f"Hình 4. Vẽ theo tỉ lệ: $p_1 = {knum(p1)}$, $p_2 = {knum(abs(p2))}$ (ngược chiều), "
            f"$|\\Delta p| = {knum(abs(dp4))}\\ \\text{{kg}}\\cdot\\text{{m/s}}$ — dài bằng tổng hai mũi tên, không phải hiệu.")

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

# ---------------- Bảng số liệu + nhận xét: lấy từ tn-01, tính lại ----------------
tn1 = json.loads((ROOT / "content/thi-nghiem/tn-l10-dongluong-01.json").read_text(encoding="utf8"))
m1 = next(t["gia_tri"] for t in tn1["tham_so"] if t["ky_hieu"] == "m")
rows = tn1["so_lieu_mau"]["hang"]
BANG = "\n".join(f"<tr><td>{num(a, 2)}</td><td>{num(b_, 2).replace('-', '−')}</td><td>{num(c, 3)}</td></tr>" for a, b_, c in rows)
dps = [m1 * abs(b_ - a) for a, b_, _ in rows]
rel = [abs(d - c) / d for d, (_, _, c) in zip(dps, rows)]
bound = [m1 * 0.02 + 0.02 * c for _, _, c in rows]          # cổng quang ±0,01 m/s mỗi lần đo + cảm biến ±2 %
assert all(abs(d - c) <= bd for d, (_, _, c), bd in zip(dps, rows, bound))
assert all(c < d for d, (_, _, c) in zip(dps, rows))
rmax = max(rel)
lan_max = [i + 1 for i, r in enumerate(rel) if abs(r - rmax) < 1e-6]
assert lan_max == [1], lan_max
NX = (f"$|\\Delta p|$ tính từ cổng quang: {'; '.join(num(d, 4 if round(d, 3) != round(d, 4) else 3) for d in dps)} $\\text{{kg}}\\cdot\\text{{m/s}}$. "
      f"So với số cảm biến, chênh {num(100 * min(rel), 1)}–{num(100 * max(rel), 1)} %: khớp $\\Delta p = F\\Delta t$.</p>"
      f"<p>Sai số dụng cụ: mỗi tốc độ sai $\\pm 0{{,}}01\\ \\text{{m/s}}$ nên $\\Delta p$ sai cỡ $\\pm 0{{,}}005$; cảm biến sai $\\pm 2\\,\\%$. "
      f"Mọi chênh lệch đều nhỏ hơn tổng hai sai số (cảm biến $\\pm 2\\,\\%$ và cổng quang $\\pm 0{{,}}005$). Lần 1 chênh tương đối lớn nhất ({num(100 * rel[0], 1)} %) vì $\\Delta p$ nhỏ nhất. "
      f"Cả 4 lần cảm biến đều <strong>nhỏ hơn</strong> một chút: đó là sai số hệ thống (cảm biến lấy mẫu sót phần đầu, cuối của xung), không phải ngẫu nhiên.")
print("Δp:", [round(d, 4) for d in dps], "chênh %:", [round(100 * r, 2) for r in rel])

# ---------------- Thử thách ⭐⭐⭐: tính từ số ----------------
M5, H5, T5, TBT = 60, 5, 0.50, 0.010
v5 = math.sqrt(2 * G * H5)
F_dem = M5 * v5 / T5 + M5 * G
F_bt = M5 * v5 / TBT + M5 * G
F_NET = format(round(M5 * v5 / T5), ",d").replace(",", "\\,")
DA = (f"$v = \\sqrt{{2gh}} \\approx {knum(v5)}\\ \\text{{m/s}}$; $(N - mg)\\Delta t = mv$ ⇒ "
      f"$N \\approx {F_NET} + {round(M5 * G):d} \\approx {knum(F_dem / 1000)}\\cdot 10^3\\ \\text{{N}}$; "
      f"bê tông: $N \\approx {knum(F_bt / 1e4)}\\cdot 10^4\\ \\text{{N}}$, lớn gấp khoảng ${round(F_bt / F_dem)}$ lần")
print("⭐⭐⭐:", round(v5, 2), round(F_dem), round(F_bt))

src = (HERE / "theory.src.html").read_text(encoding="utf8")
for k, v in {"__BANG__": BANG, "__NHANXET__": NX, "__M__": f"${M5}\\ \\text{{kg}}$", "__H__": f"${H5}\\ \\text{{m}}$",
             "__T__": f"${knum(T5, 2)}\\ \\text{{s}}$", "__TBT__": f"${knum(TBT, 2)}\\ \\text{{s}}$", "__DAP_AN__": DA}.items():
    assert k in src, k
    src = src.replace(k, v)

# ---------------- Ghép hình ----------------
figs = [re.sub(r"<figcaption>Hình \d\.", f"<figcaption>Hình {k}.", f) for k, f in enumerate((fig1, fig2, fig3, fig4), 1)]
order = [int(k) for k in re.findall(r"<!--FIG(\d)-->", src)]
assert order == sorted(order) == list(range(1, len(figs) + 1)), order
for k, f in enumerate(figs, 1):
    src = src.replace(f"<!--FIG{k}-->", f)

lint = ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = HERE / "theory.html"
out.write_text(src.replace("__PHUT__", "?"), encoding="utf8")
r = subprocess.run([sys.executable, str(lint), str(out), "--json"], capture_output=True, text=True)
mm = re.search(r'"phut"\s*:\s*([\d.]+)', r.stdout)
phut = math.ceil(float(mm.group(1))) if mm else "?"
out.write_text(src.replace("__PHUT__", str(phut)), encoding="utf8")
print("ok", len(src), "ký tự; phút =", phut, "(lint:", mm.group(1) if mm else "?", ")")
if bad:
    sys.exit(1)
