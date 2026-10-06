"""Sinh 5 hình SVG cho Bài 34 'Khối lượng riêng. Áp suất chất lỏng' (lesson 79) và thay mốc <!--FIGn--> /
__BANG__ / __NHANXET__ / __DIENBUOC__ / __DOICHIEU__ / __S1..3__ / __PHUT__ trong theory.src.html -> theory.html.
Chạy: python3 build_thi_nghiem.py rồi python3 build_figs.py (từ thư mục bài hoặc gốc repo).
Tự kiểm: mọi số trong quiz/lời giải tính lại bằng Python (assert); hình tính từ vật lí (mực nước, độ dài mũi tên
tỉ lệ độ sâu, mũi tên chĩa đúng vào điểm); nhãn không chồng, không vượt viewBox, không bị nét cắt xuyên;
chữ ≥ 17, chỉ số dưới ≥ 13 (viewBox ≤ 420 rộng)."""
import json, math, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1].parent
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import RED, BLUE, ORG, GRN, wrap  # noqa: E402

COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}
LABELS, SEGS, VB, bad = [], [], {}, []
CUR = {"fig": 0}
G, RHO_N = 10, 1000
WATER = "rgba(56,189,248,.22)"
OIL = "rgba(251,146,60,.38)"


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1, abs(a), abs(b))


def num(v, d=1):
    return f"{v:.{d}f}".replace(".", ",")


def knum(v, d=1):
    return num(v, d).replace(",", "{,}")


def defs(p):
    out = "<defs>"
    for n, c in COL.items():
        out += (f'<marker id="{p}-{n}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="11" markerHeight="11" '
                f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
    return out + "</defs>"


def arrow(p, c, x1, y1, x2, y2, w=2.6, name="mũi tên"):
    SEGS.append((CUR["fig"], x1, y1, x2, y2, name))
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{COL[c]}" stroke-width="{w}" '
            f'marker-end="url(#{p}-{c})"/>')


def line(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, name="nét", check=True):
    if check:
        SEGS.append((CUR["fig"], x1, y1, x2, y2, name))
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def poly(pts, fill, stroke="none", w=0):
    s = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    st = f' stroke="{stroke}" stroke-width="{w}"' if stroke != "none" else ""
    return f'<polygon points="{s}" fill="{fill}"{st}/>'


def path(pts, w=2.4, check=True, name="thành bình"):
    if check:
        for (a, b), (c, d) in zip(pts, pts[1:]):
            SEGS.append((CUR["fig"], a, b, c, d, name))
    s = " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<path d="M{s}" fill="none" stroke="currentColor" stroke-width="{w}" stroke-linejoin="round"/>'


def sub(base, s):
    return f'{base}<tspan baseline-shift="sub" font-size="13">{s}</tspan>'


def it(s):
    return f'<tspan font-style="italic" font-family="serif">{s}</tspan>'


def text(x, y, s, c="currentColor", size=17, anchor="start", weight="700"):
    assert size >= 17
    plain = re.sub(r"<[^>]+>", "", s)
    w = 0.58 * size * len(plain)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    LABELS.append((CUR["fig"], x0, y - 0.75 * size, x0 + w, y + 0.25 * size, plain))
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}">{s}</text>')


def dim_v(x, y1, y2, tick=6, name="kích thước"):
    """Đường kích thước thẳng đứng có hai vạch ngang."""
    return (line(x, y1, x, y2, w=1.4, name=name) + line(x - tick, y1, x + tick, y1, w=1.4, check=False)
            + line(x - tick, y2, x + tick, y2, w=1.4, check=False))


def pressure_star(p, x, y, L, gap=6):
    """Bốn mũi tên chĩa VÀO điểm (x,y) từ bốn phía, dài L (tỉ lệ áp suất do nước)."""
    out = ""
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        x1, y1 = x + dx * (gap + L), y + dy * (gap + L)
        x2, y2 = x + dx * gap, y + dy * gap
        # mũi tên phải hướng về điểm
        assert (x2 - x1) * (x - x1) + (y2 - y1) * (y - y1) > 0 and math.hypot(x2 - x1, y2 - y1) - L < 1e-9
        out += arrow(p, "r", x1, y1, x2, y2, 2.6, name=f"áp lực tại ({x:.0f},{y:.0f})")
    return out


