"""💡 Mẹo nhìn "Mắt xích yếu nhất" (lực căng dọc chuỗi xích = dòng qua các đèn nối tiếp) — gắn bài 165 (HSG 9 CĐ05) d4.
Số mẹo (khác số của đề): đèn A 3 V – 0,6 W (0,2 A, 15 Ω), đèn B 6 V – 1,8 W (0,3 A, 20 Ω) → I_max = 0,2 A, U_max = 7 V (không phải 3 + 6 = 9 V).
Chuỗi xích: mắt mảnh chịu 2, mắt dày chịu 3 → cả chuỗi chịu 2.
Khung gốc = khung CUỐI; mọi <animate> cùng begin="indefinite", cùng dur (theo meo_nhiet). Bảng tra: docs/BANG-MEO-GIAI.md."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "../../../.claude/skills/soan-bai-tap-mau/scripts"))
from hinh import fig, RED  # noqa: E402
from meo_nhiet import _anim, _show, _txt  # noqa: E402

AMBER = "#f59e0b"


def _caption(lines, y0, final, windows, T):
    t = "".join(_txt(10, y0 + 19 * i, s, size=15, weight="500") for i, s in enumerate(lines))
    return f'<g opacity="{1 if final else 0}">{t}{_show(windows, T)}</g>'


def _counter(x, y, steps, T, anchor="middle"):
    """steps = [(giây bắt đầu, chữ)]: mỗi chữ hiện từ mốc của nó tới mốc kế; chữ cuối là khung gốc."""
    out = []
    for n, (t0, s) in enumerate(steps):
        t1 = steps[n + 1][0] if n + 1 < len(steps) else None
        out.append(f'<g opacity="{1 if t1 is None else 0}">{_txt(x, y, s, size=15, anchor=anchor, weight="700")}'
                   f'{_show([(t0, t1)], T)}</g>')
    return "".join(out)


def mat_xich_yeu_nhat(noi_voi_de):
    T = 12
    # --- số liệu của mẹo
    UA, PA, UB, PB = 3.0, 0.6, 6.0, 1.8
    IA, IB = PA / UA, PB / UB
    RA, RB = UA ** 2 / PA, UB ** 2 / PB
    assert abs(IA - 0.2) < 1e-9 and abs(IB - 0.3) < 1e-9 and abs(RA - 15) < 1e-9 and abs(RB - 20) < 1e-9
    Imax = min(IA, IB)
    Umax = Imax * (RA + RB)
    assert abs(Umax - 7) < 1e-9 and abs(UA + UB - 9) < 1e-9
    sangB = Imax ** 2 * RB / PB                      # đèn B chỉ đạt 44 % công suất định mức
    assert abs(sangB - 4 / 9) < 1e-9
    b = []

    # ---------- Panel A: chuỗi xích (0–6 s)
    Y = 56
    b.append(_txt(10, 20, "Chuỗi xích: lực kéo như nhau ở mọi mắt", size=15, weight="700"))
    b.append(f'<line x1="16" y1="{Y - 22}" x2="16" y2="{Y + 22}" stroke="currentColor" stroke-width="4"/>')
    b.append(f'<line x1="16" y1="{Y}" x2="34" y2="{Y}" stroke="currentColor" stroke-width="2.2"/>')
    b.append(f'<rect x="30" y="{Y - 12}" width="88" height="24" rx="12" fill="none" stroke="currentColor" stroke-width="2.2"/>')
    # mắt mảnh chuyển đỏ khi lực kéo chạm sức chịu (từ 3 s)
    b.append(f'<g opacity="1"><rect x="30" y="{Y - 12}" width="88" height="24" rx="12" fill="none" stroke="{RED}" stroke-width="3"/>'
             f'{_show([(3, None)], T)}</g>')
    b.append(f'<rect x="106" y="{Y - 12}" width="88" height="24" rx="12" fill="none" stroke="currentColor" stroke-width="5.5"/>')
    b.append(f'<line x1="194" y1="{Y}" x2="236" y2="{Y}" stroke="currentColor" stroke-width="2.2"/>')
    b.append(f'<polygon points="234,{Y - 7} 248,{Y} 234,{Y + 7}" fill="currentColor"/>')
    b.append(_txt(74, Y + 34, "chịu 2", size=15, anchor="middle", weight="600"))
    b.append(_txt(150, Y + 34, "chịu 3", size=15, anchor="middle", weight="600"))
    b.append(_counter(282, Y + 5, [(0, "kéo: 0"), (1.5, "kéo: 1"), (3, "kéo: 2")], T))

    # ---------- Panel B: hai đèn nối tiếp (6–12 s)
    YC, XA, XB, R = 172, 84, 228, 17
    b.append(_txt(10, 122, "Nối tiếp: A (3 V–0,6 W), B (6 V–1,8 W)", size=15, weight="700"))
    for x0, x1 in ((12, XA - R), (XA + R, XB - R), (XB + R, 308)):
        b.append(f'<line x1="{x0}" y1="{YC}" x2="{x1}" y2="{YC}" stroke="currentColor" stroke-width="2.2"/>')
    for x, op_end in ((XA, 0.95), (XB, round(0.95 * sangB, 2))):
        b.append(f'<circle cx="{x}" cy="{YC}" r="{R}" fill="{AMBER}" fill-opacity="{op_end}" stroke="currentColor" stroke-width="2.2">'
                 f'{_anim("fill-opacity", [(6, 0), (8, op_end)], T)}</circle>')
        k = R * 0.62
        b.append(f'<path d="M{x - k},{YC - k} L{x + k},{YC + k} M{x - k},{YC + k} L{x + k},{YC - k}" stroke="currentColor" stroke-width="1.8" fill="none"/>')
    b.append(_txt(XA, YC - 26, "A: tối đa 0,2 A", size=15, anchor="middle", weight="600"))
    b.append(_txt(XB, YC - 26, "B: tối đa 0,3 A", size=15, anchor="middle", weight="600"))
    b.append(f'<g opacity="1">{_txt(XA, YC + 36, "đủ sáng", size=15, anchor="middle", weight="700")}{_show([(8, None)], T)}</g>')
    b.append(f'<g opacity="1">{_txt(XB, YC + 36, "còn yếu", size=15, anchor="middle", weight="600")}{_show([(8, None)], T)}</g>')
    b.append(_counter(160, YC + 60, [(0, "dòng: 0 A"), (6.7, "dòng: 0,1 A"), (8, "dòng: 0,2 A")], T))

    caps = [
        (["Mỗi mắt xích có sức chịu riêng:", "mắt mảnh chịu 2, mắt dày chịu 3."], [(0, 3)], False),
        (["Kéo tới 2: mắt mảnh vừa hết sức.", "Cả chuỗi chỉ chịu 2, không phải 3."], [(3, 6)], False),
        (["Hai đèn nối tiếp: cùng một dòng.", "Tới 0,2 A thì đèn A đã đủ sáng."], [(6, 9.5)], False),
        (["Dừng ở dòng định mức nhỏ hơn: 0,2 A.", "U lớn nhất = 0,2 × (15 + 20) = 7 V."], [(9.5, None)], True),
    ]
    for lines, win, fin in caps:
        b.append(_caption(lines, 262, fin, win, T))
    cap = ("Lực kéo dọc chuỗi xích = dòng $I$ qua các đèn nối tiếp; sức chịu của mỗi mắt = dòng định mức "
           "$I_{đm}=\\dfrac{P_{đm}}{U_{đm}}$. Đèn A có $R=15\\ \\Omega$, đèn B có $R=20\\ \\Omega$ nên "
           "$U_{max}=0{,}2\\cdot35=7\\ \\text{V}$, không phải $3+6=9\\ \\text{V}$.")
    html = fig("meo-mat-xich", "0 0 320 292",
               "Mắt xích yếu nhất: chuỗi hai mắt xích chịu 2 và chịu 3, bên dưới là hai đèn nối tiếp có dòng định mức 0,2 A và 0,3 A",
               "".join(b), cap)
    return {
        "ten": "Mắt xích yếu nhất",
        "dieu_kien": "Điện trở mỗi đèn coi như không đổi. "
                     "Các đèn nối tiếp thẳng vào nguồn, không có biến trở hay điện trở phụ. "
                     "Chỉ dùng khi đề hỏi giá trị lớn nhất để không đèn nào vượt định mức.",
        "html": html + noi_voi_de,
    }


if __name__ == "__main__":
    f = mat_xich_yeu_nhat("")
    print(f["ten"], len(f["html"].encode()), "byte")
    out = os.environ.get("MEO_OUT")
    if out:
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "mat-xich-yeu-nhat.svg.html"), "w").write(
            '<!doctype html><meta charset="utf-8"><body style="max-width:343px;margin:16px;font-family:sans-serif;color:#0f172a">'
            + f["html"].replace('class="fig"', 'class="fig" style="margin:0"'))
