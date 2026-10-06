"""Sinh 4 hình SVG cho bài 'Định luật bảo toàn động lượng' (lesson 74), bảng số liệu + nhận xét, rồi thay mốc
<!--FIGn--> / __BANG__ / __NHANXET__ / __PHUT__ trong theory.src.html -> theory.html; ghi luôn 4 file
content/thi-nghiem/tn-l10-baotoandl-0N.json (sửa số/chữ thí nghiệm ở đây, đừng sửa tay JSON).
Chạy: python3 build_figs.py (từ thư mục bài hoặc gốc repo).
Tự kiểm: nhãn không chồng nhau, không vượt viewBox, không bị nét/mũi tên cắt xuyên; độ dài mũi tên đúng tỉ lệ."""
import json, math, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"))
from svg_lib import RED, BLUE, ORG, GRN, wrap, person  # noqa: E402

COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN, "k": "currentColor"}
LABELS = []   # (fig, x0, y0, x1, y1, text)
SEGS = []     # (fig, x1, y1, x2, y2, tên)
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


def sub(base, s, fs=13):
    return f'{base}<tspan baseline-shift="sub" font-size="{fs}">{s}</tspan>'


def text(x, y, s, c="currentColor", size=14, anchor="start", weight="700", italic=False):
    plain = re.sub(r"<[^>]+>", "", s).replace("&gt;", ">").replace("&lt;", "<")
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


def num(v, d=2):
    return f"{v:.{d}f}".replace(".", ",")


def tex(v, d=2):
    return f"{v:.{d}f}".replace(".", "{,}")


# ---------------- Số liệu thí nghiệm va chạm mềm (minh hoạ) ----------------
M1 = 0.20
LOSS = [0.975, 0.985, 0.98, 0.975]            # ma sát còn sót: p sau = LOSS·p trước (trước khi làm tròn)
RUNS = [(0.20, 0.52), (0.30, 0.60), (0.40, 0.57), (0.60, 0.66)]   # (m2, v1)
DATA = []
for (m2, v1), k in zip(RUNS, LOSS):
    v_ly_thuyet = M1 * v1 / (M1 + m2)
    v = round(v_ly_thuyet * k + 1e-9, 2)
    DATA.append((m2, v1, v, v_ly_thuyet))
pt = [M1 * v1 for _, v1, _, _ in DATA]
ps = [(M1 + m2) * v for m2, _, v, _ in DATA]
lech = [100 * (b - a) / a for a, b in zip(pt, ps)]
assert all(b <= a * 1.02 for a, b in zip(pt, ps)), "p sau thường không lớn hơn p trước (lệch nhỏ nằm trong sai số)"
assert all(abs(x) < 4.5 for x in lech), lech
vs = [v for _, _, v, _ in DATA]
assert vs == sorted(vs, reverse=True), "Quan sát: m2 càng lớn, v càng nhỏ"
rel_v = [0.005 / v * 100 for v in vs]
wd = M1 / (M1 + DATA[0][0])        # tỉ lệ động năng còn lại ở lần 1 (va chạm mềm, vật 2 đứng yên)
BANG = "\n".join(f"<tr><td>{num(m2)}</td><td>{num(v1)}</td><td>{num(v)}</td></tr>" for m2, v1, v, _ in DATA)
lech_s = "; ".join(("$0\\,\\%$" if abs(x) < 0.05 else f"${tex(x, 1)}\\,\\%$") for x in lech)
NX = (f"$p_{{\\text{{trước}}}}$: {'; '.join('$' + tex(x, 3) + '$' for x in pt)} $\\text{{kg}}\\cdot\\text{{m/s}}$. "
      f"$p_{{\\text{{sau}}}}$: {'; '.join('$' + tex(x, 3) + '$' for x in ps)} $\\text{{kg}}\\cdot\\text{{m/s}}$. "
      f"Lệch: {lech_s}.</p><p>"
      f"$p_{{\\text{{sau}}}}$ thường bằng hoặc hơi nhỏ hơn $p_{{\\text{{trước}}}}$: ma sát còn sót của đệm khí và không khí "
      f"thường chỉ làm hệ mất bớt động lượng; nếu $p_{{\\text{{sau}}}}$ lớn hơn thì chênh lệch nằm trong phạm vi sai số. Thêm nữa, $v$ ghi làm tròn tới $0{{,}}01\\ \\text{{m/s}}$ "
      f"(sai tới $\\pm 0{{,}}005\\ \\text{{m/s}}$); với $v = {tex(min(vs))}\\ \\text{{m/s}}$ đã là khoảng ${round(max(rel_v))}\\,\\%$. "
      f"Vậy lệch vài phần trăm vẫn nằm trong sai số: định luật được nghiệm đúng.</p><p>"
      f"Động năng thì khác hẳn: ở lần 1 chỉ còn $\\dfrac{{m_1}}{{m_1 + m_2}} = {round(100 * wd)}\\,\\%$ — "
      f"đó là dấu hiệu của va chạm mềm (mục 3).")
