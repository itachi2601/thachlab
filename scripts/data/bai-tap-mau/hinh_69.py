"""Hình cho bài tập mẫu Bài 24 "Công suất" (Vật lí 10), lesson_id 69.
Mỗi dạng d<k>(kk): kk=0 mô phỏng chạy MỘT lần khi bấm (đặt dưới đề); kk=2 hình dữ kiện tĩnh cho phần phân tích.
Quy tắc vectơ lực: đầu mũi tên chữ V 30°, độ dài = k·F (một hệ số k cho mỗi loại trong hình), không marker.
Hình đề KHÔNG ghi và KHÔNG vẽ đáp số: D1 chỉ máy bơm + kim đồng hồ chạy 3,0 h; D2 thùng trượt 15 m trong 20 s (chậm 4 lần)
và thùng nâng 1,5 m trong 3,0 s (thật); D3 xe chạy đều 36 km/h đúng thời gian thật 5 s; D4 và D5 là lần chạy thử, tốc độ minh hoạ."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from dung import *
from svg_lib import vec_luc, chevron

GREY = "#94a3b8"


def an(attr, vals, dur, nd=1):
    return (f'<animate attributeName="{attr}" values="{";".join(f"{v:.{nd}f}" for v in vals)}" dur="{dur:.2f}s" '
            f'begin="indefinite" fill="freeze"/>')


def tr(vals, dur):
    """animateTransform translate: vals = [(dx, dy), …]."""
    return (f'<animateTransform attributeName="transform" type="translate" values="{";".join(f"{a:.1f} {b:.1f}" for a, b in vals)}" '
            f'dur="{dur:.2f}s" begin="indefinite" fill="freeze"/>')


def ts(x, y, base, sb, tail="", c="currentColor", size=13, anchor="start", weight="700"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
            f'{base}<tspan dy="4" font-size="{size - 3}">{sb}</tspan><tspan dy="-4">{tail}</tspan></text>')


def box(x, y, w, h, sw=2.2):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="none" stroke="currentColor" stroke-width="{sw}"/>'


def circ(x, y, r, sw=2):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="currentColor" stroke-width="{sw}"/>'


def pump(x, y, rot=False):
    """Máy bơm: thân chữ nhật (x..x+90, y..y+64), cánh quạt tròn 3 cánh tại tâm; rot=True quay 3 vòng khi bấm."""
    cx, cy = x + 45, y + 32
    blades = "".join(seg(cx, cy, cx + 20 * math.cos(math.radians(a)), cy - 20 * math.sin(math.radians(a)), "currentColor", 2.4) for a in (90, 210, 330))
    anim = (f'<animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};1080 {cx} {cy}" dur="6s" '
            f'begin="indefinite" fill="freeze"/>') if rot else ""
    return box(x, y, 90, 64, 2.4) + circ(cx, cy, 24) + f'<g>{blades}{anim}</g>' + dot(cx, cy, 3.5)


# ───────────── Dạng 1: máy bơm 2,0 kW chạy 3,0 h ─────────────
def d1(kk):
    b = ""
    if kk == 0:
        b += pump(40, 62, True) + lbl(85, 52, "P = 2,0 kW", ORG, 13, "middle", "700")
        cx, cy, r = 330, 94, 44
        b += circ(cx, cy, r, 2.4)
        for ang, s in ((90, "12"), (0, "3"), (270, "6"), (180, "9")):
            tx, ty = cx + (r - 14) * math.cos(math.radians(ang)), cy - (r - 14) * math.sin(math.radians(ang)) + 4
            b += lbl(tx, ty, s, "currentColor", 12, "middle", "600")
        hand = (f'<g>{seg(cx, cy, cx, cy - 30, RED, 3.2)}'
                f'<animateTransform attributeName="transform" type="rotate" values="0 {cx} {cy};90 {cx} {cy}" dur="6s" begin="indefinite" fill="freeze"/></g>')
        b += hand + dot(cx, cy, 3.5)
        b += lbl(cx, 160, "kim chạy 3,0 h", "currentColor", 13, "middle", "700") + lbl(235, 100, "Công A = ?", "currentColor", 13, "middle", "700")
        return fig("d1-0", "0 0 460 186", "Máy bơm công suất 2,0 kW chạy liên tục 3,0 giờ, đồng hồ có kim quay từ 12 đến 3", b,
                   "Mô phỏng: máy bơm hoạt động liên tục, kim đồng hồ chạy 3,0 giờ (1 s trong hình ứng với 0,5 giờ). Công A chưa tính.")
    b += pump(40, 24) + lbl(85, 16, "P = 2,0 kW", ORG, 13, "middle", "700")
    b += arrow("", "b", 140, 56, 250, 56, 2.4) + lbl(195, 46, "t = 3,0 h", BLUE, 13, "middle", "700") + lbl(262, 61, "A = ?", "currentColor", 13, "start", "700")
    b += pump(40, 112) + lbl(85, 104, "P′ = 0,50 kW", ORG, 13, "middle", "700")
    b += arrow("", "b", 140, 144, 250, 144, 2.4, "5 4") + lbl(195, 134, "t′ = ?", BLUE, 13, "middle", "700") + lbl(262, 149, "cùng công A", "currentColor", 13, "start", "700")
    return fig("d1-2", "0 0 460 196", "Hai máy bơm: máy thứ nhất 2,0 kW chạy 3,0 giờ, máy thứ hai 0,50 kW chạy thời gian chưa biết, cùng một công",
               b, "Dữ kiện: hai máy sinh cùng một công A; chiều dài mũi tên thời gian không theo tỉ lệ.")


# ───────────── Dạng 2: kéo thùng 120 N trượt 15 m trong 20 s; nâng 24 kg lên 1,5 m trong 3,0 s ─────────────
def d2(kk):
    k = 0.4; F = 120.0; x0 = 40.0; fy = 100.0           # sàn ở y=100, hộp x0..x0+44
    scale = 20.0                                          # 20 px ứng với 1 m (cảnh trên)
    front = x0 + 44
    b = ground(fy, 16, 444)
    for m in (0, 5, 10, 15):
        px = front + scale * m
        b += seg(px, fy + 8, px, fy + 16, "currentColor", 1.4) + lbl(px, fy + 32, f"{m} m" if m == 15 else str(m), "currentColor", 12, "middle", "600")
    s, tip = vec_luc("o", front, fy - 17, 1, 0, F, k)
    cart = box(x0, fy - 34, 44, 34) + s + lbl(front - 22, fy - 42, "F = 120 N", ORG, 13, "middle", "700")
    # cảnh dưới: nâng thùng 24 kg lên giá cao 1,5 m (30 px ứng với 1 m)
    gy = 262.0; hpx = 45.0; bx = 240.0
    low = ground(gy, 16, 444) + box(310, gy - hpx, 120, hpx, 2.4)
    low += dim("", "b", 214, gy, 214, gy - hpx, "", 0, 0) + lbl(208, gy - 17, "1,5 m", BLUE, 13, "end", "700")
    lift = box(bx, gy - 34, 44, 34) + lbl(bx + 22, gy - 12, "24 kg", "currentColor", 12, "middle", "600")
    if kk == 0:
        b += f'<g>{cart}{tr([(0, 0), (15 * scale, 0)], 5.0)}</g>'
        b += low + f'<g>{lift}{tr([(0, 0), (0, -hpx)], 3.0)}</g>'
        b += lbl(40, 24, "Cảnh 1: kéo thùng 15 m trong 20 s", "currentColor", 13, "start", "700") + lbl(40, 176, "Cảnh 2: nâng thùng lên giá trong 3,0 s", "currentColor", 13, "start", "700")
        return fig("d2-0", "0 0 460 290", "Hai cảnh: thùng hàng được kéo trượt 15 m trên sàn ngang trong 20 giây; thùng 24 kg được nâng lên giá cao 1,5 m trong 3,0 giây", b,
                   "Mô phỏng: cảnh 1 chạy chậm 4 lần (20 s thật ứng với 5 s); cảnh 2 chạy đúng thời gian thật (3,0 s). Công và công suất chưa tính.")
    b += cart + box(front + 15 * scale - 44, fy - 34, 44, 34, 1.4).replace('stroke="currentColor"', f'stroke="{GREY}" stroke-dasharray="5 4"')
    b += dim("", "b", front, fy - 62, front + 15 * scale, fy - 62, "d = 15 m", front + 150 - 24, fy - 70)
    b += lbl(40, 14, "Cảnh 1: kéo thùng, t = 20 s", "currentColor", 13, "start", "700") + lbl(40, 176, "Cảnh 2: nâng thùng lên giá, t = 3,0 s", "currentColor", 13, "start", "700")
    b += low + lift + box(bx, gy - hpx - 34, 44, 34, 1.4).replace('stroke="currentColor"', f'stroke="{GREY}" stroke-dasharray="5 4"')
    return fig("d2-2", "0 0 460 290", "Cảnh kéo thùng trượt 15 m trong 20 giây và cảnh nâng thùng 24 kg lên giá cao 1,5 m trong 3,0 giây", b,
               "Dữ kiện: nét đứt là vị trí cuối của thùng. Lực kéo vẽ theo tỉ lệ 1 N ứng với 0,4 px; lực nâng chưa vẽ.")


# ───────────── Dạng 3: xe máy điện chạy đều 36 km/h, lực kéo 150 N ─────────────
def scooter(rx, ry):
    """Xe máy điện nhìn nghiêng, quay sang phải; bánh sau tâm (rx, ry-10)."""
    out = circ(rx, ry - 10, 10) + circ(rx + 40, ry - 10, 10)
    out += box(rx - 6, ry - 38, 52, 18, 2.2)
    out += seg(rx + 40, ry - 20, rx + 46, ry - 48, "currentColor", 2.2) + seg(rx + 40, ry - 48, rx + 54, ry - 48, "currentColor", 2.2)
    out += seg(rx - 4, ry - 38, rx + 16, ry - 38, "currentColor", 4)
    return out


def d3(kk):
    k = 0.3; F = 150.0; rx = 30.0; ry = 100.0; pxm = 6.0       # 6 px ứng với 1 m
    b = ground(ry, 16, 444)
    for m in (0, 10, 20, 30, 40, 50):
        px = rx + pxm * m
        b += seg(px, ry + 8, px, ry + 16, "currentColor", 1.4) + lbl(px, ry + 32, f"{m} m" if m == 50 else str(m), "currentColor", 12, "middle", "600")
    fx, fyy = rx + 56, ry - 29
    s, tip = vec_luc("o", fx, fyy, 1, 0, F, k)
    veh = scooter(rx, ry) + s + lbl(rx + 22, ry - 58, "F = 150 N", ORG, 13, "middle", "700")
    if kk == 0:
        b += lbl(30, 26, "Xe chạy đều, v = 36 km/h", "currentColor", 13, "start", "700")
        b += f'<g>{veh}{tr([(0, 0), (50 * pxm, 0)], 5.0)}</g>'
        return fig("d3-0", "0 0 460 160", "Xe máy điện chạy đều trên đường thẳng ngang với tốc độ 36 km/h, lực kéo của động cơ 150 N cùng hướng chuyển động", b,
                   "Mô phỏng: chạy đúng thời gian thật 5 s, thước đo quãng đường tính từ vị trí xuất phát. Lực kéo vẽ theo tỉ lệ 1 N ứng với 0,3 px. Công suất chưa tính.")
    vs, _ = vec_luc("b", rx + 22, ry - 76, 1, 0, 36.0, 1.2)
    b += veh + vs + lbl(rx + 22, ry - 84, "v = 36 km/h", BLUE, 13, "start", "700")
    b += lbl(210, 26, "Ý c: v′ = 54 km/h, F′ = 120 N", GREY, 13, "start", "700")
    return fig("d3-2", "0 0 460 160", "Xe máy điện có lực kéo F cùng hướng với vận tốc v", b,
               "Dữ kiện ý a: lực kéo (cam) tỉ lệ 1 N ứng với 0,3 px; vận tốc (xanh) tỉ lệ 1 km/h ứng với 1,2 px. F và v cùng hướng.")


# ───────────── Dạng 4: cần cẩu 22,5 kW nâng đều 750 kg lên 30 m ─────────────
def d4(kk):
    gy = 270.0; px = 6.0                                  # 6 px ứng với 1 m
    top = gy - 30 * px                                    # đáy kiện ở độ cao 30 m
    jx = 280.0
    b = seg(30, gy, 440, gy, "currentColor", 2.4) + seg(90, gy, 90, 40, "currentColor", 4) + seg(60, 40, 330, 40, "currentColor", 4)
    b += box(52, 30, 18, 20, 2) + seg(jx, 40, jx, 46, "currentColor", 2)
    b += lbl(100, 28, "P = 22,5 kW", ORG, 13, "start", "700")
    b += seg(jx - 22, top, 352, top, GREY, 1.2, "5 4", .9) + dim("", "b", 352, gy, 352, top, "", 0, 0) + lbl(362, (gy + top) / 2 + 4, "30 m", BLUE, 13, "start", "700")
    ly0, ly1 = gy - 34, top - 34                          # y mép trên kiện lúc đầu / lúc cuối
    if kk == 0:
        n = 2; dur = 6.0
        b += (f'<line x1="{jx}" y1="46" x2="{jx}" y2="{ly0}" stroke="currentColor" stroke-width="1.8">{an("y2", [ly0, ly1], dur)}</line>'
              f'<g><rect x="{jx - 22}" y="{ly0}" width="44" height="34" fill="none" stroke="currentColor" stroke-width="2.2"/>'
              f'{lbl(jx, ly0 + 21, "750 kg", "currentColor", 12, "middle", "600")}{tr([(0, 0), (0, ly1 - ly0)], dur)}</g>')
        return fig("d4-0", "0 0 460 290", "Cần cẩu tháp có động cơ 22,5 kW nâng kiện vật liệu 750 kg từ mặt đất lên độ cao 30 m", b,
                   "Mô phỏng: lần nâng thử, tốc độ trong hình chỉ để minh hoạ (không phải kết quả cần tìm). Lực nâng, vận tốc và thời gian chưa tính.")
    b += (f'<line x1="{jx}" y1="46" x2="{jx}" y2="{ly0}" stroke="currentColor" stroke-width="1.8"/>'
          f'<rect x="{jx - 22}" y="{ly0}" width="44" height="34" fill="none" stroke="currentColor" stroke-width="2.2"/>{lbl(jx, ly0 + 21, "750 kg", "currentColor", 12, "middle", "600")}')
    b += box(jx - 22, top, 44, 34, 1.4).replace('stroke="currentColor"', f'stroke="{GREY}" stroke-dasharray="5 4"')
    return fig("d4-2", "0 0 460 290", "Kiện vật liệu 750 kg ở mặt đất cần nâng đều lên độ cao 30 m; nét đứt là vị trí cuối", b,
               "Dữ kiện: độ cao nâng 30 m (nét đứt là vị trí cuối của kiện); chưa vẽ lực nào.")


# ───────────── Dạng 5: ô tô tải 4,5 tấn, 36 kW, lên dốc 6 % ─────────────
def truck():
    """Xe tải nhìn nghiêng quay phải; gốc cục bộ (0,0) ở mặt đường dưới bánh sau."""
    out = box(-10, -48, 70, 30, 2.2) + box(60, -38, 30, 20, 2.2) + seg(60, -38, 60, -48, "currentColor", 2.2)
    out += circ(12, -9, 9) + circ(74, -9, 9)
    return out


def d5(kk):
    sl = 0.06; x0 = 20.0; y0 = 172.0; th = math.degrees(math.atan(sl))
    ys = lambda x: y0 - sl * (x - x0)
    b = seg(x0, y0, 440, ys(440), "currentColor", 3)
    b += lbl(30, 26, "Ô tô tải 4,5 tấn, công suất tối đa 36 kW", "currentColor", 13, "start", "700")
    b += lbl(30, 48, "Dốc 6 %: đi 100 m theo mặt dốc thì lên cao 6 m", "currentColor", 13, "start", "600")
    if kk == 0:
        xs = 50.0
        dx = 300.0
        inner = f'<g transform="translate({xs:.1f},{ys(xs):.1f}) rotate({-th:.2f})">{truck()}</g>'
        b += f'<g>{inner}{tr([(0, 0), (dx, -sl * dx)], 5.0)}</g>'
        b += lbl(30, 96, "Lên dốc với công suất tối đa", GREY, 13, "start", "600")
        return fig("d5-0", "0 0 460 200", "Ô tô tải leo lên một con dốc nghiêng nhẹ với công suất tối đa", b,
                   "Mô phỏng: lần chạy thử lên dốc, tốc độ trong hình chỉ để minh hoạ (không phải kết quả cần tìm). Góc dốc vẽ đúng tỉ lệ 6 %. Vận tốc chưa tính.")
    # hình dữ kiện: tam giác dốc phóng to
    A = (60.0, 176.0); B = (380.0, 176.0); C = (380.0, 106.0)
    b = lbl(30, 26, "Ô tô tải 4,5 tấn, công suất tối đa 36 kW", "currentColor", 13, "start", "700")
    b += seg(*A, *C, "currentColor", 3) + seg(*A, *B, GREY, 1.4, "5 4", .9) + seg(*B, *C, GREY, 1.4, "5 4", .9)
    ang = math.degrees(math.atan2(A[1] - C[1], C[0] - A[0]))
    b += arc(A[0], A[1], 46, 0, ang, RED) + lbl(A[0] + 60, A[1] - 12, "α", RED, 14, "start", "700")
    b += lbl(112, 138, "100 m theo mặt dốc", "currentColor", 13, "middle", "600") + lbl(388, 146, "6 m", BLUE, 13, "start", "700")
    mx, my = (A[0] + C[0]) / 2, (A[1] + C[1]) / 2
    nx, ny = -math.sin(math.radians(ang)), -math.cos(math.radians(ang))
    cx, cy = mx + 14 * nx, my + 14 * ny
    blk = f'<g transform="translate({mx:.1f},{my:.1f}) rotate({-ang:.2f})"><rect x="-26" y="-28" width="52" height="28" fill="none" stroke="currentColor" stroke-width="2.2"/></g>'
    s, tip = vec_luc("r", cx, cy, 0, 1, 45000.0, 0.0012)
    b += blk + s + lbl(cx + 8, cy + 40, "mg", RED, 13, "start", "700")
    return fig("d5-2", "0 0 460 200", "Xe trên dốc: 100 m theo mặt dốc thì lên cao 6 m; trọng lực mg thẳng đứng xuống", b,
               "Dữ kiện: dốc vẽ phóng to cho dễ thấy (thực tế nghiêng ít hơn nhiều); chỉ vẽ trọng lực mg, chưa vẽ thành phần nào.")


BUILD = [d1, d2, d3, d4, d5]
