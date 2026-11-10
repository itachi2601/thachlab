"""💡 Mẹo nhìn "Xe đẩy vào cát" (bài 83 KHTN 9 Bài 5 Khúc xạ ánh sáng, dạng 2) — định tính: hướng bẻ của tia sáng.
Mô phỏng thật: xe hai bánh (trục vuông góc hướng đi), chạy xiên từ nhựa (nhanh) xuống cát (chậm); bánh chạm cát trước chậm lại
nên xe quay. Hướng cuối lấy theo dựng Huygens sin r = (v2/v1) sin i (chỉ để TÍNH vị trí, không ghi lên hình); góc quay tức thời
chọn sao cho vừa đúng khi bánh thứ hai vào cát. Số mẹo: i = 55°, v2/v1 = 0,7 → r ≈ 35° (đề dùng 50°, 28°, 40°, 62°)."""
import math, os, sys
from meo_nhiet import _anim, _show, _txt, _caption, _f  # noqa: F401


def _caption(lines, y0, final, windows, T):  # H4: phụ đề cỡ 15 (bản meo_nhiet là 14)
    t = "".join(_txt(10, y0 + 19 * i, s, size=15, weight="500") for i, s in enumerate(lines))
    return f'<g opacity="{1 if final else 0}">{t}{_show(windows, T)}</g>'
from hinh import fig, RED, BLUE  # noqa: E402 (meo_nhiet đã thêm đường dẫn)


def _rot(pts, T):
    kt = ";".join(f"{t / T:.4f}".rstrip("0").rstrip(".") or "0" for t, _ in pts)
    vals = ";".join(f"{a:.2f} 0 0" for _, a in pts)
    return (f'<animateTransform attributeName="transform" type="rotate" values="{vals}" keyTimes="{kt}"'
            f' dur="{T}s" begin="indefinite" fill="freeze"/>')


def _simulate():
    I = math.radians(55)
    ratio = 0.7
    R = math.asin(ratio * math.sin(I))
    assert abs(math.degrees(R) - 35.1) < 0.3 and R < I
    v1, v2, W, Y0, dt = 34.0, 34.0 * ratio, 32.0, 88.0, 0.01
    ttr = W * math.sin(I) / v1
    for _ in range(12):                      # chọn tốc độ quay để vừa đúng r khi bánh 2 vào cát
        om = (R - I) / ttr
        cx, cy, th, t = 80.0, 34.0, I, 0.0
        rec, t1, t2 = [], None, None
        while True:
            ax, ay = math.cos(th), -math.sin(th)
            L = (cx - W / 2 * ax, cy - W / 2 * ay)
            Rw = (cx + W / 2 * ax, cy + W / 2 * ay)
            inL, inR = L[1] > Y0, Rw[1] > Y0
            if inL and t1 is None: t1 = t
            if inR and t2 is None: t2 = t
            rec.append((t, cx, cy, th))
            if t2 is not None and cy > Y0 + 52:
                break
            v = (v2 if inL else v1) / 2 + (v2 if inR else v1) / 2
            if inL != inR: th += om * dt
            else:
                if inL and inR: th = R
            cx += v * math.sin(th) * dt
            cy += v * math.cos(th) * dt
            t += dt
        ttr_new = t2 - t1
        if abs(ttr_new - ttr) < 1e-3: break
        ttr = ttr_new
    assert abs(rec[-1][3] - R) < 1e-6 and t1 < t2
    return I, R, rec, t1, t2, W, Y0