print("p trước", [round(x, 4) for x in pt], "p sau", [round(x, 4) for x in ps], "lệch %", [round(x, 1) for x in lech])

# ---------------- Hình 1: An trượt tới, Bình đứng yên ----------------
CUR["fig"] = 1
VB[1] = (440, 210)
GY = 188
b = defs("f1")
b += line(20, GY, 420, GY, BLUE, 2, "", .5, check=False)
for xx in (60, 150, 240, 330):
    b += line(xx, GY + 8, xx + 30, GY + 8, BLUE, 1.2, "", .35, check=False)
xa, xb = 110, 320
b += person(xa, GY) + person(xb, GY)
b += line(xa - 40, 100, xa - 22, 100, "currentColor", 1.5, "", .5, check=False)
b += line(xa - 46, 116, xa - 24, 116, "currentColor", 1.5, "", .5, check=False)
b += arrow("f1", "g", xa - 10, 56, xa + 80, 56, 3, name="v An")
b += text(xa + 35, 38, "An trượt tới", GRN, 14, "middle")
b += text(xb, 50, "Bình đứng yên", "currentColor", 14, "middle")
b += text(xa + 22, 128, "An", "currentColor", 14, "start")
b += text(xb + 22, 128, "Bình", "currentColor", 14, "start")
fig1 = wrap(f"0 0 {VB[1][0]} {VB[1][1]}",
            "An đang trượt tới trên mặt băng, Bình đứng yên phía trước; sau cú ôm hai bạn cùng lướt đi", b,
            "Hình 1. Trước cú ôm: An trượt tới, Bình đứng yên. Sau cú ôm hai bạn cùng lướt — nhanh bao nhiêu?")
fig1 = fig1.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-baotoandl-04"', 1)

# ---------------- Hình 2: ray đệm khí, va chạm mềm (vẽ theo lần đo 1) ----------------
CUR["fig"] = 2
VB[2] = (440, 260)
K = 200.0                       # px cho 1 m/s
m2_1, v1_1, _, vlt_1 = DATA[0]
T1, T2 = 100, 220
CW, CH = 56, 26
G1, G2 = 215, 395


def track(T):
    return (f'<rect x="20" y="{T}" width="400" height="8" rx="2" fill="rgba(148,163,184,.25)" '
            f'stroke="currentColor" stroke-width="1.5"/>')


def cart(x0, T, fill):
    return (f'<rect x="{x0}" y="{T-CH}" width="{CW}" height="{CH}" rx="4" fill="{fill}" '
            f'stroke="currentColor" stroke-width="2"/>')


def gate(x, T):
    return (line(x - 8, T, x - 8, T - 48, "currentColor", 2, name="cổng") + line(x - 8, T - 48, x + 8, T - 48, "currentColor", 2, name="cổng")
            + line(x + 8, T - 48, x + 8, T, "currentColor", 2, name="cổng"))


