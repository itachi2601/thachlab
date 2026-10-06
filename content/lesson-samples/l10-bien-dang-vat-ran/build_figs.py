"""Sinh 5 hình SVG + bảng số liệu thí nghiệm đo k cho bài 'Biến dạng của vật rắn' (lesson 78), thay mốc
<!--FIGn-->, __BANG_TN2__, __NHAN_XET_TN2__, __PHUT__ trong theory.src.html -> theory.html.
Chạy: python3 build_figs.py (từ thư mục bài hoặc gốc repo).
Mọi toạ độ tính từ số liệu vật lí (thang cm -> px, k, F); in kiểm: nhãn không chồng nhau, không vượt viewBox,
không bị nét/vật cản cắt xuyên; chấm số liệu nằm trên đường Hooke; mũi tên lực đúng chiều."""
import math, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import RED, BLUE, ORG, GRN, wrap  # noqa: E402

COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}
LABELS = []   # (fig, x0, y0, x1, y1, text)
SEGS = []     # (fig, x1, y1, x2, y2, tên) — nét không được cắt xuyên nhãn
BOXES = []    # (fig, x0, y0, x1, y1, tên) — vật cản (lò xo, vật, tường) không được đè nhãn
CHECKS = []
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


def it(s):
    return f'<tspan font-style="italic" font-family="serif">{s}</tspan>'


def sub(base, s):
    return f'{base}<tspan baseline-shift="sub" font-size="13">{s}</tspan>'


def text(x, y, s, c="currentColor", size=17, anchor="start", weight="700"):
    assert size >= 17, s
    plain = re.sub(r"<[^>]+>", "", s)
    w = 0.58 * size * len(plain)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    LABELS.append((CUR["fig"], x0, y - 0.75 * size, x0 + w, y + 0.25 * size, plain))
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}">{s}</text>')


def spring_v(x, y0, y1, n=9, amp=10, name="lò xo"):
    """Lò xo thẳng đứng từ y0 xuống y1: 2 đoạn thẳng ngắn ở hai đầu + n vòng răng cưa."""
    lead = 8
    a, b = y0 + lead, y1 - lead
    pts = [(x, y0), (x, a)]
    for i in range(1, 2 * n):
        pts.append((x + (amp if i % 2 else -amp), a + (b - a) * i / (2 * n)))
    pts += [(x, b), (x, y1)]
    BOXES.append((CUR["fig"], x - amp, y0, x + amp, y1, name))
    d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    return f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>'


def spring_h(x0, x1, y, n=8, amp=10, name="lò xo"):
    lead = 8
    a, b = x0 + lead, x1 - lead
    pts = [(x0, y), (a, y)]
    for i in range(1, 2 * n):
        pts.append((a + (b - a) * i / (2 * n), y + (amp if i % 2 else -amp)))
    pts += [(b, y), (x1, y)]
    BOXES.append((CUR["fig"], x0, y - amp, x1, y + amp, name))
    d = "M" + " L".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    return f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>'


def rect(x, y, w, h, fill, name, rx=3):
    BOXES.append((CUR["fig"], x, y, x + w, y + h, name))
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" '
            f'stroke="currentColor" stroke-width="2"/>')


def bag(cx, top, name):
    """Túi cam: quai + thân, đỉnh quai tại (cx, top)."""
    BOXES.append((CUR["fig"], cx - 17, top, cx + 17, top + 40, name))
    return (f'<path d="M{cx-8:.1f},{top+10:.1f} Q{cx:.1f},{top-4:.1f} {cx+8:.1f},{top+10:.1f}" fill="none" '
            f'stroke="currentColor" stroke-width="2"/>'
            f'<rect x="{cx-17:.1f}" y="{top+10:.1f}" width="34" height="30" rx="6" fill="rgba(251,146,60,.35)" '
            f'stroke="currentColor" stroke-width="2"/>')


