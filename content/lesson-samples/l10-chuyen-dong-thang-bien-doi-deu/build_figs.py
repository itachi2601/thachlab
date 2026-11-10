"""Sinh 4 hình SVG cho bài 'Chuyển động thẳng biến đổi đều' (lesson 54), thay mốc <!--FIGn--> trong theory.src.html -> theory.html.
Toạ độ đồ thị TÍNH từ phương trình (v = v0 + at) qua hàm đổi trục; lớp kiểm: hộp nhãn không chồng nhau, không vượt viewBox,
không bị đường đồ thị/mũi tên cắt xuyên; điểm cắt, độ dốc, diện tích đối chiếu lại với số trong bài.
Chạy: python3 build_figs.py   (sau đó: python3 build_bundle.py)"""
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from _margin_fig import margin_figs
import math, pathlib, re, subprocess, sys
from svg_lib import RED, BLUE, ORG, GRN, wrap
import importlib.util as _iu
_sp = _iu.spec_from_file_location("svg_lib_skill", _pl.Path(__file__).resolve().parents[3] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/svg_lib.py")
_sl = _iu.module_from_spec(_sp); _sp.loader.exec_module(_sl)
chevron = _sl.chevron          # đầu mũi tên chữ V 30° (thầy chốt 7/10/2026), không dùng marker tam giác

HERE = pathlib.Path(__file__).resolve().parent
COL = {"r": RED, "b": BLUE, "o": ORG, "g": GRN}


def sub(base, s, size=12):
    return f'{base}<tspan baseline-shift="sub" font-size="{max(size, 14)}">{s}</tspan>'


class Canvas:
    def __init__(self, name, w, h):
        self.name, self.w, self.h = name, w, h
        self.body, self.labels, self.markers, self.segs = "", [], set(), []

    def add(self, s):
        self.body += s

    def line(self, x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, obstacle=True):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.body += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"/>'
        if obstacle:
            self.segs.append((x1, y1, x2, y2))

    def dot(self, x, y, r=4, c="currentColor"):
        self.body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'

    def arr(self, c, x1, y1, x2, y2, w=3, head=11):
        """Mũi tên có ĐỈNH đúng tại (x2,y2); đầu chữ V 30° (chevron), không dùng marker."""
        col = COL.get(c, "currentColor")
        self.body += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}"/>'
                      + chevron(x2, y2, x2 - x1, y2 - y1, col, w, head))
        self.segs.append((x1, y1, x2, y2))

    def text(self, x, y, s, c="currentColor", size=14, anchor="start", weight="700", italic=False):
        st = ' font-style="italic" font-family="serif"' if italic else ""
        self.body += f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"{st}>{s}</text>'
        plain = re.sub(r"<[^>]+>", "", s)
        wdt = 0.58 * size * len(plain)
        x0 = x if anchor == "start" else (x - wdt / 2 if anchor == "middle" else x - wdt)
        self.labels.append((plain, x0, y - 0.78 * size, x0 + wdt, y + 0.22 * size, size))

    def defs(self):
        out = "<defs>"
        for c, hd in sorted(self.markers):
            out += (f'<marker id="{self.name}-{c}{hd}" viewBox="0 0 10 10" refX="0" refY="5" markerWidth="{hd}" markerHeight="{hd}" '
                    f'markerUnits="userSpaceOnUse" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{COL.get(c, "currentColor")}"/></marker>')
        return out + "</defs>"

    def check(self):
        errs = []
        for i, a in enumerate(self.labels):
            if a[5] < 14:
                errs.append(f"{self.name}: nhãn '{a[0]}' cỡ {a[5]} < 14")
            if a[1] < 2 or a[3] > self.w - 2 or a[2] < 0 or a[4] > self.h:
                errs.append(f"{self.name}: nhãn '{a[0]}' vượt viewBox {tuple(round(v) for v in a[1:5])}")
            for b in self.labels[i + 1:]:
                if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    errs.append(f"{self.name}: nhãn '{a[0]}' chồng '{b[0]}'")
            for (x1, y1, x2, y2) in self.segs:          # đường cắt xuyên hộp nhãn (lấy mẫu 200 điểm)
                for k in range(201):
                    px, py = x1 + (x2 - x1) * k / 200, y1 + (y2 - y1) * k / 200
                    if a[1] + 1 < px < a[3] - 1 and a[2] + 1 < py < a[4] - 1:
                        errs.append(f"{self.name}: đường ({x1:.0f},{y1:.0f})→({x2:.0f},{y2:.0f}) cắt nhãn '{a[0]}'")
                        break
        return errs

    def svg(self, label, cap, exp=None):
        s = wrap(f"0 0 {self.w} {self.h}", label, self.defs() + self.body, cap)
        if exp:
            s = s.replace('<figure class="fig" data-tl="1">', f'<figure class="fig" data-tl="1" data-exp="{exp}">', 1)
        return s


