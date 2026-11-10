"""💡 Mẹo nhìn "Ngồi trên bè" (docs/BANG-MEO-GIAI.md) — bài 162 dạng 4 (canô xuôi/ngược, bè, phao rơi).
Cùng quy ước với meo_nhiet.py: khung gốc = khung cuối, mọi animate begin="indefinite", cùng dur, keyTimes."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from meo_nhiet import _anim, _show, _txt, _caption, _f  # noqa: E402,F401


def _caption(lines, y0, final, windows, T):  # H4: phụ đề cỡ 15 (bản meo_nhiet là 14)
    t = "".join(_txt(10, y0 + 19 * i, s, size=15, weight="500") for i, s in enumerate(lines))
    return f'<g opacity="{1 if final else 0}">{t}{_show(windows, T)}</g>'
from hinh import fig, RED, BLUE  # noqa: E402


def ngoi_tren_be(noi_voi_de):
    """Thuyền ngược dòng làm rơi phao, 15 phút sau quay đầu; v_thuyền/nước = 4u. Hệ bờ: gặp lại phao sau đúng 15 phút nữa."""
    u, v, tdi = 2.0, 8.0, 15            # px/phút: nước, thuyền so với nước (v = 4u); phút
    # hệ bờ
    x0 = 130.0
    xb = x0 - (v - u) * tdi             # thuyền lúc quay đầu
    tve = (x0 + u * tdi - xb) / ((v + u) - u)  # phao cũng trôi: tốc độ lại gần = v
    assert abs(xb - 40) < 1e-9 and abs(tve - tdi) < 1e-9
    xb_end = xb + (v + u) * tve
    assert abs(xb_end - 190) < 1e-9 and abs(xb_end - (x0 + u * 2 * tdi)) < 1e-9
    assert (x0 - xb, xb_end - xb) == (90.0, 150.0)          # quãng đi ≠ quãng về so với bờ
    # hệ nước
    assert v * tdi == 120 and 160 - 120 == 40               # đi 120, về 120, đối xứng
    S = 0.3                                                   # giây hoạt hình / phút
    T, B0 = 20, 10
    assert abs(B0 + 2 * tdi * S - 19) < 1e-9
    WY, BY, FY = (72, 128), 90, 116
    b = []
    # nước + bờ
    b.append(f'<rect x="0" y="{WY[0]}" width="320" height="{WY[1] - WY[0]}" fill="{BLUE}" opacity=".18"/>')
    for y in WY:
        b.append(f'<line x1="0" y1="{y}" x2="320" y2="{y}" stroke="currentColor" stroke-width="2.5" opacity=".6"/>')
    posts = "".join(f'<rect x="{x - 3}" y="{WY[0] - 10}" width="6" height="10" fill="currentColor" opacity=".6"/>'
                    f'<rect x="{x - 3}" y="{WY[1]}" width="6" height="10" fill="currentColor" opacity=".6"/>'
                    for x in (20, 100, 180, 260, 340))
    b.append(f'<g transform="translate(-60,0)">{posts}{_anim("", [(0, "0,0"), (B0, "0,0"), (B0 + 9, "-60,0")], T, transform=True)}</g>')
    # --- nhóm A: nhìn từ bờ
    a = []
    a.append(_txt(10, 24, "Nhìn từ bờ", size=16, weight="700"))
    a.append(_txt(10, 48, "dòng nước →", size=15, weight="500"))
    for x in (60, 160, 260):
        a.append(f'<path d="M{x - 15} 103 H{x + 15} M{x + 7} 98 L{x + 15} 103 L{x + 7} 108" fill="none" stroke="{BLUE}" stroke-width="2" opacity=".6"/>')
    a.append(f'<circle cx="{x0:g}" cy="{FY}" r="7" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3 3"/>')
    a.append(f'<line x1="{x0:g}" y1="{BY + 6}" x2="{x0:g}" y2="{FY - 8}" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" opacity=".5"/>')
    a.append(f'<g opacity="0"><line x1="{x0:g}" y1="160" x2="{xb:g}" y2="160" stroke="currentColor" stroke-width="3"/>'
             f'{_txt(x0 + 8, 165, "đi: ngắn", size=15, weight="500")}{_show([(tdi * S, None)], T)}</g>')
    a.append(f'<g opacity="0"><line x1="{xb:g}" y1="184" x2="{xb_end:g}" y2="184" stroke="currentColor" stroke-width="3" stroke-dasharray="6 4"/>'
             f'{_txt(xb_end + 8, 189, "về: dài hơn", size=15, weight="500")}{_show([(2 * tdi * S, None)], T)}</g>')
    boat = ('<polygon points="-14,-8 14,-8 9,5 -9,5" fill="currentColor"/>')
    flt = f'<circle cx="0" cy="0" r="7" fill="{RED}"/>'
    a.append(f'<g transform="translate({xb_end:g},{FY})">{flt}{_anim("", [(0, f"{x0:g},{FY}"), (2 * tdi * S, f"{xb_end:g},{FY}")], T, transform=True)}</g>')
    a.append(f'<g transform="translate({xb_end:g},{BY})">{boat}'
             f'{_anim("", [(0, f"{x0:g},{BY}"), (tdi * S, f"{xb:g},{BY}"), (2 * tdi * S, f"{xb_end:g},{BY}")], T, transform=True)}</g>')
    b.append(f'<g opacity="0">{"".join(a)}{_show([(0, B0)], T)}</g>')
    # --- nhóm B: ngồi trên bè (hệ gắn với nước)
    g = []
    g.append(_txt(10, 24, "Ngồi trên bè (nước đứng yên)", size=16, weight="700"))
    g.append(_txt(10, 48, "← bờ trôi ngược lại", size=15, weight="500"))
    g.append(f'<g transform="translate(160,{FY})">{flt}</g>')
    g.append(f'<g transform="translate(160,{BY})">{boat}'
             f'{_anim("", [(0, f"160,{BY}"), (B0, f"160,{BY}"), (B0 + tdi * S, f"40,{BY}"), (B0 + 2 * tdi * S, f"160,{BY}")], T, transform=True)}</g>')
    g.append(f'<g>{"" }<line x1="160" y1="160" x2="40" y2="160" stroke="currentColor" stroke-width="3"/>'
             f'{_txt(100, 152, "đi 15 phút", size=15, anchor="middle", weight="600")}{_show([(B0 + tdi * S, None)], T)}</g>')
    g.append(f'<g><line x1="40" y1="184" x2="160" y2="184" stroke="currentColor" stroke-width="3" stroke-dasharray="6 4"/>'
             f'{_txt(100, 176, "về 15 phút", size=15, anchor="middle", weight="600")}{_show([(B0 + 2 * tdi * S, None)], T)}</g>')
    b.append(f'<g>{"".join(g)}{_show([(B0, None)], T)}</g>')
    caps = [
        (["Thuyền đi ngược dòng, đánh rơi phao;", "phao trôi xuôi cùng nước."], [(0, 4.5)], False),
        (["Sau 15 phút thuyền quay lại: quãng đi", "và về so với bờ khác nhau."], [(4.5, B0)], False),
        (["Ngồi trên bè: nước, phao đứng yên,", "còn bờ trôi ngược lại."], [(B0, 14.5)], False),
        (["Thuyền cùng tốc độ lúc đi và về:", "đi 15 phút thì về đúng 15 phút."], [(14.5, None)], True),
    ]
    for lines, win, fin in caps:
        b.append(_caption(lines, 214, fin, win, T))
    cap = ("Trong hệ gắn với nước, thuyền có cùng tốc độ $v$ cả đi lẫn về nên $t_{về}=t_{đi}$; "
           "rồi mới đổi lại về bờ.")
    html = fig("meo-be", "0 0 320 242", "Thuyền ngược dòng đánh rơi phao rồi quay lại: nhìn từ bờ quãng đi về khác nhau, nhìn từ nước thì đi bao lâu về bấy lâu",
               "".join(b), cap)
    return {
        "ten": "Ngồi trên bè",
        "dieu_kien": "Dòng nước đều, cùng vận tốc $u$ trên đoạn đang xét; phao hay bè trôi đúng bằng vận tốc nước "
                     "(không gió, không vướng bờ). Thuyền giữ nguyên vận tốc so với nước ở cả hai chiều, quay đầu tức thời, "
                     "không tắt máy; sông thẳng, chiều dòng không đổi. Mẹo chỉ nói thời gian đi bằng thời gian về khi thuyền quay lại gặp phao, "
                     "không dùng cho đoạn AB cố định so với bờ. Vận tốc thuyền trong mẹo là so với NƯỚC (đề cho so với bờ thì cộng/trừ $u$ trước) và phải lớn hơn $u$, không thì thuyền không ngược dòng được.",
        "html": html + noi_voi_de,
    }


if __name__ == "__main__":
    r = ngoi_tren_be("")
    print(len(r["html"].encode()), "byte")
    out = os.environ.get("MEO_OUT")
    if out:
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "be.svg.html"), "w").write(
            '<!doctype html><meta charset="utf-8"><body style="max-width:343px;margin:16px;font-family:sans-serif;color:#0f172a">'
            + r["html"].replace('class="fig"', 'class="fig" style="margin:0"')
            + "<script>document.querySelector('[data-bt-run]').onclick=e=>{e.target.closest('figure').querySelectorAll('animate,animateTransform').forEach(a=>a.beginElement())}</script>")
