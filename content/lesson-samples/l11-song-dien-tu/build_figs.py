"""Sinh 4 hình SVG cho bài 'Sóng điện từ' (Vật lí 11, lesson 30), dựng bảng thí nghiệm đo từ
content/thi-nghiem/tn-l11-songdientu-02.json, thay các mốc trong theory.src.html -> theory.html.
Chạy: python3 build_figs.py   (tự gọi build_thi_nghiem.py trước; chạy lại được)."""
import json, math, pathlib, subprocess, sys
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PHUT = 17   # = làm tròn LÊN số phút do lint_do_dai.py đo trên theory.html (script kiểm ở cuối)

subprocess.run([sys.executable, str(HERE / "build_thi_nghiem.py")], check=True, cwd=HERE)

FS = 17     # cỡ chữ nhãn (viewBox rộng 420)
CW = 0.58 * FS   # bề rộng ước lượng một ký tự (đậm) để kiểm chồng nhãn
VIOLET = "#a78bfa"


def seg(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def poly(pts, c, w=2.4, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<polyline fill="none" stroke="{c}" stroke-width="{w}"{d} opacity="{op}" stroke-linejoin="round" points="'
            + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>')


def vec(x1, y1, x2, y2, c, w=2.6, L=12):
    return seg(x1, y1, x2, y2, c, w) + chevron(x2, y2, x2 - x1, y2 - y1, c, w, L)


def dbl(x1, y1, x2, y2, c, w=2.2):
    return seg(x1, y1, x2, y2, c, w) + chevron(x2, y2, x2 - x1, y2 - y1, c, w, 10) + chevron(x1, y1, x1 - x2, y1 - y2, c, w, 10)


def t(x, y, s, c="currentColor", anchor="start", weight="600", size=FS):
    return text(x, y, s, c, size, anchor, weight)


def hop(x, y, s, anchor="start", size=FS):
    """Hộp bao ước lượng của một nhãn: (x0, y0, x1, y1)."""
    w = len(s) * 0.58 * size
    x0 = {"start": x, "middle": x - w / 2, "end": x - w}[anchor]
    return (x0, y - size * 0.8, x0 + w, y + size * 0.2)


def chong(a, b, pad=2):
    return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])


def kiem_nhan(boxes, W):
    for i, a in enumerate(boxes):
        assert a[0] >= 2 and a[2] <= W - 2, ("nhãn vượt biên", a)
        for b in boxes[i + 1:]:
            assert not chong(a, b), ("nhãn chồng nhau", a, b)


# ---------------- Hình 1: cảnh mở bài — trạm phát sóng, chung cư có thang máy, chảo thu trên mái, vệ tinh (chỉ cảnh)
W1, H1, GR = 420, 262, 248
b = seg(0, GR, W1, GR, "currentColor", 2)
# trạm phát sóng (cột giàn)
TX, TY = 52, 96
b += seg(TX, TY, TX - 24, GR, "currentColor", 2.2) + seg(TX, TY, TX + 24, GR, "currentColor", 2.2)
for k in range(1, 6):
    y = TY + (GR - TY) * k / 6
    hw = 24 * k / 6
    b += seg(TX - hw, y, TX + hw, y, "currentColor", 1.4, "", .8)
b += seg(TX, TY, TX, TY - 18, "currentColor", 2.4) + f'<circle cx="{TX}" cy="{TY-18}" r="4" fill="{RED}"/>'
for r in (14, 26):   # vệt sóng phát ra quanh đỉnh cột (chỉ phía phải)
    a0, a1 = math.radians(-45), math.radians(45)
    b += (f'<path d="M{TX + r*math.cos(a0):.1f},{TY-18 + r*math.sin(a0):.1f} A{r},{r} 0 0 1 '
          f'{TX + r*math.cos(a1):.1f},{TY-18 + r*math.sin(a1):.1f}" fill="none" stroke="{BLUE}" stroke-width="2"/>')