b = defs("f2")
b += track(T1) + track(T2)
b += gate(G1, T1) + gate(G2, T1) + gate(G1, T2) + gate(G2, T2)
c1 = 40
c2 = 255
b += cart(c1, T1, "rgba(248,113,113,.22)") + cart(c2, T1, "rgba(56,189,248,.22)")
b += text(c1 + CW / 2, T1 - 8, sub("m", "1"), "currentColor", 14, "middle")
b += text(c2 + CW / 2, T1 - 8, sub("m", "2"), "currentColor", 14, "middle")
ax = c1 + CW / 2
L1 = K * v1_1
b += arrow("f2", "g", ax, T1 - 40, ax + L1, T1 - 40, 3, name="v1")
b += text(ax + L1 / 2, T1 - 48, sub("v", "1"), GRN, 15, "middle", "700", True)
b += text(c2 + CW / 2, T1 - 36, "đứng yên", "currentColor", 13, "middle", "600")
b += text(G1, T1 - 56, "cổng quang 1", "currentColor", 13, "middle", "600")
b += text(432, T1 - 56, "cổng quang 2", "currentColor", 13, "end", "600")
b += text(12, 20, "Trước", "currentColor", 14, "start")
b += text(12, T2 - 74, "Sau", "currentColor", 14, "start")
cs = 252
b += cart(cs, T2, "rgba(248,113,113,.22)") + cart(cs + CW, T2, "rgba(56,189,248,.22)")
b += text(cs + CW / 2, T2 - 8, sub("m", "1"), "currentColor", 14, "middle")
b += text(cs + 1.5 * CW, T2 - 8, sub("m", "2"), "currentColor", 14, "middle")
bx = cs + CW
L2 = K * vlt_1
b += arrow("f2", "g", bx - 50, T2 - 40, bx - 50 + L2, T2 - 40, 3, name="v")
b += text(bx - 50 + L2 / 2, T2 - 48, "v", GRN, 15, "middle", "700", True)
b += text(40, T2 - 30, "dính nhau, đi chung", "currentColor", 13, "start", "600")
assert abs(L2 / L1 - M1 / (M1 + m2_1)) < 1e-9
fig2 = wrap(f"0 0 {VB[2][0]} {VB[2][1]}",
            "Ray đệm khí với hai cổng quang: trước va chạm xe 1 chạy, xe 2 đứng yên; sau va chạm hai xe dính nhau đi chung với vận tốc nhỏ hơn", b,
            "Hình 2. Ray đệm khí, vẽ theo tỉ lệ cho lần đo 1 (hai xe nặng bằng nhau). Trước: xe 1 có $v_1$, xe 2 đứng yên. "
            "Sau: hai xe dính nhau, mũi tên $v$ chỉ dài bằng nửa $v_1$.")

# ---------------- Hình 3: tên lửa, M = 3m ----------------
CUR["fig"] = 3
VB[3] = (440, 190)
RY = 92
RATIO = 3
b = defs("f3")
b += (f'<path d="M200,{RY-18} L320,{RY-18} L360,{RY} L320,{RY+18} L200,{RY+18} Z" fill="rgba(52,211,153,.18)" '
      f'stroke="currentColor" stroke-width="2"/>')
b += (f'<path d="M200,{RY-18} L184,{RY-34} L222,{RY-18} Z M200,{RY+18} L184,{RY+34} L222,{RY+18} Z" '
      f'fill="none" stroke="currentColor" stroke-width="2"/>')
for (cx, cy, r) in ((182, RY, 10), (164, RY - 7, 8), (165, RY + 8, 7), (148, RY, 7)):
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="rgba(251,146,60,.35)" stroke="{ORG}" stroke-width="1.2"/>'
LV = 120
b += arrow("f3", "o", 136, RY, 136 - LV, RY, 3, name="v khí")
b += arrow("f3", "g", 362, RY, 362 + LV / RATIO, RY, 3, name="V tên lửa")
b += text(76, RY - 18, "khí: m, v", ORG, 17, "middle")
b += text(432, RY - 30, "tên lửa: M, V", GRN, 17, "end")
b += text(220, 160, "M = 3m  ⇒  V = v : 3", "currentColor", 17, "middle")
b += text(220, 182, "hai mũi tên ngược chiều", "currentColor", 17, "middle", "600")
assert abs((LV / RATIO) * RATIO - LV) < 1e-9
fig3 = wrap(f"0 0 {VB[3][0]} {VB[3][1]}",
            "Tên lửa phụt khí về phía sau; vận tốc khí dài gấp ba vận tốc tên lửa, hai vận tốc ngược chiều", b,
            "Hình 3. Tên lửa đứng yên rồi phụt khí, vẽ cho $M = 3m$. Mũi tên vận tốc của khí dài gấp 3 lần của tên lửa, "
            "hai mũi tên ngược chiều: động lượng hai phần bằng nhau, trái dấu, tổng vẫn bằng 0.")
fig3 = fig3.replace('<figure class="fig"', '<figure class="fig" data-exp="tn-l10-baotoandl-03"', 1)

