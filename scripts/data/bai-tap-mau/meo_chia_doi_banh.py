"""💡 Mẹo nhìn "Chia đôi bánh" (phóng xạ: N = N0·2^(-t/T)) — L12 Bài 17 dạng 2 (cần kiểm chỉ số dạng khi gắn).
Cùng quy ước với meo_nhiet.py: khung gốc = khung CUỐI, mọi <animate> begin="indefinite" cùng dur, mốc bằng keyTimes.
Chạy thử: python3 scripts/data/bai-tap-mau/meo_chia_doi_banh.py  (MEO_OUT=thư mục → ghi bản xem thử)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from hinh import fig, RED  # noqa: E402
from meo_nhiet import _anim, _show, _f  # noqa: E402
from meo_nhiet import _txt as _txt14  # noqa: E402


def _txt(x, y, s, size=15, **kw):
    assert size >= 15  # H4: chữ trong hình >= 15
    return _txt14(x, y, s, size=size, **kw)


def _caption(lines, y0, final, windows, T):
    t = "".join(_txt(10, y0 + 19 * i, s, weight="500") for i, s in enumerate(lines))
    return f'<g opacity="{1 if final else 0}">{t}{_show(windows, T)}</g>'


AMBER = "#f59e0b"


def chia_doi_banh(noi_voi_de):
    """Bánh dài 100 %: sau T còn 1/2, 2T còn 1/4, 3T còn 1/8 = 12,5 %; rồi t = 1,5T còn 2^-1,5 ≈ 35,4 %."""
    N = lambda n: 2 ** -n
    assert abs(N(1.5) - 0.3536) < 5e-5 and abs(N(3) - 0.125) < 1e-12 and 0.25 < N(1.5) < 0.375
    T = 15
    X0, W, CY, CH = 40, 240, 34, 48                    # bánh: x, rộng 100 %, y, cao
    w = lambda n: round(W * N(n), 2)
    LY0, LY1 = 128, 172                                # đường cong N(t): N = 1 ở y=128, N = 0 ở y=172
    cx = lambda n: X0 + 80 * n                         # trục thời gian: 80 đơn vị / chu kì
    cy = lambda n: round(LY1 - (LY1 - LY0) * N(n), 1)
    b = []
    # --- bánh: viền nét đứt = bánh nguyên, phần tô = phần còn lại
    b.append(f'<rect x="{X0}" y="{CY}" width="{W}" height="{CH}" rx="6" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="5 4" opacity=".6"/>')
    pts = [(0, W), (1.5, W), (4, w(1)), (6.5, w(2)), (9, w(3)), (10.5, w(1.5))]
    b.append(f'<rect x="{X0}" y="{CY}" width="{w(1.5)}" height="{CH}" rx="6" fill="{AMBER}" stroke="currentColor" stroke-width="2">{_anim("width", pts, T)}</rect>')
    # --- thước 0–100 %
    RY = CY + CH + 8
    b.append(f'<line x1="{X0}" y1="{RY}" x2="{X0 + W}" y2="{RY}" stroke="currentColor" stroke-width="1.5" opacity=".6"/>')
    for k in (0, 50, 100):
        x = X0 + W * k / 100
        b.append(f'<line x1="{x}" y1="{RY - 4}" x2="{x}" y2="{RY + 4}" stroke="currentColor" stroke-width="1.5" opacity=".6"/>')
    b.append(_txt(X0, RY + 22, "0", anchor="middle", weight="500"))
    b.append(_txt(X0 + W, RY + 22, "100 %", anchor="middle", weight="500"))
    # --- hai vạch SAI (25 % và 37,5 %) chỉ hiện ở chặng cuối
    sai = ""
    for k, lab in ((25, "25"), (37.5, "37,5")):
        x = X0 + W * k / 100
        sai += f'<line x1="{x}" y1="{CY - 6}" x2="{x}" y2="{RY}" stroke="{RED}" stroke-width="2" stroke-dasharray="3 3"/>'
    sai += _txt(X0 + W * .25 - 4, RY + 22, "25", anchor="end", weight="600", fill=RED)
    sai += _txt(X0 + W * .375 + 4, RY + 22, "37,5", anchor="start", weight="600", fill=RED)
    b.append(f'<g opacity="1">{sai}{_show([(9.5, None)], T)}</g>')
    # --- đường cong N(t) mờ + 4 điểm
    cur = " ".join(f"{'M' if i == 0 else 'L'}{cx(i / 10 * 3):.1f},{cy(i / 10 * 3)}" for i in range(0, 11))
    b.append(f'<path d="{cur}" fill="none" stroke="currentColor" stroke-width="2" opacity=".4"/>')
    b.append(f'<line x1="{X0}" y1="{LY1}" x2="{X0 + 240}" y2="{LY1}" stroke="currentColor" stroke-width="1.5" opacity=".5"/>')
    for n, lab in ((1, "T"), (2, "2T"), (3, "3T")):
        t0 = {1: 1.5, 2: 4, 3: 6.5}[n]
        b.append(f'<circle cx="{cx(n)}" cy="{cy(n)}" r="4.5" fill="{AMBER}" stroke="currentColor" stroke-width="1.5" opacity="1">{_show([(t0, None)], T)}</circle>')
    for n, lab in ((1, "T"), (2, "2T"), (3, "3T")):
        b.append(_txt(cx(n), LY1 + 20, lab, anchor="middle", weight="500"))
    b.append(f'<circle cx="{cx(1.5)}" cy="{cy(1.5)}" r="5.5" fill="{RED}" stroke="currentColor" stroke-width="1.5" opacity="1">{_show([(9.5, None)], T)}</circle>')
    b.append(_txt(X0 - 8, LY0 + 5, "1", anchor="end", weight="500"))
    # --- số đọc theo chặng (dòng trên cùng)
    reads = [
        ("t = 0 · còn 100 %", 0, 1.5, False),
        ("t = T · còn 1/2 = 50 %", 1.5, 4, False),
        ("t = 2T · còn 1/4 = 25 %", 4, 6.5, False),
        ("t = 3T · còn 1/8 = 12,5 %", 6.5, 9.5, False),
        ("t = 1,5T · còn ≈ 35,4 %", 9.5, None, True),
    ]
    for s, a, e, fin in reads:
        b.append(f'<g opacity="{1 if fin else 0}">{_txt(10, 22, s, size=16, weight="700")}{_show([(a, e)], T)}</g>')
    # --- phụ đề theo chặng
    y = 214
    caps = [
        (["Bánh nguyên. Cứ sau mỗi chu kì T,", "bánh bị chia đôi, bỏ một nửa."], [(0, 1.5)], False),
        (["Sau T: còn một nửa.", "Nửa bỏ đi là phần đã phân rã."], [(1.5, 4)], False),
        (["Sau 2T: còn 1/4, chưa hết đâu:", "không phải trừ đều mỗi chu kì."], [(4, 6.5)], False),
        (["Sau 3T: còn 1/8 = 12,5 %.", "Mỗi chu kì chỉ bỏ nửa phần đang có."], [(6.5, 9.5)], False),
        (["Lùi về 1,5T: còn ≈ 35,4 %, không", "phải 25 % hay 37,5 % (hai vạch đỏ)."], [(9.5, 12.5)], False),
        (["Sau n chu kì còn (1/2)^n,", "n không cần là số nguyên."], [(12.5, None)], True),
    ]
    for lines, win, fin in caps:
        b.append(_caption(lines, y, fin, win, T))
    cap = ("Chia đôi bánh: $N=N_0\\cdot 2^{-t/T}$, số hạt đã phân rã $=N_0-N$. "
           "Với $t=1{,}5T$: $2^{-1{,}5}\\approx 0{,}354$.")
    html = fig("meo-banh", "0 0 320 246",
               "Cái bánh bị chia đôi sau mỗi chu kì bán rã: còn 1/2, 1/4, 1/8, rồi lùi về 1,5 chu kì còn khoảng 35,4 phần trăm",
               "".join(b), cap)
    return {
        "ten": "Chia đôi bánh",
        "dieu_kien": "Mẫu có rất nhiều hạt, mỗi hạt phân rã độc lập và hằng số phân rã không đổi "
                     "(không phụ thuộc nhiệt độ, áp suất hay hoá học). Chỉ một chất phóng xạ, hạt con không phóng xạ "
                     "hoặc đang tính riêng phần chất mẹ; đếm số hạt hay hoạt độ của chất đó, không đếm khối lượng cả mẫu "
                     "(hạt con vẫn nằm trong mẫu). Mẫu kín, $t=0$ là lúc còn nguyên chất mẹ; $t$ và $T$ cùng đơn vị.",
        "html": html + noi_voi_de,
    }


if __name__ == "__main__":
    f = chia_doi_banh("")
    print(f["ten"], len(f["html"].encode()), "byte")
    out = os.environ.get("MEO_OUT")
    if out:
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "banh.svg.html"), "w").write(
            '<!doctype html><meta charset="utf-8"><body style="max-width:343px;margin:16px;font-family:sans-serif">'
            + f["html"].replace('class="fig"', 'class="fig" style="margin:0"'))
