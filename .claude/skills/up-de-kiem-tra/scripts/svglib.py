# -*- coding: utf-8 -*-
"""svglib.py — vẽ đồ thị SVG nội tuyến cho câu hỏi ("như hình bên").

Dùng khi đề có đồ thị x–t, v–t, W–x, parabol năng lượng… Vẽ lại bằng SVG thay vì
nhúng ảnh scan: nhẹ, nét ở mọi cỡ màn hình, tự đổi màu theo nền sáng/tối.

    import sys; sys.path.insert(0, '<skill>/scripts')
    from svglib import Plot, txt, BLUE, GREEN, AMBER, AX
    import math

    f = lambda t: 10 * math.sin(2 * math.pi * t)          # x = 10sin(2πt), T = 1 s
    p = Plot(w=370, h=215, ox=48, oy=105, sx=250, sy=6.5, tmax=1.06, ymax=11)
    p.axes()                                              # trục + mũi tên + nhãn + O
    p.ytick(10, '10', dashed_to=0.25).ytick(-10, '-10', dashed_to=0.75)
    p.ttick(0.5, '0,5')
    p.curve(f, 0, 1.0)
    html = p.svg('Đồ thị li độ – thời gian')              # <figure> + <figcaption>

Tham số Plot: `w,h` khung viewBox · `ox,oy` gốc O tính bằng px · `sx,sy` số px cho
MỘT đơn vị trục hoành / trục tung · `tmax,tmin,ymax` phạm vi dữ liệu (chỉ dùng để
đặt đầu mũi tên, KHÔNG cắt đường cong).

## Ba cái bẫy đã trả giá — lớp này xử lý sẵn, đừng tự viết lại

1. **Tràn viewBox.** Mũi tên và nhãn trục nằm NGOÀI vùng dữ liệu: `axes()` vẽ tới
   `X(tmax)+16` và `Y(ymax)-14`. Chọn `w` ≥ `X(tmax)+40`, `h` ≥ vùng dưới cùng +20,
   nếu không nhãn "t (s)" bị cắt cụt hoặc mất hẳn.
2. **Đường cong cắt ngang chữ số trên trục.** Mọi chữ đi vào `self.top`, vẽ SAU
   đường cong, và có quầng nền tối (`HALO`) nên số vẫn đọc được. Đừng append chữ
   thẳng vào `self.parts`.
3. **Nhãn đường ($x_1$, $x_2$, $W_đ$…) đặt bừa.** Đặt ngay cạnh ĐỈNH của đường đó,
   và kiểm đường kia không chạy qua chỗ ấy — hai đồ thị cùng chu kì cắt nhau nhiều
   hơn ta tưởng. `label(t, v, ...)` nhận toạ độ dữ liệu.

Luôn xem lại bằng mắt trước khi đăng: `python3 svglib.py` sinh `svglib-demo.html`,
hoặc gom các hình của đề vào một trang rồi mở trong Browser pane (đọc ảnh trong
subagent để khỏi phình context).

Màu: nét/chữ mặc định `currentColor` (KHÔNG BAO GIỜ `#000` — nền site tối #0B1020).
Nhấn: `BLUE` #60A5FA, `GREEN` #34D399, `AMBER` #F59E0B. KaTeX không chạy trong SVG
nên nhãn dùng unicode (`x₁`, `Wđ`, `t₃`) hoặc để ở `figcaption`.
"""
import math

AX = 'stroke="currentColor" stroke-opacity="0.45" stroke-width="1"'
BLUE, GREEN, AMBER = '#60A5FA', '#34D399', '#F59E0B'
# Quầng nền tối để số trên trục vẫn đọc được khi đường cong đi ngang qua.
HALO = 'paint-order="stroke" stroke="#0B1020" stroke-width="3.2" stroke-linejoin="round"'


def txt(x, y, s, size=10, anchor='middle', color='currentColor', italic=False, halo=True):
    it = ' font-style="italic"' if italic else ''
    h = ' ' + HALO if halo else ''
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" font-size="{size}" '
            f'text-anchor="{anchor}"{it}{h}>{s}</text>')