# ---------------- Hình 4: chọn chiều dương, dấu của vận tốc ----------------
CUR["fig"] = 4
VB[4] = (440, 200)
AY = 150
b = defs("f4")
b += arrow("f4", "k", 20, AY, 420, AY, 2, name="trục")
b += text(418, AY - 12, "chiều +", "currentColor", 17, "end")
xa, xb, yb = 110, 340, 96
b += f'<circle cx="{xa}" cy="{yb}" r="22" fill="rgba(248,113,113,.2)" stroke="{RED}" stroke-width="2"/>'
b += f'<circle cx="{xb}" cy="{yb}" r="22" fill="rgba(56,189,248,.2)" stroke="{BLUE}" stroke-width="2"/>'
b += text(xa, yb + 5, "A", "currentColor", 17, "middle")
b += text(xb, yb + 5, "B", "currentColor", 17, "middle")
LA, LB = 100, 50
b += arrow("f4", "r", xa + 24, yb, xa + 24 + LA, yb, 3, name="vA")
b += arrow("f4", "b", xb - 24, yb, xb - 24 - LB, yb, 3, name="vB")
b += text(xa + 24 + LA / 2, yb - 16, sub("v", "A", 14) + " &gt; 0", RED, 17, "middle")
b += text(xb - 24 - LB / 2, yb - 16, sub("v", "B", 14) + " &lt; 0", BLUE, 17, "middle")
b += text(xa, AY + 30, "thế dấu +", RED, 17, "middle")
b += text(xb, AY + 30, "thế dấu −", BLUE, 17, "middle")
b += text(xa, 40, "cùng chiều +", RED, 17, "middle", "600")
b += text(xb, 40, "ngược chiều +", BLUE, 17, "middle", "600")
fig4 = wrap(f"0 0 {VB[4][0]} {VB[4][1]}",
            "Trục chiều dương hướng sang phải; vật A chạy sang phải có vận tốc dương, vật B chạy sang trái có vận tốc âm", b,
            "Hình 4. Chọn chiều dương trước. A chạy cùng chiều dương: thế $v_A \\gt 0$. B chạy ngược lại: thế $v_B \\lt 0$, "
            "dù đề chỉ cho tốc độ (số dương).")

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

# ---------------- Ghép ----------------
src = (HERE / "theory.src.html").read_text(encoding="utf8")
src = src.replace("__BANG__", BANG).replace("__NHANXET__", NX)
figs = [re.sub(r"<figcaption>Hình \d\.", f"<figcaption>Hình {k}.", f) for k, f in enumerate((fig1, fig2, fig3, fig4), 1)]
order = [int(k) for k in re.findall(r"<!--FIG(\d)-->", src)]
assert order == list(range(1, len(figs) + 1)), order
for k, f in enumerate(figs, 1):
    src = src.replace(f"<!--FIG{k}-->", f)

lint = ROOT / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = HERE / "theory.html"
out.write_text(src.replace("__PHUT__", "?"), encoding="utf8")
r = subprocess.run([sys.executable, str(lint), str(out), "--json"], capture_output=True, text=True)
mm = re.search(r'"phut"\s*:\s*([\d.]+)', r.stdout)
phut = math.ceil(float(mm.group(1))) if mm else "?"
out.write_text(src.replace("__PHUT__", str(phut)), encoding="utf8")
print("ok", len(src), "ký tự; phút =", phut, "(lint đo", mm.group(1) if mm else "?", ")")

# ---------------- Kho thí nghiệm ----------------
BAI = "Bài 29. Định luật bảo toàn động lượng"
NGUON = "content/lesson-samples/l10-bao-toan-dong-luong/theory.html"
G = 9.8


def base(n, ten, loai, muc_do, kien_thuc):
    return {"mon": "vat-ly", "lop": 10, "bai": BAI, "lesson_id": 74, "nguon_trong_bai": NGUON,
            "id": f"tn-l10-baotoandl-{n:02d}", "ten": ten, "loai": loai, "muc_do": muc_do, "kien_thuc": kien_thuc}


TN = []
t = base(1, "Va chạm mềm trên ray đệm khí, đo bằng cổng quang", "thi_nghiem", "trung_binh",
         ["baotoandl.he_kin", "baotoandl.dinh_luat", "baotoandl.va_cham_mem"])