# ================= Hình 1: mở bài — bể bơi và hồ, cùng độ sâu 2 m (không vẽ áp suất) =================
CUR["fig"] = 1
VB[1] = (420, 235)
PXM = 50                         # px mỗi mét
SURF, DEPTH, BOT = 72, 2.0, 72 + 2.6 * PXM
b = defs("f1")
pool = [(22, 46), (22, BOT), (152, BOT), (152, 46)]
b += poly([(22, SURF), (22, BOT), (152, BOT), (152, SURF)], WATER) + path(pool, name="thành bể")
lake = [(184, 56), (218, BOT), (372, BOT), (406, 56)]
xl = lambda y: 184 + (218 - 184) * (y - 56) / (BOT - 56)      # bờ trái hồ
xr = lambda y: 406 - (406 - 372) * (y - 56) / (BOT - 56)      # bờ phải hồ
b += poly([(xl(SURF), SURF), (218, BOT), (372, BOT), (xr(SURF), SURF)], WATER) + path(lake, name="bờ hồ")
yp = SURF + DEPTH * PXM
for px, dx in ((58, 96), (268, 306)):
    b += f'<circle cx="{px}" cy="{yp:.1f}" r="6" fill="{ORG}" stroke="currentColor" stroke-width="1.5"/>'
    b += line(px + 8, yp, dx + 6, yp, w=1.2, dash="3 4", op=.7, check=False)
    b += dim_v(dx, SURF, yp, name="2 m")
    b += text(dx + 8, (SURF + yp) / 2 + 6, "2 m")
assert close((yp - SURF) / PXM, 2.0)
b += text(87, 30, "bể bơi", anchor="middle", weight="600")
b += text(295, 30, "hồ rộng", anchor="middle", weight="600")
fig1 = wrap(f"0 0 {VB[1][0]} {VB[1][1]}",
            "Mặt cắt một bể bơi hẹp và một hồ rộng; ở cả hai nơi có một điểm nằm sâu 2 m dưới mặt nước",
            b, "Hình 1. Cùng độ sâu 2 m dưới mặt nước: bên trái là bể bơi hẹp, bên phải là hồ rộng.")

# ================= Hình 2: áp suất tại M, N theo mọi phương; Δh =================
CUR["fig"] = 2
VB[2] = (420, 280)
X0, X1, TOP, SURF2, BOT2 = 22, 300, 30, 62, 264
hM, hN = 50, 130                   # độ sâu (px) của M, N dưới mặt thoáng
K = 0.4                            # px mũi tên / px độ sâu  (độ dài ∝ ρgh)
M = (150, SURF2 + hM)
N = (222, SURF2 + hN)
LM, LN = K * hM, K * hN
assert close(LN / LM, hN / hM)     # tỉ lệ đúng với áp suất do nước
assert N[1] + 6 + LN < BOT2 - 2 and M[0] - 6 - LM > X0 + 40
b = defs("f2")
b += poly([(X0, SURF2), (X0, BOT2), (X1, BOT2), (X1, SURF2)], WATER)
b += path([(X0, TOP), (X0, BOT2), (X1, BOT2), (X1, TOP)], name="thành bình")
b += pressure_star("f2", *M, LM) + pressure_star("f2", *N, LN)
for P_, lab in ((M, "M"), (N, "N")):
    b += f'<circle cx="{P_[0]}" cy="{P_[1]}" r="3.5" fill="currentColor"/>'
    b += text(P_[0] + 9, P_[1] - 10, it(lab), size=18)