class Plot:
    """Hệ trục đơn giản. Geometry vào self.parts, chữ vào self.top (vẽ sau cùng)."""

    def __init__(self, w, h, ox, oy, sx, sy, tmax, ymax, tmin=0.0):
        self.w, self.h = w, h
        self.ox, self.oy, self.sx, self.sy = ox, oy, sx, sy
        self.tmax, self.ymax, self.tmin = tmax, ymax, tmin
        self.parts, self.top = [], []

    def X(self, t):
        return self.ox + t * self.sx

    def Y(self, v):
        return self.oy - v * self.sy

    def axes(self, tlabel='t (s)', ylabel='x (cm)', ybot=None):
        xr = self.X(self.tmax) + 16
        xl = self.X(self.tmin) - 10
        yt = self.Y(self.ymax) - 14
        yb = self.Y(-(ybot if ybot is not None else self.ymax)) + 10
        self.parts.append(f'<line x1="{xl:.1f}" y1="{self.oy}" x2="{xr:.1f}" y2="{self.oy}" {AX}/>')
        self.parts.append(f'<line x1="{self.ox}" y1="{yb:.1f}" x2="{self.ox}" y2="{yt:.1f}" {AX}/>')
        self.parts.append(f'<path d="M{xr:.1f} {self.oy} l-6 -3 l0 6 z" fill="currentColor" fill-opacity="0.45"/>')
        self.parts.append(f'<path d="M{self.ox} {yt:.1f} l-3 6 l6 0 z" fill="currentColor" fill-opacity="0.45"/>')
        self.top.append(txt(xr - 2, self.oy + 16, tlabel, 11, 'end'))
        self.top.append(txt(self.ox + 7, yt + 2, ylabel, 11, 'start'))
        self.top.append(txt(self.ox - 9, self.oy + 13, 'O', 10, 'end'))
        return self

    def ytick(self, v, label, dashed_to=None):
        y = self.Y(v)
        self.parts.append(f'<line x1="{self.ox-4}" y1="{y:.1f}" x2="{self.ox+4}" y2="{y:.1f}" {AX}/>')
        if dashed_to is not None:
            self.parts.append(f'<line x1="{self.ox}" y1="{y:.1f}" x2="{self.X(dashed_to):.1f}" y2="{y:.1f}" '
                              f'stroke="currentColor" stroke-opacity="0.3" stroke-dasharray="4 3"/>')
        self.top.append(txt(self.ox - 8, y + 3.5, label, 10, 'end'))
        return self

    def ttick(self, t, label):
        x = self.X(t)
        self.parts.append(f'<line x1="{x:.1f}" y1="{self.oy-4}" x2="{x:.1f}" y2="{self.oy+4}" {AX}/>')
        self.top.append(txt(x, self.oy + 15, label, 10))
        return self

    def marker(self, t, fn, label):
        """Chấm trên trục t + gạch đứt tới đường cong; nhãn luôn ở dưới trục."""
        x, v = self.X(t), fn(t)
        self.parts.append(f'<line x1="{x:.1f}" y1="{self.oy:.1f}" x2="{x:.1f}" y2="{self.Y(v):.1f}" '
                          f'stroke="currentColor" stroke-opacity="0.35" stroke-dasharray="3 3"/>')
        self.parts.append(f'<circle cx="{x:.1f}" cy="{self.oy:.1f}" r="2.6" fill="currentColor"/>')
        self.top.append(txt(x, self.oy + 16, label, 10.5))
        return self

    def curve(self, fn, t0, t1, color=BLUE, n=150, width=2):
        seen, pts = None, []
        for i in range(n + 1):
            t = t0 + (t1 - t0) * i / n
            xy = (round(self.X(t), 1), round(self.Y(fn(t)), 1))
            if xy != seen:
                pts.append(f'{xy[0]:g},{xy[1]:g}')
                seen = xy
        self.parts.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" '
                          f'stroke-width="{width}" stroke-linejoin="round"/>')
        return self

    def label(self, t, v, text, color=BLUE, anchor='start'):
        self.top.append(txt(self.X(t), self.Y(v), text, 11.5, anchor, color, italic=True))
        return self

    def svg(self, caption):
        body = "\n    ".join(self.parts + self.top)
        return (f'<figure class="fig">\n  <svg viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg">\n    '
                f'{body}\n  </svg>\n  <figcaption>{caption}</figcaption>\n</figure>')