t.update({
    "muc_tieu": "Đo vận tốc xe 1 trước va chạm và vận tốc chung của hai xe dính nhau sau va chạm với 4 giá trị m2; "
                "thấy m1·v1 ≈ (m1 + m2)·v trong phạm vi sai số, còn động năng giảm rõ.",
    "dung_cu": [{"ten": "Ray đệm khí nằm ngang + máy thổi khí", "so_luong": 1},
                {"ten": "Xe trượt 0,20 kg gắn đầu kim", "so_luong": 1},
                {"ten": "Xe trượt gắn miếng sáp, có chỗ thêm gia trọng", "so_luong": 1},
                {"ten": "Cổng quang điện + đồng hồ đo thời gian, tấm chắn 10 mm", "so_luong": 2},
                {"ten": "Gia trọng 0,10 kg", "so_luong": 4}],
    "cac_buoc": {
        "lam": ["Cân bằng ray cho nằm ngang (xe đặt yên không tự trôi).",
                "Đặt xe 2 (khối lượng m2) đứng yên giữa hai cổng quang.",
                "Đẩy nhẹ xe 1 (m1 = 0,20 kg): cổng quang 1 đo v1; hai xe dính nhau qua cổng quang 2 đo v.",
                "Thêm gia trọng cho m2 = 0,20; 0,30; 0,40; 0,60 kg, lặp lại: 4 lần đo."],
        "quan_sat": ["Hai xe dính nhau đi chậm hơn xe 1 lúc đầu; m2 càng lớn, v càng nhỏ.",
                     "v1 (m/s): " + "; ".join(num(v1) for _, v1, _, _ in DATA) + ". v (m/s): " + "; ".join(num(v) for _, _, v, _ in DATA) + "."],
        "rut_ra": ["p trước = m1·v1 ≈ p sau = (m1 + m2)·v, lệch không quá " + num(max(abs(x) for x in lech), 1) + " %, nằm trong sai số.",
                   "p sau thường không lớn hơn p trước; nếu lớn hơn thì nằm trong phạm vi sai số (ma sát còn sót thường chỉ làm mất bớt động lượng).",
                   "Động năng sau va chạm chỉ còn m1/(m1 + m2) động năng trước: va chạm mềm."]},
    "tham_so": [
        {"ky_hieu": "m1", "ten": "Khối lượng xe 1", "don_vi": "kg", "kieu": "co_dinh", "gia_tri": M1},
        {"ky_hieu": "m2", "ten": "Khối lượng xe 2", "don_vi": "kg", "kieu": "dieu_chinh", "min": 0.1, "max": 1.0, "mac_dinh": 0.2, "buoc": 0.1},
        {"ky_hieu": "v1", "ten": "Vận tốc xe 1 trước va chạm", "don_vi": "m/s", "kieu": "do_duoc", "sai_so_do": 0.005},
        {"ky_hieu": "v", "ten": "Vận tốc chung sau va chạm", "don_vi": "m/s", "kieu": "do_duoc", "sai_so_do": 0.005},
        {"ky_hieu": "p_truoc", "ten": "Động lượng trước", "don_vi": "kg·m/s", "kieu": "tinh_ra"},
        {"ky_hieu": "p_sau", "ten": "Động lượng sau", "don_vi": "kg·m/s", "kieu": "tinh_ra"}],
    "mo_hinh": {"phuong_trinh": ["p_truoc = m1·v1", "p_sau = (m1 + m2)·v", "lý tưởng: v = m1·v1/(m1 + m2)",
                                 "Wđ_sau/Wđ_truoc = m1/(m1 + m2)"],
                "gia_thiet": ["ray nằm ngang, ma sát rất nhỏ (mô hình mất 1,5–2,5 % động lượng giữa hai cổng)",
                              "va chạm xảy ra rất nhanh so với thời gian chạy giữa hai cổng",
                              "v ghi làm tròn 0,01 m/s"]},
    "so_lieu_mau": {"cot": ["m2 (kg)", "v1 (m/s)", "v (m/s)", "p trước (kg·m/s)", "p sau (kg·m/s)"],
                    "hang": [[m2, v1, v, round(a, 3), round(c, 3)] for (m2, v1, v, _), a, c in zip(DATA, pt, ps)],
                    "ghi_chu": "Số liệu minh hoạ: v = m1·v1/(m1 + m2) nhân hệ số mất mát " + ", ".join(str(k) for k in LOSS)
                               + " rồi làm tròn 0,01 m/s; không phải số đo thật."},
    "ket_qua_ky_vong": "p sau ≈ p trước, lệch 0 đến " + num(max(abs(x) for x in lech), 1) + " % và luôn ≤ p trước; lần 1 (m2 = m1) động năng còn 50 %.",
    "hien_tuong_hay_sai": ["Cho rằng sau va chạm hai xe giữ nguyên vận tốc của xe 1.",
                           "Cho rằng động năng cũng được bảo toàn như động lượng.",
                           "Coi chênh lệch vài phần trăm là định luật sai."],
    "sai_so_thuong_gap": ["Ray không thật nằm ngang làm xe tăng/giảm tốc giữa hai cổng.",
                          "Làm tròn v tới 0,01 m/s: sai số tương đối lớn khi v nhỏ (khoảng 3 % ở v = 0,16 m/s)."],
    "goi_y_mo_phong": {"loai": "2d_dong_hoc+bang_so_lieu",
                       "y_tuong": "Thanh trượt m2 và v1; hai xe chạy trên ray, cổng quang hiện số; bảng tự điền p trước, p sau, Wđ trước, Wđ sau.",
                       "diem_nhan": "Hỏi trước: m2 = m1 thì sau va chạm hai xe chạy nhanh bằng mấy phần xe 1 lúc đầu?"}})