lab1 = [("trạm phát sóng", 8, 40, "start")]
# chung cư + giếng thang máy + cabin kim loại + người cầm điện thoại
BX0, BX1, BT = 132, 270, 112
b += f'<rect x="{BX0}" y="{BT}" width="{BX1-BX0}" height="{GR-BT}" fill="rgba(148,163,184,.12)" stroke="currentColor" stroke-width="2"/>'
for y in range(BT + 34, GR, 34):
    b += seg(BX0, y, BX1, y, "currentColor", 1, "", .35)
for wx in (144, 240):
    for y in range(BT + 10, GR - 20, 34):
        b += f'<rect x="{wx}" y="{y}" width="18" height="14" fill="none" stroke="currentColor" stroke-width="1.2" opacity=".6"/>'
SX0, SX1 = 178, 228
b += seg(SX0, BT, SX0, GR, "currentColor", 1.4, "5 4", .7) + seg(SX1, BT, SX1, GR, "currentColor", 1.4, "5 4", .7)
CY0, CY1 = 172, 244
b += f'<rect x="{SX0+3}" y="{CY0}" width="{SX1-SX0-6}" height="{CY1-CY0}" fill="rgba(148,163,184,.35)" stroke="currentColor" stroke-width="2.6"/>'
PX = 203
b += f'<circle cx="{PX}" cy="{CY0+16}" r="7" fill="none" stroke="currentColor" stroke-width="2"/>'
b += seg(PX, CY0 + 23, PX, CY0 + 48, "currentColor", 2) + seg(PX, CY0 + 48, PX - 8, CY1 - 3, "currentColor", 2) + seg(PX, CY0 + 48, PX + 8, CY1 - 3, "currentColor", 2)
b += seg(PX, CY0 + 30, PX + 11, CY0 + 24, "currentColor", 2)
b += f'<rect x="{PX+10}" y="{CY0+14}" width="6" height="11" rx="1.5" fill="{ORG}"/>'
b += seg(SX1 + 2, 206, 276, 206, "currentColor", 1.2, "", .8)
lab1.append(("thang máy", 280, 212, "start"))
# chảo thu trên mái
DX, DY = 248, BT
b += seg(DX, DY, DX, DY - 12, "currentColor", 2)
b += f'<path d="M{DX-14},{DY-24} Q{DX-6},{DY-6} {DX+10},{DY-12}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
b += seg(DX - 3, DY - 17, DX + 8, DY - 30, "currentColor", 1.4)
lab1.append(("chảo thu", 276, 108, "start"))
# vệ tinh
VX, VY = 378, 38
b += f'<rect x="{VX-9}" y="{VY-9}" width="18" height="18" fill="rgba(148,163,184,.35)" stroke="currentColor" stroke-width="2"/>'
b += f'<rect x="{VX-36}" y="{VY-6}" width="24" height="12" fill="rgba(56,189,248,.45)" stroke="currentColor" stroke-width="1.2"/>'
b += f'<rect x="{VX+12}" y="{VY-6}" width="24" height="12" fill="rgba(56,189,248,.45)" stroke="currentColor" stroke-width="1.2"/>'
lab1.append(("vệ tinh", 336, 44, "end"))
for s, x, y, a in lab1:
    b += t(x, y, s, "currentColor", a, "600")
kiem_nhan([hop(x, y, s, a) for s, x, y, a in lab1], W1)
fig1 = wrap(f"0 0 {W1} {H1}",
            "Cảnh mở bài: cột trạm phát sóng điện thoại, toà chung cư có giếng thang máy và một người cầm điện thoại trong cabin, chảo thu trên mái, vệ tinh trên cao",
            b,
            "Hình 1. Trạm phát sóng, thang máy, chảo thu và vệ tinh.")