class Plot:
    """Hệ trục v–t: gốc (ox, oy) màn hình, kx px/s, kv px/(m/s)."""

    def __init__(self, c, ox, oy, kx, kv, tmax, vmax, tticks, vticks):
        self.c, self.ox, self.oy, self.kx, self.kv = c, ox, oy, kx, kv
        X, Y = self.X, self.Y
        c.arr("k", ox, oy, X(tmax) + 22, oy, 1.8, 9)
        c.arr("k", ox, oy, ox, Y(vmax) - 22, 1.8, 9)
        for t in tticks:
            c.line(X(t), oy, X(t), oy + 5, "currentColor", 1.5, obstacle=False)
            c.text(X(t), oy + 20, f"{t:g}", size=14, anchor="middle", weight="600")
        for v in vticks:
            c.line(ox - 5, Y(v), ox, Y(v), "currentColor", 1.5, obstacle=False)
            c.text(ox - 9, Y(v) + 5, f"{v:g}", size=14, anchor="end", weight="600")
        c.text(ox - 8, oy + 20, "O", size=14, anchor="end", weight="600")
        c.text(X(tmax) + 4, oy + 20, "t (s)", size=14, weight="600")   # dưới trục, tránh nhãn đường đồ thị ở mép phải
        c.text(ox + 8, Y(vmax) - 12, "v (m/s)", size=14, weight="600")

    def X(self, t):
        return self.ox + self.kx * t

    def Y(self, v):
        return self.oy - self.kv * v


ERR = []

# ---------------- Hình 1: mở bài — hai lần phanh, 36 km/h dừng sau 10 m; 72 km/h: ? (không lộ đáp án)
# Lời văn: "Một xe máy" → vẽ XE MÁY có người lái (bản trước vẽ ô tô, lệch lời văn).
c = Canvas("f1", 400, 270)
K = 7.0                      # px / m
XB = 132                     # chỗ bắt đầu phanh (mép trước bánh trước)
RW = 9                       # bán kính bánh xe


def bike(xf, yr, col):
    """Xe máy hướng sang phải, mép trước bánh trước tại x = xf; người lái ngồi trên yên."""
    fx, rx, wy = xf - RW, xf - RW - 42, yr - RW            # tâm bánh trước, bánh sau
    g = ""
    for wx in (fx, rx):
        g += f'<circle cx="{wx}" cy="{wy}" r="{RW}" fill="none" stroke="currentColor" stroke-width="2.2"/>'
        g += f'<circle cx="{wx}" cy="{wy}" r="2" fill="currentColor"/>'
    # thân xe (yên + bình xăng), càng sau, phuộc trước, tay lái
    g += (f'<path d="M{rx-4},{wy-12} L{rx+26},{wy-12} L{rx+34},{wy-18} L{fx-8},{wy-18} L{fx-6},{wy-8} L{rx+10},{wy-4} Z" '
          f'fill="{col}" fill-opacity=".45" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>')
    g += f'<line x1="{rx}" y1="{wy}" x2="{rx+12}" y2="{wy-5}" stroke="currentColor" stroke-width="2.2"/>'
    g += f'<line x1="{fx}" y1="{wy}" x2="{fx-9}" y2="{wy-26}" stroke="currentColor" stroke-width="2.4"/>'
    g += f'<line x1="{fx-13}" y1="{wy-27}" x2="{fx-4}" y2="{wy-29}" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/>'
    # người lái: hông trên yên, lưng hơi ngả trước, tay nắm lái, chân đặt gác chân
    hx, hy = rx + 14, wy - 14                               # hông ngay trên yên (đỉnh thân ở wy-12)
    sx, sy = rx + 22, wy - 40
    g += f'<circle cx="{sx+3}" cy="{sy-9}" r="7" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    g += f'<line x1="{hx}" y1="{hy}" x2="{sx}" y2="{sy}" stroke="currentColor" stroke-width="2.4"/>'
    g += f'<polyline points="{sx},{sy+4} {sx+12},{sy+12} {fx-11},{wy-28}" fill="none" stroke="currentColor" stroke-width="2.2"/>'
    g += f'<polyline points="{hx},{hy} {rx+28},{wy-26} {rx+31},{wy-17}" fill="none" stroke="currentColor" stroke-width="2.2"/>'   # chân gập, bàn chân đặt trên thân, không xuyên thân
    c.add(g)
    return sx + 3, sy - 16                                  # đỉnh đầu (để kiểm nhãn không chạm)


