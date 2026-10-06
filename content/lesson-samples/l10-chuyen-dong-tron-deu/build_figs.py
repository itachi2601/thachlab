"""Sinh 4 hình SVG cho Bài 31 Động học của chuyển động tròn đều (Vật lí 10, lesson 76),
điền số liệu thí nghiệm đo (tính từ mô hình) vào theory.src.html và dựng theory.html.
Chạy: python3 build_figs.py   (từ thư mục bài)

Màu dùng chung cả bài: RED = vectơ vận tốc · GRN = quỹ đạo / cung đi được · ORG = vật, điểm, góc θ ·
chữ và nét phụ dùng currentColor. Mọi toạ độ tính từ phương trình đường tròn; cuối mỗi hình có lớp
kiểm hộp nhãn ↔ nét vẽ (không chồng, không vượt viewBox) — sai là dừng, không sinh hình.
"""
import math, re
from svg_lib import RED, BLUE, ORG, GRN, defs

FS = 17      # cỡ nhãn (viewBox 420 thu ~0,78 ở 360px → ≥13px hiển thị)
FS_SUB = 13  # chỉ số dưới (≥13)


class Fig:
    def __init__(self, prefix, w, h):
        self.p, self.w, self.h = prefix, w, h
        self.body = defs(prefix)
        self.segs = []    # (x1, y1, x2, y2) nét vẽ mà nhãn không được đè
        self.boxes = []   # (x0, y0, x1, y1, chữ)

    # ---------- nét vẽ
    def line(self, x1, y1, x2, y2, c="currentColor", w=2, dash="", op=1, guard=True):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.body += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" '
                      f'stroke-width="{w}"{d} opacity="{op}"/>')
        if guard:
            self.segs.append((x1, y1, x2, y2))

    def arrow(self, x1, y1, x2, y2, c="r", w=3):
        col = {"r": RED, "b": BLUE, "o": ORG, "g": GRN}[c]
        self.body += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" '
                      f'stroke-width="{w}" marker-end="url(#{self.p}-{c})"/>')
        # đầu mũi tên nhô thêm ~ 6 đơn vị theo hướng mũi tên
        L = math.hypot(x2 - x1, y2 - y1)
        ex, ey = x2 + 6 * (x2 - x1) / L, y2 + 6 * (y2 - y1) / L
        self.segs.append((x1, y1, ex, ey))

    def arc(self, cx, cy, r, a0, a1, c=GRN, w=3, dash="", op=1, head=None):
        """Cung tròn tâm (cx,cy), bán kính r, từ góc a0 tới a1 (độ, chiều dương = ngược kim đồng hồ
        như toán học; trục y của SVG hướng xuống nên y = cy − r·sinφ)."""
        n = max(8, int(abs(a1 - a0) / 3))
        pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)),
                cy - r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]
        d = f' stroke-dasharray="{dash}"' if dash else ""
        mk = f' marker-end="url(#{self.p}-{head})"' if head else ""
        self.body += (f'<polyline fill="none" stroke="{c}" stroke-width="{w}"{d} opacity="{op}"{mk} points="'
                      + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '"/>')
        for a, b in zip(pts, pts[1:]):
            self.segs.append((*a, *b))
        return pts

    def dot(self, x, y, r=5, c=ORG):
        self.body += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{c}"/>'
        self.segs += [(x - r, y - r, x + r, y + r), (x - r, y + r, x + r, y - r)]

    def raw(self, s):
        self.body += s

    # ---------- chữ
    @staticmethod
    def _w(s, size):
        s = re.sub(r"<[^>]+>", "", s)
        narrow = sum(ch in "il.,:;' |()1rtfj" for ch in s)
        return (len(s) - narrow) * 0.6 * size + narrow * 0.33 * size

    def text(self, x, y, s, c="currentColor", size=FS, anchor="start", weight="600", italic=False):
        st = ' font-style="italic"' if italic else ""
        self.body += (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" '
                      f'text-anchor="{anchor}"{st}>{s}</text>')
        w = self._w(s, size)
        x0 = {"start": x, "middle": x - w / 2, "end": x - w}[anchor]
        self.boxes.append((x0, y - 0.78 * size, x0 + w, y + 0.22 * size, re.sub(r"<[^>]+>", "", s)))

    def sub(self, x, y, base, s, c="currentColor", anchor="start", italic=True):
        """Nhãn có chỉ số dưới (tspan baseline-shift, không dùng KaTeX trong SVG)."""
        st = ' font-style="italic"' if italic else ""
        self.body += (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{FS}" font-weight="700" '
                      f'text-anchor="{anchor}"{st}>{base}<tspan baseline-shift="sub" font-size="{FS_SUB}">{s}</tspan></text>')
        w = self._w(base, FS) + self._w(s, FS_SUB)
        x0 = {"start": x, "middle": x - w / 2, "end": x - w}[anchor]
        self.boxes.append((x0, y - 0.78 * FS, x0 + w, y + 0.22 * FS + 4, base + s))

    # ---------- kiểm
    def check(self, name):
        errs = []
        pad = 1.5
        for (x0, y0, x1, y1, s) in self.boxes:
            if x0 < 2 or y0 < 2 or x1 > self.w - 2 or y1 > self.h - 2:
                errs.append(f"{name}: nhãn '{s}' vượt viewBox ({x0:.0f},{y0:.0f},{x1:.0f},{y1:.0f})")
            for seg in self.segs:
                if seg_hits_box(seg, (x0 - pad, y0 - pad, x1 + pad, y1 + pad)):
                    errs.append(f"{name}: nhãn '{s}' bị nét {tuple(round(v) for v in seg)} cắt")
                    break
        for i, a in enumerate(self.boxes):
            for b in self.boxes[i + 1:]:
                if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
                    errs.append(f"{name}: nhãn '{a[4]}' chồng nhãn '{b[4]}'")
        if errs:
            raise SystemExit("\n".join(errs))
        print(f"{name}: {len(self.boxes)} nhãn, {len(self.segs)} nét — không chồng")

    def svg(self, label, cap, exp=None):
        de = f' data-exp="{exp}"' if exp else ""
        return (f'<figure class="fig" data-tl="1"{de}><svg viewBox="0 0 {self.w} {self.h}" role="img" '
                f'aria-label="{label}">{self.body}</svg><figcaption>{cap}</figcaption></figure>')