# ---------------- Hình 2: sóng điện từ — E (đỏ, thẳng đứng) ⊥ B (xanh, phương xiên vào trong) ⊥ phương truyền (trục ngang)
W2, H2 = 420, 192
X0, X1, Y0, LAM = 40, 340, 118, 200.0
AE, AB = 62, 56
ZX, ZY = -0.6, 0.6                     # phương "vào trong trang" vẽ xiên xuống – sang trái
ZN = math.hypot(ZX, ZY)
ZX, ZY = ZX / ZN, ZY / ZN
# Chiều: x phải (truyền), y lên (E), z ra phía người xem vẽ xiên xuống–trái. E×B = ŷ×ẑ = +x̂ khớp chiều truyền.
_E, _B = (0, 1, 0), (0, 0, 1)
_c = (_E[1]*_B[2]-_E[2]*_B[1], _E[2]*_B[0]-_E[0]*_B[2], _E[0]*_B[1]-_E[1]*_B[0])
assert _c == (1, 0, 0) and ZX < 0 and ZY > 0
s_ = lambda x: math.sin(2 * math.pi * (x - X0) / LAM)
b = vec(18, Y0, 404, Y0, "currentColor", 2, 12)
for k in range(1, 24):                 # các vạch nối trục → đường cong (mỗi λ/16)
    x = X0 + LAM / 16 * k
    if x > X1:
        break
    v = s_(x)
    b += seg(x, Y0, x, Y0 - AE * v, RED, 1.2, "", .55)
    b += seg(x, Y0, x + ZX * AB * v, Y0 + ZY * AB * v, BLUE, 1.2, "", .55)
xs = [X0 + i for i in range(0, int(X1 - X0) + 1, 2)]
b += poly([(x + ZX * AB * s_(x), Y0 + ZY * AB * s_(x)) for x in xs], BLUE, 2.6)
b += poly([(x, Y0 - AE * s_(x)) for x in xs], RED, 2.6)
XM = X0 + LAM / 4                      # chỗ E, B cực đại (cùng pha)
assert abs(s_(XM) - 1) < 1e-9 and abs(s_(X0 + LAM / 2)) < 1e-9
b += vec(XM, Y0, XM, Y0 - AE, RED, 3)
bx, by = XM + ZX * AB, Y0 + ZY * AB
b += vec(XM, Y0, bx, by, BLUE, 3)
lab2 = [("E", XM, Y0 - AE - 10, "middle", RED), ("B", bx - 6, by + 20, "end", BLUE),
        ("phương", 412, Y0 + 30, "end", "currentColor"), ("truyền", 412, Y0 + 50, "end", "currentColor")]
for s, x, y, a, c in lab2:
    b += f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{FS+2 if len(s)==1 else FS}" font-weight="700" text-anchor="{a}"' + (' font-style="italic" font-family="serif"' if len(s) == 1 else "") + f'>{s}</text>'
# nhãn sát vật: E cách đầu vectơ E ≤ 30 px, B cách đầu vectơ B ≤ 30 px
assert math.hypot(0, 10) < 30 and math.hypot((bx - 6) - bx, (by + 20) - by) < 30
# nhãn "phương truyền" không chạm đường cong: các đường cong kết thúc ở X1 < hộp nhãn
assert X1 + ZX * 0 < hop(412, Y0 + 30, "phương", "end")[0] - 4
kiem_nhan([hop(x, y, s, a) for s, x, y, a, c in lab2], W2)
fig2 = wrap(f"0 0 {W2} {H2}",
            "Sóng điện từ truyền theo trục nằm ngang: vectơ E màu đỏ dao động theo phương thẳng đứng, vectơ B màu xanh dao động theo phương vuông góc với trang giấy, vẽ xiên hướng ra phía người xem, hai đường cong cùng đạt cực đại và cùng qua số 0 tại một chỗ",
            b,
            "Hình 2. E (đỏ) vuông góc với B (xanh, vẽ xiên, hướng ra phía người xem).<br>"
            "Cả hai vuông góc với phương truyền, cùng pha.")