def xe_day_vao_cat(noi_voi_de):
    I, R, rec, t1, t2, W, Y0 = _simulate()
    # giao điểm hai đường đi (đường vào qua điểm đầu, đường ra qua điểm cuối) = chân pháp tuyến
    (_, ax_, ay_, _), (_, bx_, by_, _) = rec[0], rec[-1]
    d1, d2 = (math.sin(I), math.cos(I)), (math.sin(R), math.cos(R))
    det = d1[0] * (-d2[1]) - d1[1] * (-d2[0])
    s = ((bx_ - ax_) * (-d2[1]) - (by_ - ay_) * (-d2[0])) / det
    PX, PY = ax_ + s * d1[0], ay_ + s * d1[1]
    assert abs(PY - Y0) < 6, PY
    DX = 140 - PX
    # lấy mẫu: chuyển động bắt đầu ở 1,0 s; ép vị trí xe bắt đầu tại khung nghỉ
    T0, SP = 1.0, 1.0
    samp = [r for i, r in enumerate(rec) if i % 25 == 0] + [rec[-1]]
    tt = lambda r: T0 + r[0] * SP
    T = round(tt(rec[-1]) + 0.8, 1)
    ts1, ts2 = T0 + t1 * SP, T0 + t2 * SP
    xy = [(tt(r), f"{r[1] + DX:.1f},{r[2]:.1f}") for r in samp]
    an = [(tt(r), -math.degrees(r[3])) for r in samp]
    fx, fy, fa = rec[-1][1] + DX, rec[-1][2], -math.degrees(R)
    px, py = PX + DX, PY
    ex, ey = ax_ + DX, ay_
    b = []
    # hai môi trường
    b.append('<rect x="4" y="8" width="312" height="%d" fill="currentColor" opacity=".07"/>' % (Y0 - 8))
    b.append('<rect x="4" y="%d" width="312" height="96" fill="#f59e0b" opacity=".28"/>' % Y0)
    b.append(f'<line x1="4" y1="{Y0}" x2="316" y2="{Y0}" stroke="currentColor" stroke-width="2" opacity=".7"/>')
    b.append(_txt(312, Y0 - 10, "Nhựa: xe nhanh", size=15, anchor="end", weight="700"))  # góc phải dưới vùng nhựa: xe xuất phát ở góc trái trên
    b.append(_txt(8, 172, "Cát: xe chậm", size=15, weight="700"))
    # pháp tuyến + vệt đường đi
    b.append(f'<line x1="{px:.1f}" y1="14" x2="{px:.1f}" y2="{Y0 + 92}" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 4" opacity=".75"/>')
    b.append(_txt(px + 6, 24, "pháp tuyến", size=15, weight="500"))
    b.append(f'<line x1="{ex:.1f}" y1="{ey:.1f}" x2="{px:.1f}" y2="{py:.1f}" stroke="currentColor" stroke-width="1.5" stroke-dasharray="2 4" stroke-linecap="round" opacity=".8"/>')
    b.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{fx:.1f}" y2="{fy:.1f}" stroke="currentColor" stroke-width="1.5" stroke-dasharray="2 4" stroke-linecap="round" opacity=".8"/>')
    # cung góc i, r (so với pháp tuyến)
    rr = 28
    b.append(f'<path d="M{px:.1f} {py - rr:.1f} A{rr} {rr} 0 0 0 {px - rr * math.sin(I):.1f} {py - rr * math.cos(I):.1f}" fill="none" stroke="{RED}" stroke-width="2.2"/>')
    b.append(f'<path d="M{px:.1f} {py + rr:.1f} A{rr} {rr} 0 0 0 {px + rr * math.sin(R):.1f} {py + rr * math.cos(R):.1f}" fill="none" stroke="{BLUE}" stroke-width="2.2"/>')
    b.append(_txt(px - 40 * math.sin(I / 2) - 6, py - 40 * math.cos(I / 2) + 5, "i", size=17, weight="700", anchor="middle", fill=RED))
    b.append(_txt(px + 42 * math.sin(R / 2) + 4, py + 42 * math.cos(R / 2) + 7, "r", size=17, weight="700", anchor="middle", fill=BLUE))
    # xe: bánh 1 (trái, thấp hơn) chạm cát trước
    h = W / 2
    car = (f'<line x1="0" y1="0" x2="0" y2="-18" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>'
           f'<line x1="{-h}" y1="0" x2="{h}" y2="0" stroke="currentColor" stroke-width="2.5"/>'
           f'<rect x="{-h - 3}" y="-8" width="6" height="16" rx="2" fill="{RED}" stroke="currentColor" stroke-width="1.2"/>'
           f'<rect x="{h - 3}" y="-8" width="6" height="16" rx="2" fill="currentColor"/>'
           f'<rect x="-8" y="0" width="16" height="20" rx="3" fill="{BLUE}"/>'
           f'<polygon points="-5,20 5,20 0,27" fill="{BLUE}"/>'
           + _txt(-h - 11, 5, "1", size=15, anchor="middle", weight="700", fill=RED)
           + _txt(h + 11, 5, "2", size=15, anchor="middle", weight="700"))
    b.append(f'<g transform="translate({fx:.1f},{fy:.1f})">{_anim("", xy, T, transform=True)}'
             f'<g transform="rotate({fa:.2f})">{_rot(an, T)}{car}</g></g>')
    # phụ đề
    cy = 214
    caps = [
        (["Xe chạy xiên trên nhựa, hai bánh nhanh;", "trục xe vuông góc hướng đi."], [(0, ts1)], False),
        (["Bánh 1 chạm cát trước, chậm lại; bánh 2", "còn nhanh nên xe quay về pháp tuyến."], [(ts1, ts2 + 0.6)], False),
        (["Cả hai bánh trong cát: xe đi thẳng,", "hướng mới lại gần pháp tuyến.", "Cát → nhựa: đúng vệt cũ, xa pháp tuyến."], [(ts2 + 0.6, None)], True),
    ]
    for lines, win, fin in caps:
        b.append(_caption(lines, cy, fin, win, T))
    cap = ("Vào môi trường chậm hơn (chiết quang hơn) thì tia lệch lại gần pháp tuyến ($r\\lt i$); "
           "ra môi trường nhanh hơn thì lệch xa pháp tuyến. Góc đo so với pháp tuyến.")
    html = fig("meo-xe-cat", "0 0 320 262",
               "Xe đẩy hai bánh chạy xiên từ nhựa xuống cát: bánh chạm cát trước chậm lại nên xe quay, hướng mới lệch lại gần pháp tuyến",
               "".join(b), cap)
    return {
        "ten": "Xe đẩy vào cát",
        "dieu_kien": "Mặt phân cách phẳng, hai môi trường đồng nhất và đẳng hướng; ánh sáng đơn sắc. "
                     "Mỗi bánh giữ tốc độ không đổi trong từng môi trường, xe không lái nên hướng chỉ đổi do chênh tốc độ hai bánh. "
                     "Ánh sáng đi chậm hơn ở môi trường chiết quang hơn ($v=c/n$). Góc đo so với pháp tuyến; tia tới vuông góc thì không bẻ nhưng vẫn chậm lại. Mẹo chỉ cho biết hướng bẻ (không mô tả phản xạ toàn phần), không giải thích cường độ tia phản xạ hay khúc xạ.",
        "html": html + noi_voi_de,
    }


if __name__ == "__main__":
    f = xe_day_vao_cat("")
    n = len(f["html"].encode())
    print(f["ten"], n, "byte")
    assert n <= 15000
    out = os.environ.get("MEO_OUT")
    if out:
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "xe-cat.svg.html"), "w").write(
            '<!doctype html><meta charset="utf-8"><body style="max-width:343px;margin:16px;font-family:sans-serif"><div style="color:#0f172a">'
            + f["html"].replace('class="fig"', 'class="fig" style="margin:0"') + "</div>")