# ---------------- Số liệu thí nghiệm đo k (dùng chung cho bảng, Hình 4, build_thi_nghiem.py) ----------------
G_TN2, K_TN2, L0_TN2, M1 = 9.8, 25.0, 10.0, 0.050
L_DO = [11.9, 13.9, 15.9, 17.9, 19.8]           # cm, đọc trên thước mm (±0,1 cm), minh hoạ
TN2 = []
for i, l in enumerate(L_DO, 1):
    F = round(i * M1 * G_TN2, 2)
    dl = round(l - L0_TN2, 1)
    dl_model = F / K_TN2 * 100
    assert abs(dl - dl_model) <= 0.1 + 1e-9, (i, dl, dl_model)        # số "đo" nằm trong sai số đọc thước
    TN2.append((F, l, dl, F / (dl / 100)))
K_TB = sum(r[3] for r in TN2) / len(TN2)
LECH = [abs(r[3] - K_TB) for r in TN2]
MAX_LECH = [i for i, d in enumerate(LECH) if abs(d - max(LECH)) < 1e-6]
assert MAX_LECH == [0], MAX_LECH                                    # nhận xét: hàng 1 lệch nhiều nhất, duy nhất
assert TN2[0][2] == min(r[2] for r in TN2)                          # ... và đó là hàng có Δl nhỏ nhất
REL1 = 0.1 / TN2[0][2]                                               # sai số tương đối đọc thước ở hàng 1


def vn(x, n=2):
    s = f"{x:.{n}f}".rstrip("0").rstrip(".") if n else f"{x:.0f}"
    return s.replace(".", "{,}")


bang = "\n".join(f"<tr><td>${vn(F)}$</td><td>${vn(l, 1)}$</td><td>${vn(dl, 1)}$</td></tr>" for F, l, dl, _ in TN2)
ks = "; ".join(f"${vn(r[3], 1)}$" for r in TN2)
nhan_xet = (f"Năm tỉ số $F/\\left|\\Delta l\\right|$ (N/m): {ks}. Trung bình $k \\approx {vn(K_TB, 1)}\\ \\text{{N/m}}$, "
            f"các hàng lệch nhau không quá $3\\,\\%$: lực tỉ lệ thuận với độ dãn. "
            f"Hàng đầu lệch nhiều nhất (${vn(TN2[0][3], 1)}$): độ dãn nhỏ nhất ($1{{,}}9\\ \\text{{cm}}$) nên sai số đọc thước "
            f"$\\pm 0{{,}}1\\ \\text{{cm}}$ chiếm tới khoảng ${vn(REL1 * 100, 0)}\\,\\%$. Muốn $k$ chính xác hơn, dùng các hàng dãn nhiều.")
assert max(abs(r[3] / K_TB - 1) for r in TN2) < 0.03

# ---------------- Hình 1: ba lò xo treo (mở bài, không lộ đáp án) ----------------
CUR["fig"] = 1
VB[1] = (420, 290)
TOP, PX = 34, 6.0                     # mép giá treo, px mỗi cm
b = defs("f1")
b += line(24, TOP, 396, TOP, "currentColor", 4)
BOXES.append((1, 24, TOP - 3, 396, TOP + 3, "giá"))
cols = [(96, 20.0, 0), (236, 22.0, 1)]
for x, L, nb in cols:
    y1 = TOP + L * PX
    b += spring_v(x, TOP, y1)
    if nb:
        b += bag(x, y1, "túi")
    # đường kích thước bên trái lò xo
    dx = x - 26
    b += line(dx, TOP, dx, y1, "currentColor", 1.3, name=f"kt{L}")
    b += line(dx - 5, y1, dx + 5, y1, "currentColor", 1.3)
    b += text(dx - 6, (TOP + y1) / 2 + 6, f"{L:.0f} cm", anchor="end", weight="600")