# ---------------- Hình 3: thanh sô-cô-la nhìn từ trên, các vệt chảy cách đều d (= λ/2)
W3, H3 = 420, 178
PXCM = 18.0                            # px / cm
BAR0, BAR1, BY0, BY1 = 30, 390, 62, 112
D_CM = 6.12                            # λ/2 với f = 2,45 GHz
spots = [70 + i * D_CM * PXCM for i in range(3)]
assert spots[-1] + 20 < BAR1
b = f'<rect x="{BAR0}" y="{BY0}" width="{BAR1-BAR0}" height="{BY1-BY0}" rx="6" fill="rgba(146,94,60,.55)" stroke="currentColor" stroke-width="2"/>'
for x in range(BAR0 + 40, BAR1, 40):
    b += seg(x, BY0 + 4, x, BY1 - 4, "currentColor", 1, "", .3)
for x in spots:
    b += f'<ellipse cx="{x:.1f}" cy="{(BY0+BY1)/2}" rx="9" ry="13" fill="rgba(251,146,60,.85)" stroke="{ORG}" stroke-width="2"/>'
    b += seg(x, BY1 + 2, x, 136, "currentColor", 1.2, "3 3", .7)
b += dbl(spots[0], 132, spots[1], 132, GRN, 2.4)
lab3 = [("d", (spots[0] + spots[1]) / 2, 158, "middle", GRN), ("vệt chảy", spots[2] + 6, 40, "middle", ORG),
        ("phần còn cứng", 30, 40, "start", "currentColor")]
b += seg(spots[2], BY0 - 2, spots[2] + 4, 46, ORG, 1.4)
xc = (spots[0] + spots[1]) / 2
b += seg(xc, BY0 + 6, 96, 46, "currentColor", 1.2, "", .8)
for s, x, y, a, c in lab3:
    b += (f'<text x="{x:.1f}" y="{y}" fill="{c}" font-size="{FS+2}" font-weight="700" text-anchor="{a}" font-style="italic" font-family="serif">{s}</text>'
          if s == "d" else t(x, y, s, c, a, "700"))
kiem_nhan([hop(x, y, s, a) for s, x, y, a, c in lab3], W3)
fig3 = wrap(f"0 0 {W3} {H3}",
            "Thanh sô-cô-la nhìn từ trên xuống sau khi quay trong lò vi sóng không có đĩa xoay: ba vệt chảy màu cam cách đều nhau, khoảng cách giữa tâm hai vệt liền nhau ghi là d",
            b,
            "Hình 3. Thanh sô-cô-la sau khi quay (đĩa không xoay).<br>d: khoảng cách tâm hai vệt chảy liền nhau.")

# ---------------- Hình 4: thang sóng điện từ, trục log λ (10³ m → 10⁻¹³ m), mốc f = c/λ
W4, H4 = 420, 206
AX0, AX1, LMAX, LMIN = 60, 400, 3, -13
PPD = (AX1 - AX0) / (LMAX - LMIN)
xl = lambda lg: AX0 + (LMAX - lg) * PPD
assert abs(xl(LMIN) - AX1) < 1e-9 and abs((xl(0) - xl(3)) - (xl(-3) - xl(0))) < 1e-9   # trục chia đều theo luỹ thừa 10
BT4, BB4 = 82, 108
lg_ir, lg_vis = math.log10(7.6e-7), math.log10(3.8e-7)
vung = [("vô tuyến", 3, 0, "rgba(56,189,248,.30)"), ("vi sóng", 0, -3, "rgba(56,189,248,.55)"),
        ("hồng ngoại", -3, lg_ir, "rgba(248,113,113,.40)"), ("nhìn thấy", lg_ir, lg_vis, "url(#f4-vis)"),
        ("tử ngoại", lg_vis, -8, "rgba(167,139,250,.45)"), ("tia X", -8, -11, "rgba(148,163,184,.45)"),
        ("tia γ", -11, -13, "rgba(100,116,139,.65)")]
b = ('<defs><linearGradient id="f4-vis" x1="0" x2="1" y1="0" y2="0">'
     '<stop offset="0" stop-color="#ef4444"/><stop offset=".25" stop-color="#f59e0b"/><stop offset=".5" stop-color="#22c55e"/>'
     '<stop offset=".75" stop-color="#3b82f6"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs>')