# độ sâu h1 (M), h2 (N) đo từ mặt thoáng
b += line(58, N[1], N[0] - 6 - LN - 4, N[1], w=1.1, dash="3 4", op=.6, check=False)
b += dim_v(52, SURF2, N[1], name="h2") + text(60, (SURF2 + N[1]) / 2 + 22, sub(it("h"), "2"))
b += line(106, M[1], M[0] - 6 - LM - 4, M[1], w=1.1, dash="3 4", op=.6, check=False)
b += dim_v(100, SURF2, M[1], name="h1") + text(108, (SURF2 + M[1]) / 2 + 6, sub(it("h"), "1"))
# Δh bên phải bình
b += line(N[0] + 6 + LN + 4, N[1], 334, N[1], w=1.1, dash="3 4", op=.6, check=False)
b += line(M[0] + 6 + LM + 4, M[1], 334, M[1], w=1.1, dash="3 4", op=.6, check=False)
b += dim_v(328, M[1], N[1], name="Δh") + text(338, (M[1] + N[1]) / 2 + 6, "Δ" + it("h"))
b += text(306, SURF2 + 5, "mặt thoáng", weight="600")
fig2 = wrap(f"0 0 {VB[2][0]} {VB[2][1]}",
            "Bình nước có hai điểm M nông và N sâu; ở mỗi điểm bốn mũi tên chĩa vào từ bốn phía, mũi tên ở N dài hơn; ghi độ sâu h1, h2 và độ chênh Δh",
            b, "Hình 2. Ở mỗi điểm, nước ép như nhau theo mọi phương; mũi tên dài theo phần áp suất do nước. "
               "N sâu hơn M nên bị ép mạnh hơn; hiệu áp suất chỉ phụ thuộc độ chênh độ sâu.")
fig2 = fig2.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-klr-apsuat-03"', 1)

# ================= Hình 3: ống chữ U, nước + dầu (đọc hàng 10 cm của tn-04) =================
CUR["fig"] = 3
tn4 = json.loads((ROOT / "content/thi-nghiem/tn-l10-klr-apsuat-04.json").read_text(encoding="utf8"))
RHO_D = next(t for t in tn4["tham_so"] if t["ky_hieu"] == "rho_d")["mac_dinh"]
HD = 10                                      # cm cột dầu
HN = RHO_D * HD / RHO_N                      # cm cột nước tính từ mức mặt phân cách
assert [HD, HN, HD - HN] in [[a, b_, c] for a, b_, c in tn4["so_lieu_mau"]["hang"]]
assert close(RHO_D * HD, RHO_N * HN)
VB[3] = (420, 270)
SC = 12                                      # px / cm
LX0, LX1, RX0, RX1, IN_BOT, OUT_BOT, TOP3 = 96, 146, 254, 304, 214, 254, 28
YI = 190                                     # mặt phân cách dầu–nước (nhánh trái)
YOIL, YR = YI - HD * SC, YI - HN * SC        # mặt thoáng dầu (trái), mặt thoáng nước (phải)
assert YOIL < YR, "mặt dầu phải cao hơn mặt nước bên kia"
b = defs("f3")
b += poly([(LX0, YI), (LX1, YI), (LX1, IN_BOT), (RX0, IN_BOT), (RX0, YR), (RX1, YR), (RX1, OUT_BOT), (LX0, OUT_BOT)], WATER)
b += poly([(LX0, YOIL), (LX1, YOIL), (LX1, YI), (LX0, YI)], OIL)
b += path([(LX0, TOP3), (LX0, OUT_BOT), (RX1, OUT_BOT), (RX1, TOP3)], name="ống ngoài")
b += path([(LX1, TOP3), (LX1, IN_BOT), (RX0, IN_BOT), (RX0, TOP3)], name="ống trong")
b += line(LX0, YI, LX1, YI, ORG, 1.6, check=False)
# A (mặt phân cách) và B cùng mức ngang bên phải
A_, B_ = ((LX0 + LX1) / 2, YI), ((RX0 + RX1) / 2, YI)
b += line(A_[0], YI, B_[0], YI, w=1.2, dash="5 4", op=.75, name="mức ngang A–B")
for P_, lab, dx, anc in ((A_, "A", 32, "start"), (B_, "B", -32, "end")):
    b += f'<circle cx="{P_[0]:.1f}" cy="{P_[1]}" r="4" fill="currentColor"/>'
    b += text(P_[0] + dx, YI - 9, it(lab), size=18, anchor=anc)