TN.append(t)

t = base(2, "Va chạm gần đàn hồi giữa hai xe cùng khối lượng có đệm lò xo", "thi_nghiem", "co_ban",
         ["baotoandl.va_cham_dan_hoi", "baotoandl.dinh_luat"])
t.update({
    "muc_tieu": "Thấy hai xe cùng khối lượng va chạm đàn hồi trực diện thì đổi vận tốc cho nhau: xe 1 dừng, xe 2 đi tiếp với vận tốc của xe 1.",
    "dung_cu": [{"ten": "Ray đệm khí nằm ngang + máy thổi khí", "so_luong": 1},
                {"ten": "Xe trượt cùng khối lượng gắn vòng lò xo lá ở đầu", "so_luong": 2},
                {"ten": "Cổng quang điện + đồng hồ đo thời gian (tuỳ chọn)", "so_luong": 2}],
    "cac_buoc": {"lam": ["Đặt xe 2 đứng yên giữa ray.", "Đẩy xe 1 tới va thẳng vào xe 2 qua vòng lò xo lá."],
                 "quan_sat": ["Xe 1 gần như dừng hẳn ngay sau va chạm.",
                              "Xe 2 lao đi với tốc độ gần bằng tốc độ xe 1 lúc đầu."],
                 "rut_ra": ["Va chạm gần đàn hồi: động lượng và động năng đều được chuyển gần trọn từ xe 1 sang xe 2.",
                            "Hai vật bằng khối lượng va chạm đàn hồi trực diện thì đổi vận tốc cho nhau."]},
    "tham_so": [
        {"ky_hieu": "m", "ten": "Khối lượng mỗi xe", "don_vi": "kg", "kieu": "co_dinh", "gia_tri": 0.2},
        {"ky_hieu": "v1", "ten": "Vận tốc xe 1 trước va chạm", "don_vi": "m/s", "kieu": "dieu_chinh", "min": 0.1, "max": 1.0, "mac_dinh": 0.5, "buoc": 0.05},
        {"ky_hieu": "v1_sau", "ten": "Vận tốc xe 1 sau va chạm", "don_vi": "m/s", "kieu": "tinh_ra"},
        {"ky_hieu": "v2_sau", "ten": "Vận tốc xe 2 sau va chạm", "don_vi": "m/s", "kieu": "tinh_ra"}],
    "mo_hinh": {"phuong_trinh": ["v1' = ((m1 − m2)·v1 + 2·m2·v2)/(m1 + m2)", "v2' = ((m2 − m1)·v2 + 2·m1·v1)/(m1 + m2)",
                                 "m1 = m2, v2 = 0 ⇒ v1' = 0, v2' = v1"],
                "gia_thiet": ["va chạm trực diện, đàn hồi hoàn toàn", "bỏ qua ma sát của ray"]},
    "so_lieu_mau": {"cot": ["v1 (m/s)", "v1' (m/s)", "v2' (m/s)"],
                    "hang": [[0.3, 0.0, 0.3], [0.5, 0.0, 0.5], [0.8, 0.0, 0.8]],
                    "ghi_chu": "Số liệu tính từ mô hình đàn hồi lý tưởng, m1 = m2; xe thật mất vài phần trăm động năng ở lò xo."},
    "ket_qua_ky_vong": "Xe 1 dừng, xe 2 đi với vận tốc bằng vận tốc ban đầu của xe 1.",
    "hien_tuong_hay_sai": ["Đoán hai xe cùng đi với một nửa tốc độ (nhầm với va chạm mềm).",
                           "Đoán xe 1 bật ngược lại với cùng tốc độ."],
    "goi_y_mo_phong": {"loai": "2d_dong_hoc",
                       "y_tuong": "Thanh trượt m2/m1 từ 0,2 đến 5; cho thấy m2 = m1 thì xe 1 dừng, m2 > m1 thì xe 1 bật lùi, m2 < m1 thì xe 1 đi tiếp chậm hơn.",
                       "diem_nhan": "Hỏi trước: va chạm đàn hồi, hai xe bằng nhau, xe 1 sẽ làm gì?"}})