assert abs((cols[1][1] - cols[0][1]) * PX - 12) < 1e-9          # 2 cm dãn thêm -> 12 px
b += text(96, 246, "chưa treo", anchor="middle", weight="600")
b += text(236, 246, "1 túi 200 g", anchor="middle", weight="600")
# cột 3: chỉ có câu hỏi, KHÔNG vẽ lò xo (vẽ ra là lộ đáp án)
b += f'<circle cx="352" cy="{TOP + 4}" r="5" fill="none" stroke="currentColor" stroke-width="2"/>'
b += text(352, 130, "?", ORG, 40, "middle")
b += text(352, 246, "2 túi 400 g", anchor="middle", weight="600")
b += text(352, 270, "dài ? cm", ORG, 17, "middle", "600")
fig1 = wrap(f"0 0 {VB[1][0]} {VB[1][1]}",
            "Lò xo treo thẳng đứng: chưa treo dài 20 cm, treo một túi 200 g dài 22 cm, treo hai túi chưa biết dài bao nhiêu",
            b, "Hình 1. Cùng một lò xo: chưa treo gì, treo một túi cam, và câu hỏi khi treo hai túi.")
fig1 = fig1.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-biendang-04"', 1)

# ---------------- Hình 2: thanh ban đầu / bị nén / bị kéo ----------------
CUR["fig"] = 2
VB[2] = (420, 250)
X0, X1 = 150, 270                     # hai đầu thanh khi chưa biến dạng
b = defs("f2")
rows = [("Ban đầu: chưa có lực", 28, 40, X0, X1, 30, None),
        ("Nén: cặp lực hướng vào trong vật", 108, 120, X0 + 15, X1 - 15, 36, "in"),
        ("Kéo: cặp lực hướng ra ngoài vật", 188, 200, X0 - 10, X1 + 10, 24, "out")]
for lab, ly, by, a, c, h, kind in rows:
    b += text(12, ly, lab, size=17, weight="700")
    yc = by + 15
    top = yc - h / 2
    b += rect(a, top, c - a, h, "rgba(56,189,248,.18)", "thanh")
    for xg in (X0, X1):              # vạch đứt: vị trí hai đầu lúc chưa biến dạng
        b += line(xg, by - 6, xg, by + 36, "currentColor", 1.2, "3 4", .55)
    if kind == "in":
        b += arrow("f2", "r", a - 62, yc, a - 3, yc, 3, name="Fn1")
        b += arrow("f2", "r", c + 62, yc, c + 3, yc, 3, name="Fn2")
        assert a - 62 < a - 3 and c + 62 > c + 3            # hai mũi hướng VÀO thanh
    elif kind == "out":
        b += arrow("f2", "r", a - 1, yc, a - 60, yc, 3, name="Fk1")
        b += arrow("f2", "r", c + 1, yc, c + 60, yc, 3, name="Fk2")
assert rows[1][4] - rows[1][3] < X1 - X0 < rows[2][4] - rows[2][3]  # nén ngắn hơn, kéo dài hơn ban đầu
fig2 = wrap(f"0 0 {VB[2][0]} {VB[2][1]}",
            "Ba thanh: chưa có lực; bị nén bởi cặp lực hướng vào nên ngắn lại; bị kéo bởi cặp lực hướng ra nên dài ra",
            b, "Hình 2. Vạch đứt đánh dấu hai đầu thanh lúc chưa có lực. Lực (đỏ) vuông góc với hai mặt đầu: "
               "hướng vào thì thanh ngắn lại, hướng ra thì thanh dài ra.")

# ---------------- Hình 3: chiều lực đàn hồi khi dãn / nén ----------------
CUR["fig"] = 3
VB[3] = (420, 262)
WALL, NAT = 34, 180                   # mặt tường, vị trí đầu lò xo khi chưa biến dạng
b = defs("f3")
b += (f'<rect x="14" y="40" width="{WALL-14}" height="210" fill="rgba(148,163,184,.3)" stroke="currentColor" '
      f'stroke-width="2"/>')