for lane, (yr, kmh, col) in enumerate(((112, "36 km/h", ORG), (222, "72 km/h", BLUE))):
    c.line(14, yr, 390, yr, "currentColor", 2, obstacle=False)                     # mặt đường
    top = bike(XB, yr, col)
    c.text(14, yr - 34, kmh, size=14)
    assert 14 + 0.58 * 14 * len(kmh) < XB - RW - 42 - 4, "nhãn tốc độ chạm xe"     # nhãn ở trái bánh sau, không chạm xe/người
    c.line(XB, yr - 62, XB, yr + 6, RED, 2, "4 3", obstacle=False)                 # vạch bắt đầu phanh
    if lane == 0:
        XS = XB + 10 * K
        c.line(XS, yr - 44, XS, yr + 6, "currentColor", 2.4, obstacle=False)       # vạch dừng
        c.line(XB + 2, yr + 18, XS - 2, yr + 18, "currentColor", 1.5, obstacle=False)
        c.add(f'<path d="M{XB+2},{yr+13} v10 M{XS-2},{yr+13} v10" stroke="currentColor" stroke-width="1.5"/>')
        c.text((XB + XS) / 2, yr + 36, "10 m", size=14, anchor="middle")
        c.text(XS + 8, yr - 30, "dừng", size=14, weight="600")
    else:
        c.line(XB + 2, yr + 18, 398, yr + 18, "currentColor", 1.5, "5 4", obstacle=False)   # kéo hết lề: không gợi ý chỗ dừng
        c.text(262, yr + 38, "dừng ở đâu?", size=14, anchor="middle")
c.text(XB + 6, 26, "bắt đầu phanh", RED, 14, weight="600")
fig1 = c.svg("Hai lần phanh cùng một xe máy: ở 36 km/h xe dừng sau 10 m; ở 72 km/h chưa biết xe dừng ở đâu",
             "Hình 1. Cùng xe, cùng đường, cùng cách phanh. Chỉ khác tốc độ lúc bắt đầu phanh.")
ERR += c.check()

# ---------------- Hình 2: đồ thị v–t ba xe. A: v = 1 + t; B: v = 7 − t; C: v = 3
c = Canvas("f2", 440, 300)
p = Plot(c, 50, 252, 46, 25, 6.4, 8, [1, 2, 3, 4, 5, 6], [2, 4, 6, 8])
X, Y = p.X, p.Y
LINES = {"A": (1, 1, GRN), "B": (7, -1, ORG), "C": (3, 0, BLUE)}     # v0, a, màu
for n, (v0, a, col) in LINES.items():
    c.line(X(0), Y(v0), X(6), Y(v0 + a * 6), col, 3.2)
    c.text(X(6) + 8, Y(v0 + a * 6) + 5, n, col, 15)
# tam giác độ dốc trên A, từ t = 4 đến 6
c.line(X(4), Y(5), X(6), Y(5), "currentColor", 1.6, "4 3", obstacle=False)
c.line(X(6), Y(5), X(6), Y(7), "currentColor", 1.6, "4 3", obstacle=False)
c.text(X(5), Y(5) + 17, "Δt = 2 s", size=14, anchor="middle", weight="600")
c.text(X(6) + 8, Y(6) + 5, "Δv = 2 m/s", size=14, weight="600")
# chú giải
for k, (n, s) in enumerate((("A", "nhanh dần đều"), ("B", "chậm dần đều"), ("C", "thẳng đều"))):
    col = LINES[n][2]
    c.text(150, 26 + 18 * k, f"{n}: {s}", col, 14, weight="700")
# kiểm: A, B cắt nhau tại t = 3 s, v = 4 m/s (dùng ở Câu 1 và Câu 5); độ dốc B = −1
tA = (7 - 1) / (1 - (-1))
if abs(tA - 3) > 1e-9 or abs(1 + tA - 4) > 1e-9:
    ERR.append("f2: A, B không cắt nhau tại (3 s; 4 m/s)")
