"""💡 Mẹo nhìn "Cổng soát vé" (người = dòng điện, cổng khó qua = điện trở lớn) — gắn bài 90 d2, 157 d1.
Số mẹo: cổng R và 2R. Nối tiếp: 3 người qua cả hai cổng (I như nhau). Song song: 4 người qua R, 2 người qua 2R, lối chính 6.
Khung gốc = khung CUỐI; mọi <animate> cùng begin="indefinite", cùng dur (theo meo_nhiet)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from hinh import fig, RED, BLUE  # noqa: E402
from meo_nhiet import _anim, _show, _txt, _caption  # noqa: E402


def _caption(lines, y0, final, windows, T):  # H4: phụ đề cỡ 15 (bản meo_nhiet là 14)
    t = "".join(_txt(10, y0 + 19 * i, s, size=15, weight="500") for i, s in enumerate(lines))
    return f'<g opacity="{1 if final else 0}">{t}{_show(windows, T)}</g>'


def cong_soat_ve(noi_voi_de):
    T, D = 13, 4.0
    R1, R2 = 1, 2                                   # cổng R và 2R (đơn vị R)
    # --- số liệu: lượng người qua mỗi cổng trong cùng khoảng thời gian tỉ lệ nghịch R
    gap = {1: 5.0 / 2, 2: 5.0}                      # giãn cách giữa hai người liên tiếp (giây) ∝ R
    assert gap[2] / gap[1] == R2 / R1
    s1 = [1.0 + gap[1] * k for k in range(4)]       # làn R: 4 người
    s2 = [1.0 + gap[2] * k for k in range(2)]       # làn 2R: 2 người
    assert len(s1) == 4 and len(s2) == 2 and len(s1) + len(s2) == 6
    assert len(s1) / len(s2) == R2 / R1             # I1/I2 = R2/R1
    ss = [0.5 + 2.0 * k for k in range(3)]          # nối tiếp: 3 người, mỗi người qua cả hai cổng
    assert max(s1) + 3.6 < T and max(ss) + D < T
    YA, G1, G2 = 58, 100, 210                       # nối tiếp: làn, x hai cổng
    YB1, YB2, YH, GX = 152, 204, 178, 160           # song song: làn 1, làn 2, giữa sảnh, x cổng
    HX0, HX1 = 29, 291                              # tâm sảnh vào / sảnh ra
    b = []

    def gate(x, y, g, col):
        h = 14
        return "".join(f'<rect x="{x - 3}" y="{yy}" width="6" height="{h}" rx="2" fill="{col}"/>'
                       for yy in (y - g / 2 - h, y + g / 2))

    def counter(x, y, times, T=T, fmt="qua: {}", anchor="start"):
        """số đếm tăng rời rạc: nhóm n hiện từ mốc thứ n tới mốc n+1; nhóm cuối opacity gốc 1."""
        out, ts = [], sorted(times)
        edges = [0] + ts
        for n in range(len(ts) + 1):
            e = edges[n + 1] if n < len(ts) else None
            fin = e is None
            out.append(f'<g opacity="{1 if fin else 0}">{_txt(x, y, fmt.format(n), size=15, anchor=anchor, weight="700")}'
                       f'{_show([(edges[n], e)], T)}</g>')
        return "".join(out)

    # ---------- Panel A: nối tiếp
    b.append(_txt(10, 20, "Nối tiếp: một hàng, hai cổng", size=15, weight="700"))
    b.append(f'<line x1="10" y1="{YA}" x2="310" y2="{YA}" stroke="currentColor" stroke-width="2" stroke-dasharray="2 5" opacity=".45"/>')
    b.append(f'<polygon points="300,{YA - 6} 312,{YA} 300,{YA + 6}" fill="currentColor" opacity=".5"/>')
    b.append(gate(G1, YA, 22, BLUE) + gate(G2, YA, 12, RED))
    b.append(_txt(G1 - 10, YA - 12, "R", size=15, anchor="end", weight="700") + _txt(G2 - 10, YA - 12, "2R", size=15, anchor="end", weight="700"))
    X0, X1 = 14, 306
    for gx in (G1, G2):
        times = [s + D * (gx - X0) / (X1 - X0) for s in ss]
        b.append(counter(gx + 10, YA - 14, times))
    for s in ss:
        d = (f'<g opacity="0" transform="translate({X1},{YA})"><circle r="4.5" fill="currentColor"/>'
             f'{_anim("", [(s, f"{X0},{YA}"), (s + D, f"{X1},{YA}")], T, transform=True)}{_show([(s, s + D)], T)}</g>')
        b.append(d)

    # ---------- Panel B: song song
    b.append(_txt(10, 112, "Song song: hai làn, chung sảnh", size=15, weight="700"))
    for hx, nm in ((HX0, "vào"), (HX1, "ra")):
        b.append(f'<rect x="{hx - 21}" y="132" width="42" height="92" rx="8" fill="none" stroke="currentColor" stroke-width="2" opacity=".5"/>')
        b.append(_txt(hx, 216, nm, size=15, anchor="middle", weight="500"))
    L = [HX0, GX - 60, GX, GX + 60, HX1]
    for y in (YB1, YB2):
        b.append(f'<polyline points="{HX0 + 21},{YH - 8 if y < YH else YH + 8} 100,{y} 220,{y} {HX1 - 21},{YH - 8 if y < YH else YH + 8}"'
                 f' fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="2 5" opacity=".45"/>')
    b.append(gate(GX, YB1, 22, BLUE) + gate(GX, YB2, 12, RED))
    b.append(_txt(GX - 10, YB1 - 12, "R", size=15, anchor="end", weight="700") + _txt(GX - 10, YB2 - 12, "2R", size=15, anchor="end", weight="700"))
    d_ = DB = 3.6
    seg = [((HX0 - 0) ** 2 * 0 + ((100 - HX0) ** 2 + (YH - YB1) ** 2) ** .5), 120, ((100 - 29) ** 2 + (YB2 - YH) ** 2) ** .5]
    tot = sum(seg)
    f1, f2 = seg[0] / tot, (seg[0] + seg[1]) / tot
    crossings, exits = {YB1: [], YB2: []}, []
    for y, starts in ((YB1, s1), (YB2, s2)):
        for s in starts:
            pts = [(s, f"{HX0},{YH}"), (s + DB * f1, f"100,{y}"), (s + DB * f2, f"220,{y}"), (s + DB, f"{HX1},{YH}")]
            b.append(f'<g opacity="0" transform="translate({HX1},{YH})"><circle r="4.5" fill="currentColor"/>'
                     f'{_anim("", pts, T, transform=True)}{_show([(s, s + DB)], T)}</g>')
            crossings[y].append(s + DB / 2)
            exits.append(s + DB)
    assert abs(((f1 + f2) / 2) - 0.5) < 1e-9
    b.append(counter(GX + 12, YB1 - 14, crossings[YB1]))
    b.append(counter(GX + 12, YB2 - 14, crossings[YB2]))
    b.append(counter(312, 246, exits, fmt="lối chính: {}", anchor="end"))
    assert len(exits) == 6

    caps = [
        (["Mỗi chấm là một người. Cổng R dễ qua,", "cổng 2R khó qua gấp đôi."], [(0, 3.5)], False),
        (["Nối tiếp: mỗi cổng đếm cùng số người,", "không ai ứ lại giữa hai cổng."], [(3.5, 8.5)], False),
        (["Song song: cổng 2R qua ít đi một nửa,", "R qua 4 người thì 2R qua 2 người."], [(8.5, 11.5)], False),
        (["Lối chính = tổng hai làn: 4 + 2 = 6.", "Cổng càng khó, qua càng ít."], [(11.5, None)], True),
    ]
    for lines, win, fin in caps:
        b.append(_caption(lines, 276, fin, win, T))
    cap = ("Người qua mỗi phút = dòng $I$, cổng khó qua = điện trở $R$ lớn. "
           "Nối tiếp: $I$ như nhau; song song: $I=I_1+I_2$, $\\dfrac{I_1}{I_2}=\\dfrac{R_2}{R_1}$.")
    html = fig("meo-cong", "0 0 320 316", "Cổng soát vé: một hàng qua hai cổng nối tiếp, và hai làn song song chung sảnh vào, sảnh ra", "".join(b), cap)
    return {
        "ten": "Cổng soát vé",
        "dieu_kien": "Mạch ở trạng thái dừng (không đóng, ngắt hay nạp tụ), điện trở thuần $R$ không đổi theo dòng "
                     "(bóng dây tóc nóng lên thì không đúng) và dây nối coi như $R=0$. "
                     "Chỉ dòng một chiều hoặc mạch thuần trở (có tụ, cuộn cảm hay xoay chiều phải dùng $Z$ thay $R$), "
                     "mỗi nhánh chỉ có điện trở, không có nguồn riêng, và mạch phải rút được thành một hàng hoặc các làn (không phải cầu, tam giác). Mẹo chỉ nói về dòng điện, không nói về hiệu điện thế; nguồn có điện trở trong đáng kể thì thêm nhánh làm U của cả cụm giảm.",
        "html": html + noi_voi_de,
    }


if __name__ == "__main__":
    f = cong_soat_ve("")
    print(f["ten"], len(f["html"].encode()), "byte")
    out = os.environ.get("MEO_OUT")
    if out:
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "cong-soat-ve.svg.html"), "w").write(
            '<!doctype html><meta charset="utf-8"><body style="max-width:343px;margin:16px;font-family:sans-serif;color:#0f172a">'
            + f["html"].replace('class="fig"', 'class="fig" style="margin:0"'))