def seg_hits_box(seg, box):
    """Đoạn thẳng có cắt (hoặc nằm trong) hình chữ nhật không — Liang–Barsky."""
    x1, y1, x2, y2 = seg
    bx0, by0, bx1, by1 = box
    dx, dy = x2 - x1, y2 - y1
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x1 - bx0), (dx, bx1 - x1), (-dy, y1 - by0), (dy, by1 - y1)):
        if p == 0:
            if q < 0:
                return False
        else:
            t = q / p
            if p < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


def P(cx, cy, r, deg):
    return cx + r * math.cos(math.radians(deg)), cy - r * math.sin(math.radians(deg))


# ================= Hình 1: đội hình xoay trên sân băng (nhìn từ trên) =================
f = Fig("f1", 420, 250)
O = (120, 150)
PHI = 22                       # góc của hàng người so với phương ngang (chỉ là một thời điểm)
RS = (0, 62, 124, 186)         # khoảng cách từng người tới tâm
f.raw('<rect x="8" y="30" width="404" height="212" rx="40" fill="none" stroke="currentColor" '
      'stroke-width="1.5" stroke-dasharray="6 5" opacity="0.4"/>')
f.segs += [(8, 30, 412, 30), (8, 242, 412, 242), (8, 30, 8, 242), (412, 30, 412, 242)]
xe, ye = P(*O, RS[-1], PHI)
f.line(*O, xe, ye, "currentColor", 2.5)                       # tay nắm tay thành một hàng thẳng
for r in RS:
    f.dot(*P(*O, r, PHI), 10, ORG)
f.arc(*O, 44, 200, 320, "currentColor", 2, head="g")        # chiều xoay: ngược chiều kim đồng hồ
f.text(20, 22, "Sân băng nhìn từ trên xuống", "currentColor", FS, "start", "400")
f.text(O[0] - 18, O[1] - 16, "người trụ", "currentColor", FS, "end", "700")
xo, yo = P(*O, RS[-1], PHI)
f.text(xo + 4, yo - 20, "người ngoài cùng", "currentColor", FS, "middle", "700")
f.text(O[0], O[1] + 76, "chiều xoay của cả hàng", "currentColor", FS, "middle", "400")
f.check("Hình 1")
fig1 = f.svg("Sân băng nhìn từ trên: bốn người nắm tay thành một hàng thẳng, người trụ ở tâm, cả hàng xoay quanh tâm ngược chiều kim đồng hồ",
             "Hình 1. Đội hình xoay: cả hàng luôn thẳng, quay quanh người trụ.",
             "tn-l10-trondeu-01")

