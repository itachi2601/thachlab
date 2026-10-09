"""Sinh 4 hình SVG cho bài 'Sóng ngang, sóng dọc, sự truyền năng lượng của sóng cơ' (Vật lí 11, lesson 28),
dựng bảng thí nghiệm đo từ content/thi-nghiem/tn-l11-songngangdoc-03.json, thay các mốc trong theory.src.html -> theory.html.
Chạy: python3 build_thi_nghiem.py && python3 build_figs.py   (chạy lại được)."""
import json, math, pathlib, subprocess, sys
from svg_lib import *

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PHUT = 17   # = làm tròn LÊN số phút do lint_do_dai.py đo trên theory.html (script kiểm ở cuối)

subprocess.run([sys.executable, str(HERE / "build_thi_nghiem.py")], check=True, cwd=HERE)

FS = 17    # cỡ chữ nhãn (viewBox rộng 420)


def seg(x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'


def poly(pts, c, w=2.4, dash="", op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<polyline fill="none" stroke="{c}" stroke-width="{w}"{d} opacity="{op}" stroke-linejoin="round" points="'
            + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>')


def vec(x1, y1, x2, y2, c, w=2.4):
    """Vectơ: thân + đầu V 30° tại (x2, y2)."""
    return seg(x1, y1, x2, y2, c, w) + chevron(x2, y2, x2 - x1, y2 - y1, c, w)


def dbl(x1, y1, x2, y2, c, w=2.2):
    """Mũi tên hai đầu (biên độ dao động)."""
    return seg(x1, y1, x2, y2, c, w) + chevron(x2, y2, x2 - x1, y2 - y1, c, w, 10) + chevron(x1, y1, x1 - x2, y1 - y2, c, w, 10)


def t(x, y, s, c="currentColor", anchor="start", weight="600", size=FS):
    return text(x, y, s, c, size, anchor, weight)


# ---------------- Hình 1: mặt hồ, chỗ hòn sỏi rơi, gợn tròn, phao câu và chiếc lá (chỉ vẽ cảnh, không vẽ kết quả)
b = f'<rect x="0" y="70" width="420" height="180" fill="rgba(56,189,248,.12)"/>'
b += seg(0, 70, 420, 70, "currentColor", 2)
b += t(14, 58, "bờ hồ", "currentColor", "start", "500")
CX, CY = 120, 165
for i, rx in enumerate((22, 50, 80, 108)):
    b += (f'<ellipse cx="{CX}" cy="{CY}" rx="{rx}" ry="{rx*0.3:.1f}" fill="none" stroke="{BLUE}" '
          f'stroke-width="2.2" opacity="{1 - 0.18*i:.2f}"/>')
b += f'<circle cx="{CX}" cy="{CY}" r="4" fill="currentColor"/>'
b += t(CX, 118, "chỗ hòn sỏi rơi", "currentColor", "middle")
# cần câu + dây câu + phao
PX, PY = 300, 160
b += seg(412, 34, PX, 52, "currentColor", 3)
b += seg(PX, 52, PX, PY - 12, "currentColor", 1.2, "", .8)
b += f'<path d="M{PX-7},{PY} A7,10 0 0 1 {PX+7},{PY} Z" fill="{RED}"/>'
b += f'<path d="M{PX-7},{PY} A7,6 0 0 0 {PX+7},{PY} Z" fill="none" stroke="currentColor" stroke-width="1.6"/>'
b += seg(PX - 20, PY + 2, PX + 20, PY + 2, BLUE, 1.6, "", .7)
b += t(PX + 14, PY - 16, "phao câu", RED, "start", "700")
# chiếc lá
LX, LY = 352, 208
b += (f'<path d="M{LX-20},{LY} Q{LX},{LY-13} {LX+20},{LY} Q{LX},{LY+13} {LX-20},{LY} Z" fill="{GRN}" opacity=".85"/>'
      + seg(LX - 20, LY, LX + 22, LY, "currentColor", 1.2, "", .6))
b += t(LX, 238, "chiếc lá", GRN, "middle", "700")
fig1 = wrap("0 0 420 250",
            "Mặt hồ nhìn xiên: gợn tròn lan ra từ chỗ hòn sỏi rơi, phía xa có phao câu và một chiếc lá",
            b,
            "Hình 1. Gợn tròn lan từ chỗ hòn sỏi rơi về phía phao câu và chiếc lá.")

# ---------------- Hình 2: sóng ngang trên dây nhảy — dao động thẳng đứng, truyền nằm ngang
Y0, A2, LAM2, X0, X1 = 140, 40, 160, 40, 390
rope = lambda x: Y0 - A2 * math.sin(2 * math.pi * (x - X0) / LAM2)
b = seg(X0, Y0, X1, Y0, "currentColor", 1.2, "4 4", .45)
b += poly([(x, rope(x)) for x in range(X0, X1 + 1, 3)], BLUE, 2.8)
b += f'<rect x="{X1}" y="60" width="12" height="170" fill="rgba(148,163,184,.35)" stroke="currentColor" stroke-width="1.6"/>'
b += t(X1 + 6, 50, "cột", "currentColor", "middle", "500")
b += f'<circle cx="{X0}" cy="{Y0}" r="6" fill="currentColor"/>'
b += t(14, 168, "tay vẩy", "currentColor", "start", "500")
# phương truyền
b += vec(70, 40, 350, 40, GRN, 2.6) + t(210, 28, "phương truyền sóng", GRN, "middle", "700")
# dải băng ở đỉnh sóng x = 240 và biên độ dao động thẳng đứng ±A
XR = 240
assert abs(rope(XR) - (Y0 - A2)) < 0.5        # dải băng đặt đúng trên dây (ở đỉnh)
b += dbl(XR, Y0 - A2 - 4, XR, Y0 + A2 + 4, ORG, 2.4)
b += f'<rect x="{XR-5}" y="{rope(XR)-3:.1f}" width="10" height="16" fill="{ORG}"/>'
b += t(XR, 214, "dải băng: lên – xuống", ORG, "middle", "700")
fig2 = wrap("0 0 420 240",
            "Sóng ngang trên dây: sóng truyền theo phương nằm ngang, dải băng trên dây dao động lên xuống theo phương thẳng đứng",
            b,
            "Hình 2. Sóng ngang trên dây nhảy.<br>Dải băng dao động vuông góc phương truyền.")

# ---------------- Hình 3: sóng dọc trên lò xo — vùng nén, vùng dãn, vòng đánh dấu dao động dọc trục
XS, STEP, LAM3, AMP3 = 30, 9, 160, 18
assert AMP3 * 2 * math.pi / LAM3 < 1                      # vòng không chạm nhau
disp = lambda xe: AMP3 * math.sin(2 * math.pi * (xe - XS) / LAM3)
MARK = 22                                                 # vòng đánh dấu (vị trí cân bằng 228, gần chỗ lệch cực đại)
b = vec(70, 40, 350, 40, GRN, 2.6) + t(210, 28, "phương truyền sóng", GRN, "middle", "700")
for i in range(42):
    xe = XS + STEP * i
    x = xe + disp(xe)
    col, w = (ORG, 3.2) if i == MARK else ("currentColor", 1.8)
    b += f'<ellipse cx="{x:.1f}" cy="125" rx="5" ry="30" fill="none" stroke="{col}" stroke-width="{w}"/>'
# nén: du/dx < 0 tại xe − XS = λ/2 + nλ → 110, 270; dãn: du/dx > 0 → 190, 350
for xn in (110, 270):
    assert math.cos(2 * math.pi * (xn - XS) / LAM3) < -0.99
    b += t(xn, 82, "nén", RED, "middle", "700")
for xd in (190, 350):
    assert math.cos(2 * math.pi * (xd - XS) / LAM3) > 0.99
    b += t(xd, 82, "dãn", BLUE, "middle", "700")
XM = XS + STEP * MARK
b += dbl(XM - AMP3 - 6, 178, XM + AMP3 + 6, 178, ORG, 2.4)
b += t(XM + 24, 206, "vòng đánh dấu: tiến – lùi", ORG, "middle", "700")
b += dbl(14, 178, 46, 178, "currentColor", 2)
b += t(14, 206, "đầu đẩy – kéo", "currentColor", "start", "500")
fig3 = wrap("0 0 420 222",
            "Sóng dọc trên lò xo: các vòng sít nhau ở vùng nén, thưa ra ở vùng dãn; vòng đánh dấu dao động qua lại dọc trục lò xo",
            b,
            "Hình 3. Sóng dọc trên lò xo slinky.<br>Vòng cam tiến – lùi dọc phương truyền.")

# ---------------- Hình 4: đồ thị u – x của sóng dọc và hàng phần tử bên dưới
AX, A4, LAM4, XL, XR4 = 100, 45, 160, 40, 400
u = lambda x: A4 * math.sin(2 * math.pi * (x - XL) / LAM4)
b = vec(XL, AX, XR4 + 8, AX, "currentColor", 1.8) + vec(XL, 160, XL, 26, "currentColor", 1.8)
b += t(XL + 10, 30, "u", "currentColor", "start", "700") + t(XR4 + 4, AX + 24, "x", "currentColor", "end", "700")
b += poly([(x, AX - u(x)) for x in range(XL, XR4 + 1, 3)], BLUE, 2.6)
ROW, SC = 192, 14                                          # hàng phần tử: độ lệch vẽ thu nhỏ còn ±14
assert SC * 2 * math.pi / LAM4 < 1
for i in range(46):
    xe = XL + 8 * i
    x = xe + SC * u(xe) / A4
    b += seg(x, ROW - 14, x, ROW + 14, "currentColor", 2)
NEN, DAN = (120, 280), (200, 360)
for xn in NEN:
    assert abs(u(xn)) < 1e-9 and math.cos(2 * math.pi * (xn - XL) / LAM4) < -0.99   # u = 0, đồ thị đi xuống
for xd in DAN:
    assert abs(u(xd)) < 1e-9 and math.cos(2 * math.pi * (xd - XL) / LAM4) > 0.99    # u = 0, đồ thị đi lên
for x0 in NEN + DAN:
    b += seg(x0, AX, x0, ROW - 18, "currentColor", 1.2, "3 3", .6)
for xn in NEN:
    b += t(xn, ROW + 38, "nén", RED, "middle", "700")
for xd in DAN:
    b += t(xd, ROW + 38, "dãn", BLUE, "middle", "700")
b += dbl(NEN[0], 254, NEN[1], 254, GRN, 2) + t((NEN[0] + NEN[1]) / 2, 280, "λ", GRN, "middle", "700")
fig4 = wrap("0 0 420 290",
            "Đồ thị li độ u theo x của sóng dọc và hàng phần tử bên dưới: vùng nén và vùng dãn nằm ở các điểm u bằng 0",
            b,
            "Hình 4. Trên: đồ thị u – x của sóng dọc.<br>"
            "Dưới: vị trí thật của các phần tử.<br>Nén và dãn đều ở chỗ u = 0.")

# ---------------- Bảng thí nghiệm đo (từ tn-03)
tn3 = json.loads((ROOT / "content/thi-nghiem/tn-l11-songngangdoc-03.json").read_text(encoding="utf8"))
hang = tn3["so_lieu_mau"]["hang"]
ts = [r[1] for r in hang]
tb = sum(ts) / len(ts)
vn = lambda x, n=2: f"{x:.{n}f}".replace(".", ",")
rows = "".join(f"<tr><td>Lần {r[0]}</td><td>{vn(r[1])}</td></tr>" for r in hang)
rows += f"<tr><td><strong>Trung bình</strong></td><td><strong>{vn(tb, 3)}</strong></td></tr>"
bang = ('<div class="table-scroll">\n<table class="tl-table">\n<thead>\n<tr><th>Lần đo (số minh hoạ)</th><th>$t$ đi – về (s)</th></tr>\n'
        f"</thead>\n<tbody>\n{rows}\n</tbody>\n</table>\n</div>")
lech = [abs(x - tb) for x in ts]
mx = max(lech)
lan_max = [i + 1 for i, d in enumerate(lech) if abs(d - mx) < 1e-6]
assert lan_max == [2], lan_max
lech_txt = (f"Lần {lan_max[0]} lệch xa trung bình nhất: {vn(ts[lan_max[0]-1])} s, thấp hơn {vn(mx, 3)} s. "
            f"Các lần còn lại lệch không quá {vn(sorted(lech)[-2], 3)} s.")
assert abs(2 * 4.00 / tb - 6.93) < 0.01 and f"{tb:.3f}" == "1.154"

h = (HERE / "theory.src.html").read_text(encoding="utf8")
for n, f in enumerate((fig1, fig2, fig3, fig4), 1):
    assert h.count(f"<!--FIG{n}-->") == 1, f"thiếu mốc FIG{n}"
    h = h.replace(f"<!--FIG{n}-->", f)
for k, v in (("__BANG_TN__", bang), ("__LECH_NHIEU__", lech_txt), ("__PHUT__", str(PHUT))):
    assert h.count(k) == 1, k
    h = h.replace(k, v)
(HERE / "theory.html").write_text(h, encoding="utf8")
print("ok", len(h), "bytes,", h.count('<figure class="fig"'), "hình")

# kiểm số phút khớp lint_do_dai (làm tròn LÊN)
lint = ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
r = subprocess.run([sys.executable, str(lint), str(HERE / "theory.html"), "--json"], capture_output=True, text=True)
try:
    kq = json.loads(r.stdout)
    kq = kq[0] if isinstance(kq, list) else kq
    phut = math.ceil(kq["phut"] - 1e-9)
    print(f"lint_do_dai: {kq['hien']} từ hiện ngay, {kq['phut']:.2f} phút -> ghi {phut}" + ("" if phut == PHUT else f"  ✗ PHUT={PHUT} LỆCH"))
except Exception as e:  # noqa
    print("không đọc được json lint_do_dai:", e, r.stdout[:300])