b += text((LX0 + LX1) / 2, (YOIL + YI) / 2 - 4, "dầu", anchor="middle")
b += text((LX0 + LX1) / 2, (YOIL + YI) / 2 + 16, "hoả", anchor="middle")
b += text(200, 241, "nước", anchor="middle")
b += dim_v(76, YOIL, YI, name="cột dầu") + text(68, (YOIL + YI) / 2 + 6, f"{HD} cm", anchor="end")
b += dim_v(324, YR, YI, name="cột nước") + text(332, (YR + YI) / 2 + 6, f"{num(HN, 0)} cm")
fig3 = wrap(f"0 0 {VB[3][0]} {VB[3][1]}",
            "Ống chữ U: nhánh trái có cột dầu hoả 10 cm nằm trên nước, nhánh phải chỉ có nước cao 8 cm tính từ mức ngang của mặt phân cách; A và B cùng mức ngang",
            b, "Hình 3. Dầu hoả (cam) nổi trên nước ở nhánh trái. A và B cùng mức ngang, cùng nằm trong nước nên cùng áp suất: "
               "cột dầu hoả 10 cm cân với cột nước 8 cm, mặt dầu cao hơn mặt nước bên kia.")
fig3 = fig3.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-klr-apsuat-04"', 1)

# ================= Hình 4: ba bình khác hình dạng, cùng mực nước =================
CUR["fig"] = 4
VB[4] = (420, 245)
BASE4, SURF4, TOP4 = 200, 82, 56
H4 = BASE4 - SURF4
vessels = {"thẳng": ((28, 98), (28, 98)),        # (đáy trái, đáy phải), (miệng trái, miệng phải)
           "loe": ((168, 238), (138, 268)),
           "thắt": ((312, 382), (334, 360))}
b = defs("f4")
fills = []
for (bl, br), (tl, tr) in vessels.values():
    xl_ = lambda y, bl=bl, tl=tl: bl + (tl - bl) * (BASE4 - y) / (BASE4 - TOP4)
    xr_ = lambda y, br=br, tr=tr: br + (tr - br) * (BASE4 - y) / (BASE4 - TOP4)
    assert br - bl == 70                          # cùng diện tích đáy (bề rộng)
    b += poly([(xl_(SURF4), SURF4), (bl, BASE4), (br, BASE4), (xr_(SURF4), SURF4)], WATER)
    b += path([(tl, TOP4), (bl, BASE4), (br, BASE4), (tr, TOP4)], name="thành bình")
    fills.append(SURF4)
assert len(set(fills)) == 1                       # cùng mực nước
b += line(8, SURF4, 412, SURF4, w=1.1, dash="4 4", op=.55, check=False)
b += dim_v(118, SURF4, BASE4, name="h") + text(126, (SURF4 + BASE4) / 2 + 6, it("h"), size=18)
b += text(210, 228, "áp suất ở đáy như nhau", anchor="middle", weight="600")
b += text(210, 40, "cùng mực nước", anchor="middle", weight="600")
fig4 = wrap(f"0 0 {VB[4][0]} {VB[4][1]}",
            "Ba bình cùng diện tích đáy: thành thẳng, loe miệng và thắt miệng, nước cùng cao h; áp suất ở đáy ba bình như nhau",
            b, "Hình 4. Thành thẳng, loe miệng, thắt miệng: lượng nước khác nhau nhưng cùng độ sâu nên áp suất ở đáy như nhau.")