# ================= Hình 2: độ dịch chuyển góc và radian =================
f = Fig("f2", 420, 250)
O = (120, 140)
R = 100
TH = math.degrees(1.0)          # θ = 1 rad: cung dài đúng bằng bán kính
A = P(*O, R, 0)
B = P(*O, R, TH)
f.arc(*O, R, TH, 360, "currentColor", 1.5, "5 5", 0.4)
f.line(*O, *A, "currentColor", 2)
f.line(*O, *B, "currentColor", 2)
f.arc(*O, R, 0, TH, GRN, 4.5)
f.arc(*O, 26, 0, TH, ORG, 2.2)
f.dot(*O, 4, "currentColor")
f.dot(*A, 5, ORG)
f.dot(*B, 5, ORG)
tx, ty = P(*O, 44, TH / 2)
f.text(tx, ty + 5, "θ", ORG, FS + 2, "middle", "700", True)
sx, sy = P(*O, R + 16, TH / 2)
f.text(sx, sy + 5, "s", GRN, FS + 2, "start", "700", True)
f.text((O[0] + A[0]) / 2, O[1] + 20, "r", "currentColor", FS + 2, "middle", "700", True)
f.text(O[0] - 10, O[1] + 5, "O", "currentColor", FS, "end", "700")
f.text(A[0] + 10, A[1] + 5, "A", "currentColor", FS, "start", "700")
f.text(B[0] + 9, B[1] - 6, "B", "currentColor", FS, "start", "700")
f.text(250, 120, "θ = s/r (rad)", "currentColor", FS, "start", "700")
f.text(250, 150, "Cung s dài bằng r", GRN, FS, "start", "700")
f.text(250, 170, "→ θ = 1 rad ≈ 57°", GRN, FS, "start", "700")
f.check("Hình 2")
fig2 = f.svg("Đường tròn tâm O bán kính r; vật đi từ A tới B theo cung s; góc ở tâm θ bằng s chia r; khi cung dài bằng bán kính thì θ bằng 1 rad, khoảng 57 độ",
             "Hình 2. Vật đi từ A đến B: quãng đường là cung $s$, độ dịch chuyển góc là $\\theta = s/r$. Hình vẽ đúng tỉ lệ cung $s = r$, tức $\\theta = 1\\ \\text{rad}$.")

# ================= Hình 3: cùng ω, khác r → khác v =================
f = Fig("f3", 420, 260)
O = (50, 215)
R1, R2 = 85, 170
TH3 = 50
P1, P2 = P(*O, R1, 0), P(*O, R2, 0)
Q1, Q2 = P(*O, R1, TH3), P(*O, R2, TH3)
f.line(*O, *P2, "currentColor", 1.6, "5 4", 0.6)
f.line(*O, *Q2, "currentColor", 2.2)
f.arc(*O, R1, 0, TH3, GRN, 4)
f.arc(*O, R2, 0, TH3, GRN, 4)
f.arc(*O, 30, 0, TH3, ORG, 2.2)
for q in (P1, P2):
    f.dot(*q, 5, "currentColor")
for q in (Q1, Q2):
    f.dot(*q, 6, ORG)
tx, ty = P(*O, 46, TH3 / 2)
f.text(tx, ty + 5, "θ", ORG, FS + 2, "middle", "700", True)
x, y = P(*O, R1 + 14, TH3 / 2 + 4)
f.sub(x, y + 4, "s", "1", GRN)
x, y = P(*O, R2 + 14, TH3 / 2)
f.sub(x, y + 4, "s", "2", GRN)
f.text(P1[0], O[1] + 24, "r", "currentColor", FS + 1, "middle", "700", True)
f.text(P2[0], O[1] + 24, "2r", "currentColor", FS + 1, "middle", "700", True)
f.text(O[0], O[1] + 24, "O", "currentColor", FS, "middle", "700")
f.text(244, 36, "Cùng thời gian Δt:", "currentColor", FS, "start", "700")
f.text(244, 56, "cùng góc θ (cùng ω)", ORG, FS, "start", "700")
f.text(244, 86, "r gấp đôi", "currentColor", FS, "start", "400")
f.text(244, 106, "→ cung gấp đôi", GRN, FS, "start", "400")
f.text(244, 126, "→ v gấp đôi", RED, FS, "start", "700")
f.check("Hình 3")
fig3 = f.svg("Hai điểm trên cùng một bán kính, cách tâm r và 2r, cùng quay góc θ trong cùng thời gian; cung của điểm ngoài dài gấp đôi nên tốc độ gấp đôi",
             "Hình 3. Hai điểm trên cùng một bán kính quay cùng góc $\\theta$ trong cùng thời gian. Điểm cách tâm $2r$ đi cung $s_2 = 2s_1$, nên $v = \\omega r$ gấp đôi.")

