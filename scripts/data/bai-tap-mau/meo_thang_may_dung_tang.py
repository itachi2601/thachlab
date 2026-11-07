"""💡 Mẹo nhìn "Thang máy dừng tầng" (đồ thị/bảng nhiệt độ – thời gian khi đun đều) — L12 Bài 1 (lesson 2) dạng 3, 4.
Số liệu RIÊNG của mẹo (không lấy đáp số dạng 3, 4 — BANG-MEO-GIAI quy trình 3): A(0; 30) B(3; 80) C(7; 80) D(11; 220) E(18; 220) F(20; 290).
Cùng quy ước với meo_nhiet.py: khung gốc = khung CUỐI, mọi <animate> begin="indefinite" cùng dur, mốc bằng keyTimes.
Chạy thử: python3 scripts/data/bai-tap-mau/meo_thang_may_dung_tang.py  (MEO_OUT=thư mục → ghi bản xem thử)."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from hinh import fig, RED  # noqa: E402
from meo_nhiet import _anim, _show  # noqa: E402
from meo_nhiet import _txt as _txt14  # noqa: E402


def _txt(x, y, s, size=15, **kw):
    assert size >= 15  # H4: chữ trong hình >= 15
    return _txt14(x, y, s, size=size, **kw)


def _caption(lines, y0, final, windows, T):
    t = "".join(_txt(10, y0 + 19 * i, s, weight="500") for i, s in enumerate(lines))
    return f'<g opacity="{1 if final else 0}">{t}{_show(windows, T)}</g>'


AMBER = "#f59e0b"
# (phút, °C) của đồ thị mẹo và giây hoạt cảnh tương ứng mỗi điểm
PTS = [(0, 30), (3, 80), (7, 80), (11, 220), (18, 220), (20, 290)]
SEC = [1.0, 2.5, 5.5, 8.0, 11.5, 12.5]


def thang_may_dung_tang(noi_voi_de):
    (tA, TA), (tB, TB), (tC, TC), (tD, TD), (tE, TE), (tF, TF) = PTS
    NC, SOI = TB, TD
    assert TB == TC == 80 and TD == TE == 220 and tC - tB == 4 and tE - tD == 7
    # không trùng số của dạng 3 (232 °C, 5 phút) và dạng 4 (60/200 °C, 5/8 phút)
    assert {NC, SOI}.isdisjoint({60, 200, 232}) and {tC - tB, tE - tD}.isdisjoint({5, 8})
    assert tE - tD > tC - tB  # đoạn sôi dài hơn: chỗ mẹo phải nhấn "độ cao, không phải độ dài"
    T = 16
    gx = lambda t: 145 + 7 * t                    # trục phút: 7 px/phút
    gy = lambda c: round(190 - 0.48 * c, 1)       # trục °C, dùng chung cho thang máy (cùng độ cao)
    b = []
    # --- giếng thang + hai tầng dừng
    SX0, SX1, ST, SB = 14, 60, 28, 196
    b.append(f'<rect x="{SX0}" y="{ST}" width="{SX1 - SX0}" height="{SB - ST}" fill="none" stroke="currentColor" stroke-width="2" opacity=".6"/>')
    for c in (NC, SOI):
        y = gy(c)
        b.append(f'<line x1="{SX0}" y1="{y}" x2="{SX1}" y2="{y}" stroke="currentColor" stroke-width="2"/>')
        b.append(f'<line x1="{SX1}" y1="{y}" x2="{gx({NC: tB, SOI: tD}[c])}" y2="{y}" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4 4" opacity=".45"/>')
        b.append(_txt(66, y - 5, f"{c} °C", weight="600"))
    # --- buồng thang: khung gốc ở F, tịnh tiến theo đúng độ cao đồ thị
    CH = 22
    yF = gy(TF)
    b.append(f'<g><rect x="20" y="{yF - CH}" width="34" height="{CH}" rx="3" fill="{AMBER}" stroke="currentColor" stroke-width="2"/>'
             + _anim(None, [(s, f"0,{round(gy(c) - yF, 1)}") for s, (_, c) in zip(SEC, PTS)], T, transform=True) + "</g>")
    # --- ngọn lửa "đun đều" (tĩnh, V10)
    b.append(f'<path d="M37,222 C29,214 33,206 37,200 C39,207 46,211 41,222 Z" fill="{RED}" opacity=".85"/>')
    b.append(_txt(50, 220, "đun đều", weight="500"))
    # --- đồ thị T(t): trục + đường vẽ dần (dashoffset theo độ dài tích luỹ)
    b.append(f'<line x1="145" y1="190" x2="306" y2="190" stroke="currentColor" stroke-width="1.5" opacity=".6"/>')
    b.append(f'<line x1="145" y1="190" x2="145" y2="40" stroke="currentColor" stroke-width="1.5" opacity=".6"/>')
    b.append(_txt(151, 46, "T", weight="600"))
    b.append(_txt(306, 210, "t", anchor="end", weight="600"))
    xy = [(gx(t), gy(c)) for t, c in PTS]
    seg = [math.dist(xy[i], xy[i + 1]) for i in range(len(xy) - 1)]
    L = round(sum(seg), 1)
    acc = [0.0]
    for s in seg:
        acc.append(acc[-1] + s)
    d = " ".join(f"{'M' if i == 0 else 'L'}{x},{y}" for i, (x, y) in enumerate(xy))
    off = [(s, round(L - a, 1)) for s, a in zip(SEC, acc)]
    b.append(f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round" '
             f'stroke-dasharray="{L}" stroke-dashoffset="0">{_anim("stroke-dashoffset", [(0, L)] + off, T)}</path>')
    b.append(f'<circle cx="{xy[-1][0]}" cy="{xy[-1][1]}" r="5" fill="{AMBER}" stroke="currentColor" stroke-width="1.5">'
             f'{_anim("cx", [(s, x) for s, (x, _) in zip(SEC, xy)], T)}{_anim("cy", [(s, y) for s, (_, y) in zip(SEC, xy)], T)}</circle>')
    # tên hai chỗ dừng hiện khi thang tới tầng đó và giữ tới cuối
    b.append(f'<g opacity="1">{_txt(xy[2][0] + 8, gy(NC) + 22, "nóng chảy", anchor="middle", weight="600")}{_show([(SEC[1], None)], T)}</g>')
    b.append(f'<g opacity="1">{_txt((xy[3][0] + xy[4][0]) / 2, gy(SOI) - 8, "sôi", anchor="middle", weight="600")}{_show([(SEC[3], None)], T)}</g>')
    # --- số đọc theo chặng (dòng trên cùng)
    reads = [
        ("Phút 0 · 30 °C · thể rắn", 0, 1.0, False),
        ("Đi lên: chất rắn nóng lên", 1.0, 2.5, False),
        ("Dừng tầng 80 °C: 4 phút", 2.5, 5.5, False),
        ("Đi lên: chất lỏng nóng lên", 5.5, 8.0, False),
        ("Dừng tầng 220 °C: 7 phút", 8.0, 11.5, False),
        ("Đi lên: hơi nóng lên", 11.5, 13.5, False),
        ("Tầng thấp: nóng chảy, cao: sôi", 13.5, None, True),
    ]
    for s, a, e, fin in reads:
        b.append(f'<g opacity="{1 if fin else 0}">{_txt(10, 22, s, size=16, weight="700")}{_show([(a, e)], T)}</g>')
    # --- phụ đề theo chặng
    y = 240
    caps = [
        (["Đun đều: mỗi phút chất nhận nhiệt", "như nhau, nhiệt độ tăng dần."], [(0, 2.5)], False),
        (["Dừng tầng: nhiệt vẫn vào, nhưng trả", "cho nóng chảy nên T đứng yên."], [(2.5, 5.5)], False),
        (["Chảy hết mới đi tiếp. Chất lỏng", "nóng lên, dốc khác lúc còn rắn."], [(5.5, 8.0)], False),
        (["Dừng tầng sôi lâu hơn, nhưng tên", "chỗ dừng đọc theo tầng, không độ dài."], [(8.0, 11.5)], False),
        (["Sôi xong, hơi lại nóng lên.", "Mỗi chỗ dừng là một lần chuyển thể."], [(11.5, 13.5)], False),
        (["Độ cao chỗ dừng = nhiệt độ chuyển thể,", "dừng bao lâu = thời gian chuyển thể."], [(13.5, None)], True),
    ]
    for lines, win, fin in caps:
        b.append(_caption(lines, y, fin, win, T))
    cap = ("Thang máy dừng tầng: đun đều thì đoạn nằm ngang trên đồ thị $T(t)$ là lúc chất đang chuyển thể; "
           "chất vẫn nhận nhiệt nhưng nhiệt độ không đổi. Đi từ dưới lên, tầng dừng thấp là nóng chảy, tầng cao là sôi.")
    html = fig("meo-thang-may", "0 0 320 272",
               "Thang máy chạy lên cùng đồ thị nhiệt độ theo thời gian, dừng ở tầng 80 độ C khi nóng chảy 4 phút "
               "và tầng 220 độ C khi sôi 7 phút",
               "".join(b), cap)
    return {
        "ten": "Thang máy dừng tầng",
        "dieu_kien": "Chất kết tinh tinh khiết, áp suất không đổi (thuỷ tinh, nhựa đường không có chỗ dừng; nước muối thì nhiệt độ "
                     "vẫn trôi khi chuyển thể). Đun đều, cả khối cùng nhiệt độ. Đun từ thể rắn: dừng thấp là nóng chảy, "
                     "dừng cao là sôi. Làm nguội thì đi xuống, dừng đúng các tầng ấy. Bay hơi (chậm, ở mặt thoáng, ở mọi nhiệt độ) không tạo chỗ dừng; chỉ sôi mới tạo.",
        "html": html + noi_voi_de,
    }


if __name__ == "__main__":
    f = thang_may_dung_tang("")
    print(f["ten"], len(f["html"].encode()), "byte")
    out = os.environ.get("MEO_OUT")
    if out:
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "thang-may.svg.html"), "w").write(
            '<!doctype html><meta charset="utf-8"><body style="max-width:343px;margin:16px;font-family:sans-serif">'
            + f["html"].replace('class="fig"', 'class="fig" style="margin:0"'))
