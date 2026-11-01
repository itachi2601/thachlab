"""💡 Mẹo nhìn phần Nhiệt (docs/KE-HOACH-MEO-GIAI-BAI-TAP.md) — dùng chung cho HSG9 CĐ12 (bài 153) và L12 Ch.1.
Mỗi hàm trả {ten, dieu_kien, html}; html = hình SMIL bấm mới chạy (B4) + 1 câu nối với đề của dạng.
Khung gốc của mọi phần tử = khung CUỐI (chưa bấm / giảm chuyển động vẫn thấy kết luận); bấm thì chạy lại từ đầu.
Mọi <animate> cùng begin="indefinite", cùng dur, mốc thời gian bằng keyTimes (ContentHtml chỉ beginElement animate/animateTransform).
Chạy thử: python3 scripts/data/bai-tap-mau/meo_nhiet.py  → in kích thước + ghi /tmp xem nhanh nếu cần."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from hinh import fig, RED, BLUE  # noqa: E402


def _anim(attr, pts, T, discrete=False, transform=False):
    """pts = [(giây, giá trị)] tăng dần; tự thêm mốc 0 và T. Giá trị cuối phải trùng thuộc tính gốc (khung cuối)."""
    pts = sorted(pts, key=lambda p: p[0])
    if pts[0][0] > 0:
        pts = [(0, pts[0][1])] + pts
    if not discrete and pts[-1][0] < T:
        pts = pts + [(T, pts[-1][1])]
    kt = ";".join(f"{t / T:.4f}".rstrip("0").rstrip(".") or "0" for t, _ in pts)
    vals = ";".join(str(v) for _, v in pts)
    mode = ' calcMode="discrete"' if discrete else ""
    if transform:
        return (f'<animateTransform attributeName="transform" type="translate" values="{vals}" keyTimes="{kt}"'
                f' dur="{T}s" begin="indefinite" fill="freeze"{mode}/>')
    return f'<animate attributeName="{attr}" values="{vals}" keyTimes="{kt}" dur="{T}s" begin="indefinite" fill="freeze"{mode}/>'


def _show(windows, T):
    """opacity rời rạc: hiện trong các khoảng [(a, b)], b=None = tới hết."""
    pts = [(0, 0)]
    for a, b in windows:
        pts.append((a, 1))
        if b is not None:
            pts.append((b, 0))
    return _anim("opacity", pts, T, discrete=True)


def _txt(x, y, s, size=14, anchor="start", weight="600", fill="currentColor", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}"{extra}>{s}</text>'


def _caption(lines, y0, final, windows, T):
    op = "1" if final else "0"
    t = "".join(_txt(10, y0 + 19 * i, s, weight="500") for i, s in enumerate(lines))
    return f'<g opacity="{op}">{t}{_show(windows, T)}</g>'


def _mix(a, b, f):
    A = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    B = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    f = max(0.0, min(1.0, f))
    return "#" + "".join(f"{round(x + (y - x) * f):02x}" for x, y in zip(A, B))


def _f(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


# ---------------------------------------------------------------- Đòn bẩy nhiệt
def don_bay_nhiet(noi_voi_de):
    """Thả lần lượt 3 viên sắt 100 °C (mỗi viên nhiệt dung C) vào nước 20 °C; viên 1 cho 30 °C ⇒ C_nước = 7C."""
    K, T = 7, 15
    tn = lambda n: (K * 20 + 100 * n) / (K + n)
    t1, t2, t3 = tn(1), tn(2), tn(3)
    assert abs(t1 - 30) < 1e-9 and abs(t3 - 44) < 1e-9 and abs(t2 - 37.777) < 1e-2
    assert K * (t1 - 20) == 1 * (100 - t1)            # tay đòn 10 và 70 → 7 : 1
    X = lambda v: round(16 + (v - 20) / 80 * 288, 1)
    BY, AY = 92, 112                                  # dầm, trục nhiệt độ
    # lịch: (đầu, cuối) mỗi lần tiến lại; gộp ở cuối
    S = [(1.5, 4.5, 20, t1), (5.5, 8.0, t1, t2), (9.0, 11.0, t2, t3)]
    b = []
    # trục + vạch
    b.append(f'<line x1="{X(20)}" y1="{AY}" x2="{X(100)}" y2="{AY}" stroke="currentColor" stroke-width="2" opacity=".5"/>')
    for v in range(20, 101, 10):
        b.append(f'<line x1="{X(v)}" y1="{AY - 4}" x2="{X(v)}" y2="{AY + 4}" stroke="currentColor" stroke-width="1.5" opacity=".5"/>')
        if v % 20 == 0:
            b.append(_txt(X(v), AY + 21, f"{v}°", size=14, anchor="middle", weight="500"))
    # vết các điểm tựa cũ (hiện sau mỗi lần cân)
    for (_, e, _, tv), nxt in zip(S, (4.5, 8.0, 11.0)):
        b.append(f'<circle cx="{X(tv)}" cy="{AY}" r="4.5" fill="{RED}">{_show([(nxt, None)], T)}</circle>')
    # điểm tựa (tam giác) + số đọc
    piv_pts = [(0, f"{X(t1)},0")]
    for (a, e, _, tv) in S:
        piv_pts += [(a, f"{X(tv)},0")]
    tri = f'<polygon points="-9,{BY + 16} 9,{BY + 16} 0,{BY + 2}" fill="currentColor"/>'
    b.append(f'<g transform="translate({X(t3)},0)" opacity="1">{tri}{_anim("", piv_pts, T, discrete=True, transform=True)}'
             f'{_show([(1.5, None)], T)}</g>')
    for (a, e, _, tv), nxt in zip(S, (5.5, 9.0, None)):
        fin = nxt is None
        b.append(f'<g opacity="{1 if fin else 0}">{_txt(X(tv), AY + 40, _f(tv) + " °C", size=14, anchor="middle", weight="700")}'
                 f'{_show([(a, nxt)], T)}</g>')
    # dầm: hai đầu theo quả nặng trái / viên đang tới
    x1 = [(0, X(20))] + sum(([(a, X(f)), (e, X(to))] for a, e, f, to in S), [])
    x2 = [(0, X(100))] + sum(([(a - 0.5 if a > 2 else a, X(100)), (a, X(100)), (e, X(to))] for a, e, f, to in S), [])
    b.append(f'<line x1="{X(t3)}" y1="{BY}" x2="{X(t3)}" y2="{BY}" stroke="currentColor" stroke-width="3" stroke-linecap="round">'
             f'{_anim("x1", x1, T)}{_anim("x2", x2, T)}</line>')
    # quả nặng trái (nước + các viên đã thả) — cạnh to dần theo nhiệt dung
    sizes = {7: 30, 8: 33, 9: 36, 10: 39}
    lg_pts = [(0, f"{X(20)},0")] + sum(([(a, f"{X(f)},0"), (e, f"{X(to)},0")] for a, e, f, to in S), [])
    w_steps = [(0, 7), (4.5, 8), (8.0, 9), (11.0, 10)]
    rect = (f'<rect x="{-sizes[10] / 2}" y="{BY - sizes[10]}" width="{sizes[10]}" height="{sizes[10]}" rx="4" fill="{BLUE}">'
            + _anim("width", [(t, sizes[k]) for t, k in w_steps], T, discrete=True)
            + _anim("height", [(t, sizes[k]) for t, k in w_steps], T, discrete=True)
            + _anim("x", [(t, -sizes[k] / 2) for t, k in w_steps], T, discrete=True)
            + _anim("y", [(t, BY - sizes[k]) for t, k in w_steps], T, discrete=True) + "</rect>")
    labs = ""
    for txt, a, e in (("?", 0, 4.5), ("8C", 4.5, 8.0), ("9C", 8.0, 11.0), ("10C", 11.0, None)):
        labs += (f'<g opacity="{1 if e is None else 0}">{_txt(0, BY - 9, txt, size=14, anchor="middle", weight="700", fill="#0f172a")}'
                 f'{_show([(a, e)], T)}</g>')
    b.append(f'<g transform="translate({X(t3)},0)">{rect}{labs}{_anim("", lg_pts, T, transform=True)}</g>')
    # các viên sắt bên phải: hiện từ lúc xuất hiện tới khi gộp
    for k, (a, e, f, to) in enumerate(S, 1):
        appear = 0 if k == 1 else a - 0.5
        pts = [(0, f"{X(100)},0"), (a, f"{X(100)},0"), (e, f"{X(to)},0")]
        ball = (f'<circle cx="0" cy="{BY - 12}" r="12" fill="{RED}"/>'
                + _txt(0, BY - 7, "C", size=15, anchor="middle", weight="700", fill="#0f172a"))
        b.append(f'<g opacity="0" transform="translate({X(to)},0)">{ball}{_anim("", pts, T, transform=True)}{_show([(appear, e)], T)}</g>')
    # tay đòn khi viên 1 cân (dạy ý chính: 10 và 70)
    b.append(f'<g opacity="0">{_txt((X(20) + X(30)) / 2, BY - 40, "10°", size=15, anchor="middle")}'
             f'{_txt((X(30) + X(100)) / 2, BY - 40, "70°", size=15, anchor="middle")}'
             f'<line x1="{X(20)}" y1="{BY - 34}" x2="{X(30)}" y2="{BY - 34}" stroke="currentColor" stroke-dasharray="3 3"/>'
             f'<line x1="{X(30)}" y1="{BY - 34}" x2="{X(100)}" y2="{BY - 34}" stroke="currentColor" stroke-dasharray="3 3"/>'
             f'{_show([(1.5, 5.0)], T)}</g>')
    # phụ đề theo chặng (1 khối 2 dòng mỗi lúc)
    cy = 178
    caps = [
        (["Quả nặng = nhiệt dung. Nước 20 °C bên trái,", "viên sắt 100 °C bên phải."], [(0, 1.5)], False),
        (["Cân ở 30 °C: tay đòn 10° và 70°", "→ nước nặng gấp 7 viên: C(nước) = 7C."], [(1.5, 5.0)], False),
        (["Viên 2 cân với cả nước lẫn viên 1 (8C):", "8·(t − 30) = 100 − t → t ≈ 37,8 °C."], [(5.0, 8.5)], False),
        (["Quả trái nặng thêm C sau mỗi viên,", "điểm tựa nhích ít dần: 30 → 37,8 → 44 °C."], [(8.5, 12.0)], False),
        (["Thả bao nhiêu viên, điểm tựa cũng chỉ", "tiến dần tới 100 °C, không bao giờ vượt."], [(12.0, None)], True),
    ]
    for lines, win, fin in caps:
        b.append(_caption(lines, cy, fin, win, T))
    body = "".join(b)
    cap = ("Đòn bẩy nhiệt: quả nặng = nhiệt dung $mc$, điểm tựa = nhiệt độ cân bằng. "
           "Cân khi $C_1(t-t_1)=C_2(t_2-t)$ — tay đòn tỉ lệ nghịch với nhiệt dung.")
    html = fig("meo-don-bay", "0 40 320 172", "Đòn bẩy nhiệt trên trục nhiệt độ: thả lần lượt ba viên sắt 100 độ C vào nước 20 độ C", body, cap)
    return {
        "ten": "Đòn bẩy nhiệt",
        "dieu_kien": "Chỉ dùng khi không có vật nào chuyển thể, nhiệt dung riêng coi như không đổi "
                     "và bỏ qua trao đổi nhiệt với môi trường.",
        "html": html + noi_voi_de,
    }


# ---------------------------------------------------------------- Quỹ nhiệt
def quy_nhiet(noi_voi_de):
    """2 kg nước 80 °C, mỗi viên đá 50 g ở 0 °C; quỹ Q0 = 672 000 J, mỗi viên rút q = 17 000 J ⇒ N_max = 39."""
    c, lam, m, m0, t0 = 4200, 3.4e5, 2.0, 0.05, 80
    Q0, q = m * c * t0, lam * m0
    assert Q0 == 672000 and q == 17000
    Nmax = int(Q0 // q)
    du = Q0 - Nmax * q
    assert Nmax == 39 and du == 9000
    temp = lambda N: (Q0 - N * q) / ((m + N * m0) * c) if N <= Nmax else 0.0
    T = 17
    tN = lambda N: 2 + 0.25 * N                       # N viên tan xong ở giây tN(N); viên 40 rơi 13–13.8, tan dở tới 14.8
    MIL = [0, 10, 20, 30, 39]
    # hình học
    BX0, BX1, BTOP, BBOT = 20, 150, 30, 150           # bình
    lvl = lambda M: round(BBOT - 25 * M, 1)           # 2 kg → 50 px, 3,95 kg → 99 px
    QX, QW, QT, QH = 228, 44, 30, 120                 # cột quỹ
    qy = lambda E: round(QT + QH * (1 - E / Q0), 2)
    b = [f'<defs><clipPath id="meo-quy-clip"><path d="M{BX0} {BTOP} V{BBOT - 10} Q{BX0} {BBOT} {BX0 + 10} {BBOT} H{BX1 - 10} Q{BX1} {BBOT} {BX1} {BBOT - 10} V{BTOP} Z"/></clipPath></defs>']
    # nước: mực + màu theo N
    M_end = m + Nmax * m0 + (m0 * du / q)            # viên 40 tan được 9000/17000 phần
    lv_pts = [(tN(N), lvl(m + N * m0)) for N in range(0, Nmax + 1, 3)] + [(tN(Nmax), lvl(m + Nmax * m0)), (13.8, lvl(m + Nmax * m0)), (14.8, lvl(M_end))]
    col_pts = [(tN(N), _mix(RED, BLUE, 1 - temp(N) / t0)) for N in MIL] + [(13.8, _mix(RED, BLUE, 1 - temp(39) / t0)), (14.8, BLUE)]
    yE = lvl(M_end)
    b.append(f'<g clip-path="url(#meo-quy-clip)"><rect x="{BX0 - 5}" y="{yE}" width="{BX1 - BX0 + 10}" height="{BBOT + 10 - yE}" fill="{BLUE}" opacity=".55">'
             f'{_anim("y", lv_pts, T)}{_anim("height", [(t, round(BBOT + 10 - y, 1)) for t, y in lv_pts], T)}{_anim("fill", col_pts, T)}</rect></g>')
    b.append(f'<path d="M{BX0} {BTOP} V{BBOT - 10} Q{BX0} {BBOT} {BX0 + 10} {BBOT} H{BX1 - 10} Q{BX1} {BBOT} {BX1} {BBOT - 10} V{BTOP}" fill="none" stroke="currentColor" stroke-width="2.5" opacity=".6"/>')
    # viên đá: 8 lần rơi tượng trưng trong 2–11,75 s, rồi viên 40 rơi và nằm lại (nhỏ đi)
    cx, S0, S1 = 85, 18, round(18 * (1 - du / q) ** (1 / 3), 1)   # cạnh còn lại ∝ căn bậc ba khối lượng còn lại
    y_pts, op_pts = [(0, 6)], [(0, 0)]
    for i in range(8):
        a = 2 + i * 1.2
        surf = lvl(m + min(Nmax, (a + 0.9 - 2) / 0.25) * m0)
        y_pts += [(a, 6), (a + 0.9, surf - S0 / 2)]
        op_pts += [(a, 1), (a + 0.9, 0)]
    y_pts += [(13.0, 6), (13.8, yE - S1 / 2)]
    op_pts += [(13.0, 1)]
    sz = [(0, S0), (13.8, S0), (14.8, S1)]
    b.append(f'<g transform="translate({cx},{yE - S1 / 2})" opacity="1">'
             f'<rect x="{-S1 / 2}" y="{-S1 / 2}" width="{S1}" height="{S1}" rx="3" fill="#e0f2fe" stroke="{BLUE}" stroke-width="2">'
             f'{_anim("width", sz, T)}{_anim("height", sz, T)}{_anim("x", [(t, -v / 2) for t, v in sz], T)}{_anim("y", [(t, -v / 2) for t, v in sz], T)}</rect>'
             f'{_anim("", [(t, f"{cx},{y}") for t, y in y_pts], T, transform=True)}{_anim("opacity", op_pts, T, discrete=True)}</g>')
    # cột quỹ + 39 nấc
    b.append(_txt(QX + QW / 2, 20, "Quỹ nhiệt", size=14, anchor="middle", weight="700"))
    b.append(f'<rect x="{QX}" y="{QT}" width="{QW}" height="{QH}" rx="4" fill="none" stroke="currentColor" stroke-width="2" opacity=".6"/>')
    E_pts = [(tN(N), qy(Q0 - N * q)) for N in (0, Nmax)] + [(13.8, qy(du)), (14.8, qy(0))]
    yq = qy(0)
    b.append(f'<rect x="{QX + 2}" y="{yq}" width="{QW - 4}" height="{QT + QH - yq}" fill="{RED}">{_anim("y", E_pts, T)}'
             f'{_anim("height", [(t, round(QT + QH - y, 2)) for t, y in E_pts], T)}</rect>')
    for i in range(1, Nmax + 1):
        y = qy(Q0 - i * q)
        b.append(f'<line x1="{QX + 2}" y1="{y}" x2="{QX + QW - 2}" y2="{y}" stroke="currentColor" stroke-width="{1.2 if i % 10 == 0 else .5}" opacity=".45"/>')
    # số đọc theo mốc: E dưới cột quỹ; N và t dưới bình
    marks = [(0, 0)] + [(tN(N), N) for N in MIL[1:]] + [(13.8, 40)]
    for j, (a, N) in enumerate(marks):
        e = marks[j + 1][0] if j + 1 < len(marks) else None
        E = Q0 - N * q if N <= Nmax else 0
        tt = temp(N)
        ts = "0" if N > Nmax else (_f(tt, 2) if tt < 1 else _f(tt))
        fin = e is None
        g = (_txt(QX + QW / 2, 170, f"{E:,.0f} J".replace(",", " "), size=14, anchor="middle", weight="700")
             + _txt(BX0, 170, f"N = {N} viên · t ≈ {ts} °C", size=14, weight="700"))
        b.append(f'<g opacity="{1 if fin else 0}">{g}{_show([(a, e)], T)}</g>')
    cy = 196
    caps = [
        (["Mốc: nước 0 °C. Quỹ của 2 kg nước 80 °C là", "Q₀ = 2·4200·80 = 672 000 J."], [(0, 2)], False),
        (["Mỗi viên đá 50 g ở 0 °C rút đúng một nấc:", "q = λm₀ = 17 000 J. Nước nguội, nhiều thêm."], [(0 + 2, tN(Nmax))], False),
        (["Sau 39 viên quỹ còn 9 000 J: đá vẫn tan hết,", "nước còn ấm ≈ 0,54 °C."], [(tN(Nmax), 13.0)], False),
        (["Viên 40 cần 17 000 J, quỹ chỉ còn 9 000 J:", "còn đá, t = 0 °C. Vậy N tối đa = 39 viên."], [(13.0, None)], True),
    ]
    for lines, win, fin in caps:
        b.append(_caption(lines, cy, fin, win, T))
    cap = ("Quỹ nhiệt: lấy mốc nước lỏng 0 °C, nước nóng có quỹ $Q_0=mc\\,t$; mỗi viên đá rút $q$. "
           "Đá tan hết khi $Nq\\le Q_0$, nên $N_{max}$ là phần nguyên của $Q_0/q$.")
    html = fig("meo-quy", "0 0 320 238", "Quỹ nhiệt: bỏ lần lượt các viên đá 0 độ C vào 2 kg nước 80 độ C, cột quỹ cạn dần từng nấc", "".join(b), cap)
    return {
        "ten": "Quỹ nhiệt",
        "dieu_kien": "Mốc là nước lỏng ở 0&nbsp;°C và bỏ qua trao đổi nhiệt với môi trường. "
                     "Đá dưới 0&nbsp;°C thì mỗi viên rút thêm $m_0c_{đá}\\Delta t$ trước khi tan.",
        "html": html + noi_voi_de,
    }


if __name__ == "__main__":
    for f in (don_bay_nhiet(""), quy_nhiet("")):
        print(f["ten"], f"{len(f['html'].encode()) / 1024:.1f} KB")
        out = os.environ.get("MEO_OUT")
        if out:
            os.makedirs(out, exist_ok=True)
            open(os.path.join(out, f["ten"].replace(" ", "-") + ".svg.html"), "w").write(
                '<!doctype html><meta charset="utf-8"><body style="max-width:343px;margin:16px;font-family:sans-serif">'
                + f["html"].replace('class="fig"', 'class="fig" style="margin:0"')
                + "<script>document.querySelector('[data-bt-run]').onclick=e=>{e.target.closest('figure').querySelectorAll('animate,animateTransform').forEach(a=>a.beginElement())}</script>")