TN.append(t)

t = base(3, "Tên lửa bóng bay chạy trên sợi cước", "thi_nghiem", "co_ban", ["baotoandl.phan_luc"])
t.update({
    "muc_tieu": "Thấy khí phụt ra phía sau thì bóng lao về phía trước, không cần đẩy vào vật nào bên ngoài: chuyển động bằng phản lực.",
    "dung_cu": [{"ten": "Bóng bay", "so_luong": 1}, {"ten": "Ống hút", "so_luong": 1},
                {"ten": "Sợi cước dài khoảng 5 m", "so_luong": 1}, {"ten": "Băng dính", "so_luong": 1}],
    "cac_buoc": {"lam": ["Căng sợi cước nằm ngang ngang lớp, xỏ qua ống hút.",
                         "Thổi căng bóng, bóp miệng bóng, dán bóng vào ống hút (miệng bóng hướng về một đầu dây).",
                         "Buông tay."],
                 "quan_sat": ["Khí phụt ra phía sau, bóng lao về phía trước dọc sợi cước."],
                 "rut_ra": ["Khí phụt ra mang động lượng về sau thì bóng nhận động lượng về trước, tổng vẫn gần bằng 0.",
                            "Chuyển động bằng phản lực: V = −(m/M)·v."]},
    "tham_so": [
        {"ky_hieu": "m", "ten": "Khối lượng khí phụt ra (mỗi đợt)", "don_vi": "kg", "kieu": "dieu_chinh", "min": 0.001, "max": 0.01, "mac_dinh": 0.003, "buoc": 0.001},
        {"ky_hieu": "v", "ten": "Vận tốc khí phụt ra (so với đất)", "don_vi": "m/s", "kieu": "dieu_chinh", "min": 5, "max": 30, "mac_dinh": 15, "buoc": 1},
        {"ky_hieu": "M", "ten": "Khối lượng bóng + ống hút còn lại", "don_vi": "kg", "kieu": "co_dinh", "gia_tri": 0.006},
        {"ky_hieu": "V", "ten": "Vận tốc bóng", "don_vi": "m/s", "kieu": "tinh_ra"}],
    "mo_hinh": {"phuong_trinh": ["m·v + M·V = 0", "V = −(m/M)·v"],
                "gia_thiet": ["xét một đợt phụt ngắn, hệ ban đầu đứng yên", "bỏ qua ma sát ống hút–cước và sức cản không khí trong đợt phụt",
                              "mô hình phụt tức thời, không phải tên lửa phụt liên tục"]},
    "so_lieu_mau": {"cot": ["m (g)", "v (m/s)", "V (m/s)"],
                    "hang": [[1, 15, -2.5], [2, 15, -5.0], [3, 15, -7.5]],
                    "ghi_chu": "Số liệu minh hoạ tính từ V = −(m/M)·v với M = 6 g; không phải số đo thật."},
    "ket_qua_ky_vong": "Bóng chuyển động ngược chiều khí phụt; khí phụt càng nhiều, càng nhanh thì bóng càng nhanh.",
    "hien_tuong_hay_sai": ["Cho rằng bóng chạy được vì khí 'đẩy vào không khí phía sau'.",
                           "Cho rằng trong chân không tên lửa không chuyển động được."],
    "an_toan": ["Không đứng trên ghế để căng dây; buộc dây ở độ cao vừa tầm."],
    "goi_y_mo_phong": {"loai": "2d_dong_hoc+so_do_luc",
                       "y_tuong": "Bóng trên dây; mỗi lần bấm phụt một gói khí m với v; vẽ hai mũi tên động lượng bằng nhau, ngược chiều.",
                       "diem_nhan": "Hỏi trước: đặt bóng trong buồng chân không thì bóng còn chạy không?"}})