BOXES.append((3, 14, 40, WALL, 250, "tường"))
for title, y, end, kind in (("Lò xo dãn: lực đàn hồi kéo vào", 28, 240, "dan"),
                            ("Lò xo nén: lực đàn hồi đẩy ra", 150, 120, "nen")):
    yc = y + 44
    b += text(44, y, title, size=17)
    b += spring_h(WALL, end, yc, n=8 if kind == "dan" else 7)
    b += rect(end, yc - 12, 16, 24, "rgba(251,146,60,.45)", "đầu cầm", rx=3)
    b += line(NAT, yc - 26, NAT, yc - 14, "currentColor", 1.4, "3 3", .7)
    b += line(NAT, yc + 14, NAT, yc + 18, "currentColor", 1.4, "3 3", .7)
    if kind == "dan":
        assert end > NAT                                  # dãn: đầu lò xo ở xa hơn vị trí tự nhiên
        b += arrow("f3", "r", end + 18, yc, end + 78, yc, 3.2, name="tay kéo")
        b += text(end + 22, yc - 18, "tay kéo", RED, 17, weight="600")
        # lực đàn hồi lên tay: hướng về phía tường (kéo vào), đặt ở đầu lò xo
        b += arrow("f3", "b", end + 8, yc + 30, end - 56, yc + 30, 3.2, name="Fđh dãn")
        assert end - 56 < end + 8                           # mũi chĩa về tường
        b += text(end - 62, yc + 36, sub(it("F"), "đh"), BLUE, 19, "end")
    else:
        assert end < NAT                                  # nén: đầu lò xo gần tường hơn vị trí tự nhiên
        b += arrow("f3", "r", end + 86, yc, end + 20, yc, 3.2, name="tay đẩy")
        b += text(end + 50, yc - 18, "tay đẩy", RED, 17, weight="600")
        b += arrow("f3", "b", end + 8, yc + 30, end + 72, yc + 30, 3.2, name="Fđh nén")
        assert end + 72 > end + 8                           # mũi chĩa ra xa tường
        b += text(end + 80, yc + 36, sub(it("F"), "đh"), BLUE, 19)
fig3 = wrap(f"0 0 {VB[3][0]} {VB[3][1]}",
            "Lò xo gắn tường. Khi bị kéo dãn, lực đàn hồi lên tay hướng về phía tường; khi bị nén, lực đàn hồi lên tay hướng ra xa tường",
            b, "Hình 3. Vạch đứt là vị trí đầu lò xo khi chưa biến dạng. Lực đàn hồi (xanh) đặt lên vật ở đầu lò xo, "
               "luôn ngược chiều biến dạng: dãn thì kéo vào, nén thì đẩy ra.")

# ---------------- Hình 4: đồ thị F theo Δl, số liệu đo + giới hạn đàn hồi ----------------
CUR["fig"] = 4
VB[4] = (420, 310)
OX, OY, SX, SY = 60, 250, 20.0, 50.0  # gốc; px/cm; px/N
def P4(dl, F):
    return OX + dl * SX, OY - F * SY
b = defs("f4")
b += arrow("f4", "k", OX, OY, 400, OY, 1.8, name="trục x") + arrow("f4", "k", OX, OY, OX, 26, 1.8, name="trục y")
for c in (4, 8, 12, 16):
    x, _ = P4(c, 0)
    b += line(x, OY, x, OY + 6, "currentColor", 1.4)
    b += text(x, OY + 26, str(c), anchor="middle", weight="500")
for f in (1, 2, 3, 4):
    _, y = P4(0, f)
    b += line(OX - 6, y, OX, y, "currentColor", 1.4)
    b += text(OX - 10, y + 6, str(f), anchor="end", weight="500")
