"""Sinh các hình nền dùng chung: cột ghi chú (trái/phải), hình strobe cho đầu bài."""
import math
from pathlib import Path
A = Path(__file__).resolve().parent / 'assets'
A.mkdir(exist_ok=True)

def notes(side):
    x0, x1 = (145, 192) if side == 'right' else (18, 65)
    rule = 142.5 if side == 'right' else 67.5
    lines = ''.join(
        f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#8a8a8a" stroke-width="0.45" stroke-linecap="round" stroke-dasharray="0.01 1.35"/>'
        for y in range(31, 276, 8))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 210 297" width="210mm" height="297mm">'
            f'<line x1="{rule}" y1="17" x2="{rule}" y2="276" stroke="#bdbdbd" stroke-width="0.25"/>'
            f'<rect x="{x0-2}" y="12" width="{x1-x0+4}" height="0.6" fill="#0d0d0d"/>'
            f'{lines}</svg>')

def strobe(w=118, h=62, n=11, ball=3.6, white=True):
    """Ảnh chụp nhiều lần (strobe) quả bóng ném xiên + vectơ vận tốc."""
    col = '#fff' if white else '#000'
    x0, y0, rng, H = 8, h - 8, w - 22, h - 20
    pts = []
    for k in range(n + 1):
        u = k / n
        pts.append((x0 + rng * u, y0 - H * 4 * u * (1 - u)))
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}mm" height="{h}mm" fill="none">']
    # đường nền + trục
    s.append(f'<line x1="2" y1="{y0+ball+2}" x2="{w-2}" y2="{y0+ball+2}" stroke="{col}" stroke-width="0.5"/>')
    for k in range(0, 24):
        x = 4 + k * (w - 8) / 23
        s.append(f'<line x1="{x:.1f}" y1="{y0+ball+2}" x2="{x-2:.1f}" y2="{y0+ball+4.6}" stroke="{col}" stroke-width="0.35"/>')
    # quỹ đạo chấm
    d = 'M ' + ' L '.join(f'{x0 + rng*i/60:.2f} {y0 - H*4*(i/60)*(1-i/60):.2f}' for i in range(61))
    s.append(f'<path d="{d}" stroke="{col}" stroke-width="0.5" stroke-dasharray="0.1 1.6" stroke-linecap="round"/>')
    # bóng từng khung hình: mờ → rõ
    for k, (x, y) in enumerate(pts):
        op = 0.18 + 0.82 * (k / n)
        s.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{ball}" stroke="{col}" stroke-width="0.7" fill="{col}" fill-opacity="{op*0.55:.2f}"/>')
    # vectơ v tại điểm k=3 và hai thành phần
    k = 3; x, y = pts[k]; u = k / n
    slope = -H * 4 * (1 - 2 * u) / rng            # dy/dx (SVG, y xuống)
    L = 17
    vx = (L, 0); vy = (0, -L * 0.9 * (1 - 2 * u) * 1.6)
    s.append('<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
             f'<path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker></defs>')
    s.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x+vx[0]:.1f}" y2="{y:.1f}" stroke="{col}" stroke-width="0.7" stroke-dasharray="1.6 1.2" marker-end="url(#ah)"/>')
    s.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y+vy[1]:.1f}" stroke="{col}" stroke-width="0.7" stroke-dasharray="1.6 1.2" marker-end="url(#ah)"/>')
    s.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x+vx[0]:.1f}" y2="{y+vy[1]:.1f}" stroke="{col}" stroke-width="1.3" marker-end="url(#ah)"/>')
    s.append('</svg>')
    return ''.join(s)

(A / 'notes-right.svg').write_text(notes('right'))
(A / 'notes-left.svg').write_text(notes('left'))
(A / 'strobe.svg').write_text(strobe())
(A / 'strobe-big.svg').write_text(strobe(w=190, h=120, n=14, ball=5.2))
(A / 'strobe-ink.svg').write_text(strobe(white=False))
(A / 'strobe-big-ink.svg').write_text(strobe(w=190, h=120, n=14, ball=5.2, white=False))
print('ok')