def check_bounds(figs, pad_top=2):
    """Soát mọi hình xem có phần tử nào tràn viewBox không. (ok, [dòng báo cáo])

    Đây là lỗi hay gặp nhất và là lỗi KHÔNG nhìn ảnh chụp cũng bắt được: nhãn trục hay
    mũi tên nằm ngoài khung thì trình duyệt cắt im lặng. Chạy hàm này trước, chỉ đi soi
    ảnh khi nó đã sạch — đỡ hẳn một vòng screenshot.

        ok, lines = check_bounds(list(FIGS.values()))
        print('\n'.join(lines))

    Không thay được việc xem bằng mắt: chồng chữ, nhãn đặt lạc đường, đường cong sai
    pha thì chỉ mắt mới thấy.
    """
    import re
    out, ok = [], True
    for i, fig in enumerate(figs, 1):
        m = re.search(r'<svg viewBox="0 0 (\d+) (\d+)"(.*?)</svg>', fig, re.S)
        if not m:
            out.append(f'? fig{i}: không đọc được viewBox')
            ok = False
            continue
        w, h, body = int(m.group(1)), int(m.group(2)), m.group(3)
        xs, ys = [], []
        for a in ('x1', 'x2', 'cx'):
            xs += [float(v) for v in re.findall(a + r'="(-?[\d.]+)"', body)]
        for a in ('y1', 'y2', 'cy'):
            ys += [float(v) for v in re.findall(a + r'="(-?[\d.]+)"', body)]
        for pl in re.findall(r'points="([^"]+)"', body):
            for pt in pl.split():
                a, b = pt.split(',')
                xs.append(float(a))
                ys.append(float(b))
        for a, b in re.findall(r'<text x="(-?[\d.]+)" y="(-?[\d.]+)"', body):
            xs.append(float(a))
            ys.append(float(b))
        for a, b in re.findall(r'd="M(-?[\d.]+) (-?[\d.]+)', body):
            xs.append(float(a))
            ys.append(float(b))
        if not xs:
            continue
        bad = min(xs) < 0 or min(ys) < pad_top or max(xs) > w or max(ys) > h
        ok &= not bad
        out.append(f'{"✗" if bad else "✓"} fig{i} viewBox {w}x{h}  '
                   f'x[{min(xs):.0f},{max(xs):.0f}] y[{min(ys):.0f},{max(ys):.0f}]')
    out.append('BOUNDS OK' if ok else 'TRÀN VIEWBOX — nới w/h hoặc giảm sx/sy')
    return ok, out


# ---------------------------------------------------------------- demo / smoke test
if __name__ == '__main__':
    PI = math.pi
    figs = []

    # sin một chu kì, có mốc trên trục
    f = lambda t: 5 * math.sin(2 * PI * t)
    p = Plot(w=370, h=215, ox=48, oy=103, sx=255, sy=13, tmax=1.06, ymax=5.9)
    p.axes()
    p.ytick(5, '5', dashed_to=0.25).ytick(-5, '-5', dashed_to=0.75)
    p.curve(f, 0, 1.0)
    for t, lb in ((0.25, 't₁'), (0.5, 't₂'), (0.85, 't₃')):
        p.marker(t, f, lb)
    figs.append(p.svg('x–t một chu kì, ba mốc thời gian'))

    # hai đường cùng chu kì, khác biên độ và pha
    w = 2.5 * PI
    g1, g2 = lambda t: 20 * math.sin(w * t), lambda t: -10 * math.cos(w * t)
    p = Plot(w=430, h=235, ox=54, oy=115, sx=285, sy=3.6, tmax=1.22, ymax=25)
    p.axes()
    for v in (20, 10, -10, -20):
        p.ytick(v, str(v))
    for t in (0.2, 0.4, 0.6, 0.8, 1.0):
        p.ttick(t, str(t).replace('.', ','))
    p.curve(g1, 0, 1.2, color=BLUE).curve(g2, 0, 1.2, color=AMBER)
    p.label(0.2, 23.5, 'x₁', color=BLUE, anchor='middle')
    p.label(0.42, 13.5, 'x₂', color=AMBER, anchor='middle')
    figs.append(p.svg('Hai dao động cùng chu kì'))

    # parabol năng lượng, trục hoành kéo sang cả hai phía gốc
    fw = lambda x: 32 * (1 - x * x / 16)
    p = Plot(w=350, h=230, ox=172, oy=180, sx=30, sy=3.6, tmax=5.0, ymax=40, tmin=-5.0)
    p.axes(tlabel='x (cm)', ylabel='Wđ (mJ)', ybot=0)
    p.parts.append(f'<line x1="{p.ox-4}" y1="{p.Y(32):.1f}" x2="{p.ox+4}" y2="{p.Y(32):.1f}" {AX}/>')
    p.top.append(txt(p.ox - 11, p.Y(32) + 3.5, '32', 10, 'end'))
    for x in (-4, 4):
        p.parts.append(f'<line x1="{p.X(x):.1f}" y1="{p.oy-4}" x2="{p.X(x):.1f}" y2="{p.oy+4}" {AX}/>')
        p.top.append(txt(p.X(x), p.oy + 15, str(x)))
    p.curve(fw, -4, 4, color=GREEN)
    figs.append(p.svg('Động năng theo li độ'))

    body = ''.join(f'<section>{f}</section>' for f in figs)
    open('svglib-demo.html', 'w', encoding='utf-8').write(
        '<!DOCTYPE html><html><head><meta charset="utf-8"><title>svglib demo</title>'
        '<style>body{background:#0B1020;color:#E5E7EB;font-family:system-ui;padding:14px}'
        'section{border:1px solid #1f2937;border-radius:8px;padding:6px;margin-bottom:8px}'
        'figure{margin:0}svg{width:100%;max-width:430px;display:block}'
        'figcaption{font-size:11px;color:#9CA3AF;margin-top:2px}</style></head><body>'
        + body + '</body></html>')
    print('svglib-demo.html — mở trong Browser pane để xem 3 hình mẫu')
    ok, lines = check_bounds(figs)
    print('\n'.join(lines))