for name, a, c_, fill in vung:
    b += f'<rect x="{xl(a):.2f}" y="{BT4}" width="{xl(c_)-xl(a):.2f}" height="{BB4-BT4}" fill="{fill}"/>'
b += f'<rect x="{AX0}" y="{BT4}" width="{AX1-AX0}" height="{BB4-BT4}" fill="none" stroke="currentColor" stroke-width="1.8"/>'
for name, a, c_, fill in vung[1:]:
    b += seg(xl(a), BT4, xl(a), BB4, "currentColor", 1, "", .6)
# nhãn vùng: (tên, x tâm nhãn, hàng y, x đường dóng, anchor)
mid = {n: (xl(a) + xl(c_)) / 2 for n, a, c_, f in vung}
nhan = [("vô tuyến", mid["vô tuyến"], 50, mid["vô tuyến"], "middle"),
        ("hồng ngoại", 200, 50, mid["hồng ngoại"], "middle"),
        ("tử ngoại", 302, 50, mid["tử ngoại"], "middle"),
        ("vi sóng", mid["vi sóng"], 74, mid["vi sóng"], "middle"),
        ("tia X", mid["tia X"], 74, mid["tia X"], "middle"),
        ("tia γ", 382, 74, mid["tia γ"], "middle"),
        ("ánh sáng nhìn thấy", mid["nhìn thấy"] - 5, 22, mid["nhìn thấy"], "end")]
boxes4 = []
for s, x, y, xd, a in nhan:
    col = {"hồng ngoại": RED, "tử ngoại": VIOLET, "ánh sáng nhìn thấy": GRN}.get(s, "currentColor")
    b += t(x, y, s, col, a, "700")
    bx_ = hop(x, y, s, a)
    boxes4.append(bx_)
    ytop = 16 if s == "ánh sáng nhìn thấy" else y + 4
    b += seg(xd, ytop, xd, BT4, col, 1.3, "", .85)
    if s != "ánh sáng nhìn thấy":
        assert bx_[0] <= xd <= bx_[2], ("đường dóng không nằm dưới nhãn", s)
# đường dóng không cắt nhãn khác
for s, x, y, xd, a in nhan:
    ytop = 16 if s == "ánh sáng nhìn thấy" else y + 4
    for (s2, x2, y2, xd2, a2), bx2 in zip(nhan, boxes4):
        if s2 == s:
            continue
        if bx2[1] < BT4 and bx2[3] > ytop:
            assert not (bx2[0] - 2 <= xd <= bx2[2] + 2), ("đường dóng cắt nhãn", s, s2)