# ================= Hình 5: bể cá của bài toán mẫu =================
CUR["fig"] = 5
A5, B5, H5, HM5, PA5 = 0.60, 0.40, 0.50, 0.20, 1.0e5
VB[5] = (420, 262)
S5 = 3.6                                    # px / cm
TX0, BOT5 = 104, 212
TX1 = TX0 + A5 * 100 * S5
SURF5 = BOT5 - H5 * 100 * S5
TOP5 = SURF5 - 14
YM = BOT5 - HM5 * 100 * S5
XM = 236
assert close((BOT5 - SURF5) / S5, 50) and close((BOT5 - YM) / S5, 20) and close((TX1 - TX0) / S5, 60)
b = defs("f5")
b += poly([(TX0, SURF5), (TX0, BOT5), (TX1, BOT5), (TX1, SURF5)], WATER)
b += path([(TX0, TOP5), (TX0, BOT5), (TX1, BOT5), (TX1, TOP5)], name="thành bể")
b += f'<circle cx="{XM}" cy="{YM:.1f}" r="4" fill="currentColor"/>' + text(XM + 9, YM - 8, it("M"), size=18)
b += dim_v(84, SURF5, BOT5, name="50 cm") + text(76, (SURF5 + BOT5) / 2 + 6, "50 cm", anchor="end")
b += line(XM + 6, YM, 344, YM, w=1.1, dash="3 4", op=.6, check=False)
b += dim_v(338, YM, BOT5, name="20 cm") + text(346, (YM + BOT5) / 2 + 6, "20 cm")
b += (line(TX0, 228, TX1, 228, w=1.4, name="60 cm") + line(TX0, 222, TX0, 234, w=1.4, check=False)
      + line(TX1, 222, TX1, 234, w=1.4, check=False))
b += text((TX0 + TX1) / 2, 250, "60 cm", anchor="middle")
fig5 = wrap(f"0 0 {VB[5][0]} {VB[5][1]}",
            "Bể cá nhìn ngang: rộng 60 cm, nước cao 50 cm, điểm M cách đáy 20 cm",
            b, "Hình 5. Bể cá nhìn từ phía trước: mặt trước rộng 60 cm, nước cao 50 cm, điểm M cách đáy 20 cm.")
fig5 = fig5.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-klr-apsuat-05"', 1)


# ================= Kiểm toạ độ nhãn =================
def seg_hits_box(x1, y1, x2, y2, bx0, by0, bx1, by1):
    for i in range(101):
        t = i / 100
        x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        if bx0 < x < bx1 and by0 < y < by1:
            return True
    return False


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
for f, (W, H) in VB.items():
    assert W <= 420, f
print("\n".join(bad) if bad else "kiểm toạ độ: ok")

# ================= Kiểm số liệu quiz / lời giải (tính lại bằng Python) =================
# Câu 1: cưa đôi -> ρ không đổi (định tính). Câu 2: viên gạch
F2, S2 = 2 * G, 0.10 * 0.05
assert close(F2 / S2, 4000) and close(F2 / 50, 0.4) and close(2 / S2, 400) and close(F2 / (0.20 * 0.10), 1000)
# Câu 3: tầng 1 – tầng 5
assert close(RHO_N * G * 12, 1.2e5) and close(RHO_N * 12, 1.2e4) and close(1 * G * 12, 120)
# Câu 4: bình hẹp 30 cm / rộng 20 cm
assert close(RHO_N * G * 0.30, 3000) and close(RHO_N * G * 0.20, 2000)
# Câu 5: thợ lặn 15 m
assert close(1.0e5 + RHO_N * G * 15, 2.5e5) and close(RHO_N * G * 15, 1.5e5) and close(1e4 + 1.5e5, 1.6e5) and close(RHO_N * 15, 1.5e4)
# Câu 6: dầu ăn 0,92 g/cm³, 50 cm
assert close(920 * G * 0.5, 4600) and close(0.92 * G * 0.5, 4.6) and close(0.92 * G * 50, 460) and close(920 * G * 50, 460000)
# Câu 7: bình loe đáy 0,02 m², 9 kg, 30 cm -> 60 N (< 90 N); kiểm hình học có tồn tại: thể tích nón cụt 9 lít
p7 = RHO_N * G * 0.30
assert close(p7 * 0.02, 60) and close(9 * G, 90) and close(RHO_N * G * 30 * 0.02, 6000)
A1 = 0.02
x = (-math.sqrt(A1) + math.sqrt(A1 + 4 * (3 * 0.009 / 0.30 - A1))) / 2      # √A2 từ V = h/3 (A1 + A2 + √(A1A2))
A2 = x * x
assert A2 > A1 and close(0.30 / 3 * (A1 + A2 + math.sqrt(A1 * A2)), 0.009), A2   # miệng rộng hơn đáy -> đúng "loe"
# Bài toán mẫu
S5m = A5 * B5
assert close(S5m, 0.24) and close(S5m * H5 * RHO_N, 120) and close(RHO_N * G * H5, 5000)
assert close(PA5 + 5000, 1.05e5) and close(5000 * S5m, 1200) and close(120 * G, 1200)
assert close(RHO_N * G * (H5 - HM5), 3000)
# Điền bước: nước muối 1030, 30 cm
p_m = 1030 * G * 0.30
F_m = p_m * S5m
assert close(p_m, 3090) and close(F_m, 741.6)
DIENBUOC = (f"Bước 2: $p = 1030 \\cdot 10 \\cdot 0{{,}}3 = {round(p_m)}\\ \\text{{Pa}}$. "
            f"Bước 3: $F = pS = {round(p_m)} \\cdot 0{{,}}24 \\approx {knum(F_m, 0) if F_m.is_integer() else knum(F_m, 1)}\\ \\text{{N}}$.")