if (Y(1) - Y(7)) / (X(6) - X(0)) * (-p.kx / p.kv) != -1:
    ERR.append("f2: độ dốc B trên hình khác −1 m/s²")
fig2 = c.svg("Đồ thị vận tốc theo thời gian của ba xe: A dốc lên, B dốc xuống, C nằm ngang; tam giác độ dốc trên A",
             r"Hình 2. Đồ thị <em>v</em>–<em>t</em>: A nhanh dần đều ($v_0 = 1\ \text{m/s}$, dốc lên), B chậm dần đều ($v_0 = 7\ \text{m/s}$, dốc xuống), C thẳng đều. Tam giác nét đứt: độ dốc của A là $a = 2/2 = 1\ \text{m/s}^2$.")
ERR += c.check()

# ---------------- Hình 3: diện tích dưới đồ thị v–t = độ dịch chuyển. v0 = 2, a = 1, t = 0..4
c = Canvas("f3", 400, 290)
V0, A3, T3 = 2, 1, 4
V3 = V0 + A3 * T3
p = Plot(c, 50, 248, 64, 28, 4.6, 7, [1, 2, 3, 4], [2, 4, 6])
X, Y = p.X, p.Y
c.add(f'<rect x="{X(0)}" y="{Y(V0)}" width="{X(T3)-X(0)}" height="{Y(0)-Y(V0)}" fill="rgba(56,189,248,.28)"/>')
c.add(f'<polygon points="{X(0)},{Y(V0)} {X(T3)},{Y(V3)} {X(T3)},{Y(V0)}" fill="rgba(52,211,153,.30)"/>')
c.line(X(0), Y(V0), X(T3), Y(V3), "currentColor", 3)
c.line(X(T3), Y(V3), X(T3), Y(0), "currentColor", 1.4, "4 3", obstacle=False)
c.line(X(0), Y(V0), X(T3), Y(V0), "currentColor", 1.2, "3 3", .6, obstacle=False)
c.text((X(0) + X(T3)) / 2, (Y(V0) + Y(0)) / 2 + 6, sub("v", "0", 12) + "t = 8 m", size=15, anchor="middle")
gx, gy = (X(0) + 2 * X(T3)) / 3, (Y(V0) * 2 + Y(V3)) / 3       # trọng tâm tam giác
c.text(gx + 6, gy + 10, "½at² = 8 m", size=15, anchor="middle")
c.text(X(T3) + 8, Y(V3) - 4, "v = 6 m/s", size=14, weight="600")
area = (V0 + V3) / 2 * T3
if area != 16 or V0 * T3 != 8 or 0.5 * A3 * T3 ** 2 != 8:
    ERR.append("f3: diện tích không khớp 8 + 8 = 16 m")
fig3 = c.svg("Hình thang dưới đồ thị v–t chia thành hình chữ nhật v0 t bằng 8 m và tam giác một nửa a t bình phương bằng 8 m",
             r"Hình 3. $v_0 = 2\ \text{m/s}$, $a = 1\ \text{m/s}^2$, $t = 4\ \text{s}$.<br>Diện tích hình thang $= \dfrac{2 + 6}{2}\cdot 4 = 8 + 8 = 16\ \text{m}$.<br>Chữ nhật xanh dương là $v_0t$.<br>Tam giác xanh lá là $\tfrac12at^2$.")
ERR += c.check()