b += text(OX + 8, 40, it("F") + " (N)", weight="600")
b += text(408, OY + 50, "Δ" + it("l") + " (cm)", anchor="end", weight="600")
b += text(OX - 10, OY + 22, "O", anchor="end", weight="600")
DLA, FA = 12.0, K_TN2 * 12.0 / 100     # điểm A: giới hạn đàn hồi (minh hoạ), trên đường k = 25 N/m
assert abs(FA - 3.0) < 1e-9
xa, ya = P4(DLA, FA)
b += line(OX, OY, xa, ya, BLUE, 3, name="OA")
# đoạn vượt giới hạn: cong xuống dưới đường thẳng kéo dài (lực tăng chậm hơn tỉ lệ)
CTRL, END = P4(14.0, 3.35), P4(16.0, 3.45)
b += f'<path d="M{xa:.1f},{ya:.1f} Q{CTRL[0]:.1f},{CTRL[1]:.1f} {END[0]:.1f},{END[1]:.1f}" fill="none" stroke="{RED}" stroke-width="3" stroke-dasharray="7 5"/>'
for i in range(9):                       # nét cong để kiểm nhãn
    t0, t1 = i / 9, (i + 1) / 9
    q = lambda t: ((1 - t) ** 2 * xa + 2 * t * (1 - t) * CTRL[0] + t * t * END[0],
                   (1 - t) ** 2 * ya + 2 * t * (1 - t) * CTRL[1] + t * t * END[1])
    SEGS.append((4, *q(t0), *q(t1), "cong"))
    yline = OY - (q(t1)[0] - OX) / SX * K_TN2 / 100 * SY
    assert q(t1)[1] > yline - 1e-6       # đoạn cong nằm DƯỚI đường thẳng kéo dài
for F, l, dl, _ in TN2:                  # chấm số liệu đo phải nằm trên đường (lệch ≤ sai số đọc 0,1 cm = 2 px)
    x, y = P4(dl, F)
    xl = OX + F / K_TN2 * 100 * SX
    assert abs(x - xl) <= 0.1 * SX + 1e-6, (F, x, xl)
    b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{ORG}" stroke="currentColor" stroke-width="1.2"/>'
b += f'<circle cx="{xa:.1f}" cy="{ya:.1f}" r="5" fill="currentColor"/>'
b += text(xa - 6, ya - 12, "A", anchor="end")
b += text(100, 60, "A: giới hạn đàn hồi", weight="600")
b += text(180, 216, "OA: F tỉ lệ Δl", BLUE, 17, weight="600")
b += text(282, 150, "vượt giới hạn", RED, 17, weight="600")
fig4 = wrap(f"0 0 {VB[4][0]} {VB[4][1]}",
            "Đồ thị lực theo độ dãn: năm chấm số liệu đo nằm trên đoạn thẳng OA qua gốc; sau điểm A là giới hạn đàn hồi, đường cong không còn thẳng",
            b, "Hình 4. Chấm cam: năm lần đo ở bảng trên, nằm trên đoạn thẳng OA (độ cứng khoảng 25 N/m). "
               "Sau A (minh hoạ), lò xo vượt giới hạn đàn hồi, lực không còn tỉ lệ với độ dãn.")
fig4 = fig4.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-biendang-02"', 1)

# ---------------- Hình 5: hai lò xo, hai độ cứng ----------------
CUR["fig"] = 5
VB[5] = (420, 300)
OX5, OY5, SX5, SY5 = 60, 240, 40.0, 60.0   # px/cm, px/N
K1, K2 = 50.0, 25.0
def P5(dl, F):
    return OX5 + dl * SX5, OY5 - F * SY5
b = defs("f5")
b += arrow("f5", "k", OX5, OY5, 400, OY5, 1.8, name="trục x") + arrow("f5", "k", OX5, OY5, OX5, 30, 1.8, name="trục y")
for c in (2, 4, 6, 8):
    x, _ = P5(c, 0)
    b += line(x, OY5, x, OY5 + 6, "currentColor", 1.4)
    b += text(x, OY5 + 26, str(c), anchor="middle", weight="500")
for f in (1, 2, 3):
    _, y = P5(0, f)
    b += line(OX5 - 6, y, OX5, y, "currentColor", 1.4)
    b += text(OX5 - 10, y + 6, str(f), anchor="end", weight="500")