# Đổi chiều: áp suất dư 4000 Pa ở đáy thùng nước -> h
h_dc = 4000 / (RHO_N * G)
assert close(h_dc, 0.4)
DOICHIEU = (f"Áp kế ở đáy một thùng nước chỉ áp suất dư $4000\\ \\text{{Pa}}$. Mực nước cao bao nhiêu? "
            f"Áp suất dư là phần do nước: $h = \\dfrac{{p - p_a}}{{\\rho g}} = \\dfrac{{4000}}{{1000 \\cdot 10}} = {knum(h_dc, 1)}\\ \\text{{m}} = {round(h_dc * 100)}\\ \\text{{cm}}$.")
# Thử thách
rho_s1 = 54 / 20
assert close(rho_s1, 2.7)
S1 = (f"Viên sỏi $54\\ \\text{{g}}$ thả vào bình chia độ làm nước dâng thêm $20\\ \\text{{cm}}^3$. Khối lượng riêng của sỏi? "
      f"<em>(${knum(rho_s1, 1)}\\ \\text{{g/cm}}^3 = {round(rho_s1 * 1000)}\\ \\text{{kg/m}}^3$, gần bằng nhôm)</em>")
hd2 = 15
hn2 = RHO_D * hd2 / RHO_N
assert close(hn2, 12) and close(hd2 - hn2, 3)
S2 = (f"Ống chữ U chứa nước; rót dầu hoả $\\rho = {RHO_D}\\ \\text{{kg/m}}^3$ vào một nhánh, cột dầu cao ${hd2}\\ \\text{{cm}}$. "
      f"Mặt dầu cao hơn mặt nước nhánh bên kia bao nhiêu? <em>(cột nước cân bằng ${round(hn2)}\\ \\text{{cm}}$, chênh ${round(hd2 - hn2)}\\ \\text{{cm}}$)</em> "
      f"<details class=\"tl-details\"><summary>Công thức tổng quát</summary>"
      f"<p>Chênh mực: $\\Delta h = \\dfrac{{\\rho_n - \\rho_d}}{{\\rho_n}}\\,h_d$ với $h_d$ là cột dầu.</p></details>")
H_bon, H6, P6_min = 20, 15, 0.3e5
p1 = RHO_N * G * H_bon
p6 = RHO_N * G * (H_bon - H6)
h_min = H6 + P6_min / (RHO_N * G)
assert close(p1, 2e5) and close(p6, 0.5e5) and p6 >= P6_min and close(h_min, 18)
S3 = (f"Mặt nước trong bồn trên mái cao hơn vòi tầng 1 là ${H_bon}\\ \\text{{m}}$; vòi tầng 6 cao hơn vòi tầng 1 là ${H6}\\ \\text{{m}}$. "
      f"Tính áp suất dư ở hai vòi khi khoá. Máy giặt ở tầng 6 cần áp suất dư ít nhất ${knum(P6_min / 1e5, 1)}\\cdot 10^5\\ \\text{{Pa}}$: "
      f"mặt nước trong bồn phải cao hơn vòi tầng 1 ít nhất bao nhiêu? "
      f"<em>(${knum(p1 / 1e5, 0)}\\cdot 10^5\\ \\text{{Pa}}$ và ${knum(p6 / 1e5, 1)}\\cdot 10^5\\ \\text{{Pa}}$; "
      f"cần $\\rho g (H - {H6}) \\ge {knum(P6_min / 1e5, 1)}\\cdot 10^5$ nên $H \\ge {round(h_min)}\\ \\text{{m}}$)</em>")