# ================= Hình 4: vectơ vận tốc tiếp tuyến =================
f = Fig("f4", 420, 288)
C = (122, 135)
R = 88
LV = 62                                   # cùng độ dài: tốc độ không đổi
f.arc(*C, R, 0, 360, GRN, 2.5)
f.arc(*C, 30, 30, 150, "currentColor", 2, head="g")   # chiều quay ngược kim đồng hồ
f.dot(*C, 4, "currentColor")
for k, phi in enumerate((90, 205, 330)):
    x, y = P(*C, R, phi)
    f.line(*C, x, y, "currentColor", 1.4, "4 4", 0.55)
    # vận tốc khi quay ngược chiều kim đồng hồ: (−sinφ, cosφ) theo toán học → SVG (−sinφ, −cosφ)
    ux, uy = -math.sin(math.radians(phi)), -math.cos(math.radians(phi))
    f.arrow(x, y, x + LV * ux, y + LV * uy, "r", 3)
    # dấu góc vuông giữa bán kính (hướng vào tâm) và vận tốc
    rx, ry = (C[0] - x) / R, (C[1] - y) / R
    s = 9
    f.raw(f'<polyline fill="none" stroke="currentColor" stroke-width="1.3" points="'
          f'{x + s*rx:.1f},{y + s*ry:.1f} {x + s*rx + s*ux:.1f},{y + s*ry + s*uy:.1f} {x + s*ux:.1f},{y + s*uy:.1f}"/>')
    f.dot(x, y, 5, ORG)
    # nhãn v đặt lệch ra ngoài đường tròn so với đầu mũi tên
    tx, ty = x + (LV + 14) * ux - 8 * rx, y + (LV + 14) * uy - 8 * ry
    if phi == 205:
        tx, ty = x + LV * ux - 16, y + LV * uy + 16
    f.text(tx, ty + 5, "v", RED, FS + 2, "middle", "700", True)
f.text(236, 36, "v vuông góc", "currentColor", FS, "start", "700")
f.text(236, 56, "với bán kính", "currentColor", FS, "start", "700")
f.text(236, 168, "Mũi tên cùng dài:", "currentColor", FS, "start", "400")
f.text(236, 188, "tốc độ không đổi", "currentColor", FS, "start", "700")
f.text(236, 218, "Mũi tên đổi hướng:", "currentColor", FS, "start", "400")
f.text(236, 238, "vận tốc thay đổi", RED, FS, "start", "700")
f.text(20, 280, "Vật quay ngược chiều kim đồng hồ", "currentColor", FS, "start", "400")
f.check("Hình 4")
fig4 = f.svg("Đường tròn quỹ đạo với ba vectơ vận tốc màu đỏ dài bằng nhau, mỗi vectơ tiếp tuyến với đường tròn và vuông góc với bán kính, hướng khác nhau",
             "Hình 4. Ở mọi vị trí, $\\vec v$ tiếp tuyến với quỹ đạo, vuông góc với bán kính. Độ dài không đổi, hướng thì đổi liên tục.")

# ================= Số liệu thí nghiệm đo (lấy từ build_thi_nghiem.py — một nguồn) =================
from build_thi_nghiem import DO_3_VONG, xu_li_do


def vn(x, nd):
    return f"{x:.{nd}f}".replace(".", "{,}")


kq = xu_li_do()
bang = "\n".join(f"<tr><td>{i}</td><td>{t:.1f}</td></tr>".replace(".", ",") for i, t in enumerate(DO_3_VONG, 1))
h = open("theory.src.html", encoding="utf8").read()
h = (h.replace("__BANG_DO__", bang)
      .replace("__TB__", vn(kq["tb"], 2))
      .replace("__T__", vn(kq["T"], 2))
      .replace("__F__", vn(kq["f"], 3))
      .replace("__W__", vn(kq["w"], 3))
      .replace("__LECH__", kq["lech_nhat"]))
for n, fg in enumerate((fig1, fig2, fig3, fig4), 1):
    assert f"<!--FIG{n}-->" in h, f"thiếu mốc FIG{n}"
    h = h.replace(f"<!--FIG{n}-->", fg)

# Số phút đọc trong khung Mục tiêu: đo bằng lint_do_dai rồi làm tròn LÊN (nhật ký skill 6/10/2026)
import importlib.util, pathlib
lint = pathlib.Path(__file__).resolve().parents[3] / ".claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/lint_do_dai.py"
spec = importlib.util.spec_from_file_location("lint_do_dai", lint)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
open("theory.html", "w", encoding="utf8").write(h.replace("__PHUT__", "99"))
phut = math.ceil(mod.kiem("theory.html")["phut"])
h = h.replace("__PHUT__", str(phut))
assert not re.search(r"__[A-Z_]+__", h), "còn mốc __X__ chưa điền"
open("theory.html", "w", encoding="utf8").write(h)
print("ok", len(h), "bytes,", h.count('<figure class="fig"'), "hình, đọc khoảng", phut, "phút")