TN.append(t)

t = base(4, "Cú ôm trên sân băng (va chạm mềm, vật 2 đứng yên)", "vi_du", "co_ban",
         ["baotoandl.he_kin", "baotoandl.va_cham_mem"])
t.update({
    "muc_tieu": "Dự đoán vận tốc chung khi một bạn đang trượt ôm một bạn đứng yên trên băng; thấy động lượng giữ nguyên còn động năng giảm.",
    "dung_cu": [{"ten": "Sân băng (tình huống đời sống)", "so_luong": 1}],
    "cac_buoc": {"lam": ["An (50 kg) trượt 4 m/s tới ôm Bình (50 kg) đang đứng yên."],
                 "quan_sat": ["Sau cú ôm hai bạn cùng lướt đi chậm hơn An lúc đầu, rồi chậm dần và dừng do ma sát nhỏ của băng."],
                 "rut_ra": ["Ngay trước và ngay sau cú ôm, hệ kín: 50·4 = 100·v ⇒ v = 2 m/s.",
                            "Động năng giảm từ 400 J còn 200 J: va chạm mềm.",
                            "Quãng lướt dài sau đó không dùng bảo toàn động lượng được vì ma sát tác dụng lâu."]},
    "tham_so": [
        {"ky_hieu": "m1", "ten": "Khối lượng An", "don_vi": "kg", "kieu": "dieu_chinh", "min": 30, "max": 80, "mac_dinh": 50, "buoc": 5},
        {"ky_hieu": "m2", "ten": "Khối lượng Bình", "don_vi": "kg", "kieu": "dieu_chinh", "min": 30, "max": 80, "mac_dinh": 50, "buoc": 5},
        {"ky_hieu": "v1", "ten": "Vận tốc An trước cú ôm", "don_vi": "m/s", "kieu": "dieu_chinh", "min": 1, "max": 6, "mac_dinh": 4, "buoc": 0.5},
        {"ky_hieu": "v", "ten": "Vận tốc chung", "don_vi": "m/s", "kieu": "tinh_ra"}],
    "mo_hinh": {"phuong_trinh": ["m1·v1 = (m1 + m2)·v", "Wđ_truoc = m1·v1²/2", "Wđ_sau = (m1 + m2)·v²/2"],
                "gia_thiet": ["bỏ qua ma sát của băng trong lúc ôm", "chuyển động trên một đường thẳng"]},
    "so_lieu_mau": {"cot": ["m1 (kg)", "m2 (kg)", "v1 (m/s)", "v (m/s)"],
                    "hang": [[50, 50, 4, 2.0], [50, 30, 4, 2.5], [40, 60, 5, 2.0]],
                    "ghi_chu": "Tính từ mô hình."},
    "ket_qua_ky_vong": "v = 2 m/s khi hai bạn nặng bằng nhau; động năng còn một nửa.",
    "hien_tuong_hay_sai": ["Cho rằng hai bạn giữ nguyên 4 m/s.", "Cho rằng động năng được giữ nguyên nên v ≈ 2,8 m/s."],
    "goi_y_mo_phong": {"loai": "2d_dong_hoc",
                       "y_tuong": "Hai người que trên băng; thanh trượt khối lượng và vận tốc; hiện cột động lượng và động năng trước/sau.",
                       "diem_nhan": "Hỏi trước: sau cú ôm hai bạn lướt nhanh bao nhiêu?"}})
TN.append(t)

for t in TN:
    assert t["muc_do"] in ("co_ban", "trung_binh", "nang_cao")
    p = ROOT / "content/thi-nghiem" / f"{t['id']}.json"
    p.write_text(json.dumps(t, ensure_ascii=False, indent=1), encoding="utf8")
print("thí nghiệm:", ", ".join(t["id"] for t in TN))

if bad:
    sys.exit(1)