# ================= Bảng số liệu + nhận xét: đọc tn-01, tính lại =================
tn1 = json.loads((ROOT / "content/thi-nghiem/tn-l10-klr-apsuat-01.json").read_text(encoding="utf8"))
rows = tn1["so_lieu_mau"]["hang"]
RHO_AL = next(t for t in tn1["tham_so"] if t["ky_hieu"] == "rho")["gia_tri"]
BANG = "\n".join(f"<tr><td>{num(m, 1)}</td><td>{V}</td><td>{num(rho, 2)}</td></tr>" for m, V, rho in rows)
rhos = [m / V for m, V, _ in rows]
assert all(close(round(x, 2), r_[2]) for x, r_ in zip(rhos, rows))
lech = [abs(x - RHO_AL) / RHO_AL for x in rhos]
bound = [0.5 / V + 0.05 / m for m, V, _ in rows]
assert all(l_ <= bd for l_, bd in zip(lech, bound))                 # mọi hàng trong giới hạn sai số dụng cụ
lmax = max(lech)
hang_max = [i for i, l_ in enumerate(lech) if abs(l_ - lmax) < 1e-6]
assert hang_max == [0], hang_max                                    # khối nhỏ nhất lệch nhiều nhất (đúng như nhận xét)
assert all(a > b_ for a, b_ in zip(lech, lech[1:]))                 # độ lệch giảm dần khi khối to lên
tb = sum(rhos) / len(rhos)
NX = (f"<p>Bốn khối có $m$ và $V$ khác nhau gần 5 lần, nhưng $\\rho$ chỉ dao động quanh ${knum(tb, 2)}\\ \\text{{g/cm}}^3$: "
      f"khối lượng riêng là đặc trưng của chất nhôm (giá trị bảng ${knum(RHO_AL, 2)}\\ \\text{{g/cm}}^3$).</p>"
      f"<p>Hàng đầu (khối ${rows[0][1]}\\ \\text{{cm}}^3$) lệch nhiều nhất, khoảng ${knum(100 * lech[0], 1)}\\,\\%$. "
      f"Lý do: đọc vạch bình chia độ sai $\\pm 0{{,}}5\\ \\text{{cm}}^3$; với $V = {rows[0][1]}\\ \\text{{cm}}^3$ đó là "
      f"${knum(100 * 0.5 / rows[0][1], 1)}\\,\\%$, còn với $V = {rows[-1][1]}\\ \\text{{cm}}^3$ chỉ ${knum(100 * 0.5 / rows[-1][1], 1)}\\,\\%$. "
      f"Khối càng nhỏ, sai số tương đối càng lớn. Bọt khí bám vào khối cũng làm $V$ đọc lớn hơn thật.</p>")
print("ρ:", [round(x, 4) for x in rhos], "lệch %:", [round(100 * l_, 2) for l_ in lech], "TB:", round(tb, 3))

# ================= Ghép =================
src = (HERE / "theory.src.html").read_text(encoding="utf8")
for k, v in {"__BANG__": BANG, "__NHANXET__": NX, "__DIENBUOC__": DIENBUOC, "__DOICHIEU__": DOICHIEU,
             "__S1__": S1, "__S2__": S2, "__S3__": S3}.items():
    assert k in src, k
    src = src.replace(k, v)
figs = (fig1, fig2, fig3, fig4, fig5)
order = [int(k) for k in re.findall(r"<!--FIG(\d)-->", src)]
assert order == list(range(1, len(figs) + 1)), order
for k, f in enumerate(figs, 1):
    assert f"<figcaption>Hình {k}." in f, k
    assert "$" not in re.sub(r"<figcaption>.*?</figcaption>", "", f), k     # không KaTeX trong SVG
    src = src.replace(f"<!--FIG{k}-->", f)
assert "__" not in src.replace("__PHUT__", ""), re.findall(r"__\w+__", src)

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