# mốc λ và f
C = 3e8
SUP = {"0": "0", "1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "-": "−"}
ten_l = {3: "1 km", 0: "1 m", -3: "1 mm", -6: "1 μm", -9: "1 nm", -12: "1 pm"}
for lg, s in ten_l.items():
    x = xl(lg)
    b += seg(x, BB4, x, BB4 + 6, "currentColor", 1.6)
    b += t(x, 132, s, "currentColor", "middle", "600")
    e = round(math.log10(C) - lg - math.log10(3))
    assert abs(C / 10 ** lg - 3 * 10 ** e) / (3 * 10 ** e) < 1e-9
    b += (f'<text x="{x:.1f}" y="156" fill="currentColor" font-size="{FS}" font-weight="600" text-anchor="middle">3·10'
          f'<tspan baseline-shift="super" font-size="13">{e}</tspan></text>')
b += t(10, 132, "λ", "currentColor", "start", "700") + t(10, 156, "f", "currentColor", "start", "700")
b += vec(AX0, 176, AX1, 176, GRN, 2.2)
b += t((AX0 + AX1) / 2, 198, "λ giảm dần, f (Hz) tăng dần", GRN, "middle", "700")
kiem_nhan(boxes4 + [hop(xl(lg), 132, s, "middle") for lg, s in ten_l.items()] + [hop((AX0 + AX1) / 2, 198, "λ giảm dần, f (Hz) tăng dần", "middle")], W4)
fig4 = wrap(f"0 0 {W4} {H4}",
            "Thang sóng điện từ vẽ trên trục chia theo luỹ thừa 10 của bước sóng, từ 1 km bên trái tới dưới 1 pm bên phải: vô tuyến, vi sóng, hồng ngoại, dải rất hẹp ánh sáng nhìn thấy, tử ngoại, tia X, tia gamma; hàng dưới ghi tần số tương ứng",
            b,
            "Hình 4. Thang sóng điện từ, trục chia theo luỹ thừa 10, cắt từ 1 km.<br>"
            "Ánh sáng nhìn thấy chỉ là một vạch hẹp.")

# ---------------- Bảng thí nghiệm đo (từ tn-02)
tn2 = json.loads((ROOT / "content/thi-nghiem/tn-l11-songdientu-02.json").read_text(encoding="utf8"))
hang = tn2["so_lieu_mau"]["hang"]
ds = [r[1] for r in hang]
tb = sum(ds) / len(ds)
vn = lambda x, n=1: f"{x:.{n}f}".replace(".", ",")
rows = "".join(f"<tr><td>Lần {r[0]}</td><td>{vn(r[1])}</td></tr>" for r in hang)
rows += f"<tr><td><strong>Trung bình</strong></td><td><strong>{vn(tb, 2)}</strong></td></tr>"
bang = ('<div class="table-scroll">\n<table class="tl-table">\n<thead>\n<tr><th>Lần đo (số minh hoạ)</th><th>$d$ (cm)</th></tr>\n'
        f"</thead>\n<tbody>\n{rows}\n</tbody>\n</table>\n</div>")
assert f"{tb:.2f}" == "6.10"
lech = [abs(x - tb) for x in ds]
mx = max(lech)
lan_max = [i + 1 for i, d in enumerate(lech) if abs(d - mx) < 1e-6]
assert lan_max == [3, 4], lan_max
lech_txt = (f"Lần {lan_max[0]} và lần {lan_max[1]} cùng lệch xa trung bình nhất, {vn(mx)} cm "
            f"({vn(ds[lan_max[0]-1])} cm và {vn(ds[lan_max[1]-1])} cm). Các lần khác lệch không quá {vn(sorted(lech)[-3])} cm.")
c_do = 2 * tb / 100 * 2.45e9
assert abs(c_do - 2.989e8) < 1e5

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert h.count(f"<!--FIG{n}-->") == 1, f"thiếu mốc FIG{n}"
    h = h.replace(f"<!--FIG{n}-->", f)
for k, v in (("__BANG_TN__", bang), ("__LECH_NHIEU__", lech_txt), ("__PHUT__", str(PHUT))):
    assert h.count(k) == 1, k
    h = h.replace(k, v)
# thứ tự hình đúng thứ tự xuất hiện
import re
so = [int(m) for m in re.findall(r"<figcaption>Hình (\d+)\.", h)]
assert so == sorted(so) == list(range(1, len(so) + 1)), so
(HERE / "theory.html").write_text(h, encoding="utf8")
print("ok", len(h), "bytes,", h.count('<figure class="fig"'), "hình")

lint = ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
r = subprocess.run([sys.executable, str(lint), str(HERE / "theory.html"), "--json"], capture_output=True, text=True)
try:
    kq = json.loads(r.stdout)
    kq = kq[0] if isinstance(kq, list) else kq
    phut = math.ceil(kq["phut"] - 1e-9)
    print(f"lint_do_dai: {kq['hien']} từ hiện ngay, {kq['phut']:.2f} phút -> ghi {phut}" + ("" if phut == PHUT else f"  ✗ PHUT={PHUT} LỆCH"))
except Exception as e:  # noqa
    print("không đọc được json lint_do_dai:", e, r.stdout[:300])
