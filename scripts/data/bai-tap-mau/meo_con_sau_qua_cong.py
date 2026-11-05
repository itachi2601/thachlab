"""💡 Mẹo nhìn "Con sâu qua cổng" (bài 162 · dạng 3). Sâu dài L = 4 cm bò đều 1 cm/s qua cổng dài d = 6 cm.
Theo dõi MỘT điểm (đầu sâu): từ đầu vào tới đuôi ra, đầu đi d + L = 10 cm → t = 10 s.
Khung gốc = khung cuối; mọi <animate> cùng dur, begin="indefinite", fill="freeze". Thời gian hình = thời gian thật (đi từ giây 2 tới 12)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from meo_nhiet import _anim, _show, _txt, _f  # noqa: E402
from hinh import fig, RED, BLUE  # noqa: E402


def _cap(lines, y0, final, windows, T):
    t = "".join(_txt(10, y0 + 20 * i, s, size=15, weight="500") for i, s in enumerate(lines))
    return f'<g opacity="{1 if final else 0}">{t}{_show(windows, T)}</g>'


def con_sau_qua_cong(noi_voi_de):
    d, L, v = 6, 4, 1                       # cm, cm, cm/s
    t_tot = (d + L) / v
    assert t_tot == 10 and t_tot not in (12, 40, 12.8, 64)
    K = 20                                   # 1 cm = 20 đơn vị
    G0, G1 = 110, 110 + d * K                # cổng
    H0, TL0 = G0, G0 - L * K                 # đầu / đuôi lúc đầu
    T, a = 15, 2                             # tổng; bắt đầu bò
    t_head_out, t_tail_out = a + d / v, a + (d + L) / v
    assert (t_head_out, t_tail_out) == (8, 12)
    dx = (d + L) * K
    assert G1 + L * K + 10 <= 320 and TL0 >= 10
    Y, TY = 70, 118
    b = []
    # đường đi của đầu: d (đỏ) rồi L (xanh), mọc dần theo đầu
    b.append(f'<line x1="{G0}" y1="{TY}" x2="{G1}" y2="{TY}" stroke="{RED}" stroke-width="4">'
             f'{_anim("x2", [(a, G0), (t_head_out, G1)], T)}</line>')
    b.append(f'<line x1="{G1}" y1="{TY}" x2="{G1 + L * K}" y2="{TY}" stroke="{BLUE}" stroke-width="4">'
             f'{_anim("x2", [(t_head_out, G1), (t_tail_out, G1 + L * K)], T)}</line>')
    for x in (G0, G1, G1 + L * K):
        b.append(f'<line x1="{x}" y1="{TY - 6}" x2="{x}" y2="{TY + 6}" stroke="currentColor" stroke-width="2"/>')
    b.append(f'<g opacity="1">{_txt((G0 + G1) / 2, TY + 26, f"d = {d} cm", size=15, anchor="middle", weight="700")}{_show([(t_head_out, None)], T)}</g>')
    b.append(f'<g opacity="1">{_txt(G1 + L * K / 2, TY + 26, f"L = {L} cm", size=15, anchor="middle", weight="700")}{_show([(t_tail_out, None)], T)}</g>')
    b.append(f'<line x1="{G0}" y1="{Y + 12}" x2="{G0}" y2="{TY - 6}" stroke="currentColor" stroke-dasharray="3 3" opacity=".5"/>')
    b.append(f'<line x1="{G1}" y1="{Y + 12}" x2="{G1}" y2="{TY - 6}" stroke="currentColor" stroke-dasharray="3 3" opacity=".5"/>')
    # sâu: 4 đốt, ở khung cuối (đã ra khỏi cổng) = dịch dx
    segs = "".join(f'<rect x="{TL0 + i * K + 1}" y="{Y - 10}" width="{K - 2}" height="20" rx="6" fill="#86efac" stroke="#15803d" stroke-width="1.5"/>'
                   for i in range(L))
    ends = (f'<circle cx="{H0}" cy="{Y}" r="6" fill="{RED}"/><circle cx="{TL0}" cy="{Y}" r="6" fill="{BLUE}"/>')
    pts = [(0, "0,0"), (a, "0,0"), (t_tail_out, f"{dx},0")]
    b.append(f'<g transform="translate({dx},0)">{segs}{ends}{_anim("", pts, T, transform=True)}</g>')
    # cổng phủ lên sâu (nhìn như đường hầm)
    b.append(f'<rect x="{G0}" y="{Y - 26}" width="{G1 - G0}" height="52" rx="4" fill="currentColor" fill-opacity=".1" stroke="currentColor" stroke-width="2.5" opacity="1"/>')
    b.append(_txt((G0 + G1) / 2, Y - 33, f"cổng {d} cm", size=15, anchor="middle", weight="700"))
    cy = 182
    caps = [
        (["Đầu sâu (chấm đỏ) chạm cổng. Sâu dài", "4 cm bò đều 1 cm/s, cổng dài 6 cm."], [(0, a)], False),
        (["Đầu đi hết cổng: 6 cm, mất 6 s.", "Đuôi (chấm xanh) còn ở trong cổng."], [(a, t_head_out)], False),
        (["Đầu đi thêm 4 cm (bằng chiều dài", "sâu) thì đuôi mới ra khỏi cổng."], [(t_head_out, t_tail_out)], False),
        (["Đuôi vừa ra: đầu đi 6 + 4 = 10 cm,", "nên t = 10 : 1 = 10 s."], [(t_tail_out, None)], True),
    ]
    for lines, win, fin in caps:
        b.append(_cap(lines, cy, fin, win, T))
    cap = "Theo dõi MỘT điểm (đầu sâu): quãng đường $s=d+L$, $t=\\dfrac{d+L}{v}$. Qua một điểm đứng yên thì $d=0$."
    html = fig("meo-sau", "0 24 320 190", "Con sâu dài 4 cm bò đều qua cổng dài 6 cm: đầu đi 6 cm rồi thêm 4 cm thì đuôi ra", "".join(b), cap)
    return {
        "ten": "Con sâu qua cổng",
        "dieu_kien": "Vật cứng, chiều dài $L$ không đổi, coi là đoạn thẳng; cầu hoặc hầm thẳng dài $d$; chuyển động đều "
                     "trên cả đoạn tính (đổi vận tốc thì chia theo từng đoạn). Mốc từ lúc đầu vào tới lúc đuôi ra "
                     "mới đi $d+L$; &quot;đầu ra khỏi cầu&quot; chỉ đi $d$, &quot;nằm trọn trong hầm&quot; là $d-L$.",
        "html": html + noi_voi_de,
    }


if __name__ == "__main__":
    f = con_sau_qua_cong("")
    print(f["ten"], len(f["html"].encode()), "byte")
    out = os.environ.get("MEO_OUT")
    if out:
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "sau.html"), "w").write(
            '<!doctype html><meta charset="utf-8"><body style="max-width:343px;margin:16px;font-family:sans-serif;color:#0f172a">' + f["html"])