b += text(OX5 + 8, 44, it("F") + " (N)", weight="600")
b += text(408, OY5 + 46, "Δ" + it("l") + " (cm)", anchor="end", weight="600")
e1 = P5(3.0 / K1 * 100, 3.0)              # lò xo 1 tới F = 3 N (Δl = 6 cm)
e2 = P5(8.0, K2 * 8 / 100)                # lò xo 2 tới Δl = 8 cm (F = 2 N)
assert abs(e1[0] - P5(6, 0)[0]) < 1e-9 and abs(e2[1] - P5(0, 2)[1]) < 1e-9
b += line(OX5, OY5, *e1, RED, 3, name="lx1") + line(OX5, OY5, *e2, BLUE, 3, name="lx2")
# cùng F = 1 N: Δl1 = 2 cm, Δl2 = 4 cm
F0 = 1.0
q1, q2 = P5(F0 / K1 * 100, F0), P5(F0 / K2 * 100, F0)
assert abs(F0 / K1 * 100 - 2) < 1e-9 and abs(F0 / K2 * 100 - 4) < 1e-9
b += line(OX5, q1[1], q2[0], q2[1], "currentColor", 1.3, "4 4", .7, name="F=1")
for q in (q1, q2):
    b += line(q[0], q[1], q[0], OY5, "currentColor", 1.3, "4 4", .7, name="dóng")
    b += f'<circle cx="{q[0]:.1f}" cy="{q[1]:.1f}" r="5" fill="currentColor"/>'
b += text(96, 64, "lò xo 1: k = 50 N/m", RED, 17, weight="600")
b += text(300, 200, "lò xo 2:", BLUE, 17, weight="600")
b += text(300, 220, "k = 25 N/m", BLUE, 17, weight="600")
fig5 = wrap(f"0 0 {VB[5][0]} {VB[5][1]}",
            "Đồ thị lực theo độ dãn của hai lò xo: lò xo 1 dốc hơn, độ cứng 50 N/m; lò xo 2 thoải hơn, độ cứng 25 N/m; cùng lực 1 N lò xo 1 dãn 2 cm, lò xo 2 dãn 4 cm",
            b, "Hình 5. Mỗi lò xo là một đường thẳng riêng, độ dốc chính là độ cứng — không đổi dọc theo đường dù lực tăng. "
               "Cùng lực 1 N: lò xo cứng hơn dãn 2 cm, lò xo mềm hơn dãn 4 cm.")
fig5 = fig5.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-biendang-03"', 1)


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
    for g, a0, b0, a1, b1, nm in BOXES:
        if g == f and x0 < a1 and a0 < x1 and y0 < b1 and b0 < y1:
            bad.append(f"Hình {f}: vật '{nm}' đè nhãn '{s}'")
print("\n".join(bad) if bad else "kiểm toạ độ: ok")

src = (HERE / "theory.src.html").read_text(encoding="utf8")
figs = (fig1, fig2, fig3, fig4, fig5)
order = [int(n) for n in re.findall(r"<!--FIG(\d)-->", src)]
assert order == list(range(1, len(figs) + 1)), order
for n, f in enumerate(figs, 1):
    assert f"<figcaption>Hình {n}." in f, n
    src = src.replace(f"<!--FIG{n}-->", f)
src = src.replace("__BANG_TN2__", bang).replace("__NHAN_XET_TN2__", nhan_xet)
assert "__BANG" not in src and "__NHAN" not in src

lint = HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = HERE / "theory.html"
out.write_text(src.replace("__PHUT__", "?"), encoding="utf8")
r = subprocess.run([sys.executable, str(lint), str(out), "--json"], capture_output=True, text=True)
m = re.search(r'"phut"\s*:\s*([\d.]+)', r.stdout)
phut = math.ceil(float(m.group(1))) if m else "?"
out.write_text(src.replace("__PHUT__", str(phut)), encoding="utf8")
print("ok", len(src), "ký tự; phút =", phut, "; k_tb =", round(K_TB, 2), "; bảng:", [(r[0], r[1], r[2], round(r[3], 2)) for r in TN2])
if bad:
    sys.exit(1)
