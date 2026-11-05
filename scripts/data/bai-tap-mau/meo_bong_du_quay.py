"""💡 Mẹo nhìn «Bóng đu quay» — L11 Bài 4, dạng 4: thời điểm qua một vị trí lần đầu / lần thứ n.
Ghế quay đều ngược chiều kim đồng hồ trên vòng bán kính A, bắt đầu ở biên dương (φ₀ = 0); bóng x = A·cosφ.
Cờ đặt ở x = A/2: lần 1 ở góc 60° (đi sang trái), lần 2 ở góc 300° (đi sang phải), lần 3 = lần 1 + T (góc 420°).
Chạy thử: python3 scripts/data/bai-tap-mau/meo_bong_du_quay.py  (MEO_OUT=<thư mục> để ghi bản xem thử)."""
import math, os
from meo_nhiet import _anim, _show, _txt, _f  # noqa: F401
from hinh import fig, RED, BLUE  # noqa: E402

TXT_DARK = "#0f172a"


def _cap(lines, y0, final, windows, T):
    t = "".join(_txt(10, y0 + 19 * i, s, size=15, weight="500") for i, s in enumerate(lines))
    return f'<g opacity="{1 if final else 0}">{t}{_show(windows, T)}</g>'


def bong_du_quay(noi_voi_de):
    # --- số liệu mẹo: vị trí cờ x = A/2, bắt đầu ở biên dương
    w = 35.0                                   # độ/giây (chỉ để dựng hoạt hình; ω tỉ lệ)
    assert abs(math.cos(math.radians(60)) - 0.5) < 1e-12 and abs(math.cos(math.radians(300)) - 0.5) < 1e-12
    # chiều: x = cosφ, v ∝ −sinφ; lần 1 (60°): sin>0 → v<0 (trái); lần 2 (300°): sin<0 → v>0 (phải)
    assert -math.sin(math.radians(60)) < 0 < -math.sin(math.radians(300))
    # công thức chốt: t = Δφ/ω; lần 2k+1 = lần 1 + kT; lần 2k+2 = lần 2 + kT (đếm mọi lần qua, kể cả hai chiều)
    om = math.radians(w)                       # rad/s, T = 2π/ω
    Tp = 2 * math.pi / om
    t1, t2 = math.radians(60) / om, math.radians(300) / om
    cross = []                                 # các thời điểm cos(ωt) = 1/2 trong 2 chu kì
    for n in range(4000):
        a, b = n * Tp / 1000 * 0.5, (n + 1) * Tp / 1000 * 0.5
        fa, fb = math.cos(om * a) - 0.5, math.cos(om * b) - 0.5
        if fa * fb < 0:
            cross.append((a + b) / 2)
    assert len(cross) == 4
    for k in range(2):
        assert abs(cross[2 * k] - (t1 + k * Tp)) < Tp / 500 and abs(cross[2 * k + 1] - (t2 + k * Tp)) < Tp / 500
    assert abs(math.radians(420) / om - (t1 + Tp)) < 1e-9

    T = 14.0
    S, E = 1.0, 13.0                           # ghế đứng yên ở biên tới giây 1, quay hết 420° lúc giây 13
    tm = lambda phi: S + (E - S) * phi / 420.0
    ta, tb, tc = tm(60), tm(300), tm(420)
    CX, CY, R, GY = 160, 88, 70, 180
    xc = CX + R / 2
    pos = lambda phi: (CX + R * math.cos(math.radians(phi)), CY - R * math.sin(math.radians(phi)))
    ph = list(range(0, 421, 10))
    assert 60 in ph and 300 in ph
    ts = lambda phi: tm(phi)
    def pts(f):
        return [(ts(p), f(p)) for p in ph]
    r = lambda v: round(v, 1)
    fx, fy = pos(420)
    b = []
    # nền: vòng, mặt đất, tâm
    b.append(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="currentColor" stroke-width="1.5" opacity=".35"/>')
    b.append(f'<circle cx="{CX}" cy="{CY}" r="3" fill="currentColor"/>')
    b.append(f'<line x1="10" y1="{GY}" x2="310" y2="{GY}" stroke="currentColor" stroke-width="2" opacity=".6"/>')
    b.append(_txt(10, GY - 7, "mặt đất", size=15, weight="500"))
    # cờ ở x = A/2: cột chung qua cả hai điểm trên vòng + lá cờ
    y1, y2 = r(pos(60)[1]), r(pos(300)[1])
    b.append(f'<line x1="{xc}" y1="{y1}" x2="{xc}" y2="{GY}" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4 4" opacity=".55"/>')
    b.append(f'<line x1="{xc}" y1="{GY}" x2="{xc}" y2="{GY + 18}" stroke="currentColor" stroke-width="2.5"/>')
    b.append(f'<polygon points="{xc},{GY + 18} {xc},{GY + 5} {xc + 17},{GY + 11.5}" fill="{BLUE}"/>')
    # cung góc đã quét (ngược chiều kim đồng hồ: lật trục y quanh tâm)
    for rad, col, d1, d2, tt in ((R - 14, BLUE, "360 360", None, (S, tm(360))), (R - 24, "#b45309", "60 360", None, (tm(360), E))):
        a0, a1 = tt
        dash0 = "0 360"
        if col == BLUE:
            vals = [(0, dash0), (a0, dash0), (a1, d1)]
        else:
            vals = [(0, dash0), (a0, dash0), (a1, d1)]
        b.append(f'<g transform="translate({CX},{CY}) scale(1,-1)"><circle cx="0" cy="0" r="{rad}" pathLength="360" fill="none" stroke="{col}" stroke-width="5" stroke-dasharray="{d1}">'
                 f'{_anim("stroke-dasharray", vals, T)}</circle></g>')
    # tia nắng từ ghế xuống bóng + bán kính tới ghế + ghế + bóng
    b.append(f'<line x1="{r(fx)}" y1="{r(fy)}" x2="{r(fx)}" y2="{GY}" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3 4" opacity=".6">'
             f'{_anim("x1", pts(lambda p: r(pos(p)[0])), T)}{_anim("x2", pts(lambda p: r(pos(p)[0])), T)}{_anim("y1", pts(lambda p: r(pos(p)[1])), T)}</line>')
    b.append(f'<line x1="{CX}" y1="{CY}" x2="{r(fx)}" y2="{r(fy)}" stroke="{RED}" stroke-width="2.5">'
             f'{_anim("x2", pts(lambda p: r(pos(p)[0])), T)}{_anim("y2", pts(lambda p: r(pos(p)[1])), T)}</line>')
    b.append(f'<circle cx="{r(fx)}" cy="{r(fy)}" r="9" fill="{RED}">'
             f'{_anim("cx", pts(lambda p: r(pos(p)[0])), T)}{_anim("cy", pts(lambda p: r(pos(p)[1])), T)}</circle>')
    b.append(f'<ellipse cx="{r(fx)}" cy="{GY}" rx="10" ry="5" fill="currentColor">'
             f'{_anim("cx", pts(lambda p: r(pos(p)[0])), T)}</ellipse>')
    # số lần trên vòng (cạnh hai điểm cờ)
    b.append(f'<g opacity="0">{_txt(xc + 9, y1 - 6, "1", size=15, weight="700")}{_show([(ta, E)], T)}</g>')
    b.append(f'<g opacity="1">{_txt(xc + 9, y1 - 6, "1 · 3", size=15, weight="700")}{_show([(E, None)], T)}</g>')
    b.append(f'<g opacity="1">{_txt(xc + 9, y2 + 17, "2", size=15, weight="700")}{_show([(tb, None)], T)}</g>')
    # dòng đếm lần dưới mặt đất
    rows = [("Lần 1 · góc 60° · bóng sang trái", ta), ("Lần 2 · góc 300° · bóng sang phải", tb), ("Lần 3 · góc 420° = 60° + 360°", tc)]
    for i, (s, a) in enumerate(rows):
        b.append(f'<g opacity="1">{_txt(10, 226 + 20 * i, s, size=15, weight="700")}{_show([(a, None)], T)}</g>')
    caps = [
        (["Ghế quay đều, ngược chiều kim đồng hồ.", "Bóng trên đất đi qua đi lại."], [(0, ta)], False),
        (["Nửa vòng trên: bóng đi sang trái.", "Ghế quay 60° thì bóng tới cờ."], [(ta, tb)], False),
        (["Nửa vòng dưới: bóng đi sang phải.", "Ghế quay 300° là qua cờ lần nữa."], [(tb, tc - 0.3)], False),
        (["Thêm một vòng 360° là lại đúng như lần 1.", "Mỗi vòng, bóng qua cờ đúng 2 lần."], [(tc - 0.3, None)], True),
    ]
    for lines, win, fin in caps:
        b.append(_cap(lines, 294, fin, win, T))
    cap = ("Thời điểm = góc ghế đã quay chia tốc độ góc: $t=\\dfrac{\\Delta\\varphi}{\\omega}$. "
           "Vị trí không phải biên: lần $2k+1$ = lần 1 cộng $kT$, lần $2k+2$ = lần 2 cộng $kT$.")
    html = fig("meo-du-quay", "0 0 320 336",
               "Bóng đu quay: ghế quay đều ngược chiều kim đồng hồ, bóng trên mặt đất qua cờ ở nửa biên độ ba lần trong hơn một vòng",
               "".join(b), cap)
    return {
        "ten": "Bóng đu quay",
        "dieu_kien": "Chỉ dùng cho dao động điều hoà (lực hồi phục tỉ lệ với li độ, không ma sát; con lắc đơn chỉ khi biên nhỏ, "
                     "góc cực đại cỡ $10^\\circ$ trở xuống). Biên độ $A$ là bán kính vòng, $\\omega$ là tốc độ góc của vòng, "
                     "li độ $x$ là hình chiếu lên trục qua tâm, tính từ vị trí cân bằng. Chiều quay và dấu pha phải thống nhất với sách "
                     "(ở đây quay ngược chiều kim đồng hồ, góc tính từ trục $+x$).",
        "html": html + noi_voi_de,
    }


if __name__ == "__main__":
    m = bong_du_quay("")
    print(m["ten"], len(m["html"].encode()), "byte")
    out = os.environ.get("MEO_OUT")
    if out:
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "bong-du-quay.svg.html"), "w").write(
            '<!doctype html><meta charset="utf-8"><body style="max-width:343px;margin:16px;font-family:sans-serif">'
            + m["html"].replace('class="fig"', 'class="fig" style="margin:0"')
            + "<script>document.querySelector('[data-bt-run]').onclick=e=>{e.target.closest('figure').querySelectorAll('animate,animateTransform').forEach(a=>a.beginElement())}</script>")