# ---------------- Hình 4: bài toán mẫu — ô tô v = 2t, xe máy v = 10
c = Canvas("f4", 412, 300)
p = Plot(c, 55, 252, 25, 8, 12, 24, [5, 10], [10, 20])
X, Y = p.X, p.Y
TC, TG = 5, 10                            # cùng vận tốc; gặp nhau
c.add(f'<polygon points="{X(0)},{Y(10)} {X(TC)},{Y(10)} {X(0)},{Y(0)}" fill="rgba(56,189,248,.32)"/>')
c.add(f'<polygon points="{X(TC)},{Y(10)} {X(TG)},{Y(10)} {X(TG)},{Y(20)}" fill="rgba(251,146,60,.32)"/>')
c.line(X(0), Y(0), X(12), Y(24), ORG, 3.2)
c.line(X(0), Y(10), X(12), Y(10), BLUE, 3.2)
c.line(X(TG), Y(20), X(TG), Y(0), "currentColor", 1.4, "4 3", obstacle=False)
c.dot(X(TC), Y(10), 4.5)
c.text(X(0) + 8, Y(10) - 10, "xe máy: v = 10", BLUE, 14)
c.text(X(8.6), Y(17.2) - 14, "ô tô: v = 2t", ORG, 14, anchor="end")
c.text((X(0) * 2 + X(TC)) / 3 + 2, (Y(10) * 2 + Y(0)) / 3 + 5, "25 m", size=14, anchor="middle")
c.text((X(TC) + 2 * X(TG)) / 3 - 2, (Y(10) * 2 + Y(20)) / 3 + 5, "25 m", size=14, anchor="middle")
c.text(X(TG) + 8, Y(10) + 26, "gặp nhau", size=14, weight="600")
c.text(X(TG) + 8, Y(10) + 43, "t = 10 s", size=14, weight="600")
# kiểm: diện tích hai phần bằng nhau = 25 m, tổng mỗi xe 100 m
s1 = 0.5 * TC * 10
s2 = 0.5 * (TG - TC) * (2 * TG - 10)
if s1 != 25 or s2 != 25 or 0.5 * 2 * TG ** 2 != 100 or 10 * TG != 100:
    ERR.append("f4: diện tích không khớp")
fig4 = c.svg("Đồ thị v–t của ô tô (đường dốc lên v = 2t) và xe máy (đường ngang v = 10); hai phần tô màu 25 m bằng nhau, gặp nhau lúc 10 s",
             "Hình 4. Phần tô xanh (0–5&nbsp;s): xe máy bỏ xa ô tô thêm 25&nbsp;m.<br>Phần tô cam (5–10&nbsp;s): ô tô đuổi lại đúng 25&nbsp;m.<br>Hai đường cắt nhau lúc 5&nbsp;s là <strong>cùng vận tốc</strong>.<br>Gặp nhau lúc 10&nbsp;s.",
             exp="tn-l10-ctbdd-03")
ERR += c.check()

if ERR:
    print("\n".join("✗ " + e for e in ERR)); sys.exit(1)

# ---- Ảnh OpenStax College Physics 2e (28/10/2026): Hình 4 mới (Hình 2.46), xem nguon.md. Hình 4 cũ thành Hình 5.
figA = ('<figure class="fig"><img src="/assets/openstax/l10-chuyen-dong-thang-bien-doi-deu/hinh-x-v-a-theo-t.webp" alt="Ba đồ thị chồng nhau theo thời gian của một xe phản lực có gia tốc không đổi: x–t cong lên, v–t đường thẳng dốc lên, a–t đường nằm ngang" loading="lazy" width="594" height="1397">'
        '<figcaption>Hình 4. Cùng một chuyển động, ba đồ thị:<br>(a) <em>x</em>–<em>t</em> cong lên, (b) <em>v</em>–<em>t</em> thẳng dốc lên, (c) <em>a</em>–<em>t</em> nằm ngang.<br>Sách lấy <em>a</em> = 5,0 m/s² chỉ làm ví dụ.<br>'
        '<small>Hình: OpenStax, College Physics 2e, Hình 2.46 — CC BY‑NC‑SA 4.0 — openstax.org/books/college-physics-2e</small></figcaption></figure>')
fig4 = fig4.replace("Hình 4.", "Hình 5.", 1)
h = (HERE / "theory.src.html").read_text(encoding="utf8")
for mark, fg in (("1", fig1), ("2", fig2), ("3", fig3), ("3B", figA), ("4", fig4)):
    assert f"<!--FIG{mark}-->" in h, mark
    h = h.replace(f"<!--FIG{mark}-->", fg)
tmp = HERE / ".theory.tmp.html"
tmp.write_text(h.replace("__PHUT__", "15"), encoding="utf8")
lint = HERE.parents[2] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
out = subprocess.run([sys.executable, str(lint), str(tmp)], capture_output=True, text=True).stdout
tmp.unlink()
m = re.search(r"~?(\d+(?:[.,]\d+)?)\s*phút", out)
phut = round(float(m.group(1).replace(",", "."))) if m else None
if phut is None:
    print("! không đọc được số phút từ lint_do_dai:\n" + out[:600]); sys.exit(1)
h = h.replace("__PHUT__", str(phut))
(HERE / "theory.html").write_text(margin_figs(h), encoding="utf8")
print(f"ok theory.html {len(h)} ký tự · 4 hình · {phut} phút")
